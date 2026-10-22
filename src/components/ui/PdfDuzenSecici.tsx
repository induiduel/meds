/**
 * PDF ayar penceresi (Metni indir + Toplu PDF ortak): solda seçili ayarlarla üretilmiş gerçek örnek sayfa,
 * sağda sade sorular (hazır görünüm, yazı büyüklüğü, renk, kâğıda kaç sayfa, ekler) ve katlanır "Daha fazla ayar".
 */
import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { RotateCcw, Settings2, X } from 'lucide-react';
import { VARSAYILAN_DUZEN, type PdfDuzen, type PdfStil, type SayfaSayisi } from '../../services/pdfDuzen';
import '../../styles/pdf-duzen.css';

const NUP: SayfaSayisi[] = [1, 2, 4, 8];
const RENK: { id: PdfStil['renk']; ad: string; hex: string }[] = [
  { id: 'mavi', ad: 'Mavi', hex: '#0d6e96' }, { id: 'yesil', ad: 'Yeşil', hex: '#167852' },
  { id: 'mor', ad: 'Mor', hex: '#6840a8' }, { id: 'bordo', ad: 'Bordo', hex: '#96243a' },
  { id: 'turuncu', ad: 'Turuncu', hex: '#be5c14' }, { id: 'murekkep', ad: 'Siyah-beyaz', hex: '#282828' },
];
const SABLON: { ad: string; alt: string; p: Partial<PdfDuzen> }[] = [
  { ad: 'Standart', alt: 'Ekranda okumak için', p: {} },
  { ad: 'Az kâğıt', alt: 'Bir kâğıda 2 sayfa, siyah-beyaz', p: { nup: 2, kenar: 'dar', satirAraligi: 'sik', renk: 'murekkep', yaziBoyutu: 'kucuk' } },
  { ad: 'Rahat okuma', alt: 'Büyük yazı, geniş satır', p: { yaziBoyutu: 'buyuk', satirAraligi: 'ferah', kenar: 'genis' } },
  { ad: 'Sınav dosyası', alt: 'Kapaklı, her konu ayrı sayfada', p: { kapak: true, bolumYeniSayfa: true, baslikBoyutu: 'buyuk' } },
];
const PdfOnizleme = React.lazy(() => import('./PdfOnizleme'));

function Simge({ n }: { n: SayfaSayisi }) {
  const [kol, sat, yatay] = n === 2 ? [2, 1, true] : n === 4 ? [2, 2, false] : n === 8 ? [4, 2, true] : [1, 1, false];
  return (
    <span className={`pdz-simge${yatay ? ' is-yatay' : ''}`} style={{ gridTemplateColumns: `repeat(${kol}, 1fr)`, gridTemplateRows: `repeat(${sat}, 1fr)` }} aria-hidden>
      {Array.from({ length: n }, (_, i) => <i key={i} />)}
    </span>
  );
}

function Soru({ baslik, children }: { baslik: string; children: React.ReactNode }) {
  return <section className="pdz-soru"><h4>{baslik}</h4>{children}</section>;
}

function Secim<T extends string>({ ad, deger, ops, onDegis }: { ad: string; deger: T; ops: [T, string][]; onDegis: (v: T) => void }) {
  return (
    <div className="pdz-satir">
      <span className="pdz-etiket">{ad}</span>
      <div className="pdz-seg" role="radiogroup" aria-label={ad}>
        {ops.map(([v, e]) => (
          <button key={v} type="button" role="radio" aria-checked={deger === v} className={deger === v ? 'is-on' : ''} onClick={() => onDegis(v)}>{e}</button>
        ))}
      </div>
    </div>
  );
}

function Anahtar({ ad, alt, deger, onDegis }: { ad: string; alt?: string; deger: boolean; onDegis: (v: boolean) => void }) {
  return (
    <label className="pdz-anahtar">
      <span><b>{ad}</b>{alt && <small>{alt}</small>}</span>
      <input type="checkbox" role="switch" checked={deger} onChange={(e) => onDegis(e.target.checked)} />
      <span className="pdz-anahtar-yuva" aria-hidden />
    </label>
  );
}

