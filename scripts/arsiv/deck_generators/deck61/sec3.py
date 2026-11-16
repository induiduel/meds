# -*- coding: utf-8 -*-
"""
Deck 61 Section 3: Maternal Etiyolojik Faktörler
Slides 21-30 (Checkpoint 3 at slide 30)
Focus:
- Maternal kronik metabolik hastalıklar: Diabetes mellitus (glisemik kontrol, HbA1c, vaskülopati)
- Maternal endokrinopatiler: Tiroid bozuklukları (hipotiroidi, otoimmün tiroidit)
- Sistemik hastalıklar: Çölyak hastalığı, inflamatuvar barsak hastalığı (İBH), siyanotik kalp hastalıkları
- Otoimmün ve metabolik patolojiler: Sistemik lupus eritematozus (SLE) ve maternal fenilketonüri (PKU)
- Anatomik uterin faktörler: İntrauterin sineşi (Asherman sendromu) ve endometrial obliterasyon
- Tartışmalı anatomik faktörler: Leiomyomlar (submüköz vs intramural), endometrial polipler, Müllerian füzyon anomalileri (septat uterus vb.)
- Enfeksiyonlar ve tartışmalı etiyolojik ajanlar: Bakteriyel vajinozis (Gardnerella vaginalis), Mycoplasma genitalium, Ureaplasma urealyticum
- Tartışmalı sistemik enfeksiyonlar: Toxoplasma gondii, Chlamydia trachomatis, Listeria monocytogenes, Herpes simplex virus (HSV)
- Çevresel ve iatrojenik toksisite: Radyasyon (>5 rad eşiği), radyoterapi ve kemoterapi maruziyeti
- Checkpoint 3 (Tekrar ve pekiştirme sayfası)
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

def get_sec3_slides():
    slides = []

    # Slide 21
    slides.append(make_slide(
        slide_num=21,
        title="Maternal Etiyoloji: Kronik Metabolik Hastalıklar ve Diyabet",
        subtitle="Prekonsepsiyonel glisemik kontrol, HbA1c yüksekliği ve vaskülopati",
        clinical_focus="Hipergliseminin erken embriyogenez ve plasentasyon üzerindeki yıkıcı etkileri",
        narrative=(
            "Spontan abortusların maternal nedenleri arasında sistemik kronik hastalıklar geniş bir yer tutar.\n\n"
            "- **Diabetes Mellitus:** Özellikle prekonsepsiyonel dönemde glisemik kontrolü kötü olan (yüksek HbA1c düzeyleri) Tip 1 ve Tip 2 diyabetik kadınlarda spontan abortus riski bazal toplum ortalamasının **2 ila 3 katına çıkar**.\n"
            "- **Fizyopatolojik Mekanizma:** Hiperglisemi ve keton cisimcikleri organogenez sırasında reaktif oksijen radikallerini artırarak embriyonik apoptozu tetikler. Ayrıca maternal mikrovaskülopati desidual perfüzyonu bozarak trofoblast invazyonunu ve plasentasyonu yetersiz kılar.\n"
            "- **Klinik Yaklaşım:** Diyabetik kadınlarda gebelik planlanırken HbA1c'nin <%6.5 düzeyine çekilmesi abortus ve majör konjenital kardiyak/nöral anomalileri önlemede en kritik basamaktır. Buna karşılık iyi kontrollü diyabette abortus riski genel popülasyondan belirgin farklı değildir.\n\n"
            "> [!IMPORTANT]\n"
            "> Prekonsepsiyonel dönemde kontrolsüz diyabet ve yüksek HbA1c düzeyleri, spontan abortus ve embriyonik malformasyon riskini katlayarak artırır."
        ),
        bullets=[
            "Kontrolsüz diyabet ve yüksek HbA1c abortus riskini 2-3 kat artırır",
            "Hiperglisemi embriyonik dokularda oksidatif hasar ve apoptozu indükler",
            "Maternal desidual vaskülopati erken plasental perfüzyonu yetersiz kılar",
            "İyi glisemik kontrol sağlanan diyabetik kadınlarda abortus riski artmaz"
        ],
        elements=[
            make_quiz(
                question="Diabetes mellitus tanılı bir gebenin erken gebelik döneminde spontan abortus riskinin artması temel olarak aşağıdaki faktörlerden hangisiyle doğrudan ilişkilidir?",
                options=[
                    {"key": "A", "text": "Gebelik öncesi ve erken dönemdeki kontrolsüz hiperglisemi ve yüksek HbA1c düzeyleri", "isCorrect": True, "explanation": "Doğru. Düşük riski iyi kontrollü diyabette değil, zayıf kontrollü yüksek glisemili olgularda artar."},
                    {"key": "B", "text": "Hastanın üçüncü trimesterde gestasyonel diyabet taraması yaptırması", "isCorrect": False, "explanation": "Gestasyonel diyabet geç dönemde çıkar, ilk trimester abortuslarıyla ilişkisizdir."},
                    {"key": "C", "text": "Düşük doz insülin tedavisinin embriyotoksik etki göstermesi", "isCorrect": False, "explanation": "İnsülin teratojen veya abortifasit değildir; kan şekerini regüle eden esansiyel ilaçtır."},
                    {"key": "D", "text": "Oral glukoz tolerans testinin plasentayı mekanik olarak yırtması", "isCorrect": False, "explanation": "OGTT standart biyokimyasal tanı testidir, mekanik hasar yapmaz."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Maternal diyabette prekonsepsiyonel dönemde yüksek seyreden glukoz düzeyleri embriyonik apoptozu tetikleyerek erken gebelik kaybı riskini katlar.",
                masked_term="yüksek seyreden glukoz",
                hint="Diyabette kanda kontrolsüzce artan metabolik şeker fraksiyonu"
            ),
            make_chain(
                title="Kontrolsüz Diyabette Abortus Patofizyolojisi",
                steps=[
                    "Prekonsepsiyonel Hiperglisemi: Maternal kanda kronik yüksek glukoz ve HbA1c birikimi",
                    "Embriyonik Oksidatif Stres: Reaktif oksijen türevlerinin blastokistte hücresel hasar ve apoptoz yapması",
                    "Desidual Mikroanjiyopati: Uterin spiral arterlerde endotel hasarı ve implantasyon defekti",
                    "Plasental Yetersizlik ve Kayıp: Trofoblast invazyonunun durması ve ilk trimesterde spontan abortus"
                ]
            ),
            make_recall(
                question="Diyabetik bir kadında abortus ve konjenital malformasyon riskini en aza indirmek için konsepsiyon öncesi hedef HbA1c düzeyi ne olmalıdır?",
                answer="Hedef HbA1c düzeyi %6.5'in (mümkünse %6.0'ın) altında tutulmalıdır; glisemik kontrol sağlandıktan sonra gebeliğe izin verilmelidir."
            )
        ]
    ))

    # Slide 22
    slides.append(make_slide(
        slide_num=22,
        title="Maternal Endokrin Bozukluklar: Tiroid Patolojileri",
        subtitle="Klinik ve subklinik hipotiroidi, antitiroid peroksidaz (anti-TPO) varlığı",
        clinical_focus="Erken nörogenez ve trofoblast diferansiasyonunda tiroid hormonlarının rolü",
        narrative=(
            "Maternal tiroid disfonksiyonu, spontan gebelik kayıplarında sıkça suçlanan bir diğer önemli endokrin nedendir.\n\n"
            "- **Hipotiroidizm:** Özellikle klinik hipotiroidi (yüksek TSH, düşük sT4) varlığında spontan abortus, gestasyonel hipertansiyon ve fetal nörogelişimsel yetersizlik oranları belirgin yükselir. Erken embriyogenezde fetüs kendi tiroid hormonunu henüz sentezleyemediğinden tamamen maternal transplasental T4 geçişine bağımlıdır.\n"
            "- **Otoimmün Tiroidit:** Ötiroid kadınlarda dahi yüksek **anti-tiroid peroksidaz (anti-TPO)** ve anti-tiroglobulin antikorlarının bulunması, altta yatan sistemik bir immün disregülasyona işaret ederek abortus riskini hafifçe artırabilir.\n"
            "- **Klinik Yaklaşım:** Gebelik planlayan veya erken gebelikte başvuran kadınlarda TSH düzeyinin taranması ve TSH'nın ilk trimesterde kılavuz hedeflerinde (<2.5 mIU/L) tutulması levotiroksin replasmanı ile güvenceye alınır.\n\n"
            "> [!NOTE]\n"
            "> Tedavi edilmemiş belirgin hipotiroidizm ve otoimmün tiroid antikor pozitifliği erken gebelik kaybı riskini artıran endokrinolojik faktörlerdir."
        ),
        bullets=[
            "Tedavi edilmemiş hipotiroidi spontan abortus riskini belirgin şekilde artırır",
            "İlk trimesterde fetüs tiroid hormonları açısından tamamen anneye bağımlıdır",
            "Anti-TPO antikor pozitifliği ötiroid kadınlarda bile riski hafif yükseltebilir",
            "İlk trimesterde TSH düzeyinin <2.5 mIU/L düzeyinde tutulması hedeflenir"
        ],
        elements=[
            make_quiz(
                question="Erken gebelikte saptanan aşağıdaki endokrin patolojilerden hangisi tedavi edilmediğinde spontan abortus riskini artıran kanıtlanmış bir maternal nedendir?",
                options=[
                    {"key": "A", "text": "Fizyolojik prolaktin artışı", "isCorrect": False, "explanation": "Gebelikte prolaktin fizyolojik olarak yükselir, patoloji değildir."},
                    {"key": "B", "text": "Tedavi edilmemiş klinik hipotiroidizm (yüksek TSH, düşük sT4)", "isCorrect": True, "explanation": "Doğru. Kontrolsüz hipotiroidizm embriyonik gelişimi ve plasentasyonu bozarak abortus yapar."},
                    {"key": "C", "text": "Hafif izole alkalen fosfataz yüksekliği", "isCorrect": False, "explanation": "Plasental izoenzim artışına bağlı fizyolojik bir bulgudur."},
                    {"key": "D", "text": "İkinci trimesterde azalan hCG düzeyi", "isCorrect": False, "explanation": "hCG'nin 10. haftadan sonra plato çizip düşmesi fizyolojik endokrin süreçtir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Maternal tiroid bezinin yetersiz çalışması yani tedavi edilmemiş belirgin hipotiroidizm ilk trimesterde fetal kayıp riskini artıran önemli bir tablodur.",
                masked_term="hipotiroidizm",
                hint="TSH hormonunun yükselip serbest T4 düzeyinin düştüğü metabolik hastalık"
            ),
            make_slider(
                left_title="Ötiroid Gebe (TSH Normal)",
                right_title="Tedavi Edilmemiş Hipotiroidi (TSH Yüksek)",
                left_points=[
                    "Yeterli maternal T4 transplasental geçişi",
                    "Optimal trofoblastik invazyon ve desidualizasyon",
                    "Bazal toplum düzeyinde düşük riski (%10-12)"
                ],
                right_points=[
                    "Embriyonik nörogenez ve hücre bölünmesinde yetersizlik",
                    "Plasental perfüzyonda bozulma ve desidual defekt",
                    "Artmış spontan abortus ve fetal kayıp riski"
                ]
            ),
            make_recall(
                question="İlk trimesterde fetüsün kendi tiroid bezi çalışmaya başlayana kadar tiroid hormon ihtiyacı nasıl karşılanır?",
                answer="Fetüs organogenez evresinde kendi tiroid hormonunu üretemez; plasentayı geçen maternal serbest tiroksin (T4) hormonuna tamamen bağımlıdır."
            )
        ]
    ))

    # Slide 23
    slides.append(make_slide(
        slide_num=23,
        title="Sistemik Hastalıklar: Çölyak, İBH ve Siyanotik Kalp Hastalıkları",
        subtitle="Kronik malnütrisyon, vasküler hipoksi ve mikronutrient eksiklikleri",
        clinical_focus="Gastrointestinal emilim bozuklukları ve fetal oksijenizasyon kısıtlılığı",
        narrative=(
            "Maternal kronik hastalıklar spektrumunda otoimmün bağırsak patolojileri ve kardiyovasküler bozukluklar önemli bir grubu oluşturur.\n\n"
            "- **Çölyak Hastalığı:** Tanı almamış veya glutensiz diyete uymayan aktif çölyak hastalarında kronik bağırsak inflamasyonu ve emilim kusuru gelişir. Folat, çinko, demir ve yağda eriyen vitaminlerin malabsorpsiyonu erken embriyonik arrest ve spontan abortus riskini belirgin artırır. Glutensiz diyetle bu risk normale döner.\n"
            "- **İnflamatuvar Bağırsak Hastalığı (İBH - Crohn / Ülseratif Kolit):** Özellikle konsepsiyon sırasında hastalığı aktif alevlenme evresinde olan kadınlarda sistemik sitokin salınımı (TNF-alfa) ve desidual inflamasyon abortus riskini yükseltir.\n"
            "- **Siyanotik Kalp Hastalıkları:** Sağ-sol şantlı konjenital siyanotik kalp hastalıkları olan annelerde maternal kronik hipoksemi desidual spiral arterlerin oksijenlenmesini engeller; bu durum erken fetal kayıp ve abortusla sonuçlanır.\n\n"
            "> [!NOTE]\n"
            "> Tedavi edilmemiş çölyak hastalığı malnütrisyonla, siyanotik kalp hastalıkları ise maternal kronik hipoksiyle abortus riskini artırır."
        ),
        bullets=[
            "Aktif çölyak hastalığı mikronutrient malabsorpsiyonu ile abortus yapar",
            "Glutensiz diyete tam uyum çölyak hastalarında düşük riskini normale çeker",
            "Aktif inflamatuvar barsak hastalığında sistemik sitokinler desiduayı bozar",
            "Siyanotik kalp hastalıklarında kronik hipoksemi erken kayıplara yol açar"
        ],
        elements=[
            make_quiz(
                question="Tedavi edilmemiş aktif çölyak hastalığı bulunan bir kadında spontan abortus gelişme riskinin yüksek olmasının temel mekanizması hangisidir?",
                options=[
                    {"key": "A", "text": "Gluten antikorlarının fetal eritrositleri doğrudan hemolize uğratması", "isCorrect": False, "explanation": "Fetal hemoliz Rh uyuşmazlığında olur, çölyak mekanizması değildir."},
                    {"key": "B", "text": "Kronik enteropatiye bağlı mikronutrient emilim bozuklukları ve malnütrisyon", "isCorrect": True, "explanation": "Doğru. Folat, demir ve mineral malabsorpsiyonu embriyonik gelişimi ve desidualizasyonu bozar."},
                    {"key": "C", "text": "Uterus serviksinde doğumsal bağ dokusu gevşekliği oluşması", "isCorrect": False, "explanation": "Servikal yetmezlik çölyak kaynaklı değildir."},
                    {"key": "D", "text": "Overlerde androjen üretiminin katlanarak artması", "isCorrect": False, "explanation": "PCOS ile karıştıran yanlış şıktır."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Tanı almamış veya diyetsiz aktif çölyak hastalığında gelişen besin emilim bozukluğu spontan gebelik kayıplarına zemin hazırlar.",
                masked_term="çölyak",
                hint="Gluten enteropatisine yol açan otoimmün ince bağırsak hastalığı"
            ),
            make_swipe(
                title="Sistemik Hastalıklar ve Düşük Patogenezi",
                left_category="Malnütrisyon / İnflamasyon Kökenli",
                right_category="Hipoksi / Hemodinamik Kökenli",
                cards=[
                    {"text": "Aktif Çölyak Hastalığı", "category": "left", "explanation": "İntestinal villus atrofisi ve vitamin malabsorpsiyonu ile seyreder."},
                    {"text": "Siyanotik Kalp Hastalığı", "category": "right", "explanation": "Kronik maternal hipoksi ve uterin desidual perfüzyon yetmezliği yapar."},
                    {"text": "Alevlenmiş Crohn Hastalığı", "category": "left", "explanation": "Sistemik TNF-alfa sitokin fırtınası ve bağırsak inflamasyonu etkindir."}
                ]
            ),
            make_recall(
                question="Maternal siyanotik kalp hastalıklarında erken gebelik kaybının altta yatan temel hemodinamik ve biyolojik gerekçesi nedir?",
                answer="Sağdan sola şant nedeniyle maternal arteriyel kanın kronik desatürasyonu ve uteroplasental yatağa ulaşan oksijen miktarının embriyonik doku solunumu için yetersiz kalmasıdır."
            )
        ]
    ))

    # Slide 24
    slides.append(make_slide(
        slide_num=24,
        title="Otoimmün ve Metabolik Faktörler: SLE ve Fenilketonüri",
        subtitle="Lupus desidual vasküliti ve maternal hiperfenilalaninemi embriyopatisi",
        clinical_focus="İmmün kompleks kaynaklı plasental enfarktlar ve toksik metabolit geçişi",
        narrative=(
            "Maternal patolojilerde immün yanıtın plasentayı hedef alması veya kanda toksik metabolit birikimi erken gebelik kaybına yol açar.\n\n"
            "- **Sistemik Lupus Eritematozus (SLE):** Aktif lupus nefriti ve sistemik alevlenmeler desidual damarlarda nekrotizan vaskülit ve immün kompleks birikimine yol açar. Beraberinde antifosfolipid antikorları sıklıkla bulunur. Plasental yetersizlik ve erken spontan abortus oranı belirgin yüksektir.\n"
            "- **Maternal Fenilketonüri (PKU):** Diyetine uymayan PKU'lu gebelerde kanda yükselen fenilalanin plasentayı aktif taşıma ile geçerek embriyoda doğrudan teratojen ve embriyotoksik etki gösterir (**maternal PKU sendromu**). Spontan abortus, mikrosefali, konjenital kalp defektleri ve büyüme geriliği gelişir.\n"
            "- **Klinik Yaklaşım:** SLE'li olgularda remisyon döneminde gebelik planlanmalı; PKU'lu kadınlarda ise konsepsiyon öncesinden itibaren sıkı fenilalanin kısıtlı diyet uygulanmalıdır.\n\n"
            "> [!IMPORTANT]\n"
            "> Aktif SLE desidual vaskülit ve enfarkt ile, kontrolsüz maternal PKU ise fenilalaninin direkt embriyotoksisitesi ile abortus yapar."
        ),
        bullets=[
            "Aktif SLE maternal desidual vaskülit ve plasental trombozla abortus yapar",
            "Maternal fenilketonüride yüksek fenilalanin düzeyi doğrudan embriyotoksiktir",
            "Kontrolsüz PKU'da spontan abortusun yanı sıra fetal mikrosefali ve kardiyak defekt izlenir",
            "Her iki patolojide de konsepsiyon öncesi remisyon ve biyokimyasal kontrol şarttır"
        ],
        elements=[
            make_quiz(
                question="Diyet tedavisine uyumsuz bir fenilketonüri (PKU) hastasının gebe kalması durumunda erken gebelikte spontan abortus ve fetal hasar gelişmesinin temel mekanizması hangisidir?",
                options=[
                    {"key": "A", "text": "Maternal kanda biriken fenilalaninin plasentayı geçerek embriyo üzerinde toksik etki oluşturması", "isCorrect": True, "explanation": "Doğru. Maternal hiperfenilalaninemi doğrudan embriyotoksik ve teratojeniktir."},
                    {"key": "B", "text": "Trizomi 16 oluşumunun kimyasal olarak tetiklenmesi", "isCorrect": False, "explanation": "Fenilalanin otozomal trizomi nondisjunction nedeni değildir."},
                    {"key": "C", "text": "Servikal kanalın genişleyerek erken açılması", "isCorrect": False, "explanation": "PKU servikal yetmezlik yapmaz."},
                    {"key": "D", "text": "Maternal kan grubu antikorlarının titrajının yükselmesi", "isCorrect": False, "explanation": "Alloimmünizasyon mekanizması değildir."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Kontrolsüz maternal fenilketonüri vakalarında kanda aşırı biriken fenilalanin metaboliti plasentayı aşarak erken fetal kayba yol açar.",
                masked_term="fenilketonüri",
                hint="Maternal kanda toksik aminoasit artışıyla giden doğumsal metabolizma bozukluğu"
            ),
            make_spot_the_lie(
                topic="Maternal metabolik ve otoimmün etiyolojiler",
                items=[
                    {"text": "Aktif SLE alevlenmeleri desidual damarlarda vaskülit yaparak spontan abortus riskini yükseltir.", "isLie": False, "explanation": "Doğrudur; immün hasar desidual perfüzyonu bozar."},
                    {"text": "Maternal fenilketonüride yüksek kan fenilalanin düzeyleri embriyotoksik değildir, gebelikte diyet serbesttir.", "isLie": True, "explanation": "Tuzak önerme. Fenilalanin doğrudan teratojen ve embriyotoksiktir; diyet kısıtlaması konsepsiyon öncesi şarttır."},
                    {"text": "SLE remisyondayken planlanan gebeliklerde erken kayıp riski alevlenmeli döneme göre çok daha düşüktür.", "isLie": False, "explanation": "Doğrudur; klinik remisyonda vaskülit riski minimize olur."}
                ]
            ),
            make_recall(
                question="Maternal PKU sendromunda spontan düşük gerçekleşmezse doğan bebekte görülebilecek klasik konjenital defektler nelerdir?",
                answer="Mikrosefali, zeka geriliği, konjenital kalp defektleri (özellikle Fallot tetralojisi, VSD) ve intrauterin gelişme geriliğidir."
            )
        ]
    ))

    # Slide 25
    slides.append(make_slide(
        slide_num=25,
        title="Uterin Anatomik Faktörler: İntrauterin Sineşi (Asherman Sendromu)",
        subtitle="Endometrial bazalis tabakasının hasarlanması ve kavite obliterasyonu",
        clinical_focus="Geçirilmiş agresif küretaj sonrası gelişen fibröz yapışıklıklar ve implantasyon defekti",
        narrative=(
            "Maternal etiyolojide uterin kavitenin mekanik ve anatomik bütünlüğü implantasyon ve embriyonik büyüme için esastır.\n\n"
            "- **Asherman Sendromu (İntrauterin Sineşi):** Genellikle geçirilmiş enfekte küretaj, postpartum kanama müdahalesi veya pelvik cerrahiler sonrasında endometrial bazalis tabakasının travmatize olmasıyla gelişir. Kavite içinde fibrotik yapışıklıklar ve bantlar oluşur.\n"
            "- **Abortus Mekanizması:** Fibröz yapışıklıklar uterus kavitesini daraltır ve sağlıklı fonksiyonel endometrium yüzeyini yok eder. Blastokist avasküler fibröz dokuya implante olamaz veya implante olsa dahi plasenta yeterli vasküler desidua bulamadığı için erken gebelikte spontan abortus gerçekleşir.\n"
            "- **Klinik Tanı ve Tedavi:** Hipomenore veya amenore öyküsü olan bu kadınlarda histerosalpingografi (HSG), sonohisterografi (SIS) veya tanısal **histeroskopi** ile tanı konur. Tedavide histeroskopik sineşiyolizis uygulanır.\n\n"
            "> [!IMPORTANT]\n"
            "> İntrauterin sineşi (Asherman sendromu), endometrial desidua yokluğu ve kavite darlığı yaratarak abortusa yol açan kanıtlanmış bir anatomik nedendir."
        ),
        bullets=[
            "Asherman sendromu agresif küretaj sonrası gelişen intrauterin fibröz sineşidir",
            "Endometriumun avasküler nedbeleşmesi sağlıklı implantasyonu imkansız kılar",
            "Hastalar sıklıkla sekonder oligomenore/amenore ve düşüklerle başvurur",
            "Altın standart tanı ve tedavi yöntemi histeroskopidir"
        ],
        elements=[
            make_quiz(
                question="Daha önce postpartum kanama nedeniyle revizyon küretajı geçiren ve sonrasında hipomenore şikayeti başlayan bir kadında art arda iki kez ilk trimester abortusu gerçekleşiyor. Bu hastada şüphelenilmesi gereken en olası uterin anatomik patoloji hangisidir?",
                options=[
                    {"key": "A", "text": "Subseröz fundal leiomyom", "isCorrect": False, "explanation": "Subseröz miyom kavite dışındadır, implantasyonu ve menstrüasyonu bozmaz."},
                    {"key": "B", "text": "İntrauterin sineşi (Asherman sendromu)", "isCorrect": True, "explanation": "Doğru. Agresif küretaj, hipomenore ve tekrarlayan abortus öyküsü Asherman sendromunun klasik tablosudur."},
                    {"key": "C", "text": "Akut bakteriyel servisit", "isCorrect": False, "explanation": "Servisit intrauterin yapışıklık ve kalıcı hipomenore yapmaz."},
                    {"key": "D", "text": "Basit luteal over kisti", "isCorrect": False, "explanation": "Over kisti menstrüel hacmi azaltıp fibröz kavite yapmaz."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Geçirilmiş uterin travma ve küretaj sonrası kavite içinde oluşan intrauterin sineşi Asherman sendromu olarak bilinir ve abortus nedenidir.",
                masked_term="intrauterin sineşi",
                hint="Uterus içi boşlukta oluşan fibrotik yapışıklık ve skar bantları"
            ),
            make_chain(
                title="Asherman Sendromu ve Abortus Patofizyolojisi",
                steps=[
                    "Endometrial Travma: Postpartum veya enfekte kavitary küretaj sırasında stratum bazalisin tahrip olması",
                    "Fibröz Skarlaşma: Karşılıklı uterin duvarlar arasında avasküler kolajenöz sineşilerin oluşması",
                    "Kavite Daralması: Fonksiyonel endometrium yüzey alanının küçülmesi ve desidual vaskülarizasyon kaybı",
                    "İmplantasyon Defekti ve Abortus: Blastokistin avasküler nedbeye tutunması ve erken plasental iskemiyle düşük"
                ]
            ),
            make_recall(
                question="Asherman sendromunun tanısında ve cerrahi tedavisinde günümüzde altın standart kabul edilen yöntem nedir?",
                answer="Histeroskopidir (direkt kamera altında yapışıklıkların görülmesi ve makas/enerji ile açılması - histeroskopik sineşiyolizis)."
            )
        ]
    ))

    # Slide 26
    slides.append(make_slide(
        slide_num=26,
        title="Tartışmalı Anatomik Faktörler: Leiomyom, Polip ve Müllerian Anomaliler",
        subtitle="Submüköz miyomlar vs intramural/subseröz; septat uterus tartışmaları",
        clinical_focus="Uterin kaviteye uzanım gösteren lezyonların vasküler ve mekanik etkileri",
        narrative=(
            "Uterusun yapısal lezyonlarının abortus etiyolojisindeki rolü uzun yıllardır tartışmalı bir obstetrik konudur.\n\n"
            "- **Leiomyomlar:** Miyomların abortustaki etkisi yerleşim yerine göre değişir ve literatürde **etiyolojik rolü tartışmalıdır**. Uterus kavitesine bası yapan **submüköz miyomlar**, üzerlerindeki endometriumun incelmesi ve kan akımının bozulması nedeniyle düşük riskini artırabilir. Buna karşılık subseröz miyomların abortusla hiçbir ilişkisi yoktur; intramural miyomların rolü ise çelişkilidir.\n"
            "- **Endometrial Polip:** Düşüklerdeki yeri **tartışmalıdır**. Kavite içinde mekanik bariyer veya lokal inflamatuvar sitokin salınımı yapabileceği öne sürülse de net kanıt düzeyi düşüktür.\n"
            "- **Müllerian Anomaliler:** Uterus bikornis, uterus didelfis veya septat uterus gibi konjenital füzyon defektlerinin abortuslardaki rolü **tartışmalıdır**. En sık düşükle ilişkili bulunan anomali, septus dokusunun avasküler olması nedeniyle implantasyonu bozan **septat uterustur**.\n\n"
            "> [!NOTE]\n"
            "> Ders notuna göre; leiomyomlar, endometrial polipler ve Müllerian anomalilerin spontan abortus etiyolojisindeki yeri tartışmalıdır."
        ),
        bullets=[
            "Leiomyomların abortustaki etiyolojik rolü tartışmalı kabul edilir",
            "Submüköz miyomlar kaviteyi deforme ederken, subseröz miyomlar etkisizdir",
            "Endometrial poliplerin düşüklerdeki nedensel yeri literatürde tartışmalıdır",
            "Müllerian anomalilerden özellikle septat uterus avasküler septumu ile öne çıkar"
        ],
        elements=[
            make_quiz(
                question="Amfi ders notu ve obstetrik kaynaklara göre, aşağıdaki uterin anatomik durumlardan hangisinin spontan abortus etiyolojisindeki yeri 'tartışmalı' olarak nitelendirilen faktörlerden biridir?",
                options=[
                    {"key": "A", "text": "Kromozom analizinde Trizomi 16 saptanması", "isCorrect": False, "explanation": "Trizomi 16 tartışmasız kesin bir fetal genetik abortus nedenidir."},
                    {"key": "B", "text": "Gebelik haftasının 20 haftanın üzerinde olması", "isCorrect": False, "explanation": "Bu durum abortus tanım sınırının dışıdır."},
                    {"key": "C", "text": "Uterin leiomyomlar (miyomlar)", "isCorrect": True, "explanation": "Doğru. Ders notunda leiomiyom, endometrial polip ve Müllerian anomaliler 'tartışmalı faktörler' olarak sınıflandırılmıştır."},
                    {"key": "D", "text": "Anne yaşının 22 olması", "isCorrect": False, "explanation": "Genç yaş düşük riskini azaltan fizyolojik bir durumdur."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Ders notunda leiomiyom ve endometrial polip gibi uterin yapısal lezyonların abortus etiyolojisindeki yeri tartışmalı olarak belirtilmektedir.",
                masked_term="tartışmalı",
                hint="Tıbbi literatürde üzerinde kesin uzlaşı sağlanamayan, çelişkili kanıt içeren durum"
            ),
            make_venn(
                title="Kesin vs Tartışmalı Uterin Faktörler",
                label_a="Kanıtlanmış Anatomik Neden (Asherman)",
                label_b="Tartışmalı Anatomik Faktörler (Miyom / Polip)",
                items=[
                    {"criterion": "Kavitenin tamamen avasküler fibröz bantlarla oblitere olması", "correct": "A", "explanation": "Asherman sendromunun patognomonik lezyonudur."},
                    {"criterion": "Literatürde düşükle nedensellik ilişkisi açıkça tartışmalı kabul edilme", "correct": "B", "explanation": "Leiomyom ve polipler ders notunda tartışmalı başlığı altındadır."},
                    {"criterion": "Histeroskopi veya ultrasonografi ile değerlendirilebilme", "correct": "both", "explanation": "Her iki durum da kavitary görüntüleme yöntemleriyle saptanır."}
                ]
            ),
            make_recall(
                question="Müllerian anomaliler içinde tekrarlayan erken abortuslarla en güçlü ilişki gösteren ve avasküler bağ dokusu içeren konjenital malformasyon hangisidir?",
                answer="Septat uterustur (uterus septus); septum dokusunun vaskülarizasyonu son derece zayıf olduğu için bu alana implante olan embriyolar erken dönemde beslenemeyerek kaybedilir."
            )
        ]
    ))

    # Slide 27
    slides.append(make_slide(
        slide_num=27,
        title="Enfeksiyonlar ve Tartışmalı Etiyoloji: Vajinal Floradan İzole Edilenler",
        subtitle="Bakteriyel vajinozis (G. vaginalis), Mycoplasma genitalium, Ureaplasma",
        clinical_focus="Genital traktus kolonizasyonu ile gerçek abortus ilişkisi arasındaki tartışmalı zemin",
        narrative=(
            "Klinik pratikte enfeksiyonların spontan erken düşüklere yol açıp açmadığı en sık araştırılan konulardan biridir.\n\n"
            "- **Tartışmalı Konum:** Ders notunda ve obstetrik kılavuzlarda altı çizilerek belirtildiği üzere, genital enfeksiyöz ajanların **erken abortus etiyolojisindeki yeri TARTIŞMALIDIR**.\n"
            "- **Suçlanan Floralar:** En sık suçlanan ve araştırılan ajanlar arasında **bakteriyel vajinozis (Gardnerella vaginalis)**, **Mycoplasma genitalium** ve **Ureaplasma urealyticum** yer alır.\n"
            "- **Neden Tartışmalı?:** Bu mikroorganizmalar asemptomatik ve sağlıklı gebe kadınların alt genital florasında da yüksek oranlarda kolonize bulunur. Bu ajanların pozitif saptanması her zaman bir düşüğe neden olduklarını kanıtlamaz. Enfeksiyonlar daha çok ikinci trimesterdeki geç kayıplar ve preterm eylem ile ilişkilidir.\n\n"
            "> [!IMPORTANT]\n"
            "> Bakteriyel vajinozis (Gardnerella vaginalis), Mycoplasma ve Ureaplasma erken abortus etiyolojisinde suçlansa da yerleri tartışmalıdır."
        ),
        bullets=[
            "Genital enfeksiyonların erken abortus etiyolojisindeki rolü tartışmalıdır",
            "Gardnerella vaginalis (BV), Mycoplasma genitalium ve Ureaplasma en sık suçlananlardır",
            "Bu ajanlar sağlıklı gebelerin normal florasında da kolonize bulunabilir",
            "Rutin tarama ve ampirik antibiyotik kullanımının erken düşükleri önlediği kanıtlanmamıştır"
        ],
        elements=[
            make_quiz(
                question="Obstetrik amfi ders notuna göre, erken spontan abortus etiyolojisinde suçlanan enfeksiyöz ajanların (Gardnerella, Mycoplasma, Ureaplasma) bilimsel rolü hakkında hangisi doğrudur?",
                options=[
                    {"key": "A", "text": "Erken düşüklerin %90'ından bu enfeksiyonlar sorumludur", "isCorrect": False, "explanation": "Erken kayıpların %70'i genetiktir, enfeksiyon payı çok düşüktür."},
                    {"key": "B", "text": "Bu ajanların abortus etiyolojisindeki yeri tartışmalıdır", "isCorrect": True, "explanation": "Doğru. Ders notu bu mikroorganizmaların abortus etiyolojisindeki yerini açıkça 'tartışmalı' olarak belirtir."},
                    {"key": "C", "text": "Vajinal kültürde Ureaplasma üreyen her gebe mutlaka düşük yapar", "isCorrect": False, "explanation": "Ureaplasma sağlıklı asemptomatik florada da sıkça kolonizedir."},
                    {"key": "D", "text": "Bu ajanlar yalnızca üçüncü trimesterde fetal malformasyon yaparlar", "isCorrect": False, "explanation": "Erken dönemde suçlanmışlardır ancak nedensellikleri tartışmalıdır."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Bakteriyel vajinozis etkeni olan Gardnerella vaginalis gibi mikroorganizmaların abortus etiyolojisindeki yeri ders notunda tartışmalı olarak geçmektedir.",
                masked_term="Gardnerella vaginalis",
                hint="Bakteriyel vajinoziste koku ve akıntıya neden olan kokobasil etken"
            ),
            make_slider(
                left_title="Kanıtlanmış Fetal Nedenler",
                right_title="Tartışmalı Enfeksiyöz Nedenler",
                left_points=[
                    "Fetal kromozomal anöploidiler (Trizomi 16, 45,X0)",
                    "İlk trimesterde %70 nedensel pay",
                    "Doğrudan sitogenetik letalite mekanizması"
                ],
                right_points=[
                    "Gardnerella vaginalis, Mycoplasma, Ureaplasma",
                    "Erken kayıplardaki nedensel rolü tartışmalı",
                    "Sağlıklı asemptomatik gebelerde de sık kolonizasyon"
                ]
            ),
            make_recall(
                question="Neden Gardnerella vaginalis ve Ureaplasma gibi ajanların erken abortus nedeni olduğu konusu tıbbi literatürde tartışmalıdır?",
                answer="Çünkü bu mikroorganizmalar sağlıklı ve miadına sorunsuz ulaşan birçok gebenin normal alt genital florasında da yüksek oranlarda kolonize olarak izlenmekte, doğrudan plasental enfeksiyon kanıtı her zaman gösterilememektedir."
            )
        ]
    ))

    # Slide 28
    slides.append(make_slide(
        slide_num=28,
        title="Tartışmalı Sistemik Enfeksiyonlar: Toxoplasma, Chlamydia, Listeria ve HSV",
        subtitle="Zoonotik ve cinsel geçişli patojenlerin erken gebelik kaybındaki konumu",
        clinical_focus="Akut sistemik bakteriyemi/viremi ve desidual enfeksiyonun ayırt edilmesi",
        narrative=(
            "Vajinal floradaki tartışmalı bakterilerin yanı sıra bazı sistemik ve zoonotik enfeksiyonlar da ders notunda etiyolojide tartışmalı ajanlar arasında listelenmiştir.\n\n"
            "- **Suçlanan Sistemik Ajanlar:** **Toksoplazma gondii**, **Klamidya trachomatis**, **Listeriya monositogenez** ve **Herpes simplex virus (HSV)**.\n"
            "- **Etiyolojideki Yeri Tartışmalıdır:** Bu mikroorganizmalar akut maternal enfeksiyon sırasında transplasental geçişle fetüse ulaşabilir veya koryoamniyonit yapabilir. Ancak izole erken spontan abortusların doğrudan nedeni olduklarına dair kanıtlar zayıftır ve **etiyolojideki yerleri tartışmalıdır**.\n"
            "- **Klinik Gerçeklik:** Örneğin Listeria monocytogenes enfeksiyonu plasentada mikroabseler ve granülamatöz lezyonlar yaparak ölü doğuma yol açabilirken, tekrarlayan ilk trimester düşüklerinde rol oynamaz. Benzer şekilde Toksoplazma ve Chlamydia akut primer faz dışında erken düşüğün ana nedeni değildir.\n\n"
            "> [!NOTE]\n"
            "> Toksoplazma gondii, Klamidya trachomatis, Listeriya monositogenez ve Herpes simplex virus erken abortus etiyolojisinde yeri tartışmalı ajanlardır."
        ),
        bullets=[
            "Toksoplazma, Klamidya, Listeriya ve HSV suçlanan sistemik ajanlardır",
            "Ders notuna göre bu ajanların erken abortus etiyolojisindeki yeri tartışmalıdır",
            "Tekrarlayan erken düşüklerde bu etkenlerin rolü bulunmaz",
            "Primer akut enfeksiyonlar geç kayıp ve konjenital enfeksiyon tablosu yapabilir"
        ],
        elements=[
            make_quiz(
                question="Ders notunda erken gebelik kaybı etiyolojisindeki yeri 'tartışmalı suçlanan ajanlar' başlığı altında sayılan mikroorganizma grubu hangisinde eksiksiz verilmiştir?",
                options=[
                    {"key": "A", "text": "Streptococcus pneumoniae, Klebsiella pneumoniae, Pseudomonas aeruginosa", "isCorrect": False, "explanation": "Bunlar klasik solunum ve üriner sistem patojenleridir."},
                    {"key": "B", "text": "Yalnızca Hepatit A ve Rotavirüs", "isCorrect": False, "explanation": "Bu virüsler abortus etiyoloji listesinde yer almaz."},
                    {"key": "C", "text": "Toksoplazma gondii, Klamidya trachomatis, Listeriya monositogenez, Herpes simplex virus", "isCorrect": True, "explanation": "Doğru. Notta tartışmalı ajanlar olarak Gardnerella, Mycoplasma, Ureaplasma ile birlikte Toksoplazma, Klamidya, Listeriya ve HSV belirtilmiştir."},
                    {"key": "D", "text": "Helicobacter pylori ve Giardia lamblia", "isCorrect": False, "explanation": "Gastrointestinal parazit ve bakterilerdir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Besinlerle bulaşan ve plasental mikroabseler yapabilen Listeriya monositogenez bakterisinin erken abortus etiyolojisindeki yeri tartışmalıdır.",
                masked_term="Listeriya monositogenez",
                hint="Pastörize edilmemiş süt ürünleriyle bulaşan fakültatif intrasellüler bakteri"
            ),
            make_spot_the_lie(
                topic="Tartışmalı enfeksiyon ajanları",
                items=[
                    {"text": "Toksoplazma gondii ve Chlamydia trachomatis erken abortus etiyolojisinde yeri tartışmalı ajanlardandır.", "isLie": False, "explanation": "Doğrudur; notta bu ajanlar tartışmalı başlığında listelenmiştir."},
                    {"text": "Listeria monocytogenes enfeksiyonu tüm ilk trimester düşüklerinin kesin ve tek kanıtlanmış nedenidir.", "isLie": True, "explanation": "Tuzak önerme. Listeria nadir bir akut sistemik enfeksiyondur; erken düşük etiyolojisindeki yeri tartışmalıdır."},
                    {"text": "Herpes simplex virus maternal etiyolojide suçlanan ancak yeri tartışmalı olan patojenlerdendir.", "isLie": False, "explanation": "Doğrudur; nottaki 7 tartışmalı ajandan biridir."}
                ]
            ),
            make_recall(
                question="Ders notunda erken abortus etiyolojisindeki yeri tartışmalı olarak sayılan toplam 7 enfeksiyöz ajan hangileridir?",
                answer="Bakteriyel vajinozis (Gardnerella vaginalis), Mycoplasma genitalium, Ureaplasma urealyticum, Toksoplazma gondii, Klamidya trachomatis, Listeriya monositogenez ve Herpes simplex virustur (HSV)."
            )
        ]
    ))

    # Slide 29
    slides.append(make_slide(
        slide_num=29,
        title="Çevresel Toksisite: Radyasyon Eşiği, KT ve RT",
        subtitle="Radyasyonda 5 rad (0.05 Gy) güvenli eşik sınırı ve sitotoksik tedaviler",
        clinical_focus="Tanısal radyolojik işlemler ve onkolojik tedavilerin embriyotoksik sınırları",
        narrative=(
            "Maternal maruziyetler içinde fiziksel ve kimyasal ajanlar erken embriyonik dokularda doğrudan letal hasar yaratabilir.\n\n"
            "- **İyonize Radyasyon ve Kritik Eşik:** İyonize radyasyon doza bağımlı olarak embriyonik hücrelerde DNA kırıkları ve mitotik arrest oluşturur. Tıbbi ve obstetrik kılavuzlarda kabul edilen **kritik radyasyon eşiği 5 rad (0.05 Gy / 50 mGy)** düzeyidir. **5 rad üzerindeki (>5 rad)** maruziyetler spontan abortus, mikrosefali ve ağır zeka geriliği riskini belirgin artırır. Standart tanısal grafiler (akciğer grafisi, diş filmi, ekstremite röntgeni) <0.005 rad maruziyet oluşturduğundan abortusa yol açmaz.\n"
            "- **Radyoterapi (RT):** Pelvik veya abdominal radyoterapi doğrudan uterus ve gonadları hedef alarak embriyonun ölümüne ve gebeliğin sonlanmasına neden olur.\n"
            "- **Kemoterapi (KT):** Antimetabolitler (metotreksat), alkilleyici ajanlar ve DNA topoizomeraz inhibitörleri hızlı bölünen embriyonik ve trofoblastik hücreleri hızla yok ederek abortusa yol açar.\n\n"
            "> [!IMPORTANT]\n"
            "> Spontan abortus riskini artıran radyasyon eşiği >5 rad düzeyidir; radyoterapi ve kemoterapi kanıtlanmış diğer abortus nedenleridir."
        ),
        bullets=[
            "Radyasyonda abortus ve teratogenez için kabul edilen eşik değer >5 rad düzeyidir",
            "Standart tanısal grafiler (<0.005 rad) bu eşiğin bin kat altındadır ve güvenlidir",
            "Pelvik radyoterapi doğrudan uterin dokuyu ve embriyoyu tahrip ederek abortus yapar",
            "Sitotoksik kemoterapi ilaçları hızlı bölünen blastokist hücrelerini öldürür"
        ],
        elements=[
            make_quiz(
                question="İyonize radyasyon maruziyetinin bir gebede spontan abortus ve embriyotoksisite riskini belirgin şekilde artırması için ders notunda ve kılavuzlarda kabul edilen doz eşiği hangisidir?",
                options=[
                    {"key": "A", "text": ">0.001 rad", "isCorrect": False, "explanation": "Bu son derece düşük bir dozdur, arka plan doğa radyasyonu seviyesindedir."},
                    {"key": "B", "text": ">500 rad", "isCorrect": False, "explanation": "500 rad maternal ölümcül doz düzeyidir."},
                    {"key": "C", "text": "Sıfırın üzerindeki herhangi bir radyasyon maruziyeti", "isCorrect": False, "explanation": "Eşik değeri vardır (5 rad altı abortus yapmaz)."},
                    {"key": "D", "text": ">5 rad", "isCorrect": True, "explanation": "Doğru. Amfi ders notunda spontan abortus riski yaratan radyasyon dozu >5 rad olarak belirtilmiştir."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="İyonize radyasyona bağlı spontan abortus ve fetal malformasyon riskinin belirgin artması için maruziyetin beş rad düzeyinin üzerinde olması gerekir.",
                masked_term="beş rad",
                hint="Ders notunda belirtilen kritik kümülatif fetal absorbe enerji eşiği"
            ),
            make_slider(
                left_title="Güvenli Tanısal Radyoloji (<5 rad)",
                right_title="Abortus Riski Taşıyan Radyasyon (>5 rad)",
                left_points=[
                    "Akciğer grafisi, diş filmi, ekstremite röntgeni",
                    "Fetal maruziyet genellikle <0.001 - 0.05 rad arasındadır",
                    "Spontan abortus veya anomali riskinde artış yapmaz"
                ],
                right_points=[
                    "Pelvik radyoterapi ve çoklu terapötik abdominal BT çekimleri",
                    "Fetal maruziyet 5 rad eşiğini aşabilir (>5 rad)",
                    "Spontan abortus, mikrosefali ve fetal ölüm riski katlanır"
                ]
            ),
            make_recall(
                question="Acil serviste istemeden bir kez akciğer grafisi çekilen 6 haftalık gebe bir kadına abortus riski açısından ne söylenmelidir?",
                answer="Tek bir akciğer grafisinin fetal dozunun yaklaşık 0.001 rad olduğu, abortus için gereken 5 rad eşiğinin binlerce kat altında kaldığı belirtilerek hastanın gebeliği sonlandırmasına gerek olmadığı açıklanmalıdır."
            )
        ]
    ))

    # Slide 30 (Checkpoint 3)
    slides.append(make_slide(
        slide_num=30,
        title="[TEKRAR SAYFASI - CHECKPOINT 3] Maternal Etiyolojik Faktörler",
        subtitle="Kronik hastalıklar, anatomik engeller, tartışmalı enfeksiyonlar ve radyasyon",
        clinical_focus="Maternal kaynaklı gebelik kayıplarının kapsamlı entegrasyonu",
        narrative=(
            "Bu tekrar sayfası, 21-29. adımlarda işlenen Maternal Etiyoloji faktörlerini kapsamlı olarak pekiştirir.\n\n"
            "- **Kronik ve Metabolik:** Kontrolsüz diyabet (yüksek HbA1c), tedavi edilmemiş hipotiroidizm, aktif çölyak (malabsorpsiyon), siyanotik kalp hastalıkları (hipoksi), aktif SLE (desidual vaskülit) ve kontrolsüz fenilketonüri (embriyotoksisite) kanıtlanmış risklerdir.\n"
            "- **Uterin Anatomi:** Asherman sendromu (intrauterin sineşi) kesin anatomik nedendir. Leiomyomlar, endometrial polipler ve Müllerian anomaliler ise ders notuna göre **tartışmalıdır**.\n"
            "- **Tartışmalı Enfeksiyonlar:** Bakteriyel vajinozis (G. vaginalis), Mycoplasma genitalium, Ureaplasma urealyticum, Toksoplazma gondii, Klamidya trachomatis, Listeriya monositogenez ve HSV'nin erken abortustaki rolleri **TARTIŞMALIDIR**.\n"
            "- **Toksisite:** Radyasyon **>5 rad** düzeyinde abortus yapar; kemoterapi ve radyoterapi diğer nedenlerdir.\n\n"
            "> [!IMPORTANT]\n"
            "> Kesinler: Asherman, kontrolsüz DM/tiroid, SLE/PKU, radyasyon >5 rad | Tartışmalılar: Miyom, polip, Müllerian anomaliler ve 7 enfeksiyöz ajan."
        ),
        bullets=[
            "Kronik: Kontrolsüz DM, hipotiroidi, çölyak, SLE, PKU ve siyanotik kalp hastalığı",
            "Anatomik: Asherman kesin nedendir; miyom, polip ve Müllerian anomaliler tartışmalıdır",
            "Enfeksiyonlar: 7 mikroorganizmanın erken abortus etiyolojisindeki yeri tartışmalıdır",
            "Fiziksel/Kimyasal: Radyasyonda kritik sınır >5 rad düzeyidir; RT ve KT embriyotoksiktir"
        ],
        elements=[
            make_quiz(
                question="Maternal abortus etiyolojisi ile ilgili aşağıdaki ifadelerden hangisi amfi ders notundaki bilgilerle TAM UYUMLUDUR?",
                options=[
                    {"key": "A", "text": "Leiomyom ve Gardnerella vaginalis erken abortusun tartışmasız en kesin iki nedenidir", "isCorrect": False, "explanation": "Notta hem miyom hem de Gardnerella tartışmalı faktörler olarak belirtilmiştir."},
                    {"key": "B", "text": "İntrauterin sineşi (Asherman sendromu) kesin anatomik nedendir; Gardnerella ve Listeria gibi enfeksiyonların etiyolojideki yeri ise tartışmalıdır", "isCorrect": True, "explanation": "Doğru. Asherman kesin anatomik hasardır; suçlanan enfeksiyonların nedenselliği ise tartışmalıdır."},
                    {"key": "C", "text": "Radyasyonda 0.001 rad üzerinde her dozda gebelik hemen sonlandırılmalıdır", "isCorrect": False, "explanation": "Eşik doz >5 rad'dır, 0.001 rad güvenlidir."},
                    {"key": "D", "text": "İyi kontrollü tip 1 diyabette düşük riski %90'a çıkar", "isCorrect": False, "explanation": "İyi kontrollü diyabette risk bazal seviyededir; risk kontrolsüz diyabette artar."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Maternal nedenler arasında intrauterin sineşi yani Asherman sendromu kaviteyi daraltıp desiduayı yok ederek düşüğe yol açar.",
                masked_term="Asherman sendromu",
                hint="Agresif küretaj sonrası endometrial kavitede gelişen yaygın skar ve yapışıklık tablosu"
            ),
            make_table(
                title="Maternal Etiyoloji Sentez Tablosu (Checkpoint 3)",
                headers=["Etiyolojik Kategori", "Klinik Örnekler", "Etiyolojik Statü"],
                rows=[
                    [
                        {"text": "Kronik / Metabolik", "isMasked": False},
                        {"text": "Kontrolsüz DM, hipotiroidi, SLE, PKU", "isMasked": True, "hint": "Metabolik ve otoimmün sistemik hastalıklar"},
                        {"text": "Kanıtlanmış maternal risk", "isMasked": False}
                    ],
                    [
                        {"text": "Uterin Anatomik", "isMasked": False},
                        {"text": "Asherman sendromu", "isMasked": True, "hint": "İntrauterin yapışıklık ve skar tablosu"},
                        {"text": "Kanıtlanmış anatomik defekt", "isMasked": False}
                    ],
                    [
                        {"text": "Tartışmalı Anatomik", "isMasked": False},
                        {"text": "Leiomyom, endometrial polip, Müllerian", "isMasked": False},
                        {"text": "Etiyolojik rolü tartışmalı", "isMasked": True, "hint": "Literatürde net kesinlik bulunmayan statü"}
                    ],
                    [
                        {"text": "Suçlanan Enfeksiyonlar", "isMasked": False},
                        {"text": "Gardnerella, Mycoplasma, Toxoplasma, Listeria", "isMasked": False},
                        {"text": "Etiyolojideki yeri tartışmalı", "isMasked": True, "hint": "Kesin nedenselliği kanıtlanamamış durum"}
                    ]
                ]
            ),
            make_spot_the_lie(
                topic="Bölüm 3 maternal etiyoloji kazanımları",
                items=[
                    {"text": "Tedavi edilmemiş açık hipotiroidizm ve kontrolsüz diyabet erken gebelik kaybı riskini artırır.", "isLie": False, "explanation": "Doğrudur; her iki metabolik patoloji de kanıtlanmış risk faktörüdür."},
                    {"text": "Akciğer grafisi çekilen bir gebede alınan 0.001 rad radyasyon dozu nedeniyle acil küretaj yapılmalıdır.", "isLie": True, "explanation": "Tuzak önerme. Abortus ve teratogenez için eşik doz >5 rad'dır; 0.001 rad kesinlikle güvenlidir ve küretaj endikasyonu doğurmaz."},
                    {"text": "Bakteriyel vajinozis ve Ureaplasma erken abortus etiyolojisinde yeri tartışmalı ajanlardır.", "isLie": False, "explanation": "Doğrudur; ders notundaki 7 tartışmalı ajandan ikisidir."}
                ]
            ),
            make_branching(
                scenario="Tekrarlayan ilk trimester düşüğü öyküsü olan 32 yaşındaki bir kadın prekonsepsiyonel değerlendirme için başvuruyor. Yapılan tetkiklerdeki patolojiye göre yönetim belirlenecektir.",
                options=[
                    {
                        "text": "Hastada TSH 7.8 mIU/L (yüksek) ve sT4 düşük saptandığında levotiroksin tedavisi başlanarak TSH <2.5 düzeyine çekildikten sonra gebeliğe izin verilir.",
                        "isCorrect": True,
                        "feedback": "Doğru karar. Belirgin hipotiroidizm düzeltilmeden gebe kalınması abortus riskini katlar."
                    },
                    {
                        "text": "Hastanın vajinal kültüründe asemptomatik Ureaplasma saptandığında hastaya acil histerektomi planlanmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış. Ureaplasma tartışmalı bir ajandır, histerektomi gibi radikal bir cerrahi endikasyonu kesinlikle yoktur."
                    },
                    {
                        "text": "Hastada subseröz 1 cm miyom saptandığında abortusların kesin tek nedeni budur denilerek tüm overler alınmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış. Subseröz miyom kaviteyi etkilemez, düşüğe neden olmaz; ooforektomi yapılmaz."
                    }
                ]
            ),
            make_recall(
                question="Bölüm 3'te öğrenilen maternal etiyolojik faktörler içinde 'kanıtlanmış kesin' faktörler ile 'tartışmalı' faktörleri birer cümleyle nasıl özetlersiniz?",
                answer="Asherman sendromu, kontrolsüz diyabet, hipotiroidi, SLE, PKU ve >5 rad radyasyon kanıtlanmış nedenlerdir; buna karşılık leiomyomlar, endometrial polipler, Müllerian anomaliler ve 7 enfeksiyöz mikroorganizmanın (Gardnerella, Listeria vb.) rolü tartışmalıdır."
            )
        ]
    ))

    return slides
