# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 23: Ana-Çocuk Sağlığı Düzeyinin İzlenmesi
Bölüm 9: Çocuklukta Fiziksel Büyüme Parametreleri ve Fontanel Dinamikleri (Slayt 81 - 90)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_9_slides():
    slides = []

    # Slayt 81: Büyüme ile Gelişme Arasındaki Kavramsal Ayrım
    slides.append({
        "id": "k1-23-s81",
        "title": "Büyüme ile Gelişme Arasındaki Kavramsal ve Klinik Ayrım",
        "section": "Çocuklukta Fiziksel Büyüme Parametreleri ve Fontanel Dinamikleri",
        "slideNumber": 81,
        "narrative": (
            "Çocuk sağlığı izlemlerinde büyüme ve gelişme kavramları birbirini tamamlayan fakat farklı biyolojik süreçlerdir: "
            "1. **Büyüme (Growth):** Vücut hacminin ve doku kitlesinin hücresel düzeyde sayısal (kantitatif) olarak artışıdır. "
            "Hücre bölünmesi (hiperplazi) ve hücre büyümesi (hipertrofi) ile gerçekleşir. "
            "Tartı (vücut ağırlığı), boy uzunluğu ve baş çevresi gibi metrik araçlarla ölçülür. "
            "2. **Gelişme (Development):** Doku ve organların yapısal olgunlaşması ve işlevsel (kalitatif) kapasite kazanmasıdır. "
            "Santral sinir sisteminin miyelinizasyonu ve biyokimyasal differansiasyon ile ilerler. "
            "Kaba motor (oturma, yürüme), ince motor (tutma, kavrama), dil, bilişsel ve psikosoyal beceriler ile değerlendirilir. "
            "Büyüme bir çocuğun ne kadar irileştiğini, gelişme ise biyolojik olarak ne kadar yetkinleştiğini gösterir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Çocuk sağlığında vücut hacmi ve doku kitlesindeki sayısal artış büyüme olarak tanımlanırken, fonksiyonel olgunlaşma gelişme olarak adlandırılır.",
                "fonksiyonel olgunlaşma",
                "Doku ve organların biyolojik işlev kazanma süreci"
            ),
            make_table(
                "Büyüme ve Gelişme Kavramlarının Karşılaştırmalı Özellikleri",
                ["Özellik / Parametre", "Büyüme (Growth)", "Gelişme (Development)"],
                [
                    ["Tanım", "Doku ve organ kitlesindeki sayısal artış", "Biyolojik ve fonksiyonel olgunlaşma"],
                    ["Ölçüm Niteliği", "Kantitatif (Boy, tartı, baş çevresi)", "Kalitatif (Nöromotor, bilişsel basamaklar)"],
                    [
                        "Değerlendirme Aracı",
                        "Persentil eğrileri ve büyüme eğrileri",
                        {"text": "Denver gelişimsel tarama testi ve basamaklar", "isMasked": True, "hint": "Nöromotor işlevsel olgunluk skalaları"}
                    ],
                    ["Biyolojik Temel", "Hücresel hiperplazi ve hipertrofi", "Miyelinizasyon ve sinaptik organizasyon"]
                ]
            ),
            make_micro_quiz(
                "Pediatrik izlemde bir süt çocuğunun başını dik tutması, desteksiz oturması ve yabancıları ayırt etmesi aşağıdaki kavramlardan hangisi ile tanımlanır?",
                {
                    "A": "Gelişme (Fonksiyonel Olgunlaşma)",
                    "B": "Yalnızca Fiziksel Büyüme",
                    "C": "Hücresel Hiperplazi",
                    "D": "Kardiyovasküler Remodeling",
                    "E": "Kemikleşme İndeksi"
                },
                "A",
                {
                    "A": "Fonksiyonel ve nörolojik yetkinlik kazanma süreci gelişme (development) olarak tanımlanır.",
                    "B": "Büyüme yalnızca kitle ve hacim artışıdır.",
                    "C": "Hiperplazi hücre sayısı artışıdır.",
                    "D": "Remodeling damar/kalp yapısal değişimidir.",
                    "E": "Kemikleşme büyüme kıkırdağının kapanmasıdır."
                }
            )
        ]
    })

    # Slayt 82: Tartı Artış Dinamikleri ve Fizyolojik Kilo Kaybı
    slides.append({
        "id": "k1-23-s82",
        "title": "Tartı Artış Dinamikleri ve Doğum Ağırlığı Katlanma Süreleri",
        "section": "Çocuklukta Fiziksel Büyüme Parametreleri ve Fontanel Dinamikleri",
        "slideNumber": 82,
        "narrative": (
            "Çocukluk çağında vücut ağırlığı beslenme ve genel sağlık durumunun en duyarlı göstergesidir: "
            "1. **Doğum Ağırlığı ve Fizyolojik Tartı Kaybı:** Miadında doğan sağlıklı bir bebeğin ortalama ağırlığı **~3200 gramdır (2500 - 4000 g)**. "
            "Doğumdan sonraki ilk 3-5 günde idrar, mekonyum çıkışı ve ciltten sıvı kaybıyla **%5 - 10 oranında fizyolojik tartı kaybı** görülür. "
            "Bebek en geç 7. - 10. günlerde doğum ağırlığına tekrar ulaşır (%10'dan fazla kayıp dehidratasyon alarmıdır!). "
            "2. **Ağırlık Katlanma Kuralları:** "
            "- **5. Ayda:** Doğum ağırlığının **2 katına** çıkar (~6.5 kg). "
            "- **1 Yaşında (12. Ay):** Doğum ağırlığının **3 katına** çıkar (~9.5 - 10 kg). "
            "- **2 Yaşında:** Doğum ağırlığının **4 katına** ulaşır (~12 - 13 kg). "
            "İlk 3 ayda günde ortalama 20-30 gram (ayda 600-1000 g) tartı artışı beklenir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Sağlıklı bir süt çocuğu yaklaşık 5. ayda doğum ağırlığının iki katına, 1 yaşında ise doğum ağırlığının 3 katına ulaşır.",
                "doğum ağırlığının 3 katına",
                "Bir yaşındaki çocuğun tartısının doğum tartısına oranı"
            ),
            make_table(
                "Çocuklukta Vücut Ağırlığı Katlanma Dinamikleri",
                ["Kronolojik Yaş", "Beklenen Ağırlık Düzeyi", "3200 g Doğan Bebek İçin Değer"],
                [
                    ["Doğum Anı", "Doğum Ağırlığı (1x)", "~3200 gram"],
                    ["İlk 3-5 Gün", "Fizyolojik tartı kaybı (%5-10)", "~2900 - 3050 gram"],
                    ["7 - 10. Gün", "Doğum ağırlığına yeniden ulaşma", "~3200 gram"],
                    [
                        "5. Ay",
                        {"text": "Doğum ağırlığının 2 katı", "isMasked": True, "hint": "Beşinci ay tartı hedef katsayısı"},
                        "~6400 gram"
                    ],
                    ["1 Yaş (12. Ay)", "Doğum ağırlığının 3 katı", "~9600 gram"],
                    ["2 Yaş (24. Ay)", "Doğum ağırlığının 4 katı", "~12800 gram"]
                ]
            ),
            make_micro_quiz(
                "Miadında 3000 gram olarak doğan sağlıklı bir bebeğin 1 yaşını doldurduğunda beklenen normal vücut ağırlığı yaklaşık kaç kilogram olmalıdır?",
                {
                    "A": "9 kg (Doğum ağırlığının 3 katı)",
                    "B": "6 kg (Doğum ağırlığının 2 katı)",
                    "C": "12 kg (Doğum ağırlığının 4 katı)",
                    "D": "15 kg (Doğum ağırlığının 5 katı)",
                    "E": "4.5 kg (Doğum ağırlığının 1.5 katı)"
                },
                "A",
                {
                    "A": "1 yaşında bebek doğum ağırlığının 3 katına (3000 x 3 = 9000 g / 9 kg) ulaşır.",
                    "B": "6 kg 5. aydaki beklenen değerdir (2 kat).",
                    "C": "12 kg 2 yaşındaki beklenen değerdir (4 kat).",
                    "D": "15 kg okul öncesi döneme aittir.",
                    "E": "4.5 kg malnütrisyon tablosudur."
                }
            )
        ]
    })

    # Slayt 83: Boy Uzaması Dinamikleri ve Persentil Takibi
    slides.append({
        "id": "k1-23-s83",
        "title": "Boy Uzaması Dinamikleri ve Büyüme Persentil Standartları",
        "section": "Çocuklukta Fiziksel Büyüme Parametreleri ve Fontanel Dinamikleri",
        "slideNumber": 83,
        "narrative": (
            "Boy uzaması, iskelet sisteminin uzun dönemli gelişimini ve kronik beslenme durumunu yansıtır: "
            "1. **Doğum Boyu:** Term yenidoğanın ortalama doğum boyu **~50 cm'dir (48 - 52 cm)**. "
            "2. **İlk Yıl Uzama Hızı:** Hayatın ilk yılı boy uzamasının en hızlı olduğu dönemdir: "
            "- İlk 3 ayda: ~8 cm, 3-6 ayda: ~8 cm, 6-9 ayda: ~4 cm, 9-12 ayda: ~4 cm uzar. "
            "- İlk yıl toplam **25 cm uzayarak 1 yaşında ~75 cm'ye (doğum boyunun 1.5 katı)** ulaşır! "
            "3. **Sonraki Boy Dönüm Noktası:** "
            "- **4 Yaşında:** Doğum boyunun **tam 2 katına (~100 cm)** ulaşır. "
            "4. **Persentil Değerlendirmesi:** Türk çocukları persentil eğrilerinde (Neyzi eğrileri) 3. ile 97. persentil arası normal kabul edilir. "
            "3. persentil altı boy kısalığı; izlemde persentil çizgisinin aşağı doğru iki bant kırması kronik hastalık alarmıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Term bir yenidoğan ilk yıl 25 cm uzayarak bir yaşında doğum boyunun yaklaşık bir buçuk katına ulaşır.",
                "bir buçuk katına",
                "Bir yaşındaki boy uzunluğunun doğum boyuna oranı"
            ),
            make_table(
                "Yaşa Göre Standart Boy Uzaması Dönüm Noktaları",
                ["Yaş Dönemi", "Ortalama Boy Değeri", "Doğum Boyuna Oranı"],
                [
                    ["Doğum Anı", "~50 cm", "Başlangıç değeri (1x)"],
                    [
                        "1 Yaş (12. Ay)",
                        {"text": "~75 cm (25 cm artış)", "isMasked": True, "hint": "İlk yaştaki boy uzunluğu"},
                        "Doğum boyunun ~1.5 katı"
                    ],
                    ["4 Yaş", "~100 cm (1 metre)", "Doğum boyunun tam 2 katı"],
                    ["12-13 Yaş", "~150 cm", "Doğum boyunun 3 katı (puberte atağı)"]
                ]
            ),
            make_micro_quiz(
                "Doğum boyu 50 cm olan sağlıklı bir çocuğun normal büyüme standartlarına göre 4 yaşına geldiğinde beklenen boy uzunluğu yaklaşık kaç santimetredir?",
                {
                    "A": "100 cm (Doğum boyunun 2 katı)",
                    "B": "75 cm (Doğum boyunun 1.5 katı)",
                    "C": "125 cm",
                    "D": "85 cm",
                    "E": "60 cm"
                },
                "A",
                {
                    "A": "4 yaşında çocuk doğum boyunun 2 katına (50 x 2 = 100 cm) ulaşır.",
                    "B": "75 cm 1 yaşındaki boy değeridir.",
                    "C": "125 cm 7-8 yaş civarına aittir.",
                    "D": "85 cm 2 yaş civarı boydur.",
                    "E": "60 cm ilk 4-5 ay boyudur."
                }
            )
        ]
    })

    # Slayt 84: Baş ve Göğüs Çevresi Dinamikleri
    slides.append({
        "id": "k1-23-s84",
        "title": "Baş ve Göğüs Çevresi Dinamikleri ve Eşitlenme Zamanı",
        "section": "Çocuklukta Fiziksel Büyüme Parametreleri ve Fontanel Dinamikleri",
        "slideNumber": 84,
        "narrative": (
            "Baş çevresi beyin dokusunun büyümesini doğrudan yansıtır ve ilk 2 yılda her vizitte ölçülmelidir: "
            "1. **Doğum Ölçümleri:** Miadında doğan bebekte ortalama baş çevresi **34 - 36 cm'dir**. "
            "Doğumda göğüs çevresi ise baş çevresinden **1.5 - 2 cm daha KÜÇÜKTÜR (~32 - 33 cm)**. "
            "2. **Kritik Eşitlenme Dönemi:** "
            "Bebek büyüdükçe göğüs kafesi başa göre daha hızlı genişler. "
            "**12. ayda (1 yaşında) baş çevresi ile göğüs çevresi birbirine EŞİTLENİR (~46 - 47 cm)**. "
            "3. **1 Yaşından Sonra:** Göğüs çevresi baş çevresini geçer ve önde seyreder. "
            "Eğer 12. ayda baş çevresi göğüs çevresinden hala belirgin büyükse hidrosefali, "
            "beklenenden çok küçük kalmışsa mikrosefali veya kraniyosinostoz mutlaka araştırılmalıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Doğumda baş çevresinden bir buçuk iki santimetre küçük olan göğüs çevresi on ikinci ayda baş çevresine eşitlenir.",
                "on ikinci ayda",
                "Baş ve göğüs çevrelerinin eşitlendiği kritik ay"
            ),
            make_table(
                "Baş ve Göğüs Çevresi Karşılaştırma Dinamikleri",
                ["Yaş Evresi", "Baş Çevresi", "Göğüs Çevresi", "Oransal İlişki"],
                [
                    ["Doğum", "34 - 36 cm", "32 - 34 cm", "Baş çevresi göğüsten 1.5-2 cm büyüktür"],
                    [
                        "12. Ay (1 Yaş)",
                        {"text": "~46 - 47 cm", "isMasked": True, "hint": "Bir yaşındaki baş ve göğüs ölçüsü"},
                        "~46 - 47 cm",
                        "Baş ve göğüs çevresi birbirine EŞİTTİR"
                    ],
                    ["2 Yaş ve Sonrası", "~48 - 49 cm", ">50 cm", "Göğüs çevresi baş çevresini geçer"]
                ]
            ),
            make_micro_quiz(
                "Normal bir süt çocuğunda doğumda baş çevresinden daha dar olan göğüs çevresinin baş çevresine eşitlendiği gelişim ayı hangisidir?",
                {
                    "A": "12. ay (1 yaş)",
                    "B": "3. ay",
                    "C": "6. ay",
                    "D": "24. ay",
                    "E": "36. ay"
                },
                "A",
                {
                    "A": "Baş ve göğüs çevresi 12. ayda (1 yaşında) eşitlenir.",
                    "B": "3. ayda baş çevresi hala belirgin büyüktür.",
                    "C": "6. ayda baş çevresi göğüsten geniştir.",
                    "D": "24. ayda göğüs çevresi başı geçmiştir.",
                    "E": "36. ayda göğüs çevresi çok daha büyüktür."
                }
            )
        ]
    })

    # Slayt 85: Fontanel (Bıngıldak) Anatomisi ve Muayenesi
    slides.append({
        "id": "k1-23-s85",
        "title": "Fontanel (Bıngıldak) Anatomisi ve Klinik Muayene Tekniği",
        "section": "Çocuklukta Fiziksel Büyüme Parametreleri ve Fontanel Dinamikleri",
        "slideNumber": 85,
        "narrative": (
            "Fontaneller, doğum kanalından geçişi kolaylaştıran ve beynin hızlı büyümesine olanak tanıyan membranöz açıklıklardır: "
            "1. **Ön Fontanel (Bregma):** Frontal kemikler ile paryetal kemikler arasındaki birleşim yeridir. "
            "Şekli **baklava (eşkenar dörtgen)** biçimindedir. Boyutu doğumda 2x2 cm ile 4x4 cm arasında değişir. "
            "2. **Arka Fontanel (Lambda):** Oksipital kemik ile iki paryetal kemik arasındaki birleşim yeridir. "
            "Şekli **üçgen** biçimindedir. Doğumda genellikle parmak ucu kadar açıktır veya kapalı hissedilebilir (en fazla 0.5-1 cm). "
            "3. **Muayene Tekniği:** Bebek sakin, ağlamazken ve **dik oturur pozisyondayken** nazik palpasyonla muayene edilir. "
            "Yatar pozisyonda veya bebek ağlarken venöz basınç arttığı için fontanel geçici kabarabilir; bu fizyolojiktir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Kafatasında frontal ve paryetal kemikler arasında yer alan ön fontanelin anatomik şekli baklava biçimindedir.",
                "baklava biçimindedir",
                "Ön fontanelin geometrik morfolojik şekli"
            ),
            make_table(
                "Ön ve Arka Fontanellerin Anatomik Karşılaştırması",
                ["Özellik", "Ön Fontanel (Bregma)", "Arka Fontanel (Lambda)"],
                [
                    ["Komşu Kemikler", "Frontal ve Paryetal kemikler", "Paryetal ve Oksipital kemikler"],
                    [
                        "Anatomik Şekil",
                        {"text": "Baklava (Eşkenar dörtgen)", "isMasked": True, "hint": "Dört köşeli geometrik açıklık"},
                        "Üçgen"
                    ],
                    ["Doğumdaki Boyut", "2x2 cm - 4x4 cm", "Parmak ucu (~0.5 - 1 cm)"],
                    ["Kapanma Zamanı", "9 - 18. aylar", "2 - 4. aylar"]
                ]
            ),
            make_active_recall(
                "Bebeklerde kafa muayenesi yapılırken fontanelin yalancı bombe hissedilmesini engellemek için çocuğun hangi pozisyonda muayene edilmesi gerekir?",
                "Bebek sakin durumdayken dik oturur pozisyonda muayene edilmelidir.",
                "Dik duruş ve sakin ortam muayene pozisyonu"
            )
        ]
    })

    # Slayt 86: Fontanel Kapanma Zamanları ve Erken/Geç Kapanma
    slides.append({
        "id": "k1-23-s86",
        "title": "Fontanel Kapanma Zamanları ve Erken/Geç Kapanma Patolojileri",
        "section": "Çocuklukta Fiziksel Büyüme Parametreleri ve Fontanel Dinamikleri",
        "slideNumber": 86,
        "narrative": (
            "Fontanellerin kemikleşme ve kapanma takvimi beyin gelişimi ve metabolik dengeyle birebir ilişkilidir: "
            "1. **Arka Fontanel Kapanması:** Doğumdan sonra hızla kemikleşir ve **en geç 2. - 4. aylarda (ortalama 4. ayda)** tamamen kapanır. "
            "2. **Ön Fontanel Kapanması:** Beynin süratle büyümesine alan tanımak için açık kalır ve **9. - 18. aylar arasında** kapanır. "
            "3. **Erken Kapanma (<3 Ay):** Kraniyosinostoz (kafatası sütürlerinin vaktinden önce kemikleşmesi) ve mikrosefali alarmıdır. "
            "4. **Geç Kapanma (>18 Ay):** "
            "- **Raşitizm (D Vitamini Eksikliği):** En sık nedendir! Kemik mineralizasyonu bozuktur. "
            "- **Konjenital Hipotiroidi:** Tiroid hormonu eksikliği kemik olgunlaşmasını geciktirir. "
            "- **Hidrosefali:** İntrakraniyal basınç fontaneli açık tutar. "
            "- **Down Sendromu ve Osteogenezis İmperfekta.**"
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Yenidoğanda arka fontanel dördüncü ayda kapanırken, ön fontanel dokuz ile on sekizinci aylar arasında kapanır.",
                "dokuz ile on sekizinci aylar arasında",
                "Ön fontanelin normal fizyolojik kapanma aralığı"
            ),
            make_table(
                "Fontanel Kapanma Anomalileri ve Etiyolojik Nedenler",
                ["Klinik Durum", "Zaman Sınırı", "Olası Patolojik Nedenler"],
                [
                    ["Erken Kapanma", "< 3. ay", "Kraniyosinostoz, mikrosefali, hipertiroidi"],
                    ["Normal Kapanma (Arka)", "2 - 4. ay", "Fizyolojik normal süreç"],
                    ["Normal Kapanma (Ön)", "9 - 18. ay", "Fizyolojik normal süreç"],
                    [
                        "Geç Kapanma (Ön)",
                        {"text": "> 18. ay", "isMasked": True, "hint": "On sekizinci aydan sonra açık kalma sınırı"},
                        "Raşitizm, Konjenital Hipotiroidi, Hidrosefali, Down sendromu"
                    ]
                ]
            ),
            make_micro_quiz(
                "On dokuz aylık bir çocuğun muayenesinde ön fontanelin hala 3x3 cm açık olduğu tespit edilmiştir. Etyolojide ilk planda araştırılması gereken en olası iki metabolik/endokrin hastalık hangisidir?",
                {
                    "A": "Raşitizm (D vitamini eksikliği) ve Konjenital Hipotiroidi",
                    "B": "Hipertiroidi ve Tip 1 Diyabet",
                    "C": "Demir eksikliği anemisi ve B12 eksikliği",
                    "D": "Fenilketonüri ve Galaktozemi",
                    "E": "Çölyak hastalığı ve Kistik Fibrozis"
                },
                "A",
                {
                    "A": "Ön fontanelin 18 aydan sonra açık kalmasının en sık nedenleri kemikleşmeyi bozan raşitizm ve hipotiroididir.",
                    "B": "Hipertiroidi fontaneli erken kapatır.",
                    "C": "Anemi fontanel kapanmasını doğrudan geciktirmez.",
                    "D": "FKÜ ve galaktozemi primer fontanel gecikmesi yapmaz.",
                    "E": "Çölyak malabsorpsiyon yapar fakat ilk planda hipotiroidi/raşitizm taranır."
                }
            )
        ]
    })

    # Slayt 87: Fontanel Muayenesinde Klinik Alarmlar (Bombe ve Çökük Fontanel)
    slides.append({
        "id": "k1-23-s87",
        "title": "Fontanel Muayenesinde Klinik Alarmlar: Bombe ve Çökük Fontanel",
        "section": "Çocuklukta Fiziksel Büyüme Parametreleri ve Fontanel Dinamikleri",
        "slideNumber": 87,
        "narrative": (
            "Fontanelin gerginliği kafa içi basıncının ve vücut hidrasyonunun en hızlı göstergesidir: "
            "1. **Bombe / Kabarık Fontanel (KİBAS Alarmı):** "
            "Fontanel kafa kemiklerinin seviyesinin üzerine çıkmış, gergin ve atımı kaybolmuştur. "
            "En acil nedenler: **Akut Bakteriyel Menenjit**, ensefalit, intrakraniyal kanama, hidrosefali veya kafa travmasıdır. "
            "Bebekte ateş, fışkırır tarzda kusma, huzursuzluk ve tiz sesle ağlama eşlik edebilir; acil hastaneye sevk şarttır! "
            "2. **Çökük Fontanel (Dehidratasyon Alarmı):** "
            "Fontanel kafa kemiklerinin seviyesinin altına çökmüş ve içe göçmüştür. "
            "Ağır sıvı kaybının (**gastroenterit, kusma, yetersiz beslenme**) en belirgin fizik muayene bulgusudur. "
            "Göz kürelerinde çökme, cilt turgorunda azalma, mukozalarda kuruluk ve oligüri ile birliktedir; acil rehidratasyon gerekir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "İshal ve kusma şikayetiyle getirilen bir süt çocuğunda fontanelin kemik seviyesinden belirgin şekilde içe batması çökük fontanel olup ağır dehidratasyon bulgusudur.",
                "ağır dehidratasyon",
                "Çökük fontanelin gösterdiği kritik sıvı kaybı durumu"
            ),
            make_table(
                "Fontanel Morfolojik Alarmları ve Ayırıcı Tanı",
                ["Fontanel Durumu", "Fiziksel Özellik", "Kritik Nedenler", "Acil Klinik Yaklaşım"],
                [
                    [
                        "Bombe Fontanel",
                        "Kemik seviyesinin üzerinde, gergin",
                        {"text": "Menenjit, KİBAS, Hidrosefali", "isMasked": True, "hint": "Kafa içi basınç artışı yapan santral patolojiler"},
                        "Acil sevk, LP, kranial USG/BT"
                    ],
                    ["Çökük Fontanel", "Kemik seviyesinin altında, içe çökük", "Gastroenterit, ağır dehidratasyon", "İntravenöz veya oral rehidratasyon sıvısı"],
                    ["Normal Fontanel", "Kemik seviyesinde, hafif pulsatil", "Fizyolojik sağlıklı durum", "Rutin büyüme izlemi"]
                ]
            ),
            make_micro_quiz(
                "Ateş, kusma ve halsizlik şikayetiyle getirilen 6 aylık bir bebeğin dik oturur muayenesinde ön fontanelin tahta gibi gergin ve dışarı doğru kabarmış (bombe) olduğu saptanmıştır. Hekimin ilk şüphelenmesi gereken hayatı tehdit edici patoloji hangisidir?",
                {
                    "A": "Akut Menenjit / Kafa İçi Basınç Artışı (KİBAS)",
                    "B": "Ağır dehidratasyon ve sıvı kaybı",
                    "C": "D vitamini eksikliği (Raşitizm)",
                    "D": "Konjenital kalça displazisi",
                    "E": "Fizyolojik diş çıkarma reaksiyonu"
                },
                "A",
                {
                    "A": "Ateş ve bombe fontanel menenjit veya KİBAS'ın klasik alarm bulgusudur.",
                    "B": "Dehidratasyonda fontanel kabarık değil çökük olur.",
                    "C": "Raşitizmde fontanel bombeleşmez, geç kapanır.",
                    "D": "Kalça displazisi fontaneli etkilemez.",
                    "E": "Diş çıkarma fontaneli bombeleştirmez."
                }
            )
        ]
    })

    # Slayt 88: Süt Dişlerinin Çıkış Sırası ve Zamanlaması
    slides.append({
        "id": "k1-23-s88",
        "title": "Süt Dişlerinin Çıkış Sırası, Zamanlaması ve Tamamlanması",
        "section": "Çocuklukta Fiziksel Büyüme Parametreleri ve Fontanel Dinamikleri",
        "slideNumber": 88,
        "narrative": (
            "Diş gelişimi iskelet olgunlaşmasının ve çiğneme fonksiyonuna geçişin temel basamağıdır: "
            "1. **İlk Süt Dişleri:** Genellikle **5. - 9. aylarda (ortalama 6. ayda)** çıkar. "
            "İlk süren dişler hemen her zaman **alt orta kesici dişlerdir (mandibular santral insizörler)**. "
            "2. **1 Yaşındaki Durum:** 12. ayda çocukta ortalama **6 - 8 süt dişi** mevcuttur (üst ve alt kesiciler). "
            "3. **Süt Dişlerinin Tamamlanması:** "
            "Kesici dişleri takiben birinci azılar, köpek dişleri ve ikinci azılar sürer. "
            "**2.5 yaşında (30. ayda) toplam 20 süt dişinin tamamı** ağızda yerini alır. "
            "4. **Diş Çıkmasında Gecikme:** 12-13. aya kadar hiç diş çıkmaması durumunda raşitizm, "
            "hipotiroidi veya hipopitüitarizm araştırılmalıdır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Bebeklerde ilk süt dişleri genellikle 5-9. aylarda çıkar ve 2.5 yaşında 20 süt dişinin tamamı tamamlanır.",
                "2.5 yaşında 20 süt dişinin tamamı",
                "Tüm süt dişlerinin eksiksiz tamamlandığı yaş ve adet"
            ),
            make_table(
                "Süt Dişlerinin Çıkış Takvimi ve Diş Tipleri",
                ["Diş Grubu", "Ortalama Çıkış Zamanı", "Toplam Diş Sayısı"],
                [
                    ["Alt Orta Kesiciler (Santral İnsizör)", "5 - 9. Ay (İlk çıkanlar)", "2 adet"],
                    ["Üst Kesiciler ve Alt Yan Kesiciler", "8 - 12. Ay", "6 adet (1 yaşında toplam 6-8 diş)"],
                    ["Birinci Süt Azıları", "12 - 18. Ay", "4 adet"],
                    ["Köpek Dişleri (Kaninler)", "16 - 24. Ay", "4 adet"],
                    [
                        "İkinci Süt Azıları",
                        {"text": "24 - 30. Ay (2.5 Yaş)", "isMasked": True, "hint": "Süt diş dizisini tamamlayan son grup"},
                        "4 adet (Toplamda 20 diş tamamlanır)"
                    ]
                ]
            ),
            make_micro_quiz(
                "Sağlıklı bir çocukta yirmi adet süt dişinin tamamının ağızda eksiksiz olarak sürmesini tamamladığı beklenen yaş hangisidir?",
                {
                    "A": "2.5 yaş (30. ay)",
                    "B": "1 yaş (12. ay)",
                    "C": "4 yaş (48. ay)",
                    "D": "6 ay",
                    "E": "6 yaş"
                },
                "A",
                {
                    "A": "2.5 yaşında (30. ay) 20 süt dişinin tamamı tamamlanır.",
                    "B": "1 yaşında sadece 6-8 diş bulunur.",
                    "C": "4 yaşında yeni süt dişi çıkmaz.",
                    "D": "6 ayda henüz ilk diş sürmektedir.",
                    "E": "6 yaşta kalıcı dişler sürmeye başlar."
                }
            )
        ]
    })

    # Slayt 89: [TEKRAR SAYFASI - CHECKPOINT 9] Fiziksel Büyüme Ölçütleri, Fontaneller ve Diş Gelişimi
    slides.append({
        "id": "k1-23-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Fiziksel Büyüme Ölçütleri, Fontaneller ve Diş Gelişimi",
        "section": "Çocuklukta Fiziksel Büyüme Parametreleri ve Fontanel Dinamikleri",
        "slideNumber": 89,
        "narrative": (
            "Bu dokuzuncu checkpoint sayfasında, büyüme ölçütlerini ve fontanel/diş dinamiklerini özetliyoruz: "
            "1. **Büyüme vs Gelişme:** Büyüme kitlesel/sayısal artış, gelişme ise biyolojik fonksiyonel olgunlaşmadır. "
            "2. **Kilo Katlanması:** 5. ayda 2 katına, 1 yaşında 3 katına, 2 yaşında 4 katına ulaşır. "
            "3. **Boy Dinamikleri:** Doğum boyu ~50 cm'dir; ilk yıl 25 cm uzayarak 1 yaşında 1.5 katına (~75 cm), 4 yaşında 2 katına (~100 cm) çıkar. "
            "4. **Baş ve Göğüs Çevresi:** Doğumda baş çevresi 34-36 cm olup göğüsten 1.5-2 cm büyüktür; 12. AYDA BAŞ VE GÖĞÜS ÇEVRESİ EŞİTLENİR. "
            "5. **Fontaneller:** Arka fontanel (üçgen) 2-4. ayda (ortalama 4. ayda); Ön fontanel (baklava) 9-18. aylarda kapanır. "
            "6. **Fontanel Patolojileri:** Bombe fontanel menenjit/KİBAS; çökük fontanel dehidratasyondur. Geç kapanma (>18 ay) raşitizm ve hipotiroidiyi gösterir. "
            "7. **Diş Gelişimi:** İlk diş 5-9. ayda (alt orta kesici); 1 yaşında 6-8 diş; 2.5 yaşında 20 süt dişi tamamlanır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "flashcards": [
            make_flashcard(
                "k1-23-fc-s89-1",
                "Bebeklikte arka fontanelin (bıngıldağın) normal fizyolojik kapanma zamanı hangi aydır?",
                "Yaşamın ortalama dördüncü ayında kapanır.",
                "Oksipital kemik ile paryetaller arasındaki üçgen anatomik aralığın kemikleşmesi",
                "Fontanel Kapanma Zamanları"
            ),
            make_flashcard(
                "k1-23-fc-s89-2",
                "Bebeklerde doğumda baş çevresinden bir buçuk santimetre küçük olan göğüs çevresi kaçıncı ayda baş çevresine eşitlenir?",
                "On ikinci ayda (bir yaşında) eşitlenir.",
                "Süt çocukluğunun tamamlandığı ilk doğum günü evresi",
                "Büyüme Oranları"
            ),
            make_flashcard(
                "k1-23-fc-s89-3",
                "Süt çocuklarında yirmi adet süt dişinin tamamlanması normal gelişimde kaç yaşında gerçekleşir?",
                "İki buçuk yaşında tümü tamamlanır.",
                "Otuzuncu ay gelişim basamağı takvimi",
                "Diş Gelişimi"
            )
        ],
        "interactiveElements": [
            make_table(
                "Bebeklik Büyüme Parametreleri Özet Kontrol Tablosu",
                ["Ölçüm Parametresi", "1 Yaş Değeri", "Kritik Eşitlenme / Kapanma Zamanı"],
                [
                    ["Vücut Ağırlığı", "Doğum ağırlığının 3 katı (~9.5 - 10 kg)", "5. ayda 2 katı, 2 yaşta 4 katı"],
                    ["Boy Uzunluğu", "Doğum boyunun ~1.5 katı (~75 cm)", "4 yaşında 2 katı (~100 cm)"],
                    [
                        "Baş - Göğüs Çevresi",
                        {"text": "Baş ve Göğüs birbirine EŞİTLENİR (~46-47 cm)", "isMasked": True, "hint": "On ikinci aydaki baş-göğüs eşitliği"},
                        "12. aydan sonra göğüs çevresi öne geçer"
                    ],
                    ["Arka Fontanel", "Tamamen kapalıdır", "2 - 4. ayda (ortalama 4. ayda) kapanır"],
                    ["Ön Fontanel", "Kapanma sürecindedir", "9 - 18. aylar arasında kapanır"],
                    ["Süt Dişi Adedi", "6 - 8 adet kesici diş", "2.5 yaşında 20 süt dişi tamamlanır"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki pediatrik büyüme parametresi eşleştirmelerinden hangisi yanlıştır?",
                {
                    "A": "Baş ve göğüs çevresi 6. ayda eşitlenir",
                    "B": "Doğum ağırlığı 5. ayda 2 katına çıkar",
                    "C": "Doğum ağırlığı 1 yaşında 3 katına çıkar",
                    "D": "Ön fontanel 9-18. aylar arasında kapanır",
                    "E": "2.5 yaşında 20 süt dişi tamamlanır"
                },
                "A",
                {
                    "A": "Baş ve göğüs çevresi 6. ayda değil, 12. ayda (1 yaşında) eşitlenir.",
                    "B": "Ağırlık 5. ayda 2 katına çıkar (doğrudur).",
                    "C": "Ağırlık 1 yaşında 3 katına çıkar (doğrudur).",
                    "D": "Ön fontanel 9-18. aylarda kapanır (doğrudur).",
                    "E": "2.5 yaşında 20 süt dişi tamamlanır (doğrudur)."
                }
            )
        ]
    })

    # Slayt 90: Bölüm Özeti: Fiziksel Büyümeden Nöromotor Gelişim Basamakları ve Büyük Özete Geçiş
    slides.append({
        "id": "k1-23-s90",
        "title": "Bölüm Özeti: Fiziksel Büyümeden Nöromotor Gelişim Basamakları ve Büyük Özete Geçiş",
        "section": "Çocuklukta Fiziksel Büyüme Parametreleri ve Fontanel Dinamikleri",
        "slideNumber": 90,
        "narrative": (
            "Çocukluk çağı fiziksel büyüme parametreleri bölümünü tamamlarken şu ana noktaları sabitliyoruz: "
            "1. **Büyüme Hızı Sürekli Değildir:** En hızlı büyüme fetal dönem ve süt çocukluğunun ilk yılındadır; "
            "ilk yıl 25 cm uzayan bir bebek ikinci yıl 12 cm uzar. "
            "2. **Metabolik Pencereler Fontanelden İzlenir:** Ön fontanelin 18 aydan sonra kapanmaması raşitizm veya konjenital hipotiroidi gibi "
            "erken tedavi edilmediğinde zeka ve kemik yapısını kalıcı bozan hastalıkların sessiz bir işaretidir. "
            "3. **Metrik Uyum Bütünlüğü:** Boy, tartı, baş çevresi ve diş gelişimi birbiriyle senkron seyreder. "
            "4. **Son Bölüme Köprü:** Son bölümümüzde çocuğun nöromotor gelişim basamaklarını (ay ay motor, dil ve sosyal beceriler), "
            "gelişimsel kırmızı bayrakları ve dersin tümünü kapsayan Ana-Çocuk Sağlığı Büyük Özetini inceleyeceğiz."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Süt çocukluğu döneminde en hızlı büyüme ilk yılda gerçekleşir ve boy uzaması ilk on iki ayda yirmi beş santimetredir.",
                "yirmi beş santimetredir",
                "İlk yıl boyunca kazanılan toplam santimetre boy artışı"
            ),
            make_active_recall(
                "Süt çocuğunun fiziksel büyüme takibinde tartı artışının duraklaması veya persentil çizgisinin düşmesi durumunda hekimin beslenme sorgulamasında ilk değerlendirmesi gereken altın besin nedir?",
                "Anne sütü alım sıklığı ve emzirme tekniği değerlendirilmelidir.",
                "İlk 6 ayın tek ve vazgeçilmez temel besini"
            ),
            make_micro_quiz(
                "Birinci basamak hekimliği pratiğinde bir çocuğun büyüme eğrisinin değerlendirilmesinde aşağıdakilerden hangisi patolojik bir duruma işaret eder?",
                {
                    "A": "Büyüme eğrisinin izlem boyunca iki persentil bandını birden aşağı kırması",
                    "B": "Boy ve kilonun 50. persentil çizgisi üzerinde paralel seyretmesi",
                    "C": "Çocuğun 25. persentilde sağlıklı ve dengeli büyümesi",
                    "D": "Doğumdan sonraki ilk 4 günde %6 tartı kaybı olup 8. günde doğum tartısına dönülmesi",
                    "E": "Baş çevresinin 1 yaş boyunca 50. persentilde düzenli artış göstermesi"
                },
                "A",
                {
                    "A": "Persentil eğrisinin iki persentil çizgisini kırması büyüme duraklaması veya kronik hastalık alarmıdır.",
                    "B": "50. persentilde paralel seyir ideal büyümedir.",
                    "C": "25. persentil normal aralıktadır (3-97 persentil).",
                    "D": "İlk haftadaki %6 tartı kaybı tamamen fizyolojiktir.",
                    "E": "Persentil boyunca düzenli artış normaldir."
                }
            )
        ]
    })

    return slides
