#!/usr/bin/env python3
import sys
import math
from collections import defaultdict
from typing import Dict, List, Tuple

from true_string_collision import f


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


def odd_divisor_count(c: int) -> int:
    # c is odd
    count = 1
    n = c
    p = 3
    # factorization by trial division skipping even
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            count *= (e + 1)
        p += 2
    if n > 1:
        count *= 2
    return count


def enumerate_preimages(c: int, mmax: int, nmax: int) -> int:
    # naive enumeration of (m,n) to count preimages for small bounds
    cnt = 0
    target = (c - 1) // 2
    for m in range(0, mmax + 1):
        for n in range(0, nmax + 1):
            if 2 * f(m, n) + 1 == c:
                cnt += 1
    return cnt


def main():
    MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    # sample odd composites in a moderate range for naive enumeration limits
    samples: List[int] = []
    for k in range(9, MAX + 1, 2):
        # simple odd composite test
        if k % 3 == 0 and k != 3:
            samples.append(k)
        elif k % 5 == 0 and k != 5:
            samples.append(k)
        elif k % 7 == 0 and k != 7:
            samples.append(k)
        if len(samples) >= 200:
            break

    mismatches: List[Tuple[int, int, int]] = []
    for c in samples:
        # compute theoretical count
        dodd = odd_divisor_count(c)
        expected = dodd - 2
        # infer m,n bounds from factor sizes: u = 2m+3, v = 2n+3 ≤ c
        # so m,n ≤ (c-3)/2; for sampling we keep modest bounds to avoid heavy loops
        bound = min(2000, (c - 3) // 2)
        got = enumerate_preimages(c, bound, bound)
        if got != expected:
            mismatches.append((c, got, expected))
            if len(mismatches) >= 10:
                break
    if mismatches:
        print("Mismatches (c, got, expected):")
        for t in mismatches:
            print(t)
    else:
        print("All sampled odd composites matched preimage count d_odd(c)-2.")


if __name__ == "__main__":
    main()