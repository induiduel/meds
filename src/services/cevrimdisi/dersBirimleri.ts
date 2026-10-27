/**
 * Ders birimi: aynı dersin tüm çevrimdışı paketleri tek çatı altında (sesli ders, .medspak ders paketi, etkileşimli ders,
 * soru çözücü, en önemliler, alternatif çözücü). Kullanıcı bir dersi indirince hepsi birlikte iner, kayıt edilir, test edilir, silinir.
 * Eşleme (katalog paketlerinden, sunucuya dokunmadan):
 *   sesli ↔ .medspak : aynı ders anahtarı; sesli ↔ Öğren : sesli dersin `desteId`'si;
 *   sesli ↔ çözücü / önemli / alternatif : aynı branş + (ders no ya da başlık benzerliği);
 *   kalan Öğren dersleri : çözücü/önemli paketlerinin `ilgili` önerisi (sunucu katalogu), yoksa tek başına ders.
 */
import { paketDurumu, secimAl, secimliBayt, type Durum, type Modul, type Paket } from './paketMotoru';

export const UYE_SIRA: Modul[] = ['sesli', 'medspak', 'ogren', 'cozucu', 'onem', 'alt'];
export const UYE_AD: Record<string, string> = {
  sesli: 'Sesli ders', medspak: 'Ders paketi', ogren: 'Etkileşimli ders', cozucu: 'Soru çözücü', onem: 'En önemliler', alt: 'Alternatif çözücü',
};

export interface DersBirimi {
  id: string;
  grup: string;
  no: number;
  baslik: string;
  uyeler: Paket[];
  /** Sesli / .medspak üyesinden: kurul ve dönem (yoksa belirsiz) */
  kurul?: number;
  donem?: '2025-2026' | '2026-2027';
}
export type BirimDurum = 'tam' | 'kismi' | 'yok' | 'iniyor' | 'guncelleme' | 'hata';

export const boyutYaz = (n: number) => {
  if (!n) return '—';
  if (n < 1024 * 1024) return `${Math.max(1, Math.round(n / 1024))} KB`;
  if (n < 1024 ** 3) return `${(n / 1024 / 1024).toFixed(n < 10 * 1024 * 1024 ? 1 : 0).replace('.', ',')} MB`;
  return `${(n / 1024 ** 3).toFixed(2).replace('.', ',')} GB`;
};
export const katla = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');

const kelimeler = (s: string) => new Set(katla(s).replace(/[^a-z0-9\s]/g, ' ').split(/\s+/).filter((w) => w.length > 2));
function benzerlik(a: string, b: string): number {
  const x = kelimeler(a);
  const y = kelimeler(b);
  if (!x.size || !y.size) return 0;
  let ort = 0;
  x.forEach((w) => { if (y.has(w)) ort++; });
  return ort / (x.size + y.size - ort);
}
/** "Ders 16 · Tümör Biyolojisi…" → { no, ad } */
function dersBasligi(p: Paket): { no: number; ad: string } {
  const m = p.baslik.match(/^Ders\s+(\d+)\s*·\s*(.+)$/);
  return m ? { no: Number(m[1]), ad: m[2] } : { no: p.dersNo || 0, ad: p.baslik };
}

