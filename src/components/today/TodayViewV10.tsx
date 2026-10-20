import React, { useEffect, useMemo, useState } from 'react';
import { ArrowRight, Search } from 'lucide-react';
import { type AppRoute, linkClick, navigateTo, pathFor } from '../../router';
import { NAV_ITEMS, openSearch } from '../shell/navModel';
import { dayKey, getActivity, getStudySeconds } from '../../services/activityLog';
import { getProgress } from '../../services/studyStore';
import { KAT, Zengin, okuOgrenilen, type Spot, type Veri } from '../spots/spotsShared';
import { useReviewCounts } from '../../hooks/useReviewCounts';
import { OPEN_REVIEW_FLAG } from '../../services/learnReview';
import '../../styles/today.css';
import type { TodayViewProps } from './TodayView';

/**
 * Bugün — KLASİK v10 tasarımı (Ayarlar › Tasarım: Klasik). v11 için TodayView.tsx. (/bugun): öğrencinin günlük giriş sayfası. Yalnız bu cihazdaki gerçek kayıtlardan beslenir;
 * verisi olmayan kart hiç çizilmez (uydurma sayı yok).
 *  - Kaldığın yerden: Öğren ilerlemesi (`medsoru_learn_progress_v1` + `medsoru_learn_recent_v1`), soru çözümü
 *    (studyStore.getProgress), sınav spotları "öğrendim" işaretleri (`medsoru_spot_ogrendim`).
 *  - Günün spotu: exam_spots_k1.json'dan tarihe göre sabit seçim (dinamik içe aktarım; ana pakete girmez).
 *  - Sağ sütun: bugünün hedefi (son 14 günün günlük ortalamasına göre), bu hafta (çalışma süresi), tekrar zamanı
 *    (ezber kartları deposunda vadesi gelmiş kartlar).
 * Yerleşim: kap genişliği ≥ 880 px iken ana + 320 px yan sütun; daha darda (telefon, tablet, Akış) tek sütun.
 */


// ---------------------------------------------------------------------------
// Yerel kayıt okuyucuları (hepsi korumalı: gizli pencerede boş döner)
// ---------------------------------------------------------------------------
const readJson = <T,>(key: string, fallback: T): T => {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
};

type DeckProgress = Record<string, { last?: number; seen?: number[] } | undefined>;
interface CardState { box: number; due: number; seen: number }

const QUICK: AppRoute[] = ['glossary', 'diseases', 'kazanimlar', 'notes', 'practice', 'ornek_sorular'];
const WEEK_DAYS = ['Pt', 'Sa', 'Ça', 'Pe', 'Cu', 'Ct', 'Pz'];

/** Tarihten sabit bir sayı (gün içinde aynı spot) */
const hashOf = (s: string) => {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
  return h >>> 0;
};

const relDay = (iso: string) => {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  const a = new Date(); a.setHours(0, 0, 0, 0);
  const b = new Date(d); b.setHours(0, 0, 0, 0);
  const diff = Math.round((a.getTime() - b.getTime()) / 86_400_000);
  return diff <= 0 ? 'bugün' : diff === 1 ? 'dün' : `${diff} gün önce`;
};

const fmtMin = (sec: number) => {
  const m = Math.round(sec / 60);
  return m < 60 ? `${m} dk` : `${Math.floor(m / 60)} sa ${m % 60 ? `${m % 60} dk` : ''}`.trim();
};

interface ResumeCard {
  id: string;
  kind: 'learn' | 'solve' | 'spots';
  kicker: string;
  title: string;
  sub: string;
  pct: number;
  href: string;
  go: () => void;
}

