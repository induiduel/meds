/**
 * Uno motoru sınaması: `npx tsx src/services/masa/motor/uno.sinama.ts` (hata → çıkış ≠ 0)
 */
import assert from 'node:assert/strict';
import type { Olay, Rng, UnoDeger, UnoGorunum, UnoHamle, UnoKart, UnoRenk } from '../tipler';
import { unoDeste, unoMotor, type UnoDurum } from './uno';
import { UNO_DEGER_AD, elSirala, kartDegeri, oneri, oynanabilirMi } from './unoAsistan';

const tohumlu = (t: number): Rng => () => {
  t = (t + 0x6d2b79f5) | 0;
  let x = Math.imul(t ^ (t >>> 15), 1 | t);
  x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x;
  return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
};
const rng0 = tohumlu(1);

type Tanim = [UnoRenk | null, UnoDeger];
type Tamam = { durum: unknown; olaylar: Olay[] };

/** Elle kurulmuş durum: verilen eller + üst kart; kalan kartlar destede */
function kur(eller: Record<string, Tanim[]>, ust: Tanim, ek: Partial<UnoDurum> = {}): UnoDurum {
  const havuz = unoDeste();
  const al = ([r, v]: Tanim): UnoKart => {
    const i = havuz.findIndex((k) => k.renk === r && k.deger === v);
    assert(i >= 0, `kart yok: ${r}${v}`);
    return havuz.splice(i, 1)[0];
  };
  const ids = Object.keys(eller);
  return {
    tur: 'uno', elNo: 1, oyuncular: ids, kim: 0, yon: 1,
    eller: Object.fromEntries(ids.map((id) => [id, eller[id].map(al)])),
    atik: [al(ust)], deste: havuz, aktifRenk: ust[0] ?? 'k',
    cektiBuTur: false, cekilen: null, unoDedi: [], yakalanabilir: [],
    cezalar: Object.fromEntries(ids.map((id) => [id, []])), sonuc: null, ...ek,
  };
}
const kid = (d: UnoDurum, o: string, r: UnoRenk | null, v: UnoDeger): number => {
  const k = d.eller[o].find((x) => x.renk === r && x.deger === v);
  assert(k, `elde yok: ${o} ${r}${v}`);
  return k.id;
};
function yap(d: UnoDurum, o: string, h: unknown, rng: Rng = rng0): { d: UnoDurum; olaylar: Olay[] } {
  const r = unoMotor.uygula(d, o, h, rng);
  assert(!('hata' in r), `beklenmeyen hata: ${'hata' in r ? r.hata : ''}`);
  return { d: (r as Tamam).durum as UnoDurum, olaylar: (r as Tamam).olaylar };
}
function hata(d: UnoDurum, o: string, h: unknown, re?: RegExp): void {
  const r = unoMotor.uygula(d, o, h, rng0);
  assert('hata' in r, `hata bekleniyordu: ${JSON.stringify(h)}`);
  if (re) assert.match(r.hata, re);
}
const gor = (d: UnoDurum, b: string | null) => unoMotor.gorunum(d, b) as UnoGorunum;
const siradaki = (d: UnoDurum) => d.oyuncular[d.kim];
/** Destenin üstüne (ilk çekilecek) belirli kartı getir */
function usteAl(d: UnoDurum, r: UnoRenk | null, v: UnoDeger): number {
  const i = d.deste.findIndex((k) => k.renk === r && k.deger === v);
  assert(i >= 0);
  const [k] = d.deste.splice(i, 1);
  d.deste.push(k);
  return k.id;
}
function korunum(d: UnoDurum): void {
  const hepsi = [...d.deste, ...d.atik, ...d.oyuncular.flatMap((id) => d.eller[id])];
  assert.equal(hepsi.length, 108, 'kart korunumu');
  assert.equal(new Set(hepsi.map((k) => k.id)).size, 108, 'tekil kimlik');
}

let adet = 0;
function sina(ad: string, f: () => void): void {
  f();
  adet++;
  console.log(`  ✓ ${ad}`);
}

console.log('Birim');

sina('deste bileşimi: 108 kart, dağılım', () => {
  const d = unoDeste();
  assert.equal(d.length, 108);
  assert.deepEqual(d.map((k) => k.id), Array.from({ length: 108 }, (_, i) => i));
  const say = (r: UnoRenk | null, v: UnoDeger) => d.filter((k) => k.renk === r && k.deger === v).length;
  for (const r of ['k', 's', 'y', 'm'] as const) {
    assert.equal(d.filter((k) => k.renk === r).length, 25);
    assert.equal(say(r, '0'), 1);
    for (const v of ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'pas', 'yon', '+2'] as const) assert.equal(say(r, v), 2);
    assert.equal(say(r, 'joker') + say(r, '+4'), 0);
  }
  assert.equal(say(null, 'joker'), 4);
  assert.equal(say(null, '+4'), 4);
  assert.equal(d.filter((k) => k.renk === null).length, 8);
});

