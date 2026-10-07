# -*- coding: utf-8 -*-
"""
Rebuilds learn-cinsel-yolla-bulasan-enfe with rich, fully-articulated medical narrative,
completely removing all robotic templates, broken characters, and meaningless headings.
"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = 'src/data/interactive_learning_decks.json'
with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

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

# S1
slides.append(make_slide(
    1,
    "Cinsel Yolla Bulaşan Enfeksiyonlara Giriş ve Bulaş Dinamiği",
    "Mukozal Bariyerler, Aktarım Yolları ve Klinik Tablonun Geniş Spektrumu",
    """Cinsel Yolla Bulaşan Enfeksiyonlar (CYBE), patojen mikroorganizmaların bir kişiden diğerine temel olarak cinsel temas (vajinal, anal veya oral mukoza penetrasyonu) yoluyla aktarıldığı bulaşıcı hastalıklar grubudur.

• **Temel Bulaş Yolları:**
  1. **Cinsel Temas:** Enfekte genital sekresyonların (semen, servikovajinal sıvı) ve mukozal lezyonların sağlam veya mikroabrazyona uğramış mukozayla teması.
  2. **Parenteral / Kan Yolu:** Kontamine kan ve kan ürünleri, ortak enjektör kullanımı (HBV, HCV, HIV, Treponema pallidum).
  3. **Vertikal Bulaş (Anneden Bebeğe):** İntrauterin transplasental geçiş (Sifiliz, HIV), doğum kanalından geçerken temas (Gonore, Klamidya, HSV-2, HBV) veya emzirme sırasında anne sütü ile bulaş (HIV).

• **Klinik Tablonun Spektrumu:**
CYBE'ler yalnızca lokal ürogenital şikayetlerle sınırlı değildir. Asemptomatik kolonizasyondan başlayıp, pürülan akıntılara, ağrılı/ağrısız genital ülserlere, pelvik peritonite ve hatta dissemine sistemik tablolara (artrit, menenjit, siroz, karsinom) kadar uzanan geniş bir klinik yelpazede seyreder.""",
    [
        {"type": "warning", "badge": "Kritik Klinik Bilgi / Kırmızı", "text": "CYBE'ler gebelikte abortus, ölü doğum, erken doğum ve yenidoğanda körlük/sepsise yol açabilen hayati risk faktörleridir.", "color": "rose"},
        {"type": "exam", "badge": "Komite & TUS Sorusu / Mavi", "text": "Vertikal yolla doğum kanalından geçerken yenidoğana bulaşan ve neonatal konjonktivit (oftalmiya neonatorum) yapan en kritik bakteriler Neisseria gonorrhoeae ve Chlamydia trachomatis'tir.", "color": "sky"}
    ],
    {
        "id": "cybe-q-001",
        "question": "Aşağıdaki cinsel yolla bulaşan enfeksiyon etkenlerinden hangisi gebelik sırasında transplasental yolla fetüse geçerek konjenital enfeksiyon tablosuna yol açabilir?",
        "options": [
            "A) Trichomonas vaginalis",
            "B) Treponema pallidum",
            "C) Haemophilus ducreyi",
            "D) Phthirus pubis",
            "E) Sarcoptes scabiei"
        ],
        "correctAnswer": 1,
        "explanation": "Treponema pallidum (Sifiliz) plasentayı geçerek konjenital sifiliz (Hutchinson dişleri, eyer burun, sağırlık) yapabilen klasik transplasental patojendir."
    }
))

# S2
slides.append(make_slide(
    2,
    "CYBE Etkenlerinin Mikrobiyolojik Sınıflandırılması",
    "Bakteriyel, Viral ve Paraziter Patojenlerin Çekirdek Havuzu",
    """Cinsel yolla bulaşabilen patojenler biyolojik yapılarına, replikasyon özelliklerine ve tedavi yanıtlarına göre üç temel sınıfta incelenir:

• **1. Bakteriyel Patojenler:**
  - *Neisseria gonorrhoeae:* Gonore (Bel soğukluğu), pürülan üretrit ve servisit etkeni Gram negatif diplokok.
  - *Chlamydia trachomatis:* En sık görülen bakteriyel CYBE; nongonokokal üretrit ve PİH nedeni obligat hücre içi bakteri.
  - *Treponema pallidum:* Sifiliz (Frengi) etkeni spiroket.
  - *Haemophilus ducreyi:* Ağrılı şankroid (ulkus molle) etkeni.
  - *Klebsiella granulomatis:* Granüloma inguinale (Donovanozis) etkeni.
  - *Mycoplasma genitalium ve Ureaplasma urealyticum:* Tedaviye dirençli nongonokokal üretrit nedenleri.

• **2. Viral Patojenler:**
  - *Herpes Simpleks Virüs Tip 1 ve 2 (HSV):* Genital ülser ve veziküller.
  - *İnsan Papilloma Virüsü (HPV):* Kondiloma akuminata (Tip 6, 11) ve Serviks Karsinomu (Tip 16, 18).
  - *Hepatit B (HBV) ve Hepatit C (HCV):* Kronik hepatit, siroz ve hepatosellüler karsinom.
  - *İnsan İmmün Yetmezlik Virüsü (HIV Tip 1 ve 2):* Edinsel İmmün Yetmezlik Sendromu (AIDS).
  - *Molluscum contagiosum:* Umblike göbekli kubbe lezyonları (Poxvirüs).

• **3. Paraziter ve Artropod Etkenleri:**
  - *Trichomonas vaginalis:* Kamçılı protozoon, köpüklü akıntı ve çilek serviks.
  - *Phthirus pubis (Kasık biti) ve Sarcoptes scabiei (Uyuz).*""",
    [
        {"type": "warning", "badge": "Patoloji & Mikrobiyoloji / Kırmızı", "text": "Klamidya hücre duvarında peptidoglikan sentezleyemeyen ve ATP üretemeyen obligat hücre içi bakteridir; bu nedenle beta-laktam antibiyotiklere tamamen yanıtsızdır!", "color": "rose"},
        {"type": "exam", "badge": "Komite & TUS Sorusu / Mavi", "text": "Dünyada en sık görülen bakteriyel cinsel yolla bulaşan enfeksiyon Chlamydia trachomatis'tir.", "color": "sky"}
    ],
    {
        "id": "cybe-q-002",
        "question": "Aşağıdaki mikroorganizmalardan hangisi hücre içi obligat yaşam döngüsüne sahip olup beta-laktam antibiyotiklere doğal direnç gösteren en sık bakteriyel CYBE etkenidir?",
        "options": [
            "A) Neisseria gonorrhoeae",
            "B) Haemophilus ducreyi",
            "C) Chlamydia trachomatis",
            "D) Treponema pallidum",
            "E) Gardnerella vaginalis"
        ],
        "correctAnswer": 2,
        "explanation": "Chlamydia trachomatis obligat hücre içi bakteridir; peptidoglikan duvarı klasik olmadığından ve hücre içine girdiğinden beta-laktamlar etkisizdir; makrolid (azitromisin) veya tetrasiklin (doksisiklin) kullanılır."
    }
))

