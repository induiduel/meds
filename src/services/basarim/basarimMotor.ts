/**
 * Başarım motoru (sunucu) — puan + ATP (2026-10-20).
 *
 * Kurallar tek dosyadan: `src/data/basarim/tanim.json` (varsa `data/basarim/tanim.json` üst katmanı; yönetici ucuyla
 * güncellenir). Kayıtlar `data/basarim/k/<sha(uid)>.json` (kişi başına), ödemeler `data/basarim/odemeler.json`.
 *
 * - Puan yalnız sıralamaya etki eder; ATP biriktirilip kilit açmada harcanır (başlangıç 100 mol).
 * - ATP yalnız sıralama (ilk 5) ve hedef/başarım üst seviyelerinden gelir; topluluk eylemleri (soru ekleme, yorum,
 *   beğeni, katkı, hata bildirimi) ve topluluk başarımları yalnız puan verir.
 * - Günlük ATP tavanı (100): fazlası kuyruğa girer, sonraki günlerin boş payıyla hesaba geçer.
 * - Ölçüler: çalışma süresi (profil yedeği stats.studySeconds), çözülen soru (kv medsoru_basarim_sayac_v1),
 *   gerçekten bitirilen konu (kv medsoru_calisma_takip_v1: "bitti" + asgari etkin süre), giriş/oturum (sunucu kaydı),
 *   topluluk eylemleri (sunucu ara katmanı, yalnız doğrulanmış Firebase kimliği).
 * Her ödül kalıcı kimlikle bir kez verilir (ör. `h:g_calisma:2026-10-20:3`), yeniden değerlendirme çift ödül üretmez.
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import varsayilanTanim from '../../data/basarim/tanim.json';
import takvim from '../../data/kurul_takvimi_ozet.json';

// ───────────────────────── Tanım ─────────────────────────
export type Seviye = [number, number, number]; // [eşik, puan, atp]
export interface HedefTanim { id: string; donem: 'gun' | 'hafta' | 'kurul'; ad: string; olcu: string; ikon?: string; seviyeler: Seviye[] }
export interface BasarimTanim { id: string; ad: string; aciklama?: string; olcu: string; ikon?: string; renk?: string; topluluk?: boolean; seviyeler: Seviye[] }
export interface KilitTanim { id: string; tur: 'unvan' | 'cerceve' | 'efekt' | 'icerik'; ad: string; fiyat: number; etkin: boolean; renk?: string }
export interface EylemTanim { id: string; ad: string; p: number; gunlukTavan: number }
export interface Tanim {
  surum: number;
  atp: { baslangic: number; gunlukTavan: number; haftalikSiralama: number[]; kurulSiralama: number[]; siralamaEsikPuan: { hafta: number; kurul: number } };
  taban: { soruBasina: number; soruGunlukTavan: number; onDakikaBasina: number; calismaGunlukTavanSn: number; bitirilenBasina: number; bitirilenGunlukTavan: number; bitirmeAsgariSn: number };
  eylemler: EylemTanim[];
  hedefler: HedefTanim[];
  basarimlar: BasarimTanim[];
  kilitler: KilitTanim[];
}

/** Tanım doğrulaması: hata listesi (boşsa geçerli). Topluluk başarımı ATP veremez, kilit fiyatı 50–1000. */
export function tanimDogrula(t: any): string[] {
  const h: string[] = [];
  if (!t || typeof t !== 'object') return ['Tanım nesne değil.'];
  const ids = new Set<string>();
  const sev = (where: string, s: any) => {
    if (!Array.isArray(s) || !s.length) return h.push(`${where}: seviye yok`);
    let son = -1;
    s.forEach((x: any, i: number) => {
      if (!Array.isArray(x) || x.length !== 3 || x.some((n: any) => typeof n !== 'number' || n < 0)) h.push(`${where} seviye ${i + 1}: [eşik, puan, atp] sayı olmalı`);
      else {
        if (x[0] <= son) h.push(`${where} seviye ${i + 1}: eşik artan olmalı`);
        if (x[1] === 0 && x[2] === 0) h.push(`${where} seviye ${i + 1}: ödülsüz`);
        son = x[0];
      }
    });
  };
  for (const x of t.hedefler || []) {
    if (!x.id || ids.has(x.id)) h.push(`hedef kimliği boş/yinelenmiş: ${x.id}`); ids.add(x.id);
    if (!['gun', 'hafta', 'kurul'].includes(x.donem)) h.push(`${x.id}: dönem gun|hafta|kurul`);
    sev(x.id, x.seviyeler);
  }
  for (const x of t.basarimlar || []) {
    if (!x.id || ids.has(x.id)) h.push(`başarım kimliği boş/yinelenmiş: ${x.id}`); ids.add(x.id);
    sev(x.id, x.seviyeler);
    if (x.topluluk && (x.seviyeler || []).some((s: any) => s?.[2] > 0)) h.push(`${x.id}: topluluk başarımı ATP veremez`);
  }
  for (const k of t.kilitler || []) {
    if (!k.id || ids.has(k.id)) h.push(`kilit kimliği boş/yinelenmiş: ${k.id}`); ids.add(k.id);
    if (!(k.fiyat >= 50 && k.fiyat <= 1000)) h.push(`${k.id}: fiyat 50–1000 mol olmalı`);
  }
  if (!(t.atp?.gunlukTavan > 0 && t.atp.gunlukTavan <= 100)) h.push('atp.gunlukTavan 1–100 olmalı');
  return h;
}

