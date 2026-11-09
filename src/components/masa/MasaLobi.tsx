/** Lobi: masa kodu + paylaşım, oyuncular, takımlar, ayarlar (yalnız kurucu değiştirir), arkadaş daveti, başlat. */
import React, { useEffect, useRef, useState } from 'react';
import { AlertTriangle, ArrowLeftRight, BookOpen, Bot, Check, Copy, Crown, LogOut, Play, Share2, Sparkles, UserPlus, WifiOff, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { masa } from '../../services/masa/istemci';
import { EL_SECENEK, OKEY_TEMALAR, OYUNCU_SINIR, OYUN_ADI, UNO_TEMALAR, VARSAYILAN_RENKLER, type OdaGorunum, type OyuncuBilgi, type Takim } from '../../services/masa/tipler';
import { Avatar, KartOrnek, Onay, TEMA_BILGI, TasOrnek, Yaprak, bildir, sadeAd } from './kabukOrtak';
import type { KuralSekme } from './MasaKurallar';

const PALETLER: { ad: string; renkler: string[] }[] = [
  { ad: 'Klasik', renkler: [...VARSAYILAN_RENKLER] },
  { ad: 'Orman', renkler: ['#b3261e', '#14532d', '#1e3a8a', '#ca8a04'] },
  { ad: 'Şeker', renkler: ['#e91e63', '#6a1b9a', '#0288d1', '#f57c00'] },
  { ad: 'Gece', renkler: ['#9b1c31', '#111827', '#0f766e', '#a16207'] },
  { ad: 'Mercan', renkler: ['#e4572e', '#2b2d42', '#00838f', '#8e44ad'] },
];
const RENK_AD = ['1. renk', '2. renk', '3. renk', '4. renk'];
const FILDISI = '#f4ecd8';

const isik = (hex: string) => {
  const k = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255).map((v) => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
  return 0.2126 * k[0] + 0.7152 * k[1] + 0.0722 * k[2];
};
/** Fildişi taş üstünde kontrast oranı (≥ 3 okunur) */
const kontrast = (hex: string) => { const a = isik(FILDISI) + 0.05, b = isik(hex) + 0.05; return a > b ? a / b : b / a; };
const fark = (a: string, b: string) => Math.hypot(...[1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16) - parseInt(b.slice(i, i + 2), 16)));

const OZET: Record<string, string[]> = {
  yedili: ['7 taşla başlarsın. En az 3 taşlık per (seri ya da grup) açarsın.', 'Per açtıktan sonra masadaki her pere taş işleyebilirsin; eş taşla uzun seriyi ikiye de bölebilirsin.', 'Açabilecekken ya da işleyebilecekken taş çekmek ve eli devretmek cezadır (−5).', 'Elini bitiren kazanır; diğerleri kalan taşı kadar eksi alır.'],
  takim: ['Ortağın karşında oturur. Takımdan biri per açınca ikiniz de işleyebilirsiniz.', 'Biriniz elini bitirince takım kazanır.', 'Bir grup 4 taşa tamamlanınca rakip takımın her oyuncusu 1 hediye taş çeker.', 'Açabilecekken ya da işleyebilecekken çekmek ve devretmek cezadır (−5).'],
  yuzbir: ['21 taş dağıtılır; gösterge taşının bir üstü okeydir (joker).', 'Perlerinin toplamı 101 olunca ya da 5 çiftle açarsın.', 'Her tur taş çeker (desteden ya da yandan), sonunda bir taş atarsın.', 'Son taşını atan bitirir: +101. Açamayan −202 alır.'],
  uno: ['7 kartla başlarsın. Rengi, sayıyı ya da simgeyi tutturan kartı atarsın.', 'Oynayamıyorsan 1 kart çekersin.', 'Tek kartın kalınca UNO de; demezsen yakalanırsan 2 kart çekersin.', 'Kartlarını bitiren, rakiplerin elindeki kartların puanını alır.'],
};

interface Arkadas { kimlik: string; ad: string; foto?: string }

