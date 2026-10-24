/**
 * /kmb — KMB görsel sesli asistan (görünen /kamplar/kmb[/<beceri>[/ogren|sinav]], siteHaritasi).
 * Önce öğretir (adım adım sahne + EMA sesi, cümle cümle görsel eylem), sonra sınava sokar (OSCE sıralama,
 * vaka senaryoları, sahnede bul). İçerik src/data/kmb/<kod>.json, ses zamanlaması src/data/kmb/ses_<kod>.json,
 * klipler /api/cozucu-ses/kmb/ema/<kod>/<klip>.mp3. Ayrıntı: docs/KMB_GORSEL_ASISTAN.md
 */
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { getCustomApiUrl } from '../../services/api';
import { navigateTo } from '../../router';
import { icKonum } from '../../siteHaritasi';
import { SAHNELER, SahneCiz, type SahneDurum } from './sahneler';
import { uygula, type Eylem } from './eylem';
import LottieVideo, { KMB_DURDUR, LOTTILER } from './LottieVideo';
import DersVideo from './DersVideo';
import INDEX from '../../data/kmb/index.json';
import '../../styles/kmb.css';

export type Adim = { id: string; baslik: string; sahne: string; ek?: string[]; cumleler: { metin: string; eylem?: Eylem[] }[]; puf?: string[]; dikkat?: string[] };
type Senaryo = { id: string; baslik: string; sahne: string; eylem?: Eylem[]; soru: string; secenekler: { metin: string; dogru: boolean; aciklama: string }[]; puf?: string };
/** Dallanan OSCE akışı: dal yalnız listenin son basamağında; her yol kendi basamak listesini taşır (iç içe dal olabilir) */
type Basamak = { id: string; metin: string; aciklama: string; dal?: { soru: string; yollar: { id: string; etiket: string; basamaklar: Basamak[] }[] } };
type Akis = { id: string; ad: string; yonerge: string; basamaklar: Basamak[] };
type Bul = { id: string; sahne: string; yonerge: string; hedef: string; aciklama: string };
type HedefKart = { no: number; sahne: string; eylem?: Eylem[]; lottie?: string; ne: string; nasil: string[]; neden: string; hata: string; hoca: string; dogrulanacak?: string };
export type Ders = {
  kod: string; slug: string; ad: string; belgeKodu: string; amac: string;
  hedefler: { no: number; metin: string; adimlar: string[] }[];
  hedefCalisma?: HedefKart[];
  adimlar: Adim[];
  sinav: { akislar: Akis[]; senaryolar: Senaryo[]; bul: Bul[] };
};
export type SesKayit = Record<string, { h: string; sure: number; zaman: [number, number][] }>;

const DERSLER = import.meta.glob('../../data/kmb/[0-9][0-9].json');
const SESLER = import.meta.glob('../../data/kmb/ses_*.json');

const sesUrl = (kod: string, klip: string, h: string) => `${getCustomApiUrl() || ''}/api/cozucu-ses/kmb/ema/${kod}/${klip}.mp3?v=${h}`;

