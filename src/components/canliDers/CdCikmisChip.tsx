// Sesli derste çıkmış soru chip'i (kullanıcı kararı 2026-10-27): elle doğrulanmış çıkmış sorusu olan slaytın sağ
// üstünde yanıp söner; dokununca ses durur, soru tam ekran ya da normal pencerede çözülür, kapanınca ders kaldığı
// yerden sürer. Yalnız `dogrulandi` kayıtlar gösterilir (otomatik vektör eşlemesi yanlış soru bağlayabiliyordu).
import React, { useEffect, useState, useSyncExternalStore } from 'react';
import { createPortal } from 'react-dom';
import { Maximize2, Minimize2, Star, X } from 'lucide-react';
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
  return createPortal(<CikmisPencere sorular={a.sorular} i={a.i} setI={(i) => ayarla({ ...a, i })} onKapat={kapat} />, document.body);
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
                </div>
              )}
            </>
          )}
        </div>
        <div className="cd-cikp-alt">
          {sorular.length > 1 && <button type="button" className="cd-cikp-btn" disabled={i <= 0} onClick={() => setI(i - 1)}>Önceki</button>}
          {sorular.length > 1 && <button type="button" className="cd-cikp-btn" disabled={i >= sorular.length - 1} onClick={() => setI(i + 1)}>Sonraki</button>}
          <span className="cd-grow" />
          <button type="button" className="cd-cikp-btn is-ana" onClick={onKapat}>Derse dön</button>
        </div>
      </div>
    </div>
  );
}
