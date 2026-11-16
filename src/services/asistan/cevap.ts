/**
 * Tıp Asistanı — cevap derleme (F3). Üretim YOK: cevaplar `asistan_belge` kaynaklarından alıntılanır, her madde kaynak taşır.
 * Akış: anla() → bge-m3 sorgu vektörü → asistan_ara() (vektör + IDF tam metin + başlık) → niyete göre alıntı seçimi.
 */
import fs from 'fs';
import path from 'path';
import { pgPool } from '../pgDb';
import { fold, WORD_EQUIV } from '../queryIntel/core';
import { anla, NIYET_KURALLARI, type Anlama, type Niyet } from './anlama';

const EMBED_URL = process.env.MEDS_EMBED_BGE_URL || process.env.MEDS_EMBED_URL || 'http://127.0.0.1:8094/embed';

export interface Kaynak { id: string; tur: string; baslik: string; url: string; ders: string }
export type Blok =
  | { t: 'metin'; govde: string }
  | { t: 'maddeler'; baslik?: string; ogeler: Array<{ m: string; k: number }> }
  | { t: 'soru'; soru: string; secenekler: Array<{ k: string; m: string }>; dogru: string; aciklama: string; kaynak: number }
  | { t: 'tablo'; baslik: string; h: string[]; r: string[][]; kaynak: number }
  | { t: 'sayfalar'; ogeler: Array<{ baslik: string; alt: string; url: string }> };
export interface Cevap {
  ana: Niyet; ikincil: Niyet[]; guven: 'birebir' | 'yakin' | 'zayif' | 'sohbet';
  varlik: string | null; duzeltilmis: string | null;
  bloklar: Blok[]; kaynaklar: Kaynak[]; oneriler: string[]; ms: number;
}
interface Satir { id: string; tur: string; baslik: string; url: string; ders: string; kurul: number | null; skor: number; metin: string; baslik_f: string; arama: string }

/* ——— metin yardımcıları (scripts/asistan/metin.py ile AYNI olmak zorunda) ——— */
const DUR = new Set(`nedir ne neler nelerdir hangi hangisi hangileri nasil nerede nereye nereden kim kimdir mi mu midir var yok icin ile ve veya
bir bu su o da de ki gibi daha cok en hakkinda ilgili bana goster ver anlat soyle bul git ac gruptan grubundan sinifindan olarak olan olur olursa`.split(/\s+/));
export const foldSade = (s: string) => fold(s).replace(/[^a-z0-9]+/g, ' ').trim();
const kokler = (f: string) => (f.match(/[a-z0-9]+/g) || []).flatMap(w => (w.length > 5 ? [w, w.slice(0, 5)] : [w])).join(' ');
export function sorguHazirla(s: string): [string, string] {
  const f = foldSade(s);
  const kalan = f.split(' ').filter(w => !DUR.has(w)).join(' ') || f;
  return [f, kokler(kalan)];
}

const vecCache = new Map<string, number[]>();
async function embed(t: string): Promise<number[] | null> {
  const hit = vecCache.get(t);
  if (hit) return hit;
  try {
    const r = await fetch(EMBED_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ texts: [t.slice(0, 600)], kind: 'raw' }), signal: AbortSignal.timeout(4000) });
    if (!r.ok) return null;
    const v = (await r.json()).vectors?.[0] as number[] | undefined;
    if (!Array.isArray(v) || v.length !== 1024) return null;
    vecCache.set(t, v);
    if (vecCache.size > 300) vecCache.delete(vecCache.keys().next().value as string);
    return v;
  } catch { return null; }
}

async function embedMany(texts: string[]): Promise<number[][] | null> {
  try {
    const r = await fetch(EMBED_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ texts, kind: 'raw' }), signal: AbortSignal.timeout(6000) });
    if (!r.ok) return null;
    const v = (await r.json()).vectors as number[][] | undefined;
    return Array.isArray(v) ? v : null;
  } catch { return null; }
}
function kosinus(x: number[], y: number[]): number {
  let d = 0, a = 0, b = 0;
  for (let i = 0; i < x.length; i++) { d += x[i] * y[i]; a += x[i] * x[i]; b += y[i] * y[i]; }
  return d / (Math.sqrt(a * b) || 1);
}

