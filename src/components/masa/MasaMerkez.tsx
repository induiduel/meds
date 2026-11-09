/** Oyun merkezi: oyun kartları + kurulum yaprağı, kodla katıl, yarım kalan oyunlar, istatistik özeti, görünen ad. */
import React, { useEffect, useState } from 'react';
import { ArrowRight, BarChart3, BookOpen, Bot, Check, LogIn, Pause, Pencil, RefreshCw, Users, WifiOff } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { masa, masaAdi } from '../../services/masa/istemci';
import { EL_SECENEK, OYUNCU_SINIR, OYUN_ADI, type OdaOzet, type OyunTur } from '../../services/masa/tipler';
import { OyunResmi, Yaprak, sadeAd } from './kabukOrtak';
import MasaIstatistik from './MasaIstatistik';
import type { KuralSekme } from './MasaKurallar';

const OYUNLAR: { tur: OyunTur; cumle: string; etiket?: string }[] = [
  { tur: 'yedili', cumle: 'Yedi taşla başla, per aç, masadaki perlere işle; elini ilk bitiren kazanır.', etiket: 'Ana oyun' },
  { tur: 'takim', cumle: 'Yedili’nin eşli hâli: karşındaki ortağınla aynı perlere işle, birlikte bitir.' },
  { tur: 'yuzbir', cumle: 'Okeyli klasik: 101 sayıyla ya da beş çiftle aç, taşlarını erit, son taşını at.' },
  { tur: 'uno', cumle: 'Rengi ya da sayıyı tuttur, kartlarını bitir; tek kart kalınca UNO demeyi unutma.' },
];
const BOT_SECENEK: Record<OyunTur, number[]> = { yedili: [1, 2, 3, 4, 5], takim: [1, 3, 5], yuzbir: [1, 2, 3], uno: [1, 2, 3, 4, 5, 6, 7] };
const BOT_VARSAYILAN: Record<OyunTur, number> = { yedili: 2, takim: 3, yuzbir: 3, uno: 3 };
export const elAdi = (n: number) => (n === 0 ? 'Bitirene dek' : `${n} el`);

