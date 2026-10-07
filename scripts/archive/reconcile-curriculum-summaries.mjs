/**
 * scripts/reconcile-curriculum-summaries.mjs
 * 
 * MedSoru Ders Programı (Curriculum) Tabanlı Özet, Hoca, Konu ve Kurul Senkronizasyon Motoru
 * 
 * Bu script:
 * 1. Karabük Üniversitesi Tıp Fakültesi Dönem 3 Resmi Müfredatını (curriculumData.ts & donem3_curriculum.json) temel alır.
 * 2. 347 adet ders özetini inceler:
 *    - Hatalı kurulları düzeltir (örn. Kurul 2'de Enfeksiyon olamaz, Kurul 4'te Kadın Doğum olamaz).
 *    - Disiplin uyuşmazlıklarını çözer (örn. Benign Meme Hastalıkları -> Patoloji; Kardiyak Elektrofizyoloji -> Kardiyoloji).
 *    - Başlıkları profesyonel tıp Türkçesine dönüştürür (örn. "0İzolasyon" -> "İzolasyon Yöntemleri", "kardiyak elektrofizyoloji 2026" -> "Kardiyak Elektrofizyoloji ve Aritmiler").
 *    - Her dersin resmi hocasını tespit eder (örn. Prof. Dr. Hikmet Keleş, Prof. Dr. Orhan Önalan, Prof. Dr. Mehmet Özdemir, Doç. Dr. Nergiz Sevinç).
 *    - summaries_meta.json ve lectureSummariesCatalog.json dosyalarını zenginleştirip günceller.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const CATALOG_PATH = path.join(ROOT_DIR, 'data', 'lectureSummariesCatalog.json');
const SRC_CATALOG_PATH = path.join(ROOT_DIR, 'src', 'data', 'lectureSummariesCatalog.json');
const META_SRC_PATH = path.join(ROOT_DIR, 'src', 'data', 'summaries_meta.json');
const CURRICULUM_PATH = path.join(ROOT_DIR, 'data', 'donem3_curriculum.json');

// Türkçe başlık büyük/küçük harf düzeltici
function toTitleCaseTr(text) {
  if (!text) return '';
  const lowerWords = ['ve', 'ile', 'veya', 'de', 'da', 'için', 'bir', 'olan', 'giriş'];
  return text
    .split(/\s+/)
    .map((word, index) => {
      const lower = word.toLocaleLowerCase('tr-TR');
      if (index > 0 && lowerWords.includes(lower)) {
        return lower;
      }
      return lower.charAt(0).toLocaleUpperCase('tr-TR') + lower.slice(1);
    })
    .join(' ');
}

// Temizleme kuralları
function cleanLectureTitle(rawTitle) {
  if (!rawTitle) return '';
  let title = rawTitle
    .replace(/\.(md|txt|pdf|pptx)$/i, '')
    .replace(/^(\d+[\.\-\)]\s*)+/, '')
    .replace(/[_]+/g, ' ')
    .replace(/\s*\(1\)\s*$/, '')
    .replace(/\s*\(2\)\s*$/, '')
    .replace(/-dönüştürüldü/gi, '')
    .replace(/_SON/gi, '')
    .replace(/\s*son\s*$/i, '')
    .replace(/vize[_\s]*sonrası[_\s]*ilk[_\s]*ders/gi, '')
    .replace(/\s*yeni\s*\d*/gi, '')
    .replace(/\s*pptx\s*/gi, '')
    .replace(/250516\s*142750/g, '')
    .replace(/260408\s*134353/g, '')
    .replace(/18\.03\.2024/g, '')
    .replace(/12\.11\.2024/g, '')
    .replace(/\b202[0-9]\b/g, '')
    .replace(/d3[ab]/gi, '')
    .replace(/donem\s*3/gi, '')
    .replace(/3\.\s*sınıf/gi, '')
    .replace(/sunum/gi, '')
    .replace(/±/g, 'ı')
    .replace(/Ä±/g, 'ı')
    .replace(/\[Otomatik kaydedilme\]/g, '')
    .trim();

  // Özel başlık eşleştirmeleri
  const TITLE_MAP = {
    '0izolasyon yontemleri': 'İzolasyon Yöntemleri ve Hastane Enfeksiyonları',
    'aids': 'AIDS ve HIV Enfeksiyonu',
    'bagisikligi baskili hastalarda enfeksiyon': 'Bağışıklığı Baskılı Hastalarda Fırsatçı Enfeksiyonlar',
    'benign meme hastaliklari': 'Memenin Benign Hastalıkları',
    'cinsel yolla bulasan enfeksiyonlarda profilaksi ve korunma': 'Cinsel Yolla Bulaşan Enfeksiyonlarda Profilaksi ve Korunma',
    'cinsel yolla bulasan hastaliklarda tedavi': 'Cinsel Yolla Bulaşan Hastalıklarda Tedavi Prensipleri',
    'enfeksiyon hastaliklarinda temel kavramlar ve genel ozellikler': 'Enfeksiyon Hastalıklarında Temel Kavramlar ve Genel Özellikler',
    'genital enfeksiyonlar': 'Genital Enfeksiyonlar ve Tanı Yaklaşımı',
    'immun sistem bagisiklik si': 'İmmün Sistem ve Bağışıklık Sistemi Fizyopatolojisi',
    'intrauterin enfeksiyonlar': 'İntrauterin (Konjenital) Enfeksiyonlar',
    'sifiliz': 'Sifiliz (Frengi) ve Treponema Enfeksiyonları',
    'uretral akinti': 'Üretral Akıntı ve Üretritler',
    'uriner sistem enfeksiyonlarinin epidemiyoloji etyoloji ve semptomatolojisi': 'Üriner Sistem Enfeksiyonlarının Epidemiyolojisi, Etyolojisi ve Kliniği',
    'ana cocuk sag izleme': 'Ana ve Çocuk Sağlığı İzlemi',
    'salgin hastaliklarda kontrol ve korunma': 'Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri',
    'gebelik beslenme': 'Gebelik ve Emzirme Döneminde Beslenme',
    'gebelik terminolojisi': 'Gebelik Terminolojisi ve Temel Kavramlar',
    'gebelik hastaliklari dralpay aktumen': 'Gebelik Hastalıkları ve Obstetrik Komplikasyonlar',
    'korpus uteri hastaliklari': 'Korpus Uteri Hastalıkları ve Patolojisi',
    'serviks ve vulva hastaliklari': 'Serviks ve Vulva Hastalıkları Patolojisi',
    'over hastaliklari': 'Over Hastalıkları ve Tümörleri',
    'periyodik muayeneler': 'Periyodik Sağlık Muayeneleri ve Tarama Kılavuzları',
    'sss travmasi': 'Santral Sinir Sistemi Travmaları ve Cerrahi Yaklaşım',
    'medulla spinalis hastaliklari': 'Medulla Spinalis Hastalıkları ve Patolojisi',
    'sss hasar bicimleri odem hidrosefali herniasyon': 'SSS Hasar Biçimleri: Ödem, Hidrosefali ve Herniasyonlar',
    'intihar': 'İntihar Davranışı ve Psikiyatrik Aciller',
    'wonca agaci': 'Aile Hekimliğinde WONCA Ağacı ve Temel İlkeler',
    'spinal travmalar': 'Spinal Travmalar ve Omurga Cerrahisi',
    'bazal ganglionlar': 'Bazal Ganglionlar ve Hareket Bozuklukları',
    'bilinc bozuklugu olan hastaya yaklasim': 'Bilinç Bozukluğu Olan Hastaya Klinik Yaklaşım',
    '6 ozofagus': 'Özofagus Hastalıkları ve Patolojisi',
    'barsak tikanmaalri ve barsagin damarsal hastaliklari': 'İntestinal Obstrüksiyon ve Bağırsak Damar Hastalıkları',
    '35 dislipidemide kullanilan ilaclar': 'Dislipidemide Kullanılan Hipolipidemik İlaçlar',
    'karaciger hastaliginin klinik sendromlari': 'Karaciğer Hastalıklarının Klinik Sendromları ve Yetmezlik',
    'kronik diare ve malabsorbsiyon': 'Kronik Diyare ve Malabsorpsiyon Sendromları',
    'inflamatuar barsak hastaligi': 'İnflamatuar Bağırsak Hastalıkları (Ülseratif Kolit & Crohn)',
    'peptik ulser': 'Peptik Ülser ve Gastrit Patolojisi',
    'sarilikli hastaya yaklasim': 'Sarılıklı Hastaya Ayırıcı Tanı ve Yaklaşım',
    'sulfonamidler trimetoprim ve kinolonlar': 'Sülfonamidler, Trimetoprim ve Florokinolonlar',
    'zoonotik enfeksiyonlar': 'Zoonotik Enfeksiyonlar ve Klinik Tablolar',
    'kolera': 'Kolera ve Akut Gastroenteritler',
    'kardiyak elektrofizyoloji': 'Kardiyak Elektrofizyoloji ve Aritmi Mekanizmaları',
    'cpr': 'Kardiyopulmoner Resüsitasyon (CPR) ve Temel Yaşam Desteği',
    'ders2': 'Kardiyovasküler Biyokimya ve Kardiyak Belirteçler',
    'enfektif endokardit': 'Enfektif Endokardit ve Profilaksisi',
    'kanser ders': 'Kanser Patolojisi, Neoplazi ve Karsinogenez',
    'modifiye solunum sistemi anamnez fm semptom': 'Solunum Sistemi Anamnezi, Fizik Muayenesi ve Semptomları',
    'pnomoni': 'Pnömoniler ve Solunum Yolu Enfeksiyonları',
    '12 vazodilatorler ve angina pektoris tedavisi': 'Vazodilatörler ve Angina Pektoris Tedavisi',
    'ecg': 'Temel ve Klinik Elektrokardiyografi (EKG)',
    'kalp kapak hastaliklari': 'Kalp Kapak Hastalıkları ve Patolojisi',
    'anemi tc': 'Anemiler: Tanı, Sınıflandırma ve Klinik Yaklaşım',
    'anemiler tanim ve patofizyoloji': 'Anemilerin Tanımı, Sınıflandırması ve Patofizyolojisi',
    'ani kardiyak olum': 'Senkop ve Ani Kardiyak Ölüm (AKÖ)',
    'ikyd': 'İleri Kardiyak Yaşam Desteği (İKYD)',
    'halk sagligini etkileyen faktorler': 'Halk Sağlığını Etkileyen Çevresel ve Sosyal Faktörler',
    'bilinc degisikligi altered mental status ams drbusra bildik': 'Bilinç Değişikliği (AMS) ve Acil Yaklaşım',
    'd16 perif sinir hast': 'Periferik Sinir Hastalıkları ve Nöropatiler',
    'kafa travmalari': 'Kafa Travmaları ve Acil Nöroşirürjikal Yaklaşım',
    'senkop': 'Senkop Fizyopatolojisi ve Acil Yönetimi',
    'd27 myeloid lenfoid': 'Myeloid ve Lenfoid Neoplaziler (Lösemi & Lenfoma)',
    'd30 2 dalak timus': 'Dalak ve Timus Hastalıkları Patolojisi',
    'd30 1 kanama hast': 'Hemostaz ve Kanama Bozuklukları',
    'demir metabolizmasi': 'Demir Metabolizması ve Demir Eksikliği Anemisi',
    'hemolitik anemi': 'Hemolitik Anemiler ve Ayırıcı Tanı',
    'megaloblastik anemiler': 'Megaloblastik Anemiler (B12 ve Folat Eksikliği)',
    'bagisiklama': 'Aşılama, Bağışıklama ve Aşı Takvimi',
    'saglik gostergelerininbelirlenmesi': 'Sağlık Göstergelerinin Belirlenmesi ve Epidemiyoloji',
    'yaslilik ve beslenme': 'Geriatride Beslenme ve Yaşlılıkta Metabolizma',
    'yeterli ve dengeli beslenme': 'Yeterli ve Dengeli Beslenme İlkeleri',
    'cinsel farklilasma bozukluklari': 'Cinsel Farklılaşma Bozuklukları ve Genetik Temelleri',
    'saglik ve cevre iliskisi': 'Çevre Sağlığı ve Sağlık Üzerine Etkileri',
    'yaslilikta guvenli yasam': 'Geriatride Güvenli Yaşam ve Düşmelerin Önlenmesi',
    'yasliliga ozgu hareket sistemi bozukluklari': 'Yaşlılığa Özgü Hareket Sistemi Bozuklukları ve Sarkopeni',
    'kirim kongo kanamali atesi': 'Kırım-Kongo Kanamalı Ateşi (KKKA)',
    'sagligin gelistirilmesi': 'Sağlığın Geliştirilmesi ve Koruyucu Sağlık',
    'sagligin sosyallestirilmesi ders': 'Sağlığın Sosyalleştirilmesi ve Sağlık Ocakları Sistemi',
    'saglik egitimi': 'Sağlık Eğitimi ve Davranış Değişikliği Modelleri',
    'saglik yonetimi': 'Sağlık Yönetimi, Örgütlenmesi ve Finansmanı',
    'temel saglik hizmetleri': 'Temel Sağlık Hizmetleri (TSH) ve Alma-Ata Bildirgesi',
    'mobing': 'İş Yerinde Psikolojik Taciz (Mobbing) ve Hukuki Boyutları',
    'onemli beslenme sorunlari': 'Toplumda Önemli Beslenme Sorunları ve Malnütrisyon',
    'bebek beslenmesi': 'Bebek Beslenmesi, Anne Sütü ve Tamamlayıcı Besinler'
  };

  const key = title.toLowerCase().replace(/[^a-z0-9]/g, ' ').replace(/\s+/g, ' ').trim();
  for (const [k, v] of Object.entries(TITLE_MAP)) {
    if (key.includes(k)) {
      return v;
    }
  }

  return toTitleCaseTr(title);
}

