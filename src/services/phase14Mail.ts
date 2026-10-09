/**
 * "Bildirdiğin soru güncellendi" e-postası (yalnız sunucu): sorunun eski ve yeni hali, değişen alanlar vurgulu.
 */
export interface QuestionSnapshot {
  stem: string;
  options: { key: string; text: string }[];
  answer: string;
  explanation: string;
}

const esc = (s: string) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]!));
const norm = (s: string) => String(s ?? '').replace(/\s+/g, ' ').trim();
const nl = (s: string) => esc(s).replace(/\n/g, '<br>');

const INK = '#0E1726';
const INK2 = '#46546A';
const INK3 = '#5F6C80';
const LINE = '#E3E7EE';
const OK = '#157A3E';
const OK_SOFT = '#E4F3E9';
const CHANGED = '#FCEFE0';

function block(title: string, q: QuestionSnapshot, other: QuestionSnapshot, isNew: boolean) {
  const stemChanged = norm(q.stem) !== norm(other.stem);
  const opt = (o: { key: string; text: string }) => {
    const prev = other.options.find((x) => x.key === o.key);
    const changed = !prev || norm(prev.text) !== norm(o.text);
    const isAns = o.key === q.answer;
    const bg = isAns ? OK_SOFT : changed && isNew ? CHANGED : '#ffffff';
    return `<tr><td style="padding:7px 10px;border-top:1px solid ${LINE};background:${bg};vertical-align:top;width:26px;font-family:Menlo,Consolas,monospace;font-size:13px;font-weight:700;color:${isAns ? OK : INK3}">${esc(o.key)}</td>
<td style="padding:7px 10px 7px 0;border-top:1px solid ${LINE};background:${bg};font-size:14px;line-height:1.5;color:${isAns ? OK : INK};${isAns ? 'font-weight:600;' : ''}">${nl(o.text)}${isAns ? ' &nbsp;✓' : ''}</td></tr>`;
  };
  return `<td style="vertical-align:top;padding:0 6px;width:50%">
<div style="border:1px solid ${LINE};border-radius:12px;overflow:hidden;background:#fff">
<div style="padding:9px 12px;background:${isNew ? OK_SOFT : '#F6F7FA'};font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:${isNew ? OK : INK3}">${title}</div>
<div style="padding:12px;font-size:14.5px;line-height:1.6;color:${INK};${stemChanged && isNew ? `background:${CHANGED};` : ''}">${nl(q.stem) || '<i>—</i>'}</div>
<table role="presentation" cellspacing="0" cellpadding="0" style="width:100%;border-collapse:collapse">${q.options.map(opt).join('')}</table>
<div style="padding:9px 12px;border-top:1px solid ${LINE};font-size:13px;color:${INK2}">Cevap: <b style="color:${INK}">${esc(q.answer) || '—'}</b></div>
${q.explanation ? `<div style="padding:10px 12px;border-top:1px solid ${LINE};font-size:13px;line-height:1.55;color:${INK2}">${nl(q.explanation.slice(0, 1600))}</div>` : ''}
</div></td>`;
}

export function questionUpdatedEmail(p: {
  name: string;
  questionNumber?: string | number;
  discipline?: string;
  before: QuestionSnapshot;
  after: QuestionSnapshot;
  summary?: string;
  yourNote?: string;
  link: string;
}) {
  const changes: string[] = [];
  if (norm(p.before.stem) !== norm(p.after.stem)) changes.push('soru kökü');
  if (p.after.options.some((o) => norm(p.before.options.find((x) => x.key === o.key)?.text || '') !== norm(o.text)) || p.before.options.length !== p.after.options.length) changes.push('şıklar');
  if (p.before.answer !== p.after.answer) changes.push(`cevap (${p.before.answer || '—'} → ${p.after.answer})`);
  if (norm(p.before.explanation) !== norm(p.after.explanation)) changes.push('açıklama');
  const no = p.questionNumber ? `#${p.questionNumber}` : '';
  const subject = `Bildirdiğin soru güncellendi ${no}`.trim();
  const html = `<!doctype html><html lang="tr"><body style="margin:0;padding:24px 12px;background:#F4F6FA;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:${INK}">
<div style="max-width:920px;margin:0 auto">
<p style="margin:0 0 4px;font-size:12px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:#2453E6">MeDSor · Çıkmış sorular</p>
<h1 style="margin:0 0 8px;font-size:22px;line-height:1.25">Bildirdiğin soru güncellendi ${esc(no)}</h1>
<p style="margin:0 0 6px;font-size:14.5px;line-height:1.6;color:${INK2}">Merhaba ${esc(p.name)}, ${p.discipline ? `${esc(p.discipline)} dersindeki ` : ''}soruyla ilgili bildirimin yapay zekâ incelemesinden geçti ve soru güncellendi.</p>
${changes.length ? `<p style="margin:0 0 6px;font-size:14px;color:${INK2}">Değişen: <b style="color:${INK}">${esc(changes.join(', '))}</b></p>` : ''}
${p.summary ? `<p style="margin:0 0 6px;font-size:13.5px;line-height:1.55;color:${INK2}">İnceleme notu: ${esc(p.summary)}</p>` : ''}
${p.yourNote ? `<p style="margin:0 0 14px;font-size:13px;line-height:1.55;color:${INK3}">Senin bildirimin: “${esc(p.yourNote.slice(0, 400))}”</p>` : '<div style="height:8px"></div>'}
<table role="presentation" cellspacing="0" cellpadding="0" style="width:100%;border-collapse:collapse;margin:0 -6px"><tr>
${block('Eski hali', p.before, p.after, false)}
${block('Yeni hali', p.after, p.before, true)}
</tr></table>
<p style="margin:18px 0 0"><a href="${esc(p.link)}" style="display:inline-block;padding:11px 18px;border-radius:10px;background:#2453E6;color:#fff;text-decoration:none;font-size:14px;font-weight:600">Soruyu sitede aç</a></p>
<p style="margin:16px 0 0;font-size:12px;line-height:1.5;color:${INK3}">Bu e-postayı, MeDSor'da bu soru için hata bildirdiğin için aldın. Yapay zekâ düzeltmeleri hatalı olabilir; yine yanlış görürsen sorudan yeniden bildirebilirsin.</p>
</div></body></html>`;
  const text = [
    `Bildirdiğin soru güncellendi ${no}`,
    changes.length ? `Değişen: ${changes.join(', ')}` : '',
    '',
    'ESKİ HALİ',
    p.before.stem,
    ...p.before.options.map((o) => `${o.key}) ${o.text}`),
    `Cevap: ${p.before.answer || '—'}`,
    '',
    'YENİ HALİ',
    p.after.stem,
    ...p.after.options.map((o) => `${o.key}) ${o.text}`),
    `Cevap: ${p.after.answer || '—'}`,
    '',
    p.link,
  ].join('\n');
  return { subject, html, text };
}