const BILGI_TUR = ['hastalik', 'hastalik_karti', 'onem_maddesi', 'onemli', 'bilgi', 'asistan_nokta', 'sozluk', 'terim', 'spot', 'tablo', 'liste', 'kart', 'saglik', 'onem_ozet', 'ders_ozet', 'terim_yardimcisi'];
const TUR: Partial<Record<Niyet, string[]>> = {
  tanim: ['sozluk', 'hastalik', 'terim', 'terim_yardimcisi', 'hastalik_karti', 'bilgi', 'sozluk_kisaltma', 'kisaltma', 'ders_ozet'],
  cikmis_soru: ['cikmis_soru'], ornek_soru: ['ornek_soru', 'cozucu_sorusu', 'onem_ornek_soru', 'mini_soru', 'soru_karti'],
  git: ['sayfa', 'ders', 'deste', 'ders_ozet'], tablo: ['tablo', 'liste'], kisaltma: ['sozluk_kisaltma', 'kisaltma', 'sozluk'],
  goster: ['sayfa', 'ders', 'deste', 'ders_ozet'], ses_cal: ['sayfa', 'ders', 'deste', 'ders_ozet', 'asistan_nokta', 'cozucu_sorusu'],
};

async function ara(sorgu: string, a: Anlama, turler: string[] | null, n = 24): Promise<Satir[]> {
  const v = await embed(sorgu);
  const [f, kk] = sorguHazirla(sorgu);
  const qv = v ? '[' + v.join(',') + ']' : '[' + new Array(1024).fill(0).join(',') + ']';
  const r = await pgPool.query(
    `select a.id, a.tur, a.baslik, a.url, a.ders, a.kurul, a.skor, b.metin, b.baslik_f, b.arama
       from asistan_ara($1::vector, $2, $3, $4, $5::text[], $6::int) a join asistan_belge b using (id)`,
    [qv, f, kk, n, turler, a.filtre.kurul ?? null]);
  return r.rows as Satir[];
}

/** Dar konulu sorguda ("nistatin yan etkileri") niyet sözcükleri vektörü başka konulara çeker: konu sözcükleriyle ikinci geçiş yapılır */
async function araBirlesik(sorgu: string, konuMetni: string, a: Anlama, turler: string[] | null): Promise<Satir[]> {
  const ilk = await ara(sorgu, a, turler);
  if (!konuMetni || konuMetni === foldSade(sorgu)) return ilk;
  const ikinci = await ara(konuMetni, a, turler);
  const gor = new Set(ilk.map(x => x.id));
  return [...ilk, ...ikinci.filter(x => !gor.has(x.id))];
}

