import React from 'react';
import type { AppRoute } from '../../router';
import type { AppUser } from '../../services/auth';
import type { SearchHit } from '../search/searchShared';
import type { AccountActions } from './AccountMenu';
import { TopBarV15 } from '../v15/ShellV15';

export type TopBarProps = {
  active: AppRoute;
  onGo: (r: AppRoute) => void;
  user: AppUser | null;
  isAdmin: boolean;
  searchQuery?: string;
  /** hit verilirse (palette sonucuna tıklandı) doğrudan kaynağı açmak denenir */
  onSearch?: (q: string, focusId?: string, hit?: SearchHit) => void;
  onOpenOffline?: () => void;
  actions: Omit<AccountActions, 'onInstall'>;
};

/**
 * Tek tasarım (2026-10-29): yalnız v15 üst çubuğu. Klasik (v10/v11), v12 ve v13 çubukları arşivde:
 * `src/_arsiv/shell/TopBar.tsx` (yüklenmez).
 */
export const TopBar: React.FC<TopBarProps> = (props) => <TopBarV15 {...props} />;
