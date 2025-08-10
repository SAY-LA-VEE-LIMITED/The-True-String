#!/usr/bin/env python3
import sys
import math
from typing import List

# Allow importing top-level helpers
sys.path.append('/workspace')
from spectral_t_utils import T_via_sieve, progression_marking_T, T_from_formula, primes_upto

try:
    import sympy as sp
    HAVE_SYMPY = True
except Exception:
    HAVE_SYMPY = False


def naive_is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.isqrt(n))
    for d in range(3, r + 1, 2):
        if n % d == 0:
            return False
    return True


def verify_equivalence(N: int, p_max: int | None = None) -> None:
    print(f"Verifying T up to N={N} ...")
    T_sieve = T_via_sieve(N)
    T_prog = progression_marking_T(N, p_max)

    # Equivalence between sieve and progression methods
    mismatches = [(i, T_sieve[i], T_prog[i]) for i in range(N + 1) if T_sieve[i] != T_prog[i]]
    if mismatches:
        print(f"Mismatch between sieve and progression at {len(mismatches)} indices. Example: {mismatches[:5]}")
    else:
        print("Sieve and progression methods agree for all indices.")

    # Spot-check against primality oracle for odd values
    sample_points = list(range(0, min(N, 2000)))  # small sample from head
    sample_points += [N//2 + i for i in range(-100, 100) if 0 <= N//2 + i <= N]
    sample_points += [N - i for i in range(0, min(1000, N + 1))]
    sample_points = sorted(set(sample_points))

    failures = []
    for n in sample_points:
        odd = 2 * n + 1
        t = T_sieve[n]
        if HAVE_SYMPY:
            oracle = 1 if sp.isprime(odd) else 0
        else:
            oracle = 1 if naive_is_prime(odd) else 0
        if t != oracle:
            failures.append((n, odd, t, oracle))
            if len(failures) >= 10:
                break
    if failures:
        print("Disagreement with primality oracle at examples:")
        for e in failures:
            print("  n=%d (odd=%d): T=%d, oracle=%d" % e)
    else:
        print("All sampled indices agree with the primality oracle.")

    # Single-index formula tests
    primes_list = primes_upto(2 * N + 1)
    single_mismatches = []
    for n in sample_points:
        val = T_from_formula(n, primes_list)
        if val != T_sieve[n]:
            single_mismatches.append((n, val, T_sieve[n]))
            if len(single_mismatches) >= 10:
                break
    if single_mismatches:
        print("T_from_formula disagrees at examples:")
        for e in single_mismatches:
            print(f"  n={e[0]}: formula={e[1]}, sieve={e[2]}")
    else:
        print("Single-index formula agrees on sampled indices.")


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    p_max = None
    if len(sys.argv) > 2:
        p_max = int(sys.argv[2])
    verify_equivalence(N, p_max)