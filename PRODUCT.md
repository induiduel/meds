# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- **Öğrenciler (birincil):** Karabük Üniversitesi Tıp Fakültesi Dönem 3 öğrencileri (`@ogr.karabuk.edu.tr`). İki ana anları var:
  - Kurul sınavından çıkar çıkmaz, çoğunlukla telefondan, hatırladıkları soru parçalarını (kök, şık, ipucu, cevap) hızlıca girerler.
  - Sınavlara hazırlanırken ders öğrenme ekranlarında çalışır, çıkmış soruları ve ezber kartlarını çözerler.
- **Yönetici (tek kişi):** Proje sahibi. `/manage` konsolunda taslakları eşler, soruları doğrular, veri hattını ve AI ajanlarını çalıştırır.
- Veride Dönem 1–5 içeriği de vardır, ancak hedef kitle Dönem 3'tür.

## Product Purpose

Dönem 3 kurul sınavları için kolektif soru havuzu ve öğrenme aracı. Öğrencilerin hatırladığı dağınık parçalar fakültenin kendi ders materyallerine (amfi slaytları, ders notları, özetler, amfi kayıtları) ve çıkmış sorulara dayanarak tam sorulara dönüştürülür; aynı veri interaktif ders öğrenme notlarını besler.

Başarı iki eşit hedeftir:
1. Her kurul sınavının soruları fakülte kaynaklarına dayalı ve doğrulanmış biçimde havuzda kurulur.
2. Öğrenci bu soru ve kaynaklarla dersi daha iyi öğrenir (öğren, çalış, ezber kartları, çıkmış sorular).

## Positioning

Genel bir soru bankası değil: sorular **bu fakültenin kendi ders materyallerine ve kendi çıkmış sorularına** dayanarak, öğrencilerin ortak hafızasından yeniden kurulur. Her kurulan soru dayandığı kaynağı (slayt sayfası, özet, çıkmış soru, amfi kaydı) gösterir.

## Operating Context

- Parça girişi sınav çıkışında, ayakta ve telefondan yapılır; tek kelimelik parça bile kabul edilir.
- Öğrenme ve çalışma telefon, tablet (kalemle işaretleme) ve bilgisayarda yapılır; uzun okuma oturumları olur.
- Kaynaklar Google Drive'dan iner, yerelde okunur ve doğrulanarak `meds_database`'e girer (bkz. `../PROJE_TANITIMI.md`).
- Arka uç yönetici bilgisayarında çalışır (Express, port 3000), Cloudflare tüneliyle dışarı açılır; ön yüz GitHub Pages'te de yayınlanır. Yönetim konsolu `manage.nofrostlife.com.tr/manage` adresindedir.
- Yönetici yerel AI ajanları (Ollama: medgemma, qwen3, qwen3-vl, deepseek-r1, bge-m3) ve bulut AI (Gemini → Groq) kullanır.

## Capabilities and Constraints

- Soru ekle (parça girişi, yazarken benzer çıkmış sorular ve kaynaklar), Öğren (slayt okuyucu, işaretleme, kendini sına), Sözlük, Ezber kartları, Çıkmış sorular, Soru havuzu, Çalış/Test, Sıralama, Ders özetleri, Ders notları, Soru haritası, A4 kitapçık, Ses kayıtları.
- Yönetim konsolu: gelen kutusu, tüm veriler, taslaklar, taslak stüdyosu (parçaları elle eşleme, AI ile dönüştürme), moderasyon, kullanıcılar, betikler, sistem, otomasyon.
- Kaynak dayanağı zorunludur: soru yazan ya da düzelten her özellik kaynakları bulur, isteme koyar ve kullanılan kaynakları gösterir. AI çıktısı kaynak sayılmaz.
- Arayüzün iki tasarım sürümü vardır: v3 (varsayılan) ve v2 (yedek); kullanıcı geçiş yapabilir.
- Açık konu: kimlik doğrulama zayıf (yönetici kontrolü başlık ve yerel IP'ye güveniyor).

## Brand Commitments

- Ad: **MedSoru**. Arayüz, hata mesajları ve AI çıktıları **tamamen Türkçe**.
- **Ücretsiz ve reklamsız.** Maliyet yerel AI ve ücretsiz anahtarlarla düşük tutulur.
- **AI çıktısı doğrulanmış sayılmaz:** AI'nın kurduğu soru "inceleniyor" durumunda kalır, kaynağıyla gösterilir; öğrenciye kesin bilgi gibi sunulmaz.
- **Telefon öncelikli.**
- Kullanıcının bağlayıcı tasarım beklentisi (kendi sözleriyle): tasarım anlaşılır, sade ve fonksiyonel olmalı; akıcı olmalı; tüm cihazlarda boyut sorunu yaşamadan kullanılabilmeli; minimalist olmalı. Metin vurguları ve betimlemeleri önemlidir. Ders öğrenme sayfaları daha sade, anlaşılır ve göz yormayan olmalıdır.

## Evidence on Hand

- Gerçek kaynaklar: fakülte amfi slaytları ve ders notları (`data/lecture_notes.json`, `meds_database/`), ders özetleri, çıkmış sorular, amfi kaydı transkriptleri.
- Gerçek kullanıcı verisi: kayıtlı öğrenciler, katkılar, sıralama (kişisel veri; tasarımlarda gerçek isim kullanılmaz).
- Yok: kullanıcı yorumları, başarı istatistikleri, sınav sonucu etkisi. Bunlar uydurulmaz.

## Product Principles

1. **Kaynak önce gelir.** Her soru ve bilgi, fakültenin kendi materyaline bağlanabildiği ölçüde değerlidir; bağ görünür kılınır.
2. **Parça yeter.** Katkı engeli en düşük düzeyde tutulur; tek kelime bile işe yarar.
3. **Kesinlik dürüstlüğü.** Doğrulanmamış, AI üretimi ya da belirsiz bilgi her zaman öyle etiketlenir.
4. **Öğrenmeye hizmet.** Havuz bir arşiv değil, öğrenme ekranlarını besleyen yakıttır.
5. **Sadelik.** Her ekranda tek ana iş; gerisi ihtiyaç anında belirir.

## Accessibility & Inclusion

- Uzun okuma oturumları için göz yormayan okuma ekranları, açık ve koyu tema.
- Telefon, tablet (kalem girdisi, avuç içi reddi) ve bilgisayarda taşmasız çalışma.
- Dokunma hedefleri parmakla kullanılabilir boyutta; klavye ile gezinme ve görünür odak.
- "Hareketi azalt" tercihine uyulur.
