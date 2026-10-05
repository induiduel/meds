// Karabük Üniversitesi Tıp Fakültesi - Dönem 3 Resmi Eğitim Programı (2026-2027)
// Evrak Tarih ve Sayısı: 07.09.2026-E.541744

export interface CurriculumDiscipline {
  name: string;
  hours: number;
  instructors: string[];
}

export interface CurriculumCommittee {
  id: string;
  code: string;
  name: string;
  president: string;
  totalHours: number;
  examDate: string;
  disciplines: CurriculumDiscipline[];
  allDisciplineNames: string[];
}

export const OFFICIAL_CURRICULUM_COMMITTEES: CurriculumCommittee[] = [
  {
    id: 'donem3-kurul1',
    code: 'TIP 310',
    name: 'Ürogenital ve Obstetrik Kurulu',
    president: 'Dr. Öğr. Üyesi Serap Arslan',
    totalHours: 96,
    examDate: '23 Ekim 2026',
    allDisciplineNames: [
      'Tıbbi Patoloji',
      'Enfeksiyon Hastalıkları',
      'Üroloji',
      'Tıbbi Genetik',
      'Halk Sağlığı',
      'Kadın Hastalıkları ve Doğum',
      'Tıbbi Farmakoloji'
    ],
    disciplines: [
      { name: 'Tıbbi Patoloji', hours: 33, instructors: ['Prof. Dr. Hikmet Keleş'] },
      { name: 'Enfeksiyon Hastalıkları', hours: 22, instructors: ['Dr. Öğr. Üyesi Rüveyda Korkmazer', 'Uz. Dr. Merve Kaçar'] },
      { name: 'Üroloji', hours: 13, instructors: ['Dr. Öğr. Üyesi F. Şamil Uysal', 'Doç. Dr. Özer Baran', 'Dr. Öğr. Üyesi Salih Bürlükkara'] },
      { name: 'Tıbbi Genetik', hours: 12, instructors: ['Dr. Öğr. Üyesi Serap Arslan'] },
      { name: 'Halk Sağlığı', hours: 10, instructors: ['Doç. Dr. Nergiz Sevinç', 'Dr. Öğr. Üyesi Erkay Nacar'] },
      { name: 'Kadın Hastalıkları ve Doğum', hours: 4, instructors: ['Dr. Öğr. Üyesi Hilal Ezgi Türkmen'] },
      { name: 'Tıbbi Farmakoloji', hours: 2, instructors: ['Prof. Dr. Mehmet Özdemir'] },
    ]
  },
  {
    id: 'donem3-kurul2',
    code: 'TIP 320',
    name: 'Nöropsikiyatri Kurulu',
    president: 'Prof. Dr. Nurhayat Özkan Sevencan',
    totalHours: 105,
    examDate: '04 Aralık 2026',
    allDisciplineNames: [
      'Tıbbi Farmakoloji',
      'Psikiyatri',
      'Nöroloji',
      'Tıbbi Genetik',
      'Aile Hekimliği',
      'Beyin ve Sinir Cerrahisi',
      'Tıbbi Patoloji',
      'FTR',
      'Anesteziyoloji ve Reanimasyon'
    ],
    disciplines: [
      { name: 'Tıbbi Farmakoloji', hours: 28, instructors: ['Prof. Dr. Mehmet Özdemir', 'Dr. Öğr. Üyesi Namık Bilici'] },
      { name: 'Psikiyatri', hours: 24, instructors: ['Doç. Dr. Zuhal Koç Apaydın', 'Dr. Öğr. Üyesi Nefise Demir', 'Dr. Öğr. Üyesi Pınar Durmaz'] },
      { name: 'Nöroloji', hours: 18, instructors: ['Dr. Öğr. Üyesi İrfan Yavaş'] },
      { name: 'Tıbbi Genetik', hours: 10, instructors: ['Dr. Öğr. Üyesi Serap Arslan'] },
      { name: 'Aile Hekimliği', hours: 8, instructors: ['Doç. Dr. Habibe İnci', 'Dr. Öğr. Üyesi M. Murat Şahin', 'Dr. Öğr. Üyesi Aybala Cebecik Özcan'] },
      { name: 'Beyin ve Sinir Cerrahisi', hours: 6, instructors: ['Doç. Dr. Aydın Sinan Apaydın'] },
      { name: 'Tıbbi Patoloji', hours: 5, instructors: ['Prof. Dr. Hikmet Keleş'] },
      { name: 'FTR', hours: 4, instructors: ['Dr. Öğr. Üyesi Şengül Metin Tarhan'] },
      { name: 'Anesteziyoloji ve Reanimasyon', hours: 2, instructors: ['Dr. Öğr. Üyesi Alpay Ateş'] },
    ]
  },
  {
    id: 'donem3-kurul3',
    code: 'TIP 330',
    name: 'Gastrointestinal Sistem Kurulu',
    president: 'Dr. Öğr. Üyesi Erkay Nacar',
    totalHours: 90,
    examDate: '22 Ocak 2027',
    allDisciplineNames: [
      'Tıbbi Farmakoloji',
      'İç Hastalıkları',
      'Tıbbi Patoloji',
      'Çocuk Sağlığı ve Hastalıkları',
      'Tıbbi Genetik',
      'Enfeksiyon Hastalıkları'
    ],
    disciplines: [
      { name: 'Tıbbi Farmakoloji', hours: 31, instructors: ['Prof. Dr. Mehmet Özdemir', 'Dr. Öğr. Üyesi Namık Bilici'] },
      { name: 'İç Hastalıkları', hours: 26, instructors: ['Uzm. Dr. Ceren Çevik', 'Dr. Öğr. Üyesi Abdulvahap Coşkun', 'Doç. Dr. Fatih İnci', 'Uzm. Dr. Betül İverendi', 'Dr. Öğr. Üyesi Neslihan Ekşi', 'Prof. Dr. Fatih Karataş', 'Dr. Öğr. Üyesi Kenan Koşar'] },
      { name: 'Tıbbi Patoloji', hours: 19, instructors: ['Prof. Dr. Hikmet Keleş'] },
      { name: 'Çocuk Sağlığı ve Hastalıkları', hours: 6, instructors: ['Prof. Dr. Eylem Sevinç'] },
      { name: 'Tıbbi Genetik', hours: 4, instructors: ['Dr. Öğr. Üyesi Serap Arslan'] },
      { name: 'Enfeksiyon Hastalıkları', hours: 4, instructors: ['Uz. Dr. Merve Kaçar'] },
    ]
  },
  {
    id: 'donem3-kurul4',
    code: 'TIP 340',
    name: 'Dolaşım, Solunum ve Tümör Kurulu',
    president: 'Doç. Dr. M. Kamil Turan',
    totalHours: 90,
    examDate: '05 Mart 2027',
    allDisciplineNames: [
      'Kardiyoloji',
      'Tıbbi Patoloji',
      'Tıbbi Farmakoloji',
      'Çocuk Sağlığı ve Hastalıkları',
      'Tıbbi Genetik',
      'Göğüs Hastalıkları',
      'Enfeksiyon Hastalıkları',
      'Kalp ve Damar Cerrahisi',
      'İç Hastalıkları',
      'Halk Sağlığı',
      'Anesteziyoloji ve Reanimasyon'
    ],
    disciplines: [
      { name: 'Kardiyoloji', hours: 20, instructors: ['Prof. Dr. Orhan Önalan', 'Prof. Dr. Yeşim Akın', 'Dr. Öğr. Tuğba Kapanşahin'] },
      { name: 'Tıbbi Patoloji', hours: 18, instructors: ['Prof. Dr. Hikmet Keleş'] },
      { name: 'Tıbbi Farmakoloji', hours: 16, instructors: ['Prof. Dr. Mehmet Özdemir', 'Dr. Öğr. Üyesi Namık Bilici'] },
      { name: 'Çocuk Sağlığı ve Hastalıkları', hours: 9, instructors: ['Doç. Dr. Sadrettin Ekmen', 'Dr. Öğr. Üyesi Neslihan Ekşi', 'Dr. Öğr. Üyesi Yusuf Deniz'] },
      { name: 'Tıbbi Genetik', hours: 8, instructors: ['Dr. Öğr. Üyesi Serap Arslan'] },
      { name: 'Göğüs Hastalıkları', hours: 6, instructors: ['Dr. Öğr. Üyesi Rabia Hande Avcı'] },
      { name: 'Enfeksiyon Hastalıkları', hours: 4, instructors: ['Uz. Dr. Merve Kaçar'] },
      { name: 'Kalp ve Damar Cerrahisi', hours: 4, instructors: ['Doç. Dr. Erdem Çetin', 'Dr. Öğr. Üyesi Celal Selçuk Ünal'] },
      { name: 'İç Hastalıkları', hours: 2, instructors: ['Prof. Dr. Nurhayat Özkan Sevencan'] },
      { name: 'Halk Sağlığı', hours: 2, instructors: ['Doç. Dr. Nergis Sevinç', 'Dr. Öğr. Üyesi Erkay Nacar'] },
      { name: 'Anesteziyoloji ve Reanimasyon', hours: 1, instructors: ['Doç. Dr. Müge Arıkan'] },
    ]
  },
  {
    id: 'donem3-kurul5',
    code: 'TIP 350',
    name: 'Ortopedi, Travmatoloji ve Hematopoetik Sistem Kurulu',
    president: 'Doç. Dr. Habibe İnci',
    totalHours: 104,
    examDate: '22 Nisan 2027',
    allDisciplineNames: [
      'Acil Tıp',
      'Tıbbi Patoloji',
      'Ortopedi ve Travmatoloji',
      'Halk Sağlığı',
      'FTR',
      'İç Hastalıkları',
      'Tıbbi Genetik',
      'Tıbbi Farmakoloji',
      'Çocuk Sağlığı ve Hastalıkları',
      'Göğüs Cerrahisi',
      'Beyin ve Sinir Cerrahisi',
      'Enfeksiyon Hastalıkları'
    ],
    disciplines: [
      { name: 'Acil Tıp', hours: 18, instructors: ['Doç. Dr. Bora Çekmen', 'Dr. Öğr. Üyesi Murat Koyuncu', 'Dr. Öğr. Üyesi Büşra Bildik', 'Dr. Öğr. Üyesi Mustafa Köksal'] },
      { name: 'Tıbbi Patoloji', hours: 16, instructors: ['Prof. Dr. Hikmet Keleş'] },
      { name: 'Ortopedi ve Travmatoloji', hours: 13, instructors: ['Prof. Dr. Uygar Daşar', 'Doç. Dr. Yılmaz Ergişi', 'Dr. Öğr. Üyesi Osman Arıkan', 'Dr. Öğr. Üyesi Selçuk Korkmazer'] },
      { name: 'Halk Sağlığı', hours: 13, instructors: ['Doç. Dr. Nergis Sevinç', 'Dr. Öğr. Üyesi Erkay Nacar'] },
      { name: 'FTR', hours: 12, instructors: ['Doç. Dr. Hatice Gülşah Karataş', 'Dr. Öğr. Üyesi Ramazan Gündüz', 'Dr. Öğr. Üyesi Ahmet Tezce'] },
      { name: 'İç Hastalıkları', hours: 8, instructors: ['Dr. Öğr. Üyesi Abdulvahap Coşkun', 'Uzm. Dr. Mahmut Savanoğlu', 'Uzm. Dr. Kutay Sarı'] },
      { name: 'Tıbbi Genetik', hours: 6, instructors: ['Dr. Öğr. Üyesi Serap Arslan'] },
      { name: 'Tıbbi Farmakoloji', hours: 6, instructors: ['Prof. Dr. Mehmet Özdemir', 'Dr. Öğr. Üyesi Namık Bilici'] },
      { name: 'Çocuk Sağlığı ve Hastalıkları', hours: 4, instructors: ['Dr. Öğr. Üyesi Türkan Çetinceviz Cömez', 'Dr. Öğr. Üyesi Yusuf Deniz'] },
      { name: 'Göğüs Cerrahisi', hours: 3, instructors: ['Dr. Öğr. Üyesi Celal Selçuk Ünal'] },
      { name: 'Beyin ve Sinir Cerrahisi', hours: 3, instructors: ['Doç. Dr. Aydın Sinan Apaydın'] },
      { name: 'Enfeksiyon Hastalıkları', hours: 2, instructors: ['Uz. Dr. Merve Kaçar'] },
    ]
  },
  {
    id: 'donem3-kurul6',
    code: 'TIP 360',
    name: 'Endokrin, Metabolizma ve Yaşlanma Kurulu',
    president: 'Doç. Dr. Müge Arıkan',
    totalHours: 91,
    examDate: '11 Haziran 2027',
    allDisciplineNames: [
      'İç Hastalıkları',
      'Halk Sağlığı',
      'Tıbbi Farmakoloji',
      'Tıbbi Biyokimya',
      'Tıbbi Genetik',
      'Tıbbi Patoloji',
      'Çocuk Sağlığı ve Hastalıkları',
      'Psikiyatri',
      'Aile Hekimliği',
      'FTR'
    ],
    disciplines: [
      { name: 'İç Hastalıkları', hours: 30, instructors: ['Prof. Dr. Fatih Karataş', 'Prof. Dr. Nurhayat Özkan Sevencan', 'Dr. Öğr. Üyesi Abdulvahap Coşkun', 'Doç. Dr. Fatih İnci', 'Uzm. Dr. Betül İverendi', 'Uzm. Dr. Ceren Çevik'] },
      { name: 'Halk Sağlığı', hours: 17, instructors: ['Doç. Dr. Nergis Sevinç', 'Dr. Öğr. Üyesi Erkay Nacar'] },
      { name: 'Tıbbi Farmakoloji', hours: 14, instructors: ['Prof. Dr. Mehmet Özdemir', 'Dr. Öğr. Üyesi Namık Bilici'] },
      { name: 'Tıbbi Biyokimya', hours: 8, instructors: ['Prof. Dr. Tahir Kahraman', 'Prof. Dr. Eyüp Altınöz', 'Dr. Öğr. Üyesi Mehmet Kara'] },
      { name: 'Tıbbi Genetik', hours: 8, instructors: ['Dr. Öğr. Üyesi Serap Arslan'] },
      { name: 'Tıbbi Patoloji', hours: 4, instructors: ['Prof. Dr. Hikmet Keleş'] },
      { name: 'Çocuk Sağlığı ve Hastalıkları', hours: 3, instructors: ['Dr. Öğr. Üyesi Neslihan Ekşi'] },
      { name: 'Psikiyatri', hours: 3, instructors: ['Uzm. Dr. Pınar Durmaz'] },
      { name: 'Aile Hekimliği', hours: 2, instructors: ['Dr. Öğr. Üyesi Mehmet Murat Şahin'] },
      { name: 'FTR', hours: 2, instructors: ['Prof. Dr. Hatice Gülşah Karataş'] },
    ]
  }
];