sina('elBaslat: 7 kart, ilk kart sayı, aktif renk, başlayan, yön', () => {
  for (let n = 2; n <= 8; n++) for (let t = 0; t < 200; t++) {
    const oyuncular = Array.from({ length: n }, (_, i) => ({ id: `o${i}` }));
    const d = unoMotor.elBaslat({ oyuncular, elNo: 3, baslayan: t % n, rng: tohumlu(n * 1000 + t) }) as UnoDurum;
    korunum(d);
    for (const o of oyuncular) assert.equal(d.eller[o.id].length, 7);
    assert.equal(d.atik.length, 1);
    assert.match(d.atik[0].deger, /^\d$/);
    assert.equal(d.aktifRenk, d.atik[0].renk);
    assert.equal(siradaki(d), `o${t % n}`);
    assert.equal(d.yon, 1);
    assert.equal(d.deste.length, 108 - 7 * n - 1);
    assert.deepEqual(JSON.parse(JSON.stringify(d)), d, 'düz JSON');
  }
  // Bozuk rng'de de sonlanır ve sayı kartı açılır
  for (const r of [() => 0, () => 0.999999, () => 1, () => NaN, () => -3]) {
    const d = unoMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }], elNo: 1, baslayan: 0, rng: r }) as UnoDurum;
    korunum(d);
    assert.match(d.atik[0].deger, /^\d$/);
  }
  assert.throws(() => unoMotor.elBaslat({ oyuncular: [{ id: 'a' }], elNo: 1, baslayan: 0, rng: rng0 }));
});

sina('oynanabilirlik: renk, değer, simge, joker; uymayan kart ve sıra dışı hata', () => {
  const d = kur({ a: [['k', '3'], ['m', '5'], ['m', '7'], [null, 'joker'], ['s', 'pas']], b: [['k', '1'], ['y', '2']] }, ['k', '5']);
  assert.deepEqual(new Set(gor(d, 'a').oynanabilir), new Set([kid(d, 'a', 'k', '3'), kid(d, 'a', 'm', '5'), kid(d, 'a', null, 'joker')]));
  assert.deepEqual(gor(d, 'b').oynanabilir, []);
  hata(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'm', '7') }, /oynanamaz/);
  hata(d, 'b', { t: 'oyna', kart: kid(d, 'b', 'k', '1') }, /Sıra sende değil/);
  hata(d, 'a', { t: 'oyna', kart: kid(d, 'b', 'k', '1') }, /elinde yok/);
  hata(d, 'x', { t: 'cek' }, /Bu oyunda değilsin/);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'm', '5'), renk: 'y' }); // renkli kartta renk yok sayılır
  assert.equal(r.d.aktifRenk, 'm');
  assert.equal(siradaki(r.d), 'b');
  // simge eşleşmesi: farklı renkte pas üstüne pas
  const d2 = kur({ a: [['s', 'pas'], ['s', '1'], ['s', '2']], b: [['k', '1'], ['y', '2']], c: [['k', '2'], ['y', '3']] }, ['k', '5']);
  d2.atik.push(d2.deste.splice(d2.deste.findIndex((k) => k.renk === 'k' && k.deger === 'pas'), 1)[0]);
  assert.deepEqual(gor(d2, 'a').oynanabilir, [kid(d2, 'a', 's', 'pas')]);
  assert.equal(oynanabilirMi({ id: 1, renk: null, deger: '+4' }, { id: 2, renk: 'k', deger: '5' }, 'm'), true);
});

sina('pas: sıradaki atlanır (3 oyuncu) · 2 oyuncuda oynayan yeniden oynar', () => {
  const el: Record<string, Tanim[]> = { a: [['k', 'pas'], ['k', '1'], ['k', '2']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] };
  const d = kur(el, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', 'pas') });
  assert.equal(siradaki(r.d), 'c');
  assert(r.olaylar.some((o) => o.t === 'atlandi' && o.o === 'b'));
  assert(r.olaylar.some((o) => o.t === 'sira' && o.o === 'c'));
  const d2 = kur({ a: el.a, b: el.b }, ['k', '5']);
  const r2 = yap(d2, 'a', { t: 'oyna', kart: kid(d2, 'a', 'k', 'pas') });
  assert.equal(siradaki(r2.d), 'a');
});

sina('yon: yön döner (3 oyuncu) · 2 oyuncuda atlat gibi', () => {
  const el: Record<string, Tanim[]> = { a: [['k', 'yon'], ['k', '1'], ['k', '2']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] };
  const d = kur(el, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', 'yon') });
  assert.equal(r.d.yon, -1);
  assert.equal(siradaki(r.d), 'c');
  assert(r.olaylar.some((o) => o.t === 'yon' && o.yon === -1));
  assert(!r.olaylar.some((o) => o.t === 'atlandi'));
  const d2 = kur({ a: el.a, b: el.b }, ['k', '5']);
  const r2 = yap(d2, 'a', { t: 'oyna', kart: kid(d2, 'a', 'k', 'yon') });
  assert.equal(r2.d.yon, -1);
  assert.equal(siradaki(r2.d), 'a');
  assert(r2.olaylar.some((o) => o.t === 'atlandi' && o.o === 'b'));
});

sina('+2 / +4: sıradaki çeker ve sırası geçer; joker/+4 renksiz hata', () => {
  const el: Record<string, Tanim[]> = { a: [['k', '+2'], [null, '+4'], [null, 'joker'], ['k', '1']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] };
  const d = kur(el, ['k', '5']);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', '+2') });
  assert.equal(r.d.eller.b.length, 4);
  assert.equal(siradaki(r.d), 'c');
  assert.deepEqual(r.olaylar.find((o) => o.t === 'cekti'), { t: 'cekti', o: 'b', adet: 2, neden: '+2' });
  korunum(r.d);

  hata(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, '+4') }, /renk seçmelisin/);
  hata(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'joker') }, /renk seçmelisin/);
  hata(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'joker'), renk: 'x' }, /renk seçmelisin/);
  const r4 = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, '+4'), renk: 'm' });
  assert.equal(r4.d.eller.b.length, 6);
  assert.equal(r4.d.aktifRenk, 'm');
  assert.equal(siradaki(r4.d), 'c');
  assert.equal(r4.d.atik[r4.d.atik.length - 1].renk, null);
  assert(r4.olaylar.some((o) => o.t === 'renk' && o.renk === 'm'));
  assert.equal(r4.olaylar.find((o) => o.t === 'cekti')?.adet, 4);
  // 2 oyuncuda +2: oynayan yeniden oynar
  const d2 = kur({ a: el.a, b: el.b }, ['k', '5']);
  assert.equal(siradaki(yap(d2, 'a', { t: 'oyna', kart: kid(d2, 'a', 'k', '+2') }).d), 'a');
  // joker: renk değişir, sıra normal ilerler; +4 her zaman oynanabilir (elde aktif renk olsa da)
  const rj = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', null, 'joker'), renk: 'y' });
  assert.equal(rj.d.aktifRenk, 'y');
  assert.equal(siradaki(rj.d), 'b');
  assert.deepEqual(gor(rj.d, 'b').oynanabilir, []);
  assert.equal(gor(rj.d, 'c').ust.renk, null);
});

