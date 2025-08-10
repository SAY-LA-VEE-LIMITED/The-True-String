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


def is_odd_composite(k: int, primes: List[int]) -> bool:
    if k < 9 or k % 2 == 0:
        return False
    # quick primality using precomputed primes
    for p in primes:
        if p * p > k:
            break
        if k % p == 0:
            return True
    # if no divisor found up to sqrt, it's prime
    return False


def covers_by_form(k: int) -> bool:
    # Check existence of m, n >= 0 with k = 4 + 3m + 3n + 2mn
    # For fixed m, solve for n: n = (k - 4 - 3m) / (2m + 3)
    # Need integer n >= 0
    m = 0
    while True:
        denom = 2 * m + 3
        num = k - 4 - 3 * m
        if denom <= 0:
            m += 1
            continue
        if num < 0:
            # for larger m, num decreases further; break
            break
        if num % denom == 0:
            n = num // denom
            if n >= 0:
                return True
        m += 1
        # stop when denom exceeds num+denom lower bound
        if denom > num + denom:
            break
        # simple guard to avoid infinite loops; bound m by sqrt scale
        if m > int(math.sqrt(k)) + 3:
            break
    return False


def main():
    MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    primes = primes_upto(int(MAX ** 0.5) + 1000)

    misses: List[int] = []
    count = 0
    for k in range(9, MAX + 1, 2):  # odd numbers
        if is_odd_composite(k, primes):
            count += 1
            if not covers_by_form(k):
                misses.append(k)
                if len(misses) <= 10:
                    print(f"MISS: k={k}")
    print(f"Checked odd composites up to {MAX}.")
    print(f"Total odd composites: {count}")
    print(f"Misses by form 4+3m+3n+2mn: {len(misses)}")
    if misses:
        print(f"First few misses: {misses[:10]}")


if __name__ == "__main__":
    main()