export function PdfDuzenSecici({ deger, onDegis, ad = 'pdz' }: { deger: PdfDuzen; onDegis: (d: PdfDuzen) => void; ad?: string }) {
  const set = (p: Partial<PdfDuzen>) => onDegis({ ...deger, ...p });
  const sablonMu = (p: Partial<PdfDuzen>) => Object.entries({ ...VARSAYILAN_DUZEN, ...p }).every(([k, v]) => deger[k as keyof PdfDuzen] === v);
  return (
    <div className="pdz">
      <div className="pdz-oniz-kol">
        <React.Suspense fallback={<div className="pdo"><div className="pdo-kagit is-yuk" /></div>}>
          <PdfOnizleme d={deger} />
        </React.Suspense>
      </div>

      <div className="pdz-ayarlar">
        <Soru baslik="Hazır görünümler">
          <div className="pdz-sablon" role="radiogroup" aria-label="Hazır görünümler">
            {SABLON.map((s) => (
              <button key={s.ad} type="button" role="radio" aria-checked={sablonMu(s.p)} className={sablonMu(s.p) ? 'is-on' : ''} onClick={() => onDegis({ ...VARSAYILAN_DUZEN, ...s.p, ustBilgi: deger.ustBilgi, filigran: deger.filigran })}>
                <b>{s.ad}</b><small>{s.alt}</small>
              </button>
            ))}
          </div>
        </Soru>

        <Soru baslik="Yazı büyüklüğü">
          <div className="pdz-yazi" role="radiogroup" aria-label="Yazı büyüklüğü">
            {([['kucuk', 'Küçük', 13], ['normal', 'Normal', 16], ['buyuk', 'Büyük', 19], ['cokbuyuk', 'Çok büyük', 22]] as const).map(([v, e, px]) => (
              <button key={v} type="button" role="radio" aria-checked={deger.yaziBoyutu === v} className={deger.yaziBoyutu === v ? 'is-on' : ''} onClick={() => set({ yaziBoyutu: v })}>
                <span style={{ fontSize: px }} aria-hidden>Aa</span><small>{e}</small>
              </button>
            ))}
          </div>
        </Soru>

        <Soru baslik="Başlık rengi">
          <div className="pdz-renkler" role="radiogroup" aria-label="Başlık rengi">
            {RENK.map((r) => (
              <button key={r.id} type="button" role="radio" aria-checked={deger.renk === r.id} aria-label={r.ad} title={r.ad} className={deger.renk === r.id ? 'is-on' : ''} onClick={() => set({ renk: r.id })}>
                <i style={{ background: r.hex }} aria-hidden />
              </button>
            ))}
            <span className="pdz-renk-ad">{RENK.find((r) => r.id === deger.renk)?.ad}</span>
          </div>
        </Soru>

        <Soru baslik="Bir kâğıda kaç sayfa basılsın?">
          <div className="pdz-nup" role="radiogroup" aria-label="Bir kâğıda kaç sayfa">
            {NUP.map((n) => (
              <label key={n} className={`pdz-nup-ops${deger.nup === n ? ' is-on' : ''}`}>
                <input type="radio" name={`${ad}-nup`} checked={deger.nup === n} onChange={() => set({ nup: n })} />
                <Simge n={n} />
                <span>{n === 1 ? '1 sayfa' : `${n} sayfa`}</span>
              </label>
            ))}
          </div>
        </Soru>

        <Soru baslik="Eklensin mi?">
          <div className="pdz-anahtarlar">
            <Anahtar ad="Kapak sayfası" alt="Ders adı ve tarih ilk sayfada" deger={deger.kapak} onDegis={(kapak) => set({ kapak })} />
            <Anahtar ad="Her konu yeni sayfada" alt="Konular birbirine karışmaz" deger={deger.bolumYeniSayfa} onDegis={(bolumYeniSayfa) => set({ bolumYeniSayfa })} />
            <Anahtar ad="Önemli yerleri vurgula" alt="Sarı fosfor ve kırmızı yazı" deger={deger.vurgu} onDegis={(vurgu) => set({ vurgu })} />
          </div>
        </Soru>

        <details className="pdz-daha">
          <summary>Daha fazla ayar</summary>
          <div className="pdz-daha-ic">
            <Secim ad="Kâğıt boyutu" deger={deger.kagit} ops={[['a4', 'A4'], ['a5', 'A5 (küçük)'], ['letter', 'Letter']]} onDegis={(kagit) => set({ kagit })} />
            <Secim ad="Kenar boşluğu" deger={deger.kenar} ops={[['dar', 'Dar'], ['normal', 'Normal'], ['genis', 'Geniş']]} onDegis={(kenar) => set({ kenar })} />
            <Secim ad="Satır aralığı" deger={deger.satirAraligi} ops={[['sik', 'Sık'], ['normal', 'Normal'], ['ferah', 'Geniş']]} onDegis={(satirAraligi) => set({ satirAraligi })} />
            <Secim ad="Başlık büyüklüğü" deger={deger.baslikBoyutu} ops={[['kucuk', 'Sade'], ['normal', 'Normal'], ['buyuk', 'Belirgin']]} onDegis={(baslikBoyutu) => set({ baslikBoyutu })} />
            <Secim ad="Sayfa numarası" deger={deger.altBilgi} ops={[['baslik-no', 'Başlıkla'], ['no-orta', 'Ortada'], ['no-sag', 'Sağda'], ['yok', 'Olmasın']]} onDegis={(altBilgi) => set({ altBilgi })} />
            {deger.nup > 1 && <>
              <Secim ad="Kâğıt yönü" deger={deger.yon} ops={[['oto', 'Otomatik'], ['dikey', 'Dikey'], ['yatay', 'Yatay']]} onDegis={(yon) => set({ yon })} />
              <Secim ad="Sayfa sırası" deger={deger.sira} ops={[['satir', 'Soldan sağa'], ['sutun', 'Yukarıdan aşağı']]} onDegis={(sira) => set({ sira })} />
              <Anahtar ad="Sayfaların çevresine çizgi" deger={deger.cerceve} onDegis={(cerceve) => set({ cerceve })} />
            </>}
            <label className="pdz-satir">
              <span className="pdz-etiket">Yalnız şu sayfalar</span>
              <input className="pdz-girdi" inputMode="numeric" placeholder="Boşsa hepsi · örnek: 1-5, 8" value={deger.sayfaAraligi} onChange={(e) => set({ sayfaAraligi: e.target.value.replace(/[^\d,;\-\s]/g, '') })} />
            </label>
            <label className="pdz-satir">
              <span className="pdz-etiket">Her sayfanın üstüne yazı</span>
              <input className="pdz-girdi" maxLength={120} placeholder="Boşsa yok · örnek: Kurul 2 Patoloji" value={deger.ustBilgi} onChange={(e) => set({ ustBilgi: e.target.value })} />
            </label>
            <label className="pdz-satir">
              <span className="pdz-etiket">Sayfa kenarına adın</span>
              <input className="pdz-girdi" maxLength={60} placeholder="Boşsa yok" value={deger.filigran} onChange={(e) => set({ filigran: e.target.value })} />
            </label>
            <button type="button" className="pdz-sifirla" onClick={() => onDegis({ ...VARSAYILAN_DUZEN })}><RotateCcw aria-hidden /> Her şeyi baştaki hâline döndür</button>
          </div>
        </details>
      </div>
    </div>
  );
}