function useYol() {
  const oku = () => {
    const sp = new URLSearchParams(icKonum().search);
    return { beceri: sp.get('beceri') || '', b: sp.get('b') || 'ogren' };
  };
  const [yol, setYol] = useState(oku);
  useEffect(() => {
    const f = () => setYol(oku());
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  const git = useCallback((beceri: string, b = 'ogren') => {
    const sp = new URLSearchParams();
    if (beceri) sp.set('beceri', beceri);
    if (beceri && b !== 'ogren') sp.set('b', b);
    navigateTo(`/kmb${sp.toString() ? `?${sp}` : ''}`);
  }, []);
  return { ...yol, git };
}

/** Tek klip çalar; ses yoksa cümle uzunluğuna göre süreli ilerler (sessiz kip) */
function useOynatici(kod: string, ses: SesKayit | null) {
  const audio = useRef<HTMLAudioElement | null>(null);
  const zamanlayici = useRef<number | null>(null);
  const [aktif, setAktif] = useState(-1);
  const [caliyor, setCaliyor] = useState(false);
  const durdur = useCallback(() => {
    audio.current?.pause();
    if (zamanlayici.current) window.clearInterval(zamanlayici.current);
    zamanlayici.current = null;
    setCaliyor(false);
  }, []);
  useEffect(() => {
    const f = (e: Event) => { if ((e as CustomEvent).detail !== 'adim') durdur(); };
    window.addEventListener(KMB_DURDUR, f);
    return () => window.removeEventListener(KMB_DURDUR, f);
  }, [durdur]);
  const oynat = useCallback((klip: string, cumleler: string[], bitince?: () => void, basla = 0) => {
    durdur();
    window.dispatchEvent(new CustomEvent(KMB_DURDUR, { detail: 'adim' }));
    const k = ses?.[klip];
    setCaliyor(true);
    if (k) {
      const a = audio.current || (audio.current = new Audio());
      a.src = sesUrl(kod, klip, k.h);
      a.currentTime = basla > 0 ? (k.zaman[basla]?.[0] ?? 0) : 0;
      setAktif(basla);
      a.ontimeupdate = () => {
        const t = a.currentTime;
        let i = 0;
        k.zaman.forEach(([b], j) => { if (t >= b - 0.05) i = j; });
        setAktif(i);
      };
      a.onended = () => { setCaliyor(false); bitince?.(); };
      a.play().catch(() => setCaliyor(false));
      return;
    }
    // sessiz kip: ~14 karakter/sn okuma
    let i = basla, kalan = cumleler[basla]?.length / 14 || 1;
    setAktif(i);
    zamanlayici.current = window.setInterval(() => {
      kalan -= 0.1;
      if (kalan > 0) return;
      i += 1;
      if (i >= cumleler.length) { durdur(); bitince?.(); return; }
      setAktif(i);
      kalan = cumleler[i].length / 14;
    }, 100);
  }, [kod, ses, durdur]);
  useEffect(() => durdur, [durdur]);
  return { aktif, setAktif, caliyor, oynat, durdur };
}

// ———————————————————————————————— Öğret

function Ogret({ ders, ses }: { ders: Ders; ses: SesKayit | null }) {
  const [ai, setAi] = useState(0);
  const [otomatik, setOtomatik] = useState(true);
  const [video, setVideo] = useState(false);
  const adim = ders.adimlar[ai];
  const cumleler = adim.cumleler.map((c) => c.metin);
  const { aktif, setAktif, caliyor, oynat, durdur } = useOynatici(ders.kod, ses);
  const durum = useMemo(() => {
    let d: SahneDurum = {};
    adim.cumleler.slice(0, Math.max(0, aktif) + 1).forEach((c) => { d = uygula(d, c.eylem); });
    return d;
  }, [adim, aktif]);

  const sonraki = useCallback(() => setAi((i) => Math.min(i + 1, ders.adimlar.length - 1)), [ders.adimlar.length]);
  const baslat = useCallback((bas = 0) => oynat(`o-${adim.id}`, cumleler, () => { if (otomatik && ai < ders.adimlar.length - 1) window.setTimeout(sonraki, 900); }, bas),
    [adim.id, cumleler, oynat, otomatik, ai, ders.adimlar.length, sonraki]);
  const ilk = useRef(true);
  useEffect(() => {
    if (ilk.current) { ilk.current = false; setAktif(-1); return; }
    baslat(0);
    // adım değişince yeni klip
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ai]);

  return (
    <div className="kmb-ogret">
      <aside className="kmb-adimlar" aria-label="Adımlar">
        {ders.adimlar.map((a, i) => (
          <button key={a.id} className={`kmb-adim-dugme${i === ai ? ' etkin' : ''}${i < ai ? ' gecti' : ''}`} onClick={() => setAi(i)}>
            <span className="no">{i + 1}</span><span>{a.baslik}</span>
          </button>
        ))}
      </aside>
      <section className="kmb-sahne-alan">
        <div className="kmb-sahne-kap"><SahneCiz sahne={adim.sahne} durum={durum} /></div>
        {LOTTILER.some((x) => x.adim === adim.id) && (
          <div className="kmb-videolar"><LottieVideo key={adim.id} ad={`adim-${adim.id}`} kod={ders.kod} ses={ses} kompakt /></div>
        )}
        {!!adim.ek?.some((e) => e.startsWith('lottie:')) && (
          <div className="kmb-videolar">
            {adim.ek.filter((e) => e.startsWith('lottie:')).map((e) => <LottieVideo key={e} ad={e.slice(7)} kod={ders.kod} ses={ses} kompakt />)}
          </div>
        )}
        {!!adim.ek?.some((e) => !e.startsWith('lottie:')) && (
          <div className="kmb-ekler">
            {adim.ek.filter((e) => !e.startsWith('lottie:')).map((e) => (
              <figure key={e} className="kmb-ek">
                <div className="kmb-sahne-kap"><SahneCiz sahne={e} durum={durum} /></div>
                <figcaption>{SAHNELER[e]?.ad}</figcaption>
              </figure>
            ))}
          </div>
        )}
        <div className="kmb-denetim">
          <button onClick={() => setAi((i) => Math.max(0, i - 1))} disabled={ai === 0}>‹ Önceki</button>
          {caliyor
            ? <button className="ana" onClick={durdur}>❚❚ Durdur</button>
            : <button className="ana" onClick={() => baslat(aktif > 0 && aktif < cumleler.length - 1 ? aktif : 0)}>▶ {aktif >= 0 ? 'Sürdür' : 'Anlat'}</button>}
          <button onClick={sonraki} disabled={ai === ders.adimlar.length - 1}>Sonraki ›</button>
          <label className="kmb-oto"><input type="checkbox" checked={otomatik} onChange={(e) => setOtomatik(e.target.checked)} /> Otomatik ilerle</label>
          <button onClick={() => { durdur(); setVideo(true); }}>🎬 Ders videosu</button>
          <span className="kmb-sayac">{ai + 1} / {ders.adimlar.length}</span>
        </div>
        {video && <DersVideo ders={ders} ses={ses} bas={ai} onKapat={() => setVideo(false)} />}
      </section>
      <section className="kmb-anlatim">
        <h2>{adim.baslik}</h2>
        <ol className="kmb-cumleler">
          {adim.cumleler.map((c, i) => (
            <li key={i} className={i === aktif ? 'aktif' : i < aktif ? 'okundu' : ''}>
              <button onClick={() => baslat(i)}>{c.metin}</button>
            </li>
          ))}
        </ol>
        {!!adim.puf?.length && <div className="kmb-kutu puf"><b>Püf noktası</b>{adim.puf.map((p) => <p key={p}>{p}</p>)}</div>}
        {!!adim.dikkat?.length && <div className="kmb-kutu dikkat"><b>Dikkat</b>{adim.dikkat.map((p) => <p key={p}>{p}</p>)}</div>}
        {ai === ders.adimlar.length - 1 && <p className="kmb-son">Bu beceriyi bitirdin. Sınav sekmesinde OSCE sıralaması, vakalar ve sahnede bul görevleri seni bekliyor.</p>}
      </section>
    </div>
  );
}

// ———————————————————————————————— Sınav

function karistir<T>(a: T[], tohum: number): T[] {
  const r = [...a];
  let s = tohum;
  for (let i = r.length - 1; i > 0; i--) { s = (s * 9301 + 49297) % 233280; const j = Math.floor((s / 233280) * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; }
  return r;
}

type Yol = { ad: string; basamaklar: Basamak[]; kararlar: { sonra: number; soru: string; etiket: string }[] };

/** Ağacı uçtan uca yollara aç: her yol düz basamak listesi + hangi basamaktan sonra hangi kararın geldiği */
function yollar(L: Basamak[], on: Yol = { ad: '', basamaklar: [], kararlar: [] }): Yol[] {
  const tum = { ...on, basamaklar: [...on.basamaklar, ...L] };
  const son = L[L.length - 1];
  if (!son?.dal) return [tum];
  return son.dal.yollar.flatMap((y) => yollar(y.basamaklar, {
    ad: on.ad ? `${on.ad} → ${y.etiket}` : y.etiket,
    basamaklar: tum.basamaklar,
    kararlar: [...tum.kararlar, { sonra: tum.basamaklar.length, soru: son.dal!.soru, etiket: y.etiket }],
  }));
}

function Ayrinti({ b, ak, oyna, acik }: { b: Basamak; ak: string; oyna: (klip: string, m: string[]) => void; acik?: boolean }) {
  return (
    <details className="kmb-ayrinti" open={acik}>
      <summary>Ayrıntılı açıklama</summary>
      <p>{b.aciklama}</p>
      <button className="kmb-dinle" onClick={() => oyna(`a-${ak}-${b.id}`, [b.metin, b.aciklama])}>▶ Dinle</button>
    </details>
  );
}

/** Akış haritası: dallar yan yana sütun, her basamak numaralı ve açılır */
function Harita({ L, ak, oyna, bas = 1 }: { L: Basamak[]; ak: string; oyna: (k: string, m: string[]) => void; bas?: number }) {
  return (
    <ol className="kmb-harita" start={bas}>
      {L.map((b, i) => (
        <li key={b.id}>
          <div className="kmb-dugum"><span className="no">{bas + i}</span><div><b>{b.metin}</b><Ayrinti b={b} ak={ak} oyna={oyna} /></div></div>
          {b.dal && (
            <div className="kmb-dal">
              <div className="kmb-karar">◆ {b.dal.soru}</div>
              <div className="kmb-dal-yollar">
                {b.dal.yollar.map((y) => (
                  <div key={y.id} className="kmb-dal-yol">
                    <div className="kmb-dal-etiket">{y.etiket}</div>
                    <Harita L={y.basamaklar} ak={ak} oyna={oyna} bas={bas + L.length} />
                  </div>
                ))}
              </div>
            </div>
          )}
        </li>
      ))}
    </ol>
  );
}

function Siralama({ ders, oyna }: { ders: Ders; oyna: (klip: string, metin: string[]) => void }) {
  const [ai, setAi] = useState(0);
  const ak = ders.sinav.akislar[ai];
  const Y = useMemo(() => yollar(ak.basamaklar), [ak]);
  const [yi, setYi] = useState(0);
  const yol = Y[Math.min(yi, Y.length - 1)];
  const dogru = yol.basamaklar;
  const [tohum, setTohum] = useState(() => Date.now() % 10000);
  const havuz = useMemo(() => karistir(dogru.map((b, i) => ({ b, i })), tohum), [dogru, tohum]);
  const [secim, setSecim] = useState<number[]>([]);
  const [kontrol, setKontrol] = useState(false);
  const [harita, setHarita] = useState(false);
  useEffect(() => { setSecim([]); setKontrol(false); }, [tohum, ai, yi]);
  useEffect(() => { setYi(0); }, [ai]);
  // aynı metinli basamaklar (dallarda "kaydet" gibi) yer değiştirebilir: metin eşleşmesi doğru sayılır
  const dogruMu = (v: number, i: number) => v === i || dogru[v].metin === dogru[i]?.metin;
  const puan = secim.filter((v, i) => dogruMu(v, i)).length;
  return (
    <div className="kmb-siralama">
      <div className="kmb-akis-sec">
        {ders.sinav.akislar.map((a, i) => <button key={a.id} className={i === ai ? 'etkin' : ''} onClick={() => setAi(i)}>{a.ad}</button>)}
        <button className={harita ? 'etkin' : ''} onClick={() => setHarita((h) => !h)}>🗺 Akış haritası</button>
      </div>
      {Y.length > 1 && (
        <div className="kmb-yol-sec" role="radiogroup" aria-label="Durum">
          <span>Durum:</span>
          {Y.map((y, i) => <button key={y.ad} role="radio" aria-checked={i === yi} className={i === yi ? 'etkin' : ''} onClick={() => setYi(i)}>{y.ad}</button>)}
        </div>
      )}
      <p className="kmb-yonerge">{ak.yonerge} Sağdaki kartlara sırayla dokun; yanlış yerleştirdiğine dokunursan geri alınır.</p>
      {harita && <div className="kmb-harita-kap"><Harita L={ak.basamaklar} ak={ak.id} oyna={oyna} /></div>}
      <div className="kmb-sira-iki">
        <ol className="kmb-yuvalar">
          {dogru.map((_, i) => {
            const v = secim[i];
            const karar = yol.kararlar.filter((k) => k.sonra === i);
            const ok = v !== undefined && kontrol ? dogruMu(v, i) : null;
            return (
              <React.Fragment key={i}>
                {karar.map((k) => <li key={k.soru} className="kmb-karar-serit" aria-hidden><span>◆ {k.soru}</span><b>{k.etiket}</b></li>)}
                <li className={`kmb-yuva${v === undefined ? ' bos' : ''}${ok === true ? ' dogru' : ok === false ? ' yanlis' : ''}`}>
                  <span className="no">{i + 1}</span>
                  {v === undefined ? <span className="yer">{i === secim.length ? 'Sıradaki basamak' : ''}</span> : (
                    <div className="icerik">
                      <button disabled={kontrol} onClick={() => setSecim((s) => s.slice(0, i))}>{dogru[v].metin}</button>
                      {ok === false && <small>Doğrusu: {dogru[i].metin}</small>}
                      {kontrol && <Ayrinti b={dogru[i]} ak={ak.id} oyna={oyna} />}
                    </div>
                  )}
                </li>
              </React.Fragment>
            );
          })}
        </ol>
        <div className="kmb-sira-havuz">
          {havuz.filter((h) => !secim.includes(h.i)).map((h) => (
            <button key={h.i} onClick={() => setSecim((s) => [...s, h.i])}>{h.b.metin}</button>
          ))}
          {secim.length === dogru.length && !kontrol && <p className="kmb-not">Tüm basamakları yerleştirdin, kontrol edebilirsin.</p>}
        </div>
      </div>
      <div className="kmb-denetim">
        <button className="ana" disabled={secim.length !== dogru.length || kontrol} onClick={() => {
          setKontrol(true);
          oyna('', [`${dogru.length} basamaktan ${secim.filter((v, i) => dogruMu(v, i)).length} tanesini doğru yere koydun.`]);
        }}>Kontrol et</button>
        <button onClick={() => setTohum((t) => t + 1)}>Yeniden karıştır</button>
        {kontrol && <span className="kmb-sayac">{puan} / {dogru.length} doğru</span>}
      </div>
    </div>
  );
}

function Senaryolar({ ders, ses, oynatici }: { ders: Ders; ses: SesKayit | null; oynatici: ReturnType<typeof useOynatici> }) {
  const [si, setSi] = useState(0);
  const [secim, setSecim] = useState<Record<string, number>>({});
  const s = ders.sinav.senaryolar[si];
  const sec = secim[s.id];
  const durum = useMemo(() => uygula({}, s.eylem), [s]);
  const { oynat } = oynatici;
  useEffect(() => { oynat(`s-${s.id}`, [s.soru]); }, [s, oynat]);
  const dogruSay = ders.sinav.senaryolar.filter((x) => secim[x.id] !== undefined && x.secenekler[secim[x.id]].dogru).length;
  return (
    <div className="kmb-senaryo">
      <div className="kmb-senaryo-ust">
        {ders.sinav.senaryolar.map((x, i) => {
          const v = secim[x.id];
          return <button key={x.id} className={`kmb-nokta${i === si ? ' etkin' : ''}${v === undefined ? '' : x.secenekler[v].dogru ? ' dogru' : ' yanlis'}`} onClick={() => setSi(i)} aria-label={x.baslik}>{i + 1}</button>;
        })}
        <span className="kmb-sayac">{dogruSay} / {ders.sinav.senaryolar.length} doğru</span>
      </div>
      <div className="kmb-senaryo-govde">
        <div className="kmb-sahne-kap kucuk"><SahneCiz sahne={s.sahne} durum={durum} /></div>
        <div>
          <h3>Vaka {si + 1}: {s.baslik}</h3>
          <p className="kmb-soru">{s.soru}</p>
          <div className="kmb-secenekler">
            {s.secenekler.map((c, i) => (
              <button key={i} disabled={sec !== undefined}
                className={sec === undefined ? '' : c.dogru ? 'dogru' : sec === i ? 'yanlis' : 'soluk'}
                onClick={() => {
                  setSecim((m) => ({ ...m, [s.id]: i }));
                  oynat(`s-${s.id}-${i}`, [(c.dogru ? 'Doğru. ' : 'Yanlış. ') + c.aciklama]);
                }}>
                <b>{'ABCDE'[i]}</b> {c.metin}
                {sec !== undefined && (sec === i || c.dogru) && <span className="kmb-aciklama">{c.aciklama}</span>}
              </button>
            ))}
          </div>
          {sec !== undefined && s.puf && <div className="kmb-kutu puf"><b>Püf noktası</b><p>{s.puf}</p></div>}
          <div className="kmb-denetim">
            <button onClick={() => setSi((i) => Math.max(0, i - 1))} disabled={si === 0}>‹ Önceki vaka</button>
            <button className="ana" onClick={() => setSi((i) => Math.min(ders.sinav.senaryolar.length - 1, i + 1))} disabled={si === ders.sinav.senaryolar.length - 1}>Sonraki vaka ›</button>
            {sec !== undefined && <button onClick={() => setSecim((m) => { const n = { ...m }; delete n[s.id]; return n; })}>Yeniden dene</button>}
            {!ses && <span className="kmb-sayac">sessiz kip</span>}
          </div>
        </div>
      </div>
    </div>
  );
}

function SahnedeBul({ ders, oynatici }: { ders: Ders; oynatici: ReturnType<typeof useOynatici> }) {
  const [bi, setBi] = useState(0);
  const [isaret, setIsaret] = useState<{ id: string; dogru: boolean } | null>(null);
  const b = ders.sinav.bul[bi];
  const { oynat } = oynatici;
  useEffect(() => { setIsaret(null); oynat(`b-${b.id}`, [b.yonerge]); }, [b, oynat]);
  const bitti = isaret?.dogru;
  const durum = useMemo<SahneDurum>(() => (bitti ? { [b.hedef]: { vurgu: 1, etiket: true, gor: true } } : {}), [bitti, b.hedef]);
  return (
    <div className="kmb-bul">
      <p className="kmb-yonerge"><b>Görev {bi + 1} / {ders.sinav.bul.length}:</b> {b.yonerge}</p>
      <div className="kmb-sahne-kap"><SahneCiz sahne={b.sahne} durum={durum} secilebilir={!bitti} isaret={isaret} onSec={(id) => {
        if (bitti) return;
        const d = id === b.hedef;
        setIsaret({ id, dogru: d });
        if (d) oynat(`b-${b.id}-d`, ['Doğru. ' + b.aciklama]);
      }} /></div>
      {isaret && <div className={`kmb-kutu ${isaret.dogru ? 'puf' : 'dikkat'}`}><b>{isaret.dogru ? 'Doğru' : 'Burası değil, yeniden dene'}</b>{isaret.dogru && <p>{b.aciklama}</p>}</div>}
      <div className="kmb-denetim">
        <button onClick={() => setBi((i) => Math.max(0, i - 1))} disabled={bi === 0}>‹ Önceki</button>
        <button className="ana" onClick={() => setBi((i) => Math.min(ders.sinav.bul.length - 1, i + 1))} disabled={bi === ders.sinav.bul.length - 1}>Sonraki ›</button>
      </div>
    </div>
  );
}

function Sinav({ ders, ses }: { ders: Ders; ses: SesKayit | null }) {
  const [sekme, setSekme] = useState<'vaka' | 'sira' | 'bul'>('vaka');
  const oynatici = useOynatici(ders.kod, ses);
  const { oynat, durdur } = oynatici;
  useEffect(() => durdur, [sekme, durdur]);
  return (
    <div className="kmb-sinav">
      <div className="kmb-sekmeler" role="tablist">
        {([['vaka', `Vaka senaryoları (${ders.sinav.senaryolar.length})`], ['sira', 'OSCE sıralama'], ['bul', `Sahnede bul (${ders.sinav.bul.length})`]] as const).map(([k, ad]) => (
          <button key={k} role="tab" aria-selected={sekme === k} className={sekme === k ? 'etkin' : ''} onClick={() => setSekme(k)}>{ad}</button>
        ))}
      </div>
      {sekme === 'vaka' && <Senaryolar ders={ders} ses={ses} oynatici={oynatici} />}
      {sekme === 'sira' && <Siralama ders={ders} oyna={(k, m) => oynat(k || 'yok', m)} />}
      {sekme === 'bul' && <SahnedeBul ders={ders} oynatici={oynatici} />}
    </div>
  );
}

/** KMB belgesindeki öğrenim hedefleriyle çalışma: her hedef bir kart — belge metni, görsel, ses, ne/nasıl/neden/sık hata,
 *  "önce kendin anlat" kipi (hocanın sorusu sesli sorulur, öğrenci anlatır, sonra cevabı açar), isteğe bağlı Lottie gösterimi. */
function Hedefler({ ders, ses }: { ders: Ders; ses: SesKayit | null }) {
  const K = ders.hedefCalisma || [];
  const anahtar = `medsoru_kmb_hedef_${ders.kod}`;
  const [hi, setHi] = useState(0);
  const [kendin, setKendin] = useState(false);
  const [acik, setAcik] = useState(true);
  const [video, setVideo] = useState(false);
  const [bitti, setBitti] = useState<number[]>(() => { try { return JSON.parse(localStorage.getItem(anahtar) || '[]'); } catch { return []; } });
  const k = K[hi];
  const belge = ders.hedefler.find((h) => h.no === k?.no);
  const { aktif, caliyor, oynat, durdur } = useOynatici(ders.kod, ses);
  const cumleler = k ? [`Hedef ${k.no}. ${k.ne}`, ...k.nasil, k.neden, 'Sınavda sık yapılan bir hata var.', k.hata] : [];
  const durum = useMemo(() => uygula({}, k?.eylem), [k]);
  useEffect(() => { setAcik(!kendin); setVideo(false); durdur(); }, [hi, kendin, durdur]);
  const isaretle = () => {
    const y = bitti.includes(k.no) ? bitti.filter((x) => x !== k.no) : [...bitti, k.no];
    setBitti(y);
    try { localStorage.setItem(anahtar, JSON.stringify(y)); } catch { /* yerel kayıt yoksa yalnız bu oturumda */ }
  };
  if (!k) return <p className="kmb-yukleniyor">Bu derste hedef kartı yok.</p>;
  const vurgu = (i: number) => (caliyor && aktif === i ? ' aktif' : '');
  return (
    <div className="kmb-hedef">
      <aside className="kmb-adimlar" aria-label="Öğrenim hedefleri">
        <p className="kmb-hedef-ilerleme">{bitti.length} / {K.length} hedef tamam</p>
        {K.map((x, i) => (
          <button key={x.no} className={`kmb-adim-dugme${i === hi ? ' etkin' : ''}${bitti.includes(x.no) ? ' gecti' : ''}`} onClick={() => setHi(i)}>
            <span className="no">{bitti.includes(x.no) ? '✓' : x.no}</span><span>{ders.hedefler.find((h) => h.no === x.no)?.metin}</span>
          </button>
        ))}
      </aside>
      <section className="kmb-sahne-alan">
        <div className="kmb-sahne-kap"><SahneCiz sahne={k.sahne} durum={durum} /></div>
        {k.lottie && (video
          ? <div className="kmb-videolar"><LottieVideo ad={k.lottie} kod={ders.kod} ses={ses} kompakt /></div>
          : <button className="kmb-dv-ac kmb-hedef-video" onClick={() => setVideo(true)}>▶ Bu hedefin uygulamalı gösterimini izle</button>)}
      </section>
      <section className="kmb-anlatim">
        <p className="kmb-hedef-belge"><span>KMB belgesi · Hedef {k.no}</span>{belge?.metin}</p>
        <label className="kmb-oto"><input type="checkbox" checked={kendin} onChange={(e) => setKendin(e.target.checked)} /> Önce kendin anlat (cevabı gizle)</label>
        {kendin && !acik ? (
          <div className="kmb-kutu soru">
            <b>Hoca soruyor</b><p>{k.hoca}</p>
            <p className="kmb-not">Sesli anlat: ne yaparsın, nasıl yaparsın, neden? Sonra cevabı aç ve karşılaştır.</p>
            <div className="kmb-denetim">
              <button onClick={() => oynat(`h-${k.no}-s`, [k.hoca, 'Önce kendin sesli anlat, sonra cevabı aç.'])}>▶ Soruyu dinle</button>
              <button className="ana" onClick={() => setAcik(true)}>Cevabı aç</button>
            </div>
          </div>
        ) : (
          <>
            <div className={`kmb-hedef-bolum${vurgu(0)}`}><b>Ne yaparsın</b><p>{k.ne}</p></div>
            <div className="kmb-hedef-bolum"><b>Nasıl</b>{k.nasil.map((c, i) => <p key={i} className={vurgu(i + 1).trim()}>{c}</p>)}</div>
            <div className={`kmb-hedef-bolum${vurgu(k.nasil.length + 1)}`}><b>Neden</b><p>{k.neden}</p></div>
            <div className={`kmb-kutu dikkat${vurgu(k.nasil.length + 3)}`}><b>Sık hata</b><p>{k.hata}</p></div>
            <div className="kmb-kutu puf"><b>Hoca sorar</b><p>{k.hoca}</p></div>
            {k.dogrulanacak && <p className="kmb-not">Not: {k.dogrulanacak}</p>}
          </>
        )}
        <div className="kmb-denetim">
          {caliyor ? <button className="ana" onClick={durdur}>❚❚ Durdur</button>
            : <button className="ana" onClick={() => { setAcik(true); oynat(`h-${k.no}`, cumleler); }}>▶ Dinle</button>}
          <button onClick={isaretle}>{bitti.includes(k.no) ? '✓ Öğrendim' : 'Öğrendim olarak işaretle'}</button>
          <button onClick={() => setHi((i) => Math.max(0, i - 1))} disabled={hi === 0}>‹</button>
          <button onClick={() => setHi((i) => Math.min(K.length - 1, i + 1))} disabled={hi === K.length - 1}>›</button>
        </div>
      </section>
    </div>
  );
}

function Videolar({ ders, ses }: { ders: Ders; ses: SesKayit | null }) {
  const [tum, setTum] = useState(false);
  const adlar = useMemo(() => [...new Set(ders.adimlar.flatMap((a) => (a.ek || []).filter((e) => e.startsWith('lottie:')).map((e) => e.slice(7))))], [ders]);
  return (
    <div className="kmb-video-sayfa">
      <div className="kmb-video-ust">
        <p>Her video hocanın anlattığı bir aşamayı sesli ve altyazılı gösterir. Tam ekran için ⤢, klavyede boşluk oynatır, ←/→ 5 sn sarar.</p>
        <button className="kmb-dv-ac" onClick={() => setTum(true)}>🎬 Bütün dersi video olarak izle</button>
      </div>
      <h3 className="kmb-video-bas">Adım adım ders videoları</h3>
      <div className="kmb-video-izgara">
        {ders.adimlar.filter((a) => LOTTILER.some((x) => x.adim === a.id)).map((a) => <LottieVideo key={a.id} ad={`adim-${a.id}`} kod={ders.kod} ses={ses} />)}
      </div>
      <h3 className="kmb-video-bas">Konu videoları</h3>
      <div className="kmb-video-izgara">
        {adlar.map((a) => <LottieVideo key={a} ad={a} kod={ders.kod} ses={ses} />)}
      </div>
      {tum && <DersVideo ders={ders} ses={ses} onKapat={() => setTum(false)} />}
    </div>
  );
}

// ———————————————————————————————— Kabuk

export default function KmbAsistan() {
  const { beceri, b, git } = useYol();
  const kayit = INDEX.beceriler.find((x) => x.slug === beceri);
  const [ders, setDers] = useState<Ders | null>(null);
  const [ses, setSes] = useState<SesKayit | null>(null);
  const [kapsam, setKapsam] = useState(false);
  useEffect(() => {
    setDers(null); setSes(null);
    if (!kayit || kayit.durum !== 'hazir') return;
    const y = DERSLER[`../../data/kmb/${kayit.kod}.json`];
    y?.().then((m: any) => setDers(m.default || m));
    const s = SESLER[`../../data/kmb/ses_${kayit.kod}.json`];
    s?.().then((m: any) => setSes(m.default || m)).catch(() => setSes(null));
  }, [kayit]);

  if (!kayit) {
    return (
      <div className="kmb-kok">
        <header className="kmb-baslik">
          <p className="ust">Sınava hazırlan · {INDEX.ders}</p>
          <h1>KMB görsel asistan</h1>
          <p>Hocanın anlattığı her aşamayı önce sesli ve görsel olarak öğren, sonra vaka sorularıyla pratik sınava hazırlan.</p>
          <p className="kmb-not">{INDEX.degerlendirme}</p>
        </header>
        <div className="kmb-kartlar">
          {INDEX.beceriler.map((x) => (
            <button key={x.slug} className={`kmb-kart${x.durum === 'hazir' ? '' : ' bekliyor'}`} disabled={x.durum !== 'hazir'} onClick={() => git(x.slug)}>
              <span className="kod">{x.belgeKodu}</span>
              <b>{x.ad}</b>
              <span className="durum">{x.durum === 'hazir' ? 'Hazır · öğren ve sınan' : 'Ders kaydı bekleniyor'}</span>
              {!!x.hocalar.length && <span className="hoca">{x.hocalar.join(' · ')}</span>}
            </button>
          ))}
        </div>
        <ul className="kmb-takvim">{INDEX.takvim.map((t) => <li key={t.tarih}><b>{new Date(t.tarih).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' })}</b> {t.ad}</li>)}</ul>
      </div>
    );
  }

  return (
    <div className="kmb-kok">
      <header className="kmb-baslik satir">
        <div>
          <button className="kmb-geri" onClick={() => git('')}>‹ KMB becerileri</button>
          <h1>{kayit.ad}</h1>
          {ders && <p>{ders.amac}</p>}
        </div>
        <div className="kmb-sekmeler" role="tablist">
          <button role="tab" aria-selected={b === 'ogren'} className={b === 'ogren' ? 'etkin' : ''} onClick={() => git(kayit.slug, 'ogren')}>Öğren</button>
          <button role="tab" aria-selected={b === 'hedef'} className={b === 'hedef' ? 'etkin' : ''} onClick={() => git(kayit.slug, 'hedef')}>Hedeflerle çalış</button>
          <button role="tab" aria-selected={b === 'video'} className={b === 'video' ? 'etkin' : ''} onClick={() => git(kayit.slug, 'video')}>Videolar</button>
          <button role="tab" aria-selected={b === 'sinav'} className={b === 'sinav' ? 'etkin' : ''} onClick={() => git(kayit.slug, 'sinav')}>Sınav</button>
          <button className={kapsam ? 'etkin' : ''} onClick={() => setKapsam((k) => !k)}>Kazanımlar</button>
        </div>
      </header>
      {kapsam && ders && (
        <ol className="kmb-kazanim">
          {ders.hedefler.map((h) => <li key={h.no}>{h.metin} <small>{h.adimlar.map((a) => ders.adimlar.findIndex((x) => x.id === a) + 1).filter((n) => n > 0).map((n) => `Adım ${n}`).join(', ')}</small></li>)}
        </ol>
      )}
      {!ders ? <p className="kmb-yukleniyor">Yükleniyor…</p> : b === 'sinav' ? <Sinav ders={ders} ses={ses} /> : b === 'video' ? <Videolar ders={ders} ses={ses} /> : b === 'hedef' ? <Hedefler ders={ders} ses={ses} /> : <Ogret ders={ders} ses={ses} />}
    </div>
  );
}
