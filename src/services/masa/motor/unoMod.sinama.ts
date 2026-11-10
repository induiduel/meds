/**
 * Uno modları sınaması (Flip, Hepsi Joker, No Mercy, Extreme, Flex, Takım, Yalancı, Deluxe, Express, Sevimli Dostlar):
 * `npx tsx src/services/masa/motor/unoMod.sinama.ts` (hata → çıkış ≠ 0). Klasik aile: uno.sinama.ts.
 */
import assert from 'node:assert/strict';
import type { Olay, Rng, UnoDeger, UnoGorunum, UnoHamle, UnoKart, UnoMod, UnoRenk, UnoYuz } from '../tipler';
import { UNO_MODLAR, unoModTanim, unoOyuncuUygun } from '../tipler';
import { unoMotor, type UnoDurum } from './uno';
import { UNO_DEGERLER, UNO_DEGER_AD, hedefGerek, oneri } from './unoAsistan';
import { FLIP_KOYU, UNO_DESTE_DOKUM, kartPuani, unoDesteKur } from './unoKartlar';

const tohumlu = (t: number): Rng => () => {
  t = (t + 0x6d2b79f5) | 0;
  let x = Math.imul(t ^ (t >>> 15), 1 | t);
  x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x;
  return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
};
const rng0 = tohumlu(7);
/** Sabit değer dönen rng (fırlatıcı: 0 = hep fırlar, 0.99 = hiç fırlamaz) */
const sabit = (v: number): Rng => () => v;

type Tanim = [UnoRenk | null, UnoDeger, Partial<UnoYuz>?];
type Tamam = { durum: unknown; olaylar: Olay[] };
type K = UnoDurum['deste'][number];

const esit = (k: UnoYuz, [r, v, ek]: Tanim) => k.renk === r && k.deger === v && !!k.yl === !!ek?.yl && !!k.ps === !!ek?.ps && !!k.cv === !!ek?.cv && (ek?.fx === undefined ? !k.fx || r === null : !!k.fx);

/** Elle kurulmuş durum: verilen eller + üst kart; kalan kartlar destede */
function kur(mod: UnoMod, eller: Record<string, Tanim[]>, ust: Tanim, ek: Partial<UnoDurum> = {}): UnoDurum {
  const havuz: K[] = unoDesteKur(mod, tohumlu(3));
  const al = (t: Tanim): K => {
    const i = havuz.findIndex((k) => esit(k, t));
    assert(i >= 0, `kart yok: ${mod} ${t[0]}${t[1]} ${JSON.stringify(t[2] ?? {})}`);
    return havuz.splice(i, 1)[0];
  };
  const ids = Object.keys(eller);
  return {
    tur: 'uno', elNo: 1, oyuncular: ids, kim: 0, yon: 1, mod,
    eller: Object.fromEntries(ids.map((id) => [id, eller[id].map(al)])),
    atik: [al(ust)], deste: havuz, aktifRenk: ust[0] ?? 'k',
    cektiBuTur: false, cekilen: null, unoDedi: [], yakalanabilir: [], yigin: 0, yiginEn: 0, bekle: null, ver: null,
    cezalar: Object.fromEntries(ids.map((id) => [id, []])), sonuc: null,
    ...(mod === 'flip' ? { taraf: 'a' as const } : {}), ...(mod === 'noMercy' ? { elenen: [] } : {}), ...(mod === 'extreme' ? { gerilim: 0 } : {}),
    ...(mod === 'flex' ? { guc: Object.fromEntries(ids.map((id) => [id, true])) } : {}),
    ...ek,
  };
}
const kid = (d: UnoDurum, o: string, r: UnoRenk | null, v: UnoDeger, ek?: Partial<UnoYuz>): number => {
  const k = d.eller[o].find((x) => esit(x, [r, v, ek]));
  assert(k, `elde yok: ${o} ${r}${v}`);
  return k.id;
};
function yap(d: UnoDurum, o: string, h: UnoHamle, rng: Rng = rng0): { d: UnoDurum; olaylar: Olay[] } {
  const r = unoMotor.uygula(d, o, h, rng);
  assert(!('hata' in r), `beklenmeyen hata (${o} ${JSON.stringify(h)}): ${'hata' in r ? r.hata : ''}`);
  return { d: (r as Tamam).durum as UnoDurum, olaylar: (r as Tamam).olaylar };
}
function hata(d: UnoDurum, o: string, h: UnoHamle, re?: RegExp): void {
  const r = unoMotor.uygula(d, o, h, rng0);
  assert('hata' in r, `hata bekleniyordu: ${JSON.stringify(h)}`);
  if (re) assert.match(r.hata, re);
}
const gor = (d: UnoDurum, b: string | null) => unoMotor.gorunum(d, b) as UnoGorunum;
const siradaki = (d: UnoDurum) => d.oyuncular[d.kim];
const n = (d: UnoDurum, o: string) => d.eller[o].length;
/** Destenin üstüne (ilk çekilecek) belirli kartı getir */
function usteAl(d: UnoDurum, r: UnoRenk | null, v: UnoDeger): number {
  const i = d.deste.findIndex((k) => k.renk === r && k.deger === v);
  assert(i >= 0, `destede yok: ${r}${v}`);
  const [k] = d.deste.splice(i, 1);
  d.deste.push(k);
  return k.id;
}

/** Kart korunumu: her kimlik tam bir kez (eller + deste + atık + bekleyen kapalı kartlar + verilen kartlar) */
function korunum(d: UnoDurum): void {
  const hepsi: K[] = [...d.deste, ...d.atik, ...d.oyuncular.flatMap((id) => d.eller[id])];
  if (d.bekle?.tur === 'meydan') hepsi.push(...Object.values(d.bekle.konan));
  if (d.ver) hepsi.push(...d.ver.tampon.map((t) => t.kart));
  const beklenen = unoModTanim(d.mod).deste;
  assert.equal(hepsi.length, beklenen, `kart sayısı ${hepsi.length} ≠ ${beklenen}`);
  assert.equal(new Set(hepsi.map((k) => k.id)).size, beklenen, 'yinelenen kart kimliği');
  assert(d.atik.length >= 1, 'atık boş');
  if (d.mod === 'flip') for (const k of hepsi) assert(k.arka && (d.taraf === 'k') === (k.t === 'k') && (k.arka.t === 'k') !== (k.t === 'k'), 'flip yüzü tutarsız');
  if (d.mod === 'hepsiJoker') assert(hepsi.every((k) => k.renk === null));
  if (d.mod === 'noMercy') for (const id of d.oyuncular) assert(d.eller[id].length < 25 || d.elenen!.includes(id) || !!d.sonuc, 'eli 25+ olan elenmedi');
}

/** Flip: elle kurulmuş durumu koyu yüze çevir (kart yerleri değişmez) */
function koyuYap(d: UnoDurum): UnoDurum {
  const cevir = (x: K): K => ({ id: x.id, ...x.arka!, arka: { renk: x.renk, deger: x.deger } });
  d.deste = d.deste.map(cevir); d.atik = d.atik.map(cevir); for (const id of d.oyuncular) d.eller[id] = d.eller[id].map(cevir);
  d.taraf = 'k';
  return d;
}

let adet = 0;
function sina(ad: string, f: () => void): void {
  f();
  adet++;
  console.log(`  ✓ ${ad}`);
}

