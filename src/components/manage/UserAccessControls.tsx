import React, { useCallback, useEffect, useState } from 'react';
import { ShieldCheck, Ban, RotateCcw } from 'lucide-react';
import {
  ROLE_LABEL,
  describeResult,
  loadUserAccess,
  setUserRole,
  suspendUsers,
  unsuspendUsers,
  type AccessResult,
  type UserAccess,
  type UserRole,
} from '../../services/userAccessService';
import { ConfirmButton, Drawer, Field, Seg } from './consoleUi';
import { Pill } from '../v14/pageKit';

/**
 * Rol ve askı denetimleri (Kullanıcılar + Kişiler ekranları ortak kullanır).
 * Sunucu: /api/admin/people-access* (yalnız ana yönetici). Moderatör rolü şimdilik yalnız kayıt ve gösterimdir.
 */

const ROLE_OPTS: { id: UserRole; label: string }[] = [
  { id: 'student', label: ROLE_LABEL.student },
  { id: 'moderator', label: ROLE_LABEL.moderator },
  { id: 'admin', label: ROLE_LABEL.admin },
];
const fmt = (s?: string | null) => (s ? new Date(s).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }) : '');

/** uid → erişim kaydı; değişiklikten sonra yerel olarak güncellenir */
export function useUserAccess(notify: (m: string) => void) {
  const [map, setMap] = useState<Record<string, UserAccess>>({});
  const [error, setError] = useState<string | null>(null);
  const reload = useCallback(async () => {
    try {
      const r = await loadUserAccess();
      const next: Record<string, UserAccess> = {};
      for (const u of r.users || []) if (u.uid) next[u.uid] = u;
      setMap(next);
      setError(null);
    } catch (e: any) {
      setError(e?.message || 'Rol ve askı bilgisi alınamadı.');
    }
  }, []);
  useEffect(() => {
    void reload();
  }, [reload]);
  const merge = useCallback((r: AccessResult) => {
    setMap((prev) => {
      const next = { ...prev };
      for (const u of r.changed) next[u.uid] = u;
      return next;
    });
  }, []);
  const run = useCallback(
    async (fn: () => Promise<AccessResult>, verb: string) => {
      try {
        const r = await fn();
        merge(r);
        notify(describeResult(r, verb));
        return r;
      } catch (e: any) {
        notify(e?.message || 'İşlem yapılamadı.');
        return null;
      }
    },
    [merge, notify],
  );
  return {
    map,
    error,
    reload,
    setRole: (uids: string[], role: UserRole) => run(() => setUserRole(uids, role), `${ROLE_LABEL[role].toLocaleLowerCase('tr-TR')} yapıldı`),
    suspend: (uids: string[], reason: string, until?: string | null) => run(() => suspendUsers(uids, reason, until), 'askıya alındı'),
    unsuspend: (uids: string[]) => run(() => unsuspendUsers(uids), 'yeniden etkinleştirildi'),
  };
}
export type UserAccessApi = ReturnType<typeof useUserAccess>;

/** Rol + askı hapları */
export const AccessPills: React.FC<{ access?: UserAccess; fallbackRole?: string; owner?: boolean }> = ({ access, fallbackRole, owner }) => {
  const role: UserRole = owner ? 'admin' : access?.role || (fallbackRole === 'admin' ? 'admin' : fallbackRole === 'moderator' ? 'moderator' : 'student');
  return (
    <span className="inline-flex flex-wrap gap-1">
      <Pill tone={role === 'admin' ? 'acc' : role === 'moderator' ? 'ok' : ''}>{ROLE_LABEL[role]}</Pill>
      {access?.suspended && <Pill tone="bad">Askıda</Pill>}
    </span>
  );
};

