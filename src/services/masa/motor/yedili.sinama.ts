/** Yedili / Takım Yedili motor sınaması: `npx tsx src/services/masa/motor/yedili.sinama.ts` (hata varsa çıkış ≠ 0) */
import { oduncBul } from './odunc';
import assert from 'node:assert/strict';
import type { Ceza, ElSonuc, OkeyGorunum, Olay, Per, Renk, Rng, Tas } from '../tipler';
import { takimMotor, yediliMotor, type YediliDurum } from './yedili';
import { eldekiPerler, elSirala, enIyiPlan, ipuclari, islemeYerleri, perDiz, perTuru, zorunlu } from './yediliAsistan';

let adet = 0;
const sina = (ad: string, f: () => void) => { f(); adet++; console.log('  ✓ ' + ad); };
const tohumlu = (a: number): Rng => () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
const rng0 = tohumlu(1);

/** T(sayı, renk, kopya) */
const T = (s: number, r: number, k = 0): Tas => ({ id: k * 52 + r * 13 + s - 1, s, r: r as Renk });
const P = (id: number, taslar: Tas[], sahip = 'x'): Per => ({ id, tur: perTuru(taslar)!, taslar: perDiz(taslar), sahip });
const D = (g: { tur?: 'yedili' | 'takim'; eller: Tas[][]; perler?: Per[]; deste?: Tas[]; acti?: boolean[]; sira?: number; cekti?: boolean; hamleYapti?: boolean; cezalar?: Ceza[][] }): YediliDurum => ({
  tur: g.tur ?? 'yedili', elNo: 1,
  oyuncular: g.eller.map((el, i) => ({ id: 'o' + i, ...(g.tur === 'takim' ? { takim: i % 2 ? 'B' as const : 'A' as const } : {}), el, acti: !!g.acti?.[i], cezalar: g.cezalar?.[i] ?? [] })),
  sira: g.sira ?? 0, deste: g.deste ?? [], perler: g.perler ?? [], cekti: !!g.cekti, hamleYapti: !!g.hamleYapti, kuru: 0, bitti: false, sonuc: null,
});
const M = (d: YediliDurum) => (d.tur === 'takim' ? takimMotor : yediliMotor);
type Tamam = { durum: YediliDurum; olaylar: Olay[] };
const oyna = (d: YediliDurum, o: string, h: unknown): Tamam => {
  const once = JSON.stringify(d);
  const s = M(d).uygula(d, o, h, rng0);
  assert.equal(JSON.stringify(d), once, 'uygula girdiyi değiştirdi');
  if ('hata' in s) assert.fail('beklenmeyen hata: ' + s.hata);
  return s as Tamam;
};
const hata = (d: YediliDurum, o: string, h: unknown, metin?: string) => {
  const s = M(d).uygula(d, o, h, rng0);
  assert.ok('hata' in s, 'hata bekleniyordu: ' + JSON.stringify(h));
  if (metin) assert.equal((s as { hata: string }).hata, metin);
};
const turler = (ol: Olay[]) => ol.map((o) => o.t);
const cezaTur = (d: YediliDurum, i: number) => d.oyuncular[i].cezalar.map((c) => c.tur);
/** Per ve işlek çıkarmayan hurda taşlar */
const HURDA = [T(1, 0), T(5, 1), T(9, 2), T(13, 3)];
const HURDA2 = [T(2, 3), T(7, 0), T(11, 1)];

console.log('Birim: per ve işleme');
sina('per geçerlilik sınırları', () => {
  assert.equal(perTuru([T(1, 0), T(2, 0), T(3, 0)]), 'seri');
  assert.equal(perTuru([T(12, 0), T(13, 0), T(1, 0)]), null);
  assert.equal(perTuru([T(13, 0), T(1, 0), T(2, 0)]), null);
  assert.equal(perTuru([T(3, 0), T(1, 0), T(2, 0)]), 'seri');
  assert.equal(perTuru(Array.from({ length: 13 }, (_, i) => T(i + 1, 2))), 'seri');
  assert.equal(perTuru([T(4, 0), T(5, 0), T(5, 0, 1)]), null, 'kopya taşlı seri');
  assert.equal(perTuru([T(4, 0), T(5, 0), T(5, 0, 1), T(6, 0)]), null);
  assert.equal(perTuru([T(4, 0), T(5, 1), T(6, 0)]), null, 'karışık renk');
  assert.equal(perTuru([T(4, 0), T(6, 0), T(7, 0)]), null, 'boşluklu');
  assert.equal(perTuru([T(4, 0), T(5, 0)]), null, '2 taş');
  assert.equal(perTuru([]), null);
  assert.equal(perTuru([T(7, 0), T(7, 1), T(7, 2)]), 'grup');
  assert.equal(perTuru([T(7, 0), T(7, 1), T(7, 2), T(7, 3)]), 'grup');
  assert.equal(perTuru([T(7, 0), T(7, 1), T(7, 1, 1)]), null, 'aynı renk iki kez');
  assert.equal(perTuru([T(7, 0), T(7, 1), T(7, 2), T(7, 3), T(7, 0, 1)]), null, '5li grup');
  assert.equal(perTuru([T(7, 0), T(7, 1)]), null);
  assert.equal(perTuru([T(7, 0), T(7, 0), T(7, 1)]), null, 'aynı kimlik iki kez');
  assert.equal(perTuru([T(7, 0), T(7, 1), { id: 200, s: 14, r: 2 }]), null);
  assert.equal(perTuru(null as never), null);
  assert.deepEqual(perDiz([T(5, 1), T(3, 1), T(4, 1)]).map((t) => t.s), [3, 4, 5]);
  assert.deepEqual(perDiz([T(5, 3), T(5, 0), T(5, 2)]).map((t) => t.r), [0, 2, 3]);
});
sina('işleme uçları', () => {
  const perler = [P(0, [T(3, 0), T(4, 0), T(5, 0)]), P(1, [T(1, 1), T(2, 1), T(3, 1)]), P(2, [T(11, 2), T(12, 2), T(13, 2)]), P(3, [T(9, 0), T(9, 1), T(9, 3)]), P(4, [T(8, 0), T(8, 1), T(8, 2), T(8, 3)])];
  assert.deepEqual(islemeYerleri(T(2, 0), perler), [{ per: 0, uc: 'bas' }]);
  assert.deepEqual(islemeYerleri(T(6, 0, 1), perler), [{ per: 0, uc: 'son' }]);
  assert.deepEqual(islemeYerleri(T(7, 0), perler), []);
  assert.deepEqual(islemeYerleri(T(4, 0, 1), perler), [], 'araya sokma yok');
  assert.deepEqual(islemeYerleri(T(2, 2), perler), [], 'renk tutmuyor');
  assert.deepEqual(islemeYerleri(T(13, 1), perler), [], '1in altına inilmez');
  assert.deepEqual(islemeYerleri(T(1, 2), perler), [], '13ten sonra 1 gelmez');
  assert.deepEqual(islemeYerleri(T(10, 2), perler), [{ per: 2, uc: 'bas' }]);
  assert.deepEqual(islemeYerleri(T(4, 1), perler), [{ per: 1, uc: 'son' }]);
  assert.deepEqual(islemeYerleri(T(9, 2), perler), [{ per: 3, uc: null }]);
  assert.deepEqual(islemeYerleri(T(9, 1, 1), perler), [], 'grupta renk var');
  assert.deepEqual(islemeYerleri(T(8, 0, 1), perler), [], '4lü gruba eklenmez');
});
sina('eldeki perler, sıralama, ipucu, plan', () => {
  const el = [T(3, 0), T(4, 0), T(5, 0), T(6, 0), T(4, 0, 1), T(9, 0), T(9, 1), T(9, 2), T(9, 3)];
  const pp = eldekiPerler(el);
  assert.equal(pp.length, 3 + 5, '3-4-5,4-5-6,3-6 + 4lü ve dört 3lü');
  assert.ok(pp.every((p) => perTuru(p)));
  assert.deepEqual(elSirala([T(5, 1), T(3, 0), T(5, 0), T(4, 1)], 'seri'), [T(3, 0).id, T(5, 0).id, T(4, 1).id, T(5, 1).id]);
  assert.deepEqual(elSirala([T(5, 1), T(3, 0), T(5, 0), T(4, 1)], 'grup'), [T(3, 0).id, T(4, 1).id, T(5, 0).id, T(5, 1).id]);
  // 5'leri grup açmak (3 taş) yerine 5-6-7 açıp kalan iki 5'i işlemek eli bitirir (5 taş, 3 hamle; beş işleme de 5 taş ama daha uzun)
  const d = D({ eller: [[T(5, 0), T(5, 1), T(5, 2), T(6, 0), T(7, 0)], HURDA], acti: [true, false], perler: [P(0, [T(2, 0), T(3, 0), T(4, 0)]), P(1, [T(2, 1), T(3, 1), T(4, 1)]), P(2, [T(6, 2), T(7, 2), T(8, 2)])] });
  const g = yediliMotor.gorunum(d, 'o0') as OkeyGorunum;
  const plan = enIyiPlan(g, 'o0');
  assert.deepEqual(plan.map((h) => h.t), ['ac', 'isle', 'isle']);
  let dd = d;
  for (const h of plan) dd = oyna(dd, 'o0', h).durum;
  assert.ok(dd.bitti);
  assert.deepEqual(enIyiPlan(g, 'o1'), []);
  assert.deepEqual(ipuclari(g, 'o1'), []);
  const ip = ipuclari(g, 'o0');
  assert.equal(ip.filter((x) => x.hamle.t === 'ac').length, 2, '5 grubu + 5-6-7 serisi');
  assert.equal(ip.filter((x) => x.hamle.t === 'isle').length, 3);
  for (const x of ip) oyna(d, 'o0', x.hamle);
  // Açınca doğan hakla işleme (açmadan önce hak yok): 3-6 serisi + masadaki seriye 2
  const d2 = D({ eller: [[T(3, 0), T(4, 0), T(5, 0), T(6, 0, 1), T(2, 1)], HURDA], perler: [P(0, [T(3, 1), T(4, 1), T(5, 1)])] });
  const p2 = enIyiPlan(yediliMotor.gorunum(d2, 'o0') as OkeyGorunum, 'o0');
  assert.deepEqual(p2.map((h) => h.t), ['ac', 'isle']);
  let d3 = d2;
  for (const h of p2) d3 = oyna(d3, 'o0', h).durum;
  assert.ok(d3.bitti);
  // Eşitlikte az hamle: 6 taşlık tek seri (1 hamle), iki 3'lü değil
  const d4 = D({ eller: [[1, 2, 3, 4, 5, 6].map((s) => T(s, 2)).concat(HURDA2), HURDA] });
  assert.equal(enIyiPlan(yediliMotor.gorunum(d4, 'o0') as OkeyGorunum, 'o0').length, 1);
});

