SHELL := /usr/bin/bash

TEX_DIR := tex
PAPER   := $(TEX_DIR)/true_string_collision
PAPER2  := $(TEX_DIR)/main
PAPER3  := $(TEX_DIR)/true_string_unordered
BIB     := $(TEX_DIR)/references.bib

PY := python3

.PHONY: all paper paper-main paper-unordered clean verify profiles plots dist

all: paper

paper: $(PAPER).pdf

paper-main: $(PAPER2).pdf

paper-unordered: $(PAPER3).pdf

$(PAPER).pdf: $(PAPER).tex $(BIB)
	cd $(TEX_DIR) && pdflatex true_string_collision.tex >/dev/null || true
	cd $(TEX_DIR) && bibtex true_string_collision || true
	cd $(TEX_DIR) && pdflatex true_string_collision.tex >/dev/null || true
	cd $(TEX_DIR) && pdflatex true_string_collision.tex >/dev/null || true
	@echo "Built $(PAPER).pdf"

$(PAPER2).pdf: $(PAPER2).tex
	cd $(TEX_DIR) && pdflatex main.tex >/dev/null || true
	cd $(TEX_DIR) && pdflatex main.tex >/dev/null || true
	@echo "Built $(PAPER2).pdf"

$(PAPER3).pdf: $(PAPER3).tex
	cd $(TEX_DIR) && pdflatex true_string_unordered.tex >/dev/null || true
	cd $(TEX_DIR) && pdflatex true_string_unordered.tex >/dev/null || true
	@echo "Built $(PAPER3).pdf"

clean:
	cd $(TEX_DIR) && rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot

verify:
	$(PY) python/test_parametric_odd_composites.py 200000
	$(PY) python/verify_multiplicity.py 200000
	$(PY) python/verify_unordered_multiplicity.py 100000

profiles:
	$(PY) python/true_string_collision.py --max-m 120 --max-n 120 --mods 3,4,8 --divisible-by 2,3,5,7,11

plots:
	$(PY) python/plot_residues.py --max-m 120 --max-n 120 --mods 3,4,8 --out-dir fig
	@echo "Plots saved under fig/"

dist: paper paper-main paper-unordered plots
	mkdir -p dist
	tar -czf dist/release.tar.gz \
		tex/true_string_collision.pdf \
		tex/main.pdf \
		tex/true_string_unordered.pdf \
		fig/residues_mod_3.png fig/residues_mod_4.png fig/residues_mod_8.png
	@echo "Created dist/release.tar.gz"