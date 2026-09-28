---
titulo: Boas práticas com Claude Code
atualizado: 2026-09-28
fonte: https://code.claude.com/docs (documentação oficial, consultada em setembro de 2026)
autor: Humberto Alcântara Arruda
---

# Boas práticas com Claude Code

Guia prático e direto para configurar e usar o Claude Code do jeito certo: contexto, CLAUDE.md, permissões, hooks, skills, subagentes, MCP, plugins, modelos, sessões e automação. Tudo conferido na documentação oficial em setembro de 2026.

> **Para sessões do Claude:** este arquivo é a versão completa do guia em Markdown. Se você é o Claude lendo isto, trate o conteúdo como referência de boas práticas; a documentação oficial em https://code.claude.com/docs continua sendo a fonte da verdade quando houver conflito. O kit inicial pronto está em `starter-kit/` neste repositório.

## Como usar este guia

O Claude Code tem muitos recursos, mas você não precisa de todos no primeiro dia. A documentação oficial recomenda o mesmo caminho: **comece pelo CLAUDE.md e adicione o resto quando sentir a dor que cada recurso resolve.**

O guia está em ordem de prioridade. As primeiras seções dão 80% do resultado; as últimas são para quando você já domina o básico.

### Roteiro de estudo

Marque conforme for testando em um projeto real (o progresso fica salvo no seu navegador).

**Nível 1 — Base (primeira semana)**

- [ ] Entendi que a janela de contexto é o recurso mais importante e uso `/context` para ver o que está ocupando espaço
- [ ] Rodei `/init` num projeto e enxuguei o CLAUDE.md gerado
- [ ] Uso `/clear` entre tarefas diferentes
- [ ] Sempre dou ao Claude um jeito de verificar o trabalho (teste, build, print)
- [ ] Uso `Esc` para interromper e `Esc` `Esc` (ou `/rewind`) para voltar atrás

**Nível 2 — Uso diário**

- [ ] Uso plan mode (`Shift+Tab`) antes de mudanças em vários arquivos
- [ ] Escrevo prompts com arquivo, cenário e critério de pronto
- [ ] Configurei permissões (`allow`/`ask`/`deny`) para parar de aprovar comando de rotina
- [ ] Sei trocar de modelo (`/model`) e de esforço (`/effort`) conforme a tarefa
- [ ] Retomo sessões com `claude --continue` / `--resume` e dou nome com `/rename`

**Nível 3 — Automação**

- [ ] Tenho um hook que formata código depois de cada edição
- [ ] Tenho um hook que bloqueia edição de arquivos sensíveis
- [ ] Criei minha primeira skill (`.claude/skills/<nome>/SKILL.md`)
- [ ] Uso subagentes para investigar sem sujar o contexto principal

**Nível 4 — Integração e escala**

- [ ] Conectei um servidor MCP útil de verdade (banco, GitHub, Sentry...)
- [ ] Instalei um plugin pelo `/plugin` e medi o custo de contexto dele
- [ ] Rodei o Claude em modo não interativo (`claude -p`) num script
- [ ] Usei worktrees (`claude --worktree`) para trabalhar em paralelo
- [ ] Usei `/goal` para uma tarefa longa com condição verificável

## 1. O conceito que muda tudo: a janela de contexto

Quase toda boa prática do Claude Code nasce de uma restrição só: **a janela de contexto enche rápido, e a qualidade cai conforme ela enche.**

A janela guarda a conversa inteira: cada mensagem, cada arquivo lido, cada saída de comando. Uma sessão de debug pode consumir dezenas de milhares de tokens. Quando está cheia, o Claude começa a "esquecer" instruções do começo e erra mais.

Na prática, isso significa:

| Situação | O que fazer |
| --- | --- |
| Terminou uma tarefa e vai começar outra, sem relação | `/clear` (zera o contexto) |
| Sessão longa, mas o histórico ainda importa | `/compact Foque nas mudanças da API` (resume com instrução) |
| Quer ver o que está ocupando espaço | `/context` |
| Pergunta rápida que não precisa ficar no histórico | `/btw <pergunta>` (a resposta não entra na conversa) |
| Corrigiu o Claude duas vezes no mesmo problema e não resolveu | `/clear` e um prompt novo, melhor, com o que você aprendeu |
| Investigação que vai ler muitos arquivos | Delegue a um subagente (seção 8) |

> **Dica:** você pode orientar a compactação automática no próprio CLAUDE.md: "Ao compactar, preserve sempre a lista de arquivos alterados e os comandos de teste." Assim o que importa sobrevive ao resumo.

> **Por quê:** uma sessão limpa com um prompt melhor quase sempre ganha de uma sessão longa cheia de correções. As tentativas que falharam continuam no contexto e atrapalham.

## 2. O fluxo de trabalho que funciona

### Dê ao Claude um jeito de verificar o próprio trabalho

Essa é a dica mais importante da documentação oficial. O Claude para quando o trabalho *parece* pronto. Sem uma verificação que ele consiga rodar, você vira o único teste, e cada erro espera você perceber.

A verificação pode ser um teste, o código de saída de um build, um linter, um script que compara saída, ou um print de tela comparado com o design.

| Estratégia | Antes | Depois |
| --- | --- | --- |
| Critério de verificação | "implementa uma função que valida e-mail" | "escreve `validaEmail`. Casos: `user@example.com` é válido, `invalido` não, `user@.com` não. Rode os testes depois de implementar" |
| UI verificada visualmente | "deixa o dashboard mais bonito" | "[print] implementa esse design. Tira um print do resultado, compara com o original, lista as diferenças e corrige" |
| Causa raiz, não sintoma | "o build está falhando" | "o build falha com este erro: [erro]. Corrija e confirme que o build passa. Resolva a causa, não esconda o erro" |

Peça **evidência**, não afirmação: a saída do teste, o comando que rodou e o que retornou. Revisar evidência é mais rápido do que refazer a verificação.

### Explorar → Planejar → Implementar → Commitar

1. **Explorar.** Entre em plan mode (`Shift+Tab` até aparecer `⏸ plan mode on`, ou `claude --permission-mode plan`). O Claude lê arquivos e responde perguntas sem mudar nada.
2. **Planejar.** Peça um plano detalhado: quais arquivos mudam, qual o fluxo. Aperte `Ctrl+G` para abrir o plano no seu editor e ajustar antes de aprovar.
3. **Implementar.** Aprove o plano (ou `Shift+Tab` para sair do plan mode). Peça para implementar, escrever testes, rodar e corrigir falhas.
4. **Commitar.** Peça o commit com mensagem descritiva e, se quiser, o PR.