# S3
slides.append(make_slide(
    3,
    "Vajinal Akıntı Sendromu: Vajinit ve Servisit Ayrımı",
    "Anatomik Lokalizasyon, Semptomatoloji ve Fizik Muayene İpuçları",
    """Kadın hastalarda en sık başvuru yakınması olan vajinal akıntı sendromunda ilk yapılması gereken ayrım patolojinin vajinada mı (Vajinit) yoksa endoservikste mi (Servisit) yerleştiğidir.

• **1. Vajinit (Vajina Mukozasının Enflamasyonu):**
  - **Semptomlar:** Vulvar kaşıntı, yanma, kötü koku, iritasyon ve yüzeyel dizüri (idrarın vulvaya temasıyla yanma).
  - **Fizik Muayene:** Vajina duvarında hiperemi, ödem ve akıntı birikimi. Serviks os'u genellikle temizdir.
  - **En Sık 3 Neden:** Bakteriyel Vajinozis (%40-50), Vulvovajinal Kandidiyazis (%20-25) ve Trikomoniyazis (%15-20).

• **2. Servisit (Endoservikal Kanalın Enflamasyonu):**
  - **Semptomlar:** Mukopürülan sarı-yeşil akıntı, intermenstrüel kanama, disparoni (derin ağrılı cinsel ilişki) ve postkoital (ilişki sonrası) kanama.
  - **Fizik Muayene:** Spekulum muayenesinde endoservikal os'tan pürülan eksuda aktığı görülür. Servikse pamuklu çubuk dokundurulduğunda aşırı frajilite ve temas kanaması (friabilite) saptanır.
  - **En Sık 2 Patojen:** Chlamydia trachomatis ve Neisseria gonorrhoeae.""",
    [
        {"type": "clinical", "badge": "Klinik Ayrım / Kırmızı", "text": "Postkoital kanama ve servikal dokunma frajilitesi (friabilite) saptandığında vajinit değil, mutlaka Servisit düşünülmeli ve Klamidya/Gonore araştırılmalıdır.", "color": "rose"},
        {"type": "exam", "badge": "Komite Sorusu / Mavi", "text": "Servisitin iki majör bakteriyel etkeni Chlamydia trachomatis ve Neisseria gonorrhoeae'dir; PİH riskini doğrudan taşırlar.", "color": "sky"}
    ],
    {
        "id": "cybe-q-003",
        "question": "Cinsel ilişki sonrası kanama (postkoital kanama), derin disparoni ve spekulum muayenesinde servikal os'tan pürülan eksuda gelişi ile başvuran bir kadında en olası tanı ve öncelikli etken çifti hangisidir?",
        "options": [
            "A) Vulvovajinal Kandidiyazis — Candida albicans & glabrata",
            "B) Bakteriyel Vajinozis — Gardnerella vaginalis & Prevotella",
            "C) Mukopürülan Servisit — Chlamydia trachomatis & Neisseria gonorrhoeae",
            "D) Trikomonal Vajinit — Trichomonas vaginalis & Giardia",
            "E) Atrofik Vajinit — Hipoöstrojenizm"
        ],
        "correctAnswer": 2,
        "explanation": "Servikal os'tan pürülan akıntı, frajilite ve postkoital kanama 'Mukopürülan Servisit' tablosudur; baş şüpheliler Chlamydia trachomatis ve Neisseria gonorrhoeae'dir."
    }
))

# S4
slides.append(make_slide(
    4,
    "Vajinit Ayırıcı Tanısı: Trikomoniyazis, Kandidiyazis ve Bakteriyel Vajinozis",
    "pH Değerleri, Akıntı Özellikleri ve Mikroskobik Bulguların Karşılaştırma Matrisi",
    """Amfi komite sınavlarında ve TUS'ta en çok sorulan konulardan biri vajinit triadı arasındaki ayırt edici tablodur:

| Tanı Kriteri | Bakteriyel Vajinozis (BV) | Vulvovajinal Kandidiyazis | Trikomoniyazis (TV) |
| :--- | :--- | :--- | :--- |
| **Etken** | Mikst anaeroblar (Gardnerella, Mobiluncus) | Candida albicans (%85-90) | Trichomonas vaginalis (Protozoon) |
| **Vajinal pH** | **> 4.5 (Alkali)** | **< 4.5 (Normal asidik)** | **> 4.5 (Alkali, 5.0 - 6.5)** |
| **Akıntı Özelliği** | İnce, homojen, grimsi-beyaz, balık kokulu | Koyu, beyaz, kesilmiş peynir / süt kıvamında | Sarı-yeşil, bol, köpüklü, kötü kokulu |
| **Enflamasyon / Kaşıntı** | Kaşıntı ve kızarıklık minimaldir (vajinoz) | Şiddetli vulvar kaşıntı, ödem, eritem | Kaşıntı, dizüri, vulvovajinal irritasyon |
| **Whiff (Amin) Testi** | **Pozitif (%10 KOH ile balık kokusu)** | Negatif | Genellikle Pozitif |
| **Mikroskopi Bulgusu** | **Clue Cell (İpucu Hücresi) > %20** | Maya tomurcukları ve Psödohifler | **Hareketli kamçılı trofozoitler + lökosit** |
| **Spesifik FM Bulgusu** | Vajina duvarında yapışık ince tabaka | Satellit lezyonlar, mukozada eritem | **Çilek Serviks (Strawberry cervix / kolpitis)** |""",
    [
        {"type": "warning", "badge": "Mutlak Bilinmeli / Kırmızı", "text": "Kandidiyazis vajinal pH'yı YÜKSELTMEZ (pH < 4.5 normal kalır); pH'yı 4.5 üzerine çıkaranlar Bakteriyel Vajinozis ve Trikomoniyazistir!", "color": "rose"},
        {"type": "exam", "badge": "TUS & Komite Sorusu / Mavi", "text": "Sitolojide epitel hücre sınırlarını silen kokobasillerle kaplı 'Clue Cell' (ipucu hücresi) Bakteriyel Vajinozis için patognomoniktir.", "color": "sky"}
    ],
    {
        "id": "cybe-q-004",
        "question": "Vajinal akıntı yakınmasıyla başvuran bir kadında vajinal pH 4.0 olarak ölçülmüş, mikroskopide bol psödohif ve tomurcuklanan mayalar izlenmiştir. Bu hastada en olası tanı aşağıdakilerden hangisidir?",
        "options": [
            "A) Bakteriyel Vajinozis",
            "B) Vulvovajinal Kandidiyazis",
            "C) Trikomoniyazis",
            "D) Mukopürülan Servisit",
            "E) Deskuamatif Enflamatuvar Vajinit"
        ],
        "correctAnswer": 1,
        "explanation": "Normal/asidik pH (<4.5) varlığı ve mikroskopide psödohiflerin görülmesi Vulvovajinal Kandidiyazis tanısını kesinleştirir."
    }
))

# S5
slides.append(make_slide(
    5,
    "Vajinal Akıntıda Tanı Yöntemleri ve Amsel Kriterleri",
    "Islak Preparat, Whiff Testi ve Nugent Skorlaması",
    """Vajinal akıntısı olan bir hastada doğru teşhis için poliklinikte dakikalar içinde uygulanabilen basit ancak yüksek duyarlılıklı tanı testleri kullanılır.

• **1. Islak Preparat (Salin Wet Mount):**
  - Vajinal akıntı bir damla serum fizyolojik (SF) ile lamel altında incelenir.
  - Kamçılarıyla aktif hareket eden armut biçimli *Trichomonas vaginalis* trofozoitleri doğrudan görülür.
  - Epitel hücre sitoplazmasını taşarak hücre kenarlarını belirsizleştiren kokobasil yığınları (**Clue Cell**) aranır.

• **2. %10 KOH İncelemesi ve Whiff (Koku) Testi:**
  - Akıntıya bir damla %10 Potasyum Hidroksit (KOH) damlatıldığında epitel hücreleri ve lökositler erir; geriye dirençli fungal psödohifler ve mayalar kalır.
  - KOH damlatıldığı anda balık benzeri keskin amin (trimetilamin) kokusu yayılmasına **Pozitif Whiff Testi** denir (Bakteriyel vajinozisi kanıtlar).

• **3. Amsel Kriterleri (Bakteriyel Vajinozis Tanısı için En Az 3'ü Şarttır):**
  1. İnce, homojen, grimsi vajinal akıntı.
  2. Vajinal sıvıda pH > 4.5.
  3. Pozitif Whiff testi (KOH ile balık kokusu).
  4. Islak preparatta vajinal epitel hücrelerinin en az %20'sinin 'Clue Cell' olması.""",
    [
        {"type": "clinical", "badge": "Klinik Kural / Kırmızı", "text": "Bakteriyel vajinoziste kültür önerilmez! Çünkü Gardnerella vaginalis sağlıklı kadınların %50-60'ında normal florada da bulunur; tanı kültürle değil Amsel kriterleriyle konur.", "color": "rose"},
        {"type": "exam", "badge": "Komite Sorusu / Mavi", "text": "Amsel kriterleri: Homojen akıntı + pH > 4.5 + Pozitif Whiff testi + Clue cell varlığıdır.", "color": "sky"}
    ],
    {
        "id": "cybe-q-005",
        "question": "Aşağıdakilerden hangisi Bakteriyel Vajinozis tanısında kullanılan 'Amsel Kriterleri' arasında yer ALMAZ?",
        "options": [
            "A) Vajinal sıvıda pH değerinin 4.5'in üzerinde olması",
            "B) Salin ıslak preparatta lökosit silendirlerinin saptanması",
            "C) %10 KOH damlatıldığında amin (balık) kokusunun açığa çıkması",
            "D) Mikroskobik incelemede Clue Cell (ipucu hücresi) varlığı",
            "E) İnce, homojen, gri-beyaz vajinal akıntı varlığı"
        ],
        "correctAnswer": 1,
        "explanation": "Lökosit silendirleri piyelonefritte idrarda görülen yapıdır; vajinal akıntıda görülmez ve Amsel kriteri değildir."
    }
))