export function dersBirimleri(katalog: Paket[]): DersBirimi[] {
  const birimler: DersBirimi[] = [];
  const kullanilan = new Set<string>();
  const al = (id: string) => katalog.find((p) => p.id === id);
  const harita = new Map<string, Paket>(katalog.map((p) => [p.id, p]));

  // 1) Çapa: sesli dersler (+ aynı anahtarlı .medspak, desteId'li Öğren)
  for (const s of katalog.filter((p) => p.modul === 'sesli')) {
    const key = s.id.slice('sesli:'.length);
    const uyeler: Paket[] = [s];
    const mp = harita.get(`medspak:${key}`);
    if (mp) uyeler.push(mp);
    const og = s.desteId ? harita.get(`ogren:${s.desteId}`) : undefined;
    if (og) uyeler.push(og);
    birimler.push({ id: `ders:${key}`, grup: s.grup, no: s.dersNo || s.sira, baslik: s.baslik, uyeler });
  }
  // yalnız .medspak'ı olan (sesli listesinde olmayan) dersler
  for (const mp of katalog.filter((p) => p.modul === 'medspak')) {
    if (birimler.some((b) => b.uyeler.includes(mp))) continue;
    const og = mp.desteId ? harita.get(`ogren:${mp.desteId}`) : undefined;
    birimler.push({ id: `ders:${mp.id.slice('medspak:'.length)}`, grup: mp.grup, no: mp.dersNo || mp.sira, baslik: mp.baslik, uyeler: og ? [mp, og] : [mp] });
  }
  birimler.forEach((b) => b.uyeler.forEach((u) => kullanilan.add(u.id)));

  // 2) Çözücü / önemli / alternatif: aynı branşta no + başlık benzerliği
  const soru = katalog.filter((p) => ['cozucu', 'onem', 'alt'].includes(p.modul));
  const bekleyen: Paket[] = [];
  for (const p of soru) {
    const { no, ad } = dersBasligi(p);
    let en: DersBirimi | null = null;
    let enPuan = 0;
    for (const b of birimler) {
      if (b.grup !== p.grup) continue;
      const bens = benzerlik(ad, b.baslik);
      const puan = (b.no === no ? 0.4 : 0) + bens;
      if (puan > enPuan && (bens >= 0.8 || (b.no === no && bens >= 0.45))) { en = b; enPuan = puan; }
    }
    if (en && !en.uyeler.some((u) => u.modul === p.modul)) { en.uyeler.push(p); kullanilan.add(p.id); } else bekleyen.push(p);
  }
  // 3) Çapasız çözücü/önemli/alternatif: branş + ders no ile kendi aralarında birleşir
  const tek = new Map<string, DersBirimi>();
  for (const p of bekleyen) {
    const { no, ad } = dersBasligi(p);
    let k = `${p.grup}#${no || ad}`;
    while (tek.get(k)?.uyeler.some((u) => u.modul === p.modul)) k += '+';
    let b = tek.get(k);
    if (!b) { b = { id: `ders:${k}`, grup: p.grup, no, baslik: ad, uyeler: [] }; tek.set(k, b); birimler.push(b); }
    b.uyeler.push(p);
    kullanilan.add(p.id);
  }
  // 4) Kalan Öğren dersleri: çözücü/önemlinin `ilgili` önerisi → o birime; yoksa tek başına
  const birimDe = new Map<string, DersBirimi>();
  birimler.forEach((b) => b.uyeler.forEach((u) => birimDe.set(u.id, b)));
  for (const og of katalog.filter((p) => p.modul === 'ogren' && !kullanilan.has(p.id))) {
    const komsu = (og.ilgili || []).map((id) => birimDe.get(id)).find((b) => b && !b.uyeler.some((u) => u.modul === 'ogren'));
    if (komsu) { komsu.uyeler.push(og); birimDe.set(og.id, komsu); kullanilan.add(og.id); continue; }
    birimler.push({ id: `ders:${og.id}`, grup: og.grup, no: og.sira, baslik: og.baslik, uyeler: [og] });
    kullanilan.add(og.id);
  }
  void al;
  for (const b of birimler) {
    const k = b.uyeler.find((u) => u.kurul);
    if (k) { b.kurul = k.kurul; b.donem = k.donem; }
  }
  for (const b of birimler) b.uyeler.sort((x, y) => UYE_SIRA.indexOf(x.modul) - UYE_SIRA.indexOf(y.modul));
  return birimler.sort((a, b) => a.grup.localeCompare(b.grup, 'tr') || a.no - b.no || a.baslik.localeCompare(b.baslik, 'tr'));
}

type Dur = Parameters<typeof paketDurumu>[1];
export function birimDurumu(b: DersBirimi, s: Dur): { durum: BirimDurum; tamam: number; toplam: number; kalanBayt: number; toplamBayt: number } {
  let tamam = 0, iniyor = 0, guncel = 0, hata = 0;
  let kalan = 0, toplamB = 0;
  for (const u of b.uyeler) {
    const d: Durum = paketDurumu(u.id, s);
    const bayt = secimliBayt(u, secimAl(u.id, s));
    toplamB += bayt;
    if (d === 'tamam') tamam++;
    else if (d === 'guncelleme') { tamam++; guncel++; kalan += bayt; }
    else { kalan += bayt; if (d === 'iniyor' || d === 'kuyrukta') iniyor++; if (d === 'hata') hata++; }
  }
  const toplam = b.uyeler.length;
  const durum: BirimDurum = iniyor ? 'iniyor' : hata ? 'hata' : guncel ? 'guncelleme' : tamam === toplam ? 'tam' : tamam ? 'kismi' : 'yok';
  return { durum, tamam, toplam, kalanBayt: kalan, toplamBayt: toplamB };
}
