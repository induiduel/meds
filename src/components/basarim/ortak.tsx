/**
 * Başarım ortak parçaları: simge eşlemesi, ATP molekülü, ödül çipleri, seviye basamakları. Stil: styles/basarim.css (.bs-*).
 */
import React from 'react';
import {
  BookOpen, Bug, CalendarDays, CircleCheckBig, Clock, Crown, Flame, Heart, Link2, ListChecks, LogIn, MessageCircle,
  PlusCircle, Puzzle, Repeat, Target, Trophy, Lock, Check,
} from 'lucide-react';
import { olcuYaz, sayi, type Seviye } from '../../services/basarimIstemci';

export const IKON: Record<string, React.ComponentType<{ className?: string; 'aria-hidden'?: boolean; strokeWidth?: number }>> = {
  clock: Clock, target: Target, check: CircleCheckBig, door: LogIn, calendar: CalendarDays, book: BookOpen, flame: Flame,
  link: Link2, repeat: Repeat, crown: Crown, trophy: Trophy, plus: PlusCircle, puzzle: Puzzle, list: ListChecks,
  message: MessageCircle, heart: Heart, bug: Bug,
};
export const Ikon = ({ ad, className }: { ad?: string; className?: string }) => {
  const C = IKON[ad || ''] || Trophy;
  return <C className={className} aria-hidden />;
};

/** ATP molekülü: adenin halkası + riboz + üç fosfat (son bağ yüksek enerjili, parlar). */
export function AtpIkon({ boyut = 18, canli = false }: { boyut?: number; canli?: boolean }) {
  return (
    <svg className={`bs-atp-ikon${canli ? ' is-canli' : ''}`} width={boyut * 1.9} height={boyut} viewBox="0 0 38 20" aria-hidden>
      <polygon points="5,4 9,2 12,5 11,9 7,10 4,8" className="bs-atp-baz" />
      <polygon points="12,9 16,8 17,12 14,14 11,12" className="bs-atp-seker" />
      <line x1="17" y1="11" x2="21" y2="11" className="bs-atp-bag" />
      <circle cx="23" cy="11" r="2.6" className="bs-atp-p" />
      <line x1="25.6" y1="11" x2="27.4" y2="11" className="bs-atp-bag" />
      <circle cx="30" cy="11" r="2.6" className="bs-atp-p" />
      <line x1="32.6" y1="11" x2="33.6" y2="11" className="bs-atp-bag is-enerji" />
      <circle cx="36" cy="11" r="2.4" className="bs-atp-p is-son" />
    </svg>
  );
}

export function OdulCip({ p, a, kucuk = false }: { p: number; a: number; kucuk?: boolean }) {
  return (
    <span className={`bs-odul${kucuk ? ' is-kucuk' : ''}`}>
      {p > 0 && <span className="bs-odul-p">+{sayi(p)} puan</span>}
      {a > 0 && <span className="bs-odul-a"><AtpIkon boyut={kucuk ? 10 : 12} />+{sayi(a)} mol</span>}
      {a < 0 && <span className="bs-odul-a is-eksi"><AtpIkon boyut={kucuk ? 10 : 12} />{sayi(a)} mol</span>}
    </span>
  );
}

/** Seviye basamakları: alınan / sıradaki / kilitli; sıradakinde ilerleme çubuğu. */
export function Basamaklar({ seviyeler, deger, alinan, olcu, renk }: { seviyeler: Seviye[]; deger: number; alinan: number; olcu: string; renk?: string }) {
  return (
    <ol className="bs-basamak" style={renk ? ({ '--bs-renk': renk } as React.CSSProperties) : undefined}>
      {seviyeler.map(([esik, p, a], i) => {
        const tamam = i < alinan || deger >= esik;
        const ulasilan = seviyeler.filter((x, j) => j < alinan || deger >= x[0]).length;
        const sirada = i === ulasilan;
        const onceki = i === 0 ? 0 : seviyeler[i - 1][0];
        const oran = tamam ? 1 : Math.max(0, Math.min(1, (deger - onceki) / Math.max(1, esik - onceki)));
        const ust = i === seviyeler.length - 1;
        return (
          <li key={i} className={`bs-sv${tamam ? ' is-tamam' : ''}${sirada ? ' is-sirada' : ''}${ust ? ' is-ust' : ''}`}>
            <span className="bs-sv-no" aria-hidden>{tamam ? <Check strokeWidth={3} /> : sirada ? i + 1 : <Lock />}</span>
            <span className="bs-sv-govde">
              <span className="bs-sv-esik">{olcuYaz(olcu, esik)}{ust && <em> · en üst</em>}</span>
              <OdulCip p={p} a={a} kucuk />
              {sirada && <span className="bs-sv-cubuk" role="progressbar" aria-valuenow={Math.round(oran * 100)} aria-valuemin={0} aria-valuemax={100}><i style={{ width: `${oran * 100}%` }} /></span>}
            </span>
            <span className="sr-only">{tamam ? 'alındı' : sirada ? 'sırada' : 'kilitli'}</span>
          </li>
        );
      })}
    </ol>
  );
}
