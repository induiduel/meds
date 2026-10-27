import React, { useEffect, useId, useMemo, useState } from 'react';
import { BookOpen, CircleHelp, ClipboardList, Link2, Lock, Star, X } from 'lucide-react';
import { fetchSearch, type SearchDocType } from '../search/searchShared';
import { useFavoriler } from '../../services/favoriStore';
import { pathFor } from '../../router';
import { auth, ADMIN_EMAIL } from '../../services/auth';
import { satinAl, sayi, useBasarim, yenile } from '../../services/basarimIstemci';
import '../../styles/v15/sohbet-ayar.css';

/**
 * Özel sohbet eklentileri (2026-10-28): paylaşım ekleri (sayfa, soru, çıkmış soru, favori, terim) ve ATP ile açılan
 * arka plan temaları (Kalpli, Tıbbi, Papatyalı). Ek yalnız uygulama içi adres taşır; sunucu da doğrular (ekTemizle).
 */
export type EkTur = 'sayfa' | 'soru' | 'cikmis' | 'favori' | 'terim';
export interface Ek { tur: EkTur; baslik: string; alt?: string; adres: string }
export type Tema = 'kalp' | 'tibbi' | 'papatya';

const EK_AD: Record<EkTur, string> = { sayfa: 'Sayfa', soru: 'Soru', cikmis: 'Çıkmış soru', favori: 'Favori', terim: 'Terim' };
const EK_IKON: Record<EkTur, React.ReactNode> = {
  sayfa: <Link2 aria-hidden />, soru: <CircleHelp aria-hidden />, cikmis: <ClipboardList aria-hidden />, favori: <Star aria-hidden />, terim: <BookOpen aria-hidden />,
};

/** Mesajdaki paylaşım kartı: dokununca uygulama içinde açılır */
export function EkKart({ ek, ac }: { ek: Ek; ac: (adres: string) => void }) {
  if (!ek?.adres?.startsWith('/') || ek.adres.startsWith('//')) return null;
  return (
    <button type="button" className="sa-ek" onClick={() => ac(ek.adres)}>
      <span className="sa-ek-ik">{EK_IKON[ek.tur] || EK_IKON.sayfa}</span>
      <span className="sa-ek-t"><small>{EK_AD[ek.tur] || 'Paylaşım'}</small><b>{ek.baslik}</b>{ek.alt && <span>{ek.alt}</span>}</span>
    </button>
  );
}

const SAYFALAR: { baslik: string; adres: string }[] = [
  { baslik: 'Dersler', adres: '/dersler' }, { baslik: 'Soru çöz', adres: '/sorular' }, { baslik: 'Sınava hazırlan', adres: '/kamplar' },
  { baslik: 'Sözlük', adres: '/sozluk' }, { baslik: 'Çıkmış sorular', adres: '/cikmis' }, { baslik: 'Sınav spotları', adres: '/spotlar' },
  { baslik: 'Başarımlar', adres: '/basarimlar' }, { baslik: 'Sıralama', adres: '/siralama' },
];
/** Yapıştırılan bağlantıyı yalnız bu sitenin içindeki bir adrese çevirir */
function icAdres(girdi: string): string | null {
  const t = girdi.trim(); if (!t) return null;
  try {
    const u = new URL(t, location.origin);
    if (u.origin !== location.origin) return null;
    return `${u.pathname}${u.search}${u.hash}`.slice(0, 500);
  } catch { return null; }
}

type Sekme = EkTur;
const ARAMA: Partial<Record<Sekme, SearchDocType[]>> = {
  soru: ['active_question', 'ornek_question'], cikmis: ['past_question'], terim: ['glossary_term'],
};
function hitAdres(tur: Sekme, id: string): string {
  const e = encodeURIComponent(id);
  if (tur === 'terim') return `${pathFor('glossary')}?id=${e}`;
  if (tur === 'cikmis') return `${pathFor('past_exams')}/${e}`;
  return `${pathFor('questions')}/${e}`;
}

