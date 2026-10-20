/**
 * /genetik-check-up — TBG Sınav Kampı (Kurul 1 Tıbbi Genetik, 12 soru).
 * Hocanın kalıbı: "… bulguyla gelen hasta hangi sendromu düşündürür?", kanserde hedef ilaçlar, spesifik belirteçler + son yılların çıkmışları.
 * Tek kaynak: data/genetik_asistan/g07.json (asistan_birlestir.py; EMA klipleri /api/patoloji-asistan/ses/g07/<klip>.mp3)
 * ve data/genetik_kamp/kalip.json (hızlı tekrar tabloları). Hızlı mod = puan ≥ 97 adımlar + adım başına 1 soru; Tam mod = hepsi.
 */
import React, { Suspense, lazy, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Headphones,
  Check, ChevronLeft, ChevronRight, Dna, Eye, EyeOff, LifeBuoy, ListChecks, Pause, Play,
  RotateCcw, Search, Shuffle, Table2, Volume2, X, Zap, BookOpen, Layers,
} from 'lucide-react';
import { getCustomApiUrl } from '../../services/api';
import { PatolojiAsistan } from '../spots/asistan/PatolojiAsistan';
import { MetinAktarMenu } from '../MetinAktarMenu';
import type { AktarBelge } from '../../services/metinDisaAktar';
import dersRaw from '../../data/genetik_asistan/g07.json';
import kalipRaw from '../../data/genetik_kamp/kalip.json';
import '../../styles/genetik-kamp.css';

const CanliDersDers = lazy(() => import('../canliDers/CanliDersDers'));
/** Kampın sesli dersi: altı genetik dersinin slaytlarıyla tek ders (data/sesli_anlatim, sanal deste k1p-k1-70-…) */
export const TBG_DERS_KEY = 'k1-70-tbg-sinav-kampi';

interface Klip { v: string; sure: number; zaman: [number, number][] }
interface Soru {
  k: string; tur: 'cikmis' | 'ornek'; sinav?: string; kok: string; secenekler: Record<string, string>; dogru: string;
  dogruMetin: string; yanlis: Record<string, string>; yardim: Record<string, string>;
}
interface Nokta { id: string; bolum: number; puan: number; aday: number | null; kategori: string; baslik: string; bilgi: string; cumleler: string[]; sorular: Soru[] }
interface Ders { kod: string; baslik: string; giris: string[]; kapanis: string[]; bolumler: { baslik: string; neden: string }[]; noktalar: Nokta[]; klip: Record<string, Klip> }
interface KalipSatir { s: string; t: string; k: string; h: number }
interface Kalip { id: string; baslik: string; soru: string; sutun: [string, string]; satir: KalipSatir[] }

const DERS = dersRaw as unknown as Ders;
const KALIPLAR = (kalipRaw as unknown as { kalipler: Kalip[] }).kalipler;
const HIZLI_PUAN = 97;
const YAVAS_PUAN = 85;
const MODLAR = ['hizli', 'yavas', 'tam'] as const;
const MOD_AD: Record<string, string> = { hizli: 'Hızlı mod', yavas: 'Yavaş mod', tam: 'Tam mod' };
const MOD_ALT: Record<string, string> = {
  hizli: 'En çok sorulanlar, adım başına 1 soru',
  yavas: 'Kalıba uyan önemli bilgilerin hepsi',
  tam: 'Yavaş modun 2 katı ayrıntı: sınavda çıkabilecek her bilgi',
};
/** Bir nokta bu modda görünür mü */
const modda = (n: { puan: number }, m: string) => (m === 'hizli' ? n.puan >= HIZLI_PUAN : m === 'yavas' ? n.puan >= YAVAS_PUAN : true);
const HIZLAR = [1, 1.15, 1.25, 1.5, 1.75, 2];
const ANAHTAR = 'medsoru_genetik_kamp_v1';
const KATEGORI: Record<string, string> = { sendrom: 'Bulgu → sendrom', ilac: 'Kanser → ilaç', belirtec: 'Belirteç', tani: 'Tanı yöntemi' };

