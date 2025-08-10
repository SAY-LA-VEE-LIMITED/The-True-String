#!/usr/bin/env python3
import sys
import argparse
import os
from typing import Dict, List
import matplotlib.pyplot as plt

from true_string_collision import generate_counts, mod_distribution


def plot_mod_distribution(counts: Dict[int, int], modulus: int, out_path: str) -> None:
    buckets = mod_distribution(counts, modulus)
    xs = list(range(modulus))
    plt.figure(figsize=(8, 4))
    plt.bar(xs, buckets, color="#4C78A8")
    plt.title(f"Residue distribution mod {modulus}")
    plt.xlabel("Residue")
    plt.ylabel("Count (distinct outputs)")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def main():
    ap = argparse.ArgumentParser(description="Plot residue distributions for f(m,n)=4+3m+3n+2mn")
    ap.add_argument("--max-m", type=int, default=120)
    ap.add_argument("--max-n", type=int, default=120)
    ap.add_argument("--mods", type=str, default="3,4,8")
    ap.add_argument("--out-dir", type=str, default="fig")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    counts = generate_counts(args.max_m, args.max_n)

    try:
        mod_list = [int(s) for s in args.mods.split(',') if s.strip()]
    except Exception:
        mod_list = [3, 4, 8]

    for m in mod_list:
        out_path = os.path.join(args.out_dir, f"residues_mod_{m}.png")
        plot_mod_distribution(counts, m, out_path)
        print(f"Saved {out_path}")


if __name__ == "__main__":
    main()