import React, { useEffect, useMemo, useRef, useState } from 'react';
import { getProgress, getNotes } from '../../services/studyStore';
import { getStudySeconds } from '../../services/activityLog';
import { pathFor, linkClick } from '../../router';
import { autoRevealEnabled, setAutoRevealEnabled } from '../../utils/autoReveal';
import {
  AlertCircle,
  Camera,
  Check,
  CheckCircle2,
  Database,
  LogIn,
  LogOut,
  Moon,
  Palette as PaletteIcon,
  Rows3,
  ShieldCheck,
  Sun,
  SunMedium,
  Trash2,
  UserRound,
  Crosshair,
  ChevronRight,
} from 'lucide-react';
import { AppUser, updateUserProfileData } from '../../services/auth';
import { QuestionItem } from '../../types';
import { validateNamePolicy } from '../../utils/namePolicy';
import {
  DENSITY_LABELS,
  MODE_LABELS,
  PALETTE_INFO,
  type Density,
  type ThemeMode,
  useAppearance,
} from '../../utils/appearance';
import { palettesFor } from '../../utils/palettes';
import { AvatarCropper } from '../ui/AvatarCropper';
import { Row, Section, Segmented, Switch } from '../ui/kit';
import { toast } from '../ui/Toast';
import { NotesSyncRow } from './NotesSyncRow';

interface Props {
  currentUser: AppUser | null;
  isAdmin: boolean;
  questions: QuestionItem[];
  onUpdateUser: (u: AppUser) => void;
  onOpenAuth: () => void;
  onLogout: () => void;
  onOpenAdmin: () => void;
  onOpenOffline: () => void;
}

const SECTIONS = [
  { id: 'profil', label: 'Profil', icon: UserRound },
  { id: 'gorunum', label: 'Tema ve palet', icon: PaletteIcon },
  { id: 'yogunluk', label: 'Yoğunluk', icon: Rows3 },
  { id: 'calisma', label: 'Çalışma', icon: Crosshair },
  { id: 'hesap', label: 'Hesap ve veri', icon: ShieldCheck },
] as const;

const MODE_ICONS: Record<ThemeMode, React.ElementType> = { light: Sun, sepia: SunMedium, dark: Moon };

const initialsOf = (u: AppUser | null) => {
  const src = (u?.displayName || u?.email || 'Ö').trim();
  const parts = src.split(/[^\p{L}]+/u).filter(Boolean);
  return ((parts[0]?.[0] || 'Ö') + (parts[1]?.[0] || '')).toLocaleUpperCase('tr-TR');
};

/**
 * Profil ve Ayarlar tek sayfada (/ayarlar, /profil): kimlik, görünüm (tema × palet), yoğunluk, hesap.
 * Görünüm ayarları girişsiz de çalışır; profil bölümü girişte açılır.
 */
