"""
Kromozomal Hastalıklar ve Genetik Danışma (Ders 10) - Bölüm 9 (Slayt 81 - 90)
Konu: Genomik İmprinting, Uniparental Dizomi (UPD), Prader-Willi ve Angelman Sendromları
Checkpoint: Slayt 89 ([TEKRAR SAYFASI - CHECKPOINT 9])
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_9_slides():
    return [
        # Slayt 81
        {
            "title": "Genomik İmprinting (Damgalama) Kavramı ve Epigenetik Modifikasyonlar",
            "subtitle": "Mendel Kalıtımının İstisnası: Ebeveyn Kökenine Bağımlı Gen Ekspresyonu",
            "badge": "Genomik İmprinting",
            "coreContent": {
                "text": "Klasik Mendel genetiğinde bir genin anneden veya babadan kalıtılmış olması onun ekspresyon düzeyini etkilemez; her iki ebeveyn aleli de eşit kabul edilir. Ancak insan genomundaki yaklaşık 100-200 gende bu kural geçersizdir. Genomik imprinting (damgalama), bir genin transkripsiyonel aktivitesinin o genin hangi ebeveynden kalıtıldığına bağlı olarak kalıcı şekilde susturulması (sessizleştirilmesi) fenomenidir. İmprinting, DNA baz dizilimini değiştirmeyen kalıtsal epigenetik modifikasyonlarla (spesifik CpG adacıklarının DNA metiltransferazlarca metillenmesi ve histon deasetilasyonu) yönetilir. Gametogenez sırasında paternal veya maternal germ hattında kurulan bu metilasyon damgası, döllenme sonrasında embriyonik dokularda korunur. Eğer bir gen 'maternal imprint' edilmişse, anneden gelen kopya metillenerek susturulmuştur ve o gen yalnız babadan gelen alel üzerinden okunur; tersi durumda paternal kopyanın susturulduğu genler yalnız anneden ifade edilir.",
                "keyBullets": [
                    {"title": "Mendel Kalıtımı İstisnası", "desc": "Genin fonksiyonu ebeveyn kökenine bağlıdır; bir ebeveyn aleli epigenetik olarak susturulur.", "isKey": True},
                    {"title": "Epigenetik Mekanizma", "desc": "DNA dizi değişimi olmaksızın CpG metilasyonu ve histon modifikasyonu ile kurulur.", "isKey": True},
                    {"title": "Monoalelik Ekspresyon", "desc": "Hücrede iki kopyadan yalnız tek bir ebeveyne ait alel fonksiyonel protein üretir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Mendel Kalıtımı vs Genomik İmprinting",
                    "Klasik Mendel Kalıtımı",
                    "Her iki ebeveyn aleli de eşit aktiftir; genin anneden mi babadan mı geldiği fonksiyonu değiştirmez (bialelik ekspresyon).",
                    "Genomik İmprinting Modeli",
                    "Bir ebeveyn aleli gametogenezde epigenetik olarak (metilasyonla) susturulur; yalnız tek ebeveyn aleli okunur (monoalelik ekspresyon)."
                ),
                make_cloze(
                    "Genomik imprinting sürecinde bir alelin transkripsiyonel olarak susturulmasını sağlayan temel epigenetik mekanizma DNA metilasyonudur.",
                    "metilasyonu",
                    "Temel epigenetik kovalent modifikasyonu anımsayınız"
                ),
                make_active_recall(
                    "Bir gen maternal olarak imprint edilmiş (damgalanmış ve susturulmuş) ise, normal bir bireyin somatik hücrelerinde bu gen hangi ebeveynden gelen kopyadan transkribe edilir?",
                    "Yalnızca babadan (paternal kopyadan) transkribe edilir; anneden gelen kopya sessizdir.",
                    "Maternal susturulma paternal ekspresyon kuralı"
                )
            ],
            "spotPearls": [
                "Genomik imprinting: Gen ekspresyonunun ebeveyn kökenine göre belirlenmesidir.",
                "DNA baz dizisi DEĞİŞMEZ; susturulma DNA metilasyonu ile gerçekleşir.",
                "İmprinting Mendel kalıtımının klasik monoalelik istisnalarındandır."
            ]
        },

        # Slayt 82
        {
            "title": "15q11-q13 Bölgesinin Genomik Mimarisi ve İmprinting Merkezi",
            "subtitle": "Prader-Willi ve Angelman Lokusunun Bipolar Epigenetik Düzeni",
            "badge": "15q11-q13 Genomik Mimarisi",
            "coreContent": {
                "text": "15. kromozomun uzun kolunda yer alan 15q11-q13 bölgesi, insan tıbbi genetiğinde imprinting mekanizmasının en kusursuz ve klinik önemi en yüksek modelidir. Bu yaklaşık 4-6 megabazlık (Mb) genomik bölge, düşük kopya tekrarlarıyla (BP1, BP2, BP3 kırık noktaları) çevrili olup mayotik dengesizliklere son derece açıktır. 15q11-q13 bölgesinde iki zıt kutupta çalışan gen kümeleri bulunur: (1) Paternal olarak ifade edilen (anneden imprint edilip susturulan) genler: SNRPN (küçük nükleer ribonükleoprotein N), MKRN3, MAGEL2 ve snoRNA gen kümesidir (özellikle SNORD116). Bu genler yalnız babadan gelen 15. kromozomdan çalışır. (2) Maternal olarak ifade edilen (babadan imprint edilip susturulan) gen: UBE3A (ubikitin-protein ligaz E3A) genidir; özellikle nöronlarda paternal kopya susturulur ve yalnız anneden gelen kopya aktiftir. Bölgenin epigenetik şalteri ise İmprinting Merkezi (IC) tarafından yönetilir.",
                "keyBullets": [
                    {"title": "15q11-q13 Bölgesi", "desc": "Prader-Willi ve Angelman sendromlarının ortak kritik kromozomal lokusudur.", "isKey": True},
                    {"title": "Paternal Genler (PWS)", "desc": "SNRPN ve snoRNA genleridir; normalde yalnız babadan gelen kromozomdan okunur.", "isKey": True},
                    {"title": "Maternal Gen (AS)", "desc": "UBE3A ubikitin ligaz genidir; nöronlarda yalnız anneden gelen kromozomdan okunur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Kromozom 15q11-q13 Geni", "Aktif Olduğu Ebeveyn Kopyası", "Susturulduğu (İmprint) Ebeveyn", "Eksikliğinde Gelişen Sendrom"],
                    [
                        [("SNRPN ve snoRNA kümesi", False, ""), ("Paternal Kopya (Babadan gelen)", True, "Babadan aktif genler"), ("Maternal kopya susturulur", False, ""), ("Prader-Willi Sendromu (PWS)", False, "")],
                        [("UBE3A (Ubikitin Ligaz)", False, ""), ("Maternal Kopya (Anneden gelen)", True, "Anneden aktif gen"), ("Paternal kopya nöronlarda susturulur", False, ""), ("Angelman Sendromu (AS)", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "15q11-q13 bölgesinde yer alan genlerden hangisi beyin nöronlarında yalnızca maternal (anneden gelen) kromozomdan ifade edilirken, paternal kopyası imprinting ile susturulmuştur?",
                    {
                        "A": "SNRPN",
                        "B": "UBE3A",
                        "C": "MAGEL2",
                        "D": "MKRN3",
                        "E": "NDN (Necdin)"
                    },
                    "B",
                    {
                        "A": "SNRPN paternalden ifade edilir.",
                        "B": "Doğru cevap B'dir: UBE3A geni nöronlarda paternal olarak susturulur ve yalnız maternal kromozomdan ifade edilir (kaybı Angelman yapar).",
                        "C": "MAGEL2 paternaldir.",
                        "D": "MKRN3 paternaldir.",
                        "E": "NDN paternaldir."
                    }
                ),
                make_cloze(
                    "15q11-q13 bölgesinde yer alan UBE3A geni nöronlarda yalnızca maternal kromozom üzerinden ifade edilir.",
                    "maternal",
                    "UBE3A'nın aktif olduğu ebeveyn kökenini yazınız"
                )
            ],
            "spotPearls": [
                "15q11-q13 bölgesi Prader-Willi ve Angelman sendromlarının ortak lokusudur.",
                "Paternal genler: SNRPN, snoRNA kümesi (kaybı Prader-Willi sendromu yapar).",
                "Maternal gen: UBE3A ubikitin ligaz (kaybı Angelman sendromu yapar)."
            ]
        },

        # Slayt 83
        {
            "title": "Uniparental Dizomi (UPD): Tanım, İzodizomi ve Heterodizomi",
            "subtitle": "Kromozom Çiftinin Tek Ebeveynden Kalıtılması Fenomeni",
            "badge": "Uniparental Dizomi",
            "coreContent": {
                "text": "Uniparental Dizomi (UPD), diploid (46 kromozomlu) bir bireyde, homolog kromozom çiftlerinden birinin her iki kopyasının da tek bir ebeveynden kalıtılması, diğer ebeveynden o kromozoma ait hiçbir kopyanın alınamaması durumudur. Normalde birey her homolog çiftten birini anneden, birini babadan alır. UPD iki alt tipe ayrılır: (1) Heterodizomi (Heterodisomy): Mayoz I ayrılamaması sonucu ortaya çıkan anormal gamet kaynaklıdır; birey aynı ebeveynin İKİ FARKLI homolog kromozomunu birden alır (heterozigotluk korunur). (2) İzodizomi (Isodisomy): Mayoz II ayrılamaması veya post-zigotik kromozom duplikasyonu kaynaklıdır; birey tek bir ebeveyne ait TEK BİR kromatitin tamamen özdeş iki kopyasını alır (tüm kromozom boyunca tam homozigotluk oluşur). İzodizomi, taşıyıcı ebeveynde bulunan nadir bir otozomal resesif mutasyonun (örneğin kistik fibrozis) çocukta homozigot hale gelerek tek ebeveynden resesif hastalık çıkmasına yol açabilir.",
                "keyBullets": [
                    {"title": "UPD Tanımı", "desc": "Kromozom çiftinin tamamının tek ebeveynden alınması, diğerinden hiç alınmamasıdır.", "isKey": True},
                    {"title": "Heterodizomi", "desc": "Aynı ebeveynin iki farklı homoloğu alınır (Mayoz I hatası; heterozigotluk korunur).", "isKey": True},
                    {"title": "İzodizomi", "desc": "Aynı ebeveyn kromatitinin ikiz kopyası alınır (Mayoz II hatası; resesif hastalık riski).", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Heterodizomi vs İzodizomi Mekanizması",
                    "Heterodizomi (Mayoz I Kökenli)",
                    "Aynı ebeveyne ait iki farklı homolog kromozom alınır; sentromerik belirteçler için heterozigotluk korunur.",
                    "İzodizomi (Mayoz II Kökenli)",
                    "Aynı ebeveyne ait tek bir kromatitin iki özdeş kopyası alınır; sentromerik belirteçler tamamen homozigottur."
                ),
                make_cloze(
                    "Tek bir ebeveyne ait özdeş kromatitin duplikasyonu ile oluşan ve tüm kromozom boyunca homozigotluğa yol açan uniparental dizomi tipine izodizomi denir.",
                    "izodizomi",
                    "Homozigot UPD tipini anımsayınız"
                ),
                make_active_recall(
                    "İzodizomi (isodisomy) mekanizması imprinting hastalıklarının yanı sıra hangi kalıtım modelindeki hastalıkların beklenmedik şekilde tek ebeveyn üzerinden ortaya çıkmasına neden olabilir?",
                    "Otozomal resesif hastalıkların (örneğin Kistik Fibrozis, Spinal Müsküler Atrofi) tek ebeveyn taşıyıcılığıyla çocukta homozigotlaşmasına neden olabilir.",
                    "Resesif hastalık homozigotlaşma riski"
                )
            ],
            "spotPearls": [
                "Uniparental Dizomi (UPD): Bir kromozom çiftinin her iki kopyasının tek ebeveynden gelmesidir.",
                "Heterodizomi: Ebeveynin iki farklı homoloğu (Mayoz I); heterozigotluk korunur.",
                "İzodizomi: Ebeveynin özdeş kromatit kopyası (Mayoz II); resesif hastalıkları homozigotlaştırabilir."
            ]
        },

        # Slayt 84
        {
            "title": "Trizomi Kurtarma (Trisomy Rescue) ve UPD Oluşum Yolları",
            "subtitle": "Anöploid Zigotun Mitotik Düzeltimi ve İki Ebeveyn Kuralının Bozulması",
            "badge": "Trizomi Kurtarma",
            "coreContent": {
                "text": "Uniparental dizominin (UPD) embriyogenezde ortaya çıkışındaki en yaygın ve iyi tanımlanmış mekanizma 'Trizomi Kurtarma'dır (trisomy rescue). Süreç şöyle işler: Mayotik bir ayrılamama sonucu normalde embriyonik letaliteye yol açacak trizomik bir zigot (örneğin Trizomi 15 konsepsiyonu; 2 anne, 1 baba kopyası) oluşur. Erken embriyonik mitoz bölünmeler sırasında hücre genomik stresi algılar ve anafazda geri kalma (anaphase lagging) yoluyla bu üç kromozomdan birini rastgele sitoplazmaya atarak hücreyi normal diploid (46 kromozom) sayıya döndürür. Bu kurtarma sırasında atılan kromozom tek olan babaya ait kopya olursa, geride kalan iki kopya da anneye ait olur ve hücre normal diploid görünümde 'Maternal Uniparental Dizomi' (mUPD15) kazanır (üçte bir olasılık). İkinci yol ise monozomik bir zigotun tek kalan kromozomunu mitozda duplike ederek diploidleştiği 'Monozomi Kurtarma'dır (tam izodizomi üretir).",
                "keyBullets": [
                    {"title": "Trizomi Kurtarma", "desc": "Trizomik zigotun anafazda geri kalma ile 3 kromozomdan birini atıp diploidleşmesidir.", "isKey": True},
                    {"title": "UPD Olasılığı", "desc": "Trizomi kurtarmada tek ebeveyn kopyası atılırsa 1/3 olasılıkla UPD gelişir.", "isKey": True},
                    {"title": "Monozomi Kurtarma", "desc": "Monozomik zigotun tek kromozomunu duplike ederek izodizomi oluşturmasıdır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Trizomi Kurtarma ve Maternal UPD 15 Zinciri",
                    [
                        "1. Maternal mayotik ayrılamama sonucu disomik oosit normal spermle döllenir (Trizomi 15 zigotu)",
                        "2. Zigotta 2 maternal ve 1 paternal 15. kromozom bulunur (letal anöploidi)",
                        "3. Erken embriyonik mitozda anafaz gecikmesiyle babadan gelen tekil 15. kromozom hücreden atılır",
                        "4. Embriyo 46 kromozomla kurtulur ancak her iki 15. kromozom da anneden kalır (Maternal UPD15)"
                    ]
                ),
                make_cloze(
                    "Trizomik bir zigotun erken mitozda ekstra kromozomlardan birini dışarı atarak diploid karyotipe dönmesi mekanizmasına trizomi kurtarma adı verilir.",
                    "trizomi kurtarma",
                    "Anöploidi onarım mekanizması terimini anımsayınız"
                ),
                make_active_recall(
                    "2 maternal ve 1 paternal kopya içeren trizomik bir zigotta rastgele gerçekleşen trizomi kurtarma olayı sonucunda maternal UPD gelişme teorik olasılığı kaçtır?",
                    "Üçte bir (1/3; %33.3) olasılıktır (çünkü 3 kromozomdan paternal olanın atılma şansı 1/3'tür).",
                    "Paternal kopyanın atılma olasılığı"
                )
            ],
            "spotPearls": [
                "UPD en sık trizomi kurtarma (trisomy rescue) mekanizmasıyla oluşur.",
                "Trizomik hücre anafaz gecikmesiyle tek ebeveyn kopyasını atarsa 1/3 olasılıkla UPD gelişir.",
                "Monozomi kurtarma ise tek kromatitin çiftlenmesiyle tam izodizomi üretir."
            ]
        },

        # Slayt 85
        {
            "title": "Prader-Willi Sendromu (PWS): Paternal 15q11-q13 Kaybı ve SNRPN",
            "subtitle": "Etiyolojik Dağılım: Paternal Delesyon (%70) ve Maternal UPD (%30)",
            "badge": "Prader-Willi Etiyolojisi",
            "coreContent": {
                "text": "Prader-Willi sendromu (PWS), 15. kromozomun 15q11-q13 bölgesinde yer alan ve normal koşullarda yalnız babadan gelen kromozomdan aktif olarak ifade edilen genlerin (SNRPN, snoRNA kümesi / SNORD116, MAGEL2) ekspresyonunun tamamen yokluğu sonucu gelişen nörogenetik bir hastalıktır. Canlı doğumlardaki görülme sıklığı yaklaşık 1/15.000 ila 1/25.000 arasındadır. PWS etiyolojisinde iki ana sitogenetik mekanizma sorumludur: (1) Olguların yaklaşık %70'inde paternal 15q11-q13 bölgesinde de novo mikrodelesyon mevcuttur (babadan gelen aktif kopyalar fiziksel olarak silinmiştir). (2) Olguların yaklaşık %25-30'unda Maternal Uniparental Dizomi (mUPD15) mevcuttur (bireyde her iki 15. kromozom da anneden kalıtılmıştır; anne kopyaları imprinting ile zaten susturulmuş olduğundan aktif gen kalmaz). Olguların <%1'inde ise imprinting merkez mutasyonu bulunur. Tanıda DNA metilasyon analizi tüm etiyolojik tipleri %99 yakalar.",
                "keyBullets": [
                    {"title": "Paternal Gen Yokluğu", "desc": "PWS, babadan gelen aktif 15q11-q13 genlerinin (SNRPN vb.) bulunmamasıdır.", "isKey": True},
                    {"title": "Paternal Delesyon (%70)", "desc": "En sık etiyolojik nedendir; babadan gelen parçanın silinmesidir.", "isKey": True},
                    {"title": "Maternal UPD (%30)", "desc": "İkinci sık nedendir; iki adet 15 de anneden gelir, baba kopyası yoktur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Etiyolojik Mekanizma", "PWS'deki Görülme Oranı", "Moleküler / Sitogenetik Durum", "Tekrarlama Riski"],
                    [
                        [("Paternal 15q11-q13 Delesyonu", False, ""), ("~%70 (En sık neden)", True, "Babadan gelen kolda delesyon"), ("De novo 5 Mb mikrodelesyon", False, ""), ("Çok düşük (<%1)", False, "")],
                        [("Maternal Uniparental Dizomi (mUPD15)", False, ""), ("~%25 - 30 (İkinci en sık)", True, "İki kromozom da anneden"), ("Trizomi kurtarma kaynaklı", False, ""), ("Çok düşük (<%1)", False, "")],
                        [("İmprinting Merkez Mutasyonu", False, ""), ("~%1 - 2", False, ""), ("Epigenetik şalter arızası", False, ""), ("Yüksek olabilir (%50'ye varan)", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Prader-Willi sendromunun genetik etiyolojisi incelendiğinde aşağıdaki mekanizma ve oran eşleştirmelerinden hangisi DOĞRUDUR?",
                    {
                        "A": "Maternal delesyon (%70) — Paternal UPD (%30)",
                        "B": "Paternal delesyon (%70) — Maternal UPD (%30)",
                        "C": "Paternal duplikasyon (%70) — Maternal delesyon (%30)",
                        "D": "Maternal trizomi (%95) — Paternal delesyon (%5)",
                        "E": "Yalnızca X kromozomu mutasyonları (%100)"
                    },
                    "B",
                    {
                        "A": "Maternal delesyon Angelman sendromunun nedenidir.",
                        "B": "Doğru cevap B'dir: Prader-Willi sendromunun yaklaşık %70'i paternal 15q11-q13 delesyonu, yaklaşık %25-30'u ise maternal UPD kaynaklıdır.",
                        "C": "Duplikasyon değildir.",
                        "D": "Trizomi değildir.",
                        "E": "Otozomal 15. kromozomdur."
                    }
                ),
                make_cloze(
                    "Prader-Willi sendromu olgularının yaklaşık %70'inden paternal 15q11-q13 mikrodelesyonu sorumludur.",
                    "%70",
                    "Paternal delesyon görülme yüzdesini düşününüz"
                )
            ],
            "spotPearls": [
                "Prader-Willi sendromu = PATERNAL 15q11-q13 ekspresyonunun kaybıdır.",
                "Etiyoloji: %70 paternal delesyon, %30 maternal UPD15.",
                "Tanıda altın standart tarama testi DNA metilasyon analizidir (%99 tanısal duyarlılık)."
            ]
        },

        # Slayt 86
        {
            "title": "Prader-Willi Sendromunda İki Evreli Klinik: İnfantil Hipotoni ve Hiperfaji",
            "subtitle": "Beslenme Güçlüğünden Doyumsuz İştaha, Morbid Obezite ve Hipogonadizm",
            "badge": "PWS Klinik Spektrumu",
            "coreContent": {
                "text": "Prader-Willi sendromunun klinik tablosu çocukluk çağında birbiriyle taban tabana zıt iki belirgin evre sergiler: (1) İnfantil Evre (0-2 yaş): Doğumda son derece ağır genel kas hipotonisi ('bez bebek'), zayıf emme, yutma güçlüğü ve beslenme yetersizliği (failure to thrive) ile karakterizedir; bebekler nazogastrik tüple beslenmek zorunda kalır. Erkek bebeklerde mikropenis, hipoplastik skrotum ve inmemiş testis (kriptorşidizm) gibi hipogonadotropik hipogonadizm bulguları saptanır. (2) Çocukluk ve Erişkin Evresi (2-3 yaştan itibaren): Hipotalamik tokluk merkezinin işlevsizleşmesi ve dolaşımdaki 'ghrelin' açlık hormonunun aşırı yükselmesiyle inatçı, doyumsuz bir yeme dürtüsü (hiperfaji) başlar. Çocuklar kilitli buzdolaplarını kırarak yemek ararlar; kontrolsüz gıda alımı hızla morbid obeziteye, obstrüktif uyku apnesine, Tip 2 diyabete ve kardiyopulmoner yetmezliğe yol açar. Badem gözler, dar alın, küçük el ve ayaklar tipiktir.",
                "keyBullets": [
                    {"title": "1. Evre (İnfantil)", "desc": "Ağır kas hipotonisi, zayıf emme, beslenememe ve kriptorşidizm.", "isKey": True},
                    {"title": "2. Evre (Hiperfaji)", "desc": "Doyumsuz yeme arzusu, açlık hissi (ghrelin artışı), morbid obezite ve diyabet.", "isKey": True},
                    {"title": "Fiziksel Stigmalar", "desc": "Badem şeklinde gözler, dar alın, ince üst dudak, küçük eller ve ayaklar.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Prader-Willi Sendromunun İki Zıt Klinik Evresi",
                    "Evre 1: İnfantil Dönem (0 - 2 Yaş)",
                    "Ağır kas hipotonisi, emme ve yutma yetersizliği, büyüme geriliği, nazogastrik beslenme ihtiyacı, mikropenis.",
                    "Evre 2: Çocukluk ve Erişkinlik (2+ Yaş)",
                    "Doyumsuz iştah (hiperfaji), yemek çalma, morbid obezite, Tip 2 diyabet, hipogonadotropik hipogonadizm, hafif zekâ geriliği."
                ),
                make_cloze(
                    "Prader-Willi sendromlu çocuklarda 2-3 yaşından sonra hipotalamik tokluk merkezinin disfonksiyonuna bağlı gelişen kontrolsüz doyumsuz yeme dürtüsüne hiperfaji denir.",
                    "hiperfaji",
                    "Aşırı doyumsuz yeme tıbbi terimini anımsayınız"
                ),
                make_active_recall(
                    "Prader-Willi sendromlu bireylerde bebeklik döneminde genital muayenede saptanan ve hipogonadotropik hipogonadizme işaret eden klasik erkek bulguları nelerdir?",
                    "Kriptorşidizm (inmemiş testis), mikropenis ve hipoplastik skrotumdur.",
                    "PWS erkek genital stigmaları"
                )
            ],
            "spotPearls": [
                "Prader-Willi iki evrelidir: Bebeklikte ağır hipotoni/emememe; 2 yaştan sonra HİPERFAJİ ve morbid obezite.",
                "Badem gözler, küçük el-ayaklar ve hipogonadizm karakteristiktir.",
                "Ghrelin hormonu aşırı yüksektir; ölümün en sık nedeni obezite komplikasyonlarıdır."
            ]
        },

        # Slayt 87
        {
            "title": "Angelman Sendromu (AS): Maternal 15q11-q13 Kaybı ve UBE3A",
            "subtitle": "Etiyolojik Dağılım: Maternal Delesyon (%70) ve Paternal UPD (%3-5)",
            "badge": "Angelman Etiyolojisi",
            "coreContent": {
                "text": "Angelman sendromu (AS), 15q11-q13 bölgesinde yer alan ve normal koşullarda beyin nöronlarında yalnız anneden gelen kromozomdan aktif olarak ifade edilen UBE3A (Ubikitin-Protein Ligaz E3A) geninin işlev kaybı sonucu gelişen ağır bir nörogelişimsel sendromdur. UBE3A proteini, sinapslarda protein turnoverını ve nöronal plastisiteyi denetleyen kritik bir E3 ubikitin ligazdır. Paternal kopya nöronlarda imprinting ile doğal olarak susturulduğu için, maternal UBE3A kaybedildiğinde beyinde hiç fonksiyonel protein üretilemez. Angelman sendromunun etiyolojik dağılımı şöyledir: (1) Olguların yaklaşık %70'inde maternal 15q11-q13 mikrodelesyonu saptanır (en ağır seyirli gruptur). (2) Olguların %10'unda doğrudan UBE3A gen mutasyonları mevcuttur. (3) Olguların yaklaşık %3-5'inde Paternal Uniparental Dizomi (pUPD15) bulunur (iki kromozom da babadandır). (4) Olguların %2-4'ünde imprinting merkez defekti vardır.",
                "keyBullets": [
                    {"title": "Maternal UBE3A Yokluğu", "desc": "AS, anneden gelen aktif UBE3A ubikitin ligaz geninin beyinde bulunmamasıdır.", "isKey": True},
                    {"title": "Maternal Delesyon (%70)", "desc": "En sık nedendir; anneden gelen 15q11-q13 bölgesinin mikrodelesyonudur.", "isKey": True},
                    {"title": "Paternal UPD (%3-5)", "desc": "PWS'deki %30'un aksine AS'de paternal UPD çok daha nadirdir (~%3-5).", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Etiyolojik Mekanizma", "Angelman Sendromundaki Oranı", "Kritik Gen Durumu"],
                    [
                        [("Maternal 15q11-q13 Delesyonu", False, ""), ("~%70 (En yaygın neden)", True, "Maternal delesyon oranı"), ("UBE3A ve komşu genler fiziksel olarak silinmiştir", False, "")],
                        [("UBE3A Nokta Mutasyonu", False, ""), ("~%10", True, "Tek gen dizi mutasyonu"), ("Delesyon yoktur; UBE3A fonksiyonunu bozan mutasyon", False, "")],
                        [("Paternal Uniparental Dizomi (pUPD15)", False, ""), ("~%3 - 5", True, "Babadan çift kopya"), ("Her iki 15 de babadandır; maternal UBE3A yoktur", False, "")],
                        [("İmprinting Merkez Kusuru", False, ""), ("~%2 - 4", False, ""), ("Maternal alel paternal gibi yanlış damgalanmıştır", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "Angelman sendromu etiyolojisinde yer alan genetik mekanizmalar ve oranlar incelendiğinde Paternal Uniparental Dizominin (pUPD15) payı yaklaşık yüzde kaçtır?",
                    {
                        "A": "Yaklaşık %1",
                        "B": "Yaklaşık %3-5",
                        "C": "Yaklaşık %30",
                        "D": "Yaklaşık %70",
                        "E": "Yüzde 100"
                    },
                    "B",
                    {
                        "A": "%1 çok düşüktür.",
                        "B": "Doğru cevap B'dir: Angelman sendromunda paternal UPD oranı yalnızca yaklaşık %3-5'tir (Prader-Willi'deki maternal UPD oranı ise %30'dur).",
                        "C": "%30 Prader-Willi'deki maternal UPD sıklığıdır.",
                        "D": "%70 maternal delesyon oranıdır.",
                        "E": "Yalnız tek neden değildir."
                    }
                ),
                make_cloze(
                    "Angelman sendromunda nöronal sinaps gelişimini denetleyen ve yokluğunda hastalığa yol açan kritik enzim UBE3A ubikitin ligazdır.",
                    "UBE3A",
                    "Angelman'dan sorumlu ubikitin ligaz gen adını yazınız"
                )
            ],
            "spotPearls": [
                "Angelman sendromu = MATERNAL UBE3A geninin kaybıdır.",
                "Etiyoloji: %70 maternal delesyon, %10 UBE3A mutasyonu, %3-5 paternal UPD15.",
                "Prader-Willi paternal delesyon iken, Angelman maternal delesyon tablosudur."
            ]
        },

        # Slayt 88
        {
            "title": "Angelman Sendromunda Klinik Tablo: 'Mutlu Kukla' (Happy Puppet) Fenotipi",
            "subtitle": "Karakteristik Kahkaha Nöbetleri, Ataksi, Nöbet ve Konuşma Yokluğu",
            "badge": "Angelman Fenotipi",
            "coreContent": {
                "text": "Angelman sendromlu çocukların klinik fenotipi son derece çarpıcı, benzersiz ve unutulmaz özelliklerle bezelidir; tıp literatüründe tarihsel olarak 'Mutlu Kukla' (Happy Puppet) sendromu olarak adlandırılmıştır. Nörolojik tablonun dört temel direği mevcuttur: (1) Uygunsuz, kontrolsüz ve nedensiz kahkaha patlamaları ve sürekli mutlu yüz ifadesi. (2) Karakteristik hareket bozukluğu: kollar dirsekten bükük haldeyken sergilenen el çırpma hareketleri (flapping), gövdede titreme (tremor) ve geniş tabanlı, sarsak, kukla yürüyüşü benzeri ataksi. (3) Konuşma dilinin tam veya tama yakın yokluğu (çocuklar neredeyse hiç kelime üretemez; tek hece veya hiç konuşamama vardır). (4) Erken süt çocukluğunda başlayan ve EEG'de tipik trifazik yüksek voltajlı yavaş dalga deşarjları gösteren tedaviye dirençli epileptik nöbetler. Mikrosefali, prognatizm (çıkık çene), geniş ağız ve açık ten/göz rengi eşlik eder.",
                "keyBullets": [
                    {"title": "Uygunsuz Kahkaha", "desc": "Nedensiz ve sürekli gülen, neşeli, hiperaktif mizaç en kardinal bulgudur.", "isKey": True},
                    {"title": "Kukla Benzeri Ataksi", "desc": "Kolları bükük el çırpma hareketleri ve sarsak geniş tabanlı ataktik yürüyüş.", "isKey": True},
                    {"title": "Konuşma Yokluğu", "desc": "Sözlü dil gelişimi neredeyse tamamen sıfırdır; kelime kullanımı yoktur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Klinik Alan", "Angelman Sendromundaki İmzası", "Nöropatolojik / Moleküler Karşılığı"],
                    [
                        [("Davranış ve Mizaç", False, ""), ("Sürekli gülümseme, uygunsuz kahkaha krizleri", True, "Nedensiz kahkaha"), ("Mezolimbik dopaminerjik regülasyon bozukluğu"), ],
                        [("Motor Hareketler", False, ""), ("Kollar havada el çırpma ve ataksi", True, "Kukla benzeri yürüyüş"), ("Serebellar ve bazal ganglion sinaptik defekti"), ],
                        [("Konuşma Becerisi", False, ""), ("Tamamen konuşamama (konuşma yokluğu)", True, "Sıfır kelime üretimi"), ("Kortikal konuşma merkezlerinin UBE3A kaybı"), ],
                        [("Nörolojik Nöbet", False, ""), ("Erken başlayan dirençli epilepsi", False, ""), ("GABA-A reseptör genlerinin komşu delesyonu"), ]
                    ]
                ),
                make_micro_quiz(
                    "3 yaşında bir çocukta derin zihinsel gerilik, hiç konuşamama (kelime yokluğu), yürürken kollarını bükerek el çırpma hareketleri yapma, sarsak ataktik yürüyüş ve nedensiz kontrolsüz kahkaha nöbetleri saptanıyor. En olası klinik genetik tanı hangisidir?",
                    {
                        "A": "Prader-Willi Sendromu",
                        "B": "Angelman Sendromu",
                        "C": "Down Sendromu",
                        "D": "Cri du chat Sendromu",
                        "E": "Wolf-Hirschhorn Sendromu"
                    },
                    "B",
                    {
                        "A": "Prader-Willi'de obezite ve hiperfaji vardır; kahkaha nöbeti ve ataksi görülmez.",
                        "B": "Doğru cevap B'dir: Uygunsuz kahkaha, el çırpma, ataksi ve konuşamama klasik Angelman sendromu (Happy Puppet) tablosudur.",
                        "C": "Down sendromu bu tabloyu vermez.",
                        "D": "Cri du chat kedi ağlaması verir.",
                        "E": "Wolf-Hirschhorn miğfer yüzü verir."
                    }
                ),
                make_cloze(
                    "Angelman sendromlu çocukların kollarını bükerek el çırpmaları ve ataktik sarsak yürüyüşleri nedeniyle sendrom tarihsel olarak mutlu kukla sendromu olarak anılmıştır.",
                    "mutlu kukla",
                    "Sendromun tarihsel eponimini anımsayınız"
                )
            ],
            "spotPearls": [
                "Angelman sendromu: Uygunsuz kahkaha, el çırpma, kukla ataksisi, KONUŞMA YOKLUĞU ve nöbetler.",
                "UBE3A ubikitin ligaz kaybına bağlıdır.",
                "Tarihsel adı 'Mutlu Kukla' (Happy Puppet) sendromudur."
            ]
        },

        # Slayt 89 (CHECKPOINT 9)
        {
            "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Genomik İmprinting, Uniparental Dizomi, Prader-Willi ve Angelman",
            "subtitle": "Bölüm Sonu Entegrasyonu ve Aktif Hatırlama İstasyonu",
            "badge": "Checkpoint 9",
            "coreContent": {
                "text": "Bu bölümde genomik imprinting, uniparental dizomi ve 15q11-q13 sendromlarını entegre ettik. İmprinting: gen ekspresyonunun ebeveyn kökenine göre DNA metilasyonuyla susturulmasıdır (Mendel kalıtımının istisnası). Uniparental Dizomi (UPD): kromozom çiftinin tek ebeveynden gelmesidir; heterodizomi Mayoz I'de iki farklı homoloğun, izodizomi Mayoz II'de özdeş kromatitin alınmasıdır; en sık trizomi kurtarma (trisomy rescue) ile oluşur. 15q11-q13 bölgesinde paternal genler (SNRPN, snoRNA) ve maternal gen (UBE3A) yer alır. PRADER-WİLLİ SENDROMU: Paternal aktif genlerin kaybıdır; %70 paternal delesyon, %30 maternal UPD15 (mUPD15); bebeklikte ağır hipotoni/emememe, 2 yaşından sonra hiperfaji (ghrelin artışı), morbid obezite ve hipogonadizm yapar. ANGELMAN SENDROMU: Maternal UBE3A kaybıdır; %70 maternal delesyon, %10 UBE3A mutasyonu, %3-5 paternal UPD15 (pUPD15); nedensiz kahkahalar ('mutlu kukla'), el çırpma, sarsak ataksi, konuşamama ve nöbetlerle seyreder.",
                "keyBullets": [
                    {"title": "PWS vs AS Mekanizması", "desc": "PWS = Paternal kayıp (%70 delesyon, %30 mUPD); AS = Maternal kayıp (%70 delesyon, %3-5 pUPD).", "isKey": True},
                    {"title": "PWS Fenotipi", "desc": "İnfantil hipotoni -> Hiperfaji, morbid obezite, hipogonadizm, badem gözler.", "isKey": True},
                    {"title": "AS Fenotipi", "desc": "Mutlu kukla, uygunsuz kahkaha, el çırpma ataksisi, konuşma yokluğu, UBE3A kaybı.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Kriter", "Prader-Willi Sendromu (PWS)", "Angelman Sendromu (AS)"],
                    [
                        [("Eksik Ebeveyn Katkısı", False, ""), ("Paternal aktif genlerin yokluğu", True, "Baba kopyası yok"), ("Maternal aktif genin (UBE3A) yokluğu", True, "Anne kopyası yok")],
                        [("En Sık Neden (%70)", False, ""), ("Paternal 15q11-q13 delesyonu", True, "Babadan delesyon"), ("Maternal 15q11-q13 delesyonu", True, "Anneden delesyon")],
                        [("UPD Oranı ve Tipi", False, ""), ("%25 - 30 Maternal UPD15 (mUPD15)", True, "Maternal UPD oranı yüksek"), ("%3 - 5 Paternal UPD15 (pUPD15)", True, "Paternal UPD oranı düşük")],
                        [("Karakteristik Davranış", False, ""), ("Hiperfaji, yemek arama, inatçılık", False, ""), ("Uygunsuz kahkaha krizleri, hiperaktivite", False, "")],
                        [("Konuşma Becerisi", False, ""), ("Mevcut (hafif bozukluk)", False, ""), ("Tamamen yok (konuşamaz)", False, "")],
                        [("Motor Profil", False, ""), ("Bebeklikte ağır hipotoni", False, ""), ("Kollarda el çırpma, kukla ataksisi", False, "")]
                    ]
                ),
                make_cloze(
                    "Prader-Willi sendromunda maternal UPD oranı yaklaşık %30 iken, Angelman sendromunda paternal UPD oranı yalnızca yaklaşık %3-5 kadardır.",
                    "%3-5",
                    "Angelman paternal UPD oranını anımsayınız"
                ),
                make_active_recall(
                    "Prader-Willi ve Angelman sendromlarının her ikisinde de delesyon ve UPD olgularını tek bir laboratuvar testiyle %99 doğrulukla ayırt eden tanısal test nedir?",
                    "15q11-q13 bölgesine yönelik DNA Metilasyon Analizidir (MS-PCR veya MS-MLPA).",
                    "Epigenetik metilasyon tanı testi"
                )
            ],
            "spotPearls": [
                "Prader-Willi = Paternal delesyon (%70) veya Maternal UPD (%30); SNRPN; hiperfaji/obezite.",
                "Angelman = Maternal delesyon (%70) veya Paternal UPD (%3-5); UBE3A; kahkaha/ataksi/konuşamama.",
                "Her iki sendrom da 15q11-q13 bölgesinin epigenetik bozukluğudur."
            ]
        },

        # Slayt 90
        {
            "title": "Diğer İmprinting Sendromları: Beckwith-Wiedemann ve Russell-Silver",
            "subtitle": "11p15 Kromozomal Bölgesi ve IGF2 / H19 Büyüme Ekseni",
            "badge": "11p15 İmprinting",
            "coreContent": {
                "text": "Genomik imprinting mekanizması yalnızca 15. kromozomla sınırlı değildir; 11. kromozomun kısa kolunda (11p15.5) yer alan imprinting kümesi de büyüme ve tümörijenez üzerinde hayati bir kontrol uygular. Bu bölgede iki zıt büyüme sendromu modellenir: (1) Beckwith-Wiedemann Sendromu (BWS): Bir aşırı büyüme (overgrowth) sendromudur. Paternal 11p15 duplikasyonu, maternal UPD11 veya H19/IGF2 imprinting merkezinin metilasyon hatasıyla paternal büyüme faktörü IGF2'nin aşırı üretilmesi sonucu gelişir. Karakteristik bulgular: makrozomi (iri doğum), makroglossi (dev dil), omfalosel, kulak memesinde yarıklar/çentikler ve çocukluk çağında Wilms tümörü ile hepatoblastom gelişme riskinin dramatik artmasıdır. (2) Russell-Silver Sendromu (RSS): 11p15'teki IGF2 ekspresyonunun kaybı veya Maternal UPD7 sonucu gelişen zıt bir tablodur; ağır intrauterin ve postnatal büyüme geriliği, üçgen yüz ve belirgin vücut asimetrisi (hemihipotrofi) ile seyreder.",
                "keyBullets": [
                    {"title": "11p15 İmprinting Kümesi", "desc": "IGF2 (büyüme faktörü) ve H19/CDKN1C (büyüme baskılayıcı) genlerini içerir.", "isKey": True},
                    {"title": "Beckwith-Wiedemann (Aşırı Büyüme)", "desc": "Makrozomi, makroglossi, omfalosel ve Wilms tümörü riski mevcuttur.", "isKey": True},
                    {"title": "Russell-Silver (Cücelik)", "desc": "Ağır büyüme kısıtlanması, üçgen yüz ve hemihipotrofi ile zıt tablodur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "11p15 İki Zıt Büyüme Fenotipi",
                    "Beckwith-Wiedemann (Aşırı Büyüme)",
                    "Aşırı IGF2 sinyali; makrozomi, makroglossi (büyük dil), omfalosel, organomegali, Wilms tümörü yatkınlığı.",
                    "Russell-Silver (Büyüme Geriliği)",
                    "Yetersiz IGF2 sinyali (veya mUPD7); intrauterin ve postnatal bodurluk, üçgen yüz, vücut asimetrisi."
                ),
                make_micro_quiz(
                    "Yenidoğan döneminde makrozomi (iri doğum), makroglossi (belirgin büyük dil) ve omfalosel saptanan, 11p15 bölgesindeki imprinting defektine bağlı gelişen ve Wilms tümörü riski taşıyan sendrom hangisidir?",
                    {
                        "A": "Russell-Silver Sendromu",
                        "B": "Beckwith-Wiedemann Sendromu",
                        "C": "Prader-Willi Sendromu",
                        "D": "Angelman Sendromu",
                        "E": "DiGeorge Sendromu"
                    },
                    "B",
                    {
                        "A": "Russell-Silver büyüme geriliği yapar.",
                        "B": "Doğru cevap B'dir: Makroglossi, omfalosel ve Wilms tümörü triadı klasik Beckwith-Wiedemann sendromudur (11p15 imprinting defekti).",
                        "C": "Prader-Willi 15q11'dedir.",
                        "D": "Angelman 15q11'dedir.",
                        "E": "DiGeorge 22q11 delesyonudur."
                    }
                ),
                make_cloze(
                    "Beckwith-Wiedemann sendromlu çocuklarda erken çocukluk döneminde böbrekte gelişme riski belirgin derecede artan embriyonik malign tümör Wilms tümörüdür.",
                    "Wilms tümörü",
                    "Böbrek embriyonik tümör adını yazınız"
                )
            ],
            "spotPearls": [
                "Beckwith-Wiedemann sendromu (11p15): Makrozomi, makroglossi, omfalosel, Wilms tümörü.",
                "Russell-Silver sendromu (11p15 / mUPD7): Ağır büyüme geriliği, üçgen yüz, vücut asimetrisi.",
                "Bu iki sendrom 11p15 IGF2/H19 eksenindeki zıt epigenetik hataları temsil eder."
            ]
        }
    ]
