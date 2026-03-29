#!/usr/bin/env python3
# Uso: python3 scripts/build_pdf.py
# Dependências: sudo apt-get install texlive texlive-lang-portuguese texlive-fonts-extra texlive-latex-extra

import os
import subprocess
import sys

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT  = os.path.join(ROOT, "output")
SCRIPTS = os.path.dirname(os.path.abspath(__file__))

if subprocess.run(["which", "pdflatex"], capture_output=True).returncode != 0:
    print("Erro: pdflatex não encontrado.")
    sys.exit(1)

os.makedirs(OUTPUT, exist_ok=True)

print("Compilando...")
log_path = os.path.join(SCRIPTS, "build.log")
with open(log_path, "w") as log:
    for _ in range(2):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", f"-output-directory={OUTPUT}", "main.tex"],
            cwd=ROOT, stdout=log, stderr=subprocess.STDOUT
        )
        if result.returncode != 0:
            print("Erro na compilação. Verifique scripts/build.log")
            sys.exit(1)

for ext in ("aux", "toc", "out", "log"):
    aux = os.path.join(OUTPUT, f"main.{ext}")
    if os.path.exists(aux):
        os.remove(aux)

PROJECT = os.path.basename(ROOT)
os.rename(os.path.join(OUTPUT, "main.pdf"), os.path.join(OUTPUT, f"{PROJECT}.pdf"))

print(f"Concluído: output/{PROJECT}.pdf")
