import React, { useEffect, useState } from 'react';
import { Sheet } from './ui/Sheet';
import { X, AlertCircle, CheckCircle2, Eye, EyeOff, ShieldCheck, ArrowLeft, Loader2, Mail, Lock, User, Hash, Activity } from 'lucide-react';
import { Segmented } from './ui/kit';
import { registerWithEmailPassword, loginWithEmailPassword, sifreBelirlemeGerekli, ADMIN_EMAIL, AppUser } from '../services/auth';
import { validateNamePolicy } from '../utils/namePolicy';
import { useAppearance } from '../utils/appearance';
import { AuthCardV12 } from './v12/AuthV12';
import { EpostaBaglantiGiris, KodAmaci } from './EpostaBaglantiGiris';

/**
 * Giriş / kayıt kartı (kompakt). Tanıtım akışının son adımında gömülü, diğer yerlerde katmanlı pencere olarak açılır.
 * E-posta + şifre formu; altında e-posta kodu akışı (şifre belirle / şifresiz giriş); yönetici girişi altta küçük bağlantı.
 * Hesap MeDSor'un kendi kimlik sisteminde (Oracle meds-pg) gerçekten oluşturulur/doğrulanır (sahte oturum yok).
 * Google ile giriş 2026-11-02'de kaldırıldı (Google/Firebase projesi askıya alındı).
 */
interface UserAuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAuthSuccess: (user: AppUser, token?: string | null) => void;
  initialMode?: 'login' | 'register' | 'admin';
  mandatory?: boolean;
  /** Tanıtım akışının içinde, katmansız çizilir */
  embedded?: boolean;
}

type Mode = 'login' | 'register' | 'admin';