console.log('Birim: tur akışı ve ihlaller');
const SERI = P(0, [T(3, 0), T(4, 0), T(5, 0)]);
sina('yalnız işlek ihlali (cek ile)', () => {
  const d = D({ eller: [[T(6, 0), ...HURDA.slice(1)], HURDA2], acti: [true, false], perler: [SERI], deste: [T(12, 1), T(12, 3)] });
  assert.deepEqual(zorunlu(yediliMotor.gorunum(d, 'o0') as OkeyGorunum, 'o0'), { per: false, islek: true });
  const s = oyna(d, 'o0', { t: 'cek' });
  assert.deepEqual(cezaTur(s.durum, 0), ['islek']);
  assert.deepEqual(s.durum.oyuncular[0].cezalar[0], { tur: 'islek', puan: -5, aciklama: 'İşlek taşı işlemedi' });
  assert.deepEqual(turler(s.olaylar), ['ceza', 'cekti', 'cektim', 'sira']);
  assert.equal(s.olaylar[1].cezaTasi, true);
  assert.equal(s.olaylar[2].kime, 'o0');
  assert.equal(s.durum.oyuncular[0].el.length, 5);
  assert.equal(s.durum.deste.length, 1);
  assert.equal(s.durum.sira, 1);
  assert.equal(s.olaylar[3].o, 'o1');
});
sina('yalnız per ihlali (devret ile; işleme hakkı yokken işlek sayılmaz)', () => {
  const d = D({ eller: [[T(6, 0), T(1, 2), T(2, 2), T(3, 2), T(13, 3)], HURDA2], perler: [SERI], deste: [T(12, 1)] });
  const s = oyna(d, 'o0', { t: 'devret' });
  assert.deepEqual(cezaTur(s.durum, 0), ['per']);
  assert.deepEqual(s.durum.oyuncular[0].cezalar[0], { tur: 'per', puan: -5, aciklama: 'Açabileceği peri bekletti' });
  assert.deepEqual(turler(s.olaylar), ['ceza', 'cekti', 'cektim', 'sira']);
  assert.equal(s.durum.oyuncular[0].el.length, 6);
  assert.equal(s.durum.sira, 1);
  assert.equal(oyna(d, 'o0', { t: 'cek' }).durum.oyuncular[0].cezalar.length, 1);
});
sina('iki ihlal birden (cek ve devret)', () => {
  const d = D({ eller: [[T(6, 0), T(1, 2), T(2, 2), T(3, 2), T(13, 3)], HURDA2], acti: [true, false], perler: [SERI], deste: [T(12, 1), T(12, 3)] });
  for (const t of ['cek', 'devret']) {
    const s = oyna(d, 'o0', { t });
    assert.deepEqual(cezaTur(s.durum, 0), ['islek', 'per']);
    assert.deepEqual(turler(s.olaylar), ['ceza', 'ceza', 'cekti', 'cektim', 'sira']);
    assert.equal(s.durum.oyuncular[0].el.length, 6, 'tek ceza taşı');
    assert.equal(s.durum.sira, 1);
  }
});
sina('deste boşken ihlal: ceza yazılır, taş çekilmez', () => {
  const d = D({ eller: [[T(6, 0), ...HURDA.slice(1)], HURDA2], acti: [true, false], perler: [SERI] });
  const s = oyna(d, 'o0', { t: 'devret' });
  assert.deepEqual(cezaTur(s.durum, 0), ['islek']);
  assert.deepEqual(turler(s.olaylar), ['ceza', 'sira']);
  assert.equal(s.durum.oyuncular[0].el.length, 4);
});
sina('çektikten sonra doğan zorunluluk: devret ihlal, ikinci taş da çekilir', () => {
  const d = D({ eller: [[T(1, 2), T(2, 2), ...HURDA.slice(1)], HURDA2], deste: [T(12, 1), T(3, 2)] });
  const c = oyna(d, 'o0', { t: 'cek' });
  assert.deepEqual(turler(c.olaylar), ['cekti', 'cektim']);
  assert.equal(c.durum.sira, 0);
  assert.deepEqual([c.durum.cekti, c.durum.hamleYapti], [true, false]);
  assert.deepEqual((yediliMotor.gorunum(c.durum, 'o0') as OkeyGorunum).tur_, { cekti: true, hamleYapti: false });
  const s = oyna(c.durum, 'o0', { t: 'devret' });
  assert.deepEqual(cezaTur(s.durum, 0), ['per']);
  assert.equal(s.durum.oyuncular[0].el.length, 7);
  assert.equal(s.durum.deste.length, 0);
  // Kurala uyan: açıp devreder
  const a = oyna(c.durum, 'o0', { t: 'ac', taslar: [T(3, 2).id, T(1, 2).id, T(2, 2).id] });
  assert.deepEqual(a.durum.perler[0].taslar.map((t) => t.s), [1, 2, 3]);
  const v = oyna(a.durum, 'o0', { t: 'devret' });
  assert.deepEqual(turler(v.olaylar), ['devretti', 'sira']);
  assert.equal(v.durum.oyuncular[0].cezalar.length, 0);
});
sina('önce taş çek · çekip devretme · çift çekme · hamleden sonra çekme', () => {
  const d = D({ eller: [HURDA, HURDA2], deste: [T(12, 1), T(12, 3)] });
  hata(d, 'o0', { t: 'devret' }, 'Önce taş çekmelisin.');
  hata(d, 'o1', { t: 'cek' }, 'Sıra sende değil.');
  const c = oyna(d, 'o0', { t: 'cek' });
  assert.equal(c.durum.oyuncular[0].el.at(-1)!.id, T(12, 3).id);
  hata(c.durum, 'o0', { t: 'cek' }, 'Bu turda zaten taş çektin.');
  const v = oyna(c.durum, 'o0', { t: 'devret' });
  assert.equal(v.durum.sira, 1);
  assert.deepEqual([v.durum.cekti, v.durum.hamleYapti], [false, false]);
  const d2 = D({ eller: [[T(1, 2), T(2, 2), T(3, 2), ...HURDA.slice(1)], HURDA2], deste: [T(12, 1)] });
  const a = oyna(d2, 'o0', { t: 'ac', taslar: [T(1, 2).id, T(2, 2).id, T(3, 2).id] });
  assert.deepEqual(turler(a.olaylar), ['acti']);
  hata(a.durum, 'o0', { t: 'cek' }, 'Hamle yaptıktan sonra taş çekemezsin.');
  assert.equal(oyna(a.durum, 'o0', { t: 'devret' }).durum.sira, 1, 'hamle yaptıysa çekmeden devreder');
  // Deste boşken çekme: taş yok ama cekti=true, sonra devredebilir
  const d3 = D({ eller: [HURDA, HURDA2] });
  const c3 = oyna(d3, 'o0', { t: 'cek' });
  assert.deepEqual(turler(c3.olaylar), ['cekti']);
  assert.equal(c3.durum.cekti, true);
  assert.equal(c3.durum.oyuncular[0].el.length, 4);
});
sina('geçersiz hamleler', () => {
  const d = D({ eller: [[T(1, 2), T(2, 2), T(3, 2), T(6, 0), T(9, 1)], [T(4, 2), ...HURDA2]], perler: [SERI], deste: [T(12, 1)] });
  for (const h of [null, undefined, 5, 'cek', [], {}, { t: 'at', tas: 1 }, { t: 'ac' }, { t: 'ac', taslar: 'x' }, { t: 'ac', taslar: [1, 'a', 2] }, { t: 'ac', taslar: [1.5, 2, 3] }, { t: 'isle' }, { t: 'isle', tas: '1', per: 0 }, { t: 'isle', tas: T(6, 0).id, per: 0, uc: 'orta' }]) hata(d, 'o0', h, 'Geçersiz hamle.');
  hata(d, 'o0', { t: 'ac', taslar: [T(1, 2).id, T(2, 2).id, T(2, 2).id] }, 'Aynı taş iki kez seçilemez.');
  hata(d, 'o0', { t: 'ac', taslar: [T(1, 2).id, T(2, 2).id, T(4, 2).id] }, 'Bu taş elinde değil.');
  hata(d, 'o0', { t: 'ac', taslar: [T(1, 2).id, T(2, 2).id, T(9, 1).id] }, 'Bu taşlar geçerli bir per değil.');
  hata(d, 'o0', { t: 'ac', taslar: [T(1, 2).id, T(2, 2).id] }, 'Bu taşlar geçerli bir per değil.');
  hata(d, 'o0', { t: 'isle', tas: T(6, 0).id, per: 0 }, 'Önce per açmalısın.');
  hata(d, 'o0', { t: 'isle', tas: T(4, 2).id, per: 0 }, 'Bu taş elinde değil.');
  hata(d, 'yabanci', { t: 'cek' }, 'Bu masada oyuncu değilsin.');
  const a = oyna(d, 'o0', { t: 'ac', taslar: [T(1, 2).id, T(2, 2).id, T(3, 2).id] }).durum;
  hata(a, 'o0', { t: 'isle', tas: T(9, 1).id, per: 0 }, 'Bu taş o pere uymuyor.');
  hata(a, 'o0', { t: 'isle', tas: T(6, 0).id, per: 7 }, 'Böyle bir per yok.');
  hata(a, 'o0', { t: 'isle', tas: T(6, 0).id, per: 0, uc: 'bas' }, 'Bu taş perin o ucuna uymuyor.');
  const s = oyna(a, 'o0', { t: 'isle', tas: T(6, 0).id, per: 0, uc: 'son' });
  assert.deepEqual(s.olaylar[0], { t: 'isledi', o: 'o0', per: 0, tas: T(6, 0), uc: 'son' });
  assert.deepEqual(s.durum.perler[0].taslar.map((t) => t.s), [3, 4, 5, 6]);
  assert.equal(a.perler[1].id, 1);
});
sina('son taşı işleyerek bitirme ve puan', () => {
  const c: Ceza = { tur: 'per', puan: -5, aciklama: 'Açabileceği peri bekletti' };
  const d = D({ eller: [[T(2, 0)], HURDA, HURDA2], acti: [true, false, false], perler: [SERI], deste: [T(12, 1)], cezalar: [[c], [], [c, c]] });
  const s = oyna(d, 'o0', { t: 'isle', tas: T(2, 0).id, per: 0 });
  assert.deepEqual(turler(s.olaylar), ['isledi', 'elBitti']);
  assert.equal(s.olaylar[0].uc, 'bas');
  assert.ok(s.durum.bitti);
  const son = yediliMotor.sonuc(s.durum)!;
  assert.equal(son.neden, 'bitti');
  assert.deepEqual(son.kazananlar, ['o0']);
  assert.equal(son.kazananTakim, undefined);
  assert.deepEqual(son.satirlar.map((x) => [x.puan, x.kalan, x.kazandi]), [[-5, 0, true], [-4, 4, false], [-13, 3, false]]);
  assert.equal(son.satirlar[2].aciklama, '3 taş (−3) · 2 ceza (−10)');
  hata(s.durum, 'o1', { t: 'cek' }, 'El bitti.');
  assert.equal(yediliMotor.botHamle(s.durum, 'o1', rng0), null);
  assert.equal(yediliMotor.sonuc(d), null);
  // Açarak bitirme
  const d2 = D({ eller: [[T(7, 0), T(7, 1), T(7, 2)], HURDA] });
  assert.deepEqual(yediliMotor.sonuc(oyna(d2, 'o0', { t: 'ac', taslar: [T(7, 0).id, T(7, 1).id, T(7, 2).id] }).durum)!.kazananlar, ['o0']);
});
sina('kilit: deste boşken herkes eritemeden döner → berabere', () => {
  let d = D({ eller: [HURDA, HURDA2, [T(3, 3), T(8, 1)]] });
  for (const o of ['o0', 'o1', 'o2']) {
    assert.ok(!d.bitti);
    d = oyna(d, o, { t: 'cek' }).durum;
    const s = oyna(d, o, { t: 'devret' });
    d = s.durum;
    if (o === 'o2') assert.deepEqual(turler(s.olaylar), ['devretti', 'elBitti']);
  }
  const son = yediliMotor.sonuc(d)!;
  assert.equal(son.neden, 'berabere');
  assert.deepEqual(son.kazananlar, []);
  assert.deepEqual(son.satirlar.map((x) => [x.puan, x.kazandi]), [[-4, false], [-3, false], [-2, false]]);
  // Araya eritme girerse sayaç sıfırlanır; ihlalli tur da sayılır
  let e = D({ eller: [[T(7, 0), T(7, 1), T(7, 2), T(1, 3)], HURDA2], perler: [] });
  e = oyna(e, 'o0', { t: 'devret' }).durum; // per ihlali, kuru=1
  assert.deepEqual([e.kuru, e.bitti, cezaTur(e, 0).length], [1, false, 1]);
  e = oyna(oyna(e, 'o1', { t: 'cek' }).durum, 'o1', { t: 'devret' }).durum;
  assert.equal(yediliMotor.sonuc(e)!.neden, 'berabere');
  assert.equal(yediliMotor.sonuc(e)!.satirlar[0].puan, -9);
  let f = D({ eller: [[T(7, 0), T(7, 1), T(7, 2), T(1, 3)], HURDA2] });
  f = oyna(oyna(f, 'o0', { t: 'ac', taslar: [T(7, 0).id, T(7, 1).id, T(7, 2).id] }).durum, 'o0', { t: 'devret' }).durum;
  assert.deepEqual([f.kuru, f.bitti], [0, false]);
});

