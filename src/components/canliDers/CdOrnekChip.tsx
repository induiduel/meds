// Sesli derste örnek soru chip'i (kullanıcı kararı 2026-10-29): bir bölümün/parçanın son slaytında, çıkmış chip'inin
// altında görünür; dokununca ses durur, o parçaya ait (ya da buraya kadarki) örnek sorular çözülür, kapanınca ders
// kaldığı yerden sürer. Sorular `src/data/ornek_sorular/k<N>/<ders>.json` içindeki `kanit.sayfa` ile slayta bağlanır.
import React, { useEffect, useSyncExternalStore, useState } from 'react';
import { createPortal } from 'react-dom';
import { ChevronLeft, ChevronRight, ListChecks, Play, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { dersSoruKaydet } from '../../services/calismaTakip';
import { cdDurum, cdDuraklat, cdToggle, type CdDetay } from './canliDersStore';

interface OrnekSoru {
  id: string; soru: string; secenekler: Record<string, string>; dogru: string; aciklama?: string;
  sik_aciklamalari?: Record<string, string>; kanit?: { sayfa?: number; alinti?: string }; bilgi?: number[];
}
interface OrnekDers { kazanimlar?: { sorular?: OrnekSoru[] }[] }
type IndexRow = { id: string };

const indexModules = import.meta.glob('../../data/ornek_sorular/k[1-6]/index.json', { eager: true, import: 'default' }) as Record<string, IndexRow[]>;
const loaders = import.meta.glob('../../data/ornek_sorular/k[1-6]/k[1-6]-*.json', { import: 'default' }) as Record<string, () => Promise<OrnekDers>>;
const INDEX: IndexRow[] = Object.keys(indexModules).flatMap((k) => indexModules[k] || []);

const onbellek = new Map<string, Promise<OrnekSoru[]>>();
/** Sesli ders anahtarına (k2-07) karşılık gelen örnek soru dosyasını yükler; yoksa boş liste */
export function ornekSorulariYukle(key: string): Promise<OrnekSoru[]> {
  let p = onbellek.get(key);
  if (p) return p;
  const satir = INDEX.find((r) => r.id === key) || INDEX.find((r) => r.id.startsWith(`${key}-`));
  const kurul = /^k(\d)-/.exec(key)?.[1];
  p = (async () => {
    if (!satir || !kurul) return [];
    try {
      const yukle = loaders[`../../data/ornek_sorular/k${kurul}/${satir.id}.json`];
      let d: OrnekDers | null = null;
      if (yukle) d = await yukle();
      else {
        const r = await safeJsonFetch<OrnekDers>(`/api/content/ornek/k${kurul}/${satir.id}`, { cache: 'no-store' });
        if (r.ok && r.data) d = r.data;
      }
      return (d?.kazanimlar || []).flatMap((k) => k.sorular || []);
    } catch { return []; }
  })();
  onbellek.set(key, p);
  return p;
}

/** Bölümlerin son slaytı: [dosya, sayfa] (bölümün paragraflarının eşlendiği en ileri sayfa) */
function bolumSonlari(d: CdDetay): ([number, number] | null)[] {
  const esl = d.pdf?.paragraflar || [];
  return d.bolumler.map((b) => {
    let son: [number, number] | null = null;
    for (const p of b.paragraflar) {
      const e = esl[p.i];
      if (!e) continue;
      for (const s of [e.sayfa, ...(e.sayfalar || [])]) {
        const dsy = e.dosya ?? 0;
        if (!son || dsy > son[0] || (dsy === son[0] && s > son[1])) son = [dsy, s];
      }
    }
    return son;
  });
}

export interface OrnekParca { bu: OrnekSoru[]; kadar: OrnekSoru[]; no: number }
/** (dosya, sayfa) bir bölümün son slaytıysa o parçanın örnek soruları: `bu` = yalnız bu parçanın sayfaları, `kadar` = baştan buraya */
export function ornekParcaSonunda(detay: CdDetay, sorular: OrnekSoru[], dosya: number, sayfa: number): OrnekParca | null {
  if (!sorular.length || (detay.pdf?.dosyalar?.length ?? 1) > 1 && dosya !== 0) return null;
  const sonlar = bolumSonlari(detay);
  let bi = -1;
  sonlar.forEach((s, i) => { if (s && s[0] === dosya && s[1] === sayfa) bi = i; });
  if (bi < 0) return null;
  // Bölüm sonunda bir sonraki bölümün de aynı sayfada bitmesi (sonraki tek sayfa) bu bölümü ezmesin: son eşleşme kazanır
  let onceki = 0;
  for (let i = bi - 1; i >= 0; i--) { const s = sonlar[i]; if (s && s[0] === dosya) { onceki = s[1]; break; } }
  const sf = (q: OrnekSoru) => q.kanit?.sayfa ?? Math.max(0, ...(q.bilgi || [0]));
  const kadar = sorular.filter((q) => sf(q) > 0 && sf(q) <= sayfa);
  const bu = kadar.filter((q) => sf(q) > onceki);
  if (!kadar.length) return null;
  return { bu: bu.length ? bu : kadar, kadar, no: bi + 1 };
}

type Acik = { parca: OrnekParca; caliyordu: boolean } | null;
let acikDurum: Acik = null;
const dinleyiciler = new Set<() => void>();
const ayarla = (a: Acik) => { acikDurum = a; dinleyiciler.forEach((f) => f()); };
const abone = (f: () => void) => { dinleyiciler.add(f); return () => { dinleyiciler.delete(f); }; };

/** Ders anahtarının örnek sorularını bir kez yükler (hook) */
export function useOrnekSorular(key: string): OrnekSoru[] {
  const [s, setS] = useState<OrnekSoru[]>([]);
  useEffect(() => {
    let iptal = false;
    ornekSorulariYukle(key).then((x) => { if (!iptal) setS(x); });
    return () => { iptal = true; };
  }, [key]);
  return s;
}

export function CdOrnekChip({ parca }: { parca: OrnekParca | null }) {
  if (!parca) return null;
  const ac = (e: React.MouseEvent) => {
    e.stopPropagation();
    const caliyor = cdDurum().playing;
    if (caliyor) cdDuraklat();
    ayarla({ parca, caliyordu: caliyor });
  };
  return (
    <button type="button" className="cd-cikc cd-ornc" onClick={ac} onPointerDown={(e) => e.stopPropagation()}
      title="Bu parçaya ait örnek soruları çöz — dokun">
      <ListChecks aria-hidden /> Örnek soru {parca.bu.length}
    </button>
  );
}

/** Ders ekranında bir kez bulunur; açık örnek soru kartını belge köküne çizer. */
export function CdOrnekPencereKok() {
  const a = useSyncExternalStore(abone, () => acikDurum);
  useEffect(() => () => ayarla(null), []);
  if (!a) return null;
  const kapat = () => {
    ayarla(null);
    if (a.caliyordu && !cdDurum().playing) cdToggle();
  };
  return createPortal(<OrnekKart parca={a.parca} onKapat={kapat} />, document.body);
}

function OrnekKart({ parca, onKapat }: { parca: OrnekParca; onKapat: () => void }) {
  const [kapsam, setKapsam] = useState<'bu' | 'kadar'>('bu');
  const [i, setI] = useState(0);
  const [secim, setSecim] = useState<string | null>(null);
  const liste = parca[kapsam];
  const q = liste[Math.min(i, liste.length - 1)];
  useEffect(() => { setSecim(null); }, [q?.id]);
  useEffect(() => {
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') onKapat(); };
    window.addEventListener('keydown', k);
    return () => window.removeEventListener('keydown', k);
  }, [onKapat]);
  if (!q) return null;
  const cozuldu = secim != null;
  const dogru = cozuldu && secim === q.dogru;
  const git = (n: number) => { setI(n); };
  return (
    <div className="cd15-cq-kat" role="presentation" onClick={onKapat}>
      <div className="cd15-cq" role="dialog" aria-modal="true" aria-label="Örnek soru" onClick={(e) => e.stopPropagation()}>
        <div className="cd15-cq-bas">
          <span className="cd15-cq-et"><ListChecks aria-hidden /> Örnek soru</span>
          <span className="cd15-cq-no">{Math.min(i, liste.length - 1) + 1}/{liste.length}</span>
          {liste.length > 1 && <button type="button" className="v15-ib" disabled={i <= 0} onClick={() => git(i - 1)} aria-label="Önceki soru"><ChevronLeft aria-hidden /></button>}
          {liste.length > 1 && <button type="button" className="v15-ib" disabled={i >= liste.length - 1} onClick={() => git(i + 1)} aria-label="Sonraki soru"><ChevronRight aria-hidden /></button>}
          <button type="button" className="v15-ib" onClick={onKapat} aria-label="Kapat ve derse dön"><X aria-hidden /></button>
        </div>
        {parca.kadar.length > parca.bu.length && (
          <div className="cd-orn-kapsam" role="radiogroup" aria-label="Soru kapsamı">
            <button type="button" role="radio" aria-checked={kapsam === 'bu'} className={kapsam === 'bu' ? 'is-on' : ''} onClick={() => { setKapsam('bu'); setI(0); }}>Bu parça ({parca.bu.length})</button>
            <button type="button" role="radio" aria-checked={kapsam === 'kadar'} className={kapsam === 'kadar' ? 'is-on' : ''} onClick={() => { setKapsam('kadar'); setI(0); }}>Buraya kadar ({parca.kadar.length})</button>
          </div>
        )}
        <div className="cd15-cq-govde">
          <p className="cd15-cq-kok">{q.soru}</p>
          <div className="cd15-cq-siklar" role="radiogroup" aria-label="Şıklar">
            {Object.entries(q.secenekler).map(([k, m]) => {
              const d = k === q.dogru;
              const cls = !cozuldu ? '' : d ? ' is-dogru' : k === secim ? ' is-yanlis' : ' is-soluk';
              const ac = q.sik_aciklamalari?.[k];
              return (
                <button key={k} type="button" role="radio" aria-checked={k === secim} disabled={cozuldu} className={`cd15-cq-sik${cls}`}
                  onClick={() => { setSecim(k); dersSoruKaydet(cdDurum().key, 'ornek', q.id); }}>
                  <b>{k}</b>
                  <span>{m}{cozuldu && ac && (d || k === secim) && <small>{ac}</small>}</span>
                </button>
              );
            })}
          </div>
          {cozuldu && (
            <div className="cd15-cq-sonuc">
              <b className={dogru ? 'is-dogru' : 'is-yanlis'}>{dogru ? 'Doğru' : `Yanlış · doğru cevap ${q.dogru}`}</b>
              {q.aciklama && <p>{q.aciklama}</p>}
              {q.kanit?.alinti && <p className="cd15-cq-kanit">Slayttaki dayanak (sayfa {q.kanit.sayfa}): “{q.kanit.alinti}”</p>}
            </div>
          )}
        </div>
        <div className="cd15-cq-alt">
          <span className="cd15-cq-not">{cozuldu ? '' : 'Ses duraklatıldı; işin bitince kaldığın yerden sürer.'}</span>
          {cozuldu && i < liste.length - 1 && <button type="button" className="v15-btn is-soft" onClick={() => git(i + 1)}>Sonraki</button>}
          <button type="button" className={`v15-btn${cozuldu ? '' : ' is-soft'}`} onClick={onKapat}><Play aria-hidden /> Derse dön</button>
        </div>
      </div>
    </div>
  );
}
