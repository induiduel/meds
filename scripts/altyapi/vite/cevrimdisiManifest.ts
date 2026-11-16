import path from 'path';
import type { Plugin } from 'vite';

/**
 * Çevrimdışı manifesti: derlemenin hangi dosyalarının uygulama kodu, hangilerinin ders verisi olduğunu dist/cevrimdisi-manifest.json'a yazar.
 *  - `kod`: giriş, kod parçaları, CSS, işçi ve yazı tipi dosyaları (çevrimdışı modda hep cihazda tutulur; "Uygulama" paketi).
 *  - `veri`: yalnız src/data altındaki JSON'lardan oluşan parçalar → kaynak yolu (src/… göreli) → [parça, bağımlı parçalar…].
 * Sunucu (src/services/cevrimdisiKatalog.ts) paketleri bu dosyadan kurar; parça adı içerik özetli olduğundan veri değişince adres de değişir
 * ve cihazdaki paket "güncelleme var" görünür. emptyOutDir kapalı (eski parçalar dist'te kalır): yalnız bu manifestteki dosyalar geçerlidir.
 */
export function cevrimdisiManifest(root: string): Plugin {
  return {
    name: 'meds-cevrimdisi-manifest',
    apply: 'build',
    generateBundle(_opts, bundle) {
      const src = path.join(root, 'src') + path.sep;
      const veriModulu = (id: string) => {
        const n = id.split('?')[0];
        return n.startsWith(src) && n.endsWith('.json');
      };
      const kod: string[] = [];
      const veri: Record<string, string[]> = {};
      const parcalar = new Map<string, any>();
      for (const [ad, c] of Object.entries(bundle)) if (c.type === 'chunk') parcalar.set(ad, c);
      const veriParcasi = (c: any) => c.moduleIds.length > 0 && c.moduleIds.every(veriModulu);
      // Veri parçasının statik bağımlılıkları (JSON parçaları kendi başına yetmeyebilir)
      const bagimli = (ad: string, out: Set<string>) => {
        const c = parcalar.get(ad);
        if (!c || out.has(ad)) return;
        out.add(ad);
        for (const i of c.imports) bagimli(i, out);
      };
      for (const [ad, c] of Object.entries(bundle)) {
        if (c.type === 'asset') {
          if (/\.(css|woff2?|ttf|otf|wasm|svg|png|jpe?g|webp|mjs|js)$/i.test(ad)) kod.push(ad);
          continue;
        }
        if (!veriParcasi(c)) {
          kod.push(ad);
          for (const css of (c as any).viteMetadata?.importedCss || []) kod.push(css);
          continue;
        }
        const set = new Set<string>();
        bagimli(ad, set);
        const dosyalar = [ad, ...[...set].filter((x) => x !== ad && veriParcasi(parcalar.get(x)))];
        for (const m of c.moduleIds) {
          const rel = path.relative(root, m.split('?')[0]).split(path.sep).join('/');
          veri[rel] = dosyalar;
        }
      }
      this.emitFile({
        type: 'asset',
        fileName: 'cevrimdisi-manifest.json',
        source: JSON.stringify({ olusturma: new Date().toISOString(), kod: [...new Set(kod)].sort(), veri }),
      });
    },
  };
}
