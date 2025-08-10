#!/usr/bin/env python3
import sys
import math
from typing import List, Tuple

# simple sieve for primes
def primes_upto(limit: int) -> List[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(limit ** 0.5) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start:limit + 1:step] = b"\x00" * (((limit - start) // step) + 1)
    return [i for i, is_p in enumerate(sieve) if is_p]


def least_prime_factor(k: int, primes: List[int]) -> int:
    for p in primes:
        if p * p > k:
            break
        if k % p == 0:
            return p
    return k


def is_odd_composite(k: int, primes: List[int]) -> bool:
    if k < 9 or k % 2 == 0:
        return False
    lp = least_prime_factor(k, primes)
    return lp != k


def F_from_uv(u: int, v: int) -> int:
    # Given odd factors u,v >= 3, compute m,n and F(m,n)
    a = (u - 1) // 2
    b = (v - 1) // 2
    m = a - 1
    n = b - 1
    return 4 + 3*m + 3*n + 2*m*n


def main():
    MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    primes = primes_upto(int(MAX ** 0.5) + 1000)

    misses: List[int] = []
    count = 0
    for k in range(9, MAX + 1, 2):  # odd numbers
        if is_odd_composite(k, primes):
            count += 1
            p = least_prime_factor(k, primes)
            u = p
            v = k // p
            # both u,v are odd >= 3 for odd composite k
            F = F_from_uv(u, v)
            if 2 * F + 1 != k:
                misses.append(k)
                if len(misses) <= 10:
                    print(f"MISS: k={k}, got 2F+1={2*F+1}")
    print(f"Checked odd composites up to {MAX}.")
    print(f"Total odd composites: {count}")
    print(f"Misses by 2F(m,n)+1 mapping: {len(misses)}")
    if misses:
        print(f"First few misses: {misses[:10]}")


if __name__ == "__main__":
    main()