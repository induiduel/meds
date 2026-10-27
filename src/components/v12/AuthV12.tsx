import React, { useEffect, useId, useRef, useState } from 'react';
import { Activity, AlertCircle, GraduationCap, ArrowLeft, Check, CheckCircle2, Copy, ExternalLink, Globe, KeyRound, Loader2, ShieldAlert, ShieldCheck, X } from 'lucide-react';
import { EntryDialogV12 } from './OnboardingV12';
import { useAppearance } from '../../utils/appearance';
import '../../styles/v12/entry.css';
import '../../styles/v15/giris.css';

/* =============================================================================
 * v12 "Net" — giriş / kayıt kartı ve yetkili alan adı uyarısı (canvas: Entry.dc.html "Giriş", Overlays.dc.html).
 * Durum, doğrulama ve Firebase çağrıları UserAuthModal / AuthErrorModal'da kalır; burada yalnız yapı ve görünüm.
 * ============================================================================= */

export type AuthModeV12 = 'login' | 'register' | 'admin';

export interface AuthCardV12Props {
  mode: AuthModeV12;
  /** Kip değişir ve hata temizlenir */
  onMode: (m: AuthModeV12) => void;
  embedded: boolean;
  /** Kapat düğmesi gösterilsin mi (gömülü ya da zorunlu değilse) */
  closable: boolean;
  onClose: () => void;
  googleIcon: React.ReactNode;
  busy: '' | 'google' | 'form';
  disabled: boolean;
  error: string | null;
  success: string | null;
  email: string;
  setEmail: (v: string) => void;
  password: string;
  setPassword: (v: string) => void;
  showPass: boolean;
  onTogglePass: () => void;
  displayName: string;
  setDisplayName: (v: string) => void;
  studentNumber: string;
  setStudentNumber: (v: string) => void;
  adminPassword: string;
  setAdminPassword: (v: string) => void;
  onGoogle: (admin: boolean) => void;
  onLogin: (e: React.FormEvent) => void;
  onRegister: (e: React.FormEvent) => void;
  onAdminPassword: (e: React.FormEvent) => void;
  onResetPassword?: () => void;
}

/**
 * Canvas sırası: başlık + tek satır açıklama → Google ile devam et → "ya da e-posta" ayırıcı →
 * üstte etiketli alanlar (şifrede Göster) → birincil düğme → "Hesabın yok mu? Kayıt ol" → hata kutusu → alt bağlantılar.
 */
