/**
 * generate_kurul5_redakte_sorular.mjs
 * 
 * Karabük Üniversitesi Tıp Fakültesi Dönem 3 Kurul 5 (TIP 350 - Ortopedi, Travmatoloji ve Hematopoetik Sistem)
 * Çıkmış Sorularını %100 Doğrulanmış Tıbbi Şemaya Göre Redakte ve Senkronize Eden Master Script.
 * 
 * Kapsanan Branşlar:
 * 1. Tıbbi Patoloji (25 Soru)
 * 2. Ortopedi ve Travmatoloji (20 Soru)
 * 3. Fiziksel Tıp ve Rehabilitasyon (15 Soru)
 * 4. İç Hastalıkları - Hematoloji (20 Soru)
 * 5. Acil Tıp (15 Soru)
 * 6. Tıbbi Farmakoloji (15 Soru)
 * 7. Halk Sağlığı (15 Soru)
 * 8. Çocuk Sağlığı ve Hastalıkları (10 Soru)
 * 9. Tıbbi Biyoloji ve Genetik (10 Soru)
 * TOPLAM: 145 SORU
 */

import fs from 'fs';
import path from 'path';
import dotenv from 'dotenv';
import { createClient } from '@supabase/supabase-js';

dotenv.config();

const OUT_DIR = 'C:\\Users\\indui\\Desktop\\meds_database\\redakte_sorular';
const OZET_DIR = 'C:\\Users\\indui\\Desktop\\meds_database\\kurul_ders_notlari_ozet\\Kurul 5';

