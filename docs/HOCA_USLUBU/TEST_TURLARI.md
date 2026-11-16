# Hoca-tahmin test turları (2026-10-29) — 2026-27 Kurul 1 ile kör sınama

> Amaç: işçinin ders metninden "hocanın soracağı yerleri" ne kadar tutturduğunu 2026-27 sınavıyla ölçmek ve her turda rehberi/girdiyi iyileştirmek.
> Düzenek: `scripts/uretim/hoca_profili/` (`algoritmalar.py`, `karsilastir.py`, `tur_yonet.py`, `yargic.py`). Ham tur verisi: `meds_temp/hoca_profili_sinama/tur1…tur6/`.

## Düzenek (sızıntısız)
- 52 ders notu · 91 gerçek 2026-27 sorusu. Ders notları md5'e göre **geliştirme 30 ders/51 soru** ve **bekletilmiş 22 ders/40 soru** (ayarlamada hiç bakılmadı).
- Profil/gömme geçmiş çıkmışlardan, 2026-27 HARİÇ (`uslup_analiz.py --yeni-haric`); ders notlarında geçmiş yıllara ait "Çıkmış Sorular" bölümü var, bu yılın sorusu yok (kosinüs kontrolü: en yakın eşleşme ort. 0,53).
- **Kör ajan** (Sonnet; ders notu + profil + aday listesi + rehber; 2026-27 dosyalarını okuması yasak) ders başına K tahmin yazar.
- **Bağımsız yargıç ajanı** her 2026-27 sorusu için üç tahmin kümesini (LLM / algoritma ilk-K satır / rastgele K satır) **kör etiketle** puanlar: 2 = aynı bilgi (metin soruyu çözdürür), 1 = komşu, 0 = yok. Skor = puan 2 oranı ("sıkı"). Yargıç gürültüsü ≈ ±8 puan (aynı algoritma kümesi turlar arası %39–47 çıktı) → tek turdaki küçük farklara güvenme.

## Sonuç tablosu (sıkı skor)
| Tur | Küme | Tahmin/ders | LLM | Algoritma (aynı K) | Rastgele (aynı K) | Değişiklik |
|---|---|---|---|---|---|---|
| 1 | geliştirme | 8 | %37 | %39 | %12 | rehber v1, adaylar.json |
| 2 | geliştirme | 8 | %53 | %47 | %10 | v2: liste/ilaç/kural sınıfları (tur 1 kaçanlarının genel türleri) |
| 3 | geliştirme | 8 | %45 | %39 | %10 | v3: kesin tanımlar, kompakt adaylar.md, gürültü temizliği |
| 4 | geliştirme | 10–18 | %63 | %55 | %26 | v4: K ders uzunluğuna göre (kapsama), liste kuralı, profil→kota |
| **5** | **bekletilmiş** | 10–18 | **%62,5** | %25 | %12,5 | v5 kuralları; HİÇ ayarlanmamış 22 ders |
| 6 | geliştirme | 10–18 | **%69** | %49 | %20 | ders adı eşleme düzeltmesi (Patoloji/Farmakoloji profili artık yüksek güvenli) |

Okuma: (1) tek çalışma 8 tahminle ≈%45, 3 ayrı çalışmanın birleşimi %71 → **kapsama (K) belirleyici**; (2) bekletilmiş kümede LLM %62,5 ≈ geliştirmedeki %63 → rehber aşırı uyum yapmamış; (3) algoritma tek başına ders-içi satır sıralamada rastgeleden 2–3× iyi ama yargıç sıkı ölçütünde LLM'ye göre geride (bekletilmişte çok geride); (4) 14 soru (%27) üç turda da hiçbir yöntemle yakalanmadı: olumsuz kök + liste dışı eleman, ilaç imzası, sayısal eşik, klinik kural.

## Algoritma karşılaştırması (satır sıralama; altın satır isabeti, geliştirme/bekletilmiş ilk-%10 satır)
rastgele %10/%25 · uzunluk %59/%57 (etiket yanlılığı: altın satırlar uzun) · biçim %26/%38 · söz kalıbı %22/%33 · sözcük tekrarı %51/%47 · **bge-m3 anlamsal tekrar (geçmiş çıkmışa yakınlık) %49–57/%57–62** · hedef-cümle yakınlığı %41/%23 · TextRank %43/%35 · birleşik sıra ortalaması **%67–69/%65** · lojistik %67/%60. Elle etiketli 17 soruda (güvenilir etiket): birleşik ilk-10 %53, ilk-%10 %65 (rastgele %18/%23).
Sonuç: tek sinyal yok; **anlamsal tekrar + biçim + söz kalıbı birleşimi** en iyisi. Yapısal sinyaller (SPOT bölümü, dersin kendi çıkmış bölümü) ek getiri vermedi.

