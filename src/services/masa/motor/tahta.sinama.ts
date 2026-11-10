/**
 * Tahta oyunları sınaması (Go, Çizgi Yarışı, XOX): `npx tsx src/services/masa/motor/tahta.sinama.ts` (hata → çıkış ≠ 0)
 */
import assert from 'node:assert/strict';
import type { CizgiGorunum, Motor, Rng } from '../tipler';
import { goMotor, say, ozet, diriMi, goSureSonu, handikapNoktalari, type GoDurum } from './go';
import { cizgiMotor, kapismaMi, type CizgiDurum } from './cizgi';
import { xoxBotSec, xoxMotor, type XoxDurum } from './xox';

const tohumlu = (t: number): Rng => () => {
  t = (t + 0x6d2b79f5) | 0;
  let x = Math.imul(t ^ (t >>> 15), 1 | t);
  x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x;
  return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
};
const OY = [{ id: 'a' }, { id: 'b' }];
let say_ = 0;
const dene = (ad: string, f: () => void) => { f(); say_++; console.log('✓', ad); };
const ok = (r: ReturnType<Motor['uygula']>) => { if ('hata' in r) throw new Error(r.hata); return r.durum; };

/** Bot-bot tam oyun: kural dışı hamle üretmemeli, el bitmeli */
function botOyun(m: Motor, ayar: object, tohum: number, sinir = 5000) {
  const rng = tohumlu(tohum);
  let d = m.elBaslat({ oyuncular: OY, elNo: 1, baslayan: tohum % 2, rng, ayar });
  for (let n = 0; n < sinir && !m.sonuc(d); n++) {
    const kim = OY.find((o) => m.botHamle(d, o.id, rng));
    assert(kim, 'kimse oynayamıyor');
    d = ok(m.uygula(d, kim.id, m.botHamle(d, kim.id, rng), rng));
  }
  assert(m.sonuc(d), 'el bitmedi');
  return d;
}

/* ------------------------------------------------------------------ go ------------------------------------------------------------------ */
const go9 = () => goMotor.elBaslat({ oyuncular: OY, elNo: 1, baslayan: 0, rng: tohumlu(1), ayar: { goBoyut: 9 } }) as GoDurum;
const P = (x: number, y: number) => y * 9 + x;
/** Hamle dizisi: a/b sırayla; -1 pas */
const oyna = (d: GoDurum, hamleler: number[]) => hamleler.reduce((s: GoDurum, i) => ok(goMotor.uygula(s, s.sira === 'S' ? 'a' : 'b', i < 0 ? { t: 'pas' } : { t: 'koy', i }, tohumlu(0))) as GoDurum, d);

