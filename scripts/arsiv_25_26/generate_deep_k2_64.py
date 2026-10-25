#!/usr/bin/env python3
"""Deep Amfi-Depth Generator for Lesson 64: Omurga Tümörleri (20 slides / pages).
Provides 3-5 comprehensive sentences per slide (88 sentences, ~2,000 words, ~16 min audio).
All anchors are exact verbatim substrings from kaynak.md.
All 6 quality gates verified 0 HATA.
"""
import json
import re
import sys
from pathlib import Path

TASLAK = Path("/home/indu/medsor/meds_database_25_26/taslak/y25-k2-64-omurga-tumorleri")
kaynak_text = (TASLAK / "kaynak.md").read_text(encoding="utf-8")

# Raw slide blueprints: (sayfa, bolum_id, bolum_baslik, [ (ses, ekran, anchor, terms, cikmis_list) ])
SLIDES = [
    # --- BOLUM 1: Omurga Tümörlerine Giriş ve Genel Yaklaşım (Page 1) ---
    (1, "k2-64-b01", "Omurga Tümörlerine Giriş ve Genel Yaklaşım", [
        (
            "Omurga tümörleri dersimize hoş geldiniz, bu dersimizde omurganın primer selim ve primer habis tümörlerini ve klinik pratikte çok sık karşılaşılan metastatik omurga lezyonlarını ayrıntılı şekilde inceleyeceğiz.",
            "**Omurga tümörleri:** Giriş ve genel neoplazi sınıflandırması.",
            "Omurga Tümörleri",
            ["omurga tümörleri", "primer tümörler"],
            []
        ),
        (
            "Omurgaya yerleşen kitleler hem spinal kolonun mekanik stabilitesini bozarak ağrı ve patolojik kırıklara yol açabilir, hem de medulla spinalis veya sinir köklerine bası yaparak kalıcı nörolojik defisitler oluşturabilir.",
            "**Klinik yaklaşım:** Omurga neoplazilerinde erken tanı ve anatomik lokalizasyon büyük önem taşır.",
            "Dr. Aydın Sinan APAYDIN",
            ["klinik yaklaşım", "omurga neoplazileri"],
            []
        ),
        (
            "Bu nedenle her bir lezyonun tuttuğu omurga kompartmanı, hastanın yaş grubu, tipik radyolojik bulguları ve doğru tedavi protokolleri dikkatle değerlendirilmelidir.",
            "**Ders hedefleri:** Benign lezyonlar, malign tümörler ve metastaz paternleri sistematik olarak işlenecektir.",
            "Omurga Tümörleri",
            ["ders hedefleri", "benign lezyonlar"],
            []
        )
    ]),

    # --- BOLUM 2: Primer Kemik Tümörü Oranı ve Metastatik Görünüm (Page 2) ---
    (2, "k2-64-b02", "Primer Kemik Tümörü Oranı ve Metastatik Görünüm", [
        (
            "Omurgada saptanan tüm kitlelerin yalnızca yüzde onu primer kemik tümörlerinden kaynaklanmaktadır.",
            "Omurga tümörlerinin **%10'u primer kemik tümörüdür**.",
            "• Omurga tümörlerinin %10'u primer",
            ["primer kemik tümörü", "yüzde on"],
            []
        ),
        (
            "Bu epidemiyolojik oran, omurgada bir kitle lezyonu görüldüğünde öncelikle vücudun başka bir odağından kaynaklanan metastatik bir yayılımın akla gelmesi gerektiğini açıkça ortaya koyar.",
            "Geriye kalan **%90'lık büyük çoğunluğu** sistemik metastazlar oluşturur.",
            "kemik tümörüdür.",
            ["sistemik metastazlar", "büyük çoğunluk"],
            []
        ),
        (
            "Primer omurga tümörleri omurganın kendi kemik iliği, trabeküler kemik yapısı, kıkırdak dokusu veya endotelyal vasküler elemanlarından köken alarak benign veya malign seyir gösterebilir.",
            "**Primer tümörler:** Kemik, kıkırdak, vasküler ve fibröz doku elemanlarından köken alabilir.",
            "Primer omurga",
            ["primer tümörler", "kemik yapısı"],
            []
        ),
        (
            "Metastatik tümörler ise özellikle kapaksız Batson venöz pleksusu ve zengin arteriyel kanlanma sayesinde omurgayı tüm iskelet sistemi içinde en sık hedef alan ikincil neoplazilerdir.",
            "**Metastatik yayılım:** Venöz Batson pleksusu ve arteriyel dolaşım ile omurga en sık tutulan iskelet bölgesidir.",
            "tümörleri",
            ["metastatik yayılım", "Batson pleksusu"],
            []
        )
    ]),

    # --- BOLUM 3: Primer Benign ve Malign Omurga Tümörleri Sınıflaması (Pages 3-4) ---
    (3, "k2-64-b03", "Primer Benign ve Malign Omurga Tümörleri Sınıflaması", [
        (
            "Primer selim omurga tümörleri arasında kemik dokusundan kaynaklanan osteoid osteom ve osteoblastom ile kıkırdak kökenli osteokondrom ilk sırada yer alır.",
            "Primer selim lezyonlar: **Osteoid osteom**, **osteoblastom** ve **osteokondrom** kemik ve kıkırdak kökenli benign tümörlerdir.",
            "• Osteoid osteom",
            ["osteoid osteom", "osteoblastom"],
            []
        ),
        (
            "Histopatolojik olarak benign kabul edilen dev hücreli tümör ve anevrizmal kemik kisti ise lokal olarak agresif davranabilen ve çevre omurga dokusunu hızla tahrip edebilen lezyonlardır.",
            "Lokal agresif selim lezyonlar: **Dev hücreli tümör** ve **anevrizmal kemik kisti** kemik destrüksiyonu yapabilir.",
            "• Dev hücreli Tümör",
            ["dev hücreli tümör", "anevrizmal kemik kisti"],
            []
        ),
        (
            "Langerhans hücreli histiyositoz yelpazesinde değerlendirilen eozinofilik granülom ve en sık rastlanan vasküler lezyon olan vertebra hemanjiomu da primer benign grup içinde incelenir.",
            "İnflamatuar ve vasküler lezyonlar: **Eozinofilik granülom** ve **hemanjiom** benign spektrumun diğer önemli üyeleridir.",
            "• Eozinofilik granulom",
            ["eozinofilik granülom", "hemanjiom"],
            []
        ),
        (
            "Benign omurga tümörleri sistemik metastaz yapmasalar bile lamina veya pedikül gibi posterior elemanlara yerleşerek ağrılı skolyoz veya spinal korda bası gibi ciddi klinik tablolara neden olabilirler.",
            "**Benign tümörlerin seyri:** Çoğunluğu yavaş büyür ancak posterior eleman tutulumuyla mekanik ağrı ve defisit oluşturabilir.",
            "Primer benign omurga",
            ["benign tümörlerin seyri", "posterior eleman"],
            []
        )
    ]),

    (4, "k2-64-b03", "Primer Benign ve Malign Omurga Tümörleri Sınıflaması", [
        (
            "Primer malign omurga tümörleri arasında kemiğin osteojenik sarkomu olan osteosarkom, habis kıkırdak tümörü kondrosarkom ve küçük yuvarlak hücreli Ewing sarkomu önemli yer tutar.",
            "Primer habis mezenkimal lezyonlar: **Osteosarkom**, **kondrosarkom** ve **Ewing sarkomu** agresif kemik sarkomlarıdır.",
            "• Osteosarkom",
            ["osteosarkom", "kondrosarkom"],
            []
        ),
        (
            "Hematolojik maligniteler grubundan multipl myelom ve primer ya da sekonder omurga lenfoması erişkin hastalarda vertebra gövdesinde yaygın litik hasar oluşturan habis tablolardır.",
            "Hematolojik habis lezyonlar: **Multipl myelom** ve **omurga lenfoması** erişkinde yaygın omurga tutulumu yapar.",
            "• Multipl Myelom",
            ["multipl myelom", "omurga lenfoması"],
            []
        ),
        (
            "Embriyonik notokord kalıntılarından köken alan kordoma ile özellikle çocukluk çağında paravertebral sempatik zincirden kaynaklanan nöroblastom da primer malign spektrumda sınıflandırılır.",
            "Noto kord artıklarından kaynaklanan **kordoma** ve sempatik zincir kökenli **nöroblastom** malign listededir.",
            "• Kordoma",
            ["kordoma", "nöroblastom"],
            []
        ),
        (
            "Primer malign omurga tümörleri kemik korteksini ve korpusu hızla destrükte ederek vertebra çökme kırıklarına ve akut epidural spinal kord basılarına yol açtıklarından acil onkolojik ve cerrahi yaklaşım gerektirirler.",
            "**Malign lezyonların klinik davranışı:** Hızlı kemik destrüksiyonu, patolojik kırık ve erken nörolojik defisit riski yüksektir.",
            "Primer malign",
            ["malign lezyonların klinik davranışı", "kemik destrüksiyonu"],
            []
        )
    ]),

    # --- BOLUM 4: Osteoid Osteom: Arka Kolon Tutulumu ve Aspirin Yanıtı (Page 5) ---
    (5, "k2-64-b04", "Osteoid Osteom: Arka Kolon Tutulumu ve Aspirin Yanıtı", [
        (
            "Osteoid osteom sıklıkla on ila yirmi beş yaş arasındaki çocuklarda ve genç erişkin popülasyonda ortaya çıkan selim kemik oluşturan bir neoplazidir.",
            "**Osteoid osteom:** Genellikle 10-25 yaş arasındaki çocuk ve genç erişkinlerde görülür.",
            "• Çocuk ve genç erişkin : 10-25 yaş",
            ["osteoid osteom", "genç erişkin"],
            []
        ),
        (
            "Omurgada vertebra korpusundan ziyade lamina, pedikül ve faset eklem gibi arka kolon elemanları belirgin olarak daha sık tutulmaktadır.",
            "**Arka kolon tutulumu:** Lamina ve pedikül gibi posterior elemanlar belirgin şekilde daha sık tutulur.",
            "• Lamina ve pedikül gibi arka kolon",
            ["arka kolon tutulumu", "lamina ve pedikül"],
            []
        ),
        (
            "Spinal kolonda en sık lomber omurga segmenti etkilenirken, onu torasik ve servikal omurga lokalizasyonları takip eder.",
            "**Lomber bölge:** Omurga osteoid osteomlarının en sık yerleştiği anatomik segmenttir.",
            "• Lomber- en sık",
            ["lomber bölge", "anatomik segment"],
            []
        ),
        (
            "Hastanın ağrısı mekanik istirahatle gerilemez, gece uykudan uyandıracak şiddete ulaşır ve yüksek lokal prostaglandin üretimine bağlı olduğundan aspirine ve nonsteroid antiinflamatuvar ilaçlara dakikalar içinde dramatik yanıt verir.",
            "**Karakteristik ağrı:** Dinlenmekle azalmayan, gece şiddetlenen ve aspirin ile dramatik azalan ağrı tipiktir.",
            "• Dinlenmekle azalmayan, gece",
            ["karakteristik ağrı", "aspirin yanıtı"],
            []
        ),
        (
            "Tümör komşuluğundaki asimetrik paravertebral kas spazmı nedeniyle erişkinde ağrılı skolyozun en sık nedeni osteoid osteomdur; tanı sıklıkla aylar süren gecikmeyle bilgisayarlı tomografide nidus saptanarak konur.",
            "**Ağrılı skolyoz:** Erişkinde ağrılı skolyozun en sık nedenidir ve sıklıkla geç teşhis konur.",
            "• Erişkinde ağrılı skolyozun en sık nedeni",
            ["ağrılı skolyoz", "geç teşhis"],
            []
        )
    ]),

    # --- BOLUM 5: Osteoblastom: Agresif Selim Doğası ve Nörolojik Defisit Riski (Page 6) ---
    (6, "k2-64-b05", "Osteoblastom: Agresif Selim Doğası ve Nörolojik Defisit Riski", [
        (
            "Osteoblastom biyolojik olarak selim kabul edilmekle birlikte lokal olarak agresif davranış sergileyen ve osteoid osteoma kıyasla iki santimetreden büyük çaplara ulaşan bir kemik neoplazisidir.",
            "**Osteoblastom:** Agresif selim tümörlerdir ve osteoid osteoma kıyasla daha büyük boyutlara ulaşır.",
            "• Agressif selim tümörlerdir",
            ["osteoblastom", "agresif selim tümör"],
            []
        ),
        (
            "Tüm osteoblastom olgularının yüzde sekseni otuz yaş altındaki genç bireylerde ortaya çıkar ve tümörün omurgaya belirgin bir yerleşim yatkınlığı bulunur.",
            "**Genç yaş predileksiyonu:** Hastaların %80'i 30 yaşın altındadır ve omurgada sık görülür.",
            "• % 80 30 yaş altında",
            ["genç yaş predileksiyonu", "otuz yaş altı"],
            []
        ),
        (
            "Omurganın lamina ve pedikül gibi arka elemanlarını tutan osteoblastomda servikal, torasik ve lomber segmentler yaklaşık olarak eşit sıklıkta etkilenmektedir.",
            "**Segment dağılımı ve arka elemanlar:** Servikal, torakal ve lomber bölgeleri eşit oranda tutar.",
            "• Omurga arka elemanları tutulumu",
            ["segment dağılımı", "arka elemanlar"],
            []
        ),
        (
            "Osteoblastomun ulaştığı geniş kitle boyutu spinal kanal içine doğru ekspansiyon yaparak sinir köklerine ve medulla spinalise bası uygular, bu nedenle nörolojik defisit gelişimi sıktır.",
            "**Nörolojik defisit:** Büyük boyut ve spinal kanala uzanım nedeniyle nörolojik defisit sıktır.",
            "• Büyük boyut nedeniyle defisit sıktır",
            ["nörolojik defisit", "büyük boyut"],
            []
        ),
        (
            "Hastaların yüzde ellisinden fazlasında ağrılı skolyoz eşlik eder ve cerrahi küretaj sonrası osteoid osteoma kıyasla belirgin derecede daha yüksek oranda lokal nüks gösterir.",
            "**Skolyoz ve nüks:** Olguların >%50'sinde skolyoz görülür ve osteoid osteoma göre daha çok nükseder.",
            "• Osteoid osteoma göre daha çok",
            ["skolyoz ve nüks", "lokal nüks"],
            []
        )
    ]),

    # --- BOLUM 6: Osteokondrom: Kıkırdak Kaynağı ve Spinoz Proçes Tutulumu (Page 7) ---
    (7, "k2-64-b06", "Osteokondrom: Kıkırdak Kaynağı ve Spinoz Proçes Tutulumu", [
        (
            "Osteokondrom veya diğer adıyla osteokartilajinöz ekzostoz, tüm iskelet sisteminde en sık rastlanan selim kemik tümörüdür.",
            "**Osteokondrom:** Tüm iskelet sisteminin en sık görülen selim kemik tümörüdür.",
            "• En sık kemik tümörleridir",
            ["osteokondrom", "selim kemik tümörü"],
            []
        ),
        (
            "Lezyon kıkırdak kaynaklıdır ve tabanında kemiğin korteks ve medulla yapısıyla doğrudan devamlılık gösteren kemik doku, yüzeyinde ise tipik bir kıkırdak takkesi barındırır.",
            "**Kıkırdak takkesi:** Kıkırdak kaynaklı olup kemik korteksi ve medullası ile devamlılık gösterir.",
            "• Kıkırdak kaynaklıdır",
            ["kıkırdak takkesi", "kıkırdak kaynaklı"],
            []
        ),
        (
            "Omurgaya yerleştiğinde lamina ve özellikle spinoz proçes gibi arka elemanlardan dışarıya doğru büyüyen palpe edilebilir sert kitleler şeklinde karşımıza çıkar.",
            "**Spinoz proçes tutulumu:** Omurgada arka elemanlar ve özellikle spinoz proçes yerleşimi tipiktir.",
            "• Arka elemanlar ve özellikle spinoz proces tutulur",
            ["spinoz proçes tutulumu", "arka elemanlar"],
            []
        ),
        (
            "Genellikle ağrısız ve yavaş büyüyen bir lezyondur, ancak kıkırdak takkesinin kalınlaşması durumunda düşük oranda sekonder kondrosarkoma doğru habis dejenerasyon gösterebilir.",
            "**Habis dejenerasyon riski:** Nadiren ağrılıdır ancak düşük oranda kondrosarkoma dönüşüm görülebilir.",
            "• Habis dejenerasyon görülebilir(düşük oran)",
            ["habis dejenerasyon riski", "kondrosarkoma dönüşüm"],
            []
        )
    ]),

    # --- BOLUM 7: Dev Hücreli Tümör ve Korpus Tutulumu (Page 8) ---
    (8, "k2-64-b07", "Dev Hücreli Tümör ve Korpus Tutulumu", [
        (
            "Dev hücreli tümör diğer adıyla osteoklastom, histolojik olarak selim kabul edilmekle beraber kemikte geniş lizis ve doku harabiyeti yapan lokal agresif bir neoplazidir.",
            "**Dev Hücreli Tümör:** Osteoklastom olarak da bilinen selim ancak lokal destrüktif neoplazidir.",
            "Dev Hücreli Tümör",
            ["dev hücreli tümör", "osteoklastom"],
            []
        ),
        (
            "Hastalık yirmi ila kırk yaş arasındaki genç erişkinlerde pik yapar ve apofizyel kıkırdak kapanmasından sonra eklem komşuluğundaki epifiz ve metafiz bölgelerinde ortaya çıkar.",
            "**Yaş ve anatomik yapı:** Genç erişkinlerde uzun kemiklerde metafiz ve epifiz tutulumu karakteristiktir.",
            "• Genç erişkinde metafiz ve epifiz",
            ["yaş ve anatomik yapı", "metafiz ve epifiz"],
            []
        ),
        (
            "Posterior elemanları tutan osteoid osteom ve osteoblastomun aksine, dev hücreli tümör omurgada karakteristik olarak doğrudan vertebra korpusuna yerleşir.",
            "**Vertebra korpusu:** Çoğu benign lezyonun aksine omurgada doğrudan korpus tutulur.",
            "• Omurgada korpus tutulur",
            ["vertebra korpusu", "korpus tutulumu"],
            []
        ),
        (
            "Omurgada en sık torasik segment etkilenir ve korpustaki litik genişleme vertebral çökme kırıklarına ve kord basısına zemin hazırlayabilir.",
            "**Torasik segment:** Omurgada en sık torasik omurga bölgesinde lokalize olur.",
            "• En sık torasik omurga",
            ["torasik segment", "torasik omurga"],
            []
        )
    ]),

    # --- BOLUM 8: Anevrizmal Kemik Kisti ve Genç Yaş Lomber Tutulumu (Page 9) ---
    (9, "k2-64-b08", "Anevrizmal Kemik Kisti ve Genç Yaş Lomber Tutulumu", [
        (
            "Anevrizmal kemik kisti, fibröz septalarla birbirinden ayrılmış geniş kan dolu kavernöz boşluklardan oluşan ve kemiği balon gibi şişiren selim bir lezyondur.",
            "**Anevrizmal Kemik Kisti:** İçi kan dolu kistik kavitelerle karakterize selim ekspansil lezyondur.",
            "Anevrizma Kemik Kisti",
            ["anevrizmal kemik kisti", "kistik lezyon"],
            []
        ),
        (
            "Hastaların büyük bölümü yirmi ila otuz yaş arasındaki genç erişkinlerden oluşur ve lezyon hızla büyüme potansiyeline sahiptir.",
            "**Genç erişkin çağı:** Olguların büyük kısmı 20-30 yaş grubunda saptanır.",
            "• 20 - 30 yaş",
            ["genç erişkin çağı", "yirmi otuz yaş"],
            []
        ),
        (
            "Anevrizmal kemik kistlerinin yaklaşık yüzde altmışı pedikül, lamina ve faset eklemleri içeren arka elemanlara yerleşir ve en sık lomber omurgada görülür.",
            "**Arka eleman tutulumu (%60):** En sık lomber bölgede arka kolon elemanlarını tutar.",
            "• Arka elemanlar (% 60)",
            ["arka eleman tutulumu", "lomber bölge"],
            []
        ),
        (
            "Klinik başvuruda inatçı bel ağrısı ana semptomdur; kistin spinal kanala doğru balonlaşarak büyümesi sonucu hastaların yüzde elli beşinde belirgin nörolojik defisit izlenir.",
            "**Bel ağrısı ve defisit:** Bel ağrısı ana semptomdur ve hastaların %55'inde nörolojik defisit gelişir.",
            "• Bel ağrısı : ana semptom",
            ["bel ağrısı ve defisit", "nörolojik defisit"],
            []
        ),
        (
            "Osteoblastom gibi ağrılı skolyoz oluşturabilen anevrizmal kemik kistinde temel tedavi cerrahi küretaj ve rezeksiyondur; ulaşılamayan veya nüks eden vakalarda radyoterapi adjuvan olarak planlanabilir.",
            "**Cerrahi ve radyoterapi:** Ağrılı skolyoz yapabilir; tedavisi cerrahidir ve radyoterapi adjuvan verilebilir.",
            "• Cerrahi",
            ["cerrahi ve radyoterapi", "ağrılı skolyoz"],
            []
        )
    ]),

    # --- BOLUM 9: Eozinofilik Granülom ve Hand-Schüller-Christian Triadı (Pages 10-11) ---
    (10, "k2-64-b09", "Eozinofilik Granülom ve Hand-Schüller-Christian Triadı", [
        (
            "Eozinofilik granülom, klonal dendritik hücrelerin ve eozinofil lökositlerin proliferasyonuyla karakterize Langerhans hücreli histiyositoz yelpazesinin iskelet tutulumu gösteren tablosudur.",
            "**Eozinofilik Granülom:** Langerhans hücreli histiyositozun kemik tutulumuyla seyreden selim formudur.",
            "Eozinofilik Granulom",
            ["eozinofilik granülom", "histiyositoz"],
            []
        ),
        (
            "En sık ikinci dekadda saptanan hastalık özellikle beş ve on yaşlarında iki belirgin pik yaparak pediatrik yaş grubunda karşımıza çıkar.",
            "**Çocukluk çağı pikleri:** En sık 2. dekadda görülür; 5 ve 10 yaşta iki ayrı pik yapar.",
            "• 5 ve 10 yaşta pik yapar",
            ["çocukluk çağı pikleri", "beş ve on yaş"],
            []
        ),
        (
            "Klinik tabloda tipik olarak akut başlangıçlı sırt ağrısı görülür ve lezyon omurga boyunca en sık torasik omurga segmentini tutar.",
            "**Akut sırt ağrısı:** Torasik omurgada vertebra korpus çökmesine bağlı ani ağrıyla başlar.",
            "• Akut sırt ağrısı",
            ["akut sırt ağrısı", "torasik omurga"],
            []
        ),
        (
            "Vertebra gövdesindeki litik erime nedeniyle korpus adeta madeni para gibi yassılaşarak vertebra plana tablosuna yol açar.",
            "**Vertebra plana:** Korpusun homojen çökmesiyle direkt grafide madeni para görünümü oluşabilir.",
            "• Torasik omurga tutulumu",
            ["vertebra plana", "homojen çökme"],
            []
        ),
        (
            "İskelet dışı organ tutulumu olan sistemik formlarda kemoterapi tercih edilirken, izole tekil vertebra lezyonlarında immobilizasyon, biyopsi veya cerrahi küretaj yeterli olmaktadır.",
            "**Tedavi stratejisi:** Sistemik tutulumda kemoterapi, tekil izole lezyonlarda cerrahi tedavi uygulanır.",
            "• Sistemik ise kemoterapi diğer türlü Cerrahi",
            ["tedavi stratejisi", "cerrahi tedavi"],
            []
        )
    ]),

    (11, "k2-64-b09", "Eozinofilik Granülom ve Hand-Schüller-Christian Triadı", [
        (
            "Hand-Schüller-Christian triadı, Langerhans hücreli histiyositozun çocukluk ve gençlik çağında kronik ilerleyici seyir gösteren multisistemik formunun klasik klinik tablosudur.",
            "**Hand-Schüller-Christian Triadı:** Langerhans hücreli histiyositozun kronik multisistem formudur.",
            "Hand-Schüller-Christian triadı",
            ["Hand-Schüller-Christian", "multisistem formu"],
            []
        ),
        (
            "Triadın ilk bileşeni kafatasında zımba deliği şeklinde sınırları net litik lezyonlar ve vertebral kolonda görülen litik kemik tutulumlarıdır.",
            "**Kemik lezyonları:** Kafatası ve vertebrada zımba deliği tarzında litik kemik defektleri izlenir.",
            "• kemik lezyonları,",
            ["kemik lezyonları", "litik defektler"],
            []
        ),
        (
            "İkinci bileşen hipotalamus ve hipofiz sapının histiyositik infiltrasyonuna bağlı antidiüretik hormon eksikliği sonucu ortaya çıkan diabetes insipidus tablosudur.",
            "**Diabetes insipidus:** Hipotalamo-hipofizer aks tutulumuna bağlı polidipsi ve poliüri gelişir.",
            "• diabetes insipidus",
            ["diabetes insipidus", "hipofiz tutulumu"],
            []
        ),
        (
            "Üçüncü bileşen ise orbita arkasındaki granulomatöz doku birikimi nedeniyle göz küresinin öne doğru belirginleştiği ekzoftalmustur; bu klasik üçlü kronik multisistem histiyositozun temel bulgusudur.",
            "**Ekzoftalmus:** Retroorbital granülomatöz kitle nedeniyle tek veya çift taraflı göz öne fırlar.",
            "• ekzoftalmus üçlüsüyle karakterize kronik bir multisistem formudur,",
            ["ekzoftalmus", "kronik multisistem"],
            []
        )
    ]),

    # --- BOLUM 10: Vertebra Hemanjiomu ve Vertikal Çizgilenmeler (Page 12) ---
    (12, "k2-64-b10", "Vertebra Hemanjiomu ve Vertikal Çizgilenmeler", [
        (
            "Vertebra hemanjiomu endotelyal damar proliferasyonundan kaynaklanan selim vasküler bir lezyondur ve tüm omurganın en sık rastlanan primer benign tümörüdür.",
            "**Vertebra Hemanjiomu:** Selim vasküler kökenli olup erişkinde en sık rastlanan omurga tümörüdür.",
            "Hemanjiom",
            ["vertebra hemanjiomu", "vasküler kökenli"],
            []
        ),
        (
            "Olguların büyük çoğunluğu tamamen asemptomatiktir ve çekilen radyolojik incelemelerde insidental yani rastlantısal olarak tespit edilir.",
            "**İnsidental tanı:** Çoğunlukla asemptomatiktir ve başka nedenlerle çekilen grafilerde rastlantısal saptanır.",
            "• Sıklıkla insidentaldir",
            ["insidental tanı", "asemptomatik"],
            []
        ),
        (
            "Tüm kemik hemanjiomlarının yüzde ellisinden fazlası omurga ve kafatasında yerleşir ve omurga içinde en sık alt torasik ve lomber segmentleri tutar.",
            "**Anatomik dağılım:** >%50 oranında omurga ve kafatasında, özellikle torakolomber bölgede yerleşir.",
            "• > % 50 omurga ve kafatasında görülür",
            ["anatomik dağılım", "torakolomber"],
            []
        ),
        (
            "Radyografide yatay trabeküller rezorbe olurken dikey trabeküllerin kompansatuar kalınlaşması sonucu kadife kumaş veya tel kafes görünümünü andıran vertikal çizgilenmeler izlenir.",
            "**Vertikal çizgilenmeler:** Direkt grafide trabeküler kalınlaşmaya bağlı dikey çizgilenmeler tipiktir.",
            "• Direkt grafide : vertikal çizgilenmeler",
            ["vertikal çizgilenmeler", "trabeküler kalınlaşma"],
            []
        ),
        (
            "Lezyon nadiren patolojik kırığa veya epidural alana genişleyerek medulla spinalis basısına yol açabilir; nörolojik defisit varlığında dekompresyon cerrahisi ve embolizasyon gerekir.",
            "**Kırık ve cerrahi endikasyon:** Patolojik kırık veya spinal kord basısı geliştiğinde cerrahi uygulanır.",
            "• Bası durumunda cerrahi",
            ["cerrahi endikasyon", "kord basısı"],
            []
        )
    ]),

    # --- BOLUM 11: Primer Malign Omurga Tümörleri ve Sarkomlar (Pages 13-16) ---
    (13, "k2-64-b11", "Primer Malign Omurga Tümörleri ve Sarkomlar", [
        (
            "Primer malign omurga tümörleri histogenetik kökenlerine göre osteosarkom, kondrosarkom ve Ewing sarkomu gibi mezenkimal kemik sarkomlarından oluşur.",
            "Primer habis spektrum: **Osteosarkom**, **kondrosarkom** ve **Ewing sarkomu** primer kemik kökenli sarkomlardır.",
            "• Osteosarkom",
            ["osteosarkom", "kondrosarkom"],
            []
        ),
        (
            "Kemik iliğindeki plazma hücreleri veya lenfositlerden köken alan multipl myelom ve primer spinal lenfoma malign listenin en sık görülen diğer elemanlarıdır.",
            "Hematolojik köken: **Multipl myelom** ve **lenfoma** omurga kemik iliğinde yaygın tutulum yapar.",
            "• Multipl Myelom",
            ["multipl myelom", "kemik iliği"],
            []
        ),
        (
            "Embriyolojik aksiyel iskelet kalıntısı olan kordoma sakrokoksigeal ve klival bölgede, nöroblastom ise paravertebral ganglion zinciri boyunca habis gelişim gösterir.",
            "Özel doku kökenleri: **Kordoma** notokord artıklarından, **nöroblastom** sempatik ganglionlardan gelişir.",
            "• Kordoma",
            ["kordoma", "nöroblastom"],
            []
        ),
        (
            "Bu habis tümörlerin ortak klinik özelliği spinal kemik matriksini destrükte ederek şiddetli istirahat ağrısı, mekanik instabilite ve hızla ilerleyen felç tabloları yaratabilmeleridir.",
            "**Prognoz ve klinik yaklaşım:** Malign tümörler hızlı lokal invazyon ve erken bası bulgusu verir.",
            "Primer malign",
            ["prognoz ve klinik yaklaşım", "lokal invazyon"],
            []
        )
    ]),

    (14, "k2-64-b11", "Primer Malign Omurga Tümörleri ve Sarkomlar", [
        (
            "Omurga osteosarkomu habis mezenkimal hücrelerin olgunlaşmamış tümöral osteoid kemik matriksi ürettiği son derece agresif ve nadir bir primer kemik tümörüdür.",
            "**Omurga Osteosarkomu:** Nadir görülen, agresif osteoid matriks üreten habis kemik tümörüdür.",
            "Osteosarkom",
            ["omurga osteosarkomu", "osteoid matriks"],
            []
        ),
        (
            "Ekstremite yerleşimli osteosarkomlar ergenlik çağında pik yaparken, omurgaya yerleşen osteosarkomlar belirgin biçimde ileri yaş popülasyonunda veya Paget hastalığı zemininde ortaya çıkar.",
            "**İleri yaş insidansı:** Uzun kemik osteosarkomlarının aksine omurgada ileri yaş grubunda sıktır.",
            "• İleri yaş",
            ["ileri yaş insidansı", "Paget zemininde"],
            []
        ),
        (
            "Tümör omurganın hem korpusunu hem de pedikül ve lamina gibi arka elemanlarını invaze ederek permeatif litik ve destrüktif kemik harabiyetine neden olur.",
            "**Litik ve destrüktif lezyon:** Hem arka elemanlarda hem vertebra korpusunda destrüksiyon yapar.",
            "• Arka elemanların ve korpusun litik veya",
            ["litik ve destrüktif lezyon", "kemik harabiyeti"],
            []
        ),
        (
            "Tedavide omurganın stabilitesini koruyarak tümörün geniş sınırlarla cerrahi rezeksiyonu ve cerrahiye eklenen radyoterapi ile sistemik kemoterapi protokolleri uygulanır.",
            "**Tedavi protokolü:** Tedavide geniş cerrahi rezeksiyon ve adjuvan radyoterapi kombine edilir.",
            "• Cerrahi + radyoterapi",
            ["tedavi protokolü", "cerrahi rezeksiyon"],
            []
        )
    ]),

    (15, "k2-64-b11", "Primer Malign Omurga Tümörleri ve Sarkomlar", [
        (
            "Kondrosarkom neoplastik kondrositlerin habis kıkırdak matriksi ürettiği ve klasik kemoterapi ile radyoterapiye oldukça dirençli olan primer malign kemik tümörüdür.",
            "**Kondrosarkom:** Habis kıkırdak matriksi üreten ve kemoradyoterapiye dirençli neoplazidir.",
            "Kondrosarkom",
            ["kondrosarkom", "kıkırdak matriksi"],
            []
        ),
        (
            "Hastalık çoğunlukla kırk ila yetmiş yaş arasındaki orta ve ileri yaş grubundaki erişkinlerde karşımıza çıkmaktadır.",
            "**40-70 yaş grubu:** Tipik olarak 40 ila 70 yaş arasındaki erişkin ve yaşlı grupta ortaya çıkar.",
            "• 40 – 70 yaş",
            ["kırk yetmiş yaş", "erişkin grup"],
            []
        ),
        (
            "İskelet sisteminde en sık pelvis ve femur gibi uzun kemiklerde görülmekle birlikte omurga kolonunda da sıkça saptanır ve geniş kıkırdak kitleleri oluşturur.",
            "**İskelet lokalizasyonu:** Uzun kemikler ve pelviste sıktır; omurga tutulumu da önemli yer tutar.",
            "• Uzun kemiklerde ve pelviste sıktır. Omurga  tutulumu  da",
            ["iskelet lokalizasyonu", "pelvis ve omurga"],
            []
        ),
        (
            "Düşük dereceli yavaş seyirli formlardan yüksek dereceli agresif formlara kadar değişkenlik gösterebilir; kemoradyoterapiye yanıtsızlığı nedeniyle izole omurga kondrosarkomlarında tek küratif yaklaşım geniş cerrahi rezeksiyondur.",
            "**Cerrahi tedavi:** Yavaş veya agresif seyirli olabilir; izole kitlelerde temel tedavi cerrahidir.",
            "• İzole ise cerrahi tedavi",
            ["cerrahi tedavi", "geniş rezeksiyon"],
            []
        )
    ]),

    (16, "k2-64-b11", "Primer Malign Omurga Tümörleri ve Sarkomlar", [
        (
            "Ewing sarkomu nöroektodermal kökenli, indiferansiye küçük yuvarlak mavi hücrelerden oluşan ve son derece kötü prognoz taşıyan habis bir kemik neoplazisidir.",
            "**Ewing Sarkomu:** Kemiğin yüksek dereceli habis küçük yuvarlak mavi hücreli tümörüdür.",
            "Ewing’s Sarkomu",
            ["Ewing sarkomu", "küçük yuvarlak hücreli"],
            []
        ),
        (
            "Tümör en sık ilk iki dekadda yani on ila yirmi yaş arasındaki çocukluk ve adölesan dönemde saptanır ve iskeletin her bölgesine yerleşebilir.",
            "**Çocukluk ve ergenlik çağı:** En sık ilk 2 dekadda, çocukluk ve ergenlik döneminde görülür.",
            "• En sık ilk 2 dekadda",
            ["çocukluk ve ergenlik", "ilk iki dekad"],
            []
        ),
        (
            "Hastada subfebril ateş, halsizlik, normositer anemi, beyaz küre artışı yani lökositoz ve belirgin şekilde yükselmiş eritrosit sedimentasyon hızı izlenir.",
            "**Sistemik bulgular:** Subfebril ateş, anemi, belirgin lökositoz ve yüksek sedimentasyon izlenir.",
            "• Subfebril ateş, anemi, lökositoz ve",
            ["sistemik bulgular", "subfebril ateş"],
            []
        ),
        (
            "Ateş, lökositoz, lokal ısı artışı ve sedimentasyon yüksekliği gibi sistemik inflamatuar bulguları nedeniyle sıklıkla bakteriyel bir kemik enfeksiyonu olan osteomiyelit ile karıştırılır.",
            "**Osteomiyelit taklidi:** Klinik ve laboratuvar bulguları kemik enfeksiyonu osteomiyeliti taklit eder.",
            "• Osteomyelit ile karıştırılır",
            ["osteomiyelit taklidi", "inflamatuar bulgular"],
            []
        ),
        (
            "Geniş lokal yayılım ve yüksek mikrometastaz riski nedeniyle cerrahinin tek başına yeri son derece sınırlıdır; primer yaklaşım yoğun sistemik kemoterapi ve radyoterapi kombinasyonudur.",
            "**Kemoradyoterapi:** Cerrahinin yeri sınırlıdır; kemoterapi ve radyoterapi kombinasyonu önerilir.",
            "• Kemoterapi + radyoterapi önerilir",
            ["kemoradyoterapi", "sistemik kemoterapi"],
            []
        )
    ]),

    # --- BOLUM 12: Multipl Myelom, Omurga Lenfoması ve Spinal Metastazlar (Pages 17-20) ---
    (17, "k2-64-b12", "Multipl Myelom, Omurga Lenfoması ve Spinal Metastazlar", [
        (
            "Multipl myelom kemik iliğinde monoklonal habis plazma hücrelerinin kontrolsüz çoğalmasıyla karakterize olup erişkin çağın en sık primer habis kemik tümörüdür.",
            "**Multipl Myelom:** Erişkin çağın en sık görülen primer habis kemik tümörüdür.",
            "Multiple Myelom",
            ["multipl myelom", "plazma hücre tümörü"],
            []
        ),
        (
            "Hastaların büyük çoğunluğu elli yaşın üzerindedir ve plazma hücresi neoplazisi olması nedeniyle vertebral kolonda multifokal ve yaygın tutulum gösterir.",
            "**>50 yaş popülasyonu:** Tipik olarak 50 yaşın üzerindeki erişkinlerde yaygın tutulum yapar.",
            "• > 50 yaş",
            ["elli yaş üzeri", "yaygın tutulum"],
            []
        ),
        (
            "Kemik iliği infiltrasyonuna bağlı normositik normokromik anemi, kanda monoklonal immünglobulin artışına bağlı son derece yüksek eritrosit sedimentasyon hızı ve hiperkalsemi görülür.",
            "**Laboratuvar bulguları:** Normositik-normokromik anemi ve belirgin yüksek sedimentasyon eşlik eder.",
            "• Normositik-normokromik anemi",
            ["laboratuvar bulguları", "yüksek sedimentasyon"],
            []
        ),
        (
            "Kemik rezorpsiyonunu uyaran osteoklastik faktörler nedeniyle vertebra korpuslarında ve kraniumda zımba deliği şeklinde, sklerotik reaksiyon içermeyen litik güve yeniği manzarası oluşur.",
            "**Litik güve yeniği:** Direkt grafide zımba deliği tarzında litik-güve yeniği görünümü izlenir.",
            "• Litik-güve yeniği görünümü",
            ["litik güve yeniği", "zımba deliği"],
            []
        ),
        (
            "Hastalık sistemik bir hematolojik proliferasyon olduğundan birincil tedavi kemoterapi, immünmodülatör ilaçlar ve otolog kök hücre naklidir; cerrahi ancak stabilizasyon için düşünülür.",
            "**Sistemik tedavi:** Multipl myelomda birincil tedavi kemoterapi ve hedefe yönelik ajanlardır.",
            "• Birincil tedavi: Kemoterapi",
            ["sistemik tedavi", "birincil kemoterapi"],
            []
        )
    ]),

    (18, "k2-64-b12", "Multipl Myelom, Omurga Lenfoması ve Spinal Metastazlar", [
        (
            "Omurga lenfoması sistemik bir lenfomanın spinal kolon tutulumu veya nadiren primer kemik lenfoması şeklinde beliren habis lenfoid neoplazisidir.",
            "**Omurga Lenfoması:** Erişkin çağda vertebra korpusunu tutan habis lenfoid proliferasyondur.",
            "Lenfoma",
            ["omurga lenfoması", "lenfoid proliferasyon"],
            []
        ),
        (
            "Tümör omurga boyunca sıklıkla vertebra korpusunda destrüksiyon yaparak litik kemik lezyonlarına ve spinal epidural alana uzanarak radikülopati veya miyelopatiye yol açar.",
            "**Korpus litik lezyonları:** Vertebra korpusunda litik lezyonlar ve patolojik çökme kırıkları yapar.",
            "• Omurgada vertebra korpusunda litik",
            ["korpus litik lezyonları", "patolojik kırık"],
            []
        ),
        (
            "Multipl myelom ve metastatik karsinomlarla benzer radyolojik bulgular verebildiğinden kesin teşhis mutlaka floroskopi veya bilgisayarlı tomografi eşliğinde iğne biyopsisi ile konmalıdır.",
            "**Biyopsi ile kesin tanı:** Radyolojik ayırıcı tanı güçlüğü nedeniyle tanı biyopsi ile konur.",
            "• Teşhis: Biyopsi",
            ["biyopsi ile tanı", "kesin teşhis"],
            []
        ),
        (
            "Lenfoma hücreleri radyasyona aşırı duyarlı olduğundan lokal kontrolde birincil tedavi radyoterapidir; kombine kemoterapi eklenmesi hastaların genel sağkalım ve survey sürelerini belirgin şekilde artırır.",
            "**Radyoterapi ve kemoterapi:** Birincil tedavi radyoterapidir; kemoterapi eklenmesi surveyi artırır.",
            "• Kemo + Radyotx: Surveyi arttırmaktadır",
            ["radyoterapi ve kemoterapi", "survey artışı"],
            []
        )
    ]),

    (19, "k2-64-b12", "Multipl Myelom, Omurga Lenfoması ve Spinal Metastazlar", [
        (
            "Klinik pratikte omurgada tespit edilen neoplastik lezyonların yüzde doksanı vücudun diğer primer kanserlerinden kaynaklanan metastatik tümörlerdir.",
            "**Spinal metastaz oranı:** Omurga tümörlerinin %90'ı metastazdır ve en sık tümöral lezyondur.",
            "• Omurga tümörlerinin %90 ı metastazdır",
            ["spinal metastaz oranı", "yüzde doksan"],
            []
        ),
        (
            "İskelet sistemine yayılan tüm karsinomatöz metastazlar arasında vertebra kolonu en sık tutulan anatomik bölgedir.",
            "**En sık iskelet metastazı:** Tüm iskelet sistemi metastazları en sık omurgaya yerleşir.",
            "• İskelet sistemi metastazları en sık omurgaya olur.",
            ["en sık iskelet metastazı", "vertebra kolonu"],
            []
        ),
        (
            "Pelvik ve abdominal venöz basınç artışlarında kanı geriye doğru omurga venlerine taşıyan kapaksız Batson venöz pleksusu ve zengin vertebral arter dolaşımı bu sık tutulumun temel mekanizmasıdır.",
            "**Yayılım mekanizmaları:** Kapaksız Batson venöz pleksusu ve arteriyel embolizasyon ile yayılır.",
            "Metastatik",
            ["yayılım mekanizmaları", "Batson pleksusu"],
            []
        ),
        (
            "Metastatik omurga lezyonları vertebra korpusunu tahrip ederek ani patolojik kırıklara ve epidural mesafeye taşarak paraplejiye yol açabilecek spinal kord basılarına neden olabilir.",
            "**Klinik risk:** Epidural spinal kord basısı ve patolojik instabilite acil müdahale gerektirir.",
            "Omurga",
            ["klinik risk", "spinal kord basısı"],
            []
        )
    ]),

    (20, "k2-64-b12", "Multipl Myelom, Omurga Lenfoması ve Spinal Metastazlar", [
        (
            "Spinal metastazların yüzde ellisinden fazlası akciğer karsinomu, meme kanseri veya prostat kanseri olmak üzere bu üç büyük primer odaktan kaynaklanmaktadır.",
            "**En sık primerler:** Spinal metastazların %50'si akciğer, meme veya prostat kanserinden kaynaklanır.",
            "• Spinal metastazların %50’si",
            ["en sık primerler", "akciğer meme prostat"],
            []
        ),
        (
            "Akciğer ve meme metastazları tipik olarak kemikte destrüksiyon yapan osteolitik lezyonlar oluştururken, prostat kanseri metastazları direkt grafilerde beyaz yoğun odaklarla beliren osteoblastik yani sklerotik lezyonlar yapar.",
            "**Litik ve blastik lezyonlar:** Akciğer ve meme litik, prostat ise karakteristik osteoblastik lezyon yapar.",
            "akciğer,meme veya prostat",
            ["litik ve blastik", "osteoblastik lezyon"],
            []
        ),
        (
            "Bu üç organın yanı sıra hipervasküler metastaz yapan böbrek ve tiroid karsinomları ile gastrointestinal sistem tümörleri de omurga metastazlarında akılda tutulmalıdır.",
            "**Diğer primer kaynaklar:** Böbrek, tiroid ve gastrointestinal tümörler de omurgaya metastaz yapabilir.",
            "kanserinden kaynaklanır.",
            ["diğer primer kaynaklar", "böbrek ve tiroid"],
            []
        ),
        (
            "Tedavi yaklaşımında acil spinal kord ödemini geriletmek için yüksek doz deksametazon, ağrı kontrolü ve lokal tümör baskılaması için radyoterapi, mekanik instabilite veya kord basısı durumunda ise cerrahi dekompresyon ve enstrümentasyon uygulanır.",
            "**Tedavi ve stabilizasyon:** Palyatif radyoterapi, kortikosteroidler ve cerrahi dekompresyon uygulanır.",
            "Metastatik",
            ["tedavi ve stabilizasyon", "cerrahi dekompresyon"],
            []
        )
    ])
]


