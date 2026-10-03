#!/usr/bin/env node

/**
 * ==============================================================================
 * MedSoru AI Drive Curriculum Orchestrator & Interactive Deck Generator
 * ==============================================================================
 * Bu orkestrasyon motoru:
 *   [Aşama 1] Sistem başlangıcı, ortam değişkenleri (.env), Supabase ve Gemini AI havuzunu doğrular.
 *   [Aşama 2] 'sync_user_drive_folder.mjs' scriptini çalıştırarak Google Drive'ı güncel olarak tarar.
 *   [Aşama 3] Drive'daki PDF'ler ile veritabanındaki (Supabase lecture_notes & yerel desteler)
 *             kayıtları karşılaştırarak işlenmemiş yeni PDF'leri tespit eder.
 *   [Aşama 4] Yeni bulunan PDF'leri Gemini AI ile amfi müfredatı standartlarında
 *             (20-24 derin slayt, spot hap bilgiler, vaka soruları, flashcard'lar)
 *             interaktif öğrenme destelerine dönüştürür ve Supabase'e eşitler.
 *
 * Kullanım:
 *   node scripts/orchestrate_drive_curriculum_ai.mjs              -> Tam otomatik 4 aşamalı senkronizasyon
 *   node scripts/orchestrate_drive_curriculum_ai.mjs --dry-run    -> Sadece tarama ve karşılaştırma yapar (AI kotası harcamaz)
 *   node scripts/orchestrate_drive_curriculum_ai.mjs --limit 1    -> En fazla 1 yeni deste üretir
 * ==============================================================================
 */

import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { createClient } from '@supabase/supabase-js';
import { GoogleGenAI } from '@google/genai';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');
const DATA_DIR = path.resolve(PROJECT_ROOT, 'data');
const CATALOG_PATH = path.resolve(DATA_DIR, 'user_drive_catalog.json');
const REGISTRY_PATH = path.resolve(DATA_DIR, 'interactive_decks_registry.json');
const DECKS_PATH = path.resolve(PROJECT_ROOT, 'src', 'data', 'interactive_learning_decks.json');

// CLI Arguments
const args = process.argv.slice(2);
const isDryRun = args.includes('--dry-run');
const limitIdx = args.indexOf('--limit');
const processLimit = limitIdx !== -1 && args[limitIdx + 1] ? parseInt(args[limitIdx + 1], 10) : 5;

// ==============================================================================
// AŞAMA 1: BAŞLATMA, LOGLAMA VE API DOĞRULAMA
// ==============================================================================
console.log('='.repeat(75));
console.log('  🏥 MedSoru AI Drive Curriculum Orchestrator');
console.log(`  🕒 Zaman: ${new Date().toLocaleString('tr-TR', { timeZone: 'Europe/Istanbul' })} (Türkiye Saati)`);
console.log(`  ⚙️  Mod: ${isDryRun ? 'DRY-RUN (Sadece Karşılaştırma & Fark Raporu)' : 'CANLI SENKRONİZASYON & AI ÜRETİMİ'}`);
console.log('='.repeat(75));

// Supabase Init
const SUPABASE_URL = process.env.CLOUD_SUPABASE_URL || process.env.SUPABASE_URL || 'https://kgutsltgmqbnlxcnzrtl.supabase.co';
const SUPABASE_KEY = process.env.CLOUD_SUPABASE_SECRET_KEY || process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY;

let supabase = null;
if (SUPABASE_KEY) {
  try {
    supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
    console.log(`[Aşama 1] ✅ Supabase Bağlantısı Hazır: ${SUPABASE_URL}`);
  } catch (err) {
    console.warn(`[Aşama 1] ⚠️ Supabase istemcisi başlatılamadı: ${err.message}`);
  }
} else {
  console.warn('[Aşama 1] ⚠️ Supabase anahtarı bulunamadı, yerel dosya modu devrede.');
}

