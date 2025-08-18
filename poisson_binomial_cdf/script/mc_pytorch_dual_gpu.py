# mc_pytorch_dual_gpu.py
"""
GPU0: AMD Radeon Instinct MI50 - 32G
GPU1: AMD Radeon Instinct MI50 - 32G
OS: Ubuntu 22.04
PLAT: ROCm 6.3.4
"""
import time
import torch

@torch.inference_mode()
def mc_gpu_streaming_dual(p_int, limit, drafts, batch=20_000_000, seed=1234):
    """
    Two-GPU data-parallel Monte Carlo (fixed to cuda:0 and cuda:1).
    Splits each outer-loop batch across both GPUs and runs in parallel.
    """
    devices = ["cuda:0", "cuda:1"]
    ndev = 2

    # Per-device state
    ps = []
    gens = []
    drops_bufs = []
    n = None
    needed_drops = None

    for di, d in enumerate(devices):
        dev = torch.device(d)
        p = torch.tensor(p_int, dtype=torch.float32, device=dev) / 10000.0
        if n is None:
            n = p.numel()
            needed_drops = int(n - limit + 1)
        ps.append(p)
        gens.append(torch.Generator(device=dev).manual_seed(seed + di))
        drops_bufs.append(torch.empty(0, device=dev, dtype=torch.int16))

    total_1 = 0
    done = 0

    while done < drafts:
        m_total = min(batch, drafts - done)

        # Even split across the two GPUs
        m0 = m_total // ndev + (m_total % ndev > 0)
        m1 = m_total - m0
        m_per = (m0, m1)

        # Launch on both devices (async per device)
        for di, d in enumerate(devices):
            m = m_per[di]
            if m == 0:
                continue
            drops = drops_bufs[di]
            if drops.numel() != m:
                drops = torch.zeros(m, dtype=torch.int16, device=d)
                drops_bufs[di] = drops
            else:
                drops.zero_()

            p = ps[di]
            g = gens[di]

            # Stream RNG per player on this device
            for qi in p:
                u = torch.rand(m, generator=g, device=d, dtype=torch.float32)
                drops.add_((u <= qi).to(torch.int16))

        # Sync & reduce
        torch.cuda.synchronize("cuda:0")
        torch.cuda.synchronize("cuda:1")
        total_1 += int((drops_bufs[0] >= needed_drops).sum().item())
        if m1:
            total_1 += int((drops_bufs[1] >= needed_drops).sum().item())

        done += m_total

    total_0 = drafts - total_1
    return total_1, total_0


if __name__ == "__main__":
    list_p_int = [
        4667, 4400, 4000, 4000, 1304, 2128,
        3103, 5217, 1111, 2333, 857, 857,
        1400, 10000, 2500, 3333, 1250
    ]
    limit  = 14
    drafts = 1_000_000_000
    batch  = 50_000_000

    # Warm up both GPUs (helps allocator/JIT)
    _ = torch.rand(1, device="cuda:0")
    _ = torch.rand(1, device="cuda:1")
    torch.cuda.synchronize("cuda:0")
    torch.cuda.synchronize("cuda:1")

    t0 = time.perf_counter()
    c1, c0 = mc_gpu_streaming_dual(list_p_int, limit, drafts, batch=batch, seed=20250818)
    torch.cuda.synchronize("cuda:0")
    torch.cuda.synchronize("cuda:1")
    t1 = time.perf_counter()

    print(f"Total drafts: {drafts:,}")
    print(f"Returned 1: {c1:,}")
    print(f"Returned 0: {c0:,}")
    print(f"P(1): {c1/drafts:.8f}  P(0): {c0/drafts:.8f}")
    print(f"Elapsed: {t1 - t0:.4f}s")