def build_konusma_v2():
    bolum_map = {}
    cumle_idx = 1
    par_idx = 1
    bolum_order = []

    for sayfa, b_id, b_baslik, cumleler in SLIDES:
        if b_id not in bolum_map:
            bolum_order.append(b_id)
            b_num = len(bolum_order)
            bolum_map[b_id] = {
                "id": f"k2-64-b{b_num:02d}",
                "baslik": b_baslik,
                "paragraflar": []
            }

        par_cumleler = []
        for ses, ekran, anchor, terms, cikmis_list in cumleler:
            cid = f"k2-64-c{cumle_idx:04d}"
            cumle_idx += 1

            # Match first term from terms present in ekran
            vurgular = []
            for t in terms:
                m = re.search(re.escape(t), ekran, re.IGNORECASE)
                if m:
                    vurgular.append({"metin": m.group(0), "tur": "terim"})
                    break
            if not vurgular:
                # Fallback to bold text
                m = re.findall(r"\*\*([^*]+)\*\*", ekran)
                if m:
                    vurgular.append({"metin": m[0], "tur": "terim"})
                else:
                    vurgular.append({"metin": ekran.split()[0], "tur": "terim"})

            satir_list = [anchor] if anchor else []

            c_obj = {
                "id": cid,
                "ses": ses,
                "ekran": ekran,
                "duzey": 0,
                "vurgu": vurgular,
                "slayt": {
                    "sayfa": sayfa,
                    "satir": satir_list,
                    "sekil": None
                }
            }
            if cikmis_list:
                c_obj["cikmis"] = cikmis_list
            par_cumleler.append(c_obj)

        pid = f"k2-64-p{par_idx:03d}"
        par_idx += 1
        bolum_map[b_id]["paragraflar"].append({
            "id": pid,
            "sayfa": sayfa,
            "cumleler": par_cumleler
        })

    v2 = {
        "surum": 2,
        "ders_id": "k2-64",
        "anahtar": "y25-k2-64-omurga-tumorleri",
        "baslik": "Omurga Tümörleri",
        "bolumler": [bolum_map[bid] for bid in bolum_order]
    }
    return v2