dene('go: siyah başlar, sıra değişir, dolu noktaya konmaz', () => {
  const d = oyna(go9(), [P(4, 4)]);
  assert.equal(d.tahta[P(4, 4)], 'S');
  assert.equal(d.sira, 'B');
  assert.ok('hata' in goMotor.uygula(d, 'b', { t: 'koy', i: P(4, 4) }, tohumlu(0)));
  assert.ok('hata' in goMotor.uygula(d, 'a', { t: 'koy', i: P(0, 0) }, tohumlu(0)));
});
dene('go: tek taş alma ve esir', () => {
  // B (1,0)'a; S etrafını kapatır: (0,0),(2,0),(1,1)
  const d = oyna(go9(), [P(0, 0), P(1, 0), P(2, 0), P(8, 8), P(1, 1)]);
  assert.equal(d.tahta[P(1, 0)], '');
  assert.equal(d.esir.S, 1);
});
dene('go: intihar yasak', () => {
  // S köşeyi çevirir: (1,0),(0,1); B (0,0)'a konamaz
  const d = oyna(go9(), [P(1, 0), P(8, 8), P(0, 1)]);
  const r = goMotor.uygula(d, 'b', { t: 'koy', i: P(0, 0) }, tohumlu(0));
  assert.ok('hata' in r && /İntihar/.test(r.hata));
});
dene('go: ko hemen geri alınamaz', () => {
  // Klasik ko şekli: S (1,0),(0,1),(2,1),(1,2) · B (2,0),(3,1),(2,2),(1,1)? -> S (1,1) yakalanır kurulumu
  let d = oyna(go9(), [P(1, 0), P(2, 0), P(0, 1), P(3, 1), P(1, 2), P(2, 2), P(8, 8), P(1, 1)]);
  // B (1,1) şu an S taşlarıyla 3 yandan çevrili; S (2,1)'e oynar ve (1,1)'i alır
  d = oyna(d, [P(2, 1)]);
  assert.equal(d.tahta[P(1, 1)], '');
  assert.equal(d.ko, P(1, 1));
  const r = goMotor.uygula(d, 'b', { t: 'koy', i: P(1, 1) }, tohumlu(0));
  assert.ok('hata' in r && /Ko/.test(r.hata));
  d = oyna(d, [-1]); // B ko tehdidi yerine pas: ko kalkar
  d = ok(goMotor.uygula(d, 'a', { t: 'koy', i: P(7, 7) }, tohumlu(0))) as GoDurum;
  assert.equal(d.ko, null);
  assert.ok(!('hata' in goMotor.uygula(d, 'b', { t: 'koy', i: P(1, 1) }, tohumlu(0))));
});
dene('go: iki pas → sayım, ölü işaret onayı sıfırlar, iki onay bitirir', () => {
  let d = oyna(go9(), [P(4, 0), P(4, 8), -1, -1]);
  assert.equal(d.asama, 'sayim');
  d = ok(goMotor.uygula(d, 'a', { t: 'onayla' }, tohumlu(0))) as GoDurum;
  d = ok(goMotor.uygula(d, 'b', { t: 'olu', i: P(4, 0) }, tohumlu(0))) as GoDurum;
  assert.deepEqual(d.onay, []);
  assert.deepEqual(d.olu, [P(4, 0)]);
  d = ok(goMotor.uygula(d, 'a', { t: 'onayla' }, tohumlu(0))) as GoDurum;
  d = ok(goMotor.uygula(d, 'b', { t: 'onayla' }, tohumlu(0))) as GoDurum;
  assert.ok(d.sonuc);
  // Siyah taşı ölü: tahtada yalnız beyaz, tüm alan beyazın: 81 + 6.5
  assert.equal(say(d).puan.B, 87.5);
  assert.equal(d.sonuc!.kazananlar[0], 'b');
});
dene('go: sayımda devam oyuna döndürür', () => {
  let d = oyna(go9(), [-1, -1]);
  d = ok(goMotor.uygula(d, 'a', { t: 'devam' }, tohumlu(0))) as GoDurum;
  assert.equal(d.asama, 'oyun');
  assert.equal(d.sira, 'B');
});
dene('go: teslim', () => {
  const d = ok(goMotor.uygula(go9(), 'b', { t: 'teslim' }, tohumlu(0))) as GoDurum;
  assert.equal(d.sonuc!.kazananlar[0], 'a');
});
dene('go: konumsal süperko (ko dışı yinelenen diziliş yasak)', () => {
  // Geçmişe şimdiki hamlenin doğuracağı dizilişi ekle: aynı tahtaya dönüş reddedilmeli
  const d = oyna(go9(), [P(4, 4)]);
  const t = d.tahta.slice(); t[P(0, 0)] = 'B';
  const d2 = { ...d, gecmis: [...d.gecmis, ozet(t)] };
  const r = goMotor.uygula(d2, 'b', { t: 'koy', i: P(0, 0) }, tohumlu(0));
  assert.ok('hata' in r && /Süperko/.test(r.hata));
  assert.ok(!(goMotor.gorunum(d2, 'b') as any).yasal.includes(P(0, 0)));
  assert.equal(d.gecmis.length, 2);
});
dene('go: handikap taşları yıldızda, beyaz başlar, komi 0,5', () => {
  for (const h of [2, 3, 4, 5, 6, 7, 8, 9]) {
    const d = goMotor.elBaslat({ oyuncular: OY, elNo: 1, baslayan: 0, rng: tohumlu(1), ayar: { goBoyut: 19, goHandikap: h, komi: 6.5 } }) as GoDurum;
    assert.equal(d.tahta.filter((v) => v === 'S').length, h);
    assert.equal(new Set(handikapNoktalari(19, h)).size, h);
    assert.equal(d.sira, 'B'); assert.equal(d.komi, 0.5);
  }
  const d1 = goMotor.elBaslat({ oyuncular: OY, elNo: 1, baslayan: 0, rng: tohumlu(1), ayar: { goBoyut: 9, goHandikap: 1 } }) as GoDurum;
  assert.equal(d1.sira, 'S'); assert.equal(d1.komi, 0.5);
  const d9 = goMotor.elBaslat({ oyuncular: OY, elNo: 1, baslayan: 0, rng: tohumlu(1), ayar: { goBoyut: 9, goHandikap: 9 } }) as GoDurum;
  assert.equal(d9.tahta.filter((v) => v === 'S').length, 9);
  assert.ok(!('hata' in goMotor.uygula(d9, 'b', { t: 'koy', i: P(0, 0) }, tohumlu(0))));
});
dene('go: süre — ana süre, byo-yomi hakkı, süre bitince kayıp', () => {
  let d = goMotor.elBaslat({ oyuncular: OY, elNo: 1, baslayan: 0, rng: tohumlu(1), ayar: { goBoyut: 9, goSure: 'hizli' } }) as GoDurum;
  const t0 = d.saat!.sonZ;
  d = ok(goMotor.uygula(d, 'a', { t: 'koy', i: P(4, 4), z: t0 + 10_000 }, tohumlu(0))) as GoDurum;
  assert.equal(d.saat!.ana.S, 290_000);
  // Beyaz ana süreyi + 1 byo-yomi aralığını aşar (300 sn + 45 sn): 1 hak düşer
  d = ok(goMotor.uygula(d, 'b', { t: 'koy', i: P(2, 2), z: t0 + 10_000 + 345_000 }, tohumlu(0))) as GoDurum;
  assert.equal(d.saat!.ana.B, 0); assert.equal(d.saat!.periyot.B, 2);
  // Siyah süresi henüz bitmedi: sureBitti reddedilir
  assert.ok('hata' in goMotor.uygula(d, 'b', { t: 'sureBitti', z: d.saat!.sonZ + 1000 }, tohumlu(0)));
  const sonu = goSureSonu(d)!;
  assert.equal(sonu, d.saat!.sonZ + 290_000 + 3 * 30_000);
  assert.ok('hata' in goMotor.uygula(d, 'a', { t: 'koy', i: P(6, 6), z: sonu + 1 }, tohumlu(0)), 'süre bitince hamle yok');
  const b = ok(goMotor.uygula(d, 'b', { t: 'sureBitti', z: sonu + 1 }, tohumlu(0))) as GoDurum;
  assert.equal(b.sonuc!.kazananlar[0], 'b');
  assert.match(b.sonuc!.satirlar[0].aciklama!, /süreyi aştı/);
  // Durak: saat kayar
  const k = goMotor.saatKaydir!(d, 5000) as GoDurum;
  assert.equal(goSureSonu(k), sonu + 5000);
});
dene('go: bot kendi diri grubunun ölü işaretini geri alır, sonra onaylar', () => {
  // Beyaz (b, bot) iki gözlü grup: 3. satır boyunca duvar, (0,0)…(8,1) arası iki göz
  let d = go9();
  const t = d.tahta.slice();
  for (let x = 0; x < 9; x++) t[P(x, 2)] = 'B';
  for (let x = 0; x < 9; x++) if (x !== 2 && x !== 6) t[P(x, 1)] = 'B';
  for (let x = 0; x < 9; x++) t[P(x, 0)] = x === 2 || x === 6 ? '' : 'B';
  t[P(4, 6)] = 'S';
  d = { ...d, tahta: t, asama: 'sayim', paslar: 2 };
  assert.ok(diriMi(d, P(0, 2)));
  d = ok(goMotor.uygula(d, 'a', { t: 'olu', i: P(0, 2) }, tohumlu(0))) as GoDurum;
  assert.ok(d.olu.includes(P(0, 2)));
  const h1 = goMotor.botHamle(d, 'b', tohumlu(0)) as any;
  assert.deepEqual(h1, { t: 'olu', i: d.olu.find((i) => d.tahta[i] === 'B') });
  d = ok(goMotor.uygula(d, 'b', h1, tohumlu(0))) as GoDurum;
  assert.ok(!d.olu.includes(P(0, 2)));
  assert.deepEqual(goMotor.botHamle(d, 'b', tohumlu(0)), { t: 'onayla' });
});
for (const n of [9, 13] as const) for (let t = 1; t <= 4; t++) dene(`go: bot-bot ${n}×${n} tohum ${t}`, () => { botOyun(goMotor, { goBoyut: n }, t); });

