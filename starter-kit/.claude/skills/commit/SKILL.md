---
name: commit
description: Revisa as mudanças não commitadas e cria um commit com mensagem descritiva em português.
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *) Bash(git diff *)
---

## Estado atual
- Status: !`git status --short`
- Diff resumido: !`git diff --stat`

## Instruções
1. Leia o diff completo com `git diff` e procure: código de debug esquecido (`dd(`, `dump(`, `console.log`), segredos, arquivos que não deveriam entrar.
2. Se achar algo suspeito, pare e me avise em vez de commitar.
3. Se estiver tudo certo, faça `git add` só dos arquivos relacionados à mudança.
4. Mensagem: primeira linha até 72 caracteres, imperativo em português ("adiciona", "corrige"), explicando o porquê em uma segunda linha se não for óbvio.
5. Não faça push.
