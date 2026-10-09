# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_1_slides():
    slides = []

    # Slide 1
    slides.append({
        "id": "k1-18-s01",
        "title": "Halk Sağlığına Giriş: Bireyden Topluma Geçiş ve Temel Felsefe",
        "content": "Geleneksel klinik hekimlik tek bir hastanın şikayetini, tanısını ve tedavisini merkezine alırken, halk sağlığı bakış açısını tüm topluma ve toplumsal dinamiklere genişletir (Sınav Spotu):\n\n- **Halk Sağlığının Özü:** Bireysel tedavinin ötesinde **toplumun tümünün sağlığını korumayı, sürdürmeyi ve geliştirmeyi** hedefler.\n- **Klinik Hekimlik vs Halk Sağlığı:**\n  - Klinik hekimlikte hasta hekime başvurur; halk sağlığında ise hizmet toplumun ayağına götürülür.\n  - Klinik hekimlikte 'hasta birey' varken, halk sağlığında 'hasta toplum' veya 'risk altındaki nüfus' vardır.\n  - Klinik hekimlikte laboratuvar biyokimya ve patolojidir; halk sağlığının temel tanı laboratuvarı ise **epidemiyoloji ve biyoistatistiktir**.\n- **Korumanın Önceliği:** Bir insanı hastalanmaktan korumak, onu hastalandıktan sonra iyileştirmeye çalışmaktan hem insani açıdan çok daha etkilidir hem de ekonomik olarak katbekat ucuzdur.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Klinik Hekimlik vs Halk Sağlığı Yaklaşımı",
                "Klinik Hekimlik (Bireysel Tedavi)",
                "Odak noktası tek bir hastadır; hasta başvurunca tanı ve tedavi başlar; amaç hastalığı iyileştirmektir.",
                "Halk Sağlığı (Toplumsal Koruma)",
                "Odak noktası tüm toplumdur; hizmet toplumun ayağına götürülür; amaç hastalanmayı önlemek ve sağlığı geliştirmektir."
            ),
            make_quiz(
                "Halk sağlığı disiplininin klinik tıp branşlarından en temel ayırt edici felsefesi aşağıdakilerden hangisidir?",
                [
                    {"key": "A", "text": "Yalnızca hastane acil servisine başvuran ağır vakalarla ilgilenmesi", "isCorrect": False, "explanation": "Bu klinik acil tıp yaklaşımıdır."},
                    {"key": "B", "text": "Toplumun tümünün sağlığını korumayı, sürdürmeyi ve geliştirmeyi birincil hedef olarak görmesi", "isCorrect": True, "explanation": "Doğru cevap B'dir: Halk sağlığı bireysel tedaviyi değil, organize toplum çabasıyla tüm toplumun sağlığını korumayı amaçlar."},
                    {"key": "C", "text": "Yalnızca cerrahi operasyon tekniklerini geliştirmeye odaklanması", "isCorrect": False, "explanation": "Cerrahi disiplinlerin görevidir."},
                    {"key": "D", "text": "Hastalık oluştuktan sonra tanı koyup ilaç tedavisi reçete etmekle yetinmesi", "isCorrect": False, "explanation": "Bu klasik klinik hekimliktir; halk sağlığı önlemeye odaklanır."}
                ]
            )
        ]
    })

    # Slide 2
    slides.append({
        "id": "k1-18-s02",
        "title": "Winslow'un Halk Sağlığı Tanımı (1920): Bilim ve Sanat Olarak Halk Sağlığı",
        "content": "Tıp ve halk sağlığı literatürünün en saygın ve evrensel kabul gören tanımı 1920 yılında Charles-Edward Amory Winslow tarafından yapılmıştır (Sınav Spotu):\n\n- **Winslow Tanımı (1920):**\n  - 'Halk sağlığı; organize edilmiş toplum çalışmalarıyla çevre sağlık koşullarını düzelterek, bireylere sağlık bilgisi vererek, bulaşıcı hastalıkları önleyerek, hastalıkların erken tanı ve tedavisini sağlayacak sağlık örgütleri kurarak ve toplumsal çalışmaları her bireyin sağlığını sürdürecek yaşam düzeyini sağlayacak biçimde geliştirerek;\n  1. **Hastalıklardan korunmayı,**\n  2. **Yaşamın uzatılmasını,**\n  3. **Beden ve ruh sağlığı ile çalışma gücünün artırılmasını**\n  sağlayan bir **BİLİM VE SANATTIR**.'\n- **Tanımın Önemi:** Halk sağlığının yalnızca biyolojik bir tıp alanı olmadığını, toplumsal organizasyon, çevre düzeni ve sosyal politikaları da kapsayan çok boyutlu bir disiplin olduğunu tescil etmiştir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Winslow Tanımının Üç Temel Hedefi", "Uygulama Yolu ve Araçları", "Tanımlanan Disiplin Niteliği"],
                [
                    ["1. Hastalıklardan korunma", "Çevre sağlığının düzeltilmesi ve bulaşıcı hastalıkların önlenmesi", "Bilim (Biyomedikal ve Epidemiyolojik Temel)"],
                    ["2. Yaşam süresinin uzatılması", "Erken tanı, tedavi örgütlenmesi ve sağlık eğitimi", "Sanat (Sosyal Organizasyon ve İletişim Becerisi)"],
                    ["3. Beden, ruh sağlığı ve çalışma gücünün artırılması", "Her bireyin sağlığını koruyacak adil yaşam standartlarının kurulması", "Toplumsal ve Kamusal Sorumluluk"]
                ]
            ),
            make_cloze(
                "Winslow'un 1920 yılındaki klasik tanımına göre halk sağlığı organize toplum çalışmalarıyla yaşamı uzatan bir bilim ve sanattır.",
                "bilim ve sanattır",
                "Winslow'un halk sağlığı için kullandığı iki kelimelik niteleme"
            )
        ]
    })

    # Slide 3
    slides.append({
        "id": "k1-18-s03",
        "title": "Nusret Fişek'in Bütüncül Tanımı: Ana Rahminden Ölüme Kadar Sağlık",
        "content": "Türkiye'de halk sağlığı disiplininin ve sosyalleştirilmiş sağlık hizmetlerinin kurucusu olan Prof. Dr. Nusret Fişek, Winslow tanımını çağdaş ve bütüncül bir vizyonla zenginleştirmiştir (Sınav Spotu):\n\n- **Nusret Fişek'in Halk Sağlığı Tanımı:**\n  - 'Halk sağlığı; kişiyi tüm çevresiyle ele alıp sağlığını **ana rahmine düştüğü andan ölümüne kadar** kendi sorumluluğunda gören,\n  - Hastalıkların oluşumunda rol oynayan **fiziki, biyolojik, sosyal, kültürel, ekonomik ve psikolojik çevredeki olumsuz etmenlerin giderilmesine** ve olumlu bir çevre yaratılmasına uğraşan,\n  - Hastaları **erken dönemde bulup tanı koymaya ve tedavi etmeye** çalışan bir **hizmet dalı ve bunun öğretisini yapan bir bilim dalıdır**.'\n- **Yaşamın Bütünlüğü İlkesi:** Sağlık tek bir döneme (örn. sadece erişkinliğe veya hastalık anına) sıkıştırılamaz; doğum öncesinden (intrauterin) son nefese kadar kesintisiz bir bütündür.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Winslow (1920) Tanımı vs Nusret Fişek Tanımı",
                "Winslow Tanımı (1920)",
                "Organize toplum çalışmalarıyla yaşamı uzatan, beden-ruh sağlığını ve verimliliği artıran bir 'bilim ve sanat'tır.",
                "Nusret Fişek Tanımı",
                "Bireyi ana rahminden ölüme kadar tüm çevresiyle (fizik, sosyal, ekonomik) ele alan bir 'hizmet ve bilim dalı'dır."
            ),
            make_quiz(
                "Prof. Dr. Nusret Fişek'in halk sağlığı tanımında yer alan ve sağlığın başlangıç noktasını belirten temel ilke hangisidir?",
                [
                    {"key": "A", "text": "Kişinin ilk işe başladığı veya sigortalı olduğu gün", "isCorrect": False, "explanation": "İş sağlığı başlangıcıdır."},
                    {"key": "B", "text": "Kişinin ana rahmine düştüğü andan ölümüne kadar olan tüm süreç", "isCorrect": True, "explanation": "Doğru cevap B'dir: Fişek, sağlığın ana rahmine düşülen andan ölüme kadar kesintisiz bir bütün olduğunu vurgulamıştır."},
                    {"key": "C", "text": "İlk bulaşıcı hastalığın geçirildiği çocukluk dönemi", "isCorrect": False, "explanation": "Hastalık anı değil, döllenme anı esastır."},
                    {"key": "D", "text": "Ergenlik çağına girilen 18 yaş sınırı", "isCorrect": False, "explanation": "İntrauterin dönem ihmal edilemez."}
                ]
            )
        ]
    })

    # Slide 4
    slides.append({
        "id": "k1-18-s04",
        "title": "Sağlık Anlayışının Tarihsel Evrimi: Büyüsel, Dinsel ve Doğal Dönemler",
        "content": "İnsanlığın hastalıkları anlama ve açıklama çabası binlerce yıllık tarih boyunca üç büyük evreden geçmiştir (Sınav Spotu):\n\n- **1. Büyüsel (Majik) Dönem:**\n  - İlkel toplumlarda hastalıkların nedeni kötü ruhlar, büyüler, şeytani güçler veya lanetler olarak görülmüştür.\n  - Tedavi büyücüler, şamanlar ve kabile büyü hekimleri tarafından kötü ruhları kovma ayinleriyle yürütülmüştür.\n- **2. Dinsel (Teolojik) Dönem:**\n  - Hastalıkların günah işleyen insanlara tanrılar tarafından verilen bir 'ilahi ceza' veya sınav olduğuna inanılmıştır.\n  - İyileşme tapınaklarda adaklar adamak, kurban kesmek ve dua etmekle aranmıştır (örn. Antik Asklepion tapınakları).\n- **3. Doğal ve Rasyonel Dönem:**\n  - MÖ 5. yüzyılda Hipokrat ile başlamıştır; hastalıkların doğaüstü güçlerden değil, **tamamen doğal fiziksel, çevresel ve bedensel nedenlerden** kaynaklandığı kabul edilmiştir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Tıbbi Düşüncenin Evrim Basamakları",
                [
                    "1. Büyüsel Dönem: Hastalık kötü ruhların ve büyülerin eseridir; şaman ayinleri yapılır.",
                    "2. Dinsel Dönem: Hastalık tanrıların cezasıdır; tapınaklarda dua ve kurbanla şifa aranır.",
                    "3. Doğal/Rasyonel Dönem: Hipokrat ile hastalıkların doğal nedenleri ve çevresel faktörleri keşfedilir.",
                    "4. Çağdaş Halk Sağlığı: Hastalıkların sosyal, biyolojik ve çevresel belirleyicileri organize toplumla çözülür."
                ]
            ),
            make_cloze(
                "İnsanlık tarihinde hastalıkların doğaüstü güçlerin cezası değil tamamen doğal nedenlerden kaynaklandığını savunan ilk rasyonel tıp dönemi Hipokrat ile başlamıştır.",
                "Hipokrat",
                "Tıbbın babası kabul edilen antik Yunan hekimi"
            )
        ]
    })

    # Slide 5
    slides.append({
        "id": "k1-18-s05",
        "title": "Gılgamış Destanı ve Mezopotamya Tıbbı: Sağlık Kayıtlarının Kökeni",
        "content": "Tıp ve halk sağlığı tarihinin en eski yazılı belgeleri Mezopotamya uygarlıklarına kadar uzanır (Sınav Spotu):\n\n- **Gılgamış Destanı (MÖ 3000'lerin İlk Yarısı - Uruk):**\n  - İnsanlık tarihinin **bilinen en eski destanıdır**.\n  - Uruk Kralı Gılgamış'ın en yakın dostu Enkidu'nun ölümünün ardından duyduğu derin kederle **ölümsüzlüğü ve sonsuz gençliği arayışının** öyküsüdür.\n  - İnsanoğlunun yaşlanmaya, ölüme ve hastalıklara karşı başkaldırısını ve sağlık arayışını simgeler.\n- **Hammurabi Kanunları (Babil - MÖ 1750):**\n  - Tıp uygulamalarını, hekim ücretlerini ve tıbbi malpraktis cezalarını yasalaştıran bilinen ilk yazılı kodekstir.\n  - Başarısız cerrahi girişimlerde hekimin elinin kesilmesi gibi katı kurallar içerse de, hekimlik mesleğinin kamusal denetim altına alınmasının ilk örneğidir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Gılgamış Destanı vs Hammurabi Kanunları",
                "Gılgamış Destanı (MÖ ~3000)",
                "Bilinen en eski edebi eserdir; insanoğlunun ölümsüzlük, gençlik ve hastalıklara karşı varoluşsal arayışını yansıtır.",
                "Hammurabi Kanunları (MÖ ~1750)",
                "Tıbbi uygulamaları, ameliyatları ve hekimlik sorumluluğunu yasal çerçeveye bağlayan ilk kamusal düzenlemedir."
            ),
            make_quiz(
                "MÖ 3000'lerin ilk yarısında Mezopotamya'da yazılan, ölümsüzlüğü ve hastalıklardan kurtuluşu arayan kralın öyküsünü anlatan bilinen en eski destan hangisidir?",
                [
                    {"key": "A", "text": "Gılgamış Destanı", "isCorrect": True, "explanation": "Doğru cevap A'dır: Uruk Kralı Gılgamış'ın ölümsüzlüğü arayışını anlatan Gılgamış Destanı bilinen en eski destandır."},
                    {"key": "B", "text": "İlyada Destanı", "isCorrect": False, "explanation": "Homeros'un Truva savaşını anlatan destanıdır."},
                    {"key": "C", "text": "Odisseia Destanı", "isCorrect": False, "explanation": "Homeros'un antik Yunan destanıdır."},
                    {"key": "D", "text": "Manas Destanı", "isCorrect": False, "explanation": "Kırgız ulusal destanıdır."}
                ]
            )
        ]
    })

    # Slide 6
    slides.append({
        "id": "k1-18-s06",
        "title": "Hipokrat ve Rasyonel Tıp: Humoral Patoloji Teorisi",
        "content": "Antik Yunan hekimi Hipokrat (MÖ 460-370), tıbbı büyü ve hurafelerden ayırarak rasyonel bir temele oturtmuştur (Sınav Spotu):\n\n- **Doğal Nedenler İlkesi:** Hastalıkların tanrıların gazabı değil, hava, su, beslenme ve çevre gibi tamamen doğal etkenlerin bozulması sonucu ortaya çıktığını savundu.\n- **Humoral Patoloji Kuramı (Dört Sıvı Teorisi):**\n  - Sağlık, vücuttaki dört temel sıvının (**hümor**) dengesi (**ökrazi**) ile mümkündür.\n  - Bu dört sıvı: **Kan (sanguis), Balgam (flegma), Sarı Safra (chole) ve Kara Safra (melanchole)**.\n  - Bu sıvıların dengesizliği veya bozulması (**diskrazi**) hastalığa yol açar.\n- **Klinik Terminoloji:** Semptom, tanı, prognoz, profilaksi, kriz, sepsis terimlerini tıp literatürüne kazandırmış; diyabet, artrit, kanser, eklampsi, epilepsi gibi hastalıkları ilk kez adlandırmıştır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Humoral Sıvı (Hümor)", "İlişkili Organ / Unsur", "Fiziksel Nitelik", "Aşırılığında Görülen Mizaç"],
                [
                    ["Kan (Sanguis)", "Kalp / Hava", "Sıcak ve Nemli", "Sangvinik (Neşeli, hareketli, canlı)"],
                    ["Balgam (Flegma)", "Beyin / Su", "Soğuk ve Nemli", "Flegmatik (Sakin, duygusuz, ağırkanlı)"],
                    ["Sarı Safra (Chole)", "Karaciğer / Ateş", "Sıcak ve Kuru", "Kolerik (Öfkeli, tezcanlı, saldırgan)"],
                    ["Kara Safra (Melanchole)", "Dalak / Toprak", "Soğuk ve Kuru", "Melankolik (Hüzünlü, içe kapanık, kaygılı)"]
                ]
            ),
            make_cloze(
                "Hipokrat'ın humoral patoloji kuramına göre sağlık vücuttaki kan, balgam, sarı safra ve kara safra sıvılarının dengede olmasıdır.",
                "kara safra",
                "Dört vücut sıvısından dördüncüsü olan melankoli sıvısı"
            )
        ]
    })

    # Slide 7
    slides.append({
        "id": "k1-18-s07",
        "title": "Hipokratik Etik İlkeleri: 'Primum Non Nocere' (Önce Zarar Verme)",
        "content": "Hipokrat yalnızca klinik teşhis yöntemleriyle değil, hekimlik meslek ahlakını her şeyin üstünde tutmasıyla ölümsüzleşmiştir (Sınav Spotu):\n\n- **Hipokrat Andı:** Hekimlerin hastaya zarar vermeyeceğine, hastanın sırlarını saklayacağına (tıbbi gizlilik), zehir vermeyeceğine ve adaletle yaklaşacağına dair ettiği meslek yeminidir.\n- **Primum Non Nocere (Önce Zarar Verme):**\n  - Tıp etiğinin en temel ve en kutsal ilkesidir.\n  - Hekim bir tedavi veya müdahale uygularken, hastaya fayda sağlamaktan önce **asla zarar vermemeyi** garanti etmelidir.\n  - Gereksiz müdahalelerden ve hastanın hayatını tehlikeye atacak riskli uygulamalardan kaçınmayı emreder.\n- **Doğa En Güçlü İyileştiricidir (Vis Medicatrix Naturae):** Hipokrat hekimin asıl görevinin doğanın kendi kendini iyileştirme gücüne destek olmak, engelleri kaldırmak olduğunu vurgulamıştır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Hipokratik Tıp Yaklaşımının Dört İlkesi",
                [
                    "1. Gözlem ve Muayene: Hasta detaylı dinlenir, çevresi, suyu ve beslenmesi incelenir.",
                    "2. Doğal Neden Arayışı: Doğaüstü inançlar reddedilir, biyolojik dengesizlik saptanır.",
                    "3. Önce Zarar Vermeme: 'Primum non nocere' ilkesiyle zararlı müdahaleler engellenir.",
                    "4. Doğayı Destekleme: Vücudun kendi kendini onarım gücüne uygun ortam sağlanır."
                ]
            ),
            make_quiz(
                "Hipokratik tıp etiğinin en temel kuralı olan ve günümüzde tüm hekimlik uygulamalarında birincil ilke kabul edilen Latince ilke hangisidir?",
                [
                    {"key": "A", "text": "Primum non nocere (Önce zarar verme)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Primum non nocere, hekimliğin en temel etik kuralıdır."},
                    {"key": "B", "text": "Carpe diem (Günü yakala)", "isCorrect": False, "explanation": "Felsefi bir edebi deyimdir."},
                    {"key": "C", "text": "Post hoc ergo propter hoc (Bundan sonra, öyleyse bundan dolayı)", "isCorrect": False, "explanation": "Mantıksal bir yanılgıdır."},
                    {"key": "D", "text": "De mortuis nil nisi bonum (Ölülerin ardından sadece iyi konuşulur)", "isCorrect": False, "explanation": "Sosyal bir deyimdir."}
                ]
            )
        ]
    })

    # Slide 8
    slides.append({
        "id": "k1-18-s08",
        "title": "Bergamalı Galenos ve Galenik Eczacılık: Tıbbın Roma Dönemi",
        "content": "Bergama (Pergamon) doğumlu Claudius Galenos (MS 129-216), Hipokrat'tan sonra antik çağın en etkili ikinci hekimidir (Sınav Spotu):\n\n- **Roma İmparatorluğu ve Gladyatör Hekimliği:**\n  - Bergama Asklepion'unda yetişmiş, gladyatörlerin cerrahi tedavilerini üstlenerek zengin bir anatomi ve yara deneyimi kazanmıştır.\n  - Roma imparatorlarının (Marcus Aurelius) özel hekimliğini yapmıştır.\n- **Eczacılığın Babası ve Galenik İlaçlar:**\n  - Bitkisel ve hayvansal maddeleri belirli oranlarda karıştırarak, ekstrakte ederek hazırladığı farmasötik formülasyonlara **'Galenik preparatlar'** denir.\n  - Modern eczacılığın ve farmasötik teknolojinin öncüsü kabul edilir.\n- **Humoral Kuramın Dogmalaşması:** Galenos'un anatomi ve fizyoloji yazıları Orta Çağ boyunca yaklaşık 1500 yıl boyunca tartışılamaz mutlak doğrular olarak kabul edilmiştir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Hipokrat vs Bergamalı Galenos",
                "Hipokrat (MÖ 460-370)",
                "Klinik gözlemin kurucusudur; humoral teoriyi ortaya koymuş ve tıp etiğini şekillendirmiştir.",
                "Bergamalı Galenos (MS 129-216)",
                "Deneysel anatomi ve farmakolojinin öncüsüdür; galenik preparatlarla eczacılığın babası sayılır."
            ),
            make_cloze(
                "Bitkisel ve hayvansal etken maddelerin farmasötik formüllerle hazırlanmasına öncülük eden ve eczacılığın babası kabul edilen Bergamalı hekim Galenos'tur.",
                "Galenos",
                "Antik Roma döneminin ünlü Bergamalı hekimi ve farmakoloğu"
            )
        ]
    })

    # Slide 9 - CHECKPOINT 1
    slides.append({
        "id": "k1-18-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Halk Sağlığı Tanımları ve Antik Çağ Tıbbı",
        "content": "Bu checkpointte halk sağlığının temel kavramlarını ve antik çağ tıbbını özetliyoruz:\n\n- **Halk Sağlığı:** Bireyden öte toplumun tümünün sağlığını korumayı ve geliştirmeyi hedefler. Koruma tedaviden üstündür ve ucuzdur.\n- **Winslow (1920):** Organize toplum çalışmalarıyla yaşamı uzatan, beden ve ruh sağlığı ile çalışma gücünü artıran bir **bilim ve sanattır**.\n- **Nusret Fişek:** Kişiyi ana rahmine düştüğü andan ölümüne kadar tüm çevresiyle ele alan, olumsuzlukları gideren bir **hizmet ve bilim dalıdır**.\n- **Gılgamış Destanı:** Uruk Kralı'nın ölümsüzlük arayışını anlatan bilinen en eski destandır.\n- **Hipokrat:** Rasyonel tıbbın ve humoral patolojinin (kan, balgam, sarı safra, kara safra) kurucusudur; temel ilkesi 'Primum non nocere'dir.\n- **Galenos:** Bergamalı hekim, galenik preparatların geliştiricisi, eczacılığın babasıdır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Öncü / Eser", "Dönem / Yıl", "Temel Katkı ve Felsefe"],
                [
                    ["Gılgamış Destanı", "MÖ ~3000 (Uruk)", "Bilinen en eski destan; ölümsüzlük ve sağlık arayışı"],
                    ["Hipokrat", "MÖ 460-370", "Doğal nedenler, Humoral patoloji teorisi, Primum non nocere"],
                    ["Galenos", "MS 129-216", "Galenik preparatlar, anatomi deneyleri, eczacılığın babası"],
                    ["C.E.A. Winslow", "1920", "Organize toplum çabasıyla yaşamı uzatan bilim ve sanat"],
                    ["Nusret Fişek", "1914-1990", "Ana rahminden ölüme bütüncül çevre ve sosyalleştirme"]
                ]
            ),
            make_chain(
                "Antik Tıptan Halk Sağlığına Fikir Gelişimi",
                [
                    "1. Gılgamış ve Mezopotamya: İnsanın ölüm ve hastalıklara karşı ilk örgütlü sorgulaması.",
                    "2. Hipokratik Akıl: Büyü ve ceza anlayışının yıkılması, doğal çevrenin keşfi.",
                    "3. Galenik İlaç: Doğal özütlerin formüle edilerek farmakolojiye dönüştürülmesi.",
                    "4. Winslow ve Fişek: Bireysel tıbbın organize toplum ve kamusal hakka evrilmesi."
                ]
            )
        ]
    })

    # Slide 10
    slides.append({
        "id": "k1-18-s10",
        "title": "Bölüm Özeti: Antik Tıptan İslam Uygarlığı ve Orta Çağa Geçiş",
        "content": "Bölüm 1 boyunca halk sağlığının kurucu tanımlarını ve antik çağın temel taşlarını inceledik:\n\n- **Özet:** Halk sağlığı toplum odaklıdır; koruma esastır; Hipokrat ve Galenos ile tıp büyüden rasyonel gözleme evrilmiştir.\n- **Sonraki Bölüm (Bölüm 2):** Roma'nın çöküşünün ardından tıp meşalesini devralan **İslam Uygarlığı hekimlerini (Razi ve hastane yeri seçimi, İbn-i Sina ve El-Kanun, İbn-ül Habib ve bulaş gözlemleri), Orta Çağ'ı kasıp kavuran Kara Ölüm'ü (Veba) ve Venedik'te doğan Karantina kavramını** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_recall(
                "Winslow'un 1920 yılında yaptığı evrensel halk sağlığı tanımında halk sağlığı hangi iki temel nitelikle tanımlanmıştır?",
                "Bir bilim ve sanattır",
                "Halk sağlığının akademik ve pratik nitelemesi"
            ),
            make_quiz(
                "Hipokrat'ın humoral patoloji kuramında melankolik (hüzünlü ve içine kapanık) mizaçla ilişkilendirilen vücut sıvısı hangisidir?",
                [
                    {"key": "A", "text": "Kara safra (Melanchole)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Kara safra soğuk ve kuru niteliktedir, fazlalığı melankoliye yol açar."},
                    {"key": "B", "text": "Kan (Sanguis)", "isCorrect": False, "explanation": "Sangvinik mizaç yapar."},
                    {"key": "C", "text": "Balgam (Flegma)", "isCorrect": False, "explanation": "Flegmatik mizaç yapar."},
                    {"key": "D", "text": "Sarı safra (Chole)", "isCorrect": False, "explanation": "Kolerik mizaç yapar."}
                ]
            )
        ]
    })

    return slides
