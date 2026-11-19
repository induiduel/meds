/**
 * Masa sohbeti: yazı, emoji ve çıkartma. İletiler sunucuda tutulmaz (oda olayı 'sohbet'); bu istemci oyundayken biriktirir.
 * Düğme üst çubukta (SohbetDugme), panel sağdan açılan çekmece (SohbetPanel); ortak durum modül düzeyinde.
 */
import React, { useEffect, useRef, useState, useSyncExternalStore } from 'react';
import { MessageCircle, Send, Smile, Sticker, X } from 'lucide-react';
import { masa } from '../../services/masa/istemci';
import { SOHBET_CIKARTMA, SOHBET_MAKS, type OdaGorunum } from '../../services/masa/tipler';
import { sesCal } from './ortak';
import { sadeAd } from './kabukOrtak';
import '../../styles/masa/sohbet.css';

export interface Ileti { id: number; o: string; ad: string; ben: boolean; m?: string; s?: string; zaman: number }

const EMOJI = ['😀', '😂', '🤣', '😊', '😍', '😘', '😎', '🤔', '😏', '😅', '😭', '😡', '🥲', '😱', '🤯', '🙄',
  '👍', '👎', '👏', '🙌', '🤞', '✌️', '👋', '💯', '🔥', '❤️', '💔', '⭐', '🎯', '🍀', '☕', '🍵'];

let durum = { iletiler: [] as Ileti[], acik: false, okunmamis: 0, oda: '' };
const abone = new Set<() => void>();
const yay = (y: Partial<typeof durum>) => { durum = { ...durum, ...y }; abone.forEach((f) => f()); };
const useSohbet = () => useSyncExternalStore((f) => { abone.add(f); return () => { abone.delete(f); }; }, () => durum);
let sayac = 0;

/** Oda olaylarını dinler; MasaOyun içinde bir kez kurulur */
function useSohbetDinle(oda: OdaGorunum) {
  useEffect(() => { if (durum.oda !== oda.kod) yay({ iletiler: [], okunmamis: 0, oda: oda.kod }); }, [oda.kod]);
  useEffect(() => masa.olayDinle((olaylar, yeni) => {
    const gelen = olaylar.filter((o) => o.t === 'sohbet' && (typeof o.m === 'string' || typeof o.s === 'string'));
    if (!gelen.length) return;
    const adi = (id?: string) => sadeAd((id && (yeni.oyuncular.find((k) => k.id === id)?.ad || yeni.izleyiciler?.find((k) => k.id === id)?.ad)) || 'Oyuncu');
    const yeniler: Ileti[] = gelen.map((o) => ({ id: ++sayac, o: o.o || '', ad: o.o === yeni.ben ? 'Sen' : adi(o.o), ben: o.o === yeni.ben, m: o.m as string | undefined, s: o.s as string | undefined, zaman: Date.now() }));
    const disari = yeniler.filter((i) => !i.ben).length;
    yay({ iletiler: [...durum.iletiler, ...yeniler].slice(-120), okunmamis: durum.acik ? 0 : durum.okunmamis + disari });
    if (disari) sesCal('tepki');
  }), []);
}

export function SohbetDugme() {
  const { acik, okunmamis } = useSohbet();
  return (
    <button type="button" className={`mk-cubuk-dugme ms-dugme${acik ? ' is-acik' : ''}`} onClick={() => yay({ acik: !acik, okunmamis: 0 })} aria-label={`Sohbet${okunmamis ? `, ${okunmamis} yeni ileti` : ''}`} aria-expanded={acik}>
      <MessageCircle size={20} />
      {okunmamis > 0 && <span className="ms-rozet">{okunmamis > 9 ? '9+' : okunmamis}</span>}
    </button>
  );
}

