import dotenv from 'dotenv';
dotenv.config();
import { createClient } from '@supabase/supabase-js';
import {
  calculateDraftAnchorScore,
  calculateDraftCompatibility,
  clusterDraftsForCommittee,
  extractMedicalEntities,
  detectQuestionTarget
} from '../src/services/draftClusteringService';

async function run() {
  const url = process.env.SUPABASE_URL!;
  const key = (process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY)!;
  const client = createClient(url, key);

  const { data: questions, error } = await client
    .from('questions')
    .select('*')
    .eq('committee_id', 'donem3-kurul1');

  if (error || !questions) {
    console.error('Error fetching questions:', error);
    process.exit(1);
  }

  const normalized = questions.map((q) => ({
    id: q.id,
    committeeId: q.committee_id,
    questionNumber: q.question_number,
    discipline: q.discipline,
    topic: q.topic,
    status: q.status,
    claimedAnswer: q.claimed_answer,
    upvotes: q.upvotes,
    tags: q.tags || [],
    fragments: q.fragments || [],
    options: q.options || [],
    reconstruction: q.reconstruction,
    isUnassignedNumber:
      q.is_unassigned_number ||
      q.data?.isUnassignedNumber ||
      q.question_number === 0 ||
      !q.question_number,
    createdAt: q.created_at || new Date().toISOString(),
    updatedAt: q.updated_at || new Date().toISOString(),
  }));

  console.log(`\n=== DONEM 3 KURUL 1 TOPLAM SORU SAYISI: ${normalized.length} ===`);

  const downQuestions = normalized.filter((x) =>
    ['q-donem3-kurul1-unassigned-1790967391177', 'q-donem3-kurul1-unassigned-1790967419207', 'q-donem3-kurul1-unassigned-1790967524679'].includes(x.id)
  );

  console.log(`\nBulunan Down Sendromu Soruları: ${downQuestions.length}`);

  for (const q of downQuestions) {
    console.log(`\n--------------------------------------------------`);
    console.log(`ID: ${q.id}`);
    console.log(`Discipline: ${q.discipline} | Topic: ${q.topic}`);
    console.log(`Fragments count: ${q.fragments.length}`);
    q.fragments.forEach((f: any, idx: number) => console.log(`  Fragment ${idx + 1} (${f.type}): "${f.text}"`));
    console.log(`Options count: ${q.options.length}`);
    q.options.forEach((o: any) => console.log(`  Option ${o.key}: "${o.text}"`));
    
    const anchorScore = calculateDraftAnchorScore(q);
    console.log(`Anchor Score:`, anchorScore);
    const stemText = q.fragments.map((f: any) => f.text).join(' ');
    console.log(`Extracted Entities:`, extractMedicalEntities(stemText));
    console.log(`Detected Target:`, detectQuestionTarget(stemText));
  }

  if (downQuestions.length >= 2) {
    const q1 = downQuestions.find((x) => x.id === 'q-donem3-kurul1-unassigned-1790967391177')!;
    const q2 = downQuestions.find((x) => x.id === 'q-donem3-kurul1-unassigned-1790967419207')!;
    const q3 = downQuestions.find((x) => x.id === 'q-donem3-kurul1-unassigned-1790967524679')!;

    console.log(`\n=== İKİLİ UYUMLULUK ANALİZLERİ ===`);
    if (q1 && q2) {
      console.log(`\n>>> Q1 vs Q2 Uyumluluk:`);
      const comp12 = calculateDraftCompatibility(q1, q2);
      console.log(JSON.stringify(comp12, null, 2));
    }

    if (q2 && q3) {
      console.log(`\n>>> Q2 vs Q3 Uyumluluk:`);
      const comp23 = calculateDraftCompatibility(q2, q3);
      console.log(JSON.stringify(comp23, null, 2));
    }

    if (q1 && q3) {
      console.log(`\n>>> Q1 vs Q3 Uyumluluk:`);
      const comp13 = calculateDraftCompatibility(q1, q3);
      console.log(JSON.stringify(comp13, null, 2));
    }
  }

  console.log(`\n=== KOMİTE GENEL KÜMELEME RAPORU ===`);
  const clusterSummary = clusterDraftsForCommittee(normalized, 'donem3-kurul1');
  console.log(`Toplam Taslak: ${clusterSummary.totalDrafts}`);
  console.log(`Tahmini Gerçek Soru: ${clusterSummary.estimatedTrueQuestions}`);
  console.log(`Küme Sayısı: ${clusterSummary.clusters.length}`);
  console.log(`Muğlak Sayısı: ${clusterSummary.vagueDraftsCount}`);

  clusterSummary.clusters.forEach((c, idx) => {
    console.log(`\n[Küme ${idx + 1}] Çapa: ${c.anchorQuestion.id} (${c.anchorQuestion.discipline} - ${c.anchorQuestion.topic})`);
    console.log(`  Durum: ${c.status} | Güven: %${c.overallConfidence}`);
    console.log(`  Uydular (${c.satelliteDrafts.length}):`);
    c.satelliteDrafts.forEach((s) => {
      console.log(`    -> ${s.question.id} | Skor: %${s.compatibility.score} (${s.compatibility.recommendation}) | Nedenler: ${s.compatibility.reasons.join(', ')}`);
    });
  });

  console.log(`\nEşleşmemiş Muğlak Taslaklar (${clusterSummary.unmatchedVagueDrafts.length}):`);
  clusterSummary.unmatchedVagueDrafts.forEach((v) => {
    console.log(`  -> ${v.id} (${v.discipline} - ${v.topic}): "${(v.fragments[0]?.text || '').substring(0, 60)}..."`);
  });

  process.exit(0);
}

run().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});
