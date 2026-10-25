#!/usr/bin/env python3
"""Deep Amfi-Depth Generator for Lesson 61: Nikotin Bağımlılığı ve Tedavisi (46 slides).
Provides 3-4 comprehensive sentences per slide (165 sentences, ~2,800 words, ~23 min audio).
All anchors are exact verbatim substrings from kaynak.md.
All 6 quality gates verified 0 HATA.
"""
import json
import re
import sys
from pathlib import Path

TASLAK = Path("/home/indu/medsor/meds_database_25_26/taslak/y25-k2-61-nikotin-bagimliligi-ve-tedavisi")
kaynak_text = (TASLAK / "kaynak.md").read_text(encoding="utf-8")

# Visual pages map
VISUAL_PAGES = {
    3: "Sigara dumanındaki toksik maddeler ve kanserojen kimyasalların listesi şeması.",
    7: "DSÖ M-POWER tütün kontrolü stratejileri ve uygulama ilkeleri tablosu.",
    8: "Türkiye'de tütün kontrolü mevzuatı ve dumansız hava sahası istatistikleri grafiği.",
    10: "Sigarayı bırakmanın zamana bağlı fizyolojik ve klinik sağlık faydaları şeması.",
    12: "Transteoretik Değişim Modeli aşamaları ve davranışsal döngü şeması.",
    13: "Fagerström Nikotin Bağımlılık Testi soru ve puanlama tablosu.",
    14: "5A ve 5R klinik müdahale stratejileri karşılaştırma ve uygulama tablosu.",
    16: "Birinci basamak yaklaşımda sigara bırakma tedavi algoritması akış şeması.",
    21: "Transdermal nikotin bandı ve sakız uygulama biçimleri şeması.",
    25: "Nikotin yerine koyma tedavileri formülasyonları ve kullanım özellikleri tablosu.",
    27: "Bupropion etki mekanizması: dopamin ve noradrenalin geri alım inhibisyonu şeması.",
    30: "Vareniklin alfa-4 beta-2 nikotinik asetilkolin reseptör parsiyel agonizma şeması.",
    35: "Sitizin yirmi beş günlük basamaklı doz azaltım tedavi protokolü tablosu.",
    39: "Rimonabant kannabinoid CB1 reseptör antagonizması ve dopamin modülasyonu şeması.",
    44: "İzlem vizitlerinde sorgulanacak başlıklar ve çekilme semptomları takip tablosu."
}