/** Paylaşım seçici: sayfa / favori / soru / çıkmış soru / terim */
export function PaylasPaneli({ sec, kapat }: { sec: (ek: Ek) => void; kapat: () => void }) {
  const [sekme, setSekme] = useState<Sekme>('sayfa');
  const [q, setQ] = useState('');
  const [yapistir, setYapistir] = useState('');
  const [sonuc, setSonuc] = useState<{ id: string; baslik: string; alt: string; tur: string; adres: string }[] | null>(null);
  const favoriler = useFavoriler();
  useEffect(() => { setQ(''); setSonuc(null); }, [sekme]);
  useEffect(() => {
    const turler = ARAMA[sekme];
    if (!turler || q.trim().length < 2) { setSonuc(null); return; }
    const ac = new AbortController();
    const t = setTimeout(async () => {
      const r = await fetchSearch(q, { types: turler, limit: 8, fast: true }, ac.signal).catch(() => null);
      if (ac.signal.aborted) return;
      setSonuc((r?.results || []).map((h) => {
        const tur = h.documentType;
        const ham = String(h.title || h.snippet || '').replace(/\s+/g, ' ').trim();
        return {
          id: h.id, baslik: ham.slice(0, 110) || 'Başlıksız', alt: h.discipline || h.snippet?.slice(0, 80) || '', tur,
          adres: hitAdres(sekme, h.documentId),
        };
      }));
    }, 350);
    return () => { clearTimeout(t); ac.abort(); };
  }, [q, sekme]);
  const favGor = useMemo(() => {
    const k = q.trim().toLocaleLowerCase('tr-TR');
    return favoriler.filter((f) => !k || `${f.baslik} ${f.ders}`.toLocaleLowerCase('tr-TR').includes(k)).slice(0, 30);
  }, [favoriler, q]);
  const yapAdres = icAdres(yapistir);
  return (
    <div className="sa-paylas v15-card" role="dialog" aria-label="Paylaş">
      <div className="sa-baslik"><b>Sohbette paylaş</b><button type="button" className="tp15-ib" onClick={kapat} aria-label="Kapat"><X aria-hidden /></button></div>
      <div className="sa-sekme" role="tablist">
        {(Object.keys(EK_AD) as Sekme[]).map((s) => (
          <button key={s} type="button" role="tab" aria-selected={sekme === s} className={sekme === s ? 'is-on' : ''} onClick={() => setSekme(s)}>{EK_AD[s]}</button>
        ))}
      </div>
      {sekme === 'sayfa' && (
        <div className="sa-govde">
          <div className="sa-cipler">{SAYFALAR.map((p) => <button key={p.adres} type="button" onClick={() => sec({ tur: 'sayfa', baslik: p.baslik, adres: p.adres })}>{p.baslik}</button>)}</div>
          <label className="sa-alan"><span>Ya da bu sitedeki bir bağlantıyı yapıştır</span>
            <input value={yapistir} onChange={(e) => setYapistir(e.target.value)} placeholder="https://…/ders/…" inputMode="url" /></label>
          {yapistir.trim() && !yapAdres && <p className="tp15-hata">Yalnız bu sitenin bağlantıları paylaşılır.</p>}
          {yapAdres && <button type="button" className="v15-btn" onClick={() => sec({ tur: 'sayfa', baslik: SAYFALAR.find((p) => p.adres === yapAdres.split('?')[0])?.baslik || 'Sayfa bağlantısı', alt: yapAdres.slice(0, 80), adres: yapAdres })}>Bu bağlantıyı paylaş</button>}
        </div>
      )}
      {sekme === 'favori' && (
        <div className="sa-govde">
          <input className="sa-ara" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Favorilerde ara" aria-label="Favorilerde ara" />
          {!favGor.length ? <p className="v15-cap">{favoriler.length ? 'Aramana uyan favori yok.' : 'Henüz favorin yok. Ders sayfalarında ★ ile favori ekleyebilirsin.'}</p> : (
            <ul className="sa-liste">{favGor.map((f) => (
              <li key={f.id}><button type="button" onClick={() => sec({ tur: 'favori', baslik: f.baslik.slice(0, 140), alt: `${f.ders} · ${f.tur}`, adres: `${pathFor('ders_detay', f.dersKey)}?b=${encodeURIComponent(f.bolum)}` })}>
                <b>{f.baslik}</b><span>{f.ders}</span></button></li>
            ))}</ul>
          )}
        </div>
      )}
      {(sekme === 'soru' || sekme === 'cikmis' || sekme === 'terim') && (
        <div className="sa-govde">
          <input className="sa-ara" value={q} onChange={(e) => setQ(e.target.value)} autoFocus aria-label="Ara"
            placeholder={sekme === 'terim' ? 'Terim ara (ör. apoptoz)' : sekme === 'cikmis' ? 'Çıkmış soruda ara' : 'Soruda ara'} />
          {q.trim().length < 2 ? <p className="v15-cap">En az iki harf yaz.</p>
            : sonuc === null ? <span className="v15-skel b15-skel" aria-hidden />
            : !sonuc.length ? <p className="v15-cap">Sonuç bulunamadı.</p>
            : <ul className="sa-liste">{sonuc.map((s) => (
              <li key={s.id}><button type="button" onClick={() => sec({ tur: sekme, baslik: s.baslik, alt: s.alt || undefined, adres: s.adres })}><b>{s.baslik}</b>{s.alt && <span>{s.alt}</span>}</button></li>
            ))}</ul>}
        </div>
      )}
    </div>
  );
}

