/**
 * Faz 14 okuma katmanı (server-only): Faz 14'te incelenmiş ama henüz onaylanmamış sorular sitede Faz 14 hâliyle gösterilir.
 * Veri dosyası (pastQuestions.json) değişmez; onay (test/cikmis → Onayla) kalıcı yazar. Eski hâl phase14Original'da,
 * durum phase14.status = 'onay_bekliyor' (onaylananlar 'onayli'). Reddedilen/"değişiklik yok" kayıtlar uygulanmaz.
 * Kaynak: $MEDS_DATABASE_DIR/../meds_database_v2/phase14_past_question_editor/reviews.jsonl (mtime ile yeniden okunur).
 */
import fs from 'fs';
import path from 'path';

const reviewsFile = () =>
  path.join(path.dirname(process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database')), 'meds_database_v2', 'phase14_past_question_editor', 'reviews.jsonl');

let cache: Map<string, any> | null = null;
let cacheMtime = 0;

export function latestReviews(): Map<string, any> {
  try {
    const st = fs.statSync(reviewsFile());
    if (cache && st.mtimeMs === cacheMtime) return cache;
    const m = new Map<string, any>();
    const stamp = (r: any) => Date.parse(r.last_edited_at || r.approved_at || r.processed_at || '') || 0;
    for (const line of fs.readFileSync(reviewsFile(), 'utf-8').split('\n')) {
      if (!line.trim()) continue;
      try {
        const r = JSON.parse(line);
        const id = String(r.question_id || '');
        if (!id) continue;
        const prev = m.get(id);
        if (!prev || stamp(r) >= stamp(prev)) m.set(id, r);
      } catch {
        // yarım satır
      }
    }
    cache = m;
    cacheMtime = st.mtimeMs;
  } catch {
    cache = cache || new Map();
  }
  return cache;
}

export function normalizeKurul(v: unknown): string | null {
  const s = String(v || '').trim();
  const m = s.match(/kurul\s*-?\s*(\d)/i) || s.match(/^TIP\s*3(\d)0$/i);
  if (m) return `donem3-kurul${m[1]}`;
  if (/final/i.test(s)) return 'donem3-final';
  if (/b[uü]t[uü]nleme/i.test(s)) return 'donem3-butunleme';
  return s || null;
}

export function applyPhase14Overlay<T extends Record<string, any>>(list: T[]): T[] {
  const revs = latestReviews();
  if (!revs.size) return list;
  // İnceleme kaydı olan her soru, kayıt dosyası değişince "güncellendi" sayılır: cihaz önbelleği (artıksal senkron)
  // onay/red/anket sonucunu da alır; yoksa eski "onay bekliyor" ya da "cevap belirsiz" hâli cihazda kalıyordu.
  const touched = (q: T): T => {
    const at = new Date(Math.max(Date.parse(q.updatedAt || '') || 0, cacheMtime)).toISOString();
    return at === q.updatedAt ? q : { ...q, updatedAt: at };
  };
  return list.map((q) => {
    const r = revs.get(String(q.id));
    if (q.phase14 && q.phase14.status !== 'onay_bekliyor') {
      // Onaylı: veri zaten Faz 14 hâlinde. Onaydan SONRA yeniden düzenlenip onaylanmamış kayıt varsa o gösterilir.
      const approvedAt = Date.parse(q.phase14.approvedAt || '') || 0;
      const editedAt = r ? Date.parse(r.last_edited_at || '') || 0 : 0;
      if (!r || r.status !== 'review_required' || !r.proposal || editedAt <= approvedAt) return r ? touched(q) : q;
    }
    if (!r) return q;
    if (r.status !== 'review_required' || !r.proposal) return touched(q);
    const p = r.proposal;
    const src = r.source || {};
    const ans = String(p.dogru_secenek || '').toUpperCase() || undefined;
    const opts =
      p.secenekler && typeof p.secenekler === 'object' && Object.keys(p.secenekler).length >= 4
        ? Object.entries(p.secenekler).map(([k, v]) => {
            const K = k.toUpperCase();
            const ai = !(src.secenekler || {})[k] && !(src.secenekler || {})[K];
            return { key: K, text: String(v), isCorrect: K === ans, ...(ai || (p.yapay_zeka_tamamlanan_siklar || []).map((x: string) => String(x).toUpperCase()).includes(K) ? { isAiGenerated: true } : {}) };
          })
        : q.options;
    const stem = p.soru_koku || q.stem;
    const expl = p.aciklama && String(p.aciklama).trim() ? p.aciklama : q.explanation;
    const rec = q.reconstruction && typeof q.reconstruction === 'object'
      ? { ...q.reconstruction, stem, options: opts, correctAnswer: ans || q.reconstruction.correctAnswer, explanation: expl }
      : q.reconstruction;
    return {
      ...q,
      stem,
      options: opts,
      correctAnswer: ans || q.correctAnswer,
      claimedAnswer: ans || q.claimedAnswer,
      explanation: expl,
      reconstruction: rec,
      committeeId: normalizeKurul(p.kurul_adi) || q.committeeId,
      discipline: p.ders_adi || q.discipline,
      topic: p.konu_adi || q.topic,
      sik_analizi: p.sik_analizi || q.sik_analizi,
      cevap_gerekcesi: p.cevap_gerekcesi || q.cevap_gerekcesi,
      referans_kaynaklar: p.YZV?.referans_literatur ? [p.YZV.referans_literatur] : q.referans_kaynaklar,
      phase14Original: q.phase14Original || {
        stem: src.soru_koku, options: Object.entries(src.secenekler || {}).map(([k, v]) => ({ key: k.toUpperCase(), text: v })),
        explanation: src.aciklama, correctAnswer: src.dogru_secenek, committeeId: src.kurul_adi, discipline: src.ders_adi, topic: src.konu_adi,
      },
      answerDoubtful: Boolean(r.answer_doubtful),
      phase14: { status: 'onay_bekliyor', model: r.model, changes: p.degisen_alanlar || [], summary: p.YZV?.degisiklik_ozeti || p.degisiklik_ozeti,
                 cevapDegisti: p.cevap_degisti, cevapGerekcesi: p.cevap_gerekcesi, processedAt: r.processed_at },
      tags: Array.from(new Set([...(Array.isArray(q.tags) ? q.tags : []), 'faz14_inceleme'])),
      updatedAt: new Date(Math.max(Date.parse(q.updatedAt || '') || 0, Date.parse(r.last_edited_at || r.processed_at || '') || 0, cacheMtime)).toISOString(),
    };
  });
}
