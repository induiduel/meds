import React from 'react';
import { useAppearance } from '../../utils/appearance';

/** Yalnız v15 kapalıyken çizer: v15'te sayfaya taşınan ya da gezinmeyle yinelenen eski şeritler için. */
export const V15Disinda: React.FC<{ children: React.ReactNode }> = ({ children }) => (useAppearance().v15 ? null : <>{children}</>);