/** Ayar paneli ayrı diyalogda: menüler/diyaloglar içinde yalnız özet + "Ayarla" düğmesi durur */
export function PdfAyarDugme({ deger, onDegis, ad = 'pdz' }: { deger: PdfDuzen; onDegis: (d: PdfDuzen) => void; ad?: string }) {
  const [acik, setAcik] = useState(false);
  const ozet = [
    deger.nup > 1 ? `${deger.nup} sayfa/yaprak` : deger.kagit.toUpperCase(),
    { kucuk: 'küçük yazı', normal: 'normal yazı', buyuk: 'büyük yazı', cokbuyuk: 'çok büyük yazı' }[deger.yaziBoyutu],
    RENK.find((r) => r.id === deger.renk)?.ad.toLowerCase(),
    deger.kapak && 'kapak',
    deger.sayfaAraligi.trim() && `sayfa ${deger.sayfaAraligi.trim()}`,
  ].filter(Boolean).join(' · ');
  return (
    <>
      <button type="button" className="pdz-ac" onClick={() => setAcik(true)} aria-haspopup="dialog">
        <Settings2 aria-hidden />
        <span><b>PDF ayarları</b><small>{ozet}</small></span>
        <span className="pdz-ac-git">Ayarla</span>
      </button>
      {acik && createPortal(<PdfAyarDiyalog deger={deger} onDegis={onDegis} ad={ad} onKapat={() => setAcik(false)} />, document.body)}
    </>
  );
}

function PdfAyarDiyalog({ deger, onDegis, ad, onKapat }: { deger: PdfDuzen; onDegis: (d: PdfDuzen) => void; ad: string; onKapat: () => void }) {
  const kapatRef = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    kapatRef.current?.focus();
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') { e.stopPropagation(); onKapat(); } };
    document.addEventListener('keydown', k, true);
    return () => document.removeEventListener('keydown', k, true);
  }, [onKapat]);
  return (
    <div className="pdz-perde" data-ls-keep role="presentation" onClick={(e) => { if (e.target === e.currentTarget) onKapat(); }}>
      <div className="pdz-diyalog" role="dialog" aria-modal="true" aria-labelledby={`${ad}-db`}>
        <header className="pdz-d-bas">
          <span><b id={`${ad}-db`}>PDF nasıl görünsün?</b><small>Seçtikçe örnek sayfa hemen değişir</small></span>
          <button ref={kapatRef} type="button" className="pdz-d-x" onClick={onKapat} aria-label="Kapat"><X aria-hidden /></button>
        </header>
        <div className="pdz-d-govde"><PdfDuzenSecici deger={deger} onDegis={onDegis} ad={ad} /></div>
        <footer className="pdz-d-alt">
          <small>Seçimler bu cihazda hatırlanır.</small>
          <button type="button" className="pdz-d-tamam" onClick={onKapat}>Tamam</button>
        </footer>
      </div>
    </div>
  );
}