console.log('Desteler');
sina('her modun destesi beyan edilen sayıda, kimlikler benzersiz, dökümler tutarlı', () => {
  for (const m of UNO_MODLAR) {
    const d = unoDesteKur(m.id, tohumlu(1));
    assert.equal(d.length, m.deste, `${m.id} deste ${d.length}`);
    assert.equal(new Set(d.map((k) => k.id)).size, d.length);
    assert(m.elKart * m.enCok + 1 <= m.deste, `${m.id}: dağıtım desteyi aşıyor`);
    for (const [r, v] of m.ornek) assert(UNO_DEGERLER.includes(v) && (r === null || 'ksym'.includes(r)));
  }
  assert.equal(Object.keys(UNO_DESTE_DOKUM).length, UNO_MODLAR.length);
  const say = (m: UnoMod, v: UnoDeger) => unoDesteKur(m, rng0).filter((k) => k.deger === v).length;
  assert.deepEqual([say('deluxe', 'joker'), say('deluxe', '+4'), say('express', '+1'), say('express', 'joker+2')], [8, 4, 4, 2]);
  assert.deepEqual([say('hepsiJoker', 'joker'), say('hepsiJoker', 'jokerTakas'), say('hepsiJoker', 'jokerPas2')], [54, 4, 6]);
  assert.deepEqual([say('noMercy', '+10'), say('noMercy', 'rulet'), say('noMercy', 'hepsiAt'), say('noMercy', 'joker')], [4, 8, 12, 0]);
  assert.deepEqual([say('extreme', 'vur1'), say('extreme', 'vur2'), say('extreme', 'jokerVur'), say('extreme', 'yon'), say('extreme', '0')], [4, 8, 4, 4, 0]);
  assert.deepEqual([say('takim', 'jokerTakim'), say('takim', 'jokerTakim4'), unoDesteKur('takim').filter((k) => k.ps).length], [8, 4, 20]);
  const fx = unoDesteKur('flex');
  assert.deepEqual([fx.filter((k) => k.fx).length, fx.filter((k) => k.cv).length, fx.filter((k) => k.deger === 'jokerCevir').length, fx.filter((k) => k.deger === '9' || k.deger === '0').length], [54, 8, 6, 0]);
  assert(fx.every((k) => !k.fx || k.fx === 'j' || k.fx !== k.renk), 'flex rengi kartın kendi renginden farklı');
  const yl = unoDesteKur('yalanci');
  assert.deepEqual([yl.filter((k) => k.yl).length, yl.filter((k) => k.deger === 'jokerMeydan').length, yl.filter((k) => k.deger === '+4').length], [66, 6, 2]);
  assert.equal(say('dostlar', 'kitty') + say('dostlar', 'batman') + say('dostlar', 'kuromi') + say('dostlar', 'pony'), 8);
  // Flip: 112 açık + 112 koyu yüz; koyu yüz dökümü tam
  const fl = unoDesteKur('flip', tohumlu(9));
  assert(fl.every((k) => !k.t && k.arka?.t === 'k'));
  const koyu = (v: UnoDeger) => fl.filter((k) => k.arka!.deger === v).length;
  assert.deepEqual([koyu('+5'), koyu('pasHerkes'), koyu('jokerRenk'), koyu('flip'), koyu('joker'), fl.filter((k) => k.deger === 'flip').length], [8, 8, 4, 8, 4, 8]);
  assert.equal(FLIP_KOYU.reduce((t, s) => t + s.adet * (s.renkli ? 4 : 1), 0), 112);
  assert.equal(Object.keys(UNO_DEGER_AD).length, UNO_DEGERLER.length);
});

sina('puan tabloları (mod başına resmî değerler)', () => {
  const p = (m: UnoMod, r: UnoRenk | null, v: UnoDeger) => kartPuani({ renk: r, deger: v }, m);
  assert.deepEqual([p('flip', 'k', '+1'), p('flip', 'k', '+5'), p('flip', 'k', 'pasHerkes'), p('flip', null, 'joker'), p('flip', null, 'joker+2'), p('flip', null, 'jokerRenk'), p('flip', 'k', 'flip')], [10, 20, 30, 40, 50, 60, 20]);
  assert.deepEqual([p('hepsiJoker', null, 'joker'), p('hepsiJoker', null, 'jokerTakas'), p('hepsiJoker', null, '+4')], [20, 50, 50]);
  assert.deepEqual([p('extreme', 'k', 'vur1'), p('extreme', 'k', 'vur2'), p('extreme', 'k', 'hepsiAt'), p('extreme', null, 'jokerVur'), p('extreme', 'k', 'pas')], [20, 40, 30, 50, 20]);
  assert.deepEqual([p('noMercy', 'k', 'r+4'), p('noMercy', null, '+10'), p('noMercy', 'k', '7')], [20, 50, 7]);
  assert.deepEqual([p('express', 'k', '+1'), p('express', null, 'joker+2')], [20, 50]);
});

sina('oyuncu sınırı: takım 4/6/8, express en çok 6', () => {
  assert.equal(unoOyuncuUygun('takim', 4), null);
  assert.match(unoOyuncuUygun('takim', 5)!, /4, 6 ya da 8/);
  assert.match(unoOyuncuUygun('takim', 2)!, /4, 6 ya da 8/);
  assert.match(unoOyuncuUygun('express', 7)!, /en çok 6/);
  assert.equal(unoOyuncuUygun('noMercy', 8), null);
  assert.throws(() => unoMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }, { id: 'c' }], elNo: 1, baslayan: 0, rng: rng0, ayar: { unoMod: 'takim' } }));
});

/* ------------------------------------------------------------------ birim: modlar ------------------------------------------------------------------ */