/* ——— ilgi denetimi ——— */
const EQ = WORD_EQUIV.map(g => g.map(w => foldSade(w).slice(0, 7)));
/** Bir kök için kabul edilen yazımlar: pyelonefrit≈piyelonefrit, böbrek≈renal… */
function alternatifler(k: string): string[] {
  const l = new Set([k, k.replace(/^py/, 'piy'), k.replace(/^piy/, 'py')]);
  if (k.length >= 4 && /[iıuü]$/.test(k)) l.add(k.slice(0, -1)); // iyelik eki: taşı → taş, böbreği → böbreg
  for (const g of EQ) if (g.includes(k)) g.forEach(x => l.add(x));
  return [...l];
}
const kok5 = (s: string) => foldSade(s).split(' ').filter(w => w.length >= 3 && !DUR.has(w)).map(w => w.slice(0, 7));
/** Niyet sözcüklerini (tedavi, yan etki, çıkmış…) sorgudan çıkarır: geriye konu sözcükleri kalır */
function konuSozcukleri(q: string): string {
  let s = ' ' + foldSade(q) + ' ';
  for (const r of NIYET_KURALLARI) s = s.replace(new RegExp('(?:' + r.re.source + ')\\w*', 'g'), ' ');
  return s.replace(/\s+/g, ' ').trim();
}
interface Konu { stems: string[][]; esik: number; kaynak: 'varlik' | 'konu' }
function konuBul(a: Anlama): Konu {
  const topikal = new Set(kok5(konuSozcukleri(a.duzeltilmis ?? a.soru)));
  // kısaltma sorusunda (ADH açılımı) kavram eşleşmesi çok anlamlı olabilir: yalnız yazılan kısaltmaya bakılır
  const v = a.ana === 'kisaltma' ? undefined : a.varliklar.find(c => kok5(c.matched + ' ' + c.label.replace(/\(.*?\)/g, ' ')).some(x => topikal.has(x)));
  if (v) return { stems: kok5(v.label.replace(/\(.*?\)/g, ' ')).map(alternatifler), esik: 0.6, kaynak: 'varlik' };
  let s = kok5(konuSozcukleri(a.duzeltilmis ?? a.soru)).slice(0, 5).map(alternatifler);
  // büyük harfle yazılmış kısa kısaltma (MS, ADH, KOAH): 2 harfli de olsa konu sayılır
  if (!s.length) s = (a.soru.match(/\b[A-ZÇĞİÖŞÜ]{2,6}\b/g) || []).slice(0, 2).map(x => [foldSade(x)]);
  return { stems: s, esik: s.length <= 2 ? 0.99 : 0.75, kaynak: 'konu' };
}
function ilgi(s: Satir, stems: string[][]): number {
  if (!stems.length) return 1;
  const hay = ' ' + s.baslik_f + ' ' + s.arama.slice(0, 2500) + ' ';
  return stems.filter(alts => alts.some(x => hay.includes(' ' + x))).length / stems.length;
}

/* ——— cümle seçimi ——— */
function cumleler(metin: string): string[] {
  return metin.split(/\n+/).filter(l => !/^(?:[A-E]\) |Doğru: |Kazanım: )/.test(l)).flatMap(l => l.split(/(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9•*\-])/)).map(x => x.replace(/^[-•*]\s+(?=\S)/, '').trim()).filter(x => x.length >= 20 && x.length <= 420);
}
function ipucu(n: Niyet): RegExp[] { return NIYET_KURALLARI.filter(r => r.n === n).map(r => r.re); }

function ozet(metin: string, uz = 260): string {
  const t = metin.replace(/\s+/g, ' ').trim();
  return t.length <= uz ? t : t.slice(0, uz).replace(/\s\S*$/, '') + '…';
}

function soruBlogu(s: Satir, k: number): Blok | null {
  const L = s.metin.split('\n');
  const dogruI = L.findIndex(x => /^Doğru: /.test(x));
  const optI = L.findIndex(x => /^A\) /.test(x));
  if (dogruI < 0 || optI < 0) return null;
  const secenekler = L[optI].split(/; (?=[A-E]\) )/).map(x => ({ k: x.slice(0, 1), m: x.slice(3).trim() }));
  const stem = L.slice(0, optI).join(' ').trim();
  const dg = L[dogruI].replace('Doğru: ', '').trim().slice(0, 1);
  if (secenekler.length < 2 || !stem) return null;
  return { t: 'soru', soru: stem, secenekler, dogru: dg, aciklama: L.slice(dogruI + 1).join(' ').replace(/Kazanım: .*/, '').trim(), kaynak: k };
}

function tabloBlogu(s: Satir, k: number): Blok | null {
  const L = s.metin.split('\n').filter(Boolean);
  if (L.length < 2 || !L[0].includes(' | ')) return null;
  return { t: 'tablo', baslik: s.baslik, h: L[0].split(' | '), r: L.slice(1).map(x => x.split(' | ')), kaynak: k };
}

