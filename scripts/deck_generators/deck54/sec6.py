"""
Deck 54 - Section 6: Ektopik Gebelik ve Tubal Patoloji (Slayt 51-60)
Slayt 60: Checkpoint 6
"""

from meds.scripts.deck_generators.deck54.deck54_helper import (
    make_slide, make_quiz, make_cloze, make_table, make_chain,
    make_recall, make_spot_the_lie, make_slider, make_swipe, make_venn, make_branching
)

def get_sec6_slides():
    slides = []
    
    # Slide 51
    slides.append(make_slide(
        slide_num=51,
        title="Ektopik Gebelik: Tanım, Sıklık ve Anatomik Yerleşim",
        subtitle="Gebeliklerin %1'i ve %90'dan fazlasında tubal lokalizasyon",
        clinical_focus="Ektopik implantasyon sahaları ve ampuller yerleşim",
        narrative=(
            "Ektopik gebelik, döllenmiş bir ovumun (blastokistin) normal uterin kavite içindeki endometrium tabakası dışında herhangi bir anatomik bölgeye implante olmasıdır. "
            "Tüm klinik gebeliklerin yaklaşık **%1'inde** izlenir ve ilk trimester maternal ölümlerinin en sık nedenidir.\n\n"
            "- **Tubal Baskınlık:** Ektopik gebelik olgularının **%90'ından fazlasında implantasyon Fallop tüplerindedir (tubal gebelik)**. Tubal yerleşimler içinde de en sık tüpün en geniş ve fertilizasyonun gerçekleştiği bölgesi olan **ampulla (%70-80)** tutulur (bunu isthmus ve fimbria izler).\n"
            "- **Diğer Nadir Lokalizasyonlar:** Olguların kalan <%10'luk dilimi over (ovaryan), karın boşluğu (abdominal), servikal kanal veya tüpün uterus myometriumu içinden geçen intramural bölümünde (**interstisyel/kornual gebelik**) yerleşir.\n"
            "- **İnterstisyel Tehlike:** İnterstisyel tubal gebelik myometrium damarlarına çok yakın olduğu için rüptüre olduğunda en katastrofik masif kanamaya yol açan formdur.\n\n"
            "> [!IMPORTANT]\n"
            "> Ektopik gebelik tüm gebeliklerin yaklaşık %1'inde görülür ve bu olguların %90'ından fazlasında implantasyon Fallop tüplerindedir."
        ),
        bullets=[
            "Fertilize ovumun normal uterin kavite dışına implantasyonudur",
            "Tüm klinik gebeliklerin yaklaşık %1'inde izlenir",
            "Olguların %90'ından fazlasında yerleşim Fallop tüplerindedir (tubal)",
            "Nadir bölgeler: Over, batın boşluğu, serviks ve interstisyel tuba"
        ],
        elements=[
            make_quiz(
                question="Ektopik gebeliğin tüm klinik gebelikler içindeki genel görülme oranı ve en sık saptandığı anatomik organ hangisidir?",
                options=[
                    {"key": "A", "text": "Gebeliklerin %20'si — Myometrium düz kası", "isCorrect": False, "explanation": "İnsidans %1'dir; myometriumda intramural gebelik son derece istisnaidir."},
                    {"key": "B", "text": "Gebeliklerin %5'i — Douglas peritonu", "isCorrect": False, "explanation": "Abdominal implantasyon çok nadirdir (<%1)."},
                    {"key": "C", "text": "Gebeliklerin %1'i — Fallop tüpleri (tubal gebelik)", "isCorrect": True, "explanation": "Doğru. Ektopik gebelik tüm gebeliklerin %1'inde görülür ve vakaların %90'ından fazlası Fallop tüplerine (tubal) yerleşir."},
                    {"key": "D", "text": "Gebeliklerin %0.01'i — Vajen arka duvarı", "isCorrect": False, "explanation": "Vajende implantasyon olmaz."},
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Ektopik gebelik tüm gebeliklerin yüzde 1 kadarında görülür ve bu olguların yüzde 90 kadarından fazlasında implantasyon tüplerdedir.",
                masked_term="yüzde 90",
                hint="Tubal yerleşimin tüm ektopik olgular içindeki ezici sıklık payı"
            ),
            make_table(
                title="Ektopik Gebelik Anatomik Yerleşim Dağılımı",
                headers=["Lokalizasyon", "Görülme Oranı", "Klinik Özellik"],
                rows=[
                    [
                        {"text": "Fallop Tüpleri (Tubal)", "isMasked": False},
                        {"text": "Olguların %90'ından fazlası", "isMasked": True, "hint": "Ezici çoğunluktaki yüzde dilimi"},
                        {"text": "En sık ampuller bölge; rüptür riski yüksektir", "isMasked": False}
                    ],
                    [
                        {"text": "İnterstisyel / Kornual", "isMasked": False},
                        {"text": "Olguların %2-3'ü", "isMasked": True, "hint": "Tüpün uterus içi geçiş payı"},
                        {"text": "Uterin arter dallarına yakın, en ölümcül kanama tipi", "isMasked": False}
                    ],
                    [
                        {"text": "Ovaryan ve Abdominal", "isMasked": False},
                        {"text": "Olguların <%2'si", "isMasked": False},
                        {"text": "Batın içi periton veya over yüzeyi implantasyonu", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Tüpün uterus duvarı içinden geçen parçasında gelişen ektopik gebelik tipine ne ad verilir ve neden en tehlikelidir?",
                answer="İnterstisyel (kornual) gebelik denir; zengin miyometriyal damar ağına komşu olduğu için rüptüründe çok ağır ölümcül kanama yapar."
            )
        ]
    ))

    # Slide 52
    slides.append(make_slide(
        slide_num=52,
        title="Ektopik Gebelik: Etiyoloji ve Kronik Salpenjit Rolü",
        subtitle="Tüp motilitesinin bozulması, siliyer hasar ve lüminal darlık",
        clinical_focus="Ektopik gebeliğin en sık nedeni olan inflamatuar tubal hasar",
        narrative=(
            "Fertilize ovumun tubal ampulladan uterusa olan 3-4 günlük fizyolojik yolculuğu, tubal mukozanın siliyer aktivitesi ve düz kas peristaltizmi ile sağlanır. Bu mekanik veya siliyer iletimi geciktiren her türlü patoloji ektopik gebeliğe zemin hazırlar.\n\n"
            "- **En Sık Neden (Kronik İnflamasyon):** Ektopik gebelik olgularının **yaklaşık yarısında (%50) temel neden tüplerdeki geçirilmiş kronik inflamatuar değişikliklerdir (kronik salpenjit)**.\n"
            "- **Pelvik İnflamatuar Hastalık (PİH):** Başta Chlamydia trachomatis ve Neisseria gonorrhoeae olmak üzere PİH atakları tubal plikaları birbirine yapıştırarak 'çıkmaz sokaklar' (folliküler salpenjit) oluşturur ve silyaları tahrip eder; blastokist uterusa ulaşamadan tüpte takılı kalır ve implante olur.\n"
            "- **Diğer Nedenler:** Uterin leiomyomlar veya endometriozis odaklarının tüpe dıştan bası yapması, geçirilmiş tubal cerrahi ve peritubal adezyonlar ovumun geçişini mekanik olarak zorlaştırır.\n\n"
            "> [!IMPORTANT]\n"
            "> Ektopik gebeliğin en sık nedeni geçirilmiş pelvik inflamatuar hastalığa bağlı kronik tubal inflamatuar hasardır (olguların yaklaşık %50'sinde saptanır)."
        ),
        bullets=[
            "Ovumun tüpten uterusa geçişini geciktiren her faktör zemin hazırlar",
            "Olguların yaklaşık yarısında en sık neden kronik tubal inflamasyondur",
            "Klamidya ve gonore kaynaklı PİH plika yapışıklığı ve siliyer hasar yapar",
            "Endometriozis, leiomyom basısı ve cerrahi skar diğer mekanik nedenlerdir"
        ],
        elements=[
            make_quiz(
                question="Ektopik gebelik patogenezinde fertilize ovumun tubal lümenden uterusa geçişini engelleyerek olguların yaklaşık %50'sinde en sık saptanan etiyolojik faktör hangisidir?",
                options=[
                    {"key": "A", "text": "Aşırı progesteron salgılayan luteal kist", "isCorrect": False, "explanation": "Luteal kist gebeliğin doğal sonucudur; tubal obstrüksiyon yapmaz."},
                    {"key": "B", "text": "Kromozom 6 ve 12 yeniden düzenlenmeleri", "isCorrect": False, "explanation": "Bu sitogenetik bozukluk leiomyom patogenezine aittir."},
                    {"key": "C", "text": "Plasenta battledore insersiyonu", "isCorrect": False, "explanation": "Kordon varyasyonudur; tubal transportu etkilemez."},
                    {"key": "D", "text": "Geçirilmiş pelvik inflamatuar hastalığa bağlı kronik tubal inflamatuar değişiklikler", "isCorrect": True, "explanation": "Doğru. Olguların yaklaşık yarısında ektopik gebeliğin en sık nedeni geçirilmiş PİH ve kronik salpenjit hasarıdır."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Ovumun tüplerden uterusa geçişini geciktiren durumlarda olguların yaklaşık yarısında gecikme tüplerdeki kronik inflamatuar değişikliklerin varlığına bağlıdır.",
                masked_term="kronik inflamatuar değişikliklerin",
                hint="Geçirilmiş pelvik enfeksiyonların tüpte bıraktığı fibröz iltihabi hasar"
            ),
            make_chain(
                "Tubal Ektopik Gebelik Patogenez Zinciri",
                [
                    "1. Asendan Salpenjit: Klamidya veya gonore enfeksiyonu Fallop tüpü endosalpinkste akut inflamasyon ve plika hasarı başlatır.",
                    "2. Fibröz Plika Füzyonu: Kronikleşen iltihap tubal plikaları birbirine yapıştırarak kör cepler ve siliyer epitel kaybı meydana getirir.",
                    "3. Blastokist Tuzaklanması: Döllenen ovum mekanik engeli aşamaz, 6. günde tüp mukozasına tutunarak tubal implantasyonu başlatır."
                ]
            ),
            make_recall(
                question="Klinikte ektopik gebelik geçirme riski en yüksek olan hasta grubu hangi enfeksiyon öyküsüne sahiptir?",
                answer="Geçirilmiş Pelvik İnflamatuar Hastalık (PİH / kronik salpenjit) öyküsü olan kadınlardır."
            )
        ]
    ))

    # Slide 53
    slides.append(make_slide(
        slide_num=53,
        title="Tubal Patoloji: Hematosalpinks ve Lokal Genişleme",
        subtitle="Tüp duvarı erozyonu, hematom ve 3-4 cm'lik kitle oluşumu",
        clinical_focus="Rüptür öncesi Fallop tüpündeki morfolojik değişiklikler",
        narrative=(
            "Fallop tüpü ince, mukozal katlantıları olan dar bir organdır ve endometriuma kıyasla trofoblastik invazyonu sınırlayacak koruyucu kalın bir desidua tabakasından yoksundur.\n\n"
            "- **Trofoblastik Erozyon:** İmplante olan blastokistin trofoblastları Fallop tüpünün ince mukozasını ve kas tabakasını hızla aşındırır. Submukozal damarların yırtılması tüp lümeni içinde kan birikmesine (**hematosalpinks**) yol açar.\n"
            "- **Lokal Genişleme (3-4 cm):** Tuba lümeni, içinde gri-beyaz süngerimsi plasental doku parçaları, embriyonik yapılar ve taze pıhtılaşmış koyu kırmızı kan kitleleri birikmesi nedeniyle lokalize olarak **3-4 cm çapa kadar genişleyebilir**.\n"
            "- **Hematoperitoneum Başlangıcı:** Kanama fimbrial uçtan periton boşluğuna sızarak douglas boşluğunda hematom oluşturabilir.\n\n"
            "> [!NOTE]\n"
            "> Tubal gebelikte trofoblastik erozyon tuba içi hematoma (hematosalpinks) yol açar ve tuba kitle etkisiyle lokal olarak 3-4 cm'e kadar genişler."
        ),
        bullets=[
            "Tüpte koruyucu kalın desidua tabakası bulunmaz",
            "Trofoblastlar tuba duvarını hızla aşındırarak damarları deler",
            "Lümende kan toplanmasıyla hematosalpinks gelişir",
            "Tuba kan pıhtısı ve koryon dokusuyla lokal olarak 3-4 cm genişler"
        ],
        elements=[
            make_quiz(
                question="Tubal ektopik gebelikte trofoblastların tuba duvarını aşındırması sonucu lümende kan birikmesi ve tüpün lokalize genişlemesi ile ilgili aşağıdaki morfolojik terim hangisidir?",
                options=[
                    {"key": "A", "text": "Pyosalpinks", "isCorrect": False, "explanation": "Pyosalpinks tüpün cerahat (püy) ile dolmasıdır; ektopik kanama hematosalpinkstir."},
                    {"key": "B", "text": "Hidrosalpinks", "isCorrect": False, "explanation": "Hidrosalpinks steril seröz sıvı toplanmasıdır."},
                    {"key": "C", "text": "Hematosalpinks", "isCorrect": True, "explanation": "Doğru. Tubal gebelikte damar erozyonuna bağlı tuba lümeninin kanla dolmasına hematosalpinks denir."},
                    {"key": "D", "text": "Koryoamnionit", "isCorrect": False, "explanation": "Plasental membran iltihabıdır."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Tubal gebeliklerde plasental doku tuba duvarını aşındırarak tuba içi hematomu olan hematosalpinks tablosuna neden olabilir.",
                masked_term="hematosalpinks",
                hint="Fallop tüpü lümeninin kan pıhtılarıyla dolması"
            ),
            make_table(
                title="Tubal Lümen Genişleme Parametreleri",
                headers=["Patolojik Aşama", "Lüminal İçerik", "Tüp Çapı Değişimi"],
                rows=[
                    [
                        {"text": "Normal Fallop Tüpü", "isMasked": False},
                        {"text": "Minimal seröz sıvı", "isMasked": False},
                        {"text": "Birkaç milimetre (dar lümen)", "isMasked": False}
                    ],
                    [
                        {"text": "Ektopik Hematosalpinks", "isMasked": False},
                        {"text": "Pıhtılaşmış kan ve koryon villusları", "isMasked": True, "hint": "Hematom ve plasental parçalar"},
                        {"text": "Lokal olarak 3-4 cm'e kadar genişleme", "isMasked": True, "hint": "Üç ila dört santimetre boyut"}
                    ]
                ]
            ),
            make_recall(
                question="Tubal gebelik nedeniyle opere edilen bir hastada cerrahın Fallop tüpünde gördüğü lokal genişlemenin tipik çapı kaç santimetredir?",
                answer="Taze kan pıhtısı ve plasental dokuyla lokal olarak yaklaşık 3-4 cm'e kadar genişlemiş bir kitle izlenir."
            )
        ]
    ))

    # Slide 54
    slides.append(make_slide(
        slide_num=54,
        title="Ektopik Gebelik: Histopatolojik Tanı Kriterleri",
        subtitle="Koryon villusları, trofoblastlar ve Arias-Stella reaksiyonu",
        clinical_focus="Küretaj ve salpenjektomi materyalinde patolojik tanı basamakları",
        narrative=(
            "Ektopik gebeliğin kesin patolojik tanısı, Fallop tüpü rezeksiyon materyalinde veya tubal içerikte spesifik gebelik dokularının gösterilmesine dayanır.\n\n"
            "- **Koryon Villusları ve Embriyo:** Histolojik tanının altın standardı doku kesitlerinde **koryonik villusların** ve daha seyrek olarak embriyonik/fetal parçaların gösterilmesidir. Çoğu olguda embriyo erken rezorbe olduğu için tanı villuslara dayanır.\n"
            "- **Uterin Küretaj Tuzağı:** Ektopik gebelik şüphesiyle yapılan endometrial küretajda villus izlenmez; çünkü villuslar tüptedir. Uterus endometriumunda sadece gebelik hormonlarına (yüksek progesteron) yanıt olarak gelişen **desidual reaksiyon** izlenir.\n"
            "- **Arias-Stella Reaksiyonu:** Endometrial gland epitelinde yüksek hormon etkisiyle çekirdeklerde hiperkromatizm, büyüme ve sitoplazmada berraklaşma ile karakterize atipi taklidi lezyondur; karsinomla karıştırılmamalıdır.\n\n"
            "> [!IMPORTANT]\n"
            "> Ektopik gebeliğin kesin histolojik tanısı tuba kesitlerinde koryon villuslarının (veya embriyonun) gösterilmesine dayanır; uterusta villus bulunmaz."
        ),
        bullets=[
            "Kesin tanı tuba kesitinde koryon villuslarının gösterilmesidir",
            "Embriyo dokusu olguların ancak bir kısmında saptanabilir",
            "Endometrial küretajda koryon villusu KESİNLİKLE bulunmaz",
            "Uterusta desidua ve hipersekretuar Arias-Stella reaksiyonu izlenir"
        ],
        elements=[
            make_quiz(
                question="Tubal ektopik gebelik şüphesiyle salpenjektomi yapılan bir hastada patoloğun mikroskop altında kesin tanıyı koyabilmesi için aradığı patognomonik yapı hangisidir?",
                options=[
                    {"key": "A", "text": "Puro biçimli nükleuslu düz kas fasikülleri", "isCorrect": False, "explanation": "Bu yapı miyomda görülür."},
                    {"key": "B", "text": "Koryonik villuslar (veya embriyo dokusu)", "isCorrect": True, "explanation": "Doğru. Ektopik gebeliğin kesin histopatolojik tanısı tüp lümeni veya duvarında koryon villuslarının gösterilmesine bağlıdır."},
                    {"key": "C", "text": "Endometrium bazalisin myometriuma derin invazyonu", "isCorrect": False, "explanation": "Bu adenomyozis tanımıdır."},
                    {"key": "D", "text": "Wharton jeli içinde tek umbilikal arter", "isCorrect": False, "explanation": "Kordon anomalisidir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Tubal gebelik kesitlerinde histolojik tanı villuslar ve seyrek olarak embriyonun görülmesine bağlıdır.",
                masked_term="villuslar",
                hint="Plasental parankimin temel histolojik birimleri"
            ),
            make_branching(
                scenario="6 haftalık amenoresi ve pozitif gebelik testi olan 29 yaşındaki kadına anormal uterin kanama nedeniyle endometrial küretaj yapılıyor. Patoloji raporunda: 'Yaygın desidualize stroma ve Arias-Stella değişiklikleri izlenmiş olup koryon villusu veya trofoblastik doku saptanmamıştır' deniyor. Bu hastada patoloğun uyarısı ne olmalıdır?",
                options=[
                    {"text": "Uterus kavitesinde villus olmaksızın desidua görülmesi dış gebeliği (ektopik gebelik) düşündürür; acil adneksiyel USG yapılmalıdır.", "isCorrect": True, "feedback": "Kesinlikle doğru. Uterus içi desidual reaksiyona rağmen kavitede koryon villusunun bulunmaması ektopik gebeliğin klasik küretaj bulgusudur."},
                    {"text": "Hasta kesinlikle gebe değildir, işlem sonlandırılabilir.", "isCorrect": False, "feedback": "Hatalı. Pozitif gebelik testi ve desidua gebeliği kanıtlar; villus olmaması dış gebeliği gösterir."},
                    {"text": "Hastada kesin endometrial adenokarsinom vardır.", "isCorrect": False, "feedback": "Yanlış. Arias-Stella selim bir gebelik atipisi taklididir; karsinom değildir."}
                ]
            ),
            make_recall(
                question="Ektopik gebelikte yüksek hormon seviyeleri nedeniyle uterus endometrial glandlarında izlenen atipi taklitçisi hipersekretuar epitel değişikliğine ne ad verilir?",
                answer="Arias-Stella reaksiyonu (Arias-Stella fenomeni) adı verilir."
            )
        ]
    ))

    # Slide 55
    slides.append(make_slide(
        slide_num=55,
        title="Tubal Rüptür ve Akut Batın Katastrofisi",
        subtitle="Ani pelvik ağrı, masif intraabdominal kanama ve hipovolemik şok",
        clinical_focus="Ektopik gebeliğin hayatı tehdit eden cerrahi acil tablosu",
        narrative=(
            "Tüp duvarının elastikiyet kapasitesi sınırlıdır. Koryonik villuslar tüp duvarını tamamen delip incelttiğinde veya hematom içi basınç kritik seviyeyi aştığında (genellikle 6-8. gebelik haftalarında) **tubal rüptür** meydana gelir.\n\n"
            "- **Akut Batın Tablosu:** Rüptür anında hasta aniden bıçak saplanır tarzda, çok şiddetli alt karın ve pelvik ağrı hisseder. Periton içine fışkıran kan hızla hemoperitoneuma ve yaygın peritoneal irritasyona (defans ve rebaund) yol açar.\n"
            "- **Hemodinamik Çöküş ve Şok:** Kısa sürede 1000-1500 mL'yi aşabilen batın içi kanama; tansiyon düşüklüğü (hipotansiyon), taşikardi, soğuk terleme, senkop ve derin **hipovolemik şok** tablosu doğurur.\n"
            "- **Acil Cerrahi:** Tubal rüptür dakikalar içinde anne hayatını sonlandırabilecek jinekolojik bir felakettir; gecikmeksizin acil cerrahi eksplorasyon (laparoskopi/laparotomi ve salpenjektomi) gerektirir.\n\n"
            "> [!IMPORTANT]\n"
            "> Ektopik gebelik rüptürü ani şiddetli karın ağrısı, akut batın ve derin hipovolemik şok tablosuyla prezente olur; acil cerrahi girişim hayat kurtarıcıdır."
        ),
        bullets=[
            "Genellikle 6-8. haftalarda tüp duvarının delinmesiyle gelişir",
            "Bıçak saplanır tarzda ani, şiddetli pelvik ağrı ile başlar",
            "Masif intraabdominal kanama (hemoperitoneum) ve peritonit yapar",
            "Derin hipovolemik şok ve senkopa yol açar; acil cerrahi şarttır"
        ],
        elements=[
            make_quiz(
                question="6 haftalık gebelik şüphesi olan genç bir kadında aniden başlayan bıçak saplanır tarzda alt karın ağrısı, taşikardi, tansiyon 70/40 mmHg ve ultrasonda batında yaygın serbest sıvı saptanması durumunda ilk düşünülmesi gereken acil cerrahi antite hangisidir?",
                options=[
                    {"key": "A", "text": "Submukoz leiomyom dejenerasyonu", "isCorrect": False, "explanation": "Submukoz miyom menoraji yapar; akut batın ve hemoperitoneum yapmaz."},
                    {"key": "B", "text": "Battledore plasenta ayrılması", "isCorrect": False, "explanation": "Battledore doğumda kord avülsiyonu yapabilir; 6. haftada görülmez."},
                    {"key": "C", "text": "Rüptüre tubal ektopik gebelik", "isCorrect": True, "explanation": "Doğru. Ani şiddetli ağrı, periton içi serbest kanama ve hipovolemik şok rüptüre ektopik gebeliğin klasik tablosudur."},
                    {"key": "D", "text": "Koryoamnionit krizi", "isCorrect": False, "explanation": "Korioamnionit ileri haftalarda ateş ve pürülan akıntıyla seyreder; hemoperitoneum yapmaz."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Ektopik gebeliğin rüptürü durumunda birden bire karın ağrısı ve akut batın tablosu ortaya çıkar ve devamında çok ağır bir şok tablosu gelişir.",
                masked_term="akut batın",
                hint="Periton irritasyonu ve masif kanamayla karakterize cerrahi tablo"
            ),
            make_chain(
                "Tubal Rüptür ve Hemodinamik Çöküş Zinciri",
                [
                    "1. Tubal Duvar İncilmesi: Trofoblastik proteazlar tüpün ince serozasını tamamen perfore eder.",
                    "2. Damar Yırtılması ve Hemoperitoneum: Uterin-tubal anastomoz damarları yırtılır; periton boşluğuna masif arteryel kan boşalır.",
                    "3. Hipovolemik Şok: İntravasküler volüm hızla tükenir; hipotansiyon, bilinç kaybı ve kardiyovasküler kollaps gelişir."
                ]
            ),
            make_recall(
                question="Tubal ektopik gebelik rüptüründe periton içi masif kanamayı gösteren fizik muayene bulgusu nedir?",
                answer="Karında yaygın rebaund/defans, servikal hareketlerde aşırı hassasiyet ve vajinal fornikste dolgunluktur (douglasta hematom)."
            )
        ]
    ))

    # Slide 56
    slides.append(make_slide(
        slide_num=56,
        title="Preeklampsi: Tanım ve Klinik Triad",
        subtitle="Hipertansiyon, ödem ve proteinüri birlikteliği (3. trimester)",
        clinical_focus="Gebelik toksemisinin klinik kriterleri ve eklampsi eşiği",
        narrative=(
            "Preeklampsi (eski adıyla gebelik toksemisi), gebeliğe özgü, sistemik endotel hasarıyla seyreden multisistemik bir sendromdur. "
            "Klasik olarak gebeliğin **üçüncü trimesterinde (20. gebelik haftasından sonra)** ortaya çıkar.\n\n"
            "- **Klinik Triad:** Tanı üç temel klinik bulgunun bir arada görülmesiyle konur: **1) Hipertansiyon (kan basıncı ≥140/90 mmHg)**, **2) Belirgin periferik ödem (özellikle el, yüz ve pretibial bölgede)** ve **3) Proteinüri (24 saatlik idrarda ≥300 mg protein)**.\n"
            "- **Epidemiyoloji:** Tüm gebeliklerin yaklaşık **%5-10'unda** görülür. Özellikle ilk gebeliğini yaşayan (primipar) ve **35 yaş üzeri** kadınlarda insidansı belirgin şekilde artar.\n"
            "- **Eklampsi Ayrımı:** Preeklampsi tablosuna santral sinir sistemi tutulumuna bağlı **jeneralize grand-mal konvülsiyonların (nöbetlerin) eklenmesi 'eklampsi'** olarak tanımlanır.\n\n"
            "> [!IMPORTANT]\n"
            "> Preeklampsi 3. trimesterde hipertansiyon, ödem ve proteinüri triadı ile tanımlanır; bu tabloya konvülsiyonların eklenmesi 'eklampsi'dir."
        ),
        bullets=[
            "Gebeliğin 3. trimesterinde (20. haftadan sonra) gelişir",
            "Klinik triad: Hipertansiyon, periferik ödem ve proteinüri",
            "Tüm gebeliklerin %5-10'unda; primipar >35 yaş kadınlarda sıktır",
            "Tabloya jeneralize konvülsiyonlar eklenirse eklampsi adını alır"
        ],
        elements=[
            make_quiz(
                question="Gebeliğin 3. trimesterinde tansiyon yüksekliği saptanan bir kadında 'preeklampsi' tanısını kesinleştiren klasik klinik triad hangi seçenekte eksiksiz verilmiştir?",
                options=[
                    {"key": "A", "text": "Hipertansiyon, hiperglisemi ve hematüri", "isCorrect": False, "explanation": "Hiperglisemi diyabettir; hematüri nefritiktir."},
                    {"key": "B", "text": "Hipotansiyon, sarılık ve oligüri", "isCorrect": False, "explanation": "Preeklampside hipotansiyon değil hipertansiyon olur."},
                    {"key": "C", "text": "Hipertansiyon, ödem ve proteinüri", "isCorrect": True, "explanation": "Doğru. Preeklampsinin klasik klinik triadı hipertansiyon, ödem ve proteinüridir."},
                    {"key": "D", "text": "Vajinal akıntı, kaşıntı ve ateş", "isCorrect": False, "explanation": "Vajinit/servisit tablosudur."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Gebeliğin üçüncü trimesterinde hipertansiyon, ödem ve proteinüri bulgularının izlenmesi ile oluşan tabloya preeklampsi denir.",
                masked_term="hipertansiyon, ödem ve proteinüri",
                hint="Kan basıncı yükselmesi, doku şişliği ve albüminüri birlikteliği"
            ),
            make_slider(
                left_title="Preeklampsi Tablosu",
                right_title="Eklampsi Tablosu",
                left_points=[
                    "Kan basıncı ≥140/90 mmHg, el-yüzde ödem, proteinüri",
                    "Santral sinir sistemi irritasyonu (baş ağrısı, görme bulanıklığı)",
                    "Konvülsiyon (nöbet) KESİNLİKLE yoktur"
                ],
                right_points=[
                    "Hipertansiyon, ödem ve proteinüriye ek olarak nöbetler başlar",
                    "Jeneralize tonik-klonik grand-mal konvülsiyonlar gelişir",
                    "DİC, serebral kanama ve maternal mortalite riski çok yüksektir"
                ]
            ),
            make_recall(
                question="Preeklampsi tablosunu eklampsiye dönüştüren kritik klinik semptom nedir?",
                answer="Hipertansiyon, ödem ve proteinüri zemininde hastada jeneralize konvülsiyonların (nöbetlerin) başlamasıdır."
            )
        ]
    ))

    # Slide 57
    slides.append(make_slide(
        slide_num=57,
        title="Preeklampsi Patogenezi: Spiral Arteriollerde Yetersiz Dilatasyon",
        subtitle="Muskuloelastik tabakanın korunamaması ve plasental iskemi",
        clinical_focus="Preeklampsinin kök nedeni olan trofoblastik invazyon defekti",
        narrative=(
            "Preeklampsinin tüm klinik bulgularının altında yatan temel patofizyolojik defekt plasentanın uteroplasental damar yatağında gerçekleşir.\n\n"
            "- **Normal Gebelik Fizyolojisi:** Normal bir gebelikte ekstravillöz trofoblastlar miyometriyal spiral arteriolleri istila eder; damarların düz kas ve elastik tabakasını yıkarak yerini fibrinöz materyalle doldurur. Böylece spiral arterler yüksek dirençli dar borulardan, **düşük dirençli, geniş çaplı kıvrıntılı vasküler sinüzoidlere** dönüşür ve plasentaya bol maternal kan akımı sağlanır.\n"
            "- **Preeklampsideki Defekt:** Preeklampside trofoblastların invazyonu yüzeysel kalır; **spiral arteriollerin muskuloelastik duvarı aynen korunur**. Damarlar genişleyemez, lümenleri dar ve yüksek dirençli kalır.\n"
            "- **Plasental Hipoperfüzyon:** Kan plasentaya yeterince ulaşamaz; organ kronik iskemiye sürüklenir.\n\n"
            "> [!IMPORTANT]\n"
            "> Preeklampside tüm olguların temel özelliği, uteroplasental yataktaki spiral arteriollerde yetersiz dilatasyona bağlı maternal kan akımının plasentaya ulaşamamasıdır."
        ),
        bullets=[
            "Tüm olguların temel defekti spiral arteriollerdeki yetersiz dilatasyondur",
            "Normalde trofoblastlar muskuloelastik duvarı yıkarak damarları genişletir",
            "Preeklampside muskuloelastik duvar sağlam kalır ve damarlar dar kalır",
            "Sonuçta kronik plasental hipoperfüzyon ve iskemi meydana gelir"
        ],
        elements=[
            make_quiz(
                question="Preeklampsinin patogenezinde tüm klinik belirtileri başlatan uteroplasental yataktaki temel morfolojik ve fonksiyonel vasküler bozukluk nedir?",
                options=[
                    {"key": "A", "text": "Spiral arteriollerde yetersiz dilatasyona bağlı maternal kan akımının plasentaya ulaşamaması", "isCorrect": True, "explanation": "Doğru. Spiral arteriollerin genişleyememesi ve muskuloelastik duvarın aynen kalarak darlığı sürdürmesi preeklampsinin temel patofizyolojik zeminidir."},
                    {"key": "B", "text": "Umbilikal vende konjenital anevrizmatik genişleme", "isCorrect": False, "explanation": "Umbilikal kord anomalisidir; preeklampsi patogeneziyle ilgisizdir."},
                    {"key": "C", "text": "Spiral arteriollerin muskuloelastik duvarının korunamayıp yırtılması", "isCorrect": False, "explanation": "Tam tersine; preeklampside muskuloelastik duvar sağlam kalır ve damar genişleyemez."},
                    {"key": "D", "text": "Amniyotik kavitede aşırı sıvı birikimi (polihidramnios)", "isCorrect": False, "explanation": "Fetal anomalilerle ilgilidir; spiral arter patolojisi değildir."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Tüm preeklampsi olgularında temel özellik, uteroplasental yataktaki spiral arteriollerdeki yetersiz dilatasyona bağlı maternal kan akımının plasentaya yeterince ulaşamamasıdır.",
                masked_term="spiral arteriollerdeki yetersiz dilatasyona",
                hint="Maternal uteroplasental damarların genişleyememe kusuru"
            ),
            make_chain(
                "Preeklampsi İskemik Başlangıç Zinciri",
                [
                    "1. Yetersiz Trofoblastik Göç: Ekstravillöz trofoblastlar myometrial spiral arter duvarlarına yeterince penetre olamaz.",
                    "2. Damar Duvarının Sert Kalması: Spiral arteriollerin kalın muskuloelastik tabakası korunur; lümenler dar ve yüksek dirençli kalır.",
                    "3. Plasental Hipoperfüzyon: İntervillöz aralığa gelen kan akımı dramatik şekilde azalır; plasentada kronik hipoksi ve iskemi tetiklenir."
                ]
            ),
            make_recall(
                question="Normal bir gebelikte spiral arteriollerin muskuloelastik duvarının fibrinöz materyalle dolmasının fizyolojik sonucu nedir?",
                answer="Damarların genişleyerek direncinin düşmesi ve plasentaya bol miktarda anne kanının zahmetsizce akmasıdır."
            )
        ]
    ))

    # Slide 58
    slides.append(make_slide(
        slide_num=58,
        title="Preeklampsi Sistemik Komplikasyonları: Endotel Hasarı, DİC ve Enfarktlar",
        subtitle="Doku faktörü, tromboksan salınımı ve akut aterozis histolojisi",
        clinical_focus="İskemik plasentadan salınan faktörlerin maternal organlara etkisi",
        narrative=(
            "Spiral arteriolleri dar kalan iskemik plasenta, maternal dolaşıma toksik vazoaktif ve prokoagülan faktörler salgılar.\n\n"
            "- **Vazodilatör Kaybı ve Hipertansiyon:** Trofoblastlar tarafından nitrik oksit ve prostasiklin gibi vazodilatörlerin üretimi azalır; maternal sistemik vazokonstrüksiyon ve şiddetli hipertansiyon gelişir.\n"
            "- **Doku Faktörü ve DİC:** İskemik plasenta doku faktörü ve tromboksan salarak anne kanında yaygın mikrovasküler trombüsleri tetikler; tüketim koagülopatisi (**DİC**) ve yaygın organ nekrozları meydana gelir.\n"
            "- **Plasental İnfarktüsler:** Normal gebelikte nadir olan infarktlar, preeklampsili gebelerin **1/3'ünde çok sayıda** görülür; hastaların **%15'inde retroplasental hematomlar (ablasyo plasenta)** izlenir.\n"
            "- **Akut Aterozis:** Uterin spiral damarlarda fibrinoid nekroz, duvar kalınlaşması ve köpüksü lipid yüklü makrofaj birikimi (**akut aterozis**) patognomoniktir.\n\n"
            "> [!IMPORTANT]\n"
            "> İskemik plasentadan doku faktörü ve tromboksan salınması DİC'e yol açar; spiral arterlerde akut aterozis (lipid yüklü makrofajlar ve fibrinoid nekroz) izlenir."
        ),
        bullets=[
            "Vazodilatör azalması maternal sistemik hipertansiyonu tetikler",
            "Doku faktörü ve tromboksan salınımı yaygın DİC ve organ nekrozu yapar",
            "Hastaların 1/3'ünde çok sayıda plasental infarkt, %15'inde retroplasental kanama olur",
            "Spiral arterlerde akut aterozis (lipidli makrofajlar ve fibrinoid nekroz) izlenir"
        ],
        elements=[
            make_quiz(
                question="Şiddetli preeklampsi ve eklampsi zemininde iskemik plasenta tarafından salınan doku faktörü ve tromboksanın maternal dolaşımda tetiklediği en ölümcül hematolojik komplikasyon hangisidir?",
                options=[
                    {"key": "A", "text": "Otoimmün hemolitik anemi", "isCorrect": False, "explanation": "Antikor kaynaklıdır; preeklampsinin primer komplikasyonu değildir."},
                    {"key": "B", "text": "Dissemine intravasküler koagülasyon (DİC)", "isCorrect": True, "explanation": "Doğru. Doku faktörü ve tromboksan salınımı yaygın mikrovasküler tromboza ve tüketim koagülopatisine (DİC) yol açar."},
                    {"key": "C", "text": "Aplastik anemi", "isCorrect": False, "explanation": "Kemik iliği kök hücre yetmezliğidir."},
                    {"key": "D", "text": "Kronik lenfositik lösemi", "isCorrect": False, "explanation": "Malign lenfoproliferatif hastalıktır."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="İskemik plasenta dokusundan doku faktörü ve tromboksan salınması ölümcül intravasküler koagülasyon gelişimine zemin hazırlar.",
                masked_term="intravasküler koagülasyon",
                hint="Tüketim hemostaz bozukluğu ve yaygın mikrotrombüs süreci (DİC)"
            ),
            make_table(
                title="Preeklampsi Histopatolojik Vasküler Bulguları",
                headers=["Damarsal / Doku Alanı", "Gözlenen Patoloji", "Klinik Sonuç"],
                rows=[
                    [
                        {"text": "Spiral Arter Duvarı", "isMasked": False},
                        {"text": "Akut aterozis ve fibrinoid nekroz", "isMasked": True, "hint": "Lipidli köpük hücreleri ve damar ölümü"},
                        {"text": "Damar lümeninde daralma ve tromboz", "isMasked": False}
                    ],
                    [
                        {"text": "Plasenta Parankimi", "isMasked": False},
                        {"text": "Çok sayıda iskemik infarkt", "isMasked": True, "hint": "Olguların üçte birinde belirgin doku nekrozu"},
                        {"text": "Fetal büyüme geriliği ve hipoksi", "isMasked": False}
                    ],
                    [
                        {"text": "Retroplasental Yatak", "isMasked": False},
                        {"text": "Hematom ve kanama (%15)", "isMasked": False},
                        {"text": "Ablasyo plasenta (erken ayrılma)", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Preeklampsili bir hastanın desidual damarlarında mikroskop altında izlenen ve aterosklerozu taklit eden 'akut aterozis' lezyonunun içeriği nedir?",
                answer="Damar duvarında fibrinoid nekroz, kalınlaşma ve lümende toplanan köpüksü lipid yüklü makrofaj kümeleridir."
            )
        ]
    ))

    # Slide 59
    slides.append(make_slide(
        slide_num=59,
        title="Plasental Gross Anomaliler: Akreta, İnkreta ve Perkreta",
        subtitle="Desidua yokluğu, myometriyal invazyon derinliği ve rüptür riski",
        clinical_focus="Plasentanın anormal yapışma dereceleri ve postpartum kanama",
        narrative=(
            "Normal doğumda bebek doğduktan sonra plasenta, desidua spongioza tabakasından ayrılarak dışarı atılır. Ancak desidua tabakasının yetersiz olduğu durumlarda koryon villusları doğrudan myometriuma yapışır veya içine girer.\n\n"
            "- **Temel Kusur:** Desidua bazalisin parsiyel veya komplet yokluğudur; en sık geçirilmiş sezaryen veya küretaj skarları üzerinde gelişir. Plasenta doğumdan sonra ayrılamaz; masif postpartum kanama ve hayatı tehdit eden şok doğurur.\n"
            "- **Üç Anatomik Derece:**\n"
            "  * **Plasenta Akreta:** En sık görülen formdur (%80). Desidua yokluğunda koryon villusları süperfisyel olarak myometriumun yüzeyine yapışmıştır; kas içine girmemiştir.\n"
            "  * **Plasenta İnkreta:** Koryon villusları myometrium kas liflerinin derinliklerine girmiş, kas duvarı boyunca ilerlemiş fakat serozayı aşmamıştır.\n"
            "  * **Plasenta Perkreta:** Koryon villusları myometriumun tüm katmanlarını aşarak dış seroza örtüsüne ve hatta komşu organlara (özellikle mesane duvarına) kadar ulaşmıştır; uterin rüptüre neden olabilir.\n\n"
            "> [!IMPORTANT]\n"
            "> Akreta myometrium yüzeyine yapışma, inkreta kas içine girme, perkreta ise serozayı aşıp komşu organlara ulaşmadır; doğum sonu masif kanama yaparlar."
        ),
        bullets=[
            "Temel kusur koruyucu desidua tabakasının yokluğudur",
            "Akreta: Villusların süperfisyel myometriuma yapışmasıdır",
            "İnkreta: Villusların myometrium kas tabakası içine girmesidir",
            "Perkreta: Villusların myometriumu aşıp serozaya ulaşmasıdır; rüptür yapar"
        ],
        elements=[
            make_quiz(
                question="Plasentanın koryon villuslarının myometriumun tüm kalınlığını aşarak dış seroza tabakasına ulaştığı ve hatta mesaneye invaze olabildiği en ağır plasental yapışma anomalisi hangisidir?",
                options=[
                    {"key": "A", "text": "Plasenta akreta", "isCorrect": False, "explanation": "Akreta süperfisyel kas yüzeyine yapışmadır; serozayı aşmaz."},
                    {"key": "B", "text": "Plasenta perkreta", "isCorrect": True, "explanation": "Doğru. Perkreta villusların tüm myometriumu aşarak serozaya ve çevre organlara ulaşmasıdır."},
                    {"key": "C", "text": "Plasenta inkreta", "isCorrect": False, "explanation": "İnkreta kas içine girer fakat serozayı aşmaz."},
                    {"key": "D", "text": "Battledore plasenta", "isCorrect": False, "explanation": "Kordon marjinal insersiyonudur; invazyon anomalisi değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Plasental villusların myometrium duvarını aşarak serozaya kadar gelmesi ve rüptür riski doğurması perkreta olarak tanımlanır.",
                masked_term="perkreta",
                hint="Serozayı aşan en derin plasental invazyon anomalisi"
            ),
            make_slider(
                left_title="Plasenta Akreta vs İnkreta",
                right_title="Plasenta Perkreta",
                left_points=[
                    "Akreta: Süperfisyel myometrium yüzeyine doğrudan yapışma",
                    "İnkreta: Myometrium kas tabakasının içine derinlemesine girme",
                    "Lezyonlar uterus kas duvarı sınırları içinde kalır"
                ],
                right_points=[
                    "Perkreta: Myometrium duvarını tamamen delip serozaya ulaşma",
                    "Mesane ve çevre pelvik organlara invazyon gösterebilir",
                    "Doğumda spontan uterin rüptür ve katastrofik kanama yapar"
                ]
            ),
            make_recall(
                question="Plasenta akreta, inkreta ve perkretanın ortaya çıkışındaki ortak primer histopatolojik eksiklik nedir?",
                answer="Koryon villusları ile kas tabakası arasında yer alması gereken maternal desidua tabakasının yokluğudur."
            )
        ]
    ))

    # Slide 60 - Checkpoint 6
    slides.append(make_slide(
        slide_num=60,
        title="[TEKRAR SAYFASI - CHECKPOINT 6] Ektopik Gebelik, Preeklampsi ve İmplantasyon",
        subtitle="Bölüm 6 Kapsamlı Pekiştirme ve Kazanım Kontrolü",
        clinical_focus="Ektopik gebelik etiyolojisi, preeklampsi patogenezi ve plasenta akreta spektrumu özeti",
        narrative=(
            "Bu tekrar sayfası, 51-59. adımlarda işlenen Ektopik Gebelik, Preeklampsi ve Plasental İmplantasyon Anomalileri kazanımlarını pekiştirmek için düzenlenmiştir.\n\n"
            "- **Ektopik Gebelik:** Gebeliklerin %1'inde görülür ve %90'ından fazlası Fallop tüplerindedir. En sık neden geçirilmiş pelvik enfeksiyonlara bağlı kronik tubal hasardır. Damar erozyonu hematosalpinks ve 3-4 cm kitle yapar; rüptür akut batın ve şok doğurur. Kesin tanı koryon villuslarının görülmesidir; küretajda villus bulunmaz.\n"
            "- **Preeklampsi ve Eklampsi:** 3. trimesterde hipertansiyon, ödem ve proteinüri triadıdır; konvülsiyon eklenirse eklampsi olur. Temel patoloji spiral arteriollerde yetersiz dilatasyondur (muskuloelastik duvar korunur). İskemik plasenta doku faktörü salarak DİC'e yol açar; damarlarda akut aterozis izlenir.\n"
            "- **İmplantasyon Anomalileri:** Desidua yokluğunda gelişir. Akreta kas yüzeyine yapışma, inkreta kas içine girme, perkreta ise serozayı aşıp komşu organlara ulaşmadır.\n\n"
            "> [!NOTE]\n"
            "> Ektopik gebelik %90 tüptedir; preeklampsi spiral arter dilatasyon yetersizliğidir; perkreta myometriumu aşıp serozaya ulaşan en derin yapışma anomalisidir."
        ),
        bullets=[
            "Ektopik gebelik: %90 tüptedir; en sık sebep kronik tubal hasardır; rüptür şok yapar",
            "Kesin ektopik tanı: Tuba kesitinde koryon villusları; uterin küretajda villus yoktur",
            "Preeklampsi triadı: Hipertansiyon, ödem, proteinüri; +konvülsiyon = eklampsi",
            "Preeklampsi temeli: Spiral arterlerde yetersiz dilatasyon, iskemi, akut aterozis, DİC",
            "İmplantasyon anomalileri: Desidua yokluğu; akreta (yapışma), inkreta (kas içi), perkreta (seroza aşımı)"
        ],
        elements=[
            make_quiz(
                question="Ektopik gebelik ve preeklampsinin patolojik temelleri hakkında aşağıdaki ifadelerden hangisi doğru bir sınav spotudur?",
                options=[
                    {"key": "A", "text": "Ektopik gebeliğin kesin tanısı uterin küretajda bol koryon villusu gösterilmesine dayanır.", "isCorrect": False, "explanation": "Yanlış. Ektopik gebelikte uterusta villus bulunmaz; villuslar tüptedir."},
                    {"key": "B", "text": "Preeklampsinin kök patolojisi, spiral arteriollerin aşırı genişleyerek anne kanını tüketmesidir.", "isCorrect": False, "explanation": "Yanlış. Temel patoloji yetersiz dilatasyondur; damarlar dar kalır."},
                    {"key": "C", "text": "Ektopik gebeliklerin %90'ından fazlası tüplerdedir ve preeklampsinin temelinde spiral arteriollerin yetersiz dilatasyonu yatar.", "isCorrect": True, "explanation": "Doğru. Her iki bilginin kombinasyonu amfi notunun temel sınav spotudur."},
                    {"key": "D", "text": "Plasenta perkreta desiduanın aşırı kalınlaşmasıyla koryon villuslarının atrofiye uğramasıdır.", "isCorrect": False, "explanation": "Yanlış. Perkreta desidua yokluğunda villusların serozayı aşmasıdır."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Preeklampsi kliniğine santral sinir sistemi konvülsiyonlarının eklenmesi tablonun eklampsi olarak adlandırılmasına neden olur.",
                masked_term="eklampsi",
                hint="Nöbetlerle seyreden ölümcül gebelik toksemisi tablosu"
            ),
            make_table(
                title="Bölüm 6 Temel Klinik & Patolojik Özellikler",
                headers=["Klinik Tablo", "Temel Patoloji Mekanizması", "Majör Komplikasyon"],
                rows=[
                    [
                        {"text": "Tubal Ektopik Gebelik", "isMasked": False},
                        {"text": "Kronik tubal inflamasyon hasarı", "isMasked": True, "hint": "Geçirilmiş pelvik enfeksiyon skarı"},
                        {"text": "Tubal rüptür, hemoperitoneum ve şok", "isMasked": False}
                    ],
                    [
                        {"text": "Preeklampsi", "isMasked": False},
                        {"text": "Spiral arteriollerde yetersiz dilatasyon", "isMasked": True, "hint": "Miyometriyal damarların dar kalması"},
                        {"text": "DİC, serebral kanama ve eklampsi", "isMasked": False}
                    ],
                    [
                        {"text": "Plasenta Perkreta", "isMasked": False},
                        {"text": "Myometriumu aşıp serozaya ulaşma", "isMasked": True, "hint": "Tüm kas katmanlarını delip dış zara çıkma"},
                        {"text": "Uterin rüptür ve masif postpartum kanama", "isMasked": False}
                    ]
                ]
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 6 Kontrol Önermeleri",
                items=[
                    {"text": "Ektopik gebelik olgularının %90'ından fazlasında implantasyon Fallop tüplerindedir.", "isLie": False, "explanation": "Doğru. Tubal yerleşim ezici çoğunluktadır."},
                    {"text": "Preeklampside spiral arterlerin muskuloelastik duvarı aynen kalır ve damarlar dar kalır.", "isLie": False, "explanation": "Doğru. Patofizyolojinin temelidir."},
                    {"text": "Plasenta akretada koryon villusları mesaneyi delerek idrar yollarından dışarı sarkar.", "isLie": True, "explanation": "Tuzak! Kas tabakasını aşıp mesaneye ulaşan lezyon plasenta perkretadır; akreta sadece süperfisyel myometrium yüzeyine yapışmadır."},
                    {"text": "Tubal gebelik rüptürü akut batın tablosu ve hipovolemik şokla acil cerrahi gerektirir.", "isLie": False, "explanation": "Doğru. Hayatı tehdit eden cerrahi acildir."}
                ]
            ),
            make_recall(
                question="Checkpoint 6: Plasentanın anormal yapışma spektrumunda akreta, inkreta ve perkretanın myometriumdaki anatomik derinlik sınırlarını sıralayınız.",
                answer="Akreta süperfisyel myometrium yüzeyine yapışır; inkreta myometrium kası içine girer; perkreta ise myometriumu tamamen aşıp serozaya ulaşır."
            )
        ],
        is_checkpoint=True,
        checkpoint_number=6
    ))
    
    return slides
