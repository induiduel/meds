# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec5():
    slides = []

    # Slide 41: Bakteriüri Tanımı ve Suprapubik Aspirasyon Kuralı
    s41_narrative = (
        "Üriner sistem enfeksiyonunun laboratuvar tanısında idrarda saptanan mikroorganizma "
        "miktarı ve örneğin alınış yöntemi kritik bir standardizasyon gerektirir.\n\n"
        "- **Bakteriüri Tanımı:** Bakteriüri, idrarda belli bir kantitatif seviyenin üzerinde "
        "bakteri bulunması (**anlamlı bakteriüri**) olarak tanımlanır.\n"
        "- **Kontaminasyon Riski:** Doğal yolla alınan idrar örnekleri üretra ve genital floradan "
        "kontamine olabileceğinden eşik değerler (koloni sayıları) aranır.\n"
        "- **Steril Koşul İstisnası:** Ancak steril koşullarda doğrudan mesaneden alınan idrarda "
        "(**suprapubik aspirasyon**) saptanan **herhangi bir üreme anlamlıdır** ve enfeksiyon kanıtıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Bakteriüri idrarda belli seviyenin üzerinde bakteri olmasıdır; steril koşullarda alınan idrarda (suprapubik aspirasyon) HERHANGİ BİR ÜREME anlamlı kabul edilir."
    )
    s41_bullets = [
        "Bakteriüri: İdrarda belli bir seviyenin üzerinde bakteri olmasıdır (anlamlı bakteriüri).",
        "Orta akım idrarında kontaminasyonu ayırt etmek için sayısal eşikler kullanılır.",
        "Suprapubik aspirasyonla steril koşulda alınan idrarda herhangi bir üreme anlamlıdır."
    ]
    s41_elements = [
        make_cloze("Steril koşullarda alınan idrarda (suprapubik aspirasyon) saptanan herhangi bir üreme anlamlı kabul edilir.", "herhangi bir üreme", "Tek bir koloni dahi olsa tanı koyduran üreme kuralı"),
        make_table("Örnek Alma Yöntemine Göre Bakteriüri Anlamı", ["Örnek Alma Tekniği", "Flora Teması", "Anlamlılık Kriteri"], [
            {"cells": [{"text": "Orta Akım İdrarı", "isMasked": False}, {"text": "Üretral flora teması mevcut", "isMasked": True, "hint": "üretra çevresinden geçiş"}, {"text": "Belli seviyenin üzerinde (anlamlı) üreme"}]},
            {"cells": [{"text": "Suprapubik Aspirasyon", "isMasked": False}, {"text": "Sıfır flora teması (tam steril)", "isMasked": False}, {"text": "Herhangi bir üreme (≥1 KOB)", "isMasked": True, "hint": "en ufak bakteri üremesi"}]}
        ]),
        make_chain("Bakteriüri Tanı Mantığı", [
            "1. İdrar Alma: Suprapubik aspirasyonla mesaneye girilmesi.",
            "2. Tam Sterilite: Üretra ve introitus florasının tamamen baypas edilmesi.",
            "3. Ekim ve İnkübasyon: Besiyerinde koloni aranması.",
            "4. Tanı: Tek bir koloni dahi çıksa anlamlı bakteriüri kabul edilmesi."
        ]),
        make_recall("Suprapubik aspirasyonla steril koşullarda alınan idrar örneğinde bakteriüri için anlamlılık eşiği nedir?", "Herhangi bir üreme (tek bir bakteri/koloni dahi) anlamlı kabul edilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bakteriüri Tanımı", [
            {"text": "Bakteriüri idrarda belli bir seviyenin üzerinde bakteri bulunmasıdır.", "isLie": False, "explanation": "Doğru. Genel tanımdır."},
            {"text": "Suprapubik aspirasyonla alınan idrarda herhangi bir üreme anlamlıdır.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "Suprapubik aspirasyonda 100 milyon bakteri ürese bile hepsi normal flora kabul edilir.", "isLie": True, "explanation": "Tuzak! Suprapubik aspirasyon tamamen sterildir, herhangi bir üreme derhal patolojik ve anlamlı kabul edilir."},
            {"text": "Steril koşullarda alınan örneklerde kontaminasyon riski en aza iner.", "isLie": False, "explanation": "Doğru. Altın standarttır."}
        ]),
        make_quiz("İdrarda bakteriüri tanısı ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Steril koşullarda alınan idrarda (suprapubik aspirasyon) herhangi bir üreme anlamlıdır", "isCorrect": True, "explanation": "Ders notunda 'steril koşullarda alınan idrarda (suprapubik aspirasyon) herhangi bir üreme anlamlıdır' denmektedir."},
            {"key": "B", "text": "Suprapubik aspirasyonda en az 10 milyar koloni olmadan tanı konulamaz", "isCorrect": False, "explanation": "Herhangi bir üreme yeterlidir."},
            {"key": "C", "text": "Bakteriüri idrarda sadece lökosit bulunması anlamına gelir", "isCorrect": False, "explanation": "Lökosit piyüridir, bakteri varlığı bakteriüridir."},
            {"key": "D", "text": "Normal insanlarda suprapubik mesane idrarı her zaman bakterilerle doludur", "isCorrect": False, "explanation": "Normal mesane idrarı sterildir."}
        ])
    ]
    slides.append(make_slide(41, "Bakteriüri Tanımı ve Suprapubik Aspirasyon", "Bakteriüri kavramı, steril koşullarda örnekleme ve tanısal eşik kuralları", "Tanımlar", s41_narrative, s41_bullets, s41_elements))

    # Slide 42: Piyüri Tanımı: Santrifüjsüz İdrar Örneği (≥10/mm³)
    s42_narrative = (
        "Piyüri, üriner traktusta gelişen enflamatuar reaksiyonun ve konak doku hasarının "
        "idrardaki en objektif hücresel göstergesidir.\n\n"
        "- **Piyüri Tanımı:** Piyüri, idrarda belli bir kantitatif seviyenin üzerinde lökosit bulunmasıdır.\n"
        "- **Santrifüjsüz İdrar Ölçümü:** Hemositometrik sayım kamarasıyla incelenen **santrifüj edilmemiş "
        "örnekte milimetreküpte 10 veya daha fazla (≥10/mm³) lökosit** saptanması piyüri olarak kabul edilir.\n"
        "- **Klinik Değeri:** Santrifüjsüz direkt sayım, hücrelerin santrifüj gücüyle parçalanmasını "
        "ve yoğunluk değişkenliğini ortadan kaldırdığı için en güvenilir kantitatif yöntemdir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Santrifüj edilmemiş idrar örneğinde piyüri tanı eşiği: ≥10 lökosit/mm³ bulunmasıdır."
    )
    s42_bullets = [
        "Piyüri: İdrarda belli bir seviyenin üzerinde lökosit bulunmasıdır.",
        "Santrifüj edilmemiş örnekte eşik değer: ≥10/mm³ lökosit.",
        "Hemositometrik lökosit sayımı piyüri için en objektif standart ölçümdür."
    ]
    s42_elements = [
        make_cloze("Santrifüj edilmemiş idrar örneğinde piyüri tanısı için milimetreküpte en az ≥10/mm³ lökosit saptanmalıdır.", "≥10/mm³", "Santrifüjsüz idrardaki sayısal lökosit eşiği"),
        make_table("Santrifüjsüz İdrarda Piyüri Kriteri", ["İdrar Durumu", "Ölçüm Yöntemi", "Piyüri Tanı Eşiği"], [
            {"cells": [{"text": "Santrifüj Edilmemiş", "isMasked": False}, {"text": "Sayım kamarası (hemositometre)", "isMasked": True, "hint": "hücre sayım odacığı"}, {"text": "≥10/mm³ lökosit"}]},
            {"cells": [{"text": "Klinik Yansıması", "isMasked": False}, {"text": "Ürotelyal enflamatuar yanıt", "isMasked": False}, {"text": "Enflamasyonun doğrulanması", "isMasked": True, "hint": "doku reaksiyonu kanıtı"}]}
        ]),
        make_chain("Santrifüjsüz Piyüri Ölçüm Basamakları", [
            "1. Taze İdrar Temini: Çökeltilmeden ve santrifüj edilmeden alma.",
            "2. Kamaraya Yükleme: Hemositometre sayım odacığına damlatma.",
            "3. Mikroskopik Sayım: Karelerdeki lökositlerin milimetreküpe oranlanması.",
            "4. Eşik Değerlendirmesi: ≥10/mm³ bulunması halinde piyüri kabul edilmesi."
        ]),
        make_recall("Santrifüj edilmemiş idrar örneğinde piyüri tanı eşiği nedir?", "≥10/mm³ (milimetreküpte 10 veya daha fazla lökosit) saptanmasıdır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Santrifüjsüz Piyüri", [
            {"text": "Piyüri idrarda belli bir seviyenin üzerinde lökosit olmasıdır.", "isLie": False, "explanation": "Doğru. Ders notu tanımıdır."},
            {"text": "Santrifüj edilmemiş idrarda ≥10/mm³ lökosit piyüri kabul edilir.", "isLie": False, "explanation": "Doğru. Kesin sayısal eşiktir."},
            {"text": "Santrifüjsüz idrarda piyüri diyebilmek için milimetreküpte en az 100 milyon lökosit gerekir.", "isLie": True, "explanation": "Tuzak! Eşik değer yalnızca ≥10/mm³'tür."},
            {"text": "Piyüri konak dokusundaki enflamasyonu gösterir.", "isLie": False, "explanation": "Doğru. Enflamatuar belirteçtir."}
        ]),
        make_quiz("Santrifüj EDİLMEMİŞ idrar örneğinde piyüri tanısı koyabilmek için milimetreküpte bulunması gereken lökosit sayısı aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "≥10/mm³", "isCorrect": True, "explanation": "Ders notunda açıkça 'santrifüj edilmemiş örnekte ≥10/mm³' olarak belirtilmiştir."},
            {"key": "B", "text": "≥1000/mm³", "isCorrect": False, "explanation": "Çok yüksek bir değerdir."},
            {"key": "C", "text": "≥1/mm³", "isCorrect": False, "explanation": "Eşik değer 10'dur."},
            {"key": "D", "text": "Sıfır", "isCorrect": False, "explanation": "Sıfır lökosit piyüri olmadığını gösterir."}
        ])
    ]
    slides.append(make_slide(42, "Piyüri Tanımı: Santrifüjsüz İdrarda ≥10/mm³", "Piyüri kavramı ve santrifüj edilmemiş idrardaki mikroskopik eşik değer", "Tanımlar", s42_narrative, s42_bullets, s42_elements))

    # Slide 43: Piyüri Tanımı: Santrifüj Edilmiş İdrar Örneği (5-10 Lökosit)
    s43_narrative = (
        "Rutin klinik biyokimya ve mikroskopi laboratuvarlarında en yaygın uygulanan inceleme "
        "yöntemi idrarın santrifüj edilerek sedimentinin incelenmesidir.\n\n"
        "- **Santrifüj Edilmiş İdrar:** Santrifüj edilmiş idrar mikroskopisinde büyük büyütmede (40x objektif) "
        "**her alanda en az 5-10 lökosit** görülmesi piyüri olarak kabul edilir.\n"
        "- **Sediment Değerlendirmesi:** 10-12 mL idrarın standart devirde (yaklaşık 2000-3000 rpm) "
        "çökeltilmesiyle elde edilen dip tortusunda lökosit kümeleri ve parçalanmış nötrofiller incelenir.\n"
        "- **Klinik Önemi:** 5-10 lökosit/saha eşiği, alt veya üst üriner traktusta aktif bir "
        "lökosit göçünün devam ettiğini gösterir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Santrifüj edilmiş idrarda piyüri kriteri: Her alanda en az 5-10 lökosit görülmesidir."
    )
    s43_bullets = [
        "Santrifüj edilmiş idrarda piyüri: Her alanda en az 5-10 lökosit görülmesidir.",
        "İdrar sedimentinin 40x büyük büyütme alanında incelenmesi ile değerlendirilir.",
        "Her alanda ≥5-10 lökosit varlığı aktif ürotelyal enflamasyona işaret eder."
    ]
    s43_elements = [
        make_cloze("Santrifüj edilmiş idrarda büyük büyütmede her alanda en az 5-10 lökosit saptanması piyüri olarak kabul edilir.", "en az 5-10", "Santrifüj edilmiş idrar sedimentindeki büyük büyütme lökosit eşiği"),
        make_table("Piyüri Tanı Kriterleri Karşılaştırması", ["Örnek Türü", "İnceleme Büyütmesi / Tekniği", "Piyüri Eşik Değeri"], [
            {"cells": [{"text": "Santrifüjsüz İdrar", "isMasked": False}, {"text": "Hemositometrik sayım", "isMasked": False}, {"text": "≥10/mm³ lökosit", "isMasked": True, "hint": "milimetreküpte on ve üzeri"}]},
            {"cells": [{"text": "Santrifüj Edilmiş İdrar", "isMasked": False}, {"text": "Büyük büyütme sahası (HPF)", "isMasked": True, "hint": "mikroskop sahası"}, {"text": "Her sahada en az 5-10 lökosit", "isMasked": True, "hint": "beş ila on lökosit"}]}
        ]),
        make_chain("Sediment İnceleme Süreci", [
            "1. Santrifüj: İdrarın santrifüj tüpünde standart devirde çökeltilmesi.",
            "2. Süpernatanın Atılması: Üst sıvının dökülüp dip tortusunun bırakılması.",
            "3. Lam-Lamel Hazırlığı: Sedimentin lam üzerine yayılması.",
            "4. Mikroskopi: Her alanda en az 5-10 lökosit görülerek piyüri tanısı konması."
        ]),
        make_recall("Santrifüj edilmiş idrar sedimentinde piyüri diyebilmek için her alanda kaç lökosit görülmelidir?", "Her sahada (büyük büyütme alanında) en az 5-10 lökosit görülmelidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Santrifüjlü Piyüri", [
            {"text": "Santrifüj edilmiş idrarda her alanda en az 5-10 lökosit piyüri kabul edilir.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "Santrifüjsüz idrarda ise eşik ≥10/mm³'tür.", "isLie": False, "explanation": "Doğru. İki farklı kriter mevcuttur."},
            {"text": "Santrifüj edilmiş idrarda tek bir lökosit görmek için hastanın en az 5 böbreği olması şarttır.", "isLie": True, "explanation": "Tuzak! Santrifüj edilmiş idrarda 5-10 lökosit/saha piyüri eşiğidir, böbrek sayısıyla ilgisi yoktur."},
            {"text": "Lökositler sedimentte tek tek veya kümeler halinde izlenebilir.", "isLie": False, "explanation": "Doğru. Mikroskopik görünümdür."}
        ]),
        make_quiz("Santrifüj EDİLMİŞ idrar sedimentinde mikroskopta her sahada en az kaç lökosit görülmesi piyüri olarak kabul edilir?", [
            {"key": "A", "text": "En az 5-10 lökosit", "isCorrect": True, "explanation": "Ders notunda açıkça 'santrifüj edilmiş idrarda her alanda en az 5-10 lökosit' olarak belirtilmiştir."},
            {"key": "B", "text": "En az 500-1000 lökosit", "isCorrect": False, "explanation": "Çok yüksek bir sayıdır."},
            {"key": "C", "text": "Sadece 1 lökosit", "isCorrect": False, "explanation": "Tek lökosit eşik değer değildir."},
            {"key": "D", "text": "En az 50-100 eritrosit", "isCorrect": False, "explanation": "Eritrosit hematüridir, piyüri lökosittir."}
        ])
    ]
    slides.append(make_slide(43, "Piyüri Tanımı: Santrifüj Edilmiş İdrarda 5-10 Lökosit", "Santrifüjlü idrar sedimenti incelemesi ve her alanda 5-10 lökosit eşiği", "Tanımlar", s43_narrative, s43_bullets, s43_elements))

    # Slide 44: Üriner Sepsis Kavramı ve SOFA Skorlama Sistemi
    s44_narrative = (
        "Üriner sistem enfeksiyonunun lokal doku sınırlarını aşarak sistemik kan dolaşımına ve "
        "uzak organlara yayılması, hayatı tehdit eden ürosepsis tablosunu meydana getirir.\n\n"
        "- **Sepsis Tanımı:** Üriner sistem enfeksiyonu nedeniyle gelişen sepsisin değerlendirilmesinde "
        "uluslararası kılavuzlara uygun olarak **SOFA (sequential organ failure assessment)** skorlaması kullanılır.\n"
        "- **Organ Disfonksiyonu:** Sepsis, enfeksiyona karşı konağın düzensiz immün yanıtı sonucu "
        "ortaya çıkan hayatı tehdit edici organ fonksiyon bozukluğudur.\n"
        "- **SOFA'nın Rolü:** SOFA skoru, yoğun bakım ve yatan hastalarda çoklu organ yetmezliğinin "
        "ağırlığını objektif parametrelerle ölçerek mortalite riskini belirler.\n\n"
        "> [!IMPORTANT]\n"
        "> Üriner sistem enfeksiyonu nedeniyle gelişen sepsisin değerlendirilmesinde SOFA (Sequential Organ Failure Assessment) skorlama sistemi kullanılır."
    )
    s44_bullets = [
        "Üriner sistem enfeksiyonu nedeniyle gelişen sepsiste SOFA skoru kullanılır.",
        "SOFA (Sequential Organ Failure Assessment): Organ yetmezliğini değerlendirir.",
        "Enfeksiyonun hayatı tehdit eden sistemik disfonksiyon aşamasını ölçer."
    ]
    s44_elements = [
        make_cloze("Üriner sistem enfeksiyonu nedeniyle gelişen sepsisin değerlendirilmesinde SOFA skorlama sistemi kullanılır.", "SOFA", "Sıralı organ yetmezliği değerlendirme skorlama sistemi"),
        make_table("Ürosepsis ve SOFA Skorlama Rolü", ["Kavram", "Tanım / Açılım", "Klinik Amacı"], [
            {"cells": [{"text": "Ürosepsis", "isMasked": False}, {"text": "Üriner enfeksiyona bağlı sepsis tablosu", "isMasked": True, "hint": "idrar kaynaklı sistemik sepsis"}, {"text": "Acil parenteral ve yoğun bakım yönetimi"}]},
            {"cells": [{"text": "SOFA Sistemi", "isMasked": False}, {"text": "Sequential Organ Failure Assessment", "isMasked": False}, {"text": "Organ fonksiyon bozukluğunu derecelendirme", "isMasked": True, "hint": "organ yetmezliği puanlaması"}]}
        ]),
        make_chain("Lokal Enfeksiyondan Sepsise Geçiş", [
            "1. Üst ÜSE: Böbrek parankiminde derin invazyon (piyelonefrit).",
            "2. Bakteriyemi: Patojenin veya endotoksinlerin sistemik kana karışması.",
            "3. Sistemik Enflamasyon: Kontrolsüz sitokin fırtınası.",
            "4. SOFA Yükselişi: Çoklu organ yetmezliği ve sepsisin belgelenmesi."
        ]),
        make_recall("Üriner sistem enfeksiyonu nedeniyle gelişen sepsisin değerlendirilmesinde kullanılan skorlama sistemi nedir?", "SOFA (Sequential Organ Failure Assessment) skorlama sistemidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Üriner Sepsis ve SOFA", [
            {"text": "Üriner sistem enfeksiyonu nedeniyle gelişen sepsiste SOFA sistemi kullanılır.", "isLie": False, "explanation": "Doğru. Ders notu ifadesidir."},
            {"text": "SOFA organ disfonksiyonunu objektif olarak değerlendirir.", "isLie": False, "explanation": "Doğru. Skorun temel amacıdır."},
            {"text": "SOFA yalnızca hastanın saç uzunluğunu ölçen bir estetisyen tablosudur.", "isLie": True, "explanation": "Tuzak! SOFA hayati organ yetmezliklerini değerlendiren tıbbi sepsis skorlama sistemidir."},
            {"text": "Ürosepsis hayatı tehdit eden sistemik bir tablodur.", "isLie": False, "explanation": "Doğru. Acil müdahale gerektirir."}
        ]),
        make_quiz("Üriner sistem enfeksiyonu nedeniyle gelişen sepsisin değerlendirilmesinde kullanılan skorlama sistemi aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "SOFA (Sequential Organ Failure Assessment)", "isCorrect": True, "explanation": "Ders notunda 'Üriner sistem enfeksiyonu nedeniyle gelişen sepsis: SOFA skorlama sistemi kullanılır' şeklinde açıkça belirtilmiştir."},
            {"key": "B", "text": "Apgar skoru", "isCorrect": False, "explanation": "Yenidoğan ilk dakika değerlendirmesidir."},
            {"key": "C", "text": "Glasgow-Blatchford skoru", "isCorrect": False, "explanation": "Üst GİS kanama risk skorudur."},
            {"key": "D", "text": "Child-Pugh skoru", "isCorrect": False, "explanation": "Karaciğer sirozu evrelemesidir."}
        ])
    ]
    slides.append(make_slide(44, "Üriner Sepsis Kavramı ve SOFA Skorlaması", "Ürosepsis patolojisi ve Sequential Organ Failure Assessment (SOFA) sistemi", "Sepsis", s44_narrative, s44_bullets, s44_elements))

    # Slide 45: SOFA Bileşenleri: 6 Hayati Organ Sistemi
    s45_narrative = (
        "SOFA skorlama sistemi, sepsis zemininde ortaya çıkan sistemik hasarı değerlendirmek "
        "amacıyla vücudun altı majör organ sistemini eşzamanlı olarak inceler.\n\n"
        "- **Altı Organ Sistemi:** SOFA bileşenleri **solunum, koagülasyon, karaciğer, "
        "kardiyovasküler, santral sinir sistemi ve böbrek**tir.\n"
        "- **Biyokimyasal Parametreler:** Bu sistemler PaO2/FiO2 oranı, trombosit sayısı, serum bilirubin "
        "düzeyi, ortalama arter basıncı/inotrop ihtiyacı, Glaskow koma skalası ve kreatinin/idrar çıkışı ile skorlanır.\n"
        "- **Klinik Eşik:** Enfeksiyon zemininde SOFA skorunda ≥2 puanlık akut artış, sepsis ve artmış "
        "mortalite ile doğrudan ilişkilidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] SOFA skorlamasında değerlendirilen 6 temel organ sistemi: Solunum, koagülasyon, karaciğer, kardiyovasküler, santral sinir sistemi ve böbrektir."
    )
    s45_bullets = [
        "SOFA bileşenleri 6 organ sisteminden oluşur.",
        "Solunum, koagülasyon, karaciğer, kardiyovasküler, santral sinir sistemi, böbrek.",
        "Her organ sistemi için laboratuvar ve klinik parametrelerle 0-4 arası puan verilir."
    ]
    s45_elements = [
        make_cloze("SOFA skorlamasında değerlendirilen 6 organ sistemi solunum, koagülasyon, karaciğer, kardiyovasküler, santral sinir sistemi ve böbrektir.", "kardiyovasküler, santral sinir sistemi ve böbrek", "SOFA'nın son üç majör organ sistemi"),
        make_table("SOFA Skorunun 6 Organ Sistemi", ["Organ Sistemi", "Ölçülen Laboratuvar / Klinik Parametre", "Puanlama Hedefi"], [
            {"cells": [{"text": "Solunum ve Koagülasyon", "isMasked": False}, {"text": "PaO2/FiO2 ve trombosit sayısı", "isMasked": True, "hint": "akciğer gaz oranı ve kan pulcukları"}, {"text": "Hipoksemi ve trombositopeni takibi"}]},
            {"cells": [{"text": "Karaciğer ve KVS", "isMasked": False}, {"text": "Bilirubin ve OAB / inotrop ihtiyacı", "isMasked": False}, {"text": "Sarılık ve septik şok hipotansiyonu", "isMasked": True, "hint": "karaciğer ve tansiyon çöküşü"}]},
            {"cells": [{"text": "SSS ve Böbrek", "isMasked": False}, {"text": "Glaskow koma skalası ve kreatinin/idrar çıkışı", "isMasked": True, "hint": "nörolojik bilinç ve renal fonksiyon"}, {"text": "Ensefalopati ve akut böbrek hasarı"}]}
        ]),
        make_chain("SOFA 6 Organ Değerlendirmesi", [
            "1. Solunum Sistemi: PaO2/FiO2 ile oksijenasyon kontrolü.",
            "2. Hematolojik Sistem: Trombosit sayısı ile koagülasyon kontrolü.",
            "3. Karaciğer ve Dolaşım: Bilirubin ve tansiyon/inotrop takibi.",
            "4. Beyin ve Böbrek: GKS bilinç düzeyi ve kreatinin/idrar çıkışı ölçümü."
        ]),
        make_recall("SOFA skorlamasında değerlendirilen altı temel organ sistemi hangileridir?", "Solunum, koagülasyon, karaciğer, kardiyovasküler, santral sinir sistemi ve böbrektir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: SOFA Bileşenleri", [
            {"text": "SOFA skorlaması solunum, koagülasyon, karaciğer, kardiyovasküler, SSS ve böbrek sistemlerini inceler.", "isLie": False, "explanation": "Doğru. Tam 6 sistemdir."},
            {"text": "Böbrek fonksiyonları kreatinin ve idrar çıkışı ile değerlendirilir.", "isLie": False, "explanation": "Doğru. Renal parametrelerdir."},
            {"text": "SOFA skorlamasında kemik boyu, ayak numarası ve tırnak sertliği değerlendirilir.", "isLie": True, "explanation": "Tuzak! SOFA hayati 6 organ sistemini (solunum, koagülasyon, karaciğer, KVS, SSS, böbrek) değerlendirir."},
            {"text": "Trombosit sayısı koagülasyon sisteminin SOFA göstergesidir.", "isLie": False, "explanation": "Doğru. Trombositopeni puanlanır."}
        ]),
        make_quiz("SOFA skorlama sisteminde değerlendirilen 6 temel organ sistemi aşağıdakilerin hangisinde eksiksiz verilmiştir?", [
            {"key": "A", "text": "Solunum, koagülasyon, karaciğer, kardiyovasküler, santral sinir sistemi, böbrek", "isCorrect": True, "explanation": "Ders notundaki eksiksiz SOFA organ listesidir."},
            {"key": "B", "text": "Yalnızca göz, kulak, burun ve boğaz", "isCorrect": False, "explanation": "KBB muayenesidir, SOFA değildir."},
            {"key": "C", "text": "Mide, ince bağırsak ve pankreas", "isCorrect": False, "explanation": "SOFA'nın 6 sistemi bunlar değildir."},
            {"key": "D", "text": "Deri, saç, tırnak ve dişler", "isCorrect": False, "explanation": "Hayati organ disfonksiyon skorları değildir."}
        ])
    ]
    slides.append(make_slide(45, "SOFA Bileşenleri: 6 Hayati Organ Sistemi", "Solunum, koagülasyon, karaciğer, KVS, SSS ve böbrek sistemlerinin incelenmesi", "Sepsis", s45_narrative, s45_bullets, s45_elements))

    # Slide 46: SOFA Detay Parametreleri: PaO2, Trombosit, Bilirubin, Koma, Kreatinin
    s46_narrative = (
        "SOFA skorunun altı bileşeni, klinisyenin kolayca erişebileceği standart laboratuvar "
        "ve hemodinamik ölçüm parametrelerine dayandırılmıştır.\n\n"
        "- **Solunum:** Arteriyel oksijen basıncının solunan oksijen fraksiyonuna oranı (**PaO2/FiO2**).\n"
        "- **Koagülasyon ve Karaciğer:** Kan sayımında **trombosit sayısı** ve biyokimyada **total bilirubin** düzeyi.\n"
        "- **Kardiyovasküler ve SSS:** **Ortalama arter basıncı (OAB) ve inotrop ihtiyacı** ile nörolojik "
        "değerlendirmede **Glaskow koma skalası (GKS)**.\n"
        "- **Böbrek:** Serum **kreatinin düzeyi ve saatlik idrar çıkışı** ile renal disfonksiyon derecelendirilir.\n\n"
        "> [!NOTE]\n"
        "> SOFA parametreleri: PaO2/FiO2 (solunum), trombosit (koagülasyon), bilirubin (karaciğer), OAB/inotrop (KVS), Glaskow koma (SSS), kreatinin/idrar çıkışı (böbrek)."
    )
    s46_bullets = [
        "Solunum: PaO2/FiO2 oranı; Koagülasyon: Trombosit sayısı.",
        "Karaciğer: Bilirubin; Kardiyovasküler: Ortalama arter basıncı / inotrop.",
        "Santral sinir sistemi: Glaskow koma skalası; Böbrek: Kreatinin ve idrar çıkışı."
    ]
    s46_elements = [
        make_cloze("SOFA sisteminde santral sinir sistemi Glaskow koma skalası ile böbrek fonksiyonları ise kreatinin ve idrar çıkışı ile değerlendirilir.", "Glaskow koma skalası", "Nörolojik bilinç durumunu ölçen skorlama skalası"),
        make_table("SOFA Biyokimyasal ve Fizyolojik Eşleşmeleri", ["Sistem", "Spesifik Parametre", "Bozulma Yönü"], [
            {"cells": [{"text": "Solunum", "isMasked": False}, {"text": "PaO2/FiO2 oranı", "isMasked": True, "hint": "arter kan gazı parametresi"}, {"text": "Düşüş (hipoksemi)"}]},
            {"cells": [{"text": "Karaciğer", "isMasked": False}, {"text": "Total bilirubin", "isMasked": False}, {"text": "Yükseliş (kolestaz/sarılık)", "isMasked": True, "hint": "safra pigment artışı"}]},
            {"cells": [{"text": "Böbrek", "isMasked": False}, {"text": "Kreatinin ve idrar çıkışı", "isMasked": True, "hint": "böbrek atık ve debi ölçümü"}, {"text": "Kreatininde artış, idrarda azalma"}]}
        ]),
        make_chain("SOFA Laboratuvar Analiz Akışı", [
            "1. Kan Gazı: PaO2/FiO2 hesaplanması.",
            "2. Hemogram ve Biyokimya: Trombosit ve bilirubin analizi.",
            "3. Hemodinami ve Nöroloji: OAB, inotrop ve GKS kaydı.",
            "4. Renal Takip: Kreatinin artışı ve oligüri kontrolü."
        ]),
        make_recall("SOFA skorlamasında karaciğer ve solunum hangi spesifik laboratuvar parametreleri ile değerlendirilir?", "Karaciğer total bilirubin ile, solunum ise PaO2/FiO2 oranı ile değerlendirilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: SOFA Parametreleri", [
            {"text": "Solunum PaO2/FiO2 ile, koagülasyon trombosit sayısı ile izlenir.", "isLie": False, "explanation": "Doğru. Ders notu parametreleridir."},
            {"text": "Böbrek değerlendirmesinde kreatinin ve idrar çıkışı kullanılır.", "isLie": False, "explanation": "Doğru. Renal ölçümlerdir."},
            {"text": "Kardiyovasküler sistem SOFA'da sadece hastanın ayakkabı bağcığı sıklığı ile ölçülür.", "isLie": True, "explanation": "Tuzak! Kardiyovasküler sistem ortalama arter basıncı ve inotrop ihtiyacı ile değerlendirilir."},
            {"text": "Glaskow koma skalası santral sinir sistemi parametresidir.", "isLie": False, "explanation": "Doğru. Bilinç ölçer."}
        ]),
        make_quiz("SOFA skorlama sistemindeki spesifik parametre eşleştirmelerinden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Solunum: PaO2/FiO2, Koagülasyon: trombosit, Karaciğer: bilirubin, SSS: Glaskow koma skalası, Böbrek: kreatinin", "isCorrect": True, "explanation": "Ders notunda parantez içinde verilen tam parametre setidir."},
            {"key": "B", "text": "Solunum: saç uzunluğu, Karaciğer: tırnak rengi", "isCorrect": False, "explanation": "Tıbbi parametreler değildir."},
            {"key": "C", "text": "Böbrek: kan grubu, Koagülasyon: göz rengi", "isCorrect": False, "explanation": "Alakasız eşleştirmelerdir."},
            {"key": "D", "text": "Santral sinir sistemi: kan şekeri, Solunum: hematokrit", "isCorrect": False, "explanation": "SOFA parametreleri yanlış verilmiştir."}
        ])
    ]
    slides.append(make_slide(46, "SOFA Parametreleri ve Laboratuvar Eşleşmeleri", "PaO2/FiO2, trombosit, bilirubin, OAB, GKS ve kreatinin parametreleri", "Sepsis", s46_narrative, s46_bullets, s46_elements))

    # Slide 47: Hızlı Sepsis Değerlendirmesi: qSOFA Kriterleri
    s47_narrative = (
        "Yoğun bakım dışındaki servislerde veya acil servis triyajında, tam SOFA skorunun laboratuvar "
        "sonuçlarını beklemeden sepsisten şüphelenmeyi sağlayan yatak başı hızlı bir araç geliştirilmiştir.\n\n"
        "- **qSOFA (Quick SOFA):** Laboratuvar tetkiki gerektirmeyen, tamamen vital bulgular ve klinik "
        "muayene ile saniyeler içinde hesaplanan hızlı bir tarama skorudur.\n"
        "- **Hipotansiyon Kriteri:** Düşük kan basıncı (**sistolik kan basıncı <100 mmHg**) varlığı 1 puandır.\n"
        "- **Takipne Kriteri:** Yüksek solunum sayısı (**solunum sayısı ≥22 soluk/dakika**) varlığı 1 puandır.\n"
        "- **Klinik Alarm:** Ders notunda vurgulanan bu iki temel kardiyopulmoner kriterin (SBP <100 mmHg "
        "ve solunum ≥22/dk) varlığı klinisyeni acil sepsis protokolü başlatmaya yönlendirir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] qSOFA kardiyopulmoner kriterleri: Düşük kan basıncı (SBP <100 mmHg) = 1 puan; yüksek solunum sayısı (≥22 soluk/dk) = 1 puan."
    )
    s47_bullets = [
        "qSOFA: Yatak başı hızlı sepsis değerlendirme skorudur.",
        "Düşük kan basıncı: Sistolik KB <100 mmHg = 1 puan.",
        "Yüksek solunum sayısı: Solunum sayısı ≥22 soluk/dk = 1 puan."
    ]
    s47_elements = [
        make_cloze("qSOFA skorlamasında düşük kan basıncı eşiği SBP <100 mmHg olup solunum sayısı eşiği ≥22 soluk/dk olarak tanımlanır.", "SBP <100 mmHg", "Sistolik kan basıncındaki 1 puanlık hipotansiyon eşiği"),
        make_table("qSOFA Temel Kriterleri", ["Klinik Parametre", "Patolojik Eşik Değer", "qSOFA Skoru"], [
            {"cells": [{"text": "Sistolik Kan Basıncı (SBP)", "isMasked": False}, {"text": "<100 mmHg", "isMasked": True, "hint": "yüzün altındaki tansiyon"}, {"text": "1 puan"}]},
            {"cells": [{"text": "Solunum Sayısı", "isMasked": False}, {"text": "≥22 soluk/dakika", "isMasked": True, "hint": "yirmi iki ve üzeri nefes"}, {"text": "1 puan"}]}
        ]),
        make_chain("qSOFA Yatak Başı Uygulama Akışı", [
            "1. Vital Ölçüm: Şüpheli enfeksiyonlu hastanın tansiyon ve solunumunun sayılması.",
            "2. Hipotansiyon Kontrolü: SBP <100 mmHg ise 1 puan yazılması.",
            "3. Takipne Kontrolü: Solunum ≥22/dk ise 1 puan eklenmesi.",
            "4. Acil Eylem: Yüksek riskli hastanın derhal agresif resüsitasyona alınması."
        ]),
        make_recall("Ders notunda belirtilen qSOFA'nın iki temel kardiyopulmoner kriteri ve eşik değerleri nelerdir?", "Düşük kan basıncı (SBP <100 mmHg) = 1 puan ve yüksek solunum sayısı (≥22 soluk/dk) = 1 puandır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: qSOFA Kriterleri", [
            {"text": "qSOFA'da düşük kan basıncı için eşik SBP <100 mmHg'dir.", "isLie": False, "explanation": "Doğru. 1 puanlık tansiyon eşiğidir."},
            {"text": "Yüksek solunum sayısı için eşik ≥22 soluk/dakikadır.", "isLie": False, "explanation": "Doğru. 1 puanlık solunum eşiğidir."},
            {"text": "qSOFA'da tansiyonun 220 mmHg olması ve hastanın hiç nefes almaması 100 puanlık iyileşme belirtisidir.", "isLie": True, "explanation": "Tuzak! Kriterler SBP <100 mmHg ve solunum ≥22/dk olup her biri 1 puandır."},
            {"text": "qSOFA hızlı yatak başı sepsis taramasında kullanılır.", "isLie": False, "explanation": "Doğru. Pratik tarama aracıdır."}
        ]),
        make_quiz("qSOFA skorlama sisteminde yer alan kan basıncı ve solunum sayısı kriterleri aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Düşük kan basıncı (SBP <100 mmHg) = 1 puan; yüksek solunum sayısı (≥22 soluk/dk) = 1 puan", "isCorrect": True, "explanation": "Ders notunda harfiyen 'qSOFA: düşük kan basıncı (SBP <100 mmHg) = 1 puan; yüksek solunum sayısı (≥22 soluk/dk) = 1 puan' denmektedir."},
            {"key": "B", "text": "SBP >180 mmHg ve solunum <8 soluk/dk", "isCorrect": False, "explanation": "Eşikler ve yönler yanlıştır."},
            {"key": "C", "text": "SBP <60 mmHg ve solunum >45 soluk/dk", "isCorrect": False, "explanation": "qSOFA eşikleri bu değildir."},
            {"key": "D", "text": "Yalnızca nabız sayısının >150 olması", "isCorrect": False, "explanation": "Nabız qSOFA kriteri değildir."}
        ])
    ]
    slides.append(make_slide(47, "Hızlı Sepsis Değerlendirmesi: qSOFA Kriterleri", "Yatak başı sepsis taraması: SBP <100 mmHg ve solunum ≥22/dk kriterleri", "Sepsis", s47_narrative, s47_bullets, s47_elements))

    # Slide 48: Piyüri ve Bakteriüri Birlikteliğinin Klinik Önemi
    s48_narrative = (
        "Üriner sistem enfeksiyonu tanısında bakteriüri ve piyüri parametrelerinin tek başına değil, "
        "birlikte değerlendirilmesi klinisyeni yanlış tanı ve gereksiz antibiyotikten korur.\n\n"
        "- **Gerçek Enfeksiyon:** İdrarda anlamlı bakteriüriye konak dokusunun enflamatuar reaksiyonunu "
        "gösteren **piyürinin eşlik etmesi**, aktif bir ÜSE'nin en güçlü kanıtıdır.\n"
        "- **Steril Piyüri:** İdrarda piyüri (lökosit) varken rutin kültürde bakteri ürememesi; "
        "tüberküloz, Chlamydia üretriti, taş irritasyonu veya geçirilmiş antibiyotik kullanımını düşündürür.\n"
        "- **Piyürisiz Bakteriüri:** İdrarda bakteri ürerken piyüri bulunmaması ise sıklıkla asemptomatik "
        "bakteriüri veya kültür kabının kontaminasyonuna işaret eder.\n\n"
        "> [!NOTE]\n"
        "> Bakteriüri mikrobiyal varlığı, piyüri ise konak enflamatuar reaksiyonunu gösterir; ikisinin birlikteliği semptomatik enfeksiyonun temelini kurar."
    )
    s48_bullets = [
        "Bakteriüri mikrobiyal kolonizasyonu, piyüri konak enflamasyonunu belgeler.",
        "İkisinin birlikteliği semptomatik ÜSE tanısını kesinleştirir.",
        "Piyürisiz üreme kontaminasyon veya ABU; bakterisiz piyüri steril piyüri tablosudur."
    ]
    s48_elements = [
        make_cloze("İdrarda lökosit varlığına rağmen rutin kültürde bakteri ürememesi tablosuna steril piyüri adı verilir.", "steril piyüri", "Tbc ve klamidyada görülen mikroorganizmasız lökosit tablosu"),
        make_table("Bakteriüri ve Piyüri Birliktelik Matrisi", ["Bakteriüri", "Piyüri", "Olası Klinik Tanı"], [
            {"cells": [{"text": "Var (+)", "isMasked": False}, {"text": "Var (+)", "isMasked": False}, {"text": "Klasik Üriner Sistem Enfeksiyonu", "isMasked": True, "hint": "semptomatik gerçek enfeksiyon"}]},
            {"cells": [{"text": "Var (+)", "isMasked": False}, {"text": "Yok (-)", "isMasked": True, "hint": "akyuvar negatif"}, {"text": "Asemptomatik Bakteriüri veya Kontaminasyon"}]},
            {"cells": [{"text": "Yok (-)", "isMasked": True, "hint": "mikrop üremeyen"}, {"text": "Var (+)", "isMasked": False}, {"text": "Steril Piyüri (Tbc, taş, klamidya)", "isMasked": True, "hint": "kültür negatif enflamasyon"}]}
        ]),
        make_chain("Tanısal Ayrım Zinciri", [
            "1. İdrar Tahlili: Lökosit esteraz ve mikroskopide piyüri aranması.",
            "2. İdrar Kültürü: Koloni sayısı ve bakteriüri seviyesinin ölçülmesi.",
            "3. İkili Değerlendirme: Bakteri + lökosit birlikteliğinin doğrulanması.",
            "4. Klinik Karar: Uygun ampirik veya hedefe yönelik tedavinin seçilmesi."
        ]),
        make_recall("İdrarda piyüri (lökosit) olmasına rağmen rutin kültürde üreme olmaması durumuna ne ad verilir ve hangi etkenler düşünülmelidir?", "Steril piyüri adı verilir; tüberküloz, Chlamydia veya taş irritasyonu düşünülmelidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Tanısal Birliktelik", [
            {"text": "Bakteriüri ve piyüri birlikte olduğunda aktif enfeksiyon düşünülür.", "isLie": False, "explanation": "Doğru. Tipik ÜSE bulgusudur."},
            {"text": "Piyüri konak dokusunun enflamasyonunu gösterir.", "isLie": False, "explanation": "Doğru. Nörofil göçüdür."},
            {"text": "İdrarda 100 trilyon lökosit olması tamamen normaldir ve her insanda doğuştan bulunur.", "isLie": True, "explanation": "Tuzak! İdrarda lökosit artışı patolojiktir, piyüriyi gösterir."},
            {"text": "Bakteriüri olup piyüri olmaması asemptomatik bakteriüriyi düşündürebilir.", "isLie": False, "explanation": "Doğru. Klinik ayrımdır."}
        ]),
        make_quiz("İdrar analizinde belirgin piyüri saptanmasına karşın standart idrar kültüründe üreme olmaması (steril piyüri) durumunda aşağıdakilerden hangisi akla gelmelidir?", [
            {"key": "A", "text": "Tüberküloz veya Chlamydia enfeksiyonu", "isCorrect": True, "explanation": "Steril piyürinin klasik nedenleri tüberküloz, atipik üretrit etkenleri ve taşlardır."},
            {"key": "B", "text": "Hastanın tamamen iyileştiği ve hiçbir sorununun olmadığı", "isCorrect": False, "explanation": "Piyüri bir patolojiyi işaret eder."},
            {"key": "C", "text": "İdrarın aşırı steril saf suya dönüştüğü", "isCorrect": False, "explanation": "Fizyolojik bir açıklama değildir."},
            {"key": "D", "text": "Kişinin böbreklerinin çalışmayı durdurduğu", "isCorrect": False, "explanation": "Steril piyüri spesifik enfeksiyonları gösterir."}
        ])
    ]
    slides.append(make_slide(48, "Bakteriüri ve Piyüri Birlikteliğinin Klinik Yansıması", "Bakteriyel üreme ile konak enflamatuar yanıtının ayırt edici tanısal değeri", "Tanımlar", s48_narrative, s48_bullets, s48_elements))

    # Slide 49: Beşinci Bölüm Özeti: Tanı Kriterleri ve Sepsis
    s49_narrative = (
        "Bakteriüri, piyüri ve sepsis tanımları, üriner enfeksiyonun şiddetini ve hastanın "
        "risk profilini belirleyen standart köşe taşlarıdır.\n\n"
        "- **Bakteriüri ve Piyüri:** Anlamlı bakteriüri; suprapubikte **herhangi bir üreme** anlamlıdır. "
        "Piyüri ise santrifüjsüz idrarda **≥10/mm³**, santrifüj edilmişte her alanda **en az 5-10 lökosit**tir.\n"
        "- **Sepsis ve SOFA:** Üriner sepsiste **SOFA** skorlaması 6 organ sistemini (solunum, koagülasyon, "
        "karaciğer, KVS, SSS, böbrek) kapsar.\n"
        "- **Hızlı Tarama (qSOFA):** Yatak başında düşük kan basıncı (**SBP <100 mmHg** = 1 puan) ve "
        "yüksek solunum sayısı (**solunum ≥22 soluk/dk** = 1 puan) ile sepsis taranır.\n\n"
        "> [!IMPORTANT]\n"
        "> [BÖLÜM ÖZETİ] Suprapubikte herhangi bir üreme anlamlıdır; santrifüjsüz ≥10/mm³, santrifüjlü 5-10 lökosit piyüridir; SOFA 6 organı, qSOFA ise SBP <100 mmHg ve solunum ≥22/dk'yı içerir."
    )
    s49_bullets = [
        "Suprapubik aspirasyonda herhangi bir üreme anlamlıdır.",
        "Piyüri: Santrifüjsüz ≥10/mm³, santrifüj edilmişte her sahada en az 5-10 lökosit.",
        "SOFA: 6 organ (solunum, koagülasyon, karaciğer, KVS, SSS, böbrek).",
        "qSOFA: SBP <100 mmHg (1 puan) ve solunum sayısı ≥22/dk (1 puan)."
    ]
    s49_elements = [
        make_cloze("Santrifüjsüz idrarda piyüri eşiği ≥10/mm³ iken qSOFA solunum eşiği ≥22 soluk/dk olarak tanımlanır.", "≥10/mm³", "Santrifüjsüz idrar piyüri eşiği"),
        make_table("Tanısal ve Sepsis Kriterleri Özeti", ["Parametre", "Tanı Eşiği / Kriter", "Klinik Rol"], [
            {"cells": [{"text": "Suprapubik Aspirasyon", "isMasked": False}, {"text": "Herhangi bir üreme", "isMasked": True, "hint": "sayı sınırı olmaksızın"}, {"text": "Steril mesane idrarı kanıtı"}]},
            {"cells": [{"text": "Piyüri (Santrifüjsüz)", "isMasked": False}, {"text": "≥10/mm³ lökosit", "isMasked": False}, {"text": "Hemositometrik enflamasyon", "isMasked": True, "hint": "kamara sayım eşiği"}]},
            {"cells": [{"text": "Piyüri (Santrifüjlü)", "isMasked": False}, {"text": "Her alanda en az 5-10 lökosit", "isMasked": True, "hint": "sediment sahası"}, {"text": "Rutin mikroskopi eşiği"}]},
            {"cells": [{"text": "qSOFA Kriterleri", "isMasked": False}, {"text": "SBP <100 mmHg ve solunum ≥22/dk", "isMasked": False}, {"text": "Hızlı yatak başı sepsis taraması", "isMasked": True, "hint": "acil servis sepsis şüphesi"}]}
        ]),
        make_chain("Tanısal Hiyerarşi Akışı", [
            "1. İdrar Örneği: Uygun yöntemle alınıp bakteriüri/piyüri bakılması.",
            "2. Piyüri Doğrulaması: Santrifüjsüz ≥10/mm³ veya sedimentte 5-10 lökosit.",
            "3. Vital Kontrol: SBP <100 ve solunum ≥22 ile qSOFA tespiti.",
            "4. Sistemik Değerlendirme: Gereğinde 6 organlı SOFA skorlaması."
        ]),
        make_recall("Beşinci bölümün temel sayısal değerleri olarak santrifüjsüz piyüri eşiği ve qSOFA'nın iki kardiyopulmoner kriteri nedir?", "Santrifüjsüz piyüri ≥10/mm³'tür; qSOFA kriterleri ise SBP <100 mmHg ve solunum sayısı ≥22 soluk/dakikadır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 5 Özeti", [
            {"text": "Suprapubik aspirasyonla alınan idrarda herhangi bir üreme anlamlıdır.", "isLie": False, "explanation": "Doğru. Steril yöntemdir."},
            {"text": "Santrifüj edilmemiş idrarda piyüri eşiği ≥10/mm³'tür.", "isLie": False, "explanation": "Doğru. Sayısal kriterdir."},
            {"text": "qSOFA'da solunum sayısı kriteri solunumun dakikada tam 3 kez olmasıdır.", "isLie": True, "explanation": "Tuzak! qSOFA solunum sayısı kriteri ≥22 soluk/dakikadır (takipne)."},
            {"text": "SOFA skorlamasında 6 farklı organ sistemi değerlendirilir.", "isLie": False, "explanation": "Doğru. 6 sistem puanlanır."}
        ]),
        make_quiz("Beşinci bölümde işlenen tanısal kriterler ve sepsis skorları değerlendirildiğinde aşağıdakilerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Santrifüj edilmiş idrarda her alanda en az 100.000 lökosit görülmeden piyüri denilemez", "isCorrect": True, "explanation": "Yanlış! Santrifüj edilmiş idrarda her alanda en az 5-10 lökosit görülmesi piyüri için yeterlidir."},
            {"key": "B", "text": "Santrifüj edilmemiş idrarda ≥10/mm³ lökosit saptanması piyüri olarak kabul edilir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Steril koşullarda alınan idrarda (suprapubik aspirasyon) herhangi bir üreme anlamlıdır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "qSOFA'da sistolik kan basıncı <100 mmHg ve solunum sayısı ≥22 soluk/dk kriterleri kullanılır", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(49, "Beşinci Bölüm Özeti: Tanı Kriterleri ve Sepsis", "Bakteriüri, santrifüjsüz/santrifüjlü piyüri, SOFA ve qSOFA kurallarının özeti", "Bölüm Özeti", s49_narrative, s49_bullets, s49_elements))

    # Slide 50: [TEKRAR SAYFASI - CHECKPOINT 5] Bakteriüri, Piyüri ve Sepsis Tanımları
    s50_narrative = (
        "Bu tekrar sayfasında 5. Bölümde işlenen bakteriüri, santrifüjsüz/santrifüjlü piyüri "
        "kriterlerini ve SOFA/qSOFA sepsis değerlendirme sistemlerini pekiştiriyoruz.\n\n"
        "- **Bakteriüri:** İdrarda belli seviye üstünde bakteri olmasıdır; suprapubik aspirasyonda "
        "**herhangi bir üreme** anlamlı kabul edilir.\n"
        "- **Piyüri Kriterleri:** Santrifüj edilmemiş örnekte **≥10/mm³**; santrifüj edilmiş idrarda "
        "her büyük büyütme alanında **en az 5-10 lökosit** görülmesidir.\n"
        "- **Sepsis Değerlendirmesi:** **SOFA** skorlaması 6 organ sistemini (solunum, koagülasyon, "
        "karaciğer, KVS, SSS, böbrek) kapsar; **qSOFA**'da ise **SBP <100 mmHg** (1 puan) ve **solunum ≥22 soluk/dk** (1 puan) aranır.\n\n"
        "> [!IMPORTANT]\n"
        "> [TEKRAR SAYFASI - CHECKPOINT 5] Suprapubikte herhangi bir üreme anlamlıdır; piyüri santrifüjsüz ≥10/mm³, santrifüjlü 5-10 lökosittir; SOFA 6 organ sistemini incelerken qSOFA'da SBP <100 mmHg ve solunum ≥22/dk esastır."
    )
    s50_bullets = [
        "Bakteriüri: Anlamlı bakteriüri; suprapubik aspirasyonda herhangi bir üreme anlamlıdır.",
        "Piyüri: Santrifüjsüz örnekte ≥10/mm³; santrifüj edilmişte her alanda en az 5-10 lökosit.",
        "SOFA: 6 organ (solunum, koagülasyon, karaciğer, kardiyovasküler, SSS, böbrek).",
        "qSOFA: Sistolik KB <100 mmHg (1 puan) ve solunum sayısı ≥22 soluk/dk (1 puan)."
    ]
    s50_elements = [
        make_cloze("Santrifüjsüz idrar örneğinde piyüri tanısı için ≥10/mm³ lökosit aranırken qSOFA sistolik basınç eşiği SBP <100 mmHg olarak belirlenmiştir.", "≥10/mm³", "Santrifüj edilmemiş idrardaki lökosit tanı eşiği"),
        make_table("5. Bölüm Büyük Tekrar Tablosu", ["Tanısal Parametre", "Sayısal Değer / Eşik", "Klinik Anlamı"], [
            {"cells": [{"text": "Suprapubik Aspirasyon", "isMasked": False}, {"text": "Herhangi bir üreme", "isMasked": True, "hint": "tüm koloniler tanısal"}, {"text": "Steril mesane bakteriürisi"}]},
            {"cells": [{"text": "Piyüri (Santrifüjsüz)", "isMasked": False}, {"text": "≥10/mm³ lökosit", "isMasked": False}, {"text": "Sayım odacığında lökositoz", "isMasked": True, "hint": "hemositometrik eşik"}]},
            {"cells": [{"text": "Piyüri (Santrifüjlü)", "isMasked": False}, {"text": "Her alanda en az 5-10 lökosit", "isMasked": True, "hint": "mikroskop sahası eşiği"}, {"text": "Sediment mikroskopisi piyürisi"}]},
            {"cells": [{"text": "qSOFA Kriterleri", "isMasked": False}, {"text": "SBP <100 mmHg; solunum ≥22/dk", "isMasked": False}, {"text": "Hızlı yatak başı sepsis taraması", "isMasked": True, "hint": "vital sepsis alarmları"}]}
        ]),
        make_chain("5. Bölüm Sentez Zinciri", [
            "1. İdrar Kültürü: Suprapubikte herhangi bir üremenin anlamlılığı.",
            "2. Piyüri Tespiti: Santrifüjsüz ≥10/mm³ veya sedimentte 5-10 lökosit.",
            "3. qSOFA Taraması: SBP <100 mmHg ve solunum ≥22/dk ile risk tayini.",
            "4. SOFA Takibi: 6 organda disfonksiyon skorunun hesaplanması."
        ]),
        make_recall("Checkpoint 5: Santrifüjlü idrarda piyüri kriteri ve SOFA skorlamasında değerlendirilen 6 organ sistemi nedir?", "Santrifüjlü idrarda her alanda en az 5-10 lökosittir; SOFA'nın 6 organ sistemi ise solunum, koagülasyon, karaciğer, kardiyovasküler, santral sinir sistemi ve böbrektir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Checkpoint 5 Konsolidasyonu", [
            {"text": "Santrifüj edilmemiş idrarda piyüri eşik değeri ≥10/mm³ lökosittir.", "isLie": False, "explanation": "Doğru. 5. bölüm temel kuralıdır."},
            {"text": "SOFA skorlama sisteminde solunum, koagülasyon, karaciğer, KVS, SSS ve böbrek değerlendirilir.", "isLie": False, "explanation": "Doğru. 6 organ sistemidir."},
            {"text": "qSOFA'da düşük kan basıncı eşiği sistolik KB <100 mmHg ve solunum sayısı eşiği ≥22 soluk/dakikadır.", "isLie": False, "explanation": "Doğru. İki kardiyopulmoner kriterdir."},
            {"text": "Suprapubik aspirasyonla alınan idrarda bakteriüri tanısı için en az 100 milyon koloni şarttır.", "isLie": True, "explanation": "Tuzak! Steril koşullarda alınan (suprapubik aspirasyon) idrarda herhangi bir üreme anlamlı kabul edilir."}
        ]),
        make_quiz("5. Bölümün tamamı (Bakteriüri, Piyüri ve Sepsis Tanımları) değerlendirildiğinde aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Suprapubik aspirasyonla steril koşulda alınan idrarda sadece 1 koloni üremesi önemsiz kabul edilir ve hasta taburcu edilir", "isCorrect": True, "explanation": "Yanlış! Steril koşullarda alınan (suprapubik aspirasyon) idrarda herhangi bir üreme (tek bir koloni dahi) anlamlıdır."},
            {"key": "B", "text": "Santrifüj edilmemiş idrar örneğinde piyüri için ≥10/mm³ lökosit aranır", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Santrifüj edilmiş idrarda her sahada en az 5-10 lökosit görülmesi piyüri kriteridir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "qSOFA skorlamasında sistolik KB <100 mmHg ve solunum sayısı ≥22 soluk/dk kriterleri 1'er puandır", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(50, "[TEKRAR SAYFASI - CHECKPOINT 5] Bakteriüri, Piyüri ve Sepsis Tanımları", "5. Bölümün kapsamlı pekiştirmesi: bakteriüri, santrifüjsüz/santrifüjlü piyüri, SOFA ve qSOFA", "Bölüm Tekrarı", s50_narrative, s50_bullets, s50_elements))

    return slides
