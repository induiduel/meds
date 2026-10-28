import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ArrowDown, ArrowUp, ChevronLeft, ChevronRight, Columns3, RefreshCw, Search, X } from 'lucide-react';
import { useAdminSorgu, type ListeYaniti } from './api';
import { BosDurum, Hata, Yukleniyor } from './Durumlar';
import { TopluIslem } from './TopluIslem';

export type Sutun<T> = {
  anahtar: string;
  baslik: string;
  /** Hücre içeriği; yoksa satır[anahtar] */
  hucre?: (t: T) => React.ReactNode;
  /** Sıralanabilir: true → anahtar, metin → sunucu sıralama anahtarı */
  sirala?: boolean | string;
  /** CSS genişliği (ör. '120px', '2fr'); varsayılan 1fr */
  genislik?: string;
  /** Varsayılan olarak gizli (sütun seçiciden açılır) */
  gizli?: boolean;
  hizala?: 'sag' | 'orta';
  /** Yerel kipte sıralama/arama değeri */
  deger?: (t: T) => string | number;
};

export type Suzgec = { anahtar: string; etiket: string; secenekler: { deger: string; etiket: string }[] };

export type VeriTablosuProps<T> = {
  /** Kalıcı ayarlar (sütun seçimi) ve adres durumu için benzersiz ad, ör. 'sistem-denetim' */
  kimlik: string;
  sutunlar: Sutun<T>[];
  satirKimligi: (t: T) => string;
  /** Sunucu kipi: liste ucu ({ogeler,toplam,sayfa,boyut,yuzler}); sorgu ?sayfa&boyut&q&sirala&yon&s.<süzgeç> */
  kaynak?: string;
  /** Yerel kip: tüm dizi elde (küçük listeler) */
  ogeler?: T[];
  ekSorgu?: Record<string, unknown>;
  suzgecler?: Suzgec[];
  aramaYeri?: string;
  boyut?: number;
  secim?: boolean;
  topluEylemler?: (secili: string[], temizle: () => void) => React.ReactNode;
  satirTikla?: (t: T) => void;
  /** Etkin satır (çekmecede açık olan) */
  etkin?: string | null;
  canliOlay?: string[];
  bosMetin?: string;
  /** Araç çubuğunun sağına ek düğmeler */
  aracEk?: React.ReactNode;
  /** Adreste ?q=&s=&sayfa= tut (varsayılan true; aynı sayfada iki tablo varsa birinde false) */
  adresteDurum?: boolean;
};

const SATIR_Y = 36;
const SANAL_ESIK = 120;

function adresOku(): URLSearchParams { return new URLSearchParams(window.location.search); }

const fold = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '');