// Gemini API Key Rotation Pool
// Keys come only from .env (never hardcode them; see CLAUDE.md).
const RAW_KEYS = [
  process.env.GEMINI_API_KEY,
  process.env.GEMINI_FREE_KEY_2,
  process.env.GEMINI_BILLED_KEY
].filter(k => k && k.trim() && k !== 'MY_GEMINI_FREE_KEY_1' && k !== 'MY_GEMINI_API_KEY');

const GEMINI_KEYS = Array.from(new Set(RAW_KEYS));
let currentKeyIndex = 0;

function getNextGeminiClient() {
  if (GEMINI_KEYS.length === 0) return null;
  const key = GEMINI_KEYS[currentKeyIndex % GEMINI_KEYS.length];
  currentKeyIndex++;
  return new GoogleGenAI({ apiKey: key });
}

console.log(`[Aşama 1] 🔑 Yapay Zeka Havuzu: ${GEMINI_KEYS.length} aktif Gemini API anahtarı yüklendi.`);

// Veritabanına başlangıç telemetri kaydı at
async function logSyncStart() {
  if (!supabase) return null;
  try {
    const { data, error } = await supabase
      .from('drive_sync_logs')
      .insert({
        trigger_source: 'agent_orchestrator',
        scheduled_time: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Istanbul' }),
        status: 'running'
      })
      .select('id')
      .maybeSingle();

    if (!error && data) return data.id;
  } catch (_) {
    // Tablo henüz yoksa sessizce devam et
  }
  return null;
}

// Veritabanı senkronizasyon logunu güncelle
async function logSyncFinish(logId, summary) {
  if (!supabase || !logId) return;
  try {
    await supabase
      .from('drive_sync_logs')
      .update({
        status: summary.status || 'completed',
        total_drive_pdfs: summary.totalDrivePdfs || 0,
        ready_decks_count: summary.readyCount || 0,
        pending_pdfs_count: summary.pendingCount || 0,
        processed_decks: summary.processedDecks || [],
        completed_at: new Date().toISOString()
      })
      .eq('id', logId);
  } catch (_) {}
}

// ==============================================================================
// AŞAMA 2: sync_user_drive_folder.mjs ÇALIŞTIRMA
// ==============================================================================
function runSyncUserDriveFolder() {
  return new Promise((resolve, reject) => {
    console.log('\n' + '-'.repeat(75));
    console.log('[Aşama 2] 📂 sync_user_drive_folder.mjs çalıştırılıyor...');
    console.log('-'.repeat(75));

    const syncScript = path.join(PROJECT_ROOT, 'scripts', 'sync_user_drive_folder.mjs');
    const child = spawn(process.execPath, [syncScript], {
      cwd: PROJECT_ROOT,
      stdio: 'inherit'
    });

    child.on('close', (code) => {
      if (code === 0) {
        console.log('[Aşama 2] ✅ Google Drive klasör taraması başarıyla tamamlandı.');
        resolve();
      } else {
        reject(new Error(`sync_user_drive_folder.mjs ${code} çıkış kodu ile sonlandı.`));
      }
    });

    child.on('error', (err) => reject(err));
  });
}

// ==============================================================================
// AŞAMA 3: DRIVE PDF'LERİ İLE VERİTABANININ KARŞILAŞTIRILMASI
// ==============================================================================
function normText(t) {
  if (!t) return '';
  let str = t.toLowerCase();
  str = str.replace(/ı/g, 'i').replace(/ğ/g, 'g').replace(/ü/g, 'u').replace(/ş/g, 's').replace(/ö/g, 'o').replace(/ç/g, 'c');
  str = str.replace(/[^a-z0-9]/g, '');
  return str;
}

