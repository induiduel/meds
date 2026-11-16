# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec3():
    slides = []

    # Slide 21: Konak Savunması ve Anatomik/Fizyolojik Bariyerler
    s21_narrative = (
        "İnsan üriner traktusu, mikroorganizmaların sürekli tehdidine karşı son derece etkili "
        "mekanik, kimyasal ve immünolojik savunma mekanizmalarıyla donatılmıştır.\n\n"
        "- **Savunma Grupları:** Konak savunma mekanizmaları iki ana grupta incelenir: 1) Mekanik "
        "ve kimyasal bariyerler, 2) İmmün yanıt.\n"
        "- **Bariyer Bütünlüğü:** Üriner sistemin anatomik bütünlüğü ve ürotelyumun sağlam mukozal "
        "bariyeri, bakterilerin submukozal dokulara penetre olmasını mekanik olarak engeller.\n"
        "- **İşeme Yıkaması:** Normal işeme fonksiyonu, mesaneye ulaşmayı başaran mikroorganizmaları "
        "düzenli idrar akımıyla dışarı sürükleyen en temel dinamik temizleme mekanizmasıdır.\n\n"
        "> [!NOTE]\n"
        "> Üriner sistemin anatomik bütünlüğü, mukozal bariyer ve normal işeme fonksiyonu en temel mekanik savunma unsurlarını oluşturur."
    )
    s21_bullets = [
        "Konak savunması: 1) Mekanik ve kimyasal bariyerler, 2) İmmün yanıt.",
        "Üriner sistemin anatomik bütünlüğü ve mukozal bariyer fiziksel koruma sağlar.",
        "Normal işeme fonksiyonu bakterileri mekanik olarak lümenden yıkayıp uzaklaştırır."
    ]
    s21_elements = [
        make_cloze("Konak savunmasında normal işeme fonksiyonu bakterileri idrar akımı ile mekanik olarak dışarı atar.", "normal işeme fonksiyonu", "İdrarın periyodik boşaltılması ile sağlanan yıkama"),
        make_table("Mekanik ve Fiziksel Savunma Unsurları", ["Savunma Bileşeni", "Etki Mekanizması", "Koruyucu Sonuç"], [
            {"cells": [{"text": "Anatomik Bütünlük", "isMasked": False}, {"text": "Ürotelyumun kesintisiz örtüsü", "isMasked": True, "hint": "sağlam mukoza tabakası"}, {"text": "Doku invazyonunu engelleme"}]},
            {"cells": [{"text": "Normal İşeme", "isMasked": False}, {"text": "Yıkama ve lümen akımı", "isMasked": False}, {"text": "Bakterilerin mekanik klirensi", "isMasked": True, "hint": "akımla mikropların sürüklenmesi"}]}
        ]),
        make_chain("Mekanik Savunma Akış Şeması", [
            "1. Bakteriyel Giriş: Mikroorganizmanın distal üretraya sızması.",
            "2. Mukozal Bariyer: Sağlam ürotelyal yüzeye çarpması.",
            "3. İdrar Birikimi: Mesanede idrar dolumu ve işeme hissi.",
            "4. İşeme Klirensi: Yüksek akımlı idrarla bakterilerin dışarı atılması."
        ]),
        make_recall("Konak savunma mekanizmalarının iki ana grubu nedir?", "1) Mekanik ve kimyasal bariyerler, 2) İmmün yanıttır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Mekanik Savunma", [
            {"text": "Konak savunması mekanik/kimyasal bariyerler ve immün yanıt olmak üzere ikiye ayrılır.", "isLie": False, "explanation": "Doğru. Ders notu sınıflamasıdır."},
            {"text": "Normal işeme fonksiyonu bakterileri lümenden yıkayarak koruma sağlar.", "isLie": False, "explanation": "Doğru. Mekanik klirens sağlar."},
            {"text": "İdrar yapmamak ve idrarı günlerce mesanede bekletmek en güçlü konak savunma yöntemidir.", "isLie": True, "explanation": "Tuzak! İdrar stazı bakteriyel çoğalmayı artırır; tersine normal işeme fonksiyonu koruyucudur."},
            {"text": "Üriner sistemin anatomik bütünlüğü ve mukozal bariyer fiziksel koruma sunar.", "isLie": False, "explanation": "Doğru. Mekanik bariyerdir."}
        ]),
        make_quiz("Üriner sistemde bakterilerin tutunmasını ve çoğalmasını engelleyen MEKANİK savunma faktörleri arasında aşağıdakilerden hangisi yer alır?", [
            {"key": "A", "text": "Üriner sistemin anatomik bütünlüğü, mukozal bariyer ve normal işeme fonksiyonu", "isCorrect": True, "explanation": "Ders notunda mekanik ve kimyasal bariyerlerin ilk maddesi olarak açıkça belirtilmiştir."},
            {"key": "B", "text": "Yalnızca kemik iliğinde eritrosit üretilmesi", "isCorrect": False, "explanation": "Üriner mekanik savunma ile ilgisi yoktur."},
            {"key": "C", "text": "Gastrik asit salgılanması", "isCorrect": False, "explanation": "Mide savunmasıdır, üriner sistem değildir."},
            {"key": "D", "text": "Karaciğerde albümin sentezinin durması", "isCorrect": False, "explanation": "Alakasız bir patolojik tablodur."}
        ])
    ]
    slides.append(make_slide(21, "Konak Savunması: Mekanik ve Fiziksel Bariyerler", "Anatomik bütünlük, mukozal bariyer ve normal işemenin koruyucu etkisi", "Konak Savunması", s21_narrative, s21_bullets, s21_elements))

    # Slide 22: İdrarın Koruyucu Kimyasal Özellikleri
    s22_narrative = (
        "İdrar yalnızca atık maddeleri taşıyan pasif bir sıvı olmayıp, kimyasal bileşimi ve "
        "biyokimyasal özellikleri ile birçok mikroorganizmanın çoğalmasını doğrudan baskılar.\n\n"
        "- **Kimyasal Özellikler:** İdrarın koruyucu özellikleri **yüksek osmolarite, yüksek üre "
        "konsantrasyonu ve düşük pH** değerleridir.\n"
        "- **Bakteriostatik Etki:** Yüksek osmolarite ve yüksek konsantrasyondaki üre bakteriyel "
        "hücre zarında ozmotik stres oluşturarak bakteri çoğalmasını inhibe eder.\n"
        "- **Asidik Ortam:** İdrarın fizyolojik düşük pH'sı (asidik yapısı) çoğu patojenik enterik "
        "bakterinin enzimatik aktivitelerini ve optimal üreme koşullarını bozar.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] İdrarın koruyucu antibakteriyel özellikleri: Yüksek osmolarite, yüksek üre ve düşük pH'dır."
    )
    s22_bullets = [
        "İdrarın antibakteriyel özellikleri: Yüksek osmolarite, yüksek üre, düşük pH.",
        "Yüksek osmolarite ve üre bakteriyel hücre zarlarında ozmotik baskılama yapar.",
        "Düşük pH (asidik idrar) bakteriyel enzim sistemlerini inhibe eder."
    ]
    s22_elements = [
        make_cloze("İdrarın bakteriyel çoğalmayı engelleyen özellikleri yüksek osmolarite, yüksek üre ve düşük pH değerleridir.", "yüksek osmolarite, yüksek üre ve düşük pH", "İdrarın üç temel koruyucu fizikokimyasal özelliği"),
        make_table("İdrarın Koruyucu Kimyasal Parametreleri", ["Fizikokimyasal Parametre", "Biyokimyasal Durum", "Antibakteriyel Etki Mekanizması"], [
            {"cells": [{"text": "Osmolarite", "isMasked": False}, {"text": "Yüksek osmolarite", "isMasked": True, "hint": "yoğun ozmotik basınç"}, {"text": "Bakteriyel su kaybı ve hücre stresi"}]},
            {"cells": [{"text": "Üre Konsantrasyonu", "isMasked": False}, {"text": "Yüksek üre düzeyi", "isMasked": False}, {"text": "Protein denatürasyonu ve üreme inhibisyonu", "isMasked": True, "hint": "üre kaynaklı kimyasal baskılama"}]},
            {"cells": [{"text": "İdrar pH'sı", "isMasked": False}, {"text": "Düşük pH (asidik)", "isMasked": True, "hint": "asit idrar ortamı"}, {"text": "Patojenlerin enzim aktivitesini engelleme"}]}
        ]),
        make_chain("İdrarın Kimyasal Savunma Mekanizması", [
            "1. Filtrasyon: Böbreklerden yoğun üre ve elektrolit atılımı.",
            "2. Yüksek Osmolarite: İdrarın konsantre hale gelmesi.",
            "3. Düşük pH Oluşumu: Tübüler asidifikasyonla asit idrar üretimi.",
            "4. Bakteriyel Baskılanma: Patojenlerin çoğalmasının kimyasal olarak durdurulması."
        ]),
        make_recall("Ders notuna göre idrarın mikroorganizma çoğalmasını engelleyen üç temel koruyucu özelliği nedir?", "Yüksek osmolarite, yüksek üre ve düşük pH'dır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İdrarın Koruyucu Özellikleri", [
            {"text": "İdrarın yüksek osmolaritesi bakteri çoğalmasını baskılar.", "isLie": False, "explanation": "Doğru. Ders notu özelliğidir."},
            {"text": "Yüksek üre konsantrasyonu idrarın koruyucu unsurlarındandır.", "isLie": False, "explanation": "Doğru. Antibakteriyel etkilidir."},
            {"text": "İdrarın aşırı alkali (pH >9) ve saf distile su gibi düşük osmolaritede olması en güçlü koruyucu durumdur.", "isLie": True, "explanation": "Tuzak! Koruyucu özellikler yüksek osmolarite, yüksek üre ve düşük pH'dır."},
            {"text": "Düşük idrar pH'sı mikroorganizmaların optimal üremesini engeller.", "isLie": False, "explanation": "Doğru. Asidik ortam koruyucudur."}
        ]),
        make_quiz("İdrarın mikroorganizmalara karşı koruyucu kimyasal özellikleri arasında aşağıdakilerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Yüksek osmolarite, yüksek üre ve düşük pH", "isCorrect": True, "explanation": "Ders notunda harfiyen 'yüksek osmolarite, yüksek üre, düşük pH' olarak geçmektedir."},
            {"key": "B", "text": "Düşük osmolarite, sıfır üre ve alkali pH", "isCorrect": False, "explanation": "Tam tersi özelliklerdir."},
            {"key": "C", "text": "Yüksek glukoz konsantrasyonu ve nötr pH", "isCorrect": False, "explanation": "Glukoz bakteri çoğalmasını kolaylaştırır."},
            {"key": "D", "text": "Yalnızca saf safra asitleri içermesi", "isCorrect": False, "explanation": "İdrarda normalde safra asidi bulunmaz."}
        ])
    ]
    slides.append(make_slide(22, "İdrarın Özellikleri: Osmolarite, Üre ve Düşük pH", "İdrarın bakteriyel çoğalmayı baskılayan fizikokimyasal savunma faktörleri", "Konak Savunması", s22_narrative, s22_bullets, s22_elements))

    # Slide 23: Tamm-Horsfall Proteini ve Prostat Salgısı
    s23_narrative = (
        "Kimyasal savunmanın en özelleşmiş elemanları arasında böbrek tübüllerinden üretilen "
        "özel proteinler ve erkek üreme sistemine ait salgılar yer alır.\n\n"
        "- **Tamm-Horsfall Proteini:** Henle kulpunun çıkan kalın kolu hücrelerinden salgılanan "
        "**Tamm-Horsfall proteinleri (üromodulin)**, idrarda en bol bulunan proteindir.\n"
        "- **Yalancı Reseptör Etkisi:** Bu protein, taşıdığı mannoz kalıntıları ile E. coli'nin "
        "Tip 1 fimbriyalarına bağlanarak bakterileri nötralize eder ve ürotelyuma tutunmasını önler.\n"
        "- **Prostat Salgısı:** Erkeklerde prostat salgısının içerdiği çinko ve bakterisidal peptitler "
        "retrograd bakteriyel kolonizasyonu güçlü biçimde baskılar.\n\n"
        "> [!IMPORTANT]\n"
        "> Tamm-Horsfall proteini idrarda bakterilere bağlanarak üroepitele adezyonu engeller; prostat salgısı ise erkeklerde bakterisidal bariyer oluşturur."
    )
    s23_bullets = [
        "Tamm-Horsfall proteini bakterilere bağlanarak mukozaya adezyonu engeller.",
        "İdrarda en bol bulunan fizyolojik savunma glikoproteinidir.",
        "Prostat salgısı bakterisidal etkisi ile erkek üretrasını korur."
    ]
    s23_elements = [
        make_cloze("Böbreklerden salgılanıp bakterileri bağlayarak mukozaya tutunmasını engelleyen protein Tamm-Horsfall proteinidir.", "Tamm-Horsfall proteinidir", "İdrarda en bol bulunan koruyucu glikoprotein"),
        make_table("Özel Biyokimyasal Savunma Faktörleri", ["Faktör", "Üretim Yeri", "Savunma Fonksiyonu"], [
            {"cells": [{"text": "Tamm-Horsfall Proteini", "isMasked": False}, {"text": "Henle kulpu çıkan kalın kolu", "isMasked": True, "hint": "tübüler nefron segmenti"}, {"text": "Bakterileri bağlayarak adezyonu bloke etme"}]},
            {"cells": [{"text": "Prostat Salgısı", "isMasked": False}, {"text": "Prostat asiner epiteli", "isMasked": False}, {"text": "Bakterisidal antibakteriyel aktivite", "isMasked": True, "hint": "erkekteki kimyasal öldürücü güç"}]}
        ]),
        make_chain("Tamm-Horsfall Koruma Zinciri", [
            "1. Tübüler Salgılanma: Henle çıkan kolundan idrar lümenine verilme.",
            "2. Mannoz Bağlama: E. coli fimbriyalarının proteine yapışması.",
            "3. Serbest Kalma: Bakterinin mesane epiteline tutunamaması.",
            "4. İdrarla Atılım: Kompleksin idrar akımıyla vücuttan uzaklaşması."
        ]),
        make_recall("Tamm-Horsfall proteini üriner sistemde nasıl bir koruyucu fonksiyon icra eder?", "İdrarda bakterilere (fimbriyalara) bağlanarak onların üroepitele tutunmasını (adezyonunu) engeller."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tamm-Horsfall ve Prostat", [
            {"text": "Tamm-Horsfall proteinleri konak savunma mekanizmaları arasında yer alır.", "isLie": False, "explanation": "Doğru. Ders notu mekanik/kimyasal bariyeridir."},
            {"text": "Prostat salgısı erkeklerde bakterisidal etki göstererek koruma sağlar.", "isLie": False, "explanation": "Doğru. Ders notunda belirtilmiştir."},
            {"text": "Tamm-Horsfall proteini bakterileri besleyerek onların 1000 kat daha hızlı üremesini sağlar.", "isLie": True, "explanation": "Tuzak! Tamm-Horsfall proteini koruyucu bir proteindir; bakterilere bağlanarak adezyonu engeller."},
            {"text": "Kimyasal bariyerler idrarın fizikokimyasal özellikleri ile sinerjik çalışır.", "isLie": False, "explanation": "Doğru. Savunma bir bütündür."}
        ]),
        make_quiz("İdrarda bakterilerin üroepitele tutunmasını engelleyen ve konak savunmasında rol oynayan koruyucu protein aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Tamm-Horsfall proteinleri", "isCorrect": True, "explanation": "Ders notunda mekanik ve kimyasal bariyerler arasında 'Tamm-Horsfall proteinleri' açıkça sayılmıştır."},
            {"key": "B", "text": "C-reaktif protein (CRP)", "isCorrect": False, "explanation": "CRP bir akut faz reaktanıdır, idrardaki bu proteini tanımlamaz."},
            {"key": "C", "text": "Bence Jones proteini", "isCorrect": False, "explanation": "Multipl miyelomdaki patolojik immünglobulin hafif zinciridir."},
            {"key": "D", "text": "Kollajen tip 4", "isCorrect": False, "explanation": "Bazal membran yapısal proteinidir."}
        ])
    ]
    slides.append(make_slide(23, "Tamm-Horsfall Proteini ve Prostatik Savunma", "Tamm-Horsfall glikoproteininin anti-adezif rolü ve bakterisidal prostat salgısı", "Konak Savunması", s23_narrative, s23_bullets, s23_elements))

    # Slide 24: İmmün Yanıt: Hücresel ve Hümoral Bileşenler
    s24_narrative = (
        "Mekanik ve kimyasal engeller aşıldığında üriner sistem mukozası hızlı bir immünolojik "
        "alarm durumuna geçerek hücresel ve hümoral yanıtları devreye sokar.\n\n"
        "- **İmmün Bileşenler:** İmmün yanıt kapsamında **fagositik hücreler, sitokinler, komplemanlar "
        "ve salgısal IgA** (doğal hücresel ve hümoral) görev alır.\n"
        "- **Fagositoz:** Ürotelyal bariyeri geçen bakteriler submukozadaki nötrofiller ve makrofajlar "
        "tarafından hızla fagosite edilir.\n"
        "- **Sitokin ve Kompleman:** İnterlökinler (IL-8 vb.) nötrofil göçünü tetiklerken, kompleman "
        "aktivasyonu bakteriyel hücre zarlarını lizise uğratır ve salgısal IgA mukozal adezyonu önler.\n\n"
        "> [!NOTE]\n"
        "> Üriner sistem immün yanıtı: Fagositik hücreler, sitokinler, komplemanlar ve salgısal IgA'dan oluşur."
    )
    s24_bullets = [
        "İmmün yanıt: Fagositik hücreler, sitokinler, komplemanlar, salgısal IgA.",
        "Fagositik hücreler (nötrofiller) dokuya göç ederek bakterileri ortadan kaldırır.",
        "Salgısal IgA mukozal tutunmayı bloke eder, komplemanlar bakteri lizisi sağlar."
    ]
    s24_elements = [
        make_cloze("Konak immün yanıtında yer alan salgısal IgA bakterilerin mukozal yüzeylere tutunmasını engeller.", "salgısal IgA", "Mukozal immünitenin temel immünglobulini"),
        make_table("Üriner Sistem İmmün Yanıt Bileşenleri", ["İmmün Bileşen", "Yanıt Tipi", "Temel Savunma Görevi"], [
            {"cells": [{"text": "Fagositik Hücreler", "isMasked": False}, {"text": "Hücresel immünite (nötrofil/makrofaj)", "isMasked": True, "hint": "yutucu kan hücreleri"}, {"text": "Bakterilerin fagositozu ve yıkımı"}]},
            {"cells": [{"text": "Sitokinler", "isMasked": False}, {"text": "Kimyasal sinyal iletimi", "isMasked": False}, {"text": "Enflamasyon ve lökosit kemotaksisi", "isMasked": True, "hint": "hücreleri çağıran haberciler"}]},
            {"cells": [{"text": "Salgısal IgA ve Kompleman", "isMasked": False}, {"text": "Hümoral immünite", "isMasked": True, "hint": "sıvısal antikor ve protein yanıtı"}, {"text": "Adezyon blokajı ve membran lizisi"}]}
        ]),
        make_chain("Mukozal İmmün Yanıt Zinciri", [
            "1. Patojen Teması: Bakteriyel antijenlerin ürotelyuma teması.",
            "2. Sitokin Salınımı: Epitelden pro-enflamatuar sinyal üretimi.",
            "3. Lökosit Göçü: Nötrofillerin idrar lümenine çekilmesi (piyüri).",
            "4. İmmün Klirens: Salgısal IgA ve fagositlerle bakterilerin temizlenmesi."
        ]),
        make_recall("Ders notuna göre konak immün yanıtını oluşturan dört temel bileşen nedir?", "Fagositik hücreler, sitokinler, komplemanlar ve salgısal IgA'dır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İmmün Yanıt", [
            {"text": "İmmün yanıt fagositik hücreler, sitokinler, komplemanlar ve salgısal IgA'yı içerir.", "isLie": False, "explanation": "Doğru. Ders notu listesidir."},
            {"text": "Fagositik hücreler bakterileri fagositoz yoluyla ortadan kaldırır.", "isLie": False, "explanation": "Doğru. Temel hücresel mekanizmadır."},
            {"text": "Salgısal IgA bakterilerin üremesini 100 kat artıran bir bakteriyel büyüme hormonudur.", "isLie": True, "explanation": "Tuzak! Salgısal IgA konak savunmasına ait bir antikordur, bakteriyi nötralize eder."},
            {"text": "Sitokinler enflamatuar hücre göçünü organize eden sinyal molekülleridir.", "isLie": False, "explanation": "Doğru. Kemotaksis sağlar."}
        ]),
        make_quiz("Üriner sistem enfeksiyonlarına karşı konak immün yanıtının bileşenleri arasında aşağıdakilerden hangisi YER ALIR?", [
            {"key": "A", "text": "Fagositik hücreler, sitokinler, komplemanlar ve salgısal IgA", "isCorrect": True, "explanation": "Ders notunda 'İmmün yanıt: fagositik hücreler, sitokinler, komplemanlar, salgısal IgA' şeklinde tam liste verilmiştir."},
            {"key": "B", "text": "Yalnızca hemoglobin molekülleri", "isCorrect": False, "explanation": "Hemoglobin oksijen taşır, immün yanıt bileşeni değildir."},
            {"key": "C", "text": "Trombosit tıkacı ve fibrin pıhtısı", "isCorrect": False, "explanation": "Bu hemostazdır."},
            {"key": "D", "text": "Saf safra tuzları", "isCorrect": False, "explanation": "Sindirim sistemi salgısıdır."}
        ])
    ]
    slides.append(make_slide(24, "Konak İmmün Yanıtı: Hücresel ve Hümoral Hat", "Fagositik hücreler, sitokinler, kompleman sistemi ve salgısal IgA", "Konak Savunması", s24_narrative, s24_bullets, s24_elements))

    # Slide 25: Patojenite ve Virülans Faktörlerine Genel Giriş
    s25_narrative = (
        "Bir mikroorganizmanın üriner sistemde enfeksiyon oluşturabilmesi, konağın güçlü savunma "
        "bariyerlerini aşabilmesini sağlayan özel virülans donanımlarına bağlıdır.\n\n"
        "- **Virülans Sınıflaması:** Mikroorganizma patojenitesi ve virülans faktörleri dört temel "
        "kategoride toplanır: 1) Tutunma (adezyon), 2) İnvazyon, 3) Konak savunmasından kaçış, 4) Metabolik ihtiyaçlar.\n"
        "- **Patojenik Başarı:** Bu dört basamak birbiri ardına devreye girerek bakterinin idrar akımına "
        "direnmesini, doku hasarı yapmasını ve immün yanıttan kurtulmasını sağlar.\n"
        "- **Üropatojenik Özellik:** Normal bağırsak florasındaki sıradan bakterilerden farklı olarak "
        "üropatojen suşlar (ör. UPEC) bu virülans genlerini plazmid ve patojenite adacıklarında taşır.\n\n"
        "> [!NOTE]\n"
        "> Mikroorganizma virülans faktörleri: 1) Tutunma (adezyon), 2) İnvazyon, 3) Konak savunmasından kaçış, 4) Metabolik ihtiyaçlar olmak üzere dört ana gruptur."
    )
    s25_bullets = [
        "Virülans faktörleri 4 ana grupta incelenir.",
        "1) Tutunma (adezyon), 2) İnvazyon.",
        "3) Konak savunmasından kaçış, 4) Metabolik ihtiyaçlar."
    ]
    s25_elements = [
        make_cloze("Mikroorganizma virülans faktörleri tutunma, invazyon, konak savunmasından kaçış ve metabolik ihtiyaçlar olarak dört başlıkta incelenir.", "metabolik ihtiyaçlar", "Bakterinin demir ve besin teminini sağlayan virülans grubu"),
        make_table("Mikroorganizma Virülans Faktörleri Sınıflaması", ["Virülans Grubu", "Temel İşlev", "Örnek Yapı / Faktör"], [
            {"cells": [{"text": "1. Tutunma (Adezyon)", "isMasked": False}, {"text": "Üroepitele yapışma", "isMasked": True, "hint": "mukozaya tutunma"}, {"text": "Pili, fimbriya, yüzey proteinleri"}]},
            {"cells": [{"text": "2. İnvazyon", "isMasked": False}, {"text": "Doku hasarı ve penetrasyon", "isMasked": False}, {"text": "Sitotoksik/proteolitik toksinler", "isMasked": True, "hint": "hücre eriten zehirler"}]},
            {"cells": [{"text": "3. Savunmadan Kaçış", "isMasked": False}, {"text": "İmmün yanıttan kurtulma", "isMasked": True, "hint": "bağışıklıktan kaçınma"}, {"text": "Kapsül, IgA proteaz"}]},
            {"cells": [{"text": "4. Metabolik İhtiyaçlar", "isMasked": False}, {"text": "Besin ve demir temini", "isMasked": False}, {"text": "Siderofor, demir bağlayıcı proteinler", "isMasked": True, "hint": "demir çeken moleküller"}]}
        ]),
        make_chain("Patojenik Süreç Basamakları", [
            "1. Adezyon: Pili ve fimbriyalarla konak reseptörlerine tutunma.",
            "2. İnvazyon: Enzim ve toksinlerle ekstrasellüler matriks hasarı.",
            "3. Kaçış: Kapsül ve proteazlarla lökositlerden kurtulma.",
            "4. Beslenme: Sideroforlarla konak demirini bağlayıp çoğalma."
        ]),
        make_recall("Mikroorganizma patojenitesi ve virülans faktörlerinin dört ana kategorisi nedir?", "1) Tutunma (adezyon), 2) İnvazyon, 3) Konak savunmasından kaçış, 4) Metabolik ihtiyaçlardır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Virülans Sınıflaması", [
            {"text": "Tutunma (adezyon) virülans faktörlerinin ilk basamağını oluşturur.", "isLie": False, "explanation": "Doğru. Adezyon olmadan enfeksiyon başlayamaz."},
            {"text": "İnvazyon, enzimler ve toksinler aracılığıyla hücre hasarı yapar.", "isLie": False, "explanation": "Doğru. Doku harabiyeti oluşturur."},
            {"text": "Üropatojen mikroorganizmaların hiçbir virülans faktörü yoktur, tamamen pasiftirler.", "isLie": True, "explanation": "Tuzak! Üropatojenler fimbriya, toksin, kapsül ve siderofor gibi zengin virülans araçlarına sahiptir."},
            {"text": "Metabolik ihtiyaçlar siderofor gibi yapılarla demir teminini içerir.", "isLie": False, "explanation": "Doğru. Beslenme virülansıdır."}
        ]),
        make_quiz("Ders notuna göre mikroorganizma patojenitesi ve virülans faktörlerinin dört ana grubu aşağıdakilerin hangisinde eksiksiz verilmiştir?", [
            {"key": "A", "text": "Tutunma (adezyon), invazyon, konak savunmasından kaçış ve metabolik ihtiyaçlar", "isCorrect": True, "explanation": "Ders notundaki 4 ana başlıktır."},
            {"key": "B", "text": "Yalnızca fotosentez ve fermantasyon", "isCorrect": False, "explanation": "Bakteriyel virülans grubu değildir."},
            {"key": "C", "text": "Sadece spor oluşumu ve klorofil sentezi", "isCorrect": False, "explanation": "Üropatojen virülansı ile ilgisizdir."},
            {"key": "D", "text": "Kan grubu antijenleri ve albümin üretimi", "isCorrect": False, "explanation": "Konak faktörleridir, bakteri virülansı değildir."}
        ])
    ]
    slides.append(make_slide(25, "Bakteriyel Virülans Faktörlerine Genel Bakış", "Tutunma, invazyon, kaçış ve metabolik ihtiyaçlar sınıflaması", "Virülans Faktörleri", s25_narrative, s25_bullets, s25_elements))

    # Slide 26: Konak Hücrelerine Tutunma: Pili, Fimbriya ve Yüzey Proteinleri
    s26_narrative = (
        "İdrar akımının mekanik yıkama gücünü yenebilmek için bakterinin üroepitele sıkıca "
        "yapışması enfeksiyon gelişiminin zorunlu ilk adımıdır.\n\n"
        "- **Tutunma Yapıları:** Konak hücrelerine tutunma (adezyon) **pili, fimbriya ve yüzey "
        "proteinleri** aracılığıyla gerçekleştirilir.\n"
        "- **Fimbriyaların Rolü:** Bakteri yüzeyinden uzanan kıl benzeri fimbriyalar (ör. Tip 1 fimbriya "
        "ve P fimbriya), ürotelyum hücrelerindeki spesifik glikolipid ve glikoprotein reseptörlerine bağlanır.\n"
        "- **Adezyonun Önemi:** Tutunma gerçekleşmediğinde bakteriler normal işeme akımı ile mesaneden "
        "kolayca yıkanıp atılır; adezyon bakteriyi mekanik klirensten korur.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Konak hücrelerine tutunmayı (adezyon) sağlayan temel bakteriyel virülans faktörleri: Pili, fimbriya ve yüzey proteinleridir."
    )
    s26_bullets = [
        "Tutunma (adezyon): Pili, fimbriya ve yüzey proteinleri ile sağlanır.",
        "İdrar akımının mekanik yıkama etkisini kırmak için zorunlu ilk basamaktır.",
        "Fimbriyalar konak ürotelyal reseptörlerine kilitlenerek kolonizasyonu başlatır."
    ]
    s26_elements = [
        make_cloze("Konak hücrelerine tutunma (adezyon) pili, fimbriya ve yüzey proteinleri aracılığıyla gerçekleştirilir.", "pili, fimbriya ve yüzey proteinleri", "Bakterinin mukozaya tutunmasını sağlayan üç temel virülans yapısı"),
        make_table("Adezyon Yapıları ve İşlevleri", ["Bakteriyel Yapı", "Morfolojik Özellik", "Hedef ve Fonksiyon"], [
            {"cells": [{"text": "Pili ve Fimbriya", "isMasked": False}, {"text": "Hücre zarından uzanan protein lifleri", "isMasked": True, "hint": "kıl benzeri uzantılar"}, {"text": "Üroepitel reseptörlerine spesifik bağlanma"}]},
            {"cells": [{"text": "Yüzey Proteinleri", "isMasked": False}, {"text": "Dış membran adezinleri", "isMasked": False}, {"text": "Hücresel temas ve sıkı adezyon", "isMasked": True, "hint": "yüzey tutunma molekülleri"}]}
        ]),
        make_chain("Bakteriyel Adezyon Süreci", [
            "1. Yaklaşma: Bakterinin ürotelyal yüzeye yaklaşması.",
            "2. Fimbriyal Temas: Pili ve fimbriyaların reseptöre kilitlenmesi.",
            "3. Yüzey Proteini Sıkılaşması: Membran proteinleriyle adezyonun güçlenmesi.",
            "4. Yıkamaya Direnç: İdrar akımına rağmen lümende tutunmanın başarılması."
        ]),
        make_recall("Ders notuna göre bakterilerin konak hücrelerine tutunmasını (adezyon) sağlayan yapılar nelerdir?", "Pili, fimbriya ve yüzey proteinleridir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tutunma Yapıları", [
            {"text": "Pili ve fimbriyalar konak hücrelerine tutunmayı sağlar.", "isLie": False, "explanation": "Doğru. Ders notu adezyon yapılarıdır."},
            {"text": "Yüzey proteinleri bakteriyel adezyonda rol oynar.", "isLie": False, "explanation": "Doğru. Tutunma faktörüdür."},
            {"text": "Fimbriyalar bakterinin idrar akımıyla daha hızlı yıkanıp atılması için intihar molekülleridir.", "isLie": True, "explanation": "Tuzak! Fimbriyalar yıkanmayı engellemek ve üroepitele sıkıca tutunmak için en kritik virülans aracıdır."},
            {"text": "Adezyon idrar akımının mekanik temizliğini aşmak için gereklidir.", "isLie": False, "explanation": "Doğru. Tutunma şarttır."}
        ]),
        make_quiz("Üropatojen mikroorganizmaların konak hücrelerine tutunmasını (adezyon) sağlayan virülans yapıları aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Pili, fimbriya ve yüzey proteinleri", "isCorrect": True, "explanation": "Ders notunda 'Konak hücrelerine tutunma (adezyon): pili, fimbriya, yüzey proteinleri' şeklinde listelenmiştir."},
            {"key": "B", "text": "Yalnızca mitokondriyal kristalar", "isCorrect": False, "explanation": "Bakterilerde mitokondri bulunmaz."},
            {"key": "C", "text": "Ribozom alt birimleri", "isCorrect": False, "explanation": "Protein sentezinden sorumludur, adezyondan değil."},
            {"key": "D", "text": "Kalsiyum oksalat kristalleri", "isCorrect": False, "explanation": "İdrar kristalidir, bakteriyel yapı değildir."}
        ])
    ]
    slides.append(make_slide(26, "Konak Hücrelerine Tutunma: Pili, Fimbriya ve Adezinler", "Bakteriyel pili, fimbriya ve yüzey proteinlerinin mukozal tutunmadaki rolü", "Virülans Faktörleri", s26_narrative, s26_bullets, s26_elements))

    # Slide 27: İnvazyon: Enzimler ve Sitotoksik/Proteolitik Toksinler
    s27_narrative = (
        "Mukozaya tutunan üropatojenler, konak dokusunu penetre etmek ve besin maddelerine "
        "erişebilmek amacıyla doku yıkıcı faktörler salgılarlar.\n\n"
        "- **İnvazyon Faktörleri:** Bakteriyel invazyon **enzimler, sitotoksik ve proteolitik "
        "toksinler** aracılığıyla gerçekleştirilir.\n"
        "- **Doku Hasarı:** Bu toksinler ve enzimler **ekstrasellüler matriks ve hücre hasarı** "
        "oluşturarak epitel bütünlüğünü bozar.\n"
        "- **Klinik Yansıma:** Örneğin alfa-hemolizin ve sitotoksik nekrotizan faktör-1 (CNF-1) "
        "ürotelyal hücreleri parçalayarak mikroskobik veya makroskobik hematüriye ve derin doku invazyonuna yol açar.\n\n"
        "> [!IMPORTANT]\n"
        "> Bakteriyel enzimler, sitotoksik ve proteolitik toksinler ekstrasellüler matriks ve hücre hasarı oluşturarak invazyonu sağlar."
    )
    s27_bullets = [
        "İnvazyon: Enzimler, sitotoksik ve proteolitik toksinler ile yürütülür.",
        "Ekstrasellüler matriks ve konak hücre hasarı meydana getirir.",
        "Epitel bütünlüğünün parçalanması derin doku invazyonuna zemin hazırlar."
    ]
    s27_elements = [
        make_cloze("Bakteriyel invazyon sürecinde enzimler ve toksinler ekstrasellüler matriks ve hücre hasarı oluşturur.", "ekstrasellüler matriks ve hücre hasarı", "Toksinlerin dokuda oluşturduğu yapısal ve hücresel tahribat"),
        make_table("Bakteriyel İnvazyon Faktörleri", ["Faktör Türü", "Etki Mekanizması", "Patolojik Sonuç"], [
            {"cells": [{"text": "Enzimler", "isMasked": False}, {"text": "Doku bileşenlerinin hidrolizi", "isMasked": True, "hint": "bağ doku eritilmesi"}, {"text": "Matriks bariyerinin delinmesi"}]},
            {"cells": [{"text": "Sitotoksik/Proteolitik Toksinler", "isMasked": False}, {"text": "Hücre zarlarında gözenek ve lizis", "isMasked": False}, {"text": "Hücre ölümü ve doku hasarı", "isMasked": True, "hint": "ürotelyal parçalanma"}]}
        ]),
        make_chain("Bakteriyel İnvazyon Aşamaları", [
            "1. Adezyon: Ürotelyuma tutunmanın tamamlanması.",
            "2. Toksin Salınımı: Sitotoksik ve proteolitik toksinlerin lümene verilmesi.",
            "3. Hücre Parçalanması: Konak hücre zarlarının delinmesi ve matriks hasarı.",
            "4. Derin Penetrasyon: Bakterinin lamina propriaya invazyonu."
        ]),
        make_recall("Bakteriyel enzimler ile sitotoksik ve proteolitik toksinlerin dokuda oluşturduğu temel patoloji nedir?", "Ekstrasellüler matriks ve hücre hasarıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: İnvazyon Faktörleri", [
            {"text": "Bakteriyel enzimler ve toksinler invazyonda rol oynar.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Toksinler ekstrasellüler matriks ve hücre hasarına yol açar.", "isLie": False, "explanation": "Doğru. Doku yıkımı yapar."},
            {"text": "Sitotoksik toksinler konak hücrelerini gençleştirip onların yaşam süresini 200 yıla uzatır.", "isLie": True, "explanation": "Tuzak! Sitotoksik toksinler hücreleri öldürür, doku hasarı ve lizis yapar."},
            {"text": "Proteolitik toksinler protein yapıları parçalayarak dokuyu tahrip eder.", "isLie": False, "explanation": "Doğru. Enzimatik hasardır."}
        ]),
        make_quiz("Mikroorganizma patojenitesinde 'invazyon' basamağını sağlayan virülans mekanizması ve hedefi aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Enzimler, sitotoksik ve proteolitik toksinler (ekstrasellüler matriks ve hücre hasarı)", "isCorrect": True, "explanation": "Ders notundaki 2. virülans maddesidir."},
            {"key": "B", "text": "Yalnızca idrarın pH'sını aşırı asitleştirme", "isCorrect": False, "explanation": "Bu invazyon faktörü değildir."},
            {"key": "C", "text": "Tamm-Horsfall proteinini parçalamadan çoğaltma", "isCorrect": False, "explanation": "İnvazyon mekanizması değildir."},
            {"key": "D", "text": "Kemik iliğinde lökosit üretimini artırma", "isCorrect": False, "explanation": "Bakteri toksinlerinin invazyon etkisi değildir."}
        ])
    ]
    slides.append(make_slide(27, "Bakteriyel İnvazyon: Toksinler ve Matriks Hasarı", "Enzimler, sitotoksik ve proteolitik toksinlerle hücre ve doku hasarı oluşumu", "Virülans Faktörleri", s27_narrative, s27_bullets, s27_elements))

    # Slide 28: Konak Savunmasından Kaçış: Kapsül ve IgA Proteaz
    s28_narrative = (
        "Üropatojen mikroorganizmalar, doku içerisinde hayatta kalabilmek için konağın hücresel "
        "ve hümoral immün mekanizmalarını etkisiz hale getiren stratejiler geliştirmiştir.\n\n"
        "- **Kaçış Faktörleri:** Konak savunmasından kaçışta temel yapılar **kapsül ve IgA proteaz** "
        "enzimidir.\n"
        "- **Kapsül Kalkanı:** Bakteri dışındaki polisakkarit kapsül (ör. K antijeni), kompleman "
        "bağlanmasını ve fagositozu mekanik olarak maskeleyerek nötrofillerden kaçışı sağlar.\n"
        "- **IgA Proteaz:** Salgısal IgA'yı spesifik olarak parçalayan IgA proteaz enzimi, mukozal "
        "antikor bariyerini yıkarak bakterinin nötralize edilmesini önler.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Konak savunmasından kaçışı sağlayan temel bakteriyel virülans faktörleri: Kapsül ve IgA proteazdır."
    )
    s28_bullets = [
        "Konak savunmasından kaçış: Kapsül ve IgA proteaz ile sağlanır.",
        "Kapsül fagositozu ve kompleman aktivasyonunu mekanik olarak engeller.",
        "IgA proteaz mukozal salgısal IgA antikorlarını parçalayarak etkisiz kılar."
    ]
    s28_elements = [
        make_cloze("Bakterilerin konak savunmasından kaçışını sağlayan yapılar kapsül ve IgA proteaz enzimidir.", "kapsül ve IgA proteaz", "İmmün yanıttan kurtulmayı sağlayan iki temel virülans aracı"),
        make_table("Savunmadan Kaçış Mekanizmaları", ["Virülans Aracı", "Hedef İmmün Mekanizma", "Kaçış Sonucu"], [
            {"cells": [{"text": "Kapsül", "isMasked": False}, {"text": "Fagositoz ve kompleman lizisi", "isMasked": True, "hint": "nötrofil ve serum öldürmesi"}, {"text": "Opsonizasyon ve yutulmadan kurtulma"}]},
            {"cells": [{"text": "IgA Proteaz", "isMasked": False}, {"text": "Salgısal IgA antikorları", "isMasked": False}, {"text": "Mukozal immün blokajın delinmesi", "isMasked": True, "hint": "antikorların parçalanması"}]}
        ]),
        make_chain("Savunmadan Kaçış Zinciri", [
            "1. İmmün Temas: Nötrofil ve salgısal IgA'nın bakteriye yaklaşması.",
            "2. IgA Proteaz Salınımı: Antikor moleküllerinin enzimatik parçalanması.",
            "3. Kapsüler Maskeleme: Fagositoz reseptörlerinin örtülmesi.",
            "4. Canlı Kalma: Bakterinin konak dokusunda eliminasyondan kaçarak yaşaması."
        ]),
        make_recall("Ders notuna göre mikroorganizmaların konak savunmasından kaçışını sağlayan iki temel faktör nedir?", "Kapsül ve IgA proteazdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Savunmadan Kaçış", [
            {"text": "Kapsül bakteriyi fagositoza karşı korur.", "isLie": False, "explanation": "Doğru. Antifagositiktir."},
            {"text": "IgA proteaz salgısal IgA antikorlarını parçalar.", "isLie": False, "explanation": "Doğru. Mukozal antikoru yıkar."},
            {"text": "Kapsül taşıyan bakteriler nötrofilleri görünce derhal intihar eder.", "isLie": True, "explanation": "Tuzak! Kapsül nötrofillerin fagositozunu engeller ve bakterinin hayatta kalmasını sağlar."},
            {"text": "Konak savunmasından kaçış virülans faktörlerinin üçüncü basamağıdır.", "isLie": False, "explanation": "Doğru. Ders notu sınıflamasıdır."}
        ]),
        make_quiz("Üropatojen mikroorganizmaların 'konak savunmasından kaçış' basamağında kullandıkları temel faktörler aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Kapsül ve IgA proteaz", "isCorrect": True, "explanation": "Ders notunda 'Konak savunmasından kaçış: kapsül, IgA proteaz' şeklinde açıkça belirtilmiştir."},
            {"key": "B", "text": "Tamm-Horsfall proteini ve üre", "isCorrect": False, "explanation": "Bunlar konak savunma faktörleridir."},
            {"key": "C", "text": "Yalnızca laktik asit", "isCorrect": False, "explanation": "Bakteriyel kaçış faktörü değildir."},
            {"key": "D", "text": "İnsülin ve glukagon", "isCorrect": False, "explanation": "İnsan hormonlarıdır."}
        ])
    ]
    slides.append(make_slide(28, "Konak Savunmasından Kaçış: Kapsül ve IgA Proteaz", "Polisakkarit kapsül kalkanı ve IgA proteaz ile immün yanıttan kurtulma", "Virülans Faktörleri", s28_narrative, s28_bullets, s28_elements))

    # Slide 29: Metabolik İhtiyaçlar: Siderofor ve Demir Bağlayıcı Proteinler
    s29_narrative = (
        "Üriner sistem lümeni ve dokusu, mikroorganizmalar için demir gibi esansiyel mineraller "
        "açısından oldukça kısıtlı ve zorlayıcı bir besiyeridir.\n\n"
        "- **Metabolik İhtiyaçlar:** Patojenlerin metabolik ihtiyaçlarını karşılayan temel faktörler "
        "**siderofor ve demir bağlayıcı proteinler**dir.\n"
        "- **Demir Kısıtlaması:** Konak organizma demiri laktoferrin ve transferrin gibi proteinlere "
        "sıkıca bağlayarak bakterilerin kullanımına kapalı tutar.\n"
        "- **Sideroforların Gücü:** Bakterilerin salgıladığı sideroforlar (aerobaktin, enterobaktin vb.), "
        "konak proteinlerinden demiri yüksek afiniteyle kopararak bakteriyel çoğalma için temin eder.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Mikroorganizmaların metabolik ihtiyaçlarını karşılayan ve demir bağlamasını sağlayan virülans faktörleri: Siderofor ve demir bağlayıcı proteinlerdir."
    )
    s29_bullets = [
        "Metabolik ihtiyaçlar: Siderofor ve demir bağlayıcı proteinler.",
        "Konak ortamındaki serbest demir yokluğunu aşmak için esansiyeldir.",
        "Yüksek afiniteli demir şelasyonu ile bakteriyel büyüme ve bölünmeyi destekler."
    ]
    s29_elements = [
        make_cloze("Mikroorganizmaların metabolik ihtiyaçlarını karşılayan ve demir temin eden yapılar siderofor ve demir bağlayıcı proteinlerdir.", "siderofor", "Demiri konak dokusundan koparan yüksek afiniteli molekül"),
        make_table("Bakteriyel Beslenme ve Demir Şelasyonu", ["Bileşen", "Biyolojik Fonksiyon", "Klinik Önemi"], [
            {"cells": [{"text": "Sideroforlar", "isMasked": False}, {"text": "Yüksek afiniteli demir bağlama", "isMasked": True, "hint": "demiri kendine çeken molekül"}, {"text": "Demirsiz idrarda çoğalma yeteneği"}]},
            {"cells": [{"text": "Demir Bağlayıcı Proteinler", "isMasked": False}, {"text": "Demirin hücre içine taşınması", "isMasked": False}, {"text": "Metabolik enzim aktivasyonunun sürmesi", "isMasked": True, "hint": "hücresel demir transferi"}]}
        ]),
        make_chain("Bakteriyel Demir Temin Zinciri", [
            "1. Demir Açlığı: İdrarda serbest demir iyonunun bulunmaması.",
            "2. Siderofor Sentezi: Bakterinin dış ortama siderofor salgılaması.",
            "3. Şelasyon: Sideroforun konak dokusundaki demiri bağlaması.",
            "4. Hücreye Alım: Demir-siderofor kompleksinin bakteriye girmesi ve üreme."
        ]),
        make_recall("Ders notuna göre mikroorganizmaların metabolik ihtiyaçlarını karşılayan temel virülans faktörleri nelerdir?", "Siderofor ve demir bağlayıcı proteinlerdir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Metabolik İhtiyaçlar", [
            {"text": "Sideroforlar bakterilerin demir bağlamasını sağlayan virülans faktörleridir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Demir bağlayıcı proteinler bakterilerin metabolik ihtiyaçlarını karşılar.", "isLie": False, "explanation": "Doğru. Beslenme virülansıdır."},
            {"text": "Sideroforlar vücuttaki tüm demiri yok edip hastada anında kalp durmasına yol açan zehirlerdir.", "isLie": True, "explanation": "Tuzak! Sideroforlar bakterinin kendi beslenmesi için konaktan demir çalan şelatörlerdir, anlık kalp durması zehri değildir."},
            {"text": "Demir kısıtlaması konağın doğal bir savunma yöntemidir.", "isLie": False, "explanation": "Doğru. Bakteriden demir saklanır."}
        ]),
        make_quiz("Üropatojen mikroorganizmaların 'metabolik ihtiyaçlar' kapsamında demir teminini sağlayan virülans faktörleri aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Siderofor ve demir bağlayıcı proteinler", "isCorrect": True, "explanation": "Ders notunda 'Metabolik ihtiyaçlar: siderofor, demir bağlayıcı proteinler' olarak belirtilmiştir."},
            {"key": "B", "text": "Yalnızca Tip 1 fimbriya", "isCorrect": False, "explanation": "Fimbriya adezyon faktörüdür, demir bağlamaz."},
            {"key": "C", "text": "Kapsül polisakkariti", "isCorrect": False, "explanation": "Kapsül fagositozdan kaçış faktörüdür."},
            {"key": "D", "text": "Sitotoksik nekrotizan faktör", "isCorrect": False, "explanation": "Toksindir, demir şelatörü değildir."}
        ])
    ]
    slides.append(make_slide(29, "Metabolik İhtiyaçlar: Siderofor ve Demir Bağlama", "Sideroforlar ve demir bağlayıcı proteinlerle besin temini mekanizması", "Virülans Faktörleri", s29_narrative, s29_bullets, s29_elements))

    # Slide 30: [TEKRAR SAYFASI - CHECKPOINT 3] Konak Savunması ve Virülans Faktörleri
    s30_narrative = (
        "Bu tekrar sayfasında 3. Bölümde işlenen konak savunma hatlarını (mekanik, kimyasal, immün) "
        "ve mikroorganizma virülans faktörlerini (adezyon, invazyon, kaçış, metabolik) pekiştiriyoruz.\n\n"
        "- **Konak Savunması:** Normal işeme; idrar özellikleri (**yüksek osmolarite, yüksek üre, düşük pH, "
        "Tamm-Horsfall proteinleri**); prostat salgısı; fagositler, sitokinler, kompleman ve salgısal IgA.\n"
        "- **Bakteriyel Virülans:** 1) Adezyon: **pili, fimbriya, yüzey proteinleri**; 2) İnvazyon: **enzimler, "
        "sitotoksik/proteolitik toksinler**; 3) Kaçış: **kapsül, IgA proteaz**; 4) Metabolizma: **siderofor**.\n\n"
        "> [!IMPORTANT]\n"
        "> [TEKRAR SAYFASI - CHECKPOINT 3] Konak savunması yüksek osmolarite/üre/düşük pH ve Tamm-Horsfall ile mekanik-kimyasal temizlik sağlarken; bakteri buna pili/fimbriya, toksinler, kapsül/IgA proteaz ve siderofor ile karşı koyar."
    )
    s30_bullets = [
        "Konak: Yüksek osmolarite, yüksek üre, düşük pH, Tamm-Horsfall, prostat salgısı, IgA.",
        "Virülans: 1) Tutunma (pili/fimbriya), 2) İnvazyon (toksinler/enzimler).",
        "Virülans: 3) Kaçış (kapsül, IgA proteaz), 4) Metabolizma (siderofor, demir bağlama)."
    ]
    s30_elements = [
        make_cloze("Konak savunmasında idrarın özellikleri yüksek osmolarite, yüksek üre, düşük pH ve Tamm-Horsfall proteinleridir.", "Tamm-Horsfall proteinleridir", "Bakteri fimbriyalarını bağlayan koruyucu glikoprotein"),
        make_table("3. Bölüm Büyük Tekrar Tablosu", ["Kategori", "Temel Bileşenler", "Klinik / Biyolojik İşlev"], [
            {"cells": [{"text": "Konak Kimyasal Savunması", "isMasked": False}, {"text": "Yüksek osmolarite/üre, düşük pH, Tamm-Horsfall", "isMasked": True, "hint": "idrar koruma faktörleri"}, {"text": "Bakteriyel üreme ve tutunmayı engelleme"}]},
            {"cells": [{"text": "Bakteriyel Tutunma", "isMasked": False}, {"text": "Pili, fimbriya, yüzey proteinleri", "isMasked": False}, {"text": "Mukozaya adezyon ve klirensten kaçış", "isMasked": True, "hint": "yıkamaya direnç sağlama"}]},
            {"cells": [{"text": "Savunmadan Kaçış", "isMasked": False}, {"text": "Kapsül, IgA proteaz", "isMasked": True, "hint": "immün kaçış araçları"}, {"text": "Fagositoz ve mukozal IgA blokajı"}]},
            {"cells": [{"text": "Metabolik İhtiyaçlar", "isMasked": False}, {"text": "Siderofor, demir bağlayıcı proteinler", "isMasked": False}, {"text": "Konaktan demir şelasyonu", "isMasked": True, "hint": "demir çalma yeteneği"}]}
        ]),
        make_chain("Konak-Patojen Etkileşim Zinciri", [
            "1. İdrar Bariyeri: Yüksek osmolarite, üre ve düşük pH ile karşılama.",
            "2. Bakteriyel Adezyon: Pili ve fimbriyalarla Tamm-Horsfall'ı aşıp tutunma.",
            "3. İnvazyon ve Doku Hasarı: Toksin ve enzimlerle hücre tahribatı.",
            "4. Kaçış ve Beslenme: Kapsül/IgA proteazla korunup sideroforla demir temini."
        ]),
        make_recall("Checkpoint 3: İdrarın üç koruyucu fizikokimyasal özelliği ve bakterinin demir temin eden virülans aracı nedir?", "İdrarın özellikleri: yüksek osmolarite, yüksek üre, düşük pH'dır; demir temin eden virülans aracı ise siderofor ve demir bağlayıcı proteinlerdir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Checkpoint 3 Konsolidasyonu", [
            {"text": "İdrarın özellikleri yüksek osmolarite, yüksek üre ve düşük pH'dır.", "isLie": False, "explanation": "Doğru. 3. bölümün temel bilgisidir."},
            {"text": "Bakteriler konak hücrelerine pili, fimbriya ve yüzey proteinleri ile tutunur.", "isLie": False, "explanation": "Doğru. Adezyon mekanizmasıdır."},
            {"text": "Tamm-Horsfall proteini bakterilere bağlanıp onları öldüren bir antibiyotiktir.", "isLie": True, "explanation": "Tuzak! Tamm-Horsfall bir antibiyotik değil, böbrekten salgılanan ve bakterilere yapışarak onların üroepitele adezyonunu engelleyen koruyucu bir glikoproteindir."},
            {"text": "Sideroforlar bakterilerin demir bağlayıcı metabolik virülans faktörleridir.", "isLie": False, "explanation": "Doğru. Demir şelatörüdür."}
        ]),
        make_quiz("3. Bölümün tamamı (Konak Savunması ve Virülans Faktörleri) değerlendirildiğinde aşağıdaki eşleştirmelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Konak savunmasından kaçış — Pili ve fimbriya", "isCorrect": True, "explanation": "Yanlış eşleştirme! Pili ve fimbriya 'tutunma (adezyon)' faktörüdür; savunmadan kaçış faktörleri ise kapsül ve IgA proteazdır."},
            {"key": "B", "text": "Metabolik ihtiyaçlar — Siderofor ve demir bağlayıcı proteinler", "isCorrect": False, "explanation": "Doğru bir eşleştirmedir."},
            {"key": "C", "text": "İnvazyon — Enzimler, sitotoksik ve proteolitik toksinler", "isCorrect": False, "explanation": "Doğru bir eşleştirmedir."},
            {"key": "D", "text": "Kimyasal bariyer — Yüksek osmolarite, yüksek üre, düşük pH", "isCorrect": False, "explanation": "Doğru bir eşleştirmedir."}
        ])
    ]
    slides.append(make_slide(30, "[TEKRAR SAYFASI - CHECKPOINT 3] Konak Savunması ve Virülans Faktörleri", "3. Bölümün kapsamlı pekiştirmesi: konak bariyerleri, idrar özellikleri ve 4 virülans kategorisi", "Bölüm Tekrarı", s30_narrative, s30_bullets, s30_elements))

    return slides
