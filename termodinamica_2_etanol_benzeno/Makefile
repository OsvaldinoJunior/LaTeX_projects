PROJECT := $(notdir $(CURDIR))

.PHONY: pdf graficos
pdf:
	mkdir -p build
	TEXMFVAR="$(CURDIR)/build/texmf-var" pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
	TEXMFVAR="$(CURDIR)/build/texmf-var" pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
	mkdir -p output
	mv -f build/main.pdf "output/$(PROJECT).pdf"

graficos:
	MPLBACKEND=Agg python3 graficos.py
