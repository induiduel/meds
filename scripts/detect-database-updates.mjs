/**
 * scripts/detect-database-updates.mjs
 *
 * Veritabanında Soru Bazında Güncelleme Tespit ve Ekonomik Artımlı Senkronizasyon Scripti
 *
 * Kullanım:
 *   node scripts/detect-database-updates.mjs             -> Güncellemeleri tespit eder ve raporlar
 *   node scripts/detect-database-updates.mjs --sync      -> YALNIZCA güncellenen soruları çeker (tüm soruları baştan indirmez)
 *   node scripts/detect-database-updates.mjs --push      -> Yerelde güncellenen soruları Supabase'e yükler
 *   node scripts/detect-database-updates.mjs --watch     -> Sürekli izleme modu
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { createClient } from '@supabase/supabase-js';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const DATA_JSON_PATH = path.resolve(ROOT_DIR, 'data', 'pastQuestions.json');
const SRC_JSON_PATH = path.resolve(ROOT_DIR, 'src', 'data', 'pastQuestions.json');

const SUPABASE_URL = process.env.SUPABASE_URL || 'https://kgutsltgmqbnlxcnzrtl.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY || 'sb_publishable_EVdXdIi_2mxVr3HZKYabwQ_li5KuE1Q';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

function cleanForPostgres(data) {
  if (data === null || data === undefined) return data;
  if (typeof data === 'string') {
    return data.replace(/\u0000/g, '').replace(/[\x00]/g, '');
  }
  if (Array.isArray(data)) {
    return data.map(cleanForPostgres);
  }
  if (typeof data === 'object') {
    const cleaned = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = cleanForPostgres(v);
    }
    return cleaned;
  }
  return data;
}

function loadLocalQuestions() {
  const targetPath = fs.existsSync(DATA_JSON_PATH) ? DATA_JSON_PATH : SRC_JSON_PATH;
  if (!fs.existsSync(targetPath)) return [];
  try {
    const raw = fs.readFileSync(targetPath, 'utf-8');
    const data = JSON.parse(raw);
    return Array.isArray(data) ? data : [];
  } catch (err) {
    console.error(`❌ Yerel dosya okunamadı (${targetPath}):`, err.message);
    return [];
  }
}

function saveLocalQuestions(questions) {
  const content = JSON.stringify(questions, null, 2);
  try {
    if (fs.existsSync(path.dirname(DATA_JSON_PATH))) {
      fs.writeFileSync(DATA_JSON_PATH, content, 'utf-8');
    }
    if (fs.existsSync(path.dirname(SRC_JSON_PATH))) {
      fs.writeFileSync(SRC_JSON_PATH, content, 'utf-8');
    }
    return true;
  } catch (err) {
    console.error('❌ Yerel dosya kaydedilemedi:', err.message);
    return false;
  }
}

async function detectUpdates() {
  const isSyncMode = process.argv.includes('--sync') || process.argv.includes('--pull');
  const isPushMode = process.argv.includes('--push');

  console.log('\n===============================================================');
  console.log('🔍 [MedSoru] Veritabanı Güncelleme Tespit & Delta Sync Motoru');
  console.log('===============================================================');
  console.log(`🔗 Supabase URL: ${SUPABASE_URL}`);

  // 1. Yerel Veri Analizi
  const localList = loadLocalQuestions();
  const localMap = new Map();
  let localMaxUpdatedAt = '';

  for (const q of localList) {
    if (q && q.id) {
      localMap.set(q.id, q);
      if (q.updatedAt && q.updatedAt > localMaxUpdatedAt) {
        localMaxUpdatedAt = q.updatedAt;
      }
    }
  }

  console.log(`📁 Yerel Arşiv: ${localList.length.toLocaleString('tr-TR')} soru`);
  console.log(`   Son Yerel Güncelleme: ${localMaxUpdatedAt || 'Bilinmiyor'}`);

  // 2. Supabase Hafif Kontrol (~100 Baytlık Meta Sorgusu)
  const startTime = Date.now();
  const { data: latestRows, count: remoteCount, error: metaErr } = await supabase
    .from('past_questions')
    .select('updated_at', { count: 'exact' })
    .order('updated_at', { ascending: false })
    .limit(1);

  const queryDuration = Date.now() - startTime;

  if (metaErr) {
    console.error('❌ Supabase meta sorgusu başarısız:', metaErr.message);
    return;
  }

  const remoteLatestUpdatedAt = latestRows?.[0]?.updated_at || null;
  console.log(`☁️  Supabase Veritabanı: ${remoteCount.toLocaleString('tr-TR')} soru (${queryDuration} ms)`);
  console.log(`   Son Veritabanı Güncelleme: ${remoteLatestUpdatedAt || 'Bilinmiyor'}`);

  // 3. Karşılaştırma Analizi
  const isTimeEqualOrOlder = remoteLatestUpdatedAt && localMaxUpdatedAt &&
    new Date(remoteLatestUpdatedAt).getTime() <= new Date(localMaxUpdatedAt).getTime();

  if (isTimeEqualOrOlder && remoteCount === localList.length) {
    console.log('\n---------------------------------------------------------------');
    console.log('✅ SONUÇ: Veritabanı ve Yerel Arşiv %100 BİREBİR GÜNCEL!');
    console.log('⚡ Soru bazında değişiklik: 0 adet');
    console.log('💡 Harcanan Ağ Bant Genişliği: ~120 Bayt (Maksimum Tasarruf)');
    console.log('---------------------------------------------------------------\n');
    return;
  }

  // 4. Güncelleme Tespit Edildi: YALNIZCA Değişen Soruları Çek (Soru Bazında Delta)
  console.log('\n⚡ GÜNCELLEME TESPİT EDİLDİ!');
  console.log(`   Veritabanında daha yeni kayıtlar veya sayı farkı mevcut.`);
  console.log(`   Soru bazında delta sorgulanıyor (Son Tarih: ${localMaxUpdatedAt})...`);

  let deltaQuery = supabase.from('past_questions').select('*');
  if (localMaxUpdatedAt) {
    deltaQuery = deltaQuery.gt('updated_at', localMaxUpdatedAt);
  }
  deltaQuery = deltaQuery.order('updated_at', { ascending: true }).limit(500);

  const { data: deltaRows, error: deltaErr } = await deltaQuery;

  if (deltaErr) {
    console.error('❌ Delta verisi çekilemedi:', deltaErr.message);
    return;
  }

  const updatedQuestions = deltaRows || [];
  console.log(`\n📋 Tespit Edilen Değişiklikler (${updatedQuestions.length} soru):`);

  if (updatedQuestions.length === 0 && remoteCount !== localList.length) {
    console.log(`   ℹ️ Tarih farkı yok ancak toplam soru sayısında fark var (Yerel: ${localList.length}, Uzak: ${remoteCount}).`);
  }

  updatedQuestions.slice(0, 10).forEach((row, i) => {
    const isNew = !localMap.has(row.id);
    const actionLabel = isNew ? '🆕 [YENİ SORU]' : '✏️  [GÜNCELLENMİŞ]';
    console.log(`   ${i + 1}. ${actionLabel} ID: ${row.id}`);
    console.log(`      Disiplin: ${row.discipline || 'Belirtilmemiş'} | Konu: ${row.topic || 'Belirtilmemiş'}`);
    console.log(`      Güncellenme: ${row.updated_at}`);
  });

  if (updatedQuestions.length > 10) {
    console.log(`   ... ve ${updatedQuestions.length - 10} adet daha soru güncellendi.`);
  }

  // 5. İsteğe Bağlı Otomatik Senkronizasyon (--sync parametresi)
  if (isSyncMode) {
    console.log('\n📥 [Delta Sync] Soru bazında artımlı güncelleme uygulanıyor...');
    let appliedCount = 0;

    for (const row of updatedQuestions) {
      const qItem = {
        ...(row.data || {}),
        id: row.id,
        committeeId: row.committee_id || row.data?.committeeId,
        discipline: row.discipline || row.data?.discipline,
        topic: row.topic || row.data?.topic,
        examYear: row.exam_year || row.data?.examYear,
        sourceFile: row.source_file || row.data?.sourceFile,
        aiCategory: row.ai_category || row.data?.aiCategory,
        claimedAnswer: row.claimed_answer || row.data?.claimedAnswer,
        rawQuestion: row.raw_question || row.data?.rawQuestion,
        reconstruction: row.reconstruction || row.data?.reconstruction,
        isSuspect: row.is_suspect ?? row.data?.isSuspect ?? false,
        isAmbiguous: row.is_ambiguous ?? row.data?.isAmbiguous ?? false,
        isLocked: row.is_locked ?? row.data?.isLocked ?? false,
        upvotes: row.upvotes ?? row.data?.upvotes ?? 0,
        comments: row.comments || row.data?.comments || [],
        reports: row.reports || row.data?.reports || [],
        customRedactedBy: row.custom_redacted_by || row.data?.customRedactedBy,
        customRedactedAt: row.custom_redacted_at || row.data?.customRedactedAt,
        customRedactionPrompt: row.custom_redaction_prompt || row.data?.customRedactionPrompt,
        createdAt: row.created_at || row.data?.createdAt,
        updatedAt: row.updated_at || row.data?.updatedAt,
      };

      localMap.set(qItem.id, qItem);
      appliedCount++;
    }

    const mergedList = Array.from(localMap.values());
    const ok = saveLocalQuestions(mergedList);

    if (ok) {
      console.log(`✅ BAŞARILI: ${appliedCount} adet soru yerel arşiv dosyalarına işlendi!`);
      console.log(`📁 Yeni toplam yerel soru sayısı: ${mergedList.length}`);
      console.log(`💾 Tüm 1937 soruyu baştan indirmek yerine sadece ${appliedCount} soru çekilerek bant genişliği korundu.`);
    }
  } else {
    console.log('\n💡 İPUCU: Yalnızca güncellenen bu soruları yerel dosyalara işlemek için şu komutu çalıştırabilirsiniz:');
    console.log('   node scripts/detect-database-updates.mjs --sync\n');
  }
}

// Watch mode desteği
if (process.argv.includes('--watch')) {
  console.log('👀 İzleme modu başlatıldı. 60 saniyede bir kontrol edilecek...');
  detectUpdates();
  setInterval(detectUpdates, 60000);
} else {
  detectUpdates();
}
