# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 29: Karsinojenezin Moleküler Temeli
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 9: Viral ve Mikrobiyal Karsinogenez (Slayt 81 - 90)
Checkpoint: Slayt 89
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_9_slides():
    return [
        # Slayt 81
        {
            "slideNumber": 81,
            "title": "Onkojenik Virüslere Genel Bakış",
            "content": (
                "Biyolojik etkenler küresel ölçekte insan kanserlerinin yaklaşık %15 ila %20'sinin doğrudan "
                "etiyolojik nedenidir. Onkojenik enfeksiyöz ajanlar temel olarak üç grupta incelenir: Onkojenik "
                "RNA virüsleri (HTLV-1), Onkojenik DNA virüsleri (HPV, EBV, KSHV/HHV-8, HBV, Merkel hücre "
                "polyomavirüsü) ve Onkojenik bakteriler (Helicobacter pylori). Virüslerin karsinogenez oluşturma "
                "stratejileri temelde iki ana modele dayanır: Birincisi, konak genomuna doğrudan viral onkoprotein "
                "sokarak tümör baskılayıcı yolakları (TP53 ve RB) inaktive etmek ve proliferasyonu otonom kamçılamak "
                "(HPV, EBV); ikincisi ise konak dokusunda onlarca yıl süren immün-aracılı kronik hasar, rejenerasyon "
                "ve oksidatif DNA mutasyonu zemini kurmaktır (HBV, HCV ve H. pylori)."
            ),
            "elements": [
                make_table(
                    "Onkojenik Virüslerin Temel Sınıflaması",
                    ["Virüs Ailesi", "Nükleik Asit Tipi", "Başlıca İlişkili Malignite"],
                    [
                        {
                            "cells": ["HTLV-1", "Tek sarmallı RNA (Retrovirüs)", "Erişkin T hücreli lösemi / lenfoma (ATLL)"],
                            "hiddenIndex": 2,
                            "hint": "CD4 pozitif T hücresi neoplazmı"
                        },
                        {
                            "cells": ["Yüksek Riskli HPV (16, 18)", "Çift sarmallı DNA", "Serviks, anogenital ve orofarenks skuamöz karsinomu"],
                            "hiddenIndex": 2,
                            "hint": "Yassı epitel karsinomları"
                        },
                        {
                            "cells": ["EBV (HHV-4)", "Çift sarmallı DNA (Herpes)", "Burkitt lenfoma, nazofarenks Ca, Hodgkin"],
                            "hiddenIndex": 2,
                            "hint": "Lenfoid seri ve geniz epiteli neoplazmları"
                        }
                    ]
                ),
                make_cloze(
                    "Küresel kanserlerin yaklaşık yüzde on beş ila yirmisi onkojenik virüsler ve mikroorganizmalar tarafından tetiklenir.",
                    "onkojenik",
                    "Kanser yapıcı biyolojik ajanlar"
                )
            ]
        },

        # Slayt 82
        {
            "slideNumber": 82,
            "title": "Onkojenik RNA Virüsü: HTLV-1 ve Tax Proteini",
            "content": (
                "**İnsan T-Hücreli Lösemi Virüsü Tip 1 (HTLV-1)**, insanlarda doğrudan kansere yol açtığı "
                "kesin olarak kanıtlanmış yegane onkojenik retrovirüstür. Japonya'nın güney kıyıları, Karayipler "
                "ve Orta Afrika'da endemiktir; kan transfüzyonu, cinsel temas ve emzirme ile bulaşır. HTLV-1, "
                "özgül olarak **CD4+ yardımcı T lenfositlerini** enfekte eder ve çok uzun bir latent dönemin "
                "(40-60 yıl) ardından olguların %3-5'inde son derece agresif **Erişkin T-Hücreli Lösemi/Lenfoma "
                "(ATLL)** tablosuna yol açar. Karsinogenezin anahtar molekülü viral **Tax proteinidir**. Tax, "
                "konak genomundaki transkripsiyon faktörü **NF-kappaB'yi** konstitütif olarak aktive eder; "
                "IL-2 ve IL-2 reseptör genlerini tetikleyerek poliklonal otokrin T hücresi proliferasyonu başlatır "
                "ve TP53 fonksiyonlarını baskılayarak genomik istikrarsızlığı kışkırtır."
            ),
            "elements": [
                make_causal_chain(
                    "HTLV-1 Kaynaklı Erişkin T-Hücreli Lösemi (ATLL) Gelişim Zinciri",
                    [
                        "1. Retroviral Giriş: HTLV-1 periferik kanda CD4+ T lenfositlerini enfekte eder ve ters transkripsiyon yapar.",
                        "2. Tax Proteini Ekspresyonu: Viral Tax geni transkribe edilerek sitoplazmada NF-kB inhibitörünü yıkar.",
                        "3. NF-kappaB Aktivasyonu ve Otokrin Döngü: Çekirdeğe geçen NF-kB IL-2 ve IL-2R salgılatarak poliklonal çoğalma başlatır.",
                        "4. Genomik Hasar Birikimi: Tax p53'ü inhibe eder, sentrozom kontrolünü bozar ve hücrede rastlantısal mutasyonlar birikir.",
                        "5. Monoklonal Malign Transformasyon: On yıllar sonra tek bir T hücresi klonu monoklonal otonom ATLL lösemisine evrilir."
                    ]
                ),
                make_active_recall(
                    "HTLV-1 retrovirüsünün CD4+ T hücrelerinde NF-kappaB aktivasyonu ve otokrin çoğalma sağlayan kilit onkoproteini nedir?",
                    "Viral Tax onkoproteinidir.",
                    "Retrovirüs kaynaklı transkripsiyon indükleyicisi"
                )
            ]
        },

        # Slayt 83
        {
            "slideNumber": 83,
            "title": "İnsan Papilloma Virüsü (HPV): Risk Grupları",
            "content": (
                "**İnsan Papilloma Virüsü (HPV)**, skuamöz epitel yüzeyleri (cilt ve müköz membranlar) enfekte "
                "eden küçük, zarfsız çift sarmallı bir DNA virüsüdür. Genotipleri malignite potansiyellerine göre "
                "iki ana sınıfa ayrılır: **Düşük riskli tipler (özellikle Tip 6 ve 11)**, genital bölgede benign "
                "anogenital siğillere (**kondiloma aküminata**) ve laringeal papillomlara yol açarlar; epitelyal "
                "karsinoma ilerleme potansiyelleri sıfırdır. **Yüksek riskli tipler (özellikle Tip 16 ve 18)** ise, "
                "dünya genelindeki **Servikal Skuamöz Hücreli Karsinomların** %70'inden fazlasından, ayrıca vulva, "
                "vajina, penis, anüs karsinomları ile özellikle orofarenks (bademcik, dil kökü) skuamöz karsinomlarının "
                "büyük kısmından doğrudan sorumludur."
            ),
            "elements": [
                make_table(
                    "Düşük Riskli vs Yüksek Riskli HPV Tipleri",
                    ["HPV Grubu", "En Sık Genotipler", "Karakteristik Klinik Lezyonlar", "Malignite Riski"],
                    [
                        {
                            "cells": ["Düşük Riskli Tipler", "HPV Tip 6 ve 11", "Kondiloma aküminata (Genital siğil)", "Malignite riski yoktur (Benign)"],
                            "hiddenIndex": 1,
                            "hint": "Siğil yapan altı ve on bir numaralı tipler"
                        },
                        {
                            "cells": ["Yüksek Riskli Tipler", "HPV Tip 16 ve 18", "Serviks, anogenital ve orofarenks SCC", "Yüksek invaziv karsinom riski"],
                            "hiddenIndex": 1,
                            "hint": "Kanser yapan on altı ve on sekiz numaralı tipler"
                        }
                    ]
                ),
                make_cloze(
                    "Servikal skuamöz hücreli karsinom olgularının çoğundan sorumlu en yaygın yüksek riskli HPV genotipleri Tip 16 ve 18'dir.",
                    "18'dir",
                    "On altı ile birlikte kanser yapan genotip"
                )
            ]
        },

        # Slayt 84
        {
            "slideNumber": 84,
            "title": "HPV Onkoproteinleri: E6 ve E7 Mekanizmaları",
            "content": (
                "Yüksek riskli HPV tiplerinin (HPV 16, 18) karsinojenik gücü, kodladıkları iki temel erken "
                "viral protein olan **E6 ve E7 onkoproteinlerinden** kaynaklanır. **E6 onkoproteini**, konakçı hücredeki "
                "E6AP ubikitin ligazına bağlanarak tümör baskılayıcı **TP53 proteinini yakalar ve proteazomda hızla "
                "parçalanmasına (ubikitinasyon)** yol açar; böylece DNA hasarlı hücre apoptoza gidemez. E6 aynı zamanda "
                "telomeraz enziminin katalitik alt birimi olan **TERT'i aktive ederek** hücreye ölümsüzlük kazandırır. "
                "**E7 onkoproteini** ise, tümör baskılayıcı **Retinoblastom (RB) proteinine** yüksek affinite ile "
                "bağlanır ve RB'yi fosforillenmeye gerek kalmaksızın inaktive ederek hapsolmuş **E2F transkripsiyon "
                "faktörünü serbest bırakır**. Ayrıca E7, siklin bağımlı kinaz inhibitörleri olan **p21 ve p27'yi "
                "inhibe ederek** hücreyi durdurulamaz bir replikasyon fırtınasına sokar."
            ),
            "elements": [
                make_table(
                    "HPV E6 ve E7 Onkoproteinlerinin Karşılaştırmalı Hedefleri",
                    ["Viral Onkoprotein", "Birincil Hücresel Hedef", "Etki Mekanizması", "Hücresel Biyolojik Netice"],
                    [
                        {
                            "cells": ["E6 Onkoproteini", "TP53 proteini ve TERT", "p53'ü ubikitine edip parçalar, telomerazı açar", "Apoptoz kaybı ve replikatif ölümsüzlük"],
                            "hiddenIndex": 1,
                            "hint": "Genom bekçisi p53 molekülü"
                        },
                        {
                            "cells": ["E7 Onkoproteini", "Retinoblastom (RB) ve p21", "RB'yi bağlayıp E2F'yi salar, p21'i bloke eder", "G1-S kontrolünün kalkması ve bölünme"],
                            "hiddenIndex": 1,
                            "hint": "Hücre döngüsü kilit kontrolörü"
                        }
                    ]
                ),
                make_active_recall(
                    "Yüksek riskli HPV enfeksiyonunda p53 proteinine bağlanarak onu ubikitin-proteazom yolağında parçalayan viral protein hangisidir?",
                    "E6 viral onkoproteinidir.",
                    "Erken genomik ürün altı"
                )
            ]
        },

        # Slayt 85
        {
            "slideNumber": 85,
            "title": "HPV Genom İntegrasyonu: Epizomalden Lineere",
            "content": (
                "HPV'nin prekanseröz displaziden invaziv karsinoma ilerlemesinde en kritik moleküler dönüm noktası "
                "**viral genomun konak kromozomuna entegrasyonudur**. Benign kondilomlarda ve düşük dereceli öncül "
                "lezyonlarda (CIN 1) HPV DNA'sı konak çekirdeğinde kromozomdan bağımsız serbest dairesel halkalar "
                "(**epizomal form**) halinde bulunur. Ancak lezyon yüksek dereceye (CIN 2/3) ve invaziv karsinoma "
                "ilerlerken viral halkasal DNA **E1/E2 gen bölgesinden kırılarak** insan kromozomuna lineer olarak "
                "entegre olur. Normalde **viral E2 proteini**, E6 ve E7 onkoproteinlerinin transkripsiyonunu frenleyen "
                "doğal bir negatif regülatördür. Entegrasyon sırasında E2 geni parçalanıp yok olduğu için bu fren "
                "kalkar; konak hücresi kontrolsüz biçimde devasa miktarlarda **E6 ve E7 onkoproteini üretmeye "
                "başlar**; bu durum malign transformasyonu geri dönüşsüz kılar."
            ),
            "elements": [
                make_before_after(
                    "Epizomal HPV (Öncül Lezyon) vs Entegre HPV (İnvaziv Kanser)",
                    "Epizomal Form (CIN 1 / Kondilom)",
                    "Viral DNA konak kromozomundan bağımsız serbest dairesel halkadır. Sağlam E2 proteini E6 ve E7 ekspresyonunu düşük seviyede tutar.",
                    "Entegre Form (İnvaziv Karsinom)",
                    "Viral DNA insan kromozomuna entegredir. E2 geni kırılıp inaktive olur; E6 ve E7 freni boşalır ve aşırı miktarda üretilir.",
                    "Entegrasyon sırasında viral E2 represörünün kaybı karsinogenezin moleküler kilidini açan kritik andır."
                ),
                make_cloze(
                    "HPV genomunun insan DNA'sına entegrasyonu sırasında kırılarak inaktive olan ve E6/E7 üzerindeki represör freni kaldıran gen E2 genidir.",
                    "E2",
                    "İkinci erken viral represör geni"
                )
            ]
        },

        # Slayt 86
        {
            "slideNumber": 86,
            "title": "Epstein-Barr Virüsü (EBV): B Hücre Tropizmi ve LMP1",
            "content": (
                "**Epstein-Barr Virüsü (EBV / HHV-4)**, Gammaherpesvirinae ailesinden çift sarmallı bir DNA "
                "virüsüdür ve erişkin dünya nüfusunun %90'ından fazlasında asemptomatik latent enfeksiyon "
                "halinde bulunur. EBV, tükürük yoluyla bulaşır ve yüzey glikoproteini gp350 aracılığıyla matür B "
                "lenfositlerin yüzeyindeki **CD21 (Kompleman Reseptörü 2)** molekülüne bağlanarak hücre içine "
                "girer. Enfekte B lenfositlerinde latent evrede iki kilit onkoprotein üretilir: **LMP1 (Latent "
                "Membran Proteini 1)** ve **EBNA2**. LMP1, hücresel **CD40 reseptörünü taklit eden** konstitütif "
                "aktif bir sinyal merkezi gibi davranır; JAK/STAT ve NF-kappaB yollarını kesintisiz tetikleyerek "
                "antiapoptotik BCL2 ifadesini fırlatır. **EBNA2** ise, konak Siklin D ve protoonkogenlerini aktive "
                "ederek hücreyi bölünmeye zorlar. Normal bireylerde bu transforme B hücreleri sitotoksik T "
                "hücreleri tarafından kontrol altında tutulur."
            ),
            "elements": [
                make_table(
                    "EBV Ana Onkoproteinleri ve Moleküler Etkileri",
                    ["Viral Protein", "Taklit Ettiği / Etkilediği Yol", "Hücresel Biyolojik Sonuç"],
                    [
                        {
                            "cells": ["LMP1 (Latent Membran Proteini 1)", "CD40 reseptörünü taklit eder, NF-kB uyarır", "Sürekli B hücre sağkalımı ve BCL2 artışı"],
                            "hiddenIndex": 1,
                            "hint": "Meme benzeri sinyal reseptörü benzeri"
                        },
                        {
                            "cells": ["EBNA2 (Nükleer Antijen 2)", "Siklin D ve NOTCH transkripsiyonu", "B lenfositinin G0 evresinden çıkıp bölünmesi"],
                            "hiddenIndex": 1,
                            "hint": "Hücre döngüsü faktörleri aktivatörü"
                        }
                    ]
                ),
                make_cloze(
                    "Epstein-Barr virüsünün B lenfositlere tutunmak için kullandığı hücre yüzey reseptörü CD21 molekülüdür.",
                    "CD21",
                    "Kompleman reseptörü iki belirteci"
                )
            ]
        },

        # Slayt 87
        {
            "slideNumber": 87,
            "title": "EBV ile İlişkili Maligniteler",
            "content": (
                "EBV çok çeşitli hematolojik ve epitelyal malignitelerin etiyolojisinde yer alır: 1) **Burkitt "
                "Lenfoma (Endemik Afrika Tipi)**: Olguların %100'ünde EBV pozitiftir; sıtma ko-enfeksiyonu T hücre "
                "immünitesini zayıflatır ve B hücre proliferasyonu zemininde karakteristik t(8;14) MYC translokasyonu "
                "eklenerek çocuklarda çene kitlesi şeklinde patlar. 2) **Nazofaringeal Karsinom (Özellikle Tip 3 "
                "non-keratinize diferansiye olmayan tip)**: Güneydoğu Asya ve Çin'de endemiktir; tümör hücrelerinin "
                "tümünde viral genom tespit edilir ve serum anti-EBV antikorları (EBNA, VCA) erken tanıda kullanılır. "
                "3) **Hodgkin Lenfoma**: Özellikle Mikst Selüler alt tipte Reed-Sternberg hücrelerinin %50-70'i "
                "EBV-LMP1 pozitiftir. 4) **İmmünsüprese Hastalarda Lenfomalar**: AIDS veya organ nakli hastalarında "
                "T hücre baskılanması sonucu poliklonal EBV reaktivasyonu ve B hücreli lenfoproliferatif hastalıklar gelişir."
            ),
            "elements": [
                make_table(
                    "EBV ile İlişkili Başlıca Maligniteler",
                    ["Malignite Adı", "Hedef Hücre / Doku", "EBV İlişki Oranı", "Önemli Klinik Özellik"],
                    [
                        {
                            "cells": ["Endemik Burkitt Lenfoma", "B lenfoblastlar", "Yaklaşık %100", "Afrika'da çocuklarda masif mandibular kitle"],
                            "hiddenIndex": 3,
                            "hint": "Çene kemiği tümöral büyümesi"
                        },
                        {
                            "cells": ["Nazofarenks Karsinomu (Tip 3)", "Nazofarenks epitel hücreleri", "%100 (Non-keratinize tip)", "Çin ve Asya'da endemik karsinom"],
                            "hiddenIndex": 3,
                            "hint": "Uzak doğu bölgesi epitelyal tümörü"
                        },
                        {
                            "cells": ["Hodgkin Lenfoma (Mikst Selüler)", "Reed-Sternberg dev hücreleri", "%50-70 pozitif", "Bimodal yaş dağılımı ve B semptomları"],
                            "hiddenIndex": 3,
                            "hint": "Baykuş gözü hücreli lenfoma"
                        }
                    ]
                ),
                make_active_recall(
                    "Güneydoğu Asya'da endemik olan, non-keratinize histolojide ve olguların tamamında EBV genomu içeren epitelyal malignite hangisidir?",
                    "Nazofaringeal karsinomdur (Tip 3 diferansiye olmayan nazofarenks kanseri).",
                    "Üst solunum yolu epitel malignitesi"
                )
            ]
        },

        # Slayt 88
        {
            "slideNumber": 88,
            "title": "Hepatotropik Virüsler (HBV ve HCV) ve Karaciğer Kanseri",
            "content": (
                "Dünya genelinde **Hepatosellüler Karsinom (HCC)** olgularının yaklaşık %70-85'i kronik **Hepatit "
                "B Virüsü (HBV)** veya **Hepatit C Virüsü (HCV)** enfeksiyonuna bağlıdır. HBV bir hepadnavirüs "
                "(DNA virüsü), HCV ise flavivirüstür (tek sarmallı RNA virüsü). Bu virüslerin karsinogenez "
                "mekanizması öncelikli olarak **immün-aracılı kronik karaciğer hasarı, fibrozis ve siroz zeminine** "
                "dayanır. Sitotoksik T hücreleri ile enfekte hepatositler arasında yıllar boyu süren mücadele, "
                "aralıksız bir hepatosit ölümü ve rejenerasyonu tetikler; rejenerasyon sırasında reaktif oksijen "
                "radikalleri hepatosit genomunda somatik mutasyonlar biriktirir. Ayrıca HBV'de viral **HBx proteini**, "
                "p53 fonksiyonunu inhibe ederek ve transkripsiyonu uyararak doğrudan onkojenik rol de oynar. "
                "HCV ise bir RNA virüsü olduğundan konak genomuna entegre olmaz; karsinogenezi tamamen kronik "
                "inflamasyon ve siroz üzerinden yürütür."
            ),
            "elements": [
                make_before_after(
                    "Hepatit B (HBV) ile Hepatit C (HCV) Karsinogenez Mekanizması Farkı",
                    "Hepatit B Virüsü (HBV - DNA Virüsü)",
                    "DNA virüsüdür; konak genomuna entegre olabilir. Kronik sirozun yanı sıra viral HBx proteini ile doğrudan onkojenik etki de yapabilir.",
                    "Hepatit C Virüsü (HCV - RNA Virüsü)",
                    "RNA virüsüdür; konak genomuna ASLA entegre olmaz. Karsinogenez neredeyse tamamen kronik inflamasyon ve siroz zeminine bağlıdır.",
                    "HBV siroz gelişmeden de nadiren HCC yapabilirken, HCV ilişkili HCC vakalarının neredeyse tamamı siroz zeminindedir."
                ),
                make_cloze(
                    "Hepatit B virüsünün konak genomuna entegre olarak p53'ü inhibe eden ve transkripsiyonu bozan viral proteini HBx proteinidir.",
                    "HBx",
                    "Hepatit B x onkoproteini"
                )
            ]
        },

        # Slayt 89: CHECKPOINT 9
        {
            "slideNumber": 89,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Viral ve Mikrobiyal Karsinogenez",
            "content": (
                "Dokuzuncu bölümün bu tekrar sayfasında, onkojenik virüsler ve mikroorganizmaların kanser "
                "oluşturma mekanizmaları özetlenmektedir. HTLV-1 retrovirüsü viral Tax proteini ile NF-kB'yi "
                "uyararak 40-60 yıl sonra erişkin T hücreli lösemiye (ATLL) yol açar. Yüksek riskli HPV (Tip 16, 18), "
                "E6 proteini ile p53'ü parçalar ve telomerazı açarken; E7 proteini ile RB'yi bağlayarak E2F'yi salar. "
                "Viral DNA konak genomuna entegre olurken repressör E2 geninin parçalanması E6/E7 üretimini "
                "serbest bırakır. EBV, CD21 ile B lenfositlere girer; LMP1 ile CD40'ı taklit eder, Burkitt ve "
                "nazofarenks karsinomunu tetikler. HBV ve HCV ise kronik nekroinflamasyon, rejenerasyon ve siroz "
                "üzerinden hepatosellüler karsinomu (HCC) doğurur."
            ),
            "flashcards": [
                {
                    "id": "k1-29-cp09-fc01",
                    "front": "Yüksek riskli HPV tiplerinde (16, 18) p53 tümör baskılayıcı proteinini yakalayarak ubikitin-proteazomda parçalayan onkoprotein nedir?",
                    "back": "E6 viral onkoproteinidir.",
                    "hint": "Erken genomik ürün altı"
                },
                {
                    "id": "k1-29-cp09-fc02",
                    "front": "Yüksek riskli HPV tiplerinde Retinoblastom (RB) proteinine bağlanarak E2F transkripsiyon faktörünü serbest bırakan viral onkoprotein nedir?",
                    "back": "E7 viral onkoproteinidir.",
                    "hint": "Erken patolojik ürün yedi"
                },
                {
                    "id": "k1-29-cp09-fc03",
                    "front": "Epstein-Barr virüsünün (EBV) B lenfositlerde hücresel CD40 reseptörünü taklit ederek sürekli sağkalım sinyali veren ana onkoproteini nedir?",
                    "back": "LMP1 proteinidir (Latent Membran Proteini 1).",
                    "hint": "Zar yerleşimli onkojenik uyaran faktör"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 9 Özet Tablosu: Onkojenik Virüsler ve Onkoproteinleri",
                    ["Onkojenik Virüs", "Kilit Viral Onkoprotein", "Etkilenen Konakçı Hedef / Mekanizma"],
                    [
                        {
                            "cells": ["HPV Tip 16, 18", "E6 ve E7 Onkoproteinleri", "p53 yıkımı ve RB/E2F aktivasyonu"],
                            "hiddenIndex": 2,
                            "hint": "İki kilit tümör baskılayıcının felci"
                        },
                        {
                            "cells": ["EBV (HHV-4)", "LMP1 ve EBNA2", "CD40 taklidi, NF-kB ve BCL2 aktivasyonu"],
                            "hiddenIndex": 2,
                            "hint": "B lenfosit sağkalım sinyali benzeri"
                        }
                    ]
                )
            ]
        },

        # Slayt 90
        {
            "slideNumber": 90,
            "title": "Klinik Karar: Serviks Kanserinde HPV Taraması ve Aşı Profilaksisi",
            "content": (
                "Servikal karsinogenezin moleküler temelinin aydınlatılması, halk sağlığında çığır açan koruyucu "
                "stratejilerin temelini atmıştır. Güncel tarama kılavuzları, 30 yaş üstü kadınlarda Pap smear "
                "sitolojisi ile birlikte **yüksek riskli HPV DNA testinin (HPV-DNA co-testing)** yapılmasını "
                "önermektedir. HPV-DNA testi negatif olan kadınlarda serviks kanseri riski 5 yıl boyunca sıfıra "
                "yakındır. Birinci basamak korunmada ise, yüksek riskli onkojenik tiplerin (HPV 16, 18 ve diğerleri) "
                "L1 majör kapsid proteininden rekombinant DNA teknolojisiyle üretilen **HPV aşıları (gardasil vb.)**, "
                "virüs benzeri partiküller (VLP) aracılığıyla yüksek nötralizan antikor yanıtı oluşturarak "
                "servikal preinvaziv displazi ve invaziv skuamöz karsinom gelişimini %90'ın üzerinde engellemektedir."
            ),
            "elements": [
                make_branching_logic(
                    "32 yaşında asemptomatik kadın hastanın rutin jinekolojik kontrolünde yapılan Pap smear sitolojisi normal (NILM) raporlanıyor ancak eş zamanlı bakılan HPV DNA testinde yüksek riskli HPV Tip 16 pozitif saptanıyor.",
                    "Servikal karsinogenezin moleküler dinamikleri ve E6/E7 entegrasyon riski göz önüne alındığında hekimin atması gereken en doğru klinik adım ne olmalıdır?",
                    [
                        {
                            "text": "HPV Tip 16 yüksek onkojenik potansiyel taşıdığından sitoloji normal olsa dahi hasta derhal kolposkopi ve şüpheli alan biyopsisi ile değerlendirilmelidir.",
                            "isCorrect": True,
                            "explanation": "HPV 16 ve 18 pozitifliği, sitoloji normal dahi olsa invaziv öncül riskini fırlatır; doğrudan kolposkopik muayene kılavuz standartıdır."
                        },
                        {
                            "text": "Pap smear normal olduğu için HPV sonucuna bakılmaksızın hasta 5 yıl sonra kontrole çağrılmalıdır.",
                            "isCorrect": False,
                            "explanation": "Pap smear yalancı negatif olabilir; HPV 16 pozitifliğinde 5 yıl beklemek kansere davetiye çıkarır."
                        },
                        {
                            "text": "Hastaya derhal radikal histerektomi ameliyatı uygulanmalıdır.",
                            "isCorrect": False,
                            "explanation": "Kolposkopik biyopside invaziv karsinom kanıtlanmadan radikal histerektomi endikasyonu yoktur."
                        }
                    ]
                ),
                make_micro_quiz(
                    "Rekombinant HPV aşılarının üretiminde kullanılan ve nötralizan antikor üretimini tetikleyen temel immünojenik viral yapısal bileşen hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "L1 majör kapsid proteini (Virüs benzeri partiküller - VLP)",
                            "isCorrect": True,
                            "explanation": "HPV aşıları viral DNA içermez; maya veya böcek hücrelerinde sentezlenen L1 kapsid proteininin oluşturduğu virüs benzeri partiküllerden (VLP) oluşur."
                        },
                        {
                            "key": "B",
                            "text": "E6 onkoproteini",
                            "isCorrect": False,
                            "explanation": "E6 erken viral proteindir, aşıda bulunmaz."
                        },
                        {
                            "key": "C",
                            "text": "E7 onkoproteini",
                            "isCorrect": False,
                            "explanation": "E7 aşı içeriği değildir."
                        },
                        {
                            "key": "D",
                            "text": "Viral E2 represör proteini",
                            "isCorrect": False,
                            "explanation": "E2 düzenleyici proteindir, koruyucu aşı L1 kapsid proteinine dayanır."
                        }
                    ],
                    "HPV aşıları L1 kapsid proteinine karşı koruyucu antikor yanıtı oluşturur."
                )
            ]
        }
    ]
