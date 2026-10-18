/**
 * Patoloji Hızlı Check Up (/patoloji-check-up): Kurul 1 patoloji ders PDF'lerinden derlenmiş karşılaştırma tabloları
 * (araşidonik asit türevleri, COX-1/2, interlökinler, M1/M2, nekroz tipleri, kaspazlar, Th alt grupları, büyüme
 * faktörleri, hastalık ve ilaç tabloları) ve kısa notlar.
 *  - Bölüm çipleri + bölüm içi tablo listesi; arama tüm bölümlerde satır ve not süzer.
 *  - "Kendini sına": ilk sütun açık, diğer hücreler gizli; dokununca açılır. Tablo "Kontrol ettim" ile işaretlenir.
 *  - İlerleme ve tercih medsoru_checkup_v1 (userKvSync izin listesinde, profille eşitlenir).
 * Veri: checkupVeri.ts · stil: styles/checkup.css (.cu-*), yalnız palet tokenı.
 */
import React, { useCallback, useDeferredValue, useEffect, useMemo, useState } from 'react';
import { Check, Eye, EyeOff, RotateCcw, Search, Table2, X } from 'lucide-react';
import { BOLUMLER, TOPLAM, kaynakGrupla, katla, type CuBolum, type CuNot, type CuTablo } from './checkupVeri';
import '../../styles/checkup.css';

const KEY = 'medsoru_checkup_v1';
type Mod = 'oku' | 'sina';
interface Kayit {
  kontrol: Record<string, number>;
  mod: Mod;
  bolum: string;
}

const oku = (): Kayit => {
  try {
    const v = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (v && typeof v === 'object') return { kontrol: v.kontrol || {}, mod: v.mod === 'sina' ? 'sina' : 'oku', bolum: v.bolum || BOLUMLER[0]?.id };
  } catch {
    /* gizli pencere / engelli depolama */
  }
  return { kontrol: {}, mod: 'oku', bolum: BOLUMLER[0]?.id };
};
const yaz = (k: Kayit) => {
  try {
    localStorage.setItem(KEY, JSON.stringify(k));
  } catch {
    /* yok say */
  }
};

const urlBolum = () => {
  try {
    const b = new URLSearchParams(window.location.search).get('bolum');
    return b && BOLUMLER.some((x) => x.id === b) ? b : null;
  } catch {
    return null;
  }
};

const Kaynak: React.FC<{ k: string[] }> = ({ k }) => (
  <p className="cu-kaynak">
    <span>Kaynak:</span>{' '}
    {kaynakGrupla(k).map((g, i) => (
      <span key={g.kod} className="cu-kaynak-ders">
        {i > 0 && ' · '}
        {g.ad} <span className="cu-mono">s.{g.slaytlar.join(', ')}</span>
      </span>
    ))}
  </p>
);