const SOHBET: Partial<Record<Niyet, string[]>> = {
  selam: ['Merhaba! Hastalık, ilaç, bulgu, çıkmış soru ya da sitede bir sayfa sorabilirsin.', 'Selam! Ne bulmamı istersin: bir konu, bir soru, bir sayfa?'],
  tesekkur: ['Rica ederim! Başka bir şey lazım olursa yaz.', 'Ne demek! Devam edelim mi?'],
  veda: ['Görüşürüz, kolay gelsin!', 'İyi çalışmalar!'],
};
const pick = <T,>(l: T[], s: string): T => l[[...s].reduce((x, c) => x + c.charCodeAt(0), 0) % l.length];

const BASLIK: Partial<Record<Niyet, string>> = {
  tanim: 'Tanım', etiyoloji: 'Nedenler / risk', patogenez: 'Mekanizma ve patoloji', belirti: 'Belirti ve bulgular', tani: 'Tanı', laboratuvar: 'Laboratuvar',
  goruntuleme: 'Görüntüleme', ayirici_tani: 'Ayırıcı tanı', tedavi: 'Tedavi', komplikasyon: 'Komplikasyonlar', prognoz: 'Prognoz / seyir', sayi: 'Sayısal bilgiler',
  ilac_mekanizma: 'Etki mekanizması', endikasyon: 'Endikasyonlar', kontrendikasyon: 'Kontrendikasyonlar', yan_etki: 'Yan etkiler', etkilesim: 'Etkileşimler', doz: 'Doz ve kullanım',
};

function oneriUret(ad: string | null, ana: Niyet): string[] {
  if (!ad) return ['Parkinson hastalığı belirtileri', 'Bana patoloji sorusu getir', 'Sesli soru çözücü nerede'];
  const l = ['tedavisi', 'belirtileri', 'tanısı', 'çıkmış sorular'].filter(x => !(ana === 'tedavi' && x === 'tedavisi') && !(ana === 'belirti' && x === 'belirtileri') && !(ana === 'tani' && x === 'tanısı') && !(ana === 'cikmis_soru' && x === 'çıkmış sorular'));
  return l.slice(0, 3).map(x => `${ad} ${x}`);
}

