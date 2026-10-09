# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_4_slides():
    slides = []

    # Slide 31
    slides.append({
        "id": "k1-15-s31",
        "title": "Granülasyon Dokusu Tanımı: Onarımın Biyolojik Zirvesi",
        "content": "Yara iyileşmesinin 3. ila 5. günleri arasında başlayan proliferatif evrenin en karakteristik morfolojik göstergesi **granülasyon dokusudur (granulation tissue)**:\n\n- **Granülasyon Dokusu Tanımı (Sınav Spotu):** Skarla onarım sürecinde hasarlı doku boşluğunu geçici olarak dolduran, **yeni oluşmuş hassas kılcal damarlar (anjiyogenez)**, **prolifere olan fibroblastlar** ve **gevşek, ödemli bir ekstrasellüler matriks** içeren özelleşmiş genç bağ dokusudur.\n- **Makroskopik Görünüm:** Yara tabanında parlak pembe-kırmızı renkli, ıslak, yumuşak ve küçük tanecikli (granüler) bir kadife örtü gibi görünür.\n- **Hassasiyet:** Çok sayıda yeni kılcal damar içerdiği için en ufak dokunmada kolayca kanar; bu durum cerrahta dokunun canlı ve iyi kanlandığı hissini uyandırır.\n- **Zaman Çizelgesi:** 3-5. günlerde hızla artar, 7-10. günlerde yara alanını tamamen kaplar ve daha sonra olgunlaşarak fibröz skara dönüşür.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Fibrin Pıhtısı vs Granülasyon Dokusu",
                "İlk 24-48 Saat (Fibrin Pıhtısı)",
                "Koyu kırmızı/kahverengi, cansız, lökosit dolu geçici kanama tıkacıdır.",
                "3-7. Günler (Granülasyon Dokusu)",
                "Canlı, parlak pembe, yeni kılcal damarlar ve çoğalan fibroblastlarla dolu aktif onarım dokusudur."
            ),
            make_cloze(
                "Yara iyileşmesinin proliferatif evresinde oluşan, yeni kılcal damarlar ve fibroblastlardan zengin pembe dokuya granülasyon dokusu denir.",
                "granülasyon",
                "Tanecikli görünüme sahip genç onarım dokusu adı"
            )
        ]
    })

    # Slide 32
    slides.append({
        "id": "k1-15-s32",
        "title": "Granülasyon Dokusunun Üçlü Histopatolojik Bileşeni",
        "content": "Patoloji mikroskobunda granülasyon dokusu incelendiğinde üç temel yapısal bileşen bir arada izlenir (Sınav Sorusu):\n\n- **1. Yeni Oluşan Kılcal Damarlar (Anjiyogenez):**\n  - İnce duvarlı, tek katlı endotelle döşeli, henüz tam olgunlaşmamış bol miktarda yeni kapiller tomurcukları.\n  - Endotel hücreleri şişkin ve aktiftir.\n- **2. Prolifere Olan Fibroblastlar / Miyofibroblastlar:**\n  - İğsi şekilli, geniş soluk nükleuslu, aktif protein sentezi yapan genç fibroblast hücreleri.\n  - İlerleyen günlerde miyofibroblasta dönüşerek aktin flamanları kazanırlar.\n- **3. Gevşek, Ödemli Ekstrasellüler Matriks (ECM):**\n  - Fibronektin, hyaluronik asit, proteoglikanlar ve ince Tip III kollajen liflerinden oluşan hidrate gevşek zemin.\n  - Arada mononükleer iltihabi hücreler (makrofajlar, lenfositler, mast hücreleri) yer alır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Histolojik Bileşen", "Mikroskobik Özellik", "Fonksiyonel Rolü"],
                [
                    ["Yeni Damarlar (Kapillerler)", "İnce duvarlı, endoteli şişkin, bol lümenli", "Dokunun oksijenlenmesi ve beslenmesi"],
                    ["Fibroblastlar", "İğsi hücreler, geniş sitoplazma, aktif nükleus", "Kollajen ve temel matriks sentezi"],
                    ["Gevşek ECM ve Ödem", "Açık pembe zemin, proteoglikan ve fibronektin", "Hücrelerin rahat göç edebilmesini sağlama"]
                ]
            ),
            make_quiz(
                "Granülasyon dokusunun ışık mikroskobik incelemesinde aşağıdaki histolojik yapılardan hangisinin görülmesi BEKLENMEZ?",
                [
                    {"key": "A", "text": "Yeni oluşmuş, ince duvarlı kılcal damarlar (anjiyogenez)", "isCorrect": False, "explanation": "Yeni kılcal damarlar granülasyon dokusunun temel özelliğidir."},
                    {"key": "B", "text": "Geniş sitoplazmalı, prolifere olan aktif fibroblastlar", "isCorrect": False, "explanation": "Aktif fibroblastlar matriks sentezi için dokuyu doldurur."},
                    {"key": "C", "text": "Yoğun, asellüler, kalın Tip I kollajen demetleri ve avasküler alanlar", "isCorrect": True, "explanation": "Doğru cevap C'dir: Kalın Tip I kollajen demetleri ve avasküler yapı genç granülasyon dokusunda değil, aylar sonra oluşan olgun skar dokusunda görülür."},
                    {"key": "D", "text": "Gevşek, ödemli ekstrasellüler matriks ve makrofajlar", "isCorrect": False, "explanation": "Ödemli zemin ve makrofajlar granülasyon dokusunun doğal parçasıdır."}
                ]
            )
        ]
    })

    # Slide 33
    slides.append({
        "id": "k1-15-s33",
        "title": "'Granülasyon' İsimlendirmesinin Kökeni ve Makroskopi",
        "content": "Bu dokunun neden 'granülasyon' olarak adlandırıldığını bilmek patolojiyi kavramak açısından son derece aydınlatıcıdır:\n\n- **Kelime Kökeni:** Latince 'granulum' (küçük tanecik) kelimesinden türetilmiştir.\n- **Makroskopik Neden:** Açık bir yara (örneğin bacak ülseri veya geniş yanık) tabanına çıplak gözle bakıldığında, yüzeyde minik minik kırmızı kum taneleri veya nar taneleri gibi çıkıntılar görülür.\n- **Taneciklerin Biyolojik Sırrı (Sınav Spotu):** Bu minik granüllerin her biri, dikey olarak yukarıya doğru tomurcuklanan **yeni bir kılcal damar yumağını (kapiller ilmek)** ve etrafındaki fibroblast kümesini temsil eder.\n- **Klinik Değerlendirme:** Cerrahlar yara yatağında granülasyon dokusunu gördüklerinde sevinirler; çünkü bu doku yaranın enfeksiyondan arındığını ve hızla kapandığını kanıtlar. Cilt greftleri ancak iyi bir granülasyon yatağı üzerine tutunabilir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "İnfekte / Nekrotik Yara Yatağı vs Sağlıklı Granülasyon Yatağı",
                "Nekrotik Yara (İyileşmeyen)",
                "Sarı-gri renkli püy tabakası, kötü koku, avasküler soluk zemin; greft tutmaz.",
                "Sağlıklı Granülasyon Dokusu",
                "Canlı kırmızı/pembe, parlak tanecikli kadife görünüm, temiz zemin; greftleme için mükemmel."
            ),
            make_recall(
                "Granülasyon dokusunun yara yüzeyinde oluşturduğu kırmızı tanecikli (granüler) görünümün mikroskobik temeli nedir?",
                "Yüzeye doğru dik açıyla tomurcuklanan yeni kılcal damar ilmekleri (kapiller loop'lar) ve bu damarların etrafını saran fibroblast kümeleridir."
            )
        ]
    })

    # Slide 34
    slides.append({
        "id": "k1-15-s34",
        "title": "Proliferasyon Evresinde Fibroblastların Göçü ve Çoğalması",
        "content": "Granülasyon dokusunun protein sentez fabrikaları fibroblastlardır:\n\n- **Yara Yatağına Çağrı:** Yara çevresindeki sağlam dermis ve fasya dokusunda uykuda olan yerel fibroblastlar uyarılır. Ayrıca kemik iliğinden gelen fibrositler de alana göç eder.\n- **Kilit Kemotaktik ve Mitojenik Faktörler (Sınav Spotu):**\n  - **PDGF (Trombosit Kaynaklı Büyüme Faktörü):** Fibroblastları yara merkezine doğru çeken (kemotaksis) ve bölünmelerini sağlayan en güçlü mitojendir.\n  - **FGF-2 (Fibroblast Büyüme Faktörü):** Fibroblast göçünü ve proliferasyonunu şiddetle uyarır.\n  - **TGF-β:** Fibroblastların çoğalmasından ziyade **kollajen ve matriks üretimine kilitlenmesini** sağlar.\n- **Hücresel Değişim:** Fibroblastlar aktif hale geldikçe endoplazmik retikulumları devasa boyutlara ulaşır; bol miktarda fibronektin, proteoglikan ve pro-kollajen sentezleyerek doku açığını doldururlar.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Fibroblastların Yara Yatağındaki Aktivasyon Basamakları",
                [
                    "1. Kemotaktik Çekim: PDGF ve FGF sinyalleriyle çevre dokudaki fibroblastlar uyarılır.",
                    "2. Yaranın İçine Göç: Fibroblastlar integrinleriyle fibrin otoyoluna tutunarak merkeze ilerler.",
                    "3. Hücresel Proliferasyon: Büyüme faktörlerinin etkisiyle fibroblastlar hızla bölünür.",
                    "4. Tip III Kollajen Sentezi: Hücreler bol miktarda erken dönem Tip III kollajeni ve proteoglikan salgılar.",
                    "5. Doku İskeletinin Kurulması: Gevşek matriks alanı doldurur ve gerilme kuvveti kazandırmaya başlar."
                ]
            ),
            make_cloze(
                "Yara iyileşmesinde fibroblastların hasar alanına göçünü ve mitozunu uyaran en güçlü faktör trombosit kaynaklı büyüme faktörüdür.",
                "trombosit",
                "PDGF kısaltmasının açılımındaki ilk kan hücresi"
            )
        ]
    })

    # Slide 35
    slides.append({
        "id": "k1-15-s35",
        "title": "Re-epitelizasyon: Yüzeyin Kapatılması ve Temas İnhibisyonu",
        "content": "Granülasyon dokusu alttan yara boşluğunu doldururken, eşzamanlı olarak yüzey epitelinin yarayı kapatması gerekir:\n\n- **Re-epitelizasyonun Başlaması:** Kesi yapıldıktan sonraki **ilk 24-48 saat içinde**, kesi kenarlarındaki bazal keratinositler ve kıl folikülü kök hücreleri mitoza başlar.\n- **Kayan Tabaka (Sheet Migration):**\n  - Keratinositler desmozom bağlantılarını geçici olarak çözer.\n  - Fibrin pıhtısının hemen altından, granülasyon dokusunun üstünden bir çarşaf gibi yara merkezine doğru kayarlar.\n- **Temas İnhibisyonu (Contact Inhibition - Sınav Spotu):**\n  - İki karşıt yara kenarından gelen epitel hücreleri yara ortasında birbiriyle temas ettiği anda göç ve çoğalma **anında durur**.\n- **Epitelin Kalınlaşması:** Yüzey kapandıktan sonra hücreler bazal membranını salgılar, yukarıya doğru tabakalanır ve keratin üreterek normal çok katlı skuamöz epidermis katmanını yeniden oluşturur.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Epitel Göçü vs Temas İnhibisyonu",
                "Epitel Göçü (Açık Yara)",
                "Keratinositler EGF ve KGF etkisiyle pıhtı altından hızla yara ortasına doğru ilerler.",
                "Temas İnhibisyonu (Kapalı Yara)",
                "Karşıdan gelen epitel hücreleri birbirine değdiği anda çoğalma ve göç sinyali durdurulur."
            ),
            make_quiz(
                "Yara iyileşmesinde re-epitelizasyon sırasında karşıt kenarlardan göç eden keratinositlerin yara merkezinde bir araya geldiklerinde çoğalmayı ve ilerlemeyi durdurması mekanizmasına ne ad verilir?",
                [
                    {"key": "A", "text": "Temas inhibisyonu (Contact inhibition)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Normal hücreler karşı hücreyle fiziksel temas kurduğunda çoğalmayı durdurur; kanser hücrelerinde ise temas inhibisyonu kaybolmuştur."},
                    {"key": "B", "text": "Miyofibroblast kontraksiyonu", "isCorrect": False, "explanation": "Bu yaranın bağ dokusuyla büzülmesidir."},
                    {"key": "C", "text": "Eferositoz", "isCorrect": False, "explanation": "Eferositoz apoptotik hücrelerin makrofajlarca yutulmasıdır."},
                    {"key": "D", "text": "Anjiyogenez tomurcuklanması", "isCorrect": False, "explanation": "Damar oluşumudur."}
                ]
            )
        ]
    })

    # Slide 36
    slides.append({
        "id": "k1-15-s36",
        "title": "Granülasyon Dokusunda Kapiller Geçirgenlik ve Ödem",
        "content": "Granülasyon dokusunun histolojisindeki en çarpıcı özelliklerden biri yoğun doku ödemidir (Sınav Spotu):\n\n- **Neden Yeni Kılcallar Bu Kadar Geçirgendir?**\n  - Anjiyogenez sırasında oluşan yeni endotel hücreleri arasında henüz sıkı intersellüler bağlantılar (tight junction'lar) kurulmamıştır.\n  - Yeni damarların etrafını saran perisit tabakası eksiktir veya henüz gevşektir.\n  - Ayrıca ortamda yüksek konsantrasyonda **VEGF (Vasküler Endotel Büyüme Faktörü)** bulunur; VEGF'in tarihi adı **Vasküler Geçirgenlik Faktörüdür (VPF)** ve damar geçirgenliğini histaminden 50.000 kat daha güçlü artırır!\n- **Klinik Sonuç:**\n  - Plazma proteinleri ve sıvı sürekli damar dışına sızar.\n  - Bu nedenle genç granülasyon dokusu ve iyileşen yaralar **daima ödemlidir**.\n  - Bu ödem iyileşmenin doğal bir parçasıdır; lökositlerin ve besinlerin dokuya akışını kolaylaştırır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Olgun Normal Kapiller vs Genç Granülasyon Kapilleri",
                "Olgun Kapiller (Normal Doku)",
                "Sıkı endotel bağlantıları, tam perisit kılıfı ve bazal membran vardır; plazma sızdırmaz.",
                "Genç Granülasyon Kapilleri",
                "Gevşek endotel aralıkları ve yüksek VEGF etkisiyle sürekli plazma ve protein sızdırır; doku ödemlidir."
            ),
            make_cloze(
                "Granülasyon dokusundaki yeni damarların aşırı geçirgen olmasının temel nedeni eksik endotel bağlantıları ve yüksek VEGF düzeyidir.",
                "VEGF",
                "Vasküler geçirgenliği de artıran anahtar endotel büyüme faktörü"
            )
        ]
    })

    # Slide 37
    slides.append({
        "id": "k1-15-s37",
        "title": "Granülasyon Dokusu vs Granülomatöz Enflamasyon",
        "content": "Tıp fakültesi öğrencilerinin ve asistanların sınavlarda en çok karıştırdığı iki kavram isim benzerliğinden kaynaklanır (Kritik Sınav Tuzağı):\n\n- **1. Granülasyon Dokusu (Granulation Tissue):**\n  - Bir kronik iltihap türü DEĞİLDİR!\n  - Bu bir **doku onarımı (tamir) yapısıdır**.\n  - Bileşenleri: Yeni kılcal damarlar (anjiyogenez), prolifere fibroblastlar, ödem ve gevşek ECM.\n- **2. Granülomatöz Enflamasyon (Granulomatous Inflammation):**\n  - Bir onarım dokusu DEĞİLDİR!\n  - Bu özel bir **kronik enflamasyon formudur**.\n  - Bileşenleri: Sindirilemeyen antijen etrafında toplanmış **epiteloid histiyositler (makrofajlar)**, çok çekirdekli dev hücreler (Langhans, yabancı cisim) ve çevresinde lenfosit yakası.\n  - Örnek: Tüberküloz kazeöz granülomu, sarkoidoz, yabancı cisim granülomu.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Özellik", "Granülasyon Dokusu", "Granülomatöz Enflamasyon"],
                [
                    ["Süreç Tipi", "Fizyolojik doku ONARIMI", "Özel KRONİK İLTİHAP"],
                    ["Baskın Hücre", "Fibroblastlar ve Endotel hücreleri", "Epiteloid makrofajlar ve Dev hücreler"],
                    ["Vaskülarizasyon", "Aşırı zengin yeni kapillerler (anjiyogenez)", "Genellikle damardan fakir (avasküler merkez)"],
                    ["Klinik Örnek", "İyileşen cerrahi yara tabanı", "Tüberküloz, Sarkoidoz, Sifiliz granülomu"]
                ]
            ),
            make_quiz(
                "Patolojide 'granülasyon dokusu' ile 'granülomatöz enflamasyon' arasındaki temel kavramsal fark aşağıdakilerden hangisidir?",
                [
                    {"key": "A", "text": "Her ikisi de aynı şeydir, eş anlamlı terimlerdir", "isCorrect": False, "explanation": "Tamamen farklı iki patolojik antitedir."},
                    {"key": "B", "text": "Granülasyon dokusu anjiyogenez ve fibroblastlarla giden bir doku onarımı yapısıyken; granülomatöz enflamasyon epiteloid makrofaj ve dev hücrelerle karakterize özel bir kronik yangıdır", "isCorrect": True, "explanation": "Doğru cevap B'dir: Granülasyon dokusu onarımdır; granülomatöz enflamasyon ise kronik iltihaptır."},
                    {"key": "C", "text": "Granülasyon dokusu yalnız tüberkülozda görülür", "isCorrect": False, "explanation": "Tüberkülozda granülomatöz iltihap görülür; granülasyon dokusu her yarada oluşur."},
                    {"key": "D", "text": "Granülomatöz enflamasyon yalnız yeni damarlardan oluşur", "isCorrect": False, "explanation": "Granülom epiteloid makrofaj yumağıdır."}
                ]
            )
        ]
    })

    # Slide 38
    slides.append({
        "id": "k1-15-s38",
        "title": "Aşırı Granülasyon Dokusu: Eksüberan Granülasyon (Proud Flesh)",
        "content": "Granülasyon dokusu hayat kurtarıcı bir onarım yapısıdır; ancak miktarı doğru ayarlanamazsa patolojik bir engele dönüşür:\n\n- **Eksüberan Granülasyon (Proud Flesh / Vahşi Et - Sınav Spotu):**\n  - Yara iyileşmesi sırasında granülasyon dokusunun kontrolsüz ve aşırı miktarda çoğalarak **yara yüzey seviyesinin üzerine taşması (kabarması)** durumudur.\n  - Veteriner hekimlikte at bacak yaralarında çok sık görülür; insanlarda da sekonder iyileşen derin yaralarda karşımıza çıkar.\n- **Klinik Sorun:** Yaranın üzerinde kabaran bu aşırı et kitlesi, kenarlardan ilerleyen **keratinositlerin yolunu tıkar ve re-epitelizasyonu fiziksel olarak engeller!** Yara aylarca kapanamaz.\n- **Tedavi:** Cerrah bu aşırı granülasyon dokusunu bistüri ile kazıyarak (küretaj) veya gümüş nitrat koterizasyonu ile yakarak normal deri seviyesine indirir; ardından epitel hızla yarayı örter.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal Granülasyon Dokusu vs Eksüberan Granülasyon (Proud Flesh)",
                "Normal Granülasyon Dokusu",
                "Yara boşluğunu deri seviyesine kadar doldurur; epitelin üzerinden kaymasına izin verir.",
                "Eksüberan Granülasyon (Proud Flesh)",
                "Deri seviyesinin üzerine taşarak kabarır; epitelin ilerlemesini mekanik olarak bloke eder."
            ),
            make_cloze(
                "Granülasyon dokusunun yara yüzeyinin üzerine taşarak epitelizasyonu engellemesine eksüberan granülasyon denir.",
                "eksüberan",
                "Aşırı taşan granülasyon dokusu sıfatı"
            )
        ]
    })

    # Slide 39 - CHECKPOINT 4
    slides.append({
        "id": "k1-15-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Granülasyon Dokusu ve Proliferasyon Fazı (3–10. Gün)",
        "content": "Bu checkpointte proliferatif evrenin ve granülasyon dokusunun kilit prensiplerini özetliyoruz:\n\n- **Zaman Dilimi:** 3. günden itibaren başlar, 7-10. günlerde doruğa ulaşır.\n- **Üçlü Histoloji:** (1) Yeni kapillerler (anjiyogenez), (2) Prolifere fibroblastlar, (3) Ödemli gevşek ECM ve makrofajlar.\n- **Makroskopi:** Canlı kırmızı, pembe, granüler (nar tanesi gibi), kolay kanayan kadife örtü.\n- **Fibroblast Uyaranları:** PDGF (en güçlü mitojen) ve FGF.\n- **Re-epitelizasyon:** Keratinositlerin pıhtı altından kayması; karşı hücreyle karşılaşınca **temas inhibisyonu** ile durması.\n- **Ödem Nedeni:** Yeni kapillerlerin eksik endotel bağlantıları ve yüksek VEGF/VPF seviyesi.\n- **Granülasyon vs Granülom:** Granülasyon dokusu onarımdır; granülomatöz enflamasyon (epiteloid histiyositler) kronik yangıdır.\n- **Eksüberan Granülasyon:** Yüzeyin üzerine taşan aşırı granülasyon dokusu epitelizasyonu engeller.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Patolojik Antite", "Biyolojik Doğası", "Mikroskopik Görünüm", "Klinik Tedavi / Anlam"],
                [
                    ["Granülasyon Dokusu", "Fizyolojik onarım dokusu", "Yeni kapillerler + Fibroblastlar + Ödem", "Sağlıklı yara iyileşmesi göstergesi"],
                    ["Granülomatöz Enflamasyon", "Özel kronik iltihap", "Epiteloid makrofajlar + Dev hücreler", "Spesifik etken tedavisi (tüberküloz ilacı)"],
                    ["Eksüberan Granülasyon", "Aşırı taşan onarım dokusu", "Yara seviyesi üstünde kabarık kapillerler", "Cerrahi küretaj veya gümüş nitrat koter"]
                ]
            ),
            make_chain(
                "Proliferasyon Evresinin 4 Senkronize Olayı",
                [
                    "1. Anjiyogenez Başlangıcı: VEGF uyarısıyla yara tabanından kılcal tomurcuklar çıkar.",
                    "2. Fibroblast Akını: PDGF etkisiyle fibroblastlar Tip III kollajen sentezlemeye başlar.",
                    "3. Re-epitelizasyon: Keratinositler yara yüzeyini örtmek için çarşaf gibi ilerler.",
                    "4. Temas İnhibisyonu: Epitel birleştiğinde göç durur ve yüzey keratinleşir."
                ]
            )
        ]
    })

    # Slide 40
    slides.append({
        "id": "k1-15-s40",
        "title": "Mini Vaka: Diyabetik Ayak Ülserinde Granülasyon Dokusu Takibi",
        "content": "62 yaşında tip 2 diyabet hastasının sağ topuğunda 4 cm çapında derin nöropatik ayak ülseri bulunuyor. Ülser tabanındaki enfeksiyon ve sarı nekrotik dokular cerrahi debridmanla temizleniyor:\n\n- **1. Hafta:** Uygun pansuman ve kan şekeri regülasyonu sonrası yara tabanında parlak kırmızı, nar tanesi görünümünde minik kabarıklıklar (granülasyon dokusu) belirmeye başlıyor.\n- **2. Hafta:** Granülasyon dokusu derin doku açığını tamamen doldurarak yara kenarları seviyesine ulaşıyor.\n- **3. Hafta:** Yara kenarlarından pembemsi ince bir epitel tabakasının (keratinosit çarşafı) granülasyon dokusunun üzerini örterek ilerlediği (re-epitelizasyon) izleniyor.\n- **Klinik Başarı:** Sağlıklı granülasyon dokusu sayesinde ülser ampütasyona gitmeden başarıyla kapanıyor.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Klinik Karar: Diyabetik Ülserde Yara Yatağı Yönetimi",
                "Hastanın yarasında granülasyon dokusu gelişirken, yara yüzeyinde hafif sarımsı pıhtılaşmış bir eksuda görülüyor. Pansuman hemşiresi sert bir fırçayla tüm granülasyon dokusunu kanatarak kazımak istiyor. Hekim olarak tavrınız ne olmalıdır?",
                [
                    {
                        "text": "'Evet, yara tabanındaki tüm pembe tomurcukları sertçe fırçalayarak kemiğe kadar kazıyalım.'",
                        "outcome": "Büyük klinik hata: Hassas yeni kılcal damarlar yırtılır, doku iskemize olur ve iyileşme haftalarca geriye gider.",
                        "isCorrect": False
                    },
                    {
                        "text": "'Durun! O pembe tanecikli doku sağlıklı granülasyon dokusudur; sert kazıma yapılmamalı, sadece yüzeydeki gevşek eksuda nazikçe SF ile yıkanmalı ve granülasyon dokusu korunmalıdır.'",
                        "outcome": "Kusursuz yara bakımı prensibi: Granülasyon dokusu korunur, re-epitelizasyon güvenle sürer.",
                        "isCorrect": True
                    },
                    {
                        "text": "'Bacağın derhal diz üstünden kesilmesini emredelim.'",
                        "outcome": "Gereksiz malpraktis.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu diyabetik ülser vakasında yara tabanında oluşan parlak pembe granülasyon dokusunun hastanın iyileşmesindeki en kritik görevi nedir?",
                [
                    {"key": "A", "text": "Derin doku açığını doldurarak yeni damarlarla beslemek ve re-epitelizasyon için zemin hazırlamak", "isCorrect": True, "explanation": "Doğru cevap A'dır: Granülasyon dokusu derin yaralarda anatomik boşluğu doldurur, anjiyogenez sağlar ve epitelin ilerleyebileceği vasküler bir yatak kurar."},
                    {"key": "B", "text": "Kemik iliğinde alyuvar yıkımını durdurmak", "isCorrect": False, "explanation": "Sistemik kan yıkımıyla ilgisi yoktur."},
                    {"key": "C", "text": "Hastada insülin salgısını tamamen kesmek", "isCorrect": False, "explanation": "Diyabet patolojisiyle doğrudan ilgili değildir."},
                    {"key": "D", "text": "Yara kenarlarını birbirinden sonsuza dek uzaklaştırmak", "isCorrect": False, "explanation": "Tam tersine yarayı kapatmaya çalışır."}
                ]
            )
        ]
    })

    return slides
