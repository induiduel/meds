# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_7_slides():
    slides = []

    # Slide 61
    slides.append({
        "id": "k1-20-s61",
        "title": "Edinsel Trombofililere Genel Bakış: Risk Derecelendirmesi",
        "content": "Klinik pratikte karşılaşılan tromboz vakalarının büyük çoğunluğu genetik bir mutasyondan ziyade **sekonder (edinsel) risk faktörlerine** bağlıdır (Sınav Spotu):\n\n- **Çok Yüksek Tromboz Riski Taşıyan Durumlar:**\n  1. **Uzamış Yatak İstirahati ve İmmobilizasyon:** Kas pompası çalışmaz, venöz staz derinleşir.\n  2. **Miyokard Enfarktüsü ve Atriyal Fibrilasyon:** Ventriküler diskinetik duvar ve sol atriyal staz.\n  3. **Majör Doku Hasarı:** Kalça/femur kırıkları, ortopedik protez cerrahisi ve geniş yanıklar (yoğun Doku Faktörü açığa çıkar).\n  4. **Kanser (Malignite):** Tümör hücrelerinin prokoagülan salgıları.\n  5. **Prostetik Kalp Kapakları:** Yabancı yüzey teması ve türbülans.\n  6. **Özel İmmün Tablolar:** Heparine Bağlı Trombositopeni (HIT) ve Antifosfolipid Sendromu (APS).\n- **Orta ve Hafif Risk Faktörleri:** Gebelik ve lohusalık (postpartum), oral kontraseptifler (OKS), hormon replasmanı, nefrotik sendrom, orak hücreli anemi, obezite ve ileri yaş.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Risk Kategorisi", "Klinik Durumlar", "Tromboz Mekanizması"],
                [
                    ["Çok Yüksek Risk", "Malignite, ortopedik cerrahi, HIT, Antifosfolipid sendromu", "Masif doku faktörü, immün trombosit aktivasyonu"],
                    ["Yüksek Risk", "Uzamış yatak istirahati, MI, Atriyal fibrilasyon, Yanıklar", "Şiddetli venöz staz, endotel hasarı"],
                    ["Orta / Hafif Risk", "Gebelik, oral kontraseptif kullanımı, nefrotik sendrom, obezite", "Hepatik pıhtılaşma faktör artışı, antikoagülan kaybı"]
                ]
            ),
            make_cloze(
                "Edinsel hiperkoagülabilite nedenleri arasında özellikle ortopedik kalça kırığı cerrahisi ve ileri evre kanserler çok yüksek tromboz riski taşır.",
                "kanserler",
                "Trousseau sendromuna yol açan ve prokoagülan salgılayan malign tümörler"
            )
        ]
    })

    # Slide 62
    slides.append({
        "id": "k1-20-s62",
        "title": "Malignite ve Tromboz: Trousseau Sendromu (Gezici Tromboflebit)",
        "content": "Kanser hastalarında tromboz, hastalığın ilk belirtisi veya en ölümcül komplikasyonu olabilir (Sınav Spotu):\n\n- **Tümör Kökenli Prokoagülanlar:**\n  - Özellikle adenokarsinomlar (başta **Pankreas, Akciğer, Mide ve Kolon kanserleri**) hücre yüzeylerinden yoğun şekilde **Doku Faktörü (TF)** ve mikropartiküller salgılar.\n  - Ayrıca tümör kaynaklı müsinler ve **kanser prokoagülanı (sistein proteaz)** Faktör X'u doğrudan aktive edebilir.\n- **Trousseau Sendromu (Tromboflebitis Migrans / Gezici Tromboflebit):**\n  - Vücudun bir bölgesinde (örn. sol kolda) bir venöz tromboz ve flebit gelişir; birkaç gün içinde kendiliğinden gerilerken bu kez başka bir anatomik bölgede (örn. sağ bacakta veya göğüs duvarında) yeni bir trombüs patlak verir.\n  - **Patognomonik İpucu:** Açıklanamayan gezici tromboflebit atakları ile gelen bir hastada altta yatan gizli bir **Pankreas Adenokarsinomu veya visseral malignite** mutlaka araştırılmalıdır (Armand Trousseau kendi hastalığını bu bulguyla teşhis etmiştir).",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kanser Zemininde Trousseau Sendromu Mekanizması",
                [
                    "1. Müsinöz Adenokarsinom: Tümör hücreleri prokoagülan mikropartiküller döker.",
                    "2. Sistemik Faktör X Aktivasyonu: Kanser prokoagülanı kaskadı doğrudan tetikler.",
                    "3. Gezici Tromboflebit: Farklı ekstremite venlerinde sırayla pıhtılar oturur.",
                    "4. Çözülme ve Nüks: Bir odak gerilerken başka bir venöz yatak tıkanır.",
                    "5. Gizli Malignite Uyarısı: Pankreas veya akciğer tümörü taranarak tanı konur."
                ]
            ),
            make_quiz(
                "Farklı anatomik bölgelerdeki venlerde sırayla ortaya çıkıp kaybolan ve tekrar nükseden 'gezici tromboflebit' (Trousseau sendromu) tablosunda öncelikle hangi organın gizli adenokarsinomu araştırılmalıdır?",
                [
                    {"key": "A", "text": "Pankreas (veya akciğer/mide) adenokarsinomu", "isCorrect": True, "explanation": "Doğru cevap A'dır: Gezici tromboflebitis migrans (Trousseau sendromu), özellikle gizli pankreas adenokarsinomunun klasik paraneoplastik vasküler bulgusudur."},
                    {"key": "B", "text": "Beyin glioblastomu", "isCorrect": False, "explanation": "Glioblastom intrakranyal kitle yapar, Trousseau sendromu yapmaz."},
                    {"key": "C", "text": "Deri skuamöz hücreli karsinomu", "isCorrect": False, "explanation": "Cilt kanserleri gezici tromboflebit yapmaz."},
                    {"key": "D", "text": "Tiroid papiller karsinomu", "isCorrect": False, "explanation": "Tiroid kanseri tipik olarak gezici tromboflebit ile prezente olmaz."}
                ]
            )
        ]
    })

    # Slide 63
    slides.append({
        "id": "k1-20-s63",
        "title": "Heparine Bağlı Trombositopeni (HIT Tip II): İmmünolojik Temel",
        "content": "Kan sulandırıcı olarak verilen heparinin, paradoksal olarak hayatı tehdit eden masif pıhtılaşmaya yol açtığı immünolojik tablo **Heparine Bağlı Trombositopenidir (HIT)** (Sınav Spotu):\n\n- **Epidemiyoloji:** Standart (fraksiyone edilmemiş) heparin kullanan hastaların yaklaşık **%3 ila %5'inde**; düşük molekül ağırlıklı heparin (DMAH) kullananların ise <%1'inde gelişir.\n- **Zamanlama:** Tipik olarak heparin tedavisinin başlamasından sonraki **5 ila 10. günlerde** ortaya çıkar (daha önce maruziyet varsa ilk 24 saatte gelişebilir).\n- **Moleküler Antijen Kompleksi:**\n  - Trombositlerin alfa granüllerinden salgılanan pozitif yüklü bir kemokin olan **Trombosit Faktörü 4 (PF4)**, negatif yüklü heparin zincirlerine elektrostatik olarak bağlanır.\n  - Bu bağlanma sonucunda PF4 proteininin yapısı değişir ve yeni bir neoantijen oluşur: **[Heparin - PF4 Kompleksi]**.\n- **İmmünolojik Yanıt:** Vücut bu yabancı komplekse karşı **IgG yapısında otoantikorlar** üretir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "HIT Tip II Antijen ve Antikor Oluşum Akışı",
                [
                    "1. Heparin Tedavisi: Hastaya fraksiyone edilmemiş heparin başlanır.",
                    "2. PF4-Heparin Bağlanması: Trombositten dökülen PF4 heparine kenetlenir.",
                    "3. Neoantijen Oluşumu: PF4 konformasyonu değişerek immünojenik hale gelir.",
                    "4. IgG Yanıtı: Bağışıklık sistemi komplekse karşı spesifik IgG üretir (5-10. gün).",
                    "5. İmmün Kompleks: IgG antikorları dolaşımdaki [Heparin-PF4] kompleksine kilitlenir."
                ]
            ),
            make_cloze(
                "Heparine bağlı trombositopeni patogenezinde otoantikorların hedef aldığı temel antijenik yapı heparin ile Trombosit Faktörü 4 kompleksidir.",
                "Trombosit Faktörü 4",
                "Heparin ile birleştiğinde neoantijen oluşturan alfa granül kemokini (PF4)"
            )
        ]
    })

    # Slide 64
    slides.append({
        "id": "k1-20-s64",
        "title": "HIT Paradoksu: Trombositopeni Var, Neden Tromboz Gelişir?",
        "content": "HIT tablosunun tıptaki en büyük paradoksu, hastanın trombosit sayısı düşerken (trombositopeni) aynı anda vücutta masif pıhtılaşma fırtınasının kopmasıdır (Sınav Spotu):\n\n- **Trombosit FcγRIIa Reseptörünün Uyarılması:**\n  - [Heparin - PF4 - IgG] immün kompleksi, trombosit yüzeyinde bulunan **FcγRIIa (CD32)** reseptörlerine bağlanır.\n  - Bu bağlanma trombosit içinde devasa bir tirozin kinaz kaskadı başlatarak **tüm trombositleri kontrolsüz şekilde aktive eder**.\n- **Paradoksun Çözümü:**\n  1. **Trombosit Tüketimi (Trombositopeni):** Aktive olan trombositler ya kitleler halinde pıhtıların içine hapsolur ya da dalak makrofajları tarafından temizlenir; trombosit sayısı %50'den fazla düşer.\n  2. **Kontrolsüz Protrombotik Durum (Tromboz Fırtınası):** Aktive olan trombositlerden yoğun miktarda mikrodebris, Doku Faktörü ve trombin salınır; endotel hücreleri de hasarlanır.\n- **Klinik Sonuç:** Hastaların %50'sinde **masif DVT, pulmoner emboli, arteriyel inme, ekstremite gangreni ve amputasyon** riski gelişir!\n- **Tedavi:** Heparin DERHAL KESİLİR; yerine direkt trombin inhibitörleri (Argatroban, Bivalirudin) veya Fondaparinuks başlanır (asla trombosit süspansiyonu verilmez!).",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Klasik İlaç Trombositopenisi vs HIT Tip II",
                "Klasik İlaç Trombositopenisi",
                "Trombositler yok edilir; hasta kanamaya meyleder; pıhtılaşma görülmez.",
                "HIT Tip II (Paradoksal Tromboz)",
                "Trombositler Fc reseptörleriyle aktive edilerek tüketilir; trombositopeniye rağmen masif tromboz oluşur."
            ),
            make_quiz(
                "Fraksiyone edilmemiş heparin tedavisinin 7. gününde trombosit sayısı 250.000'den 80.000'e düşen ve eş zamanlı olarak sol bacağında masif derin ven trombozu gelişen bir hastada en doğru acil yaklaşım hangisidir?",
                [
                    {"key": "A", "text": "Heparin derhal kesilmeli ve Argatroban gibi direkt trombin inhibitörüne geçilmelidir", "isCorrect": True, "explanation": "Doğru cevap A'dır: Bu tablo klasik HIT'tir; heparin derhal kesilmeli, alternatif antikoagülan (Argatroban/Bivalirudin) başlanmalıdır; trombosit verilmesi trombozu daha da alevlendirir."},
                    {"key": "B", "text": "Heparin dozu iki katına çıkarılmalıdır", "isCorrect": False, "explanation": "Heparin devam ederse hasta masif tromboz veya ampütasyonla kaybedilir."},
                    {"key": "C", "text": "Trombosit süspansiyonu transfüzyonu yapılmalıdır", "isCorrect": False, "explanation": "Yeni trombositler yangına körükle gitmektir, kontrendikedir."},
                    {"key": "D", "text": "Tedavi tamamen kesilip hiçbir antikoagülan verilmemelidir", "isCorrect": False, "explanation": "Tromboz fırtınası sürdüğü için alternatif antikoagülan şarttır."}
                ]
            )
        ]
    })

    # Slide 65
    slides.append({
        "id": "k1-20-s65",
        "title": "Antifosfolipid Antikor Sendromu (APS): Triad ve β2-Glikoprotein I",
        "content": "Edinsel trombofililerin en karmaşık ve otoimmün prototipi **Antifosfolipid Antikor Sendromudur (APS / Hughes Sendromu)** (Sınav Spotu):\n\n- **Primer vs Sekonder APS:**\n  - Tek başına başka bir otoimmün hastalık olmadan gelişirse **Primer APS**,\n  - Sistemik Lupus Eritematozus (SLE) gibi bir bağ dokusu hastalığı zemininde gelişirse **Sekonder APS** adını alır.\n- **Klinik Triad (Klasik Bulgular):**\n  1. **Tekrarlayan Trombozlar:** Hem venöz (DVT, pulmoner emboli, Budd-Chiari) hem de arteriyel (inme, miyokard enfarktüsü, parmak gangreni) damarları tutar.\n  2. **Tekrarlayan Gebelik Kayıpları:** Plasental spiral arterlerde mikrotrombozlara bağlı 10. haftadan önce tekrarlayan düşükler veya geç fetal kayıplar.\n  3. **Trombositopeni:** Trombosit zarına antikor bağlanması sonucu tüketim.\n- **Gerçek Antijenik Hedef: β2-Glikoprotein I:**\n  - Adı fosfolipid antikoru olsa da antikorlar çıplak fosfolipide değil; plazma proteinlerine, özellikle **β2-Glikoprotein I (β2-GPI)** molekülüne ve **Protrombine** bağlanır.\n  - Bu bağlanma endoteli, monositleri ve trombositleri doğrudan aktive ederek protrombotik fırtına yaratır.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["APS Klinik Kriteri", "Karakteristik Özellik", "Patolojik Mekanizma"],
                [
                    ["Vasküler Tromboz", "En az 1 doğrulanmış arteriyel, venöz veya küçük damar trombozu", "Endotel aktivasyonu ve trombosit agregasyonu"],
                    ["Gebelik Morbiditesi", ">=3 açıklanamayan erken abortus veya geç intrauterin fetal kayıp", "Plasental damar trombozu ve villöz enfarktüs"],
                    ["Hematolojik Bulgu", "Hafif-orta trombositopeni ve livedo reticularis", "Trombosit tüketimi ve kutanöz mikrotromboz"]
                ]
            ),
            make_cloze(
                "Antifosfolipid antikor sendromunda antikorların hedef aldığı en temel plazma protein antijeni beta 2 glikoprotein I molekülüdür.",
                "beta 2 glikoprotein I",
                "APS patogenezinde otoantikorların bağlandığı anahtar kofaktör plazma proteini"
            )
        ]
    })

    # Slide 66
    slides.append({
        "id": "k1-20-s66",
        "title": "APS Laboratuvar Paradoksu: Lupus Antikoagülanı ve Sifiliz Testi",
        "content": "APS hastalarının laboratuvar testleri tıp fakültesi sınavlarının en ünlü tuzak sorularını barındırır (Sınav Spotu):\n\n- **Laboratuvarda Bakılan Üç Antikor:**\n  1. **Anti-Kardiyolipin Antikorları (aCL - IgG/IgM)** (ELISA ile ölçülür),\n  2. **Anti-β2-Glikoprotein I Antikorları** (ELISA ile ölçülür),\n  3. **Lupus Antikoagülanı (LA)** (Pıhtılaşma testleriyle ölçülür).\n- **Büyük Laboratuvar Paradoksu (Lupus Antikoagülanı):**\n  - Hastada in vivo ortamda masif bir **TROMBOZ (hiperkoagülabilite)** mevcuttur.\n  - Ancak hastanın kanı laboratuvar tüpüne alınıp aPTT testi yapıldığında **aPTT süresi paradoksal olarak UZAR!**\n  - Nedeni: Test tüpündeki reaktif fosfolipidlere bağlanan antikorlar, pıhtılaşma faktörlerinin tüpteki fosfolipide oturmasını engeller (in vitro pıhtılaşmayı geciktirir).\n  - Ancak hastanın vücudunda (in vivo) tam tersine endoteli uyararak pıhtı oluşturur!\n- **Sifiliz Testinde Yalancı Pozitiflik:** Klasik sifiliz tarama testi olan VDRL/RPR reaktifi kardiyolipin içerir; APS antikorları bu reaktife bağlanarak **sifiliz olmadığı halde VDRL testini pozitif çıkartır**.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "İn Vivo (Hasta Vücudu) vs İn Vitro (Laboratuvar Tüpü) APS",
                "İn Vivo (Hastanın Damarları)",
                "Masif TROMBOZ görülür; derin ven trombozları, inme, düşükler ve enfarktüsler patlak verir.",
                "İn Vitro (Test Tüpü)",
                "aPTT süresi paradoksal olarak UZAR; fosfolipid reaktifi bloke edildiği için tüpte pıhtılaşma gecikir."
            ),
            make_quiz(
                "Antifosfolipid antikor sendromunda (APS) in vivo ortamda masif tromboz eğilimi olmasına rağmen laboratuvar tüpünde aPTT süresinin paradoksal olarak uzamasına yol açan antikor fenotipine ne ad verilir?",
                [
                    {"key": "A", "text": "Lupus Antikoagülanı", "isCorrect": True, "explanation": "Doğru cevap A'dır: Lupus antikoagülanı in vitro ortamda fosfolipid reaktiflerini engelleyerek aPTT'yi uzatır; ancak in vivo ortamda güçlü bir tromboz nedenidir."},
                    {"key": "B", "text": "Anti-nükleer antikor (ANA)", "isCorrect": False, "explanation": "ANA hücresel çekirdek antikorudur, pıhtılaşma süresini doğrudan uzatmaz."},
                    {"key": "C", "text": "Anti-dsDNA", "isCorrect": False, "explanation": "Lupus nefriti ile ilişkilidir."},
                    {"key": "D", "text": "Romatoid Faktör", "isCorrect": False, "explanation": "RF IgG Fc bölgesine karşı antikordur."}
                ]
            )
        ]
    })

    # Slide 67
    slides.append({
        "id": "k1-20-s67",
        "title": "Yaygın Damar İçi Pıhtılaşma (DİK): Çift Yönlü Felaket",
        "content": "Hemostaz ve trombozun en trajik son noktası, literatürde 'Tüketim Koagülopatisi' olarak da bilinen **Dissemine İntravasküler Koagülasyondur (DİK)** (Sınav Spotu):\n\n- **Tetikleyici Faktörler:** Septik şok (gram-negatif endotoksin), obstetrik felaketler (abruptio plasenta, amniyon sıvı embolisi), masif travma/yanıklar ve akut promiyelositik lösemi (APL - M3).\n- **1. Faz: Mikrovasküler Tromboz Fırtınası:**\n  - Dolaşıma devasa miktarda Doku Faktörü veya sitokin dökülür.\n  - Tüm vücudun mikrosirkülasyonunda (böbrek, beyin, akciğer, karaciğer) yaygın mikrotrombüsler oturur.\n  - Dokularda iskemik enfarktüsler, böbrek yetmezliği ve çoklu organ yetmezliği (MODS) gelişir.\n- **2. Faz: Tüketim ve Masif Kanama:**\n  - Tüm pıhtılaşma faktörleri (özellikle fibrinojen, Faktör V, VIII) ve trombositler bu yaygın mikrotrombüslerin içinde tükenir.\n  - Eş zamanlı olarak reaktif fibrinoliz patlar; kanda aşırı FDP ve D-Dimer birikir.\n  - Sonuçta hasta pıhtılaşamaz hale gelir; damar yolu girişlerinden, cerrahi yaralardan ve mukozalardan **durdurulamayan masif kanamalar** başlar.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "DİK Patofizyolojik Kısır Döngüsü",
                [
                    "1. Masif Tetikleyici: Sepsis veya obstetrik travmayla dolaşıma doku faktörü dökülür.",
                    "2. Sistemik Mikrotromboz: Kılcal damarlarda yaygın fibrin tıkaçları oluşur.",
                    "3. Organ İskemisi: Böbrek ve beyin dokusunda mikroenfarktüsler gelişir.",
                    "4. Faktör ve Trombosit Tüketimi: Trombosit ve fibrinojen rezervi tamamen tükenir.",
                    "5. Masif Kanama Felaketi: Hasta aynı anda hem trombozdan organ kaybeder hem kanar."
                ]
            ),
            make_cloze(
                "Sepsis ve masif travma zemininde mikrovasküler trombozlarla pıhtılaşma faktörlerinin tükenmesi sonucu eş zamanlı kanamalarla seyreden tabloya dissemine intravasküler koagülasyon denir.",
                "dissemine intravasküler koagülasyon",
                "Tüketim koagülopatisi olarak da bilinen çift yönlü tromboz ve kanama sendromu"
            )
        ]
    })

    # Slide 68
    slides.append({
        "id": "k1-20-s68",
        "title": "Gebelik, Oral Kontraseptifler ve Hiperöstrojenizm",
        "content": "Kadın yaşamında östrojen hormonunun yükseldiği fizyolojik ve farmakolojik durumlar belirgin bir protrombotik zemin hazırlar (Sınav Spotu):\n\n- **Biyolojik Mantık (Evrimsel Korunma):**\n  - Gebelikte hemostatik sistemin pıhtılaşma yönüne kayması, doğum sırasındaki masif uterin kanamadan anneyi korumak için gelişmiş fizyolojik bir adaptasyondur.\n  - Ancak bu durum venöz tromboz ve pulmoner emboli riskini gebelikte ve özellikle **postpartum (lohusalık) döneminde 5-10 kat artırır**.\n- **Östrojenin Hepatik Etkileri (Kombine OKS ve Gebelik):**\n  1. **Pıhtılaşma Faktörlerini Artırır:** Karaciğerde fibrinojen, Faktör VII, Faktör VIII, Faktör X ve protrombin sentezini kamçılar.\n  2. **Doğal Antikoagülanları Azaltır:** Plazmadaki **Antitrombin III** düzeyini düşürür ve **Protein S** konsantrasyonunu belirgin azaltır.\n  3. **Kazanılmış APC Direnci:** Plazmada hafif düzeyde fonksiyonel Aktive Protein C direnci tablosu oluşturur.\n- **Kombinasyon Tehlikesi:** Faktör V Leiden taşıyıcısı olan genç bir kadın oral kontraseptif (doğum kontrol hapı) kullanırsa venöz tromboz riski **30 ila 50 katına fırlar!**",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Parametre", "Hiperöstrojenik Durumdaki Değişim", "Klinik Yansıması"],
                [
                    ["Fibrinojen, VII, VIII, X", "Belirgin artış (Hepatik sentez uyarımı)", "Kaskadın hızlanması ve pıhtılaşma eğilimi"],
                    ["Antitrombin III ve Protein S", "Belirgin azalma", "Doğal fren mekanizmasının zayıflaması"],
                    ["Faktör V Leiden + OKS", "Sinerjistik risk katlanması", "Genç kadında masif DVT ve pulmoner emboli"],
                    ["Postpartum Lohusalık", "Maksimum tromboemboli riski", "Sezaryen sonrası erken mobilizasyon ve profilaksi şarttır"]
                ]
            ),
            make_quiz(
                "Kombine oral kontraseptif (doğum kontrol hapı) kullanan veya gebe olan kadınlarda venöz tromboz riskinin artmasına yol açan temel biyokimyasal değişiklik hangisidir?",
                [
                    {"key": "A", "text": "Hepatik pıhtılaşma faktör sentezinin artması ve Antitrombin III / Protein S düzeylerinin azalması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Östrojen karaciğerde koagülasyon faktörlerini artırırken doğal antikoagülanlar olan ATIII ve Protein S'i düşürerek protrombotik ortam hazırlar."},
                    {"key": "B", "text": "Kanda trombosit sayısının 1 milyonun üzerine çıkması", "isCorrect": False, "explanation": "Östrojen aşırı trombositoz yapmaz."},
                    {"key": "C", "text": "Doku faktörünün tamamen parçalanması", "isCorrect": False, "explanation": "TF parçalanmaz."},
                    {"key": "D", "text": "Plazmin enziminin aşırı aktive olması", "isCorrect": False, "explanation": "Plazmin pıhtıyı eritir, tromboz yapmaz."}
                ]
            )
        ]
    })

    # Slide 69 - CHECKPOINT 7
    slides.append({
        "id": "k1-20-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Edinsel Trombofililer, HIT ve Antifosfolipid Sendromu",
        "content": "Bu checkpointte edinsel hiperkoagülabilite durumlarını ve özel klinik tabloları özetliyoruz:\n\n- **Malignite ve Trousseau Sendromu:** Müsinöz adenokarsinomlar (özellikle **pankreas**) prokoagülan salgılar; farklı venlerde sırayla çıkan **gezici tromboflebit (tromboflebitis migrans)** tipiktir.\n- **HIT Tip II:** Heparin-PF4 kompleksine karşı **IgG antikorları** oluşur; antikorlar trombosit **FcγRIIa** reseptörüne bağlanır; trombositler tüketilirken (**trombositopeni**) eş zamanlı olarak **masif arteriyel/venöz tromboz fırtınası** kopar; heparin hemen kesilir.\n- **Antifosfolipid Sendromu (APS):** Klinik triad: **Tekrarlayan trombozlar (venöz ve arteriyel)**, **tekrarlayan düşükler**, **trombositopeni**. Hedef antijen **β2-Glikoprotein I**'dir. İn vivo tromboz yapmasına rağmen in vitro **aPTT paradoksal olarak uzar (Lupus antikoagülanı)**; **sifiliz testi (VDRL) yalancı pozitif** çıkar.\n- **DİK (Tüketim Koagülopatisi):** Sepsis/obstetrik şokta yaygın mikrotrombozlar ve organ yetmezliği + faktörlerin tükenmesiyle durdurulamayan masif kanama.\n- **Östrojen ve Gebelik:** Faktör sentezini artırıp ATIII/Protein S'i düşürür; Faktör V Leiden ile birleşirse risk 50 kata fırlar.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Edinsel Tablo", "Temel Mekanizma / Antijen", "Ayırt Edici Klinik İpucu"],
                [
                    ["Trousseau Sendromu", "Tümör doku faktörü ve müsin salgısı", "Pankreas kanserinde gezici tromboflebit"],
                    ["HIT Tip II", "Heparin-PF4 kompleksine karşı IgG", "Heparin alan hastada trombosit düşüşü + Masif tromboz"],
                    ["Antifosfolipid Sendromu", "Anti-β2-GPI, Anti-kardiyolipin, LA", "Tekrarlayan düşük + Tromboz + Uzamış aPTT + Yalancı VDRL"],
                    ["DİK", "Sistemik doku faktörü ve mikrotrombüs", "Çoklu organ yetmezliği ve yaygın kontrolsüz kanama"],
                    ["Hiperöstrojenizm", "Artmış faktörler, azalmış ATIII / Protein S", "Lohusalıkta DVT ve OKS kullananlarda emboli"]
                ]
            ),
            make_chain(
                "Edinsel Trombofililer Büyük Özeti",
                [
                    "1. Kanser Paraneoplazisi: Trousseau sendromunda gezici tromboflebit gelişir.",
                    "2. Heparin Komplikasyonu: HIT'te PF4-antikor kompleksiyle trombositler patlar.",
                    "3. Otoimmünite: APS'de beta-2-GPI antikorlarıyla düşükler ve trombozlar oturur.",
                    "4. Tüketim Felaketi: DİK'te mikrotrombozlar organları boğarken faktörler biter."
                ]
            )
        ]
    })

    # Slide 70
    slides.append({
        "id": "k1-20-s70",
        "title": "Bölüm Özeti: Trombofililerden Trombüs Morfolojisine Geçiş",
        "content": "Bölüm 7 boyunca edinsel trombofilileri (kanser, HIT, Antifosfolipid sendromu, DİK ve hiperöstrojenizm) inceledik:\n\n- **Özet:** Edinsel faktörler immün kompleksler veya tümör prokoagülanları üzerinden kanı hiperkoagülan hale getirir.\n- **Sonraki Bölüm (Bölüm 8):** Canlı damar içinde oluşan trombüsün mikroskobik ve makroskobik mimarisini, **Zahn çizgilerini, arteriyel vs venöz trombüs farklarını, mural trombüsleri, kalp vejetasyonlarını ve ölüm sonrası (postmortem) pıhtı ayrımını** detaylarıyla ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Standart heparin kullanan bir hastada 5-10. günlerde trombositopeni ile birlikte paradoksal masif arteriyel ve venöz tromboza yol açan immün sendrom hangisidir?",
                "Heparine Bağlı Trombositopeni (HIT Tip II)",
                "Heparin-PF4 kompleksine karşı antikorların trombositleri aktive ettiği tablo"
            ),
            make_quiz(
                "Tekrarlayan derin ven trombozları ve tekrarlayan gebelik kayıpları olan genç bir kadında aPTT süresi uzun bulunuyor ve sifiliz serolojisi (VDRL) yalancı pozitif çıkıyor. En olası tanı hangisidir?",
                [
                    {"key": "A", "text": "Antifosfolipid Antikor Sendromu (APS)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Tromboz, düşükler, trombositopeni, in vitro uzamış aPTT ve yalancı pozitif VDRL klasik Antifosfolipid Antikor Sendromudur."},
                    {"key": "B", "text": "Faktör V Leiden mutasyonu", "isCorrect": False, "explanation": "Faktör V Leiden VDRL yalancı pozitifliği yapmaz."},
                    {"key": "C", "text": "Primer Sifiliz (Şankr)", "isCorrect": False, "explanation": "Sifilizde tekrarlayan tromboz ve uzamış aPTT beklenmez."},
                    {"key": "D", "text": "Hemofili A", "isCorrect": False, "explanation": "Hemofili A erkeklerde görülür ve kanama yapar."}
                ]
            )
        ]
    })

    return slides
