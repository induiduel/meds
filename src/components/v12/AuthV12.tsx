import React, { useEffect, useId, useRef, useState } from 'react';
import { Activity, AlertCircle, GraduationCap, ArrowLeft, Check, CheckCircle2, Copy, ExternalLink, Globe, KeyRound, Loader2, ShieldAlert, ShieldCheck, X } from 'lucide-react';
import { EntryDialogV12 } from './OnboardingV12';
import { useAppearance } from '../../utils/appearance';
import '../../styles/v12/entry.css';
import '../../styles/v15/giris.css';

/* =============================================================================
 * v12 "Net" — giriş / kayıt kartı ve yetkili alan adı uyarısı (canvas: Entry.dc.html "Giriş", Overlays.dc.html).
 * Durum, doğrulama ve kimlik çağrıları UserAuthModal'da kalır; burada yalnız yapı ve görünüm (Google girişi 2026-11-02'de kaldırıldı).
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
  busy: '' | 'form';
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
  onLogin: (e: React.FormEvent) => void;
  onRegister: (e: React.FormEvent) => void;
  onAdminPassword: (e: React.FormEvent) => void;
  onResetPassword?: () => void;
  /** Giriş kipinde formun altına eklenen bölüm (e-posta kodu: şifre belirle / şifresiz giriş) */
  loginExtra?: React.ReactNode;
  /** Yönetici kipinde formun altına eklenen bölüm (yönetici şifresini kodla belirleme) */
  adminExtra?: React.ReactNode;
}

/**
 * Sıra: başlık + tek satır açıklama →
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
        ? (v15 ? 'İlerlemen, notların ve hücren hesabında saklanır.' : 'E-postan ve şifrenle.')
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

          <form key={mode} onSubmit={mode === 'login' ? p.onLogin : p.onRegister} className="e12-form" noValidate>
            {mode === 'register' && (
              <div className="e12-row2">
                {field({ id: 'name', label: 'Ad soyad', value: p.displayName, set: p.setDisplayName, auto: 'name' })}
                {field({ id: 'num', label: 'Öğrenci no', value: p.studentNumber, set: p.setStudentNumber, mode: 'numeric', auto: 'off' })}
              </div>
            )}
            {mode === 'login'
              ? field({ id: 'email', label: 'E-posta ya da öğrenci no', value: p.email, set: p.setEmail, type: 'text', auto: 'username', placeholder: 'ad.soyad@ogr.karabuk.edu.tr ya da 2411…' })
              : field({ id: 'email', label: 'E-posta', value: p.email, set: p.setEmail, type: 'email', auto: 'email', mode: 'email', placeholder: 'ad.soyad@ogr.karabuk.edu.tr' })}
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
                  : undefined,
              hintOk: mode === 'register' && p.password.length >= 6,
            })}
            <button type="submit" className="e12-btn is-pri is-lg is-block" disabled={disabled}>
              {p.busy === 'form' ? spin : null}
              {mode === 'login' ? 'Giriş yap' : 'Kayıt ol'}
            </button>
          </form>
          {mode === 'login' && p.loginExtra}

          {v15 && mode === 'login' && (
            <button type="button" className="e12-btn is-lg is-block v15g-yol" onClick={() => p.onMode('register')} disabled={disabled}>
              <GraduationCap aria-hidden="true" /> Öğrenci e-postasıyla kayıt ol
            </button>
          )}

          {<p className="e12-swap">
            {mode === 'login' ? 'Hesabın yok mu?' : 'Hesabın var mı?'}{' '}
            <button type="button" className="e12-link" onClick={() => p.onMode(mode === 'login' ? 'register' : 'login')}>
              {mode === 'login' ? 'Kayıt ol' : 'Giriş yap'}
            </button>
          </p>}
        </>
      ) : (
        <>
          <form onSubmit={p.onAdminPassword} className="e12-form">
            {field({ id: 'admin', label: 'Yönetici şifresi', value: p.adminPassword, set: p.setAdminPassword, type: 'password', auto: 'current-password' })}
            <button type="submit" className="e12-btn is-pri is-lg is-block" disabled={disabled || !p.adminPassword}>Giriş</button>
          </form>
          {p.adminExtra}
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
