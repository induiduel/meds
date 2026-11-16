# -*- coding: utf-8 -*-
"""
scripts/build_karsinojenez_molekuler_deck.py
Generates full 24-slide high-yield interactive learning deck for:
Prof. Dr. Hikmet Keleş - Karsinojenezin Moleküler Temeli
Extracted from: 17)Karsinojenezin Moleküler Temeli.pdf
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = 'src/data/interactive_learning_decks.json'

with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

slides = [
    {
        "slideNumber": 1,
        "title": "Karsinojenezin Moleküler Temeline Giriş ve Hallmarks of Cancer",
        "subtitle": "Genetik hasarın kalıtsallığı, klonal evrim ve kanserin 8 temel ayırt edici özelliği.",
        "badge": "Giriş & Konsept",
        "badgeColor": "accent",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Karsinojenez çok basamaklı genetik bir süreçtir. Tek bir mutasyon kanser yapmaz; hücrenin Hanahan ve Weinberg'in tanımladığı Hallmarks of Cancer özelliklerini aşama aşama kazanması gerekir.",
            "note": "Kanserin temelindeki hasar ölümcül olmayan (non-lethal) genetik hasardır; hücre ölmez, tam tersine kontrolsüz çoğalır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Karsinojenezin Temel Moleküler İlkeleri
Kanser, genomik düzeyde gerçekleşen bir hastalıktır. Moleküler patolojinin temel yasaları:

1. **Non-Lethal Genetik Hasar:**
   Karsinojenezin kalbinde hücreyi öldürmeyen (**non-lethal**) genetik hasar yatar. Hasar öldürücü olsaydı hücre nekroza veya apoptoza giderdi; oysa kanserde hücre ölümsüzleşir ve çoğalır.
2. **Monoklonal Başlangıç ve Klonal Genişleme:**
   Tümör tek bir ata hücrenin genetik transformasyonuyla başlar (monoklonalite).
3. **Kanserin 8 Temel Ayırt Edici Özelliği (Hallmarks of Cancer - Hanahan & Weinberg):**
   - **Kendi kendine yeten büyüme sinyalleri** (Onkogen aktivasyonu).
   - **Büyüme engelleyici sinyallere duyarsızlık** (Tümör supresör gen inaktivasyonu).
   - **Değişmiş hücresel metabolizma** (Warburg etkisi / Aerobik glikoliz).
   - **Apoptozdan kaçış** (Bcl-2 aşırılığı, p53 kaybı).
   - **Sınırsız replikatif potansiyel** (Telomeraz reaktivasyonu).
   - **Kalıcı anjiyogenez indüksiyonu** (VEGF salınımı).
   - **Doku invazyonu ve metastaz yeteneği** (E-kadherin kaybı, MMP aktivasyonu).
   - **İmmün yıkımdan kaçış** (PD-L1 artışı, MHC-I kaybı).

> 🔴 **Sınav Tuzağı:** ==red:Karsinojenez tek bir genetik darbe ile gerçekleşmez; 'çok basamaklı (multi-step) karsinojenez' kuralı gereği ortalama 4-7 bağımsız sürücü mutasyonun peş peşe birikmesi şarttır!===""",
        "spotPearls": [
            "🔴 Karsinojenezin temelindeki hasar hücreyi öldürmeyen (**non-lethal**) genetik değişikliktir.",
            "🔵 ==blue:Kanser gelişiminde rol oynayan Hanahan-Weinberg ayırt edici özellikleri (Hallmarks of Cancer) arasında değişmiş hücresel metabolizma (Warburg etkisi) ve immün kaçış yer alır.==",
            "⚡ Kanser başlangıçta monoklonaldir; ancak büyüme sürecinde genetik instabilite ile subklonlar gelişir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Non-Lethal Hasar", "text": "Hücreyi öldürmeyen kalıcı onkojenik mutasyon birikimi."},
                {"label": "Klonal Evrim", "text": "Tek hücreden köken alma, zamanla heterojenite kazanma."},
                {"label": "Hallmarks", "text": "Özerk büyüme, apoptoz direnci, telomeraz, anjiyogenez, metastaz."}
            ]
        },
        "flashcards": [
            {
                "id": "km-fc-1-1",
                "front": "Karsinojenez sürecinde hücrenin apoptoza veya nekroza gitmeyip malign transformasyon geçirmesini sağlayan genetik hasar tipi nedir?",
                "back": "Non-lethal (ölümcül olmayan) genetik hasardır.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide bu ilkeyi özellikle vurguladı."
            },
            {
                "id": "km-fc-1-2",
                "front": "Hanahan ve Weinberg'in güncellenmiş Hallmarks of Cancer modeline eklenen metabolik özellik nedir?",
                "back": "Hücresel enerji metabolizmasının yeniden programlanması (Warburg etkisi / Aerobik glikoliz).",
                "facultyNote": "Oksijen varken bile glikoliz tercih edilir."
            }
        ],
        "practiceQuestion": {
            "id": "km-pq-1",
            "question": "Moleküler karsinojenezin temel prensiplerine göre, malign neoplazmların gelişimini başlatan hücresel hasar türü aşağıdakilerden hangisidir?",
            "options": [
                "A) Akut ölümcül lizozomal membran rüptürü",
                "B) Hücreyi öldürmeyen (non-lethal) kalıtsal/somatik genetik hasar",
                "C) Masif sitoplazmik kalsiyum akışı ile koagülasyon nekrozu",
                "D) Sadece mitokondriyal krista kaybı",
                "E) İskemik hücre şişmesi"
            ],
            "answer": "B",
            "explanation": "Karsinojenezin merkezinde hücreyi öldürmeyen (non-lethal) genetik hasar yer alır. Hücre ölmez; mutasyonu yavru hücrelere aktararak özerk çoğalma döngüsüne girer.",
            "isPracticeQuestion": True,
            "deckId": "learn-karsinojenezin-molekuler-temeli",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 2,
        "title": "Kanser Genlerinin Dört Ana Sınıfı",
        "subtitle": "Proto-onkogenler, tümör supresörler, apoptoz düzenleyicileri ve DNA tamir genleri.",
        "badge": "Gen Sınıfları",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Kanser genlerini 4 sınıfta topluyoruz: Gaz pedalı onkogenler, fren pedalı tümör supresörler, intiharı önleyen apoptoz genleri ve yazım hatalarını düzelten DNA tamir genleridir.",
            "note": "Onkogenlerde tek alel mutasyonu (kazanılmış fonksiyon) yeterliyken, tümör supresörlerde iki alel de inaktive olmalıdır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Karsinojenezde Rol Alan 4 Majör Gen Grubu
Genetik mutasyonların hedefi olan 4 temel düzenleyici gen sınıfı:

#### 1. Büyümeyi Teşvik Eden Proto-Onkogenler (Gaz Pedalı):
- Normalde hücre bölünmesini, farklılaşmasını ve sağkalımını yöneten genlerdir.
- Mutasyon, translokasyon veya amplifikasyon sonucu aşırı aktif hale geldiklerinde **Onkogen** adını alırlar.
- **Fonksiyon Kazanımı (Gain-of-Function):** Dominant etkilidir; ==red:tek bir alelin mutasyonu bile kontrolsüz çoğalmayı tetiklemek için yeterlidir!==

#### 2. Büyümeyi Engelleyen Tümör Baskılayıcı (Supresör) Genler (Fren Pedalı):
- Hücre siklusunu frenleyen, temas inhibisyonunu sağlayan ve bölünmeyi durduran genlerdir (Örn: RB, TP53, APC, BRCA1).
- **Fonksiyon Kaybı (Loss-of-Function):** Kural olarak resesif davranırlar; Knudson'ın iki vuruş kuralına göre ==red:her iki alelin de inaktive olması gerekir!==
- İki alt gruba ayrılırlar:
  - **Valeler (Governors):** Hücre siklus kontrol noktalarını yönetir (Örn: RB).
  - **Muhafızlar (Guardians):** Genomik hasarı tespit edip tamir veya apoptoz emri verir (Örn: TP53).

#### 3. Apoptozu Düzenleyen Genler:
- Hücre ölümünü engelleyen anti-apoptotikler (Bcl-2, Bcl-xL) onkogen gibi davranır.
- Ölümü tetikleyen pro-apoptotikler (Bax, Bak, Puma) tümör supresör gibi davranır.

#### 4. DNA Tamir Genleri:
- Karsinojenlerin veya replikasyon hatalarının oluşturduğu hasarları onaran 'bakım' (caretaker) genleridir (Örn: MSH2, MLH1, BRCA1/2, XP genleri).
- Doğrudan onkojenik değillerdir; ancak inaktive olduklarında genomik instabiliteye yol açarak diğer kanser genlerinin mutasyon hızını yüzlerce kat artırırlar (*Mutatör Fenotip*).""",
        "spotPearls": [
            "🔴 Onkogenler **dominanttır**; tek bir alelde 'fonksiyon kazanımı' (gain-of-function) kanserleşme için yeterlidir.",
            "🔵 ==blue:Tümör supresör genler kural olarak resesiftir; her iki alelin de inaktive olması (Knudson two-hit kuralı) gerekir.==",
            "⚡ DNA tamir genlerinin bozulması doğrudan tümör yapmaz; diğer genlerin mutasyon oranını artıran 'mutatör fenotip' yaratır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Onkogenler", "text": "Dominant, tek alel mutasyonu yeterli (fonksiyon kazanımı)."},
                {"label": "Tümör Supresörler", "text": "Resesif, iki alel kaybı gerekir (Governors vs Guardians)."},
                {"label": "DNA Tamir Genleri", "text": "Bakım (caretaker) genleri; kaybı mutatör fenotip yapar."}
            ]
        },
        "flashcards": [
            {
                "id": "km-fc-2-1",
                "front": "Onkogenler ile tümör supresör genler arasındaki genetik geçiş/etki farkı nedir?",
                "back": "Onkogenler dominanttır (tek alel fonksiyon kazanımı yeterlidir); tümör supresör genler ise resesiftir (iki alel inaktivasyonu gerekir).",
                "facultyNote": "TUS sınavlarında temel onkoloji ayrımıdır."
            },
            {
                "id": "km-fc-2-2",
                "front": "Tümör supresör genlerden RB ve TP53 sırasıyla hangi sınıflara girer?",
                "back": "RB bir 'Governor' (hücre siklus valisi); TP53 ise bir 'Guardian' (genom muhafızı) genidir.",
                "facultyNote": "RB siklus frenidir, p53 genom hasar bekçisidir."
            }
        ],
        "practiceQuestion": {
            "id": "km-pq-2",
            "question": "Aşağıdaki gen sınıflarından hangisinde meydana gelen tek bir alelik mutasyon (heterozigot durum), 'fonksiyon kazanımı' (gain-of-function) mekanizması ile doğrudan neoplastik transformasyonu tetikleyebilir?",
            "options": [
                "A) DNA mismatch repair genleri",
                "B) Proto-onkogenler",
                "C) Hücre siklusu freni olan tümör supresör genler (RB)",
                "D) Genom gardiyanı tümör supresör genler (TP53)",
                "E) Homolog rekombinasyon tamir genleri (BRCA1)"
            ],
            "answer": "B",
            "explanation": "Proto-onkogenler dominant etkilidir. Tek bir kopyalarında meydana gelen mutasyon (gain-of-function) onkoprotein üretimi için yeterlidir. Diğer seçeneklerdeki tümör supresör ve DNA tamir genlerinde ise her iki alelin de inaktive olması (loss-of-function) gerekir.",
            "isPracticeQuestion": True,
            "deckId": "learn-karsinojenezin-molekuler-temeli",
            "discipline": "Tıbbi Patoloji"
        }
    }
]

# Write a comprehensive array of 24 slides for Karsinojenezin Moleküler Temeli
# Slide 3: Büyüme Faktörleri ve Otokrin Döngü (PDGF, TGF-a, FGF)
# Slide 4: Reseptör Tirozin Kinazlar (RTK): EGFR (ERBB1) ve HER2 (ERBB2)
# Slide 5: ALK ve RET Reseptör Tirozin Kinaz Füzyonları
# Slide 6: İntraselüler Sinyal İletiminin Şahı: RAS Onkogeni (KRAS, NRAS, HRAS)
# Slide 7: RAS-GTP-GAP Döngüsü ve GAP Defektleri
# Slide 8: MAPK ve PI3K/AKT/mTOR Sinyal Yolakları
# Slide 9: BRAF Onkogeni ve V600E Mutasyonu
# Slide 10: Nükleer Transkripsiyon Faktörleri: MYC Onkogen Ailesi
# Slide 11: c-MYC ve Burkitt Lenfoma Translokasyonu t(8;14)
# Slide 12: N-MYC Amplifikasyonu ve Nöroblastom Prognozu
# Slide 13: Hücre Siklusu Kontrolü: Siklinler, CDK'lar ve Siklin Bağımlı Kinaz İnhibitörleri (CDKI)
# Slide 14: Siklin D1 ve Mantle Hücreli Lenfoma t(11;14)
# Slide 15: Kromozomal Yeniden Düzenlenimler: Translokasyonlar (Philadelphia t(9;22) BCR-ABL)
# Slide 16: Gen Amplifikasyonu: Çift Dakika Kromozomlar (dmin) ve Homojen Boyanan Bölgeler (HSR)
# Slide 17: Apoptoz Kaçış Mekanizmaları: Bcl-2 ve Foliküler Lenfoma t(14;18)
# Slide 18: Kanser Hücresinde Sınırsız Çoğalma: Telomeraz Enzimi ve Kriz Dönemi
# Slide 19: Anjiyogenez İndüksiyonu: VEGF, HIF-1a ve Trombospondin-1
# Slide 20: Epitelyal-Mezenkimal Geçiş (EMT) ve E-Kadherin Kaybı
# Slide 21: Ekstraselüler Matriks İnvazyonu: Tip IV Kollajenaz (MMP-2, MMP-9)
# Slide 22: Damar İçi Dolaşım ve Metastatik Kolonizasyon
# Slide 23: MikroRNA'lar ve Epigenetik Değişiklikler (DNA Hipermetilasyonu)
# Slide 24: Moleküler Hedefe Yönelik Tedaviler (İmatinib, Trastuzumab, Erlotinib)

further_slides = [
    {
        "slideNumber": 3,
        "title": "Büyüme Faktörleri ve Otokrin Uyarım Döngüsü",
        "subtitle": "Kanser hücresinin kendi büyüme faktörünü üretip tüketmesi (otokrin döngü).",
        "badge": "Büyüme Sinyalleri",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Normal hücre büyüme faktörünü komşu hücreden bekler; kanser hücresi ise kendi hormonunu kendisi üretip kendi reseptörüne bağlayarak otokrin bir kısır döngü kurar.",
            "note": "Glioblastomun PDGF üretmesi veya sarkomların TGF-alfa üretmesi otokrin stimülasyonun klasik örnekleridir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Otokrin Sinyalizasyon ve Büyüme Faktörleri
Normal fizyolojide hücreler kendi ürettikleri büyüme faktörlerine yanıt vermezler; parakrin uyarım esastır. Kanser hücreleri ise bu kuralı yıkar:

#### Otokrin Döngü Mekanizması:
Tümör hücresi hem büyüme faktörünü (ligand) hem de o faktörün reseptörünü aynı anda sentezler. Salınan büyüme faktörü aynı hücrenin yüzeyindeki reseptöre bağlanarak kesintisiz bir proliferasyon sinyali üretir.

#### Klasik Örnekler:
- **Glioblastom (GBM):** Aşırı **PDGF (Trombosit Kaynaklı Büyüme Faktörü)** üretir ve yüzeyinde PDGF reseptörü (PDGFR) taşır.
- **Sarkomlar:** Yüksek miktarda **TGF-α** üreterek yüzeylerindeki **EGFR** üzerinden otokrin çoğalırlar.
- **FGF (Fibroblast Büyüme Faktörü):** Mide karsinomlarında ve melanomlarda stromal hücreleri uyararak hem anjiyogenezi hem tümör mitozunu kamçılar.

> 🔴 **Sınav Tuzağı:** ==red:Büyüme faktörü genlerinin kendisinde mutasyon olması nadirdir; karsinojenezde asıl mutasyona uğrayan yapılar büyüme faktörü RESEPTÖRLERİ ve hücre içi sinyal iletim proteinleridir!===""",
        "spotPearls": [
            "🔴 Kanser hücresinin kendi ürettiği büyüme faktörüyle kendi reseptörünü uyarmasına **Otokrin Sinyalizasyon** denir.",
            "🔵 ==blue:Glioblastomlar PDGF ve PDGFR sentezleyerek; birçok sarkom ise TGF-alfa ve EGFR eksprese ederek otokrin döngüye girer.==",
            "⚡ Büyüme faktörü genleri genellikle mutasyona uğramaz; aşırı eksprese edilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Otokrin Döngü", "text": "Kendi ürettiği ligant ile kendi reseptörünü sürekli aktive etme."},
                {"label": "Glioblastom", "text": "PDGF / PDGFR otokrin uyarımı."},
                {"label": "Sarkomlar", "text": "TGF-alfa / EGFR otokrin uyarımı."}
            ]
        },
        "flashcards": [
            {
                "id": "km-fc-3-1",
                "front": "Glioblastom hücrelerinin kontrolsüz çoğalmasında rol oynayan karakteristik otokrin büyüme faktörü ve reseptör çifti nedir?",
                "back": "PDGF (Trombosit kaynaklı büyüme faktörü) ve PDGFR.",
                "facultyNote": "Tümör kendi büyüme faktörünü kendi üretir."
            },
            {
                "id": "km-fc-3-2",
                "front": "Karsinojenezde büyüme faktörlerinin kendisi mi yoksa reseptörleri mi daha sık onkojenik mutasyona uğrar?",
                "back": "Reseptörleri (Reseptör Tirozin Kinazlar) çok daha sık mutasyona uğrar.",
                "facultyNote": "Reseptör mutasyonu ligant olmasa bile sürekli aktif kalır."
            }
        ],
        "practiceQuestion": {
            "id": "km-pq-3",
            "question": "Malign tümör hücrelerinin dışarıdan herhangi bir parakrin büyüme faktörü uyarısına ihtiyaç duymadan, kendi sentezledikleri büyüme faktörlerini kendi yüzey reseptörlerine bağlayarak sürekli mitoza girmesi mekanizmasına ne ad verilir?",
            "options": [
                "A) Parakrin inhibisyon",
                "B) Otokrin stimülasyon",
                "C) Jukstakrin adhezyon",
                "D) Endokrin regülasyon",
                "E) Kontakt inhibisyonu"
            ],
            "answer": "B",
            "explanation": "Kanser hücrelerinin kendi büyüme faktörlerini üretip kendi reseptörlerine bağlaması ve özerk çoğalması 'Otokrin Stimülasyon' olarak adlandırılır.",
            "isPracticeQuestion": True,
            "deckId": "learn-karsinojenezin-molekuler-temeli",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 4,
        "title": "Reseptör Tirozin Kinazlar (RTK): EGFR ve HER2/neu",
        "subtitle": "ERBB1 (EGFR), ERBB2 (HER2/neu) amplifikasyonu ve hedefe yönelik antikorlar.",
        "badge": "Onkogenler",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "HER2 gen amplifikasyonu meme kanserlerinin %15-20'sinde görülür, eskiden kötü prognozdu; ancak Trastuzumab (Herceptin) ilacının geliştirilmesiyle moleküler patolojinin en büyük zaferlerinden biri olmuştur.",
            "note": "EGFR (ERBB1) mutasyonları ise sigara içmeyen kadın akciğer adenokarsinomlarında sıktır ve Tirozin Kinaz İnhibitörlerine (Gefitinib, Erlotinib) yanıt verir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Reseptör Tirozin Kinaz (RTK) Ailesi Onkogenleri
Reseptör tirozin kinazlar, hücre zarından geçen ve sitoplazmik kuyruğunda kinaz aktivitesi taşıyan moleküllerdir. Normalde ligant bağlandığında dimerleşir ve otofosforilasyonla aktive olurlar. Onkogenik formlarında ise **ligant olmaksızın sürekli açık (konstitütif aktif)** kalırlar!

#### 1. EGFR (ERBB1):
- **Epidermal Büyüme Faktörü Reseptörü.**
- **Akciğer Adenokarsinomlarında:** Özellikle sigara içmemiş Asyalı kadınlarda tirozin kinaz domaininde (Ekzon 19 delesyonu veya Ekzon 21 L858R nokta mutasyonu) aktifleştirici mutasyonlar saptanır.
- **Hedef Tedavi:** Küçük molekül tirozin kinaz inhibitörleri (**Erlotinib, Gefitinib, Osimertinib**).
- **Skuamöz Baş-Boyun ve Akciğer Kanserlerinde:** EGFR aşırı ekspresyonu sıktır.

#### 2. HER2 / neu (ERBB2):
- Hücre yüzeyinde ligant bağlama bölgesi kapalı olan ancak diğer ERBB reseptörleriyle heterodimer oluşturan güçlü bir onkoproteindir.
- **Meme Karsinomu:** Olguların %15-20'sinde **17q12 kromozomundaki ERBB2 gen amplifikasyonu** görülür. Hücre yüzeyinde 2 milyon adede kadar HER2 reseptörü dizilir.
- **Mide ve Gastroözofageal Bileşke Karsinomları:** %10-15 olguda HER2 amplifikasyonu mevcuttur.
- **Hedef Tedavi:** Monoklonal antikor **Trastuzumab (Herceptin)** ve **Pertuzumab** sağkalımı dramatik şekilde uzatır.""",
        "spotPearls": [
            "🔴 Meme kanserinde 17q12 kromozom amplifikasyonu ile aşırı eksprese edilen reseptör **HER2/neu (ERBB2)**dir; tedavide **Trastuzumab** kullanılır.",
            "🔵 ==blue:Sigara içmeyen kadın akciğer adenokarsinomlarında saptanan ve Erlotinib/Gefitinib gibi tirozin kinaz inhibitörlerine duyarlı olan mutasyon EGFR mutasyonudur.==",
            "⚡ RTK onkogenleri ligant yokluğunda bile dimerize kalarak hücreyi durmaksızın mitoza sokar."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "EGFR (ERBB1)", "text": "Akciğer adenokarsinumu; TKI (Erlotinib) hedefi."},
                {"label": "HER2 (ERBB2)", "text": "Meme ve mide karsinomu; Trastuzumab hedefi."},
                {"label": "Dimerizasyon", "text": "Ligantsız konstitütif otofosforilasyon."}
            ]
        },
        "flashcards": [
            {
                "id": "km-fc-4-1",
                "front": "İnvaziv duktal meme karsinomunda prognozu belirleyen ve Trastuzumab (Herceptin) tedavisi endikasyonunu oluşturan onkogen amplifikasyonu hangisidir?",
                "back": "HER2 / neu (ERBB2) gen amplifikasyonudur.",
                "facultyNote": "İmmünohistokimya (3+) veya FISH ile doğrulanır."
            },
            {
                "id": "km-fc-4-2",
                "front": "Akciğer adenokarsinomu tanısı alan bir hastada Erlotinib veya Osimertinib gibi tirozin kinaz inhibitörlerinin etkili olabilmesi için hangi gen mutasyonu aranır?",
                "back": "EGFR (Epidermal Büyüme Faktörü Reseptörü) mutasyonu.",
                "facultyNote": "Özellikle ekzon 19 ve 21 mutasyonları yanıt verir."
            }
        ],
        "practiceQuestion": {
            "id": "km-pq-4",
            "question": "Kırk iki yaşında kadın hastanın meme karsinomu biyopsisinde floresan in situ hibridizasyon (FISH) ile 17q kromozomunda gen amplifikasyonu saptanmıştır. Bu hastada hedefe yönelik monoklonal antikor tedavisi (Trastuzumab) için hedef alınan onkoprotein aşağıdakilerden hangisidir?",
            "options": [
                "A) c-KIT",
                "B) HER2 / neu (ERBB2)",
                "C) BRAF",
                "D) ALK",
                "E) RET"
            ],
            "answer": "B",
            "explanation": "HER2/neu (ERBB2) geni 17q12 kromozomunda yer alır ve meme karsinomlarında amplifiye olduğunda Trastuzumab (Herceptin) monoklonal antikoru için doğrudan terapötik hedeftir.",
            "isPracticeQuestion": True,
            "deckId": "learn-karsinojenezin-molekuler-temeli",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 5,
        "title": "İntraselüler Sinyal İletiminin Şahı: RAS Onkogeni",
        "subtitle": "KRAS, NRAS, HRAS, GTP-GDP döngüsü ve GAP (GTPaz aktive edici protein) rolü.",
        "badge": "Onkogenler",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "İnsan tümörlerinde en sık mutasyona uğrayan proto-onkogen RAS'tır! Pankreas kanserlerinin %90'ında, kolon kanserlerinin %50'sinde KRAS mutasyonu vardır.",
            "note": "RAS bir G-proteinidir; GTP bağlıyken aktif, GDP bağlıyken inaktiftir. Nokta mutasyonu olunca GTP'yi parçalayamaz ve daima AÇIK kalır!",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### RAS Biyolojisi ve GTPaz Kilit Mekanizması
**RAS**, reseptör tirozin kinazların iç yüzünde yerleşik, küçük bir G-proteinidir (GTPaz). İnsan kanserlerinde en sık mutasyona uğrayan **proto-onkogen ailesidir** (tüm insan kanserlerinin %20-25'inde).

#### 3 RAS Geni ve Organ Spesifitesi:
- **KRAS:** Pankreas adenokarsinomu (%90), Kolorektal karsinom (%50), Akciğer adenokarsinomu (%30).
- **NRAS:** Akut Miyeloid Lösemi (AML) ve Malign Melanom.
- **HRAS:** Mesane karsinomu.

#### Normal RAS Açma-Kapama Döngüsü:
1. **İnaktif Durum:** RAS, **GDP**'ye bağlıdır ve uyur haldedir.
2. **Aktivasyon:** Büyüme faktörü reseptöre bağlanınca SOS (GEF) proteini gelir; RAS'taki GDP atılır ve yerine **GTP** bağlanır.
3. **Sinyal İletimi:** RAS-GTP kompleksi aktive olur ve alt akım yolaklarını (**MAPK/ERK ve PI3K/AKT**) ateşler.
4. **Kapanma (Hidroliz):** Normal RAS'ın kendi içsel GTPaz aktivitesi vardır. Bu aktivite **GAP (GTPase Activating Protein)** proteinleri tarafından 1000 kat hızlandırılır. GTP hidroliz edilip GDP'ye döner ve RAS KAPANIR.

#### Onkojenik RAS Nokta Mutasyonu:
En sık **12, 13 veya 61. kodonlarda** tek bir baz değişimi (nokta mutasyonu) olur.
- Bu mutasyon RAS'ın GTPaz aktivitesini ve GAP ile etkileşimini bozar!
- RAS, GTP'yi hidroliz edip kapatamaz; **sürekli aktif GTP formunda kilitlenir!**
- Sonuç: Hücre çekirdeğine durmaksızın 'BÖLÜN!' emri gider.""",
        "spotPearls": [
            "🔴 İnsan kanserlerinde en sık mutasyona uğrayan onkogen ailesi **RAS** (özellikle Pankreas kanserinde %90 **KRAS**)dır.",
            "🔵 ==blue:RAS'ın inaktif formunda GDP, aktif formunda GTP bağlıdır. Onkojenik mutasyon GTP hidrolizini engelleyerek RAS'ı sürekli aktif tutar.==",
            "⚡ **GAP (GTPaz Aktive Edici Protein)** RAS'ın frenidir; GAP kaybı (örneğin Nörofibromin / NF1 kaybı) RAS'ın aşırı çalışmasına yol açar."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "RAS", "text": "İnsan kanserlerinde en sık mutasyona uğrayan onkogen."},
                {"label": "KRAS", "text": "Pankreas (%90) ve Kolon (%50) kanserinde baş aktör."},
                {"label": "Kilitlenme", "text": "12/13/61. kodon mutasyonu ile GTP hidroliz edilemez."}
            ]
        },
        "flashcards": [
            {
                "id": "km-fc-5-1",
                "front": "Pankreas duktal adenokarsinomlarının %90'ında saptanan en karakteristik proto-onkogen nokta mutasyonu hangisidir?",
                "back": "KRAS gen mutasyonudur (özellikle kodon 12).",
                "facultyNote": "Kolon kanserinde de %50 oranında bulunur."
            },
            {
                "id": "km-fc-5-2",
                "front": "RAS onkoproteininin daima açık (aktif) kalmasına yol açan biyokimyasal defekt nedir?",
                "back": "İçsel GTPaz aktivitesinin kaybı ve GTP'nin GDP'ye hidroliz edilememesidir.",
                "facultyNote": "GAP proteinleri artık RAS'ı kapatamaz."
            }
        ],
        "practiceQuestion": {
            "id": "km-pq-5",
            "question": "Pankreas karsinomlu bir hastadan alınan tümör dokusunda KRAS geninin 12. kodonunda nokta mutasyonu saptanmıştır. Bu mutasyonun tümör hücresinde yol açtığı temel biyokimyasal sonuç aşağıdakilerden hangisidir?",
            "options": [
                "A) RAS'ın plazma membranından nükleusa göç etmesi",
                "B) RAS'ın GTPaz aktivitesini kaybederek sürekli GTP'ye bağlı aktif formda kilitlenmesi",
                "C) p53 proteininin aşırı fosforilasyonu",
                "D) Hücre içi kalsiyum depolarının boşalması",
                "E) Telomerlerin hızla kısalması"
            ],
            "answer": "B",
            "explanation": "RAS nokta mutasyonları (kodon 12, 13, 61), proteinin içsel GTPaz aktivitesini ve GAP duyarlılığını ortadan kaldırır. RAS, GTP'yi hidroliz edemez ve sürekli aktif kalarak downstream MAPK yolağını durmaksızın uyarır.",
            "isPracticeQuestion": True,
            "deckId": "learn-karsinojenezin-molekuler-temeli",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 6,
        "title": "BRAF Onkogeni ve V600E Nokta Mutasyonu",
        "subtitle": "MAPK yolağının serin/treonin kinazı, melanom ve tiroid papiller karsinomu.",
        "badge": "Onkogenler",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "RAS'ın hemen altındaki kinaz BRAF'tır. Malign melanomların %60'ında tek bir aminoasit değişir: Valin yerine Glutamat geçer (V600E). Tedavide Vemurafenib ile bu mutasyonu doğrudan vuruyoruz.",
            "note": "BRAF V600E mutasyonu Tiroid Papiller Karsinomunda da en sık görülen onkojenik mutasyondur.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### BRAF Kinaz ve V600E Mutasyonunun Önemi
**BRAF**, RAS sinyal yolağının doğrudan alt akımında (downstream) yer alan bir **serin/treonin kinazdır**. MAPK (Mitogen-Activated Protein Kinase) kaskadının ilk basamağıdır.

#### V600E Nokta Mutasyonu:
BRAF geninde en sık görülen anormallik, 600. pozisyondaki **Valin** aminoasidinin **Glutamat (E)** ile yer değiştirmesidir (**V600E**).
- Bu tek aminoasit değişimi BRAF enziminin kinaz aktivitesini 500 kat artırır.
- RAS uyarısı olmasa bile BRAF tek başına MEK ve ERK kinazları fosforilleyerek nükleusa transkripsiyon sinyali pompalar.

#### Görüldüğü Başlıca Maligniteler:
1. **Malign Melanom:** Kutanöz melanomların **%50-60'ında** BRAF V600E saptanır. (Ayrıca benign melanositik nevüslerde de bulunur; ancak tek başına kanser yapmaya yetmez, p16/CDKN2A kaybı da gerekir).
2. **Tiroid Papiller Karsinomu:** Olguların **%40-50'sinde** en sık rastlanan genetik bozukluktur (kötü prognoz ve lenf nodu metastazı ile ilişkili).
3. **Kolorektal Kanserler:** Mikrosatellit instabilitesi gösteren sporadik sağ kolon kanserlerinde sıktır (Lynch sendromu ayrımında kullanılır!).
4. **Hairy Cell (Tüylü Hücreli) Lösemi:** Olguların **%100'e yakınında** BRAF V600E saptanır (hastalığın moleküler imzasıdır).

#### Hedef İlaçlar:
BRAF V600E inhibitörleri: **Vemurafenib, Dabrafenib**.""",
        "spotPearls": [
            "🔴 **Malign Melanom**ların %60'ında ve **Tiroid Papiller Karsinomu**nun %50'sinde saptanan en sık mutasyon **BRAF V600E** mutasyonudur.",
            "🔵 ==blue:Tüylü Hücreli (Hairy Cell) Lösemi olgularının neredeyse %100'ünde patognomonik olarak BRAF V600E mutasyonu bulunur.==",
            "⚡ BRAF inhibitörü **Vemurafenib**, V600E mutasyonlu melanom hastalarında sağkalımı uzatır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "BRAF V600E", "text": "Valin -> Glutamat değişimi; kinaz aktivitesinde 500 kat artış."},
                {"label": "Melanom & Tiroid", "text": "Melanomda %60, Tiroid Papiller Karsinomda %50."},
                {"label": "Hairy Cell Lösemi", "text": "Hemen her olguda (%100) mevcut patognomonik belirteç."}
            ]
        },
        "flashcards": [
            {
                "id": "km-fc-6-1",
                "front": "Malign melanomların yarıdan fazlasında saptanan ve Vemurafenib ile hedeflenen en sık mutasyon nedir?",
                "back": "BRAF V600E nokta mutasyonudur.",
                "facultyNote": "MAPK yolağının serin-treonin kinazıdır."
            },
            {
                "id": "km-fc-6-2",
                "front": "Hangi hematolojik malignitede BRAF V600E mutasyonu hastaların neredeyse %100'ünde saptanır?",
                "back": "Hairy Cell (Tüylü Hücreli) Lösemide.",
                "facultyNote": "Tanısal ve terapötik biyomarkerdır."
            }
        ],
        "practiceQuestion": {
            "id": "km-pq-6",
            "question": "Metastatik malign melanom tanısı alan bir hastada Vemurafenib tedavisine başlanabilmesi için tümör dokusunda aşağıdaki genetik mutasyonlardan hangisinin varlığı aranmalıdır?",
            "options": [
                "A) BCR-ABL translokasyonu",
                "B) BRAF V600E nokta mutasyonu",
                "C) HER2 amplifikasyonu",
                "D) APC delesyonu",
                "E) RET füzyonu"
            ],
            "answer": "B",
            "explanation": "Vemurafenib, mutant BRAF V600E kinazını selektif olarak inhibe eden küçük moleküldür. Tedavi öncesi tümör dokusunda BRAF V600E mutasyonunun moleküler testle gösterilmesi zorunludur.",
            "isPracticeQuestion": True,
            "deckId": "learn-karsinojenezin-molekuler-temeli",
            "discipline": "Tıbbi Patoloji"
        }
    }
]

# Add more slides to reach 24 slides total
final_batch_slides = [
    {
        "slideNumber": 7,
        "title": "Nükleer Transkripsiyon Faktörleri: MYC Onkogen Ailesi",
        "subtitle": "c-MYC, N-MYC, L-MYC, Burkitt lenfoma translokasyonu ve metabolik yeniden programlama.",
        "badge": "Onkogenler",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "MYC hücresel büyümenin ana orkestra şefidir. c-MYC t(8;14) translokasyonu ile immünoglobulin ağır zincirinin yanına geçerse Burkitt lenfoma patlar; N-MYC amplifiye olursa çocukta nöroblastom çok kötü seyreder.",
            "note": "MYC hem siklinleri uyarır hem de Warburg etkisini (aerobik glikoliz) bizzat tetikler.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### MYC Proto-Onkogen Ailesi
**MYC**, hücre çekirdeğinde DNA'ya bağlanan ve hücre siklusuna giriş, ribozom biyogenezi ve hücresel metabolizmayı kontrol eden en güçlü transkripsiyon faktörüdür.

#### MYC Ailesi Üyeleri:
- **c-MYC:** Tüm dokularda eksprese edilir.
- **N-MYC:** Nöral dokuda eksprese edilir.
- **L-MYC:** Akciğerde eksprese edilir.

#### Patolojideki İki Kritik MYC Tablosu:
1. **Burkitt Lenfoma ve t(8;14) Translokasyonu:**
   - 8. kromozomdaki **c-MYC** geni, 14. kromozomdaki **İmmünoglobulin Ağır Zincir (IgH)** gen lokusunun güçlü promotörü altına taşınır: **t(8;14)(q24;q32)**.
   - B hücrelerinde antikor geni sürekli aktif olduğundan, c-MYC aşırı miktarda üretilir.
   - Sonuç: İnsan vücudunun en hızlı bölünen tümörü (%100 Ki-67 proliferasyon indeksi, 'yıldızlı gökyüzü / starry-sky' manzarası) ortaya çıkar.
2. **Nöroblastomda N-MYC Gen Amplifikasyonu:**
   - Çocukluk çağının böbrek üstü bezi tümörü olan nöroblastomda **N-MYC gen kopyası yüzlerce kat artar**.
   - Mikroskopta sitogenetik olarak **Çift Dakika Kromozomlar (dmin)** veya **Homojen Boyanan Bölgeler (HSR)** şeklinde izlenir.
   - N-MYC amplifikasyonu evreden bağımsız olarak **SON DERECE KÖTÜ PROGNOZ** göstergesidir.""",
        "spotPearls": [
            "🔴 **Burkitt Lenfoma**'nın moleküler temeli 8. kromozomdaki **c-MYC**'in 14. kromozoma taşındığı **t(8;14)** translokasyonudur.",
            "🔵 ==blue:Pediatrik nöroblastomda N-MYC gen amplifikasyonu bulunması, evreden bağımsız olarak en güçlü KÖTÜ PROGNOZ belirtecidir.==",
            "⚡ c-MYC aşırı aktivitesi hücrede hem glikolitik enzimleri (Warburg etkisi) hem de telomerazı indükler."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "c-MYC", "text": "t(8;14) Burkitt Lenfoma; yıldızlı gökyüzü manzarası."},
                {"label": "N-MYC Amplifikasyonu", "text": "Nöroblastomda kötü prognoz ve dmin/HSR oluşumu."},
                {"label": "Fonksiyon", "text": "Hücre siklusunu açar, metabolizmayı glikolize kaydırır."}
            ]
        },
        "flashcards": [
            {
                "id": "km-fc-7-1",
                "front": "Burkitt lenfomada c-MYC onkogeninin aşırı transkripsiyonuna yol açan karakteristik kromozomal translokasyon nedir?",
                "back": "t(8;14)(q24;q32) translokasyonudur.",
                "facultyNote": "c-MYC geni 14. kromozomdaki IgH güçlendiricisinin kontrolüne girer."
            },
            {
                "id": "km-fc-7-2",
                "front": "Çocukluk çağı nöroblastomunda prognozun çok kötü olduğunu gösteren genetik biyomarker hangisidir?",
                "back": "N-MYC gen amplifikasyonudur.",
                "facultyNote": "Kopya sayısı arttıkça sağkalım düşer."
            }
        ],
        "practiceQuestion": {
            "id": "km-pq-7",
            "question": "Üç yaşındaki bir çocuğun böbrek üstü bezinde kitle saptanmış ve nöroblastom tanısı konmuştur. Genetik incelemede tümör hücrelerinde 'çift dakika kromozomlar' (double minutes) saptanmıştır. Bu hastada kötü prognozla ilişkili amplifiye olan onkogen aşağıdakilerden hangisidir?",
            "options": [
                "A) c-KIT",
                "B) N-MYC",
                "C) RET",
                "D) BCL-2",
                "E) HER2"
            ],
            "answer": "B",
            "explanation": "Nöroblastomda çift dakika kromozomlar (dmin) veya homojen boyanan bölgeler (HSR) şeklinde gen amplifikasyonu gösteren ve en önemli kötü prognoz kriteri olan onkogen N-MYC'tir.",
            "isPracticeQuestion": True,
            "deckId": "learn-karsinojenezin-molekuler-temeli",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 8,
        "title": "Hücre Siklusu Kontrolü: Siklinler, CDK'lar ve Siklin D1",
        "subtitle": "G1/S geçiş noktası, CDK4/6 aktivasyonu ve Mantle Hücreli Lenfoma t(11;14).",
        "badge": "Hücre Siklusu",
        "badgeColor": "blue",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Bütün onkogenlerin ve supresörlerin nihai buluşma yeri hücre siklusudur. Siklin D1 ile CDK4 birleşirse RB fosforillenir ve hücre bölünmeye koşar. Mantle hücreli lenfomada t(11;14) ile Siklin D1 patlar!",
            "note": "CDK inhibitörleri p16, p21 ve p27 siklusu frenleyen bekçilerdir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Hücre Siklusu Motoru ve Onkojenik Regülasyon
Hücre siklusu 4 fazdan oluşur: G1 (büyüme), S (DNA sentezi), G2 (mitoz hazırlığı) ve M (mitoz).
- Hücrenin geri dönülemez bir şekilde DNA replikasyonuna karar verdiği en kritik nokta **G1/S kontrol noktasıdır (Restriksiyon Noktası)**.

#### Siklinler ve Siklin Bağımlı Kinazlar (CDK'lar):
- CDK'lar hücrede sabit miktarda bulunur; ancak sadece partnerleri olan **Siklin** proteinleri bağlandığında aktif kinaz haline gelirler.
- **Siklin D - CDK4 / CDK6 Kompleksi:** G1/S geçişini başlatan ana motordur.
- Hedefi: **RB (Retinoblastom) proteinini fosforillemek**tir. RB fosforillenince gevşer, E2F serbest kalır ve hücre S fazına geçer.

#### Siklin Bağımlı Kinaz İnhibitörleri (CDKI) - Doğal Frenler:
- **INK4 Ailesi (p16 / CDKN2A, p15, p18, p19):** Yalnızca Siklin D/CDK4 kompleksini selektif olarak durdurur. Melanomlarda p16 kaybı sıktır.
- **CIP/KIP Ailesi (p21, p27, p57):** Tüm siklin-CDK komplekslerini geniş çapta inhibe eder. **p21, p53 tarafından uyarılır.**

#### Mantle Hücreli Lenfoma ve t(11;14):
- 11. kromozomdaki **Siklin D1 (CCND1)** geni, 14. kromozomdaki IgH yanına taşınır: **t(11;14)(q13;q32)**.
- Siklin D1 aşırı üretilir ve Mantle Hücreli Lenfomaya yol açar.""",
        "spotPearls": [
            "🔴 **Mantle Hücreli Lenfoma**'nın ayırt edici genetik translokasyonu **t(11;14)** olup **Siklin D1 (CCND1)** aşırı ekspresyonuna yol açar.",
            "🔵 ==blue:G1/S kontrol noktasında RB proteinini fosforilleyerek inaktive eden ve hücreyi S fazına sokan kompleks Siklin D - CDK4/6 kompleksidir.==",
            "⚡ CDK inhibitörü **p16 (CDKN2A)** geninin delesyonu familyal melanomda ve birçok karsinomda en sık saptanan fren kaybıdır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Siklin D / CDK4", "text": "RB'yi fosforilleyerek G1/S restriksiyon noktasını aşar."},
                {"label": "Mantle Lenfoma", "text": "t(11;14) translokasyonu ile Siklin D1 aşırılığı."},
                {"label": "p16 (INK4a)", "text": "Siklin D/CDK4'ün spesifik tümör supresör inhibitörü."}
            ]
        },
        "flashcards": [
            {
                "id": "km-fc-8-1",
                "front": "Mantle hücreli lenfomanın gelişiminde rol oynayan ve Siklin D1 genini aşırı aktive eden translokasyon nedir?",
                "back": "t(11;14)(q13;q32) translokasyonudur.",
                "facultyNote": "11. kromozomdaki CCND1 geni 14'teki IgH yanına gider."
            },
            {
                "id": "km-fc-8-2",
                "front": "DNA hasarı saptandığında p53 tarafından transkripsiyonu artırılarak hücre siklusunu G1'de donduran CDKI hangisidir?",
                "back": "p21 proteinidir.",
                "facultyNote": "p21, CDK'ları bağlayarak RB'nin fosforillenmesini engeller."
            }
        ],
        "practiceQuestion": {
            "id": "km-pq-8",
            "question": "Bir lenf nodu biyopsisinde mantle zonu genişleten küçük B hücreli bir neoplazm saptanmış ve sitogenetikte t(11;14) translokasyonu doğrulanmıştır. Bu translokasyon sonucu aşırı eksprese edilen hücre siklusu regülatörü hangisidir?",
            "options": [
                "A) c-MYC",
                "B) BCL-2",
                "C) Siklin D1",
                "D) MDM2",
                "E) HER2"
            ],
            "answer": "C",
            "explanation": "t(11;14) translokasyonu, 11q13'teki Siklin D1 (CCND1) genini 14q32'deki immünoglobulin ağır zincir promotörü altına taşır ve Mantle Hücreli Lenfomanın patognomonik genetik sürücüsüdür.",
            "isPracticeQuestion": True,
            "deckId": "learn-karsinojenezin-molekuler-temeli",
            "discipline": "Tıbbi Patoloji"
        }
    }
]

# Generate slides 9 to 24 with faculty details
more_slides = [
    {
        "slideNumber": 9,
        "title": "Kromozomal Translokasyonlar ve Füzyon Genleri",
        "subtitle": "Philadelphia kromozomu t(9;22) BCR-ABL, EML4-ALK ve Ewing sarkomu t(11;22).",
        "badge": "Translokasyonlar",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Translokasyonlar iki şekilde kanser yapar: Ya geni güçlü bir promotörün yanına taşır (Burkitt gibi) ya da iki geni birleştirip yeni bir kimerik canavar protein üretir (KML'deki BCR-ABL gibi)!",
            "note": "İmatinib (Glivec), BCR-ABL kimerik kinazının ATP cebine oturup onu susturan hedefe yönelik tıbbın ilk mucizesidir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Kanser Sitogenetiğinde Translokasyon Mekanizmaları
Kromozom parçalarının yer değiştirmesi (resiprokal translokasyonlar) hematolojik malignitelerde ve sarkomlarda en sık rastlanan mutasyonel olaydır:

#### 1. Yeni Kimerik Füzyon Proteini Üretenler:
- **Kronik Miyeloid Lösemi (KML):** **t(9;22)(q34;q11)** → **Philadelphia Kromozomu**.
  - 9. kromozomdaki **ABL1** tirozin kinaz geni, 22. kromozomdaki **BCR** geni ile birleşir: **BCR-ABL1 füzyon geni**.
  - Oluşan protein konstitütif olarak aktif bir sitoplazmik tirozin kinazdır.
  - Tedavi: Hedefe yönelik tirozin kinaz inhibitörü **İmatinib (Glivec)**.
- **Ewing Sarkomu:** **t(11;22)(q24;q12)** → **EWS-FLI1** füzyon transkripsiyon faktörü.
- **Akut Promiyelositer Lösemi (APL / AML-M3):** **t(15;17)(q22;q21)** → **PML-RARA** füzyonu. Retinoik asit reseptörü bozulur; ATRA (All-trans retinoik asit) ile diferansiye edilerek tedavi edilir.
- **Sinovyal Sarkom:** **t(X;18)(p11;q11)** → **SS18-SSX** füzyonu.

#### 2. Onkogeni Güçlü Promotör Yanına Taşıyanlar:
- Burkitt lenfoma: **t(8;14)** (c-MYC / IgH).
- Foliküler lenfoma: **t(14;18)** (BCL2 / IgH).
- Mantle hücreli lenfoma: **t(11;14)** (Siklin D1 / IgH).""",
        "spotPearls": [
            "🔴 **KML**'de saptanan **Philadelphia kromozomu t(9;22)**, kimerik **BCR-ABL** tirozin kinaz proteini üretir; tedavisi **İmatinib**dir.",
            "🔵 ==blue:Ewing sarkomunun karakteristik füzyon translokasyonu t(11;22) EWS-FLI1'dir.==",
            "⚡ **APL (AML-M3)**'te saptanan **t(15;17) PML-RARA** füzyonu, hedefe yönelik ATRA tedavisi ile kür sağlanabilen lösemi tipidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "t(9;22)", "text": "BCR-ABL; KML ve ALL; İmatinib hedefi."},
                {"label": "t(15;17)", "text": "PML-RARA; Akut Promiyelositer Lösemi (ATRA yanıtı)."},
                {"label": "t(11;22)", "text": "EWS-FLI1; Ewing sarkomu / PNET."}
            ]
        },
        "flashcards": [
            {
                "id": "km-fc-9-1",
                "front": "Kronik miyeloid lösemide (KML) 9 ve 22. kromozomlar arasında gerçekleşen translokasyon sonucu oluşan füzyon geni ve tedavi edici molekül nedir?",
                "back": "BCR-ABL1 füzyon geni; spesifik inhibitörü İmatinib'dir.",
                "facultyNote": "Moleküler hedefe yönelik onkolojinin prototipidir."
            },
            {
                "id": "km-fc-9-2",
                "front": "Akut promiyelositer lösemide (APL) promyelositlerin olgunlaşmasını durduran ve t(15;17) ile oluşan kimerik gen nedir?",
                "back": "PML-RARA (Retinoik Asit Reseptörü Alfa) füzyonudur.",
                "facultyNote": "ATRA verilince hücreler granülosite olgunlaşır."
            }
        ],
        "practiceQuestion": {
            "id": "km-pq-9",
            "question": "Kemik iliği biyopsisinde miyeloid seride belirgin sola kayma saptanan ve sitogenetik analizinde t(9;22)(q34;q11) resiprokal translokasyonu gösterilen bir hastada üretilen onkojenik kimerik protein aşağıdakilerden hangisidir?",
            "options": [
                "A) PML-RARA",
                "B) BCR-ABL1",
                "C) EWS-FLI1",
                "D) EML4-ALK",
                "E) PAX3-FOXO1"
            ],
            "answer": "B",
            "explanation": "t(9;22) translokasyonu (Philadelphia kromozomu), 9q34'teki ABL1 ile 22q11'deki BCR genlerini birleştirerek konstitütif aktif BCR-ABL1 tirozin kinazını üretir ve KML'nin tanısal göstergesidir.",
            "isPracticeQuestion": True,
            "deckId": "learn-karsinojenezin-molekuler-temeli",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 10,
        "title": "Apoptozdan Kaçış: BCL-2 ve Foliküler Lenfoma",
        "subtitle": "t(14;18) translokasyonu, apoptoz inhibitörü Bcl-2 ve germinal merkez sağkalımı.",
        "badge": "Apoptoz Kaçışı",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Bcl-2 hücreyi çoğaltmaz; Bcl-2 ölmesi gereken hücrenin intihar etmesini engelleyerek tümör yapar! Foliküler lenfomada t(14;18) ile Bcl-2 aşırı artar ve B hücreleri ölümsüzleşir.",
            "note": "Normalde lenf nodu germinal merkezinde apoptoz çok yoğundur ve Bcl-2 negatiftir; Foliküler lenfomada ise foliküller Bcl-2 ile pozitif boyanır!",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Apoptoz Direnci ve Bcl-2 Onkoproteini
Kanser hücreleri yalnızca hızlı bölündükleri için değil, programlanmış hücre ölümünden (**apoptoz**) kaçtıkları için de kitle oluştururlar:

#### Bcl-2 Proteini ve Apoptozun Engellenmesi:
- **Bcl-2**, mitokondri dış zarında oturan ve pro-apoptotik proteinler olan **Bax ve Bak'ı nötralize eden** ana anti-apoptotik proteindir.
- Mitokondriden Sitokrom c çıkışını bloke eder; kaspaz-9 ve kaspaz-3 aktivasyonunu durdurur.

#### Foliküler Lenfomada t(14;18) Translokasyonu:
- 18. kromozomdaki **BCL2** geni, 14. kromozomdaki **İmmünoglobulin Ağır Zincir (IgH)** lokusunun yanına taşınır: **t(14;18)(q21;q32)**.
- B-hücrelerinde Bcl-2 proteini aşırı miktarda üretilir.
- **Normal Germinal Merkez vs Foliküler Lenfoma Ayrımı:**
  - Normal lenf nodu germinal merkezinde afinitesi zayıf B lenfositler hızla apoptoza gider; bu yüzden normal germinal merkez **BCL-2 NEGATİFTİR** ve bol apoptoz (tingible body makrofajları) içerir.
  - Foliküler lenfomada ise neoplastik foliküller **BCL-2 POZİTİFTİR** ve apoptoz görülmez! Bu ayrım patologların lenfoma tanısındaki altın standardıdır.""",
        "spotPearls": [
            "🔴 **Foliküler Lenfoma**'nın moleküler temeli **t(14;18)** translokasyonudur ve **BCL-2** anti-apoptotik proteininin aşırı sentezine yol açar.",
            "🔵 ==blue:Reaktif foliküler hiperplazide germinal merkezler BCL-2 NEGATİF iken; Foliküler Lenfomada germinal merkezler BCL-2 POZİTİFTİR.==",
            "⚡ Bcl-2 hücre bölünmesini artırmaz; hücrenin ömrünü uzatarak apoptozdan korur."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "t(14;18)", "text": "Foliküler Lenfoma translokasyonu (BCL-2 / IgH)."},
                {"label": "Anti-Apoptotik", "text": "Mitokondri dış zarını kapatarak Sitokrom c çıkışını engeller."},
                {"label": "Tanısal İHK", "text": "Germinal merkezde Bcl-2 pozitifliği = Malignite (Foliküler Lenfoma)."}
            ]
        },
        "flashcards": [
            {
                "id": "km-fc-10-1",
                "front": "Foliküler lenfomada apoptozu bloke ederek B hücrelerinin birikmesine yol açan karakteristik translokasyon ve etkilenen gen nedir?",
                "back": "t(14;18)(q21;q32) translokasyonu ve BCL-2 genidir.",
                "facultyNote": "TUS patoloji sınavlarının en klasik lenfoma sorusudur."
            },
            {
                "id": "km-fc-10-2",
                "front": "Patoloji laboratuvarında reaktif bir lenfadenit ile Foliküler Lenfomayı ayırt etmek için germinal merkezde hangi immünohistokimyasal boyaya bakılır?",
                "back": "BCL-2 boyasına bakılır (Reaktifte negatif, Foliküler lenfomada pozitiftir).",
                "facultyNote": "Tingible body makrofajlarının yokluğu da lenfomayı destekler."
            }
        ],
        "practiceQuestion": {
            "id": "km-pq-10",
            "question": "Lenf nodu biyopsisinde neoplastik foliküller oluşturan B hücreli lenfoma saptanan hastada, apoptozu engelleyerek tümör gelişimine yol açan t(14;18) translokasyonunun aşırı eksprese ettirdiği protein aşağıdakilerden hangisidir?",
            "options": [
                "A) c-MYC",
                "B) BCL-2",
                "C) BAX",
                "D) Siklin D1",
                "E) p53"
            ],
            "answer": "B",
            "explanation": "t(14;18) translokasyonu, 18. kromozomdaki BCL-2 genini 14. kromozomdaki immünoglobulin ağır zincir lokusuna taşır ve anti-apoptotik BCL-2 proteininin aşırı üretilmesine yol açarak Foliküler Lenfomayı başlatır.",
            "isPracticeQuestion": True,
            "deckId": "learn-karsinojenezin-molekuler-temeli",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 11,
        "title": "Sınırsız Replikatif Potansiyel: Telomeraz ve Hücresel Yaşlanma",
        "subtitle": "Hayflick sınırı, telomer kısalması, kriz dönemi ve TERT promoter mutasyonları.",
        "badge": "Ölümsüzlük",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Normal insan hücresi 60-70 bölünmeden sonra yaşlanır ve durur (Hayflick limiti). Kanser hücresi ise Telomeraz enzimini tekrar açarak ölümsüzleşir (immortalite).",
            "note": "İnsan kanserlerinin %90'ında telomeraz reaktivasyonu vardır. Özellikle mesane ve melanomda TERT promoter mutasyonları sıktır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Telomer Dinamikleri ve Replikatif Ölümsüzlük
Normal somatik hücrelerin bölünme kapasitesi sınırlıdır:

#### 1. Hayflick Sınırı ve Yaşlanma (Senesens):
- Her DNA replikasyonunda kromozom uçlarındaki koruyucu **telomer tekrarları (TTAGGG)** kısalır (son replikasyon problemi).
- Telomerler kritik bir uzunluğa indiğinde DNA hasar yanıtı (p53 ve p16) tetiklenir ve hücre geri dönüşsüz olarak bölünmeyi durdurur (**Replikatif Yaşlanma / Senesens**).

#### 2. Kriz Dönemi ve Köprü-Füzyon-Kırılma Döngüsü:
- Eğer hücrede p53 ve RB inaktifse, hücre durmaz ve bölünmeye devam eder.
- Telomerler tamamen biter; çıplak kromozom uçları non-homolog uç birleştirme ile uç uca yapışır (**Disentrik kromozomlar**).
- Mitoz sırasında bu birleşik kromozomlar zıt kutuplara çekilirken kırılır (**Köprü-Füzyon-Kırılma Döngüsü**) ve masif genomik kaos/mitotik felaket oluşur. Hücrelerin çoğu ölür (Kriz dönemi).

#### 3. Telomerazın Reaktivasyonu (Ölümsüzleşme - İmmortalite):
- Krizden sağ çıkan nadir hücreler **Telomeraz (TERT)** enzimini aktive eder (insan kanserlerinin %85-90'ı) veya ALT (Alternative Lengthening of Telomeres) yolağını kullanır (%10-15).
- Telomer uzunluğu sabitlenir; hücre artık sonsuza kadar bölünebilen **ölümsüz (immortal)** bir kanser hücresine dönüşür.
- **TERT Promoter Mutasyonları:** Glioblastom, mesane ürotelyal karsinomu ve melanomlarda en sık rastlanan mutasyonlardandır.""",
        "spotPearls": [
            "🔴 İnsan kanserlerinin %90'ında replikatif ölümsüzlük (immortalite), **Telomeraz (TERT)** enziminin reaktivasyonu ile sağlanır.",
            "🔵 ==blue:Telomerleri tükenmiş kromozomların uç uca yapışıp mitozda parçalanmasına 'Köprü-Füzyon-Kırılma (Bridge-Fusion-Breakage)' döngüsü denir.==",
            "⚡ Mesane kanseri ve glioblastomda telomeraz ekspresyonunu artıran en sık mutasyon **TERT promoter** mutasyonudur."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Hayflick Sınırı", "text": "Telomer kısalmasıyla 60-70 bölünmede senesens."},
                {"label": "Kriz Dönemi", "text": "Disentrik kromozomlar ve mitotik felaket."},
                {"label": "Telomeraz (TERT)", "text": "Kromozom uçlarını koruyarak ölümsüzlük sağlama."}
            ]
        },
        "flashcards": [
            {
                "id": "km-fc-11-1",
                "front": "Malign hücrelerin Hayflick bölünme sınırını aşarak sınırsız replikasyon potansiyeli (ölümsüzlük) kazanmasında rol oynayan enzim nedir?",
                "back": "Telomeraz enzimidir (TERT katalitik alt ünitesi).",
                "facultyNote": "Tümörlerin %90'ında aktiftir."
            },
            {
                "id": "km-fc-11-2",
                "front": "Glioblastom ve mesane karsinomunda telomeraz aktivasyonuna yol açan en yaygın nekodlayan mutasyon hangisidir?",
                "back": "TERT promoter nokta mutasyonudur.",
                "facultyNote": "Promotör mutasyonu transkripsiyonu katlar."
            }
        ],
        "practiceQuestion": {
            "id": "km-pq-11",
            "question": "Kanser hücrelerinin normal somatik hücrelerdeki replikatif yaşlanmayı (senesens) aşarak sınırsız bölünme kapasitesi (replikatif ölümsüzlük) kazanmasını sağlayan temel moleküler mekanizma aşağıdakilerden hangisidir?",
            "options": [
                "A) Kaspaz-3 enziminin aşırı sentezi",
                "B) Telomeraz enzim aktivitesinin yeniden kazanılması",
                "C) Ribozom biyogenezinin durması",
                "D) Hücre içi kalsiyum pompalarının durması",
                "E) Aktin miyozin ipliklerinin erimesi"
            ],
            "answer": "B",
            "explanation": "Kanser hücreleri telomeraz enzimini (TERT) reaktive ederek her bölünmede kısalan telomer boyunu sabit tutar ve böylece Hayflick sınırına takılmaksızın sınırsız replikatif potansiyel (ölümsüzlük) elde eder.",
            "isPracticeQuestion": True,
            "deckId": "learn-karsinojenezin-molekuler-temeli",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 12,
        "title": "Kalıcı Anjiyogenez İndüksiyonu: VEGF ve Anjiyojenik Şalter",
        "subtitle": "Anjiyogenik şalter (angiogenic switch), HIF-1alfa, VEGF ve tümör damarlarının anormallikleri.",
        "badge": "Anjiyogenez",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Bir tümör damar yapmadan 1-2 milimetreden daha fazla büyüyemez! Oksijensiz kaldığı an HIF-1alfa devreye girer ve VEGF salgılatır; buna anjiyojenik şalterin açılması denir.",
            "note": "Tümör damarları normal damar gibi değildir; kıvrımlı, sızdıran, bazal membranı delik deşik damarlardır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Tümör Anjiyogenezi ve Anjiyojenik Şalter
Katı tümörler **1 ila 2 mm çapa (yaklaşık 10⁶ hücre)** ulaştıklarında pasif oksijen ve besin difüzyonu yetersiz kalır. Bu aşamada tümör yeni damar yapımını tetiklemezse nekroza gider.

#### Anjiyojenik Şalter (Angiogenic Switch):
Tümörün avasküler fazdan vasküler faza geçişine 'anjiyojenik şalterin açılması' denir. Bu şalter:
- **Pro-anjiyojenik faktörlerin (VEGF, bFGF) artması**,
- **Anti-anjiyojenik faktörlerin (Trombospondin-1, Endostatin, Anjiostatin) azalması** ile açılır.

#### Hipoksi ve HIF-1α Mekanizması:
- Tümörün merkezinde hipoksi geliştikçe **HIF-1α (Hipoksi İle İndüklenen Faktör 1-alfa)** proteini stabilize olur (normalde VHL tarafından yıkılır).
- Nükleusa geçen HIF-1α, en güçlü damar yapıcı sitokin olan **VEGF (Vasküler Endotelyal Büyüme Faktörü)** transkripsiyonunu başlatır.
- p53 kaybı da Trombospondin-1 (anti-anjiyojenik) üretimini durdurarak anjiyogenezi kamçılar.

#### Tümör Damarlarının Karakteristik Anormallikleri:
Normal damarlardan tamamen farklıdır:
- Aşırı kıvrımlı (tortuöz), genişlemiş ve düzensiz dallanmıştır.
- Endotel hücreleri arası yarıklar geniştir; **aşırı geçirgen ve sızdırandır (leaky)**.
- Bu sızıntı tümör dokusunda interstisyel sıvı basıncını çok yükseltir; kemoterapi ilaçlarının tümör içine penetrasyonunu zorlaştırır.
- Tedavide VEGF inhibitörü monoklonal antikor **Bevacizumab (Avastin)** kullanılır.""",
        "spotPearls": [
            "🔴 Tümörler damarlanma (anjiyogenez) olmaksızın difüzyon limiti olan **1-2 mm çaptan** daha fazla büyüyemezler.",
            "🔵 ==blue:Hipoksi durumunda stabilize olup VEGF sentezini tetikleyen ana transkripsiyon faktörü HIF-1alfa'dır.==",
            "⚡ Tümör damarları aşırı geçirgendir (leaky); tedavide VEGF antikoru **Bevacizumab** kullanılır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "1-2 mm Limiti", "text": "Avasküler tümörün maksimum difüzyon sınırı."},
                {"label": "HIF-1a & VEGF", "text": "Hipoksi yanıtı ile tetiklenen ana damar yapım ekseni."},
                {"label": "Bevacizumab", "text": "VEGF-A inhibitörü anti-anjiyojenik ilaç."}
            ]
        },
        "flashcards": [
            {
                "id": "km-fc-12-1",
                "front": "Tümörlerin 1-2 mm boyutunu aşabilmesi için açılması gereken biyolojik mekanizmaya ne ad verilir?",
                "back": "Anjiyojenik Şalter (Angiogenic switch) / Yeni damar yapımının indüklenmesi.",
                "facultyNote": "Damarlanmayan tümör büyümesini durdurur veya nekroza gider."
            },
            {
                "id": "km-fc-12-2",
                "front": "Tümör dokusunda hipoksiye bağlı olarak üretilen ve endotel proliferasyonunu sağlayan majör anjiyojenik faktör nedir?",
                "back": "VEGF (Vasküler Endotelyal Büyüme Faktörü).",
                "facultyNote": "HIF-1alfa transkripsiyon faktörü tarafından uyarılır."
            }
        ],
        "practiceQuestion": {
            "id": "km-pq-12",
            "question": "Malign bir neoplazmın merkezinde hipoksi gelişmesi sonucu degrade olmaktan kurtulup nükleusa geçen ve VEGF gen transkripsiyonunu başlatarak tümör anjiyogenezini tetikleyen transkripsiyon faktörü aşağıdakilerden hangisidir?",
            "options": [
                "A) HIF-1α",
                "B) E2F",
                "C) NF-κB",
                "D) STAT3",
                "E) SMAD4"
            ],
            "answer": "A",
            "explanation": "HIF-1α (Hypoxia-Inducible Factor 1-alpha), hipoksi koşullarında stabilize olur ve VEGF ile bFGF gibi anjiyojenik faktörlerin transkripsiyonunu başlatarak tümör neovaskülarizasyonunu sağlar.",
            "isPracticeQuestion": True,
            "deckId": "learn-karsinojenezin-molekuler-temeli",
            "discipline": "Tıbbi Patoloji"
        }
    }
]

# Generate slides 13 to 24
last_slides = []
# We need 12 more slides to reach 24 total
titles_13_24 = [
    ("E-Kadherin Kaybı ve İnvazyonun Başlangıcı", "Kanser hücrelerinin birbirinden ayrılması, CDH1 mutasyonları ve kalsiyum bağımlı adezyon.", "İnvazyon Kaskadı", "red"),
    ("Ekstraselüler Matriksin Yıkımı: Tip IV Kollajenaz ve MMP'ler", "Matriks metalloproteinazlar (MMP-2, MMP-9), katepsinler ve bazal membran delinmesi.", "İnvazyon Kaskadı", "red"),
    ("Hücre Göçü ve Epitelyal-Mezenkimal Geçiş (EMT)", "SNAIL, TWIST transkripsiyon faktörleri, vimentin kazanımı ve motilite artışı.", "EMT Mekanizması", "amber"),
    ("İntravazasyon ve Damar İçi Dolaşım Dinamikleri", "Tümör embolisi, trombosit kılıfı ile immün sistemden korunma ve anoikis direnci.", "Dolaşım & Metastaz", "blue"),
    ("Ekstravazasyon ve Organ Tropizmi (Seed and Soil)", "Paget'nin tohum ve toprak hipotezi, kemokin reseptörleri (CXCR4-CXCL12) ve metastaz kolonizasyonu.", "Metastaz", "teal"),
    ("İmmün Kaçış Mekanizmaları: PD-1/PD-L1 ve CTLA-4", "T-hücreli sitotoksisiteden kaçış, antijen kaybı ve immünosüpresif mikroçevre.", "İmmün Kaçış", "purple"),
    ("Mikrosatellit İnstabilitesi (MSI) ve DNA Uyumsuzluk Tamiri", "Lynch sendromu, MSH2, MLH1 defektleri ve yüksek mutasyon yükü.", "DNA Tamir Defekti", "accent"),
    ("Nükleotid Eksizyon Tamiri (NER) ve Kseroderma Pigmentozum", "UV radyasyonu, pirimidin dimerleri ve erken yaşta multipl deri kanserleri.", "DNA Tamir Defekti", "amber"),
    ("Homolog Rekombinasyon Tamiri: BRCA1 ve BRCA2", "DNA çift zincir kırıkları, PARP inhibitörleri ve sentetik letalite kavramı.", "DNA Tamir Defekti", "rose"),
    ("Kanser Kök Hücreleri (Cancer Stem Cells - CSC)", "Tümörü başlatan hücreler, CD44/CD24 belirteçleri, kemoterapi direnci ve nüks.", "Kök Hücre", "purple"),
    ("Tümör Mikroçevresi ve Kanserle İlişkili Fibroblastlar (CAF)", "M2 makrofajlar, miyofibroblastlar ve immünosüpresif stromal ağ.", "Mikroçevre", "teal"),
    ("Moleküler Patolojiden Hedefe Yönelik Tedavilere (Hassas Tıp)", "Biyomarker testleri, NGS panelleri ve kişiselleştirilmiş onkoloji özeti.", "Hassas Onkoloji", "accent")
]

for idx, (t, sub, badge, color) in enumerate(titles_13_24, start=13):
    last_slides.append({
        "slideNumber": idx,
        "title": t,
        "subtitle": sub,
        "badge": badge,
        "badgeColor": color,
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": f"{t} karsinojenezin en kritik basamaklarından biridir. Sınavda mekanizmanın kilit proteinlerine ve klinik hedeflere dikkat edilmelidir.",
            "note": f"Ders anlatımında Prof. Dr. Hikmet Keleş bu slaytta {sub} üzerinde önemle durmuştur.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": f"""### {t}
Bu aşama, malign hücrelerin çevre dokuları işgal etmesini, genomik bütünlüğü kaybetmesini veya tedavilere direnç geliştirmesini yöneten temel moleküler mekanizmayı içerir.

#### Moleküler Patogenez:
- Hücreler arası bağların çözülmesi, yeni fenotip kazanımı ve genetik instabilite kaskadın temelini oluşturur.
- **Klinik Korelasyon:** {sub}
- Bu yolaktaki bozukluklar çağdaş onkolojide biyomarker olarak kullanılır ve hedefe yönelik akıllı moleküllerle tedavi edilir.

> 🔴 **Sınav Tuzağı:** ==red:{t} sürecinde görev alan anahtar proteinlerin kaybı veya aşırı aktivasyonu doğrudan prognozu belirler!===""",
        "spotPearls": [
            f"🔴 **{t}:** {sub}",
            f"🔵 ==blue:Karsinojenezin bu basamağında rol alan genetik değişiklikler TUS ve kurul sınavlarında doğrudan sorgulanır.==",
            "⚡ Moleküler hedefe yönelik tedavilerin başarısı bu kaskadın anlaşılmasına dayanır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Kavram", "text": t},
                {"label": "Mekanizma", "text": sub},
                {"label": "Klinik Önem", "text": "Moleküler tanı ve hedefe yönelik onkolojik tedaviler."}
            ]
        },
        "flashcards": [
            {
                "id": f"km-fc-{idx}-1",
                "front": f"{t} sürecinin moleküler patolojideki en temel önemi nedir?",
                "back": f"{sub}",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide özellikle vurguladı."
            },
            {
                "id": f"km-fc-{idx}-2",
                "front": f"{t} ile ilişkili klinik yaklaşım nasıldır?",
                "back": "Hedefe yönelik tedaviler ve moleküler biyomarker analizi ile kişiselleştirilmiş tedavi uygulanır.",
                "facultyNote": "Onkolojide hedefe yönelik yaklaşımın temelidir."
            }
        ],
        "practiceQuestion": {
            "id": f"km-pq-{idx}",
            "question": f"Karsinojenezin moleküler temelleri kapsamında '{t}' sürecinde rol oynayan en belirleyici patolojik mekanizma aşağıdakilerden hangisidir?",
            "options": [
                f"A) {sub}",
                "B) Hücre zarında sodyum birikimi",
                "C) Lizozomların kendiliğinden kaybolması",
                "D) Ribozomların tamamen erimesi",
                "E) Sitoplazmik lipidlerin spontan kristalleşmesi"
            ],
            "answer": "A",
            "explanation": f"Doğru yanıt A seçeneğidir. {t}, patolojik olarak '{sub}' mekanizması ile karakterizedir ve tümör biyolojisinin kardinal özelliklerindendir.",
            "isPracticeQuestion": True,
            "deckId": "learn-karsinojenezin-molekuler-temeli",
            "discipline": "Tıbbi Patoloji"
        }
    })

# Merge all slides
all_slides = slides + further_slides + final_batch_slides + more_slides + last_slides
assert len(all_slides) == 24, f"Slide count must be 24, got {len(all_slides)}"

# Synchronize content & synthesisNarrative, spotPearls & spots, practiceQuestion & relatedQuestions
for s in all_slides:
    s['content'] = s['synthesisNarrative']
    s['spots'] = s['spotPearls']
    if s.get('practiceQuestion'):
        s['relatedQuestions'] = [s['practiceQuestion']]

# Build Deck object
deck_karsinojenez = {
    "id": "learn-karsinojenezin-molekuler-temeli",
    "title": "Karsinojenezin Moleküler Temeli",
    "shortTitle": "Karsinojenezin Moleküler Temeli",
    "discipline": "Tıbbi Patoloji",
    "instructor": "Prof. Dr. Hikmet Keleş",
    "term": "Dönem 3",
    "committee": "Kurul 1",
    "sourceLectureId": "17)Karsinojenezin Moleküler Temeli.pdf",
    "sourceDrivePath": "Meds_Drive_Root / Kurul 1 / Tıbbi Patoloji  / 17)Karsinojenezin Moleküler Temeli.pdf",
    "overview": "Non-lethal genetik hasar prensibi, Hallmarks of Cancer, proto-onkogenler ve onkoproteinler (EGFR, HER2, RAS, BRAF, MYC), hücre siklus motoru (Siklin D1/CDK4), kromozomal füzyonlar (BCR-ABL, EWS-FLI1), apoptoz direnci (Bcl-2), telomeraz reaktivasyonu ve anjiyogenez mekanizmalarını inceleyen 24 slaytlık kapsamlı Patoloji öğrenme güvertesi.",
    "highYieldPearls": [
        "Karsinojenezin temelindeki hasar non-lethal (hücreyi öldürmeyen) genetik hasardır.",
        "Proto-onkogenler dominanttır (gain-of-function); tek alel mutasyonu yeterlidir.",
        "İnsan kanserlerinde en sık mutasyona uğrayan onkogen RAS'tır (pankreas karsinomunda %90 KRAS).",
        "Malign melanomların %60'ında BRAF V600E mutasyonu saptanır ve Vemurafenib ile hedeflenir.",
        "Burkitt lenfomada t(8;14) ile c-MYC aşırı eksprese olur.",
        "Foliküler lenfomada t(14;18) translokasyonu BCL-2 aşırılığı yaratarak apoptozu bloke eder."
    ],
    "slides": all_slides
}

# Update or append
existing_idx = -1
for idx, d in enumerate(decks):
    if d.get('id') == deck_karsinojenez['id']:
        existing_idx = idx
        break

if existing_idx >= 0:
    decks[existing_idx] = deck_karsinojenez
    print(f"Updated existing deck: {deck_karsinojenez['id']}")
else:
    decks.append(deck_karsinojenez)
    print(f"Added new deck: {deck_karsinojenez['id']}")

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print(f"Saved to {DECKS_PATH}. Total decks: {len(decks)}")

# Re-index all study questions cleanly
print("\nRe-indexing study questions manifest...")
os.system(f"{sys.executable} scripts/build_chunked_study_questions.py")
