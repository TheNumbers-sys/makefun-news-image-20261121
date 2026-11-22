import { copyFileSync, mkdirSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

const outputDir = resolve(process.env.MAKEFUN_OUTPUT_DIR || "/output");
const entryPath = resolve(fileURLToPath(new URL(".", import.meta.url)), "entry.png");
mkdirSync(outputDir, { recursive: true });
copyFileSync(entryPath, resolve(outputDir, "entry.png"));
