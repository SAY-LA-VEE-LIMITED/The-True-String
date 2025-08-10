#!/usr/bin/env python3
import sys
import math
from typing import List

import numpy as np
from mpmath import mp, zetazero

# Allow importing top-level helpers
sys.path.append('/workspace')
from spectral_t_utils import T_via_sieve


def truncated_transform(T: List[int], xi: float) -> complex:
    # Compute S_N(xi) = sum_{n=1..N} T[n] * exp(-2 pi i (2n+1) xi)
    N = len(T) - 1
    if N <= 1:
        return 0
    n = np.arange(1, N + 1, dtype=np.float64)
    # phase = -2πi * (2n+1) * xi
    phase = -2.0 * math.pi * 1j * ((2.0 * n + 1.0) * xi)
    return np.sum(T[1:] * np.exp(phase))


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    print(f"Building T up to N={N} ...")
    T = T_via_sieve(N)

    mp.dps = 50
    zeros = [zetazero(k+1) for k in range(K)]  # returns 1/2 + i*gamma_k
    gammas = [mp.im(z) for z in zeros]
    xis = [float(g / (2.0 * math.pi)) for g in gammas]

    # Evaluate magnitudes at these xis and at random controls
    values = []
    for xi in xis:
        s = truncated_transform(T, xi)
        values.append((xi, abs(s)))
    controls = []
    rng = np.random.default_rng(42)
    for _ in range(K):
        xi = float(rng.uniform(0.0, 1.0))
        s = truncated_transform(T, xi)
        controls.append((xi, abs(s)))

    values.sort(key=lambda x: -x[1])
    controls.sort(key=lambda x: -x[1])

    print("Top magnitudes at xi = gamma_k / (2pi):")
    for xi, mag in values:
        print(f"  xi={xi:.12f}  |S_N|={mag:.6e}")

    print("\nTop magnitudes at random xi in [0,1):")
    for xi, mag in controls:
        print(f"  xi={xi:.12f}  |S_N|={mag:.6e}")


if __name__ == "__main__":
    main()