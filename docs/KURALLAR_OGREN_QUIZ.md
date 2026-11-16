# Öğren Destesi ve Quiz Kuralları (AGENTS.md'den taşındı, 2026-11-16)

> Bu kurallar **bağlayıcıdır** ama şu an etkin olmayan katmanlara aittir: Öğren destesi ASKIDA (AGENTS kural 22, 2026-11-02),
> Quiz üretimi KAPALI (kural 19, 2026-11-07). Kullanıcı bu katmanları yeniden açarsa ya da Öğren destesine / quiz koduna
> dokunuluyorsa bu belge okunur. Metin AGENTS.md'den **kelimesi kelimesine** taşındı; numaralar korunur (başka belgelerdeki
> "kural 7", "kural 19" atıfları buraya işaret eder). Amaç: her oturumda okunan AGENTS.md'yi inceltmek (Faz 4).

5. **Eş Zamanlı Senkronizasyon:**
   - Tek doğruluk kaynağı `meds/src/data/interactive_learning_decks.json`'dur; içerik yalnız buraya yazılır. `meds/src/data/decks/items/<id>.json` derlemede (`splitLearningDecks`) kaynaktan üretilir; dışa aktarım paketleri (`meds_export/deste_paketleri/<id>/`: deck.json, deck.md, flashcards_anki.txt) `npm run decks:packages` ile yeniden üretilir. İkisine elle yazılmaz. Slayt gövdesindeki anlatım asla boş (`""`) bırakılmamalıdır.

6. **Örnek Soru & Çıkmış Soru Gösteriminin Kaldırılması:**
   - Etkileşimli öğrenim (Öğren) modülünde ve deste yapılarında örnek soru, çıkmış soru ya da `relatedQuestions` gösterimi tamamen kaldırılmıştır. Slayt içi soru blokları ve paneldeki soru sekmesi gösterilmez.

7. **Tüm Etkileşimli Modellerde Katı Kronoloji ve Sıfır İleriye Sızıntı Kuralı (KESİNLİKLE ZORUNLU):**
   - Etkileşimli öğrenimdeki **11 modelin tümü** (`micro_quiz`, `cloze_masking`, `interactive_table`, `before_after_slider`, `branching_logic`, `causal_chain`, `active_recall`, `spot_the_lie`, `swipe_matching`, `feature_bidding`, `venn_grid`) bu kurala tabidir.
   - **Geriye Dönük / Anlık Bilgi Prensibi:** Bir slayttaki herhangi bir etkileşimli ögenin konusu, soru kökü, doğru cevabı, çeldiricileri, önermeleri, eşleme kartları, çapraz tablo kriterleri, vaka senaryosu veya gizli terimi **YALNIZCA o slayt ve o slayttan önceki slaytlarda işlenmiş bilgilerle** oluşturulabilir.
   - İleriki adımlarda (örneğin 25. slayttaki bir etkileşim için 26-100. slaytlarda) anlatılacak hiçbir terim, hastalık, mekanizma, ilaç veya bilgi etkileşimlere dahil edilemez. Kullanıcı henüz okuyup öğrenmediği bir bilginin sorusu, vakası, boşluk doldurması, önermesi, kartı veya tablosuyla **ASLA karşılaşamaz**.
   - **Karşılaştırma Modelleri (`before_after_slider`, `interactive_table`, `venn_grid`, `swipe_matching`):** Karşılaştırılan her iki taraf/hastalık/kategori de o slayta kadar işlenmiş olmalıdır. Henüz anlatılmamış bir hastalıkla erken karşılaştırma yapılamaz.
   - **Tekrar Sayfaları (Checkpoint) Kapsam Sınırı:** Bir Checkpoint slaytı (`[TEKRAR SAYFASI - CHECKPOINT n]`) **YALNIZCA kendi bölümünde (veya önceki bölümlerde) işlenmiş kazanımları** pekiştirebilir. Sonraki bölümlerin ögeleri (tablo, vaka, zincir) checkpoint sayfalarına erken eklenemez.

8. **İn-Situ Boşluk Doldurma ve İpucu Sızıntısı Yasağı:**
   - `cloze_masking` ögelerindeki cümle ve gizlenen terim (`maskedTerm`), kural olarak o slaytın kendi anlatım metninde (`synthesisNarrative` veya `content`) doğrudan yer alan temel bir bilgiyi pekiştirmelidir; slaytın konusuyla alakasız veya başka derslerden/bölümlerden kopyalanmış kopuk cümleler kullanılamaz.
   - İpucu (`hint`), cevabın hiçbir kelimesini, kökünü veya sayısını içeremez (`leaks(hint, answer) == False`).

