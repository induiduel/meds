import React, { useEffect, useMemo, useState } from 'react';

export type AlanTuru = 'metin' | 'uzun' | 'sayi' | 'secim' | 'anahtar' | 'etiketler' | 'tarih' | 'json';
export type AlanTanim = {
  ad: string;
  etiket: string;
  tur?: AlanTuru;
  secenekler?: { deger: string; etiket: string }[];
  zorunlu?: boolean;
  enFazla?: number;
  enAz?: number;
  desen?: RegExp;
  ipucu?: React.ReactNode;
  salt?: boolean;
  yerTutucu?: string;
  /** Özel doğrulama: hata metni ya da null */
  dogrula?: (v: unknown, tum: Record<string, unknown>) => string | null;
};

const esit = (a: unknown, b: unknown) => JSON.stringify(a ?? null) === JSON.stringify(b ?? null);

function alanHatasi(a: AlanTanim, v: unknown, tum: Record<string, unknown>): string | null {
  const bos = v === undefined || v === null || v === '' || (Array.isArray(v) && !v.length);
  if (a.zorunlu && bos) return 'Zorunlu alan';
  if (!bos && a.tur === 'sayi') {
    const n = Number(v);
    if (!Number.isFinite(n)) return 'Sayı olmalı';
    if (a.enAz !== undefined && n < a.enAz) return `En az ${a.enAz}`;
    if (a.enFazla !== undefined && n > a.enFazla) return `En fazla ${a.enFazla}`;
  }
  if (!bos && typeof v === 'string') {
    if (a.enFazla !== undefined && a.tur !== 'sayi' && v.length > a.enFazla) return `En fazla ${a.enFazla} karakter`;
    if (a.desen && !a.desen.test(v)) return 'Biçim geçersiz';
    if (a.tur === 'json') { try { JSON.parse(v); } catch { return 'Geçersiz JSON'; } }
  }
  return a.dogrula ? a.dogrula(v, tum) : null;
}

/** Kirli durumda sekme kapatma/yenilemede tarayıcı uyarısı */
export function useKirliUyari(kirli: boolean) {
  useEffect(() => {
    if (!kirli) return;
    const f = (e: BeforeUnloadEvent) => { e.preventDefault(); e.returnValue = ''; };
    window.addEventListener('beforeunload', f);
    return () => window.removeEventListener('beforeunload', f);
  }, [kirli]);
}

/**
 * Şema güdümlü form. kaydet yalnız değişen alanları da alabilir (ikinci argüman).
 * kirliDegisti: üst bileşen (çekmece) kapanışta uyarmak için kirli durumu öğrenir.
 */
