/** Oyun merkezi: oyun kartları + kurulum yaprağı, kodla katıl, yarım kalan oyunlar, istatistik özeti, görünen ad. */
import React, { useEffect, useState } from 'react';
import { ArrowRight, BarChart3, BookOpen, Bot, Check, LogIn, Pause, Pencil, RefreshCw, Users, WifiOff } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { masa, masaAdi } from '../../services/masa/istemci';
import { EL_SECENEK, OYUNCU_SINIR, OYUN_ADI, unoModTanim, unoOyuncuUygun, type OdaAyar, type OdaOzet, type OyunTur, type UnoMod } from '../../services/masa/tipler';
import { OyunResmi, Yaprak, sadeAd } from './kabukOrtak';
import '../../styles/masa/lobi.css';
import MasaIstatistik from './MasaIstatistik';
import { TahtaAyar, tahtaMi } from './tahta/ortak';
import { OyunModu, UnoModu } from './ModSecici';
import { KATEGORILER, OYUN_CUMLE, oyuncuYazi } from './oyunKatalog';
import type { KuralSekme } from './MasaKurallar';

const BOT_SECENEK: Record<OyunTur, number[]> = { yedili: [1, 2, 3, 4, 5], takim: [1, 3, 5], yuzbir: [1, 2, 3], uno: [1, 2, 3, 4, 5, 6, 7], go: [1], cizgi: [1], xox: [1], remi: [1, 2, 3], kastet: [1, 2, 3], duz: [1, 2, 3], pisti: [1, 3], domino: [1, 2, 3] };
const BOT_VARSAYILAN: Record<OyunTur, number> = { yedili: 2, takim: 3, yuzbir: 3, uno: 3, go: 1, cizgi: 1, xox: 1, remi: 1, kastet: 3, duz: 3, pisti: 1, domino: 1 };
export const elAdi = (n: number) => (n === 0 ? 'Bitirene dek' : `${n} el`);

