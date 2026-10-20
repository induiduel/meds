/**
 * Son Prova — soru çözme ekranı. Dört kip:
 *  - asama:   aşama sonu soruları (sesli asistan soruyu okur; cevapta doğru/yanlış + şık açıklaması + çözüm sesli)
 *  - checkup: part sonu check-up (aynı akış), genel: dersin genel check-up'ı (aynı akış)
 *  - deneme:  süreli sınav provası; cevaplar sınav bitene kadar gösterilmez, sonuçta branş/aşama dökümü
 * Her sonuç ekranı yanlışların aşamalarını listeler ve o aşamaya (sesli özette) götürür.
 */
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowLeft, ArrowRight, Check, ChevronRight, Clock, Flag, LifeBuoy, ListChecks, RotateCcw, Volume2, VolumeX, X,
} from 'lucide-react';
import {
  BRANS_KISA, spBrans, spKlip, spPartBul, spSorulariYukle, spYaz, useSpKayit, yuzde, zayifAsamalar,
  type Harf, type SpIndex, type SpSoru, type TestSonuc,
} from './spVeri';

type Q = SpSoru & { ref: string };
export type TestKip = 'asama' | 'checkup' | 'genel' | 'deneme';

const SES_KEY = 'medsoru_son_prova_ses';
const sesAcikOku = () => { try { return localStorage.getItem(SES_KEY) !== '0'; } catch { return true; } };

/** Sıralı klip çalar: yeni dizi gelince öncekini keser */
function useKlipCalar(acik: boolean) {
  const el = useRef<HTMLAudioElement | null>(null);
  const sira = useRef(0);
  const [caliyor, setCaliyor] = useState(false);
  const dur = useCallback(() => {
    sira.current++;
    if (el.current) { el.current.pause(); el.current.removeAttribute('src'); }
    setCaliyor(false);
  }, []);
  const cal = useCallback((urls: (string | null)[]) => {
    dur();
    if (!acik) return;
    const liste = urls.filter((u): u is string => !!u);
    if (!liste.length) return;
    const ben = ++sira.current;
    if (!el.current) el.current = new Audio();
    const a = el.current;
    let i = 0;
    const sonraki = () => {
      if (ben !== sira.current) return;
      if (i >= liste.length) { setCaliyor(false); return; }
      a.src = liste[i++];
      a.onended = sonraki;
      a.onerror = sonraki;
      a.play().then(() => setCaliyor(true)).catch(() => setCaliyor(false));
    };
    sonraki();
  }, [acik, dur]);
  useEffect(() => dur, [dur]);
  return { cal, dur, caliyor };
}

export function asamaYolu(ix: SpIndex, partKey: string, no: number): string | null {
  const b = spPartBul(ix, partKey);
  return b ? `/son-prova/${b.ders.brans}/${b.part.no}?asama=${no}` : null;
}

function harfler(q: Q): Harf[] {
  return (['A', 'B', 'C', 'D', 'E'] as Harf[]).filter((h) => q.secenekler[h]);
}

function SoruGovde({ q, i, n }: { q: Q; i: number; n: number }) {
  return (
    <div className="sp-soru-kok">
      <div className="sp-soru-ust">
        <span className="sp-mono">Soru {i + 1}/{n}</span>
        <span className="sp-chip">{BRANS_KISA[spBrans(q.ref)] || spBrans(q.ref)}</span>
        {q.tur === 'cikmis' && <span className="sp-chip is-cikmis" title={q.sinav}>Çıkmış</span>}
        {q.zorluk && <span className="sp-chip">{q.zorluk}</span>}
      </div>
      <p className="sp-kok">{q.soru}</p>
    </div>
  );
}