type Mod = 'hizli' | 'yavas' | 'tam';
type Sekme = 'sesli' | 'ders' | 'kalip' | 'deneme';
const SEKMELER: [Sekme, string, string, React.ComponentType<{ 'aria-hidden'?: boolean }>][] = [
  ['sesli', 'Sesli ders', 'Aşama aşama, slaytlarla', Headphones],
  ['ders', 'Soru çözerek', 'Adım adım, her adımda çıkmış', ListChecks],
  ['kalip', 'Kalıp kartları', 'Bulgu → tanı, kanser → ilaç', Table2],
  ['deneme', 'Deneme', '12 soruluk sınav provası', Shuffle],
];
/** Sayfa adresi: /genetik-check-up?b=ders|kalip|deneme (yoksa sesli ders) — her bölüm ayrı sayfa, Geri ile dönülür */
const sekmeOku = (): Sekme => {
  const b = new URLSearchParams(window.location.search).get('b');
  return b === 'ders' || b === 'kalip' || b === 'deneme' ? b : 'sesli';
};
function sekmeYaz(b: Sekme) {
  const u = new URL(window.location.href);
  if (b === 'sesli') u.searchParams.delete('b'); else u.searchParams.set('b', b);
  if (u.href !== window.location.href) window.history.pushState(window.history.state, '', u.pathname + u.search + u.hash);
}

/** Kampın ortak başı: ad + bölüm sayfaları (sesli ders ekranında geri bağlantısının yerine geçer) */
function KampGezinme({ sekme, onSekme, sade = false }: { sekme: Sekme; onSekme: (s: Sekme) => void; sade?: boolean }) {
  return (
    <nav className={`tk-gez${sade ? ' is-sade' : ''}`} aria-label="TBG Sınav Kampı bölümleri">
      <span className="tk-gez-ad" title="Kurul 1 · Tıbbi Biyoloji ve Genetik · 12 soru"><Dna aria-hidden /><b>TBG Sınav Kampı</b></span>
      <span className="tk-gez-sek" role="tablist">
        {SEKMELER.map(([id, ad, alt, Ic]) => (
          <button key={id} type="button" role="tab" aria-selected={sekme === id} className={sekme === id ? 'is-on' : ''} title={alt} onClick={() => onSekme(id)}>
            <Ic aria-hidden /><span>{ad}</span>
          </button>
        ))}
      </span>
    </nav>
  );
}
interface Kayit { mod: Mod; adim: Record<Mod, number>; tamam: Record<string, 1>; cevap: Record<string, string>; hiz: number; oto: boolean }

function kayitOku(): Kayit {
  const bos: Kayit = { mod: 'hizli', adim: { hizli: 0, yavas: 0, tam: 0 }, tamam: {}, cevap: {}, hiz: 1, oto: true };
  try {
    const r = JSON.parse(localStorage.getItem(ANAHTAR) || 'null');
    return r ? { ...bos, ...r, adim: { ...bos.adim, ...(r.adim || {}) } } : bos;
  } catch { return bos; }
}

/** **kalın** işaretlerini <b>'ye çevirir */
function Zengin({ t }: { t: string }) {
  return <>{String(t || '').split(/(\*\*[^*]+\*\*)/g).map((p, i) => (p.startsWith('**') && p.endsWith('**') ? <b key={i}>{p.slice(2, -2)}</b> : <React.Fragment key={i}>{p}</React.Fragment>))}</>;
}

const dakika = (sn: number) => Math.max(1, Math.round(sn / 60));
const harfler = (s: Soru) => Object.keys(s.secenekler).sort();

/** Bir adımın sorularından hızlı modda gösterilecek tek soru: önce çıkmış */
function modSorulari(n: Nokta, mod: Mod): Soru[] {
  if (mod !== 'hizli') return n.sorular;
  const c = n.sorular.find((s) => s.tur === 'cikmis');
  return c ? [c] : n.sorular.slice(0, 1);
}

/** Tam ekran asistan için hızlı mod: yalnız puan ≥ 97 noktalar, adım başına tek soru */
const hizliSuz = (d: Ders): Ders => ({
  ...d,
  noktalar: d.noktalar.filter((n) => n.puan >= HIZLI_PUAN).map((n) => ({ ...n, sorular: modSorulari(n, 'hizli') })),
});
const yavasSuz = (d: Ders): Ders => ({ ...d, noktalar: d.noktalar.filter((n) => n.puan >= YAVAS_PUAN) });

