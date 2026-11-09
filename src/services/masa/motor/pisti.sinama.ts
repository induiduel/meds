/**
 * Pişti motoru sınaması: `npx tsx src/services/masa/motor/pisti.sinama.ts` (hata → çıkış ≠ 0)
 */
import assert from 'node:assert/strict';
import type { Olay, Rng } from '../tipler';
import { VALE, kartPuani, pistiDeste, pistiMotor, pistiOneri, type PistiDurum, type PistiGorunum, type PistiKart, type PistiRenk } from './pisti';

const tohumlu = (t: number): Rng => () => {
  t = (t + 0x6d2b79f5) | 0;
  let x = Math.imul(t ^ (t >>> 15), 1 | t);
  x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x;
  return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
};
const rng0 = tohumlu(1);
type Tamam = { durum: unknown; olaylar: Olay[] };
type Tanim = [PistiRenk, number];

/** Elle kurulmuş durum: eller + yer (alttan üste); kalan kartlar destede */
function kur(eller: Record<string, Tanim[]>, yer: Tanim[], ek: Partial<PistiDurum> = {}): PistiDurum {
  const havuz = pistiDeste();
  const al = ([r, v]: Tanim): PistiKart => { const i = havuz.findIndex((k) => k.renk === r && k.d === v); assert(i >= 0, `kart yok ${r}${v}`); return havuz.splice(i, 1)[0]; };
  const ids = Object.keys(eller);
  const e = Object.fromEntries(ids.map((id) => [id, eller[id].map(al)]));
  return {
    tur: 'pisti', elNo: 1, oyuncular: ids, takimlar: Object.fromEntries(ids.map((id, i) => [id, i % 2 ? 'B' : 'A'])), kim: 0,
    eller: e, yer: yer.map(al), kapali: 0, deste: havuz,
    alinan: Object.fromEntries(ids.map((id) => [id, []])), pisti: Object.fromEntries(ids.map((id) => [id, 0])),
    pistiPuan: Object.fromEntries(ids.map((id) => [id, 0])), sonAlan: null, sonuc: null, ...ek,
  };
}
const kid = (d: PistiDurum, o: string, r: PistiRenk, v: number) => { const k = d.eller[o].find((x) => x.renk === r && x.d === v); assert(k); return k.id; };
function yap(d: PistiDurum, o: string, kart: number) {
  const r = pistiMotor.uygula(d, o, { t: 'oyna', kart }, rng0);
  assert(!('hata' in r), 'hata' in r ? r.hata : '');
  return { d: (r as Tamam).durum as PistiDurum, olaylar: (r as Tamam).olaylar };
}
const korunum = (d: PistiDurum) => {
  const hepsi = [...d.deste, ...d.yer, ...d.oyuncular.flatMap((id) => [...d.eller[id], ...d.alinan[id]])];
  assert.equal(hepsi.length, 52); assert.equal(new Set(hepsi.map((k) => k.id)).size, 52);
};

let adet = 0;
const sina = (ad: string, f: () => void) => { f(); adet++; console.log(`  ✓ ${ad}`); };

