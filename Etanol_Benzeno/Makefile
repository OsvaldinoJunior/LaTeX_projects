.PHONY: pdf graficos
pdf:
	mkdir -p build
	TEXMFVAR="$(CURDIR)/build/texmf-var" pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
	TEXMFVAR="$(CURDIR)/build/texmf-var" pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build main.tex

graficos:
	MPLBACKEND=Agg python3 graficos.py
