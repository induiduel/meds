/**
 * AB16 sınaması: bilinen her rota (ROUTE_PATHS iç adresi, görünen adresi ve takma adlar) 404'e düşmemeli;
 * '/' ana sayfa davranışı korunmalı; uydurma yollar 'bulunamadi' olmalı. Çalıştır: npx tsx scripts/eval/rota-404.mts
 */
import { ROUTE_PATHS, ALIASES, parseLocation, pathFor, type AppRoute } from '../../src/router';
import { KATEGORILER } from '../../src/siteHaritasi';

let hata = 0, sayi = 0;
const p = (yol: string) => { const u = new URL(yol, 'https://x.invalid'); return parseLocation({ pathname: u.pathname, search: u.search, hash: u.hash }); };
const bekle = (yol: string, ok: (r: AppRoute) => boolean, not: string) => {
  sayi++;
  const r = p(yol).route;
  if (!ok(r)) { hata++; console.log(`HATA ${yol} → ${r} (${not})`); }
};
for (const [r, ic] of Object.entries(ROUTE_PATHS) as [AppRoute, string][]) {
  if (r === 'bulunamadi') continue;
  bekle(ic, (x) => x !== 'bulunamadi', 'iç adres');
  bekle(pathFor(r), (x) => x !== 'bulunamadi', 'görünen adres');
}
for (const k of Object.keys(ALIASES)) bekle('/' + k, (x) => x !== 'bulunamadi', 'takma ad');
for (const k of KATEGORILER as unknown as { yol?: string; id?: string }[]) if (k.yol) bekle(k.yol, (x) => x !== 'bulunamadi', 'kategori');
for (const y of ['/kamplar/kurul1/checkup/tbg/v1/soru-coz', '/kamplar/kurul1/cikmis-cozucu', '/dersler/program/ekle', '/sorular/cikmis', '/kaynaklar/sozluk', '/genetik-check-up', '/spotlar?gorunum=onem', '/spotlar?gorunum=cozucu', '/topluluk?gorunum=sohbetler', '/notlarim?gorunum=paylasilan'])
  bekle(y, (x) => x !== 'bulunamadi', 'derin / eski adres');
bekle('/', (x) => x === 'quick_add', 'kök varsayılan');
bekle('/#bugun', (x) => x === 'today', 'eski #sekme');
bekle('/#olmayan-sekme', (x) => x === 'quick_add', 'kökte bilinmeyen sekme varsayılana düşer');
bekle('/meds', (x) => x === 'quick_add', '/meds öneki');
bekle('/?questionId=abc', (x) => x === 'past_exams', 'eski paylaşım');
for (const y of ['/boyle-bir-sayfa-yok', '/xyz/abc', '/dersler-yok', '/meds/olmayan']) bekle(y, (x) => x === 'bulunamadi', 'bilinmeyen');
console.log(`${sayi} adres sınandı, ${hata} HATA`);
process.exit(hata ? 1 : 0);
