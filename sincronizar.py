#!/usr/bin/env python3
"""Sincroniza todos os projetos deste repositório LaTeX com origin/main."""
import argparse
from datetime import datetime
import os
from pathlib import Path
import subprocess
import sys


def git(root, *args, check=True):
    proc = subprocess.run(
        ['git', '-C', str(root), *args], text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={**os.environ, 'GIT_TERMINAL_PROMPT': '0'}, timeout=120,
    )
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or 'Git falhou.')
    return proc


def preflight(root):
    actual = Path(git(root, 'rev-parse', '--show-toplevel').stdout.strip()).resolve()
    if actual != root:
        raise RuntimeError('Execute sobre a raiz do repositório, não sobre uma subpasta.')
    if git(root, 'symbolic-ref', '--quiet', '--short', 'HEAD').stdout.strip() != 'main':
        raise RuntimeError('Use a branch main para sincronizar os projetos.')
    gitdir = Path(git(root, 'rev-parse', '--absolute-git-dir').stdout.strip())
    for marker in ('MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'rebase-merge', 'rebase-apply', 'BISECT_LOG'):
        if (gitdir / marker).exists():
            raise RuntimeError('Conclua a operação Git pendente antes de sincronizar.')
    if git(root, 'ls-files', '-u').stdout:
        raise RuntimeError('Resolva os conflitos pendentes antes de sincronizar.')
    git(root, 'remote', 'get-url', 'origin')
    # Um repositório por diretório Latex; nenhum projeto deve virar submódulo.
    for current, dirs, files in os.walk(root):
        path = Path(current)
        if path != root and '.git' in dirs + files:
            raise RuntimeError(f'Repositório aninhado em {path.relative_to(root)}; reúna os arquivos na raiz antes de enviar.')
        dirs[:] = [d for d in dirs if d not in ('.git', '.tools', '.backups', '.venv', '__pycache__', 'build')]


def synchronize(root, message, download=False, dry_run=False):
    preflight(root)
    status = git(root, 'status', '--short').stdout
    print(status or 'Nenhuma alteração local.', end='' if status else '\n', flush=True)
    if dry_run:
        print('Simulação: ' + ('baixaria origin/main.' if download else 'criaria commit das alterações e enviaria para origin/main.') + ' Nenhum arquivo alterado; nuvem não consultada.')
        return
    if download:
        if status:
            raise RuntimeError('Há alterações locais. Envie-as ou guarde-as com git stash antes de baixar.')
        git(root, 'pull', '--ff-only', 'origin', 'main')
        print('Projetos atualizados a partir de origin/main.')
        return
    git(root, 'fetch', 'origin')
    remote = 'refs/remotes/origin/main'
    git(root, 'rev-parse', '--verify', remote)
    if git(root, 'merge-base', '--is-ancestor', remote, 'HEAD', check=False).returncode:
        raise RuntimeError('A nuvem contém alterações ausentes aqui. Baixe com ./sincronizar.py --baixar quando a pasta estiver limpa; se houver divergência, resolva-a com Git. Nenhum commit ou push foi feito.')
    if status:
        git(root, 'var', 'GIT_AUTHOR_IDENT')
        git(root, 'var', 'GIT_COMMITTER_IDENT')
        git(root, 'add', '--all')
        diff = git(root, 'diff', '--cached', '--quiet', check=False)
        if diff.returncode == 1:
            git(root, 'commit', '-m', message)
        elif diff.returncode:
            raise RuntimeError('Não foi possível verificar as alterações preparadas.')
    git(root, 'push', '--set-upstream', 'origin', 'HEAD:refs/heads/main')
    print('Todos os projetos enviados para origin/main.', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-m', '--mensagem', default='Atualiza projetos LaTeX — ' + datetime.now().astimezone().isoformat(timespec='seconds'))
    parser.add_argument('--diretorio', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--simular', action='store_true', help='Mostra alterações sem modificar arquivos nem acessar a rede.')
    parser.add_argument('--baixar', action='store_true', help='Baixa alterações da nuvem antes de começar a trabalhar; exige pasta limpa.')
    args = parser.parse_args()
    try:
        synchronize(args.diretorio.resolve(), args.mensagem, args.baixar, args.simular)
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        print(f'ERRO: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
