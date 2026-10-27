import React, { startTransition, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Check, ChevronDown, CopyCheck, CopyPlus, Eye, Search, X } from 'lucide-react';
import { useStorageRefresh } from '../../hooks/useStorageRefresh';
import { getFavoriteCards, toggleFavoriteCard } from '../../services/studyStore';
import { kaydetSpotZiyaret } from '../../services/spotCozucuIstatistik';
import { toast } from '../ui/Toast';
import { ANAHTAR, KAT, type Spot, type Veri, Zengin, azHareket, kucuk, okuOgrenilen, yazOgrenilen } from '../spots/spotsShared';
import { useV15Baslik } from './baslik';
import '../../styles/v15/ogren.css';
import '../../styles/v15/spot.css';

/**
 * v15 · Sınav spotları (tasarım sistemi v15 › B08 "önem rozetli spot kartları"). Veri ve "öğrendim" kaydı SpotsV12 ile
 * aynı (exam_spots_k1.json, medsoru_spot_ogrendim); "Karta ekle" favori ezber kartına koyar.
 * Yerleşim: üstte ders çipleri + durum çipleri (Tümü · Kesin sorulur · Öğrenilmemiş) + Oku/Kendini sına, altta kendi
 * alanında kayan kart ızgarası. Kart: önem rozeti + tür · başlık · spot; dokununca ayrıntı (maddeler, soru-cevap,
 * tuzak, tablo) kartın içinde açılır. Kendini sına kipinde spot metni dokunana dek gizlidir.
 */
const SAYFA = 30;
const KART_ONEK = 'spot:';
type Durum = 'hepsi' | 'yuksek' | 'ogrenilmemis';
const DURUM: [Durum, string][] = [['hepsi', 'Tümü'], ['yuksek', 'Kesin sorulur'], ['ogrenilmemis', 'Öğrenilmemiş']];
const ONEM: Record<number, [string, string]> = { 3: ['Kesin sorulur', 'is-w'], 2: ['Sık sorulur', 'is-a'], 1: ['Destekleyici', ''] };
const duz = (s?: string) => String(s || '').replace(/\*\*/g, '');
const tr = (n: number) => n.toLocaleString('tr-TR');

