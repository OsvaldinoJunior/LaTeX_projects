#!/bin/bash
# ================================================================
#  build.sh
#  Compila todos os projetos LaTeX em PDF e converte para .docx
#
#  Uso:
#    chmod +x build.sh
#    ./build.sh
#
#  Dependências (instalar antes se necessário):
#    sudo apt-get install texlive texlive-lang-portuguese \
#         texlive-fonts-extra texlive-latex-extra pandoc libreoffice
#
#  Saída:
#    Cada projeto gera: output/<nome_do_projeto>.pdf
#                       output/<nome_do_projeto>.docx
# ================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/output"
mkdir -p "$OUTPUT_DIR"

# Cores para log
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()    { echo -e "${GREEN}[OK]${NC} $1"; }
warn()   { echo -e "${YELLOW}[AVISO]${NC} $1"; }
error()  { echo -e "${RED}[ERRO]${NC} $1"; }

# ── Verificar dependências ──────────────────────────────────────
echo "Verificando dependências..."
MISSING=()
command -v pdflatex  &>/dev/null || MISSING+=("pdflatex  → sudo apt-get install texlive texlive-lang-portuguese texlive-fonts-extra texlive-latex-extra")
command -v libreoffice &>/dev/null || MISSING+=("libreoffice → sudo apt-get install libreoffice")
command -v pandoc    &>/dev/null || MISSING+=("pandoc    → sudo apt-get install pandoc")

if [ ${#MISSING[@]} -gt 0 ]; then
    error "Dependências faltando:"
    for m in "${MISSING[@]}"; do echo "  - $m"; done
    exit 1
fi
log "Dependências OK"

# Encontra todos os projetos com main.tex
mapfile -d '' PROJECTS < <(find "$SCRIPT_DIR" -name "main.tex" -not -path "*/.git/*" -print0)

if [ ${#PROJECTS[@]} -eq 0 ]; then
    error "Nenhum projeto com main.tex encontrado."
    exit 1
fi

for MAIN_TEX in "${PROJECTS[@]}"; do
    PROJECT_DIR="$(dirname "$MAIN_TEX")"
    PROJECT_NAME="$(basename "$PROJECT_DIR")"

    echo ""
    echo "================================================="
    echo " Projeto: $PROJECT_NAME"
    echo "================================================="

    # ── 1. Compilar LaTeX → PDF (2x para referências/sumário) ──
    echo "→ Compilando PDF..."
    if (cd "$PROJECT_DIR" && \
        pdflatex -interaction=nonstopmode main.tex > build.log 2>&1 && \
        pdflatex -interaction=nonstopmode main.tex >> build.log 2>&1); then

        PDF_SRC="$PROJECT_DIR/main.pdf"
        PDF_DST="$OUTPUT_DIR/${PROJECT_NAME}.pdf"
        cp "$PDF_SRC" "$PDF_DST"
        log "PDF gerado → output/${PROJECT_NAME}.pdf"
    else
        error "Falha ao compilar $PROJECT_NAME. Veja $PROJECT_DIR/build.log"
        continue
    fi

    # ── 2. Converter PDF → DOCX via LibreOffice ──
    echo "→ Convertendo para Word (.docx)..."
    if libreoffice --headless --convert-to docx "$PDF_DST" \
        --outdir "$OUTPUT_DIR" > /dev/null 2>&1; then
        log "Word gerado  → output/${PROJECT_NAME}.docx"
    else
        warn "LibreOffice falhou. Tentando com pandoc..."
        if pandoc "$PDF_DST" -o "$OUTPUT_DIR/${PROJECT_NAME}.docx" 2>/dev/null; then
            log "Word gerado via pandoc → output/${PROJECT_NAME}.docx"
        else
            error "Não foi possível converter $PROJECT_NAME para .docx"
        fi
    fi
done

echo ""
echo "================================================="
echo " Concluído! Arquivos em: $SCRIPT_DIR/output/"
echo "================================================="
