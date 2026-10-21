/**
 * /son-prova — Son Prova: kurulun tüm dersleri için sınav öncesi son tekrar.
 *   /son-prova                         merkez: sınav dağılımı, dersler, ilerleme, 3 deneme
 *   /son-prova/<brans>                 ders: partlar (sesli özet), part check-up'ları, genel check-up
 *   /son-prova/<brans>/<part>          part: sesli özet (sesli ders altyapısı, kamp kipi) + aşama sonu soruları; ?asama=N
 *   /son-prova/<brans>/<part>/checkup  part check-up · /son-prova/<brans>/genel  genel check-up
 *   /son-prova/deneme/<n>              100 soruluk sınav provası
 * Part açılmadan önce cihaza indirilmesi şarttır (ses + kırpılmış özet PDF): internet gitse de kaldığı yerden sürer.
 * Kurul seçimi ?kurul=N (yoksa içeriği olan en yeni kurul). İçerik: spVeri.ts.
 */
import { icKonum, icUrl } from '../../siteHaritasi';
import React, { Suspense, lazy, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowLeft, BookOpenCheck, CheckCircle2, ChevronRight, CloudDownload, FileDown, Flag, Headphones, ListChecks, Loader2,
  PlayCircle, RotateCcw, Target, WifiOff,
} from 'lucide-react';
import { navigateTo } from '../../router';
import { getCustomApiUrl } from '../../services/api';
import { cdCevrimdisiIndir as cdIndir, useCdCevrimdisi } from '../canliDers/canliDersCevrimdisi';
import { kuyrugaEkle } from '../../services/cevrimdisi/paketMotoru';
import { cdDetayGetir, cdDuraklat, cdParagrafa, useCd } from '../canliDers/canliDersStore';
import { cdAktarBelgesi } from '../canliDers/canliDersDisaAktar';
import { MetinAktarMenu } from '../MetinAktarMenu';
import {
  BRANS_KISA, partIlerleme, spIndexYukle, spKurullar, spPartBul, useSpKayit, yuzde,
  type SpAsama, type SpDers, type SpIndex, type SpPart,
} from './spVeri';
import SpTest from './SpTest';
import '../../styles/genetik-kamp.css'; // kamp kipinin aşama çubuğu (.cd-k-cubuk) stilleri
import '../../styles/son-prova.css';

const CanliDersDers = lazy(() => import('../canliDers/CanliDersDers'));

type Yol =
  | { t: 'merkez' }
  | { t: 'ders'; brans: string }
  | { t: 'part'; brans: string; no: number; asama?: number }
  | { t: 'checkup'; brans: string; no: number }
  | { t: 'genel'; brans: string }
  | { t: 'deneme'; no: number };

function yolOku(): Yol {
  const p = icKonum().pathname.replace(/\/+$/, '').split('/').slice(2).map(decodeURIComponent);
  const sp = new URLSearchParams(icKonum().search);
  if (!p.length) return { t: 'merkez' };
  if (p[0] === 'deneme' && Number(p[1])) return { t: 'deneme', no: Number(p[1]) };
  if (p.length === 1) return { t: 'ders', brans: p[0] };
  if (p[1] === 'genel') return { t: 'genel', brans: p[0] };
  const no = Number(p[1]) || 1;
  if (p[2] === 'checkup') return { t: 'checkup', brans: p[0], no };
  return { t: 'part', brans: p[0], no, asama: Number(sp.get('asama')) || undefined };
}
const git = (yol: string) => { navigateTo(yol); window.scrollTo({ top: 0 }); };
/** Part indirme: sesli özet (ses + kırpılmış PDF) + partın soru verisi ve soru sesleri (çevrimdışı paket) */
async function cdCevrimdisiIndir(key: string): Promise<void> {
  // önce sesli özet (kapı bunu bekler), sonra soru paketi — bağımlı sesli paket artık cihazda olduğundan ikinci kez inmez
  await cdIndir(key);
  try { kuyrugaEkle([`sonprova:${key}`], true); } catch { /* katalog yok: sorular derlemeyle gelir, sesleri çevrimiçi çalar */ }
}
const pdfAdres = (key: string) => `${getCustomApiUrl() || ''}/api/lecture-pdf/deck/${encodeURIComponent(`k1p-${key}`)}/0`;
const dk = (n: number) => (n >= 60 ? `${Math.floor(n / 60)} sa ${n % 60 ? `${n % 60} dk` : ''}`.trim() : `${n} dk`);

