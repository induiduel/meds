# -*- coding: utf-8 -*-
"""
Bebek Beslenmesi, Anne Sütü İmmünolojisi, Tamamlayıcı Beslenme ve Malnütrisyon Güvertesi
Sosyal Pediatri ve Çocuk Sağlığı Anabilim Dalı
24 Kapsamlı Slayt ve Pediatri Uzmanlık/Komite Sınavı Düzeyinde Sorular
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

SCRATCH_PATH = (__import__('tempfile').gettempdir() + "/deck_bebek_beslenmesi.json")
DECKS_JSON_PATH = (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))) + "/src/data/interactive_learning_decks.json")

def make_slide(slide_num, title, subtitle, narrative, spots, practice_q):
    return {
        "slideNumber": slide_num,
        "title": title,
        "subtitle": subtitle,
        "content": narrative,
        "synthesisNarrative": narrative,
        "spots": spots,
        "spotPearls": spots,
        "relatedQuestions": [practice_q],
        "practiceQuestion": practice_q
    }

slides = []

# ==============================================================================
# SLAYT 1: Bebek Beslenmesinin Epidemiyolojisi ve Küresel Hedefler
# ==============================================================================
slides.append(make_slide(
    1,
    "Bebek Beslenmesinin Epidemiyolojisi ve Küresel Hedefler",
    "Dünya ve Türkiye'de Demografik Eğilimler, Çocuk Mortalitesi ve DSÖ Stratejileri",
    """Dünya genelinde yıllık canlı doğum sayısı (CDS) yaklaşık 130-132 milyon civarında seyrederken, Türkiye'de demografik veriler son derece çarpıcı bir dönüşüm göstermektedir. Türkiye İstatistik Kurumu (TÜİK) verilerine göre Türkiye'deki canlı doğum sayısı 2022 yılında 1 milyon 35 bin iken, 2024 yılında 940 bine, 2025 yılında ise 895 bine gerilemiştir. Bu düşüşle paralel olarak, nüfusun kendini yenileme eşiği olan 2.1 düzeyindeki Toplam Doğurganlık Hızı (TDH); 2013'te 2.10 iken, 2022'de 1.69'a, 2024'te 1.49'a ve 2025'te 1.42'ye düşmüştür. Bazı illerimizde (örneğin Karabük'te 1.11) dramatik seviyelere inen doğurganlık oranları, dünyaya gelen her bir bebeğin hayatta kalmasını ve optimal potansiyeline ulaşmasını sosyal pediatri ve halk sağlığı açısından birincil öncelik haline getirmiştir.

Dünya Sağlık Örgütü (DSÖ) 2026 küresel çocuk sağlığı raporlarına göre, beş yaş altındaki çocuk ölümlerinin yaklaşık yarısı (%45-50) doğrudan veya dolaylı olarak yetersiz ve kötü beslenme (malnütrisyon) ile ilişkilidir. Dünyada 5 yaş altındaki tahmini 150 milyon çocukta kronik malnütrisyon göstergesi olan bodurluk (stunting / yaşına göre boy kısalığı), 43 milyon çocukta akut yetersiz beslenmenin göstergesi olan zayıflık/çelimsizlik (wasting / boyuna göre yetersiz ağırlık) ve eşzamanlı olarak 36 milyon çocukta aşırı kilo/obezite sorunu saptanmaktadır. Yetersiz beslenme, çocukların enfeksiyonlara karşı direncini kırmakta; pnömoni, ishal ve kızamık gibi önlenebilir hastalıklardan kaynaklanan mortaliteyi katlayarak artırmaktadır.

Bu küresel yükün önüne geçmek adına DSÖ ve UNICEF kanıta dayalı üç temel beslenme kuralını deklare etmiştir: (1) Tüm yenidoğanların doğumdan sonraki ilk bir saat içinde (altın saat) emzirilmeye başlanması, (2) Yaşamın ilk 6 ayında bebeğe su dahil hiçbir ek sıvı verilmeksizin 'SADECE ANNE SÜTÜ' ile beslenmesi, (3) Altıncı aydan itibaren besin değeri açısından yeterli, mikrobiyolojik olarak güvenli tamamlayıcı katı gıdalarla beslenmeye başlanırken emzirmenin 2 yaşına veya daha sonrasına kadar sürdürülmesidir. Yapılan epidemiyolojik modellemeler, tüm bebeklerin ilk 6 ay sadece anne sütü alması ve 2 yaşına kadar emzirilmesi durumunda, dünyada her yıl 5 yaş altındaki 820.000'den fazla çocuk ölümünün önlenebileceğini kanıtlamaktadır.""",
    [
        {"type": "clinical", "badge": "🔴 ÖNEMLİ HALK SAĞLIĞI VERİSİ", "text": "Dünyada beş yaş altı çocuk ölümlerinin yaklaşık yarısı (%45-50) doğrudan veya dolaylı olarak yetersiz beslenme (malnütrisyon) ile ilişkilidir.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "DSÖ ve UNICEF küresel bebek beslenmesi stratejisinde emzirmeye doğumdan sonraki ilk 1 saat içinde başlanması, ilk 6 ay 'sadece anne sütü' verilmesi ve emzirmenin 2 yaşına veya ötesine kadar sürdürülmesi esastır.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-001",
        "question": "Dünya Sağlık Örgütü (DSÖ) ve UNICEF'in küresel çocuk sağlığı ve beslenme stratejileri doğrultusunda, optimal bebek beslenmesi ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            "A) Yenidoğanın doğumdan sonraki ilk 1 saat içinde emzirilmeye başlanması önerilir.",
            "B) Yaşamın ilk 6 ayında anne sütü alan bebeğe sıcak iklimlerde dahi su verilmesine gerek yoktur.",
            "C) Tamamlayıcı besinlere altıncı ayın bitiminde başlanmalı ve emzirme 2 yaşına veya daha sonrasına kadar sürdürülmelidir.",
            "D) Dünyada beş yaş altı çocuk ölümlerinin yaklaşık yarısı malnütrisyonla ilişkilidir.",
            "E) Bebek doğum ağırlığının iki katına ulaştığı 4. ayda anne sütü yetersizleştiğinden tamamlayıcı katı gıdalara geçilmelidir."
        ],
        "answer": "E) Bebek doğum ağırlığının iki katına ulaştığı 4. ayda anne sütü yetersizleştiğinden tamamlayıcı katı gıdalara geçilmelidir.",
        "explanation": "Tamamlayıcı besinlere geçiş için önerilen zaman tam 6. ayın bitimidir (180. gün). İlk 6 ayda anne sütü bebeğin tüm enerji, sıvı ve makro-mikrobesin gereksinimlerini %100 oranında tek başına karşılar. 4. ayda bebeğin tartısının iki katına çıkması fizyolojik bir büyüme süreci olup ek gıdaya başlama endikasyonu değildir; aksine 6 aydan önce ek gıdaya başlamak alerji, enfeksiyon ve anne sütünün erken kesilmesi riskini doğurur."
    }
))