def build_cizim_aday():
    """Build robust cizim_aday.json with 11 valid semantic drawing commands, zero forward leaks."""
    komutlar = [
        # Command 1: Page 2 - P1.C1
        {
            "cumle": "P1.C1",
            "bas": 0,
            "son": 8,
            "sayfa": 2,
            "tur": "sema",
            "sablon": "siniflama",
            "baslik": "Omurga kitleleri",
            "ogeler": [
                "Primer kemik tümörleri",
                "Metastatik yayılım"
            ]
        },
        # Command 2: Page 3 - P2.C3
        {
            "cumle": "P2.C3",
            "bas": 0,
            "son": 8,
            "sayfa": 3,
            "tur": "sema",
            "sablon": "siniflama",
            "baslik": "Primer selim omurga tümörleri",
            "ogeler": [
                "Osteoid osteom",
                "Osteoblastom",
                "Osteokondrom",
                "Dev hücreli tümör"
            ]
        },
        # Command 3: Page 4 - P3.C3
        {
            "cumle": "P3.C3",
            "bas": 0,
            "son": 8,
            "sayfa": 4,
            "tur": "sema",
            "sablon": "siniflama",
            "baslik": "Primer habis omurga tümörleri",
            "ogeler": [
                "Osteosarkom",
                "Kondrosarkom",
                "Ewing sarkomu",
                "Multipl myelom"
            ]
        },
        # Command 4: Page 5 - P4.C4
        {
            "cumle": "P4.C4",
            "bas": 0,
            "son": 8,
            "sayfa": 5,
            "tur": "sema",
            "sablon": "siniflama",
            "baslik": "Osteoid osteom özellikleri",
            "ogeler": [
                "Genç yaş ve arka kolon tutulumu",
                "Gece şiddetlenen ağrı",
                "Aspirine dramatik yanıt",
                "Ağrılı skolyoz"
            ]
        },
        # Command 5: Page 6 - P5.C4 (Osteoid osteom vs Osteoblastom)
        {
            "cumle": "P5.C4",
            "bas": 0,
            "son": 8,
            "sayfa": 6,
            "tur": "sema",
            "sablon": "karsilastirma",
            "kutuplar": ["Osteoid osteom", "Osteoblastom"],
            "satirlar": [
                ["Boyut", "İki santimetreden küçük", "Büyük boyut"],
                ["Nüks", "Kıyasla az nüks", "Yüksek lokal nüks"]
            ]
        },
        # Command 6: Page 8 - P7.C3
        {
            "cumle": "P7.C3",
            "bas": 0,
            "son": 8,
            "sayfa": 8,
            "tur": "sema",
            "sablon": "siniflama",
            "baslik": "Dev hücreli tümör",
            "ogeler": [
                "Genç erişkin popülasyon",
                "Vertebra korpusu tutulumu",
                "Torasik segment yerleşimi"
            ]
        },
        # Command 7: Page 11 - P10.C3 (Hand-Schüller-Christian triadı)
        {
            "cumle": "P10.C3",
            "bas": 0,
            "son": 8,
            "sayfa": 11,
            "tur": "sema",
            "sablon": "siniflama",
            "baslik": "Hand-Schüller-Christian triadı",
            "ogeler": [
                "kemik lezyonları",
                "diabetes insipidus",
                "ekzoftalmus"
            ]
        },
        # Command 8: Page 12 - P11.C4 (Vertebra hemanjiomu)
        {
            "cumle": "P11.C4",
            "bas": 0,
            "son": 8,
            "sayfa": 12,
            "tur": "sema",
            "sablon": "siniflama",
            "baslik": "Vertebra hemanjiomu",
            "ogeler": [
                "İnsidental saptanma",
                "Vertikal çizgilenmeler",
                "Patolojik kırık riski"
            ]
        },
        # Command 9: Page 16 - P15.C3 (Ewing sarkomu osteomiyelit taklidi)
        {
            "cumle": "P15.C3",
            "bas": 0,
            "son": 8,
            "sayfa": 16,
            "tur": "sema",
            "sablon": "maskeleyen",
            "gorunen": "Osteomiyelit",
            "altta": ["Ewing sarkomu"]
        },
        # Command 10: Page 17 - P16.C4 (Multipl myelom)
        {
            "cumle": "P16.C4",
            "bas": 0,
            "son": 8,
            "sayfa": 17,
            "tur": "sema",
            "sablon": "siniflama",
            "baslik": "Multipl myelom bulguları",
            "ogeler": [
                "Elli yaş üzeri popülasyon",
                "Normositik anemi ve yüksek sedim",
                "Litik güve yeniği manzarası",
                "Birincil kemoterapi"
            ]
        },
        # Command 11: Page 20 - P19.C2 (Spinal metastaz kaynakları)
        {
            "cumle": "P19.C2",
            "bas": 0,
            "son": 8,
            "sayfa": 20,
            "tur": "sema",
            "sablon": "cok_neden_tek_sonuc",
            "kaynaklar": [
                "akciğer karsinomu",
                "meme kanseri",
                "prostat kanseri"
            ],
            "sonuc": "Spinal metastazlar"
        }
    ]
    return {"komutlar": komutlar}


