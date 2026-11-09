/**
 * Taş Masası kabuğu: bağlantı ömrü + duruma göre ekran (merkez → lobi → oyun katmanı).
 * Oyun sırasında gövdeye taşınan tam ekran `.mk-kabuk` çizilir; masa içini okey/ ve uno/ bileşenleri çizer.
 */
import React, { Suspense, useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence, motion } from 'motion/react';
import { Pause, Play, RefreshCw, WifiOff } from 'lucide-react';
import { masa, useMasa } from '../../services/masa/istemci';
import { OYUN_ADI, type OdaGorunum, type OyunTur } from '../../services/masa/tipler';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import { azHareket, sesCal } from './ortak';
import { Bildirimler, HataSiniri, Yaprak, bildir, sadeAd } from './kabukOrtak';
import MasaMerkez from './MasaMerkez';
import MasaLobi from './MasaLobi';
import MasaUstCubuk from './MasaUstCubuk';
import { ElSonu, MacSonu } from './MasaSonuc';
import MasaIstatistik from './MasaIstatistik';
import type { KuralSekme } from './MasaKurallar';
import '../../styles/masa/kabuk.css';
import '../../styles/masa/kabuk-oyun.css';

const OkeyMasa = React.lazy(() => import('./okey/OkeyMasa'));
const UnoMasa = React.lazy(() => import('./uno/UnoMasa'));
const MasaKurallar = React.lazy(() => import('./MasaKurallar'));

const SON_KEY = 'medsoru_masa_son';
const KOD = /^[A-Z0-9]{5}$/;
/** "Merkeze dön (oyun sürsün)": koltuk sunucuda kalır, bu sekme kendiliğinden geri oturmaz */
let ayrik = false;

interface Ucan { id: number; e: string; ad: string; x: number }

