# Sınav ayrımı v2 — prognoz ve tedavi SORULABİLİR (kullanıcı, 2026-10-16)

> ⚠️ **Türkçe üslup standardı (ZORUNLU, 2026-10-18):** metin doğal, eksiksiz ve anlaşılır Türkçe olur; çeviri mecaz ("imzası",
> "motoru", "freni") ve iç etiket ("Ayrım cümlesi:", "Akılda tut:", "Mantığı şudur:") YASAK. Ayrıntı: `meds/docs/TURKCE_USLUP_STANDARDI.md`.

Çalışma klasörü: `/home/indu/medsor/meds_temp/patoloji_onem/sinav/v2/` (PDF metni `../../pdf_metin/<kod>.md`).

Sınav kuralı (güncel, KESİN):
1. Resim/şekil ve tablolardan soru YOK (`kaynak` = `tablo` | `sekil` → sorulmaz). Bu sınıflama önceki turdan geliyor (`mevcut.kaynak`); değiştirme.
2. **Klinik bulgu** sorulmaz: belirti, semptom, fizik muayene bulgusu, başvuru şikâyeti, klinik tablo/sendromun klinik görünümü,
   görüntüleme bulgusu, laboratuvar bulgusu (hasta tetkik sonucu).
3. **Prognoz ve tedavi SORULABİLİR.** Prognoz (sağkalım, seyir, yanıt, mortalite, risk/ilerleme olasılığı) ve tedavi (ilaç, cerrahi,
   tedavi seçimi/etki mekanizması, tarama/korunma) maddeleri artık `klinik: false` ve sınava uygundur.
4. Her ders slaytından 1 soru; kod 15'ten 2 soru.

`partiler/<P>.json`: her ders için maddeler + önceki turun kararı (`mevcut` = {kaynak, klinik, not?}), `mevcut_adaylar`, `pt_ipucu`
(metinde prognoz/tedavi sözcükleri geçiyor — yalnız ipucu).

## Her madde için
- `kaynak`: önceki değer (değiştirme).
- `kategori`: `prognoz` | `tedavi` | `klinik` | `patoloji` (patoloji = morfoloji, mekanizma, tanım, sınıflama, etken, gen, epidemiyoloji, sayı…).
  Madde hem prognoz/tedavi hem patoloji içeriyorsa asıl sorulacak kısma göre seç. Klinik bulgu ile prognoz/tedavi karışıksa:
  sorulabilecek kısım prognoz/tedavi ise `prognoz`/`tedavi`.
- `klinik` = (`kategori == "klinik"`).

## Adaylar
Her ders için sınava uygun (`kaynak == metin` ve `kategori != klinik`) maddelerden 3–5 (kod 15: 5–7) sıralı aday; önceki sıralamayı
temel al, yalnız prognoz/tedavi maddesi artık güçlü bir adaysa (slaytta vurgulu, çıkmış sorusu var) sıralamaya kat. `gerekce` öğrenciye
dönük 1 cümle ("aday", "ipucu" yok).

## Çıktı — `cikti/<kod>.json`
```json
{"kod": "21", "maddeler": {"21-01": {"kaynak": "metin", "kategori": "patoloji", "klinik": false}, "21-09": {"kaynak": "metin", "kategori": "prognoz", "klinik": false}},
 "adaylar": [{"id": "21-02", "sira": 1, "gerekce": "…"}]}
```
Bitiş: her ders için `python3 dogrula.py cikti/<kod>.json` → 0 HATA. Yalnız `cikti/` altına yaz; geçici betikler `/tmp/claude-1000/sinavv2_<P>/`.
Son mesaj: ders başına prognoz/tedavi/klinik sayıları ve sıralamada değişen ders(ler).
