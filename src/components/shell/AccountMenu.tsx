import React, { useEffect, useRef } from 'react';
import {
  Activity,
  ChevronRight,
  CloudUpload,
  Database,
  FileDown,
  FileUp,
  FolderPlus,
  LogIn,
  LogOut,
  Moon,
  NotebookPen,
  ShieldCheck,
  Smartphone,
  SquarePen,
  Sun,
  SunMedium,
  Bell,
  Maximize2,
  Minimize2,
} from 'lucide-react';
import type { AppUser } from '../../services/auth';
import { MODE_LABELS, type ThemeMode, useAppearance } from '../../utils/appearance';
import { useAppFullscreen } from '../../utils/fullscreen';
import { Segmented } from '../ui/kit';
import { Sheet } from '../ui/Sheet';
import { initialsOf } from './navModel';

export interface AccountActions {
  onSettings: () => void;
  onNotifications?: () => void;
  onContribute: () => void;
  onPdf: () => void;
  onOffline?: () => void;
  onInstall?: () => void;
  onLogin: () => void;
  onAdminLogin: () => void;
  onLogout: () => void;
  isLoggingIn?: boolean;
  admin?: {
    onConsole: () => void;
    onFaz14: () => void;
    onDiagnostics?: () => void;
    onPastExam?: () => void;
    onNotebookLM?: () => void;
    onDrive: () => void;
    driveBusy?: boolean;
    driveFresh?: boolean;
    onNewCommittee: () => void;
    onSubagents?: () => void;
  };
}

const MODE_ICONS: Record<ThemeMode, React.ElementType> = { light: Sun, sepia: SunMedium, dark: Moon };

/** Hesap menüsünün içeriği: kullanıcı kartı, hızlı tema, eylemler. Telefonda alt sayfada, masaüstünde açılır kutuda. */
const MenuBody: React.FC<{ user: AppUser | null; a: AccountActions; close: () => void }> = ({ user, a, close }) => {
  const look = useAppearance();
  const [appFs, toggleAppFs] = useAppFullscreen();
  const run = (fn?: () => void) => () => {
    close();
    fn?.();
  };
  const item = (Icon: React.ElementType, tint: string, label: string, fn?: () => void, end?: React.ReactNode, disabled?: boolean) => (
    <button type="button" role="menuitem" className="ui-row has-icon" onClick={run(fn)} disabled={disabled}>
      <span className="ui-ico" style={{ '--ico-bg': tint, '--ico-fg': '#fff' } as React.CSSProperties}>
        <Icon strokeWidth={2.1} />
      </span>
      <span className="ui-row-main"><b>{label}</b></span>
      {end && <span className="ui-row-end">{end}</span>}
    </button>
  );

  return (
    <div className="sh-acct">
      <button type="button" className="ui-row sh-acct-card" onClick={run(a.onSettings)}>
        <span className="ui-avatar" style={{ '--av': '44px' } as React.CSSProperties}>
          {user?.photoURL ? <img src={user.photoURL} alt="" /> : user ? initialsOf(user) : <LogIn className="w-5 h-5" />}
        </span>
        <span className="ui-row-main">
          <b>{user ? user.displayName || user.email?.split('@')[0] : 'Giriş yapmadın'}</b>
          <span>{user ? (user.studentNumber ? `No ${user.studentNumber}` : user.email) + (a.admin ? ' · Yönetici' : '') : 'Katkı için isim gerekmez'}</span>
        </span>
        <span className="ui-row-end">Ayarlar<ChevronRight className="w-4 h-4" /></span>
      </button>

      <div className="sh-acct-theme">
        <Segmented<ThemeMode>
          label="Tema"
          value={look.mode}
          onChange={(m) => look.set({ mode: m })}
          options={(['light', 'sepia', 'dark'] as ThemeMode[]).map((m) => {
            const Icon = MODE_ICONS[m];
            return { value: m, label: <span className="inline-flex items-center gap-1.5"><Icon className="w-4 h-4" />{MODE_LABELS[m]}</span> };
          })}
        />
      </div>

      <div className="ui-group" role="menu">
      </div>

      {a.admin && (
        <div className="ui-group" role="menu">
          {item(ShieldCheck, '#FF9500', 'Yönetim konsolu', a.admin.onConsole)}
        </div>
      )}

      <div className="ui-group" role="menu">
        {user ? (
          <button type="button" role="menuitem" className="ui-row" onClick={run(a.onLogout)}>
            <span className="ui-row-main"><b style={{ color: 'var(--color-bad-text)' }}>Çıkış yap</b></span>
            <LogOut className="w-4 h-4" style={{ color: 'var(--color-bad-text)' }} />
          </button>
        ) : (
          <>
            {item(LogIn, 'var(--color-accent)', 'Öğrenci girişi', a.onLogin)}
            {item(ShieldCheck, '#8E8E93', a.isLoggingIn ? 'Giriş yapılıyor…' : 'Yönetici girişi', a.onAdminLogin, undefined, a.isLoggingIn)}
          </>
        )}
      </div>
    </div>
  );
};

export const AccountMenu: React.FC<{ open: boolean; onClose: () => void; user: AppUser | null; actions: AccountActions; phone: boolean }> = ({
  open,
  onClose,
  user,
  actions,
  phone,
}) => {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!open || phone) return;
    const onDown = (e: MouseEvent) => {
      const t = e.target as Node;
      if (ref.current && !ref.current.contains(t) && !(t as HTMLElement).closest?.('.sh-acct-btn, .s12-acct')) onClose();
    };
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
    document.addEventListener('mousedown', onDown);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDown);
      document.removeEventListener('keydown', onKey);
    };
  }, [open, phone]);

  if (phone)
    return (
      <Sheet open={open} onClose={onClose} title="Hesap" label="Hesap ve araçlar">
        <MenuBody user={user} a={actions} close={onClose} />
      </Sheet>
    );
  if (!open) return null;
  return (
    <div ref={ref} className="sh-pop" role="dialog" aria-label="Hesap ve araçlar">
      <MenuBody user={user} a={actions} close={onClose} />
    </div>
  );
};
