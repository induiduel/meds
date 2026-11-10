/** Oyun içi üst çubuk (48 px): menü, oyun adı + kod, el, sıra, skor tablosu, tepki, 2B/3B, ses, bağlantı. */
import React, { useEffect, useRef, useState } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import { ArrowDownUp, BookOpen, Bot, Box, DoorOpen, Flag, Home, Menu, Pause, Play, Smile, Square, Trophy, UserPlus, Vibrate, Volume2, VolumeX } from 'lucide-react';
import { masa } from '../../services/masa/istemci';
import { OYUN_ADI, TEPKILER, type OdaGorunum, type OkeyGorunum } from '../../services/masa/tipler';
import { oyuncuAdi, sesCal, tercihYaz, titret, useTercih } from './ortak';
import { DavetYapragi } from './MasaLobi';
import { Avatar, Onay, SkorTablo, Yaprak, cezaBilgi, puanYaz, sadeAd, tasMi } from './kabukOrtak';

export default function MasaUstCubuk({ oda, baglanti, gecikme, kurallarAc, merkezeDon }: {
  oda: OdaGorunum; baglanti: string; gecikme: number; kurallarAc: () => void; merkezeDon: () => void;
}) {
  const tercih = useTercih();
  const [menu, setMenu] = useState(false);
  const [skor, setSkor] = useState(false);
  const [tepki, setTepki] = useState(false);
  const [onay, setOnay] = useState<'bitir' | 'kalk' | null>(null);
  const tepkiKap = useRef<HTMLDivElement>(null);
  const sonTepki = useRef(0);

  const kurucu = oda.kurucu === oda.ben;
  const okey = tasMi(oda.tur);
  const oyunda = oda.asama === 'oyun';
  const sira = oda.oyun?.sira;
  const bende = oyunda && sira === oda.ben;
  const puanim = oda.skor[oda.ben] || 0;
  const kopuklar = oda.oyuncular.filter((o) => !o.bot && !o.bagli && o.id !== oda.ben);
  const hazir = baglanti === 'hazir';
  const [agAc, setAgAc] = useState(false);
  const [davet, setDavet] = useState(false);
  const ag = !hazir ? { sinif: ' is-kopuk', ad: 'Bağlantı yok', ne: 'Sunucuya ulaşılamıyor; yeniden bağlanılıyor. Koltuğun masada duruyor.' }
    : gecikme > 1000 ? { sinif: ' is-kopuk', ad: `Çok yavaş bağlantı (${gecikme} ms)`, ne: 'Hamlelerin masaya geç ulaşır; taşın bir süre “gönderiliyor” görünebilir. Wi-Fi/mobil veriyi değiştirmeyi dene.' }
    : gecikme > 400 ? { sinif: ' is-yavas', ad: `Yavaş bağlantı (${gecikme} ms)`, ne: 'Hamleler biraz gecikmeli işlenebilir; oyun sürer.' }
    : { sinif: '', ad: `Bağlantı iyi (${gecikme} ms)`, ne: 'Hamlelerin anında masaya ulaşıyor.' };
  const yalniz = !oda.oyuncular.some((o) => !o.bot && o.id !== oda.ben);

  // Tepki kutusu: dışarı dokununca / Esc ile kapanır
  useEffect(() => {
    if (!tepki) return;
    const dis = (e: PointerEvent) => { if (!tepkiKap.current?.contains(e.target as Node)) setTepki(false); };
    const tus = (e: KeyboardEvent) => { if (e.key === 'Escape') setTepki(false); };
    window.addEventListener('pointerdown', dis, true);
    window.addEventListener('keydown', tus);
    return () => { window.removeEventListener('pointerdown', dis, true); window.removeEventListener('keydown', tus); };
  }, [tepki]);

  const tepkiYolla = (e: string) => {
    setTepki(false);
    if (Date.now() - sonTepki.current < 700) return;
    sonTepki.current = Date.now();
    masa.tepki(e); sesCal('tepki'); titret(8);
  };
  const sec = (fn: () => void) => () => { setMenu(false); fn(); };
  const elMetni = `El ${oda.elNo}${oda.ayar.elSayisi ? `/${oda.ayar.elSayisi}` : ''}`;
  const cezali = okey && oda.oyun ? (oda.oyun as OkeyGorunum).oyuncular.filter((o) => o.cezalar?.length) : [];

  return (
    <header className="mk-cubuk">
      <button type="button" className="mk-cubuk-dugme" onClick={() => setMenu(true)} aria-label="Oyun menüsü"><Menu size={22} /></button>
      <div className="mk-cubuk-ad">
        <b>{OYUN_ADI[oda.tur]}</b>
        <code aria-label={`Masa kodu ${oda.kod}`}>{oda.kod}</code>
      </div>
      <span className="mk-cubuk-el">{elMetni}</span>
      <span className={`mk-cubuk-sira${bende ? ' is-ben' : ''}`} aria-live="polite">
        {oda.asama === 'bitti' ? 'Maç bitti' : oda.asama === 'elSonu' ? 'El bitti' : oda.durdu ? 'Durduruldu' : bende ? 'Sıra sende' : <><small>Sıra</small> {sadeAd(oyuncuAdi(oda, sira))}</>}
      </span>
      <span className="mk-cubuk-bosluk" />

      <button type="button" className="mk-cubuk-dugme is-skor" onClick={() => setSkor(true)} aria-label={`Skor tablosu. Toplam puanın ${puanYaz(puanim)}`}>
        <Trophy size={18} /><b className={puanim < 0 ? 'is-eksi' : ''}>{puanYaz(puanim)}</b>
      </button>
      <div className="mk-tepki-kap" ref={tepkiKap}>
        <button type="button" className="mk-cubuk-dugme" onClick={() => setTepki((a) => !a)} aria-label="Tepki gönder" aria-expanded={tepki}><Smile size={20} /></button>
        <AnimatePresence>
          {tepki && (
            <motion.div className="mk-tepki-kutu" role="menu" aria-label="Tepkiler" initial={{ opacity: 0, y: -6, scale: 0.94 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: -6, scale: 0.94 }} transition={{ duration: 0.14 }}>
              {TEPKILER.map((e) => <button key={e} type="button" role="menuitem" onClick={() => tepkiYolla(e)} aria-label={`${e} tepkisi gönder`}>{e}</button>)}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      {okey && (
        <button type="button" className="mk-cubuk-dugme is-yazi" onClick={() => tercihYaz({ boyut: tercih.boyut === '3b' ? '2b' : '3b' })} aria-label={`Görünüm ${tercih.boyut === '3b' ? '3 boyutlu' : '2 boyutlu'}. Değiştir`}>
          {tercih.boyut === '3b' ? <Box size={18} /> : <Square size={18} />}<b>{tercih.boyut === '3b' ? '3B' : '2B'}</b>
        </button>
      )}
      <button type="button" className="mk-cubuk-dugme is-ses" onClick={() => tercihYaz({ ses: !tercih.ses })} aria-label={tercih.ses ? 'Sesi kapat' : 'Sesi aç'} aria-pressed={tercih.ses}>
        {tercih.ses ? <Volume2 size={20} /> : <VolumeX size={20} />}
      </button>
      <button type="button" className={`mk-baglanti-gosterge${ag.sinif}`} onClick={() => setAgAc((x) => !x)} aria-expanded={agAc} aria-label={`${ag.ad}. Açıklama için dokun`}>
        <i />{hazir ? <small>{gecikme} ms</small> : <small>yok</small>}
      </button>
      {agAc && <div className={`mk-ag-aciklama${ag.sinif}`} role="status" onClick={() => setAgAc(false)}><b>{ag.ad}</b><span>{ag.ne}</span></div>}

      {/* Menü */}
      <Yaprak ac={menu} kapat={() => setMenu(false)} baslik={<>{OYUN_ADI[oda.tur]} <code className="mk-kod-kucuk">{oda.kod}</code></>} tema={oda.ayar.tema}>
        <ul className="mk-menu">
          <li><button type="button" onClick={sec(kurallarAc)}><BookOpen size={20} /><span><b>Kurallar</b><small>Nasıl oynanır, cezalar, puanlama</small></span></button></li>
          <li className="mk-menu-ayrac">Görünüm tercihleri</li>
          <li>
            <label className="mk-anahtar-satir is-menu"><span><b><Volume2 size={18} /> Ses</b></span>
              <input type="checkbox" className="mk-anahtar" checked={tercih.ses} onChange={(e) => tercihYaz({ ses: e.target.checked })} /></label>
          </li>
          <li>
            <label className="mk-anahtar-satir is-menu"><span><b><Vibrate size={18} /> Titreşim</b></span>
              <input type="checkbox" className="mk-anahtar" checked={tercih.titresim} onChange={(e) => tercihYaz({ titresim: e.target.checked })} /></label>
          </li>
          {oda.tur !== 'uno' && oda.tur !== 'pisti' && oda.tur !== 'domino' && !['go', 'cizgi', 'xox'].includes(oda.tur) && (
            <li>
              <label className="mk-anahtar-satir is-menu"><span><b><ArrowDownUp size={18} /> Istakayı otomatik sırala</b><small>Çektiğin taş sırasına yerleşir</small></span>
                <input type="checkbox" className="mk-anahtar" checked={tercih.otoSira} onChange={(e) => tercihYaz({ otoSira: e.target.checked })} /></label>
            </li>
          )}
          {kurucu && oda.asama !== 'bitti' && (
            <>
              <li className="mk-menu-ayrac">Kurucu</li>
              {oyunda && (
                <li><button type="button" onClick={sec(() => (oda.durdu ? masa.devam() : masa.durdur()))}>
                  {oda.durdu ? <Play size={20} /> : <Pause size={20} />}
                  <span><b>{oda.durdu ? 'Devam ettir' : 'Oyunu durdur'}</b><small>{oda.durdu ? 'Herkes kaldığı yerden sürdürür' : 'Devam ettirene dek kimse hamle yapamaz'}</small></span>
                </button></li>
              )}
              <li><button type="button" onClick={sec(() => setOnay('bitir'))}><Flag size={20} /><span><b>Oyunu bitir</b><small>Maç şimdiki puanlarla sonuçlanır</small></span></button></li>
              {kopuklar.map((o) => (
                <li key={o.id}><button type="button" onClick={sec(() => masa.botDevral(o.id))}>
                  <Bot size={20} /><span><b>Yerine bot oynasın: {sadeAd(o.ad)}</b><small>Bağlantısı koptu; geri dönerse koltuğunu alır</small></span>
                </button></li>
              ))}
            </>
          )}
          <li className="mk-menu-ayrac">Masa</li>
          <li><button type="button" onClick={sec(() => setDavet(true))}><UserPlus size={20} /><span><b>Arkadaş davet et</b><small>Bildirim gider; oyun sürerken izleyici olarak gelir, bot koltuğunu isteyebilir</small></span></button></li>
          <li><button type="button" onClick={sec(merkezeDon)}><Home size={20} /><span><b>Merkeze dön (oyun sürsün)</b><small>Koltuğun kalır; “Yarım kalan oyunların”dan dönersin</small></span></button></li>
          <li><button type="button" className="is-tehlike" onClick={sec(() => (oda.asama === 'bitti' ? masa.cik() : setOnay('kalk')))}><DoorOpen size={20} /><span><b>Masadan kalk</b><small>{oda.asama === 'bitti' ? 'Maç bitti; merkeze dönersin' : yalniz ? 'Masada başka oyuncu yok: masa kapanır' : 'Yerine bot oynar; kodla geri dönebilirsin'}</small></span></button></li>
        </ul>
      </Yaprak>

      {/* Skor */}
      <Yaprak ac={skor} kapat={() => setSkor(false)} baslik="Skor tablosu" genis tema={oda.ayar.tema}>
        <div className="mk-skor-oyuncular">
          {[...oda.oyuncular].sort((a, b) => (oda.skor[b.id] || 0) - (oda.skor[a.id] || 0)).map((o, i) => (
            <div key={o.id} className={`mk-skor-kisi${o.id === oda.ben ? ' is-ben' : ''}`}>
              <i>{i + 1}</i><Avatar ad={o.ad} foto={o.foto} bot={o.bot} id={o.id} boy={32} />
              <span>{sadeAd(o.ad)}</span><b className={(oda.skor[o.id] || 0) < 0 ? 'is-eksi' : ''}>{puanYaz(oda.skor[o.id] || 0)}</b>
            </div>
          ))}
        </div>
        <SkorTablo oda={oda} />
        {okey && oyunda && (
          <section className="mk-skor-ceza">
            <h3>Bu elin cezaları</h3>
            {!cezali.length ? <p className="mk-bos">Bu elde henüz ceza yok.</p> : (
              <ul>
                {cezali.map((o) => (
                  <li key={o.id}>
                    <b>{sadeAd(oyuncuAdi(oda, o.id))}</b>
                    <span>{o.cezalar.map((c, i) => <i key={i} className={`mk-ceza-rozet ${cezaBilgi(c).sinif}`}>{cezaBilgi(c).ad} <em>{puanYaz(c.puan)}</em></i>)}</span>
                  </li>
                ))}
              </ul>
            )}
          </section>
        )}
      </Yaprak>

      <DavetYapragi ac={davet} kapat={() => setDavet(false)} kod={oda.kod} masadakiler={oda.oyuncular.map((o) => o.id)} />
      <Onay ac={onay === 'bitir'} kapat={() => setOnay(null)} baslik="Oyunu bitir" onayAd="Oyunu bitir" tehlike onay={() => masa.bitir()}
        metin={oyunda ? 'Maç şimdiki toplam puanlarla biter. Yarım el puanlanmaz.' : 'Maç şimdiki toplam puanlarla biter.'} />
      <Onay ac={onay === 'kalk'} kapat={() => setOnay(null)} baslik="Masadan kalk" onayAd="Masadan kalk" tehlike onay={() => masa.cik()}
        metin={yalniz ? 'Masada senden başka oyuncu yok; kalkarsan masa kapanır ve bu maç sona erer.' : 'Yerine bot oynar; kodla geri dönebilirsin.'} />
    </header>
  );
}
