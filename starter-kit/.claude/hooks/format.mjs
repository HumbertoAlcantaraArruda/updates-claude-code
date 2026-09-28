#!/usr/bin/env node
// Hook PostToolUse (Edit|Write): formata o arquivo que o Claude acabou de editar.
//   .php                          -> Laravel Pint (vendor/bin/pint)
//   .js .ts .vue .css .json ...   -> Prettier (node_modules/prettier)
// Se a ferramenta não estiver instalada no projeto, não faz nada.
// Nunca bloqueia (sempre sai com 0): formatação é conveniência, não regra.

import { readFileSync, existsSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { extname, join } from "node:path";

let input = {};
try {
  input = JSON.parse(readFileSync(0, "utf8"));
} catch {
  process.exit(0);
}

const file = input?.tool_input?.file_path;
const root = process.env.CLAUDE_PROJECT_DIR || input?.cwd || process.cwd();
if (!file || !existsSync(file)) process.exit(0);

const ext = extname(file).toLowerCase();
const run = (cmd, args) =>
  spawnSync(cmd, args, { cwd: root, stdio: "ignore", timeout: 50_000 });

if (ext === ".php") {
  const pint = join(root, "vendor", "bin", "pint");
  if (existsSync(pint)) run("php", [pint, file]);
} else if (
  [".js", ".mjs", ".cjs", ".ts", ".jsx", ".tsx", ".vue", ".css", ".scss", ".json", ".md"].includes(ext)
) {
  const prettier = join(root, "node_modules", "prettier", "bin", "prettier.cjs");
  if (existsSync(prettier)) run(process.execPath, [prettier, "--write", file]);
}

process.exit(0);
