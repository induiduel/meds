import React, { useEffect, useState } from 'react';
import { Sheet } from './ui/Sheet';
import { X, AlertCircle, CheckCircle2, Eye, EyeOff, ShieldCheck, ArrowLeft, Loader2, Mail, Lock, User, Hash, Activity } from 'lucide-react';
import { Segmented } from './ui/kit';
import { registerWithEmailPassword, loginWithEmailPassword, googleSignIn, ADMIN_EMAIL, AppUser } from '../services/auth';
import { validateNamePolicy } from '../utils/namePolicy';

/**
 * Giriş / kayıt kartı (kompakt). Tanıtım akışının son adımında gömülü, diğer yerlerde katmanlı pencere olarak açılır.
 * Önce Google (tek dokunuş), sonra e-posta formu; yönetici girişi altta küçük bağlantı.
 * E-posta hesabı Firebase Authentication'da gerçekten oluşturulur/doğrulanır (sahte oturum yok).
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

const GoogleMark = () => (
  <svg viewBox="0 0 24 24" className="w-[18px] h-[18px]" aria-hidden="true">
    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.27-4.74 3.27-8.1z" />
    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84A11 11 0 0 0 12 23z" />
    <path fill="#FBBC05" d="M5.84 14.1A6.6 6.6 0 0 1 5.5 12c0-.73.13-1.44.34-2.1V7.06H2.18A11 11 0 0 0 1 12c0 1.77.43 3.45 1.18 4.94l3.66-2.84z" />
    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1A11 11 0 0 0 2.18 7.06l3.66 2.84C6.71 7.31 9.14 5.38 12 5.38z" />
  </svg>
);

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
  const [busy, setBusy] = useState<'' | 'google' | 'form'>('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      setMode(initialMode);
      setError(null);
      setSuccess(null);
    }
  }, [isOpen, initialMode]);

  useEffect(() => {
    if (!isOpen || embedded || mandatory) return;
    const esc = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
    document.addEventListener('keydown', esc);
    return () => document.removeEventListener('keydown', esc);
  }, [isOpen, embedded, mandatory, onClose]);

  if (!isOpen) return null;

  const host = typeof window !== 'undefined' ? window.location.hostname : '';

  const finish = (user: AppUser, token?: string | null, msg = 'Giriş yapıldı') => {
    setSuccess(msg);
    setTimeout(() => {
      onAuthSuccess(user, token);
      onClose();
    }, 350);
  };

  const googleError = (err: any) => {
    const code = String(err?.code || err?.message || '');
    if (code.includes('unauthorized-domain')) return `Bu adres (${host}) Google girişi için yetkili değil. nofrostlife.com.tr üzerinden deneyin.`;
    if (code.includes('popup-blocked')) return 'Tarayıcı açılır pencereyi engelledi. Engelleyiciyi kapatıp tekrar deneyin.';
    if (code.includes('popup-closed') || code.includes('cancelled-popup')) return 'Google penceresi kapatıldı. Tekrar deneyin.';
    if (code.includes('network')) return 'Bağlantı kurulamadı. İnternetinizi kontrol edin.';
    return 'Google ile giriş yapılamadı. Tekrar deneyin.';
  };

  const onGoogle = async (admin = false) => {
    setError(null);
    setBusy('google');
    try {
      const r = await googleSignIn(admin ? { preferRedirect: false } : undefined);
      if (!r) return; // yönlendirme ile devam ediyor
      if (admin && r.user.email?.toLowerCase() !== ADMIN_EMAIL.toLowerCase()) {
        setError('Bu Google hesabının yönetici yetkisi yok.');
        return;
      }
      finish(r.user, r.accessToken, admin ? 'Yönetici girişi yapıldı' : 'Google ile giriş yapıldı');
    } catch (err: any) {
      setError(googleError(err));
    } finally {
      setBusy('');
    }
  };

  const onLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setBusy('form');
    try {
      finish(await loginWithEmailPassword(email, password));
    } catch (err: any) {
      setError(err?.message || 'Giriş yapılamadı.');
    } finally {
      setBusy('');
    }
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
      setError(err?.message || 'Yönetici şifresi doğrulanamadı.');
    } finally {
      setBusy('');
    }
  };

  const disabled = busy !== '' || Boolean(success);
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
            onChange={(m) => { setMode(m); setError(null); }}
            options={[{ value: 'login', label: 'Giriş yap' }, { value: 'register', label: 'Kayıt ol' }]}
          />

          <button type="button" onClick={() => onGoogle(false)} disabled={disabled} className="au-google">
            {busy === 'google' ? <Loader2 className="au-spin" aria-hidden /> : <GoogleMark />}
            Google ile devam et
          </button>

          <div className="au-or" aria-hidden="true"><span>ya da e-posta ile</span></div>

          <form key={mode} onSubmit={mode === 'login' ? onLogin : onRegister} className="au-form" noValidate>
            {mode === 'register' && (
              <div className="au-row">
                {field({ id: 'au-name', label: 'Ad soyad', icon: User, value: displayName, set: setDisplayName, auto: 'name' })}
                {field({ id: 'au-num', label: 'Öğrenci no', icon: Hash, value: studentNumber, set: (v) => setStudentNumber(v.replace(/\D/g, '')), mode: 'numeric', auto: 'off' })}
              </div>
            )}
            {field({ id: 'au-email', label: 'E-posta', icon: Mail, value: email, set: setEmail, type: 'email', auto: 'email', mode: 'email' })}
            {field({
              id: 'au-pass', label: 'Şifre', icon: Lock, value: password, set: setPassword, type: showPass ? 'text' : 'password',
              auto: mode === 'login' ? 'current-password' : 'new-password', end: passToggle,
              hint: mode === 'register' ? (password.length >= 6 ? '✓ Yeterli uzunlukta' : 'En az 6 karakter') : undefined,
            })}
            <button type="submit" disabled={disabled} className="au-submit">
              {busy === 'form' ? <Loader2 className="au-spin" aria-hidden /> : null}
              {mode === 'login' ? 'Giriş yap' : 'Kayıt ol'}
            </button>
          </form>
        </>
      ) : (
        <div className="au-form">
          <button type="button" onClick={() => onGoogle(true)} disabled={disabled} className="au-google">
            {busy === 'google' ? <Loader2 className="au-spin" aria-hidden /> : <GoogleMark />}
            Google ile yönetici girişi
          </button>
          <div className="au-or" aria-hidden="true"><span>ya da şifre ile</span></div>
          <form onSubmit={onAdminPassword} className="au-form">
            {field({ id: 'au-admin', label: 'Yönetici şifresi', icon: ShieldCheck, value: adminPassword, set: setAdminPassword, type: 'password', auto: 'current-password' })}
            <button type="submit" disabled={disabled || !adminPassword} className="au-submit">Giriş</button>
          </form>
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
        <button type="button" onClick={() => { setMode(mode === 'admin' ? 'login' : 'admin'); setError(null); }}>
          {mode === 'admin' ? (<><ArrowLeft aria-hidden /> Öğrenci girişi</>) : 'Yönetici'}
        </button>
      </footer>
    </div>
  );

  if (embedded) return card;
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
        {card}
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
        {card}
      </div>
    </div>
  );
};