export default function MasaMerkez({ baglanti, ayrik, kalici, kur, katil, kurallarAc, istatAc }: {
  baglanti: string; ayrik: boolean; kalici: { mesaj: string; kod: string } | null;
  kur: (tur: OyunTur, botSayisi: number, elSayisi?: number) => void; katil: (kod: string) => void;
  kurallarAc: (s?: KuralSekme) => void; istatAc: () => void;
}) {
  const [secili, setSecili] = useState<OyunTur | null>(null);
  const [sonTur, setSonTur] = useState<OyunTur>('yedili');
  const [kip, setKip] = useState<'arkadas' | 'bot'>('arkadas');
  const [botN, setBotN] = useState(2);
  const [elN, setElN] = useState(3);
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

  const ac = (tur: OyunTur) => { setSecili(tur); setSonTur(tur); setKip('arkadas'); setBotN(BOT_VARSAYILAN[tur]); setElN(3); };
  const baslat = () => {
    if (!secili) return;
    setBekle(true);
    kur(secili, kip === 'bot' ? botN : 0, kip === 'bot' ? elN : undefined);
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
  const [enAz, enCok] = OYUNCU_SINIR[tur];

  return (
    <div className="mk mk-merkez">
      <header className="mk-merkez-bas">
        <div className="mk-merkez-baslik">
          <span className="mk-ust-etiket">Oyunlar</span>
          <h1>Taş Masası</h1>
          <p>Arkadaşlarınla aynı masaya otur ya da botlara karşı oyna. Okey taşlı üç oyun ve Uno; oyun yarım kalırsa kaldığın yerden sürer.</p>
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

      <section className="mk-oyunlar" aria-label="Oyunlar">
        {OYUNLAR.map((o) => (
          <button key={o.tur} type="button" className={`mk-oyun-kart${o.tur === 'yedili' ? ' is-ana' : ''}`} onClick={() => ac(o.tur)} disabled={bekle}>
            <span className="mk-oyun-kece"><OyunResmi tur={o.tur} /></span>
            <span className="mk-oyun-metin">
              {o.etiket && <em>{o.etiket}</em>}
              <b>{OYUN_ADI[o.tur]}</b>
              <span>{o.cumle}</span>
              <small><Users size={14} /> {OYUNCU_SINIR[o.tur][0]}–{OYUNCU_SINIR[o.tur][1]} oyuncu</small>
            </span>
            <ArrowRight className="mk-oyun-ok" size={20} />
          </button>
        ))}
      </section>

      <div className="mk-merkez-ikili">
        <section className="mk-pano">
          <h2><LogIn size={18} /> Kodla katıl</h2>
          <p className="mk-pano-not">Arkadaşının paylaştığı 5 karakterli masa kodunu yaz.</p>
          <form className="mk-kod-form" onSubmit={kodGonder}>
            <input
              className="mk-giris mk-kod-giris" value={kod} inputMode="text" autoCapitalize="characters" autoComplete="off" spellCheck={false}
              placeholder="KOD" aria-label="Masa kodu" maxLength={5}
              onChange={(e) => setKod(e.target.value.toLocaleUpperCase('en-US').replace(/[^A-Z0-9]/g, '').slice(0, 5))}
            />
            <button type="submit" className="mk-dugme is-ana" disabled={kod.length !== 5 || bekle}>Katıl</button>
          </form>
        </section>

        <section className="mk-pano">
          <h2><BookOpen size={18} /> Nasıl oynanır</h2>
          <p className="mk-pano-not">Dört oyunun kuralları, cezalar ve puanlama; örnek taş ve kartlarla.</p>
          <div className="mk-kural-kisayol">
            {OYUNLAR.map((o) => <button key={o.tur} type="button" className="mk-cip" onClick={() => kurallarAc(o.tur)}>{OYUN_ADI[o.tur]}</button>)}
            <button type="button" className="mk-cip" onClick={() => kurallarAc('ceza')}>Cezalar ve puan</button>
          </div>
        </section>
      </div>

      <section className="mk-pano">
        <h2><Pause size={18} /> Yarım kalan oyunların</h2>
        {odalar === null ? <p className="mk-bos">Yükleniyor…</p> : !odalar.length ? (
          <p className="mk-bos">Yarım kalan oyunun yok. Masadan çıksan da oyun saklanır; buradan geri dönersin.</p>
        ) : (
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
        )}
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
              <div className="mk-alan">
                <span className="mk-alan-ad">Bot sayısı</span>
                <div className="mk-dilim" role="radiogroup" aria-label="Bot sayısı">
                  {BOT_SECENEK[tur].map((n) => <button key={n} type="button" role="radio" aria-checked={botN === n} className={botN === n ? 'is-on' : ''} onClick={() => setBotN(n)}>{n}</button>)}
                </div>
                {tur === 'takim' && <small className="mk-alan-not">Takımlar eşit olsun diye bot sayısı tektir: {botN === 1 ? 'bire bir' : `${(botN + 1) / 2} kişilik takımlar`}; ortağın da bot olur.</small>}
              </div>
              <div className="mk-alan">
                <span className="mk-alan-ad">Kaç el</span>
                <div className="mk-dilim" role="radiogroup" aria-label="El sayısı">
                  {EL_SECENEK.map((n) => <button key={n} type="button" role="radio" aria-checked={elN === n} className={elN === n ? 'is-on' : ''} onClick={() => setElN(n)}>{n === 0 ? 'Bitirene dek' : n}</button>)}
                </div>
              </div>
            </>
          ) : (
            <p className="mk-alan-not">{enAz}–{enCok} oyuncu. El sayısını, temayı{tur === 'uno' ? '' : ', taş renklerini'} ve yardımcı asistanı lobide ayarlarsın.</p>
          )}
          <button type="button" className="mk-baglanti" onClick={() => { setSecili(null); kurallarAc(tur); }}><BookOpen size={16} /> {OYUN_ADI[tur]} kuralları</button>
        </div>
      </Yaprak>
    </div>
  );
}
