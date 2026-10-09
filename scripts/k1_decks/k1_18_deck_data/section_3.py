# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_3_slides():
    slides = []

    # Slide 21
    slides.append({
        "id": "k1-18-s21",
        "title": "Mikroskobun İcadı ve Mikrobiyal Dünyanın Keşfi: Hooke ve Leeuwenhoek",
        "content": "17. yüzyılda optik merceklerin gelişimi, tıp ve doğa bilimlerinde devrim yaratan 'görünmeyen evrenin' kapısını aralamıştır (Sınav Spotu):\n\n- **Robert Hooke (1635-1703):**\n  - Bileşik mikroskobu canlı organizmaları incelemek için ilk kullanan bilim insanıdır.\n  - 1665 yılında şişe mantarı kesitinde gördüğü boş odacıklara manastır hücrelerine benzeterek **'hücre' (cell)** adını vermiştir ('Micrographia' eseri).\n- **Antonie van Leeuwenhoek (1632-1723):**\n  - Kendi elleriyle tek mercekli ancak 300 kata kadar büyütebilen son derece hassas mikroskoplar üretmiştir.\n  - 1675 yılında göl suyu, diş plağı ve dışkı örneklerinde hareket eden mikroskobik canlıları ilk kez görmüş ve onlara **'animalcules' (küçük hayvancıklar)** adını vermiştir.\n- **Halk Sağlığı Açısından Önemi:** Bulaşıcı hastalıkların sorumlusu olan mikroorganizmaların varlığı ilk kez doğrudan gözlemlenmiştir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Robert Hooke vs Antonie van Leeuwenhoek",
                "Robert Hooke (1665)",
                "Bileşik mikroskopla mantar dokusunu inceledi ve 'hücre' kavramını ilk kez tanımladı.",
                "Antonie van Leeuwenhoek (1675)",
                "Kendi ürettiği mikroskopla bakterileri ve protozoonları ('animalcules') canlı olarak ilk gören kişidir."
            ),
            make_quiz(
                "Kendi ürettiği yüksek çözünürlüklü el yapımı mikroskopla 1675 yılında su ve diş plağında serbest yüzen mikroorganizmaları ('animalcules') ilk kez gözlemleyen doğa bilimci kimdir?",
                [
                    {"key": "A", "text": "Antonie van Leeuwenhoek", "isCorrect": True, "explanation": "Doğru cevap A'dır: Leeuwenhoek 1675'te mikroorganizmaları ilk kez doğrudan gözlemlemiştir."},
                    {"key": "B", "text": "Robert Hooke", "isCorrect": False, "explanation": "Hücre terimini bulmuştur."},
                    {"key": "C", "text": "Louis Pasteur", "isCorrect": False, "explanation": "Mikrobiyolojiyi 19. yüzyılda kurmuştur."},
                    {"key": "D", "text": "Robert Koch", "isCorrect": False, "explanation": "19. yüzyılda tüberküloz basilini bulmuştur."}
                ]
            )
        ]
    })

    # Slide 22
    slides.append({
        "id": "k1-18-s22",
        "title": "Antonie van Leeuwenhoek (1675): 'Animalcules' ve Canlı Mikroorganizmalar",
        "content": "Leeuwenhoek'un Delft'teki kumaş tüccarlığından Londra Royal Society üyeliğine uzanan serüveni bilim tarihinin en etkileyici keşiflerindendir (Sınav Spotu):\n\n- **Teknik Deha:**\n  - Dönemin bileşik mikroskopları bulanık gösterirken, Leeuwenhoek'un minik cam küreleri eriterek yaptığı tek mercekli mikroskoplar olağanüstü optik berraklık sağlamıştır.\n- **İlk Gözlemler:**\n  - Yağmur suyunda, diş kirinde ve sirke içinde binlerce minik canlının yüzdüğünü, döndüğünü ve hareket ettiğini çizimleriyle kayıt altına almıştır.\n  - Bakterileri, protozoonları (serbest amipler ve siliyatlar), sperm hücrelerini ve alyuvarları ilk çizen kişidir.\n- **Eksik Halka:**\n  - Leeuwenhoek bu küçük hayvancıkları keşfetmiş olsa da, bunların **hastalıklara yol açabileceğini ve salgınların nedeni olduğunu** düşünememiştir; bu bağlantı yaklaşık 200 yıl sonra Pasteur ve Koch tarafından kurulacaktır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Mikrobiyal Dünyanın Keşif Aşamaları",
                [
                    "1. Mercek Parlatma: Leeuwenhoek minik cam küreleri yüksek ısıyla pürüzsüzleştirir.",
                    "2. Numune İnceleme: Diş plağı ve kuyu suları odaklama iğnesine yerleştirilir.",
                    "3. 'Animalcules' Tespiti: Canlı hareket eden tek hücreli mikroorganizmalar çizilir.",
                    "4. Bilim Dünyasına Bildirim: Londra Royal Society'ye mektuplarla ilk mikrobiyolojik raporlar sunulur."
                ]
            ),
            make_cloze(
                "Antonie van Leeuwenhoek'un 1675 yılında mikroskop altında ilk kez gözlemlediği hareketli mikroorganizmalara verdiği tarihi isim animalcules terimidir.",
                "animalcules",
                "Leeuwenhoek'un küçük hayvancıklar anlamına gelen Latince nitelemesi"
            )
        ]
    })

    # Slide 23
    slides.append({
        "id": "k1-18-s23",
        "title": "Spontan Jenerasyon (Abiyogenez) Çürütülmesi: Redi ve Spallanzani",
        "content": "Yüzyıllar boyunca insanlar kurtçukların çürüyen etten, kurbağaların çamurdan, farelerin kirli bez ve buğdaydan kendiliğinden türediğine inanmıştır (Spontan Jenerasyon / Abiyogenez) (Sınav Spotu):\n\n- **Francesco Redi Deneyi (1668):**\n  - Bir kavanoza açık et, bir kavanoza kapalı et, diğerine tülbentle örtülü et koymuştur.\n  - Kurtçukların yalnızca sineklerin yumurtlayabildiği açık ette oluştuğunu, kapalı kavanozlarda et çürüse bile kurtçuk oluşmadığını kanıtlayarak 'büyük canlılarda' abiyogenezi çürütmüştür.\n- **Lazzaro Spallanzani Deneyi (1768):**\n  - Et suyunu kaynatıp ağzını erimiş camla hava almayacak şekilde kapattığında mikroorganizma üremediğini gösterdi.\n- **Son Savunma:** Abiyogenez taraftarları 'Spallanzani kavanozun ağzını kapatarak yaşamın temel gücü olan havayı (vital force) yok etti' diyerek direnmeye devam etmiştir; kesin darbeyi Pasteur vuracaktır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Abiyogenez (Kendiliğinden Oluş) vs Biyogenez (Yaşamdan Yaşama)",
                "Abiyogenez İnancı",
                "Canlıların cansız maddelerden, çamurdan ve kokuşmuş etten kendiliğinden türediği dogması.",
                "Biyogenez İlkesi",
                "Her canlı ancak kendisinden önce var olan bir canlı hücreden veya yumurtadan ürer (Omne vivum ex vivo)."
            ),
            make_quiz(
                "Açık, kapalı ve tülbentli kavanozlara et koyarak kurtçukların etten değil sinek yumurtalarından çıktığını gösteren ve abiyogenezi sarsan ilk İtalyan bilim insanı kimdir?",
                [
                    {"key": "A", "text": "Francesco Redi", "isCorrect": True, "explanation": "Doğru cevap A'dır: Francesco Redi 1668'deki kavanoz deneyiyle etten kendiliğinden kurtçuk çıkmadığını kanıtlamıştır."},
                    {"key": "B", "text": "Lazzaro Spallanzani", "isCorrect": False, "explanation": "Et suyu kaynatma deneyini yapmıştır."},
                    {"key": "C", "text": "Galileo Galilei", "isCorrect": False, "explanation": "Gökbilimci ve fizikçidir."},
                    {"key": "D", "text": "Girolamo Fracastoro", "isCorrect": False, "explanation": "Bulaş tohumları teorisini ortaya atmıştır."}
                ]
            )
        ]
    })

    # Slide 24
    slides.append({
        "id": "k1-18-s24",
        "title": "Louis Pasteur ve Germ Kuramı: Kuğu Boyunlu Balon Deneyi",
        "content": "Fransız kimyager ve mikrobiyolog Louis Pasteur (1822-1895), modern mikrobiyoloji ve halk sağlığının en büyük kurucularındandır (Sınav Spotu):\n\n- **Kuğu Boyunlu Balon (Swan-Neck Flask) Deneyi (1861):**\n  - Pasteur cam balonun boynunu 'S' şeklinde kıvırmıştır.\n  - Balondaki besiyerini kaynatarak sterilize etmiştir.\n  - Balon havaya açıktır ('vital force' engellenmemiştir) ancak havadaki toz ve mikroplar kıvrık boynun tabanına çökerek sıvıya ulaşamaz.\n  - Yıllarca bekleyen besiyerinde hiçbir mikroorganizma ürememiştir; ancak boyun kırılıp sıvı havayla doğrudan temas edince hızla bulanıklaşmış ve bakteriler üremiştir.\n- **Devrimsel Sonuç:** **Abiyogenez (kendiliğinden oluş) kesin olarak yıkılmış; 'Germ Kuramı' (hastalıkların mikrop kuramı) bilimsel olarak kanıtlanmıştır.**",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Pasteur'ün Kuğu Boyunlu Balon Deney Adımları",
                [
                    "1. Besiyeri Hazırlığı: Besleyici et suyu cam balona doldurulur.",
                    "2. Kuğu Boynu Kıvırma: Balonun boynu ısıtılarak ince 'S' biçiminde bükülür.",
                    "3. Sterilizasyon: Sıvı kaynatılarak içindeki tüm canlı sporlar öldürülür.",
                    "4. Toz Tuzaklaması: Hava serbestçe girerken toz ve mikroplar kıvrımda çöker; sıvı steril kalır.",
                    "5. Boynun Kırılması: Balon boynu kırılınca havadaki mikroplar sıvıya düşer ve bakteri patlaması olur."
                ]
            ),
            make_cloze(
                "Louis Pasteur kuğu boyunlu balon deneyi ile canlıların kendiliğinden oluşamayacağını kanıtlayarak abiyogenez teorisini kesin olarak çürütmüştür.",
                "abiyogenez",
                "Canlıların cansız maddelerden kendiliğinden türediğini iddia eden çürütülmüş kuram"
            )
        ]
    })

    # Slide 25
    slides.append({
        "id": "k1-18-s25",
        "title": "Pastörizasyon Tekniği ve Süt Kaynaklı Enfeksiyonların Önlenmesi",
        "content": "Pasteur fermentasyonun kimyasal bir bozulma değil, canlı mayalar ve bakteriler tarafından gerçekleştirilen biyolojik bir süreç olduğunu kanıtlamıştır (Sınav Spotu):\n\n- **Fermentasyonun Doğası:**\n  - Yararlı mayalar üzüm suyunu şaraba dönüştürürken, yabancı bakteriler şarabı ve birayı sirkeye çevirerek ekşitir.\n- **Pastörizasyon Yöntemi:**\n  - Sıvıların (şarap, bira ve özellikle **süt**) kaynama noktasının altında belirli bir sıcaklıkta (örn. 63-72°C) belirli bir süre tutularak içindeki patojen bakterilerin besin değerini bozmadan öldürülmesidir.\n- **Halk Sağlığı Zaferi:**\n  - Çiğ sütle bulaşan **tüberküloz (Mycobacterium bovis), brusella (Brucella abortus/melitensis), tifo ve difteri** gibi ölümcül salgınlar süt pastörizasyonu sayesinde kitlesel olarak engellenmiştir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Hastalık", "Sütle Bulaşan Patojen", "Pastörizasyonun Halk Sağlığı Etkisi"],
                [
                    ["Sığır Tüberkülozu", "Mycobacterium bovis", "Çocuklarda barsak ve kemik tüberkülozunu sıfırlamıştır"],
                    ["Bruselloz (Malta Humması)", "Brucella türleri", "Çiğ sütten geçen dalgalı ateş ve eklem tutulumunu önlemiştir"],
                    ["Tifo ve Paratifo", "Salmonella Typhi", "Süt kaynaklı kitlesel bağırsak salgınlarını durdurmuştur"],
                    ["Q Ateşi", "Coxiella burnetii", "Pastörizasyon ısısına en dirençli patojenin standardıdır"]
                ]
            ),
            make_quiz(
                "Süt ve süt ürünlerinin ısıtılarak patojen bakterilerden arındırılması yöntemi olan pastörizasyon, halk sağlığı tarihinde özellikle hangi ölümcül sığır enfeksiyonunun insanlara geçişini engellemiştir?",
                [
                    {"key": "A", "text": "Sığır tüberkülozu (Mycobacterium bovis)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Süt pastörizasyonunun en büyük zaferi çiğ sütle çocuklara bulaşan M. bovis tüberkülozunu engellemesidir."},
                    {"key": "B", "text": "Kuduz virüsü", "isCorrect": False, "explanation": "Kuduz ısırıkla bulaşır, sütle geçmez."},
                    {"key": "C", "text": "Sıtma paraziti", "isCorrect": False, "explanation": "Sivrisinekle bulaşır."},
                    {"key": "D", "text": "Kızamık virüsü", "isCorrect": False, "explanation": "Solunum damlacıklarıyla bulaşır."}
                ]
            )
        ]
    })

    # Slide 26
    slides.append({
        "id": "k1-18-s26",
        "title": "Robert Koch ve Çağdaş Bakteriyolojinin Doğuşu",
        "content": "Alman hekim ve mikrobiyolog Robert Koch (1843-1910), bakteriyolojiyi spekülatif bir meraktan kesin bir deneysel bilime dönüştürmüştür (Sınav Spotu):\n\n- **Laboratuvar Yöntem Devrimleri:**\n  - **Katı Besiyeri:** Sıvı besiyerlerinde bakteriler birbirine karışırken, haşlanmış patates dilimi ve ardından **agar-agar** kullanarak tek bir bakteriden köken alan saf bakteri kolonilerini izole etmiştir.\n  - **Petri Kutusu:** Asistanı Julius Richard Petri ile birlikte mikrobiyoloji laboratuvarlarının vazgeçilmez cam kaplarını geliştirmiştir.\n  - **Anilin Boyaları:** Şeffaf bakterileri mikroskopta görünür kılmak için anilin boyaları ile boyama tekniklerini başlatmıştır.\n  - **Mikrofotografi:** Bakterilerin mikroskopik fotoğraflarını çekerek bilimsel kanıt standardını yükseltmiştir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Sıvı Besiyeri vs Katı Agar Besiyeri (Koch Devrimi)",
                "Sıvı Besiyeri Karışıklığı",
                "Farklı bakteri türleri tek bir kapta birbirine karışır; saf kültür elde etmek neredeyse imkansızdır.",
                "Katı Agar Besiyeri (Koch)",
                "Her bakteri yerinde sabit kalır ve bölünerek milyonlarca klonundan oluşan saf bir koloni oluşturur."
            ),
            make_cloze(
                "Robert Koch katı besiyerinde tek bir bakteriden çoğalan saf koloniler elde etmek için agar-agar maddesini mikrobiyolojiye kazandırmıştır.",
                "agar-agar",
                "Katı kültür ortamı hazırlamada kullanılan deniz yosunu polisakkariti"
            )
        ]
    })

    # Slide 27
    slides.append({
        "id": "k1-18-s27",
        "title": "Koch Postülatları: Nedensellik İspatının Dört Temel Kriteri",
        "content": "Bir mikroorganizmanın belirli bir hastalığın gerçek etkeni olduğunu kanıtlamak için Robert Koch tarafından formüle edilen 4 evrensel altın kural (Sınav Spotu):\n\n- **1. Postülat:** Şüpheli mikroorganizma, o hastalıktan muzdarip **tüm hastalarda bulunmalı**, sağlıklı bireylerde bulunmamalıdır.\n- **2. Postülat:** Mikroorganizma hastalıklı konaktan izole edilmeli ve laboratuvarda **saf kültür (pure culture)** halinde üretilmelidir.\n- **3. Postülat:** Bu saf kültürden alınan mikroorganizma duyarlı, sağlıklı bir deney hayvanına verildiğinde **aynı hastalığı yeniden oluşturmalıdır**.\n- **4. Postülat:** Deneysel olarak hastalandırılan bu hayvandan aynı mikroorganizma **yeniden izole edilmeli** ve orijinal etkenle aynı özellikleri göstermelidir.\n- **Önemi:** Tıp tarihinde nedensellik (kausasyon) ilişkisini bilimsel deneyle ispatlamanın temel metodolojisidir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Koch Postülatlarının Mantıksal Dört Basamağı",
                [
                    "1. Hastada Bulunma: Şüpheli mikrop tüm hasta dokularda gösterilir.",
                    "2. Saf Kültür: Bakteri hastadan alınıp petride tek başına saf üretilir.",
                    "3. Hayvanda Hastalık: Saf kültür sağlıklı deney hayvanına verilip aynı klinik tablo oluşturulur.",
                    "4. Yeniden İzolasyon: Hastalanan hayvandan aynı mikrop yeniden saf olarak üretilir."
                ]
            ),
            make_quiz(
                "Koch postülatlarına göre bir bakterinin belirli bir hastalığın kesin etkeni sayılabilmesi için saf kültürden alınan mikrobun sağlıklı bir deney hayvanına verildiğinde ne olması şarttır?",
                [
                    {"key": "A", "text": "Hayvanın derhal aşılanıp bağışık hale gelmesi", "isCorrect": False, "explanation": "Aşı koruma sağlar, hastalık oluşturmaz."},
                    {"key": "B", "text": "Aynı hastalığın deney hayvanında da birebir meydana gelmesi", "isCorrect": True, "explanation": "Doğru cevap B'dir: 3. postülat saf kültürün deney hayvanında aynı hastalığı oluşturmasını şart koşar."},
                    {"key": "C", "text": "Bakterinin anında kristalleşip yok olması", "isCorrect": False, "explanation": "Bilim dışıdır."},
                    {"key": "D", "text": "Hayvanın kan grubunun değişmesi", "isCorrect": False, "explanation": "İlgisizdir."}
                ]
            )
        ]
    })

    # Slide 28
    slides.append({
        "id": "k1-18-s28",
        "title": "Koch'un Keşifleri: Şarbon, Tüberküloz Basili (1882) ve Kolera (1883)",
        "content": "Robert Koch insanlık tarihinin en ölümcül üç bakteriyel hastalığının etkenini bizzat izole etmiştir (Sınav Spotu):\n\n- **1. Şarbon (Bacillus anthracis - 1876):**\n  - Şarbonun spor oluşturduğunu ve bu sporların toprakta yıllarca canlı kalarak hayvanlara bulaştığını kanıtlamıştır (bir mikroorganizmanın hastalık yaptığı ilk kanıt).\n- **2. Tüberküloz Basili (Mycobacterium tuberculosis - 24 Mart 1882):**\n  - Dönemin Avrupa'sında her 7 ölümden birinin sorumlusu olan tüberkülozun (verem) genetik veya lanet değil, bir basil tarafından oluşturulduğunu özel boyama ve kültürle gösterdi.\n  - 24 Mart günü günümüzde 'Dünya Tüberküloz Günü' olarak anılır. 1905 Nobel Tıp Ödülü'nü almıştır.\n- **3. Kolera Vibrionu (Vibrio cholerae - 1883):**\n  - Mısır ve Hindistan'a giderek kolera salgınlarında etken olan virgül biçimli bakteriyi izole etmiştir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Keşif Yılı", "Hastalık", "İzole Edilen Patojen", "Halk Sağlığı Etkisi"],
                [
                    ["1876", "Şarbon", "Bacillus anthracis", "Bakteri-hastalık ilişkisinin tarihteki ilk kesin ispatı"],
                    ["1882", "Tüberküloz (Verem)", "Mycobacterium tuberculosis (Koch Basili)", "Veremin bulaşıcı olduğunun ispatı ve sanatoryumların kurulması"],
                    ["1883", "Kolera", "Vibrio cholerae", "Su kaynaklarının klorlanması ve sanitasyon önlemlerinin başlaması"]
                ]
            ),
            make_cloze(
                "Robert Koch 1882 yılında tüberküloz basili Mycobacterium tuberculosis'i bularak veremin bulaşıcı bir bakteriyel enfeksiyon olduğunu kanıtlamıştır.",
                "tüberküloz",
                "Koch basili olarak da anılan ve 1882'de keşfedilen büyük akciğer hastalığı"
            )
        ]
    })

    # Slide 29 - CHECKPOINT 3
    slides.append({
        "id": "k1-18-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Mikrobiyolojik Devrim ve Germ Kuramı",
        "content": "Bu checkpointte mikrobiyolojinin ve bakteriyolojinin kuruluşunu özetliyoruz:\n\n- **Robert Hooke (1665):** Mantarda hücreleri ilk gören ve 'cell' adını veren bilim insanıdır.\n- **Leeuwenhoek (1675):** Mikroorganizmaları ('animalcules') hareket ederken ilk kez gören kişidir.\n- **Abiyogenezin Çöküşü:** Redi et kavanozlarıyla ilk darbeyi vurdu; Pasteur kuğu boyunlu balon deneyiyle kendiliğinden oluşu tamamen yıktı.\n- **Louis Pasteur:** Germ kuramını kurdu; fermentasyonu açıkladı; pastörizasyon yöntemini geliştirdi (süt tüberkülozu ve brusellayı önledi).\n- **Robert Koch:** Katı besiyeri (agar-agar) ve petri kutusunu geliştirdi; nedensellik ispatı için 4 Koch Postülatını koydu.\n- **Koch'un Keşifleri:** Şarbon sporları (1876), Tüberküloz basili (1882), Kolera vibrionu (1883).",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Öncü Bilim İnsanı", "Çalışma Yılları", "Tıbbi ve Halk Sağlığı Devrimi"],
                [
                    ["Robert Hooke", "1665", "'Hücre' (cell) kavramını literatüre kazandırdı"],
                    ["A. van Leeuwenhoek", "1675", "Canlı mikroorganizmaları ('animalcules') ilk kez mikroskopta gördü"],
                    ["Louis Pasteur", "1861-1885", "Abiyogenezi çürüttü, pastörizasyonu buldu, germ kuramını kurdu"],
                    ["Robert Koch", "1876-1883", "Agar besiyeri, Koch postülatları, Tüberküloz (1882) ve Kolera (1883) basili"]
                ]
            ),
            make_chain(
                "Mikrobiyolojinin Kuruluş Basamakları",
                [
                    "1. Mikroskop ve Gözlem: Leeuwenhoek ile mikroorganizmaların varlığı tescillenir.",
                    "2. Abiyogenezin Reddi: Pasteur kuğu boyunlu balonla mikropların havadan geldiğini kanıtlar.",
                    "3. Katı Besiyeri ve Saf Kültür: Koch tek bir bakteriyi izole ederek saf koloni üretir.",
                    "4. Etkenlerin Tespiti: Tüberküloz ve kolera basillerinin bulunmasıyla nedensellik tamamlanır."
                ]
            )
        ]
    })

    # Slide 30
    slides.append({
        "id": "k1-18-s30",
        "title": "Bölüm Özeti: Mikroorganizmalardan Bağışıklama ve Aşı Devrimine Geçiş",
        "content": "Bölüm 3 boyunca Leeuwenhoek'un ilk gözlemlerinden Pasteur ve Koch'un devrimsel keşiflerine uzanan mikrobiyolojik aydınlanmayı inceledik:\n\n- **Özet:** Mikroorganizmaların hastalık nedeni olduğu kanıtlandı; bu keşif halk sağlığında kör dövüşünü bitirdi ve hedefe yönelik koruma dönemini başlattı.\n- **Sonraki Bölüm (Bölüm 4):** İnsanlığın enfeksiyonlara karşı en büyük silahı olan **Bağışıklama Tarihçesini (Osmanlı çiçek aşılama geleneği ve variolasyon, Edward Jenner ve sığır çiçeği aşısı, Pasteur'ün kuduz aşısı, Behring'in difteri antitoksini ve BCG aşısı)** ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_recall(
                "Robert Koch'un 1882 yılında keşfettiği ve dönemin Avrupa'sında her yedi ölümden birine yol açan bakteriyel etken hangisidir?",
                "Tüberküloz basili (Mycobacterium tuberculosis)",
                "Koch basili olarak da bilinen verem etkeni"
            ),
            make_quiz(
                "Louis Pasteur'ün canlıların kendiliğinden oluşamayacağını (abiyogenezin imkansızlığını) kanıtlamak için tasarladığı ünlü deney düzeneği hangisidir?",
                [
                    {"key": "A", "text": "Kuğu boyunlu balon deneyi", "isCorrect": True, "explanation": "Doğru cevap A'dır: Kuğu boyunlu balon deneyi tozu tutarken havayı geçirmiş ve abiyogenezi çürütmüştür."},
                    {"key": "B", "text": "Çift kör plasebo deneyi", "isCorrect": False, "explanation": "Modern klinik ilaç araştırma yöntemidir."},
                    {"key": "C", "text": "Karanlık saha mikroskopisi", "isCorrect": False, "explanation": "Spiroket boyama yöntemidir."},
                    {"key": "D", "text": "Tüp torakostomi deneyi", "isCorrect": False, "explanation": "Cerrahi göğüs tüpü uygulamasıdır."}
                ]
            )
        ]
    })

    return slides
