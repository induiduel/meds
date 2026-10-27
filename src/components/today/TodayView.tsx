import { useBasarim } from '../../services/basarimIstemci';
import { kronometreAc } from '../v15/KronometreV15';
import ProgramSimdiKarti from '../v15/ProgramSimdiKarti';
import { IlkAdimlarKarti } from '../v15/IlkAdimlarV15';
import { profilOku } from '../../services/profilKurulum';
import React, { useEffect, useMemo, useState } from 'react';
import { ArrowRight, CircleHelp, Flag, Gamepad2, Headphones, Layers, Lightbulb, RotateCcw, Search, Sparkles, Star } from 'lucide-react';
import { type AppRoute, linkClick, navigateTo, pathFor } from '../../router';
import { NAV_ITEMS, openSearch } from '../shell/navModel';
import { dayKey, getActivity, getStudySeconds } from '../../services/activityLog';
import { getProgress } from '../../services/studyStore';
import { KAT, Zengin, okuOgrenilen, type Spot, type Veri } from '../spots/spotsShared';
import { useReviewCounts } from '../../hooks/useReviewCounts';
import { gunluBag, takvimDurumu } from '../../services/kurulPencere';
import { OPEN_REVIEW_FLAG } from '../../services/learnReview';
import '../../styles/today.css';
import '../../styles/v13/today.css';
import '../../styles/v15/today.css';
import { useAppearance } from '../../utils/appearance';
import { useCdTur } from '../canliDers/useCdTur';
import { TodayViewV10 } from './TodayViewV10';

/**
 * Bugün (v10, /bugun): öğrencinin günlük giriş sayfası. Yalnız bu cihazdaki gerçek kayıtlardan beslenir;
 * verisi olmayan kart hiç çizilmez (uydurma sayı yok).
 *  - Kaldığın yerden: Öğren ilerlemesi (`medsoru_learn_progress_v1` + `medsoru_learn_recent_v1`), soru çözümü
 *    (studyStore.getProgress), sınav spotları "öğrendim" işaretleri (`medsoru_spot_ogrendim`).
 *  - Günün spotu: exam_spots_k1.json'dan tarihe göre sabit seçim (dinamik içe aktarım; ana pakete girmez).
 *  - Sağ sütun: bugünün hedefi (son 14 günün günlük ortalamasına göre), bu hafta (çalışma süresi), tekrar zamanı
 *    (ezber kartları deposunda vadesi gelmiş kartlar).
 * Yerleşim: kap genişliği ≥ 880 px iken ana + 320 px yan sütun; daha darda (telefon, tablet, Akış) tek sütun.
 */

export interface TodayViewProps {
  /** Seçili kurulun kısa adı (ör. "Kurul 1"); tarih satırında görünür */
  committeeLabel?: string;
  onGo: (route: AppRoute) => void;
}

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

const QUICK: AppRoute[] = ['kmb_asistan', 'glossary', 'diseases', 'kazanimlar', 'summaries', 'practice', 'ornek_sorular'];
/** Yeni öğrenciye (henüz çalışma/tekrar/hedef yokken) yan sütunda önerilen başlangıç sayfaları */
const START: AppRoute[] = ['soru_cozucu', 'canli_ders', 'son_prova', 'past_exams'];
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

/** Tasarım seçimi: v11 Sade (bu dosya) ya da Klasik v10 (TodayViewV10.tsx, dokunulmadan korunur) */
export const TodayView: React.FC<TodayViewProps> = (props) => {
  const { design, v13, v15 } = useAppearance();
  return design === 'v10' ? (
    <TodayViewV10 {...props} />
  ) : (
    <TodayViewV11 {...props} v12={design === 'v12'} v13={design === 'v12' && !!v13 && !v15} v15={design === 'v12' && !!v15} />
  );
};

