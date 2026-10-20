import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  AlertCircle,
  BookOpen,
  Camera,
  Check,
  CheckCircle2,
  ChevronRight,
  Compass,
  Database,
  Download,
  FileText,
  Lock,
  LogIn,
  LogOut,
  MessageSquare,
  Palette as PaletteIcon,
  Pencil,
  ShieldCheck,
  Smartphone,
  ThumbsUp,
  Trash2,
  UserRound,
  X,
} from 'lucide-react';
import { AppUser, updateUserProfileData, setOrUpdateAccountPassword, sendPasswordReset } from '../../services/auth';
import { pwaService } from '../../services/pwaService';
import { QuestionItem } from '../../types';
import { validateNamePolicy } from '../../utils/namePolicy';
import {
  DENSITY_LABELS,
  DESIGN_CHOICES,
  designChoiceOf,
  type DesignChoice,
  FILTER_MODE_LABELS,
  LAYOUT_LABELS,
  MODE_LABELS,
  PALETTE_INFO,
  TEXT_SIZE_LABELS,
  TEXT_SIZE_ORDER,
  TEXT_SIZE_PX,
  type Density,
  type DesignVersion,
  type FilterMode,
  type LayoutMode,
  type MotionPref,
  type ReadingFont,
  type TextSize,
  type ThemeMode,
  useAppearance,
  QCARD_MODE_LABELS,
  type QCardMode,
  type QCardPrefs,
} from '../../utils/appearance';
import { findPalette, palettesFor } from '../../utils/palettes';
import { autoRevealEnabled, setAutoRevealEnabled } from '../../utils/autoReveal';
import {
  buildBank,
  getFavoriteCards,
  getFavorites,
  getNotes,
  loadArchiveBank,
  setFavorite,
  toggleFavoriteCard,
  type FavoriteCard,
  type StudyQuestion,
} from '../../services/studyStore';
import { dayKey, getActivity, getStudySeconds } from '../../services/activityLog';
import { collectLocalUserData } from '../../services/userDataSyncService';
import { linkClick, navigateTo, pathFor } from '../../router';
import { initialsOf } from '../shell/navModel';
import { AvatarCropper } from '../ui/AvatarCropper';
import { toast } from '../ui/Toast';
import { TextSizeSlider } from '../settings/TextSizeSlider';
import { NotesSyncRow } from '../settings/NotesSyncRow';
import { UserDataSyncRow } from '../settings/UserDataSyncRow';
import { ArkaPlanRow } from '../settings/ArkaPlanRow';
import { WhatsAppDailyDigestRow } from '../settings/WhatsAppDailyDigestRow';
import { ProgressResetRow } from '../settings/ProgressResetRow';
import { getStatsAttempts } from '../../services/progressReset';
import { startWelcomeTour } from '../onboarding/tourState';
import { onLearnTour } from '../onboarding/learnTourState';
import '../../styles/v12/profile.css';

/**
 * v12 "Net" · Profil ve ayarlar (/ayarlar, /profil) — canvas panoları Profile.dc.html + Settings.dc.html.
 * Üstte kimlik (avatar + düzenle), altında sekmeler: Genel bakış · Katkılarım · Kaydettiklerim · Hesap · Veriler ve gizlilik;
 * sekme şeridinin sağındaki "Görünüm ve tasarım" bağlantısı görünüm ayarlarını (Settings panosu) açar.
 * Tüm veriler gerçek kaynaklardan: studyStore (ilerleme, favoriler, notlar), activityLog, havuz soruları (props),
 * Öğren ilerlemesi (medsoru_learn_progress_v1 + deckStore). Kaynağı olmayan canvas parçaları (cihaz listesi, görünürlük
 * anahtarları, hesabı sil, kart serisi) eklenmedi.
 */

export interface ProfileV12Props {
  currentUser: AppUser | null;
  isAdmin: boolean;
  questions: QuestionItem[];
  onUpdateUser: (u: AppUser) => void;
  onOpenAuth: () => void;
  onLogout: () => void;
  onOpenAdmin: () => void;
  onOpenOffline: () => void;
}

type Tab = 'genel' | 'katki' | 'kayit' | 'hesap' | 'veri';
type View = Tab | 'gorunum';

const TABS: { id: Tab; label: string }[] = [
  { id: 'genel', label: 'Genel bakış' },
  { id: 'katki', label: 'Katkılarım' },
  { id: 'kayit', label: 'Kaydettiklerim' },
  { id: 'hesap', label: 'Hesap' },
  { id: 'veri', label: 'Veriler ve gizlilik' },
];

const nf = new Intl.NumberFormat('tr-TR');

const fmtDur = (sec: number) => {
  const h = Math.floor(sec / 3600);
  const m = Math.round((sec % 3600) / 60);
  return h ? `${h} sa ${m} dk` : `${m} dk`;
};

/** Etkinlik saati: bugün → 14:32, dün → Dün 22:10, daha eski → 3 Eki */
const fmtWhen = (iso: string) => {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  const hm = d.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
  const now = new Date();
  if (dayKey(d) === dayKey(now)) return hm;
  const y = new Date(now);
  y.setDate(y.getDate() - 1);
  if (dayKey(d) === dayKey(y)) return `Dün ${hm}`;
  return d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
};

/** Göreli gün: bugün / dün / 3 gün önce / 12 Eyl */
const fmtRel = (ms: number) => {
  if (!ms) return '';
  const a = new Date();
  a.setHours(0, 0, 0, 0);
  const b = new Date(ms);
  b.setHours(0, 0, 0, 0);
  const diff = Math.round((a.getTime() - b.getTime()) / 86_400_000);
  if (diff <= 0) return 'bugün';
  if (diff === 1) return 'dün';
  if (diff < 14) return `${diff} gün önce`;
  return new Date(ms).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
};

const ts = (s?: string) => {
  const t = s ? Date.parse(s) : NaN;
  return Number.isNaN(t) ? 0 : t;
};

const readJson = <T,>(key: string, fallback: T): T => {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
};

const go = (href: string) => linkClick(() => navigateTo(href));

/* ------------------------------------------------------------------------------------------------
 * Küçük denetimler: segment (radyo grubu) ve anahtar — canvas z-seg / z-switch karşılığı
 * ---------------------------------------------------------------------------------------------- */

function Seg<T extends string>({ label, value, options, onChange }: {
  label: string;
  value: T;
  options: { value: T; label: React.ReactNode; aria?: string; style?: React.CSSProperties }[];
  onChange: (v: T) => void;
}) {
  const refs = useRef<(HTMLButtonElement | null)[]>([]);
  const onKey = (e: React.KeyboardEvent, i: number) => {
    const n = options.length;
    const next = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? (i + 1) % n : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? (i - 1 + n) % n : -1;
    if (next < 0) return;
    e.preventDefault();
    onChange(options[next].value);
    refs.current[next]?.focus();
  };
  return (
    <div className="u12-seg" role="radiogroup" aria-label={label}>
      {options.map((o, i) => {
        const on = o.value === value;
        return (
          <button
            key={o.value}
            ref={(el) => { refs.current[i] = el; }}
            type="button"
            role="radio"
            aria-checked={on}
            aria-label={o.aria}
            tabIndex={on ? 0 : -1}
            className={on ? 'is-on' : undefined}
            style={o.style}
            onClick={() => onChange(o.value)}
            onKeyDown={(e) => onKey(e, i)}
          >
            {o.label}
          </button>
        );
      })}
    </div>
  );
}

