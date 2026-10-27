/**
 * Hastalıklar · "Anatomiden gez" görünümü (v15 tasarımı b2hastalik).
 *
 * Organ sistemi uydurulmaz, istemcide gerçek veriden türetilir (deterministik, LLM yok):
 *  1. Profilin `category` alanı (diseases.json, "Uzmanlık / organ sistemi") organ sistemine doğrudan karşılık geliyorsa
 *     o sistem (CATEGORY_SYSTEM).
 *  2. Organ sistemi olmayan uzmanlıklarda (Genel Patoloji, İmmünoloji, Genetik, Enfeksiyon, Farmakoloji, Halk Sağlığı,
 *     Çocuk) yalnız profil ADINDA sözcük sınırlı organ adı geçerse (NAME_RULES) o sistem.
 *  3. Hiçbiri yoksa "Diğer" — zorla atanmaz.
 * Kurul ve "çıkmışta geçen" sayısı disease_lessons.json'dan (hastalik_ders_eslesmesi.py; bayrak 8 = çıkmış soruda geçer).
 * Bulgular: symptoms/pathognomonic/hallmarks maddelerindeki belirti/bulgu türlü varlıklar.
 */
import React, { useMemo, useState } from 'react';
import { ChevronRight, Plus, Search, X } from 'lucide-react';
import type { DiseaseProfile } from '../../types/disease';
import { LESSON_FLAG, useDiseaseLessons } from './diseaseLessons';

export interface OrganSystem { id: string; ad: string; x: number; y: number }

/** Silüet üstündeki konumlar (%; viewBox 0 0 120 260) */
export const SYSTEMS: OrganSystem[] = [
  { id: 'sinir', ad: 'Sinir sistemi ve ruh sağlığı', x: 50, y: 7 },
  { id: 'endokrin', ad: 'Endokrin ve metabolizma', x: 50, y: 18 },
  { id: 'solunum', ad: 'Solunum', x: 40, y: 28 },
  { id: 'kalp', ad: 'Kardiyovasküler', x: 56, y: 30 },
  { id: 'kan', ad: 'Kan ve lenf', x: 66, y: 37 },
  { id: 'sindirim', ad: 'Sindirim', x: 47, y: 42 },
  { id: 'uriner', ad: 'Böbrek ve idrar yolları', x: 57, y: 46 },
  { id: 'ureme', ad: 'Kadın üreme ve gebelik', x: 50, y: 54 },
  { id: 'kas', ad: 'Kas-iskelet', x: 38, y: 74 },
  { id: 'deri', ad: 'Deri', x: 23, y: 45 },
];
const DIGER: OrganSystem = { id: 'diger', ad: 'Diğer (sisteme bağlanamayan)', x: 0, y: 0 };

const CATEGORY_SYSTEM: Record<string, string> = {
  'Kardiyoloji ve Damar': 'kalp',
  'Göğüs Hastalıkları': 'solunum',
  'Gastroenteroloji ve Hepatoloji': 'sindirim',
  'Nefroloji ve Üroloji': 'uriner',
  'Kadın Hastalıkları ve Doğum': 'ureme',
  'Endokrinoloji ve Metabolizma': 'endokrin',
  'Nöroloji ve Nöroşirürji': 'sinir',
  'Psikiyatri': 'sinir',
  'Hematoloji': 'kan',
  'Kas-İskelet Sistemi': 'kas',
  'Dermatoloji': 'deri',
};

