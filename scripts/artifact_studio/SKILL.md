---
name: artifact-studyo
description: Yerel artifact stüdyosu — bir rapor, pano, özet ya da veri görselleştirmesi istendiğinde JSON reçete yazıp tek dosyalık, çevrimdışı HTML artifact üretir ve önizleme bölmesinde açar. Claude'un bulut "Artifact" özelliği 3P geçit kipinde çalışmadığı için eşdeğeridir.
---

# Artifact stüdyosu

Kullanıcı "artifact", "pano", "rapor sayfası", "tek sayfalık özet", "görsel özet" ya da
"bunu güzel bir sayfa olarak göster" derse bu yolu kullan. Çıktı; tek HTML dosyası, dış istek yok,
tema düğmesi ve yazdırma düğmesi olan bir sayfadır.

## Akış

1. **İçeriği topla.** Yalnız eldeki gerçek veriyi kullan; sayı, tarih, alıntı uydurma. Kaynağı
   (`kaynak` alanı) yaz. Veri yoksa kutuyu boş bırakma, o kutuyu hiç koyma.
2. **Reçete yaz.** JSON dosyası: `meds/scripts/artifact_studio/recete-<konu>.json`.
   Şema için: `python3 meds/scripts/artifact_studio/studyo.py --sema`
   Örnek için: `meds/scripts/artifact_studio/ornek.json`
3. **Üret.**
   ```bash
   python3 meds/scripts/artifact_studio/studyo.py meds/scripts/artifact_studio/recete-<konu>.json
   ```
   Komut çıktı yolu yazar (`scripts/artifact_studio/cikti/<ad>.html`).
4. **Aç.** `.claude/launch.json` içindeki `artifact-studyo` sunucusunu `preview_start` ile başlat;
   `preview_eval` ile `window.location = "<dosya>.html"` yap ya da doğrudan dosya yolunu aç.
   Kullanıcıya ekran görüntüsüyle birlikte göster.
5. **Düzeltme.** Reçeteyi düzenle, yeniden üret — HTML'e elle dokunma (üretilen dosya ezilir).

## Reçete

```json
{
  "baslik": "sayfa başlığı",
  "altbaslik": "tek satır alt başlık",
  "etiket": "üst bilgi (kaynak/tarih)",
  "tema": "acik | koyu",
  "vurgu": "#2f6f4f",
  "kutular": [ ... ]
}
```

Kutu türleri (`genislik`: `tam` | `yarim` | `dar`):

| tür | alanlar |
|---|---|
| `metrik` | `etiket`, `deger`, `birim`, `degisim`, `yon` (`artis`/`azalis`/`notr`), `alt` |
| `metin` | `baslik`, `govde`, `maddeler[]` |
| `grafik` | `baslik`, `tip` (`cizgi`/`sutun`), `etiketler[]`, `seriler[{ad, renk?, eksen?, degerler[]}]`, `kaynak` |
| `tablo` | `baslik`, `basliklar[]`, `satirlar[[...]]`, `kaynak` |
| `not` | `tur2` (`uyari`/`bilgi`/`basari`), `baslik`, `govde` |
| `alinti` | `govde`, `baslik` (kaynak kişi) |
| `kod` | `baslik`, `kod` |
| `ayrac` | — |

## Kurallar

- Türkçe yaz; ekran metni kısa, cümleler tam.
- Bir sayfada 1 başlık, 2–4 metrik, 1–2 grafik, 1 tablo yeterli; kalabalık yapma.
- Sütun grafiği sıfır tabanından başlar (betik ayarlar); yüzde serilerinde `birim: "%"` kullan.
- Büyüklükleri çok farklı iki seriyi (ör. 0–5 ders, 40–96 soru) aynı eksende gösterme: ikinci seriye
  `"eksen": "sag"` ver, sağ eksende ölçeklenir.
- Renk körlüğü: seri renkleri varsayılan paletten gelir, elle renk vermeyi gereksiz yere yapma.
- Dış görsel, yazı tipi, CDN kullanılmaz — artifact çevrimdışı da açılır.
- Biçimlendirici "süs" değil: kartlar taranabilir olmalı, sayılar hizalı, kaynak görünür.
- Çıktıyı `meds/scripts/artifact_studio/cikti/` dışına yazma (sunucu orayı gösterir).