console.log('Birim');
sina('deste: 52 tekil kart, 4 renk × 13, puan toplamı 4+4+2+3 = 13', () => {
  const d = pistiDeste();
  assert.equal(d.length, 52); assert.equal(new Set(d.map((k) => `${k.renk}${k.d}`)).size, 52);
  assert.equal(d.reduce((t, k) => t + kartPuani(k), 0), 4 + 4 + (2 - 0) + (3 - 0));
});
sina('elBaslat: 2/4 oyuncu, yer 4 (3 kapalı), üst Vale değil, eller 4', () => {
  for (let s = 0; s < 300; s++) for (const n of [2, 4]) {
    const d = pistiMotor.elBaslat({ oyuncular: Array.from({ length: n }, (_, i) => ({ id: `o${i}` })), elNo: 1, baslayan: 0, rng: tohumlu(s) }) as PistiDurum;
    assert.equal(d.yer.length, 4); assert.equal(d.kapali, 3); assert.notEqual(d.yer[3].d, VALE);
    d.oyuncular.forEach((id) => assert.equal(d.eller[id].length, 4));
    korunum(d);
  }
  assert.throws(() => pistiMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }, { id: 'c' }], elNo: 1, baslayan: 0, rng: rng0 }));
});
sina('aynı değer yeri alır; tek kartta pişti 10', () => {
  const d = kur({ a: [['kupa', 7], ['maca', 3]], b: [['sinek', 4]] }, [['karo', 7]]);
  const r = yap(d, 'a', kid(d, 'a', 'kupa', 7));
  assert.equal(r.d.yer.length, 0); assert.equal(r.d.alinan.a.length, 2); assert.equal(r.d.pisti.a, 1); assert.equal(r.d.pistiPuan.a, 10);
  assert(r.olaylar.some((o) => o.t === 'pisti')); assert.equal(r.d.sonAlan, 'a');
});
sina('çok kartlı yerde eşleşme pişti değil; Vale her şeyi alır ama tek karta pişti değil', () => {
  const d = kur({ a: [['kupa', 7]], b: [['maca', VALE]] }, [['sinek', 2], ['karo', 7]]);
  const r = yap(d, 'a', kid(d, 'a', 'kupa', 7));
  assert.equal(r.d.pisti.a, 0); assert.equal(r.d.alinan.a.length, 3);
  const d2 = kur({ a: [['kupa', VALE], ['kupa', 2]], b: [['sinek', 3]] }, [['karo', 5]]);
  const r2 = yap(d2, 'a', kid(d2, 'a', 'kupa', VALE));
  assert.equal(r2.d.alinan.a.length, 2); assert.equal(r2.d.pisti.a, 0);
});
sina('Vale ile tek Vale = 20; boş yere Vale yalnız bırakılır', () => {
  const d = kur({ a: [['kupa', VALE], ['kupa', 2]], b: [['sinek', 3]] }, [['karo', VALE]]);
  const r = yap(d, 'a', kid(d, 'a', 'kupa', VALE));
  assert.equal(r.d.pistiPuan.a, 20);
  const d2 = kur({ a: [['kupa', VALE], ['kupa', 2]], b: [['sinek', 3]] }, []);
  const r2 = yap(d2, 'a', kid(d2, 'a', 'kupa', VALE));
  assert.equal(r2.d.yer.length, 1); assert.equal(r2.d.alinan.a.length, 0);
});
sina('hatalar: sıra, elde olmayan kart, bozuk hamle; uygula girdiyi değiştirmez', () => {
  const d = kur({ a: [['kupa', 7]], b: [['sinek', 4]] }, [['karo', 7]]);
  const once = JSON.stringify(d);
  assert('hata' in pistiMotor.uygula(d, 'b', { t: 'oyna', kart: kid(d, 'b', 'sinek', 4) }, rng0));
  assert('hata' in pistiMotor.uygula(d, 'a', { t: 'oyna', kart: 999 }, rng0));
  assert('hata' in pistiMotor.uygula(d, 'a', { t: 'cek' }, rng0));
  yap(d, 'a', kid(d, 'a', 'kupa', 7));
  assert.equal(JSON.stringify(d), once);
});
sina('el sonu: kalan son alana, puan dökümü, çoğunluk +3, eşitlikte kimse', () => {
  // a son kartla alır; b kart bırakır, yerde kalan a'ya gider
  const d = kur({ a: [['sinek', 2]], b: [['karo', 10]] }, [['kupa', 2]], { deste: [] });
  let r = yap(d, 'a', kid(d, 'a', 'sinek', 2)); // pişti (10) + ♣2 + 2 kart
  r = yap(r.d, 'b', kid(r.d, 'b', 'karo', 10));
  const s = pistiMotor.sonuc(r.d)!;
  assert(s); assert.equal(r.d.alinan.a.length, 3);
  const a = s.satirlar.find((x) => x.id === 'a')!, b = s.satirlar.find((x) => x.id === 'b')!;
  assert.equal(a.puan, 10 + 2 + 3 + 3); assert.equal(b.puan, 0);
  assert.deepEqual(s.kazananlar, ['a']); assert.match(a.aciklama!, /1 pişti \(10\)/); assert.match(a.aciklama!, /en çok kart \+3/);
  // eşitlik: ikisi 1'er kart alır (yere hiç kart kalmaz) — kimse +3 almaz
  const e = kur({ a: [['kupa', 5]], b: [['maca', 9]] }, [], { deste: [], alinan: { a: [], b: [] } });
  let r2 = yap(e, 'a', kid(e, 'a', 'kupa', 5));
  r2 = yap(r2.d, 'b', kid(r2.d, 'b', 'maca', 9));
  const s2 = pistiMotor.sonuc(r2.d)!;
  s2.satirlar.forEach((x) => assert.equal(x.puan, 0)); assert.deepEqual(s2.kazananlar, ['a', 'b']);
});
sina('eşli: takım toplamı her üyeye, kazananTakim', () => {
  const d = kur({ a: [['kupa', 7]], b: [['maca', 3]], c: [['sinek', 4]], e: [['karo', 9]] }, [['karo', 7]], { deste: [] });
  let r = yap(d, 'a', kid(d, 'a', 'kupa', 7));
  for (const [o, k] of [['b', ['maca', 3]], ['c', ['sinek', 4]], ['e', ['karo', 9]]] as [string, Tanim][]) r = yap(r.d, o, kid(r.d, o, ...k));
  const s = pistiMotor.sonuc(r.d)!;
  // A takımı: a + c; a pişti 10 + 2 kart + son kalanlar (3) → 5 kart, çoğunluk +3
  const p = Object.fromEntries(s.satirlar.map((x) => [x.id, x.puan]));
  assert.equal(p.a, 13); assert.equal(p.c, 13); assert.equal(p.b, 0); assert.equal(s.kazananTakim, 'A'); assert.deepEqual(s.kazananlar, ['a', 'c']);
});
sina('gizlilik: görünümde başkasının eli, deste, kapalı kart yok; cektim kime’li', () => {
  const d = pistiMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }], elNo: 1, baslayan: 0, rng: rng0 }) as PistiDurum;
  const g = pistiMotor.gorunum(d, 'a') as unknown as PistiGorunum;
  const js = JSON.stringify(g);
  for (const k of [...d.eller.b, ...d.deste, ...d.yer.slice(0, 3)]) assert(!g.elim.some((x) => x.id === k.id) && g.ust?.id !== k.id);
  assert.equal(g.ust!.id, d.yer[3].id); assert.equal(g.yerSayisi, 4); assert(!js.includes('"deste":['));
  const iz = pistiMotor.gorunum(d, null) as unknown as PistiGorunum;
  assert.equal(iz.elim.length, 0);
  // yeniden dağıtımda kartlar yalnız kime'li olayda
  let s = d;
  for (let i = 0; i < 8; i++) {
    const h = pistiMotor.botHamle(s, s.oyuncular[s.kim], rng0) as { kart: number };
    const r = yap(s, s.oyuncular[s.kim], h.kart); s = r.d;
    if (i === 7) { assert(r.olaylar.some((o) => o.t === 'dagit')); r.olaylar.filter((o) => 'kartlar' in o).forEach((o) => assert(o.kime)); }
  }
});
sina('öneri: pişti fırsatı, Vale saklanır, eşleşme önce', () => {
  const D = pistiDeste();
  const k = (r: PistiRenk, v: number) => D.find((x) => x.renk === r && x.d === v)!;
  assert.equal(pistiOneri([k('kupa', VALE), k('maca', 3)], k('karo', 9), 2)!.kart, k('maca', 3).id);
  assert.equal(pistiOneri([k('kupa', VALE), k('maca', 9)], k('karo', 9), 1)!.kart, k('maca', 9).id);
  assert.match(pistiOneri([k('maca', 9)], k('karo', 9), 1)!.neden, /pişti/);
  assert.equal(pistiOneri([k('kupa', VALE), k('maca', 3)], null, 0)!.kart, k('maca', 3).id);
  assert.equal(pistiOneri([k('kupa', VALE), k('maca', 3)], k('karo', 9), 6)!.kart, k('kupa', VALE).id);
});

