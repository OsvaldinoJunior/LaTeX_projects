PROJECT := $(notdir $(CURDIR))

.PHONY: pdf
pdf:
	mkdir -p build output
	TEXMFVAR="$(CURDIR)/build/texmf-var" pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
	TEXMFVAR="$(CURDIR)/build/texmf-var" pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
	mv -f build/main.pdf "output/$(PROJECT).pdf"
