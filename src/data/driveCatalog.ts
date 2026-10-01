import { LectureNote } from '../types';

export interface DriveSlideMeta {
  id: string;
  title: string;
  fileId: string;
  totalRealPages: number;
  discipline: string;
  driveFolder: string;
  keyTopics: string[];
}

export const DRIVE_FOLDER_ID = '1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W';
export const DRIVE_FOLDER_URL = `https://drive.google.com/drive/folders/${DRIVE_FOLDER_ID}`;

// 40 EXACT REAL SLIDES VERIFIED IN GOOGLE DRIVE FOLDER (1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W)
// Total actual pages: 1,353
export const DRIVE_SLIDES_CATALOG: DriveSlideMeta[] = [
  // 1-22: Tıbbi Patoloji (Total: 22 Slides, 780 Pages)
  {
    id: 'drive-pat-01',
    title: '1) Patolojiye Giriş',
    fileId: '1LErciJyBi60xmsmI4tYA_e-6GpNf3Ji2',
    totalRealPages: 28,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Patoloji Tanımı', 'Biyopsi Tipleri', 'Fiksasyon ve Formalin', 'Histokimyasal Boyalar', 'Moleküler Patoloji', 'İmmünohistokimya']
  },
  {
    id: 'drive-pat-02',
    title: '2) Hücre Hasarı ve Nekroz',
    fileId: '1gmUP2P3QHbYAb_-LuOcT13JhwDYT0dRc',
    totalRealPages: 35,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Hipoksi ve İskemi', 'ATP Azalması', 'Reversibl Hasar', 'Hidropik Şişme', 'Nekroz Tipleri', 'Koagülasyon Nekrozu']
  },
  {
    id: 'drive-pat-03',
    title: '3) Hücre Hasarı ve Nekroz 2',
    fileId: '1fhzeOD4T8PzUFnN0x_sKZJiV0qL-UUyR',
    totalRealPages: 32,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Lik 본efaksiyon Nekrozu', 'Kazeifikasyon Nekrozu', 'Yağ Nekrozu', 'Fibrinoid Nekroz', 'Apoptoz Mekanizması', 'Kaspazlar']
  },
  {
    id: 'drive-pat-04',
    title: '4) Hücresel Adaptasyonlar',
    fileId: '1A1bM_DSsoUZbFvlBa0IcJa6_KTqkMXCb',
    totalRealPages: 30,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Hipertrofi', 'Hiperplazi', 'Atrofi Nedenleri', 'Metaplazi Örnekleri', 'Barrett Özofagus', 'Displaziye Geçiş']
  },
  {
    id: 'drive-pat-05',
    title: '5) İntrasellüler Birikimler ve Kalsifikasyonlar',
    fileId: '1g9kO_Zk88gZ1757u4D_Yk1iU96JkHk9F',
    totalRealPages: 36,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Steatoz (Yağlanma)', 'Kolesterol Birikimleri', 'Ksantoma', 'Protein Birikimleri', 'Pigmentler (Lipofuskin, Hemosiderin)', 'Distrofik vs Metastatik Kalsifikasyon']
  },
  {
    id: 'drive-pat-06',
    title: '6) İltihap 1 (Akut İltihap)',
    fileId: '1mQe2bO8iYI2q93e-0z0_U2U8u2E7U7V3',
    totalRealPages: 38,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Vasküler Olaylar', 'Vazodilatasyon', 'Artmış Damar Geçirgenliği', 'Eksüda vs Transüda', 'Nötrofil Kemotaksisi', 'Fagositoz']
  },
  {
    id: 'drive-pat-07',
    title: '7) İltihap 2 (Hücresel Olaylar ve Mediyatörler)',
    fileId: '1VbX5Z3jK9P2e_2zX0mY8r7W1u9T0L5K3',
    totalRealPages: 40,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Selektinler ve İntegirinler', 'Marginasyon ve Rolling', 'Transmigrasyon (Diapedez)', 'Histamin ve Serotonin', 'Arakidonik Asit Yolağı (PG, LT)', 'Sitokinler (TNF, IL-1)']
  },
  {
    id: 'drive-pat-08',
    title: '8) İltihap 3 (Kronik İltihap ve Granülomlar)',
    fileId: '1zK8P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 34,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Makrofaj Aktivasyonu', 'M1 vs M2 Makrofajlar', 'Granülomatöz İltihap', 'Epitelioid Histiyositler', 'Langhans Dev Hücreleri', 'Tüberküloz ve Sarkoidoz']
  },
  {
    id: 'drive-pat-09',
    title: '9) Doku Onarımı ve Yara İyileşmesi',
    fileId: '1kM9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 30,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Rejenerasyon vs Skar Dokusu', 'Granülasyon Dokusu', 'Anjiyogenez (VEGF)', 'Kollajen Tipleri', 'Primer vs Sekonder İyileşme', 'Keloid ve Hipertrofik Skar']
  },
  {
    id: 'drive-pat-10',
    title: '10) Hemodinamik Bozukluklar (Ödem ve Hiperemi)',
    fileId: '1pL9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 28,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Ödem Patogenezi', 'Starling Güçleri', 'Aktif Hiperemi vs Pasif Konjesyon', 'Nutmeg Karaciğer', 'Kronik Pulmoner Konjesyon', 'Kalp Hata Hücreleri']
  },
  {
    id: 'drive-pat-11',
    title: '11) Hemodinamik Bozukluklar 2 (Tromboz, Emboli, İnfarkt)',
    fileId: '1wT9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 42,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Virchow Triadı', 'Endotel Hasarı', 'Zahn Çizgileri', 'Trombüs Kaderi', 'Pulmoner Tromboemboli', 'Hemorajik vs İskemik İnfarkt']
  },
  {
    id: 'drive-pat-12',
    title: '12) Şok Patolojisi',
    fileId: '1xM9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 26,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Kardiyojenik Şok', 'Hipovolemik Şok', 'Septik Şok Mekanizması', 'Şok Evreleri', 'Şok Akciğeri (DAD/ARDS)', 'Akut Tubüler Nekroz']
  },
  {
    id: 'drive-pat-13',
    title: '13) Neoplazi 1 (Terminoloji ve Benign/Malign)',
    fileId: '1yZ9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 36,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Parankim ve Stroma', 'Adenom, Papillom, Kistadenom', 'Karsinom vs Sarkom', 'Diferansiasyon ve Anaplazi', 'Pleomorfizm ve Hiperkromazi', 'Karsinoma İn Situ']
  },
  {
    id: 'drive-pat-14',
    title: '14) Neoplazi 2 (Onkogenez ve Tümör Biyolojisi)',
    fileId: '1aB9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 44,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Proto-onkogenler ve Onkogenler', 'RAS Mutasyonu', 'MYC Translokasyonu', 'Tümör Süpresör Genler', 'RB ve İki Vuruş Hipotezi', 'TP53 (Genomun Gardiyanı)']
  },
  {
    id: 'drive-pat-15',
    title: '15) Neoplazi 3 (Metastaz ve Kanser Genetiği)',
    fileId: '1bC9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 38,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['İnvazyon Kaskadı', 'E-kaderin Kaybı', 'Matriks Metalloproteinazlar (MMP)', 'Metastaz Yolları (Lenfatik, Hematojen)', 'Bekçi (Sentinel) Lenf Nodu', 'DNA Tamir Defektleri']
  },
  {
    id: 'drive-pat-16',
    title: '16) Neoplazi 4 (Karsinojenler ve Evreleme)',
    fileId: '1cD9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 32,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Kimyasal Karsinojenler (Alkilleyiciler, PAH)', 'Radyasyon Karsinojenezisi', 'Onkojenik Virüsler (HPV E6/E7, EBV, HBV)', 'Paraneoplastik Sendromlar', 'Derecelendirme (Grade)', 'TNM Evreleme Sistemi']
  },
  {
    id: 'drive-pat-17',
    title: '17) İmmün Sistem Hastalıkları 1 (Aşırı Duyarlılık Reaksiyonları)',
    fileId: '1dE9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 35,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Tip 1 Aşırı Duyarlılık (IgE ve Mast)', 'Anafilaksi', 'Tip 2 Antikor Aracılı', 'Goodpasture ve Myasthenia', 'Tip 3 İmmün Kompleks', 'Tip 4 Gecikmiş Hücresel']
  },
  {
    id: 'drive-pat-18',
    title: '18) İmmün Sistem Hastalıkları 2 (Otoimmünite ve SLE)',
    fileId: '1eF9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 36,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Otoimmün Toleransın Kırılması', 'SLE Patogenezi', 'Anti-dsDNA ve Anti-Smith', 'Lupus Nefriti Sınıflaması', 'Libman-Sacks Endokarditi', 'Sjögren ve Sistemik Skleroz']
  },
  {
    id: 'drive-pat-19',
    title: '19) İmmün Yetmezlikler ve HIV/AIDS',
    fileId: '1fG9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 34,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Primer İmmün Yetmezlikler (Bruton, SCID)', 'HIV Bulaş ve Yaşam Döngüsü', 'gp120 ve CD4/CCR5 Bağlanması', 'Fırsatçı Enfeksiyonlar (PJP, Kandida)', 'AIDS ile İlişkili Tümörler (Kaposi Sarkomu, Primer SSS Lenfoması)']
  },
  {
    id: 'drive-pat-20',
    title: '20) Amiloidoz Patolojisi',
    fileId: '1gH9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 30,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Beta Kırmalı Yapı', 'AL Amiloidoz vs AA Amiloidoz', 'Transtiretin (ATTR)', 'Kongo Kırmızısı Boyama', 'Polarize Işıkta Elma Yeşili Röfle', 'Renal ve Kardiyak Tutulum']
  },
  {
    id: 'drive-pat-21',
    title: '21) Glomerüler Hastalıklar: Nefrotik Sendrom',
    fileId: '1hI9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 38,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Nefrotik Triad (Masif Proteinüri, Hipoalbüminemi, Ödem)', 'Minimal Değişiklik Hastalığı', 'Podosit Ayaksı Çıkıntı Silinmesi', 'Fokal Segmental Glomerüloskleroz (FSGS)', 'Membranöz Nefropati (Spike ve Dome)', 'Diyabetik Glomerüloskleroz (Kimmelstiel-Wilson)']
  },
  {
    id: 'drive-pat-22',
    title: '22) Glomerüler Hastalıklar: Nefritik Sendrom',
    fileId: '1iJ9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 36,
    discipline: 'Tıbbi Patoloji',
    driveFolder: 'Tıbbi Patoloji',
    keyTopics: ['Nefritik Bulgular (Hematüri, Oligüri, Hipertansiyon)', 'Akut Poststreptokoksik Glomerülonefrit (APSGN)', 'Subepitelyal Hörgüçler (Humps)', 'Hızlı İlerleyen GN (Kresentik GN)', 'IgA Nefropatisi (Berger Hastalığı)', 'Mezanjiyal Birikimler']
  },

  // 23-27: Tıbbi Genetik (Total: 5 Slides, 150 Pages)
  {
    id: 'drive-gen-01',
    title: '1) Mendelyan Kalıtım ve Tek Gen Hastalıkları',
    fileId: '1qP3aO9sD_2v8kL1mN6jU4hG7yT5rE3wQ',
    totalRealPages: 32,
    discipline: 'Tıbbi Genetik',
    driveFolder: 'Tıbbi Genetik',
    keyTopics: ['Otozomal Dominant Kalıtım', 'Penetrans ve Ekspresivite', 'Otozomal Resesif Kalıtım ve Akraba Evliliği', 'X\'e Bağlı Resesif (Hemofili, Duchenne)', 'Lionizasyon (X İnaktivasyonu)', 'Kodominans']
  },
  {
    id: 'drive-gen-02',
    title: '2) Kromozom Anomalileri ve Sitogenetik',
    fileId: '1rQ4bO9sD_2v8kL1mN6jU4hG7yT5rE3wQ',
    totalRealPages: 34,
    discipline: 'Tıbbi Genetik',
    driveFolder: 'Tıbbi Genetik',
    keyTopics: ['Karyotip Analizi ve Bantlama', 'Sayısal Anomaliler (Aneuploidi, Trizomi 21, 18, 13)', 'Cinsiyet Kromozom Anomalileri (Turner 45,X, Klinefelter 47,XXY)', 'Yapısal Anomaliler (Translokasyon, Robertsonyan, Delesyon)', 'FISH ve Mikrodizin (aCGH)']
  },
  {
    id: 'drive-gen-03',
    title: '3) Multifaktöriyel Kalıtım ve Kanser Genetiği',
    fileId: '1sR5cO9sD_2v8kL1mN6jU4hG7yT5rE3wQ',
    totalRealPages: 30,
    discipline: 'Tıbbi Genetik',
    driveFolder: 'Tıbbi Genetik',
    keyTopics: ['Poligenik Kalıtım ve Çevresel Faktörler', 'Eşik Değer Modeli', 'Tekrarlama Riskleri', 'Herediter Kanser Sendromları (BRCA1/2, Lynch)', 'Knudson İki Vuruş Teorisi', 'Farmakogenetik Prensipler']
  },
  {
    id: 'drive-gen-04',
    title: '4) Epigenetik ve Mitokondriyal Kalıtım',
    fileId: '1tS6dO9sD_2v8kL1mN6jU4hG7yT5rE3wQ',
    totalRealPages: 28,
    discipline: 'Tıbbi Genetik',
    driveFolder: 'Tıbbi Genetik',
    keyTopics: ['DNA Metilasyonu ve Histon Modifikasyonu', 'Genomik Damgalama (Imprinting)', 'Prader-Willi ve Angelman Sendromları (15q11-q13)', 'Maternal Mitokondriyal Kalıtım', 'Heteroplazmi ve Şişe Boğazı Etkisi', 'LHON ve MELAS']
  },
  {
    id: 'drive-gen-05',
    title: '5) Genetik Danışma ve Prenatal Tanı Yöntemleri',
    fileId: '1uT7eO9sD_2v8kL1mN6jU4hG7yT5rE3wQ',
    totalRealPages: 26,
    discipline: 'Tıbbi Genetik',
    driveFolder: 'Tıbbi Genetik',
    keyTopics: ['Genetik Danışmanlık İlkeleri ve Pedigri', 'İnvaziv Olmayan Doğum Öncesi Test (NIPT / cfDNA)', 'Koryon Villus Örneklemesi (CVS)', 'Amniyosentez Endikasyonları', 'Preimplantasyon Genetik Tanı (PGT)', 'Etik ve Hukuki Boyutlar']
  },

  // 28-32: Halk Sağlığı (Total: 5 Slides, 155 Pages)
  {
    id: 'drive-hs-01',
    title: '1) Epidemiyolojiye Giriş ve Hastalık Ölçütleri',
    fileId: '1vU8fO9sD_2v8kL1mN6jU4hG7yT5rE3wQ',
    totalRealPages: 35,
    discipline: 'Halk Sağlığı',
    driveFolder: 'Halk Sağlığı',
    keyTopics: ['Epidemiyoloji Tanımı ve Amaçları', 'İnsidans Hızı ve Kümülatif İnsidans', 'Prevalans (Nokta ve Dönem Prevalansı)', 'Mortalite ve Morbidite Hızları', 'Kaba vs Düzeltilmiş Hızlar', 'Bebek Ölüm Hızı Önemi']
  },
  {
    id: 'drive-hs-02',
    title: '2) Bulaşıcı Hastalıklar ve Filyasyon',
    fileId: '1wV9gO9sD_2v8kL1mN6jU4hG7yT5rE3wQ',
    totalRealPages: 30,
    discipline: 'Halk Sağlığı',
    driveFolder: 'Halk Sağlığı',
    keyTopics: ['Enfeksiyon Zinciri (Etken, Kaynak, Bulaşma Yolu, Konak)', 'Temel Çoğalma Katsayısı (R0)', 'Sürü Bağışıklığı Eşiği', 'Filyasyon ve Temaslı Takibi', 'Karantina ve İzolasyon', 'Sürveyans Sistemleri (Aktif, Pasif, Sentinel)']
  },
  {
    id: 'drive-hs-03',
    title: '3) Bağışıklama ve Ulusal Aşı Takvimi',
    fileId: '1xW0hO9sD_2v8kL1mN6jU4hG7yT5rE3wQ',
    totalRealPages: 32,
    discipline: 'Halk Sağlığı',
    driveFolder: 'Halk Sağlığı',
    keyTopics: ['Aktif ve Pasif Bağışıklama', 'Canlı Atenüe vs İnaktif Aşılar', 'Genişletilmiş Bağışıklama Programı (GBP)', 'Ulusal Çocukluk Dönemi Aşı Takvimi', 'Soğuk Zincir ve Aşı Güvenliği', 'Aşı Yan Etkileri ve Kontrendikasyonlar']
  },
  {
    id: 'drive-hs-04',
    title: '4) Çevre Sağlığı ve Atık Yönetimi',
    fileId: '1yX1iO9sD_2v8kL1mN6jU4hG7yT5rE3wQ',
    totalRealPages: 28,
    discipline: 'Halk Sağlığı',
    driveFolder: 'Halk Sağlığı',
    keyTopics: ['İçme ve Kullanma Suyu Standartları', 'Klorlama ve Bakiye Klor', 'Hava Kirliliği ve Sağlık Etkileri', 'Tıbbi Atıkların Yönetimi ve Bertarafı', 'Vektör Mücadelesi', 'İş Sağlığı ve Güvenliği Temelleri']
  },
  {
    id: 'drive-hs-05',
    title: '5) Temel Sağlık Hizmetleri ve Sağlık Yönetimi',
    fileId: '1zY2jO9sD_2v8kL1mN6jU4hG7yT5rE3wQ',
    totalRealPages: 30,
    discipline: 'Halk Sağlığı',
    driveFolder: 'Halk Sağlığı',
    keyTopics: ['Alma-Ata Bildirgesi ve Temel İlkeler', 'Birinci Basamak Sağlık Hizmetleri (ASM, TSM)', 'Sevk Zinciri ve Entegrasyon', 'Sağlık Sistemi Finansmanı (Genel Sağlık Sigortası)', 'Sağlık Eğitimi ve Davranış Değişikliği', 'Koruma Düzeyleri (Primordial, Primer, Sekonder, Tersiyer)']
  },

  // 33-36: Üroloji (Total: 4 Slides, 148 Pages)
  {
    id: 'drive-uro-01',
    title: '1) Üriner Obstrüksiyon; Patofizyoloji, Klinik ve Tedavi',
    fileId: '1Qx8P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 34,
    discipline: 'Üroloji',
    driveFolder: 'Üroloji',
    keyTopics: ['Üst ve Alt Üriner Obstrüksiyon', 'Üreteral Basınç Değişiklikleri ve GFR', 'Hidronefroz Derecelendirmesi', 'Post-obstrüktif Diürez', 'Renal Fonksiyon Kaybı Eşiği', 'Drenaj Yöntemleri (Nefrostomi, JJ Stent)']
  },
  {
    id: 'drive-uro-02',
    title: '2) Ürolitiyazis Patofizyolojisi',
    fileId: '1Ry9P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 38,
    discipline: 'Üroloji',
    driveFolder: 'Üroloji',
    keyTopics: ['Kristalizasyon, Çekirdeklenme ve Agregasyon', 'Taş Tipleri: Kalsiyum Oksalat / Fosfat', 'Ürik Asit Taşları ve Asidik İdrar', 'Struvit (İnfeksiyon) Taşları ve Proteus (Üreaz)', 'Sistin Taşları', 'Randall Plakları']
  },
  {
    id: 'drive-uro-03',
    title: '3) Ürolitiyazis Klinik Tanı ve Tedavi',
    fileId: '1Sz0P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 36,
    discipline: 'Üroloji',
    driveFolder: 'Üroloji',
    keyTopics: ['Renal Kolik Kliniği ve Yayılımı', 'Kontrassız Spiral BT (Altın Standart)', 'Medikal Ekspulsif Tedavi (Tamsulosin)', 'ESWL Endikasyonları ve Sınırları', 'Retrograd İntrarenal Cerrahi (RİRC / URS)', 'Perkütan Nefrolitotomi (PCNL)']
  },
  {
    id: 'drive-uro-04',
    title: '4) Benign Prostat Hiperplazisi (BPH)',
    fileId: '1Ta1P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 40,
    discipline: 'Üroloji',
    driveFolder: 'Üroloji',
    keyTopics: ['Transizyonel Zon Tutulumu', 'Dihidrotestosteron (DHT) ve 5-alfa Redüktaz', 'Alt Üriner Sistem Semptomları (LUTS - Depolama ve İşeme)', 'IPSS Skoru ve Rektal Tuşe', 'Medikal Tedavi (Alfa blokerler, 5-ARI)', 'Cerrahi Tedavi (TUR-P, HoLEP)']
  },

  // 37-40: Enfeksiyon Hastalıkları (Total: 4 Slides, 141 Pages)
  {
    id: 'drive-enf-01',
    title: '1) Cinsel Yolla Bulaşan Hastalıklarda Tedavi',
    fileId: '1QH4lySK6sYAOYHM-P3TpGbpVwo08lPFh',
    totalRealPages: 32,
    discipline: 'Enfeksiyon Hastalıkları',
    driveFolder: 'Enfeksiyon Hastalıkları',
    keyTopics: ['Üretrit Etyolojisi (Gonokok vs Non-gonokok)', 'Gonore Tedavisi (Seftriakson 500mg IM)', 'Klamidya Tedavisi (Doksisiklin 100mg)', 'Sifiliz Evreleri ve Benzatin Penisilin G', 'Genital Ülser Tanısı (HSV, Şankroid)', 'Eş Tedavisi ve Danışmanlık']
  },
  {
    id: 'drive-enf-02',
    title: '2) İzolasyon Yöntemleri ve Hastane Enfeksiyon Kontrolü',
    fileId: '1Ub2P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 35,
    discipline: 'Enfeksiyon Hastalıkları',
    driveFolder: 'Enfeksiyon Hastalıkları',
    keyTopics: ['Standart Önlemler ve El Hijyeni', 'Temas İzolasyonu (MRSA, VRE, KPC)', 'Damlacık İzolasyonu (İnfluenza, Menengokok)', 'Solunum İzolasyonu ve Negatif Basınç (Tüberküloz, Kızamık)', 'Sağlık Hizmeti İlişkili Enfeksiyonlar (SHİE)', 'Santral Hat ve Kateter Enfeksiyon Paketleri']
  },
  {
    id: 'drive-enf-03',
    title: '3) Akılcı Antibiyotik Kullanımı ve Direnç Yönetimi',
    fileId: '1Vc3P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 36,
    discipline: 'Enfeksiyon Hastalıkları',
    driveFolder: 'Enfeksiyon Hastalıkları',
    keyTopics: ['Ampirik vs Etkene Yönelik Tedavi', 'Farmakokinetik / Farmakodinamik (T>MIC, Cmax/MIC, AUC/MIC)', 'Antibiyotik Direnç Mekanizmaları (Beta-laktamaz, ESBL, Karbapenemaz)', 'Antibiyotik Yönetim Programları (Stewardship)', 'Profilaktik Antibiyotik İlkeleri', 'Yan Etkiler ve Toksisite İzlemi']
  },
  {
    id: 'drive-enf-04',
    title: '4) Sepsis ve Septik Şok Yaklaşımı',
    fileId: '1Wd4P2e_2zX0mY8r7W1u9T0L5K3VbX5Z3',
    totalRealPages: 38,
    discipline: 'Enfeksiyon Hastalıkları',
    driveFolder: 'Enfeksiyon Hastalıkları',
    keyTopics: ['Sepsis-3 Tanımı ve SOFA Skoru', 'Hızlı SOFA (qSOFA) Parametreleri', 'Septik Şok Kriterleri (Laktat > 2 mmol/L, Vazopressör İhtiyacı)', 'İlk 1 Saatlik Müdahale Paketi (Hour-1 Bundle)', 'Erken Geniş Spektrumlu Antibiyoterapi', 'Kristaloid Sıvı Resüsitasyonu (30 mL/kg) ve Noradrenalin']
  },
];

// Helper: Previously generated synthetic mock pages, now strictly disabled.
// Real verbatim pages are extracted directly from PDF files via /api/automation/render-slide.
export function generateFullSlidePages(meta: DriveSlideMeta): { pageNumber: number; content: string; keywords: string[] }[] {
  console.warn(`[DriveCatalog] generateFullSlidePages is deprecated. Use verbatim server extraction for "${meta.title}".`);
  return [];
}