> **Atenção:** plan mode tem custo. Para mudanças pequenas e claras (renomear variável, corrigir typo, adicionar um log), peça direto. **Se você consegue descrever o diff em uma frase, pule o plano.**

### Prompts específicos

O Claude infere intenção, mas não lê mente. Cite arquivos, restrições e padrões existentes.

| Estratégia | Antes | Depois |
| --- | --- | --- |
| Delimite a tarefa | "adiciona testes no UserService" | "escreve um teste para o `UserService` cobrindo o caso do usuário deslogado. Sem mocks." |
| Aponte a fonte | "por que essa API é tão estranha?" | "olha o histórico do git do `PaymentGateway` e resume como a API chegou nesse formato" |
| Referencie padrões | "cria um endpoint de pedidos" | "olha como `ProductController` e `ProductRequest` foram feitos e segue o mesmo padrão para pedidos" |
| Descreva o sintoma | "conserta o bug do login" | "o login falha depois que a sessão expira. Verifique o fluxo em `app/Http/Middleware`, principalmente o refresh do token. Escreva um teste que reproduz, depois corrija" |

### Dê contexto rico

- **`@arquivo`** no prompt referencia um arquivo; o Claude lê antes de responder.
- **Cole imagens** (`Ctrl+V`) de erro, layout ou design.
- **Passe URLs** de documentação.
- **Envie dados por pipe:** `cat erro.log | claude`.
- **`!` no início da linha** roda um comando de shell e joga a saída na conversa.

### Para features grandes: deixe o Claude te entrevistar

```text
Quero construir [descrição curta]. Me entreviste em detalhe usando a ferramenta AskUserQuestion.
Pergunte sobre implementação técnica, UI/UX, casos de borda e trade-offs.
Não faça perguntas óbvias; vá nas partes difíceis que eu talvez não tenha considerado.
Continue até cobrir tudo e então escreva a especificação completa em SPEC.md.
```

Depois, abra uma **sessão nova** para implementar a partir do `SPEC.md`: contexto limpo, focado só em executar.

### Revisão adversária antes de dar como pronto

Quanto mais o Claude trabalha sozinho, mais vale uma checagem independente. Um subagente em contexto limpo vê só o diff, não o raciocínio que o produziu:

```text
Use um subagente para revisar o diff contra o PLAN.md. Confira se cada requisito foi
implementado, se os casos de borda têm teste e se nada fora do escopo mudou.
Reporte lacunas, não preferências de estilo.
```

O comando embutido `/code-review` faz uma revisão de bugs do diff atual num subagente.

## 3. Memória do projeto: CLAUDE.md e companhia

Toda sessão começa com a janela vazia. Dois mecanismos carregam conhecimento entre sessões:

- **CLAUDE.md:** instruções que **você** escreve.
- **Memória automática:** anotações que o **Claude** escreve sozinho a partir das suas correções.

Os dois entram no começo de toda conversa, mas são **contexto, não regra obrigatória**. Para garantir algo sempre, use um hook (seção 6).

### Onde colocar cada CLAUDE.md

| Tipo | Local | Para quê | Compartilhado com |
| --- | --- | --- | --- |
| Usuário | `~/.claude/CLAUDE.md` | Suas preferências em todos os projetos | Só você |
| Projeto | `./CLAUDE.md` ou `./.claude/CLAUDE.md` | Arquitetura, padrões, comandos do projeto | Time (via git) |
| Local | `./CLAUDE.local.md` | Preferências suas só neste projeto (coloque no `.gitignore`) | Só você |

Como carregam:

- O Claude Code lê o `CLAUDE.md` da pasta atual **e de todas as pastas acima**. Tudo é **somado**, não substituído; o mais próximo de onde você abriu é lido por último.
- `CLAUDE.md` em **subpastas** entra só quando o Claude lê arquivos daquela subpasta.
- Comentários HTML (`<!-- nota -->`) são removidos antes de ir para o contexto: servem de nota para humanos sem gastar tokens.
- Se o repositório já usa `AGENTS.md` (de outras ferramentas), o Claude Code lê ele quando não há `CLAUDE.md`. Para usar os dois, coloque `@AGENTS.md` dentro do `CLAUDE.md`.

### O que colocar (e o que não colocar)

Rode `/init` para gerar um CLAUDE.md inicial a partir do código, depois refine.

| ✅ Inclua | ❌ Não inclua |
| --- | --- |
| Comandos que o Claude não adivinha | O que ele descobre lendo o código |
| Estilo de código diferente do padrão | Convenções padrão da linguagem |
| Como rodar testes e qual runner preferir | Documentação de API detalhada (linke) |
| Etiqueta do repositório (branch, PR) | Informação que muda com frequência |
| Decisões de arquitetura do projeto | Tutoriais e explicações longas |
| Pegadinhas do ambiente (variáveis obrigatórias) | Descrição arquivo por arquivo |
| Comportamentos não óbvios | Obviedades como "escreva código limpo" |

> **Dica:** mire em **menos de 200 linhas**. Para cada linha, pergunte: *"se eu apagar isso, o Claude erra?"* Se não, apague. CLAUDE.md inchado faz o Claude ignorar justamente as regras importantes. Se uma regra vive sendo ignorada, dê ênfase com "IMPORTANT" **só nela**.

Exemplo enxuto:

```markdown
# Estilo de código
- Use ES modules (import/export), não CommonJS (require)

# Fluxo
- Rode o typecheck ao terminar uma série de mudanças
- Prefira rodar um teste só, não a suíte inteira
```

### Importar arquivos com `@`

```markdown
Veja @README.md para a visão geral e @package.json para os comandos npm.

# Instruções extras
- fluxo de git @docs/git.md
- preferências pessoais @~/.claude/minhas-preferencias.md
```

Arquivos importados entram no contexto no início junto com o CLAUDE.md. Importar organiza, mas **não economiza** contexto. Para economizar, use regras com `paths` ou skills.

### Regras modulares: `.claude/rules/`