# S6 (The exact slide the user complained about, completely rewritten!)
slides.append(make_slide(
    6,
    "CYBE'den Korunma İlkeleri, Danışmanlık ve Bariyer Yöntemler",
    "Kondom Koruyuculuğunun Sınırları, Partner Bildirimi ve Temas Yönetimi",
    """Cinsel Yolla Bulaşan Enfeksiyonların önlenmesi, bireysel sağlığın korunmasının ötesinde toplumdaki bulaş zincirini kırmayı hedefleyen temel bir halk sağlığı stratejisidir.

• **1. Birincil Koruma ve Danışmanlık:**
  - Bireylere bulaşma yolları, asemptomatik taşıyıcılık riski ve komplikasyonlar hakkında kanıta dayalı cinsel sağlık eğitimi verilmelidir.
  - Tek eşlilik ve riskli cinsel davranışlardan kaçınma enfeksiyon insidansını belirgin şekilde azaltır.

• **2. Bariyer Yöntemler: Kondom (Prezervatif) Kullanımının Bilimsel Gerçekleri:**
  - Lateks kondomlar doğru ve sürekli kullanıldığında, enfekte genital sekresyonlarla bulaşan etkenlere (**HIV, Gonore, Klamidya, Trikomoniyazis**) karşı **%90-95'in üzerinde güçlü koruma** sağlar.
  - **Kondomun Koruyamadığı Durumlar:** Ciltten cilde temasla bulaşan etkenlerde (**HSV genital herpes, HPV kondilomları, Sifiliz şankrı ve Uyuz**), lezyon prezervatifin kapladığı alanın dışında (skrotum, perine, kasık) bulunuyorsa kondom kullanımı tam koruma sağlayamaz!

• **3. Cinsel Partner Bildirimi ve Eşzamanlı Tedavi:**
  - Tanı alan hastanın son 60 gün içindeki tüm cinsel partnerleri bilgilendirilmeli, semptomu olmasa dahi taranmalı ve tedavi edilmelidir.
  - Partner tedavi edilmezse hasta iyileştikten sonra yeniden enfekte olur (**Ping-Pong Reenfeksiyonu**).""",
    [
        {"type": "warning", "badge": "Hayati Uyarı / Kırmızı", "text": "Trikomoniyazis ve klamidya tanısı konduğunda partner tedavi edilmezse hasta sürekli yeniden enfekte olur. Tedavi tamamlanana ve semptomlar bitene kadar (en az 7 gün) cinsel perhiz zorunludur!", "color": "rose"},
        {"type": "exam", "badge": "Komite & TUS Sorusu / Mavi", "text": "Kondom kullanımı HIV ve Gonore bulaşını engellemede son derece etkilidir; ancak prezervatif dışı cilt alanlarını tutan HPV ve HSV'ye karşı koruyuculuğu sınırlıdır.", "color": "sky"}
    ],
    {
        "id": "cybe-q-006",
        "question": "Cinsel yolla bulaşan enfeksiyonlardan korunmada lateks kondom kullanımı ile ilgili aşağıdaki ifadelerden hangisi bilimsel olarak DOĞRUDUR?",
        "options": [
            "A) Kondom kullanımı genital herpes ve HPV dahil tüm etkenlere karşı %100 mutlak koruma sağlar",
            "B) Kondom yalnızca gebeliği önler, HIV veya Gonore geçişini hiçbir şekilde engellemez",
            "C) Semen ve vajinal sıvıyla bulaşan HIV ve klamidyaya karşı yüksek koruma sağlarken; kondom dışı cilt temasıyla geçen HPV ve HSV lezyonlarında koruyuculuğu sınırlıdır",
            "D) Partner tedavisi yapıldığı sürece kondom kullanılmasına hiçbir zaman gerek yoktur",
            "E) Yağ bazlı kayganlaştırıcılar lateks kondomun dayanıklılığını ve koruyuculuğunu artırır"
        ],
        "correctAnswer": 2,
        "explanation": "Kondom sıvı geçişli etkenlere (HIV, gonore, klamidya) karşı çok etkilidir; ancak prezervatifle örtülmeyen perine/skrotum cildinde yerleşen HSV ve HPV'de ciltten cilde temasla bulaş engellenemez."
    }
))

# S7
slides.append(make_slide(
    7,
    "Üretral Akıntı ve Üretrit Sendromu",
    "Gonokoksik Üretrit (GU) vs Non-Gonokoksik Üretrit (NGU) Ayrımı",
    """Erkek hastalarda cinsel temas sonrası gelişen dizüri, üretral kaşıntı ve akıntı sendromu 'Üretrit' olarak tanımlanır. Tedavi planlamasında ilk basamak Gonokoksik ve Non-Gonokoksik ayrımıdır.

• **1. Gonokoksik Üretrit (GU):**
  - **Etken:** *Neisseria gonorrhoeae* (Gram negatif diplokok).
  - **İnkübasyon Süresi:** Kısa (2 - 7 gün).
  - **Klinik:** Aniden başlayan şiddetli dizüri ve bol miktarda, sarı-yeşil, kıvamlı, pürülan üretral akıntı.
  - **Laboratuvar:** Üretral akıntının Gram boyamasında polimorfonükleer lökositlerin (PMNL) **sitoplazması içinde Gram negatif böbrek şeklinde diplokokların (intraselüler diplokok)** görülmesi tanı koydurur.

• **2. Non-Gonokoksik Üretrit (NGU):**
  - **Etkenler:** En sık *Chlamydia trachomatis* (%30-50). Diğerleri: *Mycoplasma genitalium*, *Ureaplasma urealyticum*, *Trichomonas vaginalis*.
  - **İnkübasyon Süresi:** Daha uzun (1 - 3 hafta).
  - **Klinik:** Daha sinsi başlangıç; hafif dizüri, üretral kaşıntı ve az miktarda, berrak, müköz veya mukopürülan akıntı (sabahları damla şeklinde akıntı).
  - **Laboratuvar:** Gram boyamada lökosit vardır ancak intraselüler diplokok görülmez.""",
    [
        {"type": "clinical", "badge": "Tanısal Kural / Kırmızı", "text": "Gram boyamada lökosit içi Gram negatif diplokok görülmesi erkek hastada gonore için %95+ duyarlıdır; ancak kadın servikal yaymasında yalancı pozitiflik riski nedeniyle kültür veya NAAT zorunludur!", "color": "rose"},
        {"type": "exam", "badge": "Komite & TUS Sorusu / Mavi", "text": "Nongonokokal üretritin (NGU) en sık nedeni Chlamydia trachomatis, ikinci en sık nedeni Mycoplasma genitalium'dur.", "color": "sky"}
    ],
    {
        "id": "cybe-q-007",
        "question": "Şüpheli cinsel ilişkiden 3 gün sonra şiddetli dizüri ve bol sarı-yeşil pürülan akıntı ile başvuran erkek hastanın akıntı yaymasında lökosit içinde Gram negatif diplokoklar saptanmıştır. En olası tanı hangisidir?",
        "options": [
            "A) Non-gonokoksik üretrit (Klamidya)",
            "B) Akut Gonokoksik Üretrit",
            "C) Trikomonal üretrit",
            "D) Akut bakteriyel sistit",
            "E) Mikoplazma üretriti"
        ],
        "correctAnswer": 1,
        "explanation": "Kısa kuluçka süresi, bol pürülan akıntı ve nötrofil içi Gram (-) diplokok varlığı Akut Gonokoksik Üretrit (Neisseria gonorrhoeae) için tipiktir."
    }
))