export default function MasaView() {
  const { oda, baglanti, hata, gecikme } = useMasa();
  const [kurallar, setKurallar] = useState<KuralSekme | null>(null);
  const [istat, setIstat] = useState(false);
  const [kalici, setKalici] = useState<{ mesaj: string; kod: string } | null>(null);
  const [ucanlar, setUcanlar] = useState<Ucan[]>([]);
  const botPlan = useRef(0);
  const sessiz = useRef(false);
  const ucanNo = useRef(0);

  // Bağlantı ömrü + adresle / yarım kalan masaya kendiliğinden oturma
  useEffect(() => {
    const p = new URLSearchParams(window.location.search);
    const kod = (p.get('masa') || '').trim().toUpperCase();
    if (p.has('masa')) {
      p.delete('masa');
      const s = p.toString();
      window.history.replaceState(window.history.state, '', window.location.pathname + (s ? `?${s}` : '') + window.location.hash);
    }
    let son = '';
    try { son = localStorage.getItem(SON_KEY) || ''; } catch { /* yok */ }
    if (KOD.test(kod)) { ayrik = false; masa.katil(kod); }
    else if (ayrik) { /* kullanıcı masa seçene dek bağlanma */ }
    else if (KOD.test(son)) { sessiz.current = true; masa.katil(son); }
    else masa.baglan();
    return () => masa.kapat();
  }, []);

  // Sunucu hataları
  useEffect(() => {
    if (!hata) return;
    if (sessiz.current && (hata.kod === 'oda-yok' || hata.kod === 'basladi' || hata.kod === 'dolu')) {
      sessiz.current = false;
      try { localStorage.removeItem(SON_KEY); } catch { /* yok */ }
      masa.hataSil();
      return;
    }
    botPlan.current = 0;
    if (hata.kod === 'kimlik' || hata.kod === 'kapali') setKalici({ mesaj: hata.mesaj, kod: hata.kod });
    else { bildir(hata.mesaj, 'hata', 3600); sesCal('hata'); }
  }, [hata]);

  useEffect(() => {
    if (!oda) return;
    sessiz.current = false; ayrik = false;
    setKalici(null);
    // Bota karşı: masa kurulunca botlar eklenir ve oyun hemen başlar
    if (botPlan.current && oda.asama === 'lobi' && oda.kurucu === oda.ben && oda.oyuncular.length === 1) {
      const n = botPlan.current;
      botPlan.current = 0;
      for (let i = 0; i < n; i++) masa.botEkle();
      masa.baslat();
    }
  }, [oda?.kod, oda?.asama]); // eslint-disable-line react-hooks/exhaustive-deps

  // Oda olayları: kısa bildirim + uçan tepki (durumun kaynağı değil)
  useEffect(() => masa.olayDinle((olaylar, yeni, onceki) => {
    const ad = (id?: string) => sadeAd((id && (yeni.oyuncular.find((o) => o.id === id) || onceki?.oyuncular.find((o) => o.id === id))?.ad) || 'Oyuncu');
    for (const o of olaylar) {
      if (o.t === 'tepki' && typeof o.e === 'string') {
        const id = ++ucanNo.current;
        setUcanlar((l) => [...l.slice(-7), { id, e: o.e as string, ad: o.o === yeni.ben ? 'Sen' : ad(o.o), x: 12 + ((id * 37) % 70) }]);
        setTimeout(() => setUcanlar((l) => l.filter((u) => u.id !== id)), 2200);
        if (o.o !== yeni.ben) sesCal('tepki');
      } else if (o.t === 'katildi' && o.o !== yeni.ben) bildir(`${ad(o.o)} masaya ${yeni.asama === 'lobi' ? 'katıldı' : 'geri döndü'}.`, 'iyi');
      else if (o.t === 'botDevraldi') bildir(`${ad(o.o)} yerine bot oynuyor.`);
      else if (o.t === 'ayrildi' && o.o !== yeni.ben && !olaylar.some((x) => x.t === 'botDevraldi' && x.o === o.o)) bildir(`${ad(o.o)} masadan ayrıldı.`);
      else if (o.t === 'durdu') bildir(o.o === yeni.ben ? 'Oyunu durdurdun.' : 'Kurucu oyunu durdurdu.');
      else if (o.t === 'devam') bildir(o.o === yeni.ben ? 'Oyun devam ediyor.' : 'Kurucu oyunu devam ettirdi.', 'iyi');
    }
  }), []);

  const kur = (tur: OyunTur, botSayisi: number, elSayisi?: number) => {
    botPlan.current = botSayisi;
    masa.kur(tur, elSayisi === undefined ? undefined : { elSayisi });
  };
  const merkezeDon = () => {
    ayrik = true;
    try { localStorage.removeItem(SON_KEY); } catch { /* yok */ }
    masa.kapat();
  };

  return (
    <>
      {!oda && (
        <MasaMerkez
          baglanti={baglanti} ayrik={ayrik} kalici={kalici}
          kur={kur} katil={(k) => { ayrik = false; masa.katil(k); }}
          kurallarAc={(s) => setKurallar(s || 'yedili')} istatAc={() => setIstat(true)}
        />
      )}
      {oda?.asama === 'lobi' && <MasaLobi oda={oda} baglanti={baglanti} kurallarAc={(s) => setKurallar(s || oda.tur)} />}
      {oda && oda.asama !== 'lobi' && (
        <MasaOyun oda={oda} baglanti={baglanti} gecikme={gecikme} ucanlar={ucanlar} kurallarAc={() => setKurallar(oda.tur)} istatAc={() => setIstat(true)} merkezeDon={merkezeDon} />
      )}
      <Yaprak ac={!!kurallar} kapat={() => setKurallar(null)} baslik="Nasıl oynanır" tam tema={oda?.ayar.tema}>
        <Suspense fallback={<p className="mk-bos">Kurallar yükleniyor…</p>}>
          {kurallar && <MasaKurallar ilk={kurallar} renkler={oda?.ayar.renkler} />}
        </Suspense>
      </Yaprak>
      <Yaprak ac={istat} kapat={() => setIstat(false)} baslik="İstatistiklerim" tam>
        {istat && <MasaIstatistik />}
      </Yaprak>
      <Bildirimler />
    </>
  );
}

/* ------------------------------------------------------------------ oyun katmanı ------------------------------------------------------------------ */