export const GenetikCheckUp: React.FC<{ onBack?: () => void }> = () => {
  const [kayit, setKayit] = useState<Kayit>(kayitOku);
  const [sekme, setSekme0] = useState<Sekme>(sekmeOku);
  const setSekme = useCallback((b: Sekme) => { setSekme0(b); sekmeYaz(b); window.scrollTo({ top: 0 }); }, []);
  useEffect(() => {
    const f = () => setSekme0(sekmeOku());
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  useEffect(() => { document.title = 'TBG Sınav Kampı · MeDSor'; }, [sekme]);
  const [tamEkran, setTamEkran] = useState<Mod | null>(null);
  const [yardim, setYardim] = useState<Record<string, boolean>>({});
  const [calan, setCalan] = useState<{ id: string; cumle: number; oynuyor: boolean } | null>(null);
  const audio = useRef<HTMLAudioElement | null>(null);
  const kartRef = useRef<HTMLElement | null>(null);
  const zincir = useRef<(() => void) | null>(null);

  const mod = kayit.mod;
  const guncelle = useCallback((f: (k: Kayit) => Kayit) => setKayit((k) => f(k)), []);
  useEffect(() => { try { localStorage.setItem(ANAHTAR, JSON.stringify(kayit)); } catch { /* özel pencere */ } }, [kayit]);

  const adimlar = useMemo(() => DERS.noktalar.filter((n) => modda(n, mod)), [mod]);
  const idx = Math.min(kayit.adim[mod] || 0, adimlar.length - 1);
  const nokta = adimlar[idx];

  const sure = useMemo(() => {
    const top = (m: Mod) => {
      const N = DERS.noktalar.filter((n) => modda(n, m));
      const b = new Set(N.map((n) => n.bolum));
      const k = (id: string, yedek: number) => DERS.klip[id]?.sure ?? yedek;
      return N.reduce((t, n) => t + k(`a-${n.id}`, n.cumleler.join(' ').split(/\s+/).length / 2.4)
        + modSorulari(n, m).reduce((x, s) => x + k(`q-${s.k}`, 10) + 25, 0), 0)
        + [...b].reduce((t, i) => t + k(`b-${i + 1}`, 8), 0);
    };
    return { hizli: dakika(top('hizli')), yavas: dakika(top('yavas')), tam: dakika(top('tam')) };
  }, []);

  /* ——— ses ——— */
  const durdur = useCallback(() => {
    zincir.current = null;
    const a = audio.current;
    if (a) { a.onended = null; a.ontimeupdate = null; a.pause(); }
    setCalan(null);
  }, []);
  useEffect(() => () => durdur(), [durdur]);
  useEffect(() => { if (audio.current) audio.current.playbackRate = kayit.hiz; }, [kayit.hiz]);

  const cal = useCallback((id: string, bitince?: () => void, cumle = 0) => {
    const k = DERS.klip[id];
    if (!k) { bitince?.(); return; }
    durdur();
    const a = audio.current || new Audio();
    audio.current = a;
    a.src = `${getCustomApiUrl()}/api/patoloji-asistan/ses/${DERS.kod}/${id}.mp3?v=${k.v}`;
    a.playbackRate = kayit.hiz;
    if (cumle > 0 && k.zaman[cumle]) a.currentTime = Math.max(0, k.zaman[cumle][0] - 0.05);
    zincir.current = bitince || null;
    a.ontimeupdate = () => {
      const t = a.currentTime;
      const i = k.zaman.findIndex(([b, s]) => t >= b - 0.08 && t <= s + 0.15);
      if (i >= 0) setCalan((c) => (c && c.id === id && c.cumle !== i ? { ...c, cumle: i } : c));
    };
    a.onended = () => { setCalan(null); const z = zincir.current; zincir.current = null; z?.(); };
    a.onerror = () => setCalan(null);
    setCalan({ id, cumle, oynuyor: true });
    a.play().catch(() => setCalan(null));
  }, [durdur, kayit.hiz]);

  const duraklat = useCallback(() => {
    const a = audio.current;
    if (!a || !calan) return;
    if (calan.oynuyor) { a.pause(); setCalan({ ...calan, oynuyor: false }); }
    else { a.play().catch(() => {}); setCalan({ ...calan, oynuyor: true }); }
  }, [calan]);

  const git = useCallback((i: number, oku = false) => {
    durdur();
    const yeni = Math.max(0, Math.min(adimlar.length - 1, i));
    guncelle((k) => ({ ...k, adim: { ...k.adim, [mod]: yeni } }));
    const el = kartRef.current;
    if (el && el.getBoundingClientRect().top < 0) el.scrollIntoView({ block: 'start' });
    if (oku) setTimeout(() => anlatRef.current(yeni), 60);
  }, [adimlar.length, durdur, guncelle, mod]);

  /** Adımı anlat: bölümün ilk adımıysa önce bölüm girişi, sonra anlatım, sonra ilk cevapsız sorunun kökü */
  const anlat = useCallback((i: number, cumle = 0) => {
    const n = adimlar[i];
    if (!n) return;
    const ilk = adimlar.findIndex((x) => x.bolum === n.bolum) === i;
    const soruOku = () => {
      if (!kayit.oto) return;
      const s = modSorulari(n, mod).find((x) => !kayit.cevap[x.k]);
      if (s) cal(`q-${s.k}`);
      else if (i < adimlar.length - 1) git(i + 1, true);
    };
    const ana = () => cal(`a-${n.id}`, () => { guncelle((k) => ({ ...k, tamam: { ...k.tamam, [n.id]: 1 } })); soruOku(); }, cumle);
    if (ilk && cumle === 0 && DERS.klip[`b-${n.bolum + 1}`]) cal(`b-${n.bolum + 1}`, ana); else ana();
  }, [adimlar, cal, git, guncelle, kayit.cevap, kayit.oto, mod]);
  const anlatRef = useRef(anlat);
  anlatRef.current = anlat;

  const sec = useCallback((n: Nokta, s: Soru, h: string, adimIci: boolean) => {
    guncelle((k) => ({ ...k, cevap: { ...k.cevap, [s.k]: h } }));
    const devam = () => {
      if (!adimIci || !kayit.oto) return;
      const kalan = modSorulari(n, mod).filter((x) => x.k !== s.k && !kayit.cevap[x.k]);
      if (kalan[0]) cal(`q-${kalan[0].k}`);
      else if (idx < adimlar.length - 1) git(idx + 1, true);
    };
    cal(h === s.dogru ? `d-${s.k}` : `y-${s.k}-${h}`, h === s.dogru ? devam : undefined);
  }, [adimlar.length, cal, git, guncelle, idx, kayit.cevap, kayit.oto, mod]);

  const sifirla = () => {
    if (!window.confirm('Bu sayfadaki ilerleme ve cevaplar silinsin mi?')) return;
    durdur();
    setYardim({});
    guncelle((k) => ({ ...k, adim: { hizli: 0, yavas: 0, tam: 0 }, tamam: {}, cevap: {} }));
  };

  /* ——— istatistik ——— */
  const tumSorular = useMemo(() => DERS.noktalar.flatMap((n) => n.sorular.map((s) => ({ s, n }))), []);
  const cikmisDagilim = useMemo(() => DERS.bolumler.map((b, i) => ({
    ad: b.baslik.split(':')[0],
    n: DERS.noktalar.filter((x) => x.bolum === i).reduce((t, x) => t + x.sorular.filter((s) => s.tur === 'cikmis').length, 0),
  })), []);
  const enCok = Math.max(1, ...cikmisDagilim.map((d) => d.n));
  const bitenAdim = adimlar.filter((n) => kayit.tamam[n.id]).length;
  const modSoru = adimlar.flatMap((n) => modSorulari(n, mod));
  const dogruSay = modSoru.filter((s) => kayit.cevap[s.k] === s.dogru).length;
  const cevapSay = modSoru.filter((s) => kayit.cevap[s.k]).length;

  const belge = useCallback((): AktarBelge => ({
    baslik: 'TBG Sınav Kampı — Genetik',
    alt: `${MOD_AD[mod]}: ${MOD_ALT[mod]}`,
    bolumler: [
      ...DERS.bolumler.map((b, bi) => ({
        baslik: b.baslik,
        alt: b.neden,
        md: adimlar.filter((n) => n.bolum === bi).map((n) => `### ${n.baslik}\n\n${n.cumleler.map((c) => `- ${c}`).join('\n')}`).join('\n\n'),
      })).filter((b) => b.md),
      ...KALIPLAR.map((k) => ({
        baslik: k.baslik,
        alt: k.soru,
        md: `| ${k.sutun[0]} | ${k.sutun[1]} |\n|---|---|\n${k.satir.filter((r) => mod !== 'hizli' || r.h).map((r) => `| ${r.s} | ${r.t} |`).join('\n')}`,
      })),
    ],
  }), [adimlar, mod]);

  // Sesli ders: sesli ders ekranının kendisi (kamp kipinde); tüm alanı kaplar
  if (sekme === 'sesli') {
    return (
      <div className="tk-sesli">
        <Suspense fallback={<div className="tk-bos">Yükleniyor…</div>}>
          <CanliDersDers dersKey={TBG_DERS_KEY} kamp={{ geri: <KampGezinme sekme={sekme} onSekme={setSekme} sade /> }} />
        </Suspense>
      </div>
    );
  }

  return (
    <div className="tk">
      <KampGezinme sekme={sekme} onSekme={(b) => { durdur(); setSekme(b); }} />

      {sekme !== 'kalip' && (
        <section className="tk-mod tk-mod-sade" aria-label="Çalışma modu">
          <div className="tk-mod-sec" role="radiogroup" aria-label="Mod">
            {MODLAR.map((m) => {
              const N = DERS.noktalar.filter((n) => modda(n, m));
              return (
                <button key={m} type="button" role="radio" aria-checked={mod === m} className={`tk-mod-k${mod === m ? ' is-on' : ''}`} title={MOD_ALT[m]}
                  onClick={() => { durdur(); guncelle((k) => ({ ...k, mod: m })); }}>
                  <span className="tk-mod-ad">{m === 'hizli' ? <Zap aria-hidden /> : m === 'yavas' ? <BookOpen aria-hidden /> : <Layers aria-hidden />}{MOD_AD[m]}</span>
                  <span className="tk-mod-say">{N.length} adım · {N.reduce((t, n) => t + modSorulari(n, m).length, 0)} soru · ~{sure[m]} dk</span>
                </button>
              );
            })}
          </div>
          <button type="button" className="tk-btn tk-btn-ana tk-mod-basla" onClick={() => { durdur(); setTamEkran(mod); }}>
            <Play aria-hidden /> Asistanla başla
          </button>
        </section>
      )}

      {sekme === 'ders' && (
        <div className="tk-ust-satir">
          <details className="tk-harita">
            <summary className="tk-harita-bas">
              <span className="tk-ust">Son yılların çıkmışları nereden geliyor</span>
              <span className="tk-harita-top"><b>{tumSorular.filter((x) => x.s.tur === 'cikmis').length}</b> çıkmış · <b>{tumSorular.filter((x) => x.s.tur === 'ornek').length}</b> kalıba uygun örnek</span>
            </summary>
            <ul>
              {cikmisDagilim.map((d) => (
                <li key={d.ad}><span>{d.ad}</span><i style={{ ['--w' as string]: `${(d.n / enCok) * 100}%` }} /><b className="tk-mono">{d.n}</b></li>
              ))}
            </ul>
          </details>
          <span className="tk-ilerleme">
            <span>{bitenAdim}/{adimlar.length} adım</span>
            <span>{dogruSay}/{cevapSay || 0} doğru</span>
            <button type="button" className="tk-metin-btn" onClick={sifirla} title="İlerlemeyi sıfırla"><RotateCcw aria-hidden /></button>
          </span>
        </div>
      )}
      {sekme === 'kalip' && (
        <div className="tk-ust-satir">
          <p className="tk-kalip-not">Hocanın kalıbı: <b>bulgudan sendrom</b> · <b>kanserde hedef ilaç</b> · <b>spesifik belirteç</b></p>
          <MetinAktarMenu belge={belge} dosyaAdi={`tbg-sinav-kampi-${mod}`} dugmeSinif="tk-btn" etiket="Özeti indir" />
        </div>
      )}

      {sekme === 'ders' && nokta && (
        <div className="tk-ders">
          <aside className="tk-liste" aria-label="Adımlar">
            {DERS.bolumler.map((b, bi) => {
              const N = adimlar.map((n, i) => ({ n, i })).filter((x) => x.n.bolum === bi);
              if (!N.length) return null;
              return (
                <div key={bi} className="tk-liste-b">
                  <span className="tk-liste-bas">{bi + 1}. {b.baslik.split(':')[0]}</span>
                  {N.map(({ n, i }) => (
                    <button key={n.id} type="button" className={`tk-liste-o${i === idx ? ' is-on' : ''}${kayit.tamam[n.id] ? ' is-bitti' : ''}`} onClick={() => git(i)}>
                      <span className="tk-liste-no">{kayit.tamam[n.id] ? <Check aria-hidden /> : i + 1}</span>
                      <span className="tk-liste-ad">{n.baslik}</span>
                      {n.sorular.some((s) => s.tur === 'cikmis') && <span className="tk-cik" title="Çıkmış sorusu var">Ç</span>}
                    </button>
                  ))}
                </div>
              );
            })}
          </aside>

          <article className="tk-kart" ref={kartRef}>
            <div className="tk-kart-ust">
              <span className="tk-ust">{nokta.bolum + 1}. bölüm · {DERS.bolumler[nokta.bolum]?.baslik.split(':')[0]} · adım {idx + 1}/{adimlar.length}</span>
              <span className={`tk-kat tk-kat-${nokta.kategori}`}>{KATEGORI[nokta.kategori] || nokta.kategori}</span>
            </div>
            <h2>{nokta.baslik}</h2>
            {adimlar.findIndex((x) => x.bolum === nokta.bolum) === idx && <p className="tk-neden">{DERS.bolumler[nokta.bolum]?.neden}</p>}

            <div className="tk-oynat">
              {calan && /^[ab]-/.test(calan.id) ? (
                <button type="button" className="tk-btn tk-btn-ana" onClick={duraklat}>{calan.oynuyor ? <Pause aria-hidden /> : <Play aria-hidden />}{calan.oynuyor ? 'Duraklat' : 'Devam et'}</button>
              ) : (
                <button type="button" className="tk-btn tk-btn-ana" onClick={() => anlat(idx)} disabled={!DERS.klip[`a-${nokta.id}`]}><Volume2 aria-hidden /> Sesli anlat</button>
              )}
              <label className="tk-hiz">Hız
                <select value={kayit.hiz} onChange={(e) => guncelle((k) => ({ ...k, hiz: Number(e.target.value) }))}>
                  {HIZLAR.map((h) => <option key={h} value={h}>{h}×</option>)}
                </select>
              </label>
              <label className="tk-oto"><input type="checkbox" checked={kayit.oto} onChange={(e) => guncelle((k) => ({ ...k, oto: e.target.checked }))} /> Soruyu oku, doğruysa sonraki adıma geç</label>
            </div>

            <ol className="tk-anlatim">
              {nokta.cumleler.map((c, i) => (
                <li key={i} className={calan?.id === `a-${nokta.id}` && calan.cumle === i ? 'is-on' : ''}>
                  <button type="button" onClick={() => anlat(idx, i)} title="Buradan dinle"><Zengin t={c} /></button>
                </li>
              ))}
            </ol>

            <div className="tk-sorular">
              {modSorulari(nokta, mod).map((s, si) => (
                <SoruKart key={s.k} s={s} no={si + 1} secim={kayit.cevap[s.k]} yardimAcik={!!yardim[s.k]}
                  onSec={(h) => sec(nokta, s, h, true)} onOku={() => cal(`q-${s.k}`)}
                  onYardim={() => { setYardim((y) => ({ ...y, [s.k]: true })); cal(`h-${s.k}`); }}
                  onTekrar={() => guncelle((k) => { const c = { ...k.cevap }; delete c[s.k]; return { ...k, cevap: c }; })} />
              ))}
            </div>

            <div className="tk-gezin">
              <button type="button" className="tk-btn" onClick={() => git(idx - 1)} disabled={idx === 0}><ChevronLeft aria-hidden /> Önceki</button>
              {idx < adimlar.length - 1 ? (
                <button type="button" className="tk-btn tk-btn-ana" onClick={() => { guncelle((k) => ({ ...k, tamam: { ...k.tamam, [nokta.id]: 1 } })); git(idx + 1, calan !== null); }}>Sonraki adım <ChevronRight aria-hidden /></button>
              ) : (
                <button type="button" className="tk-btn tk-btn-ana" onClick={() => { durdur(); guncelle((k) => ({ ...k, tamam: { ...k.tamam, [nokta.id]: 1 } })); setSekme('deneme'); }}>Bitir, denemeye geç <ChevronRight aria-hidden /></button>
              )}
            </div>
            {idx === adimlar.length - 1 && DERS.kapanis.length > 0 && (
              <div className="tk-kapanis">
                <span className="tk-ust">Sınava girerken</span>
                <ul>{DERS.kapanis.map((c, i) => <li key={i}><Zengin t={c} /></li>)}</ul>
              </div>
            )}
          </article>
        </div>
      )}

      {sekme === 'kalip' && <KalipKartlari mod={mod} />}
      {sekme === 'deneme' && <Deneme mod={mod} havuz={adimlar} cal={cal} durdur={durdur} />}

      {tamEkran && <PatolojiAsistan key={tamEkran} kod={DERS.kod} suz={tamEkran === 'hizli' ? hizliSuz : tamEkran === 'yavas' ? yavasSuz : undefined} onClose={() => setTamEkran(null)} />}
    </div>
  );
};

/* ——— soru kartı ——— */
function SoruKart({ s, no, secim, yardimAcik, onSec, onOku, onYardim, onTekrar }: {
  s: Soru; no: number; secim?: string; yardimAcik: boolean; onSec: (h: string) => void; onOku: () => void; onYardim: () => void; onTekrar: () => void;
}) {
  const bitti = !!secim;
  return (
    <section className="tk-soru">
      <div className="tk-soru-ust">
        <span className={`tk-etiket${s.tur === 'cikmis' ? ' is-cik' : ''}`}>{s.tur === 'cikmis' ? `Çıkmış${s.sinav ? ` · ${s.sinav}` : ''}` : 'Kalıba uygun örnek'}</span>
        <span className="tk-soru-arac">
          <button type="button" className="tk-metin-btn" onClick={onOku} title="Soruyu sesli oku"><Volume2 aria-hidden /></button>
          {bitti && <button type="button" className="tk-metin-btn" onClick={onTekrar} title="Yeniden çöz"><RotateCcw aria-hidden /></button>}
        </span>
      </div>
      <p className="tk-kok"><span className="tk-mono">{no}.</span> {s.kok}</p>
      <ul className="tk-siklar">
        {harfler(s).map((h) => {
          const durum = !bitti ? '' : h === s.dogru ? ' is-dogru' : h === secim ? ' is-yanlis' : ' is-sonuk';
          return (
            <li key={h}>
              <button type="button" className={`tk-sik${durum}`} disabled={bitti} onClick={() => onSec(h)}>
                <span className="tk-harf">{h}</span><span>{s.secenekler[h]}</span>
                {bitti && h === s.dogru && <Check aria-hidden className="tk-sik-ic" />}
                {bitti && h === secim && h !== s.dogru && <X aria-hidden className="tk-sik-ic" />}
              </button>
              {yardimAcik && s.yardim[h] && <p className="tk-yardim"><Zengin t={s.yardim[h]} /></p>}
            </li>
          );
        })}
      </ul>
      {bitti && (
        <p className={`tk-geri${secim === s.dogru ? ' is-dogru' : ' is-yanlis'}`}>
          <Zengin t={secim === s.dogru ? s.dogruMetin : s.yanlis[secim!] || s.dogruMetin} />
        </p>
      )}
      {!yardimAcik && <button type="button" className="tk-metin-btn tk-yardim-btn" onClick={onYardim}><LifeBuoy aria-hidden /> Yardım al: her şıkkı açıkla</button>}
    </section>
  );
}

/* ——— kalıp kartları ——— */
function KalipKartlari({ mod }: { mod: Mod }) {
  const [ara, setAra] = useState('');
  const [gizle, setGizle] = useState(false);
  const [acik, setAcik] = useState<Record<string, boolean>>({});
  const q = ara.trim().toLocaleLowerCase('tr');
  return (
    <div className="tk-kalip">
      <div className="tk-kalip-arac">
        <label className="tk-ara"><Search aria-hidden /><input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Bulgu, sendrom, ilaç, gen ara" /></label>
        <button type="button" className={`tk-btn${gizle ? ' is-on' : ''}`} aria-pressed={gizle} onClick={() => { setGizle((g) => !g); setAcik({}); }}>
          {gizle ? <Eye aria-hidden /> : <EyeOff aria-hidden />}{gizle ? 'Cevapları göster' : 'Cevapları gizle, kendini sına'}
        </button>
      </div>
      {KALIPLAR.map((k) => {
        const R = k.satir.filter((r) => (mod !== 'hizli' || r.h) && (!q || `${r.s} ${r.t}`.toLocaleLowerCase('tr').includes(q)));
        if (!R.length) return null;
        return (
          <section key={k.id} className="tk-kalip-k">
            <header><h3>{k.baslik}</h3><span>{k.soru}</span></header>
            <div className="tk-tablo" role="table">
              <div className="tk-tablo-s tk-tablo-bas" role="row"><span role="columnheader">{k.sutun[0]}</span><span role="columnheader">{k.sutun[1]}</span></div>
              {R.map((r, i) => {
                const id = `${k.id}-${i}`;
                const goster = !gizle || acik[id];
                return (
                  <div key={id} className="tk-tablo-s" role="row">
                    <span role="cell">{r.s}</span>
                    <span role="cell">
                      {goster ? <><b>{r.t}</b><small className="tk-mono">{r.k}</small></> : (
                        <button type="button" className="tk-gizli" onClick={() => setAcik((a) => ({ ...a, [id]: true }))}>Göster</button>
                      )}
                    </span>
                  </div>
                );
              })}
            </div>
          </section>
        );
      })}
    </div>
  );
}

/* ——— 12 soruluk deneme ——— */
function Deneme({ mod, havuz, cal, durdur }: { mod: Mod; havuz: Nokta[]; cal: (id: string, b?: () => void) => void; durdur: () => void }) {
  const [set, setSet] = useState<Soru[] | null>(null);
  const [cevap, setCevap] = useState<Record<string, string>>({});
  const [yardim, setYardim] = useState<Record<string, boolean>>({});
  const [i, setI] = useState(0);
  const basla = () => {
    durdur();
    // Çıkmışlar önce: 12 sorunun en az 8'i çıkmış, kalan kalıba uygun örnek; bölümler dengeli dağılır
    const tum = havuz.flatMap((n) => n.sorular);
    const karis = <T,>(a: T[]) => a.map((x) => [Math.random(), x] as const).sort((p, r) => p[0] - r[0]).map((x) => x[1]);
    const cik = karis(tum.filter((s) => s.tur === 'cikmis'));
    const orn = karis(tum.filter((s) => s.tur === 'ornek'));
    const secilen = [...cik.slice(0, 8), ...orn].slice(0, 12);
    setSet(karis(secilen.length < 12 ? [...secilen, ...cik.slice(8)].slice(0, 12) : secilen));
    setCevap({}); setYardim({}); setI(0);
  };
  if (!set) {
    return (
      <div className="tk-deneme-giris">
        <h3>Sınav provası</h3>
        <p>{MOD_AD[mod]} adımlarından rastgele 12 soru: çoğu son yılların çıkmışı, kalanı hocanın kalıbına uygun örnek. Her yanlışta neden yanlış olduğu sesli anlatılır.</p>
        <button type="button" className="tk-btn tk-btn-ana" onClick={basla}><Shuffle aria-hidden /> 12 soruyu başlat</button>
      </div>
    );
  }
  const s = set[i];
  const bitti = set.every((x) => cevap[x.k]);
  const dogru = set.filter((x) => cevap[x.k] === x.dogru).length;
  return (
    <div className="tk-deneme">
      <div className="tk-deneme-ust">
        <div className="tk-nokta" role="tablist" aria-label="Sorular">
          {set.map((x, j) => (
            <button key={x.k} type="button" aria-label={`${j + 1}. soru`} className={`${j === i ? 'is-on' : ''}${cevap[x.k] ? (cevap[x.k] === x.dogru ? ' is-dogru' : ' is-yanlis') : ''}`} onClick={() => { durdur(); setI(j); }}>{j + 1}</button>
          ))}
        </div>
        {bitti && <span className="tk-skor"><b>{dogru}</b>/12 doğru</span>}
      </div>
      <SoruKart s={s} no={i + 1} secim={cevap[s.k]} yardimAcik={!!yardim[s.k]}
        onSec={(h) => { setCevap((c) => ({ ...c, [s.k]: h })); cal(h === s.dogru ? `d-${s.k}` : `y-${s.k}-${h}`); }}
        onOku={() => cal(`q-${s.k}`)} onYardim={() => { setYardim((y) => ({ ...y, [s.k]: true })); cal(`h-${s.k}`); }}
        onTekrar={() => setCevap((c) => { const d = { ...c }; delete d[s.k]; return d; })} />
      <div className="tk-gezin">
        <button type="button" className="tk-btn" onClick={() => { durdur(); setI(i - 1); }} disabled={i === 0}><ChevronLeft aria-hidden /> Önceki</button>
        {i < 11 ? <button type="button" className="tk-btn tk-btn-ana" onClick={() => { durdur(); setI(i + 1); }}>Sonraki <ChevronRight aria-hidden /></button>
          : <button type="button" className="tk-btn tk-btn-ana" onClick={basla}><Shuffle aria-hidden /> Yeni 12 soru</button>}
      </div>
    </div>
  );
}

export default GenetikCheckUp;