export async function cevapla(soru: string): Promise<Cevap> {
  const t0 = Date.now();
  const a = anla(soru);
  if (/^\s*[A-ZÇĞİÖŞÜ]{2,6}\s*[?.!]?\s*$/.test(soru)) a.ana = 'kisaltma';
  const kaynaklar: Kaynak[] = [];
  const u = (x: string) => x.replace(/ /g, '%20');
  const kIdx = (s: Satir) => {
    let i = kaynaklar.findIndex(x => x.id === s.id);
    if (i < 0) { kaynaklar.push({ id: s.id, tur: s.tur, baslik: s.baslik, url: u(s.url), ders: s.ders }); i = kaynaklar.length - 1; }
    return i;
  };
  const bit = (c: Partial<Cevap> & Pick<Cevap, 'bloklar' | 'guven'>): Cevap => ({
    ana: a.ana, ikincil: a.ikincil, varlik: null, duzeltilmis: a.duzeltilmis, kaynaklar, oneriler: [], ms: Date.now() - t0, ...c,
  });

  if (SOHBET[a.ana]) return bit({ bloklar: [{ t: 'metin', govde: pick(SOHBET[a.ana]!, soru) }], guven: 'sohbet', oneriler: oneriUret(null, a.ana) });

  const sorgu = a.duzeltilmis ?? soru;
    const konu = konuBul(a);
  const varlikAd = konu.kaynak === 'varlik' ? (a.varliklar.find(c => kok5(c.matched + ' ' + c.label).length && konu.stems.flat().some(x => foldSade(c.label).includes(x)))?.label.replace(/\s*\(.*?\)\s*/g, ' ').trim() ?? null) : null;
  const stems = konu.stems;
  const esik = stems.length ? konu.esik : 0;

  if (a.ana === 'bilinmiyor' || !stems.length && !['site_yardim', 'calisma_onerisi', 'git', 'goster', 'ses_cal', 'tablo', 'cikmis_soru', 'ornek_soru'].includes(a.ana)) {
    return bit({ bloklar: [{ t: 'metin', govde: 'Ne aradığını tam anlayamadım. Bir hastalık, ilaç, bulgu ya da sayfa adı ile birlikte ne öğrenmek istediğini yazar mısın? (ör. "migren tedavisi", "nistatin yan etkileri")' }], guven: 'zayif', oneriler: oneriUret(null, a.ana) });
  }

  const bilgiNiyet = BASLIK[a.ana] !== undefined;
  const turler = TUR[a.ana] ?? (bilgiNiyet ? BILGI_TUR : null);
  const konuMetni = konuSozcukleri(sorgu);
  let satirlar = await araBirlesik(sorgu, konuMetni, a, turler);
  if (a.ana === 'site_yardim' || a.ana === 'calisma_onerisi') satirlar = await ara(sorgu, a, ['sayfa']);

  /* — sayfa / yönlendirme niyetleri — */
  if (['git', 'goster', 'ses_cal', 'site_yardim', 'calisma_onerisi'].includes(a.ana)) {
    const adaylar = satirlar.filter(s => ilgi(s, stems) >= esik).slice(0, 4);
    const ogeler = (adaylar.length ? adaylar : satirlar.slice(0, 3)).map(s => ({ baslik: s.baslik, alt: s.tur === 'sayfa' ? 'Sayfa' : s.ders || s.tur, url: u(s.url) }));
    const not = a.ana === 'goster' ? 'Görsel/çizimi sohbette gösterme henüz bağlı değil; ilgili sayfaları açabilirsin.'
      : a.ana === 'ses_cal' ? 'Sesi sohbetten oynatma henüz bağlı değil; sesli içerik bulunan sayfaları açabilirsin.'
      : a.ana === 'calisma_onerisi' ? 'Kişisel öneri henüz bağlı değil; bunlar işine yarayabilir.' : a.ana === 'site_yardim' ? 'Şu sayfalar işine yarayabilir:' : 'Şuraya gidebilirsin:';
    return bit({ bloklar: [{ t: 'metin', govde: not }, { t: 'sayfalar', ogeler }], guven: ogeler.length ? 'yakin' : 'zayif', varlik: varlikAd, oneriler: oneriUret(varlikAd, a.ana) });
  }

  /* — soru niyetleri — */
  if (a.ana === 'cikmis_soru' || a.ana === 'ornek_soru') {
    const ilgili = satirlar.filter(s => ilgi(s, stems) >= esik);
    const bl: Blok[] = [];
    const gor = new Set<string>();
    for (const s of ilgili) { const b = soruBlogu(s, kIdx(s)); if (b && b.t === 'soru' && !gor.has(foldSade(b.soru))) { gor.add(foldSade(b.soru)); bl.push(b); } if (bl.length >= 3) break; }
    if (!bl.length) return bit({ bloklar: [{ t: 'metin', govde: `${varlikAd ? `**${varlikAd}** için ` : ''}${a.ana === 'cikmis_soru' ? 'çıkmış' : 'örnek'} soru bulamadım.` }], guven: 'zayif', varlik: varlikAd, oneriler: oneriUret(varlikAd, a.ana) });
    return bit({ bloklar: [{ t: 'metin', govde: `${varlikAd ? `**${varlikAd}** ile ilgili ` : ''}${bl.length} ${a.ana === 'cikmis_soru' ? 'çıkmış' : 'örnek'} soru:` }, ...bl], guven: stems.length ? 'birebir' : 'yakin', varlik: varlikAd, oneriler: oneriUret(varlikAd, a.ana) });
  }

  /* — tablo — */
  if (a.ana === 'tablo') {
    const bl: Blok[] = [];
    for (const s of satirlar.filter(x => ilgi(x, stems) >= esik)) { const b = tabloBlogu(s, kIdx(s)); if (b) bl.push(b); if (bl.length >= 2) break; }
    if (bl.length) return bit({ bloklar: bl, guven: 'yakin', varlik: varlikAd, oneriler: oneriUret(varlikAd, a.ana) });
  }

  /* — bilgi niyetleri (ve kısaltma/tablo yedeği): kaynaktan cümle alıntısı — */
  const cue = a.ana === 'kisaltma' || a.ana === 'tablo' ? [] : ipucu(a.ana);
  const odakKok = new Set(stems.flat().length ? kok5(konuSozcukleri(a.duzeltilmis ?? a.soru)) : a.odak.flatMap(kok5));
  const bloklar: Blok[] = [];
  if (turler && !satirlar.some(s => ilgi(s, stems) >= esik)) satirlar = await araBirlesik(sorgu, konuMetni, a, null);
  const ilgiliDoc = satirlar.map(s => ({ s, g: ilgi(s, stems) })).filter(x => x.g >= (stems.length ? esik : 0.5)).slice(0, 8);
  interface Aday { m: string; s: Satir; p: number; cue: boolean }
  const topla = (docs: Array<{ s: Satir; g: number }>): Aday[] => {
    const out: Aday[] = [];
    for (const { s, g } of docs) {
      if (/kisaltma/.test(s.tur) && s.metin) { out.push({ m: `**${s.baslik}**: ${ozet(s.metin, 200)}`, s, p: 20, cue: true }); continue; }
      const ps = cumleler(s.metin).map((c, i) => {
        const fc = ' ' + foldSade(c);
        const cueVar = cue.some(re => re.test(fc));
        const konuVar = stems.length ? stems.some(alts => alts.some(x => fc.includes(' ' + x))) : false;
        const odakOran = odakKok.size ? [...odakKok].filter(x => fc.includes(' ' + x)).length / odakKok.size : 0;
        return { c, cueVar, konuVar, p: (cueVar ? 3 : 0) + (konuVar ? 2 : 0) + odakOran * 2 + g + (i === 0 ? 0.3 : 0) + s.skor * 10 };
      });
      const sec = ps.filter(x => x.cueVar || x.konuVar || !cue.length).sort((x, y) => y.p - x.p).slice(0, 3);
      for (const x of sec) out.push({ m: x.c, s, p: x.p, cue: x.cueVar });
      if (!sec.length && !cue.length && s.metin) out.push({ m: ozet(s.metin), s, p: g, cue: false });
    }
    return out;
  };
  let adaylar = topla(ilgiliDoc.slice(0, 5));
  // ders cümleleri azsa tüm türlerden tamamla (çıkmış soru açıklamaları, başka derslerin geçtiği yerler)
  if (turler && adaylar.filter(x => x.p > 2).length < 3 && stems.length) {
    const genis = await araBirlesik(sorgu, konuMetni, a, null);
    const ek = genis.map(s => ({ s, g: ilgi(s, stems) })).filter(x => x.g >= esik && !ilgiliDoc.some(d => d.s.id === x.s.id)).slice(0, 6);
    adaylar = adaylar.concat(topla(ek));
  }
  // niyet cümlesi yoksa anlamsal yeniden sıralama: ("Parkinson tedavisi" ↔ "levodopa kullanılır" cümlesi "tedavi" demese de yakın)
  if (cue.length && !adaylar.some(x => x.cue) && adaylar.length > 1) {
    const top = adaylar.sort((x, y) => y.p - x.p).slice(0, 14);
    const [qv, vs] = await Promise.all([embed(sorgu), embedMany(top.map(x => x.m.slice(0, 300)))]);
    if (qv && vs && vs.length === top.length) top.forEach((x, i) => { x.p += 8 * kosinus(qv, vs[i]); });
    adaylar = top;
  }
  adaylar.sort((x, y) => y.p - x.p);
  // yakın tekrarlar (aynı bilginin farklı kaynaktaki hali) tek cümleye iner
  const belirteç = (m: string) => new Set(foldSade(m).split(' ').filter(w => w.length > 3));
  const secilen: Array<{ m: string; k: number; cue: boolean }> = [];
  const alinanlar: Aday[] = [];
  for (const x of adaylar) {
    const bx = belirteç(x.m);
    const benzer = alinanlar.some(y => { const by = belirteç(y.m); const ort = [...bx].filter(w => by.has(w)).length; return ort / Math.max(1, Math.min(bx.size, by.size)) > 0.7; });
    if (benzer) continue;
    alinanlar.push(x); secilen.push({ m: x.m, k: kIdx(x.s), cue: x.cue });
    if (secilen.length >= 4) break;
  }
  const cueBulundu = secilen.some(x => x.cue);

  if (!secilen.length) {
    const genis = await araBirlesik(sorgu, konuMetni, a, null);
    const yakin = genis.filter(s => stems.length && ilgi(s, stems) >= esik);
    const soruB: Blok[] = [];
    for (const s of varlikAd ? [] : yakin.filter(x => /soru/.test(x.tur))) { const b = soruBlogu(s, kIdx(s)); if (b) soruB.push(b); if (soruB.length >= 2) break; }
    const ogeler = yakin.filter(s => !/soru/.test(s.tur)).slice(0, 3).map(s => ({ baslik: s.baslik, alt: s.ders || s.tur, url: u(s.url) }));
    const bos = !ogeler.length && !soruB.length;
    const ad = varlikAd ? `**${varlikAd}** için ` : '';
    return bit({
      bloklar: [{ t: 'metin', govde: bos ? `${ad}kaynaklarda bu soruya karşılık gelen bir şey bulamadım.` : `${ad}"${(BASLIK[a.ana] || (a.ana === 'tablo' ? 'tablo' : 'bu konu')).toLowerCase()}" ile ilgili doğrudan cümle bulamadım; konuyla ilgili kaynaklar:` },
        ...(ogeler.length ? [{ t: 'sayfalar', ogeler } as Blok] : []), ...soruB],
      guven: 'zayif', varlik: varlikAd, oneriler: oneriUret(varlikAd, a.ana) });
  }
  const guven: Cevap['guven'] = stems.length && cueBulundu ? 'birebir' : stems.length || cueBulundu ? 'yakin' : 'zayif';
  bloklar.push({ t: 'maddeler', baslik: `${varlikAd ? varlikAd + ' — ' : ''}${cueBulundu ? BASLIK[a.ana] || 'Kaynakta bulduklarım' : 'Kaynakta bulduklarım'}`, ogeler: secilen.map(x => ({ m: x.m, k: x.k })) });
  if (!cueBulundu && cue.length && a.ana !== 'tanim') bloklar.unshift({ t: 'metin', govde: `"${(BASLIK[a.ana] || '').toLowerCase()}" başlığını doğrudan anlatan bir cümle bulamadım; konuyla ilgili en yakın bilgiler:` });
  return bit({ bloklar, guven, varlik: varlikAd, oneriler: oneriUret(varlikAd, a.ana) });
}

/* ——— cevaplanamayanlar: içerik açığı listesi (yönetici) ——— */
const KLASOR = path.join(process.cwd(), 'data', 'asistan');
/** Tüm sorular `sorular.jsonl`'a (ayarlama için: ne soruldu, ne cevaplandı), güveni zayıf olanlar ayrıca `cevaplanamayan.jsonl`'a yazılır. Kişi bilgisi tutulmaz. */
export function cevapsizKaydet(soru: string, c: Cevap) {
  try {
    fs.mkdirSync(KLASOR, { recursive: true });
    const satir = JSON.stringify({ t: new Date().toISOString(), q: soru.slice(0, 300), ana: c.ana, guven: c.guven, varlik: c.varlik, ms: c.ms, ilk: c.kaynaklar[0]?.baslik?.slice(0, 80) ?? null }) + '\n';
    fs.appendFileSync(path.join(KLASOR, 'sorular.jsonl'), satir);
    if (c.guven === 'zayif') fs.appendFileSync(path.join(KLASOR, 'cevaplanamayan.jsonl'), satir);
  } catch { /* günlük zorunlu değil */ }
}
