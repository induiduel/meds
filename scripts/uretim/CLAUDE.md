# scripts/uretim/ — içerik üretimi

- Ders: `ders_isci/`, `sesli_anlatim/`, `ders_analizi/`, `ders_icerik/`, `ek_modul/` · Görsel: `cizim/`, `kroki/`, `ara_resim/`, `lottie/`
- Soru/çözücü: `spot_cozucu/`, `patoloji_cozucu/` (`cozucu_ses_gpu.sh`), `patoloji_soru_isci/`, `hoca_ara_soru/`, `sinav_spotlari/`
- Hoca/öğrenci: `hoca_profili/`, `hoca_vurgu/`, `ogrenci_onem/` · Kamp: `son_prova/`, `kamp/` · Arşiv dersleri `arsiv_25_26/` (CANLI üretim).

## Kurallar
- Yeni ders tam hattan yürür (`scripts/hat/tam_hat/kosucu.py`); burası aşamaların betikleridir.
- Kapılar 0 HATA: `sik_aciklama.py`, `turkce_uslup.py` (scripts kökü), `uretim/cizim/cizim_kapisi.py`, ilgili `dogrula.py`.
- LLM adımı `otomasyon/llm_kilit.py` arkasında (`MEDS_LLM_ELLE=1`); EMA sesi GPU istisnası `docs/GPU_KULLANIM.md`.
- Kök `scripts/kok.py` ile (`parents[N]` yasak); çalışma verisi `meds_temp/<modül>/`, git'e yalnız kod.
- **Ses (2026-11-16):** EMA'ya giden okunuş YALNIZ `ses_ortak/ses_metin.hazirla` (yol veriden: ders defteri/klasör adı → kurul); klip üretimi `ses_ortak/ses_klip` (`kbps`/`okunus` parametre; `E.KBPS`/`E.okunus.duzelt` ezmek YASAK). Klip karması formülüne dokunma.
- Ayrıntı: her klasörün `TALIMAT*.md`'si, `scripts/HARITA.md`, `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