/** v11 ve v12 aynı verileri kullanır; v12 yalnız düzeni değiştirir (iki sütun, tek birincil blok, satır listeleri). */
const TodayViewV11: React.FC<TodayViewProps & { v12?: boolean; v13?: boolean; v15?: boolean }> = ({ committeeLabel, onGo, v12, v13, v15 }) => {
  const basarim = useBasarim();
  // H05: Bugün koç turu — v15'te ilk girişte bir kez (görüldü bilgisi cihazda, canliDersTurDurum)
  const bugunTur = useCdTur('bugun', !!v15, () => !!document.querySelector('.t15-ring'));
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
    // Profilde seçilen günlük hedef (kayıt adımları) varsa o; yoksa son 14 günün ortalaması
    const hedef = profilOku().hedef;
    const qTarget = hedef?.soru || Math.round(avgOf(prevKeys.map((k) => solvedByDay.get(k) || 0)));
    if (qTarget > 0) {
      const v = solvedByDay.get(today) || 0;
      rows.push({ id: 'q', label: 'Soru çöz', value: `${v} / ${qTarget}`, pct: Math.min(100, Math.round((v / qTarget) * 100)) });
    }
    const sTarget = hedef ? hedef.dk * 60 : avgOf(prevKeys.map((k) => seconds[k] || 0));
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

  const primary = resume[0];
  const reviewDue = review.total.due;
  const totalDue = reviewDue + dueCards;

  if (v15) {
    const goReview = () => {
      try { sessionStorage.setItem(OPEN_REVIEW_FLAG, '1'); } catch { /* yok say */ }
      onGo('learn');
    };
    // Halka: bugünkü hedefler (son 14 günün ortalamasına göre); hedef yoksa soru doğruluğu; veri yoksa boş
    const ring = goals.length
      ? { pct: Math.round(goals.reduce((n, g) => n + g.pct, 0) / goals.length), label: 'günlük hedef' }
      : solveCard
        ? { pct: solveCard.pct, label: 'doğru oranı' }
        : null;
    const planLine = goals.length
      ? goals.map((g) => `${g.label} ${g.value}`).join(' · ')
      : primary
        ? `${primary.kicker} · ${primary.sub}`
        : 'Bir derse başla; hedeflerin çalıştıkça burada oluşur.';
    type Row = { id: string; tone: string; icon: React.ElementType; title: string; sub: string; tag: string; href: string; go: () => void };
    const KIND: Record<ResumeCard['kind'], { tone: string; icon: React.ElementType; tag: string }> = {
      learn: { tone: 'is-c', icon: Layers, tag: 'Çalış' },
      solve: { tone: 'is-ok', icon: CircleHelp, tag: 'Çöz' },
      spots: { tone: 'is-w', icon: Star, tag: 'Oku' },
    };
    const rows: Row[] = [];
    // Sınav sonrası 7 gün: hatırlanan soruları ekleme ve olası sorular çağrısı (eski kurul şeridinin yerine)
    const pencere = takvimDurumu().pencere;
    if (pencere) {
      const ne = pencere.gecenGun === 0 ? 'sınavı bugün' : pencere.gecenGun === 1 ? 'sınavı dündü' : `sınavı ${pencere.gecenGun} gün önceydi`;
      const href = gunluBag(`/olasi-sorular?kurul=${pencere.kurul.kurul}`);
      rows.push({
        id: 'olasi', tone: 'is-ai', icon: Sparkles, tag: 'Olası',
        title: `Kurul ${pencere.kurul.kurul} ${ne}`,
        sub: 'Hatırladığın soruları ekle; olası sorular her gece bunlardan kurulur',
        href, go: () => navigateTo(href),
      });
    }
    rows.push(...resume.map((r) => ({ id: r.id, ...KIND[r.kind], title: r.title, sub: `${r.kicker} · ${r.sub}`, href: r.href, go: r.go })));
    if (totalDue > 0) {
      rows.push({
        id: 'due', tone: 'is-b', icon: RotateCcw, tag: 'Tekrar',
        title: `${totalDue} tekrar zamanı geldi`,
        sub: [reviewDue ? `${reviewDue} hata defteri` : '', dueCards ? `${dueCards} ezber kartı` : ''].filter(Boolean).join(' · '),
        href: reviewDue ? pathFor('learn') : pathFor('flashcards'),
        go: reviewDue ? goReview : () => onGo('flashcards'),
      });
    }
    const spotHref = spotOfDay ? `${pathFor('spots')}?id=${encodeURIComponent(spotOfDay.s.id)}` : '';
    if (spotOfDay) {
      rows.push({
        id: 'spot', tone: 'is-w', icon: Lightbulb, tag: 'Oku',
        title: 'Günün spotu',
        sub: spotOfDay.ders ? `Ders ${spotOfDay.ders.no} · ${spotOfDay.ders.baslik}` : 'Sınav spotu',
        href: spotHref, go: () => navigateTo(spotHref),
      });
    }
    const hucreBasamak = (() => { const k = basarim.durum?.kilit || {}; return basarim.tanim.kilitler.filter((x) => x.tur === 'hucre' && k[x.id]).length; })();
    const kronoYazi = (() => {
      try {
        const d = JSON.parse(localStorage.getItem('medsoru_v15_kronometre') || '{}');
        const sn = Math.floor(((d.birikmis || 0) + (d.calisiyor && d.bas ? Date.now() - d.bas : 0)) / 1000);
        return sn ? `${Math.floor(sn / 60)}:${String(sn % 60).padStart(2, '0')}` : 'Başlat';
      } catch { return 'Başlat'; }
    })();
    const quick: { id: AppRoute; label: string; tone: string; icon: React.ElementType }[] = [
      { id: 'canli_ders', label: 'Dinle', tone: '', icon: Headphones },
      { id: 'soru_cozucu', label: 'Çöz', tone: 'is-ok', icon: CircleHelp },
      { id: 'oyunlar', label: 'Oyna', tone: 'is-w', icon: Gamepad2 },
      { id: 'hub_kamplar', label: 'Kamp', tone: 'is-ai', icon: Flag },
    ];
    const R = 44;
    const C = 2 * Math.PI * R;
    return (
      <div className="t15">
        {bugunTur.tur}
        <div className="t15-in">
          <h1 className="sr-only">Bugün</h1>
          <div className="t15-main">
            <section className="t15-hero v15-card" aria-label="Bugünün planı">
              <div className="t15-ring" role="img" aria-label={ring ? `%${ring.pct} ${ring.label}` : 'Henüz veri yok'}>
                <svg viewBox="0 0 100 100" aria-hidden="true">
                  <circle cx="50" cy="50" r={R} className="t15-ring-bg" />
                  {ring && <circle cx="50" cy="50" r={R} className="t15-ring-fg" strokeDasharray={`${(C * ring.pct) / 100} ${C}`} />}
                </svg>
                <span className="t15-ring-v">
                  <b>{ring ? `%${ring.pct}` : '—'}</b>
                  <span>{ring ? ring.label : 'veri yok'}</span>
                </span>
              </div>
              <div className="t15-plan">
                <h2 className="v15-h2">Bugünün planı</h2>
                <p className="t15-plan-l">{planLine}</p>
                {goals[0] && (
                  <span className="v15-bar" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={goals[0].pct} aria-label={goals[0].label}>
                    <span style={{ width: `${goals[0].pct}%` }} />
                  </span>
                )}
                {primary ? (
                  <a className="v15-btn t15-cta" href={primary.href} onClick={linkClick(primary.go)}>Kaldığın yerden sürdür</a>
                ) : resumeLoading ? (
                  <span className="v15-skel t15-cta-skel" aria-hidden />
                ) : (
                  <a className="v15-btn t15-cta" href={pathFor('hub_dersler')} onClick={linkClick(() => onGo('hub_dersler'))}>Derslere başla</a>
                )}
              </div>
            </section>
            {/* tasarım AA07: ders programı şimdi/sonra kartı · AB11: ilk adımlar (kapatılabilir) */}
            <ProgramSimdiKarti />
            <IlkAdimlarKarti />

            <section className="t15-flow" aria-labelledby="t15-flow-h">
              <div className="t15-sec-h">
                <h2 id="t15-flow-h" className="v15-h2">Bugünkü akış</h2>
                <a className="t15-more" href={pathFor('hub_dersler')} onClick={linkClick(() => onGo('hub_dersler'))}>Tümü</a>
              </div>
              {rows.length ? (
                <ul className="t15-rows v15-card" role="list">
                  {rows.map((r) => (
                    <li key={r.id} data-k={r.id}>
                      <a className="t15-row" href={r.href} onClick={linkClick(r.go)}>
                        <span className={`v15-tile ${r.tone}`}><r.icon aria-hidden /></span>
                        <span className="t15-row-t">
                          <b>{r.title}</b>
                          <span>{r.sub}</span>
                        </span>
                        <span className={`v15-tag ${r.tone}`}>{r.tag}</span>
                      </a>
                    </li>
                  ))}
                </ul>
              ) : resumeLoading ? (
                <span className="v15-skel t15-rows-skel" aria-hidden />
              ) : (
                <p className="t15-empty v15-card">Henüz bir şey başlatmadın. Aşağıdan bir yol seç; kaldığın yer burada görünür.</p>
              )}
            </section>
          </div>

          <aside className="t15-side" aria-label="Kısayollar ve özet">
            <nav className="t15-quick" aria-label="Hızlı başla">
              {quick.map((q) => (
                <a key={q.id} className="t15-q" href={pathFor(q.id)} onClick={linkClick(() => onGo(q.id))}>
                  <span className={`v15-tile ${q.tone}`}><q.icon aria-hidden /></span>
                  <span>{q.label}</span>
                </a>
              ))}
            </nav>
            {/* tasarım A02 durum şeridi: seri · Hücrem basamağı · kronometre (her biri kendi sayfasını açar) */}
            <div className="t15-strip v15-card">
              <div><span className="v15-label">Seri</span><b>{week.streak} gün</b></div>
              <a href={pathFor('hucrem')} onClick={linkClick(() => onGo('hucrem'))}><span className="v15-label">Hücre</span><b>{hucreBasamak}/28</b></a>
              <button type="button" onClick={kronometreAc}><span className="v15-label">Kronometre</span><b>{kronoYazi}</b></button>
            </div>
            {hasAnyStudy && (
              <div className="t15-week v15-card" aria-label="Bu haftanın çalışma süresi">
                <span className="v15-label">Hafta</span>
                <ol className="t15-week-bars" role="list">
                  {week.days.map((d) => (
                    <li key={d.key} className={d.isToday ? 'is-today' : d.future ? 'is-future' : ''} title={`${d.label}: ${fmtMin(d.sec)}`}>
                      <span className="t15-wb"><i style={{ height: `${Math.max(4, Math.round((d.sec / week.max) * 100))}%` }} /></span>
                      <span className="t15-wl">{d.label}</span>
                    </li>
                  ))}
                </ol>
              </div>
            )}
            {spotOfDay && (
              <a className="t15-spot v15-card" href={spotHref} onClick={linkClick(() => navigateTo(spotHref))}>
                <span className="v15-label">Günün spotu</span>
                <p className="t15-spot-x"><Zengin metin={spotOfDay.s.spot} /></p>
              </a>
            )}
          </aside>
        </div>
      </div>
    );
  }

  if (v13) {
    const goReview = () => {
      try { sessionStorage.setItem(OPEN_REVIEW_FLAG, '1'); } catch { /* yok say */ }
      onGo('learn');
    };
    const spotHref = spotOfDay ? `${pathFor('spots')}?id=${encodeURIComponent(spotOfDay.s.id)}` : '';
    let step = 0;
    const Step: React.FC<{ title: string; meta?: React.ReactNode; children: React.ReactNode; tone?: 'acc' | 'due' }> = ({ title, meta, children, tone }) => {
      step += 1;
      return (
        <li className={`t13-step ${tone ? `is-${tone}` : ''}`}>
          <span className="t13-n" aria-hidden>{step}</span>
          <div className="t13-card">
            <div className="t13-card-h"><h2 className="t13-h">{title}</h2>{meta && <span className="t13-meta">{meta}</span>}</div>
            {children}
          </div>
        </li>
      );
    };
    return (
      <div className="t13">
        <p className="t13-date">{dateLine}{committeeLabel ? ` · ${committeeLabel}` : ''}</p>
        <div className="t13-grid">
          <ol className="t13-plan" aria-label="Bugünün planı">
            <Step title="Kaldığın yer" meta={primary?.kicker} tone="acc">
              {primary ? (
                <a className="t13-resume" href={primary.href} onClick={linkClick(primary.go)}>
                  <span className="t13-resume-t">{primary.title}</span>
                  <span className="t13-bar" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={primary.pct} aria-label={`${primary.kicker} ilerlemesi`}>
                    <span style={{ width: `${primary.pct}%` }} />
                  </span>
                  <span className="t13-resume-f"><span className="t13-meta">{primary.sub} · %{primary.pct}</span><span className="t13-go">Devam et <ArrowRight aria-hidden /></span></span>
                </a>
              ) : resumeLoading ? (
                <span className="t13-skel ui-skel" aria-hidden />
              ) : (
                <div className="t13-empty">
                  <span>Henüz bir derse başlamadın. Bir ders aç; kaldığın yer burada görünür.</span>
                  <a className="t13-go is-solid" href={pathFor('learn')} onClick={linkClick(() => onGo('learn'))}>Derslere git <ArrowRight aria-hidden /></a>
                </div>
              )}
              {resume.length > 1 && (
                <ul className="t13-rows" role="list">
                  {resume.slice(1).map((r) => (
                    <li key={r.id}>
                      <a href={r.href} onClick={linkClick(r.go)} className="t13-row">
                        <span className="t13-row-t">{r.title}</span>
                        <span className="t13-meta">{r.kicker} · %{r.pct}</span>
                      </a>
                    </li>
                  ))}
                </ul>
              )}
            </Step>
            {totalDue > 0 && (
              <Step title="Tekrar" meta={`${totalDue.toLocaleString('tr-TR')} öge · ~${Math.max(1, Math.round(totalDue * 0.4))} dk`} tone="due">
                <ul className="t13-rows" role="list">
                  {reviewDue > 0 && (
                    <li><a className="t13-row" href={pathFor('learn')} onClick={linkClick(goReview)}><span className="t13-row-t">Hata defteri</span><span className="t13-meta">{reviewDue} öge</span></a></li>
                  )}
                  {dueCards > 0 && (
                    <li><a className="t13-row" href={pathFor('flashcards')} onClick={linkClick(() => onGo('flashcards'))}><span className="t13-row-t">Ezber kartları</span><span className="t13-meta">{dueCards} kart</span></a></li>
                  )}
                </ul>
              </Step>
            )}
            {spotOfDay && (
              <Step title="Günün spotu" meta={KAT[spotOfDay.s.kategori]?.kisa || 'Spot'}>
                <a className="t13-spot" href={spotHref} onClick={linkClick(() => navigateTo(spotHref))}>
                  <strong>{spotOfDay.s.baslik}</strong>
                  <span className="t13-spot-x"><Zengin metin={spotOfDay.s.spot} /></span>
                  {spotOfDay.ders && <span className="t13-meta">Ders {spotOfDay.ders.no} · {spotOfDay.ders.baslik}</span>}
                </a>
              </Step>
            )}
            {goals.length > 0 && (
              <Step title="Bugünün hedefi" meta="son 14 günün ortalaması">
                {goals.map((g) => (
                  <div key={g.id} className="t13-goal">
                    <span className="t13-goal-l">{g.label}</span>
                    <span className="t13-num">{g.value}</span>
                    <span className="t13-bar" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={g.pct} aria-label={g.label}><span style={{ width: `${g.pct}%` }} /></span>
                  </div>
                ))}
              </Step>
            )}
          </ol>

          <aside className="t13-side" aria-label="Kısayollar ve hafta">
            <section className="t13-box" aria-labelledby="t13-q-h">
              <h2 id="t13-q-h" className="t13-h">{hasAnyStudy ? 'Kısayollar' : 'Nereden başlamalı?'}</h2>
              <nav className="t13-chips">
                {(hasAnyStudy ? QUICK : [...START, ...QUICK.slice(0, 2)]).map((id) => {
                  const it = NAV_ITEMS[id];
                  if (!it) return null;
                  const Icon = it.icon;
                  return (
                    <a key={id} href={pathFor(id)} onClick={linkClick(() => onGo(id))} className="t13-chip" title={it.hint}>
                      <Icon aria-hidden /><span>{it.short || it.label}</span>
                    </a>
                  );
                })}
              </nav>
            </section>
            {hasAnyStudy && (
              <section className="t13-box" aria-labelledby="t13-w-h">
                <div className="t13-card-h">
                  <h2 id="t13-w-h" className="t13-h">Bu hafta</h2>
                  <span className="t13-meta">{week.streak > 1 ? `${week.streak} gün seri` : fmtMin(week.total)}</span>
                </div>
                <div className="t13-week" role="img" aria-label={`Bu haftaki çalışma süresi: ${week.days.map((d) => `${d.label} ${fmtMin(d.sec)}`).join(', ')}`}>
                  {week.days.map((d) => (
                    <div key={d.key} className={`t13-day ${d.isToday ? 'is-today' : ''} ${d.future ? 'is-future' : ''}`}>
                      <span className="t13-day-bar" style={{ height: `${Math.max(4, Math.round((d.sec / week.max) * 100))}%` }} />
                      <span className="t13-day-l">{d.label}</span>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </aside>
        </div>
      </div>
    );
  }

  if (v12) {
    const rest = resume.slice(1);
    const goReview = () => {
      try { sessionStorage.setItem(OPEN_REVIEW_FLAG, '1'); } catch { /* yok say */ }
      onGo('learn');
    };
    return (
      <div className="td td12">
        <header className="td12-head">
          <div className="td12-head-t">
            <h1 className="td12-h ms-page-title">Bugün</h1>
            <span className="td12-date">{dateLine}{committeeLabel ? ` · ${committeeLabel}` : ''}</span>
          </div>
          <button type="button" className="ui-btn td12-ic" onClick={openSearch} aria-label="Her yerde ara" aria-haspopup="dialog" title="Ara (⌘K)">
            <Search aria-hidden />
          </button>
        </header>

        <div className="td12-grid">
          <div className="td12-main">
            {primary ? (
              <a className="td12-resume" href={primary.href} onClick={linkClick(primary.go)}>
                <span className="td12-meta">Kaldığın yer · {primary.kicker}</span>
                <strong className="td12-resume-t">{primary.title}</strong>
                <span className="td12-bar" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={primary.pct} aria-label={`${primary.kicker} ilerlemesi`}>
                  <span style={{ width: `${primary.pct}%` }} />
                </span>
                <span className="td12-resume-f">
                  <span className="td12-meta">{primary.sub}</span>
                  <span className="ui-btn is-primary td12-go">Devam et <ArrowRight aria-hidden /></span>
                </span>
              </a>
            ) : resumeLoading ? (
              <span className="td12-resume-skel ui-skel" aria-hidden />
            ) : (
              <section className="td12-panel td12-empty">
                <strong>Henüz bir derse başlamadın</strong>
                <span className="td12-meta">Öğren'den bir ders aç; kaldığın yer burada görünür.</span>
                <a className="ui-btn is-primary" href={pathFor('learn')} onClick={linkClick(() => onGo('learn'))}>Öğren'e git</a>
              </section>
            )}

            <nav className="td12-links" aria-label="Kısayollar">
              {QUICK.map((id) => {
                const it = NAV_ITEMS[id];
                if (!it) return null;
                const Icon = it.icon;
                return (
                  <a key={id} href={pathFor(id)} onClick={linkClick(() => onGo(id))} className="td12-link">
                    <Icon aria-hidden /><span>{it.short || it.label}</span>
                  </a>
                );
              })}
            </nav>

            {rest.length > 0 && (
              <section className="td12-panel" aria-labelledby="td12-cont-h">
                <h2 id="td12-cont-h" className="td12-sec">Devam eden</h2>
                {rest.map((r) => (
                  <a key={r.id} href={r.href} onClick={linkClick(r.go)} className="td12-row">
                    <span className="td12-pct">%{r.pct}</span>
                    <span className="td12-row-b">
                      <span className="td12-row-t">{r.title}</span>
                      <span className="td12-meta">{r.kicker} · {r.sub}</span>
                    </span>
                    <ArrowRight className="td12-chev" aria-hidden />
                  </a>
                ))}
              </section>
            )}

            {spotOfDay && (
              <section className="td12-panel td12-spot" aria-labelledby="td12-spot-h">
                <div className="td12-spot-top">
                  <span className="td12-tag">Günün spotu · {KAT[spotOfDay.s.kategori]?.kisa || 'Spot'}</span>
                  <a className="td12-more" href={pathFor('spots')} onClick={linkClick(() => onGo('spots'))}>Tüm spotlar</a>
                </div>
                <h2 id="td12-spot-h" className="td12-spot-t">
                  <a href={`${pathFor('spots')}?id=${encodeURIComponent(spotOfDay.s.id)}`} onClick={linkClick(() => navigateTo(`${pathFor('spots')}?id=${encodeURIComponent(spotOfDay.s.id)}`))}>
                    {spotOfDay.s.baslik}
                  </a>
                </h2>
                <p className="td12-spot-x"><Zengin metin={spotOfDay.s.spot} /></p>
                {spotOfDay.ders && <span className="td12-meta">Ders {spotOfDay.ders.no} · {spotOfDay.ders.baslik}</span>}
              </section>
            )}
          </div>

          <aside className="td12-side" aria-label="Bugünün özeti">
            {totalDue === 0 && goals.length === 0 && !hasAnyStudy && (
              <section className="td12-panel" aria-labelledby="td12-start-h">
                <h2 id="td12-start-h" className="td12-sec">Nereden başlamalı?</h2>
                {START.map((id) => {
                  const it = NAV_ITEMS[id];
                  if (!it) return null;
                  const Icon = it.icon;
                  return (
                    <a key={id} href={pathFor(id)} onClick={linkClick(() => onGo(id))} className="td12-row">
                      <Icon className="td12-row-ic" aria-hidden />
                      <span className="td12-row-b"><span className="td12-row-t">{it.label}</span><span className="td12-meta">{it.hint}</span></span>
                      <ArrowRight className="td12-chev" aria-hidden />
                    </a>
                  );
                })}
              </section>
            )}
            {totalDue > 0 && (
              <section className="td12-panel" aria-labelledby="td12-due-h">
                <div className="td12-sec-row"><h2 id="td12-due-h" className="td12-sec">Bugünün tekrarı</h2><span className="td12-count">{totalDue.toLocaleString('tr-TR')}</span></div>
                {reviewDue > 0 && (
                  <a className="td12-row" href={pathFor('learn')} onClick={linkClick(goReview)}>
                    <span className="td12-row-b"><span className="td12-row-t">Hata defteri</span><span className="td12-meta">{reviewDue} öge vadesi geldi</span></span>
                    <ArrowRight className="td12-chev" aria-hidden />
                  </a>
                )}
                {dueCards > 0 && (
                  <a className="td12-row" href={pathFor('flashcards')} onClick={linkClick(() => onGo('flashcards'))}>
                    <span className="td12-row-b"><span className="td12-row-t">Kartlar</span><span className="td12-meta">{dueCards} kart</span></span>
                    <ArrowRight className="td12-chev" aria-hidden />
                  </a>
                )}
                <span className="td12-note">Tahmini {Math.max(1, Math.round(totalDue * 0.4))} dakika. Hatalar önce gelir.</span>
              </section>
            )}
            {goals.length > 0 && (
              <section className="td12-panel" aria-labelledby="td12-goal-h">
                <h2 id="td12-goal-h" className="td12-sec">Bugünün hedefi</h2>
                {goals.map((g) => (
                  <div key={g.id} className="td12-goal">
                    <div className="td12-goal-row"><span>{g.label}</span><span className="td12-num">{g.value}</span></div>
                    <span className="td12-bar" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={g.pct} aria-label={g.label}>
                      <span style={{ width: `${g.pct}%` }} />
                    </span>
                  </div>
                ))}
                <span className="td12-note">Son 14 günde çalıştığın günlerin ortalaması</span>
              </section>
            )}
            {hasAnyStudy && (
              <section className="td12-panel" aria-labelledby="td12-week-h">
                <div className="td12-sec-row">
                  <h2 id="td12-week-h" className="td12-sec">Bu hafta</h2>
                  <span className="td12-meta">{week.streak > 1 ? `${week.streak} gün seri` : week.total ? fmtMin(week.total) : 'Henüz çalışma yok'}</span>
                </div>
                <div className="td12-week" role="img" aria-label={`Bu haftaki çalışma süresi: ${week.days.map((d) => `${d.label} ${fmtMin(d.sec)}`).join(', ')}`}>
                  {week.days.map((d) => (
                    <div key={d.key} className={`td12-day ${d.isToday ? 'is-today' : ''} ${d.future ? 'is-future' : ''}`} title={`${d.label}: ${fmtMin(d.sec)}`}>
                      <span className={`td12-day-bar ${d.sec ? 'has' : ''}`} style={{ height: `${Math.max(3, Math.round((d.sec / week.max) * 100))}%` }} />
                      <span className="td12-day-l">{d.label}</span>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </aside>
        </div>
      </div>
    );
  }

  return (
    <div className="td">
      <header className="td-head">
        <div className="td-head-t">
          <span className="td-date">{dateLine}{committeeLabel ? ` · ${committeeLabel}` : ''}</span>
          <h1 className="td-h ms-page-title">Bugün</h1>
        </div>
        <div className="td-head-a">
          <button type="button" className="ui-btn td-ic" onClick={openSearch} aria-label="Her yerde ara" aria-haspopup="dialog" title="Ara (⌘K)">
            <Search aria-hidden />
          </button>
          {primary && (
            <a className="ui-btn is-primary td-cta" href={primary.href} onClick={linkClick(primary.go)}>
              Kaldığın yerden <ArrowRight aria-hidden />
            </a>
          )}
        </div>
      </header>

      <div className="td-body bento is-dense">
        {(resume.length > 0 || resumeLoading) && (
          <section className="td-card td-panel bt-wide" aria-labelledby="td-resume-h">
            <h2 id="td-resume-h" className="td-sec-h">Devam et</h2>
            <div className="td-rows">
              {resume.map((r) => (
                <a key={r.id} href={r.href} onClick={linkClick(r.go)} className={`td-row is-${r.kind}`}>
                  <span className="td-row-n" aria-hidden>%{r.pct}</span>
                  <span className="td-row-b">
                    <strong className="td-row-t">{r.title}</strong>
                    <span className="td-res-sub">{r.kicker} · {r.sub}</span>
                    <span className="td-bar" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={r.pct} aria-label={`${r.kicker} ilerlemesi`}>
                      <span style={{ width: `${r.pct}%` }} />
                    </span>
                  </span>
                  <ArrowRight className="td-row-go" aria-hidden />
                </a>
              ))}
              {resumeLoading && resume.length === 0 && (
                <>
                  <span className="td-row-skel ui-skel" aria-hidden />
                  <span className="td-row-skel ui-skel" aria-hidden />
                </>
              )}
            </div>
          </section>
        )}
        {totalDue > 0 && (
          <section className="td-card td-panel bt-side" aria-labelledby="td-due-h">
            <h2 id="td-due-h" className="td-sec-h">Bugünün tekrarı</h2>
            <div className="td-big"><b>{totalDue.toLocaleString('tr-TR')}</b><span>{dueCards > 0 && reviewDue > 0 ? `${dueCards} kart · ${reviewDue} hata` : dueCards > 0 ? 'kart' : 'hata'}</span></div>
            <span className="td-note">Tahmini {Math.max(1, Math.round(totalDue * 0.4))} dakika. Hatalar önce gelir.</span>
            <div className="td-due-acts">
              {reviewDue > 0 && (
                <a className="ui-btn is-primary" href={pathFor('learn')} onClick={linkClick(() => {
                  try { sessionStorage.setItem(OPEN_REVIEW_FLAG, '1'); } catch { /* yok say */ }
                  onGo('learn');
                })}>Hataları tekrar et</a>
              )}
              {dueCards > 0 && (
                <a className={`ui-btn ${reviewDue > 0 ? '' : 'is-primary'}`} href={pathFor('flashcards')} onClick={linkClick(() => onGo('flashcards'))}>Kartlar</a>
              )}
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
            <span className="td-note">Son 14 günde çalıştığın günlerin ortalaması</span>
          </section>
        )}
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
        <section className="td-card td-panel bt-wide" aria-labelledby="td-quick-h">
          <h2 id="td-quick-h" className="td-sec-h">Kısayollar</h2>
          <nav className="td-tiles" aria-label="Kısayollar">
            {QUICK.map((id) => {
              const it = NAV_ITEMS[id];
              if (!it) return null;
              const Icon = it.icon;
              return (
                <a key={id} href={pathFor(id)} onClick={linkClick(() => onGo(id))} className="td-tile" style={{ '--td-tint': it.tint } as React.CSSProperties}>
                  <span className="td-tile-ic" aria-hidden><Icon /></span>
                  <span className="td-tile-l">{it.short || it.label}</span>
                </a>
              );
            })}
          </nav>
        </section>
      </div>
    </div>
  );
};

export default TodayView;
