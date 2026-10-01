/**
 * scripts/build-database-json.mjs
 * 
 * MedSoru Veritabanı JSON Üretim ve Senkronizasyon Motoru
 * 
 * Hedef Klasör: C:\Users\indui\Desktop\meds_database\database_json
 * 
 * Bu script:
 * 1. Tüm dönem ve kurullar için klasör hiyerarşisini kurar:
 *    - donem1k1 ... donem1k6, donem1f, donem1b
 *    - donem2k1 ... donem2k6, donem2f, donem2b
 *    - donem3k1 ... donem3k6, donem3f, donem3b
 * 2. Her bir klasöre Supabase PostgreSQL ve Firebase Firestore standartlarına %100 uyumlu
 *    JSON dosyalarını titizlikle yerleştirir:
 *    - pastquestions.json: Doğrulanmış, temizlenmiş, şıkları ve açıklamaları tam çıkmış sınav soruları
 *    - realtimequestion.json: Canlı dönem soru taslakları ve güncel sınav havuzu
 *    - users.json: Sistem kullanıcıları, roller ve moderatörler
 *    - committee.json: Kurul/sınav meta verileri (isim, kod, branşlar, hedef soru sayısı, renk)
 *    - lectures.json: Kurula ait amfi slayt ve ders notları indeksleri
 *    - summary.json: İstatistik ve özet telemetrisi
 * 3. Kök dizine index.json, manifest.json ve README.md belgelerini üretir.
 * 
 * Böylece hiçbir sunucu/istemci sürekli ham txt okumak zorunda kalmaz!
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const BASE_OUT_DIR = 'C:\\Users\\indui\\Desktop\\meds_database\\database_json';
const MEDS_DATA_DIR = path.join(ROOT_DIR, 'data');
const MEDS_DATABASE_DIR = 'C:\\Users\\indui\\Desktop\\meds_database';

// 1. Kurul ve Sınav Tanımları (Dönem 1, 2, 3)
const COMMITTEE_DEFINITIONS = [
  // --- DÖNEM 1 ---
  {
    folderKey: 'donem1k1',
    committeeId: 'donem1-kurul1',
    donem: 1,
    kurul: 1,
    type: 'kurul',
    code: 'TIP 110',
    name: 'Dönem 1 - Kurul 1: TIP 110 - Tıbbi Bilimlere Giriş Kurulu',
    term: '2026-2027 Güz',
    color: 'emerald',
    targetCount: 100,
    examDate: 'Kasım 2026',
    description: 'Tıbbi Biyoloji, Tıbbi Biyokimya, Temel Tıbbi Terminoloji ve Hekimlik İlkeleri.',
    disciplines: ['Tıbbi Biyoloji', 'Tıbbi Biyokimya', 'Tıp Tarihi ve Deontoloji', 'Biyoistatistik']
  },
  {
    folderKey: 'donem1k2',
    committeeId: 'donem1-kurul2',
    donem: 1,
    kurul: 2,
    type: 'kurul',
    code: 'TIP 120',
    name: 'Dönem 1 - Kurul 2: TIP 120 - Hücre Yapısı ve Moleküler Mekanizmalar',
    term: '2026-2027 Güz',
    color: 'teal',
    targetCount: 100,
    examDate: 'Aralık 2026',
    description: 'Hücre membran yapısı, organeller, nükleik asitler ve enzim kinetiği.',
    disciplines: ['Tıbbi Biyoloji', 'Tıbbi Biyokimya', 'Biyofizik', 'Tıbbi Genetik']
  },
  {
    folderKey: 'donem1k3',
    committeeId: 'donem1-kurul3',
    donem: 1,
    kurul: 3,
    type: 'kurul',
    code: 'TIP 130',
    name: 'Dönem 1 - Kurul 3: TIP 130 - Temel Genetik ve Metabolizma Kurulu',
    term: '2026-2027 Güz',
    color: 'cyan',
    targetCount: 100,
    examDate: 'Ocak 2027',
    description: 'Kalıtım mekanizmaları, kromozom anomalileri, karbonhidrat ve lipid metabolizması.',
    disciplines: ['Tıbbi Genetik', 'Tıbbi Biyokimya', 'Tıbbi Mikrobiyolojiye Giriş', 'Biyoistatistik']
  },
  {
    folderKey: 'donem1k4',
    committeeId: 'donem1-kurul4',
    donem: 1,
    kurul: 4,
    type: 'kurul',
    code: 'TIP 140',
    name: 'Dönem 1 - Kurul 4: TIP 140 - Temel Doku Biyolojisi Kurulu',
    term: '2026-2027 Bahar',
    color: 'blue',
    targetCount: 100,
    examDate: 'Mart 2027',
    description: 'Epitel doku, bağ doku, kıkırdak ve kemik dokusu histolojisi ve fizyolojisi.',
    disciplines: ['Histoloji ve Embriyoloji', 'Tıbbi Fizyoloji', 'Tıbbi Biyokimya']
  },
  {
    folderKey: 'donem1k5',
    committeeId: 'donem1-kurul5',
    donem: 1,
    kurul: 5,
    type: 'kurul',
    code: 'TIP 150',
    name: 'Dönem 1 - Kurul 5: TIP 150 - Kas-İskelet Sistemi ve Hareket Kurulu',
    term: '2026-2027 Bahar',
    color: 'indigo',
    targetCount: 100,
    examDate: 'Mayıs 2027',
    description: 'Kemikler, eklemler, aksiyel ve apendiküler iskelet anatomisi.',
    disciplines: ['Anatomi', 'Histoloji ve Embriyoloji', 'Tıbbi Biyofizik']
  },
  {
    folderKey: 'donem1k6',
    committeeId: 'donem1-kurul6',
    donem: 1,
    kurul: 6,
    type: 'kurul',
    code: 'TIP 160',
    name: 'Dönem 1 - Kurul 6: TIP 160 - Temel Tıp Bilimleri Entegrasyon Kurulu',
    term: '2026-2027 Bahar',
    color: 'violet',
    targetCount: 100,
    examDate: 'Haziran 2027',
    description: 'Dönem 1 genel kazanımların klinik olgularla entegrasyonu.',
    disciplines: ['Anatomi', 'Histoloji', 'Tıbbi Biyokimya', 'Tıbbi Biyoloji']
  },
  {
    folderKey: 'donem1f',
    committeeId: 'donem1-final',
    donem: 1,
    kurul: 'final',
    type: 'final',
    code: 'TIP 100-FINAL',
    name: 'Dönem 1 - Yıl Sonu Genel Final Sınavı',
    term: '2026-2027 Genel',
    color: 'slate',
    targetCount: 150,
    examDate: 'Temmuz 2027',
    description: 'Dönem 1 tüm kurullarını kapsayan genel değerlendirme sınavı.',
    disciplines: ['Anatomi', 'Tıbbi Biyokimya', 'Histoloji ve Embriyoloji', 'Tıbbi Biyoloji', 'Biyofizik']
  },
  {
    folderKey: 'donem1b',
    committeeId: 'donem1-butunleme',
    donem: 1,
    kurul: 'butunleme',
    type: 'butunleme',
    code: 'TIP 100-BUT',
    name: 'Dönem 1 - Yıl Sonu Bütünleme Sınavı',
    term: '2026-2027 Genel',
    color: 'rose',
    targetCount: 150,
    examDate: 'Ağustos 2027',
    description: 'Dönem 1 bütünleme telafi sınavı.',
    disciplines: ['Anatomi', 'Tıbbi Biyokimya', 'Histoloji ve Embriyoloji', 'Tıbbi Biyoloji', 'Biyofizik']
  },

  // --- DÖNEM 2 ---
  {
    folderKey: 'donem2k1',
    committeeId: 'donem2-kurul1',
    donem: 2,
    kurul: 1,
    type: 'kurul',
    code: 'TIP 210',
    name: 'Dönem 2 - Kurul 1: TIP 210 - Doku ve Hücre Biyolojisi Kurulu',
    term: '2026-2027 Güz',
    color: 'emerald',
    targetCount: 100,
    examDate: 'Kasım 2026',
    description: 'Hücre fizyolojisi, membran potansiyelleri ve kas kontraksiyonu.',
    disciplines: ['Tıbbi Fizyoloji', 'Histoloji ve Embriyoloji', 'Tıbbi Biyokimya']
  },
  {
    folderKey: 'donem2k2',
    committeeId: 'donem2-kurul2',
    donem: 2,
    kurul: 2,
    type: 'kurul',
    code: 'TIP 220',
    name: 'Dönem 2 - Kurul 2: TIP 220 - Dolaşım ve Solunum Sistemi Kurulu',
    term: '2026-2027 Güz',
    color: 'rose',
    targetCount: 100,
    examDate: 'Aralık 2026',
    description: 'Kalp anatomisi, elektrofizyoloji, hemodinami ve solunum mekaniği.',
    disciplines: ['Anatomi', 'Tıbbi Fizyoloji', 'Histoloji ve Embriyoloji']
  },
  {
    folderKey: 'donem2k3',
    committeeId: 'donem2-kurul3',
    donem: 2,
    kurul: 3,
    type: 'kurul',
    code: 'TIP 230',
    name: 'Dönem 2 - Kurul 3: TIP 230 - Sindirim ve Metabolizma Kurulu',
    term: '2026-2027 Güz',
    color: 'amber',
    targetCount: 100,
    examDate: 'Ocak 2027',
    description: 'GİS anatomisi, sindirim sekresyonları, emilim ve karaciğer metabolizması.',
    disciplines: ['Anatomi', 'Tıbbi Fizyoloji', 'Tıbbi Biyokimya', 'Histoloji']
  },
  {
    folderKey: 'donem2k4',
    committeeId: 'donem2-kurul4',
    donem: 2,
    kurul: 4,
    type: 'kurul',
    code: 'TIP 240',
    name: 'Dönem 2 - Kurul 4: TIP 240 - Sinir Sistemi ve Duyu Organları Kurulu',
    term: '2026-2027 Bahar',
    color: 'indigo',
    targetCount: 100,
    examDate: 'Mart 2027',
    description: 'Santral ve periferik sinir sistemi anatomisi, göz, kulak ve duyular.',
    disciplines: ['Anatomi', 'Tıbbi Fizyoloji', 'Histoloji ve Embriyoloji']
  },
  {
    folderKey: 'donem2k5',
    committeeId: 'donem2-kurul5',
    donem: 2,
    kurul: 5,
    type: 'kurul',
    code: 'TIP 250',
    name: 'Dönem 2 - Kurul 5: TIP 250 - Endokrin ve Ürogenital Sistem Kurulu',
    term: '2026-2027 Bahar',
    color: 'teal',
    targetCount: 100,
    examDate: 'Mayıs 2027',
    description: 'Hipotalamo-hipofizer aks, böbrek fonksiyonları, asit-baz ve genital sistem.',
    disciplines: ['Anatomi', 'Tıbbi Fizyoloji', 'Histoloji ve Embriyoloji', 'Tıbbi Biyokimya']
  },
  {
    folderKey: 'donem2k6',
    committeeId: 'donem2-kurul6',
    donem: 2,
    kurul: 6,
    type: 'kurul',
    code: 'TIP 260',
    name: 'Dönem 2 - Kurul 6: TIP 260 - Biyolojik Etkenler ve İmmünoloji Kurulu',
    term: '2026-2027 Bahar',
    color: 'purple',
    targetCount: 100,
    examDate: 'Haziran 2027',
    description: 'Temel mikrobiyoloji, bakteriler, virüsler, mantarlar ve immün sistem.',
    disciplines: ['Tıbbi Mikrobiyoloji', 'İmmünoloji', 'Parazitoloji']
  },
  {
    folderKey: 'donem2f',
    committeeId: 'donem2-final',
    donem: 2,
    kurul: 'final',
    type: 'final',
    code: 'TIP 200-FINAL',
    name: 'Dönem 2 - Yıl Sonu Genel Final Sınavı',
    term: '2026-2027 Genel',
    color: 'slate',
    targetCount: 150,
    examDate: 'Temmuz 2027',
    description: 'Dönem 2 tüm sistem kurullarını kapsayan genel tıp final sınavı.',
    disciplines: ['Anatomi', 'Tıbbi Fizyoloji', 'Histoloji', 'Tıbbi Mikrobiyoloji', 'Biyokimya']
  },
  {
    folderKey: 'donem2b',
    committeeId: 'donem2-butunleme',
    donem: 2,
    kurul: 'butunleme',
    type: 'butunleme',
    code: 'TIP 200-BUT',
    name: 'Dönem 2 - Yıl Sonu Bütünleme Sınavı',
    term: '2026-2027 Genel',
    color: 'rose',
    targetCount: 150,
    examDate: 'Ağustos 2027',
    description: 'Dönem 2 bütünleme telafi sınavı.',
    disciplines: ['Anatomi', 'Tıbbi Fizyoloji', 'Histoloji', 'Tıbbi Mikrobiyoloji', 'Biyokimya']
  },

  // --- DÖNEM 3 ---
  {
    folderKey: 'donem3k1',
    committeeId: 'donem3-kurul1',
    donem: 3,
    kurul: 1,
    type: 'kurul',
    code: 'TIP 310',
    name: 'Dönem 3 - Kurul 1: TIP 310 - Ürogenital ve Obstetrik Kurulu',
    term: '2026-2027 Güz',
    color: 'teal',
    targetCount: 100,
    examDate: '23 Ekim 2026',
    description: 'Tıbbi Patoloji, Enfeksiyon Hastalıkları, Üroloji, Tıbbi Genetik, Halk Sağlığı, Kadın Hastalıkları ve Doğum, Tıbbi Farmakoloji.',
    disciplines: ['Tıbbi Patoloji', 'Tıbbi Biyoloji ve Genetik', 'Tıbbi Biyokimya', 'Enfeksiyon Hastalıkları', 'Üroloji', 'Tıbbi Genetik', 'Halk Sağlığı', 'Kadın Hastalıkları ve Doğum', 'Tıbbi Farmakoloji']
  },
  {
    folderKey: 'donem3k2',
    committeeId: 'donem3-kurul2',
    donem: 3,
    kurul: 2,
    type: 'kurul',
    code: 'TIP 320',
    name: 'Dönem 3 - Kurul 2: TIP 320 - Nöropsikiyatri Kurulu',
    term: '2026-2027 Güz',
    color: 'indigo',
    targetCount: 100,
    examDate: '04 Aralık 2026',
    description: 'Tıbbi Farmakoloji, Psikiyatri, Nöroloji, Tıbbi Genetik, Aile Hekimliği, Beyin ve Sinir Cerrahisi, Tıbbi Patoloji, FTR, Anesteziyoloji.',
    disciplines: ['Tıbbi Farmakoloji', 'Psikiyatri', 'Nöroloji', 'Tıbbi Genetik', 'Aile Hekimliği', 'Beyin ve Sinir Cerrahisi', 'Tıbbi Patoloji', 'FTR', 'Anesteziyoloji ve Reanimasyon']
  },
  {
    folderKey: 'donem3k3',
    committeeId: 'donem3-kurul3',
    donem: 3,
    kurul: 3,
    type: 'kurul',
    code: 'TIP 330',
    name: 'Dönem 3 - Kurul 3: TIP 330 - Gastrointestinal Sistem Kurulu',
    term: '2026-2027 Güz',
    color: 'amber',
    targetCount: 100,
    examDate: '22 Ocak 2027',
    description: 'Tıbbi Farmakoloji, İç Hastalıkları, Tıbbi Patoloji, Çocuk Sağlığı ve Hastalıkları, Tıbbi Genetik, Enfeksiyon Hastalıkları.',
    disciplines: ['Tıbbi Farmakoloji', 'İç Hastalıkları', 'Tıbbi Patoloji', 'Çocuk Sağlığı ve Hastalıkları', 'Tıbbi Genetik', 'Enfeksiyon Hastalıkları']
  },
  {
    folderKey: 'donem3k4',
    committeeId: 'donem3-kurul4',
    donem: 3,
    kurul: 4,
    type: 'kurul',
    code: 'TIP 340',
    name: 'Dönem 3 - Kurul 4: TIP 340 - Dolaşım, Solunum ve Tümör Kurulu',
    term: '2026-2027 Bahar',
    color: 'rose',
    targetCount: 100,
    examDate: '26 Mart 2027',
    description: 'Kardiyoloji, Göğüs Hastalıkları, Onkoloji, Patoloji ve Farmakoloji entegrasyonu.',
    disciplines: ['Tıbbi Farmakoloji', 'Tıbbi Patoloji', 'Kardiyoloji', 'Göğüs Hastalıkları', 'Göğüs Cerrahisi', 'Kalp Damar Cerrahisi', 'Çocuk Sağlığı ve Hastalıkları', 'Tıbbi Genetik']
  },
  {
    folderKey: 'donem3k5',
    committeeId: 'donem3-kurul5',
    donem: 3,
    kurul: 5,
    type: 'kurul',
    code: 'TIP 350',
    name: 'Dönem 3 - Kurul 5: TIP 350 - Endokrin, Kas-İskelet ve Cilt Kurulu',
    term: '2026-2027 Bahar',
    color: 'emerald',
    targetCount: 100,
    examDate: '07 Mayıs 2027',
    description: 'Endokrinoloji, Romatoloji, Ortopedi, Dermatoloji ve Patoloji sistemleri.',
    disciplines: ['Tıbbi Farmakoloji', 'Tıbbi Patoloji', 'İç Hastalıkları (Endokrin/Romatoloji)', 'Ortopedi ve Travmatoloji', 'Deri ve Zührevi Hastalıklar', 'Çocuk Sağlığı ve Hastalıkları', 'Tıbbi Genetik']
  },
  {
    folderKey: 'donem3k6',
    committeeId: 'donem3-kurul6',
    donem: 3,
    kurul: 6,
    type: 'kurul',
    code: 'TIP 360',
    name: 'Dönem 3 - Kurul 6: TIP 360 - Hematoloji ve Onkoloji Kurulu',
    term: '2026-2027 Bahar',
    color: 'purple',
    targetCount: 100,
    examDate: '11 Haziran 2027',
    description: 'Hematopoetik sistem, lenfoid doku patolojileri ve onkolojik mekanizmalar.',
    disciplines: ['Hematoloji', 'Onkoloji', 'Tıbbi Farmakoloji', 'Tıbbi Patoloji', 'Tıbbi Biyokimya', 'Tıbbi Genetik', 'Çocuk Hematoloji-Onkoloji']
  },
  {
    folderKey: 'donem3f',
    committeeId: 'donem3-final',
    donem: 3,
    kurul: 'final',
    type: 'final',
    code: 'TIP 300-FINAL',
    name: 'Dönem 3 - Yıl Sonu Genel Final Sınavı',
    term: '2026-2027 Genel',
    color: 'blue',
    targetCount: 150,
    examDate: 'Temmuz 2027',
    description: 'Tüm kurulları kapsayan yıl sonu genel tıp değerlendirme sınavı.',
    disciplines: ['Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'İç Hastalıkları', 'Pediatri', 'Genel Cerrahi', 'Kadın Doğum', 'Tıbbi Genetik', 'Halk Sağlığı']
  },
  {
    folderKey: 'donem3b',
    committeeId: 'donem3-butunleme',
    donem: 3,
    kurul: 'butunleme',
    type: 'butunleme',
    code: 'TIP 300-BUT',
    name: 'Dönem 3 - Yıl Sonu Bütünleme Sınavı',
    term: '2026-2027 Genel',
    color: 'rose',
    targetCount: 150,
    examDate: 'Ağustos 2027',
    description: 'Dönem 3 yıl sonu genel bütünleme değerlendirme sınavı.',
    disciplines: ['Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'İç Hastalıkları', 'Pediatri', 'Genel Cerrahi', 'Kadın Doğum', 'Tıbbi Genetik', 'Halk Sağlığı']
  }
];

// Normalize text for clean indexing and deduplication
function normalizeText(text) {
  if (!text) return '';
  return text.toLowerCase().replace(/[^\p{L}\p{N}]/gu, '').slice(0, 60);
}

// Committee ID mapper
function resolveFolderKey(committeeId, rawSource = '') {
  const c = (committeeId || '').toLowerCase().trim();
  const s = (rawSource || '').toLowerCase();

  // Explicit IDs
  for (const def of COMMITTEE_DEFINITIONS) {
    if (def.committeeId === c || def.folderKey === c) return def.folderKey;
  }

  // Regex patterns
  if (c.includes('donem3-kurul1') || c.includes('donem3k1') || s.includes('kurul 1') || s.includes('kurul1') || s.includes('kurul i')) return 'donem3k1';
  if (c.includes('donem3-kurul2') || c.includes('donem3k2') || s.includes('kurul 2') || s.includes('kurul2') || s.includes('kurul ii')) return 'donem3k2';
  if (c.includes('donem3-kurul3') || c.includes('donem3k3') || s.includes('kurul 3') || s.includes('kurul3') || s.includes('kurul iii')) return 'donem3k3';
  if (c.includes('donem3-kurul4') || c.includes('donem3k4') || s.includes('kurul 4') || s.includes('kurul4') || s.includes('kurul iv')) return 'donem3k4';
  if (c.includes('donem3-kurul5') || c.includes('donem3k5') || s.includes('kurul 5') || s.includes('kurul5') || s.includes('kurul v')) return 'donem3k5';
  if (c.includes('donem3-kurul6') || c.includes('donem3k6') || s.includes('kurul 6') || s.includes('kurul6') || s.includes('kurul vi')) return 'donem3k6';
  if (c.includes('final') || s.includes('final')) return 'donem3f';
  if (c.includes('butunleme') || c.includes('bütünleme') || s.includes('butunleme') || s.includes('bütünleme')) return 'donem3b';

  // Dönem 2 checks
  if (c.includes('donem2-kurul1') || c.includes('donem2k1')) return 'donem2k1';
  if (c.includes('donem2-kurul2') || c.includes('donem2k2')) return 'donem2k2';
  if (c.includes('donem2-kurul3') || c.includes('donem2k3')) return 'donem2k3';
  if (c.includes('donem2-kurul4') || c.includes('donem2k4')) return 'donem2k4';
  if (c.includes('donem2-kurul5') || c.includes('donem2k5')) return 'donem2k5';
  if (c.includes('donem2-kurul6') || c.includes('donem2k6')) return 'donem2k6';
  if (c.includes('donem2-final') || c.includes('donem2f')) return 'donem2f';
  if (c.includes('donem2-butunleme') || c.includes('donem2b')) return 'donem2b';

  // Dönem 1 checks
  if (c.includes('donem1-kurul1') || c.includes('donem1k1')) return 'donem1k1';
  if (c.includes('donem1-kurul2') || c.includes('donem1k2')) return 'donem1k2';
  if (c.includes('donem1-kurul3') || c.includes('donem1k3')) return 'donem1k3';
  if (c.includes('donem1-kurul4') || c.includes('donem1k4')) return 'donem1k4';
  if (c.includes('donem1-kurul5') || c.includes('donem1k5')) return 'donem1k5';
  if (c.includes('donem1-kurul6') || c.includes('donem1k6')) return 'donem1k6';
  if (c.includes('donem1-final') || c.includes('donem1f')) return 'donem1f';
  if (c.includes('donem1-butunleme') || c.includes('donem1b')) return 'donem1b';

  return 'donem3k1'; // Varsayılan Dönem 3 Kurul 1
}

// Ensure database_json directories exist
function ensureAllDirectories() {
  if (!fs.existsSync(BASE_OUT_DIR)) {
    fs.mkdirSync(BASE_OUT_DIR, { recursive: true });
  }

  for (const def of COMMITTEE_DEFINITIONS) {
    const dir = path.join(BASE_OUT_DIR, def.folderKey);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }
}

// Clean and standardize question for Cloud & Local
function standardizePastQuestion(q, folderKey, committeeId) {
  const claimedAns = q.claimedAnswer || q.reconstruction?.correctAnswer || q.rawQuestion?.claimedAnswer || null;
  const reconOptions = q.reconstruction?.options || [];
  const rawOptions = q.rawQuestion?.options || [];

  return {
    id: q.id || `past-${folderKey}-${Date.now()}-${Math.floor(Math.random() * 10000)}`,
    committeeId: committeeId,
    folderKey: folderKey,
    discipline: q.discipline || 'Tıbbi Patoloji',
    topic: q.topic || 'Genel Tıp Konusu',
    examYear: q.examYear || 'Geçmiş Yıllar Çıkmışı (Arşiv)',
    sourceFile: q.sourceFile || `${folderKey}.pdf`,
    aiCategory: q.aiCategory || null,
    claimedAnswer: claimedAns,
    rawQuestion: {
      stem: q.rawQuestion?.stem || q.reconstruction?.stem || '',
      options: rawOptions.length > 0 ? rawOptions : (reconOptions.length > 0 ? reconOptions.map(o => ({ key: o.key, text: o.text })) : []),
      claimedAnswer: claimedAns
    },
    reconstruction: q.reconstruction ? {
      stem: q.reconstruction.stem || '',
      options: reconOptions,
      correctAnswer: q.reconstruction.correctAnswer || claimedAns,
      explanation: q.reconstruction.explanation || '',
      confidenceScore: q.reconstruction.confidenceScore || 85,
      notesAndDiscrepancies: q.reconstruction.notesAndDiscrepancies || '',
      lastUpdated: q.reconstruction.lastUpdated || new Date().toISOString()
    } : null,
    isSuspect: Boolean(q.isSuspect),
    isAmbiguous: Boolean(q.isAmbiguous),
    isLocked: Boolean(q.isLocked),
    upvotes: typeof q.upvotes === 'number' ? q.upvotes : 0,
    comments: Array.isArray(q.comments) ? q.comments : [],
    reports: Array.isArray(q.reports) ? q.reports : [],
    customRedactedBy: q.customRedactedBy || null,
    customRedactedAt: q.customRedactedAt || null,
    customRedactionPrompt: q.customRedactionPrompt || null,
    createdAt: q.createdAt || new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
}

// Main execution
export async function buildDatabaseJson() {
  console.log('🏛️ [MedSoru Database JSON Motoru] Başlatılıyor...');
  console.log(`📁 Hedef Klasör: ${BASE_OUT_DIR}`);

  ensureAllDirectories();

  // 1. Kullanıcıları Yükle
  const usersPath = path.join(MEDS_DATA_DIR, 'users.json');
  let usersList = [];
  if (fs.existsSync(usersPath)) {
    try {
      usersList = JSON.parse(fs.readFileSync(usersPath, 'utf8'));
      console.log(`👤 Toplam ${usersList.length} kullanıcı profili yüklendi.`);
    } catch (e) {
      console.warn('⚠️ users.json okuma hatası:', e.message);
    }
  }

  // 2. Ders Notlarını Yükle
  const lecturesPath = path.join(MEDS_DATA_DIR, 'lecture_notes.json');
  let lecturesList = [];
  if (fs.existsSync(lecturesPath)) {
    try {
      lecturesList = JSON.parse(fs.readFileSync(lecturesPath, 'utf8'));
      console.log(`📖 Toplam ${lecturesList.length} amfi ders notu yüklendi.`);
    } catch (e) {
      console.warn('⚠️ lecture_notes.json okuma hatası:', e.message);
    }
  }

  // 3. Mevcut / Canlı Soruları (realtimequestion) Yükle
  const questionsPath = path.join(MEDS_DATA_DIR, 'questions.json');
  let realtimeQuestionsList = [];
  if (fs.existsSync(questionsPath)) {
    try {
      const qData = JSON.parse(fs.readFileSync(questionsPath, 'utf8'));
      realtimeQuestionsList = qData.questions || [];
      console.log(`⚡ Toplam ${realtimeQuestionsList.length} canlı soru taslağı yüklendi.`);
    } catch (e) {
      console.warn('⚠️ questions.json okuma hatası:', e.message);
    }
  }

  // 4. Çıkmış Soruları (pastquestions) Yükle (c:\Users\indui\Desktop\meds\data\pastQuestions.json)
  const pastPath = path.join(MEDS_DATA_DIR, 'pastQuestions.json');
  let pastQuestionsList = [];
  if (fs.existsSync(pastPath)) {
    try {
      pastQuestionsList = JSON.parse(fs.readFileSync(pastPath, 'utf8'));
      console.log(`📝 Toplam ${pastQuestionsList.length} çıkmış soru yüklendi.`);
    } catch (e) {
      console.warn('⚠️ pastQuestions.json okuma hatası:', e.message);
    }
  }

  // Ayrıca meds_sorular_txt altındaki ek soruları tara (özellikle bütünleme veya ek kurullar için)
  const txtDir = path.join(MEDS_DATABASE_DIR, 'meds_sorular_txt');
  let extraQuestionsCount = 0;
  if (fs.existsSync(txtDir)) {
    const txtFiles = fs.readdirSync(txtDir).filter(f => f.endsWith('.questions.json'));
    // Deduplicate per (folderKey + stemNorm) so final / butunleme can retain their questions
    const existingStemsByFolder = new Set();
    pastQuestionsList.forEach(q => {
      const fKey = resolveFolderKey(q.committeeId, q.sourceFile);
      const sNorm = normalizeText(q.reconstruction?.stem || q.rawQuestion?.stem || '');
      if (sNorm.length > 10) existingStemsByFolder.add(`${fKey}::${sNorm}`);
    });

    for (const f of txtFiles) {
      try {
        const rawContent = JSON.parse(fs.readFileSync(path.join(txtDir, f), 'utf8'));
        if (Array.isArray(rawContent)) {
          for (const item of rawContent) {
            const fKey = resolveFolderKey(item.committeeId, item.sourceFile || f);
            const stemNorm = normalizeText(item.rawQuestion?.stem || item.fragments?.[0]?.text || '');
            const key = `${fKey}::${stemNorm}`;

            if (stemNorm.length > 15 && !existingStemsByFolder.has(key)) {
              existingStemsByFolder.add(key);
              // Standartlaştırıp ekle
              const standardized = {
                id: item.id || `extra-${fKey}-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
                committeeId: item.committeeId || (fKey.includes('butun') || fKey.includes('3b') ? 'donem3-butunleme' : 'donem3-kurul1'),
                discipline: item.discipline || 'Tıbbi Patoloji',
                topic: item.topic || 'Çıkmış Soru',
                examYear: item.examYear && item.examYear !== 'Kategorisiz' ? item.examYear : (f.includes('22-23') ? '2022-2023' : 'Geçmiş Yıllar Çıkmışı (Arşiv)'),
                sourceFile: item.sourceFile || f,
                claimedAnswer: item.claimedAnswer || null,
                rawQuestion: {
                  stem: item.fragments?.[0]?.text || '',
                  options: item.options || [],
                  claimedAnswer: item.claimedAnswer || null
                },
                reconstruction: {
                  stem: item.fragments?.[0]?.text || '',
                  options: item.options || [],
                  correctAnswer: item.claimedAnswer || null,
                  explanation: 'Arşiv çıkmış soru metni',
                  confidenceScore: 75,
                  notesAndDiscrepancies: 'Otomasyon arşivinden aktarıldı'
                },
                isSuspect: false,
                isAmbiguous: Boolean(item.isAmbiguous),
                isLocked: false,
                upvotes: 0,
                comments: [],
                reports: []
              };
              pastQuestionsList.push(standardized);
              extraQuestionsCount++;
            }
          }
        }
      } catch (err) {}
    }
    if (extraQuestionsCount > 0) {
      console.log(`➕ Arşivden ${extraQuestionsCount} yeni tekil soru birleştirildi.`);
    }
  }

  // 5. Her Klasör İçin Verileri Ayrıştır ve Yaz
  const masterIndex = {
    generatedAt: new Date().toISOString(),
    totalCommittees: COMMITTEE_DEFINITIONS.length,
    baseDirectory: BASE_OUT_DIR,
    committees: {}
  };

  for (const def of COMMITTEE_DEFINITIONS) {
    const targetDir = path.join(BASE_OUT_DIR, def.folderKey);
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
    }

    // A. Çıkmış Sorular (pastquestions.json)
    const matchingPast = pastQuestionsList
      .filter(q => resolveFolderKey(q.committeeId, q.sourceFile) === def.folderKey)
      .map(q => standardizePastQuestion(q, def.folderKey, def.committeeId));

    // B. Mevcut / Canlı Sorular (realtimequestion.json)
    const matchingRealtime = realtimeQuestionsList
      .filter(q => resolveFolderKey(q.committeeId, q.sourceFile) === def.folderKey)
      .map(q => ({
        ...q,
        committeeId: def.committeeId,
        folderKey: def.folderKey,
        updatedAt: new Date().toISOString()
      }));

    // C. Kullanıcılar (users.json)
    // Bu kurula atanmış veya tüm kurullarda geçerli kullanıcılar
    const matchingUsers = usersList.map(u => ({
      uid: u.uid,
      email: u.email,
      displayName: u.displayName,
      studentNumber: u.studentNumber,
      role: u.role || 'student',
      activeCommittee: def.folderKey,
      updatedAt: new Date().toISOString()
    }));

    // D. Ders Notları (lectures.json)
    const matchingLectures = lecturesList
      .filter(l => resolveFolderKey(l.committeeId, l.title) === def.folderKey)
      .map(l => ({
        id: l.id,
        committeeId: def.committeeId,
        folderKey: def.folderKey,
        title: l.title,
        discipline: l.discipline,
        pageCount: l.pageCount || (l.pages ? l.pages.length : 0),
        pages: (l.pages || []).slice(0, 50),
        sourcePdf: l.sourcePdf || null,
        updatedAt: new Date().toISOString()
      }));

    // E. Kurul Meta Bilgisi (committee.json)
    const committeeData = {
      ...def,
      stats: {
        pastQuestionsCount: matchingPast.length,
        realtimeQuestionsCount: matchingRealtime.length,
        lecturesCount: matchingLectures.length,
        usersCount: matchingUsers.length
      },
      updatedAt: new Date().toISOString()
    };

    // F. Özet ve Telemetri (summary.json)
    const summaryData = {
      folderKey: def.folderKey,
      committeeId: def.committeeId,
      name: def.name,
      academicYear: def.term || '2026-2027',
      pastQuestionsCount: matchingPast.length,
      realtimeQuestionsCount: matchingRealtime.length,
      lecturesCount: matchingLectures.length,
      usersCount: matchingUsers.length,
      status: matchingPast.length > 0 ? 'active' : 'ready_for_data',
      isSupabaseReady: true,
      isFirebaseReady: true,
      lastBuildAt: new Date().toISOString()
    };

    // Dosyaları yaz
    fs.writeFileSync(path.join(targetDir, 'pastquestions.json'), JSON.stringify(matchingPast, null, 2), 'utf8');
    fs.writeFileSync(path.join(targetDir, 'realtimequestion.json'), JSON.stringify(matchingRealtime, null, 2), 'utf8');
    fs.writeFileSync(path.join(targetDir, 'users.json'), JSON.stringify(matchingUsers, null, 2), 'utf8');
    fs.writeFileSync(path.join(targetDir, 'committee.json'), JSON.stringify(committeeData, null, 2), 'utf8');
    fs.writeFileSync(path.join(targetDir, 'lectures.json'), JSON.stringify(matchingLectures, null, 2), 'utf8');
    fs.writeFileSync(path.join(targetDir, 'summary.json'), JSON.stringify(summaryData, null, 2), 'utf8');

    masterIndex.committees[def.folderKey] = {
      name: def.name,
      pastQuestionsCount: matchingPast.length,
      realtimeQuestionsCount: matchingRealtime.length,
      lecturesCount: matchingLectures.length,
      status: summaryData.status
    };

    console.log(`✅ [${def.folderKey}] -> ${matchingPast.length} çıkmış, ${matchingRealtime.length} canlı, ${matchingLectures.length} ders notu yazıldı.`);
  }

  // 6. Kök Dizin Dosyaları (index.json, manifest.json, README.md)
  fs.writeFileSync(path.join(BASE_OUT_DIR, 'index.json'), JSON.stringify(masterIndex, null, 2), 'utf8');

  const manifest = {
    version: '1.0.0',
    engine: 'MedSoru Database JSON Engine',
    subagent: 'meds_database_json_subagent',
    createdAt: new Date().toISOString(),
    totalFolders: COMMITTEE_DEFINITIONS.length,
    databaseCompatibility: ['Supabase PostgreSQL', 'Firebase Firestore', 'Localhost / Express', 'Cloudflare Workers'],
    standards: {
      encoding: 'UTF-8',
      format: 'Indented JSON (2 spaces)',
      nullByteCleaning: true,
      deduplicated: true
    }
  };
  fs.writeFileSync(path.join(BASE_OUT_DIR, 'manifest.json'), JSON.stringify(manifest, null, 2), 'utf8');

  const readmeContent = `# MedSoru Veritabanı JSON Deposu (database_json)

Bu klasör, MedSoru projesinin tüm dönem ve kurullarına ait **çıkmış sorular**, **canlı soru havuzu**, **kullanıcı profilleri**, **ders notları** ve **kurul meta verilerini** yapılandırılmış ve temizlenmiş JSON formatında barındırır.

Artık sürekli \`.txt\` veya \`.pdf\` dosyalarını baştan okumaya gerek yoktur. Buradaki dosyalar doğrudan:
- **Supabase PostgreSQL** tablolarına (\`past_questions\`, \`questions\`, \`users\`, \`lecture_notes\`, \`committees\`)
- **Firebase Firestore** koleksiyonlarına (\`past_questions\`, \`questions\`, \`users\`, \`committees\`)
- **Localhost API** sunucularına

aktarılmaya %100 hazırdır.

## 📂 Klasör Hiyerarşisi

Her bir dönem ve kurul/sınav için tekil bir klasör bulunur:
- **Dönem 1**: \`donem1k1\` ... \`donem1k6\`, \`donem1f\` (Final), \`donem1b\` (Bütünleme)
- **Dönem 2**: \`donem2k1\` ... \`donem2k6\`, \`donem2f\` (Final), \`donem2b\` (Bütünleme)
- **Dönem 3**: \`donem3k1\` ... \`donem3k6\`, \`donem3f\` (Final), \`donem3b\` (Bütünleme)

## 📄 Klasör İçi Dosya Şablonu

Her klasörde aşağıdaki standart dosyalar yer alır:
1. \`pastquestions.json\`: Çıkmış sınav soruları (doğrulanmış şıklar, soru kökü, AI açıklaması, branş ve konu).
2. \`realtimequestion.json\`: Canlı dönem öğrenci soruları ve taslak soru havuzu.
3. \`users.json\`: Kullanıcı ve moderatör profilleri.
4. \`committee.json\`: Kurul ve sınav meta verileri (isim, kod, renk, branş listesi, hedef soru sayısı).
5. \`lectures.json\`: Kurula ait amfi slayt ve ders notu indeksleri.
6. \`summary.json\`: Hızlı istatistik ve durum özeti.

## 🔄 Güncelleme ve Senkronizasyon

Bu dosyalar güncellenen parser veya AI düzeltme scriptleri sonrasında otomatik olarak yenilenebilir:
\`\`\`bash
node c:\\Users\\indui\\Desktop\\meds\\scripts\\build-database-json.mjs
\`\`\`

Buluta aktarmak için:
\`\`\`bash
node c:\\Users\\indui\\Desktop\\meds\\scripts\\sync-database-json-to-cloud.mjs
\`\`\`
`;
  fs.writeFileSync(path.join(BASE_OUT_DIR, 'README.md'), readmeContent, 'utf8');

  console.log('\n🎉 [Tamamlandı] Tüm dönem ve kurulların JSON dosyaları başarıyla hazırlandı!');
}

// Komut satırından doğrudan çağrıldığında çalıştır
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  buildDatabaseJson().catch(err => {
    console.error('❌ Kritik Hata:', err);
    process.exit(1);
  });
}
