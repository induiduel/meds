/** Taş Domino motor sınaması: `npx tsx src/services/masa/motor/domino.sinama.ts` (hata varsa çıkış ≠ 0) */
import assert from 'node:assert/strict';
import type { Olay, Renk, Rng, Tas } from '../tipler';
import { dominoMotor as M, ekNedeni, koyuslar, uyar, type DominoDurum, type DominoGorunum } from './domino';

let adet = 0;
const sina = (ad: string, f: () => void) => { f(); adet++; console.log('  ✓ ' + ad); };
const tohumlu = (a: number): Rng => () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
const rng0 = tohumlu(1);
const T = (s: number, r: number, k = 0): Tas => ({ id: k * 52 + r * 13 + s - 1, s, r: r as Renk });
const D = (g: { eller: Tas[][]; zincir: Tas[]; deste?: Tas[]; sira?: number; ek?: boolean; cekilen?: number | null; pasSayisi?: number }): DominoDurum => ({
  tur: 'domino', elNo: 1, oyuncular: g.eller.map((el, i) => ({ id: 'o' + i, el })), sira: g.sira ?? 0, deste: g.deste ?? [],
  zincir: g.zincir, cekilen: g.cekilen ?? null, ek: !!g.ek, pasSayisi: g.pasSayisi ?? 0, son: null, sonuc: null,
});
type Tamam = { durum: DominoDurum; olaylar: Olay[] };
const oyna = (d: DominoDurum, o: string, h: unknown): Tamam => {
  const once = JSON.stringify(d);
  const s = M.uygula(d, o, h, rng0);
  assert.equal(JSON.stringify(d), once, 'uygula girdiyi değiştirdi');
  if ('hata' in s) assert.fail('beklenmeyen hata: ' + s.hata);
  return s as Tamam;
};
const hata = (d: DominoDurum, o: string, h: unknown) => {
  const once = JSON.stringify(d);
  const s = M.uygula(d, o, h, rng0);
  assert.equal(JSON.stringify(d), once);
  assert.ok('hata' in s, 'hata bekleniyordu: ' + JSON.stringify(h));
};
const G = (d: DominoDurum, b: string | null) => M.gorunum(d, b) as unknown as DominoGorunum;

console.log('Eşleşme ve uçlar');
sina('uyma kuralı: aynı renk ya da aynı sayı', () => {
  assert.ok(uyar(T(6, 0), T(7, 0)));
  assert.ok(uyar(T(13, 0), T(1, 0)), 'aynı renk herhangi sayı');
  assert.ok(uyar(T(7, 2), T(7, 0)));
  assert.ok(uyar(T(7, 0, 1), T(7, 0)), 'özdeş kopya uyar');
  assert.ok(!uyar(T(6, 1), T(7, 0)));
  assert.ok(!uyar(T(9, 3), T(7, 0)));
});
sina('ek hamle nedeni', () => {
  assert.equal(ekNedeni(T(8, 0), T(7, 0), [T(7, 0), T(8, 0)]), 'ardisik');
  assert.equal(ekNedeni(T(6, 0), T(7, 0), [T(6, 0), T(7, 0)]), 'ardisik');
  assert.equal(ekNedeni(T(1, 0), T(13, 0), [T(13, 0), T(1, 0)]), null, '13→1 ardışık değil');
  assert.equal(ekNedeni(T(9, 0), T(7, 0), [T(7, 0), T(9, 0)]), null);
  assert.equal(ekNedeni(T(7, 2), T(7, 0), [T(7, 0), T(7, 2)]), 'esuc', 'tek taştan sonra iki uç 7');
  assert.equal(ekNedeni(T(4, 1), T(9, 1), [T(4, 2), T(9, 1), T(4, 1)]), 'esuc');
  assert.equal(ekNedeni(T(5, 1), T(9, 1), [T(4, 2), T(9, 1), T(5, 1)]), null);
});
sina('baş ve son uca koyma', () => {
  const d = D({ eller: [[T(3, 2), T(9, 1), T(1, 3)], [T(2, 2)]], zincir: [T(7, 0), T(3, 1)], deste: [T(5, 3)] });
  assert.deepEqual(koyuslar(d.oyuncular[0].el, d.zincir), [{ tas: T(3, 2).id, uc: 'son' }, { tas: T(9, 1).id, uc: 'son' }]);
  const a = oyna(d, 'o0', { t: 'koy', tas: T(9, 1).id, uc: 'son' });
  assert.deepEqual(a.durum.zincir.map((t) => t.s), [7, 3, 9]);
  assert.equal(a.durum.sira, 1);
  hata(d, 'o0', { t: 'koy', tas: T(9, 1).id, uc: 'bas' });
  hata(d, 'o0', { t: 'koy', tas: T(1, 3).id, uc: 'son' });
  hata(d, 'o1', { t: 'koy', tas: T(2, 2).id, uc: 'son' });
  hata(d, 'o0', { t: 'koy', tas: T(2, 2).id, uc: 'son' });
  hata(d, 'o0', { t: 'koy', tas: T(9, 1).id });
  hata(d, 'o0', { t: 'pas' });
  hata(d, 'o0', null);
});
sina('tek taşlı zincirde iki uç', () => {
  const d = D({ eller: [[T(7, 1), T(1, 1)], [T(2, 2)]], zincir: [T(7, 0)] });
  assert.equal(koyuslar(d.oyuncular[0].el, d.zincir).length, 2);
});

