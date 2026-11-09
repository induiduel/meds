/**
 * Bağlantı katmanları (H525): kendi kopukluğumuz (deneme + geri sayım), sırası olan oyuncunun kopukluğu,
 * kopuk rakiplerin süresi ve izleyici / koltuk isteği şeridi. Kişi her an ne olduğunu ve ne beklediğini görür.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import { Bot, Eye, RefreshCw, UserCheck, WifiOff, X } from 'lucide-react';
import { masa, useMasa } from '../../services/masa/istemci';
import type { OdaGorunum } from '../../services/masa/tipler';
import { sadeAd } from './kabukOrtak';

/** Saniyede bir yenilenen saat */
function useSaat(acik = true) {
  const [simdi, setSimdi] = useState(Date.now());
  useEffect(() => {
    if (!acik) return;
    setSimdi(Date.now()); // kapalıyken eskiyen saat açılınca hemen tazelenir
    const i = setInterval(() => setSimdi(Date.now()), 1000);
    return () => clearInterval(i);
  }, [acik]);
  return simdi;
}
const dkSn = (sn: number) => `${Math.floor(sn / 60)}:${String(Math.max(0, sn) % 60).padStart(2, '0')}`;

/** Kopuk oyuncuların süresi: sunucu yayın anındaki saniyeyi yollar, aradaki süre yerelde eklenir */
function useKopSure(oda: OdaGorunum) {
  const alindi = useMemo(() => Date.now(), [oda.surum]); // eslint-disable-line react-hooks/exhaustive-deps
  const kopuklar = oda.oyuncular.filter((o) => !o.bot && !o.bagli && o.id !== oda.ben);
  const simdi = useSaat(kopuklar.length > 0);
  return kopuklar.map((o) => ({ o, sn: (o.kopSn || 0) + Math.floor((simdi - alindi) / 1000) }));
}

/** Kendi bağlantımız koptu: masanın üstünde deneme sayısı ve sonraki denemeye geri sayım */
export function KopukKatman() {
  const { baglanti, deneme, sonrakiDeneme } = useMasa();
  const kopuk = baglanti !== 'hazir';
  // Çok kısa kopukluklarda (≤1,2 sn) ekran oynamasın
  const [gorun, setGorun] = useState(false);
  useEffect(() => {
    if (!kopuk) { setGorun(false); return; }
    const t = setTimeout(() => setGorun(true), 1200);
    return () => clearTimeout(t);
  }, [kopuk]);
  const simdi = useSaat(gorun);
  const kalan = Math.max(0, Math.ceil((sonrakiDeneme - simdi) / 1000));
  return (
    <AnimatePresence>
      {kopuk && (
        gorun ? (
          <motion.div key="katman" className="mk-kopuk-katman" role="alertdialog" aria-live="assertive" aria-label="Bağlantı koptu"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.2 }}>
            <div className="mk-kopuk-kutu">
              <span className="mk-kopuk-ikon"><WifiOff size={28} /></span>
              <h3>Bağlantı koptu</h3>
              <p>
                {baglanti === 'koptu' && sonrakiDeneme && kalan > 0
                  ? <>Yeniden bağlanılıyor ({deneme}. deneme) — <b>{kalan} sn</b> sonra yeniden denenecek.</>
                  : <>Yeniden bağlanılıyor{deneme ? ` (${deneme}. deneme)` : ''}…</>}
              </p>
              <small>Koltuğun masada duruyor; bağlanınca oyun kaldığı yerden sürer. Bu sırada sıra sana gelirse diğerleri seni bekler.</small>
              <button type="button" className="mk-dugme is-ana" onClick={() => masa.simdiDene()} disabled={baglanti !== 'koptu'}><RefreshCw size={18} /> Şimdi dene</button>
            </div>
          </motion.div>
        ) : (
          <motion.div key="serit" className="mk-serit" role="status" initial={{ y: -40, opacity: 0 }} animate={{ y: 0, opacity: 1 }} exit={{ y: -40, opacity: 0 }} transition={{ duration: 0.22 }}>
            <WifiOff size={16} /> Yeniden bağlanılıyor…
          </motion.div>
        )
      )}
    </AnimatePresence>
  );
}

