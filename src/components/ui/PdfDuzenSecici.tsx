/**
 * PDF ayar paneli (Metni indir + Toplu PDF ortak): hazır şablonlar, canlı küçük önizleme ve dört sekme:
 *  Sayfa (yaprağa kaç sayfa, kâğıt, kenar, sayfa aralığı, yön/sıra/çerçeve) · Yazı (metin/başlık boyutu, satır aralığı)
 *  Renk (tema, önemli işaretleri) · Ekler (kapak, konu başına yeni sayfa, üst bilgi, sayfa numarası, kenar yazısı).
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
  { ad: 'Standart', alt: 'Ekranda okuma', p: {} },
  { ad: 'Yazdırma tasarrufu', alt: '2 sayfa/yaprak, dar kenar', p: { nup: 2, kenar: 'dar', satirAraligi: 'sik', renk: 'murekkep', yaziBoyutu: 'kucuk' } },
  { ad: 'Rahat okuma', alt: 'Büyük yazı, ferah satır', p: { yaziBoyutu: 'buyuk', satirAraligi: 'ferah', kenar: 'genis' } },
  { ad: 'Sınav dosyası', alt: 'Kapak, konu başına sayfa', p: { kapak: true, bolumYeniSayfa: true, baslikBoyutu: 'buyuk' } },
];
const SEKME = ['Sayfa', 'Yazı', 'Renk', 'Ekler'] as const;

function Simge({ n }: { n: SayfaSayisi }) {
  const [kol, sat, yatay] = n === 2 ? [2, 1, true] : n === 4 ? [2, 2, false] : n === 8 ? [4, 2, true] : [1, 1, false];
  return (
    <span className={`pdz-simge${yatay ? ' is-yatay' : ''}`} style={{ gridTemplateColumns: `repeat(${kol}, 1fr)`, gridTemplateRows: `repeat(${sat}, 1fr)` }} aria-hidden>
      {Array.from({ length: n }, (_, i) => <i key={i} />)}
    </span>
  );
}

/** Seçeneklerin görünüme etkisini gösteren küçük sayfa çizimi */
function Onizleme({ d }: { d: PdfDuzen }) {
  const renk = RENK.find((r) => r.id === d.renk)?.hex || '#0d6e96';
  const yazi = { kucuk: 0.85, normal: 1, buyuk: 1.15, cokbuyuk: 1.3 }[d.yaziBoyutu];
  const satir = { sik: 4, normal: 5, ferah: 6.5 }[d.satirAraligi] * yazi;
  const kenar = { dar: 7, normal: 11, genis: 15 }[d.kenar];
  const baslik = { kucuk: 0.85, normal: 1, buyuk: 1.2 }[d.baslikBoyutu] * yazi;
  const H = d.kagit === 'a5' ? 118 : d.kagit === 'letter' ? 108 : 124;
  const satirlar: React.ReactNode[] = [];
  let y = kenar + (d.ustBilgi ? 6 : 0) + 12 * baslik;
  for (let i = 0; y < H - kenar - 8; i++) {
    const vurgu = d.vurgu && i === 3;
    satirlar.push(
      <g key={i}>
        {vurgu && <rect x={kenar + 10} y={y - 2.6} width={22} height={3.6} fill="#ffe980" />}
        <rect x={kenar} y={y - 1.2} width={(i % 4 === 3 ? 0.55 : 0.92) * (88 - 2 * kenar)} height={1.3 * yazi} rx={0.6} fill={vurgu ? '#c8262d' : '#9aa3ad'} opacity={vurgu ? 0.9 : 0.6} />
      </g>,
    );
    y += satir;
    if (i === 4) {
      y += 2;
      satirlar.push(<rect key="b2" x={kenar} y={y - 2} width={36} height={2.4 * baslik} rx={0.6} fill={renk} />);
      y += satir + 1;
    }
  }
  return (
    <svg className="pdz-oniz" viewBox={`0 0 88 ${H}`} role="img" aria-label="Sayfa önizlemesi">
      <rect x={0.5} y={0.5} width={87} height={H - 1} rx={2} fill="#fff" stroke="#c9d0d8" />
      {d.ustBilgi && <><rect x={kenar} y={kenar - 3} width={30} height={1.2} fill="#9aa3ad" /><line x1={kenar} x2={88 - kenar} y1={kenar} y2={kenar} stroke="#d6dce3" strokeWidth={0.4} /></>}
      <rect x={kenar} y={kenar + (d.ustBilgi ? 6 : 0)} width={1.4} height={7 * baslik} fill={renk} />
      <rect x={kenar + 3} y={kenar + (d.ustBilgi ? 6 : 0) + 1} width={44 * Math.min(baslik, 1.2)} height={4 * baslik} rx={0.8} fill={renk} />
      {satirlar}
      {d.altBilgi !== 'yok' && (
        <g fill="#9aa3ad">
          {d.altBilgi === 'baslik-no' && <rect x={kenar} y={H - 6} width={26} height={1.2} />}
          <rect x={d.altBilgi === 'no-orta' ? 40 : 88 - kenar - 8} y={H - 6} width={8} height={1.2} />
        </g>
      )}
      {d.filigran && <rect x={85} y={H / 2 - 12} width={1} height={24} fill="#c9d0d8" />}
    </svg>
  );
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
      <input type="checkbox" role="switch" checked={deger} onChange={(e) => onDegis(e.target.checked)} />
      <span className="pdz-anahtar-yuva" aria-hidden />
      <span><b>{ad}</b>{alt && <small>{alt}</small>}</span>
    </label>
  );
}

