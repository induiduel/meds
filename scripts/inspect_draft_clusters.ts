import dotenv from 'dotenv';
dotenv.config();
import { createClient } from '@supabase/supabase-js';
import { clusterDraftsForCommittee } from '../src/services/draftClusteringService';

const short = (s: string, n = 110) => (s || '').replace(/\s+/g, ' ').trim().slice(0, n);

async function run() {
  const url = process.env.SUPABASE_URL || 'https://kgutsltgmqbnlxcnzrtl.supabase.co';
  const key = process.env.SUPABASE_PUBLISHABLE_KEY || 'sb_publishable_EVdXdIi_2mxVr3HZKYabwQ_li5KuE1Q';
  const client = createClient(url, key);

  const { data, error } = await client.from('questions').select('*').limit(5000);
  if (error || !data) {
    console.error('FETCH_ERROR', error);
    process.exit(1);
  }

  const normalized = data.map((q: any) => ({
    id: q.id,
    committeeId: q.committee_id,
    questionNumber: q.question_number,
    discipline: q.discipline,
    topic: q.topic,
    status: q.status,
    claimedAnswer: q.claimed_answer,
    correctAnswer: q.data?.correctAnswer,
    upvotes: q.upvotes,
    tags: q.tags || [],
    fragments: q.fragments || [],
    options: q.options || [],
    reconstruction: q.reconstruction,
    stem: q.data?.stem || q.stem,
    rawStem: q.data?.rawStem,
    isUnassignedNumber: q.question_number === 0 || !q.question_number,
    contributedByName: q.data?.contributedByName,
    createdAt: q.created_at,
    updatedAt: q.updated_at,
  }));

  const byComm = new Map<string, any[]>();
  for (const q of normalized) {
    if (!byComm.has(q.committeeId)) byComm.set(q.committeeId, []);
    byComm.get(q.committeeId)!.push(q);
  }

  for (const [comm, list] of byComm) {
    const drafts = list.filter((q: any) => q.status !== 'completed');
    if (drafts.length < 3) continue;
    console.log(`\n===== ${comm} | toplam=${list.length} taslak=${drafts.length} =====`);
    const summary = clusterDraftsForCommittee(list as any, comm);
    console.log(`kume=${summary.clusters.length} muglak=${summary.vagueDraftsCount} tahminiGercek=${summary.estimatedTrueQuestions}`);
    summary.clusters.slice(0, 12).forEach((c, i) => {
      const aStem = short(c.anchorQuestion.reconstruction?.stem || (c.anchorQuestion.fragments?.[0] as any)?.text || '');
      console.log(`\n[Kume ${i + 1}] durum=${c.status} guven=%${c.overallConfidence} capa=S.${c.anchorQuestion.questionNumber} [${c.anchorQuestion.discipline}] ${short(c.anchorQuestion.topic || '', 60)}`);
      console.log(`  capa-kok: ${aStem}`);
      c.satelliteDrafts.slice(0, 6).forEach((s) => {
        const sStem = short(s.question.reconstruction?.stem || (s.question.fragments?.[0] as any)?.text || '');
        console.log(`  -> S.${s.question.questionNumber} [${s.question.discipline}] skor=%${s.compatibility.score} tav=${s.compatibility.recommendation} kokBen=%${s.compatibility.stemSimilarity} sikBen=%${s.compatibility.optionSetSimilarity} kavram=[${(s.compatibility.sharedConcepts || []).join('|')}]`);
        console.log(`     kok: ${sStem}`);
        console.log(`     neden: ${s.compatibility.reasons.slice(0, 3).join(' / ').slice(0, 220)}`);
      });
      if (c.satelliteDrafts.length > 6) console.log(`  ... +${c.satelliteDrafts.length - 6} uydu daha`);
    });
  }
  process.exit(0);
}

run().catch((err) => {
  console.error('FATAL', err);
  process.exit(1);
});