// ───────────────────────── Zaman ─────────────────────────
const gunBicim = new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Istanbul', year: 'numeric', month: '2-digit', day: '2-digit' });
export const gunOf = (d: Date | number = new Date()) => gunBicim.format(typeof d === 'number' ? new Date(d) : d);
const gunEkle = (g: string, n: number) => new Date(Date.parse(`${g}T12:00:00Z`) + n * 86400000).toISOString().slice(0, 10);
/** Haftanın pazartesisi. */
export const haftaOf = (g: string) => {
  const gd = new Date(`${g}T12:00:00Z`).getUTCDay(); // 0 pazar
  return gunEkle(g, -((gd + 6) % 7));
};
export interface Pencere { id: string; bas: string; son: string; ad: string }
const KURULLAR: { kurul: number; ad: string; baslangic: string; sinav: string }[] = (takvim as any).kurullar || [];
/** Kurul penceresi: Dönem 3 için takvimdeki kurul (ara tatil sonraki kurula yazılır); takvimi olmayan dönemde takvim ayı. */
export function kurulPencere(donem: number, g: string): Pencere {
  if (donem === Number((takvim as any).donem || 3) && KURULLAR.length) {
    for (let i = 0; i < KURULLAR.length; i++) {
      const k = KURULLAR[i];
      if (g <= k.sinav) {
        const bas = i === 0 ? k.baslangic : gunEkle(KURULLAR[i - 1].sinav, 1);
        return { id: `d${donem}-k${k.kurul}`, bas, son: k.sinav, ad: `${k.kurul}. Kurul` };
      }
    }
    const s = KURULLAR[KURULLAR.length - 1];
    const fin = String((takvim as any).butunleme || (takvim as any).final || gunEkle(s.sinav, 60));
    return { id: `d${donem}-final`, bas: gunEkle(s.sinav, 1), son: fin, ad: 'Final dönemi' };
  }
  const ay = g.slice(0, 7);
  const sonGun = new Date(Date.UTC(+ay.slice(0, 4), +ay.slice(5, 7), 0)).toISOString().slice(0, 10);
  return { id: `d${donem}-ay-${ay}`, bas: `${ay}-01`, son: sonGun, ad: 'Bu ay' };
}
const pencereGunleri = (bas: string, son: string) => { const r: string[] = []; for (let g = bas; g <= son && r.length < 400; g = gunEkle(g, 1)) r.push(g); return r; };