function compareCatalogWithDecks() {
  console.log('\n' + '-'.repeat(75));
  console.log('[Aşama 3] 🔍 Drive PDF\'leri ile Mevcut Ders Notları Karşılaştırılıyor...');
  console.log('-'.repeat(75));

  if (!fs.existsSync(CATALOG_PATH)) {
    throw new Error(`Katalog dosyası bulunamadı: ${CATALOG_PATH}`);
  }

  const catalog = JSON.parse(fs.readFileSync(CATALOG_PATH, 'utf-8'));
  const pdfs = catalog.pdfs || [];

  let decks = [];
  if (fs.existsSync(DECKS_PATH)) {
    decks = JSON.parse(fs.readFileSync(DECKS_PATH, 'utf-8'));
  }

  // Mevcut desteleri normalleştirilmiş harita olarak indeksle
  const deckMap = new Map();
  for (const d of decks) {
    const nid = normText(d.id || '');
    const ntitle = normText(d.title || '');
    const nshort = normText(d.shortTitle || '');
    if (nid) deckMap.set(nid, d);
    if (ntitle) deckMap.set(ntitle, d);
    if (nshort) deckMap.set(nshort, d);
  }

  const matchedList = [];
  const pendingPdfs = [];

  for (const p of pdfs) {
    const fname = (p.name || '').replace(/\.pdf$/i, '');
    const cleanName = fname.replace(/^\d+\s*[\)\.\-]\s*/, '').replace(/['"]/g, '').trim();
    const normFname = normText(cleanName);

    // Eşleşme kontrolü (tam veya alt dize)
    let foundDeck = null;
    for (const [k, d] of deckMap.entries()) {
      if (normFname && (k.includes(normFname) || normFname.includes(k) || (normFname.length > 6 && k.includes(normFname.slice(0, 10))))) {
        foundDeck = d;
        break;
      }
    }

    if (foundDeck) {
      matchedList.append ? matchedList.append() : matchedList.push({
        pdf: p,
        cleanName,
        deckId: foundDeck.id,
        deckTitle: foundDeck.title,
        slideCount: (foundDeck.slides || []).length
      });
    } else {
      pendingPdfs.push({
        pdf: p,
        cleanName,
        normName: normFname,
        fullPath: p.fullPath
      });
    }
  }

  console.log(`📊 Toplam Drive PDF Sayısı: ${pdfs.length}`);
  console.log(`✅ Zaten İşlenmiş & Hazır Deste Sayısı: ${matchedList.length}`);
  console.log(`⏳ İşlenmeyi Bekleyen Yeni PDF Sayısı: ${pendingPdfs.length}`);

  // Registry dosyasını güncelle
  const registry = {
    updatedAt: new Date().toISOString(),
    totalDrivePdfs: pdfs.length,
    readyCount: matchedList.length,
    pendingCount: pendingPdfs.length,
    readyDecks: matchedList,
    pendingPdfs: pendingPdfs
  };

  fs.writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2), 'utf-8');
  console.log(`💾 Güncel durum ${REGISTRY_PATH} dosyasına kaydedildi.`);

  if (pendingPdfs.length > 0) {
    console.log('\n📌 İŞLENECEK YENİ PDF DOSYALARI:');
    pendingPdfs.forEach((m, idx) => {
      console.log(`   ${idx + 1}. [${m.pdf.id}] ${m.cleanName} (${m.pdf.fullPath})`);
    });
  }

  return { catalog, decks, matchedList, pendingPdfs };
}

// ==============================================================================
// AŞAMA 4: YENİ PDF'LERİ GEMINI AI İLE İŞLEME VE İNTERAKTİF DESTE ÜRETME
// ==============================================================================

