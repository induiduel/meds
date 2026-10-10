import json

def get_sec1():
    return [
        {
            "slideNumber": 1,
            "title": "Serviks Anatomisi ve Servisit Patolojisine Giriş",
            "subtitle": "Ektoserviks, endoserviks ve inflamatuvar süreçlerin klinik çerçevesi",
            "clinicalFocus": "Anatomi ve Genel Patoloji",
            "content": "Serviks, uterusun vajinaya açılan distal boyun kısmıdır ve kadın genital sisteminde inflamatuvar lezyonların en sık yerleştiği anatomik bölgedir. Servisit terimi, servikal mukozanın enfeksiyöz veya non-enfeksiyöz yangısal reaksiyonunu tanımlar.\n\n- **Anatomik Katmanlar:** Serviks temelde vajinaya bakan ektoserviks ve uterusa uzanan endoservikal kanal olmak üzere iki belirgin anatomik ve histolojik kompartmandan meydana gelir.\n- **Klinik Görünüm:** Servisit hastalarında en belirgin başvuru semptomu lökore olarak adlandırılan irinli, müköz veya sarı-yeşil renkli vajinal akıntıdır.\n- **Tanısal Zorluk:** Normal vajinal mikrobiyotanın zenginliği ve tesadüfi bakterilerin varlığı nedeniyle enfeksiyonlu ve enfeksiyonsuz servisit ayrımı klinik muayenede her zaman kolay değildir.\n\n> [!NOTE]\n> Servisit klinik pratikte son derece yaygın olup kadınların büyük çoğunluğunda yaşamın bir evresinde semptomatik ya da asemptomatik olarak izlenir.",
            "synthesisNarrative": "Serviks, uterusun vajinaya açılan distal boyun kısmıdır ve kadın genital sisteminde inflamatuvar lezyonların en sık yerleştiği anatomik bölgedir. Servisit terimi, servikal mukozanın enfeksiyöz veya non-enfeksiyöz yangısal reaksiyonunu tanımlar.\n\n- **Anatomik Katmanlar:** Serviks temelde vajinaya bakan ektoserviks ve uterusa uzanan endoservikal kanal olmak üzere iki belirgin anatomik ve histolojik kompartmandan meydana gelir.\n- **Klinik Görünüm:** Servisit hastalarında en belirgin başvuru semptomu lökore olarak adlandırılan irinli, müköz veya sarı-yeşil renkli vajinal akıntıdır.\n- **Tanısal Zorluk:** Normal vajinal mikrobiyotanın zenginliği ve tesadüfi bakterilerin varlığı nedeniyle enfeksiyonlu ve enfeksiyonsuz servisit ayrımı klinik muayenede her zaman kolay değildir.\n\n> [!NOTE]\n> Servisit klinik pratikte son derece yaygın olup kadınların büyük çoğunluğunda yaşamın bir evresinde semptomatik ya da asemptomatik olarak izlenir.",
            "bulletPoints": [
                "Servisit, servikal mukozanın yaygın inflamasyonudur.",
                "En sık semptom pürülan veya mukoid lökoredir.",
                "Ektoserviks ve endoserviks iki ana anatomik bölümdür."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Servikal mukozanın inflamatuvar tablosunda en sık başvuru yakınması lökore olarak adlandırılan vajinal akıntıdır.",
                    "maskedTerm": "lökore",
                    "hint": "Normalden farklı renk ve kıvamdaki vajinal akıntı terimi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Servisit Genel Patolojisi",
                    "tableHeaders": ["Özellik", "Klinik Yansıması", "Tanısal Değeri"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Başvuru Semptomu", "isMasked": False},
                                {"text": "Pürülan veya mukopürülan vajinal akıntı", "isMasked": True, "hint": "iltihaplı lökore akıntısı"},
                                {"text": "Klinik şüpheyi doğuran ilk bulgudur"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Etyolojik Ayrım", "isMasked": False},
                                {"text": "Enfeksiyöz veya non-enfeksiyöz yangı", "isMasked": False},
                                {"text": "Kültür ve NAAT testleri ile doğrulanır", "isMasked": True, "hint": "mikrobiyal moleküler doğrulama"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "İnflamasyondan Lökore Gelişimine",
                    "steps": [
                        "1. Etken Teması: Servikal mukoza enfeksiyöz patojenler veya kimyasal irritanlarla temas eder.",
                        "2. Vasküler Yanıt: Mukozal kapillerlerde permeabilite artar ve dokuya nötrofil lökosit göçü başlar.",
                        "3. Salgı Artışı: Endoservikal bezlerin mukus üretimi artar ve dökülen hücrelerle karışır.",
                        "4. Lökore Oluşumu: İrinli ve mukoid eksüda dış genital kanaldan akıntı şeklinde dışarı atılır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Servisit kliniğinde hastaların hekime başvurmasına en sık yol açan kardinal semptom nedir?",
                    "answer": "Lökore adı verilen anormal, mukopürülan veya pürülan vajinal akıntıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Servisit Genel Tanımı ve Bulguları",
                    "items": [
                        {"text": "Servisit serviks mukozasının son derece sık görülen inflamatuvar bir tablosudur.", "isLie": False, "explanation": "Doğru. Kadın alt genital yolunun en yaygın yangısal durumudur."},
                        {"text": "Klinikte en sık izlenen yakınma pürülan veya mukopürülan karakterde lökoredir.", "isLie": False, "explanation": "Doğru. Hastalar sıklıkla akıntı şikayetiyle başvurur."},
                        {"text": "Normal vajinal mikrobiyota nedeniyle enfeksiyonlu ve enfeksiyonsuz servisiti ayırt etmek güç olabilir.", "isLie": False, "explanation": "Doğru. Kommensal flora ayırıcı tanıda zorluk yaratır."},
                        {"text": "Servisit daima kemik metastazı ile başlayan primer bir iskelet sistemi malignitesidir.", "isLie": True, "explanation": "Tuzak! Servisit serviksin selim inflamasyonudur, kemik tümörü değildir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servisit patolojisi ve klinik semptomatolojisi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Serviksin inflamatuvar bir tablosu olup en sık mukopürülan lökore ile kendini gösterir",
                            "isCorrect": True,
                            "explanation": "Servisit yaygın inflamatuvar lezyondur ve tipik prezentasyonu lökoredir."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca 80 yaş üstü kadınlarda görülen nadir bir primer nörolojik hastalıktır",
                            "isCorrect": False,
                            "explanation": "Üreme çağındaki kadınlarda çok yaygın jinekolojik durumdur."
                        },
                        {
                            "key": "C",
                            "text": "Hastalıkta vajinal akıntı kesinlikle görülmez, sadece görme kaybı oluşur",
                            "isCorrect": False,
                            "explanation": "Lökore servisitin en tipik kardinal semptomudur."
                        },
                        {
                            "key": "D",
                            "text": "Servisit tanısı konan hastaların tümünde derhal böbrek nakli yapılmalıdır",
                            "isCorrect": False,
                            "explanation": "Servisitin böbrek yetmezliği veya nakille ilgisi yoktur; lokal/ampirik tedavi verilir."
                        }
                    ]
                }
            ]
        },
        {
            "slideNumber": 2,
            "title": "Normal Vajinal Flora ve Servikal Mikrobiyota",
            "subtitle": "Kommensal bakteriler, asidik pH ve koruyucu bariyer mekanizmaları",
            "clinicalFocus": "Mikrobiyoloji ve Vajinal Flora",
            "content": "Kadın alt genital sisteminde ektoserviks ve vajina steril boşluklar olmayıp zengin bir kommensal mikroorganizma topluluğu ile kolonizedir. Bu mikrobiyota patojenlerin servikal kanala yerleşmesini önleyen fizyolojik bir kalkan görevi görür.\n\n- **Flora Elemanları:** Sağlıklı kadınların florasında aerob ve anaerob bakteriler, Streptococcus türleri, Staphylococcus suşları, Enterococcus faecalis, Escherichia coli ve az miktarda Candida türleri bulunabilir.\n- **Laktobasillerin Rolü:** Döderlein laktobasilleri glikojeni yıkarak laktik asit üretir ve vajinal pH'yı 3.8-4.5 aralığında asidik tutar.\n- **Patojenik Denge:** Bu fizyolojik bakteriler fırsatçı ajanların üremesini engeller; floranın bozulması servisit ve vajinit zeminini hazırlar.\n\n> [!NOTE]\n> Floradaki bakterilerin izolasyonu her zaman enfeksiyon anlamına gelmez; klinik semptomlar ve lökosit varlığıyla birlikte değerlendirilmelidir.",
            "synthesisNarrative": "Kadın alt genital sisteminde ektoserviks ve vajina steril boşluklar olmayıp zengin bir kommensal mikroorganizma topluluğu ile kolonizedir. Bu mikrobiyota patojenlerin servikal kanala yerleşmesini önleyen fizyolojik bir kalkan görevi görür.\n\n- **Flora Elemanları:** Sağlıklı kadınların florasında aerob ve anaerob bakteriler, Streptococcus türleri, Staphylococcus suşları, Enterococcus faecalis, Escherichia coli ve az miktarda Candida türleri bulunabilir.\n- **Laktobasillerin Rolü:** Döderlein laktobasilleri glikojeni yıkarak laktik asit üretir ve vajinal pH'yı 3.8-4.5 aralığında asidik tutar.\n- **Patojenik Denge:** Bu fizyolojik bakteriler fırsatçı ajanların üremesini engeller; floranın bozulması servisit ve vajinit zeminini hazırlar.\n\n> [!NOTE]\n> Floradaki bakterilerin izolasyonu her zaman enfeksiyon anlamına gelmez; klinik semptomlar ve lökosit varlığıyla birlikte değerlendirilmelidir.",
            "bulletPoints": [
                "Ektoserviks ve vajina zengin kommensal floraya sahiptir.",
                "Streptokok, stafilokok, E. coli ve Candida bulunabilir.",
                "Flora dengesinin bozulması enfeksiyon riskini artırır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Sağlıklı kadın vajinal florasında aerob bakterilerin yanı sıra Streptococcus ve Candida türleri tesadüfen saptanabilir.",
                    "maskedTerm": "Candida",
                    "hint": "Normal florada bulunabilen maya mantarı cinsi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vajinal Mikrobiyotada Bulunabilen Mikroorganizmalar",
                    "tableHeaders": ["Mikroorganizma Grubu", "Flora Durumu", "Fizyolojik Anlamı"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Laktobasiller", "isMasked": False},
                                {"text": "Baskın kommensal bakteri", "isMasked": True, "hint": "asidik pH'yı koruyan çomak"},
                                {"text": "Laktik asit üreterek asidik pH'yı korur"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Enterococcus ve E. coli", "isMasked": False},
                                {"text": "Tesadüfi flora elemanı", "isMasked": False},
                                {"text": "Aşırı çoğalmadıkça asemptomatik kalabilir", "isMasked": True, "hint": "sayıca sınırlı kolonizasyon"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Flora Dengesinden Kolonizasyona",
                    "steps": [
                        "1. Asidik Ortam: Laktobasiller ürettikleri asit ile pH değerini 4.5 altında tutar.",
                        "2. Flora Baskılanması: Antibiyotik veya hormonal değişim laktobasil sayısını düşürür.",
                        "3. pH Yükselmesi: Asidik bariyer zayıflar ve fırsatçı mikroorganizmalar hızla ürer.",
                        "4. Servikal İrritasyon: Artan bakteri yükü servikal mukozada inflamatuvar reaksiyonu tetikler."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Normal vajinal florada hastalık oluşturmaksızın tesadüfen saptanabilen kommensal mikroorganizmalara üç örnek veriniz.",
                    "answer": "Streptococcus türleri, Staphylococcus suşları, Enterococcus türleri, Escherichia coli ve Candida türleridir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vajinal ve Servikal Mikrobiyota",
                    "items": [
                        {"text": "Normal vajinal florada aerob ve anaerob bakteriler bir arada bulunabilir.", "isLie": False, "explanation": "Doğru. Mikrobiyota karmaşık dengeli bir ekosistemdir."},
                        {"text": "Sağlıklı bireylerin vajinal sürüntüsünde Candida türleri tesadüfen izlenebilir.", "isLie": False, "explanation": "Doğru. Kommensal kolonizasyon asemptomatik olabilir."},
                        {"text": "Streptokok ve stafilokoklar normal vajina florasında yer alabilen elemanlardır.", "isLie": False, "explanation": "Doğru. Rutin florada düşük sayılarda saptanabilirler."},
                        {"text": "Sağlıklı vajinal boşluk ve serviks tamamen steril olup hiçbir bakteri barındırmaz.", "isLie": True, "explanation": "Tuzak! Vajina ve ektoserviks steril değildir; laktobasiller ve kommensal mikroorganizmalarla kolonizedir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Normal vajinal flora ve servikal mikrobiyota hakkında aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Streptococcus, Staphylococcus, E. coli ve Candida türleri sağlıklı florada tesadüfen bulunabilir",
                            "isCorrect": True,
                            "explanation": "Bu mikroorganizmalar asemptomatik kadınların florasında normal olarak izlenebilir."
                        },
                        {
                            "key": "B",
                            "text": "Vajina lümeninde tek bir bakteri hücresinin görülmesi doğrudan sepsis kanıtıdır",
                            "isCorrect": False,
                            "explanation": "Vajina zengin bir kommensal floraya sahiptir, steril bir doku değildir."
                        },
                        {
                            "key": "C",
                            "text": "Laktobasiller vajinal ortamı aşırı alkali yaparak (pH > 9) mantarları öldürür",
                            "isCorrect": False,
                            "explanation": "Laktobasiller laktik asit üreterek pH'yı asidik (3.8-4.5) tutar."
                        },
                        {
                            "key": "D",
                            "text": "Normal floranın mevcudiyeti tüm cinsel yolla bulaşan hastalıkları %100 engeller",
                            "isCorrect": False,
                            "explanation": "Flora koruyucu bariyerdir ancak virülan CYBH etkenlerini mutlak olarak engelleyemez."
                        }
                    ]
                }
            ]
        },
        {
            "slideNumber": 3,
            "title": "En Yaygın Servisit Etkeni: Chlamydia trachomatis",
            "subtitle": "CYBH kliniklerinin %40'ından sorumlu zorunlu hücre içi patojen",
            "clinicalFocus": "Mikrobiyal Etyoloji",
            "content": "Chlamydia trachomatis, cinsel yolla bulaşan enfeksiyonlar arasında serviksin glandüler epitelini en sık enfekte eden bakteriyel patojendir. CYBH kliniklerine başvuran servisit vakalarının yaklaşık %40'ından sorumludur.\n\n- **Biyolojik Özellik:** Gram negatif hücre duvarına benzer yapıya sahip, zorunlu hücre içi (intraselüler) bir bakteridir; enerji üretimi için konak hücre ATP'sine bağımlıdır.\n- **Klinik Seyir:** Olguların önemli bir kısmı asemptomatik seyreder; bu sessiz taşıyıcılık enfeksiyonun toplumda fark edilmeden yayılmasına neden olur.\n- **Komplikasyon Riski:** Tedavi edilmeyen Chlamydia servisiti asendan yolla endometriuma ve tubalara yayılarak Pelvik İnflamatuvar Hastalık (PİH) ve tubal infertiliteye yol açabilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Cinsel yolla bulaşan servisit vakalarında en yaygın bakteriyel etken Chlamydia trachomatis'tir (%40'a varan oran).",
            "synthesisNarrative": "Chlamydia trachomatis, cinsel yolla bulaşan enfeksiyonlar arasında serviksin glandüler epitelini en sık enfekte eden bakteriyel patojendir. CYBH kliniklerine başvuran servisit vakalarının yaklaşık %40'ından sorumludur.\n\n- **Biyolojik Özellik:** Gram negatif hücre duvarına benzer yapıya sahip, zorunlu hücre içi (intraselüler) bir bakteridir; enerji üretimi için konak hücre ATP'sine bağımlıdır.\n- **Klinik Seyir:** Olguların önemli bir kısmı asemptomatik seyreder; bu sessiz taşıyıcılık enfeksiyonun toplumda fark edilmeden yayılmasına neden olur.\n- **Komplikasyon Riski:** Tedavi edilmeyen Chlamydia servisiti asendan yolla endometriuma ve tubalara yayılarak Pelvik İnflamatuvar Hastalık (PİH) ve tubal infertiliteye yol açabilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Cinsel yolla bulaşan servisit vakalarında en yaygın bakteriyel etken Chlamydia trachomatis'tir (%40'a varan oran).",
            "bulletPoints": [
                "En yaygın servisit etkeni Chlamydia trachomatis'tir.",
                "CYBH kliniklerinde vakaların %40'ından sorumludur.",
                "Asemptomatik kalabilir ve PİH riski doğurur."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Cinsel yolla bulaşan servisit olgularında en sık sorumlu bakteriyel patojen Chlamydia trachomatis olarak tanımlanır.",
                    "maskedTerm": "Chlamydia trachomatis",
                    "hint": "CYBH kliniklerinde servisitin %40'ından sorumlu hücre içi bakteri"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Chlamydia trachomatis Servisiti",
                    "tableHeaders": ["Özellik", "Klinik / Biyolojik Karakter", "Önemi"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Görülme Sıklığı", "isMasked": False},
                                {"text": "CYBH servisitlerinin yaklaşık %40'ı", "isMasked": True, "hint": "en sık bakteriyel oran"},
                                {"text": "En yaygın servisit etkeni kabul edilir"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Hedef Doku", "isMasked": False},
                                {"text": "Endoservikal kolumnar epitel", "isMasked": False},
                                {"text": "Pelvik inflamatuvar hastalık riski taşır", "isMasked": True, "hint": "asendan yayılım riski"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Klamidya Servisitinden Tubal Hasara",
                    "steps": [
                        "1. İnosit Teması: Chlamydia elementer cisimcikleri endoservikal kolumnar hücrelere penetre olur.",
                        "2. İntraselüler Replikasyon: Retiküler cisimciklere dönüşüp çoğalarak hücre lizisine yol açar.",
                        "3. Asemptomatik Yangı: Şikayet yaratmadan mukozada sessiz lökositik infiltrasyon oluşturur.",
                        "4. Asendan İnfiltrasyon: Bakteriler yukarı ilerleyerek endometrit, salpenjit ve tubal infertiliteye neden olur."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "CYBH kliniklerine başvuran servisit hastalarında en sık izole edilen bakteriyel patojen ve görülme oranı nedir?",
                    "answer": "Chlamydia trachomatis'tir ve olguların yaklaşık %40'ından sorumludur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Chlamydia Servisiti Özellikleri",
                    "items": [
                        {"text": "Chlamydia trachomatis cinsel yolla bulaşan servisitlerin en yaygın etkenidir.", "isLie": False, "explanation": "Doğru. Olguların yaklaşık %40'ını oluşturur."},
                        {"text": "Enfeksiyon çoğu hastada belirgin şikayet oluşturmadan asemptomatik seyredebilir.", "isLie": False, "explanation": "Doğru. Sessiz seyri nedeniyle yayılımı kolaylaşır."},
                        {"text": "Asendan yayılımla pelvik inflamatuvar hastalık ve infertiliteye yol açabilir.", "isLie": False, "explanation": "Doğru. Tubal obstrüksiyonun önemli bir nedenidir."},
                        {"text": "Chlamydia servisiti daima dışkıda amip kistlerinin görülmesiyle kesinleşir.", "isLie": True, "explanation": "Tuzak! Chlamydia bir protozoon veya amip değil, zorunlu hücre içi bakteridir; NAAT ile saptanır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Cinsel yolla bulaşan servisit olgularının etyolojisi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Chlamydia trachomatis en yaygın servisit etkeni olup vakaların yaklaşık %40'ından sorumludur",
                            "isCorrect": True,
                            "explanation": "Amfi ders notunun kilit sınav spotudur; en sık bakteriyel servisit etkenidir."
                        },
                        {
                            "key": "B",
                            "text": "Servisitlerin %99'u kızamık virüsünün servikste üremesiyle gelişir",
                            "isCorrect": False,
                            "explanation": "Kızamık etken değildir; bakteriyel ajanlar ve HSV/HPV rol oynar."
                        },
                        {
                            "key": "C",
                            "text": "Chlamydia enfeksiyonu daima çok şiddetli ağrılı sarılık tablosuyla başlar",
                            "isCorrect": False,
                            "explanation": "Klamidya sıklıkla asemptomatik lokal servisit yapar; sarılık yapmaz."
                        },
                        {
                            "key": "D",
                            "text": "Chlamydia trachomatis hücre dışında serbestçe beslenen dev bir helminttir",
                            "isCorrect": False,
                            "explanation": "Zorunlu hücre içi küçük bir bakteridir."
                        }
                    ]
                }
            ]
        },
        {
            "slideNumber": 4,
            "title": "Diğer Cinsel Yolla Bulaşan Servisit Patojenleri",
            "subtitle": "Neisseria gonorrhoeae, Trichomonas vaginalis ve Ureaplasma urealyticum",
            "clinicalFocus": "Mikrobiyal Patojenler",
            "content": "Klamidya dışında servikste akut ve kronik inflamasyona yol açan diğer önemli cinsel geçişli patojenler Neisseria gonorrhoeae, Trichomonas vaginalis ve Ureaplasma urealyticum'dur. Bu ajanlar benzer klinik tablolarla prezante olabilir.\n\n- **Neisseria gonorrhoeae:** Gram negatif diplokoktur; belirgin pürülan eksüda ve yoğun nötrofil birikimiyle karakterize akut endoservisit oluşturur.\n- **Trichomonas vaginalis:** Kamçılı bir protozoondur; vajina ve ektoservikste çilek serviks (strawberry cervix) görünümü ve köpüklü akıntı yapabilir.\n- **Ureaplasma urealyticum:** Hücre duvarı olmayan mikoplazma grubundandır; nongonokoksik üretrit ve servisit spektrumunda rol oynar.\n\n> [!NOTE]\n> Patojenlerin sıklıkla bir arada bulunabilmesi (ko-enfeksiyon) nedeniyle servisit olgularında çoklu etken taraması yapılması önerilir.",
            "synthesisNarrative": "Klamidya dışında servikste akut ve kronik inflamasyona yol açan diğer önemli cinsel geçişli patojenler Neisseria gonorrhoeae, Trichomonas vaginalis ve Ureaplasma urealyticum'dur. Bu ajanlar benzer klinik tablolarla prezante olabilir.\n\n- **Neisseria gonorrhoeae:** Gram negatif diplokoktur; belirgin pürülan eksüda ve yoğun nötrofil birikimiyle karakterize akut endoservisit oluşturur.\n- **Trichomonas vaginalis:** Kamçılı bir protozoondur; vajina ve ektoservikste çilek serviks (strawberry cervix) görünümü ve köpüklü akıntı yapabilir.\n- **Ureaplasma urealyticum:** Hücre duvarı olmayan mikoplazma grubundandır; nongonokoksik üretrit ve servisit spektrumunda rol oynar.\n\n> [!NOTE]\n> Patojenlerin sıklıkla bir arada bulunabilmesi (ko-enfeksiyon) nedeniyle servisit olgularında çoklu etken taraması yapılması önerilir.",
            "bulletPoints": [
                "Gonokok, Trichomonas ve Ureaplasma önemli etkenlerdir.",
                "N. gonorrhoeae yoğun pürülan eksüda oluşturur.",
                "Ko-enfeksiyon sıktır ve kombine tedavi gerektirebilir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Akut pürülan servisite yol açan Gram negatif diplokok yapısındaki bakteri Neisseria gonorrhoeae olarak adlandırılır.",
                    "maskedTerm": "Neisseria gonorrhoeae",
                    "hint": "Gonore etkeni olan intraselüler diplokok"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Cinsel Yolla Bulaşan Servisit Patojenleri",
                    "tableHeaders": ["Patojen", "Biyolojik Sınıfı", "Tipik Lezyon Özelliği"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Neisseria gonorrhoeae", "isMasked": False},
                                {"text": "Gram negatif diplokok", "isMasked": True, "hint": "nötrofil içi kahve çekirdeği diplokok"},
                                {"text": "Yoğun pürülan endoservikal eksüda"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Trichomonas vaginalis", "isMasked": False},
                                {"text": "Kamçılı protozoon", "isMasked": False},
                                {"text": "Köpüklü akıntı ve punktat kanamalar", "isMasked": True, "hint": "çilek serviks görünümü"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Gonokoksik Endoservisit Patogenezi",
                    "steps": [
                        "1. Pili ile Tutunma: Neisseria gonorrhoeae pili ve Opa proteinleriyle endoservikal kolumnar hücrelere bağlanır.",
                        "2. Endositoz ve Hasar: Bakteri hücre içine girip submukozaya geçer ve endotoksin salgılar.",
                        "3. Nötrofil Kemotaksisi: Doku hasarı masif polimorfonükleer lökosit infiltrasyonuna neden olur.",
                        "4. Pürülan Akıntı: Servikal kanaldan dışarı taşan yoğun sarı-yeşil irinli lökore izlenir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Chlamydia trachomatis dışında servikste pürülan yangıya en sık neden olan Gram negatif diplokok patojen hangisidir?",
                    "answer": "Neisseria gonorrhoeae'dir (gonokok)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Gonokoksik ve Trikomonal Servisit",
                    "items": [
                        {"text": "Neisseria gonorrhoeae pürülan endoservikal akıntıya yol açan önemli bir bakteridir.", "isLie": False, "explanation": "Doğru. Gonore klasik pürülan servisit nedenidir."},
                        {"text": "Trichomonas vaginalis servikste ve vajinada enflamasyon yapan hareketli bir parazittir.", "isLie": False, "explanation": "Doğru. Kamçılı protozoondur."},
                        {"text": "Ureaplasma urealyticum cinsel yolla bulaşan servisit spektrumunda yer alabilir.", "isLie": False, "explanation": "Doğru. Atipik genital patojenlerdendir."},
                        {"text": "Neisseria gonorrhoeae bir RNA virüsü olup hiçbir zaman antibiyotiklerden etkilenmez.", "isLie": True, "explanation": "Tuzak! Neisseria gonorrhoeae bir virüs değil, Gram negatif diplokok bir bakteridir; antibiyotiklerle tedavi edilir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servisit etkenleri arasında yer alan Neisseria gonorrhoeae ve Trichomonas vaginalis ile ilgili hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "N. gonorrhoeae pürülan eksüda yapan bakteri, T. vaginalis ise akıntı yapabilen kamçılı protozoondur",
                            "isCorrect": True,
                            "explanation": "Her iki ajan da servikste yangı ve karakteristik akıntı tablolarına yol açar."
                        },
                        {
                            "key": "B",
                            "text": "T. vaginalis bir mantar sporu olup vajinal asiditeyi daima sıfıra indirir",
                            "isCorrect": False,
                            "explanation": "T. vaginalis mantar değil, hareketli bir protozoondur."
                        },
                        {
                            "key": "C",
                            "text": "Gonokok enfeksiyonu yalnızca el ve ayak tırnaklarında kabarcıklar oluşturur",
                            "isCorrect": False,
                            "explanation": "Gonokok primer olarak genital mukoza ve endoserviksi tutar."
                        },
                        {
                            "key": "D",
                            "text": "Ureaplasma bakterileri daima kalın bir kitin kabukla çevrilidir",
                            "isCorrect": False,
                            "explanation": "Ureaplasma hücre duvarından yoksundur."
                        }
                    ]
                }
            ]
        },
        {
            "slideNumber": 5,
            "title": "Viral Servisitler: Genital Herpes (HSV-2) ve Neonatal Risk",
            "subtitle": "Ağrılı veziküller, latent enfeksiyon ve intrapartum dikey bulaşma",
            "clinicalFocus": "Viral Enfeksiyon ve Obstetrik Risk",
            "content": "Herpes Simplex Virus tip 2 (HSV-2), anogenital bölgeyi ve serviksi enfekte eden en önemli zarflı DNA virüslerinden biridir. Primer enfeksiyon sonrasında duyusal gangliyonlarda ömür boyu latent kalır.\n\n- **Klinik Tablo:** Serviks ve vulvada eritemli taban üzerinde gruplaşmış veziküller, ülserasyonlar ve şiddetli lokal ağrı ile karakterizedir.\n- **Sistemik Yayılım:** Primer enfeksiyonda ateş, kırgınlık ve ağrılı bilateral inguinal lenfadenopati tabloya sıklıkla eşlik eder.\n- **Neonatal Risk:** Aktif servikal lezyonu olan gebelerde doğum eylemi sırasında vajinal kanaldan bebeğe bulaşma, yenidoğanda ağır, yaygın ve fatal sistemik herpes enfeksiyonuna yol açabilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Doğum sırasında maternal genital HSV lezyonlarından bebeğe bulaşma, yenidoğanda ölümcül sistemik herpes tablosu riski taşır; bu durumda sezaryen doğum endikedir.",
            "synthesisNarrative": "Herpes Simplex Virus tip 2 (HSV-2), anogenital bölgeyi ve serviksi enfekte eden en önemli zarflı DNA virüslerinden biridir. Primer enfeksiyon sonrasında duyusal gangliyonlarda ömür boyu latent kalır.\n\n- **Klinik Tablo:** Serviks ve vulvada eritemli taban üzerinde gruplaşmış veziküller, ülserasyonlar ve şiddetli lokal ağrı ile karakterizedir.\n- **Sistemik Yayılım:** Primer enfeksiyonda ateş, kırgınlık ve ağrılı bilateral inguinal lenfadenopati tabloya sıklıkla eşlik eder.\n- **Neonatal Risk:** Aktif servikal lezyonu olan gebelerde doğum eylemi sırasında vajinal kanaldan bebeğe bulaşma, yenidoğanda ağır, yaygın ve fatal sistemik herpes enfeksiyonuna yol açabilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Doğum sırasında maternal genital HSV lezyonlarından bebeğe bulaşma, yenidoğanda ölümcül sistemik herpes tablosu riski taşır; bu durumda sezaryen doğum endikedir.",
            "bulletPoints": [
                "HSV-2 ağrılı vezikül ve ülserlerle karakterizedir.",
                "Gangliyonlarda ömür boyu latent kalabilir.",
                "Yenidoğana intrapartum bulaş ağır sistemik herpes yapar."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Doğum kanalında aktif HSV lezyonu bulunan annelerden doğum sırasında bebeğe bulaşarak ölümcül sistemik herpes gelişebilir.",
                    "maskedTerm": "sistemik herpes",
                    "hint": "Yenidoğanda yüksek mortalite ile seyreden yaygın viral tablo"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Genital Herpes (HSV-2) ve Neonatal İntrapartum Risk",
                    "tableHeaders": ["Dönem / Durum", "Klinik Özellik", "Kritik Yönetim"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Maternal Primer Atak", "isMasked": False},
                                {"text": "Ağrılı vezikül, ülser ve yüksek viral saçılım", "isMasked": True, "hint": "aktif veziküler lezyonlar"},
                                {"text": "Bulaş riski nüks atağa göre çok daha yüksektir"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Neonatal Bulaşma", "isMasked": False},
                                {"text": "Doğum kanalından geçiş sırasında temas", "isMasked": False},
                                {"text": "Sistemik tutulumu önlemek için sezaryen doğum yapılır", "isMasked": True, "hint": "koruyucu cerrahi doğum şekli"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "İntrapartum HSV Bulaş Patogenezi",
                    "steps": [
                        "1. Aktif Lezyon: Doğum kanalında anneye ait servikovajinal HSV-2 vezikülleri mevcuttur.",
                        "2. Dikey Temas: Fetus doğum eyleminde lezyonlarla ve viral partiküllerle doğrudan temas eder.",
                        "3. Viral İnvazyon: İmmün sistemi immatür olan yenidoğanda virüs mukoza ve deriden penetre olur.",
                        "4. Sistemik Yayılım: Karaciğer, akciğer ve SSS tutulumu ile fatal neonatal herpes gelişir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Maternal genital herpes (HSV-2) enfeksiyonunun gebelik ve doğum sürecindeki en tehlikeli komplikasyonu nedir?",
                    "answer": "Doğum kanalından geçiş sırasında bebeğe bulaşarak yenidoğanda ağır ve ölümcül sistemik herpes tablosuna yol açmasıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Genital Herpes ve Neonatal Risk",
                    "items": [
                        {"text": "HSV-2 serviks ve vulvada ağrılı vezikül ve ülserlerle karakterizedir.", "isLie": False, "explanation": "Doğru. Tipik klinik görünümüdür."},
                        {"text": "Primer enfeksiyonu takiben sakral gangliyonlarda latent kalabilir.", "isLie": False, "explanation": "Doğru. Yaşam boyu latentlik herpesin ana özelliğidir."},
                        {"text": "Doğum sırasında yenidoğana bulaşarak ölümcül sistemik enfeksiyon riski yaratır.", "isLie": False, "explanation": "Doğru. Neonatal herpes mortalitesi yüksek tablodur."},
                        {"text": "HSV-2 enfeksiyonu olan yenidoğanlar hiçbir tedavi almadan daima tamamen bağışık kalır.", "isLie": True, "explanation": "Tuzak! Yenidoğan herpesi ölümcül seyreder; acil antiviral tedavi ve koruyucu sezaryen gerekir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Genital herpes enfeksiyonunun obstetrik ve neonatal önemi ile ilgili hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Doğum sırasında anneden bebeğe bulaşarak yenidoğanda ölümcül sistemik herpes oluşturabilir",
                            "isCorrect": True,
                            "explanation": "Ders notunun en kritik vurgusudur; intrapartum bulaş neonatal mortaliteye neden olabilir."
                        },
                        {
                            "key": "B",
                            "text": "HSV virüsü doğum kanalındaki mukozadan hiçbir şekilde bebeğe geçemez",
                            "isCorrect": False,
                            "explanation": "Doğum kanalından geçiş sırasında bulaşma en önemli bulaş yoludur."
                        },
                        {
                            "key": "C",
                            "text": "Genital herpes enfeksiyonu yalnızca böbrek taşlarının kalsifikasyonuna neden olur",
                            "isCorrect": False,
                            "explanation": "Böbrek taşıyla ilgisi yoktur; mukokutanöz veziküloülseratif hastalıktır."
                        },
                        {
                            "key": "D",
                            "text": "Yenidoğan döneminde HSV enfeksiyonu tamamen selim olup hiçbir belirti vermez",
                            "isCorrect": False,
                            "explanation": "Tam tersine yenidoğanda karaciğer, akciğer ve beyin tutulumuyla ölümcül seyreder."
                        }
                    ]
                }
            ]
        },
        {
            "slideNumber": 6,
            "title": "Servisitte Klinik Prezentasyon ve Lökore",
            "subtitle": "Akıntı özellikleri, spekulum muayenesi ve servikal frajilite",
            "clinicalFocus": "Klinik Muayene ve Semptomlar",
            "content": "Servisit olgularında klinik tablo tamamen asemptomatik seyirden yoğun pürülan akıntı ve pelvik rahatsızlığa kadar geniş bir spektrum gösterir. Jinekolojik spekulum muayenesi lezyonun doğrudan görselleştirilmesini sağlar.\n\n- **Lökore Tanımı:** Normal vajinal salgıdan renk, koku veya vizkozite olarak farklı, genellikle sarımsı, beyaz veya yeşil tonlarda izlenen akıntıdır.\n- **Servikal Eritem ve Ödem:** Endoservikal os çevresi ödemli ve konjesyoneldir; mukozal yüzey frajil (kırılgan) olup temasla kolayca kanayabilir (kontakt kanama).\n- **Ayırıcı Belirtiler:** Beraberinde üretrit varsa dizüri; üst genital sisteme yayılım varsa derin pelvik ağrı ve disparoni tabloya eklenir.\n\n> [!NOTE]\n> Spekulum muayenesinde servikal os'tan mukopürülan eksüda gelişi ve pamuklu çubukla temas edildiğinde kolay kanama görülmesi servisitin objektif klinik bulgularıdır.",
            "synthesisNarrative": "Servisit olgularında klinik tablo tamamen asemptomatik seyirden yoğun pürülan akıntı ve pelvik rahatsızlığa kadar geniş bir spektrum gösterir. Jinekolojik spekulum muayenesi lezyonun doğrudan görselleştirilmesini sağlar.\n\n- **Lökore Tanımı:** Normal vajinal salgıdan renk, koku veya vizkozite olarak farklı, genellikle sarımsı, beyaz veya yeşil tonlarda izlenen akıntıdır.\n- **Servikal Eritem ve Ödem:** Endoservikal os çevresi ödemli ve konjesyoneldir; mukozal yüzey frajil (kırılgan) olup temasla kolayca kanayabilir (kontakt kanama).\n- **Ayırıcı Belirtiler:** Beraberinde üretrit varsa dizüri; üst genital sisteme yayılım varsa derin pelvik ağrı ve disparoni tabloya eklenir.\n\n> [!NOTE]\n> Spekulum muayenesinde servikal os'tan mukopürülan eksüda gelişi ve pamuklu çubukla temas edildiğinde kolay kanama görülmesi servisitin objektif klinik bulgularıdır.",
            "bulletPoints": [
                "Lökore renk, koku ve kıvamca anormal vajinal akıntıdır.",
                "Spekulumda eritem, ödem ve kolay kanama (frajilite) izlenir.",
                "Asemptomatik olabileceği gibi dizüri ve disparoni eşlik edebilir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Servisitte servikal os çevresindeki mukozanın pamuklu eküvyon temasıyla kolayca kanamasına servikal frajilite adı verilir.",
                    "maskedTerm": "servikal frajilite",
                    "hint": "Enflame mukozanın dokunmayla kanama hassasiyeti"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Servisitte Klinik Spekulum Muayenesi Bulguları",
                    "tableHeaders": ["Muayene Parametresi", "Tipik Bulgu", "Klinik Karşılığı"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Endoservikal Os", "isMasked": False},
                                {"text": "Mukopürülan sarı-yeşil eksüda gelişi", "isMasked": True, "hint": "irinli akıntı drenajı"},
                                {"text": "Aktif endoservikal glandüler inflamasyon"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Mukoza Teması", "isMasked": False},
                                {"text": "Kolay kontakt kanama (frajilite)", "isMasked": False},
                                {"text": "Hiperemik ve incelmiş epitel bariyeri", "isMasked": True, "hint": "kapiller frajilite artışı"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "İnflamasyondan Servikal Frajiliteye",
                    "steps": [
                        "1. Mukozal Vazodilatasyon: İnflamatuvar mediyatörler serviks stromasındaki venül ve kapillerleri genişletir.",
                        "2. Ödem ve Hiperemi: Epitel altı bağ dokusunda lökosit ve seröz sıvı toplanır.",
                        "3. Epitel Frajilitesi: Yüzey hücre bağlantıları zayıflar ve mukozal direnç çöker.",
                        "4. Kontakt Kanama: Spekulum veya sürüntü çubuğunun en hafif mekanik temasında bile kapiller kanama tetiklenir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Klinik terminolojide 'lökore' neyi ifade eder?",
                    "answer": "Normal fizyolojik sekresyondan farklı renk, koku veya vizkozitede, genellikle sarı, beyaz veya yeşilimsi vajinal akıntıyı tanımlar."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Servisitin Muayene Bulguları",
                    "items": [
                        {"text": "Spekulum muayenesinde servikal os'tan pürülan eksüda gelişi görülebilir.", "isLie": False, "explanation": "Doğru. Tipik klinik servisit muayene bulgusudur."},
                        {"text": "İnflame serviks temasla kolay kanayabilen frajil bir yapı sergiler.", "isLie": False, "explanation": "Doğru. Servikal frajilite karakteristik belirtidir."},
                        {"text": "Lökore normalden farklı renk ve kıvamdaki vajinal akıntıyı tanımlar.", "isLie": False, "explanation": "Doğru. Terim tanımı bu şekildedir."},
                        {"text": "Servisit tablosunda serviks her zaman tahta gibi sert kemik dokusuna dönüşür.", "isLie": True, "explanation": "Tuzak! Servisitte kemikleşme olmaz; ödemli, hiperemik ve frajil yumuşak mukoza izlenir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servisitin jinekolojik muayene ve klinik özellikleri ile ilgili hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Endoservikal os'tan mukopürülan akıntı gelişi ve servikal frajilite (kolay kanama) karakteristiktir",
                            "isCorrect": True,
                            "explanation": "Servisitin iki ana fizik muayene bulgusu mukopürülan eksüda ve mukozal frajilitedir."
                        },
                        {
                            "key": "B",
                            "text": "Klinik muayenede serviksin tamamen yok olduğu ve boşluk kaldığı saptanır",
                            "isCorrect": False,
                            "explanation": "Serviks mevcuttur; ödemli, eritemli ve akıntılıdır."
                        },
                        {
                            "key": "C",
                            "text": "Lökore terimi yalnızca saf kanama anlamına gelir, akıntıyı tanımlamaz",
                            "isCorrect": False,
                            "explanation": "Lökore anormal beyaz/sarı/yeşil vajinal akıntıyı tanımlar."
                        },
                        {
                            "key": "D",
                            "text": "Servisitte hastaların hiçbirinde akıntı veya muayene bulgusu olmaz",
                            "isCorrect": False,
                            "explanation": "Olguların çoğunda belirgin akıntı, eritem ve frajilite izlenir."
                        }
                    ]
                }
            ]
        },
        {
            "slideNumber": 7,
            "title": "Servisit Tanısında Laboratuvar: Moleküler Yöntemler ve NAAT",
            "subtitle": "Nükleik asit amplifikasyon testleri, duyarlılık ve patojen tanımlama",
            "clinicalFocus": "Laboratuvar Tanısı",
            "content": "Servisit tanısında klinik muayene şüpheyi doğururken, etken patojenin kesin olarak saptanması hedefe yönelik tedavi için esastır. Geleneksel kültür yöntemleri klamidya gibi zor üreyen mikroorganizmalarda yetersiz kalır.\n\n- **NAAT / PCR Üstünlüğü:** Nükleik Asit Amplifikasyon Testleri (NAAT), servikal veya vajinal sürüntüde patojen DNA/RNA'sını yüksek duyarlılık ve özgüllükle saptar.\n- **Hedef Patojenler:** NAAT panelleri Chlamydia trachomatis, Neisseria gonorrhoeae, Trichomonas vaginalis ve Mycoplasma genitalium'u aynı anda tek örnekte tanımlar.\n- **Kültürün Rolü:** Gonorede antibiyotik direnç profili (antibiyogram) elde etmek gerektiğinde selektif besiyerlerine (Thayer-Martin) kültür ekimi halen değerini korur.\n\n> [!NOTE]\n> Cinsel yolla bulaşan servisit kuşkulu her hastada NAAT ile mikrobiyal tarama yapılması, asemptomatik klamidya ve gonore enfeksiyonlarının yakalanmasında altın standarttır.",
            "synthesisNarrative": "Servisit tanısında klinik muayene şüpheyi doğururken, etken patojenin kesin olarak saptanması hedefe yönelik tedavi için esastır. Geleneksel kültür yöntemleri klamidya gibi zor üreyen mikroorganizmalarda yetersiz kalır.\n\n- **NAAT / PCR Üstünlüğü:** Nükleik Asit Amplifikasyon Testleri (NAAT), servikal veya vajinal sürüntüde patojen DNA/RNA'sını yüksek duyarlılık ve özgüllükle saptar.\n- **Hedef Patojenler:** NAAT panelleri Chlamydia trachomatis, Neisseria gonorrhoeae, Trichomonas vaginalis ve Mycoplasma genitalium'u aynı anda tek örnekte tanımlar.\n- **Kültürün Rolü:** Gonorede antibiyotik direnç profili (antibiyogram) elde etmek gerektiğinde selektif besiyerlerine (Thayer-Martin) kültür ekimi halen değerini korur.\n\n> [!NOTE]\n> Cinsel yolla bulaşan servisit kuşkulu her hastada NAAT ile mikrobiyal tarama yapılması, asemptomatik klamidya ve gonore enfeksiyonlarının yakalanmasında altın standarttır.",
            "bulletPoints": [
                "NAAT patojen DNA/RNA'sını saptayan en duyarlı yöntemdir.",
                "Chlamydia, Gonore ve Trichomonas aynı anda taranabilir.",
                "Hızlı tanı hedefe yönelik antimikrobiyal tedaviyi sağlar."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Servisitte Chlamydia trachomatis ve Neisseria gonorrhoeae patojenlerini kesinleştirmek için nükleik asit amplifikasyon testleri uygulanır.",
                    "maskedTerm": "nükleik asit amplifikasyon testleri",
                    "hint": "NAAT olarak kısaltılan yüksek duyarlılıktaki moleküler tanı yöntemi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Servisit Tanısal Yöntemlerinin Karşılaştırılması",
                    "tableHeaders": ["Tanı Yöntemi", "Duyarlılık / Özgüllük", "Temel Avantajı"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "NAAT / PCR", "isMasked": False},
                                {"text": "Çok yüksek duyarlılık ve özgüllük", "isMasked": True, "hint": "en üst düzey doğruluk"},
                                {"text": "Canlı bakteri gerektirmez, hızlı sonuç verir"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Bakteriyel Kültür", "isMasked": False},
                                {"text": "Klamidyada düşük, gonorede değişken", "isMasked": False},
                                {"text": "Antibiyotik duyarlılık testi olanağı sağlar", "isMasked": True, "hint": "direnç analizi avantajı"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Sürüntüden Moleküler Tanıya",
                    "steps": [
                        "1. Numune Alma: Endoservikal kanaldan pamuklu veya dakron eküvyonla hücresel sürüntü toplanır.",
                        "2. DNA İzolasyonu: Örnekteki hücreler parçalanarak bakteri ve parazit nükleik asitleri açığa çıkarılır.",
                        "3. Enzimatik Çoğaltma: Hedef patojen gen dizilimleri spesifik primerlerle milyonlarca kat amplifiye edilir.",
                        "4. Kesin Tanı: Saptanan floresan sinyal ile sorumlu etken hızla raporlanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Servisit etkeni olan Chlamydia trachomatis ve Neisseria gonorrhoeae tanısında günümüzde en duyarlı kabul edilen tanı yöntemi nedir?",
                    "answer": "Nükleik asit amplifikasyon testleridir (NAAT / PCR)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Servisit Laboratuvar Tanısı",
                    "items": [
                        {"text": "NAAT testleri Chlamydia ve Gonore için en yüksek duyarlılığa sahip tanı yöntemidir.", "isLie": False, "explanation": "Doğru. Moleküler amplifikasyon altın standarttır."},
                        {"text": "Vajinal veya endoservikal sürüntü örneği moleküler inceleme için yeterlidir.", "isLie": False, "explanation": "Doğru. Sürüntü numunesi NAAT için kullanılır."},
                        {"text": "Bakteriyel kültür gonokoklarda antibiyotik duyarlılığını test etme avantajı sağlar.", "isLie": False, "explanation": "Doğru. Direnç tespiti için kültür önemlidir."},
                        {"text": "Servisit tanısı için hastadan mutlaka kemik biyopsisi ve laringoskopi yapılması şarttır.", "isLie": True, "explanation": "Tuzak! Servisit alt genital yol lezyonudur; tanı lokal servikal sürüntü ile konur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servisit olgularında etken mikroorganizmanın doğrulanmasında NAAT yönteminin rolü ile ilgili hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Nükleik asit amplifikasyon testleri Chlamydia ve Neisseria saptamasında yüksek duyarlılığa sahiptir",
                            "isCorrect": True,
                            "explanation": "Moleküler yöntemler zor üreyen genital patojenlerin en güvenilir tanı aracıdır."
                        },
                        {
                            "key": "B",
                            "text": "NAAT sadece alyuvar sayısını ölçen bir idrar dansite testidir",
                            "isCorrect": False,
                            "explanation": "NAAT genetik materyali çoğaltan moleküler biyolojik testtir."
                        },
                        {
                            "key": "C",
                            "text": "Klamidya bakterileri rutin kan yaymasında ışık mikroskobunda dev kitleler olarak görülür",
                            "isCorrect": False,
                            "explanation": "Klamidya zorunlu intraselülerdir, rutin kan yaymasında görünmez."
                        },
                        {
                            "key": "D",
                            "text": "Moleküler testler yalnızca hastanın saç telinden yapılabilen bir dermatolojik yöntemdir",
                            "isCorrect": False,
                            "explanation": "Servikovajinal sürüntü örnekleriyle çalışılır."
                        }
                    ]
                }
            ]
        },
        {
            "slideNumber": 8,
            "title": "Servisit Tedavi Prensipleri ve Ampirik Yaklaşım",
            "subtitle": "Kombine antibiyotik tedavisi, partner yönetimi ve komplikasyon önleme",
            "clinicalFocus": "Tedavi ve Klinik Yönetim",
            "content": "Servisit tedavisinde temel amaç semptomların giderilmesi, asendan üst genital enfeksiyonun (PİH) engellenmesi ve toplumda enfeksiyon zincirinin kırılmasıdır. Laboratuvar sonuçları beklenirken ampirik tedaviye başlanabilir.\n\n- **Ampirik Kapsam:** Tedavi şemaları en sık görülen iki bakteriyel etkeni, yani Chlamydia trachomatis ve Neisseria gonorrhoeae'yi mutlaka eş zamanlı kapsamalıdır.\n- **Tedavi Rejimleri:** Klamidya için doksisiklin veya azitromisin; gonore için seftriakson intramusküler enjeksiyonu standart rejimleri oluşturur.\n- **Eş Tedavisi:** Cinsel partnerin eş zamanlı tedavisi şarttır; aksi takdirde hasta tedavi sonrasında enfekte partnerden tekrar enfeksiyon alır (ping-pong bulaşı).\n\n> [!IMPORTANT]\n> Servisitte etken kesinleşene kadar klamidya ve gonoreyi kapsayan ampirik tedavi başlanmalı ve hasta ile partneri tedavi tamamlanana kadar cinsel ilişkiden kaçınmalıdır.",
            "synthesisNarrative": "Servisit tedavisinde temel amaç semptomların giderilmesi, asendan üst genital enfeksiyonun (PİH) engellenmesi ve toplumda enfeksiyon zincirinin kırılmasıdır. Laboratuvar sonuçları beklenirken ampirik tedaviye başlanabilir.\n\n- **Ampirik Kapsam:** Tedavi şemaları en sık görülen iki bakteriyel etkeni, yani Chlamydia trachomatis ve Neisseria gonorrhoeae'yi mutlaka eş zamanlı kapsamalıdır.\n- **Tedavi Rejimleri:** Klamidya için doksisiklin veya azitromisin; gonore için seftriakson intramusküler enjeksiyonu standart rejimleri oluşturur.\n- **Eş Tedavisi:** Cinsel partnerin eş zamanlı tedavisi şarttır; aksi takdirde hasta tedavi sonrasında enfekte partnerden tekrar enfeksiyon alır (ping-pong bulaşı).\n\n> [!IMPORTANT]\n> Servisitte etken kesinleşene kadar klamidya ve gonoreyi kapsayan ampirik tedavi başlanmalı ve hasta ile partneri tedavi tamamlanana kadar cinsel ilişkiden kaçınmalıdır.",
            "bulletPoints": [
                "Ampirik tedavi Chlamydia ve N. gonorrhoeae'yi kapsamalıdır.",
                "Erken tedavi pelvik inflamatuvar hastalık (PİH) gelişimini önler.",
                "Ping-pong reenfeksiyonunu önlemek için partner tedavisi zorunludur."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Servisit tedavisinde reenfeksiyonu ve ping-pong döngüsünü engellemek için partner tedavisi zorunludur.",
                    "maskedTerm": "partner tedavisi",
                    "hint": "Cinsel eşin eş zamanlı medikal yönetimi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Servisitte Ampirik Tedavi Prensipleri",
                    "tableHeaders": ["Tedavi Unsuru", "Uygulama Amacı", "Klinik Gerekçe"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Kombine Rejim", "isMasked": False},
                                {"text": "Chlamydia ve Gonoreyi eş zamanlı kapsamak", "isMasked": True, "hint": "iki ana bakteriyel etken"},
                                {"text": "Ko-enfeksiyon sıklığı ve PİH riski yüksektir"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Eş Zamanlı Yönetim", "isMasked": False},
                                {"text": "Cinsel partnerin taranması ve tedavisi", "isMasked": False},
                                {"text": "Reenfeksiyon döngüsünü tamamen sonlandırmak", "isMasked": True, "hint": "tekrar bulaşmayı önleme"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Ampirik Tedaviden Şifaya",
                    "steps": [
                        "1. Klinik Tanı: Mukopürülan servisit ve frajilite saptandığında sürüntü alınıp ampirik rejim başlanır.",
                        "2. Patojen Eradikasyonu: Hücre içi klamidya ve diplokok gonore bakterileri antibiyotikle hızla öldürülür.",
                        "3. İnflamasyon Gerilemesi: Doku nötrofil infiltrasyonu azalır ve lökore ortadan kalkar.",
                        "4. Komplikasyon Önleme: Bakterilerin tubalara asendan tırmanışı kesilerek infertilite engellenir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Servisit tedavisinde hastanın iyileşmesinden hemen sonra tekrar enfekte olmasını (ping-pong enfeksiyonu) önlemek için ne yapılmalıdır?",
                    "answer": "Cinsel partnerin de eş zamanlı olarak taranması ve tedavi edilmesi gerekir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Servisit Tedavi Prensipleri",
                    "items": [
                        {"text": "Ampirik antibiyotik rejimi Chlamydia ve N. gonorrhoeae'ye etkili olmalıdır.", "isLie": False, "explanation": "Doğru. İki majör patojen hedeflenir."},
                        {"text": "Eş zamanlı partner tedavisi reenfeksiyonu önlemek için kritik öneme sahiptir.", "isLie": False, "explanation": "Doğru. Partner tedavi edilmezse tekrar bulaşır."},
                        {"text": "Erken tedavi pelvik inflamatuvar hastalık ve tubal infertilite riskini azaltır.", "isLie": False, "explanation": "Doğru. Üst genital yola yayılım engellenir."},
                        {"text": "Servisit tedavisinde tek etkili yöntem hastanın serviksinin tamamen cerrahiyle alınmasıdır.", "isLie": True, "explanation": "Tuzak! Servisit enfeksiyözdür ve medikal antibiyotikle tedavi edilir; histerektomi endikasyonu yoktur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servisitin klinik yönetimi ve antibiyotik tedavisi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Ampirik tedavi Chlamydia ve Gonoreyi kapsamalı, reenfeksiyonu önlemek için partner de tedavi edilmelidir",
                            "isCorrect": True,
                            "explanation": "Bu iki temel ilke hem klinik iyileşmeyi sağlar hem de ping-pong reenfeksiyonunu önler."
                        },
                        {
                            "key": "B",
                            "text": "Hasta tedavi edilirken partnerinin tedavi alması kesinlikle yasaktır",
                            "isCorrect": False,
                            "explanation": "Partner tedavisi reenfeksiyonu önlemek için zorunludur."
                        },
                        {
                            "key": "C",
                            "text": "Servisitte antibiyotik verilmez, sadece hastaya yüksek doz radyoterapi uygulanır",
                            "isCorrect": False,
                            "explanation": "Radyoterapi kanser tedavisidir; servisit antibiyotikle tedavi edilir."
                        },
                        {
                            "key": "D",
                            "text": "Tedavi süresi boyunca cinsel ilişkiye sınırsız devam edilmesi önerilir",
                            "isCorrect": False,
                            "explanation": "Tedavi tamamlanana kadar cinsel ilişkiden kaçınılmalıdır."
                        }
                    ]
                }
            ]
        },
        {
            "slideNumber": 9,
            "title": "Kronik Nonspesifik Servisit ve Skuamöz Metaplazi",
            "subtitle": "Mononükleer infiltrat, Naboth kistleri ve hücresel onarım yanıtı",
            "clinicalFocus": "Kronik İnflamasyon ve Histopatoloji",
            "content": "Kronik servisit, hemen hemen her erişkin kadının serviks biyopsisinde veya histerektomi materyalinde belirli bir derecede izlenen son derece yaygın fizyopatolojik bir durumdur. Çoğunlukla tekrarlayan mikro travmalar ve floranın etkisiyle sürer.\n\n- **Histopatolojik Görünüm:** Subepitelyal stromada lenfositler, plazma hücreleri ve histiyositlerden oluşan mononükleer inflamatuvar infiltrasyon izlenir.\n- **Naboth Kistleri:** İnflamasyon ve skuamöz metaplazi endoservikal glandların boşaltım kanallarını tıkayabilir; içeride biriken mukus bezleri dilate ederek kistik yapılara dönüştürür.\n- **Onarım ve Metaplazi:** Hasar gören kolumnar epitel, vajinal asidik ortama daha dirençli olan çok katlı yassı epitele dönüşür (fizyolojik skuamöz metaplazi).\n\n> [!NOTE]\n> Kronik servisit ve Naboth kistleri tamamen benign fizyopatolojik süreçlerdir; prekanseröz veya malign potansiyel taşımazlar.",
            "synthesisNarrative": "Kronik servisit, hemen hemen her erişkin kadının serviks biyopsisinde veya histerektomi materyalinde belirli bir derecede izlenen son derece yaygın fizyopatolojik bir durumdur. Çoğunlukla tekrarlayan mikro travmalar ve floranın etkisiyle sürer.\n\n- **Histopatolojik Görünüm:** Subepitelyal stromada lenfositler, plazma hücreleri ve histiyositlerden oluşan mononükleer inflamatuvar infiltrasyon izlenir.\n- **Naboth Kistleri:** İnflamasyon ve skuamöz metaplazi endoservikal glandların boşaltım kanallarını tıkayabilir; içeride biriken mukus bezleri dilate ederek kistik yapılara dönüştürür.\n- **Onarım ve Metaplazi:** Hasar gören kolumnar epitel, vajinal asidik ortama daha dirençli olan çok katlı yassı epitele dönüşür (fizyolojik skuamöz metaplazi).\n\n> [!NOTE]\n> Kronik servisit ve Naboth kistleri tamamen benign fizyopatolojik süreçlerdir; prekanseröz veya malign potansiyel taşımazlar.",
            "bulletPoints": [
                "Kronik servisit yetişkin kadınlarda neredeyse evrenseldir.",
                "Stromada lenfosit ve plazma hücre infiltrasyonu görülür.",
                "Gland ağızlarının tıkanması benign Naboth kistlerine yol açar."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Endoservikal bez kanallarının skuamöz metaplazi ile tıkanması sonucu mukusla dolu Naboth kistleri gelişir.",
                    "maskedTerm": "Naboth kistleri",
                    "hint": "Servikste benign retansiyon sonucu oluşan mukus kistleri"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Kronik Servisit Histopatolojik Özellikleri",
                    "tableHeaders": ["Morfolojik Yapı", "Gözlenen Değişiklik", "Patolojik Yorum"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Subepitelyal Stroma", "isMasked": False},
                                {"text": "Lenfosit ve plazma hücresi infiltrasyonu", "isMasked": True, "hint": "kronik mononükleer hücreler"},
                                {"text": "Kronik yangısal yanıtın göstergesidir"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Endoservikal Bezler", "isMasked": False},
                                {"text": "Kanal obstrüksiyonu ve kistik dilatasyon", "isMasked": False},
                                {"text": "Selim Naboth kisti oluşumu ile sonuçlanır", "isMasked": True, "hint": "mukus retansiyon kisti"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Kanal Tıkanıklığından Naboth Kistine",
                    "steps": [
                        "1. İnflamatuvar Uyarı: Kronik irritasyon endoservikal kanal çevresinde skuamöz metaplaziyi uyarır.",
                        "2. Kanal Ağzı Örtülmesi: Yeni oluşan skuamöz epitel kolumnar bez ağızlarını köprü gibi kapatır.",
                        "3. Mukus Birikimi: Derindeki glandüler hücreler salgı üretmeye devam eder ancak salgı dışarı boşalamaz.",
                        "4. Kistik Genişleme: Bez lümeni mukusla dolarak makroskopik Naboth kisti halini alır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Kronik servisitte endoservikal bez kanallarının metaplastik epitel veya inflamasyonla tıkanması sonucu gelişen selim mukus dolu kistlere ne ad verilir?",
                    "answer": "Naboth kistleri (retansiyon kistleri) adı verilir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Kronik Servisit ve Naboth Kistleri",
                    "items": [
                        {"text": "Kronik servisitte stromada lenfosit ve plazma hücresi infiltrasyonu izlenir.", "isLie": False, "explanation": "Doğru. Mononükleer hücreler kronik yangının temel bulgusudur."},
                        {"text": "Naboth kistleri endoservikal bezlerin kanal tıkanıklığı sonucu gelişen selim kistlerdir.", "isLie": False, "explanation": "Doğru. Mukus retansiyonu kiste yol açar."},
                        {"text": "Kronik servisit yetişkin kadın biyopsilerinde oldukça sık rastlanan bir bulgudur.", "isLie": False, "explanation": "Doğru. Patolojide neredeyse fizyolojik kabul edilecek kadar yaygındır."},
                        {"text": "Naboth kistleri %100 oranında öldürücü beyin anevrizmalarına dönüşür.", "isLie": True, "explanation": "Tuzak! Naboth kistleri serviksin tamamen selim kistleridir; beyin anevrizmasıyla hiçbir ilişkisi yoktur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Kronik servisit ve ilişkili histopatolojik değişiklikler hakkında hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Stromada lenfosit/plazma hücresi infiltrasyonu izlenir ve bez kanallarının tıkanmasıyla benign Naboth kistleri oluşur",
                            "isCorrect": True,
                            "explanation": "Kronik servisitin klasik mikroskobisi mononükleer hücre infiltratı ve retansiyon kistleridir."
                        },
                        {
                            "key": "B",
                            "text": "Naboth kistleri görüldüğü anda hastaya acil kemoterapi başlanmalıdır",
                            "isCorrect": False,
                            "explanation": "Naboth kistleri tamamen selimdir, tedavi gerektirmez."
                        },
                        {
                            "key": "C",
                            "text": "Kronik servisit sadece 5 yaş altı erkek çocuklarda görülen bir hastalıktır",
                            "isCorrect": False,
                            "explanation": "Servisit kadın genital sistemine aittir."
                        },
                        {
                            "key": "D",
                            "text": "Kronik servisitte stromada hiçbir iltihabi hücre görülmez",
                            "isCorrect": False,
                            "explanation": "Lenfositler ve plazma hücreleri belirgin olarak izlenir."
                        }
                    ]
                }
            ]
        },
        {
            "slideNumber": 10,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Servisit ve Servikal Mikrobiyota",
            "subtitle": "Klinik lökore, flora dengesi, Chlamydia ve HSV neonatal riski sentezi",
            "clinicalFocus": "Bölüm Tekrarı ve Pekiştirme",
            "content": "Bu tekrar sayfasında Bölüm 1 boyunca ele aldığımız servisit kavramını, etyolojik ajanları ve klinik yönetim ilkelerini pekiştiriyoruz.\n\n- **Lökore ve Flora:** Servisitte en sık başvuru yakınması mukopürülan lökoredir; ektoserviks zengin bir kommensal floraya sahiptir.\n- **Patojen Lideri:** Cinsel yolla bulaşan servisit olgularında en yaygın etken Chlamydia trachomatis'tir (%40) ve olgular sıklıkla asemptomatiktir.\n- **Viral Tehdit:** Herpes Simplex Virus tip 2 doğum kanalından bebeğe bulaştığında yenidoğanda fatal sistemik herpes riski oluşturur.\n- **Klinik ve Tedavi:** Spekulumda servikal frajilite ve mukopürülan eksüda saptanır; tanı NAAT ile konur ve ampirik rejimde klamidya + gonore hedeflenerek partnerle birlikte tedavi edilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Servisit cinsel yolla bulaşan enfeksiyonların en sık lokalizasyonudur; en yaygın bakteriyel etken Chlamydia trachomatis (%40), en tehlikeli neonatal tehdit maternal HSV bulaşıdır.",
            "synthesisNarrative": "Bu tekrar sayfasında Bölüm 1 boyunca ele aldığımız servisit kavramını, etyolojik ajanları ve klinik yönetim ilkelerini pekiştiriyoruz.\n\n- **Lökore ve Flora:** Servisitte en sık başvuru yakınması mukopürülan lökoredir; ektoserviks zengin bir kommensal floraya sahiptir.\n- **Patojen Lideri:** Cinsel yolla bulaşan servisit olgularında en yaygın etken Chlamydia trachomatis'tir (%40) ve olgular sıklıkla asemptomatiktir.\n- **Viral Tehdit:** Herpes Simplex Virus tip 2 doğum kanalından bebeğe bulaştığında yenidoğanda fatal sistemik herpes riski oluşturur.\n- **Klinik ve Tedavi:** Spekulumda servikal frajilite ve mukopürülan eksüda saptanır; tanı NAAT ile konur ve ampirik rejimde klamidya + gonore hedeflenerek partnerle birlikte tedavi edilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Servisit cinsel yolla bulaşan enfeksiyonların en sık lokalizasyonudur; en yaygın bakteriyel etken Chlamydia trachomatis (%40), en tehlikeli neonatal tehdit maternal HSV bulaşıdır.",
            "bulletPoints": [
                "Lökore en sık başvuru yakınmasıdır.",
                "Chlamydia en yaygın etkendir (%40).",
                "Maternal HSV yenidoğanda ölümcül sistemik herpes yapabilir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "CYBH kliniklerinde servisit vakalarının yaklaşık yüzde kırkından Chlamydia trachomatis bakterisi sorumludur.",
                    "maskedTerm": "Chlamydia trachomatis",
                    "hint": "En yaygın bakteriyel servisit patojeni"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Bölüm 1 Klinik Karşılaştırma Matrisi",
                    "tableHeaders": ["Klinik Başlık", "Temel Mekanizma / Etken", "Kritik Klinik Nokta"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Bakteriyel Servisit", "isMasked": False},
                                {"text": "Chlamydia trachomatis (%40) ve Gonore", "isMasked": True, "hint": "majör bakteriyel etkenler"},
                                {"text": "Ampirik kombine tedavi ve partner yönetimi gerekir"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Viral Servisit (HSV-2)", "isMasked": False},
                                {"text": "Ağrılı veziküloülseratif lezyonlar", "isMasked": False},
                                {"text": "Yenidoğanda ölümcül sistemik enfeksiyon riski taşır", "isMasked": True, "hint": "neonatal ölümcül tablo"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Bölüm 1 Sentez Zinciri",
                    "steps": [
                        "1. Patojen İnokülasyonu: Chlamydia veya Gonore mikroorganizmaları endoservikal kolumnar hücrelere yerleşir.",
                        "2. Mukopürülan Yanıt: Nötrofilik infiltrasyon lökore ve servikal frajilite tablosunu oluşturur.",
                        "3. Moleküler Doğrulama: NAAT paneli ile sorumlu genetik materyal yüksek hassasiyetle belirlenir.",
                        "4. Küratif Eradikasyon: Eş zamanlı partner tedavisi uygulanarak asendan komplikasyonlar önlenir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bölüm 1'de öğrenilen iki kritik spot: Servisitin en sık bakteriyel etkeni nedir ve gebede aktif HSV lezyonunun en korkulan riski nedir?",
                    "answer": "En sık etken Chlamydia trachomatis'tir (%40); aktif genital HSV'nin en korkulan riski ise doğumda bebeğe geçerek ölümcül neonatal sistemik herpes yapmasıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Checkpoint 1 Sentez Bilgileri",
                    "items": [
                        {"text": "Servisit olgularında en sık başvuru semptomu lökoredir.", "isLie": False, "explanation": "Doğru. Akıntı kardinal belirtidir."},
                        {"text": "Chlamydia trachomatis CYBH kliniklerinde servisit vakalarının yaklaşık %40'ından sorumludur.", "isLie": False, "explanation": "Doğru. Amfi notunun kilit verisidir."},
                        {"text": "Doğum kanalındaki maternal HSV-2 yenidoğanda fatal sistemik enfeksiyona yol açabilir.", "isLie": False, "explanation": "Doğru. Sezaryen endikasyonudur."},
                        {"text": "Chlamydia servisiti daima tek doz aspirinle 10 dakikada tamamen iyileşir.", "isLie": True, "explanation": "Tuzak! Chlamydia bakteriyel enfeksiyondur; uygun antibiyotik (doksisiklin/azitromisin) gerektirir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Bölüm 1'de incelenen servisit patolojisi ve etkenleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Chlamydia trachomatis en yaygın etkendir ve maternal aktif HSV yenidoğanda fatal sistemik herpes yapabilir",
                            "isCorrect": True,
                            "explanation": "Bu iki spot Bölüm 1'in en yüksek verimli sınav bilgilerini eksiksiz özetler."
                        },
                        {
                            "key": "B",
                            "text": "Servisit hastalarında vajinal akıntı görülmesi imkansız bir tıbbi anomalidir",
                            "isCorrect": False,
                            "explanation": "Lökore servisitin en sık karşılaşılan klinik başvuru semptomudur."
                        },
                        {
                            "key": "C",
                            "text": "Normal vajinal mikrobiyotada hiçbir zaman bakteri ya da maya bulunmaz",
                            "isCorrect": False,
                            "explanation": "Vajina laktobasiller, enterokoklar, streptokoklar ve kandida içeren zengin bir floraya sahiptir."
                        },
                        {
                            "key": "D",
                            "text": "Servisitin kesin tanısı için daima açık beyin biyopsisi yapılması şarttır",
                            "isCorrect": False,
                            "explanation": "Tanı lokal servikovajinal sürüntüde NAAT testleri ile konur."
                        }
                    ]
                }
            ]
        }
    ]

print("Section 1 data defined.")
