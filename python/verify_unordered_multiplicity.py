#!/usr/bin/env python3
import sys
import math
from typing import List, Tuple

from true_string_collision import f


def odd_divisor_count(c: int) -> int:
    # c odd
    count = 1
    n = c
    p = 3
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


def unordered_count_for_c(c: int, bound: int) -> int:
    # count unordered {m,n} with 2*f(m,n)+1 == c, m<=n<=bound
    target = (c - 1) // 2
    cnt = 0
    for m in range(0, bound + 1):
        for n in range(m, bound + 1):
            if 2 * f(m, n) + 1 == c:
                cnt += 1
    return cnt


def main():
    MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    samples: List[int] = []
    for k in range(9, MAX + 1, 2):
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
        dodd = odd_divisor_count(c)
        expected = (dodd - 2 + 1) // 2  # ceil((dodd-2)/2)
        # bound from factor sizes: u=2m+3 <= c => m <= (c-3)/2; keep modest
        bound = min(2000, (c - 3) // 2)
        got = unordered_count_for_c(c, bound)
        if got != expected:
            mismatches.append((c, got, expected))
            if len(mismatches) >= 10:
                break
    if mismatches:
        print("Mismatches (c, got, expected):")
        for t in mismatches:
            print(t)
    else:
        print("All sampled odd composites matched unordered preimage count ceil((d_odd(c)-2)/2).")


if __name__ == "__main__":
    main()