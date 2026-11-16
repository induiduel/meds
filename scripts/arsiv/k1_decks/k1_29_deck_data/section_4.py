# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 29: Karsinojenezin Moleküler Temeli
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 4: Epigenetik Modifikasyonlar ve Onkomirler (Slayt 31 - 40)
Checkpoint: Slayt 39
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_4_slides():
    return [
        # Slayt 31
        {
            "slideNumber": 31,
            "title": "Kanser Epigenetiğine Giriş",
            "content": (
                "Epigenetik, DNA nükleotid dizisinde hiçbir değişiklik olmaksızın gen ifadesinde meydana gelen, "
                "mitotik bölünmeler boyunca kalıtılabilen stabil moleküler değişimleri inceler. Kanser uzun yıllar "
                "yalnızca genetik (mutasyonel) bir hastalık olarak görülmüş olsa da, günümüzde neoplastik dönüşümün "
                "en az genetik kadar **epigenetik bozukluklar** tarafından yönetildiği kanıtlanmıştır. Epigenetik "
                "mekanizmalar temel olarak üç düzeyde işler: DNA metilasyonu, histon proteinlerinin translasyon "
                "sonrası modifikasyonları (asetilasyon, metilasyon, fosforilasyon) ve kodlamayan düzenleyici "
                "RNA'lar (mikroRNA, lncRNA). Genetik mutasyonlar kalıcı ve geri dönüşsüz iken; epigenetik sapmalar "
                "**potansiyel olarak geri döndürülebilir (reversible)** niteliktedir; bu özellik epigenetik ilaç "
                "tedavilerinin (epidrugs) rasyonel temelini oluşturur."
            ),
            "elements": [
                make_before_after(
                    "Genetik Mutasyonlar ile Epigenetik Değişikliklerin Karşılaştırması",
                    "Genetik Mutasyonlar (Ör. Nokta Mutasyon, Delesyon)",
                    "DNA baz dizisi kalıcı olarak değişir. Hasar geriye döndürülemez; mutasyon sonraki tüm hücre nesillerine aktarılır.",
                    "Epigenetik Modifikasyonlar (Ör. DNA Metilasyonu, Histon Asetilasyonu)",
                    "DNA dizisi tamamen normal kalır; kromatin yapısı ve gen erişilebilirliği değişir. Farmakolojik olarak geri döndürülebilir.",
                    "Epigenetik susturmanın geri döndürülebilir olması epigenetik antikanser tedavilerin ana dayanağıdır."
                ),
                make_cloze(
                    "DNA dizisinde değişiklik olmaksızın gen ifadesinin kalıtsal olarak değişmesi olayına epigenetik modifikasyon denir.",
                    "epigenetik",
                    "Genetik ötesi moleküler düzenleme"
                )
            ]
        },

        # Slayt 32
        {
            "slideNumber": 32,
            "title": "Genomda Global DNA Hipometilasyonu",
            "content": (
                "Normal insan somatik hücrelerinde genomun büyük kısmı (tekrarlayan diziler, heterokromatin ve "
                "transpozonlar) yoğun biçimde metillenmiştir; bu durum genomik yapıyı kompakt ve kararlı tutar. "
                "Malign karsinogenezin en erken ve evrensel epigenetik bulgularından biri **global DNA "
                "hipometilasyonudur**. Kanser hücrelerinde tüm genom genelinde 5-metilsitozin içeriği belirgin "
                "şekilde azalır. Tekrarlayan DNA elementlerinin (retrotranspozonlar, LINE, SINE) ve pericentromerik "
                "uydu dizilerinin hipometilasyonu, bu suskun bölgelerin gevşeyerek açılmasına neden olur. Sonuç "
                "olarak transpozonlar genomda serbestçe hareket etmeye başlar, kromozomlar arası anormal rekombinasyonlar "
                "ve kırılmalar tetiklenir; bu olgu doğrudan **kromozomal kararsızlığa (CIN)** yol açar."
            ),
            "elements": [
                make_causal_chain(
                    "Global DNA Hipometilasyonundan Kromozomal Kaosa Gidiş Zinciri",
                    [
                        "1. Metil Verici Tükenişi: Kanser metabolizmasında DNA metiltransferaz regülasyonu ve S-adenozilmetiyonin dengesi bozulur.",
                        "2. Heterokromatinin Gevşemesi: Tekrarlayan pericentromerik diziler ve transpozonlar metil gruplarını kaybeder.",
                        "3. Retrotranspozon Aktivasyonu: Normalde susturulmuş olan LINE ve SINE elemanları transkribe edilerek genoma sıçrar.",
                        "4. Eşleşme Dışı Rekombinasyon: Açık kromatinde homolog olmayan kromozom kolları arasında kırılma ve yapışmalar başlar.",
                        "5. Ağır Kromozomal Kararsızlık: Hücrede translokasyonlar, delesyonlar ve sayısal anöploidi patlak verir."
                    ]
                ),
                make_active_recall(
                    "Kanser hücrelerinde genom genelindeki heterokromatin ve tekrarlayan dizilerin metil kaybetmesi sonucu gelişen epigenetik anormallik nedir?",
                    "Global DNA hipometilasyonudur.",
                    "Genom boyu metil azalması"
                )
            ]
        },

        # Slayt 33
        {
            "slideNumber": 33,
            "title": "Tümör Baskılayıcı Promotör Hipermetilasyonu",
            "content": (
                "Kanser genomunda bir yandan global hipometilasyon yaşanırken; tam tersine gen promotör bölgelerindeki "
                "**CpG adacıkları (CpG islands)** anormal şekilde aşırı metillenir (**lokal hipermetilasyon**). "
                "Normalde aktif genlerin promotörlerindeki CpG adacıkları metilsizdir ve transkripsiyon faktörlerinin "
                "bağlanmasına açıktır. DNA Metiltransferaz (DNMT) enzimlerinin hatalı şekilde bu adacıklardaki sitozin "
                "bazlarına metil grupları eklemesi, kromatini sıkarak transkripsiyon faktörlerinin erişimini bloke "
                "eder; bu duruma **epigenetik gen susturulması (gene silencing)** denir. Kanser hücreleri, mutasyon "
                "veya delesyon yapmaksızın tümör baskılayıcı genleri (ör. **RB1, TP53, MLH1, BRCA1, VHL, CDKN2A/p16**)"
                "yalnızca promotör hipermetilasyonu ile tamamen susturabilirler (Knudson'ın epigenetik darbesi)."
            ),
            "elements": [
                make_table(
                    "Kanserde Karakteristik Olarak Hipermetile Edilen Kilit Genler",
                    ["Susturulan Gen", "Genin Normal Biyolojik Görevi", "Hipermetilasyonun Görüldüğü Malignite"],
                    [
                        {
                            "cells": ["CDKN2A (p16/INK4a)", "Siklin D/CDK4 kompleksini inhibe eden siklus freni", "Kolon, akciğer, serviks ve mesane karsinomları"],
                            "hiddenIndex": 0,
                            "hint": "G1-S fazı siklin bağımlı kinaz inhibitörü"
                        },
                        {
                            "cells": ["MLH1 Geni", "DNA uyuşmazlık onarımı (MMR) enzimi", "Sporadik mikrosatellit instabiliteli kolorektal karsinomlar"],
                            "hiddenIndex": 0,
                            "hint": "Eşleşme tamir kompleksi proteini"
                        },
                        {
                            "cells": ["BRCA1 Geni", "DNA çift iplik kırığı homolog rekombinasyon onarımı", "Sporadik over ve üçlü negatif meme karsinomları"],
                            "hiddenIndex": 0,
                            "hint": "Kalıtsal olmayan meme kanserinde susturulan gen"
                        }
                    ]
                ),
                make_cloze(
                    "Tümör baskılayıcı genlerin promotör bölgelerindeki CpG adacıklarının aşırı metillenerek genin susturulmasına promotör hipermetilasyonu denir.",
                    "hipermetilasyonu",
                    "Promotörde metil grubu yoğunlaşması"
                )
            ]
        },

        # Slayt 34
        {
            "slideNumber": 34,
            "title": "Histon Modifikasyonları ve Epigenetik Kod",
            "content": (
                "Ökaryotik DNA, oktamerik histon çekirdek proteinleri (H2A, H2B, H3, H4) etrafına sarılarak "
                "nükleozomları meydana getirir. Histon proteinlerinin amino-terminal uçlarındaki lizin ve arjinin "
                "kuyrukları, kromatini gevşeten veya sıkıştıran kovalent kimyasal modifikasyonlara uğrar. **Histon "
                "Asetiltransferazlar (HAT)** lizin rezidülerine asetil ekleyerek pozitif yükü nötralize eder; "
                "DNA-histon etkileşimi gevşer ve kromatin transkripsiyona açık aktif form olan **ökromatine** "
                "dönüşür. Buna karşılık **Histon Deasetilazlar (HDAC)** asetil gruplarını kopararak kromatini "
                "yoğunlaştırır ve transkripsiyonu kapatan sessiz **heterokromatine** çevirir. Kanser hücrelerinde "
                "tümör baskılayıcı gen bölgelerinde aşırı HDAC aktivitesi ve Histon H3 Lizin 27 trimetilasyonu "
                "(H3K27me3) saptanır; bu durum baskılayıcı genlerin susturulmasını perçinler."
            ),
            "elements": [
                make_before_after(
                    "Histon Asetilasyonu (Açık) ile Deasetilasyonunun (Kapalı) Etkisi",
                    "Histon Asetilasyonu (HAT Enzimleri)",
                    "Lizin kuyrukları asetillenir, pozitif yük nötralize olur. Kromatin gevşer (ökromatin), transkripsiyon faktörleri DNA'ya bağlanır.",
                    "Histon Deasetilasyonu (HDAC Enzimleri)",
                    "Asetil grupları sökülür, histonlar DNA'yı sıkıca sarar. Kromatin yoğunlaşır (heterokromatin), gen ekspresyonu tamamen durur.",
                    "HDAC inhibitörleri kanserde kromatini gevşeterek baskılanmış tümör baskılayıcı genleri yeniden uyandırır."
                ),
                make_active_recall(
                    "Histon kuyruklarındaki asetil gruplarını uzaklaştırarak kromatini yoğunlaştıran ve gen susturulmasına yol açan enzim ailesi hangisidir?",
                    "Histon Deasetilazlar (HDAC) enzim ailesidir.",
                    "Asetil koparan nükleer enzimler"
                )
            ]
        },

        # Slayt 35
        {
            "slideNumber": 35,
            "title": "Epigenetik Tedaviler: DNMT ve HDAC İnhibitörleri",
            "content": (
                "Epigenetik hasarların farmakolojik olarak tersine çevrilebilir olması, onkolojide 'epigenetik "
                "tedavi' sınıfını doğurmuştur. Birinci grup **DNA Metiltransferaz (DNMT) İnhibitörleridir (5-Azasitidin "
                "ve Desitabin)**. Sitozin analoğu olan bu moleküller, DNA replikasyonu sırasında zincire entegre "
                "olur ve DNMT enzimini kovalent olarak yakalayarak parçalar. Böylece hücre bölündükçe tümör baskılayıcı "
                "promotörlerindeki hipermetilasyon silinir ve p16 gibi genler yeniden uyanır; miyelodisplastik sendrom "
                "(MDS) ve AML'de standart tedavidir. İkinci grup ise **Histon Deasetilaz (HDAC) İnhibitörleridir "
                "(Vorinostat, Romidepsin)**; histonların asetilli kalarak kromatinin açık durmasını sağlarlar ve "
                "kutanöz T hücreli lenfomada (mikozis fungoides) apoptozu indüklemek için kullanılırlar."
            ),
            "elements": [
                make_table(
                    "Klinikte Kullanılan Başlıca Epigenetik Ajanlar",
                    ["İlaç Grubu", "Prototipik Moleküller", "Moleküler Etki Mekanizması", "Onaylı Endikasyon"],
                    [
                        {
                            "cells": ["DNMT İnhibitörleri", "5-Azasitidin, Desitabin", "DNA metilasyonunu silerek susturulmuş genleri açma", "Miyelodisplastik Sendrom (MDS) ve AML"],
                            "hiddenIndex": 1,
                            "hint": "Sitozin analoğu demetilleme molekülleri"
                        },
                        {
                            "cells": ["HDAC İnhibitörleri", "Vorinostat, Romidepsin", "Histon deasetilasyonunu engelleyip kromatini açık tutma", "Kutanöz T Hücreli Lenfoma (KTCL)"],
                            "hiddenIndex": 1,
                            "hint": "Deasetilazı durduran lenfoma ajanları"
                        }
                    ]
                ),
                make_cloze(
                    "Miyelodisplastik sendromda DNA metilasyonunu bloke ederek tümör baskılayıcı genlerin ifadesini geri kazandıran ilaç 5-Azasitidin molekülüdür.",
                    "5-Azasitidin",
                    "Demetilasyon sağlayan pirimidin analoğu"
                )
            ]
        },

        # Slayt 36
        {
            "slideNumber": 36,
            "title": "MikroRNA Biyogenezi ve Karsinogenezdeki Rolü",
            "content": (
                "**MikroRNA'lar (miRNA)**, yaklaşık 21-25 nükleotid uzunluğunda, protein kodlamayan, tek sarmallı "
                "küçük RNA molekülleridir. Nükleusta RNA Polimeraz II tarafından pri-miRNA olarak üretilir, **Drosha** "
                "enzimiyle pre-miRNA'ya kesilir ve Exportin-5 ile sitoplazmaya taşınır. Sitoplazmada **Dicer** "
                "endonükleazı tarafından olgun çift sarmallı forma çevrilir ve **RISC (RNA-İndüklenen Susturma "
                "Kompleksi)** içine yüklenir. miRNA'lar hedef haberci RNA'ların (mRNA) 3' çevrilmeyen bölgelerine "
                "(3'-UTR) kısmi baz eşleşmesi ile bağlanırlar. Bağlanma sonucunda hedef mRNA ya doğrudan parçalanır "
                "ya da ribozomda translasyonu bloke edilir. İnsan genomundaki protein kodlayan genlerin %60'ından "
                "fazlasının ifadesi mikroRNA'lar tarafından negatif olarak regüle edilir."
            ),
            "elements": [
                make_causal_chain(
                    "MikroRNA Biyogenezi ve mRNA Susturma Kaskadı",
                    [
                        "1. Nükleer Transkripsiyon: Genomik DNA'dan saç tokası yapısında pri-miRNA transkribe edilir.",
                        "2. Drosha/DGCR8 Kesimi: Çekirdekte pri-miRNA öncül pre-miRNA formuna kırpılır.",
                        "3. Sitoplazmaya İhracat: Pre-miRNA Exportin-5 taşıyıcısı ile nükleer porlardan sitoplazmaya aktarılır.",
                        "4. Dicer ile Olgunlaşma: Dicer enzimi ilmek kısmını keserek 22 bazlık çift sarmal miRNA üretir.",
                        "5. RISC Kompleksi Kenetlenmesi: Kılavuz miRNA ipliği RISC ile hedef mRNA'nın 3'-UTR bölgesini yıkar veya bloke eder."
                    ]
                ),
                make_active_recall(
                    "Sitoplazmada pre-miRNA'yı keserek fonksiyonel olgun mikroRNA çift sarmalını üreten temel endonükleaz enzimi hangisidir?",
                    "Dicer endonükleazıdır.",
                    "Zar kesici RNAaz enzimi"
                )
            ]
        },

        # Slayt 37
        {
            "slideNumber": 37,
            "title": "Onkojenik MikroRNA'lar (Onkomirler)",
            "content": (
                "MikroRNA'ların kanser patogenezindeki etkisi hedefledikleri mRNA'nın niteliğine bağlıdır ve iki "
                "zıt grupta incelenirler. Birinci grup **Onkomirlerdir (Onkojenik miRNA'lar)**. Eğer bir miRNA "
                "tümör baskılayıcı bir genin mRNA'sını hedef alıp susturuyorsa, bu miRNA'nın aşırı ifadesi kansere "
                "yol açar. Prototipik onkomir **miR-21**'dir; glioblastom, meme ve kolon kanserinde aşırı üretilerek "
                "PTEN ve PDCD4 tümör baskılayıcılarını yıkar ve apoptozu engeller. İkinci grup ise **Tümör Baskılayıcı "
                "miRNA'lardır**; bu moleküller normalde onkogenlerin mRNA'sını baskılarlar. En klasik örnek **miR-15 "
                "ve miR-16** ailesidir. Normalde BCL2 onkogenini frenleyen miR-15a/16-1 kümesi 13q14 lokusunda "
                "yer alır; Kronik Lenfositik Lösemide (KLL) bu bölge delesyonla kaybedilince BCL2 freni kalkar ve "
                "lösemik B hücreleri birikir."
            ),
            "elements": [
                make_table(
                    "Onkomir vs Tümör Baskılayıcı miRNA Dinamikleri",
                    ["miRNA Sınıfı", "Kanser Hücresindeki Durumu", "Hedeflediği Molekül", "Klinik Patolojik Örnek"],
                    [
                        {
                            "cells": ["Onkomir (Ör. miR-21)", "Aşırı ekspresyon (Artış)", "Tümör baskılayıcılar (PTEN, PDCD4)", "Glioblastoma ve meme karsinomu"],
                            "hiddenIndex": 0,
                            "hint": "Onkojenik fonksiyon kazanan mikroRNA"
                        },
                        {
                            "cells": ["Tümör Baskılayıcı miRNA", "Delesyon veya susturulma (Kayıp)", "Onkogenler (BCL2, RAS)", "KLL'de 13q14 kaybı ve miR-15/16 silinmesi"],
                            "hiddenIndex": 0,
                            "hint": "Kaybedildiğinde onkogeni serbest bırakan grup"
                        }
                    ]
                ),
                make_micro_quiz(
                    "Kronik lenfositik lösemi (KLL) olgularında 13q14 delesyonu ile kaybedilen ve BCL2 antiapoptotik onkogeninin aşırı üretilmesine yol açan tümör baskılayıcı mikroRNA kümesi hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "miR-21",
                            "isCorrect": False,
                            "explanation": "miR-21 bir onkomir olup PTEN'i baskılar."
                        },
                        {
                            "key": "B",
                            "text": "miR-15a ve miR-16-1 kümesi",
                            "isCorrect": True,
                            "explanation": "13q14 delesyonunda miR-15a/16-1 kaybı BCL2 üzerindeki negatif kontrolü kaldırarak KLL'yi tetikler."
                        },
                        {
                            "key": "C",
                            "text": "miR-155",
                            "isCorrect": False,
                            "explanation": "miR-155 lenfomalarda aşırı üretilen bir onkomirdir."
                        },
                        {
                            "key": "D",
                            "text": "let-7",
                            "isCorrect": False,
                            "explanation": "let-7 RAS onkogenini baskılayan bir diğer baskılayıcıdır ancak 13q14'te yerleşmez."
                        }
                    ],
                    "miR-15 ve miR-16 BCL2'nin fizyolojik frenleyicileridir."
                )
            ]
        },

        # Slayt 38
        {
            "slideNumber": 38,
            "title": "Uzun Kodlamayan RNA'lar (lncRNA) ve Epigenetik İskelet",
            "content": (
                "**Uzun kodlamayan RNA'lar (lncRNA)**, 200 nükleotidden daha uzun olan ve proteine çevrilmeyen "
                "transkriptlerdir. miRNA'lardan farklı olarak lncRNA'lar moleküler bir 'iskelet' (scaffold) gibi "
                "davranarak kromatin düzenleyici enzim komplekslerini spesifik genomik lokuslara yönlendirirler. "
                "Kanser biyolojisinde en iyi tanımlanmış lncRNA **HOTAIR**'dir (HOX Transcript Antisense RNA). "
                "HOTAIR, histon metiltransferaz kompleksi olan **PRC2'ye (Polikomb Represif Kompleks 2)** bağlanarak "
                "onu tümör baskılayıcı genlerin promotörlerine taşır ve H3K27me3 oluşturarak bu genleri kalıcı "
                "olarak susturur. Meme ve kolorektal karsinomlarda aşırı HOTAIR ekspresyonu yaygın metastaz ve kötü "
                "prognozla doğrudan ilişkilidir. Bir diğer majör lncRNA olan **MALAT1** ise alternatif uç birleştirmeyi "
                "(splicing) etkileyerek akciğer kanseri metastazını tetikler."
            ),
            "elements": [
                make_cloze(
                    "PRC2 enzim kompleksini tümör baskılayıcı promotörlere taşıyarak metastazı tetikleyen uzun kodlamayan RNA molekülü HOTAIR transkriptidir.",
                    "HOTAIR",
                    "Hox antisens uzun kodlamayan RNA"
                ),
                make_active_recall(
                    "Uzun kodlamayan RNA'ların (lncRNA) mikroRNA'lardan temel yapısal farkı nedir?",
                    "200 nükleotidden daha uzun olmaları ve kromatin modifiye edici protein komplekslerine iskele görevi görmeleridir.",
                    "Baz uzunluğu ve moleküler çatı vazifesi"
                )
            ]
        },

        # Slayt 39: CHECKPOINT 4
        {
            "slideNumber": 39,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Kanser Epigenetiği ve MikroRNA'lar",
            "content": (
                "Dördüncü bölümün bu tekrar sayfasında, DNA dizisi değişmeksizin gen ekspresyonunu değiştiren "
                "epigenetik mekanizmalar özetlenmektedir. Kanser genomunda global DNA hipometilasyonu tekrarlayan "
                "dizileri açarak kromozomal kararsızlığa yol açarken; tümör baskılayıcı promotörlerdeki lokal "
                "CpG hipermetilasyonu CDKN2A (p16), MLH1 ve BRCA1 gibi genleri sessizliğe gömer. Histon deasetilazlar "
                "(HDAC) kromatini sıkıştırır; DNMT ve HDAC inhibitörleri (5-Azasitidin, Vorinostat) bu susturmayı "
                "geri döndürür. MikroRNA'lar Dicer ile olgunlaşıp RISC kompleksiyle mRNA'ları yıkar; miR-21 "
                "prototipik onkomir, KLL'de silinen miR-15/16 ise tümör baskılayıcıdır. HOTAIR gibi lncRNA'lar "
                "ise PRC2'yi yönlendirerek epigenetik susturmayı yönetir."
            ),
            "flashcards": [
                {
                    "id": "k1-29-cp04-fc01",
                    "front": "Kanser hücrelerinde tümör baskılayıcı gen promotörlerindeki CpG adacıklarının aşırı metillenmesi gen ifadesini nasıl etkiler?",
                    "back": "Kromatini kapatarak genin transkripsiyonunu durdurur (epigenetik susturma).",
                    "hint": "Promotör erişiminin kilitlenmesi"
                },
                {
                    "id": "k1-29-cp04-fc02",
                    "front": "Miyelodisplastik sendromda DNA metilasyonunu engelleyerek susturulmuş tümör baskılayıcı genleri açan prototipik DNMT inhibitörü ilaç nedir?",
                    "back": "5-Azasitidin (veya Desitabin) ilacıdır.",
                    "hint": "Pirimidin analoğu demetilleyici ajan"
                },
                {
                    "id": "k1-29-cp04-fc03",
                    "front": "Tümör baskılayıcı bir genin mRNA'sını yıkarak kanser gelişimini destekleyen aşırı aktif mikroRNA'lara genel olarak ne ad verilir?",
                    "back": "Onkomir (Onkojenik mikroRNA) adı verilir.",
                    "hint": "Habis karakterli düzenleyici RNA grubu"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 4 Özet Tablosu: Epigenetik Mekanizmalar",
                    ["Epigenetik Olay", "Moleküler Araç", "Tümördeki Biyolojik Yansıma"],
                    [
                        {
                            "cells": ["Promotör Susturulması", "CpG hipermetilasyonu ve DNMT", "Tümör baskılayıcı genlerin ifadesiz kalması"],
                            "hiddenIndex": 0,
                            "hint": "Gen başlangıcının metillenerek kapatılması"
                        },
                        {
                            "cells": ["Onkomir Baskısı", "miR-21 aşırı ekspresyonu", "PTEN gibi koruyucu faktörlerin mRNA yıkımı"],
                            "hiddenIndex": 0,
                            "hint": "Onkojenik küçük susturucu RNA"
                        }
                    ]
                )
            ]
        },

        # Slayt 40
        {
            "slideNumber": 40,
            "title": "Klinik Karar: Kolorektal Kanserde CIMP ve Epigenetik Belirteçler",
            "content": (
                "Kolorektal karsinomların yaklaşık %15-20'si klasik kromozomal instabilite (CIN) yoluyla değil, "
                "**CpG Adası Metilatör Fenotipi (CIMP)** adı verilen epigenetik bir yolla gelişir. CIMP pozitif "
                "tümörlerde birden fazla gen promotörü aynı anda yaygın hipermetilasyona uğrar. Eğer bu genler "
                "arasında DNA tamir geni **MLH1** yer alıyorsa, MLH1 epigenetik olarak susturulur ve sporadik "
                "**Mikrosatellit İnstabilitesi (MSI-High)** tablosu doğar. Patolog kolorektal biyopsi materyalinde "
                "immünohistokimya ile MLH1 kaybı saptadığında; bunun kalıtsal Lynch sendromu mu yoksa sporadik CIMP "
                "aracılı hipermetilasyon mu olduğunu ayırt etmek için **BRAF V600E mutasyonu** ve **MLH1 promotör "
                "hipermetilasyon testi** ister. BRAF mutasyonu ve metilasyon varlığı olayın sporadik olduğunu kanıtlar."
            ),
            "elements": [
                make_branching_logic(
                    "68 yaşında kadın hastada çekum yerleşimli müsinöz adenokarsinom rezeke ediliyor. İmmünohistokimyasal taramada tümör hücrelerinde MLH1 ve PMS2 nükleer ekspresyonunun tamamen kaybolduğu izleniyor. Onkoloji konseyi olgunun Lynch sendromu mu yoksa sporadik CIMP ilişkili mi olduğunu sorguluyor.",
                    "Hastayı ve ailesini gereksiz genetik taramalardan korumak ve tümörün sporadik CIMP kökenli olduğunu kanıtlamak için patoloğun öncelikle uygulayacağı moleküler algoritma ne olmalıdır?",
                    [
                        {
                            "text": "Tümör dokusunda BRAF V600E mutasyonu ve MLH1 promotör hipermetilasyonu araştırılmalıdır; pozitiflik sporadik CIMP'yi kanıtlar ve Lynch sendromunu dışlar.",
                            "isCorrect": True,
                            "explanation": "Lynch sendromunda BRAF mutasyonu görülmez. BRAF V600E ve MLH1 promotör hipermetilasyonu tümörün sporadik CIMP zemininde geliştiğinin kesin kanıtıdır."
                        },
                        {
                            "text": "MLH1 kaybı görülen her hasta kesinlikle Lynch sendromu kabul edilmeli ve hastanın tüm torunlarına acil kolonoskopi yapılmalıdır.",
                            "isCorrect": False,
                            "explanation": "MLH1 kayıplarının çoğu sporadik CIMP hipermetilasyonuna bağlıdır, kalıtsal değildir."
                        },
                        {
                            "text": "Tümör dokusuna Philadelphia kromozomu analizi yapılmalıdır.",
                            "isCorrect": False,
                            "explanation": "Philadelphia KML belirtecidir, kolon kanseriyle ilgisi yoktur."
                        }
                    ]
                ),
                make_micro_quiz(
                    "Kolon kanserinde MLH1 geninin promotör hipermetilasyonu sonucu susturulması ve sporadik mikrosatellit instabilitesi gelişimi hangi moleküler fenotipin sonucudur?",
                    [
                        {
                            "key": "A",
                            "text": "CIMP (CpG Adası Metilatör Fenotipi)",
                            "isCorrect": True,
                            "explanation": "CIMP fenotipi yaygın promotör CpG hipermetilasyonu ile MLH1'i susturarak sporadik MSI kolon kanserlerine yol açar."
                        },
                        {
                            "key": "B",
                            "text": "CIN (Kromozomal İnstabilite Yolu)",
                            "isCorrect": False,
                            "explanation": "CIN yolu APC mutasyonu ve anöploidi ile seyreder (%80 klasik yol)."
                        },
                        {
                            "key": "C",
                            "text": "Homolog Rekombinasyon Kusuru",
                            "isCorrect": False,
                            "explanation": "Homolog rekombinasyon kusuru BRCA ilişkili meme-over kanserlerinde görülür."
                        },
                        {
                            "key": "D",
                            "text": "Nükleotid Eksizyon Onarım Kusuru",
                            "isCorrect": False,
                            "explanation": "NER kusuru kseroderma pigmentozum zeminidir."
                        }
                    ],
                    "CIMP yolu epigenetik promotör hipermetilasyonu ile seyreder."
                )
            ]
        }
    ]
