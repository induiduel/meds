/**
 * Sayfa → çevrimdışı paketleri: bulunulan ekranın internetsiz tam çalışması için cihazda olması gereken paketler.
 * Üst çubuktaki bulut simgesi (OfflineStatusBadge) ve Çevrimdışı merkezindeki "Bu sayfa" kartı (?sayfa=) kullanır.
 * Belirli bir öge açıksa (ders, sesli ders, çözücü dersi) yalnız o; liste ekranında o listenin tüm paketleri.
 * Uygulama paketi motor tarafından her zaman eklenir; bağımlılar (`bagimli`) kuyruğa girerken eklenir.
 */
import type { Paket } from './paketMotoru';
import { icYol } from '../../siteHaritasi';

export function sayfaPaketleri(adres: string, katalog: Paket[]): string[] {
  let u: URL;
  try { u = new URL(icYol(adres), 'http://x'); } catch { return []; }
  const yol = u.pathname.replace(/\/+$/, '') || '/';
  const q = (k: string) => u.searchParams.get(k) || '';
  const var_ = new Set(katalog.map((p) => p.id));
  const onek = (o: string) => katalog.filter((p) => p.id.startsWith(o)).map((p) => p.id);
  const tek = (...ids: string[]) => ids.filter((id) => var_.has(id) || id.startsWith('sesli:') || id === 'db:sorular');
  const brans = q('brans') || 'patoloji';

  let m: RegExpMatchArray | null;
  if ((m = yol.match(/^\/ogren\/(.+)$/))) return tek(`ogren:${decodeURIComponent(m[1])}`);
  if (yol === '/ogren') return onek('ogren:');
  if ((m = yol.match(/^\/canliders\/(.+)$/))) return [`sesli:${decodeURIComponent(m[1])}`];
  if (yol === '/canliders') return onek('sesli:');
  if (yol === '/soru-cozucu') return q('ders') ? tek(`cozucu:${brans}:${q('ders')}`) : onek(`cozucu:${brans}:`);
  // Çıkmış çözücü: paket soruları branşın çözücü derslerinden gelir → branşın tüm çözücü paketleri
  if (yol === '/cikmis-cozucu') return q('brans') ? onek(`cozucu:${q('brans')}:`) : onek('cozucu:');
  if (yol === '/en-onemliler') return q('ders') ? tek(`onem:${brans}:${q('ders')}`) : onek(`onem:${brans}:`);
  if (yol === '/alternatif-cozucu') return q('ders') ? tek(`alt:${q('ders')}`) : onek('alt:');
  if (yol === '/kamp' || yol.startsWith('/kamp/')) return onek('kamp:');
  if (yol === '/genetik-check-up') return tek('sayfa:tbg-kampi');
  // Son Prova: part sayfası yalnız o partın paketi (sesli özet bağımlı), deneme/genel → deneme paketi, liste → hepsi
  if (yol === '/son-prova' || yol.startsWith('/son-prova/')) {
    const p = yol.split('/').slice(2);
    const kurul = q('kurul') || '1';
    if (p[0] === 'deneme' || p[1] === 'genel') return tek(`sonprova:k${kurul}:deneme`);
    const partlar = katalog.filter((x) => x.id.startsWith(`sonprova:k${kurul}-`) && x.id.includes(`-son-prova-${(p[0] || '').replace(/(halk)(sagligi)/, '$1-$2').replace(/(kadin)(dogum)/, '$1-$2')}`));
    if (p[0] && p[1]) {
      const no = Number(p[1]) || 1;
      const hit = partlar.find((x) => x.id.endsWith(`-${no}`)) || (partlar.length === 1 ? partlar[0] : undefined);
      return hit ? [hit.id] : [];
    }
    return p[0] ? partlar.map((x) => x.id) : onek('sonprova:');
  }
  const SABIT: Record<string, string[]> = {
    '/cikmis': ['db:sorular'], '/test': ['db:sorular'], '/sorular': ['db:sorular'], '/havuz': ['db:sorular'], '/calis': ['db:sorular', 'veri:spot'],
    '/sozluk': ['veri:sozluk'], '/hastaliklar': ['veri:sozluk'], '/kartlar': ['veri:spot'], '/spotlar': ['veri:spot'],
    '/ozetler': ['veri:ozet'], '/notlar': ['veri:notlar'], '/kazanimlar': ['veri:kazanim'], '/sinav-calisma': ['veri:sinav'],
    '/ornek-sorular': ['veri:ornek'], '/saglik': ['veri:saglik'], '/olasi-sorular': ['veri:olasi'],
    '/ara': ['db:sorular', 'veri:sozluk'],
  };
  const k = Object.keys(SABIT).find((x) => yol === x || yol.startsWith(`${x}/`));
  return k ? tek(...SABIT[k]) : [];
}
