/**
 * scripts/backup-local-to-cloud.mjs
 * 
 * Yerel Supabase (Docker) veritabanındaki verileri
 * Cloud Supabase (https://kgutsltgmqbnlxcnzrtl.supabase.co) üzerine
 * yedekler.
 */

import dotenv from 'dotenv';
import { createClient } from '@supabase/supabase-js';

dotenv.config();

const LOCAL_URL = process.env.LOCAL_SUPABASE_URL || 'http://localhost:8000';
const LOCAL_KEY = process.env.LOCAL_SUPABASE_KEY || process.env.SUPABASE_SECRET_KEY;

const CLOUD_URL = process.env.CLOUD_SUPABASE_URL || 'https://kgutsltgmqbnlxcnzrtl.supabase.co';
const CLOUD_KEY = process.env.CLOUD_SUPABASE_SECRET_KEY;

if (!LOCAL_URL || !LOCAL_KEY) {
  console.error('❌ Hata: Yerel Supabase bağlantı anahtarları bulunamadı.');
  process.exit(1);
}

if (!CLOUD_URL || !CLOUD_KEY) {
  console.error('❌ Hata: Cloud Supabase bağlantı anahtarları bulunamadı.');
  process.exit(1);
}

const localClient = createClient(LOCAL_URL, LOCAL_KEY);
const cloudClient = createClient(CLOUD_URL, CLOUD_KEY);

function cleanForPostgres(data) {
  if (data === null || data === undefined) return data;
  if (typeof data === 'string') return data.replace(/\u0000/g, '').replace(/\x00/g, '');
  if (Array.isArray(data)) return data.map(cleanForPostgres);
  if (typeof data === 'object') {
    const cleaned = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = cleanForPostgres(v);
    }
    return cleaned;
  }
  return data;
}

async function runBackup() {
  console.log('====================================================');
  console.log('☁️ Yerel Supabase -> Online Supabase Bulut Yedekleme');
  console.log('====================================================');
  console.log(`Kaynak:  ${LOCAL_URL}`);
  console.log(`Hedef:   ${CLOUD_URL}`);
  console.log('');

  // 1. Kurullar
  console.log('📚 [1/4] Kurullar aktarılıyor...');
  const { data: committees, error: commErr } = await localClient.from('committees').select('*');
  if (commErr) {
    console.warn('Kurullar okunamadı:', commErr.message);
  } else if (committees?.length) {
    const cleaned = committees.map(cleanForPostgres);
    const { error } = await cloudClient.from('committees').upsert(cleaned, { onConflict: 'id' });
    if (error) console.error('Kurul yükleme hatası:', error.message);
    else console.log(`✅ ${cleaned.length} kurul Cloud Supabase'e yedeklendi.`);
  }

  // 2. Aktif Sorular
  console.log('❓ [2/4] Aktif öğrenci soruları aktarılıyor...');
  const { data: questions, error: qErr } = await localClient.from('questions').select('*');
  if (qErr) {
    console.warn('Sorular okunamadı:', qErr.message);
  } else if (questions?.length) {
    const cleaned = questions.map(cleanForPostgres);
    for (let i = 0; i < cleaned.length; i += 50) {
      await cloudClient.from('questions').upsert(cleaned.slice(i, i + 50), { onConflict: 'id' });
    }
    console.log(`✅ ${cleaned.length} aktif soru Cloud Supabase'e yedeklendi.`);
  }

  // 3. Kullanıcılar
  console.log('👤 [3/4] Kullanıcı profilleri aktarılıyor...');
  const { data: users, error: uErr } = await localClient.from('users').select('*');
  if (uErr) {
    console.warn('Kullanıcılar okunamadı:', uErr.message);
  } else if (users?.length) {
    const cleaned = users.map(cleanForPostgres);
    const { error } = await cloudClient.from('users').upsert(cleaned, { onConflict: 'uid' });
    if (error) console.error('Kullanıcı yükleme hatası:', error.message);
    else console.log(`✅ ${cleaned.length} kullanıcı Cloud Supabase'e yedeklendi.`);
  }

  // 4. Çıkmış Sorular (isteğe bağlı parça parça kontrol)
  console.log('📝 [4/4] Çıkmış soru sayısı kontrol ediliyor...');
  const { count: localCount } = await localClient.from('past_questions').select('*', { count: 'exact', head: true });
  const { count: cloudCount } = await cloudClient.from('past_questions').select('*', { count: 'exact', head: true });
  console.log(`Yerel Çıkmış Soru: ${localCount || 0} | Bulut Çıkmış Soru: ${cloudCount || 0}`);

  if (localCount && localCount > (cloudCount || 0)) {
    console.log(`Eksik ${localCount - (cloudCount || 0)} çıkmış soru buluta yedekleniyor...`);
    const { data: pqs } = await localClient.from('past_questions').select('*');
    if (pqs?.length) {
      const cleaned = pqs.map(cleanForPostgres);
      for (let i = 0; i < cleaned.length; i += 50) {
        await cloudClient.from('past_questions').upsert(cleaned.slice(i, i + 50), { onConflict: 'id' });
        process.stdout.write(`\rİlerleme: ${Math.min(i + 50, cleaned.length)} / ${cleaned.length}`);
      }
      console.log('\n✅ Tüm çıkmış sorular buluta eşitlendi.');
    }
  }

  console.log('');
  console.log('🎉 [BAŞARILI] Online Supabase bulut yedeklemesi tamamlandı!');
}

runBackup().catch((e) => {
  console.error('Yedekleme sırasında beklenmedik hata:', e);
});
