# Sections 1 to 5 for Deck 49 (50 slides)
from meds.scripts.data_decks.builder_item import mi

def get_deck_49_sections_1_to_5():
    sections = []
    
    # Section 1: Servisit Etyolojisi, Vajinal Flora ve Temel Patojenler
    sec1_items = [
        mi(
            title="Servisit Kavramı: Tanım ve Klinik Giriş",
            subtitle="Serviksin yaygın inflamatuvar tablosu ve klinik yansıması",
            lead="Servisit, serviks dokusunun mikrobiyal etkenler, kimyasal irritanlar veya travmatik faktörler zemininde gelişen yaygın inflamatuvar tablosudur. Kadın alt genital sisteminde jinekolojik polikliniklere en sık başvuru gerektiren temel antiteler arasında yer alır.",
            bullets=[
                ("Mukozal Tutulum", "Servikal mukozada vasküler konjesyon, ödem ve epitel hasarı ile birlikte nötrofilik infiltrasyon gelişir."),
                ("Klinik Belirti", "Hastalarda sıklıkla pürülan veya mukopürülan nitelikte vajinal akıntı (lökore) ve zaman zaman temas kanaması ortaya çıkar."),
                ("Asendan Yayılım Riski", "Uygun şekilde tedavi edilmeyen enfeksiyonlar endometrium ve fallop tüplerine ilerleyerek pelvik inflamatuvar hastalık riski doğurabilir.")
            ],
            alert="Servisit tek başına izole seyredebileceği gibi, vajinit veya üst genital yol enfeksiyonlarıyla kombine olarak da karşımıza çıkabilir.",
            summaries=["Serviksin yaygın inflamatuvar tablosudur.", "Mukopürülan akıntı en sık klinik belirtidir.", "Üst genital yola yayılım potansiyeli taşır."],
            cloze=["Serviksin mikrobiyal veya irritan etkenlerle gelişen yangısal sürecine servisit adı verilir.", "servisit", "Servikal dokunun yaygın yangısal durumu"],
            table={
                "title": "Servisit Temel Patolojik Parametreleri",
                "headers": ["Parametre", "Gözlenen Durum", "Klinik Yansıması"],
                "rows": [
                    {"cells": [{"text": "İnflamasyon Yeri", "isMasked": False}, {"text": "Servikal mukoza ve stroma", "isMasked": True, "hint": "Serviksin anatomik doku katmanı"}, {"text": "Eritem ve ödem gelişir", "isMasked": False}]},
                    {"cells": [{"text": "Majör Belirti", "isMasked": False}, {"text": "Mukopürülan akıntı", "isMasked": True, "hint": "İrinli vajinal sekresyon"}, {"text": "Lökore tablosu", "isMasked": False}]}
                ]
            },
            chain={
                "title": "Servisit Gelişim Basamakları",
                "steps": [
                    "1. Mukozal Ajan Girişi: Enfeksiyöz patojen servikal kanala ve epitel yüzeyine yerleşir.",
                    "2. Vasküler Yanıt: Stromadaki kılcal damarlarda belirgin konjesyon ve nötrofil göçü başlar.",
                    "3. Sekresyon Artışı: Bezlerden ve hasarlı epitelden bol miktarda pürülan eksüda salgılanır.",
                    "4. Semptom Başlangıcı: Hasta vajinal akıntı ve disparoni yakınmasıyla başvurur."
                ]
            },
            recall={"q": "Servisit tablosunda hastayı doktora getiren en karakteristik jinekolojik yakınma nedir?", "a": "Lökore olarak adlandırılan irinli veya mukopürülan vajinal akıntıdır."},
            spot={
                "topic": "Servisitin Klinik ve Patolojik Temelleri",
                "items": [
                    {"text": "Servisit, serviksin jinekolojik pratikte en sık rastlanan inflamatuvar durumudur.", "isLie": False, "explanation": "Servikal inflamasyon kadın alt genital sisteminde en sık saptanan tablolardandır."},
                    {"text": "Servisitte en tipik fizik muayene ve laboratuvar bulgusu mukopürülan vajinal akıntıdır.", "isLie": False, "explanation": "Mukopürülan eksüda ve lökore servisit için klasik bulgudur."},
                    {"text": "Servisit daima malign bir süreçtir ve kendiliğinden kemik metastazı yapar.", "isLie": True, "explanation": "Tuzak! Servisit benign bir inflamasyondur, primer malign tümör değildir."},
                    {"text": "Tedavi edilmeyen olgularda mikroorganizmalar asendan yolla üst genital traktusa yayılabilir.", "isLie": False, "explanation": "Asendan yolla endometrit, salpenjit ve pelvik inflamatuvar hastalık riski mevcuttur."}
                ]
            },
            quiz={
                "q": "Servisit tablosunun genel patolojik ve klinik seyri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                "opts": [
                    {"key": "A", "text": "Serviksin çok sık görülen benign inflamatuvar bir tablosudur", "isCorrect": True, "explanation": "Servisit benign yangısal bir antitedir ve en sık mukopürülan akıntıyla belirti verir."},
                    {"key": "B", "text": "Yalnızca ileri evre invaziv skuamöz karsinom vakalarında ortaya çıkar", "isCorrect": False, "explanation": "Malignite şartı yoktur; çoğunlukla enfeksiyöz patojenlere bağlı selim süreçtir."},
                    {"key": "C", "text": "Hiçbir zaman vajinal akıntıya veya lökoreye neden olmaz", "isCorrect": False, "explanation": "Aksine servisitin en tipik başvuru semptomu mukopürülan vajinal akıntıdır."},
                    {"key": "D", "text": "Üst genital yola ilerleme veya pelvik inflamatuvar hastalık riski taşımaz", "isCorrect": False, "explanation": "Tedavi edilmediğinde mikroorganizmalar asendan yolla tüplere yayılabilir."}
                ]
            }
        ),
        mi(
            title="Normal Vajinal Flora: Kommensal ve Tesadüfi Mikroorganizmalar",
            subtitle="Servikovajinal ekosistem ve koruyucu bariyer mekanizmaları",
            lead="Vajen ve serviks boşluğu steril değildir; dinamik ve dengeli bir mikrobiyal ekosistem barındırır. Bu floranın dominant üyesi laktobasiller olmakla birlikte, çeşitli aerob ve anaerob bakteriler tesadüfi mikroorganizmalar olarak saptanabilir.",
            bullets=[
                ("Fizyolojik Denge", "Laktobasiller laktik asit ve hidrojen peroksit üreterek pH'yı asidik (3.8-4.5) tutar; patojen kolonizasyonunu engeller."),
                ("Tesadüfi Elemanlar", "Aerob ve anaerob bakteriler, Streptococcus türleri, Staphylococcus türleri, Enterococcus türleri, Escherichia coli ve Candida türleri florada bulunabilir."),
                ("Klinik Ayrım Zorluğu", "Vajinal floranın zenginliği nedeniyle servisitin enfeksiyöz olan ve olmayan tiplerini salt mikroskopiyle ayırmak güçleşir.")
            ],
            alert="Florada saptanan tesadüfi mikroorganizmalar her zaman patojenik enfeksiyon anlamına gelmez; klinik bulgularla birlikte değerlendirilmelidir.",
            summaries=["Vajinal flora steril olmayıp laktobasiller hakimdir.", "E. coli, Streptokok ve Candida tesadüfi elemanlar olabilir.", "Floranın varlığı enfeksiyöz ayrımı zorlaştırır."],
            cloze=["Vajinal floranın asidik pH dengesini sağlayan ve patojenlerin yerleşmesini engelleyen temel kommensal bakteri grubu laktobasillerdir.", "laktobasiller", "Floranın koruyucu temel çomak bakterisi"],
            table={
                "title": "Vajinal Ekosistemin Komponentleri",
                "headers": ["Mikrobiyal Grup", "Bakteri / Mantar Türü", "Fizyolojik Rolü"],
                "rows": [
                    {"cells": [{"text": "Baskın Koruyucu", "isMasked": False}, {"text": "Lactobacillus türleri", "isMasked": True, "hint": "Asit üreten koruyucu çomak"}, {"text": "pH 3.8-4.5 tutar", "isMasked": False}]},
                    {"cells": [{"text": "Tesadüfi Eleman", "isMasked": False}, {"text": "Escherichia coli ve Candida", "isMasked": True, "hint": "Kolon kökenli basil ve maya"}, {"text": "Asemptomatik kalabilir", "isMasked": False}]}
                ]
            },
            chain={
                "title": "Vajinal Ekosistemin Koruyucu Bariyer Zinciri",
                "steps": [
                    "1. Glikojen Kullanımı: Östrojen etkisiyle vajinal epitelde biriken glikojen laktobasiller tarafından fermente edilir.",
                    "2. Laktik Asit Üretimi: Fermantasyon sonucu laktik asit ve hidrojen peroksit salgılanarak asidik pH korunur.",
                    "3. Patojen İnhibisyonu: Asidik mikroçevre eksojen anaerob ve enterik bakterilerin aşırı çoğalmasını sınırlar.",
                    "4. Bariyer Çöküşü: Floranın bozulması veya antibiyotik kullanımı fırsatçı patojenlerin üremesine yol açar."
                ]
            },
            recall={"q": "Vajinal florada tesadüfi olarak saptanabilen kommensal mikroorganizmalara üç örnek veriniz.", "a": "Streptococcus türleri, Escherichia coli ve Candida türleridir."},
            spot={
                "topic": "Vajinal Floranın Özellikleri ve Tesadüfi Elemanlar",
                "items": [
                    {"text": "Normal vajinal florada Streptococcus, Enterococcus ve E. coli tesadüfi olarak saptanabilir.", "isLie": False, "explanation": "Bu bakteriler vajinal ekosistemde asemptomatik olarak bulunabilir."},
                    {"text": "Vajinal ekosistem fizyolojik olarak tamamen steril bir ortama sahiptir.", "isLie": True, "explanation": "Tuzak! Vajen ve serviks steril değildir; laktobasiller ve kommensallerden oluşan zengin bir floraya sahiptir."},
                    {"text": "Laktobasiller vajinal ortamın asidik kalmasını sağlayarak patojen çoğalmasını baskılar.", "isLie": False, "explanation": "Laktik asit üretimi vajinal epiteli enfeksiyonlara karşı korur."},
                    {"text": "Floranın zenginliği nedeniyle servisit tablosunun enfeksiyöz ayrımını yapmak güçleşebilir.", "isLie": False, "explanation": "Flora elemanları kültürlerde üreyerek ayırıcı tanıyı zorlaştırabilir."}
                ]
            },
            quiz={
                "q": "Vajinal flora ve servisit ayırıcı tanısı ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "opts": [
                    {"key": "A", "text": "Normal vajinal boşluk ve serviks tamamen steril dokulardır", "isCorrect": True, "explanation": "Tuzaktır! Vajen ve ektoserviks steril olmayıp zengin bir kommensal floraya ev sahipliği yapar."},
                    {"key": "B", "text": "Laktobasiller vajinanın asidik pH seviyesini muhafaza eder", "isCorrect": False, "explanation": "Laktik asit salgılayarak pH'yı 3.8-4.5 aralığında tutar."},
                    {"key": "C", "text": "Candida ve E. coli florada tesadüfi eleman olarak izlenebilir", "isCorrect": False, "explanation": "Her iki mikroorganizma da kommensal olarak florada saptanabilir."},
                    {"key": "D", "text": "Floranın varlığı enfeksiyöz servisit tanısında ayrımı zorlaştırabilir", "isCorrect": False, "explanation": "Kültürde üreyen tesadüfi elemanlar ile gerçek patojenin ayrımı klinik korelasyon gerektirir."}
                ]
            }
        ),
        mi(
            title="Chlamydia trachomatis: Servisitin En Yaygın Etkeni",
            subtitle="Cinsel yolla bulaşan enfeksiyon kliniklerinde majör servisit patojeni",
            lead="Chlamydia trachomatis, cinsel yolla bulaşan bakteriyel enfeksiyonlar arasında dünya genelinde birinci sırada yer alır. Servisit olgularının etyolojisinde en sık izole edilen majör patojenik ajandır.",
            bullets=[
                ("Prevalans Oranı", "Cinsel yolla bulaşan hastalık kliniklerine başvuran servisit vakalarının yaklaşık %40'ına kadarında etken Chlamydia trachomatis'tir."),
                ("Sinsi ve Asemptomatik Seyir", "Olguların büyük bir kısmı belirgin şikayet vermeksizin asemptomatik seyreder; bu durum sessiz yayılmaya zemin hazırlar."),
                ("Pelvik İnflamatuvar Hastalık", "Tedavi edilmeyen klamidya enfeksiyonları asendan yolla tuba uterinalara ulaşarak kronik salpenjit ve tubal infertiliteye yol açabilir.")
            ],
            alert="Chlamydia trachomatis servisit vakalarının %40'ından sorumlu olup sessiz ve asemptomatik seyri nedeniyle yüksek PİH riski taşır.",
            summaries=["Klamidya servisitin en yaygın etkenidir.", "CYBH kliniklerinde vakaların %40'ına kadar sorumludur.", "Sıklıkla asemptomatik olup PİH ve infertilite yapar."],
            cloze=["Cinsel yolla bulaşan hastalık kliniklerinde servisit vakalarının yaklaşık yüzde kırkından sorumlu en yaygın etken Chlamydia trachomatis bakterisidir.", "Chlamydia trachomatis", "Hücre içi üreyen majör CYBH bakterisi"],
            table={
                "title": "Chlamydia trachomatis Klinik ve Epidemiyolojik Profili",
                "headers": ["Özellik", "Klinik Değer", "Önemli Sonuç"],
                "rows": [
                    {"cells": [{"text": "Servisitteki Payı", "isMasked": False}, {"text": "%40'a varan oran", "isMasked": True, "hint": "En yaygın servisit etkeni"}, {"text": "En sık bakteriyel ajan", "isMasked": False}]},
                    {"cells": [{"text": "Klinik Seyir", "isMasked": False}, {"text": "Sıklıkla asemptomatik", "isMasked": True, "hint": "Belirti vermeyen sinsi seyir"}, {"text": "PİH ve infertilite riski", "isMasked": False}]}
                ]
            },
            chain={
                "title": "Klamidyal Servisitin Üst Genital Yayılım Zinciri",
                "steps": [
                    "1. Kolumnar Epitel Tutulumu: Chlamydia trachomatis endoservikal glandüler hücreleri enfekte eder.",
                    "2. Hücre İçi Çoğalma: Elementer cisimcikler retiküler cisimciğe dönüşerek hücreyi lize eder.",
                    "3. Asendan Migrasyon: Servikal bariyeri aşan bakteriler endometrium ve tubalara ilerler.",
                    "4. Tubal Hasar: Kronik inflamasyon tubal tıkanıklık, ektopik gebelik ve infertiliteyle sonuçlanır."
                ]
            },
            recall={"q": "Cinsel yolla bulaşan hastalık polikliniklerinde servisitin en yaygın etkeni nedir ve vakaların yaklaşık yüzde kaçından sorumludur?", "a": "Chlamydia trachomatis'tir; vakaların %40'ına kadarından sorumludur."},
            spot={
                "topic": "Chlamydia trachomatis ve Servisit Epidemiyolojisi",
                "items": [
                    {"text": "Chlamydia trachomatis cinsel yolla bulaşan servisit vakalarının yaklaşık %40'ından sorumludur.", "isLie": False, "explanation": "Klamidya CYBH kliniklerinde en sık saptanan servisit patojenidir."},
                    {"text": "Klamidya enfeksiyonları sıklıkla tamamen asemptomatik seyreder.", "isLie": False, "explanation": "Belirti vermediği için hastalar doktora geç başvurur ve yayılım kolaylaşır."},
                    {"text": "Chlamydia trachomatis sadece erkeklerde hastalık yapar, kadın serviksinde enfeksiyon oluşturamaz.", "isLie": True, "explanation": "Tuzak! Chlamydia kadınlarda servisitin en yaygın nedenidir ve pelvik inflamatuvar hastalığa yol açar."},
                    {"text": "Tedavi edilmeyen klamidya olguları pelvik inflamatuvar hastalık ve infertilite riski taşır.", "isLie": False, "explanation": "Tubal inflamasyon skar dokusu ve mekanik tıkanıklığa yol açabilir."}
                ]
            },
            quiz={
                "q": "Servisit etyolojisinde Chlamydia trachomatis ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                "opts": [
                    {"key": "A", "text": "Servisit vakalarının %40'ına kadarından sorumlu en yaygın etkendir", "isCorrect": True, "explanation": "Klamidya CYBH kliniklerinde en sık izole edilen servisit patojenidir."},
                    {"key": "B", "text": "Her zaman çok şiddetli ağrı ve yüksek ateşle başlar, asla asemptomatik kalmaz", "isCorrect": False, "explanation": "Aksine klamidya enfeksiyonlarının büyük kısmı sessiz ve asemptomatiktir."},
                    {"key": "C", "text": "Üst genital traktusa ilerleme veya tubal tıkanıklık yapma potansiyeli yoktur", "isCorrect": False, "explanation": "Asendan yolla salpenjit, tubal hasar ve infertilite oluşturabilir."},
                    {"key": "D", "text": "Vajinal floranın fizyolojik laktobasil dengesini oluşturan selim bir bakteridir", "isCorrect": False, "explanation": "Zorunlu hücre içi patojen bir bakteridir, flora kommensali değildir."}
                ]
            }
        ),
        mi(
            title="Herpes Simplex Virus (HSV-2): Genital Herpes ve Servisit",
            subtitle="Viral genital lezyonlar ve neonatal bulaş riskinin kritik yönetimi",
            lead="Herpes Simplex Virus tip 2 (HSV-2), kadın genital sisteminde ağrılı vezikülo-ülseratif lezyonlarla seyreden ve servikal tutulum yapabilen önemli bir viral patojendir. Primer enfeksiyonlarda yaygın servikal nekroz izlenebilir.",
            bullets=[
                ("Servikal Tutulum", "HSV servikste eritem, yüzeyel erezyonlar ve ülserasyonlarla karakterize akut herpetik servisit tablosu oluşturabilir."),
                ("Yenidoğan Bulaşı", "Doğum kanalında aktif lezyonu olan anneden doğum sırasında bebeğe bulaşma riski son derece ciddidir."),
                ("Sistemik Herpes Tehlikesi", "Yenidoğanda santral sinir sistemi tutulumu, yaygın organ yetmezliği ve ölümcül seyirli neonatal herpes tablosu gelişebilir.")
            ],
            alert="Doğum eyleminde aktif genital herpes lezyonları saptanan gebelerde neonatal sistemik herpesten korunmak amacıyla sezaryen doğum endikedir.",
            summaries=["HSV-2 vezikülo-ülseratif lezyonlar ve servisit yapar.", "Doğum sırasında anneden bebeğe bulaş riski yüksektir.", "Yenidoğanda ağır ve ölümcül sistemik herpes tablosu yapabilir."],
            cloze=["Doğum kanalından geçiş sırasında bebeğe bulaşarak ölümcül neonatal sistemik enfeksiyon riski oluşturan viral servisit etkeni Herpes Simplex Virüstür.", "Herpes Simplex Virüs", "Vezikül yapan zarflı DNA virüsü"],
            table={
                "title": "Herpes Simplex Virus Tip 2 Klinik Özellikleri",
                "headers": ["Klinik Alan", "Bulgu / Tablo", "Hayati Önem"],
                "rows": [
                    {"cells": [{"text": "Maternal Lezyon", "isMasked": False}, {"text": "Ağrılı vezikül ve ülser", "isMasked": True, "hint": "Karakteristik vezikülo-ülseratif tablo"}, {"text": "Şiddetli lokal yanma", "isMasked": False}]},
                    {"cells": [{"text": "Neonatal Risk", "isMasked": False}, {"text": "Ölümcül sistemik herpes", "isMasked": True, "hint": "Ağır neonatal yaygın enfeksiyon"}, {"text": "Sezaryen endikasyonu", "isMasked": False}]}
                ]
            },
            chain={
                "title": "HSV-2 Bulaş ve Neonatal Risk Zinciri",
                "steps": [
                    "1. Viral Reaktivasyon: Maternal servikovajinal mukozada vezikül ve ülserasyonlar aktive olur.",
                    "2. Doğum Eylemi: Bebeğin başı infekte servikovajinal sekresyonlarla doğrudan temas eder.",
                    "3. Neonatal İnvazyon: Virüs mukozalardan ve konjonktivadan yenidoğan kan dolaşımına geçer.",
                    "4. Fulminan Seyir: Karaciğer, akciğer ve beyin tutulumuyla mortalite oranı yüksek sistemik herpes gelişir."
                ]
            },
            recall={"q": "Maternal genital herpes enfeksiyonunun yenidoğandaki en tehlikeli komplikasyonu nedir?", "a": "Doğumda bulaşma sonucu gelişen ağır ve ölümcül neonatal sistemik herpes tablosudur."},
            spot={
                "topic": "Herpes Simplex Virus ve Neonatal Bulaş Dinamikleri",
                "items": [
                    {"text": "HSV-2 servikste eritematöz ve ülseratif servisit lezyonlarına neden olabilir.", "isLie": False, "explanation": "Genital herpes servikal mukozada vezikül ve ülserlerle seyreder."},
                    {"text": "Doğum sırasında anneden bebeğe bulaşma riski hayati önem taşır.", "isLie": False, "explanation": "İnfekte doğum kanalından geçiş neonatal bulaşın temel yoludur."},
                    {"text": "Yenidoğana bulaşan HSV enfeksiyonu tamamen zararsızdır ve tedavi gerektirmeden 24 saatte biter.", "isLie": True, "explanation": "Tuzak! Yenidoğanda sistemik herpes ağır organ hasarı ve yüksek ölüm riski taşır."},
                    {"text": "Aktif lezyonu olan gebelerde bebeği korumak için doğum şekli kararı kritik rol oynar.", "isLie": False, "explanation": "Bulaşı engellemek amacıyla sezaryen doğum tercih edilir."}
                ]
            },
            quiz={
                "q": "Genital herpes ve HSV serviksinin klinik önemi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                "opts": [
                    {"key": "A", "text": "Doğumda bebeğe bulaşarak ölümcül neonatal sistemik enfeksiyonlara yol açabilir", "isCorrect": True, "explanation": "Doğum kanalından geçiş neonatal sistemik herpes ve ölüm riski oluşturur."},
                    {"key": "B", "text": "Yalnızca kemik iliğinde yerleşen ve asla mukozal lezyon yapmayan bir virüstür", "isCorrect": False, "explanation": "Mukokutanöz yerleşim gösterir, vezikül ve ülserler yapar."},
                    {"key": "C", "text": "Servikste hiçbir zaman eritem, ülser veya eksüda oluşturmaz", "isCorrect": False, "explanation": "Şiddetli herpetik servisit ve mukozal ülserler yapabilir."},
                    {"key": "D", "text": "Anne-bebek geçişi tıp literatüründe hiç bildirilmemiş imkansız bir durumdur", "isCorrect": False, "explanation": "Aksine en önemli neonatal ölüm nedenlerinden biridir."}
                ]
            }
        ),
        mi(
            title="Diğer Önemli Patojenler: Trichomonas, Gonore ve Ureaplasma",
            subtitle="Servisit ve üst genital sistem enfeksiyonlarında rol oynayan ajanlar",
            lead="Servisit tablosunda Chlamydia ve HSV dışında Trichomonas vaginalis, Neisseria gonorrhoeae ve Ureaplasma urealyticum gibi patojenler de belirgin doku inflamasyonuna ve pürülan akıntıya yol açar.",
            bullets=[
                ("Trichomonas vaginalis", "Kamçılı bir protozoon olup yeşilimsi, köpüklü ve kötü kokulu akıntı ile servikste 'çilek serviks' görüntüsüne yol açabilir."),
                ("Neisseria gonorrhoeae", "Gram negatif diplokok olup endoservikal bezleri tutarak bol sarı-yeşil pürülan lökore ve şiddetli servisit yapar."),
                ("Ureaplasma urealyticum", "Hücre duvarsız mikoplazma türü olup non-gonokokal servisit ve pelvik inflamatuvar süreçlerde etken olabilir.")
            ],
            alert="Trichomonas, Gonore ve Klamidya eş zamanlı koinfeksiyon oluşturabileceğinden klinik değerlendirmede kombine yaklaşım esastır.",
            summaries=["Trichomonas yeşilimsi köpüklü akıntı ve çilek serviks yapar.", "Gonore endoservikal pürülan eksüdanın klasik etkenidir.", "Ureaplasma non-gonokokal servisitlerde rol oynar."],
            cloze=["Endoservikal bezleri tutarak yoğun sarı-yeşil pürülan akıntıya yol açan Gram negatif diplokok etken Neisseria gonorrhoeaedir.", "Neisseria gonorrhoeae", "Gonokokal servisitin bakteriyel etkeni"],
            table={
                "title": "Servisite Yol Açan Diğer Patojenlerin Karakteristikleri",
                "headers": ["Patojen Mikroorganizma", "Biyolojik Tipi", "Tipik Akıntı / Bulgu"],
                "rows": [
                    {"cells": [{"text": "Trichomonas vaginalis", "isMasked": False}, {"text": "Hareketli Protozoon", "isMasked": True, "hint": "Kamçılı tek hücreli parazit"}, {"text": "Köpüklü yeşilimsi lökore", "isMasked": False}]},
                    {"cells": [{"text": "Neisseria gonorrhoeae", "isMasked": False}, {"text": "Gram negatif diplokok", "isMasked": True, "hint": "İntrasellüler kahve çekirdeği basil"}, {"text": "Yoğun pürülan eksüda", "isMasked": False}]}
                ]
            },
            chain={
                "title": "Gonokokal ve Trikomanal Mukozal Hasar Zinciri",
                "steps": [
                    "1. Mukozal İnvazyon: Gonokok piliyle endoservikal kolumnar hücrelere, Trichomonas vajinal skuamöz epitele tutunur.",
                    "2. Sitotoksik Hasar: Enzimler ve mekanik hareket epitel bütünlüğünü bozar ve mikrokanamalara yol açar.",
                    "3. Yoğun Lökosit Göçü: Çok sayıda nötrofil lümene akarak bol miktarda pürülan eksüda oluşturur.",
                    "4. Akıntı Tablosu: Hasta kokulu, sarı-yeşil pürülan akıntı yakınmasıyla başvurur."
                ]
            },
            recall={"q": "Servisitte yeşilimsi, köpüklü akıntı ve punktat kanamalı 'çilek serviks' oluşturan paraziter etken nedir?", "a": "Trichomonas vaginalis'tir."},
            spot={
                "topic": "Trichomonas ve Neisseria Gonorrhoeae Servisiti",
                "items": [
                    {"text": "Trichomonas vaginalis kamçılı bir protozoon olup pürülan akıntı ve servisit yapabilir.", "isLie": False, "explanation": "Trichomonas vajinit ve servisitin sık görülen protozoon etkenidir."},
                    {"text": "Neisseria gonorrhoeae endoservikal kolumnar epitelde yoğun irinli eksüdaya yol açar.", "isLie": False, "explanation": "Gonore endoservikal bezleri tutarak pürülan lökore yapar."},
                    {"text": "Neisseria gonorrhoeae bir mantar türüdür ve penisilinle asla tedavi edilemez.", "isLie": True, "explanation": "Tuzak! Neisseria gonorrhoeae mantar değil, Gram negatif diplokok morfolojisinde bir bakteridir."},
                    {"text": "Ureaplasma urealyticum servisit ve üst genital enfeksiyon süreçlerine katılabilir.", "isLie": False, "explanation": "Ureaplasma non-gonokokal ürogenital enfeksiyonlarda saptanan bir bakteridir."}
                ]
            },
            quiz={
                "q": "Servisit etkenleri arasında yer alan Neisseria gonorrhoeae'nin temel mikrobiyolojik özelliği nedir?",
                "opts": [
                    {"key": "A", "text": "Endoservikal kolumnar epitelde pürülan inflamasyon yapan Gram negatif diplokoktur", "isCorrect": True, "explanation": "Neisseria gonorrhoeae Gram negatif intrasellüler diplokok olup pürülan servisit yapar."},
                    {"key": "B", "text": "Hücre duvarı içeren büyük sporlu bir küf mantarıdır", "isCorrect": False, "explanation": "Mantar değil, bakteriyel diplokoktur."},
                    {"key": "C", "text": "Sadece keratinize deride yaşayan zarfsız bir DNA virüsüdür", "isCorrect": False, "explanation": "Virüs değil, bakteridir."},
                    {"key": "D", "text": "Yalnızca amipsi psödopotlarla hareket eden bir barsak parazitidir", "isCorrect": False, "explanation": "Protozoon değil, gonokok bakterisidir."}
                ]
            }
        ),
        mi(
            title="Lökore Kavramı: Tanım, Karakteristikler ve Klinik Önemi",
            subtitle="Normalden farklı renk, koku ve dokudaki vajinal sekresyonların analizi",
            lead="Lökore, fizyolojik vajinal sekresyondan belirgin şekilde ayrılan, renk, koku veya vizkozite açısından anormallik gösteren vajinal akıntıyı tanımlar. Servisitin en temel ve belirgin kardinal bulgusudur.",
            bullets=[
                ("Terminoloji Tanımı", "Lökore, genellikle beyaz veya sarımsı tonlarda, normalden farklı renk, koku veya dokuda görülen vajinal akıntıdır."),
                ("Sekresyon Kaynağı", "Servikal bezlerin aşırı uyarılması, epitel döküntüleri ve ortama göç eden nötrofillerin karışımı ile eksüda oluşur."),
                ("Klinik Anlamı", "Hastanın polikliniğe geliş nedeni çoğunlukla lökore olup, altta yatan enfeksiyöz patojene göre köpüklü, irinli veya peynirimsi olabilir.")
            ],
            alert="Lökore varlığı, serviksin veya vajinanın aktif bir inflamatuvar yanıt altında olduğunu gösteren objektif bir klinik işarettir.",
            summaries=["Lökore normalden farklı renk, koku ve kıvamdaki akıntıdır.", "Servisitin kardinal ve en sık klinik belirtisidir.", "Beyaz veya sarımsı tonlarda pürülan nitelikte olabilir."],
            cloze=["Normalden farklı renk, koku veya dokuda görülen beyaz veya sarımsı vajinal akıntıya lökore adı verilir.", "lökore", "Anormal vajinal akıntı terimi"],
            table={
                "title": "Lökore Tipleri ve Olası Etyolojik İlişkileri",
                "headers": ["Akıntı Niteliği", "Renk ve Koku", "Düşünülecek Durum"],
                "rows": [
                    {"cells": [{"text": "Pürülan / İrinli", "isMasked": False}, {"text": "Sarı-yeşil opak, kokulu", "isMasked": True, "hint": "Bakteriyel yangısal akıntı"}, {"text": "Klamidya veya Gonore servisiti", "isMasked": False}]},
                    {"cells": [{"text": "Köpüklü Homojen", "isMasked": False}, {"text": "Gri-yeşil kötü kokulu", "isMasked": True, "hint": "Paraziter köpüklü salgı"}, {"text": "Trichomonas enfeksiyonu", "isMasked": False}]}
                ]
            },
            chain={
                "title": "Servikal İnflamasyondan Lökoreye Gidiş Zinciri",
                "steps": [
                    "1. Mukozal Yangı: Servikal epitelde patojen etkisiyle lokal sitokin salınımı ve damar geçirgenliği artar.",
                    "2. Eksüdatif Sıvı Çıkışı: Kapillerlerden plazma sıvısı ve nötrofiller doku aralığına ve servikal lümene sızar.",
                    "3. Mukus Salgısı Artışı: Endoservikal bezler irritasyona yanıt olarak hipersekresyon fazına geçer.",
                    "4. Lökore Gelişimi: Hücresel döküntü, lökosit ve mukus karışımı vajinadan dışarı akar."
                ]
            },
            recall={"q": "Lökore ne demektir ve servisit tablosundaki klinik yeri nedir?", "a": "Normalden farklı renk, koku veya dokuda, beyaz-sarı tonlardaki vajinal akıntıdır; servisitin en yaygın klinik bulgusudur."},
            spot={
                "topic": "Lökore Tanımı ve Klinik Özellikleri",
                "items": [
                    {"text": "Lökore normalden farklı renk, koku veya dokudaki vajinal akıntıyı tanımlar.", "isLie": False, "explanation": "Lökore anormal vajinal akıntı için kullanılan tıbbi terimdir."},
                    {"text": "Lökore sıklıkla beyaz veya sarımsı tonlarda mukopürülan nitelikte izlenir.", "isLie": False, "explanation": "İnflamasyonla birlikte nötrofil ve mukus birikimi rengi sarı-beyaza çevirir."},
                    {"text": "Lökore her zaman fizyolojik bir durumdur ve asla hiçbir mikrobiyal enfeksiyonla ilişkili olamaz.", "isLie": True, "explanation": "Tuzak! Lökore enfeksiyöz servisit ve vajinitlerin en tipik patolojik işaretidir."},
                    {"text": "Servisitin rutin muayenelerde fark edilmesinde lökore yakınması önemli bir ipucudur.", "isLie": False, "explanation": "Akıntı şikayeti hastanın jinekoloğa başvurmasındaki ana motiftir."}
                ]
            },
            quiz={
                "q": "Lökore terimi jinekolojik patolojide aşağıdakilerden hangisini tanımlar?",
                "opts": [
                    {"key": "A", "text": "Normalden farklı renk, koku veya dokuda görülen beyaz veya sarımsı vajinal akıntıyı", "isCorrect": True, "explanation": "Lökore anormal servikovajinal sekresyonların genel klinik adıdır."},
                    {"key": "B", "text": "Sadece over kistlerinin yırtılması sonucu karın içine olan masif kanamayı", "isCorrect": False, "explanation": "Bu durum hemoperitoneumdur, lökore değildir."},
                    {"key": "C", "text": "Endometriumun menstrüel dökülme fazındaki tamamen normal kanamasını", "isCorrect": False, "explanation": "Bu fizyolojik menstrüasyondur."},
                    {"key": "D", "text": "Vajina duvarında doğumsal olarak hiç bez bulunmaması durumunu", "isCorrect": False, "explanation": "Glandüler agenezi ile ilişkisiz bir terimdir."}
                ]
            }
        ),
        mi(
            title="Pelvik İnflamatuvar Hastalık (PİH) Riski ve Komplikasyonlar",
            subtitle="Tedavi edilmeyen servisitin asendan yayılım tehlikesi ve sekelleri",
            lead="Servisit vakalarında servikal bariyerin çökmesi, patojenlerin uterus kavititesine, tuba uterinalara ve periton boşluğuna asendan yayılımına zemin hazırlar. Bu süreç pelvik inflamatuvar hastalık tablosunu doğurur.",
            bullets=[
                ("Asendan Mekanizma", "Servikal mukus tıkacının enfeksiyonla bozulması sonucu Chlamydia ve Gonokok yukarı doğru kolayca ilerler."),
                ("Tubal Hasar", "Salpenjit gelişimi, tubal epiteldeki silyaların dökülmesine, lümen içi yapışıklıklara ve hidrosalpenkse yol açar."),
                ("Geç Sekeller", "Kronik pelvik ağrı, ektopik (dış) gebelik riskinde belirgin artış ve tubal faktöre bağlı kalıcı infertilite gelişir.")
            ],
            alert="Klamidyal servisitin erken tanı ve tedavisi, genç kadınlarda infertilite ve dış gebelik komplikasyonlarını önlemede hayati rol oynar.",
            summaries=["Tedavi edilmeyen servisit pelvik inflamatuvar hastalık yapar.", "Asendan yolla endometrit ve salpenjit gelişir.", "Tubal hasar infertilite ve dış gebelikle sonuçlanır."],
            cloze=["Servisit etkenlerinin asendan yayılımla fallop tüplerinde oluşturduğu inflamasyon ve hasar sonucu tubal faktöre bağlı infertilite gelişebilir.", "infertilite", "Çocuk sahibi olamama komplikasyonu"],
            table={
                "title": "Servisitin Üst Genital Komplikasyonları",
                "headers": ["Anatomik Düzey", "Gelişen Patoloji", "Klinik Sekel"],
                "rows": [
                    {"cells": [{"text": "Tuba Uterina", "isMasked": False}, {"text": "Akut ve kronik salpenjit", "isMasked": True, "hint": "Tüplerin iltihabı ve yapışıklık"}, {"text": "İnfertilite ve dış gebelik", "isMasked": False}]},
                    {"cells": [{"text": "Pelvik Periton", "isMasked": False}, {"text": "Pelviperitonit ve apse", "isMasked": True, "hint": "Tubo-ovaryen apse odağı"}, {"text": "Kronik pelvik ağrı", "isMasked": False}]}
                ]
            },
            chain={
                "title": "Servisitten Tubal İnfertiliteye İlerleme Zinciri",
                "steps": [
                    "1. Servikal Enfeksiyon: Klamidya veya gonokok servikal kanala yerleşip çoğalır.",
                    "2. Asendan İlerleme: Mikroplar servikal os'u geçerek endometrium üzerinden tubalara ulaşır.",
                    "3. Endosalpenjit: Tubal mukoza kıvrımları yapışır, lümen daralır veya tamamen tıkanır.",
                    "4. Fonksiyon Kaybı: Ovumun taşınamaması nedeniyle infertilite veya ektopik gebelik ortaya çıkar."
                ]
            },
            recall={"q": "Tedavi edilmeyen bakteriyel servisitin tubalarda yol açtığı en önemli iki uzun dönem komplikasyon nedir?", "a": "Kalıcı infertilite (kısırlık) ve ektopik (dış) gebelik riskidir."},
            spot={
                "topic": "Servisitin Asendan Komplikasyonları ve PİH",
                "items": [
                    {"text": "Servisit tedavi edilmediğinde mikroorganizmalar asendan yolla tüplere yayılabilir.", "isLie": False, "explanation": "Asendan yol üst genital traktus enfeksiyonlarının temel mekanizmasıdır."},
                    {"text": "Salpenjit tubal mukozada yapışıklıklara ve lümen tıkanıklığına yol açabilir.", "isLie": False, "explanation": "İnflamasyon silyalı epitel kaybı ve fibrotik yapışıklıkla sonuçlanır."},
                    {"text": "Pelvik inflamatuvar hastalık geçiren kadınlarda infertilite riski tamamen sıfırdır.", "isLie": True, "explanation": "Tuzak! PİH tubal faktöre bağlı infertilitenin en sık edinsel nedenidir."},
                    {"text": "Tubal lümenin daralması embriyonun uterusa ulaşmasını engelleyerek dış gebeliğe zemin hazırlar.", "isLie": False, "explanation": "Hasarlı tüpte zigot takılarak tubal ektopik gebelik meydana gelir."}
                ]
            },
            quiz={
                "q": "Tedavi edilmemiş klamidyal servisitin en önemli klinik komplikasyonu aşağıdakilerden hangisidir?",
                "opts": [
                    {"key": "A", "text": "Asendan yolla pelvik inflamatuvar hastalık, tubal tıkanıklık ve infertilite gelişmesi", "isCorrect": True, "explanation": "Klamidya sessizce tüplere ilerleyerek kalıcı infertilite ve dış gebelik riski oluşturur."},
                    {"key": "B", "text": "Doğrudan servikal kıkırdak metaplazisi ve eklem ankilozu yapması", "isCorrect": False, "explanation": "Servikste kıkırdak dokusu veya eklem bulunmaz."},
                    {"key": "C", "text": "Kemik iliğinde eritrosit üretimini tamamen durdurması", "isCorrect": False, "explanation": "Aplastik anemi klamidya komplikasyonu değildir."},
                    {"key": "D", "text": "Overlerde androjen üretimini kalıcı olarak sıfırlaması", "isCorrect": False, "explanation": "Hormon sentezini doğrudan sıfırlayan bir etki söz konusu değildir."}
                ]
            }
        ),
        mi(
            title="Non-Enfeksiyöz Servisit: Kimyasal, Mekanik ve İrritan Nedenler",
            subtitle="Mikrobiyal etken dışı servikal yangı ve doku reaksiyonları",
            lead="Her servisit olgusu mikrobiyal patojenlere bağlı değildir. Kimyasal maddeler, lokal alerjenler, diyafram ve tampon gibi yabancı cisimler veya travmatik girişimler servikste non-enfeksiyöz inflamasyon oluşturabilir.",
            bullets=[
                ("Kimyasal İrritanlar", "Vajinal duşlar, spermisit jeller (nonoksinol-9), deodorantlar ve parfümlü hijyen ürünleri servikal epitelde toksik hasar yapar."),
                ("Mekanik Travma", "İntrauterin araç (RİA) ipleri, uzun süre unutulan vajinal tamponlar ve doğum travması granülasyon dokusu ve yangı başlatır."),
                ("Ayırıcı Tanı", "Enfeksiyöz servisitten ayrılması için akıntı mikroskopisinde patojen saptanmaması ve irritan maruziyet öyküsü aranır.")
            ],
            alert="Non-enfeksiyöz servisitler, epitel bütünlüğünü bozarak eş zamanlı cinsel yolla bulaşan enfeksiyonların yerleşmesini kolaylaştırabilir.",
            summaries=["Servisit kimyasal ve mekanik irritasyonla da gelişebilir.", "Spermisitler ve vajinal duş kimyasal yangı yapabilir.", "Epitel hasarı enfeksiyöz patojenlere zemin hazırlar."],
            cloze=["Vajinal duşlar veya spermisit kimyasalların servikal mukozada oluşturduğu enfeksiyon dışı yangısal tabloya non-enfeksiyöz servisit denir.", "non-enfeksiyöz servisit", "Mikropsuz kimyasal yangı"],
            table={
                "title": "Non-Enfeksiyöz Servisit Etyolojik Faktörleri",
                "headers": ["Etiyolojik Kategori", "Spesifik Etken", "Oluşan Doku Yanıtı"],
                "rows": [
                    {"cells": [{"text": "Kimyasal Madde", "isMasked": False}, {"text": "Spermisitler ve duşlar", "isMasked": True, "hint": "Mukozayı tahriş eden kimyasal"}, {"text": "Epitel erozyonu ve eritem", "isMasked": False}]},
                    {"cells": [{"text": "Mekanik Faktör", "isMasked": False}, {"text": "Unutulmuş tampon ve RİA", "isMasked": True, "hint": "Yabancı cisim basısı"}, {"text": "Reaktif granülasyon dokusu", "isMasked": False}]}
                ]
            },
            chain={
                "title": "Kimyasal İrritan Kaynaklı Servisit Zinciri",
                "steps": [
                    "1. Kimyasal Temas: Spermisit veya vajinal duş serviks mukozasıyla doğrudan temas eder.",
                    "2. Hücresel Toksisite: Deterjan etkisi yüzeyel epitel hücrelerinin membranlarını bozar ve parçalar.",
                    "3. Steril Yangı: Hücre içi hasar molekülleri stromada vasküler genişleme ve yangı tetikler.",
                    "4. Klinik Yakınma: Hastada yanma, akıntı ve muayenede yaygın servikal eritem saptanır."
                ]
            },
            recall={"q": "Non-enfeksiyöz servisite yol açabilen iki kimyasal irritan faktör belirtiniz.", "a": "Spermisit içeren jeller ve vajinal duş uygulamalarıdır."},
            spot={
                "topic": "Non-Enfeksiyöz Servisitin Nedenleri",
                "items": [
                    {"text": "Kimyasal spermisitler ve vajinal duş servikal mukozada non-enfeksiyöz servisit yapabilir.", "isLie": False, "explanation": "Kimyasal tahriş epitelde steril inflamasyon oluşturur."},
                    {"text": "Unutulmuş vajinal tamponlar yabancı cisim reaksiyonu ve reaktif yangı başlatabilir.", "isLie": False, "explanation": "Mekanik travma ve biriken sekresyon mukozayı reaktif olarak bozar."},
                    {"text": "Servisit kesinlikle yalnız bakterilerle olur, hiçbir kimyasal veya mekanik etken yangı yapamaz.", "isLie": True, "explanation": "Tuzak! Servisitin enfeksiyöz olmayan kimyasal ve mekanik birçok nedeni vardır."},
                    {"text": "Non-enfeksiyöz servikal erozyonlar sekonder mikrobiyal enfeksiyonların yerleşmesini kolaylaştırabilir.", "isLie": False, "explanation": "Bozulmuş epitel bariyeri enfeksiyonlara karşı korumasız hale gelir."}
                ]
            },
            quiz={
                "q": "Servisit tablosunun non-enfeksiyöz nedenleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                "opts": [
                    {"key": "A", "text": "Spermisitler, vajinal duşlar ve unutulmuş yabancı cisimler steril inflamasyon oluşturabilir", "isCorrect": True, "explanation": "Kimyasal ve mekanik etkenler mikroorganizma olmadan da yangı yapabilir."},
                    {"key": "B", "text": "Yalnızca viral genomun DNA entegrasyonu ile ortaya çıkan herediter bir sendromdur", "isCorrect": False, "explanation": "Non-enfeksiyöz servisit edinsel ve eksternal tahriş sonucudur."},
                    {"key": "C", "text": "Mukozada hiçbir zaman eritem veya vasküler genişlemeye yol açmaz", "isCorrect": False, "explanation": "Klasik inflamasyon bulguları olan kızarıklık ve ödem gelişir."},
                    {"key": "D", "text": "Asla kadınlarda görülmez, sadece erkek üretrasında ortaya çıkan bir lezyondur", "isCorrect": False, "explanation": "Serviks kadın anatomisine ait bir organdır."},
                ]
            }
        ),
        mi(
            title="Klinik Başvuru ve Muayene Bulguları: Servikal Eritem ve Friabilite",
            subtitle="Jinekolojik spekulum muayenesinde saptanan fiziksel patolojiler",
            lead="Servisit şüphesi olan hastada standart tanı spekulum muayenesiyle konur. İnflame serviks tipik fizik muayene bulguları verir; mukozal frajilite ve temas kanaması ayırıcı tanıda yol göstericidir.",
            bullets=[
                ("Eritematöz Görünüm", "Servikal os çevresinde kılcal damarların aşırı genişlemesine bağlı parlak kırmızı renk değişimi izlenir."),
                ("Servikal Frajilite", "İnflamasyonlu epitel son derece kırılgandır; pamuklu eküvyon çubuğunun hafif temasıyla bile kolayca kanar (temas kanaması)."),
                ("Endoservikal Eksüda", "Dış açıklıktan dışarıya doğru sarı-yeşil mukopürülan pıhtı veya akıntının aktığı doğrudan gözlenir.")
            ],
            alert="Eküvyonla temas kanaması (friabilite) ve os'tan pürülan akıntı gelişi, aktif servisitin iki temel fizik muayene kriteridir.",
            summaries=["Spekulum muayenesinde eritem ve ödem izlenir.", "Eküvyon temasıyla kolay kanama (friabilite) tipiktir.", "Dış os'tan mukopürülan akıntı çıkışı saptanır."],
            cloze=["İnflame servikal mukozanın sürüntü çubuğu veya temasla kolayca kanama göstermesi özelliğine friabilite denir.", "friabilite", "Temasla kolay kanama özelliği"],
            table={
                "title": "Servisitte Spekulum Muayenesi Bulguları",
                "headers": ["Fizik Muayene Parametresi", "Tipik Görünüm", "Klinik Yorum"],
                "rows": [
                    {"cells": [{"text": "Mukozal Yüzey", "isMasked": False}, {"text": "Parlak kırmızı eritem", "isMasked": True, "hint": "Vasküler konjesyon rengi"}, {"text": "Aktif yangı işareti", "isMasked": False}]},
                    {"cells": [{"text": "Doku Direnci", "isMasked": False}, {"text": "Frajil ve temasla kanayan", "isMasked": True, "hint": "Kolay kanama bulgusu"}, {"text": "Servikal frajilite (+)", "isMasked": False}]}
                ]
            },
            chain={
                "title": "Servikal Frajilite ve Kanama Mekanizması Zinciri",
                "steps": [
                    "1. İnflamatuvar Ödem: Yangı mediyatörleri stromada ödem ve kapiller damarlanmayı artırır.",
                    "2. Epitel Bütünlüğünün Bozulması: Yüzeyel skuamöz ve kolumnar hücreler arasındaki bağlantılar gevşer.",
                    "3. Mekanik Sürtünme: Muayene veya koitus sırasında oluşan hafif doku teması damarları zedeler.",
                    "4. Temas Kanaması: Hastada postkoital kanama veya muayenede temasla sızıntı kanama izlenir."
                ]
            },
            recall={"q": "Servisit muayenesinde pamuklu çubuğun servikal os'a hafifçe dokundurulmasıyla kanama gelişmesi durumuna ne ad verilir?", "a": "Servikal friabilite (frajilite / temas kanaması) adı verilir."},
            spot={
                "topic": "Servisitte Fizik Muayene Bulguları ve Friabilite",
                "items": [
                    {"text": "İnflame servikste vasküler konjesyona bağlı belirgin eritem izlenir.", "isLie": False, "explanation": "Kızarıklık inflamasyonun temel fiziksel bulgusudur."},
                    {"text": "Servikal frajilite, eküvyon temasıyla serviksin kolayca kanamasını ifade eder.", "isLie": False, "explanation": "Frajilite aktif servisitte beklenen klasik muayene bulgusudur."},
                    {"text": "Servisitli serviks taşı sertliğinde olup muayenede asla kanamaz ve daima soluk beyazdır.", "isLie": True, "explanation": "Tuzak! Servisitli mukoza ödemli, kırmızı ve son derece kırılgandır; kolayca kanar."},
                    {"text": "Servikal dış açıklıktan mukopürülan eksüdanın gelmesi klinik tanıyı destekler.", "isLie": False, "explanation": "İrinli akıntı servisitin en objektif vizüel bulgusudur."}
                ]
            },
            quiz={
                "q": "Servisitin fizik muayenesinde servikal frajilite (friabilite) bulgusu aşağıdakilerden hangisini ifade eder?",
                "opts": [
                    {"key": "A", "text": "Servikal mukozanın hafif bir temas veya sürüntü işlemiyle kolayca kanamasını", "isCorrect": True, "explanation": "Friabilite yüzeyel damarların konjesyonuna bağlı temasla kolay kanamadır."},
                    {"key": "B", "text": "Serviksin tamamen kemik dokusuna dönüşerek taşlaşmasını", "isCorrect": False, "explanation": "Kemikleşme veya ossifikasyon ile ilgisi yoktur."},
                    {"key": "C", "text": "Servikal kanalın doğum eylemi dışında 10 santimetre açılmasını", "isCorrect": False, "explanation": "Frajilite açıklık değil kanama eğilimidir."},
                    {"key": "D", "text": "Mukozada hiçbir zaman damar bulunmamasını", "isCorrect": False, "explanation": "Tam tersine aşırı damarlanma ve konjesyon vardır."}
                ]
            }
        ),
        mi(
            title="[TEKRAR SAYFASI - CHECKPOINT 1] Servisit Etyolojisi ve Klinik Özellikler",
            subtitle="İlk 9 slaytın kazanımları, patojen profilleri ve klinik sentezi",
            lead="Bu tekrar sayfasında servisitin klinik tanımı, normal vajinal floranın tesadüfi elemanları, Chlamydia trachomatis ve HSV-2 patogenezi ile lökore kavramı eksiksiz olarak pekiştirilmektedir.",
            bullets=[
                ("Klinik Tanım ve Etyoloji", "Servisit en sık mukopürülan akıntıyla seyreden yaygın inflamatuvar tablodur; CYBH kliniklerinde en sık bakteriyel etken Chlamydia trachomatis'tir (%40)."),
                ("Flora ve Ayırıcı Tanı", "Vajinal florada laktobasiller pH'yı asidik tutar; E. coli, Streptokok ve Candida tesadüfi bulunabilir ve enfeksiyöz ayrımı zorlaştırabilir."),
                ("Majör Riskler ve Bulgular", "HSV-2 doğumda ölümcül neonatal sistemik herpes riski taşır; tedavi edilmeyen bakteriyel servisitler asendan yayılımla PİH ve infertiliteye yol açar.")
            ],
            alert="Servisit tanısında mukopürülan akıntı, servikal frajilite ve klamidya odaklı yaklaşım üst genital komplikasyonların önlenmesinde esastır.",
            summaries=["Servisit sık görülen benign servikal yangıdır.", "Klamidya vakaların %40'ından sorumlu majör etkendir.", "Tedavi edilmeyen olgular PİH ve infertilite riski taşır."],
            cloze=["Cinsel yolla bulaşan servisit olgularında en sık izole edilen ve vakaların yüzde kırkına kadarından sorumlu olan patojen Chlamydia trachomatis bakterisidir.", "Chlamydia trachomatis", "Hücre içi üreyen en sık servisit bakterisi"],
            table={
                "title": "Servisit Patojenleri ve Klinik Karşılaştırması",
                "headers": ["Mikroorganizma", "Hastalık Mekanizması", "Temel Klinik Risk"],
                "rows": [
                    {"cells": [{"text": "Chlamydia trachomatis", "isMasked": False}, {"text": "Hücre içi çoğalma ve servisit", "isMasked": True, "hint": "En yaygın servisit bakterisi"}, {"text": "PİH ve tubal infertilite", "isMasked": False}]},
                    {"cells": [{"text": "HSV-2", "isMasked": False}, {"text": "Vezikülo-ülseratif mukozal lezyon", "isMasked": True, "hint": "Ağrılı vezikül yapan virüs"}, {"text": "Neonatal ölümcül herpes", "isMasked": False}]}
                ]
            },
            chain={
                "title": "Bölüm 1 Klinik Entegrasyon Zinciri",
                "steps": [
                    "1. Patojen Yerleşimi: Klamidya veya HSV serviks mukozasına temas ederek enfeksiyon başlatır.",
                    "2. İnflamasyon ve Eksüda: Nötrofil ve plazma hücresi göçüyle mukopürülan lökore gelişir.",
                    "3. Muayene Bulgusu: Spekulumda eritem, friabilite ve servikal os'tan akıntı çıkışı saptanır.",
                    "4. Komplikasyon Tehlikesi: Tedavisiz olgularda asendan yayılımla salpenjit ve infertilite tablosu oluşur."
                ]
            },
            recall={"q": "CYBH kliniklerinde servisit vakalarının yaklaşık %40'ından sorumlu olan ve sıklıkla asemptomatik seyreden etken nedir?", "a": "Chlamydia trachomatis'tir."},
            spot={
                "topic": "Servisit Etyolojisi ve Majör Patojenler Sentezi",
                "items": [
                    {"text": "Chlamydia trachomatis servisitin en yaygın bakteriyel etkenidir.", "isLie": False, "explanation": "CYBH kliniklerinde vakaların %40'ına kadar sorumludur."},
                    {"text": "Doğumda anneden bebeğe geçen HSV-2 ölümcül neonatal sistemik enfeksiyon yapabilir.", "isLie": False, "explanation": "Neonatal herpes yüksek mortaliteye sahiptir."},
                    {"text": "Normal vajinal ekosistem tamamen mikroorganizmasız ve mutlak sterildir.", "isLie": True, "explanation": "Tuzak! Vajen laktobasiller ve tesadüfi bakterilerden oluşan zengin bir floraya sahiptir."},
                    {"text": "Tedavi edilmeyen servisit olgularında asendan yayılımla pelvik inflamatuvar hastalık gelişebilir.", "isLie": False, "explanation": "Enfeksiyon endometrium ve tubalara ilerleyebilir."}
                ]
            },
            quiz={
                "q": "Servisit etyolojisi ve klinik yönetimi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                "opts": [
                    {"key": "A", "text": "Chlamydia trachomatis en sık saptanan etkendir ve tedavi edilmezse infertilite riski taşır", "isCorrect": True, "explanation": "Klamidya vakaların %40'ından sorumlu olup tubal hasar ve infertiliteye yol açabilir."},
                    {"key": "B", "text": "Servisit daima cerrahi histerektomi gerektiren primer kemik karsinomudur", "isCorrect": False, "explanation": "Servisit benign bir inflamatuvar hastalıktır."},
                    {"key": "C", "text": "Vajinal florada asla hiçbir bakteri veya mantar hücresi bulunamaz", "isCorrect": False, "explanation": "Flora zengin bir mikrobiyal dengeye sahiptir."},
                    {"key": "D", "text": "Herpes virüsü yenidoğan bebeklerde asla hiçbir hastalık oluşturmaz", "isCorrect": False, "explanation": "Yenidoğanda ölümcül sistemik herpes yapabilir."}
                ]
            }
        )
    ]
    sections.append({"title": "Servisit Etyolojisi, Vajinal Flora ve Temel Patojenler", "items": sec1_items})
    
    return sections

print("build_sections_49_pt1 ready.")
