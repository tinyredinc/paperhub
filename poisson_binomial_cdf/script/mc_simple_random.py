import random
import time

def compare_and_check(list_p, limit):
    list_rand = [random.randint(0, 10000) for _ in range(len(list_p))]
    tmp = [p for p, r in zip(list_p, list_rand) if p < r]
    return 1 if len(tmp) < limit else 0

# Your example array
list_p = [4667, 4400, 4000, 4000, 1304, 2128, 3103, 5217, 1111, 2333, 857, 857, 1400, 10000, 2500, 3333, 1250]

limit = 14
drafts = 1000000

count_1 = 0
count_0 = 0

# Start timer (elapsed wall-clock time)
start_time = time.perf_counter()

for _ in range(drafts):
    if compare_and_check(list_p, limit) == 1:
        count_1 += 1
    else:
        count_0 += 1

# End timer
end_time = time.perf_counter()

print(f"Out of {drafts} drafts:")
print(f"Returned 1: {count_1} times")
print(f"Returned 0: {count_0} times")
print(f"Probability of returning 1: {count_1 / drafts:.4f}")
print(f"Probability of returning 0: {count_0 / drafts:.4f}")
print(f"Elapsed time for {drafts} drafts: {end_time - start_time:.6f} seconds")