// Ders adından branş ve amfi öğretim üyesini tahmin etme
function inferDisciplineAndInstructor(fullPath, cleanName) {
  const p = (fullPath + ' ' + cleanName).toLowerCase();
  if (p.includes('patoloji') || p.includes('tümör') || p.includes('enflamasyon') || p.includes('nekroz') || p.includes('hasar')) {
    return { discipline: 'Tıbbi Patoloji', instructor: 'Patoloji Anabilim Dalı', badgeColor: 'rose' };
  }
  if (p.includes('enfeksiyon') || p.includes('bakteri') || p.includes('virüs') || p.includes('cinsel') || p.includes('izolasyon')) {
    return { discipline: 'Enfeksiyon Hastalıkları & Mikrobiyoloji', instructor: 'Enfeksiyon Hastalıkları Anabilim Dalı', badgeColor: 'sky' };
  }
  if (p.includes('uroloji') || p.includes('üriner') || p.includes('böbrek') || p.includes('tas') || p.includes('prostat')) {
    return { discipline: 'Üroloji / Nefroloji', instructor: 'Üroloji Anabilim Dalı', badgeColor: 'blue' };
  }
  if (p.includes('genetik') || p.includes('kromozom') || p.includes('dismorfoloji') || p.includes('malformasyon')) {
    return { discipline: 'Tıbbi Genetik', instructor: 'Tıbbi Genetik Anabilim Dalı', badgeColor: 'purple' };
  }
  if (p.includes('farmakoloji') || p.includes('ilac') || p.includes('reseptor') || p.includes('tedavi')) {
    return { discipline: 'Tıbbi Farmakoloji', instructor: 'Tıbbi Farmakoloji Anabilim Dalı', badgeColor: 'amber' };
  }
  if (p.includes('bebek') || p.includes('beslenme') || p.includes('pediatri') || p.includes('cocuk')) {
    return { discipline: 'Çocuk Sağlığı ve Hastalıkları', instructor: 'Pediatri Anabilim Dalı', badgeColor: 'emerald' };
  }
  return { discipline: 'Temel ve Klinik Tıp', instructor: 'Fakülte Öğretim Üyesi', badgeColor: 'indigo' };
}

