# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 27: Üriner Sistem Taş Hastalıkları Fizyopatolojisi
Bölüm 1: Epidemiyoloji, Coğrafi Dağılım ve Risk Faktörleri (Slayt 1 - 10)
Checkpoint: Slayt 9
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_1_slides():
    return [
        # Slayt 1
        {
            "slideNumber": 1,
            "title": "Ürolitiyazise Genel Bakış ve Küresel Epidemiyoloji",
            "content": (
                "Ürolitiyazis, böbrek parankiminde, kalikslerde, renal pelviste veya alt üriner sistemde mineral "
                "kristallerinin agregasyonu sonucu sert kalsifiye kitlelerin oluşmasıyla karakterize, yüksek morbiditeye "
                "sahip sistemik bir metabolik hastalıktır. Küresel prevalans son dekatlarda özellikle sanayileşmiş ve batı "
                "tipi beslenme tarzını benimseyen toplumlarda doğrusal bir artış göstererek %1 ile %20 arasında geniş bir "
                "dağılım sergilemektedir. İsveç, Kanada ve Amerika Birleşik Devletleri gibi sosyoekonomik düzeyi yüksek "
                "ülkelerde hayat boyu taş geliştirme riski %10'un üzerine çıkmıştır. Hastalık yalnızca mekanik bir üriner obstrüksiyon "
                "tablosu olmayıp, altta yatan sistemik vasküler, endokrin ve renal tübüler dengesizliklerin kümülatif bir dışavurumudur."
            ),
            "elements": [
                make_cloze(
                    "Küresel ölçekte ürolitiyazis prevalansı son dekatlarda artarak dünya nüfusunun yüzde bir ila yirmisini etkileyen oranlara ulaşmıştır.",
                    "yüzde bir ila yirmisini",
                    "Geniş küresel insidans aralığı"
                ),
                make_active_recall(
                    "Sanayileşmiş ülkelerde yaşam boyu üriner taş geliştirme riski hangi kritik eşik değerin üzerine çıkmıştır?",
                    "Yüzde on sınırının üzerine çıkmıştır.",
                    "Çift haneli prevalans düzeyi"
                )
            ]
        },
        # Slayt 2
        {
            "slideNumber": 2,
            "title": "Coğrafi Dağılım: Taş Kuşağı ve Türkiye'nin Konumu",
            "content": (
                "Üriner sistem taş hastalığı coğrafi ve iklimsel faktörlerden son derece belirgin biçimde etkilenir. "
                "Dünya genelinde kuru, kurak ve sıcak subtropikal kuşakta yer alan bölgeler 'taş kuşağı' (stone belt) "
                "olarak tanımlanır. Türkiye, coğrafi konumu ve iklimsel özellikleri itibarıyla Akdeniz ve Orta Doğu taş "
                "kuşağının tam kalbinde yer almakta olup, toplumdaki taş hastalığı prevalansı yaklaşık %15 seviyesindedir. "
                "Sıcak iklim koşullarında perspiratio insensibilis (hissedilmeyen terleme) ve aşırı terleme yoluyla serbest "
                "su kaybı meydana gelir; bu durum idrar konsantrasyonunu artırarak çözünen iyonların aşırı doygunluğa (supersaturasyon) "
                "ulaşmasına ve kristal çekirdeklenmesinin termodinamik olarak tetiklenmesine doğrudan zemin hazırlar."
            ),
            "elements": [
                make_table(
                    "Coğrafi ve İklimsel Faktörlerin Taş Oluşumuna Etkisi",
                    ["Bölge / Faktör", "İklimsel Karakter", "Fizyopatolojik Süreç", "Taş Riski"],
                    [
                        {
                            "cells": ["Taş Kuşağı (Türkiye vb.)", "Sıcak ve kurak", "Aşırı terleme ile idrar hacmi azalması", "Yüksek (%15 civarı)"],
                            "hiddenIndex": 3,
                            "hint": "Türkiye prevalans oranı"
                        },
                        {
                            "cells": ["Kuzey Ilıman Kuşak", "Serin ve yağışlı", "Düşük terleme, dengeli hidrasyon", "Göreceli düşük (%5-8)"],
                            "hiddenIndex": 2,
                            "hint": "Vücut sıvı kaybının azlığı"
                        }
                    ]
                ),
                make_before_after(
                    "İklim Koşullarının İdrar Dinamiklerine Etkisi",
                    "Serin ve Nemli İklim",
                    "Yeterli idrar hacmi (>2 L/gün), düşük kristal konsantrasyonu, korunan kristalizasyon inhibitör etkinliği.",
                    "Sıcak ve Kurak İklim",
                    "Konsantre idrar (<1 L/gün), yüksek kalsiyum ve oksalat süpersatürasyonu, kristal çökelmesinde belirgin hızlanma.",
                    "Türkiye gibi taş kuşağı ülkelerinde sıcak yaz aylarında dehidratasyon primer taş tetikleyicisidir."
                )
            ]
        },
        # Slayt 3
        {
            "slideNumber": 3,
            "title": "Demografik Faktörler: Yaş ve Cinsiyet Dağılımı",
            "content": (
                "Ürolitiyazis insidansı hayatın dördüncü ile altıncı dekatları (30-60 yaş arası) arasında zirve yapmaktadır. "
                "Tarihsel olarak taş hastalığı erkeklerde kadınlara kıyasla 2-3 kat daha sık bildirilmişken, son çeyrek "
                "asırda kadınlarda obezite, metabolik sendrom ve beslenme alışkanlıklarındaki dönüşüme paralel olarak bu "
                "cinsiyet farkı hızla kapanmaktadır. Taş hastalığı 20 yaşından önce oldukça nadirdir; genç yaş grubunda veya "
                "çocukluk çağında taş tespit edildiğinde primer hiperoksalüri veya sistinüri gibi monogenik metabolik bozukluklar "
                "mutlaka dışlanmalıdır. Etnik köken açısından beyaz ırkta insidans Asyalı ve siyahi popülasyonlara göre anlamlı düzeyde yüksektir."
            ),
            "elements": [
                make_cloze(
                    "Böbrek taşı insidansı yaşam döngüsü boyunca en sık dördüncü ila altıncı dekatlar arasında doruk noktasına ulaşır.",
                    "dördüncü ila altıncı dekatlar",
                    "Otuz ile altmış yaş dönemi"
                ),
                make_causal_chain(
                    "Erkeklerde Tarihsel Yüksek Taş Riskinin Biyolojik Mekanizması",
                    [
                        "1. Testosteron Etkisi: Karaciğerde glioksilat metabolizması üzerinden endojen oksalat üretiminin uyarılması",
                        "2. Östrojen Yokluğu: Kadınlardaki östrojen hormonunun idrar sitrat atılımını artırıcı koruyucu etkisinden yoksunluk",
                        "3. Kas Kitlesi Farkı: Yüksek endojen kreatinin ve pürin yıkımı nedeniyle daha yüksek ürik asit filtrasyonu",
                        "4. Süpersatürasyon: İdrarda oksalat ve ürik asit konsantrasyonunun yükselerek litogenezi kolaylaştırması"
                    ]
                )
            ]
        },
        # Slayt 4
        {
            "slideNumber": 4,
            "title": "Çevresel ve Mesleki Dehidratasyon",
            "content": (
                "Çevresel sıcaklık ve mesleki maruziyet, idrar hacmi ve konsantrasyonu üzerinde doğrudan belirleyicidir. "
                "Aşırı sıcak fırınlar, dökümhaneler, cam atölyeleri veya açık arazi tarım işçiliği gibi yüksek termal strese "
                "sahip ortamlarda çalışan bireylerde profüz terleme gelişir. Eğer kaybedilen sıvı yeterli elektrolitsiz veya "
                "elektrolitli su ile yerine konmazsa, antidiüretik hormon (ADH) salgısı maksimuma çıkarak renal medüller "
                "konsantrasyon mekanizmasını tetikler. Oluşan düşük hacimli (<1000 mL/gün) ve yüksek ozmolaliteli idrarda "
                "kalsiyum, oksalat ve ürat konsantrasyonu metastabil sınırları aşarak spontan kristalleşmeyi başlatır."
            ),
            "elements": [
                make_active_recall(
                    "Aşırı sıcak mesleki ortamlarda çalışanlarda taş oluşumunu tetikleyen birincil hormonal yanıt nedir?",
                    "Antidiüretik hormon salgısının artarak idrarı aşırı konsantre hale getirmesidir.",
                    "Vazopressin aracılı su geri emilimi"
                ),
                make_micro_quiz(
                    "Mesleki sıcaklık maruziyetine bağlı taş gelişiminde temel fizyopatolojik mekanizma hangisidir?",
                    [
                        {
                            "text": "Artmış terleme ve yetersiz sıvı alımına bağlı idrar hacminde belirgin azalma ve süpersatürasyon",
                            "isCorrect": True,
                            "explanation": "Doğrudur; su kaybı idrar konsantrasyonunu artırarak kristalizasyon eşiğini aşar."
                        },
                        {
                            "text": "Karaciğerde aşırı miktarda primer sistin sentezlenmesi",
                            "isCorrect": False,
                            "explanation": "Sistinüri genetik bir renal taşıyıcı defektidir, çevresel ısıyla doğrudan ilişkili değildir."
                        },
                        {
                            "text": "Paratiroid hormon sekresyonunun ani termal baskılanması",
                            "isCorrect": False,
                            "explanation": "Termal stres PTH baskılaması yapmaz; kalsiyum metabolizması primer olarak bozulmaz."
                        },
                        {
                            "text": "Böbrek tübüllerinde hidrojen pompalarının felce uğraması",
                            "isCorrect": False,
                            "explanation": "Tübüler asidoz patolojisidir; termal dehidratasyonun primer etkisi hacim eksikliğidir."
                        }
                    ],
                    "Dehidratasyon, çözünen tuzların konsantrasyonunu artırarak kristal oluşumunu fizikokimyasal olarak hızlandırır."
                )
            ]
        },
        # Slayt 5
        {
            "slideNumber": 5,
            "title": "Sistemik Risk Faktörleri: Obezite ve Metabolik Sendrom",
            "content": (
                "Obezite ve metabolik sendrom, litogenez patofizyolojisinde kritik birer sistemik tetikleyicidir. Visseral "
                "adipozite ve periferik insülin direnci, renal tübüler hücrelerde amonyogenez (NH4+ üretimi) mekanizmasını "
                "bozar. Proksimal tübülde sodyum-hidrojen değiştirici tip 3 (NHE3) disfonksiyonu meydana gelir ve idrarın "
                "amonyum ile tamponlanması sekteye uğrar. Sonuç olarak idrar pH'ı patolojik olarak düşer (<5.5). Düşük idrar "
                "pH'ı ürik asit kristallerinin hızla çökmesine yol açarken, artmış vücut kütlesi hiperkalsiüri, hiperoksalüri "
                "ve hiperürikozüri ile birleşerek multifaktöriyel taş oluşumunu tetikler."
            ),
            "elements": [
                make_causal_chain(
                    "İnsülin Direncinden Taş Oluşumuna Uzanan Tübüler Patofizyoloji",
                    [
                        "1. İnsülin Direnci: Renal proksimal tübül hücrelerinde insülin sinyalizasyonunun kesintiye uğraması",
                        "2. Amonyogenez Kusuru: Glutamin deaminasyonu ve amonyum sentezinin yetersiz kalması",
                        "3. Tamponlama Yetersizliği: İdrar hidrojen iyonlarının tamponlanamaması sonucu asidik idrar (pH <5.5)",
                        "4. Ürik Asit Çökmesi: Çözünmeyen ürik asidin hızla kristalleşmesi ve kalsiyum oksalat için nidus olması"
                    ]
                ),
                make_table(
                    "Metabolik Sendrom Bileşenleri ve Ürolitiyazis Riski",
                    ["Bileşen", "Biyokimyasal Değişiklik", "Üriner Sonuç", "Gelişen Taş Tipi"],
                    [
                        {
                            "cells": ["Visseral Obezite", "İnsülin direnci ve lipotoksisite", "İdrar pH düşüklüğü ve hiperkalsiüri", "Ürik asit ve kalsiyum oksalat"],
                            "hiddenIndex": 3,
                            "hint": "En yaygın iki taş türü"
                        },
                        {
                            "cells": ["Dislipidemi", "Renal lipid birikimi ve oksidatif stres", "Tübüler epitel hasarı ve kristal retansiyonu", "Kalsiyum oksalat"],
                            "hiddenIndex": 2,
                            "hint": "Epitel membran hasarı sonucu"
                        }
                    ]
                )
            ]
        },
        # Slayt 6
        {
            "slideNumber": 6,
            "title": "Tip 2 Diyabet ve İdrar Asidifikasyon Bozukluğu",
            "content": (
                "Tip 2 diabetes mellitus hastalarında taş hastalığı riski genel popülasyona kıyasla iki kat daha fazladır. "
                "Bu hastalarda görülen en temel anormallik, kronik olarak aşırı asidik idrar (pH 5.0 - 5.5) çıkarılmasıdır. "
                "Glukotoksisite ve lipotoksisite, medüller toplayıcı tübüllerdeki asit-baz düzenleme kapasitesini aşındırır. "
                "Ayrıca diyabetiklerde bağırsak geçirgenliğinin artması ve metabolik hiperfiltrasyon nedeniyle idrarla oksalat "
                "atılımı belirgin şekilde artar. Dolayısıyla diyabetik hastalar hem saf ürik asit taşları hem de ürik asit "
                "nidusları üzerinde büyüyen mikst kalsiyum oksalat taşları açısından son derece hassas bir zemin taşırlar."
            ),
            "elements": [
                make_cloze(
                    "Tip 2 diyabetli bireylerde renal amonyum üretiminin bozulması sonucu idrar pH düzeyi kronik olarak asidik kalır.",
                    "idrar pH düzeyi",
                    "Üriner asitlik parametresi"
                ),
                make_active_recall(
                    "Tip 2 diyabette ürik asit taşı riskini artıran primer fizyopatolojik idrar anormalliği nedir?",
                    "İdrar pH'ının tamponlama yetersizliği nedeniyle kronik olarak 5.5'in altında seyretmesidir.",
                    "Asidik idrar ortamı"
                )
            ]
        },
        # Slayt 7
        {
            "slideNumber": 7,
            "title": "Diyet Alışkanlıkları: Sıvı, Sodyum ve Hayvansal Protein",
            "content": (
                "Diyet bileşenleri litogenez üzerinde doğrudan ve güçlü modülatör etkilere sahiptir. Günlük sıvı alımının "
                "yetersiz olması idrar hacmini azaltarak taş oluşumunun en güçlü bağımsız risk faktörünü oluşturur. Yüksek "
                "sodyum alımı, proksimal tübülde kalsiyum ile sodyumun ortak geri emilim mekanizmasını bozar; artmış sodyum "
                "atılımı zorunlu kalsiüriye yol açarak idrar kalsiyumunu tehlikeli biçimde yükseltir. Aşırı hayvansal protein "
                "tüketimi ise kükürtlü amino asitlerin (metiyonin, sistein) yıkımıyla belirgin bir endojen asit yükü üretir; "
                "bu durum kemik resorpsiyonunu uyarır, idrar sitrat atılımını (en önemli inhibitör) baskılar ve hiperürikozüri yaratır."
            ),
            "elements": [
                make_before_after(
                    "Diyet Değişikliklerinin Üriner Litogenez Parametrelerine Etkisi",
                    "Yüksek Sodyum ve Hayvansal Protein",
                    "Yüksek idrar kalsiyumu, düşük idrar sitratı, yüksek ürik asit atılımı ve asidik idrar; litogenez zirvede.",
                    "Dengeli Kalsiyum, Düşük Sodyum ve Bol Sıvı",
                    "Yeterli idrar hacmi (>2 L), kalsiyum atılımında azalma, sitrat inhibitör kapasitesinde artış; taş riski minimize.",
                    "Sodyum kısıtlaması proksimal kalsiyum geri emilimini artırarak hiperkalsiüriyi doğrudan düzeltir."
                ),
                make_micro_quiz(
                    "Aşırı hayvansal protein tüketiminin idrar biyokimyasında yol açtığı en tehlikeli değişiklik hangisidir?",
                    [
                        {
                            "text": "Metabolik asit yükü yaratarak idrar sitrat atılımını düşürmesi ve ürik asidi artırması",
                            "isCorrect": True,
                            "explanation": "Doğrudur; kükürtlü amino asit asidozu sitrat geri emilimini artırır ve idrardaki koruyucu sitratı yok eder."
                        },
                        {
                            "text": "İdrar pH'ını 8.0'in üzerine çıkararak alkali taşları provoke etmesi",
                            "isCorrect": False,
                            "explanation": "Protein yükü idrarı alkali değil tam tersine oldukça asidik hale getirir."
                        },
                        {
                            "text": "Renal tübüllerde kalsiyum emilimini artırarak hipokalsiüri yapması",
                            "isCorrect": False,
                            "explanation": "Protein kaynaklı asidoz kalsiyum atılımını artırır, hiperkalsiüri oluşturur."
                        },
                        {
                            "text": "Bağırsakta oksalat emilimini tamamen durdurması",
                            "isCorrect": False,
                            "explanation": "Protein yükü bağırsakta oksalat emilimini durdurmaz."
                        }
                    ],
                    "Hayvansal protein, hem asit yüküyle hipositratüriye hem de pürin yüküyle hiperürikozüriye neden olur."
                )
            ]
        },
        # Slayt 8
        {
            "slideNumber": 8,
            "title": "Pediatrik Taş Hastalığı ve Monogenik Nedenler",
            "content": (
                "Çocukluk ve ergenlik çağında ürolitiyazis erişkinlere göre çok daha az sıklıkta görülmekle birlikte, son "
                "25 yılda çocuk vakalarda belirgin bir tırmanış kaydedilmiştir. Pediatrik grupta saptanan her taş vakası, "
                "altta yatan genetik veya anatomik bir anormalliğin habercisi olarak kabul edilmelidir. En sık monogenik "
                "nedenler arasında otozomal resesif geçişli sistinüri (SLC3A1 ve SLC7A9 mutasyonları) ve primer hiperoksalüri "
                "(AGXT mutasyonuna bağlı Tip 1 PH) yer alır. Primer hiperoksalüri Tip 1, erken çocukluk döneminde hızla sistemik "
                "oksalozis, nefrokalsinozis ve son dönem böbrek yetmezliğine ilerleyebilen ölümcül bir klinik tablodur."
            ),
            "elements": [
                make_cloze(
                    "Çocukluk çağında saptanan rekürren kalsiyum oksalat taşlarında karaciğer peroksizomal enzim defekti olan primer hiperoksalüri düşünülmelidir.",
                    "primer hiperoksalüri",
                    "Ciddi genetik oksalat metabolizma bozukluğu"
                ),
                make_active_recall(
                    "Pediatrik taş hastalarında monogenik genetik tarama yapılmasını gerektiren en kritik iki patoloji nedir?",
                    "Sistinüri ve primer hiperoksalüri tablolarıdır.",
                    "Resesif metabolik bozukluklar"
                )
            ]
        },
        # Slayt 9 [CHECKPOINT 1]
        {
            "slideNumber": 9,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Epidemiyoloji ve Risk Faktörleri",
            "content": (
                "Bu bölümde ürolitiyazisin küresel epidemiyolojisini, çevresel dinamiklerini ve sistemik zeminini inceledik. "
                "Böbrek taşı prevalansı dünya genelinde %1-20 arasında olup yaşam tarzı değişiklikleriyle sürekli artmaktadır. "
                "Türkiye, sıcak ve kurak iklim kuşağında yer alması nedeniyle %15 gibi oldukça yüksek bir taş sıklığına sahiptir. "
                "İnsidans 30-60 yaş grubunda zirve yapar; erkek üstünlüğü son yıllarda kadınlarda obezite artışıyla dengelenmektedir. "
                "Obezite, insülin direnci ve tip 2 diyabet, renal amonyogenezi bozarak kronik asidik idrar (pH <5.5) oluşturur. "
                "Diyetle aşırı sodyum ve hayvansal protein alımı hiperkalsiüri ve hipositratüri yaratarak litogenezi tetikler. "
                "Çocukluk çağında görülen taşlarda primer hiperoksalüri ve sistinüri gibi monogenik hastalıklar mutlaka araştırılmalıdır."
            ),
            "flashcards": [
                {
                    "id": "k1-27-cp01-fc01",
                    "front": "Türkiye'nin coğrafi olarak taş kuşağında yer alması toplumda yaklaşık yüzde kaçlık bir ürolitiyazis prevalansı yaratır?",
                    "back": "Yüzde on beş civarında bir prevalans yaratır.",
                    "hint": "Akdeniz kuşağı sıklık oranı"
                },
                {
                    "id": "k1-27-cp01-fc02",
                    "front": "Metabolik sendrom ve tip 2 diyabette proksimal tübüler amonyogenez kusurunun idrar pH'ına net etkisi nedir?",
                    "back": "İdrarın dengelenememesi sonucu pH değerinin beş buçuğun altına düşerek fazlaca asidikleşmesidir.",
                    "hint": "Nötralize edilemeyen serbest proton boşalımı neticesi"
                },
                {
                    "id": "k1-27-cp01-fc03",
                    "front": "Genç yaşta veya çocuklukta tekrarlayan taş oluşumu ile başvuran bir hastada taranması gereken iki temel resesif genetik patoloji nedir?",
                    "back": "Primer hiperoksalüri ve sistinüri metabolik bozukluklarıdır.",
                    "hint": "Ciddi monogenik litiazis nedenleri"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 1 Özet Tablosu: Epidemiyolojik Risk Belirteçleri",
                    ["Risk Faktörü", "Kritik Değer / Durum", "Primer Mekanizma", "Klinik Yansıma"],
                    [
                        {
                            "cells": ["Coğrafya", "Taş Kuşağı (%15)", "Dehidratasyon ve perspirasyon", "Konsantre litik idrar"],
                            "hiddenIndex": 3,
                            "hint": "Azalmış idrar debisi"
                        },
                        {
                            "cells": ["Tip 2 Diyabet", "İdrar pH < 5.5", "Bozulmuş renal amonyogenez", "Ürik asit çökmesi"],
                            "hiddenIndex": 2,
                            "hint": "Tamponlayıcı baz sentez kusuru"
                        }
                    ]
                )
            ]
        },
        # Slayt 10
        {
            "slideNumber": 10,
            "title": "Klinik Karar: Epidemiyolojik ve Metabolik Değerlendirme",
            "content": (
                "Ürolitiyazis şüphesiyle başvuran her hastada ayrıntılı bir epidemiyolojik ve mesleki öykü alınmalıdır. "
                "Hastanın günlük sıvı tüketim miktarı, çalıştığı ortamın termal özellikleri, hayvansal protein ve sofra tuzu "
                "tüketim alışkanlıkları sorgulanmalıdır. Eşlik eden metabolik sendrom, hipertansiyon ve diyabet varlığı "
                "idrar pH tablosunu doğrudan öngörmeyi sağlar. Aile öyküsünün pozitif olması veya taşın erken yaşta başlaması, "
                "hastanın rutin konservatif tedavi yerine ileri metabolik değerlendirme (24 saatlik idrar analizi ve genetik "
                "panel) protokolüne erkenden dahil edilmesini zorunlu kılar."
            ),
            "elements": [
                make_branching_logic(
                    "42 yaşında fırın işçisi erkek hasta, sağ yan ağrısı şikayetiyle başvuruyor. Öyküsünde günde 1 litreden az su içtiği, aşırı terlediği ve günde 2 paket tuzlu kuruyemiş tükettiği öğreniliyor.",
                    "Bu hastada taşa zemin hazırlayan temel fizyopatolojik mekanizma ve ilk basamak yönetim ne olmalıdır?",
                    [
                        {
                            "text": "Mesleki dehidratasyon ve yüksek sodyuma bağlı hiperkalsiüri; günlük idrar hacmini 2 litrenin üzerine çıkaracak hidrasyon ve tuz kısıtlaması planlanmalıdır.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; hacim eksikliği ve yüksek sodyum kalsiyum atılımını artırarak süpersatürasyona neden olur."
                        },
                        {
                            "text": "Hastada primer paratiroid adenomu düşünülmeli ve derhal cerrahi eksplorasyon yapılmalıdır.",
                            "isCorrect": False,
                            "explanation": "Öyküdeki çevresel dehidratasyon ve diyet faktörleri primer nedendir, paratiroid cerrahisi endikasyonu yoktur."
                        },
                        {
                            "text": "İdrar asitleştirici ajanlar verilerek kalsiyum çökmesi engellenmelidir.",
                            "isCorrect": False,
                            "explanation": "İdrarı asitleştirmek kalsiyum ve ürik asit çökmesini daha da artırabilir, hidrasyon esastır."
                        }
                    ]
                )
            ]
        }
    ]
