# Patoloji Soru İşçisi — yazar/denetçi talimatı (hocanın üslubuna bağlı)

**Önce oku (ZORUNLU):** `docs/PATOLOJI_HOCA_SORU_MANTIGI.md` v2 (seçim mantığı, 3 dönüşüm yöntemi, çeldirici türleri) ve `docs/PATOLOJI_SORU_ESLEME_TABLOSU.md` (30 gerçek soru–slayt örneği), `docs/SIK_ACIKLAMA_STANDARDI.md`,
`docs/TURKCE_USLUP_STANDARDI.md`, `docs/SORU_USLUBU.md`. Kural 20/22: LLM işi yalnız kullanıcının elle komutuyla (`MEDS_LLM_ELLE=1`); zamanlayıcı yok.

## Akış (tek ders)
1. `meds/.venv-ocr/bin/python -I scripts/patoloji_soru_isci/hazirla.py "<ders.pdf>" <ders klasörü>/patoloji_isci --n 12`
   → `paket.json` (önem adayları + çeldirici havuzu). Sarı dolgu YAPI ETİKETİdir (Ancak:/İstisna:/Sonuç:/Not:) — etiketin ALTINDAKİ satır puan alır; kalın, `***`, tekrar (≥2 yerde geçme) güçlü sinyaldir; başlık puan almaz.
   Biçim işaretli düz döküm: `dokum.py <pdf> <txt>` (⟦kırmızı⟧ ‹kalın› Y|sarı) — adayları ve eksikleri buradan gözle kontrol et.
2. **Vurgu gözden geçirme (yazar):** adayları PDF sayfalarıyla kontrol et; eksik çekirdek bilgi (ayırıcı bulgu, mekanizma sırası, eşleşme tablosu,
   "…ise ne olur" cümlesi, tek geçen ad/eponim) varsa `paket.json`'a `{id:"oNN", ...}` olarak ekle; gereksiz adayı sil. Genişlik kuralı: dersin çekirdek 3–5 noktası.
   Çıktı `vurgu.json` (yeni önem listesi; puan + `neden` + sayfa + birebir alıntı). Mevcut önem listesine (`*_onem`) dokunmadan ÖNERİ olarak sunulur.
3. **Soru yazımı (`sorular.json`):** her önem noktası (puan ≥ 60) için **≥2 soru, farklı kalıpta** (`dogrudan|bilesik|eslesme|sira|olumsuz|ters_ad|ters_yon|yanlis_bul`).
   - Ad/eponim noktasında biri `ters_ad`: olgu (kırmızı kısım) verilir, ad sorulur.
   - **Hocanın 3 dönüşümü:** kopya+çevirme (çeldirici = mutlaklaştırılmış/ters çevrilmiş aynı cümle), birleştirme (2–3 ardışık madde ya da iki slayt/kural+istisna tek şıkta), yön değiştirme (`ters_yon`: eski çıkmışta "X hangi etkende?" ise "etken X'te en tipik bulgu"). Her noktada biri birleştirme/kopya, biri ters yön/ad olsun. Çıkmış sorusu olan noktada ters yön ZORUNLU (çıkmış bankası: `data/pastQuestions.json`, konu araması).
   - Noktaların ~%15–20'sinde bir mantık adımı ileri (`cikarim:true`): doğru şık slayt bilgisinden bir çıkarımla bulunur; dayanak yine PDF'te olmalı.
   - Kök kısa (7–18 kelime), bağımsız; "en tipik / en olası / en karakteristik" kökleri %30–55; olumsuz kök ≤%15.
   - Şıklar %30–50 bileşik ("X + Y", "X → Y", "A: …; B: …"); **çeldirici bileşeni doğru şıkta yer değiştiren komşu kavramdır**.
   - 4 yanlışın ≥3'ü aynı dersin komşu kavramlarından (`ifade_havuzu`'ndan seç), `celdirici_kaynak`'a sayfaları yaz (≥3 sayfa); uydurma çeldirici yok.
   - Doğru şık en uzun olmaz; şık uzunlukları birbirine yakın. Doğru şıkkın konumu dengeli dağıtılır.
   - Her şık için 2–3 cümle açıklama (ne / ne işe yarar / bu soruda neden doğru-yanlış); "cevabı değil" yasak.
   - Yalnız ders PDF'inde olan bilgi; `kaynak{sayfa, metin}` birebir alıntı.
4. **Kapılar:** `python3 scripts/patoloji_soru_isci/dogrula.py sorular.json paket.json` → 0 HATA; ardından mevcut
   `scripts/tam_hat/soru_uslup.py`, `scripts/sik_aciklama.py`, `scripts/turkce_uslup.py`.
5. **Bağımsız denetçi (ayrı ajan, yazarın çıktısını görmeden PDF'ten):** her soruda tek doğru olduğunu, kaynağı ve çeldirici adilliğini doğrular → GEÇER/KALIR.
   Yalnız hatalı soru yeniden yazılır (tıbbi/kaynak hatasında tolerans yok).
6. Yayın: kullanıcı onayıyla ders `ornek_sorular`/`cikabilecek_sorular` katmanına eklenir (önce git, `onem`+1, `dagit.sh`).

## Yapma
- Sarı vurguya/başlığa bakarak önem verme. Kırmızıyı "önemli" sayma (slaytların ~%42'si kırmızı).
- Kaynak dışı bilgi, slayt/ders/hoca göndermeli kök, "hepsi/hiçbiri" şıkkı.
- Kurul 1 verisine toplu müdahale. Kurul 2 patoloji için ilk çıkmış gelince profili yeniden hesapla (`PATOLOJI_HOCA_SORU_MANTIGI.md` §5).