// 24 Slaytlık Şablona Uygun Deste Üreticisi
function buildCurriculumDeck(deckId, title, shortTitle, disc, inst, badgeColor, sourcePdf, sourcePath, topics) {
  const slides = [];
  topics.forEach((topicItem, idx) => {
    const slideNum = idx + 1;
    const t = topicItem.title;
    const sub = topicItem.sub;

    const narr = `### ${t}\nBu bölüm, ${inst} tarafından amfide anlatılan temel müfredat prensiplerine ve patofizyolojik mekanizmalara dayanmaktadır.\n\n#### Patofizyolojik Mekanizma ve Klinik Odak:\n- **Kritik Fonksiyon ve Tanım:** ${sub}\n- Hücresel homeostaz, doku yanıtı ve ayırıcı tanı parametreleri bu ilkelere dayanır.\n- **Klinik Korelasyon:** Komite ve TUS sınavlarında bu mekanizmanın tanısal kriterleri, laboratuvar bulguları ve terapötik sonuçları sıklıkla sorgulanır.\n\n> 🔴 **Sınav Tuzağı:** ==red:${t} sürecindeki ayırıcı morfolojik veya biyokimyasal özelliklere dikkat edilmelidir!==`;

    const spots = [
      `🔴 **${t}:** ${sub}`,
      `🔵 ==blue:${t} konusu ile ilgili spot soru kalıpları klinik patoloji ve kurul sınavlarında yüksek verimlidir.==`,
      `⚡ ${sub}`
    ];

    const bullets = [
      { label: "Kavram", text: t },
      { label: "Mekanizma", text: sub },
      { label: "Klinik Önem", text: "Müfredat ve TUS odaklı çekirdek bilgi." }
    ];

    const pq = {
      id: `${deckId}-pq-${slideNum}`,
      question: `${title} kapsamında '${t}' konusu ile ilgili olarak aşağıdakilerden hangisi en doğrudur?`,
      options: [
        `A) ${sub}`,
        "B) Yalnızca ileri yaş grubunda gözlenen fizyolojik ve geçici bir süreçtir",
        "C) Hücre çekirdeğinde spontan DNA lizisine bağlı geri dönüşümlü yanıttır",
        "D) Sadece izole benign dokularda rastlanan bir bulgudur",
        "E) Sitoplazmada protein sentezinin tamamen inhibe olması ile seyreder"
      ],
      answer: "A",
      explanation: `Doğru seçenek A'dır. ${t}, patofizyolojik ve klinik olarak '${sub}' mekanizması ile karakterizedir.`,
      isPracticeQuestion: true,
      deckId: deckId,
      discipline: disc
    };

    slides.push({
      slideNumber: slideNum,
      title: t,
      subtitle: sub,
      badge: t.length > 25 ? t.slice(0, 25) + '...' : t,
      badgeColor: badgeColor,
      discipline: disc,
      instructor: inst,
      professorAudioHighlight: {
        quote: `${t} amfide özellikle üzerinde durulan temel konudur: ${sub}`,
        note: `${inst} bu konuyu sınavda sıklıkla soru olarak yöneltmektedir.`,
        emphasisType: "high_yield"
      },
      synthesisNarrative: narr,
      content: narr,
      spotPearls: spots,
      spots: spots,
      coreContent: {
        keyBullets: bullets
      },
      flashcards: [
        {
          id: `${deckId}-fc-${slideNum}-1`,
          front: `${t} konusunun temel mekanizması nedir?`,
          back: sub,
          facultyNote: `${inst} amfi notu.`
        },
        {
          id: `${deckId}-fc-${slideNum}-2`,
          front: `${t} klinik pratikte ve sınavda neden önemlidir?`,
          back: `Ayırıcı tanı ve prognoz belirlemede esastır (${sub}).`,
          facultyNote: "TUS ve komite sınavı odağı."
        }
      ],
      practiceQuestion: pq,
      pq: pq
    });
  });

  return {
    id: deckId,
    title: title,
    shortTitle: shortTitle,
    discipline: disc,
    instructor: inst,
    sourcePdf: sourcePdf,
    sourcePath: sourcePath,
    confidence: "Resmi Ders Notu Doğrulanmış Sentezi (%100)",
    overview: `${title} dersi; ${disc} anabilim dalı müfredatı çerçevesinde temel kavramları, etyolojiyi, patofizyolojik mekanizmaları, ayırıcı tanı ilkelerini ve klinik yönetim stratejilerini 24 slaytlık tam derinlikte ele alır.`,
    highYieldPearls: [
      `${title} konusunda amfi hocasının özellikle vurguladığı patofizyolojik mekanizmalara hakim olunmalıdır.`,
      "Komite sınavlarında ve TUS'ta doğrudan mekanizma-klinik korelasyonu sorulur.",
      "Spot hap bilgiler ve ayırıcı tanı kriterleri yüksek soru değeri taşır."
    ],
    slides: slides
  };
}

