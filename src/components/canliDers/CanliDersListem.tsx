/**
 * Canlı ders · "Listem" arayüzü: liste görünümü (liste sayfasında sekme), listeye ekle düğmesi, tekrar seçici ve
 * oynatıcıdaki önceki/sonraki ders denetimi. Durum canliDersListe.ts'tedir.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowDown, ArrowUp, ListCheck, ListMusic, ListPlus, Pause, Play, Repeat, Repeat1, SkipBack, SkipForward, Trash2, X,
} from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import { cdToggle, fmtSure, useCd, type CdListeDers } from './canliDersStore';
import {
  CD_TEKRAR_SAYILAR, cdListeAtla, cdListeCikar, cdListeDegistir, cdListeOynat, cdListeTasi, cdListeTemizle, cdTekrarAyarla,
  tekrarSayiYaz, useCdListe, useCdListeSira, type CdTekrarMod,
} from './canliDersListe';

/* ---------------- listeye ekle ---------------- */

export function ListeEkleDugme({ dersKey, baslik, etiketli }: { dersKey: string; baslik: string; etiketli?: boolean }) {
  const ekli = useCdListe((s) => s.keys.includes(dersKey));
  const ad = ekli ? 'Listemden çıkar' : 'Listeme ekle';
  return (
    <button
      type="button"
      className={`cd-btn${etiketli ? '' : ' is-ikon'}${ekli ? ' is-on' : ''}`}
      onClick={() => cdListeDegistir(dersKey)}
      aria-pressed={ekli}
      aria-label={`${ad}: ${baslik}`}
      title={ad}
    >
      {ekli ? <ListCheck aria-hidden /> : <ListPlus aria-hidden />}
      {etiketli && <span>{ekli ? 'Listemde' : 'Listeme ekle'}</span>}
    </button>
  );
}

/* ---------------- tekrar seçici ---------------- */

const MODLAR: { mod: CdTekrarMod; ad: string; alt: string }[] = [
  { mod: 'kapali', ad: 'Tekrar yok', alt: 'Ders / liste bitince durur' },
  { mod: 'ders', ad: 'Dersi tekrarla', alt: 'Biten ders yeniden çalar' },
  { mod: 'liste', ad: 'Listeyi tekrarla', alt: 'Liste bitince başa döner' },
];