const QCARD_MODE_HINTS: Record<QCardMode, string> = {
  tam: 'Soru, şıklar ve işlemler kartta açık.',
  katlanir: 'Yalnız soru kökü ve künye; şıklar ve cevap dokununca açılır.',
  dar: 'Soru ve şıklar açık; şıklar sıkı satırlarda, genişse iki sütun.',
};
const QCARD_FIELDS: [keyof Omit<QCardPrefs, 'mode'>, string, string][] = [
  ['kurul', 'Kurul bilgisi', 'Kart başlığında kurul.'],
  ['ders', 'Ders bilgisi', 'Kart başlığında ders adı.'],
  ['yil', 'Sene bilgisi', 'Kart başlığında sınav yılı.'],
  ['aciklama', 'Açıklama', 'Açıklama düğmesi ve gövdesi; kapalıyken yalnız doğru/yanlış görünür.'],
  ['sikAciklama', 'Şık açıklaması', 'Açıklamadaki şık şık analiz.'],
];

const Toggle: React.FC<{ checked: boolean; onChange: (v: boolean) => void; labelledBy: string }> = ({ checked, onChange, labelledBy }) => (
  <button type="button" role="switch" aria-checked={checked} aria-labelledby={labelledBy} className="u12-switch" onClick={() => onChange(!checked)}>
    <span className="u12-switch-t" aria-hidden="true" />
  </button>
);

/** Ayar satırı: solda başlık + açıklama, sağda denetim (canvas .st-row) */
const SetRow: React.FC<{ id: string; title: React.ReactNode; sub?: React.ReactNode; children?: React.ReactNode; danger?: boolean }> = ({ id, title, sub, children, danger }) => (
  <div className="u12-srow">
    <div className="u12-srow-l">
      <span id={id} className={`u12-h3 ${danger ? 'is-bad' : ''}`}>{title}</span>
      {sub && <span className="u12-meta">{sub}</span>}
    </div>
    {children}
  </div>
);

/** Gezinen ayar satırı (sağda ok) */
const NavRow: React.FC<{ title: string; sub: string; onClick: () => void; icon: React.ElementType }> = ({ title, sub, onClick, icon: Icon }) => (
  <button type="button" className="u12-srow is-link" onClick={onClick}>
    <span className="u12-lead" aria-hidden="true"><Icon /></span>
    <span className="u12-srow-l">
      <span className="u12-h3">{title}</span>
      <span className="u12-meta">{sub}</span>
    </span>
    <ChevronRight className="u12-chev" aria-hidden />
  </button>
);

const Empty: React.FC<{ icon?: React.ElementType; title: string; body: string; children?: React.ReactNode }> = ({ icon: Icon, title, body, children }) => (
  <div className="u12-empty">
    {Icon && <span className="u12-lead" aria-hidden="true"><Icon /></span>}
    <h3 className="u12-h3">{title}</h3>
    <p>{body}</p>
    {children}
  </div>
);

/* ------------------------------------------------------------------------------------------------
 * Profil düzenleme (ProfileSettingsView › ProfileSection ile aynı kurallar: ad politikası, kayıt, fotoğraf)
 * ---------------------------------------------------------------------------------------------- */

function useProfileEditor(user: AppUser | null, onUpdateUser: (u: AppUser) => void) {
  const [name, setName] = useState(user?.displayName || '');
  const [num, setNum] = useState(user?.studentNumber || '');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    setName(user?.displayName || '');
    setNum(user?.studentNumber || '');
    setError(null);
  }, [user?.uid]);

  const dirty = !!user && (name.trim() !== (user.displayName || '') || num !== (user.studentNumber || ''));

  const reset = () => {
    setName(user?.displayName || '');
    setNum(user?.studentNumber || '');
    setError(null);
  };

  const save = async (patch?: { photoURL?: string | null }) => {
    if (!user) return;
    setError(null);
    if (!patch && name.trim()) {
      const check = validateNamePolicy(name.trim(), { adminEmail: user.email });
      if (!check.isValid) {
        setError(check.errorMessage || 'Geçersiz isim.');
        return;
      }
    }
    setSaving(true);
    try {
      const updated = await updateUserProfileData(user, {
        displayName: name.trim() || undefined,
        studentNumber: num || undefined,
        ...(patch || {}),
      });
      onUpdateUser(updated);
      if (patch) toast.success(patch.photoURL ? 'Fotoğraf güncellendi' : 'Fotoğraf kaldırıldı');
      else {
        setSaved(true);
        window.setTimeout(() => setSaved(false), 2400);
      }
    } catch (e: any) {
      setError(e?.message || 'Kaydedilemedi.');
    } finally {
      setSaving(false);
    }
  };

  return { name, setName, num, setNum, saving, error, saved, dirty, reset, save };
}

/* ------------------------------------------------------------------------------------------------
 * Katkılar: havuz sorularından (props) kullanıcının soruları, parçaları, şık önerileri ve yorumları
 * ---------------------------------------------------------------------------------------------- */

type ContribKind = 'soru' | 'parca' | 'sik' | 'yorum';
interface ContribRow {
  key: string;
  text: string;
  meta: string;
  likes: number;
  comments?: number;
  badge?: { t: string; tone?: 'ok' | 'warn' };
  href: string;
  at: number;
}

const qText = (q: QuestionItem) =>
  String(q.reconstruction?.stem || q.rawStem || q.fragments?.find((f) => f.type === 'stem')?.text || q.fragments?.[0]?.text || '').trim() ||
  `${q.discipline || 'Soru'} · Soru ${q.questionNumber}`;

const qMeta = (q: QuestionItem, extra?: string) =>
  [q.discipline, q.examYear, q.questionNumber ? `Soru ${q.questionNumber}` : '', extra].filter(Boolean).join(' · ');

const statusBadge = (q: QuestionItem): ContribRow['badge'] =>
  q.status === 'completed' ? { t: 'Tamamlandı', tone: 'ok' } : q.status === 'reconstructing' ? { t: 'Kuruluyor', tone: 'warn' } : q.status === 'gathering' ? { t: 'Toplanıyor' } : undefined;

function buildContrib(questions: QuestionItem[], user: AppUser): Record<ContribKind, ContribRow[]> {
  const uid = user.uid;
  const name = user.displayName || '';
  const out: Record<ContribKind, ContribRow[]> = { soru: [], parca: [], sik: [], yorum: [] };
  for (const q of questions) {
    const href = pathFor('questions', q.id);
    const mine = (q.fragments || []).filter((f) => f.authorUid === uid || (!!name && f.author === name));
    if (q.contributedByUid === uid) {
      const at = Math.max(0, ...(q.fragments || []).map((f) => ts(f.timestamp)), ts(q.reconstruction?.lastUpdated));
      out.soru.push({ key: q.id, text: qText(q), meta: qMeta(q, fmtRel(at)), likes: q.upvotes || 0, comments: q.comments?.length || 0, badge: statusBadge(q), href, at });
    }
    mine.forEach((f) => {
      const at = ts(f.timestamp);
      out.parca.push({
        key: `${q.id}:${f.id}`,
        text: f.text,
        meta: qMeta(q, fmtRel(at)),
        likes: f.upvotes || 0,
        badge: q.status === 'completed' ? { t: 'Soruya dönüştü', tone: 'ok' } : undefined,
        href,
        at,
      });
    });
    (q.options || []).forEach((o) => {
      if (!(o.suggestedByUid === uid || (!!name && o.suggestedBy === name))) return;
      out.sik.push({ key: `${q.id}:${o.key}`, text: `${o.key}) ${o.text}`, meta: qMeta(q), likes: o.upvotes || 0, href, at: 0 });
    });
    if (name) {
      (q.comments || []).forEach((c, i) => {
        if (c.author !== name) return;
        const at = ts(c.createdAt);
        out.yorum.push({ key: `${q.id}:c${c.id || i}`, text: c.text, meta: qMeta(q, fmtRel(at)), likes: 0, href, at });
      });
    }
  }
  (Object.keys(out) as ContribKind[]).forEach((k) => out[k].sort((a, b) => b.at - a.at));
  return out;
}

