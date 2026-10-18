import type { MechanismPathway } from '../../types/pathway';
import { ARACHIDONIC_ACID_PATHWAY } from './arachidonicAcidPathway';

/**
 * 2. Apoptoz Kaskadı (İntrinsik vs Ekstrinsik Yolak)
 * Konu: Tıbbi Patoloji - Hücre Hasarı ve Hücre Ölümü
 */
export const APOPTOSIS_CASCADE_PATHWAY: MechanismPathway = {
  id: 'apoptoz-kaskadi-intrinsik-ekstrinsik',
  title: 'Apoptoz Kaskadı: İntrinsik ve Ekstrinsik Yolaklar',
  subtitle: 'Bcl-2 Ailesi, Sitokrom c, Kaspaz 9, Kaspaz 8 ve Yürütücü Kaspaz 3 Aktivasyonu',
  discipline: 'Tıbbi Patoloji',
  summary: 'Programlı hücre ölümünün (apoptoz) iki ana tetikleyici kolunu (mitokondriyal intrinsik ve ölüm reseptörü ekstrinsik) ve kaspaz aktivasyon kaskadını adım adım açıklar.',
  nodes: [
    { id: 'dna_damage', label: 'DNA Hasarı / Sitotoksik Stres', sublabel: 'p53 İndüksiyonu', type: 'substrate', x: 25, y: 10, badge: 'İntrinsik Uyaran' },
    { id: 'death_ligands', label: 'FasL / TNF-alfa', sublabel: 'Ölüm Ligandları', type: 'substrate', x: 75, y: 10, badge: 'Ekstrinsik Uyaran' },
    { id: 'bcl2_family', label: 'Bcl-2 / Bcl-xL', sublabel: 'Anti-apoptotik Proteinler', type: 'drug_inhibitor', x: 10, y: 28, badge: '(-) Apoptoz Freni' },
    { id: 'bax_bak', label: 'Bax / Bak Oligomerleri', sublabel: 'Pro-apoptotik Kanal Oluşumu', type: 'enzyme', x: 25, y: 30, badge: 'Mitokondri Poru' },
    { id: 'fas_receptor', label: 'Fas (CD95) / TNFR1', sublabel: 'FADD Adaptör Proteini', type: 'receptor', x: 75, y: 30, badge: 'Ölüm Reseptörü' },
    { id: 'cytochrome_c', label: 'Sitokrom c Salınımı', sublabel: 'Sitoplazmaya Geçiş', type: 'intermediate', x: 25, y: 50, badge: 'Mitokondri İçi Sinyal' },
    { id: 'apaf1', label: 'Apaf-1 + Apoptozom', sublabel: 'Sitokrom c + dATP Kompleksi', type: 'enzyme', x: 25, y: 68, badge: 'Apoptozom' },
    { id: 'caspase9', label: 'Başlatıcı Kaspaz-9', sublabel: 'İntrinsik Başlatıcı', type: 'enzyme', x: 38, y: 78, badge: 'İntrinsik Kaspaz' },
    { id: 'caspase8', label: 'Başlatıcı Kaspaz-8', sublabel: 'DISC Kompleksi Ürünü', type: 'enzyme', x: 68, y: 68, badge: 'Ekstrinsik Kaspaz' },
    { id: 'caspase3', label: 'Yürütücü Kaspaz-3 & Kaspaz-6', sublabel: 'Ortak Terminal Yürütücü', type: 'enzyme', x: 50, y: 88, badge: 'Yürütücü Kaspaz' },
    { id: 'apoptotic_bodies', label: 'Apoptozis ve Apopitotik Cisimcikler', sublabel: 'Fagositoz (İnflamasyonsuz Temizlenme)', type: 'clinical_effect', x: 50, y: 98, badge: 'Sonuç' },
  ],
  edges: [
    { id: 'e1', from: 'dna_damage', to: 'bax_bak', type: 'activation', label: 'p53 -> BH3-only aktivasyonu' },
    { id: 'e2', from: 'bcl2_family', to: 'bax_bak', type: 'inhibition', label: '(-) Membranı korur' },
    { id: 'e3', from: 'bax_bak', to: 'cytochrome_c', type: 'conversion', label: 'Dış zar geçirgenliği (MOMP)' },
    { id: 'e4', from: 'cytochrome_c', to: 'apaf1', type: 'activation', label: 'Apaf-1 ile birleşir' },
    { id: 'e5', from: 'apaf1', to: 'caspase9', type: 'conversion', label: 'Kaspaz-9 bölünür' },
    { id: 'e6', from: 'death_ligands', to: 'fas_receptor', type: 'activation', label: 'Trimerizasyon' },
    { id: 'e7', from: 'fas_receptor', to: 'caspase8', type: 'conversion', label: 'FADD -> Prokaspaz-8' },
    { id: 'e8', from: 'caspase9', to: 'caspase3', type: 'activation', label: 'Ortak yol aktivasyonu' },
    { id: 'e9', from: 'caspase8', to: 'caspase3', type: 'activation', label: 'Ortak yol aktivasyonu' },
    { id: 'e10', from: 'caspase3', to: 'apoptotic_bodies', type: 'conversion', label: 'Endonükleaz ve hücre iskeleti yıkımı' },
  ],
  steps: [
    {
      stepNumber: 1,
      title: 'Aşama 1: Apoptotik Uyaranlar ve Tetikleyici Sinyaller',
      subtitle: 'Hücre İçi Stres vs Hücre Dışı Ölüm Emri',
      description: '- **İntrinsik Tetikleyici:** DNA hasarı, radyasyon veya oksidatif stres p53 proteinini uyarır.\n- **Ekstrinsik Tetikleyici:** T hücreleri üzerindeki FasL veya sitokin TNF-alfa hücre yüzey ölüm reseptörlerine bağlanır.',
      narration: 'Apoptoz kaskadı iki farklı kapıdan başlayabilir: İçeride ağır DNA hasarı ve oksidatif stres p53 üzerinden intrinsik mitokondriyal yolu tetiklerken; dışarıda sitotoksik T lenfositlerin Fas ligandı hücre zarı ölüm reseptörlerini uyararak ekstrinsik yolu başlatır.',
      activeNodeIds: ['dna_damage', 'death_ligands'],
      activeEdgeIds: ['e1', 'e6'],
      spotlight: '📌 [SINAV SPOTU] Apoptozun fizyolojik başlatıcıları: İntrinsik yolda p53 ve mitokondri, ekstrinsik yolda Fas/FasL reseptör etkileşimi.',
      durationSeconds: 14,
    },
    {
      stepNumber: 2,
      title: 'Aşama 2: Mitokondriyal Denge: Bcl-2 vs Bax/Bak',
      subtitle: 'Yaşam ve Ölüm Arasındaki Moleküler Terazi',
      description: '- **Bcl-2 ve Bcl-xL:** Anti-apoptotik bekçilerdir; mitokondri dış zarını sağlam tutarak sitokrom c kaçağını engeller.\n- **Bax ve Bak:** Pro-apoptotik efektörlerdir; oligomerleşerek zarda por açar.',
      narration: 'Mitokondri dış zarında hayati bir moleküler terazi kurulur. Anti-apoptotik Bcl-2 zarı koruyup por açılmasını engellerken; pro-apoptotik Bax ve Bak oligomerleşerek mitokondri zarında delikler açar ve sitokrom c salınımına izin verir.',
      activeNodeIds: ['bcl2_family', 'bax_bak'],
      activeEdgeIds: ['e2', 'e3'],
      spotlight: '🚨 [TUS SORUSU] Foliküler lenfomada t(14;18) translokasyonu sonucu Bcl-2 aşırı üretilir ve tümör hücresi apoptozdan kaçar!',
      durationSeconds: 15,
    },
    {
      stepNumber: 3,
      title: 'Aşama 3: Sitokrom c ve Apoptozom Oluşumu',
      subtitle: 'Başlatıcı Kaspaz-9 Aktivasyonu',
      description: '- **Sitokrom c Salınımı:** Zardan sızan sitokrom c sitoplazmada **Apaf-1** ile birleşerek tekerlek benzeri **Apoptozom** kompleksini kurar.\n- **Kaspaz-9:** Apoptozom içinde prokaspaz-9 aktif kaspaz-9 haline bölünür.',
      narration: 'Mitokondriden sitoplazmaya sızan Sitokrom c, Apaf-1 proteiniyle birleşerek tekerlek biçiminde devasa bir apoptozom kompleksi kurar. Bu kompleks, intrinsik yolun başlatıcı enzimi olan Kaspaz-9u aktive eder.',
      activeNodeIds: ['cytochrome_c', 'apaf1', 'caspase9'],
      activeEdgeIds: ['e4', 'e5'],
      spotlight: '📌 [SINAV SPOTU] İntrinsik yolun başlatıcı kaspazı KASPAZ-9; ekstrinsik yolun başlatıcı kaspazı KASPAZ-8dir.',
      durationSeconds: 14,
    },
    {
      stepNumber: 4,
      title: 'Aşama 4: Ortak Yürütücü Yol: Kaspaz-3 ve Hücresel İntihar',
      subtitle: 'Kromatin Yoğunlaşması ve Apopitotik Cisimcikler',
      description: '- **Kaspaz-3 (Cellular Executioner):** Hem kaspaz-9 hem kaspaz-8 ortak yürütücü kaspaz-3ü aktifler.\n- **Kaspazla Aktive Olan DNaz (CAD):** Çekirdek DNA sını 180-200 baz çiftlik oligonükleozomal parçalara (DNA merdiveni) böler.\n- **Sessiz Temizlik:** İnflamasyon oluşturmadan makrofajlar tarafından fagositozla yok edilir.',
      narration: 'Hem kaspaz-9 hem kaspaz-8, ortak yürütücü olan Kaspaz-3 enzimini aktifler. Kaspaz-3 hücre iskeletini ve nükleusu parçalar. Hücre apopitotik cisimciklere ayrılarak hiçbir yangı oluşturmadan makrofajlarca sessizce temizlenir.',
      activeNodeIds: ['caspase3', 'apoptotic_bodies'],
      activeEdgeIds: ['e8', 'e9', 'e10'],
      spotlight: '💡 [ALTIN KURAL] Apoptozda hücre zarı parçalanmaz, yangı/inflamasyon oluşmaz (Nekrozun aksine sessiz ve programlı ölümdür).',
      durationSeconds: 16,
    },
  ],
};

