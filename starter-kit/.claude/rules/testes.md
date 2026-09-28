---
paths:
  - "tests/**/*.php"
---

# Regras para testes

<!-- Esta regra só entra no contexto quando o Claude lê arquivos em tests/. -->

- Use Pest com `it('...')`; um comportamento por teste.
- Banco: use `RefreshDatabase` e factories; nada de inserts manuais.
- Não use mocks para o que dá para testar de verdade com o banco de testes.
- Rode só o arquivo afetado: `php artisan test tests/Feature/NomeTest.php`.
