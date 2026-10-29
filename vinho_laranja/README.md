# Vinho laranja — apresentação independente

Apresentação introdutória com enfoque em produção, composição e perfil sensorial, para público acadêmico. Planejada para **8 min 30 s**, dentro da faixa de 5 a 10 minutos, com 10 slides (incluindo capa e referências). O tempo real depende do ensaio e do ritmo de fala.

## Estrutura da fala

- **Introdução (slides 1–2):** definição, objetivo e caminho da apresentação.
- **Desenvolvimento (slides 3–8):** comparação com branco e tinto convencionais, história, produção, partes da uva, perfil sensorial e controle de qualidade.
- **Conclusão (slide 9):** síntese e resposta ao objetivo inicial.
- **Referências (slide 10):** fontes e materiais de aula.

O slide 3 compara uva, contato com cascas, cor usual e taninos. A tabela apresenta padrões de elaboração, com ressalva de que há exceções e variações de estilo.

## Arquivos

- `main.tex`: todos os textos, títulos e referências; procure por `SLIDE 1` até `SLIDE 10`.
- `config/estilo.tex`: cores, fontes e recorte das imagens no layout.
- `roteiro.md`: falas sugeridas, transições, tempo por slide e fontes.
- `assets/`: seis imagens fotorrealistas ilustrativas, geradas por IA.
- `assets/prompts.json`: prompts completos e identificação do modo de geração.
- `Makefile`: comando de compilação.
- `output/vinho_laranja.pdf`: PDF final, atualizado no mesmo caminho.

No início de `main.tex`, edite `\Autor` para alterar o apresentador. Não foram atribuídos disciplina, instituição ou integrantes do projeto de termodinâmica a este novo trabalho.

## Compilar

Requer Make e TeX Live com Beamer, TikZ, Latin Modern e anyfontsize.

```sh
cd ~/Documents/Projetos/Latex/vinho_laranja
make pdf
```

Os temporários ficam em `build/` e são ignorados pelo Git. O PDF final só é substituído quando as duas passagens da compilação terminam com sucesso. A pedido do usuário, `output/vinho_laranja.pdf` é versionado junto com os fontes e as imagens; a exceção está no `.gitignore` deste projeto.

Este projeto não depende de nenhum arquivo de `termodinamica_2_etanol_benzeno/`; a apresentação anterior permanece separada. Usa o mesmo repositório Git da pasta `Latex`, sem criar um Git dentro deste projeto.

## Recorte e rigor

O tema é o vinho de uvas brancas fermentado com maceração, não vinho de fruta laranja. A apresentação distingue o uso amplo do nome comercial da categoria específica da OIV-ECO 647-2020, que exige pelo menos um mês de maceração. O fluxograma é esquemático. As imagens fotorrealistas foram geradas por IA usando a ferramenta image_gen; não documentam vinícolas, produtos, pessoas ou resultados experimentais reais. A apresentação identifica essa origem no rodapé. Os prompts completos estão em `assets/prompts.json`.

As referências verificadas estão no slide final e no roteiro. O conteúdo também usa as aulas 6–8 sobre vinho tinto e a aula 10 sobre vinho branco; a aula 9 é identificada como conteúdo de cerveja e não foi usada como fonte de etapas de vinificação. Data de consulta: 29/10/2026.

## Cópia no GitHub

- [Pasta completa](https://github.com/OsvaldinoJunior/LaTeX_projects/tree/main/vinho_laranja)
- [PDF final](https://github.com/OsvaldinoJunior/LaTeX_projects/blob/main/vinho_laranja/output/vinho_laranja.pdf)

Depois de editar e recompilar, use o script `sincronizar.py` na raiz `Latex/` para enviar também a nova versão do PDF.