// Resmi Hoca Eşleştirme Sözlüğü
const INSTRUCTOR_RULES = [
  // Spesifik hoca isimleri
  { regex: /hikmet\s*keleş/i, name: 'Prof. Dr. Hikmet Keleş', title: 'Prof. Dr.' },
  { regex: /mehmet\s*özdemir/i, name: 'Prof. Dr. Mehmet Özdemir', title: 'Prof. Dr.' },
  { regex: /orhan\s*önalan/i, name: 'Prof. Dr. Orhan Önalan', title: 'Prof. Dr.' },
  { regex: /yeşim\s*akın/i, name: 'Prof. Dr. Yeşim Akın', title: 'Prof. Dr.' },
  { regex: /fatih\s*karataş/i, name: 'Prof. Dr. Fatih Karataş', title: 'Prof. Dr.' },
  { regex: /nurhayat\s*özkan\s*sevencan/i, name: 'Prof. Dr. Nurhayat Özkan Sevencan', title: 'Prof. Dr.' },
  { regex: /uygar\s*daşar/i, name: 'Prof. Dr. Uygar Daşar', title: 'Prof. Dr.' },
  { regex: /hatice\s*gülşah\s*karataş/i, name: 'Prof. Dr. Hatice Gülşah Karataş', title: 'Prof. Dr.' },
  { regex: /tahir\s*kahraman/i, name: 'Prof. Dr. Tahir Kahraman', title: 'Prof. Dr.' },
  { regex: /eyüp\s*altınöz/i, name: 'Prof. Dr. Eyüp Altınöz', title: 'Prof. Dr.' },
  { regex: /nergis\s*sevinç|nergiz\s*sevinç/i, name: 'Doç. Dr. Nergiz Sevinç', title: 'Doç. Dr.' },
  { regex: /habibe\s*inci/i, name: 'Doç. Dr. Habibe İnci', title: 'Doç. Dr.' },
  { regex: /zuhal\s*koç/i, name: 'Doç. Dr. Zuhal Koç Apaydın', title: 'Doç. Dr.' },
  { regex: /aydın\s*sinan\s*apaydin/i, name: 'Doç. Dr. Aydın Sinan Apaydın', title: 'Doç. Dr.' },
  { regex: /bora\s*çekmen/i, name: 'Doç. Dr. Bora Çekmen', title: 'Doç. Dr.' },
  { regex: /sadrettin\s*ekmen/i, name: 'Doç. Dr. Sadrettin Ekmen', title: 'Doç. Dr.' },
  { regex: /erdem\s*çetin/i, name: 'Doç. Dr. Erdem Çetin', title: 'Doç. Dr.' },
  { regex: /müge\s*arıkan/i, name: 'Doç. Dr. Müge Arıkan', title: 'Doç. Dr.' },
  { regex: /özer\s*baran/i, name: 'Doç. Dr. Özer Baran', title: 'Doç. Dr.' },
  { regex: /yılmaz\s*ergişi/i, name: 'Doç. Dr. Yılmaz Ergişi', title: 'Doç. Dr.' },
  { regex: /fatih\s*inci/i, name: 'Doç. Dr. Fatih İnci', title: 'Doç. Dr.' },
  { regex: /serap\s*arslan/i, name: 'Dr. Öğr. Üyesi Serap Arslan', title: 'Dr. Öğr. Üyesi' },
  { regex: /rüveyda\s*korkmazer/i, name: 'Dr. Öğr. Üyesi Rüveyda Korkmazer', title: 'Dr. Öğr. Üyesi' },
  { regex: /namık\s*bilici/i, name: 'Dr. Öğr. Üyesi Namık Bilici', title: 'Dr. Öğr. Üyesi' },
  { regex: /irfan\s*yavaş/i, name: 'Dr. Öğr. Üyesi İrfan Yavaş', title: 'Dr. Öğr. Üyesi' },
  { regex: /erkay\s*nacar/i, name: 'Dr. Öğr. Üyesi Erkay Nacar', title: 'Dr. Öğr. Üyesi' },
  { regex: /şamil\s*uysal/i, name: 'Dr. Öğr. Üyesi F. Şamil Uysal', title: 'Dr. Öğr. Üyesi' },
  { regex: /hilal\s*ezgi\s*türkmen/i, name: 'Dr. Öğr. Üyesi Hilal Ezgi Türkmen', title: 'Dr. Öğr. Üyesi' },
  { regex: /nefise\s*demir/i, name: 'Dr. Öğr. Üyesi Nefise Demir', title: 'Dr. Öğr. Üyesi' },
  { regex: /murat\s*şahin/i, name: 'Dr. Öğr. Üyesi M. Murat Şahin', title: 'Dr. Öğr. Üyesi' },
  { regex: /aybala\s*cebecik/i, name: 'Dr. Öğr. Üyesi Aybala Cebecik Özcan', title: 'Dr. Öğr. Üyesi' },
  { regex: /rabia\s*hande\s*avcı/i, name: 'Dr. Öğr. Üyesi Rabia Hande Avcı', title: 'Dr. Öğr. Üyesi' },
  { regex: /tuğba\s*kapanşahin/i, name: 'Dr. Öğr. Üyesi Tuğba Kapanşahin', title: 'Dr. Öğr. Üyesi' },
  { regex: /neslihan\s*ekşi/i, name: 'Dr. Öğr. Üyesi Neslihan Ekşi', title: 'Dr. Öğr. Üyesi' },
  { regex: /yusuf\s*deniz/i, name: 'Dr. Öğr. Üyesi Yusuf Deniz', title: 'Dr. Öğr. Üyesi' },
  { regex: /celal\s*selçuk\s*ünal/i, name: 'Dr. Öğr. Üyesi Celal Selçuk Ünal', title: 'Dr. Öğr. Üyesi' },
  { regex: /murat\s*koyuncu/i, name: 'Dr. Öğr. Üyesi Murat Koyuncu', title: 'Dr. Öğr. Üyesi' },
  { regex: /büşra\s*bildik/i, name: 'Dr. Öğr. Üyesi Büşra Bildik', title: 'Dr. Öğr. Üyesi' },
  { regex: /mustafa\s*köksal/i, name: 'Dr. Öğr. Üyesi Mustafa Köksal', title: 'Dr. Öğr. Üyesi' },
  { regex: /osman\s*arıkan/i, name: 'Dr. Öğr. Üyesi Osman Arıkan', title: 'Dr. Öğr. Üyesi' },
  { regex: /selçuk\s*korkmazer/i, name: 'Dr. Öğr. Üyesi Selçuk Korkmazer', title: 'Dr. Öğr. Üyesi' },
  { regex: /ramazan\s*gündüz/i, name: 'Dr. Öğr. Üyesi Ramazan Gündüz', title: 'Dr. Öğr. Üyesi' },
  { regex: /abdulvahap\s*coşkun/i, name: 'Dr. Öğr. Üyesi Abdulvahap Coşkun', title: 'Dr. Öğr. Üyesi' },
  { regex: /türkan\s*çetinceviz/i, name: 'Dr. Öğr. Üyesi Türkan Çetinceviz Cömez', title: 'Dr. Öğr. Üyesi' },
  { regex: /mehmet\s*kara/i, name: 'Dr. Öğr. Üyesi Mehmet Kara', title: 'Dr. Öğr. Üyesi' },
  { regex: /alpay\s*aktümen/i, name: 'Uzm. Dr. Alpay Aktümen', title: 'Uzm. Dr.' },
  { regex: /merve\s*kaçar/i, name: 'Uzm. Dr. Merve Kaçar', title: 'Uzm. Dr.' },
  { regex: /pınar\s*durmaz/i, name: 'Uzm. Dr. Pınar Durmaz', title: 'Uzm. Dr.' },
  { regex: /begüm\s*şahin/i, name: 'Dr. Öğr. Üyesi Begüm Şahin', title: 'Dr. Öğr. Üyesi' },
  { regex: /salih\s*bürlükkara/i, name: 'Dr. Öğr. Üyesi Salih Bürlükkara', title: 'Dr. Öğr. Üyesi' },
  { regex: /kutay\s*sarı/i, name: 'Uzm. Dr. Kutay Sarı', title: 'Uzm. Dr.' },
  { regex: /mahmut\s*savanoğlu/i, name: 'Uzm. Dr. Mahmut Savanoğlu', title: 'Uzm. Dr.' }
];

