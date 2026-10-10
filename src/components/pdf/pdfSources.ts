/**
 * PDF Stüdyosu veri katmanı: çıkmış sorular, soru havuzu, kazanım temelli örnek sorular ve Öğren destelerinin
 * mini soruları tek bir soru modeline (PdfQuestion) çevrilir. Çıkmış sorularda ekrandaki varsayılan sürüm
 * (denetleyici sürümü varsa o) kullanılır; şık analizi, açıklama ve referanslar da taşınır.
 */
import type { QuestionItem } from '../../types';
import { cleanWhy, splitExplanation } from '../learn/lesson/LessonBlocks';
import { normalizeRefList } from '../QuestionAboutDialog';

export type QuestionSource = 'past' | 'pool' | 'ornek' | 'mini';

export interface PdfOption {
  key: string;
  text: string;
  /** Şık açıklaması / şık analizi gerekçesi */
  why?: string;
  /** Şık analizindeki hüküm: Doğru ifade, Yanlış ifade, Tartışmalı */
  verdict?: { label: string; tone: 'ok' | 'bad' | 'warn' };
}

export interface PdfQuestion {
  id: string;
  source: QuestionSource;
  /** Kaynaktaki soru numarası */
  number?: number;
  committeeId?: string;
  discipline: string;
  topic?: string;
  year?: string;
  /** Gruplama etiketi: kazanım, slayt ya da deste */
  group?: string;
  difficulty?: 'kolay' | 'orta' | 'zor';
  stem: string;
  options: PdfOption[];
  answer?: string;
  explanation?: string;
  refs: string[];
  badges: { label: string; tone: 'ok' | 'warn' | 'bad' | 'accent' | 'ai' }[];
}

export const COMMITTEE_NAME: Record<string, string> = {
  'donem3-kurul1': 'Kurul 1 · Ürogenital ve Obstetrik',
  'donem3-kurul2': 'Kurul 2 · Nöropsikiyatri',
  'donem3-kurul3': 'Kurul 3 · Gastrointestinal Sistem',
  'donem3-kurul4': 'Kurul 4 · Dolaşım, Solunum ve Tümör',
  'donem3-kurul5': 'Kurul 5 · Ortopedi, Travma ve Hematopoetik',
  'donem3-kurul6': 'Kurul 6 · Endokrin, Metabolizma ve Yaşlanma',
  'donem3-final': 'Final',
  'donem3-butunleme': 'Bütünleme',
};
export const committeeShort = (id?: string) => (id ? (COMMITTEE_NAME[id] || id).split(' · ')[0] : '');

const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];
const s = (v: any) => String(v ?? '').trim();

/** "DOĞRU: …", "YANLIŞ / TARTIŞMALI – …" önekini hükme çevirir (Hakkında penceresindeki kuralın aynısı). */
export const parseVerdict = (raw: string): { verdict?: PdfOption['verdict']; reason: string } => {
  const m = raw.match(/^\s*(DOĞRU|YANLIŞ|TARTIŞMALI)(?:\s*\/\s*(TARTIŞMALI|YANLIŞ|DOĞRU))?\s*[:\-–]\s*/i);
  if (!m) return { reason: raw.trim() };
  const v = m[1].toLocaleUpperCase('tr-TR');
  const disputed = /TARTIŞMALI/i.test(m[0]);
  const verdict: PdfOption['verdict'] = disputed
    ? { label: v === 'TARTIŞMALI' ? 'Tartışmalı' : `${v === 'DOĞRU' ? 'Doğru' : 'Yanlış'} · tartışmalı`, tone: 'warn' }
    : v === 'DOĞRU'
      ? { label: 'Doğru ifade', tone: 'ok' }
      : { label: 'Yanlış ifade', tone: 'bad' };
  return { verdict, reason: raw.slice(m[0].length).trim() };
};

const optList = (raw: any[]): PdfOption[] =>
  (raw || [])
    .map((o: any, i: number): PdfOption =>
      typeof o === 'string'
        ? { key: LETTERS[i], text: o.replace(/^\s*[A-Ea-e][).:-]\s*/, '') }
        : { key: s(o.key || LETTERS[i]).toUpperCase().slice(0, 1), text: s(o.text), why: s(o.explanation) || undefined }
    )
    .filter((o, i, arr) => o.key && o.text && arr.findIndex((x) => x.key === o.key) === i)
    .sort((a, b) => a.key.localeCompare(b.key));

