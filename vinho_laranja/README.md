# Vinho laranja — apresentação independente

Apresentação introdutória com enfoque em produção, composição e perfil sensorial, para público acadêmico. Planejada para **9 min 20 s**, dentro da faixa de 5 a 10 minutos, com 10 slides (incluindo capa e referências). O tempo real depende do ensaio e do ritmo de fala.

## Estrutura da fala

- **Introdução (slides 1–2):** raízes na tradição georgiana e vestígios de vinho de cerca de 6000–5800 a.C. (aproximadamente 8 mil anos), distinguindo essa datação da origem exata do estilo laranja.
- **Desenvolvimento (slides 3–8):** comparação com branco e tinto convencionais, método e tempos no qvevri, produção desde a colheita e seleção, partes da uva, perfil sensorial e controle de qualidade.
- **Conclusão (slide 9):** como contato com cascas, fermentação, maturação e proteção mudam cor, aromas, textura e estabilidade.
- **Referências (slide 10):** fontes e materiais de aula.

O slide 3 compara uva, contato com cascas, cor usual e taninos. Todas as células da tabela são centralizadas na horizontal e na vertical. Ela apresenta padrões de elaboração, com ressalva de que há exceções e variações de estilo.

O slide 4 descreve um exemplo tradicional de Kakheti: alcoólica de cerca de 20–40 dias e contato total com sólidos de aproximadamente 5–6 meses, incluindo a alcoólica. O carregamento, a vedação e a trasfega são situados na sequência, sem inventar prazos fixos; maturação posterior e envase variam. As fontes e as distinções entre fermentação, maceração e maturação estão no roteiro. O slide 5 começa na colheita e seleção das uvas, e a conclusão relaciona escolhas de processo com o que muda no vinho.

## Arquivos

- `main.tex`: todos os textos, títulos e referências; procure por `SLIDE 1` até `SLIDE 10`.
- `config/estilo.tex`: cores, fontes e recorte das imagens no layout.
- `roteiro.md`: falas sugeridas, transições, tempo por slide e fontes.
- `assets/`: seis imagens fotorrealistas ilustrativas, geradas por IA, e um mapa cartográfico da Geórgia.
- `assets/mapa_georgia.png`: globo localizador e mapa do Cáucaso usados no slide 2.
- `assets/mapa_georgia_dados.json` e `assets/gerar_mapa_georgia.py`: dados e script para reproduzir o mapa.
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

## Mapa de localização da Geórgia

O slide 2 destaca o país no Cáucaso e mostra sua localização no globo. A base é o [Natural Earth](https://www.naturalearthdata.com/about/terms-of-use/), em domínio público: países a 1:110 milhões no globo e 1:50 milhões no detalhe regional. Os dados foram obtidos do [repositório dos mantenedores](https://github.com/nvkelso/natural-earth-vector/tree/master/geojson) em 29/10/2026; o extrato local mantém os polígonos mundiais e recorta o detalhe regional. A localização foi conferida em [Enterprise Georgia](https://www.enterprisegeorgia.gov.ge/en/about-georgia) e [Georgia Travel](https://georgia.travel/why-georgia-geography). O mapa é cartográfico, distinto das fotos ilustrativas por IA.

O PDF compila diretamente com a imagem existente. Para redesenhar o mapa, use Python com NumPy e Matplotlib:

```sh
python assets/gerar_mapa_georgia.py
make pdf
```