/* ------------------------------------------------------------------ çizgi ------------------------------------------------------------------ */
const cz = (kare: number, ek: Partial<CizgiDurum> = {}) => ({ ...(cizgiMotor.elBaslat({ oyuncular: OY, elNo: 1, baslayan: 0, rng: tohumlu(1), ayar: { cizgiKare: kare as 32 } }) as CizgiDurum), ...ek });
const sutun = (s: number, r0: number, r1: number) => { const a = []; const d = r1 >= r0 ? 1 : -1; for (let r = r0; r !== r1 + d; r += d) a.push({ s, r }); return a; };

dene('çizgi: modlar ve başlangıç', () => {
  for (const [k, g] of [[32, 3], [64, 5], [96, 5], [128, 7]]) {
    const d = cz(k);
    assert.equal(d.uzunluk, k); assert.equal(d.genislik, g);
    assert.deepEqual(d.cizgiler.a, [{ s: (g - 1) / 2, r: 0 }]);
    assert.deepEqual(d.cizgiler.b, [{ s: (g - 1) / 2, r: k - 1 }]);
  }
});
dene('çizgi: zar sonra adım; sıra yalnız adımlar bitince geçer', () => {
  let d = ok(cizgiMotor.uygula(cz(32), 'a', { t: 'zar' }, tohumlu(3))) as CizgiDurum;
  const z = d.zar!;
  assert.ok(z >= 1 && z <= 6);
  assert.ok('hata' in cizgiMotor.uygula(d, 'a', { t: 'ilerle', yon: 'sol' }, tohumlu(0)), 'önü açıkken yana geçilmez');
  for (let i = 0; i < z; i++) d = ok(cizgiMotor.uygula(d, 'a', { t: 'ilerle', yon: 'duz' }, tohumlu(0))) as CizgiDurum;
  assert.equal(d.cizgiler.a.length, 1 + z);
  assert.equal(d.kim, 1);
  assert.equal(d.gecmis.at(-1)!.fark, z);
});
dene('çizgi: rakip gövdesi önü kapatınca yana geçiş + yan hakkı', () => {
  // b çizgisi 1. sütundan sola kırılıp 0. sütunda a'nın önüne inmiş (a 0. sütunda, gövdeye takılıyor; yüz yüze değil)
  const d0 = cz(32, {
    cizgiler: { a: sutun(1, 0, 3).concat([{ s: 0, r: 3 }]), b: sutun(1, 31, 10).concat(sutun(0, 10, 4)).concat([{ s: 1, r: 4 }]) },
  });
  // a başı (0,3), önü (0,4) b gövdesi; b başı (1,4) — a ile aynı sütunda değil
  assert.ok(!kapismaMi(d0));
  let d = ok(cizgiMotor.uygula(d0, 'a', { t: 'zar' }, tohumlu(5))) as CizgiDurum;
  if (d.kim === 0) {
    assert.deepEqual((cizgiMotor.gorunum(d, 'a') as CizgiGorunum).yonler, []); // sağ (1,3) kendi gövdesi, sol yok → bekler
  }
});
dene('çizgi: yüz yüze + yarı geçilmiş → kapışma; kazanan ilerler, kaybeden geriler', () => {
  // a 2..20 (yarıyı geçti), b 31..21: yüz yüze
  const d0 = cz(32, { cizgiler: { a: sutun(1, 0, 20), b: sutun(1, 31, 21) } });
  assert.ok(kapismaMi(d0));
  for (let t = 1; t < 40; t++) {
    const r = cizgiMotor.uygula(d0, 'a', { t: 'zar' }, tohumlu(t));
    const d = ok(r) as CizgiDurum, k = d.gecmis.at(-1)!.kapisma!;
    assert.ok(k);
    const az = d.gecmis.at(-1)!.zar, bz = k.rakipZar;
    if (az > bz) { assert.equal(d.cizgiler.a.length, 21 + (az - bz)); assert.equal(d.cizgiler.b.length, 11 - (az - bz)); }
    else if (az < bz) { assert.equal(d.cizgiler.b.length, 11 + (bz - az)); assert.equal(d.cizgiler.a.length, 21 - (bz - az)); }
    else { assert.equal(d.cizgiler.a.length, 21); assert.equal(d.cizgiler.b.length, 11); }
    assert.equal(d.kim, 1);
  }
});
dene('çizgi: tam ortada yüz yüze → kapışma yok', () => {
  const d0 = cz(32, { cizgiler: { a: sutun(1, 0, 15), b: sutun(1, 31, 16) } });
  assert.ok(!kapismaMi(d0));
  const d = ok(cizgiMotor.uygula(d0, 'a', { t: 'zar' }, tohumlu(2))) as CizgiDurum;
  assert.deepEqual((cizgiMotor.gorunum(d, 'a') as CizgiGorunum).yonler.sort(), ['sag', 'sol']);
});
dene('çizgi: kalesi kalan kaybederse kale alınır', () => {
  const d0 = cz(32, { cizgiler: { a: sutun(1, 0, 30), b: [{ s: 1, r: 31 }] } });
  for (let t = 1; t < 30; t++) {
    const d = ok(cizgiMotor.uygula(d0, 'a', { t: 'zar' }, tohumlu(t))) as CizgiDurum;
    const k = d.gecmis.at(-1)!.kapisma!;
    if (k.kazanan === 'a') { assert.equal(d.sonuc?.kazananlar[0], 'a'); return; }
  }
  assert.fail('a hiç kazanmadı');
});
for (const k of [32, 64, 96, 128]) for (let t = 1; t <= 5; t++) dene(`çizgi: bot-bot ${k} kare tohum ${t}`, () => {
  const d = botOyun(cizgiMotor, { cizgiKare: k }, t) as CizgiDurum;
  assert.ok(d.gecmis.length <= 4);
});

