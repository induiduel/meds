import React, { useEffect, useMemo, useState } from 'react';
import { Bookmark, SlidersHorizontal, Trash2, X } from 'lucide-react';
import '../../styles/v15/suzgec.css';

/**
 * v15 · Ortak soru süzgeci (tasarım Y03 aktif çipler · Y04 PC yan panel · Y05 kayıtlı süzgeçler).
 * Çağıran taraf yönleri (ders, konu, kurul, yıl, durum …) ve seçeneklerini verir; bileşen yalnız seçim durumunu yönetir.
 * - Y03: seçili her değer kapatılabilir çip; "Temizle".
 * - Y04: geniş ekranda (≥900px kap) listenin solunda kalıcı panel, dar ekranda "Süzgeç" düğmesiyle açılan alt sayfa.
 * - Y05: süzgeç adla kaydedilir; kayıt yalnız bu cihazda (localStorage `medsoru_suzgec_<kayitAnahtari>_v1`, try/catch).
 * Süzme işini çağıran yapar: `suzgecUyar(deger, yon, ogeDegeri)`.
 */
export interface SuzgecYonu { id: string; ad: string; secenekler: { deger: string; n?: number }[] }
export type SuzgecDegeri = Record<string, string[]>;
interface Kayitli { ad: string; deger: SuzgecDegeri; at: string }

export const suzgecUyar = (d: SuzgecDegeri, yon: string, v: string | undefined | null) => {
  const s = d[yon];
  return !s || !s.length || (v != null && s.includes(v));
};
export const suzgecSayisi = (d: SuzgecDegeri) => Object.values(d).reduce((a, s) => a + (s?.length || 0), 0);

const anahtar = (k: string) => `medsoru_suzgec_${k}_v1`;
const kayitOku = (k: string): Kayitli[] => {
  try { const x = JSON.parse(localStorage.getItem(anahtar(k)) || '[]'); return Array.isArray(x) ? x.filter((y) => y && typeof y.ad === 'string' && y.deger) : []; } catch { return []; }
};
const kayitYaz = (k: string, l: Kayitli[]) => { try { localStorage.setItem(anahtar(k), JSON.stringify(l.slice(0, 20))); } catch { /* kota / özel pencere */ } };

interface Props {
  yonler: SuzgecYonu[];
  deger: SuzgecDegeri;
  onChange: (d: SuzgecDegeri) => void;
  kayitAnahtari: string;
  /** süzülmüş öge sayısı (çip satırında) */
  sonuc?: number;
  children: React.ReactNode;
}