export const ProfileSettingsView: React.FC<Props> = ({ currentUser, isAdmin, questions, onUpdateUser, onOpenAuth, onLogout, onOpenAdmin, onOpenOffline }) => {
  const look = useAppearance();
  const [active, setActive] = useState<string>('profil');
  const [autoReveal, setAutoReveal] = useState(autoRevealEnabled);

  // Kısa yol listesinde etkin bölüm: kaydırmayla izlenir
  useEffect(() => {
    const els = SECTIONS.map((s) => document.getElementById(s.id)).filter(Boolean) as HTMLElement[];
    const io = new IntersectionObserver(
      (entries) => {
        const vis = entries.filter((e) => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
        if (vis) setActive(vis.target.id);
      },
      { rootMargin: '-80px 0px -55% 0px' }
    );
    els.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, []);

  return (
    <div className="ui-page is-wide">
      <div className="ui-page-head">
        <h1>Profil ve ayarlar</h1>
        <p>Kimliğin, görünüm ve yerleşim tercihlerin. Görünüm ayarları bu cihazda saklanır.</p>
      </div>

      <div className="ui-split">
        <nav className="ui-toc" aria-label="Ayar bölümleri">
          {SECTIONS.map(({ id, label, icon: Icon }) => (
            <a
              key={id}
              href={`#${id}`}
              aria-current={active === id}
              onClick={(e) => {
                e.preventDefault();
                document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
                setActive(id);
              }}
            >
              <Icon strokeWidth={2} />
              {label}
            </a>
          ))}
        </nav>

        <div className="flex flex-col min-w-0" style={{ gap: 'calc(var(--dn-gap) * 2.25)' }}>
          <ProfileSection currentUser={currentUser} questions={questions} onUpdateUser={onUpdateUser} onOpenAuth={onOpenAuth} />

          <Section id="gorunum" title="Tema ve palet" foot="Sarı tema uzun okuma için: kâğıt tonu, düşük mavi ışık. Her temanın paleti ayrı hatırlanır.">
            <div className="ui-group">
              <Row
                stack
                title="Tema"
                sub={`${MODE_LABELS[look.mode]} · ${PALETTE_INFO[look.mode][look.palette].name}`}
              >
                <Segmented<ThemeMode>
                  label="Tema"
                  value={look.mode}
                  onChange={(m) => look.set({ mode: m })}
                  options={(['light', 'sepia', 'dark'] as ThemeMode[]).map((m) => {
                    const Icon = MODE_ICONS[m];
                    return {
                      value: m,
                      label: (
                        <span className="inline-flex items-center gap-1.5">
                          <Icon className="w-4 h-4" strokeWidth={2} />
                          {MODE_LABELS[m]}
                        </span>
                      ),
                    };
                  })}
                />
              </Row>
              <Row stack title="Palet">
                <div role="radiogroup" aria-label={`${MODE_LABELS[look.mode]} tema paleti`} className="grid gap-2.5" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(min(100%, 140px), 1fr))' }}>
                  {palettesFor(look.mode).map(({ id: p }) => {
                    const info = PALETTE_INFO[look.mode][p];
                    const on = look.palette === p;
                    return (
                      <button key={p} type="button" role="radio" aria-checked={on} className="ui-choice" onClick={() => look.set({ palette: p })}>
                        <PaletteSwatch colors={info.swatch} dark={look.mode === 'dark'} />
                        <span className="flex flex-col gap-0.5 min-w-0">
                          <b>{info.name}</b>
                          <span>{info.hint}</span>
                        </span>
                        {on && (
                          <span className="ui-choice-check" aria-hidden="true">
                            <Check strokeWidth={3} />
                          </span>
                        )}
                      </button>
                    );
                  })}
                </div>
              </Row>
            </div>
          </Section>

          <Section id="yogunluk" title="Yoğunluk" foot="Kompakt soru çözümünde daha çok bilgi gösterir; Geniş, yazıyı büyütür ve kartları ferahlatır. Dokunmatik ekranda düğmeler parmak boyutunun altına inmez.">
            <div className="ui-group">
              <Row stack title="Yerleşim" sub="Yazı ölçeği, boşluklar, satır ve kontrol yükseklikleri, ızgara kolonları birlikte değişir.">
                <Segmented<Density>
                  label="Yoğunluk"
                  value={look.density}
                  onChange={(d) => look.set({ density: d })}
                  options={(['compact', 'normal', 'wide'] as Density[]).map((d) => ({ value: d, label: DENSITY_LABELS[d] }))}
                />
              </Row>
              <div className="ui-row ui-row-stack">
                <DensityPreview />
              </div>
            </div>
          </Section>

          <Section
            id="calisma"
            title="Çalışma"
            foot="Bir şıkka ya da etkileşime dokunduğunda açılan açıklama ekranın altında kalırsa kart görünür alanın ortasına kaydırılır."
          >
            <div className="ui-group">
              <Row
                icon={Crosshair}
                iconBg="#1E4FD8"
                title="Açıklamaya otomatik kaydır"
                sub={autoReveal ? 'Açık' : 'Kapalı'}
                end={<Switch label="Açıklamaya otomatik kaydır" checked={autoReveal} onChange={(on) => { setAutoReveal(on); setAutoRevealEnabled(on); }} />}
              />
            </div>
          </Section>

          <Section id="hesap" title="Hesap ve veri">
            <div className="ui-group">
              <Row icon={Database} iconBg="#30B0C7" title="Çevrimdışı veritabanı" sub="Soruları, sözlüğü ve kartları cihaza indir" onClick={onOpenOffline} />
              <NotesSyncRow />
              {isAdmin && <Row icon={ShieldCheck} iconBg="#FF9500" title="Yönetim konsolu" sub="Taslaklar, moderasyon, sistem" onClick={onOpenAdmin} />}
              {currentUser ? (
                <button type="button" className="ui-row has-icon" onClick={onLogout}>
                  <span className="ui-ico" style={{ '--ico-bg': 'var(--color-bad)', '--ico-fg': '#fff' } as React.CSSProperties}>
                    <LogOut strokeWidth={2.1} />
                  </span>
                  <span className="ui-row-main">
                    <b style={{ color: 'var(--color-bad-text)' }}>Çıkış yap</b>
                  </span>
                </button>
              ) : (
                <Row icon={LogIn} title="Giriş yap" sub="Katkıların adınla görünsün" onClick={onOpenAuth} />
              )}
            </div>
          </Section>
        </div>
      </div>
    </div>
  );
};

const PaletteSwatch: React.FC<{ colors: [string, string, string]; dark: boolean }> = ({ colors: [bg, card, accent], dark }) => (
  <span
    className="ui-swatch"
    aria-hidden="true"
    style={{ '--sw-bg': bg, '--sw-card': card, '--sw-accent': accent, '--sw-ink': dark ? '#E6E9EF' : '#2A2622' } as React.CSSProperties}
  >
    <i />
    <i />
    <em>
      <s />
      <s />
    </em>
  </span>
);

/** Yoğunluğun canlı önizlemesi: gerçek tokenlarla çizilmiş küçük bir soru kartı */
const DensityPreview: React.FC = () => (
  <div className="ui-preview d-farm" aria-label="Önizleme">
    <div className="pv-q">
      <span className="pv-meta">
        <span className="hk-dot" />
        Farmakoloji · Lokal anestezikler
      </span>
      <p className="pv-stem">Aşağıdakilerden hangisi amid yapılı bir lokal anesteziktir?</p>
      <div>
        <div className="pv-opt"><i>A</i>Prokain</div>
        <div className="pv-opt is-ok"><i>B</i>Lidokain</div>
        <div className="pv-opt"><i>C</i>Tetrakain</div>
      </div>
    </div>
  </div>
);

const ProfileSection: React.FC<{
  currentUser: AppUser | null;
  questions: QuestionItem[];
  onUpdateUser: (u: AppUser) => void;
  onOpenAuth: () => void;
}> = ({ currentUser, questions, onUpdateUser, onOpenAuth }) => {
  const [name, setName] = useState(currentUser?.displayName || '');
  const [num, setNum] = useState(currentUser?.studentNumber || '');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);
  const [cropFile, setCropFile] = useState<File | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setName(currentUser?.displayName || '');
    setNum(currentUser?.studentNumber || '');
  }, [currentUser?.uid]);

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

  if (!currentUser) {
    return (
      <Section id="profil" title="Profil">
        <div className="ui-group">
          <div className="ui-row" style={{ gap: 16, paddingBlock: 'var(--dn-pad)' }}>
            <span className="ui-avatar" style={{ '--av': '56px' } as React.CSSProperties}>
              <UserRound className="w-6 h-6" />
            </span>
            <span className="ui-row-main">
              <b>Giriş yapmadın</b>
              <span>Katkıların adınla ve fotoğrafınla görünsün. Görünüm ayarları girişsiz de çalışır.</span>
            </span>
            <button type="button" className="ui-btn is-primary" onClick={onOpenAuth}>
              Giriş yap
            </button>
          </div>
        </div>
      </Section>
    );
  }

  const dirty = name.trim() !== (currentUser.displayName || '') || num !== (currentUser.studentNumber || '');
  const nameErr = error && /isim|ad/i.test(error);

  const save = async (patch?: { photoURL?: string | null }) => {
    setError(null);
    if (!patch && name.trim()) {
      const check = validateNamePolicy(name.trim(), { adminEmail: currentUser.email });
      if (!check.isValid) {
        setError(check.errorMessage || 'Geçersiz isim.');
        return;
      }
    }
    setSaving(true);
    try {
      const updated = await updateUserProfileData(currentUser, {
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

  const photo = currentUser.photoURL || '';

  return (
    <Section id="profil" title="Profil" foot="E-posta adresin her kurulda ilk katkın için teşekkür e-postası almak içindir; kimseyle paylaşılmaz.">
      <div className="ui-group">
        <div className="ui-row" style={{ gap: 16, paddingBlock: 'var(--dn-pad)' }}>
          <span className="ui-avatar" style={{ '--av': '72px' } as React.CSSProperties}>
            {photo ? <img src={photo} alt="Profil fotoğrafı" /> : initialsOf(currentUser)}
          </span>
          <span className="ui-row-main" style={{ gap: 2 }}>
            <b style={{ fontSize: 'calc(var(--dn-body) + 4px)', fontWeight: 650 }}>{currentUser.displayName || currentUser.email?.split('@')[0]}</b>
            <span>{currentUser.email}</span>
            <span className="flex flex-wrap gap-1.5 mt-1.5">
              <button type="button" className="ui-btn is-tonal is-sm" onClick={() => fileRef.current?.click()}>
                <Camera />
                {photo ? 'Değiştir' : 'Fotoğraf ekle'}
              </button>
              {photo && (
                <button type="button" className="ui-btn is-ghost is-sm" style={{ '--b-fg': 'var(--color-bad-text)' } as React.CSSProperties} onClick={() => save({ photoURL: '' })}>
                  <Trash2 />
                  Kaldır
                </button>
              )}
            </span>
          </span>
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
        </div>
      </div>

      {(() => {
        // Profil istatistik şeridi (canvas "Settings"): gerçek veriler — katkı (havuz), çözüm, süre, not (bu cihaz)
        const prog = Object.values(getProgress());
        const ok = prog.filter((a) => a.correct).length;
        const sec = Object.values(getStudySeconds()).reduce((a, s) => a + s, 0);
        const h = Math.floor(sec / 3600), m = Math.round((sec % 3600) / 60);
        return (
          <div className="pf-stats">
            <div><b>{contributed}</b><span>katkı verdiğin soru</span></div>
            <div><b>{prog.length}</b><span>çözdüğün soru</span></div>
            <div><b>%{prog.length ? Math.round((ok / prog.length) * 100) : 0}</b><span>doğruluk</span></div>
            <div><b>{h ? `${h} sa ${m} dk` : `${m} dk`}</b><span>çalışma süresi</span></div>
            <div><b>{getNotes().length}</b><span>not</span></div>
            <a href={pathFor('stats')} onClick={linkClick(() => { window.history.pushState(null, '', pathFor('stats')); window.dispatchEvent(new PopStateEvent('popstate')); })} className="pf-more">İstatistiklerim <ChevronRight aria-hidden /></a>
          </div>
        );
      })()}

      <form
        className="ui-group"
        style={{ marginTop: 'calc(var(--dn-gap) * .5)' }}
        onSubmit={(e) => {
          e.preventDefault();
          save();
        }}
      >
        <div className="ui-row ui-row-stack">
          <div className="ui-field">
            <label htmlFor="pf-name">Görünen ad</label>
            <input
              id="pf-name"
              className="ui-input"
              value={name}
              autoComplete="name"
              aria-invalid={nameErr ? true : undefined}
              aria-describedby="pf-name-h"
              onChange={(e) => setName(e.target.value)}
              placeholder="Adın ve soyadın"
            />
            <span id="pf-name-h" className={`ui-hint ${nameErr ? 'is-error' : ''}`}>
              {nameErr ? error : 'Soru ve şık eklerken bu ad kullanılır.'}
            </span>
          </div>
          <div className="ui-field">
            <label htmlFor="pf-num">Öğrenci numarası <span style={{ fontWeight: 400, color: 'var(--color-ink-3)' }}>(isteğe bağlı)</span></label>
            <input
              id="pf-num"
              className="ui-input"
              inputMode="numeric"
              value={num}
              style={{ fontFamily: 'var(--font-mono)' }}
              onChange={(e) => setNum(e.target.value.replace(/\D/g, '').slice(0, 12))}
              placeholder="20241054012"
              aria-describedby="pf-num-h"
            />
            <span id="pf-num-h" className={`ui-hint ${num.length === 11 ? 'is-ok' : ''}`}>
              {num ? (num.length === 11 ? '11 hane, standart numara' : `${num.length} hane`) : 'Boşluk ve tire otomatik temizlenir.'}
            </span>
          </div>
          {error && !nameErr && (
            <div className="ui-callout is-bad" role="alert">
              <AlertCircle />
              <span>{error}</span>
            </div>
          )}
          <div className="flex items-center justify-end gap-2">
            {saved && (
              <span className="ui-hint is-ok inline-flex items-center gap-1" role="status">
                <CheckCircle2 className="w-4 h-4" /> Kaydedildi
              </span>
            )}
            <button type="submit" className={`ui-btn is-primary ${saving ? 'is-loading' : ''}`} disabled={!dirty || saving}>
              Kaydet
            </button>
          </div>
        </div>
      </form>

      {cropFile && (
        <AvatarCropper
          file={cropFile}
          onCancel={() => setCropFile(null)}
          onDone={(url) => {
            setCropFile(null);
            save({ photoURL: url });
          }}
        />
      )}
    </Section>
  );
};
