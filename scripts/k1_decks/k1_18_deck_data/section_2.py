# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_2_slides():
    slides = []

    # Slide 11
    slides.append({
        "id": "k1-18-s11",
        "title": "Orta Çağ İslam Hekimliğinin Tıp Tarihindeki Yeri",
        "content": "Avrupa'nın Orta Çağ'da karanlık ve skolastik bir dogmatizme gömüldüğü dönemde, tıp meşalesi İslam coğrafyasında parlamıştır (Sınav Spotu):\n\n- **Antik Mirasın Korunması ve Geliştirilmesi:**\n  - Hipokrat ve Galenos'un Grekçe eserleri Bağdat'taki Beyt'ül Hikme'de (Bilgelik Evi) Arapçaya çevrildi.\n  - Yalnızca çeviriyle yetinilmemiş, titiz klinik gözlemler, farmakolojik deneyler ve hastane teşkilatlanmalarıyla tıp bilimi zenginleştirilmiştir.\n- **Kokuşma ve Miazma Anlayışı:**\n  - Hastalıkların kokuşmuş hava, bataklık gazları ve bozulmuş organik maddelerden kaynaklandığı düşünülmüş; bu anlayış erken dönem çevre sağlığı ve hijyen uygulamalarını doğurmuştur.\n- **Bimaristanlar (Hastaneler):** İslam dünyasında zengin vakıflar tarafından desteklenen, din, dil, ırk ve sosyal sınıf ayrımı gözetmeksizin herkese ücretsiz hizmet veren tam teşekküllü tıp merkezleri kurulmuştur.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Orta Çağ Avrupa Tıbbı vs İslam Hekimliği",
                "Orta Çağ Avrupa Tıbbı",
                "Skolastik baskı, cadı avları, banyo yapmanın yasaklanması ve hastalıkların şeytani ceza sayılması.",
                "İslam Dünyası Hekimliği",
                "Klinik gözlem, deney, hijyen, ücretsiz bimaristanlar (hastaneler) ve tıp kütüphaneleri."
            ),
            make_quiz(
                "Orta Çağ'da İslam dünyasında kurulan, din ve ırk ayrımı gözetmeksizin tüm hastalara ücretsiz tedavi ve bakım sunan tarihi hastanelere ne ad verilirdi?",
                [
                    {"key": "A", "text": "Bimaristan (Darüşşifa)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Bimaristan veya Darüşşifa, İslam ve Türk-İslam coğrafyasındaki gelişmiş hastanelerdir."},
                    {"key": "B", "text": "Asklepion", "isCorrect": False, "explanation": "Antik Yunan tapınak tedavi merkezidir."},
                    {"key": "C", "text": "Leprozaryum", "isCorrect": False, "explanation": "Cüzzam tecrit kampıdır."},
                    {"key": "D", "text": "Karvanseray", "isCorrect": False, "explanation": "Ticaret kervanlarının konaklama yeridir."}
                ]
            )
        ]
    })

    # Slide 12
    slides.append({
        "id": "k1-18-s12",
        "title": "Ebubekir Razi ve Kokuşma Kuramı: Bağdat'ta Et Asarak Hastane Seçimi",
        "content": "Ebubekir Muhammed ibn Zekeriya er-Razi (MS 865-925), klinik gözlem ve deneysel tıbbın en büyük İslam hekimidir (Sınav Spotu):\n\n- **Kokuşma (Putrefaksiyon) Kuramı:**\n  - Hastalıkların havadaki kokuşma ve organik bozulmalarla yakın ilişkili olduğunu savunan ilk hekimlerdendir.\n- **Tarihi Hastane Yeri Seçimi Deneyi:**\n  - Abbasi Halifesi Bağdat'ta yeni bir hastane (Adudi Bimaristanı) inşa etmek istediğinde yer seçimini Razi'ye danışmıştır.\n  - Razi, Bağdat'ın farklı köşelerine ve sokaklarına taze et parçaları astırmıştır.\n  - Belirli aralıklarla etleri kontrol etmiş ve **et parçalarının en geç bozulduğu, en geç kokuştuğu bölgeyi** havanın en temiz ve rutubetin en az olduğu yer olarak belirleyip hastaneyi oraya inşa ettirmiştir.\n- **Klinik Ayırıcı Tanı:** Çiçek hastalığı (Variola) ile kızamığı (Morbilli) klinik olarak birbirinden ilk ayıran hekim de Razi'dir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Razi'nin Hastane Yeri Seçimi Deney Basamakları",
                [
                    "1. Şehir Haritası: Bağdat'ın farklı rüzgar ve yerleşim alanları belirlenir.",
                    "2. Eşit Et Parçaları: Taze etler kentin farklı noktalarındaki direklere asılır.",
                    "3. Kokuşma Hızı Gözlemi: Hangi bölgedeki etin daha çabuk kurtlandığı ve bozulduğu takip edilir.",
                    "4. Temiz Havanın Tespiti: Eti en geç kokuşan nokta en sağlıklı çevre olarak seçilip hastane kurulur."
                ]
            ),
            make_cloze(
                "Bağdat'ta hastane inşa edilecek en havadar ve temiz yeri seçmek için kentin farklı yerlerine et parçaları astırarak en geç kokuşan yeri belirleyen hekim Ebubekir Razi'dir.",
                "Ebubekir Razi",
                "Kokuşma kuramını hastane yer seçiminde kullanan büyük İslam hekimi"
            )
        ]
    })

    # Slide 13
    slides.append({
        "id": "k1-18-s13",
        "title": "İbn-i Sina (Avicenna): 'El-Kanun fi't-Tıbb' ve 'Kitab-üş Şifa'",
        "content": "Batı dünyasında 'Avicenna' ve 'Hekimlerin Hükümdarı' olarak tanınan İbn-i Sina (980-1037), tıp tarihinin en anıtsal figürlerindendir (Sınav Spotu):\n\n- **El-Kanun fi't-Tıbb (Tıbbın Kanunu):**\n  - Beş ciltlik devasa bir tıp ansiklopedisidir.\n  - Anatomi, fizyoloji, patoloji, hijyen, cerrahi ve farmakolojiyi mükemmel bir mantıksal sistemle sınıflandırmıştır.\n  - 12. yüzyılda Latinceye çevrilmiş ve Avrupa tıp fakültelerinde (Paris, Montpellier, Bologna) **17. yüzyılın sonuna kadar yaklaşık 500 yıl boyunca temel ders kitabı** olarak okutulmuştur.\n- **Kitab-üş Şifa (İyileşme Kitabı):** Mantık, fizik, matematik ve metafiziği kapsayan felsefi başyapıtıdır.\n- **Halk Sağlığı ve Hijyen Görüşü:** Hastalıkların suda ve havada bulunan 'gözle görülemeyecek kadar küçük tohumlar veya kurtçuklar' aracılığıyla yayılabileceğini mikroskoptan yüzyıllar önce sezgisel olarak öne sürmüştür.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["İbn-i Sina Eseri", "İçerik ve Kapsam", "Tıp Tarihindeki Etkisi"],
                [
                    ["El-Kanun fi't-Tıbb", "5 ciltlik tıp ve farmakoloji ansiklopedisi", "500 yıl boyunca Doğu ve Batı tıp fakültelerinde temel başvuru kitabı"],
                    ["Kitab-üş Şifa", "Ruh, akıl, mantık ve doğa felsefesi eseri", "Bütüncül tıp ve psikolojik iyileşmenin kuramsal temeli"]
                ]
            ),
            make_quiz(
                "İbn-i Sina'nın yazdığı, 17. yüzyılın sonuna kadar hem İslam coğrafyasında hem de Avrupa üniversitelerinde tıp eğitiminin vazgeçilmez temel ders kitabı olan anıtsal eser hangisidir?",
                [
                    {"key": "A", "text": "El-Kanun fi't-Tıbb (Tıbbın Kanunu)", "isCorrect": True, "explanation": "Doğru cevap A'dır: El-Kanun fi't-Tıbb yüzyıllar boyunca tıp öğretiminin klasik başvuru kitabı olmuştur."},
                    {"key": "B", "text": "Kitab-ül Hayavan", "isCorrect": False, "explanation": "Cahiz'in zooloji kitabıdır."},
                    {"key": "C", "text": "De Re Metallica", "isCorrect": False, "explanation": "Agricola'nın madencilik kitabıdır."},
                    {"key": "D", "text": "Kutadgu Bilig", "isCorrect": False, "explanation": "Yusuf Has Hacib'in siyasetnamesidir."}
                ]
            )
        ]
    })

    # Slide 14
    slides.append({
        "id": "k1-18-s14",
        "title": "İbn-ül Habib ve Salgın Gözlemleri: Temas, Giysi ve Kap-Kacak Bulaşı",
        "content": "Endülüs ve İslam tıbbında salgın hastalıkların bulaşma dinamiklerini gözlemleyen öncülerden biri de İbn-ül Habib'dir (Sınav Spotu):\n\n- **Veba Salgınlarında Temas Gözlemi:**\n  - Endülüs'te yaşanan veba ve humma salgınlarında hastalarla yakın temasta bulunanların hastalandığını kayıt altına almıştır.\n- **Cansız Maddelerle Bulaş (Fomitler):**\n  - Bulaşmanın yalnızca solunan havayla sınırlı kalmadığını; hastaların **kullandığı giysiler, yatak çarşafları, kap-kacak ve yemek kapları** aracılığıyla da sağlıklı kişilere geçtiğini ilk kez sistemli biçimde gözlemlemiştir.\n- **Korunmanın Önemi:**\n  - Tedavi imkanlarının kısıtlı olduğu bir çağda salgından korunmanın en etkili yolunun **hastalarla teması kesmek, eşyalarını dezenfekte etmek veya yakmak ve sağlam kişileri izole etmek** olduğunu savunmuştur.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Miazma (Kötü Hava) vs İbn-ül Habib'in Temas/Fomit Gözlemi",
                "Klasik Miazma İnancı",
                "Hastalık yalnızca havaya yayılan görünmez kokulardan ve zehirli buharlardan bulaşır sanılıyordu.",
                "İbn-ül Habib'in Gözlemi",
                "Bulaşmanın hasta giysileri, çarşaflar ve kap-kacak gibi eşyalarla (fomitlerle) doğrudan temasla olduğunu kanıtladı."
            ),
            make_cloze(
                "Veba salgınlarında hastalığın yalnızca hava yoluyla değil, hastaların giysileri ve kap-kacakları üzerinden temasla bulaştığını gözlemleyen hekim İbn-ül Habib'dir.",
                "İbn-ül Habib",
                "Temas ve cansız eşya (fomit) bulaşını ilk vurgulayan İslam hekimi"
            )
        ]
    })

    # Slide 15
    slides.append({
        "id": "k1-18-s15",
        "title": "Kara Ölüm (Veba Pandemisi): 14. Yüzyıl Demografik ve Sosyal Çöküşü",
        "content": "İnsanlık tarihinin en yıkıcı pandemisi 1347-1351 yılları arasında Avrupa, Asya ve Kuzey Afrika'yı vuran 'Kara Ölüm'dür (Sınav Spotu):\n\n- **Etken ve Vektör:** Yersinia pestis basili; kemirgenlerden (siyah sıçan) insanlara **kene ve pireler (Xenopsylla cheopis)** aracılığıyla bulaşır.\n- **Demografik Yıkım:**\n  - Yalnızca 4-5 yıl içinde Avrupa nüfusunun yaklaşık **%30 ila %50'si (25-50 milyon insan)** hayatını kaybetmiştir.\n  - Kentler boşalmış, tarlalar ekilememiş, feodal sistem çökmüş ve iş gücü açığı doğmuştur.\n- **Halk Sağlığı Açısından Etkisi:**\n  - Hastalık karşısında bireysel tedavinin tamamen çaresiz kalması, yönetimleri **toplumsal önlemler, tecrit, mezarlıkların kent dışına taşınması ve karantina** gibi kamusal halk sağlığı mekanizmalarını kurmaya zorlamıştır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Kara Ölümün Halk Sağlığı Kurumlarını Doğurma Süreci",
                [
                    "1. Pandemik Yayılım: Ticaret gemileriyle sıçan ve pireler Avrupa limanlarına veba taşır.",
                    "2. Bireysel Tıbbın İflası: İlaç ve bitkisel karışımlar devasa ölümleri engelleyemez.",
                    "3. Kamusal Çaresizlik: Nüfusun yarısı ölünce devletler ve kent konseyleri müdahale etmek zorunda kalır.",
                    "4. Karantina ve Sağlık Kurulları: Gemilerin tecrit edilmesi ve ilk sağlık kurullarının kurulması sağlanır."
                ]
            ),
            make_quiz(
                "14. yüzyılda Avrupa nüfusunun üçte birinden fazlasını yok ederek feodal yapıyı sarsan ve modern karantina uygulamalarının doğmasına yol açan büyük pandemi hangisidir?",
                [
                    {"key": "A", "text": "Kara Ölüm (Veba Pandemisi)", "isCorrect": True, "explanation": "Doğru cevap A'dır: 1347-1351 Kara Ölüm veba pandemisi halk sağlığı önlemlerinin ve karantinanın miladı olmuştur."},
                    {"key": "B", "text": "İspanyol Gribi", "isCorrect": False, "explanation": "1918 yılında 20. yüzyılda yaşanmıştır."},
                    {"key": "C", "text": "Asya Kolerası", "isCorrect": False, "explanation": "19. yüzyılda yaşanmıştır."},
                    {"key": "D", "text": "Justinien Vebası", "isCorrect": False, "explanation": "6. yüzyılda Bizans'ta yaşanmıştır."}
                ]
            )
        ]
    })

    # Slide 16
    slides.append({
        "id": "k1-18-s16",
        "title": "Karantina Kavramının Doğuşu: Venedik 'Quaranta Giorni' (40 Gün) Kuralı",
        "content": "Karantina, halk sağlığı tarihinin en köklü ve başarılı kamusal enfeksiyon kontrol mekanizmalarından biridir (Sınav Spotu):\n\n- **Kavramın Kökeni:**\n  - İtalyanca **'quaranta giorni' (kırk gün)** kelimesinden türemiştir.\n- **Tarihsel Uygulama (Ragusa ve Venedik):**\n  - 1377 yılında Adriyatik kıyısındaki Ragusa (Dubrovnik) limanında salgın bölgelerinden gelen gemilerin 30 gün ('trentina') açıkta bekletilmesi kararlaştırıldı.\n  - 1403 yılında Venedik Senatosu bu süreyi **40 güne (karantina)** çıkardı ve Santa Maria di Nazareth adasında tarihin ilk karantina hastanesini (**lazaretto**) kurdu.\n- **40 Gün Mantığı:** Dinsel geleneklerin (İsa'nın çölde 40 gün kalması, Nuh tufanında 40 gün yağmur) etkisi bulunmakla birlikte, vebanın kuluçka ve klinik seyrini kapsayacak yeterlilikte bir gözlem süresi sağlamıştır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Kavram / Kurum", "Kökeni ve Anlamı", "Uygulama Amacı"],
                [
                    ["Quaranta Giorni", "İtalyanca '40 gün'", "Salgın bölgesinden gelen yolcu ve malların açık denizde tecrit süresi"],
                    ["Lazaretto", "Venedik'teki tecrit adası", "Şüpheli yolcuların ve cüzzamlı/vebalıların karaya ayak basmadan gözlenmesi"],
                    ["Karantina", "Evrensel halk sağlığı terimi", "Enfeksiyonun kuluçka süresince bulaş zincirini kırmak için uygulanan kısıtlama"]
                ]
            ),
            make_cloze(
                "Salgın bölgelerinden gelen gemilerin limana girmeden önce açıkta bekletilmesini ifade eden karantina terimi İtalyanca kırk gün anlamına gelen quaranta giorni sözcüğünden türemiştir.",
                "kırk gün",
                "Karantina kelimesinin İtalyanca sözlük karşılığı olan zaman dilimi"
            )
        ]
    })

    # Slide 17
    slides.append({
        "id": "k1-18-s17",
        "title": "Lepra (Cüzzam) ve Orta Çağda İzolasyon / Leprozaryumlar",
        "content": "Mycobacterium leprae'nin neden olduğu lepra (cüzzam), insanlık tarihinde en katı sosyal tecrit uygulamalarına maruz kalan hastalıktır (Sınav Spotu):\n\n- **Damgalama ve Dini Dışlanma:**\n  - Cüzzamlılar derideki şekil bozuklukları nedeniyle 'lanetlenmiş' veya 'yaşayan ölü' kabul edilmiş, toplumdan tamamen aforoz edilmiştir.\n  - Boyunlarına çıngırak veya çan asılarak dolaşmaya zorlanmış, sağlıklı insanlara yaklaşmaları ölüm cezasıyla yasaklanmıştır.\n- **Leprozaryumlar (Cüzzam Evleri):**\n  - Orta Çağ Avrupa'sında ve Doğu'da kent surlarının kilometrelerce uzağında binlerce lepra tecrit merkezi kurulmuştur.\n- **Halk Sağlığı Dersi:**\n  - Bilimsel olmayan zalimce damgalama ve ayrımcılık bir halk sağlığı hatası olsa da, lepranın bulaşıcılığının fark edilmesi ve tecrit edilmesi **kronik enfeksiyonların izolasyonla kontrol altına alınabileceğinin** tarihteki en erken kanıtıdır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Leprada Damgalama vs Bilimsel İzolasyon",
                "Orta Çağ Damgalaması",
                "Hastayı 'lanetlenmiş günahkar' ilan edip çan taktırarak insanlık dışı şekilde sürgüne göndermek.",
                "Halk Sağlığı Açısından İzolasyon",
                "Bulaş zincirini kırmak amacıyla tıbbi gözetim altında tedavi ve rehabilitasyon sağlamak."
            ),
            make_quiz(
                "Orta Çağ boyunca şekil bozukluğu yapan cüzzam (lepra) hastalarının kent dışındaki tecrit merkezlerine kapatıldığı tarihi kurumlara ne ad verilir?",
                [
                    {"key": "A", "text": "Leprozaryum (Miskinler Tekkesi)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Cüzzamlıların tecrit edildiği merkezlere Batı'da Leprozaryum, Osmanlı'da Miskinler Tekkesi denirdi."},
                    {"key": "B", "text": "Sanatoryum", "isCorrect": False, "explanation": "Tüberküloz hastalarının dinlenme ve tedavi hastanesidir."},
                    {"key": "C", "text": "Karantina istasyonu", "isCorrect": False, "explanation": "Limanlarda gemilerin bekletildiği yerdir."},
                    {"key": "D", "text": "Huzurevi", "isCorrect": False, "explanation": "Yaşlı bakım merkezidir."}
                ]
            )
        ]
    })

    # Slide 18
    slides.append({
        "id": "k1-18-s18",
        "title": "Osmanlı Tıbbında Şifahaneler ve Bimarhaneler: Su Sesi ve Müzikle Terapi",
        "content": "Osmanlı İmparatorluğu, İslam tıp mirasını hümanist ve estetik bir sağlık anlayışıyla zirveye taşımıştır (Sınav Spotu):\n\n- **Edirne Sultan II. Bayezid Külliyesi Şifahanesi (1488):**\n  - Akıl ve ruh hastalarının Avrupa'da 'içine şeytan girmiş' denilerek zincirlendiği ve yakıldığı bir dönemde;\n  - Edirne Darüşşifası'nda hastalar **su sesi, musiki (makamlarla müzik terapisi), güzel kokular ve çiçek bahçeleriyle** tedavi edilmiştir.\n  - Akustik mimarisi sesi kubbeden her odaya eşit yankılatacak şekilde tasarlanmıştır.\n- **Vakıf Sağlık Modeli:**\n  - Zenginlerin ve padişahların kurduğu vakıflar sayesinde hastanelerde tedavi, ilaç, yemek ve konaklama tamamen **ücretsiz** sunulmuştur.\n- **Sosyal Hekimlik Nüveleri:** Osmanlı'da yetimlerin korunması, yoksullara aşevi hizmeti ve cüzzamlılar için 'Miskinler Tekkesi' kurulması halk sağlığının öncül adımlarıdır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Osmanlı Darüşşifasında Bütüncül Tedavi Yaklaşımı",
                [
                    "1. Ücretsiz Kabul: Vakıf güvencesiyle maddi durumu ne olursa olsun hasta kabul edilir.",
                    "2. Doğal ve Akustik Mimari: Havuzlu geniş avlu, havadar kubbeler ve bol gün ışığı sağlanır.",
                    "3. Müzik ve Ses Terapisi: Hastanın ruh haline uygun makamlarla müzik ve su sesi dinletilir.",
                    "4. Sosyal Rehabilitasyon: Çiçek yetiştiriciliği ve el işleriyle hasta yeniden topluma kazandırılır."
                ]
            ),
            make_cloze(
                "1488 yılında kurulan ve akıl hastalarını su sesi, müzik makamları ve güzel kokularla tedavi eden ünlü Osmanlı tıp merkezi Edirne II. Bayezid Külliyesi Darüşşifası'dır.",
                "Edirne II. Bayezid",
                "Müzik ve su sesiyle şifa dağıtan ünlü Osmanlı külliyesinin padişah adı"
            )
        ]
    })

    # Slide 19 - CHECKPOINT 2
    slides.append({
        "id": "k1-18-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] İslam Tıbbı, Salgınlar ve Karantina Tarihçesi",
        "content": "Bu checkpointte Orta Çağ İslam hekimliğini, pandemileri ve karantinanın doğuşunu özetliyoruz:\n\n- **Ebubekir Razi:** Kokuşma kuramı doğrultusunda Bağdat'ta direklere et astırarak en geç bozulan yere hastane inşa ettirmiştir; çiçek ile kızamığı ayırt etmiştir.\n- **İbn-i Sina (Avicenna):** 500 yıl boyunca temel tıp kitabı olarak okutulan 'El-Kanun fi't-Tıbb'ı yazmıştır.\n- **İbn-ül Habib:** Vebada bulaşın yalnızca hava değil giysiler ve kap-kacak temasıyla (fomitlerle) olduğunu göstermiştir.\n- **Kara Ölüm (1347-1351):** Yersinia pestis veba pandemisi Avrupa nüfusunun üçte birini yok etmiş, örgütlü halk sağlığı önlemlerini zorunlu kılmıştır.\n- **Karantina (Quaranta Giorni):** Venedik'te gemilerin 40 gün açıkta tecrit edilmesiyle başlamış, ilk lazaretto kurulmuştur.\n- **Osmanlı Şifahaneleri:** Edirne II. Bayezid Darüşşifası'nda akıl hastaları su sesi ve müzikle insancıl biçimde tedavi edilmiştir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Tarihi Olay / Kişi", "Dönem / Yüzyıl", "Halk Sağlığına Bıraktığı Miras"],
                [
                    ["Ebubekir Razi", "MS 865-925", "Havanın temizliğine göre et asarak hastane yeri seçimi"],
                    ["İbn-i Sina", "MS 980-1037", "El-Kanun eseri, 500 yıllık tıp ansiklopedisi"],
                    ["İbn-ül Habib", "Orta Çağ", "Giysi ve kap-kacakla temasın salgınlardaki rolü"],
                    ["Kara Ölüm", "1347-1351", "Demografik yıkım ve kamusal sağlık meclislerinin kuruluşu"],
                    ["Venedik Karantinası", "1377-1403", "40 günlük açık deniz tecridi ve lazaretto kurumu"],
                    ["Edirne Darüşşifası", "1488", "Su sesi ve müzikle bütüncül ruh sağlığı tedavisi"]
                ]
            ),
            make_chain(
                "Salgın Yönetiminde Tarihsel Dönüm Noktaları",
                [
                    "1. Razi'nin Çevre Seçimi: Hastane yerinin temiz havaya göre belirlenmesi.",
                    "2. İbn-ül Habib'in İzolasyonu: Bulaşıcı eşyaların imhası ve temasın kesilmesi.",
                    "3. Venedik Karantinası: Gemilerin 40 gün tecrit edilmesi ve ilk sağlık kordonu.",
                    "4. Kamusal Sağlık Örgütlenmesi: Kent sağlık konseylerinin daimi hale gelmesi."
                ]
            )
        ]
    })

    # Slide 20
    slides.append({
        "id": "k1-18-s20",
        "title": "Bölüm Özeti: Orta Çağdan Mikrobiyolojik Devrime Geçiş",
        "content": "Bölüm 2 boyunca Orta Çağ salgınlarının yarattığı yıkımı, İslam tıbbının akılcı çözümlerini ve karantinanın doğumunu inceledik:\n\n- **Özet:** Salgınlar toplumları sarsmış; Razi havanın önemini kanıtlamış, Venedik karantinayı başlatmıştır; ancak hastalıkların asıl mikrobiyolojik etkenleri henüz bilinmiyordu.\n- **Sonraki Bölüm (Bölüm 3):** Mikroskobun icadıyla başlayan **Mikrobiyolojik Devrimi (Leeuwenhoek'un mikroorganizmaları keşfi, Pasteur'ün kendiliğinden oluşu yıkması, Robert Koch ve Koch postülatları)** ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_recall(
                "Bağdat'ta et astırarak en geç bozulan yere hastane inşa ettiren ve çiçek ile kızamığı ilk ayıran İslam hekimi kimdir?",
                "Ebubekir Razi (er-Razi)",
                "Kokuşma kuramının öncüsü İslam hekimi"
            ),
            make_quiz(
                "Venedik'te 1403 yılında salgın şüphesi olan gemi yolcularını ve hastaları karaya çıkarmadan tecrit etmek amacıyla kurulan ilk karantina hastanelerine ne ad verilirdi?",
                [
                    {"key": "A", "text": "Lazaretto", "isCorrect": True, "explanation": "Doğru cevap A'dır: Venedik Santa Maria di Nazareth adasında kurulan ilk tecrit hastanesine Lazaretto adı verilmiştir."},
                    {"key": "B", "text": "Darüşşifa", "isCorrect": False, "explanation": "İslam/Türk hastanesidir."},
                    {"key": "C", "text": "Sanatoryum", "isCorrect": False, "explanation": "Verem hastanesidir."},
                    {"key": "D", "text": "Poliklinik", "isCorrect": False, "explanation": "Modern ayaktan tedavi birimidir."}
                ]
            )
        ]
    })

    return slides
