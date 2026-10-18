import type { MechanismPathway } from '../../types/pathway';

export const ARACHIDONIC_ACID_PATHWAY: MechanismPathway = {
  id: 'arasidonik-asit-ve-eikozanoid-yolagi',
  title: 'Araşidonik Asit Yolağı ve Eikozanoid Sentezi',
  subtitle: 'Fosfolipaz A2, Siklooksijenaz (COX), Lipooksijenaz (LOX) ve Farmakolojik İnhibitörler',
  discipline: 'Tıbbi Patoloji & Farmakoloji',
  summary: 'Hücre zarındaki fosfolipidlerin araşidonik aside ve ardından prostaglandin, tromboksan ile lökotriyenlere dönüşümünü, inflamasyon kaskadını ve ilaçların (Steroidler, NSAİİ, Zileuton) etki mekanizmalarını adım adım açıklar.',
  nodes: [
    // Seviye 1: Membran ve Substrat
    {
      id: 'membrane_phospholipids',
      label: 'Membran Fosfolipidleri',
      sublabel: 'Fosfatidilinozitol / Kolin',
      type: 'substrate',
      x: 50,
      y: 8,
      badge: 'Zar Lipidleri',
      tooltip: 'Hücre hasarı, mekanik travma veya kimyasal uyaranlarla aktive olan fosfolipit çift katmanı.',
    },
    // Seviye 2: Enzim ve Düzenleyiciler
    {
      id: 'pla2',
      label: 'Fosfolipaz A2 (PLA2)',
      sublabel: 'Hız kısıtlayıcı kilit enzim',
      type: 'enzyme',
      x: 50,
      y: 22,
      badge: 'Enzim',
      tooltip: 'Zar fosfolipidlerinden araşidonik asidi serbestleştiren primer enzimdir.',
    },
    {
      id: 'corticosteroids',
      label: 'Kortikosteroidler',
      sublabel: 'Anneksin-1 (Lipokortin) sentezi',
      type: 'drug_inhibitor',
      x: 82,
      y: 18,
      badge: '(-) Güçlü İnhibitör',
      tooltip: 'Lipokortin (Anneksin A1) sentezini indükleyerek PLA2 aktivitesini en baştan bloke ederler.',
    },
    {
      id: 'stimulators',
      label: 'Bradikinin / Trombin / Ang II',
      sublabel: 'Hücre hasarı ve mediyatörler',
      type: 'drug_activator',
      x: 18,
      y: 18,
      badge: '(+) Aktivasyon',
      tooltip: 'Hücre yüzey reseptörlerini uyararak hücre içi kalsiyumu artırır ve PLA2 enzimini tetikler.',
    },
    // Seviye 3: Ana Metabolit (Merkez)
    {
      id: 'arachidonic_acid',
      label: 'Araşidonik Asit',
      sublabel: '20 Karbonlu Çoklu Doymamış Yağ Asidi',
      type: 'intermediate',
      x: 50,
      y: 36,
      badge: 'Kavşak Noktası',
      tooltip: 'Eikozanoid sentezinin ortak öncülüdür; COX ve LOX kollarına ayrılır.',
    },
    // Sol Dal: 5-LOX ve Lökotriyenler
    {
      id: 'lox_enzyme',
      label: '5-Lipooksijenaz (5-LOX)',
      sublabel: 'Nötrofil / Eozinofil enzimi',
      type: 'enzyme',
      x: 22,
      y: 52,
      badge: 'Lökotriyen Yolağı',
    },
    {
      id: 'zileuton',
      label: 'Zileuton',
      sublabel: 'Selektif 5-LOX inhibitörü',
      type: 'drug_inhibitor',
      x: 6,
      y: 52,
      badge: '(-) İlaç Hedefi',
    },
    {
      id: 'leukotrienes',
      label: 'Lökotriyenler (LTB4, C4, D4, E4)',
      sublabel: 'Bronkokonstriksiyon & Kemotaksis',
      type: 'product',
      x: 15,
      y: 72,
      badge: 'Astım / İnflamasyon',
      tooltip: 'LTB4 nötrofil kemotaksisi yapar; LTC4/LTD4/LTE4 ise güçlü bronkokonstriksiyon ve damar geçirgenliği sağlar.',
    },
    {
      id: 'leukotriene_antagonists',
      label: 'Montelukast / Zafirlukast',
      sublabel: 'CysLT1 Reseptör Antagonistleri',
      type: 'drug_inhibitor',
      x: 6,
      y: 88,
      badge: '(-) Reseptör Blokajı',
    },
    // Sağ Dal: COX ve Prostanoidler
    {
      id: 'cox_enzyme',
      label: 'Siklooksijenaz (COX-1 & COX-2)',
      sublabel: 'Konstitütif (COX-1) & İndüklenebilir (COX-2)',
      type: 'enzyme',
      x: 75,
      y: 52,
      badge: 'Prostanoid Yolağı',
    },
    {
      id: 'nsaids',
      label: 'NSAİİ (Aspirin, İndometazin)',
      sublabel: 'Non-selektif COX inhibitörleri',
      type: 'drug_inhibitor',
      x: 93,
      y: 45,
      badge: '(-) COX-1 & COX-2',
      tooltip: 'Aspirin COX enzimini geri dönüşümsüz (kovalent asetilasyon), diğer NSAİİler ise yarışmalı inhibe eder.',
    },
    {
      id: 'cox2_inhibitors',
      label: 'Selektif COX-2 İnhibitörleri',
      sublabel: 'Selekoksib',
      type: 'drug_inhibitor',
      x: 93,
      y: 58,
      badge: '(-) Yalnız COX-2',
      tooltip: 'Mide mukozasını koruyan COX-1e dokunmadan yalnız inflamatuar COX-2yi hedefler.',
    },
    {
      id: 'pgh2',
      label: 'Prostaglandin Endoperoksit (PGH2)',
      sublabel: 'Ortak prostanoid ara ürünü',
      type: 'intermediate',
      x: 75,
      y: 68,
      badge: 'Ara Basamak',
    },
    // Seviye 4: Terminal Eikozanoidler
    {
      id: 'prostacyclin',
      label: 'Prostasiklin (PGI2)',
      sublabel: 'Vasküler Endotel Ürünü',
      type: 'product',
      x: 52,
      y: 86,
      badge: 'Vazodilatasyon',
      tooltip: 'Damar endotelinde sentezlenir: Güçlü vazodilatör ve trombosit agregasyon inhibitörüdür.',
    },
    {
      id: 'prostaglandins',
      label: 'Prostaglandinler (PGE2, PGF2a)',
      sublabel: 'İnflamasyon, Ateş ve Ağrı',
      type: 'product',
      x: 74,
      y: 86,
      badge: 'Ateş & Ağrı Mediyatörü',
      tooltip: 'Vazodilatasyon, ağrı reseptörlerinin duyarlılaştırılması ve hipotalamik ateş yanıtından sorumludur.',
    },
    {
      id: 'thromboxane',
      label: 'Tromboksan A2 (TXA2)',
      sublabel: 'Trombosit Ürünü',
      type: 'product',
      x: 94,
      y: 86,
      badge: 'Vazokonstriksiyon',
      tooltip: 'Trombositlerde üretilir: Güçlü vazokonstriktör ve trombosit agregasyon tetikleyicisidir.',
    },
  ],
  edges: [
    // Yukarıdan aşağıya akış
    { id: 'e1', from: 'membrane_phospholipids', to: 'pla2', type: 'conversion', label: 'Hücre uyarısı' },
    { id: 'e2', from: 'pla2', to: 'arachidonic_acid', type: 'conversion', label: 'Ester bağı koparılır' },
    // Düzenleyiciler
    { id: 'e3', from: 'stimulators', to: 'pla2', type: 'activation', label: '(+) Kalsiyum artışı' },
    { id: 'e4', from: 'corticosteroids', to: 'pla2', type: 'inhibition', label: '(-) Lipokortin blokajı' },
    // Ayrım: Sol Dal (5-LOX)
    { id: 'e5', from: 'arachidonic_acid', to: 'lox_enzyme', type: 'conversion', label: '5-LOX yolağı' },
    { id: 'e6', from: 'zileuton', to: 'lox_enzyme', type: 'inhibition', label: '(-) Enzim inhibisyonu' },
    { id: 'e7', from: 'lox_enzyme', to: 'leukotrienes', type: 'conversion', label: 'Lökotriyen sentezi' },
    { id: 'e8', from: 'leukotriene_antagonists', to: 'leukotrienes', type: 'inhibition', label: '(-) Reseptör blokajı' },
    // Ayrım: Sağ Dal (COX)
    { id: 'e9', from: 'arachidonic_acid', to: 'cox_enzyme', type: 'conversion', label: 'Siklooksijenaz yolağı' },
    { id: 'e10', from: 'nsaids', to: 'cox_enzyme', type: 'inhibition', label: '(-) Non-selektif blokaj' },
    { id: 'e11', from: 'cox2_inhibitors', to: 'cox_enzyme', type: 'inhibition', label: '(-) Selektif COX-2 blokajı' },
    { id: 'e12', from: 'cox_enzyme', to: 'pgh2', type: 'conversion', label: 'PGH2 oluşumu' },
    // Terminal Ürünler
    { id: 'e13', from: 'pgh2', to: 'prostacyclin', type: 'conversion', label: 'Endotelde PGI2 Sentaz' },
    { id: 'e14', from: 'pgh2', to: 'prostaglandins', type: 'conversion', label: 'PGE Sentaz' },
    { id: 'e15', from: 'pgh2', to: 'thromboxane', type: 'conversion', label: 'Trombositte TXA2 Sentaz' },
  ],
  steps: [
    {
      stepNumber: 1,
      title: 'Aşama 1: Membran Fosfolipidleri ve Hücre Uyarımı',
      subtitle: 'Enflamasyonun Başlangıç Noktası',
      description: `
- **Zar Hasarı:** Hücre travması, infeksiyon veya kimyasal uyaranlar, hücre zarındaki fosfolipit çift katmanını uyarır.
- **Fosfolipit Havuzu:** Zar yapısında özellikle fosfatidilkolin ve fosfatidilinozitol zengin araşidonik asit kaynakları barındırır.
- **Başlatıcı Sinyal:** Bradikinin, trombin veya kalsiyum akışı, enzimatik yıkım sürecini tetikler.
      `.trim(),
      narration: 'İnflamasyon kaskadı, doku hasarı, travma veya mikrobiyal uyarılarda hücre membranındaki fosfolipidlerin uyarılmasıyla başlar. Membran yapısında özellikle fosfatidilkolin ve fosfatidilinozitol, eikozanoid sentezi için temel hammadde havuzunu oluşturur.',
      activeNodeIds: ['membrane_phospholipids', 'stimulators'],
      activeEdgeIds: ['e1'],
      spotlight: '📌 [SINAV SPOTU] Tüm eikozanoidlerin ortak kökeni hücre zarındaki fosfolipitlerdir.',
      durationSeconds: 11,
    },
    {
      stepNumber: 2,
      title: 'Aşama 2: Fosfolipaz A2 Aktivasyonu ve Kortikosteroid Etkisi',
      subtitle: 'Kilit Hız Kısıtlayıcı Basamak',
      description: `
- **Fosfolipaz A2 (PLA2):** Membran lipidlerinden 20 karbonlu serbest araşidonik asidi koparan ana enzimdir.
- **Kortikosteroidlerin Gücü:** Kortikosteroidler gen ekspresyonu düzeyinde **Anneksin-1 (Lipokortin)** proteinini artırarak PLA2 enzimini doğrudan inhibe eder.
- **Klinik Sonuç:** Steroidler bu basamağı bloke ederek hem prostaglandin hem de lökotriyen yollarının İKİSİNİ BİRDEN keser. Bu yüzden en güçlü anti-inflamatuar ilaçlardır.
      `.trim(),
      narration: 'Burada hız kısıtlayıcı kilit enzim Fosfolipaz A2 devreye girer. Glukokortikoidler, yani kortikosteroidler, gen düzeyinde Anneksin-1 yani Lipokortin proteinini artırarak bu enzimi doğrudan inhibe eder. Bu sayede hem prostaglandin hem de lökotriyen kolları eş zamanlı durdurulur.',
      activeNodeIds: ['pla2', 'corticosteroids', 'stimulators'],
      activeEdgeIds: ['e2', 'e3', 'e4'],
      spotlight: '🚨 [TUS SORUSU] Kortikosteroidler lipokortin (anneksin A1) sentezini artırarak Fosfolipaz A2 enzimini inhibe eder; bu sayede hem COX hem LOX kolları eşzamanlı durur!',
      durationSeconds: 14,
    },
    {
      stepNumber: 3,
      title: 'Aşama 3: Araşidonik Asit Kavşağı ve Dallanma',
      subtitle: 'Serbest Eikozanoid Öncülü',
      description: `
- **Merkezi Kavşak:** Serbest kalan serbest araşidonik asit (Araşidonat), iki ana biyokimyasal yolağa ayrılır.
- **1. Kol (Sol):** 5-Lipooksijenaz yolağı ile **Lökotriyenler** sentezlenir.
- **2. Kol (Sağ):** Siklooksijenaz yolağı ile **Prostanoidler** (Prostaglandinler, Prostasiklin ve Tromboksan) sentezlenir.
      `.trim(),
      narration: 'Zardan koparılan serbest Araşidonik asit, yolağın merkezi kavşak noktasıdır. Hücre tipine ve ortama göre önünde iki temel yön vardır: Bir kol 5-Lipooksijenaz üzerinden lökotriyenlere, diğer kol ise Siklooksijenaz üzerinden prostanoidlere ayrılır.',
      activeNodeIds: ['arachidonic_acid', 'lox_enzyme', 'cox_enzyme'],
      activeEdgeIds: ['e5', 'e9'],
      spotlight: '💡 [MEKANİZMA] Bir kol bloke edildiğinde araşidonik asit diğer kola kayarak o yolun ürünlerini artırabilir (Örn: Aspirin astımı).',
      durationSeconds: 13,
    },
    {
      stepNumber: 4,
      title: 'Aşama 4: 5-Lipooksijenaz Yolağı, Lökotriyenler ve Astım',
      subtitle: 'Lökosit Kemotaksisi ve Bronkospazm',
      description: `
- **5-LOX Enzimi:** Nötrofil ve mast hücrelerinde araşidonik asidi 5-HPETE üzerinden lökotriyenlere çevirir.
- **LTB4:** Güçlü nötrofil kemotaktik ajanıdır; nötrofilleri hasar bölgesine çeker.
- **LTC4, LTD4, LTE4 (SRS-A):** Histaminden 1000 kat daha güçlü bronkokonstriktördür ve damar geçirgenliğini belirgin artırır.
- **İlaçlar:** **Zileuton** 5-LOX enzimini inhibe eder; **Montelukast ve Zafirlukast** ise CysLT1 reseptörlerini bloke ederek astımda kullanılır.
      `.trim(),
      narration: 'Lökosit ve mast hücrelerinde çalışan 5-Lipooksijenaz yolağında üretilen lökotriyenlerden LTB4 güçlü bir nötrofil kemotaksis ajanıdır. LTC4, D4 ve E4 ise histaminden çok daha güçlü bir bronkokonstriksiyon yapar. Zileuton bu enzimi bloke ederken, Montelukast ve Zafirlukast ise reseptörleri kapatarak astım tedavisinde kullanılır.',
      activeNodeIds: ['lox_enzyme', 'zileuton', 'leukotrienes', 'leukotriene_antagonists'],
      activeEdgeIds: ['e6', 'e7', 'e8'],
      spotlight: '📌 [SINAV SPOTU] LTB4: Nötrofil kemotaksisi. LTC4, LTD4, LTE4: Bronkokonstriksiyon ve vasküler permeabilite artışı.',
      durationSeconds: 16,
    },
    {
      stepNumber: 5,
      title: 'Aşama 5: Siklooksijenaz (COX) Yolağı ve NSAİİ Blokajı',
      subtitle: 'Aspirin, Non-selektif NSAİİ ve Selekoksib',
      description: `
- **COX-1:** Konstitütif (yapısal) enzimdir; mide mukozasını korur, böbrek perfüzyonunu ve trombosit fonksiyonunu sağlar.
- **COX-2:** İnflamasyon, sitokinler ve büyüme faktörleri ile indüklenir; ağrı ve ateşten primer sorumludur.
- **Aspirin:** COX-1 ve COX-2 enzimlerini **geri dönüşümsüz (irreversibl) asetilleyerek** bloke eder.
- **NSAİİ (İbuprofen, İndometazin):** Geri dönüşümlü olarak her iki izoformu inhibe eder.
- **Selekoksib:** Selektif COX-2 inhibitörüdür; mideyi korur fakat kardiyovasküler tromboz riskini artırabilir.
      `.trim(),
      narration: 'Siklooksijenaz yolağında yapısal COX-1 mide mukozasını korurken, indüklenebilir COX-2 enflamatuvar ağrı ve ateşi tetikler. Aspirin enzimi kovalent asetilasyonla geri dönüşümsüz bloke eden tek klasik ajandır. Selekoksib gibi selektif COX-2 inhibitörleri ise mideyi korurken kardiyovasküler tromboz riskine dikkat edilmelidir.',
      activeNodeIds: ['cox_enzyme', 'nsaids', 'cox2_inhibitors', 'pgh2'],
      activeEdgeIds: ['e10', 'e11', 'e12'],
      spotlight: '🚨 [ÖNEMLİ] Aspirin COX enzimini kovalent asetilasyonla geri dönüşümsüz inhibe eden tek klasik NSAİİdir.',
      durationSeconds: 16,
    },
    {
      stepNumber: 6,
      title: 'Aşama 6: Terminal Eikozanoidler ve Vasküler Terazi',
      subtitle: 'Prostasiklin (PGI2) vs Tromboksan A2 (TXA2)',
      description: `
- **Prostasiklin (PGI2):** Vasküler endotelde üretilir. **Güçlü vazodilatasyon** yapar ve **trombosit agregasyonunu engeller**.
- **Tromboksan A2 (TXA2):** Trombositlerde üretilir. **Güçlü vazokonstriksiyon** yapar ve **trombosit agregasyonunu tetikler**.
- **PGE2 / PGD2:** Arteriyolleri genişletir (ödemi kolaylaştırır), hipotalamusta ateşi yükseltir ve ağrı reseptörlerini duyarlılaştırır.
- **Fizyolojik Terazi:** Sağlıklı endotel ve trombositler arasındaki PGI2 / TXA2 dengesi, damar içi pıhtılaşmayı ve kan akımını kusursuz kontrol eder.
      `.trim(),
      narration: 'Son basamakta hayati bir biyolojik terazi kurulur: Damar endotelinden salgılanan Prostasiklin damarları genişletip trombosit kümelenmesini önlerken; trombositlerden üretilen Tromboksan A2 tam tersine damarı büzer ve pıhtılaşmayı başlatır. PGE2 ise hipotalamusta ateşi tetikler ve ağrıyı duyarlılaştırır.',
      activeNodeIds: ['prostacyclin', 'prostaglandins', 'thromboxane'],
      activeEdgeIds: ['e13', 'e14', 'e15'],
      spotlight: '⚖️ [KLİNİK TERAZİ] PGI2 (Endotel) = Vazodilatasyon + Agregasyon İnhibisyonu. TXA2 (Trombosit) = Vazokonstriksiyon + Agregasyon Uyarımı.',
      durationSeconds: 16,
    },
  ],
  examPoints: [
    'Fosfolipaz A2 (PLA2) hız kısıtlayıcı kilit enzimdir; kortikosteroidler lipokortin ile PLA2yi bloke eder.',
    'Aspirin COX enzimini geri dönüşümsüz asetilleyen tek ajandır.',
    'LTB4 nötrofil kemotaksisi yapar; LTC4/LTD4/LTE4 ise güçlü bronkokonstriksiyon sağlar.',
    'Endotel kaynaklı PGI2 vazodilatatör ve agregasyon engelleyicidir; trombosit kaynaklı TXA2 vazokonstriktör ve agregasyon tetikleyicidir.',
  ],
};