// Varsayılan Kurul/Disiplin Hoca Eşleştirme (Curriculum Ground Truth)
const CURRICULUM_DEFAULT_INSTRUCTORS = {
  1: {
    'Tıbbi Patoloji': 'Prof. Dr. Hikmet Keleş',
    'Enfeksiyon Hastalıkları': 'Dr. Öğr. Üyesi Rüveyda Korkmazer',
    'Üroloji': 'Dr. Öğr. Üyesi F. Şamil Uysal',
    'Tıbbi Genetik': 'Dr. Öğr. Üyesi Serap Arslan',
    'Halk Sağlığı': 'Doç. Dr. Nergiz Sevinç',
    'Kadın Hastalıkları ve Doğum': 'Dr. Öğr. Üyesi Hilal Ezgi Türkmen',
    'Tıbbi Farmakoloji': 'Prof. Dr. Mehmet Özdemir'
  },
  2: {
    'Tıbbi Farmakoloji': 'Prof. Dr. Mehmet Özdemir',
    'Psikiyatri': 'Doç. Dr. Zuhal Koç Apaydın',
    'Nöroloji': 'Dr. Öğr. Üyesi İrfan Yavaş',
    'Tıbbi Genetik': 'Dr. Öğr. Üyesi Serap Arslan',
    'Aile Hekimliği': 'Doç. Dr. Habibe İnci',
    'Beyin ve Sinir Cerrahisi': 'Doç. Dr. Aydın Sinan Apaydın',
    'Tıbbi Patoloji': 'Prof. Dr. Hikmet Keleş',
    'FTR': 'Prof. Dr. Hatice Gülşah Karataş',
    'Anesteziyoloji ve Reanimasyon': 'Doç. Dr. Müge Arıkan'
  },
  3: {
    'Tıbbi Farmakoloji': 'Prof. Dr. Mehmet Özdemir',
    'İç Hastalıkları': 'Prof. Dr. Fatih Karataş',
    'Tıbbi Patoloji': 'Prof. Dr. Hikmet Keleş',
    'Çocuk Sağlığı ve Hastalıkları': 'Doç. Dr. Sadrettin Ekmen',
    'Tıbbi Genetik': 'Dr. Öğr. Üyesi Serap Arslan',
    'Enfeksiyon Hastalıkları': 'Dr. Öğr. Üyesi Rüveyda Korkmazer',
    'Gastroenteroloji': 'Prof. Dr. Fatih Karataş',
    'Genel Cerrahi': 'Prof. Dr. Fatih Karataş',
    'Biyokimya': 'Prof. Dr. Tahir Kahraman'
  },
  4: {
    'Kardiyoloji': 'Prof. Dr. Orhan Önalan',
    'Tıbbi Patoloji': 'Prof. Dr. Hikmet Keleş',
    'Tıbbi Farmakoloji': 'Prof. Dr. Mehmet Özdemir',
    'Çocuk Sağlığı ve Hastalıkları': 'Doç. Dr. Sadrettin Ekmen',
    'Tıbbi Genetik': 'Dr. Öğr. Üyesi Serap Arslan',
    'Göğüs Hastalıkları': 'Dr. Öğr. Üyesi Rabia Hande Avcı',
    'Enfeksiyon Hastalıkları': 'Uz. Dr. Merve Kaçar',
    'Kalp ve Damar Cerrahisi': 'Doç. Dr. Erdem Çetin',
    'İç Hastalıkları': 'Prof. Dr. Nurhayat Özkan Sevencan',
    'Halk Sağlığı': 'Doç. Dr. Nergiz Sevinç',
    'Anestezi ve Reanimasyon': 'Doç. Dr. Müge Arıkan',
    'Göğüs Cerrahisi': 'Dr. Öğr. Üyesi Celal Selçuk Ünal'
  },
  5: {
    'Acil Tıp': 'Doç. Dr. Bora Çekmen',
    'Tıbbi Patoloji': 'Prof. Dr. Hikmet Keleş',
    'Ortopedi ve Travmatoloji': 'Prof. Dr. Uygar Daşar',
    'Halk Sağlığı': 'Doç. Dr. Nergiz Sevinç',
    'FTR': 'Prof. Dr. Hatice Gülşah Karataş',
    'İç Hastalıkları': 'Dr. Öğr. Üyesi Abdulvahap Coşkun',
    'Tıbbi Genetik': 'Dr. Öğr. Üyesi Serap Arslan',
    'Tıbbi Farmakoloji': 'Prof. Dr. Mehmet Özdemir',
    'Çocuk Sağlığı ve Hastalıkları': 'Dr. Öğr. Üyesi Türkan Çetinceviz Cömez',
    'Göğüs Cerrahisi': 'Dr. Öğr. Üyesi Celal Selçuk Ünal',
    'Beyin ve Sinir Cerrahisi': 'Doç. Dr. Aydın Sinan Apaydın',
    'Enfeksiyon Hastalıkları': 'Uz. Dr. Merve Kaçar'
  },
  6: {
    'İç Hastalıkları': 'Prof. Dr. Fatih Karataş',
    'Halk Sağlığı': 'Doç. Dr. Nergiz Sevinç',
    'Tıbbi Farmakoloji': 'Prof. Dr. Mehmet Özdemir',
    'Tıbbi Biyokimya': 'Prof. Dr. Tahir Kahraman',
    'Tıbbi Genetik': 'Dr. Öğr. Üyesi Serap Arslan',
    'Tıbbi Patoloji': 'Prof. Dr. Hikmet Keleş',
    'Çocuk Sağlığı ve Hastalıkları': 'Dr. Öğr. Üyesi Neslihan Ekşi',
    'Psikiyatri': 'Uzm. Dr. Pınar Durmaz',
    'Aile Hekimliği': 'Dr. Öğr. Üyesi M. Murat Şahin',
    'FTR': 'Prof. Dr. Hatice Gülşah Karataş'
  }
};

