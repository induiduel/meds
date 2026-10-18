/**
 * Soru çözücü ve En önemliler sayfalarının sade başlangıç ekranları (branş seçilmeden önce).
 * Branş satırına dokununca ?brans=<id> eklenir (geri tuşu buraya döner); "Kaldığın yerden devam" son çalışılan yere götürür.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { BarChart3, Clock, Eraser, Headphones, HelpCircle, Lightbulb, Star } from 'lucide-react';
import { Baslangic, type BaslangicSatir } from '../ui/Baslangic';
import { BRANSLAR, bransTanim, type Brans } from './brans';
import { cozucuDizinYukle, ozet, setAdi, useIlerleme, type CDizin } from './cozucu/cozucuVeri';
import { ONEM_SON_KEY, dizinYukle as onemDizinYukle, useOgrenilen, type Dizin } from './onem/onemVeri';
import { useSpotCozucuStats } from '../../services/spotCozucuIstatistik';
import { getAsistanSureGruplari, getCozucuSureGruplari } from './sure/spotsSureVeri';
import { SpotsSureDiyalog } from './sure/SpotsSureDiyalog';
import { SpotCozucuIstatistikModal } from './stats/SpotCozucuIstatistikModal';
import { cozucuyaGit, onemeGit } from './spotsYol';

const sayi = (n: number) => n.toLocaleString('tr-TR');
const yuzde = (a: number, b: number) => (b ? Math.round((a / b) * 100) : 0);

/** Tüm branşların dizinlerini paralel yükler (her biri birkaç KB) */
const useDizinler = <T,>(yukle: (b: Brans) => Promise<T>) => {
  const [d, setD] = useState<Partial<Record<Brans, T>> | null>(null);
  useEffect(() => {
    let canli = true;
    Promise.all(BRANSLAR.map((b) => yukle(b.id).then((x) => [b.id, x] as const).catch(() => [b.id, null] as const)))
      .then((r) => { if (canli) setD(Object.fromEntries(r.filter(([, x]) => x)) as Partial<Record<Brans, T>>); });
    return () => { canli = false; };
  }, [yukle]);
  return d;
};

/* ── Soru çözücü ─────────────────────────────────────────────────────── */
export const CozucuBaslangic: React.FC = () => {
  const dizinler = useDizinler<CDizin>(cozucuDizinYukle);
  const ilerleme = useIlerleme();
  const stats = useSpotCozucuStats();
  const [sure, setSure] = useState(false);
  const [istatistik, setIstatistik] = useState(false);

  const satirlar = useMemo<BaslangicSatir[] | null>(() => {
    if (!dizinler) return null;
    return BRANSLAR.flatMap((b) => {
      const dz = dizinler[b.id];
      if (!dz?.dersler.length) return [];
      let toplam = 0, cozulen = 0;
      for (const d of dz.dersler) { const o = ozet(ilerleme[d.kod], d.soru); toplam += d.soru; cozulen += Math.min(d.soru, o.cozulen); }
      const konu = new Set(dz.dersler.map((d) => d.no)).size;
      return [{
        id: b.id,
        ad: b.tam,
        alt: `${konu} konu · ${sayi(toplam)} soru${cozulen ? ` · ${sayi(cozulen)} çözüldü` : ''}`,
        pay: toplam ? cozulen / toplam : 0,
        durum: cozulen ? `%${yuzde(cozulen, toplam)}` : undefined,
        onSec: () => cozucuyaGit({ brans: b.id }),
      }];
    });
  }, [dizinler, ilerleme]);

  const toplam = useMemo(() => {
    if (!dizinler) return null;
    let soru = 0;
    for (const dz of Object.values(dizinler)) for (const d of dz?.dersler || []) soru += d.soru;
    return soru;
  }, [dizinler]);

  const son = stats.lastCozucu;
  const sonDers = son ? dizinler?.[son.brans]?.dersler.find((d) => d.kod === son.kod) : undefined;
  const devam = son && (!dizinler || sonDers) && !(sonDers && ozet(ilerleme[sonDers.kod], sonDers.soru).tamam)
    ? {
        etiket: `Kaldığın yerden devam · ${bransTanim(son.brans).ad}`,
        ad: `${son.dersNo}. ${son.baslik}${sonDers && setAdi(sonDers) ? ` · ${setAdi(sonDers)}` : ''}`,
        sag: son.toplamSoru ? `${Math.min(son.soruNo, son.toplamSoru)}/${son.toplamSoru}` : undefined,
        onClick: () => cozucuyaGit({ brans: son.brans, ders: son.kod, coz: '1' }),
      }
    : null;

  return (
    <>
      <Baslangic
        ikon={Headphones}
        baslik="Soru çözücü"
        aciklama="Asistan soruyu ve seçenekleri sesli okur, sen seçersin; sonra her seçeneğin nedenini ders sunumuna dayanarak açıklar."
        ozet={toplam !== null ? <><b>{satirlar?.length ?? 0}</b> ders · <b>{sayi(toplam)}</b> soru{stats.cozulenSoru > 0 && <> · <b>%{stats.dogrulukOrani}</b> doğru</>}</> : undefined}
        devam={devam}
        listeAd="Bir ders seç"
        satirlar={satirlar}
        alt={
          <>
            <details className="bs-nasil">
              <summary><span className="bs-link"><HelpCircle aria-hidden />Nasıl çalışır?</span></summary>
              <ul className="bs-adim">
                <li><Lightbulb aria-hidden /><span><b>İpucu:</b> cevabı söylemeden neyi düşünmen gerektiğini hatırlatır.</span></li>
                <li><Eraser aria-hidden /><span><b>Bir yanlışı ele:</b> bir yanlış seçeneği nedeniyle açıklayıp eler.</span></li>
                <li><Headphones aria-hidden /><span><b>Çözümü dinle:</b> tüm seçenekleri tek tek açıklar, doğru cevabı ve nedenini söyler.</span></li>
              </ul>
            </details>
            <button type="button" className="bs-link" onClick={() => setSure(true)}><Clock aria-hidden />Süreler</button>
            <button type="button" className="bs-link" onClick={() => setIstatistik(true)}><BarChart3 aria-hidden />İstatistikler</button>
          </>
        }
      />
      {sure && (
        <SpotsSureDiyalog
          takipModul="cozucu"
          baslik="Soru çözücü süreleri"
          gruplar={getCozucuSureGruplari()}
          onKapat={() => setSure(false)}
          onDersAc={(b, k) => { setSure(false); cozucuyaGit({ brans: b, ders: k, coz: '1' }); }}
          birimAd="set"
          not="Süreler EMA seslendirmesine göredir. Soru kökü, seçenekler, ipucu, eleme ve detaylı çözüm açıklamalarını içerir."
        />
      )}
      {istatistik && <SpotCozucuIstatistikModal onClose={() => setIstatistik(false)} onBransSec={(b) => { setIstatistik(false); cozucuyaGit({ brans: b }); }} />}
    </>
  );
};