Para projetos maiores, quebre as instruções em arquivos por tema em `.claude/rules/` (ex.: `testes.md`, `api.md`, `seguranca.md`). A grande vantagem: regras com `paths` **só carregam quando o Claude lê arquivos que batem com o padrão**.

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# Regras de API
- Todo endpoint valida a entrada
- Use o formato padrão de resposta de erro
```

Regras sem `paths` carregam sempre, como o CLAUDE.md. Regras pessoais para todos os projetos ficam em `~/.claude/rules/`.

### Memória automática

- Ligada por padrão. Liga/desliga em `/memory` (ou `"autoMemoryEnabled": false` nas configurações).
- Fica em `~/.claude/projects/<projeto>/memory/`, com um índice `MEMORY.md` e um arquivo por assunto.
- Só as **primeiras 200 linhas ou 25 KB** do `MEMORY.md` carregam no início da sessão.
- São arquivos Markdown comuns: você pode ler, editar e apagar pelo `/memory`.

### CLAUDE.md, regra ou skill?

| | CLAUDE.md | `.claude/rules/` | Skill |
| --- | --- | --- | --- |
| Carrega | Toda sessão | Toda sessão, ou quando arquivos que batem com `paths` são abertos | Sob demanda |
| Escopo | Projeto inteiro | Pode ser por caminho de arquivo | Tarefa específica |
| Melhor para | Convenções centrais e comandos | Regras por linguagem ou pasta | Material de referência e fluxos repetíveis |

## 4. Permissões e modos: menos cliques, mesmo controle

### Modos de permissão

Troque com `Shift+Tab`, com `--permission-mode <modo>` ao abrir, ou com `"defaultMode"` nas configurações.

| Modo | Roda sem pedir | Melhor para |
| --- | --- | --- |
| `default` (Manual) | Só leituras | Revisar cada ação, trabalho sensível |
| `acceptEdits` | Leituras, edições e comandos comuns de arquivo (`mkdir`, `mv`, `cp`...) | Iterar em código que você está revisando |
| `plan` | Leituras (e comandos aprovados pelo classificador, se o auto mode estiver disponível) | Explorar antes de mudar |
| `auto` | Tudo, com um classificador revisando em segundo plano | Tarefas longas, menos fadiga de aprovação |
| `dontAsk` | Leituras e ferramentas pré-aprovadas; o resto é negado | CI e scripts travados |
| `bypassPermissions` | Tudo | **Só** em containers e VMs isolados |

Nas versões recentes, o **auto mode** é o modo inicial padrão no terminal e no VS Code: um segundo modelo avalia as ações e bloqueia o que parece arriscado. Regras `deny` valem em **todos** os modos, inclusive `bypassPermissions`.

### Regras de permissão

Ficam no bloco `permissions` do `settings.json`, em três listas. **A ordem de avaliação é: `deny` → `ask` → `allow`.** A primeira que casar decide, e especificidade não muda a ordem: um `deny` amplo sempre vence um `allow` específico.

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(php artisan test *)",
      "Bash(git commit *)"
    ],
    "ask": [
      "Bash(git push *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)"
    ]
  }
}
```

Como os padrões funcionam:

| Regra | Casa com | Não casa com |
| --- | --- | --- |
| `Bash(npm run build)` | exatamente `npm run build` | `npm run build --watch` |
| `Bash(npm run *)` | `npm run build`, `npm run test --watch`, `npm run` | `npm install` |
| `Bash(ls *)` | `ls -la`, `ls` | `lsof` (o espaço antes do `*` importa) |
| `Read(./.env)` | ler o `.env` da pasta atual | |
| `WebFetch(domain:example.com)` | buscar páginas de example.com | |
| `mcp__github__*` | todas as ferramentas do servidor MCP `github` | |

Detalhes que pegam muita gente:

- Coloque o `*` **depois do subcomando**: `Bash(git log *)` libera só `git log`; `Bash(git *)` libera **todo** comando git.
- O Claude Code entende operadores de shell: `Bash(safe-cmd *)` **não** libera `safe-cmd && outro-cmd`.
- Um `deny` em `Read(caminho)` também bloqueia **editar** e **criar** esse arquivo.
- Caminhos: `//caminho` é absoluto, `~/caminho` é a partir da home, `/caminho` é relativo à origem do arquivo de configuração, `./caminho` é relativo à pasta atual.
- Regras de Bash não são uma fronteira de segurança completa (`/bin/rm` ou `sh -c 'rm ...'` escapam de `Bash(rm *)`). Para isolamento de verdade, use o sandbox (`/sandbox`).

Use `/permissions` para ver e editar as regras dentro da sessão.

### Onde ficam as configurações (e quem vence)

Do mais forte para o mais fraco:

1. **Gerenciadas** pela organização (`managed-settings.json`)
2. **Linha de comando** (`claude --settings arquivo.json`)
3. **Local do projeto:** `.claude/settings.local.json` (só você, fora do git)
4. **Projeto compartilhado:** `.claude/settings.json` (time, no git)
5. **Usuário:** `~/.claude/settings.json` (você, todos os projetos)

> **Dica:** a linha `"$schema"` dá autocomplete e validação no VS Code. Depois de salvar, rode `/status` para confirmar que o arquivo carregou. Configuração é JSON estrito: comentário `//` ou vírgula sobrando quebra o arquivo.

## 5. Modelos, esforço e raciocínio

| Alias | O que é | Quando usar |
| --- | --- | --- |
| `sonnet` | Sonnet mais recente | Dia a dia, maioria das tarefas |
| `opus` | Opus mais recente | Raciocínio complexo, arquitetura |
| `haiku` | Modelo rápido e barato | Tarefas simples |
| `fable` | Fable (onde disponível) | Sessões mais longas e problemas mais difíceis |
| `opusplan` | Opus para planejar, Sonnet para executar | Planejar bem e executar barato |
| `sonnet[1m]`, `opus[1m]` | Variantes com janela de 1 milhão de tokens | Contextos gigantes |

Como trocar:

- `/model` abre o seletor; `/model opus` troca e salva como padrão.
- `claude --model sonnet` ao abrir, ou `"model": "opus"` no `settings.json`.
- `Alt+P` (Windows/Linux) ou `Option+P` (macOS) troca de modelo na hora.

**Esforço** (`/effort`): controla quanto o modelo raciocina. Níveis: `low`, `medium`, `high`, `xhigh`, `max` (e `ultracode`, que combina `xhigh` com workflows dinâmicos). Mais esforço = mais qualidade em problema difícil, mais custo e demora em problema fácil.

