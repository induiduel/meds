// Sesli ders öncesi "Ders analizi" (kullanıcı kararı 2026-10-29): derste ne anlatılacak, bilinmesi gerekenler, en önemli
// yerler, çıkmış sorularda ne soruldu, hocanın soru üslubu ve nelere odaklanılmalı. Aynı pencerede "Ders özeti" sekmesi:
// dersin içerikleri (önem listesi + sesli çözücü) tamamlandıktan sonra onlardan derlenir, en önemli yerleri anlatır.
// Veri: src/data/ders_analizi/<key>.json (scripts/ders_analizi/uret.py, LLM yok). Her bölüm EMA ile dinlenebilir
// (scripts/ders_analizi/ses.py → /api/cozucu-ses/k<N>dersanaliz/ema/<kod>/<klip>.mp3); ders sesi çalıyorsa susturulur.
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { CircleHelp, ClipboardList, ListChecks, Pause, Play, X } from 'lucide-react';
import { cdDurum, cdDuraklat } from './canliDersStore';
import '../../styles/v15/ders_analizi.css';

interface Madde { baslik?: string; metin: string; neden?: string; cevap?: string; s?: number[]; cikmis?: boolean }
interface Bolum { id: string; baslik: string; giris?: string; guven?: string; s?: number[]; cikmis?: boolean; maddeler: Madde[]; klip: string; v: string }
export interface DersAnaliz {
  key: string; kod: string; brans: string; konu: string; ogretim_uyesi?: string;
  sesKlasor: { brans: string; kod: string }; analiz: Bolum[]; ozet: Bolum[] | null; ozetEksik?: string[];
}

const VERI = import.meta.glob('../../data/ders_analizi/*.json', { import: 'default' }) as Record<string, () => Promise<DersAnaliz>>;
const kisaKey = (k: string) => /^k\d-\d{2}/.exec(k)?.[0] || k;
const dosya = (key: string) => VERI[`../../data/ders_analizi/${kisaKey(key)}.json`];

export const dersAnalizVar = (key: string | null | undefined) => !!key && !!dosya(key);

export function useDersAnaliz(key: string | null | undefined, acik: boolean): DersAnaliz | null {
  const [v, setV] = useState<DersAnaliz | null>(null);
  useEffect(() => {
    let iptal = false;
    const f = key && acik ? dosya(key) : undefined;
    if (f) f().then((x) => { if (!iptal) setV(x); }).catch(() => { if (!iptal) setV(null); });
    return () => { iptal = true; };
  }, [key, acik]);
  return v;
}

const sesYolu = (d: DersAnaliz, b: Bolum) =>
  `/api/cozucu-ses/${d.sesKlasor.brans}/ema/${encodeURIComponent(d.sesKlasor.kod)}/${b.klip}.mp3?v=${b.v}`;
const sayfa = (s?: number[]) => (s?.length ? `s. ${s.join(', ')}` : '');

type Sekme = 'analiz' | 'ozet';

