# -*- coding: utf-8 -*-
"""
Deck 61 Section 1: Tanım, İnsidans ve Risk Faktörleri
Slides 1-10 (Checkpoint 1 at slide 10)
Focus:
- Spontan abortus tanımı: 20 hafta öncesi, <500 gram
- Erken abortus (ilk 12 hafta) vs Geç abortus (13-20. hafta)
- Genel insidans (%15-20), klinik tanınan gebeliklerde insidans (%10-12)
- Düşüklerin %80'inin ilk trimesterde gerçekleşmesi
- İlk 8 haftada en yüksek risk dönemi
- Yaşam tarzı riskleri (sigara, alkol, aşırı kafein)
- Etnik ve demografik riskler (Afrika kökenli olmak, ileri anne yaşı)
- Anamnez riskleri (önceki EPL ve ölü doğum öyküsü)
- Medikal riskler (diyabet, yardımcı üreme teknikleri, kanama)
- Checkpoint 1
"""

from meds.scripts.deck_generators.deck61.deck61_helper import (
    make_slide,
    make_quiz,
    make_cloze,
    make_table,
    make_chain,
    make_recall,
    make_spot_the_lie,
    make_slider,
    make_swipe,
    make_branching,
    make_venn
)

def get_sec1_slides():
    slides = []

    # Slide 1
    slides.append(make_slide(
        slide_num=1,
        title="Spontan Abortus: Tanım, Gestasyonel Hafta ve Ağırlık Kriterleri",
        subtitle="20. gebelik haftası ve 500 gram sınırı",
        clinical_focus="Erken gebelik kaybının yasal ve tıbbi obstetrik tanımı",
        narrative=(
            "Obstetrik terminolojide **spontan abortus (düşük)**, viabilite sınırına ulaşmamış bir gebeliğin kendiliğinden sonlanmasını ifade eder.\n\n"
            "- **Resmi Tanım Kriterleri:** Gebeliğin **ilk 20 haftası içinde**, ağırlığı **500 gramdan küçük** olan embriyo veya fetüsün ve eklerinin (plasenta, membranlar) tamamının ya da bir kısmının uterus kavitesi dışına atılmasıdır.\n"
            "- **Fetal Ağırlık Eşiği:** 500 gram sınırı Dünya Sağlık Örgütü (DSÖ) tarafından belirlenen standart viabilite eşiğidir. 20. haftadan sonra veya 500 gramın üzerindeki fetal kayıplar abortus değil, **ölü doğum (intrauterin fetal eksitus)** veya erken preterm doğum olarak adlandırılır.\n"
            "- **Klinik Yansıması:** Acil servise kanama ile başvuran hastada son adet tarihine göre gebelik haftasının 20 haftanın altında olduğunun teyidi abortus protokollerinin başlatılmasında ilk adımdır.\n\n"
            "> [!IMPORTANT]\n"
            "> İlk 20 gebelik haftasından önce ve 500 gramdan küçük embriyo/fetüsün uterus dışına atılması spontan abortus olarak tanımlanır."
        ),
        bullets=[
            "Abortus sınırı: İlk 20 gebelik haftası ve 500 gramdan küçük fetal ağırlıktır",
            "Embriyo/fetüs ve eklerinin tamamı veya bir kısmı uterus kavitesi dışına atılır",
            "20 hafta veya 500 gram üzerindeki kayıplar ölü doğum (fetal eksitus) kabul edilir",
            "İlk trimester acil kanamalarında obstetrik yaklaşımın temel başlangıç tanımıdır"
        ],
        elements=[
            make_quiz(
                question="Obstetrik pratikte bir gebelik kaybının 'spontan abortus' olarak tanımlanabilmesi için kabul edilen gebelik haftası ve fetal ağırlık üst sınırları hangisinde eksiksiz verilmiştir?",
                options=[
                    {"key": "A", "text": "İlk 20 gebelik haftasından önce ve 500 gramdan küçük olması", "isCorrect": True, "explanation": "Doğru. Abortusun klasik obstetrik tanımı ilk 20 hafta ve 500 gram altındaki kayıplardır."},
                    {"key": "B", "text": "İlk 24 gebelik haftasından önce ve 1000 gramdan küçük olması", "isCorrect": False, "explanation": "24 hafta viabilite sınırıdır; klasik abortus tanımı 20 haftadır."},
                    {"key": "C", "text": "İlk 12 gebelik haftasından önce ve 250 gramdan küçük olması", "isCorrect": False, "explanation": "İlk 12 hafta erken abortusu tanımlar; genel sınır 20 haftadır."},
                    {"key": "D", "text": "İlk 28 gebelik haftasından önce ve 750 gramdan küçük olması", "isCorrect": False, "explanation": "28 hafta 3. trimester başlangıcıdır; abortus değildir."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="İlk 20 gebelik haftasından önce ve 500 gramdan hafif embriyo veya fetüsün uterus dışına atılmasına spontan abortus denir.",
                masked_term="spontan abortus",
                hint="Erken dönemde viabilite öncesi kendiliğinden gebelik kaybı terimi"
            ),
            make_slider(
                left_title="Spontan Abortus (Düşük)",
                right_title="İntrauterin Ölü Doğum (Fetal Eksitus)",
                left_points=[
                    "Gebeliğin ilk 20 haftası içinde gerçekleşir",
                    "Fetal ağırlık 500 gramın altındadır",
                    "Etiyolojide kromozomal genetik anomaliler baskındır"
                ],
                right_points=[
                    "Gebeliğin 20. haftasından sonra meydana gelir",
                    "Fetal ağırlık 500 gram ve üzerindedir",
                    "Kordon kazaları, plasenta dekolmanı ve maternal hastalıklar ön plandadır"
                ]
            ),
            make_recall(
                question="Dünya Sağlık Örgütü ve obstetrik cemiyetlerin abortus tanımında 500 gram ağırlık ve 20 hafta sınırını koymalarının temel fizyolojik gerekçesi nedir?",
                answer="Bu sınırın altındaki fetüslerin akciğer ve organ matürasyonu açısından uterus dışında yaşama yeteneğinin (ekstrauterin viabilite) bulunmamasıdır."
            )
        ]
    ))

    # Slide 2
    slides.append(make_slide(
        slide_num=2,
        title="Erken Abortus vs Geç Abortus: Trimester Ayrımı",
        subtitle="İlk 12 hafta (1. trimester) ile 13-20. haftalar (2. trimester) farkı",
        clinical_focus="Etiyoloji ve klinik yaklaşımı değiştiren gestasyonel zamanlama",
        narrative=(
            "Spontan düşükler olayın gerçekleştiği gestasyonel haftaya göre iki temel evreye ayrılır ve bu ayrım etiyolojik araştırmanın yönünü tamamen belirler.\n\n"
            "- **Erken Abortus (1. Trimester):** Gebeliğin **ilk 12 haftası** içinde meydana gelen kayıplardır. Erken gebelik kaybı (EPL) olarak da adlandırılır. Tüm spontan düşüklerin ezici çoğunluğunu oluşturur ve etiyolojisinde fetal kromozomal genetik bozukluklar (%50-70) başrol oynar.\n"
            "- **Geç Abortus (2. Trimester):** Gebeliğin **13 ile 20. haftaları arasında** gerçekleşen kayıplardır. Bu evrede kromozomal anomalilerin payı belirgin şekilde azalır (%30 civarına düşer); buna karşılık maternal anatomik kusurlar (servikal yetmezlik, uterin septum), antifosfolipid sendromu, sistemik hastalıklar ve enfeksiyonlar ön plana geçer.\n\n"
            "> [!NOTE]\n"
            "> İlk 12 haftadaki kayıplar erken abortustur ve genetik kökenlidir; 13-20. haftalardaki kayıplar geç abortustur ve maternal/anatomik nedenler ağır basar."
        ),
        bullets=[
            "İlk 12 hafta içindeki kayıplar: Erken abortus (erken gebelik kaybı - EPL)",
            "13-20. haftalar arasındaki kayıplar: Geç abortus (ikinci trimester abortusu)",
            "Erken abortuslarda fetal kromozomal anomaliler (%70) baskındır",
            "Geç abortuslarda servikal yetmezlik, enfeksiyon ve maternal faktörler öne çıkar"
        ],
        elements=[
            make_quiz(
                question="15 haftalık gebe bir kadında servikal açıklık ve membran rüptürü sonrası gebelik kaybı meydana geliyor. Bu klinik tablo gebelik haftasına göre hangi grupta sınıflandırılır ve etiyolojide hangisi ilk trimester kayıplarına kıyasla daha sık rol oynar?",
                options=[
                    {"key": "A", "text": "Erken abortus — Trizomi 16 anomalisi", "isCorrect": False, "explanation": "15. hafta geç abortustur; trizomiler ilk trimesterde daha sıktır."},
                    {"key": "B", "text": "Geç abortus — Maternal anatomik ve servikal faktörler", "isCorrect": True, "explanation": "Doğru. 13-20. hafta arası geç abortustur; genetikten ziyade servikal yetmezlik ve anatomik faktörler baskındır."},
                    {"key": "C", "text": "Ölü doğum — Akut kord dolanması", "isCorrect": False, "explanation": "20 haftadan önce ölü doğum denmez; abortustur."},
                    {"key": "D", "text": "Missed abortus — Paternal dengeli translokasyon", "isCorrect": False, "explanation": "Düşük materyali atılmıştır; missed değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Gebeliğin on üçüncü haftası ile yirminci haftası arasında gerçekleşen fetal kayıplar geç abortus olarak adlandırılır.",
                masked_term="geç abortus",
                hint="İkinci trimesterde gerçekleşen düşük kategorisi"
            ),
            make_table(
                title="Erken ve Geç Abortus Karşılaştırmalı Özellikleri",
                headers=["Kriter", "Erken Abortus", "Geç Abortus"],
                rows=[
                    [
                        {"text": "Gebelik Haftası Aralığı", "isMasked": False},
                        {"text": "İlk 12 gebelik haftası", "isMasked": True, "hint": "Birinci trimester dönemi"},
                        {"text": "13-20. gebelik haftaları", "isMasked": False}
                    ],
                    [
                        {"text": "Baskın Etiyolojik Neden", "isMasked": False},
                        {"text": "Fetal kromozomal anomaliler (%70)", "isMasked": True, "hint": "Genetik anöploidiler"},
                        {"text": "Maternal anatomik, enfeksiyöz ve servikal yetmezlik", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Birinci trimester düşüğü ile ikinci trimester düşüğü araştırılırken klinisyenin tanısal test önceliği nasıl farklılaşır?",
                answer="İlk trimester düşüğünde fetal genetik/sitogenetik analiz ön plandayken, ikinci trimester düşüğünde maternal servikal uzunluk, uterin anatomi ve antifosfolipid antikor testleri ön plana geçer."
            )
        ]
    ))

    # Slide 3
    slides.append(make_slide(
        slide_num=3,
        title="Spontan Abortus İnsidansı ve Trimester Dağılımı",
        subtitle="Tüm gebeliklerde %15-20, klinik gebeliklerde %10-12 sıklık",
        clinical_focus="Toplumda düşük sıklığı ve ilk trimester yığılması",
        narrative=(
            "Spontan abortus insan üremesinde en sık karşılaşılan gebelik komplikasyonudur; ancak gerçek insidansı tanı anına göre farklılık gösterir.\n\n"
            "- **Genel ve Klinik İnsidans:** Subklinik (biyokimyasal) implantasyon kayıpları dahil edildiğinde **tüm gebeliklerin yaklaşık %15-20'si** spontan abortus ile sonuçlanır. Ultrason veya fizik muayene ile klinik olarak tanınmış gebeliklerde ise bu oran **%10-12** civarındadır.\n"
            "- **İlk Trimester Yığılması:** Spontan düşüklerin **%80'i ilk trimesterde (ilk 12 haftada)** gerçekleşir. Bu erken kayıpların en az **%50'si doğrudan fetal kromozom anomalileri** ile ilişkilidir.\n"
            "- **Zaman Bağımlı Eğri:** Gebelik haftası ilerledikçe düşük insidansı hızla düşer; özellikle ultrasonda fetal kalp aktivitesi pozitif olarak belgelendikten sonra abortus riski belirgin şekilde azalır.\n\n"
            "> [!IMPORTANT]\n"
            "> Klinik olarak tanınan gebeliklerin %10-12'si düşer; spontan düşüklerin %80'i ilk trimesterdedir ve bunların yarısı kromozomaldir."
        ),
        bullets=[
            "Tüm gebeliklerin %15-20'si; klinik tanınan gebeliklerin %10-12'si düşükle biter",
            "Tüm spontan abortusların %80'i ilk trimesterde meydana gelir",
            "İlk trimester düşüklerinin yaklaşık %50'sinde kromozomal anomali saptanır",
            "Fetal kalp atımı izlendikten sonra düşük riski dramatik olarak azalır"
        ],
        elements=[
            make_quiz(
                question="Spontan abortusların gestasyonel trimester dağılımı ve genetik altyapısı incelendiğinde aşağıdaki oranlardan hangisi tıbbi literatür verileriyle tam uyumludur?",
                options=[
                    {"key": "A", "text": "Düşüklerin %20'si ilk trimesterde olur ve genetik nedenler %5'tir.", "isCorrect": False, "explanation": "Yanlış. Tam tersi; düşüklerin %80'i ilk trimesterde olur ve %50'si genetiktir."},
                    {"key": "B", "text": "Düşüklerin %50'si ikinci trimesterde olur ve tümü servikal yetmezliğe bağlıdır.", "isCorrect": False, "explanation": "İkinci trimester düşükleri azınlıktadır (%20)."},
                    {"key": "C", "text": "Spontan düşüklerin %80'i ilk trimesterde görülür ve bunların yaklaşık %50'si kromozom anomalileri ile ilişkilidir.", "isCorrect": True, "explanation": "Doğru. Düşüklerin ezici çoğunluğu (%80) ilk trimesterdedir ve yarısında kromozomal defekt bulunur."},
                    {"key": "D", "text": "Klinik tanınan gebeliklerin %50'si ilk 4 haftada spontan düşer.", "isCorrect": False, "explanation": "Klinik gebeliklerde oran %10-12'dir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Spontan düşüklerin yüzde sekseni ilk trimesterde görülür ve bu kayıpların yarısı fetal kromozom anomalilerine bağlıdır.",
                masked_term="yüzde sekseni",
                hint="Düşüklerin ilk üç ayda gerçekleşen ezici çoğunluk oranı"
            ),
            make_chain(
                title="Gestasyonel Süreçte Abortus Riskinin Zamansal Azalma Seyri",
                steps=[
                    "1. İmplantasyon Dönemi: Döllenmiş ovumun tutunması sırasında en yüksek biyokimyasal kayıp oranı görülür.",
                    "2. İlk 8 Hafta: Klinik düşük riskinin tepe noktaya (%80'lik payın merkezi) ulaştığı evredir.",
                    "3. Fetal Kalp Tespiti: Ultrasonda canlı fetal kalp atımı pozitifleştiğinde düşük riski %5'in altına geriler.",
                    "4. İkinci Trimester: 12. haftadan sonra genetik kayıplar minimalize olur; düşük riski %1-2 seviyesine iner."
                ]
            ),
            make_recall(
                question="Klinikte 8 haftalık bir gebede ultrasonda güçlü fetal kalp atımı (FKA) saptandığında, bu hastanın abortus riski hakkında aileye nasıl güven verici bir istatistik verilebilir?",
                answer="Fetal kalp atımı pozitif olarak belgelendikten sonra, ek bir maternal risk faktörü yoksa spontan abortus riskinin %3-5 seviyelerine kadar düştüğü söylenebilir."
            )
        ]
    ))

    # Slide 4
    slides.append(make_slide(
        slide_num=4,
        title="İlk 8 Hafta Kuralı ve Genetik Bozuklukların Dinamiği",
        subtitle="Risk ilk 8 haftada en yüksektir; gebelik ilerledikçe genetik etki azalır",
        clinical_focus="Fetal organogenez evresinde ölümcül mutasyonların elenmesi",
        narrative=(
            "İnsan embriyogenezinde doğal seleksiyon en sert şekilde ilk haftalarda çalışır. Spontan abortus riski gebelik süreci boyunca sabit kalmaz; belirgin bir zaman bağımlı eğri çizer.\n\n"
            "- **En Yüksek Risk Aralığı:** Abortus riski **ilk 8 gebelik haftasında en yüksektir**. Embriyonik hücre bölünmelerinin ve majör organ taslaklarının oluştuğu bu evrede, ölümcül genomik defektler embriyonun yaşamını sürdürmesine izin vermez.\n"
            "- **Genetik Bozuklukların Azalma Prensibi:** Gebelik haftası ilerledikçe, genetik bozukluklara bağlı düşüklerin oranı ve genel düşük insidansı hızla azalır. Yani erken kayıplarda genetik anomalilerin etkisi maksimumdur; fetüs büyüdükçe hayatta kalabilen kromozomal anomalili fetüsler (Trizomi 21 gibi) doğuma kadar ulaşabilir.\n"
            "- **8. Hafta Eşiği:** 8. gebelik haftasından sonra embriyonik dönem tamamlanıp fetal dönem başladığında düşük eğrisi dik bir iniş gösterir.\n\n"
            "> [!NOTE]\n"
            "> Düşük riski ilk 8 haftada en yüksektir; gebelik ilerledikçe genetik bozukluklara bağlı düşükler ve düşük insidansı azalır."
        ),
        bullets=[
            "Spontan abortus riski ilk 8 gebelik haftasında tepe noktadadır",
            "Gebelik süreci ilerledikçe genetik bozukluklara bağlı düşükler hızla azalır",
            "Erken kayıplarda genetik anöploidilerin payı belirgin şekilde daha fazladır",
            "8. haftadan sonra fetal döneme geçişle birlikte kayıp riski dik bir düşüş gösterir"
        ],
        elements=[
            make_quiz(
                question="Spontan abortusların zamansal dağılımı ve genetik anomalilerin gebelik haftasıyla ilişkisi hakkında aşağıdaki ifadelerden hangisi amfi ders notunun temel spot bilgisidir?",
                options=[
                    {"key": "A", "text": "Abortus riski en yüksek 16-20. haftalarda izlenir ve genetik nedenler bu haftalarda pik yapar.", "isCorrect": False, "explanation": "Yanlış. Risk ilk 8 haftada en yüksektir ve genetik nedenler erken haftalarda piktir."},
                    {"key": "B", "text": "Genetik anöploidilerin düşüğe yol açma oranı 1. ve 3. trimesterde tamamen eşittir.", "isCorrect": False, "explanation": "Yanlış. Gebelik ilerledikçe genetik düşükler hızla azalır."},
                    {"key": "C", "text": "Abortus riski ilk 8 haftada en yüksektir; gebelik süreci ilerledikçe genetik bozukluklara bağlı düşükler ve genel düşük insidansı azalır.", "isCorrect": True, "explanation": "Doğru. Amfi ders notunun temel ilkesidir: risk ilk 8 haftada zirvedir ve genetik etki zamanla geriler."},
                    {"key": "D", "text": "İlk 8 haftada düşüklerin tamamı maternal servikal yetmezlikten kaynaklanır.", "isCorrect": False, "explanation": "Servikal yetmezlik 2. trimester patolojisidir; ilk 8 haftada genetik nedenler hakimdir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Spontan abortus riski ilk sekiz haftada en yüksektir ve gebelik ilerledikçe genetik bozuklukların oranı azalır.",
                masked_term="ilk sekiz haftada",
                hint="Düşük yapma ihtimalinin en tepeye ulaştığı kritik embriyonik zaman dilimi"
            ),
            make_slider(
                left_title="İlk 8 Gebelik Haftası",
                right_title="12. Hafta Sonrası (2. Trimester)",
                left_points=[
                    "Spontan abortus riskinin en tepe yaptığı zaman dilimidir",
                    "Kayıpların %70'inden fazlası ağır kromozomal anomalilere bağlıdır",
                    "Doğal seleksiyon ile letal embriyolar elenir"
                ],
                right_points=[
                    "Genel spontan düşük insidansı belirgin olarak gerilemiştir",
                    "Kromozomal anomali oranı %30 seviyesine düşer",
                    "Maternal rahim anomalileri ve enfeksiyonlar ön plana geçer"
                ]
            ),
            make_recall(
                question="İlk 8 haftadaki düşüklerin doğadaki biyolojik ve evrimsel yararı nedir?",
                answer="Ağır ve yaşamla bağdaşmayan kromozomal anomalilere sahip kusurlu embriyoların erken dönemde elenerek doğal seleksiyonun sağlanmasıdır."
            )
        ]
    ))

    # Slide 5
    slides.append(make_slide(
        slide_num=5,
        title="Spontan Abortusta Yaşam Tarzı Risk Faktörleri",
        subtitle="Sigara, alkol ve aşırı kafein tüketiminin embriyotoksik etkileri",
        clinical_focus="Önlenebilir maternal alışkanlıkların desidua ve trofoblast üzerindeki hasarı",
        narrative=(
            "Spontan abortus patogenezinde genetik faktörlerin yanı sıra maternal maruziyetler ve modifiye edilebilir yaşam tarzı faktörleri kritik rol oynar.\n\n"
            "- **Sigara (Tütün Kullanımı):** Nikotin vazokonstriksiyon yaparak uteroplasental kan akımını azaltır; karbonmonoksit ise fetal hemoglobini bağlayarak fetal doku hipoksisi yaratır. Doz bağımlı olarak abortus riskini 1.5-2 kat artırır.\n"
            "- **Alkol Tüketimi:** Alkol ve metaboliti asetaldehit doğrudan embriyotoksik ve teratojendir. Özellikle gebeliğin ilk haftalarında düzenli veya 'binge' (aşırı) alkol tüketimi desidual kanlanmayı bozarak erken düşüğü tetikler.\n"
            "- **Aşırı Kafein Alımı:** Günlük >200-300 mg (2-3 fincan kahveden fazla) kafein tüketimi, serbest fetal dolaşımda vazokonstriksiyon ve cAMP artışı yaparak düşük riskinde artışla ilişkilendirilmiştir.\n\n"
            "> [!NOTE]\n"
            "> Sigara, alkol ve aşırı kafein tüketimi erken gebelik kaybı için kanıtlanmış önlenebilir majör yaşam tarzı risk faktörleridir."
        ),
        bullets=[
            "Sigara: Nikotin vazokonstriksiyonu ve CO hipoksisi ile düşük riskini artırır",
            "Alkol: Asetaldehit doğrudan embriyotoksik etki yaparak trofoblastı bozar",
            "Aşırı kafein: Günlük >200 mg kafein plasental perfüzyonu olumsuz etkiler",
            "Bu faktörler gebelik öncesinde ve başında modifiye edilebilir risklerdir"
        ],
        elements=[
            make_quiz(
                question="İlk trimesterde spontan abortus riskini belirgin şekilde artıran, desidual kan akımını bozarak fetal hipoksiye ve embriyotoksisiteye yol açan modifiye edilebilir maternal yaşam tarzı faktörleri hangisinde bir arada verilmiştir?",
                options=[
                    {"key": "A", "text": "Hafif tempolu yürüyüş ve folik asit desteği", "isCorrect": False, "explanation": "Bunlar sağlıklı gebelik alışkanlıklarıdır; riski azaltır."},
                    {"key": "B", "text": "Sigara içimi, alkol tüketimi ve aşırı kafein alımı", "isCorrect": True, "explanation": "Doğru. Sigara, alkol ve aşırı kafein ders notunda belirtilen temel yaşam tarzı risk faktörleridir."},
                    {"key": "C", "text": "Bol su tüketimi ve Akdeniz tipi beslenme", "isCorrect": False, "explanation": "Koruyucu beslenme tarzıdır."},
                    {"key": "D", "text": "Günde 8 saat uyku ve demir takviyesi", "isCorrect": False, "explanation": "Düşük riski oluşturmaz."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Maternal sigara kullanımı, alkol tüketimi ve aşırı kafein alımı erken gebelik kaybı riskini artıran önemli faktörlerdir.",
                masked_term="aşırı kafein alımı",
                hint="Günde yüksek doz kahve ve çay tüketimiyle alınan uyarıcı madde"
            ),
            make_table(
                title="Yaşam Tarzı Faktörleri ve Fetal Patolojik Mekanizmaları",
                headers=["Zararlı Faktör", "Etki Mekanizması", "Obstetrik Sonuç"],
                rows=[
                    [
                        {"text": "Sigara (Nikotin / CO)", "isMasked": False},
                        {"text": "Vazokonstriksiyon ve karboksihemoglobin hipoksisi", "isMasked": True, "hint": "Damar büzüşmesi ve oksijen taşınmasının bozulması"},
                        {"text": "Düşük riski artışı, plasental hipoperfüzyon", "isMasked": False}
                    ],
                    [
                        {"text": "Alkol Maruziyeti", "isMasked": False},
                        {"text": "Direkt embriyotoksik ve sitotoksik hasar", "isMasked": True, "hint": "Asetaldehitin hücre bölünmesini zehirlemesi"},
                        {"text": "Erken embriyonik kayıp ve teratojenite", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Gebelikte kafein tüketimi için uluslararası obstetrik kılavuzların önerdiği güvenli günlük üst sınır nedir?",
                answer="Günde 200 mg kafeindir (yaklaşık 1 kupa filtre kahve veya 2 fincan Türk kahvesi/çay)."
            )
        ]
    ))

    # Slide 6
    slides.append(make_slide(
        slide_num=6,
        title="Demografik ve Etnik Risk Faktörleri",
        subtitle="Afrika kökenli olmak ve ileri anne yaşının kümülatif etkisi",
        clinical_focus="Etnik yatkınlık ve oosit yaşlanmasının düşük insidansına yansıması",
        narrative=(
            "Spontan abortus epidemiyolojisinde bazı demografik ve etnik özellikler bağımsız risk faktörü olarak tanımlanmıştır.\n\n"
            "- **Etnik Köken (Afrika Kökenli Olmak):** Geniş çaplı epidemiyolojik çalışmalarda, Afrika kökenli kadınlarda beyaz ırka kıyasla spontan abortus ve erken gebelik kaybı oranlarının istatistiksel olarak daha yüksek olduğu belgelenmiştir. Bu durum sosyoekonomik faktörlerin yanı sıra kronik hipertansiyon, leiomyom prevalansının yüksekliği ve vasküler yatkınlıklarla ilişkilendirilir.\n"
            "- **Maternal Yaş Faktörü:** 20-30 yaş arası kadınlarda spontan abortus riski %10 civarındayken, 35 yaş üzerinde %20'ye, 40 yaş üzerinde %40'a ve 45 yaş üzerinde %80'e fırlar. Bunun temel nedeni oositlerde yaşa bağlı mayotik nondisjunction (ayrılmama) kusurlarının katlanarak artmasıdır.\n\n"
            "> [!NOTE]\n"
            "> Afrika kökenli olmak ve özellikle 35 yaş üzeri ileri maternal yaş spontan abortus riskini belirgin şekilde artıran demografik faktörlerdir."
        ),
        bullets=[
            "Afrika kökenli kadınlarda spontan abortus insidansı daha yüksektir",
            "Maternal yaş ile düşük riski eksponansiyel olarak artar (40 yaşta %40)",
            "İleri yaşta oosit mayoz bölünme hataları ve anöploidiler dramatik artar",
            "Etnik zemin ve yaş faktörü hasta danışmanlığında mutlaka hesaba katılmalıdır"
        ],
        elements=[
            make_quiz(
                question="Spontan abortus epidemiyolojisinde bağımsız risk faktörü olarak kabul edilen etnik köken ve yaş dinamikleri ile ilgili hangisi doğrudur?",
                options=[
                    {"key": "A", "text": "Anne yaşı ilerledikçe spontan düşük riski azalır ve 40 yaşta sıfırlanır.", "isCorrect": False, "explanation": "Yanlış. Anne yaşıyla risk hızla artar; 40 yaşta %40'a ulaşır."},
                    {"key": "B", "text": "Etnik kökenin gebelik kaybı üzerinde hiçbir istatistiksel etkisi yoktur.", "isCorrect": False, "explanation": "Yanlış. Afrika kökenli olmak risk faktörleri arasındadır."},
                    {"key": "C", "text": "Afrika kökenli olmak ve ileri anne yaşı spontan abortus riskini belirgin şekilde artıran faktörlerdir.", "isCorrect": True, "explanation": "Doğru. Amfi ders notunda Afrika kökenli olmak ve ileri anne yaşı risk faktörleri arasında açıkça sıralanmıştır."},
                    {"key": "D", "text": "En düşük abortus riski 45 yaş üzerindeki gebelerde görülür.", "isCorrect": False, "explanation": "45 yaş üzerinde düşük riski %80'in üzerindedir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Epidemiyolojik çalışmalarda Afrika kökenli olmak ve ileri anne yaşı spontan abortus riskini artıran demografik faktörler arasında yer alır.",
                masked_term="Afrika kökenli olmak",
                hint="Ders notunda düşük riskiyle ilişkisi belirtilen spesifik etnik demografi"
            ),
            make_slider(
                left_title="Genç Anne Yaşı (20-30 Yaş)",
                right_title="İleri Anne Yaşı (≥40 Yaş)",
                left_points=[
                    "Oosit kalitesi ve mitotik iğ iplikçikleri stabildir",
                    "Kromozomal anöploidi oranı düşüktür",
                    "Spontan abortus riski yaklaşık %10-12 düzeyindedir"
                ],
                right_points=[
                    "Oositler uzun süre profaz 1'de beklediği için mayotik ayrılmama sıktır",
                    "Fetal anöploidi ve trizomi riski katlanarak artar",
                    "Spontan abortus riski %40-50 ve üzerine tırmanır"
                ]
            ),
            make_recall(
                question="İleri anne yaşında düşük riskinin dramatik şekilde artmasının altında yatan temel hücresel mekanizma nedir?",
                answer="Oositlerin doğumdan itibaren mayoz I profazında (diktiyoten evresi) beklemesi nedeniyle kohezin proteinlerinin zayıflaması ve yaşa bağlı mayotik ayrılmama (nondisjunction) kusurlarının artmasıdır."
            )
        ]
    ))

    # Slide 7
    slides.append(make_slide(
        slide_num=7,
        title="Obstetrik Öykünün Önemi: Önceki EPL ve Ölü Doğum Anamnezi",
        subtitle="Tekrarlayan kayıp riski ve gebelik geçmişinin prognostik değeri",
        clinical_focus="Bir kadının geçmiş obstetrik hikayesinin sonraki gebeliğe etkisi",
        narrative=(
            "Bir kadının önceki gebelik öyküsü, mevcut gebelikteki spontan abortus riskini öngörmede en güçlü klinik rehberdir.\n\n"
            "- **Daha Önce EPL (Erken Gebelik Kaybı) Geçirmiş Olmak:** Daha önce bir kez erken düşük yaşayan bir kadında bir sonraki gebelikte düşük riski hafif artar (%15-20). Ancak daha önce iki düşük geçirmişse risk %25-30'a, ardışık üç düşükten sonra ise %35-45'e yükselir.\n"
            "- **Önceki Ölü Doğum Öyküsü:** Geçmişinde intrauterin fetal ölüm (ölü doğum) hikayesi olan kadınlarda; altta yatan kalıtsal trombofili, antifosfolipid sendromu, uterin vasküler yetersizlik veya genetik translokasyonlar nedeniyle erken gebelikte de abortus riski belirgin olarak yüksektir.\n"
            "- **Klinik Yaklaşım:** Anamnezinde EPL veya ölü doğum olan her gebe, ilk trimesterden itibaren yüksek riskli kabul edilerek yakın takip protokolüne alınmalıdır.\n\n"
            "> [!IMPORTANT]\n"
            "> Daha önce erken gebelik kaybı (EPL) veya ölü doğum yaşamış olmak, sonraki gebeliklerde abortus riskini belirgin şekilde artıran majör obstetrik faktörlerdir."
        ),
        bullets=[
            "Daha önce EPL geçirmiş olmak sonraki gebelikte düşük riskini katlar",
            "Düşük sayısı arttıkça (1'den 2 ve 3'e) tekrarlama riski %40'lara tırmanır",
            "Önceki ölü doğum öyküsü vasküler ve trombofilik zemin açısından uyarıcıdır",
            "Geçmiş gebelik kayıpları detaylı etiyolojik tarama endikasyonudur"
        ],
        elements=[
            make_quiz(
                question="Obstetrik polikliniğe başvuran bir gebenin anamnezinde daha önce iki kez erken gebelik kaybı (EPL) ve bir kez 28. haftada açıklanamayan ölü doğum öyküsü saptanıyor. Bu hastanın mevcut gebeliğindeki abortus riski hakkında en doğru yaklaşım hangisidir?",
                options=[
                    {"key": "A", "text": "Geçmiş gebeliklerin mevcut gebelik riskine hiçbir etkisi yoktur, rutin izlem yeterlidir.", "isCorrect": False, "explanation": "Yanlış. Geçmiş kayıplar riski katlar."},
                    {"key": "B", "text": "Daha önce EPL ve ölü doğum geçirmiş olmak abortus riskini belirgin artırır; hasta yüksek riskli kabul edilip incelenmelidir.", "isCorrect": True, "explanation": "Doğru. Önceki EPL ve ölü doğum öyküsü bağımsız güçlü risk faktörleridir."},
                    {"key": "C", "text": "Hastada kesinlikle komplet mol hidatiform gelişecektir.", "isCorrect": False, "explanation": "Öykü trofoblastik tümör anlamına gelmez."},
                    {"key": "D", "text": "Ölü doğum öyküsü olan kadınlar bir daha asla gebe kalamaz.", "isCorrect": False, "explanation": "Fertilite kaybı anlamına gelmez."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Anamnezde daha önce erken gebelik kaybı geçirmiş olmak sonraki gebeliklerde spontan abortus riskini belirgin şekilde artıran faktörlerdendir.",
                masked_term="erken gebelik kaybı",
                hint="İngilizce kısaltması EPL olan ilk trimester düşüğü öyküsü"
            ),
            make_chain(
                title="Geçmiş Düşük Sayısına Göre Tekrarlama Riski Kaskadı",
                steps=[
                    "1. Sıfır Düşük Öyküsü: Genel toplumdaki bazal spontan abortus riski yaklaşık %10-12 düzeyindedir.",
                    "2. Bir Düşük Sonrası: Bir sonraki gebelikte abortus riski hafif artışla yaklaşık %15-20'ye çıkar.",
                    "3. İki Düşük Sonrası: Tekrarlama riski belirgin bir sıçrama yaparak %25-30 bandına tırmanır.",
                    "4. Üç Düşük Sonrası: Kalıcı patoloji şüphesi doğar; risk %35-45'e ulaşır ve rekürren abortus protokolü başlar."
                ]
            ),
            make_recall(
                question="Daha önce bir kez spontan düşük yapmış bir kadına bir sonraki gebeliğin başarı şansı hakkında bilgi verirken en doğru yaklaşım nedir?",
                answer="Bir düşük sonrası kadının bir sonraki gebeliğinde sağlıklı bir canlı doğum yapma şansının halen çok yüksek (%80-85 civarında) olduğu belirtilerek anksiyete yatıştırılmalıdır."
            )
        ]
    ))

    # Slide 8
    slides.append(make_slide(
        slide_num=8,
        title="Medikal ve İatrojenik Risk Faktörleri",
        subtitle="Diyabet, yardımcı üreme teknikleri (YÜT) ve erken vajinal kanama",
        clinical_focus="Maternal metabolik durum ve yardımla üreme sürecinin obstetrik riskleri",
        narrative=(
            "Spontan abortus zemininde yatan tıbbi hastalıklar ve reprodüktif müdahaleler incelendiğinde üç faktör öne çıkar.\n\n"
            "- **Diabetes Mellitus:** Özellikle prekonsepsiyonel dönemde glisemik kontrolü zayıf olan (yüksek HbA1c seviyeleri) diyabetik kadınlarda spontan abortus ve majör konjenital malformasyon riski 2-3 kat artar. İnsülin direnci ve hiperglisemi embriyonik vaskülarizasyonu bozar.\n"
            "- **Yardımcı Üreme Teknikleri (YÜT / IVF):** Tüp bebek ve ovulasyon indüksiyonu ile elde edilen gebeliklerde spontan düşük oranları doğal gebeliklere kıyasla daha yüksek bildirilmektedir. Bu artış teknikten ziyade altta yatan maternal ileri yaş, infertilite etiyolojisi (PCOS, endometriozis) ve çoğul gebeliklerle ilişkilidir.\n"
            "- **Erken Vajinal Kanama:** İlk trimesterde vajinal kanama yaşayan kadınlarda, gebelik devam etse dahi nihai gebelik kaybı ve preterm doğum riski belirgin derecede yükselir.\n\n"
            "> [!NOTE]\n"
            "> Zayıf kontrollü diyabet, yardımcı üreme teknikleri ve erken vajinal kanama spontan düşük riskini artıran önemli medikal faktörlerdir."
        ),
        bullets=[
            "Diyabette zayıf glisemik kontrol (yüksek HbA1c) abortus riskini belirgin artırır",
            "Yardımcı üreme teknikleri (YÜT) zeminindeki infertilite etiyolojisiyle riski artırır",
            "İlk trimesterde vajinal kanama görülmesi düşük riskinin bağımsız habercisidir",
            "Glisemik optimizasyon ve yakın ultrason takibi bu grupta zorunludur"
        ],
        elements=[
            make_quiz(
                question="İlk trimester gebeliği olan bir kadında aşağıdaki medikal ve obstetrik durumlardan hangisi amfi ders notuna göre spontan abortus riskini artıran faktörler arasında yer alır?",
                options=[
                    {"key": "A", "text": "İyi kontrollü gestasyonel ağırlık artışı", "isCorrect": False, "explanation": "Risk faktörü değildir."},
                    {"key": "B", "text": "Diyabet, yardımcı üreme teknikleri ve erken vajinal kanama", "isCorrect": True, "explanation": "Doğru. Ders notunun 'Risk Faktörleri' listesinde diyabet, YÜT ve vajinal kanama açıkça belirtilmiştir."},
                    {"key": "C", "text": "Tekil normal intrauterin gebelik", "isCorrect": False, "explanation": "Normal fizyolojik durumdur."},
                    {"key": "D", "text": "Normal tiroid fonksiyon testleri", "isCorrect": False, "explanation": "Normal TSH riski artırmaz."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Maternal diyabet ve yardımcı üreme teknikleri spontan abortus riskini artıran önemli klinik faktörlerdir.",
                masked_term="yardımcı üreme teknikleri",
                hint="Tüp bebek (IVF) ve aşılama gibi infertilite tedavi yöntemleri"
            ),
            make_table(
                title="Medikal Risk Faktörleri ve Patofizyolojik Etkileri",
                headers=["Klinik Durum", "Patofizyolojik Mekanizma", "Düşük Dışındaki Ek Risk"],
                rows=[
                    [
                        {"text": "Diabetes Mellitus", "isMasked": False},
                        {"text": "Hiperglisemi ve serbest oksijen radikali hasarı", "isMasked": True, "hint": "Kanda glukoz yüksekliği toksisitesi"},
                        {"text": "Konjenital fetal kardiyak ve nöral tüp defektleri", "isMasked": False}
                    ],
                    [
                        {"text": "İlk Trimester Kanaması", "isMasked": False},
                        {"text": "Desidual ayrılma ve subkoryonik hematom", "isMasked": True, "hint": "Plasenta tabanında kan göllenmesi"},
                        {"text": "Plasenta dekolmanı ve erken doğum riski", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Diyabetik bir kadında gebelik planlanmadan önce spontan abortus ve fetal malformasyon riskini en aza indirmek için hangi laboratuvar parametresinin hedef değerde olması istenir?",
                answer="Serum HbA1c düzeyinin gebelik öncesinde %6.0 - 6.5'in altında (ideal glisemik kontrolde) olması istenir."
            )
        ]
    ))

    # Slide 9
    slides.append(make_slide(
        slide_num=9,
        title="Spontan Abortus Risk Faktörleri: Bütünsel Özet Tablosu",
        subtitle="Yaşam tarzı, demografi, obstetrik öykü ve medikal risklerin sentezi",
        clinical_focus="İlk muayenede risk skorlaması ve önleyici yaklaşım",
        narrative=(
            "Spontan abortus tek bir nedene bağlı gelişen izole bir patoloji değildir; çok sayıda maternal, çevresel ve obstetrik faktörün birleşimiyle tetiklenir.\n\n"
            "- **Tüm Risk Faktörlerinin Sentezi:** Amfi ders notunda vurgulanan ana risk faktörleri şunlardır:\n"
            "  1. **Yaşam Tarzı:** Sigara, alkol ve aşırı kafein alımı.\n"
            "  2. **Demografi:** İleri maternal yaş ve Afrika kökenli olmak.\n"
            "  3. **Obstetrik Öykü:** Daha önce EPL (erken gebelik kaybı) veya ölü doğum geçirmiş olmak.\n"
            "  4. **Medikal Durumlar:** Diyabet, yardımcı üreme teknikleri (YÜT) ile gebe kalmış olmak ve ilk trimesterde vajinal kanama gibi tıbbi komplikasyonların varlığı.\n"
            "- **Klinik Değerlendirme:** Bu faktörlerden bir veya daha fazlasına sahip gebeler, ilk trimester kanaması olduğunda doğrudan 'yüksek riskli düşük tehdidi' olarak ele alınmalıdır.\n\n"
            "> [!IMPORTANT]\n"
            "> Sigara, alkol, aşırı kafein, Afrika kökeni, önceki EPL/ölü doğum, diyabet, YÜT ve vajinal kanama abortusun temel risk faktörleridir."
        ),
        bullets=[
            "Yaşam tarzı: Sigara, alkol ve aşırı kafein alımı riski katlar",
            "Demografi: İleri anne yaşı ve Afrika kökenli olmak bağımsız faktörlerdir",
            "Anamnez: Önceki düşükler ve ölü doğum hikayesi tekrarlama riskini artırır",
            "Medikal: Kontrolsüz diyabet, YÜT gebelikleri ve vajinal kanama komplikasyonları"
        ],
        elements=[
            make_quiz(
                question="Birinci basamak hekimine başvuran 6 haftalık bir gebenin dosyasında aşağıdakilerden hangisinin bulunması spontan abortus riskini artıran faktörlerden biri DEĞİLDİR?",
                options=[
                    {"key": "A", "text": "Günde 1 paket sigara içimi ve aşırı kafein tüketimi", "isCorrect": False, "explanation": "Bu kanıtlanmış bir yaşam tarzı riskidir."},
                    {"key": "B", "text": "Önceki gebeliğinde 8. haftada EPL (düşük) geçirmiş olması", "isCorrect": False, "explanation": "Önceki düşük öyküsü riski belirgin artırır."},
                    {"key": "C", "text": "24 yaşında olması ve gebelik öncesi günlük folik asit (400 mcg) kullanması", "isCorrect": True, "explanation": "Doğru. Genç yaş ve prekonsepsiyonel folik asit desteği düşük risk faktörü değildir; aksine sağlıklı gebelik göstergesidir."},
                    {"key": "D", "text": "Gebeliğin yardımcı üreme tekniği (IVF) ile elde edilmiş olması ve kontrolsüz diyabet", "isCorrect": False, "explanation": "YÜT ve diyabet risk faktörleri arasındadır."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Daha önce ölü doğum yapmış olmak ve kontrolsüz diyabet spontan abortus riskini artıran tıbbi faktörlerdendir.",
                masked_term="ölü doğum",
                hint="Gebeliğin 20. haftasından sonra anne karnında fetal kayıp durumu"
            ),
            make_swipe(
                title="Gebelik Faktörleri Risk Değerlendirmesi",
                left_category="Abortus Riskini Artıran Faktörler",
                right_category="Düşük Riski Oluşturmayan / Koruyucu Durumlar",
                cards=[
                    {"text": "Maternal sigara ve düzenli alkol tüketimi", "category": "left", "explanation": "Embriyotoksik ve vazokonstriktör etkilerle riski artırır."},
                    {"text": "Düzenli prekonsepsiyonel folik asit desteği", "category": "right", "explanation": "Nöral tüp defektlerini önleyen koruyucu vitamindir."},
                    {"text": "Daha önce iki kez erken gebelik kaybı (EPL) öyküsü", "category": "left", "explanation": "Tekrarlama riskini %30'lara çıkaran güçlü faktördür."},
                    {"text": "Genç reprodüktif yaş (22 yaş) ve normal kan şekeri", "category": "right", "explanation": "En düşük bazal abortus riskine sahip gruptur."}
                ]
            ),
            make_recall(
                question="İlk vizitte gebe bir kadının anamnezinde abortus risk faktörlerini sorgulamanın temel klinik amacı nedir?",
                answer="Modifiye edilebilir riskleri (sigara, alkol, kafein, kan şekeri kontrolü) hızla düzelterek ve yüksek riskli gebeleri yakın ultrasonik ve hormonal takibe almaktır."
            )
        ]
    ))

    # Slide 10 - Checkpoint 1
    slides.append(make_slide(
        slide_num=10,
        title="[TEKRAR SAYFASI - CHECKPOINT 1] Tanım, İnsidans ve Risk Faktörleri",
        subtitle="Bölüm 1 Kapsamlı Pekiştirme ve Kazanım Kontrolü",
        clinical_focus="Abortus sınırları, trimester dinamikleri ve risk faktörlerinin sentezi",
        narrative=(
            "Bu tekrar sayfası, 1-9. adımlarda incelenen Abortus Tanımı, İnsidansı ve Risk Faktörleri kazanımlarını pekiştirmek için düzenlenmiştir.\n\n"
            "- **Tanım ve Eşikler:** Spontan abortus ilk 20 gebelik haftasından önce ve 500 gramdan küçük embriyo/fetüs ve eklerinin atılmasıdır. İlk 12 hafta erken abortustur; 13-20. haftalar geç abortustur.\n"
            "- **İnsidans ve Zaman:** Tüm gebeliklerin %15-20'si, klinik gebeliklerin %10-12'si düşer. Düşüklerin %80'i ilk trimesterdedir ve bunların %50'si kromozomaldir. Risk ilk 8 haftada en yüksektir; gebelik ilerledikçe genetik düşükler azalır.\n"
            "- **Majör Risk Faktörleri:** Sigara, alkol, aşırı kafein, Afrika kökenli olmak, önceki EPL ve ölü doğum öyküsü, diyabet, yardımcı üreme teknikleri (YÜT) ve erken vajinal kanamadır.\n\n"
            "> [!NOTE]\n"
            "> 20 hafta / 500 gram sınırı abortusu tanımlar; kayıpların %80'i ilk trimesterdedir; risk ilk 8 haftada en yüksektir; sigara, alkol, diyabet ve önceki EPL temel risklerdir."
        ),
        bullets=[
            "20 hafta ve 500 gram altı kayıplar spontan abortus kabul edilir",
            "İlk 12 hafta erken abortus; 13-20. hafta geç abortustur",
            "Kayıpların %80'i ilk trimesterdedir; bunların %50'si kromozomaldir",
            "Risk ilk 8 haftada zirvedir; zamanla genetik anomalilerin oranı azalır",
            "Sigara, alkol, kafein, Afrika kökeni, önceki EPL/ölü doğum ve diyabet majör risklerdir"
        ],
        elements=[
            make_quiz(
                question="Bölüm 1 boyunca öğrenilen temel epidemiyolojik ve tanımlayıcı ilkeler ışığında, spontan abortusla ilgili aşağıdaki ifadelerden hangisi KESİNLİKLE DOĞRUDUR?",
                options=[
                    {"key": "A", "text": "22. haftada ve 600 gram ağırlığında gerçekleşen gebelik kaybı erken abortus olarak adlandırılır.", "isCorrect": False, "explanation": "Yanlış. 20 hafta ve 500 gram üzeri kayıplar abortus değil ölü doğumdur."},
                    {"key": "B", "text": "Spontan düşüklerin %80'i ikinci trimesterde gerçekleşir ve genetik anomali oranı haftalar ilerledikçe artar.", "isCorrect": False, "explanation": "Yanlış. Düşüklerin %80'i ilk trimesterdedir ve genetik oran zamanla azalır."},
                    {"key": "C", "text": "Spontan abortus ilk 20 hafta ve <500 gram kayıplardır; düşüklerin %80'i ilk trimesterdedir ve risk ilk 8 haftada en yüksektir.", "isCorrect": True, "explanation": "Doğru. Bölüm 1'in tüm tanımlayıcı ve istatistiksel ilkelerini eksiksiz özetleyen doğru ifadedir."},
                    {"key": "D", "text": "Daha önce erken gebelik kaybı (EPL) yaşamış olmak sonraki gebelikte düşük riskini sıfıra indirir.", "isCorrect": False, "explanation": "Yanlış. Önceki kayıp sonraki riski belirgin şekilde artırır."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Spontan abortus ilk yirmi gebelik haftasından önce ve beş yüz gramdan küçük embriyo veya fetüsün atılması olarak tanımlanır.",
                masked_term="ilk yirmi gebelik haftasından",
                hint="Düşük tanımındaki resmi süre ve zaman üst eşiği"
            ),
            make_table(
                title="Bölüm 1 Temel Epidemiyoloji ve Risk Faktörleri Özeti",
                headers=["Kategori", "Temel Kriter / Değer", "Klinik Yansıması"],
                rows=[
                    [
                        {"text": "Abortus Tanım Eşiği", "isMasked": False},
                        {"text": "İlk 20 hafta ve <500 gram", "isMasked": True, "hint": "Yasal viabilite öncesi dönem ve kütle sınırı"},
                        {"text": "Viabilite öncesi fetal kayıpların sınıflaması", "isMasked": False}
                    ],
                    [
                        {"text": "En Yüksek Risk Zamanı", "isMasked": False},
                        {"text": "İlk 8 gebelik haftası", "isMasked": True, "hint": "Embriyonik dönemin zirve kayıp aralığı"},
                        {"text": "Ağır genetik anomalilerin doğal seleksiyonla elenmesi", "isMasked": False}
                    ],
                    [
                        {"text": "Trimester Dağılımı", "isMasked": False},
                        {"text": "%80 ilk trimester; %50 kromozomal", "isMasked": True, "hint": "Düşüklerin büyük kısmının erken haftalarda toplanması"},
                        {"text": "İlk trimesterde genetik analiz önceliği", "isMasked": False}
                    ]
                ]
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 1 Kontrol Önermeleri",
                items=[
                    {"text": "İlk 12 hafta içindeki kayıplar erken abortus (EPL) olarak adlandırılır.", "isLie": False, "explanation": "Doğru. 12 hafta sınırı erken abortustur."},
                    {"text": "Klinik olarak tanınan gebeliklerin yaklaşık %10-12'si spontan abortusla sonuçlanır.", "isLie": False, "explanation": "Doğru. Klinik gebeliklerde oran %10-12'dir."},
                    {"text": "Gebelik haftası ilerledikçe fetal kromozomal anomaliye bağlı düşüklerin oranı ve sayısı katlanarak artar.", "isLie": True, "explanation": "Tuzak! Gebelik süreci ilerledikçe genetik bozukluklara bağlı düşükler ve düşük insidansı hızla azalır; erken kayıplarda genetik etki çok daha fazladır."},
                    {"text": "Sigara, alkol, aşırı kafein ve kontrolsüz diyabet kanıtlanmış düşük risk faktörleridir.", "isLie": False, "explanation": "Doğru. Amfi ders notundaki temel risk faktörleridir."}
                ]
            ),
            make_recall(
                question="Checkpoint 1: Spontan abortus tanımında kullanılan iki temel eşik değer (hafta ve gram) nedir ve düşüklerin yüzde kaçı ilk trimesterde görülür?",
                answer="İlk 20 gebelik haftasından önce ve 500 gramdan küçük olmasıdır; tüm spontan düşüklerin %80'i ilk trimesterde meydana gelir."
            )
        ],
        is_checkpoint=True,
        checkpoint_number=1
    ))

    return slides
