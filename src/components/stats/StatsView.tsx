import React, { useEffect, useMemo, useState } from 'react';
import { BookmarkCheck, Check, ChevronRight, Clock3, Flag, Headphones, MessageSquare, NotebookPen, PenLine, Plus, RotateCcw, Star, Trophy, X } from 'lucide-react';
import type { QuestionItem } from '../../types';
import type { AppUser } from '../../services/auth';
import type { AppRoute } from '../../router';
import {
  getFavoriteCards, getFavorites, getNotes, getReview, loadArchiveBank, type StudyQuestion,
} from '../../services/studyStore';
import { getStatsAttempts, getStatsTests } from '../../services/progressReset';
import { dayKey, getActivity, getStudySeconds, type ActivityKind } from '../../services/activityLog';
import { computeContributorStats } from '../../utils/contributionScore';
import { useSpotCozucuStats, fmtSureDk } from '../../services/spotCozucuIstatistik';
import './stats.css';
import { useAppearance } from '../../utils/appearance';
const CalismaGrafikleriV15 = React.lazy(() => import('../v15/CalismaGrafikleriV15'));
import '../../styles/v12/secondary.css';

/**
 * İstatistiklerim (v10 kompakt yeniden kurulum 2026-10-13, "Istatistik-Masaustu" artboard'u).
 * Üstte dönem seçici (7 gün / 30 gün / Kurul), 4 KPI kutusu (önceki döneme göre fark), derslere göre
 * doğruluk çubukları, 12 haftalık etkinlik ısı haritası ve zayıf konular; altında ayrıntılar
 * (puan değişimi, günlük çözülen, soru durumu, katkılar, kaydettiklerin, etkinlik akışı).
 * Tüm sayılar gerçek kaynaklardan gelir: çözüm geçmişi, çalışma süresi ve etkinlik günlüğü bu cihazdadır
 * (localStorage); katkı puanı ve sıralama Sıralama sayfasıyla aynı hesapla havuz verisinden çıkar.
 * Verisi olmayan bileşen gösterilmez.
 */
interface Props {
  questions: QuestionItem[];
  currentUser: AppUser | null;
  onGo: (r: AppRoute) => void;
}

type Period = 'hafta' | 'ay' | 'kurul';
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
/** "kurul-3", "k3", "3" → "Kurul 3"; tanınmazsa kimliğin kendisi. */
const kurulLabel = (id: string) => {
  const n = /(\d+)/.exec(id)?.[1];
  return n ? `Kurul ${n}` : id;
};
/** Doğruluk eşikleri: ≥%70 iyi, ≥%55 orta, altı zayıf. */
const tone = (acc: number) => (acc >= 70 ? 'is-good' : acc >= 55 ? 'is-mid' : 'is-bad');
const signed = (n: number) => (n > 0 ? `+${nf.format(n)}` : n < 0 ? `−${nf.format(-n)}` : '±0');

