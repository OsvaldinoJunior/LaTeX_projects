#!/bin/bash
# Uso: ./scripts/build.sh   (a partir da raiz do projeto)
set -e

SCRIPTS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPTS")"
OUTPUT="$ROOT/output"
mkdir -p "$OUTPUT"

LOG="$SCRIPTS/build.log"

echo "Compilando..."
for i in 1 2; do
    pdflatex -interaction=nonstopmode -output-directory="$OUTPUT" "$ROOT/main.tex" >> "$LOG" 2>&1
done

rm -f "$OUTPUT"/main.{aux,toc,out,log}

PROJECT="$(basename "$ROOT")"
mv "$OUTPUT/main.pdf" "$OUTPUT/$PROJECT.pdf"

echo "Concluído: output/$PROJECT.pdf"
