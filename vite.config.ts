import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { fileURLToPath } from 'url';
import { defineConfig } from 'vite';
import dotenv from 'dotenv';

dotenv.config();

const __dirname = fileURLToPath(new URL('.', import.meta.url));

export default defineConfig(({ mode }) => {
  const isGhPages =
    process.env.BUILD_TARGET === 'gh-pages' ||
    process.env.npm_lifecycle_event === 'build:gh-pages' ||
    process.env.npm_lifecycle_event === 'predeploy';

  return {
    base: process.env.VITE_BASE || '/',
    plugins: [react(), tailwindcss()],
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
              if (
                normalized.includes('/jspdf/') ||
                normalized.includes('/html2canvas/') ||
                normalized.includes('/dompurify/')
              ) {
                return 'vendor-pdf';
              }
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
        ignored: ['**/data/**', '**/dist/**', '**/scripts/**', '**/.agents/**', '**/node_modules/**'],
      },
      allowedHosts: true,
    },
  };
});