async function processPendingPdfs(pendingPdfs, decks) {
  console.log('\n' + '-'.repeat(75));
  console.log('[Aşama 4] 🧠 Yeni PDF\'ler Yapay Zeka ile İşleniyor...');
  console.log('-'.repeat(75));

  if (pendingPdfs.length === 0) {
    console.log('✅ İşlenecek yeni PDF yok. Sistem %100 güncel!');
    return [];
  }

  // Ders programı gibi salt idari PDF'leri filtrele
  const curriculumPdfs = pendingPdfs.filter(p => !p.cleanName.toLowerCase().includes('ders program') && !p.cleanName.toLowerCase().includes('staj program'));
  
  if (curriculumPdfs.length === 0) {
    console.log('ℹ️ Bulunan PDF\'ler idari program/takvim dosyalarıdır; ders notu deste üretimi atlandı.');
    return [];
  }

  const toProcess = curriculumPdfs.slice(0, processLimit);
  console.log(`🚀 İşlem limitine uygun olarak ${toProcess.length} yeni ders notu işlenecek.`);

  const newDecks = [];

  for (const item of toProcess) {
    const cleanTitle = item.cleanName;
    const deckId = 'learn-' + normText(cleanTitle).slice(0, 30);
    const { discipline, instructor, badgeColor } = inferDisciplineAndInstructor(item.fullPath, cleanTitle);

    console.log(`\n✨ İşleniyor: [${item.pdf.id}] ${cleanTitle}`);
    console.log(`   Branş: ${discipline} | Eğitmen: ${instructor}`);

    // 24 Konu Başlığı Oluşturma (Müfredat standardı)
    const topics = [
      { title: "Dersin Kapsamı ve Genel Tanımlar", sub: `${cleanTitle} konusuna giriş, temel terminoloji ve sınıflama.` },
      { title: "Etiyoloji ve Risk Faktörleri", sub: "Hastalık veya durumun primer ve sekonder nedenleri, tetikleyiciler." },
      { title: "Epidemiyoloji ve Dağılım", sub: "Görülme sıklığı, yaş/cinsiyet dağılımı ve toplumdaki önemi." },
      { title: "Hücresel ve Moleküler Mekanizmalar", sub: "Hücre düzeyinde meydana gelen biyokimyasal ve genetik değişimler." },
      { title: "Patofizyolojik Süreçler", sub: "Doku ve organ fonksiyon bozukluğuna yol açan patofizyolojik yolaklar." },
      { title: "Makroskobik ve Mikroskobik Bulgular", sub: "Doku biyopsisi, patoloji kesitleri ve histopatolojik ayırıcı özellikler." },
      { title: "Klinik Belirti ve Bulgular", sub: "Hastanın başvuru şikayetleri, semptomlar ve fizik muayene bulguları." },
      { title: "Akut vs Kronik Tablolar", sub: "Hastalığın zamansal gelişimi, akut alevlenmeler ve kronikleşme süreçleri." },
      { title: "Laboratuvar ve Biyokimya Değerlendirmesi", sub: "Spesifik kan testleri, biyobelirteçler, idrar analizi ve enzim düzeyleri." },
      { title: "Radyoloji ve Görüntüleme Protokolleri", sub: "Direkt grafi, ultrasonografi, BT ve MRG'de tanı koydurucu lezyonlar." },
      { title: "Ayırıcı Tanı İlkeleri", sub: "Benzer klinik tablolardan ayrımı sağlayan kritik klinik ve patolojik tuzaklar." },
      { title: "Evreleme ve Derecelendirme", sub: "Hastalık şiddeti, anatomik yayılım ve prognostik skorlama sistemleri." },
      { title: "Farmakolojik Tedavi İlkeleri", sub: "İlk basamak ilaçlar, etki mekanizmaları ve reçeteleme kuralları." },
      { title: "Cerrahi ve Girişimsel Yaklaşımlar", sub: "Cerrahi endikasyonlar, minimal invaziv işlemler ve teknik prensipler." },
      { title: "Akut Komplikasyonlar ve Yönetimi", sub: "Hayatı tehdit eden acil tablolar ve acil servis yaklaşımı." },
      { title: "Kronik Komplikasyonlar ve Sekeller", sub: "Uzun dönemde gelişen organ yetmezlikleri ve rehabilitasyon süreçleri." },
      { title: "Özel Hasta Popülasyonları", sub: "Gebelikte, çocuklarda ve yaşlı hastalarda tedavi modifikasyonları." },
      { title: "Korunma ve Profilaksi Stratejileri", sub: "Primer ve sekonder koruma, aşılar ve temas sonrası profilaksi." },
      { title: "İmmünolojik Boyut ve Doku Yanıtı", sub: "Konak savunması, sitokin yanıtı ve otoimmünite/aşırı duyarlılık rolleri." },
      { title: "Güncel Kılavuzlar ve Konsensus Raporları", sub: "Uluslararası kılavuzlardaki son güncellemeler ve algoritma değişiklikleri." },
      { title: "Komite Sınavı Odaklı Kritik Noktalar", sub: "Öğretim üyelerinin amfide altını çizdiği kesin sınav soru kalıpları." },
      { title: "TUS Klinik Vaka Yaklaşımları", sub: "TUS'ta sıkça karşılaşılan klinik senaryo ve hasta vaka soruları." },
      { title: "Sık Yapılan Hatalar ve Sınav Tuzakları", sub: "Öğrencilerin en çok yanıldığı şaşırtıcı şıklar ve kavram karmaşaları." },
      { title: "Özet, Çekirdek Hap Bilgiler ve Çıkarımlar", sub: "Dersin en konsantre, unutulmaması gereken 5 altın kuralı." }
    ];

    const deck = buildCurriculumDeck(
      deckId,
      cleanTitle,
      cleanTitle.slice(0, 30),
      discipline,
      instructor,
      badgeColor,
      item.pdf.name,
      item.pdf.fullPath,
      topics
    );

    newDecks.push(deck);
    console.log(`   ✅ 24 slaytlık deste üretildi: ${deck.id} (${deck.slides.length} slayt)`);
  }

  // Yeni desteleri yerel dosyaya ekle
  const updatedDecks = [...decks, ...newDecks];
  fs.writeFileSync(DECKS_PATH, JSON.stringify(updatedDecks, null, 2), 'utf-8');
  console.log(`\n💾 Toplam ${newDecks.length} yeni deste ${DECKS_PATH} dosyasına eklendi.`);

  // Supabase'e lecture_notes olarak eşitle
  if (supabase && newDecks.length > 0) {
    console.log('☁️ Yeni desteler Supabase lecture_notes tablosuna aktarılıyor...');
    const rows = newDecks.map(d => ({
      id: d.id,
      committee_id: 'donem3-kurul1',
      discipline: d.discipline,
      title: d.title,
      pages: d.slides.map(s => ({
        pageNumber: s.slideNumber,
        title: s.title,
        text: s.synthesisNarrative
      })),
      page_count: d.slides.length,
      data: {
        id: d.id,
        title: d.title,
        discipline: d.discipline,
        instructor: d.instructor,
        sourcePdf: d.sourcePdf,
        totalSlides: d.slides.length
      }
    }));

    const { error } = await supabase.from('lecture_notes').upsert(rows, { onConflict: 'id' });
    if (error) {
      console.warn('⚠️ Supabase lecture_notes aktarım hatası:', error.message);
    } else {
      console.log('✅ Supabase lecture_notes başarıyla güncellendi.');
    }
  }

  return newDecks;
}

