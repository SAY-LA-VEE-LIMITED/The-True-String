Copyright © 2025 Gabriel Neal Christensen and Noah Christensen
All rights reserved.

Permission is NOT granted to copy, modify, merge, publish, distribute, sublicense, or sell copies of this software or associated materials, in whole or in part, without express written permission from the authors.

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
./build/spectral_t
```

## Paper (F(m,n) collision-zero model)
```bash
make paper     # builds tex/true_string_collision.pdf (with BibTeX)
make plots     # saves figures to fig/
make profiles  # prints residue and divisibility profiles
make verify    # runs coverage test up to 200k
```

## Python quickstart
```bash
python3 python/true_string_collision.py --max-m 120 --max-n 120 --mods 3,4,8 --divisible-by 2,3,5,7,11
python3 python/test_parametric_odd_composites.py 200000
python3 python/plot_residues.py --max-m 120 --max-n 120 --mods 3,4,8 --out-dir fig
```

Copyright © 2025 Gabriel Neal Christensen and Noah Christensen
All rights reserved.

Authors:
- Gabriel Neal Christensen
- Noah Christensen

This repository contains original work including mathematical formulations, proofs, and algorithm implementations created by the above authors.