/** Kaynak + aşama bağlantısı */
function Kaynak({ q, ix, onGit }: { q: Q; ix: SpIndex; onGit: (yol: string) => void }) {
  const b = spPartBul(ix, q.asama[0]);
  const a = b?.part.asamalar.find((x) => x.no === q.asama[1]);
  const yol = asamaYolu(ix, q.asama[0], q.asama[1]);
  return (
    <p className="sp-kaynak">
      {b && a ? (
        <>Bu bilgi: <b>{BRANS_KISA[b.ders.brans]} {b.ders.partlar.length > 1 ? `Part ${b.part.no} · ` : ''}Aşama {a.no}</b> — {a.dersNo}) {a.dersAd}
          {q.kaynak.s.length ? <>, slayt {q.kaynak.s.slice(0, 3).join(', ')}</> : null}
          {yol && <button type="button" className="sp-link" onClick={() => onGit(yol)}>Bu bölüme dön <ChevronRight aria-hidden /></button>}
        </>
      ) : null}
    </p>
  );
}

export interface SpTestProps {
  ix: SpIndex;
  kip: TestKip;
  refs: string[];
  baslik: string;
  alt?: string;
  /** ilerleme anahtarı (asama: "<part>:<no>", checkup: part, genel: "k1:<brans>", deneme: "k1:<no>") */
  anahtar: string;
  sureDk?: number;
  onKapat: () => void;
  onGit: (yol: string) => void;
  /** aşama kipinde: bitince "derse devam" */
  devamEtiket?: string;
}

