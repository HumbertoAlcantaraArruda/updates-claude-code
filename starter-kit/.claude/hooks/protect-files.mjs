#!/usr/bin/env node
// Hook PreToolUse (Edit|Write): bloqueia edição de arquivos sensíveis.
// Claude Code manda um JSON no stdin. Sair com código 2 BLOQUEIA a ação,
// e o texto no stderr volta para o Claude como explicação.
// Feito em Node (sem jq) para funcionar igual no Windows, macOS e Linux.

import { readFileSync } from "node:fs";
import { basename } from "node:path";

let input = {};
try {
  input = JSON.parse(readFileSync(0, "utf8"));
} catch {
  process.exit(0); // sem JSON válido: não decide nada, segue o fluxo normal
}

const raw = input?.tool_input?.file_path ?? "";
const filePath = raw.replaceAll("\\", "/"); // normaliza caminhos do Windows
const name = basename(filePath);

const blocked = [
  // .env e variações (.env.local, .env.production), mas libera .env.example
  () => name.startsWith(".env") && name !== ".env.example",
  () => filePath.includes("/.git/"),
  () => name === "composer.lock",
  () => name === "package-lock.json",
  () => filePath.includes("/vendor/"),
  () => filePath.includes("/node_modules/"),
];

if (blocked.some((rule) => rule())) {
  console.error(
    `Bloqueado pelo hook protect-files: "${raw}" é um arquivo protegido. ` +
      `Se a mudança for mesmo necessária, peça para o usuário fazer manualmente.`
  );
  process.exit(2);
}

process.exit(0);
