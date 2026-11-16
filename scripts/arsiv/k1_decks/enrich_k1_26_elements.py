# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 26: Genetik, Pediatrik ve Çevresel Patoloji
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
İnteraktif Eleman Zenginleştirme ve %8.0 Çeşitlilik Dengeleme Modülü.
Tüm 7 interaktif eleman tipinin en az %8.0 oranına ulaşmasını sağlar.
"""

from scripts.k1_26_deck_data.helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_extra_branching():
    """Branching logic (klinik ve patolojik karar senaryoları) ögeleri (29 adet)."""
    return {
        2: make_branching_logic(
            "Bir tıp öğrencisi insan genom projesi verilerini incelerken protein kodlayan genlerin toplam genomun sadece %1.5'ini oluşturduğunu öğreniyor.",
            "Bu durum insan biyolojisinin karmaşıklığının nasıl sağlandığı konusunda hangi temel mekanizmayı ön plana çıkarır?",
            [
                {
                    "text": "Alternatif uçbirleştirme (splicing) ve translasyon sonrası protein modifikasyonlarının tek bir genden çok sayıda farklı fonksiyonel protein üretmesi",
                    "isCorrect": True,
                    "explanation": "Doğrudur; insan proteomu gen sayısıyla değil, alternatif uçbirleştirme ve post-translasyonel modifikasyonlarla çeşitlendirilir."
                },
                {
                    "text": "İnsan hücrelerinin bakteriler gibi sürekli plazmid DNA transferi yapması",
                    "isCorrect": False,
                    "explanation": "Hatalı; plazmid transferi prokaryotlara özgüdür, insan genom mimarisiyle ilişkisizdir."
                },
                {
                    "text": "Geriye kalan %98.5'lik DNA'nın hiçbir transkripsiyonel aktivite göstermemesi",
                    "isCorrect": False,
                    "explanation": "Hatalı; kodlamayan bölgelerden miRNA ve lncRNA gibi çok sayıda düzenleyici transkript sentezlenir."
                }
            ]
        ),
        4: make_branching_logic(
            "Laboratuvarda bir onkogenin aşırı ekspresyonunu baskılamak amacıyla 22 nükleotidlik sentetik bir mikroRNA (miRNA) tasarlanıyor.",
            "Bu miRNA'nın hücre sitoplazmasında hedef mRNA'yı susturabilmesi için birleşmesi gereken temel protein kompleksi hangisidir?",
            [
                {
                    "text": "RISC (RNA-induced silencing complex) protein kompleksi",
                    "isCorrect": True,
                    "explanation": "Doğrudur; miRNA'lar tek iplik halinde RISC kompleksine yüklenerek hedef mRNA'nın 3'-UTR bölgesine kilitlenir ve translasyonu baskılar."
                },
                {
                    "text": "Proteazom 26S kompleksi",
                    "isCorrect": False,
                    "explanation": "Hatalı; proteazom ubikitinlenmiş proteinleri yıkar, mRNA susturması yapmaz."
                },
                {
                    "text": "DNA Polimeraz III holoenzimi",
                    "isCorrect": False,
                    "explanation": "Hatalı; DNA polimeraz replikasyon enzimidir."
                }
            ]
        ),
        6: make_branching_logic(
            "Kardiyoloji servisinde akut koroner sendrom geçiren bir hastaya klopidogrel başlanması planlanıyor. Ancak hastada hepatik CYP2C19 geninde fonksiyon kaybı yapan homozigot SNP saptanıyor.",
            "Bu farmakogenomik bilginin ışığında hastada nasıl bir klinik risk beklenir ve ne yapılmalıdır?",
            [
                {
                    "text": "Klopidogrel bir ön ilaçtır; CYP2C19 inaktif olunca aktif metabolitine dönüşemez, trombosit inhibisyonu sağlanamaz ve stent trombozu riski artar; alternatif antiagregan (prasugrel/tikagrelor) seçilmelidir",
                    "isCorrect": True,
                    "explanation": "Kusursuz Farmakogenomik Değerlendirme: Klopidogrel CYP2C19 ile aktive edilir; yavaş metabolize edicilerde ilaç etkisiz kalır."
                },
                {
                    "text": "İlaç vücutta birikerek şiddetli kanama yapar; doz yarıya indirilmelidir",
                    "isCorrect": False,
                    "explanation": "Hatalı; ön ilaç aktive edilemediği için kanama değil tromboz riski doğar."
                }
            ]
        ),
        8: make_branching_logic(
            "Miyelodisplastik sendromlu (MDS) yaşlı bir hastada tümör baskılayıcı gen promotörlerinde yaygın hipermetilasyon saptanıyor.",
            "Bu hastada susturulmuş genlerin yeniden transkripsiyona açılmasını sağlamak için hangi mekanizmayla çalışan epigenetik ilaç tercih edilmelidir?",
            [
                {
                    "text": "DNA metiltransferaz (DNMT) inhibitörü olan Azasitidin veya Desitabin",
                    "isCorrect": True,
                    "explanation": "Doğrudur; DNMT inhibitörleri DNA replikasyonu sırasında metilasyonun aktarılmasını engelleyerek promotörleri hipometile eder ve koruyucu genleri uyandırır."
                },
                {
                    "text": "Yüksek doz folik asit ve B12 vitamini takviyesi",
                    "isCorrect": False,
                    "explanation": "Hatalı; folat tek karbon vericisidir ve metilasyon substratını artırabilir, epigenetik demetilasyon yapmaz."
                }
            ]
        ),
        12: make_branching_logic(
            "Ailesel hiperkolesterolemi tanısı alan bir ailenin pedigri analizinde, babada ve 3 çocuğunun 2'sinde ağır koroner ateroskleroz ve tendon ksantomları saptanıyor; anne ise tamamen sağlıklıdır.",
            "Bu hastalığın kalıtım modeli ve etkilenen moleküler mekanizma nedir?",
            [
                {
                    "text": "Otozomal Dominant kalıtım; LDL reseptör geninde mutasyon ve heterozigotlarda haployetmezlik",
                    "isCorrect": True,
                    "explanation": "Doğrudur; ailesel hiperkolesterolemi klasik OD hastalıktır, her gebelikte %50 risk taşır ve reseptör haployetmezliği ile seyreder."
                },
                {
                    "text": "X'e bağlı resesif kalıtım; sadece erkek çocuklarda görülür",
                    "isCorrect": False,
                    "explanation": "Hatalı; ailesel hiperkolesterolemi otozomaldir, kız çocukları da eşit etkilenir."
                }
            ]
        ),
        14: make_branching_logic(
            "Hemofili A tanılı bir erkeğin genetik danışmanlık görüşmesinde çocuk sahibi olma planı tartışılıyor. Eşi genetik olarak tamamen normaldir.",
            "Bu ailenin doğacak çocuklarının hastalık ve taşıyıcılık durumu nasıl olacaktır?",
            [
                {
                    "text": "Doğacak tüm erkek çocukları tamamen sağlıklı olacaktır; tüm kız çocukları ise zorunlu asemptomatik taşıyıcı olacaktır",
                    "isCorrect": True,
                    "explanation": "Kusursuz Genetik Bilgi: Baba erkek çocuklarına Y kromozomunu verdiği için hastalık aktarılamaz; kızlarına ise mutant X kromozomunu verir."
                },
                {
                    "text": "Erkek çocukların %50'si hemofili hastası olacaktır",
                    "isCorrect": False,
                    "explanation": "Hatalı; babadan oğula X'e bağlı geçiş imkansızdır."
                }
            ]
        ),
        16: make_branching_logic(
            "Marfan sendromlu genç bir sporcuda ekokardiyografide aort kökü çapının 46 mm'ye genişlediği (aort kökü dilatasyonu) saptanıyor.",
            "Bu hastada patofizyolojik olarak aşırı serbest kalan TGF-beta sinyalini baskılayarak aort genişlemesini yavaşlatmak için rehberlerde önerilen ilaç grubu hangisidir?",
            [
                {
                    "text": "Anjiyotensin Reseptör Blokörleri (Losartan) ve Beta-blokerler",
                    "isCorrect": True,
                    "explanation": "Doğrudur; Losartan AT1 reseptörünü bloke ederek TGF-beta sinyal kaskadını doğrudan zayıflatır; beta blokerler ise sistolik darbe basıncını düşürür."
                },
                {
                    "text": "Yüksek doz kalsiyum ve D vitamini infüzyonu",
                    "isCorrect": False,
                    "explanation": "Hatalı; kalsiyum aort dilatasyonunu durduramaz."
                }
            ]
        ),
        18: make_branching_logic(
            "Uzun boylu, zayıf, parmakları aşırı uzun 17 yaşındaki bir gencin göz muayenesinde bilateral lens subluksasyonu saptanıyor. Biyokimyada idrarda homosistin negatif bulunuyor.",
            "Lens subluksasyonunun süperotemporal (yukarı-dışa) yönde olması hangi kesin tanıyı destekler?",
            [
                {
                    "text": "FBN1 mutasyonuna bağlı Marfan Sendromu",
                    "isCorrect": True,
                    "explanation": "Doğrudur; Marfan'da siliyer zonül zayıflığı lensi yukarı-dışa çeker; homosistinüride ise aşağı-içe yer değiştirir."
                },
                {
                    "text": "Sistationin beta-sentaz eksikliğine bağlı Homosistinüri",
                    "isCorrect": False,
                    "explanation": "Hatalı; homosistinüride lens aşağı-içe sublukse olur ve idrarda homosistin pozitiftir."
                }
            ]
        ),
        22: make_branching_logic(
            "Kistik fibrozis şüphesi olan 4 aylık bir bebeğin genetik analizinde homozigot Delta-F508 (Phe508del) mutasyonu doğrulanıyor.",
            "Bu mutasyonun CFTR proteininde yol açtığı primer hücresel kusur nedir ve yeni nesil modülatör ilaçlar (Lumakaftor) bu kusuru nasıl düzeltir?",
            [
                {
                    "text": "Proteinin endoplazmik retikulumda hatalı katlanarak proteazomlarda yıkılmasıdır; kaperon benzeri modülatörler katlanmayı düzelterek proteinin hücre zarına ulaşmasını sağlar",
                    "isCorrect": True,
                    "explanation": "Mükemmel Moleküler Patoloji: Delta-F508 Sınıf II işlenme defektidir; düzelticiler (correctors) proteini zara ulaştırır."
                },
                {
                    "text": "Proteinin hücre zarında kanal kapağının açılamamasıdır; ilaçlar por çapını genişletir",
                    "isCorrect": False,
                    "explanation": "Hatalı; bu Sınıf III (G551D) mutasyonudur ve İvakaftor ile potansiyelize edilir."
                }
            ]
        ),
        24: make_branching_logic(
            "Kronik öksürük ve tekrarlayan pnömoni atakları olan 2 yaşında bir çocuğa pilokarpin iyontoforezi ile ter testi uygulanıyor. Ter klorür konsantrasyonu 82 mEq/L bulunuyor.",
            "Bu laboratuvar sonucunun kesin patolojik anlamı nedir?",
            [
                {
                    "text": "Sonuç >60 mEq/L eşiğini aştığı için Kistik Fibrozis tanısı kesinleşmiştir",
                    "isCorrect": True,
                    "explanation": "Doğrudur; ter klorürünün 60 mEq/L üzerinde olması kistik fibrozis için altın standart tanı kriteridir."
                },
                {
                    "text": "Sonuç normaldir; çocuğun aşırı tuzlu beslendiğini gösterir",
                    "isCorrect": False,
                    "explanation": "Hatalı; normal ter klorürü <30 mEq/L'dir, 82 mEq/L patolojiktir."
                }
            ]
        ),
        26: make_branching_logic(
            "Yenidoğan yoğun bakım servisinde kistik fibrozis tanılı bir bebeğin doğumdan sonraki 36. saatte safralı kusması ve mekonyum çıkaramaması üzerine çekilen batın grafisinde mikrokolon ve ileusta sabun köpüğü görünümü izleniyor.",
            "Bu klinik tablonun adı ve cerrahi/tıbbi yaklaşım prensibi nedir?",
            [
                {
                    "text": "Mekonyum İleusudur; yapışkan mekonyum tıkacını çözmek için gastrografin lavmanı veya cerrahi lavaj uygulanmalıdır",
                    "isCorrect": True,
                    "explanation": "Doğrudur; mekonyum ileusu KF'li yenidoğanların %15-20'sinde ilk belirtidir ve dehidrate mukustan kaynaklanır."
                },
                {
                    "text": "Hirschsprung hastalığıdır; aganglionik segment rezeke edilmelidir",
                    "isCorrect": False,
                    "explanation": "Hatalı; Hirschsprung rektosigmoid aganglionozistir, kistik fibrozis ile doğrudan ilişkili değildir."
                }
            ]
        ),
        28: make_branching_logic(
            "38 yaşında gebe bir kadının prenatal taramasında fetüste Trizomi 21 (Down sendromu) şüphesi beliriyor. Doğum sonrası yapılan genetik analizde karyotip 46,XY,t(14;21) saptanıyor.",
            "Bu Robertson translokasyonlu Down sendromu olgusunun maternal mayoz ayrılamamasına göre en kritik klinik farkı nedir?",
            [
                {
                    "text": "Anne yaşından bağımsızdır ve ebeveynlerden birinde dengeli taşıyıcılık varsa sonraki gebeliklerde tekrarlama riski çok yüksektir",
                    "isCorrect": True,
                    "explanation": "Kusursuz Genetik Bilgi: Translokasyon Down sendromları ailesel kalıtılabilir ve ebeveyn taşıyıcılığı araştırılmalıdır."
                },
                {
                    "text": "Translokasyonlu Down sendromunda zeka geriliği hiç görülmez",
                    "isCorrect": False,
                    "explanation": "Hatalı; fenotipik bulgular ve zeka geriliği klasik trizomi 21 ile tamamen aynıdır."
                }
            ]
        ),
        32: make_branching_logic(
            "Bir halk sağlığı epidemiyoloğu, büyük bir kentin sanayi bölgesine yakın yoksul mahallelerinde astım ve kardiyovasküler hastalık prevalansının lüks banliyölere göre 4 kat yüksek olduğunu tespit ediyor.",
            "Bu sağlık eşitsizliğinin altında yatan temel patogenetik gerçeklik nedir?",
            [
                {
                    "text": "Sosyal belirleyiciler; dezavantajlı grupların endüstriyel PM2.5 ve ozon kirliliğine, kalitesiz konutlara ve kurşunlu altyapıya orantısız şekilde daha fazla maruz kalması",
                    "isCorrect": True,
                    "explanation": "Doğrudur; modern tıpta hastalık farklılıklarının ana belirleyicisi genetik ırk değil, çevresel maruziyet adaletsizliğidir."
                },
                {
                    "text": "Yoksul popülasyonun genetik olarak savunma mekanizmalarından tamamen yoksun doğması",
                    "isCorrect": False,
                    "explanation": "Hatalı ve bilim dışı; genomik çeşitlilik popülasyonlar arasında değil, bireyler arasındadır."
                }
            ]
        ),
        34: make_branching_logic(
            "Yaz aylarında sıcak hava dalgası sırasında acil servise baş dönmesi, kuru sıcak cilt, konfüzyon ve rektal ateşi 41.2°C ölçülen 75 yaşında KOAH ve kalp yetmezliği tanılı bir hasta getiriliyor.",
            "Bu hastadaki ölümcül patoloji ve acil fizyopatolojik yönetim ne olmalıdır?",
            [
                {
                    "text": "Sıcak Çarpması (Heat Stroke); termoregülatuvar merkez çökmüştür; hastaya derhal evaporatif soğutma ve buzlu sıvı uygulanmalıdır",
                    "isCorrect": True,
                    "explanation": "Doğrudur; sıcak hava dalgaları yaşlı ve kardiyak rezervi kısıtlı bireylerde fatal termoregülasyon çöküşüne yol açar."
                },
                {
                    "text": "Akut bakteriyel sepsis; derhal antipiretik aspirin verilip beklenmelidir",
                    "isCorrect": False,
                    "explanation": "Hatalı; sıcak çarpmasında aspirin kontrendikedir ve vücut sıcaklığı acil fiziksel soğutma ile düşürülmelidir."
                }
            ]
        ),
        36: make_branching_logic(
            "Güneşli ve rüzgarsız bir yaz gününde şehir merkezinde koşan bir maratoncuda koşunun 45. dakikasında şiddetli göğüs yanması, kuru öksürük ve hırıltı başlıyor.",
            "Havadaki fotokimyasal dumanın hangi temel oksidan bileşeni solunum epitelinde lipid peroksidasyonuna yol açmıştır?",
            [
                {
                    "text": "Troposferik Ozon (O3)",
                    "isCorrect": True,
                    "explanation": "Doğrudur; güneşli günlerde otomobil egzozlarının fotokimyasal reaksiyonu ile yer seviyesinde ozon tepe yapar ve güçlü serbest radikal hasarı oluşturur."
                },
                {
                    "text": "Karbonmonoksit (CO)",
                    "isCorrect": False,
                    "explanation": "Hatalı; CO serbest radikal ve mukozal yanma yapmaz, oksihemoglobini bağlar."
                }
            ]
        ),
        38: make_branching_logic(
            "Kırsal bölgede kış aylarında bacasız kömür sobası yanan kapalı bir odada uyuyan aile sabah baş ağrısı, bulantı ve baygınlık ile uyanıyor. Hastaların dudak ve tırnak dipleri vişne kırmızısı (kiraz kırmızısı) renktedir.",
            "Bu tablonun patolojik tanısı ve acil hayat kurtarıcı tedavisi nedir?",
            [
                {
                    "text": "Akut Karbonmonoksit (CO) Zehirlenmesi; derhal %100 normobarik veya hiperbarik oksijen tedavisi uygulanmalıdır",
                    "isCorrect": True,
                    "explanation": "Mükemmel Klinik Bilgi: CO hemoglobine 200 kat sıkı bağlanarak karboksihemoglobin yapar; kiraz kırmızısı renk oluşturur; yüksek basınçlı oksijen CO'yu kovar."
                },
                {
                    "text": "Methemoglobinemi; metilen mavisi verilmelidir",
                    "isCorrect": False,
                    "explanation": "Hatalı; methemoglobinemide çikolata kahverengi kan ve siyanoz olur, kiraz kırmızısı CO'ya özgüdür."
                }
            ]
        ),
        42: make_branching_logic(
            "Eski bir sanayi kasabasında yaşayan 4 yaşında bir çocuğun rutin taramasında kan kurşun seviyesi 22 µg/dL ölçülüyor.",
            "Hekimin bu çocuk için atması gereken İLK ve EN ÖNEMLİ basamak hangisidir?",
            [
                {
                    "text": "Çocuğun evindeki eski boyalar ve içme suyu tesisatının incelenerek maruziyet kaynağından derhal uzaklaştırılması",
                    "isCorrect": True,
                    "explanation": "Doğrudur; ağır metal toksikolojisinde ilk kural maruziyet kaynağının kesilmesidir; aksi takdirde şelasyon tedavisi dahi etkisiz kalır."
                },
                {
                    "text": "Hiçbir müdahale yapılmadan 1 yıl sonra kontrol kan tahlili istenmesi",
                    "isCorrect": False,
                    "explanation": "Hatalı ve ihmal; >3.5 µg/dL üzeri değerler çocukta bilişsel gerilik riski taşır, 22 µg/dL acil araştırma gerektirir."
                }
            ]
        ),
        44: make_branching_logic(
            "Akü geri dönüşüm tesisinde çalışan 40 yaşındaki bir işçide halsizlik, karın koliği ve el parmaklarında uyuşma saptanıyor. Tam kan sayımında Hb: 9.2 g/dL, MCV: 72 fL bulunuyor. Ferritin düzeyi normaldir.",
            "Bu mikrositer hipokromik aneminin etyolojisini kanıtlamak için periferik yaymada hangi morfolojik bulgu aranmalıdır?",
            [
                {
                    "text": "Eritrosit sitoplazmasında bazofilik beneklenme (ribozomal RNA agregatları)",
                    "isCorrect": True,
                    "explanation": "Doğrudur; pirimidin-5'-nükleotidaz inhibisyonuna bağlı bazofilik beneklenme kurşun anemisinin patognomonik periferik yayma izidir."
                },
                {
                    "text": "Eritrositlerde oraklaşma ve Howell-Jolly cisimcikleri",
                    "isCorrect": False,
                    "explanation": "Hatalı; bu orak hücreli anemidir."
                }
            ]
        ),
        46: make_branching_logic(
            "Japonya'da Minamata Körfezi kıyısında yaşayan ve gebeliği boyunca düzenli kirlenmiş ton balığı tüketen bir annenin bebeğinde mikrosefali ve ağır serebral palsi saptanıyor.",
            "Metilcıvanın fetal beyinde yaptığı bu yıkımın temel biyolojik nedeni nedir?",
            [
                {
                    "text": "Metilcıvanın lipofilik yapısıyla plasentayı ve fetal kan-beyin bariyerini aşarak nöronal bölünme ve göçü durdurması",
                    "isCorrect": True,
                    "explanation": "Doğrudur; metilcıva fetal nöronal hücre iskeletini ve mikrotübülleri tahrip ederek ağır konjenital nöropatoloji yapar."
                },
                {
                    "text": "Bebeğin kulak zarının yüksek ses dalgalarıyla patlaması",
                    "isCorrect": False,
                    "explanation": "Hatalı; Minamata hastalığı kimyasal ağır metal nörotoksisitesidir."
                }
            ]
        ),
        48: make_branching_logic(
            "Maden atıklarıyla kirlenmiş pirinç tarlalarından beslenen menopoz sonrası bir kadında şiddetli kemik ağrıları, proksimal tübüler proteinüri ve radyografide yaygın psödokırıklar (Looser zonları) saptanıyor.",
            "Bu İtai-İtai hastalığı tablosunda kemik yıkımına yol açan toksik ağır metal hangisidir?",
            [
                {
                    "text": "Kadmiyum (Cd)",
                    "isCorrect": True,
                    "explanation": "Doğrudur; kadmiyum renal tübüler kalsiyum emilimini bozar, D vitamini aktivasyonunu durdurur ve ağır osteomalaziye (İtai-İtai) yol açar."
                },
                {
                    "text": "Demir (Fe)",
                    "isCorrect": False,
                    "explanation": "Hatalı; demir fazlalığı hemokromatoz yapar, kemik erimesi yapmaz."
                }
            ]
        ),
        52: make_branching_logic(
            "Günde 2 paket sigara içen 55 yaşındaki bir hastada sigara dumanındaki polisiklik aromatik hidrokarbonların (PAH) bronş epitelinde yaptığı mutasyon araştırılıyor.",
            "Bu karsinojenik bileşiklerin insan akciğer kanserlerinde en sık mutasyona uğrattığı tümör baskılayıcı gen hangisidir?",
            [
                {
                    "text": "TP53 tümör baskılayıcı geni",
                    "isCorrect": True,
                    "explanation": "Doğrudur; benzo[a]piren epoksitleri TP53 geninin DNA bağlama alanındaki spesifik kodonlara kovalent yapışarak p53'ü inaktive eder."
                },
                {
                    "text": "İnsülin geni",
                    "isCorrect": False,
                    "explanation": "Hatalı; insülin metabolik hormondur, tümör baskılayıcı değildir."
                }
            ]
        ),
        54: make_branching_logic(
            "40 paket-yıl sigara öyküsü olan 60 yaşında erkek hasta öksürük ve hemoptizi ile başvuruyor. Bronkoskopide sağ ana bronşu tıkayan vejetan kitle saptanıyor. Biyopside keratin incileri ve intersellüler köprüler izleniyor.",
            "Bu tümörün patolojik tanısı nedir ve sigara ile ilişkisi nasıldır?",
            [
                {
                    "text": "Skuamöz Hücreli Akciğer Karsinomu; sigara kullanımı ile en güçlü nedensel ilişkiye sahip majör karsinom tiplerinden biridir",
                    "isCorrect": True,
                    "explanation": "Doğrudur; keratin incileri ve intersellüler köprüler skuamöz karsinomun patognomonik histolojisidir ve sigarayla doğrudan ilişkilidir."
                },
                {
                    "text": "Akciğer Adenokarsinomu; sigara ile ilişkisi en zayıf olan periferik tiptir",
                    "isCorrect": False,
                    "explanation": "Hatalı; adenokarsinom glandüler tübüller ve musin üretir, keratin incisi yapmaz."
                }
            ]
        ),
        56: make_branching_logic(
            "Gebelikte sigara içmeye devam eden bir annenin 38. haftada doğan bebeğinde doğum ağırlığı 1950 gram (beklenenin çok altında) ölçülüyor.",
            "Tütün dumanının fetal intrauterin gelişme geriliği (İUGR) yapmasındaki iki ana mekanizma nedir?",
            [
                {
                    "text": "Nikotinin plasental damarları büzerek kan akımını kesmesi ve karbonmonoksitin fetal dokularda hipoksi yapması",
                    "isCorrect": True,
                    "explanation": "Doğrudur; nikotin vazokonstriktördür, CO ise fetal oksihemoglobin eğrisini bozarak bebeği kronik hipokside bırakır."
                },
                {
                    "text": "Dumandaki katranın amniyon sıvısını doğrudan pıhtılaştırması",
                    "isCorrect": False,
                    "explanation": "Hatalı; duman amniyon sıvısına katran dökmez, hasar vasküler ve hipoksiktir."
                }
            ]
        ),
        58: make_branching_logic(
            "Hafta sonu yoğun alkol tüketen bir bireyde pazartesi günü karaciğer biyopsisinde sentrilobüler hepatositlerde sitoplazmayı dolduran ve nükleusu kenara iten geniş berrak yağ vakuolleri izleniyor.",
            "Bu akut alkolik steatoz tablosunun prognozu ve geri dönüşümlülüğü nasıldır?",
            [
                {
                    "text": "Alkol tüketimi kesildiğinde günler-haftalar içinde tamamen geri dönebilen (reversibl) iyi huylu bir tablodur",
                    "isCorrect": True,
                    "explanation": "Doğrudur; basit alkolik steatoz fibrozis içermez ve alkol bırakıldığında NAD+ dengesi düzelerek tamamen iyileşir."
                },
                {
                    "text": "Geri dönüşümsüz siroz evresidir ve acil karaciğer nakli gerektirir",
                    "isCorrect": False,
                    "explanation": "Hatalı; basit steatoz siroz değildir, siroz geri dönüşümsüz nodüler sklerozdur."
                }
            ]
        ),
        62: make_branching_logic(
            "Kıtlık bölgesinde yaşayan 2 yaşında bir çocuğun muayenesinde boy ve kilo -3 SD altında bulunuyor. Çocuk bir deri bir kemik kalmış, tüm kasları erimiş, yanak yağları yok olmuş ancak vücudunda hiçbir ödem saptanmamıştır.",
            "Bu çocuğun tedavisinde dikkat edilmesi gereken en hayati metabolik tehlike hangisidir?",
            [
                {
                    "text": "Yeniden Besleme Sendromu (Refeeding Sendromu); aniden yüksek karbonhidrat verildiğinde insülin patlamasıyla hücre içine fosfat ve potasyum kaçışı ve kardiyak arrest riski",
                    "isCorrect": True,
                    "explanation": "Mükemmel Pediatrik ve Metabolik Bilgi: Uzun süreli açlıkta ani glukoz verilmesi hipofosfatemi ve fatal aritmi yapar; besleme kademeli olmalıdır."
                },
                {
                    "text": "Çocuğa derhal sınırsız yağlı yemek verilmesi gerekliliği",
                    "isCorrect": False,
                    "explanation": "Hatalı ve ölümcül; kontrolsüz besleme refeeding sendromunu tetikler."
                }
            ]
        ),
        64: make_branching_logic(
            "Sütten kesildikten sonra sadece mısır ve nişasta ile beslenen 15 aylık bir çocukta bacaklarda masif gode bırakan ödem, batında asit ve karaciğerde büyüme saptanıyor. Laboratuvarda serum albümini 1.8 g/dL bulunuyor.",
            "Bu Kwashiorkor tablosunda karaciğerde yağlanma görülmesinin nedeni nedir?",
            [
                {
                    "text": "Diyetle protein alınamadığı için karaciğerin trigliseridleri dışarı salacak apolipoproteinleri sentezleyememesi",
                    "isCorrect": True,
                    "explanation": "Doğrudur; apolipoprotein yokluğunda VLDL üretilemez ve yağ karaciğer hücrelerinde hapsolur."
                },
                {
                    "text": "Çocuğun aşırı miktarda tereyağı tüketmesi",
                    "isCorrect": False,
                    "explanation": "Hatalı; çocuk yağ değil nişasta tüketmektedir; sorun lipid çıkışının protein yokluğuyla kilitlenmesidir."
                }
            ]
        ),
        72: make_branching_logic(
            "20 yaşında bir üniversite öğrencisi genç kız aşırı kilo alma korkusuyla günde 300 kaloriden az besleniyor. Boy: 168 cm, Kilo: 38 kg (VKİ: 13.5 kg/m²). Son 8 aydır hiç adet görmediğini belirtiyor. Nabız 48/dk, tansiyon 80/50 mmHg.",
            "Bu anoreksiya nervoza tablosunda amenorenin altta yatan nöroendokrin mekanizması nedir?",
            [
                {
                    "text": "Adipoz doku ve leptin tükenmesine bağlı olarak hipotalamustan GnRH salınımının baskılanması ve hipofizden LH/FSH salgısının durması",
                    "isCorrect": True,
                    "explanation": "Doğrudur; kritik yağ kütlesinin altına inildiğinde hipotalamik GnRH pulsatilitesi çöker ve sekonder amenore gelişir."
                },
                {
                    "text": "Overlerde polikistik kistlerin aşırı androjen üretmesi",
                    "isCorrect": False,
                    "explanation": "Hatalı; bu PKOS'tur ve obeziteyle ilişkilidir, anoreksiyadaki hipoöstrojenik hipotalamik amenoredir."
                }
            ]
        ),
        74: make_branching_logic(
            "45 yaşında erkek hastada boy: 175 cm, kilo: 110 kg (VKİ: 35.9 kg/m²), bel çevresi: 114 cm ölçülüyor. Açlık kan şekeri 138 mg/dL, trigliserid 280 mg/dL, HDL 32 mg/dL.",
            "Bu hastadaki viseral yağlanmanın metabolik sendrom ve diyabeti tetiklemesindeki temel mekanizma nedir?",
            [
                {
                    "text": "Viseral yağ dokusunun portal sisteme serbest yağ asitleri (FFA) ve TNF-alfa boşaltarak karaciğer ve kasta insülin reseptör sinyalini kilitlemesi",
                    "isCorrect": True,
                    "explanation": "Doğrudur; viseral adipoz doku yüksek lipolitik aktiviteyle doğrudan portal vene FFA pompalar ve sistemik insülin direncini başlatır."
                },
                {
                    "text": "Viseral yağın böbrekleri ezerek eritropoietin salgısını durdurması",
                    "isCorrect": False,
                    "explanation": "Hatalı; metabolik sendrom EPO eksikliği değil, insülin direnci tablosudur."
                }
            ]
        ),
        84: make_branching_logic(
            "Tütsülenmiş et ve salamura balık tüketiminin çok yüksek olduğu bir coğrafyada gastrik adenokarsinom insidansının dünya ortalamasının 5 katı olduğu görülüyor.",
            "Mide mukozasında intestinal metaplazi ve displazi üzerinden kanser gelişimini tetikleyen temel gıda kimyasalı hangisidir?",
            [
                {
                    "text": "Nitrit ve sekonder aminlerden mide asidinde oluşan Nitrozaminler ve Nitrozamidler",
                    "isCorrect": True,
                    "explanation": "Doğrudur; nitrozaminler mide epiteli DNA'sını alkilleyerek atrofik gastrit zemininde intestinal tip gastrik karsinomu tetikler."
                },
                {
                    "text": "C vitamini ve turunçgil asitleri",
                    "isCorrect": False,
                    "explanation": "Hatalı; C vitamini nitrozasyonu engelleyen koruyucu antioksidandır."
                }
            ]
        )
    }

def get_extra_causal_chains():
    """Causal chain (mekanizma zinciri) ögeleri (9 adet)."""
    return {
        3: make_causal_chain(
            "Epigenetik Modifikasyonlarla Kromatin Yoğunlaşması Zinciri",
            [
                "1. Sinyal Algılama: Hücre dışı veya gelişimsel sinyallerle histon modifiye edici enzimlerin uyarılması",
                "2. Histon Deasetilasyonu: HDAC enzimlerinin lizin artıklarındaki asetil gruplarını koparması",
                "3. Elektrostatik Çekim: Pozitif yüklü histonların negatif yüklü DNA fosfat iskeletine sıkıca yapışması",
                "4. Nükleozom Sıkışması: Kromatin liflerinin 30 nm'lik heterokromatin lifleri halinde kilitlenmesi",
                "5. Transkripsiyonel Susturulma: RNA polimeraz II erişiminin engellenmesi ve genin sessizleşmesi"
            ]
        ),
        7: make_causal_chain(
            "Kopya Sayısı Varyasyonundan (CNV) Nörogelişimsel Hastalığa",
            [
                "1. Mayotik Rekombinasyon Hatası: Düşük kopyalı tekrarlar arasında eşit olmayan krosing-over gerçekleşmesi",
                "2. Segmenter Dengesizlik: Kromozom bölgesinde binlerce bazlık segmentin silinmesi (delesyon) veya kopyalanması",
                "3. Gen Dozaj Değişimi: Bölgedeki nörogelişimsel genlerin ifade düzeyinin yüzde elli düşmesi veya artması",
                "4. Sinaptik Matürasyon Kusuru: Serebral kortekste nöronal devrelerin ve bağlantıların bozulması",
                "5. Klinik Fenotip: Otizm spektrum bozukluğu veya açıklanamayan mental motor gelişim geriliği"
            ]
        ),
        13: make_causal_chain(
            "Otozomal Resesif Enzim Defektinde Hücresel Hasar Zinciri",
            [
                "1. Çift Alel Mutasyonu: Anne ve babadan gelen her iki kopyada da inaktive edici mutasyon bulunması",
                "2. Katalitik Enzim Yokluğu: Kritik metabolik yolaktaki enzimin sıfıra inmesi",
                "3. Toksik Substrat Birikimi: Parçalanamayan öncül molekülün lizozomlarda veya kanda toksik birikmesi",
                "4. Ürün Eksikliği: Enzimin ürettiği nihai esansiyel ürünün sentezlenememesi",
                "5. Doku Harabiyeti: Hücresel fonksiyonların çökmesi ve erken çocuklukta organ yetmezliği"
            ]
        ),
        17: make_causal_chain(
            "Marfan Sendromunda İskelet Deformitesi Oluşum Zinciri",
            [
                "1. FBN1 Defekti: 15q21 gen mutasyonu sonucu mikrofibrillerin hatalı polimerizasyonu",
                "2. Kıkırdak Elastisite Kaybı: Epifiz büyüme plaklarındaki bağ dokusunun gevşemesi ve gerilme direncinin düşmesi",
                "3. TGF-beta Uyarısı: Serbest kalan büyüme faktörünün periost ve kıkırdak proliferasyonunu kontrolsüz tetiklemesi",
                "4. Uzun Kemik Aşırı Büyümesi: Falankslar ve kostal kıkırdakların orantısız şekilde uzaması",
                "5. Fenotipik Bulgular: Araknodaktili, pektus ekskavatum ve kifoskolyoz deformiteleri"
            ]
        ),
        23: make_causal_chain(
            "Kistik Fibroziste Pseudomonas Biyofilm Kolonizasyonu Zinciri",
            [
                "1. Dehidrate Mukus: Klor atılamaması ve sodyum emilimiyle solunum epitel yüzeyinin kuruması",
                "2. Siliyer Klirens Felci: Mukosiliyer asansörün tıkaçlar altında kalarak mikropları temizleyememesi",
                "3. Bakteriyel Tutunma: Çevresel Pseudomonas aeruginosa bakterilerinin yapışkan mukusa kolonize olması",
                "4. Aljinat Üretimi: Bakterinin fenotip değiştirerek mukoid kapsül ve biyofilm zırhı örmesi",
                "5. Kronik Doku Harabiyeti: Nötrofil enzimleriyle bronş kıkırdağının erimesi ve yaygın bronşiektazi"
            ]
        ),
        33: make_causal_chain(
            "Küresel Isınmadan Su Kaynaklı Salgınlara Giden Yolak",
            [
                "1. Sera Gazı Birikimi: Atmosferde CO2 artışıyla okyanus ve kara yüzey sıcaklıklarının yükselmesi",
                "2. Aşırı Yağış ve Taşkın: Isınan havanın daha fazla su buharı tutarak şiddetli fırtına ve sellere yol açması",
                "3. Kanalizasyon Taşması: Sel sularının kentsel kanalizasyonu patlatarak temiz içme suyu şebekesine karışması",
                "4. Patojen Çoğalması: Ilık sularda Vibrio cholerae ve Cryptosporidium kistlerinin patlayıcı çoğalması",
                "5. Kitlesel İshal Salgını: Kontamine su tüketimiyle kolera ve gastroenterit epidemileri"
            ]
        ),
        43: make_causal_chain(
            "Kurşunun Kemik İliği ve Hem Sentezini Çökertme Basamakları",
            [
                "1. Kurşun Emilimi: Sindirim veya solunum yoluyla kana karışan kurşunun eritroblastlara girmesi",
                "2. -SH Enzim Blokajı: ALA dehidrataz ve ferrokelataz enzimlerinin kovalent olarak kilitlenmesi",
                "3. Protoporfirin Yığılması: Demirin porfirin halkasına takılamayıp serbest eritrosit protoporfirini yapması",
                "4. Hemoglobin Sentez Çöküşü: Yetersiz hemoglobin üretimiyle mikrositer hipokromik anemi gelişmesi",
                "5. RNA Parçalanamaması: Pirimidin-5'-nükleotidaz inhibisyonuyla bazofilik beneklenmenin belirmesi"
            ]
        ),
        53: make_causal_chain(
            "Tütün Dumanından Koroner Arter Tıkanıklığına Giden Yolak",
            [
                "1. Toksin Girişi: Sigara dumanındaki serbest radikaller ve nikotinin alveollerden kana sızması",
                "2. Endotel Disfonksiyonu: Arter duvarında nitrik oksit sentezinin durması ve damarın büzüşmesi",
                "3. Köpük Hücre Teşekkülü: Okside LDL'nin makrofajlarca yutularak aterosklerotik plak yapması",
                "4. Trombosit Agregasyonu: Tromboksan artışıyla pıhtılaşma hücrelerinin plak üzerine yapışması",
                "5. Akut Koroner Oklüzyon: Plak yırtılmasıyla saniyeler içinde lümenin pıhtıyla tıkanıp miyokard enfarktüsü yapması"
            ]
        ),
        63: make_causal_chain(
            "Kwashiorkorda Hipoalbüminemik Asit ve Ödem Basamakları",
            [
                "1. Proteinden Yoksun Diyet: Çocuğun sadece nişasta/karbonhidrat ile beslenmesi, aminoasit girişinin durması",
                "2. Karaciğer Sentez Çöküşü: Hepatositlerin albümin üretimini sürdürememesi ve kanda albüminin dip yapması",
                "3. Plazma Onkotik Düşüşü: Kılcal damar içinde sıvıyı tutan osmotik kuvvetin tamamen sıfırlanması",
                "4. İnterstisyel Sıvı Kaçışı: Suyun damar dışına sızarak doku aralıklarında ve periton boşluğunda birikmesi",
                "5. Anazarka Ödem ve Asit: Bacaklarda gode bırakan şişlik ve ileri derecede çıkık şiş karın tablosu"
            ]
        )
    }

def get_extra_cloze():
    """Cloze masking (boşluk doldurma) ögeleri (8 adet)."""
    return {
        5: make_cloze(
            "İnsan genomunda protein kodlayan genlerin ekzonik dizileri tüm nükleotid diziliminin yalnızca yüzde bir buçuğunu oluşturur.",
            "yüzde bir buçuğunu",
            "Yaklaşık yirmi bin genin nükleotid kütlesi içindeki minimal payı"
        ),
        15: make_cloze(
            "Marfan sendromunda mikrofibrillerin yapıtaşı olan ve elastik liflere iskelet sağlayan glikoproteine fibrillin-1 adı verilir.",
            "fibrillin-1",
            "On beşinci kromozomdaki FBN1 geni tarafından kodlanan büyük bağ dokusu proteini"
        ),
        25: make_cloze(
            "Kistik fibrozis hastalarında lümenden klor emiliminin bozulması ter bezlerinde yüksek klorürlü hipertonik ter oluşmasına yol açar.",
            "hipertonik ter",
            "Deri yüzeyinde litrede altmış milieşdeğerin üzerinde klor içeren aşırı tuzlu salgı"
        ),
        35: make_cloze(
            "Hava kirliliğinde çapı on mikrometreden küçük partiküller üst ve alt solunum yollarına penetre olarak kronik bronşite yol açar.",
            "on mikrometreden küçük",
            "Solunabilir kaba partikül madde fraksiyonunun aerodinamik sınır boyutu"
        ),
        45: make_cloze(
            "Kurşun zehirlenmesinde eritrositlerde ribozomal RNA parçalanamaması sonucu periferik yaymada bazofilik beneklenme izlenir.",
            "bazofilik beneklenme",
            "Kırmızı kan hücresi sitoplazmasında mavi noktasal granüller oluşturan inklüzyon"
        ),
        55: make_cloze(
            "Sigara dumanındaki oksidan maddeler alfa-1 antitripsini inaktive ederek kontrolsüz elastaz aktivitesiyle sentriasiner amfizeme yol açar.",
            "sentriasiner amfizem",
            "Asinusun merkezindeki solunum bronşiyollerinin yıkımıyla karakterize tütün amfizemi tipi"
        ),
        65: make_cloze(
            "Beslenme yetersizliğinde diyetle hem kalori hem proteinin eşit derecede yokluğuna bağlı somatik kas erimesi tablosuna marasmus denir.",
            "marasmus",
            "Ödem görülmeyen ve yaşlı adam yüzü manzarası veren saf kalori açlığı sendromu"
        ),
        75: make_cloze(
            "Obezitede viseral yağ kütlesi arttıkça plazma konsantrasyonu paradoksal olarak azalan koruyucu hormona adiponektin adı verilir.",
            "adiponektin",
            "AMPK enzimini aktive ederek insülin duyarlılığı ve yağ oksidasyonu sağlayan koruyucu peptit"
        )
    }

def get_extra_sliders():
    """Before/After slider (karşılaştırmalı durum) ögeleri (5 adet)."""
    return {
        72: make_before_after(
            "Yeme Bozukluklarında Vücut Ağırlığı ve Beden Algısı",
            "Anoreksiya Nervoza (Kısıtlayıcı Tip)",
            "Aşırı düşük vücut ağırlığı (<17.5 VKİ), kaşeksi, şiddetli hipotalamik amenore ve kendini şişman görme hezeyanı",
            "Bulimia Nervoza (Arındırıcı Tip)",
            "Genellikle normal veya hafif kilolu beden yapısı; gizli aşırı yeme nöbetleri peşinden kusma ve laksatif kullanımı"
        ),
        74: make_before_after(
            "İki Farklı Yağ Dağılım Modelinin Metabolik Riski",
            "Gluteofemoral Subkütan Yağlanma (Armut Tipi)",
            "Deri altında toplanır; serbest yağ asitlerini sistemik venlere yavaş verir; diyabet ve enfarktüs riski düşüktür",
            "Abdominal Viseral Yağlanma (Elma Tipi)",
            "Omentum ve mezenterde toplanır; portal vene masif serbest yağ asidi boşaltır; insülin direnci ve metabolik sendromu tetikler"
        ),
        82: make_before_after(
            "Diyet Lifinin Bağırsak Mikrobiyotasındaki Dönüşümü",
            "Liften Yoksun Rafine Şeker Diyeti",
            "Yavaş bağırsak geçişi, karsinojenlerin kolon mukozasıyla uzun teması ve artmış kolorektal polip ve kanser riski",
            "Yüksek Lifli ve Posalı Diyet",
            "Hızlı fekal atılım, seyreltilmiş safra asitleri ve bakteriyel bütirat senteziyle kolonositlerin kanserden korunması"
        ),
        84: make_before_after(
            "A Vitamini Eksikliğinde Göz Epiteli Metaplazisi",
            "Sağlıklı Oküler Yüzey",
            "Mukus salgılayan goblet hücreleri ve nemli şeffaf kornea epiteli ile pürüzsüz görme yüzeyi",
            "A Vitamini Eksikliği (Kseroftalmi)",
            "Goblet kaybı, keratinize kuru skuamöz metaplazi, Bitot lekeleri ve korneanın eriyerek delinmesi (keratomalazi)"
        ),
        92: make_before_after(
            "Prematüre vs Term Bebek Akciğer Biyofiziği",
            "Matür Term Akciğeri (Yeterli Sürfaktan)",
            "Alveol yüzey gerilimi düşüktür; ekspiryum sonunda alveoller açık kalır ve gaz değişimi kesintisiz sürer",
            "Prematüre Akciğeri (RDS / Sürfaktan Yok)",
            "Yüksek yüzey gerilimiyle alveoller her nefes verişte kollabe olur; hiyalin membranlar oluşur ve solunum felç olur"
        )
    }

def get_extra_quizzes():
    """Micro quiz (küçük test sorusu) ögeleri (5 adet)."""
    return {
        73: make_micro_quiz(
            "Bulimia nervoza tanılı bir hastada diş hekimi muayenesinde ön kesici dişlerin arka (lingual) yüzeylerinde diş minesinin kimyasal olarak eridiği saptanmıştır. Bu lezyonun patolojik adı ve nedeni nedir?",
            {
                "A": "Perimolizis; tekrarlayan kusmalarda mide hidroklorik asidinin diş minesini eritmesi",
                "B": "Diş çürüğü; aşırı çikolata tüketimi",
                "C": "Florozis; sudaki aşırı flor birikimi",
                "D": "Amelogenezis imperfekta; genetik diş minesi defekti",
                "E": "Skorbüt; C vitamini eksikliği"
            },
            "A",
            {
                "A": "Doğrudur; mide asidinin geriye çıkması ön dişlerin lingual yüzeyindeki kalsiyumu eriterek perimolizis yapar.",
                "B": "Yanlış; çürük bakteriyeldir.",
                "C": "Yanlış; florozis beyaz lekeler yapar.",
                "D": "Yanlış; bu kalıtsal hastalıktır.",
                "E": "Yanlış; skorbütte diş eti kanar."
            }
        ),
        77: make_micro_quiz(
            "Aşağıdakilerden hangisi yağ dokusundan salgılanan ve obez bireylerde diğer adipokinlerin aksine kan konsantrasyonu paradoksal olarak DÜŞEN koruyucu hormondur?",
            {
                "A": "Adiponektin",
                "B": "Leptin",
                "C": "Rezistin",
                "D": "TNF-alfa",
                "E": "İnterlökin-6"
            },
            "A",
            {
                "A": "Doğrudur; adiponektin yağ kütlesi arttıkça düşen yegane koruyucu adipokindir ve eksikliği insülin direncine yol açar.",
                "B": "Yanlış; leptin obezitede aşırı yükselir.",
                "C": "Yanlış; rezistin obezitede artar.",
                "D": "Yanlış; TNF-alfa yağ dokusunda artar.",
                "E": "Yanlış; IL-6 yağ dokusunda artar."
            }
        ),
        83: make_micro_quiz(
            "Nemli ve sıcak depolanan yer fıstığı ve mısır gibi gıdalarda üreyen Aspergillus flavus kaynaklı Aflatoksin B1'in hepatoselüler karsinom gelişimine yol açarken TP53 geninde yaptığı karakteristik moleküler mutasyon hangisidir?",
            {
                "A": "Kodon 249'da G:C -> T:A transversiyon mutasyonu",
                "B": "Kodon 12'de K-RAS aktivasyonu",
                "C": "EGFR ekzon 19 delesyonu",
                "D": "HER2 gen amplifikasyonu",
                "E": "BRCA1 geninde delesyon"
            },
            "A",
            {
                "A": "Doğrudur; aflatoksin 2,3-epoksit p53 geninin 249. kodonundaki guanine bağlanarak spesifik G->T transversiyonu yapar.",
                "B": "Yanlış; K-RAS nitrozaminlerle ilişkilidir.",
                "C": "Yanlış; EGFR akciğer kanserindedir.",
                "D": "Yanlış; HER2 meme kanserindedir.",
                "E": "Yanlış; BRCA1 meme ve over kanserindedir."
            }
        ),
        87: make_micro_quiz(
            "Prematüre doğan bir bebekte Tip 2 pnömositlerin immatür olması sonucu sentezlenemeyen ve eksikliğinde yaygın mikroatelektaziler ile respiratuar distres sendromuna (RDS) yol açan yüzey aktif lipid maddesi hangisidir?",
            {
                "A": "Sürfaktan (Dipalmitoilfosfatidilkolin)",
                "B": "Miyelin bazik proteini",
                "C": "Glikojen granülleri",
                "D": "Tip IV kollajen",
                "E": "Fibronektin"
            },
            "A",
            {
                "A": "Doğrudur; Tip 2 pnömositlerin ürettiği sürfaktan alveol yüzey gerilimini düşürerek ekspiryumda açık kalmalarını sağlar.",
                "B": "Yanlış; sinir kılıfı lipididir.",
                "C": "Yanlış; karbonhidrat deposudur.",
                "D": "Yanlış; bazal membran proteinidir.",
                "E": "Yanlış; ekstraselüler matriks proteinidir."
            }
        ),
        93: make_micro_quiz(
            "Yeni Nesil Dizileme (NGS) teknolojisinin klinik onkolojide klasik Sanger dizilemesine kıyasla sağladığı en büyük devrimsel tanısal üstünlük nedir?",
            {
                "A": "Milyonlarca DNA reaksiyonunu eşzamanlı ve paralel okuyarak tek bir biyopside yüzlerce kanser genini aynı anda tarayabilmesi",
                "B": "Yalnızca canlı hücre kültürlerinde çalışabilmesi",
                "C": "DNA yerine sadece protein moleküllerini okuyabilmesi",
                "D": "Maliyetinin Sanger'e göre bin kat daha pahalı olması",
                "E": "Sadece tek bir geni tek seferde inceleyebilmesi"
            },
            "A",
            {
                "A": "Doğrudur; NGS masif paralel dizileme ile çok genli kanser panellerini hızla ve yüksek doğrulukla tarar.",
                "B": "Yanlış; parafin doku DNA'sından kültürsüz çalışır.",
                "C": "Yanlış; nükleik asit dizilemesidir.",
                "D": "Yanlış; nükleotid başına maliyeti çok daha düşüktür.",
                "E": "Yanlış; tek gen Sanger'in kısıtlılığıdır."
            }
        )
    }

def enrich_slides(slides):
    """Slaytlara ek interaktif elemanları yerleştirir ve dengeler."""
    extra_branching = get_extra_branching()
    extra_chains = get_extra_causal_chains()
    extra_cloze = get_extra_cloze()
    extra_sliders = get_extra_sliders()
    extra_quizzes = get_extra_quizzes()

    for slide in slides:
        s_num = slide.get("slideNumber", 0)
        elems = slide.get("interactiveElements", [])

        if s_num in extra_branching:
            elems.append(extra_branching[s_num])
        if s_num in extra_chains:
            elems.append(extra_chains[s_num])
        if s_num in extra_cloze:
            elems.append(extra_cloze[s_num])
        if s_num in extra_sliders:
            elems.append(extra_sliders[s_num])
        if s_num in extra_quizzes:
            elems.append(extra_quizzes[s_num])

        slide["interactiveElements"] = elems

    return slides
