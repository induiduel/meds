/**
 * 101 Okey motor sınaması: `npx tsx src/services/masa/motor/yuzbir.sinama.ts` (hata → çıkış ≠ 0).
 * Birim sınamaları + tohumlu bot oyunları (taş korunumu, per geçerliliği, ceza, sonlanma) + bulanık sınama + açılış araması süresi.
 */
import assert from 'node:assert/strict';
import type { Ceza, ElSonuc, OkeyGorunum, Olay, Per, Renk, Tas } from '../tipler';
import { yuzbirMotor as M, type YuzbirDurum, type YuzbirOyuncu } from './yuzbir';
import { acilisAra, acilisBul, ciftBul, elSirala, enIyiDizilim, etkin, gercek, ipuclari, islemeYerleri, jokerMi, okeyBul, perAra, perCoz, type Okey } from './yuzbirAsistan';

const tohum = (a: number) => () => {
  a = (a + 0x6d2b79f5) | 0;
  let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
const T = (s: number, r: number, k = 0): Tas => ({ id: r * 26 + (s - 1) * 2 + k, s, r: r as Renk });
const S = (k = 0): Tas => ({ id: 104 + k, s: 0, r: 0 });
const OK: Okey = { s: 5, r: 3 };
const J = (k = 0) => T(5, 3, k);
const AD = ['a', 'b', 'c', 'd'];
const rng0 = tohum(1);

function kur(eller: Tas[][], ek: Partial<YuzbirDurum> = {}, oy: Partial<YuzbirOyuncu>[] = []): YuzbirDurum {
  return {
    tur: 'yuzbir', elNo: 1, sira: 0, deste: [T(1, 3), T(2, 3), T(3, 3)], gosterge: T(4, 3), okey: OK, perler: [], perNo: 100,
    cekti: true, hamleYapti: false, yandanAlinan: null, buTurActi: false, sonuc: null,
    oyuncular: eller.map((el, i) => ({ id: AD[i], el, acti: false, ciftActi: false, cezalar: [], atiklar: [], ...oy[i] })),
    ...ek,
  };
}
const per = (id: number, tur: Per['tur'], taslar: Tas[], sahip = 'a'): Per => ({ id, tur, taslar, sahip });
type Tamam = { durum: YuzbirDurum; olaylar: Olay[] };
function oyna(d: YuzbirDurum, o: string, h: unknown): Tamam {
  const once = JSON.stringify(d);
  const r = M.uygula(d, o, h, rng0);
  assert.equal(JSON.stringify(d), once, 'uygula girdi durumunu değiştirdi');
  assert.ok(!('hata' in r), `beklenmeyen hata: ${'hata' in r ? r.hata : ''}`);
  return r as Tamam;
}
function hata(d: YuzbirDurum, o: string, h: unknown, icerir?: string): string {
  const once = JSON.stringify(d);
  const r = M.uygula(d, o, h, rng0);
  assert.equal(JSON.stringify(d), once, 'uygula girdi durumunu değiştirdi');
  assert.ok('hata' in r, `hata bekleniyordu: ${JSON.stringify(h)}`);
  if (icerir) assert.ok(r.hata.includes(icerir), `"${r.hata}" içinde "${icerir}" yok`);
  return r.hata;
}
const gor = (d: YuzbirDurum, ben: string | null) => M.gorunum(d, ben) as OkeyGorunum;
const sonuc = (d: YuzbirDurum) => M.sonuc(d) as ElSonuc;
const puanlar = (d: YuzbirDurum) => Object.fromEntries(sonuc(d).satirlar.map((s) => [s.id, s.puan]));
let sayac = 0;
const bolum = (ad: string, f: () => void) => { f(); sayac++; console.log(`  ✓ ${ad}`); };

console.log('Birim sınamaları');

bolum('gösterge / okey / dağıtım', () => {
  assert.deepEqual(okeyBul(T(13, 2)), { s: 1, r: 2 });
  assert.deepEqual(okeyBul(T(4, 3)), OK);
  for (let n = 2; n <= 4; n++) {
    for (let t = 0; t < 200; t++) {
      const bas = t % n;
      const d = M.elBaslat({ oyuncular: AD.slice(0, n).map((id) => ({ id })), elNo: 1, baslayan: bas, rng: tohum(t * 7 + n) }) as YuzbirDurum;
      assert.notEqual(d.gosterge.s, 0, 'gösterge sahte okey olamaz');
      assert.deepEqual(d.okey, { s: (d.gosterge.s % 13) + 1, r: d.gosterge.r });
      d.oyuncular.forEach((o, i) => assert.equal(o.el.length, i === bas ? 22 : 21));
      assert.equal(d.deste.length, 106 - 1 - 21 * n - 1);
      assert.equal(d.sira, bas);
      assert.equal(d.cekti, true);
      korunum(d);
      hata(d, AD[bas], { t: 'cek' }, 'zaten');
    }
  }
  assert.throws(() => M.elBaslat({ oyuncular: [{ id: 'a' }], elNo: 1, baslayan: 0, rng: rng0 }));
});

bolum('sahte okey', () => {
  assert.equal(jokerMi(S(), OK), false);
  assert.equal(jokerMi(J(), OK), true);
  assert.deepEqual(gercek(S(), OK), { s: 5, r: 3 });
  assert.equal(gercek(J(), OK), null);
  const c = perCoz([T(4, 3), S(), T(6, 3)], OK);
  assert.ok(c && c.tur === 'seri' && c.deger === 15 && c.taslar.every((t) => !t.yerine));
  assert.equal(perCoz([S(), T(5, 0), T(5, 1)], OK)?.deger, 15);
  assert.equal(perCoz([S(), T(6, 0), T(7, 0)], OK), null, 'sahte okey joker gibi davranamaz');
  assert.equal(perCoz([S(0), S(1)], OK)?.tur, 'cift');
});

bolum('per çözümü: seri / grup / çift, joker yerleşimi, değerler', () => {
  const c = (ts: Tas[]) => perCoz(ts, OK);
  assert.deepEqual([c([T(5, 0), T(3, 0), T(4, 0)])?.tur, c([T(5, 0), T(3, 0), T(4, 0)])?.deger], ['seri', 12]);
  assert.deepEqual(c([T(5, 0), T(3, 0), T(4, 0)])?.taslar.map((t) => t.s), [3, 4, 5]);
  assert.equal(c([T(1, 0), T(2, 0), T(3, 0)])?.deger, 6);
  assert.equal(c([T(12, 0), T(13, 0), T(1, 0)]), null, '12-13-1 yok');
  assert.equal(c([T(3, 0), T(4, 0), T(5, 1)]), null);
  assert.equal(c([T(3, 0), T(4, 0), T(4, 0, 1)]), null);
  const orta = c([T(3, 0), J(), T(5, 0)]);
  assert.ok(orta && orta.deger === 12);
  assert.deepEqual(orta.taslar[1].yerine, { s: 4, r: 0 });
  const uc = c([J(), T(11, 0), T(12, 0)]);
  assert.ok(uc && uc.deger === 36);
  assert.deepEqual(uc.taslar[2].yerine, { s: 13, r: 0 });
  const alt = c([T(12, 0), J(), T(13, 0)]);
  assert.ok(alt && alt.deger === 36, '13 aşılamaz: joker alta');
  assert.deepEqual(alt.taslar[0].yerine, { s: 11, r: 0 });
  assert.equal(c([T(3, 0), T(4, 0), J(0), J(1)])?.deger, 18);
  assert.equal(c([T(12, 0), T(13, 0), J(0), J(1)])?.deger, 46);
  assert.equal(c([T(12, 0), J(0), J(1), T(9, 0)])?.deger, 42);
  assert.equal(c([T(1, 0), T(5, 0), J(0), J(1)]), null);
  assert.equal(c(Array.from({ length: 13 }, (_, i) => T(i + 1, 1)))?.deger, 91);
  const g = c([T(7, 2), J(), T(7, 0)]);
  assert.ok(g && g.tur === 'grup' && g.deger === 21);
  assert.deepEqual(g.taslar.map((t) => etkin(t, OK).r), [0, 1, 2]);
  assert.deepEqual(g.taslar[1].yerine, { s: 7, r: 1 }, 'joker eksik renklerin en küçük dizinlisi');
  assert.equal(c([T(7, 0), T(7, 1), T(7, 2), T(7, 3)])?.deger, 28);
  assert.equal(c([T(7, 0), T(7, 1), J(0), J(1)])?.deger, 28);
  assert.equal(c([T(7, 0), T(7, 0, 1), T(7, 1)]), null, 'grupta aynı renk iki kez olmaz');
  assert.equal(c([T(7, 0), T(7, 1), T(7, 2), T(7, 3), J()]), null);
  assert.equal(c([T(7, 0), J(0), J(1)]), null, 'bir perde en az 2 gerçek taş');
  assert.deepEqual([c([T(7, 0), T(7, 0, 1)])?.tur, c([T(7, 0), T(7, 0, 1)])?.deger], ['cift', 14]);
  assert.equal(c([T(7, 0), T(7, 1)]), null);
  const jc = c([J(), T(9, 2)]);
  assert.ok(jc && jc.tur === 'cift' && jc.deger === 18);
  assert.deepEqual(jc.taslar[1].yerine, { s: 9, r: 2 });
  assert.equal(c([J(0), J(1)])?.tur, 'cift');
  assert.equal(c([T(7, 0)]), null);
});

const EL100 = [T(11, 0), T(12, 0), T(13, 0), T(11, 1), T(12, 1), T(13, 1), ...[1, 2, 3, 4, 5, 6, 7].map((s) => T(s, 2))];
const PER100 = [[T(11, 0), T(12, 0), T(13, 0)], [T(11, 1), T(12, 1), T(13, 1)], [1, 2, 3, 4, 5, 6, 7].map((s) => T(s, 2))].map((p) => p.map((t) => t.id));
const EL101 = [T(10, 0), T(11, 0), T(12, 0), T(13, 0), T(10, 1), T(11, 1), T(12, 1), T(13, 1), T(3, 0), T(3, 1), T(3, 2)];
const PER101 = [EL101.slice(0, 4), EL101.slice(4, 8), EL101.slice(8)].map((p) => p.map((t) => t.id));

bolum('açılış: 100 ret / 101 kabul, girdi denetimi', () => {
  const d = kur([[...EL100, T(9, 0), T(2, 1)], [T(1, 0)]]);
  hata(d, 'a', { t: 'ac101', perler: PER100 }, '100');
  assert.equal(acilisBul(d.oyuncular[0].el, OK), null);
  assert.equal(enIyiDizilim(d.oyuncular[0].el, OK).toplam, 100);
  const e = kur([[...EL101, T(7, 0), T(2, 1)], [T(1, 0)]]);
  const r = oyna(e, 'a', { t: 'ac101', perler: PER101 });
  const a = r.durum.oyuncular[0];
  assert.ok(a.acti && !a.ciftActi && a.el.length === 2 && r.durum.perler.length === 3);
  assert.ok(r.durum.hamleYapti && r.durum.buTurActi);
  assert.equal((r.olaylar[0].perler as Per[]).length, 3);
  assert.equal(acilisBul(e.oyuncular[0].el, OK)?.toplam, 101);
  hata(r.durum, 'a', { t: 'ac101', perler: PER101 }, 'Zaten açtın');
  hata(e, 'a', { t: 'ac101', perler: [PER101[0], PER101[0], PER101[2], PER101[1]] }, 'iki perde');
  hata(e, 'a', { t: 'ac101', perler: [...PER101.slice(0, 2), [T(3, 0).id, T(3, 1).id, T(3, 3).id]] }, 'elinde değil');
  hata(e, 'a', { t: 'ac101', perler: [...PER101.slice(0, 2), [T(3, 0).id, T(3, 1).id, T(7, 0).id]] }, '3. per');
  hata(e, 'a', { t: 'ac101', perler: 'x' });
  hata(e, 'a', { t: 'ac101', perler: [[1.5, 2, 3]] });
  hata(e, 'b', { t: 'ac101', perler: PER101 }, 'Sıra sende değil');
  hata(e, 'z', { t: 'ac101', perler: PER101 }, 'oyuncu değilsin');
  hata(e, 'a', { t: 'ac', taslar: PER101[0] }, 'Henüz açmadın');
  hata(e, 'a', { t: 'isle', tas: 1, per: 1 }, 'önce açmalısın');
  hata(kur([EL101, [T(1, 0)]]), 'a', { t: 'ac101', perler: PER101 }, 'Atacak bir taş bırakmalısın.');
  hata(kur([[...EL101, T(9, 0)], [T(1, 0)]], { cekti: false, sira: 0 }), 'a', { t: 'ac101', perler: PER101 }, 'Önce taş çek');
});

const cift = (s: number, r: number) => [T(s, r, 0), T(s, r, 1)];
bolum('çiftle açılış: 4 ret / 5 kabul; çift açan seri açamaz', () => {
  const dort = [cift(1, 0), cift(2, 0), cift(9, 1), cift(13, 2)];
  const el = [...dort.flat(), T(7, 0), J(), T(3, 1), T(4, 1), T(5, 1), T(6, 2), T(6, 2, 1), T(8, 0)];
  const d = kur([el, [T(1, 1)]]);
  hata(d, 'a', { t: 'ac101', perler: dort.map((p) => p.map((t) => t.id)) }, 'en az 5 çift');
  hata(d, 'a', { t: 'ac101', perler: [...dort.map((p) => p.map((t) => t.id)), [T(3, 1).id, T(4, 1).id, T(5, 1).id]] }, 'karıştırılamaz');
  const bes = [...dort.map((p) => p.map((t) => t.id)), [T(7, 0).id, J().id]];
  const r = oyna(d, 'a', { t: 'ac101', perler: bes });
  assert.ok(r.durum.oyuncular[0].ciftActi && r.durum.perler.every((p) => p.tur === 'cift'));
  assert.deepEqual(r.durum.perler[4].taslar[1].yerine, { s: 7, r: 0 });
  hata(r.durum, 'a', { t: 'ac', taslar: [T(3, 1).id, T(4, 1).id, T(5, 1).id] }, 'Çiftle açtın');
  const r2 = oyna(r.durum, 'a', { t: 'ac', taslar: [T(6, 2).id, T(6, 2, 1).id] });
  assert.equal(r2.durum.perler.length, 6);
  hata(r2.durum, 'a', { t: 'isle', tas: T(8, 0).id, per: r2.durum.perler[0].id }, 'Çifte taş işlenmez');
  assert.equal(acilisBul(el, OK)?.cift, true);
  // seri/grupla açan çift açamaz
  const e = oyna(kur([[...EL101, ...cift(9, 0), T(2, 1)], [T(1, 0)]]), 'a', { t: 'ac101', perler: PER101 }).durum;
  hata(e, 'a', { t: 'ac', taslar: cift(9, 0).map((t) => t.id) }, 'çift açamazsın');
});

bolum('yandan alma: kullanmadan atma hatası, geri koyma, kullanınca serbest', () => {
  const X = T(9, 0);
  const d = kur([[T(1, 1)], [T(2, 2), T(8, 1)]], { sira: 1, cekti: false }, [{ atiklar: [T(4, 0), X] }]);
  hata(d, 'b', { t: 'at', tas: T(2, 2).id }, 'Önce taş çek');
  hata(d, 'b', { t: 'geriKoy' }, 'Geri koyulacak taş yok');
  hata(d, 'b', { t: 'cek', kaynak: 'cop' });
  const r = oyna(d, 'b', { t: 'cek', kaynak: 'atik' });
  assert.equal(r.durum.yandanAlinan, X.id);
  assert.equal(gor(r.durum, 'a').yandanAlinan, X.id);
  assert.deepEqual(r.olaylar, [{ t: 'cekti', o: 'b', kaynak: 'atik', tas: X }]);
  assert.deepEqual(r.durum.oyuncular[0].atiklar, [T(4, 0)], 'yalnız son atılan taş alınır');
  assert.equal(hata(r.durum, 'b', { t: 'at', tas: T(2, 2).id }), 'Yandan aldığın taşı kullanmalı ya da geri koymalısın.');
  assert.equal(hata(r.durum, 'b', { t: 'at', tas: X.id }), 'Yandan aldığın taşı kullanmalı ya da geri koymalısın.');
  hata(r.durum, 'b', { t: 'cek' }, 'zaten');
  const g = oyna(r.durum, 'b', { t: 'geriKoy' });
  assert.equal(g.durum.yandanAlinan, null);
  assert.deepEqual(g.durum.oyuncular[0].atiklar, [T(4, 0), X]);
  assert.deepEqual(g.durum.oyuncular[1].el.map((t) => t.id), [T(2, 2).id, T(8, 1).id, T(3, 3).id]);
  assert.equal(g.durum.deste.length, 2);
  assert.ok(g.olaylar.some((o) => o.t === 'cektim' && o.kime === 'b'));
  hata(g.durum, 'b', { t: 'geriKoy' });
  assert.equal(oyna(g.durum, 'b', { t: 'at', tas: T(8, 1).id }).durum.sira, 0);
  hata(kur([[T(1, 1)], [T(2, 2)]], { sira: 1, cekti: false }), 'b', { t: 'cek', kaynak: 'atik' }, 'alınacak taş yok');
  // deste boşken geri koyma eli bitirir
  const bos = oyna(kur([[T(1, 1)], [T(2, 2)]], { sira: 1, cekti: false, deste: [] }, [{ atiklar: [X] }]), 'b', { t: 'cek', kaynak: 'atik' });
  assert.equal(sonuc(oyna(bos.durum, 'b', { t: 'geriKoy' }).durum).neden, 'deste');
  // açmış oyuncu yandan aldığını işler → atabilir
  const p = per(1, 'seri', [T(6, 0), T(7, 0), T(8, 0)]);
  const ac = kur([[T(1, 1)], [T(2, 2), T(8, 1)]], { sira: 1, cekti: false, perler: [p] }, [{ atiklar: [X] }, { acti: true }]);
  const a1 = oyna(ac, 'b', { t: 'cek', kaynak: 'atik' });
  const a2 = oyna(a1.durum, 'b', { t: 'isle', tas: X.id, per: 1 });
  assert.equal(a2.durum.yandanAlinan, null);
  assert.deepEqual(a2.durum.perler[0].taslar.map((t) => t.s), [6, 7, 8, 9]);
  assert.deepEqual(a2.olaylar[0], { t: 'isledi', o: 'b', per: 1, tas: X, uc: 'son' });
  hata(a2.durum, 'b', { t: 'geriKoy' });
  const a3 = oyna(a2.durum, 'b', { t: 'at', tas: T(2, 2).id });
  assert.equal(a3.durum.oyuncular[1].cezalar.length, 0);
  // açmamış oyuncu yandan aldığı taşla açar
  const y = kur([[T(1, 1)], [...EL101.slice(1), T(9, 1), T(2, 2)]], { sira: 1, cekti: false }, [{ atiklar: [EL101[0]] }]);
  assert.deepEqual(M.botHamle(y, 'b', rng0), { t: 'cek', kaynak: 'atik' });
  const y1 = oyna(y, 'b', { t: 'cek', kaynak: 'atik' });
  const y2 = oyna(y1.durum, 'b', { t: 'ac101', perler: PER101 });
  assert.equal(y2.durum.yandanAlinan, null);
});

bolum('işleme: uçlar, grup, okey ve belirsiz uç', () => {
  const seri = per(1, 'seri', [T(6, 0), T(7, 0), T(8, 0)]);
  const alt = per(2, 'seri', [T(1, 1), T(2, 1), T(3, 1)]);
  const grup = per(3, 'grup', [T(9, 0), T(9, 1), T(9, 3)]);
  const dolu = per(4, 'grup', [T(2, 0), T(2, 1), T(2, 2), T(2, 3)]);
  const cf = per(5, 'cift', cift(12, 2));
  const perler = [seri, alt, grup, dolu, cf];
  assert.deepEqual(islemeYerleri(T(5, 0), perler, OK), [{ per: 1, uc: 'bas' }]);
  assert.deepEqual(islemeYerleri(T(9, 0, 1), perler, OK), [{ per: 1, uc: 'son' }]);
  assert.deepEqual(islemeYerleri(T(9, 2), perler, OK), [{ per: 3, uc: null }]);
  assert.deepEqual(islemeYerleri(T(12, 2), perler, OK), []);
  assert.deepEqual(islemeYerleri(T(2, 2, 1), perler, OK), []);
  assert.deepEqual(islemeYerleri(J(), perler, OK), [{ per: 1, uc: 'bas' }, { per: 1, uc: 'son' }, { per: 2, uc: 'son' }, { per: 3, uc: null }]);
  const d = kur([[J(0), J(1), T(9, 2), T(4, 1), T(11, 3), S()], [T(1, 0)]], { perler }, [{ acti: true }]);
  hata(d, 'a', { t: 'isle', tas: J().id, per: 1 }, 'iki ucuna');
  hata(d, 'a', { t: 'isle', tas: J().id, per: 1, uc: 'orta' });
  hata(d, 'a', { t: 'isle', tas: J().id, per: 4 }, 'işlenmez');
  hata(d, 'a', { t: 'isle', tas: J().id, per: 5 }, 'Çifte');
  hata(d, 'a', { t: 'isle', tas: J().id, per: 99 }, 'per yok');
  hata(d, 'a', { t: 'isle', tas: T(11, 3).id, per: 1 }, 'işlenmez');
  hata(d, 'a', { t: 'isle', tas: T(4, 1).id, per: 2, uc: 'bas' }, 'uymuyor');
  const r1 = oyna(d, 'a', { t: 'isle', tas: J().id, per: 1, uc: 'bas' });
  assert.deepEqual(r1.durum.perler[0].taslar[0], { ...J(), yerine: { s: 5, r: 0 } });
  const r2 = oyna(r1.durum, 'a', { t: 'isle', tas: J(1).id, per: 3 });
  assert.deepEqual(r2.durum.perler[2].taslar.map((t) => etkin(t, OK).r), [0, 1, 2, 3]);
  assert.deepEqual(r2.durum.perler[2].taslar[2].yerine, { s: 9, r: 2 });
  hata(r2.durum, 'a', { t: 'isle', tas: T(9, 2).id, per: 3 }, 'işlenmez');
  // masadaki okeyin yeri değişmez: seri artık 5–8, 4 başa işlenir
  assert.deepEqual(islemeYerleri(T(4, 0), r2.durum.perler, OK), [{ per: 1, uc: 'bas' }]);
  const r3 = oyna(r2.durum, 'a', { t: 'isle', tas: T(4, 1).id, per: 2 });
  assert.deepEqual(r3.durum.perler[1].taslar.map((t) => t.s), [1, 2, 3, 4]);
  // sahte okey = okeyin değeri (5 sarı): 5'li gruba girer
  const sg = kur([[S(), T(1, 0)], [T(1, 1)]], { perler: [per(1, 'grup', [T(5, 0), T(5, 1), T(5, 2)])] }, [{ acti: true }]);
  assert.deepEqual(oyna(sg, 'a', { t: 'isle', tas: 104, per: 1 }).durum.perler[0].taslar[3], S());
});

bolum('atacak taş bırakma kuralı', () => {
  const p = per(1, 'seri', [T(6, 0), T(7, 0), T(8, 0)]);
  const d = kur([[T(3, 1), T(4, 1), T(5, 1)], [T(1, 0)]], { perler: [p] }, [{ acti: true }]);
  assert.equal(hata(d, 'a', { t: 'ac', taslar: [T(3, 1).id, T(4, 1).id, T(5, 1).id] }), 'Atacak bir taş bırakmalısın.');
  const e = kur([[T(9, 0)], [T(1, 0)]], { perler: [p] }, [{ acti: true }]);
  assert.equal(hata(e, 'a', { t: 'isle', tas: T(9, 0).id, per: 1 }), 'Atacak bir taş bırakmalısın.');
  const f = kur([[T(3, 1), T(4, 1), T(5, 1), T(9, 0)], [T(1, 0)]], { perler: [p] }, [{ acti: true }]);
  const r = oyna(f, 'a', { t: 'ac', taslar: [T(5, 1).id, T(3, 1).id, T(4, 1).id] });
  assert.equal(r.durum.oyuncular[0].el.length, 1);
  hata(f, 'a', { t: 'ac', taslar: [T(3, 1).id, T(3, 1).id, T(4, 1).id] }, 'iki kez');
  hata(f, 'a', { t: 'ac', taslar: [T(3, 1).id, T(4, 1).id, T(9, 0).id] }, 'per olmuyor');
  hata(f, 'a', { t: 'ac', taslar: [T(3, 1).id, T(4, 1).id, T(6, 1).id] }, 'elinde değil');
});

bolum('cezalar: işlek atma, okey atma; bitiş atışında ceza yok', () => {
  const p = per(1, 'seri', [T(6, 0), T(7, 0), T(8, 0)]);
  const d = kur([[T(9, 0), T(2, 2), J()], [T(1, 0)]], { perler: [p] });
  const r1 = oyna(d, 'a', { t: 'at', tas: T(9, 0).id });
  assert.deepEqual(r1.durum.oyuncular[0].cezalar, [{ tur: 'islekAtti', puan: -101, aciklama: 'İşlek taş attı' }]);
  assert.deepEqual(r1.olaylar.map((o) => o.t), ['atti', 'ceza', 'sira']);
  assert.deepEqual(gor(r1.durum, 'b').oyuncular[0].cezalar.length, 1);
  const r2 = oyna(d, 'a', { t: 'at', tas: J().id });
  assert.deepEqual(r2.durum.oyuncular[0].cezalar, [{ tur: 'okeyAtti', puan: -101, aciklama: 'Okey attı' }]);
  const r3 = oyna(d, 'a', { t: 'at', tas: T(2, 2).id });
  assert.equal(r3.durum.oyuncular[0].cezalar.length, 0);
  assert.deepEqual(r3.olaylar, [{ t: 'atti', o: 'a', tas: T(2, 2) }, { t: 'sira', o: 'b' }]);
  assert.deepEqual([r3.durum.sira, r3.durum.cekti, r3.durum.hamleYapti], [1, false, false]);
  assert.deepEqual(r3.durum.oyuncular[0].atiklar, [T(2, 2)]);
  hata(d, 'a', { t: 'at', tas: T(1, 0).id }, 'elinde değil');
  hata(d, 'a', { t: 'at' });
  for (const son of [J(), T(9, 0)]) {
    const b = oyna(kur([[son], [T(1, 0)]], { perler: [p] }, [{ acti: true }]), 'a', { t: 'at', tas: son.id });
    assert.equal(sonuc(b.durum).neden, 'bitti');
    assert.deepEqual(sonuc(b.durum).kazananlar, ['a']);
    assert.equal(b.durum.oyuncular[0].cezalar.length, 0, 'bitiş atışında ceza yok');
    assert.equal(b.olaylar[b.olaylar.length - 1].t, 'elBitti');
    hata(b.durum, 'b', { t: 'cek' }, 'El bitti');
    assert.equal(M.botHamle(b.durum, 'b', rng0), null);
    assert.equal(gor(b.durum, null).bitti, true);
  }
});

const C: Ceza = { tur: 'islekAtti', puan: -101, aciklama: 'İşlek taş attı' };
bolum('deste bitişi ve puanlar', () => {
  const oy = [{ acti: true }, {}, { acti: true }, { acti: true, ciftActi: true, cezalar: [C] }];
  const eller = () => [[T(2, 0)], [T(1, 1), T(13, 1)], [J(), T(5, 0), S()], [T(10, 2), T(2, 1)]];
  // deste
  const ds = oyna(kur(eller(), { sira: 1, cekti: false, deste: [] }, oy), 'b', { t: 'cek' });
  assert.equal(sonuc(ds.durum).neden, 'deste');
  assert.deepEqual(sonuc(ds.durum).kazananlar, []);
  assert.deepEqual(puanlar(ds.durum), { a: -2, b: -202, c: -111, d: -24 - 101 });
  assert.ok(sonuc(ds.durum).satirlar.every((s) => !s.kazandi));
  assert.equal(sonuc(kur(eller())), null);
  // olağan bitiş
  const n = oyna(kur(eller(), {}, oy), 'a', { t: 'at', tas: T(2, 0).id });
  assert.deepEqual(puanlar(n.durum), { a: 101, b: -202, c: -111, d: -125 });
  assert.deepEqual(sonuc(n.durum).satirlar.map((s) => s.kalan), [0, 2, 3, 2]);
  assert.deepEqual(sonuc(n.durum).satirlar.map((s) => s.kazandi), [true, false, false, false]);
  assert.equal(sonuc(n.durum).satirlar[3].aciklama, '2 taş (−24) · çiftle açtı ×2 · 1 ceza (−101)');
  // kazananın cezası da eklenir
  const kc = oyna(kur(eller(), {}, [{ acti: true, cezalar: [C] }, ...oy.slice(1)]), 'a', { t: 'at', tas: T(2, 0).id });
  assert.equal(puanlar(kc.durum).a, 0);
  // elden bitme: aynı turda açıp bitirme → +202, diğerlerinin eksisi 2 kat (cezalar katlanmaz)
  const e0 = kur([[...EL101, T(2, 0)], ...eller().slice(1)], {}, [{}, ...oy.slice(1)]);
  const e1 = oyna(e0, 'a', { t: 'ac101', perler: PER101 });
  const e2 = oyna(e1.durum, 'a', { t: 'at', tas: T(2, 0).id });
  assert.deepEqual(puanlar(e2.durum), { a: 202, b: -404, c: -222, d: -48 - 101 });
  assert.ok(sonuc(e2.durum).satirlar[0].aciklama?.includes('Elden'));
});

bolum('açılış önceki turdaysa elden bitme sayılmaz', () => {
  const s0 = oyna(kur([[...EL101, T(2, 0), T(8, 3)], [T(1, 1), T(13, 1)]], { deste: [T(3, 3), T(1, 3)] }), 'a', { t: 'ac101', perler: PER101 });
  const s1 = oyna(s0.durum, 'a', { t: 'at', tas: T(8, 3).id });
  assert.equal(s1.durum.buTurActi, false);
  const s2 = oyna(oyna(s1.durum, 'b', { t: 'cek' }).durum, 'b', { t: 'at', tas: T(13, 1).id });
  const s3 = oyna(s2.durum, 'a', { t: 'cek' });
  assert.deepEqual(s3.olaylar, [{ t: 'cekti', o: 'a', kaynak: 'deste' }, { t: 'cektim', kime: 'a', tas: T(3, 3) }]);
  const s4 = oyna(s3.durum, 'a', { t: 'isle', tas: T(3, 3).id, per: s3.durum.perler[2].id });
  const s5 = oyna(s4.durum, 'a', { t: 'at', tas: T(2, 0).id });
  assert.deepEqual(puanlar(s5.durum), { a: 101, b: -202 });
});

function tasKimlikleri(x: unknown, out: number[] = []): number[] {
  if (Array.isArray(x)) for (const y of x) tasKimlikleri(y, out);
  else if (x && typeof x === 'object') {
    const o = x as Record<string, unknown>;
    if (typeof o.id === 'number' && typeof o.s === 'number' && typeof o.r === 'number') out.push(o.id);
    for (const v of Object.values(o)) tasKimlikleri(v, out);
  }
  return out;
}

bolum('görünüm ve gizlilik', () => {
  const d = M.elBaslat({ oyuncular: AD.map((id) => ({ id })), elNo: 3, baslayan: 2, rng: tohum(42) }) as YuzbirDurum;
  const gizli = (ben: string | null) => new Set([...d.deste, ...d.oyuncular.filter((o) => o.id !== ben).flatMap((o) => o.el)].map((t) => t.id));
  for (const ben of [...AD, null, 'yabanci']) {
    const g = gor(d, ben);
    assert.equal(g.tur, 'yuzbir');
    assert.deepEqual(g.elim, d.oyuncular.find((o) => o.id === ben)?.el ?? []);
    const giz = gizli(ben);
    assert.ok(tasKimlikleri(g).every((id) => !giz.has(id)), 'başkasının eli ya da deste sızdı');
    assert.deepEqual([g.elNo, g.sira, g.deste, g.tur_.cekti, g.bitti, g.okey, g.gosterge], [3, 'c', 20, true, false, d.okey, d.gosterge]);
    assert.deepEqual(g.oyuncular.map((o) => o.tasSayisi), [21, 21, 22, 21]);
    assert.ok(g.oyuncular.every((o) => o.atiklar && o.ciftActi === false && Array.isArray(o.cezalar)));
    assert.equal('yandanAlinan' in g, false);
    assert.doesNotThrow(() => JSON.stringify(g));
  }
  assert.deepEqual(JSON.parse(JSON.stringify(d)), d, 'durum düz JSON olmalı');
  assert.equal(M.botHamle(d, 'a', rng0), null);
  assert.equal(ipuclari(gor(d, 'a'), 'a').length, 0);
  assert.ok(ipuclari(gor(d, 'c'), 'c').some((i) => i.hamle.t === 'at' || i.hamle.t === 'ac101'));
});

bolum('asistan: sıralama, dizilim, ipuçları', () => {
  const el = [T(7, 3), ...EL101, J(), T(2, 0)];
  assert.deepEqual(elSirala(el, OK, 'per').slice(-2), [T(2, 0).id, T(7, 3).id]);
  assert.equal(new Set(elSirala(el, OK, 'per')).size, el.length);
  assert.equal(elSirala(el, OK, 'seri')[0], T(2, 0).id);
  assert.equal(elSirala(el, OK, 'grup')[0], T(2, 0).id);
  assert.equal(elSirala(el, OK, 'seri').at(-1), J().id);
  const diz = enIyiDizilim(el, OK);
  assert.equal(diz.toplam, 39 + 33 + 33 + 9); // 13-13-okey grubu + iki 10-11-12 serisi + 3ler
  assert.equal(acilisAra(el, OK, { zorunlu: T(7, 3).id }), null);
  assert.ok(acilisAra(el, OK, { zorunlu: J().id })?.perler.flat().some((t) => t.id === J().id));
  assert.equal(ciftBul([...cift(1, 0), T(4, 2), J(0), J(1)], OK).length, 2);
  assert.equal(ciftBul([...cift(1, 0), J(0), J(1)], OK, { birak: 1 }).length, 1);
  const d = kur([el, [T(1, 1)]], { sira: 0 });
  const ip = ipuclari(gor(d, 'a'), 'a');
  const ac = ip.find((i) => i.hamle.t === 'ac101');
  assert.ok(ac && ac.aciklama.includes('açabilirsin'));
  const r = oyna(d, 'a', ac.hamle);
  for (const i of ipuclari(gor(r.durum, 'a'), 'a')) oyna(r.durum, 'a', i.hamle);
  const bek = kur([[T(1, 1)], [T(3, 3), T(8, 1)]], { sira: 1, cekti: false, perler: [per(1, 'grup', [T(3, 0), T(3, 1), T(3, 2)])] }, [{ atiklar: [T(3, 3, 1)] }, { acti: true }]);
  assert.deepEqual(ipuclari(gor(bek, 'b'), 'b').map((i) => i.hamle), [{ t: 'cek', kaynak: 'atik' }, { t: 'cek', kaynak: 'deste' }]);
});

/* ------------------------------------------------------------------ değişmezler ------------------------------------------------------------------ */

function korunum(d: YuzbirDurum): void {
  const ids = [d.gosterge, ...d.deste, ...d.perler.flatMap((p) => p.taslar), ...d.oyuncular.flatMap((o) => [...o.el, ...o.atiklar])].map((t) => t.id).sort((a, b) => a - b);
  assert.equal(ids.length, 106, `taş sayısı ${ids.length}`);
  for (let i = 0; i < 106; i++) assert.equal(ids[i], i, 'taş kayboldu ya da çoğaldı');
}

function perGecerli(p: Per, okey: Okey): void {
  const e = p.taslar.map((t) => etkin(t, okey));
  const ger = p.taslar.filter((t) => !jokerMi(t, okey)).length;
  for (const t of p.taslar) assert.equal(!!t.yerine, jokerMi(t, okey), 'yerine yalnız jokerde dolu');
  if (p.tur === 'cift') return void assert.ok(e.length === 2 && e[0].s === e[1].s && e[0].r === e[1].r, 'çift bozuk');
  assert.ok(ger >= 2, 'perde en az 2 gerçek taş');
  if (p.tur === 'grup') {
    assert.ok(e.length >= 3 && e.length <= 4 && e.every((x) => x.s === e[0].s) && new Set(e.map((x) => x.r)).size === e.length, 'grup bozuk');
    assert.deepEqual(e.map((x) => x.r), e.map((x) => x.r).slice().sort(), 'grup renk sırasında değil');
  } else {
    assert.ok(e.length >= 3 && e.length <= 13 && e[0].s >= 1 && e[e.length - 1].s <= 13, 'seri sınır dışı');
    assert.ok(e.every((x, i) => x.r === e[0].r && x.s === e[0].s + i), 'seri ardışık değil');
  }
}

/* ------------------------------------------------------------------ rastgele bot oyunları ------------------------------------------------------------------ */

console.log('Rastgele bot oyunları');
const ornekler: YuzbirDurum[] = [];
for (const n of [2, 3, 4]) {
  const EL = 400;
  const st = { bitti: 0, deste: 0, elden: 0, hamle: 0, ceza: 0, acan: 0, yandan: 0, cift: 0, enUzun: 0 };
  const rng = tohum(1000 + n);
  for (let el = 0; el < EL; el++) {
    let d = M.elBaslat({ oyuncular: AD.slice(0, n).map((id) => ({ id })), elNo: el + 1, baslayan: el % n, rng }) as YuzbirDurum;
    korunum(d);
    let adim = 0;
    while (!d.sonuc) {
      assert.ok(++adim < 3000, 'el sonlanmıyor');
      const o = d.oyuncular[d.sira];
      for (const p of d.oyuncular) if (p.id !== o.id) assert.equal(M.botHamle(d, p.id, rng), null);
      const h = M.botHamle(d, o.id, rng) as { t: string; tas?: number; kaynak?: string };
      assert.ok(h, 'bot hamle üretmedi');
      const r = M.uygula(d, o.id, h, rng);
      assert.ok(!('hata' in r), `bot kural dışı oynadı: ${JSON.stringify(h)} → ${'hata' in r ? r.hata : ''}`);
      const y = (r as Tamam).durum;
      for (const e of (r as Tamam).olaylar) {
        if (e.t === 'cektim') assert.equal(e.kime, o.id);
        else assert.equal(e.kime, undefined);
        if (e.t === 'cekti' && e.kaynak === 'deste') assert.equal(e.tas, undefined, 'desteden çekilen taş sızdı');
        if (e.t === 'ceza') {
          // yalnız kaçınılmazsa: eldeki her taş okey ya da işlekti
          assert.ok(o.el.every((t) => jokerMi(t, d.okey) || islemeYerleri(t, d.perler, d.okey).length > 0), 'bot kaçınılabilir ceza aldı');
          st.ceza++;
        }
      }
      if (h.t === 'cek' && h.kaynak === 'atik') st.yandan++;
      if (h.t === 'geriKoy') assert.fail('bot yandan aldığı taşı kullanamadı');
      korunum(y);
      for (const p of y.perler) perGecerli(p, y.okey);
      assert.ok(y.sonuc || y.oyuncular.every((p) => p.el.length > 0), 'el bitmeden taşsız oyuncu');
      d = y;
      st.hamle++;
      if (st.hamle % 97 === 0 && ornekler.length < 600 && !d.sonuc) ornekler.push(d);
    }
    st.enUzun = Math.max(st.enUzun, adim);
    const s = d.sonuc as ElSonuc;
    st[s.neden === 'bitti' ? 'bitti' : 'deste']++;
    st.acan += d.oyuncular.filter((o) => o.acti).length;
    st.cift += d.oyuncular.filter((o) => o.ciftActi).length;
    if (s.satirlar.some((x) => x.puan >= 202)) st.elden++;
    assert.equal(s.satirlar.length, n);
    assert.equal(s.kazananlar.length, s.neden === 'bitti' ? 1 : 0);
    for (const x of s.satirlar) assert.equal(x.kalan, d.oyuncular.find((o) => o.id === x.id)?.el.length);
  }
  const yz = (x: number) => `${((100 * x) / EL).toFixed(1)}%`;
  console.log(`  ✓ ${n} oyuncu, ${EL} el: bitti ${yz(st.bitti)} · deste ${yz(st.deste)} · elden bitme ${st.elden} · açan oyuncu ${(st.acan / EL).toFixed(2)}/el (çiftle ${st.cift}) · yandan alma ${st.yandan} · ceza ${st.ceza} · hamle ${(st.hamle / EL).toFixed(0)}/el (en uzun ${st.enUzun})`);
}

/* ------------------------------------------------------------------ bulanık sınama ------------------------------------------------------------------ */

console.log('Bulanık sınama');
{
  const rng = tohum(77);
  const sec = <X>(l: X[]): X => l[Math.floor(rng() * l.length)];
  const sayi = () => sec<unknown>([Math.floor(rng() * 110), Math.floor(rng() * 110), -1, 106, 1.5, NaN, Infinity, '3', null, undefined, {}, []]);
  const dizi = () => sec<unknown>([Array.from({ length: Math.floor(rng() * 6) }, sayi), Array.from({ length: 3 }, () => Math.floor(rng() * 106)), null, 'abc', 7, {}, Array.from({ length: 40 }, sayi)]);
  let tamam = 0;
  let ret = 0;
  let d = ornekler[0];
  for (let i = 0; i < 40000; i++) {
    if (i % 25 === 0 || d.sonuc) d = sec(ornekler);
    const o = d.oyuncular[d.sira];
    const elden = () => (rng() < 0.7 && o.el.length ? sec(o.el).id : sayi());
    const perKim = () => (rng() < 0.7 && d.perler.length ? sec(d.perler).id : sayi());
    const h = sec<() => unknown>([
      () => null, () => undefined, () => 5, () => 'cek', () => [], () => ({}), () => ({ t: sayi() }), () => ({ t: 'devret' }), () => ({ t: 'yok' }),
      () => ({ t: 'cek', kaynak: sec<unknown>(['deste', 'atik', 'x', 3, null, undefined]) }),
      () => ({ t: 'geriKoy' }),
      () => ({ t: 'at', tas: elden() }),
      () => ({ t: 'ac', taslar: rng() < 0.6 ? Array.from({ length: 2 + Math.floor(rng() * 3) }, elden) : dizi() }),
      () => ({ t: 'ac101', perler: rng() < 0.6 ? Array.from({ length: 1 + Math.floor(rng() * 6) }, () => (rng() < 0.8 ? Array.from({ length: 2 + Math.floor(rng() * 3) }, elden) : dizi())) : dizi() }),
      () => ({ t: 'isle', tas: elden(), per: perKim(), uc: sec<unknown>([undefined, 'bas', 'son', 'x', 1, null]) }),
      () => M.botHamle(d, o.id, rng),
    ])();
    const kim = rng() < 0.85 ? o.id : sec<unknown>([...AD, 'x', '', null, 5]);
    const once = JSON.stringify(d);
    let r: ReturnType<typeof M.uygula>;
    try {
      r = M.uygula(d, kim as string, h, rng);
      M.botHamle(d, kim as string, rng);
      gor(d, kim as string);
    } catch (e) {
      assert.fail(`motor istisna fırlattı: ${JSON.stringify(h)} → ${String(e)}`);
    }
    assert.equal(JSON.stringify(d), once, 'girdi durumu değişti');
    if ('hata' in r) {
      assert.ok(typeof r.hata === 'string' && r.hata.length > 5);
      ret++;
    } else {
      tamam++;
      d = r.durum as YuzbirDurum;
      korunum(d);
      for (const p of d.perler) perGecerli(p, d.okey);
      for (const p of d.oyuncular) assert.ok(d.sonuc || p.el.length > 0);
    }
  }
  console.log(`  ✓ 40.000 rastgele/bozuk hamle (${ornekler.length} oyun içi durumdan): istisna yok · ${tamam} kabul · ${ret} ret`);
}

/* ------------------------------------------------------------------ arama doğruluğu + süre ------------------------------------------------------------------ */

console.log('Açılış araması');
{
  // Kaba kuvvetle karşılaştırma: küçük ve sık örgülü ellerde en yüksek toplam aynı olmalı
  const rng = tohum(5);
  const kaba = (el: Tas[], okey: Okey): number => {
    if (el.length < 3) return 0;
    const [ilk, ...kalan] = el;
    let en = kaba(kalan, okey);
    for (let m = 1; m < 1 << kalan.length; m++) {
      const ic: Tas[] = [ilk];
      const dis: Tas[] = [];
      kalan.forEach((t, i) => (m & (1 << i) ? ic : dis).push(t));
      if (ic.length < 3) continue;
      const c = perCoz(ic, okey);
      if (c && c.tur !== 'cift') en = Math.max(en, c.deger + kaba(dis, okey));
    }
    return en;
  };
  let jokerli = 0;
  for (let i = 0; i < 400; i++) {
    const okey: Okey = { s: 1 + Math.floor(rng() * 6), r: Math.floor(rng() * 2) as Renk };
    const havuz: Tas[] = [S(0), S(1)];
    for (let r = 0; r < 3; r++) for (let s = 1; s <= 7; s++) havuz.push(T(s, r, 0), T(s, r, 1));
    for (let k = havuz.length - 1; k > 0; k--) { const j = Math.floor(rng() * (k + 1)); [havuz[k], havuz[j]] = [havuz[j], havuz[k]]; }
    const el = havuz.slice(0, 7 + Math.floor(rng() * 5));
    if (el.some((t) => jokerMi(t, okey))) jokerli++;
    const a = perAra(el, okey);
    assert.equal(a.toplam, kaba(el, okey), `arama en iyiyi bulamadı: ${JSON.stringify(el)} okey ${JSON.stringify(okey)}`);
    assert.equal(new Set(a.perler.flat().map((t) => t.id)).size, a.perler.flat().length);
  }
  console.log(`  ✓ kaba kuvvetle 400 küçük elde aynı en yüksek toplam (${jokerli} elde joker)`);

  const eller: { el: Tas[]; okey: Okey }[] = [];
  for (let i = 0; i < 1000; i++) {
    const d = M.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }], elNo: 1, baslayan: 0, rng }) as YuzbirDurum;
    eller.push({ el: d.oyuncular[0].el, okey: d.okey });
  }
  for (const e of eller.slice(0, 50)) acilisBul(e.el, e.okey); // ısınma
  let enKotu = 0;
  let top = 0;
  let acan = 0;
  let ciftle = 0;
  for (const { el, okey } of eller) {
    const t0 = performance.now();
    const a = acilisBul(el, okey);
    const ms = performance.now() - t0;
    top += ms;
    enKotu = Math.max(enKotu, ms);
    if (!a) continue;
    acan++;
    if (a.cift) ciftle++;
    const ids = a.perler.flat().map((t) => t.id);
    assert.equal(new Set(ids).size, ids.length);
    assert.ok(ids.every((id) => el.some((t) => t.id === id)));
    const coz = a.perler.map((p) => perCoz(p, okey));
    assert.ok(coz.every((c) => c && (c.tur === 'cift') === a.cift));
    assert.equal(coz.reduce((x, c) => x + (c?.deger ?? 0), 0), a.toplam);
    assert.ok(a.cift ? a.perler.length >= 5 : a.toplam >= 101);
  }
  console.log(`  ✓ acilisBul, 1.000 rastgele 22 taşlı el: ortalama ${(top / 1000).toFixed(3)} ms · en kötü ${enKotu.toFixed(2)} ms · ${acan} elde açılış var (${ciftle} çiftle)`);
  // En kötü durum: tek renge yığılmış çift kopyalı el + 2 joker (düğüm tavanı)
  const zor = [...[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].flatMap((s) => [T(s, 0, 0), T(s, 0, 1)]), J(0), J(1)];
  const t0 = performance.now();
  const z = acilisBul(zor, OK);
  console.log(`  ✓ yığılmış el (20 taş tek renk çift kopya + 2 okey): ${(performance.now() - t0).toFixed(1)} ms, toplam ${z?.toplam}`);
  assert.ok(z && z.toplam >= 101);
}

console.log(`\nTAMAM: ${sayac} birim bölümü + rastgele oyunlar + bulanık sınama + arama geçti.`);
