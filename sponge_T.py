#!/usr/bin/env python3
# sponge_T.py
# Compatible with Python 3.11.2
# Implements T[n] indicator for odd primes using:
#   1) Direct formula test
#   2) Composite progression marking
#   3) Fast sieve method

from __future__ import annotations
import math
from typing import List


def primes_upto(limit: int) -> List[int]:
    """Return list of all primes <= limit."""
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start:limit + 1:step] = b"\x00" * (((limit - start) // step) + 1)
    return [i for i, is_p in enumerate(sieve) if is_p]


def T_from_formula(n: int, primes: List[int] | None = None) -> int:
    """
    Check if n corresponds to an odd prime (o_n = 2n+1) via your progression rule:
      If exists p >= 3 such that n = (3p - 1)/2 + p*m (m>=0) -> composite -> 0
      Else -> 1
    """
    if n < 1:
        return 0
    o_n = 2 * n + 1
    if o_n == 3:
        return 1
    if primes is None:
        primes = primes_upto(o_n)
    for p in primes:
        if p < 3:
            continue
        base = (3 * p - 1) // 2
        if base > n:
            break
        diff = n - base
        if diff >= 0 and diff % p == 0:
            return 0
    return 1


def progression_marking_T(N: int, p_max: int | None = None) -> List[int]:
    """
    Build T[0..N] via marking composite indices from the progression:
      n_p(m) = (3p - 1)//2 + p*m
    Requires odd primes p >= 3 up to p_max (default: 2*N+1 for completeness).
    """
    T = [1] * (N + 1)
    T[0] = 0
    if p_max is None:
        p_max = 2 * N + 1
    primes = primes_upto(p_max)
    for p in primes:
        if p < 3:
            continue
        base = (3 * p - 1) // 2
        if base > N:
            break
        n_idx = base
        while n_idx <= N:
            T[n_idx] = 0
            n_idx += p
    return T


def T_via_sieve(N: int) -> List[int]:
    """
    Exact T using odd-only sieve:
      T[n] = 1 iff o_n = 2n+1 is prime.
    """
    limit = 2 * N + 1
    if limit < 2:
        return [0] * (N + 1)
    size = (limit + 1) // 2
    is_prime_odd = [True] * size
    is_prime_odd[0] = False
    max_i = int(math.isqrt(limit)) // 2
    for i in range(1, max_i + 1):
        if is_prime_odd[i]:
            p = 2 * i + 1
            start = (p * p - 1) // 2
            for j in range(start, size, p):
                is_prime_odd[j] = False
    T = [0] * (N + 1)
    for n in range(0, N + 1):
        if is_prime_odd[n]:
            T[n] = 1
    return T


def show_T_sample(N: int, method: str = "sieve", p_max: int | None = None) -> None:
    if method == "sieve":
        T = T_via_sieve(N)
    elif method == "progression":
        T = progression_marking_T(N, p_max)
    else:
        raise ValueError("method must be 'sieve' or 'progression'")
    print(" n   o_n   T[n]")
    for n in range(min(N + 1, 40)):
        print(f"{n:2d}  {2*n+1:5d}   {T[n]}")


def main() -> None:
    N = 50
    print("Sample from sieve method:")
    show_T_sample(N, method="sieve")

    print("\nSample from progression marking (p_max=50):")
    show_T_sample(N, method="progression", p_max=50)

    print("\nSingle index test with formula:")
    for test_n in [1, 5, 10, 20]:
        print(f"n={test_n}, o_n={2*test_n+1}, T={T_from_formula(test_n)}")


if __name__ == "__main__":
    main()
