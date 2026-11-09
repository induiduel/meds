/**
 * Kastet + Remi motor sınaması: `npx tsx src/services/masa/motor/acikMasa.sinama.ts` (hata → çıkış ≠ 0).
 * Birim sınamaları (düzenle, çek/pas, 26 alan + çift, 22 tavanı, Remi 30 açılışı, puan) + tohumlu bot benzetimi.
 */
import assert from 'node:assert/strict';
import type { ElSonuc, Motor, OkeyGorunum, Per, Renk, Tas } from '../tipler';
import { acikPer, kastetMotor, remiMotor, type AcikDurum } from './acikMasa';

const tohum = (a: number) => () => {
  a = (a + 0x6d2b79f5) | 0;
  let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
const T = (s: number, r: number, k = 0): Tas => ({ id: r * 26 + (s - 1) * 2 + k, s, r: r as Renk });
const S = (k = 0): Tas => ({ id: 104 + k, s: 0, r: 0 });
const AD = ['a', 'b', 'c', 'd'];
const rng0 = tohum(1);
let sayac = 0;
const bolum = (ad: string, f: () => void) => { f(); sayac++; console.log(`  ✓ ${ad}`); };

function kur(tur: 'kastet' | 'remi', eller: Tas[][], ek: Partial<AcikDurum> = {}): AcikDurum {
  return {
    tur, elNo: 1, sira: 0, deste: [T(1, 3), T(2, 3), T(3, 3)], gosterge: tur === 'kastet' ? T(4, 3) : null, okey: tur === 'kastet' ? { s: 5, r: 3 } : null,
    perler: [], ciftler: [], perNo: 50, hamleYapti: false, pasSeri: 0, sonuc: null,
    oyuncular: eller.map((el, i) => ({ id: AD[i], el, acti: false, cezalar: [] })), ...ek,
  };
}
const per = (id: number, taslar: Tas[], tur: Per['tur'] = 'seri'): Per => ({ id, tur, taslar, sahip: 'b' });
function oyna(M: Motor, d: AcikDurum, o: string, h: unknown): AcikDurum {
  const once = JSON.stringify(d);
  const r = M.uygula(d, o, h, rng0);
  assert.equal(JSON.stringify(d), once, 'uygula girdiyi değiştirdi');
  assert.ok(!('hata' in r), `beklenmeyen hata: ${'hata' in r ? r.hata : ''}`);
  return (r as { durum: AcikDurum }).durum;
}
function hata(M: Motor, d: AcikDurum, o: string, h: unknown, icerir: string) {
  const r = M.uygula(d, o, h, rng0);
  assert.ok('hata' in r, `hata bekleniyordu: ${JSON.stringify(h)}`);
  assert.ok(r.hata.includes(icerir), `"${r.hata}" içinde "${icerir}" yok`);
}

console.log('Birim sınamaları');
bolum('per çözümü (okey / Remi jokeri)', () => {
  assert.ok(acikPer([T(5, 1), T(6, 1), T(7, 1)], null));
  assert.equal(acikPer([T(12, 1), T(13, 1), T(1, 1)], null), null);
  assert.equal(acikPer([T(5, 1), T(5, 1, 1), T(5, 2)], null), null);
  const r = acikPer([T(5, 1), S(), T(7, 1)], null)!;
  assert.equal(r.taslar[1].s, 0); assert.deepEqual(r.taslar[1].yerine, { s: 6, r: 1 }); assert.equal(r.deger, 18);
  assert.equal(acikPer([T(5, 1), S(), S(1)], null), null, 'iki joker + bir taş per değil');
  const k = acikPer([T(5, 3), T(9, 0), T(10, 0)], { s: 5, r: 3 })!; // okey 8'in yerine
  assert.equal(k.tur, 'seri');
  assert.ok(acikPer([S(), T(9, 0), T(10, 0)], { s: 5, r: 3 }) === null, 'Kastet sahte okey sıradan taş (mavi 5)');
});
bolum('Kastet: çek-aç dışlaması, pas, örnek yer değiştirmeler', () => {
  const M = kastetMotor;
  const d = kur('kastet', [[T(5, 0), T(5, 2), T(7, 2), T(9, 1)], [T(1, 0)]], { perler: [per(1, [T(5, 1), T(6, 1), T(7, 1), T(8, 1)])] });
  hata(M, d, 'a', { t: 'pas' }, 'pas geçemezsin');
  hata(M, d, 'b', { t: 'cek' }, 'Sıra sende değil');
  // siyah 5'i alıp üçlü grup
  const d2 = oyna(M, d, 'a', { t: 'duzenle', perler: [[T(6, 1).id, T(7, 1).id, T(8, 1).id], [T(5, 1).id, T(5, 0).id, T(5, 2).id]] });
  assert.equal(d2.oyuncular[0].el.length, 2); assert.equal(d2.perler.length, 2); assert.ok(d2.oyuncular[0].acti);
  hata(M, d2, 'a', { t: 'cek' }, 'çekemezsin');
  hata(M, d2, 'a', { t: 'duzenle', perler: [[T(6, 1).id, T(7, 1).id, T(8, 1).id]] }, 'ele geri alınamaz');
  hata(M, d2, 'a', { t: 'duzenle', perler: d2.perler.map((p) => p.taslar.map((t) => t.id)) }, 'en az bir taş');
  const d3 = oyna(M, d2, 'a', { t: 'pas' });
  assert.equal(d3.sira, 1); assert.equal(d3.hamleYapti, false);
  // 5-6-7-8-9 + 7 → 5-6-7 ve 7-8-9
  const e = kur('kastet', [[T(7, 1, 1)], []], { perler: [per(1, [5, 6, 7, 8, 9].map((s) => T(s, 1)))] });
  const e2 = oyna(M, e, 'a', { t: 'duzenle', perler: [[T(5, 1).id, T(6, 1).id, T(7, 1).id], [T(7, 1, 1).id, T(8, 1).id, T(9, 1).id]] });
  assert.equal(e2.oyuncular[0].el.length, 0);
  assert.equal(e2.sonuc, null, 'Kastet bitiş pasla');
  const e3 = oyna(M, e2, 'a', { t: 'pas' });
  const s = M.sonuc(e3) as ElSonuc;
  assert.deepEqual(s.kazananlar, ['a']); assert.equal(s.satirlar[0].puan, 50); assert.equal(s.satirlar[1].puan, 0);
});
bolum('Kastet: çek sırayı geçirir, 22 tavanı, kalan puanı', () => {
  const M = kastetMotor;
  const d = oyna(M, kur('kastet', [[T(1, 0)], [T(2, 0)]]), 'a', { t: 'cek' });
  assert.equal(d.sira, 1); assert.equal(d.oyuncular[0].el.length, 2);
  const yirmi = Array.from({ length: 22 }, (_, i) => T((i % 13) + 1, Math.floor(i / 13), 0));
  const t = kur('kastet', [yirmi, [T(1, 2)]]);
  hata(M, t, 'a', { t: 'cek' }, '22');
  const t2 = oyna(M, t, 'a', { t: 'pas' });
  assert.equal(t2.sira, 1);
  // herkes çekemeyip pas → kazanansız
  const b = kur('kastet', [[T(1, 0), T(5, 3)], [S()]], { deste: [] });
  const b2 = oyna(M, oyna(M, b, 'a', { t: 'pas' }), 'b', { t: 'pas' });
  const s = M.sonuc(b2) as ElSonuc;
  assert.equal(s.neden, 'deste'); assert.equal(s.satirlar[0].puan, -26, 'okey 25'); assert.equal(s.satirlar[1].puan, -5, 'sahte okey = okeyin sayısı');
});
bolum('Kastet: 26 alan dolmadan çift yok, dolunca çift alanı', () => {
  const M = kastetMotor;
  const perler = Array.from({ length: 26 }, (_, i) => per(i + 1, [T(1, i % 4, 0), T(2, i % 4, 0), T(3, i % 4, 0)].map((t) => ({ ...t, id: 200 + i * 3 + t.s }))));
  const d = kur('kastet', [[T(9, 0), T(9, 0, 1), T(4, 1)], []], { perler: perler.slice(0, 25) });
  const ids = (l: Per[]) => l.map((p) => p.taslar.map((t) => t.id));
  hata(M, d, 'a', { t: 'duzenle', perler: ids(perler.slice(0, 25)), ciftler: [[T(9, 0).id, T(9, 0, 1).id]] }, 'dolunca');
  const d2 = kur('kastet', [[T(9, 0), T(9, 0, 1), T(4, 1)], []], { perler });
  hata(M, kur('kastet', [[T(4, 1), T(5, 1), T(6, 1)], []], { perler }), 'a', { t: 'duzenle', perler: [...ids(perler), [T(4, 1).id, T(5, 1).id, T(6, 1).id]] }, '26');
  const d3 = oyna(M, d2, 'a', { t: 'duzenle', perler: ids(perler), ciftler: [[T(9, 0).id, T(9, 0, 1).id]] });
  assert.equal(d3.ciftler.length, 1);
  const g = M.gorunum(d3, 'b') as OkeyGorunum;
  assert.equal(g.perler.filter((p) => p.tur === 'cift').length, 1); assert.equal(g.elim.length, 0);
  hata(M, d3, 'a', { t: 'duzenle', perler: [...ids(perler).slice(1), [...ids(perler)[0], T(9, 0).id]] }, 'Çift alanı');
});
bolum('Remi: 30 açılışı, açılış öncesi masaya dokunulmaz, el boşalınca biter', () => {
  const M = remiMotor;
  const masa = per(1, [T(1, 2), T(2, 2), T(3, 2)]);
  const d = kur('remi', [[T(3, 0), T(4, 0), T(5, 0), T(4, 2)], [T(13, 1), S()]], { perler: [masa] });
  hata(M, d, 'a', { t: 'duzenle', perler: [[T(1, 2).id, T(2, 2).id, T(3, 2).id], [T(3, 0).id, T(4, 0).id, T(5, 0).id]] }, 'en az 30');
  hata(M, d, 'a', { t: 'duzenle', perler: [[T(1, 2).id, T(2, 2).id, T(3, 2).id, T(4, 2).id]] }, 'dokunamazsın');
  hata(M, d, 'a', { t: 'pas' }, 'çekmelisin');
  const e = kur('remi', [[T(10, 0), T(11, 0), S(), T(4, 2)], [T(13, 1), T(1, 1)]], { perler: [masa] });
  const e2 = oyna(M, e, 'a', { t: 'duzenle', perler: [[T(1, 2).id, T(2, 2).id, T(3, 2).id], [T(10, 0).id, T(11, 0).id, S().id]] });
  assert.ok(e2.oyuncular[0].acti);
  const e3 = oyna(M, e2, 'a', { t: 'duzenle', perler: [[T(1, 2).id, T(2, 2).id, T(3, 2).id, T(4, 2).id], [T(10, 0).id, T(11, 0).id, S().id]] });
  const s = M.sonuc(e3) as ElSonuc;
  assert.deepEqual(s.kazananlar, ['a']); assert.equal(s.satirlar[0].puan, 14); assert.equal(s.satirlar[1].puan, -14);
  const j = kur('remi', [[T(1, 0)], [S(), T(2, 0)]], { deste: [] });
  const j2 = oyna(M, oyna(M, j, 'a', { t: 'pas' }), 'b', { t: 'pas' });
  assert.equal((M.sonuc(j2) as ElSonuc).satirlar[1].puan, -32, 'joker 30');
});

console.log('Bot benzetimi');
for (const [ad, M] of [['Kastet', kastetMotor], ['Remi', remiMotor]] as const) {
  let el = 0, kazanan = 0, hamleTop = 0;
  const bas = Date.now();
  for (let n = 2; n <= 4; n++) for (let tur = 0; tur < 100; tur++) {
    const rng = tohum(n * 1000 + tur);
    let d = M.elBaslat({ oyuncular: AD.slice(0, n).map((id) => ({ id })), elNo: 1, baslayan: tur, rng }) as AcikDurum;
    let adim = 0;
    while (!M.sonuc(d)) {
      assert.ok(++adim < 5000, `${ad}: el bitmedi (n=${n}, tur=${tur})`);
      const o = d.oyuncular[d.sira].id;
      for (const x of d.oyuncular) if (x.id !== o) assert.equal(M.botHamle(d, x.id, rng), null);
      const h = M.botHamle(d, o, rng);
      const r = M.uygula(d, o, h, rng);
      assert.ok(!('hata' in r), `${ad} bot hamlesi reddedildi: ${'hata' in r ? r.hata : ''} ${JSON.stringify(h)}`);
      d = (r as { durum: AcikDurum }).durum;
      // korunum + geçerlilik + gizlilik
      const top = d.deste.length + d.oyuncular.reduce((a, x) => a + x.el.length, 0) + [...d.perler, ...d.ciftler].reduce((a, p) => a + p.taslar.length, 0) + (d.gosterge ? 1 : 0);
      assert.equal(top, 106, 'taş korunumu');
      for (const p of d.perler) assert.ok(acikPer(p.taslar, d.okey), 'masada geçersiz per');
      if (d.tur === 'kastet') { assert.ok(d.perler.length <= 26); for (const x of d.oyuncular) assert.ok(x.el.length <= 22); }
      for (const ev of (r as { olaylar: { kime?: string; t: string }[] }).olaylar) if (ev.t === 'cektim') assert.ok(ev.kime);
      const g = M.gorunum(d, null) as OkeyGorunum;
      assert.equal(g.elim.length, 0);
      hamleTop++;
    }
    el++;
    if ((M.sonuc(d) as ElSonuc).kazananlar.length) kazanan++;
  }
  console.log(`  ✓ ${ad}: ${el} el, ${kazanan} kazananlı, ${hamleTop} hamle, ${Date.now() - bas} ms, takılma yok`);
}
console.log(`\nTamam: ${sayac} birim bölümü + bot benzetimi.`);
