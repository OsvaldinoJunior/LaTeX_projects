# Etanol e benzeno — equilíbrio líquido-vapor

Apresentação Beamer: `main.tex`. Figuras e script `graficos.py` preservados do ZIP original.

## Gerar o PDF

Instale Git, Make e uma distribuição TeX Live com Beamer e fontes recomendadas em cada computador.
No Ubuntu: `sudo apt install git make texlive-latex-recommended texlive-fonts-recommended`.

Na pasta deste projeto:

```sh
make pdf
```

Resultado: `output/termodinamica_2_etanol_benzeno.pdf`. Arquivos temporários ficam em `build/`, fora do Git.

## Regenerar os gráficos (opcional)

As imagens já estão incluídas. Para recalcular:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
make graficos
```

As dependências Python ainda não têm versões fixadas. Para resultados consistentes entre máquinas, use as mesmas versões de Python, bibliotecas e TeX Live. O conteúdo técnico e os cálculos não foram auditados.

## Sincronização com o GitHub

Este trabalho integra o repositório único `OsvaldinoJunior/LaTeX_projects`, na pasta `termodinamica_2_etanol_benzeno/`.

Na raiz `Latex/`, use `./sincronizar.py --baixar` antes de trabalhar e `./sincronizar.py -m "Atualiza termodinâmica"` ao terminar. Veja o [guia principal](../README.md) para configurar outro computador. Não inicialize outro Git dentro desta pasta.