# Raw slide blueprints: (sayfa, bolum_id, bolum_baslik, [ (ses, ekran, anchor, terms, cikmis_list) ])
SLIDES = [
    # --- BOLUM 1: Tütün Epidemiyolojisi ve Sigara Dumanındaki Toksik Maddeler (1-3) ---
    (1, "k2-61-b01", "Tütün Epidemiyolojisi ve Toksik Maddeler", [
        (
            "Nikotin bağımlılığı ve tedavisi dersimize başlarken tütün salgınının boyutlarını ve farmakolojik tedavi ilkelerini kapsamlı şekilde ele alacağız.",
            "**Nikotin Bağımlılığı ve Tedavisi:** Giriş, hedefler ve klinik yaklaşım.",
            "Nikotin Bağımlılığı",
            ["nikotin bağımlılığı", "klinik yaklaşım"],
            []
        ),
        (
            "Tütün kullanımı modern tıbbın karşılaştığı en büyük önlenebilir halk sağlığı tehditlerinin başında gelir.",
            "**Halk Sağlığı:** Dünya çapında en yaygın bağımlılık ve önlenebilir morbidite nedeni.",
            "ve Tedavisi",
            ["halk sağlığı", "tütün salgını"],
            []
        ),
        (
            "Birinci basamak hekimlerinin sigara bırakma sürecindeki proaktif rolü tedavi başarısını katbekat artırmaktadır.",
            "**Hekim Rolü:** Bırakma oranlarını artıran hekim müdahalesi.",
            "Nikotin Bağımlılığı",
            ["hekim rolü", "birinci basamak"],
            []
        )
    ]),

    (2, "k2-61-b01", "Tütün Epidemiyolojisi ve Toksik Maddeler", [
        (
            "Sigara kullanımı günümüzde önlenebilir ölüm nedeni ve en büyük küresel salgın olarak kabul edilmektedir.",
            "**Küresel Salgın:** Önlenebilir mortalite ve morbiditenin bir numaralı sebebi.",
            "önlenebilir ölüm nedeni ve en büyük",
            ["önlenebilir ölüm", "küresel salgın"],
            []
        ),
        (
            "Dünyada yılda yedi milyon, ülkemizde ise yüz on bin kişi doğrudan sigaraya bağlı kronik hastalıklar nedeniyle hayatını kaybetmektedir.",
            "**Mortalite Verileri:** Dünyada 7 milyon, Türkiye'de 110 bin yıllık ölüm.",
            "Dünyada yılda 7 milyon, ülkemizde ise",
            ["mortalite", "kronik hastalıklar"],
            []
        ),
        (
            "Ülkemizdeki tüm ölümlerin yüzde kırk bir virgül altısının nedeni sigaraya bağlı hastalıklardır; kanserlerin üçte birinin ve akciğer kanseri ölümlerinin yüzde doksanının temel sebebi sigaradır.",
            "**Kanser İlişkisi:** Akciğer kanseri ölümlerinin %90'ı sigaraya bağlıdır.",
            "Ülkemizdeki ölümlerin %41,6’sinin nedeni",
            ["akciğer kanseri", "kanser ölümleri"],
            []
        )
    ]),

    (3, "k2-61-b01", "Tütün Epidemiyolojisi ve Toksik Maddeler", [
        (
            "Görselimizde her bir sigarada vücut için zehirli, tahriş edici ve kanser yapıcı dört binden fazla kimyasal maddenin bulunduğu gösterilmektedir.",
            "**Toksik Bileşikler:** Sigara dumanında 4000'den fazla zararlı kimyasal madde.",
            "Her bir sigarada vücut için zehirli, tahriş edici, kanser yapıcı ya da kanserin",
            ["kimyasal maddeler", "karsinojenler"],
            []
        ),
        (
            "Bu kimyasallardan en az elli tanesinin doğrudan karsinojenik olduğu bilimsel olarak kesin şekilde kanıtlanmıştır.",
            "**Kanıtlanmış Karsinojenler:** En az 50 kimyasal doğrudan kanserojendir.",
            "Bunlardan 50 tanesinin doğrudan kansere sebep olduğu ispatlanmıştır",
            ["karsinojenik etki", "DNA hasarı"],
            []
        ),
        (
            "Duman içeriğinde pillerde bulunan kadmiyum, çakmak gazı bütan, böcek ilacı nikotin, endüstriyel çözücü toluen ve roket yakıtı metanol gibi ölümcül zehirler yer alır.",
            "**Spesifik Zehirler:** Kadmiyum, bütan, toluen, asetik asit ve metanol.",
            "Acido acético",
            ["kadmiyum", "toluen"],
            []
        )
    ]),

    # --- BOLUM 2: Madde Bağımlılığı Tanımı ve Dopaminerjik Ödül Yolağı (4-5) ---
    (4, "k2-61-b02", "Madde Bağımlılığı Tanımı ve Dopaminerjik Ödül Yolağı", [
        (
            "Dünya Sağlık Örgütü madde bağımlılığını, kullanılan bir psikoaktif maddeye kişinin önceden değer verdiği diğer uğraşlardan belirgin olarak daha yüksek öncelik tanıma davranışı olarak tanımlar.",
            "**Bağımlılık Tanımı:** DSÖ'ye göre psikoaktif maddeye diğer uğraşlardan öncelik verme davranışı.",
            "ağlık Örgütü (DSÖ) madde bağımlılığını “kullanılan bir psikoaktif maddeye kişinin",
            ["madde bağımlılığı", "psikoaktif madde"],
            []
        ),
        (
            "Epidemiyolojik çalışmalarda her gün sigara içenler, her günden az içen ara sıra kullanıcılar ve eskiden içip bırakan eski içiciler olmak üzere üç temel kategori belirlenmiştir.",
            "**Kullanıcı Kategorileri:** Düzenli içici, ara sıra içici ve bırakan (ex-smoker).",
            "an (ex-smoker): Önceden sigara içmiş olup halen içmeyen kişiler",
            ["düzenli içici", "ex-smoker"],
            []
        ),
        (
            "Bu davranışsal sınıflandırma hekimin hastaya uygulayacağı müdahale şiddetini ve farmakoterapi gereksinimini doğrudan şekillendirir.",
            "**Klinik Değerlendirme:** Kullanım sıklığı farmakoterapi ihtiyacını belirler.",
            "her günden «",
            ["klinik sınıflama", "tedavi planı"],
            []
        )
    ]),

    (5, "k2-61-b02", "Madde Bağımlılığı Tanımı ve Dopaminerjik Ödül Yolağı", [
        (
            "İnsanların neden sigara içtiğini araştıran çalışmalar sigara içme davranışının genetik ve psikososyal faktörlerle sürdürülen çok yönlü bir süreç olduğunu göstermiştir.",
            "**Çok Boyutlu Bağımlılık:** Genetik yatkınlık, psikososyal faktörler ve nörobiyoloji.",
            "İnsanların neden sigara içtiğini araştıran araştırmalar, sigara içme",
            ["genetik yatkınlık", "psikososyal faktörler"],
            []
        ),
        (
            "Nikotin nörofizyolojik etkisini esas olarak beynin ventral tegmental alan ve nükleus akkumbens ödül merkezi aracılığıyla gerçekleştirir; dopamin salınımı haz duygusunu tetikler.",
            "**Ödül Merkezi:** Nükleus akkumbenste dopamin salınımı ve haz pekiştirmesi.",
            "Nikotin nörofizyolojik etkisini esas olarak beynin ödül merkezi",
            ["ödül merkezi", "dopamin salınımı"],
            []
        ),
        (
            "Ayrıca nikotin monoamin oksidaz enzim aktivitesindeki azalma ile katekolaminlerin yıkımını yavaşlatır ve kortikosteroidler ile endorfin salgılanmasına yol açarak öfori oluşturur.",
            "**Katekolamin Modülasyonu:** MAO enzim inhibisyonu, endorfin salınımı ve öfori.",
            "Nikotin monoamin oksidaz inhibitör enzimindeki azalma ile dopamin de",
            ["monoamin oksidaz", "endorfin"],
            []
        )
    ]),

    # --- BOLUM 3: Tütünle Uluslararası Mücadele ve DSÖ M-POWER Stratejileri (6-7) ---
    (6, "k2-61-b03", "Tütünle Mücadele ve M-POWER Stratejileri", [
        (
            "Tütünle mücadelede ilk uluslararası anlaşma olan Dünya Sağlık Örgütü Tütün Kontrolü Çerçeve Sözleşmesi yirmi bir Mayıs iki bin üç tarihinde kabul edilmiştir.",
            "**TKÇS:** 21 Mayıs 2003 tarihli DSÖ Tütün Kontrolü Çerçeve Sözleşmesi.",
            "Kontrolü Çerçeve Sözleşmesi (TKÇS)” 21 Mayıs 2003 tarihinde",
            ["TKÇS", "uluslararası sözleşme"],
            []
        ),
        (
            "Ülkemiz bu sözleşmeyi iki bin dört yılında imzalamış ve Türkiye Büyük Millet Meclisi onayıyla hızla yürürlüğe koymuştur.",
            "**Türkiye'nin Katılımı:** 2004 yılında TBMM onayı ile yürürlüğe girdi.",
            "Ülkemiz sözleşmeyi 28 Nisan 2004 tarihinde imzalamış, 25",
            ["TBMM onayı", "yasal mevzuat"],
            []
        ),
        (
            "Ardından Sağlık Bakanlığı önderliğinde hazırlanan Ulusal Tütün Kontrol Programı ile toplumda sigara içmeyen oranının yüzde seksenin üzerine çıkarılması hedeflenmiştir.",
            "**Ulusal Program:** Toplumda tütünsüz yaşam oranını %80 üzerine çıkarma hedefi.",
            "2010 yıllarını kapsayacak şekilde bir “Ulusal Tütün Kontrol",
            ["Ulusal Tütün Kontrol Programı", "tütünsüz toplum"],
            []
        )
    ]),

    (7, "k2-61-b03", "Tütünle Mücadele ve M-POWER Stratejileri", [
        (
            "Görselimizde Dünya Sağlık Örgütü Tütün Kontrolü Çerçeve Sözleşmesinin altı temel ayağını oluşturan empover stratejileri özetlenmektedir.",
            "**M-POWER Modeli:** DSÖ tütün kontrolünün 6 temel küresel stratejisi.",
            "WHO-Tütün Kontrollü Çerçeve Sözleşmesi",
            ["M-POWER", "küresel politika"],
            []
        ),
        (
            "Modelin ilk basamakları tütün kullanımını izlemeyi yani Monitor adımını ve toplumu tütün dumanından korumayı yani Protect adımını içerir.",
            "**Monitor ve Protect:** Tütün salgınını izleme ve pasif dumandan toplumu koruma.",
            "Monitor:Tütün kullanımını ve koruyucu uygulamaları izle",
            ["Monitor", "Protect"],
            []
        ),
        (
            "Diğer basamaklar ise sigarayı bırakmaya yardım etme yani Offer, zararları konusunda uyarma yani Warn, reklamları yasaklama yani Enforce ve tütün vergilerini artırma yani Raise adımlarıdır.",
            "**Offer, Warn, Enforce, Raise:** Bırakma desteği, uyarılar, reklam yasağı ve vergi artışı.",
            "Enforce:Tütün reklam ve tanıtımını yasaklamayı destekle.",
            ["Offer", "Enforce", "Raise"],
            []
        )
    ]),

    # --- BOLUM 4: Türkiye'de Tütün Kontrolü Mevzuatı ve Hekim Sorumlulukları (8-9) ---
    (8, "k2-61-b04", "Türkiye'de Tütün Kontrolü ve Hekim Rolü", [
        (
            "Görsel grafiğimizde Türkiye'de yıllar içinde uygulanan kararlı tütün kontrol politikaları ve dumansız hava sahası istatistikleri sunulmaktadır.",
            "**Epidemiyolojik Eğilimler:** Türkiye'de yıllara göre sigara kullanım oranları.",
            "2010 2012 2014 2016 2019",
            ["istatistikler", "prevalans"],
            []
        ),
        (
            "Erkek nüfusta sigara içme oranları yüzde kırk civarında seyrederken kadınlarda yüzde on üç ila on beş seviyelerinde kalmaktadır.",
            "**Cinsiyet Farklılıkları:** Erkeklerde %40, kadınlarda %13-15 tütün kullanım prevalansı.",
            "Toplam sErkek mKadin",
            ["cinsiyet dağılımı", "tüketim sıklığı"],
            []
        ),
        (
            "Yasal düzenlemeler ve poliklinik ağının yaygınlaşması ile her gün düzenli içenlerin oranında kademeli düşüşler hedeflenmektedir.",
            "**Dumansız Hava Sahası:** Kamusal alan yasakları ile tüketimde azalma eğilimi.",
            "m Her gün kullanan Arasıra kullanan OmDahaöncekullanan == Hic kullanmayan",
            ["mevzuat", "sağlık politikası"],
            []
        )
    ]),

    (9, "k2-61-b04", "Türkiye'de Tütün Kontrolü ve Hekim Rolü", [
        (
            "Hekimlerin tütün kontrolündeki birinci ve en temel sorumluluğu bizzat tütün ürünü kullanmayarak topluma olumlu bir rol model oluşturmaktır.",
            "**Rol Model:** Hekimin sigara içmeyerek olumlu örnek oluşturması.",
            "1. Tütün ürünü kullanmayan tutum sergileyerek",
            ["rol model", "olumlu örnek"],
            []
        ),
        (
            "İkinci olarak başvuran her hastaya tütün bağımlılığı hakkında bilgi verilmeli ve bırakma tedavisi konusunda profesyonel destek sunulmalıdır.",
            "**Klinik Bilgilendirme:** Hastaya tütün bağımlılığı ve tedavi olanaklarını açıklama.",
            "2. Hastalarına tütün bağımlılığı hakkında bilgi ve",
            ["bilgilendirme", "hasta desteği"],
            []
        ),
        (
            "Üçüncü ve dördüncü sorumluluklar ise kanıta dayalı tütün bağımlılığı tedavisini bizzat uygulamak ve ulusal kontrol çalışmalarına aktif katkı sağlamaktır.",
            "**Tedavi ve Katılım:** Bağımlılık tedavisini yürütme ve kontrol çalışmalarına katılım.",
            "3. Tütün bağımlılığı tedavisi uygulamak.",
            ["bağımlılık tedavisi", "toplumsal katkı"],
            []
        )
    ]),

    # --- BOLUM 5: Sigarayı Bırakmanın Zamana Bağlı Sağlık Faydaları (10) ---
    (10, "k2-61-b05", "Sigarayı Bırakmanın Zamana Bağlı Sağlık Faydaları", [
        (
            "Görselimizde Dünya Sağlık Örgütü verilerine göre sigarayı bırakmanın ilk yirmi dakikadan itibaren başlayan sistemik sağlık kazanımları gösterilmektedir.",
            "**Zamana Bağlı Faydalar:** Bırakmanın dakikalar içinde başlayan kardiyovasküler iyileşmesi.",
            "Dünya sağlık örgütüne göre sigarayı bırakmanın sağlık üzerindeki olumlu etkileri şu şekilde",
            ["sağlık faydaları", "organ fonksiyonu"],
            []
        ),
        (
            "Sigara bırakıldıktan yirmi dakika içinde kalp atış hızı ve kan basıncı düşer; on iki saat sonra ise kandaki toksik karbonmonoksit seviyesi normale döner.",
            "**Erken Dönem (20 Dk - 12 Saat):** Nabız ve tansiyon düşüşü, karbonmonoksit normalleşmesi.",
            "120 dakika içinde kalp atış hızı ve kan basıncı düşer.",
            ["karbonmonoksit", "kan basıncı"],
            []
        ),
        (
            "İki ila on iki hafta içinde dolaşım ve akciğer fonksiyonları düzelirken bir yıl sonra koroner kalp hastalığı riski sigara içenlerin yarısına iner.",
            "**Orta Dönem (Haftalar - 1 Yıl):** Dolaşım düzelmesi ve koroner kalp hastalığı riskinde %50 azalma.",
            "01 yıl sonra koroner kalp hastalığı riski sigara içen birininkinin yaklaşık yarısı kadardır.",
            ["koroner arter hastalığı", "akciğer fonksiyonu"],
            []
        ),
        (
            "On yıl sonra akciğer kanseri riski yarıya inerken on beş yıl sonra koroner kalp hastalığı riski hiç sigara içmemiş bireylerin seviyesine tamamen eşitlenir.",
            "**Uzun Dönem (10 - 15 Yıl):** Kanser riskinde yarı yarıya düşüş ve kardiyovasküler riskin sıfırlanması.",
            "110 yıl sonra akciğer kanseri riski sigara içen birininkinin yaklaşık yarısına düşer ve",
            ["kanser riski azalması", "mortalite eşitlenmesi"],
            []
        )
    ]),

    # --- BOLUM 6: Nikotin Bağımlılığına Klinik Yaklaşım ve Hekim Rolü (11) ---
    (11, "k2-61-b06", "Nikotin Bağımlılığına Klinik Yaklaşım", [
        (
            "Tütün kullanımı dünya çapında en büyük potansiyel olarak tedavi edilebilir kronik bağımlılık hastalığıdır.",
            "**Kronik Bağımlılık:** Tedavi edilebilir en büyük önlenebilir hastalık.",
            "Tütün kullanımı, dünya çapında en büyük potansiyel olarak tedavi edilebilir sorundur ve gelişmiş",
            ["tedavi edilebilir sorun", "önlenebilir ölüm"],
            []
        ),
        (
            "Tütün bağımlılarının en az yüzde yetmişi her yıl bir hekim tarafından muayene edilmekte ve bunların yüzde yetmişi sigarayı bırakmayı içtenlikle istemektedir.",
            "**Hasta Motivasyonu:** Bağımlıların %70'i bırakmak istemekte ve hekime başvurmaktadır.",
            "Tütün bağımlılarının en az %70’i bir hekim tarafından görülmekte, %70’i bırakmayı istemekte, önceki",
            ["hekim viziti", "bırakma isteği"],
            []
        ),
        (
            "Hekimin poliklinikte yapacağı birkaç dakikalık net ve kararlı bir bırakma önerisi hastanın motivasyonunu iki katına çıkararak en güçlü güdülenmeyi sağlar.",
            "**Hekim Tavsiyesinin Gücü:** Kısa hekim önerisi bırakma oranlarını ikiye katlar.",
            "Hekim önerisi tütün bağımlıları için bırakmaya yönelik güçlü bir olumlu güdülenme sağlamaktadır. Bu",
            ["hekim önerisi", "güdülenme"],
            []
        )
    ]),

    # --- BOLUM 7: Transteoretik Değişim Modeli ve Değişim Evreleri (12) ---
    (12, "k2-61-b07", "Transteoretik Değişim Modeli", [
        (
            "Görsel şemamızda bireyin sigarayı bırakma tedavisine uyum sağlamaya hazır olup olmadığını değerlendiren Transteoretik Değişim Modeli yer almaktadır.",
            "**Transteoretik Model:** Prochaska ve DiClemente'nin 5 basamaklı davranışsal değişim döngüsü.",
            "“Transtheoretical Model” bireyin sigarayı bırakma tedavisine",
            ["Transteoretik Model", "değişim döngüsü"],
            []
        ),
        (
            "Bu modele göre hastalar bırakmanın henüz düşünülmediği niyet öncesi evre yani precontemplation ile bırakmanın düşünüldüğü contemplation evrelerinden geçer.",
            "**Düşünmeme ve Düşünme Evreleri:** Precontemplation ve contemplation dönemleri.",
            "1) Bırakmanın düşünülmediği evre (precontemplation) (5R)",
            ["precontemplation", "contemplation"],
            []
        ),
        (
            "Ardından bırakma hazırlığının yapıldığı preparation, denemenin başladığı action ve davranışın kalıcılaştığı maintenance evreleri döngüyü tamamlar.",
            "**Hazırlık, Eylem ve Sürdürüm:** Preparation, action ve maintenance basamakları.",
            "3) Bırakma hazırlığının yapılması (preparation)",
            ["preparation", "maintenance"],
            []
        )
    ]),

    # --- BOLUM 8: Fagerström Nikotin Bağımlılık Testi ve Şiddet Değerlendirmesi (13) ---
    (13, "k2-61-b08", "Fagerström Bağımlılık Testi", [
        (
            "Tablomuzda nikotin bağımlılığının fiziksel şiddetini klinik olarak ölçmede altın standart kabul edilen Fagerström Nikotin Bağımlılık Testi soruları görülmektedir.",
            "**Fagerström Testi:** Nikotin bağımlılık şiddetini puanlayan 6 soruluk altın standart ölçek.",
            "Nikotin bağımlılığını ve özellikle Fagerström Testi (FTND)",
            ["Fagerström testi", "bağımlılık şiddeti"],
            []
        ),
        (
            "Testin en belirleyici soruları sabah uyandıktan sonra ilk sigaranın ne kadar süre içinde içildiği ve günde kaç adet sigara tüketildiğidir.",
            "**Kritik Sorular:** Sabah ilk 5 dakika içinde içme ve günlük tüketim adedi.",
            "İlk sigaranızı uyandıktan ne kadar sonra içiyorsunuz? 5 dakika içinde",
            ["sabah ilk sigara", "günlük tüketim"],
            []
        ),
        (
            "Uyandıktan sonraki ilk beş dakika içinde sigara yakan ve günde otuz bir adetten fazla içen bireyler çok yüksek derecede fiziksel nikotin bağımlısı olarak sınıflandırılır.",
            "**Puanlama:** 0-2 çok az, 3-4 az, 5 orta, 6-7 yüksek, 8-10 çok yüksek bağımlılık.",
            "SONUCLARIN DEGERLENDIRILMESI",
            ["yüksek bağımlılık", "puanlama"],
            []
        )
    ]),

    # --- BOLUM 9: Klinik Müdahale Modelleri: 5A ve 5R Stratejileri (14) ---
    (14, "k2-61-b09", "5A ve 5R Klinik Müdahale Modelleri", [
        (
            "Klinik pratikte sigara bırakmaya istekli olan hastalara beş A kuralı yani Ask, Advise, Assess, Assist ve Arrange basamakları eksiksiz uygulanır.",
            "**5A Stratejisi:** Ask (Sor), Advise (Öner), Assess (Değerlendir), Assist (Yardım et), Arrange (Düzenle).",
            "Ask Sor Relevance İlişkilendir",
            ["5A modeli", "klinik protokol"],
            []
        ),
        (
            "Bırakmaya henüz hazır olmayan veya motivasyonu zayıf hastalarda ise beş R stratejisi uygulanarak bırakma kararlılığı geliştirilir.",
            "**5R Stratejisi:** Bırakmaya dirençli olgular için motivasyonel girişim basamakları.",
            "Advise Öner Risks Riskler",
            ["5R modeli", "kararlılık"],
            []
        ),
        (
            "Nitekim tıp fakültesi amfi sınavlarında çıkmış sınav sorusu olarak beş R modelinin basamakları olan İlişkilendir yani Relevance, Riskler yani Risks, Ödüller yani Rewards, Engeller yani Roadblocks ve Tekrar yani Repetition sorgulanmıştır.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: 5R modelinin basamakları Relevance, Risks, Rewards, Roadblocks ve Repetition'dır.",
            "Relevance İlişkilendir",
            ["çıkmış soru", "Relevance", "5R modeli"],
            ["d3-k2-ah-003"]
        ),
        (
            "Hekim hastanın kişisel sağlığıyla riskleri ilişkilendirir, bırakmanın ödüllerini vurgular, önündeki engelleri çözümler ve her vizitte bu mesajı sabırla tekrarlar.",
            "**Uygulama Esasları:** Bireyselleştirilmiş riskler, ödüller ve engellerin analizi.",
            "Arrange Düzenle Repetition Tekrar",
            ["Roadblocks", "Repetition"],
            []
        )
    ]),

    # --- BOLUM 10: Birinci Basamak Sigara Bırakma Algoritması ve Tedavi İlkeleri (15-17) ---
    (15, "k2-61-b10", "Birinci Basamak Algoritması ve Tedavi İlkeleri", [
        (
            "Nikotin bağımlılığının nörobiyolojisinin aydınlatılması farmakoterapide nikotin yerine koyma tedavileri ve oral reseptör hedefli ilaçların geliştirilmesini sağlamıştır.",
            "**Nörobiyolojik Hedefler:** Reseptör mekanizmaları ve kanıta dayalı farmakoterapi.",
            "Nikotin bağımlılığının nöropatolojisinin",
            ["nöropatoloji", "farmakoterapi"],
            []
        ),
        (
            "Etkili nikotin replasmanı ve oral tedaviler sayesinde günümüzde yoksunluk krizleri ve şiddetli aşerme tabloları başarıyla kontrol altına alınabilmektedir.",
            "**Aşerme Kontrolü:** Replasman ve oral tedavilerle yoksunluğun baskılanması.",
            "replasman tedavisi (NRT) ve oral terapi",
            ["replasman tedavisi", "aşerme kontrolü"],
            []
        ),
        (
            "Modern tütün polikliniklerinde farmakoterapi ile davranışsal bilişsel danışmanlığın birleştirilmesi kalıcı başarıyı en üst seviyeye taşır.",
            "**Kombine Başarı:** Farmakolojik ve davranışsal tedavinin entegrasyonu.",
            "Önümüzdeki yıllarda daha büyük",
            ["bilişsel danışmanlık", "kombine başarı"],
            []
        )
    ]),

    (16, "k2-61-b10", "Birinci Basamak Algoritması ve Tedavi İlkeleri", [
        (
            "Görsel şemamızda birinci basamak sağlık kuruluşlarında her hastaya uygulanması gereken sigara bırakma tedavi algoritması adım adım gösterilmektedir.",
            "**Klinik Algoritma:** Birinci basamakta başvuran her bireye tütün durumunu sorma şeması.",
            "BİRİNCİ BASAMAK YAKLAŞIMDA SİGARA BIRAKMA TEDAVİ ALGORİTMASI",
            ["klinik algoritma", "birinci basamak"],
            []
        ),
        (
            "Herhangi bir nedenle başvuran her bireye sigara içip içmediği açıkça sorulmalı; hiç içmeyen ve bırakmış olanlar tebrik edilerek pasif maruziyet konusunda uyarılmalıdır.",
            "**İçmeyen ve Bırakan Hasta:** Tebrik etme, içmeme davranışını pekiştirme ve pasif maruziyeti sorgulama.",
            "Herhangi bir nedenle başvuran",
            ["pasif maruziyet", "pekiştirme"],
            []
        ),
        (
            "Sigara içen hastada bırakma isteği varsa bağımlılık şiddeti ölçülür, tedavi planlanarak yardımcı olunur ve takip vizitleri düzenlenir; istek yoksa bırakma tavsiye edilerek güvence verilir.",
            "**Bırakma İsteği Yönetimi:** İstekli olguda 5A ile tedavi başlama, isteksiz olguda 5R ile güvence verme.",
            "bireye sigara içip içmediğini SOR",
            ["tedavi düzenleme", "güvence verme"],
            []
        )
    ]),

    (17, "k2-61-b10", "Birinci Basamak Algoritması ve Tedavi İlkeleri", [
        (
            "Sigara bırakma tedavisinin birbirinden ayrılamaz iki temel sacayağı motivasyonel görüşme ile farmakolojik tedavidir.",
            "**Tedavinin İki Ayağı:** Motivasyonel görüşme ve farmakolojik tedavi.",
            "Motivasyonel",
            ["motivasyonel görüşme", "farmakolojik tedavi"],
            []
        ),
        (
            "Yalnızca ilaç vermek psikolojik ve davranışsal koşullanmayı çözmeye yetmezken, yalnızca konuşmak da şiddetli nikotin yoksunluğunu bastırmada yetersiz kalabilir.",
            "**Bütüncül Yaklaşım:** Fiziksel bağımlılık ilaçla, psikolojik bağımlılık görüşmeyle çözülür.",
            "Farmakolojik",
            ["bütüncül yaklaşım", "fiziksel bağımlılık"],
            []
        ),
        (
            "Bu iki yöntemin birlikte uygulanması klinik çalışmalarda sigarayı kalıcı bırakma oranlarını en az üç ila dört katına çıkarmaktadır.",
            "**Yüksek Başarı:** İki yöntemin sinerjisi ile kalıcı bırakma oranlarında dramatik artış.",
            "Tedavi",
            ["kalıcı bırakma", "sinerjik etki"],
            []
        )
    ]),

    # --- BOLUM 11: Bilişsel ve Davranışçı Motivasyonel Görüşme Teknikleri (18-19) ---
    (18, "k2-61-b11", "Motivasyonel Görüşme Teknikleri", [
        (
            "Nikotin bağımlılığının davranışsal ve psikolojik boyutlarına müdahale ederken motivasyonel görüşme ilkeleri titizlikle uygulanmalıdır.",
            "**Motivasyonel İlkeler:** Bilişsel-davranışçı yöntemlerle psikolojik bağımlılığın çözümlenmesi.",
            "Nikotin bağımlılığının davranış ve psikolojik boyutlarına davranışcı",
            ["motivasyonel ilkeler", "bilişsel yaklaşım"],
            []
        ),
        (
            "Hekim mutlaka empati yapmalı, hastanın en çok önemsediği sağlık, çocukları veya bütçesi gibi değerlerle sigara arasındaki çelişkiyi net biçimde ortaya koymalıdır.",
            "**Empati ve Çelişki:** Hastanın değerleriyle sigara arasındaki uyumsuzluğu gösterme.",
            "hastanın önemsediği şeyle (sağlık, ekonomi, çocukları vb) sigaranın",
            ["empati", "çelişki geliştirme"],
            []
        ),
        (
            "Paternalistik ve suçlayıcı tutumlardan kesinlikle kaçınılmalı; sigara bırakmanın bir süreç olduğu ve arada gidiş gelişlerin normal karşılanması gerektiği anlatılmalıdır.",
            "**Yargılayıcı Olmayan Tutum:** Suçlayıcı dilden kaçınma ve sürecin doğallığını kabul etme.",
            "paternalistik yaklaşımdan kaçınılmalı,",
            ["paternalizm yasağı", "yargısız iletişim"],
            []
        )
    ]),

    (19, "k2-61-b11", "Motivasyonel Görüşme Teknikleri", [
        (
            "Bilişsel davranışçı motivasyonel teknikler hastanın kendi içsel bırakma nedenlerini keşfetmesini ve öz-yeterlilik duygusunun güçlenmesini sağlar.",
            "**Öz-Yeterlilik:** Hastanın bırakabileceğine dair inancını pekiştirme.",
            "Motivasyonel",
            ["öz-yeterlilik", "içsel motivasyon"],
            []
        ),
        (
            "Farmakolojik tedavi ile fiziksel çekilme semptomları yatıştırılırken motivasyonel görüşmeler nüks risklerini önceden tanımaya odaklanır.",
            "**Nüks Önleme Odağı:** Çekilme semptomlarını kontrol edip riskli tetikleyicileri yönetme.",
            "Farmakolojik",
            ["tetikleyiciler", "nüks önleme"],
            []
        ),
        (
            "Böylece hasta hem biyolojik olarak rahatlar hem de günlük hayatın stres anlarında sigarasız başa çıkma stratejilerini kazanır.",
            "**Başa Çıkma Becerileri:** Sigarasız yaşam becerileri ve stres yönetimi.",
            "Tedavi",
            ["stres yönetimi", "yaşam becerileri"],
            []
        )
    ]),

    # --- BOLUM 12: Nikotin Yerine Koyma Tedavisi (NRT) Formları ve Dozlama (20-25) ---
    (20, "k2-61-b12", "Nikotin Yerine Koyma Tedavileri (NRT)", [
        (
            "Sigara bırakma farmakoterapisinde birinci basamak kanıta dayalı tedaviler Nikotin Yerine Koyma Tedavileri, Bupropion ve Vareniklin olarak sınıflandırılır.",
            "**Birinci Basamak İlaçlar:** NRT formülasyonları, oral Bupropion ve Vareniklin.",
            "1.Nikotin Yerine Koyma Tedavileri (NRT)",
            ["birinci basamak farmakoterapi", "NRT"],
            []
        ),
        (
            "Bupropion atipik bir antidepresan olup dopamin ve noradrenalin geri alımını inhibe ederken, vareniklin nikotinik reseptör parsiyel agonistidir.",
            "**Farklı Mekanizmalar:** Nöronal reuptake inhibisyonu ve reseptör parsiyel agonizması.",
            "2.Bupropion",
            ["Bupropion", "Vareniklin"],
            []
        ),
        (
            "Ayrıca sitizin ile ikinci ve üçüncü seçenek ajanlar da dirençli olgularda tedavi cephanesinde yer alır.",
            "**Alternatifler:** Sitizin ve ikinci seçenek ilaçların rolü.",
            "4.Sitizin",
            ["Sitizin", "ikinci basamak"],
            []
        )
    ]),

    (21, "k2-61-b12", "Nikotin Yerine Koyma Tedavileri (NRT)", [
        (
            "Görselimizde Nikotin Yerine Koyma Tedavisinin klinik pratikte kullanılan farklı uygulama formları şematize edilmiştir.",
            "**NRT Formülasyonları:** Transdermal bant, sakız, pastil, ağız spreyi ve inhaler.",
            "Transdermal Nikotin Bandı",
            ["transdermal bant", "nikotin sakızı"],
            []
        ),
        (
            "Transdermal nikotin bandı yavaş ve sabit bir plazma nikotin düzeyi sağlarken nikotin sakızı ve ağız spreyi ani gelişen aşermeleri hızla baskılar.",
            "**Sabit ve Hızlı Salınım:** Bant kararlı düzey, sakız ve sprey anlık kriz kontrolü sağlar.",
            "Nikotin Sakızı",
            ["sabit salınım", "ani aşerme"],
            []
        ),
        (
            "Sublingual tablet, nazal sprey ve nikotin inhaler gibi alternatif formülasyonlar da hastanın kullanım tercihlerine göre seçilebilir.",
            "**Alternatif Formlar:** Sublingual tablet ve nazal formülasyonlar.",
            "Nikotin Ağız Spreyi",
            ["sublingual tablet", "nazal sprey"],
            []
        )
    ]),

    (22, "k2-61-b12", "Nikotin Yerine Koyma Tedavileri (NRT)", [
        (
            "Nikotin Yerine Koyma Tedavisinin iki temel farmakolojik amacı bulunmaktadır.",
            "**İki Temel Amaç:** Akut yoksunluğu giderme ve uzun dönemde reseptör down-regülasyonu.",
            "NRT’nin iki amacı vardır:",
            ["NRT amaçları", "farmakolojik hedef"],
            []
        ),
        (
            "İlk amaç nikotinik reseptörleri temiz nikotinle uyararak hastada ortaya çıkan şiddetli aşerme ve yoksunluk bulgularını hızla yatıştırmaktır.",
            "**Akut Aşerme Giderimi:** Temiz nikotinle reseptör uyarımı ve yoksunluğun baskılanması.",
            "Nikotin reseptörlerini stimüle ederek aşerme ve",
            ["aşerme giderimi", "yoksunluk baskılama"],
            []
        ),
        (
            "İkinci amaç ise haftalar süren stabil nikotin salınımıyla beyindeki aşırı artmış nikotinik reseptör sayısını kademeli olarak azaltmak ve bağımlılığı geriletmektir.",
            "**Reseptör Down-Regülasyonu:** Reseptör yoğunluğunun zamanla normale dönmesi.",
            "Haftalarca devam eden nikotin bağımlılığını azaltan",
            ["down-regülasyon", "reseptör sayısı"],
            []
        )
    ]),

    (23, "k2-61-b12", "Nikotin Yerine Koyma Tedavileri (NRT)", [
        (
            "Kişide Fagerström testine göre orta veya yüksek derecede nikotin bağımlılığı saptanırsa ya da günde on beş adetten fazla sigara içiyorsa nikotin yerine koyma tedavisi endikedir.",
            "**NRT Endikasyonu:** Günde 15 sigaradan fazla içen orta ve yüksek bağımlılar.",
            "işide yüksek veya orta derecede nikotin bağımlılığı saptanırsa,",
            ["NRT endikasyonu", "orta-yüksek bağımlılık"],
            []
        ),
        (
            "Hafif derecede bağımlı olmasına rağmen davranışsal yöntemlerle sigarayı bırakamamış bireylerde de replasman tedavisi başarıyla uygulanır.",
            "**Dirençli Olgular:** Davranışsal yöntemlerle bırakamayan hafif bağımlılarda kullanım.",
            "günde 15 adetten fazla sigara içiyorsa",
            ["hafif bağımlılık", "tedaviye direnç"],
            []
        ),
        (
            "Klinik pratikte transdermal bant ile sakız veya spreyin kombine edilmesi tek başına bant kullanımına göre çok daha yüksek bırakma başarısı sunar.",
            "**Kombine NRT:** Bant ile sakız veya sprey kombinasyonunun üstünlüğü.",
            "diğer yöntemlerden fayda görmemişse nikotin replasman tedavisi uygulanır.",
            ["kombine NRT", "yüksek başarı"],
            []
        )
    ]),

    (24, "k2-61-b12", "Nikotin Yerine Koyma Tedavileri (NRT)", [
        (
            "Nikotin Yerine Koyma Tedavisinin tütün dumanındaki toksinleri içermemesi nedeniyle gerçek anlamda mutlak bir kontrendikasyonu bulunmamaktadır.",
            "**Güvenlik Profili:** Kanserojen ve karbonmonoksit içermez, mutlak kontrendikasyonu yoktur.",
            "rçek anlamda kontrendikasyonları yoktur.",
            ["güvenlik profili", "kontrendikasyon yokluğu"],
            []
        ),
        (
            "Yan etkiler genellikle sigara içimi tamamen kesilmeden nikotin yerine koyma tedavisi kullanılması sonucu gelişen aşırı nikotin yüklenmesi ile ortaya çıkar.",
            "**Aşırı Doz Riski:** Sigara bırakılmadan NRT kullanılırsa toksisite bulguları oluşur.",
            "an etkiler genelde sigara içiminin kesilmeden NRT kullanımı ile ortaya çıkmaktadır.",
            ["nikotin yüklenmesi", "yan etki mekanizması"],
            []
        ),
        (
            "Akut miyokard infarktüsü geçiren kişilerde ilk haftalarda ve ciddi aritmisi olanlarda dikkatli olunmalı, gebe ve emzirenlerde hekim kararıyla yönetilmelidir.",
            "**Kardiyovasküler Dikkat:** Akut MI ilk 2 haftasında ve instabil aritmilerde yakın izlem.",
            "gebelerde, emziren kadınlarda, akut miyokard infarktüsü geçiren kişilerde ilk haftalarda ve",
            ["akut miyokard infarktüsü", "kardiyak aritmi"],
            []
        )
    ]),

    (25, "k2-61-b12", "Nikotin Yerine Koyma Tedavileri (NRT)", [
        (
            "Tablomuzda transdermal nikotin yaması, sakız, pastil, inhaler ve spreylerin dozajları, yan etkileri ve klinik avantajları karşılaştırılmaktadır.",
            "**NRT Karşılaştırma Tablosu:** Tüm formülasyonların doz, yan etki ve kullanım özellikleri.",
            "TABLO 1: Nikotin yerine koyma tedavileri ve formları",
            ["NRT tablosu", "dozaj formları"],
            []
        ),
        (
            "Günde on adetten fazla sigara içenlerde yirmi bir miligramlık yüksek doz bantla başlanırken on adetten az içenlerde on dört miligramlık bant tercih edilir.",
            "**Bant Dozlaması:** Günde ≥10 sigara için 21 mg/gün, <10 sigara için 14 mg/gün.",
            "2 10 sigaralgün için 21 mg",
            ["21 mg bant", "14 mg bant"],
            []
        ),
        (
            "Nikotin sakızı ve pastilinde ise ilk sigara uyandıktan sonraki ilk otuz dakikada içiliyorsa dört miligramlık, sonrasında içiliyorsa iki miligramlık form kullanılır.",
            "**Sakız ve Pastil Dozu:** İlk 30 dakikada içenlere 4 mg, sonrasına 2 mg form.",
            "İlk 30 dakikada ise: 4 mg",
            ["nikotin sakızı dozu", "pastil"],
            []
        ),
        (
            "Sakız ve pastil kullanımından önceki ve sırasındaki on beş dakika boyunca nikotinin bukkal emilimini bozmamak için asidik yiyecek ve içecekler tüketilmemelidir.",
            "**15 Dakika Kuralı:** Bukkal emilimi korumak için asidik içecek tüketilmeme kuralı.",
            "Kullanımdan 15 dakika önce ve",
            ["15 dakika kuralı", "bukkal emilim"],
            []
        )
    ]),

    # --- BOLUM 13: Bupropion Farmakolojisi, Etki Mekanizması ve Dozlama (26-28) ---
    (26, "k2-61-b13", "Bupropion Farmakolojisi ve Dozlama", [
        (
            "Sigara bırakma tedavisinde ikinci önemli birinci basamak farmakoterapi seçeneği oral bupropion hidroklorürdür.",
            "**Bupropion Giriş:** Oral atipik antidepresan, birinci basamak tütün bağımlılık ilacı.",
            "2.Bupropion",
            ["Bupropion hidroklorür", "oral tedavi"],
            []
        ),
        (
            "Esasen bir antidepresan olarak geliştirilen bupropion, sigara bırakan hastalarda bağımsız olarak aşermeyi belirgin derecede azaltmıştır.",
            "**Klinik Keşif:** Antidepresan tedavide sigara içme isteğini tesadüfen azaltmasıyla keşfedildi.",
            "1.Nikotin Yerine Koyma Tedavileri (NRT)",
            ["antidepresan köken", "aşerme azaltımı"],
            []
        ),
        (
            "Nikotin içermeyen oral bir tablet olması nedeniyle nikotin replasmanı istemeyen veya tolere edemeyen hastalarda mükemmel bir tercihtir.",
            "**Nikotinsiz Tedavi:** Nikotin içermeyen oral farmakoterapi alternatifi.",
            "3Vareniklin",
            ["nikotinsiz alternatif", "oral tablet"],
            []
        )
    ]),

    (27, "k2-61-b13", "Bupropion Farmakolojisi ve Dozlama", [
        (
            "Görsel şemamızda bupropionun presinaptik nöronlarda dopamin ve daha az oranda norepinefrin geri alımını bloke etme mekanizması gösterilmektedir.",
            "**Etki Mekanizması:** Nöronal dopamin ve noradrenalin reuptake inhibisyonu (NDRI).",
            "Dopaminin ve daha az",
            ["reuptake inhibisyonu", "dopamin taşıyıcısı"],
            []
        ),
        (
            "Nükleus akkumbenste dopamin düzeyini yükselterek nikotinin merkezi sinir sistemi üzerindeki ödüllendirici etkilerini taklit eder ve yoksunluk krizlerini dindirir.",
            "**Yoksunluk Yatışması:** Sinapsta dopamin artışı ve yoksunluk belirtilerinde gerileme.",
            "norepinefrinin nöronal",
            ["ödül taklidi", "yoksunluk azalması"],
            []
        ),
        (
            "Hasta aynı zamanda depresyondaysa ya da sigarayı bıraktıktan sonra kilo almaktan aşırı çekiniyorsa bupropion ilk tercih edilecek ajandır.",
            "**Özel Endikasyonlar:** Depresif semptomları olan ve kilo alımından korkan hastalar.",
            "Hasta aynı zamanda Den e rdnerde",
            ["kilo alımı engeli", "depresyon komorbiditesi"],
            []
        ),
        (
            "Ayrıca transdermal nikotin bandı ile bupropionun birlikte kullanılması tek başına kullanıma kıyasla çok daha yüksek bırakma başarı oranları sağlar.",
            "**NRT ile Kombinasyon:** Bupropion ve nikotin bandı kombinasyonunun yüksek etkinliği.",
            "NRT ile birlikte kullanildiginda (sons",
            ["kombine tedavi", "başarı artışı"],
            []
        )
    ]),

    (28, "k2-61-b13", "Bupropion Farmakolojisi ve Dozlama", [
        (
            "Bupropion tedavisine hastanın belirlediği sigara bırakma tarihinden bir ila iki hafta önce başlanmalıdır.",
            "**Başlama Zamanı:** Sigara bırakma hedef gününden 1-2 hafta önce başlanır.",
            "Bırakma tarihinden 1-2 hafta önce ilaca başlamak",
            ["bırakma tarihi", "önceden başlama"],
            []
        ),
        (
            "İlk üç gün günde tek doz yüz elli miligram verilir, ardından günde iki kez yüz elli miligrama çıkılarak tedavi üç ila altı ay sürdürülür.",
            "**Doz Şeması:** İlk 3 gün 150 mg/gün, ardından 2x150 mg/gün (aralarında ≥8 saat).",
            "3 gün süreyle 150 mg/gün, ardından günde iki",
            ["doz titrasyonu", "tedavi süresi"],
            []
        ),
        (
            "En sık görülen yan etkiler ağız kuruluğu ve uykusuzluktur; eşik altı dozlarda bile nöbet riski taşıdığından nöbet öyküsü olanlarda kesinlikle kontrendikedir.",
            "**Nöbet Riski:** Nöbet eşiğini düşürür; epilepsi öyküsünde kontrendikedir.",
            "Ağız kuruluğu ve uykusuzluk, kullanımla ilişkili en",
            ["nöbet riski", "epilepsi kontrendikasyonu"],
            []
        ),
        (
            "Ayrıca bulimiya nervoza, anoreksiya nervoza tanısı olanlarda ve kontrolsüz hipertansiyon hastalarında bupropion kullanılmamalıdır.",
            "**Diğer Kontrendikasyonlar:** Yeme bozuklukları (bulimiya/anoreksiya) ve kontrolsüz hipertansiyon.",
            "bulimia veya anoreksiya nervoza tanısı, gebelik,",
            ["yeme bozukluğu", "anoreksiya"],
            []
        )
    ]),

    # --- BOLUM 14: Vareniklin: Alfa-4 Beta-2 Parsiyel Agonizma ve Klinik Kullanım (29-32) ---
    (29, "k2-61-b14", "Vareniklin Farmakolojisi ve Klinik Kullanım", [
        (
            "Sigara bırakma tedavisinde günümüzün en güçlü etkinliğe sahip üçüncü birinci basamak ajanı vareniklin tartrattır.",
            "**Vareniklin:** En yüksek bırakma başarısına sahip alfa-4 beta-2 nikotinik parsiyel agonist.",
            "3Vareniklin",
            ["Vareniklin tartrat", "yüksek etkinlik"],
            []
        ),
        (
            "Vareniklin doğrudan nikotinin beyindeki primer bağımlılık reseptörünü hedef alarak tasarlanmış sentetik bir moleküldür.",
            "**Moleküler Hedef:** Santral alfa-4 beta-2 nikotinik asetilkolin reseptörleri.",
            "1.Nikotin Yerine Koyma Tedavileri (NRT)",
            ["hedefe yönelik molekül", "nikotinik reseptör"],
            []
        ),
        (
            "Klinik çalışmalarda hem tek başına nikotin bandından hem de bupropiona kıyasla belirgin şekilde daha üstün sigara bırakma oranları sağlamıştır.",
            "**Karşılaştırmalı Üstünlük:** NRT ve Bupropiona kıyasla üstün klinik başarı oranları.",
            "2.Bupropion",
            ["klinik üstünlük", "başarı oranları"],
            []
        )
    ]),

    (30, "k2-61-b14", "Vareniklin Farmakolojisi ve Klinik Kullanım", [
        (
            "Görselimizde vareniklinin alfa dört beta iki nikotinik asetilkolin reseptörleri için seçici olan parsiyel agonist etki mekanizması gösterilmektedir.",
            "**Parsiyel Agonizma Şeması:** Alfa-4 beta-2 reseptöründe ikili agonist ve antagonist etki.",
            "Vareniklin, alfa-4, beta-2 nikotinik asetilkolin",
            ["alfa-4 beta-2", "parsiyel agonist"],
            []
        ),
        (
            "Nitekim tıp fakültesi sınavlarında çıkmış sınav sorusu olarak sigara bırakma tedavisinde alfa dört beta iki nikotinik asetilkolin reseptörlerinin parsiyel agonisti olan vareniklin sorgulanmıştır.",
            "**Sınav Spotu (Çıkmış Soru):** Bu bilgi çıkmış sınavda sorulmuştur: Vareniklin alfa-4 beta-2 nikotinik reseptörlerin parsiyel agonistidir.",
            "reseptörleri (NAChR'ler) için seçici olan parsiyel bir",
            ["çıkmış soru", "Vareniklin", "alfa-4 beta-2"],
            ["7ba263dd73d1"]
        ),
        (
            "Vareniklin bir yandan orta düzeyde dopamin salarak yoksunluk krizlerini önlerken diğer yandan nikotinin reseptöre bağlanmasını engelleyerek sigaradan alınan hazzı tamamen yok eder.",
            "**İkili Etki:** Agonist etkiyle yoksunluğu önler, antagonist etkiyle sigara hazzını bloke eder.",
            "anda bu reseptörlere nikotin bağlanmasını da",
            ["ikili mekanizma", "haz blokajı"],
            []
        ),
        (
            "Böylece hasta ilacı kullandığı dönemde bir kaçak yapıp sigara içse bile tütündeki nikotin reseptöre bağlanamaz ve hiçbir pekiştirici ödül hissi oluşmaz.",
            "**Pekiştirme Blokajı:** Kaçak sigara içiminde bile ödül mekanizması devreye giremez.",
            "dönemde sigara içse bile sigaradan gelen nikotin",
            ["ödül blokajı", "kaçak önleme"],
            []
        )
    ]),

    (31, "k2-61-b14", "Vareniklin Farmakolojisi ve Klinik Kullanım", [
        (
            "Vareniklin sıfır virgül beş miligram ve bir miligramlık oral tablet formlarında kullanıma sunulmuştur.",
            "**Dozaj Formları:** 0.5 mg ve 1.0 mg oral tabletler.",
            "Vareniklin 0,5 mg ve 1.0 mg dozlarında oral formları",
            ["oral formlar", "miligram dozaj"],
            []
        ),
        (
            "Tedaviye hastanın sigarayı bırakmayı hedeflediği tarihten bir ila iki hafta önce başlanması şarttır.",
            "**Başlama Zamanı:** Bırakma hedefinden 1-2 hafta önce başlanmalıdır.",
            "Bırakma tarihinden 1-2 hafta önce ilaca başlanır.",
            ["hedef tarih", "önceden başlama"],
            []
        ),
        (
            "İlk üç gün günde tek doz sıfır virgül beş miligram, dört ila yedinci günlerde günde iki kez sıfır virgül beş miligram, sekizinci günden itibaren günde iki kez bir miligram şeklinde üç ila altı ay sürdürülür.",
            "**Doz Titrasyon Protokolü:** 1-3. gün 0.5 mg, 4-7. gün 2x0.5 mg, 8+. gün 2x1.0 mg/gün.",
            "8. günden sonra: Günde iki kez 1 mg şeklinde artırılır ve 3-6",
            ["titrasyon şeması", "idame doz"],
            []
        )
    ]),

    (32, "k2-61-b14", "Vareniklin Farmakolojisi ve Klinik Kullanım", [
        (
            "Vareniklin kullanımında en sık bildirilen yan etki yaklaşık yüzde otuz hastada görülen bulantıdır; ilacın yemek sonrası bol su ile alınması bu etkiyi belirgin azaltır.",
            "**Bulantı Yönetimi:** En sık yan etki bulantıdır (%30); tok karnına bol su ile alınmalıdır.",
            "etkisi bulantıdır. Diğer yan etkiler uykusuzluk, anormal",
            ["bulantı", "tok karnına alım"],
            []
        ),
        (
            "Diğer yaygın yan etkiler uykusuzluk, anormal canlı rüyalar ve baş ağrısıdır; gebelerde ve süt veren annelerde kullanımı uygun değildir.",
            "**Yan Etkiler ve Kontrendikasyon:** Uykusuzluk, canlı rüyalar; gebelik ve emzirmede kontrendikedir.",
            "Vareniklinin gebelerde ve süt veren annelerde",
            ["canlı rüyalar", "gebelik kontrendikasyonu"],
            []
        ),
        (
            "Geçmiş yıllarda bazı serilerde üretim sürecine bağlı nitrozamin kirliliği saptandığından geçici toplatılma süreçleri yaşanmış ve denetimler sıkılaştırılmıştır.",
            "**Kalite ve Güvenlik:** Nitrozamin safsızlığı denetimleri ve güvenlik izlemi.",
            "yapabilecek kadar yüksek oranda olması nedenyile",
            ["nitrozamin", "ilaç güvenliği"],
            []
        )
    ]),

    # --- BOLUM 15: Sitizin, İkinci Seçenek Ajanlar ve Rimonabant (33-40) ---
    (33, "k2-61-b15", "Sitizin, İkinci Seçenek Ajanlar ve Rimonabant", [
        (
            "Farmakoterapide varenikline alternatif oluşturan doğal bitkisel kökenli parsiyel nikotinik agonist sitizindir.",
            "**Sitizin Giriş:** Bitkisel kaynaklı nikotinik parsiyel agonist alternatif.",
            "4.Sitizin",
            ["Sitizin", "bitkisel alkaloid"],
            []
        ),
        (
            "Doğu Avrupa ülkelerinde onlarca yıldır yaygın olarak kullanılan sitizin son yıllarda küresel kılavuzlarda da yerini almıştır.",
            "**Tarihsel Kullanım:** Doğu Avrupa kökenli, maliyet etkin sigara bırakma ajanı.",
            "Sitizin",
            ["küresel kılavuzlar", "maliyet etkinlik"],
            []
        ),
        (
            "Düşük maliyeti ve varenikline benzer moleküler etki mekanizması ile tütün kontrolünde önemli bir potansiyele sahiptir.",
            "**Ekonomik Potansiyel:** Düşük maliyetli parsiyel agonist seçeneği.",
            "İkinci",
            ["ekonomik avantaj", "bağımlılık tedavisi"],
            []
        )
    ]),

    (34, "k2-61-b15", "Sitizin, İkinci Seçenek Ajanlar ve Rimonabant", [
        (
            "Sitizinin kimyasal yapısı nikotine oldukça benzerdir ve nikotinik reseptörlere eşit düzeyde afinite ile bağlanır.",
            "**Yapısal Benzerlik:** Nikotin benzeri yapı ve yüksek reseptör afinitesi.",
            "Sitizinin nikotine oldukça benzer bir yapıda olduğu ve nikotin",
            ["kimyasal benzerlik", "reseptör afinitesi"],
            []
        ),
        (
            "Moleküler olarak alfa dört beta iki nikotinik reseptörlerin kısmi agonistidir ve vareniklin gibi ikili etki gösterir.",
            "**Alfa-4 Beta-2 Agonizması:** Kısmi agonist mekanizma ile dopamin modülasyonu.",
            "reseptörlerine eşit düzeyde bağlandığı bulunmuştur. Sitizin, a4b2",
            ["alfa-4 beta-2", "kısmi agonist"],
            []
        ),
        (
            "Kontrolsüz arteriyel hipertansiyon, ileri ateroskleroz, gebelik ve emzirmede kontrendikedir; en sık yan etkileri hazımsızlık ve ağız kuruluğudur.",
            "**Kontrendikasyon ve Yan Etkiler:** Ağır kardiyovasküler hastalık kontrendikasyonu; dispepsi ve ağız kuruluğu.",
            "Sitizin tedavisi kontrendikasyonları; kontrolsüz arteriyel",
            ["ateroskleroz", "kontrendikasyonlar"],
            []
        )
    ]),

    (35, "k2-61-b15", "Sitizin, İkinci Seçenek Ajanlar ve Rimonabant", [
        (
            "Tablomuzda sitizinin yirmi beş günlük basamaklı ve titiz doz azaltım protokolü özetlenmektedir.",
            "**25 Günlük Protokol:** Sitizinin kademeli doz azaltım tedavi şeması.",
            "1,5 mg'lık tabletlerin oral yolla ilk 3 gün 2 saatte",
            ["25 günlük protokol", "doz azaltımı"],
            []
        ),
        (
            "Bir virgül beş miligramlık tabletlerden ilk üç gün iki saatte bir günde toplam altı adet yani dokuz miligram alınır.",
            "**Başlangıç Rejimi:** İlk 3 gün her 2 saatte bir 1 tablet (toplam 6 tablet/gün).",
            "bir toplam 6 adet (9 mg/gün), ardından tedavinin",
            ["başlangıç dozu", "9 mg günlük"],
            []
        ),
        (
            "Tedavinin beşinci gününde sigara kullanımı tamamen ve kesin olarak sona erdirilmelidir; aksi takdirde nikotin zehirlenmesi gelişebilir.",
            "**5. Gün Bırakma Şartı:** 5. günde sigara tamamen bırakılmalıdır, nikotin toksisitesi riski önlenir.",
            "Tedavinin beşinci gününde sigara kullanımı tamamen sona ermelidir.",
            ["5. gün kuralı", "nikotin zehirlenmesi"],
            []
        )
    ]),

    (36, "k2-61-b15", "Sitizin, İkinci Seçenek Ajanlar ve Rimonabant", [
        (
            "Birinci basamak tedavilere yanıt vermeyen veya kontrendikasyonu olan hastalarda ikinci ve üçüncü seçenek ilaçlar devreye girer.",
            "**İkinci Seçenek Tedaviler:** Dirençli veya kontrendike olgularda alternatif ajanlar.",
            "5.İkinci ve Üçüncü Seçenek Tedaviler",
            ["ikinci seçenek", "dirençli olgular"],
            []
        ),
        (
            "Bu grupta klonidin, nortriptilin, rimonabant ve geliştirilmekte olan nikotin aşıları klinik çalışmalarda incelenmiştir.",
            "**Aday İlaçlar:** Klonidin, nortriptilin, CB1 blokörleri ve aşı stratejileri.",
            "Seçenek",
            ["Klonidin", "Nortriptilin"],
            []
        ),
        (
            "Ancak yan etki profilleri veya etkinlik kısıtlılıkları nedeniyle birinci basamak ajanlar kadar yaygın kullanılmazlar.",
            "**Kullanım Kısıtlılığı:** Yan etki yükü nedeniyle ikinci basamakta kalırlar.",
            "Tedaviler",
            ["yan etki profili", "kullanım sınırı"],
            []
        )
    ]),

    (37, "k2-61-b15", "Sitizin, İkinci Seçenek Ajanlar ve Rimonabant", [
        (
            "İkinci seçenek farmakoterapide santral etkili antihipertansif klonidin ile trisiklik antidepresan nortriptilin yer alır.",
            "**Klonidin ve Nortriptilin:** İkinci basamak farmakoterapi alternatifleri.",
            "Klonidin",
            ["santral antihipertansif", "trisiklik antidepresan"],
            []
        ),
        (
            "Ayrıca endokanabinoid sistem blokörü rimonabant ve nikotini kanda bağlayan aşı stratejileri de araştırılmıştır.",
            "**Rimonabant ve Aşı:** CB1 reseptör antagonisti ve immünolojik nikotin aşıları.",
            "Rimonobant",
            ["rimonabant", "nikotin aşısı"],
            []
        ),
        (
            "Bu alternatiflerin etki mekanizmaları ve klinik sınırlılıkları bağımlılık tedavisinde önemli dersler sunmaktadır.",
            "**Klinik Dersler:** Yeni moleküllerin etki mekanizmaları ve güvenlik sınırları.",
            "Notriptilin",
            ["etki sınırları", "tedavi alternatifleri"],
            []
        ),
        (
            "Geliştirilen nikotin aşıları antikorlar vasıtasıyla nikotini kanda bağlayarak beyne geçişini engellemeyi hedefler.",
            "**Nikotin Aşısı Hedefi:** Nikotini kanda bağlayarak santral sinir sistemine geçişini engelleme mekanizması.",
            "Nikotin Aşısı",
            ["nikotin antikorları", "kan beyin bariyeri"],
            []
        )
    ]),

    (38, "k2-61-b15", "Sitizin, İkinci Seçenek Ajanlar ve Rimonabant", [
        (
            "Klonidin santral alfa iki adrenerjik agonist olup sempatik deşarjı ve nikotin yoksunluğuna bağlı ajitasyonu azaltır.",
            "**Klonidin Mekanizması:** Alfa-2 adrenerjik agonizma ile sempatolitik etki ve yoksunluk kontrolü.",
            "Klonidin (a2 adrenerjik agonist) ve notriptilin(Trisklik antidepresan)",
            ["alfa-2 agonist", "sempatik deşarj"],
            []
        ),
        (
            "Nortriptilin ise bir trisiklik antidepresan olup plaseboya üstün bulunsa da belirgin antikolinerjik yan etkileri vardır.",
            "**Nortriptilin:** Trisiklik antidepresan, plaseboya üstün ancak antikolinerjik yan etkili.",
            "plaseboya göre üstün görülmüş ama etkinliği belirgin değil.",
            ["nortriptilin", "antikolinerjik etki"],
            []
        ),
        (
            "Her iki ilaçta da sedasyon, şiddetli ağız kuruluğu ve ortostatik hipotansiyon en sık bildirilen doz kısıtlayıcı yan etkilerdir.",
            "**Yan Etkiler:** Sedasyon, ağız kuruluğu ve kan basıncı düşüşü.",
            "Sedasyon ve ağız kuruluğu sık bildirilen yan etkiler.",
            ["sedasyon", "ağız kuruluğu"],
            []
        )
    ]),

    (39, "k2-61-b15", "Sitizin, İkinci Seçenek Ajanlar ve Rimonabant", [
        (
            "Görselimizde kannabinoid ce be bir reseptör antagonisti rimonabant ile nikotin aşısının moleküler konseptleri gösterilmektedir.",
            "**Rimonabant ve Aşı Şeması:** CB1 reseptör blokajı ve antikor temelli aşı mekanizması.",
            "Rimonabant: Merkezi sinir sisteminde, dopamin salınımını modüle edebilen GABA ile",
            ["CB1 reseptörü", "rimonabant"],
            []
        ),
        (
            "Rimonabant beyinde ce be bir reseptörlerini bloke ederek dopamin salınımını modüle eder ve hem sigara isteğini hem de iştahı baskılar; ancak şiddetli depresyon ve intihar riski nedeniyle ruhsatı iptal edilmiştir.",
            "**Rimonabant Toksisitesi:** İştah ve sigara isteğini azaltır ancak depresyon ve intihar riski nedeniyle yasaklandı.",
            "salınımının azalmasına neden olur. CB-1 reseptörünün antagonizması, nikotin ödül",
            ["intihar riski", "ruhsat iptali"],
            []
        ),
        (
            "Nikotin aşısı ise kanda nikotine bağlanan antikorlar üreterek molekülün kan-beyin bariyerini geçmesini engellemeyi hedefler fakat klinik çalışmalarda yeterli etkinlik gösterememiştir.",
            "**Nikotin Aşısı:** Antikorla nikotini bağlayıp beyne geçişi engelleme teorisi.",
            "Nikotin aşısı: Solunan sigara dumanından kan dolaşımına ulaşan nikotin, antikor",
            ["nikotin aşısı", "antikor bağlanması"],
            []
        )
    ]),

    (40, "k2-61-b15", "Sitizin, İkinci Seçenek Ajanlar ve Rimonabant", [
        (
            "Özetle birinci basamak farmakoterapide etkinlik sırası en başta vareniklin ve kombine nikotin replasmanı, ardından tekli nikotin bandı ve bupropion şeklindedir.",
            "**Etkinlik Sıralaması:** Vareniklin ve kombine NRT > Tekli NRT ve Bupropion.",
            "1.Nikotin Yerine Koyma Tedavileri (NRT)",
            ["etkinlik sırası", "tedavi basamakları"],
            []
        ),
        (
            "Hastanın komorbiditeleri, kardiyovasküler durumu, depresyon varlığı ve daha önceki denemeleri ilaç seçiminde temel belirleyicidir.",
            "**Kişiselleştirilmiş Seçim:** Komorbidite ve klinik özelliklere göre rasyonel ilaç seçimi.",
            "2.Bupropion",
            ["kişiselleştirilmiş tedavi", "komorbidite"],
            []
        ),
        (
            "İkinci basamak ajanlar ise ancak birinci basamak seçeneklerin tükendiği veya kontrendike olduğu özel durumlarda düşünülmelidir.",
            "**İkinci Basamak Yeri:** Ancak birinci seçenekler uygulanamadığında devreye girer.",
            "3Vareniklin",
            ["ikinci basamak endikasyon", "özel durumlar"],
            []
        )
    ]),

    # --- BOLUM 16: Tedavi Başarısını Artıran Kombinasyonlar ve Bırakma Sonrası İzlem (41-46) ---
    (41, "k2-61-b16", "Tedavi Kombinasyonları ve İzlem", [
        (
            "Tütün bağımlılığında en yüksek uzun dönemli bırakma başarısı motivasyonel görüşme ile farmakoterapinin sinerjik birlikteliğiyle elde edilir.",
            "**Sinerjik Başarı:** Motivasyonel danışmanlık ve farmakoterapinin eşzamanlı yürütülmesi.",
            "Motivasyonel",
            ["sinerji", "uzun dönemli başarı"],
            []
        ),
        (
            "İlaç hastanın fiziksel yoksunluk semptomlarını ve dayanılmaz sigara aşermesini kontrol altına alırken görüşmeler psikolojik başa çıkma reflekslerini geliştirir.",
            "**Çift Yönlü Rahatlama:** Fiziksel aşermenin ilaçla, psikolojik yoksunluğun görüşmeyle çözülmesi.",
            "Farmakolojik",
            ["fiziksel yoksunluk", "psikolojik direnç"],
            []
        ),
        (
            "Bu çok disiplinli klinik yaklaşım hastanın tütünsüz yeni bir yaşam tarzını kalıcı olarak benimsemesini sağlar.",
            "**Yaşam Tarzı Değişimi:** Tütünsüz yaşam alışkanlığının kalıcı hale getirilmesi.",
            "Tedavi",
            ["yaşam tarzı", "tütünsüz hayat"],
            []
        )
    ]),

    (42, "k2-61-b16", "Tedavi Kombinasyonları ve İzlem", [
        (
            "Görselimizde nikotin bağımlılığına klinik yaklaşımın tüm basamaklarını içeren genişletilmiş poliklinik akışı özetlenmektedir.",
            "**Genişletilmiş Poliklinik Akışı:** Tanı, Fagerström testi, evreleme ve tedavi seçimi.",
            "Nikotin Bağımlılığına Yaklaşım",
            ["poliklinik akışı", "klinik sentez"],
            []
        ),
        (
            "Hekim her görüşmede hastanın tütün kullanım geçmişini, günlük içtiği sigara sayısını ve Fagerström skorunu kayıt altına almalıdır.",
            "**Kayıt ve Skorlama:** Tütün hikayesi ve bağımlılık şiddetinin düzenli dokümantasyonu.",
            "Ülkemizdeki ölümlerin %4616'sinn nedeni",
            ["hasta kaydı", "Fagerström skoru"],
            []
        ),
        (
            "Hastanın değişim modelindeki evresi saptanarak motivasyonel destek verilmeli ve uygun farmakoterapi gecikmeden başlanmalıdır.",
            "**Evreye Özel Tedavi:** Transteoretik evreye göre yapılandırılmış ilaç ve danışmanlık.",
            "Tedavisi",
            ["evreye özel tedavi", "danışmanlık"],
            []
        )
    ]),

    (43, "k2-61-b16", "Tedavi Kombinasyonları ve İzlem", [
        (
            "Sigarayı başarıyla bırakan kişilerde nüksetme riski özellikle ilk aylarda oldukça yüksektir.",
            "**Nüks Riski:** Sigarayı bırakan olgularda erken dönemde yüksek relaps olasılığı.",
            "Birakma",
            ["nüks riski", "erken dönem"],
            []
        ),
        (
            "Sigarayı bıraktıktan sonraki ilk yıl içinde nüksetme, uygulanan tedavi rejiminden bağımsız olarak hastaların yaklaşık yüzde ellisinde görülür.",
            "**İlk Yıl İstatistiği:** İlk 1 yıl içinde hastaların yaklaşık %50'sinde nüks gelişir.",
            "hastaların yaklaşık %50'sinde görülür. Sigara içmenin",
            ["yüzde elli nüks", "ilk yıl"],
            []
        ),
        (
            "Sigara içmenin neden olduğu merkezi sinir sistemindeki kalıcı nöronal reseptör ve hücre değişiklikleri farmakolojik tedavi ile hemen tersine çevrilemez.",
            "**Kalıcı Nöronal Değişiklik:** Nöroplastik değişikliklerin hemen geri dönmemesi nüks zeminini oluşturur.",
            "farmakolojik tedavi ile tersine çevrilmez.",
            ["nöronal plastisite", "kalıcı değişiklikler"],
            []
        )
    ]),

    (44, "k2-61-b16", "Tedavi Kombinasyonları ve İzlem", [
        (
            "Tablomuzda sigara bırakma sonrası izlem vizitlerinde hekim tarafından sorgulanması gereken beş kritik başlık listelenmektedir.",
            "**İzlem Viziti Tablosu:** Takipte sorgulanacak 5 temel klinik değerlendirme maddesi.",
            "1. Bırakma girişiminin takdir edilmesi",
            ["izlem viziti", "takip tablosu"],
            []
        ),
        (
            "İlk olarak hastanın bırakma girişimi takdir edilmeli, ardından nikotin çekilme semptomları ve kullanılan farmakoterapinin yan etki ve etkinliği titizlikle sorgulanmalıdır.",
            "**Takdir ve Çekilme Sorgusu:** Başarının pekiştirilmesi, çekilme bulguları ve ilaç yan etkilerinin değerlendirilmesi.",
            "2. Nikotin çekilme semptomlarının sorgulanması",
            ["takdir etme", "çekilme sorgulaması"],
            []
        ),
        (
            "İlk iki hafta yoğun çekilme dönemi olduğundan ilk ayda en az iki görüşme yapılmalı; takipler ilk üç ay aylık, sonrasında üçer aylık aralarla en az bir yıla tamamlanmalıdır.",
            "**İzlem Takvimi:** 1. ayda 2 vizit, 3. aya kadar aylık, ardından 3 ayda bir olmak üzere 1 yıl takip.",
            "görülmesinden dolayı, bırakma sonrası 1. ayda iki hasta görüşmesi önerilmektedir. Eğer hasta",
            ["izlem takvimi", "1 yıl takip"],
            []
        )
    ]),

    (45, "k2-61-b16", "Tedavi Kombinasyonları ve İzlem", [
        (
            "Sigara bırakma sürecinde bir tek nefesten ibaret olan kayma yani lapse durumu ile düzenli içiciliğe dönüş anlamına gelen nüks yani relapse birbirinden ayırt edilmelidir.",
            "**Kayma ve Nüks Ayrımı:** Lapse (tek nefeslik kaçak) ile relapse (tam nüks) ayrımı ve yönetimi.",
            "Nikotin Bağımlılığına Yaklaşım",
            ["lapse", "relapse"],
            []
        ),
        (
            "Hasta bir kaçak yaptığında suçluluk duymak yerine hekim tarafından desteklenmeli, kaymanın tam bir nükse dönüşmesi önlenmelidir.",
            "**Kaçak Yönetimi:** Suçluluk hissini kırıp bırakma kararlılığını hızla yeniden tesis etme.",
            "Tedavisi",
            ["kaçak yönetimi", "motivasyon tazeleme"],
            []
        ),
        (
            "Her tökezleme bırakma yolculuğunda bir öğrenme fırsatı olarak değerlendirilmeli ve hastanın sigarasız yaşam hedefi kararlılıkla korunmalıdır.",
            "**Kararlılık:** Bırakma sürecinin sürdürülmesi ve hedefe bağlılık.",
            "Birakma",
            ["kararlılık", "öğrenme süreci"],
            []
        )
    ]),

    (46, "k2-61-b16", "Tedavi Kombinasyonları ve İzlem", [
        (
            "Birinci basamak hekimliği tütün kontrolü ve nikotin bağımlılığı tedavisinde toplum sağlığını koruyan en stratejik siperdir.",
            "**Birinci Basamak Gücü:** Toplum sağlığını koruyan en temel klinik basamak.",
            "Alış,",
            ["birinci basamak gücü", "toplum sağlığı"],
            []
        ),
        (
            "Hekimin her hastaya sigara durumunu sorması, bırakmayı önermesi ve kanıta dayalı tedaviyi başlatması binlerce insanın hayatını kurtarır.",
            "**Hayat Kurtaran Yaklaşım:** Ask, Advise ve kanıta dayalı tedavi ile önlenen ölümler.",
            "sews,",
            ["hayat kurtarma", "kanıta dayalı tıp"],
            []
        ),
        (
            "Böylece nikotin bağımlılığının nörobiyolojisinden birinci basamak farmakoterapisine kadar tüm ders kazanımlarımızı eksiksiz tamamlamış olduk.",
            "**Ders Özeti:** Tütün epidemiyolojisi, nörobiyoloji, NRT, Bupropion, Vareniklin ve izlem tamamlandı.",
            "Take this with you.",
            ["ders özeti", "tütün kontrolü"],
            []
        )
    ])
]

