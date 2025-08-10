# spectral_t_utils.py
# Python 3.8+
# Provides functions to compute T[n] (n -> odd o_n = 2n+1)
# in several ways:
#  - T_from_formula(n): direct floor-formula test (scans primes)
#  - progression_marking_T(N, p_max=None): marks composites by progressions (up to p_max)
#  - T_via_sieve(N): fast exact T array using sieve (recommended)

import math
from typing import List, Tuple

# -----------------------
# Utility: generate primes up to limit (simple sieve)
# -----------------------
def primes_upto(limit: int) -> List[int]:
    """Return list of primes <= limit (simple sieve)."""
    if limit < 2:
        return []
    sieve = bytearray(b'\x01') * (limit + 1)
    sieve[0:2] = b'\x00\x00'
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            step = p
            start = p*p
            sieve[start:limit+1:step] = b'\x00' * (((limit - start)//step) + 1)
    return [i for i, is_p in enumerate(sieve) if is_p]

# -----------------------
# Direct floor-formula test (literal translation)
# -----------------------
def T_from_formula(n: int, primes: List[int] = None) -> int:
    """
    Evaluate the floor-expression test for index n:
      T[n] = 1  iff n is NOT in any composite progression n_p(m) for p>=3
    Here n corresponds to the odd integer o_n = 2n+1.
    This implements the idea:
      if exists p>=3 and m>=0 s.t. n = (3p-1)/2 + p*m  -> composite -> T[n]=0
      otherwise T[n]=1
    Returns 1 if o_n is prime *by this test* (i.e., wasn't hit), 0 otherwise.

    Note: Correctness requires scanning primes p <= o_n (or <= sqrt(o_n) with factor logic).
    This function is O(#primes) per call; use sparingly or vectorize.
    """
    if n < 1:
        return 0
    o = 2*n + 1
    if o == 3:
        return 1
    # generate primes if not provided
    if primes is None:
        primes = primes_upto(int(math.isqrt(o)) + 1)
    # We need to check all odd primes p >= 3 up to o (worst case).
    # But logically it's enough to test p <= o (or p <= o/3?), scanning small p will find factors.
    for p in primes:
        if p < 3:
            continue
        # compute (3p-1)/2
        base = (3*p - 1)//2
        if base > n:
            # for increasing p, base grows; once base>n no p will satisfy with nonnegative m
            break
        # check whether n - base is divisible by p and quotient >= 0
        diff = n - base
        if diff >= 0 and (diff % p) == 0:
            # n equals base + p*m for some integer m >= 0, so it's composite of form p*(2m+3)
            return 0
    # if none of the progressions hit it, treat as prime under this rule
    # (note: for strict correctness, check actual primality of o)
    # We'll conservatively return 1 here.
    return 1

# -----------------------
# Progression-marking to build T up to N
# -----------------------
def progression_marking_T(N: int, p_max: int = None) -> List[int]:
    """
    Build T[0..N] (inclusive) using composite-generating progressions:
      For each odd prime p >= 3 up to p_max (or up to limit derived from N),
      mark indices n_p(m) = (3p-1)//2 + p*m <= N as composite (T[n]=0).
    Returns T as list of ints (0/1) indexed by n (0..N).
    NOTE: T[0] corresponds to o_0 = 1 (non-prime) — conventionally T[0]=0.
    Parameters:
      N    : maximum n index to produce (so odd numbers up to 2N+1)
      p_max: upper bound on prime p to use. If None, choose p_max = 2*N+1 (full)
    Complexity:
      If p_max ~ sqrt(2N) you mark many composites with fewer p; if p_max ~ N you do a heavier O(N^2) job.
    """
    # initialize as "unmarked" (assume prime) then mark composites
    T = [1] * (N + 1)
    T[0] = 0  # o_0 = 1 is not prime
    if p_max is None:
        # safe default: primes up to N (or sqrt limit). We'll use p_max = 2*N+1 (full)
        p_max = 2*N + 1
    # generate odd primes up to p_max
    primes = primes_upto(p_max)
    for p in primes:
        if p < 3:
            continue
        base = (3*p - 1) // 2
        if base > N:
            # for larger p base exceeds N, further p's will be even larger -> stop early
            break
        # mark n = base + p*m
        n = base
        while n <= N:
            T[n] = 0
            n += p
    return T

# -----------------------
# Fast exact T via odd-only sieve (recommended)
# -----------------------
def T_via_sieve(N: int) -> List[int]:
    """
    Compute exact T[0..N] where T[n] = 1 iff o_n = 2n+1 is prime.
    We do an odd-only sieve up to 2N+1.
    Complexity: ~O(N log log N) work and O(N) memory.
    """
    limit = 2*N + 1
    if limit < 2:
        return [0]*(N+1)
    # boolean array for odd numbers: index i corresponds to 2*i+1
    size = (limit + 1) // 2
    is_prime_odd = [True] * size
    is_prime_odd[0] = False  # 1 not prime
    max_i = int(math.isqrt(limit))//2
    for i in range(1, max_i + 1):
        if is_prime_odd[i]:
            p = 2*i + 1
            start = (p*p - 1)//2
            for j in range(start, size, p):
                is_prime_odd[j] = False
    # Build T list aligning index n to 2n+1 (n range 0..N)
    T = [0]*(N+1)
    for n in range(0, N+1):
        idx = n  # since 2n+1 index in odd array is index n
        if idx < size and is_prime_odd[idx]:
            T[n] = 1
        else:
            T[n] = 0
    # ensure T[0]=0, T[1]=1 for o_1=3 etc.
    return T

# -----------------------
# Convenience: print small table
# -----------------------
def show_T_sample(N: int, method: str = 'sieve', p_max: int = None) -> None:
    if method == 'sieve':
        T = T_via_sieve(N)
    elif method == 'progression':
        T = progression_marking_T(N, p_max)
    else:
        raise ValueError("method must be 'sieve' or 'progression'")
    print("n  o_n  T[n]")
    for n in range(0, min(N+1, 40)):
        print(f"{n:2d}  {2*n+1:5d}   {T[n]}")