export function PdfDuzenSecici({ deger, onDegis, ad = 'pdz' }: { deger: PdfDuzen; onDegis: (d: PdfDuzen) => void; ad?: string }) {
  const [sekme, setSekme] = useState<(typeof SEKME)[number]>('Sayfa');
  const set = (p: Partial<PdfDuzen>) => onDegis({ ...deger, ...p });
  const sablonMu = (p: Partial<PdfDuzen>) => Object.entries({ ...VARSAYILAN_DUZEN, ...p }).every(([k, v]) => deger[k as keyof PdfDuzen] === v);
  return (
    <div className="pdz">
      <div className="pdz-sablon" role="group" aria-label="Hazır şablonlar">
        {SABLON.map((s) => (
          <button key={s.ad} type="button" className={sablonMu(s.p) ? 'is-on' : ''} onClick={() => onDegis({ ...VARSAYILAN_DUZEN, ...s.p, ustBilgi: deger.ustBilgi, filigran: deger.filigran })}>
            <b>{s.ad}</b><small>{s.alt}</small>
          </button>
        ))}
      </div>

      <div className="pdz-govde">
        <Onizleme d={deger} />
        <div className="pdz-panel">
          <div className="pdz-sekmeler" role="tablist" aria-label="PDF ayarları">
            {SEKME.map((s) => (
              <button key={s} type="button" role="tab" id={`${ad}-t-${s}`} aria-selected={sekme === s} className={sekme === s ? 'is-on' : ''} onClick={() => setSekme(s)}>{s}</button>
            ))}
            <button type="button" className="pdz-sifirla" onClick={() => onDegis({ ...VARSAYILAN_DUZEN })} title="Tüm ayarları varsayılana döndür" aria-label="Varsayılana döndür"><RotateCcw aria-hidden /></button>
          </div>

          <div className="pdz-icerik" role="tabpanel" aria-labelledby={`${ad}-t-${sekme}`}>
            {sekme === 'Sayfa' && <>
              <div className="pdz-nup" role="radiogroup" aria-label="Bir yaprağa kaç sayfa">
                {NUP.map((n) => (
                  <label key={n} className={`pdz-nup-ops${deger.nup === n ? ' is-on' : ''}`}>
                    <input type="radio" name={`${ad}-nup`} checked={deger.nup === n} onChange={() => set({ nup: n })} />
                    <Simge n={n} />
                    <span>{n === 1 ? 'Normal' : `${n} sayfa`}</span>
                  </label>
                ))}
              </div>
              {deger.nup > 1 && <>
                <Secim ad="Yaprak yönü" deger={deger.yon} ops={[['oto', 'Otomatik'], ['dikey', 'Dikey'], ['yatay', 'Yatay']]} onDegis={(yon) => set({ yon })} />
                <Secim ad="Sıra" deger={deger.sira} ops={[['satir', 'Soldan sağa'], ['sutun', 'Yukarıdan aşağı']]} onDegis={(sira) => set({ sira })} />
                <Secim ad="Aralık" deger={deger.bosluk} ops={[['normal', 'Normal'], ['dar', 'Dar']]} onDegis={(bosluk) => set({ bosluk })} />
                <Anahtar ad="Sayfa çerçevesi" deger={deger.cerceve} onDegis={(cerceve) => set({ cerceve })} />
              </>}
              <Secim ad="Kâğıt" deger={deger.kagit} ops={[['a4', 'A4'], ['a5', 'A5'], ['letter', 'Letter']]} onDegis={(kagit) => set({ kagit })} />
              <Secim ad="Kenar boşluğu" deger={deger.kenar} ops={[['dar', 'Dar'], ['normal', 'Normal'], ['genis', 'Geniş']]} onDegis={(kenar) => set({ kenar })} />
              <label className="pdz-satir">
                <span className="pdz-etiket">Sayfa aralığı</span>
                <input className="pdz-girdi" inputMode="numeric" placeholder="Tümü (örn. 1-5, 8)" value={deger.sayfaAraligi} onChange={(e) => set({ sayfaAraligi: e.target.value.replace(/[^\d,;\-\s]/g, '') })} />
              </label>
            </>}

            {sekme === 'Yazı' && <>
              <Secim ad="Metin boyutu" deger={deger.yaziBoyutu} ops={[['kucuk', 'Küçük'], ['normal', 'Normal'], ['buyuk', 'Büyük'], ['cokbuyuk', 'Çok büyük']]} onDegis={(yaziBoyutu) => set({ yaziBoyutu })} />
              <Secim ad="Başlık boyutu" deger={deger.baslikBoyutu} ops={[['kucuk', 'Sade'], ['normal', 'Normal'], ['buyuk', 'Belirgin']]} onDegis={(baslikBoyutu) => set({ baslikBoyutu })} />
              <Secim ad="Satır aralığı" deger={deger.satirAraligi} ops={[['sik', 'Sık'], ['normal', 'Normal'], ['ferah', 'Ferah']]} onDegis={(satirAraligi) => set({ satirAraligi })} />
            </>}

            {sekme === 'Renk' && <>
              <div className="pdz-satir">
                <span className="pdz-etiket">Başlık ve işaret rengi</span>
                <div className="pdz-renkler" role="radiogroup" aria-label="Renk teması">
                  {RENK.map((r) => (
                    <button key={r.id} type="button" role="radio" aria-checked={deger.renk === r.id} className={deger.renk === r.id ? 'is-on' : ''} onClick={() => set({ renk: r.id })} title={r.ad}>
                      <i style={{ background: r.hex }} aria-hidden /><span>{r.ad}</span>
                    </button>
                  ))}
                </div>
              </div>
              <Anahtar ad="Önemli yer işaretleri" alt="Sarı fosfor + kırmızı yazı; kapalıyken düz metin" deger={deger.vurgu} onDegis={(vurgu) => set({ vurgu })} />
            </>}

            {sekme === 'Ekler' && <>
              <Anahtar ad="Kapak sayfası" alt="Başlık, açıklama ve tarih ayrı ilk sayfada" deger={deger.kapak} onDegis={(kapak) => set({ kapak })} />
              <Anahtar ad="Her konu yeni sayfada" alt="Sayfa sayısı artar, konular karışmaz" deger={deger.bolumYeniSayfa} onDegis={(bolumYeniSayfa) => set({ bolumYeniSayfa })} />
              <Secim ad="Sayfa numarası" deger={deger.altBilgi} ops={[['baslik-no', 'Başlık + no'], ['no-orta', 'Ortada'], ['no-sag', 'Sağda'], ['yok', 'Yok']]} onDegis={(altBilgi) => set({ altBilgi })} />
              <label className="pdz-satir">
                <span className="pdz-etiket">Üst bilgi</span>
                <input className="pdz-girdi" maxLength={120} placeholder="Boş bırakılırsa yok (örn. Kurul 2 – Patoloji)" value={deger.ustBilgi} onChange={(e) => set({ ustBilgi: e.target.value })} />
              </label>
              <label className="pdz-satir">
                <span className="pdz-etiket">Kenar yazısı</span>
                <input className="pdz-girdi" maxLength={60} placeholder="Sayfa kenarında dikey (örn. adın)" value={deger.filigran} onChange={(e) => set({ filigran: e.target.value })} />
              </label>
            </>}
          </div>
        </div>
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
          <b id={`${ad}-db`}>PDF ayarları</b>
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
