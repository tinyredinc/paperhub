"""
Exact analytical probability for the Monte Carlo experiment (Poisson–binomial CDF)

Setup
-----
Given integers p_i and independent R_i ~ Uniform{0,...,10000}, define
X_i = 1{ p_i < R_i }. Then S = sum_i X_i is Poisson–binomial with success probs

    q_i = P(X_i = 1) = clip((10000 - p_i) / 10001, 0, 1).

Goal
----
Compute P(S < L) exactly, i.e. the CDF at L-1.

Method
------
Dynamic programming (O(n * L)):
    f[k] = probability that partial sum equals k.
    Initialize f[0] = 1.
    Update for each q_i:
        f[k] = f[k]*(1-q_i) + f[k-1]*q_i   (for k>0)
        f[0] = f[0]*(1-q_i)
Final result = sum_{k=0}^{L-1} f[k].
"""

import numpy as np


def probs_from_p(list_p):
    """Convert integer thresholds p_i to success probs q_i, clipped to [0,1]."""
    p = np.asarray(list_p, dtype=np.int64)
    q = (10000 - p) / 10001.0
    return np.clip(q, 0.0, 1.0)


def poisson_binomial_cdf_less_than(q, L):
    """Exact P(S < L) for S = sum Bernoulli(q_i), via O(n*L) DP."""
    q = np.asarray(q, dtype=np.float64)
    n = q.size
    if L <= 0:
        return 0.0
    if L > n:
        return 1.0

    f = np.zeros(L, dtype=np.float64)
    f[0] = 1.0
    for qi in q:
        kmax = min(L - 1, n)
        for k in range(kmax, 0, -1):
            f[k] = f[k] * (1.0 - qi) + f[k - 1] * qi
        f[0] *= (1.0 - qi)
    return float(f.sum())


if __name__ == "__main__":
    # Example input (same as your simulation)
    list_p = [
        4667, 4400, 4000, 4000, 1304, 2128,
        3103, 5217, 1111, 2333, 857, 857,
        1400, 10000, 2500, 3333, 1250
    ]
    limit = 14

    q = probs_from_p(list_p)
    prob = poisson_binomial_cdf_less_than(q, limit)

    print(f"n = {len(list_p)}, limit = {limit}")
    print(f"Exact P(S < {limit}) = {prob:.10f}")