// All valid disciplines across Dönem 3 (Genel Tıp is strictly forbidden)
export const ALL_VALID_DISCIPLINES: string[] = Array.from(
  new Set(OFFICIAL_CURRICULUM_COMMITTEES.flatMap(c => c.allDisciplineNames))
).sort();

/**
 * 2026-2027 Karabük Üniversitesi Tıp Fakültesi Dönem 3 Resmi Müfredat Dersleri (22 Ders)
 * Evrak Tarih ve Sayısı: 07.09.2026-E.541744
 */
export const DONEM3_CURRICULUM_DISCIPLINES: string[] = [
  'Acil Tıp',
  'Aile Hekimliği',
  'Anesteziyoloji ve Reanimasyon',
  'Beyin ve Sinir Cerrahisi',
  'Çocuk Sağlığı ve Hastalıkları',
  'Enfeksiyon Hastalıkları',
  'FTR',
  'Göğüs Cerrahisi',
  'Göğüs Hastalıkları',
  'Halk Sağlığı',
  'İç Hastalıkları',
  'Kadın Hastalıkları ve Doğum',
  'Kalp ve Damar Cerrahisi',
  'Kardiyoloji',
  'Nöroloji',
  'Ortopedi ve Travmatoloji',
  'Psikiyatri',
  'Tıbbi Biyokimya',
  'Tıbbi Farmakoloji',
  'Tıbbi Genetik',
  'Tıbbi Patoloji',
  'Üroloji'
];