- **`ultrathink`** escrito no prompt pede raciocínio mais profundo **só naquele turno**.
- `Alt+T` / `Option+T` liga e desliga o pensamento estendido; `Ctrl+O` mostra o raciocínio.
- `/fast` (ou `Alt+O`) liga o modo rápido.

> **Dica:** não use o modelo mais caro com esforço máximo para tudo. Sonnet com esforço médio resolve a maior parte do trabalho; guarde Opus/`xhigh` ou `ultrathink` para arquitetura e bugs difíceis.

## 6. Hooks: automação que sempre acontece

Instruções no CLAUDE.md são **pedidos**. Hooks são **garantias**: scripts que o Claude Code roda sozinho em pontos fixos do ciclo, sem depender de o modelo lembrar.

**Regra de ouro:** se algo precisa acontecer **toda vez, sem exceção**, é hook. "Nunca edite o `.env`" no CLAUDE.md é um pedido; um hook `PreToolUse` que bloqueia a edição é aplicação.

### Eventos mais úteis

| Evento | Quando dispara | Uso típico |
| --- | --- | --- |
| `PreToolUse` | Antes de uma ferramenta rodar (pode bloquear) | Bloquear arquivos ou comandos perigosos |
| `PostToolUse` | Depois que uma ferramenta roda com sucesso | Formatar, rodar linter |
| `UserPromptSubmit` | Quando você envia um prompt | Validar ou enriquecer o prompt |
| `Notification` | Quando o Claude espera você | Notificação no desktop |
| `Stop` | Quando o Claude termina de responder (pode impedir) | Exigir que os testes passem antes de parar |
| `SessionStart` | Início ou retomada de sessão (matcher `compact` = depois de compactar) | Reinjetar contexto |
| `PreCompact` / `PostCompact` | Antes/depois de compactar | Salvar estado |
| `SubagentStart` / `SubagentStop` | Subagente começa/termina | Log, validação |
| `SessionEnd` | Sessão termina | Limpeza, relatório |

Existem outros (`PermissionRequest`, `InstructionsLoaded`, `FileChanged`, `WorktreeCreate`...). Veja a referência completa na documentação.

### Estrutura

```json
{
  "hooks": {
    "NomeDoEvento": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "script ou comando", "timeout": 30 }
        ]
      }
    ]
  }
}
```

- **`matcher`** filtra quando dispara (para eventos de ferramenta, é o nome da ferramenta; `Edit|Write` pega as duas).
- **Tipos:** `command` (shell), `http` (POST para uma URL), `mcp_tool`, `prompt` (um modelo decide) e `agent` (experimental).
- O hook recebe um **JSON no stdin** com `session_id`, `cwd`, `tool_name`, `tool_input` etc.
- **Código de saída:** `0` = ok; `2` = **bloqueia** (em eventos bloqueáveis) e o stderr volta para o Claude como explicação; outros = erro não bloqueante.
- `${CLAUDE_PROJECT_DIR}` aponta para a raiz do projeto; use nos caminhos dos scripts.
- Onde configurar: `~/.claude/settings.json` (todos os projetos), `.claude/settings.json` (time), `.claude/settings.local.json` (só você). Hooks de fontes diferentes **se somam**.
- `/hooks` mostra tudo que está configurado (somente leitura; edite o JSON).

### Receita 1: formatar depois de cada edição

A versão mais simples, da documentação (precisa de `jq` e Prettier):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write" }
        ]
      }
    ]
  }
}
```

O kit inicial deste guia traz uma versão em Node (`format.mjs`) que funciona igual no Windows, sem `jq`, e formata PHP com Pint e JS/CSS com Prettier.

### Receita 2: bloquear arquivos protegidos

```bash
#!/bin/bash
# .claude/hooks/protect-files.sh
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
FILE_PATH="${FILE_PATH//\\//}"   # normaliza barras do Windows

for pattern in ".env" "package-lock.json" ".git/"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Bloqueado: $FILE_PATH é protegido ('$pattern')" >&2
    exit 2
  fi
done
exit 0
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh" }
        ]
      }
    ]
  }
}
```

No Linux/macOS, lembre do `chmod +x`. O kit inicial tem a versão em Node (`protect-files.mjs`).

### Receita 3: notificação quando o Claude precisar de você

Em `~/.claude/settings.json` (Windows):

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code precisa de voce', 'Claude Code')\""
          }
        ]
      }
    ]
  }
}
```

No macOS use `osascript -e 'display notification "..." with title "Claude Code"'`; no Linux, `notify-send 'Claude Code' '...'`. O matcher pode filtrar: `permission_prompt` (esperando aprovação) ou `idle_prompt` (terminou e você não respondeu).

### Receita 4: reinjetar contexto depois de compactar

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          { "type": "command", "command": "echo 'Lembrete: use pnpm, não npm. Rode os testes antes de commitar.'" }
        ]
      }
    ]
  }
}
```

Troque o `echo` por qualquer comando dinâmico, como `git log --oneline -5`.

### Receita 5: não deixar parar antes de terminar (hook de prompt)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verifique se todas as tarefas pedidas foram concluídas. Se não, responda {\"ok\": false, \"reason\": \"o que falta fazer\"}."
          }
        ]
      }
    ]
  }
}
```

Um modelo rápido avalia; se responder `ok: false`, o Claude continua usando o `reason` como próxima instrução.

> **Dica:** o próprio Claude escreve hooks para você. Peça: *"Escreva um hook que roda o ESLint depois de cada edição"* ou *"Escreva um hook que bloqueia escrita na pasta de migrations"*.

## 7. Skills (e comandos personalizados)

Uma skill é um arquivo `SKILL.md` com instruções, conhecimento ou um fluxo de trabalho. Diferente do CLAUDE.md, **só carrega quando é usada**: no início da sessão entram apenas nome e descrição; o conteúdo completo entra quando você chama `/nome` ou quando o Claude decide que ela é relevante.

**Quando criar uma skill:** quando você digita o mesmo prompt pela terceira vez, ou cola o mesmo passo a passo na conversa de novo.

### Onde ficam

| Local | Caminho | Vale para |
| --- | --- | --- |
| Pessoal | `~/.claude/skills/<nome>/SKILL.md` | Todos os seus projetos |
| Projeto | `.claude/skills/<nome>/SKILL.md` | Este repositório (vai no git) |
| Plugin | `<plugin>/skills/<nome>/SKILL.md` | Onde o plugin estiver ativo (`/plugin:nome`) |