console.log('Flip');
sina('Flip kartı her şeyi çevirir: yeni üst = eski en alt kartın koyu yüzü; eller ve deste döner', () => {
  const d = kur('flip', { a: [['k', 'flip'], ['k', '3'], ['m', '4']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const alt = d.atik[0], aEl = d.eller.a.filter((k) => k.deger !== 'flip'), desteUst = d.deste[d.deste.length - 1];
  // gizlilik: kendi elimde öbür yüz yok, rakibin elinde yalnız öbür yüz var
  const g0 = gor(d, 'a');
  assert(g0.elim.every((k) => !('arka' in k)));
  assert.deepEqual(g0.oyuncular.find((o) => o.id === 'b')!.arka, d.eller.b.map((k) => k.arka));
  assert.equal(g0.oyuncular.find((o) => o.id === 'a')!.arka, undefined);
  assert.deepEqual(g0.desteUst, desteUst.arka);
  assert.equal(g0.taraf, 'a');
  if (alt.arka!.renk === null) return; // koyu yüz joker: renk seçimi ayrı sınanır
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', 'flip') });
  assert.equal(r.d.taraf, 'k');
  const ust = r.d.atik[r.d.atik.length - 1];
  assert.equal(ust.id, alt.id);
  assert.deepEqual([ust.renk, ust.deger, ust.t], [alt.arka!.renk, alt.arka!.deger, 'k']);
  assert.equal(r.d.aktifRenk, alt.arka!.renk);
  assert.deepEqual(r.d.eller.a.map((k) => [k.id, k.deger]), aEl.map((k) => [k.id, k.arka!.deger]));
  assert.equal(r.d.deste[0].id, desteUst.id, 'deste ters döndü');
  assert.equal(siradaki(r.d), 'b');
  assert.equal(gor(r.d, 'b').taraf, 'k');
  korunum(r.d);
});
sina('Flip sonrası üstte joker çıkarsa çeviren renk seçer, sonra sıra geçer', () => {
  const d = kur('flip', { a: [['k', 'flip'], ['k', '3']], b: [['s', '1'], ['s', '2']] }, ['k', '5']);
  d.atik[0].arka = { renk: null, deger: 'jokerRenk', t: 'k' };
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', 'flip') });
  assert.deepEqual(r.d.bekle, { tur: 'renk', kim: 'a', sonra: 'gec' });
  assert.equal(gor(r.d, 'a').sira, 'a');
  hata(r.d, 'b', { t: 'cek' }, /Renk seçilmesi/);
  const r2 = yap(r.d, 'a', { t: 'renk', renk: 'y' });
  assert.equal(r2.d.aktifRenk, 'y');
  assert.equal(siradaki(r2.d), 'b');
  assert.equal(n(r2.d, 'b'), 2, 'açılan jokerin etkisi uygulanmaz');
});
sina('+1 ve koyu yüz: +5, Herkesi Atlat', () => {
  const d = kur('flip', { a: [['k', '+1'], ['k', '3']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', '+1'), uno: true });
  assert.equal(n(r.d, 'b'), 3); assert.equal(siradaki(r.d), 'c');
  // koyu yüz elle kurulur
  const k = koyuYap(kur('flip', { a: [['k', '1'], ['k', '2'], ['k', '3']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']));
  k.eller.a[0] = { ...k.eller.a[0], renk: 'm', deger: '+5', t: 'k' };
  k.eller.a[1] = { ...k.eller.a[1], renk: 'm', deger: 'pasHerkes', t: 'k' };
  k.aktifRenk = 'm';
  const s = yap(k, 'a', { t: 'oyna', kart: k.eller.a[1].id });
  assert.equal(siradaki(s.d), 'a', 'Herkesi Atlat: yeniden oynar');
  const s2 = yap(s.d, 'a', { t: 'oyna', kart: k.eller.a[0].id, uno: true });
  assert.equal(n(s2.d, 'b'), 7); assert.equal(siradaki(s2.d), 'c');
});
sina('Joker +2 itirazı (2 / 4) ve Joker Renk Çek itirazı (renk gelene dek, haksızsa +2)', () => {
  const d = kur('flip', { a: [[null, 'joker+2'], ['k', '3'], ['m', '4']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'joker+2'), renk: 'm' });
  assert.deepEqual(gor(r.d, 'b').bekle, { tur: 'itiraz', oynayan: 'a', hedef: 'b', kart: 'joker+2' });
  const kabul = yap(r.d, 'b', { t: 'kabul' });
  assert.equal(n(kabul.d, 'b'), 4); assert.equal(siradaki(kabul.d), 'c');
  const hakli = yap(r.d, 'b', { t: 'itiraz' }); // a'nın elinde k3 vardı (önceki renk k)
  assert.equal(n(hakli.d, 'a'), 4); assert.equal(n(hakli.d, 'b'), 2); assert.equal(siradaki(hakli.d), 'b');
  const d2 = kur('flip', { a: [[null, 'joker+2'], ['y', '3'], ['m', '4']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const haksiz = yap(yap(d2, 'a', { t: 'oyna', kart: kid(d2, 'a', null, 'joker+2'), renk: 'm' }).d, 'b', { t: 'itiraz' });
  assert.equal(n(haksiz.d, 'b'), 6); assert.equal(siradaki(haksiz.d), 'c');
  // Joker Renk Çek
  const e = koyuYap(kur('flip', { a: [['y', '3'], ['m', '4'], ['m', '6']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']));
  e.eller.a[0] = { ...e.eller.a[0], renk: null, deger: 'jokerRenk', t: 'k' };
  e.eller.a[1] = { ...e.eller.a[1], renk: 'm', deger: '4', t: 'k' }; e.eller.a[2] = { ...e.eller.a[2], renk: 'm', deger: '6', t: 'k' };
  e.atik[0] = { ...e.atik[0], renk: 'y', deger: '5', t: 'k' }; e.aktifRenk = 'y';
  for (const id of ['b', 'c']) e.eller[id] = e.eller[id].map((x) => ({ ...x, renk: 's' as const, deger: '1' as const, t: 'k' as const }));
  // deste: üstte k olmayan 2 kart, sonra k
  const kirmizi = e.deste.findIndex((x) => x.renk === 'k'), baska = e.deste.filter((x) => x.renk !== 'k' && x.renk !== null).slice(0, 2);
  const kk = e.deste[kirmizi];
  e.deste = [...e.deste.filter((x) => x !== kk && !baska.includes(x)), kk, ...baska];
  const er = yap(e, 'a', { t: 'oyna', kart: e.eller.a[0].id, renk: 'k' });
  assert.equal(er.d.bekle?.tur, 'itiraz');
  const ek = yap(er.d, 'b', { t: 'kabul' });
  assert.equal(n(ek.d, 'b'), 5, 'k gelene dek 3 kart'); assert.equal(siradaki(ek.d), 'c');
  const ei = yap(er.d, 'b', { t: 'itiraz' }); // a'nın elinde k yoktu → haksız itiraz: renk gelene dek + 2
  assert.equal(n(ei.d, 'b'), 7);
  korunum(ei.d);
});

console.log('Hepsi Joker');
sina('renk yok, her kart oynanır; ilk kartın etkisi yok; isteğe bağlı çekme', () => {
  const d = kur('hepsiJoker', { a: [[null, 'joker'], [null, 'jokerPas'], [null, 'jokerYon']], b: [[null, 'joker'], [null, 'joker']], c: [[null, 'joker'], [null, 'joker']] }, [null, '+4']);
  const g = gor(d, 'a');
  assert.equal(g.renksiz, true);
  assert.equal(g.oynanabilir.length, 3);
  assert.equal(g.cekOlur, true);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'joker') }); // renk verilmeden
  assert.equal(siradaki(r.d), 'b');
  const c = yap(d, 'a', { t: 'cek' });
  assert.equal(c.d.cektiBuTur, true);
  hata(c.d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'jokerPas') }, /yalnız çektiğin/);
  yap(c.d, 'a', { t: 'pas' });
  for (let i = 0; i < 40; i++) {
    const e = unoMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }, { id: 'c' }], elNo: 1, baslayan: 0, rng: tohumlu(i), ayar: { unoMod: 'hepsiJoker' } }) as UnoDurum;
    assert.equal(siradaki(e), 'a'); assert.equal(e.yon, 1); assert.equal(e.bekle, null); assert.equal(n(e, 'a'), 7);
  }
});
sina('İkili Atlat, Hedefli +2 (hedef atlanmaz), +4 itirazsız', () => {
  const el: Tanim[] = [[null, 'jokerPas2'], [null, 'jokerHedef2'], [null, '+4'], [null, 'joker']];
  const d = kur('hepsiJoker', { a: el, b: [[null, 'joker'], [null, 'joker']], c: [[null, 'joker'], [null, 'joker']], e: [[null, 'joker'], [null, 'joker']] }, [null, 'joker']);
  assert.equal(siradaki(yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'jokerPas2') }).d), 'e');
  hata(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'jokerHedef2') }, /rakip seç/);
  hata(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'jokerHedef2'), hedef: 'a' }, /rakip seç/);
  const h = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'jokerHedef2'), hedef: 'c' });
  assert.equal(n(h.d, 'c'), 4); assert.equal(siradaki(h.d), 'b');
  const p = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, '+4') });
  assert.equal(p.d.bekle, null); assert.equal(n(p.d, 'b'), 6); assert.equal(siradaki(p.d), 'c');
  // 2 oyuncu: İkili Atlat → yeniden oynar
  const iki = kur('hepsiJoker', { a: [[null, 'jokerPas2'], [null, 'joker'], [null, 'joker']], b: [[null, 'joker'], [null, 'joker']] }, [null, 'joker']);
  assert.equal(siradaki(yap(iki, 'a', { t: 'oyna', kart: kid(iki, 'a', null, 'jokerPas2') }).d), 'a');
});
sina('Zorunlu Takas: eller değişir; son kartsa boş eli alan kazanır', () => {
  const d = kur('hepsiJoker', { a: [[null, 'jokerTakas'], [null, 'joker'], [null, 'joker'], [null, 'jokerPas']], b: [[null, 'joker'], [null, 'jokerYon']], c: [[null, 'joker'], [null, 'joker']] }, [null, 'joker']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'jokerTakas'), hedef: 'b' });
  assert.equal(n(r.d, 'a'), 2); assert.equal(n(r.d, 'b'), 3);
  assert(r.d.eller.a.some((k) => k.deger === 'jokerYon'));
  const son = kur('hepsiJoker', { a: [[null, 'jokerTakas']], b: [[null, 'joker'], [null, 'jokerYon']], c: [[null, 'joker'], [null, 'joker']] }, [null, 'joker']);
  const s = yap(son, 'a', { t: 'oyna', kart: kid(son, 'a', null, 'jokerTakas'), hedef: 'c' });
  assert.deepEqual(s.d.sonuc?.kazananlar, ['c']);
  assert.equal(n(s.d, 'a'), 2);
  assert.equal(s.d.sonuc!.satirlar.find((x) => x.id === 'a')!.puan, -40);
});