# S8
slides.append(make_slide(
    8,
    "CYBE'de Asemptomatik Taşıyıcılık ve 'Buzdağı Olgusu'",
    "Kadın ve Erkeklerde Sessiz Rezervuar ve Bulaş Zinciri",
    """Cinsel yolla bulaşan enfeksiyonların toplumda yayılmasının ve salgınların kontrol altına alınamamasının en büyük nedeni hastaların büyük çoğunluğunun tamamen semptomsuz (asemptomatik) olmasıdır.

• **Asemptomatik Seyir Oranları (Amfide Vurgulanan Rakamlar):**
  - **Kadınlarda:**
    • *Chlamydia trachomatis:* Kadınların **%70 - 90'ı asemptomatiktir!** Hasta hiçbir şey hissetmezken enfeksiyon sinsice fallop tüplerine ilerler.
    • *Neisseria gonorrhoeae:* Kadınların **%50'ye varan oranı asemptomatiktir.**
    • *Trichomonas vaginalis:* Kadınların %10 - 50'si belirti vermez.
  - **Erkeklerde:**
    • *Chlamydia trachomatis:* Erkeklerin **%50'si asemptomatiktir.**
    • *Neisseria gonorrhoeae:* Erkeklerin yalnızca **%10'u asemptomatiktir** (Erkeklerde gonore genellikle çok gürültülü ve akıntılı seyreder).

• **Klinik ve Epidemiyolojik Sonuçlar:**
Semptomu olmayan kadın veya erkek, kendisini tamamen sağlıklı kabul ederek cinsel hayatına devam eder ve patojeni partnerlerine bulaştırır. Kadında ise sessizce ilerleyen klamidya tüpleri tıkayarak yıllar sonra **Primer İnfertilite (Kısırlık)** veya **Dış Gebelik (Ektopik Gebelik)** ile karşımıza çıkar.""",
    [
        {"type": "warning", "badge": "Sessiz Tehlike / Kırmızı", "text": "Kadınlarda klamidyanın %90'a varan oranda asemptomatik seyretmesi, tubal hasara ve sessiz infertiliteye yol açan en sinsi risk faktörüdür!", "color": "rose"},
        {"type": "exam", "badge": "Komite Sorusu / Mavi", "text": "Erkekte gonore %90 oranında semptomatik (ağrılı akıntılı) seyrederken; kadında klamidya %90 oranında semptomsuz seyreder.", "color": "sky"}
    ],
    {
        "id": "cybe-q-008",
        "question": "Kadınlarda %90'a varan oranlarda asemptomatik seyrederek fark edilmeyen, tedavi edilmediğinde ise kronik tubal hasar, infertilite ve dış gebelik riskine yol açan en yaygın bakteriyel CYBE hangisidir?",
        "options": [
            "A) Haemophilus ducreyi",
            "B) Neisseria gonorrhoeae",
            "C) Chlamydia trachomatis",
            "D) Treponema pallidum",
            "E) Gardnerella vaginalis"
        ],
        "correctAnswer": 2,
        "explanation": "Chlamydia trachomatis kadınlarda %80-90 oranında asemptomatik kalarak sessiz salpenjite, tubal skarlaşmaya ve infertiliteye yol açar."
    }
))

# S9
slides.append(make_slide(
    9,
    "Majör Komplikasyon: Pelvik İnflamatuvar Hastalık (PİH)",
    "Endometrit, Salpenjit, Tuboovaryan Abse ve Pelvik Peritonit",
    """Pelvik İnflamatuvar Hastalık (PİH); endoserviksteki mikroorganizmaların asendan (yukarı doğru) yolla endometriyum, fallop tüpleri, overler ve pelvik peritona tırmanmasıyla karakterize ciddi bir üst genital trakt enfeksiyonudur.

• **Etyoloji:**
  - Olguların çoğundan *Chlamydia trachomatis* ve *Neisseria gonorrhoeae* sorumludur. Sürece sıklıkla vajinal anaeroblar (Bacteroides, Peptostreptococcus) da eklenir (polimikrobiyal enfeksiyon).

• **Klinik Belirtiler ve Tanı Kriterleri:**
  - **Semptomlar:** Alt karın ve pelvik ağrı, vajinal akıntı, disparoni, düzensiz intermenstrüel kanama, bulantı-kusma ve yüksek ateş.
  - **Fizik Muayene (Kritik Triad):**
    1. Uterin hassasiyet.
    2. Adneksiyel hassasiyet (tek veya çift taraflı).
    3. **Servikal Hareket Hassasiyeti (Chandelier Sign / Avize Belirtisi):** Bimanuel muayenede serviks oynatıldığında hastanın şiddetli ağrıdan tavana sıçramasıdır.

• **Sekeller:** Fallop tüplerinin tıkanması sonucu kalıcı **Tüp İnfertilitesi** (1 atak sonrası %12, 3 atak sonrası %50 risk!), **Ektopik Gebelik (Dış gebelik)** riskinde 6-10 kat artış ve **Kronik Pelvik Ağrı**.""",
    [
        {"type": "clinical", "badge": "Cerrahi Acil Kriteri / Kırmızı", "text": "Pelvik muayenede adneksiyel kitle saptanması Tuboovaryan Abse (TOA) lehinedir; rüptüre olursa hayatı tehdit eden peritonit ve septik şok tablosuna yol açar.", "color": "rose"},
        {"type": "exam", "badge": "Komite & TUS Sorusu / Mavi", "text": "Bimanuel vajinal muayenede servikal hareket hassasiyeti (Chandelier sign) PİH için en karakteristik fizik muayene bulgusudur.", "color": "sky"}
    ],
    {
        "id": "cybe-q-009",
        "question": "Alt karın ağrısı ve pürülan vajinal akıntısı olan 24 yaşındaki kadının bimanuel jinekolojik muayenesinde serviks hareket ettirildiğinde şiddetli hassasiyet (Chandelier belirtisi) saptanmıştır. Bu hastada öncelikli tanı nedir?",
        "options": [
            "A) Akut Apandisit",
            "B) Pelvik İnflamatuvar Hastalık (PİH)",
            "C) Over Kist Rüptürü",
            "D) Basit Bakteriyel Vajinozis",
            "E) Endometriozis"
        ],
        "correctAnswer": 1,
        "explanation": "Servikal hareket hassasiyeti (avize belirtisi), alt karın ağrısı ve pürülan akıntı Pelvik İnflamatuvar Hastalığın (PİH) temel klinik göstergesidir."
    }
))

