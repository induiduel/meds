/**
 * Canlı ders bitişinde (sırada başka ders yoksa) kullanıcıya ilgili dersin spot bilgilerinin sesli asistanını
 * açabilmeyi veya soru çözücüde interaktif soru çözmeyi önerir ve yönlendirir.
 * Eşleme: branş + branş içi numara (Patoloji/Enfeksiyon/Üroloji/Genetik/Halk Sağlığı/Kadın Doğum/Farmakoloji dizinleri).
 */
import React, { useEffect, useRef, useState } from 'react';
import { Award, ClipboardList, Headphones, HelpCircle, History, SkipForward, X } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import { dersCozucu, dersHocaCozucu, type DersCozucu } from './dersCozucu';
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
  brans?: Brans;
  /** Kurul 2+ dersleri: başlık ↔ src/data/k<N>*_cozucu eşlemesi (dersCozucu) */
  sesliCozucu?: DersCozucu | null;
  hocaCozucu?: DersCozucu | null;
  sonraki?: CdListeDers;
  cozucu?: { kod: string; soru: number };
  asistan?: { kod: string; soru?: number; adim?: number };
}

async function oneriBul(key: string): Promise<Oneri | null> {
  const liste = await cdListeGetir();
  const d = liste.find((x) => x.key === key);
  if (!d) return null;
  const brans = d.brans ? BRANS[d.brans] : undefined;
  // Aynı branşta (yoksa aynı dönemde) numarası bir sonraki güncel ders
  const sonraki = liste.find((x) => x.key !== d.key && !x.arsiv && !x.sinama && x.brans === d.brans && x.donem === d.donem && Number(x.no) === Number(d.no) + 1);
  const temel = { d, brans, sonraki, sesliCozucu: dersCozucu(d.baslik, d.key), hocaCozucu: dersHocaCozucu(d.baslik, d.key) };
  // Ders sonu penceresi her derste açılır (en az örnek sorular bağlantısı vardır)
  if (!brans) return temel;

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

  return { ...temel, cozucu: cozucuBilgi, asistan: asistanBilgi };
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

  const git = (url: string) => { kapat(); navigateTo(url); };

  const asistanAc = () => {
    const a = oneri.asistan;
    if (!a || !oneri.brans) return;
    kapat();
    navigateTo(onemYolu({ brans: oneri.brans, ders: a.kod, asistan: '1' }));
  };

  const cozucuAc = () => {
    const c = oneri.cozucu;
    if (!c || !oneri.brans) return;
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
        ) : (
          // Motivasyon kapalıyken de ders sonu kutlama animasyonu oynar (hareketi azalt → son kare)
          <div className="cd-mola cd-bitti-mot"><Lottie name="kutlama" loop={false} className="cd-mola-anim" /></div>
        )}
        <b id="cd-cz-b" className="cd-dlg-baslik">{mot ? 'Ders bitti, tebrikler! Pekiştirelim mi?' : 'Ders bitti — pekiştirelim mi?'}</b>
        <p id="cd-cz-m" className="cd-dlg-metin">
          <b>{cdDersEtiketi(oneri.d)} · {oneri.d.baslik}</b> tamamlandı. Konuyu pekiştirmek için aşağıdakilerden birini seç ya da sonraki derse geç:
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
          {!oneri.cozucu && oneri.sesliCozucu && (
            <button ref={!oneri.asistan ? ilkDugmeRef : undefined} type="button" className="on-hero-asistan cd-bitti-hero-btn is-cozucu" onClick={() => git(oneri.sesliCozucu!.url)}>
              <span className="on-hero-asistan-i" aria-hidden><Headphones /></span>
              <span><b>Sesli soru çözücü</b><small>{oneri.sesliCozucu.soru ? `${oneri.sesliCozucu.soru} soru · ` : ''}her şık kaynağıyla, sesli çözüm</small></span>
            </button>
          )}
          {oneri.hocaCozucu && (
            <button type="button" className="on-hero-asistan cd-bitti-hero-btn" onClick={() => git(oneri.hocaCozucu!.url)}>
              <span className="on-hero-asistan-i" aria-hidden><Award /></span>
              <span><b>Sesli hoca çözücü</b><small>{oneri.hocaCozucu.soru} soru · hocanın üslubunda</small></span>
            </button>
          )}
          <button ref={!oneri.asistan && !oneri.cozucu && !oneri.sesliCozucu ? ilkDugmeRef : undefined} type="button" className="on-hero-asistan cd-bitti-hero-btn" onClick={() => git(`${pathFor('ders_detay', oneri.d.key)}?b=sorular`)}>
            <span className="on-hero-asistan-i" aria-hidden><ClipboardList /></span>
            <span><b>Örnek sorular</b><small>Müfredata sadık sorular, anında geri bildirim</small></span>
          </button>
          <button type="button" className="on-hero-asistan cd-bitti-hero-btn" onClick={() => git(pathFor('ders_detay', oneri.d.key))}>
            <span className="on-hero-asistan-i" aria-hidden><History /></span>
            <span><b>Çıkmış sorular ve ders içerikleri</b><small>Dersin çıkmış soruları, çözücüleri ve tüm katmanları</small></span>
          </button>
        </div>

        <div className="cd-dlg-eylem">
          <button type="button" className="cd-btn" onClick={kapat}>Daha sonra</button>
          {oneri.sonraki && <button type="button" className="cd-btn is-ana" onClick={() => git(pathFor('canli_ders', oneri.sonraki!.key))}><SkipForward aria-hidden /><span>Sonraki ders</span></button>}
        </div>
      </div>
    </div>
  );
}
