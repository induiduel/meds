// MedSoru pipeline: ortak yollar. Akış: Drive -> downloads -> temp -> database
import path from 'path';
export const PROJECT_ROOT = process.env.MEDS_PROJECT_ROOT || '/home/indu/medsor';
export const DOWNLOADS_DIR = process.env.MEDS_DOWNLOADS_DIR || path.join(PROJECT_ROOT, 'meds_downloads');
export const TEMP_DIR = process.env.MEDS_TEMP_DIR || path.join(PROJECT_ROOT, 'meds_temp');
export const DATABASE_DIR = process.env.MEDS_DATABASE_DIR || path.join(PROJECT_ROOT, 'meds_database');

// Drive kök klasörleri (herkese açık; kimlik bilgisi gerekmez)
export const DRIVE_ROOTS = [
  { key: 'drive_root', name: 'Meds_Drive_Root', id: '1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W' },
  { key: 'cikmislar_k1_6_final', name: '1) Çıkmışlar (Kurul 1-6 & Final)', id: '18U1LZVvV0VROcWVQTDBeJYwdBWiEIVwS' },
  { key: 'cikmis_25_26_d3', name: '2) 25-26 Dönem 3 Çıkmışları', id: '1VJwhDITJWZFaaBTvMajnLUzII31r1GTp' },
  { key: 'donem3', name: '3) 3. Dönem', id: '1AZaRbCpIUKtv0t6sg3VaZHC42NmbrnB4' },
  { key: 'cikmis_sorular', name: '4) Çıkmış Sorular', id: '16ianUX4Nnl-dU9SZOSOgvDDuEaM1x6vZ' },
  { key: 'sinif3', name: '5) 3. Sınıf', id: '1FAqqW0iAeg3NNjkPBeY3zG9X4FXaJuVM' },
  { key: 'd3_cikmis_toplama', name: '6) Dönem 3 Çıkmış Toplama', id: '1QKbD3800KBa3AUWP8apMSiKCMV0jiA21' },
  { key: 'gecen_yil_d3', name: '7) Geçen Yıl Dönem 3 Kaynakları', id: '1X5bsCn74i_0wy_Zj8eX_AOCpDSGGMw0j' },
];
