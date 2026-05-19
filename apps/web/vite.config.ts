import path from "node:path";
import { fileURLToPath } from "node:url";

import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const currentDir = path.dirname(fileURLToPath(import.meta.url));
  const repoRoot = path.resolve(currentDir, "../..");
  const env = loadEnv(mode, repoRoot, "");

  return {
    plugins: [react()],
    define: {
      __WEB_API_BASE_URL__: JSON.stringify(
        env.WEB_API_BASE_URL || "http://localhost:8000",
      ),
    },
  };
});
