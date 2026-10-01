#!/usr/bin/env node
/**
 * MedSoru Çıkmış Soru & Amfi Slayt İlişki Yönetim Motoru (Master Runner)
 * (scripts/manage-slide-relations.mjs)
 * 
 * Bu betik iki ana scripti entegre olarak yönetir:
 * 1. Script 1 (Denetim & Kesme): Çıkmış sorularla ilişkilendirilen ders slaytlarını denetler,
 *    içerik uyuşmazlığı olan veya geçersiz tüm ilişkileri keser.
 * 2. Script 2 (Eşleştirme & Vurgulama): İlişkisiz veya hatalı ilişkisi kesilmiş sorular için
 *    tüm amfi ders notlarını tarar, konu ve bilgi eşleştiğinde ilişki kurar ve ilişkili metni vurgular.
 * 
 * Kullanım Örnekleri:
 *   node scripts/manage-slide-relations.mjs --all        # İki scripti sırayla çalıştırır
 *   node scripts/manage-slide-relations.mjs --audit      # Sadece 1. scripti (denetim & kesme) çalıştırır
 *   node scripts/manage-slide-relations.mjs --match      # Sadece 2. scripti (eşleştirme & bağlama) çalıştırır
 *   node scripts/manage-slide-relations.mjs --stats      # Mevcut eşleşme istatistiklerini görüntüler
 */

import fs from 'fs';
import path from 'path';
import { runSlideAudit } from './audit-and-disconnect-faulty-slides.mjs';
import { runSlideMatching } from './match-and-link-lecture-slides.mjs';
import { DATA_PAST_PATH } from './slide-matching-utils.mjs';

function printHelp() {
  console.log(`
========================================================================
🩺 MedSoru Çıkmış Soru & Amfi Slaytı İlişki Yönetim CLI
========================================================================

Kullanım:
  node scripts/manage-slide-relations.mjs [seçenekler]

Seçenekler:
  --all            : 1. Script'i (Hatalı ilişkileri kesme) ve ardından
                     2. Script'i (Yeni ders eşleştirmesi ve vurgulama) sırayla çalıştırır.
  --audit          : Sadece 1. Script'i (Slayt Denetimi ve Hatalı İlişkileri Kesme) çalıştırır.
  --match          : Sadece 2. Script'i (İlişkisiz/Hatalı Soruları Eşleştirme ve Vurgulama) çalıştırır.
  --stats          : Mevcut veritabanındaki slayt eşleşme durumlarını ve istatistiklerini listeler.
  --min-score <n>  : Eşleştirme için asgari kabul puanı (varsayılan: 60).
  --limit <n>      : İşlenecek maksimum soru sayısı (test amaçlı).
  --dry-run        : Değişiklikleri dosyalara kaydetmeden simüle eder.
  --help, -h       : Bu yardım metnini görüntüler.

Örnekler:
  npm run slides:audit      # Sadece hatalı ilişkileri temizler
  npm run slides:match      # Temizlenmiş soruları amfi notlarıyla eşleştirir
  npm run slides:sync       # Tam senkronizasyon (Denetle -> Kes -> Yeniden Eşleştir)
========================================================================
  `);
}

function showStats() {
  if (!fs.existsSync(DATA_PAST_PATH)) {
    console.error('Hata: pastQuestions.json dosyası bulunamadı:', DATA_PAST_PATH);
    return;
  }
  const questions = JSON.parse(fs.readFileSync(DATA_PAST_PATH, 'utf8'));
  let total = questions.length;
  let withMatch = 0;
  let withSnippet = 0;
  let withHighlightedText = 0;
  let auditVerified = 0;
  let auditDisconnected = 0;
  let unassociated = 0;

  for (const q of questions) {
    const hasNote = Boolean(q.lectureReference?.noteTitle || q.matchedNoteTitle);
    if (hasNote) withMatch++;
    else unassociated++;

    if (q.lectureReference?.matchedSnippet) withSnippet++;
    if (q.lectureReference?.highlightedText) withHighlightedText++;
    if (q.slideAudit?.status === 'verified') auditVerified++;
    if (q.slideAudit?.status === 'disconnected') auditDisconnected++;
  }

  console.log('\n======================================================');
  console.log('📊 [MedSoru Veritabanı Slayt İlişki İstatistikleri]');
  console.log('======================================================');
  console.log(`Toplam Çıkmış Soru           : ${total}`);
  console.log(`Ders Slaytı ile İlişkili     : ${withMatch} (%${((withMatch / total) * 100).toFixed(1)})`);
  console.log(`İlişkili ve Metin Vurgulu    : ${withHighlightedText} (%${((withHighlightedText / total) * 100).toFixed(1)})`);
  console.log(`Snippet İçeren Soru          : ${withSnippet}`);
  console.log(`Doğrulanmış (Verified)       : ${auditVerified}`);
  console.log(`İlişkisi Kesilmiş            : ${auditDisconnected}`);
  console.log(`İlişkisiz (Slaytı Olmayan)   : ${unassociated} (%${((unassociated / total) * 100).toFixed(1)})`);
  console.log('======================================================\n');
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    printHelp();
    showStats();
    return;
  }

  const dryRun = args.includes('--dry-run');
  const limitIdx = args.indexOf('--limit');
  const limit = limitIdx !== -1 && args[limitIdx + 1] ? parseInt(args[limitIdx + 1], 10) : null;
  const scoreIdx = args.indexOf('--min-score');
  const minScore = scoreIdx !== -1 && args[scoreIdx + 1] ? parseInt(args[scoreIdx + 1], 10) : 60;

  if (args.includes('--stats')) {
    showStats();
    return;
  }

  if (args.includes('--audit')) {
    console.log('🚀 [Adım 1/1] Slayt Denetimi ve Hatalı İlişkileri Kesme Başlatılıyor...');
    await runSlideAudit({ verbose: true, dryRun });
    showStats();
    return;
  }

  if (args.includes('--match')) {
    console.log('🚀 [Adım 1/1] Slayt Eşleştirme, Bağlama ve Vurgulama Başlatılıyor...');
    await runSlideMatching({ verbose: true, dryRun, minScore, limit });
    showStats();
    return;
  }

  if (args.includes('--all')) {
    console.log('\n======================================================');
    console.log('🚀 [TAM SENKRONİZASYON BAŞLATILDI]');
    console.log('   Adım 1: Hatalı Slayt İlişkilerini Denetle ve Kes');
    console.log('   Adım 2: Ders Notlarını İncele, Eşleştir ve Vurgula');
    console.log('======================================================\n');

    console.log('--- [ADIM 1]: Hatalı İlişkileri Kesme ---');
    const auditRes = await runSlideAudit({ verbose: true, dryRun });

    console.log('\n--- [ADIM 2]: İlişkisiz ve Düzeltilecek Soruları Eşleştirme & Vurgulama ---');
    const matchRes = await runSlideMatching({ verbose: true, dryRun, minScore, limit });

    console.log('\n--- [ADIM 3]: Nihai Doğrulama Denetimi ---');
    await runSlideAudit({ verbose: false, dryRun });

    showStats();
    console.log('🎉 Tam senkronizasyon başarıyla tamamlandı!');
    return;
  }

  console.log('Geçersiz parametre. Yardım için: node scripts/manage-slide-relations.mjs --help');
}

main().catch(err => {
  console.error('Kritik Çalışma Hatası:', err);
  process.exit(1);
});
