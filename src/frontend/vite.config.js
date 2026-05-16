import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3001,
    host: true,
    proxy: {
      '/knowledge-base': 'http://localhost:8080',
      '/compare': 'http://localhost:8080',
      '/health': 'http://localhost:8080',
      '/ingest': 'http://localhost:8080',
      '/metrics': 'http://localhost:8080',
    },
  },
})
