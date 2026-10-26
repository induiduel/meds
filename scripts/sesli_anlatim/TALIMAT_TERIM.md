# Talimat — Sesli ders PDF terim yardımcısı (`terim` adımı)

Çalışma klasöründe `sayfalar.md` (her slaytın metni, `## <dosya>:<sayfa>` başlıklı) ve `terimler.json` (doğrulanmış
sözlükten aday taslak) vardır. Görevin `terimler.json`'u son hâline getirmek.

## Seçim
Her slayt için öğrencinin takılabileceği sözcükleri seç (sayfa başına **en çok 8**, gereksizse hiç):
- `terim`: tıbbi terim (hastalık, yapı, süreç, ilaç sınıfı),
- `latince`: Latince/yabancı sözcük ve kalıp (ör. *in situ*, *corpus luteum*, *-itis* ekli adlar),
- `karisan`: sık karıştırılan terim — `f` alanına karıştırıldığı terimi yaz (ör. hiperplazi ↔ hipertrofi),
- `kisaltma`: kısaltma (açılımı + ne olduğu).
**Türkçe kökenli sözcükleri seçme** (gelişme, bilinç, ağrı, kanama, bozukluk, yetmezlik …; kapı HATA verir). Gündelik Türkçe sözcükleri, başlık kelimelerini ve aynı terimin tekrarlarını seçme. Aynı terim başka sayfada da
geçiyorsa her sayfada yeniden yazılabilir (öğrenci o sayfadadır).

## Açıklama (`a`)
- **1–2 cümle, 25–280 karakter**, basit ve net Türkçe; tanım + gerekiyorsa tek ayırt edici bilgi.
- Yalnız slaytta ve ders içeriğinde dayanağı olan bilgi; uydurma yok. `…`/`...` ile kesme yok, tam cümleyle bitir.
- `karisan` açıklaması farkı söyler ("Hipertrofi hücre boyutunun, hiperplazi hücre sayısının artışıdır.").
- Çeviri mecaz ve iç etiket yasak (`meds/docs/TURKCE_USLUP_STANDARDI.md`).

## Biçim
```json
{ "key": "<ders>", "s": { "0:12": [ { "t": "Metaplazi", "a": "…", "k": "terim" },
                                   { "t": "Hiperplazi", "a": "…", "k": "karisan", "f": "Hipertrofi" } ] } }
```
`t` slayttaki yazımla aynı olmalı (kapı kutuyu bu metinle bulur; Türkçe ek payı vardır).

## Kapı
`terim_sozlugu.py dogrula <key> terimler.json` **0 HATA** olana dek düzelt. Kapıyı gevşetme, terimi uydurma.
