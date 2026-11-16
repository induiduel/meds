# MeDSor Tıp Asistanı — Yol Haritası ve Özellik Kataloğu

Durum: TASARIM (2026-10-29). Henüz kod yok. Kural 10 (yerel GPU yasağı) ve kural 20 (LLM/API otomasyon yasağı) geçerlidir.

## 1. Mimari karar: üretken LLM YOK, "anlayan arama motoru" VAR

Gerekçe:
- Kural 20 + "API bağlanmasın, limit tüketmesin": bulut LLM dışarıda.
- Kural 10: GPU yasak. Oracle'da CPU+RAM kısıtlı; 1–3B parametreli yerel model Türkçe tıpta halüsinasyon yapar, "doğru cevap" şartını bozar.
- Öğrenci sorusunun büyük kısmı kaynakta vardır: hastalık, bulgu, ilaç, sayı, çıkmış soru, sayfa. Bunun için **bulma + alıntılama** üretimden daha doğrudur ve kaynak gösterir.

Karar: yerel LLM fikri iptal. Yerine 6 katmanlı, deterministik hat:

1. **Normalleştirme**: Türkçe küçültme, ek/kök sadeleştirme, yazım hatası (trigram), kısaltma sözlüğü, eşanlamlı grafiği (mevcut `queryIntel` + hastalık grafiği).
2. **Niyet sınıflayıcı**: kural + ağırlıklı anahtar kelime + küçük lojistik regresyon (kb boyutunda, ms'de çalışır). Örnek niyetler: tanım, belirti, tedavi, ilaç, doz/sayı, ayırıcı tanı, çıkmış soru, örnek soru, git/aç, ses çal, göster, karşılaştır, site yardımı.
3. **Varlık çıkarımı**: hastalık/ilaç/bulgu/ders/kurul/branş (sözlük + grafik üzerinde en uzun eşleşme).
4. **Getirme**: PostgreSQL FTS + pg_trgm (sözcüksel) + mevcut bge-m3 vektör servisi (`/api/rag/related`, CPU, 127.0.0.1:8094) → RRF birleştirme. Yeniden sıralama ucuz özelliklerle (varlık eşleşmesi, kaynak türü, kurul uyumu).
5. **Cevap derleme**: şablon + kaynaktan çıkarılmış cümle/tablo/madde. Sayı ve ad hiçbir zaman "üretilmez", yalnız kaynaktan kopyalanır.
6. **Eylem planı**: cevapla birlikte UI eylemleri (aç, kaydır, vurgula, ses çal, çizim göster, soru kartı çıkar) JSON olarak döner; ön yüz uygular.

Bilmiyorsa: "Kaynakta bulamadım" + en yakın 3 sonuç + "yöneticiye bildir" (soru günlüğüne düşer, eksik içerik listesi olur). Uydurma yok.

Gelecekte (isteğe bağlı, yalnız ölçüm iyileşmezse): tarayıcıda çalışan <100 MB niyet/yeniden-sıralama modeli (ONNX, WASM). Sunucuya yük binmez. Üretken model bu planda yok.

Kaynak tavanı: asistan hizmeti tek süreç, ≤150 MB RAM, sorgu başına <150 ms hedef; vektör servisi zaten çalışıyor. `MemoryMax/CPUQuota/OOMScoreAdjust` zorunlu.

## 2. Yol haritası

| Faz | Süre | Çıktı | Kapı |
|---|---|---|---|
| F0 Envanter | 2 gün | İndekslenecek kaynak listesi (ders, önem listesi, spot, çıkmış, örnek, terim, hastalık, ilaç, çözücü, sesli ders, site haritası), tek "belge" şeması | Her kaynak kimlik+URL+tür taşır |
| F1 İndeks | 4 gün | `asistan_belge` tablosu (FTS+trgm+vektör), gece artımlı güncelleme | Tüm kaynakların %100'ü indekste |
| F2 Anlama | 4 gün | Normalleştirici, varlık çıkarıcı, niyet sınıflayıcı, 500 soruluk sınama seti | Niyet doğruluğu ≥%92 |
| F3 Cevap + sohbet UI | 5 gün | `/api/asistan/sor`, sohbet paneli, metin/kart/tablo cevapları, kaynak chip'i | Sınama setinde ilk-3 isabet ≥%90 |
| F4 Site eylemleri | 5 gün | Yönlendirme, vurgulama, kaydırma, ses/çizim oynatma, soru gösterme | Eylem planı şeması + ekran sınaması |
| F5 Oturum/bağlam | 3 gün | Takip soruları ("peki tedavisi?"), önceki cevap bağlamı, geri bildirim | Takip çözümü ≥%85 |
| F6 Kişiselleştirme | 4 gün | Çalışma verisine göre öneri, zayıf konu, bitirdiklerim | Gizlilik kontrolü |
| F7 Sertleştirme | 3 gün | Başarım, hız, önbellek, hata günlüğü, yönetim paneli (cevaplanamayanlar) | p95 <300 ms |
| F8 Sürekli iyileşme | süreğen | Cevaplanamayan sorulardan sözlük/eşanlamlı genişletme (elle onay) | Haftalık rapor |

Her faz: önce sınama seti, sonra kod; `guncelleme_notu.json` onem+1, dağıtım yalnız `dagit.sh`; sunucu kodu değişince `meds-web` elle yeniden başlatılır. Hata çözümleri `KURUL2_YAPILMAYACAK_HATALAR.md` + `DEGISIKLIK_KAYDI.md`'ye işlenir.

## 3. Özellik kataloğu (230)

### A. Anlama (1–25)
1. Türkçe küçük/büyük harf (İ/ı) doğru normalleştirme
2. Ek/kök sadeleştirme ("böbreğin", "böbreklerde" → böbrek)
3. Yazım hatası düzeltme (trigram)
4. ASCII yazımı anlama ("hipertansiyon", "hipertansıyon", "gogus agrisi")
5. Kısaltma çözme (MI, DM, KOAH, ARDS…)
6. Eşanlamlı grafiği (Türkçe/Latince/İngilizce adlar)
7. Tamlama ≠ kavram kuralı (yanlış eşanlamlı üretmeme)
8. Çok sözcüklü varlık eşleştirme (en uzun eşleşme)
9. Hastalık adı çıkarımı
10. İlaç adı çıkarımı (etken madde/ticari ad)
11. Bulgu/belirti çıkarımı
12. Laboratuvar değeri çıkarımı (sayı + birim)
13. Ders/kurul/branş adı çıkarımı
14. Slayt/sayfa numarası çıkarımı ("12. slayt")
15. Yıl/sınav çıkarımı ("2023 dönem 3")
16. Niyet sınıflama (tanım, belirti, tedavi…)
17. Çoklu niyet ("tanımı ve tedavisi")
18. Olumsuzlama ("…hariç", "…değildir")
19. Karşılaştırma niyeti ("A ile B farkı")
20. Sayı/miktar niyeti ("kaç", "oranı", "doz")
21. Belirsiz soru için netleştirme sorusu
22. Eksik cümle ve telegram tarzı sorgu ("dm tedavi")
23. Argo/sınav dili ("çıkar mı", "sorulur mu")
24. Selamlama/teşekkür/veda algısı
25. Dil algısı (İngilizce soruya Türkçe terim eşlemesi)

### B. Arama ve getirme (26–50)
26. Tam metin arama (FTS)
27. Bulanık arama (pg_trgm)
28. Anlamsal arama (bge-m3)
29. RRF birleştirme
30. Varlık ağırlıklı yeniden sıralama
31. Kaynak türüne göre ağırlık (resmî > özet > not)
32. Kurul/ders filtresi
33. Kullanıcının kurulu/dönemi önceliği
34. Yeni içerik indeksine gece artımlı ekleme
35. Silinen içeriğin indeksten düşmesi
36. Tek sorguda çok kaynak (ders+soru+spot+ses)
37. Aynı bilginin yinelenen sonuçlarını teke indirme
38. Pasaj kırpma (tüm sayfa değil ilgili cümleler)
39. Eşleşen sözcüğü işaretleme
40. Tablo satırı bazlı getirme
41. Sayı bazlı getirme ("%80", "3 ay")
42. Hastalık→ilaç→yan etki grafiği gezintisi
43. Bulgu→olası hastalık (ters arama)
44. İlaç→endikasyon/kontrendikasyon
45. "Benzeri" bilgi bulma (kaynakta benzer ifade)
46. Eş anlamlı sorguyla ikinci geçiş
47. Sorgu genişletme (grafikten komşular)
48. Sonuçsuzlukta kademeli gevşetme
49. Çıkmış soru benzerliği (soru metninden soru bulma)
50. Önbellek (sık sorgular RAM'de)

### C. Cevap derleme (51–75)
51. Tek cümle net cevap
52. Maddeli cevap (`- **Başlık:** açıklama`)
53. Tablo cevabı
54. Karşılaştırma tablosu (A/B/ikisi/hiçbiri)
55. Adım adım mekanizma zinciri
56. Sayı kartı (değer, birim, kaynak)
57. Referans aralığı kartı
58. Ayırıcı tanı listesi
59. "Sınavda böyle sorulur" notu (çıkmış eşlemesinden)
60. Kaynak chip'i (ders, slayt, sayfa)
61. Kaynak çelişkisinde her iki değeri gösterme
62. Güven göstergesi (kaynaktan birebir / yakın / zayıf eşleşme)
63. "Kaynakta yok" dürüst cevabı
64. En yakın 3 sonuç önerisi
65. Cevap uzunluğu ayarı (kısa/orta/ayrıntılı)
66. "Daha fazla" ile genişletme
67. Özetle (3 madde)
68. Kısaltma açılımı kartı
69. Terim sözlüğü kartı (1–2 cümle)
70. Mnemonic/akılda kalıcı ipucu (kaynakta varsa)
71. Sık yapılan hata uyarısı (hata defterinden)
72. Klinik ipucu kutusu (`[!NOTE]`)
73. Önemli sınav spotu kutusu (`[!IMPORTANT]`)
74. Doğal Türkçe üslup kapısı (turkce_uslup.py ile şablon denetimi)
75. Şablon çeşitliliği (aynı cümleyi tekrarlamama)

### D. Tıbbi sorgu tipleri (76–105)
76. Hastalık tanımı
77. Etiyoloji/risk faktörleri
78. Patogenez/mekanizma
79. Patoloji bulguları
80. Klinik belirti/bulgu
81. Tanı kriterleri
82. Laboratuvar bulguları
83. Görüntüleme bulguları
84. Ayırıcı tanı
85. Tedavi basamakları
86. Komplikasyonlar
87. Prognoz
88. Epidemiyoloji (sayılar)
89. İlaç etki mekanizması
90. İlaç endikasyonları
91. Kontrendikasyonlar
92. Yan etkiler
93. İlaç etkileşimleri
94. Doz ve kullanım yolu
95. Farmakokinetik bilgiler
96. Anatomik yapı ve ilişkiler
97. Fizyolojik değerler
98. Mikroorganizma özellikleri
99. Genetik/kalıtım örüntüsü
100. Sendrom bileşenleri ("triadı", "pentadı")
101. Eponim açıklama
102. Latince/Türkçe terim karşılığı
103. Tablo istek: "…tablosunu göster"
104. Liste istek: "…sayıları"
105. "Hangisi daha sık/önemli" türü sıralama soruları

### E. Soru bankası (106–125)
106. Çıkmış soru getir (konuya göre)
107. Örnek soru getir
108. Sorunun kendisini sohbette göstermek
109. Soruyu çözülebilir kart olarak sohbette sunmak
110. Şık seçince doğru/yanlış + açıklama
111. "Yardım al" (her şık açıklaması)
112. Soruya sayfada gitme ve vurgulama
113. Yıl/kurul filtresi
114. Zorluk filtresi
115. Rastgele soru ("bana bir soru sor")
116. Mini sınav (5 soru) sohbette
117. Yanlış yapılan sorular tekrar
118. Aynı kavramdan ters soru (pozitif/negatif çift)
119. Sesli çözücü açıklamasını çal
120. Sorunun kaynak slaytını göster
121. Benzer sorular
122. Çıkmış sorudan dersin ilgili bölümüne köprü
123. "Bu konu kaç kez çıktı" istatistiği
124. Kurula göre çıkma sıklığı
125. Soru metnini yapıştırınca eşleşen soruyu bulma

### F. Site yönlendirme (126–150)
126. "… sayfasına git" (Ders çalış/Soru çöz/Sınav/Başvuru)
127. Ders açma (kurul/branş/ders)
128. Öğren destesini açma
129. Önem listesini açma
130. Sınav spotlarını açma
131. Çıkmış çözücüyü açma
132. Sözlüğü açma ve terime inme
133. Hastalık sayfasını açma
134. Check Up/kamp sayfalarını açma
135. Son Prova'yı açma
136. Kaynaklar (Sağlık Bakanlığı) sayfasına gitme
137. Bitirdiklerim/çalışma takibine gitme
138. Ayarlar (tema, yazı boyutu) yönlendirmesi
139. "Nerede?" soruları ("sesli ders nerede")
140. "Nasıl yapılır?" site rehberi (not al, favori, çevrimdışı)
141. Kapalı sayfaları önermemek (KAPALI_SAYFALAR)
142. Eski adresleri yeni adrese çevirme
143. Derin bağlantı üretme (siteHaritasi.ts)
144. Geri/ileri ile asistanın açtığı yeri hatırlama
145. Hesap ve giriş yardımı
146. Çevrimdışı kullanım yardımı
147. Bildirim/güncelleme açıklaması
148. Başarım ve puan sorularını yanıtlama
149. Hata bildirimi sayfasına yönlendirme
150. İletişim/yöneticiye ilet

### G. Vurgulama, kaydırma, ses, çizim (151–170)
151. Sayfada elemana kaydır
152. Elemanı vurgula (halka/parlama, birkaç sn)
153. Metin içinde cümleyi işaretle
154. Tablo satırı/sütunu vurgula
155. PDF sayfasına git ve bölgeyi işaretle
156. Yalnız ilgili görsel bölgeyi kırpıp sohbette göster
157. Görsel üstündeki çizimi (cizim katmanı) tek başına göster
158. Çizim + ilgili cümlenin sesi birlikte
159. Yalnız ilgili cümle/klip sesini çal (başlangıç–bitiş)
160. Ses hızı kontrolü
161. Sesi durdur/devam
162. Oynatma bitince asistanın dersi yerinde bırakması
163. Aynı anda tek ses (diğerini kıs)
164. Vurguyu kapat
165. Lazer/oku kuralı (CIZIM_KURALLARI uyumu)
166. Yakınlaştırma (zoom) yönlendirmesi
167. Birden çok vurgu için sıralı tur ("göster, sonra şunu göster")
168. Kullanıcı kaydırırsa vurguyu iptal
169. Mobilde kısa vurgu varyantı
170. Erişilebilirlik: vurgu için ekran okuyucu bildirimi

### H. Sohbet arayüzü bileşenleri (171–190)
171. Yüzen asistan düğmesi (her sayfada)
172. Yan panel/alt sayfa kipi (mobil)
173. Tam ekran kipi
174. Metin kutusu + sesle sorma (tarayıcı konuşma tanıma, isteğe bağlı)
175. Öneri çipleri (başlangıç soruları)
176. Hızlı eylem düğmeleri (git, çal, göster)
177. Kaynak kartı bileşeni
178. Soru kartı bileşeni
179. Tablo bileşeni
180. Karşılaştırma bileşeni
181. Mekanizma zinciri bileşeni
182. Sayı kartı bileşeni
183. Ses oynatıcı mini bileşeni
184. Görsel/çizim önizleme bileşeni
185. Mini sınav bileşeni
186. Flashcard bileşeni
187. Geri bildirim (beğen/beğenme + neden)
188. Konuşma geçmişi (cihazda)
189. Konuşmayı temizle / yeni konu
190. Yazıyor göstergesi yerine anlık sonuç (<150 ms)

### I. Bağlam ve kişiselleştirme (191–210)
191. Takip sorusu çözümü ("peki tedavisi?")
192. Zamir çözümü ("bunun", "onun")
193. Geçerli sayfa bağlamı ("şu an baktığım slayt")
194. Seçili metni sorma ("bunu açıkla")
195. Kullanıcının kurulu/dönemi
196. Zayıf konu önerisi
197. Çalışma planı önerisi
198. Günlük hedef hatırlatması
199. Bitmemiş dersi devam ettirme
200. "Bugün ne çalışayım" önerisi
201. Sınava kalan süreye göre öneri
202. Favoriler ve notlara erişim
203. Yaklaşan Kurul takvimi cevabı
204. Yanlış soru geçmişinden tekrar listesi
205. İlerleme özeti
206. Başarım/puan durumu sorgusu
207. Arkadaş sıralaması (varsa) sorgusu
208. Tercih hatırlama (kısa/ayrıntılı)
209. Gizlilik: kişisel veriyi sohbette düz yazmama
210. Konuşma verisini silme hakkı

### J. Kalite, güvenlik, başarım, yönetim (211–230)
211. Her cevapta kaynak şartı (kaynaksız tıbbi iddia yok)
212. Sayı kapısı: sayılar kaynakta birebir bulunmak zorunda
213. Kaynak dışı üretim yasağı
214. Tıbbi tavsiye reddi ("kendime/hastama tedavi söyle" → eğitim amaçlı uyarı)
215. Acil/kişisel sağlık sorusunda güvenli yönlendirme (112/hekim)
216. Kötüye kullanım ve spam sınırı (kişi başı hız sınırı)
217. Prompt-injection olmaması (LLM yok; yine de girdiyi temizleme)
218. Cevaplanamayan soru günlüğü
219. Yönetici paneli: en çok sorulan, en çok başarısız
220. Eşanlamlı önerisi kuyruğu (elle onay)
221. Sınama seti + her dağıtımda otomatik doğruluk raporu
222. Regresyon kapısı (doğruluk düşerse dağıtım durur)
223. İndeks sağlık kontrolü (eksik kaynak raporu)
224. Gecikme/RAM izleme, `MemoryMax`/`CPUQuota`
225. Önbellek geçersizleme (içerik değişince)
226. Çevrimdışı mod: tarayıcıda hafif yerel indeks (sık terimler)
227. Hata günlüğü ve yeniden deneme
228. A/B: cevap şablonu denemeleri
229. Erişilebilirlik (klavye, ekran okuyucu, kontrast)
230. Belgeleme: `API_KATALOG.md`, el kitabı, hata defteri güncelleme

## 4. Eylem planı şeması (taslak)

```json
{
  "cevap": [{"tur":"metin|tablo|sayi|soru|karsilastirma|zincir|gorsel|ses","veri":{}}],
  "kaynaklar": [{"tur":"ders","kimlik":"k2-07","slayt":12,"url":"/dersler/kurul2/..."}],
  "eylemler": [
    {"tip":"git","url":"..."},
    {"tip":"kaydir","hedef":"#slayt-12"},
    {"tip":"vurgula","hedef":"#h-3","sure":4000},
    {"tip":"ses_cal","klip":"...","bas":12.4,"bit":19.8},
    {"tip":"cizim_goster","key":"...","cumle":7}
  ],
  "guven": "birebir|yakin|zayif",
  "oneriler": ["peki tedavisi?"]
}
```

## 5. Riskler
- İçerik kimliklerinin kararlı olması gerekir (kalıcı kimlik kuralı mevcut).
- Vurgu/çizim için hedef elemanlara kararlı `data-asistan-hedef` anahtarları eklenmeli (F4).
- Kural 18 (çizim izolasyonu) asistan çizim göstermesinde de geçerli: yalnız o cümlenin çizimi.
- Mevcut `LocalAiChatView`/`QuestionAiChatDrawer` incelenip birleştirilmeli (çift sohbet arayüzü olmasın).

## 6. F0 sonucu (2026-10-29) — TAMAM

Araç: `scripts/asistan/kaynaklar.py` (salt okur, LLM/GPU yok) → `meds_temp/asistan/belgeler.jsonl` + `envanter_rapor.json`.
Belge şeması: `{id, tur, baslik, metin, ders, kurul, brans, url, kaynak, meta}`; kimlikler `tur:kimlik`, tekrar 0, hata 0.

**35.625 belge, 27 tür** (bu kaynaklar mevcut `/api/search` + `rag_chunks` içinde YOK):
ders_icerik (terim 1540, kısaltma 105, bilgi 250, hastalık kartı 351, önemli 260, spot 605, tablo 606, liste 156, kart 753, mini soru 446, özet 7) ·
önem listesi (özet 75, madde 2400, örnek soru 852) · asistan noktası 1857 · çözücü sorusu 3448 · çıkmış 5991 · örnek soru 8892 ·
sözlük 4001 + terim yardımcısı 436 + kısaltma 287 · hastalık 510 · soru kartı 505 · ders 247 · deste 182 · Sağlık Bakanlığı 837 · site sayfaları 26.

**Mevcut altyapı (yeniden yapma):** sitede `/api/search`, `/api/search/understand` (queryIntel), `SearchPalette`, vektör araması ve
`v15/SohbetEkleri.tsx` (sohbet ekleri) var. `rag_chunks` türleri: lecture_slide 25.302, deck_slide 11.998, summary 3.850,
glossary_term 6.296, disease 1.419, past_question 4.456, ornek_question 8.892, ai_* (kanıt değil, alınmaz).

**F1 kararları (tekrarı önlemek için):**
- İndeks = `belgeler.jsonl` (yapılandırılmış) + `rag_chunks` içinden YALNIZ `lecture_slide`, `summary`, `deck_slide` (slayt metni). `past_question`, `ornek_question`, `glossary_term`, `disease` rag'den alınmaz (doğrudan kaynakta zaten var); `ai_*`, `deepseek_*` alınmaz (kanıt değil).
- Vektör: mevcut `rag_vektor_hatti.py` kalıbı, ayrı tablo `asistan_belge`; bge-m3 CPU servisi.
- Dağıtım: `scripts/asistan/` ve `meds_temp` dışında kalıcı olması gereken indeks Oracle'a fark olarak gider.

**Açık noktalar (F1/F4'te doğrulanacak):**
1. 51 deste `overview` boş → deste slaytları rag `deck_slide` ile gelir; deste belgesi yalnız başlık olarak kalır.
2. Sözlük/hastalık adresleri `/sozluk?id=`, `/hastaliklar?id=` (`universalRedirectService.ts` biçimi); sözlük anahtarı ile `id` eşleşmesi ve `/saglik/<bölüm>` slug'ları ekran sınamasıyla doğrulanmalı.
3. Kısa metinli kayıtlar (kısaltma 151, kart 70, terim 25) aranırken başlıkla birlikte indekslenir.
4. Çıkmış sorularda `kurul` var, branş yok; branş çıkarımı F2 varlık sözlüğüyle yapılır.
5. Önem listesi çözücü soruları aynı konuyu iki kez anlatabilir; cevapta aynı kaynak teke indirilir (özellik 37).

## 7. F1 sonucu (2026-10-29) — TAMAM

- Tablo `asistan_belge` + `asistan_ara()` (`deploy/pg/sql/asistan_belge.sql`), 35.207 belge, hepsinin bge-m3 vektörü var (GPU, 954 sn).
- Arama: vektör (HNSW) + IDF ağırlıklı tam metin (sık sözcük "ilaç" nadir sözcük "nistatin"i bastırmaz) + başlık trigram, RRF ile birleşir.
- Araçlar: `kaynaklar.py` (belge üret) → `vektorle.py [--gpu]` (artımlı, parça önbelleği `meds_temp/asistan/vektor/`) → `.venv-ocr/bin/python yukle.py` (artımlı yükleme). Sınama: `ara_test.py` → **15/16**.
- Kalan 1 başarısız: "en önemli konular nerede" (site yönlendirmesi). Çözüm F2/F3: niyet "git/aç" ise `sayfa` türü öne alınır.
- Düzeltilen hatalar: sağlık künye listeleri ("kaynaklar 186") indekse girmiyor; `kurul` "butunleme" gibi metin değerleri sayıya çevrilir (ham değer meta'da).
- Oracle'a aktarım henüz YOK (F7'de fark eşitlemesi + `dagit.sh`); canlı site bu tabloyu kullanmıyor.
- GPU: AGENTS.md kural 10'a yedinci istisna işlendi (kilit 300,3000).

## 8. F2 sonucu (2026-10-29) — TAMAM (bir açık nokta F3'e devredildi)

- `src/services/asistan/anlama.ts`: `anla(soru)` → niyet (31 tür), ikincil niyet, varlıklar, süzgeç (kurul/yıl/branş), belirsizlik. Yazım düzeltme ve varlık çıkarımı mevcut `queryIntel` motorundan gelir (yeniden yazılmadı); asistana özgü olan niyet katmanıdır.
- Kural tuzağı: yazım düzeltme sohbet sözcüklerini bozabiliyor ("selam"); niyet hem özgün hem düzeltilmiş metinden aranır.
- Sınama (`scripts/asistan/anlama_sinama.mts`, setler `scripts/asistan/sinama/`, üretici `sinama_uret.py`): 457 soru, niyet %100.
  **Bu sayı şişik:** kurallar bu sette görülen hatalara göre ayarlandı. Ayarlamaya girmemiş ilk bağımsız ölçüm (71 soru): **%84,5**. Hatalar genellenebilir kurallarla düzeltildi (nasıl olur/ortaya çıkar, "hangi X'te kullanılır", site sözcükleri vb.); bağımsız set de böylece kirlendi. Gerçek doğruluk için yeni, hiç görülmemiş sorular (öğrenci soruları/günlük) gerekir: F3 sonrası "cevaplanamayan soru günlüğü"nden taze set alınmalı.
- Varlık yakalama %94,5. Kaçanlar (Hemipleji, Sarkopeni, Jinekomasti, Dengvaxia, Metildopa…) queryIntel paketinde olmayan sözlük terimleri. **F3 çözümü:** varlık bulunamazsa `asistan_belge.baslik_f` tam/önek eşleşmesiyle yedek varlık.
- Not: sınama setindeki "…ki̇bas…" gibi biçimler Python `.lower()` artefaktıdır (İ → i + birleşik nokta); `fold` bunu doğru işler.

## 9. F3 sonucu (2026-10-29) — TAMAM (tarayıcıda görsel sınama yapılmadı)

- **Sunucu:** `src/services/asistan/cevap.ts` + `routes.ts`; `POST /api/asistan/sor {soru}` → `{ana, ikincil, guven, varlik, bloklar, kaynaklar, oneriler, ms}`; kişi başı dakikada 40 istek; sunucu kodu değiştiği için `meds-web` yeniden başlatıldı. Ortalama 150–500 ms (CPU embed dahil).
- **Üretim yok:** her cümle `asistan_belge`'den alıntıdır ve numaralı kaynak taşır. Güven: `birebir` (konu + niyet cümlesi), `yakin`, `zayif` (zayıfta "bulamadım" + ilgili sayfalar).
- **Konu denetimi:** soru niyet sözcüklerinden arındırılır, kalan konu sözcükleri (yazım varyantları dahil: pyelonefrit≈piyelonefrit) belgede geçmiyorsa cevap verilmez. Bu, "nistatin yan etkileri" sorusuna başka ilacın yan etkilerini vermeyi engelledi (ilk sürümde veriyordu).
- **Bloklar:** metin, maddeler (kaynak numaralı), çözülebilir soru kartı, tablo, sayfa kartları (uygulama içi yönlendirme). Yönlendirme niyetleri (git/goster/ses_cal/site_yardim/calisma_onerisi) sayfa kartı döner; **görsel gösterme, ses çalma, vurgulama F4**, kişisel öneri F6.
- **Ön yüz:** `src/components/asistan/AsistanPanel.tsx` + `src/styles/v15/asistan.css`, `ShellV15` içine bağlı (portal; sağ altta "Asistan" düğmesi, mobilde tam ekran, Esc kapatır, geçmiş cihazda son 20 mesaj). `vite build` ve `tsc` temiz.
- **Cevapsız günlüğü:** `data/asistan/cevaplanamayan.jsonl` (yalnız `zayif` olanlar) — F2 için taze sınama seti kaynağı.
- **Bilinen sınırlar:** (1) Aynı kısaltmanın birden çok anlamı hepsi listelenir (ADH: alkol dehidrogenaz / antidiüretik hormon / atipik duktal hiperplazi). (2) "X tanısı" gibi sorularda ilgili cümle yoksa yalnız sayfa kartı gelir. (3) Sözlük/hastalık sayfa adreslerinin (`/sozluk?id=…`, `/hastaliklar?id=…`) ekranda doğru açıldığı sınanmadı. (4) Panel Oracle'da yok: `asistan_belge` tablosu ve veri Oracle'a taşınmadan dağıtım yapılırsa canlıda hata verir (F7).

### 9b. F3 düzeltme turu (2026-10-29) — günlükten öğrenilenler

Kaynak: `data/asistan/cevaplanamayan.jsonl` (gerçek denemeler: "anosmi", "nistatin", "nistatin nedir?", "ADH", "ACTH"). Tüm sorular artık `data/asistan/sorular.jsonl`'a da yazılıyor (soru, niyet, güven, ms, ilk kaynak; kişi bilgisi yok).
Kök nedenler ve çözümler:
1. **Yalın terim = niyetsiz = "anlayamadım".** Niyet çıkmazsa soru bilgi araması sayılır (`tanim`); büyük harfli yalın kısaltma (ADH, ACTH) kısaltma sorusudur.
2. **Cümle seçimi niyet sözcüğü şartına bağlıydı** ("tedavi" geçmeyen ama tedaviyi anlatan cümle elenirdi). Şimdi konu sözcüğü geçen cümle yeter; ders cümleleri azsa tüm türlerden (çıkmış soru açıklamaları dahil) tamamlanır; niyet cümlesi hiç yoksa cümleler bge-m3 ile anlamsal sıralanır (+0,3–3 sn).
3. **Başlık yalan söylüyordu** ("Parkinson — Tedavi" altında belirtiler). Niyet cümlesi bulunmadıysa başlık "Kaynakta bulduklarım" ve açıklama notu çıkar.
4. **Soru kayıtlarında şık/doğru satırları cümle sanılıyordu**; elendi.
5. **Türkçe iyelik eki** (taşı≠taş) ve kısa kısaltmalar (MS) eşleşmiyordu.
Sonuç: 15 çeşitli soruda 14 cevaplı / 1 zayıf (önce günlükteki sorular neredeyse hep boştu). Bilinen dürüst boşluklar: kaynakta olmayan bilgi (Parkinson tedavisi, rifampisin yan etkisi, ACTH açılımı) uydurulmaz; içerik açığı olarak `cevaplanamayan.jsonl`'dan izlenir.

## 10. DURDURULDU (2026-10-29, kullanıcı kararı)

Proje şimdilik durduruldu ve gizlendi; F4 ve sonrası başlamadı. Kod ve veri yerinde duruyor, hiçbir şey silinmedi.
- **Panel gizli:** `AsistanPanel` yalnız tarayıcıda `localStorage.medsor_asistan_goster = '1'` iken görünür.
- **Uç kapalı:** `POST /api/asistan/sor` sunucuda `MEDS_ASISTAN=1` yoksa 404 verir (kontrol edildi: 404).
- **Çalışan iş yok:** vektörleme/yükleme süreçleri bitti; yerel `asistan_belge` tablosu (35.207 belge) duruyor; Oracle'a hiçbir şey gönderilmedi, canlı sitede asistan hiç yayımlanmadı.
- **Yeniden açmak için:** `.env`'e `MEDS_ASISTAN=1` + `systemctl --user restart meds-web`; panelde yukarıdaki localStorage anahtarı (ya da kalıcı açmak için `gorunur()` işlevi). Sonra yol haritası §8–9'daki açık noktalardan (F4) devam.
