#!/usr/bin/env python3
import sys
import argparse
import math
from typing import Dict, Tuple

try:
    import sympy as sp
    HAVE_SYMPY = True
except Exception:
    HAVE_SYMPY = False


def f(m: int, n: int) -> int:
    return 4 + 3*m + 3*n + 2*m*n


def is_prime(n: int) -> bool:
    if HAVE_SYMPY:
        return bool(sp.isprime(n))
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.isqrt(n))
    for d in range(3, r+1, 2):
        if n % d == 0:
            return False
    return True


def generate_counts(max_m: int, max_n: int) -> Dict[int, int]:
    counts: Dict[int, int] = {}
    for m in range(0, max_m + 1):
        for n in range(0, max_n + 1):
            x = f(m, n)
            counts[x] = counts.get(x, 0) + 1
    return counts


def summarize(counts: Dict[int, int]) -> Tuple[int, int, int, int]:
    total = len(counts)
    collisions = sum(1 for v in counts.values() if v >= 2)
    unique_primes = 0
    unique_nonprimes = 0
    for x, c in counts.items():
        if c == 1:
            if is_prime(x):
                unique_primes += 1
            else:
                unique_nonprimes += 1
    return total, collisions, unique_primes, unique_nonprimes


def mod3_distribution(counts: Dict[int, int]) -> Tuple[int, int, int]:
    # among distinct outputs (keys of counts)
    r0 = r1 = r2 = 0
    for x in counts.keys():
        r = x % 3
        if r == 0:
            r0 += 1
        elif r == 1:
            r1 += 1
        else:
            r2 += 1
    return r0, r1, r2


def main():
    ap = argparse.ArgumentParser(description="Generate collision-zero True String counts for f(m,n)=4+3m+3n+2mn")
    ap.add_argument("--max-m", type=int, default=200, help="Maximum m")
    ap.add_argument("--max-n", type=int, default=200, help="Maximum n")
    ap.add_argument("--list-first", type=int, default=0, help="List first K sorted entries with (value, count)")
    args = ap.parse_args()

    counts = generate_counts(args.max_m, args.max_n)
    total, collisions, unique_primes, unique_nonprimes = summarize(counts)

    print(f"f(m,n)=4+3m+3n+2mn over m in [0,{args.max_m}], n in [0,{args.max_n}]")
    print(f"Distinct values             : {total}")
    print(f"Collision values (count>=2) : {collisions}")
    print(f"Unique primes               : {unique_primes}")
    print(f"Unique non-primes           : {unique_nonprimes}")

    r0, r1, r2 = mod3_distribution(counts)
    print(f"Modulo 3 distribution among distinct outputs: r0={r0}, r1={r1}, r2={r2}")

    if args.list_first > 0:
        items = sorted(counts.items())[:args.list_first]
        print("First entries (x: count):")
        for x, c in items:
            print(f"  {x}: {c}")


if __name__ == "__main__":
    main()