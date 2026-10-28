import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { CalendarDays, Check, ChevronDown } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import { aktifKurul, bugun, KURULLAR } from '../../services/kurulTakvimi';
import { kurulKaydet } from '../kurul/KurulSecici';
import { kurulGizli, useSiteAyar } from '../../services/siteAyar';
import '../../styles/v15/kurulsec.css';

/**
 * v15 · Kurul seçici (tasarım A04 kurul + L05 kurulListe): "Kurul N ▾" düğmesi; açılan listede her kurulun teması ve
 * durumu (Bitti · Aktif · başlangıç tarihi), altta "Takvimi aç". Durum ve temalar takvimden (kurulTakvimi); seçim
 * sitenin kurul kaydına yazılır (kurulKaydet), sayfa kendi adresine gider (onSec).
 */
/** "NÖROPSİKİYATRİ KURULU" → "Nöropsikiyatri" (Türkçe küçük harf; "ve" küçük, sondaki "kurulu" atılır) */
const temaAd = (t: string) => t.toLocaleLowerCase('tr-TR').replace(/\s*kurulu\s*$/, '').split(/\s+/).map((w) => (w === 've' ? w : w.charAt(0).toLocaleUpperCase('tr-TR') + w.slice(1))).join(' ');
const AY = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara'];

export default function KurulSecV15({ kurul, onSec, className = '' }: { kurul: number; onSec: (k: number) => void; className?: string }) {
  const [acik, setAcik] = useState(false);
  const [yer, setYer] = useState<{ top: number; left: number }>({ top: 0, left: 0 });
  const kok = useRef<HTMLDivElement>(null);
  const menu = useRef<HTMLDivElement>(null);
  const g = bugun();
  const aktif = aktifKurul().kurul;
  useSiteAyar(); // panelde kapatılan kurul (kurul:<n>) öğrencinin listesinden kalkar
  useEffect(() => {
    if (!acik) return;
    const d = (e: MouseEvent) => { if (!kok.current?.contains(e.target as Node) && !menu.current?.contains(e.target as Node)) setAcik(false); };
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') setAcik(false); };
    document.addEventListener('mousedown', d); document.addEventListener('keydown', k);
    return () => { document.removeEventListener('mousedown', d); document.removeEventListener('keydown', k); };
  }, [acik]);
  const durum = (k: (typeof KURULLAR)[number]) => {
    if (g > k.sinav) return { ad: 'Bitti', cls: 'is-ok' };
    if (k.kurul === aktif) return { ad: 'Aktif', cls: 'is-a' };
    const d = new Date(`${k.baslangic}T12:00:00`);
    return { ad: Number.isNaN(d.getTime()) ? 'Kapalı' : `${d.getDate()} ${AY[d.getMonth()]}`, cls: '' };
  };
  return (
    <div className={`ks15 ${className}`} ref={kok}>
      <button type="button" className="ks15-dug" aria-haspopup="listbox" aria-expanded={acik} onClick={(e) => { const r = e.currentTarget.getBoundingClientRect(); setYer({ top: r.bottom, left: Math.max(16, Math.min(window.innerWidth - Math.min(300, window.innerWidth - 32) - 16, r.left)) }); setAcik((v) => !v); }}>
        Kurul {kurul}<ChevronDown aria-hidden />
      </button>
      {acik && createPortal(
        <div ref={menu} className="ks15-menu" role="listbox" aria-label="Kurul seç" style={yer}>
          {KURULLAR.filter((k) => k.kurul === kurul || !kurulGizli(k.kurul)).map((k) => {
            const d = durum(k);
            return (
              <button key={k.kurul} type="button" role="option" aria-selected={k.kurul === kurul} className={k.kurul === kurul ? 'is-on' : ''}
                onClick={() => { setAcik(false); kurulKaydet(k.kurul); onSec(k.kurul); }}>
                <span className={`ks15-nokta ${d.cls}`} aria-hidden />
                <span className="ks15-t"><b>Kurul {k.kurul}</b><small>{temaAd(k.ad)}</small></span>
                <span className={`ks15-d ${d.cls}`}>{d.ad}</span>
                {k.kurul === kurul && <Check className="ks15-ok" aria-hidden />}
              </button>
            );
          })}
          <hr />
          <button type="button" className="ks15-takvim" onClick={() => { setAcik(false); navigateTo(pathFor('sinav_takvimi')); }}><CalendarDays aria-hidden /> Takvimi aç</button>
        </div>,
        document.body,
      )}
    </div>
  );
}
