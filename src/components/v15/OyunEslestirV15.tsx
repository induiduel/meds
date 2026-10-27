import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Check, Timer } from 'lucide-react';
import { OyunUst, SonKart } from './OyunKitV15';
import type { GlossaryEntry } from '../../data/glossary';

/**
 * v15 · Eşleştir (Oyunlar, tek kişilik): sözlükten 5 terim + karışık tanımları; terime sonra tanıma dokun.
 * 3 tur, süre ve yanlış sayısı tutulur; en iyi süre cihazda (medsoru_oyun_rekor_v1, `eslestir:<kategori>`).
 * Tanım ilk cümlesiyle kısaltılır; terimin kendisi (ya da adının ilk sözcüğü) tanımda geçiyorsa "…" ile gizlenir.
 */
const TUR = 3;
const CIFT = 5;
/** [GlossaryEntry.category etiketi (data/glossary CATEGORY_LABELS), görünen ad] */
export const ESLESTIR_KATEGORI: [string, string][] = [['', 'Karışık'], ['Klinik hastalık', 'Hastalık'], ['Tıbbi Patoloji', 'Patoloji'], ['Farmakoloji', 'İlaç'], ['Genetik & Patoloji', 'Genetik'], ['Mikrobiyoloji', 'Mikroorganizma'], ['Tanı & Yöntem', 'Tanı']];
const REKOR_KEY = 'medsoru_oyun_rekor_v1';

interface Cift { id: string; terim: string; tanim: string }
const karistir = <T,>(a: T[]) => { const r = [...a]; for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; } return r; };
const kacir = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
function tanimYap(e: GlossaryEntry): string {
  let t = String(e.definition || '').split(/(?<=[.!?])\s+/)[0] || '';
  const ad = String(e.term || '').replace(/\s*\(.*?\)\s*/g, ' ').trim();
  for (const p of [ad, ad.split(/\s+/)[0]].filter((x) => x.length > 3)) t = t.replace(new RegExp(`(?<!\\p{L})${kacir(p)}`, 'giu'), '…');
  return t.length > 150 ? `${t.slice(0, 147)}…` : t;
}