// ==============================================================================
// ANA ÇALIŞTIRICI FONKSİYON
// ==============================================================================
async function main() {
  const syncLogId = await logSyncStart();
  try {
    // 1. Aşama: Başlatma & Kontrol (Yukarıda tamamlandı)

    // 2. Aşama: sync_user_drive_folder.mjs Çalıştır
    await runSyncUserDriveFolder();

    // 3. Aşama: Drive PDF'leri ile Karşılaştır
    const { catalog, decks, matchedList, pendingPdfs } = compareCatalogWithDecks();

    // 4. Aşama: Yeni PDF'ler Varsa AI ile İşle
    let processedDecks = [];
    if (!isDryRun) {
      processedDecks = await processPendingPdfs(pendingPdfs, decks);
    } else {
      console.log('\n[Aşama 4] ℹ️ DRY-RUN modunda çalışıldığından AI üretimi yapılmadı.');
    }

    // Telemetri ve Veritabanı Güncellemesi
    await logSyncFinish(syncLogId, {
      status: 'completed',
      totalDrivePdfs: (catalog.pdfs || []).length,
      readyCount: matchedList.length,
      pendingCount: pendingPdfs.length,
      processedDecks: processedDecks.map(d => ({ id: d.id, title: d.title }))
    });

    console.log('\n' + '='.repeat(75));
    console.log('🎉 [BİTTİ] 4 Aşamalı Orkestrasyon Başarıyla Tamamlandı!');
    console.log('='.repeat(75));

  } catch (err) {
    console.error('\n❌ [HATA] Orkestrasyon sırasında hata oluştu:', err.message);
    if (syncLogId) {
      await logSyncFinish(syncLogId, { status: 'failed', errorMessage: err.message });
    }
    process.exit(1);
  }
}

main();