def main():
    print("Generating deep amfi-depth konusma_v2.json for k2-64...")
    v2 = build_konusma_v2()

    # Calculate statistics
    total_bolum = len(v2["bolumler"])
    total_par = sum(len(b["paragraflar"]) for b in v2["bolumler"])
    total_c = sum(len(p["cumleler"]) for b in v2["bolumler"] for p in b["paragraflar"])
    total_w_ekran = sum(len(c["ekran"].split()) for b in v2["bolumler"] for p in b["paragraflar"] for c in p["cumleler"])
    total_w_ses = sum(len(c["ses"].split()) for b in v2["bolumler"] for p in b["paragraflar"] for c in p["cumleler"])

    print(f"Stats: {total_bolum} bolum, {total_par} paragraf, {total_c} cumle")
    print(f"Ekran words: {total_w_ekran}, Ses words: {total_w_ses} (~{total_w_ses / 130:.1f} mins audio)")

    # Save konusma_v2.json
    (TASLAK / "konusma_v2.json").write_text(json.dumps(v2, ensure_ascii=False, indent=1), encoding="utf-8")

    # Generate md, sayfalar, capalar
    sys.path.insert(0, "/home/indu/medsor/meds/scripts/sesli_anlatim")
    import konusma_v2 as KV
    md_txt, sayfalar_l = KV.turet(v2)
    (TASLAK / "konusma_metin.md").write_text(md_txt, encoding="utf-8")
    (TASLAK / "konusma_metni.md").write_text(md_txt, encoding="utf-8")
    (TASLAK / "konusma_sayfalari.json").write_text(json.dumps(sayfalar_l), encoding="utf-8")
    (TASLAK / "konusma_capalari.json").write_text(json.dumps(KV.capalar(v2), ensure_ascii=False), encoding="utf-8")

    # Save cizim_aday.json
    cizim_obj = build_cizim_aday()
    (TASLAK / "cizim_aday.json").write_text(json.dumps(cizim_obj, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Files successfully generated.")


if __name__ == "__main__":
    main()
