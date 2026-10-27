// Sesli derste çıkmış soru chip'i (kullanıcı kararı 2026-10-27): elle doğrulanmış çıkmış sorusu olan slaytın sağ
// üstünde yanıp söner; dokununca ses durur, soru tam ekran ya da normal pencerede çözülür, kapanınca ders kaldığı
// yerden sürer. Yalnız `dogrulandi` kayıtlar gösterilir (otomatik vektör eşlemesi yanlış soru bağlayabiliyordu).
import React, { useEffect, useLayoutEffect, useState, useSyncExternalStore } from 'react';
import { createPortal } from 'react-dom';
import { ChevronLeft, ChevronRight, Maximize2, Minimize2, Play, Star, X } from 'lucide-react';
import { useAppearance } from '../../utils/appearance';
import { safeJsonFetch } from '../../services/api';
import { cdDurum, cdDuraklat, cdToggle, type CdCikmisKonum } from './canliDersStore';

interface TekSoru {
  id: string; kok: string; yil?: string | null; konu?: string | null; dogru: string | null; aciklama?: string | null;
  siklar: { k: string; m: string; a?: string | null }[];
}

/** Açıklamadaki **kalın** işaretlerini <b>'ye çevirir (ham yıldız gösterilmez). */
const kalin = (t: string) => t.split(/\*\*(.+?)\*\*/g).map((p, i) => (i % 2 ? <b key={i}>{p}</b> : p));

export function cikmisSayfada(liste: CdCikmisKonum[] | null | undefined, dosya: number, sayfa: number) {
  return (liste || []).filter((q) => q.dogrulandi && q.s === sayfa && (q.d ?? 0) === dosya);
}

// Pencere durumu slayttan bağımsız tutulur: ses durunca görünüm canlı konuma döner ve slayt (chip'le birlikte)
// ekrandan kaldırılabilir; durum chip'te olsaydı pencere kaybolurdu (2026-10-27 sınamasında görüldü).
type Acik = { sorular: CdCikmisKonum[]; i: number; caliyordu: boolean } | null;
let acikDurum: Acik = null;
const dinleyiciler = new Set<() => void>();
const ayarla = (a: Acik) => { acikDurum = a; dinleyiciler.forEach((f) => f()); };
const abone = (f: () => void) => { dinleyiciler.add(f); return () => { dinleyiciler.delete(f); }; };
// Yalnız geliştirme derlemesinde: kartı tarayıcı sınamasında açmak için (üretim paketine girmez)
if (import.meta.env.DEV && typeof window !== 'undefined') (window as unknown as { __cdCikmisAc?: (s: CdCikmisKonum[]) => void }).__cdCikmisAc = (s) => ayarla({ sorular: s, i: 0, caliyordu: false });

/** Çıkmış penceresini dışarıdan aç (oynatıcı şeridi, tasarım S21): çalıyorsa durur, kapanınca sürer */
export function cdCikmisAc(sorular: CdCikmisKonum[]) {
  if (!sorular.length) return;
  const caliyor = cdDurum().playing;
  if (caliyor) cdDuraklat();
  ayarla({ sorular, i: 0, caliyordu: caliyor });
}

export function CdCikmisChip({ sorular }: { sorular: CdCikmisKonum[] }) {
  if (!sorular.length) return null;
  const ac = (e: React.MouseEvent) => {
    e.stopPropagation();
    const caliyor = cdDurum().playing;
    if (caliyor) cdDuraklat();
    ayarla({ sorular, i: 0, caliyordu: caliyor });
  };
  const dogrudan = sorular.some((q) => q.seviye !== 'ilgili');
  return (
    <button type="button" className={`cd-cikc${dogrudan ? '' : ' is-ilgili'}`} onClick={ac} onPointerDown={(e) => e.stopPropagation()}
      title={dogrudan ? 'Bu slayttaki bilgi çıkmış sınavda soruldu — dokun, çöz' : 'Bu slaytla ilişkili çıkmış soru — dokun, çöz'}>
      <Star aria-hidden /> Çıkmış{sorular.length > 1 ? ` ${sorular.length}` : ''}
    </button>
  );
}

