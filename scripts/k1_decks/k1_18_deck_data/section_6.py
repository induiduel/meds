# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_6_slides():
    slides = []

    # Slide 51
    slides.append({
        "id": "k1-18-s51",
        "title": "Skorbüt (C Vitamini Eksikliği) ve Denizcilerin Meslek Hastalığı",
        "content": "Coğrafi Keşifler döneminde denizcileri okyanus fırtınalarından, gemi kazalarından ve savaşlardan daha fazla kıran en büyük tehdit skorbüttü (Sınav Spotu):\n\n- **Hastalığın Nedeni:**\n  - İnsan vücudu askorbik asit (C vitamini) sentezleyemez; dışarıdan taze sebze ve meyveyle almak zorundadır.\n  - Aylarca süren okyanus seferlerinde taze besinler tükenir, tayfalar yalnızca kuru peksimet ve tuzlanmış domuz etiyle beslenirdi.\n- **Klinik Tablo:**\n  - Kollajen sentezinde prolin ve lizin hidroksilasyonu durur.\n  - Damar endoteli çatlar; diş etleri süngerleşip kararır ve kanar; dişler dökülür; deride peteşi ve ekimozlar çıkar.\n  - Eski yara izleri yeniden açılır, kemikler kırılır ve hasta aşırı yorgunluk, letarji ve kalp yetmezliğinden hayatını kaybeder.\n- **Meslek Hastalığı Niteliği:** Skorbüt, denizcilik mesleğinin karakteristik bir malnütrisyon tablosuydu.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Taze C Vitamini Varlığı vs Aylarca Yokluğu (Skorbüt)",
                "Yeterli C Vitamini (Kollajen Sağlam)",
                "Kollajen lifleri çapraz bağlanır, damar duvarı dayanıklıdır, diş etleri ve kemikler sağlıklıdır.",
                "C Vitamini Yokluğu (Skorbüt)",
                "Kollajen çatlar, diş etleri çürürcesine kanar, eski yaralar açılır, kemik kırıkları ve ölüm gerçekleşir."
            ),
            make_quiz(
                "Okyanus aşırı uzun deniz seferlerinde taze sebze ve meyve tüketemeyen denizcilerde kollajen sentez bozukluğu sonucu diş eti kanamaları ve ölümle seyreden eksiklik hastalığı hangisidir?",
                [
                    {"key": "A", "text": "Skorbüt (C vitamini eksikliği)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Skorbüt askorbik asit eksikliğine bağlı kollajen sentez kusurudur; denizcilerin meslek hastalığıydı."},
                    {"key": "B", "text": "Beriberi (B1 vitamini eksikliği)", "isCorrect": False, "explanation": "Tiamin eksikliğidir, pirinç yiyenlerde görülür."},
                    {"key": "C", "text": "Pellegra (B3 vitamini eksikliği)", "isCorrect": False, "explanation": "Niasin eksikliğidir, mısır yiyenlerde görülür."},
                    {"key": "D", "text": "Raşitizm (D vitamini eksikliği)", "isCorrect": False, "explanation": "Kemik mineralizasyon bozukluğudur."}
                ]
            )
        ]
    })

    # Slide 52
    slides.append({
        "id": "k1-18-s52",
        "title": "Kommodor Anson'un Dünya Gezisi (1740): Skorbütün Trajedisi",
        "content": "Skorbütün ne denli dehşet verici bir halk sağlığı ve askeri felaket olduğu Kommodor George Anson'un tarihi seferiyle belgelenmiştir (Sınav Spotu):\n\n- **Büyük Britanya Donanma Seferi (1740-1744):**\n  - İngiliz amirali George Anson, 7 büyük savaş gemisi ve **1955 kişilik seçkin tayfayla** İspanyol donanmasına karşı dünya turuna çıktı.\n- **Korkunç Kayıp Oranı:**\n  - 3.5 yıl sonra İngiltere'ye yalnızca tek bir gemi (Centurion) ve bir avuç insanla dönebildi.\n  - Toplam 1955 personelden **1051 kişi (%54'ü)** düşman kurşunuyla değil, **yalnızca skorbüt hastalığından** dolayı can verdi!\n- **Tarihsel Çıkarım:**\n  - Donanmaları düşman donanmalarının değil, tek bir besin maddesi eksikliğinin yok edebildiği gerçeği, İngiliz tıp dünyasını acil çözüm aramaya itti.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Sefer Parametresi", "Çıkış Değeri (1740)", "Dönüş Değeri (1744)", "Kayıp Oranı"],
                [
                    ["Savaş Gemisi Sayısı", "7 gemi", "Yalnızca 1 gemi", "%85 gemi kaybı"],
                    ["Toplam Mürettebat", "1955 tayfa", "Geriye kalan az sayıda asker", "1051 skorbüt ölümü (%54)"],
                    ["Ölüm Nedeni", "Düşman çatışması çok az", "Temel neden: Taze gıdasızlık ve skorbüt", "Tarihin en büyük beslenme trajedisi"]
                ]
            ),
            make_cloze(
                "1740 yılında yedi gemi ve 1955 personelle sefere çıkan ve mürettebatının yüzde elli dördünü skorbütten kaybeden ünlü İngiliz komutan Kommodor Anson'dur.",
                "Kommodor Anson",
                "Skorbütün yıkıcılığını belgeleyen tarihi dünya seferinin amirali"
            )
        ]
    })

    # Slide 53
    slides.append({
        "id": "k1-18-s53",
        "title": "James Lind (1753) ve İlk Kontrollü Klinik Deney: Narenciye Tedavisi",
        "content": "İskoç donanma hekimi James Lind (1716-1794), tıp tarihinin ilk prospektif kontrollü klinik çalışmasını tasarlamıştır (Sınav Spotu):\n\n- **Tarihi Klinik Deney (20 Mayıs 1747 - HMS Salisbury Gemisi):**\n  - Lind, skorbüte yakalanmış, benzer ağırlıktaki 12 denizciyi seçti.\n  - Hepsine aynı standart gemi diyetini verdi ancak hastaları **ikişer kişilik 6 gruba ayırarak** farklı ek tedaviler uyguladı:\n  - 1. Grup: Günde bir litre elma şarabı (cider),\n  - 2. Grup: Sülfürik asit damlası (vitriol iksiri),\n  - 3. Grup: Sirke,\n  - 4. Grup: Deniz suyu,\n  - 5. Grup: Baharatlı sarımsak macunu ve arpa suyu,\n  - **6. Grup: Günde 2 portakal ve 1 limon**.\n- **Sonuç:** Narenciye (portakal ve limon) alan iki denizci **6 gün içinde mucizevi bir şekilde tamamen iyileşti** ve diğer hastalara bakacak güce kavuştu; diğer gruplarda hiçbir düzelme olmadı.\n- **A Treatise of the Scurvy (1753):** Lind bu tarihi bulguyu kitabıyla yayınladı.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "James Lind'in Kontrollü Klinik Deney Basamakları",
                [
                    "1. Homojen Grup Seçimi: Benzer evredeki 12 skorbütlü denizci belirlenir.",
                    "2. Sabit Temel Diyet: Tüm hastalara aynı yemek verilir (karıştırıcı faktörler kontrol edilir).",
                    "3. 6 Ayrı Kol: İkişer kişilik gruplara elma şarabı, sirke, deniz suyu, vitriol ve narenciye verilir.",
                    "4. Kesin Sonuç: Yalnızca portakal ve limon alan grup 6 günde hızla ayağa kalkar.",
                    "5. Bilimsel Kanıt: Tıp tarihinin ilk kontrollü karşılaştırmalı klinik deneyi belgelenir."
                ]
            ),
            make_cloze(
                "1747 yılında gemide skorbütlü denizcileri gruplara ayırarak limon ve portakalın iyileştirici etkisini ilk kontrollü klinik deneyle kanıtlayan hekim James Lind'dir.",
                "James Lind",
                "İlk kontrollü klinik beslenme deneyini yapan İskoç donanma cerrahı"
            )
        ]
    })

    # Slide 54
    slides.append({
        "id": "k1-18-s54",
        "title": "Narenciyenin Zorunlu Kılınması ve Britanya Deniz Üstünlüğü",
        "content": "James Lind'in bulgusu, bürokratik ihmaller nedeniyle donanmada hemen kabul görmemiş; ancak 42 yıl sonra hayata geçirilmiştir (Sınav Spotu):\n\n- **Gilbert Blane ve Zorunlu Limon Suyu (1795):**\n  - Kraliyet Donanması Sağlık Heyeti Başkanı Gilbert Blane, Lind'in çalışmasını referans alarak tüm İngiliz savaş gemilerinde **her denizciye günlük limon suyu (lime juice) verilmesini zorunlu kıldı**.\n- **Halk Sağlığı ve Askeri Sonuç:**\n  - Karardan hemen sonra İngiliz donanmasında skorbüt vakaları bıçak gibi kesilerek **sıfıra indi**.\n  - Donanma personeli açık denizlerde aylarca sağlıklı kalabildiği için Napolyon savaşlarında (Trafalgar Savaşı - 1805) Fransız ve İspanyol donanmalarına karşı kesin bir üstünlük sağladı.\n- **'Limey' Lakabı:** İngiliz denizcilerine limondan dolayı dünya denizcilik argosunda 'Limey' lakabı takılmıştır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Limon Suyu Öncesi Donanma vs Limon Suyu Sonrası Donanma",
                "Limon Suyu Öncesi",
                "Gemiler skorbüt yüzünden savaşamadan limanlara dönmek zorunda kalır veya batardı.",
                "Limon Suyu Sonrası (1795)",
                "Skorbüt sıfırlandı; donanma aylarca denizde kalarak küresel deniz hakimiyetini kurdu."
            ),
            make_quiz(
                "James Lind'in keşfinden sonra İngiliz Kraliyet Donanması'nda tüm denizcilere günlük limon suyu verilmesini zorunlu kılan ve skorbütü sıfırlayan hekim kimdir?",
                [
                    {"key": "A", "text": "Gilbert Blane", "isCorrect": True, "explanation": "Doğru cevap A'dır: Gilbert Blane 1795'te donanmada limon suyunu zorunlu kılmış ve skorbütü bitirmiştir."},
                    {"key": "B", "text": "Kommodor Anson", "isCorrect": False, "explanation": "Seferde tayfasını kaybeden komutandır."},
                    {"key": "C", "text": "John Snow", "isCorrect": False, "explanation": "Kolera epidemiyolojistidir."},
                    {"key": "D", "text": "Edwin Chadwick", "isCorrect": False, "explanation": "Sanitasyon reformcusudur."}
                ]
            )
        ]
    })

    # Slide 55
    slides.append({
        "id": "k1-18-s55",
        "title": "Pellegra, Beriberi ve Raşitizm: Beslenme Yetersizliklerinin Keşfi",
        "content": "Skorbütün ardından 19. ve 20. yüzyıllarda tek taraflı beslenmenin yol açtığı diğer 'eksiklik hastalıkları' da çözülmüştür (Sınav Spotu):\n\n- **1. Beriberi (B1 Vitamini / Tiamin Eksikliği):**\n  - Kabuğu soyulmuş (cilalanmış beyaz pirinç) ile beslenen Asya toplumlarında polinöropati, kas erimesi (kuru beriberi) ve kalp yetmezliği (yaş beriberi) yapardı.\n  - Christiaan Eijkman (1897), tavuklara pirinç kepeği yedirerek beriberiyi iyileştirdi (1929 Nobel Ödülü).\n- **2. Pellegra (B3 Vitamini / Niasin Eksikliği):**\n  - Yalnızca mısırla beslenen yoksul köylülerde **4D belirtisi (Dermatit, Diyare, Demans, Death - Ölüm)** ile seyrederdi.\n  - Joseph Goldberger (1914), pellagranın bulaşıcı değil, protein ve süt eksikliğine bağlı bir beslenme yetersizliği olduğunu kanıtladı.\n- **3. Raşitizm (D Vitamini Eksikliği):**\n  - Sanayi kentlerinde güneş görmeyen fabrika çocuklarında eğri bacaklar ve kemik deformiteleri balık yağı ve güneş ışığıyla önlendi.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Hastalık", "Eksik Olan Besin Öğesi", "Temel Klinik Bulgular", "Halk Sağlığı Önlemi"],
                [
                    ["Skorbüt", "C Vitamini (Askorbik asit)", "Diş eti kanaması, peteşi, yara açılması", "Taze narenciye ve sebze tüketimi"],
                    ["Beriberi", "B1 Vitamini (Tiamin)", "Periferik nöropati, kardiyak yetmezlik", "Tam tahıl ve pirinç kepeği tüketimi"],
                    ["Pellegra", "B3 Vitamini (Niasin) / Triptofan", "4D: Dermatit, Diyare, Demans, Ölüm", "Et, süt, yumurta ve niasin takviyesi"],
                    ["Raşitizm", "D Vitamini / Kalsiyum", "Kraniotabes, bacaklarda O/X eğriliği", "Güneş ışığı ve balık yağı (D vitamini)"]
                ]
            ),
            make_quiz(
                "Yalnızca mısır ağırlıklı beslenen yoksul toplumlarda görülen; dermatit, diyare, demans ve tedavi edilmezse ölümle (4D) karakterize niasin eksikliği hastalığı hangisidir?",
                [
                    {"key": "A", "text": "Pellegra", "isCorrect": True, "explanation": "Doğru cevap A'dır: Pellegra niasin (B3) eksikliğinde görülen klasik 4D tablosudur."},
                    {"key": "B", "text": "Beriberi", "isCorrect": False, "explanation": "B1 vitamini eksikliğidir."},
                    {"key": "C", "text": "Skorbüt", "isCorrect": False, "explanation": "C vitamini eksikliğidir."},
                    {"key": "D", "text": "Kretenizm", "isCorrect": False, "explanation": "İyot eksikliğidir."}
                ]
            )
        ]
    })

    # Slide 56
    slides.append({
        "id": "k1-18-s56",
        "title": "Bernardino Ramazzini (1633-1714): İş Sağlığı ve Meslek Hastalıklarının Babası",
        "content": "İtalyan hekim Bernardino Ramazzini, çalışanların sağlığını ve çalışma ortamının hastalıklara etkisini inceleyen ilk bilim insanıdır (Sınav Spotu):\n\n- **De Morbis Artificum Diatriba (Çalışanların Hastalıkları - 1700):**\n  - Tıp tarihinde iş sağlığı ve meslek hastalıkları üzerine yazılmış **ilk kapsamlı kitaptır**.\n  - Madenciler, cam üfleyicileri, fırıncılar, eczacılar, lağım temizleyicileri, dokumacılar ve katipler dahil 50'den fazla meslek grubunun maruz kaldığı tehlikeleri incelemiştir.\n- **İki Temel Hastalık Nedeni:**\n  1. **İş yerindeki zararlı maddeler:** Tozlar, zehirli dumanlar, cıva, kurşun buharları ve gazlar.\n  2. **Ergonomik ve fiziksel zorlanmalar:** Sürekli aynı duruşta (postürde) hareketsiz kalma, ağır yük kaldırma, tekrarlayan hareketler ve aşırı zorlanmalar.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Ramazzini Öncesi Tıp vs Ramazzini'nin İş Sağlığı",
                "Ramazzini Öncesi",
                "Hekimler yalnızca hastanın organına ve mizacına bakar, ne iş yaptığını sormayı akıllarına bile getirmezdi.",
                "Ramazzini'nin Devrimi (1700)",
                "Hastanın yaptığı işin, soluduğu tozun ve duruşunun hastalığın asıl kaynağı olduğunu ortaya koydu."
            ),
            make_cloze(
                "1700 yılında yazdığı De Morbis Artificum Diatriba eseriyle iş sağlığı ve meslek hastalıklarının kurucusu kabul edilen İtalyan hekim Bernardino Ramazzini'dir.",
                "Bernardino Ramazzini",
                "İş sağlığı ve güvenliğinin babası kabul edilen İtalyan tıp bilgini"
            )
        ]
    })

    # Slide 57
    slides.append({
        "id": "k1-18-s57",
        "title": "'Ne İş Yaparsınız?' Sorusu: Anamnezde Mesleki Maruziyetin Önemi",
        "content": "Ramazzini, klinik tıp muayenesine evrensel ve hayati bir soru eklemiştir (Sınav Spotu):\n\n- **Hipokratik Anamneze Eklenen Tarihi Soru:**\n  - Hipokrat hekimlere hastanın yaşını, şikayetini, beslenmesini ve idrarını sormayı öğütlemişti.\n  - Ramazzini ise şöyle demiştir:\n  - *'Bir hekim bir işçinin evine gittiğinde yalnızca nabzını saymakla yetinmemelidir. Hastaya mutlaka şu soruyu da yöneltmelidir: **NE İŞ YAPARSINIZ? (Quam artem exerceat?)**'*\n- **Halk Sağlığı Açısından Önemi:**\n  - Günümüzde silikozis, asbestozis, kurşun zehirlenmesi, mezotelyoma ve mesleki astım gibi binlerce hastalık ancak hastanın mesleği ve işyeri koşulları sorgulandığında doğru teşhis edilebilir.\n  - Anamnezde meslek sorgulaması koruyucu iş hekimliğinin temelidir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Mesleki Anamnez ve Tanı Basamakları",
                [
                    "1. Şikayet ve Öykü: Hastanın öksürük, nefes darlığı veya karın ağrısı şikayeti dinlenir.",
                    "2. Ramazzini Sorusu: 'Ne iş yaparsınız?' sorusuyla çalışma ortamı ve iş tanımı öğrenilir.",
                    "3. Maruziyet Analizi: Solunan tozlar (asbest, silika), kimyasallar veya ergonomik riskler taranır.",
                    "4. Meslek Hastalığı Tanısı ve Bildirim: Hastalık işyeri ortamıyla ilişkilendirilir ve koruyucu önlemler alınır."
                ]
            ),
            make_cloze(
                "Bernardino Ramazzini, hekimlerin anamnez alırken hastalarına mutlaka sorması gereken altın sorunun ne iş yaparsınız sorusu olduğunu vurgulamıştır.",
                "ne iş yaparsınız",
                "Ramazzini'nin Hipokratik muayeneye eklediği meslek sorgulama sorusu"
            )
        ]
    })

    # Slide 58
    slides.append({
        "id": "k1-18-s58",
        "title": "Sanayi Devrimi, Çocuk İşçiliği ve Fabrika Yasaları (Factory Acts)",
        "content": "18. ve 19. yüzyıllarda Sanayi Devrimi, muazzam bir zenginlik yaratırken işçi sınıfı için korkunç bir sağlık felaketine dönüştü (Sınav Spotu):\n\n- **Vahşi Çalışma Koşulları:**\n  - 5-6 yaşındaki küçücük çocuklar maden ocaklarında günde 14-16 saat çalıştırılıyor, baca temizliğinde kanserojen ise maruz kalıyor, dokuma tezgahlarında parmaklarını kaybediyordu.\n  - Bacaları temizleyen çocuklarda kurum maruziyetine bağlı gelişen skrotum kanseri (Pott kanseri), **tarihte tanımlanan ilk mesleki kanserdir** (Percivall Pott, 1775).\n- **Fabrika Yasaları (Factory Acts):**\n  - İngiltere'de ardı ardına çıkarılan yasalarla çocuk işçilerin çalışma saatleri sınırlandırıldı, 9 yaşından küçüklerin çalışması yasaklandı ve fabrikalara havalandırma zorunluluğu getirildi.\n- **Halk Sağlığı Dersi:** Çalışan sağlığı bireysel bir şans değil, **devletin yasalarla ve denetimlerle korumak zorunda olduğu kamusal bir haktır**.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Gelişme / Yasa", "Yıl / Hekim", "Halk Sağlığı ve İşçi Koruması"],
                [
                    ["Baca Temizleyicileri Skrotum Kanseri", "1775 (Percivall Pott)", "Tarihte kimyasal maruziyete bağlı tanımlanan ilk meslek kanseri"],
                    ["İngiliz Fabrika Yasası (Factory Act)", "1833", "9 yaş altı çocuk işçiliğinin yasaklanması ve fabrika müfettişliği"],
                    ["10 Saat Yasası", "1847", "Kadın ve gençlerin günlük çalışma süresinin 10 saatle sınırlandırılması"]
                ]
            ),
            make_quiz(
                "1775 yılında baca temizleyicisi çocuklarda kurum maruziyetine bağlı gelişen skrotum kanserini tanımlayarak tarihte ilk mesleki kanseri keşfeden cerrah kimdir?",
                [
                    {"key": "A", "text": "Percivall Pott", "isCorrect": True, "explanation": "Doğru cevap A'dır: Percivall Pott baca temizleyicisi çocuklardaki skrotum kanserini bularak ilk mesleki kanseri belgelemiştir."},
                    {"key": "B", "text": "Bernardino Ramazzini", "isCorrect": False, "explanation": "İş sağlığı kitabını yazmıştır."},
                    {"key": "C", "text": "James Lind", "isCorrect": False, "explanation": "Skorbüt araştırmacısıdır."},
                    {"key": "D", "text": "Edwin Chadwick", "isCorrect": False, "explanation": "Sanitasyon reformcusudur."}
                ]
            )
        ]
    })

    # Slide 59 - CHECKPOINT 6
    slides.append({
        "id": "k1-18-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Beslenme Tarihçesi, Skorbüt ve İş Sağlığı",
        "content": "Bu checkpointte beslenme yetersizliklerini, skorbütü ve iş sağlığının kurucularını özetliyoruz:\n\n- **Skorbüt (C Vitamini Eksikliği):** Kollajen sentez kusuru; diş eti kanaması, peteşi ve yaraların açılmasıyla seyreder; denizcilerin meslek hastalığıydı.\n- **Kommodor Anson (1740):** 1955 kişilik mürettebatının %54'ünü (1051 kişi) skorbütten kaybetti.\n- **James Lind (1753):** 1747'de 12 denizci üzerinde tarihin ilk kontrollü klinik deneyini yaptı; limon ve portakalın skorbütü iyileştirdiğini kanıtladı.\n- **Gilbert Blane (1795):** Donanmada limon suyunu zorunlu kılarak skorbütü sıfırladı; İngiliz deniz üstünlüğünü sağladı.\n- **Diğer Beslenme Hastalıkları:** Beriberi (B1), Pellegra (B3 / Niasin - 4D), Raşitizm (D vitamini).\n- **Bernardino Ramazzini (1700):** 'De Morbis Artificum Diatriba' ile iş sağlığının babasıdır; anamneze 'Ne iş yaparsınız?' sorusunu eklemiştir.\n- **Percivall Pott (1775):** Baca temizleyicilerinde ilk meslek kanserini (skrotum kanseri) tanımladı.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Öncü / Olay", "Yıl / Dönem", "Halk Sağlığı ve Tıp Alanındaki Yeri"],
                [
                    ["Kommodor Anson", "1740", "Mürettebatının %54'ünü skorbüte kurban veren tarihi felaket"],
                    ["James Lind", "1753", "Limon ve portakalla skorbütü yenen ilk kontrollü klinik deney"],
                    ["Bernardino Ramazzini", "1700", "İş sağlığının babası, 'Ne iş yaparsınız?' sorusu"],
                    ["Percivall Pott", "1775", "Baca temizleyicisi çocuklarda ilk mesleki skrotum kanseri"],
                    ["Gilbert Blane", "1795", "Donanmada limon suyunu zorunlu kılarak skorbütü bitiren hekim"]
                ]
            ),
            make_chain(
                "Beslenme ve İş Sağlığının Gelişim Çizgisi",
                [
                    "1. Anson Trajedisi: Skorbütün bir donanmayı yok edebilecek güçte olduğunun görülmesi.",
                    "2. Lind'in Narenciye Deneyi: Limonun koruyuculuğunun kontrollü deneyle ispatı.",
                    "3. Ramazzini ve İş Yeri: Hastalıkların yapılan işle ve çalışma ortamıyla bağının kurulması.",
                    "4. Fabrika Yasaları: Çocuk işçiliğinin yasaklanması ve iş sağlığının kamusal güvenceye alınması."
                ]
            )
        ]
    })

    # Slide 60
    slides.append({
        "id": "k1-18-s60",
        "title": "Bölüm Özeti: Sanayi Döneminden Sosyal Hekimliğe Geçiş",
        "content": "Bölüm 6 boyunca beslenme yetersizliklerinin bilimsel çözümünü ve çalışma yaşamının sağlık üzerindeki derin izlerini inceledik:\n\n- **Özet:** Lind skorbütü narenciyeyle çözdü, Ramazzini iş sağlığının temellerini attı; ancak hastalıkların köklerinin yalnızca biyolojik değil, sosyoekonomik olduğu giderek daha net anlaşıldı.\n- **Sonraki Bölüm (Bölüm 7):** Sağlığın toplumsal belirleyicilerini ele alan **Sosyal Hekimlik akımını, Alfred Grotjahn'ın kurallarını, Rudolf Virchow'u, 1948'de Dünya Sağlık Örgütü'nün (DSÖ) kuruluşunu ve toplum hekimliği modelini** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_recall(
                "1700 yılında yazdığı eserle hekimlere hastalarına mutlaka 'Ne iş yaparsınız?' diye sormalarını öğütleyen iş sağlığının babası kimdir?",
                "Bernardino Ramazzini",
                "İtalyan iş hekimliği öncüsü"
            ),
            make_quiz(
                "1747 yılında gemide skorbüt hastalarına limon ve portakal vererek tıp tarihinin ilk kontrollü klinik deneyini gerçekleştiren İskoç cerrah kimdir?",
                [
                    {"key": "A", "text": "James Lind", "isCorrect": True, "explanation": "Doğru cevap A'dır: James Lind skorbüt ve narenciye deneyiyle ilk kontrollü klinik araştırmayı yapmıştır."},
                    {"key": "B", "text": "John Snow", "isCorrect": False, "explanation": "Kolera araştırmacısıdır."},
                    {"key": "C", "text": "Edward Jenner", "isCorrect": False, "explanation": "Çiçek aşısını bulmuştur."},
                    {"key": "D", "text": "Louis Pasteur", "isCorrect": False, "explanation": "Kuduz aşısını bulmuştur."}
                ]
            )
        ]
    })

    return slides
