-- 0001 · İçerik seti sürümleri (GELECEK_PLANLAMASI P3.3). Yalnız ekler.
-- Her ders ürünü (deste, sesli metin v2, önem, çözücü, asistan, olası soru …) bir satır: hangi kaynaktan (kaynak_sha),
-- hangi sürümle, ne zaman üretildi. Kaynak değişince üretici yeni sürüm yazar; istemci "bu ders güncellendi" gösterebilir.
CREATE TABLE IF NOT EXISTS icerik_setleri (
  kimlik      text NOT NULL,              -- k2-07 (ders) ya da k1 (kurul geneli, ör. olası sorular)
  tur         text NOT NULL,              -- deste | sesli_v2 | onem | cozucu | asistan | olasi_soru | onem_haritasi
  surum       integer NOT NULL DEFAULT 1,
  kurul       smallint,
  kaynak_sha  text,                       -- girdinin karması (kaynak.md / yuvalar.json parmak izi)
  yol         text,                       -- üretilen dosyanın göreli yolu
  ozet        jsonb NOT NULL DEFAULT '{}'::jsonb,  -- sayılar: madde, soru, cümle, ses …
  uretildi    timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (kimlik, tur, surum)
);
CREATE INDEX IF NOT EXISTS icerik_setleri_kurul_tur ON icerik_setleri (kurul, tur);
CREATE OR REPLACE VIEW icerik_setleri_son AS
  SELECT DISTINCT ON (kimlik, tur) * FROM icerik_setleri ORDER BY kimlik, tur, surum DESC;