export function CdDersAnaliz({ dersKey, baslangic = 'analiz', onKapat }: { dersKey: string; baslangic?: Sekme; onKapat: () => void }) {
  const d = useDersAnaliz(dersKey, true);
  const [sekme, setSekme] = useState<Sekme>(baslangic);
  const [calan, setCalan] = useState<string | null>(null);
  const [sesHata, setSesHata] = useState(false);
  const ses = useRef<HTMLAudioElement | null>(null);
  const sira = useRef<Bolum[]>([]);

  const durdur = useCallback(() => { ses.current?.pause(); sira.current = []; setCalan(null); }, []);

  const cal = useCallback((liste: Bolum[]) => {
    if (!d || !liste.length) return;
    if (cdDurum().playing) cdDuraklat();
    sira.current = liste.slice(1);
    const b = liste[0];
    const a = ses.current || (ses.current = new Audio());
    a.onended = () => { const n = sira.current; n.length ? cal(n) : setCalan(null); };
    a.onerror = () => { setSesHata(true); setCalan(null); sira.current = []; };
    a.src = sesYolu(d, b);
    a.play().then(() => { setCalan(b.id); setSesHata(false); }).catch(() => setCalan(null));
    document.getElementById(`da-${b.id}`)?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }, [d]);

  useEffect(() => {
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') { e.stopPropagation(); onKapat(); } };
    document.addEventListener('keydown', k, true);
    return () => { document.removeEventListener('keydown', k, true); ses.current?.pause(); };
  }, [onKapat]);
  useEffect(durdur, [sekme, durdur]);

  const bolumler = d ? (sekme === 'analiz' ? d.analiz : d.ozet || []) : [];

  return createPortal(
    <div className="da-ort" onClick={(e) => { if (e.target === e.currentTarget) onKapat(); }}>
      <div className="da" role="dialog" aria-modal="true" aria-label={sekme === 'analiz' ? 'Ders analizi' : 'Ders özeti'}>
        <header className="da-bas">
          <div>
            <small>{d ? `${d.brans}${d.ogretim_uyesi ? ` · ${d.ogretim_uyesi}` : ''}` : 'Yükleniyor'}</small>
            <h2>{d?.konu || '…'}</h2>
          </div>
          <button type="button" className="cd-btn is-ikon" onClick={onKapat} aria-label="Kapat" title="Kapat (Esc)"><X aria-hidden /></button>
        </header>

        <div className="da-arac">
          <div className="da-sekme" role="tablist">
            <button type="button" role="tab" aria-selected={sekme === 'analiz'} onClick={() => setSekme('analiz')}><CircleHelp aria-hidden />Ders analizi</button>
            <button type="button" role="tab" aria-selected={sekme === 'ozet'} onClick={() => setSekme('ozet')}><ListChecks aria-hidden />Ders özeti</button>
          </div>
          {bolumler.length > 0 && (
            calan
              ? <button type="button" className="da-dinle is-on" onClick={durdur}><Pause aria-hidden />Durdur</button>
              : <button type="button" className="da-dinle" onClick={() => cal(bolumler)}><Play aria-hidden />Tümünü dinle</button>
          )}
        </div>
        {sesHata && <p className="da-uyari">Bu bölümün sesi henüz hazır değil; metni okuyabilirsin.</p>}

        <div className="da-govde">
          {d && sekme === 'ozet' && !d.ozet && (
            <p className="da-bos">Ders özeti, dersin içerikleri tamamlandıktan sonra onlardan hazırlanır.
              {d.ozetEksik?.length ? ` Henüz eksik: ${d.ozetEksik.join(', ')}.` : ''}</p>
          )}
          {bolumler.map((b, i) => (
            <section key={b.id} id={`da-${b.id}`} className={`da-bolum${calan === b.id ? ' is-calan' : ''}`}>
              <div className="da-bolum-bas">
                <span className="da-no">{i + 1}</span>
                <h3>{b.baslik}{b.cikmis && <em className="da-rozet">çıkmış</em>}{b.s?.length ? <small>{sayfa(b.s)}</small> : null}</h3>
                <button type="button" className="cd-btn is-ikon" aria-label={calan === b.id ? 'Durdur' : `${b.baslik} bölümünü dinle`}
                  onClick={() => (calan === b.id ? durdur() : cal([b]))}>
                  {calan === b.id ? <Pause aria-hidden /> : <Play aria-hidden />}
                </button>
              </div>
              {b.giris && <p className="da-giris">{b.giris}</p>}
              {b.maddeler.length > 0 && (
                <ul>
                  {b.maddeler.map((m, j) => (
                    <li key={j}>
                      {m.baslik && <b>{m.baslik}{m.cikmis && <em className="da-rozet">çıkmış</em>}</b>}
                      <span>{m.metin}</span>
                      {m.cevap && <span className="da-cevap">Cevap: {m.cevap}</span>}
                      {m.neden && <small className="da-neden">{m.neden}</small>}
                      {m.s?.length ? <small className="da-sayfa">{sayfa(m.s)}</small> : null}
                    </li>
                  ))}
                </ul>
              )}
            </section>
          ))}
        </div>
      </div>
    </div>,
    document.body,
  );
}

/** Ders araç çubuğu düğmesi: ders çalarken de analize/özete ulaşılır */
export function CdDersAnalizDugme({ dersKey }: { dersKey: string }) {
  const [acik, setAcik] = useState(false);
  if (!dersAnalizVar(dersKey)) return null;
  return (
    <>
      <button type="button" className="cd-btn is-ikon" onClick={() => setAcik(true)} aria-label="Ders analizi ve ders özeti" title="Ders analizi · ders özeti">
        <ClipboardList aria-hidden />
      </button>
      {acik && <CdDersAnaliz dersKey={dersKey} onKapat={() => setAcik(false)} />}
    </>
  );
}
