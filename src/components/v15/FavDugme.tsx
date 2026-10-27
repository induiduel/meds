import React, { createContext, useContext } from 'react';
import { Repeat, Star } from 'lucide-react';
import { favoriCevir, favoriId, useFavoriler, type FavoriTur } from '../../services/favoriStore';

/** Ders içerik sayfasının bağlamı: kayıt hangi dersten/bölümden geldi */
export const FavBaglam = createContext<{ dersKey: string; ders: string; bolum: string } | null>(null);

export interface FavKayit { tur: FavoriTur; baslik: string; metin: string; slayt?: number[]; adim?: number }

/** ★ (kaydet) + ↻ (tekrar et) düğmeleri; kartın sağ üstüne yerleşir */
export function FavDugme({ k }: { k: FavKayit }) {
  const b = useContext(FavBaglam);
  const liste = useFavoriler();
  if (!b) return null;
  const id = favoriId(b.dersKey, k.tur, k.baslik);
  const f = liste.find((x) => x.id === id);
  const kurul = Number(/^k(\d+)/.exec(b.dersKey)?.[1] || 0);
  const bas = (bayrak: 'yildiz' | 'tekrar') => (e: React.MouseEvent) => {
    e.stopPropagation(); e.preventDefault();
    favoriCevir({ id, tur: k.tur, baslik: k.baslik, metin: k.metin, dersKey: b.dersKey, ders: b.ders, kurul, bolum: b.bolum, slayt: k.slayt?.length ? k.slayt : undefined, adim: k.adim || undefined }, bayrak);
  };
  return (
    <span className="fav-dugme">
      <button type="button" className={f?.yildiz ? 'is-on' : ''} onClick={bas('yildiz')} aria-pressed={!!f?.yildiz} aria-label="Yıldızla (Bugün sayfasına kaydet)" title="Yıldızla"><Star aria-hidden /></button>
      <button type="button" className={f?.tekrar ? 'is-on' : ''} onClick={bas('tekrar')} aria-pressed={!!f?.tekrar} aria-label="Tekrar et listesine ekle" title="Tekrar et"><Repeat aria-hidden /></button>
    </span>
  );
}