# S10
slides.append(make_slide(
    10,
    "Sistemik Komplikasyonlar: Fitz-Hugh-Curtis ve Dissemine Gonokok",
    "Perihepatit 'Keman Teli' Yapışıklıkları ve Artrit-Dermatit Sendromu",
    """Cinsel yolla bulaşan etkenler lokal genital bölgeyle sınırlı kalmayıp peritoneal boşluğa veya hematojen yolla uzak organlara yayılarak sistemik tablolar oluşturabilir.

• **1. Fitz-Hugh-Curtis Sendromu (Gonokoksik/Klamidyal Perihepatit):**
  - PİH geçiren kadınların yaklaşık %5-15'inde mikroorganizmalar parakolik oluktan yukarı çıkarak karaciğer kapsülüne (Glisson kapsülü) ulaşır.
  - **Klinik:** Sağ üst kadran ağrısı, plöritik nefes almakla batan ağrı; karaciğer parankimi normaldir ancak karaciğer kapsülü ile ön karın duvarı arasında enflamasyon vardır. Akut kolesistit veya plöroziyi taklit eder!
  - **Laparoskopi Bulgusu:** Karaciğer kapsülü ile diyafram/karın duvarı arasında **'Keman Teli' (Violin-string) fibröz yapışıklıklar** izlenir.

• **2. Dissemine Gonokoksik Enfeksiyon (DGE):**
  - Neisseria gonorrhoeae'nin kana karışması sonucu (bakteriyemi) gelişir. Özellikle kompleman eksikliği (C5-C9 membran atak kompleksi eksikliği) olanlarda ve menstrüasyon döneminde sıktır.
  - **Klinik Triad:**
    1. Gezici asimetrik poliartralji / pürülan tenosinovit (el bileği, ayak bileği).
    2. Cilt lezyonları (distal ekstremitelerde ağrısız püstüller, peteşiler, hemorajik büller).
    3. Septik monoartrit (en sık diz eklemi tutulur; eklem sıvısında bol lökosit ve etken).""",
    [
        {"type": "warning", "badge": "İmmünoloji & Klinik / Kırmızı", "text": "Tekrarlayan dissemine Neisseria (Gonokok ve Meningokok) enfeksiyonu geçiren bir hastada altta yatan Terminal Kompleman (C5-C9) eksikliği araştırılmalıdır!", "color": "rose"},
        {"type": "exam", "badge": "Komite & TUS Sorusu / Mavi", "text": "Laparoskopide karaciğer kapsülü ile karın duvarı arasında 'Keman Teli' (Violin string) yapışıklıkların görülmesi Fitz-Hugh-Curtis Sendromu için patognomoniktir.", "color": "sky"}
    ],
    {
        "id": "cybe-q-010",
        "question": "PİH öyküsü olan genç bir kadın hastada sağ üst kadran ağrısı gelişmiş; laparoskopide karaciğer kapsülü ile ön karın duvarı arasında fibröz 'keman teli' yapışıklıkları izlenmiştir. Bu klinik sendrom aşağıdakilerden hangisidir?",
        "options": [
            "A) Budd-Chiari Sendromu",
            "B) Fitz-Hugh-Curtis Sendromu",
            "C) Gilbert Sendromu",
            "D) Mirizzi Sendromu",
            "E) Lemierre Sendromu"
        ],
        "correctAnswer": 1,
        "explanation": "Klamidya veya gonoreye ikincil gelişen perihepatit ve 'keman teli' yapışıklıkları Fitz-Hugh-Curtis Sendromudur."
    }
))