export const UserAuthModal: React.FC<UserAuthModalProps> = ({
  isOpen,
  onClose,
  onAuthSuccess,
  initialMode = 'register',
  mandatory = false,
  embedded = false,
}) => {
  const [mode, setMode] = useState<Mode>(initialMode);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPass, setShowPass] = useState(false);
  const [displayName, setDisplayName] = useState('');
  const [studentNumber, setStudentNumber] = useState('');
  const [adminPassword, setAdminPassword] = useState('');
  const [busy, setBusy] = useState<'' | 'form'>('');
  const [kodAkisi, setKodAkisi] = useState<KodAmaci | null>(null);
  const [kodUyari, setKodUyari] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      setMode(initialMode);
      setKodAkisi(null);
      setKodUyari(null);
      setError(null);
      setSuccess(null);
    }
  }, [isOpen, initialMode]);

  const v12 = useAppearance().design === 'v12';

  useEffect(() => {
    if (!isOpen || embedded || mandatory) return;
    const esc = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
    document.addEventListener('keydown', esc);
    return () => document.removeEventListener('keydown', esc);
  }, [isOpen, embedded, mandatory, onClose]);

  if (!isOpen) return null;

  const finish = (user: AppUser, token?: string | null, msg = 'Giriş yapıldı') => {
    setSuccess(msg);
    setTimeout(() => {
      onAuthSuccess(user, token);
      onClose();
    }, 350);
  };

  /** Kod akışıyla (şifre belirle / şifresiz giriş) açılan oturum */
  const onKodGiris = (user: AppUser, msg: string) => {
    if (mode === 'admin' && user.email?.toLowerCase() !== ADMIN_EMAIL.toLowerCase()) {
      setError('Bu hesabın yönetici yetkisi yok.');
      return;
    }
    finish(user, null, msg);
  };

  const onLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setBusy('form');
    try {
      finish(await loginWithEmailPassword(email, password));
    } catch (err: any) {
      if (sifreBelirlemeGerekli(err)) {
        // Eski giriş sisteminden taşınan hesap: yönetici onaylı şifre belirleme açılır (hata yerine yönlendirme)
        if (err?.veri?.email && !email.includes('@')) setEmail(err.veri.email);
        setKodUyari(err?.message || null);
        setKodAkisi('talep');
        return;
      }
      setError(err?.message || 'Giriş yapılamadı.');
    } finally {
      setBusy('');
    }
  };

  const onResetPassword = () => {
    setError(null);
    setSuccess(null);
    setKodUyari(null);
    setKodAkisi('talep');
  };

  const onRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    const nameCheck = validateNamePolicy(displayName, { adminEmail: email });
    if (!nameCheck.isValid) {
      setError(nameCheck.errorMessage || 'Geçersiz ad soyad.');
      return;
    }
    const num = studentNumber.replace(/\D/g, '');
    if (num.length < 5) {
      setError('Öğrenci numaranızı girin.');
      return;
    }
    setBusy('form');
    try {
      finish(await registerWithEmailPassword(email, password, displayName.trim(), num), null, 'Kayıt tamamlandı, giriş yapıldı');
    } catch (err: any) {
      if (sifreBelirlemeGerekli(err)) {
        setMode('login');
        setKodUyari(err?.message || null);
        setKodAkisi('talep');
        return;
      }
      setError(err?.message || 'Kayıt yapılamadı.');
    } finally {
      setBusy('');
    }
  };

  const onAdminPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setBusy('form');
    try {
      finish(await loginWithEmailPassword(ADMIN_EMAIL, adminPassword), null, 'Yönetici girişi yapıldı');
    } catch (err: any) {
      if (sifreBelirlemeGerekli(err)) {
        setKodUyari('Yönetici hesabının şifresi henüz belirlenmedi. E-postayla kod alabilir ya da kendi bilgisayarındaki yönetim panelinden (Kullanıcılar › Şifre talepleri) talebini onaylayabilirsin.');
        setKodAkisi('talep');
        return;
      }
      setError(err?.message || 'Yönetici şifresi doğrulanamadı.');
    } finally {
      setBusy('');
    }
  };

  const disabled = busy !== '';
  const inSheet = !embedded;

  /** Yüzen etiketli, ikonlu alan: boşken etiket yer tutucu gibi durur, odak/doluyken yukarı küçülür. */
  const field = (o: {
    id: string; label: string; icon: React.ElementType; value: string; set: (v: string) => void;
    type?: string; auto?: string; mode?: 'numeric' | 'email'; end?: React.ReactNode; hint?: string;
  }) => {
    const Icon = o.icon;
    return (
      <label className={`au-field ${o.value ? 'has-val' : ''}`} htmlFor={o.id}>
        <Icon className="au-ic" aria-hidden />
        <input
          id={o.id}
          type={o.type || 'text'}
          value={o.value}
          onChange={(e) => o.set(e.target.value)}
          autoComplete={o.auto}
          inputMode={o.mode}
          placeholder=" "
          required
          disabled={disabled}
        />
        <span className="au-lbl">{o.label}</span>
        {o.end}
        {o.hint && <small className="au-hint">{o.hint}</small>}
      </label>
    );
  };

  const passToggle = (
    <button type="button" onClick={() => setShowPass((v) => !v)} className="au-eye" aria-label={showPass ? 'Şifreyi gizle' : 'Şifreyi göster'}>
      {showPass ? <EyeOff aria-hidden /> : <Eye aria-hidden />}
    </button>
  );

  const card = (
    <div className={`au ${embedded ? 'is-embedded' : ''}`}>
      <header className="au-head">
        <span className="au-mark" aria-hidden><Activity strokeWidth={2.4} /></span>
        <div className="au-titles">
          <h2>{mode === 'admin' ? 'Yönetici girişi' : mode === 'login' ? 'Tekrar hoş geldin' : 'Hesap oluştur'}</h2>
          <p>{mode === 'admin' ? 'Yönetim konsoluna erişim' : 'Katkıların adınla görünsün; soru eklemek için giriş şart değil.'}</p>
        </div>
        {!embedded && !mandatory && (
          <button type="button" onClick={onClose} className="au-close" aria-label="Kapat"><X aria-hidden /></button>
        )}
      </header>

      {mode !== 'admin' ? (
        <>
          <Segmented<'login' | 'register'>
            className="au-seg"
            label="Giriş ya da kayıt"
            value={mode === 'register' ? 'register' : 'login'}
            onChange={(m) => { setMode(m); setError(null); setSuccess(null); }}
            options={[{ value: 'login', label: 'Giriş yap' }, { value: 'register', label: 'Kayıt ol' }]}
          />

          <form key={mode} onSubmit={mode === 'login' ? onLogin : onRegister} className="au-form" noValidate>
            {mode === 'register' && (
              <div className="au-row">
                {field({ id: 'au-name', label: 'Ad soyad', icon: User, value: displayName, set: setDisplayName, auto: 'name' })}
                {field({ id: 'au-num', label: 'Öğrenci no', icon: Hash, value: studentNumber, set: (v) => setStudentNumber(v.replace(/\D/g, '')), mode: 'numeric', auto: 'off' })}
              </div>
            )}
            {field({ id: 'au-email', label: mode === 'login' ? 'E-posta ya da öğrenci no' : 'E-posta', icon: Mail, value: email, set: setEmail, type: mode === 'login' ? 'text' : 'email', auto: mode === 'login' ? 'username' : 'email', mode: mode === 'login' ? undefined : 'email' })}
            {field({
              id: 'au-pass', label: 'Şifre', icon: Lock, value: password, set: setPassword, type: showPass ? 'text' : 'password',
              auto: mode === 'login' ? 'current-password' : 'new-password', end: passToggle,
              hint: mode === 'register' ? (password.length >= 6 ? '✓ Yeterli uzunlukta' : 'En az 6 karakter') : undefined,
            })}
            {mode === 'login' && (
              <div className="flex justify-end -mt-1 mb-1">
                <button
                  type="button"
                  onClick={onResetPassword}
                  disabled={disabled}
                  className="text-xs font-medium underline opacity-80 hover:opacity-100"
                >
                  Şifremi unuttum / Şifre tanımla
                </button>
              </div>
            )}
            <button type="submit" disabled={disabled} className="au-submit">
              {busy === 'form' ? <Loader2 className="au-spin" aria-hidden /> : null}
              {mode === 'login' ? 'Giriş yap' : 'Kayıt ol'}
            </button>
          </form>
          {mode === 'login' && <EpostaBaglantiGiris email={email} setEmail={setEmail} disabled={disabled} acik={kodAkisi} setAcik={setKodAkisi} onGiris={onKodGiris} uyari={kodUyari} />}
        </>
      ) : (
        <div className="au-form">
          <form onSubmit={onAdminPassword} className="au-form">
            {field({ id: 'au-admin', label: 'Yönetici şifresi', icon: ShieldCheck, value: adminPassword, set: setAdminPassword, type: 'password', auto: 'current-password' })}
            <button type="submit" disabled={disabled || !adminPassword} className="au-submit">Giriş</button>
          </form>
          <EpostaBaglantiGiris email={ADMIN_EMAIL} setEmail={() => {}} sabitEposta={ADMIN_EMAIL} disabled={disabled} acik={kodAkisi} setAcik={setKodAkisi} onGiris={onKodGiris} uyari={kodUyari} />
        </div>
      )}

      {error && (
        <p role="alert" className="au-msg is-bad"><AlertCircle aria-hidden /> {error}</p>
      )}
      {success && (
        <p role="status" className="au-msg is-ok"><CheckCircle2 aria-hidden /> {success}</p>
      )}

      <footer className="au-foot">
        <a href="/sartlar" target="_blank" rel="noopener noreferrer">Kullanım şartları</a>
        <i aria-hidden>·</i>
        <a href="/policy" target="_blank" rel="noopener noreferrer">Gizlilik</a>
        <i aria-hidden>·</i>
        <button type="button" onClick={() => { setMode(mode === 'admin' ? 'login' : 'admin'); setKodAkisi(null); setKodUyari(null); setError(null); setSuccess(null); }}>
          {mode === 'admin' ? (<><ArrowLeft aria-hidden /> Öğrenci girişi</>) : 'Yönetici'}
        </button>
      </footer>
    </div>
  );

  const body = v12 ? (
    <AuthCardV12
      mode={mode}
      onMode={(m) => { setMode(m); setKodAkisi(null); setKodUyari(null); setError(null); setSuccess(null); }}
      embedded={embedded}
      closable={!embedded && !mandatory}
      onClose={onClose}
      busy={busy}
      disabled={disabled}
      error={error}
      success={success}
      email={email}
      setEmail={setEmail}
      password={password}
      setPassword={setPassword}
      showPass={showPass}
      onTogglePass={() => setShowPass((v) => !v)}
      displayName={displayName}
      setDisplayName={setDisplayName}
      studentNumber={studentNumber}
      setStudentNumber={(v) => setStudentNumber(v.replace(/\D/g, ''))}
      adminPassword={adminPassword}
      setAdminPassword={setAdminPassword}
      onLogin={onLogin}
      onRegister={onRegister}
      onAdminPassword={onAdminPassword}
      onResetPassword={onResetPassword}
      loginExtra={<EpostaBaglantiGiris email={email} setEmail={setEmail} disabled={disabled} v12 acik={kodAkisi} setAcik={setKodAkisi} onGiris={onKodGiris} uyari={kodUyari} />}
      adminExtra={<EpostaBaglantiGiris email={ADMIN_EMAIL} setEmail={() => {}} sabitEposta={ADMIN_EMAIL} disabled={disabled} v12 acik={kodAkisi} setAcik={setKodAkisi} onGiris={onKodGiris} uyari={kodUyari} />}
    />
  ) : card;

  if (embedded) return body;
  if (inSheet) {
    return (
      <Sheet
        open
        onClose={() => !mandatory && onClose()}
        hideClose
        bare
        width={420}
        label="Giriş ve kayıt"
      >
        {body}
      </Sheet>
    );
  }
  return (
    <div
      className="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-3 sm:p-4 bg-[var(--color-scrim)]"
      role="dialog"
      aria-modal="true"
      aria-label="Giriş ve kayıt"
      onClick={() => !mandatory && onClose()}
    >
      <div className="w-full max-w-[380px]" onClick={(e) => e.stopPropagation()}>
        {body}
      </div>
    </div>
  );
};
