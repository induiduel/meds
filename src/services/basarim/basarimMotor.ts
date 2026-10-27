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
export interface KilitTanim {
  id: string; tur: 'unvan' | 'cerceve' | 'efekt' | 'icerik' | 'renk' | 'esya' | 'hucre'; ad: string; fiyat: number; etkin: boolean; renk?: string; aciklama?: string;
  /** Hücrem: bu basamaktan önce açılması gereken basamak; `cag` evrim çağı adı */
  onceki?: string; cag?: string;
  /** unvanın kıdemi; `kidemAcar` unvan alınınca kişinin kıdemi buna yükselir (bir önceki kıdem gerekir), diğerleri o kıdemde açılır */
  kidem?: number; kidemAcar?: boolean; eski?: boolean;
}
export interface KidemTanim { no: number; ad: string; tavan: number; aciklama?: string }
export const YONETICI_EPOSTA = 'nofrostlife@gmail.com';
export interface EylemTanim { id: string; ad: string; p: number; gunlukTavan: number }
export interface Tanim {
  surum: number;
  atp: { baslangic: number; gunlukTavan: number; haftalikSiralama: number[]; kurulSiralama: number[]; siralamaEsikPuan: { hafta: number; kurul: number }; calismaHaftaBirinci?: number; calismaEsikSn?: number };
  taban: { soruBasina: number; soruGunlukTavan: number; onDakikaBasina: number; calismaGunlukTavanSn: number; bitirilenBasina: number; bitirilenGunlukTavan: number; bitirmeAsgariSn: number };
  eylemler: EylemTanim[];
  hedefler: HedefTanim[];
  basarimlar: BasarimTanim[];
  kilitler: KilitTanim[];
  kidemler?: KidemTanim[];
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
    if (!(k.fiyat >= 50 && k.fiyat <= 10000)) h.push(`${k.id}: fiyat 50–10.000 mol olmalı`);
    if (k.tur === 'hucre' && k.onceki && !(t.kilitler || []).some((x: any) => x.id === k.onceki)) h.push(`${k.id}: önceki basamak ${k.onceki} yok`);
    if (k.tur === 'unvan' && k.kidem != null && !(t.kidemler || []).some((x: any) => x.no === k.kidem)) h.push(`${k.id}: kıdem ${k.kidem} tanımlı değil`);
  }
  if (!(t.atp?.gunlukTavan > 0 && t.atp.gunlukTavan <= 100)) h.push('atp.gunlukTavan 1–100 olmalı');
  let onceki = 0;
  for (const x of t.kidemler || []) {
    if (x.no !== onceki + 1) h.push(`kıdem numaraları 1'den sırayla artmalı (${x.ad})`);
    if (!(x.tavan >= 1 && x.tavan <= 1000)) h.push(`${x.ad}: günlük tavan 1–1000 olmalı`);
    onceki = x.no;
  }
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
/** Takvimli dönemde (D3) kurul her zaman takvimdeki aktif kurul; elle seçilen eski değer sayılmaz. */
export function efektifKurul(donem: number | null, kurul: number | null, g: string = gunOf()): number | null {
  if (donem === Number((takvim as any).donem || 3) && KURULLAR.length) {
    const m = /^d\d+-k(\d+)$/.exec(kurulPencere(donem, g).id);
    if (m) return Number(m[1]);
  }
  return kurul;
}
const pencereGunleri = (bas: string, son: string) => { const r: string[] = []; for (let g = bas; g <= son && r.length < 400; g = gunEkle(g, 1)) r.push(g); return r; };

// ───────────────────────── Kayıt ─────────────────────────
export interface DefterKaydi { id: string; t: 'baslangic' | 'hedef' | 'basarim' | 'siralama' | 'harcama' | 'yonetici'; by?: string; geriAlindi?: string; ad: string; p: number; a: number; at: string; g: string; ust?: boolean; ref?: string }
export interface Kisi {
  uid: string; ad: string; donem: number | null; kurul: number | null; profilAt?: string;
  /** Profil kurulumundaki üniversite (Sıralama › Üniversite/Sınıfım süzgeci) */
  universite?: string;
  defter: DefterKaydi[];
  atp: { bakiye: number; kuyruk: { id: string; a: number; ad: string; at: string }[]; gun: Record<string, number> };
  eylem: { gun: Record<string, Record<string, number>>; toplam: Record<string, number>; begeni: string[] };
  giris: { gun: Record<string, number>; son: number };
  /** gün → ölçü (soru, sn, bitir); yedekteki günler budansa da toplamlar korunur (en büyük tutulur) */
  metrik: Record<string, { sn: number; soru: number; bitir: number }>;
  gunPuan: Record<string, number>;
  kilit: Record<string, string>;
  secili: { unvan?: string; cerceve?: string; efekt?: string; renk?: string };
  goruldu: string;
  degerAt?: string;
  /** Aynı kişinin ikinci hesabı: asıl hesabın uid'i; sıralamada görünmez (kayıt silinmez) */
  birlesti?: string;
  email?: string;
  /** Yöneticinin verdiği gizli unvan: mağazada yok; `muaf` ise günlük ATP/puan sınırları ve içerik kilitleri uygulanmaz. */
  ozel?: { unvan: string; muaf: boolean; gorunur: boolean; at: string; by: string };
  /** Tüketilir ögeler (seri koruyucu …): adet */
  esya?: Record<string, number>;
  /** Seri koruyucuyla kapatılmış (girilmemiş) günler */
  korunan?: string[];
  /** Konu (calisma_takip anahtarı) → son görülen etkin süre; gün → konu → o gün eklenen süre (35 gün) */
  konuSn?: Record<string, number>;
  konuGun?: Record<string, Record<string, number>>;
  /** Hücrem: glukoz (enerji) bakiyesi, canlılık 0–100, istatistikler; `sn`/`soru` en son işlenen toplam ölçüler */
  hucre?: HucreKayit;
}
export interface HucreKayit { glukoz: number; kazanilan: number; harcanan: number; metabolik: number; canlilik: number; son: number; sn: number; soru: number }
/** Hücrem kuralları; tanim.json'daki `hucre` bölümü varsayılanların üstüne yazar. */
export const HUCRE_VARSAYILAN = {
  baslangic: 100, glukozDk: 1, glukozSoru: 2, tuketimTaban: 0.5, tuketimBasamak: 0.25, aclikHiz: 8, toparlanma: 10, glukozFiyatCarpan: 1,
  sampiyonCarpan: [1.25, 1.15, 1.1], haftalikSiralama: [40, 25, 15],
};
/** Yönetim günlüğü satırı (data/basarim/yonetim_gunlugu.jsonl, yalnız ekleme). */
export interface YonetimKaydi { at: string; by: string; uid: string; ad: string; tur: string; gerekce: string; ayrinti: any; once: any; sonra: any }