console.log('Birim: seriyi bölerek işleme');
sina('bölme: geçerli yerler, parça <3 ret, uç sayı normal işleme, grup bölünmez', () => {
  const uzun = P(0, [3, 4, 5, 6, 7].map((s) => T(s, 0)), 'o1');
  const perler = [uzun, P(1, [T(9, 0), T(9, 1), T(9, 3)]), P(2, [T(8, 0), T(8, 1), T(8, 2), T(8, 3)]), P(3, [3, 4, 5, 6].map((s) => T(s, 1)))];
  assert.deepEqual(islemeYerleri(T(5, 0, 1), perler), [{ per: 0, uc: 'bol' }]);
  assert.deepEqual(islemeYerleri(T(4, 0, 1), perler), [], 'alt parça 2 taş');
  assert.deepEqual(islemeYerleri(T(6, 0, 1), perler), [], 'üst parça 2 taş');
  assert.deepEqual(islemeYerleri(T(3, 0, 1), perler), []);
  assert.deepEqual(islemeYerleri(T(7, 0, 1), perler), []);
  assert.deepEqual(islemeYerleri(T(5, 1, 1), perler), [], '4 taşlık seri bölünmez');
  assert.deepEqual(islemeYerleri(T(5, 2), perler), [], 'renk tutmuyor');
  assert.deepEqual(islemeYerleri(T(2, 0), perler), [{ per: 0, uc: 'bas' }], 'uç sayı normal işleme');
  assert.deepEqual(islemeYerleri(T(8, 0, 1), perler), [{ per: 0, uc: 'son' }], 'uç normal işleme; 4lü grup bölünmez/eklenmez');
  assert.deepEqual(islemeYerleri(T(9, 0, 1), perler), [], 'grup bölünmez');
  const d = D({ eller: [[T(5, 0, 1), T(4, 0, 1), ...HURDA.slice(1)], HURDA2], acti: [true, false], perler: [uzun], deste: [T(12, 1)] });
  hata(d, 'o0', { t: 'isle', tas: T(4, 0, 1).id, per: 0 }, 'Bu taş o pere uymuyor.');
  hata(d, 'o0', { t: 'isle', tas: T(5, 0, 1).id, per: 0, uc: 'bas' }, 'Bu taş perin o ucuna uymuyor.');
  hata(d, 'o0', { t: 'isle', tas: T(5, 0, 1).id, per: 0, uc: 'son' }, 'Bu taş perin o ucuna uymuyor.');
  hata(d, 'o0', { t: 'isle', tas: T(5, 0, 1).id, per: 0, uc: 'bol' }, 'Geçersiz hamle.');
  hata({ ...d, oyuncular: d.oyuncular.map((o) => ({ ...o, acti: false })) }, 'o0', { t: 'isle', tas: T(5, 0, 1).id, per: 0 }, 'Önce per açmalısın.');
  const s = oyna(d, 'o0', { t: 'isle', tas: T(5, 0, 1).id, per: 0 });
  assert.deepEqual(s.olaylar, [{ t: 'isledi', o: 'o0', per: 0, tas: T(5, 0, 1), uc: 'bol', yeniPer: 1 }]);
  assert.deepEqual(s.durum.perler.map((x) => [x.id, x.tur, x.sahip, x.taslar.map((t) => t.id)]), [
    [0, 'seri', 'o1', [T(3, 0).id, T(4, 0).id, T(5, 0, 1).id]],
    [1, 'seri', 'o0', [T(5, 0).id, T(6, 0).id, T(7, 0).id]],
  ]);
  assert.equal(s.durum.hamleYapti, true);
  // Bölünce 4 artık alt parçanın sonuna uymaz ama zincir: 9 taşlık seride bölme + doğan parçalara işleme
  const g = yediliMotor.gorunum(d, 'o0') as OkeyGorunum;
  const ip = ipuclari(g, 'o0');
  assert.equal(ip.length, 1);
  assert.deepEqual(ip[0].hamle, { t: 'isle', tas: T(5, 0, 1).id, per: 0 });
  assert.equal(ip[0].aciklama, '5 taşını 3–7 serisini bölerek işle');
  assert.deepEqual(zorunlu(g, 'o0'), { per: false, islek: true });
});
sina('bölme: işlek cezası, bölmeyle bitirme, plan zinciri, takım', () => {
  const uzun = P(0, [3, 4, 5, 6, 7].map((s) => T(s, 0)), 'o1');
  const d = D({ eller: [[T(5, 0, 1), ...HURDA.slice(1)], HURDA2], acti: [true, false], perler: [uzun], deste: [T(12, 1)] });
  for (const t of ['devret', 'cek']) {
    const c = oyna(d, 'o0', { t });
    assert.deepEqual(cezaTur(c.durum, 0), ['islek']);
    assert.deepEqual(turler(c.olaylar), ['ceza', 'cekti', 'cektim', 'sira']);
  }
  assert.deepEqual(yediliMotor.botHamle(d, 'o0', rng0), { t: 'isle', tas: T(5, 0, 1).id, per: 0 });
  const b = oyna(D({ eller: [[T(5, 0, 1)], HURDA2], acti: [true, false], perler: [uzun] }), 'o0', { t: 'isle', tas: T(5, 0, 1).id, per: 0 });
  assert.deepEqual(turler(b.olaylar), ['isledi', 'elBitti']);
  assert.deepEqual(yediliMotor.sonuc(b.durum)!.kazananlar, ['o0']);
  assert.equal(b.durum.perler.length, 2);
  // Zincir: 6 tek başına işlenemez; 5 ile bölününce alt parça 3-4-5 olur ve 6 onun sonuna işlenir
  let z = D({ eller: [[T(6, 0, 1), T(5, 0, 1)], HURDA2], acti: [true, false], perler: [uzun] });
  const plan = enIyiPlan(yediliMotor.gorunum(z, 'o0') as OkeyGorunum, 'o0');
  assert.deepEqual(plan, [{ t: 'isle', tas: T(5, 0, 1).id, per: 0 }, { t: 'isle', tas: T(6, 0, 1).id, per: 0 }]);
  for (const h of plan) z = oyna(z, 'o0', h).durum;
  assert.ok(z.bitti);
  assert.deepEqual(z.perler.map((x) => x.taslar.map((t) => t.s)), [[3, 4, 5, 6], [5, 6, 7]]);
  // Takım: arkadaşın açılışıyla bölme hakkı; rakipte yok; hediye doğmaz
  const t = D({ tur: 'takim', eller: [HURDA, [T(5, 0, 1), T(2, 3)], [T(5, 0, 1), T(10, 3)], HURDA2], acti: [true, false, false, false], perler: [uzun], sira: 2, deste: [T(12, 1), T(12, 3)] });
  assert.deepEqual(turler(oyna(t, 'o2', { t: 'isle', tas: T(5, 0, 1).id, per: 0 }).olaylar), ['isledi']);
  hata({ ...t, sira: 1 }, 'o1', { t: 'isle', tas: T(5, 0, 1).id, per: 0 }, 'Önce per açmalısın.');
});