function MasaOyun({ oda, baglanti, gecikme, ucanlar, kurallarAc, istatAc, merkezeDon }: {
  oda: OdaGorunum; baglanti: string; gecikme: number; ucanlar: Ucan[]; kurallarAc: () => void; istatAc: () => void; merkezeDon: () => void;
}) {
  const [masaAnahtar, setMasaAnahtar] = useState(0);
  /** Sonucu ekranda olan el (0 = kapalı); son hamle görülsün diye gecikmeyle açılır */
  const [elAcik, setElAcik] = useState(0);
  const [macAcik, setMacAcik] = useState(false);
  /** 'elSonu' aşamasında sonucu görülmüş el: maç bitince aynı el yeniden gösterilmez */
  const gorulen = useRef(0);
  const sonucVar = !!oda.elSonuc;

  useEffect(() => { lockScroll(); return unlockScroll; }, []);

  useEffect(() => {
    setElAcik(0); setMacAcik(false);
    if (oda.asama === 'elSonu' && sonucVar) {
      const t = setTimeout(() => { gorulen.current = oda.elNo; setElAcik(oda.elNo); }, 900);
      return () => clearTimeout(t);
    }
    if (oda.asama === 'bitti') {
      const elOnce = sonucVar && gorulen.current !== oda.elNo;
      const t = setTimeout(() => (elOnce ? setElAcik(oda.elNo) : setMacAcik(true)), elOnce ? 900 : 350);
      return () => clearTimeout(t);
    }
    if (oda.asama === 'oyun') gorulen.current = 0;
  }, [oda.kod, oda.asama, oda.elNo, sonucVar]);

  const kurucu = oda.kurucu === oda.ben;
  const Masa = oda.tur === 'uno' ? UnoMasa : OkeyMasa;
  const az = azHareket();

  return createPortal(
    <div className="mk mk-kabuk" data-tema={oda.ayar.tema} data-tur={oda.tur}>
      <MasaUstCubuk oda={oda} baglanti={baglanti} gecikme={gecikme} kurallarAc={kurallarAc} merkezeDon={merkezeDon} />
      <div className="mk-sahne">
        <div className="mk-masa-yuva">
          <HataSiniri key={masaAnahtar} yedek={
            <div className="mk-sahne-ileti">
              <h3>Masa çizilemedi</h3>
              <p>Oyun sunucuda sürüyor; masayı yenileyince kaldığı yerden görünür.</p>
              <button type="button" className="mk-dugme is-ana" onClick={() => setMasaAnahtar((k) => k + 1)}><RefreshCw size={18} /> Masayı yenile</button>
            </div>
          }>
            <Suspense fallback={<div className="mk-sahne-ileti"><span className="mk-donen" /><p>{OYUN_ADI[oda.tur]} masası hazırlanıyor…</p></div>}>
              <Masa oda={oda} />
            </Suspense>
          </HataSiniri>
        </div>

        <AnimatePresence>
          {baglanti !== 'hazir' && (
            <motion.div key="kopuk" className="mk-serit" role="status" initial={{ y: -40, opacity: 0 }} animate={{ y: 0, opacity: 1 }} exit={{ y: -40, opacity: 0 }} transition={{ duration: 0.22 }}>
              <WifiOff size={16} /> Yeniden bağlanılıyor…
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence>
          {oda.durdu && oda.asama === 'oyun' && (
            <motion.div key="durdu" className="mk-durdu" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.2 }}>
              <div className="mk-durdu-kutu">
                <span className="mk-durdu-ikon"><Pause size={28} /></span>
                <h3>Oyun durduruldu</h3>
                {kurucu
                  ? <button type="button" className="mk-dugme is-ana" onClick={() => masa.devam()}><Play size={18} /> Devam ettir</button>
                  : <p>Kurucunun devam ettirmesi bekleniyor.</p>}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence>
          {elAcik === oda.elNo && oda.elSonuc && (
            <ElSonu key={`el-${oda.elNo}`} oda={oda} sonuc={oda.elSonuc} macBitti={oda.asama === 'bitti'} macaGec={() => { gorulen.current = oda.elNo; setElAcik(0); setMacAcik(true); }} />
          )}
          {macAcik && oda.asama === 'bitti' && <MacSonu key="mac" oda={oda} istatAc={istatAc} />}
        </AnimatePresence>

        <div className="mk-ucanlar" aria-hidden="true">
          <AnimatePresence>
            {ucanlar.map((u) => (
              <motion.div key={u.id} className="mk-ucan" style={{ left: `${u.x}%` }}
                initial={{ opacity: 0, y: 30, scale: 0.5 }} animate={{ opacity: 1, y: az ? 0 : -90, scale: 1 }} exit={{ opacity: 0, y: az ? 0 : -150 }}
                transition={{ duration: az ? 0.2 : 0.9, ease: 'easeOut' }}>
                <span className="mk-ucan-e">{u.e}</span>
                <span className="mk-ucan-ad">{u.ad}</span>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>
    </div>,
    document.body,
  );
}
