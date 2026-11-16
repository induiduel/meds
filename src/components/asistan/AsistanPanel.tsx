import React, { useCallback, useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Bot, Send, X, ExternalLink, Check, XCircle, RotateCcw } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { navigateTo } from '../../router';
import '../../styles/v15/asistan.css';

/**
 * Tıp Asistanı sohbet paneli (F3). Cevaplar sunucuda kaynaktan alıntılanır (POST /api/asistan/sor); bu bileşen yalnız gösterir.
 * Blok türleri: metin, maddeler (kaynak numaralı), soru (çözülebilir kart), tablo, sayfalar (uygulama içi yönlendirme).
 */
type Blok =
  | { t: 'metin'; govde: string }
  | { t: 'maddeler'; baslik?: string; ogeler: Array<{ m: string; k: number }> }
  | { t: 'soru'; soru: string; secenekler: Array<{ k: string; m: string }>; dogru: string; aciklama: string; kaynak: number }
  | { t: 'tablo'; baslik: string; h: string[]; r: string[][]; kaynak: number }
  | { t: 'sayfalar'; ogeler: Array<{ baslik: string; alt: string; url: string }> };
interface Kaynak { id: string; tur: string; baslik: string; url: string; ders: string }
interface Cevap { guven: 'birebir' | 'yakin' | 'zayif' | 'sohbet'; bloklar: Blok[]; kaynaklar: Kaynak[]; oneriler: string[]; duzeltilmis: string | null }
interface Mesaj { rol: 'k' | 'a'; metin?: string; cevap?: Cevap; hata?: string }

const GUVEN: Record<string, string> = { birebir: 'Kaynaktan alıntı', yakin: 'Yakın eşleşme', zayif: 'Zayıf eşleşme' };
const BASLANGIC = ['Parkinson hastalığı belirtileri', 'Bana patoloji sorusu getir', 'Sesli soru çözücü nerede', 'ADH açılımı'];
const ANAHTAR = 'medsor_asistan_gecmis';

/** **kalın** işaretini göster; başka biçim yorumlanmaz (kaynak metin güvenli düz yazı olarak basılır) */
function Yazi({ s }: { s: string }) {
  return <>{s.split(/(\*\*[^*]+\*\*)/g).map((p, i) => (p.startsWith('**') && p.endsWith('**') ? <b key={i}>{p.slice(2, -2)}</b> : <React.Fragment key={i}>{p}</React.Fragment>))}</>;
}

function SoruKarti({ b, kaynak }: { b: Extract<Blok, { t: 'soru' }>; kaynak?: Kaynak }) {
  const [sec, setSec] = useState<string | null>(null);
  return (
    <div className="as15-soru">
      <p className="as15-soru-k"><Yazi s={b.soru} /></p>
      <div className="as15-sik" role="group" aria-label="Seçenekler">
        {b.secenekler.map((o) => {
          const durum = sec ? (o.k === b.dogru ? 'dogru' : o.k === sec ? 'yanlis' : '') : '';
          return (
            <button key={o.k} type="button" className={`as15-sk ${durum}`} disabled={!!sec} onClick={() => setSec(o.k)}>
              <b>{o.k}</b><span>{o.m}</span>
              {durum === 'dogru' && <Check aria-hidden />}{durum === 'yanlis' && <XCircle aria-hidden />}
            </button>
          );
        })}
      </div>
      {sec && (
        <div className="as15-acik" role="status">
          <b>{sec === b.dogru ? 'Doğru!' : `Doğru cevap: ${b.dogru}`}</b>
          {b.aciklama && <p><Yazi s={b.aciklama} /></p>}
          {kaynak && <button type="button" className="as15-kay" onClick={() => navigateTo(kaynak.url)}>{kaynak.baslik.slice(0, 60)} <ExternalLink aria-hidden /></button>}
        </div>
      )}
    </div>
  );
}

function BlokGoster({ b, c, ac }: { b: Blok; c: Cevap; ac: (u: string) => void }) {
  switch (b.t) {
    case 'metin': return <p className="as15-p"><Yazi s={b.govde} /></p>;
    case 'maddeler': return (
      <div className="as15-md">
        {b.baslik && <h4>{b.baslik}</h4>}
        <ul>{b.ogeler.map((o, i) => (
          <li key={i}><Yazi s={o.m} />{c.kaynaklar[o.k] && <button type="button" className="as15-no" title={c.kaynaklar[o.k].baslik} onClick={() => ac(c.kaynaklar[o.k].url)}>{o.k + 1}</button>}</li>
        ))}</ul>
      </div>
    );
    case 'soru': return <SoruKarti b={b} kaynak={c.kaynaklar[b.kaynak]} />;
    case 'tablo': return (
      <div className="as15-tb"><h4>{b.baslik}</h4>
        <div className="as15-tb-k"><table><thead><tr>{b.h.map((x, i) => <th key={i}>{x}</th>)}</tr></thead>
          <tbody>{b.r.map((r, i) => <tr key={i}>{r.map((x, j) => <td key={j}>{x}</td>)}</tr>)}</tbody></table></div>
      </div>
    );
    case 'sayfalar': return (
      <div className="as15-sy">{b.ogeler.map((o, i) => (
        <button key={i} type="button" className="as15-kart" onClick={() => ac(o.url)}><span><b>{o.baslik.slice(0, 80)}</b><small>{o.alt}</small></span><ExternalLink aria-hidden /></button>
      ))}</div>
    );
  }
}

