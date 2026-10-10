import React, { useEffect, useState } from 'react';
import { X, AlertCircle, CheckCircle2, Eye, EyeOff, ShieldCheck, ArrowLeft, Loader2 } from 'lucide-react';
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

  const input =
    'w-full h-11 px-3 rounded-xl border border-line bg-white text-[16px] sm:text-[14.5px] text-ink placeholder:text-ink-3 outline-none focus:border-accent focus:ring-2 focus:ring-accent/15';
  const label = 'block text-[12.5px] font-semibold text-ink-2 mb-1';
  const disabled = busy !== '' || Boolean(success);

  const card = (
    <div className={`w-full max-w-[380px] mx-auto bg-white rounded-2xl border border-line ${embedded ? '' : 'shadow-xl'} p-4 sm:p-5 flex flex-col gap-3.5`}>
      {!embedded && (
        <div className="flex items-center justify-between -mt-1">
          <h2 className="m-0 text-[16px] font-bold text-ink">{mode === 'admin' ? 'Yönetici girişi' : mode === 'login' ? 'Giriş yap' : 'Kayıt ol'}</h2>
          {!mandatory && (
            <button type="button" onClick={onClose} className="w-9 h-9 -mr-2 inline-flex items-center justify-center rounded-lg text-ink-3 hover:bg-canvas cursor-pointer" aria-label="Kapat">
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      )}

      {mode !== 'admin' ? (
        <>
          <div className="grid grid-cols-2 p-1 rounded-xl bg-canvas" role="tablist" aria-label="Giriş ya da kayıt">
            {(['login', 'register'] as const).map((m) => (
              <button
                key={m}
                type="button"
                role="tab"
                aria-selected={mode === m}
                onClick={() => {
                  setMode(m);
                  setError(null);
                }}
                className={`h-9 rounded-lg text-[13.5px] font-semibold cursor-pointer transition-colors ${mode === m ? 'bg-white text-ink shadow-xs' : 'text-ink-3 hover:text-ink'}`}
              >
                {m === 'login' ? 'Giriş' : 'Kayıt'}
              </button>
            ))}
          </div>

          <button
            type="button"
            onClick={() => onGoogle(false)}
            disabled={disabled}
            className="h-11 rounded-xl border border-line bg-white hover:bg-canvas text-[14.5px] font-semibold text-ink inline-flex items-center justify-center gap-2.5 cursor-pointer disabled:opacity-60"
          >
            {busy === 'google' ? <Loader2 className="w-[18px] h-[18px] animate-spin" /> : <GoogleMark />}
            Google ile devam et
          </button>

          <div className="flex items-center gap-3 text-[12px] text-ink-3" aria-hidden="true">
            <span className="h-px flex-1 bg-line" /> ya da e-posta ile <span className="h-px flex-1 bg-line" />
          </div>

          <form onSubmit={mode === 'login' ? onLogin : onRegister} className="flex flex-col gap-2.5" noValidate>
            {mode === 'register' && (
              <div className="grid grid-cols-1 xs:grid-cols-2 gap-2.5">
                <div>
                  <label className={label} htmlFor="au-name">Ad soyad</label>
                  <input id="au-name" className={input} value={displayName} onChange={(e) => setDisplayName(e.target.value)} autoComplete="name" required />
                </div>
                <div>
                  <label className={label} htmlFor="au-num">Öğrenci no</label>
                  <input id="au-num" className={input} value={studentNumber} onChange={(e) => setStudentNumber(e.target.value.replace(/\D/g, ''))} inputMode="numeric" autoComplete="off" required />
                </div>
              </div>
            )}
            <div>
              <label className={label} htmlFor="au-email">E-posta</label>
              <input id="au-email" className={input} type="email" value={email} onChange={(e) => setEmail(e.target.value)} autoComplete="email" placeholder="ad.soyad@ogr.karabuk.edu.tr" required />
            </div>
            <div>
              <label className={label} htmlFor="au-pass">Şifre</label>
              <div className="relative">
                <input
                  id="au-pass"
                  className={`${input} pr-11`}
                  type={showPass ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
                  placeholder={mode === 'register' ? 'En az 6 karakter' : ''}
                  required
                />
                <button type="button" onClick={() => setShowPass((v) => !v)} className="absolute right-1 top-1 w-9 h-9 inline-flex items-center justify-center rounded-lg text-ink-3 hover:text-ink cursor-pointer" aria-label={showPass ? 'Şifreyi gizle' : 'Şifreyi göster'}>
                  {showPass ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>
            <button type="submit" disabled={disabled} className="h-11 mt-0.5 rounded-xl bg-accent hover:bg-accent-hover text-white text-[14.5px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60">
              {busy === 'form' && <Loader2 className="w-4 h-4 animate-spin" />}
              {mode === 'login' ? 'Giriş yap' : 'Kayıt ol'}
            </button>
          </form>
        </>
      ) : (
        <div className="flex flex-col gap-2.5">
          <p className="m-0 flex items-center gap-1.5 text-[13.5px] font-semibold text-ink">
            <ShieldCheck className="w-4 h-4 text-accent" /> Yönetici girişi
          </p>
          <button type="button" onClick={() => onGoogle(true)} disabled={disabled} className="h-11 rounded-xl border border-line bg-white hover:bg-canvas text-[14.5px] font-semibold text-ink inline-flex items-center justify-center gap-2.5 cursor-pointer disabled:opacity-60">
            {busy === 'google' ? <Loader2 className="w-[18px] h-[18px] animate-spin" /> : <GoogleMark />}
            Google ile yönetici girişi
          </button>
          <form onSubmit={onAdminPassword} className="flex gap-2">
            <input className={input} type="password" value={adminPassword} onChange={(e) => setAdminPassword(e.target.value)} placeholder="ya da yönetici şifresi" autoComplete="current-password" aria-label="Yönetici şifresi" />
            <button type="submit" disabled={disabled || !adminPassword} className="h-11 px-4 rounded-xl bg-accent text-white text-[14px] font-semibold cursor-pointer disabled:opacity-60 shrink-0">Giriş</button>
          </form>
        </div>
      )}

      {error && (
        <p role="alert" className="m-0 flex items-start gap-2 rounded-xl bg-rose-50 text-rose-800 px-3 py-2 text-[13px] leading-snug">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" /> {error}
        </p>
      )}
      {success && (
        <p role="status" className="m-0 flex items-center gap-2 rounded-xl bg-emerald-50 text-emerald-800 px-3 py-2 text-[13px]">
          <CheckCircle2 className="w-4 h-4 shrink-0" /> {success}
        </p>
      )}

      <div className="flex items-center justify-center gap-3 pt-1 border-t border-line text-[11.5px] text-ink-3">
        <a href="/sartlar" target="_blank" rel="noopener noreferrer" className="hover:text-accent underline">Kullanım Şartları</a>
        <span>·</span>
        <a href="/policy" target="_blank" rel="noopener noreferrer" className="hover:text-accent underline">Gizlilik Politikası</a>
      </div>

      <button
        type="button"
        onClick={() => {
          setMode(mode === 'admin' ? 'login' : 'admin');
          setError(null);
        }}
        className="self-center min-h-8 px-2 text-[12px] text-ink-3 hover:text-ink inline-flex items-center gap-1 cursor-pointer"
      >
        {mode === 'admin' ? (<><ArrowLeft className="w-3.5 h-3.5" /> Öğrenci girişine dön</>) : 'Yönetici girişi'}
      </button>
    </div>
  );

  if (embedded) return card;
  return (
    <div
      className="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-3 sm:p-4 bg-slate-900/45"
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