export interface MotorDeps { dataDir: string; srcDir: string; okuYedek: (uid: string) => any | null; fotoBul?: (uid: string) => string | null }

export function createBasarimMotor(deps: MotorDeps) {
  const kok = path.join(deps.dataDir, 'basarim');
  const kisiDir = path.join(kok, 'k');
  fs.mkdirSync(kisiDir, { recursive: true });
  const ustTanimDosya = path.join(kok, 'tanim.json');
  const odemeDosya = path.join(kok, 'odemeler.json');
  const gunlukDosya = path.join(kok, 'yonetim_gunlugu.jsonl');
  const gunlukYaz = (x: YonetimKaydi) => fs.appendFileSync(gunlukDosya, JSON.stringify(x) + '\n');
  const gunlukOku = (uid: string | null, limit = 300): YonetimKaydi[] => {
    try {
      const satir = fs.readFileSync(gunlukDosya, 'utf8').split('\n').filter(Boolean);
      const r: YonetimKaydi[] = [];
      for (let i = satir.length - 1; i >= 0 && r.length < limit; i--) { try { const x = JSON.parse(satir[i]); if (!uid || x.uid === uid) r.push(x); } catch { /* bozuk satır */ } }
      return r;
    } catch { return []; }
  };

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

  // ───── Kıdem ─────
  const kidemler = (): KidemTanim[] => (tanim.kidemler?.length ? tanim.kidemler : [{ no: 1, ad: 'Çömez', tavan: tanim.atp.gunlukTavan }]);
  const kidemNo = (k: Kisi) => tanim.kilitler.reduce((m, x) => (x.tur === 'unvan' && x.kidemAcar && k.kilit[x.id] && (x.kidem || 1) > m ? x.kidem || 1 : m), 1);
  const kidemOf = (k: Kisi) => kidemler().find((x) => x.no === kidemNo(k)) || kidemler()[0];
  const yoneticiMi = (k: Kisi) => String(k.email || '').toLowerCase() === YONETICI_EPOSTA;
  /** Günlük ATP tavanı: kıdeme göre; yönetici ve muaf gizli unvanlıda sınır yok (null). */
  const tavanOf = (k: Kisi): number | null => (yoneticiMi(k) || k.ozel?.muaf ? null : kidemOf(k).tavan);

  // ───── Ders adları (konu kimliği → okunur ad) ─────
  let dersAd: Map<string, string> | null = null;
  const dersAdlari = () => {
    if (dersAd) return dersAd;
    dersAd = new Map();
    try {
      const dir = path.join(deps.srcDir, 'data', 'dersler');
      for (const f of fs.readdirSync(dir)) {
        if (!/^k\d+\.json$/.test(f)) continue;
        for (const x of JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).dersler || []) if (x?.id) dersAd.set(x.id, `${x.brans} · ${x.konu}`);
      }
    } catch { /* ders kayıt defteri yoksa kimlikten türetilir */ }
    return dersAd;
  };
  const MODUL_AD: Record<string, string> = { sesli: 'Sesli ders', ogren: 'Etkileşimli', cozucu: 'Soru çözücü', onem: 'En önemliler', kamp: 'Kurul kampı' };
  const konuAdi = (id: string) => {
    const [m, ...r] = id.split(':'); const rest = r.join(':');
    const bk = rest.match(/^([a-zçğıöşü]+)\/[a-z]?0*(\d+)$/i);
    if (bk) return { ad: `${bk[1].charAt(0).toLocaleUpperCase('tr-TR')}${bk[1].slice(1)} · ${bk[2]}. ders`, modul: MODUL_AD[m] || m };
    const kimlik = rest.match(/k\d+-\d+/)?.[0];
    const ad = (kimlik && dersAdlari().get(kimlik)) || rest.replace(/^k\d+p?-/, '').replace(/-v\d+$/, '').replace(/[-_/]+/g, ' ').replace(/^deck /, '').trim();
    return { ad: ad.charAt(0).toLocaleUpperCase('tr-TR') + ad.slice(1), modul: MODUL_AD[m] || m };
  };

  // ───── ATP ─────
  const kuyrukIsle = (k: Kisi) => {
    const g = gunOf();
    const tv = tavanOf(k);
    let bos = tv == null ? Number.MAX_SAFE_INTEGER : tv - (k.atp.gun[g] || 0);
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

  /** Konu başına süre artışını güne yazar (en çok çalışılan dersler). İlk görüşte birikmiş süre son çalışıldığı güne yazılır. */
  const konuTakip = (k: Kisi, b: any) => {
    const takip = kvJson(b, 'medsoru_calisma_takip_v1');
    if (!takip?.k) return;
    const ilk = !k.konuSn;
    const snap = (k.konuSn ||= {}); const kg = (k.konuGun ||= {});
    const bugun = gunOf();
    for (const [id, r] of Object.entries<any>(takip.k)) {
      const sn = Number(r?.sn) || 0;
      const fark = sn - (snap[id] || 0);
      if (fark > 0) {
        const g = ilk || !(id in snap) ? (r?.sonAt ? gunOf(Date.parse(r.sonAt)) : bugun) : bugun;
        const gg = (kg[g] ||= {});
        gg[id] = (gg[id] || 0) + Math.min(fark, 86400);
      }
      snap[id] = sn;
    }
    const gunler = Object.keys(kg).sort();
    if (gunler.length > 35) for (const x of gunler.slice(0, gunler.length - 35)) delete kg[x];
  };
  const enCokDersler = (k: Kisi, bas: string, son: string, n = 3) => {
    const t: Record<string, number> = {};
    for (const [g, m] of Object.entries(k.konuGun || {})) if (g >= bas && g <= son) for (const [id, sn] of Object.entries(m)) t[id] = (t[id] || 0) + sn;
    return Object.entries(t).sort((a, b) => b[1] - a[1]).slice(0, n).map(([id, sn]) => ({ id, ...konuAdi(id), sn }));
  };
  const snAralik = (k: Kisi, bas: string, son: string) => Object.entries(k.metrik).reduce((a, [g, m]) => (g >= bas && g <= son ? a + Math.min(m.sn, 86400) : a), 0);

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
      case 'seri': return enUzunSeri([...Object.keys(k.giris.gun), ...(k.korunan || [])]);
      case 'oturum_max': return Math.max(0, ...Object.values(k.giris.gun));
      case 'ust_hedef': return k.defter.filter((d) => d.t === 'hedef' && d.ust).length;
      case 'hucre_basamak': return hucreBasamak(k);
      case 'glukoz_kazanilan': return Math.floor(k.hucre?.kazanilan || 0);
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
    const var_ = (g: string) => !!k.giris.gun[g] || !!k.korunan?.includes(g);
    let g = gunOf(); if (!var_(g)) g = gunEkle(g, -1);
    let n = 0; while (var_(g)) { n++; g = gunEkle(g, -1); }
    return n;
  };

  const pencereOf = (k: Kisi, donem: HedefTanim['donem'], g: string): Pencere => {
    if (donem === 'gun') return { id: g, bas: g, son: g, ad: 'Bugün' };
    if (donem === 'hafta') { const b = haftaOf(g); return { id: b, bas: b, son: gunEkle(b, 6), ad: 'Bu hafta' }; }
    return kurulPencere(k.donem || 3, g);
  };
  const pencereOlcu = (k: Kisi, p: Pencere, olcu: string) => pencereGunleri(p.bas, p.son).reduce((a, g) => a + olcuGun(k, g, olcu), 0);

  // ───── Hücrem: glukoz, canlılık, büyüklük sıralaması ─────
  const HV = () => ({ ...HUCRE_VARSAYILAN, ...((tanim as any).hucre || {}) });
  const hucreBasamak = (k: Kisi) => tanim.kilitler.reduce<number>((a, x) => (x.tur === 'hucre' && x.etkin && k.kilit[x.id] ? a + 1 : a), 0);
  const sinirla = (n: number, a = 0, b = 100) => Math.max(a, Math.min(b, n));
  /** Sıralama anlık görüntüsü (60 sn): uid → dönemindeki sırası; ilk üçe glukoz kazanç çarpanı verir. */
  const siraOnb = { t: 0, m: new Map<string, number>() };
  const hucreSatirlari = (donem: number) => {
    hepsiniYukle();
    return [...onbellek.values()].filter((k) => (k.donem || VARSAYILAN_DONEM) === donem && k.uid !== 'ai-test' && !k.birlesti && hucreBasamak(k) > 0)
      .map((k) => { const n = hucreBasamak(k); const uyku = (k.hucre?.canlilik ?? 100) <= 0; return { k, n, boyut: uyku ? n / 2 : n, uyku, kazanilan: k.hucre?.kazanilan || 0 }; })
      .sort((a, b) => b.boyut - a.boyut || b.kazanilan - a.kazanilan || a.k.uid.localeCompare(b.k.uid));
  };
  const siraYenile = () => {
    if (Date.now() - siraOnb.t < 60_000) return;
    siraOnb.t = Date.now(); siraOnb.m = new Map();
    hepsiniYukle();
    for (const d of new Set([...onbellek.values()].map((k) => k.donem || VARSAYILAN_DONEM))) hucreSatirlari(d).forEach((x, i) => siraOnb.m.set(x.k.uid, i + 1));
  };
  const hucreCarpan = (k: Kisi) => { const r = siraOnb.m.get(k.uid); return r ? (HV().sampiyonCarpan[r - 1] || 1) : 1; };
  /** Çalışma/soru → glukoz; geçen süre kadar metabolizma glukozu yer, yetmezse canlılık düşer, yetince toparlanır. */
  const hucreGuncelle = (k: Kisi, simdi = Date.now()): HucreKayit => {
    const v = HV();
    const sn = toplamOlcu(k, 'calisma_sn'), soru = toplamOlcu(k, 'soru');
    let h = k.hucre;
    if (!h) { h = k.hucre = { glukoz: v.baslangic, kazanilan: 0, harcanan: 0, metabolik: 0, canlilik: 100, son: simdi, sn, soru }; return h; }
    siraYenile();
    const kazan = ((Math.max(0, sn - h.sn) / 60) * v.glukozDk + Math.max(0, soru - h.soru) * v.glukozSoru) * hucreCarpan(k);
    h.sn = Math.max(h.sn, sn); h.soru = Math.max(h.soru, soru);
    h.glukoz += kazan; h.kazanilan += kazan;
    const saat = Math.min(72, Math.max(0, (simdi - h.son) / 3_600_000)); h.son = simdi;
    if (saat > 0) {
      const gerek = saat * (v.tuketimTaban + hucreBasamak(k) * v.tuketimBasamak);
      const odenen = Math.min(h.glukoz, gerek);
      h.glukoz -= odenen; h.metabolik += odenen;
      const oran = gerek > 0 ? odenen / gerek : 1;
      h.canlilik = sinirla(h.canlilik + saat * oran * v.toparlanma - saat * (1 - oran) * v.aclikHiz);
    }
    return h;
  };

  // ───── Değerlendirme ─────
  const tabanPuan = (k: Kisi, g: string) => {
    const t = tanim.taban; const m = k.metrik[g];
    if (!m) return 0;
    const muaf = !!k.ozel?.muaf;
    return (muaf ? m.soru : Math.min(m.soru, t.soruGunlukTavan)) * t.soruBasina
      + Math.floor((muaf ? m.sn : Math.min(m.sn, t.calismaGunlukTavanSn)) / 600) * t.onDakikaBasina
      + (muaf ? m.bitir : Math.min(m.bitir, t.bitirilenGunlukTavan)) * t.bitirilenBasina;
  };
  const eylemPuan = (k: Kisi, g: string) => {
    const e = k.eylem.gun[g]; if (!e) return 0;
    return tanim.eylemler.reduce((a, x) => a + (k.ozel?.muaf ? e[x.id] || 0 : Math.min(e[x.id] || 0, x.gunlukTavan)) * x.p, 0);
  };
  const gunPuanHesapla = (k: Kisi) => {
    const gp: Record<string, number> = {};
    for (const g of new Set([...Object.keys(k.metrik), ...Object.keys(k.eylem.gun)])) gp[g] = tabanPuan(k, g) + eylemPuan(k, g);
    for (const d of k.defter) if (d.p && !d.geriAlindi) gp[d.g] = (gp[d.g] || 0) + d.p;
    k.gunPuan = gp;
  };

  /** Kişiyi yeniden değerlendirir: ölçüleri yedekten tazeler, hedef/başarım ödüllerini verir, kuyruğu işler.
   *  Dönem seçmemiş kişinin yalnız ölçüleri ve taban puanı güncellenir (sıralamada varsayılan dönemde görünür), ödül verilmez. */
  const degerlendir = (k: Kisi) => {
    const b = deps.okuYedek(k.uid);
    if (b?.email) k.email = String(b.email);
    if (b) konuTakip(k, b);
    if (b) {
      const ad = String(b.displayName || '').trim().slice(0, 40);
      if (ad) k.ad = ad;
      for (const [g, m] of Object.entries(yedektenMetrik(b))) {
        const c = k.metrik[g] || { sn: 0, soru: 0, bitir: 0 };
        k.metrik[g] = { sn: Math.max(c.sn, m.sn), soru: Math.max(c.soru, m.soru), bitir: Math.max(c.bitir, m.bitir) };
        // Sistem kurulmadan önceki çalışma günleri de giriş günü sayılır (seri ve sadakat başarımları geçmişi tanısın)
        if (!k.giris.gun[g] && (k.metrik[g].sn >= 60 || k.metrik[g].soru > 0) && g <= gunOf()) k.giris.gun[g] = 1;
      }
    }
    const bugun = gunOf();
    hucreGuncelle(k);
    if (!k.donem) { gunPuanHesapla(k); k.degerAt = new Date().toISOString(); kaydet(k); return; }
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
  /** Dönem seçmemiş kişiler bu dönemin sıralamasında görünür (takvimdeki dönem). */
  const VARSAYILAN_DONEM = Number((takvim as any).donem || 3);
  const puanAralik = (k: Kisi, bas: string, son: string) => Object.entries(k.gunPuan).reduce((a, [g, p]) => (g >= bas && g <= son ? a + p : a), 0);
  /** Sıralamada herkesin profil fotoğrafı görünür: https adresi ya da profilden yüklenen kırpılmış resim (256 px JPEG, ~15–30 KB; 60 KB üstü atlanır). */
  const foto = (uid: string): string | undefined => {
    try {
      const f = deps.fotoBul?.(uid);
      if (!f) return undefined;
      if (/^https:\/\//.test(f)) return f.length < 1000 ? f : undefined;
      return /^data:image\/(jpeg|png|webp);base64,/.test(f) && f.length < 80_000 ? f : undefined;
    } catch { return undefined; }
  };
  /** donem -1 + universite: üniversitenin tüm dönemleri; universite verilirse yalnız o üniversite. */
  const siralama = (donem: number, kapsam: 'hafta' | 'kurul' | 'tum', g = gunOf(), universite?: string) => {
    hepsiniYukle();
    const dSuz = universite && donem === -1 ? null : donem;
    const p = kapsam === 'hafta' ? { bas: haftaOf(g), son: gunEkle(haftaOf(g), 6), ad: 'Bu hafta', id: haftaOf(g) } : kapsam === 'kurul' ? kurulPencere(dSuz ?? VARSAYILAN_DONEM, g) : { bas: '0000', son: '9999', ad: 'Tüm zamanlar', id: 'tum' };
    const satir = [...onbellek.values()].filter((k) => (dSuz == null || (k.donem || VARSAYILAN_DONEM) === dSuz) && (!universite || k.universite === universite) && k.uid !== 'ai-test' && !k.birlesti).map((k) => ({ k, puan: puanAralik(k, p.bas, p.son) }))
      .filter((x) => x.puan > 0)
      .sort((a, b) => b.puan - a.puan || a.k.uid.localeCompare(b.k.uid));
    return { pencere: p, satir };
  };

  /** Çalışma süresi sıralaması: gün ya da hafta; en çok çalışılan dersler satırda. */
  const calismaSiralama = (donem: number, kapsam: 'gun' | 'hafta', g = gunOf()) => {
    hepsiniYukle();
    const p = kapsam === 'gun' ? { bas: g, son: g, ad: 'Bugün', id: g } : { bas: haftaOf(g), son: gunEkle(haftaOf(g), 6), ad: 'Bu hafta', id: haftaOf(g) };
    const satir = [...onbellek.values()].filter((k) => (k.donem || VARSAYILAN_DONEM) === donem && k.uid !== 'ai-test' && !k.birlesti)
      .map((k) => ({ k, sn: snAralik(k, p.bas, p.son) })).filter((x) => x.sn >= 60)
      .sort((a, b) => b.sn - a.sn || a.k.uid.localeCompare(b.k.uid));
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
      // Haftanın en çok çalışanı (eşik süresini geçtiyse)
      const ck = `calisma:${gecenHafta}:d${d}`;
      if (!kayit[ck] && tanim.atp.calismaHaftaBirinci) {
        const ilk = calismaSiralama(d, 'hafta', gecenHafta).satir[0];
        if (ilk && ilk.sn >= (tanim.atp.calismaEsikSn || 0) && odul(ilk.k, { id: `s:${ck}`, t: 'siralama', ad: `Haftanın en çok çalışanı (${Math.round(ilk.sn / 3600)} sa)`, p: 0, a: tanim.atp.calismaHaftaBirinci })) degisen.add(ilk.k);
        kayit[ck] = new Date().toISOString();
      }
      const hk = `hucre:${gecenHafta}:d${d}`;
      if (!kayit[hk]) {
        hucreSatirlari(d).slice(0, 3).forEach((x, i) => {
          const a = HV().haftalikSiralama[i]; if (!a) return;
          if (odul(x.k, { id: `s:${hk}`, t: 'siralama', ad: `Haftanın en büyük hücresi · ${i + 1}.`, p: 0, a })) degisen.add(x.k);
        });
        kayit[hk] = new Date().toISOString();
      }
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
      if (simdi - (k.giris.son || 0) > OTURUM_ARA) {
        const g = gunOf(simdi);
        // Seri koruyucu: dün girilmediyse ve önceki gün zincir sürüyorsa bir koruyucu harcanır
        const dun = gunEkle(g, -1), evvel = gunEkle(g, -2);
        const vardi = (x: string) => !!k.giris.gun[x] || !!k.korunan?.includes(x);
        if (!k.giris.gun[g] && !vardi(dun) && vardi(evvel) && (k.esya?.esya_seri || 0) > 0) {
          k.esya!.esya_seri -= 1; (k.korunan ||= []).push(dun);
          k.defter.push({ id: `k:${dun}`, t: 'harcama', ad: `Seri koruyucu kullanıldı (${dun})`, p: 0, a: 0, at: new Date().toISOString(), g });
        }
        k.giris.gun[g] = (k.giris.gun[g] || 0) + 1;
      }
      k.giris.son = simdi;
      try { odemeleriIsle(); } catch (e: any) { console.warn('[basarim] ödeme:', e?.message); }
      // Dönem seçilmeden ödül verilmez (kurul penceresi döneme bağlı); ölçü ve taban puan yine güncellenir
      degerlendir(k);
      return this.ozet(k);
    },
    bag(uid: string) { return onbellek.get(uid)?.birlesti || kisi(uid).birlesti || null; },
    /** İkinci hesabı asıl hesaba bağlar (geri almak için hedef null). */
    birlestir(kaynak: string, hedef: string | null) {
      const k = kisi(kaynak);
      if (hedef) k.birlesti = hedef; else delete k.birlesti;
      kaydet(k);
    },
    yenidenDegerlendir(uid: string) { degerlendir(kisi(uid)); },
    /** Tüm profil yedeklerini tarar: kaydı olmayan kişiler de sıralamaya girer, eski ölçüler tazelenir. */
    tumunuDegerlendir(uidler: string[]) {
      hepsiniYukle();
      let n = 0;
      for (const uid of uidler) { try { degerlendir(kisi(uid)); n++; } catch (e: any) { console.warn('[basarim] tarama:', uid.slice(0, 8), e?.message); } }
      return n;
    },
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
        profil: { donem: k.donem, kurul: efektifKurul(k.donem, k.kurul), ad: k.ad },
        puan: { toplam: puanAralik(k, '0000', '9999'), bugun: k.gunPuan[bugun] || 0 },
        atp: { bakiye: k.atp.bakiye, kuyrukta: k.atp.kuyruk.reduce((a, q) => a + q.a, 0), bugunAlinan: k.atp.gun[bugun] || 0, tavan: tavanOf(k) },
        kidem: { ...kidemOf(k), sonraki: kidemler().find((x) => x.no === kidemOf(k).no + 1) || null },
        esya: k.esya || {},
        calisma: { bugun: snAralik(k, bugun, bugun), hafta: snAralik(k, haftaOf(bugun), gunEkle(haftaOf(bugun), 6)), dersler: enCokDersler(k, haftaOf(bugun), gunEkle(haftaOf(bugun), 6), 5) },
        seri: guncelSeri(k),
        hedefler, basarimlar,
        siralama: { hafta: sira('hafta'), kurul: sira('kurul'), tum: sira('tum') },
        kurulPencere: kurulPencere(d, bugun),
        defter: k.defter.slice(-80).reverse(),
        yeni: k.defter.filter((x) => x.at > k.goruldu && x.t !== 'baslangic'),
        kilit: k.kilit, secili: k.secili,
        hucre: this.hucreOzet(k),
        ozel: k.ozel ? { unvan: k.ozel.unvan, muaf: k.ozel.muaf } : null,
      };
    },
    hucreOzet(k: Kisi) {
      const v = HV(); const h = hucreGuncelle(k); const n = hucreBasamak(k);
      const d = k.donem || VARSAYILAN_DONEM; const sat = hucreSatirlari(d); const i = sat.findIndex((x) => x.k.uid === k.uid);
      const saatlik = v.tuketimTaban + n * v.tuketimBasamak;
      return {
        glukoz: Math.floor(h.glukoz * 10) / 10, kazanilan: Math.floor(h.kazanilan), harcanan: Math.floor(h.harcanan), metabolik: Math.floor(h.metabolik),
        canlilik: Math.round(h.canlilik), uyku: h.canlilik <= 0, basamak: n, saatlik, carpan: hucreCarpan(k),
        saatKaldi: saatlik > 0 ? Math.floor(h.glukoz / saatlik) : null,
        sira: i < 0 ? null : i + 1, kisi: sat.length, calismaSn: toplamOlcu(k, 'calisma_sn'), soru: toplamOlcu(k, 'soru'),
        atpKazanilan: k.defter.reduce((a, x) => (x.a > 0 && !x.geriAlindi ? a + x.a : a), 0),
        basarim: k.defter.filter((x) => x.t === 'basarim' && !x.geriAlindi).length,
        glukozDk: v.glukozDk, glukozSoru: v.glukozSoru, glukozFiyatCarpan: v.glukozFiyatCarpan,
      };
    },
    /** Hücre büyüklüğü sıralaması: basamak sayısı (uykudaki hücre yarım), eşitlikte toplam kazanılan glukoz. */
    hucreListesi(uid: string | null, donem: number) {
      try { odemeleriIsle(); } catch { /* */ }
      const v = HV(); siraOnb.t = 0;
      const sat = hucreSatirlari(donem);
      const mk = (x: (typeof sat)[number], i: number) => ({
        sira: i + 1, ad: x.k.ad || 'Tıbbiyeli', ben: x.k.uid === uid, foto: foto(x.k.uid), renk: x.k.secili.renk, cerceve: x.k.secili.cerceve, kidem: kidemOf(x.k).ad,
        basamak: x.n, cag: tanim.kilitler.filter((t) => t.tur === 'hucre' && t.etkin && x.k.kilit[t.id]).pop()?.cag || '',
        canlilik: Math.round(x.k.hucre?.canlilik ?? 100), uyku: x.uyku, glukoz: Math.floor(x.kazanilan), calismaSn: toplamOlcu(x.k, 'calisma_sn'), soru: toplamOlcu(x.k, 'soru'),
        atp: x.k.defter.reduce((a, d) => (d.a > 0 && !d.geriAlindi ? a + d.a : a), 0), basarim: x.k.defter.filter((d) => d.t === 'basarim' && !d.geriAlindi).length,
      });
      const satir = sat.slice(0, 100).map(mk);
      const benim = uid ? sat.findIndex((x) => x.k.uid === uid) : -1;
      if (benim >= 100) satir.push(mk(sat[benim], benim));
      return { satir, benim: benim >= 0 ? benim + 1 : null, odul: v.haftalikSiralama, carpan: v.sampiyonCarpan };
    },
    universiteAyarla(uid: string, universite: string) {
      const k = kisi(uid); const u = universite.trim().slice(0, 120);
      if ((k.universite || '') === u) return;
      k.universite = u || undefined; kaydet(k);
    },
    universiteOf(uid: string) { return kisi(uid).universite || ''; },
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
      degerlendir(k);
    },
    /** İçerik kilidi açık mı: kilit etkin değilse herkese açık; açılmışsa, muaf gizli unvanlı ya da yöneticiyse geçer. */
    kilitAcikMi(uid: string, id: string): boolean {
      const item = tanim.kilitler.find((x) => x.id === id);
      if (!item || !item.etkin) return true;
      const k = kisi(uid);
      return !!k.kilit[id] || !!k.ozel?.muaf || yoneticiMi(k);
    },
    satinAl(uid: string, id: string, odeme: 'atp' | 'glukoz' = 'atp'): { ok: true } | { hata: string } {
      const k = kisi(uid);
      const item = tanim.kilitler.find((x) => x.id === id);
      if (!item) return { hata: 'Böyle bir içerik yok.' };
      if (!item.etkin) return { hata: 'Bu içerik henüz açılmadı.' };
      if (item.tur !== 'esya' && k.kilit[id]) return { hata: 'Bu kilit zaten açık.' };
      if (item.tur === 'unvan' && item.kidem) {
        const simdiki = kidemNo(k);
        const gerek = item.kidemAcar ? item.kidem - 1 : item.kidem;
        if (simdiki < gerek) return { hata: `Önce ${kidemler().find((x) => x.no === gerek)?.ad || gerek + '.'} kıdemine yüksel.` };
      }
      if (item.tur === 'hucre' && item.onceki && !k.kilit[item.onceki]) {
        return { hata: `Önce "${tanim.kilitler.find((x) => x.id === item.onceki)?.ad || item.onceki}" basamağını aç.` };
      }
      const glukozla = odeme === 'glukoz';
      if (glukozla) {
        if (item.tur !== 'hucre') return { hata: 'Glukozla yalnız hücre basamakları açılır.' };
        const h = hucreGuncelle(k); const f = Math.ceil(item.fiyat * HV().glukozFiyatCarpan);
        if (h.glukoz < f) return { hata: `Yetersiz glukoz: ${f} gerekli, ${Math.floor(h.glukoz)} var. Ders çalışıp soru çözerek glukoz kazan.` };
        h.glukoz -= f; h.harcanan += f;
      } else {
        if (k.atp.bakiye < item.fiyat) return { hata: `Yetersiz ATP: ${item.fiyat} mol gerekli, ${k.atp.bakiye} mol var.` };
        k.atp.bakiye -= item.fiyat;
      }
      const at = new Date().toISOString();
      if (item.tur === 'esya') {
        (k.esya ||= {})[id] = (k.esya[id] || 0) + 1;
        k.defter.push({ id: `x:${id}:${at}`, t: 'harcama', ad: item.ad, p: 0, a: -item.fiyat, at, g: gunOf() });
        kaydet(k);
        return { ok: true };
      }
      k.kilit[id] = at;
      k.defter.push({ id: `x:${id}`, t: 'harcama', ad: (item.tur === 'unvan' && item.kidemAcar ? `${item.ad} · kıdem yükseldi` : item.ad) + (glukozla ? ' (glukoz)' : ''), p: 0, a: glukozla ? 0 : -item.fiyat, at, g: gunOf() });
      if (item.tur !== 'icerik') (k.secili as any)[item.tur] = id;
      kaydet(k);
      return { ok: true };
    },
    sec(uid: string, tur: 'unvan' | 'cerceve' | 'efekt' | 'renk', id: string | null) {
      const k = kisi(uid);
      if (id && !k.kilit[id]) return false;
      if (id) k.secili[tur] = id; else delete k.secili[tur];
      kaydet(k);
      return true;
    },
    calismaListesi(uid: string | null, donem: number, kapsam: 'gun' | 'hafta') {
      try { odemeleriIsle(); } catch { /* */ }
      const s = calismaSiralama(donem, kapsam);
      const satir = s.satir.slice(0, 100).map((x, i) => ({
        sira: i + 1, ad: x.k.ad || 'Tıbbiyeli', sn: x.sn, ben: x.k.uid === uid, foto: foto(x.k.uid), renk: x.k.secili.renk, cerceve: x.k.secili.cerceve, kidem: kidemOf(x.k).ad,
        dersler: enCokDersler(x.k, s.pencere.bas, s.pencere.son, 3),
      }));
      const benim = uid ? s.satir.findIndex((x) => x.k.uid === uid) : -1;
      return { pencere: s.pencere, satir, benim: benim >= 0 ? benim + 1 : null, odul: kapsam === 'hafta' ? tanim.atp.calismaHaftaBirinci || 0 : 0, esikSn: tanim.atp.calismaEsikSn || 0 };
    },
    siralamaListesi(uid: string | null, donem: number, kapsam: 'hafta' | 'kurul' | 'tum', universite?: string) {
      try { odemeleriIsle(); } catch { /* */ }
      const s = siralama(donem, kapsam, gunOf(), universite);
      const satir = s.satir.slice(0, 100).map((x, i) => ({
        sira: i + 1, ad: x.k.ad || 'Tıbbiyeli', puan: x.puan, ben: x.k.uid === uid, foto: foto(x.k.uid),
        ozel: !!x.k.ozel?.gorunur,
        unvan: x.k.ozel?.gorunur ? x.k.ozel.unvan : x.k.secili.unvan ? tanim.kilitler.find((t) => t.id === x.k.secili.unvan)?.ad.replace(/^Unvan:\s*/, '') : undefined,
        cerceve: x.k.secili.cerceve,
        renk: x.k.secili.renk,
        kidem: kidemOf(x.k).ad,
        basarim: x.k.defter.filter((d) => d.t === 'basarim').length,
      }));
      const benim = uid ? s.satir.findIndex((x) => x.k.uid === uid) : -1;
      if (benim >= 100) satir.push({ sira: benim + 1, ad: s.satir[benim].k.ad, puan: s.satir[benim].puan, ben: true, foto: foto(s.satir[benim].k.uid), ozel: false, unvan: undefined, cerceve: undefined, renk: undefined, kidem: kidemOf(s.satir[benim].k).ad, basarim: 0 });
      return { pencere: s.pencere, satir, atpOdul: kapsam === 'hafta' ? tanim.atp.haftalikSiralama : kapsam === 'kurul' ? tanim.atp.kurulSiralama : [] };
    },
    // ───── Yönetim (yalnız yönetici uçları çağırır; her işlem gerekçeli, defterde iz + yonetim_gunlugu.jsonl) ─────
    yonetimListe() {
      hepsiniYukle();
      const bugun = gunOf(); const hb = haftaOf(bugun);
      return [...onbellek.values()].filter((k) => k.uid !== 'ai-test').map((k) => {
        const kp = kurulPencere(k.donem || 3, bugun);
        return {
          uid: k.uid, ad: k.ad, email: k.email || '', donem: k.donem, kurul: efektifKurul(k.donem, k.kurul), birlesti: k.birlesti || null,
          puan: puanAralik(k, '0000', '9999'), hafta: puanAralik(k, hb, gunEkle(hb, 6)), kurulPuan: puanAralik(k, kp.bas, kp.son),
          atp: k.atp.bakiye, kuyruk: k.atp.kuyruk.reduce((a, q) => a + q.a, 0), kilit: Object.keys(k.kilit).length,
          basarim: k.defter.filter((d) => d.t === 'basarim' && !d.geriAlindi).length,
          sonGiris: k.giris.son ? new Date(k.giris.son).toISOString() : '', ozel: k.ozel || null,
          kidem: kidemOf(k).ad, tavan: tavanOf(k),
        };
      });
    },
    yonetimKisi(uid: string) {
      const k = kisi(uid);
      return { kisi: { ...k, metrik: undefined, eylem: { toplam: k.eylem.toplam }, defter: [...k.defter].reverse() }, ozet: this.ozet(k), gunluk: gunlukOku(uid) };
    },
    yonetimGunlugu(limit = 300) { return gunlukOku(null, limit); },
    yonetimIslem(uid: string, by: string, tur: string, g: any, gerekce: string): { hata?: string } {
      gerekce = String(gerekce || '').trim();
      if (gerekce.length < 3) return { hata: 'Gerekçe yazılmalı (en az 3 harf).' };
      const k = kisi(uid);
      const kuyrukT = () => k.atp.kuyruk.reduce((a, q) => a + q.a, 0);
      const anlik = () => ({ puan: puanAralik(k, '0000', '9999'), atp: k.atp.bakiye, kuyruk: kuyrukT(), donem: k.donem, kurul: efektifKurul(k.donem, k.kurul), kilit: Object.keys(k.kilit), ozel: k.ozel || null });
      const once = anlik();
      const at = new Date().toISOString();
      const iz = (ad: string, p: number, a: number) => k.defter.push({ id: `y:${at}:${Math.random().toString(36).slice(2, 7)}`, t: 'yonetici', ad, p, a, at, g: gunOf(), by });
      const n = Math.round(Number(g?.miktar) || 0);
      switch (tur) {
        case 'puan':
          if (!n || Math.abs(n) > 100000) return { hata: 'Puan miktarı 1–100.000 arası olmalı (eksi olabilir).' };
          iz(`Yönetici ${Math.abs(n)} puan ${n > 0 ? 'ekledi' : 'düştü'}: ${gerekce}`, n, 0); break;
        case 'atp':
          if (!n || Math.abs(n) > 100000) return { hata: 'ATP miktarı 1–100.000 arası olmalı (eksi olabilir).' };
          if (k.atp.bakiye + n < 0) return { hata: `Bakiye eksiye düşemez (bakiye ${k.atp.bakiye} mol).` };
          k.atp.bakiye += n; iz(`Yönetici ${Math.abs(n)} mol ATP ${n > 0 ? 'ekledi' : 'düştü'}: ${gerekce}`, 0, n); break;
        case 'kuyruk_aktar': {
          const t = kuyrukT(); if (!t) return { hata: 'Kuyruk boş.' };
          k.atp.bakiye += t; k.atp.kuyruk = []; iz(`Kuyruktaki ${t} mol hemen hesaba geçirildi: ${gerekce}`, 0, 0); break;
        }
        case 'kuyruk_sil': {
          const t = kuyrukT(); if (!t) return { hata: 'Kuyruk boş.' };
          k.atp.kuyruk = []; iz(`Kuyruktaki ${t} mol silindi: ${gerekce}`, 0, 0); break;
        }
        case 'kilit_ver': {
          const it = tanim.kilitler.find((x) => x.id === g?.id);
          if (!it) return { hata: 'Böyle bir kilit yok.' };
          if (k.kilit[it.id]) return { hata: 'Kilit zaten açık.' };
          k.kilit[it.id] = at; iz(`Yönetici kilidi açtı (${it.ad}): ${gerekce}`, 0, 0); break;
        }
        case 'kilit_al': {
          const it = tanim.kilitler.find((x) => x.id === g?.id);
          if (!it || !k.kilit[it.id]) return { hata: 'Bu kilit açık değil.' };
          delete k.kilit[it.id];
          for (const t of ['unvan', 'cerceve', 'efekt'] as const) if (k.secili[t] === it.id) delete k.secili[t];
          if (g?.iade) { k.atp.bakiye += it.fiyat; iz(`Kilit geri alındı, ${it.fiyat} mol iade (${it.ad}): ${gerekce}`, 0, it.fiyat); }
          else iz(`Kilit geri alındı (${it.ad}): ${gerekce}`, 0, 0);
          break;
        }
        case 'profil': {
          const d = Number(g?.donem), ku = Number(g?.kurul);
          if (!(d >= 1 && d <= 6) || !(ku >= 1 && ku <= 10)) return { hata: 'Dönem 1–6, kurul 1–10 olmalı.' };
          k.donem = d; k.kurul = ku; iz(`Dönem/kurul ${d}. dönem ${ku}. kurul yapıldı: ${gerekce}`, 0, 0); break;
        }
        case 'ozel': {
          const unvan = String(g?.unvan || '').trim().slice(0, 40);
          if (!unvan) return { hata: 'Unvan yazılmalı.' };
          k.ozel = { unvan, muaf: g?.muaf !== false, gorunur: !!g?.gorunur, at, by };
          iz(`Gizli unvan verildi: ${unvan}${k.ozel.muaf ? ' (sınırlardan muaf)' : ''}: ${gerekce}`, 0, 0); break;
        }
        case 'ozel_kaldir':
          if (!k.ozel) return { hata: 'Gizli unvan yok.' };
          iz(`Gizli unvan kaldırıldı (${k.ozel.unvan}): ${gerekce}`, 0, 0); delete k.ozel; break;
        case 'odul_geri': {
          const d = k.defter.find((x) => x.id === g?.id);
          if (!d || d.t === 'harcama') return { hata: 'Kayıt bulunamadı ya da harcama geri alınamaz (kilidi geri alıp iade et).' };
          if (d.geriAlindi) return { hata: 'Bu kayıt zaten geri alınmış.' };
          if (d.a > 0) {
            const q = k.atp.kuyruk.find((x) => x.id === d.id);
            const dus = d.a - (q ? q.a : 0);
            if (k.atp.bakiye - dus < 0) return { hata: `Bakiye yetmiyor: ${dus} mol düşülmeli, bakiye ${k.atp.bakiye} mol.` };
            if (q) k.atp.kuyruk = k.atp.kuyruk.filter((x) => x !== q);
            k.atp.bakiye -= dus;
          } else if (d.a < 0) k.atp.bakiye -= d.a;
          // Hedef/başarım ödülü geri alınınca yeniden verilmesin: kimlik defterde kalır, yalnız etkisi kalkar
          d.geriAlindi = at; iz(`Geri alındı: ${d.ad}: ${gerekce}`, 0, 0); break;
        }
        default: return { hata: 'Bilinmeyen işlem.' };
      }
      degerlendir(k);
      gunlukYaz({ at, by, uid, ad: k.ad, tur, gerekce: gerekce.slice(0, 300), ayrinti: g || {}, once, sonra: anlik() });
      return {};
    },
  };
}
export type BasarimMotor = ReturnType<typeof createBasarimMotor>;
