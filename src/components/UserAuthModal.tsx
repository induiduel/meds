import React, { useState, useEffect } from 'react';
import { 
  X, 
  LogIn, 
  UserPlus, 
  ShieldCheck, 
  AlertCircle, 
  CheckCircle2, 
  Mail, 
  Lock, 
  User, 
  Hash,
  Globe,
  Copy,
  Check,
  ExternalLink,
  KeyRound,
  ArrowRight,
  RefreshCw,
  Sparkles
} from 'lucide-react';
import { 
  registerWithEmailPassword, 
  loginWithEmailPassword, 
  googleSignIn, 
  setLocalAdminSession,
  ADMIN_EMAIL,
  FIREBASE_CONSOLE_URL,
  FIREBASE_PROJECT_ID,
  AppUser 
} from '../services/auth';

interface UserAuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAuthSuccess: (user: AppUser, token?: string | null) => void;
  initialMode?: 'login' | 'register' | 'admin';
}

export const UserAuthModal: React.FC<UserAuthModalProps> = ({
  isOpen,
  onClose,
  onAuthSuccess,
  initialMode = 'login',
}) => {
  const [mode, setMode] = useState<'login' | 'register' | 'admin'>(initialMode);
  
  // Student form state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [studentNumber, setStudentNumber] = useState('');
  
  // Admin form state
  const [adminAuthMethod, setAdminAuthMethod] = useState<'google' | 'password' | 'bypass'>('google');
  const [adminPassword, setAdminPassword] = useState('');
  
  // Status states
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [domainError, setDomainError] = useState(false);
  const [copiedDomain, setCopiedDomain] = useState(false);

  // Sync mode when initialMode changes
  useEffect(() => {
    if (isOpen) {
      setMode(initialMode);
      setError(null);
      setSuccess(null);
      setDomainError(false);
    }
  }, [isOpen, initialMode]);

  if (!isOpen) return null;

  const currentHostname = typeof window !== 'undefined' ? window.location.hostname : 'localhost';

  const copyDomain = () => {
    navigator.clipboard.writeText(currentHostname);
    setCopiedDomain(true);
    setTimeout(() => setCopiedDomain(false), 2000);
  };

  const handleStudentNumberChange = (val: string) => {
    const numeric = val.replace(/\D/g, '');
    setStudentNumber(numeric);
  };

  // Student Email & Password Login
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setDomainError(false);
    setIsLoading(true);
    try {
      const user = await loginWithEmailPassword(email, password);
      setSuccess('Giriş başarılı!');
      setTimeout(() => {
        onAuthSuccess(user);
        onClose();
      }, 400);
    } catch (err: any) {
      if (err.code === 'auth/wrong-password') {
        setError('Hatalı şifre girdiniz.');
      } else {
        setError(err.message || 'Giriş yapılamadı.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Student Register
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setDomainError(false);
    setIsLoading(true);
    try {
      if (!displayName.trim()) {
        throw new Error('Lütfen adınızı ve soyadınızı giriniz.');
      }
      const cleanNum = studentNumber.replace(/\D/g, '');

      const user = await registerWithEmailPassword(
        email,
        password,
        displayName.trim(),
        cleanNum || undefined
      );

      setSuccess('Kayıt başarılı! Öğrenci hesabınız oluşturuldu.');
      setTimeout(() => {
        onAuthSuccess(user);
        onClose();
      }, 600);
    } catch (err: any) {
      if (err.code === 'auth/email-already-in-use') {
        setError('Bu e-posta adresiyle kayıtlı bir hesap zaten var. Lütfen giriş sekmesinden giriş yapınız.');
      } else if (err.code === 'auth/weak-password') {
        setError('Şifre en az 6 karakter olmalıdır.');
      } else {
        setError(err.message || 'Kayıt işlemi tamamlandı.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Student Google Login
  const handleStudentGoogleLogin = async () => {
    setError(null);
    setDomainError(false);
    setIsLoading(true);
    try {
      const result = await googleSignIn();
      if (result) {
        setSuccess('Google ile giriş başarılı!');
        setTimeout(() => {
          onAuthSuccess(result.user, result.accessToken);
          onClose();
        }, 400);
      }
    } catch (err: any) {
      console.warn('Student Google login error:', err);
      if (
        err.code === 'auth/unauthorized-domain' ||
        err.message?.includes('unauthorized-domain')
      ) {
        setDomainError(true);
        setError(`Bu alan adı (${currentHostname}) henüz Firebase konsolunda yetkilendirilmemiş. Lütfen e-posta ve şifrenizle giriş yapınız veya kayıt olunuz.`);
      } else if (err.code === 'auth/popup-blocked') {
        setError('Açılır pencere (popup) tarayıcınız tarafından engellendi. Lütfen popup engelleyicinizi kapatınız.');
      } else {
        setError(`Google ile giriş yapılamadı: ${err.message || 'Yetkilendirme hatası'}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Admin Google Login (Popup or Redirect)
  const handleAdminGoogleLogin = async (preferRedirect = false) => {
    setError(null);
    setDomainError(false);
    setIsLoading(true);
    try {
      const result = await googleSignIn({ preferRedirect });
      if (result) {
        if (result.user.email?.toLowerCase() !== ADMIN_EMAIL.toLowerCase()) {
          setError(`Giriş yapılan Google hesabı (${result.user.email}) yönetici yetkisine sahip değil. Lütfen ${ADMIN_EMAIL} ile giriş yapınız.`);
          return;
        }
        setSuccess('Yönetici girişi başarılı!');
        setTimeout(() => {
          onAuthSuccess(result.user, result.accessToken);
          onClose();
        }, 400);
      }
    } catch (err: any) {
      console.warn('Admin Google login error:', err);
      if (
        err.code === 'auth/unauthorized-domain' ||
        err.message?.includes('unauthorized-domain')
      ) {
        setDomainError(true);
        setError(`"${currentHostname}" alan adı Firebase Authentication ayarlarında henüz yetkili alan adları listesine eklenmemiş.`);
      } else if (err.code === 'auth/popup-blocked') {
        setError('Açılır pencere (popup) engellendi. Aşağıdaki "Yönlendirme ile Giriş" butonunu kullanabilirsiniz.');
      } else {
        setError(`Google ile giriş yapılamadı: ${err.message || 'Yetkilendirme hatası'}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Admin Email/Password Login
  const handleAdminPasswordLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setDomainError(false);
    setIsLoading(true);
    try {
      const user = await loginWithEmailPassword(ADMIN_EMAIL, adminPassword);
      setSuccess('Yönetici şifre doğrulaması başarılı!');
      setTimeout(() => {
        onAuthSuccess(user);
        onClose();
      }, 400);
    } catch (err: any) {
      setError(err.message || 'Yönetici şifresi doğrulanamadı.');
    } finally {
      setIsLoading(false);
    }
  };

  // Emergency Admin Bypass Login
  const handleEmergencyAdminBypass = () => {
    const user = setLocalAdminSession(ADMIN_EMAIL);
    setSuccess('Yönetici acil oturumu açıldı!');
    setTimeout(() => {
      onAuthSuccess(user, null);
      onClose();
    }, 300);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-fadeIn">
      <div 
        className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-lg overflow-hidden relative max-h-[92vh] flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-teal-900 via-teal-800 to-slate-900 p-5 text-white flex items-center justify-between shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-white/10 text-teal-300">
              {mode === 'admin' ? <ShieldCheck className="w-5 h-5" /> : <User className="w-5 h-5" />}
            </div>
            <div>
              <h3 className="font-bold text-base leading-tight">
                {mode === 'login' ? 'Öğrenci Girişi' : mode === 'register' ? 'Yeni Öğrenci Kaydı' : 'Yönetici Girişi (nofrostlife)'}
              </h3>
              <p className="text-xs text-teal-200/80">
                {mode === 'admin' ? 'nofrostlife@gmail.com ile tam yönetim yetkisi' : 'Sorularınızı yönetin, düzenleyin ve takip edin'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-white/70 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab switchers */}
        <div className="flex border-b border-slate-200 bg-slate-50 text-xs font-semibold shrink-0">
          <button
            onClick={() => { setMode('login'); setError(null); setDomainError(false); }}
            className={`flex-1 py-3 text-center border-b-2 transition-all cursor-pointer ${
              mode === 'login' 
                ? 'border-teal-600 text-teal-900 bg-white font-bold' 
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            Giriş Yap
          </button>
          <button
            onClick={() => { setMode('register'); setError(null); setDomainError(false); }}
            className={`flex-1 py-3 text-center border-b-2 transition-all cursor-pointer ${
              mode === 'register' 
                ? 'border-teal-600 text-teal-900 bg-white font-bold' 
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            Kayıt Ol
          </button>
          <button
            onClick={() => { setMode('admin'); setError(null); setDomainError(false); }}
            className={`flex-1 py-3 text-center border-b-2 transition-all cursor-pointer ${
              mode === 'admin' 
                ? 'border-amber-500 text-amber-900 bg-white font-bold' 
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            Yönetici Girişi
          </button>
        </div>

        {/* Feedback Messages */}
        <div className="p-5 pb-0 shrink-0">
          {error && (
            <div className="bg-rose-50 border border-rose-200 text-rose-800 text-xs p-3 rounded-lg flex items-start gap-2 mb-3">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}
          {success && (
            <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs p-3 rounded-lg flex items-start gap-2 mb-3">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span>{success}</span>
            </div>
          )}
        </div>

        {/* Body content */}
        <div className="p-5 pt-3 overflow-y-auto">
          {/* TAB 1: LOGIN */}
          {mode === 'login' && (
            <div className="space-y-4">
              <form onSubmit={handleLogin} className="space-y-3.5">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    E-posta Adresi
                  </label>
                  <div className="relative">
                    <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                    <input
                      type="email"
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="ornek@universite.edu.tr veya gmail"
                      className="w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-hidden focus:border-teal-600"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Şifre
                  </label>
                  <div className="relative">
                    <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                    <input
                      type="password"
                      required
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                      className="w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-hidden focus:border-teal-600"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-teal-700 hover:bg-teal-800 text-white font-bold py-2.5 rounded-lg text-sm transition-all shadow-sm cursor-pointer disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {isLoading ? <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <LogIn className="w-4 h-4" />}
                  <span>E-posta ile Giriş Yap</span>
                </button>
              </form>

              <div className="relative flex py-1 items-center">
                <div className="grow border-t border-slate-200"></div>
                <span className="shrink mx-3 text-slate-400 text-xs">veya</span>
                <div className="grow border-t border-slate-200"></div>
              </div>

              {/* Student Google login button */}
              <button
                type="button"
                onClick={handleStudentGoogleLogin}
                disabled={isLoading}
                className="w-full bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 font-semibold py-2.5 px-4 rounded-lg text-sm transition-all shadow-xs flex items-center justify-center gap-3 cursor-pointer disabled:opacity-50"
              >
                <svg className="w-4 h-4" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.66v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.15z" />
                  <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.24v3.15C3.26 21.36 7.33 24 12 24z" />
                  <path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.24C.45 8.15 0 9.99 0 12s.45 3.85 1.24 5.42l4.04-3.15z" />
                  <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.24 6.58l4.04 3.15c.95-2.83 3.6-4.98 6.72-4.98z" />
                </svg>
                <span>Google ile Hızlı Giriş Yap</span>
              </button>

              <div className="text-center pt-2">
                <span className="text-xs text-slate-500">Hesabınız yok mu? </span>
                <button
                  type="button"
                  onClick={() => { setMode('register'); setError(null); setDomainError(false); }}
                  className="text-xs font-bold text-teal-700 hover:underline cursor-pointer"
                >
                  Hemen Kayıt Olun
                </button>
              </div>
            </div>
          )}

          {/* TAB 2: REGISTER */}
          {mode === 'register' && (
            <form onSubmit={handleRegister} className="space-y-3.5">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Ad Soyad <span className="text-rose-500">*</span>
                </label>
                <div className="relative">
                  <User className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    required
                    value={displayName}
                    onChange={(e) => setDisplayName(e.target.value)}
                    placeholder="Örn: Dr. Adayı Ahmet Yılmaz"
                    className="w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-hidden focus:border-teal-600"
                  />
                </div>
                <p className="text-[10px] text-slate-500 mt-0.5">
                  Bu isim soru eklerken otomatik hatırlanacaktır.
                </p>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1 flex items-center justify-between">
                  <span>Öğrenci Numarası <span className="text-slate-400 font-normal">(İsteğe bağlı)</span></span>
                  {studentNumber && (
                    <span className={`text-[11px] font-bold px-2 py-0.5 rounded ${studentNumber.length === 11 ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' : 'bg-teal-50 text-teal-800 border border-teal-200'}`}>
                      {studentNumber.length === 11 ? '✓ 11 Haneli Standart No (Geçerli)' : `${studentNumber.length} Hane Girildi (Kabul Edildi ✓)`}
                    </span>
                  )}
                </label>
                <div className="relative">
                  <Hash className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    inputMode="numeric"
                    maxLength={16}
                    value={studentNumber}
                    onChange={(e) => handleStudentNumberChange(e.target.value)}
                    placeholder="Örn: 20241054012"
                    className="w-full pl-9 pr-3 py-2 text-sm font-mono border border-slate-300 rounded-lg focus:outline-hidden focus:border-teal-600"
                  />
                </div>
                <p className="text-[10px] text-slate-400 mt-0.5">
                  Boşluklu veya tireli yapıştırsanız bile otomatik temizlenir.
                </p>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  E-posta Adresi <span className="text-rose-500">*</span>
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Herhangi bir e-posta (üniversite veya kişisel)"
                    className="w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-hidden focus:border-teal-600"
                  />
                </div>
                <p className="text-[10px] text-emerald-700 mt-0.5 font-medium">
                  🎉 İlk soru katkınızda bu adrese resmi teşekkür ve tebrik e-postası iletilecektir (Her kurulda 1 kez).
                </p>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Şifre Belirleyin <span className="text-rose-500">*</span>
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="password"
                    required
                    minLength={6}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Şifrenizi yazın (en az 6 karakter)"
                    className="w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-hidden focus:border-teal-600"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-teal-700 hover:bg-teal-800 text-white font-bold py-2.5 rounded-lg text-sm transition-all shadow-sm cursor-pointer disabled:opacity-50 flex items-center justify-center gap-2 mt-2"
              >
                {isLoading ? <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <UserPlus className="w-4 h-4" />}
                <span>Kayıt Ol ve Giriş Yap</span>
              </button>

              <div className="text-center pt-1">
                <span className="text-xs text-slate-500">Zaten hesabınız var mı? </span>
                <button
                  type="button"
                  onClick={() => { setMode('login'); setError(null); setDomainError(false); }}
                  className="text-xs font-bold text-teal-700 hover:underline cursor-pointer"
                >
                  Giriş Yapın
                </button>
              </div>
            </form>
          )}

          {/* TAB 3: ADMIN MULTI-PATH LOGIN */}
          {mode === 'admin' && (
            <div className="space-y-4">
              <div className="bg-amber-50/80 border border-amber-200/80 rounded-xl p-3 flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-amber-100 text-amber-700 border border-amber-300 flex items-center justify-center shrink-0 mt-0.5">
                  <ShieldCheck className="w-5 h-5" />
                </div>
                <div className="text-xs text-amber-900">
                  <div className="font-bold text-amber-950">Yönetici Hesabı: {ADMIN_EMAIL}</div>
                  <p className="text-[11px] text-amber-800 mt-0.5 leading-relaxed">
                    Google Drive arşivleme, soru silme, yeni kurul ekleme ve limit kontrolleri bu hesaba aittir.
                  </p>
                </div>
              </div>

              {/* Domain Authorization Diagnostic Box (shown if unauthorized-domain error occurred) */}
              {domainError && (
                <div className="bg-rose-50 border border-rose-200 rounded-xl p-3 space-y-2.5 text-xs text-rose-900 animate-fadeIn">
                  <div className="flex items-center gap-2 font-bold text-rose-800">
                    <Globe className="w-4 h-4 text-rose-600 shrink-0" />
                    <span>Firebase Yetkili Alan Adı Gerekiyor</span>
                  </div>
                  <p className="text-[11px] text-rose-800 leading-normal">
                    Google OAuth güvenlik protokolü gereği, <strong className="font-mono bg-rose-100 px-1 py-0.5 rounded">{currentHostname}</strong> alan adının Firebase Konsolu Authorized Domains listesine eklenmesi gerekmektedir.
                  </p>
                  
                  <div className="flex items-center gap-2 bg-white border border-rose-300 rounded p-1.5 font-mono text-slate-900 text-[11px]">
                    <span className="flex-1 font-bold truncate">{currentHostname}</span>
                    <button
                      type="button"
                      onClick={copyDomain}
                      className="px-2 py-1 rounded bg-rose-100 hover:bg-rose-200 text-rose-800 font-sans text-[10px] font-semibold flex items-center gap-1 cursor-pointer shrink-0"
                    >
                      {copiedDomain ? <Check className="w-3 h-3 text-emerald-600" /> : <Copy className="w-3 h-3" />}
                      <span>{copiedDomain ? 'Kopyalandı' : 'Kopyala'}</span>
                    </button>
                  </div>

                  <div className="flex items-center gap-2 pt-1">
                    <a
                      href={FIREBASE_CONSOLE_URL}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 bg-rose-600 hover:bg-rose-700 text-white font-bold py-1.5 px-2.5 rounded-lg text-[11px] flex items-center justify-center gap-1.5 transition-colors"
                    >
                      <span>Firebase Konsolunu Aç</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                    <button
                      type="button"
                      onClick={handleEmergencyAdminBypass}
                      className="flex-1 bg-teal-700 hover:bg-teal-800 text-white font-bold py-1.5 px-2.5 rounded-lg text-[11px] flex items-center justify-center gap-1.5 cursor-pointer shadow-xs"
                    >
                      <KeyRound className="w-3 h-3 text-teal-300" />
                      <span>Hemen Giriş Yap (Bypass)</span>
                    </button>
                  </div>
                </div>
              )}

              {/* Admin Auth Method Switcher */}
              <div className="grid grid-cols-3 gap-1.5 bg-slate-100 p-1 rounded-xl text-[11px] font-bold">
                <button
                  type="button"
                  onClick={() => setAdminAuthMethod('google')}
                  className={`py-1.5 rounded-lg transition-all cursor-pointer ${
                    adminAuthMethod === 'google'
                      ? 'bg-white text-slate-900 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  Google OAuth
                </button>
                <button
                  type="button"
                  onClick={() => setAdminAuthMethod('password')}
                  className={`py-1.5 rounded-lg transition-all cursor-pointer ${
                    adminAuthMethod === 'password'
                      ? 'bg-white text-slate-900 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  Şifre ile
                </button>
                <button
                  type="button"
                  onClick={() => setAdminAuthMethod('bypass')}
                  className={`py-1.5 rounded-lg transition-all cursor-pointer ${
                    adminAuthMethod === 'bypass'
                      ? 'bg-amber-500 text-white shadow-xs'
                      : 'text-amber-800 hover:text-amber-950'
                  }`}
                >
                  ⚡ Acil Erişim
                </button>
              </div>

              {/* Sub-view: Google OAuth */}
              {adminAuthMethod === 'google' && (
                <div className="space-y-2.5 pt-1">
                  <button
                    type="button"
                    onClick={() => handleAdminGoogleLogin(false)}
                    disabled={isLoading}
                    className="w-full bg-white hover:bg-slate-50 border border-slate-300 text-slate-800 font-bold py-2.5 px-4 rounded-xl text-sm transition-all shadow-xs flex items-center justify-center gap-3 cursor-pointer disabled:opacity-50"
                  >
                    <svg className="w-5 h-5 shrink-0" viewBox="0 0 24 24">
                      <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.66v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.15z" />
                      <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.24v3.15C3.26 21.36 7.33 24 12 24z" />
                      <path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.24C.45 8.15 0 9.99 0 12s.45 3.85 1.24 5.42l4.04-3.15z" />
                      <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.24 6.58l4.04 3.15c.95-2.83 3.6-4.98 6.72-4.98z" />
                    </svg>
                    <span>{isLoading ? 'Bağlanılıyor...' : 'Google ile Yönetici Girişi (Popup)'}</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => handleAdminGoogleLogin(true)}
                    disabled={isLoading}
                    className="w-full bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-700 font-semibold py-2 px-3 rounded-lg text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
                  >
                    <RefreshCw className="w-3.5 h-3.5 text-slate-500" />
                    <span>Popup engelleniyorsa: Yönlendirme (Redirect) ile Aç</span>
                  </button>

                  <p className="text-[10px] text-slate-400 text-center">
                    Giriş hesabı mutlaka <strong className="text-slate-600 font-mono">{ADMIN_EMAIL}</strong> olmalıdır.
                  </p>
                </div>
              )}

              {/* Sub-view: Password Login for Admin */}
              {adminAuthMethod === 'password' && (
                <form onSubmit={handleAdminPasswordLogin} className="space-y-3 pt-1">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">
                      Yönetici E-posta
                    </label>
                    <input
                      type="email"
                      disabled
                      value={ADMIN_EMAIL}
                      className="w-full px-3 py-2 text-xs bg-slate-100 border border-slate-300 rounded-lg font-mono text-slate-700"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">
                      Yönetici Şifresi
                    </label>
                    <div className="relative">
                      <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                      <input
                        type="password"
                        required
                        value={adminPassword}
                        onChange={(e) => setAdminPassword(e.target.value)}
                        placeholder="Yönetici şifreniz"
                        className="w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-hidden focus:border-amber-600"
                      />
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={isLoading || !adminPassword}
                    className="w-full bg-amber-600 hover:bg-amber-700 text-white font-bold py-2.5 rounded-lg text-xs transition-all shadow-sm cursor-pointer disabled:opacity-50 flex items-center justify-center gap-2"
                  >
                    {isLoading ? <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <LogIn className="w-4 h-4" />}
                    <span>Şifre ile Yönetici Girişi Yap</span>
                  </button>
                </form>
              )}

              {/* Sub-view: Emergency Bypass */}
              {adminAuthMethod === 'bypass' && (
                <div className="space-y-3 pt-1 bg-amber-50/60 border border-amber-200 rounded-xl p-3.5">
                  <div className="flex items-center gap-2 text-xs font-bold text-amber-950">
                    <Sparkles className="w-4 h-4 text-amber-600" />
                    <span>Geliştirici & Acil Durum Girişi</span>
                  </div>
                  <p className="text-[11px] text-amber-900 leading-relaxed">
                    Firebase alan adı yetkilendirmesi veya Google API kısıtlamalarına takılmadan doğrudan yerel yönetici oturumu açar.
                  </p>
                  <button
                    type="button"
                    onClick={handleEmergencyAdminBypass}
                    className="w-full bg-amber-600 hover:bg-amber-700 text-white font-bold py-2.5 px-4 rounded-xl text-xs transition-all shadow-sm flex items-center justify-center gap-2 cursor-pointer"
                  >
                    <KeyRound className="w-4 h-4" />
                    <span>Yönetici Olarak Giriş Yap ({ADMIN_EMAIL})</span>
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
