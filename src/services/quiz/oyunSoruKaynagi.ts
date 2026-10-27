/**
 * Oyunlar (canlı yarışma) soru kaynağı. Sunucu tarafı.
 * Sorular yalnız yayındaki sesli soru çözücü setlerinden gelir (src/data/<branş>_cozucu/<kod>.json; yazar + denetçi
 * hattından geçmiş, her şıkkı açıklamalı). Yeni soru üretilmez, LLM çağrılmaz. Uzun kökler (>220 karakter) oyuna
 * alınmaz: yarışma kısa okunur sorularla oynanır. Süre kök + şık uzunluğundan 10–25 sn.
 */
import fs from 'fs';
import path from 'path';
import type { QuizQuestion } from '../../types/quiz';

interface CSoru { no: number; soru: string; secenekler: Record<string, string>; dogru: string; siklar?: Record<string, string>; ipucu?: string; zorluk?: string; gorsel?: string }
interface CDers { kod: string; no?: number; baslik: string; sorular: CSoru[] }
export interface OyunKaynak { brans: string; ad: string; kurul: number; ders: { kod: string; baslik: string; n: number }[]; n: number; gorselN: number }
/** görselli soru: sorunun `gorsel` alanı yayındaki bir görsel adresi (/… ya da https://…) */
const gorselli = (s: CSoru) => typeof s.gorsel === 'string' && /^(\/|https:\/\/)/.test(s.gorsel);

const KOK = path.join(process.cwd(), 'src', 'data');
const KOK_SINIR = 220;
let onbellek: { at: number; v: Map<string, CDers[]> } | null = null;

/** branş adı: brans kayıt defterinden (src/data/dersler/branslar.json), yoksa klasör adı */
function bransAdlari(): Map<string, string> {
  const m = new Map<string, string>();
  try {
    const b = JSON.parse(fs.readFileSync(path.join(KOK, 'dersler', 'branslar.json'), 'utf8'));
    for (const x of b.branslar || []) m.set(x.slug, x.kisa || x.ad);
  } catch { /* yok */ }
  return m;
}

function yukle(): Map<string, CDers[]> {
  if (onbellek && Date.now() - onbellek.at < 10 * 60_000) return onbellek.v;
  const v = new Map<string, CDers[]>();
  for (const klasor of fs.readdirSync(KOK)) {
    const m = /^(.+)_cozucu$/.exec(klasor);
    if (!m) continue;
    const dersler: CDers[] = [];
    for (const f of fs.readdirSync(path.join(KOK, klasor))) {
      if (!f.endsWith('.json') || f === 'index.json') continue;
      try {
        const d = JSON.parse(fs.readFileSync(path.join(KOK, klasor, f), 'utf8')) as CDers;
        const sorular = (d.sorular || []).filter((s) => s?.soru && s.soru.length <= KOK_SINIR && s.secenekler?.[s.dogru]);
        if (sorular.length) dersler.push({ kod: d.kod || f.replace(/\.json$/, ''), no: d.no, baslik: d.baslik, sorular });
      } catch { /* bozuk dosya atlanır */ }
    }
    if (dersler.length) v.set(m[1], dersler.sort((a, b) => String(a.kod).localeCompare(String(b.kod), 'tr', { numeric: true })));
  }
  onbellek = { at: Date.now(), v };
  return v;
}

export function oyunKaynaklari(): OyunKaynak[] {
  const adlar = bransAdlari();
  return [...yukle()].map(([brans, dersler]) => {
    const k = /^k(\d+)(.+)$/.exec(brans);
    const slug = k ? k[2] : brans;
    return {
      brans,
      ad: adlar.get(slug) || slug,
      kurul: k ? Number(k[1]) : 1,
      ders: dersler.map((d) => ({ kod: String(d.kod), baslik: d.baslik, n: d.sorular.length })),
      n: dersler.reduce((a, d) => a + d.sorular.length, 0),
      gorselN: dersler.reduce((a, d) => a + d.sorular.filter(gorselli).length, 0),
    };
  }).sort((a, b) => b.kurul - a.kurul || b.n - a.n);
}

const karistir = <T,>(a: T[]): T[] => {
  const r = [...a];
  for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; }
  return r;
};

/** brans (zorunlu), ders kodu (isteğe bağlı), n soru (3–20) → QuizQuestion listesi; kaynak yoksa boş */
export function oyunSorulari(brans: string, ders: string | undefined, n: number, yalnizGorselli = false): QuizQuestion[] {
  const dersler = (yukle().get(brans) || []).filter((d) => !ders || String(d.kod) === ders);
  const havuz = dersler.flatMap((d) => d.sorular.filter((s) => !yalnizGorselli || gorselli(s)).map((s) => ({ d, s })));
  const adet = Math.max(3, Math.min(20, Math.round(n) || 10));
  return karistir(havuz).slice(0, adet).map(({ d, s }) => {
    const uzunluk = s.soru.length + Object.values(s.secenekler).join(' ').length;
    const sure = Math.max(10, Math.min(25, Math.round(6 + uzunluk / 22)));
    const id = `oy_${brans}_${d.kod}_${s.no}`;
    return {
      id,
      question_pair_id: id,
      knowledge_atom_id: '',
      course_id: brans,
      board_id: '',
      schedule_ref: '',
      topic_id: String(d.kod),
      audio_lesson_id: '',
      learning_objective_id: '',
      direction: 'positive_direct',
      archetype: d.baslik,
      prompt: s.soru,
      options: s.secenekler,
      correct_option: s.dogru,
      option_explanations: s.siklar || {},
      recall_hint: s.ipucu,
      estimated_reading_sec: sure,
      difficulty: s.zorluk === 'zor' ? 'hard' : s.zorluk === 'kolay' ? 'easy' : 'medium',
      evidence: { page: 0, quote: '' },
      ...(gorselli(s) ? { gorsel: s.gorsel } : {}),
    } as QuizQuestion;
  });
}