// ───────────────────────── Kayıt ─────────────────────────
export interface DefterKaydi { id: string; t: 'baslangic' | 'hedef' | 'basarim' | 'siralama' | 'harcama'; ad: string; p: number; a: number; at: string; g: string; ust?: boolean; ref?: string }
export interface Kisi {
  uid: string; ad: string; donem: number | null; kurul: number | null; profilAt?: string;
  defter: DefterKaydi[];
  atp: { bakiye: number; kuyruk: { id: string; a: number; ad: string; at: string }[]; gun: Record<string, number> };
  eylem: { gun: Record<string, Record<string, number>>; toplam: Record<string, number>; begeni: string[] };
  giris: { gun: Record<string, number>; son: number };
  /** gün → ölçü (soru, sn, bitir); yedekteki günler budansa da toplamlar korunur (en büyük tutulur) */
  metrik: Record<string, { sn: number; soru: number; bitir: number }>;
  gunPuan: Record<string, number>;
  kilit: Record<string, string>;
  secili: { unvan?: string; cerceve?: string; efekt?: string };
  goruldu: string;
  degerAt?: string;
}

export interface MotorDeps { dataDir: string; srcDir: string; okuYedek: (uid: string) => any | null }

export function createBasarimMotor(deps: MotorDeps) {
  const kok = path.join(deps.dataDir, 'basarim');
  const kisiDir = path.join(kok, 'k');
  fs.mkdirSync(kisiDir, { recursive: true });
  const ustTanimDosya = path.join(kok, 'tanim.json');
  const odemeDosya = path.join(kok, 'odemeler.json');

  let tanim: Tanim = varsayilanTanim as any;
  const tanimYukle = () => {
    try {
      if (fs.existsSync(ustTanimDosya)) {
        const t = JSON.parse(fs.readFileSync(ustTanimDosya, 'utf8'));
        if (!tanimDogrula(t).length) { tanim = t; return; }
        console.warn('[basarim] üst tanım geçersiz, varsayılan kullanılıyor');
      }
    } catch (e: any) { console.warn('[basarim] üst tanım okunamadı:', e?.message); }
    tanim = varsayilanTanim as any;
  };
  tanimYukle();

  const atomik = (f: string, v: unknown) => { const tmp = `${f}.${process.pid}.tmp`; fs.writeFileSync(tmp, JSON.stringify(v)); fs.renameSync(tmp, f); };
  const dosyaOf = (uid: string) => path.join(kisiDir, `${crypto.createHash('sha256').update(`bs:${uid}`).digest('hex').slice(0, 32)}.json`);

  const onbellek = new Map<string, Kisi>();
  let hepsiYuklu = false;
  const hepsiniYukle = () => {
    if (hepsiYuklu) return;
    for (const f of fs.readdirSync(kisiDir)) {
      if (!f.endsWith('.json')) continue;
      try { const k: Kisi = JSON.parse(fs.readFileSync(path.join(kisiDir, f), 'utf8')); if (k?.uid && !onbellek.has(k.uid)) onbellek.set(k.uid, k); } catch { /* bozuk */ }
    }
    hepsiYuklu = true;
  };

  const yeniKisi = (uid: string): Kisi => {
    const at = new Date().toISOString();
    return {
      uid, ad: '', donem: null, kurul: null, defter: [{ id: 'baslangic', t: 'baslangic', ad: 'Hoş geldin ATP’si', p: 0, a: tanim.atp.baslangic, at, g: gunOf() }],
      atp: { bakiye: tanim.atp.baslangic, kuyruk: [], gun: {} }, eylem: { gun: {}, toplam: {}, begeni: [] }, giris: { gun: {}, son: 0 },
      metrik: {}, gunPuan: {}, kilit: {}, secili: {}, goruldu: at,
    };
  };
  const kisi = (uid: string): Kisi => {
    let k = onbellek.get(uid);
    if (!k) {
      const f = dosyaOf(uid);
      try { if (fs.existsSync(f)) k = JSON.parse(fs.readFileSync(f, 'utf8')); } catch { /* bozuk */ }
      if (!k) k = yeniKisi(uid);
      onbellek.set(uid, k);
    }
    return k;
  };
  const kaydet = (k: Kisi) => atomik(dosyaOf(k.uid), k);

  // ───── ATP ─────
  const kuyrukIsle = (k: Kisi) => {
    const g = gunOf();
    let bos = tanim.atp.gunlukTavan - (k.atp.gun[g] || 0);
    while (bos > 0 && k.atp.kuyruk.length) {
      const q = k.atp.kuyruk[0];
      const al = Math.min(bos, q.a);
      k.atp.bakiye += al; k.atp.gun[g] = (k.atp.gun[g] || 0) + al; bos -= al; q.a -= al;
      if (q.a <= 0) k.atp.kuyruk.shift();
    }
    const gunler = Object.keys(k.atp.gun).sort();
    if (gunler.length > 60) for (const x of gunler.slice(0, gunler.length - 60)) delete k.atp.gun[x];
  };
  /** `g`: puanın yazılacağı gün (geçmiş pencerenin hedefi kendi gününe yazılır; sıralama haftası şişmesin). */
  const odul = (k: Kisi, e: Omit<DefterKaydi, 'at' | 'g'>, g = gunOf()): boolean => {
    if (k.defter.some((d) => d.id === e.id)) return false;
    const at = new Date().toISOString();
    k.defter.push({ ...e, at, g });
    if (e.a > 0) k.atp.kuyruk.push({ id: e.id, a: e.a, ad: e.ad, at });
    return true;
  };

  // ───── Ölçüler ─────
  const kvJson = (b: any, key: string) => { try { const r = b?.kv?.[key]; return r?.v ? JSON.parse(r.v) : null; } catch { return null; } };
  /** Profil yedeğinden gün → ölçü. */
  const yedektenMetrik = (b: any): Record<string, { sn: number; soru: number; bitir: number }> => {
    const m: Record<string, { sn: number; soru: number; bitir: number }> = {};
    const al = (g: string) => (m[g] ||= { sn: 0, soru: 0, bitir: 0 });
    for (const [g, s] of Object.entries<any>(b?.stats?.studySeconds || {})) if (/^\d{4}-\d\d-\d\d$/.test(g)) al(g).sn = Math.min(Number(s) || 0, 86400);
    const sayac = kvJson(b, 'medsoru_basarim_sayac_v1');
    for (const cihaz of Object.values<any>(sayac?.c || {})) for (const [g, n] of Object.entries<any>(cihaz || {})) if (/^\d{4}-\d\d-\d\d$/.test(g)) al(g).soru += Math.max(0, Number(n) || 0);
    const takip = kvJson(b, 'medsoru_calisma_takip_v1');
    for (const [id, r] of Object.entries<any>(takip?.k || {})) {
      if (r?.durum !== 'bitti' || !r.bittiAt) continue;
      const yeter = (Number(r.sn) || 0) >= tanim.taban.bitirmeAsgariSn || (id.startsWith('cozucu:') && (Number(r.soru) || 0) >= 20);
      if (yeter) al(gunOf(Date.parse(r.bittiAt))).bitir += 1;
    }
    return m;
  };

  const olcuGun = (k: Kisi, g: string, olcu: string): number => {
    const m = k.metrik[g];
    switch (olcu) {
      case 'calisma_sn': return m?.sn || 0;
      case 'soru': return m?.soru || 0;
      case 'bitirilen': return m?.bitir || 0;
      case 'oturum': return k.giris.gun[g] || 0;
      case 'aktif_gun': return aktifMi(k, g) ? 1 : 0;
      default: return 0;
    }
  };
  const aktifMi = (k: Kisi, g: string) => { const m = k.metrik[g]; return (m?.sn || 0) >= 900 || (m?.soru || 0) >= 20 || (m?.bitir || 0) > 0; };
  const toplamOlcu = (k: Kisi, olcu: string): number => {
    const gunler = Object.keys(k.metrik);
    switch (olcu) {
      case 'calisma_sn': return gunler.reduce((a, g) => a + k.metrik[g].sn, 0);
      case 'soru': return gunler.reduce((a, g) => a + k.metrik[g].soru, 0);
      case 'bitirilen': return gunler.reduce((a, g) => a + k.metrik[g].bitir, 0);
      case 'giris_gun': return Object.keys(k.giris.gun).length;
      case 'seri': return enUzunSeri(Object.keys(k.giris.gun));
      case 'oturum_max': return Math.max(0, ...Object.values(k.giris.gun));
      case 'ust_hedef': return k.defter.filter((d) => d.t === 'hedef' && d.ust).length;
      case 'podyum': return k.defter.filter((d) => d.t === 'siralama' && d.id.startsWith('s:hafta:')).length;
      default: return k.eylem.toplam[olcu] || 0;
    }
  };
  const enUzunSeri = (gunler: string[]) => {
    const s = [...gunler].sort(); let en = 0, cur = 0, onceki = '';
    for (const g of s) { cur = onceki && gunEkle(onceki, 1) === g ? cur + 1 : 1; en = Math.max(en, cur); onceki = g; }
    return en;
  };
  const guncelSeri = (k: Kisi) => {
    let g = gunOf(); if (!k.giris.gun[g]) g = gunEkle(g, -1);
    let n = 0; while (k.giris.gun[g]) { n++; g = gunEkle(g, -1); }
    return n;
  };

  const pencereOf = (k: Kisi, donem: HedefTanim['donem'], g: string): Pencere => {
    if (donem === 'gun') return { id: g, bas: g, son: g, ad: 'Bugün' };
    if (donem === 'hafta') { const b = haftaOf(g); return { id: b, bas: b, son: gunEkle(b, 6), ad: 'Bu hafta' }; }
    return kurulPencere(k.donem || 3, g);
  };
  const pencereOlcu = (k: Kisi, p: Pencere, olcu: string) => pencereGunleri(p.bas, p.son).reduce((a, g) => a + olcuGun(k, g, olcu), 0);

  // ───── Değerlendirme ─────
  const tabanPuan = (k: Kisi, g: string) => {
    const t = tanim.taban; const m = k.metrik[g];
    if (!m) return 0;
    return Math.min(m.soru, t.soruGunlukTavan) * t.soruBasina
      + Math.floor(Math.min(m.sn, t.calismaGunlukTavanSn) / 600) * t.onDakikaBasina
      + Math.min(m.bitir, t.bitirilenGunlukTavan) * t.bitirilenBasina;
  };
  const eylemPuan = (k: Kisi, g: string) => {
    const e = k.eylem.gun[g]; if (!e) return 0;
    return tanim.eylemler.reduce((a, x) => a + Math.min(e[x.id] || 0, x.gunlukTavan) * x.p, 0);
  };
  const gunPuanHesapla = (k: Kisi) => {
    const gp: Record<string, number> = {};
    for (const g of new Set([...Object.keys(k.metrik), ...Object.keys(k.eylem.gun)])) gp[g] = tabanPuan(k, g) + eylemPuan(k, g);
    for (const d of k.defter) if (d.p) gp[d.g] = (gp[d.g] || 0) + d.p;
    k.gunPuan = gp;
  };

  /** Kişiyi yeniden değerlendirir: ölçüleri yedekten tazeler, hedef/başarım ödüllerini verir, kuyruğu işler. */
  const degerlendir = (k: Kisi) => {
    const b = deps.okuYedek(k.uid);
    if (b) {
      if (!k.ad && b.displayName) k.ad = String(b.displayName).slice(0, 40);
      for (const [g, m] of Object.entries(yedektenMetrik(b))) {
        const c = k.metrik[g] || { sn: 0, soru: 0, bitir: 0 };
        k.metrik[g] = { sn: Math.max(c.sn, m.sn), soru: Math.max(c.soru, m.soru), bitir: Math.max(c.bitir, m.bitir) };
        // Sistem kurulmadan önceki çalışma günleri de giriş günü sayılır (seri ve sadakat başarımları geçmişi tanısın)
        if (!k.giris.gun[g] && (k.metrik[g].sn >= 60 || k.metrik[g].soru > 0) && g <= gunOf()) k.giris.gun[g] = 1;
      }
    }
    const bugun = gunOf();
    // Hedefler: bugün + dün (geç eşitlenen veri), bu + geçen hafta, bu + geçen kurul
    for (const h of tanim.hedefler) {
      const gunler = h.donem === 'gun' ? [bugun, gunEkle(bugun, -1)] : h.donem === 'hafta' ? [bugun, gunEkle(bugun, -7)] : [bugun];
      if (h.donem === 'kurul') { const p = pencereOf(k, 'kurul', bugun); gunler.push(gunEkle(p.bas, -1)); }
      for (const g of gunler) {
        const p = pencereOf(k, h.donem, g);
        const v = pencereOlcu(k, p, h.olcu);
        h.seviyeler.forEach(([esik, puan, atp], i) => {
          if (v >= esik) odul(k, { id: `h:${h.id}:${p.id}:${i + 1}`, t: 'hedef', ad: `${h.ad} · ${i + 1}. seviye`, p: puan, a: atp, ust: i === h.seviyeler.length - 1, ref: h.id }, p.son < bugun ? p.son : bugun);
        });
      }
    }
    for (const bs of tanim.basarimlar) {
      const v = toplamOlcu(k, bs.olcu);
      bs.seviyeler.forEach(([esik, puan, atp], i) => {
        if (v >= esik) odul(k, { id: `b:${bs.id}:${i + 1}`, t: 'basarim', ad: `${bs.ad} · ${i + 1}. seviye`, p: puan, a: bs.topluluk ? 0 : atp, ust: i === bs.seviyeler.length - 1, ref: bs.id });
      });
    }
    gunPuanHesapla(k);
    kuyrukIsle(k);
    k.degerAt = new Date().toISOString();
    kaydet(k);
  };

  // ───── Sıralama ─────
  const puanAralik = (k: Kisi, bas: string, son: string) => Object.entries(k.gunPuan).reduce((a, [g, p]) => (g >= bas && g <= son ? a + p : a), 0);
  const siralama = (donem: number, kapsam: 'hafta' | 'kurul' | 'tum', g = gunOf()) => {
    hepsiniYukle();
    const p = kapsam === 'hafta' ? { bas: haftaOf(g), son: gunEkle(haftaOf(g), 6), ad: 'Bu hafta', id: haftaOf(g) } : kapsam === 'kurul' ? kurulPencere(donem, g) : { bas: '0000', son: '9999', ad: 'Tüm zamanlar', id: 'tum' };
    const satir = [...onbellek.values()].filter((k) => k.donem === donem && k.uid !== 'ai-test').map((k) => ({ k, puan: puanAralik(k, p.bas, p.son) }))
      .filter((x) => x.puan > 0)
      .sort((a, b) => b.puan - a.puan || a.k.uid.localeCompare(b.k.uid));
    return { pencere: p, satir };
  };

  /** Biten hafta/kurul için ilk 5'e ATP (dönem başına, bir kez). */
  let sonOdeme = 0;
  const odemeleriIsle = () => {
    if (Date.now() - sonOdeme < 10 * 60_000) return;
    sonOdeme = Date.now();
    hepsiniYukle();
    let kayit: Record<string, string> = {};
    try { if (fs.existsSync(odemeDosya)) kayit = JSON.parse(fs.readFileSync(odemeDosya, 'utf8')); } catch { /* */ }
    const bugun = gunOf();
    const donemler = new Set([...onbellek.values()].map((k) => k.donem).filter((d): d is number => !!d));
    const degisen = new Set<Kisi>();
    for (const d of donemler) {
      const gecenHafta = gunEkle(haftaOf(bugun), -7);
      const gecenKurul = kurulPencere(d, gunEkle(kurulPencere(d, bugun).bas, -1));
      const isler: { anahtar: string; kapsam: 'hafta' | 'kurul'; g: string; oduller: number[]; esik: number; ad: string }[] = [
        { anahtar: `hafta:${gecenHafta}:d${d}`, kapsam: 'hafta', g: gecenHafta, oduller: tanim.atp.haftalikSiralama, esik: tanim.atp.siralamaEsikPuan.hafta, ad: 'Haftalık sıralama' },
      ];
      if (gecenKurul.son < bugun) isler.push({ anahtar: `kurul:${gecenKurul.id}`, kapsam: 'kurul', g: gecenKurul.son, oduller: tanim.atp.kurulSiralama, esik: tanim.atp.siralamaEsikPuan.kurul, ad: `${gecenKurul.ad} sıralaması` });
      for (const is of isler) {
        if (kayit[is.anahtar]) continue;
        const { satir } = siralama(d, is.kapsam, is.g);
        satir.slice(0, 5).forEach((x, i) => {
          if (x.puan < is.esik || !is.oduller[i]) return;
          if (odul(x.k, { id: `s:${is.anahtar}`, t: 'siralama', ad: `${is.ad} · ${i + 1}.`, p: 0, a: is.oduller[i] })) degisen.add(x.k);
        });
        kayit[is.anahtar] = new Date().toISOString();
      }
    }
    for (const k of degisen) { kuyrukIsle(k); kaydet(k); }
    atomik(odemeDosya, kayit);
  };

  // ───── Dışa açık işlemler ─────
  const OTURUM_ARA = 30 * 60_000;
  return {
    tanim: () => tanim,
    tanimYaz(t: any): string[] {
      const h = tanimDogrula(t);
      if (h.length) return h;
      atomik(ustTanimDosya, t); tanimYukle();
      return [];
    },
    kisi,
    /** Giriş/oturum kaydı + değerlendirme; durum özeti döner. */
    durum(uid: string, ad?: string) {
      const k = kisi(uid);
      if (ad && !k.ad) k.ad = ad.slice(0, 40);
      const simdi = Date.now();
      if (simdi - (k.giris.son || 0) > OTURUM_ARA) { const g = gunOf(simdi); k.giris.gun[g] = (k.giris.gun[g] || 0) + 1; }
      k.giris.son = simdi;
      try { odemeleriIsle(); } catch (e: any) { console.warn('[basarim] ödeme:', e?.message); }
      // Dönem seçilmeden ödül verilmez (kurul penceresi döneme bağlı); yalnız giriş kaydedilir
      if (k.donem) degerlendir(k); else kaydet(k);
      return this.ozet(k);
    },
    yenidenDegerlendir(uid: string) { const k = kisi(uid); if (k.donem) degerlendir(k); },
    ozet(k: Kisi) {
      const bugun = gunOf();
      const hedefler = tanim.hedefler.map((h) => {
        const p = pencereOf(k, h.donem, bugun);
        return { id: h.id, deger: pencereOlcu(k, p, h.olcu), pencere: p, alinan: h.seviyeler.filter((_, i) => k.defter.some((d) => d.id === `h:${h.id}:${p.id}:${i + 1}`)).length };
      });
      const basarimlar = tanim.basarimlar.map((b) => ({ id: b.id, deger: toplamOlcu(k, b.olcu), alinan: b.seviyeler.filter((_, i) => k.defter.some((d) => d.id === `b:${b.id}:${i + 1}`)).length }));
      const d = k.donem || 3;
      const sira = (kap: 'hafta' | 'kurul' | 'tum') => { const s = siralama(d, kap); const i = s.satir.findIndex((x) => x.k.uid === k.uid); return { sira: i < 0 ? null : i + 1, kisi: s.satir.length, puan: i < 0 ? 0 : s.satir[i].puan }; };
      return {
        profil: { donem: k.donem, kurul: k.kurul, ad: k.ad },
        puan: { toplam: puanAralik(k, '0000', '9999'), bugun: k.gunPuan[bugun] || 0 },
        atp: { bakiye: k.atp.bakiye, kuyrukta: k.atp.kuyruk.reduce((a, q) => a + q.a, 0), bugunAlinan: k.atp.gun[bugun] || 0, tavan: tanim.atp.gunlukTavan },
        seri: guncelSeri(k),
        hedefler, basarimlar,
        siralama: { hafta: sira('hafta'), kurul: sira('kurul'), tum: sira('tum') },
        kurulPencere: kurulPencere(d, bugun),
        defter: k.defter.slice(-80).reverse(),
        yeni: k.defter.filter((x) => x.at > k.goruldu && x.t !== 'baslangic'),
        kilit: k.kilit, secili: k.secili,
      };
    },
    goruldu(uid: string, at: string) { const k = kisi(uid); if (at > k.goruldu) { k.goruldu = at; kaydet(k); } },
    profil(uid: string, donem: number, kurul: number, ad?: string) {
      const k = kisi(uid);
      k.donem = donem; k.kurul = kurul; k.profilAt = new Date().toISOString();
      if (ad) k.ad = ad.slice(0, 40);
      degerlendir(k);
    },
    /** Topluluk eylemi (yalnız puan); beğeni hedef başına bir kez sayılır. */
    eylem(uid: string, tur: string, anahtar?: string) {
      if (!tanim.eylemler.some((e) => e.id === tur)) return;
      const k = kisi(uid);
      if (anahtar) {
        const h = crypto.createHash('sha1').update(anahtar).digest('hex').slice(0, 16);
        if (k.eylem.begeni.includes(h)) return;
        k.eylem.begeni.push(h);
        if (k.eylem.begeni.length > 5000) k.eylem.begeni.splice(0, 1000);
      }
      const g = gunOf();
      const gg = (k.eylem.gun[g] ||= {});
      gg[tur] = (gg[tur] || 0) + 1;
      k.eylem.toplam[tur] = (k.eylem.toplam[tur] || 0) + 1;
      if (k.donem) degerlendir(k); else kaydet(k);
    },
    satinAl(uid: string, id: string): { ok: true } | { hata: string } {
      const k = kisi(uid);
      const item = tanim.kilitler.find((x) => x.id === id);
      if (!item) return { hata: 'Böyle bir içerik yok.' };
      if (!item.etkin) return { hata: 'Bu içerik henüz açılmadı.' };
      if (k.kilit[id]) return { hata: 'Bu kilit zaten açık.' };
      if (k.atp.bakiye < item.fiyat) return { hata: `Yetersiz ATP: ${item.fiyat} mol gerekli, ${k.atp.bakiye} mol var.` };
      k.atp.bakiye -= item.fiyat;
      k.kilit[id] = new Date().toISOString();
      k.defter.push({ id: `x:${id}`, t: 'harcama', ad: item.ad, p: 0, a: -item.fiyat, at: k.kilit[id], g: gunOf() });
      if (item.tur !== 'icerik') k.secili[item.tur] = id;
      kaydet(k);
      return { ok: true };
    },
    sec(uid: string, tur: 'unvan' | 'cerceve' | 'efekt', id: string | null) {
      const k = kisi(uid);
      if (id && !k.kilit[id]) return false;
      if (id) k.secili[tur] = id; else delete k.secili[tur];
      kaydet(k);
      return true;
    },
    siralamaListesi(uid: string | null, donem: number, kapsam: 'hafta' | 'kurul' | 'tum') {
      try { odemeleriIsle(); } catch { /* */ }
      const s = siralama(donem, kapsam);
      const satir = s.satir.slice(0, 100).map((x, i) => ({
        sira: i + 1, ad: x.k.ad || 'Tıbbiyeli', puan: x.puan, ben: x.k.uid === uid,
        unvan: x.k.secili.unvan ? tanim.kilitler.find((t) => t.id === x.k.secili.unvan)?.ad.replace(/^Unvan:\s*/, '') : undefined,
        cerceve: x.k.secili.cerceve,
        basarim: x.k.defter.filter((d) => d.t === 'basarim').length,
      }));
      const benim = uid ? s.satir.findIndex((x) => x.k.uid === uid) : -1;
      if (benim >= 100) satir.push({ sira: benim + 1, ad: s.satir[benim].k.ad, puan: s.satir[benim].puan, ben: true, unvan: undefined, cerceve: undefined, basarim: 0 });
      return { pencere: s.pencere, satir, atpOdul: kapsam === 'hafta' ? tanim.atp.haftalikSiralama : kapsam === 'kurul' ? tanim.atp.kurulSiralama : [] };
    },
  };
}
export type BasarimMotor = ReturnType<typeof createBasarimMotor>;
