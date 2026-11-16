/**
 * Çıkmış soru veritabanına (data/pastQuestions.json, ~97 MB) servislerden erişim noktası.
 *
 * Neden: servisler dosyayı her çağrıda baştan JSON.parse edip doğrudan geri yazıyordu; bu, sunucunun
 * `cachedPastQuestionsDb` önbelleğini ve `savePastQuestionsDb` (fren + toplu atomik yazım + DB aynası) yolunu
 * atlıyor, eşzamanlı yazımda kayıp riski ve her çağrıda ~100 MB geçici kopya demekti.
 *
 * Sunucu açılışta `registerCikmisErisimi({ cikmisOku, cikmisKaydet })` ile kendi işlevlerini enjekte eder.
 * Enjeksiyon yoksa (betikten çağrı): okuma dosyadan yapılır (salt okunur geri dönüş), YAZMA reddedilir.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { veriOlayi } from './veriGunlugu.ts';

export type CikmisErisimi = {
  /** Sunucu önbelleğinden sığ kopya liste (öğeler paylaşılır). */
  cikmisOku: () => any[];
  /** Sunucunun tek yazım yolu (savePastQuestionsDb). */
  cikmisKaydet: (liste: any[]) => void;
};

const BURASI = path.dirname(fileURLToPath(import.meta.url));
const DOSYA = path.resolve(BURASI, '..', '..', 'data', 'pastQuestions.json');

let erisim: CikmisErisimi | null = null;

export function registerCikmisErisimi(e: CikmisErisimi): void {
  erisim = e;
}

export function cikmisOku(): any[] {
  if (erisim) {
    try { return erisim.cikmisOku(); } catch (e: any) {
      veriOlayi('hata', 'cikmis-erisim', 'enjekte okuma başarısız', { hata: String(e?.message || e) });
      return [];
    }
  }
  // Geri dönüş (betik): salt okunur
  try {
    if (!fs.existsSync(DOSYA)) return [];
    const veri = JSON.parse(fs.readFileSync(DOSYA, 'utf-8'));
    return Array.isArray(veri) ? veri : [];
  } catch {
    return [];
  }
}

/** Sunucu yolu yoksa yazmaz: hata kaydı düşer ve fırlatır (çağıran kendi catch'inde başarısız sayar). */
export function cikmisKaydet(liste: any[], kaynak: string): void {
  if (!erisim) {
    veriOlayi('hata', 'cikmis-erisim', 'sunucu kaydetme yolu enjekte edilmeden pastQuestions yazımı reddedildi', { kaynak });
    throw new Error('pastQuestions yazımı yalnız sunucu üzerinden yapılır (registerCikmisErisimi yok)');
  }
  erisim.cikmisKaydet(liste);
}
