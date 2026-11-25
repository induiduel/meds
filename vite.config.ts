import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { fileURLToPath } from 'url';
import { defineConfig, type Plugin } from 'vite';
import dotenv from 'dotenv';
import { splitLearningDecks } from './scripts/altyapi/vite/splitLearningDecks.ts';
import { surumDosyasi } from './scripts/altyapi/vite/surumDosyasi.ts';
import { cevrimdisiManifest } from './scripts/altyapi/vite/cevrimdisiManifest.ts';
import { yonetimGirisi } from './scripts/altyapi/vite/yonetimGirisi.ts';

dotenv.config();

const __dirname = fileURLToPath(new URL('.', import.meta.url));

function parcaAdi(id: string): string | null {
  const normalized = id.replace(/\\/g, '/');

  // 1. External Vendor Code Splitting
  if (normalized.includes('node_modules')) {
    // Yalnız paket kökleri: '/react-dom/' eşleşmesi @floating-ui/react-dom'u ve react-dom/server'ı (yalnız PDF
    // dışa aktarımında gereken ~75 KB gzip) her sayfanın açılış parçasına sokuyordu (H131a).
    if (
      (/\/node_modules\/(react|react-dom|scheduler)\//.test(normalized)) &&
      !/\/react-dom\/(server|cjs\/react-dom-server|static)/.test(normalized)
    ) {
      return 'vendor-react';
    }
    if (normalized.includes('/@google/genai/')) {
      return 'vendor-genai';
    }
    if (normalized.includes('/@tanstack/')) {
      return 'vendor-tanstack';
    }
    // jspdf/html2canvas yalnızca PDF dışa aktarırken dinamik yüklenir; elle gruplanınca
    // ortak yardımcılar bu parçaya düşüp her sayfada 600 KB yükleniyordu.
    if (normalized.includes('/motion/') || /\/node_modules\/(motion-dom|motion-utils)\//.test(normalized)) {
      return 'vendor-motion';
    }
    if (normalized.includes('/lucide-react/')) {
      return 'vendor-lucide';
    }
  }

  // 2. Local Application Code Splitting (Local Chunklama)
  if (normalized.endsWith('/src/data/bundledScripts.ts')) return 'admin-bundled-scripts';
  if (normalized.includes('/src/data/summaries/')) {
    const match = normalized.match(/kurul\d+/);
    if (match) {
      return `local-data-summaries-${match[0]}`;
    }
  }
  if (normalized.includes('/src/data/kazanimlar/lite/')) {
    // Kurul başına parça: ekran yalnız seçili kurulun lite/k<N>.json'unu ister; eskiden 6 kurul tek parçaydı (3,4 MB).
    const match = normalized.match(/\/lite\/(k\d+)\.json/);
    return match ? `local-data-kazanimlar-lite-${match[1]}` : 'local-data-kazanimlar-lite';
  }
  if (normalized.includes('/src/data/kazanimlar/questions/')) {
    // Konu başına parça (questions/k<N>/d<i>-k<j>.json, _dizin.json): her dosya kendi parçası kalır;
    // kurulu tek parçada toplamak K1'de ≈31 MB tek indirme demekti.
    const parca = normalized.match(/\/questions\/(k\d+)\/([\w-]+)\.json/);
    if (parca) return `local-data-kazanimlar-q-${parca[1]}-${parca[2].replace(/^_/, '')}`;
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
  return null;
}

/**
 * v16 ikon seti (docs/V16_PLAN.md): uygulamanın `lucide-react` içe aktarmaları src/components/v16/lucideV16.ts'e yönlenir;
 * o modül v16 açıkken eşlenen ikonları tuval setiyle çizer, gerisini lucide'den aynen geçirir. Ara modülün kendi isteği gerçek pakete.
 */
function v16LucideEklentisi(): Plugin {
  const ara = path.resolve(__dirname, 'src/components/v16/lucideV16.ts');
  return {
    name: 'v16-lucide',
    enforce: 'pre',
    resolveId(id, importer) {
      if (id !== 'lucide-react' || !importer) return null;
      if (path.resolve(importer.split('?')[0]) === ara) return null;
      return ara;
    },
  };
}

export default defineConfig(({ mode }) => {
  return {
    base: process.env.VITE_BASE || '/',
    plugins: [v16LucideEklentisi(), splitLearningDecks(__dirname), surumDosyasi(__dirname), cevrimdisiManifest(__dirname), yonetimGirisi(), react(), tailwindcss()],
    resolve: {
      alias: [
        { find: '@', replacement: path.resolve(__dirname, '.') },
      ],
    },
    // Yazım yardımcısı işçisi (src/workers/composerWorker.ts) modeli dinamik içe aktarır: es biçimi gerekli
    worker: { format: 'es' as const },
    build: {
      target: 'es2022',
      cssCodeSplit: true,
      // Hız (2026-11-17): esbuild küçültücü Vite 8/rolldown'da yerel oxc'den ~2× yavaş ve daha büyük çıktı veriyordu
      // (vendor-react gzip 68,6 → 67,5 KB). 2600+ parçanın gzip boyutunu tek tek hesaplamak da ~15 sn sürüyordu.
      minify: 'oxc',
      reportCompressedSize: false,
      emptyOutDir: false,
      // dist/.vite/manifest.json: sunucu eski hash'li parçaları budarken güncel kümeyi buradan okur (server.ts pruneDistAssets)
      manifest: true,
      // Büyük parçalar tembel veri (diseases/glossary/ansiklopedi JSON'u); kod parçası bu sınıra yaklaşmaz.
      chunkSizeWarningLimit: 5000,
      rolldownOptions: {
        // lottie-web kendi içinde doğrudan eval kullanır (değiştiremeyiz); sql.js'in node modülleri tarayıcıda zaten kullanılmaz.
        checks: { eval: false },
        onLog(level, log, handler) {
          if (/has been externalized for browser compatibility/.test(log.message || '') && /sql\.js/.test(log.message || '')) return;
          handler(level, log);
        },
        // Yönetim ayrı girişi (2026-10-28): /manage öğrenci uygulamasının ortak girişini yüklemez (src/manage-main.tsx)
        input: { index: path.resolve(__dirname, 'index.html'), manage: path.resolve(__dirname, 'manage.html') },
        output: {
          chunkFileNames: 'assets/chunk-[name]-[hash].js',
          entryFileNames: 'assets/entry-[name]-[hash].js',
          assetFileNames: 'assets/asset-[name]-[hash].[ext]',
          // manualChunks yerine codeSplitting (2026-11-17): tek ad işlevli grupta rolldown yakalanan modülün bağımlılıklarını
          // da aynı gruba çeker; react çekirdeği vendor-lucide'a, jsx-runtime vendor-motion'a düşüyor ve iki paket her
          // sayfanın açılış zincirine giriyordu. React grubu daha yüksek öncelikle önce yakalar.
          codeSplitting: { groups: [
            {
              name: 'vendor-react',
              priority: 30,
              test: (id: string) => /\/node_modules\/(react|react-dom|scheduler)\//.test(id.replace(/\\/g, '/')) &&
                !/\/react-dom\/(server|cjs\/react-dom-server|static)/.test(id.replace(/\\/g, '/')),
            },
            // Açılış zincirindeki ikonlar ayrı küçük parçada; kalan ~ikonlar yalnız tembel ekran açılınca iner.
            { name: 'vendor-lucide-ilk', priority: 20, tags: ['$initial'], test: /[\\/]node_modules[\\/]lucide-react[\\/]/ },
            { name: (id: string) => parcaAdi(id), debugName: 'parcaAdi' },
          ] },
        },
      },
    },
    preview: {
      proxy: { '/api': { target: 'http://localhost:3000', changeOrigin: true, ws: true } },
    },
    server: {
      port: 5174,
      proxy: {
        '/api': {
          target: 'http://localhost:3000',
          changeOrigin: true,
          // Oyunlar: /api/quiz/ws websocket'i de geçsin
          ws: true,
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