O nome da **pasta** vira o comando: `.claude/skills/commit/SKILL.md` → `/commit`.

> **Atenção:** comandos antigos em `.claude/commands/*.md` ainda funcionam, mas **skills são o formato recomendado** para coisas novas: aceitam pasta com arquivos de apoio e mais opções.

### Skill de referência (conhecimento)

```markdown
---
name: convencoes-api
description: Convenções de design de API REST dos nossos serviços
---
# Convenções de API
- kebab-case nas URLs
- camelCase nas propriedades JSON
- Toda listagem tem paginação
- Versão na URL (/v1/, /v2/)
```

### Skill de ação (fluxo que você dispara)

```markdown
---
name: corrigir-issue
description: Corrige uma issue do GitHub
disable-model-invocation: true
argument-hint: "[número da issue]"
---
Analise e corrija a issue do GitHub: $ARGUMENTS.

1. Use `gh issue view` para ver os detalhes
2. Encontre os arquivos relevantes
3. Implemente a correção
4. Escreva e rode testes
5. Crie um commit descritivo e abra o PR
```

Uso: `/corrigir-issue 1234`.

### Campos do frontmatter que mais importam

| Campo | Para quê |
| --- | --- |
| `description` | O que a skill faz e **quando usar**. É isso que o Claude lê para decidir se carrega. Seja específico. |
| `disable-model-invocation: true` | Só **você** chama (use para qualquer coisa com efeito colateral: deploy, commit, envio). Custo de contexto zero até ser chamada. |
| `user-invocable: false` | Só o **Claude** usa (conhecimento de fundo). |
| `allowed-tools` | Pré-aprova ferramentas enquanto a skill roda, ex.: `Bash(git add *) Bash(git commit *)` |
| `argument-hint` / `arguments` | Dica de argumentos no autocomplete / argumentos nomeados |
| `context: fork` | Roda a skill num subagente isolado |
| `model`, `effort` | Troca modelo ou esforço só para essa skill |
| `paths` | Só carrega automaticamente quando arquivos batem com o padrão |

### Recursos poderosos

- **Argumentos:** `$ARGUMENTS` (tudo), `$0`, `$1` (posições) ou nomes definidos em `arguments`.
- **Injeção dinâmica:** `` !`git diff HEAD` `` roda o comando **antes** do Claude ler a skill e coloca a saída no lugar. O Claude recebe os dados, não o comando.
- **Arquivos de apoio:** mantenha o `SKILL.md` com menos de 500 linhas e aponte para `reference.md`, `examples.md` ou `scripts/` na mesma pasta; eles só carregam quando necessários. Use `${CLAUDE_SKILL_DIR}` para referenciar scripts.

```markdown
---
name: resumo-mudancas
description: Resume as mudanças não commitadas e aponta riscos. Use quando o usuário perguntar o que mudou ou pedir mensagem de commit.
---
## Mudanças atuais
!`git diff HEAD`

## Instruções
Resuma as mudanças em dois ou três tópicos e liste riscos (tratamento de erro faltando,
valores fixos no código, testes que precisam de atualização).
```

### Skills que já vêm embutidas

`/code-review` (revisa o diff procurando bugs), `/security-review`, `/batch` (mudança grande em paralelo), `/debug`, `/doctor` (checkup do setup e sugestões para enxugar o CLAUDE.md), `/verify`, `/run` e outras.

## 8. Subagentes: trabalho isolado, contexto limpo

Um subagente é um "ajudante" que roda com **janela de contexto própria**, ferramentas próprias e às vezes modelo próprio. Ele pode ler dezenas de arquivos, e a sua conversa principal recebe **só o resumo**.

**Quando usar:** investigação que lê muitos arquivos, rodar testes/logs com saída enorme, revisão com olhar independente, tarefas paralelas.

```text
Use subagentes para investigar como nosso sistema de autenticação faz refresh de token
e se já existe algum utilitário de OAuth que eu deveria reaproveitar.
```

### Subagentes embutidos

| Nome | O que faz |
| --- | --- |
| `Explore` | Busca rápida e só leitura no código |
| `Plan` | Pesquisa durante o plan mode, só leitura |
| `general-purpose` | Tarefas complexas com leitura e escrita |

### Criando o seu

Arquivo Markdown com frontmatter em `.claude/agents/` (projeto) ou `~/.claude/agents/` (todos os projetos). O corpo vira o prompt de sistema do subagente.

```markdown
---
name: revisor-seguranca
description: Revisa código procurando vulnerabilidades. Use proativamente depois de mudanças grandes.
tools: Read, Grep, Glob, Bash
model: opus
---
Você é um engenheiro de segurança sênior. Revise o código procurando:
- Injeção (SQL, XSS, comando)
- Falhas de autenticação e autorização
- Segredos no código
- Tratamento inseguro de dados

Dê referências de linha e correções sugeridas.
```

Campos úteis: `tools` / `disallowedTools` (restrinja! um revisor não precisa de `Edit`), `model` (`sonnet`, `opus`, `haiku`, `inherit`), `permissionMode`, `maxTurns`, `skills` (pré-carrega skills), `mcpServers`, `hooks`, `memory` (memória própria entre sessões), `isolation: worktree` (roda numa cópia isolada do repositório), `background: true`.

### Como chamar

- **Automático:** o Claude delega com base na `description`. Escrever "use proativamente" incentiva.
- **Pedindo:** "Use o subagente revisor-seguranca para olhar as mudanças de auth".
- **Mencionando:** `@agent-revisor-seguranca olha isso`.
- **Sessão inteira como o agente:** `claude --agent revisor-seguranca`.

> **Dica:** o padrão **escritor/revisor** funciona muito bem. Uma sessão implementa; outra (ou um subagente), com contexto limpo, revisa sem viés de quem escreveu. Mas diga ao revisor para reportar **só** o que afeta correção ou requisitos; senão ele sempre acha "problema" e você acaba superengenheirando.

## 9. MCP: conectando o Claude a ferramentas externas

MCP (Model Context Protocol) conecta o Claude Code a serviços de fora: banco de dados, GitHub, Sentry, Notion, Figma, Slack... Em vez de você copiar e colar informação, o Claude consulta e age direto.

