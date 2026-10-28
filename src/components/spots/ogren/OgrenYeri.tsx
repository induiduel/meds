import React, { useEffect, useMemo, useRef, useState } from 'react';
import { BookOpenText, ChevronLeft, ChevronRight, ExternalLink, Locate, X } from 'lucide-react';
import { DECK_CATALOG, loadDeck, loadDeckCatalog } from '../../../data/deckStore';
import type { InteractiveDeck } from '../../learn/InteractiveDeckView';
import { buildSteps, inline, mdToHtml, stripEmoji, type LessonStep } from '../../learn/lesson/lessonModel';
import { navigateTo } from '../../../router';
import type { Brans } from '../brans';
import { ogrenYerleri, type OgrenYer } from './ogrenEsle';
import '../../../styles/ogren-ders.css';
import '../../../styles/ogren-yeri.css';
// Katalog tembel yüklenir; bu modül eşzamanlı okuduğundan yüklenirken hazır olmasını bekle.
await loadDeckCatalog().catch(() => undefined);

/**
 * "Öğren'de bu yer" paneli: sesli çözücüdeki soru (ya da sesli asistan noktası) için Öğren destesindeki eşleşen adımı
 * çözücüden çıkmadan gösterir. Geniş ekranda sağda yan panel (çözücü daralır), telefonda alttan açılan sayfa.
 * İçerik kendi içinde kayar; önceki/sonraki adıma geçilebilir, "Eşleşen adıma dön" ile geri gelinir, "Öğren'de aç" tam derse gider.
 * Eşleme: scripts/spot_cozucu/ogren_esle.py (PDF sayfası + metin benzerliği; kanıt zayıfsa eşleme yok → panel bunu söyler).
 */
interface Props {
  brans: Brans;
  kod: string;
  tur: 's' | 'n';
  id: string | number | undefined;
  /** başlıktaki bağlam, ör. "Soru 12" */
  baglam?: string;
  onKapat: () => void;
}

const katalog = (id: string) => DECK_CATALOG.find((d) => d.id === id);
const desteAdi = (id: string) => {
  const d = katalog(id);
  return stripEmoji(String(d?.shortTitle || d?.title || id));
};
const surumAdi = (id: string) => String(katalog(id)?.versionLabel || '');

const Adim: React.FC<{ s: LessonStep }> = ({ s }) => {
  const anlatim = useMemo(() => mdToHtml(s.narrative), [s.narrative]);
  return (
    <>
      <h3 className="oy-baslik">{s.title}</h3>
      {s.narrative && <div className="oy-metin" dangerouslySetInnerHTML={{ __html: anlatim }} />}
      {s.bullets.length > 0 && (
        <ul className="oy-maddeler">
          {s.bullets.map((b, k) => (
            <li key={k} className={b.isKey ? 'is-anahtar' : undefined}>
              {b.title && <b dangerouslySetInnerHTML={{ __html: inline(b.title) }} />}
              {b.desc && <span dangerouslySetInnerHTML={{ __html: inline(b.desc) }} />}
            </li>
          ))}
        </ul>
      )}
      {s.table && (
        <div className="ls-table oy-tablo">
          {s.table.title && <b className="oy-tablo-b">{s.table.title}</b>}
          <table>
            <thead><tr>{s.table.headers.map((h, k) => <th key={k} dangerouslySetInnerHTML={{ __html: inline(String(h)) }} />)}</tr></thead>
            <tbody>{s.table.rows.map((r, k) => (
              <tr key={k}>{r.map((c, j) => <td key={j} dangerouslySetInnerHTML={{ __html: inline(typeof c === 'string' ? c : String((c as { text?: string })?.text ?? '')) }} />)}</tr>
            ))}</tbody>
          </table>
        </div>
      )}
      {(s.important || s.examTip) && (
        <aside className="ls-note is-warn">
          <span className="ls-note-k">{s.examTip ? 'Sınav spotu' : 'Önemli'}</span>
          <p dangerouslySetInnerHTML={{ __html: inline(String(s.examTip || s.important)) }} />
        </aside>
      )}
      {s.spots.length > 0 && (
        <ul className="oy-spotlar" aria-label="Spot bilgiler">
          {s.spots.map((x, k) => <li key={k} dangerouslySetInnerHTML={{ __html: inline(x) }} />)}
        </ul>
      )}
    </>
  );
};