/** Ders ekranında bir kez bulunur; açık çıkmış penceresini belge köküne çizer. */
export function CdCikmisPencereKok() {
  const a = useSyncExternalStore(abone, () => acikDurum);
  useEffect(() => () => ayarla(null), []);
  if (!a) return null;
  const kapat = () => {
    ayarla(null);
    if (a.caliyordu && !cdDurum().playing) cdToggle();
  };
  const setI = (i: number) => ayarla({ ...a, i });
  return createPortal(
    <CikmisSecim sorular={a.sorular} i={a.i} setI={setI} onKapat={kapat} />,
    document.body,
  );
}

/** v15'te kompakt kart (tasarım sistemi v15 › S2 · V/W), diğer tasarımlarda eski pencere */
function CikmisSecim(p: { sorular: CdCikmisKonum[]; i: number; setI: (i: number) => void; onKapat: () => void }) {
  const { v15 } = useAppearance();
  return v15 ? <CikmisKart {...p} /> : <CikmisPencere {...p} />;
}

/** Soru verisini çeker; kart ve pencere aynı akışı kullanır */
function useTekSoru(id: string) {
  const [veri, setVeri] = useState<TekSoru | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const [secim, setSecim] = useState<string | null>(null);
  useEffect(() => {
    let iptal = false;
    setVeri(null); setHata(null); setSecim(null);
    safeJsonFetch<TekSoru>(`/api/past-exams/tek/${encodeURIComponent(id)}`)
      .then((r) => { if (iptal) return; if (r.ok && r.data) setVeri(r.data); else setHata('Soru yüklenemedi.'); })
      .catch(() => { if (!iptal) setHata('Soru yüklenemedi.'); });
    return () => { iptal = true; };
  }, [id]);
  return { veri, hata, secim, setSecim };
}

/**
 * v15 kompakt çıkmış kartı: tam ekran diyalog yerine metin bölmesinin üstünde (telefonda oynatıcının üstünde) açılır;
 * PDF ve sorunun dayandığı yer görünür kalır. Cevaptan sonra yalnız doğru ve seçilen şık kalır (telefonda), sonuç tek
 * satır, açıklama 3 satır ("Devamı" ile tamamı), "Derse dön" sesi kaldığı yerden sürdürür.
 */