export default function MasaLobi({ oda, baglanti, kurallarAc }: { oda: OdaGorunum; baglanti: string; kurallarAc: (s?: KuralSekme) => void }) {
  const kurucu = oda.kurucu === oda.ben;
  const [enAz, enCok] = OYUNCU_SINIR[oda.tur];
  const okey = oda.tur !== 'uno';
  const [kopyalandi, setKopyalandi] = useState(false);
  const [davet, setDavet] = useState(false);
  const [cikis, setCikis] = useState(false);
  const [taslak, setTaslak] = useState<string[]>(oda.ayar.renkler);
  const gonderZaman = useRef<any>(null);
  const baglantiAdres = `${window.location.origin}/sorular/oyunlar?masa=${oda.kod}`;

  // Sunucudaki renkler değişince (başka cihaz / palet) taslak ona uzlaşır
  const sunucuRenk = oda.ayar.renkler.join();
  useEffect(() => { setTaslak(oda.ayar.renkler); }, [sunucuRenk]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => () => clearTimeout(gonderZaman.current), []);

  const ayniVar = new Set(taslak.map((r) => r.toLowerCase())).size < 4;
  const yakin = !ayniVar && taslak.some((a, i) => taslak.some((b, j) => j > i && fark(a, b) < 70));
  const soluk = taslak.map((r) => kontrast(r) < 2.6);
  const renkYaz = (yeni: string[], hemen = false) => {
    setTaslak(yeni);
    clearTimeout(gonderZaman.current);
    if (new Set(yeni.map((r) => r.toLowerCase())).size < 4) return; // sunucu özdeş renkleri kabul etmez
    gonderZaman.current = setTimeout(() => masa.ayar({ renkler: yeni }), hemen ? 0 : 220);
  };

  const kopyala = async (metin: string) => {
    try { await navigator.clipboard.writeText(metin); }
    catch {
      const a = document.createElement('textarea');
      a.value = metin; a.style.position = 'fixed'; a.style.opacity = '0';
      document.body.appendChild(a); a.select();
      try { document.execCommand('copy'); } catch { /* yok */ }
      a.remove();
    }
    setKopyalandi(true);
    setTimeout(() => setKopyalandi(false), 1600);
  };
  const paylas = async () => {
    const veri = { title: `${OYUN_ADI[oda.tur]} masası`, text: `${OYUN_ADI[oda.tur]} masama gel! Kod: ${oda.kod}`, url: baglantiAdres };
    if (navigator.share) { try { await navigator.share(veri); } catch { /* vazgeçildi */ } }
    else { await kopyala(baglantiAdres); bildir('Bağlantı kopyalandı.', 'iyi'); }
  };

  const A = oda.oyuncular.filter((o) => o.takim === 'A'), B = oda.oyuncular.filter((o) => o.takim !== 'A');
  const neden = oda.oyuncular.length < enAz ? `En az ${enAz} oyuncu gerekir: arkadaşını çağır ya da bot ekle.`
    : oda.oyuncular.length > enCok ? `En çok ${enCok} oyuncu oynayabilir.`
    : oda.tur === 'takim' && (!A.length || A.length !== B.length) ? `Takımlar eşit olmalı (şu an A ${A.length} – B ${B.length}).` : '';
  const dolu = oda.oyuncular.length >= enCok;

  const oyuncuSatir = (o: OyuncuBilgi) => (
    <li key={o.id} className={`mk-oyuncu${o.id === oda.ben ? ' is-ben' : ''}`}>
      <Avatar ad={o.ad} foto={o.foto} bot={o.bot} id={o.id} boy={40} tac={o.id === oda.kurucu} />
      <span className="mk-oyuncu-ad">
        <b>{sadeAd(o.ad)}{o.id === oda.ben && <em>sen</em>}</b>
        <small>
          {o.id === oda.kurucu && <i className="mk-rozet is-altin"><Crown size={12} /> Kurucu</i>}
          {o.bot ? <i className="mk-rozet"><Bot size={12} /> Bot</i> : o.bagli ? <i className="mk-durum is-bagli">Bağlı</i> : <i className="mk-durum is-kopuk">Bağlantı koptu</i>}
        </small>
      </span>
      {oda.tur === 'takim' && (kurucu || o.id === oda.ben) && (
        <button type="button" className="mk-ikon-dugme" onClick={() => masa.takim(o.takim === 'A' ? 'B' : 'A', o.id === oda.ben ? undefined : o.id)} aria-label={`${sadeAd(o.ad)}: ${o.takim === 'A' ? 'B' : 'A'} takımına geçir`}>
          <ArrowLeftRight size={18} />
        </button>
      )}
      {kurucu && o.id !== oda.ben && (
        <button type="button" className="mk-ikon-dugme" onClick={() => masa.cikar(o.id)} aria-label={`${sadeAd(o.ad)} masadan çıkar`}><X size={18} /></button>
      )}
    </li>
  );
  const boslar = (n: number) => Array.from({ length: Math.max(0, n) }, (_, i) => <li key={`bos-${i}`} className="mk-oyuncu is-bos"><span className="mk-avatar is-bos" /><span className="mk-oyuncu-ad"><b>Boş koltuk</b></span></li>);
  const temalar: readonly string[] = okey ? OKEY_TEMALAR : UNO_TEMALAR;

  return (
    <div className="mk mk-lobi" data-tema={oda.ayar.tema}>
      <header className="mk-lobi-bas">
        <div>
          <span className="mk-ust-etiket">{OYUN_ADI[oda.tur]} · Lobi</span>
          <h1>Masa kodu</h1>
        </div>
        <button type="button" className="mk-dugme is-soluk" onClick={() => setCikis(true)}><LogOut size={18} /> Masadan ayrıl</button>
      </header>

      {baglanti !== 'hazir' && <div className="mk-uyari" role="status"><p><WifiOff size={16} /> Yeniden bağlanılıyor…</p></div>}

      <section className="mk-kod-pano">
        <div className="mk-kod" aria-label={`Masa kodu ${oda.kod.split('').join(' ')}`}>{oda.kod.split('').map((h, i) => <span key={i}>{h}</span>)}</div>
        <div className="mk-kod-dugmeler">
          <button type="button" className="mk-dugme is-ana" onClick={() => void kopyala(oda.kod)}>{kopyalandi ? <Check size={18} /> : <Copy size={18} />} {kopyalandi ? 'Kopyalandı' : 'Kodu kopyala'}</button>
          <button type="button" className="mk-dugme is-acik" onClick={() => void paylas()}><Share2 size={18} /> Bağlantıyı paylaş</button>
        </div>
        <p>Arkadaşların Oyunlar sayfasında “Kodla katıl”a bu kodu yazar ya da bağlantıya dokunur.</p>
      </section>

      <div className="mk-lobi-izgara">
        <section className="mk-pano">
          <div className="mk-pano-bas">
            <h2>Oyuncular <small>{oda.oyuncular.length}/{enCok}</small></h2>
            {kurucu && (
              <div className="mk-pano-dugmeler">
                <button type="button" className="mk-cip" onClick={() => masa.botEkle()} disabled={dolu}><Bot size={16} /> Bot ekle</button>
                <button type="button" className="mk-cip" onClick={() => setDavet(true)} disabled={dolu}><UserPlus size={16} /> Arkadaş davet et</button>
              </div>
            )}
          </div>
          {oda.tur === 'takim' ? (
            <div className="mk-takimlar">
              {(['A', 'B'] as Takim[]).map((t) => {
                const l = t === 'A' ? A : B;
                return (
                  <div key={t} className={`mk-takim is-${t}`}>
                    <h3><i className={`mk-takim-nokta is-${t}`}>{t}</i> {t} takımı <small>{l.length} kişi</small></h3>
                    <ul className="mk-oyuncular">{l.map(oyuncuSatir)}{!l.length && <li className="mk-oyuncu is-bos"><span className="mk-oyuncu-ad"><b>Henüz kimse yok</b></span></li>}</ul>
                  </div>
                );
              })}
            </div>
          ) : (
            <ul className="mk-oyuncular">{oda.oyuncular.map(oyuncuSatir)}{boslar(Math.min(enCok, Math.max(enAz, oda.oyuncular.length + 1)) - oda.oyuncular.length)}</ul>
          )}
          {oda.tur === 'takim' && <p className="mk-alan-not">Herkes kendi takımını değiştirebilir; kurucu herkesinkini. Ortaklar masada karşılıklı oturur.</p>}
        </section>

        <section className="mk-pano">
          <div className="mk-pano-bas">
            <h2>Ayarlar</h2>
            {!kurucu && <small className="mk-salt">Yalnız kurucu değiştirir</small>}
          </div>

          <div className="mk-alan">
            <span className="mk-alan-ad">Kaç el oynanacak</span>
            <div className="mk-dilim" role="radiogroup" aria-label="El sayısı">
              {EL_SECENEK.map((n) => (
                <button key={n} type="button" role="radio" aria-checked={oda.ayar.elSayisi === n} disabled={!kurucu} className={oda.ayar.elSayisi === n ? 'is-on' : ''} onClick={() => masa.ayar({ elSayisi: n })}>{n === 0 ? 'Bitirene dek' : n}</button>
              ))}
            </div>
            {oda.ayar.elSayisi === 0 && <small className="mk-alan-not">Maç, kurucu menüden “Oyunu bitir” diyene dek sürer.</small>}
          </div>

          <label className="mk-anahtar-satir">
            <span>
              <b><Sparkles size={16} /> Yardımcı asistan</b>
              <small>İpucu verir, işlek taşı gösterir, istenirse en iyi hamleyi oynar. Kapalıyken herkes kendi gözüne güvenir.</small>
            </span>
            <input type="checkbox" className="mk-anahtar" checked={oda.ayar.asistan} disabled={!kurucu} onChange={(e) => masa.ayar({ asistan: e.target.checked })} />
          </label>

          <div className="mk-alan">
            <span className="mk-alan-ad">Tema</span>
            <div className="mk-temalar" role="radiogroup" aria-label="Tema">
              {temalar.map((t) => (
                <button key={t} type="button" role="radio" aria-checked={oda.ayar.tema === t} disabled={!kurucu} className={`mk-tema is-${t}${oda.ayar.tema === t ? ' is-on' : ''}`} onClick={() => masa.ayar({ tema: t })}>
                  <span className="mk-tema-onizleme">
                    {okey ? (
                      <><TasOrnek s={7} r={0} renkler={taslak} tema={t} boy={26} /><TasOrnek s={8} r={2} renkler={taslak} tema={t} boy={26} /><TasOrnek s={0} r={0} renkler={taslak} tema={t} boy={26} kapali /></>
                    ) : (
                      <><KartOrnek renk="k" deger="7" tema={t} boy={30} /><KartOrnek deger="joker" tema={t} boy={30} /><KartOrnek tema={t} boy={30} kapali /></>
                    )}
                  </span>
                  <b>{TEMA_BILGI[t]?.ad || t}</b>
                  <small>{TEMA_BILGI[t]?.aciklama}</small>
                </button>
              ))}
            </div>
          </div>

          {okey && (
            <div className="mk-alan">
              <span className="mk-alan-ad">Taş renkleri</span>
              <div className="mk-renk-onizleme" aria-label="Taş önizlemesi">
                {[0, 1, 2, 3].map((r) => <TasOrnek key={r} s={[5, 11, 1, 13][r]} r={r as 0 | 1 | 2 | 3} renkler={taslak} tema={oda.ayar.tema} boy={40} />)}
              </div>
              {kurucu && (
                <>
                  <div className="mk-paletler" role="group" aria-label="Hazır paletler">
                    {PALETLER.map((p) => {
                      const secili = p.renkler.join() === taslak.join();
                      return (
                        <button key={p.ad} type="button" className={`mk-palet${secili ? ' is-on' : ''}`} aria-pressed={secili} onClick={() => renkYaz(p.renkler, true)}>
                          <span>{p.renkler.map((r) => <i key={r} style={{ background: r }} />)}</span>{p.ad}
                        </button>
                      );
                    })}
                  </div>
                  <div className="mk-renkler">
                    {taslak.map((r, i) => (
                      <label key={i} className={`mk-renk${soluk[i] ? ' is-uyari' : ''}`}>
                        <input type="color" value={r} aria-label={`${RENK_AD[i]} seç`} onChange={(e) => renkYaz(taslak.map((x, j) => (j === i ? e.target.value.toLowerCase() : x)))} />
                        <span>{RENK_AD[i]}</span>
                      </label>
                    ))}
                  </div>
                  {ayniVar && <p className="mk-ipucu is-hata"><AlertTriangle size={16} /> Dört renk birbirinden farklı olmalı; aynı renk iki kez seçili olduğu için değişiklik uygulanmadı.</p>}
                  {yakin && <p className="mk-ipucu is-uyari"><AlertTriangle size={16} /> İki renk birbirine çok yakın; masada karışabilir.</p>}
                  {soluk.some(Boolean) && <p className="mk-ipucu is-uyari"><AlertTriangle size={16} /> {soluk.map((s, i) => (s ? RENK_AD[i] : '')).filter(Boolean).join(', ')} fildişi taşın üstünde zor okunur; daha koyu bir ton seç.</p>}
                </>
              )}
            </div>
          )}
        </section>
      </div>

      <section className="mk-pano mk-ozet">
        <div className="mk-pano-bas">
          <h2><BookOpen size={18} /> Kısaca {OYUN_ADI[oda.tur]}</h2>
          <button type="button" className="mk-cip" onClick={() => kurallarAc(oda.tur)}>Tüm kurallar</button>
        </div>
        <ol>{OZET[oda.tur].map((s) => <li key={s}>{s}</li>)}</ol>
      </section>

      <footer className="mk-lobi-alt">
        {kurucu ? (
          <>
            <p className={neden ? 'is-uyari' : ''}>{neden || `${oda.oyuncular.length} oyuncu hazır. ${oda.ayar.elSayisi ? `${oda.ayar.elSayisi} el oynanacak.` : 'Sen bitirene dek oynanacak.'}`}</p>
            <button type="button" className="mk-dugme is-ana is-buyuk" disabled={!!neden} onClick={() => masa.baslat()}><Play size={20} /> Oyunu başlat</button>
          </>
        ) : (
          <p><span className="mk-donen" /> Kurucunun oyunu başlatması bekleniyor…</p>
        )}
      </footer>

      <DavetYapragi ac={davet} kapat={() => setDavet(false)} kod={oda.kod} masadakiler={oda.oyuncular.map((o) => o.id)} />
      <Onay ac={cikis} kapat={() => setCikis(false)} baslik="Masadan ayrıl" onayAd="Ayrıl" tehlike onay={() => masa.cik()}
        metin={kurucu && oda.oyuncular.some((o) => !o.bot && o.id !== oda.ben) ? 'Koltuğun boşalır ve kuruculuk masadaki başka bir oyuncuya geçer.' : kurucu ? 'Masada başka oyuncu yok; ayrılırsan masa kapanır.' : 'Koltuğun boşalır. Oyun başlamadıysa aynı kodla yeniden katılabilirsin.'} />
    </div>
  );
}

