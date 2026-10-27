/**
 * Öğrenci profili (tasarım v15 › I07–I10 kayıt adımları): üniversite, sınıf, öğrenci numarası, eğitim yılı, aktif kurul,
 * günlük hedef ve hatırlatma saati. Cihazda `medsoru_profil_v1`; userKvSync SYNC_PATTERNS'te (hesaba eşitlenir, başka
 * cihazda yeniden sorulmaz). Günlük hedef Bugün planının hedefi olur (yoksa son 14 günün ortalaması kullanılır).
 */
import { useSyncExternalStore } from 'react';

export interface Profil {
  universite?: string;
  fakulte?: string;
  sinif?: number;
  numara?: string;
  egitimYili?: string;
  kurul?: number;
  hedef?: { ad: string; dk: number; soru: number };
  hatirlatma?: string;
  tamam?: string;
}
export const PROFIL_KEY = 'medsoru_profil_v1';
const OLAY = 'medsoru:profil';

let ham: string | null | undefined;
let onb: Profil = {};
export const profilOku = (): Profil => {
  let h: string | null = null;
  try { h = localStorage.getItem(PROFIL_KEY); } catch { /* yok */ }
  if (h !== ham) { ham = h; try { onb = h ? JSON.parse(h) : {}; } catch { onb = {}; } }
  return onb;
};
export const profilYaz = (p: Profil) => {
  try { localStorage.setItem(PROFIL_KEY, JSON.stringify(p)); } catch { /* dolu */ }
  window.dispatchEvent(new Event(OLAY));
};
const abone = (f: () => void) => {
  const g = (e: Event) => { if (!(e instanceof StorageEvent) || e.key === PROFIL_KEY) f(); };
  window.addEventListener(OLAY, g); window.addEventListener('storage', g);
  return () => { window.removeEventListener(OLAY, g); window.removeEventListener('storage', g); };
};
export const useProfil = () => useSyncExternalStore(abone, profilOku, profilOku);

export const HEDEFLER: { ad: string; dk: number; soru: number }[] = [
  { ad: 'Hafif', dk: 20, soru: 20 },
  { ad: 'Düzenli', dk: 45, soru: 40 },
  { ad: 'Yoğun', dk: 90, soru: 80 },
  { ad: 'Sınav haftası', dk: 150, soru: 120 },
];

/** Tıp fakültesi olan üniversitelerden bir seçki; listede olmayan "Elle ekle" ile yazılır */
export const UNIVERSITELER: string[] = [
  'Karabük Üniversitesi', 'Ankara Üniversitesi', 'Hacettepe Üniversitesi', 'Gazi Üniversitesi', 'Ankara Yıldırım Beyazıt Üniversitesi',
  'İstanbul Üniversitesi', 'İstanbul Üniversitesi-Cerrahpaşa', 'Marmara Üniversitesi', 'Sağlık Bilimleri Üniversitesi',
  'Ege Üniversitesi', 'Dokuz Eylül Üniversitesi', 'İzmir Katip Çelebi Üniversitesi', 'Akdeniz Üniversitesi', 'Uludağ Üniversitesi',
  'Erciyes Üniversitesi', 'Selçuk Üniversitesi', 'Necmettin Erbakan Üniversitesi', 'Atatürk Üniversitesi', 'Ondokuz Mayıs Üniversitesi',
  'Karadeniz Teknik Üniversitesi', 'Çukurova Üniversitesi', 'Dicle Üniversitesi', 'Fırat Üniversitesi', 'İnönü Üniversitesi',
  'Pamukkale Üniversitesi', 'Eskişehir Osmangazi Üniversitesi', 'Kocaeli Üniversitesi', 'Sakarya Üniversitesi', 'Düzce Üniversitesi',
  'Bolu Abant İzzet Baysal Üniversitesi', 'Zonguldak Bülent Ecevit Üniversitesi', 'Trakya Üniversitesi', 'Süleyman Demirel Üniversitesi',
  'Mersin Üniversitesi', 'Gaziantep Üniversitesi', 'Sivas Cumhuriyet Üniversitesi', 'Tokat Gaziosmanpaşa Üniversitesi',
  'Kırıkkale Üniversitesi', 'Hitit Üniversitesi', 'Kastamonu Üniversitesi', 'Çankırı Karatekin Üniversitesi', 'Recep Tayyip Erdoğan Üniversitesi',
  'Ordu Üniversitesi', 'Giresun Üniversitesi', 'Van Yüzüncü Yıl Üniversitesi', 'Muğla Sıtkı Koçman Üniversitesi', 'Manisa Celal Bayar Üniversitesi',
  'Aydın Adnan Menderes Üniversitesi', 'Balıkesir Üniversitesi', 'Çanakkale Onsekiz Mart Üniversitesi', 'Tekirdağ Namık Kemal Üniversitesi',
  'Afyonkarahisar Sağlık Bilimleri Üniversitesi', 'Kütahya Sağlık Bilimleri Üniversitesi', 'Hatay Mustafa Kemal Üniversitesi',
  'Kahramanmaraş Sütçü İmam Üniversitesi', 'Malatya Turgut Özal Üniversitesi', 'Harran Üniversitesi', 'Bezmiâlem Vakıf Üniversitesi',
  'Başkent Üniversitesi', 'Koç Üniversitesi', 'Acıbadem Mehmet Ali Aydınlar Üniversitesi', 'Yeditepe Üniversitesi', 'Medipol Üniversitesi',
];
