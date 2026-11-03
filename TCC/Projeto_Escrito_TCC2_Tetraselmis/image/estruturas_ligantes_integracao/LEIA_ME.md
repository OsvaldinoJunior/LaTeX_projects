# Estruturas 2D do inventário atual

Os quatro painéis vetoriais mostram os 34 registros utilizados na triagem (17 comerciais/de referência e 17 do conjunto de prospecção). Os desenhos foram gerados dos campos `REMARK SMILES` preservados nos PDBQT de 1H1B das execuções com coordenadas corrigidas. O SMILES correspondente de 2PE4 foi conferido para cada registro.

A validação exigiu sanitização pelo RDKit, cobertura completa de `REMARK SMILES IDX` e correspondência de elemento químico para cada átomo pesado do primeiro modelo PDBQT. Os registros KDO e alpha-Kdo possuem o mesmo SMILES estereoquímico; foram mantidos como dois registros do inventário e identificados com asterisco, sem alegar duas estruturas distintas.

Os desenhos representam conectividade e estereoquímica registradas no preparo. Não representam a pose de docking, suas cargas parciais ou o estado de protonação em solução. A conferência não é uma determinação independente da identidade experimental nem da origem dos compostos na microalga.

Arquivos de apoio:

- `manifesto_estruturas.json`: verificação detalhada, índices atômicos, fontes e hashes SHA-256.
- `mapeamento_smiles.csv`: correspondência entre nome, SMILES, fonte e posição nos painéis.
- Quatro arquivos `.svg`: fonte vetorial editável dos desenhos.
- Quatro arquivos `.pdf`: painéis utilizados no LaTeX, sem imagens rasterizadas.
- Quatro arquivos `_previa.png`: renderizações para conferência visual.

Para regenerar, executar da raiz do projeto:

```bash
python3 scripts/gerar_estruturas_integracao.py
```

A geração utiliza RDKit 2025.09.4 e PyMuPDF, sem consultar bancos externos ou modificar arquivos de simulação. A fonte de desenho é Tinos quando disponível no sistema; os nomes são incluídos como texto vetorial com acentos. A escala é ajustada por molécula; L2U ocupa duas colunas para facilitar a leitura.