function DavetYapragi({ ac, kapat, kod, masadakiler }: { ac: boolean; kapat: () => void; kod: string; masadakiler: string[] }) {
  const [liste, setListe] = useState<Arkadas[] | null>(null);
  const [durum, setDurum] = useState<Record<string, 'gidiyor' | 'gitti' | string>>({});
  useEffect(() => {
    if (!ac) return;
    let canli = true;
    void safeJsonFetch<{ arkadaslar: Arkadas[] }>('/api/arkadas').then((r) => { if (canli) setListe(r.ok && Array.isArray(r.data?.arkadaslar) ? r.data!.arkadaslar : []); });
    return () => { canli = false; };
  }, [ac]);
  const cagir = async (k: string) => {
    setDurum((d) => ({ ...d, [k]: 'gidiyor' }));
    const r = await safeJsonFetch<{ ok?: boolean; error?: string }>('/api/masa/davet', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ kimlik: k, kod }) });
    setDurum((d) => ({ ...d, [k]: r.ok ? 'gitti' : (r.data?.error || r.error || 'Davet gönderilemedi.') }));
  };
  return (
    <Yaprak ac={ac} kapat={kapat} baslik="Arkadaş davet et">
      {liste === null ? <p className="mk-bos">Arkadaşların yükleniyor…</p> : !liste.length ? (
        <p className="mk-bos">Henüz arkadaşın yok. Masa kodunu ya da bağlantıyı paylaşarak herkesi çağırabilirsin.</p>
      ) : (
        <ul className="mk-davet">
          {liste.map((a) => {
            const d = durum[a.kimlik], masada = masadakiler.includes(a.kimlik);
            return (
              <li key={a.kimlik}>
                <Avatar ad={a.ad} foto={a.foto} id={a.kimlik} boy={40} />
                <span className="mk-davet-ad"><b>{a.ad}</b>{d && d !== 'gidiyor' && d !== 'gitti' && <small className="is-hata">{d}</small>}{d === 'gitti' && <small>Bildirim gönderildi</small>}</span>
                {masada ? <i className="mk-rozet is-iyi">Masada</i> : (
                  <button type="button" className="mk-dugme is-ana" disabled={d === 'gidiyor' || d === 'gitti'} onClick={() => void cagir(a.kimlik)}>{d === 'gitti' ? <><Check size={16} /> Gitti</> : 'Davet et'}</button>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </Yaprak>
  );
}