function CikmisKart({ sorular, i, setI, onKapat }: { sorular: CdCikmisKonum[]; i: number; setI: (i: number) => void; onKapat: () => void }) {
  const q = sorular[i];
  const { veri, hata, secim, setSecim } = useTekSoru(q.id);
  const [uzun, setUzun] = useState(false);
  useEffect(() => setUzun(false), [q.id]);
  useEffect(() => {
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') onKapat(); };
    window.addEventListener('keydown', k);
    return () => window.removeEventListener('keydown', k);
  }, [onKapat]);
  const cozuldu = secim != null;
  const dogru = cozuldu && veri ? secim === veri.dogru : false;
  const cok = sorular.length > 1;
  // Kart belge kökünde: oynatıcının (cd-dock) üstünde kalsın diye alt boşluk oynatıcının gerçek konumundan ölçülür
  const [alt, setAlt] = useState(12);
  useLayoutEffect(() => {
    const olc = () => {
      const kart = [...document.querySelectorAll<HTMLElement>('.cd-dock > *')].find((e) => e.offsetHeight > 0);
      setAlt(kart ? Math.max(12, Math.round(window.innerHeight - kart.getBoundingClientRect().top + 10)) : 12);
    };
    olc();
    window.addEventListener('resize', olc);
    return () => window.removeEventListener('resize', olc);
  }, []);
  return (
    <div className="cd15-cq-kat" role="presentation" onClick={onKapat} style={{ '--cd15-cq-alt': `${alt}px` } as React.CSSProperties}>
      <div className="cd15-cq" role="dialog" aria-modal="true" aria-label="Çıkmış soru" onClick={(e) => e.stopPropagation()}>
        <div className="cd15-cq-bas">
          <span className="cd15-cq-et"><Star aria-hidden /> Çıkmış soru{q.yil ? ` · ${q.yil}` : ''}{q.seviye === 'ilgili' ? ' · ilişkili' : ''}</span>
          {cok && <span className="cd15-cq-no">{i + 1}/{sorular.length}</span>}
          {cok && <button type="button" className="v15-ib" disabled={i <= 0} onClick={() => setI(i - 1)} aria-label="Önceki soru"><ChevronLeft aria-hidden /></button>}
          {cok && <button type="button" className="v15-ib" disabled={i >= sorular.length - 1} onClick={() => setI(i + 1)} aria-label="Sonraki soru"><ChevronRight aria-hidden /></button>}
          <button type="button" className="v15-ib" onClick={onKapat} aria-label="Kapat ve derse dön"><X aria-hidden /></button>
        </div>
        <div className="cd15-cq-govde">
          {hata ? <p className="cd15-cq-not">{hata}</p> : !veri ? <span className="v15-skel cd15-cq-iskelet" aria-label="Yükleniyor" /> : (
            <>
              <p className="cd15-cq-kok">{veri.kok}</p>
              <div className="cd15-cq-siklar" role="radiogroup" aria-label="Şıklar">
                {veri.siklar.map((s) => {
                  const d = s.k === veri.dogru;
                  const cls = !cozuldu ? '' : d ? ' is-dogru' : s.k === secim ? ' is-yanlis' : ' is-soluk';
                  return (
                    <button key={s.k} type="button" role="radio" aria-checked={s.k === secim} disabled={cozuldu} className={`cd15-cq-sik${cls}`} onClick={() => setSecim(s.k)}>
                      <b>{s.k}</b>
                      <span>{s.m}{cozuldu && s.a && (d || s.k === secim) && <small>{s.a}</small>}</span>
                    </button>
                  );
                })}
              </div>
              {cozuldu && (
                <div className="cd15-cq-sonuc">
                  <b className={dogru ? 'is-dogru' : 'is-yanlis'}>{dogru ? 'Doğru' : `Yanlış · doğru cevap ${veri.dogru}`}</b>
                  {veri.aciklama && (
                    <>
                      <p className={uzun ? '' : 'is-kisa'}>{kalin(veri.aciklama)}</p>
                      {!uzun && veri.aciklama.length > 180 && <button type="button" className="cd15-cq-devam" onClick={() => setUzun(true)}>Devamı</button>}
                    </>
                  )}
                  {q.kanit && <p className="cd15-cq-kanit">Slayttaki dayanak: “{q.kanit}”</p>}
                </div>
              )}
            </>
          )}
        </div>
        <div className="cd15-cq-alt">
          <span className="cd15-cq-not">{cozuldu ? (cok && i < sorular.length - 1 ? `${i + 2}. soru hazır` : '') : 'Ses duraklatıldı; cevaplayınca kaldığın yerden sürer.'}</span>
          {cozuldu && cok && i < sorular.length - 1 && <button type="button" className="v15-btn is-soft" onClick={() => setI(i + 1)}>Sonraki</button>}
          <button type="button" className={`v15-btn${cozuldu ? '' : ' is-soft'}`} onClick={onKapat}><Play aria-hidden /> Derse dön</button>
        </div>
      </div>
    </div>
  );
}

