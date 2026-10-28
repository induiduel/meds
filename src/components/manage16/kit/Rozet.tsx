import React from 'react';

export type Ton = 'notr' | 'iyi' | 'uyari' | 'kotu' | 'vurgu' | 'bilgi';

/** Küçük etiket. ton: notr | iyi | uyari | kotu | vurgu | bilgi */
export const Rozet: React.FC<{ ton?: Ton; children: React.ReactNode; title?: string }> = ({ ton = 'notr', children, title }) => (
  <span className={`m16-rozet t-${ton}`} title={title}>{children}</span>
);

/** Noktalı durum göstergesi (ör. çevrimiçi, çalışıyor) */
export const Durum: React.FC<{ ton?: Ton; children: React.ReactNode }> = ({ ton = 'notr', children }) => (
  <span className={`m16-durumnokta t-${ton}`}><i aria-hidden="true" />{children}</span>
);

/** HTTP durum kodu → ton */
export const durumTonu = (kod: number): Ton => (kod >= 500 ? 'kotu' : kod >= 400 ? 'uyari' : kod >= 200 && kod < 300 ? 'iyi' : 'notr');
