/**
 * Düz Okey motor sınaması: `npx tsx src/services/masa/motor/duzOkey.sinama.ts` (hata → çıkış ≠ 0).
 * Birim sınamaları (çek/at, bitir doğrulaması, puan çarpanları, gösterge, deste sonu) + tohumlu bot benzetimi.
 */
import assert from 'node:assert/strict';
import type { ElSonuc, OkeyGorunum, Renk, Tas } from '../tipler';
import { bitisBul, duzMotor as M, tamBol, yediCift, type DuzDurum } from './duzOkey';

const tohum = (a: number) => () => {
  a = (a + 0x6d2b79f5) | 0;
  let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
const T = (s: number, r: number, k = 0): Tas => ({ id: r * 26 + (s - 1) * 2 + k, s, r: r as Renk });
const OK = { s: 5, r: 3 as Renk };
const J = (k = 0) => T(5, 3, k);
const AD = ['a', 'b', 'c', 'd'];
const rng0 = tohum(1);
let sayac = 0;
const bolum = (ad: string, f: () => void) => { f(); sayac++; console.log(`  ✓ ${ad}`); };
const kur = (eller: Tas[][], ek: Partial<DuzDurum> = {}): DuzDurum => ({
  tur: 'duz', elNo: 1, sira: 0, deste: [T(1, 3), T(2, 3)], gosterge: T(4, 3), okey: OK, cekti: true, sonuc: null,
  oyuncular: eller.map((el, i) => ({ id: AD[i], el, atiklar: [], cezalar: [], attiMi: false, gosterdi: false })), ...ek,
});
function oyna(d: DuzDurum, o: string, h: unknown): DuzDurum {
  const once = JSON.stringify(d);
  const r = M.uygula(d, o, h, rng0);
  assert.equal(JSON.stringify(d), once, 'uygula girdiyi değiştirdi');
  assert.ok(!('hata' in r), `beklenmeyen hata: ${'hata' in r ? r.hata : ''}`);
  return (r as { durum: DuzDurum }).durum;
}
const hata = (d: DuzDurum, o: string, h: unknown, ic: string) => { const r = M.uygula(d, o, h, rng0); assert.ok('hata' in r && r.hata.includes(ic), JSON.stringify(r).slice(0, 200)); };
// 14 taş: 1-2-3 kırmızı, 4-5-6-7 siyah, 9 grup (3), 11-12-13 mavi + okey yerine
const BITEN = [T(1, 0), T(2, 0), T(3, 0), T(4, 1), T(5, 1), T(6, 1), T(7, 1), T(9, 0), T(9, 1), T(9, 2), T(11, 2), T(12, 2), J(), T(10, 2)];

console.log('Birim sınamaları');
bolum('tam bölme ve 7 çift', () => {
  const b = tamBol(BITEN.slice(0, 13), OK);
  assert.ok(b && b.flat().length === 13);
  assert.equal(tamBol([...BITEN.slice(0, 12), T(10, 0)], OK), null);
  const cift = [1, 2, 3, 4, 5, 6].flatMap((s) => [T(s, 0), T(s, 0, 1)]);
  assert.ok(yediCift([...cift, T(8, 1), J()], OK));
  assert.equal(yediCift([...cift, T(8, 1), T(9, 1)], OK), null);
  assert.equal(bitisBul(BITEN.concat(T(13, 0)), OK)?.tas, T(13, 0).id);
  assert.equal(bitisBul([...BITEN.slice(0, 13), T(10, 0), T(13, 1)], OK), null);
});
bolum('çek / at / sıra / yandan', () => {
  const d = kur([[...BITEN.slice(0, 14), T(13, 1)], BITEN.slice(0, 14).map((t) => ({ ...t, id: t.id ^ 1 }))]);
  hata(d, 'a', { t: 'cek' }, 'zaten');
  const d2 = oyna(d, 'a', { t: 'at', tas: T(13, 1).id });
  assert.equal(d2.sira, 1); assert.equal(d2.cekti, false);
  hata(d2, 'b', { t: 'at', tas: d2.oyuncular[1].el[0].id }, 'Önce taş çek');
  const d3 = oyna(d2, 'b', { t: 'cek', kaynak: 'atik' });
  assert.equal(d3.oyuncular[1].el.length, 15); assert.equal(d3.oyuncular[0].atiklar.length, 0);
  const g = M.gorunum(d3, 'a') as OkeyGorunum;
  assert.equal(g.elim.length, 14); assert.equal(g.oyuncular[1].tasSayisi, 15);
});
bolum('bitir: doğrulama ve puan çarpanları', () => {
  const el = [...BITEN, T(13, 1)];
  const d = kur([el, [T(1, 1)]]);
  const b = bitisBul(el, OK)!;
  hata(d, 'a', { t: 'bitir', tas: T(13, 1).id, gruplar: [b.gruplar.flat()] }, 'bitmiyor');
  hata(d, 'a', { t: 'bitir', tas: T(13, 1).id, gruplar: b.gruplar.slice(1) }, '14 taşın');
  const s = M.sonuc(oyna(d, 'a', { t: 'bitir', tas: b.tas, gruplar: b.gruplar })) as ElSonuc;
  assert.equal(s.satirlar[0].puan, 0); assert.equal(s.satirlar[1].puan, -2);
  // okey atarak: 13 taş + okey yerine gerçek taş
  const el2 = [...BITEN.slice(0, 12), T(13, 2), T(10, 2), J()];
  const b2 = bitisBul(el2, OK)!;
  assert.equal(b2.tas, J().id, 'okey atarak bitmek öncelikli');
  assert.equal((M.sonuc(oyna(kur([el2, [T(1, 1)]]), 'a', { t: 'bitir', ...b2 })) as ElSonuc).satirlar[1].puan, -4);
  const cift = [1, 2, 3, 4, 5, 6, 7].flatMap((s) => [T(s, 0), T(s, 0, 1)]);
  const el3 = [...cift.slice(0, 13), J(), J(1)];
  const b3 = bitisBul(el3, OK)!;
  assert.equal(b3.tas, J().id);
  assert.equal((M.sonuc(oyna(kur([el3, [T(1, 1)], [T(2, 1)]]), 'a', { t: 'bitir', ...b3 })) as ElSonuc).satirlar[2].puan, -8);
});
bolum('gösterge (bir kez, ilk tur) ve deste sonu', () => {
  const d = kur([[T(4, 3), T(1, 0)], [T(2, 0)], [T(3, 0)]]);
  hata(kur([[T(1, 0)], [T(2, 0)]]), 'a', { t: 'goster' }, 'aynısı yok');
  const d2 = oyna(d, 'a', { t: 'goster' });
  assert.equal(d2.oyuncular[1].cezalar[0].puan, -1); assert.equal(d2.oyuncular[0].cezalar.length, 0);
  hata(d2, 'a', { t: 'goster' }, 'zaten');
  const d3 = oyna(d2, 'a', { t: 'at', tas: T(1, 0).id });
  hata({ ...d3, sira: 0, cekti: true }, 'a', { t: 'goster' }, 'ilk turunda');
  const e = oyna(kur([[T(1, 0), T(2, 0)], [T(3, 0)]], { deste: [] }), 'a', { t: 'at', tas: T(1, 0).id });
  const s = M.sonuc(e) as ElSonuc;
  assert.equal(s.neden, 'deste'); assert.equal(s.kazananlar.length, 0); assert.equal(s.satirlar[1].puan, 0);
});

console.log('Bot benzetimi');
let el = 0, biten = 0, hamle = 0;
const bas = Date.now();
for (let n = 2; n <= 4; n++) for (let t = 0; t < 150; t++) {
  const rng = tohum(n * 7919 + t);
  let d = M.elBaslat({ oyuncular: AD.slice(0, n).map((id) => ({ id })), elNo: 1, baslayan: t, rng }) as DuzDurum;
  let adim = 0;
  while (!M.sonuc(d)) {
    assert.ok(++adim < 1000, 'el bitmedi');
    const o = d.oyuncular[d.sira].id;
    const h = M.botHamle(d, o, rng);
    const r = M.uygula(d, o, h, rng);
    assert.ok(!('hata' in r), `bot hamlesi reddedildi: ${'hata' in r ? r.hata : ''}`);
    d = (r as { durum: DuzDurum }).durum;
    const top = d.deste.length + 1 + d.oyuncular.reduce((a, x) => a + x.el.length + x.atiklar.length, 0);
    assert.equal(top, 106, 'taş korunumu');
    for (const ev of (r as { olaylar: { t: string; kime?: string }[] }).olaylar) if (ev.t === 'cektim') assert.ok(ev.kime);
    assert.equal((M.gorunum(d, null) as OkeyGorunum).elim.length, 0);
    hamle++;
  }
  el++;
  if ((M.sonuc(d) as ElSonuc).kazananlar.length) biten++;
}
console.log(`  ✓ ${el} el, ${biten} bitirildi, ${hamle} hamle, ${Date.now() - bas} ms, takılma yok`);
console.log(`\nTamam: ${sayac} birim bölümü + bot benzetimi.`);
