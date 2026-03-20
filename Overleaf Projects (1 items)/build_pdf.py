#!/usr/bin/env python3
# ================================================================
#  build_pdf.py
#  Compila todos os projetos LaTeX encontrados na pasta,
#  salva os PDFs e converte para Word (.docx)
#
#  Uso:
#    python3 build_pdf.py
#
#  Dependências:
#    sudo apt-get install texlive texlive-lang-portuguese \
#         texlive-fonts-extra texlive-latex-extra libreoffice
# ================================================================

import os
import shutil
import subprocess
import sys

# ── Configurações ────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR  = os.path.join(SCRIPT_DIR, "output")
COMPILAÇÕES = 2   # Rodar pdflatex 2x garante sumário e referências corretos

# ── Cores ANSI ───────────────────────────────────────────────────
GREEN  = "\033[0;32m"
RED    = "\033[0;31m"
YELLOW = "\033[1;33m"
RESET  = "\033[0m"

def log(msg):   print(f"{GREEN}[OK]{RESET} {msg}")
def warn(msg):  print(f"{YELLOW}[AVISO]{RESET} {msg}")
def error(msg): print(f"{RED}[ERRO]{RESET} {msg}")


def check_dependencies():
    """Verifica se pdflatex e pdf2docx estão disponíveis."""
    missing = []
    if not shutil.which("pdflatex"):
        missing.append("pdflatex  → sudo apt-get install texlive texlive-lang-portuguese texlive-fonts-extra texlive-latex-extra")
    try:
        import pdf2docx  # noqa
    except ImportError:
        missing.append("pdf2docx  → pip install pdf2docx")

    if missing:
        error("Dependências faltando:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)
    log("Dependências OK.")


def find_projects():
    """Encontra todos os main.tex excluindo .git."""
    projects = []
    for root, dirs, files in os.walk(SCRIPT_DIR):
        dirs[:] = [d for d in dirs if d != ".git"]
        if "main.tex" in files:
            projects.append(root)
    return projects


def compile_pdf(project_dir: str) -> str | None:
    """
    Compila main.tex em project_dir e retorna o caminho do PDF gerado,
    ou None em caso de falha.
    """
    log_file = os.path.join(project_dir, "build_pdf.log")

    with open(log_file, "w") as lf:
        for run in range(1, COMPILAÇÕES + 1):
            print(f"  → Compilação {run}/{COMPILAÇÕES}...")
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "main.tex"],
                cwd=project_dir,
                stdout=lf,
                stderr=subprocess.STDOUT,
            )
            if result.returncode != 0:
                error(f"Erro na compilação {run}. Veja: {log_file}")
                return None

    pdf_path = os.path.join(project_dir, "main.pdf")
    if not os.path.isfile(pdf_path):
        error(f"PDF não encontrado após compilação. Veja: {log_file}")
        return None

    return pdf_path


def save_pdf(pdf_src: str, project_name: str) -> str:
    """Copia o PDF gerado para output/ com o nome do projeto."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_dst = os.path.join(OUTPUT_DIR, f"{project_name}.pdf")
    shutil.copy2(pdf_src, pdf_dst)
    return pdf_dst


def convert_to_docx(pdf_path: str, project_name: str) -> bool:
    """
    Converte o PDF para Word (.docx) usando pdf2docx.
    Retorna True em caso de sucesso, False em caso de falha.
    """
    print("  → Convertendo para Word (.docx)...")
    try:
        from pdf2docx import Converter
        docx_path = os.path.join(OUTPUT_DIR, f"{project_name}.docx")
        print(f"  → Salvando em: {docx_path}")
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()
        if not os.path.isfile(docx_path):
            error("Arquivo .docx não encontrado após conversão.")
            return False
        return True
    except ImportError:
        error("pdf2docx não instalado. Rode: pip install pdf2docx")
        return False
    except Exception as e:
        error(f"Erro na conversão: {e}")
        return False


def main():
    print("=" * 50)
    print(" build_pdf.py — LaTeX → PDF → Word")
    print("=" * 50)

    check_dependencies()

    projects = find_projects()
    if not projects:
        error("Nenhum projeto com main.tex encontrado.")
        sys.exit(1)

    print(f"\n{len(projects)} projeto(s) encontrado(s).\n")
    pdf_ok, pdf_fail, docx_ok, docx_fail = [], [], [], []

    for project_dir in projects:
        project_name = os.path.basename(project_dir)
        print(f"\n{'='*50}")
        print(f" Projeto: {project_name}")
        print(f"{'='*50}")

        # ── 1. Compilar PDF ──────────────────────────────────────
        pdf_src = compile_pdf(project_dir)
        if not pdf_src:
            pdf_fail.append(project_name)
            continue

        pdf_dst = save_pdf(pdf_src, project_name)
        log(f"PDF salvo  → output/{project_name}.pdf")
        pdf_ok.append(project_name)

        # ── 2. Converter para Word ───────────────────────────────
        if convert_to_docx(pdf_dst, project_name):
            log(f"Word salvo → output/{project_name}.docx")
            docx_ok.append(project_name)
        else:
            docx_fail.append(project_name)

    # ── Resumo final ─────────────────────────────────────────────
    print(f"\n{'='*50}")
    print(f" Resumo")
    print(f"{'='*50}")
    print(f"  PDFs gerados  : {len(pdf_ok)}")
    print(f"  PDFs com erro : {len(pdf_fail)}")
    print(f"  DOCX gerados  : {len(docx_ok)}")
    print(f"  DOCX com erro : {len(docx_fail)}")
    if pdf_ok or docx_ok:
        log(f"Arquivos em: {os.path.relpath(OUTPUT_DIR, SCRIPT_DIR)}/")
    if pdf_fail:
        for f in pdf_fail:
            error(f"PDF falhou: {f}")
    if docx_fail:
        for f in docx_fail:
            warn(f"DOCX falhou: {f}")
    print()


if __name__ == "__main__":
    main()