export default function OyunEslestirV15({ kategori, onCik }: { kategori: string; onCik: () => void }) {
  const [havuz, setHavuz] = useState<Cift[] | null>(null);
  const [tur, setTur] = useState(0);
  const [secili, setSecili] = useState<string | null>(null);
  const [tamam, setTamam] = useState<Set<string>>(new Set());
  const [hatali, setHatali] = useState<string | null>(null);
  const [yanlis, setYanlis] = useState(0);
  const [bas, setBas] = useState(0);
  const [sn, setSn] = useState(0);
  const [bitti, setBitti] = useState(false);
  const anahtar = `eslestir:${kategori || '*'}`;
  const katAd = ESLESTIR_KATEGORI.find(([k]) => k === kategori)?.[1] || 'Karışık';
  const [rekor, setRekor] = useState<number>(() => { try { return JSON.parse(localStorage.getItem(REKOR_KEY) || '{}')[anahtar] || 0; } catch { return 0; } });
  const [yeniRekor, setYeniRekor] = useState(false);
  const zaman = useRef(0);
  const [seri, setSeri] = useState(0);
  const [yeni, setYeni] = useState<string | null>(null);

  const kur = () => {
    import('../../data/glossary').then(({ GLOSSARY }) => {
      const aday = GLOSSARY.filter((e) => (!kategori || e.category === kategori) && e.term && e.definition && e.term.length <= 40)
        .map((e) => ({ id: e.term, terim: e.term, tanim: tanimYap(e) })).filter((c) => c.tanim.length >= 30 && !c.tanim.startsWith('…'));
      setHavuz(karistir(aday).slice(0, TUR * CIFT));
      setTur(0); setTamam(new Set()); setSecili(null); setYanlis(0); setBas(Date.now()); setSn(0); setBitti(false); setYeniRekor(false); setSeri(0);
    });
  };
  useEffect(kur, [kategori]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (!bas || bitti) return;
    zaman.current = window.setInterval(() => setSn(Math.floor((Date.now() - bas) / 1000)), 250);
    return () => clearInterval(zaman.current);
  }, [bas, bitti]);

  const ciftler = useMemo(() => (havuz || []).slice(tur * CIFT, tur * CIFT + CIFT), [havuz, tur]);
  const tanimlar = useMemo(() => karistir(ciftler), [ciftler]);

  const terimSec = (id: string) => { if (!tamam.has(id)) setSecili(id === secili ? null : id); };
  const tanimSec = (id: string) => {
    if (!secili || tamam.has(id)) return;
    if (id === secili) {
      const n = new Set(tamam).add(id);
      setTamam(n); setSecili(null); setYeni(id); setSeri((x) => x + 1);
      if (ciftler.every((c) => n.has(c.id))) {
        if (tur + 1 >= TUR) {
          const skor = Math.floor((Date.now() - bas) / 1000) + yanlis * 5;
          setBitti(true);
          if (!rekor || skor < rekor) { setRekor(skor); setYeniRekor(true); try { const o = JSON.parse(localStorage.getItem(REKOR_KEY) || '{}'); o[anahtar] = skor; localStorage.setItem(REKOR_KEY, JSON.stringify(o)); } catch { /* yok */ } }
        } else setTimeout(() => { setTur((t) => t + 1); setTamam(new Set()); }, 450);
      }
    } else {
      setYanlis((y) => y + 1); setHatali(id); setSeri(0);
      setTimeout(() => setHatali(null), 450);
    }
  };

  if (!havuz) return <span className="v15-skel b15-skel" aria-hidden />;
  if (havuz.length < TUR * CIFT) return <section className="v15-card oy15-kart"><p>Bu kategoride yeterli terim yok.</p><button type="button" className="oy15-cik" onClick={onCik}>Geri</button></section>;

  if (bitti) {
    const skor = sn + yanlis * 5;
    return (
      <SonKart baslik={`${skor} sn skor`} alt={`${katAd} · ${TUR * CIFT} eşleşme · her yanlış +5 sn · az olan iyi`}
        dogru={TUR * CIFT} yanlis={yanlis} sureSn={sn} enIyi={rekor} rekor={yeniRekor}
        oran={TUR * CIFT / (TUR * CIFT + yanlis)} onCik={onCik} onYeniden={kur} />
    );
  }

  const k = (c: Cift, terim: boolean) => {
    const ok = tamam.has(c.id);
    const cls = ok ? ` is-tamam${yeni === c.id ? ' og15-onay' : ''}` : !terim && hatali === c.id ? ' is-hata og15-titre' : terim && secili === c.id ? ' is-secili' : '';
    return (
      <li key={c.id}><button type="button" className={`es15-k${terim ? ' is-terim' : ''}${cls}`} disabled={ok || (!terim && !secili)} aria-pressed={terim ? secili === c.id : undefined}
        onClick={() => (terim ? terimSec(c.id) : tanimSec(c.id))}>{ok && <Check aria-hidden className="oy15-iz-ok" />}<span>{terim ? c.terim : c.tanim}</span></button></li>
    );
  };
  return (
    <section className="oy15-soru og15-oyun" lang="tr">
      <OyunUst ilerleme={(tur * CIFT + tamam.size) / (TUR * CIFT)} sol={`Tur ${tur + 1}/${TUR}`} puan={tur * CIFT + tamam.size} puanEtiket="eşleşme" seri={seri}
        ek={<><span className="og15-cip"><Timer aria-hidden /> {sn} sn</span><span className="og15-cip is-sonuk">{katAd} · {yanlis} yanlış</span></>} onCik={onCik} />
      <p className="v15-cap">Önce bir terime, sonra onun tanımına dokun.</p>
      <div className="oy15-iz">
        <div className="oy15-iz-b"><h3 className="oy15-iz-h">Terimler</h3><ul className="es15-sutun oy15-iz-terimler" aria-label="Terimler">{ciftler.map((c) => k(c, true))}</ul></div>
        <div className="oy15-iz-b"><h3 className="oy15-iz-h">Tanımlar</h3><ul className="es15-sutun" aria-label="Tanımlar">{tanimlar.map((c) => k(c, false))}</ul></div>
      </div>
    </section>
  );
}