sina('çekme: yalnız çekilen oynanır / pas; çekmeden pas ve ikinci çekme hata', () => {
  const d = kur({ a: [['k', '1'], ['m', '7']], b: [['s', '1'], ['s', '2']] }, ['k', '5']);
  hata(d, 'a', { t: 'pas' }, /Önce kart çekmelisin/);
  hata(d, 'b', { t: 'cek' }, /Sıra sende değil/);
  const c = usteAl(d, 'k', '9');
  const r = yap(d, 'a', { t: 'cek' }); // elinde oynanabilir kart varken de serbest
  assert.equal(r.d.eller.a.length, 3);
  assert.equal(siradaki(r.d), 'a');
  assert.equal(gor(r.d, 'a').cekilen, c);
  assert.equal(gor(r.d, 'a').cektiBuTur, true);
  assert.deepEqual(gor(r.d, 'a').oynanabilir, [c]);
  assert.equal(gor(r.d, 'b').cekilen, undefined);
  assert.equal(gor(r.d, null).cekilen, undefined);
  hata(r.d, 'a', { t: 'cek' }, /zaten çektin/);
  hata(r.d, 'a', { t: 'oyna', kart: kid(r.d, 'a', 'k', '1') }, /yalnız çektiğin/);
  assert.equal(siradaki(yap(r.d, 'a', { t: 'oyna', kart: c }).d), 'b');
  const p = yap(r.d, 'a', { t: 'pas' });
  assert.equal(siradaki(p.d), 'b');
  assert.equal(p.d.cektiBuTur, false);
  assert.deepEqual(p.olaylar.map((o) => o.t), ['pas', 'sira']);
  // çekilen oynanamıyorsa yalnız pas
  const c2 = usteAl(d, 'y', '8');
  const r2 = yap(d, 'a', { t: 'cek' });
  assert.deepEqual(gor(r2.d, 'a').oynanabilir, []);
  hata(r2.d, 'a', { t: 'oyna', kart: c2 }, /oynanamaz/);
  hata(r2.d, 'a', { t: 'oyna', kart: kid(r2.d, 'a', 'k', '1') }, /yalnız çektiğin/);
  yap(r2.d, 'a', { t: 'pas' });
});

sina('deste yenileme: atık (üst hariç) karılır; ikisi de boşsa 0 kart ve oyun sürer', () => {
  const d = kur({ a: [['k', '1'], ['m', '7']], b: [['s', '1'], ['s', '2']] }, ['k', '5']);
  // desteyi atığın altına taşı (aralarında joker/+4 de var)
  const ust = d.atik.pop()!;
  d.atik = [...d.deste, ust];
  d.deste = [];
  const altAdet = d.atik.length - 1;
  const r = yap(d, 'a', { t: 'cek' }, tohumlu(7));
  assert(r.olaylar[0].t === 'karildi');
  assert.equal(r.d.atik.length, 1);
  assert.equal(r.d.atik[0].id, ust.id);
  assert.equal(r.d.deste.length, altAdet - 1);
  assert(r.d.deste.filter((k) => k.deger === 'joker' || k.deger === '+4').every((k) => k.renk === null));
  assert.notDeepEqual(r.d.deste.map((k) => k.id), d.atik.slice(0, altAdet - 1).map((k) => k.id), 'karıldı');
  korunum(r.d);
  // ikisi de boş: kartların hepsi ellerde
  const b = kur({ a: [['k', '1']], b: [['s', '1']], c: [['y', '3'], ['y', '4']] }, ['m', '5']);
  b.eller.c.push(...b.deste);
  b.deste = [];
  b.eller.c = b.eller.c.filter((k) => k.renk !== null || (b.eller.a.push(k), false)); // jokerleri a'ya ver (c'de kalmasın)
  b.eller.a = b.eller.a.filter((k) => k.renk !== null || (b.eller.b.push(k), false)); // sonra b'ye: a oynayamaz olsun
  korunum(b);
  const rb = yap(b, 'a', { t: 'cek' });
  assert.deepEqual(rb.olaylar, [{ t: 'cekti', o: 'a', adet: 0, neden: 'cek' }]);
  assert.equal(gor(rb.d, 'a').cekilen, undefined);
  assert.deepEqual(gor(rb.d, 'a').oynanabilir, []);
  assert.equal(siradaki(yap(rb.d, 'a', { t: 'pas' }).d), 'b');
  // +4 hedefi çekebildiği kadar çeker: atıkta yalnız eski üst kart var → karılır, 4 yerine 1 kart
  const r4 = yap(yap(rb.d, 'a', { t: 'pas' }).d, 'b', { t: 'oyna', kart: kid(b, 'b', null, '+4'), renk: 'k' });
  assert.equal(r4.olaylar.find((o) => o.t === 'cekti')?.adet, 1);
  assert(r4.olaylar.some((o) => o.t === 'karildi'));
  assert.equal(r4.d.deste.length + r4.d.atik.length, 1);
  assert.equal(siradaki(r4.d), 'a');
  korunum(r4.d);
});

