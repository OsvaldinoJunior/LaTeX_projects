# Projetos LaTeX — OsvaldinoJunior

Um único repositório para editar e sincronizar todos os trabalhos entre computadores.
Remoto: https://github.com/OsvaldinoJunior/LaTeX_projects (público).

## Organização

| Pasta | Trabalho |
| --- | --- |
| `termodinamica_2_etanol_benzeno/` | Termodinâmica: apresentação de equilíbrio líquido-vapor etanol–benzeno |
| `Estagio_CIA_Relatorio/` | Relatório de estágio |
| `Processos_Fermentativos_Industriais/PFI_curva_padrao/` | Curva padrão |
| `Processos_Fermentativos_Industriais/PFI_isolamento_leveduras/` | Isolamento de leveduras |
| `TCC/PFC_Chlorella_HEFA/` | Projeto de conclusão |
| `TCC/Resumo_TCC/` | Resumo do TCC |
| `Tratamento_de_dados/` | Scripts e materiais de tratamento de dados |

Edite os arquivos nas respectivas pastas. Novos trabalhos podem ser criados em novas pastas desta raiz; não execute `git init` dentro deles.

## Rotina neste computador

```sh
cd ~/Documents/Projetos/Latex
# Ao começar, com a pasta sem alterações pendentes:
./sincronizar.py --baixar

# Edite seus trabalhos. Confira o que será enviado:
./sincronizar.py --simular

# Ao terminar:
./sincronizar.py -m "Descreve as alterações nos trabalhos"
```

O script encontra a raiz pelo próprio caminho, mesmo executado de outra pasta. Sem `-m`, usa data e hora na mensagem. Requer Python 3 e Git; a autenticação do GitHub deve estar configurada no terminal.

Os arquivos modificados são atualizados **no mesmo caminho do GitHub**. Arquivos novos são adicionados e exclusões locais também são registradas. Todos os trabalhos são enviados no mesmo commit quando alterados juntos. O `.gitignore` exclui arquivos temporários, PDFs compilados e configurações locais; os arquivos já rastreados continuam versionados.

A simulação é local e não consulta a nuvem. O envio consulta `origin/main` antes do commit e recusa prosseguir se houver alterações remotas ausentes localmente. Nunca força a substituição do histórico. Se outro computador enviar mudanças durante o push, o Git também pode recusá-lo; o commit permanece salvo localmente para resolver a divergência. Código de saída 1 indica falha.

Se houver alterações locais ao tentar baixar, primeiro envie ou guarde essas alterações. Havendo divergência de histórico, resolva com Git antes de repetir. Envie as mudanças antes de trocar de computador.

## Preparar outro computador

Instale Git, Python 3 e a mesma versão do TeX Live. Autentique sua conta no GitHub para poder enviar (por exemplo, `gh auth login` e `gh auth setup-git`).

```sh
mkdir -p ~/Documents/Projetos
cd ~/Documents/Projetos
git clone https://github.com/OsvaldinoJunior/LaTeX_projects.git Latex
cd Latex
git config user.name "OsvaldinoJunior"
git config user.email "osvaldinocsjunior@gmail.com"
./sincronizar.py --baixar
```

Se já existir uma pasta `Latex` com arquivos nesse computador, preserve-a e clone em outro diretório antes de reunir suas alterações. Use `git clone` na primeira vez; depois use o script para atualizar.

## Compilar termodinâmica

```sh
cd termodinamica_2_etanol_benzeno
make pdf
```

PDF: `termodinamica_2_etanol_benzeno/build/main.pdf`. Veja o [guia do projeto](termodinamica_2_etanol_benzeno/README.md) para gerar os gráficos. Os outros trabalhos mantêm seus scripts e configuração originais; a compilação deles não foi validada nesta organização.

## Arquivos locais

A pasta `.tools/` contém o GitHub CLI usado na autenticação do Git e deve ser mantida neste computador. Ela e os PDFs compilados não são enviados ao GitHub. O histórico dos projetos está no Git do repositório principal. Mantenha também um backup independente.