# ==============================================================================
# SLAYT 2: Süt Çocuğunda Fizyolojik Büyüme Dinamikleri ve Sıvı Dağılımı
# ==============================================================================
slides.append(make_slide(
    2,
    "Süt Çocuğunda Fizyolojik Büyüme Dinamikleri ve Sıvı Dağılımı",
    "Fizyolojik Kilo Kaybı, Ağırlık/Boy Katlanma Eşikleri ve Vücut Sıvı Kompartmanları",
    """Yenidoğan bir bebeğin dünyaya adaptasyon sürecinde karşılaştığı ilk dinamik olay fizyolojik tartı kaybıdır. Doğumu takip eden ilk 3-5 gün içerisinde ekstrasellüler sıvı volümünün daralması, mekonyum ve idrar çıkışı ile henüz minimal hacimde olan kolostrum alımı nedeniyle bebekler kilo kaybederler. Term yenidoğanlarda doğum tartısının %5-10'una kadar olan kayıplar fizyolojik kabul edilir (prematürelerde bu oran %10-15'e kadar çıkabilir). Sağlıklı bir bebek genellikle yaşamın 10. ile 14. günleri arasında tekrar doğum tartısına ulaşmalıdır. Doğum tartısına 14. günde ulaşılamaması veya ağırlık kaybının %10'u aşması; yetersiz emzirme, dehidratasyon ve neonatal hipernatremi açısından acil klinik değerlendirme gerektiren bir kırmızı bayraktır.

Bebeklik dönemi, insan yaşam döngüsünde somatik büyüme hızının en yüksek olduğu evredir. Sağlıklı term bir süt çocuğu:
• Ortalama 4-5. aylarda doğum ağırlığının 2 katına (yaklaşık 6.5-7 kg),
• Bir yaşında doğum ağırlığının 3 katına (yaklaşık 10 kg),
• İki yaşında ise doğum ağırlığının yaklaşık 4 katına (yaklaşık 12-13 kg) ulaşır.
İkinci yılda kazanılan ağırlık (yaklaşık 2.5-3 kg), bebeğin doğum ağırlığına eşdeğerdir. Boy uzaması incelendiğinde; ortalama 50 cm doğan bir bebeğin boyu ilk yılda %50 artış göstererek 1 yaşında ortalama 75 cm'ye ulaşır; 4 yaşında ise doğum boyunun tam 2 katına (100 cm) erişir.

Vücut kompozisyonu ve sıvı kompartmanları büyüme sürecinde köklü bir yeniden yapılanmaya uğrar. Yenidoğan döneminde toplam vücut suyu, toplam vücut ağırlığının %70-75'ini oluştururken; yağ dokusunun birikimi ve hücre kitlesinin artışıyla 1 yaşında erişkin düzeyine yaklaşarak %60'a geriler. Toplam vücut yağı ilk 9 ayda olağanüstü bir ivmeyle artarak bebeğin termoregülasyonunu sağlar ve merkezi sinir sistemi miyelinizasyonu için lipit depoları oluşturur. Çocukluk döneminin geri kalanında yağ dokusu artış hızı yavaşlar. Süt çocuğunda günlük sıvı dönüşüm hızının (turnover) yüksek olması, onları dehidratasyona karşı erişkinden katbekat daha duyarlı kılar.""",
    [
        {"type": "clinical", "badge": "🔴 FİZYOLOJİK TARTI KAYBI EŞİĞİ", "text": "İlk günlerdeki kilo kaybı term bebekte %10'u geçmemeli ve bebek 10-14. günlerde doğum tartısını yakalamış olmalıdır.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Sağlıklı bir süt çocuğu doğum ağırlığının 4-5. aylarda 2 katına, 1 yaşında 3 katına; doğum boyunun ise 1 yaşında %50 fazlasına (75 cm), 4 yaşında 2 katına (100 cm) ulaşması beklenir.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-002",
        "question": "Zamanında, normal spontan vajinal yolla 3200 gram ve 50 cm olarak doğan sağlıklı bir bebeğin büyüme basamakları ile ilgili aşağıdaki beklentilerden hangisi fizyolojik gelişim kurallarına uymaz?",
        "options": [
            "A) Bebeğin yaşamın 3. gününde tartısının 3000 grama gerilemesi patolojik kabul edilmez.",
            "B) Bebeğin en geç 10-14. günlerde tekrar 3200 grama ulaşması beklenir.",
            "C) Bebeğin 5. ay civarında tartısının yaklaşık 6400 gram olması beklenir.",
            "D) Bebeğin 1 yaşındaki tahmini boyunun yaklaşık 100 cm olması beklenir.",
            "E) Bebeğin 1 yaşındaki tahmini ağırlığının yaklaşık 9600 gram olması beklenir."
        ],
        "answer": "D) Bebeğin 1 yaşındaki tahmini boyunun yaklaşık 100 cm olması beklenir.",
        "explanation": "Bebeğin boyu ilk 1 yılda %50 artarak ortalama 75 cm'ye ulaşır. Doğum boyunun iki katına (50 cm x 2 = 100 cm) ulaştığı yaş 1 yaş değil, 4 yaştır. Diğer seçeneklerdeki 4-5. ayda ağırlığın 2 katına (6400 g) ve 1 yaşında 3 katına (9600 g) çıkması ile ilk günlerdeki %5-10 fizyolojik tartı kaybı tamamen doğrudur."
    }
))

# ==============================================================================
# SLAYT 3: Gastrointestinal ve Renal İmmatüritenin Beslenme Açısından Önemi
# ==============================================================================
slides.append(make_slide(
    3,
    "Gastrointestinal ve Renal İmmatüritenin Beslenme Açısından Önemi",
    "Mide Kapasitesi, Asidite Dinamikleri, Enzim Matürasyonu ve Renal Konsantrasyon Kısıtlılığı",
    """Yenidoğan ve erken süt çocukluğu dönemi gastrointestinal sistemi, biyokimyasal ve mekanik açılardan henüz olgunlaşmamış (immatür) özellikler taşır. Doğumda bebeğin anatomik mide kapasitesi yalnızca 10-20 mL (bir ceviz büyüklüğünde) iken; 2. haftada 60-90 mL'ye, 1. ayda 90-150 mL'ye ve bir yaşında yaklaşık 200-250 mL'ye ulaşır. Bu kısıtlı mide hacmi, yenidoğanın neden seyrek ve bol öğünler yerine sık aralıklarla (günde 8-12 kez) ve küçük hacimlerle beslenmek zorunda olduğunu açıklar. Midenin boşalma süresi alınan sütün bileşimiyle doğrudan ilişkilidir: Anne sütü midede yumuşak, gevşek floküller oluşturarak ortalama 1.5 saatte duodenuma geçerken; inek sütü ve kazein ağırlıklı formüller sert kazein pıhtısı (curd) nedeniyle mideyi ancak 3-4 saatte terk eder.

Gastrik sekresyon dinamikleri incelendiğinde, yaşamın ilk haftalarında mide asiditesi düşüktür (gastrik pH erişkine göre daha nötrdür) ve gastrik pepsin salınımı sınırlıdır. Bu fizyolojik hipoklorhidri tablosu iki ucu keskin bir kılıç gibidir: Bir yandan anne sütündeki immünoglobulinlerin (özellikle sekretuvar IgA) ve biyoaktif büyüme faktörlerinin midede asit tarafından denatüre olmadan ve parçalanmadan doğrudan bağırsağa geçişini mümkün kılar; diğer yandan patojen mikroorganizmalara karşı gastrik asit bariyerinin zayıf kalmasına yol açar. İnce bağırsakta ise duodenal enzim aktiviteleri sınırlıdır. Özellikle pankreatik amilaz aktivitesi ilk 4-6 ayda neredeyse yok denecek düzeydedir. Bu nedenle süt çocuğuna 6 aydan önce nişastalı besinler (tahıl unları, patates vb.) verilmesi sindirilemeyen karbonhidratların kolonda fermantasyonuna, aşırı gaz sancısına ve ozmotik diyareye yol açar.

Yenidoğanın böbrek fonksiyonları da beslenme rejimini doğrudan kısıtlayan en kritik organ sistemidir. Yenidoğan böbreğinde glomerüler filtrasyon hızı (GFR) düşüktür ve Henle kulpunun kısalığı ile medüller hipertonisitenin yetersizliği nedeniyle tübüler konsantrasyon kapasitesi ileri derecede sınırlıdır. Sağlıklı bir erişkin böbreği idrarı 1200-1400 mOsm/kg düzeyine kadar konsantre ederek suyu tutabilirken, yenidoğan ve küçük süt çocuğu idrarı en fazla 600-700 mOsm/kg düzeyinde konsantre edebilir. Bu durum, bebeğin yüksek solüt yüküne (yüksek protein ve inorganik tuzlar) maruz kaldığında böbreklerden serbest suyu koruyamayarak hızla dehidrate olmasına ve hiperosmolaliteye girmesine zemin hazırlar.""",
    [
        {"type": "clinical", "badge": "🔴 PANKREATİK AMİLAZ EKSİKLİĞİ", "text": "İlk 4-6 ayda pankreatik amilaz aktivitesi yetersizdir; bu evrede nişastalı besin verilmesi ozmotik ishale ve malabsorpsiyona yol açar.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Süt çocuğunda renal konsantrasyon kapasitesi (maksimum 600-700 mOsm/kg) erişkinin (1200-1400 mOsm/kg) yaklaşık yarısı kadardır; bu nedenle yüksek renal solüt yükü hızla dehidratasyon doğurur.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-003",
        "question": "Süt çocuğunun gastrointestinal ve renal fizyolojisi ile ilgili aşağıdaki ifadelerden hangisi, beslenme yönetimi açısından doğru bir gerekçe sunmaz?",
        "options": [
            "A) Yenidoğanda mide kapasitesinin 10-20 mL olması nedeniyle ilk günlerde sık aralıklarla az miktarda besleme fizyolojiktir.",
            "B) Gastrik asiditenin ilk haftalarda düşük olması, anne sütündeki sekretuvar IgA'nın denatüre olmadan bağırsağa ulaşmasını destekler.",
            "C) Pankreatik amilaz aktivitesi doğumda erişkin düzeyinde olduğundan kompleks nişastalı katı gıdalar ilk aydan itibaren sindirilebilir.",
            "D) Anne sütünün kazein/whey oranı sayesinde midede gevşek pıhtı oluşur ve mide boşalması inek sütüne göre daha hızlıdır.",
            "E) İnfant böbreğinin idrar konsantrasyon kapasitesinin kısıtlı olması, yüksek solüt yüküne sahip gıdaların dehidratasyon riskini artırmasına neden olur."
        ],
        "answer": "C) Pankreatik amilaz aktivitesi doğumda erişkin düzeyinde olduğundan kompleks nişastalı katı gıdalar ilk aydan itibaren sindirilebilir.",
        "explanation": "Pankreatik amilaz aktivitesi yaşamın ilk 4-6 ayında neredeyse yoktur; kompleks polisakkaritleri sindiremez. Bu nedenle nişastalı ek gıdalara 6. aydan önce başlanmaz. Diğer tüm seçenekler doğru fizyolojik mekanizmaları açıklar."
    }
))

# ==============================================================================
# SLAYT 4: Süt Çocuğunda Enerji, Sıvı ve Makrobesin İhtiyaçları
# ==============================================================================
slides.append(make_slide(
    4,
    "Süt Çocuğunda Enerji, Sıvı ve Makrobesin İhtiyaçları",
    "Metabolik Harcama, Yaş Gruplarına Göre Sıvı Dengesi ve Büyümenin İzlenmesi",
    """Süt çocuğunun enerji tüketimi; bazal metabolizma hızı, fiziksel aktivite, besinlerin termik etkisi (spesifik dinamik etki), dışkı ile kayıplar ve yeni doku yapımını kapsayan 'büyüme' bileşeninden oluşur. Büyümenin payı yaşamın ilk 2 ayında toplam enerjinin yaklaşık %30-35'ini oluştururken, büyüme hızının yavaşlamasıyla 1 yaşında %5'e kadar geriler. Sağlıklı, zamanında doğmuş bir süt çocuğunun günlük enerji gereksinimi ilk 6 ayda ortalama 100-110 kcal/kg/gün (yaklaşık 20 kcal/30 mL veya 67 kcal/100 mL anne sütü) düzeyindedir; 6-12. aylarda ise ortalama 95-100 kcal/kg/gün seviyesine iner.

Süt çocukları, vücut yüzey alanlarının ağırlıklarına oranının yüksek olması, metabolizma hızlarının büyüklüğü ve renal konsantrasyon yeteneklerinin kısıtlılığı sebebiyle sıvı dengesizliklerine son derece duyarlıdır. Günlük sıvı gereksinimi harcanan kalori başına 1.5 mL/kcal/gün olarak kabul edilir. Ağırlık bazında yaşa göre günlük sıvı gereksinimleri şu şekildedir:
• 10 günlük bebek: 125-150 mL/kg/gün
• 3 aylık bebek: 140-160 mL/kg/gün
• 6 aylık bebek: 130-155 mL/kg/gün
• 1 yaşındaki çocuk: 120-135 mL/kg/gün
Anne sütünün hacimce %87-88'i sudan ibarettir. Bu nedenle sadece anne sütüyle beslenen bir bebeğe, çöl ikliminde veya aşırı sıcak yaz aylarında bile dışarıdan su verilmesine kesinlikle lüzum yoktur; su vermek tokluk hissi yaratarak süt tüketimini ve anne sütü üretimini düşürür.

Bir bebeğin enerji ve sıvı alımının yeterliliğini izlemenin en objektif ve güvenilir yolu, ağırlık, boy ve baş çevresi ölçümlerinin standart persentil büyüme eğrilerine (DSÖ büyüme eğrileri) işlenmesidir. Klinik pratikte yeterli beslenmenin göstergeleri: Bebeğin günde en az 6-8 kez açık renkli idrar yapması, emzirme sonrası doymuş şekilde gevşeyip 2-3 saat uyuması, aktif emme seslerinin duyulması ve ilk 3 ayda günde ortalama 25-30 gram (haftada 150-210 g) tartı artışı göstermesidir.""",
    [
        {"type": "clinical", "badge": "🔴 ANNE SÜTÜ ALAN BEBEĞE SU VERİLMESİ", "text": "Anne sütünün %87-88'i sudur. İlk 6 ay sadece anne sütü alan bebeğe sıcak iklimde dahi ek su verilmez; su verilmesi meme emmeyi azaltır ve enfeksiyon riski doğurur.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Süt çocuğunda sıvı gereksinimi tüketilen enerji başına yaklaşık 1.5 mL/kcal/gün olup, 3 aylık bir bebeğin ortalama günlük sıvı ihtiyacı 140-160 mL/kg/gün'dür.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-004",
        "question": "Üç aylık, sadece anne sütü ile beslenen, doğum tartısı 3200 g ve şu anki tartısı 6000 g olan sağlıklı bir süt çocuğunun beslenmesi ve hidrasyonu ile ilgili aşağıdaki klinik değerlendirmelerden hangisi yanlıştır?",
        "options": [
            "A) Günlük enerji gereksinimi yaklaşık 100-110 kcal/kg/gün düzeyindedir.",
            "B) Bebeğin günde 6-8 kez bezini ıslatması ve huzurlu uyuması sıvı alımının yeterli olduğunu gösterir.",
            "C) Yaz aylarında havanın çok sıcak olması durumunda her emzirme seansından sonra 30-50 mL kaynatılmış ılık su verilmelidir.",
            "D) Bebeğin günlük sıvı gereksinimi yaklaşık 140-160 mL/kg/gün düzeyindedir.",
            "E) Anne sütünün yaklaşık %87'si su olduğu için böbreklerin serbest su ihtiyacını eksiksiz karşılar."
        ],
        "answer": "C) Yaz aylarında havanın çok sıcak olması durumunda her emzirme seansından sonra 30-50 mL kaynatılmış ılık su verilmelidir.",
        "explanation": "İlk 6 ay sadece anne sütü alan bir bebeğe aşırı sıcak havalarda bile su verilmemelidir. Ek su verilmesi mide hacmini kaplayarak anne sütü alımını azaltır, hiponatremi (su zehirlenmesi) riski yaratır ve kontaminasyonla ishale zemin hazırlar. Sıcak havalarda çözüm daha sık emzirmektir."
    }
))

# ==============================================================================
# SLAYT 5: Protein ve Yağ Metabolizması: Esansiyel Yağ Asitleri ve Taurin
# ==============================================================================
slides.append(make_slide(
    5,
    "Protein ve Yağ Metabolizması: Esansiyel Yağ Asitleri ve Taurin",
    "Protein Katabolizması, Linoleik Asit, LC-PUFA (DHA/ARA) ve Nörogelişimsel Rolleri",
    """Hızlı büyüme ve hücre bölünmesi nedeniyle süt çocuğunun vücut ağırlığı başına düşen protein gereksinimi erişkine kıyasla oldukça yüksektir. Yaşamın ilk 6 ayında önerilen günlük protein alımı 2.2 g/kg/gün iken, 7-12. aylarda 1.6 g/kg/gün düzeyine geriler. Anne sütü, toplam protein konsantrasyonu formül mamalara ve inek sütüne göre daha düşük olmasına rağmen (~0.9-1.2 g/dL), biyolojik değeri ve esansiyel amino asit dengesi kusursuz olduğu için ilk 6 ayda bebeğin tüm protein gereksinimini eksiksiz temin eder. İkinci 6 ayda ise diyet; yoğurt, yumurta, kıyma gibi yüksek kaliteli hayvansal protein kaynaklarıyla desteklenmelidir.

Yağlar, süt çocuğu beslenmesinde en yoğun enerji kaynağını teşkil eder ve anne sütü toplam kalorisin yaklaşık %50'sini (tüketilen her 100 kcal başına 3.8 - 6.0 g yağ) karşılar. Diyet yağları yağda eriyen vitaminlerin (A, D, E, K) emilimini sağlamanın yanı sıra merkezi sinir sistemi miyelinizasyonu için esansiyel lipidleri temin eder. Linoleik asit (C18:2, omega-6) vücutta sentezlenemeyen temel bir esansiyel yağ asididir; cilt bütünlüğünün korunması, hücresel membran yapısı ve büyüme için zorunludur. Anne sütü enerjisinin yaklaşık %4-5'i linoleik asitten gelir; bu oran eksikliği önleyen eşiğin (%1-2) katbekat üzerindedir.

Anne sütü lipid fraksiyonunun formül mamalardan en üstün yönü, uzun zincirli çoklu doymamış yağ asitlerini (LC-PUFA) hazır ve dengeli olarak içermesidir: Dokozaheksaenoik asit (DHA, 22:6 n-3) ve Araşidonik asit (ARA, 20:4 n-6). Bu yağ asitleri serebral korteks gri cevherinin ve retina fotoreseptör membranlarının temel yapı taşıdır. Anne sütüyle beslenen bebeklerin bilişsel fonksiyon testlerinde ve görme keskinliği muayenelerinde mama ile beslenenlere kıyasla daha başarılı olmalarının temelinde DHA ve ARA zenginliği yatar. Ayrıca anne sütünde serbest bir beta-amino sülfonik asit olan Taurin düzeyi inek sütünden 30-40 kat daha fazladır. Taurin; karaciğerde safra asitlerinin konjugasyonunda, retina membran stabilitesinde ve serbest radikal hasarını önlemede vazgeçilmez bir role sahiptir.""",
    [
        {"type": "clinical", "badge": "🔴 TAURİNİN KRİTİK ROLLERİ", "text": "Anne sütündeki taurin inek sütünden 30-40 kat fazladır; retina fotoreseptör gelişimi, nörotransmisyon ve safra asidi konjugasyonu için vazgeçilmezdir.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Anne sütünde bulunan DHA (dokozaheksaenoik asit) ve ARA (araşidonik asit), beyin korteksi ve retina miyelinizasyonunda görevli esansiyel LC-PUFA'lardır.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-005",
        "question": "Anne sütünün biyokimyasal içeriğinde bulunan lipid ve amino asit fraksiyonları ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            "A) Anne sütü enerjisinin yaklaşık %50'si yağlardan sağlanmaktadır.",
            "B) Linoleik asit anne sütü enerjisinin yaklaşık %5'ini oluşturarak cilt bütünlüğü ve büyüme gereksinimini karşılar.",
            "C) Anne sütünde serbest taurin konsantrasyonu inek sütüne göre 30-40 kat daha fazladır.",
            "D) DHA ve ARA, retina fotoreseptör tabakası ve serebral korteks gelişimi için kritik öneme sahip LC-PUFA türevleridir.",
            "E) Yenidoğan döneminde protein ihtiyacı erişkinden düşük olduğu için ilk 6 ayda kilogram başına 0.8 g protein verilmesi yeterlidir."
        ],
        "answer": "E) Yenidoğan döneminde protein ihtiyacı erişkinden düşük olduğu için ilk 6 ayda kilogram başına 0.8 g protein verilmesi yeterlidir.",
        "explanation": "Yenidoğan ve süt çocuğunda hızlı somatik büyüme nedeniyle kilogram başına protein ihtiyacı erişkinden (erişkin ~0.8-1.0 g/kg/gün) çok daha yüksektir. 0-6 ayda protein ihtiyacı 2.2 g/kg/gün, 7-12 ayda ise 1.6 g/kg/gün düzeyindedir."
    }
))

# ==============================================================================
# SLAYT 6: Mikrobesin Dengesi: Demir, Çinko, Kalsiyum-Fosfor ve Flor
# ==============================================================================
slides.append(make_slide(
    6,
    "Mikrobesin Dengesi: Demir, Çinko, Kalsiyum-Fosfor ve Flor",
    "Depoların Tükenme Zamanı, Emilim Dinamikleri ve Rutin Profilaksiler",
    """Zamanında (term) doğan sağlıklı bir bebeğin vücut demir depoları, fetal yaşamın son trimesterinde anneden aktif transplasental taşınmayla oluşturulur. Bu fetal depolar, bebek doğum ağırlığının 2 katına ulaşana kadar (term bebekte yaklaşık 4-6 ay) eritropoez için yeterli demiri sağlar. Prematüre ve düşük doğum ağırlıklı bebeklerde ise fetal depo süresi kısa kaldığından demir depoları 2. ayda tükenir. Anne sütünün demir konsantrasyonu mutlak değer olarak düşük olmasına karşın (~0.3-0.5 mg/L), emilim oranı olağanüstü yüksektir (%50-60). İnek sütündeki demirin ise yalnızca %10'u emilebilir. Ancak 4-6. aydan sonra depolar tükendiğinden, Sağlık Bakanlığı Çocuk Sağlığı izlem protokolü gereğince tüm term bebeklere 4. aydan itibaren 1 mg/kg/gün profilaktik elemental demir (prematürelere 2. aydan itibaren 2 mg/kg/gün) başlanmalıdır.

Çinko, DNA ve RNA polimerazlar başta olmak üzere 300'den fazla enzimin yapısına giren, hücresel proliferasyon, epitel bütünlüğü ve immün direnç için şart olan bir iz elementtir. Yenidoğanın vücudunda mobilize edilebilir çinko deposu bulunmadığından diyet kaynaklı çinkoya doğar doğmaz ihtiyaç duyar. Anne sütündeki çinko, özel düşük molekül ağırlıklı çinko bağlayıcı ligandlar sayesinde formül mamalara göre katbekat yüksek biyoyararlanıma sahiptir ve ilk 6 ay bebeğe tam yeterlidir. 6. aydan sonra tamamlayıcı beslenmeye geçildiğinde kırmızı et ve yumurta gibi zengin hayvansal çinko kaynaklarının diyete eklenmesi gerekir.

Kalsiyum ve fosfor metabolizmasında kritik kavram mutlak miktar değil 'Ca/P oranı'dır. Anne sütünde Ca/P oranı 2:1 gibi biyolojik açıdan ideal bir dengededir ve anne sütündeki kalsiyumun yaklaşık 2/3'ü (%60-70) vücut tarafından emilip kemiklere yatırılır. İnek sütünde ise kalsiyum 3 kat, fosfor ise tam 6 kat fazladır ve Ca/P oranı 1.2:1'e düşer. İnek sütünün bu aşırı fosfor yükü immatür böbrekten atılamaz; kanda fosfor birikir (hiperfosfatemi), serum serbest kalsiyumunu çöktürür ve yaşamın ilk haftalarında 'Neonatal Hipokalsemik Tetani' ve konvülsiyonlara yol açar. Anne sütünün flor içeriği ise düşüktür (<0.05 mg/L); diş çıkarma sonrası topikal ve içme suyu florizasyonu diş çürüklerinden korunmada temel unsurdur.""",
    [
        {"type": "clinical", "badge": "🔴 RUTİN DEMİR PROFİLAKSİSİ", "text": "Term bebeklerde fetal demir depoları 4. ayda tükenmeye başlar; bu nedenle 4. aydan itibaren tüm term bebeklere 1 mg/kg/gün profilaktik demir başlanır.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "İnek sütündeki aşırı fosfor (Ca/P oranının 1.2:1 olması), yenidoğanda hiperfosfatemiye ve sekonder hipokalsemik tetaniye yol açar. Anne sütünde Ca/P oranı 2:1'dir.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-006",
        "question": "Süt çocuğu beslenmesinde demir ve kalsiyum-fosfor dengesi ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            "A) Anne sütündeki demirin biyoyararlanımı yaklaşık %50 iken, inek sütündeki demirin emilimi yaklaşık %10 düzeyindedir.",
            "B) Term doğan sağlıklı bir bebeğin demir depoları genellikle doğum ağırlığının iki katına ulaştığı 4-6. aylara kadar yeterlidir.",
            "C) İnek sütü ile beslenen yenidoğanlarda aşırı fosfor yüklenmesine bağlı olarak neonatal hipokalsemik tetani riski artar.",
            "D) Anne sütündeki Ca/P oranı yaklaşık 2:1 olup kalsiyumun emilimi için optimal fizyolojik ortamı sağlar.",
            "E) Anne sütü alan term bebeklere demir depolarının zengin olması nedeniyle 1 yaşına kadar hiçbir koşulda profilaktik demir verilmemelidir."
        ],
        "answer": "E) Anne sütü alan term bebeklere demir depolarının zengin olması nedeniyle 1 yaşına kadar hiçbir koşulda profilaktik demir verilmemelidir.",
        "explanation": "Term bebeklerin demir depoları 4-6. ayda tükenir. Anne sütü demirinin biyoyararlanımı yüksek olsa da mutlak miktarı düşüktür ve 4. aydan sonra artan kan volümünü karşılayamaz. Bu nedenle Sağlık Bakanlığı protokolüne göre tüm term bebeklere 4. aydan itibaren 1 mg/kg/gün profilaktik demir başlanması zorunludur."
    }
))

# ==============================================================================
# SLAYT 7: Vitamin Profili ve Yaşamın Başındaki Rutin Profilaksiler
# ==============================================================================
slides.append(make_slide(
    7,
    "Vitamin Profili ve Yaşamın Başındaki Rutin Profilaksiler",
    "Yenidoğanın Hemorajik Hastalığı (K Vitamini), Raşitizm Profilaksisi (D Vitamini) ve B12 Riski",
    """Yenidoğan bir bebeğin dünyaya geldiği andan itibaren hekimin yönetmesi gereken iki hayati vitamin açığı vardır: K vitamini ve D vitamini. Yenidoğanlar; plasentadan K vitamini geçişinin son derece kısıtlı olması, karaciğerde pıhtılaşma faktörleri (Faktör II, VII, IX, X) sentezinin immatürlüğü ve bağırsak florasında henüz K vitamini sentezleyen mikroorganizmaların bulunmaması sebebiyle derin bir K vitamini eksikliği ile doğarlar. Bu tablo önlenmediğinde yaşamın ilk günlerinde veya 2-8. haftalarında gastrointestinal, umbilikal ve en ölümcülü intrakraniyal kanamalarla seyreden 'Yenidoğanın Hemorajik Hastalığı' (K Vitamini Eksikliği Kanaması - VKDB) gelişir. Bu fatal komplikasyonu engellemek için doğumdan hemen sonra tüm yenidoğanlara rutin olarak 1 mg intramüsküler (IM) K1 vitamini (fitomenadion) uygulanmalıdır.

Anne sütü, zamanında doğmuş bir bebeğin hemen hemen tüm vitamin ihtiyaçlarını eksiksiz karşılarken tek bir kritik istisnaya sahiptir: D VİTAMİNİ. Anne sütünün D vitamini içeriği düşüktür (litrede yalnızca 20-40 IU D vitamini içerir). Bebeğin günlük D vitamini gereksinimi ise en az 400 IU'dur. Cilt kanseri riski nedeniyle bebeklerin doğrudan güneş ışığına maruz bırakılması da önerilmediğinden; beslenme şeklinden bağımsız olarak (sadece anne sütü veya formül mama almasına bakılmaksızın) doğumdan itibaren TÜM BEBEKLERE en az 1 yaşına kadar günlük 400 IU (günde 3 damla D3 vitamini) profilaksisi verilmesi zorunludur.

Suda eriyen vitaminler (B kompleksi ve C vitamini) annenin beslenme durumunu doğrudan yansıtır. Anne sütü C vitamini yönünden zengindir ve ilk 6 ay skorbütten tamamen korur; buna karşın pastörize/kaynatılmış inek sütünde C vitamini ısı ile tahrip olur. B12 vitamini hayvansal gıdalarda bulunur; katı vejetaryen/vegan beslenen veya pernisiyöz anemisi, gastrik bypass cerrahisi bulunan annelerin bebeklerinde ciddi B12 eksikliği, megaloblastik anemi ve geri dönüşümsüz nöromotor gelişim geriliği (hipotoni, tremor, konvülsiyon) gelişir. Ayrıca keçi sütü folat ve B12 yönünden ileri derecede yetersiz olup 'keçi sütü anemisi'ne (megaloblastik anemi) yol açtığından bebek beslenmesinde tek başına asla kullanılmamalıdır.""",
    [
        {"type": "clinical", "badge": "🔴 RUTİN D VİTAMİNİ PROFİLAKSİSİ", "text": "Anne sütü D vitamininden fakirdir. Doğumdan itibaren beslenme şekline bakılmaksızın tüm bebeklere 400 IU/gün (3 damla) D vitamini profilaksisi başlanmalıdır.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Doğumda intramüsküler 1 mg K vitamini uygulanmasının temel amacı, intrakraniyal kanamalara yol açabilen 'Yenidoğanın Hemorajik Hastalığı'nı önlemektir.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-007",
        "question": "Yenidoğan ve süt çocuğu döneminde vitamin gereksinimleri ve rutin profilaksiler ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            "A) Yenidoğanın hemorajik hastalığını önlemek amacıyla doğumu takiben 1 mg K vitamini intramüsküler uygulanır.",
            "B) Anne sütü D vitamini açısından zengin olduğu için sadece anne sütü alan bebeklere ilk 6 ay D vitamini desteği gerekmez.",
            "C) Katı vejetaryen annelerin anne sütü ile beslenen bebeklerinde B12 vitamini eksikliği ve megaloblastik anemi görülebilir.",
            "D) Keçi sütü folik asit ve B12 vitamini açısından yetersiz olduğundan bebeklerde megaloblastik anemiye yol açabilir.",
            "E) Anne sütü C vitamini açısından zengin olup ilk 6 ayda bebeğin gereksinimini tam olarak karşılar."
        ],
        "answer": "B) Anne sütü D vitamini açısından zengin olduğu için sadece anne sütü alan bebeklere ilk 6 ay D vitamini desteği gerekmez.",
        "explanation": "Anne sütü hemen tüm besin ögelerinden zengin olmasına rağmen D vitamininden fakirdir (litrede sadece 20-40 IU). Bu nedenle sadece anne sütü alanlar dahil tüm bebeklere doğumdan itibaren günlük 400 IU D vitamini profilaksisi verilmesi zorunludur."
    }
))