export function SohbetPanel({ oda }: { oda: OdaGorunum }) {
  useSohbetDinle(oda);
  const { iletiler, acik } = useSohbet();
  const [yazi, setYazi] = useState('');
  const [kutu, setKutu] = useState<null | 'emoji' | 'cikartma'>(null);
  const liste = useRef<HTMLOListElement>(null);
  const giris = useRef<HTMLInputElement>(null);
  const [onizleme, setOnizleme] = useState<Ileti | null>(null);

  useEffect(() => { const l = liste.current; if (l) l.scrollTop = l.scrollHeight; }, [iletiler.length, acik]);
  useEffect(() => { if (!acik) setKutu(null); }, [acik]);
  // Panel kapalıyken gelen iletiyi kısa önizleme olarak göster (masayı örtmeyen küçük balon)
  useEffect(() => {
    const son = iletiler[iletiler.length - 1];
    if (acik || !son || son.ben) return;
    setOnizleme(son);
    const t = setTimeout(() => setOnizleme(null), 3500);
    return () => clearTimeout(t);
  }, [iletiler.length]); // eslint-disable-line react-hooks/exhaustive-deps

  const gonderYazi = (e?: React.FormEvent) => {
    e?.preventDefault();
    const m = yazi.trim();
    if (!m) return;
    masa.sohbet({ m }); setYazi(''); setKutu(null);
  };
  const emojiEkle = (em: string) => {
    const el = giris.current;
    const bas = el?.selectionStart ?? yazi.length, son = el?.selectionEnd ?? yazi.length;
    const y = (yazi.slice(0, bas) + em + yazi.slice(son)).slice(0, SOHBET_MAKS);
    setYazi(y);
    requestAnimationFrame(() => { el?.focus(); el?.setSelectionRange(bas + em.length, bas + em.length); });
  };

  return (
    <>
      {onizleme && !acik && (
        <button type="button" className="ms-onizleme" onClick={() => { setOnizleme(null); yay({ acik: true, okunmamis: 0 }); }}>
          <b>{onizleme.ad}</b> <span>{onizleme.s ?? onizleme.m}</span>
        </button>
      )}
      {acik && (
        <aside className="ms-panel" aria-label="Masa sohbeti" onPointerDown={(e) => e.stopPropagation()}>
          <header className="ms-baslik">
            <MessageCircle size={18} aria-hidden="true" /><b>Sohbet</b>
            <button type="button" className="ms-kapat" onClick={() => yay({ acik: false })} aria-label="Sohbeti kapat"><X size={18} /></button>
          </header>
          <ol className="ms-liste" ref={liste} aria-live="polite">
            {iletiler.length === 0 && <li className="ms-bos">Henüz ileti yok. Masaya bir selam gönder 👋</li>}
            {iletiler.map((i, n) => {
              const ayniKisi = n > 0 && iletiler[n - 1].o === i.o;
              return (
                <li key={i.id} className={`ms-ileti${i.ben ? ' is-ben' : ''}${i.s ? ' is-cikartma' : ''}`}>
                  {!ayniKisi && !i.ben && <span className="ms-ad">{i.ad}</span>}
                  {i.s ? <span className="ms-cikartma" aria-label={`${i.ad} çıkartma gönderdi`}>{i.s}</span> : <span className="ms-balon">{i.m}</span>}
                </li>
              );
            })}
          </ol>
          {kutu && (
            <div className={`ms-secici ms-secici--${kutu}`} role="menu" aria-label={kutu === 'emoji' ? 'Emojiler' : 'Çıkartmalar'}>
              {kutu === 'emoji'
                ? EMOJI.map((em) => <button key={em} type="button" role="menuitem" onClick={() => emojiEkle(em)}>{em}</button>)
                : SOHBET_CIKARTMA.map((s) => <button key={s} type="button" role="menuitem" onClick={() => { masa.sohbet({ s }); setKutu(null); }} aria-label={`${s} çıkartmasını gönder`}>{s}</button>)}
            </div>
          )}
          <form className="ms-form" onSubmit={gonderYazi}>
            <button type="button" className={`ms-ikon${kutu === 'emoji' ? ' is-acik' : ''}`} onClick={() => setKutu((k) => (k === 'emoji' ? null : 'emoji'))} aria-label="Emoji ekle"><Smile size={20} /></button>
            <button type="button" className={`ms-ikon${kutu === 'cikartma' ? ' is-acik' : ''}`} onClick={() => setKutu((k) => (k === 'cikartma' ? null : 'cikartma'))} aria-label="Çıkartma gönder"><Sticker size={20} /></button>
            <input ref={giris} value={yazi} maxLength={SOHBET_MAKS} onChange={(e) => setYazi(e.target.value)} placeholder="Mesaj yaz…" aria-label="Mesaj" enterKeyHint="send" autoComplete="off" />
            <button type="submit" className="ms-ikon ms-gonder" disabled={!yazi.trim()} aria-label="Gönder"><Send size={18} /></button>
          </form>
        </aside>
      )}
    </>
  );
}