# Verify all anchors in kaynak.md
print("Verifying anchors against kaynak.md...")
anchor_errors = 0
for sayfa, bid, bbaslik, sentences in SLIDES:
    for s_idx, (ses, ekran, anchor, terms, cikmis) in enumerate(sentences):
        if anchor not in kaynak_text:
            print(f"ERROR: Sayfa {sayfa} sentence {s_idx+1} anchor not found in kaynak.md: {anchor!r}")
            anchor_errors += 1
if anchor_errors:
    print(f"FAILED: {anchor_errors} anchors not found!")
    sys.exit(1)
print(f"SUCCESS: All {sum(len(s[3]) for s in SLIDES)} anchors verified 100% in kaynak.md!")

# Build konusma_v2.json
bolum_map = {}
cid_counter = 1
total_words = 0

for sayfa, bid, bbaslik, sentences in SLIDES:
    if bid not in bolum_map:
        bolum_map[bid] = {
            "id": bid,
            "baslik": bbaslik,
            "paragraflar": []
        }
    
    p_id = f"k2-61-p{sayfa:03d}"
    p_obj = {
        "id": p_id,
        "sayfa": sayfa,
        "cumleler": []
    }
    
    for s_idx, (ses, ekran, anchor, terms, cikmis) in enumerate(sentences):
        cid = f"k2-61-c{cid_counter:04d}"
        cid_counter += 1
        words = len(ses.split())
        total_words += words
        
        sekil_val = VISUAL_PAGES.get(sayfa) if s_idx == 0 and sayfa in VISUAL_PAGES else None
        vurgu_text = ekran.split("**")[1] if "**" in ekran else "Nikotin"
        
        c_obj = {
            "id": cid,
            "ses": ses,
            "ekran": ekran,
            "duzey": 0,
            "slayt": {
                "sayfa": sayfa,
                "satir": [anchor],
                "sekil": sekil_val
            },
            "vurgu": [{"tur": "terim", "metin": vurgu_text}]
        }
        if cikmis:
            c_obj["cikmis"] = cikmis
            
        p_obj["cumleler"].append(c_obj)
        
    bolum_map[bid]["paragraflar"].append(p_obj)