/** Ad içinde sözcük başında geçen organ kökleri (yalnız organ dışı uzmanlıklar için) */
const NAME_RULES: Array<[RegExp, string]> = [
  [/(^|[\s(-])(kalp|kardiy|miyokard|perikard|endokard|aort|koroner|arter|ven[öo]z|damar|vaskül)/i, 'kalp'],
  [/(^|[\s(-])(akciğer|pulmon|bronş|plevr|pnömon|solunum|trake)/i, 'solunum'],
  [/(^|[\s(-])(karaciğer|hepat|mide|gastr|bağırsak|kolon|özofag|pankrea|safra|intestin|rektum)/i, 'sindirim'],
  [/(^|[\s(-])(böbrek|renal|nefr|glomerül|mesane|üret|idrar|prostat|testis)/i, 'uriner'],
  [/(^|[\s(-])(uterus|over|serviks|endometri|vajen|plasenta|gebelik|meme)/i, 'ureme'],
  [/(^|[\s(-])(tiroid|paratiroid|adrenal|hipofiz|diyabet)/i, 'endokrin'],
  [/(^|[\s(-])(beyin|serebr|nöro|menenj|ensefal|spinal|sinir)/i, 'sinir'],
  [/(^|[\s(-])(lösemi|lenfoma|anemi|lenf|kan\b|trombosit|hemoli|miyelom)/i, 'kan'],
  [/(^|[\s(-])(kemik|osteo|eklem|artrit|kas\b|miyopati|kıkırdak)/i, 'kas'],
  [/(^|[\s(-])(deri|derma|kutan)/i, 'deri'],
];

export function systemOf(d: DiseaseProfile): string {
  const c = CATEGORY_SYSTEM[d.category];
  if (c) return c;
  for (const [re, id] of NAME_RULES) if (re.test(d.name)) return id;
  return 'diger';
}

const FINDING_TYPES = new Set(['belirti', 'bulgu']);
export function findingsOf(d: DiseaseProfile): string[] {
  const out = new Set<string>();
  const facts = [...(d.sections.symptoms || []), ...(d.sections.pathognomonic || []), ...(d.hallmarks || [])];
  for (const f of facts) for (const e of f.entities || []) if (FINDING_TYPES.has(e.type) && e.name) out.add(e.name.toLocaleLowerCase('tr-TR'));
  return [...out];
}

const cap = (s: string) => s.charAt(0).toLocaleUpperCase('tr-TR') + s.slice(1);

const Silhouette: React.FC = () => (
  <svg className="an15-body" viewBox="0 0 120 260" aria-hidden focusable="false">
    <g fill="var(--color-line-soft, var(--color-line))" stroke="var(--color-ink-3)" strokeWidth="1" strokeLinejoin="round">
      <circle cx="60" cy="20" r="15" />
      <path d="M52 34h16v8H52z" />
      <path d="M34 46c4-5 14-6 26-6s22 1 26 6l4 50c0 6-4 10-8 46l-4 10H42l-4-10c-4-36-8-40-8-46z" />
      <path d="M33 48l-12 40-6 52 7 2 10-50 8-30z" />
      <path d="M87 48l12 40 6 52-7 2-10-50-8-30z" />
      <path d="M44 150l-4 54-2 50h12l6-54 4-46z" />
      <path d="M76 150l4 54 2 50H70l-6-54-4-46z" />
    </g>
  </svg>
);

export const DiseaseAnatomy: React.FC<{ diseases: DiseaseProfile[]; onOpen: (d: DiseaseProfile) => void }> = ({ diseases, onOpen }) => {
  const lessons = useDiseaseLessons();

  const bySys = useMemo(() => {
    const m = new Map<string, DiseaseProfile[]>();
    for (const d of diseases) {
      const s = systemOf(d);
      if (!m.has(s)) m.set(s, []);
      m.get(s)!.push(d);
    }
    return m;
  }, [diseases]);
  const findings = useMemo(() => new Map(diseases.map((d) => [d.id, findingsOf(d)])), [diseases]);
  const pastIds = useMemo(() => {
    const s = new Set<string>();
    if (lessons) for (const [id, rows] of Object.entries(lessons.hastaliklar)) if (rows.some((r) => r[2] & LESSON_FLAG.cikmis)) s.add(id);
    return s;
  }, [lessons]);

  const firstSys = SYSTEMS.reduce((a, b) => ((bySys.get(b.id)?.length || 0) > (bySys.get(a.id)?.length || 0) ? b : a), SYSTEMS[0]);
  const [sysId, setSysId] = useState<string | null>(null);
  const cur = sysId ?? firstSys.id;
  const sys = cur === 'diger' ? DIGER : SYSTEMS.find((s) => s.id === cur)!;
  const list = bySys.get(cur) || [];

  // Sistemin en sık kurulu (ders eşlemesinden)
  const kurul = useMemo(() => {
    if (!lessons) return null;
    const cnt = new Map<number, number>();
    for (const d of list) for (const r of lessons.hastaliklar[d.id] || []) {
      const k = lessons.konular[r[0]]?.k;
      if (k != null) cnt.set(k, (cnt.get(k) || 0) + 1);
    }
    let best: number | null = null;
    for (const [k, n] of cnt) if (best == null || n > (cnt.get(best) || 0)) best = k;
    return best;
  }, [lessons, list]);
  const pastN = list.filter((d) => pastIds.has(d.id)).length;

  const [picked, setPicked] = useState<string[]>([]);
  const [adding, setAdding] = useState(false);
  const [fq, setFq] = useState('');
  const pickSys = (id: string) => { setSysId(id); setPicked([]); setAdding(false); };

  const options = useMemo(() => {
    const cnt = new Map<string, number>();
    for (const d of list) for (const f of findings.get(d.id) || []) cnt.set(f, (cnt.get(f) || 0) + 1);
    return [...cnt].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'tr'));
  }, [list, findings]);
  const shownOpts = options.filter(([f]) => !picked.includes(f) && (!fq || f.includes(fq.toLocaleLowerCase('tr-TR')))).slice(0, 24);

  const matches = useMemo(() => {
    const rows = list.map((d) => ({ d, f: findings.get(d.id) || [] })).filter((r) => picked.every((p) => r.f.includes(p)));
    rows.sort((a, b) => (+pastIds.has(b.d.id) - +pastIds.has(a.d.id)) || a.d.name.localeCompare(b.d.name, 'tr'));
    return rows;
  }, [list, findings, picked, pastIds]);

  const kurulAd = kurul != null ? `Kurul ${kurul}` : null;
  const meta = [kurulAd, `${list.length} hastalık`, lessons && pastN > 0 ? `${pastN} çıkmışta geçen` : null].filter(Boolean).join(' · ');
  const digerN = bySys.get('diger')?.length || 0;

  return (
    <div className="an15">
      <div className="g12-panel an15-g">
        <div className="an15-fig">
          <Silhouette />
          {SYSTEMS.map((s) => {
            const n = bySys.get(s.id)?.length || 0;
            return (
              <button key={s.id} type="button" className={`an15-dot ${s.id === cur ? 'is-on' : ''}`} style={{ left: `${s.x}%`, top: `${s.y}%` }}
                disabled={n === 0} aria-pressed={s.id === cur} aria-label={`${s.ad}: ${n} hastalık`} title={`${s.ad} · ${n}`} onClick={() => pickSys(s.id)} />
            );
          })}
        </div>
        {digerN > 0 && (
          <button type="button" className={`g12-chip an15-diger ${cur === 'diger' ? 'is-on' : ''}`} aria-pressed={cur === 'diger'} onClick={() => pickSys('diger')}>
            Diğer · {digerN}
          </button>
        )}
      </div>

      <div className="an15-y">
        <div className="g12-panel an15-sys">
          <div className="an15-sys-t">
            <b>{sys.ad}</b>
            <span className="g12-m">{meta}</span>
          </div>
          <ChevronRight aria-hidden />
        </div>

        <span className="g12-sub an15-lbl">Bulgular</span>
        <div className="g12-chips an15-cips">
          {picked.map((f) => (
            <button key={f} type="button" className="g12-chip" onClick={() => setPicked(picked.filter((x) => x !== f))} aria-label={`${f} bulgusunu kaldır`}>
              <span>{cap(f)}</span><X aria-hidden />
            </button>
          ))}
          {options.length > 0 && (
            <button type="button" className="g12-chip an15-add" aria-expanded={adding} onClick={() => setAdding((v) => !v)}>
              <Plus aria-hidden /><span>Bulgu ekle</span>
            </button>
          )}
          {picked.length > 1 && <button type="button" className="g12-chip-clear" onClick={() => setPicked([])}>Temizle</button>}
        </div>
        {adding && (
          <div className="g12-panel an15-pick">
            <label className="g12-field">
              <Search aria-hidden />
              <input type="search" value={fq} onChange={(e) => setFq(e.target.value)} placeholder="Bulgu ara" aria-label="Bulgu ara" />
            </label>
            <div className="g12-pills">
              {shownOpts.map(([f, n]) => (
                <button key={f} type="button" className="g12-pill" onClick={() => { setPicked([...picked, f]); setFq(''); }}>
                  <span>{cap(f)}</span><b className="g12-num">{n}</b>
                </button>
              ))}
              {shownOpts.length === 0 && <span className="g12-m">Eşleşen bulgu yok.</span>}
            </div>
          </div>
        )}

        <div className="g12-panel an15-list">
          {matches.length === 0 ? (
            <p className="g12-m an15-empty">Seçilen bulguların tümünü içeren hastalık yok.</p>
          ) : (
            <ul>
              {matches.slice(0, 60).map(({ d, f }) => {
                const lbl = (picked.length ? picked : f.slice(0, 2)).map(cap).join(' · ');
                return (
                  <li key={d.id}>
                    <button type="button" className="g12-row" onClick={() => onOpen(d)}>
                      <span className="g12-row-t">
                        <span className="t">{d.name}</span>
                        {pastIds.has(d.id) && <span className="g12-badge is-warn">Çıkmışta</span>}
                      </span>
                      {lbl && <span className="d">{lbl}</span>}
                    </button>
                  </li>
                );
              })}
            </ul>
          )}
          {matches.length > 60 && <p className="g12-m an15-empty">İlk 60 gösteriliyor ({matches.length}). Bulgu ekleyerek daralt.</p>}
        </div>
      </div>
    </div>
  );
};
