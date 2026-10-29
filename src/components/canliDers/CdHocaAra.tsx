// Sesli derste "Hocanın sorabileceği soru" ara sayfası (kullanıcı kararı 2026-10-29; AGENTS.md kural 27).
// Hoca üslubuna göre soru çıkabilecek slaytın son paragrafı bitince ders sesi durur, yerine yapay bir soru sayfası açılır:
// EMA soruyu okur (q-N), kısa bir düşünme payından sonra çözer (c-N) ve çözümü önceki slaytlara dayanarak anlatır (a-N);
// sayfa kapanınca ders bir sonraki slayttan sürer. Araç çubuğundaki ünlem (CdHocaAraDugme) tüm soruları ardışık oynatır.
// Veri: src/data/k<N>hocaara_cozucu/{index,<kod>}.json (scripts/hoca_ara_soru/kur.py birlestir); aynı sorular ders dışında
// /soru-cozucu?brans=k<N>hocaara ile çözülür. Ses tek oynatıcıdan sırayla çalınır; ders sesi çalarsa ara ses susar.
import React, { useCallback, useEffect, useRef, useState, useSyncExternalStore } from 'react';
import { createPortal } from 'react-dom';
import { ChevronLeft, ChevronRight, CircleAlert, Pause, Play, X } from 'lucide-react';
import { dersSoruKaydet } from '../../services/calismaTakip';
import { klipYolu, HARFLER, type CDers, type CDizin, type CSoru, type Harf, type Klip } from '../spots/cozucu/cozucuVeri';
import type { Brans } from '../spots/brans';
import { cdAbone, cdDurum, cdDuraklat, cdParagrafa, cdToggle } from './canliDersStore';
import '../../styles/v15/hoca_ara.css';

type AraSoru = CSoru & { ara: NonNullable<CSoru['ara']>; anlatim: string };
interface AraDers { brans: Brans; ders: Omit<CDers, 'sorular'> & { sorular: AraSoru[] }; ortak: CDizin['ortak'] }

const DIZIN = import.meta.glob('../../data/k*hocaara_cozucu/index.json', { eager: true, import: 'default' }) as Record<string, CDizin & { dersler: { kod: string; key?: string }[] }>;
const DERS = import.meta.glob('../../data/k*hocaara_cozucu/*.json', { import: 'default' }) as Record<string, () => Promise<CDers>>;
const onbellek = new Map<string, Promise<AraDers | null>>();
const kisaKey = (k: string) => /^k\d-\d{2}/.exec(k)?.[0] || k;

/** Ders anahtarının ara soruları (yoksa null) */
export function hocaAraYukle(key: string): Promise<AraDers | null> {
  let p = onbellek.get(key);
  if (p) return p;
  p = (async () => {
    for (const [yol, d] of Object.entries(DIZIN)) {
      const x = d.dersler.find((y) => y.key === key) || d.dersler.find((y) => y.key && kisaKey(y.key) === kisaKey(key));
      if (!x) continue;
      const brans = /data\/(k[^/]*)_cozucu\//.exec(yol)?.[1] as Brans;
      const f = DERS[yol.replace('index.json', `${x.kod}.json`)];
      if (!f) return null;
      const ders = (await f()) as unknown as AraDers['ders'];
      return ders.sorular?.length ? { brans, ders, ortak: d.ortak || {} } : null;
    }
    return null;
  })().catch(() => null);
  onbellek.set(key, p);
  return p;
}

export function useHocaAra(key: string | null | undefined): AraDers | null {
  const [v, setV] = useState<AraDers | null>(null);
  useEffect(() => {
    let iptal = false;
    setV(null);
    if (key) hocaAraYukle(key).then((x) => { if (!iptal) setV(x); });
    return () => { iptal = true; };
  }, [key]);
  return v;
}

/* ── tercih: ders içinde kendiliğinden açılsın mı (öğrenci kapatabilir) ── */
const TERCIH = 'medsoru_hoca_ara_oto_v1';
const otoAcik = () => { try { return localStorage.getItem(TERCIH) !== '0'; } catch { return true; } };
const otoYaz = (v: boolean) => { try { localStorage.setItem(TERCIH, v ? '1' : '0'); } catch { /* özel pencere */ } };