/** Açıklama içinde şık satırları ("A seçeneği yanlıştır: …") varsa şıklara dağıtılır. */
const attachWhy = (options: PdfOption[], explanation?: string): { options: PdfOption[]; explanation?: string } => {
  if (!explanation || options.some((o) => o.why)) return { options, explanation };
  const { perOption, rest } = splitExplanation(explanation, options.map((o) => o.key));
  if (Object.keys(perOption).length < 2) return { options, explanation };
  return { options: options.map((o) => ({ ...o, why: perOption[o.key] || o.why })), explanation: rest || undefined };
};

/* ---------------------------------------------------------------------------
 * Çıkmış sorular (ApiService.getPastQuestions çıktısı)
 * ------------------------------------------------------------------------- */
export function fromPastQuestion(q: any): PdfQuestion | null {
  const den = q.denetleyiciSurumu || {};
  const rec = q.reconstruction || {};
  const stem = s(rec.stem || q.stem || q.rawQuestion?.stem || q.fragments?.[0]?.text);
  if (!stem) return null;
  const answer = s(rec.correctAnswer || q.correctAnswer || q.claimedAnswer).toUpperCase().slice(0, 1);
  let options = optList(rec.options?.length ? rec.options : q.options || q.rawQuestion?.options || []);
  const sa = q.sik_analizi || den.sik_analizi;
  if (sa && typeof sa === 'object') {
    options = options.map((o) => {
      const raw = sa[o.key] ?? sa[o.key.toLowerCase()];
      if (!raw) return o;
      const { verdict, reason } = parseVerdict(String(raw));
      return { ...o, why: reason, verdict };
    });
  }
  const expl = s(rec.explanation || q.explanation) || undefined;
  const spread = attachWhy(options, expl);
  const badges: PdfQuestion['badges'] = [];
  const tags: string[] = Array.isArray(q.tags) ? q.tags : [];
  if (q.denetleyiciOnayi || q.denetleyici_onayi || q.surum === 'denetleyici' || tags.includes('denetleyici_onayi')) badges.push({ label: 'Denetleyici onaylı', tone: 'ok' });
  if (q.phase14 || tags.includes('faz14_duzeltildi')) badges.push({ label: q.phase14?.status === 'onay_bekliyor' ? 'Faz 14 · onay bekliyor' : 'Faz 14', tone: 'ai' });
  if (q.answerStatus === 'dogrulandi') badges.push({ label: 'Cevap slaytla doğrulandı', tone: 'ok' });
  if (q.answerStatus === 'dogrulanmadi' || q.answerDoubtful) badges.push({ label: 'Cevap tartışmalı', tone: 'warn' });
  if (q.isAmbiguous) badges.push({ label: 'Eksik', tone: 'warn' });
  return {
    id: s(q.id),
    source: 'past',
    number: Number(q.questionNumber) || undefined,
    committeeId: s(q.contentCommitteeId || q.committeeId) || undefined,
    discipline: s(q.discipline) || 'Tıp',
    topic: s(q.topic) || undefined,
    year: s(q.examYear) || undefined,
    stem,
    options: spread.options,
    answer: answer || undefined,
    explanation: spread.explanation,
    refs: normalizeRefList(q.referans_kaynaklar ?? den.referans_kaynaklar),
    badges,
  };
}

/* ---------------------------------------------------------------------------
 * Soru havuzu (öğrencilerin topladığı sorular)
 * ------------------------------------------------------------------------- */
export function fromPoolQuestion(q: QuestionItem): PdfQuestion | null {
  const rec: any = q.reconstruction || {};
  const stem = s(rec.stem || q.fragments?.map((f: any) => f.text).join(' ') || (q as any).stem);
  if (!stem) return null;
  const answer = s(rec.correctAnswer || q.claimedAnswer).toUpperCase().slice(0, 1);
  const spread = attachWhy(optList(rec.options?.length ? rec.options : q.options || []), s(rec.explanation) || undefined);
  return {
    id: s(q.id),
    source: 'pool',
    number: q.questionNumber || undefined,
    committeeId: q.committeeId,
    discipline: s(q.discipline) || 'Tıp',
    topic: s(q.topic) || undefined,
    year: s(q.examYear) || undefined,
    stem,
    options: spread.options,
    answer: answer || undefined,
    explanation: spread.explanation,
    refs: [],
    badges: q.status === 'completed' ? [{ label: 'Tamamlandı', tone: 'ok' }] : [{ label: 'Toplanıyor', tone: 'warn' }],
  };
}

/* ---------------------------------------------------------------------------
 * Örnek sorular (src/data/ornek_sorular/k1/<ders>.json)
 * ------------------------------------------------------------------------- */
