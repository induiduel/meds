"""
Section 8: Protein Homeostazı (Proteostazis) ve Nörodejenerasyon (Slayt 71 - 80)
"""
from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_8_slides():
    slides = []

    # Slide 71
    slides.append({
        "id": "k1-08-s71",
        "title": "Proteostazis Ağı: Hücresel Protein Dengesi",
        "subtitle": "Protein sentezi, şaperon aracılı katlanma, otofaji ve proteazomal yıkım dengesi",
        "badge": "Protein Biyolojisi",
        "badgeColor": "indigo",
        "coreContent": {
            "text": (
                "**Proteostazis** (protein homeostazı), hücrenin fonksiyonel bir proteom sürdürebilmek için yürüttüğü "
                "biyosentez, katlanma, taşınma ve proteolitik yıkım süreçlerinin kusursuz entegrasyonudur.\n\n"
                "Proteostazis ağının iki ana ayağı:\n"
                "1. **Katlanma Desteği:** Şaperon proteinleri (Hsp70, Hsp90, şaperoninler).\n"
                "2. **Temizlik ve Yıkım:** Ubiquitin-Proteazom Sistemi (==UPS==) ve Otofaji-Lizozom yolağı.\n\n"
                "> Yaşlanma boyunca bu dengenin çökmesi protein agregasyonuna ve hücresel disfonksiyona yol açar."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Hücrede fonksiyonel protein dengesini koruyan karmaşık sisteme proteostazis ağı adı verilir.",
                "proteostazis",
                "Protein homeostazı kavramı"
            ),
            make_active_recall(
                "Proteostazis ağının çökmesinin yaşlanan hücrede oluşturduğu en tehlikeli iki sonuç nedir?",
                "1) Normal proteinlerin fonksiyonel kaybı ve 2) Katlanamayan toksik protein agregatlarının birikerek ER stresi ve apoptozu tetiklemesidir."
            )
        ]
    })

    # Slide 72
    slides.append({
        "id": "k1-08-s72",
        "title": "Yaşlanmayla Şaperon Kapasitesinin Zayıflaması",
        "subtitle": "Isı şok proteinlerinin (Hsp70, Hsp90) ekspresyon kaybı ve katlanma defektleri",
        "badge": "Şaperonlar",
        "badgeColor": "blue",
        "coreContent": {
            "text": (
                "Moleküler şaperonlar proteinlerin doğru üç boyutlu konformasyonlarına katlanmasını sağlar ve kümelenmelerini önler.\n\n"
                "Yaşlanan hücrelerde şaperonları kodlayan **Isı Şok Faktörü-1 (HSF-1)** aktivitesi belirgin biçimde zayıflar.\n\n"
                "Hsp70 ve Hsp90 gibi koruyucu şaperon düzeyleri düşer.\n\n"
                "> Termal veya oksidatif stres altında yaşlı hücre hasarlı proteinlerini tekrar katlayamaz; yanlış katlanan moleküller çökelir."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Stres anında şaperon proteinlerinin sentezini başlatan anahtar transkripsiyon faktörü HSF-1 faktörüdür.",
                "HSF-1",
                "Heat shock factor-1 kısaltması"
            ),
            make_before_after(
                "Genç Hücre Şaperon Yanıtı ile Yaşlı Hücre Şaperon Yanıtı",
                "Genç Hücre Şaperon Yanıtı",
                "Stres anında Hsp70 hızla 20 kat artar; hatalı proteinleri yakalayıp düzeltir veya proteazoma sunar.",
                "Yaşlı Hücre Şaperon Yanıtı",
                "HSF-1 yanıt vermez; şaperon havuzu yetersiz kalır, yanlış katlanmış proteinler oligomerik agregatlara dönüşür."
            )
        ]
    })

    # Slide 73
    slides.append({
        "id": "k1-08-s73",
        "title": "26S Proteazom Sisteminin Yaşla Tıkanması",
        "subtitle": "Ubiquitinlenmiş proteinlerin yıkılamaması ve proteazom kilitlenmesi",
        "badge": "Proteazom Yıkımı",
        "badgeColor": "red",
        "coreContent": {
            "text": (
                "26S proteazom, ubiquitinle etiketlenmiş kısa ömürlü ve hatalı proteinleri ATP harcayarak aminoasitlere parçalar.\n\n"
                "Yaşlanma sürecinde iki majör sorun ortaya çıkar:\n"
                "1. Proteazomun 20S katalitik çekirdeğindeki tripsin ve kimotripsin benzeri enzim aktiviteleri azalır.\n"
                "2. Oksidatif stresle karbonillenmiş ve çapraz bağlanmış proteinler proteazom kanalına girer ancak parçalanamaz; ==proteazom namlusunu tıkayarak kilitler==."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Çapraz bağlanmış okside protein agregatları 26S proteazom kanalını fiziksel olarak tıkayarak proteazom felcine yol açar.",
                "proteazom felcine",
                "Ubiquitin-proteazom sisteminin çalışamaz hale gelmesi"
            ),
            make_active_recall(
                "Proteazomun yaşla tıkanması hücre içindeki diğer normal proteinleri nasıl etkiler?",
                "Hücre döngüsü inhibitörleri, transkripsiyon faktörleri ve kısa ömürlü regülatör proteinler parçalanamaz; hücre içi protein dengesi tamamen kaosa sürüklenir."
            )
        ]
    })

    # Slide 74
    slides.append({
        "id": "k1-08-s74",
        "title": "Yaşlanan Hücrede Otofaji ve Lizozom Kapasitesinin Çöküşü",
        "subtitle": "Makrootofaji, şaperon aracılı otofaji (CMA) ve lipofuksin yükü",
        "badge": "Otofaji",
        "badgeColor": "amber",
        "coreContent": {
            "text": (
                "Proteazomun sığdıramayacağı büyük protein agregatlarını ve organelleri temizleyen ana sistem **otofajidir**.\n\n"
                "Yaşlanma ile otofaji genlerinin (**ATG genleri**) ekspresyonu düşer.\n\n"
                "Ayrıca Şaperon Aracılı Otofaji (CMA) reseptörü olan **LAMP-2A** zarlardan silinir.\n\n"
                "> Lizozomlar sindirilemeyen lipofuksin atıklarıyla tıka basa dolar; hücre 'çöpünü boşaltamayan' bir eve dönüşür."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Şaperon aracılı otofajide (CMA) proteinlerin lizozoma girmesini sağlayan membran reseptörü LAMP-2A reseptörüdür.",
                "LAMP-2A",
                "Lizozomal membran glikoproteini 2A"
            ),
            make_causal_chain(
                "Otofaji Yetersizliğinden Agregat Toksisitesine",
                [
                    "1. ATG Baskılanması: Yaşlanma ile otofaji genlerinin transkripsiyonu azalır.",
                    "2. Lizozom Yükü: Biriken lipofuksin asit hidrolazların serbestliğini kısıtlar.",
                    "3. Agregat Birikimi: Çözünmeyen protein kümeleri sitoplazmada devasa yığınlar yapar.",
                    "4. ER Stresi: Genişleyen agregatlar hücresel organel trafiğini felç eder.",
                    "5. Nörodejenerasyon: Nöronlar sinaptik iletiyi kaybedip apoptoza gider."
                ]
            )
        ]
    })

    # Slide 75
    slides.append({
        "id": "k1-08-s75",
        "title": "Nörodejeneratif Hastalıklarda Protein Agregasyonu",
        "subtitle": "Bölünmeyen nöronların protein birikimlerine aşırı duyarlılığı",
        "badge": "Nöropatoloji",
        "badgeColor": "purple",
        "coreContent": {
            "text": (
                "Nöronlar post-mitotik hücrelerdir; yani bölünerek sitoplazmalarındaki atıkları iki yavru hücreye paylaştırıp seyreltemezler.\n\n"
                "Bu nedenle yaşlanmayla ortaya çıkan proteostazis yetersizliğinden **en ağır etkilenen doku merkezi sinir sistemidir**.\n\n"
                "Her nörodejeneratif hastalıkta kendine özgü bir mutant veya yanlış katlanmış protein agregatı başroldedir:\n\n"
                "- Alzheimer: Beta-amiloid ve Tau\n"
                "- Parkinson: Alfa-sinüklein\n"
                "- Huntington: Huntingtin (poliglutamin)\n"
                "- ALS: TDP-43 ve SOD1"
            )
        },
        "interactiveElements": [
            make_table(
                ["Nörodejeneratif Hastalık", "Biriken Temel Protein", "Histopatolojik Lezyon"],
                [
                    [("Alzheimer Hastalığı", False, ""), ("Beta-amiloid ve Hiperfosforile Tau", False, ""), ("Senil plaklar ve Nörofibriler yumaklar", True, "Serebral kortekste biriken mikroskobik odaklar")],
                    [("Parkinson Hastalığı", False, ""), ("Alfa-sinüklein", False, ""), ("Lewy cisimcikleri", True, "Substansiya nigrada eozinofilik inklüzyonlar")],
                    [("Huntington Hastalığı", False, ""), ("Huntingtin (CAG tekrarı)", False, ""), ("Nükleer inklüzyonlar", True, "Kaudat nükleus nöronlarında kümelenmeler")],
                    [("Amyotrofik Lateral Skleroz", False, ""), ("TDP-43 ve SOD1", False, ""), ("Ön boynuz motor nöron inklüzyonları", True, "Spinal kord harabiyeti yaratan birikim")]
                ]
            ),
            make_cloze(
                "Nöronların yaşa bağlı protein agregatlarına en duyarlı hücre olmasının nedeni post-mitotik olmaları ve bölünememeleridir.",
                "post-mitotik",
                "Hücre döngüsünden kalıcı olarak çıkmış bölünmeyen hücre terimi"
            )
        ]
    })

    # Slide 76
    slides.append({
        "id": "k1-08-s76",
        "title": "Alzheimer Hastalığı: Plaklar ve Yumaklar",
        "subtitle": "Ekstrasellüler amiloid-beta ile intrasellüler hiperfosforile tau ikilisi",
        "badge": "Alzheimer Patolojisi",
        "badgeColor": "red",
        "coreContent": {
            "text": (
                "Alzheimer hastalığı ileri yaş demansının en yaygın nedenidir ve iki majör protein agregatıyla karakterizedir:\n\n"
                "1. **Senil (Amiloid) Plaklar:** Amiloid öncül proteinin (APP) beta ve gama sekretazlarca hatalı kesilmesiyle oluşan ==ekstrasellüler A-beta42 fibrilleridir==.\n"
                "2. **Nörofibriler Yumaklar (NFT):** Mikrotübül stabilizatörü olan tau proteininin aşırı fosforillenerek nöron sitoplazmasında biriktiği ==intrasellüler agregatlardır==.\n\n"
                "> Sinaps kaybı ve serebral korteks atrofisi derin hafıza kaybına yol açar."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Alzheimer hastalığında nöron sitoplazmasında biriken intrasellüler lezyon nörofibriler yumaklar olarak adlandırılır.",
                "nörofibriler yumaklar",
                "Hiperfosforile tau proteinlerinin oluşturduğu alev şekilli yumaklar"
            ),
            make_before_after(
                "Alzheimer'da Ekstrasellüler Plak ile İntrasellüler Yumak",
                "Senil Amiloid Plak (Ekstrasellüler)",
                "Nöropilde nöronlar arasında biriken, Kongo kırmızısı ile elma yeşili çift kırıcı A-beta amiloid çekirdeği.",
                "Nörofibriler Yumak (İntrasellüler)",
                "Nöron perikaryonunda mikrotübül transportunu felç eden çift sarmallı tau filaman yumağı."
            )
        ]
    })

    # Slide 77
    slides.append({
        "id": "k1-08-s77",
        "title": "Parkinson Hastalığı: Lewy Cisimcikleri ve Alfa-Sinüklein",
        "subtitle": "Substansiya nigra dopaminerjik nöron kaybı ve eozinofilik sitoplazmik inklüzyonlar",
        "badge": "Hareket Bozukluğu",
        "badgeColor": "rose",
        "coreContent": {
            "text": (
                "Parkinson hastalığında orta beyindeki **substansiya nigra pars kompaktanın** dopaminerjik nöronları seçici olarak ölür.\n\n"
                "Sağ kalan nöronların sitoplazmasında yuvarlak, eozinofilik, etrafı açık haleli inklüzyonlar saptanır (**Lewy cisimcikleri**).\n\n"
                "Lewy cisimciğinin ana omurgasını presinaptik bir protein olan ==alfa-sinüklein== agregatları ve ubiquitin oluşturur.\n\n"
                "> Dopamin eksikliği istirahat tremoru, rijidite, bradikinezi ve postüral instabiliteye neden olur."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Parkinson hastalığında dopaminerjik nöronlarda Lewy cisimciklerini oluşturan temel protein alfa-sinüklein proteinidir.",
                "alfa-sinüklein",
                "SNCA geni tarafından kodlanan presinaptik patolojik protein"
            ),
            make_micro_quiz(
                "Yetmiş yaşında istirahat tremoru, maske yüz ve bradikinezi ile başvuran hastanın substansiya nigra nöronlarında eozinofilik konsantrik Lewy cisimcikleri saptanıyor. Bu cisimciklerde biriken ana protein hangisidir?",
                {
                    "A": "Alfa-sinüklein",
                    "B": "Trigliserid",
                    "C": "Melanin",
                    "D": "Kalsiyum fosfat",
                    "E": "Glikojen"
                },
                "A",
                {
                    "A": "Doğru cevap A'dır: Lewy cisimciğinin ana yapı taşı alfa-sinüklein protein agregatıdır.",
                    "B": "Steatoz lipididir.",
                    "C": "Nöromelanin normalde bulunur ancak Lewy cisimciği proteindir.",
                    "D": "Kalsifikasyondur.",
                    "E": "Glikojenozdur."
                }
            )
        ]
    })

    # Slide 78
    slides.append({
        "id": "k1-08-s78",
        "title": "Huntington Hastalığı ve ALS: Proteotoksik İntihar",
        "subtitle": "CAG trinükleotid patlaması ve motor nöronlarda TDP-43 birikimi",
        "badge": "Nörogenetik",
        "badgeColor": "cyan",
        "coreContent": {
            "text": (
                "Proteostazis yetersizliğinin diğer iki ölümcül tablosu:\n\n"
                "- **Huntington Hastalığı:** HTT genindeki **CAG trinükleotid tekrar artışı** sonucu uzamış poliglutamin kuyruğuna sahip mutant huntingtin üretilir; striatumdaki (kaudat nükleus) nöron nükleuslarında toksik inklüzyonlar yapar.\n"
                "- **Amiyotrofik Lateral Skleroz (ALS):** Spinal kord ön boynuz motor nöronlarında nükleustan sitoplazmaya kaçıp kümelenen ==TDP-43== proteini ve SOD1 agregatları ilerleyici felç yapar."
            )
        },
        "interactiveElements": [
            make_cloze(
                "ALS olgularının büyük kısmında motor nöron sitoplazmasında biriken anahtar patolojik protein TDP-43 proteinidir.",
                "TDP-43",
                "TAR DNA-binding protein 43 kısaltması"
            ),
            make_active_recall(
                "Huntington hastalığında mutasyonun moleküler doğası nedir ve biriken proteinde hangi aminoasit zinciri uzamıştır?",
                "CAG trinükleotid tekrar artışı mutasyonudur; proteinde uzamış poliglutamin (polyQ) kuyruğu oluşur ve nükleer agregasyona yol açar."
            )
        ]
    })

    # Slide 79 (CHECKPOINT 8)
    slides.append({
        "id": "k1-08-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Proteostazis Çöküşü ve Nörodejenerasyon",
        "subtitle": "Bölüm 8 Şaperonlar, Proteazom Kilitlenmesi, Alzheimer ve Parkinson",
        "badge": "Checkpoint 8",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 8,
        "coreContent": {
            "text": (
                "Sekizinci kontrol noktasında proteostazis ve nörodejenerasyonu özetliyoruz:\n\n"
                "1. **Proteostazis Ağı:** Şaperon katlaması + Proteazom yıkımı + Otofaji temizliği.\n"
                "2. **Yaşla Çöküş:** Hsp70 azalır, okside proteinler 20S proteazom namlusunu tıkar, otofaji zayıflar.\n"
                "3. **Nöron Kırılganlığı:** Post-mitotik oldukları için biriken agregatları bölünmeyle seyreltemezler.\n"
                "4. **Alzheimer:** Ekstrasellüler A-beta plakları + İntrasellüler tau nörofibriler yumakları.\n"
                "5. **Parkinson:** Substansiya nigrada alfa-sinüklein içeren Lewy cisimcikleri."
            )
        },
        "interactiveElements": [
            make_micro_quiz(
                "Alzheimer hastalığında nöronların hücre iskeletini parçalayarak nörofibriler yumakları oluşturan mikrotübül ilişkili protein hangisidir?",
                {
                    "A": "Alfa-sinüklein",
                    "B": "Hiperfosforile Tau",
                    "C": "TDP-43",
                    "D": "Huntingtin",
                    "E": "PrP"
                },
                "B",
                {
                    "A": "Parkinson proteinidir.",
                    "B": "Doğru cevap B'dir: Alzheimer'da intrasellüler nörofibriler yumakları oluşturan molekül hiperfosforile tau proteinidir.",
                    "C": "ALS proteinidir.",
                    "D": "Huntington proteinidir.",
                    "E": "Prion proteinidir."
                }
            ),
            make_active_recall(
                "Alzheimer'daki beta-amiloid plakları ile Parkinson'daki Lewy cisimciklerinin hücresel yerleşim farkı nedir?",
                "Beta-amiloid plakları nöronlar arasında ekstrasellüler alanda yerleşirken; Lewy cisimcikleri dopaminerjik nöron sitoplazmasında intrasellüler yerleşir."
            )
        ]
    })

    # Slide 80
    slides.append({
        "id": "k1-08-s80",
        "title": "Proteostazisi Güçlendiren Tedavi Yaklaşımları",
        "subtitle": "Otofaji indükleyicileri, kimyasal şaperonlar ve proteazom aktivatörleri",
        "badge": "Tedavi Hedefleri",
        "badgeColor": "emerald",
        "coreContent": {
            "text": (
                "Proteostazis yetersizliğini tersine çevirmek nörodejeneratif hastalıkların tedavisinde ana hedeftir:\n\n"
                "1. **Otofajinin İndüklenmesi:** mTOR inhibitörleri (Rapamisin) veya AMPK aktivatörleri (Metformin) ile hücresel lizozomal temizliğin tetiklenmesi.\n"
                "2. **Kimyasal ve Farmakolojik Şaperonlar:** Hatalı katlanan proteinlerin agregasyonunu engelleyen küçük moleküller.\n"
                "3. **İmmünoterapi:** Beta-amiloid ve alfa-sinükleine karşı monoklonal antikorlar (Lecanemab, Donanemab) ile ekstrasellüler plakların makrofajlarca temizlenmesi."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Alzheimer hastalığında beyindeki beta-amiloid plaklarını temizlemek için geliştirilen monoklonal antikor tedavisi immünoterapi yaklaşımıdır.",
                "immünoterapi",
                "Hedefe yönelik monoklonal antikor stratejisi"
            ),
            make_branching_logic(
                "Erken evre Alzheimer tanısı alan ve beyin PET incelemesinde yoğun amiloid birikimi saptanan bir hastada güncel biyolojik tedavi yaklaşımı ne olmalıdır?",
                [
                    {"text": "Yüksek doz kalsiyum vererek plakların distrofik taşlaşmasını sağlamak", "isCorrect": False, "feedback": "Kalsiyum verilmesi nörotoksisiteyi ve hücre ölümünü artırır."},
                    {"text": "Hedefe yönelik anti-amiloid monoklonal antikor tedavileri (Lecanemab vb.) ile mikroglia aracılı plak temizliğini desteklemek", "isCorrect": True, "feedback": "Doğru modern tedavi! Anti-amiloid antikorlar ekstrasellüler plak yükünü azaltarak bilişsel gerilemeyi yavaşlatır."},
                    {"text": "Hemen tüm nöronal protein sentezini durduran toksinler vermek", "isCorrect": False, "feedback": "Fatal nörolojik hasar yapar."}
                ]
            )
        ]
    })

    return slides