sina('UNO: deme, unutma, kendisi kapatma, yakalama, pencerenin kapanması', () => {
  const el: Record<string, Tanim[]> = { a: [['k', '1'], ['k', '2']], b: [['s', '1'], ['s', '2'], ['k', '9']], c: [['y', '1'], ['y', '2']] };
  const d = kur(el, ['k', '5']);
  const k1 = kid(d, 'a', 'k', '1');
  // dedi
  const dedi = yap(d, 'a', { t: 'oyna', kart: k1, uno: true });
  assert.deepEqual(dedi.d.unoDedi, ['a']);
  assert.deepEqual(dedi.d.yakalanabilir, []);
  assert(dedi.olaylar.some((o) => o.t === 'uno' && o.o === 'a'));
  assert.equal(gor(dedi.d, 'c').oyuncular[0].unoDedi, true);
  hata(dedi.d, 'b', { t: 'yakala', hedef: 'a' }, /Yakalanacak kimse yok/);
  hata(dedi.d, 'a', { t: 'uno' }, /UNO diyecek durumda değilsin/);
  // demedi
  const demedi = yap(d, 'a', { t: 'oyna', kart: k1 });
  assert.deepEqual(demedi.d.yakalanabilir, ['a']);
  assert.deepEqual(gor(demedi.d, null).yakalanabilir, ['a']);
  assert.equal(gor(demedi.d, 'b').oyuncular[0].unoDedi, false);
  hata(demedi.d, 'a', { t: 'yakala', hedef: 'a' }, /Kendini yakalayamazsın/);
  hata(demedi.d, 'b', { t: 'yakala', hedef: 'c' }, /Yakalanacak kimse yok/);
  hata(demedi.d, 'b', { t: 'yakala', hedef: 'yok' });
  hata(demedi.d, 'b', { t: 'yakala' });
  // (a) kendisi kapatır (sıra onda değilken)
  const kapatti = yap(demedi.d, 'a', { t: 'uno' });
  assert.deepEqual(kapatti.d.yakalanabilir, []);
  assert.deepEqual(kapatti.d.unoDedi, ['a']);
  hata(kapatti.d, 'c', { t: 'yakala', hedef: 'a' }, /Yakalanacak kimse yok/);
  // (b) sırası olmayan c yakalar: 2 kart + ceza, sıra değişmez
  const y = yap(demedi.d, 'c', { t: 'yakala', hedef: 'a' });
  assert.equal(y.d.eller.a.length, 3);
  assert.deepEqual(y.d.cezalar.a, [{ tur: 'uno', puan: 0, aciklama: 'UNO demedi' }]);
  assert.deepEqual(y.d.yakalanabilir, []);
  assert.equal(siradaki(y.d), 'b');
  assert.deepEqual(y.olaylar[0], { t: 'yakalandi', o: 'a', yakalayan: 'c' });
  assert.deepEqual(y.olaylar[1], { t: 'cekti', o: 'a', adet: 2, neden: 'yakalandi' });
  assert.equal(y.olaylar[2].kime, 'a');
  hata(y.d, 'b', { t: 'yakala', hedef: 'a' }, /Yakalanacak kimse yok/);
  korunum(y.d);
  // pencere: sıradaki oyuncu çekince ya da oynayınca kapanır
  hata(yap(demedi.d, 'b', { t: 'cek' }).d, 'c', { t: 'yakala', hedef: 'a' }, /Yakalanacak kimse yok/);
  const oynadi = yap(demedi.d, 'b', { t: 'oyna', kart: kid(d, 'b', 'k', '9') });
  hata(oynadi.d, 'c', { t: 'yakala', hedef: 'a' }, /Yakalanacak kimse yok/);
  hata(oynadi.d, 'a', { t: 'uno' });
  // kart sayısı 1'den farklı olunca unoDedi sıfırlanır (+2 yiyince)
  const s = kur({ a: [['k', '1'], ['k', '2']], b: [['k', '+2'], ['s', '2'], ['s', '3']] }, ['k', '5']);
  const s1 = yap(s, 'a', { t: 'oyna', kart: kid(s, 'a', 'k', '1'), uno: true });
  const s2 = yap(s1.d, 'b', { t: 'oyna', kart: kid(s, 'b', 'k', '+2') });
  assert.equal(s2.d.eller.a.length, 3);
  assert.deepEqual(s2.d.unoDedi, []);
  // 3 karttan 2'ye düşerken uno:true sorun değil, anlamı yok
  const u = kur({ a: [['k', '1'], ['k', '2'], ['k', '3']], b: [['s', '1'], ['s', '2']] }, ['k', '5']);
  const u1 = yap(u, 'a', { t: 'oyna', kart: kid(u, 'a', 'k', '1'), uno: true });
  assert.deepEqual(u1.d.unoDedi, []);
  assert(!u1.olaylar.some((o) => o.t === 'uno'));
});