export interface OrnekIndexRow { id: string; sira: number; ders: string; konu: string; ogretim_uyesi: string; soru_sayisi: number; kazanim: number }
const ornekIndex = import.meta.glob('../../data/ornek_sorular/k1/index.json', { eager: true, import: 'default' }) as Record<string, OrnekIndexRow[]>;
const ornekLoaders = import.meta.glob('../../data/ornek_sorular/k1/k1-*.json', { import: 'default' }) as Record<string, () => Promise<any>>;
export const ORNEK_INDEX: OrnekIndexRow[] = Object.values(ornekIndex)[0] || [];

export async function loadOrnekQuestions(dersId: string): Promise<PdfQuestion[]> {
  const loader = ornekLoaders[`../../data/ornek_sorular/k1/${dersId}.json`];
  if (!loader) return [];
  const ders = await loader();
  const out: PdfQuestion[] = [];
  for (const k of ders?.kazanimlar || []) {
    for (const q of k.sorular || []) {
      const answer = s(q.dogru).toUpperCase();
      const options = Object.entries(q.secenekler || {})
        .map(([key, text]) => ({ key: key.toUpperCase(), text: s(text), why: s(q.sik_aciklamalari?.[key]) || undefined }))
        .sort((a, b) => a.key.localeCompare(b.key));
      out.push({
        id: s(q.id),
        source: 'ornek',
        committeeId: 'donem3-kurul1',
        discipline: s(ders.ders) || 'Tıp',
        topic: s(ders.konu),
        group: `Kazanım ${k.no} · ${s(k.metin)}`,
        difficulty: q.zorluk,
        stem: s(q.soru),
        options,
        answer: answer || undefined,
        explanation: s(q.aciklama) || undefined,
        refs: [],
        badges: [],
      });
    }
  }
  return out;
}

/* ---------------------------------------------------------------------------
 * Mini sorular: Öğren destelerindeki micro_quiz (ve istenirse klinik karar) ögeleri
 * ------------------------------------------------------------------------- */
const CP_RE = /^\[TEKRAR SAYFASI\s*-\s*CHECKPOINT\s*(\d+)\]\s*/i;
export function miniQuestionsFromDeck(deck: any, includeBranching: boolean): PdfQuestion[] {
  const out: PdfQuestion[] = [];
  const slides: any[] = Array.isArray(deck?.slides) ? deck.slides : [];
  slides.forEach((sl, idx) => {
    const els: any[] = (Array.isArray(sl.interactiveElements) && sl.interactiveElements.length
      ? sl.interactiveElements
      : Array.isArray(sl.elements) && sl.elements.length
        ? sl.elements
        : sl.interactiveElement
          ? [sl.interactiveElement]
          : sl.microQuiz
            ? [{ type: 'micro_quiz', ...sl.microQuiz }]
            : []
    ).filter((e: any) => e && (e.type === 'micro_quiz' || (includeBranching && e.type === 'branching_logic')));
    const slideNo = sl.slideNumber ?? idx + 1;
    const title = s(sl.title).replace(CP_RE, '');
    els.forEach((e, j) => {
      const raw = e.type === 'branching_logic' ? e.options || [] : e.microQuizOptions || e.options || [];
      const options: PdfOption[] = raw
        .map((o: any, k: number) => ({
          key: e.type === 'branching_logic' ? LETTERS[k] : s(o.key || LETTERS[k]).toUpperCase(),
          text: s(o.text),
          why: cleanWhy(e.type === 'branching_logic' ? o.feedback : o.explanation) || undefined,
          ok: !!o.isCorrect,
        }))
        .filter((o: any) => o.text);
      const right = options.find((o: any) => o.ok);
      const stem = s(e.type === 'branching_logic' ? e.scenario || e.question : e.question || e.sentence);
      if (!stem || options.length < 2) return;
      out.push({
        id: `${deck.id}:${slideNo}:${j}`,
        source: 'mini',
        number: undefined,
        committeeId: undefined,
        discipline: s(deck.discipline) || 'Tıp',
        topic: s(deck.shortTitle || deck.title),
        group: `Adım ${slideNo} · ${title}`,
        stem,
        options: options.map(({ ok: _ok, ...o }: any) => o),
        answer: right?.key,
        explanation: undefined,
        refs: [],
        badges: e.type === 'branching_logic' ? [{ label: 'Klinik karar', tone: 'accent' }] : [],
      });
    });
  });
  return out;
}

/** Yıl etiketlerini yeniden eskiye sıralar ("2024-2025 Final" < "2025-2026 Kurul"). */
export const sortYears = (ys: string[]) => {
  const k = (y: string) => (/\d{4}/.test(y) ? y : '');
  return [...new Set(ys.filter(Boolean))].sort((a, b) => k(b).localeCompare(k(a), 'tr', { numeric: true }) || a.localeCompare(b, 'tr'));
};