/**
 * 3. Akut Enflamasyonda Lökosit Ekstravazasyonu ve Kemotaksis
 * Konu: Tıbbi Patoloji & İmmünoloji - Enflamasyon Hücresel Olaylar
 */
export const LEUKOCYTE_EXTRAVASATION_PATHWAY: MechanismPathway = {
  id: 'lokosit-ekstravazasyonu-ve-adezyon',
  title: 'Akut Enflamasyonda Lökosit Ekstravazasyonu',
  subtitle: 'Marjinasyon, Yuvarlanma (Selektinler), Sıkı Adezyon (İntegrinler) ve Transmigrasyon (PECAM-1)',
  discipline: 'Tıbbi Patoloji & İmmünoloji',
  summary: 'Enflamasyon bölgesine nötrofillerin damar içinden dokuya geçiş adımlarını ve ilgili adezyon moleküllerini (Selektin, İntegrin, PECAM-1) adım adım gösterir.',
  nodes: [
    { id: 'stasis', label: 'Vasküler Staz & Marjinasyon', sublabel: 'Kan akımı yavaşlar, lökositler çeperde', type: 'substrate', x: 20, y: 15, badge: 'Adım 1: Marjinasyon' },
    { id: 'selectins', label: 'Yuvarlanma (Rolling)', sublabel: 'E-Selektin, P-Selektin & Sialyl-Lewis X', type: 'enzyme', x: 50, y: 15, badge: 'Adım 2: Zayıf Tutunma' },
    { id: 'integrins', label: 'Sıkı Adezyon (Adhesion)', sublabel: 'İntegrinler (LFA-1, Mac-1) & ICAM-1 / VCAM-1', type: 'intermediate', x: 80, y: 35, badge: 'Adım 3: Sıkı Kenetlenme' },
    { id: 'pecam1', label: 'Transmigrasyon (Diapedez)', sublabel: 'PECAM-1 (CD31) Molekülü', type: 'intermediate', x: 80, y: 65, badge: 'Adım 4: Damardan Çıkış' },
    { id: 'chemotaxis', label: 'Kemotaksis ve Hedefe Varış', sublabel: 'C5a, LTB4, IL-8, Bakteriyel Peptidler', type: 'product', x: 50, y: 85, badge: 'Adım 5: Göç' },
    { id: 'phagocytosis', label: 'Fagositoz ve Bakterisidal Yıkım', sublabel: 'O2 Bağımlı Solunumsal Patlama (MPO)', type: 'clinical_effect', x: 20, y: 85, badge: 'Hedef Yanıt' },
  ],
  edges: [
    { id: 'e1', from: 'stasis', to: 'selectins', type: 'conversion', label: 'Endotele çarpma' },
    { id: 'e2', from: 'selectins', to: 'integrins', type: 'activation', label: 'Kemokin uyarısı ile afinite artar' },
    { id: 'e3', from: 'integrins', to: 'pecam1', type: 'conversion', label: 'Endotel aralığına girer' },
    { id: 'e4', from: 'pecam1', to: 'chemotaxis', type: 'conversion', label: 'Kimyasal gradiyente yönelim' },
    { id: 'e5', from: 'chemotaxis', to: 'phagocytosis', type: 'conversion', label: 'Mikroba bağlanma ve yutma' },
  ],
  steps: [
    {
      stepNumber: 1,
      title: 'Aşama 1: Vasküler Yavaşlama ve Marjinasyon',
      subtitle: 'Nötrofillerin Çepere İtilmesi',
      description: '- **Vazodilatasyon ve Staz:** Postkapiller venüllerde kan akımı yavaşlar, eritrositler ortada kümelenir.\n- **Marjinasyon:** Ağırlaşan lökositler damar duvarına doğru savrulur ve endotelle ilk teması kurar.',
      narration: 'Vazodilatasyon ile venüllerde kan akımı yavaşlar. Lökositler kan akımının merkezinden endotel duvarına savrularak marjinasyon gösterir.',
      activeNodeIds: ['stasis'],
      activeEdgeIds: ['e1'],
      spotlight: '📌 [SINAV SPOTU] Lökosit ekstravazasyonu en yoğun POSTKAPİLLER VENÜLLERDE gerçekleşir.',
      durationSeconds: 9,
    },
    {
      stepNumber: 2,
      title: 'Aşama 2: Yuvarlanma (Rolling) ve Selektinler',
      subtitle: 'Zayıf ve Geçici Bağlantılar',
      description: '- **Endotel Selektinleri:** P-selektin (Weibel-Palade cisimciklerinden hızlıca salınır) ve E-selektin (IL-1 ve TNF ile indüklenir).\n- **Lökosit Ligandı:** Sialyl-Lewis X oligosakkariti.\n- **Klinik:** LAD Tip 2 (Lökosit Adezyon Defekti 2) fukoz metabolizma bozukluğu sonucu selektin ligandının eksikliğidir.',
      narration: 'Endoteldeki P ve E-selektinler, nötrofil üzerindeki Sialyl-Lewis X karbonhidratlarına geçici olarak bağlanıp kopar. Lökosit çeper boyunca yuvarlanmaya başlar.',
      activeNodeIds: ['selectins'],
      activeEdgeIds: ['e2'],
      spotlight: '🚨 [TUS SORUSU] P-selektin trombosit ve endotelde WEIBEL-PALADE cisimciklerinde hazır depolanır; histamin uyarısıyla saniyeler içinde yüzeye çıkar!',
      durationSeconds: 12,
    },
    {
      stepNumber: 3,
      title: 'Aşama 3: Sıkı Adezyon ve İntegrin Aktivasyonu',
      subtitle: 'Lökositlerin Yüzeye Çivilenmesi',
      description: '- **İntegrinler:** Lökosit yüzeyindeki LFA-1 ve Mac-1 (Beta-2 integrinler / CD11/CD18).\n- **Endotel Ligandları:** ICAM-1 ve VCAM-1.\n- **Klinik:** LAD Tip 1 (CD18 beta zincir mutasyonu) = Göbek kordonu düşmesinde gecikme ve tekrarlayan piyojenik infeksiyonlar.',
      narration: 'Kemokinlerin uyarısıyla nötrofil üzerindeki integrinler yüksek afinite moduna geçer ve endoteldeki ICAM-1e kenetlenerek hücreyi tamamen durdurur.',
      activeNodeIds: ['integrins'],
      activeEdgeIds: ['e3'],
      spotlight: '📌 [TUS KLASİĞİ] LAD Tip 1: Beta-2 integrin (CD18) eksikliği; göbek kordonunun geç düşmesi ile karakterizedir.',
      durationSeconds: 12,
    },
    {
      stepNumber: 4,
      title: 'Aşama 4: Transmigrasyon (Diapedez) ve PECAM-1',
      subtitle: 'Endotel Bağlantılarından Dokulara Sızma',
      description: '- **PECAM-1 (CD31):** Hem lökositte hem endotel hücre kavşağında yer alan adezyon molekülüdür; lökositin iki endotel hücresi arasından kaymasını sağlar.',
      narration: 'Sıkı tutunan lökosit, PECAM-1 yani CD31 moleküllerinin kılavuzluğunda endotel hücrelerinin arasından doku boşluğuna sızar.',
      activeNodeIds: ['pecam1'],
      activeEdgeIds: ['e4'],
      spotlight: '📌 [SINAV SPOTU] Transmigrasyonda (diapedez) görev alan temel adezyon molekülü PECAM-1 (CD31) dir.',
      durationSeconds: 10,
    },
    {
      stepNumber: 5,
      title: 'Aşama 5: Kemotaksis ve Hedef Yıkım',
      subtitle: 'Bakteriye Doğru Yönelim ve Fagositoz',
      description: '- **Kemotaktik Ajanlar:** C5a (kompleman), LTB4 (lökotriyen), IL-8 ve bakteriyel formil-metionil peptidler.\n- **Sonuç:** Nötrofiller bu koku izini sürerek mikroorganizmayı fagositozla içine alır ve lizozomlarla yok eder.',
      narration: 'Damardan çıkan nötrofiller C5a, LTB4 ve interlökin 8 gibi kemotaktik sinyallerin izini sürerek iltihap odağına ulaşır ve mikropları yutar.',
      activeNodeIds: ['chemotaxis', 'phagocytosis'],
      activeEdgeIds: ['e5'],
      spotlight: '💡 [SPOT BİLGİ] Nötrofil kemotaksisini uyaran 4 ana faktör: C5a, LTB4, IL-8 ve Bakteriyel ürünler (N-formilmetionin).',
      durationSeconds: 12,
    },
  ],
};

/**
 * Tüm Hazır Mekanizmalar Kataloğu
 * Her ders için yeni mekanizmalar bu kataloğa eklenebilir veya çalışma anında dinamik üretilebilir.
 */
export const PATHWAY_CATALOG: Record<string, MechanismPathway> = {
  'arasidonik-asit': ARACHIDONIC_ACID_PATHWAY,
  'apoptoz-kaskadi': APOPTOSIS_CASCADE_PATHWAY,
  'lokosit-ekstravazasyonu': LEUKOCYTE_EXTRAVASATION_PATHWAY,
};

export const getPathwayById = (id: string): MechanismPathway | undefined => {
  return PATHWAY_CATALOG[id];
};