const TabloKart: React.FC<{
  t: CuTablo;
  satirlar: string[][];
  mod: Mod;
  kontrol: boolean;
  onKontrol: () => void;
  bolumAd?: string;
}> = ({ t, satirlar, mod, kontrol, onKontrol, bolumAd }) => {
  const [acik, setAcik] = useState<Set<string>>(() => new Set());
  const [hepsi, setHepsi] = useState(false);
  useEffect(() => {
    setAcik(new Set());
    setHepsi(false);
  }, [mod]);
  const gizli = mod === 'sina' && !hepsi;
  const ac = (key: string) => setAcik((s) => new Set(s).add(key));
  const gizliSay = gizli ? satirlar.length * (t.sutun.length - 1) - acik.size : 0;

  return (
    <section className={`cu-kart${kontrol ? ' is-ok' : ''}`} id={`cu-${t.id}`} aria-labelledby={`cu-h-${t.id}`}>
      <header className="cu-kart-bas">
        <div className="cu-kart-t">
          {bolumAd && <small className="cu-ust">{bolumAd}</small>}
          <h3 id={`cu-h-${t.id}`}>{t.baslik}</h3>
        </div>
        <div className="cu-kart-arac">
          {mod === 'sina' && (
            <button type="button" className="cu-btn" onClick={() => (hepsi || gizliSay === 0 ? (setHepsi(false), setAcik(new Set())) : setHepsi(true))}>
              {hepsi || gizliSay === 0 ? <><RotateCcw aria-hidden /> Yeniden gizle</> : <><Eye aria-hidden /> Tümünü aç</>}
            </button>
          )}
          <button type="button" className={`cu-btn cu-btn-ok${kontrol ? ' is-on' : ''}`} aria-pressed={kontrol} onClick={onKontrol}>
            <Check aria-hidden /> {kontrol ? 'Kontrol edildi' : 'Kontrol ettim'}
          </button>
        </div>
      </header>
      <div className="cu-tablo-kap">
        <table className="cu-tablo">
          <thead>
            <tr>
              {t.sutun.map((s) => (
                <th key={s} scope="col">{s}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {satirlar.map((r, i) => (
              <tr key={i}>
                {r.map((c, j) => {
                  const key = `${i}:${j}`;
                  const kapali = gizli && j > 0 && !acik.has(key);
                  return j === 0 ? (
                    <th key={j} scope="row" data-l={t.sutun[j]}>{c}</th>
                  ) : (
                    <td key={j} data-l={t.sutun[j]}>
                      {kapali ? (
                        <button type="button" className="cu-gizli" onClick={() => ac(key)} aria-label={`${r[0]} — ${t.sutun[j]}: göster`}>
                          <EyeOff aria-hidden /> Göster
                        </button>
                      ) : (
                        c
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Kaynak k={t.k} />
    </section>
  );
};

const Notlar: React.FC<{ notlar: CuNot[]; baslik?: string }> = ({ notlar, baslik = 'Kısa notlar' }) =>
  notlar.length === 0 ? null : (
    <section className="cu-notlar" aria-label={baslik}>
      <h3>{baslik}</h3>
      <ul>
        {notlar.map((n, i) => (
          <li key={i}>
            <span>{n.m}</span>
            <small className="cu-mono">{kaynakGrupla([n.k]).map((g) => `${g.ad} · s.${g.slaytlar.join(', ')}`)}</small>
          </li>
        ))}
      </ul>
    </section>
  );

export const PatolojiCheckUp: React.FC = () => {
  const [kayit, setKayit] = useState<Kayit>(() => {
    const k = oku();
    const u = urlBolum();
    return u ? { ...k, bolum: u } : k;
  });
  const [q, setQ] = useState('');
  const dq = useDeferredValue(q.trim());
  useEffect(() => yaz(kayit), [kayit]);

  const bolum: CuBolum = BOLUMLER.find((b) => b.id === kayit.bolum) || BOLUMLER[0];
  const sec = useCallback((id: string) => {
    setKayit((k) => ({ ...k, bolum: id }));
    try {
      const u = new URL(window.location.href);
      u.searchParams.set('bolum', id);
      window.history.replaceState(window.history.state, '', u.pathname + u.search);
    } catch {
      /* yok say */
    }
    window.scrollTo({ top: 0 });
  }, []);
  const kontrolEt = (id: string) =>
    setKayit((k) => {
      const kontrol = { ...k.kontrol };
      if (kontrol[id]) delete kontrol[id];
      else kontrol[id] = Date.now();
      return { ...k, kontrol };
    });

  const sonuc = useMemo(() => {
    if (dq.length < 2) return null;
    const terimler = katla(dq).split(/\s+/).filter(Boolean);
    const uyar = (s: string) => {
      const f = katla(s);
      return terimler.every((t) => f.includes(t));
    };
    const tablolar: { b: CuBolum; t: CuTablo; satirlar: string[][] }[] = [];
    const notlar: CuNot[] = [];
    for (const b of BOLUMLER) {
      for (const t of b.tablolar) {
        const baslikUyar = uyar(t.baslik);
        const satirlar = baslikUyar ? t.satir : t.satir.filter((r) => uyar(r.join(' ')));
        if (satirlar.length) tablolar.push({ b, t, satirlar });
      }
      notlar.push(...b.notlar.filter((n) => uyar(n.m)));
    }
    return { tablolar, notlar };
  }, [dq]);

  const toplamKontrol = Object.keys(kayit.kontrol).length;
  const bolumKontrol = (b: CuBolum) => b.tablolar.filter((t) => kayit.kontrol[t.id]).length;

  return (
    <div className="cu">
      <header className="cu-bas">
        <span className="cu-ic" aria-hidden><Table2 /></span>
        <div className="cu-bas-t">
          <h1>Patoloji Hızlı Check Up</h1>
          <p>Mediyatörler, sitokinler, hücre tipleri, nekroz ve hastalıklar karşılaştırmalı tablolarda. Her tablo ders slaytına dayanır.</p>
          <p className="cu-ozet cu-mono">
            {BOLUMLER.length} bölüm · {TOPLAM.tablo} tablo · {TOPLAM.satir} satır · {TOPLAM.not} kısa not ·{' '}
            <b>{toplamKontrol}/{TOPLAM.tablo}</b> kontrol edildi
          </p>
        </div>
      </header>

      <div className="cu-arac">
        <label className="cu-ara">
          <Search aria-hidden />
          <input
            type="search"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Ara: TNF, kaspaz-9, LTB4, Th2, PLA2R…"
            aria-label="Tablolarda ara"
            data-page-search
          />
          {q && (
            <button type="button" className="cu-ara-sil" onClick={() => setQ('')} aria-label="Aramayı temizle">
              <X aria-hidden />
            </button>
          )}
        </label>
        <div className="cu-mod" role="radiogroup" aria-label="Görünüm">
          {(['oku', 'sina'] as Mod[]).map((m) => (
            <button key={m} type="button" role="radio" aria-checked={kayit.mod === m} className={kayit.mod === m ? 'is-on' : ''} onClick={() => setKayit((k) => ({ ...k, mod: m }))}>
              {m === 'oku' ? <><Eye aria-hidden /> Oku</> : <><EyeOff aria-hidden /> Kendini sına</>}
            </button>
          ))}
        </div>
      </div>

      {!sonuc && (
        <nav className="cu-bolumler" aria-label="Bölümler">
          {BOLUMLER.map((b, i) => {
            const n = bolumKontrol(b);
            return (
              <button key={b.id} type="button" className={`cu-bolum${b.id === bolum.id ? ' is-on' : ''}`} aria-current={b.id === bolum.id ? 'true' : undefined} onClick={() => sec(b.id)}>
                <span className="cu-bolum-no cu-mono">{String(i + 1).padStart(2, '0')}</span>
                <span className="cu-bolum-t">
                  <b>{b.ad}</b>
                  <small>{b.kisa}</small>
                </span>
                <span className={`cu-bolum-say cu-mono${n === b.tablolar.length ? ' is-ok' : ''}`}>{n}/{b.tablolar.length}</span>
              </button>
            );
          })}
        </nav>
      )}

      <main className="cu-icerik">
        {sonuc ? (
          <>
            <p className="cu-sonuc-say" role="status">
              “{dq}” için {sonuc.tablolar.length} tabloda {sonuc.tablolar.reduce((a, x) => a + x.satirlar.length, 0)} satır, {sonuc.notlar.length} not
            </p>
            {sonuc.tablolar.length === 0 && sonuc.notlar.length === 0 && <p className="cu-bos">Eşleşen satır yok. Kısaltmayı ya da başka bir yazımı dene (ör. “IL-1” yerine “interlökin”).</p>}
            {sonuc.tablolar.map(({ b, t, satirlar }) => (
              <TabloKart key={t.id} t={t} satirlar={satirlar} mod={kayit.mod} kontrol={!!kayit.kontrol[t.id]} onKontrol={() => kontrolEt(t.id)} bolumAd={b.ad} />
            ))}
            <Notlar notlar={sonuc.notlar} baslik="Eşleşen kısa notlar" />
          </>
        ) : (
          <>
            <div className="cu-bolum-bas">
              <h2>{bolum.ad}</h2>
              <div className="cu-toc" aria-label="Bu bölümdeki tablolar">
                {bolum.tablolar.map((t) => (
                  <a key={t.id} href={`#cu-${t.id}`} className={kayit.kontrol[t.id] ? 'is-ok' : ''} onClick={(e) => {
                    e.preventDefault();
                    document.getElementById(`cu-${t.id}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
                  }}>
                    {kayit.kontrol[t.id] && <Check aria-hidden />}
                    {t.baslik}
                  </a>
                ))}
              </div>
            </div>
            {bolum.tablolar.map((t) => (
              <TabloKart key={t.id} t={t} satirlar={t.satir} mod={kayit.mod} kontrol={!!kayit.kontrol[t.id]} onKontrol={() => kontrolEt(t.id)} />
            ))}
            <Notlar notlar={bolum.notlar} />
            <div className="cu-gecis">
              {BOLUMLER.indexOf(bolum) < BOLUMLER.length - 1 && (
                <button type="button" className="cu-btn cu-btn-ana" onClick={() => sec(BOLUMLER[BOLUMLER.indexOf(bolum) + 1].id)}>
                  Sonraki bölüm: {BOLUMLER[BOLUMLER.indexOf(bolum) + 1].ad}
                </button>
              )}
            </div>
          </>
        )}
      </main>
      <p className="cu-uyari">İçerik Kurul 1 Tıbbi Patoloji ders slaytlarından derlenmiştir; her tablonun altında ders ve slayt numarası yazar.</p>
    </div>
  );
};

export default PatolojiCheckUp;
