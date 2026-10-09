# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 23: Ana-Çocuk Sağlığı Düzeyinin İzlenmesi
Bölüm 10: Nöromotor Gelişim Basamakları ve Ana-Çocuk Sağlığı Büyük Özeti (Slayt 91 - 100)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_10_slides():
    slides = []

    # Slayt 91: 1. ve 2. Ay Nöromotor ve Sosyal Gelişim Basamakları
    slides.append({
        "id": "k1-23-s91",
        "title": "1. ve 2. Ay Nöromotor ve Sosyal Gelişim Basamakları",
        "section": "Nöromotor Gelişim Basamakları ve Ana-Çocuk Sağlığı Büyük Özeti",
        "slideNumber": 91,
        "narrative": (
            "Yaşamın ilk iki ayı santral sinir sisteminin dış çevreye uyum sağladığı ve ilkel reflekslerin hakim olduğu evredir: "
            "1. **1. Ay Gelişim Basamakları:** "
            "- **Motor:** Yüzüstü (prone) yatırıldığında başını bir taraftan diğerine çevirebilir, çenesini yataktan hafifçe kaldırır. Eller çoğunlukla yumruk şeklindedir. "
            "- **Görsel/İşitsel:** Objeleri veya insan yüzünü orta hatta (90 derece) kadar gözleriyle izler. Ani yüksek seslere irkilerek veya ağlayarak tepki verir. "
            "2. **2. Ay Gelişim Basamakları (Sosyal Dönüm Noktası):** "
            "- **Motor:** Başını dik tutmaya başlar (yüzüstüyken göğsünü hafif kaldırır, kucakta dik durabilir). Eller gevşer ve sık sık açık durur. "
            "- **Görsel:** Objeleri orta hattın ötesine, perifere doğru (180 derece) başını çevirerek takip eder. "
            "- **Sosyal İletişim:** Kendisiyle konuşulduğunda, gülümsendiğinde karşılık olarak **sosyal gülümseme (sosyal tebessüm)** gösterir. "
            "Sosyal gülümseme otizm ve ağır nörolojik hasarların dışlanmasında en erken ve kritik psikososyal basamaktır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "İkinci ayın en kritik psikososyal gelişim basamağı, bebekle konuşulup gülümsendiğinde karşılık vermesini sağlayan sosyal gülümsemedir.",
                "sosyal gülümsemedir",
                "İki aylık bebeğin insan yüzüne ve sesine verdiği yanıt tebessümü"
            ),
            make_table(
                "1. ve 2. Ay Gelişim Basamakları Karşılaştırma Matrisi",
                ["Gelişim Alanı", "1. Ay Basamağı", "2. Ay Basamağı"],
                [
                    ["Baş Kontrolü", "Yüzüstüyken başı hafifçe kaldırma", "Başını dik tutabilme, göğsü hafif kaldırma"],
                    ["El Pozisyonu", "Eller çoğunlukla sıkı yumruk", "Eller gevşek ve açık"],
                    ["Görsel Takip", "Orta hatta kadar (90 derece)", "Perifere doğru tam takip (180 derece)"],
                    [
                        "Sosyal Yanıt",
                        "Sese irkilme veya sakinleşme",
                        {"text": "Sosyal gülümseme (sosyal tebessüm)", "isMasked": True, "hint": "Konuşulunca tebessümle karşılık verme"}
                    ]
                ]
            ),
            make_micro_quiz(
                "İki aylık sağlıklı bir bebeğin rutin sağlam çocuk izleminde hekimin görmeyi beklediği en karakteristik sosyal gelişim basamağı hangisidir?",
                {
                    "A": "Konuşulunca veya gülününce sosyal gülümseme göstermesi",
                    "B": "Desteksiz bağımsız oturabilmesi",
                    "C": "Eşyayı bir elinden diğerine aktarması",
                    "D": "Kerpeten tutuşu ile boncuk toplaması",
                    "E": "Anlamlı iki kelimeli cümle kurması"
                },
                "A",
                {
                    "A": "2. ayda konuşulunca karşılık veren sosyal gülümseme başlar.",
                    "B": "Desteksiz oturma 6. ay basamağıdır.",
                    "C": "El transferi 6. ayda gerçekleşir.",
                    "D": "Kerpeten tutuşu 12. ay basamağıdır.",
                    "E": "İki kelimeli cümle 24. ay (2 yaş) basamağıdır."
                }
            )
        ]
    })

    # Slayt 92: 3. ve 4. Ay Motor ve Dil Gelişim Basamakları
    slides.append({
        "id": "k1-23-s92",
        "title": "3. ve 4. Ay Motor, Dil ve Bilişsel Gelişim Basamakları",
        "section": "Nöromotor Gelişim Basamakları ve Ana-Çocuk Sağlığı Büyük Özeti",
        "slideNumber": 92,
        "narrative": (
            "3 ve 4. aylar istemli hareketlerin ilkel reflekslerin yerini almaya başladığı dönemdir: "
            "1. **3. Ay Gelişim Basamakları:** "
            "- **Motor:** Yüzüstü yatarken kollarının (ön kolunun) üzerine dayanarak göğsünü yataktan tamamen kaldırır. Eller açıktır, eline verilen çıngırağı sallar. "
            "- **Sosyal/Bilişsel:** Yakınlarını, özellikle anneyi tanır, meme veya biberon görünce heyecanlanır. "
            "2. **4. Ay Gelişim Basamakları (Gövde Kontrolü ve Kahkaha):** "
            "- **Motor:** **Destekle oturabilir** (arkasına yastık konulduğunda oturur). Çekilince baş arkaya düşmez, gövdeyle aynı hizada gelir. "
            "Ellerini orta hatta birleştirir, nesnelere iki eliyle birden uzanır ve yakalar. "
            "- **Dil ve İletişim:** Agu sesleri ve vokal sesler çıkarır. Çevresindeki uyaranlara yüksek sesle **kahkaha (sesli gülme)** atarak tepki verir. "
            "- **Refleks Değişimi:** Moro ve asimetrik tonik boyun refleksi bu dönemde zayıflayarak kaybolur."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Dördüncü ayda bebek arkasından desteklendiğinde destekle oturur ve yüksek sesle kahkaha atarak güler.",
                "destekle oturur",
                "Dördüncü ayda gövdenin yastıkla desteklenerek sağlandığı oturma biçimi"
            ),
            make_table(
                "3. ve 4. Ay Gelişimsel Beceriler Matrisi",
                ["Gelişim Alanı", "3. Ay Becerisi", "4. Ay Becerisi"],
                [
                    ["Kaba Motor", "Ön kollar üzerinde gövdeyi kaldırma", "Destekle oturabilme, tam baş kontrolü"],
                    ["İnce Motor", "Eline verilen nesneyi tutma", "Elleri orta hatta kavuşturma, iki elle uzanma"],
                    [
                        "Ses ve İletişim",
                        "Sesli agulamalar çıkarma",
                        {"text": "Yüksek sesle kahkaha atma (sesli gülme)", "isMasked": True, "hint": "Neşeli sesli kahkaha basamağı"}
                    ],
                    ["İlkel Refleksler", "Moro ve yakalama zayıflar", "Moro refleksi tamamen kaybolma sürecindedir"]
                ]
            ),
            make_micro_quiz(
                "Dört aylık bir bebeğin nöromotor muayenesinde hekimin bebeği sırtüstü yatarken ellerinden tutup oturur pozisyona çekerken (traksiyon testi) normalde görmesi gereken baş yanıtı hangisidir?",
                {
                    "A": "Başın gövdeyle aynı hizada gelmesi (baş düşmesinin olmaması)",
                    "B": "Başın tamamen arkaya düşerek sarkması",
                    "C": "Asimetrik boyun ekstansiyonu",
                    "D": "Opistotonus duruşuna geçmesi",
                    "E": "Moro refleksinin şiddetle tetiklenmesi"
                },
                "A",
                {
                    "A": "4. ayda boyun kasları güçlenmiştir; çekildiğinde baş gövdeyle birlikte gelir.",
                    "B": "Başın arkaya düşmesi hipotoni veya motor gerilik işaretidir.",
                    "C": "Asimetrik boyun patolojiktir.",
                    "D": "Opistotonus menenjit veya tetanoz bulgusudur.",
                    "E": "Moro 4. ayda kaybolmalıdır."
                }
            )
        ]
    })

    # Slayt 93: 6. Ay Kritik Dönüm Noktası: Desteksiz Oturma ve El Transferi
    slides.append({
        "id": "k1-23-s93",
        "title": "6. Ay Kritik Dönüm Noktası: Desteksiz Oturma ve El Transferi",
        "section": "Nöromotor Gelişim Basamakları ve Ana-Çocuk Sağlığı Büyük Özeti",
        "slideNumber": 93,
        "narrative": (
            "6. ay, bebek gelişiminde hem motor hem de beslenme açısından en önemli altın dönüm noktasıdır: "
            "1. **Desteksiz Bağımsız Oturma:** Bebek hiçbir destek olmadan düz bir zeminde **desteksiz oturabilir**. "
            "Omurga diktir, kollarını öne dayayarak denge kurar (tripod oturuşu) ve kısa sürede kollar serbest kalır. "
            "2. **El Transferi (Objeyi Elden Ele Geçirme):** İnce motorda çığır açan bir gelişmedir; "
            "bebek bir elindeki nesneyi istemli olarak diğer eline aktarabilir. İki beyin hemisferinin korpus kallozum aracılığıyla iletişimini gösterir. "
            "3. **Ses ve İletişim:** Tek heceli sesler çıkarır ('ba', 'da', 'ma', 'ge'). "
            "4. **Sosyal Biliş (Yabancı Farkındalığı):** Tanıdık yüzler ile yabancıları net olarak ayırt eder, yabancılara karşı çekingenlik gösterir. "
            "5. **Beslenme Entegrasyonu:** Desteksiz oturma ve dil itme refleksinin kaybolmasıyla katı ek gıdaya güvenle başlanır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Altıncı ayın en kritik kaba motor basamağı bebeğin hiçbir destek almadan desteksiz oturmasıdır.",
                "desteksiz oturmasıdır",
                "Altıncı ayda kazanılan bağımsız oturma yetisi"
            ),
            make_table(
                "6. Ay Gelişimsel Dönüm Noktaları Özeti",
                ["Gelişimsel Alan", "Kritik 6. Ay Becerisi", "Klinik / Biyolojik Önemi"],
                [
                    [
                        "Kaba Motor",
                        {"text": "Desteksiz bağımsız oturma", "isMasked": True, "hint": "Yardımsız dik oturabilme becerisi"},
                        "Omurga kas gücü ve postural denge olgunlaşması"
                    ],
                    ["İnce Motor", "Nesneyi bir elden diğerine geçirme", "İki el koordinasyonu ve interhemisferik iletişim"],
                    ["Dil Gelişimi", "Tek heceli sesler (ba, da, ma)", "Konuşma öncesi vokalizasyon"],
                    ["Sosyal Gelişim", "Yabancıları ayırt etme", "Bağlanma ve görsel hafıza gelişimi"]
                ]
            ),
            make_micro_quiz(
                "Tıp fakültesi kurul ve uzmanlık sınavlarında en sık sorgulanan pediatrik basamaklardan biri olan 'desteksiz oturma' becerisi normal bir bebekte hangi ayda beklenir?",
                {
                    "A": "6. ay",
                    "B": "2. ay",
                    "C": "4. ay",
                    "D": "9. ay",
                    "E": "12. ay"
                },
                "A",
                {
                    "A": "Desteksiz oturma 6. ayın karakteristik dönüm noktasıdır.",
                    "B": "2. ayda ancak baş dik tutulabilir.",
                    "C": "4. ayda destekle oturur.",
                    "D": "9. ayda emekler ve ayağa kalkar.",
                    "E": "12. ayda yürümeye başlar."
                }
            )
        ]
    })

    # Slayt 94: 9. Ay Gelişim Basamakları: Emekleme ve Hece Tekrarları
    slides.append({
        "id": "k1-23-s94",
        "title": "9. Ay Gelişim Basamakları: Emekleme, Ayağa Kalkma ve Hece Tekrarları",
        "section": "Nöromotor Gelişim Basamakları ve Ana-Çocuk Sağlığı Büyük Özeti",
        "slideNumber": 94,
        "narrative": (
            "9. ayda bebek yerçekimine karşı koyarak bağımsız hareket alanını genişletir: "
            "1. **Kaba Motor Beceriler:** "
            "- **Emekleme:** Karın üzerinde sürünerek veya eller ve dizler üzerinde koordineli emekler. "
            "- **Ayağa Kalkma:** Koltuk, masa gibi mobilyalara tutunarak kendi kendine ayağa kalkar, dik durur. "
            "2. **İnce Motor Beceriler:** "
            "- Radyal-dijital kavrama: Nesneleri başparmak ile diğer parmaklar arasında tutar. "
            "- İki nesneyi birbirine vurarak ses çıkarır, parmağıyla küçük delikleri kurcalar. "
            "3. **Dil ve İletişim:** "
            "- Hece tekrarları (kanonik babıldama): '**ma-ma**', '**ba-ba**', '**da-da**' gibi çift heceli sesleri art arda söyler (henüz amaca özgü olmayabilir). "
            "- Çevredekilerin ses tonunu ve mimiklerini taklit eder. "
            "4. **Bilişsel/Sosyal:** "
            "- **Nesne Kalıcılığı:** Saklanan bir oyuncağın örtüsünü kaldırıp arar. "
            "- Ce-e (peek-a-boo) oyunu oynamaktan büyük keyif alır. Ayrılık anksiyetesi belirginleşir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Dokuz aylık bir bebek mobilyalara tutunarak ayağa kalkar ve ma-ma, ba-ba gibi hece tekrarları yapar.",
                "hece tekrarları yapar",
                "Dokuzuncu ayda görülen çift heceli babıldama konuşma becerisi"
            ),
            make_table(
                "9. Ay Nörogelişimsel Göstergeleri",
                ["Gelişim Boyutu", "Kazanılan Beceri", "Gelişimsel Test Karşılığı"],
                [
                    ["Lokomosyon", "Emekleme ve tutunarak ayağa kalkma", "Alt ekstremite ağırlık taşıma kapasitesi"],
                    [
                        "İnce Manipülasyon",
                        {"text": "İki nesneyi birbirine vurma, radyal kavrama", "isMasked": True, "hint": "Nesneleri birbirine tokuşturma"},
                        "Bilateral el manipülasyonu"
                    ],
                    ["Konuşma", "Hece tekrarları (ma-ma, ba-ba)", "Kanonik babıldama evresi"],
                    ["Biliş", "Saklanan nesneyi örtünün altından bulma", "Nesne sürekliliği kavramı (Piaget)"]
                ]
            ),
            make_micro_quiz(
                "Dokuz aylık bir bebeğin gelişim muayenesinde hekimin gözlemlemesi gereken normal davranışlar arasında aşağıdakilerden hangisi yer almaz?",
                {
                    "A": "Bağımsız olarak merdiven çıkabilmesi ve koşması",
                    "B": "Tutunarak ayağa kalkabilmesi",
                    "C": "Emekleyerek oda içinde yer değiştirebilmesi",
                    "D": "'Ma-ma', 'ba-ba' gibi hece tekrarları yapabilmesi",
                    "E": "Saklanan nesneyi arayıp bulabilmesi"
                },
                "A",
                {
                    "A": "Merdiven çıkma ve koşma 2-3 yaş basamağıdır, 9. ayda beklenmez.",
                    "B": "Tutunarak kalkma 9. ay basamağıdır.",
                    "C": "Emekleme 9. ayda görülür.",
                    "D": "Hece tekrarları 9. ay dil özelliğidir.",
                    "E": "Nesne kalıcılığı 9. ayda gelişir."
                }
            )
        ]
    })

    # Slayt 95: 12. Ay Gelişim Basamakları: Yürüme ve Kerpeten Tutuşu
    slides.append({
        "id": "k1-23-s95",
        "title": "12. Ay Gelişim Basamakları: Yürüme (Sıralama) ve Kerpeten Tutuşu",
        "section": "Nöromotor Gelişim Basamakları ve Ana-Çocuk Sağlığı Büyük Özeti",
        "slideNumber": 95,
        "narrative": (
            "12. ay (1 yaş), süt çocukluğundan oyun çocukluğuna geçişin taçlandığı evredir: "
            "1. **Kaba Motor Beceriler:** "
            "- **Sıralama ve Yürüme:** Bir elinden tutulunca rahatlıkla yürür. Eşyalara tutunarak yan yan adımlar atar (sıralama). "
            "Bazı bebekler bağımsız ilk adımlarını atar (bağımsız yürüme 15-18. aya kadar normal kabul edilir). "
            "2. **İnce Motor Beceriler (Kerpeten Tutuşu - Pincer Grasp):** "
            "- Başparmak ve işaret parmağının uç kısımlarını hassas bir kıskaç gibi kullanarak yerdeki ekmek kırıntısını veya küçük boncuğu toplar. "
            "İnce motor olgunlaşmanın en rafine kanıtıdır. "
            "3. **Dil ve İletişim:** "
            "- Anlamlı **1 - 2 sözcük** söyler ('anne', 'baba', 'su', 'dede'yi kişiye/nesneye özel bilinçli kullanır). "
            "- 'Topu bana ver', 'gel' gibi tek basamaklı basit komutları anlar ve uygular. "
            "4. **Sosyal Beceriler:** "
            "- El sallayarak 'bay-bay' yapar, alkış (ce-e/alkış) yapar, bardağı iki eliyle tutup su içebilir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "On ikinci ayda bebek küçük nesneleri başparmak ve işaret parmağı uçlarıyla kerpeten tutuşu yaparak kusursuzca yakalar.",
                "kerpeten tutuşu",
                "Baş ve işaret parmağı ucuyla yapılan ince hassas kavrama manevrası"
            ),
            make_table(
                "12. Ay (1 Yaş) Gelişimsel Standartları",
                ["Gelişim Boyutu", "12. Ay Kritik Başarısı", "Normal Kabul Edilen Üst Sınır"],
                [
                    ["Kaba Motor", "Bir elinden tutulunca yürüme / sıralama", "18. aya kadar bağımsız yürüme normaldir"],
                    [
                        "İnce Motor",
                        {"text": "Kerpeten tutuşu (Pincer grasp)", "isMasked": True, "hint": "Başparmak ve işaret parmağı kıskaç hareketi"},
                        "Küçük nesneleri hassas kavrayabilme"
                    ],
                    ["Dil", "Anlamlı 1-2 kelime söyleme", "18. aya kadar en az 3-5 kelime"],
                    ["Sosyal", "Bay-bay yapma, alkışlama, basit komuta uyma", "Göz teması ve ortak dikkat kurma"]
                ]
            ),
            make_micro_quiz(
                "Bir yaşındaki bir çocuğun muayenesinde yerdeki küçük bir üzüm tanesini başparmağı ile işaret parmağının uçlarını birleştirerek tutabilmesi hangi nöromotor becerinin geliştiğini gösterir?",
                {
                    "A": "Olgun Kerpeten Tutuşu (Pincer grasp)",
                    "B": "Palmar Yakalama Refleksi",
                    "C": "Moro Refleksi",
                    "D": "Asimetrik Tonik Boyun",
                    "E": "Tripod Duruşu"
                },
                "A",
                {
                    "A": "Baş ve işaret parmağı ucuyla tutma olgun pincer/kerpeten tutuşudur ve 12. ayda beklenir.",
                    "B": "Palmar refleks 3-4. ayda kaybolur.",
                    "C": "Moro 4. ayda kaybolur.",
                    "D": "Tonik boyun ilkel reflekstir.",
                    "E": "Tripod duruşu 6. ay oturma şeklidir."
                }
            )
        ]
    })

    # Slayt 96: Çocuk Gelişiminde Kırmızı Bayraklar (Gelişimsel Gerilik Alarmları)
    slides.append({
        "id": "k1-23-s96",
        "title": "Çocuk Gelişiminde Kırmızı Bayraklar: Hekimin Sevk Kriterleri",
        "section": "Nöromotor Gelişim Basamakları ve Ana-Çocuk Sağlığı Büyük Özeti",
        "slideNumber": 96,
        "narrative": (
            "Gelişimsel basamakların beklenen üst sınırlarda kazanılamaması 'Kırmızı Bayrak' (alarm) olarak tanımlanır ve acil ileri tetkik gerektirir: "
            "1. **3. Ayda:** Baş kontrolünün hiç olmaması, anne yüzüne veya sesine sosyal gülümseme göstermemesi. "
            "2. **6. Ayda:** Destekle dahi oturamaması, nesnelere uzanmaması, göz kontağı kurmaması, seslere yönelmemesi. "
            "3. **9. Ayda:** **Desteksiz oturamaması**, heceleme seslerinin (babıldama) hiç olmaması, iki elini simetrik kullanmaması. "
            "4. **12. Ayda:** İsmi söylendiğinde bakmaması (otizm alarmı!), saklanan nesneyi aramaması, işaret parmağıyla bir şeyi göstermemesi. "
            "5. **18. Ayda:** **Bağımsız yürüyememesi**, tek bir anlamlı kelimesinin olmaması. "
            "6. **Kazanılmış Becerilerin Kaybı (Regresyon):** Hangi yaşta olursa olsun konuşan çocuğun susması veya yürüyen çocuğun yürüyememesi "
            "nörodejeneratif hastalık (metabolik, genetik, SMA, Rett sendromu) alarmıdır!"
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Çocuklukta nörogelişimsel izlemde bir çocuğun on sekizinci ayda bağımsız yürüyememesi acil sevk gerektiren kırmızı bayrak alarmıdır.",
                "on sekizinci ayda bağımsız yürüyememesi",
                "Yürüme gecikmesinde kırmızı alarm sayılan maksimum yaş sınırı"
            ),
            make_table(
                "Pediatrik Gelişimde Yaşa Göre Kırmızı Bayrak (Alarm) Sınırları",
                ["Kritik Yaş Sınırı", "Kırmızı Bayrak Bulgusu", "Şüphe Edilen Patoloji"],
                [
                    ["3. Ay", "Sosyal gülümseme ve baş kontrolü yokluğu", "Serebral palsi, mental retardasyon"],
                    ["6. Ay", "Göz teması kuramama, sese dönmeme", "Konjenital sağırlık, görme kusuru, otizm spektrumu"],
                    [
                        "9. Ay",
                        {"text": "Desteksiz oturamama", "isMasked": True, "hint": "Dokuzuncu ayda bağımsız oturamama alarmı"},
                        "Hipotoni, miyopati, motor korteks hasarı"
                    ],
                    ["18. Ay", "Bağımsız yürüyememe ve tek kelime konuşamama", "Gelişimsel motor/dil geriliği, SMA"],
                    ["Herhangi bir yaş", "Kazanılan motor/dil becerisinin kaybı (regresyon)", "Nörodejeneratif ve metabolik hastalıklar"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki durumlardan hangisi birinci basamak aile hekimliği izleminde doğrudan ileri çocuk nörolojisi merkezine sevk gerektiren bir gelişimsel kırmızı bayraktır?",
                {
                    "A": "Dokuz aylık bir bebeğin desteksiz bağımsız oturamaması",
                    "B": "İki aylık bebeğin henüz iki kelimeli cümle kuramaması",
                    "C": "Dört aylık bebeğin desteksiz yürüyememesi",
                    "D": "Beş aylık bebeğin henüz diş çıkarmamış olması",
                    "E": "On aylık bebeğin henüz merdiven tırmanamaması"
                },
                "A",
                {
                    "A": "Desteksiz oturma 6. ayda beklenir; 9. aya kadar kazanılamaması kırmızı bayraktır.",
                    "B": "İki kelimeli cümle 24. ay basamağıdır.",
                    "C": "Yürüme 12-18. ayda beklenir.",
                    "D": "İlk diş 5-9. ayda çıkar, 13. aya kadar normaldir.",
                    "E": "Merdiven çıkma 2-3 yaş basamağıdır."
                }
            )
        ]
    })

    # Slayt 97: Çocuk Sağlığı İzlemlerinde Rutin Aşılama Takvimi (GBP)
    slides.append({
        "id": "k1-23-s97",
        "title": "Genişletilmiş Bağışıklama Programı (GBP) ve Aşı Tereddüdü",
        "section": "Nöromotor Gelişim Basamakları ve Ana-Çocuk Sağlığı Büyük Özeti",
        "slideNumber": 97,
        "narrative": (
            "Genişletilmiş Bağışıklama Programı (GBP), halk sağlığının en maliyet-etkili ve hayat kurtarıcı müdahalesidir: "
            "1. **GBP Hedefi:** Boğmaca, difteri, tetanoz, kızamık, kızamıkçık, kabakulak, tüberküloz, çocuk felci (polio), "
            "hepatit B, hepatit A, suçiçeği, hemofilus influenza tip b ve pnömokok olmak üzere **13 bulaşıcı hastalığa** karşı "
            "tüm çocukları ücretsiz olarak aşılamaktır. "
            "2. **Aşı Takvimi Kilometre Taşları:** "
            "- Doğumda: Hepatit B 1. doz. "
            "- 1. Ay: Hepatit B 2. doz. "
            "- 2. Ay: BCG (Verem), 5'li Karma (DaBT-İPA-Hib), KPA (Zatürre). "
            "- 4. Ay: 5'li Karma 2, KPA 2. "
            "- 6. Ay: 5'li Karma 3, KPA 3, Hepatit B 3, OPA (Oral Polio) 1. "
            "- 12. Ay: KKK (Kızamık-Kabakulak-Kızamıkçık), Suçiçeği, KPA pekiştirme. "
            "- 18. Ay: DaBT-İPA-Hib pekiştirme, OPA 2, Hepatit A 1. doz. "
            "- 24. Ay: Hepatit A 2. doz. "
            "3. **Aşı Tereddüdü ile Mücadele:** Hekimin en önemli rolü empati kurarak kanıta dayalı tıbbi verilerle aşı tereddüdünü gidermektir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Ülkemizde Sağlık Bakanlığı Genişletilmiş Bağışıklama Programı kapsamında çocukluk çağında on üç antijene karşı ücretsiz rutin aşılama yürütülmektedir.",
                "on üç antijene",
                "Ulusal aşı takviminde ücretsiz koruma sağlanan hastalık/antijen sayısı"
            ),
            make_table(
                "Türkiye Ulusal Çocukluk Çağı Aşı Takvimi Özeti",
                ["Aşı / Antijen", "Uygulama Ayları", "Korunan Hastalık"],
                [
                    ["Hepatit B", "Doğumda, 1. ayda, 6. ayda", "Viral hepatit B ve karaciğer sirozu"],
                    ["BCG (Verem)", "2. ayda tek doz", "Miliyer tüberküloz ve tüberküloz menenjiti"],
                    [
                        "5'li Karma (DaBT-İPA-Hib)",
                        "2, 4, 6 ve 18. aylarda",
                        {"text": "Difteri, Boğmaca, Tetanoz, Polio, Hib menenjiti", "isMasked": True, "hint": "Beş bileşenli karma aşının içeriği"}
                    ],
                    ["KPA (Konjuge Pnömokok)", "2, 4 ve 12. aylarda", "Pnömokokal pnömoni ve menenjit"],
                    ["KKK (Kızamık-Kabakulak-Kızamıkçık)", "12. ayda", "Kızamık ve konjenital rubella sendromu"],
                    ["Hepatit A", "18 ve 24. aylarda", "Bulaşıcı sarılık (Hepatit A)"]
                ]
            ),
            make_micro_quiz(
                "Sağlık Bakanlığı Ulusal Aşı Takvimi'ne göre 2. ayını dolduran sağlıklı bir bebeğe aynı gün aile sağlığı merkezinde rutin olarak uygulanan aşılar hangileridir?",
                {
                    "A": "BCG, 5'li Karma (DaBT-İPA-Hib) ve KPA",
                    "B": "KKK, Suçiçeği ve Hepatit A",
                    "C": "Yalnızca Hepatit B 1. doz",
                    "D": "Yalnızca Oral Polio Aşısı (OPA)",
                    "E": "Kuduz ve Sarıhumma aşıları"
                },
                "A",
                {
                    "A": "2. ayda verem aşısı (BCG), 5'li karma ve KPA (zatürre) aşıları uygulanır.",
                    "B": "KKK ve suçiçeği 12. ayda, Hepatit A 18. ayda yapılır.",
                    "C": "Hepatit B 1. dozu doğumda uygulanır.",
                    "D": "OPA 6 ve 18. aylarda verilir.",
                    "E": "Kuduz rutin aşı takviminde yer almaz."
                }
            )
        ]
    })

    # Slayt 98: Sağlık Hizmetlerinin Sosyalleştirilmesinden (1961) Günümüze AÇS Kazanımları
    slides.append({
        "id": "k1-23-s98",
        "title": "1961'den Günümüze Ana-Çocuk Sağlığı: Sosyalleştirme ve Kazanımlar",
        "section": "Nöromotor Gelişim Basamakları ve Ana-Çocuk Sağlığı Büyük Özeti",
        "slideNumber": 98,
        "narrative": (
            "Türkiye'de ana-çocuk sağlığı hizmetlerinin modern mimarisi 1961 yılında atılmıştır: "
            "1. **224 Sayılı Kanun (1961):** Prof. Dr. Nusret Fişek öncülüğünde çıkarılan 'Sağlık Hizmetlerinin Sosyalleştirilmesi Hakkında Kanun' "
            "ile sağlık ocakları kurulmuş, ana-çocuk sağlığı ve aile planlaması entegre birinci basamak hizmeti olarak köylere kadar ulaştırılmıştır. "
            "2. **Tarihsel Kazanımlar:** "
            "- Anne Ölüm Oranı (AÖO): 1970'lerde yüz binde 200'lerin üzerindeyken bugün **yüz binde 12 - 13 düzeyine** indirilmiştir. "
            "- Bebek Ölüm Hızı (BÖH): Binde 150'lerden **binde 9 düzeyine** geriletilmiştir. "
            "- Sağlık kuruluşunda doğum oranı %99'un üzerine çıkmıştır. "
            "3. **Mevcut Halk Sağlığı Zorlukları:** "
            "- **Yüksek Sezaryen Oranı:** DSÖ önerisi %15 iken Türkiye'de %50'nin üzerindedir. "
            "- **Bölgesel Eşitsizlikler:** Doğu ile Batı, kırsal ile kentsel alanlar arasında bebek ölüm hızında hala farklar mevcuttur. "
            "- **Erken Yaşta Evlilikler ve Adölesan Gebelikler.**"
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Türkiye'de birinci basamak sağlık hizmetlerinin temelini atan ve ana-çocuk sağlığını entegre eden 224 sayılı kanun Prof. Dr. Nusret Fişek öncülüğünde hazırlanmıştır.",
                "Nusret Fişek",
                "Türk halk sağlığının ve sağlık ocakları modelinin kurucu lideri"
            ),
            make_table(
                "Türkiye'de Ana-Çocuk Sağlığı Göstergelerinin Tarihsel Seyri",
                ["Gösterge Adı", "1970'ler / 1980'ler", "Günümüz (TNSA / TÜİK)"],
                [
                    ["Anne Ölüm Oranı (100.000 canlı doğumda)", "> 200", "~ 12 - 13"],
                    ["Bebek Ölüm Hızı (1.000 canlı doğumda)", "> 150", "~ 9.0"],
                    [
                        "Hastanede Doğum Oranı",
                        "< %40",
                        {"text": "> %99", "isMasked": True, "hint": "Kurumsal doğumun neredeyse evrenselleştiği oran"}
                    ],
                    ["Sezaryen Oranı", "< %10", "> %50 (Halk sağlığı sorunu)"]
                ]
            ),
            make_micro_quiz(
                "Türkiye'de 1961 yılında çıkarılan 224 sayılı Sağlık Hizmetlerinin Sosyalleştirilmesi Hakkında Kanun'un ana-çocuk sağlığı hizmetlerine getirdiği en temel yapısal yenilik hangisidir?",
                {
                    "A": "Koruyucu ve tedavi edici sağlık hizmetlerinin entegre edilerek en uç kırsala kadar ulaştırılması",
                    "B": "Tüm doğumların yalnızca özel üniversite hastanelerinde zorunlu kılınması",
                    "C": "Aşılama hizmetlerinin tamamen ücretli hale getirilmesi",
                    "D": "Ebe ve hemşirelerin sahada görev yapmasının yasaklanması",
                    "E": "Kadınların sağlık hizmetine erişiminin sınırlandırılması"
                },
                "A",
                {
                    "A": "224 sayılı yasa koruyucu ve tedavi edici hekimliği entegre ederek halka ücretsiz ulaştırmıştır.",
                    "B": "Doğumlar köylerdeki sağlık ocakları ve dispanserlere kadar yaygınlaştırılmıştır.",
                    "C": "Aşılar tamamen ücretsizdir.",
                    "D": "Ebeler sahanın en temel koruyucu sağlık personeli olmuştur.",
                    "E": "Kadın ve çocuk sağlığı öncelikli hedef seçilmiştir."
                }
            )
        ]
    })

    # Slayt 99: Birinci Basamakta AÇS Yönetimi: Hekimin Yasal ve Etik Sorumlulukları
    slides.append({
        "id": "k1-23-s99",
        "title": "Birinci Basamakta AÇS Yönetimi ve Hekimin Yasal Sorumlulukları",
        "section": "Nöromotor Gelişim Basamakları ve Ana-Çocuk Sağlığı Büyük Özeti",
        "slideNumber": 99,
        "narrative": (
            "Aile hekimleri ve saha hekimleri ana-çocuk sağlığının hem tıbbi yöneticisi hem de yasal güvencesidir: "
            "1. **İzlem Protokollerine Uyum:** Sağlık Bakanlığı'nın belirlediği gebe (en az 4), lohusa (en az 3), "
            "bebek (en az 9) ve çocuk (en az 7) izlemlerinin eksiksiz yapılması ve HSYS/ATS sistemlerine girilmesi yasal zorunluluktur. "
            "2. **Anne ve Bebek Ölümlerinin Bildirimi:** Her anne ölümü ve bebek ölümü 24 saat içinde İl Sağlık Müdürlüğü'ne bildirilir "
            "ve 'Anne ve Bebek Ölümleri İnceleme Komisyonu' tarafından kök neden analizi yapılır. "
            "3. **Çocuk İhmal ve İstismarının Bildirimi:** TCK Madde 280 gereğince sağlık mesleği mensupları görevleri sırasında "
            "çocuk istismarı veya ihmali şüphesi duyduklarında durumu derhal adli mercilere bildirmekle yasal olarak yükümlüdür. "
            "4. **Bebek Dostu Sağlık Kuruluşu:** Anne sütünün ilk 6 ay tek başına, 2 yaşına kadar ek gıdayla sürdürülmesini desteklemek hekimlik etiğidir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Sağlık çalışanları görevleri sırasında karşılaştıkları çocuk ihmali ve istismarı şüphesini adli mercilere bildirmekle yasal olarak yükümlüdür.",
                "adli mercilere bildirmekle",
                "TCK 280 gereğince şüphenin yasal olarak iletilmesi gereken resmi makamlar"
            ),
            make_table(
                "Birinci Basamak Hekiminin AÇS Yasal ve İdari Yükümlülükleri",
                ["Yasal Yükümlülük Alanı", "Yasal Dayanak / Süre", "Hekimin Sorumluluğu"],
                [
                    ["Gebe / Lohusa / Çocuk İzlemleri", "Bakanlık İzlem Protokolleri", "Tüm muayene ve aşıların kayıt altına alınması"],
                    [
                        "Anne ve Bebek Ölüm Bildirimi",
                        {"text": "24 saat içinde bildirim", "isMasked": True, "hint": "Ölüm vakasının resmi idareye bildirilme süresi"},
                        "Ölüm inceleme komisyonuna veri sunumu"
                    ],
                    ["İhmal ve İstismar Bildirimi", "TCK Madde 280", "Şüphe halinde savcılık veya çocuk izlem merkezine (ÇİM) bildirim"],
                    ["Soğuk Zincir Yönetimi", "Aşı Takip Sistemi (ATS)", "Aşıların +2 ile +8 derecede saklanmasını denetleme"]
                ]
            ),
            make_micro_quiz(
                "Birinci basamakta görev yapan bir hekimin muayene ettiği 2 yaşındaki bir çocukta sigara yanıkları ve farklı yaşlarda kemik kırıkları saptaması durumunda yasal ve etik olarak ilk yapması gereken eylem hangisidir?",
                {
                    "A": "Durumu derhal adli mercilere (Savcılık / Kolluk / ÇİM) bildirmek",
                    "B": "Aileyi azarlayarak eve göndermek",
                    "C": "Yalnızca bir sonraki yıl izleme randevusu vermek",
                    "D": "Kırıkların kendiliğinden iyileşmesini beklemek",
                    "E": "Olayı hiçbir kayda geçirmeden unutmak"
                },
                "A",
                {
                    "A": "TCK 280 gereği istismar şüphesi derhal adli mercilere ve Çocuk İzlem Merkezi'ne bildirilmek zorundadır.",
                    "B": "Aileyi uyarmak çocuğu daha büyük hayati tehlikeye atar.",
                    "C": "Bir yıl beklemek ihmal suçudur.",
                    "D": "Tıbbi müdahale ve adli rapor şarttır.",
                    "E": "Bildirmemek Türk Ceza Kanunu'na göre suç teşkil eder."
                }
            )
        ]
    })

    # Slayt 100: [TEKRAR SAYFASI - CHECKPOINT 10] Ana-Çocuk Sağlığı Düzeyinin İzlenmesi Büyük Özeti
    slides.append({
        "id": "k1-23-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Ana-Çocuk Sağlığı Düzeyinin İzlenmesi Büyük Özeti",
        "section": "Nöromotor Gelişim Basamakları ve Ana-Çocuk Sağlığı Büyük Özeti",
        "slideNumber": 100,
        "narrative": (
            "Tüm dersin zirvesi olan bu 100. slaytta, Ana-Çocuk Sağlığı Düzeyinin İzlenmesi konusunun tüm çekirdek kazanımlarını özetliyoruz: "
            "1. **Mortalite Ölçütleri:** AÖO 100.000 canlı doğumda anne ölümleridir; BÖH 1.000 canlı doğumda 1 yaş altı ölümlerdir. "
            "2. **DÖB Standartları:** İlk vizit ilk 14 haftada; komplikasyonsuz gebede EN AZ 4 İZLEM (14, 18-24, 30-32, 36-38. haftalar). "
            "3. **Gebe Takibi:** Toplam 10-12.5 kg kilo alımı idealdir. Tansiyon >140/90 mmHg ve proteinüri preeklampsi alarmıdır. "
            "4. **Lohusa ve Kadın:** Lohusalık 42 gündür. Rutin lohusa izlemi TOPLAM 3 KEZ yapılır. Gebe olmayan kadın YILDA 2 KEZ izlenir. "
            "5. **Bebek ve Çocuk:** Bebek izlemleri 0-1 yaşta 9 kez; çocuk izlemleri 1-5 yaşta TOPLAM 7 KEZ yapılır. "
            "6. **Fiziksel Büyüme:** Ağırlık 5. ayda 2 katı, 1 yaşında 3 katıdır. Baş ve göğüs çevresi 12. AYDA EŞİTLENİR. "
            "7. **Fontaneller ve Diş:** Arka fontanel 4. ayda, ön fontanel 9-18. aylarda kapanır. 2.5 yaşında 20 süt dişi tamamlanır. "
            "8. **Gelişim Basamakları:** 2. ay sosyal gülümseme, 4. ay destekle oturma/kahkaha, 6. AY DESTEKSİZ OTURMA/el transferi, "
            "9. ay emekleme/hece tekrarı, 12. ay kerpeten tutuşu/sıralama. 18. ayda bağımsız yürüyememek kırmızı bayraktır!"
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "flashcards": [
            make_flashcard(
                "k1-23-fc-s100-1",
                "Süt çocuklarında nöromotor gelişim basamaklarına göre desteksiz bağımsız oturma becerisi normalde hangi ayda kazanılır?",
                "Altıncı ayda bu beceri edinilir.",
                "Ek gıdalara başlama dönemiyle eşzamanlı motor sıçrama evresi",
                "Nöromotor Basamaklar"
            ),
            make_flashcard(
                "k1-23-fc-s100-2",
                "Gelişimsel basamaklarda bir çocuğun desteksiz bağımsız yürüyememesi durumu en geç kaçıncı ayda kırmızı bayrak (acil sevk) alarmıdır?",
                "On sekizinci ayda bağımsız adım atamamak alarmdır.",
                "Bir buçuk yaşını dolduran çocukta kaba motor gecikme sınırı",
                "Gelişimsel Alarmlar"
            ),
            make_flashcard(
                "k1-23-fc-s100-3",
                "Çocuklarda küçük nesnelerin başparmak ve işaret parmağı uçlarıyla tutulmasını sağlayan olgun kerpeten tutuşu kaçıncı ayda gelişir?",
                "On ikinci ayda tamamlanır.",
                "İlk yaş günüyle eşleşen ince motor kavrama seviyesi",
                "İnce Motor Gelişim"
            )
        ],
        "interactiveElements": [
            make_table(
                "Ana-Çocuk Sağlığı Düzeyinin İzlenmesi Büyük Özet Tablosu",
                ["Klinik Protokol / Dönem", "Standart İzlem Sıklığı", "En Kritik Sağlık Göstergesi / Müdahale"],
                [
                    ["Gebe İzlemi (DÖB)", "En az 4 izlem (14, 20, 32, 36. haftalar)", "Preeklampsi tespiti, TT aşısı, demir ve D vit."],
                    ["Lohusa İzlemi", "Toplam 3 izlem (Ertesi gün, 1. ve 6. hafta)", "Uterus atonisi, loşi kontrolü, sepsis ve depresyon"],
                    ["15-49 Yaş Kadın İzlemi", "Yılda 2 kez (6 ayda bir)", "HPV-DNA smear (30-65 yaş) ve mamografi"],
                    ["Bebek İzlemi (0-1 Yaş)", "Hastanede 2 + ASM'de 7 = 9 izlem", "Topuk kanı, Kalça USG (4-6 hf), GBP rutin aşıları"],
                    ["Çocuk İzlemi (1-5 Yaş)", "Toplam 7 izlem (1, 1.5, 2, 2.5, 3, 4, 5 yaş)", "Otizm taraması (18 ay), görme/tansiyon (3 yaş)"],
                    ["Fiziksel Büyüme", "Tartı (1 yaşta 3 kat), Boy (1 yaşta 1.5 kat)", "Baş ve göğüs çevresi 12. ayda eşitlenir"],
                    [
                        "Nöromotor Gelişim",
                        {"text": "Desteksiz oturma (6. ay), Pincer (12. ay)", "isMasked": True, "hint": "Altıncı ve on ikinci ay temel motor kilometre taşları"},
                        "18. ayda yürüyememe kırmızı bayraktır"
                    ]
                ]
            ),
            make_micro_quiz(
                "Ana-Çocuk Sağlığı izlem protokollerinde yer alan aşağıdaki temel kurallardan hangisi yanlıştır?",
                {
                    "A": "Komplikasyonsuz gebelerde Sağlık Bakanlığı en az 2 izlem önermektedir",
                    "B": "Lohusalıkta rutin izlem sayısı toplam 3'tür",
                    "C": "1-5 yaş arası çocuklarda toplam 7 izlem yapılır",
                    "D": "Baş ve göğüs çevresi 12. ayda eşitlenir",
                    "E": "Desteksiz oturma 6. ayda kazanılan kritik bir motor basamaktır"
                },
                "A",
                {
                    "A": "Sağlık Bakanlığı komplikasyonsuz gebelere en az 2 değil, EN AZ 4 İZLEM şart koşmaktadır.",
                    "B": "Lohusa izlemi ertesi gün dahil toplam 3 kezdir (doğrudur).",
                    "C": "1-5 yaş arasında 7 izlem yapılır (doğrudur).",
                    "D": "Baş ve göğüs 12. ayda eşitlenir (doğrudur).",
                    "E": "Desteksiz oturma 6. aydadır (doğrudur)."
                }
            )
        ]
    })

    return slides