# ==============================================================================
# SLAYT 8: Laktasyonun Evreleri: Kolostrum, Geçiş Sütü ve Olgun Süt Dinamikleri
# ==============================================================================
slides.append(make_slide(
    8,
    "Laktasyonun Evreleri: Kolostrum, Geçiş Sütü ve Olgun Süt Dinamikleri",
    "Zamansal Dönüşüm, Biyokimyasal Farklılıklar ve Mekonyum Eliminasyonu",
    """İnsan sütü statik bir sıvı değil, bebeğin büyüme basamaklarına ve metabolik olgunlaşmasına mükemmel şekilde uyum sağlayan dinamik, canlı bir biyolojik dokudur. Doğumdan itibaren salgılanan anne sütü kronolojik olarak üç ana evreye ayrılır:
1. **Kolostrum (Ağız Sütü):** Doğumdan sonraki ilk 4-5 gün boyunca salgılanan süttür.
2. **Geçiş Sütü (Transisyonel Süt):** 6. günden 15. güne kadar süren, kolostrumdan olgun süte geçiş evresidir.
3. **Olgun Süt (Matür Süt):** 15. günden itibaren laktasyonun sonuna kadar salgılanan dengeli süttür.

Kolostrum; sarımsı-koyu kıvamlı, adeta konsantre bir altın damlasıdır. Sarı rengini yüksek beta-karoten içeriğinden alır. Olgun süte kıyasla yağ ve laktoz içeriği daha düşük; buna karşılık protein, sodyum, potasyum, klor, çinko ve yağda eriyen vitaminler (A ve E vitaminleri) açısından belirgin şekilde daha zengindir. Kolostrumun en çarpıcı özelliği immünolojik yoğunluğudur: Sekretuvar IgA (sIgA), laktoferrin, lizozim ve maternal canlı lökositler (makrofaj ve nötrofiller) açısından olgun sütten katbekat yoğundur. Bir bebeğin steril intrauterin ortamdan mikroplarla dolu dış dünyaya geçişinde aldığı ilk doğal mukozal aşıdır.

Kolostrumun bir diğer eşsiz fizyolojik işlevi hafif laksatif (müshil) etkisidir. Gastrointestinal motiliteyi artırarak mekonyumun ilk 24-48 saat içinde hızla atılmasını sağlar. Bu sayede bağırsak lümeninde biriken indirekt bilirubinin enterohepatik dolaşımla geri emilmesi engellenir ve hiperbilirubinemi (sarılık) riski önemli ölçüde azaltılır. Anne sütünün bileşimi doğum haftasına göre de farklılaşır: Prematüre doğuran annelerin sütü, ilk haftalarda term doğuranlara kıyasla daha yüksek protein, sodyum, klor ve immünolojik koruyucu içerirken laktoz oranı daha düşüktür; bu sayede prematürenin yüksek protein ihtiyacını karşılarken immatür laktaz kapasitesini korur.""",
    [
        {"type": "clinical", "badge": "🔴 KOLOSTRUMUN LAKSATİF ETKİSİ", "text": "Kolostrum mekonyum atılımını hızlandırarak bilirubinin enterohepatik dolaşımla geri emilimini önler ve yenidoğan sarılığı riskini azaltır.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Kolostrum olgun süte göre protein, sodyum, klor, sIgA, laktoferrin ve vitamin A'dan daha zengin; laktoz ve yağdan ise daha fakirdir.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-008",
        "question": "Doğumdan sonraki ilk 4-5 gün boyunca salgılanan kolostrum (ağız sütü) ile olgun anne sütünün karşılaştırılması hakkında aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            "A) Kolostrumun protein içeriği olgun anne sütüne göre daha yüksektir.",
            "B) Kolostrum sekretuvar IgA, laktoferrin ve lökositler açısından son derece zengindir.",
            "C) Kolostrumun laktoz ve yağ konsantrasyonu olgun anne sütünden daha yüksektir.",
            "D) Kolostrum içerdiği sodyum, potasyum ve klor gibi mineraller yönünden olgun sütten zengindir.",
            "E) Kolostrum laksatif etkisiyle mekonyumun atılımını hızlandırarak neonatal sarılık riskini azaltır."
        ],
        "answer": "C) Kolostrumun laktoz ve yağ konsantrasyonu olgun anne sütünden daha yüksektir.",
        "explanation": "Kolostrum olgun süte göre DAHA AZ yağ ve DAHA AZ laktoz içerir. Buna karşılık protein, sodyum, klor, çinko, A vitamini, sIgA ve laktoferrin konsantrasyonu olgun sütten belirgin şekilde daha yüksektir."
    }
))

