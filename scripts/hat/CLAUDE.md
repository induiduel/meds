# scripts/hat/ — içerik hattının orkestrasyonu

- `tam_hat/` — içerik üretiminin TEK hattı: `kosucu.py` (giriş), `mod.py` (katman sırası, tam/tasarruf), `baglam.py` (read-once `baglam/`),
  `hazirlik.py` (E0), `ders_kilit.py` (atomik ders kilidi), `kural_secici.py`, kapılar (`anlatim_kapi.py`, `kaynak_kapisi.py`, `ornek_soru_kapi.py`), `dis_ajan/`.
- `takvim/` aktif kurul · `dersler/` ders kayıt defteri · `onem/` · `oncelikli_dersler/` · `olasi_soru/` · `paket/` (.medspak) · `quiz_motoru/` (quiz KAPALI).

## Kurallar
- Giriş: `python3 scripts/hat/tam_hat/kosucu.py <klasör> --ders <key> --mod <tam|tasarruf>`; sırayı yalnız `mod.py` verir.
- Aşamalar `baglam/`'ı okur; ham slaytı/şablonu tekrar tarama (`docs/TAM_HAT_HIZLI_AKIS.md` §0.0).
- Alt ajana yalnız `python3 scripts/hat/tam_hat/kural_secici.py --oku <aşama>` listesi verilir.
- LLM çağıran her betik `otomasyon/llm_kilit.py` arkasında (`MEDS_LLM_ELLE=1` yoksa çıkış 75); zamanlayıcı kurma yok (AGENTS kural 20).
- Kök `scripts/kok.py` ile; `parents[N]` yasak (D2).
- Ayrıntı: `docs/KURUL_OTOMASYON_EL_KITABI.md`, `docs/KURUL2_DERS_STANDARDI.md`, `scripts/HARITA.md`.