console.log('Çekme ve pas');
sina('koyabilirken çekmek 1 taş, sıra geçer', () => {
  const d = D({ eller: [[T(2, 0), T(1, 2)], [T(2, 2)]], zincir: [T(7, 0)], deste: [T(5, 3), T(8, 0)] });
  const a = oyna(d, 'o0', { t: 'cek' });
  assert.equal(a.durum.sira, 1);
  assert.equal(a.durum.oyuncular[0].el.length, 3);
  assert.equal(a.durum.cekilen, null);
});
sina('koyamazken uyan taş gelene dek çekilir; yalnız o taş ya da pas', () => {
  const d = D({ eller: [[T(1, 2)], [T(2, 2)]], zincir: [T(7, 0)], deste: [T(5, 3), T(9, 0), T(3, 3), T(11, 1)] });
  const a = oyna(d, 'o0', { t: 'cek' });
  assert.equal(a.durum.sira, 0);
  assert.equal(a.durum.cekilen, T(9, 0).id);
  assert.equal(a.durum.oyuncular[0].el.length, 4);
  assert.equal(a.durum.deste.length, 1);
  assert.equal(a.olaylar.find((o) => o.t === 'cekti')!.adet, 3);
  hata(a.durum, 'o0', { t: 'cek' });
  hata(a.durum, 'o0', { t: 'koy', tas: T(1, 2).id, uc: 'son' });
  const g = G(a.durum, 'o0');
  assert.deepEqual(g.secenekler, [{ tas: T(9, 0).id, uc: 'bas' }, { tas: T(9, 0).id, uc: 'son' }]);
  assert.ok(g.pasOlur && !g.cekOlur);
  assert.equal(oyna(a.durum, 'o0', { t: 'pas' }).durum.sira, 1);
  assert.equal(oyna(a.durum, 'o0', { t: 'koy', tas: T(9, 0).id, uc: 'son' }).durum.sira, 1);
});
sina('uyan gelmeden deste biterse sıra geçer ve pas sayılır', () => {
  const d = D({ eller: [[T(1, 2)], [T(2, 2)]], zincir: [T(7, 0)], deste: [T(5, 3), T(11, 1)] });
  const a = oyna(d, 'o0', { t: 'cek' });
  assert.equal(a.durum.sira, 1);
  assert.equal(a.durum.deste.length, 0);
  assert.equal(a.durum.pasSayisi, 1);
});
sina('deste boş: koyabiliyorsan pas yok, koyamıyorsan pas', () => {
  const d = D({ eller: [[T(2, 0)], [T(2, 2)]], zincir: [T(7, 0)] });
  hata(d, 'o0', { t: 'pas' });
  hata(d, 'o0', { t: 'cek' });
  const a = oyna(D({ eller: [[T(2, 1)], [T(2, 2)]], zincir: [T(7, 0)] }), 'o0', { t: 'pas' });
  assert.equal(a.durum.pasSayisi, 1);
  assert.equal(a.durum.sira, 1);
});

