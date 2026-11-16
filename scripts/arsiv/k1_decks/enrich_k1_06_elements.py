#!/usr/bin/env python3
"""Comprehensive Enrichment Elements Generator for k1-06 Deck"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.k1_06_deck_data.helpers import (
    make_micro_quiz, make_branching_logic, make_causal_chain,
    make_before_after, make_active_recall, make_cloze, make_table
)

def get_21_quizzes():
    # Slots: 2, 5, 8, 11, 14, 18, 22, 28, 32, 36, 38, 42, 44, 52, 58, 64, 72, 78, 84, 92, 96
    return {
        2: make_micro_quiz(
            "Anne Ölüm Oranı (MMR) hesaplanırken formülün paydasında kullanılan demografik veri hangisidir?",
            {"A": "Toplam nüfus", "B": "15-49 yaş kadın nüfusu", "C": "Canlı doğum sayısı", "D": "Toplam gebe sayısı", "E": "Hastane doğum sayısı"},
            "C",
            {"A": "Toplam nüfus kaba ölüm hızında kullanılır.", "B": "Anne ölüm hızında (rate) kullanılır.", "C": "Doğru cevap C'dir: MMR paydada daima canlı doğum sayısını alır ve 100.000 ile çarpılır.", "D": "Kayıt dışı gebelikler bilinemez.", "E": "Ev doğumlarını dışlar."}
        ),
        5: make_micro_quiz(
            "DSÖ verilerine göre 2020 yılında kaydedilen küresel anne ölümlerinin yaklaşık yüzde kaçı düşük ve alt-orta gelirli ülkelerde gerçekleşmiştir?",
            {"A": "%50", "B": "%70", "C": "%85", "D": "%95", "E": "%99"},
            "D",
            {"A": "Çok düşüktür.", "B": "Eksiktir.", "C": "Gerçek oranın gerisindedir.", "D": "Doğru cevap D'dir: Küresel anne ölümlerinin yaklaşık %95'i düşük ve orta gelirli ülkelerde yığılmıştır.", "E": "Gelişmiş ülkelerde de nadir ölümler mevcuttur."}
        ),
        8: make_micro_quiz(
            "TÜİK verilerine göre Türkiye'de 15-19 yaş adölesan doğurganlık hızı 2001'den 2023'e nasıl bir seyir izlemiştir?",
            {"A": "Binde 49'dan binde 11'e gerilemiştir", "B": "Binde 100'den binde 50'ye inmiştir", "C": "Binde 25'te sabit kalmıştır", "D": "Binde 15'ten binde 35'e tırmanmıştır", "E": "Binde 70'ten binde 4'e düşmüştür"},
            "A",
            {"A": "Doğru cevap A'dır: TÜİK verilerine göre adölesan doğurganlık hızı 2001'de binde 49 iken 2023'te binde 11'e inmiştir.", "B": "Gerçek dışıdır.", "C": "Düşüş vardır.", "D": "Tırmanış değil düşüş yaşanmıştır.", "E": "Binde 4 aşırı abartılıdır."}
        ),
        11: make_micro_quiz(
            "Tüm dünyada doğrudan obstetrik nedenli anne ölümlerinin bir numaralı tekil sebebi hangisidir?",
            {"A": "Puerperal sepsis", "B": "Şiddetli postpartum kanama", "C": "Eklampsi", "D": "Tıkalı travay", "E": "Amniyotik sıvı embolisi"},
            "B",
            {"A": "İkinci sıradadır.", "B": "Doğru cevap B'dir: Şiddetli doğum sonu kanama (özellikle uterin atoni) anne ölümlerinin %27'si ile bir numaralı sebeptir.", "C": "Yaklaşık %14 paya sahiptir.", "D": "Önemli bir sebeptir ancak birinci değildir.", "E": "Nadir fatal bir tablodur."}
        ),
        14: make_micro_quiz(
            "Preeklampsi tablosunda eklamptik jeneralize konvülsiyonların önlenmesi ve tedavisinde ilk tercih edilen ilaç hangisidir?",
            {"A": "Diazepam", "B": "Fenitoin", "C": "Magnezyum sülfat", "D": "Metildopa", "E": "Furosemid"},
            "C",
            {"A": "İlk tercih değildir.", "B": "Eklampside etkisizdir.", "C": "Doğru cevap C'dir: Magnezyum sülfat serebral vazospazmı çözen ve membranları stabilize eden altın standarttır.", "D": "Kronik tansiyon ilacıdır.", "E": "Diüretikler hipovolemiyi artırır."}
        ),
        18: make_micro_quiz(
            "Dünya Sağlık Örgütü'ne göre kadınların doğum bakımı almasını engelleyen faktörler arasında aşağıdakilerden hangisi YER ALMAZ?",
            {"A": "Yoksulluk ve ekonomik engeller", "B": "Sağlık tesislerine uzaklık", "C": "Toplumsal sağlık eğitimi", "D": "Kültürel inançlar ve geleneksel engeller", "E": "Sağlık hizmetlerinin kalitesizliği"},
            "C",
            {"A": "Yoksulluk temel engeldir.", "B": "Mesafe ve ulaşım ana engeldir.", "C": "Doğru cevap C'dir: Sağlık eğitimi bir engel değil; bakıma erişimi artıran ve hayat kurtaran temel çözümdür.", "D": "Karar vermeyi geciktirir.", "E": "Hizmet zaafiyetidir."}
        ),
        22: make_micro_quiz(
            "Gebelikte plazma hacmi artışının alyuvar artışından fazla olması sonucu ortaya çıkan fizyolojik tablonun laboratuvar karşılığı nedir?",
            {"A": "Fizyolojik lökositoz", "B": "Fizyolojik hemodilüsyon (2. trimestr Hb < 10,5 g/dl anemi sınırı)", "C": "Trombositopenik purpura", "D": "Mutlak polisitemi", "E": "Hemolitik üremik sendrom"},
            "B",
            {"A": "Lökositoz hücresel artımdır.", "B": "Doğru cevap B'dir: Plazma %50 artarken alyuvar %20-30 artar; bu hemodilüsyon 2. trimestrde anemi sınırını 10,5 g/dl'ye çeker.", "C": "Otoimmün yıkımdır.", "D": "Polisitemi kan koyulaşmasıdır.", "E": "Mikroanjiyopatidir."}
        ),
        28: make_micro_quiz(
            "İntrauterin malnütrisyonun erişkinlikte koroner kalp hastalığı ve Tip 2 diyabet riskini kalıcı olarak artırdığını savunan hipotezin kurucusu kimdir?",
            {"A": "David Barker", "B": "Hans Selye", "C": "Rudolf Virchow", "D": "Ignaz Semmelweis", "E": "Alexander Fleming"},
            "A",
            {"A": "Doğru cevap A'dır: Fetal programlama hipotezini David Barker ortaya koymuştur.", "B": "Stres araştırmacısıdır.", "C": "Hücresel patologdur.", "D": "El hijyeni öncüsüdür.", "E": "Penisilini bulmuştur."}
        ),
        32: make_micro_quiz(
            "Anne beslenmesini olumsuz etkileyen ve riskli gebelik olarak tanımlanan obstetrik ve demografik özellikler arasında hangisi yer alır?",
            {"A": "25-30 yaş arası olmak", "B": "Üniversite mezunu olmak", "C": "Doğum sayısının 4 ve üzeri olması", "D": "Hafif tempolu yürüyüş yapmak", "E": "Tekil gebelik taşımak"},
            "C",
            {"A": "İdeal üreme yaşıdır.", "B": "Sağlık bilincini artırır.", "C": "Doğru cevap C'dir: 4 ve üzeri doğum (büyük multiparite) maternal depoları tüketerek malnütrisyon riskini katlar.", "D": "Faydalı bir aktivitedir.", "E": "Standart durumdur."}
        ),
        36: make_micro_quiz(
            "Gebelikte aşırı beslenen ve gestasyonel diyabet gelişen annenin bebeğinde doğumdan hemen sonra hipoglisemi gelişmesinin temel patofizyolojik nedeni nedir?",
            {"A": "Fetal glukagon yetersizliği", "B": "İntrauterin hiperglisemiye yanıt olarak gelişen fetal hiperinsülinizmin kord kesildikten sonra şekeri hızla tüketmesi", "C": "Annenin insülininin plasentadan bebeğe geçmesi", "D": "Bebekte adrenal bez yetmezliği", "E": "Fetal glukoz-6-fosfataz enzim eksikliği"},
            "B",
            {"A": "Glukagon ikincildir.", "B": "Doğru cevap B'dir: Anne şekeri kesilince kanda yüksek kalan fetal insülin mevcut glukozu hızla tüketerek hipoglisemi nöbeti yapar.", "C": "Maternal insülin plasentayı kesinlikle geçemez.", "D": "Adrenal patoloji değildir.", "E": "Glikojen depo hastalığıdır."}
        ),
        38: make_micro_quiz(
            "Gebelikte aşırı kalori alımı ve kontrolsüz kilo kazanımının en sık yol açtığı maternal ve fetal komplikasyon çifti hangisidir?",
            {"A": "Osteomalazi - Düşük doğum ağırlığı", "B": "Gestasyonel diyabet - Fetal makrozomi", "C": "Megaloblastik anemi - Spina bifida", "D": "Kretenizm - Fetal hidrosefali", "E": "Uterin atoni - Konjenital katarakt"},
            "B",
            {"A": "Yetersiz beslenme sonucudur.", "B": "Doğru cevap B'dir: Aşırı beslenme annede gestasyonel diyabete, bebekte ise fetal hiperinsülinizmle makrozomiye yol açar.", "C": "Folat/B12 eksikliğidir.", "D": "İyot eksikliğidir.", "E": "Alakasız tablodur."}
        ),
        42: make_micro_quiz(
            "Gebelik öncesi normal beden kitle indeksine (BKİ: 20,0 - 24,9 kg/m²) sahip bir kadında tüm gebelik boyunca önerilen toplam ağırlık artışı ne kadardır?",
            {"A": "5,0 - 7,0 kg", "B": "7,0 - 11,5 kg", "C": "11,5 - 16,0 kg", "D": "18,0 - 22,0 kg", "E": "En az 25 kg"},
            "C",
            {"A": "Çok yetersizdir.", "B": "Fazla kiloluların hedefidir.", "C": "Doğru cevap C'dir: Normal kilolu kadınlar için önerilen sağlıklı kilo artış koridoru 11,5-16,0 kg'dır.", "D": "Çoğul gebelik aralığıdır.", "E": "Aşırı obezite riskidir."}
        ),
        44: make_micro_quiz(
            "Gebelik öncesi BKİ değeri 30 ve üzerinde olan obez bir gebe kadında tüm gebelik boyunca önerilen ağırlık artışı hedefi nedir?",
            {"A": "Kilo almamalı ve 5 kilo vermelidir", "B": "En az 6,0 kg ağırlık artışı hedeflenmelidir", "C": "11,5 - 16,0 kg almalıdır", "D": "20 - 25 kg almalıdır", "E": "Sadece 1-2 kg almalıdır"},
            "B",
            {"A": "Gebelikte zayıflama diyeti ketozis riski nedeniyle kontrendikedir.", "B": "Doğru cevap B'dir: Obez gebelerde (BKİ ≥30) önerilen ağırlık artışı en az 6,0 kg'dır (IOM aralığı 5-9 kg).", "C": "Normal kiloluların hedefidir.", "D": "Tehlikeli aşırı artımdır.", "E": "Fetal ünite ağırlığına dahi yetmez."}
        ),
        52: make_micro_quiz(
            "Fetal beyin korteksi ve retina fotoreseptör tabakasının gelişimi için zorunlu olan ve kuru beyin ağırlığının %50-60'ını oluşturan n-3 yağ asidi hangisidir?",
            {"A": "Araşidonik asit", "B": "Oleik asit", "C": "Dokosahekzaenoik asit (DHA)", "D": "Palmitik asit", "E": "Bütirik asit"},
            "C",
            {"A": "n-6 serisindedir.", "B": "Zeytinyağı asididir.", "C": "Doğru cevap C'dir: DHA (n-3) fetal beyin nörogenezi ve görme keskinliği için en kritik yağ asididir.", "D": "Doymuş yağdır.", "E": "Kısa zincirlidir."}
        ),
        58: make_micro_quiz(
            "Gebelikte iyot eksikliğinin fetüs üzerinde yol açtığı ve önlenebilir zeka geriliğinin en sık sebebi olan klinik tablo hangisidir?",
            {"A": "Spina bifida", "B": "Kretenizm", "C": "Fetal alkol sendromu", "D": "Fenilketonüri", "E": "Galaktozemi"},
            "B",
            {"A": "Folik asit eksikliğindedir.", "B": "Doğru cevap B'dir: İyot eksikliği fetüste kretenizm, sağırlık, cücelik ve derin mental retardasyon yapar.", "C": "Alkol teratojenitesidir.", "D": "Enzim kusurudur.", "E": "Karbonhidrat metabolizma bozukluğudur."}
        ),
        64: make_micro_quiz(
            "Gebelikte hem gelişmiş hem de gelişmekte olan ülkelerde en sık görülen tekil mikronütrient beslenme yetersizliği hangisidir?",
            {"A": "B12 vitamini eksikliği", "B": "Demir eksikliği anemisi", "C": "D vitamini eksikliği", "D": "Çinko eksikliği", "E": "Folat eksikliği"},
            "B",
            {"A": "Vejetaryenlerde sıktır.", "B": "Doğru cevap B'dir: Demir eksikliği anemisi gebelikte dünyada ve Türkiye'de en sık görülen nutrisyonel yetersizliktir.", "C": "İkincil sıklıktadır.", "D": "Nadir değildir ama anemi daha sıktır.", "E": "Profilaksiyle önlenir."}
        ),
        72: make_micro_quiz(
            "T.C. Sağlık Bakanlığı'nın Gebelere Demir Destek Programı kapsamında uygulanan profilaksi takvimi ve dozu hangisinde doğru verilmiştir?",
            {"A": "12. haftadan doğuma kadar - günlük 20 mg", "B": "16. haftadan doğum sonu 3. aya kadar (toplam 9 ay) - günlük 40-60 mg elementer demir", "C": "İlk 3 ay boyunca - günlük 100 mg", "D": "Doğum sonu 6 ay boyunca - günlük 10 mg", "E": "24. haftadan doğuma kadar - günlük 200 mg"},
            "B",
            {"A": "D vitamini takvimidir.", "B": "Doğru cevap B'dir: 16. haftadan başlayıp lohusalık 3. aya kadar (toplam 9 ay) günlük 40-60 mg elementer demir verilir.", "C": "İlk 3 ayda verilmez.", "D": "Eksik süredir.", "E": "Profilaksi değil tedavi dozudur."}
        ),
        78: make_micro_quiz(
            "T.C. Sağlık Bakanlığı'nın gebe destek programına göre D vitamini desteği hangi haftada başlar ve günlük önerilen doz kaç IU'dur?",
            {"A": "16. hafta - 400 IU", "B": "12. hafta - 1200 IU", "C": "Gebe kalmadan 3 ay önce - 2000 IU", "D": "24. hafta - 800 IU", "E": "Doğumdan hemen sonra - 5000 IU"},
            "B",
            {"A": "Demir haftasıdır.", "B": "Doğru cevap B'dir: D vitamini desteği 12. haftada başlar ve doğum sonu 6. aya kadar günlük 1200 IU (9 damla) verilir.", "C": "Folik asit zamanlamasıdır.", "D": "Geç haftadır.", "E": "Toksik dozdur."}
        ),
        84: make_micro_quiz(
            "Gebelikte son trimestrde sıklaşan mide yanması ve gastroözofageal reflü yakınmalarını önlemede hangisi DOĞRU bir yaşam tarzı tavsiyesidir?",
            {"A": "Yemeklerden hemen sonra sırtüstü uzanıp dinlenmek", "B": "Günde iki büyük ağır öğün yemek", "C": "Yemekten hemen sonra yatmamak ve yatak başını yüksekte tutarak uyumak", "D": "Yemeklerle birlikte bol asitli meyve suları içmek", "E": "Gece yatmadan hemen önce bol yağlı sütlü tatlı tüketmek"},
            "C",
            {"A": "Asit kaçışını artırır.", "B": "Mide gerginliğini artırır.", "C": "Doğru cevap C'dir: Yemekten sonra uzanmamak, az-sık yemek ve başı yüksekte uyumak yerçekimi bariyerini korur.", "D": "Mideyi tahriş eder.", "E": "Reflüyü şiddetlendirir."}
        ),
        92: make_micro_quiz(
            "Emziren bir annede günlük enerji alımının hangi eşiğin altına düşmesi anne sütü miktarını doğrudan ve belirgin şekilde azaltır?",
            {"A": "Günlük 2500 kalori", "B": "Günlük 2200 kalori", "C": "Günlük 1800 kalori", "D": "Günlük 1200 kalori", "E": "Günlük 3000 kalori"},
            "C",
            {"A": "Normal hedeftir.", "B": "Sütü azaltmaz.", "C": "Doğru cevap C'dir: Günlük 1800 kalorinin altına inildiğinde prolaktin sentezi ve süt hacmi dramatik biçimde düşer.", "D": "Açlık sınırıdır.", "E": "Gereksiz fazladır."}
        ),
        96: make_micro_quiz(
            "Gebelikte pastörize edilmemiş süt, taze/küflü peynirler ve işlenmiş soğuk etlerin tüketilmesinin yasaklanmasına yol açan en ölümcül bakteriyel patojen hangisidir?",
            {"A": "Listeria monocytogenes", "B": "Helicobacter pylori", "C": "Streptococcus pneumoniae", "D": "Mycobacterium leprae", "E": "Vibrio cholerae"},
            "A",
            {"A": "Doğru cevap A'dır: Listeria soğukta üreyen, pastörize edilmemiş sütten bulaşan ve fetüste ölü doğum yapan bakteridir.", "B": "Ülser yapar.", "C": "Zatürre yapar.", "D": "Lepra yapar.", "E": "Kolera yapar."}
        )
    }

def get_21_chains():
    # Slots: 3, 6, 10, 16, 17, 21, 26, 27, 31, 37, 41, 46, 47, 51, 56, 57, 61, 66, 67, 76, 77
    return {
        3: make_causal_chain(
            "DSÖ Küresel Anne Ölümü İlerleme Zinciri",
            [
                "1. Küresel Seferberlik: Milenyum Kalkınma Hedefleri ile anne ölümlerine odaklanıldı.",
                "2. Kurumsal Doğum Artışı: Doğumların sağlık merkezlerinde yapılması teşvik edildi.",
                "3. Yüzde 34 Düşüş: 2000-2020 arasında küresel MMR oranında üçte birlik gerileme sağlandı.",
                "4. 287.000 Kayıp Bilanço: İlerlemeye rağmen 2020'de yıllık 287.000 anne hayatını kaybetti.",
                "5. 2030 SKA Hedefi: Küresel MMR'nin 70'in altına çekilmesi için acil yatırımlar sürmektedir."
            ]
        ),
        6: make_causal_chain(
            "Adolesan Gebelikte Komplikasyon Gelişim Zinciri",
            [
                "1. Erken Yaşta Gebelik: 10-19 yaşındaki genç kız kemik çatısı olgunlaşmadan gebe kalır.",
                "2. Pelvik Darlık: Dar doğum kanalı fetal başın ilerlemesini mekanik olarak bloke eder.",
                "3. Obstrüktif Travay: Doğum eylemi günlerce ilerleyemez; uterus alt segmenti aşırı gerilir.",
                "4. İskemik Nekroz: Fetal başın simfizis pubise uzun basısı vajinal dokularda nekroz yapar.",
                "5. Obstetrik Fistül: Mesane-vajina duvarı delinerek kalıcı idrar inkontinansı ve dışlanma oluşur."
            ]
        ),
        10: make_causal_chain(
            "Vasıflı Ebe ile Hayat Kurtarma Zinciri",
            [
                "1. Doğum Eylemi Takibi: Vasıflı ebe partograf kullanarak travayın ilerlemesini izler.",
                "2. Erken Teşhis: Başın ilerlemediğini veya kalp seslerinin bozulduğunu ilk anda saptar.",
                "3. Profilaktik Oksitosin: Doğumun üçüncü evresinde rutin uterotonik yaparak kanamayı önler.",
                "4. Zamanında Sevk: Cerrahi ihtiyaçta hastayı donanımlı ameliyathaneye gecikmeden ulaştırır.",
                "5. Maternal Sağkalım: Basit koruyucu adımlarla önlenebilir anne ölümleri sıfırlanır."
            ]
        ),
        16: make_causal_chain(
            "Güvenli Olmayan Kürtajda Perforasyon ve Sepsis Zinciri",
            [
                "1. Yasadışı Girişim: İstenmeyen gebelik tıbbi standarttan yoksun ortamda ehil olmayan ellerce tahliye edilir.",
                "2. Uterin Perforasyon: Keskin aletler myometriyumu delerek periton boşluğuna ve bağırsağa girer.",
                "3. Masif Kanama ve Bulaş: Uterin damar yırtılmasıyla iç kanama ve bağırsak florası sızıntısı başlar.",
                "4. Fulminan Peritonit: Clostridium ve anaerop bakteriler yaygın pelvik gangren üretir.",
                "5. Septik Şok ve Ölüm: Zamanında cerrahi drenaj ve antibiyotik verilmezse saatler içinde anne kaybedilir."
            ]
        ),
        17: make_causal_chain(
            "Uterin Atoniye Bağlı Postpartum Kanama Mekanizması",
            [
                "1. Plasental Ayrılma: Doğumda plasenta ayrılarak devasa spiral arter ağızlarını açığa çıkarır.",
                "2. Miyometriyal Yetersizlik: Rahim kas lifleri yorgunluk nedeniyle güçlü kasılamaz.",
                "3. Açık Damar Ağızları: 'Canlı ligatür' mekanizması çalışmadığı için dakikada 600 ml kan fışkırır.",
                "4. Hipovolemik Şok: Dakikalar içinde maternal kan hacmi tükenir, doku perfüzyonu çöker.",
                "5. Uterotonik Müdahale: Acil oksitosin infüzyonu ve bimanüel masajla kasılma sağlanır."
            ]
        ),
        21: make_causal_chain(
            "Maternal Endokrin Adaptasyon Zinciri",
            [
                "1. Sinsityotrofoblast Sentezi: Plasenta hızla hPL, östrojen ve progesteron salgılamaya başlar.",
                "2. İnsülin Reseptör Blokajı: hPL maternal kas ve yağ dokusunda fizyolojik insülin direnci kurar.",
                "3. Glukoz Tasarrufu: Annenin glukoz kullanımı kısıtlanarak kan şekeri yükseltilir.",
                "4. Kolaylaştırılmış Difüzyon: Artan glukoz GLUT-1 taşıyıcılarıyla fetüse kesintisiz akar.",
                "5. Fetal Nörogenez Desteği: Anne karnındaki embriyo kesintisiz enerjiyle beynini büyütür."
            ]
        ),
        26: make_causal_chain(
            "Doğum Öncesi Bakımda Risk Erken Tanı Zinciri",
            [
                "1. Periyodik DÖB Viziti: Gebe semptomu olmasa dahi izlem takvimine uygun şekilde gelir.",
                "2. Rutin Tarama: Her vizitte kan basıncı ölçülür, idrarda dipstick protein bakılır.",
                "3. Asemptomatik Preeklampsi Tespiti: Tansiyon 145/95 mmHg ve protein 1+ erken yakalanır.",
                "4. Erken Profilaksi: Hasta takibe alınır, magnezyum sülfat ile nöbetler engellenir.",
                "5. Maternal-Fetal Sağkalım: Eklamptik koma yaşanmadan güvenli doğum planlanır."
            ]
        ),
        27: make_causal_chain(
            "Supin Hipotansif Sendrom Zinciri",
            [
                "1. Sırtüstü Yatış: İkinci trimestrden sonra gebe sırtüstü (supin) pozisyona geçer.",
                "2. Vena Kava Basısı: Ağırlaşan uterus vena cava inferioru omurga üzerine sıkıştırır.",
                "3. Venöz Dönüş Çöküşü: Kalbe dönen kan hacmi (preload) ve kardiyak debi aniden düşer.",
                "4. Serebral İskemi: Maternal kan basıncı hızla düşer; bayılma hissi ve terleme başlar.",
                "5. Sol Yan Pozisyon: Gebe sola çevrildiğinde bası kalkar ve dolaşım anında düzelir."
            ]
        ),
        31: make_causal_chain(
            "İki Canlı Efsanesinin Obeziteye Dönüşme Zinciri",
            [
                "1. Toplumsal Baskı: Çevre baskısıyla gebeye her şeyden çift porsiyon yedirilir.",
                "2. Boş Kalori Yığılması: Şekerli tatlılar ve hamur işleri günlük 3500 kaloriye tırmanır.",
                "3. Aşırı Yağ Depolanması: Fetal ihtiyaç fazlası kalori maternal pelvik yağ dokusuna gömülür.",
                "4. İnsülin Tükenişi: Pankreas beta hücreleri aşırı direnci karşılayamaz ve GDM patlar.",
                "5. Sezaryen ve Kalıcı Obezite: Doğum güçleşir, cerrahi doğum gerekir ve kilo kalıcılaşır."
            ]
        ),
        37: make_causal_chain(
            "Fetal Hiperinsülinizm ve Makrozomi Zinciri",
            [
                "1. Maternal Hiperglisemi: Annenin kanındaki yüksek glukoz plasentayı kolaylaştırılmış difüzyonla geçer.",
                "2. İnsülin Geçememesi: Maternal insülin plasentayı aşamaz; fötal kanda yalnız serbest glukoz birikir.",
                "3. Fetal Pankreas Uyarısı: Fötal beta hücreleri hipertrofiye uğrayarak aşırı insülin salgılar.",
                "4. Anabolik Patlama: İnsülin fötal yağ dokusunu büyüterek makrozomi (>4000 g) yapar.",
                "5. Omuz Distosisi: İrilleşen fetal omuz kuşağı doğum kanalında simfizis pubise takılır."
            ]
        ),
        41: make_causal_chain(
            "Gebelikte 12,5 kg Ağırlık İnşa Zinciri",
            [
                "1. Fetal Ünite Kurulması: Bebek (3,4 kg), plasenta (0,7 kg) ve sıvı (0,8 kg) ile 5 kg oluşur.",
                "2. Kan Hacmi Genişlemesi: Plazma ve alyuvar artışıyla anne dolaşımına 1,8 kg sıvı eklenir.",
                "3. Maternal Organ Büyümesi: Uterus ve meme dokusu hipertrofisi 1,5 kg kütle yapar.",
                "4. Laktasyon Deposu: Emzirmede süt üretmek üzere kalça ve karında 3,5 kg yağ depolanır.",
                "5. Sağlıklı Doğum Bitişi: Toplam 12,5 kg ile hem fetal gelişim hem süt güvenceye alınır."
            ]
        ),
        46: make_causal_chain(
            "Gebelik Öncesi BKİ'ye Göre Kilo Programlama Zinciri",
            [
                "1. Prekonsepsiyonel Ölçüm: Gebe kalındığı andaki boy ve tartı ile BKİ (kg/m²) hesaplanır.",
                "2. Kilo Koridoru Belirleme: Normal kilolu kadına 11,5-16 kg; obez kadına en az 6 kg hedefi konur.",
                "3. Haftalık İzlem: İkinci yarıda haftalık tartı artışının 400 gramı aşmaması takip edilir.",
                "4. İnsülin Direnci Kontrolü: Aşırı yağlanma engellenerek direncin GDM'ye dönüşmesi önlenir.",
                "5. Optimal Doğum Tartısı: Bebek ne büyüme geriliğine ne makrozomiye girmeden 3200 g ile doğar."
            ]
        ),
        47: make_causal_chain(
            "Adolesan Gebelikte Büyüme Rekabeti Zinciri",
            [
                "1. Biyolojik İmmatürite: Genç adölesanın epifiz kıkırdakları açık olup büyümesi sürmektedir.",
                "2. Fötal İskelet Talebi: Fötus iskeletini kurabilmek için maternal kalsiyum ve proteine muhtaçtır.",
                "3. Besin Paylaşım Savaşı: Diyet yetersiz kaldığında adölesan vücudu besinleri paylaştırır.",
                "4. Çift Yönlü Yıkım: Anne adayının boy uzaması duraklar; bebek ise IUGR tablosuna girer.",
                "5. Üst Sınır Diyet Desteği: Kılavuzların üst sınırında kalori ve 1300 mg kalsiyumla denge kurtarılır."
            ]
        ),
        51: make_causal_chain(
            "Maternal Protein Sentez Zinciri",
            [
                "1. Aminoasit Havuzu: Günlük diyete eklenen 20-25 g kaliteli protein bağırsaktan emilir.",
                "2. Karaciğer Albumin Sentezi: Onkotik basıncı korumak üzere maternal proteinler üretilir.",
                "3. Plasental Aktif Taşıma: Aminoasitler plasental pompalarla fetal kana konsantre edilir.",
                "4. Fötal Organ Büyümesi: Beyin, kalp ve kas dokularında toplam 925 g protein biriktirilir.",
                "5. İdeal Doğum Kütlesi: Yeterli protein fötal büyüme kısıtlılığını engelleyerek sağkalımı sağlar."
            ]
        ),
        56: make_causal_chain(
            "İyotlu Tuzun Sofraya Ulaşma Zinciri",
            [
                "1. Endüstriyel İyotlama: Rafine sofra tuzuna potasyum iyodat bileşiği homojen püskürtülür.",
                "2. Koyu Kapta Muhafaza: Evde tuz ışıksız, nemsiz, koyu renkli ve ağzı kapalı kavanoza konur.",
                "3. Uçuculuğun Önlenmesi: Yüksek kaynama sıcaklığının iyodu buharlaştırmaması için erken atılmaz.",
                "4. Ocaktan Sonra Ekleme: Tencere ateşten alındıktan sonra veya sofrada tabağa serpilir.",
                "5. Biyoaktif Emilim: İyot eksiksiz emilerek fetal tiroid hormon sentezini güvenceye alır."
            ]
        ),
        57: make_causal_chain(
            "İyot Eksikliğinde Kretenizm Gelişim Zinciri",
            [
                "1. Maternal İyot Açığı: Annenin diyetinde iyot eksik olduğunda tiroid hormon sentezi çöker.",
                "2. Fetal Beyin Yoksunluğu: İlk 12 haftada kendi tiroidi olmayan fetüse T4 transferi yapılamaz.",
                "3. Nöronal Göç Durması: Serebral korteks ve koklear hücrelerin nörogenezi felce uğrar.",
                "4. İrreversibl Beyin Hasarı: Nöronal aksonların miyelinizasyonu durur; zeka geriliği kalıcılaşır.",
                "5. İyotlu Tuz Profilaksisi: Toplumda iyotlu tuz kullanımıyla kretenizm tamamen silinir."
            ]
        ),
        61: make_causal_chain(
            "Nöral Tüp Kapanma Takvimi Zinciri",
            [
                "1. Prekonsepsiyonel Hazırlık: Gebe kalmadan 3 ay önce folik asit başlanarak eritrositler doyurulur.",
                "2. Fertilizasyon ve İmplantasyon: Döllenen zigot blastokiste dönüşüp endometriyuma tutunur.",
                "3. Nöral Oluk Oluşumu: 21. günde ektoderm kalınlaşarak nöral kıvrımları yükseltir.",
                "4. 28. Günde Tam Kapanma: Kranial ve kaudal nöroporlar 28. günde sımsıkı kapanarak tüpü tamamlar.",
                "5. Kusursuz SSS Temeli: Spina bifida ve anensefali riski %85 oranında önlenmiş olur."
            ]
        ),
        66: make_causal_chain(
            "C Vitamini ile Non-Hem Demir Emilim Zinciri",
            [
                "1. Bitkisel Demir Tüketimi: Ispanak ve baklagillerdeki demir ferrik (Fe3+) iyon kompleksleridir.",
                "2. Çökelme Riski: Bağırsak alkali ortamında Fe3+ çökelerek emilemez hale gelebilir.",
                "3. Askorbat İndirgemesi: Taze portakal suyu veya limonlu salatadaki C vitamini Fe3+'ü Fe2+'ye indirger.",
                "4. Şelasyon Koruması: C vitamini Fe2+ ile çözünür kelatlar kurarak duodenal DMT-1 kanalına taşır.",
                "5. Üç Kat Emilim Artışı: Diyetteki bitkisel demirin kana geçişi %3'ten %10-15 düzeyine tırmanır."
            ]
        ),
        67: make_causal_chain(
            "Nöral Tüp Kapanma Başarısızlığı Zinciri",
            [
                "1. Folat Yetersizliği: Hücre bölünmesinde nükleotid sentezi için gereken tetrahidrofolat tükenir.",
                "2. DNA Metilasyon Blokajı: Nöroektodermal kök hücrelerin bölünme hızı ve gen regülasyonu bozulur.",
                "3. Nöral Plak Kıvrılamaması: Embriyogenezin 21-28. günlerinde nöral oluk kenarları birleşemez.",
                "4. Açık Kalan Nöropor: 28. günde nöropor açık kalarak nöral dokuyu amniyona maruz bırakır.",
                "5. Spina Bifida / Anensefali: Sinir dokusu dejenere olur; omurilik kanalı açık kalır."
            ]
        ),
        76: make_causal_chain(
            "Tütün Dumanının Fetal Hipoksi Zinciri",
            [
                "1. Sigara Dumanı İnhalasyonu: Gebe kadın tütün dumanını çekerek nikotin ve CO'yu kana alır.",
                "2. Nikotin Vazokonstriksiyonu: Nikotin sempatik deşarjla uterus spiral arterlerini büzer.",
                "3. Karboksihemoglobin Sentezi: CO plasentayı geçerek fetal hemoglobine 200 kat güçlü bağlanır.",
                "4. Doku Hipoksisi: Uteroplasental akım azalırken, kanda taşınan oksijen dokulara bırakılamaz.",
                "5. Düşük Doğum Ağırlığı: Fetal hücre proliferasyonu frenlenir; bebek 250 g zayıf doğar."
            ]
        ),
        77: make_causal_chain(
            "Fetal Alkol Sendromunda Hücresel Yıkım Zinciri",
            [
                "1. Hızlı Plasental Difüzyon: Alkol hızla plasentayı geçerek fetal kanda anneyle aynı seviyeye ulaşır.",
                "2. Enzim İmmatüritesi: Fötal karaciğerde alkol dehidrogenaz bulunmadığı için etanol birikir.",
                "3. Nöral Krest Apoptozu: Alkol reaktif oksijen üreterek göç eden nöral krest hücrelerini öldürür.",
                "4. Dismorfolojik Şekillenme: Maksiller çıkıntılar birleşemez; filtrum düzleşir, dudak incelir.",
                "5. Kalıcı Nörokognitif Defisit: Beyin korteksi hipoplastik kalır; ömür boyu zeka geriliği oluşur."
            ]
        )
    }
    return chains

def get_21_sliders():
    sliders = {
        4: make_before_after(
            "2000 Yılı Anne Ölümleri vs 2020 Yılı Anne Ölümleri",
            "2000 Yılı Küresel Anne Sağlığı Düzeyi",
            "Yıllık anne ölüm oranı (MMR) çok yüksektir; kurumsal doğumlar kısıtlı, ebe açığı derin ve küresel farkındalık yetersizdir.",
            "2020 Yılı Küresel Anne Sağlığı Düzeyi",
            "Milenyum ve Sürdürülebilir Kalkınma Hedefleri ile MMR %34 oranında düşürülmüş, kurumsal doğumlar yaygınlaştırılmıştır."
        ),
        7: make_before_after(
            "10-14 Yaş Adolesan Gebelik vs 20-24 Yaş Yetişkin Gebelik",
            "10-14 Yaş Genç Adolesan Gebeliği",
            "Jinekolojik yaş <2 yıldır; kemik pelvisi dar, eklampsi ve obstrüktif travay riski maksimum, obstetrik fistül ve ölüm sıktır.",
            "20-24 Yaş İdeal Yetişkin Gebeliği",
            "Kemik pelvis tam olgunlaşmıştır; hormonal eksen stabil, obstetrik komplikasyon ve mortalite oranları en düşük düzeydedir."
        ),
        13: make_before_after(
            "Doğrudan vs Dolaylı Maternal Ölüm Nedenleri",
            "Doğrudan Obstetrik Ölüm Tablosu",
            "Gebelik, doğum ve lohusalık durumuna ya da obstetrik müdahalelere doğrudan bağlı komplikasyonlardır: Postpartum şiddetli kanama, puerperal sepsis, preeklampsi/eklampsi, obstrüktif travay ve güvenli olmayan kürtaj.",
            "Dolaylı Obstetrik Ölüm Tablosu",
            "Gebelik öncesinde var olan ya da gebelikte başlayıp gebeliğin fizyolojik hemodinamik yüküyle dekompanse olan hastalıklardır: Ağır demir eksikliği anemisi, maternal kalp kapak yetmezlikleri, sıtma ve HIV enfeksiyonu."
        ),
        23: make_before_after(
            "Gebe Olmayan Kadın vs Gebe Kadın Hemodinamisi",
            "Gebe Olmayan Kadın Dolaşımı",
            "Plazma hacmi yaklaşık 2,6 litredir; kardiyak debi 4,5-5,0 L/dk, oksijen tüketimi bazal düzeyde ve sistemik vasküler direnç normal seviyededir.",
            "Gebe Kadın Dolaşımı (Fizyolojik Uyum)",
            "Plazma hacmi %45-50 artarak 3,8 litreye ulaşır; kardiyak debi %30-50 tırmanır, oksijen tüketimi %20-30 yükselir ve fizyolojik hemodilüsyonla Hb sınırı 10,5-11 g/dl'ye iner."
        ),
        24: make_before_after(
            "Gebelikte Solunum Sistemi vs Gebe Olmayan Solunum",
            "Gebe Olmayan Kadın Solunumu",
            "Dakika ventilasyonu 6-7 L/dk; tidal volüm 500 ml, arteriyel pCO2 yaklaşık 40 mmHg ve bazal asit-baz dengesi nötraldir.",
            "Gebelikte Solunum Sistemi (Hiperventilasyon)",
            "Oksijen gereksinimi %20-30 artar; progesteron etkisiyle tidal volüm 700 ml'ye çıkar ve pCO2 30 mmHg'ye inerek fizyolojik solunumsal alkaloz oluşur."
        ),
        33: make_before_after(
            "İntrauterin Kıtlık vs Tasarruflu Fenotip Sonucu",
            "Fetal Dönemde İntrauterin Kıtlık",
            "Yetersiz maternal beslenme ortamında fetüs glukozu korumak için periferik dokularda insülin direnci geliştirir; pankreas beta hücre kütlesi ve nefron sayısı kısıtlı kalır.",
            "Erişkinlikte Bolluk Çatışması (Mismatch)",
            "Tasarruflu programlanan birey yetişkinlikte zengin kalorili batı tipi beslendiğinde kısıtlı organ kapasitesi çöker; erken yaşta Tip 2 diyabet, hipertansiyon ve koroner arter hastalığı patlar."
        ),
        34: make_before_after(
            "Maternal Yetersiz Beslenme vs Maternal Sağlıklı Beslenme",
            "Yetersiz Beslenen Gebe Tablosu",
            "Kendi kas ve kemik dokusunu harcar; osteomalazi, ağır demir eksikliği anemisi, toksemi ve doğum yorgunluğu gelişir.",
            "Yeterli ve Dengeli Beslenen Gebe",
            "Maternal depolar korunur; kemik yoğunluğu sağlam kalır, laktasyon için 3,5 kg yağ depolanır ve postpartum toparlanma hızlı olur."
        ),
        43: make_before_after(
            "Normal Kilo Alımı vs Aşırı Kilo Alımının Doğum Çıktıları",
            "Normal Kilo Kazanımı (11,5 - 16 kg)",
            "Doğum kanalı yumuşak doku yağlanması dengelidir; bebek 3000-3500 g ideal tartıda doğar, spontan vajinal doğum şansı maksimumdur ve doğum sonu kalıcı kilo kalmaz.",
            "Aşırı Kilo Kazanımı (>20 kg / Obezite)",
            "Pelvik yağ birikimi doğum kanalını daraltır; fetal makrozomi (>4000 g), omuz distosisi, acil sezaryen gereksinimi ve lohusalıkta kalıcı maternal obezite riski tırmanır."
        ),
        45: make_before_after(
            "Tekil Gebelik vs Çoğul Gebelik Ağırlık Hedefleri",
            "Tekil Gebelikte Kilo Kazanımı",
            "Normal kilolu kadında 11,5-16,0 kg artış hedeflenir; fetal ünite toplam yaklaşık 5 kg ağırlığındadır.",
            "Çoğul (Üçüz) Gebelikte Kilo Kazanımı",
            "Üç bebeğin plasentaları ve katlanan amniyon yükü nedeniyle toplam yaklaşık 23 kg ağırlık artışı hedeflenir."
        ),
        53: make_before_after(
            "İyotlu Diyet vs İyot Yetersizliği Fetal Beyni",
            "Yeterli İyot Alan Fetal Beyin",
            "Anne tiroidi yeterli T4 üretir; ilk 12 haftada fetal beyin korteksi ve koklea nöronları düzenli göç eder; işitme, görme ve zihinsel potansiyel eksiksiz gelişir.",
            "İyotsuz Kalan Fetal Beyin (Kretenizm)",
            "T4 transferi durur; serebral korteks hipoplastik kalır; bebek geri dönüşsüz nörolojik kretenizm, derin mental retardasyon, sağırlık-dilsizlik ve spastik dipleji ile doğar."
        ),
        54: make_before_after(
            "Tahıllarda Fitat Varlığı vs Mayalama Fermantasyonu",
            "Mayasız Kepekli Tahıl Tüketimi",
            "Yüksek oranda fitik asit (fitat) içerir; bağırsak lümeninde çinko ve demir iyonlarını çözünmez tuzlar halinde çökelterek emilimi bloke eder.",
            "Geleneksel Mayalı Ekmek Tüketimi",
            "Fermantasyon sürecinde mayadaki fitaz enzimi aktifleşir; fitatları parçalayarak çinko ve demirin serbest kalmasını ve yüksek oranda emilmesini sağlar."
        ),
        62: make_before_after(
            "Spina Bifida vs Anensefali Klinik Tablosu",
            "Spina Bifida (Kaudal Defekt)",
            "Omurga kanalı açık kalır; meningomiyelosel, alt ekstremite paraplejisi, inkontinans ve hidrosefali gelişir; cerrahiyle yaşatılabilir.",
            "Anensefali (Kranial Defekt)",
            "Kranial nöropor açık kalır; serebral hemisferler ve kalvaryum hiç gelişmez; yaşamla bağdaşmayan fatal tablodur."
        ),
        63: make_before_after(
            "Düşük Riskli vs Yüksek Riskli Folik Asit Profilaksisi",
            "Standart Düşük Riskli Gebe",
            "Daha önce anomalili doğum öyküsü yoktur; gebe kalmadan 3 ay önce başlanıp ilk 12 hafta boyunca günde 400 mcg (0,4 mg) standart folik asit tableti verilir.",
            "Yüksek Riskli Gebe (NTD Öykülü)",
            "Önceki gebeliğinde spina bifida öyküsü vardır veya antiepileptik kullanır; gebelikten 3 ay önce başlanarak doz tam 10 katına çıkarılır: Günde 4000 mcg (4 mg) folik asit verilir."
        ),
        68: make_before_after(
            "1. ve 3. Trimestr Anemi Eşiği vs 2. Trimestr Eşiği",
            "1. ve 3. Trimestr Anemi Kriteri",
            "Hemoglobin değerinin 11,0 g/dl altında olması durumunda anemi kabul edilir; hematokrit sınırı yaklaşık %33 düzeyindedir.",
            "2. Trimestr Anemi Kriteri (Pik Hemodilüsyon)",
            "Plazma hacmi artışının zirveye çıkması nedeniyle hemoglobin değerinin 10,5 g/dl altında olması anemi kabul edilir; 10,8 g/dl fizyolojiktir."
        ),
        73: make_before_after(
            "Sağlık Bakanlığı Demir vs D Vitamini Protokolleri",
            "Demir Destek Protokolü",
            "16. gebelik haftasında başlar, gebelik boyunca 6 ay ve doğum sonu 3 ay olmak üzere toplam 9 ay sürer; günlük doz 40-60 mg elementer demirdir.",
            "D Vitamini Destek Protokolü",
            "12. gebelik haftasında başlar ve doğum sonrası 6. aya kadar kesintisiz sürdürülür; günlük doz 1200 IU (30 mcg / 9 damla) kolekalsiferoldür."
        ),
        80: make_before_after(
            "Gebelikte Alkol vs Sigara Toksikolojisi",
            "Alkol Maruziyeti (Teratogenez)",
            "Hücresel nörotoksisite ile Fetal Alkol Sendromu yapar; düz filtrum, ince üst dudak, mikrosefali ve kalıcı zeka geriliği üretir.",
            "Sigara Maruziyeti (Vasküler Hipoksi)",
            "Nikotin ve CO ile plasental kanı keserek düşük doğum ağırlığı, ablasyo plasenta ve erken doğum yapar; yüz dismorfisi yapmaz."
        ),
        83: make_before_after(
            "Fizyolojik Gebelik Bulantısı vs Hiperemezis Gravidarum",
            "Fizyolojik Bulantı (Emesis)",
            "Genellikle sabahları kuru gıdayla hafifler; kilo kaybı yoktur (<%5), dehidratasyon bulgusu izlenmez, idrarda keton negatiftir ve ayaktan diyetle yönetilir.",
            "Patolojik Hiperemezis Gravidarum",
            "Gün boyu inatçı kusma sürer; vücut ağırlığının %5'inden fazlası kaybedilir, mukozalar kuru, idrarda 3+ ketonüri vardır; hastanede IV hidrasyon ve tiamin gerektirir."
        ),
        88: make_before_after(
            "Sağlıklı Diş Eti vs Gebelik Epulisi (Epulis Gravidarum)",
            "Sağlıklı Diş Eti Dokusu",
            "Açık pembe renkli, sıkı kıvamlı, portakal kabuğu pürtüklü ve fırçalarken kanamayan sağlam gingival mukozadır.",
            "Epulis Gravidarum (Gebelik Epulisi)",
            "Östrojen damarlanmasıyla interdental papillada gelişen selim, parlak kırmızı, ödemli ve en ufak dokunmada kolayca kanayan vasküler yumrudur."
        ),
        93: make_before_after(
            "Gebelikte Besin Grupları vs Emziklilikte Besin Grupları",
            "Gebelikte Besin Grupları Ekleri",
            "Süt grubu +1 porsiyon (toplam 3-4 porsiyon), et grubu +0,5-1 porsiyon (toplam 3 porsiyon); TAHILLARDA İSE HİÇBİR EK PORSİYONA GEREK YOKTUR.",
            "Emziklilikte Besin Grupları Ekleri",
            "Süt grubu +1 porsiyon (toplam 3-4 porsiyon), et grubu +1 porsiyon; artan enerji ve süt sentezi maliyetini karşılamak için TAHILLARA GÜNLÜK +1,5 PORSİYON EKLENİR."
        ),
        95: make_before_after(
            "Emzirmede Alkol vs Temiz Laktasyon",
            "Temiz Laktasyon Dönemi",
            "Oksitosin salınımı kusursuz çalışır; süt inme refleksi güçlüdür, bebek sakin uyur ve büyüme eğrisi düzenli ilerler.",
            "Alkol Alan Emziren Anne Tablosu",
            "Etanol oksitosini felç eder; süt inmesi zorlaşır, bebekte derin letarji, büyüme duraksaması ve zayıf emme gelişir."
        ),
        98: make_before_after(
            "İlk 6 Ay Sadece Anne Sütü vs Erken Ek Gıda Başlanması",
            "Eksklüzif Anne Sütü Alan Bebek",
            "Mide-bağırsak mukozası sIgA ile korunur; solunum ve sindirim enfeksiyonu riski minimumdur, ek suya dahi ihtiyaç duymaz.",
            "Erken Ek Gıda Başlanan Bebek (<6 Ay)",
            "Anne sütü alımı azalır; sindirim enzim immatüritesi nedeniyle gıda alerjisi, ishal ve bağırsak mikrobiyota bozulması riski tırmanır."
        )
    }
    return sliders

def get_21_branchings():
    branchings = {
        8: make_branching_logic(
            "15 yaşında adölesan bir gebe 28. haftada halsizlik yakınmasıyla aile hekimliğine başvuruyor. Hemoglobin 8,2 g/dl saptanıyor. Boy uzaması ve ağırlık artışı yetişkin ortalamasının oldukça gerisinde.",
            [
                {
                    "text": "Adolesan annenin kendi büyümesi ile bebeğin büyümesinin yarıştığını fark ederek diyetini üst sınır kalori, 1300 mg kalsiyum ve tedavi dozu demirle zenginleştirmek.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru yaklaşım. Adolesan gebelerde besin rekabeti mevcuttur; önerilerin üst sınırı hedeflenmeli ve 1300 mg kalsiyum verilmelidir."
                },
                {
                    "text": "Kilo almasını durdurmak için kalori kısıtlaması yapmak ve demir ilacını doğuma kadar ertelemek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Kalori kısıtlamak adölesanın boyunun kısa kalmasına ve bebeğin ağır IUGR ile doğmasına yol açar."
                }
            ]
        ),
        15: make_branching_logic(
            "Doğumhanede termde normal doğum yapan kadında plasenta ayrıldıktan 5 dakika sonra masif vajinal kanama başlıyor. Uterus göbek hizasında yumuşak, gevşek ve süngerimsi palpe ediliyor.",
            [
                {
                    "text": "Kanamanın durmasını bekleyip hastayı odaya göndermek ve soğuk kompres uygulamak.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Uterus atonisi dakikalar içinde hipovolemik şok ve ölüme yol açar; pasif beklenemez."
                },
                {
                    "text": "Uterin atoni teşhisiyle derhal bimanüel uterin masaja başlamak ve IV oksitosin infüzyonunu açmak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru klinik yaklaşım. Postpartum kanamanın bir numaralı sebebi atonidir; ilk müdahale oksitosin ve fundus masajıdır."
                }
            ]
        ),
        25: make_branching_logic(
            "30 haftalık gebe kadın muayene masasına sırtüstü uzandığı anda aniden soğuk terleme, göz kararması ve bayılma hissi tanımlıyor. Kan basıncı 80/50 mmHg ölçülüyor.",
            [
                {
                    "text": "Hastayı derhal sol yan dekübit pozisyonuna çevirmek ve uterusun vena kava basısını kaldırmak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru karar. Bu tablo supin hipotansif sendromdur; gebeyi sola çevirmek venöz dönüşü ve tansiyonu anında düzeltir."
                },
                {
                    "text": "Hastayı hemen ayağa kaldırıp hızlıca yürütmeye çalışmak.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Serebral perfüzyon çökmüşken ayağa kaldırmak senkopa ve kafa travmasına yol açar."
                }
            ]
        ),
        28: make_branching_logic(
            "Doğum ağırlığı 2100 gram (düşük doğum ağırlığı) olan ve intrauterin büyüme kısıtlılığı yaşayan bir bebeğin ailesi, bebeğin ileriki yaşamında karşılaşabileceği riskleri öğrenmek istiyor.",
            [
                {
                    "text": "Barker hipotezine göre fetal kıtlık ortamının tasarruflu fenotip oluşturduğunu; çocuklukta aşırı kalorili beslenirse erişkinlikte Tip 2 diyabet ve KAH riskinin katlanacağını anlatmak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru koruyucu hekimlik vizyonu. Barker hipotezi tam olarak bu fetal kökenli metabolik uyumsuzluğu açıklar."
                },
                {
                    "text": "Bebeğin hafif doğmasının onu hayat boyu diyabet ve kalp krizinden tamamen koruyacağını söylemek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Düşük doğum ağırlıklı doğan bebekler erişkin çağda metabolik sendrom açısından en yüksek risk grubundadır."
                }
            ]
        ),
        35: make_branching_logic(
            "Gebelik öncesi BKİ'si 34 kg/m² olan obez bir gebe kadın, bebeğinin sağlığı için gebelik boyunca zayıflama diyeti yapıp 8 kilo vermek istediğini söylüyor.",
            [
                {
                    "text": "Çok iyi bir fikir olduğunu söyleyip karbonhidratsız ketojenik zayıflama diyeti yazmak.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Gebelikte zayıflama diyeti ketozis yaparak fötal beyin gelişimini bozar ve nörobilişsel gerilik yaratır."
                },
                {
                    "text": "Gebelikte kilo vermenin kesinlikle yasak olduğunu, obez gebelerde dahi en az 6 kg ağırlık kazanılması gerektiğini açıklamak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru danışmanlık. BKİ ≥30 olan gebelerde hedef kilo vermek değil, en az 6 kg'lık kontrollü artış sağlamaktır."
                }
            ]
        ),
        45: make_branching_logic(
            "20 haftalık ikiz gebeliği olan bir kadın diyetisyene başvurarak günlük beslenmesine tekiz gebelik gibi 300 kalori eklemesinin yeterli olup olmadığını soruyor.",
            [
                {
                    "text": "İkiz gebelikte günlük ek enerji ihtiyacının +600 kalori olduğunu belirterek kaliteli protein ve kalori desteği planlamak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru yaklaşım. Kılavuzlara göre ikiz gebelikte önerilen günlük ek enerji +600 kal/gündür."
                },
                {
                    "text": "İkiz gebelikte bebekler küçük kalacağı için hiç kalori artışına gerek olmadığını söylemek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Yetersiz kalori anne katabolizmasını tetikler ve erken doğum ile ağır IUGR riskini katlar."
                }
            ]
        ),
        48: make_branching_logic(
            "24 haftalık üçüz gebeliği olan bir kadın, doktoruna toplam kaç kilo almasının uygun olduğunu ve günlük ne kadar ek kalori tüketmesi gerektiğini soruyor.",
            [
                {
                    "text": "Üçüz gebeliklerde toplam yaklaşık 23 kg ağırlık artışı ve günlük +900 kalori ek enerji gerektiğini söylemek.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru kılavuz bilgisi. Ders notlarına göre üçüz gebelikte 23 kg ağırlık artışı ve +900 kal/gün ek enerji esastır."
                },
                {
                    "text": "Üçüz gebelikte de tekil gebelik gibi en fazla 12 kg alınması ve günde 300 kalori eklenmesinin yeterli olduğunu söylemek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! 12 kg üçüz bebeklerin fötal ünite ağırlığını dahi karşılayamaz; ağır preterm doğum ve malnütrisyona yol açar."
                }
            ]
        ),
        55: make_branching_logic(
            "Dağlık bir kırsal bölgede yaşayan ve guatrı olan gebe kadın yemeklerinde kaya tuzu kullandığını ve iyotlu tuzu hiç tüketmediğini söylüyor.",
            [
                {
                    "text": "Kaya tuzunun doğal olduğunu söyleyip devam etmesini tavsiye etmek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! İyotsuz kaya tuzu fetüste kretenizm, zeka geriliği ve sağırlık riskini maksimuma çıkarır."
                },
                {
                    "text": "İyot eksikliğinin bebekte kretenizm ve zeka geriliği yapacağını anlatıp koyu kapta saklanan iyotlu tuza geçişi sağlamak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru halk sağlığı müdahalesi. İyotlu tuz kullanımı önlenebilir zeka geriliğini sıfırlayan temel araçtır."
                }
            ]
        ),
        65: make_branching_logic(
            "Önceki gebeliğinde spina bifidalı bir bebek dünyaya getiren ve tekrar çocuk sahibi olmak isteyen 28 yaşındaki bir kadın prekonsepsiyonel danışmanlığa geliyor.",
            [
                {
                    "text": "Gebe kaldıktan sonra test pozitif çıkınca günlük 400 mcg folik aside başlamasını söylemek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! 28. günde tüp kapanır; gebelik sonrasında başlamak geçtir ve yüksek riskte 400 mcg yetersizdir."
                },
                {
                    "text": "Gebe kalmadan en az 3 ay önce günlük 4000 mcg (4 mg) yüksek doz folik asit tabletine başlamasını reçete etmek.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru protokol. NTD öyküsü olan kadınlarda doz 10 kat artırılarak prekonsepsiyonel 4 mg/gün olarak uygulanır."
                }
            ]
        ),
        68: make_branching_logic(
            "22 haftalık bir gebenin rutin kan tahlilinde hemoglobin değeri 10,7 g/dl ölçülüyor. Gebe anemi olduğunu düşünerek endişeyle polikliniğe başvuruyor.",
            [
                {
                    "text": "İkinci trimestrde plazma artışına bağlı fizyolojik hemodilüsyon nedeniyle anemi sınırının 10,5 g/dl olduğunu, 10,7 g/dl'nin anemi olmadığını açıklayıp rutin profilaksiye devam etmek.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Harika klinik yaklaşım. DSÖ'ye göre 2. trimestr anemi eşiği 10,5 g/dl'dir; 10,7 g/dl fizyolojik hemodilüsyondur."
                },
                {
                    "text": "Derhal hastaneye yatırıp acil eritrosit süspansiyonu transfüzyonu yapmak.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Hemoglobin 10,7 g/dl ikinci üç ayda fizyolojik bir değerdir; gereksiz transfüzyon morbidite üretir."
                }
            ]
        ),
        75: make_branching_logic(
            "14 haftalık gebe kadın akşam yemeklerinde günde bir kadeh kırmızı şarabın bebeğin kalbine iyi geleceğini duyduğunu belirterek onayınızı istiyor.",
            [
                {
                    "text": "Kırmızı şarabın antioksidan olduğunu söyleyip haftada birkaç kadehe izin vermek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Gebelikte güvenli alkol miktarı sıfırdır; en hafif alkol dahi fötal beyin korteksinde nöron ölümüne yol açar."
                },
                {
                    "text": "Gebelikte alkolün güvenli hiçbir dozu olmadığını, Fetal Alkol Sendromu riskini ve sıfır alkol kuralını kesin dille anlatmak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru klinik yaklaşım. Gebelikte altın kural mutlak alkol abstinansı ve sıfır toleranstır."
                }
            ]
        ),
        85: make_branching_logic(
            "28 haftalık bir gebede kan basıncı 150/95 mmHg ölçülüyor ve idrarda 2+ proteinüri saptanıyor. Hasta komşusunun tavsiyesiyle yemeklerindeki tuzu tamamen kestiğini söylüyor.",
            [
                {
                    "text": "Doğru yaptığını söyleyip hiç tuz tüketmemesini ve az su içmesini tembihlemek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Preeklampside aşırı tuz kısıtlaması intravasküler volümü çökerterek fötal distresi ve asfikisiyi tetikler."
                },
                {
                    "text": "Preeklampside tuzu tamamen kesmenin tehlikeli olduğunu, normal tuzlu dengeli beslenmeye devam etmesi gerektiğini anlatmak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru patofizyolojik yaklaşım. Preeklampside tuz tamamen kesilmez; normal tuzlu diyet sürdürülmelidir."
                }
            ]
        ),
        88: make_branching_logic(
            "Gebeliğinin 10. haftasında olan bir kadın dişlerini fırçalarken diş etlerinin kanadığını ve şiştiğini söylüyor. Dişlerini fırçalamayı tamamen bırakmayı düşündüğünü belirtiyor.",
            [
                {
                    "text": "Fırçalamayı bırakırsa periodontal enfeksiyonların erken doğumu tetikleyeceğini anlatıp yumuşak fırça, diş ipi ve C vitamini desteği önermek.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru yaklaşım. Diş eti hijyeni bırakılamaz; periodontit erken doğum riskini 2 katına çıkarır. Yumuşak fırça ve C vitamini esastır."
                },
                {
                    "text": "Doğuma kadar diş fırçalamanın yasak olduğunu söyleyip hiç ağız bakımı yapmamasını tembihlemek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Ağız hijyeninin terkedilmesi derin bakteriyel enfeksiyonlara ve sistemik inflamasyonla fetal kayıplara zemin hazırlar."
                }
            ]
        ),
        90: make_branching_logic(
            "8 haftalık gebe kadın günde 6-7 kez kustuğunu, 4 kilo verdiğini (gebelik öncesi 60 kg) belirtiyor. İdrar tahlilinde 3+ keton saptanıyor.",
            [
                {
                    "text": "Evde tuzlu kraker yemesini ve bol çay içmesini önerip 1 ay sonra kontrole çağırmak.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Hastada >%5 kilo kaybı ve ağır ketonüri mevcuttur; bu tablo Hiperemezis Gravidarumdur ve evde takip edilemez."
                },
                {
                    "text": "Hastayı derhal servise yatırmak, oral alımı durdurup IV sıvı-elektrolit ve tiamin tedavisi başlatmak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru karar. Kilo kaybı %6,6 ve belirgin ketonüri varlığı acil hospitalizasyon ve IV hidrasyon gerektirir."
                }
            ]
        ),
        95: make_branching_logic(
            "2 aylık bebeğini emziren bir anne süt miktarını artırmak için günde 3 büyük kupa demli kahve içtiğini ve çok az su tükettiğini belirtiyor. Bebeğin aşırı huzursuz olduğu ve uyumadığı öğreniliyor.",
            [
                {
                    "text": "Kahveyi günde 1 fincanla sınırlamasını, günde 2-3 litre sıvı tüketmesini ve emzirme aralarında su içmesini tavsiye etmek.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru yaklaşım. Fazla kafein süte geçerek bebekte taşikardi ve uykusuzluk yapar; sütü artıran faktör hidrasyondur."
                },
                {
                    "text": "Kahvenin süt üretimini kamçıladığını söyleyip kafein miktarını daha da artırmasını önermek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Aşırı kafein bebeği intoksike eder ve diüretik etkisiyle maternal dehidratasyon yaparak sütü azaltır."
                }
            ]
        ),
        1: make_branching_logic(
            "Evlilik planı yapan ve 4 ay sonra gebe kalmak isteyen 24 yaşındaki sağlıklı bir kadın aile sağlığı merkezine danışmanlığa geliyor.",
            [
                {
                    "text": "Gebelik oluştuktan sonra kadın doğum uzmanına görünmesinin yeterli olduğunu söyleyip göndermek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Nöral tüp 28. günde kapandığı için gebelik sonrasına bırakılan folat profilaksisi geç kalır."
                },
                {
                    "text": "Prekonsepsiyonel bakım kapsamında günde 400 mcg folik asit başlamak ve genel sağlık taraması yapmak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru halk sağlığı yaklaşımı. Planlı gebelikten 3 ay önce başlanan folik asit NTD'yi önler."
                }
            ]
        ),
        19: make_branching_logic(
            "Doğum eylemi 20 saattir süren ve başın pelviste takıldığı anlaşılan bir gebenin yakınları evde doğumda ısrar ediyor.",
            [
                {
                    "text": "Tıkalı doğum eyleminin uterus rüptürüne ve obstetrik fistüle yol açacağını anlatıp acil sezaryen için tam donanımlı hastaneye sevki sağlamak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Hayat kurtarıcı karar. Obstrüktif travay cerrahi olmadan çözülemez; evde ısrar maternal-fetal ölümle biter."
                },
                {
                    "text": "Evde oksitosin damlatıp beklemeye devam etmek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Tıkalı travayda mekanik engel varken uterotonik vermek uterus rüptürünü kesinleştirir."
                }
            ]
        ),
        39: make_branching_logic(
            "Gebeliğinin 16. haftasında olan ve sadece patates kızartması ve gazlı içecekle beslendiğini söyleyen gebenin muayenesinde aşırı kilo artışı saptanıyor.",
            [
                {
                    "text": "'İki canlısın, canın ne çekerse onu ye' diyerek beslenmesini onaylamak.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Bu hatalı anlayış maternal gestasyonel diyabet ve fetal makrozomiye davetiye çıkarır."
                },
                {
                    "text": "İki canlı anlayışının yanlış olduğunu, aşırı kalorinin diyabet ve makrozomi riski yarattığını anlatıp dengeli diyet planlamak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru yaklaşım. Gebe her şeyden iki kat değil, belirli besin ögelerinden kaliteli beslenmelidir."
                }
            ]
        ),
        59: make_branching_logic(
            "Vejetaryen olduğunu ve hiçbir hayvansal gıda (et, süt, yumurta) tüketmediğini belirten 12 haftalık gebe kadın rutin kontrole geliyor.",
            [
                {
                    "text": "Bitkisel gıdalarda B12 olduğunu söyleyip hiçbir takviyeye gerek olmadığını belirtmek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! B12 yalnız hayvansal gıdalarda bulunur; vejetaryen gebede takviye edilmezse bebekte kalıcı beyin hasarı ve megaloblastik anemi gelişir."
                },
                {
                    "text": "B12 vitamininin yalnız hayvansal besinlerde olduğunu açıklayarak gebeye derhal farmakolojik B12 desteği reçete etmek.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru koruyucu hekimlik kararı. Vegan/vejetaryen annelerde B12 replasmanı zorunludur."
                }
            ]
        ),
        79: make_branching_logic(
            "16. gebelik haftasına giren sağlıklı bir gebenin rutin hemoglobin tahlili 12,2 g/dl (normal) çıkıyor. Ebe demir ilacı başlamak istediğinde gebe 'Kanım iyiymiş, ilaca gerek yok' diyor.",
            [
                {
                    "text": "Gebelik boyunca 1000 mg demir gerekeceğini ve diyetin yetmeyeceğini anlatıp Sağlık Bakanlığı profilaktik demir desteğini başlatmak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Kusursuz halk sağlığı yaklaşımı. Klinik anemi olmasa dahi tüm gebelere 16. haftada 40-60 mg demir başlanması kuraldır."
                },
                {
                    "text": "Haklı olduğunu söyleyip demir desteğini tamamen iptal etmek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Profilaksi verilmezse 3. trimestrde fötal talep maternal depoları boşaltarak ağır anemi yaratır."
                }
            ]
        ),
        99: make_branching_logic(
            "Yeni doğum yapmış bir anne, sütünün henüz az geldiğini düşünerek bebeğe şekerli su ve hazır mama vermeye başladığını söylüyor.",
            [
                {
                    "text": "Şekerli suyun sarılığı önleyeceğini söyleyip devam etmesini istemek.",
                    "isCorrect": False,
                    "feedback": "Yanlış! Şekerli su vermek emme refleksini bozar, bağırsak florasını yıkar ve anne sütü üretimini durdurur."
                },
                {
                    "text": "İlk 6 ay su dahil hiçbir ek gıdanın verilmemesi gerektiğini, kolostrumun bebeğe yeteceğini ve emzirdikçe sütün artacağını anlatmak.",
                    "isCorrect": True,
                    "feedback": "Tebrikler! Doğru emzirme danışmanlığı. İlk 6 ay sadece anne sütü verilmeli, ek su verilmemelidir."
                }
            ]
        )
    }
    return branchings

def get_21_tables():
    tables = {
        9: make_table(
            ["Gösterge / Parametre", "Küresel Değer (DSÖ)", "Türkiye Düzeyi (TÜİK)"],
            [
                [("Yıllık Anne Ölümü", False, ""), ("Yaklaşık 287.000 kadın", True, "Küresel yıllık maternal ölüm sayısı"), ("Gelişmiş ülke seviyesine yakın düşüş", False, "")],
                [("Ölümlerin Gelir Grubu Dağılımı", False, ""), ("Yüzde 95 düşük ve orta gelirli ülkelerde", True, "Yoksul ülkelerdeki yığılma yüzdesi"), ("Hastanede doğum oranı yüzde 99 üstü", False, "")],
                [("Adolesan Doğurganlık Hızı", False, ""), ("Dünya genelinde binde 40 civarı", False, ""), ("2023 itibarıyla binde 11", True, "Türkiye'nin güncel adölesan doğum hızı")]
            ]
        ),
        12: make_table(
            ["Doğrudan Obstetrik Neden", "Ölümlerdeki Yaklaşık Payı", "Temel Patolojik Mekanizma"],
            [
                [("Şiddetli Kanama (PPH)", False, ""), ("Tüm ölümlerin yaklaşık yüzde 27'si", True, "En sık ölüm nedeninin küresel yüzdesi"), ("Uterin atoni ve açık kalan spiral arterler", False, "")],
                [("Puerperal Sepsis", False, ""), ("Tüm ölümlerin yaklaşık yüzde 11'i", False, ""), ("Non-steril doğum ve polimikrobiyal endometrit", True, "Doğum sonu kan zehirlenmesi mekanizması")],
                [("Hipertansif Bozukluklar", False, ""), ("Tüm ölümlerin yaklaşık yüzde 14'ü", False, ""), ("Yaygın endotel hasarı ve eklampsi nöbetleri", True, "Preeklampsinin ölümcül serebral tablosu")]
            ]
        ),
        19: make_table(
            ["Obstetrik Komplikasyon", "Temel Patofizyoloji", "Altın Standart Tedavi / Yaklaşım"],
            [
                [("Postpartum Kanama", False, ""), ("Uterin atoni ve açık kalan spiral damarlar", False, ""), ("Profilaktik oksitosin ve bimanüel masaj", True, "Uterotonik hormon ve mekanik yaklaşım")],
                [("Preeklampsi / Eklampsi", False, ""), ("Yaygın endotel hasarı ve serebral vazospazm", False, ""), ("Magnezyum sülfat infüzyonu ve doğum", True, "Nöbet önleyici iyon infüzyonu")],
                [("Tıkalı Doğum Eylemi", False, ""), ("Sefalopelvik uyumsuzluk ve mekanik ilerlememe", False, ""), ("Acil sezaryen doğum eylemi", True, "Cerrahi doğum müdahalesi")]
            ]
        ),
        29: make_table(
            ["Fizyolojik Parametre", "Gebelikteki Değişim Yönü / Oranı", "Klinik Yansıması / Önemi"],
            [
                [("Plazma Hacmi", False, ""), ("Yüzde 45-50 oranında artış", True, "Sıvı fazdaki devasa yükselme"), ("Fizyolojik hemodilüsyon ve viskozite düşüşü", False, "")],
                [("Oksijen Tüketimi", False, ""), ("Yüzde 20-30 oranında artış", True, "Metabolik oksijen talebi artışı"), ("Progesterona bağlı hiperventilasyon ve alkaloz", False, "")],
                [("Gastrointestinal Motilite", False, ""), ("Progesteron ile belirgin yavaşlama", False, ""), ("Gastroözofageal reflü ve safra stazı", True, "Düz kas gevşemesine bağlı klinik yakınma")]
            ]
        ),
        32: make_table(
            ["Anne Beslenmesini Bozan Risk Faktörü", "Klinik Eşik Değeri", "Gelişen Maternal-Fetal Patoloji"],
            [
                [("Uç Anne Yaşları", False, ""), ("18 yaş altı veya 35 yaş üstü", True, "Riskli gebelik yaş sınırları"), ("Adolesanda eklampsi ve IUGR; ileri yaşta kromozom anomalisi", False, "")],
                [("Büyük Multiparite", False, ""), ("4 ve üzeri doğum yapmış olmak", True, "Depoları tüketen doğum sayısı eşiği"), ("Maternal tükenmişlik sendromu ve ağır anemi", False, "")],
                [("Aşırı Fiziksel İş Yükü", False, ""), ("Ağır tarla veya beden işçiliği", False, ""), ("Negatif enerji dengesi ve fetal büyüme kısıtlılığı", True, "Kalori açığının fötal tartıdaki sonucu")]
            ]
        ),
        39: make_table(
            ["Beslenme Durumu", "Anne Üzerindeki Temel Sonuç", "Bebek Üzerindeki Temel Sonuç"],
            [
                [("Yetersiz Beslenme", False, ""), ("Doku yıkımı, anemi ve osteomalazi", True, "Annede kemik yumuşaması ve kan kaybı tablosu"), ("İntrauterin büyüme kısıtlılığı ve düşük doğum ağırlığı", False, "")],
                [("Aşırı Beslenme", False, ""), ("Gestasyonel diyabet, hipertansiyon ve zorunlu sezaryen", False, ""), ("Makrozomi, omuz distosisi ve neonatal hipoglisemi", True, "İri bebek ve doğum kanalı travması")]
            ]
        ),
        49: make_table(
            ["Gebelik Türü / Durum", "Önerilen Ağırlık Artışı", "Günlük Ek Enerji İhtiyacı"],
            [
                [("Normal Tekil Gebelik (Normal BKİ)", False, ""), ("11,5 - 16,0 kg toplam artış", False, ""), ("+340 kal/gün ek enerji", True, "Tekil gebelikte günlük ek kalori")],
                [("İkiz Gebelik", False, ""), ("16,8 - 24,5 kg toplam artış", False, ""), ("+600 kal/gün ek enerji", True, "İkiz gebelikte günlük ek kalori")],
                [("Üçüz Gebelik", False, ""), ("Yaklaşık 23 kg toplam artış", True, "Üçüz gebelik için önerilen kilo artışı"), ("+900 kal/gün ek enerji", True, "Üçüz gebelikte günlük ek kalori")]
            ]
        ),
        52: make_table(
            ["Esansiyel Besin Öğesi", "Gebelikte Günlük İhtiyaç / Ek", "Fetal ve Maternal Temel Fonksiyon"],
            [
                [("Protein", False, ""), ("Günlük diyete 20-25 g ek protein", True, "Günlük eklenmesi gereken protein gramı"), ("Fetüs, plasenta ve uterus dokularının sentezi (925 g)", False, "")],
                [("Kalsiyum", False, ""), ("Günlük 1000-1300 mg elementer kalsiyum", False, ""), ("Fetal iskelet mineralizasyonu (30 g) ve preeklampsi önleme", True, "Kemik gelişimi ve damar tonusu koruması")],
                [("Çinko (Zn)", False, ""), ("Tahıl fitatlarından uzak tüketim", False, ""), ("DNA polimeraz aktivitesi ve intrauterin büyüme", True, "Hücre bölünmesini sağlayan eser element rolü")]
            ]
        ),
        59: make_table(
            ["Besin Öğesi / Mineral", "Gebelikteki Temel Rolü", "Eksikliği veya Fazlalığının Riskleri"],
            [
                [("Protein", False, ""), ("Fetal ve maternal doku sentezi (toplam 925 g)", False, ""), ("Günlük 20-25 g eklenmezse kas yıkımı ve IUGR", True, "Protein açığında fötal büyüme kısıtlılığı")],
                [("İyot", False, ""), ("Tiroid hormonu ve fötal beyin korteksi gelişimi", False, ""), ("Kretenizm, sağırlık ve derin zeka geriliği", True, "İyot eksikliğinin ağır konjenital tablosu")],
                [("A Vitamini", False, ""), ("Görme pigmentleri ve organogenez kontrolü", False, ""), ("Fazlası yarık damak ve teratojenite yapar", True, "A vitamini toksisitesinin fötal anomalisi")]
            ]
        ),
        69: make_table(
            ["Parametre / Besin Öğesi", "Standart Durum / Değer", "Özel / Riskli Durum Değeri"],
            [
                [("Folik Asit Dozu", False, ""), ("Gebe kalmadan 3 ay önce 400 mcg/gün", False, ""), ("NTD öyküsünde 4000 mcg (4 mg/gün)", True, "Yüksek riskli gebedeki 10 kat doz")],
                [("Anemi Hemoglobin Eşiği", False, ""), ("1. ve 3. trimestrde Hb < 11,0 g/dl", False, ""), ("2. trimestrde Hb < 10,5 g/dl", True, "İkinci üç aydaki özel anemi sınırı")],
                [("Demir Emilim Verimi", False, ""), ("Diyetteki toplam demirin yüzde 10'u", False, ""), ("C vitamini ile 3 kat artış; çay ile blokaj", True, "Emilimi etkileyen besinsel faktörler")]
            ]
        ),
        74: make_table(
            ["Zararlı Madde / Alışkanlık", "Toksikolojik Kritik Eşik", "Fetal Patolojik Sonuç"],
            [
                [("Kafein (Kahve)", False, ""), ("Günde 5 fincandan fazla tüketim", True, "Yüksek riskli kahve tüketim adedi"), ("Erken doğum, DDA ve fetal kemik kalsiyum kaybı", False, "")],
                [("Alkol (Etanol)", False, ""), ("İlk trimestrde 60 g/gün üzeri tüketim", True, "FAS tetikleyen günlük saf alkol gramı"), ("Fetal Alkol Sendromu (FAS): Mikrosefali ve zeka geriliği", False, "")],
                [("Tütün (Sigara)", False, ""), ("Gebelikte tek bir dal dahi içilmesi", False, ""), ("Nikotin vazokonstriksiyonu ve karbonmonoksit hipoksisi ile DDA", True, "Tütünün fötal oksijeni kesme mekanizması")]
            ]
        ),
        79: make_table(
            ["Sağlık Bakanlığı Destek Programı", "Başlama ve Bitiş Zamanı", "Günlük Profilaktik Doz"],
            [
                [("Demir Destek Programı", False, ""), ("16. haftadan doğum sonu 3. aya (toplam 9 ay)", False, ""), ("Günlük 40-60 mg elementer demir", True, "Ulusal demir destek dozu")],
                [("D Vitamini Destek Programı", False, ""), ("12. haftadan doğum sonu 6. aya kadar", False, ""), ("Günlük 1200 IU (9 damla)", True, "Ulusal D vitamini profilaksi dozu")]
            ]
        ),
        82: make_table(
            ["Gastrointestinal Yakınma", "Tetikleyici Neden", "Besinsel / Yaşam Tarzı Çözümü"],
            [
                [("Sabah Bulantısı", False, ""), ("hCG piki ve sabah mide asidi birikimi", False, ""), ("Sabah kalkmadan tuzlu kraker atıştırmak", True, "Boş mide asidini nötralize eden kuru gıda")],
                [("Kabızlık (Konstipasyon)", False, ""), ("Progesteron düz kas hipomotilitesi", False, ""), ("Günde 8-12 bardak sıvı ve posalı beslenme", True, "Bağırsak pasajını açan sıvı hedefi")],
                [("Pika Sendromu", False, ""), ("Doku demir ve çinko açlığı", True, "Besin dışı madde aşermesini tetikleyen mineral açığı"), ("Demir preparatı replasmanı ve diyet desteği", False, "")]
            ]
        ),
        89: make_table(
            ["Gebelik Sağlık Sorunu", "Temel Patofizyolojik Neden", "Önerilen Besinsel ve Davranışsal Tedavi"],
            [
                [("Sabah Bulantısı", False, ""), ("hCG piki ve açlıkta biriken mide asidi", False, ""), ("Yataktan kalkmadan tuzlu kraker atıştırmak", True, "Sabah bulantısını kesen kuru gıda taktiği")],
                [("Mide Yanması (Reflü)", False, ""), ("AÖS sfinkter gevşemesi ve uterusun basısı", False, ""), ("Yemekten sonra yatmama ve başı yüksekte uyuma", True, "Reflüyü engelleyen yatış kuralı")],
                [("Konstipasyon (Kabızlık)", False, ""), ("Progesteron hipomotilitesi ve demir hapları", False, ""), ("Günde 8-12 bardak sıvı ve posalı beslenme", True, "Bağırsak pasajını açan sıvı ve lif hedefi")]
            ]
        ),
        91: make_table(
            ["Bebek Yaşı", "Mide Kapasitesi Hacmi", "Beslenme Sıklığı ve Modeli"],
            [
                [("1. Ay", False, ""), ("120 - 150 ml mide hacmi", True, "İlk aydaki mide dolum kapasitesi"), ("2-3 saatte bir sadece anne sütü", False, "")],
                [("3. Ay", False, ""), ("150 - 180 ml mide hacmi", True, "Üçüncü aydaki mide hacmi"), ("Günde 6-8 kez eksklüzif emzirme", False, "")],
                [("6. Ay", False, ""), ("180 - 210 ml mide hacmi", True, "Altıncı aydaki mide hacmi"), ("Anne sütü + tamamlayıcı besinlere geçiş", False, "")]
            ]
        ),
        96: make_table(
            ["Riskli Besin Maddesi", "Taşıdığı Biyolojik / Kimyasal Tehlike", "Fetal ve Maternal Klinik Sonuç"],
            [
                [("Pastörize Edilmemiş Süt ve Peynir", False, ""), ("Listeria monocytogenes bakterisi", True, "Soğukta üreyen çiğ süt bakterisi"), ("Koryoamniyonit, dissemine sepsis ve ölü doğum", False, "")],
                [("Çiğ Et ve Şarküteri Ürünleri", False, ""), ("Toxoplasma gondii paraziti ve nitritler", False, ""), ("Konjenital toksoplazmozis, koryoretinit ve mikrosefali", True, "Çiğ etten bulaşan göz-beyin anomalisi")],
                [("Büyük Yırtıcı Dip Balıkları", False, ""), ("Ağır metal metil cıva birikimi", True, "Dip balıklarındaki nörotoksik metal"), ("Fetal serebral korteks tahribatı ve serebral palsi", False, "")]
            ]
        ),
        99: make_table(
            ["Dönem / Durum", "Günlük Ek Enerji İhtiyacı", "Temel Besin Grubu Özelliği"],
            [
                [("Normal Gebelik Dönemi", False, ""), ("Günlük ortalama +340 kalori", False, ""), ("Tahıllarda ek porsiyona gerek yoktur", True, "Gebelikte tahıl artırılmama kuralı")],
                [("Emziklilik Dönemi (İlk 6 Ay)", False, ""), ("Günlük ortalama +500 kalori", True, "Emziklilikteki ek kalori miktarı"), ("Ek 15 g protein ve +1,5 porsiyon tahıl", False, "")],
                [("Yetersiz Beslenme (<1800 kal)", False, ""), ("Günlük 1800 kalorinin altı", False, ""), ("Anne sütü salgılanması belirgin düşer", True, "Aşırı kalori kısıtlamasının laktasyonel sonucu")]
            ]
        ),
        100: make_table(
            ["Halk Sağlığı Hedefi", "Uluslararası Altın Standart", "Ulusal Sağlık Bakanlığı Protokolü"],
            [
                [("Folik Asit Desteği", False, ""), ("Gebe kalmadan 3 ay önce 400 mcg/gün", False, ""), ("Aile hekimliklerinde prekonsepsiyonel danışmanlık", True, "Birinci basamak folat bilgilendirmesi")],
                [("Profilaktik Demir", False, ""), ("Tüm gebelere anemi önleme desteği", False, ""), ("16. haftadan doğum sonu 3. aya 40-60 mg", True, "9 aylık ulusal demir standardı")],
                [("D Vitamini Takviyesi", False, ""), ("Güneşlenme ve diyet desteği", False, ""), ("12. haftadan doğum sonu 6. aya 1200 IU", True, "Bebek ve anne kemik koruma dozu")]
            ]
        ),
        15: make_table(
            ["Doğum Sonu Kanama (PPH) 4T Kuralı", "Etiyolojik Komponent", "Klinik Yönetim Yaklaşımı"],
            [
                [("Tone (Tonus)", False, ""), ("Uterin atoni (yüzde 70 en sık sebep)", True, "Uterus gevşekliğinin etiyolojik payı"), ("Fundus masajı ve IV oksitosin infüzyonu", False, "")],
                [("Tissue (Doku)", False, ""), ("Plasenta veya kotiledon retansiyonu", True, "Parça kalması patolojisi"), ("Manuel kavite kontrolü ve küretaj", False, "")],
                [("Trauma (Travma)", False, ""), ("Servikal veya vajinal laserasyon", False, ""), ("Cerrahi sütürasyon ve doku onarımı", True, "Yırtıkların primer kapatılması")]
            ]
        ),
        45: make_table(
            ["Çoğul Gebelik Tipi", "Önerilen Toplam Ağırlık Artışı", "Günlük Ek Enerji İhtiyacı"],
            [
                [("Tekil Gebelik (Normal BKİ)", False, ""), ("11,5 - 16,0 kg ağırlık artışı", False, ""), ("Günlük +340 kalori", False, "")],
                [("İkiz Gebelik", False, ""), ("16,8 - 24,5 kg ağırlık artışı", True, "İkiz gebelikte önerilen kilo koridoru"), ("Günlük +600 kalori", False, "")],
                [("Üçüz Gebelik", False, ""), ("Yaklaşık 23 kg ağırlık artışı", True, "Üçüz gebelikte hedeflenen toplam tartı"), ("Günlük +900 kalori", False, "")]
            ]
        ),
        65: make_table(
            ["Demir İhtiyacı Kompartmanı", "Tüketilen Net Demir Miktarı", "Biyolojik Fonksiyonu"],
            [
                [("Maternal Eritrosit Genişlemesi", False, ""), ("Yaklaşık 450 - 500 mg demir", True, "Genişleyen alyuvar kitlesinin demir payı"), ("Genişleyen plazma hacminde oksijen taşınması", False, "")],
                [("Fötus ve Plasenta Dokusu", False, ""), ("Yaklaşık 300 - 350 mg demir", True, "Fetal karaciğer depolarına çekilen demir"), ("Fetal büyüme ve ilk 6 ayın demir deposu", False, "")],
                [("Doğum Kan Kaybı ve Bazal Kayıp", False, ""), ("Yaklaşık 400 - 450 mg demir", False, ""), ("Doğumdaki fizyolojik kayıp ve dökülen hücreler", True, "Maternal kan kaybı ve cilt kayıpları")]
            ]
        )
    }

    return tables

if __name__ == "__main__":
    q, c, s, b, t = get_21_quizzes(), get_21_chains(), get_21_sliders(), get_21_branchings(), get_21_tables()
    print(f"Hazırlanan tam envanter: Quizzes={len(q)}, Chains={len(c)}, Sliders={len(s)}, Branchings={len(b)}, Tables={len(t)}")