console.log('No Mercy');
sina('yığma: eşit ya da büyük değer eklenir, küçük eklenmez; ekleyemeyen hepsini çeker', () => {
  const d = kur('noMercy', { a: [['k', 'r+4'], ['k', '3']], b: [['m', '+2'], [null, '+6'], ['s', '1']], c: [[null, '+10'], ['y', '2'], ['y', '3']] }, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', 'r+4'), uno: true });
  assert.equal(r.d.yigin, 4); assert.equal(siradaki(r.d), 'b');
  assert.deepEqual(gor(r.d, 'b').oynanabilir, [kid(d, 'b', null, '+6')]);
  hata(r.d, 'b', { t: 'oyna', kart: kid(d, 'b', 'm', '+2') }, /\+4 ya da daha büyük/);
  const r2 = yap(r.d, 'b', { t: 'oyna', kart: kid(d, 'b', null, '+6'), renk: 'y' });
  assert.equal(r2.d.yigin, 10);
  const r3 = yap(r2.d, 'c', { t: 'oyna', kart: kid(d, 'c', null, '+10'), renk: 'y' });
  assert.equal(r3.d.yigin, 20); assert.equal(siradaki(r3.d), 'a');
  const r4 = yap(r3.d, 'a', { t: 'cek' });
  assert.equal(n(r4.d, 'a'), 21); assert.equal(r4.d.yigin, 0); assert.equal(siradaki(r4.d), 'b');
  korunum(r4.d);
});
sina('uyan kart gelene dek çekilir ve gelen kart oynanmak zorundadır; oynanabilir kart varken çekilmez', () => {
  const d = kur('noMercy', { a: [['m', '1'], ['m', '2']], b: [['s', '1'], ['s', '2']] }, ['k', '5']);
  usteAl(d, 'k', '8'); usteAl(d, 'y', '3'); usteAl(d, 's', '9');
  const r = yap(d, 'a', { t: 'cek' });
  assert.equal(n(r.d, 'a'), 5);
  const g = gor(r.d, 'a');
  assert.equal(g.zorunlu, true); assert.deepEqual(g.oynanabilir, [r.d.cekilen]);
  hata(r.d, 'a', { t: 'pas' }, /oynamak zorundasın/);
  yap(r.d, 'a', { t: 'oyna', kart: r.d.cekilen! });
  const v = kur('noMercy', { a: [['k', '1'], ['m', '2']], b: [['s', '1'], ['s', '2']] }, ['k', '5']);
  hata(v, 'a', { t: 'cek' }, /Oynanabilir kartın var/);
  assert.equal(gor(v, 'a').cekOlur, false);
});
sina('25 kartta elenme: kartlar oyundan çıkar, sıra atlar; son kalan kazanır (+250)', () => {
  const cok: Tanim[] = Array.from({ length: 10 }, (_, i): Tanim => ['m', String(i) as UnoDeger]).concat(Array.from({ length: 10 }, (_, i): Tanim => ['s', String(i) as UnoDeger]), [['y', '1'], ['y', '2']]);
  const d = kur('noMercy', { a: [[null, '+6'], ['k', '3']], b: cok, c: [['y', '4'], ['y', '3']] }, ['k', '5']);
  const r = yap(yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, '+6'), renk: 'k', uno: true }).d, 'b', { t: 'cek' });
  assert.deepEqual(r.d.elenen, ['b']); assert.equal(n(r.d, 'b'), 0);
  assert(r.olaylar.some((o) => o.t === 'elendi' && o.o === 'b'));
  assert.equal(siradaki(r.d), 'c');
  assert.equal(gor(r.d, 'c').oyuncular.find((o) => o.id === 'b')!.elendi, true);
  hata(r.d, 'b', { t: 'cek' }, /elendin/);
  korunum(r.d);
  // iki kişide elenme → kalan kazanır
  const iki = kur('noMercy', { a: [[null, '+6'], ['k', '3']], b: cok }, ['k', '5']);
  const s = yap(yap(iki, 'a', { t: 'oyna', kart: kid(iki, 'a', null, '+6'), renk: 'k', uno: true }).d, 'b', { t: 'cek' });
  assert.deepEqual(s.d.sonuc?.kazananlar, ['a']);
  assert.equal(s.d.sonuc!.satirlar.find((x) => x.id === 'a')!.puan, 250);
  assert.equal(s.d.sonuc!.satirlar.find((x) => x.id === 'b')!.puan, -250);
});
sina('Hepsini At, Herkesi Atlat, Renk Ruleti, 7 takas (hedefli), 0 devir, Joker Yön +4', () => {
  const d = kur('noMercy', { a: [['k', 'hepsiAt'], ['k', '1'], ['k', '2'], ['m', '3'], ['m', 'pasHerkes']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', 'hepsiAt') });
  assert.equal(n(r.d, 'a'), 2); assert.equal(r.d.atik[r.d.atik.length - 1].deger, 'hepsiAt'); assert.equal(siradaki(r.d), 'b');
  korunum(r.d);
  const son = kur('noMercy', { a: [['k', 'hepsiAt'], ['k', '1'], ['k', '2']], b: [['s', '1'], ['s', '2']] }, ['k', '5']);
  assert.deepEqual(yap(son, 'a', { t: 'oyna', kart: kid(son, 'a', 'k', 'hepsiAt') }).d.sonuc?.kazananlar, ['a']);
  const ph = kur('noMercy', { a: [['k', 'pasHerkes'], ['k', '1'], ['k', '2']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  assert.equal(siradaki(yap(ph, 'a', { t: 'oyna', kart: kid(ph, 'a', 'k', 'pasHerkes') }).d), 'a');
  // Renk Ruleti: sıradaki renk seçer, o renk gelene dek alır, sırası geçer
  const ru = kur('noMercy', { a: [[null, 'rulet'], ['k', '1'], ['k', '2']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const mavi = ru.deste.find((x) => x.renk === 'm')!, baska = ru.deste.filter((x) => x.renk !== 'm').slice(0, 3);
  ru.deste = [...ru.deste.filter((x) => x !== mavi && !baska.includes(x)), mavi, ...baska];
  const r1 = yap(ru, 'a', { t: 'oyna', kart: kid(ru, 'a', null, 'rulet') });
  assert.deepEqual(gor(r1.d, 'b').bekle, { tur: 'rulet', kim: 'b' });
  hata(r1.d, 'b', { t: 'cek' }, /Renk Ruleti/);
  const r2 = yap(r1.d, 'b', { t: 'renk', renk: 'm' });
  assert.equal(n(r2.d, 'b'), 6); assert.equal(r2.d.aktifRenk, 'm'); assert.equal(siradaki(r2.d), 'c');
  // 7: seçilen rakiple takas; 0: herkes yöndeki oyuncuya verir
  const t = kur('noMercy', { a: [['k', '7'], ['k', '0'], ['m', '9']], b: [['s', '1'], ['s', '2'], ['s', '3'], ['s', '4']], c: [['y', '1']] }, ['k', '5']);
  const t1 = yap(t, 'a', { t: 'oyna', kart: kid(t, 'a', 'k', '7'), hedef: 'c' });
  assert.equal(n(t1.d, 'a'), 1); assert.equal(n(t1.d, 'c'), 2);
  const t0 = yap(t, 'a', { t: 'oyna', kart: kid(t, 'a', 'k', '0') });
  assert.deepEqual([n(t0.d, 'a'), n(t0.d, 'b'), n(t0.d, 'c')], [1, 2, 4]);
  // Joker Yön +4: yön döner, yeni yöndeki sıradaki hedef; iki kişide ceza oynayana döner
  const y = kur('noMercy', { a: [[null, 'jokerYon4'], ['k', '1'], ['k', '2']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const y1 = yap(y, 'a', { t: 'oyna', kart: kid(y, 'a', null, 'jokerYon4'), renk: 'k' });
  assert.equal(y1.d.yon, -1); assert.equal(siradaki(y1.d), 'c'); assert.equal(y1.d.yigin, 4);
  const y2 = kur('noMercy', { a: [[null, 'jokerYon4'], ['k', '1'], ['k', '2']], b: [['s', '1'], ['s', '2']] }, ['k', '5']);
  const y3 = yap(y2, 'a', { t: 'oyna', kart: kid(y2, 'a', null, 'jokerYon4'), renk: 'k' });
  assert.equal(siradaki(y3.d), 'a'); assert.equal(y3.d.yigin, 4);
  hata(y3.d, 'a', { t: 'oyna', kart: kid(y2, 'a', 'k', '1') }, /daha büyük/);
  assert.equal(n(yap(y3.d, 'a', { t: 'cek' }).d, 'a'), 6);
  for (let i = 0; i < 60; i++) {
    const e = unoMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }], elNo: 1, baslayan: 0, rng: tohumlu(i), ayar: { unoMod: 'noMercy' } }) as UnoDurum;
    assert.equal(e.atik[0].deger.length, 1, 'ilk kart sayı');
  }
});

console.log('Extreme');
sina('fırlatıcı: çekmek = basmak, sıra geçer; boş basış gerilimi artırır', () => {
  const d = kur('extreme', { a: [['m', '1'], ['m', '2']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  assert.equal(gor(d, 'a').firlatici, true);
  const bos = yap(d, 'a', { t: 'cek' }, sabit(0.99));
  assert.equal(n(bos.d, 'a'), 2); assert.equal(bos.d.gerilim, 1); assert.equal(siradaki(bos.d), 'b');
  assert(bos.olaylar.some((o) => o.t === 'firlat' && o.adet === 0));
  const dolu = yap(d, 'a', { t: 'cek' }, sabit(0));
  assert.equal(n(dolu.d, 'a'), 4, 'rng 0 → 2 kart fırlar'); assert.equal(dolu.d.gerilim, 0); assert.equal(siradaki(dolu.d), 'b');
  korunum(dolu.d);
});
sina('Vur kartları birikir (Mega Hit): renk aranmaz; sıra ilk vurandan sonrakine döner', () => {
  const d = kur('extreme', { a: [['k', 'vur2'], ['k', '3']], b: [['m', 'vur1'], ['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', 'vur2'), uno: true });
  assert.equal(r.d.yigin, 2); assert.equal(siradaki(r.d), 'b');
  assert.deepEqual(gor(r.d, 'b').oynanabilir, [kid(d, 'b', 'm', 'vur1')]);
  hata(r.d, 'b', { t: 'oyna', kart: kid(d, 'b', 's', '1') }, /Vur kartı/);
  // b basarsa: tek vuruş → sıra c'ye
  const bas = yap(r.d, 'b', { t: 'cek' }, sabit(0.99));
  assert.equal(siradaki(bas.d), 'c'); assert.equal(bas.d.gerilim, 2); assert.equal(bas.d.yigin, 0);
  // b eklerse: c 3 basış üstlenir, sıra ilk vuran a'dan sonrakine (b) döner
  const r2 = yap(r.d, 'b', { t: 'oyna', kart: kid(d, 'b', 'm', 'vur1') });
  assert.equal(r2.d.yigin, 3); assert.equal(siradaki(r2.d), 'c');
  const r3 = yap(r2.d, 'c', { t: 'cek' }, sabit(0.99));
  assert.equal(r3.d.gerilim, 3); assert.equal(siradaki(r3.d), 'b');
});
sina('Çifte Saldırı: hedef seçilir, sıra hedeften sonrakine geçer; Hepsini At; UNO cezası 2 basış', () => {
  const d = kur('extreme', { a: [[null, 'jokerVur'], ['k', '3'], ['k', '4']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']], e: [['m', '1'], ['m', '2']] }, ['k', '5']);
  hata(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'jokerVur'), renk: 'k' }, /rakip seç/);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'jokerVur'), renk: 'k', hedef: 'c' });
  assert.equal(siradaki(r.d), 'c'); assert.equal(r.d.yigin, 2);
  const r2 = yap(r.d, 'c', { t: 'cek' }, sabit(0));
  assert.equal(n(r2.d, 'c'), 4); assert.equal(siradaki(r2.d), 'e');
  const h = kur('extreme', { a: [['k', 'hepsiAt'], ['k', '3'], ['k', '4'], ['m', '9']], b: [['s', 'hepsiAt'], ['s', '2']] }, ['k', '5']);
  const h1 = yap(h, 'a', { t: 'oyna', kart: kid(h, 'a', 'k', 'hepsiAt') });
  assert.equal(n(h1.d, 'a'), 1);
  assert.deepEqual(gor(h1.d, 'b').oynanabilir, [kid(h, 'b', 's', 'hepsiAt')], 'Hepsini At üstüne başka renkten Hepsini At');
  const y = yap(h1.d, 'b', { t: 'yakala', hedef: 'a' }, sabit(0));
  assert.equal(n(y.d, 'a'), 3, 'yakalanan fırlatıcıya basar');
});

console.log('Flex');
sina('flex rengiyle oynama: güç yeşilken; geçerli renk kartın asıl rengi; güç kırmızıya döner', () => {
  const d = kur('flex', { a: [['m', '5', { fx: 'k' }], ['m', '2'], ['y', '3']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '7']);
  const kart = d.eller.a[0];
  kart.fx = 'k';
  const g = gor(d, 'a');
  assert.deepEqual(g.flex, [kart.id]); assert.deepEqual(g.yalnizFlex, [kart.id]); assert.deepEqual(g.oynanabilir, [kart.id]);
  hata(d, 'a', { t: 'oyna', kart: kart.id }, /yalnız flex yüzüyle/);
  const r = yap(d, 'a', { t: 'oyna', kart: kart.id, flex: true });
  assert.equal(r.d.aktifRenk, 'm'); assert.equal(r.d.guc!.a, false); assert.equal(siradaki(r.d), 'b');
  assert.equal(gor(r.d, 'b').oyuncular.find((o) => o.id === 'a')!.guc, false);
  // güç kırmızıyken flex yok
  const k = structuredClone(d); k.guc!.a = false;
  assert.deepEqual(gor(k, 'a').oynanabilir, []);
  hata(k, 'a', { t: 'oyna', kart: kart.id, flex: true }, /Güç kartın kırmızı/);
});
sina('flex aksiyonlar: +2 → herkes 1 çeker · Atlat → herkes atlanır · Yön → dön + atlat; hepsi kırmızı olunca hepsi yeşil', () => {
  const el: Tanim[] = [['k', '+2', { fx: 'k' }], ['k', 'pas', { fx: 'k' }], ['k', 'yon', { fx: 'k' }], ['k', '1']];
  const d = kur('flex', { a: el, b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']], e: [['m', '1'], ['m', '2']] }, ['k', '7']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', '+2', { fx: 'k' }), flex: true });
  assert.deepEqual([n(r.d, 'b'), n(r.d, 'c'), n(r.d, 'e')], [3, 3, 3]); assert.equal(siradaki(r.d), 'b');
  const duz = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', '+2', { fx: 'k' }) });
  assert.equal(n(duz.d, 'b'), 4); assert.equal(siradaki(duz.d), 'c'); assert.equal(duz.d.guc!.a, true);
  assert.equal(siradaki(yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', 'pas', { fx: 'k' }), flex: true }).d), 'a');
  const y = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', 'yon', { fx: 'k' }), flex: true });
  assert.equal(y.d.yon, -1); assert.equal(siradaki(y.d), 'c');
  const son = structuredClone(d); son.guc = { a: true, b: false, c: false, e: false };
  const s = yap(son, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', 'pas', { fx: 'k' }), flex: true });
  assert.deepEqual(s.d.guc, { a: true, b: true, c: true, e: true });
});
sina('flex jokerler, Güçleri Çevir, çevirme simgeli sayı, Flex +4 itirazı (4 / 6)', () => {
  const d = kur('flex', { a: [[null, 'fxHedef2'], [null, 'fxHerkes'], [null, 'fx+4'], [null, 'jokerCevir'], ['m', '4', { cv: 1 }], ['y', '1']], b: [['s', '1'], ['s', '2']], c: [['y', '2'], ['y', '3']] }, ['m', '7']);
  const h = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'fxHedef2'), renk: 'k', flex: true, hedef: 'c' });
  assert.equal(n(h.d, 'c'), 4); assert.equal(siradaki(h.d), 'b'); assert.equal(h.d.guc!.a, false);
  assert.equal(n(yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'fxHedef2'), renk: 'k' }).d, 'c'), 2, 'düz yüz: yalnız joker');
  const he = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'fxHerkes'), renk: 'k', flex: true });
  assert.deepEqual([n(he.d, 'b'), n(he.d, 'c')], [4, 4]);
  const cv = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'jokerCevir'), renk: 'k' });
  assert.deepEqual(cv.d.guc, { a: true, b: true, c: true }, 'hepsi kırmızıya döner → hepsi yeniden yeşil');
  const sayi = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'm', '4', { cv: 1 }) });
  assert.equal(sayi.d.guc!.a, false, 'çevirme simgeli sayı kendi gücünü çevirir');
  const dort = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'fx+4'), renk: 'k' });
  assert.equal(dort.d.bekle?.tur, 'itiraz');
  assert.equal(n(yap(dort.d, 'b', { t: 'itiraz' }).d, 'a'), 9, 'elde m ve joker vardı: itiraz haklı');
  const hedefli = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'fx+4'), renk: 'k', flex: true, hedef: 'c' });
  assert.equal(n(hedefli.d, 'c'), 6); assert.equal(siradaki(hedefli.d), 'b'); assert.equal(hedefli.d.bekle, null);
});