console.log('Ek hamle');
sina('aynı renkten ardışık: bir taş daha', () => {
  const d = D({ eller: [[T(8, 0), T(2, 3), T(1, 3)], [T(2, 2)]], zincir: [T(4, 3), T(7, 0)], deste: [T(4, 1)] });
  const a = oyna(d, 'o0', { t: 'koy', tas: T(8, 0).id, uc: 'son' });
  assert.ok(a.durum.ek);
  assert.equal(a.durum.sira, 0);
  assert.ok(a.olaylar.some((o) => o.t === 'ekHamle' && o.neden === 'ardisik'));
  hata(a.durum, 'o0', { t: 'cek' });
  const b = oyna(a.durum, 'o0', { t: 'koy', tas: T(2, 3).id, uc: 'bas' });
  assert.equal(b.durum.sira, 1);
  assert.ok(!b.durum.ek);
  assert.equal(oyna(a.durum, 'o0', { t: 'pas' }).durum.sira, 1);
});
sina('iki uç aynı sayı: bir taş daha', () => {
  const d = D({ eller: [[T(4, 0), T(4, 2)], [T(2, 2)]], zincir: [T(4, 3), T(9, 0)] });
  const a = oyna(d, 'o0', { t: 'koy', tas: T(4, 0).id, uc: 'son' });
  assert.ok(a.olaylar.some((o) => o.t === 'ekHamle' && o.neden === 'esuc'));
  assert.ok(a.durum.ek);
});
sina('ardışık değilse ek hamle yok', () => {
  const d = D({ eller: [[T(11, 0), T(1, 3)], [T(2, 2)]], zincir: [T(4, 3), T(7, 0)] });
  const a = oyna(d, 'o0', { t: 'koy', tas: T(11, 0).id, uc: 'son' });
  assert.ok(!a.durum.ek);
  assert.equal(a.durum.sira, 1);
});
sina('ek hamle zincirlenmez', () => {
  const d = D({ eller: [[T(8, 0), T(1, 3)], [T(2, 2)]], zincir: [T(4, 3), T(7, 0)], ek: true });
  const a = oyna(d, 'o0', { t: 'koy', tas: T(8, 0).id, uc: 'son' });
  assert.ok(!a.durum.ek);
  assert.equal(a.durum.sira, 1);
});
sina('koyacak taş yoksa ek hamle verilmez', () => {
  const d = D({ eller: [[T(8, 0), T(1, 1)], [T(2, 2)]], zincir: [T(4, 3), T(7, 0)] });
  const a = oyna(d, 'o0', { t: 'koy', tas: T(8, 0).id, uc: 'son' });
  assert.ok(!a.durum.ek);
  assert.equal(a.durum.sira, 1);
});

console.log('Bitiş ve puan');
sina('eli bitiren kazanır, diğerleri toplamı kadar eksi', () => {
  const d = D({ eller: [[T(6, 0)], [T(2, 2), T(10, 1)], [T(5, 3)]], zincir: [T(7, 0)] });
  const a = oyna(d, 'o0', { t: 'koy', tas: T(6, 0).id, uc: 'bas' });
  const s = a.durum.sonuc!;
  assert.equal(s.neden, 'bitti');
  assert.deepEqual(s.kazananlar, ['o0']);
  assert.deepEqual(s.satirlar.map((x) => x.puan), [17, -12, -5]);
  assert.equal(M.sonuc(a.durum), s);
  hata(a.durum, 'o1', { t: 'pas' });
});
sina('kilit: herkes art arda pas → en düşük toplam kazanır', () => {
  const d = D({ eller: [[T(2, 1)], [T(3, 2), T(10, 1)], [T(1, 3), T(5, 2)]], zincir: [T(7, 0)] });
  let s = oyna(d, 'o0', { t: 'pas' });
  s = oyna(s.durum, 'o1', { t: 'pas' });
  assert.equal(s.durum.sonuc, null);
  s = oyna(s.durum, 'o2', { t: 'pas' });
  const r = s.durum.sonuc!;
  assert.equal(r.neden, 'berabere');
  assert.deepEqual(r.kazananlar, ['o0']);
  assert.deepEqual(r.satirlar.map((x) => x.puan), [19, -13, -6]);
});
sina('ek hamleyi geri çeviren pas kilit sayacını sıfırlar', () => {
  const d = D({ eller: [[T(8, 1)], [T(1, 1)]], zincir: [T(8, 0), T(7, 0), T(8, 2)], ek: true, pasSayisi: 1 });
  const a = oyna(d, 'o0', { t: 'pas' });
  assert.equal(a.durum.pasSayisi, 0);
  assert.equal(a.durum.sonuc, null);
});

