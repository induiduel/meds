/**
 * Canlı ders bitişinde (sırada başka ders yoksa) kullanıcıya ilgili dersin spot bilgilerinin sesli asistanını
 * açabilmeyi veya soru çözücüde interaktif soru çözmeyi önerir ve yönlendirir.
 * Eşleme: branş + branş içi numara (Patoloji/Enfeksiyon/Üroloji/Genetik/Halk Sağlığı/Kadın Doğum/Farmakoloji dizinleri).
 */
import React, { useEffect, useRef, useState } from 'react';
import { CircleHelp, Headphones, HelpCircle, Sparkles, X } from 'lucide-react';
import { navigateTo } from '../../router';
import { cozucuYolu, onemYolu } from '../spots/spotsYol';
import { cdListeGetir, type CdListeDers } from './canliDersStore';
import { CD_SPOT_BRANS as BRANS, cdDersEtiketi } from './canliDersKategori';
import { cozucuDizinYukle } from '../spots/cozucu/cozucuVeri';
import { asistanDizinDosyasi } from '../spots/asistan/asistanVeri';
import type { Brans } from '../spots/brans';
import { Lottie } from '../ui/Lottie';
import { cdBitisBirlestir, cdMolaKapat, useCdMola } from './canliDersMotivasyon';


interface Oneri {
  d: CdListeDers;
  brans: Brans;
  cozucu?: { kod: string; soru: number };
  asistan?: { kod: string; soru?: number; adim?: number };
}

async function oneriBul(key: string): Promise<Oneri | null> {
  const d = (await cdListeGetir()).find((x) => x.key === key);
  const brans = d?.brans ? BRANS[d.brans] : undefined;
  if (!d || !brans) return null;

  const no = Number(d.no);
  let cozucuBilgi: { kod: string; soru: number } | undefined;
  let asistanBilgi: { kod: string; soru?: number; adim?: number } | undefined;

  try {
    const dz = await cozucuDizinYukle(brans);
    const c = dz.dersler.find((x) => Number(x.no) === no);
    if (c) cozucuBilgi = { kod: c.kod, soru: c.soru };
  } catch {
    /* yok */
  }

  try {
    const yukleyici = asistanDizinDosyasi(brans);
    if (yukleyici) {
      const adz = await yukleyici();
      const dersler = adz?.default?.dersler;
      if (Array.isArray(dersler)) {
        const a = dersler.find((x: any) => Number(x.no) === no);
        if (a) asistanBilgi = { kod: a.kod, soru: a.soru, adim: a.adim };
      }
    }
  } catch {
    /* yok */
  }

  if (!cozucuBilgi && !asistanBilgi) return null;
  return { d, brans, cozucu: cozucuBilgi, asistan: asistanBilgi };
}

export default function CanliDersCozucuSoru() {
  const [oneri, setOneri] = useState<Oneri | null>(null);
  const ilkDugmeRef = useRef<HTMLButtonElement>(null);
  const mola = useCdMola();
  // Motivasyon açıksa ders sonu sözü + hikâyeli animasyon bu pencerenin başında
  const mot = !!oneri && mola.acik && mola.tip === 'bitis' && mola.key === oneri.d.key ? mola : null;
  useEffect(() => { if (oneri) cdBitisBirlestir(oneri.d.key); }, [oneri, mola.acik]);
  const kapat = () => { setOneri(null); if (mot) cdMolaKapat(false); };

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
    ilkDugmeRef.current?.focus();
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') kapat(); };
    document.addEventListener('keydown', k);
    return () => document.removeEventListener('keydown', k);
  }, [oneri]);

  if (!oneri) return null;

  const asistanAc = () => {
    const a = oneri.asistan;
    if (!a) return;
    kapat();
    navigateTo(onemYolu({ brans: oneri.brans, ders: a.kod, asistan: '1' }));
  };

  const cozucuAc = () => {
    const c = oneri.cozucu;
    if (!c) return;
    kapat();
    navigateTo(cozucuYolu({ brans: oneri.brans, ders: c.kod, coz: '1' }));
  };

  return (
    <div className="cd-dlg" role="presentation" onClick={(e) => { if (e.target === e.currentTarget) kapat(); }}>
      <div className="cd-dlg-kart is-dar" role="alertdialog" aria-modal="true" aria-labelledby="cd-cz-b" aria-describedby="cd-cz-m">
        <button type="button" className="cd-dlg-x cd-btn is-ikon" onClick={kapat} aria-label="Kapat"><X aria-hidden /></button>
        {mot ? (
          <div className="cd-mola cd-bitti-mot">
            <Lottie key={mot.anim} name={mot.anim} className="cd-mola-anim" />
            <p className="cd-mola-metin">{mot.metin}</p>
          </div>
        ) : <span className="cd-ikon" aria-hidden><CircleHelp /></span>}
        <b id="cd-cz-b" className="cd-dlg-baslik">{mot ? 'Ders bitti, tebrikler! Pekiştirelim mi?' : 'Ders bitti — pekiştirelim mi?'}</b>
        <p id="cd-cz-m" className="cd-dlg-metin">
          <b>{cdDersEtiketi(oneri.d)} · {oneri.d.baslik}</b> tamamlandı. Konuyu hafızana kazımak için spot bilgilerle sesli asistanı dinleyebilir veya interaktif soruları çözebilirsin:
        </p>

        <div className="cd-bitti-secenekler" role="group" aria-label="Pekiştirme seçenekleri">
          {oneri.asistan && (
            <button
              ref={ilkDugmeRef}
              type="button"
              className="on-hero-asistan cd-bitti-hero-btn"
              onClick={asistanAc}
            >
              <span className="on-hero-asistan-i" aria-hidden><Headphones /></span>
              <span>
                <b>Sesli Sınav Asistanını Aç</b>
                <small>En önemli spotları sesli özetler, adım adım kritik sorularla pekiştirir</small>
              </span>
            </button>
          )}

          {oneri.cozucu && (
            <button
              ref={!oneri.asistan ? ilkDugmeRef : undefined}
              type="button"
              className="on-hero-asistan cd-bitti-hero-btn is-cozucu"
              onClick={cozucuAc}
            >
              <span className="on-hero-asistan-i" aria-hidden><HelpCircle /></span>
              <span>
                <b>İnteraktif Soru Çözücü</b>
                <small>{oneri.cozucu.soru} soruluk sesli soru çözümü ve detaylı şık analizleri</small>
              </span>
            </button>
          )}
        </div>

        <div className="cd-dlg-eylem">
          <button type="button" className="cd-btn" onClick={kapat}>Daha sonra</button>
        </div>
      </div>
    </div>
  );
}