# ==============================================================================
# SLAYT 9: Emzirme Seansının İç Dinamiği: Ön Süt ile Son Süt Arasındaki Kritik Denge
# ==============================================================================
slides.append(make_slide(
    9,
    "Emzirme Seansının İç Dinamiği: Ön Süt ile Son Süt Arasındaki Kritik Denge",
    "Laktoz Yükü, Yağ Yoğunluğu, Doygunluk Mekanizması ve Meme Boşalmasının Önemi",
    """Anne sütünün kompozisyonu sadece laktasyonun evreleri boyunca değil, tek bir emzirme seansının başlangıcı ile bitişi arasında da dinamik olarak değişir. Emzirme seansının başlangıcında gelen süte 'Ön Süt' (foremilk), seansın sonuna doğru meme derinliklerinden sağılan süte ise 'Son Süt' (hindmilk) adı verilir. Bu iki fraksiyon arasındaki biyokimyasal tezat, bebeğin hidrasyonu ve enerji regülasyonu açısından hayati bir fizyolojik mekanizmadır.

Ön süt; mavimsi-beyaz, sulu ve akışkandır. İçeriğinde yüksek oranda su, protein, suda eriyen vitaminler ve özellikle bol miktarda LAKTOZ bulunur. Ön sütün temel fizyolojik görevi; bebeğin susuzluğunu (hidrasyon ihtiyacını) gidermek ve emmeye başladığı anda kan şekerini hızla regüle ederek emme motivasyonunu canlı tutmaktır. Bebek emmeye devam ettikçe, oksitosin etkisiyle alveol myoepitelyal hücreleri kasılır ve meme bezi kanallarındaki akım hızlanır. Bu mekanik hareketle, alveol epitel hücrelerinin membranına tutunmuş halde duran yağ damlacıkları koparak süte karışır. Sonuç olarak seansın sonuna doğru sütün rengi krema kıvamına ve koyu beyaza döner; yağ içeriği ön süte kıyasla tam 4-5 katına çıkar, protein miktarı ise yaklaşık %50 artar.

Son sütün yüksek yağ ve kalori içeriği kolesistokinin (CCK) salgılanmasını uyararak bebeğin hipotalamusundaki tokluk merkezini tetikler; bebek doygunluk hissine ulaşarak memeyi kendiliğinden bırakır ve kilo alımı sağlanır. Burada yapılan EN BÜYÜK KLİNİK HATA: Annenin bebeği bir memede 5-7 dakika tutup henüz o meme boşalmadan diğer memeye geçirmesidir. Bu durumda bebek her iki memeden de sadece laktozdan zengin ön sütü alır, yağdan zengin son sütü alamaz. Sonuçta; bağırsakta fermente olan aşırı laktoza bağlı gaz sancısı (infantil kolik), yeşil, köpüklü, asidik dışkılama, perianal eritem ve kilo alamama tablosu ortaya çıkar. Anneye bir meme tamamen boşalana kadar bebeğin aynı memede tutulması gerektiği mutlaka öğretilmelidir.""",
    [
        {"type": "clinical", "badge": "🔴 ÖN SÜT - SON SÜT KLİNİK SENDROMU", "text": "Bebek memeyi tam boşaltmadan diğer memeye geçirilirse aşırı laktoz yükü nedeniyle huzursuzluk, gaz sancısı, köpüklü-yeşil dışkı ve kilo alamama gelişir.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Emzirme seansında ön süt su ve laktozdan zenginken; son sütte yağ miktarı 4-5 kat, protein miktarı ise yaklaşık %50 oranında artarak tokluk sağlar.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-009",
        "question": "İki aylık sağlıklı bir bebeğin annesi; bebeğin emzirme sonrasında sürekli ağladığını, karnında aşırı gaz olduğunu, dışkısının yeşil renkli, sulu ve köpüklü olduğunu ve son kontrolde yeterli kilo alamadığını belirtiyor. Öyküde annenin sütü bol olduğu için bebeği her iki memeden 5'er dakika emzirip bıraktığı öğreniliyor. Bu tablonun altında yatan temel patofizyolojik mekanizma aşağıdakilerden hangisidir?",
        "options": [
            "A) Anne sütünde kazein oranının aşırı yüksek olması",
            "B) Bebeğin yağdan zengin son sütü alamayıp laktozdan zengin ön sütü aşırı tüketmesi",
            "C) Annede sekretuvar IgA eksikliğine bağlı sekonder enfeksiyon",
            "D) Bebekte konjenital laktaz eksikliği tablosu",
            "E) Anne sütünde renal solüt yükünün yüksek olması"
        ],
        "answer": "B) Bebeğin yağdan zengin son sütü alamayıp laktozdan zengin ön sütü aşırı tüketmesi",
        "explanation": "Bebek memeyi tamamen boşaltmadan diğer memeye geçirildiğinde, yağdan zengin kalorili 'son süt'ü alamaz; sadece su ve laktozdan zengin 'ön süt'ü alır. Aşırı laktoz kolonda bakterilerce fermente edilir; laktik asit ve hidrojen gazı açığa çıkarak infantil kolik, asidik-köpüklü yeşil dışkı, pişik ve kalori yetersizliğine bağlı kilo alamama tablosuna yol açar."
    }
))

# ==============================================================================
# SLAYT 10: Biyokimyasal Karşılaştırma I: Kazein ve Whey (Peyniraltı Suyu) Fraksiyonları
# ==============================================================================
slides.append(make_slide(
    10,
    "Biyokimyasal Karşılaştırma I: Kazein ve Whey Fraksiyonları",
    "Protein Oranları (40:60 vs. 80:20), Pıhtılaşma Karakteri ve Beta-Laktoglobulin Tehdidi",
    """Süt proteinleri temel olarak iki büyük fraksiyona ayrılır: Asidik ortamda çöken kalsiyum bağlı proteinler olan 'Kazein' ve sıvıda çözünmüş halde kalan 'Whey' (peyniraltı suyu) proteinleri. İnsan sütü ile inek sütü arasındaki en köklü fark bu iki fraksiyonun oranında ve kalitesinde yatar. İnsan olgun sütünde Kazein/Whey oranı 40:60'tır (erken laktasyonda bu oran 20:80 veya 10:90'a kadar iner). İnek sütünde ise tam tersine Kazein/Whey oranı 80:20'dir. Yani inek sütü kazein ağırlıklı iken, anne sütü whey proteini baskın bir süttür.

Bu oransal fark mide sindiriminde dramatik sonuçlar doğurur: İnek sütünün yüksek kazein içeriği mide asidi ve pepsinle karşılaştığında sert, kaba, çözünmesi güç yoğun bir pıhtı (curd) oluşturur. Bu durum midenin boşalma süresini 3-4 saate kadar uzatır ve süt çocuğunun immatür sindirim sisteminde kramplara ve distansiyona neden olur. Anne sütünün baskın whey içeriği ise midede yumuşak, gevşek floküller meydana getirir; sindirim enzimleri tarafından hızla hidrolize edilerek mideyi ortalama 1.5 saatte terk eder. Anne sütündeki kazein başlıca beta-kazein olup, fosfor ve kalsiyum emilimini kolaylaştıran miseller oluşturur.

Whey fraksiyonunun niteliksel bileşimi alerji ve immünoloji açısından en kritik ayrımı oluşturur: İnek sütünün en temel whey proteini olan ve çocukluk çağındaki inek sütü proteini alerjisinin (İSPA) bir numaralı sorumlusu kabul edilen BETA-LAKTOGLOBULİN, ANNE SÜTÜNDE KESİNLİKLE BULUNMAZ! Anne sütünün whey fraksiyonunu ise bebeğin fizyolojisine uygun alfa-laktalbumin (%25-35), laktoferrin (%15-20), sekretuvar IgA (%10-12) ve lizozim oluşturur. Anne sütü, bebeğin bağırsak epiteline yabancı antijen sunmayan, immünolojik koruyuculuğu en üst düzeye çıkarılmış mükemmel bir tasarımdır.""",
    [
        {"type": "clinical", "badge": "🔴 BETA-LAKTOGLOBULİN ALERJENİ", "text": "İnek sütündeki başlıca alerjen whey proteini olan Beta-Laktoglobulin anne sütünde KESİNLİKLE BULUNMAZ.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Kazein / Whey oranı anne sütünde 40:60 (whey baskın), inek sütünde ise 80:20 (kazein baskın)'dir. Bu nedenle anne sütü midede yumuşak floküller yaparak hızlı sindirilir.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-010",
        "question": "Anne sütü ile inek sütünün protein fraksiyonları ve özellikleri karşılaştırıldığında aşağıdaki ifadelerden hangisi doğru bir bilgidir?",
        "options": [
            "A) Anne sütünde kazein/whey oranı 80:20 olup inek sütünden daha sert pıhtı oluşturur.",
            "B) İnek sütünde bulunan en önemli alerjen protein olan beta-laktoglobulin anne sütünde kesinlikle bulunmaz.",
            "C) İnek sütünün mide boşalma süresi anne sütünden daha kısadır.",
            "D) Anne sütü whey proteinlerinin büyük kısmını alfa-s1 kazein oluşturur.",
            "E) Anne sütündeki toplam protein konsantrasyonu inek sütündekinden yaklaşık 3 kat daha fazladır."
        ],
        "answer": "B) İnek sütünde bulunan en önemli alerjen protein olan beta-laktoglobulin anne sütünde kesinlikle bulunmaz.",
        "explanation": "Beta-laktoglobulin inek sütünün ana whey proteini ve süt çocukluğundaki en güçlü alerjendir; insan sütünde kesinlikle bulunmaz. Anne sütünde Kazein/Whey oranı 40:60 iken inek sütünde 80:20'dir. Anne sütü toplam proteini ~1 g/dL iken inek sütü ~3.3 g/dL'dir."
    }
))

# ==============================================================================
# SLAYT 11: Biyokimyasal Karşılaştırma II: Karbonhidratlar, Lipitler ve Biyoyararlanım
# ==============================================================================
slides.append(make_slide(
    11,
    "Biyokimyasal Karşılaştırma II: Karbonhidratlar, Lipitler ve Biyoyararlanım",
    "Laktoz Üstünlüğü, Demir-Çinko Emilim Oranları (%50 vs. %10) ve Safra Tuzu Bağımlı Lipaz",
    """Karbonhidrat kompozisyonunda insan sütü tüm memeli türleri arasında en yüksek laktoz yoğunluğuna sahip sütlerden biridir. Anne sütündeki laktoz konsantrasyonu yaklaşık 7.0 g/dL iken, inek sütünde bu değer 4.8 g/dL düzeyindedir. Laktoz (glukoz + galaktoz); galaktoz molekülü sayesinde merkezi sinir sisteminde serebrosid ve sfingomiyelin sentezinin vazgeçilmez ham maddesidir. Ayrıca kolona ulaşan laktoz, laktobasiller ve bifidobakteriler tarafından laktik aside fermente edilerek bağırsak pH'sını asidik tutar. Bu asidik lümen ortamı bir yandan patojen enterik bakterilerin yerleşmesini engellerken, diğer yandan kalsiyum, magnezyum ve demirin iyonize çözünürlüğünü artırarak bağırsaktan emilimlerini belirgin şekilde stimüle eder.

Demir içeriği mutlak konsantrasyon olarak hem anne sütünde hem de inek sütünde düşüktür (her iki sütte de yaklaşık 0.3-0.5 mg/L). Ancak biyoyararlanım açısından aralarında devasa bir uçurum vardır: Anne sütündeki demirin yaklaşık %50-60'ı mükemmel bir şekilde emilirken, inek sütündeki demirin yalnızca %10'u emilebilmektedir! Anne sütündeki demir biyoyararlanımını bu denli yüksek kılan faktörler; yüksek laktoz, yüksek C vitamini, düşük fosfor, düşük kazein ve laktoferrinin demiri spesifik enterosit reseptörlerine doğrudan teslim etmesidir. Ancak bu üstün biyoyararlanım 'SADECE ANNE SÜTÜ' alındığında geçerlidir. Bebeğe dışarıdan meyve veya sebze püresi gibi ek besinler erken verildiğinde, bağırsak mikroçevresi bozulur ve anne sütü demirinin emilimi derhal %10 düzeyine geriler.

Lipit metabolizmasında insan sütü bir başka biyokimyasal mucizeye sahiptir: Anne sütünde meme bezinden salgılanan 'Safra Tuzu Bağımlı Lipaz' (BSSL / Bile Salt-Stimulated Lipase) enzimi mevcuttur. Yenidoğanın pankreatik lipazı ve safra tuzu havuzu henüz immatür olmasına rağmen, anne sütü ile bebeğin midesine giren BSSL duodenumda aktifleşerek trigliseritleri ester bağlarından hidrolize eder ve anne sütü yağının emilimini %95'in üzerine çıkarır. Buna karşın inek sütü BSSL içermez ve uzun zincirli doymuş yağ asitleri içerir; bu nedenle inek sütü yağının %20-48'i sindirilemeden feçesle kaybedilir ve kalsiyum sabunları oluşturarak inatçı kabızlığa yol açar.""",
    [
        {"type": "clinical", "badge": "🔴 EK GIDANIN DEMİR EMİLİMİNE ETKİSİ", "text": "Anne sütündeki demirin %50-60'ı emilir. Ancak erken ek gıda verildiğinde lümen ortamı bozularak demir emilimi anında %10'a düşer!", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Anne sütü yağı Safra Tuzu Bağımlı Lipaz (BSSL) sayesinde %95 emilirken; inek sütü yağının %20-48'i sindirilemeyip feçesle atılır.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-011",
        "question": "Anne sütü ile inek sütünün karbonhidrat, demir ve yağ sindirimi parametreleri karşılaştırıldığında aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            "A) Anne sütündeki laktoz konsantrasyonu inek sütündekinden belirgin şekilde daha yüksektir.",
            "B) Laktozun bağırsakta laktik aside fermente olması lümen pH'sını düşürerek kalsiyum ve demir emilimini kolaylaştırır.",
            "C) Anne sütündeki demirin yaklaşık %50-60'ı emilirken, inek sütündeki demirin yalnızca %10'u emilebilir.",
            "D) Anne sütü alan bebeğe erken dönemde meyve püresi başlanması demir emilimini %50'den %10'a düşürür.",
            "E) İnek sütü yüksek miktarda safra tuzu bağımlı lipaz (BSSL) içerdiği için yağ emilim yüzdesi anne sütünden üstündür."
        ],
        "answer": "E) İnek sütü yüksek miktarda safra tuzu bağımlı lipaz (BSSL) içerdiği için yağ emilim yüzdesi anne sütünden üstündür.",
        "explanation": "BSSL (Safra Tuzu Bağımlı Lipaz) enzimi anne sütünde bulunur, inek sütünde bulunmaz. Bu sayede anne sütü yağı %95 oranında emilirken, inek sütü yağının %20-48'i sindirilemeden feçesle kaybedilir."
    }
))

# ==============================================================================
# SLAYT 12: Renal Solüt Yükü (RSL), Osmolarite ve İnfant Böbreğinin Korunması
# ==============================================================================
slides.append(make_slide(
    12,
    "Renal Solüt Yükü (RSL), Osmolarite ve İnfant Böbreğinin Korunması",
    "Elektrolit Yükü, İdrar Konsantrasyon Kapasitesi ve Hipernatremik Dehidratasyon Riski",
    """Renal Solüt Yükü (RSL); diyetle alınan besinlerin katabolizması sonucu böbrekler yoluyla idrarla atılması gereken çözünmüş maddelerin (özellikle üre, sodyum, potasyum, klor ve kullanılmayan fosfor) toplam miktarını ifade eder. Bir besinin renal solüt yükü ne kadar yüksekse, böbreğin bu solütleri kandan temizleyip atabilmesi için o kadar fazla obligat (zorunlu) idrar suyuna ihtiyacı vardır. Süt çocuğunun böbreği henüz immatür olup idrarı en fazla 600-700 mOsm/kg konsantre edebildiğinden, yüksek solüt yükü infant fizyolojisi için ciddi bir metabolik tehdittir.

Anne sütünün osmolaritesi ortalama 286-300 mOsm/kg iken, inek sütünün osmolaritesi yaklaşık 400 mOsm/kg civarındadır. Daha da önemlisi, Potansiyel Renal Solüt Yükü (PRSL) açısından inek sütü anne sütünün yaklaşık üç katıdır (inek sütünde ~30-35 mOsm/100 kcal iken anne sütünde ~10-12 mOsm/100 kcal). İnek sütündeki sodyum ve potasyum miktarı anne sütünün tam 3 katı, fosfor ise tam 6 katıdır. Ayrıca inek sütünün yüksek protein içeriğinin (%20 enerji proteinden gelir) yıkımıyla devasa miktarda üre açığa çıkar ve böbrek tübüllerine biner.

Sağlıklı bir süt çocuğunda inek sütü verildiğinde böbrek maksimum konsantrasyon kapasitesini zorlayarak bu yükü telafi edebilir. Ancak araya ateşli bir enfeksiyon, ishal, kusma veya aşırı sıcak hava girdiğinde; akciğer ve deriden buharlaşma kayıpları artar. Bu durumda inek sütü alan bebek, yüksek solüt yükünü idrarla atabilmek için zorunlu su kaybetmeye devam eder ve serbest su hızla tükenir. Sonuç; kan sodyumunun 150 mEq/L'nin üzerine fırladığı, intrasellüler dehidratasyon, beyin kanaması ve kalıcı nörolojik hasarla seyreden ölümcül 'Hipernatremik Dehidratasyon' tablosudur. Anne sütü, düşük osmolaritesi ve düşük RSL düzeyi sayesinde bebeğin serbest su rezervini koruyan doğal bir emniyet kemeridir.""",
    [
        {"type": "clinical", "badge": "🔴 HİPERNATREMİK DEHİDRATASYON RİSKİ", "text": "İnek sütü yüksek protein ve elektrolit içeriğiyle renal solüt yükünü 3 kat artırır; ishal ve ateşte serbest su hızla tükenerek hipernatremik dehidratasyon gelişir.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Anne sütünün osmolaritesi 286 mOsm/kg iken inek sütünün osmolaritesi yaklaşık 400 mOsm/kg'dır. Anne sütü sodyum ve potasyumu inek sütünün 1/3'ü kadardır.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-012",
        "question": "Süt çocuğu beslenmesinde Renal Solüt Yükü (RSL) ve osmolarite kavramları ile ilgili aşağıdaki klinik değerlendirmelerden hangisi yanlıştır?",
        "options": [
            "A) Anne sütünün osmolaritesi yaklaşık 286 mOsm/kg olup plazma ile izo-ozmolardır.",
            "B) İnek sütünün potansiyel renal solüt yükü anne sütünün yaklaşık 3 katıdır.",
            "C) İnek sütündeki sodyum ve potasyum miktarı anne sütündekinin yaklaşık 3 katı düzeyindedir.",
            "D) Süt çocuğunun böbreği idrarı 1400 mOsm/kg düzeyine kadar konsantre edebildiği için inek sütünün solüt yükü dehidratasyon riski yaratmaz.",
            "E) Gastroenterit geçiren ve inek sütüyle beslenen bir bebekte artan zorunlu su kaybı hipernatremik dehidratasyona yol açabilir."
        ],
        "answer": "D) Süt çocuğunun böbreği idrarı 1400 mOsm/kg düzeyine kadar konsantre edebildiği için inek sütünün solüt yükü dehidratasyon riski yaratmaz.",
        "explanation": "Süt çocuğunun böbrek konsantrasyon kapasitesi erişkin (1200-1400 mOsm/kg) düzeyinde değildir; maksimum 600-700 mOsm/kg'dır. Bu nedenle inek sütünün yüksek solüt yükünü atabilmek için çok fazla zorunlu su harcar ve akut hastalıklarda hızla dehidrate olur."
    }
))

# ==============================================================================
# SLAYT 13: Anne Sütünün İmmünolojik Mimarisi: Hücresel ve Sıvısal Savunma Faktörleri
# ==============================================================================
slides.append(make_slide(
    13,
    "Anne Sütünün İmmünolojik Mimarisi: Hücresel ve Sıvısal Savunma Faktörleri",
    "Sekretuvar IgA (sIgA), Laktoferrin, Lizozim, Lökositler ve Enteromammarik Dolaşım",
    """Anne sütü basit bir besin solüsyonu değil; antienflamatuar, antimikrobiyal ve immünomodülatör faktörlerle donatılmış aktif, canlı bir immünolojik dokudur. Sıvısal (hümoral) savunmanın amiral gemisi SEKRETUVAR IgA'dır (sIgA). sIgA dimerik yapıda olup, meme epitelinden geçerken kazandığı 'sekretuvar komponent' sayesinde bebeğin mide asidine ve bağırsaktaki proteolitik enzimlere karşı tam dirençlidir. sIgA sistemik dolaşıma emilmez; bebek bağırsak mukozasını koruyucu bir zırh gibi sıvayarak patojen bakteri ve virüslerin epitel hücrelerine tutunmasını (adhezyonunu) mekanik olarak engeller ve onları nötralize eder ('immün dışlama' / immune exclusion).

Anne sütündeki sIgA'nın antijenik özgüllüğü olağanüstü bir biyolojik mekanizma olan 'Enteromammarik ve Bronkomammarik Dolaşım' ile belirlenir: Annenin bağırsak mukozasındaki Peyer plaklarında veya solunum yolunda bir patojenle (ör. Rotavirüs, Salmonella, Grip virüsü) karşılaşan B lenfositler uyarılır. Bu uyarılmış B lenfositler mezenterik lenf nodları ve duktus torasikus yoluyla sistemik kana geçer ve hedefe yönelik olarak meme bezine göç ederler. Meme dokusunda plazma hücresine dönüşerek doğrudan o patojene özgül sIgA salgılarlar. Böylece anne, kendi çevresinde maruz kaldığı enfeksiyon etkenlerine karşı sütü aracılığıyla bebeğine spesifik hazır antikor kalkanı sunar.

İmmün sistemin diğer güçlü biyokimyasal silahları Laktoferrin ve Lizozimdir:
• **Laktoferrin:** Demir bağlayıcı bir glikoproteindir. Bağırsak lümenindeki serbest demir iyonlarını (Fe3+) olağanüstü yüksek afiniteyle bağlayarak demire bağımlı bakterilerin (*E. coli*, *Klebsiella*, *Pseudomonas*, mantarlar) çoğalmasını durdurur (bakteriyostatik etki). Aynı zamanda doğrudan bakteri membranını parçalayarak bakterisidal etki de gösterir.
• **Lizozim:** Gram-pozitif bakterilerin hücre duvarındaki peptidoglikan bağlarını yıkar; laktoferrin ile güçlü bir sinerji içinde çalışır.
• **Hücresel Faktörler:** Kolostrumda mL başına milyonlarca canlı maternal lökosit (%80-90 makrofaj, %10 nötrofil ve lenfosit) bulunur. Bu hücreler fagositoz yapar, sitokin ve interferon salgılayarak bebeğin mukozal bağışıklığını bizzat destekler.""",
    [
        {"type": "clinical", "badge": "🔴 ENTEROMAMMARİK HALKA", "text": "Annenin bağırsağında antijenle karşılaşan B lenfositler meme bezine göç ederek o patojene özgül sIgA üretir; anne sütü bebeğe hedefe yönelik hazır antikor sağlar.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Sekretuvar IgA sekretuvar komponenti sayesinde proteolitik sindirime dirençlidir; bağırsak mukozasında immün dışlama yaparak enfeksiyonları önler.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-013",
        "question": "Anne sütünün immünolojik bileşenleri ve etki mekanizmaları ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            "A) Sekretuvar IgA içerdiği sekretuvar komponent sayesinde mide asidi ve proteolitik enzimler tarafından parçalanmaz.",
            "B) Enteromammarik dolaşım sayesinde annenin bağırsak florasındaki patojenlere karşı özgül sIgA antikorları anne sütüne geçer.",
            "C) Laktoferrin serbest demiri bağlayarak demire bağımlı bakterilerin çoğalmasını engelleyen bakteriyostatik bir proteindir.",
            "D) Lizozim bakterilerin hücre duvarındaki peptidoglikan tabakasını parçalayarak antibakteriyel etkinlik gösterir.",
            "E) Sekretuvar IgA bebek tarafından hızla emilerek sistemik kan dolaşımına geçer ve fetal IgG düzeylerini artırır."
        ],
        "answer": "E) Sekretuvar IgA bebek tarafından hızla emilerek sistemik kan dolaşımına geçer ve fetal IgG düzeylerini artırır.",
        "explanation": "Sekretuvar IgA sistemik dolaşıma EMİLMEZ. Bağırsak lümeninde ve mukozal yüzeyde kalarak patojenlerin mukozaya yapışmasını (adhezyonunu) engeller (immün dışlama). Sistemik korumayı sağlayan antikor ise fetal dönemde plasentadan geçen maternal IgG'dir."
    }
))

# ==============================================================================
# SLAYT 14: İnsan Sütü Oligosakkaritleri (HMO), Prebiyotikler ve Mikrobiyota Kurulumu
# ==============================================================================
slides.append(make_slide(
    14,
    "İnsan Sütü Oligosakkaritleri (HMO), Prebiyotikler ve Mikrobiyota Kurulumu",
    "Patojen Tuzakları (Decoy Receptors), Bifidobacterium infantis Kolonizasyonu ve İmmün Tolerans",
    """İnsan Sütü Oligosakkaritleri (Human Milk Oligosaccharides - HMO); anne sütünde laktoz ve yağlardan sonra en yüksek konsantrasyonda bulunan üçüncü büyük katı bileşendir (litrede yaklaşık 5-15 gram). HMO'lar son derece kompleks, fukozillenmiş ve siyalillenmiş glikan polimerleridir. Evrimsel ve biyolojik açıdan en büyüleyici gerçek şudur: Yenidoğan bebek HMO'ları sindirebilecek hiçbir gastrointestinal enzime sahip değildir! Anne sütü bu devasa biyosentez enerjisini bebeğin dokularını beslemek için değil; bebeğin mikrobiyotasını kurmak ve patojenleri tuzağa düşürmek için harcar.

HMO'lar mideden ve ince bağırsaktan sindirilmeden geçerek kolona ulaşır. Burada yararlı kommensal bakteri olan *Bifidobacterium infantis* (ve *B. bifidum*) için son derece seçici bir besin (prebiyotik) substratı görevi görür. Patojen bakteriler HMO'ları fermente edemezken, *B. infantis* HMO'ları tüketerek ortama bol miktarda Kısa Zincirli Yağ Asitleri (SCFA; özellikle asetat, propiyonat, bütirat) ve laktat salgılar. Bu metabolitler kolon pH'sını düşürür (pH ~5.0-5.5), enterik patojenlerin (*E. coli*, *Clostridium difficile*, *Salmonella*) kolonizasyonunu engeller, bağırsak epitelinde sıkı bağlantı (tight junction) proteinlerinin sentezini uyararak bağırsak geçirgenliğini kapatır ve prematürelerde Nekrotizan Enterokolit (NEK) riskini dramatik olarak azaltır.

HMO'ların ikinci mucizevi savunma mekanizması 'Yalancı Reseptör / Patojen Tuzağı' (Decoy Receptor / Soluble Receptor Analogue) fonksiyonudur. Bağırsak mukozasını istila etmek isteyen birçok patojen virüs, bakteri ve toksin (ör. Rotavirüs, Norovirüs, *Campylobacter jejuni*, *Streptococcus pneumoniae*, *Entamoeba histolytica*); epitel hücresinin yüzeyindeki glikan reseptörlerine tutunmak zorundadır. HMO molekülleri, bu epitel reseptörlerinin üç boyutlu moleküler ikizidir! Patojenler epitel yerine lümende serbest dolaşan HMO'lara bağlanır; patojen tuzağa düşürülerek mukozaya tutunamadan dışkıyla atılır. Ayrıca az miktarda dolaşıma emilen HMO'lar lökositlerin endotelyal adezyonunu düzenleyerek sistemik anti-enflamatuar etki oluşturur.""",
    [
        {"type": "clinical", "badge": "🔴 PREBİYOTİK ETKİ VE NEK'TEN KORUNMA", "text": "HMO'lar Bifidobacterium infantis'i seçici olarak besleyerek bağırsak pH'sını düşürür ve prematürelerde Nekrotizan Enterokolit (NEK) gelişimini önler.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "HMO'lar patojenlerin epitele bağlanmasını engelleyen 'yalancı reseptör' (decoy receptor) görevi görerek Rotavirüs ve Campylobacter gibi etkenleri nötralize eder.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-014",
        "question": "İnsan sütü oligosakkaritlerinin (HMO) biyolojik özellikleri ve etki mekanizmaları ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            "A) Anne sütünde laktoz ve yağdan sonra konsantrasyonu en yüksek üçüncü katı bileşendir.",
            "B) Bebek tarafından pankreatik enzimlerle hidrolize edilerek temel glukoz kaynağı olarak emilir.",
            "C) Bifidobacterium infantis için seçici prebiyotik substrat görevi görerek bağırsak florasını düzenler.",
            "D) Bağırsak epitelindeki reseptörleri taklit eden 'yalancı reseptör' (decoy) etkisiyle patojenlerin mukozaya yapışmasını engeller.",
            "E) Ürettikleri kısa zincirli yağ asitleri sayesinde kolon pH'sını asidik tutarak patojen kolonizasyonunu baskılar."
        ],
        "answer": "B) Bebek tarafından pankreatik enzimlerle hidrolize edilerek temel glukoz kaynağı olarak emilir.",
        "explanation": "HMO'lar bebek tarafından SİNDİRİLEMEZ. Bebekte bunları parçalayacak enzim yoktur. Sindirilmeden kolona geçer ve orada yararlı bakterileri (Bifidobakteriler) besler ve patojenleri tuzağa düşürür."
    }
))