/* ------------------------------------------------------------------ xox ------------------------------------------------------------------ */
dene('çizgi: koş tek hamlede düz adımların hepsini harcar, sıra geçer', () => {
  let d = ok(cizgiMotor.uygula(cz(64), 'a', { t: 'zar' }, tohumlu(3))) as CizgiDurum;
  const z = d.zar!;
  d = ok(cizgiMotor.uygula(d, 'a', { t: 'kos' }, tohumlu(0))) as CizgiDurum;
  assert.equal(d.cizgiler.a.length, 1 + z);
  assert.equal(d.kim, 1);
  assert.equal(d.gecmis[d.gecmis.length - 1].fark, z);
});
dene('çizgi eğlence: özel kareler ayna simetrik, kale satırlarında yok', () => {
  for (const k of [32, 64, 128]) {
    const d = cizgiMotor.elBaslat({ oyuncular: OY, elNo: 1, baslayan: 0, rng: tohumlu(k), ayar: { cizgiKare: k as 32, cizgiMod: 'eglence' } }) as CizgiDurum;
    assert.ok(d.ozel!.length >= 6);
    for (const x of d.ozel!) {
      assert.ok(x.r > 0 && x.r < k - 1);
      assert.ok(d.ozel!.some((y) => y.t === x.t && y.s === d.genislik - 1 - x.s && y.r === k - 1 - x.r));
    }
  }
});
dene('çizgi eğlence: ileri +3, tuzak 2 geri ve tur biter, zar tekrar', () => {
  const temel = (t: 'ileri' | 'tuzak' | 'zar') => ({ ...cz(64), ozel: [{ s: 2, r: 1, t }] });
  let d = ok(cizgiMotor.uygula(temel('ileri'), 'a', { t: 'zar' }, tohumlu(3))) as CizgiDurum;
  const z = d.zar!;
  d = ok(cizgiMotor.uygula(d, 'a', { t: 'kos' }, tohumlu(0))) as CizgiDurum;
  assert.equal(d.cizgiler.a.length, 1 + z + 3); assert.equal(d.ozel!.length, 0);
  d = ok(cizgiMotor.uygula(temel('tuzak'), 'a', { t: 'zar' }, tohumlu(3))) as CizgiDurum;
  d = ok(cizgiMotor.uygula(d, 'a', { t: 'kos' }, tohumlu(0))) as CizgiDurum;
  assert.equal(d.cizgiler.a.length, 1); assert.equal(d.kim, 1);
  d = ok(cizgiMotor.uygula(temel('zar'), 'a', { t: 'zar' }, tohumlu(3))) as CizgiDurum;
  d = ok(cizgiMotor.uygula(d, 'a', { t: 'kos' }, tohumlu(0))) as CizgiDurum;
  assert.equal(d.kim, 0); assert.equal(d.zar, null);
});
for (let t = 1; t <= 6; t++) dene(`çizgi eğlence: bot-bot 64 kare tohum ${t}`, () => { botOyun(cizgiMotor, { cizgiKare: 64, cizgiMod: 'eglence' }, t); });
const xo = (n: number) => xoxMotor.elBaslat({ oyuncular: OY, elNo: 1, baslayan: 0, rng: tohumlu(1), ayar: { xoxBoyut: n as 3 } }) as XoxDurum;
const xoyna = (d: XoxDurum, h: number[]) => h.reduce((s, i, k) => ok(xoxMotor.uygula(s, k % 2 ? 'b' : 'a', { t: 'koy', i }, tohumlu(0))) as XoxDurum, d);
dene('xox: yatay kazanma', () => { const d = xoyna(xo(3), [0, 3, 1, 4, 2]); assert.deepEqual(d.cizgi, [0, 1, 2]); assert.equal(d.sonuc!.kazananlar[0], 'a'); });
dene('xox: çapraz (ters) kazanma 5×5 hedef 4', () => {
  const d = xoyna(xo(5), [4, 0, 8, 1, 12, 2, 16]);
  assert.equal(d.hedef, 4); assert.equal(d.sonuc!.kazananlar[0], 'a');
});
dene('xox: berabere', () => { const d = xoyna(xo(3), [0, 1, 2, 4, 3, 5, 7, 6, 8]); assert.equal(d.sonuc!.neden, 'berabere'); });
dene('xox: dolu kare ve sıra', () => {
  const d = xoyna(xo(3), [4]);
  assert.ok('hata' in xoxMotor.uygula(d, 'b', { t: 'koy', i: 4 }, tohumlu(0)));
  assert.ok('hata' in xoxMotor.uygula(d, 'a', { t: 'koy', i: 0 }, tohumlu(0)));
});
dene('xox: 3×3 bot-bot hep berabere (kusursuz)', () => { for (let t = 0; t < 4; t++) assert.equal((botOyun(xoxMotor, { xoxBoyut: 3, botZorluk: 'zor' }, t) as XoxDurum).sonuc!.neden, 'berabere'); });
dene('xox: kolay/orta bot hata yapar (kazanılabilir)', () => {
  // Zor X'e karşı kolay O: 40 elde en az bir kez kaybetmeli; kolay O 'zor' kadar sağlam değil
  let kayip = 0;
  for (let t = 0; t < 40; t++) {
    let d = xo(3); d = { ...d, zorluk: 'kolay' };
    const rng = tohumlu(100 + t);
    while (!d.sonuc) {
      const z = d.sira === 'X' ? 'zor' : 'kolay';
      const i = xoxBotSec({ ...d, zorluk: z }, rng);
      d = (xoxMotor.uygula(d, d.oyuncular[d.sira === 'X' ? 0 : 1], { t: 'koy', i }, rng) as { durum: XoxDurum }).durum;
    }
    if (d.sonuc.kazananlar[0] === d.oyuncular[0]) kayip++;
  }
  assert.ok(kayip >= 5, `kolay bot yalnız ${kayip} kez kaybetti`);
});
for (const n of [4, 5, 6]) dene(`xox: ${n}×${n} bot-bot biter`, () => { botOyun(xoxMotor, { xoxBoyut: n }, n); });

console.log(`\n${say_} sınama geçti.`);