9. **Adım Başına Öge Yoğunluğu (4-6 Kuralı):**
   - Her slaytta (checkpoint dahil) **4 ila 6 interaktif öge** kullanılır; tek tipe yığılma yapılmaz, 11 model dengeli dağıtılır.
   - Her adımda **en fazla 1 adet mekanizma zinciri** (`causal_chain`) olabilir; ek mekanizma pekiştirmesi tablo, karşılaştırma veya hatırlama kartıyla yapılır.
   - **Zorluk seviyesi orta-zor:** Sorular ezber-tanıma değil mekanizma/ayırıcı-tanı/muhakeme ölçer; her soruda en az 2 güçlü çeldirici öğretilmiş komşu kavramlardan kurulur, tuzaklar klasik sınav çeldiricilerinden seçilir, açıklamalar fizyopatolojik gerekçelidir.
   - `spot_the_lie` ögelerinde 3-4 önerme + tam 1 tuzak (`isLie: true`) + her önermede gerekçeli açıklama zorunludur; `swipe_matching` kartlarındaki her kart öğretilmiş bir kavrama aittir; `venn_grid` kriterleri (`A`/`B`/`both`/`neither`) yalnızca öğrenilmiş kutupları karşılaştırır.

9b. **Ders Sonu Oyunları (yeni derslerde ZORUNLU, rehber §5.14):**
   - Yeni üretilen her destenin SON slaytı `[OYUN SAYFASI] Ders Sonu Oyunları: <konu>` + `isGameFinale: true` olur; içinde yalnız `sequence_order`, `estimate_slider`, `perturbation`, `fix_the_text` (dördü de, toplam 4–6) bulunur. Bu dört tür başka slaytta kullanılmaz.
   - Doğrulama: `python3 meds/scripts/validate_learning_decks.py deck.json --oyun-zorunlu` → 0 HATA.

19. **Otomatik Quiz ve Aktif Geri Çağırma (Active Recall) Hattı (kullanıcı kararı 2026-10-26):**
   - ⛔ **Quiz üretimi KAPALI (kullanıcı kararı 2026-11-07: "quiz çok fazla oluşturuluyor, quiz oluşturmayı kapat"):** tam içerik işçisi ve dış ajanlar aksi söylenene kadar `quiz_havuzu.json` ÜRETMEZ; katman "atlandı — kullanıcı kararı" diye raporlanır, eksikliği dersi tamamlanmamış saymaz. `atomik_bilgi_envanteri.json` (ders paketi/önem için) üretilmeye devam eder. Ders içerik paketindeki mini `quiz` sayfası (`ders_icerik_uret.py`) bu yasağın dışındadır. Aşağıdaki maddeler yalnız kullanıcı quiz'i açıkça yeniden isterse uygulanır.
   - **Sıralı İş Akışı ve Öncelik Kilidi:** Drive'dan yeni ders materyali geldiğinde Sesli Ders (Audio Lesson) süreci tamamlanmadan (`COMPLETED`) Quiz üretim ajanları KESİNLİKLE tetiklenemez.
   - **Örnek soru sayısı (2026-10-27; bundan sonra işçiye verilen her ders/slayt dosyası için):** her derste önem listesinin tamamı + diğer ayrıntı kapsamın ~%40'ı örnek soruya çevrilir; toplam 50'yi aşar, 100'ü geçmez (`KURUL2_DERS_STANDARDI.md` §10.8).
   - **Kapsam (kullanıcı kararı 2026-10-27):** Quiz üretimi HER ders için aktiftir (eski Farmakoloji kilidi kalktı); yeni her derste atomik envanterden `quiz_havuzu.json` da üretilir (kural 21/22 katmanı). Kod ders-bağımsızdır (`kapsam.py`).
   - **Single Source of Truth (İşlem Tekrarı Yasağı):** Sesli ders için çıkarılan kazanım ve çıkmış soru araştırması tekrar edilmez; ortak `atomik_bilgi_envanteri.json` her iki süreci besler. Kaynak dışına çıkmak (halüsinasyon) KESİNLİKLE YASAKTIR.
   - **2x Çapraz Sorgulama Kuralı:** $N$ atomik bilgi birimi $\rightarrow$ en az $2N$ özgün soru (1 pozitif `positive_direct` + 1 ters `negative_inverse`, `question_pair_id` ile bağlı).
   - **Active Recall ve Süre Standardı:** Sorular uzun paragraflardan arındırılmış, 5-15 saniyede okunup yanıtlanabilir, kısa ve net olmalıdır. Solo ve Multiplayer modları destekler.
   - **Batch Processing:** Token sınırına takılmamak ve yüzeyselleşmeyi önlemek için üretim alt başlık bazlı veya en fazla 25 atomik bilgi (50 soru) içeren partiler halinde döngüyle yapılır.
   - **Düşük Gecikmeli Realtime Standardı (<50 ms):** Multiplayer Quiz modunda gecikmeyi en aza indirmek için `/api/quiz/ws` üzerinden Native WebSocket, RAM içi oda yönetimi (in-memory state, 0 ms DB wait), soru ön yükleme (pre-fetching ile 0 ms render gecikmesi) ve NTP ping-pong tabanlı saat ofseti telafisi zorunludur (`docs/REALTIME_QUIZ_MIMARISI.md`).
   - **Kapı:** `python3 meds/scripts/hat/quiz_motoru/quiz_dogrula.py <quiz_dosyasi>` 0 HATA vermeden yayınlanamaz.

