import React, { useState } from 'react';
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
  Sparkles
} from 'lucide-react';
import { 
  registerWithEmailPassword, 
  loginWithEmailPassword, 
  googleSignIn, 
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
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [studentNumber, setStudentNumber] = useState('');
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleStudentNumberChange = (val: string) => {
    // Only digits, maximum 11 characters
    const numeric = val.replace(/\D/g, '').slice(0, 11);
    setStudentNumber(numeric);
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      const user = await loginWithEmailPassword(email, password);
      setSuccess('Giriş başarılı!');
      setTimeout(() => {
        onAuthSuccess(user);
        onClose();
      }, 500);
    } catch (err: any) {
      if (err.code === 'auth/user-not-found' || err.code === 'auth/invalid-credential') {
        setError('E-posta adresi veya şifre hatalı.');
      } else if (err.code === 'auth/wrong-password') {
        setError('Hatalı şifre girdiniz.');
      } else {
        setError(err.message || 'Giriş yapılamadı.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      if (!displayName.trim()) {
        throw new Error('Lütfen adınızı ve soyadınızı giriniz.');
      }
      if (studentNumber && studentNumber.length !== 11) {
        throw new Error('Öğrenci numarası tam 11 haneli olmalıdır (veya boş bırakınız).');
      }

      const user = await registerWithEmailPassword(
        email,
        password,
        displayName.trim(),
        studentNumber.trim() || undefined
      );

      setSuccess('Kayıt başarılı! Giriş yapıldı.');
      setTimeout(() => {
        onAuthSuccess(user);
        onClose();
      }, 600);
    } catch (err: any) {
      if (err.code === 'auth/email-already-in-use') {
        setError('Bu e-posta adresiyle kayıtlı bir hesap zaten var. Lütfen giriş yapınız.');
      } else if (err.code === 'auth/weak-password') {
        setError('Şifre en az 6 karakter olmalıdır.');
      } else {
        setError(err.message || 'Kayıt sırasında bir hata oluştu.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleAdminGoogleLogin = async () => {
    setError(null);
    setIsLoading(true);
    try {
      const result = await googleSignIn();
      if (result) {
        setSuccess('Yönetici girişi başarılı!');
        setTimeout(() => {
          onAuthSuccess(result.user, result.accessToken);
          onClose();
        }, 500);
      }
    } catch (err: any) {
      setError(err.message || 'Yönetici girişi başarısız oldu.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-fadeIn">
      <div 
        className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-md overflow-hidden relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-teal-900 via-teal-800 to-slate-900 p-5 text-white flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-white/10 text-teal-300">
              {mode === 'admin' ? <ShieldCheck className="w-5 h-5" /> : <User className="w-5 h-5" />}
            </div>
            <div>
              <h3 className="font-bold text-base leading-tight">
                {mode === 'login' ? 'Öğrenci Girişi' : mode === 'register' ? 'Yeni Öğrenci Kaydı' : 'Yönetici Girişi'}
              </h3>
              <p className="text-xs text-teal-200/80">
                {mode === 'admin' ? 'nofrostlife@gmail.com ile Google Girişi' : 'Sorularınızı yönetin, düzenleyin ve takip edin'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-white/70 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab switchers */}
        <div className="flex border-b border-slate-200 bg-slate-50 text-xs font-semibold">
          <button
            onClick={() => { setMode('login'); setError(null); }}
            className={`flex-1 py-3 text-center border-b-2 transition-all cursor-pointer ${
              mode === 'login' 
                ? 'border-teal-600 text-teal-900 bg-white font-bold' 
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            Giriş Yap
          </button>
          <button
            onClick={() => { setMode('register'); setError(null); }}
            className={`flex-1 py-3 text-center border-b-2 transition-all cursor-pointer ${
              mode === 'register' 
                ? 'border-teal-600 text-teal-900 bg-white font-bold' 
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            Kayıt Ol
          </button>
          <button
            onClick={() => { setMode('admin'); setError(null); }}
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
        <div className="p-5 pb-0">
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
        <div className="p-5 pt-3">
          {/* TAB 1: LOGIN */}
          {mode === 'login' && (
            <form onSubmit={handleLogin} className="space-y-4">
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
                <span>Giriş Yap</span>
              </button>

              <div className="text-center pt-2">
                <span className="text-xs text-slate-500">Hesabınız yok mu? </span>
                <button
                  type="button"
                  onClick={() => { setMode('register'); setError(null); }}
                  className="text-xs font-bold text-teal-700 hover:underline cursor-pointer"
                >
                  Hemen Kayıt Olun
                </button>
              </div>
            </form>
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
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  11 Haneli Öğrenci Numarası <span className="text-slate-400 font-normal">(İsteğe bağlı)</span>
                </label>
                <div className="relative">
                  <Hash className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    inputMode="numeric"
                    maxLength={11}
                    value={studentNumber}
                    onChange={(e) => handleStudentNumberChange(e.target.value)}
                    placeholder="Örn: 20241054012"
                    className="w-full pl-9 pr-3 py-2 text-sm font-mono border border-slate-300 rounded-lg focus:outline-hidden focus:border-teal-600"
                  />
                  {studentNumber && (
                    <span className="absolute right-3 top-2.5 text-[11px] font-bold text-slate-400">
                      {studentNumber.length}/11
                    </span>
                  )}
                </div>
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
                    placeholder="Şifrenizi yazın (herhangi bir kısıtlama yok, en az 6 hane)"
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
                  onClick={() => { setMode('login'); setError(null); }}
                  className="text-xs font-bold text-teal-700 hover:underline cursor-pointer"
                >
                  Giriş Yapın
                </button>
              </div>
            </form>
          )}

          {/* TAB 3: ADMIN GOOGLE LOGIN */}
          {mode === 'admin' && (
            <div className="space-y-4 py-2 text-center">
              <div className="w-12 h-12 rounded-full bg-amber-100 text-amber-800 border border-amber-300 flex items-center justify-center mx-auto">
                <ShieldCheck className="w-6 h-6 text-amber-600" />
              </div>
              <div>
                <h4 className="font-bold text-slate-900 text-sm">
                  Sistem Yöneticisi Girişi
                </h4>
                <p className="text-xs text-slate-500 mt-1 max-w-xs mx-auto">
                  Google Drive klasör arşivleme, soru silme ve 100/150 soru yuvası açma işlemleri yönetici (nofrostlife@gmail.com) yetkisi gerektirir.
                </p>
              </div>

              <button
                type="button"
                onClick={handleAdminGoogleLogin}
                disabled={isLoading}
                className="w-full bg-white hover:bg-slate-50 border border-slate-300 text-slate-800 font-semibold py-2.5 px-4 rounded-xl text-sm transition-all shadow-sm flex items-center justify-center gap-3 cursor-pointer disabled:opacity-50 active:scale-95"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.66v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.15z" />
                  <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.24v3.15C3.26 21.36 7.33 24 12 24z" />
                  <path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.24C.45 8.15 0 9.99 0 12s.45 3.85 1.24 5.42l4.04-3.15z" />
                  <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.24 6.58l4.04 3.15c.95-2.83 3.6-4.98 6.72-4.98z" />
                </svg>
                <span>{isLoading ? 'Giriş Yapılıyor...' : 'Yönetici Girişi (Google)'}</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
