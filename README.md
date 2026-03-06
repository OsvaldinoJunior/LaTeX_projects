# LaTeX Projects

Este repositório contém projetos em LaTeX para criação de documentos acadêmicos.

## Estrutura

```
LaTeX_projects/
├── PFI/
│   ├── main.tex           # Arquivo principal
│   ├── config/            # Arquivos de configuração
│   │   ├── capa.tex
│   │   ├── elementos.tex
│   │   ├── espacamento.tex
│   │   ├── margens.tex
│   │   ├── pacotes.tex
│   │   ├── pagina.tex
│   │   ├── paginacao.tex
│   │   ├── sumario.tex
│   │   └── titulos.tex
│   ├── conteudo/          # Conteúdo do documento
│   │   ├── introducao.tex
│   │   ├── objetivos.tex
│   │   ├── material_metodos.tex
│   │   ├── resultados.tex
│   │   ├── revisao.tex
│   │   ├── conclusao.tex
│   │   └── referencias.tex
│   └── image/             # Imagens
│       └── furg.png
└── .gitignore
```

## Compilação

Para compilar o documento, execute:

```bash
cd PFI
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Ou utilize uma ferramenta como VS Code com extensão LaTeX Workshop.

