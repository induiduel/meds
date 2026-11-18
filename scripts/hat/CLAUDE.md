# scripts/hat/ — içerik hattının orkestrasyonu

- `tam_hat/` — içerik üretiminin TEK hattı: `kosucu.py` (giriş), `mod.py` (katman sırası, tam/tasarruf), `baglam.py` (read-once `baglam/`),
  `hazirlik.py` (E0), `ders_kilit.py` (atomik ders kilidi), `kural_secici.py`, kapılar (`anlatim_kapi.py`, `kaynak_kapisi.py`, `ornek_soru_kapi.py`), `dis_ajan/`.
- `takvim/` aktif kurul · `dersler/` ders kayıt defteri · `onem/` · `oncelikli_dersler/` · `olasi_soru/` · `paket/` (.medspak) · `quiz_motoru/` (quiz KAPALI).

## Kurallar
- Giriş: `python3 scripts/hat/tam_hat/kosucu.py <klasör> --ders <key> --mod <tam|tasarruf>`; sırayı yalnız `mod.py` verir.
- Aşamalar `baglam/`'ı okur; ham slaytı/şablonu tekrar tarama (`docs/TAM_HAT_HIZLI_AKIS.md` §0.0).
- **Alt ajan TEK dosya okur (2026-11-17, H594):** `baglam/is_<katman>.md` (kural paketi + şema + veri) ya da `baglam/kural_<aşama>.md`
  (`baglam.py` üretir; `kural_secici.py --paket`). `--oku` listesi/`--ozet`/`sema.md`/dilimler ayrıca okutulmaz; denetçi `kural_denetci.md` okur.
- Elle bakmak için: `python3 scripts/hat/tam_hat/kural_secici.py --oku <aşama>` listesi + `--ozet <aşama>` (≤300 kelime);
  kapılı maddeler tek satırdır, tam metin `--tam <H no|aşama>`. `--denetle` madde kaybını da HATA sayar.
- `baglam/` dilimli: aşama yalnız kendi `kaynak_<atom|hoca|cikmis|uslup>.md` dilimini okur (`baglam.py` DILIM_ASAMA).
- LLM çağıran her betik `otomasyon/llm_kilit.py` arkasında (`MEDS_LLM_ELLE=1` yoksa çıkış 75); zamanlayıcı kurma yok (AGENTS kural 20).
- Katman manifesti: `tam_hat/manifest.py uret|goster|denetle|fark <key>` → `meds_database_v2/ders_bilgi/<key>/katman_manifest.json` (`manifest.json` bilgi deposunundur, ezilmez); kapıyı çalıştırmaz, `--kapi-sonucu katman=gecti|kaldi` işler.
- `hoca_kirp.py` (C6: döküm → slayt başına kırpık, LLM yok) · `iskelet.py` (C7: `baglam/iskelet_<aşama>.json`, `numarala`, `denetle`) · `kosucu.py --olc` (girdi ölçümü) · bağımlılık/paralel grup `mod.py BAGIMLILIK`.
- Kök `scripts/kok.py` ile; `parents[N]` yasak (D2).
- Ayrıntı: `docs/KURUL_OTOMASYON_EL_KITABI.md`, `docs/KURUL2_DERS_STANDARDI.md`, `scripts/HARITA.md`.