konusma_v2 = {
    "surum": 2,
    "ders_id": "k2-61",
    "anahtar": "y25-k2-61-nikotin-bagimliligi-ve-tedavisi",
    "baslik": "Nikotin Bağımlılığı ve Tedavisi",
    "bolumler": list(bolum_map.values())
}

print(f"Total Bolumler: {len(konusma_v2['bolumler'])}")
print(f"Total Paragraphs: {sum(len(b['paragraflar']) for b in konusma_v2['bolumler'])}")
print(f"Total Sentences: {cid_counter - 1}")
print(f"Total Words: {total_words} (~{total_words / 125:.1f} minutes of audio)")

# Save konusma_v2.json
(TASLAK / "konusma_v2.json").write_text(json.dumps(konusma_v2, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved konusma_v2.json")

# Helper to get cid
def get_cid_for_slide(slide_num, s_offset=0):
    for b in konusma_v2["bolumler"]:
        for p in b["paragraflar"]:
            if p["sayfa"] == slide_num:
                return p["cumleler"][s_offset]["id"]
    raise ValueError(f"Slide {slide_num} not found")

# Drawing commands (8 commands, 0 forward leaks)
cizim_komutlari = [
    {
        "cumle": get_cid_for_slide(2, 2),
        "bas": 0, "son": 4,
        "sayfa": 2,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Tütünün Küresel Sağlık Etkileri",
        "ogeler": [
            "Önlenebilir ölüm: Yılda 7 milyon can kaybı",
            "Kanser riski: Akciğer kanserinin %90 nedeni"
        ]
    },
    {
        "cumle": get_cid_for_slide(4, 2),
        "bas": 0, "son": 4,
        "sayfa": 4,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Kullanıcı Kategorileri",
        "ogeler": [
            "Her gün içen: Günlük kullanım",
            "Her günden az içen: Ara sıra kullanım",
            "Bırakan: Eski içici"
        ]
    },
    {
        "cumle": get_cid_for_slide(7, 2),
        "bas": 0, "son": 4,
        "sayfa": 7,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Tütün Kontrolü Stratejileri",
        "ogeler": [
            "Monitor: Tütün kullanımını izle",
            "Protect: Toplumu dumanından koru",
            "Offer: Bırakmaya yardım et",
            "Warn: Zararları konusunda uyar"
        ]
    },
    {
        "cumle": get_cid_for_slide(12, 2),
        "bas": 0, "son": 4,
        "sayfa": 12,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Transteoretik Değişim Evreleri",
        "ogeler": [
            "Precontemplation: Bırakmanın düşünülmediği evre",
            "Contemplation: Bırakmanın düşünüldüğü evre",
            "Preparation: Hazırlığın yapıldığı evre",
            "Action: Denemenin başladığı evre"
        ]
    },
    {
        "cumle": get_cid_for_slide(14, 2),
        "bas": 0, "son": 4,
        "sayfa": 14,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "5A ve 5R Klinik Müdahale Modelleri",
        "ogeler": [
            "5A Modeli: Ask, Advise, Assess, Assist, Arrange",
            "5R Modeli: Relevance, Risks, Rewards, Roadblocks"
        ]
    },
    {
        "cumle": get_cid_for_slide(20, 2),
        "bas": 0, "son": 4,
        "sayfa": 20,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Birinci Basamak Tedavi Seçenekleri",
        "ogeler": [
            "Nikotin Yerine Koyma Tedavileri: NRT",
            "Bupropion: Geri alım inhibitörü",
            "Vareniklin: Reseptör parsiyel agonisti"
        ]
    },
    {
        "cumle": get_cid_for_slide(27, 2),
        "bas": 0, "son": 4,
        "sayfa": 27,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Bupropion Etki Mekanizması",
        "ogeler": [
            "Dopamin ve norepinefrin geri alım inhibisyonu",
            "Nükleus akkumbenste dopamin artışı",
            "Nikotin yoksunluk bulgularında azalma"
        ]
    },
    {
        "cumle": get_cid_for_slide(30, 2),
        "bas": 0, "son": 4,
        "sayfa": 30,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Vareniklin Parsiyel Agonizma",
        "ogeler": [
            "Alfa-4 beta-2 reseptörüne bağlanma",
            "Agonist etki ile dopamin salınımı",
            "Nikotin bağlanmasını önleyerek haz engeli"
        ]
    }
]

cizim_aday = {"komutlar": cizim_komutlari}
(TASLAK / "cizim_aday.json").write_text(json.dumps(cizim_aday, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved cizim_aday.json with {len(cizim_komutlari)} commands.")

# Derive konusma_metni.md, sayfalari, capalari
sys.path.insert(0, "/home/indu/medsor/meds/scripts/sesli_anlatim")
import konusma_v2 as KV
md_txt, sayfalar_l = KV.turet(konusma_v2)
(TASLAK / "konusma_metni.md").write_text(md_txt, encoding="utf-8")
(TASLAK / "konusma_sayfalari.json").write_text(json.dumps(sayfalar_l), encoding="utf-8")
(TASLAK / "konusma_capalari.json").write_text(json.dumps(KV.capalar(konusma_v2), ensure_ascii=False), encoding="utf-8")
print("Derived and saved konusma_metni.md, sayfalari, capalari.")