export const Form: React.FC<{
  alanlar: AlanTanim[];
  deger: Record<string, unknown>;
  kaydet: (yeni: Record<string, unknown>, degisen: Record<string, unknown>) => void | Promise<void>;
  iptal?: () => void;
  kaydetMetni?: string;
  kirliDegisti?: (kirli: boolean) => void;
}> = ({ alanlar, deger, kaydet, iptal, kaydetMetni = 'Kaydet', kirliDegisti }) => {
  const baslangic = useMemo(() => {
    const o: Record<string, unknown> = { ...deger };
    for (const a of alanlar) if (a.tur === 'json' && typeof o[a.ad] !== 'string') o[a.ad] = JSON.stringify(o[a.ad] ?? null, null, 2);
    return o;
  }, [deger, alanlar]);
  const [d, setD] = useState(baslangic);
  const [dokunuldu, setDokunuldu] = useState<Set<string>>(new Set());
  const [mesgul, setMesgul] = useState(false);
  const [sunucuHata, setSunucuHata] = useState('');
  useEffect(() => { setD(baslangic); setDokunuldu(new Set()); }, [baslangic]);

  const hatalar = useMemo(() => Object.fromEntries(alanlar.map((a) => [a.ad, alanHatasi(a, d[a.ad], d)])), [alanlar, d]);
  const degisen = useMemo(() => Object.fromEntries(alanlar.filter((a) => !esit(d[a.ad], baslangic[a.ad])).map((a) => {
    if (a.tur !== 'json') return [a.ad, d[a.ad]];
    try { return [a.ad, JSON.parse(String(d[a.ad] || 'null'))]; } catch { return [a.ad, d[a.ad]]; }
  })), [alanlar, d, baslangic]);
  const kirli = Object.keys(degisen).length > 0;
  const gecerli = Object.values(hatalar).every((h) => !h);
  useKirliUyari(kirli);
  useEffect(() => { kirliDegisti?.(kirli); }, [kirli, kirliDegisti]);

  const ayarla = (ad: string, v: unknown) => { setD((x) => ({ ...x, [ad]: v })); setDokunuldu((s) => new Set(s).add(ad)); };

  const gonder = async (e: React.FormEvent) => {
    e.preventDefault();
    setDokunuldu(new Set(alanlar.map((a) => a.ad)));
    if (!gecerli || !kirli) return;
    setMesgul(true);
    setSunucuHata('');
    try {
      const yeni: Record<string, unknown> = { ...d };
      for (const a of alanlar) {
        if (a.tur === 'json') yeni[a.ad] = JSON.parse(String(d[a.ad] || 'null'));
        if (a.tur === 'sayi' && d[a.ad] !== '' && d[a.ad] != null) yeni[a.ad] = Number(d[a.ad]);
      }
      await kaydet(yeni, degisen);
    } catch (err: any) {
      setSunucuHata(err?.message || 'Kaydedilemedi');
    } finally {
      setMesgul(false);
    }
  };

  return (
    <form className="m16-form" onSubmit={gonder} noValidate>
      {alanlar.map((a) => {
        const id = `m16f-${a.ad}`;
        const h = dokunuldu.has(a.ad) ? hatalar[a.ad] : null;
        const v = d[a.ad];
        const ortak = { id, disabled: a.salt, 'aria-invalid': Boolean(h), 'aria-describedby': h ? `${id}-h` : undefined };
        let girdi: React.ReactNode;
        switch (a.tur || 'metin') {
          case 'uzun': girdi = <textarea {...ortak} className="m16-girdi" rows={4} value={String(v ?? '')} placeholder={a.yerTutucu} onChange={(e) => ayarla(a.ad, e.target.value)} />; break;
          case 'json': girdi = <textarea {...ortak} className="m16-girdi m16-kod" rows={8} value={String(v ?? '')} spellCheck={false} onChange={(e) => ayarla(a.ad, e.target.value)} />; break;
          case 'sayi': girdi = <input {...ortak} className="m16-girdi" type="number" inputMode="decimal" value={v === undefined || v === null ? '' : String(v)} onChange={(e) => ayarla(a.ad, e.target.value)} />; break;
          case 'tarih': girdi = <input {...ortak} className="m16-girdi" type="date" value={String(v ?? '').slice(0, 10)} onChange={(e) => ayarla(a.ad, e.target.value)} />; break;
          case 'secim': girdi = (
            <select {...ortak} className="m16-girdi" value={String(v ?? '')} onChange={(e) => ayarla(a.ad, e.target.value)}>
              {!a.zorunlu && <option value="">—</option>}
              {(a.secenekler || []).map((o) => <option key={o.deger} value={o.deger}>{o.etiket}</option>)}
            </select>
          ); break;
          case 'anahtar': girdi = (
            <button type="button" id={id} role="switch" aria-checked={v === true} disabled={a.salt} className={`m16-anahtar ${v === true ? 'on' : ''}`} onClick={() => ayarla(a.ad, v !== true)}><i aria-hidden="true" /></button>
          ); break;
          case 'etiketler': girdi = <input {...ortak} className="m16-girdi" value={Array.isArray(v) ? v.join(', ') : String(v ?? '')} placeholder="virgülle ayırın" onChange={(e) => ayarla(a.ad, e.target.value.split(',').map((x) => x.trim()).filter(Boolean))} />; break;
          default: girdi = <input {...ortak} className="m16-girdi" value={String(v ?? '')} placeholder={a.yerTutucu} onChange={(e) => ayarla(a.ad, e.target.value)} />;
        }
        return (
          <div key={a.ad} className={`m16-alan ${a.tur === 'anahtar' ? 'yatay' : ''}`}>
            <label htmlFor={id}>{a.etiket}{a.zorunlu && <span aria-hidden="true"> *</span>}</label>
            {girdi}
            {a.ipucu && !h && <small className="m16-alan-ipucu">{a.ipucu}</small>}
            {h && <small id={`${id}-h`} className="m16-alan-hata">{h}</small>}
          </div>
        );
      })}
      {sunucuHata && <p className="m16-alan-hata" role="alert">{sunucuHata}</p>}
      <div className="m16-form-eylem">
        {kirli && <span className="m16-kirli">Kaydedilmemiş değişiklik</span>}
        {iptal && <button type="button" className="m16-btn hayalet" onClick={iptal}>Vazgeç</button>}
        <button type="submit" className="m16-btn birincil" disabled={!kirli || mesgul}>{mesgul ? 'Kaydediliyor…' : kaydetMetni}</button>
      </div>
    </form>
  );
};