export default function SoruSuzgecV15({ yonler, deger, onChange, kayitAnahtari, sonuc, children }: Props) {
  const [acik, setAcik] = useState(false);
  const [kayitlar, setKayitlar] = useState<Kayitli[]>(() => kayitOku(kayitAnahtari));
  const [ad, setAd] = useState('');
  useEffect(() => { setKayitlar(kayitOku(kayitAnahtari)); }, [kayitAnahtari]);
  const n = suzgecSayisi(deger);
  const yonAd = useMemo(() => new Map(yonler.map((y) => [y.id, y.ad])), [yonler]);

  const degistir = (y: string, v: string) => {
    const s = deger[y] || [];
    onChange({ ...deger, [y]: s.includes(v) ? s.filter((x) => x !== v) : [...s, v] });
  };
  const kaydet = () => {
    const a = ad.trim();
    if (!a || !n) return;
    const l = [{ ad: a, deger, at: new Date().toISOString() }, ...kayitlar.filter((k) => k.ad !== a)];
    setKayitlar(l); kayitYaz(kayitAnahtari, l); setAd('');
  };
  const sil = (a: string) => { const l = kayitlar.filter((k) => k.ad !== a); setKayitlar(l); kayitYaz(kayitAnahtari, l); };

  const panel = (
    <div className="sz15-panel-i">
      {yonler.filter((y) => y.secenekler.length > 1 || (deger[y.id]?.length ?? 0) > 0).map((y) => (
        <fieldset key={y.id} className="sz15-yon">
          <legend className="v15-label">{y.ad}</legend>
          <div className="sz15-sec">
            {y.secenekler.map((s) => {
              const on = (deger[y.id] || []).includes(s.deger);
              return (
                <button key={s.deger} type="button" className={`sz15-cip${on ? ' is-on' : ''}`} aria-pressed={on} onClick={() => degistir(y.id, s.deger)}>
                  <span>{s.deger}</span>{s.n != null && <small>{s.n}</small>}
                </button>
              );
            })}
          </div>
        </fieldset>
      ))}
      <div className="sz15-kayit">
        <span className="v15-label">Kayıtlı süzgeçler</span>
        {kayitlar.length ? (
          <ul role="list">
            {kayitlar.map((k) => (
              <li key={k.ad}>
                <button type="button" className="sz15-kayit-b" onClick={() => { onChange(k.deger); setAcik(false); }}>
                  <Bookmark aria-hidden /><span><b>{k.ad}</b><small>{Object.entries(k.deger).flatMap(([, s]) => s || []).join(' · ') || 'boş'}</small></span>
                </button>
                <button type="button" className="v15-ib" onClick={() => sil(k.ad)} aria-label={`${k.ad} süzgecini sil`}><Trash2 aria-hidden /></button>
              </li>
            ))}
          </ul>
        ) : <p className="v15-cap">Henüz kayıtlı süzgeç yok. Seçim yapıp aşağıdan adlandırarak kaydet.</p>}
        <form className="sz15-kaydet" onSubmit={(e) => { e.preventDefault(); kaydet(); }}>
          <input value={ad} onChange={(e) => setAd(e.target.value)} placeholder={n ? 'Süzgeç adı' : 'Önce seçim yap'} disabled={!n} maxLength={40} aria-label="Süzgeç adı" />
          <button type="submit" className="v15-btn is-soft" disabled={!n || !ad.trim()}>Kaydet</button>
        </form>
      </div>
    </div>
  );

  return (
    <div className="sz15">
      <aside className="sz15-yan v15-card" aria-label="Süzgeç">{panel}</aside>
      <div className="sz15-ana">
        <div className="sz15-cubuk">
          <button type="button" className="v15-btn is-ghost sz15-ac" onClick={() => setAcik(true)}>
            <SlidersHorizontal aria-hidden /> Süzgeç{n ? ` (${n})` : ''}
          </button>
          {n > 0 && (
            <div className="sz15-aktif" aria-label="Etkin süzgeçler">
              {Object.entries(deger).flatMap(([y, s]) => (s || []).map((v) => (
                <button key={`${y}:${v}`} type="button" className="sz15-cip is-on" onClick={() => degistir(y, v)} aria-label={`${yonAd.get(y) || y}: ${v} süzgecini kaldır`}>
                  <span>{v}</span><X aria-hidden />
                </button>
              )))}
              <button type="button" className="sz15-temizle" onClick={() => onChange({})}>Temizle</button>
            </div>
          )}
          {sonuc != null && <span className="v15-cap sz15-sonuc">{sonuc} sonuç</span>}
        </div>
        {children}
      </div>
      {acik && (
        <div className="sz15-perde" onClick={() => setAcik(false)}>
          <div className="sz15-sayfa" role="dialog" aria-modal="true" aria-label="Süzgeç" onClick={(e) => e.stopPropagation()}>
            <div className="sz15-sayfa-b"><b>Süzgeç</b><button type="button" className="v15-ib" onClick={() => setAcik(false)} aria-label="Kapat"><X aria-hidden /></button></div>
            {panel}
            <button type="button" className="v15-btn sz15-tamam" onClick={() => setAcik(false)}>{sonuc != null ? `${sonuc} sonucu göster` : 'Tamam'}</button>
          </div>
        </div>
      )}
    </div>
  );
}