export const AuthCardV12: React.FC<AuthCardV12Props> = (p) => {
  const uid = useId();
  const { mode, disabled } = p;
  const v15 = useAppearance().v15;
  const title = mode === 'admin' ? 'Yönetici girişi' : mode === 'login' ? (v15 ? 'Hesabına gir' : 'Giriş yap') : 'Hesap oluştur';
  const sub =
    mode === 'admin'
      ? 'Yönetim konsoluna erişim'
      : mode === 'login'
        ? (v15 ? 'İlerlemen, notların ve hücren hesabında saklanır.' : 'Tek dokunuşla Google, ya da e-postan ve şifrenle.')
        : v15 ? 'Okul e-postan ve öğrenci numaranla hesabını oluştur.' : 'Katkıların adınla görünsün; soru eklemek için giriş şart değil.';

  const field = (o: {
    id: string; label: string; value: string; set: (v: string) => void;
    type?: string; auto?: string; mode?: 'numeric' | 'email'; placeholder?: string; end?: React.ReactNode;
    hint?: React.ReactNode; hintOk?: boolean;
  }) => {
    const id = `${uid}-${o.id}`;
    return (
      <div className="e12-fld">
        <label className="e12-label" htmlFor={id}>{o.label}</label>
        <div className="e12-field">
          <input
            id={id}
            type={o.type || 'text'}
            value={o.value}
            onChange={(e) => o.set(e.target.value)}
            autoComplete={o.auto}
            inputMode={o.mode}
            placeholder={o.placeholder}
            required
            disabled={disabled}
            aria-describedby={o.hint ? `${id}-h` : undefined}
          />
          {o.end}
        </div>
        {o.hint && <p id={`${id}-h`} className={`e12-hint ${o.hintOk ? 'is-ok' : ''}`}>{o.hint}</p>}
      </div>
    );
  };

  const spin = <Loader2 className="e12-spin" aria-hidden="true" />;
  const passToggle = (
    <button
      type="button"
      className="e12-btn is-ghost is-sm e12-eye"
      onClick={p.onTogglePass}
      aria-label={p.showPass ? 'Şifreyi gizle' : 'Şifreyi göster'}
      aria-pressed={p.showPass}
    >
      {p.showPass ? 'Gizle' : 'Göster'}
    </button>
  );

  return (
    <div className={`e12-auth ${p.embedded ? 'is-embedded' : ''}${v15 ? ' v15g' : ''}`}>
      <header className="e12-auth-h">
        {v15 && <span className="v15g-mark" aria-hidden="true"><Activity strokeWidth={2.4} /></span>}
        <div>
          <h2>{title}</h2>
          <p>{sub}</p>
        </div>
        {p.closable && (
          <button type="button" className="e12-btn is-ghost is-icon is-sm" onClick={p.onClose} aria-label="Kapat">
            <X aria-hidden="true" />
          </button>
        )}
      </header>

      {mode !== 'admin' ? (
        <>
          {false && (
            <div className="v15g-seg" role="tablist" aria-label="Giriş ya da kayıt">
              {(['login', 'register'] as const).map((m) => (
                <button key={m} type="button" role="tab" aria-selected={mode === m} className={mode === m ? 'is-on' : ''} onClick={() => mode !== m && p.onMode(m)}>
                  {m === 'login' ? 'Giriş yap' : 'Kayıt ol'}
                </button>
              ))}
            </div>
          )}
          <button type="button" className="e12-btn is-lg is-block e12-google" onClick={() => p.onGoogle(false)} disabled={disabled}>
            {p.busy === 'google' ? spin : p.googleIcon}
            Google ile devam et
          </button>

          {v15 && mode === 'login' && (
            <button type="button" className="e12-btn is-lg is-block v15g-yol" onClick={() => p.onMode('register')} disabled={disabled}>
              <GraduationCap aria-hidden="true" /> Öğrenci e-postasıyla kayıt ol
            </button>
          )}
          <div className="e12-or" aria-hidden="true"><span>{v15 ? 'ya da' : 'ya da e-posta ile'}</span></div>

          <form key={mode} onSubmit={mode === 'login' ? p.onLogin : p.onRegister} className="e12-form" noValidate>
            {mode === 'register' && (
              <div className="e12-row2">
                {field({ id: 'name', label: 'Ad soyad', value: p.displayName, set: p.setDisplayName, auto: 'name' })}
                {field({ id: 'num', label: 'Öğrenci no', value: p.studentNumber, set: p.setStudentNumber, mode: 'numeric', auto: 'off' })}
              </div>
            )}
            {field({ id: 'email', label: 'E-posta', value: p.email, set: p.setEmail, type: 'email', auto: 'email', mode: 'email', placeholder: 'ad.soyad@ogr.karabuk.edu.tr' })}
            {field({
              id: 'pass',
              label: 'Şifre',
              value: p.password,
              set: p.setPassword,
              type: p.showPass ? 'text' : 'password',
              auto: mode === 'login' ? 'current-password' : 'new-password',
              end: passToggle,
              hint:
                mode === 'register'
                  ? p.password.length >= 6
                    ? (<><Check aria-hidden="true" /> Yeterli uzunlukta</>)
                    : 'En az 6 karakter'
                  : mode === 'login' && p.onResetPassword ? (
                      <button type="button" className="e12-link" onClick={p.onResetPassword} disabled={disabled}>
                        Şifremi unuttum / Şifre tanımla
                      </button>
                    ) : undefined,
              hintOk: mode === 'register' && p.password.length >= 6,
            })}
            <button type="submit" className="e12-btn is-pri is-lg is-block" disabled={disabled}>
              {p.busy === 'form' ? spin : null}
              {mode === 'login' ? 'Giriş yap' : 'Kayıt ol'}
            </button>
          </form>

          {<p className="e12-swap">
            {mode === 'login' ? 'Hesabın yok mu?' : 'Hesabın var mı?'}{' '}
            <button type="button" className="e12-link" onClick={() => p.onMode(mode === 'login' ? 'register' : 'login')}>
              {mode === 'login' ? 'Kayıt ol' : 'Giriş yap'}
            </button>
          </p>}
        </>
      ) : (
        <>
          <button type="button" className="e12-btn is-lg is-block e12-google" onClick={() => p.onGoogle(true)} disabled={disabled}>
            {p.busy === 'google' ? spin : p.googleIcon}
            Google ile yönetici girişi
          </button>
          <div className="e12-or" aria-hidden="true"><span>ya da şifre ile</span></div>
          <form onSubmit={p.onAdminPassword} className="e12-form">
            {field({ id: 'admin', label: 'Yönetici şifresi', value: p.adminPassword, set: p.setAdminPassword, type: 'password', auto: 'current-password' })}
            <button type="submit" className="e12-btn is-pri is-lg is-block" disabled={disabled || !p.adminPassword}>Giriş</button>
          </form>
          <p className="e12-swap">
            <button type="button" className="e12-link" onClick={() => p.onMode('login')}>
              <ArrowLeft aria-hidden="true" /> Öğrenci girişi
            </button>
          </p>
        </>
      )}

      {p.embedded && <span className="e12-auth-fill" aria-hidden="true" />}

      {p.error && (
        <p role="alert" className="e12-alert"><AlertCircle aria-hidden="true" /><span>{p.error}</span></p>
      )}
      {p.success && (
        <p role="status" className="e12-alert is-ok"><CheckCircle2 aria-hidden="true" /><span>{p.success}</span></p>
      )}

      <footer className="e12-auth-f">
        <a href="/sartlar" target="_blank" rel="noopener noreferrer">Kullanım şartları</a>
        <span aria-hidden="true">·</span>
        <a href="/policy" target="_blank" rel="noopener noreferrer">Gizlilik</a>
        {mode !== 'admin' && (
          <>
            <span aria-hidden="true">·</span>
            <button type="button" className="e12-link is-quiet" onClick={() => p.onMode('admin')}>Yönetici girişi</button>
          </>
        )}
      </footer>
    </div>
  );
};