/* ── En önemliler ───────────────────────────────────────────────────── */
export interface OnemSon { brans: Brans; kod: string; baslik: string; no?: number }
const onemSonOku = (): OnemSon | null => {
  try { const v = JSON.parse(localStorage.getItem(ONEM_SON_KEY) || 'null'); return v && v.brans && v.kod ? v : null; } catch { return null; }
};

const kodOfId = (id: string) => id.slice(0, id.lastIndexOf('-'));

export const OnemBaslangic: React.FC = () => {
  const dizinler = useDizinler<Dizin>(onemDizinYukle);
  const ogr = useOgrenilen();
  const [sure, setSure] = useState(false);
  const son = useMemo(onemSonOku, []);

  const ogrKod = useMemo(() => {
    const r: Record<string, number> = {};
    for (const id of ogr) { const k = kodOfId(id); r[k] = (r[k] || 0) + 1; }
    return r;
  }, [ogr]);

  const satirlar = useMemo<BaslangicSatir[] | null>(() => {
    if (!dizinler) return null;
    return BRANSLAR.flatMap((b) => {
      const dz = dizinler[b.id];
      if (!dz?.dersler.length) return [];
      const madde = dz.dersler.reduce((t, d) => t + d.madde, 0);
      const o = dz.dersler.reduce((t, d) => t + Math.min(d.madde, ogrKod[d.kod] || 0), 0);
      return [{
        id: b.id,
        ad: b.tam,
        alt: `${dz.dersler.length} konu · ${sayi(madde)} madde${o ? ` · ${sayi(o)} öğrenildi` : ''}`,
        pay: madde ? o / madde : 0,
        durum: o ? `%${yuzde(o, madde)}` : undefined,
        onSec: () => onemeGit({ brans: b.id }),
      }];
    });
  }, [dizinler, ogrKod]);

  const toplam = useMemo(() => (dizinler ? Object.values(dizinler).reduce((t, dz) => t + (dz?.dersler.reduce((s, d) => s + d.madde, 0) || 0), 0) : null), [dizinler]);
  const devam = son
    ? {
        etiket: `Kaldığın yerden devam · ${bransTanim(son.brans).ad}`,
        ad: son.no ? `${son.no}. ${son.baslik}` : son.baslik,
        onClick: () => onemeGit({ brans: son.brans, ders: son.kod }),
      }
    : null;

  return (
    <>
      <Baslangic
        ikon={Star}
        baslik="En önemliler"
        aciklama="Her konunun sınav için en önemli bilgileri 100 puanlık önem sırasıyla; her madde ders PDF'inden alıntılı. Sesli asistanla da dinleyebilirsin."
        ozet={toplam !== null ? <><b>{sayi(toplam)}</b> madde · <b>{sayi(ogr.size)}</b> öğrenildi</> : undefined}
        devam={devam}
        listeAd="Bir ders seç"
        satirlar={satirlar}
        alt={<button type="button" className="bs-link" onClick={() => setSure(true)}><Clock aria-hidden />Sesli asistan süreleri</button>}
      />
      {sure && (
        <SpotsSureDiyalog
          takipModul="onem"
          baslik="Sesli sınav asistanı ders süreleri"
          gruplar={getAsistanSureGruplari()}
          onKapat={() => setSure(false)}
          onDersAc={(b, k) => { setSure(false); onemeGit({ brans: b, ders: k, asistan: '1' }); }}
        />
      )}
    </>
  );
};