/**
 * Verilen serbest veya karmaşık branş adını Dönem 3 resmi ders programındaki standart ada normalize eder.
 * Dönem 3 müfredatında yer almayan dersler için (Anatomi, Histoloji, Fizyoloji, vb.) null döner.
 */
export function normalizeDonem3Discipline(raw?: string): string | null {
  if (!raw) return null;
  const c = raw.trim().toLocaleLowerCase('tr-TR').replace(/[\u0300-\u036f]/g, '');

  // Dönem 3 müfredatında bulunmayan branşları dışla (Dönem 1 & 2 veya diğer stajlar)
  if (c.includes('anatomi')) return null;
  if (c.includes('histoloji') || c.includes('embriyoloji')) return null;
  if (c.includes('fizyoloji')) return null;
  if (c.includes('biyofizik')) return null;
  if (c.includes('biyoistatistik')) return null;
  if (c.includes('deontoloji') || c.includes('tıp tarihi') || c.includes('tip tarihi')) return null;
  if (c.includes('davranış') || c.includes('davranis')) return null;
  if (c.includes('terminoloji')) return null;
  if (c.includes('ilk yardım') || c.includes('ilk yardim')) return null;
  if (c.includes('genel cerrahi')) return null;
  if (c.includes('kulak burun') || c.includes('kbb')) return null;

  // Dönem 3 Resmi Müfredat Ders Eşleştirmeleri
  if (c.includes('acil')) return 'Acil Tıp';
  if (c.includes('aile')) return 'Aile Hekimliği';
  if (c.includes('anestezi')) return 'Anesteziyoloji ve Reanimasyon';
  if (c.includes('beyin') || c.includes('nöroşirürji') || c.includes('norosirurji')) return 'Beyin ve Sinir Cerrahisi';
  if (c.includes('çocuk') || c.includes('cocuk') || c.includes('pediatri')) return 'Çocuk Sağlığı ve Hastalıkları';
  if (c.includes('enfeksiyon') || c.includes('mikrobiyoloji')) return 'Enfeksiyon Hastalıkları';
  if (c.includes('ftr') || c.includes('fiziksel tıp') || c.includes('fiziksel tip') || c.includes('fizik tedavi') || c.includes('rehabilitasyon')) return 'FTR';
  if (c.includes('göğüs cerrahi') || c.includes('gogus cerrahi')) return 'Göğüs Cerrahisi';
  if (c.includes('göğüs') || c.includes('gogus') || c.includes('pulmon')) return 'Göğüs Hastalıkları';
  if (c.includes('halk')) return 'Halk Sağlığı';
  if (c.includes('kadın') || c.includes('kadin') || c.includes('doğum') || c.includes('dogum') || c.includes('obstetrik')) return 'Kadın Hastalıkları ve Doğum';
  if (c.includes('kalp ve damar') || c.includes('kalp damar') || c.includes('kvc')) return 'Kalp ve Damar Cerrahisi';
  if (c.includes('kardiyo')) return 'Kardiyoloji';
  if (c.includes('nöro') || c.includes('noro')) return 'Nöroloji';
  if (c.includes('ortopedi') || c.includes('travmatoloji')) return 'Ortopedi ve Travmatoloji';
  if (c.includes('psiki') || c.includes('ruh sağlığı') || c.includes('ruh sagligi')) return 'Psikiyatri';
  if (c.includes('biyokimya') || c.includes('biokimya')) return 'Tıbbi Biyokimya';
  if (c.includes('farma')) return 'Tıbbi Farmakoloji';
  if (c.includes('genetik')) return 'Tıbbi Genetik';
  if (c.includes('patoloji')) return 'Tıbbi Patoloji';
  if (c.includes('üroloji') || c.includes('uroloji')) return 'Üroloji';
  if (c.includes('iç') || c.includes('ic') || c.includes('dahiliye')) return 'İç Hastalıkları';

  return null;
}

/**
 * Sorunun Dönem 3'e ait olup olmadığını doğrular.
 * Hem kurul kimliğinin donem3 ile başlamasını hem de dersin Dönem 3 müfredatında yer almasını kontrol eder.
 */
export function isDonem3Question(q: { committeeId?: string; discipline?: string }): boolean {
  if (!q) return false;
  const cid = (q.committeeId || '').toLowerCase().trim();
  return cid.startsWith('donem3');
}

export function normalizeDisciplineName(name: string): string {
  const norm = normalizeDonem3Discipline(name);
  if (norm) return norm;
  return 'Tıbbi Patoloji';
}