/* -----------------------------------------------------------------------------
 * Firebase yetkili alan adı uyarısı (AuthErrorModal v12 görünümü): sola hizalı diyalog,
 * renkli başlık şeridi yerine ton simgesi; iki çözüm çizgiyle ayrılmış iki bölüm.
 * --------------------------------------------------------------------------- */

export interface AuthErrorV12Props {
  onClose: () => void;
  domain: string;
  domains: string[];
  adminEmail: string;
  projectId: string;
  consoleUrl: string;
  tokenInput: string;
  setTokenInput: (v: string) => void;
  showTokenInput: boolean;
  onToggleToken: () => void;
  onCopy: (d: string) => void;
  onBypass: () => void;
}

export const AuthErrorV12: React.FC<AuthErrorV12Props> = (p) => {
  const id = useId();
  const [copied, setCopied] = useState<string | null>(null);
  const timer = useRef<number | undefined>(undefined);
  useEffect(() => () => window.clearTimeout(timer.current), []);
  const copy = (d: string) => {
    p.onCopy(d);
    setCopied(d);
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => setCopied(null), 2000);
  };

  return (
    <EntryDialogV12 labelledBy={`${id}-t`} onClose={p.onClose} width={560}>
      <div className="e12-dlg-h">
        <span className="e12-lead is-warn" aria-hidden="true"><ShieldAlert /></span>
        <div>
          <h2 id={`${id}-t`}>Firebase Yetkili Alan Adı (Authorized Domain) Uyarısı</h2>
          <p>Hata Kodu: <code className="e12-code">auth/unauthorized-domain</code></p>
        </div>
        <button type="button" className="e12-btn is-ghost is-icon is-sm" onClick={p.onClose} aria-label="Kapat"><X aria-hidden="true" /></button>
      </div>

      <div className="e12-dlg-b">
        <p>
          Firebase Authentication güvenlik politikası gereği, uygulamanın çalıştığı alan adını
          (<code className="e12-code">{p.domain}</code>) Firebase konsoluna kaydetmeniz gerekir.
        </p>

        <section className="e12-sec">
          <h3 className="e12-sec-h is-warn"><Globe aria-hidden="true" /> 1. Kalıcı Çözüm: Alan Adını Firebase'e Ekleyin (1 Dakika)</h3>
          <ol className="e12-steps">
            <li>
              Aşağıdaki butona basarak Firebase Authentication ayarlarını açın:
              <div className="e12-steps-act">
                <a href={p.consoleUrl} target="_blank" rel="noopener noreferrer" className="e12-btn is-sm">
                  Firebase Konsolunu Aç <ExternalLink aria-hidden="true" />
                </a>
              </div>
            </li>
            <li>
              Açılan sayfada <strong>"Yetkili alan adları" (Authorized domains)</strong> başlığı altındaki <strong>"Alan adı ekle" (Add domain)</strong> butonuna tıklayın.
            </li>
            <li>
              Aşağıdaki alan adlarını tek tek yapıştırıp kaydedin:
              <ul className="e12-domains">
                {p.domains.map((dom) => (
                  <li key={dom}>
                    <code>{dom}</code>
                    <button type="button" className="e12-btn is-ghost is-sm" onClick={() => copy(dom)}>
                      {copied === dom ? <Check aria-hidden="true" /> : <Copy aria-hidden="true" />}
                      <span>{copied === dom ? 'Kopyalandı' : 'Kopyala'}</span>
                    </button>
                  </li>
                ))}
              </ul>
            </li>
          </ol>
        </section>

        <section className="e12-sec">
          <div className="e12-sec-row">
            <h3 className="e12-sec-h is-ok"><ShieldCheck aria-hidden="true" /> 2. Beklemeden Devam Et: Yönetici Girişi Yap</h3>
            <span className="e12-badge is-ok">Hemen Kullan</span>
          </div>
          <p>
            Firebase ayarlarını yapmadan önce de sisteminizi test etmek ve tüm soruları yönetmek için doğrudan
            <strong> {p.adminEmail}</strong> yetkili oturumuyla devam edebilirsiniz.
          </p>
          <button type="button" className="e12-btn is-pri is-block e12-wrap" onClick={p.onBypass}>
            <KeyRound aria-hidden="true" />
            <span>Yönetici Olarak Hemen Giriş Yap ({p.adminEmail})</span>
          </button>
          <div className="e12-token">
            <button type="button" className="e12-link" onClick={p.onToggleToken} aria-expanded={p.showTokenInput}>
              {p.showTokenInput ? 'Belirteç kutusunu gizle' : 'Google Drive Access Token girmek ister misiniz? (İsteğe bağlı)'}
            </button>
            {p.showTokenInput && (
              <>
                <div className="e12-field is-mono">
                  <input
                    type="password"
                    aria-label="Google Drive Access Token"
                    placeholder="ya29.a0AfH6SM..."
                    value={p.tokenInput}
                    onChange={(e) => p.setTokenInput(e.target.value)}
                  />
                </div>
                <p className="e12-hint">Google OAuth token girerseniz Drive yüklemelerini doğrudan yapabilirsiniz.</p>
              </>
            )}
          </div>
        </section>
      </div>

      <div className="e12-dlg-f">
        <span className="e12-dlg-meta">Proje ID: <code className="e12-code">{p.projectId}</code></span>
        <span className="e12-grow" />
        <button type="button" className="e12-btn" onClick={p.onClose}>Kapat</button>
      </div>
    </EntryDialogV12>
  );
};