# ==============================================================================
# SLAYT 15: Emzirme Nöroendokrinolojisi: Prolaktin ve Oksitosin Refleksleri
# ==============================================================================
slides.append(make_slide(
    15,
    "Emzirme Nöroendokrinolojisi: Prolaktin ve Oksitosin Refleksleri",
    "Süt Yapım Refleksi, Süt Boşalma (Let-Down) Refleksi, FIL ve Emzirme Başarısı",
    """Başarılı bir laktasyon süreci, anne ile bebek arasında işleyen iki kusursuz nöroendokrin refleks yayına dayanır:
1. **Süt Üretim Refleksi (Prolaktin Refleksi):** Ön hipofizden yönetilir.
2. **Süt Boşalma / Fışkırtma Refleksi (Oksitosin / Let-Down Refleksi):** Arka hipofizden yönetilir.
Bebeğin meme ucunu ve areolayı kavramasıyla buradaki dokunma duyusu reseptörleri mekanik olarak uyarılır. Sinirsel impulslar interkostal sinirler ve spinal kord üzerinden hipotalamusa ulaşarak bu iki refleksi senkronize biçimde aktive eder.

Prolaktin, ön hipofizin laktotrof hücrelerinden salgılanır ve meme alveollerindeki glandüler sekretuvar epitel hücrelerini uyararak sütün biyosentezini sağlar. Prolaktin salgısı emzirme sırasında kanda yükselir, ancak kandaki pik seviyesine emzirme bittikten yaklaşık 30-40 dakika sonra ulaşır. Bu biyolojik gecikme çok derin bir anlam taşır: Prolaktin o anki emzirmenin değil, 'BİR SONRAKİ EMZİRMENİN SÜTÜNÜ' üretir! Prolaktin salınımı sirkadiyen ritim gösterir ve geceleri gündüze göre belirgin şekilde daha yüksektir. Bu nedenle geceleri yapılan emzirmeler, sütün devamlılığı ve laktasyon amenoresinin (doğal kontraseptif etki) sürdürülmesi için elzemdir.

Oksitosin ise hipotalamusun supraoptik ve paraventriküler nükleuslarında sentezlenip arka hipofizden dolaşıma salınır. Oksitosin alveollerin ve duktusların etrafını bir sepet gibi saran myoepitelyal hücreleri kastırır. Kasılmayla alveollerdeki süt laktifer duktuslara ve subareolar sinüslere doğru basınçla fışkırtılır; buna 'süt inme (let-down) veya süt fışkırtma refleksi' denir. Oksitosin psikolojik duruma son derece duyarlıdır: Annenin bebeğini düşünmesi, koklaması, ağlamasını duyması refleksi başlatabilirken; ağrı, anksiyete, stres, utanma ve şüphe sempatoadrenal sistem aktivasyonuyla oksitosin salgısını anında bloke ederek sütün memede hapsolmasına yol açar. Oksitosin aynı zamanda myometriyumu kasarak lohusalıkta uterus involüsyonunu hızlandırır ve postpartum kanamayı önler. Memede süt kaldığında ise süte geçen 'FIL' (Feedback Inhibitor of Lactation) proteini otokrin olarak süt yapımını baskılar; bu nedenle süt yapımını artırmanın tek yolu memeyi sık ve tam boşaltmaktır.""",
    [
        {"type": "clinical", "badge": "🔴 OKSİTOSİN VE STRES İLİŞKİSİ", "text": "Stres ve ağrı oksitosin refleksini bloke ederek sütün dışarı fışkırmasını engeller. Anneye huzurlu ortam ve güven sağlamak süt boşalmasını çözer.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Prolaktin ön hipofizden salgılanıp süt sentezini sağlar (gece salgısı daha yüksektir); Oksitosin arka hipofizden salgılanıp myoepitelyal hücreleri kasarak sütü fışkırtır (let-down).", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-015",
        "question": "Laktasyon nöroendokrinolojisi ve emzirme refleksleri ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            "A) Prolaktin ön hipofizden salgılanır ve meme alveollerinde süt sentezini uyarır.",
            "B) Prolaktin düzeyi emzirme sonrasında pik yaparak bir sonraki emzirmenin sütünü hazırlar.",
            "C) Oksitosin arka hipofizden salgılanarak alveol çevresindeki myoepitelyal hücreleri kasar ve sütü fışkırtır.",
            "D) Oksitosin refleksi annenin ağrı, stres ve endişe duyması durumunda inhibe olur.",
            "E) Prolaktin hormonu gündüz saatlerinde en yüksek seviyeye ulaştığı için gündüz emzirmeleri geceye göre süt yapımında daha etkilidir."
        ],
        "answer": "E) Prolaktin hormonu gündüz saatlerinde en yüksek seviyeye ulaştığı için gündüz emzirmeleri geceye göre süt yapımında daha etkilidir.",
        "explanation": "Prolaktin hormonu sirkadiyen ritim gereği GECELERİ en yüksek seviyededir. Gece emzirmeleri süt yapımının sürdürülmesi ve prolaktin düzeylerinin korunması açısından gündüze göre çok daha kritiktir."
    }
))