/** 2026-10-29: proje durduruldu, panel gizli. Yalnız geliştirici açar: localStorage.medsor_asistan_goster = '1' (sunucuda MEDS_ASISTAN=1 de gerekir). */
const gorunur = () => { try { return localStorage.getItem('medsor_asistan_goster') === '1'; } catch { return false; } };

export default function AsistanPanel() {
  if (!gorunur()) return null;
  return <AsistanIc />;
}

function AsistanIc() {
  const [acik, setAcik] = useState(false);
  const [mesajlar, setMesajlar] = useState<Mesaj[]>(() => { try { return JSON.parse(localStorage.getItem(ANAHTAR) || '[]').slice(-20); } catch { return []; } });
  const [girdi, setGirdi] = useState('');
  const [bekle, setBekle] = useState(false);
  const son = useRef<HTMLDivElement>(null);
  const kutu = useRef<HTMLInputElement>(null);

  useEffect(() => { try { localStorage.setItem(ANAHTAR, JSON.stringify(mesajlar.slice(-20))); } catch { /* özel pencere */ } }, [mesajlar]);
  useEffect(() => { if (acik) { son.current?.scrollIntoView({ block: 'end' }); kutu.current?.focus(); } }, [acik, mesajlar, bekle]);
  useEffect(() => {
    if (!acik) return;
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') setAcik(false); };
    window.addEventListener('keydown', k); return () => window.removeEventListener('keydown', k);
  }, [acik]);

  const gonder = useCallback(async (metin: string) => {
    const soru = metin.trim(); if (!soru || bekle) return;
    setGirdi(''); setBekle(true);
    setMesajlar((m) => [...m, { rol: 'k', metin: soru }]);
    const r = await safeJsonFetch<Cevap>('/api/asistan/sor', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ soru }) });
    setMesajlar((m) => [...m, r.ok && r.data ? { rol: 'a', cevap: r.data } : { rol: 'a', hata: r.status === 429 ? 'Çok sık soruyorsun, biraz bekle.' : 'Şu an cevap veremiyorum, tekrar dene.' }]);
    setBekle(false);
  }, [bekle]);

  const ac = useCallback((url: string) => { navigateTo(url); if (window.matchMedia('(max-width: 720px)').matches) setAcik(false); }, []);
  const sonOneri = [...mesajlar].reverse().find((m) => m.cevap)?.cevap?.oneriler;

  return createPortal(
    <>
      {!acik && <button type="button" className="as15-fab" onClick={() => setAcik(true)} aria-label="Tıp asistanını aç"><Bot aria-hidden /><span>Asistan</span></button>}
      {acik && (
        <section className="as15" role="dialog" aria-label="Tıp asistanı">
          <header className="as15-ust">
            <Bot aria-hidden /><b>Tıp Asistanı</b><small>Cevaplar ders kaynaklarından alınır</small>
            <button type="button" className="as15-ib" onClick={() => setMesajlar([])} aria-label="Sohbeti temizle" title="Sohbeti temizle"><RotateCcw aria-hidden /></button>
            <button type="button" className="as15-ib" onClick={() => setAcik(false)} aria-label="Kapat"><X aria-hidden /></button>
          </header>
          <div className="as15-gov" aria-live="polite">
            {!mesajlar.length && (
              <div className="as15-ilk">
                <p>Hastalık, ilaç, bulgu, çıkmış soru ya da sitede bir sayfa sorabilirsin.</p>
                <div className="as15-cip">{BASLANGIC.map((s) => <button key={s} type="button" onClick={() => gonder(s)}>{s}</button>)}</div>
              </div>
            )}
            {mesajlar.map((m, i) => m.rol === 'k' ? <div key={i} className="as15-k">{m.metin}</div> : (
              <div key={i} className="as15-a">
                {m.hata && <p className="as15-p as15-hata">{m.hata}</p>}
                {m.cevap?.duzeltilmis && <p className="as15-duz">“{m.cevap.duzeltilmis}” olarak anladım.</p>}
                {m.cevap?.bloklar.map((b, j) => <BlokGoster key={j} b={b} c={m.cevap!} ac={ac} />)}
                {m.cevap && GUVEN[m.cevap.guven] && <small className={`as15-gv ${m.cevap.guven}`}>{GUVEN[m.cevap.guven]}</small>}
              </div>
            ))}
            {bekle && <div className="as15-a as15-yaz" aria-label="Aranıyor"><i /><i /><i /></div>}
            {!bekle && sonOneri?.length ? <div className="as15-cip">{sonOneri.map((s) => <button key={s} type="button" onClick={() => gonder(s)}>{s}</button>)}</div> : null}
            <div ref={son} />
          </div>
          <form className="as15-form" onSubmit={(e) => { e.preventDefault(); gonder(girdi); }}>
            <input ref={kutu} value={girdi} onChange={(e) => setGirdi(e.target.value)} placeholder="Bir şey sor: migren tedavisi, nistatin yan etkileri…" maxLength={400} aria-label="Sorun" />
            <button type="submit" disabled={!girdi.trim() || bekle} aria-label="Gönder"><Send aria-hidden /></button>
          </form>
        </section>
      )}
    </>,
    document.body,
  );
}
