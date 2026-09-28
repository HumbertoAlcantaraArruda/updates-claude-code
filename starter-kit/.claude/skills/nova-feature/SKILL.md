---
name: nova-feature
description: Implementa uma feature seguindo explorar, planejar, implementar e verificar. Use quando o usuário pedir uma funcionalidade nova que toca vários arquivos.
disable-model-invocation: true
argument-hint: "[descrição da feature]"
---

# Nova feature: $ARGUMENTS

Siga as fases na ordem. Não pule a verificação.

## 1. Explorar (sem editar nada)
- Encontre código parecido que já existe e siga o mesmo padrão.
- Liste os arquivos que provavelmente mudam.
- Se a exploração for grande, use um subagente para não encher o contexto.

## 2. Planejar
- Escreva um plano curto: arquivos, rotas, migrations, testes.
- Diga o que fica FORA do escopo.
- Pare e peça minha aprovação antes de editar.

## 3. Implementar
- Comece pelo teste que prova a feature (ele deve falhar primeiro).
- Implemente até o teste passar.

## 4. Verificar e mostrar evidência
- Rode `php artisan test` nos arquivos afetados e mostre a saída.
- Rode `git diff --stat` e resuma o que mudou em 3 linhas.
- Liste riscos ou pontas soltas, se houver.
