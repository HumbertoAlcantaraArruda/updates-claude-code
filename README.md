# Boas práticas com Claude Code

Guia prático em português para configurar e usar o Claude Code: janela de contexto, fluxo de trabalho, CLAUDE.md, permissões, modelos, hooks, skills, subagentes, MCP, plugins, sessões e automação. Conferido na documentação oficial em setembro de 2026.

**Site:** https://humbertoalcantaraarruda.github.io/boas-praticas-claude-code/

## O que tem aqui

| Arquivo | Para quê |
| --- | --- |
| [`GUIA.md`](GUIA.md) | O guia completo em Markdown. Fonte única do conteúdo; ideal para uma sessão do Claude ler. |
| [`starter-kit/`](starter-kit) | Kit pronto para copiar num projeto (Laravel + JS): CLAUDE.md, permissões, hooks, regra, skills e subagente. |
| [`index.html`](index.html) | O site, gerado a partir do `GUIA.md`. |
| [`llms.txt`](llms.txt) | Índice para LLMs. |
| [`build.py`](build.py) / [`template.html`](template.html) | Gerador do site. |

## Ensinar a uma sessão do Claude

```text
Leia o guia em https://raw.githubusercontent.com/HumbertoAlcantaraArruda/boas-praticas-claude-code/main/GUIA.md
e o kit em https://github.com/HumbertoAlcantaraArruda/boas-praticas-claude-code/tree/main/starter-kit.
Depois analise este projeto e proponha (sem aplicar ainda) um CLAUDE.md enxuto,
as regras de permissão e os hooks que fazem sentido aqui. Explique cada escolha.
```

## Usar o kit inicial

1. Copie `starter-kit/CLAUDE.md` e `starter-kit/.claude/` para a raiz do seu projeto.
2. Adicione as linhas de `starter-kit/gitignore-adicionar.txt` ao `.gitignore`.
3. Ajuste o `CLAUDE.md` à sua stack.
4. No Claude Code, rode `/status`, `/hooks` e `/context` para conferir.

Os hooks são em Node (sem `jq`) e funcionam no Windows, macOS e Linux.

## Atualizar o site

Edite o `GUIA.md` e rode:

```bash
pip install markdown pygments
python build.py
```

---

Guia independente, sem vínculo com a Anthropic. Claude e Claude Code são marcas da Anthropic. Quando algo divergir, vale a [documentação oficial](https://code.claude.com/docs).