export default function SpotsV15() {
  const [veri, setVeri] = useState<Veri | null>(null);
  const [hata, setHata] = useState(false);
  const [girdi, setGirdi] = useState('');
  const [q, setQ] = useState('');
  const [araAcik, setAraAcik] = useState(false);
  const [disiplin, setDisiplin] = useState('');
  const [durum, setDurum] = useState<Durum>('hepsi');
  const [sina, setSina] = useState(false);
  const [acik, setAcik] = useState<string | null>(null);
  const [gorulen, setGorulen] = useState<Set<string>>(() => new Set());
  const [limit, setLimit] = useState(SAYFA);
  const [ogrenilen, setOgrenilen] = useState<Set<string>>(okuOgrenilen);
  useStorageRefresh([ANAHTAR], () => setOgrenilen(okuOgrenilen()));
  const [kartta, setKartta] = useState<Set<string>>(() => new Set(getFavoriteCards().map((c) => c.id)));
  useStorageRefresh(['medsoru_flashcard_favorites_v1'], () => setKartta(new Set(getFavoriteCards().map((c) => c.id))));
  const [odak, setOdak] = useState<string | null>(() => { try { return new URLSearchParams(window.location.search).get('id'); } catch { return null; } });
  const bekci = useRef<HTMLLIElement>(null);
  const alan = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let iptal = false;
    import('../../data/exam_spots_k1.json')
      .then((m) => { if (!iptal) setVeri((m.default ?? m) as unknown as Veri); })
      .catch(() => { if (!iptal) setHata(true); });
    return () => { iptal = true; };
  }, []);

  const dersMap = useMemo(() => new Map((veri?.dersler || []).map((d) => [d.no, d])), [veri]);
  const disiplinler = useMemo(() => {
    const m = new Map<string, number>();
    for (const s of veri?.spotlar || []) { const d = dersMap.get(s.ders)?.disiplin || 'Diğer'; m.set(d, (m.get(d) || 0) + 1); }
    return [...m.entries()].sort((a, b) => b[1] - a[1]);
  }, [veri, dersMap]);
  const metin = useMemo(() => {
    const m = new Map<string, string>();
    for (const s of veri?.spotlar || []) m.set(s.id, kucuk([s.baslik, s.spot, s.tuzak, s.cevap, s.soru, ...(s.maddeler || []), ...(s.etiketler || [])].filter(Boolean).join(' ')));
    return m;
  }, [veri]);

  const liste = useMemo(() => {
    if (!veri) return [] as Spot[];
    const k = kucuk(q.trim()).split(/\s+/).filter(Boolean);
    return veri.spotlar.filter((s) => {
      if (disiplin && dersMap.get(s.ders)?.disiplin !== disiplin) return false;
      if (durum === 'yuksek' && s.onem < 3) return false;
      if (durum === 'ogrenilmemis' && ogrenilen.has(s.id)) return false;
      if (k.length) { const t = metin.get(s.id) || ''; if (!k.every((w) => t.includes(w))) return false; }
      return true;
    });
  }, [veri, disiplin, durum, ogrenilen, q, metin, dersMap]);

  useEffect(() => { setLimit(SAYFA); alan.current?.scrollTo({ top: 0 }); }, [disiplin, durum, q]);
  useEffect(() => {
    const el = bekci.current;
    if (!el || liste.length <= limit) return;
    const io = new IntersectionObserver((e) => { if (e.some((x) => x.isIntersecting)) setLimit((l) => l + SAYFA); }, { root: alan.current, rootMargin: '600px 0px' });
    io.observe(el);
    return () => io.disconnect();
  }, [limit, liste.length]);

  // Derin bağlantı (?id=): süzgeçleri sıfırla, spota kadar çiz, aç ve ortala
  useEffect(() => {
    if (!veri || !odak) return;
    const i = veri.spotlar.findIndex((x) => x.id === odak);
    if (i < 0) { setOdak(null); return; }
    if (disiplin || durum !== 'hepsi' || q) { setDisiplin(''); setDurum('hepsi'); setQ(''); setGirdi(''); return; }
    if (i >= limit) { setLimit(i + SAYFA); return; }
    const id = odak;
    setAcik(id);
    setOdak(null);
    requestAnimationFrame(() => document.getElementById(`sp15-${id}`)?.scrollIntoView({ block: 'center', behavior: azHareket() ? 'auto' : 'smooth' }));
  }, [veri, odak, limit, disiplin, durum, q]);

  const ogren = useCallback((id: string) => setOgrenilen((p) => {
    const n = new Set(p);
    if (n.has(id)) n.delete(id); else n.add(id);
    yazOgrenilen(n);
    return n;
  }), []);
  const kartaEkle = useCallback((s: Spot) => {
    const id = `${KART_ONEK}${s.id}`;
    const next = toggleFavoriteCard({ id, front: duz(s.soru || s.baslik), back: duz(s.cevap ? `${s.cevap} — ${s.spot}` : s.spot), group: 'Sınav spotları' });
    const ekli = next.some((c) => c.id === id);
    setKartta(new Set(next.map((c) => c.id)));
    toast.show('success', ekli ? 'Kartlara eklendi' : 'Kartlardan çıkarıldı', ekli ? 'Kartlar › Göz at › Favoriler' : s.baslik);
  }, []);
  const ac = (s: Spot) => {
    setAcik((a) => (a === s.id ? null : s.id));
    kaydetSpotZiyaret({ id: s.id, ders: s.ders, baslik: s.baslik, kategori: s.kategori });
  };

  const toplam = veri?.spotlar.length || 0;
  const ogrSayi = useMemo(() => (veri ? veri.spotlar.filter((s) => ogrenilen.has(s.id)).length : 0), [veri, ogrenilen]);
  useV15Baslik({ baslik: 'Sınav spotları', alt: veri ? `Kurul ${veri.kurul ?? 1} · ${tr(ogrSayi)}/${tr(toplam)} öğrenildi` : undefined });

  return (
    <div className="sp15">
      <h1 className="sr-only">Sınav spotları</h1>
      <div className="o15-ust">
        {araAcik ? (
          <label className="o15-ara">
            <Search aria-hidden />
            <input autoFocus type="search" value={girdi} placeholder="Spotlarda ara" aria-label="Spotlarda ara"
              onChange={(e) => { const v = e.target.value; setGirdi(v); startTransition(() => setQ(v)); }} />
            <button type="button" className="v15-ib" onClick={() => { setGirdi(''); setQ(''); setAraAcik(false); }} aria-label="Aramayı kapat"><X aria-hidden /></button>
          </label>
        ) : (
          <div className="o15-cipler v15-hscroll" role="toolbar" aria-label="Durum">
            {DURUM.map(([id, t]) => (
              <button key={id} type="button" className={`o15-cip${durum === id ? ' is-on' : ''}`} aria-pressed={durum === id} onClick={() => setDurum(id)}>{t}</button>
            ))}
            <span className="sp15-ayrac" aria-hidden />
            <button type="button" className={`o15-cip${sina ? ' is-on' : ''}`} aria-pressed={sina} onClick={() => { setSina((v) => !v); setGorulen(new Set()); }}>
              <Eye aria-hidden /> Kendini sına
            </button>
          </div>
        )}
        {!araAcik && <button type="button" className="v15-ib" onClick={() => setAraAcik(true)} aria-label="Ara"><Search aria-hidden /></button>}
      </div>
      {!araAcik && disiplinler.length > 1 && (
        <div className="o15-cipler v15-hscroll sp15-dal" role="toolbar" aria-label="Ders">
          <button type="button" className={`o15-cip${!disiplin ? ' is-on' : ''}`} aria-pressed={!disiplin} onClick={() => setDisiplin('')}>Tüm dersler</button>
          {disiplinler.map(([d, n]) => (
            <button key={d} type="button" className={`o15-cip${disiplin === d ? ' is-on' : ''}`} aria-pressed={disiplin === d} onClick={() => setDisiplin(d)}>{d} <span className="v15-cap">{n}</span></button>
          ))}
        </div>
      )}

      <div className="sp15-alan" ref={alan}>
        {!veri ? (
          hata ? <p className="b15-bos v15-card">Spotlar yüklenemedi.</p> : <span className="v15-skel b15-skel" aria-hidden />
        ) : liste.length ? (
          <ul className="sp15-izgara" role="list">
            {liste.slice(0, limit).map((s) => {
              const [onemAd, onemCls] = ONEM[s.onem] || ONEM[1];
              const o = ogrenilen.has(s.id);
              const a = acik === s.id;
              const gizli = sina && !gorulen.has(s.id);
              const d = dersMap.get(s.ders);
              return (
                <li key={s.id} id={`sp15-${s.id}`} className={`sp15-kart v15-card${o ? ' is-ok' : ''}${a ? ' is-acik' : ''}`}>
                  <button type="button" className="sp15-bas" aria-expanded={a} onClick={() => ac(s)}>
                    <span className="sp15-rz">
                      <span className={`v15-tag ${onemCls}`}>{onemAd}</span>
                      <span className="v15-cap">{KAT[s.kategori]?.kisa}</span>
                      {o && <Check className="sp15-ok" aria-label="Öğrenildi" />}
                    </span>
                    <b>{s.baslik}</b>
                    {!gizli && <span className="sp15-spot"><Zengin metin={s.spot} /></span>}
                    <ChevronDown className="sp15-ok2" aria-hidden />
                  </button>
                  {gizli && (
                    <button type="button" className="v15-btn is-soft sp15-goster" onClick={() => setGorulen((p) => new Set(p).add(s.id))}>Cevabı göster</button>
                  )}
                  {a && !gizli && (
                    <div className="sp15-detay">
                      {s.soru && <p className="sp15-sc"><span className="v15-label">Soru</span>{duz(s.soru)}<br /><span className="v15-label">Cevap</span><b>{duz(s.cevap)}</b></p>}
                      {!!s.maddeler?.length && <ul className="sp15-mad">{s.maddeler.map((m, i) => <li key={i}><Zengin metin={m} /></li>)}</ul>}
                      {s.karsilastir && (
                        <div className="sp15-tablo"><table>
                          <thead><tr>{s.karsilastir.basliklar.map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
                          <tbody>{s.karsilastir.satirlar.map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j}><Zengin metin={c} /></td>)}</tr>)}</tbody>
                        </table></div>
                      )}
                      {s.tuzak && <p className="sp15-tuzak"><span className="v15-label">Tuzak</span><Zengin metin={s.tuzak} /></p>}
                      <p className="v15-cap">{d ? `${d.no}. ${d.baslik}${d.hoca ? ` · ${d.hoca}` : ''}` : ''}</p>
                      <div className="sp15-eylem">
                        <button type="button" className={`v15-btn ${o ? 'is-soft' : ''}`} onClick={() => ogren(s.id)}><Check aria-hidden /> {o ? 'Öğrenildi' : 'Öğrendim'}</button>
                        <button type="button" className="v15-btn is-ghost" onClick={() => kartaEkle(s)}>
                          {kartta.has(`${KART_ONEK}${s.id}`) ? <><CopyCheck aria-hidden /> Kartta</> : <><CopyPlus aria-hidden /> Karta ekle</>}
                        </button>
                      </div>
                    </div>
                  )}
                </li>
              );
            })}
            {liste.length > limit && <li ref={bekci} className="v15-skel sp15-bekci" aria-hidden />}
          </ul>
        ) : (
          <p className="b15-bos v15-card">Bu süzgeçte spot yok.</p>
        )}
      </div>
    </div>
  );
}