function CikmisPencere({ sorular, i, setI, onKapat }: { sorular: CdCikmisKonum[]; i: number; setI: (i: number) => void; onKapat: () => void }) {
  const q = sorular[i];
  const [tam, setTam] = useState(false);
  const [veri, setVeri] = useState<TekSoru | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const [secim, setSecim] = useState<string | null>(null);
  useEffect(() => {
    let iptal = false;
    setVeri(null); setHata(null); setSecim(null);
    safeJsonFetch<TekSoru>(`/api/past-exams/tek/${encodeURIComponent(q.id)}`)
      .then((r) => { if (iptal) return; if (r.ok && r.data) setVeri(r.data); else setHata('Soru yüklenemedi.'); })
      .catch(() => { if (!iptal) setHata('Soru yüklenemedi.'); });
    return () => { iptal = true; };
  }, [q.id]);
  useEffect(() => {
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') onKapat(); };
    window.addEventListener('keydown', k);
    return () => window.removeEventListener('keydown', k);
  }, [onKapat]);
  const cozuldu = secim != null;
  return (
    <div className="cd-cikp-zemin" role="presentation" onClick={onKapat}>
      <div className={`cd-cikp${tam ? ' is-tam' : ''}`} role="dialog" aria-modal="true" aria-label="Çıkmış soru" onClick={(e) => e.stopPropagation()}>
        <div className="cd-cikp-bas">
          <span className="cd-cikp-etiket"><Star aria-hidden /> Çıkmış soru{q.yil ? ` · ${q.yil}` : ''}{q.seviye === 'ilgili' ? ' · ilişkili' : ''}</span>
          {sorular.length > 1 && <span className="cd-cikp-no">{i + 1}/{sorular.length}</span>}
          <span className="cd-grow" />
          <button type="button" className="cd-ib" onClick={() => setTam((t) => !t)} aria-label={tam ? 'Normal ekran' : 'Tam ekran'}>{tam ? <Minimize2 /> : <Maximize2 />}</button>
          <button type="button" className="cd-ib" onClick={onKapat} aria-label="Kapat ve derse dön"><X /></button>
        </div>
        <div className="cd-cikp-govde">
          {hata ? <p className="cd-cikp-hata">{hata}</p> : !veri ? <p className="cd-cikp-yuk">Yükleniyor…</p> : (
            <>
              <p className="cd-cikp-kok">{veri.kok}</p>
              <div className="cd-cikp-siklar" role="radiogroup" aria-label="Şıklar">
                {veri.siklar.map((s) => {
                  const dogru = s.k === veri.dogru;
                  const cls = !cozuldu ? '' : dogru ? ' is-dogru' : s.k === secim ? ' is-yanlis' : ' is-soluk';
                  return (
                    <button key={s.k} type="button" role="radio" aria-checked={s.k === secim} disabled={cozuldu}
                      className={`cd-cikp-sik${cls}`} onClick={() => setSecim(s.k)}>
                      <b>{s.k}</b><span>{s.m}{cozuldu && s.a && (dogru || s.k === secim) && <small>{s.a}</small>}</span>
                    </button>
                  );
                })}
              </div>
              {cozuldu && (
                <div className="cd-cikp-sonuc">
                  <b className={secim === veri.dogru ? 'is-dogru' : 'is-yanlis'}>{secim === veri.dogru ? 'Doğru' : `Yanlış — doğru cevap ${veri.dogru}`}</b>
                  {veri.aciklama && <p>{kalin(veri.aciklama)}</p>}
                  {q.kanit && <p className="cd-cikp-kanit">Slayttaki dayanak: “{q.kanit}”</p>}
                  {q.kaynak && <p className="cd-cikp-kanit">Kaynak: {q.kaynak}</p>}
                </div>
              )}
            </>
          )}
        </div>
        <div className="cd-cikp-alt">
          {sorular.length > 1 && <button type="button" className="cd-cikp-btn" disabled={i <= 0} onClick={() => setI(i - 1)}>Önceki</button>}
          {sorular.length > 1 && <button type="button" className="cd-cikp-btn" disabled={i >= sorular.length - 1} onClick={() => setI(i + 1)}>Sonraki</button>}
          <span className="cd-grow" />
          {/* Kullanıcı isteği 2026-10-27: soruyu çıkmış sorular bölümünde ayrıca görüntüle (yeni sekme; ders burada bekler) */}
          <a className="cd-cikp-btn" href={`/sorular/cikmis/${encodeURIComponent(q.id)}`} target="_blank" rel="noopener">Çıkmış soruyu görüntüle</a>
          <button type="button" className="cd-cikp-btn is-ana" onClick={onKapat}>Derse dön</button>
        </div>
      </div>
    </div>
  );
}
