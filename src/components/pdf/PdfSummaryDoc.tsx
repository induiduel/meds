/**
 * Ders özetlerinin PDF'i: başlık Öğren adım başlığıyla (ls-head), metin Öğren anlatımıyla (ls-prose: not
 * kutuları, tablolar, maddeler) aynı dilde çizilir. Özet içindeki örnek soruların cevap blokları
 * (<details>) seçime göre cevap notuna çevrilir ya da çıkarılır.
 */
import React from 'react';
import { mdToHtml } from '../learn/lesson/lessonModel';
import { Cover, Masthead, type CoverInfo } from './PdfParts';

export type SummaryQuestions = 'answered' | 'plain' | 'none';

export interface SummaryDocOptions {
  keyPoints: boolean;
  tables: boolean;
  callouts: boolean;
  questions: SummaryQuestions;
  toc: boolean;
  cover: boolean;
}

export interface SummaryForPdf {
  id: string;
  title: string;
  discipline: string;
  kurul: number;
  instructor?: string;
  keyPoints: string[];
  content: string;
}

const QUESTION_HEAD = /^#{1,3}\s.*(soru|vaka|pekiştirme|test)/i;

/** Özet markdown'ını seçeneklere göre süzer. */
export function prepareSummary(md: string, o: SummaryDocOptions): string {
  const lines = String(md || '').split('\n');
  const out: string[] = [];
  let skipSection = false;
  let inDetails = false;
  let detailBuf: string[] = [];
  for (const raw of lines) {
    const line = raw.replace(/<\/?summary[^>]*>/gi, '');
    if (/^#{1,2}\s/.test(line)) skipSection = o.questions === 'none' && QUESTION_HEAD.test(line);
    if (skipSection) continue;
    if (/<details>/i.test(line)) {
      inDetails = true;
      detailBuf = [];
      continue;
    }
    if (inDetails) {
      if (/<\/details>/i.test(line)) {
        inDetails = false;
        const body = detailBuf.map((l) => l.trim()).filter(Boolean).join(' ');
        if (o.questions === 'answered' && body) out.push('', `> [!TIP] ${body}`, '');
        continue;
      }
      detailBuf.push(line);
      continue;
    }
    if (!o.tables && /^\s*\|.*\|\s*$/.test(line)) continue;
    if (!o.callouts && line.trim().startsWith('>')) continue;
    out.push(line);
  }
  // İlk satır başlığın tekrarıysa (emoji + başlık) ve meta satırları (**Ders Kodu:** …) üst bilgi olarak ayrı gösterilir
  return out.join('\n');
}

/** Özetin başındaki "**Öğretim Üyesi:** …" gibi meta satırlarını ayırır. */
const splitMeta = (md: string): { meta: [string, string][]; body: string } => {
  const lines = md.split('\n');
  const meta: [string, string][] = [];
  let i = 0;
  // İlk satır genelde emoji'li başlık
  if (lines[0] && !/^#|^\s*[-*|>]/.test(lines[0]) && lines[0].length < 140) i = 1;
  for (; i < lines.length; i++) {
    const m = lines[i].match(/^\s*\*\*([^*]{2,40}):\*\*\s*(.+)$/);
    if (m) meta.push([m[1].trim(), m[2].trim()]);
    else if (lines[i].trim()) break;
  }
  return { meta, body: lines.slice(i).join('\n') };
};

export const SummaryDoc: React.FC<{ summaries: SummaryForPdf[]; options: SummaryDocOptions; cover: CoverInfo }> = ({ summaries, options: o, cover }) => (
  <>
    {o.cover ? <Cover info={cover} /> : summaries.length > 1 ? <Masthead info={cover} /> : null}
    {o.toc && summaries.length > 1 && (
      <section className="pd-box" style={{ marginBottom: 22 }}>
        <div className="ls-sec-h">İçindekiler <span>{summaries.length}</span></div>
        <ol className="pd-toc">
          {summaries.map((s, i) => (
            <li key={s.id}>
              <small>{i + 1}</small>
              <span>{s.title}</span>
            </li>
          ))}
        </ol>
      </section>
    )}
    {summaries.map((s) => {
      const { meta, body } = splitMeta(prepareSummary(s.content, o));
      return (
        <article key={s.id} className="pd-sum">
          <header className="ls-head">
            <div className="ls-eyebrow-row">
              <span>Kurul {s.kurul}</span>
              <span className="dot" aria-hidden />
              <span>{s.discipline}</span>
              {s.instructor && (
                <>
                  <span className="dot" aria-hidden />
                  <span>{s.instructor}</span>
                </>
              )}
            </div>
            <h1 className="ls-title"><span>{s.title}</span></h1>
          </header>
          {meta.length > 0 && (
            <ul className="ls-info pd-box" style={{ padding: '2px 14px' }}>
              {meta.map(([k, v]) => (
                <li key={k}>
                  <span><b>{k}</b><br />{v.replace(/\*\*/g, '')}</span>
                </li>
              ))}
            </ul>
          )}
          {o.keyPoints && s.keyPoints.length > 0 && (
            <ul className="ls-keys">
              {s.keyPoints.slice(0, 8).map((k, i) => (
                <li key={i} className={i === 0 ? 'is-key' : ''}>
                  <p>{k}</p>
                </li>
              ))}
            </ul>
          )}
          <div className="ls-prose" dangerouslySetInnerHTML={{ __html: mdToHtml(body) }} />
        </article>
      );
    })}
  </>
);
