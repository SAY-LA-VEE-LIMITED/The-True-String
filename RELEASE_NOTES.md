# Release v0.1.0 — True String (F/g forms), Proofs, and Reproducibility

Highlights
- Rigorous theorems: factorization 2F/g+1, full coverage of odd composites, ordered and unordered multiplicity formulas
- Clean separation of proofs vs. empirical sections (residue profiles, plots)
- Reproducible Python scripts and C++ demo; Makefile targets; CI builds PDFs and uploads artifacts
- Dual licensing: code (MIT), docs/figures (CC BY-NC-SA 4.0)

Contents
- Papers: tex/true_string_collision.tex, tex/true_string_unordered.tex, tex/main.tex
- Python: verification scripts, residue/plot utilities
- C++: spectral_t demo
- CI: builds PDFs, uploads PDFs and dist bundle

Build
```bash
# C++ demo
cmake -B build && cmake --build build && ./build/spectral_t

# Paper builds and plots
make plots
make paper          # tex/true_string_collision.pdf
make paper-unordered  # tex/true_string_unordered.pdf
make paper-main       # tex/main.pdf

# Dist bundle (PDFs + figures)
make dist  # dist/release.tar.gz
```

Verification
```bash
pip3 install --break-system-packages -r python/requirements.txt
python3 python/test_parametric_odd_composites.py 200000
python3 python/verify_multiplicity.py 200000
python3 python/verify_unordered_multiplicity.py 100000
```

Notes
- RH-related content is empirical/observational only; no RH proof is claimed.
- Code license: MIT; Docs/figures: CC BY-NC-SA 4.0.