sina('el sonu: son kart +2 ile bitiş, puan tablosu, bittikten sonra hamle hata', () => {
  const d = kur({ a: [['k', '+2']], b: [['s', '7'], ['s', 'pas'], [null, 'joker']], c: [['y', '0'], ['m', 'yon'], [null, '+4'], ['y', '9']] }, ['k', '5']);
  d.unoDedi = ['a'];
  const c1 = usteAl(d, 'm', '4');
  const c2 = usteAl(d, 'y', '+2'); // üstte: önce bu çekilir
  assert.equal(unoMotor.sonuc(d), null);
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', '+2') });
  assert.deepEqual(r.d.eller.b.map((k) => k.id).slice(-2), [c2, c1]);
  assert.equal(r.olaylar[r.olaylar.length - 1].t, 'elBitti');
  assert(!r.olaylar.some((o) => o.t === 'sira'));
  const s = unoMotor.sonuc(r.d)!;
  assert.equal(s.neden, 'bitti');
  assert.deepEqual(s.kazananlar, ['a']);
  const bPuan = 7 + 20 + 50 + 4 + 20; // çekilen 2 kart dahil
  const cPuan = 0 + 20 + 50 + 9;
  assert.deepEqual(s.satirlar.map((x) => [x.id, x.puan, x.kalan, x.kazandi]), [['a', bPuan + cPuan, 0, true], ['b', -bPuan, 5, false], ['c', -cPuan, 4, false]]);
  assert.equal(s.satirlar[1].aciklama, `5 kart (−${bPuan})`);
  assert.equal(gor(r.d, 'b').bitti, true);
  assert.deepEqual(gor(r.d, 'b').oynanabilir, []);
  hata(r.d, 'b', { t: 'cek' }, /El bitti/);
  assert.equal(unoMotor.botHamle(r.d, 'b', rng0), null);
  korunum(r.d);
  // değerler
  const v = (renk: UnoRenk | null, deger: UnoDeger) => kartDegeri({ id: 0, renk, deger });
  assert.deepEqual([v('k', '0'), v('k', '9'), v('s', 'pas'), v('y', 'yon'), v('m', '+2'), v(null, 'joker'), v(null, '+4')], [0, 9, 20, 20, 20, 50, 50]);
  // yalnız '0' kalan kaybeden: puan 0 (−0 değil); cezalı satır
  const z = kur({ a: [['k', '1']], b: [['s', '0']] }, ['k', '5'], { cezalar: { a: [], b: [{ tur: 'uno', puan: 0, aciklama: 'UNO demedi' }] } });
  const zs = unoMotor.sonuc(yap(z, 'a', { t: 'oyna', kart: kid(z, 'a', 'k', '1') }).d)!;
  assert(Object.is(zs.satirlar[1].puan, 0) && Object.is(zs.satirlar[0].puan, 0));
  assert.equal(zs.satirlar[1].cezalar.length, 1);
  assert.match(zs.satirlar[1].aciklama!, /1 UNO cezası/);
});

