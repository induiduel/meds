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
      'Anestezi ve Reanimasyon'
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
      { name: 'Anestezi ve Reanimasyon', hours: 1, instructors: ['Doç. Dr. Müge Arıkan'] },
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

export function normalizeDisciplineName(name: string): string {
  if (!name) return 'Tıbbi Patoloji';
  const clean = name.trim().toLowerCase();
  if (clean.includes('genel tıp')) return 'Tıbbi Patoloji'; // Banish Genel Tıp
  if (clean.includes('patoloji')) return 'Tıbbi Patoloji';
  if (clean.includes('farma')) return 'Tıbbi Farmakoloji';
  if (clean.includes('genetik')) return 'Tıbbi Genetik';
  if (clean.includes('enfeksiyon')) return 'Enfeksiyon Hastalıkları';
  if (clean.includes('üroloji') || clean.includes('uroloji')) return 'Üroloji';
  if (clean.includes('halk')) return 'Halk Sağlığı';
  if (clean.includes('kadın') || clean.includes('doğum') || clean.includes('obstetrik')) return 'Kadın Hastalıkları ve Doğum';
  if (clean.includes('nöro') || clean.includes('noro')) return 'Nöroloji';
  if (clean.includes('psiki')) return 'Psikiyatri';
  if (clean.includes('aile')) return 'Aile Hekimliği';
  if (clean.includes('beyin') || clean.includes('nöroşirürji')) return 'Beyin ve Sinir Cerrahisi';
  if (clean.includes('ftr') || clean.includes('fizik tedavi') || clean.includes('rehabilitasyon')) return 'FTR';
  if (clean.includes('anestezi')) return 'Anesteziyoloji ve Reanimasyon';
  if (clean.includes('iç') || clean.includes('dahiliye')) return 'İç Hastalıkları';
  if (clean.includes('çocuk') || clean.includes('pediatri')) return 'Çocuk Sağlığı ve Hastalıkları';
  if (clean.includes('kardiyo')) return 'Kardiyoloji';
  if (clean.includes('göğüs cerrahi') || clean.includes('gogus cerrahi')) return 'Göğüs Cerrahisi';
  if (clean.includes('göğüs') || clean.includes('gogus') || clean.includes('pulmon')) return 'Göğüs Hastalıkları';
  if (clean.includes('kalp ve damar') || clean.includes('kvc')) return 'Kalp ve Damar Cerrahisi';
  if (clean.includes('acil')) return 'Acil Tıp';
  if (clean.includes('ortopedi')) return 'Ortopedi ve Travmatoloji';
  if (clean.includes('biyo') || clean.includes('biokimya')) return 'Tıbbi Biyokimya';

  return 'Tıbbi Patoloji';
}
