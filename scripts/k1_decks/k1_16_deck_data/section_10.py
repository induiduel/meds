# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_10_slides():
    slides = []

    # Slide 91
    slides.append({
        "id": "k1-16-s91",
        "title": "Kan Kaybının Hacmi ve Hızı: %20 Kuralı ve Şok Eşiği",
        "content": "Bir kanamanın organizma üzerindeki klinik etkisi iki temel değişkene bağlıdır: kaybedilen kanın toplam hacmi ve bu kaybın hızı (Sınav Spotu):\n\n- **Toplam Kan Hacmi:** Sağlıklı bir yetişkinde vücut ağırlığının yaklaşık %7-8'i (ortalama 5 litre) kandır.\n- **%20 Kuralı (Fizyolojik Kompansasyon Sınırı):**\n  - Sağlıklı bir yetişkin, ani gelişen kan kaybında **toplam kan hacminin %20'sine kadar olan kayıpları (yaklaşık 750 - 1000 ml)** fizyolojik kompensasyon mekanizmalarıyla tolere edebilir.\n  - Sempatik aktivasyon, taşikardi, periferik vazokonstriksiyon ve sıvı kayması sayesinde tansiyon korunur.\n- **%20'nin Üzerinde Akut Kayıp:** Toplam kan hacminin %20'sinden fazlası hızla kaybedildiğinde venöz dönüş çöker, kardiyak dolum durur ve hasta **hemorajik (hipovolemik) şoka** girer; acil transfüzyon yapılmazsa ölüm kaçınılmazdır.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Akut <%20 Kan Kaybı vs >%20 Akut Kan Kaybı",
                "<%20 Kan Kaybı (Tolere Edilebilir)",
                "Sempatik sistem taşikardi ve vazokonstriksiyonla kan basıncını ve hayati organ akımını idame ettirir.",
                ">%20 Kan Kaybı (Hipovolemik Şok)",
                "Kompensasyon sınırları aşılır; hipotansiyon, doku hipoperfüzyonu, laktik asidoz ve şok gelişir."
            ),
            make_cloze(
                "Sağlıklı bir yetişkinde akut kan kaybında kompanse edilebilen ve tolere edilen maksimum oran toplam kan hacminin yüzde 20 kadarıdır.",
                "yüzde 20",
                "Akut tolere edilebilir maksimum kan kaybı yüzdesi"
            )
        ]
    })

    # Slide 92
    slides.append({
        "id": "k1-16-s92",
        "title": "Hızlı Kan Kaybı vs Yavaş Kan Kaybı Dinamikleri",
        "content": "Kanamanın zaman içindeki yayılım hızı vücudun uyum yeteneğini belirler:\n\n- **Akut (Hızlı) Masif Kanama:**\n  - Birkaç dakika içinde femoral arter yırtılması veya aort rüptürüyle 1500 ml kan kaybedilirse; kemik iliği eritrosit üretecek veya damarlar hacim toplayacak zaman bulamaz.\n  - Sonuç: Ağır hipotansiyon, kardiyovasküler kollaps ve ani ölüm.\n- **Kronik (Yavaş) Kanama:**\n  - Günde 10-20 ml gibi küçük miktarlarda aylar boyunca süren kanamalarda (ör. kolon kanseri veya peptik ülser) toplamda litrelerce kan kaybedilse bile hasta şoka girmez.\n  - Plazma hacmi böbreklerin su tutmasıyla korunur; kemik iliği eritropoietin uyarısıyla retikülositoz yapar ve eritrosit üretimini katlar.\n  - Sonuçta şok değil, derin bir **kronik anemi** tablosu oluşur.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Parametre", "Akut Hızlı Kan Kaybı", "Kronik Yavaş Kan Kaybı"],
                [
                    ["Kayıp Süresi", "Dakikalar - saatler içinde", "Haftalar - aylar boyunca"],
                    ["Hemodinamik Sonuç", "Hipovolemik şok ve kardiyovasküler kollaps", "Normovolemik derin kronik anemi"],
                    ["Kemik İliği Yanıtı", "Zaman yetersizliği nedeniyle yanıtsız", "Eritroid hiperplazi ve retikülosit artışı"],
                    ["Primer Klinik Belirti", "Hipotansiyon, taşikardi, soğuk terleme", "Halsizlik, solukluk, efor dispnesi"]
                ]
            ),
            make_quiz(
                "Aşağıdakilerden hangisi akut masif kanama ile kronik yavaş kanama arasındaki temel klinik farkı doğru açıklar?",
                [
                    {"key": "A", "text": "Akut hızlı kanamada temel tehdit hipovolemik şok iken; kronik yavaş kanamada temel klinik tablo kompanse anemidir", "isCorrect": True, "explanation": "Doğru cevap A'dır: Hızlı kayıplar hemodinamik şok yaratırken, yavaş kayıplarda plazma hacmi korunur ve anemi gelişir."},
                    {"key": "B", "text": "Kronik kanamada hasta dakikalar içinde şoka girer", "isCorrect": False, "explanation": "Kronik kanamada şok gelişmez."},
                    {"key": "C", "text": "Akut kanamada hemoglobin düzeyi anında sıfıra düşer", "isCorrect": False, "explanation": "Akut kanamada başlangıçta hemodilüsyon olmadan Hb normal bile çıkabilir."},
                    {"key": "D", "text": "Her iki durumda da hiçbir kompansasyon mekanizması çalışmaz", "isCorrect": False, "explanation": "Fizyolojik kompansasyonlar devreye girer."}
                ]
            )
        ]
    })

    # Slide 93
    slides.append({
        "id": "k1-16-s93",
        "title": "Kanama Lokalizasyonunun Önemi: Deri Altı vs Hayati Organlar",
        "content": "Kanamanın gerçekleştiği anatomik lokalizasyon, kanayan hacimden çok daha belirleyici olabilir (Sınav Spotu):\n\n- **Tolerans Alanı (Subkutan Doku / Kas İçi):**\n  - Uyluk kası içine veya deri altına 100-200 ml kan sızması yalnızca lokal bir şişlik, ağrı ve ekimoz yapar; hastanın genel durumunu veya yaşamsal fonksiyonlarını etkilemez.\n- **Sıfır Tolerans Alanları (Kapalı ve Kritik Alanlar):**\n  1. **Beyin Parankimi (İntraserebral Hemoraji):** Beyin sapında (pons) meydana gelen **yalnızca 5-10 ml'lik minik bir kanama**, solunum merkezini parçalayarak veya foramen magnum herniasyonuna yol açarak hastayı anında öldürebilir.\n  2. **Perikard Kesi (Hemoperikardiyum):** 150-250 ml kan kalbi sıkıştırarak (tamponad) diyastolik dolumu sıfırlar ve dakikalar içinde ölüme neden olur.\n  3. **Larinks / Trakea:** Az miktarda kanın hava yoluna dolması asfiksiye (boğulma) yol açar.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Subkutan Doku Kanaması vs Beyin Sapı Kanaması",
                "Subkutan 100 ml Kanama",
                "Deri altında geniş bir morluk (ekimoz) ve hafif ağrı oluşturur; hasta hayatını normal sürdürür.",
                "Beyin Sapı 5 ml Kanama",
                "Solunum ve kardiyak merkezleri ezer; kafa içi basıncı fırlatarak dakikalar içinde ölüme yol açar."
            ),
            make_quiz(
                "Deri altına sızan 100 ml'lik bir kanama hafif bir morlukla iyileşirken, beyin sapında meydana gelen yalnızca 5 ml'lik bir kanamanın hastayı öldürmesinin temel nedeni nedir?",
                [
                    {"key": "A", "text": "Beyindeki kanamanın pıhtılaşma faktörlerini tamamen yok etmesi", "isCorrect": False, "explanation": "Pıhtılaşma faktörleri sistemiktir."},
                    {"key": "B", "text": "Kafatasının esnemeyen kapalı bir kutu olması ve beyin sapındaki solunum/dolaşım merkezlerinin mekanik kompresyonla parçalanması", "isCorrect": True, "explanation": "Doğru cevap B'dir: Beyin sapı lokalizasyonu hayati merkezleri barındırır ve en ufak basınç artışı bile ölümcüldür."},
                    {"key": "C", "text": "Deri altındaki kanamanın mikrop üretmesi", "isCorrect": False, "explanation": "Deri altı hematom steril olabilir."},
                    {"key": "D", "text": "Beyin hücrelerinin eritrositleri düşman sanıp parçalaması", "isCorrect": False, "explanation": "Bilim dışı iddia."}
                ]
            )
        ]
    })

    # Slide 94
    slides.append({
        "id": "k1-16-s94",
        "title": "İntrakraniyal Kanamalar: Beyin Sapı ve Herniasyon Riski",
        "content": "Beyin içi kanamalar nörolojik morbidite ve mortalitenin en sık nedenlerindendir:\n\n- **1. İntraserebral (Parankimal) Kanama:** En sık kontrolsüz kronik sistemik hipertansiyona bağlı olarak bazal ganglionlar (putamen, talamus) ve beyin sapında Charcot-Bouchard mikroanevrizmalarının patlamasıyla gelişir.\n- **2. Subaraknoid Kanama:** En sık Willis poligonundaki sakküler (berry) anevrizma rüptürüyle gelişir; hasta hayatının en şiddetli baş ağrısını tarifler ('yıldırım baş ağrısı').\n- **Patolojik Yıkım:**\n  - Kanama beyin dokusunu yırtarak parankimde hematom oluşturur.\n  - Hematom çevre beyin dokusunda reaktif ödem yaratır; kafa içi basınç (KİBA) hızla fırlar.\n  - Beyin sapı mekanik olarak ezilir veya serebellar tonsiller foramen magnumdan aşağı fıtıklaşarak (tonsiller herniasyon) solunumu durdurur.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Hipertansif İntraserebral Kanama Basamakları",
                [
                    "1. Kronik Hipertansiyon: Bazal ganglion arteriyollerinde hiyalin arteriyoloskleroz gelişir.",
                    "2. Mikroanevrizma Rüptürü: Zayıflayan damar yüksek basınçla yırtılır (Charcot-Bouchard).",
                    "3. İntraparankimal Hematom: Kan beyin dokusunu parçalayarak kitle oluşturur.",
                    "4. Herniasyon ve Ölüm: KİBA artışı beyin sapını sıkıştırarak solunumu durdurur."
                ]
            ),
            make_cloze(
                "Hipertansif hastalarda bazal ganglionlarda ve beyin sapında küçük arteriyol yırtılmasıyla gelişen kanamalara intraserebral kanama denir.",
                "intraserebral",
                "Beyin parankimi içine olan kanamayı ifade eden tıbbi terim"
            )
        ]
    })

    # Slide 95
    slides.append({
        "id": "k1-16-s95",
        "title": "Dış Kanama vs İç Hematom Ayrımı ve Demir Homeostazı",
        "content": "Patolojide ve kurul sınavlarında en sık sorulan biyokimyasal ve hematolojik ayrımlardan biri kanamanın vücut içine mi yoksa dışına mı olduğudur (Sınav Spotu):\n\n- **1. Dış Kanama (External Hemorrhage):**\n  - Kanın vücut dışına aktığı durumlardır: Peptik ülser kanaması (hematemez, melena), aşırı menstrüasyon (menoraji), hemoroidal kanama, açık yara kanaması.\n  - Eritrositler vücuttan dışarı atıldığı için içlerindeki **demir (Fe) organizmadan tamamen kaybolur**.\n  - Tekrarlayan dış kanamalarda demir depoları tükenir ve **Demir Eksikliği Anemisi** gelişir.\n- **2. İç Hematom (Internal Hemorrhage):**\n  - Kanın doku planları veya kapalı vücut boşlukları içine aktığı durumlardır (ör. uyluk hematomu, hemotoraks, hemoperiton).\n  - Eritrositler dokudaki makrofajlar tarafından fagosite edilir; hemoglobin parçalanır ve serbest kalan demir apoferritin ile bağlanarak **vücut içinde geri kazanılır (recycle edilir)**.\n  - Bu nedenle **iç hematomlar kesinlikle demir eksikliği anemisine yol açmaz**.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Kronik Dış Kanama vs Büyük İç Hematom Demir Dengesi",
                "Kronik Dış Kanama (Mide Ülseri)",
                "Eritrositler dışkı/kusmukla atılır; demir kaybedilir; mutlaka Demir Eksikliği Anemisi gelişir.",
                "Büyük İç Hematom (Uyluk Hematomu)",
                "Eritrositler doku makrofajlarınca fagositozla sindirilir; demir geri kazanılır; demir eksikliği gelişmez."
            ),
            make_quiz(
                "Kronik peptik ülser kanaması olan bir hastada demir eksikliği anemisi gelişirken; uyluk kası içinde 500 ml hematomu olan bir hastada demir eksikliği anemisi gelişmemesinin nedeni nedir?",
                [
                    {"key": "A", "text": "Midede demir emiliminin durması, kasta ise demirin kendiliğinden çoğalması", "isCorrect": False, "explanation": "Demir kendiliğinden çoğalmaz."},
                    {"key": "B", "text": "İç hematomdaki eritrositlerin makrofajlarca parçalanarak demirin vücutça geri kazanılması, dış kanamada ise demirin vücuttan tamamen atılması", "isCorrect": True, "explanation": "Doğru cevap B'dir: İç hematomda demir makrofajlarca geri dönüştürülür (recycle), dış kanamada ise kaybolur."},
                    {"key": "C", "text": "Mide ülserinin kemik iliğini felç etmesi", "isCorrect": False, "explanation": "Ülser kemik iliğini felç etmez."},
                    {"key": "D", "text": "Uyluk kasının sürekli demir sentezlemesi", "isCorrect": False, "explanation": "Kas dokusu demir sentezlemez."}
                ]
            )
        ]
    })

    # Slide 96
    slides.append({
        "id": "k1-16-s96",
        "title": "Kronik Dış Kanama ve Demir Eksikliği Anemisinin Gelişimi",
        "content": "Kronik gizli dış kanamalar klinik hekimlikte en sık anemi nedenidir:\n\n- **Gizli Kan Kaybı (Occult Bleeding):**\n  - Kolon adenokarsinomu veya mide ülseri olan bir hastada gözle görülür kanama olmayabilir.\n  - Ancak her gün gaita ile 10-15 ml kan kaybedilir (gaitada gizli kan pozitifliği).\n- **Depoların Tükenmesi:**\n  - Vücudun günlük demir emilim kapasitesi (yaklaşık 1-2 mg) bu kaybı karşılayamaz.\n  - Önce karaciğer ve kemik iliğindeki ferritin depoları boşalır; ardından serum demiri düşer ve demir bağlama kapasitesi (TDBK) artar.\n- **Hematolojik Profil (Demir Eksikliği Anemisi):**\n  - Kemik iliği hemoglobin sentezleyemez; kana salınan eritrositler küçük (**mikrositer**) ve soluk (**hipokrom**) kalır.\n  - Hastada yorgunluk, efor dispnesi, tırnaklarda kaşık tırnak (koilonişi) ve dilde glossit gelişir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kronik Dış Kanamada Demir Eksikliği Anemisi Aşamaları",
                [
                    "1. Kronik Gizli Kanama: Peptik ülser veya kolon tümöründen düzenli eritrosit kaçağı.",
                    "2. Demir Depolarının Boşalması: Serum ferritin düzeyi kritik seviyenin altına iner.",
                    "3. Hemoglobin Sentez Kısıtlaması: Kemik iliğinde normoblastlar hemoglobin üretemez.",
                    "4. Mikrositer Hipokrom Anemi: Periferik yaymada küçük ve soluk eritrositler izlenir."
                ]
            ),
            make_cloze(
                "Kronik dış kanama sonucu vücut demir depolarının tükenmesiyle gelişen tabloya demir eksikliği anemisi denir.",
                "demir eksikliği anemisi",
                "Kronik kan kaybına bağlı gelişen en sık anemi türü"
            )
        ]
    })

    # Slide 97
    slides.append({
        "id": "k1-16-s97",
        "title": "İç Kanamalarda Demirin Geri Kazanımı ve Sarılık (İkter)",
        "content": "İç kanamalarda demir kaybı olmazken, ortaya çıkan aşırı bilirubin yükü farklı bir klinik bulgu yaratır (Sınav Spotu):\n\n- **Dev Hematomların Rezorpsiyonu:** Uyluk kası içi, retroperiton veya geniş plevral hemotoraks alanlarında yüzlerce mililitre kan göllenir.\n- **Masif Bilirubin Üretimi:**\n  - Doku makrofajları milyonlarca eritrositi hızla parçalar.\n  - Hem oksijenaz ve biliverdin redüktaz enzimleri devasa miktarda **indirekt (ankonjüge) bilirubin** üretir.\n- **Karaciğer Kapasitesinin Aşılması:**\n  - Kana dökülen bu yüksek miktardaki indirekt bilirubini karaciğer glukuronil transferaz enzimi ile hızla konjüge edip safraya atamaz.\n- **Sarılık (Prehepatik / Hemolitik İkter):**\n  - Hastanın skleralarında ve cildinde sararma (sarılık/ikter) gelişir.\n  - Laboratuvarda serum indirekt bilirubin düzeyi yükselir; ancak safra yolları veya karaciğer enzimleri normaldir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Küçük İç Kanama vs Masif İç Hematom Rezorpsiyonu",
                "Küçük Hematom",
                "Lokal makrofajlar pigmenti temizler; sistemik bilirubin yükselmez, sarılık oluşmaz.",
                "Masif İç Hematom (Rezorpsiyon Evresi)",
                "Aşırı hemoglobin yıkımı sonucu kana bol serbest bilirubin dökülür; hastada geçici sarılık (ikter) gelişir."
            ),
            make_quiz(
                "Büyük bir trafik kazası sonrası retroperitoneal geniş hematomu olan bir hastada 4 gün sonra skleralarda sararma ve serum indirekt bilirubin artışı saptanıyor. Neden nedir?",
                [
                    {"key": "A", "text": "Hematomdaki eritrositlerin makrofajlarca parçalanmasıyla açığa çıkan aşırı bilirubinin karaciğer konjugasyon kapasitesini aşması", "isCorrect": True, "explanation": "Doğru cevap A'dır: İç hematomun rezorpsiyonu sırasında yoğun hemoglobin yıkımı indirekt bilirubini artırarak geçici sarılık yapar."},
                    {"key": "B", "text": "Hastanın akut Hepatit A enfeksiyonu kapması", "isCorrect": False, "explanation": "Akut travma hematomu ile ilişkisizdir."},
                    {"key": "C", "text": "Safra kesesinin mekanik olarak tamamen yırtılması", "isCorrect": False, "explanation": "İzole retroperitoneal hematomda safra yırtığı şart değildir."},
                    {"key": "D", "text": "Böbreklerin idrar yerine safra üretmesi", "isCorrect": False, "explanation": "Böbrekler safra üretmez."}
                ]
            )
        ]
    })

    # Slide 98
    slides.append({
        "id": "k1-16-s98",
        "title": "Hemoraji, Şok ve Hemodinamik Dekompansasyonun Yönetimi",
        "content": "Ağır kanama kontrol altına alınamazsa dolaşım sistemi geri dönüşümsüz şok evresine ilerler:\n\n- **Hemorajik Şok Evreleri:**\n  1. **Non-progresif (Kompensatuvar) Evre:** Nörohümoral mekanizmalar (sempatik aktivasyon, katekolaminler, RAAS, ADH) taşikardi ve periferik vazokonstriksiyon ile hayati organların (beyin ve kalp) perfüzyonunu korur.\n  2. **Progresif Evre:** Doku hipoperfüzyonu derinleşir; anaerobik glikoliz başlar; laktik asidoz gelişir; arterioller asidozla gevşer ve kan göllenir.\n  3. **İrreversibl (Geri Dönüşümsüz) Evre:** Hücre ölümü yaygınlaşır; barsak iskemisiyle endotoksinler kana sızar; çoklu organ yetmezliği (MODS) ve ölüm gelişir.\n- **Tedavinin Patofizyolojik Temeli:** Kanamayı cerrahi/mekanik olarak durdurmak, kristalloid ve eritrosit süspansiyonu ile damar içi hacmi ve oksijen taşıma kapasitesini hızla yerine koymaktır.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Hemorajik Şokun Evreleri ve Gidişatı",
                [
                    "1. Masif Kan Kaybı: Damar içi efektif dolaşan kan hacmi kritik eşiğin altına iner.",
                    "2. Kompensasyon: Taşikardi ve vazokonstriksiyon kan basıncını geçici olarak tutar.",
                    "3. Progresif Doku İskemisi: Laktik asidoz ve vazomotor felç perfüzyonu tamamen çökertir.",
                    "4. İrreversibl Hücre Ölümü: Çoklu organ yetmezliğiyle tablo geri dönüşümsüzleşir."
                ]
            ),
            make_cloze(
                "Ağır kanamada kan basıncının düşmesi ve dokulara yetersiz perfüzyonla seyreden hayatı tehdit eden dolaşım çöküşüne hipovolemik şok denir.",
                "hipovolemik şok",
                "Kan ve sıvı kaybına bağlı gelişen akut dolaşım yetmezliği"
            )
        ]
    })

    # Slide 99
    slides.append({
        "id": "k1-16-s99",
        "title": "Entegre Klinik Vaka: Kalp Yetmezliği, Siroz ve Hemoraji Sentezi",
        "content": "Hemodinamik dengenin bozulduğu klinik bir olgu üzerinden dersin tüm kazanımlarını birleştiriyoruz:\n\n- **Vaka:** 62 yaşında kronik alkol kullanımı ve iskemik kalp yetmezliği öyküsü olan erkek hasta acil servise nefes darlığı, bacaklarda aşırı şişlik ve karında belirgin distansiyon ile getiriliyor:\n- **Bulguların Patofizyolojik Açıklaması:**\n  1. **Akciğerde Yaş Raller ve Dispne:** Sol kalp yetmezliğine bağlı pulmoner konjesyon ve alveoler **transuda ödemi**.\n  2. **Bilateral Pretibial Gode Bırakan Ödem:** Sağ kalp yetmezliği ve sekonder hiperaldosteronizme bağlı **artmış sistemik venöz hidrostatik basınç**.\n  3. **Masif Karın Şişliği (Asit):** Siroza bağlı portal hipertansiyon (hidrostatik ↑) ve karaciğerin albümin üretememesi (**azalmış onkotik basınç**) kombinasyonu.\n  4. **Kollarda Yaygın Ekimozlar:** Karaciğer yetmezliğine bağlı **koagülasyon faktör sentez kusuru** ve hipersplenizme bağlı hafif trombositopeni.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Klinik Karar: Bu Hastada Asit ve Ödemin Patofizyolojik Analizi",
                "Bu hastadaki karın sıvısı (asit) ve bacak ödeminin patofizyolojisi hakkında hekimler arası konseyle hangisi en doğru değerlendirmedir?",
                [
                    {
                        "text": "Hastada kesinlikle bakteriyel peritonit vardır, sıvı yüksek proteinli eksudadır ve acil ameliyat gerekir.",
                        "outcome": "Hatalı analiz: Siroz ve kalp yetmezliğindeki asit öncelikle hemodinamik transudadır, enfeksiyon kanıtı olmadan eksuda denemez.",
                        "isCorrect": False
                    },
                    {
                        "text": "Kardiyak hidrostatik basınç artışı ile sirotik hipoalbüminemi ve portal hipertansiyonun birleştiği miks bir hemodinamik dekompansasyondur; sıvı transuda karakterindedir.",
                        "outcome": "Kusursuz patolojik muhakeme: Hemodinamik faktörler, Starling dengesi ve karaciğer sentez yetmezliği tam bir sentezle açıklanmıştır.",
                        "isCorrect": True
                    },
                    {
                        "text": "Hastanın ödemi sadece fazla su içmesinden kaynaklanmaktadır, ilaçsız kendiliğinden geçer.",
                        "outcome": "Hayati tehlike yaratan ihmal.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu vakada hastanın cildinde kolayca morluklar (ekimoz) oluşmasının karaciğer patolojisiyle doğrudan ilişkili temel nedeni hangisidir?",
                [
                    {"key": "A", "text": "Karaciğer parankim hasarı nedeniyle pıhtılaşma faktörlerinin (Faktör II, VII, IX, X vb.) sentezinin çökmesi", "isCorrect": True, "explanation": "Doğru cevap A'dır: Karaciğer neredeyse tüm koagülasyon faktörlerini üretir; yetmezliğinde faktör sentezi çöker ve kanama eğilimi doğar."},
                    {"key": "B", "text": "Hastanın kemiklerinin eriyip deriyi delmesi", "isCorrect": False, "explanation": "Kemik erimesi doğrudan ekimoz yapmaz."},
                    {"key": "C", "text": "Karaciğerin aşırı eritrosit üretip damarları patlatması", "isCorrect": False, "explanation": "Karaciğer erişkinde eritrosit üretmez."},
                    {"key": "D", "text": "Tüm lenf nodlarının birden yok olması", "isCorrect": False, "explanation": "Lenf nodları yok olmaz."}
                ]
            )
        ]
    })

    # Slide 100 - CHECKPOINT 10
    slides.append({
        "id": "k1-16-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Kurul 1 Entegre Klinik ve Patoloji Özeti",
        "content": "Kurul 1 Ders 16'nın büyük final tekrarında tüm hemodinamik ilkeleri ve sınav spotlarını özetliyoruz:\n\n- **Hiperemi vs Konjesyon:** Hiperemi aktif, arteriyel, kırmızı ve sıcaktır; konjesyon pasif, venöz drenaj kusuru, siyanotik ve soğuktur.\n- **Organ Konjesyonları:** Kronik akciğer konjesyonunda 'kalp yetmezliği hücreleri' (siderofajlar) ve 'kahverengi endürasyon'; karaciğerde sentrilobüler nekroz ve 'muskat karaciğeri' (nutmeg liver).\n- **Ödemin 5 Mekanizması:** Hidrostatik ↑ (KKY, DVT), Onkotik ↓ (Nefrotik, siroz, kwashiorkor), Lenfatik obstrüksiyon (Peau d'orange, filaryazis), Na/su retansiyonu (Böbrek yetmezliği), Geçirgenlik ↑ (Enflamatuvar eksuda).\n- **Ödem Morfolojisi:** Akciğerde köpüklü pembe sıvı; beyinde düzleşmiş giruslar ve ölümcül foramen magnum tonsiller herniasyonu.\n- **Kanama Boyutları:** Peteşi (1-2 mm), Purpura (3-5 mm - vaskülitte palpabl), Ekimoz (1-2 cm - hemoglobin $\\to$ bilirubin $\\to$ hemosiderin renk döngüsü).\n- **Kanama Kliniği:** Akut %20'ye kadar kayıp tolere edilir; beyin sapında 5 ml ölümcüldür; dış kanama demir eksikliği anemisi yaparken iç hematom demir eksikliği yapmaz.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Patolojik Süreç", "Anahtar Hücresel / Morfolojik Bulgu", "Klinik Yansıması"],
                [
                    ["Kronik Akciğer Konjesyonu", "Hemosiderin yüklü makrofajlar ('Kalp yetmezliği hücreleri')", "Sol ventrikül yetmezliğinde kahverengi endürasyon"],
                    ["Kronik Karaciğer Konjesyonu", "Lobül merkezi nekroz, perifer yağlanma ('Muskat karaciğeri')", "Sağ ventrikül yetmezliğinde kardiyak siroz"],
                    ["Nefrotik Sendrom", "Masif proteinüri ve ağır hipoalbüminemi", "Sabah periorbital ödem ve anasarka"],
                    ["Meme Kanseri", "Subdermal lenfatik infiltrasyon", "Meme cildinde 'Peau d'orange' (portakal kabuğu)"],
                    ["Beyin Ödemi", "Düzleşmiş giruslar, silinmiş sulkuslar", "Foramen magnumdan tonsiller herniasyon ve ani ölüm"],
                    ["Ekimoz Renk Evrimi", "Hemoglobin (mor) $\\to$ Bilirubin (yeşil) $\\to$ Hemosiderin (sarı)", "Adli tıpta travma gününün tayini"]
                ]
            ),
            make_chain(
                "Hemodinamik Bozukluklar Kurul 1 Büyük Akış Şeması",
                [
                    "1. Starling Dengesi: Hidrostatik itme ve onkotik çekme kuvvetleri.",
                    "2. Dengesizlik Sonucu: Transuda kaçışı ile dokuda ödem ve boşlukta efüzyon.",
                    "3. Vasküler Göllenme: Aktif arteriyel hiperemi vs Pasif venöz konjesyon.",
                    "4. Organ Hasarı: Alveolde siderofajlar, karaciğerde muskat görünümü.",
                    "5. Damar Dışına Kanama: Peteşi (1-2 mm), purpura (3-5 mm), ekimoz (1-2 cm).",
                    "6. Hayati Sonuç: %20 akut kayıpla şok; iç hematomda demir korunurken dış kanamada anemi."
                ]
            )
        ]
    })

    return slides