// ───── Arka plan temaları ─────
export const TEMA_LISTE: { id: Tema; ad: string; ac: string; kilit: string }[] = [
  { id: 'kalp', ad: 'Kalpli', ac: 'Seçtiğin renk paletine uyan kalpler', kilit: 'sohbet_tema_kalp' },
  { id: 'tibbi', ad: 'Tıbbi', ac: 'Artı, kapsül ve EKG çizgisi', kilit: 'sohbet_tema_tibbi' },
  { id: 'papatya', ad: 'Papatyalı', ac: 'Beyaz papatyalar ve yapraklar', kilit: 'sohbet_tema_papatya' },
];
const KALP = 'M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z';
const Papatya = ({ x, y, s, r = 0 }: { x: number; y: number; s: number; r?: number }) => (
  <g transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}>
    {Array.from({ length: 8 }, (_, i) => <ellipse key={i} className="pet" cx="0" cy="-9.5" rx="4.2" ry="9" transform={`rotate(${i * 45})`} />)}
    <circle className="mer" r="4.6" />
  </g>
);

/** Sohbet zemini: renkler paletin belirteçlerinden (CSS sınıfları) gelir; her palet/temada uyum sağlar */
export function SohbetZemin({ tema }: { tema: Tema | null | undefined }) {
  const id = useId().replace(/[^a-z0-9]/gi, '');
  if (!tema) return null;
  const p = `sz${id}`;
  return (
    <svg className={`sa-zemin sa-z-${tema}`} aria-hidden focusable="false" width="100%" height="100%">
      <defs>
        {tema === 'kalp' && (
          <pattern id={p} width="104" height="104" patternUnits="userSpaceOnUse">
            <path className="h1" d={KALP} transform="translate(20 24) rotate(-14) scale(1.15) translate(-12 -12)" />
            <path className="h2" d={KALP} transform="translate(74 62) rotate(12) scale(.8) translate(-12 -12)" />
            <path className="h3" d={KALP} transform="translate(80 14) rotate(-6) scale(.45) translate(-12 -12)" />
            <path className="h3" d={KALP} transform="translate(26 82) rotate(10) scale(.5) translate(-12 -12)" />
            <circle className="h3" cx="52" cy="48" r="2" />
          </pattern>
        )}
        {tema === 'tibbi' && (
          <pattern id={p} width="132" height="132" patternUnits="userSpaceOnUse">
            <path className="t1" d="M-3.5 -10h7v6.5h6.5v7h-6.5v6.5h-7v-6.5h-6.5v-7h6.5z" transform="translate(24 26)" />
            <g transform="translate(96 34) rotate(38)"><rect className="t2" x="-15" y="-6.5" width="30" height="13" rx="6.5" /><path className="t2" d="M0 -6.5v13" /></g>
            <path className="t2" d="M0 104H34l6-17 8 32 7-24 4 9H132" />
            <circle className="t3" cx="64" cy="48" r="2.4" />
            <circle className="t3" cx="14" cy="70" r="2" />
            <path className="t3" d="M-2 -6h4v4h4v4h-4v4h-4v-4h-4v-4h4z" transform="translate(112 78)" />
          </pattern>
        )}
        {tema === 'papatya' && (
          <pattern id={p} width="120" height="120" patternUnits="userSpaceOnUse">
            <path className="yap" d="M0 0c8-3 15 0 19 8-8 3-16 0-19-8z" transform="translate(52 62) rotate(-20)" />
            <path className="yap" d="M0 0c8-3 15 0 19 8-8 3-16 0-19-8z" transform="translate(16 92) rotate(160)" />
            <Papatya x={30} y={32} s={1} r={8} />
            <Papatya x={90} y={86} s={.75} r={-12} />
            <Papatya x={96} y={20} s={.42} r={20} />
            <Papatya x={14} y={104} s={.4} r={0} />
          </pattern>
        )}
      </defs>
      <rect width="100%" height="100%" fill={`url(#${p})`} />
    </svg>
  );
}