export function VeriTablosu<T>(p: VeriTablosuProps<T>) {
  const adres = p.adresteDurum !== false;
  const ilk = adres ? adresOku() : new URLSearchParams();
  const [q, setQ] = useState(ilk.get('q') || '');
  const [debQ, setDebQ] = useState(q);
  const [sayfa, setSayfa] = useState(Number(ilk.get('sayfa')) || 0);
  const [sirala, setSirala] = useState(ilk.get('sirala') || '');
  const [yon, setYon] = useState<'artan' | 'azalan'>(ilk.get('yon') === 'artan' ? 'artan' : 'azalan');
  const [suz, setSuz] = useState<Record<string, string>>(() => {
    const o: Record<string, string> = {};
    ilk.forEach((v, k) => { if (k.startsWith('s.')) o[k.slice(2)] = v; });
    return o;
  });
  const [secili, setSecili] = useState<Set<string>>(new Set());
  const ayarKey = `m16_sutun_${p.kimlik}`;
  const [gizliSutun, setGizliSutun] = useState<Set<string>>(() => {
    try { const r = localStorage.getItem(ayarKey); if (r) return new Set(JSON.parse(r)); } catch { /* */ }
    return new Set(p.sutunlar.filter((s) => s.gizli).map((s) => s.anahtar));
  });
  const [sutunMenu, setSutunMenu] = useState(false);
  const boyut = p.boyut || 50;

  useEffect(() => { const t = setTimeout(() => setDebQ(q), 250); return () => clearTimeout(t); }, [q]);
  useEffect(() => { setSayfa(0); }, [debQ, JSON.stringify(suz), JSON.stringify(p.ekSorgu || {})]); // eslint-disable-line react-hooks/exhaustive-deps

  // Adres durumu
  useEffect(() => {
    if (!adres) return;
    const u = new URL(window.location.href);
    for (const k of [...u.searchParams.keys()]) if (k === 'q' || k === 'sayfa' || k === 'sirala' || k === 'yon' || k.startsWith('s.')) u.searchParams.delete(k);
    if (debQ) u.searchParams.set('q', debQ);
    if (sayfa) u.searchParams.set('sayfa', String(sayfa));
    if (sirala) { u.searchParams.set('sirala', sirala); u.searchParams.set('yon', yon); }
    for (const [k, v] of Object.entries(suz)) if (v) u.searchParams.set(`s.${k}`, v);
    if (u.href !== window.location.href) window.history.replaceState(window.history.state, '', u.href);
  }, [adres, debQ, sayfa, sirala, yon, suz]);

  const sunucu = useAdminSorgu<ListeYaniti<T>>(p.kaynak || null, {
    sorgu: { ...(p.ekSorgu || {}), sayfa, boyut, q: debQ, sirala, yon: sirala ? yon : undefined, ...Object.fromEntries(Object.entries(suz).map(([k, v]) => [`s.${k}`, v])) },
    canliOlay: p.canliOlay,
  });

  // Yerel kip
  const yerel = useMemo(() => {
    if (!p.ogeler) return null;
    let l = p.ogeler;
    for (const [k, v] of Object.entries(suz)) if (v) l = l.filter((t) => String((t as any)[k]) === v);
    if (debQ) {
      const terms = fold(debQ).split(/\s+/).filter(Boolean);
      l = l.filter((t) => { const m = fold(p.sutunlar.map((s) => String(s.deger ? s.deger(t) : (t as any)[s.anahtar] ?? '')).join(' ')); return terms.every((x) => m.includes(x)); });
    }
    if (sirala) {
      const s = p.sutunlar.find((x) => (typeof x.sirala === 'string' ? x.sirala : x.anahtar) === sirala);
      const f = (t: T) => (s?.deger ? s.deger(t) : (t as any)[sirala]);
      const d = yon === 'artan' ? 1 : -1;
      l = [...l].sort((a, b) => { const x = f(a), y = f(b); return (x < y ? -1 : x > y ? 1 : 0) * d; });
    }
    return { ogeler: l.slice(sayfa * boyut, sayfa * boyut + boyut), toplam: l.length, sayfa, boyut } as ListeYaniti<T>;
  }, [p.ogeler, p.sutunlar, suz, debQ, sirala, yon, sayfa, boyut]);

  const veri = yerel || sunucu.veri;
  const ogeler = veri?.ogeler || [];
  const toplam = veri?.toplam || 0;
  const sayfaSayisi = Math.max(1, Math.ceil(toplam / boyut));
  const gorunen = p.sutunlar.filter((s) => !gizliSutun.has(s.anahtar));
  const izgara = `${p.secim ? '36px ' : ''}${gorunen.map((s) => s.genislik || 'minmax(0,1fr)').join(' ')}`;
  // H143: satırlar ayrı ızgara; her satır kendi içeriğine (max-content) genişleyince sütunlar kayıyordu.
  // Tüm satırlar aynı en küçük genişliği paylaşır: her izin px alt sınırlarının toplamı (telefonda yatay kaydırma bununla).
  const enAz = (p.secim ? 36 : 0) + gorunen.reduce((t, s) => {
    const g = s.genislik || '';
    const m = /^minmax\(\s*(\d+)px/.exec(g) || /^(\d+)px$/.exec(g.trim());
    return t + (m ? Number(m[1]) : 80);
  }, 0);

  const sirayaGec = (s: Sutun<T>) => {
    if (!s.sirala) return;
    const k = typeof s.sirala === 'string' ? s.sirala : s.anahtar;
    if (sirala !== k) { setSirala(k); setYon('azalan'); } else if (yon === 'azalan') setYon('artan'); else { setSirala(''); }
  };

  const tumSecili = ogeler.length > 0 && ogeler.every((t) => secili.has(p.satirKimligi(t)));
  const secimDegistir = (id: string) => setSecili((s) => { const n = new Set(s); if (n.has(id)) n.delete(id); else n.add(id); return n; });
  const temizle = useCallback(() => setSecili(new Set()), []);

  // Sanal kaydırma (büyük sayfa boyutlarında)
  const govdeRef = useRef<HTMLDivElement>(null);
  const [kaydir, setKaydir] = useState(0);
  const sanal = ogeler.length > SANAL_ESIK;
  const yukseklik = 560;
  const bas = sanal ? Math.max(0, Math.floor(kaydir / SATIR_Y) - 10) : 0;
  const son = sanal ? Math.min(ogeler.length, bas + Math.ceil(yukseklik / SATIR_Y) + 20) : ogeler.length;

  const satirTus = (e: React.KeyboardEvent<HTMLDivElement>, t: T) => {
    if (e.key === 'Enter') { e.preventDefault(); p.satirTikla?.(t); }
    else if (e.key === ' ' && p.secim) { e.preventDefault(); secimDegistir(p.satirKimligi(t)); }
    else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      const el = (e.currentTarget[e.key === 'ArrowDown' ? 'nextElementSibling' : 'previousElementSibling'] as HTMLElement | null);
      el?.focus();
    }
  };

  const hata = !yerel && sunucu.hata;
  const ilkYukleme = !yerel && sunucu.yukleniyor && !sunucu.veri;

  return (
    <div className="m16-tablo">
      <div className="m16-tablo-arac">
        <label className="m16-ara">
          <Search aria-hidden="true" />
          <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder={p.aramaYeri || 'Ara…'} aria-label="Tabloda ara" />
          {q && <button type="button" onClick={() => setQ('')} aria-label="Aramayı temizle"><X aria-hidden="true" /></button>}
        </label>
        <div className="m16-tablo-arac-sag">
          {p.aracEk}
          <div className="m16-acilir">
            <button type="button" className="m16-btn hayalet ikon" aria-label="Sütunlar" aria-expanded={sutunMenu} onClick={() => setSutunMenu((v) => !v)}><Columns3 aria-hidden="true" /></button>
            {sutunMenu && (
              <div className="m16-acilir-menu" role="menu" onMouseLeave={() => setSutunMenu(false)}>
                {p.sutunlar.map((s) => (
                  <label key={s.anahtar} className="m16-onay-kutu" role="menuitemcheckbox" aria-checked={!gizliSutun.has(s.anahtar)}>
                    <input type="checkbox" checked={!gizliSutun.has(s.anahtar)} onChange={() => {
                      const n = new Set(gizliSutun);
                      if (n.has(s.anahtar)) n.delete(s.anahtar); else if (gorunen.length > 1) n.add(s.anahtar);
                      setGizliSutun(n);
                      try { localStorage.setItem(ayarKey, JSON.stringify([...n])); } catch { /* */ }
                    }} />
                    {s.baslik}
                  </label>
                ))}
              </div>
            )}
          </div>
          {!yerel && <button type="button" className="m16-btn hayalet ikon" aria-label="Yenile" onClick={() => void sunucu.yenile()}><RefreshCw className={sunucu.yukleniyor ? 'm16-don' : ''} aria-hidden="true" /></button>}
        </div>
      </div>
      {!!p.suzgecler?.length && (
        <div className="m16-cipler" role="group" aria-label="Süzgeçler">
          {p.suzgecler.map((f) => (
            <div key={f.anahtar} className="m16-cip-grup">
              <span className="m16-cip-etiket">{f.etiket}</span>
              {f.secenekler.map((o) => {
                const on = suz[f.anahtar] === o.deger;
                const n = veri?.yuzler?.[f.anahtar]?.find((y) => y.deger === o.deger)?.n;
                return (
                  <button key={o.deger} type="button" className={`m16-cip ${on ? 'on' : ''}`} aria-pressed={on}
                    onClick={() => setSuz((s) => { const x = { ...s }; if (on) delete x[f.anahtar]; else x[f.anahtar] = o.deger; return x; })}>
                    {o.etiket}{n !== undefined && <em>{n}</em>}
                  </button>
                );
              })}
            </div>
          ))}
        </div>
      )}

      <div className="m16-tablo-kap" role="table" style={{ ['--m16-tablo-en' as any]: `${enAz}px` }} aria-rowcount={toplam} aria-busy={sunucu.yukleniyor}>
        <div className="m16-satir m16-baslik-satir" role="row" style={{ gridTemplateColumns: izgara }}>
          {p.secim && (
            <span role="columnheader" className="m16-hucre-sec">
              <input type="checkbox" aria-label="Sayfadakilerin tümünü seç" checked={tumSecili}
                onChange={() => setSecili((s) => { const n = new Set(s); for (const t of ogeler) { const id = p.satirKimligi(t); if (tumSecili) n.delete(id); else n.add(id); } return n; })} />
            </span>
          )}
          {gorunen.map((s) => {
            const k = typeof s.sirala === 'string' ? s.sirala : s.anahtar;
            const aktif = s.sirala && sirala === k;
            return (
              <span key={s.anahtar} role="columnheader" className={`m16-hucre ${s.hizala ? `h-${s.hizala}` : ''}`} aria-sort={aktif ? (yon === 'artan' ? 'ascending' : 'descending') : undefined}>
                {s.sirala ? (
                  <button type="button" className="m16-sirala" onClick={() => sirayaGec(s)}>
                    {s.baslik}{aktif && (yon === 'artan' ? <ArrowUp aria-hidden="true" /> : <ArrowDown aria-hidden="true" />)}
                  </button>
                ) : s.baslik}
              </span>
            );
          })}
        </div>
        {hata ? <Hata hata={hata} yenile={() => void sunucu.yenile()} /> : ilkYukleme ? <Yukleniyor satir={8} /> : ogeler.length === 0 ? (
          <BosDurum baslik={debQ || Object.keys(suz).length ? 'Eşleşen kayıt yok' : p.bosMetin || 'Kayıt yok'} />
        ) : (
          <div ref={govdeRef} className="m16-tablo-govde" role="rowgroup" style={sanal ? { maxHeight: yukseklik, overflowY: 'auto' } : undefined}
            onScroll={sanal ? (e) => setKaydir((e.target as HTMLDivElement).scrollTop) : undefined}>
            {sanal && <div style={{ height: bas * SATIR_Y }} aria-hidden="true" />}
            {ogeler.slice(bas, son).map((t) => {
              const id = p.satirKimligi(t);
              return (
                <div key={id} role="row" tabIndex={0} className={`m16-satir ${p.satirTikla ? 'tik' : ''} ${p.etkin === id ? 'etkin' : ''} ${secili.has(id) ? 'secili' : ''}`}
                  style={{ gridTemplateColumns: izgara, ...(sanal ? { height: SATIR_Y } : {}) }}
                  onClick={(e) => { if ((e.target as HTMLElement).closest('input,button,a')) return; p.satirTikla?.(t); }}
                  onKeyDown={(e) => satirTus(e, t)}>
                  {p.secim && (
                    <span role="cell" className="m16-hucre-sec"><input type="checkbox" aria-label="Satırı seç" checked={secili.has(id)} onChange={() => secimDegistir(id)} /></span>
                  )}
                  {gorunen.map((s) => {
                    const icerik = s.hucre ? s.hucre(t) : String((t as any)[s.anahtar] ?? '');
                    // Düz metin hücre kesilirse (…) tamamı imleçle okunabilsin
                    const baslik = typeof icerik === 'string' || typeof icerik === 'number' ? String(icerik) : undefined;
                    return (
                      <span key={s.anahtar} role="cell" title={baslik && baslik.length > 8 ? baslik : undefined} className={`m16-hucre ${s.hizala ? `h-${s.hizala}` : ''}`}>
                        {icerik}
                      </span>
                    );
                  })}
                </div>
              );
            })}
            {sanal && <div style={{ height: (ogeler.length - son) * SATIR_Y }} aria-hidden="true" />}
          </div>
        )}
      </div>

      <div className="m16-sayfala">
        <span>{toplam.toLocaleString('tr-TR')} kayıt{secili.size ? ` · ${secili.size} seçili` : ''}</span>
        <div>
          <button type="button" className="m16-btn hayalet ikon" disabled={sayfa === 0} onClick={() => setSayfa((s) => s - 1)} aria-label="Önceki sayfa"><ChevronLeft aria-hidden="true" /></button>
          <span aria-live="polite">{sayfa + 1} / {sayfaSayisi}</span>
          <button type="button" className="m16-btn hayalet ikon" disabled={sayfa + 1 >= sayfaSayisi} onClick={() => setSayfa((s) => s + 1)} aria-label="Sonraki sayfa"><ChevronRight aria-hidden="true" /></button>
        </div>
      </div>

      {p.secim && p.topluEylemler && <TopluIslem secili={secili.size} temizle={temizle}>{p.topluEylemler([...secili], temizle)}</TopluIslem>}
    </div>
  );
}