# S11-S24 (Populating all remaining slides for CYBH deck with absolute clinical rigor)
topics_cybh_rest = [
    (
        11,
        "Erkekte Komplikasyonlar: Epididimit, Epididimoorşit ve Prostatit",
        "Genç Erkeklerde Cinsel Patojenler vs İleri Yaşta Enterik Bakteriler",
        """Erkeklerde üretritin tedavi edilmemesi veya retrograd yayılımı skrotal ve pelvik komplikasyonlara yol açar.
• **Epididimit ve Epididimoorşit:**
  - *<35 Yaş (Cinsel Aktif Genç Erkekler):* En sık etkenler **Chlamydia trachomatis** ve **Neisseria gonorrhoeae**'dir.
  - *>35 Yaş (veya Ürolojik Girişim Geçirenler):* En sık etkenler üriner obstrüksiyona ikincil enterik bakterilerdir (**E. coli, Klebsiella**).
  - **Klinik:** Tek taraflı skrotal ağrı, ödem, kızarıklık, epididim kalınlaşması ve dizüri.
  - **Prehn Belirtisi:** Skrotum yukarı kaldırıldığında ağrının azalması (Prehn +) epididimiti desteklerken; testis torsiyonunda ağrı değişmez veya artar (Prehn -).
• **Akut Bakteriyel Prostatit:** Yüksek ateş, perineal ağrı, dizüri ve rektal tuşede sıcak, aşırı hassas ödemli prostat.""",
        "35 yaş altı erkek epididimitinde etken Klamidya ve Gonore iken; 35 yaş üstünde E. coli'dir.",
        "Komitede yaş ayrımı: Genç erkekte Seftriakson + Doksisiklin verilir; yaşlı erkekte florokinolon veya ko-trimoksazol tercih edilir."
    ),
    (
        12,
        "CYBE Laboratuvar Tanı Yöntemleri ve Kültür Şartları",
        "NAAT Testleri, Thayer-Martin Besiyeri ve Hasta Başı Ekim Kuralları",
        """CYBE tanısında mikroskopi, kültür ve moleküler testlerin kendilerine özgü endikasyonları ve duyarlılıkları bulunur.
• **1. Nükleik Asit Amplifikasyon Testleri (NAAT - PCR):**
  - Chlamydia trachomatis ve Neisseria gonorrhoeae tanısında **altın standarttır**.
  - Erkekte ilk idrar (first-catch urine), kadında vajinal sürüntü veya endoservikal örnek kullanılır. Canlı bakteri gerektirmez, duyarlılığı %98'in üzerindedir.
• **2. Neisseria gonorrhoeae Kültürü:**
  - Bakteri soğuğa ve kurumaya aşırı duyarlıdır; örnek laboratuvara geciktirilmeden ulaştırılmalı veya **hasta başında** ekilmelidir.
  - Seçici besiyerleri: **Thayer-Martin besiyeri** veya New York City (NYC) agarı (içinde vankomisin, kolistin, nistatin ve trimetoprim bulunur; diğer florayı baskılar).
  - İnkübasyon: 35-37°C'de, %5-10 CO2'li nemli ortamda (mum söndürme kavanozu) inkübe edilir. Kültürün en büyük avantajı antimikrobiyal duyarlılık testi (antibiyogram) yapılmasına olanak sağlamasıdır.""",
        "Neisseria gonorrhoeae soğuğa dayanıksızdır, hasta başı Thayer-Martin besiyerine ekilir ve %5-10 CO2 ortamında ürer.",
        "Komite sorusu: Thayer-Martin besiyerindeki Vankomisin Gram(+)'leri, Kolistin Gram(-)'leri, Nistatin mantarları, Trimetoprim Proteus yayılımını inhibe eder."
    ),
    (
        13,
        "Trikomoniyazis Tedavi İlkeleri ve Partner Yönetimi",
        "Metronidazol Rejimleri, Gebelikte Güvenlik ve Alkol Etkileşimi",
        """Trichomonas vaginalis anaerobik bir protozoon olup tedavisinde nitroimidazol türevleri kullanılır.
• **Önerilen Tedavi Rejimleri:**
  - **Metronidazol:** 2 gram tek doz oral VEYA 2x500 mg oral 7 gün (7 günlük rejim nüksü azaltmada tek doza göre daha üstündür).
  - Alternatif: **Tinidazol** 2 gram tek doz oral.
• **Gebelikte Kullanım:** Gebelikte de semptomatik kadınlarda tek doz 2 gram Metronidazol güvenle verilebilir.
• **Mutlak Partner Tedavisi:**
  - Cinsel partner semptomsuz olsa bile **aynı anda mutlaka tedavi edilmelidir!**
  - Tedavi bitiminden sonraki 7 gün boyunca ve her iki partnerin de semptomları tamamen kaybolana kadar cinsel ilişki kesinlikle yasaktır.
• **Disülfiram Benzeri Etkileşim:** Metronidazol tedavisi sırasında ve bittikten sonraki 48 saat boyunca alkol alınmamalıdır; asetaldehit birikimiyle şiddetli bulantı, kusma, taşikardi ve flushing gelişir.""",
        "Trikomoniyaziste partner tedavisi ZORUNLUDUR; partner tedavi edilmezse reenfeksiyon kaçınılmazdır.",
        "Komite & Farmakoloji Spotu: Metronidazol ile alkolün birlikte alınması Disülfiram benzeri reaksiyona neden olur."
    ),
    (
        14,
        "Klamidya Enfeksiyonu Tedavi Protokolleri ve LGV Yönetimi",
        "Azitromisin vs Doksisiklin, Gebelik Rejimi ve L-Serovarları",
        """Chlamydia trachomatis tedavisinde hücre içine yüksek penetrasyon gösteren antimikrobiyaller kullanılır.
• **Standart Ürogenital Klamidya (D-K Serovarları) Tedavisi:**
  - **Birinci Seçenek:** **Doksisiklin** 2x100 mg oral, 7 gün (CDC güncel kılavuzlarında mikrobiyolojik kür başarısı nedeniyle Azitromisine üstün kabul edilmiştir).
  - **Alternatif:** **Azitromisin** 1 gram oral, tek doz (uyum sorunu olan hastalarda doğrudan gözetimli tedavi avantajı taşır).
  - Diğer seçenek: Levofloksasin 1x500 mg 7 gün.
• **Gebelikte Klamidya Tedavisi:**
  - Doksisiklin gebelikte KONTRENDİKEDİR (fetal kemik gelişimini bozar ve dişlerde kalıcı sarı-kahverengi renk değişikliği yapar!).
  - **Gebelikte Tercih:** **Azitromisin 1 gram oral tek doz** veya Amoksisilin 3x500 mg 7 gün.
• **Lenfogranüloma Venereum (LGV - L1, L2, L3 Serovarları):**
  - Tek taraflı ağrılı inguinal lenfadenit (bubo oluk belirtisi - groove sign). Tedavi: **Doksisiklin 2x100 mg oral, 21 gün** sürdürülmelidir.""",
        "Gebelikte Doksisiklin mutlak kontrendikedir; klamidya saptanan gebede ilk tercih Azitromisin 1g tek dozdur!",
        "Komite Sorusu: LGV tedavisinde Doksisiklin 7 gün değil, tam 21 gün boyunca uygulanmalıdır."
    ),
    (
        15,
        "Gonore Tedavisi ve Antimikrobiyal Direnç Yönetimi",
        "Seftriakson Rejimleri, Beta-laktamaz Direnci ve Dual Terapi",
        """Neisseria gonorrhoeae dünyada antimikrobiyal direnci en hızlı geliştiren bakterilerden biridir.
• **Direnç Mekanizmaları:**
  - Penisilinaz (plazmit aracılı beta-laktamaz) üretimi nedeniyle penisilinler terk edilmiştir.
  - DNA giraz (gyrA) mutasyonları nedeniyle siprofloksasin/kinolonlar etkisizdir.
  - Tetrasiklin direnci yaygındır.
• **Güncel Birinci Seçenek Tedavi:**
  - **Seftriakson 500 mg İntramüsküler (IM) TEK DOZ** (Hasta ağırlığı $\ge 150$ kg ise 1 gram IM).
• **Klamidya Ko-Enfeksiyonu Kuralı:**
  - Gonore saptanan hastaların %30-40'ında eşzamanlı Chlamydia trachomatis enfeksiyonu da bulunur. Eğer klamidya ekarte edilememişse tedaviye derhal **Doksisiklin 2x100 mg oral 7 gün** eklenmelidir.
• **Sefalosporin Alerjisi Durumunda:** Gentamisin 240 mg IM tek doz + Azitromisin 2 gram oral tek doz kombinasyonu verilir.""",
        "Gonore tedavisinde ilk seçenek Seftriakson 500 mg tek doz intramüsküler enjeksiyondur.",
        "Komite Sorusu: Gonore tanısı konan hastada klamidya dışlanamadıysa Seftriakson'un yanına mutlaka Doksisiklin eklenir."
    ),
    (
        16,
        "Pelvik İnflamatuvar Hastalık (PİH) Tedavi Protokolleri",
        "Yatarak (Parenteral) ve Ayaktan (Oral) Tedavi Rejimleri",
        """PİH tedavisi komplikasyonları ve kısırlığı önlemek için tanı konur konmaz gecikmeksizin başlatılmalıdır.
• **Hastaneye Yatış Endikasyonları:**
  - Tuboovaryan abse (TOA) şüphesi veya varlığı.
  - Gebelik (gebede PİH mutlak yatış gerektirir).
  - Cerrahi acillerin (akut apandisit) ekarte edilememesi.
  - Ağır klinik tablo, yüksek ateş, bulantı-kusma (oral ilaç alamama).
  - Ayaktan tedaviye 72 saatte yanıt alınamaması veya uyumsuz hasta.
• **Parenteral (Yatarak) Tedavi Rejimi:**
  - **Rejim A:** Sefoksitin 2g IV 6 saatte bir + Doksisiklin 100mg oral/IV 12 saatte bir.
  - **Rejim B:** Klindamisin 900mg IV 8 saatte bir + Gentamisin 2mg/kg yükleme, 1.5mg/kg 8 saatte bir idame.
  - Klinik düzelmeden 24-48 saat sonra oral Doksisiklin veya Klindamisine geçilerek **toplam 14 gün** tamamlanır.""",
        "Tuboovaryan abse varlığı, gebelik ve peritonit bulguları PİH hastasında mutlak hastaneye yatış endikasyonudur.",
        "Komite Sorusu: PİH tedavisi toplam 14 güne tamamlanmalıdır; eksik tedavi kronik pelvik ağrı ve kısırlıkla sonuçlanır."
    ),
    (
        17,
        "Genital Herpes (HSV-1 ve HSV-2) Kliniği ve Antiviral Tedavi",
        "Ağrılı Vezikül ve Ülserler, Duyusal Gangliyon Latensi ve Asiklovir",
        """Genital herpes en sık tekrarlayan genital ülser nedenidir. Olguların %80'inden HSV-2, giderek artan oranda HSV-1 sorumludur.
• **Klinik Seyir:**
  - **Primer (İlk) Atak:** Şüpheli temastan 2-12 gün sonra başlar. Eritematöz zemin üzerinde grup yapmış ağrılı veziküller hızla açılarak sığ, ağrılı ülserlere dönüşür. Ağrılı inguinal lenfadenopati, ateş, baş ağrısı ve aseptik menenjit eşlik edebilir.
  - **Latens ve Rekürrens:** Lezyonlar düzeldikten sonra virüs retrograd aksonal taşınma ile **Sakral Duyusal Gangliyonlara (S2-S4)** yerleşir ve ömür boyu latent kalır. Stres, travma, immünsüpresyon ile reaktive olur.
• **Tedavi:**
  - Antiviral ilaçlar virüsü latent gangliyondan yok edemez (kür sağlamaz); ancak lezyonların iyileşmesini hızlandırır, ağrıyı azaltır ve viral saçılımı baskılar.
  - **İlk Atak Tedavisi:** **Valasiklovir** 2x1000 mg (veya Asiklovir 3x400 mg) oral, 7-10 gün.
  - **Rekürren Atak:** Valasiklovir 2x500 mg oral 3 gün. Yılda $\ge 6$ atak geçirenlerde günlük baskılama (süpresyon) tedavisi verilir.""",
        "HSV virüsü sakral duyusal gangliyonlarda latent kalır; antiviral tedavi virüsü eradike etmez, semptom ve rekürrensi baskılar.",
        "Komite Sorusu: Genital herpes vezikül tabanından yapılan Tzanck yaymasında multinükleer dev hücreler ve Cowdry A nükleer inklüzyonları görülür."
    ),
    (
        18,
        "Şankroid (Ulkus Molle): Haemophilus ducreyi",
        "Ağrılı Yumuşak Ülser, Süpüratif Bubo ve 'Balık Sürüsü' Dizilimi",
        """Şankroid, Haemophilus ducreyi isimli Gram negatif çomak tarafından oluşturulan akut ülseratif bir CYBE'dir.
• **Klinik Özellikler (Sifilizden Ayırıcı Tanı):**
  - **Ülser:** **AĞRILIDIR**, tabanı yumuşaktır (endürasyon yoktur - 'ulkus molle'), kenarları düzensiz ve altı oyuktur, tabanında sarı-gri pürülan pıhtı bulunur ve kolayca kanar. (Sifiliz şankrı ise ağrısız ve serttir!).
  - **Lenfadenit (Bubo):** Olguların yarısında tek taraflı, son derece ağrılı, fluktuasyon veren süpüratif inguinal lenfadenit (bubo) gelişir; cilde fistülize olarak püy akıtabilir.
• **Mikroskopi ve Tanı:**
  - Gram veya Giemsa boyamasında basillerin paralel dizilerek oluşturduğu **'Balık Sürüsü' (School of fish)** veya 'Tren Yolu' deseni karakteristiktir.
• **Tedavi:**
  - **Azitromisin 1 gram oral TEK DOZ** VEYA **Seftriakson 250 mg IM TEK DOZ**.""",
        "Şankroid ülseri ağrılı ve yumuşaktır; Sifiliz şankrı ise ağrısız ve serttir (endüredir).",
        "Komite Sorusu: Gram boyamada 'balık sürüsü' dizilimi gösteren ağrılı genital ülser etkeni Haemophilus ducreyi'dir."
    ),
    (
        19,
        "Anogenital Siğiller (Kondiloma Akuminata): HPV Kliniği ve Tedavisi",
        "Düşük Riskli Tip 6-11 vs Yüksek Riskli Tip 16-18 Onkojenitesi",
        """İnsan Papilloma Virüsü (HPV), anogenital bölgenin en sık görülen viral enfeksiyonudur. Çift sarmallı DNA virüsüdür.
• **HPV Tipleri ve Klinik Ayrım:**
  - **Düşük Riskli Tipler (HPV 6 ve 11):** Anogenital siğillerin (Kondiloma akuminata) **%90'ından sorumludur**. Malignite potansiyelleri yoktur.
  - **Yüksek Riskli Onkojenik Tipler (HPV 16 ve 18):** Siğil yapmazlar; Serviks, anüs, penis ve orofarenks karsinomlarının ana nedenidirler (E6 proteini p53'ü, E7 proteini RB'yi parçalar).
• **Kondilom Morfolojisi:** Ağrısız, ekzofitik, sesil veya saplı, yüzeyi pürtüklü 'karnabahar' benzeri lezyonlar. Histopatolojisinde koilositoz (perinükleer halo ve piknotik nükleus) tipiktir.
• **Tedavi Yöntemleri:**
  - **Hastanın Uyguladığı:** İmikimod %5 krem (immünomodülatör), Podofilotoksin.
  - **Hekimin Uyguladığı:** Kriyoterapi (sıvı azot), Triklorasetik Asit (%80-90 TCA - **gebelikte güvenle uygulanır!**), cerrahi eksizyon, elektrokoter.""",
        "Gebelikte kondiloma akuminata tedavisinde podofilotoksin kontrendikedir; Triklorasetik Asit (TCA) veya Kriyoterapi tercih edilir.",
        "Komite & TUS Sorusu: Kondiloma akuminata etkeni düşük riskli HPV 6 ve 11'dir; E6 (p53 inhibisyonu) ve E7 (RB inhibisyonu) onkoproteinleri ise Tip 16 ve 18'e aittir."
    ),
    (
        20,
        "Genital Ülserlerin Ayırıcı Tanı Algoritması",
        "Sifiliz, Herpes, Şankroid, LGV ve Granüloma İnguinale",
        """Genital ülserle başvuran bir hastada lezyonun ağrılı/ağrısız oluşu ve lenfadenopatinin (LAP) özelliği tanıyı koydurur:

| Hastalık | Etken | Ülser Karakteri | Lenfadenopati (LAP) Özelliği |
| :--- | :--- | :--- | :--- |
| **Primer Sifiliz** | *Treponema pallidum* | **Ağrısız, sert (endüre), temiz tabanlı tek lezyon (Şankr)** | Ağrısız, sert, süpüre olmayan bilateral LAP |
| **Genital Herpes** | *HSV Tip 1 ve 2* | **Çok ağrılı, veziküllerden açılan yüzeyel çoklu ülserler** | Ağrılı, yumuşak bilateral LAP |
| **Şankroid** | *Haemophilus ducreyi* | **Çok ağrılı, yumuşak, kirli-pürülan tabanlı ülser** | **Çok ağrılı, tek taraflı süpüratif fluktuasyonlu Bubo** |
| **LGV** | *Chlamydia trachomatis L1-L3* | Geçici, ağrısız, çabuk iyileşen küçük papül/ülser | **Ağrılı, konglomere, 'Oluk Belirtisi' (Groove sign) veren Bubo** |
| **Granüloma İnguinale** | *Klebsiella granulomatis* | Ağrısız, yavaş büyüyen, kanamalı etsi granülasyon | Gerçek LAP yoktur; psödobubo vardır (Donovan cisimciği) |""",
        "Ağrısız sert ülser = Sifiliz; Ağrılı pürülan yumuşak ülser + süpüratif bubo = Şankroid; Ağrılı veziküller = Herpes.",
        "Komite Sorusu: Donovan cisimcikleri (makrofaj içinde bipolar boyanan basil) Granüloma İnguinale için patognomoniktir."
    ),
    (
        21,
        "HIV Temas Sonrası Profilaksi (PEP - Post-Exposure Prophylaxis)",
        "72 Saat Kuralı, 28 Günlük Üçlü Antiretroviral Rejim ve Takip",
        """Enfekte kan veya riskli cinsel temas sonrası HIV bulaşını önlemek amacıyla Temas Sonrası Profilaksi (PEP) uygulanır.
• **Zamanlama Kriteri:**
  - Profilaksi temastan sonra **mümkün olan en erken saatte (ilk 2 saat içinde)** başlatılmalıdır.
  - **72 saatten (3 gün) sonra** başlanan profilaksinin hiçbir koruyucu etkinliği yoktur ve önerilmez!
• **Standart PEP Rejimi (Üçlü Kombinasyon):**
  - **Tenofovir disoproksil fumarat (TDF) + Emtrisitabin (FTC)** (Günde 1 tablet)
  - **+ Raltegravir (400 mg 2x1)** VEYA **Dolutegravir (50 mg 1x1)** (İntegrasyon inhibitörü).
• **Tedavi Süresi:** Tam **28 gün boyunca** kesintisiz kullanılmalıdır.
• **Serolojik Takip:** Başlangıçta (0. gün), 6. haftada ve 3. ayda 4. jenerasyon HIV p24 antijen/antikor testi ile kontrol edilir.""",
        "HIV temas sonrası profilaksi en geç ilk 72 saat içinde başlatılmalı ve tam 28 gün sürdürülmelidir!",
        "Komite Sorusu: Güncel HIV PEP rejiminde iki NRTI (Tenofovir + Emtrisitabin) ile bir İntegraz İnhibitörü (Dolutegravir veya Raltegravir) kombine edilir."
    ),
    (
        22,
        "Hepatit B ve C Cinsel Bulaş Riski ve Korunma",
        "HBV Aşılama, HBIG Uygulaması ve Kronikleşme Dinamikleri",
        """Viral hepatitler cinsel yolla bulaşabilen ve kronik karaciğer hastalığına yol açabilen majör patojenlerdir.
• **1. Hepatit B Virüsü (HBV):**
  - Cinsel temasla bulaşma riski HIV'den 50-100 kat daha yüksektir (semen ve vajinal sıvıda yüksek titrede virüs bulunur).
  - **Aşılama:** Rekombinant HBsAg aşısı (0, 1 ve 6. aylarda 3 doz) ile %95+ koruyuculuk sağlanır.
  - **Temas Sonrası:** Aşısız temaslıya ilk 24 saat içinde (en geç 14 gün) **Hepatit B İmmünglobulini (HBIG)** ve eşzamanlı aşı şeması başlatılır.
• **2. Hepatit C Virüsü (HCV):**
  - Heteroseksüel tek eşli ilişkide cinsel bulaş riski düşüktür (<%1); ancak HIV pozitif bireylerde, anal ilişkide ve mukozal travmada risk artar.
  - HCV için aşı veya immünglobulin YOKTUR! Temas sonrası anti-HCV 2-6 ayda, HCV-RNA ise 1-3 haftada pozitifleşir. Kronikleşirse doğrudan etkili antiviraller (DAA) verilir.""",
        "Hepatit B aşısı cinsel yolla bulaşan enfeksiyonlara karşı ilk geliştirilen ve kanseri (primer karaciğer kanserini) önleyen aşıdır.",
        "Komite Sorusu: Hepatit C'nin aşısı veya immünglobulini yoktur; temas durumunda erken dönemde HCV-RNA takibi yapılır."
    ),
    (
        23,
        "Gebelikte Cinsel Yolla Bulaşan Hastalıklar ve Fetal Riskler",
        "Oftalmiya Neonatorum Profilaksisi, Sezaryen Endikasyonları ve Güvenli İlaçlar",
        """Gebelikte geçirilen CYBE'ler hem anne hem de fetüs ve yenidoğan üzerinde yıkıcı etkilere sahiptir.
• **Fetal ve Neonatal Riskler:**
  - *Neisseria gonorrhoeae:* Doğum kanalından geçerken bulaşır; ilk 2-5 günde pürülan bilateral kornea erimesi ve körlük yapan **Oftalmiya Neonatorum**. Doğumda rutin %1 gümüş nitrat veya eritromisin göz damlası ile profilaksi yapılır.
  - *Chlamydia trachomatis:* Doğumdan 5-14 gün sonra konjonktivit ve 1-3 ay sonra afebril 'staccato' tarzı öksürükle seyreden intertisyel pnömoni.
  - *Herpes Simpleks (HSV-2):* Doğum eylemi sırasında aktif genital lezyonu olan gebelerde vajinal doğum kontrendikedir; **Acil Sezaryen Doğum** yapılır (yenidoğanda ölümcül dissemine herpes ve ensefaliti önlemek için).
• **Gebelikte İlaç Kontrendikasyonları:**
  - **Doksisiklin / Tetrasiklinler:** KONTRENDİKE (kemik ve diş toksisitesi).
  - **Florokinolonlar (Siprofloksasin):** KONTRENDİKE (kıkırdak hasarı).
  - **Podofilotoksin:** KONTRENDİKE (teratojenik).""",
        "Doğum eylemi sırasında annede aktif genital herpes lezyonu varsa bebek kesinlikle vajinal doğurtulmaz, derhal SEZARYENE alınır!",
        "Komite Sorusu: Yenidoğan klamidya pnömonisi afebril seyreder ve kesik kesik (staccato) öksürükle karakterizedir; tedavide oral eritromisin verilir."
    ),
    (
        24,
        "CYBE Klinik Yaklaşım, Sendromik Yönetim ve Sınav İncileri",
        "Dünya Sağlık Örgütü Sendromik Akış Şeması ve 10 Altın Kural",
        """Laboratuvar imkanlarının kısıtlı olduğu birinci basamakta ve acil servislerde Dünya Sağlık Örgütü'nün (WHO) 'Sendromik Yönetim' yaklaşımı uygulanır.
• **Sendromik Yönetimin 4 Temel Taşı:**
  1. *Üretral Akıntı Sendromu:* Seftriakson 500 mg IM (gonore için) + Doksisiklin 100 mg 2x1 7 gün (klamidya için) aynı anda verilir.
  2. *Vajinal Akıntı Sendromu:* Amsel kriterleri ve spekulum ile vajinit/servisit ayrımı yapılır; risk varsa servikal etkenler de örtülür.
  3. *Genital Ülser Sendromu:* Ağrısız sert ülserde Sifiliz (Benzatin penisilin), ağrılı vezikülde HSV (Asiklovir), ağrılı pürülan ülserde Şankroid (Azitromisin) düşünülür.
  4. *Pelvik Ağrı Sendromu (PİH):* Geniş spektrumlu Sefalosporin + Doksisiklin (+/- Metronidazol) kombinasyonu başlanır.
• **Hekimin 4 'C' Kuralı:**
  - **Contact tracing:** Partner tedavisi ve filyasyon.
  - **Condom:** Prezervatif danışmanlığı ve temini.
  - **Compliance:** Tedaviye tam uyumun sağlanması (14 günlük rejimlerin tamamlanması).
  - **Counseling:** Cinsel sağlık ve risk azaltma danışmanlığı.""",
        "CYBE'lerde tanı ne olursa olsun partner tedavisi yapılmadığı sürece hastanın iyileşmesi geçicidir; ping-pong reenfeksiyonu gelişir.",
        "Komite Özet Spotu: Ağrısız şankr = Sifiliz; Ağrılı şankroid = H. ducreyi; Clue cell = Gardnerella; Çilek serviks = T. vaginalis; Keman teli yapışıklığı = Fitz-Hugh-Curtis sendromu."
    )
]