const CONTRIB_SEGS: { id: ContribKind; label: string; note: string; empty: string }[] = [
  { id: 'soru', label: 'Sorular', note: 'Hatırlayıp havuza eklediğin sorular.', empty: 'Havuza eklediğin bir soru henüz yok. Hatırladığın soruyu “Soru ekle” ile paylaşabilirsin.' },
  { id: 'parca', label: 'Parçalar', note: 'Sorulara girdiğin parçalar; benzerleri birleşip soruya dönüşür.', empty: 'Henüz bir soruya parça eklemedin.' },
  { id: 'sik', label: 'Şık önerileri', note: 'Havuz sorularına önerdiğin şıklar.', empty: 'Henüz şık önermedin.' },
  { id: 'yorum', label: 'Yorumlar', note: 'Havuz sorularına yazdığın yorumlar (görünen adınla eşleşir).', empty: 'Havuz sorularına yazdığın bir yorum yok.' },
];

/* ------------------------------------------------------------------------------------------------
 * Ana bileşen
 * ---------------------------------------------------------------------------------------------- */

export const ProfileV12: React.FC<ProfileV12Props> = ({ currentUser, isAdmin, questions, onUpdateUser, onOpenAuth, onLogout, onOpenAdmin, onOpenOffline }) => {
  const [view, setView] = useState<View>(() => {
    const h = typeof window !== 'undefined' ? window.location.hash.replace('#', '') : '';
    return h === 'gorunum' ? 'gorunum' : h === 'hesap' ? 'hesap' : 'genel';
  });
  const ed = useProfileEditor(currentUser, onUpdateUser);
  const [cropFile, setCropFile] = useState<File | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);
  const nameRef = useRef<HTMLInputElement>(null);
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([]);
  const [focusName, setFocusName] = useState(false);

  useEffect(() => {
    if (focusName && view === 'hesap') {
      nameRef.current?.focus();
      setFocusName(false);
    }
  }, [focusName, view]);

  const pickPhoto = () => fileRef.current?.click();
  const photo = currentUser?.photoURL || '';
  const shownName = currentUser ? currentUser.displayName || currentUser.email?.split('@')[0] || 'Öğrenci' : 'Misafir';

  const onTabKey = (e: React.KeyboardEvent, i: number) => {
    const n = TABS.length;
    const next = e.key === 'ArrowRight' ? (i + 1) % n : e.key === 'ArrowLeft' ? (i - 1 + n) % n : e.key === 'Home' ? 0 : e.key === 'End' ? n - 1 : -1;
    if (next < 0) return;
    e.preventDefault();
    setView(TABS[next].id);
    tabRefs.current[next]?.focus();
  };

  return (
    <div className="ui-page is-wide u12-pf">
      <div className="u12-box">
        <section className="u12-head" aria-label="Profil özeti">
          <div className="u12-av-wrap">
            <span className="u12-av" aria-hidden="true">
              {photo ? <img src={photo} alt="" /> : currentUser ? initialsOf(currentUser) : <UserRound />}
            </span>
            {currentUser && (
              <button type="button" className="u12-av-edit" aria-label="Profil fotoğrafını değiştir" onClick={pickPhoto}>
                <Pencil aria-hidden />
              </button>
            )}
          </div>
          <div className="u12-grow">
            <h1 className="u12-name">{shownName}</h1>
            <div className="u12-sub u12-meta">
              <span>{currentUser ? currentUser.email : 'Giriş yapmadın; görünüm ayarları ve bu cihazdaki ilerleme yine çalışır.'}</span>
              {currentUser?.studentNumber && <span className="u12-num">{currentUser.studentNumber}</span>}
            </div>
          </div>
          {currentUser ? (
            <button type="button" className="u12-btn is-sm" onClick={() => { setView('hesap'); setFocusName(true); }}>
              <Pencil aria-hidden />
              Profili düzenle
            </button>
          ) : (
            <button type="button" className="u12-btn is-sm is-pri" onClick={onOpenAuth}>
              <LogIn aria-hidden />
              Giriş yap
            </button>
          )}
        </section>

        <div className="u12-tabs">
          <div className="u12-tablist" role="tablist" aria-label="Profil bölümleri">
            {TABS.map((t, i) => {
              const on = view === t.id;
              return (
                <button
                  key={t.id}
                  ref={(el) => { tabRefs.current[i] = el; }}
                  id={`u12-tab-${t.id}`}
                  type="button"
                  role="tab"
                  aria-selected={on}
                  aria-controls={`u12-panel-${t.id}`}
                  tabIndex={on || (view === 'gorunum' && i === 0) ? 0 : -1}
                  className={on ? 'is-on' : undefined}
                  onClick={() => setView(t.id)}
                  onKeyDown={(e) => onTabKey(e, i)}
                >
                  {t.label}
                </button>
              );
            })}
          </div>
          <button type="button" className={`u12-applink ${view === 'gorunum' ? 'is-on' : ''}`} aria-current={view === 'gorunum' ? 'true' : undefined} onClick={() => setView('gorunum')}>
            Görünüm ve tasarım
            <ChevronRight aria-hidden />
          </button>
        </div>

        {view === 'genel' && <OverviewPanel currentUser={currentUser} questions={questions} />}
        {view === 'katki' && <ContribPanel currentUser={currentUser} questions={questions} onOpenAuth={onOpenAuth} />}
        {view === 'kayit' && <SavedPanel questions={questions} />}
        {view === 'hesap' && (
          <AccountPanel
            currentUser={currentUser}
            isAdmin={isAdmin}
            ed={ed}
            nameRef={nameRef}
            photo={photo}
            onPickPhoto={pickPhoto}
            onRemovePhoto={() => ed.save({ photoURL: '' })}
            onOpenAuth={onOpenAuth}
            onLogout={onLogout}
            onOpenAdmin={onOpenAdmin}
            onAppearance={() => setView('gorunum')}
          />
        )}
        {view === 'veri' && <DataPanel onOpenOffline={onOpenOffline} />}
        {view === 'gorunum' && <AppearancePanel />}
      </div>

      <input
        ref={fileRef}
        type="file"
        accept="image/*"
        hidden
        onChange={(e) => {
          const f = e.target.files?.[0];
          e.target.value = '';
          if (!f) return;
          if (f.size > 15 * 1024 * 1024) {
            toast.error('Dosya çok büyük', 'En fazla 15 MB bir görsel seç.');
            return;
          }
          setCropFile(f);
        }}
      />
      {cropFile && (
        <AvatarCropper
          file={cropFile}
          onCancel={() => setCropFile(null)}
          onDone={(url) => {
            setCropFile(null);
            ed.save({ photoURL: url });
          }}
        />
      )}
    </div>
  );
};

/* ------------------------------------------------------------------------------------------------
 * Genel bakış
 * ---------------------------------------------------------------------------------------------- */

type DeckProgress = Record<string, { last?: number; seen?: number[] } | undefined>;
interface LessonRow { id: string; title: string; seen: number; total: number }

