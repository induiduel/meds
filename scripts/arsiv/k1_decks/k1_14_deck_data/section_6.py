# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_6_slides():
    slides = []

    # Slide 51
    slides.append({
        "id": "k1-14-s51",
        "title": "21. Yüzyılda İletişim Krizi ve Değişen Toplum Dinamikleri",
        "content": "21. yüzyılda halk sağlığı uzmanlarının karşılaştığı en çetin engel biyolojik patojenlerden ziyade değişen toplumsal iletişim dinamikleridir:\n\n- **Buyurgan Dilin İflası (Sınav Spotu):** Geçmiş yüzyıllarda devletin veya hekimin tek taraflı 'şunu yapın, bunu yapmayın' şeklindeki tepeden inme, buyurgan dili artık toplumlar tarafından benimsenmemektedir.\n- **Uzman Görüşüne Azalan Güven:** Bilgiye erişimin demokratikleşmesiyle birlikte sahte uzmanlar türemiş, bilimsel otoriteye ve kurumlara duyulan geleneksel güven aşınmıştır.\n- **İnternet ve Sosyal Medya Kaynağı:** İnsanlar sağlık bilgilerini artık hekimlerinden önce sosyal medyadan, arama motorlarından ve kapalı mesajlaşma gruplarından almaktadır.\n- **Hızlı İnfial:** Yanlış veya provokatif bir haber saniyeler içinde viral hale gelerek kitlesel paniğe veya sağlık personeline saldırılara yol açabilmektedir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "20. Yüzyıl Klasik İletişim vs 21. Yüzyıl Dijital İletişim Gerçeği",
                "20. Yüzyıl (Tepeden İnme İletişim)",
                "Tek taraflı resmi bildiriler, radyodan kamu spotları, uzman otoritesinin sorgulanmadan kabul edilmesi.",
                "21. Yüzyıl (Çift Yönlü ve Dağınık İletişim)",
                "Sosyal medya algoritmaları, buyurgan dilin reddi, uzman görüşüne şüphe ve anlık infial riski."
            ),
            make_cloze(
                "21. yüzyılda halk sağlığı yönetiminde tek taraflı buyurgan dil benimsenmemekte, uzman görüşüne güven azalmaktadır.",
                "buyurgan",
                "Toplumun artık kabul etmediği otoriter iletişim üslubu"
            )
        ]
    })

    # Slide 52
    slides.append({
        "id": "k1-14-s52",
        "title": "İnfodemi: Tanımı, Yayılım Hızı ve Halk Sağlığı Tehdidi",
        "content": "Salgın dönemlerinde yalnızca virüsler değil, bilgi kirliliği de epidemik bir hızla yayılır:\n\n- **İnfodemi Tanımı (Sınav Spotu):** Bir salgın (epidemi veya pandemi) sırasında, patojenle birlikte veya patojenden daha hızlı bir şekilde **yanlış, gereksiz, kanıtsız ve panik yaratacak kadar abartılı bilgilerin** toplumda kontrolsüzce yayılması durumudur.\n- **İki Uçlu Tehlike:**\n  1. **Yanlış Tedavi Çılgınlığı:** Çamaşır suyu içmek, yüksek doz parazit ilaçları kullanmak gibi ölümcül sahte kürlerin yayılması.\n  2. **Önlemleri Reddetme:** Aşının kısırlık yaptığı, maskenin oksijensiz bıraktığı veya virüsün bir komplo olduğu yalanlarıyla korunma tedbirlerinin boykot edilmesi.\n- **Sonuç:** İnfodemi, patojenden daha fazla insanın hastalanmasına ve ölümüne neden olabilen ölümcül bir bilgi pandemisidir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "Salgın sırasında patojenle birlikte yanlış, gereksiz ve panik yaratacak kadar abartılı bilgilerin kontrolsüz yayılmasına ne ad verilir?",
                [
                    {"key": "A", "text": "İnfodemi", "isCorrect": True, "explanation": "Doğru cevap A'dır: İnfodemi (information + epidemic), salgın dönemlerindeki kontrolsüz bilgi kirliliğini ve dezenformasyonu tanımlayan standart halk sağlığı terimidir."},
                    {"key": "B", "text": "Biyoterörizm", "isCorrect": False, "explanation": "Biyoterörizm biyolojik silahların kasıtlı kullanımıdır."},
                    {"key": "C", "text": "Sürveyans fazı", "isCorrect": False, "explanation": "Sürveyans sistematik veri toplama sürecidir."},
                    {"key": "D", "text": "Amplifikasyon dönemi", "isCorrect": False, "explanation": "Amplifikasyon patojenin vakaları hızla artırma evresidir."}
                ]
            ),
            make_recall(
                "İnfodemi halk sağlığı önlemlerini neden doğrudan baltalar?",
                "Çünkü infodemi halkta panik, komplo teorilerine inanç ve sağlık kurumlarına güvensizlik yaratarak aşı, maske ve izolasyon gibi hayat kurtarıcı tedbirlerin reddedilmesine yol açar."
            )
        ]
    })

    # Slide 53
    slides.append({
        "id": "k1-14-s53",
        "title": "İnfodemiyle Mücadelede Üç Kutsal İlke: Konuş, Dinle, Dedikoduyu Engelle",
        "content": "DSÖ ve halk sağlığı otoriteleri, infodeminin yıkıcı etkilerini durdurabilmek için üç aşamalı temel bir iletişim formülü belirlemiştir (Sınav Spotu):\n\n- **1. Konuş (Şeffaf ve Proaktif Bilgilendirme):** Bilgi boşluğu bırakılamaz. Resmi kanallar doğru, anlaşılır, dürüst ve kanıta dayalı bilgiyi ilk andan itibaren sürekli paylaşmalıdır.\n- **2. Dinle (Sosyal Dinleme / Social Listening):** Toplumun kaygıları, korkuları, inançları ve soruları analiz edilmelidir. İnsanların ne hissettiğini bilmeden verilen cevaplar havada kalır.\n- **3. Dedikoduları Engelle (Rumour Tracking & Fact-checking):** Sahada ve dijital mecralarda üretilen şehir efsaneleri ve sahte haberler anında tespit edilmeli; bilimsel kanıtlarla hızla ve alay etmeden çürütülmelidir.\n- **Kritik Kural:** Halkı azarlamak değil, güven inşa ederek dedikodunun önünü kesmek esastır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "İnfodemi Yönetim Döngüsü",
                [
                    "1. Sosyal Dinleme: Sosyal medya ve çağrı merkezleri taranarak hangi dedikoduların yayıldığı saptanır.",
                    "2. Doğrulama ve Yanıt Hazırlığı: Bilim kurulu dedikoduyu çürüten sade ve görsel materyaller hazırlar.",
                    "3. Çok Kanallı Konuşma: Etkili kanaat önderleri ve hekimler aracılığıyla doğru bilgi kitlelere ulaştırılır.",
                    "4. Dedikoduyu Engelleme: Sahte iddialar yayılmadan önce 'ön-çürütme' (pre-bunking) ile toplum aşılanır."
                ]
            ),
            make_cloze(
                "İnfodemiyi önlemenin ve yönetmenin üç temel kuralı konuşma, dinleme ve dedikoduları engellemedir.",
                "engelleme",
                "Yalan ve asılsız haberlerin yayılmasını durdurma eylemi"
            )
        ]
    })

    # Slide 54
    slides.append({
        "id": "k1-14-s54",
        "title": "Güven İnşası: Dinlemek Anlatmak Kadar Önemlidir",
        "content": "Risk iletişiminde en sık yapılan ölümcül hata, toplumun sadece 'bilgilendirilmesi gereken pasif bir alıcı' olarak görülmesidir:\n\n- **Önce Güven Tesis Edilmeli (Sınav Spotu):** Bilimsel gerçekleri veya uzman tavsiyelerini iletebilmenin ön koşulu, hedef kitlenin size güvenmesidir. Güven yoksa dünyanın en mükemmel ilacı da gelse halk onu kullanmayı reddeder.\n- **Dinlemenin Gücü:** İnsanların inançlarını, korkularını, algılarını ve kaygılarını dinlemek; onlara gerçekleri anlatmak kadar, hatta bazen daha önemlidir.\n- **Empati ve Alçakgönüllülük:** 'Biz tıp profesörüyüz, siz bilmezsiniz' kibri halkı bilimden uzaklaştırır ve şarlatanların kucağına iter. Bilim insanları belirsizlikleri dürüstçe kabul etmeli ve halkın endişelerine saygıyla yaklaşmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["İletişim Yaklaşımı", "Davranış Kalıbı", "Toplumsal Sonuç"],
                [
                    ["Kibirli ve Buyurgan", "Halkı cahillikle suçlama, zorlayıcı emirler, soru sormayı yasaklama", "Öfke, direnç, aşı karşıtlığı ve sağlıkçıya şiddet"],
                    ["Güven Temelli ve Katılımcı", "Kaygıları sabırla dinleme, şeffaf açıklama, yerel liderlerle iş birliği", "Yüksek uyum, filyasyona destek ve toplumsal sahiplenme"]
                ]
            ),
            make_quiz(
                "21. yüzyılda uzman görüşünü topluma başarıyla aktarabilmenin temel ön koşulu aşağıdakilerden hangisidir?",
                [
                    {"key": "A", "text": "Sosyal medyayı tamamen kapatıp tek televizyon kanalından yayın yapmak", "isCorrect": False, "explanation": "Sansür güveni yok eder ve dedikoduları daha da körükler."},
                    {"key": "B", "text": "Halka tıbbi tavsiyeleri iletmeden önce güven tesis etmek ve toplumun kaygılarını dinlemek", "isCorrect": True, "explanation": "Doğru cevap B'dir: Ders notunda açıkça vurgulandığı üzere, tavsiye vermeden önce güven tesis edilmeli; kaygıları dinlemek gerçekleri anlatmak kadar önemlidir."},
                    {"key": "C", "text": "Yalnızca Latince tıp terimleri kullanarak otoriter görünmek", "isCorrect": False, "explanation": "Karmaşık Latince dil iletişimi imkansız kılar."},
                    {"key": "D", "text": "Salgınla ilgili tüm verileri gizli tutmak", "isCorrect": False, "explanation": "Veri gizleme güveni tamamen bitirir."}
                ]
            )
        ]
    })

    # Slide 55
    slides.append({
        "id": "k1-14-s55",
        "title": "Toplumsal Bazda Düşünmek: Homojen Değil Heterojen Toplum",
        "content": "Salgın yönetiminde yapılan en büyük planlama hatalarından biri, bir ülkedeki veya şehirdeki tüm insanları tek tip (monolitik/homojen) kabul etmektir:\n\n- **Toplumlar Yekpare Değildir (Sınav Spotu):** Bir toplum homojen bir kitle değildir; etnik köken, din, dil, sosyoekonomik gelişmişlik düzeyi ve kültürel inançlar açısından derin farklılıklar barındırır.\n- **Risk Algısının Değişkenliği:** Zengin bir plazada yaşayan bir birey ile gecekondu mahallesinde günlük yevmiye ile çalışan veya mülteci kampında yaşayan birinin risk algısı ve salgın tedbirlerine uyabilme kapasitesi tamamen farklıdır.\n- **'Evde Kal' Çelişkisi:** 'Evde kalın' çağrısı, günlük çalışmak zorunda olan veya evi olmayan biri için uygulanabilir değildir; sosyal ve ekonomik destek sağlanmadan bu kitleye izolasyon dayatılamaz.\n- **Kültürel İnançlar:** Cenaze ritüelleri, bayramlaşma gelenekleri ve el sıkışma alışkanlıkları bulaşta kritik rol oynar; bu geleneklere saygılı alternatifler üretilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Monolitik Yaklaşım vs Toplumsal Tabanlı Yaklaşım",
                "Monolitik Yaklaşım (Hatalı)",
                "Tüm topluma aynı kalıp mesajı verir; sosyoekonomik güçlükleri ve kültürel inanç farklılıklarını görmezden gelir.",
                "Toplumsal Tabanlı Yaklaşım (Doğru)",
                "Farklı etnik, dini ve ekonomik grupların ihtiyaçlarını ve yerel liderlerini dikkate alarak özelleştirilmiş strateji kurar."
            ),
            make_cloze(
                "İnsan toplulukları yekpare değildir; risk algısı sosyoekonomik gelişmişlik, din, kültürel inançlar ve dil farklılıklarına göre değişir.",
                "yekpare",
                "Toplumların homojen olmadığını ifade eden kelime"
            )
        ]
    })

    # Slide 56
    slides.append({
        "id": "k1-14-s56",
        "title": "Eğitilmiş ve Hazırlıklı Toplumun Gücü",
        "content": "Salgınla mücadelenin en güçlü ve en ucuz kalkanı, sağlık okuryazarlığı yüksek ve salgınlara hazırlanmış bir halktır:\n\n- **Bağımsız Erken Teşhis Yeteneği (Sınav Spotu):** İyi eğitimli, bilinçli ve hazırlıklı bir toplum, olağan dışı bir hastalık kümelenmesini veya salgın belirtilerini **daha uzman desteği sahaya ulaşmadan bile fark edebilir**.\n- **Hızlı Öz-Önlem:** Böyle bir toplumda bireyler, semptom hissettiğinde kendiliğinden maske takar, işe veya okula gitmez, yaşlı aile bireylerini korumaya alır ve sağlık birimini uyarır.\n- **Müdahalelerin Etkin Uygulanması:** Devlet bir tedbir açıkladığında (örneğin aşılama veya temaslı bildirimi), bilinçli toplum bu tedbire polis zoruyla değil, kendi sorumluluğu olarak gönüllü katılır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "İyi eğitimli ve hazırlıklı bir toplumun salgın yönetimindeki en belirgin avantajı aşağıdakilerden hangisidir?",
                [
                    {"key": "A", "text": "Hastalık belirtilerini uzman desteği olmadan bile erkenden fark edebilmek ve tedbirleri etkin uygulamak", "isCorrect": True, "explanation": "Doğru cevap A'dır: Ders notunda belirtildiği gibi, iyi eğitimli bir toplum salgınları uzman desteği gelmeden dahi fark edebilir ve müdahalelerin sahada hızla benimsenmesini sağlar."},
                    {"key": "B", "text": "Hastanelere hiç gitmeyip tüm ameliyatları evde kendi kendine yapmak", "isCorrect": False, "explanation": "Cerrahi ve ileri tıp evde yapılamaz."},
                    {"key": "C", "text": "Aşı ve ilaç üretimini tamamen durdurmak", "isCorrect": False, "explanation": "Aşı üretimi toplumun eğitimiyle durdurulmaz, bilakis teşvik edilir."},
                    {"key": "D", "text": "Salgın boyunca hiçbir kamu yetkilisiyle konuşmamak", "isCorrect": False, "explanation": "İletişimsizlik salgını felakete sürükler."}
                ]
            ),
            make_recall(
                "Sağlık okuryazarlığı düşük toplumlarda salgın yönetimi neden çok daha yüksek maliyetli ve ölümlüdür?",
                "Çünkü geç başvuru, gizlenen temaslılar, aşı reddi ve infodemi nedeniyle filyasyon çürür; hastalar ancak yoğun bakım aşamasında sağlık sistemine ulaşır."
            )
        ]
    })

    # Slide 57
    slides.append({
        "id": "k1-14-s57",
        "title": "Stigmatizasyon ve Hastalıktan Kurtulanların Topluma Kaynaştırılması",
        "content": "Salgın dönemlerinde toplumda korkuyla birlikte ortaya çıkan en tehlikeli sosyo-psikolojik olgu **damgalama (stigmatizasyon)** ve dışlamadır:\n\n- **Damgalama Tehdidi:** Hastalığa yakalanan bireyler, aileleri ve hatta onları tedavi eden hekim ve hemşireler toplum tarafından 'vebalı' muamelesi görebilir; evlerinden atılabilir veya hakarete uğrayabilir.\n- **Filyasyonun Çöküşü:** Damgalanmaktan korkan insanlar semptomlarını gizler, test yaptırmaktan kaçar ve temaslılarını bildirmez. Bu durum salgının yer altında kontrolsüz büyümesine yol açar.\n- **Kurtulanları Topluma Kaynaştırma (Sınav Spotu):** Salgından iyileşip hayatta kalanların (survivors) dışlanmasını önlemek, onları birer kahraman ve toplum elçisi olarak yeniden topluma entegre etmek halk sağlığının temel görevidir.\n- **İyileşenlerin Rolü:** İyileşen kişiler plazma bağışçısı olabilir, sahada filyasyon ve temaslı ikna ekiplerine gönüllü rehberlik edebilir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_branching(
                "Toplumsal Yönetim: İyileşen Hastalara Karşı Ayrımcılık",
                "Bir köyde COVID-19 veya Kırım-Kongo geçirip hastaneden taburcu olan bir aile, köylüler tarafından taşlanarak köyden kovulmak isteniyor. Köy hekimi ve filyasyon ekibi lideri olarak nasıl davranırsınız?",
                [
                    {
                        "text": "Olaylara karışmayıp jandarmadan aileyi başka bir kente nakletmesini istemek",
                        "outcome": "Hatalı yaklaşım: Bu davranış damgalamayı meşrulaştırır ve diğer köylülerin hastalık belirtilerini gizlemesine yol açar.",
                        "isCorrect": False
                    },
                    {
                        "text": "Köy meydanında muhtar ve imamla birlikte toplantı yaparak ailenin artık bulaştırıcı olmadığını açıklamak ve aileyi desteklemek",
                        "outcome": "Mükemmel halk sağlığı liderliği: Güven inşa edilir, stigmatizasyon kırılır ve hastalıktan kurtulanlar güvenle topluma yeniden kaynaştırılır.",
                        "isCorrect": True
                    },
                    {
                        "text": "Köylüleri televizyona çıkarıp tüm Türkiye'ye rezil etmekle tehdit etmek",
                        "outcome": "Yıkıcı yaklaşım: Çatışmayı körükler ve sağlık personeline karşı şiddet başlatır.",
                        "isCorrect": False
                    }
                ]
            ),
            make_cloze(
                "Salgın yönetiminde damgalamayı önlemek ve hastalıktan kurtulanları topluma kaynaştırmak sürdürülebilir filyasyon için şarttır.",
                "kaynaştırmak",
                "İyileşen kişilerin yeniden topluma kabul edilmesi süreci"
            )
        ]
    })

    # Slide 58
    slides.append({
        "id": "k1-14-s58",
        "title": "Sosyal Medya, Doğrulama Platformları ve Proaktif İletişim",
        "content": "Dijital çağda risk iletişiminin sahnesi hastane koridorlarından sosyal medya platformlarına kaymıştır:\n\n- **Dedikoduyu Anında Tespit:** WhatsApp gruplarında yayılan 'aşı kısırlık yapıyor' veya 'hastanelerde hastalar bilerek öldürülüyor' iddiaları anlık takip edilmelidir.\n- **Proaktif ve Sade Görseller:** 50 sayfalık resmi tıp genelgelerini halk okumaz. Bunun yerine TikTok, Instagram ve YouTube için 30 saniyelik net, sempatik, hekim anlatımlı videolar ve infografikler üretilmelidir.\n- **Doğrulama (Fact-checking) Ağları:** Teyit platformları ile iş birliği yapılarak sahte görseller ve montaj videolar ifşa edilmelidir.\n- **Yerel Dinamikler ve Kanaat Önderleri:** Halkın güvendiği yerel din adamları, sporcular, sanatçılar ve mahalle muhtarları iletişime dahil edilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["İletişim Kanalı", "Avantajı", "Risk ve Yönetim Stratejisi"],
                [
                    ["Resmi Basın Bülteni", "Hukuki ve resmi netlik sağlar", "Çok resmi ve sıkıcı olabilir; sadeleştirilmelidir"],
                    ["Kısa Video / Sosyal Medya", "Milyonlarca gence dakikalar içinde ulaşır", "Algoritmalar sansasyonel yalanları öne çıkarabilir; proaktif olunmalı"],
                    ["Muhtarlar ve Kanaat Önderleri", "Derin yerel güven ve yüz yüze ikna sağlar", "Önce liderlerin kendileri eğitilmeli ve ikna edilmelidir"]
                ]
            ),
            make_quiz(
                "Salgın iletişiminde sosyal medya ve internet ortamındaki infodemiye karşı en etkili strateji hangisidir?",
                [
                    {"key": "A", "text": "Hekimlerin sosyal medyaya girişini yasaklamak", "isCorrect": False, "explanation": "Hekimlerin sesini kısmak alanı şarlatanlara terk etmek demektir."},
                    {"key": "B", "text": "Doğru, sade ve görsel içeriklerle proaktif olarak bilgi boşluklarını doldurmak ve dedikoduları hızla çürütmek", "isCorrect": True, "explanation": "Doğru cevap B'dir: Bilgi boşluğu bırakmamak ve görsel/anlaşılır kanıtlarla yalanı anında çürütmek infodemiyi durdurmanın anahtarıdır."},
                    {"key": "C", "text": "Sadece Latince akademik makaleler yayınlayarak halkı görmezden gelmek", "isCorrect": False, "explanation": "Akademik makaleleri sokaktaki insan anlayamaz."},
                    {"key": "D", "text": "Hiçbir dedikoduya cevap vermeyip suskun kalmak", "isCorrect": False, "explanation": "Suskunluk toplum nezdinde suçluluk veya çaresizlik olarak algılanır."}
                ]
            )
        ]
    })

    # Slide 59 - CHECKPOINT 6
    slides.append({
        "id": "k1-14-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Risk İletişimi, İnfodemi Yönetimi ve Toplumsal Dinamikler",
        "content": "Bu checkpointte salgının sosyolojik boyutunu, iletişim engellerini ve infodemi yönetimini özetliyoruz:\n\n- **21. Yüzyıl İletişim Krizi:** Buyurgan dil kabul görmez, uzman görüşüne güven azalmıştır; bilgi internet ve sosyal medyadan alınmaktadır.\n- **Önce Güven Tesis Edilmeli:** Dinlemek, insanlara gerçekleri ve tavsiyeleri anlatmak kadar önemlidir.\n- **İnfodemi:** Patojenle birlikte yayılan abartılı, yanlış ve panik yaratan bilgi salgınıdır.\n- **Üç Mücadele Kuralı:** Konuş, dinle ve dedikoduları engelle.\n- **Toplum Yekpare Değildir:** Din, kültür, dil ve sosyoekonomik farklılıklar risk algısını ve uyumu belirler.\n- **Eğitilmiş Toplum:** Uzman desteği olmadan dahi salgını fark edebilir ve tedbirleri sahiplenir.\n- **Stigmatizasyon:** Damgalamayla mücadele edilmeli, hastalıktan kurtulanlar topluma kaynaştırılmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "Başarılı Risk İletişiminin 4 Aşaması",
                [
                    "1. Güven İnşası: Alçakgönüllü ve empati kuran bir dille toplumun korku ve kaygıları dinlenir.",
                    "2. İnfodemi Tespiti: Sahada yayılan dedikodular ve sosyal medya yalanları anında taranır.",
                    "3. Şeffaf ve Sade Konuşma: Kanıta dayalı gerçekler anlaşılır görseller ve yerel liderlerle aktarılır.",
                    "4. Toplumsal Kaynaşma: Hastalar damgalanmaktan korunur, iyileşenler sürece dahil edilir."
                ]
            ),
            make_slider(
                "İnfodemi Yönetiminin İki Yüzü",
                "Sosyal Dinleme ve Empati (Giriş)",
                "Toplumun kaygılarını dinleyerek sahte dedikoduların kaynağını anlamak.",
                "Dedikoduyu Engelleme ve Eylem (Sonuç)",
                "Proaktif ve sade içeriklerle yanlış bilgiyi çürüterek kitlesel paniği önlemek."
            )
        ]
    })

    # Slide 60
    slides.append({
        "id": "k1-14-s60",
        "title": "Mini Vaka: Aşı Karşıtlığı ve WhatsApp İnfodemisiyle Mücadele",
        "content": "Kızamık salgınının baş gösterdiği bir ilçede, anneler arasında 'Kızamık aşısı otizm yapıyor ve kısırlık bırakıyor' şeklinde sahte bir ses kaydı WhatsApp gruplarında hızla yayılıyor. Aşı ret oranı bir haftada %8'den %45'e fırlıyor:\n\n- **İlçe Sağlık Müdürü Eylemi:**\n  1. **Dinleme:** Anne gruplarıyla aile sağlığı merkezlerinde çay sohbetleri düzenlenerek korkuları sabırla dinleniyor.\n  2. **Kanaat Önderleri:** İlçenin sevilen kadın doğum uzmanı ve yerel din görevlisi çocuklarını kameralar önünde aşılatıyor.\n  3. **Dedikoduyu Engelleme:** Otizm iddiasının 1998'de tıp literatüründen sahtekarlık nedeniyle atılan Andrew Wakefield makalesine dayandığı, milyonlarca çocukta yapılan güncel çalışmalarla kesinlikle çürütüldüğü broşürlerle açıklanıyor.\n- **Sonuç:** Buyurgan bir dille ceza kesmek yerine güven tesis edilerek aşılanma oranı %92'ye çıkarılıyor ve kızamık salgını sınırlanıyor.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_branching(
                "Klinik Karar: Aşı Reddi Yapan Anneyle İletişim",
                "Polikliniğe gelen bir anne, 'WhatsApp'ta okudum, bu aşı çocuğumun beynini yakıyormuş, aşıyı yaptırmayacağım' diyerek bebeğini kucağına alıyor. En doğru hekim yaklaşımı hangisidir?",
                [
                    {
                        "text": "'Siz tıptan ne anlarsınız, aşı yaptırmazsanız sizi savcılığa şikayet ederim' diye azarlamak",
                        "outcome": "Felaket yaklaşımı: Anne tamamen yabancılaşır, kaçar ve aşı karşıtı grupların kucağına düşer.",
                        "isCorrect": False
                    },
                    {
                        "text": "Anneyi sakin bir odaya davet edip bebeği için duyduğu koruma içgüdüsünü anladığını belirterek kaygılarını dinlemek, aşının güvenlik testlerini ve kızamığın beyin hasarı riskini şefkatle açıklamak",
                        "outcome": "Mükemmel risk iletişimi: Güven tesis edilir, annenin haklı endişesi giderilir ve bebek güvenle aşılanır.",
                        "isCorrect": True
                    },
                    {
                        "text": "'Haklı olabilirsiniz hanımefendi, ben de pek güvenmiyorum' demek",
                        "outcome": "Mesleki kusur: Hekim bilime aykırı konuşarak bebeğin hayatını tehlikeye atar.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu vakada İlçe Sağlık Müdürlüğü'nün cezai yaptırım yerine annelerin kaygılarını dinleyip yerel liderlerle birlikte hareket etmesi hangi ilkeyi temsil eder?",
                [
                    {"key": "A", "text": "Güven inşası ve dinlemenin anlatmak kadar önemli olması", "isCorrect": True, "explanation": "Doğru cevap A'dır: 21. yüzyıl risk iletişiminde kilit kural, halkı azarlamak değil, güven tesis etmek ve toplumun kaygılarını dinlemektir."},
                    {"key": "B", "text": "Küresel eradikasyon sertifikasyonu", "isCorrect": False, "explanation": "Eradikasyon dünya çapında yok olmadır."},
                    {"key": "C", "text": "Biyoterörist ajan üretimi", "isCorrect": False, "explanation": "Konuyla hiçbir ilgisi yoktur."},
                    {"key": "D", "text": "Yalnızca laboratuvar gen dizi analizi", "isCorrect": False, "explanation": "Bu iletişim değil moleküler genetiktir."}
                ]
            )
        ]
    })

    return slides