sina('gizlilik: görünüm ve olaylarda başkasının kartı yok', () => {
  const d = kur({ a: [['k', '+2'], ['k', '1'], ['m', '3']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5']);
  const anahtarlar = ['aktifRenk', 'atikSayisi', 'bitti', 'cektiBuTur', 'deste', 'elNo', 'elim', 'oynanabilir', 'oyuncular', 'sira', 'tur', 'ust', 'yakalanabilir', 'yon'];
  for (const b of ['a', 'b', 'c', null, 'yabanci']) {
    const g = gor(d, b);
    assert.deepEqual(Object.keys(g).sort(), anahtarlar);
    assert.deepEqual(g.elim, b && d.eller[b] ? d.eller[b] : []);
    assert.equal(typeof g.deste, 'number');
    for (const o of g.oyuncular) assert.deepEqual(Object.keys(o).sort(), ['id', 'kartSayisi', 'unoDedi']);
    const gizli = d.oyuncular.filter((x) => x !== b).flatMap((x) => d.eller[x]).concat(d.deste);
    const metin = JSON.stringify(g);
    for (const k of gizli) assert(!metin.includes(JSON.stringify(k)), 'başkasının kartı sızdı');
  }
  const r = yap(d, 'a', { t: 'oyna', kart: kid(d, 'a', 'k', '+2') });
  for (const o of r.olaylar) {
    if (o.t === 'cektim') { assert.equal(o.kime, 'b'); assert.equal((o.kartlar as UnoKart[]).length, 2); }
    else { assert.equal(o.kime, undefined); assert.equal(o.kartlar, undefined); }
  }
  assert.deepEqual(r.olaylar.map((o) => o.t), ['oynadi', 'cekti', 'cektim', 'sira']);
  // görünümü değiştirmek durumu etkilemez
  const g = gor(d, 'a');
  g.elim[0].deger = '9'; g.ust.deger = '9'; g.yakalanabilir.push('x');
  assert.deepEqual(gor(d, 'a').ust, d.atik[0]);
  assert.notEqual(d.eller.a[0].deger, '9');
});

sina('uygula girdi durumunu değiştirmez (geçerli ve geçersiz hamlede)', () => {
  const d = kur({ a: [['k', '+2'], ['k', '1'], [null, '+4']], b: [['s', '1']], c: [['y', '1'], ['y', '2']] }, ['k', '5'], { yakalanabilir: ['b'] });
  const once = JSON.stringify(d);
  const hamleler: unknown[] = [{ t: 'oyna', kart: kid(d, 'a', 'k', '+2') }, { t: 'oyna', kart: kid(d, 'a', null, '+4'), renk: 'm' }, { t: 'cek' }, { t: 'pas' }, { t: 'uno' }, { t: 'yakala', hedef: 'b' }, { t: 'oyna', kart: 999 }];
  for (const o of ['a', 'b', 'c']) for (const h of hamleler) { unoMotor.uygula(d, o, h, rng0); assert.equal(JSON.stringify(d), once); }
});

sina('bot ve asistan: öncelikler, joker rengi, UNO, yakalama belirlenimci', () => {
  const bot = (d: UnoDurum, o: string) => unoMotor.botHamle(d, o, rng0) as UnoHamle | null;
  // sayı kartı: en çok renkten (aktif renk k; elde m çok ama uymuyor → k'dan en yüksek sayı), jokerler saklanır
  const d = kur({ a: [['k', '3'], ['k', '8'], ['k', 'pas'], [null, 'joker'], ['m', '1'], ['m', '2'], ['m', '4'], ['m', '6']], b: [['s', '1'], ['s', '2'], ['s', '3']] }, ['k', '5']);
  assert.deepEqual(bot(d, 'a'), { t: 'oyna', kart: kid(d, 'a', 'k', '8') });
  assert.equal(bot(d, 'b'), null);
  assert.deepEqual(oneri(gor(d, 'a'), 'a')?.hamle, bot(d, 'a'));
  assert.equal(oneri(gor(d, 'b'), 'b'), null);
  // değer eşleşmesiyle çok renkten oynar: üst k5, elde m5 (m çok) → m5
  const d5 = kur({ a: [['k', '9'], ['m', '5'], ['m', '2'], ['m', '4']], b: [['s', '1'], ['s', '2'], ['s', '3']] }, ['k', '5']);
  assert.deepEqual(bot(d5, 'a'), { t: 'oyna', kart: kid(d5, 'a', 'm', '5') });
  // rakip 1–2 kartta: +2 > +4 > pas
  const t = kur({ a: [['k', '8'], ['k', 'pas'], ['k', '+2'], [null, '+4'], ['m', '1']], b: [['s', '1'], ['s', '2']] }, ['k', '5']);
  assert.deepEqual(bot(t, 'a'), { t: 'oyna', kart: kid(t, 'a', 'k', '+2') });
  t.eller.a = t.eller.a.filter((k) => k.deger !== '+2');
  assert.deepEqual(bot(t, 'a'), { t: 'oyna', kart: kid(t, 'a', null, '+4'), renk: 'k' });
  t.eller.a = t.eller.a.filter((k) => k.deger !== '+4');
  assert.deepEqual(bot(t, 'a'), { t: 'oyna', kart: kid(t, 'a', 'k', 'pas') });
  // yalnız joker uyuyor: en çok olan renk; 2 karttan 1'e düşerken uno:true
  const j = kur({ a: [[null, 'joker'], ['y', '1'], ['y', '2'], ['s', '3']], b: [['s', '1'], ['s', '2'], ['s', '4']] }, ['k', '5']);
  assert.deepEqual(bot(j, 'a'), { t: 'oyna', kart: kid(j, 'a', null, 'joker'), renk: 'y' });
  const j2 = kur({ a: [[null, 'joker'], ['y', '1']], b: [['s', '1'], ['s', '2'], ['s', '4']] }, ['k', '5']);
  assert.deepEqual(bot(j2, 'a'), { t: 'oyna', kart: kid(j2, 'a', null, 'joker'), renk: 'y', uno: true });
  assert.match(oneri(gor(j2, 'a'), 'a')!.aciklama, /UNO/);
  // oynanabilir yok → çek; çekilen uymuyorsa pas, uyuyorsa onu oynar
  const c = kur({ a: [['m', '1'], ['m', '2'], ['m', '3']], b: [['s', '1'], ['s', '2'], ['s', '4']] }, ['k', '5']);
  assert.deepEqual(bot(c, 'a'), { t: 'cek' });
  usteAl(c, 'y', '8');
  assert.deepEqual(bot(yap(c, 'a', { t: 'cek' }).d, 'a'), { t: 'pas' });
  const ck = usteAl(c, 'k', '8');
  assert.deepEqual(bot(yap(c, 'a', { t: 'cek' }).d, 'a'), { t: 'oyna', kart: ck });
  // yakalama: belirlenimci, ≈ yarı yarıya; devralınan el kendisi için UNO der
  const y = kur({ a: [['k', '1']], b: [['s', '1'], ['s', '2']], c: [['y', '1'], ['y', '2']] }, ['k', '5'], { kim: 1, yakalanabilir: ['a'] });
  assert.deepEqual(bot(y, 'a'), { t: 'uno' });
  assert.deepEqual(oneri(gor(y, 'a'), 'a')?.hamle, { t: 'uno' });
  assert.deepEqual(oneri(gor(y, 'c'), 'c')?.hamle, { t: 'yakala', hedef: 'a' });
  let yakalayan = 0;
  for (let i = 0; i < 400; i++) {
    const yi = { ...y, oyuncular: ['a', 'b', `bot${i}`], eller: { ...y.eller, [`bot${i}`]: y.eller.c }, cezalar: { ...y.cezalar, [`bot${i}`]: [] } };
    const h = bot(yi, `bot${i}`);
    assert.deepEqual(h, bot(yi, `bot${i}`), 'aynı durumda aynı karar');
    if (h) { assert.deepEqual(h, { t: 'yakala', hedef: 'a' }); yap(yi, `bot${i}`, h); yakalayan++; }
  }
  assert(yakalayan > 150 && yakalayan < 250, `yakalama oranı ${yakalayan}/400`);
});

sina('elSirala ve adlar', () => {
  const el: UnoKart[] = [
    { id: 1, renk: null, deger: '+4' }, { id: 2, renk: 'm', deger: '3' }, { id: 3, renk: null, deger: 'joker' }, { id: 4, renk: 'k', deger: '+2' },
    { id: 5, renk: 'k', deger: '0' }, { id: 6, renk: 's', deger: 'pas' }, { id: 7, renk: 'y', deger: '9' }, { id: 8, renk: 'k', deger: '7' }, { id: 9, renk: 'k', deger: 'yon' },
  ];
  const once = JSON.stringify(el);
  assert.deepEqual(elSirala(el), [5, 8, 9, 4, 6, 7, 2, 3, 1]);
  assert.equal(JSON.stringify(el), once);
  assert.equal(Object.keys(UNO_DEGER_AD).length, 15);
  assert(Object.values(UNO_DEGER_AD).every((a) => a.length > 0));
});

/* ------------------------------------------------------------------ rastgele oyun ------------------------------------------------------------------ */

console.log('Rastgele oyun (hepsi bot)');
const EL_ADET = 300;
for (let n = 2; n <= 8; n++) {
  const rng = tohumlu(4242 + n);
  const oyuncular = Array.from({ length: n }, (_, i) => ({ id: `b${i}` }));
  let hamle = 0, enUzun = 0, karilma = 0, yakalama = 0, unoKapat = 0;
  for (let e = 0; e < EL_ADET; e++) {
    let d = unoMotor.elBaslat({ oyuncular, elNo: e + 1, baslayan: e % n, rng }) as UnoDurum;
    korunum(d);
    let adim = 0;
    while (!unoMotor.sonuc(d)) {
      assert(++adim <= 5000, `el sonlanmadı (n=${n}, el=${e})`);
      // Rastgele bir bottan başlayarak yapacak işi olanı bul
      const ilk = Math.floor(rng() * n);
      let o = '', h: UnoHamle | null = null;
      for (let i = 0; i < n && !h; i++) { o = oyuncular[(ilk + i) % n].id; h = unoMotor.botHamle(d, o, rng) as UnoHamle | null; }
      assert(h, `hiçbir botun hamlesi yok (n=${n}, el=${e})`);
      if (h.t === 'oyna') {
        if (d.eller[o].length === 2) assert.equal(h.uno, true, 'bot 2→1 düşerken UNO der');
        if (rng() < 0.3) h = { ...h, uno: false }; // unutkan insan benzetimi: yakalama yolları da koşsun
      }
      if (h.t === 'yakala') yakalama++;
      if (h.t === 'uno') unoKapat++;
      const once = adim % 37 === 0 ? JSON.stringify(d) : null;
      const r = unoMotor.uygula(d, o, h, rng);
      assert(!('hata' in r), `bot hatalı hamle: ${JSON.stringify(h)} → ${'hata' in r ? r.hata : ''}`);
      if (once) assert.equal(JSON.stringify(d), once);
      for (const ol of r.olaylar) {
        if (ol.t === 'karildi') karilma++;
        if (ol.kartlar !== undefined) assert(ol.t === 'cektim' && typeof ol.kime === 'string');
      }
      d = r.durum as UnoDurum;
      korunum(d);
      for (const id of d.unoDedi.concat(d.yakalanabilir)) assert.equal(d.eller[id].length, 1);
      const g = gor(d, siradaki(d));
      assert(g.oynanabilir.every((id) => g.elim.some((k) => k.id === id)));
    }
    hamle += adim; enUzun = Math.max(enUzun, adim);
    const s = unoMotor.sonuc(d)!;
    assert.equal(s.neden, 'bitti');
    assert.equal(s.kazananlar.length, 1);
    const kazanan = s.satirlar.find((x) => x.kazandi)!;
    const kaybeden = s.satirlar.filter((x) => !x.kazandi);
    assert.equal(kazanan.id, s.kazananlar[0]);
    assert.equal(kazanan.kalan, 0);
    assert.equal(kaybeden.length, n - 1);
    assert.equal(kazanan.puan + kaybeden.reduce((t, x) => t + x.puan, 0), 0, 'kazanan puanı = kaybedenlerin toplamı');
    for (const x of kaybeden) {
      assert.equal(x.kalan, d.eller[x.id].length);
      assert(x.kalan > 0 && x.puan <= 0);
      assert.equal(0 - x.puan, d.eller[x.id].reduce((t, k) => t + kartDegeri(k), 0));
    }
    assert.equal(s.satirlar.reduce((t, x) => t + x.puan, 0), 0);
  }
  console.log(`  ✓ ${n} oyuncu: ${EL_ADET} el, ${hamle} hamle (ort. ${(hamle / EL_ADET).toFixed(0)}, en uzun ${enUzun}), ${karilma} karma, ${yakalama} yakalama, ${unoKapat} geç UNO`);
}

/* ------------------------------------------------------------------ bulanık ------------------------------------------------------------------ */

console.log('Bulanık');
{
  const rng = tohumlu(99);
  const sec = <T>(a: readonly T[]): T => a[Math.floor(rng() * a.length)];
  const cop: unknown[] = [null, undefined, 0, -1, 1.5, NaN, Infinity, '', 'k', 'x', '__proto__', 'constructor', true, [], {}, [1], { t: 'oyna' }, 1e9, '5'];
  const tler: unknown[] = ['oyna', 'cek', 'pas', 'uno', 'yakala', 'ac', 'at', '', null, 7, 'toString'];
  let deneme = 0, gecerli = 0, el = 0;
  for (let tur = 0; tur < 60; tur++) {
    const n = 2 + (tur % 7);
    const ids = Array.from({ length: n }, (_, i) => `p${i}`);
    let d = unoMotor.elBaslat({ oyuncular: ids.map((id) => ({ id })), elNo: 1, baslayan: tur, rng }) as UnoDurum;
    for (let i = 0; i < 1500 && !d.sonuc; i++) {
      const o = sec([...ids, ...ids, ...ids, 'yok', '', '__proto__', 'constructor']);
      let h: unknown;
      const z = rng();
      if (z < 0.1) h = sec(cop);
      else if (z < 0.55) h = { t: sec(tler), kart: rng() < 0.7 ? Math.floor(rng() * 110) : sec(cop), renk: rng() < 0.6 ? sec(['k', 's', 'y', 'm']) : sec(cop), uno: sec([true, false, undefined, 'evet', 1]), hedef: rng() < 0.7 ? sec(ids) : sec(cop) };
      else h = unoMotor.botHamle(d, siradaki(d), rng) ?? { t: 'cek' }; // ilerlesin diye geçerli hamleler de karışır
      const once = i % 53 === 0 ? JSON.stringify(d) : null;
      let r: ReturnType<typeof unoMotor.uygula> | undefined;
      assert.doesNotThrow(() => { r = unoMotor.uygula(d, o as string, h, rng); }, `istisna: ${JSON.stringify(h)}`);
      if (once) assert.equal(JSON.stringify(d), once);
      deneme++;
      assert(r);
      if ('hata' in r) { assert(typeof r.hata === 'string' && r.hata.length > 0); continue; }
      gecerli++;
      d = r.durum as UnoDurum;
      korunum(d);
      assert.doesNotThrow(() => { for (const b of [...ids, null, 'yok']) unoMotor.gorunum(d, b); unoMotor.sonuc(d); });
    }
    if (d.sonuc) el++;
  }
  // bozuk durum / bozuk rng de istisna fırlatmaz
  const d = unoMotor.elBaslat({ oyuncular: [{ id: 'a' }, { id: 'b' }], elNo: 1, baslayan: 0, rng }) as UnoDurum;
  for (const bozuk of [null, undefined, 5, 'x', {}, { tur: 'uno' }, { ...d, eller: {} }, { ...d, atik: [] }, { ...d, deste: null }]) {
    for (const h of [{ t: 'cek' }, { t: 'oyna', kart: 1, renk: 'k' }, { t: 'yakala', hedef: 'b' }, { t: 'uno' }, { t: 'pas' }]) {
      assert.doesNotThrow(() => unoMotor.uygula(bozuk, 'a', h, rng));
    }
  }
  for (const r of [() => 1, () => NaN, () => -1, () => Infinity]) {
    const x = unoMotor.uygula({ ...d, atik: [...d.deste, ...d.atik], deste: [] }, d.oyuncular[d.kim], { t: 'cek' }, r);
    assert(!('hata' in x));
    korunum(x.durum as UnoDurum);
  }
  console.log(`  ✓ ${deneme} hamle denemesi (${gecerli} geçerli, ${deneme - gecerli} reddedildi), ${el}/60 el sonlandı, istisna yok`);
}

console.log(`\nTAMAM: ${adet} birim sınaması + rastgele oyun (2–8 oyuncu × ${EL_ADET} el) + bulanık`);
