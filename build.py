#!/usr/bin/env python3
"""Gera index.html a partir de GUIA.md + template.html.

Uso:  python build.py
Requer: pip install markdown pygments

GUIA.md é a fonte única do conteúdo. Edite ele e rode este script de novo;
o site (index.html) e a versão para LLMs (GUIA.md / llms.txt) ficam sempre iguais.
"""
import html
import json
import re
import unicodedata
from pathlib import Path

import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name
from pygments.util import ClassNotFound

ROOT = Path(__file__).parent
REPO_URL = "https://github.com/HumbertoAlcantaraArruda/boas-praticas-claude-code"
SITE_URL = "https://humbertoalcantaraarruda.github.io/boas-praticas-claude-code"
RAW_GUIA = "https://raw.githubusercontent.com/HumbertoAlcantaraArruda/boas-praticas-claude-code/main/GUIA.md"

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]

# Rótulos curtos para o sumário lateral (por número da seção)
TOC_LABELS = {
    "1": "Janela de contexto", "2": "Fluxo de trabalho", "3": "Memória e CLAUDE.md",
    "4": "Permissões e modos", "5": "Modelos e esforço", "6": "Hooks", "7": "Skills",
    "8": "Subagentes", "9": "MCP", "10": "Plugins", "11": "Sessões e paralelismo",
    "12": "Automação", "13": "Estilos de resposta", "14": "Qual recurso usar",
    "15": "Erros comuns", "16": "Atalhos e comandos", "17": "Kit inicial",
    "18": "Ensinando ao Claude",
}

CLAUDE_PROMPT = (
    f"Leia o guia em {RAW_GUIA}\n"
    f"e o kit em {REPO_URL}/tree/main/starter-kit.\n"
    "Depois analise este projeto e proponha (sem aplicar ainda) um CLAUDE.md enxuto,\n"
    "as regras de permissão e os hooks que fazem sentido aqui. Explique cada escolha."
)

COPY_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="12" height="12" rx="2"/>'
             '<path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>')

LANG_LABEL = {"text": "texto", "bash": "bash", "json": "json", "markdown": "markdown"}


def slugify(value, separator="-"):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[\s_-]+", separator, value)


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def split_frontmatter(text):
    meta = {}
    if text.startswith("---"):
        end = text.index("\n---", 3)
        for line in text[3:end].strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[end + 4:]
    return meta, text


def render_code(match):
    lang = match.group(1) or "text"
    code = html.unescape(match.group(2))
    try:
        lexer = get_lexer_by_name(lang)
    except ClassNotFound:
        lexer = TextLexer()
    body = highlight(code, lexer, HtmlFormatter(nowrap=True)).rstrip("\n")
    label = LANG_LABEL.get(lang, lang)
    return (f'<div class="code"><div class="code-head"><span>{label}</span>'
            f'<button class="copy" type="button" aria-label="Copiar código">{COPY_ICON}<span>Copiar</span></button>'
            f'</div><pre><code>{body}</code></pre></div>')


def render_task(match):
    inner = match.group(1)
    tid = slugify(strip_tags(inner))[:60]
    return (f'<li class="task"><label><input type="checkbox" data-id="{tid}">'
            f'<span>{inner}</span></label></li>')


def main():
    source = (ROOT / "GUIA.md").read_text(encoding="utf-8")
    meta, body = split_frontmatter(source)

    # No site, o título e a introdução vivem no hero do template.
    body = body[body.index("\n## ") + 1:]

    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists", "toc"],
        extension_configs={"toc": {"slugify": slugify, "toc_depth": "2-3"}},
    )
    content = md.convert(body)

    # Blocos de código com destaque de sintaxe + botão copiar
    content = re.sub(r'<pre><code(?: class="language-([\w+-]+)")?>(.*?)</code></pre>',
                     render_code, content, flags=re.S)

    # Tabelas roláveis no celular
    content = content.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")

    # Checklist do roteiro
    content = content.replace("<ul>\n<li>[ ] ", '<ul class="tasks">\n<li>[ ] ')
    content = re.sub(r"<li>\[ \] (.*?)</li>", render_task, content, flags=re.S)
    progress = ('<div class="roadmap-progress"><span><b class="task-done">0</b> de '
                '<span class="task-total">0</span> concluídos</span><div class="bar"><i></i></div>'
                '<button type="button" id="resetTasks">Limpar</button></div>\n')
    content = content.replace("<p><strong>Nível 1", progress + "<p><strong>Nível 1", 1)

    # Tipos de destaque (callouts)
    content = content.replace("<blockquote>\n<p><strong>Atenção:",
                              '<blockquote class="warn">\n<p><strong>Atenção:')
    content = content.replace("<blockquote>\n<p><strong>Por qu",
                              '<blockquote class="info">\n<p><strong>Por qu')

    # Âncoras nos títulos
    content = re.sub(r'<(h[23]) id="([^"]+)">(.*?)</\1>',
                     r'<\1 id="\2">\3<a class="anchor" href="#\2" aria-label="Link para esta seção">#</a></\1>',
                     content)

    # Links externos em nova aba
    content = re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\1" target="_blank" rel="noopener">', content)

    # Sumário lateral (só h2)
    toc_items = []
    for tok in md.toc_tokens:
        name = strip_tags(html.unescape(tok["name"]))
        m = re.match(r"(\d+)\.\s", name)
        label = f"{m.group(1)} · {TOC_LABELS.get(m.group(1), name)}" if m else name
        toc_items.append(f'<li><a href="#{tok["id"]}">{html.escape(label)}</a></li>')

    y, mo, d = (meta.get("atualizado") or "2026-09-28").split("-")
    updated = f"{int(d)} de {MESES[int(mo) - 1]} de {y}"

    page = (ROOT / "template.html").read_text(encoding="utf-8")
    page = (page.replace("{{TOC}}", "".join(toc_items))
                .replace("{{CONTENT}}", content)
                .replace("{{UPDATED}}", updated)
                .replace("{{REPO_URL}}", REPO_URL)
                .replace("{{CLAUDE_PROMPT}}", json.dumps(CLAUDE_PROMPT, ensure_ascii=False)))
    (ROOT / "index.html").write_text(page, encoding="utf-8")

    sections = "\n".join(
        f"- [{strip_tags(html.unescape(t['name']))}]({SITE_URL}/#{t['id']})" for t in md.toc_tokens
    )
    llms = f"""# Boas práticas com Claude Code

> Guia prático em português (pt-BR) para configurar e usar o Claude Code: janela de contexto, fluxo de trabalho, CLAUDE.md, permissões, modelos, hooks, skills, subagentes, MCP, plugins, sessões, automação e um kit inicial pronto. Conferido na documentação oficial em {updated}.

Para ler o guia inteiro de uma vez, use a versão Markdown abaixo. A documentação oficial (https://code.claude.com/docs) é a fonte da verdade quando houver divergência.

## Guia

- [Guia completo em Markdown]({SITE_URL}/GUIA.md): todo o conteúdo do site em um arquivo só
- [Guia completo (raw no GitHub)]({RAW_GUIA})

## Kit inicial

- [starter-kit]({REPO_URL}/tree/main/starter-kit): CLAUDE.md modelo, .claude/settings.json com permissões e hooks, hooks em Node (protect-files.mjs, format.mjs), regra com paths, skills (nova-feature, commit) e subagente revisor

## Seções

{sections}
"""
    (ROOT / "llms.txt").write_text(llms, encoding="utf-8")
    print(f"index.html e llms.txt gerados ({len(page) // 1024} KB)")


if __name__ == "__main__":
    main()