function Geri({ yol, metin }: { yol: string; metin: string }) {
  return (
    <a className="sp-geri-bag" href={yol} onClick={(e) => { if (e.button || e.metaKey || e.ctrlKey) return; e.preventDefault(); git(yol); }}>
      <ArrowLeft aria-hidden /> <span>{metin}</span>
    </a>
  );
}

export default function SonProvaView() {
  const [yol, setYol] = useState<Yol>(yolOku);
  useEffect(() => {
    const f = () => setYol(yolOku());
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  const kurullar = spKurullar();
  const kurul = Number(new URLSearchParams(icKonum().search).get('kurul')) || kurullar[kurullar.length - 1] || 1;
  const [ix, setIx] = useState<SpIndex | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  useEffect(() => { spIndexYukle(kurul).then(setIx).catch((e) => setHata(String(e?.message || e))); }, [kurul]);
  useEffect(() => { document.title = 'Son Prova · MeDSor'; }, [yol]);

  if (hata) return <div className="sp"><div className="sp-kart sp-bos"><p>{hata}</p></div></div>;
  if (!ix) return <div className="sp"><div className="sp-kart sp-bos"><Loader2 className="sp-don" aria-hidden /> <p>Yükleniyor…</p></div></div>;
  const ders = 'brans' in yol ? ix.dersler.find((d) => d.brans === yol.brans) : undefined;

  if (yol.t === 'merkez') return <Merkez ix={ix} />;
  if (yol.t === 'deneme') {
    const d = ix.denemeler.find((x) => x.no === yol.no);
    if (!d) return <Bulunamadi />;
    return (
      <div className="sp sp-dar">
        <Geri yol="/son-prova" metin="Son Prova" />
        <SpTest key={`d${d.no}`} ix={ix} kip="deneme" refs={d.sorular} anahtar={`k${ix.kurul}:${d.no}`} sureDk={d.sure}
          baslik={`Deneme ${d.no} · ${d.sorular.length} soru`} alt={`Kurul ${ix.kurul} sınav provası · ${d.sure} dakika`}
          onKapat={() => git('/son-prova')} onGit={git} devamEtiket="Son Prova'ya dön" />
      </div>
    );
  }
  if (!ders) return <Bulunamadi />;
  if (yol.t === 'ders') return <DersSayfa ix={ix} ders={ders} />;
  if (yol.t === 'genel') {
    return (
      <div className="sp sp-dar">
        <Geri yol={`/son-prova/${ders.brans}`} metin={ders.ad} />
        <SpTest key={`g${ders.brans}`} ix={ix} kip="genel" refs={ders.genel} anahtar={`k${ix.kurul}:${ders.brans}`}
          baslik={`${ders.ad} · Genel check-up`} alt={`${ders.genel.length} soru · tüm konular`}
          onKapat={() => git(`/son-prova/${ders.brans}`)} onGit={git} devamEtiket="Derse dön" />
      </div>
    );
  }
  const part = ders.partlar.find((p) => p.no === yol.no);
  if (!part) return <Bulunamadi />;
  if (yol.t === 'checkup') {
    const refs = part.asamalar.flatMap((a) => a.checkup);
    return (
      <div className="sp sp-dar">
        <Geri yol={`/son-prova/${ders.brans}`} metin={ders.ad} />
        <SpTest key={`c${part.key}`} ix={ix} kip="checkup" refs={refs} anahtar={part.key}
          baslik={`${ders.ad}${ders.partlar.length > 1 ? ` · Part ${part.no}` : ''} · Check-up`} alt={`${refs.length} soru · partın tüm aşamaları`}
          onKapat={() => git(`/son-prova/${ders.brans}`)} onGit={git} devamEtiket="Derse dön" />
      </div>
    );
  }
  return <PartSayfa key={part.key} ix={ix} ders={ders} part={part} asama={yol.asama} />;
}

function Bulunamadi() {
  return <div className="sp"><Geri yol="/son-prova" metin="Son Prova" /><div className="sp-kart sp-bos"><p>Bu sayfa bulunamadı.</p></div></div>;
}

/* ---------------- merkez ---------------- */
function Merkez({ ix }: { ix: SpIndex }) {
  const k = useSpKayit();
  const toplam = Object.values(ix.sinav).reduce((a, s) => a + s.soru, 0);
  const tumAsama = ix.dersler.flatMap((d) => d.partlar.flatMap((p) => p.asamalar.map((a) => `${p.key}:${a.no}`)));
  const biten = tumAsama.filter((a) => k.asama[a]).length;
  const sure = ix.dersler.reduce((a, d) => a + d.partlar.reduce((b, p) => b + p.tahminiDk, 0), 0);
  return (
    <div className="sp">
      <header className="sp-bas">
        <span className="sp-ic"><Flag aria-hidden /></span>
        <div className="sp-bas-t">
          <p className="sp-ust">Kurul {ix.kurul} · {toplam} soruluk sınav</p>
          <h1>Son Prova</h1>
          <p>Her dersin sınavda sorulan ve sorulmaya en müsait bilgileri, ders slaytlarıyla birlikte sesli özet olarak. Her aşamanın sonunda
            soru, her partın sonunda check-up, en sonda 100 soruluk üç deneme. Yanlışların seni eksik bölüme götürür.</p>
        </div>
      </header>

      <section className="sp-kart sp-ozet" aria-label="Genel ilerleme">
        <div className="sp-ozet-say"><b>{yuzde(biten, tumAsama.length)}%</b><span>{biten}/{tumAsama.length} aşama</span></div>
        <div className="sp-ozet-say"><b>{dk(sure)}</b><span>toplam sesli özet (1×)</span></div>
        <div className="sp-ozet-say"><b>{ix.dersler.reduce((a, d) => a + d.partlar.length, 0)}</b><span>part · {ix.dersler.length} ders</span></div>
      </section>

      <section aria-labelledby="sp-dag">
        <h2 id="sp-dag" className="sp-h2">Sınav dağılımı ve dersler</h2>
        <div className="sp-dersler">
          {ix.dersler.map((d) => <DersKart key={d.brans} ix={ix} d={d} toplam={toplam} />)}
        </div>
      </section>

      <section aria-labelledby="sp-den">
        <h2 id="sp-den" className="sp-h2">Sınav provaları</h2>
        <p className="sp-not">Gerçek sınavın dağılımıyla ({Object.values(ix.sinav).map((s) => `${s.ad} ${s.soru}`).join(', ')}); kolay–orta zorlukta, çıkmışların üslubunda. Üç deneme birbirinden ve aşama sorularından farklıdır.</p>
        <div className="sp-denemeler">
          {ix.denemeler.map((d) => {
            const s = k.deneme[`k${ix.kurul}:${d.no}`];
            return (
              <button key={d.no} type="button" className="sp-kart sp-deneme-kart" onClick={() => git(`/son-prova/deneme/${d.no}`)}>
                <span className="sp-ic is-kucuk"><Target aria-hidden /></span>
                <span className="sp-deneme-t"><b>Deneme {d.no}</b><small>{d.sorular.length} soru · {d.sure} dakika</small></span>
                {s?.sonuc ? <span className="sp-rozet is-iyi">{s.sonuc.d}/{s.sonuc.n}</span>
                  : s ? <span className="sp-rozet">Devam et</span> : <ChevronRight aria-hidden />}
              </button>
            );
          })}
        </div>
      </section>
    </div>
  );
}

function DersKart({ ix, d, toplam }: { ix: SpIndex; d: SpDers; toplam: number }) {
  const k = useSpKayit();
  const asama = d.partlar.flatMap((p) => p.asamalar.map((a) => `${p.key}:${a.no}`));
  const biten = asama.filter((a) => k.asama[a]).length;
  const g = k.genel[`k${ix.kurul}:${d.brans}`];
  return (
    <button type="button" className="sp-kart sp-ders-kart" style={{ '--sp-c': `var(--sp-${d.brans})` } as React.CSSProperties} onClick={() => git(`/son-prova/${d.brans}`)}>
      <span className="sp-ders-ust">
        <b>{d.ad}</b>
        <span className="sp-soru-say" title="Sınavdaki soru sayısı">{d.soru} soru</span>
      </span>
      <span className="sp-bar" aria-hidden><i style={{ width: `${(100 * d.soru) / toplam}%` }} /></span>
      <span className="sp-ders-alt">
        <span>{d.partlar.length} part · {dk(d.partlar.reduce((a, p) => a + p.tahminiDk, 0))}</span>
        <span>{biten}/{asama.length} aşama{g ? ` · genel %${yuzde(g.d, g.n)}` : ''}</span>
      </span>
    </button>
  );
}

/* ---------------- ders ---------------- */
function DersSayfa({ ix, ders }: { ix: SpIndex; ders: SpDers }) {
  const k = useSpKayit();
  const g = k.genel[`k${ix.kurul}:${ders.brans}`];
  return (
    <div className="sp" style={{ '--sp-c': `var(--sp-${ders.brans})` } as React.CSSProperties}>
      <Geri yol="/son-prova" metin="Son Prova" />
      <header className="sp-bas">
        <span className="sp-ic"><BookOpenCheck aria-hidden /></span>
        <div className="sp-bas-t">
          <p className="sp-ust">Kurul {ix.kurul} · sınavda {ders.soru} soru</p>
          <h1>{ders.ad}</h1>
          <p>Partları sırayla dinle; her aşamanın sonundaki soruları çöz, partın sonunda check-up'ı yap. Hepsi bitince genel check-up seni eksik kalan bölüme yönlendirir.</p>
        </div>
      </header>
      {ders.partlar.map((p) => <PartKart key={p.key} ix={ix} ders={ders} p={p} />)}
      <section className="sp-kart sp-genel">
        <div>
          <h2 className="sp-h3">Genel check-up</h2>
          <p className="sp-not">{ders.genel.length} soru, dersin bütün aşamalarından. Yanlışlarına göre hangi bölüme dönmen gerektiğini gösterir.</p>
        </div>
        <button type="button" className="sp-btn sp-btn-ana" onClick={() => git(`/son-prova/${ders.brans}/genel`)}>
          {g ? <><RotateCcw aria-hidden /> Yeniden çöz · %{yuzde(g.d, g.n)}</> : <><ListChecks aria-hidden /> Başla</>}
        </button>
      </section>
    </div>
  );
}

function PartKart({ ix, ders, p }: { ix: SpIndex; ders: SpDers; p: SpPart }) {
  const k = useSpKayit();
  const il = partIlerleme(k, p);
  const { kayit, is } = useCdCevrimdisi(p.key);
  const indirildi = !!kayit && kayit.pdfler.length > 0;
  return (
    <section className="sp-kart sp-part">
      <div className="sp-part-bas">
        <div>
          <p className="sp-ust">{ders.partlar.length > 1 ? `Part ${p.no} · ` : ''}{dk(p.tahminiDk)} · {p.asamalar.length} aşama · {p.sayfa} slayt</p>
          <h2 className="sp-h3">{p.baslik}</h2>
        </div>
        <span className="sp-mono">{il.biten}/{il.toplam}</span>
      </div>
      <ol className="sp-asama-liste">
        {p.asamalar.map((a) => {
          const s = k.asama[`${p.key}:${a.no}`];
          return (
            <li key={a.no}>
              <button type="button" onClick={() => git(`/son-prova/${ders.brans}/${p.no}?asama=${a.no}`)}>
                {s ? <CheckCircle2 className="is-tamam" aria-label="tamam" /> : <span className="sp-asama-no">{a.no}</span>}
                <span className="sp-asama-t"><b>{a.baslik}</b><small>{a.dersNo}) {a.dersAd}</small></span>
                {s && <span className="sp-mono">{s.d}/{s.n}</span>}
              </button>
            </li>
          );
        })}
      </ol>
      <div className="sp-arac">
        <button type="button" className="sp-btn sp-btn-ana" onClick={() => git(`/son-prova/${ders.brans}/${p.no}`)}>
          <PlayCircle aria-hidden /> {il.biten ? 'Devam et' : 'Başla'}
        </button>
        <button type="button" className="sp-btn" onClick={() => git(`/son-prova/${ders.brans}/${p.no}/checkup`)}>
          <ListChecks aria-hidden /> Check-up{il.checkup ? ` · %${yuzde(il.checkup.d, il.checkup.n)}` : ''}
        </button>
        {!indirildi && (
          <button type="button" className="sp-btn" disabled={!!is && !is.hata} onClick={() => cdCevrimdisiIndir(p.key).catch(() => {})}>
            <CloudDownload aria-hidden /> {is && !is.hata ? `İniyor %${Math.round(is.oran * 100)}` : 'Cihaza indir'}
          </button>
        )}
        <OzetIndir partKey={p.key} />
      </div>
    </section>
  );
}

/** Özet metni (.pdf/.docx/.md/.txt) ve kırpılmış slayt PDF'i indirme */
function OzetIndir({ partKey }: { partKey: string }) {
  return (
    <>
      <MetinAktarMenu etiket="Özeti indir" belge={async () => {
        const d = await cdDetayGetir(partKey);
        return cdAktarBelgesi(d, 'Son Prova', true);
      }} dosyaAdi={`Son Prova - ${partKey}`} dugmeSinif="sp-btn" />
      <a className="sp-btn" href={`${pdfAdres(partKey)}`} download target="_blank" rel="noopener"><FileDown aria-hidden /> Slayt PDF'i</a>
    </>
  );
}

/* ---------------- part (sesli özet + aşama soruları) ---------------- */
function PartSayfa({ ix, ders, part, asama }: { ix: SpIndex; ders: SpDers; part: SpPart; asama?: number }) {
  const { kayit, is } = useCdCevrimdisi(part.key);
  const indirildi = !!kayit && kayit.pdfler.length > 0;
  const [cevrimici, setCevrimici] = useState(typeof navigator === 'undefined' ? true : navigator.onLine);
  useEffect(() => {
    const a = () => setCevrimici(true), b = () => setCevrimici(false);
    window.addEventListener('online', a); window.addEventListener('offline', b);
    return () => { window.removeEventListener('online', a); window.removeEventListener('offline', b); };
  }, []);
  const ustYol = `/son-prova/${ders.brans}`;
  const gez = (
    <nav className="sp-part-gez" aria-label="Son Prova">
      <Geri yol={ustYol} metin={ders.ad} />
      <b className="sp-part-ad">{ders.partlar.length > 1 ? `Part ${part.no} · ` : ''}{part.baslik}</b>
    </nav>
  );

  if (!indirildi) {
    return (
      <div className="sp sp-dar">
        {gez}
        <section className="sp-kart sp-kapi">
          <span className="sp-ic"><CloudDownload aria-hidden /></span>
          <h2 className="sp-h3">Önce bu partı cihazına indir</h2>
          <p>Son Prova partları kesintisiz çalışsın diye ses ve özet slayt PDF'i ({part.sayfa} sayfa) önce cihaza iner. İndirdikten sonra
            internet gitse de, ekrandan çıkıp dönsen de kaldığın yerden hiç beklemeden devam edersin.</p>
          {is?.hata && <p className="sp-hata">{is.hata}</p>}
          {!cevrimici && <p className="sp-hata"><WifiOff aria-hidden /> İnternet yok. İndirmek için bağlan.</p>}
          <button type="button" className="sp-btn sp-btn-ana" disabled={(!!is && !is.hata) || !cevrimici} onClick={() => cdCevrimdisiIndir(part.key).catch(() => {})}>
            {is && !is.hata ? <><Loader2 className="sp-don" aria-hidden /> İniyor %{Math.round(is.oran * 100)}</> : <><CloudDownload aria-hidden /> İndir ve başla</>}
          </button>
          {is && !is.hata && <div className="sp-ilerleme" aria-hidden><i style={{ width: `${Math.round(is.oran * 100)}%` }} /></div>}
        </section>
      </div>
    );
  }
  return <PartOynatici ix={ix} ders={ders} part={part} asama={asama} gez={gez} />;
}

function PartOynatici({ ix, ders, part, asama, gez }: { ix: SpIndex; ders: SpDers; part: SpPart; asama?: number; gez: React.ReactNode }) {
  const k = useSpKayit();
  const key = part.key;
  const aktif = useCd((s) => (s.key === key ? s.aktif : -1));
  const caliyor = useCd((s) => s.key === key && s.playing);
  const sonda = useCd((s) => s.key === key && !s.playing && s.dur > 0 && s.t >= s.dur - 1.5);
  const hazir = useCd((s) => s.key === key && s.dur > 0 && !!s.detay);
  const [test, setTest] = useState<SpAsama | null>(null);
  const [checkupSor, setCheckupSor] = useState(false);
  const atlanan = useRef(new Set<number>());

  // ?asama=N: ses yüklenince o aşamanın başına git (oynatmadan)
  const gidildi = useRef(false);
  useEffect(() => {
    if (!hazir || gidildi.current || !asama) return;
    const a = part.asamalar.find((x) => x.no === asama);
    if (a) cdParagrafa(a.p[0], false);
    gidildi.current = true;
  }, [hazir, asama, part]);

  // Aşama sınırı: ses bir sonraki aşamaya geçtiği anda (oynarken) durur ve biten aşamanın soruları açılır.
  // Aşama sırası paragraf aralığından bulunur; geçiş bir aşama ileri olmalı (elle ileri atlamada soru sorulmaz).
  const asamaSira = (i: number) => part.asamalar.findIndex((a) => i >= a.p[0] && i <= a.p[1]);
  const oncekiSira = useRef(-1);
  useEffect(() => {
    const yeni = aktif >= 0 ? asamaSira(aktif) : -1;
    const eski = oncekiSira.current;
    oncekiSira.current = yeni;
    if (!caliyor || eski < 0 || yeni !== eski + 1) return;
    const biten = part.asamalar[eski];
    if (k.asama[`${key}:${biten.no}`] || atlanan.current.has(biten.no)) return;
    cdDuraklat();
    cdParagrafa(part.asamalar[yeni].p[0], false);
    setTest(biten);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [aktif, caliyor]);

  // Ses bitince: son aşamanın soruları, sonra check-up önerisi
  useEffect(() => {
    if (!sonda) return;
    const son = part.asamalar[part.asamalar.length - 1];
    if (!k.asama[`${key}:${son.no}`] && !atlanan.current.has(son.no)) setTest(son);
    else if (!k.checkup[key]) setCheckupSor(true);
  }, [sonda, part, key, k.asama, k.checkup]);

  const kapat = useCallback((devam: boolean) => {
    const a = test;
    setTest(null);
    if (!a) return;
    atlanan.current.add(a.no);
    const son = part.asamalar[part.asamalar.length - 1];
    if (a.no === son.no) { if (!k.checkup[key]) setCheckupSor(true); return; }
    if (devam) {
      const sonraki = part.asamalar.find((x) => x.no === a.no + 1);
      if (sonraki) cdParagrafa(sonraki.p[0], true);
    }
  }, [test, part, key, k.checkup]);

  const suAn = part.asamalar.find((a) => aktif >= a.p[0] && aktif <= a.p[1]);

  const soruAsama = suAn || part.asamalar[0];
  const soruDurum = k.asama[`${key}:${soruAsama.no}`];
  const ust = (
    <nav className="sp-ust-gez" aria-label="Son Prova">
      <Geri yol={`/son-prova/${ders.brans}`} metin={BRANS_KISA[ders.brans]} />
      <button type="button" className={`sp-btn sp-btn-kucuk${soruDurum ? ' is-tamam' : ''}`} onClick={() => { cdDuraklat(); setTest(soruAsama); }}
        title={`Aşama ${soruAsama.no} · ${soruAsama.baslik} — ${soruAsama.dersNo}) ${soruAsama.dersAd}`}>
        {soruDurum ? <CheckCircle2 aria-hidden /> : <ListChecks aria-hidden />}
        <span>Aşama {soruAsama.no} soruları{soruDurum ? ` · ${soruDurum.d}/${soruDurum.n}` : ''}</span>
      </button>
      <button type="button" className={`sp-btn sp-btn-kucuk${k.checkup[key] ? ' is-tamam' : ''}`} onClick={() => git(`/son-prova/${ders.brans}/${part.no}/checkup`)}>
        <Target aria-hidden /><span>Check-up</span>
      </button>
    </nav>
  );

  return (
    <div className="sp-part-sayfa">
      {/* Soru ya da check-up önerisi açıkken ders (metin + PDF) gizlenir; bileşen yerinde kalır, ses ve konum korunur */}
      <div className={test || checkupSor ? 'sp-gizli' : 'sp-ders-alan'}>
        <Suspense fallback={<div className="sp-kart sp-bos"><Loader2 className="sp-don" aria-hidden /></div>}>
          <CanliDersDers dersKey={key} kamp={{ geri: ust }} />
        </Suspense>
      </div>

      {test && (
        <section className="sp-sayfa-ici" aria-label={`Aşama ${test.no} soruları`}>
          <div className="sp-sayfa-ici-ic">
            <SpTest key={`${key}:${test.no}`} ix={ix} kip="asama" refs={test.sorular} anahtar={`${key}:${test.no}`}
              baslik={`Aşama ${test.no} soruları`} alt={`${test.baslik} · ${test.dersNo}) ${test.dersAd}`}
              onKapat={() => kapat(true)} onGit={(y) => { setTest(null); git(y); }}
              devamEtiket={test.no === part.asamalar[part.asamalar.length - 1].no ? 'Partı bitir' : 'Derse devam'} />
            <button type="button" className="sp-btn sp-katman-atla" onClick={() => kapat(false)}>Şimdi değil, derse dön</button>
          </div>
        </section>
      )}
      {checkupSor && (
        <section className="sp-sayfa-ici" aria-label="Part tamamlandı">
          <div className="sp-sayfa-ici-ic sp-kart sp-kapi">
            <span className="sp-ic"><CheckCircle2 aria-hidden /></span>
            <h2 className="sp-h3">Part bitti</h2>
            <p>Şimdi partın check-up testiyle ({part.asamalar.reduce((n, a) => n + a.checkup.length, 0)} soru) eksiklerini gör.</p>
            <div className="sp-arac">
              <button type="button" className="sp-btn" onClick={() => setCheckupSor(false)}>Sonra</button>
              <button type="button" className="sp-btn sp-btn-ana" onClick={() => git(`/son-prova/${ders.brans}/${part.no}/checkup`)}><ListChecks aria-hidden /> Check-up'a başla</button>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
