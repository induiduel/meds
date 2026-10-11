import React, { useEffect, useMemo, useState } from 'react';
import { BookmarkCheck, Check, Clock3, Flag, MessageSquare, NotebookPen, PenLine, Plus, RotateCcw, Star, X } from 'lucide-react';
import type { QuestionItem } from '../../types';
import type { AppUser } from '../../services/auth';
import type { AppRoute } from '../../router';
import { PageHeader } from '../ui/PageHeader';
import {
  getFavoriteCards, getFavorites, getNotes, getProgress, getReview, getTestHistory, loadArchiveBank, type StudyQuestion,
} from '../../services/studyStore';
import { dayKey, getActivity, getStudySeconds, type ActivityKind } from '../../services/activityLog';
import { computeContributorStats } from '../../utils/contributionScore';

/**
 * İstatistiklerim (yeniden kurulum 2026-10-11, canvas "Stats" artboard'u).
 * Tüm sayılar gerçek kaynaklardan gelir: çözüm geçmişi, çalışma süresi ve etkinlik günlüğü bu cihazdadır
 * (localStorage); katkı puanı ve sıralama Sıralama sayfasıyla aynı hesapla havuz verisinden çıkar.
 */
interface Props {
  questions: QuestionItem[];
  currentUser: AppUser | null;
  onGo: (r: AppRoute) => void;
}

type Period = 'hafta' | 'ay' | 'tum';
const DAY = 86_400_000;
const nf = new Intl.NumberFormat('tr-TR');
const fmtDur = (sec: number) => {
  const h = Math.floor(sec / 3600);
  const m = Math.round((sec % 3600) / 60);
  return h ? `${h} sa ${m} dk` : `${m} dk`;
};
const KIND: Record<ActivityKind, { label: string; cls: string }> = {
  coz: { label: 'Çözdü', cls: 'k-coz' },
  yanlis: { label: 'Yanlış', cls: 'k-yan' },
  not: { label: 'Not', cls: 'k-not' },
  begen: { label: 'Beğendi', cls: 'k-beg' },
  kaydet: { label: 'Kaydetti', cls: 'k-beg' },
  katki: { label: 'Katkı', cls: 'k-kat' },
  test: { label: 'Test', cls: 'k-coz' },
  bitir: { label: 'Bitirdi', cls: 'k-bit' },
};
const relTime = (iso: string) => {
  const d = Date.now() - Date.parse(iso);
  if (d < 60_000) return 'şimdi';
  if (d < 3_600_000) return `${Math.floor(d / 60_000)} dk`;
  if (d < DAY) return `${Math.floor(d / 3_600_000)} sa`;
  if (d < 7 * DAY) return `${Math.floor(d / DAY)} gün`;
  return new Date(iso).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
};
const readCardNotes = (): number => {
  try { return Object.keys(JSON.parse(localStorage.getItem('medsoru_card_notes_v1') || '{}')).length; } catch { return 0; }
};

