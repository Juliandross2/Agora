import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    minify: true, // Usa el minificador por defecto de Vite (esbuild)
    rollupOptions: {
      output: {
        manualChunks: (id) => {
          // Vendor chunks
          if (id.includes('node_modules/react') || id.includes('node_modules/react-dom')) {
            return 'react-vendor';
          }
          if (id.includes('node_modules/react-router')) {
            return 'router-vendor';
          }
          if (id.includes('node_modules/notistack')) {
            return 'notistack-vendor';
          }
          if (id.includes('node_modules/@hello-pangea')) {
            return 'dnd-vendor';
          }
          if (id.includes('node_modules/lucide')) {
            return 'icons-vendor';
          }
          if (id.includes('node_modules/xlsx') || id.includes('node_modules/jspdf') || id.includes('node_modules/html2canvas')) {
            return 'export-vendor';
          }
          
          // App code chunks
          if (id.includes('src/pages')) {
            return 'pages';
          }
          if (id.includes('src/components')) {
            return 'components';
          }
          if (id.includes('src/services')) {
            return 'services';
          }
        },
      },
    },
    chunkSizeWarningLimit: 1000,
  },
})