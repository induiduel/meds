/**
 * Kurul takvimi — tek doğruluk kaynağı `src/data/kurul_takvimi_ozet.json`
 * (`scripts/takvim/kurul_takvimi.py --yaz` ders programı PDF'inden üretir; ders işçisi program değişince yeniler).
 * Sunucu ve ön yüz aynı kuralı kullanır; Python karşılığı `scripts/takvim/aktif_kurul.py`.
 *
 * Kural: aktif kurul = sınav günü henüz geçmemiş ilk kurul (sınav günü dahil o kurul aktiftir).
 * Sınavı geçmiş kurullar "arşiv"dir: verileri silinmez, ayrı görünümden erişilir.
 */
import takvim from '../data/kurul_takvimi_ozet.json';

export interface KurulBilgi { kurul: number; kod: string; ad: string; baslangic: string; sinav: string; bitis: string }

export const KURULLAR: KurulBilgi[] = (takvim as any).kurullar;
export const FINAL_TARIHI: string = (takvim as any).final;
export const BUTUNLEME_TARIHI: string = (takvim as any).butunleme;

/** Yerel gün (YYYY-AA-GG); saat dilimi kaymasıyla sınav günü yanlış kurula düşmesin. */
export function bugun(d: Date = new Date()): string {
  const p = (n: number) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

export function kurulId(kurul: number): string { return `donem3-kurul${kurul}`; }

/** Aktif committee kimliği: kurul → final → bütünleme. */
export function aktifCommitteeId(gun: string = bugun()): string {
  const k = KURULLAR.find((x) => gun <= x.sinav);
  if (k) return kurulId(k.kurul);
  if (FINAL_TARIHI && gun <= FINAL_TARIHI) return 'donem3-final';
  if (BUTUNLEME_TARIHI && gun <= BUTUNLEME_TARIHI) return 'donem3-butunleme';
  return 'donem3-final';
}

export function aktifKurul(gun: string = bugun()): KurulBilgi {
  return KURULLAR.find((x) => gun <= x.sinav) || KURULLAR[KURULLAR.length - 1];
}

/** Sınavı geçmiş (arşiv) kurullar — eski içerik "Geçmiş kurullar" görünümünde. */
export function arsivKurullar(gun: string = bugun()): KurulBilgi[] {
  return KURULLAR.filter((x) => x.sinav < gun);
}

/** Sınavı bugün ya da daha önce yapılmış en son kurul (olası soru toplama penceresi). */
export function sonSinavKurul(gun: string = bugun()): KurulBilgi | null {
  const g = KURULLAR.filter((x) => x.sinav <= gun);
  return g.length ? g[g.length - 1] : null;
}

export function sinavaKalanGun(gun: string = bugun()): number {
  const k = aktifKurul(gun);
  return Math.round((Date.parse(k.sinav) - Date.parse(gun)) / 86400000);
}