export function runReconciliation() {
  console.log('🩺 [MedSoru Müfredat & Özet Senkronizasyonu] Başlatılıyor...');

  if (!fs.existsSync(CATALOG_PATH)) {
    throw new Error(`Catalog dosyası bulunamadı: ${CATALOG_PATH}`);
  }

  const catalog = JSON.parse(fs.readFileSync(CATALOG_PATH, 'utf8'));
  console.log(`📂 İncelenecek toplam özet sayısı: ${catalog.length}`);

  let disciplineFixCount = 0;
  let titleFixCount = 0;
  let instructorAssignedCount = 0;

  const reconciledCatalog = catalog.map((s) => {
    let kurul = s.kurul;
    let discipline = s.discipline;
    const oldTitle = s.title;
    const content = s.content || '';
    const searchTarget = `${s.fileName} ${s.title} ${content.slice(0, 1500)}`
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase();

    // 1. DİSİPLİN VE KURUL TUTARSIZLIKLARININ GİDERİLMESİ
    // Kurul 1
    if (kurul === 1) {
      if (searchTarget.includes('benign meme') || searchTarget.includes('meme')) {
        discipline = 'Tıbbi Patoloji';
      } else if (searchTarget.includes('bebek beslenmesi') || searchTarget.includes('ana çocuk') || searchTarget.includes('salgın')) {
        discipline = 'Halk Sağlığı';
      }
    }

    // Kurul 2
    if (kurul === 2) {
      if (discipline === 'Enfeksiyon Hastalıkları' || searchTarget.includes('medulla spinalis') || searchTarget.includes('sss hasar')) {
        discipline = 'Tıbbi Patoloji';
      } else if (discipline === 'Halk Sağlığı') {
        if (searchTarget.includes('intihar')) discipline = 'Psikiyatri';
        if (searchTarget.includes('wonca')) discipline = 'Aile Hekimliği';
      } else if (searchTarget.includes('spinal travma')) {
        discipline = 'Beyin ve Sinir Cerrahisi';
      }
    }

    // Kurul 3
    if (kurul === 3) {
      if (discipline === 'Genel Tıp' || searchTarget.includes('özofagus') || searchTarget.includes('barsak')) {
        discipline = 'Tıbbi Patoloji';
      } else if (searchTarget.includes('dislipidemi') || searchTarget.includes('sülfonamid') || searchTarget.includes('kinolon') || searchTarget.includes('trimetoprim')) {
        discipline = 'Tıbbi Farmakoloji';
      } else if (searchTarget.includes('karaciğer') || searchTarget.includes('sarılık') || searchTarget.includes('peptik') || searchTarget.includes('diare') || searchTarget.includes('malabsorbsiyon')) {
        discipline = 'İç Hastalıkları';
      }
    }

    // Kurul 4
    if (kurul === 4) {
      if (searchTarget.includes('elektrofizyoloji') || searchTarget.includes('kardiyak elektrofizyoloji')) {
        discipline = 'Kardiyoloji';
      } else if (searchTarget.includes('cpr') || searchTarget.includes('resüsitasyon')) {
        discipline = 'Anestezi ve Reanimasyon';
      } else if (searchTarget.includes('kanser kemoterapisi') || searchTarget.includes('vazodilatör') || searchTarget.includes('angina')) {
        discipline = 'Tıbbi Farmakoloji';
      } else if (searchTarget.includes('kanser patolojisi') || searchTarget.includes('kanser ders')) {
        discipline = 'Tıbbi Patoloji';
      } else if (searchTarget.includes('kardiyak belirteç') || searchTarget.includes('ders2')) {
        discipline = 'Kardiyoloji';
      }
    }

    // Kurul 5
    if (kurul === 5) {
      if (searchTarget.includes('anemi') || searchTarget.includes('demir metabolizması') || searchTarget.includes('megaloblastik') || searchTarget.includes('hemolitik') || searchTarget.includes('kanama')) {
        discipline = 'İç Hastalıkları';
      } else if (searchTarget.includes('ani kardiyak') || searchTarget.includes('ikyd') || searchTarget.includes('senkop') || searchTarget.includes('büşra bildik') || searchTarget.includes('altered mental')) {
        discipline = 'Acil Tıp';
      } else if (searchTarget.includes('myeloid') || searchTarget.includes('dalak') || searchTarget.includes('timus') || searchTarget.includes('lenfoid')) {
        discipline = 'Tıbbi Patoloji';
      } else if (searchTarget.includes('halk sağlığını etkileyen') || searchTarget.includes('sağlığın')) {
        discipline = 'Halk Sağlığı';
      } else if (searchTarget.includes('kafa travması') || searchTarget.includes('kafa travmaları')) {
        discipline = 'Beyin ve Sinir Cerrahisi';
      } else if (searchTarget.includes('periferik sinir') || searchTarget.includes('perif sinir')) {
        discipline = 'FTR';
      }
    }

    // Kurul 6
    if (kurul === 6) {
      if (searchTarget.includes('bağışıklama') || searchTarget.includes('sağlık göstergeleri') || searchTarget.includes('yaşlılık ve beslenme') || searchTarget.includes('sağlık ve çevre') || searchTarget.includes('dengeli beslenme') || searchTarget.includes('mobing') || searchTarget.includes('beslenme sorunları')) {
        discipline = 'Halk Sağlığı';
      } else if (searchTarget.includes('cinsel farklılaşma')) {
        discipline = 'Tıbbi Genetik';
      } else if (searchTarget.includes('hareket sistemi') || searchTarget.includes('yaşlılıkta güvenli')) {
        discipline = 'FTR';
      }
    }

    if (discipline !== s.discipline) {
      disciplineFixCount++;
    }

    // 2. BAŞLIK TEMİZLEME VE DÜZENLEME
    const cleanTitle = cleanLectureTitle(oldTitle);
    if (cleanTitle !== oldTitle) {
      titleFixCount++;
    }

    // 3. HOCA (INSTRUCTOR) TESPİTİ
    let instructor = null;

    // A) İçerikte veya başlıkta hoca adı var mı?
    for (const rule of INSTRUCTOR_RULES) {
      if (rule.regex.test(content) || rule.regex.test(s.fileName) || rule.regex.test(oldTitle)) {
        instructor = rule.name;
        break;
      }
    }

    // B) Eğer bulunamadıysa, o kurul ve disiplinin resmi baş hocasını ata
    if (!instructor) {
      const kurulMap = CURRICULUM_DEFAULT_INSTRUCTORS[kurul] || {};
      instructor = kurulMap[discipline] || 'Dönem 3 Öğretim Üyesi';
    }

    instructorAssignedCount++;

    return {
      ...s,
      kurul,
      committeeId: `donem3-kurul${kurul}`,
      discipline,
      title: cleanTitle,
      instructor
    };
  });

  console.log(`✅ ${titleFixCount} dersin başlığı resmi terminolojiye göre temizlendi.`);
  console.log(`✅ ${disciplineFixCount} dersin hatalı disiplin/kurul etiketi düzeltildi.`);
  console.log(`✅ ${instructorAssignedCount} dersin resmi öğretim üyesi başarıyla bağlandı.`);

  // 1. Zenginleştirilmiş metadata JSON (src/data/summaries_meta.json)
  const metaList = reconciledCatalog.map(s => ({
    id: s.id,
    kurul: s.kurul,
    committeeId: s.committeeId,
    discipline: s.discipline,
    title: s.title,
    instructor: s.instructor,
    fileName: s.fileName,
    keyPoints: s.keyPoints,
    charCount: s.charCount,
    readingTimeMinutes: s.readingTimeMinutes
  }));

  fs.writeFileSync(META_SRC_PATH, JSON.stringify(metaList, null, 2), 'utf8');
  console.log(`💾 Metadata kaydedildi: ${META_SRC_PATH}`);

  // 2. Tam katalog (data/ ve src/data/)
  const fullJson = JSON.stringify(reconciledCatalog, null, 2);
  fs.writeFileSync(CATALOG_PATH, fullJson, 'utf8');
  if (fs.existsSync(path.dirname(SRC_CATALOG_PATH))) {
    fs.writeFileSync(SRC_CATALOG_PATH, fullJson, 'utf8');
  }
  console.log(`💾 Tam katalog güncellendi.`);

  return { titleFixCount, disciplineFixCount, instructorAssignedCount };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  runReconciliation();
}
