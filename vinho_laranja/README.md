# Vinho laranja — apresentação independente

Apresentação introdutória com enfoque em produção, composição e perfil sensorial, para público acadêmico. Planejada para **7 min 30 s**, dentro da faixa de 5 a 10 minutos, com 9 slides (incluindo capa e referências). O tempo real depende do ensaio e do ritmo de fala.

## Arquivos

- `main.tex`: todos os textos, títulos e referências; procure por `SLIDE 1` até `SLIDE 9`.
- `config/estilo.tex`: cores, fontes e ilustrações vetoriais próprias desta apresentação.
- `roteiro.md`: falas sugeridas, transições, tempo por slide e fontes.
- `Makefile`: comando de compilação.
- `output/vinho_laranja.pdf`: PDF final, atualizado no mesmo caminho.

No início de `main.tex`, edite `\Autor` para alterar o apresentador. Não foram atribuídos disciplina, instituição ou integrantes do projeto de termodinâmica a este novo trabalho.

## Compilar

Requer Make e TeX Live com Beamer, TikZ, Latin Modern e anyfontsize.

```sh
cd ~/Documents/Projetos/Latex/vinho_laranja
make pdf
```

Os temporários ficam em `build/`. O PDF final só é substituído quando as duas passagens da compilação terminam com sucesso. PDFs e temporários continuam ignorados pelo Git.

Este projeto não depende de nenhum arquivo de `termodinamica_2_etanol_benzeno/`; a apresentação anterior permanece separada. Usa o mesmo repositório Git da pasta `Latex`, sem criar um Git dentro deste projeto.

## Recorte e rigor

O tema é o vinho de uvas brancas fermentado com maceração, não vinho de fruta laranja. A apresentação distingue o uso amplo do nome comercial da categoria específica da OIV-ECO 647-2020, que exige pelo menos um mês de maceração. Os diagramas são esquemáticos; não apresentam dados experimentais nem parâmetros de uma receita de produção.

As referências verificadas estão no slide final e no roteiro. Data de consulta: 29/10/2026.
