# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_1_slides():
    slides = []

    # Slide 1
    slides.append({
        "id": "k1-12-s01",
        "title": "Enflamasyonun Kimyasal Mediyatörleri: Tanım ve Temel İlkeler",
        "content": "Enflamasyonun kimyasal mediyatörleri, enfeksiyöz patojenlere, fiziksel/kimyasal hasara veya immün komplekslere karşı dokularda ortaya çıkan koruyucu enflamatuar reaksiyonları **başlatan, güçlendiren ve düzenleyen** çözünebilir biyomoleküllerdir. Mediyatörler rastgele dolaşan pasif moleküller olmayıp son derece katı biyolojik ilkelere tabidir:\n\n1. **Lokal Üretim:** Genellikle doğrudan enflamasyon odağında veya hasara uğrayan dokunun hemen komşuluğunda üretilirler.\n2. **Kısa Yarılanma Ömrü:** Mediyatörlerin büyük çoğunluğu çok kısa ömürlüdür; sentezlendikten dakikalar sonra enzimatik olarak parçalanır, nötralize edilir veya reseptör düzeyinde inaktive edilir.\n3. **Uyarana Bağımlılık:** Üretimleri mikrobiyal ürünlere (PAMP'lar) ve hasarlı hücrelerden ortama saçılan moleküllere (DAMP'lar) yanıt olarak süratle tırmanır.\n4. **Doku Hasarı Riski:** Mediyatörlerin aşırı, kontrolsüz veya uzamış üretimi enflamasyonun kendisinin birincil doku tahribatı nedenine dönüşmesine yol açabilir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_cloze(
                "Enflamasyonun kimyasal mediyatörleri enflamatuar reaksiyonları baslatan, güclendiren ve düzenleyen çözünebilir moleküllerdir.",
                "baslatan, güclendiren ve düzenleyen",
                "Mediyatörlerin 3 kardinal regülasyon fiili"
            ),
            make_quiz(
                "Enflamasyonun kimyasal mediyatörlerinin genel biyolojik özellikleriyle ilgili hangisi YANLIŞTIR?",
                [
                    {"key": "A", "text": "Mediyatörlerin çoğu dolaşımda haftalarca aktif kalarak etki gösterir.", "explanation": "A seçeneği YANLIŞTIR: Mediyatörlerin büyük çoğunluğu son derece kısa ömürlüdür; dakikalar içinde hızla yıkılır veya inaktive edilir."},
                    {"key": "B", "text": "Genellikle enflamasyon bölgesinde veya yakınında lokal olarak üretilirler.", "explanation": "B seçeneği doğrudur: Sistemik değil lokal üretim esastır."},
                    {"key": "C", "text": "Mikrobiyal ürünlere ve hasarlı hücre moleküllerine yanıtla üretimleri tetiklenir.", "explanation": "C seçeneği doğrudur: PAMP ve DAMP'lar üretimi uyarır."},
                    {"key": "D", "text": "Aşırı veya kontrolsüz üretimleri sekonder doku hasarına yol açabilir.", "explanation": "D seçeneği doğrudur: Kontrolsüz mediyatör salınımı oto-destrüksiyon yapar."},
                    {"key": "E", "text": "Reaksiyonu başlatma, amplifiye etme ve çözünmeyi düzenleme görevleri vardır.", "explanation": "E seçeneği doğrudur: Temel tanımı oluşturur."}
                ],
                "A"
            )
        ]
    })

    # Slide 2
    slides.append({
        "id": "k1-12-s02",
        "title": "Hücre Kaynaklı ve Plazma Kaynaklı Mediyatörlerin Ayrımı",
        "content": "Kimyasal mediyatörler köken aldıkları anatomik kompartımana ve aktivasyon mekanizmalarına göre iki ana grupta sınıflandırılır:\n\n- **Hücre Kaynaklı Mediyatörler:** Doku makrofajları, mast hücreleri, dendritik hücreler, nötrofiller, trombositler ve vasküler endotel tarafından üretilir. Ya hücre içinde önceden sentezlenip granüllerde depolanmış olarak bekletilir ve uyarılınca saniyeler içinde hızla degranüle edilir (örneğin mast hücresindeki **histamin**), ya da hücresel uyarı sonrası enzimler aracılığıyla sıfırdan yeni sentezlenir (örneğin **prostaglandinler, lökotrienler ve sitokinler**).\n- **Plazma Kaynaklı Mediyatörler:** Başlıca **karaciğer** tarafından sentezlenip dolaşıma verilen plazma proteinleridir. Dolaşımda biyolojik olarak inaktif prekürsör (zimojen) formda bulunurlar. Enflamasyon sahasında proteolitik kaskad basamaklarının tetiklenmesiyle aktif hale geçerler (örneğin **kompleman sistemi, kallikrein-kinin sistemi ve pıhtılaşma/fibrinoliz faktörleri**).",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Mediyatör Kökenleri Karşılaştırması",
                "Hücre Kaynaklı Mediyatörler",
                "Lokal hücrelerce üretilir; granülde depolanmış (histamin) veya yeni sentezlenir (eikozanoidler, sitokinler).",
                "Plazma Kaynaklı Mediyatörler",
                "Karaciğerde sentezlenir; kanda inaktif dolaşır, proteolitik kaskadla aktive olur (kompleman, kinin)."
            ),
            make_recall(
                "Plazma kaynaklı mediyatörlerin (kompleman, kinin vb.) büyük çoğunluğunu sentezleyip kana inaktif prekürsör olarak veren temel organ hangisidir?",
                "Karaciğerdir.",
                "Plazma proteinlerinin ana fabrikası olan organ"
            )
        ]
    })

    # Slide 3
    slides.append({
        "id": "k1-12-s03",
        "title": "Enflamasyonun Kardinal Belirtileri ve Sorumlu Mediyatörler",
        "content": "Celsus ve Virchow tarafından tanımlanan klasik enflamasyon belirtilerinin her biri spesifik kimyasal mediyatörlerin vasküler ve dokusal etkileriyle ortaya çıkar:\n\n1. **Kızarıklık (Rubor) ve Sıcaklık (Calor):** Arteryel prekapiller sfinkterlerin gevşemesi ve vazodilatasyon sonucu doku perfüzyonunun artmasıyla gelişir. Başlıca sorumluları **Histamin, Prostaglandinler (PGE2, PGI2, PGD2) ve Nitrik Oksittir (NO)**.\n2. **Şişlik / Ödem (Tumor):** Postkapiller venüllerde endotel hücre kasılmasıyla interendotelyal aralıkların açılması ve eksüda birikimidir. Sorumluları **Histamin, Lökotrienler (LTC4, LTD4, LTE4), C3a, C5a ve Bradikinindir**.\n3. **Ağrı (Dolor):** Doku gerilmesi ve nosiseptif sinir uçlarının uyarılmasıdır. Doğrudan ağrı oluşturan temel mediyatör **Bradikinin**, sinirleri duyarlılaştıran ise **Prostaglandinlerdir (özellikle PGE2)**.\n4. **Fonksiyon Kaybı (Functio Laesa):** Ağrı, şişlik ve doku hasarının ortak neticesidir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Kardinal Belirti", "Fizyopatolojik Mekanizma", "En Önemli Kimyasal Mediyatörler"],
                [
                    [
                        {"text": "Kızarıklık ve Sıcaklık (Rubor/Calor)", "isMasked": False, "hint": ""},
                        {"text": "Arterioler vazodilatasyon ve hiperemi", "isMasked": True, "hint": "Damar genişlemesi ve kan göllenmesi"},
                        {"text": "Histamin, PGE2, PGI2, PGD2, Nitrik Oksit", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Şişlik / Ödem (Tumor)", "isMasked": False, "hint": ""},
                        {"text": "Venüler permeabilite artışı ve eksüda", "isMasked": True, "hint": "Endotel aralıklarının açılması"},
                        {"text": "Histamin, LTC4/D4/E4, Bradikinin, C3a, C5a", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Ağrı (Dolor)", "isMasked": False, "hint": ""},
                        {"text": "Nosiseptör uyarımı ve ağrı eşiğinin düşmesi", "isMasked": True, "hint": "Sinir uçlarının sensitizasyonu"},
                        {"text": "Bradikinin, Prostaglandinler (PGE2), Nöropeptitler", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Enflamasyonda doğrudan ağrı oluşturan temel mediyatörler bradikinin ve prostaglandinlerdir.",
                "bradikinin ve prostaglandinlerdir",
                "Kinin ailesi üyesi ve eikozanoid ağrı mediyatörleri"
            )
        ]
    })

    # Slide 4
    slides.append({
        "id": "k1-12-s04",
        "title": "Vazoaktif Aminlere Giriş: Histaminin Hücresel Kaynakları",
        "content": "Akut enflamasyon yanıtının en erken döneminde (ilk saniyeler ve dakikalar içinde) devreye giren mediyatör grubuna 'vazoaktif aminler' denir. Bu grubun prototipi **histamindir** (histidinin dekarboksilasyonu ile sentezlenir). Histamin vücutta üç temel hücre tipinde depolanır:\n\n1. **Mast Hücreleri (En Zengin Kaynak):** Damarların ve sinirlerin hemen komşuluğunda, bağ dokusu içinde stratejik olarak yerleşmiş nöbetçi hücrelerdir. Sitoplazmalarında yoğun bazofilik granüller içinde heparin ile kompleks yapmış halde yüksek miktarda histamin taşırlar.\n2. **Kandaki Bazofiller:** Dolaşımda bulunan granülositlerdir; mast hücrelerine benzer şekilde granüllerinde histamin depolar ve alerjik/enflamatuar uyarılarla dokuya geçerek salınım yaparlar.\n3. **Trombositler:** Pıhtılaşma esnasında yoğun granüllerinden (dense granules) histamin ve serotonin salgılarlar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_cloze(
                "Vücutta önceden depolanmıs en zengin histamin kaynağı perivasküler bag dokusunda yerlesik mast hücreleridir.",
                "mast hücreleridir",
                "Histamin granüllerini en bol taşıyan bağ dokusu nöbetçi hücresi"
            ),
            make_recall(
                "Vazoaktif amin grubundan olan histamin hangi amino asidin dekarboksilasyonu ile sentezlenir?",
                "Histidin amino asididir.",
                "Histaminin prekürsörü olan temel amino asit"
            )
        ]
    })

    # Slide 5
    slides.append({
        "id": "k1-12-s05",
        "title": "Mast Hücresi Degranülasyonunu Tetikleyen Mekanizmalar",
        "content": "Mast hücrelerinin sitoplazmik granüllerini dışarı boşaltması (degranülasyon) immünolojik veya non-immünolojik çok çeşitli uyaranlarla tetiklenebilir:\n\n1. **İmmünolojik / Alerjik Tetikleyiciler (Tip I Aşırı Duyarlılık):** Mast hücresi yüzeyindeki yüksek afiniteli FcεRI reseptörlerine bağlı spesifik **IgE antikorlarının** antijenle (alerjen) çapraz bağlanması (cross-linking) intraselüler kalsiyum patlamasına ve ani degranülasyona yol açar.\n2. **Kompleman Anafilatoksinleri:** Kompleman kaskadının aktivasyonu ile açığa çıkan **C3a ve C5a** peptitleri, mast hücresindeki anafilatoksin reseptörlerine bağlanarak antikor bağımsız hızlı degranülasyon yapar.\n3. **Fiziksel Hasar:** Mekanik travma, cerrahi kesi, aşırı soğuk veya aşırı sıcak uyaranları.\n4. **Endojen Peptitler ve Sitokinler:** Duyusal sinirlerden salınan nöropeptitler (**Madde P**) ile makrofaj kaynaklı **IL-1 ve IL-8** sitokinleri de degranülasyonu indükler.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Mast Hücresi Degranülasyon Kaskadı",
                [
                    "1. Uyaran Bağlanması: Alerjenin yüzeydeki IgE molekülleriyle çapraz bağlanması",
                    "2. İntraselüler Sinyal: Tirozin kinaz aktivasyonu ve hücre içi kalsiyum iyonu yükselmesi",
                    "3. Granül Füzyonu: Önceden hazır histamin keseciklerinin plazma zarıyla kaynaşması",
                    "4. Ekzositoz: Histaminin saniyeler içinde doku interstisyumuna salınması"
                ]
            ),
            make_quiz(
                "Mast hücrelerinden antikor ve antijen aracılığı olmaksızın, doğrudan kendi reseptörlerine bağlanarak histamin degranülasyonu yaptıran kompleman parçacıkları hangileridir?",
                [
                    {"key": "A", "text": "C3a ve C5a (Anafilatoksinler)", "explanation": "A seçeneği DOĞRUDUR: C3a ve C5a mast hücresi yüzeyindeki reseptörlerine bağlanarak anafilatoksin etkisiyle histamin salınımını tetikler."},
                    {"key": "B", "text": "C3b ve iC3b", "explanation": "B seçeneği yanlıştır: Bunlar opsonindir, fagositozu artırır."},
                    {"key": "C", "text": "C5b-9 (Membran atak kompleksi)", "explanation": "C seçeneği yanlıştır: Hücre zarında delik açar (lizis)."},
                    {"key": "D", "text": "Faktör B ve Faktör D", "explanation": "D seçeneği yanlıştır: Alternatif yol enzimleridir."},
                    {"key": "E", "text": "C1 inhibitörü (C1-INH)", "explanation": "E seçeneği yanlıştır: Düzenleyici proteindir, degranülasyon yapmaz."}
                ],
                "A"
            )
        ]
    })

    # Slide 6
    slides.append({
        "id": "k1-12-s06",
        "title": "Histamin Reseptörleri: H1 Reseptörü ve Venüler Geçirgenlik",
        "content": "Histamin hedef hücrelerde dört farklı G-protein kenetli reseptör (H1, H2, H3, H4) üzerinden etki gösterir. Akut enflamasyon ve vasküler yanıtta en kritik olanı mikrovasküler endotelde yer alan **H1 reseptörüdür**:\n\n- **Arterioler Vazodilatasyon:** Histamin arteriol düz kasında endotel kaynaklı Nitrik Oksit (NO) sentezini uyararak damar genişlemesi ve lokal eritem (kızarıklık) oluşturur.\n- **Venüler Endotel Kasılması (Geçici Geçirgenlik):** Histaminin en karakteristik akut etkisi postkapiller venüllerde gerçekleşir. Endotel hücrelerindeki H1 reseptörlerini uyararak hücre içi aktin-miyozin kasılmasını tetikler. Endotel hücreleri büzüşür ve aralarındaki interendotelyal bağlantılar açılarak sıvı ve proteinlerin interstisyuma kaçmasına (eksüda / ödem) yol açar. Bu geçirgenlik artışı 'erken geçici yanıt' olarak adlandırılır; dakikalar içinde başlar ve 15-30 dakika içinde hızla söner.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_cloze(
                "Histamin postkapiller venüllerde H1 reseptörü üzerinden endotel kasılması yaparak erken geçici geçirgenlik artışına neden olur.",
                "H1 reseptörü",
                "Akut enflamasyon ve alerjide vasküler etkileri yürüten histamin reseptörü"
            ),
            make_recall(
                "Histaminin venül geçirgenliğini artırırken endotel hücrelerinde meydana getirdiği temel hücresel hareket nedir?",
                "Endotel hücre kasılmasıdır (endothelial cell contraction).",
                "Hücrelerin büzüşerek aralık açması hareketi"
            )
        ]
    })

    # Slide 7
    slides.append({
        "id": "k1-12-s07",
        "title": "Serotonin (5-Hidroksitriptamin): Trombosit Kaynağı ve Vazomotor Etkisi",
        "content": "İkinci majör vazoaktif amin **Serotonindir (5-HT)**. Triptofan amino asidinden sentezlenir. İnsanlarda serotonin esas olarak gastrointestinal sistem enterokromafin hücrelerinde ve santral sinir sisteminde üretilmekle birlikte, enflamasyon açısından en önemli periferik deposu **trombositlerdir (kan pulcukları)**. Trombositler dolaşımda kandan serotonini aktif olarak içeri alarak yoğun granüllerinde depolarlar. Trombosit agregasyonu ve pıhtılaşma tetiklendiğinde (örneğin endotel hasarı veya kollajen teması sonrası) serotonin hızla dışarı salınır. Histaminden farklı olarak serotoninin temel vasküler etkisi **vazokonstriksiyondur**; kanamayı durdurmak için hasarlı damarı büzer. Enflamasyondaki vasküler geçirgenlik artırıcı rolü insanlarda histamine kıyasla çok daha sınırlı ve ikincil düzeydedir.",
        "sourcePdf": "Kurul 1 - Ders 11: Üriner Obstrüksiyonun Fizyopatolojisi (Doç. Dr. Özer Baran); Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri",
        "elements": [
            make_slider(
                "Histamin ve Serotonin Karşılaştırması",
                "Histamin (Mast Hücresi)",
                "Arteriol vazodilatasyonu, venül endotel kasılmasıyla belirgin permeabilite artışı ve kaşıntı yapar.",
                "Serotonin (Trombosit)",
                "Trombosit agregasyonunda salınır; vazokonstriksiyon etkisi baskındır, geçirgenlik rolü sınırlıdır."
            ),
            make_cloze(
                "Trombosit granüllerinden salınan serotoninin vasküler sistem üzerindeki en belirgin baskın etkisi vazokonstriksiyondur.",
                "vazokonstriksiyondur",
                "Damar lümenini daraltıcı etki"
            )
        ]
    })

    # Slide 8
    slides.append({
        "id": "k1-12-s08",
        "title": "Vazoaktif Aminlerin Hızlı İnaktivasyonu ve Zaman Eğrisi",
        "content": "Vazoaktif aminler akut enflamatuar yanıtın 'ilk dalga' hücum kıtasıdır; ancak etkilerinin kontrolsüz yayılmasını önlemek amacıyla vücutta son derece süratli enzimatik yıkım mekanizmalarıyla donatılmışlardır:\n\n- **Histamin Yıkımı:** Salınan histamin dokuda hızla iki enzim yolağıyla inaktive edilir: Histamin N-metiltransferaz (HNMT) ve Diamin Oksidaz (DAO / Histaminaz). Bu enzimler serbest histamini dakikalar içinde metabolitlerine dönüştürür.\n- **Zaman Eğrisi:** Histaminin tetiklediği vasküler geçirgenlik artışı saniyeler içinde başlar, 5-10. dakikalarda tepe yapar ve genellikle 15-30 dakika içinde tamamen sönümlenir ('erken geçici faz').\n\nEğer enflamasyon devam edecekse, vazoaktif aminlerin sönümlendiği bu noktadan itibaren bayrağı ikinci dalga mediyatörler olan **araşidonik asit metabolitleri (prostaglandinler ve lökotrienler)** devralır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Akut Vasküler Fazın Zaman Sıralaması",
                [
                    "1. Hasar / Uyarı: Mast hücresi membran uyarımı ve histamin boşalması",
                    "2. Erken Geçici Yanıt (0-15 dk): H1 reseptör uyarımı ile venüler sızıntı ve kızarıklık",
                    "3. Enzimatik Yıkım (15-30 dk): Histaminaz/DAO ile serbest aminlerin hızla parçalanması",
                    "4. İkinci Dalgaya Geçiş (30+ dk): Eikozanoid ve sitokinlerin devreye girerek geçirgenliği sürdürmesi"
                ]
            ),
            make_recall(
                "Doku interstisyumunda serbest histamini süratle yıkarak erken vasküler yanıtın 15-30 dakikada sönmesini sağlayan enzim hangisidir?",
                "Diamin Oksidazdır (DAO / Histaminaz).",
                "Histamini yıkan klasik oksidaz enzimi"
            )
        ]
    })

    # Slide 9 (CHECKPOINT 1)
    slides.append({
        "id": "k1-12-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Mediyatör Temelleri ve Vazoaktif Aminler",
        "content": "Enflamasyonun kimyasal mediyatörleri ve vazoaktif aminlerin temel ilkeleri:\n\n1. **Tanım ve Prensip:** Mediyatörler reaksiyonu başlatan, güçlendiren ve düzenleyen çözünebilir moleküllerdir; lokal üretilirler ve kısa ömürlüdürler.\n2. **Köken Ayrımı:** Hücre kaynaklı olanlar granülde depolu (histamin) veya yeni sentezlenirken (PG, LT, sitokin); plazma kaynaklı olanlar (kompleman, kinin) karaciğerde sentezlenip kanda inaktif gezer.\n3. **Kardinal Bulgular:** Kızarıklık/sıcaklık histamin/PGE2/NO ile; ödem histamin/lökotrien/bradikinin ile; ağrı bradikinin ve PGE2 ile ortaya çıkar.\n4. **Histamin:** En zengin kaynak mast hücresidir; IgE, C3a/C5a, travma ile salınır. H1 reseptörüyle arteriol vazodilatasyonu ve venül endotel kasılması (erken geçici geçirgenlik) yapar.\n5. **Serotonin:** Trombosit granüllerindedir; vazokonstriksiyon etkisi baskındır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Akut enflamasyonun erken vasküler değişiklikleriyle ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?",
                [
                    {"key": "A", "text": "Histaminin venüllerdeki temel etkisi: H1 reseptörü aracılı endotel hücre kasılması ve geçici permeabilite artışı", "explanation": "A seçeneği DOĞRUDUR: Histamin H1 reseptörleriyle endotel kasılması yaparak erken geçici geçirgenlik artışına neden olur."},
                    {"key": "B", "text": "Serotoninin temel hücresel kaynağı: Plazma dendritik hücreleri", "explanation": "B seçeneği yanlıştır: Serotonin periferde trombosit granüllerinde depolanır."},
                    {"key": "C", "text": "Plazma kaynaklı mediyatörlerin ana sentez yeri: Dalak kırmızı pulpası", "explanation": "C seçeneği yanlıştır: Karaciğerde sentezlenirler."},
                    {"key": "D", "text": "Enflamasyonda ağrıyı oluşturan temel vazoaktif amin: Serotonin", "explanation": "D seçeneği yanlıştır: Ağrı esas olarak bradikinin ve PGE2 ile ilişkilidir."},
                    {"key": "E", "text": "Histaminin yarılanma ömrü: Dolaşımda 3-4 gün boyunca aktiftir", "explanation": "E seçeneği yanlıştır: Dakikalar içinde DAO ve HNMT ile yıkılır."}
                ],
                "A"
            ),
            make_cloze(
                "Histaminin venüllerde interendotelyal aralıkları acması erken geçici geçirgenlik yanıtı olarak adlandırılır.",
                "erken geçici",
                "Dakikalar içinde başlayıp 15-30 dakikada sönen faz"
            )
        ]
    })

    # Slide 10
    slides.append({
        "id": "k1-12-s10",
        "title": "H1 Reseptör Antagonistlerinin (Antihistaminikler) Klinik Farmakolojisi",
        "content": "Histaminin akut vasküler ve düz kas etkilerini engellemek amacıyla geliştirilen **H1 reseptör antagonistleri (antihistaminikler)** klinik pratikte alerjik rinit, ürtiker ve akut anafilaksi tedavisinin temel ilaçlarıdır. Bu ilaçlar endotel hücreleri ve düz kas üzerindeki H1 reseptörlerini kompetitif olarak bloke ederler. Sonuç olarak venüler geçirgenlik artışı, kaşıntı ve bronkokonstriksiyon önlenir. Ancak hekimin bilmesi gereken kritik bir farmakolojik gerçek vardır: **Şiddetli bronkospazm ve sistemik anaflakside antihistaminikler tek başına YETERSİZDİR!** Çünkü astım ve bronkospazmda lümeni daraltan asıl güçlü mediyatörler histaminden yüzlerce kat daha potent olan sisteinil lökotrienler (LTC4, LTD4, LTE4) ve PAF'tır. Bu nedenle hayatı tehdit eden anaflakside ilk basamak ilaç antihistaminik değil, alfa ve beta adrenerjik etkili adrenalindir (epinefrin).",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Arı sokması sonrası tüm vücutta ürtiker plakları, dudaklarda anjiyoödem, şiddetli stridor ve hipotansiyon (tansiyon 70/40 mmHg) ile acile getirilen bir hastada nöbetçi hekim yalnızca intramüsküler H1 antihistaminik (feniramin) uyguluyor; ancak hastanın bronkospazmı gerilemiyor ve tablosu kötüleşiyor.",
                "Bu tablonun düzelmemesindeki temel farmakolojik gerekçe ve yapılması gereken hayat kurtarıcı adım nedir?",
                [
                    {
                        "text": "Anaflaktik bronkokonstriksiyondan histaminden ziyade lökotrienler sorumludur; H1 blokajı yetersizdir, derhal intramüsküler adrenalin (epinefrin) uygulanmalıdır.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. Anaflaksideki derin vasküler çöküş ve bronkokonstriksiyon lökotrien/PAF aracılıdır; tek başına antihistaminik yetersizdir, ilk tercih adrenalindir."
                    },
                    {
                        "text": "Hastaya acilen 5 litre soğuk su içirilmelidir.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Şok ve havayolu tıkanıklığı olan hastaya su içirmek aspirasyona yol açar."
                    },
                    {
                        "text": "Antihistaminik dozu 100 katına çıkarılmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Doz artışı anaflaksiyi geri döndürmez; fizyolojik antagonist olan adrenalin şarttır."
                    }
                ]
            ),
            make_recall(
                "Akut anafilaktik şokta sistemik vazodilatasyonu ve bronkospazmı hızla geri çeviren ilk tercih hayat kurtarıcı sempatomimetik ilaç hangisidir?",
                "Adrenalindir (epinefrin).",
                "Alfa ve beta adrenerjik acil resüsitasyon hormonu"
            )
        ]
    })

    return slides
