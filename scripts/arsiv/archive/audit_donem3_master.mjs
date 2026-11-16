import fs from 'fs';
import path from 'path';
import dotenv from 'dotenv';
import { createClient } from '@supabase/supabase-js';

dotenv.config();

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY;
const sb = createClient(supabaseUrl, supabaseKey);

const committees = [
  { key: 'donem3k1', id: 'donem3-kurul1', name: 'Kurul 1 (Ürogenital ve Obstetrik)' },
  { key: 'donem3k2', id: 'donem3-kurul2', name: 'Kurul 2 (Nöropsikiyatri)' },
  { key: 'donem3k3', id: 'donem3-kurul3', name: 'Kurul 3 (Gastrointestinal Sistem)' },
  { key: 'donem3k4', id: 'donem3-kurul4', name: 'Kurul 4 (Dolaşım, Solunum, Neoplazi)' },
  { key: 'donem3k5', id: 'donem3-kurul5', name: 'Kurul 5 (Kas-İskelet ve Hematoloji)' },
  { key: 'donem3k6', id: 'donem3-kurul6', name: 'Kurul 6 (Endokrin ve Yaşlanma)' },
  { key: 'donem3f',  id: 'donem3-final',  name: 'Dönem 3 Final Sınavı' },
  { key: 'donem3b',  id: 'donem3-butunleme', name: 'Dönem 3 Bütünleme Sınavı' },
];

async function check() {
  console.log('====================================================');
  console.log('   KARABÜK ÜNİVERSİTESİ TIP FAKÜLTESİ DÖNEM 3');
  console.log('   MASTER REDAKSİYON & SENKRONİZASYON RAPORU');
  console.log('====================================================\n');

  let totalLocal = 0;
  let totalSb = 0;

  for (const c of committees) {
    const localPath = path.join(`${process.env.MEDS_DATABASE_DIR || '/home/indu/medsor/meds_database'}/database_json`, c.key, 'pastquestions.json');
    let localCount = 0;
    if (fs.existsSync(localPath)) {
      const arr = JSON.parse(fs.readFileSync(localPath, 'utf8'));
      localCount = arr.length;
      totalLocal += localCount;
    }
    
    const { count, error } = await sb.from('past_questions').select('*', { count: 'exact', head: true }).eq('committee_id', c.id);
    const sbCount = count || 0;
    totalSb += sbCount;

    console.log(`📌 ${c.name}:`);
    console.log(`   • Yerel JSON (database_json/${c.key}): ${localCount} soru`);
    console.log(`   • Supabase (committee_id: '${c.id}'): ${sbCount} soru\n`);
  }

  console.log('----------------------------------------------------');
  console.log(`🎯 TOPLAM YEREL DÖNEM 3 SORU: ${totalLocal}`);
  console.log(`☁️  TOPLAM SUPABASE DÖNEM 3 SORU: ${totalSb}`);
  console.log('----------------------------------------------------');

  // Check redakte_sorular directory files
  const redakteDir = `${process.env.MEDS_DATABASE_DIR || '/home/indu/medsor/meds_database'}/redakte_sorular`;
  if (fs.existsSync(redakteDir)) {
    const files = fs.readdirSync(redakteDir);
    console.log(`\n📁 redakte_sorular klasöründeki toplam JSON/Rapor dosyası: ${files.length}`);
  }
}

check().catch(console.error);