# ==============================================================================
# SLAYT 16: Klinik Emzirme Yönetimi: Doğru Teknik, Meme Sorunları ve Saklama Kuralları
# ==============================================================================
slides.append(make_slide(
    16,
    "Klinik Emzirme Yönetimi: Doğru Teknik, Meme Sorunları ve Saklama Kuralları",
    "Latch-on Kriterleri, Meme Başı Çatlakları, Mastit Yönetimi ve '3-3-3 Kuralı'",
    """Emzirme başarısızlıklarının ve erken sütten kesmenin en sık nedeni süt azlığı değil, yanlış emzirme tekniği ve sonucunda gelişen meme komplikasyonlarıdır. Doğru kavrama (latch-on) kriterleri şunlardır:
• Bebeğin ağzı 130-140 derece geniş açılmış olmalıdır.
• Alt dudak dışa doğru tamamen kıvrılmış ('balık dudağı' görünümü) olmalıdır.
• Bebeğin çenesi memeye dayanmış veya gömülmüş olmalıdır.
• Yanaklar dolgun olmalı, emme sırasında içe çökmemeli ve şapırtı sesi çıkmamalıdır (yutkunma sesi duyulmalıdır).
• Areolanın büyük kısmı (özellikle alt yarısı) bebeğin ağzında olmalıdır.
Bebek sadece meme ucunu (meme başını) emdiğinde; meme başı sert damağa sürtünerek travmatize olur, kanamalı ağrılı çatlaklar (fissürler) gelişir ve süt sinüsleri sıkılamadığı için meme boşalamaz.

Süt stazı (angurjman / meme dolgunluğu) tedavi edilmezse enfeksiyöz mastite ilerler. Mastit; memede lokalize eritem, ısı artışı, şiddetli ağrı, ateş (>38.5°C) ve halsizlik ile karakterizedir (en sık etken *Staphylococcus aureus*). Mastit yönetiminde yapılan EN BÜYÜK YANLIŞ emzirmeyi kesmektir! Emzirme ve memenin boşaltılması mastit tedavisinin birincil basamağıdır. Anneye antibiyotik (penisilinaz dirençli penisilinler veya 1. kuşak sefalosporinler) ve analjezik verilse dahi her iki memeden emzirmeye kesintisiz devam edilmelidir; sütün bebeğe hiçbir zararı yoktur.

Sağılmış anne sütünün saklanmasında klinik pratik altın kural '3-3-3 Kuralı'dır:
• Oda sıcaklığında (22-26°C): 3 saat (temiz/serin koşullarda 4-6 saat)
• Buzdolabının iç raflarında (+4°C): 3 gün (asla kapakta değil, iç rafta)
• Derin dondurucuda (-18°C): 3 ay
Saklanan anne sütü asla mikrodalga fırında veya doğrudan ocak üzerinde ısıtılmaz! Mikrodalga sütün içinde 'sıcak cepler' oluşturarak bebeğin ağzını yakabilir ve koruyucu immünoglobulinleri/enzimleri tahrip eder. Süt, ılık su dolu bir kap içine oturtularak (benmari usulü) çözdürülmeli ve hafifçe çalkalanarak homojenize edilmelidir.""",
    [
        {"type": "clinical", "badge": "🔴 MASTİTTE EMZİRME DEVAMI", "text": "Mastit veya meme absesi geliştiğinde emzirmeye KESİNLİKLE ara verilmez! Memenin boşaltılması tedavinin temelidir, antibiyotik altında emzirme sürdürülür.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Sağılmış anne sütü saklama kuralı (3-3-3): Oda ısısında 3 saat, buzdolabında (+4°C) 3 gün, derin dondurucuda (-18°C) 3 ay saklanabilir.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-016",
        "question": "Doğumdan sonraki 3. haftada sağ memesinde şiddetli ağrı, kızarıklık, sertlik ve 38.8°C ateş şikayetiyle başvuran ve klinik olarak akut puerperal mastit tanısı konulan emziren bir anneye yaklaşımda aşağıdakilerden hangisi yanlıştır?",
        "options": [
            "A) Uygun antibiyotik ve analjezik tedavi başlanmalıdır.",
            "B) Bebeğin enfekte memeden emzirilmesine derhal son verilmeli ve o meme kurutulmalıdır.",
            "C) Memedeki süt stazını gidermek için sık emzirme ve gerekirse sağma uygulanmalıdır.",
            "D) Emzirme pozisyonu ve kavrama (latch-on) tekniği değerlendirilip düzeltilmelidir.",
            "E) Sağılan anne sütü derin dondurucuda (-18°C) 3 aya kadar saklanabilir."
        ],
        "answer": "B) Bebeğin enfekte memeden emzirilmesine derhal son verilmeli ve o meme kurutulmalıdır.",
        "explanation": "Mastit tedavisinde en kritik basamak memenin boşaltılmasıdır. Emzirmenin kesilmesi süt stazını artırarak tabloyu meme absesine ilerletir. Anne uygun antibiyotik alırken bebeğini enfekte memeden de güvenle emzirmeye devam etmelidir."
    }
))

# ==============================================================================
# SLAYT 17: Emzirmenin Kontrendikasyonları: Kesin Engeller ve Yanlış Bilinen Mitler
# ==============================================================================
slides.append(make_slide(
    17,
    "Emzirmenin Kontrendikasyonları: Kesin Engeller ve Yanlış Bilinen Mitler",
    "Klasik Galaktozemi, HIV, Sitotoksik İlaçlar vs. Hepatit B/C, CMV, Mastit Gerçeği",
    """Anne sütünün sağladığı emsalsiz tıbbi ve immünolojik yararlar nedeniyle, emzirmeyi kesin olarak yasaklayan durumlar tıpta son derece sınırlıdır. Kontrendikasyonlar bebek kaynaklı ve anne kaynaklı olarak ayrılır:
• **Bebek Kaynaklı TEK KESİN Kontrendikasyon:** KLASİK GALAKTOZEMİ'dir (galaktoz-1-fosfat üridiltransferaz enzim eksikliği). Anne sütündeki laktoz bağırsakta glukoz ve galaktoza hidrolize edildiğinden; galaktoz birikimi bebekte katarakt, siroz, karaciğer yetmezliği, letarji ve neonatal sepsise (özellikle *E. coli*) yol açar. Bu bebeklere kesinlikle soya bazlı/galaktozsuz özel formül mama verilmelidir. (Not: Fenilketonüride anne sütü tamamen yasak değildir; kan fenilalanin düzeyi izlenerek özel fenilalaninsiz mama ile anne sütü kombine edilir).

Anne Kaynaklı Kesin/Mutlak Kontrendikasyonlar:
1. **Anne HIV Pozitifliği:** Gelişmiş ülkelerde ve temiz suya/formül mamaya güvenli erişimin olduğu toplumlarda emzirme KESİNTİSİZ KONTRENDİKEDİR (vertikal bulaş riski %15-20). Ancak temiz suyun bulunmadığı, bebeklerin enfeksiyöz ishalden öldüğü az gelişmiş ülkelerde DSÖ antiretroviral tedavi eşliğinde emzirmeyi önermektedir.
2. **HTLV-1 ve HTLV-2 Enfeksiyonları:** Viral bulaş ve lenfoma/miyelopati riski nedeniyle emzirme yasaktır.
3. **Kanser Kemoterapisi ve Radyoaktif İzotoplar:** Antimetabolitler, alkilleyici ajanlar ve nükleer tıp izotopları süte geçtiğinden laktasyon durdurulur (radyoaktif maddelerde izotop klerensine kadar geçici kontrendikasyon).
4. **Anne Madde/Uyuşturucu Bağımlılığı:** Kokain, eroin, amfetamin gibi maddelerin kullanımı.
5. **Aktif ve Tedavisiz Tüberküloz:** Annede açık tüberküloz varsa bulaşma süt yoluyla değil solunum damlacıklarıyladır. Bu nedenle anne ile bebek arasındaki doğrudan temas kesilir; ANCAK süte basil geçmediği için anne tedavi alırken sütü sağılarak bebeğe güvenle verilebilir! Tedavinin 2. haftasından sonra balgam negatifleşince bebek doğrudan memeye verilebilir.

EMZİRMEYE KESİNLİKLE ENGEL OLMAYAN DURUMLAR (Yanlış Mitler):
• **Hepatit B:** Bebeğe doğumdan sonraki ilk 12 saat içinde Hepatit B aşısı ve Hepatit B immünglobulini (HBIG) yapıldıktan sonra anne güvenle emzirebilir.
• **Hepatit C:** Meme başında açık/kanamalı fissür olmadığı sürece emzirmeye engel değildir.
• **CMV Enfeksiyonu:** Term doğan sağlıklı bebeklerde emzirme kontrendike değildir (sadece çok düşük doğum ağırlıklı prematürelerde süt dondurulup verilebilir).
• **Mastit veya Meme Absesi:** Drene edilerek emzirmeye devam edilir.
• **Annenin Basit Ateşli Enfeksiyonları:** Soğuk algınlığı, grip, gastroenteritte hijyen önlemleriyle emzirilir; anne sütünün antikorları bebeği korur.""",
    [
        {"type": "clinical", "badge": "🔴 BEBEKTE TEK KESİN KONTRENDİKASYON", "text": "Klasik Galaktozemi anne sütünün bebek kaynaklı TEK kesin kontrendikasyonudur; fenilketonüride ise anne sütü kontrollü verilebilir.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Hepatit B taşıyıcısı anne; bebeğe doğumda aşı ve HBIG yapıldıktan sonra güvenle emzirebilir, emzirme KONTRENDİKE DEĞİLDİR.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-017",
        "question": "Anne sütü ile beslenme ve emzirmenin kontrendikasyonları ile ilgili aşağıdaki klinik eşleştirmelerden hangisi yanlıştır?",
        "options": [
            "A) Klasik Galaktozemi - Bebek için kesin emzirme kontrendikasyonudur.",
            "B) Gelişmiş ülkelerde anne HIV pozitifliği - Kesin emzirme kontrendikasyonudur.",
            "C) Annede HBsAg pozitifliği (Hepatit B) - Doğumda bebeğe aşı ve HBIG yapılsa dahi kesin emzirme kontrendikasyonudur.",
            "D) Anneye radyoaktif iyot-131 tedavisi uygulanması - Geçici emzirme kontrendikasyonudur.",
            "E) Aktif balgam pozitif tüberkülozlu anne - Doğrudan temas kesilir ancak sağılmış anne sütü bebeğe verilebilir."
        ],
        "answer": "C) Annede HBsAg pozitifliği (Hepatit B) - Doğumda bebeğe aşı ve HBIG yapılsa dahi kesin emzirme kontrendikasyonudur.",
        "explanation": "Hepatit B enfeksiyonu emzirme kontrendikasyonu DEĞİLDİR. Doğumdan sonraki ilk 12 saat içinde bebeğe Hepatit B aşısı ve Hepatit B hiperimmün globulini (HBIG) yapıldığı takdirde anne bebeğini güvenle emzirebilir."
    }
))

# ==============================================================================
# SLAYT 18: Tamamlayıcı Beslenme (Ek Gıda): Fizyolojik Gerekçeler ve 6. Ay Eşiği
# ==============================================================================
slides.append(make_slide(
    18,
    "Tamamlayıcı Beslenme (Ek Gıda): Fizyolojik Gerekçeler ve 6. Ay Eşiği",
    "Besin Boşluğu (Energy Gap), Çiğneme Refleksinin Gelişimi ve Erken Başlamanın Riskleri",
    """'Tamamlayıcı Beslenme'; anne sütünün tek başına süt çocuğunun artan besin ögesi ve enerji gereksinimlerini karşılamaya yetmediği dönemde, anne sütüne ilave olarak diğer katı ve sıvı besinlerin diyete kademeli olarak dahil edilmesi sürecidir. Dünya Sağlık Örgütü (DSÖ), Amerikan Pediatri Akademisi (AAP) ve ESPGHAN, tamamlayıcı besinlere 'TAM 6. AYIN BİTİMİNDE' (180. günde) başlanmasını kesin bir dille önermektedir. Yaşamın ilk 6 ayında anne sütü bebeğin gereksinimlerinin %100'ünü tek başına karşılarken; 6-12. aylarda bu oran %50'ye, 12-24. aylarda ise %30'a geriler. Aradaki bu fark 'Besin ve Enerji Boşluğu' (Nutrient Gap) olarak tanımlanır.

Altıncı ayda tamamlayıcı beslenmeye geçilmesini zorunlu kılan fizyolojik gerekçeler şunlardır:
1. **Mikrobesin Açığı:** Fetal demir ve çinko depoları 6. ay civarında tamamen tükenir; anne sütündeki konsantrasyonlar hızlı büyüyen vücut kitlesine yetersiz kalır.
2. **Nöromotor Olgunlaşma:** 6. ayda bebek başını dik tutabilir, destekle oturabilir, nesneleri eliyle kavrayıp ağzına götürebilir.
3. **Ekstrüzyon Refleksinin Kaybolması:** İlk aylarda dilde bulunan 'dışarı itme refleksi' (katı bir nesne konduğunda dilin onu dışarı fırlatması) 4-6. aylarda kaybolur; yerini çiğneme, dili arkaya doğru yuvarlama ve yutma koordinasyonuna bırakır. Ek gıdaya 7-8. aylardan sonraya gecikilirse çiğneme tembelliği, pütürlü gıdaları reddetme ve anoreksi gelişir.

Peki neden 6. aydan önce (özellikle 4 aydan önce) ek gıda verilmemelidir?
• Gastrointestinal enzimler (pankreatik amilaz ve lipaz) henüz immatürdür, malabsorpsiyon gelişir.
• İntestinal mukozal bariyer immatürdür; sıkı bağlantılar gevşek olduğundan yabancı gıda proteinleri kana geçerek gıda alerjilerini tetikler.
• Böbreğin solüt konsantrasyon yeteneği düşüktür; gereksiz solüt yükü bebeği dehidratasyona sürükler.
• Ek besinler tokluk hissi yaratarak bebeğin memeyi emmesini azaltır; meme boşalmadığı için anne sütü üretimi hızla geriler ve bebek anne sütünün benzersiz koruyuculuğunu kaybeder.""",
    [
        {"type": "clinical", "badge": "🔴 EKSTRÜZYON REFLEKSİNİN KAYBI", "text": "Dilin katı gıdayı dışarı itme refleksi (ekstrüzyon) 4-6. aylarda kaybolur; baş kontrolü ve destekli oturma ile birlikte 6. ayda ek gıdaya geçişi mümkün kılar.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Tamamlayıcı beslenmeye tam 6. ayın bitiminde (180. gün) başlanmalıdır; ilk 6 ayda anne sütü ihtiyacın %100'ünü, 6-12 ayda %50'sini, 12-24 ayda %30'unu karşılar.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-018",
        "question": "Tamamlayıcı beslenmeye (ek gıdalara) geçiş zamanlaması ve fizyolojik gerekçeleri ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            "A) Tamamlayıcı beslenmeye tam 6. ayın bitiminde (180. günde) başlanması önerilir.",
            "B) Altıncı aydan sonra demir ve çinko depolarının tükenmesi ek gıdaya başlanmasının en önemli gerekçelerindendir.",
            "C) İlk aylarda güçlü olan dilin dışarı itme (ekstrüzyon) refleksi 4-6. aylarda zayıflayarak kaybolur.",
            "D) 4 aydan önce ek gıdalara başlanması bağırsak mukozal geçirgenliğinin yüksek olması nedeniyle alerji riskini artırır.",
            "E) Anne sütü 6-12. aylar arasında bebeğin enerji gereksiniminin %90'ını tek başına karşılamayı sürdürür."
        ],
        "answer": "E) Anne sütü 6-12. aylar arasında bebeğin enerji gereksiniminin %90'ını tek başına karşılamayı sürdürür.",
        "explanation": "Anne sütü ilk 6 ayda gereksinimin %100'ünü karşılarken, 6-12. aylar arasında bu oran %50'ye, 12. aydan sonra ise %30'a düşer. Kalan açık tamamlayıcı besinlerle kapatılmalıdır."
    }
))

# ==============================================================================
# SLAYT 19: Tamamlayıcı Besinlerin Seçimi ve Uygulama Protokolü
# ==============================================================================
slides.append(make_slide(
    19,
    "Tamamlayıcı Besinlerin Seçimi ve Uygulama Protokolü",
    "İlk Besinler (Yoğurt, Sebze, Meyve), Kıyma Eklenmesi ve '3 Gün Bekleme Kuralı'",
    """Tamamlayıcı besinlere geçiş bir beslenme devrimidir ve katı klinik kurallarla yönetilmelidir. Başlangıçta besinler tek bileşenli, yumuşak kıvamda, hipoalerjenik ve sindirimi kolay olmalıdır. Türkiye'de ve dünyada ilk başlanacak ideal gıdalar:
1. **Ev Yapımı Taze Yoğurt:** Laktik asit fermantasyonu sayesinde laktozu düşüktür, sindirimi kolaydır, kalsiyum biyoyararlanımı mükemmeldir ve probiyotik içeriğiyle bağırsak florasını güçlendirir.
2. **Sebze Püreleri:** Havuç, patates, bal kabağı, kabak gibi alerji potansiyeli düşük sebzeler buharda haşlanıp zeytinyağı eklenerek püre yapılır. Tuz KESİNLİKLE eklenmez.
3. **Meyve Püreleri:** Elma, şeftali, armut gibi meyveler cam rendede hazırlanarak C vitamini ve lif sağlar.

Klinik pratikte besin alerjilerini ve intoleransları ayırt edebilmek için '3 Gün Bekleme Kuralı' esastır. Her yeni besin tek başına, başlangıçta 1-2 tatlı kaşığı gibi küçük miktarlarda, sabah veya öğle öğününde verilir ve 3 gün boyunca diyete başka hiçbir yeni besin eklenmez. Bu süre zarfında bebekte perioral kızarıklık, ürtiker, egzama alevlenmesi, kusma, mukuslu/kanlı ishal veya aşırı huzursuzluk gelişip gelişmediği gözlenir. Reaksiyon yoksa o besin güvenli kabul edilir ve bir sonraki yeni besine geçilir.

Besinlerin tolere edilmesinin ardından 7. aydan itibaren sebze pürelerinin içine MUTLAKA çift çekilmiş kuzu kıyması (demir ve çinko kaynağı) eklenmelidir. 8. aydan itibaren iyice pişmiş yumurta sarısı (1/8 ile başlanıp artırılarak), baklagiller ve kılçıksız balık diyete dahil edilir. ÇOK KRİTİK KURAL: Besinler ASLA blenderdan geçirilip pütürsüz sıvı çorba kıvamında verilmemelidir! Blender alışkanlığı oromotor çiğneme refleksini köreltir ve bebek 1 yaşında dahi pütürlü gıda yiyemez hale gelir. Besinler çatal arkasıyla ezilerek pütürlü kıvamda sunulmalı, 8-9. aylarda 'parmak besinler' (finger foods) ile bebeğin kendi kendine beslenmesi desteklenmelidir.""",
    [
        {"type": "clinical", "badge": "🔴 BLENDER KULLANIMI YASAĞI", "text": "Ek gıdalar blenderdan geçirilmemeli, çatal arkasıyla ezilerek pütürlü verilmelidir; aksi halde çiğneme refleksi gelişemez ve gıda reddi oluşur.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Her yeni ek gıda tek başına, 3 gün arayla (3 gün kuralı) başlanarak olası besin alerjileri ve intoleranslar izlenmelidir.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-019",
        "question": "Altıncı ayını dolduran sağlıklı bir süt çocuğunda tamamlayıcı besinlere başlama ilkeleri ile ilgili aşağıdaki önerilerden hangisi yanlıştır?",
        "options": [
            "A) Yeni başlanan her gıda tek başına verilmeli ve alerji takibi için aralarında en az 3 gün beklenmelidir.",
            "B) Başlangıçta yoğurt, sebze püresi ve meyve püresi gibi sindirimi kolay besinler tercih edilmelidir.",
            "C) Çiğneme becerisinin gelişmesi için besinler blenderdan geçirilerek tamamen pürüzsüz sıvı hale getirilmelidir.",
            "D) 7. aydan itibaren sebze pürelerine demir ve çinko desteği sağlamak amacıyla çift çekilmiş kıyma eklenmelidir.",
            "E) Bebeklerin kendi kendine beslenmesini desteklemek amacıyla 8-9. aylarda parmak besinler sunulabilir."
        ],
        "answer": "C) Çiğneme becerisinin gelişmesi için besinler blenderdan geçirilerek tamamen pürüzsüz sıvı hale getirilmelidir.",
        "explanation": "Besinlerin blenderdan geçirilerek tamamen pürüzsüz yapılması çiğneme refleksinin gelişimini engeller ve ileriki aylarda pütürlü gıdaların reddine yol açar. Besinler çatal arkasıyla ezilerek pütürlü kıvamda sunulmalıdır."
    }
))

# ==============================================================================
# SLAYT 20: Süt Çocuğunda Bir Yaş Altı Yasak Besinler ve Klinik Riskleri
# ==============================================================================
slides.append(make_slide(
    20,
    "Süt Çocuğunda Bir Yaş Altı Yasak Besinler ve Klinik Riskleri",
    "Bal (İnfant Botulizmi), İnek Sütü (Gizli Kanama), Tuz, Şeker ve Boğulma Tehlikeleri",
    """Tamamlayıcı beslenme döneminde bazı gıdalar vardır ki, bir yaşından önce bebeğe verilmesi doğrudan toksik, organ hasarı yapıcı veya ölümcül sonuçlar doğurabilir. Hekimin bu yasak gıdaları aileye gerekçeleriyle anlatması hayati bir sorumluluktur.

1. **BAL ve Pastörize Edilmemiş Mısır Şurubu:** Bir yaşından önce KESİNLİKLE YASAKTIR. Bal, toprak kaynaklı *Clostridium botulinum* sporları içerebilir. Erişkin bağırsak florası ve asit ortamı bu sporların çimlenmesini engellerken; süt çocuğunun immatür florasında sporlar vejetatif bakteriye dönüşerek ölümcül nörotoksin salgılar. Bu durum 'İnfant Botulizmi'ne yol açar. Tablo; inatçı kabızlık, emme zayıflığı, pitozis, baş kontrolünün kaybı, jeneralize hipotoni ('gevşek bebek' / floppy infant tablosu) ve solunum arresti ile seyreder.
2. **İNEK SÜTÜ (İçecek Olarak):** Bir yaşından önce içecek olarak inek sütü verilmesi kesinlikle yasaktır (yoğurt ve peynir gibi fermente ürünler serbesttir). İnek sütü verildiğinde: (a) Bağırsak mukozasında mikroanjiyopatik hasar oluşturarak dışkıyla gizli kan kaybına ve dirençli demir eksikliği anemisine yol açar, (b) Yüksek kazein ve kalsiyum içeriğiyle demir emilimini bloke eder, (c) Aşırı protein ve sodyum içeriğiyle immatür böbreği yüksek renal solüt yükü altında bırakır.
3. **TUZ ve ŞEKER:** Bir yaşına kadar yemeklere asla tuz eklenmemelidir; bebeğin böbrekleri tuzu atamaz ve ileriki yaşlarda esansiyel hipertansiyon eşiği düşer. Şeker ise tat duyusunu bozar, obezite ve erken diş çürüklerine zemin hazırlar.
4. **YUMURTA BEYAZI:** Yüksek alerjenitesi (ovalbumin) nedeniyle geleneksel olarak 1 yaşından sonraya bırakılır; yumurta sarısı ise 8. ayda başlanabilir.
5. **BAKLA:** Glukoz-6-fosfat dehidrogenaz (G6PD) enzim eksikliği olan bebeklerde akut intravasküler hemolize (favizm krizine) neden olabileceğinden 1 yaş öncesi verilmez.
6. **SERT, YUVARLAK KATI BESİNLER:** Bütün fındık, fıstık, ceviz, leblebi, bütün üzüm, zeytin, yuvarlak kesilmiş sosis; trakeobronşiyal aspirasyon ve mekanik asfiksiye bağlı ani çocuk ölümlerinin en sık nedenidir; 1 yaş altında ezilmeden bütün halde verilmesi kesinlikle yasaktır.""",
    [
        {"type": "clinical", "badge": "🔴 İNFANT BOTULİZMİ VE BAL YASAĞI", "text": "Bal Clostridium botulinum sporları içerir; 1 yaşından küçüklerde 'gevşek bebek', pitozis ve solunum arrestiyle seyreden infant botulizmine yol açar.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "İnek sütünün 1 yaşından önce içecek olarak verilmesi; bağırsaktan gizli kan kaybı, demir eksikliği anemisi ve aşırı renal solüt yükü nedeniyle KONTRENDİKEDİR.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-020",
        "question": "Dokuz aylık bir bebeğin beslenme öyküsünde büyükannesi tarafından öksürüğü geçsin diye günde iki tatlı kaşığı bal verildiği ve kahvaltılarda sulandırılmış inek sütü içirildiği öğreniliyor. Bu uygulamaların bebekte yol açabileceği klinik riskler ile ilgili aşağıdaki eşleştirmelerden hangisi doğrudur?",
        "options": [
            "A) Bal - İnfant Botulizmi (Hipotoni ve solunum arresti) / İnek Sütü - İntestinal gizli kanama ve demir eksikliği anemisi",
            "B) Bal - Hiperkalsemi / İnek Sütü - Laktoz fazlalığına bağlı hipoglisemi",
            "C) Bal - Çölyak hastalığı / İnek Sütü - K vitamini toksisitesi",
            "D) Bal - Skorbüt hastalığı / İnek Sütü - Favizm krizi",
            "E) Bal - Renal tübüler asidoz / İnek Sütü - Hiperkalemiye bağlı aritmi"
        ],
        "answer": "A) Bal - İnfant Botulizmi (Hipotoni ve solunum arresti) / İnek Sütü - İntestinal gizli kanama ve demir eksikliği anemisi",
        "explanation": "Bal Clostridium botulinum sporları içerdiği için 1 yaş altında infant botulizmi (gevşek bebek sendromu) riski taşır. İnek sütü ise mukozal mikrovasküler hasarla gizli kan kaybına, demir emilim bozukluğuna ve ağır demir eksikliği anemisine yol açar."
    }
))

# ==============================================================================
# SLAYT 21: Protein-Enerji Malnütrisyonu (PEM): Tanım, Epidemiyoloji ve Sınıflamalar
# ==============================================================================
slides.append(make_slide(
    21,
    "Protein-Enerji Malnütrisyonu (PEM): Tanım, Epidemiyoloji ve Sınıflamalar",
    "Gomez, Waterlow ve DSÖ Z-Skoru Sınıflamaları; Bodurluk (Stunting) vs. Çelimsizlik (Wasting)",
    """Protein-Enerji Malnütrisyonu (PEM); vücudun fizyolojik fonksiyonlarını sürdürebilmesi ve büyümesi için gereken protein, enerji ve mikrobesinlerin yetersiz alımı veya emilim bozukluğu sonucu ortaya çıkan, hücresel düzeyden organ sistemlerine kadar yayılan patolojik bir tablodur. Gelişmekte olan ülkelerde çocuk morbidite ve mortalitesinin bir numaralı arka plan nedenidir. Malnütrisyonun ciddiyetini, süresini ve tipini belirlemek amacıyla çeşitli klinik ve antropometrik sınıflamalar geliştirilmiştir.

Tarihsel ve klinik sınıflamalar:
1. **Gomez Sınıflaması:** Bebeğin mevcut ağırlığının yaşa göre standart medyan ağırlığa oranına dayanır:
   • %90-110: Normal
   • %75-89: 1. Derece (Hafif) Malnütrisyon
   • %60-74: 2. Derece (Orta) Malnütrisyon
   • <%60: 3. Derece (Ağır) Malnütrisyon (Nutrisyonel ödem varlığında ağırlıktan bağımsız direkt 3. derece kabul edilir).
2. **Waterlow Sınıflaması:** Malnütrisyonun süresini ve kronikliğini ayırmada kullanılır:
   • **Boya Göre Ağırlık (Wasting / Zayıflık / Çelimsizlik):** AKUT malnütrisyonu yansıtır. Mevcut ağırlığın o boydaki medyan ağırlığa oranıdır.
   • **Yaşa Göre Boy (Stunting / Bodurluk / Cücelik):** KRONİK malnütrisyonu yansıtır. Geçmişten gelen uzun süreli beslenme yetersizliğinin ve büyüme duraklamasının göstergesidir.

GÜNCEL DSÖ ANTROPOMETRİK STANDARTLARI (Z-SKORLARI):
DSÖ büyüme standartlarında çocuğun ölçümleri referans popülasyon medyanından standart sapma (SD) uzaklığıyla ifade edilir:
• **Akut Malnütrisyon (Wasting / Çelimsizlik):** Boya göre ağırlık (WHZ) <-2 SD ise akut malnütrisyon; <-3 SD ise 'Ağır Akut Malnütrisyon' (SAM - Severe Acute Malnutrition) denir.
• **Kronik Malnütrisyon (Stunting / Bodurluk):** Yaşa göre boy (HAZ) <-2 SD ise bodurluk; <-3 SD ise ağır bodurluktur.
• **Düşük Kilo (Underweight):** Yaşa göre ağırlık (WAZ) <-2 SD'dir.
• **Ödemli Malnütrisyon Kuralı:** İki taraflı pretibial nutrisyonel ödem varlığı, antropometrik ölçüm ve Z-skorundan bağımsız olarak hastayı doğrudan 'Ağır Akut Malnütrisyon' sınıfına sokar!""",
    [
        {"type": "clinical", "badge": "🔴 ÖDEMLİ MALNÜTRİSYON KURALI", "text": "İki taraflı pretibial nutrisyonel ödem varlığı, tartı ve boy ölçümlerinden bağımsız olarak hastayı doğrudan 'Ağır Akut Malnütrisyon' (SAM) kabul ettirir.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Waterlow sınıflamasına göre 'Boya göre ağırlık' AKUT malnütrisyonu (wasting); 'Yaşa göre boy' ise KRONİK malnütrisyonu (stunting) gösterir.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-021",
        "question": "Süt çocuğu ve çocukluk çağı malnütrisyonunun antropometrik sınıflamaları ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
        "options": [
            "A) Waterlow sınıflamasında 'yaşa göre boy' düşüklüğü kronik malnütrisyonu (bodurluk / stunting) gösterir.",
            "B) Waterlow sınıflamasında 'boya göre ağırlık' düşüklüğü akut malnütrisyonu (çelimsizlik / wasting) gösterir.",
            "C) Gomez sınıflamasında yaşa göre ağırlığı referans değerin %60'ının altında olan çocuk ağır (3. derece) malnütrisyon grubundadır.",
            "D) DSÖ kriterlerine göre boya göre ağırlık Z-skoru <-3 SD olan veya nutrisyonel ödemi bulunan çocuk Ağır Akut Malnütrisyon (SAM) kabul edilir.",
            "E) Pretibial ödemi olan bir çocukta boya göre ağırlık Z-skoru normal sınırlarda ise hasta malnütrisyon olarak sınıflandırılamaz."
        ],
        "answer": "E) Pretibial ödemi olan bir çocukta boya göre ağırlık Z-skoru normal sınırlarda ise hasta malnütrisyon olarak sınıflandırılamaz.",
        "explanation": "Nutrisyonel ödem varlığı, tartı veya Z-skoru ne olursa olsun hastayı doğrudan en ağır malnütrisyon grubu olan 'Ağır Akut Malnütrisyon' (Kwashiorkor) sınıfına sokar. Ödem vücut ağırlığını yapay olarak artırabilir."
    }
))

# ==============================================================================
# SLAYT 22: Şiddetli Kalori Yetersizliği: Marasmus Kliniği ve Patofizyolojisi
# ==============================================================================
slides.append(make_slide(
    22,
    "Şiddetli Kalori Yetersizliği: Marasmus Kliniği ve Patofizyolojisi",
    "Deri Altı Yağ ve Kas Erimesi, 'İhtiyar Adam Yüzü', Torba Pantolon Belirtisi ve Adaptasyon",
    """Marasmus (Kuru Malnütrisyon); hem enerjinin (total kalorinin) hem de proteinin ileri derecede ve dengeli yetersizliği sonucu ortaya çıkan ağır malnütrisyon tablosudur. Tipik olarak yaşamın ilk 1 yılında (<1 yaş), anne sütünün çok erken kesildiği, aşırı sulandırılmış unlu mamalarla veya mikroplarla kontamine sulandırılmış biberon mamalarıyla beslenen, tekrarlayan gastroenterit ve enfeksiyon atakları geçiren bebeklerde görülür. Marasmusta organizma tam bir 'açlık adaptasyonu' (maraton koşucusu metabolizması) sergiler; glukoneojenez, lipoliz ve kas proteolizi devrededir.

Klinik görünüm adeta 'bir deri bir kemik' tablosudur. En karakteristik patolojik bulgular:
• **Deri Altı Yağ Dokusunun Tamamen Kaybı:** Vücutta yağ dokusu en son yanaklardaki emme yağ yastıkçıklarından (Bichat yağ yastığı) kaybolur. Bichat yastıkçıkları da eridiğinde yanaklar çöker, elmacık kemikleri fırlar ve hastaya karakteristik 'İhtiyar Adam Yüzü' (Senil Fasies) görünümünü verir.
• **Ağır Kas Atrofisi:** İskelet kasları enerji üretmek amacıyla tamamen eritilmiştir. Deri elastikiyetini kaybederek incelir; özellikle gluteal bölgede ve uyluklarda sarkarak bol bir pantolon görünümü alır ('Torba Pantolon' / Baggy Pants belirtisi).
• **Kemik Çıkıntıları ve Karın:** Kaburgalar tek tek sayılır, kostosternal bileşkeler belirgindir. Karın genellikle çekiktir (skafoid karın) veya karın kaslarının zayıflığına ve meteorizme bağlı bombe olabilir.

Marasmusun patofizyolojik ve laboratuvar ayırt edici özellikleri:
• **ÖDEM KESİNLİKLE YOKTUR!**
• Hepatomegali (karaciğer yağlanması) görülmez; karaciğer boyutları normal veya küçülmüştür.
• Serum albümini ve total protein düzeyleri normal sınırlardadır veya sadece hafifçe düşüktür (çünkü karaciğer parçalanan kas amino asitleriyle albümin sentezini sürdürebilir).
• İştah genellikle açıktır; çocuk açtır, huzursuzdur, çevresine karşı dikkatli ve uyanıktır. Bazal metabolizma hızı, kalp atım hacmi ve vücut sıcaklığı düşüktür; hipotermi ve hipoglisemiye karşı son derece duyarlıdırlar.""",
    [
        {"type": "clinical", "badge": "🔴 MARASMUSUN KLİNİK İMZALARI", "text": "Marasmusta ödem YOKTUR! Bichat yağ dokusu erimesiyle 'İhtiyar Adam Yüzü' ve uyluk derisinde sarkmayla 'Torba Pantolon' görünümü tipiktir.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Marasmusta total kalori eksikliği vardır; kas erimesi ve deri altı yağ kaybı aşırıdır, serum albümini genellikle normaldir ve ödem KESİNLİKLE bulunmaz.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-022",
        "question": "Sekiz aylık bir bebek; aşırı zayıflık ve kilo alamama şikayetiyle getiriliyor. Fizik muayenede deri altı yağ dokusunun tamamen kaybolduğu, yanakların çöktüğü ve 'ihtiyar adam yüzü' görünümü olduğu, uyluk derisinin bol bir pantolon gibi sarktığı, belirgin kas atrofisi bulunduğu ancak pretibial ödemin OLMADIĞI saptanıyor. Laboratuvarında serum albümini 3.6 g/dL (normal) ölçülen ve iştahının açık olduğu gözlenen bu bebek için en olası tanı aşağıdakilerden hangisidir?",
        "options": [
            "A) Kwashiorkor",
            "B) Marasmus",
            "C) Çölyak Krizi",
            "D) Kistik Fibrozis",
            "E) Konjenital Nefrotik Sendrom"
        ],
        "answer": "B) Marasmus",
        "explanation": "Deri altı yağ dokusunun ve Bichat yastıkçıklarının erimesi ('ihtiyar adam yüzü'), kas atrofisi, 'torba pantolon' görünümü, normal serum albümini, iştahın açık olması ve en önemlisi ÖDEMİN OLMAMASI klasik Marasmus (kuru malnütrisyon) tablosudur."
    }
))

# ==============================================================================
# SLAYT 23: Islak Malnütrisyon: Kwashiorkor Kliniği ve Patofizyolojisi
# ==============================================================================
slides.append(make_slide(
    23,
    "İleri Protein Yetersizliği: Kwashiorkor Kliniği ve Patofizyolojisi",
    "Nutrisyonel Ödem, Hipoalbüminemi, Yağlı Karaciğer, 'Pullu Boya Dermatozu' ve Bayrak Belirtisi",
    """Kwashiorkor (Islak Malnütrisyon); Batı Afrika Ga dilinde 'yeni bir bebek doğduğunda tahttan indirilen, memeden kesilen çocuğun hastalığı' anlamına gelir. Tipik olarak 1-3 yaş grubunda; yeni bir kardeşin doğumuyla aniden anne sütünden kesilen ve protein içeriği yok denecek kadar az fakat kalorisi yüksek nişastalı, şekerli veya tahıllı (mısır, manyok, pirinç lapası) diyetle beslenen çocuklarda görülür. Diyetle karbonhidrat alındığı için plazma insülin düzeyi yüksek kalır; insülin kas proteolizini ve lipolizi baskılar. Bu durum karaciğer için serbest amino asit havuzunu tamamen kurutur ve karaciğerin protein sentez fabrikasını çökertir.

Patofizyolojinin merkezinde derin HİPOALBÜMİNEMİ (<2.5 g/dL, sıklıkla <1.5 g/dL) yer alır. Plazma onkotik basıncının çökmesiyle damar içi sıvı interstisyel dokuya sızar ve jeneralize ÖDEM gelişir. Ödem önce ayak sırtında ve pretibial bölgede başlar, periorbital dokuya yayılarak 'Ay Dede Yüzü' (Moon Face) tablosunu oluşturur ve asite kadar ilerler. İkinci kritik bulgu HEPATOMEGALİ (Yağlı Karaciğer)dir: Karbonhidratlar karaciğerde yağa dönüştürülür; ancak bu yağları karaciğerden perifere taşıyacak olan apolipoproteinler (özellikle VLDL) sentezlenemediği için trigliseritler hepatositler içinde hapsolur ve karaciğer ileri derecede yağlanarak büyür.

Kwashiorkorun diğer çarpıcı klinik bulguları:
1. **Deri Lezyonları ('Pullu Boya / Dökülen Boya Dermatozu' - Flaky-Paint Dermatosis):** Basınç ve sürtünme gören kalça ve bacaklarda deride hiperpigmentasyon, çatlaklar, soyulmalar ve açık ülserasyonlar gelişir.
2. **Saç Değişiklikleri ('Bayrak Belirtisi' - Flag Sign):** Saçlar incelir, kurur, kolayca dökülür ve kızıllaşır (bakır rengi alır). Yetersiz beslenme ile iyi beslenme dönemlerinin ardışık izini taşıyan açık ve koyu renkli saç bantlaşmalarına 'Bayrak Belirtisi' denir.
3. **Mental Değişiklikler ve Anoreksi:** Marasmusun aksine çocuk son derece apatik, letarjik, mutsuz ve çevreye tamamen ilgisizdir; sürekli sızlanır ve ŞİDDETLİ ANOREKSİ (iştahsızlık) mevcuttur. Marasmik-Kwashiorkor ise hem şiddetli kas erimesinin hem de ödemin bir arada bulunduğu en ölümcül tablodur.""",
    [
        {"type": "clinical", "badge": "🔴 KWASHİORKORUN PATOGNOMONİK BULGULARI", "text": "Hipoalbüminemiye bağlı ÖDEM, karaciğerde apolipoprotein yetersizliğine bağlı HEPATOMEGALİ ve 'Pullu Boya Dermatozu' Kwashiorkor'un temel triadıdır.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Kwashiorkorda karaciğer yağlanmasının (hepatomegali) temel nedeni, trigliseritleri taşıyacak apolipoproteinlerin (VLDL) yetersiz sentezlenmesidir.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-023",
        "question": "İki yaşında bir çocuk; annesinin yeni doğum yapması üzerine sütten kesilmiş ve sadece mısır ve nişasta lapası ile beslenmiştir. Fizik muayenede iki taraflı pretibial gode bırakan ödem, yüzde 'ay dede' görünümü, karında asit, belirgin hepatomegali, uyluklarda pul pul dökülen hiperpigmente lezyonlar ('pullu boya dermatozu') ve saçlarında açık-koyu renk bantlaşması saptanıyor. Laboratuvarında serum albümini 1.8 g/dL saptanan bu çocukta hepatomegalinin temel patofizyolojik nedeni aşağıdakilerden hangisidir?",
        "options": [
            "A) Karaciğerde aşırı glikojen depolanması",
            "B) Apolipoprotein sentez yetersizliğine bağlı olarak trigliseritlerin VLDL şeklinde karaciğerden atılamaması",
            "C) Safra asidi sentezinin aşırı artması",
            "D) Hepatik ven trombozu (Budd-Chiari sendromu)",
            "E) Karaciğerde aşırı demir birikimi (Hemokromatozis)"
        ],
        "answer": "B) Apolipoprotein sentez yetersizliğine bağlı olarak trigliseritlerin VLDL şeklinde karaciğerden atılamaması",
        "explanation": "Kwashiorkorda seçici protein eksikliği nedeniyle karaciğerde apolipoprotein sentezi durur. Karbonhidrattan sentezlenen yağlar (trigliseritler) VLDL haline getirilip kana verilemez; hepatositlerde birikerek ağır yağlı karaciğer ve hepatomegaliye yol açar."
    }
))

# ==============================================================================
# SLAYT 24: Ağır Malnütrisyonda Kritik Yönetim İlkeleri ve Refeeding Sendromu Riski
# ==============================================================================
slides.append(make_slide(
    24,
    "Ağır Malnütrisyonda Kritik Yönetim İlkeleri ve Refeeding Sendromu Riski",
    "DSÖ Protokolü: Stabilizasyon, Rehabilitasyon, F-75/F-100 ve Ölümcül Hatalar",
    """Ağır akut malnütrisyonlu (SAM) bir çocuk standart bir açlık hastası gibi tedavi edilemez. Bu çocuklarda hücresel düzeyde 'Redüktif Adaptasyon' (küçülerek hayatta kalma) gelişmiştir: Na+/K+ ATPaz pompaları yavaşlamış, hücre içi potasyum ve magnezyum boşalmış, hücre içine sodyum ve su dolmuştur. Karaciğer, pankreas ve böbrek fonksiyonları minimum kapasiteyle çalışır, kalp kası atrofiktir. Bu kırılgan dengeye yapılacak kontrolsüz bir müdahale (hızlı IV sıvı veya yüksek protein/tuz verilmesi) kalp yetmezliği ve ani ölümle sonuçlanır.

DSÖ Yönetim Protokolü iki ana faza ayrılır:
1. **Stabilizasyon Fazı (1-7. Gün):** Amaç yaşamı tehdit eden acil metabolik komplikasyonları çözmektir:
   • Hipoglisemi (<54 mg/dL) ve Hipotermi (<35.5°C) derhal tedavi edilir ve önlenir.
   • Dehidratasyon tedavisinde ASLA standart IV sıvılar verilmez! Oral rehidratasyon için düşük sodyumlu, yüksek potasyumlu özel solüsyon olan ReSoMal kullanılır.
   • Elektrolit imbalansı düzeltilir: Potasyum (3-4 mmol/kg/gün) ve Magnezyum (0.4-0.6 mmol/kg/gün) eklenir; sodyum kısıtlanır.
   • İmmün sistem çöktüğü için ateş olmasa dahi TÜM HASTALARA rutin geniş spektrumlu antibiyotik başlanır.
   • Beslenmeye düşük protein ve düşük laktozlu özel formül olan F-75 (75 kcal/100 mL, 0.9 g protein/100 mL) ile çok sık aralıklarla (2 saatte bir) başlanır.
2. **Rehabilitasyon Fazı (2-6. Hafta):** Ödem çözüldüğünde ve iştah geri geldiğinde hasta F-100 formülüne (100 kcal/100 mL, 2.9 g protein/100 mL) veya RUTF'ye (Kullanıma Hazır Terapötik Besin) geçirilerek hızlı kilo alımı (catch-up growth) hedeflenir.

ÖLÜMCÜL HATALAR VE REFEEDING (YENİDEN BESLEME) SENDROMU:
• **Stabilizasyon Fazında ASLA DEMİR VERİLMEZ!** Malnütrisyonlu çocukta transferrin düzeyi düşüktür; verilen demir serbest kalarak bakteriyel proliferasyonu patlatır ve serbest oksijen radikalleriyle fatal septik şoka yol açar. Demir tedavisi yalnızca rehabilitasyon fazında kilo alımı başladığında eklenir!
• **Refeeding Sendromu:** Uzun süreli açlıktan sonra aniden yüksek kalorili/karbonhidratlı beslenme verilirse; kanda hızla fırlayan insülin, zaten tükenmiş olan serum potasyumu, magnezyumu ve özellikle FOSFATI hücre içine sokar. Sonuç: Derin hipofosfatemi, ATP tükenmesi, aritmiler, konjestif kalp yetmezliği, solunum kas felci ve ölümdür.""",
    [
        {"type": "clinical", "badge": "🔴 STABİLİZASYONDA DEMİR YASAĞI", "text": "Ağır malnütrisyonun ilk basamağında (stabilizasyon) ASLA demir verilmez! Serbest demir enfeksiyonu alevlendirir ve ölümcül septik şoka yol açar.", "color": "rose"},
        {"type": "exam", "badge": "🔵 ÇIKMIŞ SORU SPOTU", "text": "Refeeding sendromunun temel biyokimyasal belirteci ani insülin deşarjına bağlı gelişen HİPOFOSFATEMİ'dir; ATP tükenmesi ve kardiyak arreste yol açar.", "color": "sky"}
    ],
    {
        "id": "prac-bebek-beslenme-024",
        "question": "Ağır akut malnütrisyon (SAM) tanısıyla hastaneye yatırılan bir süt çocuğunun ilk hafta (stabilizasyon fazı) yönetiminde aşağıdaki uygulamalardan hangisi KESİNLİKLE YAPILMAMALIDIR?",
        "options": [
            "A) Hipoglisemiyi önlemek amacıyla sık aralıklarla düşük proteinli F-75 diyeti ile beslenmesi",
            "B) Dehidratasyon tedavisinde düşük sodyumlu, yüksek potasyumlu ReSoMal solüsyonunun kullanılması",
            "C) Enfeksiyon bulgusu olmasa dahi geniş spektrumlu antibiyotik başlanması",
            "D) Derin anemiyi düzeltmek amacıyla oral yüksek doz elemental demir tedavisi başlanması",
            "E) Hipotermiyi önlemek için çocuğun sıcak tutulması ve kanguru bakımı uygulanması"
        ],
        "answer": "D) Derin anemiyi düzeltmek amacıyla oral yüksek doz elemental demir tedavisi başlanması",
        "explanation": "Ağır malnütrisyonun stabilizasyon fazında KESİNLİKLE DEMİR VERİLMEZ. Transferrin azlığı nedeniyle serbest kalan demir serbest radikal hasarına, enfeksiyonların alevlenmesine ve fatal septik şoka yol açar. Demir tedavisi yalnızca rehabilitasyon fazında kilo alımı başladıktan sonra verilir."
    }
))

deck_data = {
    "deckId": "learn-bebek-beslenmesi",
    "title": "Bebek Beslenmesi, Anne Sütü İmmünolojisi, Tamamlayıcı Beslenme ve Malnütrisyon",
    "slides": slides
}

# 1. Scratch JSON dosyasına UTF-8 olarak kaydet
with open(SCRATCH_PATH, 'w', encoding='utf-8') as f:
    json.dump(deck_data, f, ensure_ascii=False, indent=2)

print(f"[OK] 24 slayt başarıyla üretildi ve kaydedildi: {SCRATCH_PATH}")

# 2. interactive_learning_decks.json dosyasına da ekle veya güncelle
if os.path.exists(DECKS_JSON_PATH):
    with open(DECKS_JSON_PATH, 'r', encoding='utf-8') as f:
        existing_decks = json.load(f)
    
    # Mevcut deck var mı kontrol et
    updated = False
    for i, d in enumerate(existing_decks):
        if d.get('deckId') == 'learn-bebek-beslenmesi':
            existing_decks[i] = deck_data
            updated = True
            break
    
    if not updated:
        existing_decks.append(deck_data)
        print(f"[OK] Yeni deck interactive_learning_decks.json listesine eklendi.")
    else:
        print(f"[OK] Mevcut deck interactive_learning_decks.json içinde güncellendi.")
        
    with open(DECKS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(existing_decks, f, ensure_ascii=False, indent=2)
    print(f"[OK] {DECKS_JSON_PATH} başarıyla güncellendi. Toplam deck sayısı: {len(existing_decks)}")
