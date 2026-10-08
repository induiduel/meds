import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { fileURLToPath } from 'url';
import { defineConfig } from 'vite';
import dotenv from 'dotenv';
import { splitLearningDecks } from './scripts/vite/splitLearningDecks';

dotenv.config();

const __dirname = fileURLToPath(new URL('.', import.meta.url));

export default defineConfig(({ mode }) => {
  const isGhPages =
    process.env.BUILD_TARGET === 'gh-pages' ||
    process.env.npm_lifecycle_event === 'build:gh-pages' ||
    process.env.npm_lifecycle_event === 'predeploy';

  return {
    base: process.env.VITE_BASE || (isGhPages ? '/meds/' : '/'),
    plugins: [splitLearningDecks(__dirname), react(), tailwindcss()],
    define: {
      'process.env.SUPABASE_URL': JSON.stringify(process.env.SUPABASE_URL || 'https://kgutsltgmqbnlxcnzrtl.supabase.co'),
      'process.env.SUPABASE_PUBLISHABLE_KEY': JSON.stringify(process.env.SUPABASE_PUBLISHABLE_KEY || 'sb_publishable_EVdXdIi_2mxVr3HZKYabwQ_li5KuE1Q'),
      'process.env.SUPABASE_KEY': JSON.stringify(process.env.SUPABASE_PUBLISHABLE_KEY || 'sb_publishable_EVdXdIi_2mxVr3HZKYabwQ_li5KuE1Q'),
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.'),
      },
    },
    build: {
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
              if (normalized.includes('/@supabase/')) {
                return 'vendor-supabase';
              }
              if (normalized.includes('/@google/genai/')) {
                return 'vendor-genai';
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