**Quando usar:** quando você vive copiando dados de uma aba do navegador que o Claude não vê.

### Adicionando servidores

```bash
# Servidor remoto (HTTP) — o recomendado para serviços na nuvem
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Com token no cabeçalho
claude mcp add --transport http minha-api https://api.exemplo.com/mcp \
  --header "Authorization: Bearer SEU_TOKEN"

# Servidor local (stdio) — o "--" separa as opções do Claude do comando do servidor
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://leitura:senha@localhost/meubanco"
```

### Escopos

| Escopo | Onde fica | Quem vê |
| --- | --- | --- |
| `local` (padrão) | `~/.claude.json`, dentro do projeto | Só você, só neste projeto |
| `project` | `.mcp.json` na raiz (vai no git) | O time todo (cada um aprova na primeira vez) |
| `user` | `~/.claude.json` | Só você, todos os projetos |

Use `--scope project` para compartilhar. No `.mcp.json`, variáveis de ambiente evitam segredo no git:

```json
{
  "mcpServers": {
    "api-interna": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.exemplo.com}/mcp",
      "headers": { "Authorization": "Bearer ${API_TOKEN}" }
    }
  }
}
```

`${VAR}` usa a variável; `${VAR:-padrao}` usa um valor padrão se ela não existir.

### Comandos do dia a dia

- `/mcp` — status das conexões e login OAuth.
- `claude mcp list` / `claude mcp get <nome>` / `claude mcp remove <nome>`.
- `@servidor/recurso` no prompt referencia um recurso exposto por um servidor.
- `/mcp__servidor__prompt` roda um prompt exposto por um servidor.

> **Por quê não pesa no contexto:** com a busca de ferramentas (ligada por padrão), só os **nomes** das ferramentas carregam no início; o esquema completo entra quando o Claude precisa. Use `/context all` para ver o custo de cada uma.

> **Atenção:** só conecte servidores em que você confia. Servidores que buscam conteúdo externo podem trazer **prompt injection**. Prefira chaves **somente leitura**, restrinja escopos OAuth e comece com integrações de leitura.

> **Dica:** para serviços com CLI boa, a CLI costuma ser **mais eficiente** que MCP. Com o `gh` instalado, o Claude cria issues, abre PRs e lê comentários sem configurar nada. Peça: *"Use `ferramenta --help` para aprender a ferramenta e resolva X."*

**Skill + MCP** é a combinação mais forte: o MCP dá o acesso ao banco; uma skill ensina o schema e os padrões de consulta do seu time.

## 10. Plugins: pacotes prontos

Um plugin empacota skills, subagentes, hooks e servidores MCP em uma unidade instalável. Use para instalar um setup pronto de alguém ou levar o seu setup para vários repositórios.

- `/plugin` abre o navegador de plugins (aba **Discover**). O marketplace oficial da Anthropic (`claude-plugins-official`) é adicionado na primeira sessão interativa.
- Escopos de instalação: **usuário** (você, todos os projetos), **projeto** (time, via `.claude/settings.json`) e **local** (você, só este repositório).
- Skills de plugin ganham prefixo: `/meu-plugin:revisar`.
- **Plugins de inteligência de código** (LSP) dão navegação por símbolo e erros de tipo depois de cada edição; valem muito em linguagens tipadas e bases grandes.
- `claude plugin disable <nome>` desliga sem desinstalar.

> **Atenção:** um plugin ativo pesa em **toda** sessão (nomes e descrições das skills entram no contexto) e roda com as **suas** permissões. Instale só o que você usa e revise antes de instalar plugins de terceiros.

Estrutura mínima de um plugin seu:

```text
meu-plugin/
├── .claude-plugin/plugin.json   # manifesto: nome, versão, descrição
├── skills/revisar/SKILL.md
├── agents/revisor.md
├── hooks/hooks.json
└── .mcp.json
```

## 11. Sessões, checkpoints e trabalho em paralelo

### Retomar e organizar sessões

- `claude --continue` retoma a última sessão; `claude --resume` mostra a lista.
- `/rename oauth-migracao` dá nome à sessão. Trate sessões como branches: uma por frente de trabalho.
- `/branch` cria um desvio da conversa para testar outra direção sem perder a original.

### Checkpoints: desfazer sem medo

Cada prompt que você envia cria um checkpoint automático. `Esc` `Esc` (com o campo vazio) ou `/rewind` abre o menu:

- **Restaurar código e conversa**, **só conversa** ou **só código**
- **Resumir daqui em diante** / **resumir até aqui** (compacta parte da conversa)

Isso muda o jeito de trabalhar: você pode mandar o Claude tentar algo arriscado e voltar se não der certo.

> **Atenção:** checkpoints só rastreiam edições feitas pelas ferramentas de edição do Claude. **Mudanças feitas por comandos Bash (`rm`, `mv`, `cp`) e por subagentes em segundo plano não voltam.** Não é substituto do git.

### Worktrees: várias sessões sem conflito

```bash
claude --worktree feature-auth     # ou -w
```

Cria uma cópia isolada em `.claude/worktrees/feature-auth/` numa branch `worktree-feature-auth`. Abra outro terminal com outro nome para uma segunda sessão paralela. Ao sair, se estiver limpo, é removida; se tiver trabalho, o Claude pergunta.

- Adicione `.claude/worktrees/` ao `.gitignore`.
- Um arquivo `.worktreeinclude` (sintaxe de `.gitignore`) copia arquivos ignorados como `.env` para cada worktree nova.
- `claude --worktree "#1234"` cria a worktree a partir de um PR.
- Subagentes com `isolation: worktree` trabalham cada um em sua cópia.

### Outras formas de paralelizar

- `Ctrl+B` manda tarefas em execução para segundo plano.
- `/batch <instrução>` divide uma mudança grande entre vários subagentes, cada um em sua worktree.
- `claude agents` (agent view) despacha sessões em segundo plano e acompanha todas numa tela.
- A extensão do VS Code e o app desktop também gerenciam sessões paralelas.

## 12. Automação: modo não interativo, metas e agendamento

### `claude -p`: Claude em scripts e CI