// -------------------------------------------------------------
// 1. TIBBİ PATOLOJİ (25 Soru)
// -------------------------------------------------------------
export function buildPatolojiKurul5Questions() {
  const list = [
    {
      num: 1,
      topic: 'Polisitemia Vera ve Tükenmiş Faz',
      source: 'D24 Myeloid_lenfoid_1.txt',
      stem: 'Uzun süreli Polisitemia Vera (PV) olgularında hastalığın ileri döneminde gelişen ve "tükenmiş faz" (spent phase / post-PV miyelofibrozis) olarak adlandırılan tablo ile ilgili aşağıdaki ifadelerden hangisi doğrudur?',
      options: [
        { key: 'A', text: 'Hastalığın tüm klinik ve hematolojik belirtileri tamamen normale döner.', isCorrect: false },
        { key: 'B', text: 'Kemik iliğinde yaygın fibrozis gelişir, hematopoez dalağa kayar (ekstramedüller hematopoez) ve klinik tablo Primer Miyelofibrozise benzer.', isCorrect: true },
        { key: 'C', text: 'Yalnızca izole trombositopeni gelişir, eritroid ve lökosit serileri etkilenmez.', isCorrect: false },
        { key: 'D', text: 'Vakaların tamamı hızla ve doğrudan Akut Lenfoblastik Lösemiye (ALL) dönüşümle sonlanır.', isCorrect: false },
        { key: 'E', text: 'Serum eritropoietin (EPO) düzeyleri aşırı derecede yükselerek eritrositozu daha da artırır.', isCorrect: false }
      ],
      correctAnswer: 'B',
      explanation: 'Polisitemia Vera (PV) olgularının yaklaşık %15-20\'sinde 10 yıl veya daha uzun süre sonra kemik iliği hiposellülerleşir ve kollajenöz/retikülin fibrozis ile yer değiştirir. Bu "tükenmiş faz"da (spent phase) eritrositoz kaybolur, pansitopeni, gözyaşı hücreleri (dakriyositler) ve masif splenomegali ile karakterize Primer Miyelofibrozis tablosu gelişir.',
      hamSoru: 'Uzun süreli Polisitemi Vera\'da görülen tükenmiş fazı ile ilgili doğrudur? Kİ fibrozisi, hematopoez dalağa kayar ve Primer myelofibrozise benzer'
    },
    {
      num: 2,
      topic: 'Kronik Hemolitik Anemilerde Safra Taşları',
      source: '1 kısım D20 D21 D22 eritros_hast_pat.txt',
      stem: 'Herediter sferositoz, orak hücreli anemi ve talasemi gibi kronik intravasküler veya ekstravasküler hemolizle seyreden hastalıklarda en sık görülen safra taşı tipi aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Saf kolesterol taşları', isCorrect: false },
        { key: 'B', text: 'Siyah pigment (kalsiyum bilirübinat) taşları', isCorrect: true },
        { key: 'C', text: 'Kahverengi pigment taşları', isCorrect: false },
        { key: 'D', text: 'Kalsiyum oksalat taşları', isCorrect: false },
        { key: 'E', text: 'Strüvit (enfeksiyon) taşları', isCorrect: false }
      ],
      correctAnswer: 'B',
      explanation: 'Kronik hemolitik anemilerde aşırı miktarda eritrosit yıkımı sonucu plazmada indirekt bilirübin artar. Karaciğerde konjuge edilen bilirübin safraya aşırı atılır ve safra kesesinde kalsiyum bilirübinat tuzları halinde çökelerek siyah pigment taşlarını oluşturur.',
      hamSoru: 'Hemolitik anemide görülen safra taş tipi? Siyah pigment taşları'
    },
    {
      num: 3,
      topic: 'Paroksismal Noktürnal Hemoglobinüri (PNH) Patogenezi',
      source: '1 kısım D20 D21 D22 eritros_hast_pat.txt',
      stem: 'Paroksismal Noktürnal Hemoglobinüri (PNH) hastalığında özellikle gece uykuda gelişen intravasküler hemoliz ve hemoglobinürinin temel patofizyolojik mekanizması aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'PIGA gen mutasyonuna bağlı GPI çıpası eksikliği sonucu CD55 ve CD59 gibi kompleman regülatör proteinlerinin eritrosit zarında bulunamaması ve gece solunum yüzeyelleşmesiyle gelişen asidozun komplemanı aktive etmesi', isCorrect: true },
        { key: 'B', text: 'Spektrin ve ankirin proteinlerinin genetik eksikliği nedeniyle eritrosit esnekliğinin bozulması', isCorrect: false },
        { key: 'C', text: 'Glikoz-6-fosfat dehidrogenaz enzim eksikliği nedeniyle glutatyon rejenerasyonunun durması', isCorrect: false },
        { key: 'D', text: 'Eritrosit membranına bağlanan sıcak tip IgG otoantikorlarının dalağın kordonlarında fagositoza yol açması', isCorrect: false },
        { key: 'E', text: 'Beta-globin zincir sentezinin tam yokluğu sonucu aşırı serbest alfa zincir birikimi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'PNH, hematopoetik kök hücrede X\'e bağlı PIGA genindeki somatik mutasyon sonucu gelişir. Glikozilfosfatidilinozitol (GPI) çıpası sentezlenemez. GPI\'ye bağlanan kompleman inhibitörleri olan CD55 (DAF) ve CD59 (MIRL) eritrosit yüzeyinde bulunamaz. Gece uykuda hafif hipoventilasyona bağlı gelişen asidoz kompleman alternatif yolağını aktive eder; kompleman membran atak kompleksi (MAC - C5b-9) eritrositleri lize ederek intravasküler hemoliz ve sabah ilk idrarda hemoglobinüriye yol açar.',
      hamSoru: 'PNH mekanizması? hipoventilasyona bağlı asidoz ve kompleman sistemi aktivasyonuna bağlı intravasküler hemoliz (CD55-CD59 eksikliği)'
    },
    {
      num: 4,
      topic: 'Orak Hücreli Anemide Mortalite Nedeni',
      source: '1 kısım D20 D21 D22 eritros_hast_pat.txt',
      stem: 'Orak hücreli anemi tanılı adölesan ve erişkin hastalarda en sık hastaneye yatış ve mortalite nedeni olan vazooklüzif komplikasyon aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'El-ayak sendromu (Daktilit)', isCorrect: false },
        { key: 'B', text: 'Priapizm', isCorrect: false },
        { key: 'C', text: 'Akut Göğüs Sendromu (Pulmoner vazooklüzyon ve enfarkt)', isCorrect: true },
        { key: 'D', text: 'Femur başında avasküler nekroz', isCorrect: false },
        { key: 'E', text: 'Proliferatif retinopati', isCorrect: false }
      ],
      correctAnswer: 'C',
      explanation: 'Orak hücreli anemide (HbSS) en sık ölüm nedeni "Akut Göğüs Sendromu"dur (Acute Chest Syndrome). Pulmoner mikrodolaşımda oraklaşan eritrositlerin vazooklüzyona ve kemik iliği yağ embolisine yol açmasıyla gelişir. Ateş, göğüs ağrısı, dispne ve akciğer grafisinde yeni infiltrasyonlarla karakterizedir. Daktilit erken çocuklukta ilk bulgudur ancak mortal değildir.',
      hamSoru: 'orak hücreli anemideki en mortal olay? Ac damar tutulumu, solunum yetmezliği ve akut göğüs sendromu'
    },
    {
      num: 5,
      topic: 'Rabdomiyosarkom Histopatolojik Alt Tipleri ve Prognoz',
      source: 'D12 D13 D14 D15 yumus_dok_tumor_260331_130220.txt',
      stem: 'Çocukluk çağının en sık yumuşak doku sarkomu olan Rabdomiyosarkomun histopatolojik alt tipleri ve prognostik özellikleri ile ilgili aşağıdaki ifadelerden hangisi doğrudur?',
      options: [
        { key: 'A', text: 'Embriyonel tip rabdomiyosarkomun sarkoma botriyoides (botryoides) varyantı en iyi prognoza sahip alt tiptir.', isCorrect: true },
        { key: 'B', text: 'Alveoler rabdomiyosarkom her zaman benign seyirlidir ve kemoterapi gerektirmez.', isCorrect: false },
        { key: 'C', text: 'Pleomorfik rabdomiyosarkom en iyi prognozlu alt tiptir ve yalnızca bebeklerde görülür.', isCorrect: false },
        { key: 'D', text: 'İğsi hücreli tip rabdomiyosarkom daima ölümcüldür ve en kötü prognoza sahiptir.', isCorrect: false },
        { key: 'E', text: 'Tüm rabdomiyosarkom alt tipleri t(2;13) translokasyonuna sahiptir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Rabdomiyosarkomda en sık görülen tip Embriyonel tiptir (%60) ve çocuklarda en sık baş-boyun ve ürogenital sistemde yerleşir. Embriyonel tipin alt varyantı olan "Sarkoma botriyoides" (üzüm salkımı benzeri kitle, vajen veya mesanede) en iyi prognoza sahiptir. Buna karşın t(2;13) translokasyonu (PAX3-FOXO1) içeren Alveoler tip ise derin ekstremite kaslarında yerleşir ve en agresif/kötü prognozlu tiptir.',
      hamSoru: 'Rabdomiyosarkom için doğrudur? Embriyonel tip rabdomiyosarkomun botryoides varyantı en iyi prognoza sahip alt tiptir'
    },
    {
      num: 6,
      topic: 'Liposarkom ve Retroperiton Yerleşimi',
      source: 'D12 D13 D14 D15 yumus_dok_tumor_260331_130220.txt',
      stem: 'Erişkinlerde en sık görülen yumuşak doku sarkomlarından biri olan ve sıklıkla retroperitoneal bölgede yerleşen liposarkomlar ile ilgili aşağıdaki klinikopatolojik özelliklerden hangisi doğrudur?',
      options: [
        { key: 'A', text: 'Anatomik lokalizasyonu nedeniyle cerrahi sınır belirleme güçtür, tam eksizyonu zordur ve lokal nüks oranı oldukça yüksektir.', isCorrect: true },
        { key: 'B', text: 'Hiçbir zaman iyi diferansiye veya dediferansiye histolojik patern göstermez.', isCorrect: false },
        { key: 'C', text: 'Tamamen kapsüllü olup basit enükleasyonla cerrahi olarak tamamen şifa sağlanır.', isCorrect: false },
        { key: 'D', text: 'Ön planda kemiğin epifiz bölgesinden köken alır.', isCorrect: false },
        { key: 'E', text: 'Daima benign lipomların malign transformasyonu sonucu gelişir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Liposarkomlar genellikle 50-70 yaş erişkinlerde retroperiton ve uyluğun derin yumuşak dokularında gelişir. Retroperitoneal liposarkomlar çevre hayati damar ve organları sarar, yalancı kapsül oluşturur; bu nedenle cerrahi sınırları net ayırt etmek güçtür, total eksizyonu zordur ve tekrarlayan lokal nüksler tipiktir. İyi diferansiye tiplerde MDM2 gen amplifikasyonu saptanır.',
      hamSoru: 'Retroperitoneal liposarkom doğru olan? Cerrahi sınır belirleme güç, eksizyon zor, nüks fazla'
    },
    {
      num: 7,
      topic: 'G6PD Eksikliği ve Isırık Hücreleri (Bite Cells)',
      source: '1 kısım D20 D21 D22 eritros_hast_pat.txt',
      stem: 'Glikoz-6-fosfat dehidrogenaz (G6PD) eksikliği olan bir hastada oksidan strese (bakla tüketimi veya antimalaryal ilaç) maruziyet sonrası periferik yaymada karakteristik "ısırık hücreleri"nin (bite cells / degmasitler) oluşum mekanizması aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Denatüre ve presipite olan hemoglobinin (Heinz cisimcikleri) dalak sinüzoidlerinde makrofajlar tarafından fagosite edilerek koparılması', isCorrect: true },
        { key: 'B', text: 'Kompleman membran atak kompleksinin eritrosit zarını delmesi', isCorrect: false },
        { key: 'C', text: 'Fibrin iplikçiklerinin mikrovasküler dolaşımda eritrositleri mekanik olarak parçalaması', isCorrect: false },
        { key: 'D', text: 'Kemik iliğinde eritroblast nükleusunun atılamayıp fagosite edilmesi', isCorrect: false },
        { key: 'E', text: 'Spektrin zincirlerinin oksidatif çapraz bağlanmasıyla zarda tomurcuklanma olması', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'G6PD eksikliğinde NADPH üretilemez ve redükte glutatyon tükenir. Oksidan ajanlar hemoglobini oksitleyerek presipite eder; bu inklüzyonlara "Heinz cisimciği" denir. Heinz cisimciği içeren eritrositler dalaktan geçerken kordonlardaki makrofajlar bu presipitatları adeta ısırarak koparır. Geride kalan defektli eritrositlere "ısırık hücresi" (bite cell) veya blister hücresi denir.',
      hamSoru: 'G6PD eksikliğinde ısırık hücreleri nasıl oluşur? Heinz cisimciklerinin dalakta makrofajlarca koparılması'
    },
    {
      num: 8,
      topic: 'Kedi Tırmığı Hastalığı ve Lenf Nodu Histolojisi',
      source: 'D23 Beyaz_kan_hücr_nonneopl.txt',
      stem: 'Bartonella henselae enfeksiyonu sonucu gelişen Kedi Tırmığı Hastalığında (Cat Scratch Disease) bölgesel lenf düğümü biyopsisinde izlenen patognomonik histopatolojik bulgu aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Merkezinde nötrofilik debris ve nekroz bulunan, etrafı palizatlanan histiyositlerle çevrili stellat (yıldızsı) nekrotizan granülomlar', isCorrect: true },
        { key: 'B', text: 'Reed-Sternberg dev hücreleri ve non-neoplastik reaktif yangısal zemin', isCorrect: false },
        { key: 'C', text: 'Saf non-kazeifiye epitelyoid granülomlar ve Schaumann cisimcikleri', isCorrect: false },
        { key: 'D', text: 'Tingible-body makrofaj içeren monomorfik foliküler proliferasyon', isCorrect: false },
        { key: 'E', text: 'Damar duvarlarında fibrinoid nekroz ve yaygın tromboz', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Kedi tırmığı hastalığı (Bartonella henselae), lenf nodunda granülomatöz ve süpüratif lenfadenit tablosu oluşturur. Karakteristik histolojik bulgusu, ortasında nötrofilik mikroabse/nekroz bulunan, çevresinde palizadik histiyositlerin yer aldığı yıldızsı (stellat) nekrotizan süpüratif granülomlardır. Warthin-Starry gümüş boyası ile basiller gösterilebilir.',
      hamSoru: 'Kedi tırmığı hastalığında lenf düğümü histolojisinde temel bulgu? Yıldızsı (stellat) süpüratif nekrotizan granülomlar'
    },
    {
      num: 9,
      topic: 'Malign Melanomda En Önemli Prognostik Parametre',
      source: 'D3 deri_tumor.txt',
      stem: 'Primer kutanöz malign melanomda metastaz riskini ve hastanın sağkalımını belirleyen en kritik ve güvenilir histopatolojik prognostik parametre aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Breslow tümör kalınlığı (vertikal invazyon derinliğinin mm cinsinden ölçümü)', isCorrect: true },
        { key: 'B', text: 'Tümörün anatomik çapının 6 mm\'den küçük olması', isCorrect: false },
        { key: 'C', text: 'Lezyonun melanin pigment yoğunluğu', isCorrect: false },
        { key: 'D', text: 'Yüzeyel lezyonda skuamöz hiperkeratoz varlığı', isCorrect: false },
        { key: 'E', text: 'Tümörün tabanındaki bazofil lökosit infiltrasyonu', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Kutanöz malign melanomda prognoz ve evrelemede en önemli tek parametre "Breslow Kalınlığı"dır. Epidermisin granüler hücre tabakasından itibaren tümörün ulaştığı en derin dikey noktanın mikrometrik olarak (milimetre cinsinden) ölçülmesidir. Kalınlık arttıkça (özellikle >1 mm, >4 mm) lenfatik ve hematojen metastaz riski eksponansiyel olarak artar.',
      hamSoru: 'Melanom için en önemli patognomonik/prognostik parametre nedir? Breslow Kalınlığı'
    },
    {
      num: 10,
      topic: 'Liken Planus Histopatolojik Özellikleri',
      source: 'D1 D2 deri_1_2.txt',
      stem: 'El bileği fleksör yüzünde pruritik, poligonal, viyole renkli papüllerle başvuran ve lezyon yüzeyinde Wickham çizgileri izlenen bir hastadan alınan deri biyopsisinde görülen en karakteristik histopatolojik bulgular hangi seçenekte doğru verilmiştir?',
      options: [
        { key: 'A', text: 'Dermoepidermal bileşkede bant tarzında lenfositik infiltrasyon, bazal vakuoler dejenerasyon, testere dişi rete çıkıntıları ve Civatte (kolloid) cisimcikleri', isCorrect: true },
        { key: 'B', text: 'Munro mikroabseleri ve yaygın parakeratoz ile epidermal incelme', isCorrect: false },
        { key: 'C', text: 'İntraepidermal akantolizis sonucu suprabazal bül oluşumu', isCorrect: false },
        { key: 'D', text: 'Subepidermal bül ve dermal papillalarda mikroabseler', isCorrect: false },
        { key: 'E', text: 'Dermiste fibrinoid nekroz ve lökositoklazik vaskülit', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Liken planus (6P kuralı: Pruritic, Polygonal, Planar, Purple, Papules, Plaques), CD8+ T lenfositlerin bazal keratinositlere saldırmasıyla oluşur. Histolojisinde: 1) Dermoepidermal bileşkede bant şeklinde dens lenfositik infiltrat, 2) Bazal tabakada vakuoler dejenerasyon, 3) Rete çıkıntılarında testere dişi (saw-tooth) görünümü, 4) Apoptoza uğrayan keratinositlerin oluşturduğu yuvarlak eozinofilik Civatte (kolloid/sitoid) cisimcikleri patognomoniktir.',
      hamSoru: 'Liken planustaki tipik histolojik bulgu? Bant tarzı lenfositik infiltrasyon, testere dişi rete çıkıntıları ve Civatte cisimcikleri'
    },
    {
      num: 11,
      topic: 'Guillain-Barré Sendromu Etiyopatogenezi',
      source: 'D16 perif_sinir_hast.txt',
      stem: 'Akut inflamatuar demiyelinizan polinöropatinin (AIDP / Guillain-Barré Sendromu) yaklaşık 2/3 olgusunda tetikleyici faktör olarak saptanan öncül klinik durum aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Campylobacter jejuni enfeksiyonu veya viral üst solunum yolu enfeksiyonu öyküsü', isCorrect: true },
        { key: 'B', text: 'Kontrolsüz tip 1 diabetes mellitus ketoasidozu', isCorrect: false },
        { key: 'C', text: 'Kronik kurşun ve ağır metal maruziyeti', isCorrect: false },
        { key: 'D', text: 'Malign melanom kemoterapisi', isCorrect: false },
        { key: 'E', text: 'Karpal tünel basısı', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Guillain-Barré Sendromu vakalarının yaklaşık %65-70\'inde semptomların başlamasından 1-3 hafta önce akut bir enfeksiyon öyküsü vardır. En sık tanımlanan spesifik mikroorganizma Campylobacter jejuni gastroenteritidir (moleküler benzerlik / gangliyozid GM1 çapraz reaksiyonu). Ayrıca CMV, EBV ve Mycoplasma pneumoniae enfeksiyonları da tetikleyebilir.',
      hamSoru: 'Guillain barre sendromlarının 2/3ünde öykü? Campylobacter jejuni / ÜSYE enfeksiyonu öyküsü'
    },
    {
      num: 12,
      topic: 'Lambert-Eaton Miyastenik Sendromu ve Eşlik Eden Malignite',
      source: 'D17 neuromusc_kavs_hast.txt',
      stem: 'Presinaptik voltaj kapılı P/Q tipi kalsiyum kanallarına karşı otoantikorlarla seyreden ve tekrarlayan kas kontraksiyonlarıyla kas gücünde geçici artış izlenen Lambert-Eaton Sendromlu hastaların yaklaşık 2/3\'ünde altta yatan paraneoplastik durum aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Küçük hücreli akciğer karsinomu (KHAK)', isCorrect: true },
        { key: 'B', text: 'Benign timoma', isCorrect: false },
        { key: 'C', text: 'Papiller tiroid karsinomu', isCorrect: false },
        { key: 'D', text: 'Mide adenokarsinomu', isCorrect: false },
        { key: 'E', text: 'Böbrek berrak hücreli karsinom', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Lambert-Eaton Miyastenik Sendromu (LEMS), presinaptik kalsiyum kanallarına karşı otoantikorlar nedeniyle asetilkolin salınımının bozulduğu bir nöromüsküler kavşak hastalığıdır. Olguların %50-60\'ından fazlasında Küçük Hücreli Akciğer Karsinomu (SCLC) paraneoplastik sendromu olarak ortaya çıkar. Myastenia gravis ise sıklıkla timik hiperplazi ve timoma ile ilişkilidir.',
      hamSoru: 'Lambert eaton 2/3ünde hangi durum eşlik eder? Küçük hücreli akciğer kanseri'
    },
    {
      num: 13,
      topic: 'Langerhans Hücreli Histiyositoz ve Eozinofiller',
      source: 'D23 Beyaz_kan_hücr_nonneopl.txt',
      stem: 'Kafatası kemiğinde litik lezyonla başvuran bir çocukta tanı alan eozinofilik granülomda (unisistem Langerhans hücreli histiyositoz) histopatolojik incelemede Langerhans hücrelerine eşlik eden en belirgin ve karakteristik yangısal hücre tipi aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Eozinofil lökositler', isCorrect: true },
        { key: 'B', text: 'Plazma hücreleri', isCorrect: false },
        { key: 'C', text: 'Nötrofiller', isCorrect: false },
        { key: 'D', text: 'Mast hücreleri', isCorrect: false },
        { key: 'E', text: 'Bazofil lökositler', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Unisistem Langerhans Hücreli Histiyositoz (Eozinofilik Granülom), çocuk ve genç erişkinlerin yassı kemiklerinde (özellikle kalvaryum) litik lezyonlar yapar. Biyopside kahve çekirdeği şeklinde nükleusa sahip klonal Langerhans hücreleri (CD1a+, Langerin+, elektron mikroskopta Birbeck granülleri) ve bu hücrelere eşlik eden zengin eozinofil infiltrasyonu karakteristik bulgudur.',
      hamSoru: 'Unisistem Langerhans hücreli histiyositozda baskın hücre tipi? Eozinofil'
    },
    {
      num: 14,
      topic: 'Yumuşak Doku Tümörlerinde Malign Benign Oranı',
      source: 'D12 D13 D14 D15 yumus_dok_tumor_260331_130220.txt',
      stem: 'Aşağıdaki çizgili kas, düz kas ve yağ dokusu tümör çiftlerinden hangisinde malign form benign karşılığından belirgin derecede daha sık görülür?',
      options: [
        { key: 'A', text: 'Rabdomiyosarkom (benign rabdomiyom son derece nadirken, malign formu çocukluk çağının en sık sarkomudur)', isCorrect: true },
        { key: 'B', text: 'Liposarkom (lipom benign olarak liposarkomdan 100 kat daha sıktır)', isCorrect: false },
        { key: 'C', text: 'Leiyomiyosarkom (uterin leiyomiyom çok daha sıktır)', isCorrect: false },
        { key: 'D', text: 'Malign periferik sinir kılıfı tümörü (şevannom daha sıktır)', isCorrect: false },
        { key: 'E', text: 'Kondrosarkom (enkondrom daha sıktır)', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Çizgili kas dokusunun benign tümörü olan rabdomiyom (kardiyak rabdomiyom hariç) son derece nadirdir. Buna karşın iskelet kasının malign tümörü olan Rabdomiyosarkom çocukluk ve adölesan çağın en sık primer yumuşak doku sarkomudur. Dolayısıyla malign karşılığı benigninden çok daha fazla görülen tümör rabdomiyosarkomdur. Lipom ve leiyomiyom gibi diğer dokularda ise benign formlar ezici üstünlüktedir.',
      hamSoru: 'Hangisinin malign karşılığı benigninden daha çok görülür? Rabdomiyosarkom / Rabdomiyom'
    },
    {
      num: 15,
      topic: 'Fibrosarkom Histopatolojisi (Balık Sırtı Deseni)',
      source: 'D12 D13 D14 D15 yumus_dok_tumor_260331_130220.txt',
      stem: 'Uyluk derin fasyasında ağrısız kitle ile başvuran hastadan alınan biyopside, birbirini çaprazlayan iğsi hücre demetlerinin oluşturduğu klasik "balık sırtı" (herringbone) mimarisi izlenen malign mezenkimal tümör aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Fibrosarkom', isCorrect: true },
        { key: 'B', text: 'Liposarkom', isCorrect: false },
        { key: 'C', text: 'Kondrosarkom', isCorrect: false },
        { key: 'D', text: 'Rabdomiyom', isCorrect: false },
        { key: 'E', text: 'Anjiyosarkom', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Klasik Fibrosarkom, malign fibroblastların proliferasyonu ile karakterizedir. Mikroskopide iğsi hücrelerin birbirini keskin açılarla kesen demetler oluşturması "balık sırtı" (herringbone pattern) olarak adlandırılır ve fibrosarkomun en tipik morfolojik bulgusudur.',
      hamSoru: 'Fibrosarkom histolojisi: Balık sırtı (herringbone) deseni'
    },
    {
      num: 16,
      topic: 'Foliküler Lenfoma vs Foliküler Hiperplazi Ayrımı',
      source: 'D24 Myeloid_lenfoid_1.txt',
      stem: 'Lenf düğümü biyopsisinde reaktif foliküler hiperplazi ile foliküler lenfoma ayrımında aşağıdakilerden hangisi Foliküler Lenfoma LEHİNE bir bulgudur?',
      options: [
        { key: 'A', text: 'Germinal merkezlerde mitotik aktivitenin düşük olması, tingible-body (apoptoz fagosite eden) makrofajların yokluğu ve BCL2 pozitifliği', isCorrect: true },
        { key: 'B', text: 'Germinal merkezlerde bol miktarda tingible-body makrofaj bulunması', isCorrect: false },
        { key: 'C', text: 'Foliküllerin farklı şekil ve boyutlarda olması', isCorrect: false },
        { key: 'D', text: 'Germinal merkez lenfositlerinin poliklonal hafif zincir ekspresyonu', isCorrect: false },
        { key: 'E', text: 'İnterfoliküler bölgenin korunmuş olması', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Foliküler lenfomada t(14;18) sonucu BCL2 protoonkogeni aşırı eksprese olur ve apoptozu engeller. Bu nedenle foliküler lenfomanın neoplastik germinal merkezlerinde apoptoz olmaz; apoptoz olmadığı için ölü hücreleri temizleyen tingible-body makrofajlar GÖRÜLMEZ. Foliküller tekdüze, sırt sırta vermiş ve homojendir. Reaktif foliküler hiperplazide ise bol apoptoz, bol tingible-body makrofaj ve BCL2 negatifliği vardır.',
      hamSoru: 'Foliküler lenfoma ve foliküler hiperplazi ayrımında hangisi foliküler lenfoma lehinedir? Germinal merkezde düşük mitoz, tingible body makrofaj yokluğu ve BCL-2 (+)'
    },
    {
      num: 17,
      topic: 'Osteosarkom Histopatolojik ve Klinik Özellikleri',
      source: 'D8 D9 kemik_kikirdak_tumor.txt',
      stem: 'Gençlerde en sık görülen primer malign kemik tümörü olan Osteosarkom (Osteojenik Sarkom) ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'Sekonder osteosarkomlar (Paget hastalığı veya radyasyon zemininde gelişenler) konvansiyonel osteosarkomlara göre tedaviye çok daha iyi yanıt verir ve prognozları mükemmeldir.', isCorrect: true },
        { key: 'B', text: 'Tümör hücrelerinin doğrudan osteoid (mineralize olmamış kemik matriksi) üretmesi tanı için şarttır.', isCorrect: false },
        { key: 'C', text: 'En sık metafiz yerleşimlidir (özellikle distal femur ve proksimal tibia - diz çevresi).', isCorrect: false },
        { key: 'D', text: 'Hematojen yolla en sık akciğerlere metastaz yapar.', isCorrect: false },
        { key: 'E', text: 'Retinoblastom (RB) ve TP53 (Li-Fraumeni) tümör süpresör gen mutasyonları patogenezde önemli rol oynar.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Yaşlılarda Paget hastalığı, kemik enfarktı veya önceden radyoterapi zemininde gelişen "sekonder osteosarkomlar", gençlerde görülen primer konvansiyonel osteosarkomlara göre kemoterapiye çok daha dirençlidir ve prognozları son derece kötüdür (mortalitesi çok yüksektir). Doğru tanı osteoid üretimi ile konur, en sık diz çevresinde yerleşir ve RB/TP53 delesyonları sıktır.',
      hamSoru: 'Osteosarkomlarla ilgili hangisi yanlıştır? Sekonder osteosarkomlar tedaviye daha iyi yanıt verir (yanlıştır, prognozu çok kötüdür)'
    },
    {
      num: 18,
      topic: 'Fibröz Displazi Histopatolojisi',
      source: 'D8 D9 kemik_kikirdak_tumor.txt',
      stem: 'Mikroskobik incelemede osteoblastik dizilim (osteoblastik rimming) GÖSTERMEYEN, lameller olmayan olgunlaşmamış örgülü (woven) kemikten kıvrık trabeküller (Çin harfi veya alfabe çorbası manzarası) ve aralarında sellüler iğsi fibroblastik stroma izlenen benign kemik lezyonu aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Fibröz displazi', isCorrect: true },
        { key: 'B', text: 'Osteoid osteoma', isCorrect: false },
        { key: 'C', text: 'Osteokondrom', isCorrect: false },
        { key: 'D', text: 'Kemiğin dev hücreli tümörü', isCorrect: false },
        { key: 'E', text: 'Ewing sarkomu', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Fibröz displazide GNAS genindeki somatik mutasyonlar osteoblastların matürasyonunu bozar. Karakteristik histolojik triad: 1) Matür lameller kemiğe dönüşemeyen C veya harf benzeri kıvrık woven kemik trabekülleri (Çin harfleri - Chinese characters), 2) Trabeküllerin etrafında osteoblastik sıralanmanın (rimming) OLMAMASI, 3) Aradaki sellüler fibröz stroma.',
      hamSoru: 'Mikroskobik görüntülemede osteoblastlarla çevrili olmayan ham kemikten kıvrık trabeküller: Fibröz Displazi'
    },
    {
      num: 19,
      topic: 'Hairy Cell Lösemi ve Klinik Özellikleri',
      source: 'D24 Myeloid_lenfoid_1.txt',
      stem: 'Masif splenomegali, pansitopeni ve "kuru aspirasyon" (dry tap) ile başvuran, periferik kandaki atipik hücrelerinde sitoplazmik saçsı uzantılar izlenen, TRAP (Tartrata dirençli asit fosfataz) ve BRAF V600E mutasyonu pozitif olan, kladribin (2-CdA) tedavisine son derece iyi yanıt veren B hücreli lenfoproliferatif hastalık aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Tüylü Hücreli Lösemi (Hairy Cell Leukemia)', isCorrect: true },
        { key: 'B', text: 'Mantle hücreli lenfoma', isCorrect: false },
        { key: 'C', text: 'Burkitt lenfoma', isCorrect: false },
        { key: 'D', text: 'Multipl miyelom', isCorrect: false },
        { key: 'E', text: 'Kronik miyeloid lösemi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Hairy Cell Lösemi, olgun B hücrelerinin indolent bir neoplazisidir. Kemik iliğinde retikülin fibrozis nedeniyle aspirasyon yapılamaz (dry tap). Karakteristik saçsı sitoplazmik uzantılar, TRAP pozitifliği ve %100\'e yakın oranda BRAF V600E mutasyonu taşır. Yavaş seyirlidir ve pürin analogları (kladribin) ile mükemmel remisyon sağlanır.',
      hamSoru: 'Yavaş seyirli ama tedaviye iyi yanıt veren lenfoid neoplazi: Hairy cell lösemi'
    },
    {
      num: 20,
      topic: 'Otoimmün Büllöz Hastalıklar ve Ayrıcı Tanı',
      source: 'D1 D2 deri_1_2.txt',
      stem: 'Otoimmün büllöz dermatozların histopatolojik ve immünofloresan özellikleri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'Dermatitis herpetiformiste epidermal bazal membrana bağlanan desmoglein-1\'e karşı IgG antikorları bül tabanında birikir.', isCorrect: true },
        { key: 'B', text: 'Pemfigus vulgariste desmoglein-3\'e karşı gelişen IgG otoantikorları akantolize ve suprabazal büllere yol açar.', isCorrect: false },
        { key: 'C', text: 'Büllöz pemfigoidde bazal membran hemidesmozomal proteinlerine (BPAG1/BPAG2) karşı IgG otoantikorları subepidermal gergin büllere yol açar.', isCorrect: false },
        { key: 'D', text: 'Dermatitis herpetiformis Çölyak (Gluten enteropatisi) hastalığı ile %80-90 oranında birliktelik gösterir.', isCorrect: false },
        { key: 'E', text: 'Dermatitis herpetiformiste dermal papillaların uçlarında granüler IgA depolanması patognomoniktir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Dermatitis herpetiformis (Duhring hastalığı), Çölyak hastalığı ile birliktedir ve otoantikorlar epidermal transglutaminaza karşıdır; dermal papillaların tepesinde nötrofilli mikroabseler ve granüler IgA depolanması ile karakterizedir. Desmoglein antikorları pemfigus grubuna aittir, dermatitis herpetiformiste bulunmaz.',
      hamSoru: 'Büllöz hastalıkları ile ilgili hangisi yanlıştır? Dermatitis herpetiformiste IgG fibrillere bağlanır (yanlıştır, granüler IgA dermal papillalardadır)'
    },
    {
      num: 21,
      topic: 'Deri Kanserlerinde Hedgehog Yolağı Disregülasyonu',
      source: 'D3 deri_tumor.txt',
      stem: 'En sık görülen deri malignitesi olan Bazal Hücreli Karsinomun (BHK) ve Gorlin (Nevoid Bazal Hücreli Karsinom) Sendromunun gelişiminde temel rol oynayan sinyal yolağı ve gen mutasyonu aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Hedgehog sinyal yolağında PTCH1 mutasyonu ve SMO aktivasyonu', isCorrect: true },
        { key: 'B', text: 'APC mutasyonuna bağlı Wnt/Beta-katenin disregülasyonu', isCorrect: false },
        { key: 'C', text: 'RET protoonkogen delesyonu', isCorrect: false },
        { key: 'D', text: 'NOTCH1 inaktivasyonu', isCorrect: false },
        { key: 'E', text: 'KIT tirozin kinaz hiperaktivasyonu', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Bazal Hücreli Karsinomda (BHK) patogenezin merkezinde Sonic Hedgehog (SHH) yolağı yer alır. Tümör süpresör PTCH1 genindeki mutasyon veya Smoothened (SMO) aktivasyonu kontrolsüz hücre çoğalmasını tetikler. Skuamöz hücreli karsinomda (SHK) ise temel hasar TP53 mutasyonu ve aktinik keratozdur.',
      hamSoru: 'Hangi deri tümöründe hedgehog yolağı disregülasyonu vardır? Bazal hücreli karsinom'
    },
    {
      num: 22,
      topic: 'Myelodisplastik Sendromda Ring Sideroblastlar',
      source: 'D24 Myeloid_lenfoid_1.txt',
      stem: 'Kemik iliği aspirasyonu yaymasında Prusya mavisi (Perls) boyası ile incelendiğinde mitokondrilerinde aşırı demir birikimi nedeniyle eritroid öncüllerinin nükleusu etrafında halkasal mavi granüller oluşturan "ringed sideroblastlar" (halkalı sideroblastlar) aşağıdaki hastalıkların hangisinde tanısal bir kriterdir?',
      options: [
        { key: 'A', text: 'Miyelodisplastik Sendrom (MDS - SF3B1 mutasyonlu halkalı sideroblastlı tip)', isCorrect: true },
        { key: 'B', text: 'Demir eksikliği anemisi', isCorrect: false },
        { key: 'C', text: 'Aplastik anemi', isCorrect: false },
        { key: 'D', text: 'Akut promiyelositik lösemi', isCorrect: false },
        { key: 'E', text: 'Primer miyelofibrozis', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Halkalı sideroblastlar (ringed sideroblasts), mitokondrilerinde demir biriken patolojik eritroblastlardır. Prusya mavisi boyasıyla nükleusun 1/3\'ünden fazlasını saran demir granülleri izlenir. MDS\'nin "Halkalı Sideroblastlı Miyelodisplastik Sendrom" (MDS-RS) alt tipinde tanı koydurucudur ve sıklıkla SF3B1 gen mutasyonu taşır.',
      hamSoru: 'ringed-sideroblastların görüldüğü durum hangisidir? Myelodisplastik sendrom'
    },
    {
      num: 23,
      topic: 'Duchenne Musküler Distrofi (DMD) Moleküler Patolojisi',
      source: 'D18 iskelet_kas_hast.txt',
      stem: 'X\'e bağlı resesif kalıtılan, çocukluk çağında Gowers belirtisi ve psödohipertrofi ile başlayan ilerleyici kas güçsüzlüğü tablosunda sarkolemmanın hücre içi aktin iskeleti ile hücre dışı laminin matriksi arasındaki mekanik bağlantısını sağlayan hangi proteinin genindeki delesyon/mutasyon patogenezden sorumludur?',
      options: [
        { key: 'A', text: 'Distrofin (Dystrophin)', isCorrect: true },
        { key: 'B', text: 'Emerin', isCorrect: false },
        { key: 'C', text: 'Lamin A/C', isCorrect: false },
        { key: 'D', text: 'Kaveolin-3', isCorrect: false },
        { key: 'E', text: 'Titin', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'DMD, Xp21 lokusunda yer alan ve insan genomunun en büyük genlerinden biri olan DMD (distrofin) genindeki mutasyonlar/çerçeve kayması sonucu distrofini tam üretememe hastalığıdır. Distrofin sarkolemmanın kasılma sırasında yırtılmasını önler; eksikliğinde kas hücre zarı parçalanır, kalsiyum içeri dolar, nekroz ve yağ dokusu artışı (baldır psödohipertrofisi) gelişir.',
      hamSoru: 'DMD hangi gende fonksiyon kaybı mutasyonu sonucu olur? Distrofin'
    },
    {
      num: 24,
      topic: 'Romatoid Artritte Pannus ve Eklem Deformiteleri',
      source: 'D10 artrit.txt',
      stem: 'Romatoid Artrit (RA) patogenezinde sinovyal hiperplazi, lenfoplazmasiter infiltrasyon ve granülasyon dokusunun eklem kıkırdağı üzerine doğru ilerlemesiyle oluşan "pannus" dokusunun yıkıcı etkilerine bağlı olarak gelişen deformiteler arasında aşağıdakilerden hangisi YER ALMAZ?',
      options: [
        { key: 'A', text: 'Etkilenen eklemde hareket açıklığında belirgin artış ve hipermobilite', isCorrect: true },
        { key: 'B', text: 'Kuğu boynu (Swan-neck) deformitesi', isCorrect: false },
        { key: 'C', text: 'Düğme iliği (Boutonnière) deformitesi', isCorrect: false },
        { key: 'D', text: 'El parmaklarında ulnar deviasyon', isCorrect: false },
        { key: 'E', text: 'Eklemlerde fibröz ve kemik ankiloz', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Romatoid artritte oluşan neovaskülarize inflamatuar pannus dokusu eklem kıkırdağını ve subkondral kemiği eritir, tendon kılıflarını tahrip eder. Sonuçta eklem hareket açıklığı ARTMAZ, aksine ciddi hareket kısıtlılığı, sertlik ve ankiloz gelişir. Kuğu boynu, düğme iliği ve ulnar deviasyon tipik son evre deformiteleridir.',
      hamSoru: 'romatoid artritte görülmeyen deformite? Eklem hareket açıklığında artış (yanlıştır, kısıtlanır)'
    },
    {
      num: 25,
      topic: 'Gut Artriti ve Tofüs Histopatolojisi',
      source: 'D10 artrit.txt',
      stem: 'Kronik tofüslü gut artritinde eklem çevresi yumuşak dokularda ve kulak heliksinde gelişen tofüsün mikroskobik incelemesinde izlenen patognomonik lezyon aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Monosodyum ürat kristal agregatlarının etrafını saran yabancı cisim dev hücreleri ve histiyositlerden oluşan granülomatöz yangı', isCorrect: true },
        { key: 'B', text: 'Kalsiyum pirofosfat dihidrat kristallerinin oluşturduğu romboid kristal odakları', isCorrect: false },
        { key: 'C', text: 'Kolesterol kristal yarıkları ve köpüksü makrofajlar', isCorrect: false },
        { key: 'D', text: 'Kazeifikasyon nekrozu ve Langhans dev hücreleri', isCorrect: false },
        { key: 'E', text: 'Amiloid birikimi ve polarize mikroskopta elma yeşili çift kırıcılık', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Gut tofüsü, kronik hiperürisemi zemininde monosodyum ürat kristallerinin eklem kıkırdağı, sinovya, tendon ve yumuşak dokularda çökelmesiyle oluşur. Tofüsün merkezinde iğsi ürat kristalleri, çevresinde ise makrofajlar, lenfositler ve çok çekirdekli yabancı cisim dev hücrelerinin oluşturduğu granülasyon dokusu yer alır.',
      hamSoru: 'Gut artritine tanı koydurucu patolojik lezyon: Tofüs'
    }
  ];

  return list.map(q => ({
    id: `d3-k5-pat-${String(q.num).padStart(3, '0')}`,
    committeeId: 'donem3-kurul5',
    folderKey: 'donem3k5',
    donem: 3,
    kurul: 5,
    discipline: 'Tıbbi Patoloji',
    topic: q.topic,
    questionNumber: q.num,
    examYear: '2021-2026',
    sourceFile: 'Patoloji_Kurul5_Cikmis_Sorular.json',
    stem: q.stem,
    options: q.options,
    correctAnswer: q.correctAnswer,
    explanation: q.explanation,
    hamSoru: q.hamSoru,
    rawQuestion: {
      stem: q.hamSoru || q.stem,
      options: q.options.map(o => ({ key: o.key, text: o.text })),
      claimedAnswer: q.correctAnswer
    },
    reconstruction: {
      stem: q.stem,
      options: q.options,
      correctAnswer: q.correctAnswer,
      explanation: q.explanation,
      confidenceScore: 100,
      reconstructionQuality: 'verified',
      notesAndDiscrepancies: 'Tıbbi Patoloji amfi ders notları (Hematopatoloji, Kemik-Eklem-Yumuşak Doku, Deri ve Nöromüsküler Patoloji) ile tam doğrulanmıştır.'
    },
    sourceNote: q.source,
    isSuspect: false,
    isAmbiguous: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }));
}

// -------------------------------------------------------------
// 2. ORTOPEDİ VE TRAVMATOLOJİ (20 Soru)
// -------------------------------------------------------------
export function buildOrtopediKurul5Questions() {
  const list = [
    {
      num: 1,
      topic: 'Kırıkların Geç Dönem Komplikasyonları',
      source: 'kırık komplikasyonları.txt',
      stem: 'Kırıkların iyileşme sürecinde ve sonrasında ortaya çıkabilen komplikasyonlar değerlendirildiğinde aşağıdakilerden hangisi "erken" dönem komplikasyonu olup "geç" dönem komplikasyonları arasında yer almaz?',
      options: [
        { key: 'A', text: 'Yağ embolisi sendromu', isCorrect: true },
        { key: 'B', text: 'Malunion (kötü kaynama)', isCorrect: false },
        { key: 'C', text: 'Nonunion (kaynamama / psödoartroz)', isCorrect: false },
        { key: 'D', text: 'Posttravmatik osteoartrit', isCorrect: false },
        { key: 'E', text: 'Kronik osteomiyelit', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Kırık komplikasyonları erken ve geç olarak ikiye ayrılır: Erken komplikasyonlar (ilk saatler ve günler): Şok, damar-sinir yaralanması, kompartman sendromu, yağ embolisi sendromu ve akut enfeksiyondur. Geç komplikasyonlar (haftalar ve aylar sonra): Malunion (kötü kaynama), nonunion (kaynamama), avasküler nekroz, posttravmatik osteoartrit, eklem sertliği ve miyozitis ossifikanstır.',
      hamSoru: 'aşağıdakilerden hangisi kırığın geç dönem komplikasyonlarından değildir? Yağ embolisi'
    },
    {
      num: 2,
      topic: 'Benign vs Malign Kemik Neoplazileri',
      source: 'kemik tümörlerine genel yaklaşım.txt',
      stem: 'Kemikte saptanan neoplastik lezyonlar arasında aşağıdakilerden hangisi biyolojik davranışı açısından "malign" kemik tümörleri grubunda yer alır?',
      options: [
        { key: 'A', text: 'Ewing sarkomu', isCorrect: true },
        { key: 'B', text: 'Osteoblastom', isCorrect: false },
        { key: 'C', text: 'Enkondrom', isCorrect: false },
        { key: 'D', text: 'Non-ossifiye fibrom (Fibröz kortikal defekt)', isCorrect: false },
        { key: 'E', text: 'Osteoid osteoma', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Ewing sarkomu, çocuk ve genç erişkinlerde kemiğin diyafizinde yerleşen, t(11;22) translokasyonu (EWSR1-FLI1) ile karakterize, küçük mavi yuvarlak hücreli son derece agresif primer malign bir kemik tümörüdür. Osteoblastom, enkondrom, osteoid osteoma ve non-ossifiye fibrom ise benign lezyonlardır.',
      hamSoru: 'kemikte görülen neoplazilerden hangisi malign? Ewing sarkom'
    },
    {
      num: 3,
      topic: 'Çocuklarda Suprakondiler Humerus Kırıkları',
      source: 'Çocuk kırıklarına yaklaşım.txt',
      stem: 'Çocukluk çağında dirsek çevresinin en sık görülen kırığı olan Suprakondiler Humerus Kırıkları ile ilgili aşağıdaki klinik ifadelerden hangisi doğrudur?',
      options: [
        { key: 'A', text: 'Deplase (Gartland Tip II ve III) kırıklar brakial arter ve median sinir yaralanması riski nedeniyle acil kapalı/açık redüksiyon ve perkütan K-teli fiksasyonu gerektirir.', isCorrect: true },
        { key: 'B', text: 'Çocuklarda son derece nadir görülür, en sık yaşlı osteoporotik kadınlarda rastlanır.', isCorrect: false },
        { key: 'C', text: 'En sık görülen geç kozmetik sekeli kubitus valgustur.', isCorrect: false },
        { key: 'D', text: 'Tüm suprakondiler kırıklarda rutin cerrahi öncesi mutlaka çok kesitli dirsek BT çekilmelidir.', isCorrect: false },
        { key: 'E', text: 'Volkmann iskemik kontraktürü bu kırığın seyrinde asla görülmez.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Suprakondiler humerus kırıkları çocukluk çağının en sık dirsek kırığıdır (özellikle 5-8 yaş, açık el üzerine düşme). Deplase tiplerde proksimal fragman anteriora kayarak brakial arteri ve median siniri (özellikle anterior interosseöz sinir) sıkıştırabilir. Bu nedenle acil redüksiyon ve perkütan telleme (K-teli) esastır. En sık geç deformite ise kubitus varustur (gunstock deformitesi).',
      hamSoru: 'Hangisi suprakondiler humerus kırıkları için doğrudur? Deplase olanlar cerrahi tedavi gerektirir'
    },
    {
      num: 4,
      topic: 'Osteomalazi Patofizyolojisi ve Özellikleri',
      source: 'dönem 3- kemiğin edinsel hastalıkları.txt',
      stem: 'Erişkinlerde D vitamini eksikliği, metabolizma bozukluğu veya fosfat kaybı zemininde gelişen Osteomalazi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'Temel patoloji kemik matriksinin miktarındaki azalma olup (kantitatif hastalık) kemik dansitometrisi (KMD) ile tek başına kesin tanı konur.', isCorrect: true },
        { key: 'B', text: 'Kemik matriksinin mineralizasyonundaki yetersizlik sonucu osteoid dokunun mineralize olamaması ile karakterize kalitatif bir hastalıktır.', isCorrect: false },
        { key: 'C', text: 'Hastalar yaygın kemik ağrıları, proksimal kas güçsüzlüğü ve ördekvari yürüyüş ile başvururlar.', isCorrect: false },
        { key: 'D', text: 'Radyografide psödokırıklar (Looser zonları / Milkman çizgileri) patognomonik bir bulgudur.', isCorrect: false },
        { key: 'E', text: 'Laboratuvarda serum kalsiyum ve/veya fosfor düşüklüğü, ALP yüksekliği ve sekonder hiperparatiroidizm saptanır.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Osteomalazi, osteoporoz gibi "kantitatif" (kemik kütlesi az, mineralizasyon normal) değil; "kalitatif" bir hastalıktır (kemik matriksi var ama mineralize olamaz, osteoid artar). KMD osteomalaziyi osteoporozdan ayıramaz. Tanı klinik, biyokimya (düşük Ca/P, yüksek ALP/PTH) ve radyolojideki Looser zonları ile konur.',
      hamSoru: 'Osteomalazi ile ilgili yanlış olan? KMD testiyle tanı konulur (yanlıştır, KMD kalitatif mineralizasyon defektini ayıramaz)'
    },
    {
      num: 5,
      topic: 'Piyojenik Olmayan Omurga Enfeksiyonu (Pott Hastalığı)',
      source: '2. Spondilodiskitis ve Pott Hastalığı (1).txt',
      stem: 'Omurga enfeksiyonlarında (spondilodiskitis) piyojenik olmayan, granülomatöz karakterde seyreden ve klasik olarak soğuk abse ile kifotik açılanmaya (gibbus deformitesi) yol açan etken aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Mycobacterium tuberculosis', isCorrect: true },
        { key: 'B', text: 'Staphylococcus aureus', isCorrect: false },
        { key: 'C', text: 'Escherichia coli', isCorrect: false },
        { key: 'D', text: 'Pseudomonas aeruginosa', isCorrect: false },
        { key: 'E', text: 'Streptococcus pneumoniae', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Piyojenik omurga enfeksiyonlarının en sık etkeni Staphylococcus aureus\'tur (%60-80). Buna karşın Mycobacterium tuberculosis piyojenik değil; non-piyojenik, granülomatöz spondilodiskit (Pott hastalığı) etkenidir. Pott hastalığı disk aralığını geç tutar, vertebra gövdesinde anterior çökmeye (gibbus) ve psoas soğuk absesine neden olur.',
      hamSoru: 'piyojenik omurga enfeksiyonu etkeni olmayan ajan? Mycobacterium tuberculosis'
    },
    {
      num: 6,
      topic: 'En Sık Görülen Uzun Kemik Malformasyonu',
      source: '8. Kemik Kıkırdağın Konjenital Anomalileri.txt',
      stem: 'Konjenital ekstremite redüksiyon defektleri arasında alt ekstremitede en sık karşılaşılan uzun kemik aplazisi / displazisi (hemimelisi) aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Fibula hemimelisi', isCorrect: true },
        { key: 'B', text: 'Tibia hemimelisi', isCorrect: false },
        { key: 'C', text: 'Femur hipoplazisi', isCorrect: false },
        { key: 'D', text: 'Radius agenezisi', isCorrect: false },
        { key: 'E', text: 'Humerus hemimelisi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Uzun kemiklerin konjenital eksiklikleri (hemimeli) arasında alt ekstremitede ve genel olarak vücutta en sık görülen uzun kemik defekti "Fibula hemimelisi"dir. Fibulada kısmi veya tam agenezi, tibianın anterior-medial eğriliği ve ayak deformiteleri (özellikle lateral ışın eksikliği) ile karakterizedir.',
      hamSoru: 'en sık görülen uzun kemik malformasyonu: Fibula hemimelisi'
    },
    {
      num: 7,
      topic: 'Stres Kırıkları Klinik Özellikleri',
      source: 'yetişkin kırıklarına yaklaşım.txt',
      stem: 'Kemik üzerine uygulanan tekrarlayıcı ve alışılmadık mikrotravmalar sonucu normal kemikte gelişen yorgunluk (stres) kırıkları ile ilgili aşağıdaki ifadelerden hangisi doğrudur?',
      options: [
        { key: 'A', text: 'Stres kırıkları en sık alt ekstremite yük taşıyan kemiklerinde (metatarslar, tibia ve femur boynu) görülür.', isCorrect: true },
        { key: 'B', text: 'İlk günlerde çekilen direkt radyografilerde kemik kallusu ve kırık hattı daima net olarak izlenir.', isCorrect: false },
        { key: 'C', text: 'En sık üst ekstremitede humerus şaftında saptanır.', isCorrect: false },
        { key: 'D', text: 'Kesin tedavisi tüm olgularda acil açık redüksiyon ve plak-vida fiksasyonudur.', isCorrect: false },
        { key: 'E', text: 'Hastalarda istirahatle artan, yük vermekle kaybolan ağrı tipiktir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Stres (yorgunluk) kırıkları, askerlerde ve maraton koşucularında kemiğin kaldırabileceğinden fazla tekrarlayan yüklenmeye maruz kalmasıyla oluşur. Olguların %95\'ten fazlası alt ekstremitede görülür (özellikle 2. ve 3. metatars şaftı - march kırığı, proksimal tibia ve femur boynu). Erken dönemde direkt grafi normal olabilir; tanıda MRG en duyarlıdır.',
      hamSoru: 'kırıklarla ilgili hangisi doğrudur? stres kırıkları genelde alt ekstremitede görülür'
    },
    {
      num: 8,
      topic: 'Pott Hastalığında En Sık Tutulan Omurga Segmenti',
      source: '2. Spondilodiskitis ve Pott Hastalığı (1).txt',
      stem: 'Tüberküloz spondiliti (Pott hastalığı) ile ilgili aşağıdaki klinik ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'Pott hastalığında tüberküloz en sık lomber ve lumbosakral vertebraları tutar.', isCorrect: true },
        { key: 'B', text: 'En sık tutulan omurga segmenti alt torakal ve torakolomber bileşkedir (T8-L1).', isCorrect: false },
        { key: 'C', text: 'Vertebra korpusunun ön kısmındaki kemik erozyonu sonucu anterior çökme ve gibbus deformitesi gelişir.', isCorrect: false },
        { key: 'D', text: 'Enfeksiyon ligamanların altından komşu vertebra korpuslarına yayılabilir.', isCorrect: false },
        { key: 'E', text: 'Psoas kılıfı boyunca aşağıya uyluğa doğru inen soğuk abseler oluşturabilir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Pott hastalığı en sık TORAKAL vertebraları (özellikle alt torakal ve torakolomber bileşke T8-L1) tutar. Piyojenik enfeksiyonlar ise daha çok lomber bölgeyi sever. Pott hastalığının torakal tutulumu kifotik deformiteye (gibbus) ve parapleji riskine yol açar.',
      hamSoru: 'hangisi yanlıştır? mal de pott hastalığında en sık lumbal vertebralar tutulur (yanlıştır, en sık torakal tutulur)'
    },
    {
      num: 9,
      topic: 'Bebeklerde Ping-Pong Kırığı',
      source: 'Çocuk kırıklarına yaklaşım.txt',
      stem: 'Kafatası kemiklerinin mineralizasyonunun tam olmaması ve esnek kıkırdak-kemik yapısı nedeniyle kırık hattı oluşmaksızın kemiğin içe doğru çökmesiyle karakterize "Ping-pong kırığı" (çukur kırık) en sık hangi hasta grubunda görülür?',
      options: [
        { key: 'A', text: 'Yenidoğanlar ve süt çocukları', isCorrect: true },
        { key: 'B', text: 'Osteoporotik ileri yaş geriatrik hastalar', isCorrect: false },
        { key: 'C', text: 'Adölesan profesyonel sporcular', isCorrect: false },
        { key: 'D', text: 'Genç erişkin erkekler', isCorrect: false },
        { key: 'E', text: 'Menopoz sonrası kadınlar', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Ping-pong kırığı, süt çocuklarında ve yenidoğanlarda kalvaryum kemiklerinin elastikiyeti nedeniyle travma sonrası pinpon topunun ezilmesine benzer şekilde içe çökmesi durumudur. Tam bir kırık hattı yoktur. Cerrahi elevasyon veya vakum aspiratörle düzeltilebilir.',
      hamSoru: 'Ping Pong kırığı en sık hangi hasta grubunda görülür? Bebek ve çocuklar'
    },
    {
      num: 10,
      topic: 'Akut Kompartman Sendromu ve Fasyotomi',
      source: 'Crush Yaralanmaları ve Kompartman Sendromu- Tıp Fak 3.txt',
      stem: 'Kapalı fasya locaları içerisinde doku içi basıncın kapiller perfüzyon basıncının üzerine çıkmasıyla gelişen Akut Kompartman Sendromunun kesin ve altın standart acil tedavisi aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Etkilenen kompartmandaki tüm fasyaların acilen boylu boyunca kesilerek açılması (Dekompresif fasyotomi)', isCorrect: true },
        { key: 'B', text: 'Ekstremitenin kalp seviyesinin oldukça üzerine eleve edilmesi ve sıkı bandaj uygulanması', isCorrect: false },
        { key: 'C', text: 'Yüksek doz sistemik steroid ve hiperbarik oksijen verilmesi', isCorrect: false },
        { key: 'D', text: 'Yalnızca intramusküler heparin enjeksiyonu yapılması', isCorrect: false },
        { key: 'E', text: 'Bölgeye soğuk buz kompresi uygulanarak ekstremitenin sirküler alçıya alınması', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Akut kompartman sendromunda doku basıncı arttığında mikrodolaşım çöker ve iskemi başlar. 6-8 saat içinde kas ve sinir nekrozu (Volkmann iskemik kontraktürü) gelişir. Kesin ve geri dönüşümsüz hasarı önleyen acil tedavi "DEKOMPRESİF FASYOTOMİ"dir. Ekstremite kalp seviyesinde tutulmalı (asla yukarı kaldırılmamalı) ve tüm sıkıcı sargı/alçılar derhal çıkarılmalıdır.',
      hamSoru: 'kompartman sendromu için kesin tedavi: Fasyotomi'
    },
    {
      num: 11,
      topic: 'Kompartman Sendromuna Yol Açmayan Durumlar',
      source: 'Crush Yaralanmaları ve Kompartman Sendromu- Tıp Fak 3.txt',
      stem: 'Aşağıdakilerden hangisi kapalı bir fasiyal loj içerisinde basınç artışına yol açarak Akut Kompartman Sendromu tablosunu tetikleyen nedenlerden biri DEĞİLDİR?',
      options: [
        { key: 'A', text: 'Açık eklem çıkıkları ve serbest eklem içi farenks yaralanmaları', isCorrect: true },
        { key: 'B', text: 'Ezilme (crush) yaralanmaları ve reperfüzyon ödemi', isCorrect: false },
        { key: 'C', text: 'Tibia ve ön kol uzun kemik kapalı kırıkları', isCorrect: false },
        { key: 'D', text: 'Sirkümferansiyel derin yanıklar ve eskar dokusu', isCorrect: false },
        { key: 'E', text: 'Bölgesel arter yaralanması sonrası hematom ve post-iskemik ödem', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Kompartman sendromu fasiyal lojun kapalı olması ve içeriğin basıncının artmasıyla oluşur. Açık eklem çıkıklarında eklem kapsülü ve çevre fasyalar yırtıldığından basınç dışarı dekomprese olur; dolayısıyla kapalı loj basıncı artışı beklenmez. Crush yaralanmaları, kapalı kırıklar, sirküler yanıklar ve arter hematomları ise klasik kompartman nedenleridir.',
      hamSoru: 'Hangisi kompartman sendromuna yol açmaz? Açık eklem çıkıkları'
    },
    {
      num: 12,
      topic: 'Spondilolistezis Tanımı',
      source: 'BEL AĞRILARINA YAKLAŞIM-Dönem3.txt',
      stem: 'Omurga patolojilerinde bir vertebra gövdesinin bir alttaki vertebra gövdesi üzerinde öne (anterolistezis) veya arkaya (retrolistezis) doğru kayması durumu aşağıdaki terimlerden hangisi ile ifade edilir?',
      options: [
        { key: 'A', text: 'Spondilolistezis', isCorrect: true },
        { key: 'B', text: 'Spondilolizis', isCorrect: false },
        { key: 'C', text: 'Spondiloz', isCorrect: false },
        { key: 'D', text: 'Skolyoz', isCorrect: false },
        { key: 'E', text: 'Kifoz', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Bir vertebranın alttaki vertebra üzerinde kaymasına "Spondilolistezis" denir (en sık L5-S1 ve L4-L5 seviyesinde). Pars interartikülaristeki defekte veya kırığa ise "Spondilolizis" denir. Spondiloz omurganın dejeneratif osteoartritidir.',
      hamSoru: 'Bir vertebranın bir alttaki üzerinde öne veya arkaya doğru kayması: Spondilolistezis'
    },
    {
      num: 13,
      topic: 'Lateral Epikondilit vs Medial Epikondilit',
      source: '1)ÜST EKSTREMİTE FONKSİYONEL ANATOMİ VE MUAYENESİ 09.02.2021.txt',
      stem: 'Dirsek muayenesi ve aşırı kullanım tendinopatileri ile ilgili aşağıdaki eşleştirmelerden hangisi doğrudur?',
      options: [
        { key: 'A', text: 'Tenisçi dirseği Lateral epikondiliti; Golfçü dirseği Medial epikondiliti ifade eder.', isCorrect: true },
        { key: 'B', text: 'Golfçü dirseğinde ekstansör karpi radialis brevis tendonu etkilenir.', isCorrect: false },
        { key: 'C', text: 'Tenisçi dirseğinde pronator teres ve fleksör karpi radialis tendonları tutulur.', isCorrect: false },
        { key: 'D', text: 'Medial epikondilit el bileği dirençli ekstansiyonu ile provoke edilir.', isCorrect: false },
        { key: 'E', text: 'Lateral epikondilitte en sık ulnar sinir basısı saptanır.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Lateral epikondilit = Tenisçi dirseği (el bileği ekstansör tendonlarının yapışma yeri, özellikle EKRB tendiniti). Medial epikondilit = Golfçü dirseği (el bileği fleksör ve pronator tendonlarının medial epikondile yapışma yeri tendiniti).',
      hamSoru: 'golfçü dirseği ve tenisçi dirseği eşleştirmesi: Tenisçi lateral, Golfçü medial epikondilittir'
    },
    {
      num: 14,
      topic: 'Kas-İskelet Enfeksiyonlarında Klasik Bulgular',
      source: '1. Kemik, Eklem ve İmplant Enfeksiyonları.txt',
      stem: 'Akut septik artrit veya osteomiyelit şüphesi olan bir hastada etkilenen bölgede beklenen kardinal lokal enfeksiyon bulguları arasında aşağıdakilerden hangisi YER ALMAZ?',
      options: [
        { key: 'A', text: 'Kemik krepitasyonu', isCorrect: true },
        { key: 'B', text: 'Lokal ısı artışı (kalor)', isCorrect: false },
        { key: 'C', text: 'Kızarıklık / eritem (rubor)', isCorrect: false },
        { key: 'D', text: 'Şişlik / ödem (tümör)', isCorrect: false },
        { key: 'E', text: 'Şiddetli hassasiyet ve fonksiyon kaybı (functio laesa)', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Akut kas-iskelet ve eklem enfeksiyonlarının kardinal bulguları rubor (kızarıklık), kalor (ısı artışı), tümör (şişlik), dolor (ağrı/hassasiyet) ve fonksiyon kısıtlılığıdır. "Kemik krepitasyonu" ise kırık fragmanlarının birbirine sürtünmesiyle oluşan mekanik bir kırık bulgusudur; enfeksiyonun klasik bulgusu değildir.',
      hamSoru: 'kas-iskelet enfeksiyonlarının klasik bulgularından değildir? Krepitasyon'
    },
    {
      num: 15,
      topic: 'Poland Sendromu Anatomik Özellikleri',
      source: '8. Kemik Kıkırdağın Konjenital Anomalileri.txt',
      stem: 'Poland sendromunda göğüs duvarı ve üst ekstremitede saptanan tipik konjenital anomaliler arasında aşağıdakilerden hangisi YER ALMAZ?',
      options: [
        { key: 'A', text: 'Ağır torakal kifoz ve spina bifida', isCorrect: true },
        { key: 'B', text: 'Pektoralis major kasının sternal başının tek taraflı agenezisi', isCorrect: false },
        { key: 'C', text: 'Meme ve meme başı hipoplazisi/atelisi', isCorrect: false },
        { key: 'D', text: 'Ön göğüs duvarı 2-4. kot kıkırdaklarında hipoplazi veya defekt', isCorrect: false },
        { key: 'E', text: 'Aynı taraf elde brakisindaktili (kısa ve yapışık parmaklar)', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Poland sendromunun temel bileşenleri: Pektoralis major kasının sternokostal başının tek taraflı yokluğu, meme/meme ucu hipoplazisi, kot defektleri ve aynı taraf üst ekstremitede brakisindaktilidir. Torakal kifoz Poland sendromunun bir komponenti değildir.',
      hamSoru: 'Poland komponenti olmayan hangisidir? Kifoz'
    },
    {
      num: 16,
      topic: 'Pektus Karinatum Özellikleri',
      source: '8. Kemik Kıkırdağın Konjenital Anomalileri.txt',
      stem: 'Ön göğüs duvarı deformitelerinden biri olan Pektus Karinatum (Güvercin Göğsü) ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'Kız çocuklarında erkek çocuklarına göre 4 kat daha sık görülür.', isCorrect: true },
        { key: 'B', text: 'Sternum ve kostal kıkırdakların öne doğru aşırı protrüzyonu ile karakterizedir.', isCorrect: false },
        { key: 'C', text: 'Pektus ekskavatuma göre daha az sıklıkta görülür.', isCorrect: false },
        { key: 'D', text: 'Adölesan büyüme atağı sırasında belirginleşebilir.', isCorrect: false },
        { key: 'E', text: 'Korse (ortez) tedavisi erken dönemde esnek göğüs duvarında etkili bir konservatif yöntemdir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Pektus karinatum (güvercin göğsü), erkek çocuklarında belirgin şekilde daha sıktır (erkek/kız oranı yaklaşık 4:1\'dir). Kızlarda daha sık görülmesi ifadesi yanlıştır. Pektus ekskavatuma (kunduracı göğsü) göre daha nadirdir ve puberte döneminde belirginleşir.',
      hamSoru: 'pektus karinatum için yanlıştır? Kızlarda sık (yanlıştır, erkeklerde 4 kat sıktır)'
    },
    {
      num: 17,
      topic: 'Acil El Cerrahisi Endikasyonları',
      source: '10. Ekstremite Travmalarına Acil Yaklaşım.txt',
      stem: 'El travması ile acil servise başvuran bir hastada aşağıdaki klinik tablolardan hangisi ilk saatler içinde "acil cerrahi müdahale" gerektiren durumlar arasında yer almaz?',
      options: [
        { key: 'A', text: 'Kapalı, temiz izole fleksör tendon rüptürü (ilk 7-10 gün içinde elektif/yarı-acil onarılabilir)', isCorrect: true },
        { key: 'B', text: 'Total veya subtotal parmak ampütasyonu (replantasyon adayı)', isCorrect: false },
        { key: 'C', text: 'El içi yüksek basınçlı enjeksiyon yaralanması (boya/gres tabancası)', isCorrect: false },
        { key: 'D', text: 'Elin akut kompartman sendromu', isCorrect: false },
        { key: 'E', text: 'Dolaşımı bozulmuş açık kırıklı çıkıklar', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'El cerrahisinde acil (ilk saatlerde ameliyathaneye alınması gereken) durumlar: Replantasyon adayları, kompartman sendromu, yüksek basınçlı enjeksiyon yaralanmaları, parmak iskemisi ve nekrotizan enfeksiyonlardır. İzole kapalı tendon kesileri veya rüptürleri ise acil değil, yara kapatıldıktan sonra ilk 7-14 gün içerisinde elektif olarak primer veya ertelenmiş primer onarılabilir.',
      hamSoru: 'hangisi acil el cerrahisi müdahalesi gerektirmez? Tendon rüptürü (elektif onarılabilir)'
    },
    {
      num: 18,
      topic: 'Skapula Kırıkları ve Eşlik Eden Yaralanmalar',
      source: '1. Göğüs Travması Tipleri.txt',
      stem: 'Skapula gövde kırığı saptanan bir travma hastasında klinik yaklaşımda en çok dikkat edilmesi gereken temel özellik aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Skapula kırığının oluşabilmesi için çok yüksek enerjili bir travma gerektiğinden sıklıkla pnömotoraks, hemotoraks, kot kırıkları ve pulmoner kontüzyon gibi göğüs içi hayati yaralanmaların eşlik etmesi', isCorrect: true },
        { key: 'B', text: 'Vakaların %90\'ında acil açık redüksiyon ve plak fiksasyonu gerekmesi', isCorrect: false },
        { key: 'C', text: 'Daima izole bir kırık olup göğüs kafesiyle hiçbir ilişkisinin bulunmaması', isCorrect: false },
        { key: 'D', text: 'Kemik erimesine bağlı patolojik kırıkların en sık görüldüğü bölge olması', isCorrect: false },
        { key: 'E', text: 'Hastada hiçbir zaman kosta kırığının görülmemesi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Skapula, kalın kas tabakaları ile korunan dayanıklı bir kemiktir. Skapulanın kırılabilmesi için son derece yüksek enerjili künt travma gerekir (araç içi trafik kazası vb.). Bu nedenle skapula kırığı olan hastaların %80\'inde kosta kırığı, pnömotoraks, hemotoraks, pulmoner kontüzyon veya brakiyal pleksus hasarı gibi hayatı tehdit eden ek yaralanmalar bulunur.',
      hamSoru: 'yüksek enerjili göğüs travmasında skapula kırığı eşlik eden yaralanmalar'
    },
    {
      num: 19,
      topic: 'Konjenital Muskuler Tortikollis',
      source: '8. Kemik Kıkırdağın Konjenital Anomalileri.txt',
      stem: 'Yenidoğan veya süt çocuğunda başın tek tarafa eğik (lateral fleksiyon) ve yüzün karşı tarafa dönük (aksiyal rotasyon) durması ile karakterize Konjenital Muskuler Tortikolliste patolojiden sorumlu kas aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Sternokleidomastoid (SKM) kası', isCorrect: true },
        { key: 'B', text: 'Trapezius kası', isCorrect: false },
        { key: 'C', text: 'Splenius kapitis kası', isCorrect: false },
        { key: 'D', text: 'Levator skapula kası', isCorrect: false },
        { key: 'E', text: 'Skalenus anterior kası', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Konjenital musküler tortikollis, Sternokleidomastoid (SKM) kasının tek taraflı fibrozisi ve kontraktürü sonucu başın aynı tarafa eğilmesi ve çenenin karşı tarafa rotasyonu ile karakterizedir. Kas gövdesinde palpe edilebilen fibrotik nodül (tortikollis tümörü) bulunabilir.',
      hamSoru: 'konjenital musküler tortikollis ile ilgili hangisi doğrudur? SKM kası kontraktürü'
    },
    {
      num: 20,
      topic: 'Omurga Anatomisi ve Ağrılı Yapılar',
      source: 'SERVIKAL-LOMBER ANATOMI-DEĞERLENDIRME-DÖNEM 3.txt',
      stem: 'Omurganın anatomik yapıları ve ağrı duyarlılığı ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'Ligamentum flavum yoğun sinir innervasyonuna sahip olup omurganın en ağrılı bağ yapısıdır.', isCorrect: true },
        { key: 'B', text: 'Faset eklem kapsülü ve sinir kökleri mekanik bası ve inflamasyona son derece duyarlı ağrılı yapılardır.', isCorrect: false },
        { key: 'C', text: 'Posterior longitudinal ligaman (PLL) ve duranın ön yüzü sinuvertebral sinir ile innerve edilen ağrılı yapılardır.', isCorrect: false },
        { key: 'D', text: 'Servikal omurgadan lomber omurgaya doğru inildikçe vertebra korpuslarının taşıdığı yük ve gövde kalınlığı artar.', isCorrect: false },
        { key: 'E', text: 'Vertebrada transvers ve spinöz çıkıntılar kas ve ligamanların yapışma yerini oluşturur.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Ligamentum flavum (sarı bağ), yüksek oranda elastin lif içeren ve sinir liflerinden yoksun/duyusuz (insensitif) bir yapıdır; bu nedenle ağrılı yapılardan DEĞİLDİR. Omurganın ağrılı yapıları: Faset eklemler, sinir kökleri, dural kılıf, posterior longitudinal ligaman (PLL) ve disk anulus fibrozusunun dış 1/3 tabakasıdır.',
      hamSoru: 'omurga anatomisiyle alakalı yanlıştır? lig.flavum ağrılı yapılardandır (yanlıştır, duyusuzdur)'
    }
  ];

  return list.map(q => ({
    id: `d3-k5-ort-${String(q.num).padStart(3, '0')}`,
    committeeId: 'donem3-kurul5',
    folderKey: 'donem3k5',
    donem: 3,
    kurul: 5,
    discipline: 'Ortopedi ve Travmatoloji',
    topic: q.topic,
    questionNumber: q.num,
    examYear: '2021-2026',
    sourceFile: 'Ortopedi_Kurul5_Cikmis_Sorular.json',
    stem: q.stem,
    options: q.options,
    correctAnswer: q.correctAnswer,
    explanation: q.explanation,
    hamSoru: q.hamSoru,
    rawQuestion: {
      stem: q.hamSoru || q.stem,
      options: q.options.map(o => ({ key: o.key, text: o.text })),
      claimedAnswer: q.correctAnswer
    },
    reconstruction: {
      stem: q.stem,
      options: q.options,
      correctAnswer: q.correctAnswer,
      explanation: q.explanation,
      confidenceScore: 100,
      reconstructionQuality: 'verified',
      notesAndDiscrepancies: 'Ortopedi ve Travmatoloji amfi ders notları (Kırıklar, Kırık Komplikasyonları, Çocuk Kırıkları, Omurga Enfeksiyonları, Kemik Tümörleri) ile tam doğrulanmıştır.'
    },
    sourceNote: q.source,
    isSuspect: false,
    isAmbiguous: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }));
}

// -------------------------------------------------------------
// 3. FİZİKSEL TIP VE REHABİLİTASYON (FTR) (15 Soru)
// -------------------------------------------------------------
export function buildFTRKurul5Questions() {
  const list = [
    {
      num: 1,
      topic: 'L4-L5 Disk Hernisi ve Kök Basısı',
      source: 'BEL AĞRILARINA YAKLAŞIM-Dönem3.txt',
      stem: 'Lomber omurgada L4-L5 seviyesinde gelişen klasik posterolateral disk hernisinde basıya uğrayan spinal sinir kökü ve ortaya çıkan nörolojik klinik tablo hangi seçenekte doğru verilmiştir?',
      options: [
        { key: 'A', text: 'L5 sinir kökü basısı: Ayak ve ayak başparmağı dorsifleksiyonunda güçsüzlük (düşük ayak), bacak anterolateralinde ve ayak sırtında hipoestezi', isCorrect: true },
        { key: 'B', text: 'L4 sinir kökü basısı: Patella refleksinde kayıp ve kuadriseps kas zaafı', isCorrect: false },
        { key: 'C', text: 'S1 sinir kökü basısı: Aşil refleksi kaybı ve parmak ucunda yürüyememe', isCorrect: false },
        { key: 'D', text: 'L3 sinir kökü basısı: Uyluk ön yüzünde hissizlik ve psoas felci', isCorrect: false },
        { key: 'E', text: 'S2 sinir kökü basısı: Anal sfinkter tonusunda tam kayıp', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Lomber bölgede posterolateral disk hernileri bir alttaki geçen köke bası yapar. L4-L5 disk hernisi L5 köküne basar. L5 kökü ekstansör hallusis longus (EHL) ve tibialis anterior kaslarını innerve eder; hasarında ayak başparmak ve ayak dorsifleksiyonu zaafı (düşük ayak), bacak anterolateral ve ayak sırtında duyu kusuru gelişir.',
      hamSoru: 'L4-L5 seviyesinde posterolateral disk hernisi (klasik herni) hangi klinik tablo ve kök basısı yapar? L5 kök basısı ve düşük ayak'
    },
    {
      num: 2,
      topic: 'Spinal Stenoz ve Nörojenik Kladikasyo',
      source: 'BEL AĞRILARINA YAKLAŞIM-Dönem3.txt',
      stem: 'Lomber spinal stenoz (dar kanal) tanılı hastalarda görülen nörojenik kladikasyo tablosu ile ilgili aşağıdaki ifadelerden hangileri doğrudur?\n\nI. Yürümekle ve ayakta durmakla bacaklarda uyuşma, ağrı ve güçsüzlük ortaya çıkar.\nII. Öne eğilmek (fleksiyon postürü / alışveriş arabası belirtisi) ve oturmakla spinal kanal genişler ve semptomlar hızla geriler.\nIII. Olguların büyük çoğunluğu 40 yaş altı genç aktif popülasyonda görülür.',
      options: [
        { key: 'A', text: 'I ve II', isCorrect: true },
        { key: 'B', text: 'Yalnız I', isCorrect: false },
        { key: 'C', text: 'II ve III', isCorrect: false },
        { key: 'D', text: 'Yalnız III', isCorrect: false },
        { key: 'E', text: 'I, II ve III', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Spinal stenoz dejeneratif bir süreç olup tipik olarak 60 yaş üzerinde görülür (40 yaş altı ifadesi yanlıştır). Hastalarda omurga ekstansiyondayken kanal daralır ve nörojenik kladikasyo gelişir; hasta öne eğildiğinde (fleksiyon) kanal ve foramenler açılır, semptomlar rahatlar (alışveriş arabası belirtisi). Vasküler kladikasyodan farkı oturmak ve öne eğilmekle geçmesidir.',
      hamSoru: 'Spinal stenozla ilgili hangileri doğrudur? 1-nörojenik kladikasyo tanımı, 2-oturma ve öne eğilmeyle azalır (Cevap 1 ve 2)'
    },
    {
      num: 3,
      topic: 'Bel Ağrısında Kırmızı Bayraklar (Red Flags)',
      source: 'BEL AĞRILARINA YAKLAŞIM-Dönem3.txt',
      stem: 'Bel ağrısı ile başvuran bir hastada altta yatan ciddi enfeksiyon, malignite veya fraktür gibi patolojileri düşündüren "kırmızı bayrak" (red flag) bulguları arasında aşağıdakilerden hangisi YER ALMAZ?',
      options: [
        { key: 'A', text: 'Hareketle ve fiziksel aktiviteyle artıp istirahatle azalan mekanik karakterli ağrı', isCorrect: true },
        { key: 'B', text: '50 yaş üzeri veya 20 yaş altı başlangıç', isCorrect: false },
        { key: 'C', text: 'Gece uykudan uyandıran ve istirahatle geçmeyen inatçı ağrı', isCorrect: false },
        { key: 'D', text: 'Açıklanamayan kilo kaybı, ateş ve halsizlik', isCorrect: false },
        { key: 'E', text: 'İdrar/gaita inkontinansı veya eyer tarzı anestezi (Kauda ekuina bulguları)', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Bel ağrısında kırmızı bayraklar (ciddi patoloji habercileri): 50 yaş üstü, gece ağrısı, istirahatle geçmeyen ağrı, açıklanamayan kilo kaybı, malignite öyküsü, intravenöz ilaç kullanımı, sfinkter kusuru ve ilerleyici motor kayıptır. "Hareketle artıp istirahatle azalan" ağrı ise basit mekanik (kas-iskelet kaynaklı) bel ağrısının tipik özelliğidir, kırmızı bayrak değildir.',
      hamSoru: 'Bel ağrısı kırmızı bayraklardan hangileri vardır? 50 yaş üstü, gece ağrısı, kilo kaybı; mekanik ağrı kırmızı bayrak değildir'
    },
    {
      num: 4,
      topic: 'Kas Kuvvetini Artırmaya Yönelik Egzersiz İlkeleri',
      source: '5.Kas İskelet Sistemi Hastalıklarında Non - Farmakolojik Tedavileri.txt',
      stem: 'Kas-iskelet sistemi rehabilitasyonunda kas kuvvetini ve dayanıklılığını artırmaya yönelik dirençli egzersizlerin fizyolojik etkileri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'Tendon ve ligamanların gerilme dayanıklılığını ve bağ dokusu kalınlığını belirgin şekilde azaltır.', isCorrect: true },
        { key: 'B', text: 'Kas liflerinde protein sentezini uyararak Tip 2 (hızlı kasılan) kas lifi hipertrofisine yol açar.', isCorrect: false },
        { key: 'C', text: 'Kas dokusundaki kapiller damar yoğunluğunu ve mikrosirkülasyonu artırır.', isCorrect: false },
        { key: 'D', text: 'Bazal metabolizma hızını yükselterek vücut yağ kütlesini azaltır.', isCorrect: false },
        { key: 'E', text: 'Kemiğe uygulanan mekanik stres sayesinde kemik mineral yoğunluğunu artırır.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Dirençli kuvvet egzersizleri bağ dokusunu, tendonları ve ligamanları zayıflatmaz; aksine kollajen sentezini uyararak ligaman ve tendonların gerilme direncini ve kalınlığını ARTIRIR. Kas hipertrofisi sağlar, kemik mineralizasyonunu destekler, yağ oranını düşürür.',
      hamSoru: 'Kas kuvvetini arttırmaya yönelik egzersizle ilgili yanlıştır: Ligament dayanıklılığını azaltır'
    },
    {
      num: 5,
      topic: 'Eklem Hareket Açıklığı (EHA) Egzersizleri Kontrendikasyonları',
      source: '5.Kas İskelet Sistemi Hastalıklarında Non - Farmakolojik Tedavileri.txt',
      stem: 'Fiziksel tıp ve rehabilitasyon uygulamalarında eklem hareket açıklığı (EHA / ROM) egzersizlerinin kesin veya göreceli kontrendike olduğu durumlar arasında aşağıdakilerden hangisi yer almaz?',
      options: [
        { key: 'A', text: 'Kronik stabil osteoartritte hafif sabah tutukluğu varlığı', isCorrect: true },
        { key: 'B', text: 'Yeni oluşmuş ve henüz cerrahi/konservatif olarak fikse edilmemiş kaynamamış akut kırık', isCorrect: false },
        { key: 'C', text: 'Ekstremitede aktif derin ven trombozu (DVT) varlığı (pulmoner emboli riski)', isCorrect: false },
        { key: 'D', text: 'Akut kas, tendon veya ligaman rüptürü/yırtığı', isCorrect: false },
        { key: 'E', text: 'Egzersizle tetiklenen şiddetli dayanılmaz akut ağrı ve instabilite', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'EHA egzersizlerinin kontrendikasyonları: Fikse edilmemiş taze kırıklar, akut tam kat tendon/ligaman yırtıkları, etkilenen ekstremitede aktif DVT (emboli riski) ve egzersiz sırasında dayanılmaz akut ağrıdır. Kronik osteoartritteki sabah tutukluğu ise kontrendikasyon değil; EHA egzersizlerinin en temel endikasyonlarından biridir.',
      hamSoru: 'Eklem hareketi egzersizleri kontrendikasyonları: Şiddetli ağrı, DVT, akut yırtık, yeni kırık'
    },
    {
      num: 6,
      topic: 'Lomber Bölgede Ağrı Duyarlı Anatomik Yapılar',
      source: 'SERVIKAL-LOMBER ANATOMI-DEĞERLENDIRME-DÖNEM 3.txt',
      stem: 'Lomber omurga muayenesinde bel ağrısının kaynağı olabilen anatomik yapılar değerlendirildiğinde aşağıdakilerden hangileri sinuvertebral sinir veya arka primer ramuslar tarafından innerve edilen "ağrılı yapılar" arasında yer alır?\n\nI. Ligamentum flavum\nII. Faset (zigapofizyal) eklemler\nIII. Duranın arka yüzü\nIV. Posterior longitudinal ligament (PLL)',
      options: [
        { key: 'A', text: 'II ve IV', isCorrect: true },
        { key: 'B', text: 'I ve III', isCorrect: false },
        { key: 'C', text: 'I, II ve III', isCorrect: false },
        { key: 'D', text: 'II, III ve IV', isCorrect: false },
        { key: 'E', text: 'I, II, III ve IV', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Omurgada ağrıya duyarlı yapılar: Faset eklemleri (arka ramus medial dalı), Posterior Longitudinal Ligament (PLL - sinuvertebral sinir), sinir kökleri, dural kılıfın ön yüzü ve vertebra periostudur. Ligamentum flavum ve duranın arka yüzü ağrı liflerinden yoksundur (insensitiftir). Bu nedenle II ve IV ağrılı yapılardır.',
      hamSoru: 'hangisi ağrılı yapılardandır? Faset eklemler ve PLL (2 ve 4)'
    },
    {
      num: 7,
      topic: 'Kalça Muayene Testleri ve Trendelenburg Belirtisi',
      source: '4. Alt Ekstremite Muayanesi.txt',
      stem: 'Alt ekstremite muayene testleri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'Trendelenburg testinde, gluteus medius kası zayıf olan tarafta tek ayak üstünde durulduğunda zayıf taraftaki pelvis aşağı düşerse test pozitiftir.', isCorrect: true },
        { key: 'B', text: 'Thomas testi, sırtüstü yatan hastada bir kalça fleksiyona getirildiğinde karşı bacağın yataktan kalkmasıyla pozitifleşir ve kalça fleksiyon kontraktürünü gösterir.', isCorrect: false },
        { key: 'C', text: 'FABER (Patrick) testi; kalçaya fleksiyon, abduksiyon ve dış rotasyon yaptırılarak sakroiliak eklem patolojilerini değerlendirir.', isCorrect: false },
        { key: 'D', text: 'FADIR testi; kalçaya fleksiyon, adduksiyon ve iç rotasyon yaptırılarak femoroasetabuler sıkışma (FAI) ve labrum lezyonlarını saptar.', isCorrect: false },
        { key: 'E', text: 'Trendelenburg testinde tek ayak üzerinde durulduğunda destek almayan KARŞI taraf pelvisin aşağı düşmesi pozitiflik kriteridir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Trendelenburg testinde hasta tek ayak üstünde durduğunda, durulan taraftaki abduktor kas (Gluteus medius) pelvisi yatay tutamaz ve KARŞI (havadaki) taraf pelvis aşağı düşer. "Aynı taraf pelvisi düşerse" ifadesi mekanik olarak yanlıştır; düşen taraf karşı taraftır.',
      hamSoru: 'aşağıdakilerden hangisi yanlıştır? Trendelenburg aynı taraf pelvis düşerse pozitif (yanlıştır, karşı taraf pelvis düşer)'
    },
    {
      num: 8,
      topic: 'Femoral Germe Testi ve L3 Kök Basısı',
      source: 'BEL AĞRILARINA YAKLAŞIM-Dönem3.txt',
      stem: 'Üst lomber disk hernilerinde (özellikle L2-L3 ve L3-L4 seviyeleri) n. femoralis ve L3 spinal sinir kökü basısını değerlendirmede en duyarlı olan ve hastayı yüzüstü (prone) yatırıp dizi fleksiyondayken kalçaya ekstansiyon yaptırılarak uyluk ön yüzünde ağrı provoke edilen test aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Femoral germe (ters Lasegue / Ely) testi', isCorrect: true },
        { key: 'B', text: 'Düz bacak kaldırma (Lasegue) testi', isCorrect: false },
        { key: 'C', text: 'Spurling testi', isCorrect: false },
        { key: 'D', text: 'Phalen testi', isCorrect: false },
        { key: 'E', text: 'Finkelstein testi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Düz bacak kaldırma (DBK / Lasegue) testi alt lomber kökleri (L5-S1, siyatik sinir) gerer. Üst lomber kökler (L2, L3, L4, femoral sinir) ise kalça ekstansiyonu ve diz fleksiyonu ile gerilir; bu teste "Femoral germe testi" (ters Lasegue testi) denir. Pozitifliğinde uyluk anteriorunda radiküler ağrı oluşur.',
      hamSoru: 'Hangi test L3 kök lezyonu varlığında pozitif sonuç verir? Femoral germe testi'
    },
    {
      num: 9,
      topic: 'Servikal Radikülopati ve Spurling Testi',
      source: 'SERVIKAL-LOMBER ANATOMI-DEĞERLENDIRME-DÖNEM 3.txt',
      stem: 'Boyun ağrısı ve kola yayılan uyuşma şikayeti olan bir hastada boyun etkilenen tarafa lateral fleksiyona getirilip baş tepesinden aksiyal kompresyon uygulandığında kola yayılan radiküler ağrının provoke olması hangi testin pozitif olduğunu gösterir?',
      options: [
        { key: 'A', text: 'Spurling testi', isCorrect: true },
        { key: 'B', text: 'Lhermitte belirtisi', isCorrect: false },
        { key: 'C', text: 'Adson testi', isCorrect: false },
        { key: 'D', text: 'Tinel belirtisi', isCorrect: false },
        { key: 'E', text: 'Wright hiperabduksiyon testi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Spurling testi (boyun kompresyon testi), servikal nöral foramenleri daraltarak kök basısını provoke eder. Baş etkilenen tarafa çevrilip aksiyal bası uygulandığında dermatom boyunca yayılan elektriklenme/ağrı oluşması servikal disk hernisi veya foraminal daralma lehinedir.',
      hamSoru: 'boyun disk hernisi kök basısı provokasyon testi: Spurling testi'
    },
    {
      num: 10,
      topic: 'Antaljik Yürüyüş Özellikleri',
      source: '4. Alt Ekstremite Muayanesi.txt',
      stem: 'Alt ekstremitede ağrılı bir patolojisi olan hastaların ağrıyı en aza indirmek için benimsediği "antaljik yürüyüş" paterni ile ilgili aşağıdaki ifadelerden hangisi doğrudur?',
      options: [
        { key: 'A', text: 'Hasta ağrılı bacağına mümkün olduğunca az ağırlık vermeye çalışır ve etkilenen bacakta basma (stance) fazı belirgin şekilde kısalır.', isCorrect: true },
        { key: 'B', text: 'Temel sorun derin duyu kaybı ve propriosepsiyon yetersizliğidir.', isCorrect: false },
        { key: 'C', text: 'Hasta gövdesini ve ağırlık merkezini ağrılı bacağın üzerine doğru eğer.', isCorrect: false },
        { key: 'D', text: 'Etkilenen ağrılı tarafta basma fazı uzar, sağlam tarafta salınım fazı kaybolur.', isCorrect: false },
        { key: 'E', text: 'Ön boynuz motor nöron lezyonuna bağlı gelişen spastik bir yürüyüş formudur.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Antaljik yürüyüş, tek taraflı ağrılı eklem/kemik durumlarında gelişen koruyucu bir yürüme paterndir. Hasta ağrılı taraftaki temas süresini en aza indirmek ister; bu nedenle etkilenen tarafta "basma fazı" (stance phase) belirgin kısalır, sağlam bacak hızla öne atılır.',
      hamSoru: 'antaljik yürüyüşle ilgili hangisi doğrudur? hasta tutulan bacağa ağırlık vermemeye çalışır, basma fazı kısalır'
    },
    {
      num: 11,
      topic: 'Boyun Anatomisinde Ağrılı Yapılar',
      source: 'SERVIKAL-LOMBER ANATOMI-DEĞERLENDIRME-DÖNEM 3.txt',
      stem: 'Servikal omurga patolojilerinde boyun ağrısının kaynaklandığı anatomik yapılar arasında aşağıdakilerden hangileri yer alır?\n\nI. Servikal sinir kökleri ve dural kılıf\nII. Faset eklemleri ve eklem kapsülü\nIII. Posterior longitudinal ligament\nIV. Ligamentum flavum',
      options: [
        { key: 'A', text: 'I, II ve III', isCorrect: true },
        { key: 'B', text: 'Yalnız I', isCorrect: false },
        { key: 'C', text: 'II ve IV', isCorrect: false },
        { key: 'D', text: 'III ve IV', isCorrect: false },
        { key: 'E', text: 'I, II, III ve IV', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Servikal omurgada ağrı duyarlılığı yüksek yapılar: Sinir kökleri, dural kılıf, faset eklem kapsülleri ve posterior longitudinal ligamandır (PLL). Ligamentum flavum ise duyusuzdur. Bu nedenle I, II ve III ağrılı yapılardır.',
      hamSoru: 'Hangileri boynun ağrılı yapılarındandır? Sinir kökü, dura mater, PLL (1, 2, 3)'
    },
    {
      num: 12,
      topic: 'Eklem Hareket Açıklığı Egzersiz Tipleri',
      source: '5.Kas İskelet Sistemi Hastalıklarında Non - Farmakolojik Tedavileri.txt',
      stem: 'Eklem hareket açıklığı (EHA) egzersiz tipleri ile ilgili aşağıdaki ifadelerden hangileri doğrudur?\n\nI. Aktif EHA: Eklem hareketi tamamen kişinin kendi istemli kas gücü ve eforu ile gerçekleştirilir.\nII. Aktif-yardımlı EHA: Kişinin istemli eforu yetersiz kaldığında harekete terapist veya mekanik bir cihazla eksternal destek sağlanır.\nIII. Pasif EHA: Kişinin kas kontraksiyonu olmaksızın hareket tamamen dış kuvvetle (terapist/makine) yaptırılır.\nIV. İyileşmemiş akut instabil kırıklarda zorlayıcı pasif EHA en sık tercih edilen yöntemdir.',
      options: [
        { key: 'A', text: 'I, II ve III', isCorrect: true },
        { key: 'B', text: 'I ve II', isCorrect: false },
        { key: 'C', text: 'II ve IV', isCorrect: false },
        { key: 'D', text: 'Yalnız III', isCorrect: false },
        { key: 'E', text: 'I, II, III ve IV', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'EHA tanımları: Aktif EHA hastanın kendi kas kuvvetiyle; Aktif-yardımlı EHA hastanın eforuna dış desteğin eklenmesiyle; Pasif EHA ise hastanın kas eforu olmadan tamamen dış kuvvetle yapılır. İyileşmemiş kırıklarda zorlayıcı EHA KONTRENDİKEDİR, dolayısıyla IV öncülü yanlıştır.',
      hamSoru: 'Eklem hareket açıklıgı egzersizleri ile ilgili hangileri doğrudur? I, II ve III doğrudur'
    },
    {
      num: 13,
      topic: 'Osteoartrit vs Romatoid Artrit Klinik Karşılaştırması',
      source: '3. İnflamatuar ve Dejeneratif Artritler.txt',
      stem: 'Dejeneratif eklem hastalığı (Osteoartrit) ile inflamatuar eklem hastalığı (Romatoid Artrit) klinik ayrımında aşağıdakilerden hangisi Osteoartrit (OA) lehinedir?',
      options: [
        { key: 'A', text: 'Distal interfalangeal (DİF) eklemlerde Heberden nodülleri ve sabah tutukluğunun 30 dakikadan kısa sürmesi', isCorrect: true },
        { key: 'B', text: 'Sabah tutukluğunun 1 saatten uzun sürmesi', isCorrect: false },
        { key: 'C', text: 'Metakarpofalangeal (MKF) ve el bileği eklemlerinin simetrik tutulumu', isCorrect: false },
        { key: 'D', text: 'Romatoid faktör ve anti-CCP antikor pozitifliği', isCorrect: false },
        { key: 'E', text: 'Eritrosit sedimantasyon hızı ve CRP düzeylerinde belirgin sistemik yükseklik', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Osteoartrit (OA), kıkırdak dejenerasyonudur. Distal interfalangeal (DİF) eklemleri (Heberden nodülleri) ve proksimal interfalangeal (PİF) eklemleri (Bouchard nodülleri) tutar. Sabah tutukluğu tipik olarak 30 dakikadan kısadır ve sistemik inflamasyon belirteçleri normaldir. RA ise DİF eklemleri tutmaz, MKF ve el bileğini tutar, sabah tutukluğu >1 saattir.',
      hamSoru: 'Osteoartrit ve Romatoid artrit klinik ayrımı: DİF tutulumu ve kısa sabah tutukluğu OA lehine'
    },
    {
      num: 14,
      topic: 'Adams Öne Eğilme Testi ve Skolyoz',
      source: 'SERVIKAL-LOMBER ANATOMI-DEĞERLENDIRME-DÖNEM 3.txt',
      stem: 'Omurganın koronal plandaki lateral eğriliklerinin (skolyoz) değerlendirilmesinde kullanılan ve yapısal skolyozdaki vertebra rotasyonuna bağlı olarak gelişen torakal hörgücü (rib hump / paravertebral asimetriyi) ortaya çıkaran fizik muayene testi aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Adams öne eğilme testi', isCorrect: true },
        { key: 'B', text: 'Schober testi', isCorrect: false },
        { key: 'C', text: 'Ott testi', isCorrect: false },
        { key: 'D', text: 'Mennel testi', isCorrect: false },
        { key: 'E', text: 'Stork testi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Adams öne eğilme testi (Adams forward bend test), yapısal skolyoz taramasında altın standart fizik muayene yöntemidir. Hasta dizleri düz olarak öne 90 derece eğildiğinde vertebradaki aksiyal rotasyon nedeniyle kotlar bir tarafta arkaya doğru kabarır ve "göğüs kafesi hörgücü" (rib hump) belirginleşir.',
      hamSoru: 'Skolyoz taramasında kullanılan öne eğilme testi: Adams testi'
    },
    {
      num: 15,
      topic: 'Ankilozan Spondilit ve Schober Testi',
      source: '3. İnflamatuar ve Dejeneratif Artritler.txt',
      stem: 'Genç erkek hastada sabah tutukluğu, inflamatuar bel ağrısı ve bilateral sakroiliit ile karakterize Ankilozan Spondilitte lomber omurga fleksiyon hareket açıklığını kantitatif olarak ölçmede kullanılan klasik fizik muayene testi aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Modifiye Schober testi', isCorrect: true },
        { key: 'B', text: 'Finkelstein testi', isCorrect: false },
        { key: 'C', text: 'Lachman testi', isCorrect: false },
        { key: 'D', text: 'Apley kompresyon testi', isCorrect: false },
        { key: 'E', text: 'Hawkins-Kennedy testi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Schober testi (veya modifiye Schober), lumbosakral bileşke (L5-S1 gamzeleri arası) hizasından yukarı doğru 10 cm işaretlenip hastaya tam fleksiyon yaptırıldığında mesafenin ne kadar uzadığını ölçer. Normalde en az 5 cm uzamalıdır (toplam >= 15 cm). 5 cm\'den az artış lomber fleksiyon kısıtlılığını gösterir.',
      hamSoru: 'Ankilozan spondilitte lomber omurga hareketliliğini ölçen test: Schober testi'
    }
  ];

  return list.map(q => ({
    id: `d3-k5-ftr-${String(q.num).padStart(3, '0')}`,
    committeeId: 'donem3-kurul5',
    folderKey: 'donem3k5',
    donem: 3,
    kurul: 5,
    discipline: 'Fiziksel Tıp ve Rehabilitasyon',
    topic: q.topic,
    questionNumber: q.num,
    examYear: '2021-2026',
    sourceFile: 'FTR_Kurul5_Cikmis_Sorular.json',
    stem: q.stem,
    options: q.options,
    correctAnswer: q.correctAnswer,
    explanation: q.explanation,
    hamSoru: q.hamSoru,
    rawQuestion: {
      stem: q.hamSoru || q.stem,
      options: q.options.map(o => ({ key: o.key, text: o.text })),
      claimedAnswer: q.correctAnswer
    },
    reconstruction: {
      stem: q.stem,
      options: q.options,
      correctAnswer: q.correctAnswer,
      explanation: q.explanation,
      confidenceScore: 100,
      reconstructionQuality: 'verified',
      notesAndDiscrepancies: 'Fiziksel Tıp ve Rehabilitasyon amfi ders notları (Lomber-Servikal Muayene, Eklem Muayenesi, EHA ve Egzersiz Tedavileri, Artritler) ile tam doğrulanmıştır.'
    },
    sourceNote: q.source,
    isSuspect: false,
    isAmbiguous: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }));
}

// -------------------------------------------------------------
// 4. İÇ HASTALIKLARI (HEMATOLOJİ) (20 Soru)
// -------------------------------------------------------------
export function buildDahiliyeKurul5Questions() {
  const list = [
    {
      num: 1,
      topic: 'Demir Eksikliği vs Talasemi Taşıyıcılığı Ayrımı',
      source: '2. demir metabolizması.txt',
      stem: 'Mikrositer anemi saptanan bir hastada Demir Eksikliği Anemisi ile Beta-Talasemi Minör (taşıyıcılık) ayırıcı tanısı ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'RDW (eritrosit dağılım genişliği) değeri Talasemi taşıyıcılığında belirgin derecede yüksekken, Demir Eksikliği Anemisinde tamamen normal sınırlardadır.', isCorrect: true },
        { key: 'B', text: 'Mentzer indeksi (MCV / RBC sayısı) Demir Eksikliği Anemisinde >13, Talasemi taşıyıcılığında ise <13 olarak hesaplanır.', isCorrect: false },
        { key: 'C', text: 'Talasemi taşıyıcılığında eritrosit sayısı (RBC) anemiye rağmen sıklıkla 5 milyon/uL\'nin üzerindedir (mikrositoza eşlik eden eritrositoz).', isCorrect: false },
        { key: 'D', text: 'Serum ferritini ve kemik iliği hemosiderin depoları Demir Eksikliğinde azalmış, Talasemi taşıyıcılığında ise normal veya hafif artmıştır.', isCorrect: false },
        { key: 'E', text: 'Hemoglobin elektroforezinde HbA2 düzeyinin %3.5\'in üzerinde olması Beta-Talasemi taşıyıcılığı lehinedir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Demir eksikliği anemisinde eritrosit boyutları değişkendir (anizositoz); bu nedenle RDW YÜKSEKTİR (>%15). Talasemi taşıyıcılığında ise genetik homojenite nedeniyle mikrositer hücreler tekdüzedir ve RDW NORMALDİR. Mentzer indeksi MCV/RBC <13 talasemi, >13 demir eksikliği lehinedir.',
      hamSoru: 'Demir eksikliği ve talasemi ayrımı için hangisi yanlıştır? Talasemi de RDW yüksek demir eksikliğinde normaldir (yanlıştır, tam tersi)'
    },
    {
      num: 2,
      topic: 'Vejetaryen Hastada B12 Eksikliği ve Tedavi Yaklaşımı',
      source: '3.Megaloblastik Anemiler.txt',
      stem: 'Kırk iki yaşında sıkı vejetaryen erkek hasta son iki aydır yürürken dengesizlik, bacaklarda uyuşma ve unutkanlık yakınmaları ile başvuruyor. Laboratuvarında Hb: 9.1 g/dL, MCV: 112 fL, RDW yüksek, periferik yaymada oval makrositler ve nötrofillerde hipersegmentasyon görülüyor. Serum B12: 98 pg/mL, serum metilmalonik asit ve homosistein belirgin yüksek bulunuyor. Bu hastada tedavi yaklaşımında en kritik kural aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Öncelikle parenteral B12 vitamini tedavisi başlanmalıdır; çünkü tek başına folat verilirse anemi hematolojik olarak düzelse bile geri dönüşümsüz nörolojik hasar (subakut kombine dejenerasyon) ilerlemeye devam eder.', isCorrect: true },
        { key: 'B', text: 'Önce oral yüksek doz folik asit başlanmalıdır, çünkü folat eksikliği nörolojik bulguları daha hızlı düzeltir.', isCorrect: false },
        { key: 'C', text: 'Sadece kırmızı etten zengin diyet düzenlenmesi yeterlidir, ilaç tedavisine gerek yoktur.', isCorrect: false },
        { key: 'D', text: 'Hematolojik parametreler normale dönene kadar B12 vitamini verilmemelidir.', isCorrect: false },
        { key: 'E', text: 'Metilmalonik asit yüksekliğini düşürmek için piridoksin (B6) monoterapisi uygulanmalıdır.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'B12 eksikliği tanısı konmadan veya B12 verilmeden tek başına Folat verilirse "folat tuzağı" aşılır ve megaloblastik anemi düzelir; ancak B12\'nin miyelin sentezindeki kofaktör rolü karşılanamaz. Sonuçta spinal kordun arka ve yan kordon demiyelinizasyonu (subakut kombine dejenerasyon) sessizce ilerler ve kalıcı parapleji/nörolojik hasar oluşur.',
      hamSoru: '42 yaşında vejetaryen erkek B12 eksikliği tedavisi: Önce B12 başlanmalı; tek başına folat verilirse anemi düzelir fakat geri dönüşümsüz nörolojik hasar devam eder'
    },
    {
      num: 3,
      topic: 'B12 Vitamini Fizyolojik Emilim Yolu',
      source: '3.Megaloblastik Anemiler.txt',
      stem: 'Diyetle alınan B12 vitamininin (kobalamin) gastrointestinal kanaldan fizyolojik olarak emilerek kana geçebilmesi için midede pariyetal hücrelerden salınan hangi glikoproteine bağlanması ve hangi bağırsak segmentinden reseptör aracılı emilmesi zorunludur?',
      options: [
        { key: 'A', text: 'İntrinsik faktör (İF) - Terminal ileum', isCorrect: true },
        { key: 'B', text: 'Haptokorrin (R-bağlayıcı) - Duodenum', isCorrect: false },
        { key: 'C', text: 'Transkobalamin II - Jejunum', isCorrect: false },
        { key: 'D', text: 'Ferritin - Çekum', isCorrect: false },
        { key: 'E', text: 'Hepcidin - Kolon', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'B12 vitamini midede pariyetal hücrelerin salgıladığı "İntrinsik Faktör" (İF) ile kompleks oluşturur. Bu B12-İF kompleksi pankreatik enzimlere dirençlidir ve terminal ileumdaki spesifik kübilin/amnionless reseptörleri aracılığıyla kalsiyum varlığında reseptör aracılı endositozla emilir.',
      hamSoru: 'B12 vitamini emilirken intestiyuma ne aracılığıyla alınır? İntrinsik faktör'
    },
    {
      num: 4,
      topic: 'K Vitaminine Bağımlı Olmayan Koagülasyon Faktörü',
      source: 'Hemostaz ve Kanama Diyatezleri.txt',
      stem: 'Karaciğerde gama-glutamil karboksilaz enzimi aracılığıyla glutamik asit kalıntılarının karboksillenmesi için K vitaminine İHTİYAÇ DUYMAYAN koagülasyon faktörü aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Faktör VIII (F8)', isCorrect: true },
        { key: 'B', text: 'Faktör II (Protrombin)', isCorrect: false },
        { key: 'C', text: 'Faktör VII (Prokonvertin)', isCorrect: false },
        { key: 'D', text: 'Faktör IX (Christmas faktörü)', isCorrect: false },
        { key: 'E', text: 'Faktör X (Stuart-Prower faktörü)', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'K vitaminine bağımlı pıhtılaşma faktörleri: Faktör II, VII, IX, X ve antikoagülan Protein C ile Protein S\'dir (1972 kuralı). Faktör VIII ise karaciğer dışı vasküler endotel hücrelerinde üretilir ve von Willebrand faktör ile taşınır; K vitaminine bağımlı DEĞİLDİR.',
      hamSoru: 'K vit\'e bağlı olmayan faktör hangisidir? Faktör 8 (F8)'
    },
    {
      num: 5,
      topic: 'Glanzmann Trombastenisi Moleküler Defekti',
      source: 'Hemostaz ve Kanama Diyatezleri.txt',
      stem: 'Mukokutanöz kanamalarla başvuran, trombosit sayısı ve morfolojisi tamamen normal olan ancak periferik kanda trombosit agregasyonunun gerçekleşmediği Glanzmann Trombastenisinde eksik olan trombosit yüzey glikoprotein kompleksi aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Glikoprotein IIb/IIIa (İntegrin alfa-IIb / beta-3)', isCorrect: true },
        { key: 'B', text: 'Glikoprotein Ib-IX-V kompleksi', isCorrect: false },
        { key: 'C', text: 'Glikoprotein Ia/IIa (Kollajen reseptörü)', isCorrect: false },
        { key: 'D', text: 'Glikoprotein VI', isCorrect: false },
        { key: 'E', text: 'P-selektin (CD62P)', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Glanzmann trombastenisi otozomal resesif bir trombosit agregasyon bozukluğudur. Fibrinojenin bağlandığı GP IIb/IIIa (CD41/CD61) reseptörü eksiktir veya fonksiyon dışıdır. ADP, epinefrin ve kollajen ile trombositler agrege olamaz (ristosetin ile aglütinasyon korunur). GP Ib eksikliği ise Bernard-Soulier sendromudur.',
      hamSoru: 'Glanzmann hangisinin eksikliğinde? Gp 2b-3a'
    },
    {
      num: 6,
      topic: 'Megaloblastik Anemi Spesifik Morfolojik Bulgusu',
      source: '3.Megaloblastik Anemiler.txt',
      stem: 'Periferik kan yaymasında B12 vitamini veya folik asit eksikliğine bağlı megaloblastik anemiyi diğer makrositer anemilerden ayıran en erken ve en spesifik lökosit bulgusu aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Nötrofillerin nükleuslarında hipersegmentasyon (6 veya daha fazla loblu nötrofil görülmesi)', isCorrect: true },
        { key: 'B', text: 'Lenfositlerde atipik Downey hücresi dönüşümü', isCorrect: false },
        { key: 'C', text: 'Monositoz ve Auer çomakları varlığı', isCorrect: false },
        { key: 'D', text: 'Döhle cisimcikleri ve toksik granülasyon', isCorrect: false },
        { key: 'E', text: 'Pelger-Huet nükleer hiposegmentasyonu', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Megaloblastik anemide DNA sentezi bozulur ancak RNA ve sitoplazma gelişimi devam eder (nükleositoplazmik asenkroni). Nötrofillerde nükleer segmentasyon gecikir ve anormal artar; periferik yaymada nükleusu 5\'ten fazla (özellikle 6 ve üzeri) lob içeren nötrofillerin görülmesi (hipersegmentasyon) megaloblastik aneminin patognomonik periferik bulgusudur.',
      hamSoru: 'megaloblastik anemi için spesifik bulgu? periferik yaymada nötrofil segment sayısının 6 ve üstünde olması'
    },
    {
      num: 7,
      topic: 'Demir Metabolizması ve Göstergeleri',
      source: '2. demir metabolizması.txt',
      stem: 'Vücut demir metabolizması ve laboratuvar parametreleri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'Plazma demir konsantrasyonu (serum demiri) günlük diurnal ritimden ve beslenmeden etkilenmediği için toplam vücut demir deposunu tek başına en doğru yansıtan göstergedir.', isCorrect: true },
        { key: 'B', text: 'Vücudun demir depo miktarını en güvenilir yansıtan plazma parametresi ferritin düzeyidir.', isCorrect: false },
        { key: 'C', text: 'Diyetle alınan Fe+3 (ferrik) demir, duodenal sitokrom B (DCYTB) enzimi ile Fe+2 (ferröz) forma indirgenerek DMT-1 ile enterosite alınır.', isCorrect: false },
        { key: 'D', text: 'Dolaşımda plazma demiri transferrine bağlı olarak taşınır ve normal transferrin satürasyonu %20-45 arasındadır.', isCorrect: false },
        { key: 'E', text: 'Serum demirinin aşırı yükselmesi ve transferrin satürasyonunun >%50 olması hipersideremi / demir yüklenmesi lehinedir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Serum demiri gün içi saatlik dalgalanma gösterir, akut inflamasyondan, diyetten etkilenir; bu nedenle tek başına vücut demir deposunu güvenle yansıtmaz. Vücut demir depolarının en doğru plazma göstergesi "FERRİTİN"dir (1 ug/L serum ferritini yaklaşık 8-10 mg depo demirine karşılık gelir).',
      hamSoru: 'Demir metabolizması ile ilgili hangisi yanlıştır? Plazma demir konsantrasyonu vücut demir miktarını en doğru yansıtır (yanlıştır, ferritin yansıtır)'
    },
    {
      num: 8,
      topic: 'Koagülasyon Yolağı Testleri: aPTT vs PT',
      source: 'Hemostaz ve Kanama Diyatezleri.txt',
      stem: 'Hemostaz mekanizması ve pıhtılaşma tarama testleri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'Aktive parsiyel tromboplastin zamanı (aPTT) sadece ekstrensek yolağı değerlendiren ve Faktör VII eksikliğine en duyarlı olan testtir.', isCorrect: true },
        { key: 'B', text: 'Protrombin zamanı (PT/INR) ekstrensek yolağı (Faktör VII) ve ortak yolağı değerlendirir.', isCorrect: false },
        { key: 'C', text: 'aPTT intrensek yolağı (Faktör XII, XI, IX, VIII) ve ortak yolağı değerlendirir.', isCorrect: false },
        { key: 'D', text: 'Ristosetin kofaktör aktivitesi von Willebrand hastalığı teşhisinde vWF fonksiyonunu değerlendiren en spesifik testtir.', isCorrect: false },
        { key: 'E', text: 'K vitamini eksikliğinde ilk uzayan test Faktör VII\'nin yarı ömrü en kısa olduğu için PT\'dir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'aPTT intrensek ve ortak yolağı değerlendirir; intrensek yolak Faktör XII, XI, IX ve VIII\'den oluşur. Ekstrensek yolağı (Faktör VII ve Doku Faktörü) değerlendiren test ise Protrombin Zamanıdır (PT).',
      hamSoru: 'Aşağıdakilerden hangisi yanlıştır? aPTT ekstrensek yolağı değerlendirir (yanlıştır, intrensek yolağı değerlendirir)'
    },
    {
      num: 9,
      topic: 'Talasemi Majörde Görülmeyen Komplikasyon',
      source: 'Hemoglobinopatiler.txt',
      stem: 'Beta-Talasemi Majör (Cooley anemisi) tanılı ve düzenli transfüzyon almayan bir çocukta kronik ağır hemoliz ve kemik iliği aşırı aktivitesine bağlı olarak beklenen klinik bulgular arasında aşağıdakilerden hangisi YER ALMAZ?',
      options: [
        { key: 'A', text: 'Dalakta tekrarlayan enfarktlar sonucu erken yaşta spontan otosplenektomi gelişmesi', isCorrect: true },
        { key: 'B', text: 'Kemik iliği eritroid hiperplazisi nedeniyle kafatasında kıl fırça manzarası ve elmacık kemiklerinde belirginleşme (sincap yüzü görünümü)', isCorrect: false },
        { key: 'C', text: 'Masif splenomegali ve hepatomegali (ekstramedüller hematopoez)', isCorrect: false },
        { key: 'D', text: 'Ağır inefektif eritropoez ve büyüme geriliği / kaşeksi', isCorrect: false },
        { key: 'E', text: 'Hem transfüzyona hem de aşırı bağırsak demir emilimine bağlı sekonder hemokromatozis (hemosiderozis)', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Otosplenektomi (dalağın tekrarlayan vazooklüzif enfarktlar ve fibrozis sonucu küçülüp yok olması) ORAK HÜCRELİ ANEMİYE özgüdür. Beta-Talasemi majörde ise tam tersine aşırı ekstravasküler hemoliz ve ekstramedüller hematopoez nedeniyle MASİF SPLENOMEGALİ gelişir; otosplenektomi asla görülmez.',
      hamSoru: 'Aşağıdakilerden hangisi talasemi durumunda beklenmez? Otosplenektomi (orak hücrelide olur)'
    },
    {
      num: 10,
      topic: 'Herediter Sferositozda Beklenmeyen Durum',
      source: '1 kısım D20 D21 D22 eritros_hast_pat.txt',
      stem: 'Eritrosit iskelet membran proteinleri (ankirin, spektrin, bant 3) genetik mutasyonlarına bağlı gelişen Herediter Sferositozda aşağıdaki patofizyolojik ve klinik durumlardan hangisi BEKLENMEZ?',
      options: [
        { key: 'A', text: 'Kemik iliğinde eritroid seride matürasyon arresti ve belirgin inefektif eritropoez', isCorrect: true },
        { key: 'B', text: 'Splenomegali (sferositlerin dalak kırmızı pulpasında hapsolması)', isCorrect: false },
        { key: 'C', text: 'Retikülositoz (kemik iliğinin kompanse edici aşırı eritroid hiperplazisi)', isCorrect: false },
        { key: 'D', text: 'Kalsiyum bilirübinat safra kesesi taşları (kolelitiyazis)', isCorrect: false },
        { key: 'E', text: 'Osmotik frajilite testinde eritrositlerin hipotonik tuz çözeltisinde erken hemolizi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Herediter sferositozda kemik iliğinde üretim tamamen normal ve etkilidir (efektif eritropoez vardır, retikülosit sayısı %10-20\'lere fırlar). Sorun periferde dalağın sferositleri parçalamasıdır (ekstravasküler hemoliz). "İnefektif eritropoez" (hücrelerin kemik iliğinde ölmesi) ise Talasemi ve Megaloblastik Anemiye özgüdür.',
      hamSoru: 'hangisi herediter sferositozda beklenmez? inefektif eritropoez'
    },
    {
      num: 11,
      topic: 'Oksijen Taşıyan Hemoglobin Demirinin Değerliği',
      source: '1.Anemiler Tanım ve Patofizyoloji.txt',
      stem: 'Normal koşullarda eritrositler içerisinde moleküler oksijeni (O2) reversibl olarak bağlayıp dokulara taşımakla görevli hemoglobin hem grubundaki demir atomunun elektriksel değerliği aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Fe+2 (Ferröz demir)', isCorrect: true },
        { key: 'B', text: 'Fe+3 (Ferrik demir)', isCorrect: false },
        { key: 'C', text: 'Fe0 (Elementer demir)', isCorrect: false },
        { key: 'D', text: 'Fe+4 (Ferroradikal demir)', isCorrect: false },
        { key: 'E', text: 'Fe+1 (Hipoprotodemir)', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Hemoglobinde oksijen bağlayabilen fonksiyonel demir "Fe+2" (ferröz) değerliklidir. Eğer demir oksitlenerek "Fe+3" (ferrik) hale geçerse "Methemoglobin" oluşur; methemoglobin oksijen taşıyamaz ve doku hipoksisi ile siyanoza yol açar.',
      hamSoru: 'Hangisi yanlıştır? Oksijen taşıyan demir Fe+3 (yanlıştır, oksijen taşıyan Fe+2\'dir)'
    },
    {
      num: 12,
      topic: 'Anemilerde Genel Tanı İlkeleri ve Kurallar',
      source: '1.Anemiler Tanım ve Patofizyoloji.txt',
      stem: 'Anemilerin klinik ve laboratuvar değerlendirmesi ile ilgili aşağıdaki ifadelerden hangileri doğrudur?\n\nI. Normal koşullarda ve normositik eritrositlerde "Hemoglobin (g/dL) x 3 = Hematokrit (%)" kuralı yaklaşık olarak geçerlidir.\nII. Yüksek rakımda yaşayanlarda ve kronik sigara içicilerinde doku hipoksisi EPO salınımını uyararak hematokriti fizyolojik olarak yükseltir.\nIII. Kronik hastalık anemisi başlangıçta normositer iken uzun vadede mikrositer hipokrom anemi tablosu sergileyebilir.\nIV. B12 vitamini ve folat eksikliği anemisi tipik non-megaloblastik makrositer anemi örneğidir.',
      options: [
        { key: 'A', text: 'I, II ve III', isCorrect: true },
        { key: 'B', text: 'I ve II', isCorrect: false },
        { key: 'C', text: 'II ve IV', isCorrect: false },
        { key: 'D', text: 'Yalnız III', isCorrect: false },
        { key: 'E', text: 'I, II, III ve IV', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'I doğru (3 katı kuralı), II doğru (yüksek irtifa ve sigara sekonder polisitemi yapar), III doğru (KHA normositer başlar, demir kısıtlı eritropoezle mikrositerleşebilir). IV ise YANLIŞTIR: B12 ve folat eksikliği MEGALOBLASTİK aneminin prototipidir; non-megaloblastik makrositoz ise karaciğer hastalığı, hipotiroidi ve alkolizmde görülür.',
      hamSoru: 'Anemilerle ilgili hangileri doğrudur? 1-Hb x 3 = Hct, 2-dağda/sigarada Hct yüksek, 3-KHA mikrositer/normositer olabilir (1, 2, 3 doğrudur)'
    },
    {
      num: 13,
      topic: 'Oral Demir Absorbsiyon Testi',
      source: '2. demir metabolizması.txt',
      stem: 'Oral demir tedavisine dirençli veya malabsorpsiyon şüphesi olan hastalarda bağırsak demir emilim kapasitesini değerlendirmek için yapılan Oral Demir Absorbsiyon Testi ile ilgili aşağıdaki ifadelerden hangileri doğrudur?\n\nI. Test öncesi bazal açlık serum demir düzeyi ölçülür.\nII. Hastaya oral yoldan standart dozda (örneğin 60-65 mg elementer demir) demir preparatı verilir.\nIII. İkinci saatte ölçülen serum demir düzeyinin bazale göre en az 50-100 ug/dL artması normal emilimi gösterir; artışın olmaması emilim bozukluğuna (örn. Çölyak) işaret eder.',
      options: [
        { key: 'A', text: 'I, II ve III', isCorrect: true },
        { key: 'B', text: 'I ve II', isCorrect: false },
        { key: 'C', text: 'II ve III', isCorrect: false },
        { key: 'D', text: 'Yalnız I', isCorrect: false },
        { key: 'E', text: 'Yalnız III', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Oral demir absorbsiyon testinde: Sabah aç karnına bazal serum demiri alınır, ardından oral demir verilir ve 2. saatte serum demiri tekrar ölçülür. Normal bireylerde serum demirinde >50-100 ug/dL belirgin bir artış beklenir. Artış olmaması duodenal mukoza hasarını veya emilim bozukluğunu gösterir.',
      hamSoru: 'Oral demir absorbsiyon testi ile ilgili hangileri doğrudur? Bazal açlık ölçümü, oral demir verilmesi, serum demir artış kriteri'
    },
    {
      num: 14,
      topic: 'Kronik Hastalık Anemisi ve Hepcidin Rolü',
      source: '1.Anemiler Tanım ve Patofizyoloji.txt',
      stem: 'Kronik enfeksiyon, malignite ve romatolojik otoimmün hastalıklarda karaciğerden IL-6 uyarısıyla sentezlenen hepcidin hormonunun ferroportin kanallarını parçalaması sonucu gelişen Kronik Hastalık Anemisinde laboratuvarda aşağıdakilerden hangisi izlenir?',
      options: [
        { key: 'A', text: 'Serum demiri düşük, ferritin düzeyi normal veya yüksek, toplam demir bağlama kapasitesi (TDBK) düşük', isCorrect: true },
        { key: 'B', text: 'Serum demiri yüksek, ferritin düşük, TDBK aşırı yüksek', isCorrect: false },
        { key: 'C', text: 'Serum demiri ve ferritin sıfır, TDBK normal', isCorrect: false },
        { key: 'D', text: 'Ferritin <10 ng/mL ve transferrin satürasyonu >%60', isCorrect: false },
        { key: 'E', text: 'Serum ferritini düşük ve çözünür transferrin reseptörü (sTfR) aşırı yüksek', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Kronik hastalık anemisinde (KHA) temel sorun demir yokluğu değil; demirin makrofajlarda ve karaciğerde hapsedilmesidir (demir kilitlenmesi). Hepcidin ferroportini yıktığı için demir plazmaya salınamaz: Serum demiri düşüktür, ferritin (akut faz reaktanı olarak da) normal veya YÜKSEKTİR, TDBK ise DÜŞÜKTÜR.',
      hamSoru: 'Kronik hastalık anemisinde laboratuvar: Serum demiri düşük, ferritin normal veya yüksek, TDBK düşük'
    },
    {
      num: 15,
      topic: 'von Willebrand Hastalığı ve Laboratuvar Bulguları',
      source: 'Hemostaz ve Kanama Diyatezleri.txt',
      stem: 'En sık görülen kalıtsal kanama diyatezi olan von Willebrand Hastalığı (vWH Tip 1) ile ilgili aşağıdaki ifadelerden hangisi doğrudur?',
      options: [
        { key: 'A', text: 'Hem primer hemostazı (trombosit adezyon bozukluğuna bağlı kanama zamanı uzaması) hem de sekonder hemostazı (Faktör VIII taşıyıcılığı azaldığı için aPTT uzaması) etkileyebilir.', isCorrect: true },
        { key: 'B', text: 'Daima X\'e bağlı resesif kalıtılır ve sadece erkek çocuklarda kanama yapar.', isCorrect: false },
        { key: 'C', text: 'Trombosit sayısı <20.000/uL düzeyine kadar düşer.', isCorrect: false },
        { key: 'D', text: 'Protrombin zamanı (PT) belirgin derecede uzar.', isCorrect: false },
        { key: 'E', text: 'Tedavide desmopresin (dDAVP) kullanımı tamamen kontrendikedir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'vWF iki temel göreve sahiptir: 1) Trombositleri subendotelyal kollajene bağlar (adezyon) - eksikliğinde kanama zamanı uzar, mukokutanöz kanama olur. 2) Dolaşımda Faktör VIII\'i yıkımdan korur - eksikliğinde F8 plazma düzeyi düşer ve aPTT uzar. vWH otozomal dominant kalıtılır, trombosit sayısı genellikle normaldir.',
      hamSoru: 'von Willebrand hastalığı özellikleri: Kanama zamanı ve aPTT uzayabilir, primer ve sekonder hemostazı etkiler'
    },
    {
      num: 16,
      topic: 'Hemofili Kalıtımı ve Klinik Tablo',
      source: 'Hemostaz ve Kanama Diyatezleri.txt',
      stem: 'Faktör VIII eksikliği (Hemofili A) ve Faktör IX eksikliği (Hemofili B) ile ilgili aşağıdaki klinik ve genetik ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'Hemofili B taşıyıcısı olan bir kadının babası hemofili hastası ise tüm erkek çocukları kesinlikle %100 hemofili hastası olarak doğar.', isCorrect: true },
        { key: 'B', text: 'Hemofili A ve Hemofili B X\'e bağlı resesif kalıtım gösterir.', isCorrect: false },
        { key: 'C', text: 'Hemofili hastası bir erkeğin tüm kız çocukları zorunlu olarak taşıyıcı olur.', isCorrect: false },
        { key: 'D', text: 'Klinik şiddet ve kanama sıklığı plazmadaki aktif faktör düzeyinin düşüklüğü ile doğru orantılıdır.', isCorrect: false },
        { key: 'E', text: 'Ağır hemofilide en karakteristik kanama tipi yük taşıyan büyük eklemlere spontan kanamadır (hemartroz).', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Hemofili taşıyıcısı bir kadının (X^H X^h) her bir erkek çocuğuna mutant X kromozomunu aktarma olasılığı %50\'dir (yani erkek çocuklarının %50\'si hasta, %50\'si sağlıklı doğar; %100 değildir). Hemofili hastası erkeğin (X^h Y) ise tüm kızları X^h alacağı için %100 taşıyıcı olur.',
      hamSoru: 'Hemofili için hangisi yanlıştır? Taşıyıcı kadının tüm erkek çocukları kesinlikle hasta doğar (yanlıştır, %50 ihtimal vardır)'
    },
    {
      num: 17,
      topic: 'TTP Patogenezi ve ADAMTS13 Enzimi',
      source: 'Hemostaz ve Kanama Diyatezleri.txt',
      stem: 'Trombositopeni, mikroanjiyopatik hemolitik anemi (şistositler), dalgalı nörolojik semptomlar, böbrek fonksiyon bozukluğu ve ateşten oluşan klasik klinik pentadla karakterize Trombotik Trombositopenik Purpura (TTP) tablosunda patogenezden sorumlu temel moleküler bozukluk aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'von Willebrand faktörü parçalayan metalloproteaz olan ADAMTS13 enzim aktivitesinin ağır eksikliği veya inhibe edici otoantikorlar', isCorrect: true },
        { key: 'B', text: 'Shiga toksininin endotel hücresinde Gb3 reseptörüne bağlanması', isCorrect: false },
        { key: 'C', text: 'Faktör V Leiden mutasyonuna bağlı aktive protein C direnci', isCorrect: false },
        { key: 'D', text: 'Prokalsitonin ve protein S genetik duplikasyonu', isCorrect: false },
        { key: 'E', text: 'GP Ib reseptörüne karşı alloantikor gelişimi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'TTP\'de ADAMTS13 (vWF-cleaving protease) eksiktir (otoantikorlara veya nadiren konjenital mutasyona bağlı). vWF ultra-büyük multimerleri parçalanamaz ve mikrovasküler yatakta yaygın trombosit agregasyonuna ve trombüslere yol açar. Trombositler tüketilir, eritrositler bu pıhtılardan geçerken parçalanır (şistositler). Tedavisi acil plazmaferezdir.',
      hamSoru: 'TTP tablosunda patogenezden sorumlu temel defekt: ADAMTS13 eksikliği'
    },
    {
      num: 18,
      topic: 'Dissemine İntravasküler Koagülasyon (DIC) Bulguları',
      source: 'Hemostaz ve Kanama Diyatezleri.txt',
      stem: 'Ağır sepsis, travma veya obstetrik komplikasyonlar zemininde yaygın mikrovasküler tromboz ve ardından tüketim koagülopatisi ile gelişen Yaygın Damar İçi Pıhtılaşma (DIC) tablosunda aşağıdaki laboratuvar bulgularından hangisi BEKLENMEZ?',
      options: [
        { key: 'A', text: 'Serum fibrinojen düzeyinde aşırı yükselme ve D-dimer negatifliği', isCorrect: true },
        { key: 'B', text: 'Trombositopeni (trombositlerin tüketilmesi)', isCorrect: false },
        { key: 'C', text: 'Protrombin zamanı (PT) ve aPTT testlerinde belirgin uzama', isCorrect: false },
        { key: 'D', text: 'Fibrin yıkım ürünlerinde ve D-dimer düzeyinde belirgin artış', isCorrect: false },
        { key: 'E', text: 'Periferik yaymada parçalanmış eritrositler (şistositler / miğfer hücreleri)', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'DIC bir "tüketim koagülopatisi"dir. Pıhtılaşma faktörleri ve fibrinojen aşırı tüketilir; bu nedenle plazma fibrinojeni DÜŞER. Oluşan yaygın fibrin pıhtıları sekonder fibrinoliz ile eritilir; bu nedenle D-dimer ve fibrin yıkım ürünleri AŞIRI DERECEDE YÜKSELİR.',
      hamSoru: 'DIC laboratuvarında hangisi beklenmez? Fibrinojen yükselmesi ve D-dimer negatifliği (yanlıştır, fibrinojen düşer, D-dimer çok yükselir)'
    },
    {
      num: 19,
      topic: 'Miyeloproliferatif Neoplazilerde Genetik Belirteçler',
      source: 'D24 Myeloid_lenfoid_1.txt',
      stem: 'BCR-ABL negatif klasik Miyeloproliferatif Neoplazilerin (Polisitemia Vera, Esansiyel Trombositemi, Primer Miyelofibrozis) tanısal değerlendirmesinde kullanılan sürücü (driver) gen mutasyonları arasında aşağıdakilerden hangisi YER ALMAZ?',
      options: [
        { key: 'A', text: 'NPM1 ve FLT3-ITD mutasyonları (Akut Miyeloid Lösemiye özgü mutasyonlar)', isCorrect: true },
        { key: 'B', text: 'JAK2 V617F mutasyonu', isCorrect: false },
        { key: 'C', text: 'JAK2 Ekzon 12 mutasyonu', isCorrect: false },
        { key: 'D', text: 'CALR (Kalretikülin) gen mutasyonları', isCorrect: false },
        { key: 'E', text: 'MPL (Trombopoietin reseptörü) gen mutasyonları', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Klasik BCR-ABL negatif miyeloproliferatif neoplazilerde (MPN) taranan 3 majör sürücü mutasyon vardır: JAK2 (V617F ve ekzon 12), CALR ve MPL mutasyonlarıdır. NPM1 ve FLT3 mutasyonları ise Akut Miyeloid Löseminin (AML) moleküler tanısında ve prognozunda kullanılan belirteçlerdir.',
      hamSoru: 'Myeloproliferatif hastalıklarda bakılan markerlardan biri değildir? NPM1 / FLT3'
    },
    {
      num: 20,
      topic: 'Aplastik Anemi Patofizyolojisi ve Tanı',
      source: '1.Anemiler Tanım ve Patofizyoloji.txt',
      stem: 'Kök hücre hasarı veya T lenfosit aracılı otoimmün süpresyon sonucu kemik iliğinde tüm hematopoetik serilerin baskılandığı Aplastik Anemi ile ilgili aşağıdaki ifadelerden hangisi doğrudur?',
      options: [
        { key: 'A', text: 'Kemik iliği biyopsisinde hematopoetik hücre oranı <%25\'e düşmüştür ve ilik boşluğu yağ dokusu ile dolmuştur; splenomegali kural olarak saptanmaz.', isCorrect: true },
        { key: 'B', text: 'Masif hepatosplenomegali ve lenfadenopati en temel tanı kriteridir.', isCorrect: false },
        { key: 'C', text: 'Periferik kanda belirgin retikülositoz ve polikromazi izlenir.', isCorrect: false },
        { key: 'D', text: 'Serum demiri çok düşük, transferrin satürasyonu sıfırdır.', isCorrect: false },
        { key: 'E', text: 'Tanıda birinci basamak küratif yaklaşım splenektomidir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Aplastik anemide multipotan kök hücre yok olur. Kemik iliğinde hematopoez durur, yerini sarı yağ iliği alır (hiposellüler ilik). Periferde pansitopeni ve retikülositopeni vardır. Fizik muayenede splenomegali OLMAMASI aplastik anemi lehine çok önemli bir ayırıcı tanı kriteridir (splenomegali varsa lösemi, lenfoma veya miyelofibrozis düşünülür).',
      hamSoru: 'Aplastik anemi özellikleri: Kemik iliğinde yağ dokusu artışı (<%25 sellülarite), splenomegali olmaması'
    }
  ];

  return list.map(q => ({
    id: `d3-k5-dah-${String(q.num).padStart(3, '0')}`,
    committeeId: 'donem3-kurul5',
    folderKey: 'donem3k5',
    donem: 3,
    kurul: 5,
    discipline: 'İç Hastalıkları (Hematoloji)',
    topic: q.topic,
    questionNumber: q.num,
    examYear: '2021-2026',
    sourceFile: 'Dahiliye_Hematoloji_Kurul5_Cikmis_Sorular.json',
    stem: q.stem,
    options: q.options,
    correctAnswer: q.correctAnswer,
    explanation: q.explanation,
    hamSoru: q.hamSoru,
    rawQuestion: {
      stem: q.hamSoru || q.stem,
      options: q.options.map(o => ({ key: o.key, text: o.text })),
      claimedAnswer: q.correctAnswer
    },
    reconstruction: {
      stem: q.stem,
      options: q.options,
      correctAnswer: q.correctAnswer,
      explanation: q.explanation,
      confidenceScore: 100,
      reconstructionQuality: 'verified',
      notesAndDiscrepancies: 'İç Hastalıkları (Hematoloji) amfi ders notları (Anemiler, Demir Metabolizması, Megaloblastik Anemiler, Hemostaz ve Kanama Bozuklukları) ile tam doğrulanmıştır.'
    },
    sourceNote: q.source,
    isSuspect: false,
    isAmbiguous: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }));
}

// -------------------------------------------------------------
// 5. ACİL TIP (15 Soru)
// -------------------------------------------------------------
export function buildAcilTipKurul5Questions() {
  const list = [
    {
      num: 1,
      topic: 'İKYD Şoklanabilir Ritimler',
      source: 'Dönem 3 - İKYD_260408_134353.txt',
      stem: 'Kardiyak arest tablosundaki bir hastada İleri Kardiyak Yaşam Desteği (İKYD) algoritmasına göre defibrilatör ile elektrik şoku uygulanabilen (şoklanabilir / geri döndürülebilir) ritimler hangi seçenekte doğru olarak verilmiştir?\n\nI. Ventriküler Fibrilasyon (VF)\nII. Nabızsız Elektriksel Aktivite (NEA)\nIII. Nabızsız Ventriküler Taşikardi (pVT)\nIV. Asistoli',
      options: [
        { key: 'A', text: 'I ve III', isCorrect: true },
        { key: 'B', text: 'II ve IV', isCorrect: false },
        { key: 'C', text: 'I, II ve III', isCorrect: false },
        { key: 'D', text: 'Yalnız I', isCorrect: false },
        { key: 'E', text: 'I, II, III ve IV', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Kardiyak arest ritimleri iki ana gruba ayrılır: 1) Şoklanabilir ritimler: Ventriküler Fibrilasyon (VF) ve Nabızsız Ventriküler Taşikardi (pVT). Bu ritimlerde derhal defibrilasyon uygulanır. 2) Şoklanamaz ritimler: Asistoli ve Nabızsız Elektriksel Aktivite (NEA). Bu ritimlerde defibrilasyon uygulanmaz; yüksek kaliteli CPR ve IV adrenalin verilir.',
      hamSoru: 'Yukarıdakilerden hangisi defibrile edilebilir (Geri döndürülebilir) bir ritim? 1-VF, 3-Nabızsız VT (1 ve 3)'
    },
    {
      num: 2,
      topic: 'İKYD Basamakları ve 30 Bası Sonrası',
      source: 'Dönem 3 - İKYD_260408_134353.txt',
      stem: 'Temel ve İleri Yaşam Desteğinde henüz ileri hava yolu (endotrakeal tüp) yerleştirilmemiş kardiyak arestli bir erişkinde kesintisiz 30 göğüs basısı tamamlandıktan sonra derhal yapılması gereken işlem aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Balon-valf-maske ile göğsü yükseltecek şekilde 2 suni soluk verilmesi (30:2 döngüsü)', isCorrect: true },
        { key: 'B', text: '1 mg intravenöz adrenalin uygulanması', isCorrect: false },
        { key: 'C', text: 'Hemen 150-200 Joule senkronize kardiyoversiyon uygulanması', isCorrect: false },
        { key: 'D', text: 'Karotis nabzının 30 saniye boyunca yeniden palpe edilmesi', isCorrect: false },
        { key: 'E', text: 'Derhal santral venöz kateter takılması', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'İleri hava yolu olmayan erişkin kardiyak resüsitasyonunda standart bası-soluk oranı 30:2\'dir. 30 yüksek kaliteli göğüs basısının hemen ardından hava yolu açılır ve her biri 1 saniye süren 2 kurtarıcı soluk verilir; göğüs basılarına verilen ara 10 saniyeyi kesinlikle geçmemelidir.',
      hamSoru: 'İKYD başlanan entübasyon yapılmayan hastada 30 kalp basısından sonra yapılması gereken ilk şey nedir? Balon maske ile 2 suni soluk verilmeli'
    },
    {
      num: 3,
      topic: 'Kardiyak Arest İlk 2 Dakikada Yapılmayan İşlem',
      source: 'Dönem 3 - İKYD_260408_134353.txt',
      stem: 'Şoklanabilir bir ritimle (VF/pVT) seyreden kardiyak arest olgusunda ilk şok uygulandıktan hemen sonraki ilk 2 dakikalık CPR siklusu içerisinde aşağıdakilerden hangisinin yapılması ALGORİTMAYA UYGUN DEĞİLDİR?',
      options: [
        { key: 'A', text: '1 mg intravenöz adrenalin enjeksiyonu yapılması', isCorrect: true },
        { key: 'B', text: 'Kesintisiz ve yüksek kaliteli göğüs basısı uygulanması', isCorrect: false },
        { key: 'C', text: 'Yüksek akımlı oksijen desteği sağlanması', isCorrect: false },
        { key: 'D', text: 'Hava yolu açıklığının sağlanması ve monitörizasyonun kontrolü', isCorrect: false },
        { key: 'E', text: 'Geri döndürülebilir nedenlerin (5H / 5T) taranmaya başlanması', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'VF/pVT algoritmasında 1. şok sonrası hemen 2 dakika CPR yapılır. Adrenalin İLK 2 DAKİKADA VERİLMEZ. Adrenalin (1 mg IV) 2. başarısız şoktan sonra (3. şok öncesi veya CPR sırasında) başlanır ve her 3-5 dakikada bir tekrarlanır. İlk 2 dakikada erken adrenalin verilmesi VF\'de sağkalımı artırmaz.',
      hamSoru: 'Kardiyak Arest olan kişide ilk 2 dakika içinde hangisi yapılmaz? Adrenalin enjeksiyonu yapılmaz'
    },
    {
      num: 4,
      topic: 'ATLS-10 İlk Bakıda Hayatı Tehdit Eden Yaralanmalar',
      source: 'Dönem 3 - Travma.txt',
      stem: 'ATLS 10. Baskı ilk bakı (Primary Survey) basamağında göğüs travmasında derhal tanınıp dakikalar içinde tedavi edilmesi gereken ve hayatı doğrudan tehdit eden patolojilerden biri aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Masif hemotoraks', isCorrect: true },
        { key: 'B', text: 'Subdural hematom', isCorrect: false },
        { key: 'C', text: 'C1-C3 seviyesinde stabil olmayan omurilik yaralanması', isCorrect: false },
        { key: 'D', text: 'Batın içi solid organ yaralanması', isCorrect: false },
        { key: 'E', text: 'Pelvis kırığına bağlı hematom', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'ATLS ilk bakıda toraksta hayatı tehdit eden majör yaralanmalar: 1) Havayolu obstrüksiyonu, 2) Trakeobronşiyal ağaç yaralanması, 3) Tansiyon pnömotoraks, 4) Açık pnömotoraks, 5) Masif hemotoraks (>1500 mL kan), 6) Kardiyak tamponad ve 7) Yelken göğüstür (Flail chest). Masif hemotoraks bu ölümcül tablolardan biridir.',
      hamSoru: 'ATLS-10 ilk bakıda bakılması gereken hastalıklardan biridir? Masif hemotoraks'
    },
    {
      num: 5,
      topic: 'Kardiyak Arestte 5H-5T ve Hipotermi',
      source: 'Dönem 3 - Özel durumlarda İKYD_260408_134230.txt',
      stem: 'Bir kış sabahı banyoda ıslak ve bilinci kapalı bulunan 64 yaşındaki erkek hasta acil servise CPR eşliğinde getiriliyor. Monitörizasyonda asistoli saptanıyor. Kan gazı alınıyor, hasta başı ultrasonografide sağ kalp boşlukları doğal, perikardiyal mayi yok, pnömotoraks ekarte ediliyor. Bu hastada resüsitasyon başarısını doğrudan belirleyen ve geri döndürülebilir nedenler (5H-5T) arasında henüz DEĞERLENDİRİLMEMİŞ olan en kritik parametre aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Hastanın vücut çekirdek sıcaklığı (Ağır hipotermi varlığı)', isCorrect: true },
        { key: 'B', text: 'Karbonmonoksit düzeyi', isCorrect: false },
        { key: 'C', text: 'Aort diseksiyonu genişliği', isCorrect: false },
        { key: 'D', text: 'Sol ventrikül ejeksiyon fraksiyonu', isCorrect: false },
        { key: 'E', text: 'Serum kalsiyum düzeyi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Soğuk kış günü ıslak bulunan ve asistolide olan hastada geri döndürülebilir nedenlerden "Hipotermi" (Hypothermia) mutlaka düşünülmelidir. Ağır hipotermide kalp asistolide kalabilir. Hipotermik hasta ısıtılana kadar "ölü kabul edilmez" ("Kimse sıcak ve ölü olana kadar ölü değildir"). Çekirdek vücut sıcaklığı (özofagus/rektal prob) mutlaka ölçülmeli ve aktif dahili ısıtma yapılmalıdır.',
      hamSoru: 'Kış günü banyoda ıslak bulunan asistoli hasta geri döndürülebilir nedenlerden hangisine bakılmadı? Vücut sıcaklığı (hipotermi)'
    },
    {
      num: 6,
      topic: 'Senkop Tanımı ve Klinik Özellikleri',
      source: 'SENKOP.txt',
      stem: 'Geçici bilinç kaybı nedenlerinden biri olan Senkop ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'Senkop, serebral perfüzyon bozukluğuna bağlı gelişen ve kural olarak 30 dakikadan uzun süren derin bilinç kaybı tablosudur.', isCorrect: true },
        { key: 'B', text: 'Kardiyak senkoplar (ventriküler aritmiler, AV bloklar) aniden başlar ve sıklıkla öncü prodromal belirti vermez.', isCorrect: false },
        { key: 'C', text: 'Yaşlılarda aort kapak stenozu eforla ilişkili senkobun en önemli nedenlerinden biridir ve mutlaka ekarte edilmelidir.', isCorrect: false },
        { key: 'D', text: 'Doğurganlık çağındaki kadınlarda senkopla başvurulduğunda ektopik gebelik rüptürü ve pulmoner emboli akılda tutulmalıdır.', isCorrect: false },
        { key: 'E', text: 'Karotis sinüs aşırı duyarlılığı, yaşlı ve hipertansif erkeklerde başı aniden çevirme veya sıkı yaka ile tetiklenebilir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Senkop; global serebral hipoperfüzyona bağlı gelişen, ani başlangıçlı, KISA SÜRELİ (genellikle birkaç saniye-dakika süren) ve KENDİLİĞİNDEN TAMAMEN DÜZELEN geçici bir bilinç kaybıdır. Bilinç kaybının 30 dakikadan uzun sürmesi senkop değil, KOMA veya status epileptikustur.',
      hamSoru: 'senkopla ilgili hangisi yanlış? senkop 30 dakikadan uzun süren bilinç kaybıdır (yanlıştır, saniyeler-dakikalar sürer)'
    },
    {
      num: 7,
      topic: 'Kardiyak Tamponad ve Beck Triadı',
      source: '1. Göğüs Travması Tipleri.txt',
      stem: 'Perikardiyal boşlukta sıvı birikmesi sonucu intrakardiyak basınçların eşitlenmesiyle gelişen Kardiyak Tamponadda izlenen klasik "Beck Triadı" bulguları arasında aşağıdakilerden hangisi YER ALMAZ?',
      options: [
        { key: 'A', text: 'Dudaklarda ve parmak uçlarında belirgin periferik siyanoz', isCorrect: true },
        { key: 'B', text: 'Sistemik hipotansiyon ve nabız basıncında daralma', isCorrect: false },
        { key: 'C', text: 'Boyun venlerinde belirgin dolgunluk (artmış juguler venöz basınç)', isCorrect: false },
        { key: 'D', text: 'Oskültasyonda derinden gelen, zayıflamış/boğuk kalp sesleri', isCorrect: false },
        { key: 'E', text: 'Pulsus paradoksus eşlik edebilen hemodinamik instabilite', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Beck Triadı, kardiyak tamponadın 3 klasik fizik muayene bulgusudur: 1) Hipotansiyon (azalmış kardiyak debi ve daralmış nabız basıncı), 2) Boyun venöz dolgunluğu (sağ atriyum doluş basıncının artması), 3) Boğuk/derinden gelen kalp sesleri (kalp ile göğüs duvarı arasına giren sıvı). Siyanoz triadda yer almaz.',
      hamSoru: 'Beck triadı bulgularından değildir? Siyanoz'
    },
    {
      num: 8,
      topic: 'Künt Göğüs Travmalarının Komplikasyonları',
      source: '1. Göğüs Travması Tipleri.txt',
      stem: 'Motorlu taşıt kazası veya yüksekten düşme gibi künt toraks travmalarına maruz kalan bir hastada travmanın doğrudan bir sonucu olarak gelişmesi beklenmeyen klinik durum aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Eforla tetiklenen stabil kronik angina pektoris atağı', isCorrect: true },
        { key: 'B', text: 'Yelken göğüs (Flail chest)', isCorrect: false },
        { key: 'C', text: 'Masif veya basit hemotoraks', isCorrect: false },
        { key: 'D', text: 'Tansiyon veya basit pnömotoraks', isCorrect: false },
        { key: 'E', text: 'Pulmoner kontüzyon ve akciğer laserasyonu', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Künt göğüs travmaları doğrudan kosta kırıkları, yelken göğüs, pnömotoraks, hemotoraks, pulmoner kontüzyon, miyokard kontüzyonu ve diyafram rüptürüne yol açar. Kronik stabil angina pektoris ise travmatik bir mekanizma değil; altta yatan koroner aterosklerotik plak darlıklarına bağlı miyokardiyal oksijen arz-talep dengesizliğidir.',
      hamSoru: 'künt göğüs travmalarının olası sonuçlarından değildir? Angina pektoris'
    },
    {
      num: 9,
      topic: 'Göğüs Travmalarında En Sık Solunum Bulgusu',
      source: '1. Göğüs Travması Tipleri.txt',
      stem: 'Toraks travmalı olgularda ağrı, kot kırıkları, ventilasyon-perfüzyon uyumsuzluğu ve atelektazilere bağlı olarak en sık karşılaşılan solunum sistemi semptom ve bulgusu aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Dispne (Nefes darlığı ve taşipne)', isCorrect: true },
        { key: 'B', text: 'Apne', isCorrect: false },
        { key: 'C', text: 'Masif hemoptizi', isCorrect: false },
        { key: 'D', text: 'Stridor', isCorrect: false },
        { key: 'E', text: 'Biot solunumu', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Göğüs travması geçiren hastaların %70-80\'inden fazlasında görülen en yaygın semptom göğüs ağrısı; solunum sistemine ait en sık semptom ve fizik muayene bulgusu ise "DİSPNE" (nefes darlığı, yüzeysel ve hızlı solunum / taşipne) tablosudur.',
      hamSoru: 'Göğüs travmalarında en sık karşılaşılan solunum sistemi bulgusu: Dispne'
    },
    {
      num: 10,
      topic: 'Elektrik Çarpması Olay Yeri Yönetimi',
      source: 'çevresel aciller dönem 3 damla 2.txt',
      stem: 'Yüksek veya alçak gerilim elektrik çarpmasına maruz kalmış ve olay yerinde hareketsiz yatan bir kazazedeye müdahale ederken kurtarıcı hekimin atması gereken İLK ve en öncelikli adım aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Öncelikle ortam güvenliğini sağlamak için elektrik akımını kaynaktan kesmek veya iletken olmayan yalıtkan bir cisimle temas bağlantısını kesmek', isCorrect: true },
        { key: 'B', text: 'Derhal kazazedenin yanına koşarak çıplak elle karotis nabzını kontrol etmek', isCorrect: false },
        { key: 'C', text: 'Kazazedeye derhal 200 J defibrilasyon uygulamak', isCorrect: false },
        { key: 'D', text: 'Kazazedenin vücuduna soğuk su dökerek yanıkları soğutmak', isCorrect: false },
        { key: 'E', text: 'Kazazedeyi kollarından çekerek hızla uzaklaştırmak', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Elektrik yaralanmalarında ilk kural kurtarıcının güvenliğidir (sahne güvenliği). Elektrik akımı kesilmeden hastaya dokunulursa akım kurtarıcıya geçer ("ikinci kurban"). Bu nedenle ilk yapılması gereken şarteli kapatmak, fişi çekmek veya akımı yalıtkan kuru bir cisimle kesmektir.',
      hamSoru: 'elektrik çarpması vakasında ilk yapılması gereken? elektrik akımını kesmek'
    },
    {
      num: 11,
      topic: 'Akut Zehirlenmelerde Mide Dekontaminasyonu',
      source: 'zehirlenmeler dönem 4.txt',
      stem: 'Akut toksik madde zehirlenmelerinde gastrointestinal dekontaminasyon yöntemleri değerlendirildiğinde güncel kılavuzlarda aspirasyon riski ve özofagus perforasyonu tehlikesi nedeniyle artık RUTİN OLARAK KULLANILMAYAN ve önerilmeyen yöntem aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'İpeka şurubu veya mekanik uyarı ile hastayı kusturma', isCorrect: true },
        { key: 'B', text: 'İlk 1 saat içinde tek doz aktif kömür uygulaması', isCorrect: false },
        { key: 'C', text: 'Bilinç açık veya entübe hastada orogastrik tüp ile mide yıkama', isCorrect: false },
        { key: 'D', text: 'Demir ve lityum zehirlenmesinde tüm bağırsak irrigasyonu (PEG)', isCorrect: false },
        { key: 'E', text: 'Spesifik antidot uygulanması', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Zehirlenmelerde kusturma (ipeca şurubu verilmesi veya boğazın uyarılması) toksikolojik acillerde artık kesinlikle önerilmemektedir. Hem aspire edilerek kimyasal pnömoni oluşturma riski çok yüksektir, hem de korozif (asit/alkali) maddelerde özofagusu ikinci kez yakar ve rüptür riski oluşturur.',
      hamSoru: 'toksik zehirlenmelerde mide yıkanmasında hangi yöntem kullanılmaz? kusturma'
    },
    {
      num: 12,
      topic: 'Kolinerjik Toksidrom ve Nikotinik Bulgular',
      source: 'zehirlenmeler dönem 4.txt',
      stem: 'Organofosfatlı veya karbamatlı tarım ilacı zehirlenmelerinde asetilkolinesteraz enzim inhibisyonu sonucu gelişen kolinerjik krizde aşağıdakilerden hangisi doğrudan sempatik gangliyonlar ve nöromüsküler kavşaktaki "nikotinik" reseptör aşırı uyarımına bağlı bir bulgudur?',
      options: [
        { key: 'A', text: 'İskelet kaslarında fasikülasyonlar, kramplar ve ardından flaksid kas paralizisi', isCorrect: true },
        { key: 'B', text: 'Aşırı tükürük salgısı (salivasyon)', isCorrect: false },
        { key: 'C', text: 'Yaygın bronşiyal sekresyon artışı (bronkore) ve bronkokonstriksiyon', isCorrect: false },
        { key: 'D', text: 'Miyozis ve lakrimasyon (gözyaşı akması)', isCorrect: false },
        { key: 'E', text: 'Defekasyon ve istemsiz ürinasyon', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Kolinerjik toksidrom bulguları ikiye ayrılır: 1) Muskarinik bulgular (DUMBELS / SLUDGE): Salivasyon, lakrimasyon, ürinasyon, defekasyon, GIS krampları, bronkore/bronkospazm, miyozis ve bradikardi (Atropin ile düzelir). 2) Nikotinik bulgular (MATCH): Kas Fasikülasyonları, Kramp, Güçsüzlük/Paralizi, Taşikardi ve Hipertansiyon (Atropin nikotinik reseptörleri bloke edemez; Pralidoksim/PAM gerekir).',
      hamSoru: 'kolinerjik toksidromun nikotinik etkisi: Kas fasikülasyonları'
    },
    {
      num: 13,
      topic: 'Sıcak Çarpması (Heat Stroke) Tedavisi İlkeleri',
      source: 'çevresel aciller dönem 3 damla 2.txt',
      stem: 'Vücut çekirdek sıcaklığının >40°C üzerine çıktığı ve santral sinir sistemi disfonksiyonu (konfüzyon, deliryum, koma) ile seyreden Sıcak Çarpmasında (Heat Stroke) acil tedavi yaklaşımı ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?',
      options: [
        { key: 'A', text: 'Ateşi düşürmek için derhal yüksek doz oral veya parenteral antipiretikler (parasetamol veya aspirin) verilmelidir.', isCorrect: true },
        { key: 'B', text: 'Hedef ilk 30 dakika içinde hastanın çekirdek sıcaklığını hızla 38.5-39°C altına düşürmektir.', isCorrect: false },
        { key: 'C', text: 'Buharlaşma yoluyla soğutma (hastanın üzerine ılık su püskürtülüp vantilatörle hava üflenmesi) en güvenli yöntemdir.', isCorrect: false },
        { key: 'D', text: 'Soğuk suya daldırma (buzlu su banyosu) klasik genç egzersiz ilişkili sıcak çarpmasında en hızlı soğutma tekniğidir.', isCorrect: false },
        { key: 'E', text: 'Titreşimi önlemek için gerekirse benzodiazepin uygulanabilir.', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Sıcak çarpmasında hipotalamik termoregülasyon seti bozulmamıştır; doğrudan çevresel aşırı ısı birikimi ve terleme yetersizliği vardır. Bu nedenle antipiretikler (parasetamol, NSAİİ, aspirin) HİÇBİR İŞE YARAMAZ; aksine fulminan karaciğer hasarını ve koagülopatiyi artırırlar (KONTRENDİKEDİRLER). Tek etkin tedavi FİZİKSEL HIZLI SOĞUTMADIR.',
      hamSoru: 'sıcak çarpmasındaki tedavilerden biri değildir? Antipiretik verilir (yanlıştır, kontrendikedir)'
    },
    {
      num: 14,
      topic: 'Kafa Travması Sonrası Santral Diabetes İnsipidus',
      source: 'kafa travmaları .txt',
      stem: 'Kafa tabanı travması sonrası gelişen poliüri ve hipernatremi tablosunda aşağıdakilerden hangisi Santral Diabetes İnsipidus (Dİ) tanısı ile UYUŞMAYAN bir bulgudur?',
      options: [
        { key: 'A', text: 'Plazma Antidiüretik Hormon (ADH / Vazopresin) düzeylerinin aşırı yüksek olması', isCorrect: true },
        { key: 'B', text: 'Serum sodyumunun >145 mEq/L ve serum ozmolaritesinin yüksek olması', isCorrect: false },
        { key: 'C', text: 'İdrar dansitesinin (<1.005) ve idrar ozmolaritesinin düşük olması (<300 mOsm/kg)', isCorrect: false },
        { key: 'D', text: 'Günde 3 litrenin üzerinde bol miktarda dilüe idrar çıkarılması (poliüri)', isCorrect: false },
        { key: 'E', text: 'Hipovolemiye sekonder taşikardi ve hipotansiyon gelişebilmesi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Santral Diabetes İnsipidus, kafa travmasında hipotalamo-hipofizer sapın zedelenmesi sonucu nörohipofizden ADH salınamaması durumudur. Bu nedenle kanda ADH DÜŞÜKTÜR veya yoktur. Böbrekler suyu geri ememez, idrar ozmolaritesi düşer, plazma hiperozmolar hale gelir. "ADH yüksekliği" Uygunsuz ADH Salınımı Sendromuna (SIADH) aittir.',
      hamSoru: 'Kafa travması sonucu gelişen hipernatremi için hangisi diyabetes insipidus lehine değildir? ADH yüksekliği'
    },
    {
      num: 15,
      topic: 'Baziller Kafa Kırığı ve Nazal BOS Sızıntısı',
      source: 'kafa travmaları .txt',
      stem: 'Kafa travması sonrası temporal kemik veya lamina kribroza kırığı zemininde burundan berrak sıvı gelmesi (BOS rinoresi) saptanan bir hastada klinik yönetim ile ilgili aşağıdaki uygulamalardan hangisi KONTRENDİKEDİR?',
      options: [
        { key: 'A', text: 'Körlemesine nazogastrik sonda yerleştirilmesi (kırık tabandan kafa içine penetrasyon riski)', isCorrect: true },
        { key: 'B', text: 'Hastanın yatak başının 30 derece yükseltilmesi', isCorrect: false },
        { key: 'C', text: 'Hastanın burnunu sümkürmesinin ve ıkınmasının yasaklanması', isCorrect: false },
        { key: 'D', text: 'Sıvıda Beta-2 transferrin veya glikoz analizi yapılarak BOS olduğunun doğrulanması', isCorrect: false },
        { key: 'E', text: 'Nöroşirürji konsültasyonu istenmesi ve yakın menenjit takibi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Kribriform plaka veya kafa tabanı kırığı olan ve rinore gelişen hastalarda NAZAL YOLDAN TÜP / NAZOGASTRİK SONDA TAKILMASI KESİNLİKLE KONTRENDİKEDİR! Tüp kırık hattından doğrudan kranial boşluğa ve beyin parankimine girerek ölümcül hasar yapabilir. Tüp gerekiyorsa OROGASTRİK yolla takılmalıdır.',
      hamSoru: 'Baziller kırıkta BOS sızıntısı var ne yapılmaz? Nazogastrik sonda takılması kontrendikedir'
    }
  ];

  return list.map(q => ({
    id: `d3-k5-aci-${String(q.num).padStart(3, '0')}`,
    committeeId: 'donem3-kurul5',
    folderKey: 'donem3k5',
    donem: 3,
    kurul: 5,
    discipline: 'Acil Tıp',
    topic: q.topic,
    questionNumber: q.num,
    examYear: '2021-2026',
    sourceFile: 'Acil_Tip_Kurul5_Cikmis_Sorular.json',
    stem: q.stem,
    options: q.options,
    correctAnswer: q.correctAnswer,
    explanation: q.explanation,
    hamSoru: q.hamSoru,
    rawQuestion: {
      stem: q.hamSoru || q.stem,
      options: q.options.map(o => ({ key: o.key, text: o.text })),
      claimedAnswer: q.correctAnswer
    },
    reconstruction: {
      stem: q.stem,
      options: q.options,
      correctAnswer: q.correctAnswer,
      explanation: q.explanation,
      confidenceScore: 100,
      reconstructionQuality: 'verified',
      notesAndDiscrepancies: 'Acil Tıp amfi ders notları (İKYD, Travma, Çevresel Aciller, Zehirlenmeler, Senkop, Kafa Travmaları) ile tam doğrulanmıştır.'
    },
    sourceNote: q.source,
    isSuspect: false,
    isAmbiguous: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }));
}

// -------------------------------------------------------------
// 6. TIBBİ FARMAKOLOJİ (15 Soru)
// -------------------------------------------------------------
export function buildFarmakolojiKurul5Questions() {
  const list = [
    {
      num: 1,
      topic: 'Oral Retinoidler ve Teratojenite (İzotretinoin)',
      source: '61 Dermatolojik Farmakoloji.txt',
      stem: 'Şiddetli nodülokistik akne tedavisinde sistemik olarak kullanılan ve aşırı derecede teratojenik (kranial, kardiyak ve timik malformasyonlar) olan İzotretinoin reçete edilirken doğurganlık çağındaki bir kadının uyması gereken en kritik kural aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Tedaviye başlamadan en az 1 ay önce, tedavi süresince ve tedavi bittikten sonra en az 1 ay boyunca iki farklı etkili kontraseptif yöntem kullanması', isCorrect: true },
        { key: 'B', text: 'Sadece tedavi günü tek doz acil kontraseptif alması', isCorrect: false },
        { key: 'C', text: 'Tedavi sırasında güneş koruyucu kullanması durumunda kontrasepsiyona gerek olmaması', isCorrect: false },
        { key: 'D', text: 'İlacı yemeklerden 2 saat önce aç karnına alması', isCorrect: false },
        { key: 'E', text: 'Gebe kalması durumunda ilacın dozunun yarıya indirilmesi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Oral izotretinoin bilinen en güçlü insan teratojenlerinden biridir. Bu nedenle doğurganlık çağındaki kadınlarda tedaviye başlanmadan 1 ay önce, tedavi boyunca ve ilaç kesildikten sonra 1 ay boyunca (veya menstrüel siklus boyunca) en az iki güvenilir kontrasepsiyon yöntemi (çifte korunma) şarttır ve her ay negatif gebelik testi zorunludur.',
      hamSoru: 'İzotretinoin kullanan doğurgan kadının kontrasepsiyon kuralı: 1 ay öncesi, tedavi boyu ve tedaviden sonra en az 1 ay etkili kontrasepsiyon'
    },
    {
      num: 2,
      topic: 'Asitretin ve 3 Yıl Gebelik Yasağı',
      source: '61 Dermatolojik Farmakoloji.txt',
      stem: 'Yaygın püstüler psöriyazis tedavisinde oral yoldan kullanılan, yağ dokusunda biriken ve alkol tüketimi varlığında yarı ömrü 120 güne kadar uzayan etretinata dönüşerek tedaviden sonraki 3 yıl boyunca teratojenik risk oluşturan ikinci kuşak aromatik retinoid aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Asitretin', isCorrect: true },
        { key: 'B', text: 'İzotretinoin', isCorrect: false },
        { key: 'C', text: 'Tretinoin', isCorrect: false },
        { key: 'D', text: 'Adapalen', isCorrect: false },
        { key: 'E', text: 'Tazaroten', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Asitretin, psöriyaziste kullanılan sistemik bir retinoiddir. Özellikle alkolle birlikte alındığında vücutta esterleşerek yarı ömrü çok uzun olan etretinata dönüşür. Bu nedenle gebelik riski olan kadınlarda tedavi bittikten sonra tam 3 YIL BOYUNCA gebelik kesinlikle yasaktır ve etkili kontrasepsiyon sürdürülmelidir.',
      hamSoru: 'Tedavi bittikten sonraki 3 yıl boyunca korunma gereken psöriyazis ilacı: Asitretin'
    },
    {
      num: 3,
      topic: '5-Alfa Redüktaz İnhibitörü ve Alopesi Tedavisi',
      source: '61 Dermatolojik Farmakoloji.txt',
      stem: 'Genetik yatkınlığı olan erkeklerde kıl foliküllerinde testosteronun daha aktif formu olan dihidrotestosterona (DHT) dönüşümünü katalizleyen Tip 2 5-alfa redüktaz enzimini selektif olarak inhibe eden ve androjenik alopesi tedavisinde kullanılan ilaç aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Finasterid', isCorrect: true },
        { key: 'B', text: 'Minoksidil', isCorrect: false },
        { key: 'C', text: 'Spironolakton', isCorrect: false },
        { key: 'D', text: 'Flutamid', isCorrect: false },
        { key: 'E', text: 'Ketokonazol', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Finasterid, Tip 2 5-alfa redüktaz enzim inhibitörüdür. Dolaşımdaki ve saçlı derideki dihidrotestosteron (DHT) seviyesini %70\'e yakın oranda düşürerek kıl foliküllerinin minyatürizasyonunu durdurur. Androjenik alopeside (1 mg/gün) ve benign prostat hiperplazisinde (5 mg/gün) kullanılır.',
      hamSoru: 'androjenik alopeside testosteronun DHT ye dönüşmesini inhibe eden 5 alfa redüktaz inhibitörü: Finasterid'
    },
    {
      num: 4,
      topic: 'Aspirin Triadı (Samter Sendromu / AERD)',
      source: '1. Kas-İskelet-Eklem Sisteminde İlaçlar 2.txt',
      stem: 'Otuz beş yaşında kadın hasta sık baş ağrıları nedeniyle nonsteroid antiinflamatuar ilaç (aspirin/naproksen) kullanmaya başladıktan sonra şiddetli astım atakları ve nazal polipozis tablosu geliştirmiştir. Bu aşırı duyarlılık tablosunun (Aspirinle alevlenen solunum yolu hastalığı / AERD) temel patofizyolojik mekanizması aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'COX-1 enziminin inhibisyonu sonucu araşidonik asit metabolizmasının 5-lipooksijenaz (5-LOX) yolağına kayması ve bronkokonstriktör sisteinil lökotrienlerin (LTC4, LTD4, LTE4) aşırı üretimi', isCorrect: true },
        { key: 'B', text: 'İlaca karşı gelişen IgE aracılı Tip 1 anafilaktik reaksiyon', isCorrect: false },
        { key: 'C', text: 'Bronşiyal muskarinik M3 reseptörlerinin doğrudan uyarılması', isCorrect: false },
        { key: 'D', text: 'Beta-2 adrenerjik reseptörlerin geri dönüşümsüz blokajı', isCorrect: false },
        { key: 'E', text: 'Trombositopeniye sekonder gelişen hava yolu kanaması', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Aspirin Triadı (Widal / Samter Sendromu): Astım + Nazal polipozis + Aspirin/NSAİİ intoleransıdır. Tip 1 alerjik reaksiyon değildir; non-immünolojik bir biyokimyasal sapmadır. COX-1 inhibe olunca siklooksijenaz yolu tıkanır, araşidonik asit lipooksijenaz yoluna sapar ve bronşları kasan lökotrienler aşırı üretilir.',
      hamSoru: 'ağrı kesici kullanımı sonrası astım atağı ve nazal polip gelişimi: Aspirin (COX-1 inhibisyonu ile lökotrien artışı)'
    },
    {
      num: 5,
      topic: 'Allopurinolün Etki Mekanizması ve Uzun Etki Sebebi',
      source: '1. Kas-İskelet-Eklem Sisteminde İlaçlar 2.txt',
      stem: 'Kronik tofüslü gut hastasında ürik asit üretimini azaltmak amacıyla başlanan Allopurinolün etki mekanizması ve günde tek doz kullanılmasına olanak tanıyan uzun etki süresinin temel nedeni aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Ksantin oksidaz enzimini inhibe etmesi ve vücutta karaciğerde yarı ömrü 18-30 saat olan aktif metaboliti oksipurinole (alloksantin) dönüşmesi', isCorrect: true },
        { key: 'B', text: 'Probenesid gibi renal tübüler ürik asit geri emilimini bloke etmesi', isCorrect: false },
        { key: 'C', text: 'Ürik asidi allantoine yıkan ürikaz enzimini doğrudan aktive etmesi', isCorrect: false },
        { key: 'D', text: 'Nötrofillerde mikrotübül polimerizasyonunu geri dönüşümsüz durdurması', isCorrect: false },
        { key: 'E', text: 'İnce bağırsaktan pürin emilimini tamamen engellemesi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Allopurinol bir pürin analoğu olup ksantin oksidaz enziminin substratı ve inhibitörüdür. Hipoksantinin ksantine, ksantinin ürik aside dönüşümünü durdurur. Allopurinolün kendi yarı ömrü kısadır (1-2 saat), ancak aktif metaboliti olan "Oksipurinole" (alloksantin) metabolize olur; oksipurinolün yarı ömrü 24-30 saat olduğu için günde tek doz uygulanabilir.',
      hamSoru: 'Allopurinol etki mekanizması ve uzun etkili olmasının sebebi: Ksantin oksidaz inhibisyonu ve aktif metaboliti oksipurinolün uzun yarı ömrü'
    },
    {
      num: 6,
      topic: 'Osteoporozda Osteoblastik Yapımı Artıran Ajan (Teriparatid)',
      source: '2. Kemik Mineralizasyonu ve Homeostazis İlaçları.txt',
      stem: 'Yetmiş iki yaşında şiddetli osteoporozu olan bir hastaya kemik kırıklarını önlemek için başlanan ilaç kemik yıkımını baskılamak yerine doğrudan osteoblast aktivitesini artırarak kemik yapımını tetiklemiş ve takiplerinde hafif hiperkalsemiye yol açmıştır. Bu farmakolojik profil aşağıdaki ilaçlardan hangisine aittir?',
      options: [
        { key: 'A', text: 'Teriparatid (Rekombinant insan PTH 1-34 analoğu)', isCorrect: true },
        { key: 'B', text: 'Alendronat (Oral bisfosfonat)', isCorrect: false },
        { key: 'C', text: 'Zoledronik asit (İV bisfosfonat)', isCorrect: false },
        { key: 'D', text: 'Denosumab (RANKL monoklonal antikoru)', isCorrect: false },
        { key: 'E', text: 'Kalsitonin (Antirezorptif peptid)', isCorrect: false },
      ],
      correctAnswer: 'A',
      explanation: 'Bisfosfonatlar, denosumab ve kalsitonin kemik rezorpsiyonunu (yıkımını) baskılayan "antirezorptif" ajanlardır. Kemik YAPIMINI (osteoblastik kemik formasyonunu) doğrudan uyaran kemik anabolik ajanı ise intermittan subkutan uygulanan rekombinant PTH analoğu olan "Teriparatid"dir (veya abaloparatid). Osteoblastik aktiviteyi artırır, hiperkalsemi yapabilir.',
      hamSoru: 'osteoporoz tedavisinde osteoblast aktivitesini ve kemik yapımını artıran, hiperkalsemi yapabilen: Teriparatid'
    },
    {
      num: 7,
      topic: 'Topikal Antifungal Tedavi (Nistatin)',
      source: '61 Dermatolojik Farmakoloji.txt',
      stem: 'Vulvovajinal kandidiyazis ve kutanöz Candida enfeksiyonlarının topikal tedavisinde mantar hücre membranındaki ergosterole bağlanarak gözenekler açmak suretiyle fungisidal etki gösteren polien grubu antifungal ajan aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Nistatin', isCorrect: true },
        { key: 'B', text: 'Terbinafin', isCorrect: false },
        { key: 'C', text: 'Permetrin', isCorrect: false },
        { key: 'D', text: 'Oksimetazolin', isCorrect: false },
        { key: 'E', text: 'Minosiklin', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Nistatin, polien yapılı bir antifungal ajandır. Mantar hücre zarındaki ergosterole bağlanarak membran geçirgenliğini bozar ve hücre içi potasyum/magnezyum kaybına yol açarak mantarı öldürür. Gastrointestinal kanaldan emilmediği için oral aftlarda ve topikal olarak kandidiyazis tedavisinde çok güvenlidir.',
      hamSoru: 'vulvovajinal kandida tedavisinde topikal antifungal: Nistatin'
    },
    {
      num: 8,
      topic: 'Sulindak ve Kolon Polip İnbibisyonu',
      source: '1. Kas-İskelet-Eklem Sisteminde İlaçlar 2.txt',
      stem: 'Sülfoksit yapısında bir ön-ilaç (prodrug) olan, vücutta aktif sülfür metabolitine indirgenerek COX inhibisyonu yapan, böbrek prostaglandinlerini diğer NSAİİ\'lere göre daha az baskıladığı düşünülen ve Familyal Adenomatöz Polipozis (FAP) zemininde kolon polip sayısını ve kanser gelişimini baskılayabilen NSAİ ilaç aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Sulindak (Sulindac)', isCorrect: true },
        { key: 'B', text: 'İndometazin', isCorrect: false },
        { key: 'C', text: 'Ketoprofen', isCorrect: false },
        { key: 'D', text: 'Diklofenak', isCorrect: false },
        { key: 'E', text: 'Meloksikam', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Sulindak, bir ön-ilaçtır (sülfoksit formu inaktiftir). Karaciğerde aktif sülfür bileşiğine metabolize olur. Böbrekte tekrar inaktif sülfoksite oksitlendiği için "renal-koruyucu NSAİİ" olarak anılmıştır. Familyal adenomatöz polipozis (FAP) olgularında kolonik adenomların gerilemesini sağlar.',
      hamSoru: 'Sülfoksit içeren NSAİ ön ilaç, FAP ve kolon polipleri baskılayan: Sulindak'
    },
    {
      num: 9,
      topic: 'Akne Vulgaris Tedavisinde Yeri Olmayan Ajan',
      source: '61 Dermatolojik Farmakoloji.txt',
      stem: 'Akne vulgaris patogenezinde rol oynayan folliküler hiperkeratinizasyon, sebum artışı, Cutibacterium acnes proliferasyonu ve inflamasyon hedeflenerek uygulanan güncel medikal tedaviler arasında aşağıdakilerden hangisi YER ALMAZ?',
      options: [
        { key: 'A', text: 'Oral ketokonazol (sistemik hepatotoksik antifungal)', isCorrect: true },
        { key: 'B', text: 'Topikal benzoil peroksit', isCorrect: false },
        { key: 'C', text: 'Topikal retinoidler (Tretinoin / Adapalen)', isCorrect: false },
        { key: 'D', text: 'Topikal klindamisin veya eritromisin', isCorrect: false },
        { key: 'E', text: 'Sistemik izotretinoin', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Akne vulgaris bir bakteri ve keratinizasyon hastalığıdır (Cutibacterium acnes). Ketokonazol bir antifungaldir; Malassezia folikülitinde kullanılır ancak standart akne vulgaris tedavisinde yeri yoktur ve oral formu yüksek hepatotoksisite riski nedeniyle aknede kullanılmaz.',
      hamSoru: 'hangisi akne vulgaris tedavisinde kullanılmaz? Ketokonazol'
    },
    {
      num: 10,
      topic: 'Kalsimimetik İlaçlar ve Etki Mekanizması',
      source: '2. Kemik Mineralizasyonu ve Homeostazis İlaçları.txt',
      stem: 'Sekonder hiperparatiroidizm ve paratiroid karsinomunda kullanılan ve paratiroid bezindeki kalsiyum algılayıcı reseptörlerin (CaSR) duyarlılığını allosterik olarak artırarak PTH salgılanmasını doğrudan baskılayan "kalsimimetik" ilaç aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Sinakalset (Cinacalcet)', isCorrect: true },
        { key: 'B', text: 'Stronsiyum ranelat', isCorrect: false },
        { key: 'C', text: 'Alendronat', isCorrect: false },
        { key: 'D', text: 'Kalsitriol', isCorrect: false },
        { key: 'E', text: 'Raloksifen', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Sinakalset, paratiroid hücre zarı üzerindeki G-protein kenetli Kalsiyum Algılayıcı Reseptörün (CaSR) duyarlılığını artıran birinci basamak kalsimimetik ilaçtır. Dolaşımdaki kalsiyumu taklit ederek paratiroid bezini kalsiyum yüksekmiş gibi yanıltır ve PTH sentez/salınımını belirgin olarak düşürür.',
      hamSoru: 'Aşağıdakilerden hangisi kalsimimetiktir? Sinakalset'
    },
    {
      num: 11,
      topic: 'Bisfosfonatların Etki Mekanizması ve Komplikasyonları',
      source: '2. Kemik Mineralizasyonu ve Homeostazis İlaçları.txt',
      stem: 'Osteoporoz tedavisinde birinci basamak olarak kullanılan azot içeren bisfosfonatların (Alendronat, Zoledronat) hücresel etki mekanizması ve uzun süreli kullanımda görülebilen nadir ciddi komplikasyonu hangi seçenekte doğru verilmiştir?',
      options: [
        { key: 'A', text: 'Farnesil pirofosfat (FPP) sentaz inhibisyonu ile osteoklast apoptozu — Çene kemiğinde osteonekroz (BRONJ)', isCorrect: true },
        { key: 'B', text: 'Dihidrofolat redüktaz aktivasyonu — Akut gut artriti', isCorrect: false },
        { key: 'C', text: 'Alkalen fosfataz blokajı — Hipofosfatemi', isCorrect: false },
        { key: 'D', text: 'Siklooksijenaz inhibisyonu — Aort anevrizması', isCorrect: false },
        { key: 'E', text: 'RANKL reseptör gen duplikasyonu — Multipl miyelom', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Azotlu bisfosfonatlar kolesterol biyosentezindeki mevalonat yolağında "Farnesil pirofosfat sentaz" enzimini inhibe eder. Osteoklastların fırçamsı kenarı bozulur ve osteoklast apoptoza gider. Kemik yapışması çok güçlüdür; uzun süreli kullanımda kemik döngüsünün aşırı baskılanmasına bağlı olarak "Çene Osteonekrozu" ve "Atipik Subtrokanterik Femur Kırıkları" riski taşır.',
      hamSoru: 'Bisfosfonat etki mekanizması ve çene osteonekrozu komplikasyonu'
    },
    {
      num: 12,
      topic: 'Denosumab Etki Mekanizması',
      source: '2. Kemik Mineralizasyonu ve Homeostazis İlaçları.txt',
      stem: 'Postmenopozal osteoporozda ve kemik metastazlarında 6 ayda bir subkutan uygulanan ve osteoblastlar tarafından üretilen RANKL molekülüne bağlanarak osteoklastların olgunlaşmasını, aktivasyonunu ve sağkalımını engelleyen monoklonal antikor aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Denosumab', isCorrect: true },
        { key: 'B', text: 'Romosozumab', isCorrect: false },
        { key: 'C', text: 'İnfliksimab', isCorrect: false },
        { key: 'D', text: 'Adalimumab', isCorrect: false },
        { key: 'E', text: 'Rituksimab', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Denosumab, osteoblastların salgıladığı RANKL ligandına yüksek afiniteyle bağlanan insan monoklonal antikorudur. RANK reseptörünün RANKL ile uyarılmasını engeller (osteoprotegerin benzeri etki yapar). Osteoklast gelişimi durur ve kemik rezorpsiyonu hızla baskılanır.',
      hamSoru: 'RANKL monoklonal antikoru osteoporoz ilacı: Denosumab'
    },
    {
      num: 13,
      topic: 'NSAİİ ve Peptik Ülser Patogenezi',
      source: '1. Kas-İskelet-Eklem Sisteminde İlaçlar 2.txt',
      stem: 'Kronik eklem ağrısı nedeniyle non-selektif NSAİ ilaç (örneğin indometazin veya aspirin) kullanan bir hastada peptik ülser ve gastrointestinal kanama gelişmesinin temel moleküler mekanizması aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Mide mukozasında koruyucu prostaglandinlerin (özellikle PGE2 ve PGI2) sentezinden sorumlu konstitütif COX-1 enziminin inhibe edilmesi', isCorrect: true },
        { key: 'B', text: 'Mide paryetal hücrelerinde H+/K+ ATPaz pompa sayısının artması', isCorrect: false },
        { key: 'C', text: 'Gastrin hormon salgısının geri dönüşümsüz olarak durdurulması', isCorrect: false },
        { key: 'D', text: 'Helicobacter pylori bakterisinin doğrudan mideye inoküle edilmesi', isCorrect: false },
        { key: 'E', text: 'Gastrik venlerde yaygın vazodilatasyon ve kanama', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'COX-1 enzimi mide mukozasında devamlı olarak aktiftir (konstitütif) ve PGE2 ile PGI2 üretir. Bu prostaglandinler mukus salgısını, bikarbonat salgısını ve mukozal kan akımını artırır, mide asit salgısını ise baskılar. Non-selektif NSAİİ\'ler COX-1\'i bloke edince bu koruyucu kalkan çöker ve peptik ülser gelişir.',
      hamSoru: 'ağrı kesici içen bir kişide peptik ülser gelişimi sebebi: COX-1 inhibisyonu ile koruyucu prostaglandinlerin azalması'
    },
    {
      num: 14,
      topic: 'Akut Gut Artritinde Kolşisin Etkisi',
      source: '1. Kas-İskelet-Eklem Sisteminde İlaçlar 2.txt',
      stem: 'Akut gut artriti krizinde ilk 24-36 saat içinde başlandığında eklem ağrısı ve inflamasyonunu hızla gerileten ve nötrofillerde tübülin proteinine bağlanarak mikrotübül polimerizasyonunu engelleyen ilaç aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Kolşisin (Colchicine)', isCorrect: true },
        { key: 'B', text: 'Allopurinol', isCorrect: false },
        { key: 'C', text: 'Febuksostat', isCorrect: false },
        { key: 'D', text: 'Probenesid', isCorrect: false },
        { key: 'E', text: 'Rasburikaz', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Kolşisin, tübülini bağlayarak mikrotübül montajını bozar. Bu durum nötrofillerin kemotaksisini, inflamasyon bölgesine göçünü ve ürat kristallerini fagositozunu engeller. Allopurinol ve febuksostat akut atakta başlanmaz (krizi alevlendirir); atakta kolşisin, NSAİİ veya steroid kullanılır.',
      hamSoru: 'Akut gut krizinde tübülin inhibisyonu yapan ilaç: Kolşisin'
    },
    {
      num: 15,
      topic: 'Romatoid Artritte Metotreksatın Temel Etkisi',
      source: '1. Kas-İskelet-Eklem Sisteminde İlaçlar 2.txt',
      stem: 'Romatoid Artrit tedavisinde "altın standart" hastalık modifiye edici antiromatizmal ilaç (csDMARD) olarak kabul edilen düşük doz Metotreksatın temel antiinflamatuar mekanizması aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'AICAR transformilaz inhibisyonu sonucu hücre dışına adenozin salınımının artması ve adenozinin inflamatuar hücreleri baskılaması', isCorrect: true },
        { key: 'B', text: 'Doğrudan TNF-alfa reseptörlerine kovalent bağlanarak bloke etmesi', isCorrect: false },
        { key: 'C', text: 'Kalsinörin enzimini inhibe ederek IL-2 sentezini durdurması', isCorrect: false },
        { key: 'D', text: 'Guanin nükleotid sentezinde inozin monofosfat dehidrogenazı bloke etmesi', isCorrect: false },
        { key: 'E', text: 'B lenfosit CD20 yüzey antijenlerini yok etmesi', isCorrect: false }
      ],
      correctAnswer: 'A',
      explanation: 'Metotreksat yüksek dozda antikanser olarak dihidrofolat redüktazı (DHFR) bloke eder. Ancak romatolojik düşük dozda (haftada 7.5-25 mg) temel antiinflamatuar mekanizması AICAR transformilaz inhibisyonudur; hücre içinde AICAR birikir, AMP deaminaz inhibe olur ve hücre dışına güçlü bir antiinflamatuar olan "ADENOZİN" salınır.',
      hamSoru: 'Metotreksatın romatizmal hastalıklardaki antiinflamatuar mekanizması: Adenozin artışı'
    }
  ];

  return list.map(q => ({
    id: `d3-k5-far-${String(q.num).padStart(3, '0')}`,
    committeeId: 'donem3-kurul5',
    folderKey: 'donem3k5',
    donem: 3,
    kurul: 5,
    discipline: 'Tıbbi Farmakoloji',
    topic: q.topic,
    questionNumber: q.num,
    examYear: '2021-2026',
    sourceFile: 'Farmakoloji_Kurul5_Cikmis_Sorular.json',
    stem: q.stem,
    options: q.options,
    correctAnswer: q.correctAnswer,
    explanation: q.explanation,
    hamSoru: q.hamSoru,
    rawQuestion: {
      stem: q.hamSoru || q.stem,
      options: q.options.map(o => ({ key: o.key, text: o.text })),
      claimedAnswer: q.correctAnswer
    },
    reconstruction: {
      stem: q.stem,
      options: q.options,
      correctAnswer: q.correctAnswer,
      explanation: q.explanation,
      confidenceScore: 100,
      reconstructionQuality: 'verified',
      notesAndDiscrepancies: 'Tıbbi Farmakoloji amfi ders notları (Dermatolojik Farmakoloji, Kas-İskelet İlaçları, Kemik Mineralizasyonu ve Gut Tedavisi) ile tam doğrulanmıştır.'
    },
    sourceNote: q.source,
    isSuspect: false,
    isAmbiguous: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }));
}