const OverviewPanel: React.FC<{ currentUser: AppUser | null; questions: QuestionItem[] }> = ({ currentUser, questions }) => {
  const stats = useMemo(() => {
    const prog = getStatsAttempts().map(([, a]) => a);
    const ok = prog.filter((a) => a.correct).length;
    const secs = getStudySeconds();
    const total = Object.values(secs).reduce((a, s) => a + s, 0);
    let week = 0;
    for (let i = 0; i < 7; i++) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      week += secs[dayKey(d)] || 0;
    }
    const todayN = prog.filter((a) => a.at && dayKey(new Date(a.at)) === dayKey()).length;
    return { solved: prog.length, ok, acc: prog.length ? Math.round((ok / prog.length) * 100) : 0, total, week, todayN, notes: getNotes().length };
  }, []);

  const contributed = useMemo(() => {
    if (!currentUser) return 0;
    const n = currentUser.displayName;
    return questions.filter(
      (q) =>
        q.contributedByUid === currentUser.uid ||
        q.fragments.some((f) => f.authorUid === currentUser.uid || (n && f.author === n)) ||
        q.options.some((o) => o.suggestedByUid === currentUser.uid || (n && o.suggestedBy === n))
    ).length;
  }, [questions, currentUser]);

  const activity = useMemo(() => getActivity().slice(-6).reverse(), []);

  // Devam eden dersler: Öğren ilerlemesi (görülen adımlar) + en son açılma; katalog yalnız ilerleme varsa yüklenir
  const learnProgress = useMemo(() => readJson<DeckProgress>('medsoru_learn_progress_v1', {}), []);
  const learnRecent = useMemo(() => readJson<Record<string, number>>('medsoru_learn_recent_v1', {}), []);
  const hasLearn = Object.values(learnProgress).some((p) => (p?.seen?.length || 0) > 0);
  const [lessons, setLessons] = useState<LessonRow[] | null>(hasLearn ? null : []);
  useEffect(() => {
    if (!hasLearn) return;
    let off = false;
    import('../../data/deckStore')
      .then((m) => m.loadDeckCatalog().then(() => m))
      .then(({ DECK_CATALOG, deckName }) => {
        if (off) return;
        const byId = new Map(DECK_CATALOG.map((d) => [d.id, d]));
        const rows = Object.entries(learnProgress)
          .map(([id, p]) => ({ id, p, d: byId.get(id), at: learnRecent[id] || 0 }))
          .filter((x) => x.d && (x.p?.seen?.length || 0) > 0 && (x.p?.seen?.length || 0) < (x.d.slideCount || Infinity))
          .sort((a, b) => b.at - a.at)
          .slice(0, 4)
          .map((x) => ({ id: x.id, title: deckName(x.d!), seen: Math.min(x.d!.slideCount || 0, x.p?.seen?.length || 0), total: x.d!.slideCount || 0 }));
        setLessons(rows);
      })
      .catch(() => { if (!off) setLessons([]); });
    return () => { off = true; };
  }, [hasLearn, learnProgress, learnRecent]);

  return (
    <div role="tabpanel" id="u12-panel-genel" aria-labelledby="u12-tab-genel" className="u12-stack">
      <section className="u12-panel">
        <div className="u12-panel-h">
          <h2 className="u12-h2 u12-grow">Senin sayıların</h2>
          <a className="u12-link" href={pathFor('stats')} onClick={go(pathFor('stats'))}>İstatistiklerim</a>
        </div>
        <div className="u12-strip">
          <div className="u12-stat"><span className="u12-meta">Çözdüğün soru</span><span className="v">{nf.format(stats.solved)}</span><span className="u12-meta">{stats.todayN ? `bugün ${nf.format(stats.todayN)}` : 'bu cihazda'}</span></div>
          <div className="u12-stat"><span className="u12-meta">Doğru oranın</span><span className="v">{stats.solved ? `%${stats.acc}` : '—'}</span><span className="u12-meta">{nf.format(stats.ok)} doğru</span></div>
          <div className="u12-stat"><span className="u12-meta">Çalışma süren</span><span className="v">{fmtDur(stats.total)}</span><span className="u12-meta">son 7 gün {fmtDur(stats.week)}</span></div>
          <div className="u12-stat"><span className="u12-meta">Katkı verdiğin soru</span><span className="v">{currentUser ? nf.format(contributed) : '—'}</span><span className="u12-meta">{currentUser ? 'soru havuzunda' : 'giriş yapınca'}</span></div>
          <div className="u12-stat"><span className="u12-meta">Notların</span><span className="v">{nf.format(stats.notes)}</span><span className="u12-meta">bu cihazda</span></div>
        </div>
      </section>

      <div className="u12-cols">
        <section className="u12-panel u12-col-a">
          <div className="u12-panel-h">
            <h2 className="u12-h2 u12-grow">Son etkinlik</h2>
            {activity.length > 0 && <a className="u12-link" href={pathFor('stats')} onClick={go(pathFor('stats'))}>Tümü</a>}
          </div>
          {activity.length ? (
            <ul className="u12-list">
              {activity.map((a, i) => (
                <li key={`${a.at}-${i}`} className="u12-row">
                  <span className="u12-time">{fmtWhen(a.at)}</span>
                  <span className="u12-grow u12-clamp2">{a.text}</span>
                </li>
              ))}
            </ul>
          ) : (
            <Empty title="Henüz etkinlik yok" body="Soru çözdükçe, not aldıkça ve test bitirdikçe burada görünür." />
          )}
        </section>

        <section className="u12-panel u12-col-b">
          <div className="u12-panel-h"><h2 className="u12-h2 u12-grow">Devam eden dersler</h2></div>
          {lessons === null ? (
            <p className="u12-loading u12-meta" role="status">Dersler yükleniyor…</p>
          ) : lessons.length ? (
            <ul className="u12-list">
              {lessons.map((l) => (
                <li key={l.id}>
                  <a className="u12-row is-link" href={pathFor('learn', l.id)} onClick={go(pathFor('learn', l.id))}>
                    <span className="u12-grow u12-lesson">
                      <span className="t u12-clamp1">{l.title}</span>
                      <span className="u12-bar" aria-hidden="true"><i style={{ width: `${l.total ? Math.round((l.seen / l.total) * 100) : 0}%` }} /></span>
                      <span className="u12-meta u12-num">{l.seen} / {l.total} adım</span>
                    </span>
                    <ChevronRight className="u12-chev" aria-hidden />
                  </a>
                </li>
              ))}
            </ul>
          ) : (
            <Empty title="Yarım kalan ders yok" body="Öğren’de başladığın dersler burada kaldığın adımla görünür.">
              <a className="u12-btn is-sm" href={pathFor('learn')} onClick={go(pathFor('learn'))}><BookOpen aria-hidden />Öğren’e git</a>
            </Empty>
          )}
        </section>
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------------------------------------
 * Katkılarım
 * ---------------------------------------------------------------------------------------------- */

const PAGE = 20;

const ContribPanel: React.FC<{ currentUser: AppUser | null; questions: QuestionItem[]; onOpenAuth: () => void }> = ({ currentUser, questions, onOpenAuth }) => {
  const [seg, setSeg] = useState<ContribKind>('soru');
  const [limit, setLimit] = useState(PAGE);
  const data = useMemo(() => (currentUser ? buildContrib(questions, currentUser) : null), [questions, currentUser]);
  useEffect(() => setLimit(PAGE), [seg]);

  if (!currentUser || !data) {
    return (
      <div role="tabpanel" id="u12-panel-katki" aria-labelledby="u12-tab-katki">
        <section className="u12-panel">
          <Empty icon={UserRound} title="Katkıların için giriş yap" body="Havuza eklediğin sorular, parçalar ve şık önerilerin adınla burada toplanır.">
            <button type="button" className="u12-btn is-sm is-pri" onClick={onOpenAuth}><LogIn aria-hidden />Giriş yap</button>
          </Empty>
        </section>
      </div>
    );
  }

  const cur = CONTRIB_SEGS.find((s) => s.id === seg)!;
  const rows = data[seg];

  return (
    <div role="tabpanel" id="u12-panel-katki" aria-labelledby="u12-tab-katki" className="u12-stack is-tight">
      <div className="u12-toolbar">
        <Seg<ContribKind>
          label="Katkı türü"
          value={seg}
          onChange={setSeg}
          options={CONTRIB_SEGS.map((s) => ({ value: s.id, label: <>{s.label} <span className="u12-seg-n">{nf.format(data[s.id].length)}</span></> }))}
        />
        <span className="u12-meta u12-grow">{cur.note}</span>
      </div>

      {rows.length ? (
        <section className="u12-panel">
          <ul className="u12-list">
            {rows.slice(0, limit).map((r) => (
              <li key={r.key}>
                <a className="u12-row is-link is-top" href={r.href} onClick={go(r.href)}>
                  <span className="u12-grow u12-two">
                    <span className="t u12-clamp2">{r.text}</span>
                    <span className="u12-meta u12-clamp1">{r.meta}</span>
                  </span>
                  <span className="u12-row-end">
                    <span className="u12-counts">
                      <span aria-label={`${r.likes} beğeni`}><ThumbsUp aria-hidden /><span className="u12-num">{r.likes}</span></span>
                      {r.comments !== undefined && <span aria-label={`${r.comments} yorum`}><MessageSquare aria-hidden /><span className="u12-num">{r.comments}</span></span>}
                    </span>
                    {r.badge && <span className={`u12-badge ${r.badge.tone ? `is-${r.badge.tone}` : ''}`}>{r.badge.t}</span>}
                  </span>
                </a>
              </li>
            ))}
          </ul>
          {rows.length > limit && (
            <div className="u12-more">
              <button type="button" className="u12-btn is-sm is-ghost" onClick={() => setLimit((l) => l + PAGE)}>
                Daha fazla göster ({nf.format(rows.length - limit)})
              </button>
            </div>
          )}
        </section>
      ) : (
        <section className="u12-panel">
          <Empty icon={FileText} title={`${cur.label}: henüz kayıt yok`} body={cur.empty}>
            <a className="u12-btn is-sm" href={pathFor('questions')} onClick={go(pathFor('questions'))}>Soru havuzuna git</a>
          </Empty>
        </section>
      )}
    </div>
  );
};

/* ------------------------------------------------------------------------------------------------
 * Kaydettiklerim: favori sorular (studyStore favorites + soru bankası) ve favori kartlar
 * ---------------------------------------------------------------------------------------------- */

type Removed = { kind: 'q'; id: string } | { kind: 'c'; card: FavoriteCard };

const SavedPanel: React.FC<{ questions: QuestionItem[] }> = ({ questions }) => {
  const [favIds, setFavIds] = useState<string[]>(() => [...getFavorites()]);
  const [cards, setCards] = useState<FavoriteCard[]>(getFavoriteCards);
  const [archive, setArchive] = useState<StudyQuestion[] | null>(favIds.length ? null : []);
  const [removed, setRemoved] = useState<Removed | null>(null);
  const timer = useRef<number | undefined>(undefined);

  // Çıkmış soru arşivi yalnız kayıtlı soru varsa ve bu sekme açıkken yüklenir
  useEffect(() => {
    if (!favIds.length || archive) return;
    let off = false;
    loadArchiveBank().then((a) => { if (!off) setArchive(a); }).catch(() => { if (!off) setArchive([]); });
    return () => { off = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const byId = useMemo(() => new Map(buildBank(archive || [], questions).map((q) => [q.id, q])), [archive, questions]);
  const savedQs = favIds.map((id) => byId.get(id)).filter((q): q is StudyQuestion => !!q);
  const missing = archive ? favIds.length - savedQs.length : 0;

  useEffect(() => () => window.clearTimeout(timer.current), []);
  const announce = (r: Removed) => {
    setRemoved(r);
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => setRemoved(null), 5000);
  };

  const removeQ = (id: string) => {
    setFavIds([...setFavorite(id, false)]);
    announce({ kind: 'q', id });
  };
  const removeC = (c: FavoriteCard) => {
    setCards(toggleFavoriteCard({ id: c.id, front: c.front, back: c.back, group: c.group }));
    announce({ kind: 'c', card: c });
  };
  const undo = () => {
    if (!removed) return;
    if (removed.kind === 'q') setFavIds([...setFavorite(removed.id, true)]);
    else {
      const c = removed.card;
      if (!getFavoriteCards().some((x) => x.id === c.id)) setCards(toggleFavoriteCard({ id: c.id, front: c.front, back: c.back, group: c.group }));
    }
    window.clearTimeout(timer.current);
    setRemoved(null);
  };

  const qHref = (q: StudyQuestion) => (q.source === 'arşiv' ? `${pathFor('past_exams')}/${encodeURIComponent(q.id)}` : pathFor('questions', q.id));

  return (
    <div role="tabpanel" id="u12-panel-kayit" aria-labelledby="u12-tab-kayit" className="u12-cols">
      <section className="u12-panel u12-col-a">
        <div className="u12-panel-h">
          <h2 className="u12-h2 u12-grow">Kaydedilen sorular</h2>
          <span className="u12-meta u12-num">{archive ? nf.format(savedQs.length) : nf.format(favIds.length)}</span>
        </div>
        {archive === null ? (
          <p className="u12-loading u12-meta" role="status">Kayıtlı sorular yükleniyor…</p>
        ) : savedQs.length ? (
          <ul className="u12-list">
            {savedQs.map((q) => (
              <li key={q.id} className="u12-row">
                <span className="u12-lead" aria-hidden="true"><FileText /></span>
                <a className="u12-grow u12-two u12-plain" href={qHref(q)} onClick={go(qHref(q))}>
                  <span className="t u12-clamp2">{q.stem}</span>
                  <span className="u12-meta u12-clamp1">{[q.discipline, q.year, q.number ? `Soru ${q.number}` : '', q.source === 'arşiv' ? 'Çıkmış' : 'Soru havuzu'].filter(Boolean).join(' · ')}</span>
                </a>
                <button type="button" className="u12-btn is-icon is-sm is-ghost" aria-label={`Kayıttan çıkar: ${q.stem.slice(0, 80)}`} onClick={() => removeQ(q.id)}>
                  <X aria-hidden />
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <Empty title="Kaydedilen soru yok" body="Çıkmış sorularda ya da çalışırken yıldıza dokunarak soru kaydedebilirsin." />
        )}
        {missing > 0 && <p className="u12-foot u12-meta">{nf.format(missing)} kayıtlı soru artık soru bankasında bulunmuyor.</p>}
      </section>

      <section className="u12-panel u12-col-b">
        <div className="u12-panel-h">
          <h2 className="u12-h2 u12-grow">Kaydedilen kartlar</h2>
          <span className="u12-meta u12-num">{nf.format(cards.length)}</span>
        </div>
        {cards.length ? (
          <ul className="u12-list">
            {cards.map((c) => (
              <li key={c.id} className="u12-row">
                <span className="u12-grow u12-two">
                  <span className="t u12-clamp1">{c.front}</span>
                  <span className="u12-meta u12-clamp2">{c.back}</span>
                </span>
                <button type="button" className="u12-btn is-icon is-sm is-ghost" aria-label={`Kayıttan çıkar: ${c.front.slice(0, 80)}`} onClick={() => removeC(c)}>
                  <X aria-hidden />
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <Empty title="Kaydedilen kart yok" body="Kart tekrarında yıldız simgesiyle kart kaydedebilirsin.">
            <a className="u12-btn is-sm" href={pathFor('flashcards')} onClick={go(pathFor('flashcards'))}>Kartlara git</a>
          </Empty>
        )}
      </section>

      {/* Gövdeye taşınır: animasyonlu üst öğe position:fixed'i kendine bağlamasın */}
      {removed && createPortal(
        <div className="u12-toast" role="status">
          <span>{removed.kind === 'q' ? 'Soru kayıttan çıkarıldı' : 'Kart kayıttan çıkarıldı'}</span>
          <button type="button" onClick={undo}>Geri al</button>
        </div>,
        document.body,
      )}
    </div>
  );
};

/* ------------------------------------------------------------------------------------------------
 * Hesap
 * ---------------------------------------------------------------------------------------------- */

const AccountPanel: React.FC<{
  currentUser: AppUser | null;
  isAdmin: boolean;
  ed: ReturnType<typeof useProfileEditor>;
  nameRef: React.RefObject<HTMLInputElement | null>;
  photo: string;
  onPickPhoto: () => void;
  onRemovePhoto: () => void;
  onOpenAuth: () => void;
  onLogout: () => void;
  onOpenAdmin: () => void;
  onAppearance: () => void;
}> = ({ currentUser, isAdmin, ed, nameRef, photo, onPickPhoto, onRemovePhoto, onOpenAuth, onLogout, onOpenAdmin, onAppearance }) => {
  const nameErr = !!ed.error && /isim|ad/i.test(ed.error);
  const [newPass, setNewPass] = useState('');
  const [passBusy, setPassBusy] = useState(false);
  const [passErr, setPassErr] = useState<string | null>(null);
  const [passOk, setPassOk] = useState<string | null>(null);

  const onSavePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPassErr(null);
    setPassOk(null);
    setPassBusy(true);
    try {
      await setOrUpdateAccountPassword(newPass);
      setNewPass('');
      setPassOk('Şifreniz kaydedildi. Artık hesabınıza hem Google ile hem de e-posta + şifrenizle giriş yapabilirsiniz.');
      toast.success('Şifre kaydedildi', 'Hem Google hem e-posta + şifre ile giriş aktif.');
    } catch (err: any) {
      setPassErr(err?.message || 'Şifre kaydedilemedi.');
    } finally {
      setPassBusy(false);
    }
  };

  const onSendResetMail = async () => {
    if (!currentUser?.email) return;
    setPassErr(null);
    setPassOk(null);
    setPassBusy(true);
    try {
      await sendPasswordReset(currentUser.email);
      setPassOk(`${currentUser.email} adresine şifre belirleme / sıfırlama bağlantısı gönderildi.`);
      toast.success('E-posta gönderildi', `${currentUser.email} gelen kutusunu kontrol edin.`);
    } catch (err: any) {
      setPassErr(err?.message || 'Şifre bağlantısı gönderilemedi.');
    } finally {
      setPassBusy(false);
    }
  };

  return (
    <div role="tabpanel" id="u12-panel-hesap" aria-labelledby="u12-tab-hesap" className="u12-stack">
      {currentUser ? (
        <>
        <form
          className="u12-panel"
          onSubmit={(e) => {
            e.preventDefault();
            ed.save();
          }}
        >
          <div className="u12-panel-h"><h2 className="u12-h2 u12-grow">Profil bilgileri</h2></div>
          <div className="u12-form">
            <div>
              <label className="u12-label" htmlFor="u12-name">Görünen ad</label>
              <div className={`u12-field ${nameErr ? 'is-bad' : ''}`}>
                <input
                  ref={nameRef}
                  id="u12-name"
                  value={ed.name}
                  autoComplete="name"
                  placeholder="Adın ve soyadın"
                  aria-invalid={nameErr || undefined}
                  aria-describedby="u12-name-h"
                  onChange={(e) => ed.setName(e.target.value)}
                />
              </div>
              <span id="u12-name-h" className={`u12-hint ${nameErr ? 'is-bad' : ''}`}>{nameErr ? ed.error : 'Soru ve şık eklerken bu ad kullanılır.'}</span>
            </div>
            <div>
              <label className="u12-label" htmlFor="u12-num">Öğrenci numarası <span className="u12-opt">(isteğe bağlı)</span></label>
              <div className="u12-field">
                <input
                  id="u12-num"
                  className="u12-num"
                  inputMode="numeric"
                  value={ed.num}
                  placeholder="20241054012"
                  aria-describedby="u12-num-h"
                  onChange={(e) => ed.setNum(e.target.value.replace(/\D/g, '').slice(0, 12))}
                />
              </div>
              <span id="u12-num-h" className={`u12-hint ${ed.num.length === 11 ? 'is-ok' : ''}`}>
                {ed.num ? (ed.num.length === 11 ? '11 hane, standart numara' : `${ed.num.length} hane`) : 'Boşluk ve tire otomatik temizlenir.'}
              </span>
            </div>
            <div>
              <label className="u12-label" htmlFor="u12-mail">E-posta</label>
              <div className="u12-field is-ro">
                <Lock aria-hidden />
                <input id="u12-mail" value={currentUser.email || ''} readOnly aria-readonly="true" />
              </div>
              <span className="u12-hint">Giriş hesabına bağlı; buradan değiştirilemez.</span>
            </div>
          </div>

          <div className="u12-avatar">
            <span className="u12-av is-lg" aria-hidden="true">{photo ? <img src={photo} alt="" /> : initialsOf(currentUser)}</span>
            <div className="u12-avatar-t">
              <div>
                <span className="u12-h3">Profil fotoğrafı</span>
                <span className="u12-hint">Görsel seçince kırpma penceresi açılır: sürükleyerek konumla, yakınlaştır. En fazla 15 MB.</span>
              </div>
              <div className="u12-actions">
                <button type="button" className="u12-btn is-sm" onClick={onPickPhoto}><Camera aria-hidden />{photo ? 'Fotoğrafı değiştir' : 'Fotoğraf yükle'}</button>
                {photo && <button type="button" className="u12-btn is-sm is-ghost is-danger" onClick={onRemovePhoto}><Trash2 aria-hidden />Kaldır</button>}
              </div>
            </div>
          </div>

          {ed.error && !nameErr && (
            <div className="u12-alert" role="alert"><AlertCircle aria-hidden /><span>{ed.error}</span></div>
          )}
          <div className="u12-panel-f">
            {ed.saved && <span className="u12-hint is-ok u12-saved" role="status"><CheckCircle2 aria-hidden />Kaydedildi</span>}
            <button type="button" className="u12-btn is-ghost" onClick={ed.reset} disabled={!ed.dirty || ed.saving}>Vazgeç</button>
            <button type="submit" className="u12-btn is-pri" disabled={!ed.dirty || ed.saving} aria-busy={ed.saving || undefined}>{ed.saving ? 'Kaydediliyor…' : 'Kaydet'}</button>
          </div>
        </form>

        <form className="u12-panel" onSubmit={onSavePassword}>
          <div className="u12-panel-h">
            <h2 className="u12-h2 u12-grow">Şifre belirle / değiştir</h2>
          </div>
          <div className="u12-form">
            <div>
              <label className="u12-label" htmlFor="u12-new-pass">Yeni e-posta şifresi (en az 6 karakter)</label>
              <div className="u12-field">
                <input
                  id="u12-new-pass"
                  type="password"
                  value={newPass}
                  autoComplete="new-password"
                  placeholder="Yeni şifreniz"
                  disabled={passBusy}
                  onChange={(e) => setNewPass(e.target.value)}
                />
              </div>
              <span className="u12-hint">
                Google ile giriş yaptığınızda Firebase güvenlik gereği eski şifreyi kaldırır. Buradan yeni şifre tanımlayarak hesabınıza hem Google ile hem de e-posta + şifre ile giriş yapabilirsiniz.
              </span>
            </div>
          </div>
          {passErr && (
            <div className="u12-alert" role="alert"><AlertCircle aria-hidden /><span>{passErr}</span></div>
          )}
          {passOk && (
            <div className="u12-panel-f"><span className="u12-hint is-ok u12-saved" role="status"><CheckCircle2 aria-hidden />{passOk}</span></div>
          )}
          <div className="u12-panel-f">
            <button type="button" className="u12-btn is-ghost" onClick={onSendResetMail} disabled={passBusy}>
              E-postama şifre bağlantısı gönder
            </button>
            <button type="submit" className="u12-btn is-pri" disabled={passBusy || newPass.trim().length < 6}>
              {passBusy ? 'İşleniyor…' : 'Şifreyi kaydet'}
            </button>
          </div>
        </form>
        </>
      ) : (
        <section className="u12-panel">
          <Empty icon={UserRound} title="Giriş yapmadın" body="Katkıların adınla ve fotoğrafınla görünsün. Görünüm ayarları girişsiz de çalışır.">
            <button type="button" className="u12-btn is-sm is-pri" onClick={onOpenAuth}><LogIn aria-hidden />Giriş yap</button>
          </Empty>
        </section>
      )}

      <section className="u12-panel">
        <NavRow icon={PaletteIcon} title="Görünüm ve tasarım (Net v12)" sub="Tasarım, tema, palet, yoğunluk, yazı, süzgeç modu" onClick={onAppearance} />
        {!pwaService.getState().isInstalled && (
          <NavRow icon={Smartphone} title="Uygulamayı cihaza yükle (Tam Ekran PWA)" sub="iOS Safari, iOS Chrome, Android ve bilgisayarda ana ekrana ekle" onClick={() => pwaService.promptInstall()} />
        )}
        <NavRow icon={Compass} title="Tanıtım turu" sub="Sayfaları ve özellikleri yeniden gez" onClick={startWelcomeTour} />
        <NavRow icon={Compass} title="Öğren turu" sub="Ders kitaplığı ve etkileşim türleri" onClick={onLearnTour} />
        {isAdmin && <NavRow icon={ShieldCheck} title="Yönetim konsolu" sub="Taslaklar, moderasyon, sistem" onClick={onOpenAdmin} />}
        {currentUser && (
          <SetRow id="u12-oturum" title="Oturum" sub="Bu cihazda çıkış yaparsın. Eşitlenmiş ilerlemen hesabında kalır.">
            <button type="button" className="u12-btn is-sm is-danger" onClick={onLogout}><LogOut aria-hidden />Çıkış yap</button>
          </SetRow>
        )}
      </section>
    </div>
  );
};

/* ------------------------------------------------------------------------------------------------
 * Veriler ve gizlilik
 * ---------------------------------------------------------------------------------------------- */

const DataPanel: React.FC<{ onOpenOffline: () => void }> = ({ onOpenOffline }) => {
  const download = useCallback(() => {
    try {
      const blob = new Blob([JSON.stringify(collectLocalUserData(), null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `medsoru-verilerim-${dayKey()}.json`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch {
      toast.error('İndirilemedi', 'Tarayıcı dosya oluşturmaya izin vermedi.');
    }
  }, []);

  return (
    <div role="tabpanel" id="u12-panel-veri" aria-labelledby="u12-tab-veri" className="u12-stack">
      <section className="u12-panel">
        <div className="u12-panel-h"><h2 className="u12-h2 u12-grow">Eşitleme ve Bildirimler</h2></div>
        <div className="u12-legacy">
          <UserDataSyncRow />
          <ArkaPlanRow />
          <WhatsAppDailyDigestRow />
          <NotesSyncRow />
        </div>
      </section>

      <section className="u12-panel">
        {!pwaService.getState().isInstalled && (
          <SetRow id="u12-pwa-kur" title="Uygulamayı cihaza yükle (PWA)" sub="Tarayıcı adres çubuklarını kaldırarak gerçek tam ekran ve çevrimdışı uygulama olarak çalıştır.">
            <button type="button" className="u12-btn is-sm is-pri" onClick={() => pwaService.promptInstall()}><Smartphone aria-hidden />Ana Ekrana Ekle</button>
          </SetRow>
        )}
        <SetRow id="u12-indir" title="Verilerimi indir" sub="Bu cihazdaki ilerleme, test geçmişi, kaydedilenler, notlar ve bildirimler tek JSON dosyasında.">
          <button type="button" className="u12-btn is-sm" onClick={download}><Download aria-hidden />İndir (JSON)</button>
        </SetRow>
        <SetRow id="u12-cevrimdisi" title="Çevrimdışı veritabanı" sub="Soruları, sözlüğü ve kartları cihaza indir; bağlantı yokken de çalış.">
          <button type="button" className="u12-btn is-sm" onClick={onOpenOffline}><Database aria-hidden />Cihaza indir</button>
        </SetRow>
      </section>

      <section className="u12-panel" id="u12-sifirla">
        <div className="u12-legacy">
          <ProgressResetRow />
        </div>
      </section>

      <p className="u12-foot u12-meta">E-posta adresin her kurulda ilk katkın için teşekkür e-postası almak içindir; kimseyle paylaşılmaz.</p>
    </div>
  );
};

/* ------------------------------------------------------------------------------------------------
 * Görünüm ve tasarım (canvas Settings.dc.html)
 * ---------------------------------------------------------------------------------------------- */

const DESIGN_INFO: Record<DesignChoice, { name: string; hint: string }> = {
  v13: { name: 'Ada', hint: 'Yüzen menü adaları, şeritsiz, en kompakt. Telefon ve tablete göre kuruldu.' },
  v12: { name: 'Net', hint: 'Sade, kompakt, tek ekranda bilgi.' },
  v11: { name: 'Sade', hint: 'Geniş boşluklar, okuma odaklı.' },
  v10: { name: 'Klasik', hint: 'Kart ızgaraları, renkli bölümler.' },
};

const LAYOUT_HINTS: Record<LayoutMode, string> = {
  akis: 'Sade: tek sütun, okumaya uygun dar genişlik; yan sütunlar ve açıklamalar gizlenir, menü ince şerit.',
  pano: 'Dengeli: içerik 1320 px\'e kadar yayılır; çok geniş ekranda çıkmış kartları iki sütun olur.',
  odak: 'Geniş ekran: sayfalar tüm genişliği kullanır; liste solda, ayrıntı sağda açılır.',
};
const DENSITY_HINTS: Record<Density, string> = {
  compact: 'Arayüz %92: daha çok içerik sığar. Telefonda dokunma alanları küçülmesin diye uygulanmaz.',
  normal: 'Arayüz %100.',
  wide: 'Arayüz %108: menü, düğme, liste yazıları ve boşluklar birlikte büyür.',
};

const AppearancePanel: React.FC = () => {
  const look = useAppearance();
  const [autoReveal, setAutoReveal] = useState(autoRevealEnabled);
  const palInfo = PALETTE_INFO[look.mode][look.palette];
  const accents = findPalette(look.mode, look.palette).accents;

  return (
    <div role="region" aria-labelledby="u12-gorunum-h" className="u12-stack">
      <h2 id="u12-gorunum-h" className="u12-vh">Görünüm ve tasarım</h2>
      <section className="u12-stack is-tight" aria-labelledby="u12-tasarim-h">
        <div className="u12-sechead">
          <h3 id="u12-tasarim-h" className="u12-h2 u12-grow">Tasarım</h3>
          <span className="u12-meta">Eski sürümler kalır; istediğin an geç.</span>
        </div>
        <div className="u12-designs" role="radiogroup" aria-labelledby="u12-tasarim-h">
          {DESIGN_CHOICES.map((v) => {
            const on = designChoiceOf(look) === v;
            return (
              <button key={v} type="button" role="radio" aria-checked={on} className={`u12-design is-${v} ${on ? 'is-on' : ''}`} onClick={() => look.set({ choice: v })}>
                <span className="u12-mini" aria-hidden="true"><i /><i /><i /><i /></span>
                <span className="u12-design-t">
                  <span className="u12-h3">{DESIGN_INFO[v].name}</span>
                  <span className={`u12-badge ${v === 'v13' ? 'is-acc' : ''}`}>{v}</span>
                  {on && <Check className="u12-design-ok" aria-hidden />}
                </span>
                <span className="u12-meta">{DESIGN_INFO[v].hint}</span>
              </button>
            );
          })}
        </div>
      </section>

      <section className="u12-panel" aria-label="Renk ve yazı">
        <SetRow id="u12-s-tema" title="Tema" sub={look.mode === 'sepia' ? 'Sarı tema uzun okuma için: kâğıt tonu, düşük mavi ışık.' : 'Ortam ışığına göre seç; her temanın paleti ayrı hatırlanır.'}>
          <Seg<ThemeMode> label="Tema" value={look.mode} onChange={(m) => look.set({ mode: m })}
            options={(['light', 'sepia', 'dark'] as ThemeMode[]).map((m) => ({ value: m, label: MODE_LABELS[m] }))} />
        </SetRow>
        <SetRow id="u12-s-palet" title={`Palet · ${palInfo?.name || ''}`} sub={palInfo?.hint || 'Her temada ayrı palet.'}>
          <div className="u12-swatches" role="radiogroup" aria-labelledby="u12-s-palet">
            {palettesFor(look.mode).map(({ id: p }) => {
              const info = PALETTE_INFO[look.mode][p];
              const on = look.palette === p;
              return (
                <button key={p} type="button" role="radio" aria-checked={on} aria-label={info.name} title={info.hint} className="u12-sw" onClick={() => look.set({ palette: p })}
                  style={{ '--sw-bg': info.swatch[0], '--sw-ac': info.swatch[2] } as React.CSSProperties}>
                  <i aria-hidden="true" />
                </button>
              );
            })}
          </div>
        </SetRow>
        {accents && (
          <SetRow id="u12-s-vurgu" title="Vurgu rengi" sub="Düğmeler, seçili sekmeler ve vurgular bu renge geçer; zemin aynı kalır.">
            <div className="u12-swatches" role="radiogroup" aria-labelledby="u12-s-vurgu">
              {accents.map((a) => {
                const on = look.accent === a.id;
                return (
                  <button key={a.id} type="button" role="radio" aria-checked={on} aria-label={a.name} title={a.name} className="u12-sw is-acc" onClick={() => look.set({ accent: a.id })}
                    style={{ '--sw-ac': a.accent, '--sw-on': a.on } as React.CSSProperties}>
                    <i aria-hidden="true">{on && <Check />}</i>
                  </button>
                );
              })}
            </div>
          </SetRow>
        )}
        <SetRow id="u12-s-yog" title="Arayüz ölçeği" sub={DENSITY_HINTS[look.density]}>
          <Seg<Density> label="Yoğunluk" value={look.density} onChange={(d) => look.set({ density: d })}
            options={(['wide', 'normal', 'compact'] as Density[]).map((d) => ({ value: d, label: DENSITY_LABELS[d] }))} />
        </SetRow>
        <SetRow id="u12-s-boyut" title={`Yazı boyutu · ${look.textPx} px`} sub="12–20 px arası. Tüm arayüz (yazılar, düğmeler, boşluklar, menü) bu boyuta göre ölçeklenir; 16 px varsayılan.">
          <TextSizeSlider />
        </SetRow>
        <p className="u12-meta u12-preview-read" aria-hidden="true">Gebeliğin 20. haftasından sonra yeni başlayan hipertansiyon ve proteinüri preeklampsi düşündürür.</p>
        <SetRow id="u12-s-okuma" title="Okuma yazısı" sub="Soru kökü, ders anlatımı ve notlarda.">
          <Seg<ReadingFont> label="Okuma yazısı" value={look.reading} onChange={(v) => look.set({ reading: v })}
            options={[
              { value: 'serif', label: 'Tırnaklı', style: { fontFamily: 'var(--read-font, Georgia, serif)' } },
              { value: 'sans', label: 'Düz' },
            ]} />
        </SetRow>
      </section>

      <section className="u12-panel" aria-label="Kullanım">
        <SetRow id="u12-s-suzgec" title="Süzgeç modu" sub="Basit: arama + hızlı haplar. Gelişmiş: tüm süzgeç ve sıralama hep açık.">
          <Seg<FilterMode> label="Süzgeç modu" value={look.filters} onChange={(v) => look.set({ filters: v })}
            options={(['basit', 'gelismis'] as FilterMode[]).map((v) => ({ value: v, label: FILTER_MODE_LABELS[v] }))} />
        </SetRow>
        <SetRow id="u12-s-etiket" title="Soru etiketleri" sub="Çıkmış ve örnek soru kartlarındaki işaret etiketleri. Kapalıyken yalnız soru ve şıklar görünür.">
          <Toggle labelledBy="u12-s-etiket" checked={look.qtags} onChange={(on) => look.set({ qtags: on })} />
        </SetRow>
        <SetRow id="u12-s-qcard" title="Çıkmış soru kartı" sub={QCARD_MODE_HINTS[look.qcard.mode]}>
          <Seg<QCardMode> label="Çıkmış soru kartı" value={look.qcard.mode} onChange={(v) => look.set({ qcard: { mode: v } })}
            options={(['tam', 'katlanir', 'dar'] as QCardMode[]).map((v) => ({ value: v, label: QCARD_MODE_LABELS[v] }))} />
        </SetRow>
        {QCARD_FIELDS.map(([k, title, sub]) => (
          <SetRow key={k} id={`u12-s-qc-${k}`} title={title} sub={sub}>
            <Toggle labelledBy={`u12-s-qc-${k}`} checked={look.qcard[k] as boolean} onChange={(on) => look.set({ qcard: { [k]: on } })} />
          </SetRow>
        ))}
        <SetRow id="u12-s-hareket" title="Hareket" sub="Az: geçiş ve canlandırmalar kapanır, sayfalar anında değişir. Sistem tercihi “azalt” ise her zaman uyulur.">
          <Seg<MotionPref> label="Hareket" value={look.motion} onChange={(v) => look.set({ motion: v })}
            options={[{ value: 'full', label: 'Tam' }, { value: 'reduced', label: 'Az' }]} />
        </SetRow>
        <SetRow id="u12-s-duzen" title="Görüntüleme modu" sub={`${LAYOUT_HINTS[look.layout]} Telefonda üç mod da tek sütundur.`}>
          <Seg<LayoutMode> label="Görüntüleme modu" value={look.layout} onChange={(v) => look.set({ layout: v })}
            options={(['akis', 'pano', 'odak'] as LayoutMode[]).map((v) => ({ value: v, label: LAYOUT_LABELS[v] }))} />
        </SetRow>
        <SetRow id="u12-s-kaydir" title="Açılan öğeye otomatik kaydır" sub="Açılan içerik (açıklama, kart, menü bölümü) ekran dışında kalırsa görünür alana getirir.">
          <Toggle labelledBy="u12-s-kaydir" checked={autoReveal} onChange={(on) => { setAutoReveal(on); setAutoRevealEnabled(on); }} />
        </SetRow>
      </section>
      <p className="u12-foot u12-meta">Görünüm ayarları bu cihazda saklanır ve girişliyken hesabınla eşitlenir.</p>
    </div>
  );
};