console.log('Birim: takım');
const GRUP3 = P(0, [T(9, 0), T(9, 1), T(9, 3)], 'o0');
sina('takım açılışıyla işleme hakkı; per zorunluluğu kişisel', () => {
  const d = D({ tur: 'takim', eller: [HURDA, HURDA2, [T(6, 0), T(10, 3)], [T(2, 0), T(10, 1)]], acti: [true, false, false, false], perler: [SERI], sira: 2, deste: [T(12, 1), T(12, 3)] });
  const g = takimMotor.gorunum(d, 'o2') as OkeyGorunum;
  assert.deepEqual(g.oyuncular.map((o) => [o.takim, o.acti, o.takimActi]), [['A', true, true], ['B', false, false], ['A', false, true], ['B', false, false]]);
  assert.deepEqual(zorunlu(g, 'o2'), { per: false, islek: true });
  const s = oyna(d, 'o2', { t: 'isle', tas: T(6, 0).id, per: 0 });
  assert.equal(s.durum.oyuncular[2].acti, false, 'işlemek per açmış saymaz');
  assert.deepEqual(cezaTur(oyna(d, 'o2', { t: 'cek' }).durum, 2), ['islek']);
  const d1 = { ...d, sira: 3 };
  assert.deepEqual(zorunlu(takimMotor.gorunum(d1, 'o3') as OkeyGorunum, 'o3'), { per: false, islek: false });
  hata(d1, 'o3', { t: 'isle', tas: T(2, 0).id, per: 0 }, 'Önce per açmalısın.');
  assert.deepEqual(turler(oyna(d1, 'o3', { t: 'cek' }).olaylar), ['cekti', 'cektim']);
  // Yedili modunda aynı durumda başkasının açılışı hak vermez
  hata({ ...d, tur: 'yedili' }, 'o2', { t: 'isle', tas: T(6, 0).id, per: 0 }, 'Önce per açmalısın.');
});
sina('hediye: 4. taşı işleme, 4lü açma, deste yettiği kadar, bitirişte yok, yedilide yok', () => {
  const eller = [[T(9, 2), T(1, 0)], HURDA2, HURDA, [T(3, 3), T(8, 1)]];
  const d = D({ tur: 'takim', eller, acti: [true, false, false, false], perler: [GRUP3], deste: [T(12, 1), T(12, 3), T(12, 2)] });
  const s = oyna(d, 'o0', { t: 'isle', tas: T(9, 2).id, per: 0 });
  assert.deepEqual(turler(s.olaylar), ['isledi', 'hediye', 'cektim', 'cektim']);
  assert.deepEqual(s.olaylar[1].kimler, ['o1', 'o3']);
  assert.deepEqual(s.olaylar.slice(2).map((o) => o.kime), ['o1', 'o3']);
  assert.deepEqual(s.durum.oyuncular.map((o) => o.el.length), [1, 4, 4, 3]);
  assert.deepEqual(s.durum.perler[0].taslar.map((t) => t.r), [0, 1, 2, 3]);
  assert.equal(s.durum.sira, 0);
  // Deste 1 taş: yalnız sıradaki ilk rakip
  const t = oyna({ ...d, deste: [T(12, 1)] }, 'o0', { t: 'isle', tas: T(9, 2).id, per: 0 });
  assert.deepEqual(t.olaylar[1].kimler, ['o1']);
  assert.deepEqual(turler(oyna({ ...d, deste: [] }, 'o0', { t: 'isle', tas: T(9, 2).id, per: 0 }).olaylar), ['isledi']);
  // Hamleyi yapandan sonraki oturma sırası: o3 oynarsa önce o0, sonra o2
  const d3 = D({ tur: 'takim', eller: [HURDA, HURDA2, [T(3, 3), T(8, 1)], [T(9, 2), T(1, 0)]], acti: [false, false, false, true], perler: [GRUP3], sira: 3, deste: [T(12, 1), T(12, 3)] });
  assert.deepEqual(oyna(d3, 'o3', { t: 'isle', tas: T(9, 2).id, per: 0 }).olaylar[1].kimler, ['o0', 'o2']);
  // 4'lü açma
  const d4 = D({ tur: 'takim', eller: [[T(4, 0), T(4, 1), T(4, 2), T(4, 3), T(1, 0)], HURDA2], deste: [T(12, 1), T(12, 3)] });
  const ids4 = [0, 1, 2, 3].map((r) => T(4, r).id);
  assert.deepEqual(turler(oyna(d4, 'o0', { t: 'ac', taslar: ids4 }).olaylar), ['acti', 'hediye', 'cektim']);
  assert.deepEqual(turler(oyna(d4, 'o0', { t: 'ac', taslar: ids4.slice(1) }).olaylar), ['acti'], '3lü hediye vermez');
  // Bitirişte hediye yok
  const d5 = D({ tur: 'takim', eller: [[T(9, 2)], HURDA2], acti: [true, false], perler: [GRUP3], deste: [T(12, 1)] });
  const b = oyna(d5, 'o0', { t: 'isle', tas: T(9, 2).id, per: 0 });
  assert.deepEqual(turler(b.olaylar), ['isledi', 'elBitti']);
  assert.equal(b.durum.deste.length, 1);
  // Yedili modunda hediye yok
  assert.deepEqual(turler(oyna({ ...d, tur: 'yedili' }, 'o0', { t: 'isle', tas: T(9, 2).id, per: 0 }).olaylar), ['isledi']);
});
sina('takım puanı', () => {
  const c: Ceza = { tur: 'islek', puan: -5, aciklama: 'İşlek taşı işlemedi' };
  const d = D({ tur: 'takim', eller: [HURDA, [T(9, 2)], HURDA2, [T(3, 3), T(8, 1)]], acti: [false, false, false, true], perler: [GRUP3], sira: 1, cezalar: [[c], [c], [], []] });
  const s = oyna(d, 'o1', { t: 'isle', tas: T(9, 2).id, per: 0 });
  const son = takimMotor.sonuc(s.durum)!;
  assert.equal(son.kazananTakim, 'B');
  assert.deepEqual(son.kazananlar, ['o1', 'o3']);
  assert.deepEqual(son.satirlar.map((x) => [x.id, x.puan, x.kalan, x.kazandi]), [['o0', -9, 4, false], ['o1', -5, 0, true], ['o2', -3, 3, false], ['o3', 0, 2, true]]);
  assert.deepEqual(s.olaylar.at(-1), { t: 'elBitti', neden: 'bitti', kazananlar: ['o1', 'o3'] });
});