console.log('Takım');
const takimKur = (eller: Record<string, Tanim[]>, ust: Tanim, ek: Partial<UnoDurum> = {}) => kur('takim', eller, ust, ek);
sina('el başı: herkes ortağına 1 kart verir (aynı anda), sonra oyun başlar', () => {
  let d = unoMotor.elBaslat({ oyuncular: ['a', 'b', 'c', 'e'].map((id) => ({ id })), elNo: 1, baslayan: 0, rng: tohumlu(5), ayar: { unoMod: 'takim' } }) as UnoDurum;
  assert.equal(d.ver?.kalan.length, 4);
  assert.deepEqual(gor(d, 'a').ver, { kime: 'c', adet: 1, neden: 'takim' });
  assert.deepEqual(gor(d, 'a').oyuncular.map((o) => o.takim), [0, 1, 0, 1]);
  hata(d, siradaki(d), { t: 'cek' }, /vereceğin kartı seç/);
  const verilen: Record<string, number> = {};
  for (const id of ['a', 'b', 'c', 'e']) { verilen[id] = d.eller[id][0].id; d = yap(d, id, { t: 'ver', kart: verilen[id] }).d; korunum(d); }
  assert.equal(d.ver, null);
  assert(d.eller.c.some((k) => k.id === verilen.a) && d.eller.a.some((k) => k.id === verilen.c) && d.eller.e.some((k) => k.id === verilen.b));
  for (const id of ['a', 'b', 'c', 'e']) assert.equal(n(d, id), 7);
  assert.equal(d.atik[0].deger.length, 1);
});
sina('Takım Oyunu jokeri: sıra ortağa atlar, ortak oynamak zorunda; oynayamıyorsa oynayan 2 çeker', () => {
  const d = takimKur({ a: [[null, 'jokerTakim'], ['k', '1'], ['k', '2']], b: [['s', '1'], ['s', '2']], c: [['m', '3'], ['y', '9']], e: [['m', '1'], ['m', '2']] }, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'jokerTakim'), renk: 'm' });
  assert.equal(siradaki(r.d), 'c'); assert.equal(gor(r.d, 'c').takimOyun, true); assert.equal(gor(r.d, 'c').cekOlur, false);
  hata(r.d, 'c', { t: 'cek' }, /uyan bir kartını oynamalısın/);
  const r2 = yap(r.d, 'c', { t: 'oyna', kart: kid(d, 'c', 'm', '3'), uno: true });
  assert.equal(siradaki(r2.d), 'e'); assert.equal(r2.d.takimOyun, null);
  const o = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'jokerTakim'), renk: 's' });
  assert.equal(n(o.d, 'a'), 4, 'ortak oynayamadı: 2 çeker'); assert.equal(siradaki(o.d), 'e');
});
sina('Takıma +4: sıradaki 2 çeker ve atlanır, onun ortağı da 2 çeker; paslaşma simgesi', () => {
  const d = takimKur({ a: [[null, 'jokerTakim4'], ['k', '1', { ps: 1 }], ['k', '2']], b: [['s', '1'], ['s', '2']], c: [['m', '3'], ['y', '9']], e: [['m', '1'], ['m', '2']] }, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'jokerTakim4'), renk: 'm' });
  assert.deepEqual([n(r.d, 'b'), n(r.d, 'e'), n(r.d, 'c')], [4, 4, 2]); assert.equal(siradaki(r.d), 'c');
  const p = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', '1', { ps: 1 }) });
  assert.equal(p.d.ver?.neden, 'sembol'); assert.equal(siradaki(p.d), 'b');
  hata(p.d, 'b', { t: 'cek' }, /Kart verilmesi/);
  const aKart = p.d.eller.a[0].id, cKart = p.d.eller.c[0].id;
  const p2 = yap(yap(p.d, 'a', { t: 'ver', kart: aKart }).d, 'c', { t: 'ver', kart: cKart });
  assert.equal(p2.d.ver, null);
  assert(p2.d.eller.a.some((k) => k.id === cKart) && p2.d.eller.c.some((k) => k.id === aKart));
  assert.deepEqual([n(p2.d, 'a'), n(p2.d, 'c')], [2, 2]);
  yap(p2.d, 'b', { t: 'cek' });
});
sina('eli biten: ortak yarısını verir (büyük parça onda kalır); ortağın 1 kartı varsa çıkar; ikisi de bitince takım kazanır', () => {
  const d = takimKur({ a: [['k', '1']], b: [['s', '1'], ['s', '2']], c: [['m', '3'], ['y', '9'], ['y', '8'], ['y', '7'], ['y', '6']], e: [['m', '1'], ['m', '2']] }, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', '1') });
  assert.equal(r.d.sonuc, null);
  assert.deepEqual(r.d.ver?.kalan, [{ kim: 'c', kime: 'a', adet: 2 }]);
  assert.deepEqual(gor(r.d, 'c').ver, { kime: 'a', adet: 2, neden: 'yari' });
  let x = yap(r.d, 'c', { t: 'ver', kart: r.d.eller.c[0].id }).d;
  assert.equal(n(x, 'a'), 0, 'kartlar hepsi verilince geçer');
  x = yap(x, 'c', { t: 'ver', kart: x.eller.c[0].id }).d;
  assert.deepEqual([n(x, 'a'), n(x, 'c')], [2, 3]); assert.equal(x.ver, null);
  korunum(x);
  // ortağın 1 kartı: oyuncu çıkar, sıra onu atlar; ortak çekince yarısını verir
  const c1 = takimKur({ a: [['k', '1']], b: [['s', '1'], ['s', '2']], c: [['m', '3']], e: [['m', '1'], ['m', '2']] }, ['k', '5']);
  const r1 = yap(c1, 'a', { t: 'oyna', kart: kid(c1, 'a', 'k', '1') });
  assert.equal(r1.d.ver, null); assert(r1.olaylar.some((o) => o.t === 'cikti' && o.o === 'a'));
  assert.equal(gor(r1.d, 'b').oyuncular[0].cikti, true);
  let y = yap(r1.d, 'b', { t: 'cek' }).d; y = yap(y, 'b', { t: 'pas' }).d;
  assert.equal(siradaki(y), 'c');
  usteAl(y, 's', '9'); usteAl(y, 's', '8');
  y = yap(y, 'c', { t: 'cek' }).d; // c 2 kart oldu → yarısı (1) a'ya
  assert.deepEqual(y.ver?.kalan, [{ kim: 'c', kime: 'a', adet: 1 }]);
  y = yap(y, 'c', { t: 'ver', kart: y.eller.c[0].id }).d;
  assert.deepEqual([n(y, 'a'), n(y, 'c')], [1, 1]);
  // kazanma: a çıkmış, c son kartını oynar
  const k = takimKur({ a: [['k', '1']], b: [['s', '1'], ['s', '2']], c: [['k', '3']], e: [['m', '1'], [null, 'joker']] }, ['k', '5']);
  let z = yap(k, 'a', { t: 'oyna', kart: kid(k, 'a', 'k', '1') }).d;
  z = yap(yap(z, 'b', { t: 'cek' }).d, 'b', { t: 'pas' }).d;
  z = yap(z, 'c', { t: 'oyna', kart: kid(k, 'c', 'k', '3') }).d;
  assert.deepEqual(z.sonuc?.kazananlar, ['a', 'c']);
  const puan = (id: string) => z.sonuc!.satirlar.find((s) => s.id === id)!.puan;
  assert(puan('a') === puan('c') && puan('a') > 50 && puan('e') === -51);
  // ortak, ortağı için UNO diyebilir; ortağını yakalayamaz
  const u = takimKur({ a: [['k', '1'], ['k', '2']], b: [['s', '1'], ['s', '2']], c: [['k', '3'], ['y', '2']], e: [['m', '1'], ['m', '2']] }, ['k', '5']);
  const u1 = yap(u, 'a', { t: 'oyna', kart: kid(u, 'a', 'k', '1') });
  hata(u1.d, 'c', { t: 'yakala', hedef: 'a' }, /Ortağını yakalayamazsın/);
  assert.deepEqual(yap(u1.d, 'c', { t: 'uno' }).d.unoDedi, ['a']);
});

console.log('Yalancı');
const YL = { yl: 1 as const };
sina('yalancı kartı kapalı oynanır, söylenen ortadakine uymalı; düz kart açık oynanır', () => {
  const d = kur('yalanci', { a: [['m', '3', YL], ['k', '2'], ['y', '9']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const yk = kid(d, 'a', 'm', '3', YL);
  assert.deepEqual(gor(d, 'a').oynanabilir.sort(), [yk, kid(d, 'a', 'k', '2')].sort());
  hata(d, 'a', { t: 'oyna', kart: yk }, /ne olduğunu söylemelisin/);
  hata(d, 'a', { t: 'oyna', kart: yk, kapali: true, beyan: { renk: 'm', deger: '3' } }, /ortadakine uymalı/);
  hata(d, 'a', { t: 'oyna', kart: yk, kapali: true, beyan: { renk: 'k', deger: 'jokerMeydan' } }, /ne olduğunu söylemelisin/);
  const r = yap(d, 'a', { t: 'oyna', kart: yk, kapali: true, beyan: { renk: 'k', deger: '8' } });
  assert.deepEqual(gor(r.d, 'b').bekle, { tur: 'yalan', oynayan: 'a', beyan: { renk: 'k', deger: '8' }, karar: 'b' });
  // gizlilik: kimse gerçek kartı görmez
  for (const b of ['a', 'b', 'c', null]) assert.deepEqual(gor(r.d, b).ust, { id: yk, renk: 'k', deger: '8', kp: 1 });
  assert(!JSON.stringify(r.olaylar).includes('"deger":"3"'));
  assert.equal(gor(r.d, 'b').sira, 'b');
  hata(r.d, 'b', { t: 'cek' }, /inan ya da yalan de/);
  hata(r.d, 'c', { t: 'inan' }, /sıradaki oyuncunun kararı/);
  hata(r.d, 'a', { t: 'yalan' }, /Kendi kartın/);
  // inan: söylenen kart sayılır, kart kapalı kalır
  const i = yap(r.d, 'b', { t: 'inan' });
  assert.equal(i.d.aktifRenk, 'k'); assert.equal(siradaki(i.d), 'b'); assert.deepEqual(gor(i.d, 'b').ust, { id: yk, renk: 'k', deger: '8', kp: 1 });
  assert.deepEqual(gor(i.d, 'b').oynanabilir, [], 'b: s1, s2 uymuyor (k8)');
  // yalan yakalandı: kart geri döner, yalancı 1 çeker, sırası geçer
  const y = yap(r.d, 'c', { t: 'yalan' });
  assert.equal(n(y.d, 'a'), 4); assert.equal(y.d.atik.length, 1); assert.equal(siradaki(y.d), 'b'); assert.equal(y.d.aktifRenk, 'k');
  assert(y.d.eller.a.some((k) => k.id === yk && !k.by));
  korunum(y.d);
  // doğru söylemiş: kart açılır, itiraz eden 1 çeker
  const t = kur('yalanci', { a: [['k', '3', YL], ['k', '2'], ['y', '9']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const t1 = yap(t, 'a', { t: 'oyna', kart: kid(t, 'a', 'k', '3', YL), kapali: true, beyan: { renk: 'k', deger: '3' } });
  const t2 = yap(t1.d, 'c', { t: 'yalan' });
  assert.equal(n(t2.d, 'c'), 3); assert.equal(n(t2.d, 'a'), 2); assert.equal(siradaki(t2.d), 'b');
  assert.deepEqual(gor(t2.d, 'b').ust, { id: kid(t, 'a', 'k', '3', YL), renk: 'k', deger: '3', yl: 1 });
});
sina('söylenen aksiyon inanılınca uygulanır (+2, +4); düz kartı kapalı oynamak yakalanırsa 6 kart', () => {
  const d = kur('yalanci', { a: [['m', '3', YL], ['k', '2'], ['y', '9']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const yk = kid(d, 'a', 'm', '3', YL);
  const r = yap(yap(d, 'a', { t: 'oyna', kart: yk, kapali: true, beyan: { renk: 'k', deger: '+2' } }).d, 'b', { t: 'inan' });
  assert.equal(n(r.d, 'b'), 4); assert.equal(siradaki(r.d), 'c');
  const r4 = yap(yap(d, 'a', { t: 'oyna', kart: yk, kapali: true, beyan: { renk: 's', deger: '+4' } }).d, 'b', { t: 'inan' });
  assert.equal(n(r4.d, 'b'), 6); assert.equal(r4.d.aktifRenk, 's'); assert.equal(siradaki(r4.d), 'c');
  const duz = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', '2'), kapali: true, beyan: { renk: 'k', deger: '2' } });
  const y = yap(duz.d, 'b', { t: 'yalan' });
  assert.equal(n(y.d, 'a'), 9, 'düz kart kapalı: geri alır + 6');
});
sina('son kart kapalı: inanılırsa kazanır, yalan yakalanırsa oyun sürer; 7 takas hedefli', () => {
  const d = kur('yalanci', { a: [['m', '3', YL]], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: d.eller.a[0].id, kapali: true, beyan: { renk: 'k', deger: '1' } });
  assert.equal(r.d.sonuc, null); assert.equal(n(r.d, 'a'), 0);
  assert.deepEqual(yap(r.d, 'b', { t: 'inan' }).d.sonuc?.kazananlar, ['a']);
  const y = yap(r.d, 'c', { t: 'yalan' });
  assert.equal(y.d.sonuc, null); assert.equal(n(y.d, 'a'), 2);
  const t = kur('yalanci', { a: [['k', '7'], ['m', '1'], ['m', '2'], ['m', '4']], b: [['s', '1'], ['s', '2']], c: [['y', '1']] }, ['k', '5']);
  const t1 = yap(t, 'a', { t: 'oyna', kart: kid(t, 'a', 'k', '7'), hedef: 'c' });
  assert.deepEqual([n(t1.d, 'a'), n(t1.d, 'c')], [1, 3]);
});
sina('Meydan Okuma: herkes kapalı kart koyar; yalancı kartını geri alıp 1 çeker; doğru renk sorguyu bitirir', () => {
  const d = kur('yalanci', { a: [[null, 'jokerMeydan'], ['k', '2'], ['y', '9']], b: [['s', '1'], ['m', '2']], c: [['y', '1'], ['m', '4']], e: [['m', '6'], ['k', '9']] }, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'jokerMeydan'), renk: 'm' });
  assert.deepEqual(gor(r.d, 'b').bekle, { tur: 'meydan', oynayan: 'a', renk: 'm', asama: 'koy', koymayan: ['b', 'c', 'e'], konan: [] });
  hata(r.d, 'a', { t: 'sorgula', hedef: 'b' }, /sorgulayamazsın/);
  let x = yap(r.d, 'b', { t: 'koy', kart: kid(d, 'b', 's', '1') }).d; // yalan
  hata(x, 'b', { t: 'koy', kart: kid(d, 'b', 'm', '2') });
  x = yap(x, 'c', { t: 'koy', kart: kid(d, 'c', 'm', '4') }).d; // doğru
  x = yap(x, 'e', { t: 'koy', kart: kid(d, 'e', 'k', '9') }).d; // yalan
  korunum(x);
  assert.equal(gor(x, 'a').bekle?.tur === 'meydan' && (gor(x, 'a').bekle as { asama: string }).asama, 'sorgu');
  assert.equal(gor(x, 'a').sira, 'a');
  const s1 = yap(x, 'a', { t: 'sorgula', hedef: 'b' });
  assert.equal(n(s1.d, 'b'), 3, 'yalancı: kart geri + 1'); assert.equal(s1.d.bekle?.tur, 'meydan');
  hata(s1.d, 'a', { t: 'sorgula', hedef: 'b' }, /sorgulanamaz/);
  const s2 = yap(s1.d, 'a', { t: 'sorgula', hedef: 'c' }); // doğru renk → biter; e sorgulanmadan kurtulur
  assert.equal(s2.d.bekle, null); assert.equal(s2.d.aktifRenk, 'm'); assert.equal(siradaki(s2.d), 'b');
  assert.deepEqual([n(s2.d, 'c'), n(s2.d, 'e')], [1, 1]);
  assert.equal(s2.d.atik[s2.d.atik.length - 1].deger, 'jokerMeydan');
  assert.deepEqual(s2.d.unoDedi.sort(), ['c', 'e']);
  korunum(s2.d);
  // yeter: hepsi kurtulur; son kartını koyan kazanır
  const tek = kur('yalanci', { a: [[null, 'jokerMeydan'], ['k', '2'], ['y', '9']], b: [['s', '1']], c: [['y', '1'], ['m', '4']] }, ['k', '5']);
  let z = yap(tek, 'a', { t: 'oyna', kart: kid(tek, 'a', null, 'jokerMeydan'), renk: 'm' }).d;
  z = yap(z, 'b', { t: 'koy', kart: kid(tek, 'b', 's', '1') }).d;
  z = yap(z, 'c', { t: 'koy', kart: kid(tek, 'c', 'y', '1') }).d;
  assert.deepEqual(yap(z, 'a', { t: 'yeter' }).d.sonuc?.kazananlar, ['b']);
});

console.log('Deluxe · Express · Sevimli Dostlar');
sina('Express: 5 kart, +1, Joker +2 itirazı; Deluxe: klasik kurallar, hedef 500', () => {
  const e = unoMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }], elNo: 1, baslayan: 0, rng: tohumlu(2), ayar: { unoMod: 'express' } }) as UnoDurum;
  assert.equal(e.eller.a.length + e.eller.b.length >= 10, true);
  assert.equal(gor(e, 'a').hedefPuan, 250);
  const d = kur('express', { a: [[null, 'joker+2'], ['y', '3'], ['m', '4']], b: [['s', '1'], ['s', '2']] }, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'joker+2'), renk: 'm' });
  assert.equal(r.d.bekle?.tur, 'itiraz');
  assert.equal(n(yap(r.d, 'b', { t: 'itiraz' }).d, 'b'), 6);
  const dl = kur('deluxe', { a: [[null, '+4'], ['y', '3'], ['m', '4']], b: [['s', '1'], ['s', '2']] }, ['k', '5']);
  assert.equal(yap(dl, 'a', { t: 'oyna', kart: kid(dl, 'a', null, '+4'), renk: 'm' }).d.bekle?.tur, 'itiraz');
  assert.equal(gor(dl, 'a').hedefPuan, 500);
});
sina('Sevimli Dostlar: hediye, siper, şaka, gökkuşağı', () => {
  const el: Tanim[] = [[null, 'kitty'], [null, 'batman'], [null, 'kuromi'], [null, 'pony'], ['m', '1'], ['m', '2'], ['y', '9']];
  const d = kur('dostlar', { a: el, b: [['k', '+2'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  // Kedicik: seçilen rakibe 2 kart verilir
  hata(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'kitty'), renk: 'm' }, /rakip seç/);
  const k = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'kitty'), renk: 'm', hedef: 'c' });
  assert.deepEqual(gor(k.d, 'a').ver, { kime: 'c', adet: 2, neden: 'hediye' });
  let x = yap(k.d, 'a', { t: 'ver', kart: kid(d, 'a', 'y', '9') }).d;
  x = yap(x, 'a', { t: 'ver', kart: kid(d, 'a', null, 'batman') }).d;
  assert.deepEqual([n(x, 'a'), n(x, 'c')], [4, 4]); assert.equal(siradaki(x), 'b');
  // Yarasa: ceza yokken herkesi atlatır
  assert.equal(siradaki(yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'batman'), renk: 'm' }).d), 'a');
  // Yaramaz Tavşan: bütün rakipler 1 çeker
  const ku = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'kuromi'), renk: 'm' });
  assert.deepEqual([n(ku.d, 'b'), n(ku.d, 'c')], [3, 3]); assert.equal(siradaki(ku.d), 'b');
  // Gökkuşağı Tayı: seçilen rengin hepsi atılır
  const po = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'pony'), renk: 'm' });
  assert.equal(n(po.d, 'a'), 4); assert.equal(po.d.atik[po.d.atik.length - 1].deger, 'pony'); assert.equal(po.d.aktifRenk, 'm');
  korunum(po.d);
  // Siper: biriken cezayı siler
  const s = kur('dostlar', { a: [['k', '+2'], ['k', '1'], ['k', '3']], b: [[null, 'batman'], ['s', '2'], ['s', '3']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const s1 = yap(s, 'a', { t: 'oyna', kart: kid(s, 'a', 'k', '+2') });
  assert.equal(s1.d.yigin, 2);
  assert.deepEqual(gor(s1.d, 'b').oynanabilir, [kid(s, 'b', null, 'batman')]);
  const s2 = yap(s1.d, 'b', { t: 'oyna', kart: kid(s, 'b', null, 'batman'), renk: 's' });
  assert.equal(s2.d.yigin, 0); assert.equal(n(s2.d, 'b'), 2); assert.equal(siradaki(s2.d), 'c');
  assert(s2.olaylar.some((o) => o.t === 'siper'));
});

sina('asistan: hedefli kartta hedef, takasta en az kartlı rakip, bekleyen kararlar için öneri', () => {
  const d = kur('hepsiJoker', { a: [[null, 'jokerTakas'], [null, 'joker'], [null, 'joker'], [null, 'joker'], [null, 'joker']], b: [[null, 'joker'], [null, 'jokerYon']], c: [[null, 'joker'], [null, 'joker'], [null, 'joker']] }, [null, 'joker']);
  assert.deepEqual(oneri(gor(d, 'a'), 'a')?.hamle, { t: 'oyna', kart: kid(d, 'a', null, 'jokerTakas'), hedef: 'b' });
  assert.equal(hedefGerek('noMercy', '7', false), true); assert.equal(hedefGerek('klasik', '7', false), false); assert.equal(hedefGerek('flex', 'fx+4', false), false);
  const t = takimKur({ a: [['k', '1'], ['k', '2']], b: [['s', '1'], ['s', '2']], c: [['k', '3'], ['y', '2']], e: [['m', '1'], ['m', '2']] }, ['k', '5'], { ver: { neden: 'takim', kalan: [{ kim: 'a', kime: 'c', adet: 1 }], tampon: [] } });
  assert.equal(oneri(gor(t, 'a'), 'a')?.hamle.t, 'ver');
  assert.equal(oneri(gor(t, 'b'), 'b'), null);
});

/* ------------------------------------------------------------------ rastgele oyun ------------------------------------------------------------------ */

console.log('Rastgele oyun (hepsi bot, mod başına)');
const EL = Number(process.env.UNO_EL) || 120;
const MODLAR: UnoMod[] = ['deluxe', 'express', 'flip', 'hepsiJoker', 'noMercy', 'extreme', 'flex', 'takim', 'yalanci', 'dostlar', 'yediSifir'];
for (const mod of MODLAR) {
  const tanim = unoModTanim(mod);
  const sayilar = tanim.cift ? [4, 6, 8] : [2, 3, 4, 5, 6, 7, 8].filter((x) => x >= tanim.enAz && x <= tanim.enCok);
  let hamle = 0, enUzun = 0, el = 0;
  const olay: Record<string, number> = {};
  for (const N of sayilar) {
    const rng = tohumlu(9000 + N * 17 + mod.length);
    const oyuncular = Array.from({ length: N }, (_, i) => ({ id: `b${i}` }));
    for (let e = 0; e < EL; e++) {
      let d = unoMotor.elBaslat({ oyuncular, elNo: e + 1, baslayan: e % N, rng, ayar: { unoMod: mod } }) as UnoDurum;
      korunum(d);
      let adim = 0;
      while (!unoMotor.sonuc(d)) {
        assert(++adim <= 12000, `el sonlanmadı (${mod}, n=${N}, el=${e})`);
        const ilk = Math.floor(rng() * N);
        let o = '', h: UnoHamle | null = null;
        for (let i = 0; i < N && !h; i++) { o = oyuncular[(ilk + i) % N].id; h = unoMotor.botHamle(d, o, rng) as UnoHamle | null; }
        assert(h, `hiçbir botun hamlesi yok (${mod}, n=${N}, el=${e}, adım=${adim}): ${JSON.stringify({ kim: siradaki(d), bekle: d.bekle, ver: d.ver?.kalan, yigin: d.yigin })}`);
        if (h.t === 'oyna' && rng() < 0.25) h = { ...h, uno: false };
        const once = adim % 41 === 0 ? JSON.stringify(d) : null;
        const r = unoMotor.uygula(d, o, h, rng);
        assert(!('hata' in r), `bot hatalı hamle (${mod}, n=${N}): ${o} ${JSON.stringify(h)} → ${'hata' in r ? r.hata : ''}`);
        if (once) assert.equal(JSON.stringify(d), once);
        for (const ol of r.olaylar) olay[ol.t] = (olay[ol.t] || 0) + 1;
        d = r.durum as UnoDurum;
        korunum(d);
        for (const id of d.unoDedi.concat(d.yakalanabilir)) assert.equal(d.eller[id].length, 1);
        // görünümler: her bakan için kurulabilir, gizli bilgi sızmaz
        if (adim % 13 === 0) for (const b of [siradaki(d), null]) {
          const g = gor(d, b);
          assert(g.oynanabilir.every((id) => g.elim.some((k) => k.id === id)));
          const js = JSON.stringify(g);
          assert(!js.includes('"by"') && !js.includes('"tampon"') && !js.includes('"haksiz"') && !js.includes('"konan":{'), 'gizli alan sızdı');
          if (mod === 'flip') assert(g.elim.every((k) => !('arka' in k)));
        }
      }
      hamle += adim; enUzun = Math.max(enUzun, adim); el++;
      const s = unoMotor.sonuc(d)!;
      assert(s.kazananlar.length >= 1);
      assert.equal(s.satirlar.length, N);
      if (mod === 'takim') assert.equal(s.kazananlar.length, 2);
      const kazananPuan = s.satirlar.find((x) => x.kazandi)!.puan;
      assert.equal(kazananPuan, 0 - s.satirlar.filter((x) => !x.kazandi).reduce((t, x) => t + x.puan, 0), 'kazanan puanı = kaybedenlerin toplamı');
      assert.equal(unoMotor.botHamle(d, 'b0', rng), null);
    }
  }
  const ozet = Object.entries(olay).filter(([k]) => ['flip', 'elendi', 'firlat', 'guc', 'gucHepsi', 'verildi', 'yalan', 'inandi', 'meydan', 'sorgu', 'siper', 'rulet', 'takimOyun', 'cikti', 'dondu', 'attiHepsi', 'takas', 'devir', 'itiraz', 'karildi', 'yigin'].includes(k)).map(([k, v]) => `${k} ${v}`).join(', ');
  console.log(`  ✓ ${tanim.ad}: ${el} el (${sayilar.join('/')} oyuncu), ort. ${(hamle / el).toFixed(0)} hamle, en uzun ${enUzun} · ${ozet}`);
}

/* ------------------------------------------------------------------ bulanık ------------------------------------------------------------------ */

console.log('Bulanık (rastgele ve bozuk hamleler)');
{
  const rng = tohumlu(77);
  const sec = <T,>(a: readonly T[]): T => a[Math.floor(rng() * a.length)];
  const renkler: (UnoRenk | undefined)[] = ['k', 's', 'y', 'm', undefined];
  let deneme = 0, gecerli = 0;
  for (const mod of [...MODLAR, 'klasik'] as UnoMod[]) {
    const N = mod === 'takim' ? 4 : 3;
    const oyuncular = Array.from({ length: N }, (_, i) => ({ id: `p${i}` }));
    for (let e = 0; e < 12; e++) {
      let d = unoMotor.elBaslat({ oyuncular, elNo: 1, baslayan: 0, rng, ayar: { unoMod: mod } }) as UnoDurum;
      for (let i = 0; i < 900 && !d.sonuc; i++) {
        const o = sec(oyuncular).id;
        const el = d.eller[o];
        const kart = el.length ? sec(el).id : -1;
        const hedef = sec(oyuncular).id;
        const turler = ['oyna', 'oyna', 'oyna', 'cek', 'pas', 'uno', 'yakala', 'renk', 'kabul', 'itiraz', 'ver', 'inan', 'yalan', 'koy', 'sorgula', 'yeter', 'bozuk'];
        const t = sec(turler);
        const h: Record<string, unknown> = { t, kart: rng() < 0.05 ? 9999 : kart, renk: sec(renkler), hedef: rng() < 0.1 ? 'yok' : hedef, flex: rng() < 0.3, uno: rng() < 0.5 };
        if (rng() < 0.4) { h.kapali = true; h.beyan = { renk: sec(renkler), deger: sec(UNO_DEGERLER) }; }
        deneme++;
        const r = rng() < 0.02 ? unoMotor.uygula(d, o, sec([null, 5, 'x', [], {}] as unknown[]), rng) : unoMotor.uygula(d, o, h, rng);
        if (!('hata' in r)) { gecerli++; d = r.durum as UnoDurum; korunum(d); for (const b of [o, null]) gor(d, b); }
        else assert(typeof r.hata === 'string' && r.hata.length > 3 && r.hata !== 'Hamle işlenemedi.', `motor istisnası (${mod}): ${JSON.stringify(h)}`);
        // tıkanma olmasın: arada botlar yürütür
        if (i % 9 === 0) for (const p of oyuncular) { const bh = unoMotor.botHamle(d, p.id, rng); if (bh) { const br = unoMotor.uygula(d, p.id, bh, rng); assert(!('hata' in br), `bot hatalı (${mod}): ${JSON.stringify(bh)} → ${'hata' in br ? br.hata : ''}`); d = br.durum as UnoDurum; korunum(d); break; } }
      }
    }
  }
  console.log(`  ✓ ${deneme} hamle denemesi (${gecerli} geçerli), istisna yok`);
}

console.log(`\nTAMAM: ${adet} birim sınaması + ${MODLAR.length} mod rastgele oyun + bulanık`);