export const StatsView: React.FC<Props> = ({ questions, currentUser, onGo }) => {
  const [period, setPeriod] = useState<Period>('hafta');
  const [tab, setTab] = useState<'fav' | 'kart' | 'not' | 'tekrar'>('fav');
  const [bank, setBank] = useState<StudyQuestion[]>([]);
  useEffect(() => { loadArchiveBank().then(setBank).catch(() => setBank([])); }, []);

  const since = period === 'hafta' ? Date.now() - 7 * DAY : period === 'ay' ? Date.now() - 30 * DAY : 0;
  const progress = useMemo(() => getProgress(), []);
  const attempts = useMemo(() => Object.entries(progress), [progress]);
  const inPeriod = attempts.filter(([, a]) => Date.parse(a.at) >= since);
  const correct = inPeriod.filter(([, a]) => a.correct).length;
  const wrongAll = attempts.filter(([, a]) => !a.correct).length;
  const accuracy = inPeriod.length ? Math.round((correct / inPeriod.length) * 100) : 0;

  const seconds = useMemo(() => getStudySeconds(), []);
  const periodSec = Object.entries(seconds).filter(([d]) => Date.parse(d) >= since - DAY).reduce((a, [, s]) => a + s, 0);
  const totalSec = Object.values(seconds).reduce((a, s) => a + s, 0);

  // Seri: bugünden geriye kesintisiz çalışılan günler
  const streak = useMemo(() => {
    const active = new Set([...Object.keys(seconds).filter((d) => seconds[d] >= 60), ...attempts.map(([, a]) => dayKey(new Date(a.at)))]);
    let n = 0;
    for (let d = new Date(); active.has(dayKey(d)); d = new Date(d.getTime() - DAY)) n++;
    return n;
  }, [seconds, attempts]);

  // Katkı puanı, sıralama ve haftalık puan değişimi (Sıralama ile aynı ağırlıklar)
  const contrib = useMemo(() => {
    const board = computeContributorStats(questions, currentUser);
    const me = board.find((b) => b.isCurrentUser);
    const ranked = board.filter((b) => b.totalPoints > 0);
    const rank = me && me.totalPoints > 0 ? ranked.findIndex((b) => b.id === me.id) + 1 : null;
    const myKeys = new Set([currentUser?.uid, currentUser?.displayName, currentUser?.email].filter(Boolean).map((s) => String(s).toLowerCase()));
    const weeks = Array.from({ length: 8 }, () => 0);
    const add = (iso: string | undefined, pts: number) => {
      if (!iso) return;
      const ago = Math.floor((Date.now() - Date.parse(iso)) / (7 * DAY));
      if (ago >= 0 && ago < 8) weeks[7 - ago] += pts;
    };
    questions.forEach((q) => {
      if (myKeys.has(String(q.contributedByUid || q.contributedByName || '').toLowerCase())) add(q.createdAt, 10);
      q.fragments.forEach((f) => { if (myKeys.has(String(f.authorUid || f.author || '').toLowerCase())) add(f.timestamp, f.type === 'stem' ? 10 : 5); });
    });
    return { me, rank, weeks };
  }, [questions, currentUser]);

  // Son 14 gün: günlük çözülen (doğru/yanlış)
  const days = useMemo(() => {
    const out = Array.from({ length: 14 }, (_, i) => {
      const d = new Date(Date.now() - (13 - i) * DAY);
      return { key: dayKey(d), lab: String(d.getDate()), today: i === 13, ok: 0, bad: 0 };
    });
    const idx = new Map(out.map((d, i) => [d.key, i]));
    attempts.forEach(([, a]) => {
      const i = idx.get(dayKey(new Date(a.at)));
      if (i !== undefined) a.correct ? out[i].ok++ : out[i].bad++;
    });
    return out;
  }, [attempts]);
  const dayMax = Math.max(4, ...days.map((d) => d.ok + d.bad));
  const dayAvg = Math.round(days.reduce((a, d) => a + d.ok + d.bad, 0) / 14);

  // 12 haftalık çalışma takvimi (süre)
  const heat = useMemo(() => {
    const today = new Date();
    const start = new Date(today.getTime() - (83 + ((today.getDay() + 6) % 7)) * DAY);
    return Array.from({ length: 84 + ((today.getDay() + 6) % 7) + 1 }, (_, i) => {
      const d = new Date(start.getTime() + i * DAY);
      const s = seconds[dayKey(d)] || 0;
      return { key: dayKey(d), s, lvl: s === 0 ? 0 : s < 900 ? 1 : s < 1800 ? 2 : s < 3600 ? 3 : 4 };
    }).slice(-84);
  }, [seconds]);

  // Ders bazında
  const byLesson = useMemo(() => {
    const disc = new Map(bank.map((q) => [q.id, q.discipline]));
    const m = new Map<string, { n: number; ok: number }>();
    attempts.forEach(([id, a]) => {
      const d = disc.get(id);
      if (!d) return;
      const e = m.get(d) || { n: 0, ok: 0 };
      e.n++; if (a.correct) e.ok++;
      m.set(d, e);
    });
    return [...m.entries()].sort((a, b) => b[1].n - a[1].n).slice(0, 6);
  }, [bank, attempts]);
  const lessonMax = Math.max(1, ...byLesson.map(([, v]) => v.n));

  const favorites = useMemo(() => [...getFavorites()], []);
  const favCards = useMemo(() => getFavoriteCards(), []);
  const notes = useMemo(() => getNotes(), []);
  const review = useMemo(() => [...getReview()], []);
  const tests = useMemo(() => getTestHistory(), []);
  const cardNotes = useMemo(readCardNotes, []);
  const activity = useMemo(() => getActivity().slice(-40).reverse(), []);
  const bankById = useMemo(() => new Map(bank.map((q) => [q.id, q])), [bank]);
  const contribCount = activity.filter((a) => a.kind === 'katki').length;

  // Puan grafiği (8 hafta, kümülatif)
  const cum = contrib.weeks.reduce<number[]>((acc, v) => [...acc, (acc[acc.length - 1] || 0) + v], []);
  const base = Math.max(0, (contrib.me?.totalPoints || 0) - (cum[cum.length - 1] || 0));
  const series = cum.map((v) => v + base);
  const sMax = Math.max(10, ...series);
  const px = (i: number) => 44 + i * 70;
  const py = (v: number) => 160 - (v / sMax) * 140;
  const line = series.map((v, i) => `${px(i)},${Math.round(py(v))}`).join(' ');
  const area = `M${px(0)},160 L${line.replace(/ /g, ' L')} L${px(7)},160 Z`;
  const weekDelta = contrib.weeks[7];

  const savedTabs = [
    { id: 'fav' as const, label: 'Favori sorular', n: favorites.length, rows: favorites.slice(0, 5).map((id) => ({ t: bankById.get(id)?.stem || id, m: [bankById.get(id)?.discipline, bankById.get(id)?.year].filter(Boolean).join(' · ') || 'Soru' })) },
    { id: 'kart' as const, label: 'Beğenilen kartlar', n: favCards.length, rows: favCards.slice(0, 5).map((c) => ({ t: c.front, m: c.group || 'Kart' })) },
    { id: 'not' as const, label: 'Notların', n: notes.length + cardNotes, rows: notes.slice(0, 5).map((n) => ({ t: n.title || 'Başlıksız not', m: new Date(n.updatedAt).toLocaleDateString('tr-TR') })) },
    { id: 'tekrar' as const, label: 'Tekrar listesi', n: review.length, rows: review.slice(0, 5).map((id) => ({ t: bankById.get(id)?.stem || id, m: bankById.get(id)?.discipline || 'Soru' })) },
  ];
  const curTab = savedTabs.find((s) => s.id === tab)!;

  return (
    <div className="st flex flex-col gap-3 min-w-0 pb-12">
      <PageHeader title="İstatistiklerim" description="Çözdüğün sorular, çalışma süren, katkıların ve kaydettiklerin. Çözüm ve süre verisi bu cihazda tutulur." />

      <div className="st-bar">
        <span className="st-seg" role="radiogroup" aria-label="Dönem">
          {([['hafta', 'Bu hafta'], ['ay', 'Bu ay'], ['tum', 'Tümü']] as const).map(([id, l]) => (
            <button key={id} type="button" role="radio" aria-checked={period === id} onClick={() => setPeriod(id)}>{l}</button>
          ))}
        </span>
      </div>

      <section className="st-card st-kpis" aria-label="Özet">
        <div className="st-kpi"><span className="l">Toplam puan</span><span className="v">{nf.format(contrib.me?.totalPoints || 0)}</span><span className={`d ${weekDelta > 0 ? 'up' : ''}`}>{weekDelta > 0 ? `+${weekDelta} bu hafta` : 'bu hafta katkı yok'}</span></div>
        <div className="st-kpi"><span className="l">Sıralamadaki yerin</span><span className="v">{contrib.rank ? `${contrib.rank}.` : '—'}</span><span className="d">{contrib.rank ? 'katkı sıralamasında' : 'katkı yapınca görünür'}</span></div>
        <div className="st-kpi"><span className="l">Çözülen soru</span><span className="v">{nf.format(inPeriod.length)}</span><span className="d">toplam {nf.format(attempts.length)}</span></div>
        <div className="st-kpi"><span className="l">Doğruluk</span><span className="v">%{accuracy}</span><span className="d">{correct} doğru · {inPeriod.length - correct} yanlış</span></div>
        <div className="st-kpi"><span className="l">Çalışma süresi</span><span className="v">{fmtDur(periodSec)}</span><span className="d">toplam {fmtDur(totalSec)}</span></div>
        <div className="st-kpi"><span className="l">Seri</span><span className="v">{streak} gün</span><span className="d">arka arkaya çalışılan</span></div>
      </section>

      <div className="st-grid">
        <section className="st-card" aria-label="Puan değişimi">
          <div className="st-h"><b>Puan değişimi</b><span>son 8 hafta</span></div>
          <svg viewBox="0 0 560 176" role="img" aria-label={`Son 8 haftada puan ${series[0]} → ${series[7]}`} className="st-line">
            {[20, 70, 120].map((y) => <line key={y} x1="36" x2="548" y1={y} y2={y} className="st-grid-l" />)}
            <line x1="36" x2="548" y1="160" y2="160" className="st-axis" />
            <path d={area} className="st-area" />
            <polyline points={line} className="st-poly" />
            {series.map((v, i) => <circle key={i} cx={px(i)} cy={py(v)} r={i === 7 ? 5 : 3} className="st-dot" />)}
            <text x={px(7)} y={py(series[7]) - 12} textAnchor="middle" className="st-last">{series[7]}</text>
          </svg>
          <div className="st-xl">{series.map((_, i) => <span key={i}>{i === 7 ? 'Bu hf' : `H-${7 - i}`}</span>)}</div>
        </section>

        <section className="st-card" aria-label="Günlük çözülen soru">
          <div className="st-h"><b>Günlük çözülen soru</b><span>son 14 gün · ort. {dayAvg}</span><span className="st-lg"><i className="is-ok" />Doğru <i className="is-bad" />Yanlış</span></div>
          <div className="st-bars" role="img" aria-label="Son 14 günde günlük çözülen soru sayısı">
            {days.map((d) => (
              <div key={d.key} className={`st-col ${d.today ? 'is-today' : ''}`} title={`${d.ok + d.bad} soru · ${d.ok} doğru · ${d.bad} yanlış`}>
                <span className="n">{d.ok + d.bad || ''}</span>
                <span className="bad" style={{ height: `${(d.bad / dayMax) * 112}px` }} />
                <span className="ok" style={{ height: `${(d.ok / dayMax) * 112}px` }} />
              </div>
            ))}
          </div>
          <div className="st-xl is-14">{days.map((d) => <span key={d.key} className={d.today ? 'is-today' : ''}>{d.lab}</span>)}</div>
        </section>
      </div>

      <div className="st-grid">
        <section className="st-card" aria-label="Ders bazında">
          <div className="st-h"><b>Ders bazında</b><span>çözdüğün çıkmış sorular</span></div>
          {byLesson.length ? byLesson.map(([d, v]) => {
            const acc = Math.round((v.ok / v.n) * 100);
            return (
              <div key={d} className="st-row">
                <span className="t">{d}</span>
                <span className="n">{v.n}</span>
                <span className={`n ${acc >= 75 ? 'is-ok' : acc < 60 ? 'is-bad' : ''}`}>%{acc}</span>
                <span className="st-meter"><span style={{ width: `${(v.n / lessonMax) * 100}%` }} /></span>
              </div>
            );
          }) : <p className="st-empty">Çalış sayfasında soru çözdükçe ders dökümü burada belirir.</p>}
        </section>

        <section className="st-card" aria-label="Çalışma takvimi">
          <div className="st-h"><b>Çalışma takvimi</b><span>son 12 hafta</span><span className="st-sp" /><span className="st-mono">{fmtDur(totalSec)}</span></div>
          <div className="st-heat-wrap">
            <div className="st-heat" role="img" aria-label="Son 12 haftada günlük çalışma süresi">
              {heat.map((h) => <i key={h.key} className={h.lvl ? `l${h.lvl}` : ''} title={`${new Date(h.key).toLocaleDateString('tr-TR')} · ${fmtDur(h.s)}`} />)}
            </div>
          </div>
          <div className="st-legend">Az <span className="st-heat is-legend"><i /><i className="l1" /><i className="l2" /><i className="l3" /><i className="l4" /></span> Çok</div>
          <p className="st-note"><Clock3 aria-hidden /> Süre, sekme açıkken ve son bir dakikada etkileşim varken sayılır.</p>
        </section>
      </div>

      <div className="st-grid is-3">
        <section className="st-card" aria-label="Soru durumu">
          <div className="st-h"><b>Soru durumu</b></div>
          <button type="button" className="st-li" onClick={() => onGo('study')}><span className="ic is-ok"><Check /></span>Doğru çözdüklerin<span className="n">{nf.format(attempts.length - wrongAll)}</span></button>
          <button type="button" className="st-li" onClick={() => onGo('study')}><span className="ic is-bad"><X /></span>Yanlışların<span className="n">{nf.format(wrongAll)}</span></button>
          <button type="button" className="st-li" onClick={() => onGo('study')}><span className="ic is-warn"><RotateCcw /></span>Tekrar listesi<span className="n">{review.length}</span></button>
          <button type="button" className="st-li" onClick={() => onGo('practice')}><span className="ic"><Flag /></span>Bitirdiğin testler<span className="n">{tests.length}</span></button>
          {wrongAll > 0 && <div className="st-cta"><button type="button" className="st-primary" onClick={() => onGo('study')}>{wrongAll} yanlışı yeniden çöz</button></div>}
        </section>

        <section className="st-card" aria-label="Katkıların">
          <div className="st-h"><b>Katkıların</b></div>
          <button type="button" className="st-li" onClick={() => onGo('questions')}><span className="ic is-accent"><Plus /></span>Eklediğin sorular<span className="n">{contrib.me?.questionsCount || 0}</span></button>
          <button type="button" className="st-li" onClick={() => onGo('questions')}><span className="ic is-clinic"><PenLine /></span>Önerdiğin şıklar<span className="n">{contrib.me?.optionsCount || 0}</span></button>
          <button type="button" className="st-li" onClick={() => onGo('questions')}><span className="ic"><RotateCcw /></span>Düzeltmelerin<span className="n">{contrib.me?.revisionsCount || 0}</span></button>
          <button type="button" className="st-li" onClick={() => onGo('leaderboard')}><span className="ic is-ai"><Star /></span>Aldığın beğeni<span className="n">{contrib.me?.upvotesCount || 0}</span></button>
          <button type="button" className="st-li" onClick={() => onGo('past_exams')}><span className="ic"><MessageSquare /></span>Bu cihazdaki katkı işlemleri<span className="n">{contribCount}</span></button>
        </section>

        <section className="st-card" aria-label="Kaydettiklerin">
          <div className="st-h"><b>Kaydettiklerin</b></div>
          <div className="stx-tabs" role="tablist" aria-label="Kayıt türü">
            {savedTabs.map((s) => (
              <button key={s.id} type="button" role="tab" aria-selected={tab === s.id} onClick={() => setTab(s.id)}>{s.label}<span>{s.n}</span></button>
            ))}
          </div>
          {curTab.rows.length ? curTab.rows.map((r, i) => (
            <div key={i} className="st-saved"><b>{r.t}</b><span>{r.m}</span></div>
          )) : <p className="st-empty">{tab === 'fav' ? 'Çalışırken yıldızladığın sorular burada.' : tab === 'kart' ? 'Ezber kartlarında yıldızladıkların burada.' : tab === 'not' ? 'Notlar ve kart notların burada.' : 'Yanlış yaptığın sorular burada toplanır.'}</p>}
          <div className="st-cta"><button type="button" className="st-link" onClick={() => onGo(tab === 'kart' ? 'flashcards' : 'study')}>{tab === 'kart' ? <BookmarkCheck /> : <NotebookPen />} Tümünü aç</button></div>
        </section>
      </div>

      <section className="st-card" aria-label="Etkinlik akışı">
        <div className="st-h"><b>Etkinlik akışı</b><span>bu cihazda yaptığın işlemler</span></div>
        {activity.length ? activity.slice(0, 12).map((a, i) => (
          <div key={i} className="st-feed"><span className={`kind ${KIND[a.kind]?.cls || ''}`}>{KIND[a.kind]?.label || a.kind}</span><span className="t">{a.text}</span><span className="w">{relTime(a.at)}</span></div>
        )) : <p className="st-empty">Soru çözdükçe, not aldıkça ve katkı yaptıkça işlemlerin burada listelenir.</p>}
      </section>
    </div>
  );
};

export default StatsView;