console.log('Gizlilik');
sina('başkasının eli ve deste görünmez', () => {
  const d = M.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }, { id: 'c' }], elNo: 1, baslayan: 0, rng: tohumlu(5) }) as DominoDurum;
  const g = G(d, 'b');
  assert.deepEqual(g.elim, d.oyuncular[1].el);
  assert.deepEqual(g.secenekler, []);
  assert.ok(!g.pasOlur && !g.cekOlur);
  const metin = JSON.stringify(g);
  for (const t of [...d.oyuncular[0].el, ...d.oyuncular[2].el, ...d.deste]) assert.ok(!metin.includes(`"id":${t.id},`), 'gizli taş sızdı: ' + t.id);
  assert.equal(g.deste, d.deste.length);
  const iz = G(d, null);
  assert.deepEqual(iz.elim, []);
  assert.deepEqual(iz.oyuncular.map((o) => o.tasSayisi), [7, 7, 7]);
  assert.equal(d.deste.length + 21 + 1, 104);
});
sina('çekilen taş yalnız sırası olana görünür', () => {
  const d = D({ eller: [[T(1, 2)], [T(2, 2)]], zincir: [T(7, 0)], deste: [T(5, 3), T(8, 0)] });
  const a = oyna(d, 'o0', { t: 'cek' });
  assert.equal(G(a.durum, 'o0').tur_.cekilen, T(8, 0).id);
  assert.equal(G(a.durum, 'o1').tur_.cekilen, undefined);
  assert.ok(a.olaylar.some((o) => o.t === 'cektim' && o.kime === 'o0'));
});

console.log('Bot elleri');
sina('2–4 oyuncu × yüzlerce bot eli biter, bot hep geçerli', () => {
  let el = 0, kilit = 0, ek = 0;
  for (let n = 2; n <= 4; n++) for (let k = 0; k < 250; k++) {
    const rng = tohumlu(n * 1000 + k);
    let d = M.elBaslat({ oyuncular: Array.from({ length: n }, (_, i) => ({ id: 'b' + i })), elNo: 1, baslayan: k, rng }) as DominoDurum;
    let adim = 0;
    while (!M.sonuc(d)) {
      assert.ok(++adim < 2000, 'el bitmedi');
      const sira = d.oyuncular[d.sira].id;
      for (const o of d.oyuncular) if (o.id !== sira) assert.equal(M.botHamle(d, o.id, rng), null);
      const h = M.botHamle(d, sira, rng);
      const s = M.uygula(d, sira, h, rng);
      if ('hata' in s) assert.fail(`bot hatası: ${s.hata} ${JSON.stringify(h)}`);
      if (s.olaylar.some((o) => o.t === 'ekHamle')) ek++;
      d = s.durum as DominoDurum;
      const toplam = d.deste.length + d.zincir.length + d.oyuncular.reduce((t, o) => t + o.el.length, 0);
      assert.equal(toplam, 104);
    }
    const r = M.sonuc(d)!;
    if (r.neden === 'berabere') kilit++;
    assert.ok(r.kazananlar.length >= 1);
    el++;
  }
  console.log(`    ${el} el, ${kilit} kilit, ${ek} ek hamle`);
});

console.log(`\n${adet} sınama geçti.`);
