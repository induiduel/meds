# -*- coding: utf-8 -*-
"""
Deck 61 Section 2: Fetal Genetik ve Kromozomal Nedenler
Slides 11-20 (Checkpoint 2 at slide 20)
Focus:
- Fetal kromozomal anomalilerin trimester dağılımı (%70 ilk trimester, %30 ikinci trimester)
- Spontan abortus materyallerinde en sık rastlanan karyotip (Normal karyotip)
- En sık tekil kromozom anomalisi (45,X0 - Turner Sendromu)
- En sık otozomal trizomi türü (Trizomi 16)
- Canlı doğumlarda görülen trizomiler (Trizomi 21 Down, 18 Edwards, 13 Patau) ile abortus ilişkisi
- Abort materyallerinde ASLA görülmeyen trizomiler (Trizomi 1, 3 ve 19)
- Maternal yaş artışı ve anöploidi riski (oosit mayoz I duraklaması, non-disjunction)
- Poliploidiler: Triploidi (69 kromozom, parsiyel mol, diandrik/diginik) ve Tetraploidi (92 kromozom)
- Yapısal kromozom anomalileri (Resiprokal ve Robertsonian translokasyonlar, delesyonlar, inversiyonlar)
- Checkpoint 2 (Tekrar ve pekiştirme sayfası)
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

def get_sec2_slides():
    slides = []

    # Slide 11
    slides.append(make_slide(
        slide_num=11,
        title="Fetal Etiyoloji: Erken ve Geç Kayıplarda Genetik Payı",
        subtitle="İlk trimesterde %70, ikinci trimesterde %30 kromozomal anomali oranı",
        clinical_focus="Gestasyonel yaş ilerledikçe genetik kökenli kayıpların oranındaki dramatik düşüş",
        narrative=(
            "Spontan abortusların etiyolojisi incelendiğinde en belirleyici faktör fetal genetik kusurlardır.\n\n"
            "- **Trimester Ayrımı:** Erken gebelik kayıplarında (ilk 12 hafta / ilk trimester) saptanan kromozomal anomali oranı **%70 seviyesindedir**. Buna karşılık ikinci trimesterde (13-20. haftalar) gerçekleşen geç abortuslarda bu oran **%30'a geriler**.\n"
            "- **Doğal Seçilim Mekanizması:** İnsan embriyogenezinde ağır sitogenetik defektler organogenezin erken evrelerinde ölümcül seyreder. Bu nedenle ağır anöploidiler ilk trimesterde uterustan elenir.\n"
            "- **Klinik Yansıması:** İlk trimesterde kaybedilen bir gebelikte altta yatan temel şüphe fetal genetik bozuklukken, ikinci trimester kayıplarında servikal yetmezlik, enfeksiyon ve anatomik defektler gibi maternal faktörler ön plana çıkar.\n\n"
            "> [!IMPORTANT]\n"
            "> Kromozomal anomali oranı ilk trimester kayıplarında %70 iken, ikinci trimester kayıplarında %30'a düşer."
        ),
        bullets=[
            "İlk trimester spontan düşüklerinde kromozomal anomali sıklığı %70'tir",
            "İkinci trimester kayıplarında genetik köken oranı %30 düzeyine geriler",
            "Ağır karyotip anomalileri erken organogenezde fetal yaşamla bağdaşmaz",
            "Gebelik haftası ilerledikçe maternal ve anatomik etkenlerin payı artış gösterir"
        ],
        elements=[
            make_quiz(
                question="Spontan abortus materyallerinin sitogenetik analizinde saptanan kromozomal anomali oranlarının trimesterlere göre dağılımı hangisinde doğru verilmiştir?",
                options=[
                    {"key": "A", "text": "İlk trimesterde %70, ikinci trimesterde %30", "isCorrect": True, "explanation": "Doğru. İlk trimesterde kromozomal kusurlar %70 oranında bulunurken, ikinci trimesterde %30'a geriler."},
                    {"key": "B", "text": "İlk trimesterde %30, ikinci trimesterde %70", "isCorrect": False, "explanation": "Tam tersidir; erken dönemde genetik hasar oranı çok daha yüksektir."},
                    {"key": "C", "text": "Her iki trimesterde de sabit %50", "isCorrect": False, "explanation": "Kromozom anomali oranı gebelik haftası ilerledikçe belirgin şekilde azalır."},
                    {"key": "D", "text": "İlk trimesterde %95, ikinci trimesterde %5", "isCorrect": False, "explanation": "Oranlar orantısız abartılmıştır; resmi oranlar %70 ve %30'dur."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Spontan abortuslarda saptanan kromozomal anomali oranı ilk trimesterde %70 iken ikinci trimesterde bu oran belirgin şekilde düşerek %30 düzeyine iner.",
                masked_term="%70",
                hint="Erken üç aylık evredeki yüksek genetik kusur yüzdesi"
            ),
            make_slider(
                left_title="İlk Trimester Kayıpları",
                right_title="İkinci Trimester Kayıpları",
                left_points=[
                    "Kromozomal anomali oranı yaklaşık %70",
                    "Ağır anöploidi ve poliploidiler baskın",
                    "Embriyonik arrest ve gelişim durması ön planda"
                ],
                right_points=[
                    "Kromozomal anomali oranı yaklaşık %30",
                    "Öploid (normal karyotip) kayıplar belirgin baskın",
                    "Maternal, anatomik veya servikal faktörler ön planda"
                ]
            ),
            make_recall(
                question="Gebelik haftası ilerledikçe abortuslarda genetik defekt oranının %70'ten %30'a düşmesinin temel biyolojik gerekçesi nedir?",
                answer="Ağır sitogenetik kusurların embriyogenez ve erken organogenez evresinde gelişimsel arrest oluşturarak erken elenmesi, ileri haftalara yalnızca viabilitesi daha yüksek veya genetik olarak normal fetüslerin ulaşabilmesidir."
            )
        ]
    ))

    # Slide 12
    slides.append(make_slide(
        slide_num=12,
        title="Abort Materyallerinde En Sık Karyotip: Normal Karyotip Paradoksu",
        subtitle="Anöploidi toplamda yüksek olsa da tekil olarak en sık karyotip öploididir",
        clinical_focus="Sitogenetik analizde normal karyotip varlığının etiyolojik anlamı",
        narrative=(
            "Klinik ve sitogenetik sınavlarda en sık düşülen tuzaklardan biri abort materyallerinde tekil olarak en sık izlenen karyotip sorusudur.\n\n"
            "- **En Sık Rastlanan Karyotip:** Tüm spontan abortus materyalleri topluca analiz edildiğinde **en sık rastlanan karyotip normal karyotiptir (öploidi - 46,XX veya 46,XY)**.\n"
            "- **Paradoksun Nedeni:** Kromozomal anomaliler kendi içinde trizomiler, monozomiler ve poliploidiler gibi onlarca alt gruba dağılır. Toplam anomalilerin oranı %50-70 olsa dahi, hiçbir spesifik anomali tek başına normal karyotip oranını (%30-50) geçemez.\n"
            "- **Klinik Değerlendirme:** Düşük materyalinde normal karyotip saptanması, kaybın sitogenetik bir hatadan ziyade maternal enfeksiyonlar, immünolojik yanıtlar, endokrin düzensizlikler veya anatomik yetersizliklerden kaynaklanabileceğini düşündürür.\n\n"
            "> [!NOTE]\n"
            "> Spontan abort materyallerinde tek başına en sık rastlanan karyotip normal (öploid) karyotiptir."
        ),
        bullets=[
            "Abort materyallerinde tekil olarak en sık rastlanan durum normal karyotiptir",
            "Anomalili karyotipler kendi içinde onlarca farklı sitogenetik gruba bölünür",
            "Öploid kayıplarda maternal endokrin, anatomik ve immünolojik nedenler aranmalıdır",
            "Tek bir kromozomal anomali türü tek başına öploidi oranını aşamaz"
        ],
        elements=[
            make_quiz(
                question="Spontan abortus materyallerinde sitogenetik inceleme yapıldığında en sık rastlanan karyotip hangisidir?",
                options=[
                    {"key": "A", "text": "47,XX,+16 (Trizomi 16)", "isCorrect": False, "explanation": "Trizomiler arasında en sıktır ancak tüm materyaller içinde öploidiyi geçemez."},
                    {"key": "B", "text": "45,X0 (Turner Sendromu)", "isCorrect": False, "explanation": "En sık tekil kromozom anomalisidir ancak normal karyotip sıklığından düşüktür."},
                    {"key": "C", "text": "Normal karyotip (Öploidi)", "isCorrect": True, "explanation": "Doğru. Düşük materyallerinde en sık saptanan tekil karyotip normal karyotiptir."},
                    {"key": "D", "text": "69,XXY (Triploidi)", "isCorrect": False, "explanation": "Poliploidiler abortusların yalnızca küçük bir fraksiyonunu oluşturur."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Spontan abortus materyallerinde sitogenetik olarak en sık rastlanan karyotip normal karyotiptir.",
                masked_term="normal karyotiptir",
                hint="Sitogenetik hasar içermeyen standart kromozom yapısı"
            ),
            make_spot_the_lie(
                topic="Düşük materyallerinde sitogenetik dağılım",
                items=[
                    {"text": "Spontan abortus materyallerinde tek başına en sık saptanan karyotip normal karyotiptir.", "isLie": False, "explanation": "Doğrudur; anomaliler parçalı dağıldığı için öploidi tekil olarak en büyüktür."},
                    {"text": "Tüm abortusların %90'ından fazlasında 45,X0 karyotipi saptanır ve öploidi hiç görülmez.", "isLie": True, "explanation": "Tuzak önerme. 45,X0 en sık tekil anomali olsa da oranı yaklaşık %15-20'dir; en sık karyotip ise normal karyotiptir."},
                    {"text": "Normal karyotipli gebelik kayıplarında maternal endokrin veya anatomik patolojiler araştırılmalıdır.", "isLie": False, "explanation": "Doğrudur; fetüs genetik olarak sağlamsa kayıp maternal konak kaynaklı olabilir."}
                ]
            ),
            make_recall(
                question="Genetik incelemesinde normal karyotip (46,XX veya 46,XY) gelen bir erken abortus vakasında araştırılması gereken temel maternal etiyolojiler nelerdir?",
                answer="Uterin anatomik faktörler (sineşi, septus), kontrolsüz endokrinopatiler (diyabet, tiroid hastalıkları), antifosfolipid sendromu ve enfeksiyonlar düşünülmelidir."
            )
        ]
    ))

    # Slide 13
    slides.append(make_slide(
        slide_num=13,
        title="En Sık Tekil Kromozom Anomalisi: 45,X0 (Turner Sendromu)",
        subtitle="Monozomi X tüm kromozomal abortusların yaklaşık %20'sini oluşturur",
        clinical_focus="Paternal cinsiyet kromozomu kaybı ve in utero fetal letalite",
        narrative=(
            "Abortus materyallerinde saptanan patolojik kromozom anomalileri tek tek incelendiğinde en büyük payı tek bir monozomi türü alır.\n\n"
            "- **En Sık Tekil Anomali:** Kromozomal bozukluklar arasında tek başına en sık görülen spesifik anomali **45,X0 (Monozomi X / Turner Sendromu)** tablosudur.\n"
            "- **Fetal Letalite Oranı:** 45,X0 konseptüslerinin yaklaşık **%99'u in utero kaybedilir** ve spontan abortus ile sonuçlanır. Canlı doğuma yalnızca %1'lik son derece kısıtlı bir mozaik veya şanslı grup ulaşabilir.\n"
            "- **Köken Mekanizması:** Olguların çoğunda (%75-80) kaybedilen cinsiyet kromozomu paternal kökenlidir (spermatogenez sırasında oluşan non-disjunction hatası). Maternal yaş ile güçlü bir ilişkisi yoktur.\n\n"
            "> [!IMPORTANT]\n"
            "> Spontan abortuslarda en sık görülen tekil kromozom anomalisi 45,X0 (Turner sendromu) tablosudur."
        ),
        bullets=[
            "Tek başına en sık görülen kromozom anomalisi 45,X0 (Turner sendromu) tablosudur",
            "Kromozomal anomalili düşüklerin yaklaşık %15-20'sinden sorumludur",
            "45,X0 konseptüslerinin %99'u fetal yaşamda spontan abortus ile kaybedilir",
            "Otozomal monozomilerden farklı olarak yaşam siklusunda konseptüs oluşturabilir"
        ],
        elements=[
            make_quiz(
                question="Spontan düşük materyallerinde saptanan sitogenetik defektler içinde tek başına en sık görülen spesifik kromozom anomalisi hangisidir?",
                options=[
                    {"key": "A", "text": "Trizomi 21 (Down Sendromu)", "isCorrect": False, "explanation": "Trizomi 21 canlı doğumlarda sıktır ancak abortuslarda tekil en sık anomali değildir."},
                    {"key": "B", "text": "45,X0 (Turner Sendromu)", "isCorrect": True, "explanation": "Doğru. Abort materyallerinde tek başına en sık izlenen kromozom anomalisi 45,X0 monozomisidir."},
                    {"key": "C", "text": "Trizomi 18 (Edwards Sendromu)", "isCorrect": False, "explanation": "Edwards sendromu ağır bir trizomi olsa da tekil lider değildir."},
                    {"key": "D", "text": "47,XXY (Klinefelter Sendromu)", "isCorrect": False, "explanation": "Klinefelter sendromu abortus materyallerinde nadirdir ve letal seyretmez."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Spontan abortuslarda tek başına en sık görülen kromozom anomalisi 45,X0 karyotipine sahip Turner sendromudur.",
                masked_term="45,X0",
                hint="Monozomi X sitogenetik formülü"
            ),
            make_chain(
                title="45,X0 Oluşumu ve Erken Fetal Kayıp Mekanizması",
                steps=[
                    "Gametogenez Hatası: Gametogenezde paternal veya maternal cinsiyet kromozomunun mayotik ayrılamaması (non-disjunction)",
                    "Monozomi X Fertilizasyonu: Tek X kromozomu taşıyan 45,X0 zigotunun oluşması ve implantasyonu",
                    "Organogenez Yetersizliği: Lenfatik sistem hipoplazisi, kardiyak yetmezlik ve ağır kistik higroma gelişimi",
                    "Spontan Terminasyon: Konseptüslerin %99'unun ilk trimesterde spontan abortus ile uterus dışına atılması"
                ]
            ),
            make_recall(
                question="45,X0 genotipine sahip zigotların in utero sağkalım oranı ne kadardır ve klinik akıbeti nedir?",
                answer="Yaklaşık %99'u intrauterin dönemde spontan abortus ile kaybedilir; sadece %1'i canlı doğuma ulaşarak postnatal Turner sendromu kliniği ile tanınır."
            )
        ]
    ))

    # Slide 14
    slides.append(make_slide(
        slide_num=14,
        title="Otozomal Trizomiler ve Trizomi 16 Özelliği",
        subtitle="Abortuslarda en sık izlenen otozomal trizomi: Trizomi 16",
        clinical_focus="Trizomilerin genel grup liderliği ve Trizomi 16'nın in utero tam letalitesi",
        narrative=(
            "Kromozomal anomalili abortusların yaklaşık yarısını (%50) otozomal trizomiler oluşturur.\n\n"
            "- **En Sık Trizomi:** Spontan abortuslarda trizomiler arasında açık ara **en sık görülen trizomi türü Trizomi 16'dır** (tüm trizomilerin yaklaşık üçte biri).\n"
            "- **Tam Letalite:** Trizomi 16 fetal gelişimle kesinlikle bağdaşmaz. Tıp literatüründe Trizomi 16 ile canlı doğmuş hiçbir olgu bildirilmemiştir; **canlı doğumda ASLA görülmez**.\n"
            "- **Maternal Yaş Duyarlılığı:** Trizomi 16 sıklığı maternal yaşın ilerlemesiyle katlanarak artar. Yaşlı oositlerde mayoz I bölünmesindeki kohezin proteinlerinin zayıflaması 16. kromozomun non-disjunction riskini yükseltir.\n\n"
            "> [!IMPORTANT]\n"
            "> Spontan abortus materyallerinde saptanan trizomilerden en sık görüleni Trizomi 16'dır ve canlı doğumda asla izlenmez."
        ),
        bullets=[
            "Otozomal trizomiler kromozomal abortusların yaklaşık %50'sini oluşturur",
            "Trizomiler arasında en sık görüleni Trizomi 16'dır",
            "Trizomi 16 yaşamla kesinlikle bağdaşmaz ve canlı doğumu yoktur",
            "Anne yaşının ilerlemesi ile Trizomi 16 insidansı belirgin artar"
        ],
        elements=[
            make_quiz(
                question="Spontan abortus materyallerinde saptanan otozomal trizomiler arasında en sık görülen kromozomal anomali hangisidir?",
                options=[
                    {"key": "A", "text": "Trizomi 21", "isCorrect": False, "explanation": "Trizomi 21 canlı doğan bebeklerde en sıktır; düşük materyallerinde Trizomi 16'dan seyrektir."},
                    {"key": "B", "text": "Trizomi 18", "isCorrect": False, "explanation": "Trizomi 18 ikinci en sık canlı trizomidir ancak abortuslarda Trizomi 16'nın gerisindedir."},
                    {"key": "C", "text": "Trizomi 13", "isCorrect": False, "explanation": "Trizomi 13 (Patau) abortuslarda görülür fakat en sık olanı değildir."},
                    {"key": "D", "text": "Trizomi 16", "isCorrect": True, "explanation": "Doğru. Düşüklerde en sık izlenen otozomal trizomi Trizomi 16'dır."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Spontan abortus materyallerinde trizomilerden en sık görüleni Trizomi 16 tablosudur ve canlı doğumu yoktur.",
                masked_term="Trizomi 16",
                hint="Düşüklerde en sık görülen ve canlı doğuma ulaşamayan otozomal anomali"
            ),
            make_table(
                title="Abortuslarda Sık Görülen Sitogenetik Anomaliler",
                headers=["Sitogenetik Anomali", "Sıklık / Pozisyon", "Canlı Doğum Potansiyeli"],
                rows=[
                    [
                        {"text": "Normal Karyotip", "isMasked": False},
                        {"text": "Tekil en sık karyotip", "isMasked": True, "hint": "Tek başına en yüksek orana sahip sitogenetik durum"},
                        {"text": "Sağlıklı bebek doğumu mümkündür", "isMasked": False}
                    ],
                    [
                        {"text": "45,X0 (Turner)", "isMasked": False},
                        {"text": "Tekil en sık anomali", "isMasked": False},
                        {"text": "%1 canlı doğum", "isMasked": True, "hint": "Konseptüslerin çok büyük kısmının in utero kaybedilmesi"}
                    ],
                    [
                        {"text": "Trizomi 16", "isMasked": False},
                        {"text": "En sık trizomi türü", "isMasked": False},
                        {"text": "Asla canlı doğmaz", "isMasked": True, "hint": "Yüzde sıfır sağkalım oranı"}
                    ]
                ]
            ),
            make_recall(
                question="Birinci trimester düşüğü yapan hastanın küretaj materyalinde Trizomi 16 saptanması ne anlama gelir?",
                answer="Kaybın oogenez sırasında rastlantısal bir mayotik non-disjunction hatasından kaynaklandığını, bu anomalinin yaşamla bağdaşmadığını ve sonraki gebelikler için spesifik bir rekürrens riskinin genellikle düşük olduğunu gösterir."
            )
        ]
    ))

    # Slide 15
    slides.append(make_slide(
        slide_num=15,
        title="Canlı Doğuma Ulaşabilen Trizomiler ve Abortus Payı",
        subtitle="Trizomi 21 (Down), Trizomi 18 (Edwards) ve Trizomi 13 (Patau)",
        clinical_focus="Canlı doğan anöploidilerin de aslında büyük oranda in utero elendiği gerçeği",
        narrative=(
            "Pediatri ve klinik genetikte iyi bilinen Trizomi 21, 18 ve 13 olguları spontan abortus serilerinde de önemli bir yer tutar.\n\n"
            "- **İn Utero Doğal Seleksiyon:** Canlı doğabilen trizomik embriyoların da büyük bir kısmı gebelik sırasında kaybedilir. Trizomi 21 konseptüslerinin yaklaşık **%70-80'i**, Trizomi 18 ve 13'ün ise **%95'ten fazlası** spontan abortus veya intrauterin ölüm ile sonuçlanır.\n"
            "- **Abortus Dağılımı:** Düşük materyallerinde Trizomi 22 ve Trizomi 21, Trizomi 16'dan sonra en sık karşılaşılan diğer trizomi gruplarıdır.\n"
            "- **Maternal Yaş Riski:** Bu trizomilerin tamamında anne yaşının 35'in üzerinde olması riski katlar. Ancak Trizomi 16 gibi tamamen letal olanlardan farkları, belirli bir yüzdesinin miada ulaşıp canlı doğabilmesidir.\n\n"
            "> [!NOTE]\n"
            "> Down (21), Edwards (18) ve Patau (13) sendromları canlı doğabilse de konseptüslerinin büyük bölümü ilk trimesterde abortus ile elenir."
        ),
        bullets=[
            "Trizomi 21 konseptüslerinin %70-80'i miada ulaşamadan spontan abortusla kaybedilir",
            "Trizomi 18 ve 13 olgularının %95'ten fazlası intrauterin letalite gösterir",
            "Abort materyallerinde Trizomi 22 ve 21, Trizomi 16'dan sonra sık görülenlerdir",
            "Maternal yaş artışı tüm otozomal trizomilerin ortak risk faktörüdür"
        ],
        elements=[
            make_quiz(
                question="Canlı doğuma ulaşabilen otozomal trizomilerin (Down, Edwards, Patau) intrauterin seyri hakkında hangisi doğrudur?",
                options=[
                    {"key": "A", "text": "Konseptüslerin tamamı miada ulaşır ve düşük görülmez", "isCorrect": False, "explanation": "Aksine Down sendromlu fetüslerin bile %70-80'i in utero elenir."},
                    {"key": "B", "text": "Bu sendromlara sahip embriyoların da büyük çoğunluğu spontan abortus ile sonuçlanır", "isCorrect": True, "explanation": "Doğru. Doğal seleksiyon nedeniyle bu anomalilerin büyük kısmı in utero abortusla elenir."},
                    {"key": "C", "text": "Yalnızca Trizomi 21 düşük yapar, Trizomi 18 ve 13 yapmaz", "isCorrect": False, "explanation": "Trizomi 18 ve 13'ün in utero kaybı Trizomi 21'den çok daha yüksektir (>%95)."},
                    {"key": "D", "text": "Bu trizomiler sadece ikinci trimesterde kaybedilir", "isCorrect": False, "explanation": "Büyük bölümü ilk trimesterde abortusla sonuçlanır."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Canlı doğumla sonuçlanabilen Down sendromuna yol açan Trizomi 21 konseptüslerinin yaklaşık %75 kadarı in utero spontan abortus ile kaybedilir.",
                masked_term="Trizomi 21",
                hint="Down sendromuna neden olan otozomal anöploidi"
            ),
            make_swipe(
                title="Trizomilerin Klinik Karakterizasyonu",
                left_category="Canlı Doğumu Olan Trizomiler",
                right_category="Canlı Doğumu Olmayan Trizomiler",
                cards=[
                    {"text": "Trizomi 21 (Down Sendromu)", "category": "left", "explanation": "Postnatal dönemde yaşayabilen trizomidir."},
                    {"text": "Trizomi 16", "category": "right", "explanation": "Yaşamla kesinlikle bağdaşmaz, canlı doğumu yoktur."},
                    {"text": "Trizomi 18 (Edwards Sendromu)", "category": "left", "explanation": "Canlı doğabilen ancak ağır anomalili trizomidir."},
                    {"text": "Trizomi 13 (Patau Sendromu)", "category": "left", "explanation": "Canlı doğabilen ağır kraniofasiyal anomalili trizomidir."}
                ]
            ),
            make_recall(
                question="Trizomi 21 konseptüslerinin ne kadarı miada ulaşamadan intrauterin dönemde kaybedilir?",
                answer="Yaklaşık %70 ila %80'i erken gebelikte spontan abortus veya intrauterin fetal kayıp ile elenir."
            )
        ]
    ))

    # Slide 16
    slides.append(make_slide(
        slide_num=16,
        title="Abort Materyallerinde ASLA Görülmeyen Trizomiler",
        subtitle="Trizomi 1, 3 ve 19: Preimplantasyonel veya çok erken letalite",
        clinical_focus="Sitogenetik analizde bazı kromozomların hiç saptanmaması ve sınav değeri",
        narrative=(
            "Klinik sitogenetikte ve obstetrik amfi derslerinde altı en kalın çizilen kurallardan biri abort materyalinde hiç rastlanmayan kromozomlardır.\n\n"
            "- **Asla Görülmeyen Üçlü:** Spontan abortus materyallerinde **Trizomi 1, Trizomi 3 ve Trizomi 19 HİÇ GÖRÜLMEZ**.\n"
            "- **Biyolojik Gerekçe:** Bu kromozomlar (özellikle 1 ve 3) devasa boyutlardadır ve hücresel canlılık, mitotik bölünme ve erken embriyogenez için mutlak şart olan yaşamsal genleri kodlar. Bu kromozomlardaki fazlalık zigotun bölünmesini ilk birkaç hücre döngüsünde durdurur.\n"
            "- **Preimplantasyonel Kayıp:** Konseptüs klinik bir gebelik haline gelemeden veya uterus kavitesine implante bile olamadan blastomer evresinde arrest olur. Bu nedenle klinik abortus materyalinde saptanamazlar.\n\n"
            "> [!IMPORTANT]\n"
            "> Spontan abort materyallerinde Trizomi 1, Trizomi 3 ve Trizomi 19 hiçbir zaman saptanmaz; implantasyon öncesi arrest olurlar."
        ),
        bullets=[
            "Abortus materyallerinde Trizomi 1, 3 ve 19 sitogenetik olarak hiç görülmez",
            "Bu kromozomlardaki gen dozaj fazlalığı zigotik evrede bölünmeyi durdurur",
            "Kayıp klinik gebelik tanısı almadan, implantasyon öncesinde gerçekleşir",
            "Sınavlarda en sık sorgulanan sitogenetik mutlak negatiflik bilgisidir"
        ],
        elements=[
            make_quiz(
                question="Spontan abortus materyallerinin sitogenetik incelemesinde aşağıdaki otozomal trizomilerden hangisi HİÇBİR ZAMAN görülmez?",
                options=[
                    {"key": "A", "text": "Trizomi 16", "isCorrect": False, "explanation": "Trizomi 16 düşüklerde en sık görülen trizomidir."},
                    {"key": "B", "text": "Trizomi 22", "isCorrect": False, "explanation": "Trizomi 22 düşüklerde sık rastlanan bir anöploididir."},
                    {"key": "C", "text": "Trizomi 1", "isCorrect": True, "explanation": "Doğru. Trizomi 1, 3 ve 19 abort materyallerinde preimplantasyonel letalite nedeniyle hiç görülmez."},
                    {"key": "D", "text": "Trizomi 15", "isCorrect": False, "explanation": "Trizomi 15 abortuslarda rapor edilen trizomilerdendir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Spontan abortus materyallerinde Trizomi 1, 3 ve Trizomi 19 sitogenetik incelemelerde hiçbir zaman tespit edilemez.",
                masked_term="Trizomi 19",
                hint="Düşük materyallerinde bir ve üç ile birlikte hiç saptanamayan üçüncü otozomal anöploidi grubu"
            ),
            make_spot_the_lie(
                topic="Düşük materyalinde kromozom dağılımları",
                items=[
                    {"text": "Trizomi 16 düşük materyallerinde en sık izlenen otozomal trizomidir.", "isLie": False, "explanation": "Doğrudur; trizomilerin yaklaşık üçte birini oluşturur."},
                    {"text": "Trizomi 1 abortus materyallerinde en sık görülen ve en hafif seyreden trizomidir.", "isLie": True, "explanation": "Tuzak önerme. Trizomi 1 abort materyallerinde HİÇ görülmez; preimplantasyon evrede letaldir."},
                    {"text": "Trizomi 3 ve Trizomi 19 klinik olarak tanınan abortus materyallerinde saptanmaz.", "isLie": False, "explanation": "Doğrudur; bu kromozomlar erken bölünme evresinde embriyoyu arrest eder."}
                ]
            ),
            make_recall(
                question="Abortus materyallerinde asla izlenmeyen üç trizomi hangileridir ve neden klinik düşük olarak materyalde bulunmazlar?",
                answer="Trizomi 1, Trizomi 3 ve Trizomi 19'dur. Gen yoğunluğu ve hayati fonksiyonlar nedeniyle preimplantasyonel dönemde ölümcül olup klinik gebelik aşamasına ulaşamadıkları için materyalde izlenmezler."
            )
        ]
    ))

    # Slide 17
    slides.append(make_slide(
        slide_num=17,
        title="Maternal Yaş Artışı ve Kromozomal Anöploidi Mekanizması",
        subtitle="Oosit mayoz I arresti, kohezin instabilitesi ve non-disjunction",
        clinical_focus="İleri anne yaşı ile trizomi riskinin logaritmik yükselişi",
        narrative=(
            "Maternal yaş, fetal kromozomal anöploidi ve spontan abortus riskinin en güçlü belirleyicisidir.\n\n"
            "- **Biyolojik Mekanizma:** Kadınlarda oositler intrauterin 5. ayda **mayoz I profazında (diploten / diktiyoten evresi)** bölünmeyi durdurur. Ovulasyona kadar geçen 20 ila 45 yıllık bu bekleme süresinde kromatidleri bir arada tutan **kohezin kompleksleri** ve mikrotübül iğ iplikçikleri yaşlanmaya bağlı dejenerasyona uğrar.\n"
            "- **Mayotik Non-Disjunction:** Ovulasyon tetiklendiğinde kromozomlar zıt kutuplara eşit ayrılamaz (**non-disjunction**). Bu durum doğrudan trizomik veya monozomik oositlerin döllenmesine yol açar.\n"
            "- **Klinik Eğri:** 20 yaşındaki bir kadında anöploidik abortus riski %10 civarındayken, 35 yaşında %20'ye, 40 yaşında %40'a ve 45 yaşında %80'in üzerine çıkar.\n\n"
            "> [!NOTE]\n"
            "> İleri anne yaşında oositlerde kohezin proteinlerinin zayıflaması sonucu mayoz I'de non-disjunction sıklığı ve dolayısıyla trizomik abortus oranı katlanarak artar."
        ),
        bullets=[
            "Oositler fetal yaşamdan ovulasyona kadar mayoz I profazında bekler",
            "Yıllar içinde kohezin proteinleri ve iğ iplikçiklerinde yapısal dejenerasyon gelişir",
            "Mayoz I'deki ayrılamama (non-disjunction) trizomik zigot oluşumuna yol açar",
            "Maternal yaş ile 45,X0 değil, özellikle otozomal trizomi sıklığı korelasyon gösterir"
        ],
        elements=[
            make_quiz(
                question="İleri anne yaşında otozomal trizomilere bağlı spontan abortus riskinin belirgin artmasının altında yatan temel hücresel mekanizma hangisidir?",
                options=[
                    {"key": "A", "text": "Endometrium kalınlığının aşırı artarak implantasyonu engellemesi", "isCorrect": False, "explanation": "Anöploidi riski endometriyal değil oosit kaynaklı bir defekttir."},
                    {"key": "B", "text": "Oositlerin on yıllarca mayoz I profazında beklemesi sonucu kohezin kaybı ve non-disjunction", "isCorrect": True, "explanation": "Doğru. Diktiyoten evresinde uzun süre bekleyen oositlerde mayotik non-disjunction gelişir."},
                    {"key": "C", "text": "Spermatogenez sırasında paternal delesyon oranının katlanması", "isCorrect": False, "explanation": "Trizomilerin büyük çoğunluğunda hata maternal oogenez kaynaklıdır."},
                    {"key": "D", "text": "Mitokondriyal DNA'nın tamamen parçalanması", "isCorrect": False, "explanation": "Trizomi doğrudan kromozomal ayrılma kusurudur."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="İleri anne yaşındaki kadınlarda oositlerin mayoz I evresinde ayrılma kusuru yaşaması sonucu otozomal trizomik abortus sıklığı belirgin şekilde yükselir.",
                masked_term="mayoz I",
                hint="Oositlerin doğum öncesi durakladığı ilk mayotik evre"
            ),
            make_chain(
                title="Maternal Yaş ve Anöploidik Abortus Patofizyolojisi",
                steps=[
                    "Uzamış Mayotik Duraklama: Oositlerin fetal dönemden itibaren mayoz I diktiyoten evresinde on yıllarca beklemesi",
                    "Kohezin Dejenerasyonu: Yaşla birlikte kromatidleri bağlayan kohezin proteinlerinin ve iğ ipliklerinin yapısal bozulması",
                    "Mayotik Non-Disjunction: Ovulasyonda kromozomların kutuplara asimetrik çekilmesi ve anöploidik ovum üretimi",
                    "Trizomik Zigot ve Abortus: Döllenme sonrası gelişen embriyoda gen dozaj dengesizliği ve erken gelişimsel arrest"
                ]
            ),
            make_recall(
                question="İleri anne yaşı otozomal trizomileri katlayarak artırırken, en sık monozomi olan 45,X0 (Turner) üzerinde benzer bir yaş etkisi var mıdır?",
                answer="Hayır. 45,X0 olgularının yaklaşık %80'inde kaybedilen cinsiyet kromozomu paternal kökenlidir (sperm kaynaklıdır), bu nedenle maternal yaş ile belirgin bir pozitif korelasyon göstermez."
            )
        ]
    ))

    # Slide 18
    slides.append(make_slide(
        slide_num=18,
        title="Poliploidiler: Triploidi ve Tetraploidi",
        subtitle="Triploidi (69 kromozom, parsiyel mol) ve Tetraploidi (92 kromozom)",
        clinical_focus="Çift sperm fertilizasyonu (dispermi) ve trofoblastik veziküler dejenerasyon",
        narrative=(
            "Kromozomal anomalili spontan abortusların yaklaşık %20'sini tam kromozom takımı katlanmaları olan **poliploidiler** oluşturur.\n\n"
            "- **Triploidi (69 Kromozom):** En sık görülen poliploididir (%15-20). Genellikle tek bir ovumun iki ayrı sperm tarafından döllenmesi (**dispermi**) veya nadiren diploit bir gametin fertilizasyonu ile oluşur. Paternal kökenli olduğunda (**diandrik**) plasentada trofoblastik proliferasyon ve **parsiyel mol hidatiform** gelişir. Maternal kökenli olduğunda (**diginik**) ağır fetal büyüme kısıtlılığı ve küçük plasenta izlenir.\n"
            "- **Tetraploidi (92 Kromozom):** Abortusların yaklaşık %5'inde görülür. Fertilizasyon sonrasında ilk mitotik bölünmede sitokinezin gerçekleşememesi (DNA replike olup hücrenin bölünememesi) sonucu oluşur. Çok erken evrede letaldir.\n\n"
            "> [!IMPORTANT]\n"
            "> Triploidi (69 kromozom) çoğunlukla iki spermin tek ovumu döllemesiyle (dispermi) oluşur ve parsiyel mol tablosuyla birliktelik gösterir."
        ),
        bullets=[
            "Triploidi 69 kromozom taşır ve abortusların yaklaşık %15-20'sinde izlenir",
            "Dispermi (tek ovumun iki spermle fertilizasyonu) en yaygın etiyolojik nedendir",
            "Diandrik triploidi parsiyel mol hidatiform kliniği ile karakterizedir",
            "Tetraploidi (92 kromozom) erken mitotik bölünme yetersizliğinden kaynaklanır"
        ],
        elements=[
            make_quiz(
                question="Spontan abortus materyalinde 69,XXY karyotipi ve plasental hidropik villus dejenerasyonu (parsiyel mol) saptanan bir hastada bu durumun en olası mekanizması hangisidir?",
                options=[
                    {"key": "A", "text": "Ovumun iki ayrı sperm tarafından döllenmesi (Dispermi)", "isCorrect": True, "explanation": "Doğru. Triploidi en sık dispermi (iki spermle fertilizasyon) sonucu oluşur ve parsiyel mol yapabilir."},
                    {"key": "B", "text": "Maternal 21. kromozomun mayozda ayrılamaması", "isCorrect": False, "explanation": "Bu durum Trizomi 21 (Down sendromu) oluşturur, 69 kromozom değil."},
                    {"key": "C", "text": "Zigotun ilk mitozunda hücre bölünmesinin durması", "isCorrect": False, "explanation": "Bu mekanizma 92 kromozomlu tetraploidiye yol açar."},
                    {"key": "D", "text": "Paternal X kromozomunun tamamen kaybolması", "isCorrect": False, "explanation": "Bu durum 45,X0 monozomisine yol açar."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Abortus materyallerinde 69 kromozomlu triploidi oluşumunun en sık mekanizması tek bir ovumun iki spermle döllenmesi yani dispermi durumudur.",
                masked_term="dispermi",
                hint="İki spermin tek yumurtaya girmesi olayı"
            ),
            make_slider(
                left_title="Diandrik Triploidi (Paternal)",
                right_title="Diginik Triploidi (Maternal)",
                left_points=[
                    "Fazla kromozom takımı babadan gelir",
                    "Geniş, kistik ve hidropik plasenta",
                    "Parsiyel mol hidatiform klinik tablosu"
                ],
                right_points=[
                    "Fazla kromozom takımı anneden gelir",
                    "Küçük, sklerotik ve kistsiz plasenta",
                    "Ağır asimetrik fetal gelişme geriliği"
                ]
            ),
            make_recall(
                question="Abortus materyallerinde saptanan 92 kromozomlu tetraploidi döllenme hatası mıdır, mitoz hatası mıdır?",
                answer="Mitoz hatasıdır; normal döllenmiş diploit bir zigotun ilk hücre bölünmesinde kromozomların replike olup sitokinezin (hücre bölünmesinin) gerçekleşememesi sonucu meydana gelir."
            )
        ]
    ))

    # Slide 19
    slides.append(make_slide(
        slide_num=19,
        title="Yapısal Kromozom Anomalileri: Translokasyon ve İnversiyonlar",
        subtitle="Resiprokal ve Robertsonian translokasyon taşıyıcılığı ve dengesiz gametler",
        clinical_focus="Ebeveyn dengeli translokasyonunun embriyoda dengesiz kariyotipe yol açması",
        narrative=(
            "Sayısal kromozom anomalilerinin (anöploidi/poliploidi) yanı sıra yapısal anomaliler de abortuslara neden olur.\n\n"
            "- **Yapısal Hasarlar:** Spontan abortusların yaklaşık %3-6'sında delesyonlar, duplikasyonlar, inversiyonlar veya translokasyonlar saptanır.\n"
            "- **Ebeveyn Taşıyıcılığı:** Ebeveynlerden birinde bulunan **dengeli resiprokal translokasyon** veya akrosentrik kromozomlar (13, 14, 15, 21, 22) arasındaki **Robertsonian translokasyon**, ebeveynde fenotipik hiçbir hastalık yapmaz. Ancak mayoz bölünmede kromozomlar ayrılırken embriyoya **dengesiz (unbalanced)** genetik materyal aktarılır.\n"
            "- **Klinik Sonuç:** Parsiyel monozomi veya parsiyel trizomi ile sonuçlanan bu dengesiz embriyolar genellikle ilk trimesterde spontan abortus ile kaybedilir. Bu patoloji özellikle tekrarlayan gebelik kayıplarında parental karyotip analizinin ana gerekçesidir.\n\n"
            "> [!NOTE]\n"
            "> Fenotipik olarak tamamen sağlıklı bir ebeveyndeki dengeli translokasyon, gametogenezde dengesiz (unbalanced) kromozom dağılımına yol açarak abortusa neden olabilir."
        ),
        bullets=[
            "Yapısal kromozom defektleri abortusların %3-6'sından sorumludur",
            "Dengeli translokasyon taşıyıcısı anne veya baba tamamen sağlıklıdır",
            "Mayozda dengesiz ayrılma (unbalanced segregation) embriyoda letal defekt yapar",
            "Robertsonian translokasyon akrosentrik kromozomlar (13, 14, 15, 21, 22) arasında olur"
        ],
        elements=[
            make_quiz(
                question="Ebeveynlerden birinde dengeli Robertsonian translokasyonu bulunmasının fetüste spontan abortusa yol açma mekanizması hangisidir?",
                options=[
                    {"key": "A", "text": "Uterus içi kan akımının mekanik olarak tıkanması", "isCorrect": False, "explanation": "Translokasyon genetik bir defekttir, uterus vasküler tıkanıklığı yapmaz."},
                    {"key": "B", "text": "Maternal enfeksiyonlara yatkınlığın artması", "isCorrect": False, "explanation": "Translokasyon immün yetmezlik yaratmaz."},
                    {"key": "C", "text": "Mayoz bölünmede dengesiz gamet oluşumu sonucu fetüste parsiyel trizomi veya monozomi gelişmesi", "isCorrect": True, "explanation": "Doğru. Dengeli taşıyıcılık mayozda dengesiz ayrılmaya yol açarak fetal letalite yapar."},
                    {"key": "D", "text": "Fetal eritrositlerin plasentada parçalanması", "isCorrect": False, "explanation": "Eritrosit yıkımı Rh uyuşmazlığında görülür."},
                    {"key": "E", "text": "Plasenta perkreata gelişmesi", "isCorrect": False, "explanation": "İnvazyon anomalisi translokasyon ile ilişkili değildir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Ebeveyndeki dengeli translokasyon mayoz sırasında dengesiz ayrılma göstererek embriyoda ölümcül dengesiz genetik materyale ve abortusa neden olur.",
                masked_term="dengesiz",
                hint="Asimetrik dağılımlı, eksik veya fazla genetik parça içeren durum"
            ),
            make_venn(
                title="Sayısal vs Yapısal Kromozom Anomalileri",
                label_a="Sayısal Anomaliler (Anöploidi/Poliploidi)",
                label_b="Yapısal Anomaliler (Translokasyon/İnversiyon)",
                items=[
                    {"criterion": "Trizomi 16 ve 45,X0 gibi tam kromozom sayısı farkları", "correct": "A", "explanation": "Doğrudan kromozom sayısı değişikliğidir."},
                    {"criterion": "Ebeveyn dengeli taşıyıcılığı nedeniyle embriyoya dengesiz aktarım", "correct": "B", "explanation": "Yapısal translokasyonların klasik patogenezidir."},
                    {"criterion": "İlk trimesterde spontan abortusa yol açabilme potansiyeli", "correct": "both", "explanation": "Her iki anomali türü de gebelik kaybı yapabilir."}
                ]
            ),
            make_recall(
                question="Tekrarlayan düşük yapan bir çiftte anne veya babada dengeli translokasyon saptanırsa klinik yönetimde ne önerilir?",
                answer="Genetik danışmanlık ve preimplantasyon genetik tanı (PGT) ile dengeli/öploid embriyoların seçilerek transfer edildiği tüp bebek (IVF) tedavisi önerilir."
            )
        ]
    ))

    # Slide 20 (Checkpoint 2)
    slides.append(make_slide(
        slide_num=20,
        title="[TEKRAR SAYFASI - CHECKPOINT 2] Fetal Genetik ve Kromozomal Etiyoloji",
        subtitle="Sayısal anomaliler, sıklık kuralları, letal trizomiler ve yaş faktörü",
        clinical_focus="Düşüklerin sitogenetik profilinin kapsamlı entegrasyonu",
        narrative=(
            "Bu checkpoint sayfası, spontan abortusların fetal genetik altyapısını ve sınavların en kritik sitogenetik spotlarını pekiştirir.\n\n"
            "- **Trimester Dağılımı:** Kromozomal kusur oranı ilk trimesterde **%70**, ikinci trimesterde **%30'dur**.\n"
            "- **En Sık Tablolar:** Abortus materyalinde tekil olarak en sık karyotip **normal karyotip (öploidi)**; en sık tekil anomali **45,X0 (Turner)**; en sık otozomal trizomi **Trizomi 16'dır**.\n"
            "- **Mutlak Negatifler:** **Trizomi 1, 3 ve 19** abort materyalinde preimplantasyonel letalite nedeniyle **HİÇ GÖRÜLMEZ**.\n"
            "- **Yaş ve Poliploidi:** İleri anne yaşı mayoz I non-disjunction ile trizomileri artırırken; triploidi çoğunlukla iki spermin tek ovumu döllemesiyle (**dispermi**) oluşur ve parsiyel molle ilişkilidir.\n\n"
            "> [!IMPORTANT]\n"
            "> Tekil en sık: Normal Karyotip | En sık anomali: 45,X0 | En sık trizomi: Trizomi 16 | Asla görülmeyenler: Trizomi 1, 3 ve 19."
        ),
        bullets=[
            "İlk trimesterde %70, ikinci trimesterde %30 kromozomal defekt izlenir",
            "En sık karyotip: Normal karyotip; En sık anomali: 45,X0; En sık trizomi: Trizomi 16",
            "Trizomi 1, 3 ve 19 klinik abortus materyalinde asla bulunmaz",
            "Triploidi en sık dispermi ile oluşur; ileri anne yaşı otozomal trizomileri artırır"
        ],
        elements=[
            make_quiz(
                question="Spontan abortus sitogenetiği ile ilgili aşağıdaki eşleştirmelerden hangisi KESİNLİKLE YANLIŞTIR?",
                options=[
                    {"key": "A", "text": "Tek başına en sık saptanan spesifik anomali — 45,X0 (Turner)", "isCorrect": False, "explanation": "Doğru eşleştirmedir; tekil en sık kromozomal anomali 45,X0'dır."},
                    {"key": "B", "text": "Otozomal trizomiler arasında en sık görülen — Trizomi 16", "isCorrect": False, "explanation": "Doğru eşleştirmedir; trizomilerin yaklaşık %30'undan fazlası Trizomi 16'dır."},
                    {"key": "C", "text": "Düşük materyalinde en sık izlenen ve canlı doğabilen trizomi — Trizomi 1", "isCorrect": True, "explanation": "Yanlış eşleştirme (Doğru cevap). Trizomi 1 abort materyalinde HİÇBİR ZAMAN görülmez."},
                    {"key": "D", "text": "Düşük materyallerinde en sık rastlanan tekil karyotip — Normal karyotip", "isCorrect": False, "explanation": "Doğru eşleştirmedir; parçalı anomalilere karşı öploidi en büyüktür."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Spontan abortuslarda trizomilerden en sık görüleni Trizomi 16 iken, abortus materyalinde Trizomi 1, 3 ve 19 asla görülmez.",
                masked_term="Trizomi 16",
                hint="Düşüklerde en sık saptanan otozomal anöploidi"
            ),
            make_table(
                title="Fetal Sitogenetik Altın Özeti (Checkpoint 2)",
                headers=["Kategori", "Spesifik Anomali / Durum", "Klinik Özellik"],
                rows=[
                    [
                        {"text": "Tekil En Sık Karyotip", "isMasked": False},
                        {"text": "Normal Karyotip (Öploidi)", "isMasked": True, "hint": "Sitogenetik kusur taşımayan standart genetik yapı"},
                        {"text": "Maternal nedenler sorgulanmalıdır", "isMasked": False}
                    ],
                    [
                        {"text": "En Sık Kromozom Anomalisi", "isMasked": False},
                        {"text": "45,X0 (Turner Sendromu)", "isMasked": True, "hint": "Tek X kromozomu taşıyan monozomi"},
                        {"text": "%99 in utero letaldir", "isMasked": False}
                    ],
                    [
                        {"text": "En Sık Otozomal Trizomi", "isMasked": False},
                        {"text": "Trizomi 16", "isMasked": False},
                        {"text": "Canlı doğumu kesinlikle yoktur", "isMasked": True, "hint": "Yüzde sıfır sağkalım oranı"}
                    ],
                    [
                        {"text": "Hiç Görülmeyen Trizomiler", "isMasked": False},
                        {"text": "Trizomi 1, 3 ve 19", "isMasked": True, "hint": "İmplantasyon öncesi letal olan üçlü grup"},
                        {"text": "Preimplantasyonel arrest olurlar", "isMasked": False}
                    ]
                ]
            ),
            make_spot_the_lie(
                topic="Bölüm 2 kazanımları",
                items=[
                    {"text": "İlk trimester spontan abortuslarında genetik anomali oranı ikinci trimestere göre çok daha yüksektir.", "isLie": False, "explanation": "Doğrudur; ilk trimesterde %70, ikinci trimesterde %30'dur."},
                    {"text": "Trizomi 16, canlı doğumlarda en sık saptanan ve hafif mental retardasyon yapan bir anomalidir.", "isLie": True, "explanation": "Tuzak önerme. Trizomi 16 yaşamla kesinlikle bağdaşmaz ve canlı doğumu ASLA yoktur; abortuslarda en sıktır."},
                    {"text": "45,X0 monozomisi taşıyan embriyoların yaklaşık %99'u abortusla kaybedilir.", "isLie": False, "explanation": "Doğrudur; canlı doğuma sadece %1'lik grup ulaşabilir."}
                ]
            ),
            make_branching(
                scenario="İlk trimesterde küretaj yapılan bir hastanın tahliye materyali sitogenetik analize gönderiliyor. Patoloji raporundaki kromozom sonucuna göre klinik yaklaşım belirlenecektir.",
                options=[
                    {
                        "text": "Trizomi 16 saptandığında sonraki gebelikler için rutin takip önerilir, tekrarlama riski genel olarak düşüktür.",
                        "isCorrect": True,
                        "feedback": "Doğru karar. Trizomi 16 rastlantısal oosit mayoz I non-disjunction hatasıdır, spesifik parental rekürrens göstermez."
                    },
                    {
                        "text": "Normal karyotip (46,XX) saptandığında başka hiçbir araştırma yapmaya gerek yoktur, gebelik kesinlikle tesadüfen düşmüştür.",
                        "isCorrect": False,
                        "feedback": "Yanlış. Normal karyotip varlığında maternal anatomik, immünolojik veya endokrin nedenler araştırılmalıdır."
                    },
                    {
                        "text": "Dengesiz translokasyon saptandığında anne ve babaya test yapılmadan hemen kemoterapi başlanmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış. Dengesiz translokasyonda parental periferik karyotip analizi yapılır, kemoterapi endikasyonu yoktur."
                    }
                ]
            ),
            make_recall(
                question="Birinci trimesterde kaybedilen bir gebelik ile ikinci trimesterde kaybedilen bir gebelik sitogenetik beklenti açısından nasıl farklılaşır?",
                answer="İlk trimester kayıplarında %70 oranında kromozomal anomali (Trizomi 16, 45,X0 vb.) beklenirken; ikinci trimester kayıplarında genetik anomali oranı %30'a geriler ve servikal yetmezlik, enfeksiyon veya anatomik uterin nedenler ön plana çıkar."
            )
        ]
    ))

    return slides
