#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Dependências locais compatíveis com o cache bibliográfico incluído.
if [[ -d dependencias_tex/biblatex ]]; then
 export TEXINPUTS="$PWD/dependencias_tex/biblatex//:$PWD/dependencias_tex/logreq//:${TEXINPUTS:-}"
fi
if command -v biber >/dev/null 2>&1; then
 pdflatex -interaction=nonstopmode -halt-on-error main.tex
 biber main
else
 bib_atual=$(sha256sum zotero.bib | cut -d ' ' -f1)
 bib_cache=$(cat bibliografia_cache/zotero.sha256)
 if [[ "$bib_atual" != "$bib_cache" ]]; then
  echo 'Bibliografia alterada: instale Biber 2.19 para regenerar as referências.' >&2
  exit 1
 fi
 cp bibliografia_cache/main.bbl main.bbl
fi
for rodada in 1 2 3; do
 pdflatex -interaction=nonstopmode -halt-on-error main.tex
done
python3 - <<'PY'
from pathlib import Path
import shutil
nome='PROSPECÇÃO IN SILICO DE SUBSTÂNCIAS POLIMÉRICAS EXTRACELULARES (SPE) DA MICROALGA Tetraselmis chuii COMO INIBIDORES DE ENZIMAS CUTÂNEAS ASSOCIADAS AO ENVELHECIMENTO.pdf'
shutil.copy2('main.pdf',nome)
shutil.copy2('main.pdf','Trabalho_TCC2_atualizado.pdf')
PY
