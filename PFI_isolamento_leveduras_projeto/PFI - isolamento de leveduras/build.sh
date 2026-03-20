#!/bin/bash
# ================================================================
#  build.sh — Gera o PDF do relatório LaTeX
#  Uso: ./build.sh
# ================================================================

set -e

MAIN="main"
OUTPUT_DIR="output"

echo "Compilando (1ª passagem)..."
pdflatex -interaction=nonstopmode "$MAIN.tex" > /dev/null

echo "Compilando (2ª passagem — sumário e referências cruzadas)..."
pdflatex -interaction=nonstopmode "$MAIN.tex" > /dev/null

echo "Copiando para $OUTPUT_DIR/..."
mkdir -p "$OUTPUT_DIR"
cp "$MAIN.pdf" "$OUTPUT_DIR/$MAIN.pdf"

echo "Limpando arquivos auxiliares..."
rm -f "$MAIN.aux" "$MAIN.log" "$MAIN.toc" "$MAIN.out"

echo ""
echo "PDF gerado: $OUTPUT_DIR/$MAIN.pdf"
