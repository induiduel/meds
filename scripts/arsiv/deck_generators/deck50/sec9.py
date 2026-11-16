from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec9():
    slides = []

    # Slide 81
    narrative_81 = """Treponemal (spesifik) testler, hastanın serumunda doğrudan *Treponema pallidum* yüzey antijenlerine karşı gelişmiş olan spesifik antikorları tespit etme prensibine dayanır. VDRL ve RPR gibi lipoidal (non-treponemal) testlerin aksine, burada hedeflenen yapı bakterinin kendisine aittir. Bu nedenle, treponemal testlerin özgüllüğü (spesifisitesi) oldukça yüksektir ve biyolojik yanlış pozitiflik oranları çok daha düşüktür.
*   **Prensip:** *T. pallidum* spesifik antikorlarının saptanması.
*   **Kullanım Amacı:** Tarama testleriyle (VDRL/RPR) saptanan pozitiflikleri doğrulamak.
*   **Örnek Testler:** TPHA, FTA-ABS, MHA-TP.
> Treponemal testler, lipitlere değil doğrudan bakteriyel antijenlere karşı oluşan antikorları ölçtükleri için enfeksiyon varlığını kesin olarak kanıtlamak amacıyla doğrulama testi olarak kullanılırlar.
"""
    slide_81 = make_slide(
        title="Treponemal (Spesifik) Testlerin Biyolojik Prensibi",
        narrative=narrative_81,
        elements=[
            make_cloze("Treponemal testler, hastanın serumunda {{c1::T. pallidum::bakteri}} antijenlerine karşı gelişmiş spesifik antikorları arar."),
            make_cloze("Non-treponemal testler (VDRL, RPR) doku hasarı lipitlerini saptarken, treponemal testler doğrudan {{c1::bakteriye::hedef}} özgüllük gösterir."),
            make_cloze("Treponemal testlerin temel kullanım amacı, pozitif çıkan tarama testlerini {{c1::doğrulamak}}tır."),
            make_recall("Treponemal testler ne tür bir antikoru saptar?", "Doğrudan Treponema pallidum yüzey antijenlerine karşı gelişen spesifik antikorları."),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Treponemal testlerin temel özellikleri.",
                "Treponemal testler yüksek oranda biyolojik yanlış pozitifliğe açıktır.",
                "Treponemal testlerin özgüllüğü oldukça yüksektir ve spesifik antikorları saptadıkları için genellikle doğrulama amacıyla kullanılırlar; biyolojik yanlış pozitiflik ihtimali lipoidal testlere kıyasla çok daha düşüktür.",
                [
                    "Treponemal testler doğrudan bakterinin kendisine ait hedefleri tespit eder.",
                    "VDRL gibi tarama testlerinin pozitifliğini doğrulamak için kullanılırlar.",
                    "TPHA ve FTA-ABS, bu test grubuna örnek olarak verilebilir."
                ]
            )
        ]
    )
    slides.append(slide_81)

    # Slide 82
    narrative_82 = """TPHA (Treponema Pallidum Hemaglütinasyon Testi), en sık kullanılan spesifik treponemal doğrulama testlerinden biridir. Testin temel mantığı, *T. pallidum* antijenleri ile kaplanmış olan eritrositlerin, hasta serumundaki spesifik treponemal antikorlarla bir araya geldiğinde kümelenme (hemaglütinasyon) göstermesidir.
*   **Avantajları:** Kolay uygulanabilir, ucuz, standardize edilmesi kolay ve yüksek özgüllüğe sahiptir.
*   **Zaman Çizelgesi:** Hastalığın başlangıcından birkaç hafta sonra pozitifleşir ve VDRL'den biraz daha geç saptanabilir hale gelir.
> Pratik ve ekonomik olması nedeniyle, özellikle otomatize sistemlerde RPR pozitifliğini doğrulamak için ilk basamak spesifik test olarak sıklıkla tercih edilir. Eritrositlerin çökme (kümelenme) paternine bakılarak sonuç okunur.
"""
    slide_82 = make_slide(
        title="TPHA (Treponema Pallidum Hemaglütinasyon) Testi",
        narrative=narrative_82,
        elements=[
            make_cloze("TPHA testinde, *T. pallidum* antijenleriyle kaplı {{c1::eritrositler::hücre}}, hasta serumundaki antikorlarla karşılaşınca {{c2::hemaglütinasyon::reaksiyon}} gösterir."),
            make_cloze("TPHA, sıklıkla VDRL/RPR sonuçlarını {{c1::doğrulamak}} için kullanılan spesifik bir testtir."),
            make_cloze("Hemaglütinasyon (kümelenme) görülmesi, testin {{c1::pozitif::sonuç}} olduğunu ifade eder."),
            make_chain("TPHA Testinin Prensipleri", [
                "Eritrositler bakteriyel antijenle kaplanır",
                "Hasta serumu eklenir",
                "Spesifik antikor varsa hemaglütinasyon gerçekleşir",
                "Pozitif doğrulama sonucu raporlanır"
            ]),
            make_quiz(
                "TPHA testi için aşağıdakilerden hangisi doğrudur?",
                [
                    "Antijenle kaplı eritrositlerin kümelenmesi esasına dayanır",
                    "Bir non-treponemal testtir",
                    "Sifiliz tedavisinin takibinde en değerli testtir",
                    "Testin pozitifliği sadece aktif enfeksiyonu gösterir"
                ],
                0,
                "TPHA, antikor varlığında eritrositlerin hemaglütinasyonuna dayanan spesifik bir treponemal testtir. Tedavi takibinde kullanılmaz ve ömür boyu pozitif kalabilir."
            )
        ]
    )
    slides.append(slide_82)

    # Slide 83
    narrative_83 = """FTA-ABS (Fluorescent Treponemal Antibody Absorption), en duyarlı (sensitif) ve sifiliz enfeksiyonunda *en erken yükselen (pozitifleşen)* serolojik testtir. 'Absorpsiyon' kelimesi, test yapılmadan önce hastanın serumunun zararsız (saprofit) diğer treponemalarla karşılaştırılarak non-spesifik antikorların emilip (absorbe edilip) uzaklaştırıldığını ifade eder.
*   **Yöntem:** İndirekt immünofloresan yöntemi kullanılır; floresan mikroskop altında parlayan spiroketler aranır.
*   **Zamanlama:** VDRL ve TPHA'dan bile önce pozitifleşir (genellikle şankr ortaya çıktıktan hemen sonra veya bazen ilk haftada).
> FTA-ABS, diğer testler henüz negatifken dahi şüpheli temas sonrası çok erken dönemde tanı koydurabilen 'altın standart' doğrulama testidir; ancak maliyetli ve emek yoğundur.
"""
    slide_83 = make_slide(
        title="FTA-ABS (Floresan Treponemal Antikor Absorbsiyonu) Testi",
        narrative=narrative_83,
        elements=[
            make_cloze("Sifiliz enfeksiyonunda pozitifleşen *ilk* serolojik test {{c1::FTA-ABS::test adı}} testidir."),
            make_cloze("FTA-ABS testindeki 'ABS' (absorpsiyon), testin özgüllüğünü artırmak için {{c1::saprofit::zararsız}} treponemalara karşı oluşan antikorların uzaklaştırılmasını belirtir."),
            make_cloze("Bu test {{c1::indirekt immünofloresan::yöntem}} prensibine göre çalışır ve mikroskop altında değerlendirilir."),
            make_recall("Sifiliz serolojisinde hangi test diğerlerinden daha erken pozitifleşir?", "FTA-ABS (Fluorescent Treponemal Antibody Absorption)."),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: FTA-ABS testi.",
                "FTA-ABS, VDRL'den aylar sonra pozitifleşen geç bir testtir.",
                "Tam tersine, FTA-ABS, sifilizde pozitifleşen EN ERKEN serolojik testtir; VDRL ve TPHA'dan bile önce pozitif hale gelir.",
                [
                    "İndirekt immünofloresan mikroskopi gerektiren emek yoğun bir testtir.",
                    "Saprofit treponemalara karşı gelişen antikorlar absorpsiyon işlemi ile uzaklaştırılır.",
                    "Primer şankr döneminde duyarlılığı oldukça yüksektir."
                ]
            )
        ]
    )
    slides.append(slide_83)

    # Slide 84
    narrative_84 = """Treponemal spesifik testlerin (TPHA, FTA-ABS) çok önemli bir klinik sınırlaması vardır: Başarılı bir tedavi sonrasında dahi serumda antikor titreleri düşmez. Hastalar tamamen iyileşse bile, treponemal antikorlar hastanın bağışıklık sisteminde bir 'hafıza' olarak kalır.
*   **Klinik Anlam:** Treponemal testlerin pozitifliği, hastanın 'şu an aktif sifiliz mi' yoksa 'geçmişte başarılı şekilde tedavi edilmiş bir hasta mı' olduğunu ayırt edemez.
*   **Kural:** Treponemal testler *tedavi takibinde KULLANILAMAZ.*
> "Bir kere treponemal, her zaman treponemal." deyişi, TPHA veya FTA-ABS testinin ömür boyu pozitif kaldığını vurgular. Tedaviye yanıtı ölçmek için mutlaka titre veren non-treponemal testler (VDRL/RPR) izlenmelidir.
"""
    slide_84 = make_slide(
        title="Treponemal Testlerin Ömür Boyu Pozitif Kalması",
        narrative=narrative_84,
        elements=[
            make_cloze("Sifiliz başarılı bir şekilde tedavi edilse bile, {{c1::treponemal::test grubu}} testler ömür boyu pozitif kalır."),
            make_cloze("Treponemal testler, hastanın aktif enfeksiyonu olup olmadığını göstermediğinden {{c1::tedavi takibinde::klinik kullanım}} kullanılamazlar."),
            make_cloze("Sifiliz tedavisinin başarısını ölçmek için, antikor titresi düşen {{c1::non-treponemal::test grubu}} testler (VDRL veya RPR) kullanılmalıdır."),
            make_table("Test Gruplarının Karşılaştırılması",
                ["Özellik", "Non-Treponemal (VDRL)", "Treponemal (FTA-ABS)"],
                [
                    ["Tedavi Sonrası", "Negatifleşir / Titre Düşer", "Ömür boyu pozitif kalır"],
                    ["Tedavi Takibi", "Kullanılır", "Kullanılmaz"],
                    ["Biyolojik Yalancı Pozitiflik", "Sık", "Nadir"]
                ]
            ),
            make_quiz(
                "Geçmişte sifiliz geçirmiş ve başarılı bir şekilde tedavi edilmiş bir hastada hangi serolojik tablonun görülmesi beklenir?",
                [
                    "VDRL negatif, TPHA pozitif",
                    "VDRL pozitif, TPHA negatif",
                    "Hem VDRL hem TPHA pozitif",
                    "Hem VDRL hem TPHA negatif"
                ],
                0,
                "Tedavi edilen hastada lipoidal antikorlar (VDRL) zamanla negatifleşirken (veya çok düşük titrede kalırken), spesifik treponemal antikorlar (TPHA) ömür boyu pozitif kalır."
            )
        ]
    )
    slides.append(slide_84)

    # Slide 85
    narrative_85 = """Klasik sifiliz serolojik tanı algoritması, iki basamaklı bir yaklaşımı gerektirir. Önce tarama, sonra doğrulama yapılır. Toplum taramalarında, duyarlılığı (sensitivitesi) yüksek ve ucuz olan non-treponemal testler (VDRL veya RPR) ilk basamak olarak kullanılır.
*   **Algoritma Adımları:**
    1.  İlk test VDRL/RPR'dir. Sonuç negatifse, erken enfeksiyon şüphesi yoksa sifiliz dışlanır.
    2.  İlk test (VDRL/RPR) *pozitifse*, biyolojik yalancı pozitiflik ihtimalini dışlamak için mutlaka bir *treponemal test* (TPHA veya FTA-ABS) ile doğrulanır.
> Geleneksel tanı algoritmasında hiçbir zaman tek başına VDRL pozitifliğine dayanarak kesin tanı konulmaz; TPHA/FTA-ABS doğrulaması şarttır. (Not: Ters algoritmalarda önce treponemal ile başlanabilir, ancak temel prensip yine iki testin uyumudur).
"""
    slide_85 = make_slide(
        title="Tanı Algoritması: Nontreponemal Tarama ve Treponemal Doğrulama",
        narrative=narrative_85,
        elements=[
            make_cloze("Klasik sifiliz tanı algoritmasında ilk olarak {{c1::VDRL veya RPR::tarama testi}} yapılır."),
            make_cloze("Tarama testinin pozitif gelmesi durumunda, kesin tanı için {{c1::TPHA veya FTA-ABS::doğrulama testi}} gibi spesifik bir test yapılmalıdır."),
            make_cloze("Yalnızca VDRL pozitifliğine dayanarak kesin tanı konulmaz çünkü {{c1::biyolojik yalancı pozitiflik::durum}} riski vardır."),
            make_chain("Klasik Sifiliz Tanı Algoritması", [
                "Hastadan alınan kan örneği",
                "Non-treponemal test (VDRL/RPR) uygulanması",
                "Testin pozitif çıkması",
                "Treponemal test (TPHA/FTA-ABS) ile doğrulama",
                "Kesin sifiliz tanısının konulması"
            ]),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Klasik tanı algoritması.",
                "RPR negatif gelen bir hastada enfeksiyonu dışlamak için mutlaka TPHA yapılmalıdır.",
                "Klasik algoritmada tarama testi (RPR/VDRL) negatif gelirse (ve çok erken/çok geç dönem şüphesi yoksa) sifiliz dışlanmış kabul edilir, rutin olarak doğrulama testi (TPHA) istenmez.",
                [
                    "Klasik algoritmada VDRL pozitifliği her zaman treponemal bir testle doğrulanmalıdır.",
                    "Tarama testleri duyarlılığı yüksek, nispeten ucuz testlerdir.",
                    "Doğrulama testlerinin temel amacı, otoimmünite veya gebelik gibi durumlara bağlı yalancı pozitiflikleri ayırt etmektir."
                ]
            )
        ]
    )
    slides.append(slide_85)

    # Slide 86
    narrative_86 = """Sifiliz tedavisinin köşe taşı ve altın standardı **Penisilin**'dir. *Treponema pallidum*, şaşırtıcı bir şekilde on yıllar boyunca penisiline karşı hiçbir direnç geliştirmemiş nadir bakterilerden biridir. Bakteri yavaş çoğaldığı için (bölünme süresi 30-33 saat), tedavininde kanda uzun süre etkili düzeyde kalabilen depo penisilin formları tercih edilir.
*   **Temel İlaç:** Benzatin Penisilin G (depo formdur, kas içine IM olarak uygulanır).
*   **Avantajı:** Tek bir doz uygulandığında bile haftalarca düşük ama etkili bir kan konsantrasyonu sağlayarak yavaş bölünen spiroketleri yok eder.
> Sifilizde tedavinin başarısızlık nedeni genellikle ilacın bakteriye etki etmemesi (direnç) değil, enfeksiyonun evresine uygun doz şemasının veya süresinin seçilmemesidir. Penisilin her evrede ilk seçenektir.
"""
    slide_86 = make_slide(
        title="Tedavi Temel Prensipleri ve Treponema'nın Penisilin Duyarlılığı",
        narrative=narrative_86,
        elements=[
            make_cloze("Sifiliz tedavisinde altın standart antimikrobiyal ajan {{c1::Penisilin::ilaç}}'dir."),
            make_cloze("*Treponema pallidum*, uzun yıllar geçmesine rağmen penisiline karşı {{c1::direnç::mekanizma}} geliştirmemiştir."),
            make_cloze("Bakteri yavaş çoğaldığı için tedavide genellikle uzun etkili olan {{c1::Benzatin Penisilin G::depo form}} kas içine (IM) tercih edilir."),
            make_recall("Sifilizde Penisilin neden hala en etkili tedavidir?", "Çünkü T. pallidum penisiline karşı günümüze dek hiçbir antimikrobiyal direnç geliştirmemiştir."),
            make_quiz(
                "Sifiliz tedavisinde uzun etkili depo penisilin formlarının (Benzatin Penisilin) tercih edilmesinin temel nedeni aşağıdakilerden hangisidir?",
                [
                    "Bakterinin hücre içi yerleşimi",
                    "Spiroketlerin kanda bulunmaması",
                    "Bakterinin çok yavaş çoğalması (bölünme süresinin uzun olması)",
                    "Hastaların hap yutmayı tercih etmemesi"
                ],
                2,
                "Treponema pallidum'un bölünme süresi uzundur (30 saati bulabilir). Hücre duvarı sentezi yavaş olduğundan, ilacın vücutta uzun süre etkili bir konsantrasyonda kalması gerekir."
            )
        ]
    )
    slides.append(slide_86)

    # Slide 87
    narrative_87 = """Erken dönem sifiliz; Primer (şankr), Sekonder (döküntüler) ve Erken Latent (enfeksiyonun üzerinden 1 yıldan az zaman geçmiş gizli dönem) evrelerini kapsar. Bu evrelerde spiroketler yoğun olsa da henüz geri dönüşsüz doku hasarı oluşmamıştır.
*   **Standart Tedavi:** Tek doz **Benzatin Penisilin G 2.4 milyon ünite**, intramüsküler (IM) yoldan uygulanır.
*   Bu doz, kanda yeterli inhibitör konsantrasyonu 2-3 hafta boyunca sağlayarak, erken dönemdeki yavaş çoğalan bakterilerin tamamını temizlemek için genellikle yeterlidir.
> Erken sifilizde hastanın tek bir iğne ile tamamen tedavi edilebilmesi, bu enfeksiyonun halk sağlığı açısından kontrolünü kolaylaştıran çok önemli bir özelliktir.
"""
    slide_87 = make_slide(
        title="Primer, Sekonder ve Erken Latent Sifiliz Tedavisi",
        narrative=narrative_87,
        elements=[
            make_cloze("Primer, sekonder ve erken latent sifilizde standart tedavi {{c1::Tek doz::uygulama sıklığı}} Benzatin Penisilin G uygulamasıdır."),
            make_cloze("Erken sifiliz için kullanılan Benzatin Penisilin G'nin dozu genellikle {{c1::2.4 milyon ünite::doz miktarı}} IM'dir."),
            make_cloze("Erken latent sifiliz, hastanın enfeksiyonu {{c1::1 yıldan::süre}} daha kısa bir süredir taşıdığı asemptomatik evredir."),
            make_table("Erken Sifiliz Tedavi Şeması",
                ["Evre", "İlaç", "Doz ve Yol", "Sıklık"],
                [
                    ["Primer Şankr", "Benzatin Penisilin G", "2.4 MÜ - IM", "Tek Doz"],
                    ["Sekonder Döküntü", "Benzatin Penisilin G", "2.4 MÜ - IM", "Tek Doz"],
                    ["Erken Latent (<1 yıl)", "Benzatin Penisilin G", "2.4 MÜ - IM", "Tek Doz"]
                ]
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Erken sifiliz tedavisi.",
                "Sekonder sifiliz tedavisinde Benzatin Penisilin G art arda 3 hafta boyunca yapılmalıdır.",
                "Sekonder sifiliz de tıpkı primer sifiliz gibi erken dönem kabul edilir ve tek doz 2.4 milyon ünite Benzatin Penisilin G (IM) tedavisi yeterlidir.",
                [
                    "Primer sifilizde tek doz intramüsküler depo penisilin standarttır.",
                    "Erken latent sifiliz enfeksiyonun bulaşmasından sonraki ilk bir yılı ifade eder ve tek doz ile tedavi edilebilir.",
                    "Erken evrede tedavi başarısı genellikle yüz güldürücüdür."
                ]
            )
        ]
    )
    slides.append(slide_87)

    # Slide 88
    narrative_88 = """Geç dönem sifiliz; Geç Latent (enfeksiyon süresi >1 yıl veya bilinmiyor), Gommatöz (benign tersiyer) ve Kardiyovasküler sifilizi içerir. Enfeksiyonun üzerinden uzun zaman geçtiği için tek bir depo doz spiroketleri tamamen temizlemeye yetmeyebilir.
*   **Standart Tedavi:** Benzatin Penisilin G 2.4 milyon ünite (IM), **haftada bir kez, arka arkaya 3 hafta boyunca** uygulanır. Toplam doz 7.2 milyon üniteye ulaşır.
*   **Amaç:** Penisilin kan düzeyini daha uzun süre (yaklaşık 1 ay) koruyarak, derin dokulara yerleşmiş ve çok daha yavaş bölünen gizli spiroketleri yok etmektir.
> Latent sifiliz teşhisi konan ancak enfeksiyonu ne zaman kaptığı bilinmeyen hastalara da güvenli tarafta kalmak adına daima "Geç Latent" muamelesi yapılıp 3 haftalık doz uygulanır.
"""
    slide_88 = make_slide(
        title="Geç Latent, Gommatöz ve Kardiyovasküler Sifiliz Tedavisi",
        narrative=narrative_88,
        elements=[
            make_cloze("Geç latent veya süresi bilinmeyen latent sifilizde, Benzatin Penisilin G haftada bir olmak üzere toplam {{c1::3 hafta::süre}} boyunca uygulanır."),
            make_cloze("Kardiyovasküler sifiliz ve gommatöz hastalık, tedavinin {{c1::uzatılmasını::değişiklik}} gerektiren geç dönem bulgularıdır."),
            make_cloze("Üç haftalık tedavide her seans için verilen Benzatin Penisilin dozu {{c1::2.4 milyon ünite::doz}}'dir."),
            make_recall("Süresi bilinmeyen asemptomatik sifiliz hastasında tedavi yaklaşımı ne olmalıdır?", "Geç latent sifiliz kabul edilerek haftada 1 dozdan ardışık 3 hafta Benzatin Penisilin G (IM) verilmelidir."),
            make_quiz(
                "Geç sifiliz evrelerinde (geç latent, gommatöz, kardiyovasküler) Benzatin Penisilin'in haftada bir kez 3 hafta uygulanmasının temel amacı nedir?",
                [
                    "Penisilin alerjisi riskini minimize etmek",
                    "İlacın kan beyin bariyerini geçmesini sağlamak",
                    "Kan penisilin seviyesini uzun süre sabit tutarak derin dokulardaki yavaş bölünen treponemaları yok etmek",
                    "Treponema pallidum'un penisilinaz üretmesini engellemek"
                ],
                2,
                "Geç dönemde organizmalar çok yavaş bölünür ve derin dokulara yerleşmiştir. Bakteriyi ortadan kaldırmak için etkili kan düzeyinin daha uzun süre (3 hafta/21-28 gün) korunması şarttır."
            )
        ]
    )
    slides.append(slide_88)

    # Slide 89
    narrative_89 = """Nörosifiliz, *T. pallidum*'un merkezi sinir sistemine istilasıdır. Depo etkili Benzatin Penisilin, Kan-Beyin Bariyeri'ni (KBB) yeterince geçemediğinden, beyin omurilik sıvısında (BOS) etkili treponemisidal konsantrasyonlara ulaşamaz. Bu sebeple nörosifilizde tedavi protokolü tamamen değişir.
*   **İlaç:** Sulu (Kısa Etkili) Kristalize Penisilin G.
*   **Yol ve Doz:** İntravenöz (IV), yüksek dozlarda (günde 18-24 milyon ünite, 4 saatte bir bölünerek).
*   **Süre:** Hastaneye yatışla birlikte 10-14 gün boyunca uygulanır.
> Nörosifiliz tanısında kural şudur: Depo kas iğneleri (Benzatin) BOS'a geçmez; MSS enfeksiyonunu tedavi etmek için mutlaka damardan, yüksek dozda ve sık aralıklarla sulu penisilin verilmelidir!
"""
    slide_89 = make_slide(
        title="Nörosifiliz Tedavi Protokolü",
        narrative=narrative_89,
        elements=[
            make_cloze("Nörosifiliz tedavisinde Benzatin Penisilin yerine {{c1::Kristalize::form}} Penisilin G tercih edilir."),
            make_cloze("Benzatin penisilinin nörosifilizde kullanılmamasının sebebi, {{c1::kan beyin bariyerini::anatomik yapı}} yeterince geçememesidir."),
            make_cloze("Nörosifilizde Kristalize Penisilin G, kas içine değil mutlaka {{c1::intravenöz (IV)::yol}} yolla uygulanır."),
            make_cloze("Nörosifiliz tedavisi hastane yatışıyla genellikle {{c1::10-14 gün::süre}} devam eder."),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Nörosifiliz tedavisi.",
                "Nörosifiliz tanısı alan bir hastaya tek doz yüksek doz Benzatin Penisilin G (IM) yapılıp taburcu edilir.",
                "Benzatin Penisilin G kan-beyin bariyerini geçemez; bu nedenle nörosifiliz mutlaka hastanede yatarak 10-14 gün boyunca IV Kristalize Penisilin G ile tedavi edilmelidir.",
                [
                    "Kristalize Penisilin G intravenöz yolla ve sık aralıklarla (örneğin 4 saatte bir) verilir.",
                    "Tedavi süresi kural olarak en az 10-14 gün olarak planlanır.",
                    "Amaç beyin omurilik sıvısında yüksek treponemisidal ilaç konsantrasyonuna ulaşmaktır."
                ]
            )
        ]
    )
    slides.append(slide_89)

    # Slide 90
    narrative_90 = """[TEKRAR SAYFASI - CHECKPOINT 9]
Bu bölümde sifilizin doğrulama testleri ve tedavi şemalarını inceledik.
1.  **Treponemal Testler:** TPHA ve FTA-ABS (en erken pozitifleflen testtir). Ömür boyu pozitif kalırlar, hastalık aktivitesini göstermezler, tedavi takibinde KULLANILAMAZLAR.
2.  **Klasik Tanı:** Önce tarama (VDRL), sonra doğrulama (TPHA/FTA-ABS).
3.  **Temel İlaç:** *T. pallidum* penisiline dirençsizdir.
4.  **Erken Dönem Tedavi:** (Primer, Sekonder, Erken Latent): Tek doz IM Benzatin Penisilin 2.4 MU.
5.  **Geç Dönem Tedavi:** (Geç Latent, KV, Gommatöz): Haftada 1 dozdan, toplam 3 doz IM Benzatin Penisilin.
6.  **Nörosifiliz Tedavisi:** BOS'a geçebilmesi için 10-14 gün boyunca IV Kristalize Penisilin.
"""
    slide_90 = make_slide(
        title="[TEKRAR SAYFASI - CHECKPOINT 9] Treponemal Testler ve Tedavi Şemaları",
        narrative=narrative_90,
        elements=[
            make_cloze("Sifilizde en erken pozitifleşen ve en duyarlı treponemal test {{c1::FTA-ABS::test}}'dir."),
            make_cloze("Başarılı bir tedavi sonrasında VDRL titresi düşerken, TPHA gibi testler ömür boyu {{c1::pozitif::sonuç}} kalır."),
            make_cloze("Sekonder sifilizin standart tedavisi {{c1::tek doz::sıklık}} Benzatin Penisilin uygulamasıdır."),
            make_cloze("Nörosifilizde ilacın BOS'a geçebilmesi için mutlaka {{c1::intravenöz::yol}} yoldan Kristalize Penisilin verilmelidir."),
            make_table("Sifiliz Evreleri ve Tedavi Özet Tablosu",
                ["Klinik Evre", "İlaç Tercihi", "Uygulama Yolu ve Süresi"],
                [
                    ["Primer / Sekonder / Erken Latent", "Benzatin Penisilin G", "Tek Doz, İntramüsküler"],
                    ["Geç Latent / Tersiyer (Kardiyovasküler)", "Benzatin Penisilin G", "Haftada 1 kez (3 Hafta), İntramüsküler"],
                    ["Nörosifiliz", "Kristalize Penisilin G", "4 saatte bir (10-14 Gün), İntravenöz"]
                ]
            )
        ]
    )
    slides.append(slide_90)

    return slides
