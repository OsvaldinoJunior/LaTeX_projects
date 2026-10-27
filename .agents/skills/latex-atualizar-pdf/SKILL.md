---
name: latex-atualizar-pdf
description: Atualizar documentos deste repositório LaTeX e recompilar o PDF final no mesmo caminho, substituindo a versão anterior após validar a compilação. Use ao editar texto, formatação, referências, tabelas, cálculos ou figuras que afetem o documento.
---

# Atualizar LaTeX e o PDF existente

A preferência do usuário é manter uma única versão corrente de cada documento: os fontes LaTeX editados e o PDF final atualizado, com o nome e o caminho já usados pelo projeto.

- Edite os fontes do trabalho solicitado. Quando as alterações afetarem o documento, recompile antes de encerrar a tarefa; isso inclui figuras, tabelas, bibliografia e arquivos incluídos. Alterações apenas em guias ou configurações sem efeito no documento não exigem recompilar.
- O padrão de todos os trabalhos é `<pasta-do-projeto>/output/<nome-da-pasta-do-projeto>.pdf`. Use esse destino ao criar projetos; nas atualizações, substitua o PDF nesse mesmo caminho. Identifique o comando de compilação no projeto. Não crie variantes como `final_v2.pdf`, `atualizado.pdf` ou cópias com data, salvo pedido do usuário.
- Em `termodinamica_2_etanol_benzeno/`, execute `make pdf` nessa pasta. O resultado corrente é `output/termodinamica_2_etanol_benzeno.pdf`; `build/` guarda somente temporários.
- Nos trabalhos antigos, leia `scripts/build_pdf.py` ou `scripts/native.sh` antes de executar. O resultado final é `output/<nome-da-pasta-do-projeto>.pdf`. Não confunda PDFs de referência ou figuras com o PDF final.
- Compile a partir da raiz do trabalho, resolva referências e bibliografia com as passagens necessárias e confira o código de saída e o PDF gerado. Confira as páginas afetadas quando houver mudanças de apresentação visual.
- Substitua o PDF anterior somente por uma compilação bem-sucedida. Quando o comando escrever diretamente no destino, preserve temporariamente o PDF válido anterior fora dos arquivos versionados e restaure-o se a compilação falhar. Remova essa cópia temporária ao concluir. Também é possível compilar em área temporária e substituir o destino após validar, respeitando caminhos relativos e configurações do projeto.
- Se houver erro ou dependência ausente, tente corrigir dentro do escopo autorizado. Se não conseguir, preserve o último PDF válido e informe que ele ainda não reflete os fontes atuais. Não anuncie o PDF como atualizado sem validar a geração.
- Ao concluir, informe o caminho do PDF atualizado. Fontes e PDFs continuam sujeitos ao `.gitignore` existente: atualizar o PDF local não implica adicioná-lo ao GitHub. Não altere essa regra nem force o envio de PDFs sem solicitação.
- Esta skill não concede autorização adicional para publicar ou fazer push. Quando o envio estiver autorizado na tarefa, use o fluxo do repositório (`sincronizar.py`), mantendo os caminhos dos fontes e o histórico existente.
