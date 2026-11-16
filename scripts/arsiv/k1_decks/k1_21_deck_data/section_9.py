# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 21: Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler
(Uz. Dr. Merve Kaçar - Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji ABD)
Bölüm 9: Enfeksiyon Hastalığının Doğal Seyri ve Klinik Evreleri (Slayt 81 - 90)
Checkpoint 9: Slayt 89
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_9_slides():
    slides = []

    # Slayt 81: Enfeksiyon Hastalığının Zaman Çizelgesi ve Klinik Fazları
    slides.append({
        "id": "k1-21-s81",
        "title": "Enfeksiyon Hastalığının Zaman Çizelgesi ve Klinik Fazları",
        "section": "Enfeksiyon Hastalığının Doğal Seyri ve Klinik Evreleri",
        "slideNumber": 81,
        "narrative": (
            "Bir patojen duyarlı konakçıya ulaştığında enfeksiyon hastalığı rastgele gelişmez; "
            "fizyopatolojik mekanizmalara ve immün yanıtın seyrine bağlı olarak belirli kronolojik "
            "aşamalardan geçer. Tıbbi mikrobiyoloji ve enfeksiyon klinik pratiğinde bir enfeksiyon "
            "hastalığının doğal seyri temel olarak beş ana evrede incelenir: "
            "1. **Karşılaşma ve Giriş (Exposure & Entry):** Etkenin konağa temas edip bariyerleri aşması. "
            "2. **İnkübasyon (Kuluçka) Dönemi:** Etkenin girişi ile ilk semptomun belirmesi arasındaki sessiz çoğalma evresi. "
            "3. **Prodromal Dönem:** Halsizlik ve hafif ateş gibi özgül olmayan sistemik öncü belirtilerin belirmesi. "
            "4. **Klinik (Akut / Akme) Dönemi:** Hastalığa özgü patognomonik bulguların zirveye ulaştığı evre. "
            "5. **Nekahat (Konvalesan) Dönemi:** Patojenin kontrol altına alınması ve doku onarımının gerçekleşmesi. "
            "Her evrenin mikrobiyolojik yükü, patolojik yanıtı ve bulaştırıcılık potansiyeli birbirinden farklıdır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Enfeksiyon hastalığının doğal seyri etken girişi, inkübasyon, prodrom, klinik hastalık ve nekahat evrelerinden oluşur.",
                "doğal seyri",
                "Hastalığın zaman içindeki kronolojik gelişim süreci"
            ),
            make_causal_chain(
                "Enfeksiyon Hastalığının Kronolojik İlerleme Aşamaları",
                [
                    "1. Giriş: Patojen mukoza veya derideki reseptörlere tutunur.",
                    "2. İnkübasyon: Semptomsuz evrede patojen kritik eşiğe kadar çoğalır.",
                    "3. Prodrom: İnterlökin-1 ve TNF salınımıyla genel halsizlik başlar.",
                    "4. Akut Faz: Karakteristik organ hasarı ve patognomonik bulgular zirve yapar.",
                    "5. Nekahat: İmmün eliminasyon ile semptomlar yatışır ve doku iyileşir."
                ]
            ),
            make_table(
                "Enfeksiyon Evreleri ve Temel Nitelikleri",
                ["Klinik Evre", "Patojen Yükü", "Semptom Niteliği", "Bulaştırıcılık Durumu"],
                [
                    ["İnkübasyon", "Artış eğiliminde", "Tamamen asemptomatik", "Hastalığa göre değişken"],
                    ["Prodromal", "Hızlı yükselir", "Non-spesifik genel belirtiler", "Genellikle yüksektir"],
                    ["Akut Hastalık", "Zirve noktada (pik)", "Hastalığa özgül ve şiddetli", "En yüksek düzeydedir"],
                    ["Nekahat", "Düşüşe geçer", "Klinik düzelme ve doku onarımı", "Portörlükte sürebilir"]
                ],
                hidden_coords=[(0, 2), (1, 2), (2, 2), (3, 3)],
                hints=[
                    "Bu evrede hastada hiçbir şikayet bulunmaz",
                    "Özgül olmayan kırgınlık ve halsizlik hali",
                    "Hastalığın kendine has patognomonik tablosu",
                    "Klinik iyileşmeye rağmen dış ortama saçılım riski"
                ]
            )
        ]
    })

    # Slayt 82: Birinci Evre: Karşılaşma, Giriş ve Kolonizasyon Dinamikleri
    slides.append({
        "id": "k1-21-s82",
        "title": "Birinci Evre: Karşılaşma, Giriş ve Kolonizasyon Dinamikleri",
        "section": "Enfeksiyon Hastalığının Doğal Seyri ve Klinik Evreleri",
        "slideNumber": 82,
        "narrative": (
            "Enfeksiyonun başlangıç noktası, mikroorganizmanın konak yüzeyiyle ilk fiziksel temas kurduğu "
            "**karşılaşma ve giriş** anıdır. Patojenler hava yolu, sindirim kanalı, ürogenital traktus ya da "
            "deri bütünlüğünün bozulduğu çatlak ve yaralanmalardan giriş yaparlar. "
            "Girişi takiben ilk kritik aşama **kolonizasyondur**. Mikroorganizma fimbriya, pili ve adezyon molekülleri "
            "aracılığıyla epitel hücre yüzeyindeki glikoprotein reseptörlerine spesifik olarak bağlanır. "
            "Epitel yüzeyinde peristaltizm, mukosiliyer klirens, mide asiditesi ve sekresyonların yıkama etkisine "
            "karşı direnç göstererek çoğalan patojen mikrokoloniler oluşturur. "
            "Kolonizasyon aşamasında henüz konak dokusuna derin invazyon gerçekleşmemiş olabilir; bu aşamada immün "
            "sistem veya normal flora engeli etkeni durdurursa enfeksiyon yerleşmeden sonlanabilir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Mikroorganizmanın konak epitel yüzeyine tutunup çoğalarak yerleşmesine kolonizasyon adı verilir.",
                "kolonizasyon",
                "Doku hasarı yapmaksızın yüzeyde yerleşik üreme aşaması"
            ),
            make_before_after(
                "İlk Karşılaşma ve Kolonizasyon Ayrımı",
                "Yüzeyel Temas ve Giriş",
                "Patojen epitel yüzeyine damlacık veya temasla ulaşır; mukosiliyer klirens ve peristaltizm etkeni uzaklaştırmaya çalışır.",
                "Spesifik Kolonizasyon",
                "Adezinler konak reseptörlerine kilitlenir; yıkama mekanizmalarına direnç gösterilerek biyofilm ve mikrokoloniler inşa edilir.",
                "Yüzeyel kontaminasyonun stabil doku kolonizasyonuna evrilme dinamikleri"
            ),
            make_active_recall(
                "Kolonizasyonun gerçek bir enfeksiyon hastalığına dönüşmesi için hangi patolojik basamağın aşılması zorunludur?",
                "Patojenin epitelyal bariyeri aşarak submukozal dokuya veya kana invaze olması ve doku hasarı başlatması gerekir.",
                "Bariyer aşımı ve inflamatuar hasar kriteri"
            )
        ]
    })

    # Slayt 83: İkinci Evre: İnkübasyon (Kuluçka) Dönemi ve Değişken Süreler
    slides.append({
        "id": "k1-21-s83",
        "title": "İkinci Evre: İnkübasyon (Kuluçka) Dönemi ve Değişken Süreler",
        "section": "Enfeksiyon Hastalığının Doğal Seyri ve Klinik Evreleri",
        "slideNumber": 83,
        "narrative": (
            "**İnkübasyon (kuluçka) dönemi**, etkenin konağa giriş anından ilk klinik semptom veya bulgunun "
            "ortaya çıkışına kadar geçen süredir. Bu evrede konakta klinik hiçbir rahatsızlık hissi yoktur, "
            "ancak mikrobiyolojik açıdan patojen dokularda son derece aktiftir; geometrik hızla replike olur, "
            "hücre içi veya dışı ortama yayılır ve doku harabiyeti için kritik eşik konsantrasyona ulaşmaya çalışır. "
            "İnkübasyon süresi patojenden patojene ve konağın direncine bağlı olarak olağanüstü geniş bir yelpazede değişir: "
            "- **Çok Kısa (Saatler):** Stafilokokal gıda zehirlenmesi (önceden üretilmiş enterotoksin alımıyla 1-6 saat). "
            "- **Kısa (1-3 gün):** İnfluenza, rinovirüs (soğuk algınlığı), kolera. "
            "- **Orta (1-3 hafta):** Suçiçeği (10-21 gün), kızamık (10-14 gün), tifo (7-14 gün). "
            "- **Uzun (Haftalar - Aylar):** Hepatit B ve C (1-6 ay), kuduz (ısırık yerine göre 1-3 ay veya yıl). "
            "- **Çok Uzun (Yıllar):** Lepra (2-10 yıl), Kuru ve Creutzfeldt-Jakob prion hastalıkları (30 yıla kadar)."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Patojenin konağa girdiği an ile ilk klinik semptomun belirdiği an arasındaki süreye inkübasyon dönemi denir.",
                "inkübasyon dönemi",
                "Klinik sessizlik içinde patojen çoğalma süresi"
            ),
            make_table(
                "Farklı Enfeksiyonların Tipik İnkübasyon Aralıkları",
                ["Hastalık Tablosu", "Etken Mikroorganizma", "Tipik İnkübasyon Süresi", "Süreyi Belirleyen Temel Dinamik"],
                [
                    ["Stafilokokal intoksikasyon", "S. aureus enterotoksini", "1 - 6 saat", "Önceden hazır toksin etkisi"],
                    ["İnfluenza (Grip)", "İnfluenza virüsü", "1 - 4 gün", "Üst solunum epitelinde hızlı replikasyon"],
                    ["Suçiçeği (Varisella)", "Varisella Zoster Virüsü", "10 - 21 gün", "Primer ve sekonder viremi evreleri"],
                    ["Kuduz (Rabies)", "Rabies lyssavirus", "1 - 3 ay (yıllara dek)", "Periferik sinirden SSS'ye aksonal göç"]
                ],
                hidden_coords=[(0, 2), (1, 2), (2, 2), (3, 2)],
                hints=[
                    "Birkaç saatlik çok kısa zehirlenme tablosu",
                    "Birkaç günlük tipik solunum yolu kuluçkası",
                    "İki-üç haftalık viral döküntülü hastalık süresi",
                    "Aylarca süren santral sinir sistemi aksonal taşınması"
                ]
            ),
            make_micro_quiz(
                "İnkübasyon süresinin klinik ve epidemiyolojik önemi ile ilgili aşağıdakilerden hangisi yanlıştır?",
                {
                    "A": "İnkübasyon süresi patojenin inokulum dozu ve konağın immünitesiyle ters orantılı kısalabilir",
                    "B": "Preforme toksinlerle oluşan gıda intoksikasyonlarında kuluçka süresi saatler kadar kısadır",
                    "C": "Kuduzda santral sinir sistemine yakın ısırıklarda inkübasyon süresi daha kısa sürer",
                    "D": "İnkübasyon süresince hasta her zaman tamamen bulaştırıcısızdır ve mikrop saçamaz",
                    "E": "Karantina süreleri belirlenirken ilgili hastalığın bilinen en uzun inkübasyon süresi esas alınır"
                },
                "D",
                "Doğru cevap D'dir: Kızamık, suçiçeği ve SARS-CoV-2 gibi pek çok viral enfeksiyonda semptomlar başlamadan 1-2 gün önce (inkübasyonun son evresinde) yüksek düzeyde viral saçılım ve bulaştırıcılık mevcuttur. A, B, C ve E seçeneklerindeki prensipler epidemiyolojik olarak tamamen doğrudur."
            )
        ]
    })

    # Slayt 84: Üçüncü Evre: Prodromal Dönem ve Sistemik Semptomlar
    slides.append({
        "id": "k1-21-s84",
        "title": "Üçüncü Evre: Prodromal Dönem ve Sistemik Semptomlar",
        "section": "Enfeksiyon Hastalığının Doğal Seyri ve Klinik Evreleri",
        "slideNumber": 84,
        "narrative": (
            "İnkübasyonun ardından gelen **prodromal dönem**, enfeksiyon hastalığının ilk klinik işaretlerinin "
            "ortaya çıktığı ancak hastalığa özgü patognomonik bulguların henüz belirmemiği ara evredir. "
            "Bu evre genellikle 1 ila 3 gün sürer. "
            "Klinik tabloyu oluşturan semptomlar tamamen **özgül olmayan (non-spesifik)** sistemik yakınmalardır: "
            "Halsizlik, kırgınlık (malez), iştahsızlık, subfebril veya hafif ateş, baş ağrısı, miyalji ve yaygın eklem sızısı. "
            "Fizyopatolojik olarak bu tablonun nedeni, patojenin çoğalmasıyla aktive olan makrofaj ve dentritik "
            "hücrelerden salgılanan pirojenik sitokinlerdir (**İnterlökin-1, İnterlökin-6, TNF-alfa ve İnterferonlar**). "
            "Bu sitokinler hipotalamustaki termoregülasyon merkezini etkileyerek ateşi tetikler ve kas dokusunda katabolizmayı artırır. "
            "Hekim bu evrede yalnızca bu bulgulara dayanarak spesifik hastalığın tanısını koymakta zorlanır."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Prodromal dönemde görülen halsizlik ve ateş gibi özgül olmayan semptomların temel kaynağı interlökin-1 ve TNF gibi endojen sitokin salınımıdır.",
                "sitokin salınımıdır",
                "İnflamatuar aracı moleküllerin sistemik dolaşıma dökülmesi"
            ),
            make_causal_chain(
                "Prodromal Belirtilerin Sitokin Aracılı Patofizyolojisi",
                [
                    "1. Patojen Kritik Eşik: Mikroorganizma dokuda antijen sunumunu tetikleyecek yoğunluğa ulaşır.",
                    "2. Makrofaj Aktivasyonu: TLR reseptörleri üzerinden IL-1, IL-6 ve TNF-alfa sentezlenir.",
                    "3. Hipotalamik Uyarı: Prostaglandin E2 artışı ile termostat ayar noktası yükseltilir.",
                    "4. Sistemik Yanıt: Hasta üşüme, titreme, baş ağrısı ve halsizlik hissetmeye başlar.",
                    "5. Kararsız Klinik: Bulgular pek çok enfeksiyonda ortak olduğundan özgül tanı konamaz."
                ]
            ),
            make_active_recall(
                "Prodromal dönem ile akut hastalık dönemi arasındaki en temel tanısal fark nedir?",
                "Prodromal dönemde yalnızca özgül olmayan sistemik belirtiler (halsizlik, subfebril ateş) varken, akut dönemde hastalığa özgü patognomonik bulgular ortaya çıkar.",
                "Spesifik tanı koydurucu klinik bulguların varlığı"
            )
        ]
    })

    # Slayt 85: Dördüncü Evre: Hastalık (Akut / Klinik / Akme) Dönemi
    slides.append({
        "id": "k1-21-s85",
        "title": "Dördüncü Evre: Hastalık (Akut / Klinik / Akme) Dönemi",
        "section": "Enfeksiyon Hastalığının Doğal Seyri ve Klinik Evreleri",
        "slideNumber": 85,
        "narrative": (
            "Enfeksiyon hastalığının **akut (klinik / akme)** dönemi, patojen çoğalmasının, salgılanan toksinlerin "
            "ve konak immün yanıtına bağlı doku harabiyetinin **en üst düzeye (zirve / pik noktaya)** ulaştığı evredir. "
            "Bu evrenin ayırt edici özelliği, hastalığa özgül ve tanı koydurucu **patognomonik belirti ve bulguların** "
            "tüm şiddetiyle sahneye çıkmasıdır: "
            "- Kızamıkta bukkal mukozada Koplik lekeleri ve sefalokaudal yayılan makülopapüler döküntü, "
            "- Viral hepatitte belirgin sklera ve cilt sarılığı ile karaciğer hassasiyeti, "
            "- Menenjitte fışkırır tarzda kusma, ense sertliği ve Kernig-Brudzinski pozitifliği, "
            "- Tifoda basamaklı yükselen yüksek ateş, rölatif bradikardi (Faget belirtisi) ve gül lekeleri. "
            "Patojen yükü ve inflamatuar hasar maksimumdur; konak savunması yetersiz kalırsa bu evrede septik şok, "
            "çoklu organ yetmezliği veya ölüm gerçekleşebilir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Hastalığın en şiddetli yaşandığı ve patognomonik klinik bulguların belirdiği zirve evreye akme veya akut dönem denir.",
                "akut dönem",
                "Klinik tablonun en tepeye ulaştığı faz"
            ),
            make_table(
                "Akut Klinik Evrede Hastalıklara Özgü Patognomonik Bulgular",
                ["Enfeksiyon Tablosu", "Tipik Etken Patojen", "Karakteristik Klinik / Patognomonik Bulgu", "Etkilenen Hedef Doku"],
                [
                    ["Kızamık (Rubeola)", "Morbillivirus", "Koplik lekeleri ve makülopapüler döküntü", "Solunum mukozası ve deri"],
                    ["Akut Hepatit", "Hepatit virüsleri (A-E)", "Sarılık (ikter), kolüri ve hepatomegali", "Karaciğer hepatositleri"],
                    ["Akut Bakteriyel Menenjit", "N. meningitidis / S. pneum.", "Ense sertliği ve fışkırır kusma", "Leptomeninksler ve BOS"],
                    ["Tetanoz", "C. tetani (Tetanospazmin)", "Trismus (çene kilitlenmesi) ve opistotonus", "GABAerjik internöronlar"]
                ],
                hidden_coords=[(0, 2), (1, 2), (2, 2), (3, 2)],
                hints=[
                    "Ağız içi mukoza lekesi ve birleşik deri lezyonları",
                    "Bilirubin yüksekliğine bağlı göz ve cilt rengi değişimi",
                    "Meningeal irritasyonun klasik fizik muayene bulgusu",
                    "İnhibitör iletim bloke olunca gelişen rijit kas spazmı"
                ]
            ),
            make_micro_quiz(
                "Enfeksiyon hastalığının klinik (akme) dönemi ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
                {
                    "A": "Patojen yükü ve immün aracılı doku hasarı genellikle maksimum seviyededir",
                    "B": "Hastalığa özgü karakteristik ve patognomonik bulgular bu evrede ortaya çıkar",
                    "C": "Hastalık dönemi daima tam şifa ile sonlanır, ölüm veya sekel riski bu evrede bulunmaz",
                    "D": "Konak defansının mikroorganizmayı sınırlandıramadığı durumlarda sepsis ve şok gelişebilir",
                    "E": "Laboratuvarda akut faz reaktanları (CRP, prokalsitonin) ve spesifik antijenler en yüksek düzeydedir"
                },
                "C",
                "Doğru cevap C'dir: Akut hastalık dönemi ölüm (fatalite), kalıcı sekel veya organ yetmezliği riskinin en yüksek olduğu dönemdir; asla kendiliğinden daima tam şifayla sonlanacağı söylenemez. Diğer seçenekler akut dönemin temel patofizyolojik özellikleridir."
            )
        ]
    })

    # Slayt 86: Enfeksiyon Hastalıklarının Sonlanım Çeşitleri (Akıbet)
    slides.append({
        "id": "k1-21-s86",
        "title": "Enfeksiyon Hastalıklarının Sonlanım Çeşitleri (Akıbet)",
        "section": "Enfeksiyon Hastalığının Doğal Seyri ve Klinik Evreleri",
        "slideNumber": 86,
        "narrative": (
            "Akut hastalık döneminin ardından enfeksiyonun seyri konağın direncine, patojenin özelliklerine ve "
            "uygulanan tıbbi tedaviye bağlı olarak farklı yollar izleyebilir. Bir enfeksiyon hastalığının temel "
            "sonlanım (akıbet) biçimleri şunlardır: "
            "1. **Tam Şifa (Rezolüsyon / Restitutio ad integrum):** Patojen vücuttan bütünüyle temizlenir, dokular "
            "anatomik ve fonksiyonel olarak tamamen normale döner. "
            "2. **Sekel ile İyileşme:** Mikroorganizma temizlenir ancak dokuda oluşturduğu hasar kalıcı sakatlığa yol açar "
            "(ör. çocuk felci sonrası flask paralizi, bakteriyel menenjit sonrası işitme kaybı). "
            "3. **Kronikleşme:** İmmün yanıt patojeni bütünüyle yok edemez; aktif enfeksiyon ve doku inflamasyonu aylarca/yıllarca "
            "düşük yoğunlukta sürer (ör. Kronik Hepatit B ve C). "
            "4. **Latentlik (Uyku Evresi):** Patojen sessizce hücre içinde kalır, klinik semptom yoktur ancak ileride reaktive olabilir (HSV, VZV, tüberküloz). "
            "5. **Taşıyıcılık (Portörlük):** Konak tamamen sağlıklıdır ancak mikrobu etrafa saçmaya devam eder (Salmonella Typhi safra kesesi portörlüğü). "
            "6. **Ölüm (Eksitus):** Aşırı doku hasarı, septik şok veya çoklu organ disfonksiyonu sonucu konak kaybedilir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Mikroorganizmanın vücuttan tamamen temizlenip dokuların anatomik ve fonksiyonel olarak normale dönmesine tam şifa veya rezolüsyon adı verilir.",
                "tam şifa",
                "Eksiksiz anatomik ve işlevsel düzelme durumu"
            ),
            make_before_after(
                "Tam Şifa ve Sekel Bırakarak İyileşme Karşılaştırması",
                "Tam Şifa (Rezolüsyon)",
                "Patojen tamamen elimine edilir, parankim hücreleri rejenere olur, organ fonksiyonları eski sağlıklı durumuna eksiksiz döner.",
                "Sekel ile Sonlanım",
                "Patojen vücuttan temizlenmiş olsa bile sinir hasarı, nekroz veya fibrozis nedeniyle kalıcı organ disfonksiyonu kalır.",
                "Enfeksiyon sonrası doku rejenerasyonu ile kalıcı defekt oluşumunun ayrımı"
            ),
            make_branching_logic(
                "35 yaşında erkek hasta akut Hepatit B tanısı almış ve 6 aydır takip edilmektedir. Kontrol tahlillerinde HBsAg pozitifliği devam etmekte, karaciğer enzimleri dalgalı seyretmektedir. Bu klinik gidişat ve yönetimle ilgili en doğru karar hangisidir?",
                [
                    {
                        "text": "Akut dönemin 6 aydan uzun sürmesi ve HBsAg'nin pozitif kalması tablonun Kronik Hepatit B'ye evrildiğini gösterir; hasta kronik hepatit protokolüne alınmalıdır.",
                        "isCorrect": True,
                        "explanation": "Doğru. Hepatit B enfeksiyonunda HBsAg'nin 6 aydan uzun süre serumda pozitif kalması 'kronikleşme' kriteridir ve takip/tedavi stratejisi kronik hepatit yönetimine göre yeniden şekillendirilir."
                    },
                    {
                        "text": "Bu durum tam şifadır, karaciğer enzimlerinin yüksekliği sadece geçici beslenme bozukluğuna bağlıdır.",
                        "isCorrect": False,
                        "explanation": "Yanlış. HBsAg 6 aydan uzun süre kanda pozitifse tam şifadan (rezolüsyon) bahsedilemez; virüs kalıcı hale gelmiştir."
                    },
                    {
                        "text": "Hastada sekel kalmıştır ve virüs vücuttan temizlenmiştir, bu nedenle hiçbir takip gerekmez.",
                        "isCorrect": False,
                        "explanation": "Yanlış. HBsAg pozitifliği virüsün aktif varlığını gösterir, temizlendiği anlamına gelmez."
                    },
                    {
                        "text": "HBsAg pozitifliği sadece hastanın aşılandığını gösterir, virüs taşıyıcılığı söz konusu değildir.",
                        "isCorrect": False,
                        "explanation": "Yanlış. Aşılanmış kişilerde Anti-HBs pozitiftir; HBsAg pozitifliği aktif virüs replikasyonunu ve enfeksiyonu simgeler."
                    }
                ]
            )
        ]
    })

    # Slayt 87: Beşinci Evre: Nekahat (Konvalesan) Dönemi ve Portörlük Riski
    slides.append({
        "id": "k1-21-s87",
        "title": "Beşinci Evre: Nekahat (Konvalesan) Dönemi ve Portörlük Riski",
        "section": "Enfeksiyon Hastalığının Doğal Seyri ve Klinik Evreleri",
        "slideNumber": 87,
        "narrative": (
            "**Nekahat (konvalesan / iyileşme) dönemi**, akut enfeksiyon belirtilerinin kaybolmaya başladığı, "
            "hastanın kendini giderek daha iyi hissettiği ve doku onarımının hızlandığı evredir. "
            "Bu dönemde spesifik humoral ve hücresel immünite (özellikle yüksek titrede koruyucu IgG antikorları ve "
            "bellek T hücreleri) sahaya hakimdir ve patojen yükü hızla geriletilir. "
            "**Enfeksiyon Hastalıklarında En Kritik Klinik Kural:** "
            "Klinik iyileşme (semptomların yok olması), her zaman mikrobiyolojik kür (mikrobun vücuttan tamamen temizlenmesi) "
            "anlamına gelmez! "
            "Pek çok hastalıkta (örneğin Salmonella tifo, kolera, boğmaca, difteri) hasta klinik olarak tamamen iyileşmiş "
            "ve kendini sağlıklı hissediyor olsa bile, dışkı, idrar veya solunum sekresyonlarıyla dış ortama canlı mikrop "
            "saçmaya devam edebilir. Bu duruma **konvalesan portörlük (taşıyıcılık)** denir ve toplum sağlığı açısından "
            "en sinsi salgın kaynaklarından birini oluşturur."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Klinik olarak iyileşen bireylerin mikroorganizmayı çevreye saçmaya devam etmesi durumuna konvalesan portörlük denir.",
                "konvalesan portörlük",
                "İyileşme evresinde süregiden bulaştırıcılık hali"
            ),
            make_before_after(
                "Nekahat Döneminde Klinik İyileşme ve Mikrobiyolojik Durum",
                "Görünen Klinik Tablo",
                "Ateş düşmüştür, ağrılar kaybolmuştur, hastanın iştahı ve genel güç durumu normale yaklaşmaktadır.",
                "Gizli Mikrobiyolojik Gerçek",
                "Organlarda kalan az sayıdaki patojen dış ortama saçılmayı sürdürebilir; bulaştırıcılık devam edebilir.",
                "Semptomsuzluk hissi ile etken yayılımının birbirinden bağımsız seyredebileceği gerçeği"
            ),
            make_active_recall(
                "Nekahat döneminde kanda pik yapan ve uzun süreli bağışıklığı sağlayan immünglobulin sınıfı hangisidir?",
                "İmmünglobulin G (IgG) antikorları pik yapar ve uzun süreli koruyucu humoral bağışıklığı sağlar.",
                "İkincil immün yanıtın majör antikor sınıfı"
            )
        ]
    })

    # Slayt 88: Subklinik (Asemptomatik) Enfeksiyonlar ve Sessiz Bulaştırıcılar
    slides.append({
        "id": "k1-21-s88",
        "title": "Subklinik (Asemptomatik) Enfeksiyonlar ve Sessiz Bulaştırıcılar",
        "section": "Enfeksiyon Hastalığının Doğal Seyri ve Klinik Evreleri",
        "slideNumber": 88,
        "narrative": (
            "Enfeksiyon her zaman belirgin bir hastalık tablosuyla sonuçlanmaz. Mikroorganizmanın vücuda girip "
            "çoğaldığı, immün yanıt oluşturduğu (serokonversiyon sağladığı) ancak konakta **hiçbir klinik belirti "
            "veya bulguya yol açmadığı** durumlara **subklinik (asemptomatik / inapparent) enfeksiyon** adı verilir. "
            "Subklinik enfeksiyonlar halk sağlığı ve epidemiyolojide devasa bir buzdağının su altındaki görünmeyen kısmıdır: "
            "- **Poliomiyelit (Çocuk Felci):** Virüsü alanların %90-95'inde enfeksiyon tamamen subkliniktir; sadece %1'den azında felç gelişir. "
            "- **Hepatit A:** Küçük çocuklarda %80'in üzerinde sarılıksız ve asemptomatik seyrederken, erişkinlerde ağır sarılık yapar. "
            "- **SARS-CoV-2:** Popülasyonun önemli bir kısmı asemptomatik veya çok hafif geçirerek toplumsal yayılımı sürdürmüştür. "
            "Asemptomatik bireyler kendilerini hasta hissetmedikleri için toplum içinde serbestçe dolaşır, izolasyon önlemi "
            "almazlar ve enfeksiyon zincirinin en tehlikeli sessiz bulaştırıcıları (vektörleri) haline gelirler."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Kişide semptom görülmemesine rağmen patojenin çoğalıp immün yanıt oluşturduğu tablolara subklinik enfeksiyon denir.",
                "subklinik enfeksiyon",
                "Klinik bulgu vermeyen sessiz patolojik süreç"
            ),
            make_table(
                "Klinik Hastalık ile Subklinik Enfeksiyonun Karşılaştırmalı Özellikleri",
                ["Özellik Parametresi", "Belirgin Klinik Enfeksiyon", "Subklinik (Asemptomatik) Enfeksiyon"],
                [
                    ["Klinik Semptomlar", "Mevcut (ateş, ağrı, organ disfonksiyonu)", "Tamamen yoktur (birey kendini sağlıklı hisseder)"],
                    ["Patojen Çoğalması", "Yüksek yoğunlukta ve doku yıkıcı", "Düşük/orta düzeyde, doku harabiyeti sınırlı"],
                    ["Spesifik Antikor Yanıtı", "Gelişir (IgM ve ardından IgG)", "Gelişir (serokonversiyon pozitifleşir)"],
                    ["Toplumsal Bulaş Riski", "Hasta yattığı/izole olduğu için kısıtlanabilir", "Hasta dolaşımda olduğu için sinsi ve yüksektir"]
                ],
                hidden_coords=[(0, 2), (2, 2), (3, 2)],
                hints=[
                    "Bireyde şikayet bulunmaması hali",
                    "İmmün sistemin sessizce hafıza oluşturması",
                    "İzolasyon uygulanmadığı için kontrolsüz yayılım"
                ]
            ),
            make_micro_quiz(
                "Subklinik (asemptomatik) enfeksiyonların epidemiyolojik önemi ile ilgili hangisi en doğrudur?",
                {
                    "A": "Subklinik enfeksiyon geçiren kişilerde hiçbir zaman antikor oluşmaz ve bağışıklık gelişmez",
                    "B": "Semptom göstermeyen kişiler enfeksiyon etkenini çevreye bulaştıramazlar",
                    "C": "Kendilerini hasta hissetmeyip toplumda dolaştıkları için salgınların yayılmasında birincil rol oynarlar",
                    "D": "Poliomiyelit virüsü ile enfekte olanların %99'unda ağır klinik felç gelişir",
                    "E": "Subklinik enfeksiyonlar yalnızca hayvanlarda görülür, insanlarda her mikrop hastalık yapar"
                },
                "C",
                "Doğru cevap C'dir: Subklinik enfeksiyon geçirenler semptom hissetmediklerinden günlük aktivitelerine ve sosyal temaslarına devam ederler, böylece patojeni çevreye yayarak gizli bulaş zincirini beslerler. A yanlıştır çünkü serokonversiyon ve bağışıklık gelişir; B yanlıştır çünkü bulaştırıcıdırlar; D yanlıştır çünkü polioda %90-95 asemptomatiktir."
            )
        ]
    })

    # Slayt 89: [TEKRAR SAYFASI - CHECKPOINT 9] Enfeksiyon Hastalığının Doğal Seyri
    slides.append({
        "id": "k1-21-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Enfeksiyon Hastalığının Doğal Seyri",
        "section": "Enfeksiyon Hastalığının Doğal Seyri ve Klinik Evreleri",
        "slideNumber": 89,
        "narrative": (
            "Bu checkpoint sayfasında enfeksiyon hastalığının doğal seyri ve klinik evrelerine ait "
            "en kritik mekanizmaları pekiştiriyoruz: "
            "1. **İnkübasyon Dönemi:** Giriş ile ilk belirti arasındaki sessiz çoğalma aralığıdır. "
            "2. **Prodromal Dönem:** Halsizlik, baş ağrısı ve subfebril ateş gibi sitokin kaynaklı özgül olmayan belirtilerin evresidir. "
            "3. **Akut Dönem:** Patognomonik bulguların ve patojen yükünün zirveye ulaştığı fazdır. "
            "4. **Nekahat ve Portörlük:** İyileşme evresinde klinik semptomlar bitse bile mikroorganizma saçılımı sürebilir. "
            "5. **Subklinik Enfeksiyon:** Buzdağının görünmeyen tabanıdır; semptomsuz antikor geliştiren ve mikrobu yayan kişilerdir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_flashcard(
                "k1-21-fc-25",
                "Enfeksiyon etkeninin vücuda girmesi ile ilk klinik belirti veya bulguların ortaya çıkması arasında geçen sessiz süreye ne ad verilir?",
                "İnkübasyon (kuluçka) dönemi",
                "Patojenin semptom oluşturmaksızın geometrik olarak çoğaldığı evre",
                "Klinik Seyir"
            ),
            make_flashcard(
                "k1-21-fc-26",
                "Özgül olmayan genel halsizlik, hafif ateş ve baş ağrısı gibi semptomların görüldüğü, hastalığa has patognomonik bulguların henüz belirmediği evre hangisidir?",
                "Prodromal dönem",
                "Akut klinik tablodan hemen önce gelen haberci faz",
                "Klinik Seyir"
            ),
            make_flashcard(
                "k1-21-fc-27",
                "Klinik semptomların tamamen kaybolduğu nekahat döneminde patojenin vücuttan dış ortama atılmaya devam etmesi durumuna ne denir?",
                "Konvalesan taşıyıcılık (portörlük)",
                "İyileşme sonrası çevreyi enfekte etme potansiyelinin sürmesi hali",
                "Klinik Seyir"
            )
        ]
    })

    # Slayt 90: Bölüm Özeti: Klinik Seyirden Tanı ve Tedavi İlkelerine Geçiş
    slides.append({
        "id": "k1-21-s90",
        "title": "Bölüm Özeti: Klinik Seyirden Tanı ve Tedavi İlkelerine Geçiş",
        "section": "Enfeksiyon Hastalığının Doğal Seyri ve Klinik Evreleri",
        "slideNumber": 90,
        "narrative": (
            "Enfeksiyon hastalığının klinik evrelerini bilmek hekime üç hayati avantaj sağlar: "
            "Birincisi, doğru evrede doğru tanı yöntemini seçmek (örneğin inkübasyon sonu veya erken prodromda PCR/antijen, "
            "nekahatte ise IgG antikor testleri tercih edilir). "
            "İkincisi, ampirik veya hedefe yönelik tedaviyi zamanında başlatarak akut evrede gelişebilecek geri dönüşümsüz "
            "doku harabiyetini, sepsisi ve ölümü engellemek. "
            "Üçüncüsü, nekahat veya asemptomatik evredeki bireyleri tespit ederek bulaşma zincirini kırmak ve toplum "
            "sağlığını korumaktır. "
            "Bir sonraki ve son bölümümüzde, mikrobiyolojik tanı testleri, seroloji, moleküler yöntemler (PCR), "
            "akılcı antibiyotik kullanımı, hastane enfeksiyonları ve küresel enfeksiyon tehditleri incelenecektir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Hastalığın erken evresinde etkenin kendisi veya genetik materyali aranırken nekahat evresinde spesifik IgG antikorları araştırılır.",
                "IgG antikorları",
                "Geçirilmiş enfeksiyonu ve bağışıklığı gösteren immünglobulin sınıfı"
            ),
            make_causal_chain(
                "Klinik Evreye Göre Tanısal Yaklaşım Mantığı",
                [
                    "1. Giriş ve İnkübasyon Sonu: Virüs veya bakteri yükü yüksektir; nükleik asit (PCR) pozitifleşir.",
                    "2. Akut Dönem: Patojen antijenleri kanda veya sekresyonda saptanır; erken IgM yükselmeye başlar.",
                    "3. Nekahat Başı: Patojen temizlenirken IgM pik yapar, ardından yerini IgG'ye bırakır.",
                    "4. Geç İyileşme: IgM negatifleşir; yüksek afiniteli IgG pozitifliği kalıcı bağışıklığı belgeler."
                ]
            ),
            make_active_recall(
                "Akut bir enfeksiyon şüphesinde erken dönemde neden serolojik antikor taraması yerine direkt mikroskopi, kültür veya PCR tercih edilir?",
                "Çünkü antikorların (IgM/IgG) saptanabilir düzeye ulaşması için 7-14 günlük bir latent periyot gerekir (pencere dönemi); erken dönemde seroloji yalancı negatif sonuç verir.",
                "Pencere dönemi ve antikor sentez hızı kısıtı"
            )
        ]
    })

    return slides