export const OgrenYeri: React.FC<Props> = ({ brans, kod, tur, id, baglam, onKapat }) => {
  const [yerler, setYerler] = useState<OgrenYer[] | null>(null);
  const [sec, setSec] = useState(0);
  const [deste, setDeste] = useState<{ id: string; adimlar: LessonStep[] } | null>(null);
  const [hata, setHata] = useState(false);
  const [konum, setKonum] = useState(0);
  const govde = useRef<HTMLDivElement>(null);
  const kapatRef = useRef<HTMLButtonElement>(null);

  useEffect(() => { kapatRef.current?.focus({ preventScroll: true }); }, []);
  useEffect(() => {
    let canli = true;
    setYerler(null);
    setSec(0);
    if (id == null) { setYerler([]); return; }
    ogrenYerleri(brans, kod, tur, id).then((l) => { if (canli) setYerler(l); }).catch(() => { if (canli) setYerler([]); });
    return () => { canli = false; };
  }, [brans, kod, tur, id]);

  const yer = yerler?.[sec];
  useEffect(() => {
    if (!yer) return;
    let canli = true;
    setHata(false);
    if (deste?.id !== yer.deck) setDeste(null);
    loadDeck<InteractiveDeck>(yer.deck)
      .then((d) => {
        if (!canli) return;
        if (!d) { setHata(true); return; }
        setDeste({ id: yer.deck, adimlar: buildSteps(d) });
      })
      .catch(() => { if (canli) setHata(true); });
    return () => { canli = false; };
  }, [yer?.deck]); // eslint-disable-line react-hooks/exhaustive-deps

  const hedef = useMemo(() => {
    if (!deste || !yer || deste.id !== yer.deck) return -1;
    const k = deste.adimlar.findIndex((s) => s.number === yer.slayt);
    return k >= 0 ? k : 0;
  }, [deste, yer]);
  useEffect(() => { if (hedef >= 0) setKonum(hedef); }, [hedef]);
  useEffect(() => { govde.current?.scrollTo({ top: 0 }); }, [konum, deste?.id]);

  const adim = deste && hedef >= 0 ? deste.adimlar[konum] : undefined;
  const n = deste?.adimlar.length || 0;
  const git = (d: number) => setKonum((k) => Math.max(0, Math.min(n - 1, k + d)));
  const uzak = adim && konum !== hedef ? konum - hedef : 0;

  const tus = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') { e.preventDefault(); onKapat(); return; }
    if ((e.target as HTMLElement).closest('input,textarea,select')) return;
    if (e.key === 'ArrowRight' && !e.altKey) { e.preventDefault(); git(1); }
    if (e.key === 'ArrowLeft' && !e.altKey) { e.preventDefault(); git(-1); }
  };

  return (
    <aside className="oy" aria-label="Öğren'deki karşılığı" onKeyDown={tus}>
      <header className="oy-ust">
        <span className="oy-ikon" aria-hidden><BookOpenText /></span>
        <div className="oy-ust-t">
          <small>Öğren'de bu bilgi{baglam ? ` · ${baglam}` : ''}</small>
          <b>{yer ? desteAdi(yer.deck) : id == null ? 'Bilgi noktası bekleniyor' : yerler === null ? 'Aranıyor…' : 'Eşleşen adım yok'}</b>
        </div>
        <button ref={kapatRef} type="button" className="oy-kapat" onClick={onKapat} aria-label="Öğren panelini kapat" title="Kapat (Esc)"><X /></button>
      </header>

      {yerler && yerler.length > 1 && (
        <div className="oy-secim" role="group" aria-label="Eşleşen dersler">
          {yerler.map((y, k) => (
            <button key={`${y.deck}-${y.slayt}`} type="button" className={`oy-cip${k === sec ? ' is-on' : ''}`} aria-pressed={k === sec} onClick={() => setSec(k)}
              title={`${desteAdi(y.deck)} · adım ${y.slayt}`}>
              {surumAdi(y.deck) || desteAdi(y.deck)}<span>adım {y.slayt}</span>
            </button>
          ))}
        </div>
      )}

      <div className="oy-govde" ref={govde} tabIndex={0} aria-live="polite">
        {yerler === null && <p className="oy-bos">Öğren'deki yeri aranıyor…</p>}
        {id == null && <p className="oy-bos">Anlatım bir bilgi noktasına gelince o bilginin Öğren'deki yeri burada açılır.</p>}
        {id != null && yerler && !yerler.length && (
          <p className="oy-bos">Bu {tur === 's' ? 'soru' : 'bilgi'} için Öğren'de güvenilir bir eşleşme bulunamadı. Yanlış adım göstermemek için boş bırakıldı.</p>
        )}
        {yer && hata && <p className="oy-bos">Ders yüklenemedi. Bağlantını kontrol edip yeniden dene.</p>}
        {yer && !hata && !adim && <p className="oy-bos">Ders açılıyor…</p>}
        {adim && (
          <>
            {uzak !== 0 && (
              <button type="button" className="oy-uzak" onClick={() => setKonum(hedef)}>
                <Locate aria-hidden />Eşleşen adımdan {Math.abs(uzak)} adım {uzak > 0 ? 'ileridesin' : 'geridesin'} · geri dön
              </button>
            )}
            <div className="oy-adim-no">Adım {adim.number}{konum === hedef ? <em>eşleşen yer</em> : null}</div>
            <Adim s={adim} />
          </>
        )}
      </div>

      {adim && (
        <footer className="oy-alt">
          <button type="button" className="oy-btn" onClick={() => git(-1)} disabled={konum <= 0} aria-label="Önceki adım"><ChevronLeft aria-hidden /><span>Önceki</span></button>
          <span className="oy-sayac">{konum + 1} / {n}</span>
          <button type="button" className="oy-btn" onClick={() => git(1)} disabled={konum >= n - 1} aria-label="Sonraki adım"><span>Sonraki</span><ChevronRight aria-hidden /></button>
          <button type="button" className="oy-btn is-dolu" onClick={() => navigateTo(`/ogren/${deste!.id}?adim=${adim.number}`)} title="Dersi bu adımda Öğren'de aç">
            <ExternalLink aria-hidden /><span>Öğren'de aç</span>
          </button>
        </footer>
      )}
    </aside>
  );
};

export default OgrenYeri;