export default function MasaMerkez({ baglanti, ayrik, kalici, kur, katil, kurallarAc, istatAc }: {
  baglanti: string; ayrik: boolean; kalici: { mesaj: string; kod: string } | null;
  kur: (tur: OyunTur, botSayisi: number, ayar?: Partial<OdaAyar>) => void; katil: (kod: string) => void;
  kurallarAc: (s?: KuralSekme) => void; istatAc: () => void;
}) {
  const [secili, setSecili] = useState<OyunTur | null>(null);
  const [sonTur, setSonTur] = useState<OyunTur>('yedili');
  const [kip, setKip] = useState<'arkadas' | 'bot'>('arkadas');
  const [botN, setBotN] = useState(2);
  const [elN, setElN] = useState(3);
  const [tahtaAyar, setTahtaAyar] = useState<Partial<OdaAyar>>({});
  const [asistan, setAsistan] = useState(true);
  const [unoMod, setUnoMod] = useState<UnoMod>('klasik');
  const [tasN, setTasN] = useState<7 | 14>(7);
  const [kod, setKod] = useState('');
  const [bekle, setBekle] = useState(false);
  const [odalar, setOdalar] = useState<OdaOzet[] | null>(null);
  const [ad, setAd] = useState(masaAdi);
  const [adDuzen, setAdDuzen] = useState(false);
  const [adTaslak, setAdTaslak] = useState('');

  useEffect(() => {
    let canli = true;
    void safeJsonFetch<{ ogeler: OdaOzet[] }>('/api/masa/odalarim').then((r) => { if (canli) setOdalar(r.ok && Array.isArray(r.data?.ogeler) ? r.data!.ogeler : []); });
    return () => { canli = false; };
  }, []);
  // Kur/katıl yanıtı gelmezse (hata bildirimi çıkar) düğmeler yeniden açılır
  useEffect(() => { if (!bekle) return; const t = setTimeout(() => setBekle(false), 5000); return () => clearTimeout(t); }, [bekle]);
  useEffect(() => { if (kalici) setBekle(false); }, [kalici]);

  const ac = (tur: OyunTur) => { setSecili(tur); setSonTur(tur); setKip(tahtaMi(tur) ? 'bot' : 'arkadas'); setBotN(BOT_VARSAYILAN[tur]); setElN(3); setAsistan(true); setUnoMod('klasik'); setTasN(7); };
  // Uno: bot sayısı seçenekleri moda göre süzülür (Takım: toplam 4/6/8; Express: en çok 6); geçersiz kalan seçim en yakın geçerliye çekilir
  const botSecenekBul = (t: OyunTur, m: UnoMod) => (t === 'uno' ? BOT_SECENEK.uno.filter((b) => !unoOyuncuUygun(m, b + 1)) : BOT_SECENEK[t]);
  useEffect(() => {
    if (secili !== 'uno') return;
    const s = botSecenekBul('uno', unoMod);
    if (s.length && !s.includes(botN)) setBotN(s.reduce((en, b) => (Math.abs(b - botN) < Math.abs(en - botN) ? b : en)));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [unoMod, secili]);
  const baslat = () => {
    if (!secili) return;
    setBekle(true);
    const t = tahtaMi(secili) ? tahtaAyar : {};
    // Bota karşı oyunda lobi atlanır: mod, zorluk ve taş sayısı burada seçilir
    kur(secili, kip === 'bot' ? botN : 0, kip === 'bot' ? { ...t, elSayisi: elN, asistan, unoMod, tasSayisi: tasN } : tahtaMi(secili) ? t : undefined);
    setSecili(null);
  };
  const kodGonder = (e: React.FormEvent) => {
    e.preventDefault();
    if (kod.length !== 5) return;
    setBekle(true);
    katil(kod);
  };
  const adKaydet = (e: React.FormEvent) => {
    e.preventDefault();
    const yeni = adTaslak.replace(/[<>]/g, '').trim().slice(0, 24);
    if (yeni) {
      masa.adYaz(yeni);
      setAd(yeni);
      // Ad sunucuya bağlanırken gider: boştayken bağlantı tazelenir
      if (baglanti === 'hazir' && !ayrik) { masa.kapat(); masa.baglan(); }
    }
    setAdDuzen(false);
  };
  const tur = secili || sonTur;
  const botSecenek = botSecenekBul(tur, unoMod);

  return (
    <div className="mk mk-merkez">
      <header className="mk-merkez-bas">
        <div className="mk-merkez-baslik">
          <span className="mk-ust-etiket">Oyunlar</span>
          <h1>Taş Masası</h1>
          <p>Arkadaşlarınla aynı masaya otur ya da botlara karşı oyna. Okey, kart ve tahta oyunları tek masada; oyun yarım kalırsa kaldığın yerden sürer.</p>
        </div>
        <div className="mk-ad">
          {adDuzen ? (
            <form onSubmit={adKaydet} className="mk-ad-form">
              <label htmlFor="mk-ad-giris">Masadaki adın</label>
              <div>
                <input id="mk-ad-giris" className="mk-giris" value={adTaslak} maxLength={24} autoFocus onChange={(e) => setAdTaslak(e.target.value)} autoComplete="off" />
                <button type="submit" className="mk-ikon-dugme is-dolu" aria-label="Adı kaydet"><Check size={20} /></button>
              </div>
            </form>
          ) : (
            <button type="button" className="mk-ad-dugme" onClick={() => { setAdTaslak(ad); setAdDuzen(true); }} aria-label={`Masadaki adın ${ad}. Değiştir`}>
              <span><small>Masadaki adın</small><b>{ad}</b></span>
              <Pencil size={16} />
            </button>
          )}
        </div>
      </header>

      {kalici && (
        <div className="mk-uyari is-hata" role="alert">
          <p>{kalici.kod === 'kimlik' ? 'Oturumun doğrulanamadı. Oturumu yenileyince masalara yeniden bağlanırsın.' : kalici.mesaj}</p>
          {kalici.kod === 'kimlik' && <button type="button" className="mk-dugme is-ana" onClick={() => window.location.reload()}><RefreshCw size={18} /> Oturumu yenile</button>}
        </div>
      )}
      {!kalici && baglanti === 'koptu' && <div className="mk-uyari" role="status"><p><WifiOff size={16} /> Oyun sunucusuna bağlanılıyor…</p></div>}

      <form className="mk-hizli" onSubmit={kodGonder}>
        <span className="mk-hizli-metin">
          <LogIn size={20} />
          <span><b>Kodla katıl</b><small>Arkadaşının paylaştığı 5 karakterli masa kodunu yaz.</small></span>
        </span>
        <span className="mk-kod-form">
          <input
            className="mk-giris mk-kod-giris" value={kod} inputMode="text" autoCapitalize="characters" autoComplete="off" spellCheck={false}
            placeholder="KOD" aria-label="Masa kodu" maxLength={5}
            onChange={(e) => setKod(e.target.value.toLocaleUpperCase('en-US').replace(/[^A-Z0-9]/g, '').slice(0, 5))}
          />
          <button type="submit" className="mk-dugme is-ana" disabled={kod.length !== 5 || bekle}>Katıl</button>
        </span>
      </form>

      {!!odalar?.length && (
        <section className="mk-pano">
          <h2><Pause size={18} /> Yarım kalan oyunların <small>{odalar.length}</small></h2>
          <ul className="mk-yarim">
            {odalar.map((o) => (
              <li key={o.kod}>
                <span className="mk-yarim-resim"><OyunResmi tur={o.tur} /></span>
                <span className="mk-yarim-metin">
                  <b>{OYUN_ADI[o.tur]} <code>{o.kod}</code></b>
                  <span>{o.oyuncular.length ? o.oyuncular.map(sadeAd).join(', ') : 'Henüz kimse katılmadı'}</span>
                  <small>
                    {o.asama === 'lobi' ? 'Lobide bekliyor' : `${o.elNo}. el`}
                    {o.durdu && <i className="mk-rozet is-durdu">Durduruldu</i>}
                    {o.kurucuBen && <i className="mk-rozet">Kurucu sensin</i>}
                  </small>
                </span>
                <button type="button" className="mk-dugme is-ana" disabled={bekle} onClick={() => { setBekle(true); katil(o.kod); }}>Devam et</button>
              </li>
            ))}
          </ul>
        </section>
      )}

      {KATEGORILER.map((k) => (
        <section key={k.id} className="mk-kat" aria-labelledby={`mk-kat-${k.id}`}>
          <header className="mk-kat-bas">
            <h2 id={`mk-kat-${k.id}`}>{k.ad}</h2>
            <p>{k.alt}</p>
            <span>{k.turler.length} oyun</span>
          </header>
          <div className="mk-oyunlar" data-n={k.turler.length}>
            {k.turler.map((t) => (
              <button key={t} type="button" className={`mk-oyun-kart${t === 'yedili' ? ' is-ana' : ''}`} onClick={() => ac(t)} disabled={bekle}>
                <span className="mk-oyun-kece"><OyunResmi tur={t} /></span>
                <span className="mk-oyun-metin">
                  {t === 'yedili' && <em>Ana oyun</em>}
                  <b>{OYUN_ADI[t]}</b>
                  <span>{OYUN_CUMLE[t]}</span>
                  <small><Users size={14} /> {oyuncuYazi(OYUNCU_SINIR[t])}</small>
                </span>
                <ArrowRight className="mk-oyun-ok" size={20} />
              </button>
            ))}
          </div>
        </section>
      ))}

      <section className="mk-pano">
        <h2><BookOpen size={18} /> Nasıl oynanır</h2>
        <p className="mk-pano-not">Her oyunun taşları ve kartları, bir turun akışı, cezalar ve puanlama; şemalı ve örnekli.</p>
        <div className="mk-kural-gruplar">
          {KATEGORILER.map((k) => (
            <div key={k.id} className="mk-kural-grup">
              <span>{k.ad}</span>
              {k.turler.map((t) => <button key={t} type="button" className="mk-cip" onClick={() => kurallarAc(t)}>{OYUN_ADI[t]}</button>)}
            </div>
          ))}
          <div className="mk-kural-grup">
            <span>Genel</span>
            <button type="button" className="mk-cip" onClick={() => kurallarAc('ceza')}>Cezalar ve puan</button>
            <button type="button" className="mk-cip" onClick={() => kurallarAc('ipucu')}>Masa ve ipuçları</button>
          </div>
        </div>
      </section>

      <section className="mk-pano">
        <div className="mk-pano-bas">
          <h2><BarChart3 size={18} /> İstatistiklerim</h2>
          <button type="button" className="mk-cip" onClick={istatAc}>Tam ekran</button>
        </div>
        <MasaIstatistik />
      </section>

      <Yaprak ac={!!secili} kapat={() => setSecili(null)} baslik={OYUN_ADI[tur]} alt={
        <button type="button" className="mk-dugme is-ana is-buyuk" onClick={baslat}>{kip === 'bot' ? 'Oyunu başlat' : 'Masayı kur'}</button>
      }>
        <div className="mk-kurulum">
          <div className="mk-kurulum-resim"><OyunResmi tur={tur} /></div>
          <div className="mk-kurulum-tanit">
            <p>{OYUN_CUMLE[tur]}</p>
            <small><Users size={14} /> {oyuncuYazi(OYUNCU_SINIR[tur])}</small>
          </div>
          <div className="mk-secim" role="radiogroup" aria-label="Oyun biçimi">
            <button type="button" role="radio" aria-checked={kip === 'arkadas'} className={kip === 'arkadas' ? 'is-on' : ''} onClick={() => setKip('arkadas')}>
              <Users size={22} /><b>Arkadaşlarla oyna</b><span>Masa kurulur, kodu paylaşırsın. Eksik koltuğa bot ekleyebilirsin.</span>
            </button>
            <button type="button" role="radio" aria-checked={kip === 'bot'} className={kip === 'bot' ? 'is-on' : ''} onClick={() => setKip('bot')}>
              <Bot size={22} /><b>Bota karşı oyna</b><span>Botlar oturur, oyun hemen başlar.</span>
            </button>
          </div>
          {kip === 'bot' ? (
            <>
              {botSecenek.length > 1 && <div className="mk-alan">
                <span className="mk-alan-ad">Bot sayısı</span>
                <div className="mk-dilim" role="radiogroup" aria-label="Bot sayısı">
                  {botSecenek.map((n) => <button key={n} type="button" role="radio" aria-checked={botN === n} className={botN === n ? 'is-on' : ''} onClick={() => setBotN(n)}>{n}</button>)}
                </div>
                {tur === 'uno' && botSecenek.length < BOT_SECENEK.uno.length && <small className="mk-alan-not">{unoModTanim(unoMod).cift ? `${unoModTanim(unoMod).ad} modu ikişerli takımlarla oynanır: sen ve ${botN} bot, ${(botN + 1) / 2} takım; karşındaki bot ortağın olur.` : `${unoModTanim(unoMod).ad} modu en çok ${unoModTanim(unoMod).enCok} oyuncuyla oynanır.`}</small>}
                {tur === 'takim' && <small className="mk-alan-not">Takımlar eşit olsun diye bot sayısı tektir: {botN === 1 ? 'bire bir' : `${(botN + 1) / 2} kişilik takımlar`}; ortağın da bot olur.</small>}
              </div>}
              <div className="mk-alan">
                <span className="mk-alan-ad">Kaç el</span>
                <div className="mk-dilim" role="radiogroup" aria-label="El sayısı">
                  {EL_SECENEK.map((n) => <button key={n} type="button" role="radio" aria-checked={elN === n} className={elN === n ? 'is-on' : ''} onClick={() => setElN(n)}>{n === 0 ? 'Bitirene dek' : n}</button>)}
                </div>
              </div>
              {tur === 'uno' && <UnoModu mod={unoMod} sec={setUnoMod} kurallarAc={(m) => { setSecili(null); kurallarAc(`uno:${m}`); }} />}
              {tur === 'takim' && botN <= 3 && <div className="mk-alan">
                <span className="mk-alan-ad">Kişi başı taş</span>
                <div className="mk-dilim" role="radiogroup" aria-label="Kişi başı taş">
                  {([7, 14] as const).map((n) => <button key={n} type="button" role="radio" aria-checked={tasN === n} className={tasN === n ? 'is-on' : ''} onClick={() => setTasN(n)}>{n} taş</button>)}
                </div>
              </div>}
              {(!tahtaMi(tur) || tur === 'go') && <OyunModu tur={tur} asistan={asistan} sec={setAsistan} />}
            </>
          ) : (
            <p className="mk-alan-not">{tahtaMi(tur) ? 'Arkadaşın kodla katılır; ayarları lobide de değiştirebilirsin.' : <>El sayısını, {tur === 'uno' ? 'Uno modunu, ' : ''}zorluğu ve temayı lobide ayarlarsın.</>}</p>
          )}
          {tahtaMi(tur) && <TahtaAyar tur={tur} ayar={tahtaAyar} degistir={(a) => setTahtaAyar((x) => ({ ...x, ...a }))} />}
          <button type="button" className="mk-baglanti" onClick={() => { setSecili(null); kurallarAc(tur === 'uno' && kip === 'bot' ? `uno:${unoMod}` : tur); }}><BookOpen size={16} /> {OYUN_ADI[tur]} kuralları</button>
        </div>
      </Yaprak>
    </div>
  );
}
