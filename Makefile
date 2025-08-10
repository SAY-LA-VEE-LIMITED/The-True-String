SHELL := /usr/bin/bash

TEX_DIR := tex
PAPER   := $(TEX_DIR)/true_string_collision
BIB     := $(TEX_DIR)/references.bib

PY := python3

.PHONY: all paper clean verify profiles plots

all: paper

paper: $(PAPER).pdf

$(PAPER).pdf: $(PAPER).tex $(BIB)
	cd $(TEX_DIR) && pdflatex true_string_collision.tex >/dev/null || true
	cd $(TEX_DIR) && bibtex true_string_collision || true
	cd $(TEX_DIR) && pdflatex true_string_collision.tex >/dev/null || true
	cd $(TEX_DIR) && pdflatex true_string_collision.tex >/dev/null || true
	@echo "Built $(PAPER).pdf"

clean:
	cd $(TEX_DIR) && rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot

verify:
	$(PY) python/test_parametric_odd_composites.py 200000

profiles:
	$(PY) python/true_string_collision.py --max-m 120 --max-n 120 --mods 3,4,8 --divisible-by 2,3,5,7,11

plots:
	$(PY) python/plot_residues.py --max-m 120 --max-n 120 --mods 3,4,8 --out-dir fig
	@echo "Plots saved under fig/"