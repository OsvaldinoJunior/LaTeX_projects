#!/usr/bin/env python3
# Uso: python3 scripts/build_pdf.py
# Dependências: sudo apt-get install texlive texlive-lang-portuguese texlive-fonts-extra texlive-latex-extra

import os
import subprocess
import sys
import shutil

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT  = os.path.join(ROOT, "output")
SCRIPTS = os.path.dirname(os.path.abspath(__file__))

if subprocess.run(["which", "pdflatex"], capture_output=True).returncode != 0:
    print("Erro: pdflatex não encontrado.")
    sys.exit(1)

os.makedirs(OUTPUT, exist_ok=True)

# TEXINPUTS garante que \input{} e \includegraphics{} resolvam
# a partir do ROOT, mesmo com -output-directory apontando para output/
env = os.environ.copy()
env["TEXINPUTS"] = ROOT + "/:"

print("Compilando (2 passagens para sumário e referências cruzadas)...")
log_path = os.path.join(SCRIPTS, "build.log")
with open(log_path, "w") as log:
    for passagem in range(1, 3):
        print(f"  Passagem {passagem}/2...")
        result = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                f"-output-directory={OUTPUT}",
                "main.tex",
            ],
            cwd=ROOT,
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        if result.returncode != 0:
            print("Erro na compilação. Verifique scripts/build.log")
            sys.exit(1)

# Remove arquivos auxiliares do output/
for ext in ("aux", "toc", "out", "log"):
    aux = os.path.join(OUTPUT, f"main.{ext}")
    if os.path.exists(aux):
        os.remove(aux)

# Renomeia main.pdf para <nome-do-projeto>.pdf
PROJECT  = os.path.basename(ROOT)
src_pdf  = os.path.join(OUTPUT, "main.pdf")
dest_pdf = os.path.join(OUTPUT, f"{PROJECT}.pdf")
shutil.move(src_pdf, dest_pdf)

print(f"Concluído: output/{PROJECT}.pdf")
