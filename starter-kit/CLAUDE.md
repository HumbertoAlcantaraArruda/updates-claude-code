# Nome do Projeto

<!--
  Modelo de CLAUDE.md para um projeto Laravel + JavaScript.
  Regras de ouro:
  - Mantenha abaixo de ~200 linhas. Arquivo longo = regras ignoradas.
  - Para cada linha, pergunte: "se eu apagar isso, o Claude erra?" Se não, apague.
  - Comentários HTML como este NÃO entram no contexto do Claude (servem para humanos).
  - O que só importa às vezes vai para uma skill (.claude/skills/) ou regra com paths (.claude/rules/).
-->

## Stack
- Laravel 11 (PHP 8.3), MySQL, Redis
- Front: Vite + JavaScript
- Testes: Pest (PHPUnit por baixo)

## Comandos
- Testes: `php artisan test` — prefira rodar só o teste afetado: `php artisan test --filter=NomeDoTeste`
- Formatação PHP: `./vendor/bin/pint` (um hook já roda isso depois de cada edição)
- Front: `npm run dev` / `npm run build`
- IMPORTANT: nunca rode `php artisan migrate:fresh`, `db:wipe` ou qualquer comando destrutivo no banco sem me perguntar.

## Convenções
- Controllers finos; regra de negócio em `app/Services`
- Validação sempre em Form Requests (`app/Http/Requests`)
- Rotas de API versionadas em `/api/v1`
- Respostas JSON seguem o padrão de `app/Http/Resources`

## Fluxo de trabalho
- Antes de dizer que terminou: rode os testes afetados e mostre a saída.
- Mudança que toca mais de 3 arquivos: proponha um plano antes de editar.
- Commits pequenos, mensagem em português no imperativo ("adiciona", "corrige").
- Ao compactar o contexto, preserve a lista de arquivos alterados e os comandos de teste usados.

## Pegadinhas deste projeto
- <exemplo: filas usam Redis; em testes use `Queue::fake()`>
- <exemplo: o `.env.testing` usa um banco separado>

## Mais contexto (carregado junto)
<!-- Use @caminho para importar arquivos. Cuidado: importados também entram no contexto no início. -->
- Visão geral: @README.md
