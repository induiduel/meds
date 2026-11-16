/**
 * Veri bütünlüğü günlüğü (sunucu tarafı).
 * Budama freni, boşla ezme reddi, yedek temizliği gibi veri olayları `data/gunluk/veri-YYYY-MM.jsonl`
 * dosyasına tek satır JSON olarak eklenir. Asla fırlatmaz; günlük yazılamazsa yalnız konsola düşer.
 * Dosya 20 MB'ı geçince `.1` adıyla döndürülür (önceki `.1` ezilir).
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

export type VeriSeviye = 'bilgi' | 'uyari' | 'hata';

const BURASI = path.dirname(fileURLToPath(import.meta.url));
// src/services → proje kökü/data
const GUNLUK_DIR = path.resolve(BURASI, '..', '..', 'data', 'gunluk');
const TAVAN = 20 * 1024 * 1024;

export function veriOlayi(seviye: VeriSeviye, kaynak: string, mesaj: string, ek?: object): void {
  try {
    if (seviye === 'uyari') console.warn(`[veri:${kaynak}] ${mesaj}`, ek ?? '');
    else if (seviye === 'hata') console.error(`[veri:${kaynak}] ${mesaj}`, ek ?? '');
  } catch { /* konsol bile yoksa sessiz */ }
  try {
    const simdi = new Date();
    const ay = `${simdi.getFullYear()}-${String(simdi.getMonth() + 1).padStart(2, '0')}`;
    fs.mkdirSync(GUNLUK_DIR, { recursive: true });
    const dosya = path.join(GUNLUK_DIR, `veri-${ay}.jsonl`);
    try {
      if (fs.statSync(dosya).size > TAVAN) fs.renameSync(dosya, `${dosya}.1`);
    } catch { /* dosya yok */ }
    const satir = JSON.stringify({ zaman: simdi.toISOString(), seviye, kaynak, mesaj, ...(ek ? { ek } : {}) });
    fs.appendFileSync(dosya, satir + '\n', 'utf8');
  } catch (e: any) {
    try { console.warn('[veriGunlugu] günlük yazılamadı:', e?.message || e); } catch { /* yok */ }
  }
}

/**
 * Genel ekleyici: `data/gunluk/<onEk>-YYYY-MM.jsonl` dosyasına tek satır JSON ekler (ör. onEk 'vitals').
 * Aynı 20 MB döndürme kuralı; asla fırlatmaz. Önek yalnız [a-z0-9-] olabilir.
 */
export function gunlugeEkle(dosyaOnEki: string, kayit: object): void {
  try {
    if (!/^[a-z0-9-]{1,32}$/.test(dosyaOnEki)) return;
    const simdi = new Date();
    const ay = `${simdi.getFullYear()}-${String(simdi.getMonth() + 1).padStart(2, '0')}`;
    fs.mkdirSync(GUNLUK_DIR, { recursive: true });
    const dosya = path.join(GUNLUK_DIR, `${dosyaOnEki}-${ay}.jsonl`);
    try {
      if (fs.statSync(dosya).size > TAVAN) fs.renameSync(dosya, `${dosya}.1`);
    } catch { /* dosya yok */ }
    fs.appendFileSync(dosya, JSON.stringify(kayit) + '\n', 'utf8');
  } catch (e: any) {
    try { console.warn('[veriGunlugu] günlük yazılamadı:', e?.message || e); } catch { /* yok */ }
  }
}
