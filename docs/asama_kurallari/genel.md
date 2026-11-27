# Aşama kuralları — genel

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/hat/tam_hat/kural_secici.py`. 14 madde. Tek satırlı maddeleri betik denetler (tam metin: `kural_secici.py --tam <H no|aşama>`).

### Kurul 2 hattı için genel kural


### Diğer oturumlarda düzeltilen hatalardan çıkarılan dersler (tarama 2026-10-20)


### Kurul 2 içeriğinin karşılaması gereken sonradan eklenen özellikler


### H18 — Diğer oturumların 2026-10-20 düzeltmelerinden Kurul 2'ye taşınanlar (kayıt)


### H20 — Kurul 1'de elle kurulan Son Prova ve anlamsal çapa Kurul 2'de unutulmasın / K1'e sabit kalmasın (2026-10-21)
- **Kural:** kurul başına elle yapılan her yeni ürün, ertesi gün hat.json'a aşama olarak girer; betik kurul/branş/kod
  biçimini plandan ya da kayıt defterinden alır, talimatları depoda (`meds/scripts/...`) tutulur.
- **Kapı — EKLENDİ:** `son_prova` aşaması (plan_kurul.py + son_prova_zinciri.py), `ders_zinciri` `capa` adımı
  (capa_dogrula.py). Son Prova sınav dağılımı duyurusu yoksa bildirim gider.



### H447 — Metni değişen paragrafların v2 cümleleri boş kaldı, ders ekranı ve çapası o paragraflarda eksik yayında (2026-10-30)
- **Önleme:** `klip_tasi.py` "v2: N paragraf boş" raporu verdiyse o ders, boş paragraflar `konusma_v2` biçiminde yazılıp
  `konusma_v2.py --dogrula <dizin>` (kaynak.md ile) 0 HATA verene dek dağıtılmaz; açık iş olarak not düşmek yerine aynı oturumda kapatılır.


### H658 — Yapay zekâ test oturumu canlıda ders ayrıntısını açamıyordu: çerez api. alt alanına gitmiyordu (2026-11-25)
- **Önleme:** Kapı yanıtı (500 + "Sunucu hatası") gerçek çökme sanılmasın: önce aynı ucu konteyner içinden dene
  (`docker --context oracle exec meds-app node -e "fetch('http://localhost:3000/api/...')"`; içeride 200 ise sorun kimlik).
  Oturum/çerez kuran her yeni yol iki alan adını (site + `api.`) birlikte sınar; önbellekten gelen başarı kanıt sayılmaz.

### H694 — Görüntü (taranmış) ders PDF'i: kanıt kapısı, terim ve kısaltma boş kaldı (2026-11-26, k2-61)
- **Kural:** E0'da `sayfalar.json` metinli sayfa oranı düşükse E1'den ÖNCE OCR yapılır; görüntüleyiciye metin katmanlı PDF konur.


### Hat dışı maddeler (ön yüz/yönetim/altyapı — içerik aşamasını ilgilendirmez; tam metin konu dosyasında)
- hatalar/betik_altyapi.md: H5, H25, H26, H27, H34, H35, H78, H90, H440, H478, H484, H489, H557, H558, H560, H561, H577, H578, H584, H593, H594, H597, H601, H585, H598, H604, H610, H630, H631, H632, H633, H635, H649
- hatalar/on_yuz_oynatici_ders.md: H82, —, —, H117, H111g, H111p, H111q, H330, H335, H449, H491, H492, H493, H494, H495, H496, H491, H494, H495, H496, H507, H519, H520, H602, H636, H637, H638, —, —, H652, H653, H654
- hatalar/on_yuz_sayfa_denetimi.md: H86, H101, H102, H102, H104, H106, H107, H122, H109, H124, H110, H127, H111r, H111t, H131d, H139, H140, H144, H145, H147, H148, H149, H150, H151, H154, H200, H220, H239, H242, H300, H340, H380, H400, H435, H436, H458, H551, H588, H590, H591, H603, H611, H614, H616
- hatalar/on_yuz_tasarim_tema.md: H48, H87, H90, H99, H100, —, —, H100, H111c, H111h, H111s, H131c, H388, H431, H433, H439, H475, H502, H504, H517, H518, H659, H660, H661, H662, H663, H664, H665, H666, H668, H669, H671, H672, H673, H674, H675, H676, H678, H679, H680, H681, H686, H685, H687, H689, H690, H691, H693, H701, H702, H703
- hatalar/yonetim_basarim.md: H111d, H111e, H111f, H111u, H131, H131a, H131b, H141, H142, H143, H146, H152, H153, H170, H250, H290, H296, H310, H320, H431
