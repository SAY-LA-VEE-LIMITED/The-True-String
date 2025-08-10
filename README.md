# The-True-String
WE Solved Prime Numbers
# spectral-t

C++17 implementation of T(n) sequence for odd primes oₙ = 2n+1.

Features:
- Exact odd-only sieve (`T_via_sieve`)
- Progression-based marking method (`progression_marking_T`)
- Direct per-index formula test (`T_from_formula`)
- Fully cross-platform with CMake
- Automated build & test with GitHub Actions

## Build
```bash
cmake -B build
cmake --build build
./build/spectral_t_demo
