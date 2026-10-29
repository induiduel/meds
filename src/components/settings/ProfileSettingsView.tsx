import React, { useEffect, useMemo, useRef, useState } from 'react';
import { TextSizeSlider } from './TextSizeSlider';
import { getProgress, getNotes } from '../../services/studyStore';
import { getStudySeconds } from '../../services/activityLog';
import { pathFor, linkClick } from '../../router';
import { autoRevealEnabled, setAutoRevealEnabled } from '../../utils/autoReveal';
import {
  AlertCircle,
  Camera,
  Check,
  CheckCircle2,
  ChevronDown,
  Database,
  LogIn,
  LogOut,
  Moon,
  Palette as PaletteIcon,
  ShieldCheck,
  Sun,
  SunMedium,
  Trash2,
  UserRound,
  ChevronRight,
  Compass,
} from 'lucide-react';
import { AppUser, updateUserProfileData } from '../../services/auth';
import { QuestionItem } from '../../types';
import { validateNamePolicy } from '../../utils/namePolicy';
import {
  DENSITY_LABELS,
  LAYOUT_LABELS,
  READING_LABELS,
  READING_ORDER,
  type DesignVersion,
  TEXT_SIZE_ORDER,
  TEXT_SIZE_PX,
  FILTER_MODE_LABELS,
  type ReadingFont,
  type TextSize,
  type FilterMode,
  MODE_LABELS,
  PALETTE_INFO,
  type Density,
  type LayoutMode,
  type ThemeMode,
  useAppearance,
  QCARD_MODE_LABELS,
  type QCardMode,
  type QCardPrefs,
} from '../../utils/appearance';
import { findPalette, palettesFor } from '../../utils/palettes';
import { AvatarCropper } from '../ui/AvatarCropper';
import { Row, Section, Segmented, Switch } from '../ui/kit';
import { performansModu, performansModuAyarla, tvModu, tvModuAyarla } from '../../services/hizliMod';
import { toast } from '../ui/Toast';
import { NotesSyncRow } from './NotesSyncRow';
import { UserDataSyncRow } from './UserDataSyncRow';
import { ArkaPlanRow } from './ArkaPlanRow';
import { GorunumEkleri } from './GorunumEkleri';
import { ProgressResetRow } from './ProgressResetRow';
import { startWelcomeTour } from '../onboarding/tourState';
import { onLearnTour } from '../onboarding/learnTourState';
import { ProfileV12 } from '../v12/ProfileV12';
import './settings.css';

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

const LAYOUT_CHOICES: { id: LayoutMode; hint: string }[] = [
  { id: 'akis', hint: 'Tek sütun, okumaya uygun genişlik; menü ince şerit.' },
  { id: 'pano', hint: 'Geniş ızgara: kartlar sütunlara dizilir, menü açık.' },
  { id: 'odak', hint: 'Tam genişlik: liste solda, ayrıntı sağda açılır.' },
];

const SECTIONS = [
  { id: 'gorunum', label: 'Görünüm', icon: PaletteIcon },
  { id: 'profil', label: 'Profil', icon: UserRound },
  { id: 'hesap', label: 'Hesap ve veri', icon: ShieldCheck },
] as const;

const MODE_ICONS: Record<ThemeMode, React.ElementType> = { light: Sun, sepia: SunMedium, dark: Moon };

const initialsOf = (u: AppUser | null) => {
  const src = (u?.displayName || u?.email || 'Ö').trim();
  const parts = src.split(/[^\p{L}]+/u).filter(Boolean);
  return ((parts[0]?.[0] || 'Ö') + (parts[1]?.[0] || '')).toLocaleUpperCase('tr-TR');
};

/**
 * Profil ve Ayarlar tek sayfada (/ayarlar, /profil) — v10 kompakt yeniden kurulum (2026-10-13, "Ayarlar-Masaustu").
 * Masaüstünde solda kullanıcı kartı + bölüm menüsü; sağda Görünüm (tema kartları, palet ızgarası, görüntüleme modu,
 * kompakt ayar listesi), Profil ve Hesap ve veri. Tablet/telefonda menü üstte yatay çip satırına döner.
 * Görünüm ayarları girişsiz de çalışır; profil bölümü girişte açılır.
 */
export const ProfileSettingsView: React.FC<Props> = (props) => {
  // v12 "Net": canvas Profile + Settings panolarına göre ayrı yapı (components/v12/ProfileV12.tsx); v10/v11 aşağıda değişmeden
  const v12 = useAppearance().design === 'v12';
  return v12 ? <ProfileV12 {...props} /> : <ProfileSettingsClassic {...props} />;
};

