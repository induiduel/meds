# Çıkmış soru tekrar analizi (v1, 2026-10-14)

Çalışma alanı `../../meds_temp/tekrar_analizi/` (betikler oradan çalışır; buradakiler arşiv kopyası).
Kural: yalnız aynı yıl + aynı kurul olduğu kesin kopyalar `birlestirmeler.json`'da birleştirilir; kurul+final ve farklı yıllar
gerçek tekrar (similarPastQuestions bandı); belirsizler birleştirilmez.

| Adım | Betik |
|---|---|
| Metin sürümleri | 01_cikar.py |
| Aday çiftler (TF-IDF + rapidfuzz) | 02_aday.py |
| Kaynak bölümleri + örtüşme | 03_bolum.py |
| Sınav kimliği (yıl/sınav/kesinlik) | 04_birim.py |
| Kural sınıflaması | 05_cift_sinifla.py |
| İnceleme partileri (alt ajan) | 06_paket.py, TALIMAT_kopya_inceleme.md, dogrula_kopya.py |
| Kısıtlı kümeleme, tekrar aileleri | 07_grupla.py |
| Uygulama (--yaz) | 08_uygula.py |
| Konu→özet haritası, özet→PDF | 11_ozet_harita.py, 14_ozet_pdf.py |
| Soru ilişki dizini | 12_soru_iliski.py |
| Cevap↔özet adayları + anlamsal inceleme | 13_ozet_aday.py, 15_anlamsal_paket.py, TALIMAT_ozet_anlamsal.md, dogrula_ozet.py |
| İlişki + özet kanıtı yazımı (--yaz) | 16_uygula_iliski.py |
| Varlık grafiği | 20_varlik.py → meds_database_v2/iliski/ |