export function TekrarSecici({ yukari = true }: { yukari?: boolean }) {
  const mod = useCdListe((s) => s.mod);
  const sayi = useCdListe((s) => s.sayi);
  // Ders tekrarı sürerken kaçıncı tekrarda olunduğu ("1/3"); ilk çalışta yalnız sayı
  const tur = useCdListe((s) => (s.mod === 'ders' ? s.dersTur : s.mod === 'liste' ? s.listeTur : 0));
  const [acik, setAcik] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!acik) return;
    const dis = (e: PointerEvent) => { if (!ref.current?.contains(e.target as Node)) setAcik(false); };
    const esc = (e: KeyboardEvent) => { if (e.key === 'Escape') { e.stopPropagation(); setAcik(false); } };
    document.addEventListener('pointerdown', dis);
    document.addEventListener('keydown', esc, true);
    requestAnimationFrame(() => ref.current?.querySelector<HTMLElement>('.cd-tk-mod[aria-checked="true"]')?.focus());
    return () => {
      document.removeEventListener('pointerdown', dis);
      document.removeEventListener('keydown', esc, true);
    };
  }, [acik]);
  const ozet = mod === 'kapali' ? 'Tekrar kapalı' : `${mod === 'ders' ? 'Ders' : 'Liste'} tekrarı ${sayi === 0 ? 'sınırsız' : `${sayi} kez`}`;
  const Ikon = mod === 'ders' ? Repeat1 : Repeat;
  return (
    <div className="cd-menu-kap" ref={ref}>
      <button
        type="button"
        className={`cd-ib cd-tk-btn${mod !== 'kapali' ? ' is-on' : ''}`}
        aria-haspopup="dialog"
        aria-expanded={acik}
        onClick={() => setAcik((x) => !x)}
        title={ozet}
        aria-label={`Tekrar: ${ozet}`}
      >
        <Ikon aria-hidden />
        {mod === 'kapali'
          ? <span className="cd-tk-ad">Tekrar</span>
          : <span className="cd-tk-sayi">{tur > 0 ? `${tur}/${sayi === 0 ? '∞' : sayi}` : tekrarSayiYaz(sayi)}</span>}
      </button>
      {acik && (
        <div className={`cd-tk-menu${yukari ? '' : ' is-asagi'}`} role="dialog" aria-label="Tekrar">
          <div role="radiogroup" aria-label="Tekrar türü">
            {MODLAR.map((m) => (
              <button
                key={m.mod}
                type="button"
                role="radio"
                aria-checked={mod === m.mod}
                className="cd-tk-mod"
                onClick={() => cdTekrarAyarla(m.mod)}
              >
                <span className="cd-tk-nokta" aria-hidden />
                <span><b>{m.ad}</b><small>{m.alt}</small></span>
              </button>
            ))}
          </div>
          <div className={`cd-tk-sayilar${mod === 'kapali' ? ' is-kapali' : ''}`}>
            <span>Kaç kez</span>
            <div role="radiogroup" aria-label="Tekrar sayısı">
              {CD_TEKRAR_SAYILAR.map((n) => (
                <button
                  key={n}
                  type="button"
                  role="radio"
                  aria-checked={mod !== 'kapali' && sayi === n}
                  aria-label={n === 0 ? 'Sınırsız' : `${n} kez`}
                  title={n === 0 ? 'Sınırsız (döngü)' : `${n} kez daha`}
                  disabled={mod === 'kapali'}
                  onClick={() => cdTekrarAyarla(mod, n)}
                >
                  {tekrarSayiYaz(n)}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ---------------- oynatıcıda liste denetimi ---------------- */

/** Liste çalarken: önceki ders · "Liste 2/5" · sonraki ders */
/** dar: telefonda denetimlerin üstünde ayrı satır (masaüstünde gizli; masaüstünde sol gruptaki görünür) */
export function ListeDockDenetim({ mini, dar }: { mini?: boolean; dar?: boolean }) {
  const sira = useCdListeSira();
  const n = useCdListe((s) => s.keys.length);
  if (sira < 0) return null;
  const git = () => navigateTo(`${pathFor('canli_ders')}#listem`);
  return (
    <div className={`cd-ld${mini ? ' is-mini' : ''}${dar ? ' is-dar' : ''}`}>
      {!mini && (
        <button type="button" className="cd-ib" onClick={() => cdListeAtla(-1)} disabled={sira === 0} aria-label="Listede önceki ders" title="Önceki ders">
          <SkipBack aria-hidden />
        </button>
      )}
      {!mini && (
        <button type="button" className="cd-ld-sira" onClick={git} title="Listemi aç" aria-label={`Listem: ${sira + 1}. ders / ${n}`}>
          <ListMusic aria-hidden />
          <span>{sira + 1}/{n}</span>
        </button>
      )}
      <button type="button" className="cd-ib" onClick={() => cdListeAtla(1)} disabled={sira >= n - 1} aria-label="Listede sonraki ders" title="Sonraki ders">
        <SkipForward aria-hidden />
      </button>
    </div>
  );
}

/* ---------------- liste görünümü ---------------- */

export function Listem({ dersler, onTumu }: { dersler: CdListeDers[]; onTumu: () => void }) {
  const keys = useCdListe((s) => s.keys);
  const sira = useCdListeSira();
  const playing = useCd((s) => s.playing);
  const [onay, setOnay] = useState(false);
  const harita = useMemo(() => new Map(dersler.map((d) => [d.key, d])), [dersler]);
  const ogeler = useMemo(() => keys.map((k) => harita.get(k)).filter((d): d is CdListeDers => !!d), [keys, harita]);
  const toplam = ogeler.reduce((a, d) => a + ((d.varsayilan || d.varyantlar[0])?.sureSn || 0), 0);
  const caliyorKey = sira >= 0 ? keys[sira] : null;

  useEffect(() => {
    if (!onay) return;
    const t = window.setTimeout(() => setOnay(false), 4000);
    return () => window.clearTimeout(t);
  }, [onay]);

  if (!ogeler.length) {
    return (
      <div className="cd-bos cd-lm-bos">
        <span className="cd-ikon" aria-hidden><ListMusic /></span>
        <p><b>Listen boş.</b> Tüm dersler sekmesinde <ListPlus aria-label="listeye ekle" className="cd-satir-ikon" /> ile ders ekle; liste sırayla, kendiliğinden çalar.</p>
        <button type="button" className="cd-btn" onClick={onTumu}>Tüm derslere git</button>
      </div>
    );
  }

  return (
    <section className="cd-lm" aria-label="Listem">
      <div className="cd-lm-bas">
        <div className="cd-lm-bilgi">
          <b>Listem</b>
          <small>{ogeler.length} ders · {fmtSure(toplam)}</small>
        </div>
        <div className="cd-lm-eylem">
          <TekrarSecici yukari={false} />
          {sira >= 0 ? (
            <button type="button" className="cd-btn is-ana" onClick={cdToggle}>
              {playing ? <Pause aria-hidden /> : <Play aria-hidden />}
              <span>{playing ? 'Duraklat' : 'Sürdür'}</span>
            </button>
          ) : (
            <button type="button" className="cd-btn is-ana" onClick={() => cdListeOynat()}>
              <Play aria-hidden />
              <span>Listeyi oynat</span>
            </button>
          )}
          <button
            type="button"
            className={`cd-btn is-ikon${onay ? ' is-tehlike' : ''}`}
            onClick={() => (onay ? (cdListeTemizle(), setOnay(false)) : setOnay(true))}
            aria-label={onay ? 'Emin misin? Listeyi temizle' : 'Listeyi temizle'}
            title={onay ? 'Onaylamak için yeniden dokun' : 'Listeyi temizle'}
          >
            <Trash2 aria-hidden />
          </button>
        </div>
      </div>
      <ol className="cd-satirlar cd-lm-ogeler">
        {ogeler.map((d, k) => {
          const v = d.varsayilan || d.varyantlar[0];
          const bu = d.key === caliyorKey;
          return (
            <li key={d.key} className={`cd-satir${bu ? ' is-caliyor' : ''}`}>
              <div className="cd-satir-ana cd-lm-satir">
                <span className="cd-no" aria-hidden>{k + 1}</span>
                <button
                  type="button"
                  className="cd-satir-ad cd-lm-ad"
                  onClick={() => (bu ? cdToggle() : cdListeOynat(d.key))}
                  aria-label={bu ? `${playing ? 'Duraklat' : 'Sürdür'}: ${d.baslik}` : `Listeyi bu dersten oynat: ${d.baslik}`}
                >
                  <b>{d.no}. {d.baslik}</b>
                  <small>
                    <span>{v ? fmtSure(v.sureSn) : ''}</span>
                    {bu && <span className="cd-chip is-on">{playing ? 'Çalıyor' : 'Duraklatıldı'}</span>}
                  </small>
                </button>
                <div className="cd-satir-eylem cd-lm-eylem-s">
                  <button type="button" className="cd-btn is-ikon" onClick={() => cdListeTasi(d.key, -1)} disabled={k === 0} aria-label={`Yukarı taşı: ${d.baslik}`} title="Yukarı">
                    <ArrowUp aria-hidden />
                  </button>
                  <button type="button" className="cd-btn is-ikon" onClick={() => cdListeTasi(d.key, 1)} disabled={k === ogeler.length - 1} aria-label={`Aşağı taşı: ${d.baslik}`} title="Aşağı">
                    <ArrowDown aria-hidden />
                  </button>
                  <button type="button" className="cd-btn is-ikon" onClick={() => cdListeCikar(d.key)} aria-label={`Listeden çıkar: ${d.baslik}`} title="Listeden çıkar">
                    <X aria-hidden />
                  </button>
                </div>
              </div>
            </li>
          );
        })}
      </ol>
    </section>
  );
}
