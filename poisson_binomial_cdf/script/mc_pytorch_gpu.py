import time
import torch

def mc_gpu_torch(p_int, limit, drafts, batch=10_000_000, seed=1234, device="cuda"):
    """
    Monte Carlo on GPU (ROCm/CUDA via PyTorch).
    p_int : list/array of ints in [0,10000] representing dropout probs * 10000
    limit : admission non-drop threshold (same semantics as your CPU code)
    drafts: total number of simulations
    batch : per-GPU-batch to fit VRAM (tune this)
    """
    dev = torch.device(device)
    p = torch.tensor(p_int, dtype=torch.float32, device=dev) / 10000.0
    n = p.numel()
    needed_drops = int(n - limit + 1)       # same equivalence as your CPU logic

    gen = torch.Generator(device=dev).manual_seed(seed)

    total_1 = 0
    done = 0
    while done < drafts:
        m = min(batch, drafts - done)
        # Uniforms on GPU; compare to p on GPU; reduce on GPU
        u = torch.rand((m, n), generator=gen, device=dev, dtype=torch.float32)
        drops = (u <= p).sum(dim=1)
        total_1 += int((drops >= needed_drops).sum().item())
        done += m

    total_0 = drafts - total_1
    return total_1, total_0

if __name__ == "__main__":
    list_p_int = [
        4667, 4400, 4000, 4000, 1304, 2128,
        3103, 5217, 1111, 2333, 857, 857,
        1400, 10000, 2500, 3333, 1250
    ]
    limit = 14
    drafts = 100_000_000
    batch  = 10_000_000    # tune to 32GB VRAM

    t0 = time.perf_counter()
    c1, c0 = mc_gpu_torch(list_p_int, limit, drafts, batch=batch, seed=20250818)
    t1 = time.perf_counter()

    print(f"Total drafts: {drafts:,}")
    print(f"Returned 1: {c1:,}")
    print(f"Returned 0: {c0:,}")
    print(f"P(1): {c1/drafts:.8f}  P(0): {c0/drafts:.8f}")
    print(f"Elapsed: {t1 - t0:.4f}s")
