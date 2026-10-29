import React from 'react';
import type { AppRoute } from '../../router';
import type { AppUser } from '../../services/auth';
import { SideNavV15 } from '../v15/ShellV15';

export type SideNavProps = { active: AppRoute; onGo: (r: AppRoute) => void; isAdmin: boolean; user: AppUser | null };

/**
 * Tek tasarım (2026-10-29): yalnız v15 kenar rayı. Klasik (v10/v11), v12 ve v13 menüleri arşivde:
 * `src/_arsiv/shell/SideNav.tsx` (yüklenmez).
 */
export const SideNav: React.FC<SideNavProps> = (props) => <SideNavV15 {...props} />;