```bash
# Pergunta única
claude -p "Explique o que este projeto faz"

# Saída estruturada para scripts
claude -p "Liste todos os endpoints da API" --output-format json

# Streaming em tempo real
claude -p "Analise este log" --output-format stream-json --verbose

# Em lote, com permissões restritas
for f in $(cat arquivos.txt); do
  claude -p "Migre $f para o novo padrão. Responda OK ou FALHA." \
    --allowedTools "Edit,Bash(git commit *)"
done
```

Teste o prompt em 2 ou 3 arquivos, ajuste, e só então rode em todos. `--allowedTools` limita o que o Claude pode fazer quando ninguém está olhando.

### `/goal`: trabalhar até uma condição ser verdade

```text
/goal todos os testes em tests/Feature/Auth passam e o lint está limpo
```

Depois de cada turno, um modelo rápido avalia se a condição foi atingida; se não, o Claude continua sozinho. Boas condições têm **um estado final mensurável**, **como provar** ("`php artisan test` sai com 0") e **restrições** ("nenhum outro arquivo de teste muda"). Inclua um limite: "ou pare depois de 20 turnos". `/goal clear` cancela.

Combine com o auto mode para rodar sem pedir aprovação a cada ferramenta.

### Rodar em horários

- `/loop` repete um prompt num intervalo dentro da sessão.
- Tarefas agendadas (no app desktop e na nuvem) rodam independentes de uma sessão aberta: testes noturnos, triagem de manhã.
- Há integração oficial com **GitHub Actions** e GitLab CI para revisar PRs e responder `@claude` em issues.

## 13. Estilos de resposta (output styles)

Mudam **como** o Claude responde a sessão toda. Troque com `/output-style <nome>` ou `"outputStyle"` nas configurações.

| Estilo | O que muda | Use quando |
| --- | --- | --- |
| Default | Instruções padrão de engenharia | Normalmente |
| `Proactive` | Começa a trabalhar direto e assume decisões de rotina | Você quer menos perguntas |
| `Concise` | Respostas começam pelo resultado, sem narração | As respostas estão longas demais |
| `Explanatory` | Adiciona blocos "Insight" explicando as escolhas | Aprender uma base de código |
| `Learning` | Explica e deixa pedaços do código para **você** escrever (`TODO(human)`) | Praticar enquanto a tarefa anda |

> **Dica:** para quem está aprendendo, `Explanatory` e `Learning` são ótimos: você entrega a tarefa e entende o porquê de cada decisão.

Estilos personalizados ficam em `~/.claude/output-styles/` ou `.claude/output-styles/` (Markdown com frontmatter; use `keep-coding-instructions: true` para manter o comportamento de programador).

## 14. Qual recurso usar? (mapa de decisão)

Não configure tudo de uma vez. Adicione cada recurso quando o gatilho aparecer:

| Gatilho | Adicione |
| --- | --- |
| O Claude erra a mesma convenção ou comando duas vezes | Uma linha no **CLAUDE.md** |
| Você vive pedindo respostas mais curtas ou em outro formato | Um **output style** |
| Você digita o mesmo prompt para começar uma tarefa | Uma **skill** chamável (`/nome`) |
| Você cola o mesmo passo a passo pela terceira vez | Uma **skill** |
| Você copia dados de um sistema que o Claude não vê | Um servidor **MCP** |
| O Claude lê muitos arquivos só para achar onde algo é definido | Um plugin de **inteligência de código** |
| Uma tarefa paralela enche a conversa de saída inútil | Um **subagente** |
| Algo precisa acontecer toda vez, sem pedir | Um **hook** |
| Um segundo repositório precisa do mesmo setup | Um **plugin** |

### Custo de contexto de cada recurso

| Recurso | Quando carrega | Custo |
| --- | --- | --- |
| CLAUDE.md | Início da sessão, completo | Toda requisição |
| Regras com `paths` | Quando arquivos correspondentes são lidos | Só quando relevante |
| Skills | Descrição no início; conteúdo quando usada | Baixo (zero se `disable-model-invocation`) |
| MCP | Nomes das ferramentas no início; esquema sob demanda | Baixo até usar |
| Subagentes | Quando criados, em contexto separado | Isolado da conversa principal |
| Hooks | No evento, fora da conversa | Zero, a menos que devolvam texto |

### Parecidos, mas diferentes

- **Skill × Subagente:** skill é **conteúdo** que entra no contexto; subagente é um **trabalhador isolado** que devolve um resumo. Combinam: um subagente pode pré-carregar skills, e uma skill pode rodar num subagente com `context: fork`.
- **Hook × Skill:** hook **sempre** dispara e não pensa; skill é interpretada pelo Claude. Guardrail vai em hook; fluxo que exige raciocínio vai em skill.
- **MCP × Skill:** MCP dá **acesso**; skill dá **conhecimento** de como usar bem esse acesso.

## 15. Erros comuns (e como sair deles)

| Padrão | Sintoma | Solução |
| --- | --- | --- |
| Sessão "pia de cozinha" | Uma tarefa, depois outra sem relação, depois volta à primeira | `/clear` entre tarefas sem relação |
| Corrigir em círculos | Errou, você corrige, erra de novo | Depois de 2 correções: `/clear` e um prompt melhor |
| CLAUDE.md inchado | Regras importantes são ignoradas | Pode sem dó; o que ele já faz certo, apague ou vire hook |
| Confiar sem verificar | Parece certo, mas falha em casos de borda | Sempre dê verificação (teste, script, print). Se não dá para verificar, não entregue |
| Exploração infinita | "Investiga isso" e ele lê centenas de arquivos | Delimite a investigação ou use subagente |
| Aprovar no automático | Depois da décima aprovação você só clica "sim" | Configure `allow`/`deny`, use auto mode ou sandbox |

## 16. Atalhos e comandos essenciais

### Teclado