console.log('Birim: dağıtım, görünüm, gizlilik, bot');
sina('elBaslat', () => {
  for (const m of [yediliMotor, takimMotor]) for (let n = 2; n <= 6; n++) {
    const d = m.elBaslat({ oyuncular: Array.from({ length: n }, (_, i) => ({ id: 'o' + i, takim: i % 2 ? 'B' as const : 'A' as const })), elNo: 3, baslayan: n - 1, rng: tohumlu(n) }) as YediliDurum;
    const et = m === takimMotor && n >= 5 ? 4 : 7;
    assert.ok(d.oyuncular.every((o) => o.el.length === et));
    assert.equal(d.deste.length, 104 - et * n);
    assert.equal(d.sira, n - 1);
    assert.equal(d.elNo, 3);
    assert.equal(new Set([...d.deste, ...d.oyuncular.flatMap((o) => o.el)].map((t) => t.id)).size, 104);
    assert.deepEqual(JSON.parse(JSON.stringify(d)), d, 'düz JSON');
    assert.equal(m.gorunum(d, 'o0').sira, 'o' + (n - 1));
  }
  const a = JSON.stringify(yediliMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }], elNo: 1, baslayan: 0, rng: tohumlu(7) }));
  assert.equal(a, JSON.stringify(yediliMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }], elNo: 1, baslayan: 0, rng: tohumlu(7) })), 'tohumla yinelenebilir');
  assert.notEqual(a, JSON.stringify(yediliMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }], elNo: 1, baslayan: 0, rng: tohumlu(8) })));
  assert.throws(() => yediliMotor.elBaslat({ oyuncular: [{ id: 'a' }], elNo: 1, baslayan: 0, rng: rng0 }));
  assert.deepEqual([yediliMotor.tur, yediliMotor.min, yediliMotor.max, takimMotor.tur], ['yedili', 2, 6, 'takim']);
});
/** Açık (kime'siz) olayda yalnız masaya inen taşlar bulunabilir */
const acikTaslar = (ol: Olay[]): number[] => ol.filter((o) => o.kime === undefined).flatMap((o) => {
  if (o.t === 'acti') return (o.perler as Per[]).flatMap((p) => p.taslar.map((t) => t.id));
  if (o.t === 'isledi') return [(o.tas as Tas).id];
  assert.ok(!('tas' in o) && !('taslar' in o) && !('el' in o), 'açık olayda taş: ' + o.t);
  return [];
});
sina('gizlilik: görünüm ve olaylar', () => {
  const d = yediliMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }, { id: 'c' }], elNo: 1, baslayan: 1, rng: tohumlu(42) }) as YediliDurum;
  const idler = (x: unknown): Set<number> => new Set([...JSON.stringify(x).matchAll(/"id":(\d+)/g)].map((m) => +m[1]));
  for (const bakan of ['a', 'b', 'c', null, 'yok']) {
    const g = yediliMotor.gorunum(d, bakan) as OkeyGorunum;
    const benim = d.oyuncular.find((o) => o.id === bakan)?.el ?? [];
    assert.deepEqual(g.elim, benim);
    assert.deepEqual([...idler(g)].sort(), benim.map((t) => t.id).sort(), 'görünümde yalnız kendi eli');
    assert.deepEqual(g.oyuncular.map((o) => o.tasSayisi), [7, 7, 7]);
    assert.equal(g.deste, 83);
    assert.deepEqual(g.tur_, { cekti: false, hamleYapti: false });
    assert.equal(g.sira, 'b');
  }
  const g = yediliMotor.gorunum(d, 'a') as OkeyGorunum;
  g.elim.pop();
  assert.equal(d.oyuncular[0].el.length, 7, 'görünüm durumu paylaşmaz');
  const s = oyna(D({ eller: [HURDA, HURDA2], deste: [T(12, 1)] }), 'o0', { t: 'cek' });
  assert.deepEqual(acikTaslar(s.olaylar), []);
  assert.deepEqual(s.olaylar.filter((o) => o.kime).map((o) => [o.kime, (o.tas as Tas).id]), [['o0', T(12, 1).id]]);
  assert.ok(!JSON.stringify(s.olaylar.filter((o) => !o.kime)).includes('"id"'));
});
sina('bot: önce plan, sonra çek, sonra devret; sırası değilse null', () => {
  let d = D({ eller: [[T(1, 2), T(2, 2), T(3, 2), T(6, 0), T(9, 1)], HURDA2], perler: [SERI], deste: [T(12, 1)] });
  assert.equal(yediliMotor.botHamle(d, 'o1', rng0), null);
  const sira: string[] = [];
  while (d.sira === 0) { const h = yediliMotor.botHamle(d, 'o0', rng0) as { t: string }; sira.push(h.t); d = oyna(d, 'o0', h).durum; }
  assert.deepEqual(sira, ['ac', 'isle', 'devret']);
  assert.equal(d.oyuncular[0].cezalar.length, 0);
  assert.deepEqual(yediliMotor.botHamle(d, 'o1', rng0), { t: 'cek' });
  d = oyna(d, 'o1', { t: 'cek' }).durum;
  assert.deepEqual(yediliMotor.botHamle(d, 'o1', rng0), { t: 'devret' });
});