export const StatsView: React.FC<Props> = ({ questions, currentUser, onGo }) => {
  const [period, setPeriod] = useState<Period>('hafta');
  const [tab, setTab] = useState<'fav' | 'kart' | 'not' | 'tekrar'>('fav');
  const spotStats = useSpotCozucuStats();
  const [bank, setBank] = useState<StudyQuestion[]>([]);
  const [bankReady, setBankReady] = useState(false);
  useEffect(() => {
    loadArchiveBank().then(setBank).catch(() => setBank([])).finally(() => setBankReady(true));
  }, []);

  // Arşiv dahil: ilerleme sıfırlansa da istatistikler korunur
  const attempts = useMemo(() => getStatsAttempts(), []);
  const bankById = useMemo(() => new Map(bank.map((q) => [q.id, q])), [bank]);
  const wrongAll = attempts.filter(([, a]) => !a.correct).length;

  // "Kurul" dönemi: en son çözülen sorunun kurulu (şu an çalışılan kurul)
  const currentKurul = useMemo(() => {
    let best: { at: number; kid: string } | null = null;
    attempts.forEach(([id, a]) => {
      const kid = bankById.get(id)?.committeeId;
      const at = Date.parse(a.at);
      if (kid && (!best || at > best.at)) best = { at, kid };
    });
    return (best as { at: number; kid: string } | null)?.kid || null;
  }, [attempts, bankById]);

  // Dönem penceresi ve karşılaştırma için bir önceki eşit pencere
  const win = period === 'hafta' ? 7 * DAY : period === 'ay' ? 30 * DAY : 7 * DAY;
  const now = Date.now();
  const since = now - win;
  const prevSince = now - 2 * win;
  const inScope = (id: string, at: string, from: number, to = Infinity) => {
    if (period === 'kurul') return bankById.get(id)?.committeeId === currentKurul;
    const t = Date.parse(at);
    return t >= from && t < to;
  };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const inPeriod = useMemo(() => attempts.filter(([id, a]) => inScope(id, a.at, since)), [attempts, bankById, period, currentKurul]);
  const prevPeriod = period === 'kurul' ? [] : attempts.filter(([id, a]) => inScope(id, a.at, prevSince, since));
  const correct = inPeriod.filter(([, a]) => a.correct).length;
  const accuracy = inPeriod.length ? Math.round((correct / inPeriod.length) * 100) : 0;
  const prevAcc = prevPeriod.length ? Math.round((prevPeriod.filter(([, a]) => a.correct).length / prevPeriod.length) * 100) : null;
  const kurulWeek = period === 'kurul' ? inPeriod.filter(([, a]) => Date.parse(a.at) >= now - 7 * DAY).length : 0;

  const seconds = useMemo(() => getStudySeconds(), []);
  const secBetween = (from: number, to: number) => Object.entries(seconds).filter(([d]) => { const t = Date.parse(d); return t >= from - DAY && t < to - DAY; }).reduce((a, [, s]) => a + s, 0);
  const totalSec = Object.values(seconds).reduce((a, s) => a + s, 0);
  const periodSec = period === 'kurul' ? totalSec : secBetween(since, now + DAY);
  const prevSec = period === 'kurul' ? 0 : secBetween(prevSince, since);

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
  const dayTotal = days.reduce((a, d) => a + d.ok + d.bad, 0);
  const dayAvg = Math.round(dayTotal / 14);

  // 12 haftalık etkinlik (çalışma süresi; süre yoksa o gün çözülen soru da etkinlik sayılır)
  const heat = useMemo(() => {
    const solvedByDay = new Map<string, number>();
    attempts.forEach(([, a]) => { const k = dayKey(new Date(a.at)); solvedByDay.set(k, (solvedByDay.get(k) || 0) + 1); });
    const today = new Date();
    const start = new Date(today.getTime() - (83 + ((today.getDay() + 6) % 7)) * DAY);
    return Array.from({ length: 84 + ((today.getDay() + 6) % 7) + 1 }, (_, i) => {
      const d = new Date(start.getTime() + i * DAY);
      const k = dayKey(d);
      const s = seconds[k] || 0;
      const n = solvedByDay.get(k) || 0;
      const lvl = s >= 3600 || n >= 40 ? 4 : s >= 1800 || n >= 20 ? 3 : s >= 900 || n >= 8 ? 2 : s > 0 || n > 0 ? 1 : 0;
      return { key: k, s, n, lvl };
    }).slice(-84);
  }, [seconds, attempts]);
  const heatActive = heat.some((h) => h.lvl > 0);

  // Derslere göre doğruluk (seçili dönem)
  const byLesson = useMemo(() => {
    const m = new Map<string, { n: number; ok: number }>();
    inPeriod.forEach(([id, a]) => {
      const d = bankById.get(id)?.discipline;
      if (!d) return;
      const e = m.get(d) || { n: 0, ok: 0 };
      e.n++; if (a.correct) e.ok++;
      m.set(d, e);
    });
    return [...m.entries()].map(([d, v]) => ({ d, n: v.n, acc: Math.round((v.ok / v.n) * 100) }));
  }, [bankById, inPeriod]);
  const bars = [...byLesson].sort((a, b) => b.acc - a.acc || b.n - a.n).slice(0, 10);
  // Zayıf konular: en az 3 çözüm, doğruluk %60 altı, en zayıf 3
  const weak = byLesson.filter((l) => l.n >= 3 && l.acc < 60).sort((a, b) => a.acc - b.acc).slice(0, 3);

  const favorites = useMemo(() => [...getFavorites()], []);
  const favCards = useMemo(() => getFavoriteCards(), []);
  const notes = useMemo(() => getNotes(), []);
  const review = useMemo(() => [...getReview()], []);
  const tests = useMemo(() => getStatsTests(), []);
  const cardNotes = useMemo(readCardNotes, []);
  const activity = useMemo(() => getActivity().slice(-40).reverse(), []);
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
  const hasPoints = (contrib.me?.totalPoints || 0) > 0;

  const savedTabs = [
    { id: 'fav' as const, label: 'Favori sorular', n: favorites.length, rows: favorites.slice(0, 5).map((id) => ({ t: bankById.get(id)?.stem || id, m: [bankById.get(id)?.discipline, bankById.get(id)?.year].filter(Boolean).join(' · ') || 'Soru' })) },
    { id: 'kart' as const, label: 'Beğenilen kartlar', n: favCards.length, rows: favCards.slice(0, 5).map((c) => ({ t: c.front, m: c.group || 'Kart' })) },
    { id: 'not' as const, label: 'Notların', n: notes.length + cardNotes, rows: notes.slice(0, 5).map((n) => ({ t: n.title || 'Başlıksız not', m: new Date(n.updatedAt).toLocaleDateString('tr-TR') })) },
    { id: 'tekrar' as const, label: 'Tekrar listesi', n: review.length, rows: review.slice(0, 5).map((id) => ({ t: bankById.get(id)?.stem || id, m: bankById.get(id)?.discipline || 'Soru' })) },
  ];
  const curTab = savedTabs.find((s) => s.id === tab)!;

  // KPI farkları: 7/30 gün → bir önceki eşit dönem; Kurul → son 7 gün
  const prevLabel = period === 'hafta' ? 'önceki 7 güne göre' : 'önceki 30 güne göre';
  const solvedDelta = period === 'kurul'
    ? { t: kurulWeek ? `+${nf.format(kurulWeek)} bu hafta` : 'bu hafta çözüm yok', dir: kurulWeek ? 'up' : '' }
    : { t: `${signed(inPeriod.length - prevPeriod.length)} ${prevLabel}`, dir: inPeriod.length > prevPeriod.length ? 'up' : inPeriod.length < prevPeriod.length ? 'down' : '' };
  const accDelta = prevAcc === null || !inPeriod.length
    ? { t: inPeriod.length ? `${nf.format(correct)} doğru · ${nf.format(inPeriod.length - correct)} yanlış` : 'bu dönemde çözüm yok', dir: '' }
    : { t: `${signed(accuracy - prevAcc)} puan`, dir: accuracy > prevAcc ? 'up' : accuracy < prevAcc ? 'down' : '' };
  const secDelta = period === 'kurul'
    ? { t: 'tüm zamanlar', dir: '' }
    : { t: periodSec === prevSec ? 'önceki dönemle aynı' : `${periodSec > prevSec ? '+' : '−'}${fmtDur(Math.abs(periodSec - prevSec))}`, dir: periodSec > prevSec ? 'up' : periodSec < prevSec ? 'down' : '' };

  const kpis = [
    { l: 'Çözülen soru', v: nf.format(inPeriod.length), d: solvedDelta },
    { l: 'Doğruluk', v: inPeriod.length ? `%${accuracy}` : '—', d: accDelta },
    { l: 'Çalışma süresi', v: fmtDur(periodSec), d: secDelta },
    { l: 'Seri', v: `${streak} gün`, d: { t: streak ? 'arka arkaya çalışılan' : 'bugün çalışınca başlar', dir: '' } },
  ];

  const lessonsLoading = !bankReady && inPeriod.length > 0;
  const showBars = lessonsLoading || bars.length > 0;
  const showSide = heatActive || weak.length > 0;

  const { v15 } = useAppearance();
  return (
    <div className="stv flex flex-col min-w-0 pb-12 o12-page o12-stv">
      <header className="stv-head">
        <div className="stv-title">
          <h1>İstatistiklerim</h1>
          <p>Çözüm ve süre verisi bu cihazda tutulur.</p>
        </div>
        <div className="stv-seg" role="tablist" aria-label="Dönem">
          {([['hafta', '7 gün'], ['ay', '30 gün'], ['kurul', 'Kurul']] as const).map(([id, l]) => (
            <button
              key={id}
              type="button"
              role="tab"
              aria-selected={period === id}
              disabled={id === 'kurul' && !currentKurul}
              title={id === 'kurul' ? (currentKurul ? `${kurulLabel(currentKurul)} · en son çalıştığın kurul` : 'Kurul sorusu çözünce açılır') : undefined}
              onClick={() => setPeriod(id)}
            >{id === 'kurul' && currentKurul ? kurulLabel(currentKurul) : l}</button>
          ))}
        </div>
      </header>

      {v15 && <React.Suspense fallback={null}><CalismaGrafikleriV15 aralik={period === 'hafta' ? 7 : 30} /></React.Suspense>}

      {/* Bento pano (styles/bento.css): dört sayı kutusu, altında geniş doğruluk kartı + yanda etkinlik / zayıf konular */}
      <div className="stv-bento bento" role="group" aria-label="Özet">
        {kpis.map((k) => (
          <div key={k.l} className="stv-kpi bt-mini">
            <span className="l">{k.l}</span>
            <strong className="v">{k.v}</strong>
            <span className={`d ${k.d.dir === 'up' ? 'is-up' : k.d.dir === 'down' ? 'is-down' : ''}`}>{k.d.t}</span>
          </div>
        ))}

        {showBars && (
          <section className={`stv-card ${showSide ? 'bt-wide' : 'bt-full'} ${heatActive && weak.length > 0 ? 'bt-tall' : ''}`} aria-labelledby="stv-acc-h">
            <div className="stv-h"><h2 id="stv-acc-h">Derslere göre doğruluk</h2><span>{period === 'kurul' && currentKurul ? kurulLabel(currentKurul) : period === 'hafta' ? 'son 7 gün' : 'son 30 gün'}</span></div>
            {lessonsLoading ? (
              <div className="stv-bars" aria-busy="true">
                {Array.from({ length: 5 }, (_, i) => <div key={i} className="stv-bar"><span className="ui-skel stv-skel-t" /><span className="ui-skel stv-skel-b" /><span /></div>)}
              </div>
            ) : (
              <ul className="stv-bars">
                {bars.map((b) => (
                  <li key={b.d} className="stv-bar">
                    <span className="t" title={b.d}>{b.d}</span>
                    <span className="tr" role="img" aria-label={`%${b.acc} doğru, ${b.n} soru`}><span className={`f ${tone(b.acc)}`} style={{ width: `${Math.max(2, b.acc)}%` }} /></span>
                    <span className="v">%{b.acc}<small>{b.n}</small></span>
                  </li>
                ))}
              </ul>
            )}
          </section>
        )}

        {heatActive && (
          <section className={`stv-card ${showBars ? 'bt-side' : 'bt-half'}`} aria-labelledby="stv-heat-h">
            <div className="stv-h"><h2 id="stv-heat-h">Etkinlik</h2><span>son 12 hafta · {fmtDur(totalSec)}</span></div>
            <div className="stv-heat" role="img" aria-label="Son 12 haftada günlük etkinlik">
              {heat.map((h) => <i key={h.key} className={h.lvl ? `l${h.lvl}` : ''} title={`${new Date(h.key).toLocaleDateString('tr-TR')} · ${fmtDur(h.s)}${h.n ? ` · ${h.n} soru` : ''}`} />)}
            </div>
            <div className="stv-legend"><span>Az</span><i /><i className="l1" /><i className="l2" /><i className="l3" /><i className="l4" /><span>Çok</span></div>
            <p className="stv-note"><Clock3 aria-hidden /> Süre, sekme açıkken ve son bir dakikada etkileşim varken sayılır.</p>
          </section>
        )}
        {weak.length > 0 && (
          <section className={`stv-card ${showBars ? 'bt-side' : 'bt-half'}`} aria-labelledby="stv-weak-h">
            <div className="stv-h"><h2 id="stv-weak-h">Zayıf konular</h2><span>%60 altı</span></div>
            <div className="stv-weak">
              {weak.map((w) => (
                <button key={w.d} type="button" onClick={() => onGo('study')} title={`${w.d} · Çalış sayfasında yanlışlarını yeniden çöz`}>
                  <span className="t">{w.d}</span><span className="v">%{w.acc}</span><ChevronRight aria-hidden />
                </button>
              ))}
            </div>
          </section>
        )}
      </div>

      {!attempts.length && !heatActive && (
        <p className="stv-empty-all">Çalış sayfasında soru çözdükçe doğruluk, ders dökümü ve etkinlik burada belirir.</p>
      )}

      <h2 className="stv-sec">Ayrıntılar</h2>

      {/* Ayrıntılar bento panosu: iki grafik yarım, üç liste kartı üçte bir, etkinlik akışı tam satır */}
      <div className="st-bento bento">
        {hasPoints && (
          <section className={`st-card ${dayTotal > 0 ? 'bt-half' : 'bt-full'}`} aria-label="Puan değişimi">
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
        )}

        {dayTotal > 0 && (
          <section className={`st-card ${hasPoints ? 'bt-half' : 'bt-full'}`} aria-label="Günlük çözülen soru">
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
        )}

        <section className="st-card" aria-label="Soru durumu">
          <div className="st-h"><b>Soru durumu</b></div>
          <button type="button" className="st-li" onClick={() => onGo('study')}><span className="ic is-ok"><Check /></span>Doğru çözdüklerin<span className="n">{nf.format(attempts.length - wrongAll)}</span></button>
          <button type="button" className="st-li" onClick={() => onGo('study')}><span className="ic is-bad"><X /></span>Yanlışların<span className="n">{nf.format(wrongAll)}</span></button>
          <button type="button" className="st-li" onClick={() => onGo('study')}><span className="ic is-warn"><RotateCcw /></span>Tekrar listesi<span className="n">{review.length}</span></button>
          <button type="button" className="st-li" onClick={() => onGo('practice')}><span className="ic"><Flag /></span>Bitirdiğin testler<span className="n">{tests.length}</span></button>
          {wrongAll > 0 && <div className="st-cta"><button type="button" className="st-primary" onClick={() => onGo('study')}>{wrongAll} yanlışı yeniden çöz</button></div>}
        </section>

        <section className="st-card" aria-label="Sınav Spotları ve Sesli Soru Çözücü">
          <div className="st-h">
            <b>Spotlar & Soru Çözücü</b>
            <span className="st-sp" />
            <span className="st-mono">{fmtSureDk(spotStats.toplamSureSn)}</span>
          </div>
          <button type="button" className="st-li" onClick={() => onGo('spots')}>
            <span className="ic is-accent"><Headphones /></span>
            Sesli soru çözücü
            <span className="n">{spotStats.cozulenSoru} / {spotStats.toplamSoru} (%{spotStats.dogrulukOrani} doğruluk)</span>
          </button>
          <button type="button" className="st-li" onClick={() => onGo('spots')}>
            <span className="ic is-ok"><BookmarkCheck /></span>
            Öğrenilen spotlar
            <span className="n">{spotStats.ogrenilenSpot} / {spotStats.toplamSpot} (%{spotStats.spotOgrenmeOrani})</span>
          </button>
          {spotStats.cozulenSoru > 0 && (
            <div style={{ padding: '6px 12px', fontSize: 11.5, color: 'var(--color-text-sub)' }}>
              {spotStats.dogruIlk} ilk denemede doğru · {spotStats.dogruYardimli} yardımla · {spotStats.yanlis} çözüm dinlendi
              {spotStats.ortalamaSoruSuresiSn > 0 && ` · ~${spotStats.ortalamaSoruSuresiSn} sn/soru`}
            </div>
          )}
          <div className="st-cta">
            <button type="button" className="st-primary" onClick={() => onGo('spots')}>
              Spotlar ve soru çözücüye git
            </button>
          </div>
        </section>

        <section className="st-card" aria-label="Katkıların">
          <div className="st-h"><b>Katkıların</b><span className="st-sp" /><span className="st-mono">{weekDelta > 0 ? `+${weekDelta} bu hafta` : ''}</span></div>
          <button type="button" className="st-li" onClick={() => onGo('leaderboard')}><span className="ic is-accent"><Trophy /></span>Toplam puan{contrib.rank ? ` · ${contrib.rank}. sırada` : ''}<span className="n">{nf.format(contrib.me?.totalPoints || 0)}</span></button>
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

        {activity.length > 0 && (
          <section className="st-card bt-full" aria-label="Etkinlik akışı">
            <div className="st-h"><b>Etkinlik akışı</b><span>bu cihazda yaptığın işlemler</span></div>
            {activity.slice(0, 12).map((a, i) => (
              <div key={i} className="st-feed"><span className={`kind ${KIND[a.kind]?.cls || ''}`}>{KIND[a.kind]?.label || a.kind}</span><span className="t">{a.text}</span><span className="w">{relTime(a.at)}</span></div>
            ))}
          </section>
        )}
      </div>
    </div>
  );
};

export default StatsView;