/** Rakiplerin bağlantı durumu: kopuk koltuk rozetleri ve sırası kopuk oyuncudaysa bekleme kartı */
export function RakipBaglanti({ oda }: { oda: OdaGorunum }) {
  const kopuklar = useKopSure(oda);
  const kurucu = oda.kurucu === oda.ben;
  const oyunda = oda.asama === 'oyun' && !oda.durdu;
  const siradaki = oyunda ? kopuklar.find((k) => k.o.id === oda.oyun?.sira) : undefined;
  if (!kopuklar.length) return null;
  return (
    <>
      <ul className="mk-kopuk-rozetler" aria-label="Bağlantısı kopan oyuncular">
        {kopuklar.map(({ o, sn }) => (
          <li key={o.id} className={sn >= 60 ? 'is-uzun' : ''}>
            <WifiOff size={13} aria-hidden="true" /> <b>{sadeAd(o.ad)}</b> bağlantı bekleniyor <time>{dkSn(sn)}</time>
          </li>
        ))}
      </ul>
      <AnimatePresence>
        {siradaki && (
          <motion.div key={siradaki.o.id} className="mk-sira-bekle" role="status" aria-live="polite"
            initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.96 }} transition={{ duration: 0.18 }}>
            <span className="mk-donen" />
            <div>
              <b>{sadeAd(siradaki.o.ad)}’in bağlantısı bekleniyor</b>
              <small>Sıra onda ve bağlantısı {dkSn(siradaki.sn)} önce koptu. Geri gelince oyun kaldığı yerden sürer.</small>
            </div>
            {kurucu
              ? <button type="button" className="mk-dugme is-ana" onClick={() => masa.botDevral(siradaki.o.id)}><Bot size={18} /> Bot devralsın</button>
              : <small className="mk-sira-bekle-not">Kurucu isterse yerine bot oynatabilir.</small>}
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

/** İzleyici şeridi: izleyiciye koltuk isteme, kurucuya gelen istekleri onaylama */
export function IzleyiciSerit({ oda }: { oda: OdaGorunum }) {
  const [ac, setAc] = useState(false);
  const kurucu = oda.kurucu === oda.ben;
  const botlar = oda.oyuncular.filter((o) => o.bot);
  const benimIstek = oda.izleyiciler?.find((i) => i.id === oda.ben)?.istek;
  const istekler = kurucu ? (oda.izleyiciler || []).filter((i) => i.istek) : [];
  const devrilebilir = oda.asama === 'oyun' || oda.asama === 'elSonu';

  if (oda.izliyor) {
    return (
      <div className="mk-izle-serit" role="status">
        <Eye size={16} aria-hidden="true" />
        <span>
          <b>İzliyorsun.</b>{' '}
          {benimIstek ? `${sadeAd(oda.oyuncular.find((o) => o.id === benimIstek)?.ad || 'Bot')} koltuğu için kurucunun onayı bekleniyor…`
            : !devrilebilir ? 'Maç sürmüyor.'
            : botlar.length ? 'Oynamak istersen bot oynayan bir koltuğu iste; kurucu onaylayınca o koltuktan devam edersin.'
            : 'Masada bot yok; biri kalkarsa koltuğunu isteyebilirsin.'}
        </span>
        {devrilebilir && !benimIstek && botlar.length > 0 && (
          ac ? (
            <span className="mk-izle-secim">
              {botlar.map((o) => <button key={o.id} type="button" className="mk-cip" onClick={() => { setAc(false); masa.koltukIste(o.id); }}>{sadeAd(o.ad)}</button>)}
              <button type="button" className="mk-ikon-dugme" onClick={() => setAc(false)} aria-label="Vazgeç"><X size={16} /></button>
            </span>
          ) : <button type="button" className="mk-dugme is-ana" onClick={() => setAc(true)}><UserCheck size={16} /> Koltuk iste</button>
        )}
      </div>
    );
  }
  if (!istekler.length) return null;
  return (
    <div className="mk-izle-serit is-istek" role="status">
      {istekler.map((i) => (
        <span key={i.id} className="mk-izle-istek">
          <span><b>{sadeAd(i.ad)}</b> {sadeAd(oda.oyuncular.find((o) => o.id === i.istek)?.ad || 'bot')} koltuğunda oynamak istiyor.</span>
          <button type="button" className="mk-dugme is-ana" onClick={() => masa.koltukVer(i.id, i.istek)}><UserCheck size={16} /> Onayla</button>
          <button type="button" className="mk-dugme is-soluk" onClick={() => masa.koltukRed(i.id)}>Şimdi değil</button>
        </span>
      ))}
    </div>
  );
}
