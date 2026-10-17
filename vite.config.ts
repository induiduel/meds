import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { fileURLToPath } from 'url';
import { defineConfig } from 'vite';
import dotenv from 'dotenv';
import { splitLearningDecks } from './scripts/vite/splitLearningDecks';
import { surumDosyasi } from './scripts/vite/surumDosyasi';

dotenv.config();

const __dirname = fileURLToPath(new URL('.', import.meta.url));

export default defineConfig(({ mode }) => {
  return {
    base: process.env.VITE_BASE || '/',
    plugins: [splitLearningDecks(__dirname), surumDosyasi(__dirname), react(), tailwindcss()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.'),
      },
    },
    // Yazım yardımcısı işçisi (src/workers/composerWorker.ts) modeli dinamik içe aktarır: es biçimi gerekli
    worker: { format: 'es' as const },
    build: {
      target: 'es2022',
      cssCodeSplit: true,
      minify: 'esbuild',
      emptyOutDir: false,
      chunkSizeWarningLimit: 2500,
      rollupOptions: {
        output: {
          chunkFileNames: 'assets/chunk-[name]-[hash].js',
          entryFileNames: 'assets/entry-[name]-[hash].js',
          assetFileNames: 'assets/asset-[name]-[hash].[ext]',
          manualChunks(id) {
            const normalized = id.replace(/\\/g, '/');

            // 1. External Vendor Code Splitting
            if (normalized.includes('node_modules')) {
              if (
                normalized.includes('/react/') ||
                normalized.includes('/react-dom/') ||
                normalized.includes('/scheduler/')
              ) {
                return 'vendor-react';
              }
              if (
                normalized.includes('/firebase/') ||
                normalized.includes('/@firebase/')
              ) {
                return 'vendor-firebase';
              }
              if (normalized.includes('/@google/genai/')) {
                return 'vendor-genai';
              }
              if (normalized.includes('/@tanstack/')) {
                return 'vendor-tanstack';
              }
              // jspdf/html2canvas yalnızca PDF dışa aktarırken dinamik yüklenir; elle gruplanınca
              // ortak yardımcılar bu parçaya düşüp her sayfada 600 KB yükleniyordu.
              if (normalized.includes('/motion/')) {
                return 'vendor-motion';
              }
              if (normalized.includes('/lucide-react/')) {
                return 'vendor-lucide';
              }
            }

            // 2. Local Application Code Splitting (Local Chunklama)
            if (normalized.includes('/src/data/summaries/')) {
              const match = normalized.match(/kurul\d+/);
              if (match) {
                return `local-data-summaries-${match[0]}`;
              }
            }
            if (normalized.includes('/src/data/kazanimlar/lite/')) {
              return 'local-data-kazanimlar-lite';
            }
            if (normalized.includes('/src/data/kazanimlar/questions/')) {
              const match = normalized.match(/k\d+/);
              if (match) {
                return `local-data-kazanimlar-q-${match[0]}`;
              }
            }
            if (normalized.includes('/src/data/kazanimlar/')) {
              const match = normalized.match(/k\d+/);
              if (match) {
                return `local-data-kazanimlar-${match[0]}`;
              }
            }
          },
        },
      },
    },
    preview: {
      proxy: { '/api': { target: 'http://localhost:3000', changeOrigin: true } },
    },
    server: {
      port: 5174,
      proxy: {
        '/api': {
          target: 'http://localhost:3000',
          changeOrigin: true,
        },
      },
      // HMR kapalı (iframe önizleme), ama dosya izleme açık: yoksa Vite ilk
      // dönüştürdüğü modülü önbellekte tutar ve yenilemede eski kod gelir.
      hmr: false,
      watch: {
        ignored: ['**/.venv*/**', '**/__pycache__/**', '**/data/**', '**/dist/**', '**/scripts/**', '**/.agents/**', '**/node_modules/**'],
      },
      allowedHosts: true,
    },
  };
});