export default function SpTest({ ix, kip, refs, baslik, alt, anahtar, sureDk, onKapat, onGit, devamEtiket }: SpTestProps) {
  const [sorular, setSorular] = useState<Q[] | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const kayit = useSpKayit();
  const deneme = kip === 'deneme';
  const [i, setI] = useState(0);
  const [cevap, setCevap] = useState<Record<string, Harf>>(() => (deneme ? kayit.deneme[anahtar]?.cevap || {} : {}));
  const [yardim, setYardim] = useState<Record<string, boolean>>({});
  const [bitti, setBitti] = useState<boolean>(() => (deneme ? !!kayit.deneme[anahtar]?.bitti : false));
  const [sesAcik, setSesAcik] = useState(sesAcikOku);
  const { cal, dur, caliyor } = useKlipCalar(sesAcik && !deneme);
  const ustRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let iptal = false;
    spSorulariYukle(ix.kurul, refs).then((q) => { if (!iptal) setSorular(q); }).catch((e) => setHata(String(e?.message || e)));
    return () => { iptal = true; };
  }, [ix.kurul, refs]);

  // deneme: başlangıç zamanı ve cevaplar kalıcı (sayfa kapanıp açılınca kaldığı yerden sürer)
  useEffect(() => {
    if (!deneme) return;
    spYaz((k) => (k.deneme[anahtar] ? k : { ...k, deneme: { ...k.deneme, [anahtar]: { cevap: {}, bas: Date.now() } } }));
  }, [deneme, anahtar]);
  const bas = kayit.deneme[anahtar]?.bas || Date.now();
  const [simdi, setSimdi] = useState(Date.now());
  useEffect(() => {
    if (!deneme || bitti) return;
    const t = window.setInterval(() => setSimdi(Date.now()), 1000);
    return () => window.clearInterval(t);
  }, [deneme, bitti]);
  const kalanSn = deneme && sureDk ? Math.max(0, Math.round(sureDk * 60 - (simdi - bas) / 1000)) : 0;

  const q = sorular?.[i];
  // soru açılınca sesli asistan okur (deneme hariç)
  useEffect(() => {
    if (!q || deneme || bitti) return;
    if (!cevap[q.ref]) cal([spKlip(q.ref, q, 'q')]);
    ustRef.current?.scrollIntoView({ block: 'nearest' });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [q?.ref]);

  const sec = (h: Harf) => {
    if (!q || bitti) return;
    if (deneme) {
      const n = { ...cevap, [q.ref]: h };
      setCevap(n);
      spYaz((k) => ({ ...k, deneme: { ...k.deneme, [anahtar]: { ...(k.deneme[anahtar] || { bas: Date.now() }), cevap: n } } }));
      return;
    }
    if (cevap[q.ref]) return;
    setCevap((c) => ({ ...c, [q.ref]: h }));
    if (h === q.dogru) cal([spKlip(q.ref, q, 'd'), spKlip(q.ref, q, 'c')]);
    else cal([spKlip(q.ref, q, 's', h), spKlip(q.ref, q, 'c')]);
  };

  const sonuc = useMemo<TestSonuc | null>(() => {
    if (!sorular) return null;
    const yanlis = sorular.filter((x) => cevap[x.ref] !== x.dogru).map((x) => x.ref);
    return { d: sorular.length - yanlis.length, n: sorular.length, at: Date.now(), yanlis };
  }, [sorular, cevap]);

  const bitir = useCallback(() => {
    if (!sonuc) return;
    dur();
    setBitti(true);
    spYaz((k) => {
      if (kip === 'asama') return { ...k, asama: { ...k.asama, [anahtar]: sonuc } };
      if (kip === 'checkup') return { ...k, checkup: { ...k.checkup, [anahtar]: sonuc } };
      if (kip === 'genel') return { ...k, genel: { ...k.genel, [anahtar]: sonuc } };
      return { ...k, deneme: { ...k.deneme, [anahtar]: { ...(k.deneme[anahtar] || { bas: Date.now(), cevap }), cevap, bitti: Date.now(), sonuc } } };
    });
  }, [sonuc, kip, anahtar, cevap, dur]);

  useEffect(() => { if (deneme && sureDk && !bitti && kalanSn === 0 && sorular) bitir(); }, [deneme, sureDk, bitti, kalanSn, sorular, bitir]);

  const yeniden = () => {
    dur();
    setCevap({});
    setYardim({});
    setI(0);
    setBitti(false);
    if (deneme) spYaz((k) => ({ ...k, deneme: { ...k.deneme, [anahtar]: { cevap: {}, bas: Date.now() } } }));
  };
  const sesDegis = () => {
    const v = !sesAcik;
    setSesAcik(v);
    try { localStorage.setItem(SES_KEY, v ? '1' : '0'); } catch { /* yok */ }
    if (!v) dur();
  };

  useEffect(() => {
    const f = (e: KeyboardEvent) => {
      if (!q || bitti || (e.target as HTMLElement)?.closest('input,textarea')) return;
      const h = e.key.toUpperCase();
      if (['A', 'B', 'C', 'D', 'E'].includes(h) && q.secenekler[h as Harf]) { e.preventDefault(); sec(h as Harf); }
      else if (e.key === 'ArrowRight' && sorular && i < sorular.length - 1) setI(i + 1);
      else if (e.key === 'ArrowLeft' && i > 0) setI(i - 1);
    };
    window.addEventListener('keydown', f);
    return () => window.removeEventListener('keydown', f);
  });

  if (hata) return <div className="sp-kart sp-bos"><p>{hata}</p><button type="button" className="sp-btn" onClick={onKapat}>Geri</button></div>;
  if (!sorular || !q) return <div className="sp-kart sp-bos"><p>Sorular yükleniyor…</p></div>;

  /* ---------------- sonuç ---------------- */
  if (bitti && sonuc) {
    const yanlisQ = sorular.filter((x) => cevap[x.ref] !== x.dogru);
    const zayif = zayifAsamalar(yanlisQ);
    const brans = deneme ? Object.entries(ix.sinav).map(([b, s]) => {
      const qs = sorular.filter((x) => spBrans(x.ref) === b);
      return { b, ad: s.ad, n: qs.length, d: qs.filter((x) => cevap[x.ref] === x.dogru).length };
    }).filter((x) => x.n) : [];
    return (
      <div className="sp-test" ref={ustRef}>
        <div className="sp-kart sp-sonuc">
          <p className="sp-ust">{baslik}</p>
          <div className="sp-puan">
            <b>{sonuc.d}</b><span>/ {sonuc.n} doğru</span>
            <em className={yuzde(sonuc.d, sonuc.n) >= 70 ? 'is-iyi' : yuzde(sonuc.d, sonuc.n) >= 50 ? 'is-orta' : 'is-zayif'}>%{yuzde(sonuc.d, sonuc.n)}</em>
          </div>
          {deneme && (
            <div className="sp-brans-tablo" role="table" aria-label="Branşlara göre sonuç">
              {brans.map((x) => (
                <div key={x.b} role="row" className="sp-brans-satir">
                  <span role="cell">{x.ad}</span>
                  <span role="cell" className="sp-mono">{x.d}/{x.n}</span>
                  <span role="cell" className="sp-bar" aria-hidden><i style={{ width: `${yuzde(x.d, x.n)}%` }} /></span>
                </div>
              ))}
            </div>
          )}
          {zayif.length > 0 ? (
            <div className="sp-zayif">
              <h3>Eksik kalan bölümler</h3>
              <p>Yanlış yaptığın soruların bilgisi bu aşamalarda anlatılıyor. Dinleyip tekrar çöz.</p>
              <ul>
                {zayif.slice(0, 12).map((z) => {
                  const b = spPartBul(ix, z.part);
                  const a = b?.part.asamalar.find((x) => x.no === z.no);
                  const yol = asamaYolu(ix, z.part, z.no);
                  if (!b || !a || !yol) return null;
                  return (
                    <li key={`${z.part}:${z.no}`}>
                      <button type="button" className="sp-zayif-btn" onClick={() => onGit(yol)}>
                        <span className="sp-nokta" style={{ background: `var(--sp-${b.ders.brans})` }} aria-hidden />
                        <span className="sp-zayif-t"><b>{BRANS_KISA[b.ders.brans]}{b.ders.partlar.length > 1 ? ` · Part ${b.part.no}` : ''} · Aşama {a.no}</b><small>{a.baslik}</small></span>
                        <span className="sp-mono">{z.n} yanlış</span>
                        <ChevronRight aria-hidden />
                      </button>
                    </li>
                  );
                })}
              </ul>
            </div>
          ) : <p className="sp-tebrik">Tüm sorular doğru. Bu bölüm tamam.</p>}
          <div className="sp-arac">
            <button type="button" className="sp-btn" onClick={yeniden}><RotateCcw aria-hidden /> Yeniden çöz</button>
            <button type="button" className="sp-btn sp-btn-ana" onClick={onKapat}>{devamEtiket || 'Tamam'} <ArrowRight aria-hidden /></button>
          </div>
        </div>
        <div className="sp-kart">
          <h3 className="sp-h3">Cevaplar ve açıklamalar</h3>
          <ol className="sp-inceleme">
            {sorular.map((x, k) => {
              const c = cevap[x.ref];
              return (
                <li key={x.ref} className={c === x.dogru ? 'is-dogru' : 'is-yanlis'}>
                  <p className="sp-kok"><span className="sp-mono">{k + 1}.</span> {x.soru}</p>
                  <p className="sp-cevap-ozet">
                    {c ? <>Senin cevabın <b>{c}</b> · </> : <>Boş · </>}Doğru cevap <b>{x.dogru}) {x.secenekler[x.dogru]}</b>
                  </p>
                  {c && c !== x.dogru && x.siklar[c] && <p className="sp-aciklama is-yanlis"><b>{c})</b> {x.siklar[c]}</p>}
                  <p className="sp-aciklama">{x.cozum || x.siklar[x.dogru]}</p>
                  <Kaynak q={x} ix={ix} onGit={onGit} />
                </li>
              );
            })}
          </ol>
        </div>
      </div>
    );
  }

  /* ---------------- soru ---------------- */
  const c = cevap[q.ref];
  const goster = !deneme && !!c;
  const cevapli = Object.keys(cevap).filter((r) => sorular.some((x) => x.ref === r)).length;
  return (
    <div className="sp-test" ref={ustRef}>
      <div className="sp-test-bas">
        <div className="sp-test-bas-t">
          <p className="sp-ust">{alt}</p>
          <h2>{baslik}</h2>
        </div>
        <div className="sp-arac">
          {deneme && sureDk ? (
            <span className={`sp-sure${kalanSn < 600 ? ' is-az' : ''}`} aria-live="off"><Clock aria-hidden />{Math.floor(kalanSn / 60)}:{String(kalanSn % 60).padStart(2, '0')}</span>
          ) : (
            <button type="button" className={`sp-btn${sesAcik ? ' is-on' : ''}`} onClick={sesDegis} aria-pressed={sesAcik} title="Sesli asistan">
              {sesAcik ? <Volume2 aria-hidden /> : <VolumeX aria-hidden />}<span>{caliyor ? 'Okuyor…' : 'Sesli asistan'}</span>
            </button>
          )}
          <button type="button" className="sp-btn" onClick={() => { dur(); onKapat(); }} aria-label="Kapat"><X aria-hidden /></button>
        </div>
      </div>
      <div className="sp-ilerleme" aria-hidden><i style={{ width: `${yuzde(cevapli, sorular.length)}%` }} /></div>

      <div className="sp-kart sp-soru">
        <SoruGovde q={q} i={i} n={sorular.length} />
        <ul className="sp-siklar" role="list">
          {harfler(q).map((h) => {
            const durum = goster ? (h === q.dogru ? 'is-dogru' : h === c ? 'is-yanlis' : 'is-soluk') : c === h ? 'is-secili' : '';
            return (
              <li key={h}>
                <button type="button" className={`sp-sik ${durum}`} onClick={() => sec(h)} disabled={goster} aria-pressed={c === h}>
                  <span className="sp-harf">{h}</span>
                  <span className="sp-sik-t">{q.secenekler[h]}</span>
                  {goster && h === q.dogru && <Check aria-label="doğru" />}
                  {goster && h === c && h !== q.dogru && <X aria-label="yanlış" />}
                </button>
                {goster && (h === c || h === q.dogru) && q.siklar[h] && (
                  <p className={`sp-aciklama ${h === q.dogru ? 'is-dogru' : 'is-yanlis'}`}>{q.siklar[h]}</p>
                )}
              </li>
            );
          })}
        </ul>
        {!deneme && !c && q.ipucu && (
          yardim[q.ref]
            ? <p className="sp-ipucu"><LifeBuoy aria-hidden /> {q.ipucu}</p>
            : <button type="button" className="sp-btn sp-btn-yardim" onClick={() => { setYardim((y) => ({ ...y, [q.ref]: true })); cal([spKlip(q.ref, q, 'i')]); }}><LifeBuoy aria-hidden /> Yardım al</button>
        )}
        {goster && (
          <div className={`sp-geri ${c === q.dogru ? 'is-dogru' : 'is-yanlis'}`}>
            <b>{c === q.dogru ? 'Doğru!' : `Doğru cevap ${q.dogru}`}</b>
            {q.cozum && <p>{q.cozum}</p>}
            <Kaynak q={q} ix={ix} onGit={onGit} />
          </div>
        )}
      </div>

      <div className="sp-test-alt">
        <button type="button" className="sp-btn" onClick={() => setI(i - 1)} disabled={i === 0}><ArrowLeft aria-hidden /> Önceki</button>
        {deneme && (
          <div className="sp-izgara" role="navigation" aria-label="Sorular">
            {sorular.map((x, k) => (
              <button key={x.ref} type="button" className={`${k === i ? 'is-on' : ''}${cevap[x.ref] ? ' is-dolu' : ''}`} onClick={() => setI(k)} aria-label={`Soru ${k + 1}`}>{k + 1}</button>
            ))}
          </div>
        )}
        {i < sorular.length - 1 ? (
          <button type="button" className="sp-btn sp-btn-ana" onClick={() => setI(i + 1)} disabled={!deneme && !c}>Sonraki <ArrowRight aria-hidden /></button>
        ) : (
          <button type="button" className="sp-btn sp-btn-ana" onClick={() => {
            if (deneme && cevapli < sorular.length && !window.confirm(`${sorular.length - cevapli} soru boş. Sınavı bitirmek istiyor musun?`)) return;
            bitir();
          }} disabled={!deneme && !c}>
            {deneme ? <><Flag aria-hidden /> Sınavı bitir</> : <><ListChecks aria-hidden /> Sonucu gör</>}
          </button>
        )}
      </div>
    </div>
  );
}