/* ------------------------------------------------------------------ rastgele oyunlar ------------------------------------------------------------------ */

function degismez(d: YediliDurum): void {
  const hepsi = [...d.deste, ...d.perler.flatMap((p) => p.taslar), ...d.oyuncular.flatMap((o) => o.el)];
  assert.equal(hepsi.length, 104, 'toplam taş');
  assert.equal(new Set(hepsi.map((t) => t.id)).size, 104, 'tekil kimlik');
  for (const t of hepsi) assert.ok(t.id >= 0 && t.id < 104 && t.s === (t.id % 13) + 1 && t.r === Math.floor(t.id / 13) % 4);
  assert.equal(new Set(d.perler.map((p) => p.id)).size, d.perler.length);
  for (const p of d.perler) {
    assert.equal(perTuru(p.taslar), p.tur, 'masadaki per geçerli');
    assert.deepEqual(p.taslar.map((t) => t.id), perDiz(p.taslar).map((t) => t.id), 'per sırası');
  }
  assert.ok(d.sira >= 0 && d.sira < d.oyuncular.length);
}
function puanDenetle(d: YediliDurum, son: ElSonuc): void {
  const bitiren = d.oyuncular.find((o) => o.el.length === 0);
  assert.equal(son.neden, bitiren ? 'bitti' : 'berabere');
  if (!bitiren) assert.equal(d.deste.length, 0, 'berabere yalnız deste boşken');
  const kazandi = (o: YediliDurum['oyuncular'][number]) => !!bitiren && (d.tur === 'takim' ? o.takim === bitiren.takim : o === bitiren);
  assert.deepEqual(son.kazananlar, d.oyuncular.filter(kazandi).map((o) => o.id));
  assert.equal(son.kazananTakim, d.tur === 'takim' && bitiren ? bitiren.takim : undefined);
  son.satirlar.forEach((s, i) => {
    const o = d.oyuncular[i];
    assert.equal(s.id, o.id);
    assert.equal(s.kalan, o.el.length);
    assert.equal(s.kazandi, kazandi(o));
    assert.deepEqual(s.cezalar, o.cezalar);
    assert.ok(o.cezalar.every((c) => c.puan === -5));
    assert.equal(s.puan, (kazandi(o) ? 0 : -o.el.length) - 5 * o.cezalar.length);
    assert.ok(Object.is(s.puan, 0) || s.puan !== 0, '−0 yok');
  });
}
const oyuncuListe = (n: number) => Array.from({ length: n }, (_, i) => ({ id: 'o' + i, takim: (i % 2 ? 'B' : 'A') as 'A' | 'B' }));

console.log('Rastgele oyun (tümü bot)');
let enUzunPlan = 0, yavasPlan = 0;
for (const m of [yediliMotor, takimMotor]) for (let n = 2; n <= 6; n++) {
  const EL = 500, rng = tohumlu(1000 * n + (m.tur === 'takim' ? 7 : 3));
  let hamleTop = 0, enCok = 0, bitti = 0, berabere = 0, hediye = 0;
  for (let e = 0; e < EL; e++) {
    let d = m.elBaslat({ oyuncular: oyuncuListe(n), elNo: e + 1, baslayan: e % n, rng }) as YediliDurum;
    degismez(d);
    let k = 0;
    while (!d.bitti) {
      assert.ok(++k <= 5000, 'el 5.000 hamlede bitmedi');
      const o = d.oyuncular[d.sira].id;
      for (const diger of d.oyuncular) if (diger.id !== o) assert.equal(m.botHamle(d, diger.id, rng), null);
      const t0 = performance.now();
      const h = m.botHamle(d, o, rng);
      const sure = performance.now() - t0;
      enUzunPlan = Math.max(enUzunPlan, sure);
      if (sure > 20) yavasPlan++;
      assert.ok(h, 'bot hamle vermedi');
      const once = k % 50 === 0 ? JSON.stringify(d) : '';
      const s = m.uygula(d, o, h, rng);
      if ('hata' in s) assert.fail(`bot geçersiz hamle: ${JSON.stringify(h)} → ${s.hata}`);
      if (once) assert.equal(JSON.stringify(d), once, 'uygula girdiyi değiştirdi');
      const yeni = s.durum as YediliDurum;
      const masa = new Set(yeni.perler.flatMap((p) => p.taslar.map((t) => t.id)));
      for (const id of acikTaslar(s.olaylar)) assert.ok(masa.has(id), 'açık olaydaki taş masada değil');
      assert.ok(!s.olaylar.some((x) => x.t === 'ceza'), 'bot ceza aldı');
      hediye += s.olaylar.filter((x) => x.t === 'hediye').length;
      d = yeni;
      degismez(d);
    }
    assert.ok(d.oyuncular.every((x) => x.cezalar.length === 0));
    const son = m.sonuc(d)!;
    puanDenetle(d, son);
    son.neden === 'bitti' ? bitti++ : berabere++;
    hamleTop += k; enCok = Math.max(enCok, k);
  }
  console.log(`  ✓ ${m.tur} ${n} oyuncu: ${EL} el · bitti ${bitti} · berabere ${berabere} · ort. ${(hamleTop / EL).toFixed(0)} hamle · en uzun ${enCok}${m.tur === 'takim' ? ` · hediye ${hediye}` : ''}`);
  adet++;
}
console.log(`  bot hamlesi en uzun hesap: ${enUzunPlan.toFixed(1)} ms · 20 ms üstü ${yavasPlan} kez`);
assert.ok(enUzunPlan < 50, 'enIyiPlan 50 ms sınırını aştı');