/** Tema seçici: kilitli temalar ATP ile açılır, açık olanlar tek dokunuşla uygulanır */
export function TemaSecici({ aktif, sec, kapat }: { aktif: Tema | null; sec: (t: Tema | null) => void; kapat: () => void }) {
  const { tanim, durum } = useBasarim();
  const [bekle, setBekle] = useState('');
  const [ileti, setIleti] = useState('');
  useEffect(() => { void yenile(); }, []);
  const yonetici = String(auth?.currentUser?.email || '').toLowerCase() === ADMIN_EMAIL.toLowerCase();
  const acik = (kilit: string) => {
    const k = tanim.kilitler.find((x) => x.id === kilit);
    return !k || !k.etkin || yonetici || !!durum?.kilit?.[kilit] || !!durum?.ozel?.muaf;
  };
  const tikla = async (t: (typeof TEMA_LISTE)[number]) => {
    setIleti('');
    if (acik(t.kilit)) { sec(t.id); return; }
    const k = tanim.kilitler.find((x) => x.id === t.kilit);
    if (!k || !durum) { setIleti('Kilit bilgisi alınamadı; birazdan tekrar dene.'); return; }
    if (durum.atp.bakiye < k.fiyat) { setIleti(`${sayi(k.fiyat - durum.atp.bakiye)} mol ATP eksik. Hedefler ve başarımlar ATP kazandırır.`); return; }
    if (!confirm(`${t.ad} temasını ${sayi(k.fiyat)} mol ATP ile açmak istiyor musun?`)) return;
    setBekle(t.id);
    try { await satinAl(k.id); sec(t.id); } catch (e: any) { setIleti(e?.message || 'Açılamadı'); } finally { setBekle(''); }
  };
  return (
    <div className="sa-paylas v15-card" role="dialog" aria-label="Sohbet teması">
      <div className="sa-baslik"><b>Sohbet arka planı</b><button type="button" className="tp15-ib" onClick={kapat} aria-label="Kapat"><X aria-hidden /></button></div>
      <div className="sa-temalar">
        <button type="button" className={`sa-tema${!aktif ? ' is-on' : ''}`} onClick={() => sec(null)}>
          <span className="sa-onizle sa-onizle-yok" /><b>Varsayılan</b><small>Düz arka plan</small>
        </button>
        {TEMA_LISTE.map((t) => {
          const k = tanim.kilitler.find((x) => x.id === t.kilit);
          const kilitli = !acik(t.kilit);
          return (
            <button key={t.id} type="button" className={`sa-tema${aktif === t.id ? ' is-on' : ''}${kilitli ? ' is-kilit' : ''}`} onClick={() => void tikla(t)} disabled={bekle === t.id}>
              <span className={`sa-onizle sa-oz-${t.id}`}><SohbetZemin tema={t.id} />{kilitli && <span className="sa-kilit"><Lock aria-hidden /></span>}</span>
              <b>{t.ad}</b><small>{kilitli && k ? `${sayi(k.fiyat)} mol ATP ile aç` : t.ac}</small>
            </button>
          );
        })}
      </div>
      {durum && <p className="v15-cap">ATP bakiyen: <b>{sayi(durum.atp.bakiye)} mol</b>. Açtığın tema hesabında kalıcıdır; seçimin yalnız senin ekranında görünür.</p>}
      {ileti && <p className="tp15-hata" role="alert">{ileti}</p>}
    </div>
  );
}
