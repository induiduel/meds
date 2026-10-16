# Patoloji — Sınav İçin En Önemliler (100 puan) — alt ajan talimatı

Çalışma klasörü: `/home/indu/medsor/meds_temp/patoloji_onem/`

Kullanıcının kuralları (KESİN):
- **Tek kaynak ders PDF'i.** `pdf_metin/<kod>.md` = Kurul 1 Tıbbi Patoloji ders PDF'inin sayfa sayfa metni (`=== SAYFA n ===`).
  **PDF'te olmayan hiçbir bilgi yazılmaz** — kendi tıp bilgini, kitap bilgisini, başka ders notunu EKLEME. PDF'teki ifadeyi
  sadeleştirebilir, Türkçesini düzeltebilir, kısaltabilirsin; yeni olgu/sayı/oran/terim ekleyemezsin.
- **Sınava yönelik:** yalnız sınavda sorulabilecek bilgi (tanım, en sık, karakteristik bulgu, ayırıcı özellik, sayı/eşik, eşleşme,
  sınıflama, mekanizma, klasik tuzak). Tarihçe, slayt başlığı, genel giriş cümlesi, "teşekkürler" vb. YOK.
- **Özet niteliğinde, basit, hap bilgi:** her madde tek satırlık tek cümle (`bilgi`, en çok 30 kelime) ya da tek cümle + en çok 4 kısa alt madde (`alt`).
  Anahtar terimleri `**kalın**` yaz. Uzun anlatım yalnız `detay`'da.
- **100 puan ölçeği:** her maddeye 0–100 arası `puan` ver (sınavda sorulma olasılığı × önemi). Bantlar 10'ar puan: 90–100, 80–89, 70–79,
  60–69, 50–59, (40–49 …). En önemliden başla; 90–100 bandı dersin "olmazsa olmaz" çekirdeğidir.
  Puan ipuçları: çıkmış soruda sorulmuş (aşağıdaki aday liste) → yüksek; slaytta "en sık / en önemli / karakteristik / patognomonik /
  tanı koydurucu / dikkat / önemli" vurgusu, büyük harf/tekrar → yüksek; ayrıntı/istisna → düşük.

## Girdi
- `partiler/<P>.json`: `[{kod, ad, pdf_metin: "pdf_metin/<kod>.md", cikmis_adaylari: [{id, sinav, kok, secenekler, dogru, konu}]}]`
  `cikmis_adaylari` bu derse bağlanmış çıkmış sorular — bazıları başka konuya ait olabilir; yalnız gerçekten o maddeyi soranı bağla.

## Çıktı — `cikti/<kod>.json` (her ders AYRI dosya)
```json
{
  "kod": "07", "baslik": "Akut Enflamasyon", "pdf": "7)Akut Enflamasyon.pdf",
  "ozet": "Dersin 2–3 cümlelik özeti (PDF'ten).",
  "neden_onemli": "Bu dersin sınav açısından önemi: kaç çıkmış soru, hangi konular tekrar tekrar soruluyor (1–3 cümle).",
  "maddeler": [
    {
      "id": "07-01", "puan": 97,
      "baslik": "Akut enflamasyonun ana hücresi",
      "bilgi": "Akut enflamasyonda dokuya ilk ve en çok gelen hücre **nötrofildir**.",
      "alt": [],
      "tur": "en_sik",
      "alinti": [{"sayfa": 12, "metin": "PDF'ten BİREBİR 4–30 kelime"}],
      "neden": "Neden önemli — 1 cümle (ör. '2020-21 ve 2024-25'te soruldu', 'slaytta vurgulu', 'klasik çeldirici: makrofaj').",
      "detay": "- **Başlık:** açıklama\n- **…:** …  (60–180 kelime, yalnız PDF içeriği, maddeli)",
      "ornek_soru": {"kok": "…?", "secenekler": {"A": "…", "B": "…", "C": "…", "D": "…", "E": "…"}, "dogru": "C",
                     "aciklama": "1–2 cümle; çeldiriciler PDF'teki komşu kavramlardan"},
      "cikmis": ["k1-2024-2025-q050"]
    }
  ]
}
```
- `tur`: `tanim` | `en_sik` | `karakteristik` | `sayi` | `eslesme` | `mekanizma` | `siniflama` | `tuzak` | `tani_tedavi`.
- Madde sayısı PDF yoğunluğuyla orantılı: **20–45** (kısa ders ~20, uzun ders ~40). 90–100 bandında 4–8 madde; her bantta en az 2 madde
  (90–100 … 50–59). Aynı bilgi iki kez yazılmaz.
- `alinti`: 1–3 öge; `metin` ilgili sayfadan BİREBİR (büyük/küçük harf, satır sonu, madde işareti farkı önemsiz). `sayfa` doğru olmalı (±1).
- `ornek_soru`: puanı **≥70** olan her maddede ZORUNLU (diğerlerinde isteğe bağlı). 5 şık, tek doğru, kök "?" ile biter; doğru cevap ve
  çeldiriciler PDF'te geçen kavramlardan. Çıkmış soruyu kopyalama, kendi sorunu yaz.
- `cikmis`: yalnız aday listesinden, o maddeyi doğrudan soran soruların id'leri (yoksa `[]`).
- `bilgi`/`alt`'taki her sayı (yüzde, yaş, süre, oran) PDF metninde geçmelidir.

## Bitiş
Her ders için `python3 araclar/dogrula.py cikti/<kod>.json` → **0 HATA**. Uyarıları gözden geçir.
Yerel GPU/LLM yok; yalnız `cikti/` altına yaz (geçici betikler `/tmp/claude-1000/patoloji_<P>/` altında, başka ajanlarla karışmasın).
Son mesajında kısa özet: ders başına madde sayısı ve bant dağılımı, bağlanan çıkmış soru sayısı, PDF'te belirsiz/okunaksız bulduğun yerler.