console.log('Bulanık sınama (kurala uygun/uygunsuz rastgele hamleler)');
for (const m of [yediliMotor, takimMotor]) for (let n = 2; n <= 6; n++) {
  const EL = 200, rng = tohumlu(77 * n + (m.tur === 'takim' ? 5 : 1));
  const sec = <X>(a: X[]): X => a[Math.floor(rng() * a.length)];
  let hamleTop = 0, hataTop = 0, cezaTop = 0, biten = 0;
  for (let e = 0; e < EL; e++) {
    let d = m.elBaslat({ oyuncular: oyuncuListe(n), elNo: e + 1, baslayan: e % n, rng }) as YediliDurum;
    for (let k = 0; k < 3000 && !d.bitti; k++) {
      const sirali = d.oyuncular[d.sira];
      let o = sirali.id, h: unknown;
      const g = m.gorunum(d, o) as OkeyGorunum;
      const z = zorunlu(g, o), ip = ipuclari(g, o), zar = rng();
      assert.equal(z.per || z.islek, ip.length > 0, 'zorunluluk ⇔ ipucu var');
      if (zar < 0.45) h = m.botHamle(d, o, rng);
      else if (zar < 0.6 && ip.length) h = sec(ip).hamle;
      else if (zar < 0.72) h = { t: 'cek' };
      else if (zar < 0.84) h = { t: 'devret' };
      else if (zar < 0.88) { o = sec(d.oyuncular).id; h = sec([{ t: 'cek' }, { t: 'devret' }, m.botHamle(d, sirali.id, rng)]); }
      else if (zar < 0.94) h = { t: 'ac', taslar: Array.from({ length: 2 + Math.floor(rng() * 4) }, () => (rng() < 0.7 && sirali.el.length ? sec(sirali.el).id : Math.floor(rng() * 110) - 3)) };
      else if (zar < 0.98) h = { t: 'isle', tas: rng() < 0.7 && sirali.el.length ? sec(sirali.el).id : Math.floor(rng() * 110), per: Math.floor(rng() * (d.perler.length + 2)) - 1, ...(rng() < 0.3 ? { uc: sec(['bas', 'son']) } : {}) };
      else h = sec<unknown>([null, 7, 'x', {}, { t: 'at', tas: 3 }, { t: 'ac', taslar: null }, { t: 'isle', tas: {}, per: [] }, [], { t: 'cek', kaynak: 'atik' }]);
      const once = JSON.stringify(d);
      let s: ReturnType<typeof m.uygula>;
      try { s = m.uygula(d, o, h, rng); } catch (x) { assert.fail(`motor istisna fırlattı: ${JSON.stringify(h)} → ${x}`); }
      assert.equal(JSON.stringify(d), once, 'uygula girdiyi değiştirdi');
      hamleTop++;
      if ('hata' in s) { assert.ok(typeof s.hata === 'string' && s.hata.length > 0); hataTop++; continue; }
      assert.equal(o, sirali.id, 'sırası olmayan oyuncunun hamlesi kabul edildi');
      const yeni = s.durum as YediliDurum, cezalar = s.olaylar.filter((x) => x.t === 'ceza').map((x) => (x.ceza as Ceza).tur);
      const t = (h as { t: string }).t;
      // İhlal tam olarak: cek/devret + zorunluluk
      assert.deepEqual(cezalar, t === 'cek' || t === 'devret' ? [...(z.islek ? ['islek'] : []), ...(z.per ? ['per'] : [])] : []);
      if (cezalar.length) assert.ok(yeni.bitti || yeni.sira !== d.sira, 'ihlalde tur geçmeli');
      if (t === 'ac' || t === 'isle') assert.ok(ip.some((x) => x.hamle.t === t && (t === 'isle' ? x.hamle.t === 'isle' && x.hamle.tas === (h as { tas: number }).tas && x.per === (h as { per: number }).per : true)), 'ipucunda olmayan hamle kabul edildi');
      const masa = new Set(yeni.perler.flatMap((p) => p.taslar.map((x) => x.id)));
      for (const id of acikTaslar(s.olaylar)) assert.ok(masa.has(id));
      for (const x of s.olaylar) if (x.t === 'cektim') assert.ok(typeof x.kime === 'string' && yeni.oyuncular.find((y) => y.id === x.kime)!.el.some((y) => y.id === (x.tas as Tas).id));
      cezaTop += cezalar.length;
      d = yeni;
      degismez(d);
    }
    if (d.bitti) { biten++; puanDenetle(d, m.sonuc(d)!); } else assert.equal(m.sonuc(d), null);
  }
  console.log(`  ✓ ${m.tur} ${n} oyuncu: ${EL} el · ${hamleTop} hamle · ${hataTop} ret · ${cezaTop} ceza · biten ${biten}`);
  adet++;
}

console.log(`\nTAMAM: ${adet} sınama geçti.`);

sina('duzenle: masadaki perler yeniden kurulur, taş ele dönmez', () => {
  const t = (s: number, r: 0 | 1 | 2 | 3, k = 0) => ({ id: r * 13 + (s - 1) + k * 52, s, r });
  const d0 = yediliMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }], elNo: 1, baslayan: 0, rng: () => 0.3 }) as YediliDurum;
  const d = structuredClone(d0);
  d.oyuncular[0].acti = true;
  d.oyuncular[0].el = [t(9, 3, 1)];
  d.perler = [
    { id: 0, tur: 'seri', taslar: [t(3, 0), t(4, 0), t(5, 0), t(6, 0)], sahip: 'a' },
    { id: 1, tur: 'grup', taslar: [t(6, 1), t(6, 2), t(6, 3)], sahip: 'b' },
  ];
  // 6 kırmızıyı gruba taşı: 3-4-5 kırmızı seri + 6'lı dörtlü grup
  const r = yediliMotor.uygula(d, 'a', { t: 'duzenle', perler: [[t(3, 0).id, t(4, 0).id, t(5, 0).id], [t(6, 0).id, t(6, 1).id, t(6, 2).id, t(6, 3).id]] }, () => 0) as any;
  assert.ok(!r.hata, r.hata);
  assert.equal(r.durum.perler.length, 2);
  assert.deepEqual(r.durum.perler.map((p: any) => p.id).sort(), [0, 1]);
  const eksik = yediliMotor.uygula(d, 'a', { t: 'duzenle', perler: [[t(3, 0).id, t(4, 0).id, t(5, 0).id], [t(6, 1).id, t(6, 2).id, t(6, 3).id]] }, () => 0) as any;
  assert.ok(eksik.hata);
  const elden = yediliMotor.uygula(d, 'a', { t: 'duzenle', perler: [[t(3, 0).id, t(4, 0).id, t(5, 0).id, t(6, 0).id], [t(6, 1).id, t(6, 2).id, t(6, 3).id, t(9, 3, 1).id]] }, () => 0) as any;
  assert.ok(elden.hata, 'elden taş geçersiz per kuramaz');
  const yabanci = yediliMotor.uygula(d, 'a', { t: 'duzenle', perler: [[t(3, 0).id, t(4, 0).id, t(5, 0).id, t(6, 0).id], [t(6, 1).id, t(6, 2).id, t(6, 3).id], [t(1, 2).id, t(2, 2).id, t(3, 2).id]] }, () => 0) as any;
  assert.ok(yabanci.hata, 'elde olmayan taş eklenemez');
  const gecersiz = yediliMotor.uygula(d, 'a', { t: 'duzenle', perler: [[t(3, 0).id, t(4, 0).id], [t(5, 0).id, t(6, 0).id, t(6, 1).id, t(6, 2).id, t(6, 3).id]] }, () => 0) as any;
  assert.ok(gecersiz.hata);
});

