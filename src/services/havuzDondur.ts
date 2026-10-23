/**
 * Havuz dondurma: sınav günü öğrenci kayıtları yalnız toplanır, üzerinde hiçbir otomatik işlem yapılmaz
 * (kullanıcı kararı 2026-10-23). `data/havuz_dondur.json` içinde `{"dondur": true}` varken:
 *  - serbest metin ayrıştırma (Gemini) ve soru kaydına geri yazma durur (ham girdi yine `question_intake/girdiler.jsonl`e yazılır),
 *  - havuz kümeleme ve yapay zekâ birleştirmesi durur,
 *  - çift modeli öğrenmesi durur,
 *  - cihazdaki olası soru gece işi (`scripts/olasi_soru/gece.sh`) aynı dosyayı Oracle'dan okuyup çıkar.
 * Kayıt, oy, yorum, ham soru defteri ve meds-pg yansıtması etkilenmez. Kaldırmak: dosyayı sil ya da `dondur: false`.
 * Dosya her istekte değil 5 sn'de bir okunur; sunucu yeniden başlatılmadan açılıp kapanır.
 */
import fs from 'fs';
import path from 'path';

let file = '';
let cache = { at: 0, value: false };

export function havuzDondurDosyasi(dataDir: string) {
  file = path.join(dataDir, 'havuz_dondur.json');
  cache = { at: 0, value: false };
}

export function havuzDonduruldu(): boolean {
  if (!file) return false;
  const now = Date.now();
  if (now - cache.at < 5_000) return cache.value;
  let value = false;
  try { value = JSON.parse(fs.readFileSync(file, 'utf8'))?.dondur === true; } catch { value = false; }
  if (value !== cache.value && cache.at) console.log(`[Havuz] otomatik işleme ${value ? 'donduruldu' : 'yeniden açıldı'}`);
  cache = { at: now, value };
  return value;
}