/* ── açık sayfa durumu ── */
type Acik = { veri: AraDers; liste: AraSoru[]; i: number; hepsi: boolean; caliyordu: boolean; devam: number | null } | null;
let acik: Acik = null;
const dinle = new Set<() => void>();
const ayarla = (a: Acik) => { acik = a; dinle.forEach((f) => f()); };
const abone = (f: () => void) => { dinle.add(f); return () => { dinle.delete(f); }; };

function ac(veri: AraDers, liste: AraSoru[], hepsi: boolean, devam: number | null) {
  const s = cdDurum();
  const caliyordu = s.playing;
  if (caliyordu) cdDuraklat();
  ayarla({ veri, liste, i: 0, hepsi, caliyordu: caliyordu || devam != null, devam });
}

/* ── tek ses oynatıcısı: her çalış öncekini keser; eski onended'ler jetonla düşer ── */
let ses: HTMLAudioElement | null = null;
let jeton = 0;
function sesDur() { jeton++; if (ses) { ses.onended = null; ses.ontimeupdate = null; ses.pause(); } }
function sesCal(url: string | null, okumaSn: number, onT: (t: number) => void): Promise<boolean> {
  sesDur();
  const j = jeton;
  return new Promise((coz) => {
    if (!url) { // klip yoksa okuma süresi kadar bekle (metin ekranda)
      const t0 = performance.now();
      const id = window.setInterval(() => {
        if (j !== jeton) { clearInterval(id); coz(false); return; }
        const t = (performance.now() - t0) / 1000;
        onT(t);
        if (t >= okumaSn) { clearInterval(id); coz(true); }
      }, 100);
      return;
    }
    ses = ses || new Audio();
    ses.src = url;
    ses.ontimeupdate = () => { if (j === jeton && ses) onT(ses.currentTime); };
    ses.onended = () => { if (j === jeton) coz(true); };
    ses.onerror = () => { if (j === jeton) coz(true); };
    ses.play().catch(() => { if (j === jeton) coz(true); });
  });
}
const okumaSn = (m: string) => Math.max(2, (m.match(/\S+/g) || []).length * 0.42);

/** Ders ekranında bir kez bulunur: tetikleyici (slayt bitti → soru sayfası) + açık sayfa */
export function CdHocaAraKok({ dersKey }: { dersKey: string }) {
  const veri = useHocaAra(dersKey);
  const a = useSyncExternalStore(abone, () => acik);
  const gosterilen = useRef(new Set<number>());
  useEffect(() => { gosterilen.current = new Set(); }, [dersKey]);
  useEffect(() => () => { sesDur(); ayarla(null); }, []);
  useEffect(() => {
    if (!veri) return;
    let onceki = cdDurum().aktif;
    let caliyordu = cdDurum().playing;
    const birak = cdAbone(() => {
      const s = cdDurum();
      // Sayfa açıkken ders sesi yeniden başlatılırsa ara ses susar ve sayfa kalkar (iki ses üst üste çalmaz)
      if (s.playing && !caliyordu && acik) { sesDur(); ayarla(null); }
      caliyordu = s.playing;
      if (s.aktif === onceki) return;
      const bitti = onceki;
      onceki = s.aktif;
      if (!s.playing || acik || !otoAcik() || s.aktif !== bitti + 1) return;
      const liste = veri.ders.sorular.filter((q) => q.ara.paragraf === bitti && !gosterilen.current.has(q.no));
      if (!liste.length) return;
      liste.forEach((q) => gosterilen.current.add(q.no));
      ac(veri, liste, false, s.aktif);
    });
    return () => { birak(); };
  }, [veri]);
  if (!a) return null;
  const kapat = () => {
    sesDur();
    const x = acik;
    ayarla(null);
    if (!x?.caliyordu || cdDurum().playing) return;
    if (x.devam != null) cdParagrafa(x.devam); else cdToggle();
  };
  return createPortal(<AraSayfa a={a} onKapat={kapat} />, document.body);
}

/** Araç çubuğu ünlemi: tüm ara soruları ardışık okutup çözdürür */
export function CdHocaAraDugme({ dersKey }: { dersKey: string }) {
  const veri = useHocaAra(dersKey);
  if (!veri) return null;
  const n = veri.ders.sorular.length;
  return (
    <button type="button" className="cd-btn is-ikon ha-dugme" onClick={() => ac(veri, veri.ders.sorular, true, null)}
      aria-label={`Hocanın sorabileceği sorular (${n}) — hepsini sesli çöz`} title={`Hocanın sorabileceği sorular (${n}): okur, çözer, slayttan anlatır`}>
      <CircleAlert aria-hidden /><span className="ha-dugme-n" aria-hidden>{n}</span>
    </button>
  );
}

