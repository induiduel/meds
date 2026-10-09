# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_5_slides():
    slides = []

    # Slide 41
    slides.append({
        "id": "k1-13-s41",
        "title": "Granülomatöz Enflamasyonun Tanımı ve Biyolojik Amacı",
        "content": "Granülomatöz enflamasyon, kronik enflamasyonun son derece özel, kendine has morfolojik bir alt tipidir:\n\n- **Tanım:** Temelini aktive makrofajların (epiteloid histiositlerin) oluşturduğu, çevresinde lenfositlerin yer aldığı, sıklıkla çok çekirdekli dev hücreler ve bazen merkezi nekroz içeren mikroskobik nodüler hücresel kümelenmelere **granülom** denir.\n- **Biyolojik Mantık (Hücresel İzolasyon):** Vücut fagositozla yok edemediği, sindirime dirençli bir mikroorganizmayı (tüberküloz basili) ya da yabancı cismi (dikiş ipliği, silika) tamamen yok edemeyeceğini anladığında onu dokudan izole etmeye karar verir.\n- **Bir Karantina Duvarı:** Granülom adeta bir biyolojik cezaevi veya karantina koğuşudur; zararlı etkeni hapsederek çevreye ve diğer organlara yayılmasını sınırlar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Diffüz Kronik Yangı vs Granülomatöz Yangı",
                "Diffüz Kronik Enflamasyon",
                "Hücreler doku aralıklarına gevşekçe yayılmıştır; etkeni sınırlayıcı belirgin nodüler duvar yoktur.",
                "Granülomatöz Enflamasyon",
                "Epiteloid hücreler sıkı nodüler kordonlar kurarak etkeni fiziksel ve kimyasal karantinaya alır."
            ),
            make_cloze(
                "Granülomatöz enflamasyon vücudun fagositozla eritemediği dirençli etkenleri çevre dokudan izole etmek için geliştirdiği bir karantina stratejisidir.",
                "karantina",
                "Zararlı etkenin yayılımını engelleyen izolasyon yaklaşımı"
            )
        ]
    })

    # Slide 42
    slides.append({
        "id": "k1-13-s42",
        "title": "Granülomun Hücresel Mimarisi: Merkezden Perifere Tabakalar",
        "content": "Tipik bir granülom mikroskop altında merkezden dışa doğru konsantrik tabakalanma sergiler:\n\n1. **Merkez (Çekirdek):** Zararlı etkenin yer aldığı bölgedir. Tüberkülozda burada amorf pembe **kazeifikasyon nekrozu** bulunur; yabancı cisim granülomlarında yabancı materyal yer alır; sarkoidozda ise merkez asellüler nekroz içermez.\n2. **Orta Kuşak (Epiteloid Hücre Zonu):** Granülomun hacmini oluşturan ana katmandır. Birbirine sıkıca yaslanmış bol pembe sitoplazmalı **epiteloid histiositler** ve bunların kaynaşmasıyla oluşan **çok çekirdekli dev hücreler**.\n3. **Periferik Kuşak (Lenfosit Manto Tabakası):** Çevreyi bir yüzük gibi saran CD4+ ve CD8+ lenfositler, plazma hücreleri.\n4. **En Dış Sınır (Fibröz Kapsül):** Zamanla fibroblastların biriktirdiği konsantrik kollajen lif demetleri.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Granülomun Merkezden Dışa Anatomik Tabakalanması",
                [
                    "1. Santral Merkez: Etken ve olası kazeöz nekroz çekirdeği bulunur.",
                    "2. Epiteloid Bariyer: Sıkı paketlenmiş epiteloid histiositler ve dev hücreler duvar örer.",
                    "3. Lenfosit Kuşağı: Çevrede nöbet tutan T ve B lenfosit mantosu yer alır.",
                    "4. Fibröz Sınır: En dışta fibroblastlar kollajen sentezleyerek granülomu dokudan tamamen ayırır."
                ]
            ),
            make_quiz(
                "Klasik bir granülom yapısında lezyonun ana kütlesini oluşturan ve etkeni çepeçevre saran temel hücre tipi hangisidir?",
                [
                    {"key": "A", "text": "Epiteloid histiositler (aktive makrofajlar)", "explanation": "A seçeneği DOĞRUDUR: Granülomun mimari yapıtaşı epiteloid makrofajlardır."},
                    {"key": "B", "text": "Nötrofil lökositler", "explanation": "B seçeneği yanlıştır: Akut hücrelerdir, klasik granülom gövdesini oluşturmazlar."},
                    {"key": "C", "text": "Endotel hücreleri", "explanation": "C seçeneği yanlıştır: Damar duvarı hücresidir."},
                    {"key": "D", "text": "Eritrositler", "explanation": "D seçeneği yanlıştır: Damar içi oksijen taşıyıcılarıdır."},
                    {"key": "E", "text": "Bazofiller", "explanation": "E seçeneği yanlıştır: Dolaşımdaki vazoaktif granülositlerdir."}
                ],
                "A"
            )
        ]
    })

    # Slide 43
    slides.append({
        "id": "k1-13-s43",
        "title": "Epiteloid Makrofajlar: Morfoloji ve Fonksiyonel Dönüşüm",
        "content": "Granülomun temel yapıtaşı olan epiteloid hücreler, T lenfositlerinden gelen yoğun sitokin bombardımanı sonucu şekil ve görev değiştiren makrofajlardır:\n\n- **Neden 'Epiteloid' Denir?** Işık mikroskobunda yassı veya prizmatik epitel hücrelerine benzedikleri için bu isim verilmiştir. Hücre sınırları birbirine öylesine sıkı yaslanır ki aradaki sınır silikleşir (sinsityum benzeri görünüm).\n- **Morfolojik Özellikler (Sınav Spotu):**\n  - Bol, soluk eozinofilik (pembe), granüler sitoplazma.\n  - Geniş, oval veya veziküler, nükleolus içeren, açık renkli 'terlik tabanı' ya da 'muz' şeklinde çekirdek.\n- **Fonksiyonel Makas Değişimi:** Bu hücreler fagositoz yeteneklerini büyük ölçüde kaybetmişlerdir; buna karşın **sekretuar (salgılayıcı) ve bariyer oluşturucu** kapasiteleri kat kat artmıştır. Sürekli TNF-α, enzim ve kemokin salgılarlar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Sıradan Doku Makrofajı vs Epiteloid Makrofaj",
                "Sıradan Makrofaj",
                "Düzensiz psödopotlu, yoğun fagositoz yapan, vakuollü amipsi hücredir.",
                "Epiteloid Makrofaj",
                "Bol pembe sitoplazmalı, epitel benzeri sıkı dizilen, fagositozu azalmış sekresyonu artmış hücredir."
            ),
            make_cloze(
                "Granülomdaki aktive makrofajlar bol pembe sitoplazmaları ve birbirine sıkıca kenetlenen sınırları nedeniyle epiteloid histiosit adını alırlar.",
                "epiteloid histiosit",
                "Epitel benzeri makrofajların patolojik adı"
            )
        ]
    })

    # Slide 44
    slides.append({
        "id": "k1-13-s44",
        "title": "Çok Çekirdekli Dev Hücrelerin Oluşumu ve Makrofaj Füzyonu",
        "content": "Granülom kesitlerinde 40-50 mikron hatta 100 mikron çapa ulaşabilen, içerisinde onlarca çekirdek barındıran devasa hücreler izlenir:\n\n- **Oluşum Mekanizması:** Dev hücreler çekirdeğin anormal bölünmesiyle (amitoz) DEĞİL, birden fazla aktive makrofajın hücre zarlarının **birbiriyle kaynaşması (füzyon)** sonucu meydana gelir!\n- **Füzyon Sinyalleri:** Th1 lenfositlerinden salınan **IFN-γ** ve makrofaj kökenli **IL-4 / IL-13** gibi sitokinler hücre zarındaki füzyon reseptörlerini (CD44, DC-STAMP ve makrofaj füzyon reseptörü MFR) aktive eder.\n- **Biyolojik Amaç:** Tek bir makrofajın yutamayacağı büyüklükteki yabancı cisimleri veya mikobakteri kolonilerini ortak geniş bir sitoplazma içine hapsedip sınırlandırmaktır.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Makrofaj Füzyonu ve Dev Hücre Oluşum Basamakları",
                [
                    "1. Yoğun Sitokin Maruziyeti: Ortamdaki yüksek IFN-gama ve IL-4 makrofaj yüzey moleküllerini değiştirir.",
                    "2. Hücre Zar Teması: Makrofajlar CD44 ve füzyon proteinleri aracılığıyla birbirine yapışır.",
                    "3. Lipid Membran Kaynaşması: Bitişik zarlar erir; sitoplazmalar tek bir dev hücrede birleşir.",
                    "4. Çok Çekirdekli Yapı: 10 ila 50 makrofaj çekirdeği ortak sitoplazma içinde özgün dizilimler kazanır."
                ]
            ),
            make_recall(
                "Granülomlarda izlenen çok çekirdekli dev hücrelerin temel hücresel kökeni ve oluşum mekanizması nedir?",
                "Aktive makrofajların (histiositlerin) hücre zarlarının birbiriyle kaynaşmasıdır (füzyon).",
                "Makrofajların birleşmesi mekanizması"
            )
        ]
    })

    # Slide 45
    slides.append({
        "id": "k1-13-s45",
        "title": "Langhans Tipi Dev Hücre: Nalsı Çekirdek Tacı",
        "content": "Granülomatöz enflamasyonda dev hücrelerin çekirdek dizilimi patoloğa etiyoloji hakkında çok değerli ipuçları verir:\n\n- **Langhans Tipi Dev Hücre Morfolojisi (Sınav Spotu):**\n  - Çok sayıda çekirdek (genellikle 15-30 adet), dev hücrenin periferinde **nal şeklinde (at nalı)** ya da yarım daire / tam çember (**taç şeklinde**) dizilmiştir.\n  - Hücrenin merkezinde ise homojen, pembe, granüler sitoplazma alanı boş kalır.\n- **Klinik Birliktelik:** En klasik olarak **Tüberküloz** (Mycobacterium tuberculosis) tüberküllerinde izlenir. Ayrıca lepra, sarkoidoz ve mantar enfeksiyonlarında da görülebilir.\n- **Kritik İsim Karışıklığı Uyarısı:** Derideki antijen sunucu dendritik hücre olan 'Langerhans hücresi' veya pankreastaki 'Langerhans adacıkları' ile KESİNLİKLE KARIŞTIRILMAMALIDIR! Bu hücrenin adı **Langhans dev hücresidir**.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Hücre / Yapı Adı", "Hücresel Köken", "Temel Görevi / Özelliği"],
                [
                    [
                        {"text": "Langhans Dev Hücresi", "isMasked": False, "hint": ""},
                        {"text": "Füzyona uğramış makrofajlar", "isMasked": True, "hint": "Çok çekirdekli granülom hücresi"},
                        {"text": "Periferik nal şeklinde dizilmiş çekirdekler (Tüberküloz)", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Langerhans Hücresi", "isMasked": True, "hint": "Epidermisteki antijen sunucu dentritik hücre"},
                        {"text": "Epidermal dentritik hücre", "isMasked": False, "hint": ""},
                        {"text": "Birbeck granülleri içeren antijen sunucu hücre", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Langerhans Adacıkları", "isMasked": False, "hint": ""},
                        {"text": "Pankreas endokrin epiteli", "isMasked": False, "hint": ""},
                        {"text": "İnsülin ve glukagon salgılayan endokrin adacık", "isMasked": True, "hint": "Kan şekerini düzenleyen bez"}
                    ]
                ]
            ),
            make_quiz(
                "Akciğer biyopsisinde granülom periferinde çekirdekleri 'at nalı' şeklinde dizilmiş çok çekirdekli dev hücrelere ne ad verilir?",
                [
                    {"key": "A", "text": "Langhans tipi dev hücre", "explanation": "A seçeneği DOĞRUDUR: Periferik nal/taç dizilimli dev hücre tüberkülozun klasik Langhans hücresidir."},
                    {"key": "B", "text": "Langerhans hücresi", "explanation": "B seçeneği yanlıştır: Deri epidermisinde Birbeck granüllü dentritik hücredir."},
                    {"key": "C", "text": "Touton dev hücresi", "explanation": "C seçeneği yanlıştır: Ksantomlarda kolesterol halkalı dev hücredir."},
                    {"key": "D", "text": "Osteoklast", "explanation": "D seçeneği yanlıştır: Kemik rezorpsiyon dev hücresidir."},
                    {"key": "E", "text": "Aschoff hücresi", "explanation": "E seçeneği yanlıştır: Akut romatizmal karditte görülen miyokard histiositidir."}
                ],
                "A"
            )
        ]
    })

    # Slide 46
    slides.append({
        "id": "k1-13-s46",
        "title": "Yabancı Cisim Tipi Dev Hücre: Düzensiz Çekirdek Dağılımı",
        "content": "İmmünolojik olmayan veya inert yabancı materyallerin dokuya girmesiyle oluşan dev hücreler Langhans tipinden farklı bir yerleşim sergiler:\n\n- **Morfoloji (Sınav Spotu):** Çekirdekler hücrenin periferinde düzenli bir nal oluşturmaz; sitoplazmanın **her tarafına düzensiz, kaotik ve rastgele dağılmıştır** (sitoplazmada kümelenmiş veya serpintili).\n- **İçerik:** Dev hücrenin sitoplazması içinde fagositozla sarılmış cerrahi sütür parçası, talk pudrası partikülleri veya ahşap kıymığı doğrudan görülebilir.\n- **Görüldüğü Durumlar:** Ameliyat sonrası dikiş granülomları, intravenöz uyuşturucu bağımlılarında talk granülomları, göze veya deriye batan yabancı cisimler.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Langhans Tipi vs Yabancı Cisim Tipi Dev Hücre",
                "Langhans Dev Hücresi (İmmün Granülom)",
                "Çekirdekler hücre kenarında at nalı veya taç şeklinde düzenli bir çember oluşturur.",
                "Yabancı Cisim Dev Hücresi (Non-immün Granülom)",
                "Çekirdekler sitoplazmanın her tarafına dağınık ve düzensiz olarak saçılmıştır."
            ),
            make_cloze(
                "Yabancı cisim tipi dev hücrelerde çekirdekler sitoplazma içinde düzensiz ve rastgele dağılım gösterir.",
                "düzensiz ve rastgele",
                "Langhans'tan farklı olan kaotik nükleer yerleşim"
            )
        ]
    })

    # Slide 47
    slides.append({
        "id": "k1-13-s47",
        "title": "Touton Tipi Dev Hücre ve Kolesterol Halkası",
        "content": "Lipid metabolizması bozukluklarında ve bazı fibrohistiositik lezyonlarda son derece özgün bir dev hücre tipi karşımıza çıkar:\n\n- **Touton Dev Hücresi Morfolojisi:**\n  - Hücrenin tam merkezinde çekirdeklerin oluşturduğu **kapalı bir halka** yer alır.\n  - Çekirdek halkasının içindeki merkezi sitoplazma eozinofilik ve homojendir.\n  - Çekirdek halkasının dışındaki periferik sitoplazma ise yoğun lipid ve kolesterol fagositozu nedeniyle **köpüksü (vakuollü / ksantomlu)** görünümdedir.\n- **Görüldüğü Lezyonlar:**\n  - **Ksantomlar (Xanthoma):** Hiperlipidemili hastalarda tendon ve ciltte gelişen lipid nodülleri.\n  - **Ksantogranülomlar:** Juvenil ksantogranülom ve böbrekte ksantogranülomatöz piyelonefrit lezyonlarında tanısal anahtar hücredir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Diz tendonları üzerinde sarı renkli nodülleri olan ve hiperkolesterolemi tanısıyla takip edilen hastanın deri lezyon biyopsisinde merkezde çekirdek halkası, periferde köpüksü sitoplazması olan dev hücreler izleniyor.",
                "Ksantom lezyonlarında karakteristik olan ve bu morfolojiyi sergileyen dev hücre tipi hangisidir?",
                [
                    {
                        "text": "Touton tipi dev hücredir.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! Touton dev hücresi çekirdek halkasını çevreleyen köpüksü lipidli dış sitoplazmasıyla ksantomların tipik hücresidir."
                    },
                    {
                        "text": "Langhans tipi dev hücredir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Langhans tüberkülozda görülür, köpüksü lipid halkası içermez."
                    },
                    {
                        "text": "Reed-Sternberg hücresidir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Hodgkin lenfomanın baykuş gözü çekirdekli malign neoplastik hücresidir."
                    }
                ]
            ),
            make_recall(
                "Merkezde çekirdek halkası ve etrafında köpüksü lipid vakuolleri içeren sitoplazması ile ksantomlarda saptanan dev hücre tipi nedir?",
                "Touton tipi dev hücresidir.",
                "Lipid ilişkili halkasal çekirdekli dev hücre"
            )
        ]
    })

    # Slide 48
    slides.append({
        "id": "k1-13-s48",
        "title": "Granülomun Manto Kuşağı: Lenfositler ve Fibroblastlar",
        "content": "Granülomun etrafını saran manto kuşağı, içeride hapsedilen etkenin dışarı sızmasını engelleyen nöbetçi kordonudur:\n\n- **Lenfosit Mantosu:** Epiteloid hücrelerin hemen dışını çevreleyen bu kuşakta **CD4+ Th1 hücreleri, sitotoksik CD8+ T hücreleri ve plazma hücreleri** bulunur. Bu lenfositler içeriye sürekli IFN-γ pompalayarak epiteloid bariyerin diri kalmasını sağlar.\n- **Fibroblastik Duvar:** En dış tabakada, makrofaj kaynaklı TGF-β uyarısıyla toplanan fibroblastlar konsantrik kollajen lif demetleri örer.\n- **İyileşme Akıbeti:** Granülom zamanla canlılığını kaybedip söndüğünde bu fibröz duvar içeriye doğru ilerler; granülom tamamen kalsifiye ve hyalinize bir **fibröz skara** (nodüle) dönüşerek iyileşir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Aktif Canlı Granülom vs İyileşmiş / Skarlaşmış Granülom",
                "Aktif Granülom",
                "Canlı epiteloid hücreler, aktif lenfosit mantosu ve nekroz; sürekli sitokin salınımı mevcuttur.",
                "İyileşmiş Skarlaşmış Granülom",
                "Hücreler kaybolmuş, yerini yoğun asellüler kollajen ve distrofik kalsifikasyon almıştır."
            ),
            make_cloze(
                "Granülom çevresinde yer alan fibroblastların ördüğü kollajen lifler zamanla lezyonun fibröz skar ve kalsifikasyon ile iyileşmesini sağlar.",
                "fibröz skar",
                "Granülomun sonlandığında bıraktığı sert bağ dokusu kalıntısı"
            )
        ]
    })

    # Slide 49
    slides.append({
        "id": "k1-13-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Granülom Mimarisi, Epiteloid Hücreler ve Dev Hücre Tipleri",
        "content": "Bu kontrol noktasında granülomatöz enflamasyonun temel hücresel mimarisini ve dev hücre tiplerini pekiştiriyoruz:\n\n- **Granülom:** Epiteloid histiositlerin oluşturduğu nodüler izolasyon yapısı.\n- **Epiteloid Hücre:** IFN-γ ile aktive olmuş, bol pembe sitoplazmalı, fagositozu azalmış sekresyonu artmış makrofaj.\n- **Dev Hücre Mekanizması:** Çekirdek bölünmesi değil, 10-50 makrofajın hücre zarlarının füzyonu.\n- **Langhans Dev Hücresi:** At nalı / taç şeklinde periferik çekirdek dizilimi (Tüberküloz, sarkoidoz).\n- **Yabancı Cisim Dev Hücresi:** Sitoplazmada düzensiz, kaotik dağılmış çekirdekler (Dikiş, talk).\n- **Touton Dev Hücresi:** Ortada çekirdek halkası, periferde köpüksü lipidli dış sitoplazma (Ksantomlar).\n- **Manto Tabakası:** Çevredeki T lenfosit kuşağı ve en dıştaki fibroblastik kollajen kapsül.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Granülom oluşumunda makrofajların epiteloid hücrelere dönüşmesini ve füzyonla dev hücre oluşturmasını sağlayan primer immün sitokin hangisidir?",
                [
                    {"key": "A", "text": "İnterferon-gama (IFN-γ)", "explanation": "A seçeneği DOĞRUDUR: IFN-gama epiteloid dönüşümün ve makrofaj füzyonunun tepe sitokinidir."},
                    {"key": "B", "text": "İnterlökin-10", "explanation": "B seçeneği yanlıştır: Anti-enflamatuar sitokindir."},
                    {"key": "C", "text": "Eotaksin", "explanation": "C seçeneği yanlıştır: Eozinofil kemokinidir."},
                    {"key": "D", "text": "Heparin", "explanation": "D seçeneği yanlıştır: Antikoagülandır."},
                    {"key": "E", "text": "Histamin", "explanation": "E seçeneği yanlıştır: Vazoaktif amindir."}
                ],
                "A"
            ),
            make_cloze(
                "Granülomlardaki çok çekirdekli dev hücreler amitoz bölünmeyle değil çok sayıda aktive makrofajın hücre zarlarının füzyonu sonucu meydana gelir.",
                "hücre zarlarının füzyonu",
                "Dev hücre oluşumunun hücresel birleşme mekanizması"
            )
        ]
    })

    # Slide 50
    slides.append({
        "id": "k1-13-s50",
        "title": "Granülomun İmmünolojik Omurgası: CD4+ / IFN-γ / TNF-α Aksı",
        "content": "Granülom gelişiminin ve dokuda hayatta kalmasının arkasında kusursuz bir immünolojik aks yatar:\n\n1. **Antijenik Tanıma:** Makrofaj sindiremediği mikobakteriyi CD4+ naif T hücresine sunar; IL-12 salgılar.\n2. **Th1 Farklılaşması:** T hücresi Th1 soyuna farklılaşır ve bol miktarda **IFN-γ** üretir.\n3. **Epiteloidleşme:** IFN-γ makrofajları epiteloid histiositlere çevirir ve füzyonu tetikler.\n4. **TNF-α ile Bütünlüğün Korunması (Sınav Spotu):** Makrofajlardan salınan **Tümör Nekroz Faktörü (TNF-α)**, granülomun bir arada durmasını sağlayan 'çimento'dur. TNF-α reseptörleri bloke edildiğinde granülom dağılır ve basiller vücuda saçılır!",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Granülomun İmmünolojik Kurulum Zinciri",
                [
                    "1. Antijenik Karşılaşma: Makrofaj dirençli mikrobu fagositozla alır ve IL-12 salgılar.",
                    "2. Th1 ve IFN-gama: CD4+ Th1 hücreleri ortama yüksek dozda IFN-gama salgılar.",
                    "3. Epiteloid Dönüşüm: Makrofajlar pembe epiteloid kordonlara ve Langhans dev hücrelerine evrilir.",
                    "4. TNF-alfa ile Harçlama: Salgılanan TNF-alfa granülomun yapısal bütünlüğünü korur ve basili hapseder."
                ]
            ),
            make_recall(
                "Granülomun mimari bütünlüğünü koruyan ve ilaçlarla bloke edildiğinde latent tüberkülozun reaktivasyonuna yol açan kilit sitokin hangisidir?",
                "Tümör Nekroz Faktörüdür (TNF-α).",
                "Granülomun harcı sayılan majör pro-enflamatuar sitokin"
            )
        ]
    })

    return slides