const ProfileSettingsClassic: React.FC<Props> = ({ currentUser, isAdmin, questions, onUpdateUser, onOpenAuth, onLogout, onOpenAdmin, onOpenOffline }) => {
  const look = useAppearance();
  const [active, setActive] = useState<string>('gorunum');
  const [autoReveal, setAutoReveal] = useState(autoRevealEnabled);
  const [preview, setPreview] = useState(false);

  // Bölüm menüsünde etkin bölüm: kaydırmayla izlenir
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

  const modeName = MODE_LABELS[look.mode];
  const sections = SECTIONS;

  return (
    <div className="ui-page is-wide">
    <div className="ayr">
      <nav className="ayr-nav" aria-label="Ayar bölümleri">
        <div className="ayr-me">
          <span className="ayr-av" aria-hidden="true">
            {currentUser?.photoURL ? <img src={currentUser.photoURL} alt="" /> : currentUser ? initialsOf(currentUser) : <UserRound />}
          </span>
          <span className="ayr-me-t">
            <strong>{currentUser ? currentUser.displayName || currentUser.email?.split('@')[0] : 'Misafir'}</strong>
            <span>{currentUser ? currentUser.email : 'Giriş yapmadın'}</span>
          </span>
        </div>
        <div className="ayr-links">
          {sections.map(({ id, label, icon: Icon }) => (
            <a
              key={id}
              href={`#${id}`}
              aria-current={active === id ? 'true' : undefined}
              onClick={(e) => {
                e.preventDefault();
                document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
                setActive(id);
              }}
            >
              <Icon strokeWidth={2} aria-hidden />
              {label}
            </a>
          ))}
        </div>
      </nav>

      <div className="ayr-main">
        <header className="ayr-head">
          <h1>Profil ve ayarlar</h1>
          <p>Görünüm ayarları bu cihazda saklanır; her temanın paleti ayrı hatırlanır.</p>
        </header>

        <section id="gorunum" className="ayr-sec" aria-labelledby="ayr-gorunum-h">
          <h2 id="ayr-gorunum-h" className="ayr-h1">Görünüm</h2>

          <div className="ayr-block">
            <h3 id="ayr-tema-h">Tema</h3>
            <div role="radiogroup" aria-labelledby="ayr-tema-h" className="ayr-themes">
              {(['light', 'sepia', 'dark'] as ThemeMode[]).map((m) => {
                const Icon = MODE_ICONS[m];
                const sw = findPalette(m, look.palettes[m]).swatch;
                const on = look.mode === m;
                return (
                  <button key={m} type="button" role="radio" aria-checked={on} className="ayr-opt ayr-theme" onClick={() => look.set({ mode: m })}>
                    <span className="ayr-dot" aria-hidden="true" style={{ '--sw-bg': sw[0], '--sw-accent': sw[2] } as React.CSSProperties} />
                    <Icon aria-hidden strokeWidth={2} />
                    {MODE_LABELS[m]}
                  </button>
                );
              })}
            </div>
            {look.mode === 'sepia' && <p className="ayr-foot">Sarı tema uzun okuma için: kâğıt tonu, düşük mavi ışık.</p>}
          </div>

          <div className="ayr-block">
            <h3 id="ayr-palet-h">Palet · {modeName}</h3>
            <div role="radiogroup" aria-labelledby="ayr-palet-h" className="ayr-pals">
              {palettesFor(look.mode).map(({ id: p }) => {
                const info = PALETTE_INFO[look.mode][p];
                const on = look.palette === p;
                return (
                  <button key={p} type="button" role="radio" aria-checked={on} title={info.hint} className="ayr-opt ayr-pal" onClick={() => look.set({ palette: p })}>
                    <PaletteSwatch colors={info.swatch} />
                    <span className="n">{info.name}</span>
                    {on && <Check className="ayr-tick" strokeWidth={3} aria-hidden />}
                  </button>
                );
              })}
            </div>
            <p className="ayr-foot">{PALETTE_INFO[look.mode][look.palette]?.hint}</p>
          </div>

          {(() => {
            const accents = findPalette(look.mode, look.palette).accents;
            if (!accents) return null;
            return (
              <div className="ayr-block">
                <h3 id="ayr-vurgu-h">Vurgu rengi · {PALETTE_INFO[look.mode][look.palette]?.name}</h3>
                <div role="radiogroup" aria-labelledby="ayr-vurgu-h" className="ayr-accents">
                  {accents.map((a) => {
                    const on = look.accent === a.id;
                    return (
                      <button key={a.id} type="button" role="radio" aria-checked={on} className="ayr-acc" onClick={() => look.set({ accent: a.id })}
                        style={{ '--acc': a.accent, '--acc-on': a.on } as React.CSSProperties}>
                        <span className="ayr-acc-dot" aria-hidden>{on && <Check strokeWidth={3.2} />}</span>
                        <span className="ayr-acc-n">{a.name}</span>
                      </button>
                    );
                  })}
                </div>
                <p className="ayr-foot">Düğmeler, seçili sekmeler ve vurgular bu renge geçer; zemin aynı kalır.</p>
              </div>
            );
          })()}

          <GorunumEkleri look={look} />

          <div className="ayr-block">
            <h3 id="ayr-duzen-h">Görüntüleme modu</h3>
            <div role="radiogroup" aria-labelledby="ayr-duzen-h" className="ayr-modes">
              {LAYOUT_CHOICES.map((c) => {
                const on = look.layout === c.id;
                return (
                  <button key={c.id} type="button" role="radio" aria-checked={on} className="ayr-opt ayr-mode" onClick={() => look.set({ layout: c.id })}>
                    <span className={`lm-thumb is-${c.id}`} aria-hidden="true"><i /><i /><i /><i /></span>
                    <strong>{LAYOUT_LABELS[c.id]}</strong>
                    <span>{c.hint}</span>
                  </button>
                );
              })}
            </div>
            <p className="ayr-foot">Menünün yeri, içerik genişliği ve kartların yerleşimi değişir. Telefonda üç mod da tek sütundur.</p>
          </div>

          <div className="ayr-list">
            <div className="ayr-row">
              <span className="ayr-row-t">
                <b id="ayr-yog-h">Yoğunluk</b>
                <span>Yazı ölçeği, boşluklar ve satır yükseklikleri birlikte değişir; dokunmatikte düğmeler küçülmez.</span>
              </span>
              <Segmented<Density>
                label="Yoğunluk"
                value={look.density}
                onChange={(d) => look.set({ density: d })}
                options={(['compact', 'normal', 'wide'] as Density[]).map((d) => ({ value: d, label: DENSITY_LABELS[d] }))}
              />
            </div>
            <div className="ayr-row is-sub">
              <button type="button" className="ayr-disc" aria-expanded={preview} aria-controls="ayr-yog-pv" onClick={() => setPreview((v) => !v)}>
                <ChevronDown aria-hidden className={preview ? 'is-open' : ''} />
                {preview ? 'Önizlemeyi gizle' : 'Yoğunluk önizlemesi'}
              </button>
            </div>
            <div id="ayr-yog-pv" className="ayr-pv" hidden={!preview}>
              <DensityPreview />
            </div>
            <div className="ayr-row" hidden={look.design === 'v10'}>
              <span className="ayr-row-t">
                <b>Okuma yazısı</b>
                <span>Soru kökü, ders anlatımı ve notlar bu yazıyla ve boyutla gösterilir.</span>
              </span>
              <span style={{ display: 'flex', gap: 8, flexWrap: 'wrap', justifyContent: 'flex-end' }}>
                <Segmented<ReadingFont> label="Okuma yazısı" value={look.reading} onChange={(v) => look.set({ reading: v })}
                  options={READING_ORDER.map((v) => ({ value: v, label: READING_LABELS[v] }))} />
                <TextSizeSlider />
              </span>
            </div>
            <div className="ayr-row" hidden={look.design === 'v10'}>
              <span className="ayr-row-t">
                <b>Süzgeç modu</b>
                <span>Basit: yalnız hızlı süzgeç hapları. Gelişmiş: tüm süzgeçler ve sıralamalar her zaman görünür.</span>
              </span>
              <Segmented<FilterMode> label="Süzgeç modu" value={look.filters} onChange={(v) => look.set({ filters: v })}
                options={(['basit', 'gelismis'] as FilterMode[]).map((v) => ({ value: v, label: FILTER_MODE_LABELS[v] }))} />
            </div>
            <div className="ayr-row" hidden={look.design === 'v10'}>
              <span className="ayr-row-t">
                <b>Soru etiketlerini göster</b>
                <span>Çıkmış ve örnek soru kartlarındaki işaret etiketleri. Kapalıyken yalnız soru ve şıklar görünür.</span>
              </span>
              <Switch label="Soru etiketlerini göster" checked={look.qtags} onChange={(on) => look.set({ qtags: on })} />
            </div>
            <div className="ayr-row">
              <span className="ayr-row-t">
                <b>Çıkmış soru kartı</b>
                <span>Tam: her şey açık. Katlanır: yalnız soru kökü ve künye, şıklar dokununca. Dar şıklar: sıkı satırlar.</span>
              </span>
              <Segmented<QCardMode> label="Çıkmış soru kartı" value={look.qcard.mode} onChange={(v) => look.set({ qcard: { mode: v } })}
                options={(['tam', 'katlanir', 'dar'] as QCardMode[]).map((v) => ({ value: v, label: QCARD_MODE_LABELS[v] }))} />
            </div>
            {([['kurul', 'Kurul bilgisi'], ['ders', 'Ders bilgisi'], ['yil', 'Sene bilgisi'], ['aciklama', 'Açıklama'], ['sikAciklama', 'Şık açıklaması']] as [keyof Omit<QCardPrefs, 'mode'>, string][]).map(([k, l]) => (
              <div key={k} className="ayr-row is-sub">
                <span className="ayr-row-t"><b>{l}</b></span>
                <Switch label={l} checked={look.qcard[k]} onChange={(on) => look.set({ qcard: { [k]: on } })} />
              </div>
            ))}
            <div className="ayr-row">
              <span className="ayr-row-t">
                <b>Hareketi azalt</b>
                <span>Geçiş ve canlandırmalar kapanır; sayfalar anında değişir.</span>
              </span>
              <Switch label="Hareketi azalt" checked={look.motion === 'reduced'} onChange={(on) => look.set({ motion: on ? 'reduced' : 'full' })} />
            </div>
            <div className="ayr-row">
              <span className="ayr-row-t">
                <b>Açılan öğeye otomatik kaydır</b>
                <span>Açılan içerik (açıklama, kart, menü bölümü) ekran dışında kalırsa görünür alana getirir.</span>
              </span>
              <Switch label="Açılan öğeye otomatik kaydır" checked={autoReveal} onChange={(on) => { setAutoReveal(on); setAutoRevealEnabled(on); }} />
            </div>
            <div className="ayr-row">
              <span className="ayr-row-t">
                <b>Performans modu</b>
                <span>Sesli ders, soru çözücü ve PDF'e odaklanır: yan özellikler ve ağır efektler kapanır, PDF'ler cihazda tutulur, açılış hızlanır. Sayfa yeniden yüklenir.</span>
              </span>
              <Switch label="Performans modu" checked={performansModu()} onChange={performansModuAyarla} />
            </div>
            <div className="ayr-row">
              <span className="ayr-row-t">
                <b>TV modu</b>
                <span>TV'de kendiliğinden açılır. Sesli dersler listesiyle başlar, kumanda tuşları çalışır, PDF düşük çözünürlükte hızlı çizilir.</span>
              </span>
              <Switch label="TV modu" checked={tvModu()} onChange={tvModuAyarla} />
            </div>
          </div>
        </section>

        <ProfileSection currentUser={currentUser} questions={questions} onUpdateUser={onUpdateUser} onOpenAuth={onOpenAuth} />

        <Section id="hesap" title="Hesap ve veri">
          <div className="ui-group">
            <UserDataSyncRow />
            <ArkaPlanRow />
            <Row icon={Database} iconBg="var(--color-clinic)" title="Çevrimdışı veritabanı" sub="Soruları, sözlüğü ve kartları cihaza indir" onClick={onOpenOffline} />
            <NotesSyncRow />
            <ProgressResetRow />
            <Row icon={Compass} iconBg="var(--color-accent)" title="Tanıtım turu" sub="Sayfaları ve özellikleri yeniden gez" onClick={startWelcomeTour} />
            <Row icon={Compass} iconBg="var(--color-accent)" title="Tanıtım videoları" sub="Sesli ders, soru çözücü, oyunlar ve daha fazlası" onClick={() => window.dispatchEvent(new CustomEvent('medsoru:tanitim'))} />
            <Row icon={Compass} iconBg="var(--color-accent)" title="Öğren turu" sub="Ders kitaplığı ve etkileşim türleri" onClick={onLearnTour} />
            {isAdmin && <Row icon={ShieldCheck} iconBg="var(--color-warn)" title="Yönetim konsolu" sub="Taslaklar, moderasyon, sistem" onClick={onOpenAdmin} />}
            {currentUser ? (
              <button type="button" className="ui-row has-icon" onClick={onLogout}>
                <span className="ui-ico" style={{ '--ico-bg': 'var(--color-bad)', '--ico-fg': 'var(--color-on-solid)' } as React.CSSProperties}>
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

/** Palet önizlemesi: zemin · yüzey · vurgu üç küçük kare (renkler palet kaydından gelir). */
const PaletteSwatch: React.FC<{ colors: [string, string, string] }> = ({ colors }) => (
  <span className="ayr-sw" aria-hidden="true">
    {colors.map((c, i) => <i key={i} style={{ '--sw': c } as React.CSSProperties} />)}
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
