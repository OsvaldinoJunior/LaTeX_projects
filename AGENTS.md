# Instruções para IAs neste repositório

Ao alterar fontes LaTeX ou materiais que afetem um documento, leia e aplique [.agents/skills/latex-atualizar-pdf/SKILL.md](.agents/skills/latex-atualizar-pdf/SKILL.md).

Preferência permanente do usuário: atualizar os fontes e recompilar o PDF final **no mesmo nome e caminho**, substituindo a versão anterior após uma compilação válida. Não deixar somente o `.tex` atualizado nem criar PDFs com sufixos de versão, salvo solicitação explícita. Se a compilação falhar, preservar o último PDF válido e informar a pendência.

Padrão de saída: `<pasta-do-projeto>/output/<nome-da-pasta-do-projeto>.pdf`. `build/` é reservado a arquivos temporários.

Todos os trabalhos pertencem ao Git da raiz; não criar repositórios Git nas subpastas. Respeitar o `.gitignore` e as autorizações de envio da tarefa. PDFs compilados são locais e não são enviados automaticamente ao GitHub.
