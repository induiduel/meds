import React from 'react';
import type { AppRoute } from '../../router';
import { TabBarV15 } from '../v15/ShellV15';

export type TabBarProps = {
  active: AppRoute;
  onGo: (r: AppRoute) => void;
  isAdmin: boolean;
  onPdf: () => void;
  onOffline?: () => void;
};

/**
 * Tek tasarım (2026-10-29): yalnız v15 alt çubuğu. Klasik ada (v10/v11), v12 ve v13 çubukları arşivde:
 * `src/_arsiv/shell/TabBar.tsx` (yüklenmez).
 */
export const TabBar: React.FC<TabBarProps> = (props) => <TabBarV15 {...props} />;
