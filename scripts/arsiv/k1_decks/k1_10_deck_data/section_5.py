"""
Kromozomal Hastalıklar ve Genetik Danışma (Ders 10) - Bölüm 5 (Slayt 41 - 50)
Konu: Edwards Sendromu (Trizomi 18), Patau Sendromu (Trizomi 13) ve Trizomilerin Karşılaştırmalı Analizi
Checkpoint: Slayt 49 ([TEKRAR SAYFASI - CHECKPOINT 5])
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_5_slides():
    return [
        # Slayt 41
        {
            "title": "Edwards Sendromu (Trizomi 18): Epidemiyoloji ve Fetal Seyir",
            "subtitle": "Canlı Doğan İkinci En Sık Otozomal Trizomi ve Ağır Mortalite",
            "badge": "Edwards Sendromu",
            "coreContent": {
                "text": "Edwards sendromu (Trizomi 18 [47,+18]), canlı doğan bebekler arasında Down sendromundan sonra en sık görülen ikinci otozomal trizomidir. Canlı doğumlardaki sıklığı yaklaşık 1/750 ila 1/6000 arasındadır. Trizomi 18 olgularının yaklaşık %95'i intrauterin dönemde spontan abortus veya intrauterin fetal ölüm (IUFD) ile kaybedilir. Canlı doğmayı başaran bebeklerin de prognozu son derece kasvetlidir: canlı doğanların %50'si yaşamın ilk haftasında, yaklaşık %90'ı ise ilk bir yıl içinde çoklu organ yetmezliği veya kardiyorespiratuvar arrest nedeniyle kaybedilir; 1 yaşını geçebilenler yalnız %5-10'luk küçük bir gruptur. Kız cinsiyette görülme oranı erkeklere göre belirgin derecede fazladır (canlı doğanların ~%80'i kızdır). Etiyolojide olguların %70'i mayotik ayrılamamadan (%95 maternal kökenli ve ileri anne yaşıyla ilişkili), %20'si translokasyonlardan ve geri kalanı mozaisizmden kaynaklanır.",
                "keyBullets": [
                    {"title": "Görülme Sıklığı", "desc": "Canlı doğan ikinci en sık trizomidir (yaklaşık 1/750 canlı doğum).", "isKey": True},
                    {"title": "Ağır Mortalite", "desc": "Canlı doğanların %50'si ilk hafta, %90'ı ilk bir yıl içinde kaybedilir.", "isKey": True},
                    {"title": "Kız Baskınlığı", "desc": "Canlı doğan Trizomi 18 bebeklerinin yaklaşık %80'i kız cinsiyettedir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_cloze(
                    "Edwards sendromu (Trizomi 18) tanılı canlı doğan bebeklerin yaklaşık %80'i kız cinsiyettedir.",
                    "%80",
                    "Kız cinsiyet oranını düşününüz"
                ),
                make_table(
                    ["Klinik Parametre", "Edwards Sendromu (Trizomi 18)", "Prognoz / Önemi"],
                    [
                        [("Canlı Doğum Sıklığı", False, ""), ("~1/750 canlı doğum (ders slaytı)", True, "İkinci en sık trizomi"), ("Down'dan sonraki en yaygın otozomal anöploidi", False, "")],
                        [("Spontan Düşük Oranı", False, ""), ("Konsepsiyonların %95'i düşükle sonuçlanır", True, "Aşırı yüksek intrauterin seleksiyon"), ("Yalnızca %5'i canlı doğuma ulaşabilir", False, "")],
                        [("İlk Hafta Mortalitesi", False, ""), ("Canlı doğanların %50'si ilk hafta kaybedilir", True, "İlk 7 gün kaybı"), ("Ağır konjenital kalp ve solunum yetmezliği", False, "")],
                        [("Etiyolojik Dağılım", False, ""), ("%70 ayrılamama, %20 translokasyon", True, "Translokasyon oranı nispeten yüksek"), ("Translokasyonlarda parental karyotip şarttır", False, "")]
                    ]
                ),
                make_active_recall(
                    "Edwards sendromlu canlı doğan bebeklerin yaklaşık yarısı (%50) yaşamın hangi zaman diliminde kaybedilir?",
                    "Yaşamın ilk haftasında (ilk 7 gün içinde) kaybedilir.",
                    "İlk hafta mortalite oranı"
                )
            ],
            "spotPearls": [
                "Edwards sendromu (Trizomi 18) canlı doğan ikinci en sık trizomidir (1/750).",
                "Canlı doğanların %50'si ilk hafta ölür; %90'ı ilk yılı göremez; %80'i kızdır.",
                "Etiyolojide %70 ayrılamama, %20 translokasyon rol oynar."
            ]
        },

        # Slayt 42
        {
            "title": "Edwards Sendromunun Karakteristik Dismorfolojisi: Clenched Hand ve Rocker-Bottom Ayak",
            "subtitle": "Karakteristik Fleksiyon Kontraktürleri ve İskelet Deformiteleri",
            "badge": "Edwards Dismorfolojisi",
            "coreContent": {
                "text": "Edwards sendromlu bir yenidoğanın fizik muayenesinde patognomonik sayılabilecek derecede spesifik iskelet ve ekstremite deformiteleri izlenir. En karakteristik el bulgusu 'clenched hand' (kenetlenmiş yumruk el) manzarasıdır: parmaklar sıkı bir yumruk şeklinde fleksiyondadır; 2. parmak (işaret parmağı) 3. parmağın üzerine, 5. parmak (küçük parmak) ise 4. parmağın üzerine çaprazlama biner (örtüşen parmaklar / overlapping fingers). Başparmak ve tırnaklar hipoplaziktir. Ayak muayenesinde en tipik bulgu 'rocker-bottom ayak' (beşik taban / külbütör taban ayağı) deformitesidir; belirgin kalkaneus çıkıntısı ve konveks ayak tabanı ile karakterizedir. Başta belirgin çıkıntılı bir oksiput (prominent oksiput), düşük yerleşimli ve malforme faun kulaklar, dar palpebral fissürler ve belirgin mikrognati (küçük çene) dikkati çeker.",
                "keyBullets": [
                    {"title": "Clenched Hand", "desc": "2. parmağın 3.'nün, 5. parmağın 4.'nün üzerine bindiği sıkı yumruk eldir.", "isKey": True},
                    {"title": "Rocker-Bottom Ayak", "desc": "Belirgin kalkaneus ve konveks tabanlı beşik ayak deformitesidir.", "isKey": True},
                    {"title": "Belirgin Oksiput", "desc": "Kafatası arkaya doğru çıkıntılıdır; mikrognati ve faun kulaklar eşlik eder.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Down Sendromu vs Edwards Sendromu Ekstremite Muayenesi",
                    "Down Sendromu Ekstremiteleri",
                    "Geniş ve kısa eller, tek transvers palmar çizgi (Simian çizgisi), 5. parmakta klinodaktili, ayak 1-2. parmakta sandal gap.",
                    "Edwards Sendromu Ekstremiteleri",
                    "Clenched hand (2. ve 5. parmakların iç parmaklar üzerine bindiği yumruk el), hipoplastik tırnaklar, rocker-bottom (beşik taban) ayak."
                ),
                make_micro_quiz(
                    "Yenidoğan yoğun bakım ünitesinde değerlendirilen bir dismorfik bebekte belirgin oksiput çıkıntısı, 2. ve 5. parmakların diğer parmaklar üzerine bindiği kenetlenmiş yumruk el (clenched hand) ve beşik taban ayak (rocker-bottom foot) saptanıyor. En olası ön tanı hangisidir?",
                    {
                        "A": "Down Sendromu (Trizomi 21)",
                        "B": "Patau Sendromu (Trizomi 13)",
                        "C": "Edwards Sendromu (Trizomi 18)",
                        "D": "Turner Sendromu (45,X)",
                        "E": "Klinefelter Sendromu (47,XXY)"
                    },
                    "C",
                    {
                        "A": "Down sendromunda hipotoni ve Simian çizgisi görülür.",
                        "B": "Patau'da polidaktili, yarık damak/dudak ve mikroftalmi triadı vardır.",
                        "C": "Doğru cevap C'dir: Clenched hand, belirgin oksiput ve rocker-bottom ayak Edwards sendromunun (Trizomi 18) klasik bulgularıdır.",
                        "D": "Turner'da yele boyun ve ödem görülür.",
                        "E": "Klinefelter yenidoğanda dismorfik bulgu vermez."
                    }
                ),
                make_cloze(
                    "Edwards sendromunda el parmaklarının üst üste bindiği sıkı yumruk el deformitesine tıbbi literatürde clenched hand adı verilir.",
                    "clenched hand",
                    "Yumruk el teriminin İngilizce/Latince karşılığını anımsayınız"
                )
            ],
            "spotPearls": [
                "Edwards sendromunun (Trizomi 18) kardinal bulguları: CLENCHED HAND ve ROCKER-BOTTOM ayaktır.",
                "Belirgin oksiput çıkıntısı ve faun kulaklar tipiktir.",
                "Parmakların üst üste binmesi (2. parmak 3.'nün, 5. parmak 4.'nün üzerinde) patognomoniktir."
            ]
        },

        # Slayt 43
        {
            "title": "Edwards Sendromunda Sistemik Anomaliler, Mikrosefali ve Hipertonisite",
            "subtitle": "Down Sendromundan Tonus Farkı: İnfantil Hipertonisite",
            "badge": "Sistemik Tutulum",
            "coreContent": {
                "text": "Edwards sendromunda klinik tabloyu Down sendromundan ayıran en temel nörolojik muayene farkı kas tonusudur. Down sendromunda gevşek genel hipotoni hakimken, Edwards sendromlu bebeklerde belirgin kas hipertonisitesi (spastisite ve fleksör sertlik) dikkati çeker. Fetal dönemde azalmış fetal hareketler, polihidramnios, küçük plasenta ve tek umblikal arter (2 damarlı kordon) sık saptanan ultrasonografik belirteçlerdir. Neredeyse tüm olgularda (%95+) ağır konjenital kalp hastalıkları bulunur; en sık lezyonlar Ventriküler Septal Defekt (VSD), Patent Duktus Arteriyozus (PDA) ve aortik/pulmoner kapak anomalileridir. Üriner sistemde at nalı böbrek, kistik böbrek displazisi ve hidronefroz olguların yarısından fazlasında mevcuttur. Gastrointestinal sistemde Meckel divertikülü ve omfalosel eşlik edebilir. Şiddetli mikrosefali ve derin psikomotor mental gerilik kaçınılmazdır.",
                "keyBullets": [
                    {"title": "Kas Tonusu Zıtlığı", "desc": "Down sendromundaki hipotoninin aksine Edwards sendromunda HİPERTONİSİTE hakimdir.", "isKey": True},
                    {"title": "Prenatal İpuçları", "desc": "Tek umblikal arter, küçük plasenta, polihidramnios ve azalmış fetal aktivite.", "isKey": True},
                    {"title": "Organ Tutulumu", "desc": "VSD, PDA, at nalı böbrek ve omfalosel son derece yaygındır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Down vs Edwards: Kas Tonusu Karşılaştırması",
                    "Down Sendromu Tonusu",
                    "Aşırı gevşek infantil hipotoni ('bez bebek' manzarası); eklemlerde aşırı hipermobilite ve laksisite.",
                    "Edwards Sendromu Tonusu",
                    "Belirgin infantil hipertonisite; kaslarda spastik rijidite ve inatçı fleksiyon kontraktürleri."
                ),
                make_micro_quiz(
                    "Aşağıdaki yenidoğan klinik bulgularından hangisi Down sendromunda değil, karakteristik olarak Edwards sendromunda (Trizomi 18) gözlenir?",
                    {
                        "A": "Belirgin infantil genel hipotoni",
                        "B": "Belirgin kas hipertonisitesi",
                        "C": "Brushfield lekeleri",
                        "D": "Endokardiyal yastık defekti (AVSD)",
                        "E": "Duodenal atrezi"
                    },
                    "B",
                    {
                        "A": "Hipotoni Down sendromunun özelliğidir.",
                        "B": "Doğru cevap B'dir: Kas hipertonisitesi Edwards sendromunun karakteristik bulgusudur; Down'da hipotoni vardır.",
                        "C": "Brushfield lekeleri Down sendromuna özgüdür.",
                        "D": "AVSD Down sendromuna özgüdür.",
                        "E": "Duodenal atrezi Down sendromunda tipiktir."
                    }
                ),
                make_cloze(
                    "Down sendromundaki belirgin kas hipotonisinin aksine, Edwards sendromlu bebeklerin nörolojik muayenesinde belirgin hipertonisite saptanır.",
                    "hipertonisite",
                    "Artmış kas tonusu terimini anımsayınız"
                )
            ],
            "spotPearls": [
                "Edwards sendromunda kas tonusu HİPERTONİKTİR (Down'da hipotoniktir).",
                "Tek umblikal arter ve at nalı böbrek Edwards sendromunda son derece sıktır.",
                "Ağır konjenital kalp hastalığı (%95+) erken ölümün ana nedenidir."
            ]
        },

        # Slayt 44
        {
            "title": "Patau Sendromu (Trizomi 13): Epidemiyoloji ve Fetal Letalite",
            "subtitle": "Canlı Doğan En Nadir ve En Yıkıcı Otozomal Trizomi",
            "badge": "Patau Sendromu",
            "coreContent": {
                "text": "Patau sendromu (Trizomi 13 [47,+13]), canlı doğumla bağdaşan üç büyük otozomal trizomi arasında en nadir görülen ve en ağır seyirli olanıdır. Canlı doğumlardaki görülme sıklığı yaklaşık 1/5000 ila 1/10000 arasındadır. Konsepsiyonların %95'ten fazlası intrauterin dönemde spontan düşükle sonuçlanır; tüm kromozomal spontan abortus materyallerinin yaklaşık %15'ini Trizomi 13 konsepsiyonları oluşturur. Canlı doğan bebeklerde sağkalım son derece kısıtlıdır: olguların yaklaşık %50'si yaşamın ilk ayında, %90'ından fazlası ise ilk bir yıl içinde kaybedilir. Etiyolojide olguların %80'i mayotik ayrılamamadan (ileri maternal yaşla güçlü ilişkili), %20'si ise Robertsonian translokasyonlardan [özellikle rob(13;14)] kaynaklanır. Bu yüksek translokasyon oranı nedeniyle Patau sendromlu bebeklerin ebeveynlerine de mutlaka sitogenetik analiz yapılmalıdır.",
                "keyBullets": [
                    {"title": "Görülme Sıklığı", "desc": "Yaklaşık 1/5000 canlı doğumda görülür; canlı trizomilerin en nadiridir.", "isKey": True},
                    {"title": "Ağır Mortalite", "desc": "Canlı doğanların %90'ından fazlası ilk yıl içinde hayatını kaybeder.", "isKey": True},
                    {"title": "Translokasyon Payı (%20)", "desc": "Olguların %20'si Robertsonian translokasyon [rob(13;14)] kaynaklıdır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Klinik Parametre", "Patau Sendromu (Trizomi 13)", "Klinik Yorum"],
                    [
                        [("Canlı Doğum Sıklığı", False, ""), ("~1/5000 canlı doğum (ders slaytı)", True, "Canlı doğan en nadir trizomi"), ("Down ve Edwards'a göre daha seyrektir", False, "")],
                        [("Abortuslardaki Payı", False, ""), ("Spontan düşüklerin yaklaşık %15'i", True, "Düşüklerdeki yüksek pay"), ("İntrauterin seleksiyon son derece şiddetlidir", False, "")],
                        [("1 Yaş Sağkalımı", False, ""), ("%10'dan az (%90+ ilk yıl ölür)", True, "Aşırı düşük sağkalım"), ("En ağır seyirli canlı doğum trizomisidir", False, "")],
                        [("Translokasyon Oranı", False, ""), ("%20 [çoğunlukla rob(13;14)]", True, "Beşte bir oranında translokasyon"), ("Ebeveyn karyotipi kesinlikle incelenmelidir", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Patau sendromu (Trizomi 13) olgularının etiyolojik dağılımında Robertsonian translokasyonların payı yaklaşık yüzde kaçtır?",
                    {
                        "A": "Yaklaşık %1",
                        "B": "Yaklaşık %4",
                        "C": "Yaklaşık %20",
                        "D": "Yaklaşık %50",
                        "E": "Yüzde 95"
                    },
                    "C",
                    {
                        "A": "Mozaiklik oranıdır.",
                        "B": "Down sendromundaki translokasyon oranıdır (%4).",
                        "C": "Doğru cevap C'dir: Patau sendromu olgularının yaklaşık %20'si Robertsonian translokasyona [genellikle rob(13;14)] bağlıdır.",
                        "D": "Çok yüksektir.",
                        "E": "Klasik trizomi oranıdır."
                    }
                ),
                make_active_recall(
                    "Patau sendromuna (Trizomi 13) yol açan Robertsonian translokasyonlar arasında en sık görülen spesifik kromozomal füzyon hangisidir?",
                    "rob(13;14) sentrik füzyonudur.",
                    "13. kromozomu içeren en sık füzyon"
                )
            ],
            "spotPearls": [
                "Patau sendromu canlı doğan en nadir ve en ağır trizomidir (1/5000).",
                "Olguların %90'ından fazlası ilk bir yıl içinde kaybedilir.",
                "Etiyolojide Robertsonian translokasyon payı %20'dir [özellikle rob(13;14)]."
            ]
        },

        # Slayt 45
        {
            "title": "Patau Sendromunda Holoprozensefali ve Santral Sinir Sistemi Kusurları",
            "subtitle": "Ön Beyin Segmentasyon Kusuru ve Ağır Nörogelişimsel Hasar",
            "badge": "Holoprozensefali",
            "coreContent": {
                "text": "Patau sendromunun (Trizomi 13) patofizyolojik ve morfolojik omurgasını, embriyonik ön beynin (prozensefalon) iki ayrı hemisfere bölünememesiyle karakterize holoprozensefali malformasyonu oluşturur. Prekordal mezenkimin indüksiyon kusuru sonucu gelişen bu anomalide serebral hemisferler tek bir ortak ventrikül etrafında kaynaşmış olarak kalır; korpus kallozum agenezisi, koku soğancığı (olfaktör bulbus) yokluğu (arhinensefali) ve optik kiyazma anomalileri eşlik eder. Holoprozensefali nörolojik tablonun yanı sıra orta hat yüz yapılarının gelişimini de doğrudan yıkar. Bu durum yüzün orta hattında siklopi (tek göz), probosis (tüp burun), ağır hipotelorizm veya etmosefali gibi aşırı ağır kraniofasiyal anomalilere yol açar. Ağır nöbetler ve derin koma tablosu erken yenidoğan ölümlerinin en önemli santral nedenidir.",
                "keyBullets": [
                    {"title": "Holoprozensefali", "desc": "Ön beynin iki hemisfere bölünememesi kusurudur; Trizomi 13'ün ana patolojisidir.", "isKey": True},
                    {"title": "Orta Hat Yıkımı", "desc": "Beyin kusuru orta hat yüz anomalilerine (hipotelorizm, siklopi, probosis) yol açar.", "isKey": True},
                    {"title": "Kranial Anomaliler", "desc": "Arhinensefali (koku soğancığı yokluğu) ve korpus kallozum agenezisi sıktır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Trizomi 13'te Holoprozensefali Gelişim Zinciri",
                    [
                        "1. 13. kromozomdaki gelişimsel genlerin trizomik dozajı prekordal plağın indüksiyonunu bozar",
                        "2. Embriyogenezin 4-5. haftasında prosensefalon sağ ve sol telensefalik veziküllere ayrılamaz",
                        "3. Serebral korteks tek bir ortak monoventrikül şeklinde kaynaşık kalır",
                        "4. Yüzün orta hat göçü duraklar; yarık damak, hipotelorizm ve şiddetli orta hat defektleri gelişir"
                    ]
                ),
                make_cloze(
                    "Patau sendromunda ön beynin iki hemisfere ayrılamamasıyla karakterize majör santral sinir sistemi malformasyonuna holoprozensefali denir.",
                    "holoprozensefali",
                    "Ön beyin bölünme kusuru terimini anımsayınız"
                ),
                make_active_recall(
                    "Trizomi 13 (Patau) sendromunda koku duyusu ile ilgili beyin yapılarının (olfaktör bulbus ve traktus) konjenital yokluğuna ne ad verilir?",
                    "Arhinensefali (arhinencephaly) adı verilir.",
                    "Koku soğancığı agenezisi"
                )
            ],
            "spotPearls": [
                "Patau sendromunun (Trizomi 13) ana beyin patolojisi HOLOPROZENSEFALİDİR.",
                "Holoprozensefali orta hat yüz yapılarının gelişimini yıkar (yarık dudak, hipotelorizm, probosis).",
                "Arhinensefali ve korpus kallozum agenezisi Trizomi 13'te tipiktir."
            ]
        },

        # Slayt 46
        {
            "title": "Patau Sendromunun Karakteristik Triadı: Mikroftalmi + Yarık Dudak/Damak + Polidaktili",
            "subtitle": "Klinik Tanıda Yüksek Özgüllüğe Sahip Üçlü Stigma",
            "badge": "Karakteristik Triad",
            "coreContent": {
                "text": "Patau sendromunun klinik tanısında hekime en yüksek tanısal özgüllüğü sağlayan klasik bir klinik triad tanımlanmıştır: Mikroftalmi/Anoftalmi + Bilateral Yarık Dudak/Damak + Postaksiyel Polidaktili. Bu üç bulgunun bir arada saptanması aksi kanıtlanana kadar Trizomi 13'ü düşündürür. Gözlerde aşırı küçülme (mikroftalmi) veya tam yokluk (anoftalmi), iriste kolobom ve retina displazisi görülür. Yüzde orta hat defektlerine bağlı geniş bilateral yarık dudak ve yarık damak mevcuttur. Ekstremitelerde ise ellerde ve bazen ayaklarda serçe parmağın (veya 5. parmağın) yanında fazladan bir parmağın bulunması şeklinde tanımlanan postaksiyel polidaktili olguların yaklaşık %70'inde saptanır. Bu üçlü bulgu kümesi, yenidoğanda Patau sendromu ile Edwards sendromunu fizik muayenede saniyeler içinde ayırt etmeyi sağlar.",
                "keyBullets": [
                    {"title": "Patau Triadı", "desc": "Mikroftalmi/anoftalmi + Yarık dudak/damak + Postaksiyel polidaktili.", "isKey": True},
                    {"title": "Göz Patolojileri", "desc": "Mikroftalmi, kolobom ve retina displazisi tipik nöroektodermal anomalilerdir.", "isKey": True},
                    {"title": "Postaksiyel Polidaktili", "desc": "5. parmak (küçük parmak) tarafındaki fazla parmaktır; olguların çoğunda görülür.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Triad Bileşeni", "Morfolojik Özellik", "Embriyolojik / Patolojik Köken"],
                    [
                        [("Mikroftalmi / Anoftalmi", False, ""), ("Göz küresinin aşırı küçük veya yok olması", True, "Göz küresi hipoplazisi"), ("Optik vezikül gelişim kusuru", False, "")],
                        [("Yarık Dudak ve Damak", False, ""), ("Bilateral geniş orofasiyal yarıklar", True, "Maksiller ve medial nazal füzyon kusuru"), ("Maksiller çıkıntıların orta hatta birleşememesi", False, "")],
                        [("Postaksiyel Polidaktili", False, ""), ("5. parmağın yanında fazladan parmak", True, "Serçe parmak tarafı fazla parmak"), ("Ekstremite tomurcuğu apikal ektodermal sırt kusuru", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Yenidoğan muayenesinde saptanan mikroftalmi, bilateral yarık dudak/damak ve postaksiyel polidaktili triadı aşağıdaki kromozomal sendromlardan hangisi için patognomoniktir?",
                    {
                        "A": "Down Sendromu (Trizomi 21)",
                        "B": "Edwards Sendromu (Trizomi 18)",
                        "C": "Patau Sendromu (Trizomi 13)",
                        "D": "Turner Sendromu (45,X)",
                        "E": "Wolf-Hirschhorn Sendromu (4p-)"
                    },
                    "C",
                    {
                        "A": "Down sendromunda polidaktili veya anoftalmi beklenmez.",
                        "B": "Edwards'ta clenched hand ve rocker-bottom ayak vardır.",
                        "C": "Doğru cevap C'dir: Mikroftalmi + yarık dudak/damak + polidaktili klasik Patau sendromu (Trizomi 13) triadıdır.",
                        "D": "Turner'da kısa boy ve yele boyun görülür.",
                        "E": "Wolf-Hirschhorn'da miğfer yüzü ve mikrosefali vardır."
                    }
                ),
                make_cloze(
                    "Patau sendromunda el ve ayaklarda 5. parmağın lateralinde fazladan parmak bulunması anomalisine postaksiyel polidaktili adı verilir.",
                    "postaksiyel",
                    "Ulnar / fibular taraf fazla parmak terimini düşününüz"
                )
            ],
            "spotPearls": [
                "Patau sendromunun klasik triadı: MİKROFTALMİ + YARIK DUDAK/DAMAK + POLİDAKTİLİDİR.",
                "Polidaktili genellikle postaksiyeldir (5. parmak yanında).",
                "Bu triad Trizomi 13'ü diğer tüm trizomilerden ayıran en spesifik klinik tablodur."
            ]
        },

        # Slayt 47
        {
            "title": "Patau Sendromunda Kutis Aplazi (Oksipital Skalp Defekti) ve Omfalosel",
            "subtitle": "Karakteristik Cilt ve Karın Duvarı Malformasyonları",
            "badge": "Kutis Aplazi ve Omfalosel",
            "coreContent": {
                "text": "Patau sendromunda (Trizomi 13) triada ek olarak tanı koydurucu değeri son derece yüksek olan diğer iki kardinal fizik muayene bulgusu kutis aplazi ve omfaloseldir. Kutis aplazi (aplasia cutis congenita), saçlı deride özellikle verteks ve parieto-oksipital bölgede cildin ve saç foliküllerinin konjenital yokluğu ile karakterize fokal ülseratif veya zarsı cilt defektidir; bebeğin başında zımba ile delinmiş gibi yuvarlak, cildi eksik alanlar şeklinde görülür. İkinci majör bulgu karın duvarının embriyonik kapanma defekti olan omfaloseldir; bağırsakların ve bazen karaciğerin göbek kordonunun içine doğru periton ve amniyon zarlarıyla örtülü bir kese içinde fıtıklaşmasıdır. Patau sendromlu bebeklerde ayrıca alında alev hemanjiomları (kapiller hemanjiomlar), mikrosefali, eğimli alın ve polikistik böbrekler yaygın olarak izlenir.",
                "keyBullets": [
                    {"title": "Kutis Aplazi", "desc": "Kafa derisinde (saçlı deride) zımba deliği gibi cildin doğumsal yokluğudur.", "isKey": True},
                    {"title": "Omfalosel", "desc": "Karın içi organların amniyon zarlı bir kese içinde göbek tabanından fıtıklaşmasıdır.", "isKey": True},
                    {"title": "Kapiller Hemanjiom", "desc": "Özellikle alında ve yüzde yaygın vasküler lekelenmeler dikkati çeker.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Patau Ek Bulguları: Kutis Aplazi vs Omfalosel",
                    "Kutis Aplazi (Aplasia Cutis)",
                    "Oksipital saçlı deride tam kat cilt ve saç dokusu yokluğu; zarsı veya kabuklu yuvarlak defekt.",
                    "Omfalosel (Omphalocele)",
                    "Göbek kordonu kökünde, periton ve amniyonla çevrili kese içinde bağırsak herniasyonu."
                ),
                make_cloze(
                    "Patau sendromlu bebeklerin saçlı derisinde cildin konjenital yokluğuyla karakterize oksipital defekte kutis aplazi veya aplasia cutis denir.",
                    "kutis aplazi",
                    "Saçlı deri yokluğu tıbbi terimini anımsayınız"
                ),
                make_active_recall(
                    "Trizomi 13 olgularında karın duvarının kapanma defekti sonucu bağırsakların zarlı bir kese içinde dışarıda bulunması malformasyonuna ne ad verilir?",
                    "Omfalosel (omphalocele) adı verilir.",
                    "Zarlı göbek fıtıklaşması"
                )
            ],
            "spotPearls": [
                "Kutis aplazi (saçlı deride zımba deliği gibi cilt defekti) Trizomi 13 için çok karakteristiktir.",
                "Omfalosel Trizomi 13 ve Trizomi 18 olgularında sık görülen bir karın duvarı defektidir.",
                "Alında kapiller hemanjiomlar Patau sendromunda sık saptanan vasküler stigmattır."
            ]
        },

        # Slayt 48
        {
            "title": "Üç Majör Canlı Trizominin Karşılaştırmalı Ayrımı: 21 vs 18 vs 13",
            "subtitle": "Klinik, Tonus, Organ Tutulumu ve Prognoz Karşılaştırma Matrisi",
            "badge": "Trizomi Karşılaştırması",
            "coreContent": {
                "text": "Tıp fakültesi klinik sınavlarında ve TUS'ta canlı doğan üç majör otozomal trizominin (Down, Edwards, Patau) birbirleriyle ayırıcı tanısı en yüksek verimli soru alanlarından biridir. Bu üç sendromun karşılaştırmalı analizi şu eksenlerde kurgulanır: (1) Kas tonusu: Down sendromunda belirgin hipotoni, Edwards sendromunda belirgin hipertonisite mevcuttur. (2) Karakteristik kranial bulgu: Down'da brakisefali ve düz oksiput; Edwards'ta belirgin çıkıntılı oksiput; Patau'da mikrosefali ve eğimli alın izlenir. (3) Ekstremite imzası: Down'da Simian çizgisi ve sandal gap; Edwards'ta clenched hand (üst üste binen parmaklar) ve rocker-bottom ayak; Patau'da postaksiyel polidaktili görülür. (4) Kardiyak profil: Down'da AVSD (endokardiyal yastık); Edwards'ta VSD/PDA; Patau'da kompleks kardiyak malformasyonlar hakimdir. (5) Sağkalım: Down sendromlu bireyler erişkin yaşa ulaşırken, Edwards ve Patau'da olguların %90'ı ilk bir yıl içinde kaybedilir.",
                "keyBullets": [
                    {"title": "Tonus Ayrımı", "desc": "Down = Hipotoni; Edwards = Hipertonisite.", "isKey": True},
                    {"title": "Ekstremite İmzası", "desc": "Down = Simian çizgisi/Sandal gap; Edwards = Clenched hand/Rocker-bottom; Patau = Polidaktili.", "isKey": True},
                    {"title": "Kardiyak İmzası", "desc": "Down = AVSD; Edwards = VSD/PDA; Patau = VSD/PDA/Kompleks defektler.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Klinik Parametre", "Down Sendromu (Trizomi 21)", "Edwards Sendromu (Trizomi 18)", "Patau Sendromu (Trizomi 13)"],
                    [
                        [("Karyotip", False, ""), ("47,+21", False, ""), ("47,+18", False, ""), ("47,+13", False, "")],
                        [("Kas Tonusu", False, ""), ("Genel Hipotoni", True, "Gevşek kas"), ("Genel Hipertonisite", True, "Spastik kas"), ("Değişken / Santral felç", False, "")],
                        [("Kafa / Yüz Şekli", False, ""), ("Düz oksiput, epikantus", False, ""), ("Belirgin çıkıntılı oksiput", True, "Arka kafa çıkıntısı"), ("Mikrosefali, holoprozensefali", True, "Ön beyin kusuru")],
                        [("Karakteristik El", False, ""), ("Simian çizgisi, klinodaktili", False, ""), ("Clenched hand (yumruk el)", True, "Parmak parmak üstüne"), ("Postaksiyel polidaktili", True, "Fazla parmak")],
                        [("Karakteristik Ayak", False, ""), ("Sandal gap (geniş aralık)", False, ""), ("Rocker-bottom (beşik taban)", True, "Konveks taban"), ("Rocker-bottom ayak", False, "")],
                        [("Patognomonik Triad/İpucu", False, ""), ("AVSD + Duodenal atrezi", False, ""), ("Faun kulak + Tek umblikal arter", False, ""), ("Mikroftalmi + Yarık damak + Polidaktili", True, "Patau klasik triadı")],
                        [("1 Yaş Sağkalımı", False, ""), ("> %85 (Erişkin yaşa ulaşır)", False, ""), ("%5 - 10 (%90 ilk yıl ölür)", False, ""), ("< %10 (%90 ilk yıl ölür)", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Aşağıdaki klinik eşleştirmelerden hangisi yanlıştır?",
                    {
                        "A": "Down Sendromu — İnfantil kas hipotonisi",
                        "B": "Edwards Sendromu — Kas hipertonisitesi ve clenched hand",
                        "C": "Patau Sendromu — Holoprozensefali ve polidaktili",
                        "D": "Down Sendromu — Çıkıntılı oksiput ve rocker-bottom ayak",
                        "E": "Patau Sendromu — Kutis aplazi ve omfalosel"
                    },
                    "D",
                    {
                        "A": "Doğru eşleştirmedir: Down'da hipotoni vardır.",
                        "B": "Doğru eşleştirmedir: Edwards'ta hipertoni ve clenched hand vardır.",
                        "C": "Doğru eşleştirmedir: Patau'da holoprozensefali ve polidaktili vardır.",
                        "D": "Doğru cevap D'dir (yanlış eşleştirme): Çıkıntılı oksiput ve rocker-bottom ayak Down'da değil, Edwards sendromunda (Trizomi 18) görülür.",
                        "E": "Doğru eşleştirmedir: Patau'da kutis aplazi görülür."
                    }
                ),
                make_active_recall(
                    "Canlı doğabilen üç trizomi arasında infantil hipertonisite ve parmakların üst üste binmesiyle (clenched hand) ayırt edilen sendrom hangisidir?",
                    "Edwards Sendromu (Trizomi 18).",
                    "Hipertoni ve yumruk el sendromu"
                )
            ],
            "spotPearls": [
                "Down = Hipotoni + Simian çizgisi + AVSD + Sandal gap.",
                "Edwards = Hipertonisite + Clenched hand + Rocker-bottom ayak + Çıkıntılı oksiput.",
                "Patau = Holoprozensefali + Mikroftalmi + Yarık dudak/damak + Polidaktili + Kutis aplazi."
            ]
        },

        # Slayt 49 (CHECKPOINT 5)
        {
            "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Edwards (Trizomi 18) ve Patau (Trizomi 13) Sendromları",
            "subtitle": "Bölüm Sonu Entegrasyonu ve Aktif Hatırlama İstasyonu",
            "badge": "Checkpoint 5",
            "coreContent": {
                "text": "Bu bölümde canlı doğabilen diğer iki majör otozomal trizomiyi (18 ve 13) inceledik. Edwards sendromu (Trizomi 18; 1/750) canlı doğan ikinci en sık trizomidir; %80'i kızdır; canlı doğanların %50'si ilk hafta, %90'ı ilk yıl ölür. İnfantil hipertonisite, belirgin oksiput çıkıntısı, clenched hand (2. ve 5. parmakların içe çaprazlandığı yumruk el) ve rocker-bottom ayak karakteristik bulgulardır. Patau sendromu (Trizomi 13; 1/5000) en nadir ve en ağır trizomidir; %90'ı ilk yıl kaybedilir; %20'si translokasyon kaynaklıdır [rob(13;14)]. Patolojinin temeli ön beyin bölünme kusuru olan holoprozensefalidir. Karakteristik triadı: mikroftalmi/anoftalmi + yarık dudak/damak + postaksiyel polidaktilidir. Saçlı deride kutis aplazi ve karın duvarında omfalosel patognomonik ek bulgulardır. Üç trizomi arasında Down'da hipotoni, Edwards'ta hipertonisite hakimdir.",
                "keyBullets": [
                    {"title": "Edwards İmzası", "desc": "Trizomi 18; %80 kız; hipertonisite, clenched hand, rocker-bottom ayak, çıkıntılı oksiput.", "isKey": True},
                    {"title": "Patau İmzası", "desc": "Trizomi 13; holoprozensefali, mikroftalmi + yarık damak + polidaktili triadı, kutis aplazi.", "isKey": True},
                    {"title": "Prognoz Kıyaslaması", "desc": "Edwards ve Patau'da olguların %90'ı ilk yıl kaybedilir; Down erişkinliğe ulaşır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Karakteristik Stigma", "Hangi Sendroma Özgü?", "Sınav Spotu Değeri"],
                    [
                        [("Clenched Hand (Yumruk El)", False, ""), ("Edwards Sendromu (Trizomi 18)", True, "Parmak üstüne binme"), ("2. ve 5. parmaklar çaprazlar", False, "")],
                        [("Rocker-Bottom Ayak", False, ""), ("Edwards ve Patau sendromları", True, "Beşik taban deformitesi"), ("Edwards'ta daha klasik", False, "")],
                        [("Mikroftalmi + Yarık Damak + Polidaktili", False, ""), ("Patau Sendromu (Trizomi 13)", True, "Klasik tanısal triad"), ("Patognomonik üçlü bulgu", False, "")],
                        [("Kutis Aplazi (Saçlı Deri Defekti)", False, ""), ("Patau Sendromu (Trizomi 13)", True, "Zımba deliği skalp defekti"), ("Patau'da çok tipiktir", False, "")]
                    ]
                ),
                make_cloze(
                    "Patau sendromlu bebeklerin kafa derisinde zımba ile delinmiş gibi yuvarlak cilt yokluğu alanlarına kutis aplazi adı verilir.",
                    "kutis aplazi",
                    "Skalp cilt defekti terimini anımsayınız"
                ),
                make_active_recall(
                    "Edwards sendromlu canlı doğan bebeklerin cinsiyet dağılımında belirgin olarak öne çıkan özellik nedir?",
                    "Bebeklerin yaklaşık %80'inin kız cinsiyette olmasıdır.",
                    "Kız cinsiyet belirgin baskınlığı"
                )
            ],
            "spotPearls": [
                "Edwards: Trizomi 18, %80 kız, hipertoni, clenched hand, rocker-bottom ayak.",
                "Patau: Trizomi 13, triad = mikroftalmi + yarık damak + polidaktili, kutis aplazi.",
                "Her iki sendromda da olguların %90'ı ilk bir yıl içinde hayatını kaybeder."
            ]
        },

        # Slayt 50
        {
            "title": "Diğer Otozomal Trizomilerin Fetal Letalitesi ve Spontan Abortuslar",
            "subtitle": "Trizomi 16, Trizomi 22 ve Gelişimsel Dozaj Bariyerleri",
            "badge": "Letal Trizomiler",
            "coreContent": {
                "text": "13, 18 ve 21 dışındaki diğer 19 çift otozomal kromozomun tam trizomileri istisnasız insan embriyogenezinde erken fetal letalite sergiler ve hiçbir koşulda canlı doğuma ulaşamaz. Bu letal trizomiler arasında en dramatik örnek Trizomi 16'dır. Trizomi 16, klinik olarak saptanan erken spontan abortus materyallerinde en sık rastlanan tekil trizomi olup, tüm kromozomal düşüklerin yaklaşık üçte birini (tüm spontan düşüklerin ~%15'ini) oluşturur. Embriyo genellikle gebeliğin ilk 8-10. haftasında kardiyak aktivite kazanamadan dejenere olur. İkinci en sık letal trizomi Trizomi 22'dir (tüm düşüklerin ~%5'i). Trizomi 8 ve Trizomi 9 gibi bazı otozomlar ise ancak post-zigotik mozaisizm (örneğin 46/47,+8 mozaikliği) durumunda canlı doğabilir; saf trizomileri tamamen letaldir. Bu biyolojik seleksiyon mekanizması, gen dozajı dengesizliğinin embriyonik gelişimi nasıl filtrelediğini gösterir.",
                "keyBullets": [
                    {"title": "Mutlak Letalite", "desc": "13, 18 ve 21 dışındaki tüm otozomların tam trizomileri embriyonik letaldir.", "isKey": True},
                    {"title": "Trizomi 16 Liderliği", "desc": "Spontan abortuslarda tek başına en sık görülen trizomidir; asla canlı doğmaz.", "isKey": True},
                    {"title": "Mozaik İstisnalar", "desc": "Trizomi 8 ve 9 ancak mozaik formda canlı doğuma ulaşabilir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Kromozom Numarası", "Gebelikteki Fenotipik Durumu", "Canlı Doğum Olasılığı"],
                    [
                        [("Trizomi 16", False, ""), ("Düşüklerde en sık saptanan trizomi (~%15)", True, "En sık abortus trizomisi"), ("Tam formda %0 (Asla canlı doğamaz)", False, "")],
                        [("Trizomi 22", False, ""), ("Düşüklerde ikinci en sık trizomi (~%5)", True, "İkinci sık abortus trizomisi"), ("Tam formda %0 (Canlı doğumla bağdaşmaz)", False, "")],
                        [("Trizomi 8", False, ""), ("Spontan düşüklerde sık; bazen mozaik", False, ""), ("Yalnızca MOZAİK ise canlı doğabilir", False, "")],
                        [("Trizomi 13, 18, 21", False, ""), ("İntrauterin sağkalabilen üç otozom", False, ""), ("Canlı doğabilir (ağır anomalilerle)", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Erken spontan abortus materyallerinin sitogenetik incelemesinde en sık saptanan, ancak embriyonik gelişimin ilk haftalarında mutlak letaliteye yol açarak hiçbir zaman canlı doğuma ulaşamayan otozomal trizomi hangisidir?",
                    {
                        "A": "Trizomi 13",
                        "B": "Trizomi 16",
                        "C": "Trizomi 18",
                        "D": "Trizomi 21",
                        "E": "Trizomi X"
                    },
                    "B",
                    {
                        "A": "Trizomi 13 canlı doğabilir.",
                        "B": "Doğru cevap B'dir: Trizomi 16 spontan abortuslarda en sık saptanan trizomidir ve mutlak letaldir.",
                        "C": "Trizomi 18 canlı doğabilir.",
                        "D": "Trizomi 21 canlı doğabilir.",
                        "E": "Trizomi X canlı doğar ve fertildir."
                    }
                ),
                make_active_recall(
                    "Trizomi 8 veya Trizomi 9 karyotipik anöploidisine sahip bir fetüsün canlı doğabilmesi ancak hangi sitogenetik mekanizmanın varlığıyla mümkün olabilir?",
                    "Post-zigotik mozaisizm (normal 46 hücre hattının bulunması) sayesinde mümkün olabilir.",
                    "Mozaik sağkalım mekanizması"
                )
            ],
            "spotPearls": [
                "Trizomi 16 spontan abortuslarda en sık saptanan trizomidir ve ASLA canlı doğamaz.",
                "Trizomi 22 düşüklerdeki ikinci en sık letal trizomidir.",
                "Trizomi 8 ve 9 ancak mozaik formda canlı doğuma ulaşabilir."
            ]
        }
    ]
