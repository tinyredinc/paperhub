import time
import numpy as np
import multiprocessing as mp


def worker(list_p_np, limit, chunk_iters):
    """Simulate `chunk_iters` drafts and return how many produced outcome=1."""
    # Generate random numbers for all drafts in this worker
    list_rand_all = np.random.randint(0, 10001, size=(chunk_iters, len(list_p_np)))
    # Count per draft how many times p_i < rand_i
    tmp_counts = np.sum(list_p_np < list_rand_all, axis=1)
    # Outcome = 1 if that count < limit, else 0
    return np.sum(tmp_counts < limit)


def parallel_vectorized(list_p_np, limit, drafts, num_workers):
    """Run `drafts` simulations in parallel, split across `num_workers` processes."""
    chunk = drafts // num_workers
    remainder = drafts % num_workers
    tasks = [(list_p_np, limit, chunk) for _ in range(num_workers)]
    if remainder > 0:
        tasks[0] = (list_p_np, limit, chunk + remainder)

    with mp.Pool(num_workers) as pool:
        counts_1 = pool.starmap(worker, tasks)

    total_1 = sum(counts_1)
    total_0 = drafts - total_1
    return total_1, total_0


if __name__ == "__main__":

    # Problem setup
    list_p_np = np.array([4667, 4400, 4000, 2333, 5217, 3103, 1111, 4000, 2128, 1304, 2128, 10000, 10000, 1400, 1400, 857, 857, 3333])
    limit = 14

    # Simulation parameters
    batch_size = 10_000_000   # drafts per batch
    iterations = 1          # number of batches
    num_workers = mp.cpu_count()

    total_1 = 0
    total_0 = 0
    p1_history = []  # store P(1) after each batch

    start = time.perf_counter()
    for i in range(1, iterations + 1):
        c1, c0 = parallel_vectorized(list_p_np, limit, batch_size, num_workers)
        total_1 += c1
        total_0 += c0
        total = total_1 + total_0

        p1 = total_1 / total
        p1_history.append(p1)

        print(f"After {i} batches ({total:,} drafts): "
              f"P(1) = {p1:.8f}, P(0) = {1 - p1:.8f}")
    end = time.perf_counter()

    # Final summary
    print("\nFinal results:")
    print(f"Total drafts: {total:,}")
    print(f"Returned 1: {total_1:,}")
    print(f"Returned 0: {total_0:,}")
    print(f"Final Probability of returning 1: {total_1 / total:.8f}")
    print(f"Final Probability of returning 0: {total_0 / total:.8f}")
    print(f"Elapsed time: {end - start:.4f} seconds")

    # Convergence trace (can be plotted later)
    print(p1_history)