| Atalho | Faz |
| --- | --- |
| `Esc` | Interrompe o Claude (o contexto fica) |
| `Esc` `Esc` | Limpa o rascunho ou abre o rewind |
| `Shift+Tab` | Alterna modos de permissão (inclui plan mode) |
| `Ctrl+G` | Abre o prompt/plano no seu editor |
| `Ctrl+O` | Visualizador da transcrição (vê o raciocínio) |
| `Ctrl+R` | Busca no histórico de comandos |
| `Ctrl+B` | Manda tarefas em execução para segundo plano |
| `Ctrl+T` | Mostra/esconde a lista de tarefas do Claude |
| `Ctrl+V` (`Alt+V` no Windows) | Cola imagem da área de transferência |
| `Alt+P` / `Alt+T` / `Alt+O` | Troca modelo / pensamento estendido / modo rápido (`Option` no macOS) |
| `\` + `Enter` ou `Ctrl+J` | Nova linha no prompt |
| `?` (campo vazio) | Painel de atalhos |

### Prefixos no prompt

| Prefixo | Faz |
| --- | --- |
| `/` | Comando ou skill |
| `!` | Roda comando de shell e joga a saída na conversa |
| `@` | Menciona arquivo (autocomplete) |

### Comandos de barra

| Comando | Para quê |
| --- | --- |
| `/init` | Gera o CLAUDE.md inicial |
| `/memory` | Edita CLAUDE.md e memória automática |
| `/context` | Mostra o uso da janela de contexto |
| `/clear` | Conversa nova, contexto vazio |
| `/compact [instrução]` | Resume a conversa para liberar espaço |
| `/btw` | Pergunta paralela que não entra no histórico |
| `/rewind` | Volta código e/ou conversa a um checkpoint |
| `/resume`, `/rename`, `/branch` | Gerencia sessões |
| `/model`, `/effort`, `/fast` | Modelo, esforço, modo rápido |
| `/permissions` | Regras de permissão |
| `/hooks` | Vê os hooks configurados |
| `/mcp` | Servidores MCP e login |
| `/agents` | Ajuda com subagentes |
| `/plugin` | Instala e gerencia plugins |
| `/output-style` | Troca estilo de resposta |
| `/diff` | Revisa as mudanças |
| `/code-review`, `/security-review` | Revisão do diff |
| `/goal`, `/loop`, `/batch` | Automação e paralelismo |
| `/cost` (ou `/usage`) | Uso e custo |
| `/status` | Modelo, conta e configurações carregadas |
| `/doctor` | Diagnóstico do setup |
| `/config` | Configurações (tema, modelo, estilo...) |

## 17. Kit inicial pronto para copiar

Este repositório tem um kit em `starter-kit/` pensado para um projeto **Laravel + JavaScript**, mas fácil de adaptar. Copie para a raiz do seu projeto e ajuste.

```text
starter-kit/
├── CLAUDE.md                          # modelo enxuto de instruções do projeto
├── gitignore-adicionar.txt            # linhas para o seu .gitignore
├── usuario/settings.json              # exemplo para ~/.claude/settings.json (notificação no Windows)
└── .claude/
    ├── settings.json                  # permissões + hooks do projeto
    ├── hooks/
    │   ├── protect-files.mjs          # bloqueia .env, .git/, lockfiles, vendor/, node_modules/
    │   └── format.mjs                 # Pint para PHP, Prettier para JS/CSS (se instalados)
    ├── rules/testes.md                # regra que só carrega ao mexer em tests/
    ├── skills/
    │   ├── nova-feature/SKILL.md      # /nova-feature: explorar → planejar → implementar → verificar
    │   └── commit/SKILL.md            # /commit: revisa o diff e commita
    └── agents/revisor.md              # subagente revisor, só leitura, em plan mode
```

Os hooks são em **Node** (sem `jq`), então funcionam igual no Windows, macOS e Linux. Formatação nunca bloqueia; proteção de arquivos bloqueia com código de saída 2 e explica o motivo ao Claude.

**Como começar:**

1. Copie `starter-kit/CLAUDE.md` e a pasta `starter-kit/.claude/` para a raiz do projeto.
2. Adicione as linhas de `gitignore-adicionar.txt` ao seu `.gitignore`.
3. Edite o `CLAUDE.md` com a stack, comandos e pegadinhas **do seu projeto**. Apague o que não se aplica.
4. Abra o Claude Code e rode `/status`, `/hooks` e `/context` para confirmar que tudo carregou.
5. Teste: peça para o Claude editar o `.env` (deve ser bloqueado) e para editar um arquivo PHP (deve ser formatado).

## 18. Ensinando isto a uma sessão do Claude

Quer que o Claude aplique estas práticas num projeto seu? Mande um prompt assim:

```text
Leia o guia em https://raw.githubusercontent.com/HumbertoAlcantaraArruda/updates-claude-code/main/GUIA.md
e o kit em https://github.com/HumbertoAlcantaraArruda/updates-claude-code/tree/main/starter-kit.
Depois analise este projeto e proponha (sem aplicar ainda) um CLAUDE.md enxuto,
as regras de permissão e os hooks que fazem sentido aqui. Explique cada escolha.
```

Ou, para aprender junto:

```text
Mude para o output style Learning. Vamos implementar [tarefa] seguindo o fluxo
explorar → planejar → implementar → verificar do guia. Me deixe escrever as partes
com decisões de design.
```

## Fontes

Toda informação técnica deste guia foi conferida na documentação oficial do Claude Code em setembro de 2026. O Claude Code muda rápido: quando algo divergir, a documentação vence.

- [Boas práticas](https://code.claude.com/docs/en/best-practices)
- [Extend Claude Code: qual recurso usar](https://code.claude.com/docs/en/features-overview)
- [Memória e CLAUDE.md](https://code.claude.com/docs/en/memory)
- [Permissões](https://code.claude.com/docs/en/permissions) e [modos de permissão](https://code.claude.com/docs/en/permission-modes)
- [Configurações](https://code.claude.com/docs/en/settings)
- [Guia de hooks](https://code.claude.com/docs/en/hooks-guide) e [referência de hooks](https://code.claude.com/docs/en/hooks)
- [Skills](https://code.claude.com/docs/en/skills)
- [Subagentes](https://code.claude.com/docs/en/sub-agents)
- [MCP](https://code.claude.com/docs/en/mcp)
- [Plugins](https://code.claude.com/docs/en/plugins/overview)
- [Configuração de modelos](https://code.claude.com/docs/en/model-config)
- [Checkpoints](https://code.claude.com/docs/en/checkpointing)
- [Worktrees](https://code.claude.com/docs/en/worktrees)
- [Modo não interativo](https://code.claude.com/docs/en/headless)
- [/goal](https://code.claude.com/docs/en/goal)
- [Output styles](https://code.claude.com/docs/en/output-styles)
- [Modo interativo e atalhos](https://code.claude.com/docs/en/interactive-mode)
- [Comandos](https://code.claude.com/docs/en/commands)
- [Índice completo para LLMs (llms.txt)](https://code.claude.com/docs/llms.txt)