sina('takim: 5–6 oyuncuda 4 taş, 2–4 oyuncuda kurucu seçimi 7/14', () => {
  const oy = (n: number) => Array.from({ length: n }, (_, i) => ({ id: `o${i}`, takim: (i % 2 ? 'B' : 'A') as 'A' | 'B' }));
  const say = (n: number, tasSayisi?: 7 | 14) => (takimMotor.elBaslat({ oyuncular: oy(n), elNo: 1, baslayan: 0, rng: () => 0.5, ayar: tasSayisi ? { tasSayisi } : undefined }) as YediliDurum).oyuncular.map((o) => o.el.length);
  assert.deepEqual(say(6, 14), [4, 4, 4, 4, 4, 4]);
  assert.deepEqual(say(4, 14), [14, 14, 14, 14]);
  assert.deepEqual(say(4), [7, 7, 7, 7]);
  assert.deepEqual(say(2, 14), [14, 14]);
  assert.equal((takimMotor.elBaslat({ oyuncular: oy(4), elNo: 1, baslayan: 0, rng: () => 0.5, ayar: { tasSayisi: 14 } }) as YediliDurum).deste.length, 104 - 56);
});

sina('duzenle: masadan alınan taş eldekilerle yeni per olur (dörtlü 10 grubundan sarı 10 + eldeki sarı 9 ve 11)', () => {
  const t = (s: number, r: 0 | 1 | 2 | 3, k = 0) => ({ id: r * 13 + (s - 1) + k * 52, s, r });
  const d = structuredClone(yediliMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }], elNo: 1, baslayan: 0, rng: () => 0.3 }) as YediliDurum);
  d.oyuncular[0].acti = true;
  d.oyuncular[0].el = [t(9, 3), t(11, 3), t(2, 1)];
  d.perler = [
    { id: 0, tur: 'grup', taslar: [t(3, 0), t(3, 1), t(3, 2), t(3, 3)], sahip: 'a' },
    { id: 1, tur: 'grup', taslar: [t(10, 0), t(10, 1), t(10, 2), t(10, 3)], sahip: 'a' },
  ];
  const uclu = [t(10, 0).id, t(10, 1).id, t(10, 2).id], seri = [t(9, 3).id, t(10, 3).id, t(11, 3).id], ucler = d.perler[0].taslar.map((x) => x.id);
  const r = yediliMotor.uygula(d, 'a', { t: 'duzenle', perler: [ucler, uclu, seri] }, () => 0) as any;
  assert.ok(!r.hata, r.hata);
  assert.deepEqual(r.durum.oyuncular[0].el.map((x: any) => x.id), [t(2, 1).id]);
  assert.equal(r.durum.perler.length, 3);
  assert.equal(r.durum.perler.flatMap((p: any) => p.taslar).length, 10);
  assert.equal(new Set(r.durum.perler.map((p: any) => p.id)).size, 3);
  assert.ok(r.durum.hamleYapti);
  assert.ok(r.olaylar.some((o: any) => o.t === 'duzenledi' && o.adet === 2));
  // Hamle yapıldı: artık taş çekilmez
  assert.ok((yediliMotor.uygula(r.durum, 'a', { t: 'cek' }, () => 0) as any).hata);
  // Son taşlar düzenlemeyle eriyince el biter
  const son = structuredClone(d);
  son.oyuncular[0].el = [t(9, 3), t(11, 3)];
  const b = yediliMotor.uygula(son, 'a', { t: 'duzenle', perler: [ucler, uclu, seri] }, () => 0) as any;
  assert.ok(!b.hata && b.durum.bitti && b.durum.sonuc.kazananlar[0] === 'a');
  // Açmamış oyuncu masaya dokunamaz; grup 2 taşa düşemez
  const kapali = structuredClone(d); kapali.oyuncular[0].acti = false;
  assert.ok((yediliMotor.uygula(kapali, 'a', { t: 'duzenle', perler: [ucler, uclu, seri] }, () => 0) as any).hata);
  const uc = structuredClone(d); uc.perler[1].taslar = [t(10, 1), t(10, 2), t(10, 3)];
  assert.ok((yediliMotor.uygula(uc, 'a', { t: 'duzenle', perler: [ucler, [t(10, 1).id, t(10, 2).id], seri] }, () => 0) as any).hata);
});
console.log('TAMAM: düzenle (elden taş) sınamaları geçti.');

sina('oduncBul: seçili el taşları masadan ödünç taşla per olur ve motor kabul eder (her renk)', () => {
  const t = (s: number, r: 0 | 1 | 2 | 3, k = 0) => ({ id: r * 13 + (s - 1) + k * 52, s, r });
  const kur = (el: any[], perler: any[]) => {
    const d = structuredClone(yediliMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }], elNo: 1, baslayan: 0, rng: () => 0.3 }) as YediliDurum);
    d.oyuncular[0].acti = true; d.oyuncular[0].el = el; d.perler = perler;
    return d;
  };
  const uygula = (d: YediliDurum, perler: number[][] | null) => { assert.ok(perler, 'çözüm yok'); const r = yediliMotor.uygula(d, 'a', { t: 'duzenle', perler }, () => 0) as any; assert.ok(!r.hata, r.hata); return r.durum as YediliDurum; };
  for (const r of [0, 1, 2, 3] as const) {
    // Dörtlü 10 grubundan r rengindeki 10 + eldeki 9 ve 11
    const d = kur([t(9, r, 1), t(11, r, 1), t(1, 0)], [{ id: 0, tur: 'grup', taslar: [t(10, 0), t(10, 1), t(10, 2), t(10, 3)], sahip: 'b' }]);
    const s = uygula(d, oduncBul(d.oyuncular[0].el.slice(0, 2), d.perler));
    assert.equal(s.oyuncular[0].el.length, 1);
    assert.equal(s.perler.length, 2);
  }
  // Üçlü gruptan taş alınamaz
  const uc = kur([t(9, 3), t(11, 3), t(1, 0)], [{ id: 0, tur: 'grup', taslar: [t(10, 1), t(10, 2), t(10, 3)], sahip: 'b' }]);
  assert.equal(oduncBul(uc.oyuncular[0].el.slice(0, 2), uc.perler), null);
  // Serinin ucundan (4 taşlı) ve ortasından (bölerek, 7 taşlı) alma; eldeki iki 6 ile grup
  const seri = kur([t(6, 1), t(6, 2), t(1, 0)], [{ id: 0, tur: 'seri', taslar: [3, 4, 5, 6].map((x) => t(x, 0)), sahip: 'b' }]);
  assert.equal(uygula(seri, oduncBul(seri.oyuncular[0].el.slice(0, 2), seri.perler)).perler.length, 2);
  const orta = kur([t(6, 1), t(6, 2), t(1, 0)], [{ id: 0, tur: 'seri', taslar: [3, 4, 5, 6, 7, 8, 9].map((x) => t(x, 0)), sahip: 'b' }]);
  assert.equal(uygula(orta, oduncBul(orta.oyuncular[0].el.slice(0, 2), orta.perler)).perler.length, 3);
  const kisa = kur([t(6, 1), t(6, 2), t(1, 0)], [{ id: 0, tur: 'seri', taslar: [5, 6, 7].map((x) => t(x, 0)), sahip: 'b' }]);
  assert.equal(oduncBul(kisa.oyuncular[0].el.slice(0, 2), kisa.perler), null);
  // Tek taşla: iki ayrı perden birer taş
  const iki = kur([t(8, 3), t(1, 0)], [
    { id: 0, tur: 'grup', taslar: [t(8, 0), t(8, 1), t(8, 2), t(8, 3, 1)], sahip: 'b' },
    { id: 1, tur: 'seri', taslar: [4, 5, 6, 7].map((x) => t(x, 3)), sahip: 'b' },
    { id: 2, tur: 'seri', taslar: [9, 10, 11, 12].map((x) => t(x, 3)), sahip: 'b' },
  ]);
  const c = uygula(iki, oduncBul([t(8, 3)], iki.perler));
  assert.equal(c.perler.length, 4);
  // zorunlu taş: yalnız o taşı içeren çözüm
  const z = kur([t(9, 3, 1), t(11, 3, 1), t(1, 0)], [{ id: 0, tur: 'grup', taslar: [t(10, 0), t(10, 1), t(10, 2), t(10, 3)], sahip: 'b' }]);
  assert.equal(oduncBul(z.oyuncular[0].el.slice(0, 2), z.perler, null, t(10, 0).id), null);
  assert.ok(oduncBul(z.oyuncular[0].el.slice(0, 2), z.perler, null, t(10, 3).id));
});
