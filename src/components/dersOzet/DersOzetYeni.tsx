/**
 * Ders özeti — ALTERNATİF tam ekran çalışma/takip ekranı (2026-11-23).
 *
 * Klasik ekran (DersOzetView) olduğu gibi kalır; bu bileşen onun yerine geçebilen opsiyonel bir görünümdür.
 * Yönetici onayı: `ders_ozet_yeni` özellik bayrağı (Yönetim › Site › Özellik bayrakları). Bayrak kapalıyken
 * yalnız yönetici görebilir; açıldığında herkes ders başına "Yeni ekran" düğmesiyle geçebilir
 * (cihaz tercihi `medsoru_ders_ozet_gorunum_v1`: 'yeni' | 'eski').
 *
 * Yapı: üst şerit (geri · ders · işaret yüzdesi · tam ekran · klasik) · sol bölüm dizini (okunan bölüm işaretli,
 * bölüm başına öğrenilen/toplam) · orta okuma sütunu (maddeler, tür + çıkmış rozetleri, "öğrendim" onayı) ·
 * alt çalışma iskelesi (önceki/sonraki bölüm, oynat, hız, süre, ilerleme). Tam ekran: uygulama tam ekranı
 * (`html.is-app-fullscreen`; menü/üst bar gizlenir). Klavye: Boşluk oynat/duraklat · ← → bölüm · F tam ekran.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowLeft, BookOpenCheck, Check, ChevronDown, ChevronLeft, ChevronRight, CircleCheck, Headphones, LayoutList,
  Maximize2, Minimize2, Pause, Play, RotateCcw, Star,
} from 'lucide-react';
import { guvenliLazy } from '../../utils/guvenliLazy';
import { useAppFullscreen } from '../../utils/fullscreen';
import { navigateTo } from '../../router';
import type { Brans } from '../spots/brans';
import { dk, ozIlerlemeYaz, TUR_AD, useOzIlerleme, type OzDers } from './dersOzetVeri';
import { isaretTemizle, isaretToggle, useOzetIsaret } from './dersOzetIsaret';
import { useOzetOynatici } from './oynatici';
import '../../styles/v15/dersOzetYeni.css';

const SoruCozucu = guvenliLazy(() => import('../spots/cozucu/SoruCozucu'));

const kalin = (m: string) => m.split(/\*\*(.+?)\*\*/g).map((p, i) => (i % 2 ? <strong key={i}>{p}</strong> : <React.Fragment key={i}>{p}</React.Fragment>));
const sure = (sn: number) => { const s = Math.max(0, Math.round(sn)); return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`; };

export const DersOzetYeni: React.FC<{ ders: string; d: OzDers; onKlasik: () => void }> = ({ ders, d, onKlasik }) => {
  const oy = useOzetOynatici(d, ders);
  const isaret = useOzetIsaret()[ders] || {};
  const il = useOzIlerleme()[ders];
  const [tam, tamDegis] = useAppFullscreen();
  const [coz, setCoz] = useState<null | 'tum' | 'cikmis'>(null);
  const [cozKod, setCozKod] = useState<string | null>(null);
  const [cikmisAc, setCikmisAc] = useState(false);
  const [aktifBolum, setAktifBolum] = useState<string>(d.bolumler[0]?.id || 'akilda');
  const kok = useRef<HTMLDivElement>(null);

  const tumMaddeler = useMemo(() => [
    ...d.bolumler.flatMap((b) => b.maddeler.map((m) => ({ id: m.id, bolum: b.id }))),
    ...d.akilda.map((_, i) => ({ id: `akilda-${i + 1}`, bolum: 'akilda' })),
  ], [d]);
  const isaretli = tumMaddeler.filter((m) => isaret[m.id]).length;
  const oran = tumMaddeler.length ? Math.round((isaretli / tumMaddeler.length) * 100) : 0;
  const cikmisSay = useMemo(() => new Map((d.cikmis || []).map((c, i) => [c.id, i + 1])), [d]);

  const icindekiler = useMemo(() => [
    ...d.bolumler.map((b, i) => ({
      id: b.id, ad: b.baslik, say: b.maddeler.length,
      biten: b.maddeler.filter((m) => isaret[m.id]).length,
      ikon: String(i + 1).padStart(2, '0'),
    })),
    { id: 'akilda', ad: 'Akılda kalması gerekenler', say: d.akilda.length, biten: d.akilda.filter((_, i) => isaret[`akilda-${i + 1}`]).length, ikon: '★' },
  ], [d, isaret]);

  const git = (id: string) => {
    setAktifBolum(id);
    document.getElementById(id === 'akilda' ? 'dz-akilda' : `dz-b-${id}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  // Okunan öğe değişince bölüm dizininde de işaretle
  useEffect(() => {
    if (!oy.aktif) return;
    const b = tumMaddeler.find((m) => m.id === oy.aktif)?.bolum;
    if (b) setAktifBolum(b);
  }, [oy.aktif, tumMaddeler]);

  // Klavye: Space oynat/duraklat · ← → bölüm · F tam ekran
  useEffect(() => {
    const f = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      if (e.key === ' ') { e.preventDefault(); oy.calYaDur(); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); oy.sonraki(); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); oy.onceki(); }
      else if (e.key === 'f' || e.key === 'F') tamDegis(kok.current);
    };
    window.addEventListener('keydown', f);
    return () => window.removeEventListener('keydown', f);
  }, [oy, tamDegis]);

  const Oge: React.FC<{ id: string; tur?: string; cikmis?: string[]; s?: number[]; metin: string }> = ({ id, tur, cikmis, s, metin }) => (
    <li id={`dz-${id}`} className={`dzn-madde${tur ? ` dzn-${tur}` : ''}${oy.aktif === id ? ' dzn-aktif' : ''}${isaret[id] ? ' dzn-tik' : ''}`}>
      <button type="button" className="dzn-tik-d" role="checkbox" aria-checked={!!isaret[id]} aria-label="Öğrendim olarak işaretle" onClick={() => isaretToggle(ders, id)}>
        <Check size={13} aria-hidden />
      </button>
      <div className="dzn-madde-g">
        {(!!tur || !!cikmis?.length || !!s?.length) && (
          <div className="dzn-madde-ust">
            {tur && TUR_AD[tur as keyof typeof TUR_AD] ? <span className="dzn-tur">{TUR_AD[tur as keyof typeof TUR_AD]}</span> : null}
            {!!cikmis?.length && <span className="dzn-cikmis" title="Bu bilgi çıkmış soruda soruldu">Çıkmış</span>}
            {!!s?.length && <span className="dzn-sayfa" title="Slayt sayfası">s. {s.join(', ')}</span>}
          </div>
        )}
        <p className="dzn-metin" role="button" tabIndex={0} onClick={() => oy.buradan(id)}
          onKeyDown={(e) => { if (e.key === 'Enter') oy.buradan(id); }}>{kalin(metin)}</p>
      </div>
    </li>
  );

  return (
    <div className={`dzn${tam ? ' is-tam' : ''}`} ref={kok}>
      <header className="dzn-ust">
        <div className="dzn-ust-sol">
          <button type="button" className="dzn-ikon" aria-label="Ders özeti listesine dön" onClick={() => navigateTo(`/dersler/ders-ozeti/kurul${d.kurul}`)}><ArrowLeft size={18} /></button>
          <div className="dzn-ust-t">
            <h1>{d.baslik}</h1>
            <p>Ders özeti · {d.brans || ''}{d.ogretim_uyesi ? ` · ${d.ogretim_uyesi}` : ''}</p>
          </div>
        </div>
        <div className="dzn-ust-istat">
          <span className="dzn-yuzde" aria-label={`Maddelerin yüzde ${oran} kadarı işaretli`}>{oran}%</span>
          <span className="dzn-ust-alt">{isaretli}/{tumMaddeler.length} madde</span>
        </div>
        <button type="button" className="dzn-ikon" onClick={() => tamDegis(kok.current)} aria-label={tam ? 'Tam ekrandan çık' : 'Tam ekran'}>
          {tam ? <Minimize2 size={18} /> : <Maximize2 size={18} />}
        </button>
        <button type="button" className="dzn-klasik" onClick={onKlasik} title="Klasik ders özeti ekranına dön">Klasik ekran</button>
      </header>

      <div className="dzn-govde">
        <aside className="dzn-yan" aria-label="Bölümler">
          <p className="dzn-yan-b">İçindekiler</p>
          <nav className="dzn-dizin">
            {icindekiler.map((b) => (
              <button key={b.id} type="button" className={`dzn-dizin-s${aktifBolum === b.id ? ' on' : ''}${b.biten === b.say && b.say > 0 ? ' bitti' : ''}`} onClick={() => git(b.id)}>
                <span className="dzn-dizin-n">{b.ikon}</span>
                <span className="dzn-dizin-a">{b.ad}</span>
                <span className="dzn-dizin-sy">{b.biten}/{b.say}</span>
              </button>
            ))}
          </nav>
          <div className="dzn-yan-alt">
            <p>{d.sure ? `${dk(d.sure)} ses` : ''}{d.cikmis.length ? ` · ${d.cikmis.length} çıkmış` : ''}{d.cozucu ? ` · ${d.cozucu.soru} soru` : ''}</p>
            {!!isaretli && (
              <button type="button" className="dzn-link" onClick={() => isaretTemizle(ders)}>
                <RotateCcw size={13} aria-hidden /> İşaretleri temizle
              </button>
            )}
          </div>
        </aside>

        <main className="dzn-oku">
          <section className="dzn-giris">
            <p>{kalin(d.giris)}</p>
            <nav className="dzn-cipler" aria-label="Bölümler (telefon)">
              {icindekiler.map((b) => (
                <button key={b.id} type="button" className={aktifBolum === b.id ? 'on' : ''} onClick={() => git(b.id)}>{b.ikon === '★' ? '★ Akılda' : `${b.ikon} · ${b.ad}`}</button>
              ))}
            </nav>
            <div className="dzn-araclar">
              {d.ses && (
                <button type="button" className="dzn-btn dzn-birincil" onClick={oy.calYaDur}>
                  {oy.caliyor ? <Pause size={16} aria-hidden /> : oy.basladi || il?.klip ? <Headphones size={16} aria-hidden /> : <Play size={16} aria-hidden />}
                  {oy.caliyor ? 'Duraklat' : oy.basladi || il?.klip ? 'Kaldığın yerden dinle' : `Sesli dinle · ${dk(d.sure)}`}
                </button>
              )}
              {d.cozucu && (
                <button type="button" className="dzn-btn" onClick={() => { oy.dur(); setCozKod(d.cozucu!.kod); setCoz('tum'); }}>
                  <BookOpenCheck size={16} aria-hidden /> Sesli soru çöz · {d.cozucu.soru}
                </button>
              )}
              {d.cozucu && d.cozucu.cikmis > 0 && (
                <button type="button" className="dzn-btn" onClick={() => { oy.dur(); setCozKod(d.cozucu!.kod); setCoz('cikmis'); }}>
                  Yalnız çıkmışlar · {d.cozucu.cikmis}
                </button>
              )}
            </div>
            {!!tumMaddeler.length && (
              <div className="dzn-ilerleme" aria-hidden><span style={{ width: `${oran}%` }} /></div>
            )}
          </section>

          {d.bolumler.map((b, i) => (
            <section key={b.id} id={`dz-b-${b.id}`} className={`dzn-bolum${aktifBolum === b.id ? ' on' : ''}`}>
              <h2>
                <span className="dzn-b-no">{String(i + 1).padStart(2, '0')}</span>
                <span className="dzn-b-ad">{b.baslik}</span>
                <span className="dzn-b-say">{b.maddeler.filter((m) => isaret[m.id]).length}/{b.maddeler.length}</span>
              </h2>
              <ul>
                {b.maddeler.map((m) => <Oge key={m.id} id={m.id} tur={m.tur} cikmis={m.cikmis} s={m.s} metin={m.metin} />)}
              </ul>
            </section>
          ))}

          <section id="dz-akilda" className={`dzn-bolum dzn-akilda${aktifBolum === 'akilda' ? ' on' : ''}`}>
            <h2>
              <Star size={18} aria-hidden />
              <span className="dzn-b-ad">Akılda kalması gerekenler</span>
              <span className="dzn-b-say">{d.akilda.filter((_, i) => isaret[`akilda-${i + 1}`]).length}/{d.akilda.length}</span>
            </h2>
            <ul>
              {d.akilda.map((a, i) => <Oge key={i} id={`akilda-${i + 1}`} cikmis={a.cikmis} s={a.s} metin={a.metin} />)}
            </ul>
          </section>

          <div className="dzn-bitir">
            {il?.bitti ? (
              <button type="button" className="dzn-btn" onClick={() => ozIlerlemeYaz(ders, null)}><RotateCcw size={16} aria-hidden /> Bitti işaretini kaldır</button>
            ) : (
              <button type="button" className="dzn-btn dzn-birincil" onClick={() => ozIlerlemeYaz(ders, { bitti: new Date().toISOString() })}><CircleCheck size={16} aria-hidden /> Bu özeti bitirdim</button>
            )}
            {d.cozucu && <button type="button" className="dzn-btn" onClick={() => { oy.dur(); setCozKod(d.cozucu!.kod); setCoz('tum'); }}><BookOpenCheck size={16} aria-hidden /> Şimdi soruları çöz</button>}
          </div>

          {d.cikmis.length > 0 && (
            <section className="dzn-cikmislar">
              <button type="button" className="dzn-ac" onClick={() => setCikmisAc((x) => !x)} aria-expanded={cikmisAc}>
                <LayoutList size={16} aria-hidden /> Bu dersin çıkmış soruları ({d.cikmis.length})
                <ChevronDown size={16} className={cikmisAc ? 'dzn-don' : ''} aria-hidden />
              </button>
              {cikmisAc && (
                <ol>
                  {d.cikmis.map((c) => (
                    <li key={c.id} value={cikmisSay.get(c.id)}>
                      <p className="dzn-kok">{c.kok}</p>
                      <p className="dzn-cevap"><strong>Cevap:</strong> {c.cevap}{c.yil ? <span className="dzn-yil"> · {c.yil}</span> : null}</p>
                    </li>
                  ))}
                </ol>
              )}
            </section>
          )}
        </main>
      </div>

      <footer className="dzn-dock" role="region" aria-label="Sesli özet oynatıcı">
        <div className="dzn-dock-ust">
          <span className="dzn-dock-ad">{oy.basladi ? oy.klipAdi : 'Dinlemeye hazır'}</span>
          <span className="dzn-dock-sure">{sure(oy.ilerleme * (d.sure || 0))} / {sure(d.sure || 0)}</span>
        </div>
        <div className="dzn-dock-cubuk" aria-hidden><span style={{ width: `${Math.round(oy.ilerleme * 100)}%` }} /></div>
        <div className="dzn-dock-alt">
          <button type="button" className="dzn-ikon" onClick={oy.onceki} aria-label="Önceki bölüm" disabled={!d.ses}><ChevronLeft size={20} /></button>
          <button type="button" className="dzn-oynat" onClick={oy.calYaDur} aria-label={oy.caliyor ? 'Duraklat' : 'Oynat'} disabled={!d.ses}>
            {oy.caliyor ? <Pause size={22} /> : <Play size={22} />}
          </button>
          <button type="button" className="dzn-ikon" onClick={oy.sonraki} aria-label="Sonraki bölüm" disabled={!d.ses}><ChevronRight size={20} /></button>
          <button type="button" className="dzn-hiz" onClick={oy.hizDegis} aria-label="Okuma hızı" disabled={!d.ses}>{oy.hiz}×</button>
          <span className="dzn-dock-bos" />
          <span className="dzn-dock-ipucu"><kbd>Boşluk</kbd> oynat · <kbd>←</kbd><kbd>→</kbd> bölüm · <kbd>F</kbd> tam ekran</span>
        </div>
      </footer>

      {coz && d.cozucu && (
        <React.Suspense fallback={null}>
          <SoruCozucu key={cozKod || d.cozucu.kod} brans={d.cozucu.brans as Brans} kod={cozKod || d.cozucu.kod} mod={coz === 'cikmis' ? 'cikmis' : undefined}
            onClose={() => setCoz(null)} onDersDegis={(k) => { if (!d.cozucu?.kodlar || d.cozucu.kodlar.includes(k)) setCozKod(k); else setCoz(null); }} />
        </React.Suspense>
      )}
    </div>
  );
};

export default DersOzetYeni;