console.log('Bot elleri');
for (const n of [2, 4]) sina(`${n} oyuncu × 400 el: bot hep geçerli, el biter, korunum, puan tutarlı`, () => {
  for (let s = 0; s < 400; s++) {
    const rng = tohumlu(s * 7 + n);
    let d = pistiMotor.elBaslat({ oyuncular: Array.from({ length: n }, (_, i) => ({ id: `o${i}` })), elNo: 1, baslayan: s % n, rng }) as PistiDurum;
    let adim = 0;
    while (!pistiMotor.sonuc(d)) {
      const o = d.oyuncular[d.kim];
      for (const b of d.oyuncular) if (b !== o) assert.equal(pistiMotor.botHamle(d, b, rng), null);
      const h = pistiMotor.botHamle(d, o, rng);
      assert(h);
      const r = pistiMotor.uygula(d, o, h, rng);
      assert(!('hata' in r));
      d = (r as Tamam).durum as PistiDurum;
      korunum(d);
      assert(++adim <= 52);
    }
    assert.equal(adim, 48);
    const son = pistiMotor.sonuc(d)!;
    assert.equal(d.yer.length, 0); assert.equal(d.deste.length, 0);
    const toplamKart = d.oyuncular.reduce((t, id) => t + d.alinan[id].length, 0);
    assert.equal(toplamKart, 52);
    const birim = n === 4 ? 2 : 1;
    const toplam = son.satirlar.reduce((t, x) => t + x.puan, 0) / birim;
    const pisti = d.oyuncular.reduce((t, id) => t + d.pistiPuan[id], 0);
    assert(toplam === 13 + pisti || toplam === 16 + pisti, `puan ${toplam}`);
    assert(son.kazananlar.length >= 1);
  }
});

console.log(`\n${adet} sınama geçti.`);