/** Ayrıntı sayfasındaki "Rol ve erişim" bölümü */
export const AccessSection: React.FC<{ uid?: string; email?: string; owner: boolean; api: UserAccessApi }> = ({ uid, owner, api }) => {
  const access = uid ? api.map[uid] : undefined;
  const [reason, setReason] = useState('');
  const [until, setUntil] = useState('');
  const [busy, setBusy] = useState(false);
  if (!uid) return null;
  if (owner) {
    return (
      <section className="ms-dsec">
        <h3>Rol ve erişim</h3>
        <p className="m-0 text-sm text-ink-3">
          <ShieldCheck aria-hidden="true" className="inline w-4 h-4" /> Ana yönetici hesabı. Rolü değiştirilemez, askıya alınamaz.
        </p>
      </section>
    );
  }
  const wrap = async (fn: () => Promise<unknown>) => {
    setBusy(true);
    try {
      await fn();
    } finally {
      setBusy(false);
    }
  };
  const role = access?.role || 'student';
  return (
    <section className="ms-dsec">
      <h3>Rol ve erişim</h3>
      {api.error && <p className="m-0 text-sm text-ink-3">{api.error}</p>}
      <Field label="Rol">
        <Seg label="Rol" value={role} onChange={(r) => r !== role && void wrap(() => api.setRole([uid], r))} options={ROLE_OPTS} />
      </Field>
      <p className="m-0 text-sm text-ink-3">Moderatör ve yönetici rolleri şimdilik yalnız kayıt ve gösterim içindir; yönetim yetkisi yalnız ana yöneticidedir.</p>
      {access?.suspended ? (
        <div className="flex flex-col gap-2" style={{ minWidth: 0 }}>
          <p className="m-0 text-sm" style={{ color: 'var(--danger, var(--bad))', overflowWrap: 'anywhere' }}>
            Askıda{access.suspension?.until ? `, ${fmt(access.suspension.until)} tarihine kadar` : ', süresiz'}. Gerekçe: {access.suspension?.reason || 'belirtilmedi'}
          </p>
          <ConfirmButton className="m14-btn" icon={RotateCcw} confirmLabel="Askıyı kaldırmayı onayla" busy={busy} onConfirm={() => wrap(() => api.unsuspend([uid]))}>
            Askıyı kaldır
          </ConfirmButton>
        </div>
      ) : (
        <div className="flex flex-col gap-2" style={{ minWidth: 0 }}>
          <Field label="Askıya alma gerekçesi">
            <textarea className="ms-input" rows={2} value={reason} onChange={(e) => setReason(e.target.value)} placeholder="Öğrenciye gösterilecek gerekçe" />
          </Field>
          <Field label="Bitiş tarihi (isteğe bağlı)">
            <input type="date" className="ms-input" value={until} min={new Date(Date.now() + 864e5).toLocaleDateString('sv-SE')} onChange={(e) => setUntil(e.target.value)} />
          </Field>
          <ConfirmButton
            className="m14-btn danger"
            icon={Ban}
            confirmLabel="Askıya almayı onayla"
            busy={busy}
            disabled={reason.trim().length < 3}
            title={reason.trim().length < 3 ? 'Önce gerekçe yazın' : undefined}
            onConfirm={() =>
              wrap(async () => {
                const r = await api.suspend([uid], reason.trim(), until ? `${until}T23:59:59` : null);
                if (r?.changed.length) {
                  setReason('');
                  setUntil('');
                }
              })
            }
          >
            Askıya al
          </ConfirmButton>
        </div>
      )}
    </section>
  );
};

/** Toplu rol değiştirme / askıya alma çekmecesi */
export const AccessBulkDrawer: React.FC<{
  mode: null | 'role' | 'suspend';
  uids: string[];
  names: string[];
  api: UserAccessApi;
  onClose: () => void;
  onDone: () => void;
}> = ({ mode, uids, names, api, onClose, onDone }) => {
  const [role, setRole] = useState<UserRole>('student');
  const [reason, setReason] = useState('');
  const [until, setUntil] = useState('');
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    if (mode) {
      setRole('student');
      setReason('');
      setUntil('');
    }
  }, [mode]);
  const go = async () => {
    setBusy(true);
    try {
      const r = mode === 'role' ? await api.setRole(uids, role) : await api.suspend(uids, reason.trim(), until ? `${until}T23:59:59` : null);
      if (r) onDone();
    } finally {
      setBusy(false);
    }
  };
  const ready = uids.length > 0 && (mode === 'role' || reason.trim().length >= 3);
  return (
    <Drawer
      open={!!mode}
      onClose={() => !busy && onClose()}
      title={mode === 'role' ? `Rol değiştir · ${uids.length} hesap` : `Askıya al · ${uids.length} hesap`}
      foot={
        <>
          <button type="button" className="m14-btn ghost" onClick={onClose} disabled={busy}>Vazgeç</button>
          {mode === 'role' ? (
            <button type="button" className="m14-btn primary" disabled={!ready || busy} onClick={() => void go()}>
              {busy ? 'Kaydediliyor…' : 'Rolü uygula'}
            </button>
          ) : (
            <ConfirmButton className="m14-btn danger" icon={Ban} confirmLabel={`${uids.length} hesabı askıya almayı onayla`} busy={busy} disabled={!ready} onConfirm={go}>
              Askıya al
            </ConfirmButton>
          )}
        </>
      }
    >
      {mode === 'role' ? (
        <Field label="Yeni rol">
          <Seg label="Yeni rol" value={role} onChange={setRole} options={ROLE_OPTS} />
        </Field>
      ) : (
        <>
          <Field label="Gerekçe (zorunlu)">
            <textarea className="ms-input" rows={3} value={reason} onChange={(e) => setReason(e.target.value)} placeholder="Öğrencilere gösterilecek gerekçe" />
          </Field>
          <Field label="Bitiş tarihi (isteğe bağlı, boşsa süresiz)">
            <input type="date" className="ms-input" value={until} min={new Date(Date.now() + 864e5).toLocaleDateString('sv-SE')} onChange={(e) => setUntil(e.target.value)} />
          </Field>
          <p className="pk14-note">Askıdaki hesaplar içerikleri okuyabilir; soru, yorum, bildirim gibi gönderimler sunucuda reddedilir. Hiçbir veri silinmez.</p>
        </>
      )}
      <p className="pk14-note">Ana yönetici hesabı seçimde olsa bile atlanır.</p>
      <p className="pk14-note" style={{ overflowWrap: 'anywhere' }}>Hesaplar: {names.join(', ') || '—'}</p>
    </Drawer>
  );
};
