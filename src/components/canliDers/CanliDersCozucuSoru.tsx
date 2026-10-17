/**
 * Canlı ders bitince (sırada başka ders yoksa) o dersin sesli soru çözücüsünü açmayı önerir.
 * Eşleme: branş + branş içi numara (Patoloji/Enfeksiyon/Üroloji çözücü dizinleri); çözücüsü olmayan derste soru sorulmaz.
 */
import React, { useEffect, useRef, useState } from 'react';
import { CircleHelp, X } from 'lucide-react';
import { navigateTo } from '../../router';
import { cdListeGetir, type CdListeDers } from './canliDersStore';
import { cdDersEtiketi } from './canliDersKategori';
import { cozucuDizinYukle } from '../spots/cozucu/cozucuVeri';
import type { Brans } from '../spots/brans';

const BRANS: Record<string, Brans> = { 'Tıbbi Patoloji': 'patoloji', 'Enfeksiyon Hastalıkları': 'enfeksiyon', 'Üroloji': 'uroloji' };

type Oneri = { d: CdListeDers; brans: Brans; kod: string; soru: number };

async function oneriBul(key: string): Promise<Oneri | null> {
  const d = (await cdListeGetir()).find((x) => x.key === key);
  const brans = d?.brans ? BRANS[d.brans] : undefined;
  if (!d || !brans) return null;
  const dz = await cozucuDizinYukle(brans);
  const c = dz.dersler.find((x) => Number(x.no) === Number(d.no));
  return c ? { d, brans, kod: c.kod, soru: c.soru } : null;
}

export default function CanliDersCozucuSoru() {
  const [oneri, setOneri] = useState<Oneri | null>(null);
  const evetRef = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    const f = (e: Event) => {
      const key = (e as CustomEvent<{ key: string }>).detail?.key;
      if (key) oneriBul(key).then(setOneri, () => {});
    };
    window.addEventListener('cd:ders-bitti', f);
    return () => window.removeEventListener('cd:ders-bitti', f);
  }, []);
  useEffect(() => {
    if (!oneri) return;
    evetRef.current?.focus();
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') setOneri(null); };
    document.addEventListener('keydown', k);
    return () => document.removeEventListener('keydown', k);
  }, [oneri]);
  if (!oneri) return null;
  const ac = () => {
    setOneri(null);
    if (document.fullscreenElement) void document.exitFullscreen?.().catch(() => {});
    navigateTo(`/spotlar?gorunum=cozucu&brans=${oneri.brans}&ders=${encodeURIComponent(oneri.kod)}&coz=1`);
  };
  return (
    <div className="cd-dlg" role="presentation" onClick={(e) => { if (e.target === e.currentTarget) setOneri(null); }}>
      <div className="cd-dlg-kart is-dar" role="alertdialog" aria-modal="true" aria-labelledby="cd-cz-b" aria-describedby="cd-cz-m">
        <button type="button" className="cd-dlg-x cd-btn is-ikon" onClick={() => setOneri(null)} aria-label="Kapat"><X aria-hidden /></button>
        <span className="cd-ikon" aria-hidden><CircleHelp /></span>
        <b id="cd-cz-b" className="cd-dlg-baslik">Ders bitti — soru çözelim mi?</b>
        <p id="cd-cz-m" className="cd-dlg-metin">
          <b>{cdDersEtiketi(oneri.d)} · {oneri.d.baslik}</b> için {oneri.soru} soruluk sesli soru çözücü hazır. Şimdi açılsın mı?
        </p>
        <div className="cd-dlg-eylem">
          <button type="button" className="cd-btn" onClick={() => setOneri(null)}>Şimdi değil</button>
          <button ref={evetRef} type="button" className="cd-btn is-ana" onClick={ac}>Soru çözücüyü aç</button>
        </div>
      </div>
    </div>
  );
}
