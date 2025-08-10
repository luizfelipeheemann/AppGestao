import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // Esta é a configuração que resolve o erro.
      // Ela diz ao Vite que "@" é um atalho para a pasta "src".
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