## Bulunan hatalar ve çözümü (H-kaydı özeti)
- **Ders adı uyuşmazlığı:** 2026-27 dosyası "Patoloji/Farmakoloji" derken çıkmış bankası "Tıbbi Patoloji/Farmakoloji" → profil `_genel`'e düşüyordu (güven düşük). Çözüm: `sinama_ortak.DERS_ESLE`; yeni ders ekleyen kod ders adını `uslup_analiz.DERS_ESLE` ile eşler.
- **Metrik yanlılığı:** çok satırlı kaynakta "en iyi pozitif" ölçütü rastgeleyi şişiriyordu → AUC ve tek-satır etiketine geçildi.
- **Sızıntı:** profil 2026-27'yi içeriyordu → sınama için ayrı sızıntısız profil.
- **Etiket yanlılığı:** otomatik altın satırlar uzun satırlara kayıyor; uzunluk tek başına güçlü görünüyor → elle etiketli alt küme ve yargıç ölçütüyle doğrulandı.

## Sınırlar (gizleme yok)
- 10 tur hedeflendi; **6 tur koşuldu** (4 geliştirme, 1 bekletilmiş, 1 düzeltme sonrası geliştirme). Kalan turlar yargıç gürültüsü (±8) altında kalacak kadar küçük kazanç beklentisiyle ve ~1,3 milyon alt ajan jetonu/tur maliyetiyle durduruldu; sürdürmek için `tur_yonet.py girdi 7` + aynı protokol.
- Test yalnız Kurul 1 (52 ders notu); Kurul 2+ için ilk gerçek sınav gelince aynı düzenek yeniden koşulmalı.
- Düzeltme (tur 6) bekletilmiş kümede yeniden ölçülmedi.
- "Yakalama" = tahmin listesinde sorunun bilgisinin bulunması; sınavda tam o soruyu soracağımız anlamına gelmez. Hocanın ders içi vurgusu (ses, işaret) bu testte yoktu; gerçek hatta ek sinyal olarak eklenir.

## Tur 7–9 (2026-10-29)

| Tur | Küme | Rehber | Ajan (sıkı) | Algoritma | Rastgele |
|---|---|---|---|---|---|
| 7 | geliştirme (30 ders, 51 soru) | v5 (değişmedi) | %68,6 | %51 | %23,5 |
| 8 | geliştirme | v6 | %80,4 | %51 | %23,5 |
| 9 | bekletilmiş (22 ders, 40 soru) | v6 | %75 | %37,5 | %20 |

- Tur 7 rehber değişmeden tekrarlandı: tur 6 ile aynı (%69) → tek tur gürültüsü ≈ ±8.
- v6 değişiklikleri (ajan geri bildirimi): kapalı `bilgi_turu` listesi, orta güven kuralı (yarı ders / yarı yerel), liste tavanı min(K/3,4), spot/gövde ve birleşik olguda satır, tek soruluk çıkmışta ters yön, farmakoloji kotası. Tur 8'de +12 puan (gürültünün üstünde), bekletilmişte %62,5 → %75.
- Dikkat: tur 8 aynı dersleri tur 7 ile kullandı (ajanlar tur 7 çıktısını görmedi ama dersler aynı); bağımsız doğrulama tur 9'dur. Tur 10 yapılmadı: kalan kazanım ±8 gürültünün altında.
- Algoritma çizgisi bekletilmişte %37,5: aday listesi rastgeleden iyi ama önemi ajan gerekçesi belirliyor.

## Tur 10–11: v7 denemesi (geri alındı)
- v7 = klinik yönetim aday sınıfı (E) + dışlanan eleman + alt tür kuralı (tur 8–9'da kaçırılan 20 sorudan türetildi; kaçırılanlar çoğunlukla tedavi/aşı/izlem ve listede olmayan elemanı soran olumsuz kökler).
- Sonuç: geliştirme %82,4 (algo %54,9, rastgele %27,5), bekletilmiş %65 (algo %37,5, rastgele %15). v6'ya göre ortalama %78 → %73,7: gürültü (±8) içinde, yarar kanıtlanmadı; kurallar kaçırılanlara uydurulduğu için bekletilmiş ölçüm zaten iyimser olurdu, yine de artmadı → rehber v6'ya döndürüldü, E sınıfı çıktıdan kapatıldı.
- Sonuç: v6 kararlı sürüm. Kalan ~%20–25 kaçırma (tedavi/aşı/izlem yönetim soruları, dışlanan eleman) tahmin sayısını artırmadan kapanmıyor; K'yi artırmak (kapsama) tek kanıtlı kaldıraç.