type Evre = 'oku' | 'dusun' | 'coz' | 'anlat' | 'bitti';
const BEKLE_SN = 5;

function AraSayfa({ a, onKapat }: { a: NonNullable<Acik>; onKapat: () => void }) {
  const { veri, liste, hepsi } = a;
  const q = liste[Math.min(a.i, liste.length - 1)];
  const [evre, setEvre] = useState<Evre>('oku');
  const [secim, setSecim] = useState<Harf | null>(null);
  const [vurgu, setVurgu] = useState<string | null>(null); // 'kok' | harf | 'anlatim'
  const [kalan, setKalan] = useState(BEKLE_SN);
  const [durdu, setDurdu] = useState(false);
  const [oto, setOto] = useState(otoAcik);
  const akis = useRef(0);
  const { brans, ders, ortak } = veri;

  const klip = useCallback((ad: string): { url: string | null; k?: Klip } => {
    const k = ders.klip?.[ad];
    if (!k) return { url: null };
    return { url: `${klipYolu(brans, 'ema', ders.klasor || ders.kod, ad)}?v=${k.v}`, k };
  }, [brans, ders]);
  const ortakUrl = (ad: string) => (ortak[ad] ? `${klipYolu(brans, 'ema', 'ortak', ad)}?v=${ortak[ad].v}` : null);

  /** Bir klibi çalar; zaman dizisine göre o an okunan parçayı vurgular */
  const cal = useCallback(async (ad: string, metin: string, parca: (c: number) => string | null) => {
    const { url, k } = klip(ad);
    return sesCal(url, okumaSn(metin), (t) => {
      const z = k?.zaman || [];
      let c = 0;
      for (let x = 0; x < z.length; x++) if (t >= z[x][0]) c = x;
      setVurgu(parca(c));
    });
  }, [klip]);

  const sonraki = useCallback(() => {
    if (a.i < liste.length - 1) ayarla({ ...a, i: a.i + 1 });
    else onKapat();
  }, [a, liste.length, onKapat]);

  /** çözüm + slayt anlatımı, ardından sonraki soru / derse dönüş */
  const cozVeAnlat = useCallback(async (no: number, yanlis: Harf | null, dogruSecti = false) => {
    const id = akis.current;
    const dur = () => id !== akis.current;
    setEvre('coz');
    if (yanlis) {
      if (!(await sesCal(ortakUrl('yanlis'), 0.8, () => {})) || dur()) return;
      if (!(await cal(`s-${no}-${yanlis}`, q.siklar[yanlis], () => yanlis)) || dur()) return;
    }
    if (!(await cal(dogruSecti ? `d-${no}` : `c-${no}`, q.cozum, () => q.dogru)) || dur()) return;
    setEvre('anlat');
    if (!(await cal(`a-${no}`, q.anlatim, () => 'anlatim')) || dur()) return;
    setEvre('bitti');
    setVurgu(null);
    await new Promise((r) => setTimeout(r, 1200));
    if (!dur()) sonraki();
  }, [cal, q, sonraki]); // eslint-disable-line react-hooks/exhaustive-deps

  // Soru değişince: oku → düşünme payı → çöz → anlat
  useEffect(() => {
    const id = ++akis.current;
    const dur = () => id !== akis.current;
    setEvre('oku'); setSecim(null); setVurgu(null); setDurdu(false); setKalan(BEKLE_SN);
    (async () => {
      const ok = await cal(`q-${q.no}`, [q.soru, ...Object.values(q.secenekler)].join(' '), (c) => (c === 0 ? 'kok' : HARFLER[c - 1] || null));
      if (!ok || dur()) return;
      setEvre('dusun'); setVurgu(null);
      for (let s = BEKLE_SN; s > 0; s--) {
        setKalan(s);
        await new Promise((r) => setTimeout(r, 1000));
        if (dur()) return;
      }
      cozVeAnlat(q.no, null);
    })();
    return () => { akis.current++; sesDur(); };
  }, [q.no]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') onKapat(); };
    window.addEventListener('keydown', k);
    return () => window.removeEventListener('keydown', k);
  }, [onKapat]);

  const sec = (h: Harf) => {
    if (secim) { // çözülmüş soruda şıkka dokunmak o şıkkın açıklamasını okur
      akis.current++;
      setDurdu(false);
      cal(`s-${q.no}-${h}`, q.siklar[h], () => h);
      return;
    }
    akis.current++;
    setSecim(h);
    dersSoruKaydet(cdDurum().key, 'hoca', `${ders.kod}-${q.no}`);
    cozVeAnlat(q.no, h === q.dogru ? null : h, h === q.dogru);
  };
  const hemenCoz = () => { akis.current++; cozVeAnlat(q.no, null); };
  const duraklat = () => {
    if (!ses) return;
    if (durdu) { ses.play().catch(() => {}); setDurdu(false); } else { ses.pause(); setDurdu(true); }
  };
  const cozuldu = evre === 'coz' || evre === 'anlat' || evre === 'bitti';
  const sira = Math.min(a.i, liste.length - 1);
  const git = (n: number) => ayarla({ ...a, i: n });

  return (
    <div className="ha-kat" role="presentation">
      <div className="ha-sayfa" role="dialog" aria-modal="true" aria-label="Hocanın sorabileceği soru">
        <header className="ha-bas">
          <span className="ha-et"><CircleAlert aria-hidden /> Hocanın sorabileceği soru</span>
          <span className="ha-no">{hepsi || liste.length > 1 ? `${sira + 1}/${liste.length} · ` : ''}{q.ara.sayfa}. slayttan sonra</span>
          {(hepsi || liste.length > 1) && <button type="button" className="ha-ib" disabled={sira <= 0} onClick={() => git(sira - 1)} aria-label="Önceki soru"><ChevronLeft aria-hidden /></button>}
          {(hepsi || liste.length > 1) && <button type="button" className="ha-ib" disabled={sira >= liste.length - 1} onClick={() => git(sira + 1)} aria-label="Sonraki soru"><ChevronRight aria-hidden /></button>}
          <button type="button" className="ha-ib" onClick={duraklat} aria-label={durdu ? 'Sesi sürdür' : 'Sesi duraklat'}>{durdu ? <Play aria-hidden /> : <Pause aria-hidden />}</button>
          <button type="button" className="ha-ib" onClick={onKapat} aria-label={hepsi ? 'Kapat' : 'Atla ve derse dön'}><X aria-hidden /></button>
        </header>
        <div className="ha-govde">
          <p className={`ha-kok${vurgu === 'kok' ? ' is-okunan' : ''}`}>{q.soru}</p>
          <div className="ha-siklar" role="radiogroup" aria-label="Seçenekler">
            {HARFLER.map((h) => {
              const d = h === q.dogru;
              const cls = !cozuldu ? '' : d ? ' is-dogru' : h === secim ? ' is-yanlis' : ' is-soluk';
              return (
                <button key={h} type="button" role="radio" aria-checked={h === secim} className={`ha-sik${cls}${vurgu === h ? ' is-okunan' : ''}`} onClick={() => sec(h)}>
                  <b>{h}</b>
                  <span>{q.secenekler[h]}{cozuldu && (vurgu === h || d) && <small>{q.siklar[h]}</small>}</span>
                </button>
              );
            })}
          </div>
          {evre === 'dusun' && (
            <p className="ha-dusun">Düşün: {kalan} sn sonra çözüyorum · <button type="button" onClick={hemenCoz}>Hemen çöz</button></p>
          )}
          {(evre === 'anlat' || evre === 'bitti') && (
            <section className={`ha-anlat${vurgu === 'anlatim' ? ' is-okunan' : ''}`} aria-label="Slaytlardan çözüm">
              <h3>Slaytlardan çözüm <span>{q.sayfa.map((p) => `${p}. slayt`).join(' · ')}</span></h3>
              <p>{q.anlatim}</p>
            </section>
          )}
        </div>
        <footer className="ha-alt">
          {!hepsi && (
            <label className="ha-oto">
              <input type="checkbox" checked={oto} onChange={(e) => { setOto(e.target.checked); otoYaz(e.target.checked); }} />
              Derste kendiliğinden göster
            </label>
          )}
          <span className="ha-bosluk" />
          {cozuldu && sira < liste.length - 1 && <button type="button" className="ha-btn is-soft" onClick={() => git(sira + 1)}>Sonraki soru</button>}
          <button type="button" className="ha-btn" onClick={onKapat}><Play aria-hidden /> {hepsi ? 'Kapat' : 'Derse dön'}</button>
        </footer>
      </div>
    </div>
  );
}