export const TodayViewV10: React.FC<TodayViewProps> = ({ committeeLabel, onGo }) => {
  const today = dayKey();
  const dateLine = useMemo(
    () => new Date().toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', weekday: 'long' }),
    [],
  );

  // --- Öğren: en son açılan ve bitmemiş deste (katalog yalnız ilerleme varsa yüklenir) ---
  const learnProgress = useMemo(() => readJson<DeckProgress>('medsoru_learn_progress_v1', {}), []);
  const learnRecent = useMemo(() => readJson<Record<string, number>>('medsoru_learn_recent_v1', {}), []);
  const hasLearn = Object.values(learnProgress).some((p) => (p?.seen?.length || 0) > 0);
  const [learnCard, setLearnCard] = useState<ResumeCard | null | undefined>(hasLearn ? undefined : null);
  useEffect(() => {
    if (!hasLearn) return;
    let off = false;
    import('../../data/deckStore')
      .then((m) => m.loadDeckCatalog().then(() => m))
      .then(({ DECK_CATALOG, deckName }) => {
        if (off) return;
        const byId = new Map(DECK_CATALOG.map((d) => [d.id, d]));
        const cands = Object.entries(learnProgress)
          .map(([id, p]) => ({ id, p, d: byId.get(id), at: learnRecent[id] || 0 }))
          .filter((x) => x.d && (x.p?.seen?.length || 0) > 0)
          .sort((a, b) => {
            const doneA = (a.p?.seen?.length || 0) >= (a.d!.slideCount || Infinity) ? 1 : 0;
            const doneB = (b.p?.seen?.length || 0) >= (b.d!.slideCount || Infinity) ? 1 : 0;
            return doneA - doneB || b.at - a.at;
          });
        const top = cands[0];
        if (!top || !top.d) { setLearnCard(null); return; }
        const total = top.d.slideCount || 0;
        const seen = Math.min(total, top.p?.seen?.length || 0);
        setLearnCard({
          id: 'learn',
          kind: 'learn',
          kicker: 'Öğren',
          title: deckName(top.d),
          sub: total ? `Adım ${Math.min(total, (top.p?.last ?? 0) + 1)} / ${total}` : `${seen} adım görüldü`,
          pct: total ? Math.round((seen / total) * 100) : 0,
          href: pathFor('learn', top.id),
          go: () => navigateTo(pathFor('learn', top.id)),
        });
      })
      .catch(() => { if (!off) setLearnCard(null); });
    return () => { off = true; };
  }, [hasLearn, learnProgress, learnRecent]);

  // --- Soru çözümü: tüm denemeler (çıkmış, çalış, test) ---
  const solveCard = useMemo<ResumeCard | null>(() => {
    const all = Object.values(getProgress());
    if (all.length === 0) return null;
    const correct = all.filter((a) => a.correct).length;
    const last = all.reduce((m, a) => (a.at > m ? a.at : m), '');
    const todayN = all.filter((a) => a.at && dayKey(new Date(a.at)) === today).length;
    const pct = Math.round((correct / all.length) * 100);
    return {
      id: 'solve',
      kind: 'solve',
      kicker: 'Soru çöz',
      title: `${all.length.toLocaleString('tr-TR')} soru çözdün`,
      sub: `%${pct} doğru${todayN ? ` · bugün ${todayN}` : last ? ` · son: ${relDay(last)}` : ''}`,
      pct,
      href: pathFor('past_exams'),
      go: () => onGo('past_exams'),
    };
  }, [today, onGo]);

  // --- Sınav spotları verisi: günün spotu + ders başına öğrenilen ---
  const [spots, setSpots] = useState<Veri | null | undefined>(undefined);
  useEffect(() => {
    let off = false;
    import('../../data/exam_spots_k1.json')
      .then((m) => { if (!off) setSpots((m.default ?? m) as unknown as Veri); })
      .catch(() => { if (!off) setSpots(null); });
    return () => { off = true; };
  }, []);
  const learned = useMemo(() => okuOgrenilen(), []);

  const spotsCard = useMemo<ResumeCard | null>(() => {
    if (!spots || learned.size === 0) return null;
    const byLesson = new Map<number, Spot[]>();
    for (const s of spots.spotlar) {
      const arr = byLesson.get(s.ders);
      if (arr) arr.push(s); else byLesson.set(s.ders, [s]);
    }
    const cands = [...byLesson].map(([no, list]) => ({
      no,
      got: list.filter((s) => learned.has(s.id)).length,
      total: list.length,
      next: list.find((s) => !learned.has(s.id)),
    })).filter((c) => c.got > 0);
    // Bitmemiş dersler önce; aralarında en çok ilerlenen
    cands.sort((a, b) => Number(!a.next) - Number(!b.next) || b.got - a.got);
    const best = cands[0];
    if (!best) return null;
    const ders = spots.dersler.find((d) => d.no === best.no);
    const target = best.next ? `${pathFor('spots')}?id=${encodeURIComponent(best.next.id)}` : pathFor('spots');
    return {
      id: 'spots',
      kind: 'spots',
      kicker: 'Spotlar',
      title: `Ders ${best.no}${ders ? ` · ${ders.baslik}` : ''}`,
      sub: `${best.got} / ${best.total} spot öğrenildi`,
      pct: Math.round((best.got / best.total) * 100),
      href: target,
      go: () => navigateTo(target),
    };
  }, [spots, learned]);

  const spotOfDay = useMemo(() => {
    if (!spots || spots.spotlar.length === 0) return null;
    const pool = spots.spotlar.filter((s) => s.onem >= 3);
    const list = pool.length ? pool : spots.spotlar;
    const s = list[hashOf(today) % list.length];
    return { s, ders: spots.dersler.find((d) => d.no === s.ders) };
  }, [spots, today]);

  // --- Etkinlik: hafta, seri, bugünün hedefi ---
  const seconds = useMemo(() => getStudySeconds(), []);
  const activity = useMemo(() => getActivity(), []);

  const week = useMemo(() => {
    const now = new Date();
    const monday = new Date(now);
    monday.setHours(0, 0, 0, 0);
    monday.setDate(now.getDate() - ((now.getDay() + 6) % 7));
    const days = WEEK_DAYS.map((label, i) => {
      const d = new Date(monday);
      d.setDate(monday.getDate() + i);
      const k = dayKey(d);
      return { label, key: k, sec: seconds[k] || 0, isToday: k === today, future: d.getTime() > now.getTime() };
    });
    const max = Math.max(...days.map((d) => d.sec), 1);
    const total = days.reduce((n, d) => n + d.sec, 0);
    // Seri: bugünden (bugün henüz boşsa dünden) geriye kesintisiz çalışılan günler
    let streak = 0;
    const c = new Date(now);
    if (!seconds[dayKey(c)]) c.setDate(c.getDate() - 1);
    while (seconds[dayKey(c)] > 0 && streak < 400) { streak++; c.setDate(c.getDate() - 1); }
    return { days, max, total, streak };
  }, [seconds, today]);
  const hasAnyStudy = Object.values(seconds).some((v) => v > 0);

  const goals = useMemo(() => {
    const solvedByDay = new Map<string, number>();
    for (const e of activity) {
      if (e.kind !== 'coz' && e.kind !== 'yanlis') continue;
      const k = dayKey(new Date(e.at));
      solvedByDay.set(k, (solvedByDay.get(k) || 0) + 1);
    }
    const prevKeys: string[] = [];
    for (let i = 1; i <= 14; i++) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      prevKeys.push(dayKey(d));
    }
    const avgOf = (vals: number[]) => {
      const act = vals.filter((v) => v > 0);
      return act.length ? act.reduce((a, b) => a + b, 0) / act.length : 0;
    };
    const rows: { id: string; label: string; value: string; pct: number }[] = [];
    const qTarget = Math.round(avgOf(prevKeys.map((k) => solvedByDay.get(k) || 0)));
    if (qTarget > 0) {
      const v = solvedByDay.get(today) || 0;
      rows.push({ id: 'q', label: 'Soru çöz', value: `${v} / ${qTarget}`, pct: Math.min(100, Math.round((v / qTarget) * 100)) });
    }
    const sTarget = avgOf(prevKeys.map((k) => seconds[k] || 0));
    if (sTarget >= 60) {
      const v = seconds[today] || 0;
      rows.push({ id: 's', label: 'Çalışma süresi', value: `${fmtMin(v)} / ${fmtMin(sTarget)}`, pct: Math.min(100, Math.round((v / sTarget) * 100)) });
    }
    return rows;
  }, [activity, seconds, today]);

  const review = useReviewCounts();
  const dueCards = useMemo(() => {
    const store = readJson<Record<string, CardState>>('medsoru_flashcards_v1', {});
    const now = Date.now();
    return Object.values(store).filter((s) => s && typeof s.due === 'number' && s.due <= now).length;
  }, []);

  const resume = [learnCard, solveCard, spotsCard].filter((c): c is ResumeCard => !!c);
  const resumeLoading = learnCard === undefined || (spots === undefined && learned.size > 0);

  return (
    <div className="td">
      <header className="td-head">
        <div className="td-head-t">
          <span className="td-date">{dateLine}{committeeLabel ? ` · ${committeeLabel}` : ''}</span>
          <h1 className="td-h ms-page-title">Bugün</h1>
        </div>
        <button type="button" className="td-search" onClick={openSearch} aria-label="Her yerde ara" aria-haspopup="dialog">
          <Search aria-hidden />
          <span className="td-search-ph">Her yerde ara: terim, soru, ders</span>
          <kbd className="td-kbd">⌘K</kbd>
        </button>
      </header>

      {/* Bento pano (styles/bento.css): geniş kutular solda, özet kutuları sağda eşleşir; telefonda öncelik sırasıyla tek sütun */}
      <div className="td-body bento is-dense">
        {(resume.length > 0 || resumeLoading) && (
          <section className="td-sec bt-wide" aria-labelledby="td-resume-h">
            <h2 id="td-resume-h" className="td-sec-h">Kaldığın yerden</h2>
            <div className="td-resume">
              {resume.map((r) => (
                <a key={r.id} href={r.href} onClick={linkClick(r.go)} className={`td-card td-res is-${r.kind}`}>
                  <span className="td-kick">{r.kicker}</span>
                  <strong className="td-res-t">{r.title}</strong>
                  <span className="td-res-sub">{r.sub}</span>
                  <span className="td-bar" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={r.pct} aria-label={`${r.kicker} ilerlemesi`}>
                    <span style={{ width: `${r.pct}%` }} />
                  </span>
                </a>
              ))}
              {resumeLoading && resume.length === 0 && (
                <>
                  <span className="td-card td-res-skel ui-skel" aria-hidden />
                  <span className="td-card td-res-skel ui-skel" aria-hidden />
                </>
              )}
            </div>
          </section>
        )}
        {goals.length > 0 && (
          <section className="td-card td-panel bt-side" aria-labelledby="td-goal-h">
            <h2 id="td-goal-h" className="td-sec-h">Bugünün hedefi</h2>
            {goals.map((g) => (
              <div key={g.id} className="td-goal">
                <div className="td-goal-row"><span>{g.label}</span><span className="td-num">{g.value}</span></div>
                <span className="td-bar is-thick" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={g.pct} aria-label={g.label}>
                  <span style={{ width: `${g.pct}%` }} />
                </span>
              </div>
            ))}
            <span className="td-note">Hedef: son 14 günde çalıştığın günlerin ortalaması</span>
          </section>
        )}
        <section className="td-sec bt-wide" aria-labelledby="td-quick-h">
          <h2 id="td-quick-h" className="td-sec-h">Hızlı erişim</h2>
          <nav className="td-tiles" aria-label="Hızlı erişim">
            {QUICK.map((id) => {
              const it = NAV_ITEMS[id];
              if (!it) return null;
              const Icon = it.icon;
              return (
                <a key={id} href={pathFor(id)} onClick={linkClick(() => onGo(id))} className="td-card td-tile" style={{ '--td-tint': it.tint } as React.CSSProperties}>
                  <span className="td-tile-ic" aria-hidden><Icon /></span>
                  <span className="td-tile-l">{it.label}</span>
                </a>
              );
            })}
          </nav>
        </section>
        {hasAnyStudy && (
          <section className="td-card td-panel bt-side" aria-labelledby="td-week-h">
            <div className="td-panel-top">
              <h2 id="td-week-h" className="td-sec-h">Bu hafta</h2>
              <span className="td-note">{week.streak > 1 ? `${week.streak} gün seri` : week.total ? fmtMin(week.total) : 'Henüz çalışma yok'}</span>
            </div>
            <div className="td-week" role="img" aria-label={`Bu haftaki çalışma süresi: ${week.days.map((d) => `${d.label} ${fmtMin(d.sec)}`).join(', ')}`}>
              {week.days.map((d) => (
                <div key={d.key} className={`td-day ${d.isToday ? 'is-today' : ''} ${d.future ? 'is-future' : ''}`} title={`${d.label}: ${fmtMin(d.sec)}`}>
                  <span className={`td-day-bar ${d.sec ? 'has' : ''}`} style={{ height: `${Math.max(4, Math.round((d.sec / week.max) * 100))}%` }} />
                  <span className="td-day-l">{d.label}</span>
                </div>
              ))}
            </div>
          </section>
        )}
        {spots === undefined ? (
          <div className="td-card td-spot-skel ui-skel bt-wide" aria-hidden />
        ) : spotOfDay ? (
          <section className="td-card td-spot bt-wide" aria-labelledby="td-spot-h">
            <div className="td-spot-top">
              <span className="td-kick is-bad">Günün spotu · {KAT[spotOfDay.s.kategori]?.kisa || 'Spot'}</span>
              {spotOfDay.ders && <span className="td-spot-src">Ders {spotOfDay.ders.no} · {spotOfDay.ders.baslik}</span>}
              <a className="td-link" href={pathFor('spots')} onClick={linkClick(() => onGo('spots'))}>Tüm spotlar</a>
            </div>
            <h2 id="td-spot-h" className="td-spot-t">
              <a href={`${pathFor('spots')}?id=${encodeURIComponent(spotOfDay.s.id)}`} onClick={linkClick(() => navigateTo(`${pathFor('spots')}?id=${encodeURIComponent(spotOfDay.s.id)}`))}>
                {spotOfDay.s.baslik}
              </a>
            </h2>
            <p className="td-spot-x"><Zengin metin={spotOfDay.s.spot} /></p>
          </section>
        ) : null}
        {review.total.due > 0 && (
          <section className="td-due bt-side" aria-labelledby="td-rev-h">
            <h2 id="td-rev-h" className="td-due-t">Hata defteri</h2>
            <span className="td-due-x">Derste yanlış yaptığın {review.total.due.toLocaleString('tr-TR')} etkileşim bugün tekrar bekliyor (~{Math.max(1, Math.round(review.total.due * 0.5))} dk).</span>
            <a
              className="ui-btn is-primary td-due-go"
              href={pathFor('learn')}
              onClick={linkClick(() => {
                try { sessionStorage.setItem(OPEN_REVIEW_FLAG, '1'); } catch { /* yok say */ }
                onGo('learn');
              })}
            >
              Tekrara başla <ArrowRight aria-hidden />
            </a>
          </section>
        )}
        {dueCards > 0 && (
          <section className="td-due bt-side" aria-labelledby="td-due-h">
            <h2 id="td-due-h" className="td-due-t">Tekrar zamanı</h2>
            <span className="td-due-x">{dueCards.toLocaleString('tr-TR')} kart bugün tekrar bekliyor.</span>
            <a className="ui-btn is-primary td-due-go" href={pathFor('flashcards')} onClick={linkClick(() => onGo('flashcards'))}>
              Başlat <ArrowRight aria-hidden />
            </a>
          </section>
        )}
      </div>
    </div>
  );
};

export default TodayViewV10;