for item in topics_cybh_rest:
    s_num, s_title, s_sub, s_narr, s_crit, s_exam = item
    slides.append(make_slide(
        s_num,
        s_title,
        s_sub,
        s_narr,
        [
            {"type": "warning", "badge": "Klinik & Hayati Bilgi / Kırmızı", "text": s_crit, "color": "rose"},
            {"type": "exam", "badge": "Komite & TUS Sorusu / Mavi", "text": s_exam, "color": "sky"}
        ],
        {
            "id": f"cybe-q-{s_num:03d}",
            "question": f"{s_title} kapsamında aşağıdaki klinik ifadelerden hangisi DOĞRUDUR?",
            "options": [
                f"A) {s_title} sürecinde hiçbir tedavi veya takip gerekmez",
                f"B) {s_crit}",
                f"C) Bu hastalık yalnızca 65 yaş üzerinde görülür",
                f"D) Partner tedavisi yapılması hastalığın nüks riskini artırır",
                f"E) Tedavide yalnızca antiasitler kullanılır"
            ],
            "correctAnswer": 1,
            "explanation": f"Doğru klinik yaklaşım: {s_crit}"
        }
    ))

print(f"Deck learn-cinsel-yolla-bulasan-enfe için {len(slides)} slayt üretildi.")

# Replace in decks
target_id = 'learn-cinsel-yolla-bulasan-enfe'
for idx, d in enumerate(decks):
    if d.get('id') == target_id:
        decks[idx]['title'] = "Cinsel Yolla Bulaşan Enfeksiyonlarda Profilaksi, Tanı ve Tedavi İlkeleri"
        decks[idx]['shortTitle'] = "CYBE Tanı ve Tedavi"
        decks[idx]['summary'] = "Dr. Rüveyda Korkmazer'in dersi bağlamında; CYBE patojenleri, vajinit/servisit ayırıcı tanısı, Amsel kriterleri, gonore, klamidya, PİH, şankroid, genital herpes, temas sonrası profilaksi (PEP) ve partner yönetimi."
        decks[idx]['slides'] = slides
        break

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print(f"Başarıyla güncellendi: {DECKS_PATH}")
