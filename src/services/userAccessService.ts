/** Yönetim › Kullanıcı rolleri ve askı işlemleri (sunucu: src/services/userAdminRoutes.ts) */
import { adminCall } from './peopleService';

export type UserRole = 'student' | 'moderator' | 'admin';
export const ROLE_LABEL: Record<UserRole, string> = { student: 'Öğrenci', moderator: 'Moderatör', admin: 'Yönetici' };

export interface UserSuspension {
  active: boolean;
  reason: string;
  until: string | null;
  by: string;
  at: string;
  liftedAt?: string;
  liftedBy?: string;
}
export interface UserAccess {
  uid: string;
  email: string;
  displayName: string;
  role: UserRole;
  isOwner: boolean;
  suspended: boolean;
  suspension: UserSuspension | null;
  accessHistory: { at: string; by: string; kind: 'role' | 'suspend' | 'unsuspend'; from?: string; to?: string; reason?: string; until?: string | null }[];
}
export interface AccessResult {
  success: boolean;
  changed: UserAccess[];
  skipped: { uid: string; reason: string }[];
}

export const loadUserAccess = () => adminCall<{ users: UserAccess[]; roles: UserRole[] }>('/api/admin/people-access');
export const setUserRole = (uids: string[], role: UserRole) =>
  adminCall<AccessResult>('/api/admin/people-access/role', { method: 'POST', body: JSON.stringify({ uids, role }) });
export const suspendUsers = (uids: string[], reason: string, until?: string | null) =>
  adminCall<AccessResult>('/api/admin/people-access/suspend', { method: 'POST', body: JSON.stringify({ uids, reason, until: until || null }) });
export const unsuspendUsers = (uids: string[]) =>
  adminCall<AccessResult>('/api/admin/people-access/unsuspend', { method: 'POST', body: JSON.stringify({ uids }) });

/** Sonuç özeti (toast metni) */
export function describeResult(r: AccessResult, verb: string): string {
  const parts = [`${r.changed.length} hesap ${verb}`];
  if (r.skipped.length) parts.push(`${r.skipped.length} atlandı (${Array.from(new Set(r.skipped.map((s) => s.reason))).join(' ')})`);
  return parts.join(', ') + '.';
}
