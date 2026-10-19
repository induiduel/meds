import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, ChevronLeft, ChevronRight, Headphones, ListMusic, Pause, Play, Repeat, Sparkles } from 'lucide-react';
import { altDersYukle, altDizinYukle, altSesYolu, dk, HARFLER, ilerlemeOku, ilerlemeYaz, sureYazi, type AltDers, type AltDizin, type AltSoru, type Harf } from './altVeri';
import '../../styles/alternatif-cozucu.css';

/**
 * Patoloji alternatif sesli soru çözücü (/alternatif-cozucu).
 * Ders seçilir; soru kökü + seçenekler ekranda dururken EMA seslendirmesi çözümü baştan sona anlatır.
 * "Otomatik geç" açıkken ses bitince sıradaki soruya geçer. İlerleme tarayıcıda (medsoru_alt_cozucu_v1).
 */
const katla = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');
const oku = (k: string) => { try { return new URLSearchParams(location.search).get(k); } catch { return null; } };
const yaz = (p: Record<string, string | null>) => {
  try {
    const u = new URL(location.href);
    Object.entries(p).forEach(([k, v]) => (v === null ? u.searchParams.delete(k) : u.searchParams.set(k, v)));
    history.replaceState(history.state, '', u.pathname + u.search);
  } catch { /* yok */ }
};

const AlternatifCozucuView: React.FC = () => {
  const [dizin, setDizin] = useState<AltDizin | null>(null);
  const [hata, setHata] = useState(false);
  const [ders, setDers] = useState<AltDers | null>(null);
  const [idx, setIdx] = useState(0);
  const [ara, setAra] = useState('');
  const [caliyor, setCaliyor] = useState(false);
  const [oto, setOto] = useState(true);
  const [hiz, setHiz] = useState(1);
  const [anlik, setAnlik] = useState(0);
  const [sure, setSure] = useState(0);
  const sesRef = useRef<HTMLAudioElement | null>(null);
  const otoRef = useRef(oto);
  otoRef.current = oto;

  useEffect(() => {
    altDizinYukle().then((d) => {
      setDizin(d);
      const k = oku('ders');
      if (k) d.dersler.some((x) => x.kod === k) && ac(k);
    }).catch(() => setHata(true));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const ac = useCallback((kod: string) => {
    altDersYukle(kod).then((d) => {
      const kayit = ilerlemeOku()[kod];
      const s = Number(oku('s'));
      const i = s ? Math.max(0, d.sorular.findIndex((q) => q.no === s)) : (kayit?.i || 0);
      setDers(d);
      setIdx(Math.min(Math.max(0, i), d.sorular.length - 1));
      setCaliyor(false);
      yaz({ ders: kod, s: null });
      window.scrollTo({ top: 0 });
    }).catch(() => setHata(true));
  }, []);

  const kapat = useCallback(() => {
    setDers(null);
    setCaliyor(false);
    yaz({ ders: null, s: null });
  }, []);

  const soru: AltSoru | undefined = ders?.sorular[idx];

  // Soru değişince sesi hazırla; çalıyorsa devam et
  useEffect(() => {
    const a = sesRef.current;
    if (!a || !ders || !soru) return;
    a.src = altSesYolu(ders.kod, soru);
    a.playbackRate = hiz;
    setAnlik(0);
    setSure(soru.sure || 0);
    if (caliyor) a.play().catch(() => setCaliyor(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ders?.kod, soru?.no]);

  useEffect(() => {
    if (sesRef.current) sesRef.current.playbackRate = hiz;
  }, [hiz]);

  const git = useCallback((yeni: number, oynat = false) => {
    if (!ders) return;
    const i = Math.min(Math.max(0, yeni), ders.sorular.length - 1);
    setIdx(i);
    const k = ders.sorular[i];
    ilerlemeYaz(ders.kod, { i, bitti: ilerlemeOku()[ders.kod]?.bitti || [] });
    yaz({ s: String(k.no) });
    if (oynat) setCaliyor(true);
  }, [ders]);

  const oynatDuraklat = useCallback(() => {
    const a = sesRef.current;
    if (!a) return;
    if (caliyor) { a.pause(); setCaliyor(false); } else { a.play().then(() => setCaliyor(true)).catch(() => setCaliyor(false)); }
  }, [caliyor]);

  // Klavye: boşluk oynat/duraklat, oklar gezinme
  useEffect(() => {
    if (!ders) return;
    const f = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT')) return;
      if (e.code === 'Space') { e.preventDefault(); oynatDuraklat(); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); git(idx + 1, caliyor); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); git(idx - 1, caliyor); }
    };
    window.addEventListener('keydown', f);
    return () => window.removeEventListener('keydown', f);
  }, [ders, idx, caliyor, git, oynatDuraklat]);

  const dersler = useMemo(() => {
    const q = katla(ara.trim());
    return (dizin?.dersler || []).filter((d) => !q || katla(`${d.no} ${d.baslik}`).includes(q));
  }, [dizin, ara]);

  const toplam = useMemo(() => {
    const d = dizin?.dersler || [];
    return { ders: new Set(d.map((x) => x.no)).size, soru: d.reduce((a, b) => a + b.soru, 0), sure: d.reduce((a, b) => a + b.sure, 0) };
  }, [dizin]);

  if (hata) return <p className="ac-bos">Alternatif çözücü yüklenemedi.</p>;
  if (!dizin) return <p className="ac-bos">Yükleniyor…</p>;
  if (!dizin.dersler.length) return <p className="ac-bos">Alternatif çözücü hazırlanıyor.</p>;

  /* ---------- Ders listesi ---------- */
  if (!ders) {
    return (
      <div className="ac ac-liste-sayfa">
        <header className="ac-baslik">
          <div className="ac-baslik-t">
            <h2><Sparkles aria-hidden />Alternatif çözücü</h2>
            <span className="ac-sayi">{toplam.ders} ders · {toplam.soru.toLocaleString('tr-TR')} soru · {Math.round(toplam.sure / 3600)} saat ses</span>
          </div>
          <p className="ac-aciklama">
            Her soru baştan sona sesli anlatılır: kök ve seçenekler okunur, seçenekler tek tek değerlendirilir,
            doğru cevap gerekçesiyle söylenir. Örnek ve çıkmış patoloji soruları.
          </p>
          <div className="ac-ara">
            <input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Ders ara (ör. nekroz, tümör)" aria-label="Ders ara" />
          </div>
        </header>
        <ul className="ac-liste">
          {dersler.map((d) => {
            const il = ilerlemeOku()[d.kod];
            const biten = il?.bitti?.length || 0;
            return (
              <li key={d.kod}>
                <button type="button" className="ac-satir" onClick={() => ac(d.kod)}>
                  <span className="ac-no">{d.no}</span>
                  <span className="ac-satir-t">
                    <b>{d.baslik}</b>
                    <small>{d.soru} soru · {d.cikmis} çıkmış · {dk(d.sure)}{biten ? ` · ${biten} dinlendi` : ''}</small>
                    {biten > 0 && <span className="ac-cubuk" aria-hidden><i style={{ width: `${(biten / d.soru) * 100}%` }} /></span>}
                  </span>
                  <span className="ac-durum"><Headphones aria-hidden />Dinle</span>
                </button>
              </li>
            );
          })}
        </ul>
        {!dersler.length && <p className="ac-bos">“{ara}” ile eşleşen ders yok.</p>}
      </div>
    );
  }

  /* ---------- Çözücü ---------- */
  const q = ders.sorular[idx];
  const ilerleme = Math.round(((idx + 1) / ders.sorular.length) * 100);
  const dinlenen = ilerlemeOku()[ders.kod]?.bitti || [];

  return (
    <div className="ac ac-oynatici">
      <header className="ac-ust">
        <button type="button" className="ac-ikon" onClick={kapat} aria-label="Ders listesine dön"><ArrowLeft aria-hidden /></button>
        <div className="ac-ust-t">
          <b>{ders.no}. {ders.baslik}</b>
          <small>Soru {idx + 1} / {ders.sorular.length} · {q.tur === 'cikmis' ? 'Çıkmış' : 'Örnek'}</small>
        </div>
        <div className="ac-ust-sag">
          <button type="button" className="ac-ikon" onClick={() => git(idx - 1, caliyor)} disabled={idx === 0} aria-label="Önceki soru"><ChevronLeft aria-hidden /></button>
          <button type="button" className="ac-ikon" onClick={() => git(idx + 1, caliyor)} disabled={idx === ders.sorular.length - 1} aria-label="Sonraki soru"><ChevronRight aria-hidden /></button>
        </div>
      </header>

      <div className="ac-ilerleme" aria-hidden><i style={{ width: `${ilerleme}%` }} /></div>

      <main className="ac-sahne">
        <section className="ac-soru">
          <p className="ac-kok">{q.soru}</p>
          <ol className="ac-secenek">
            {HARFLER.map((h: Harf) => (
              <li key={h} className={h === q.dogru ? 'is-dogru' : ''}>
                <span className="ac-harf">{h}</span>
                <span>{q.secenekler[h]}</span>
                {h === q.dogru && <span className="ac-tik" aria-label="Doğru cevap">✓</span>}
              </li>
            ))}
          </ol>
        </section>

        <section className="ac-cozum">
          <h3><Headphones aria-hidden />Çözüm</h3>
          <p className="ac-giris">{q.giris}</p>
          <ul className="ac-aciklama">
            {HARFLER.map((h: Harf) => (
              <li key={h} className={h === q.dogru ? 'is-dogru' : ''}>
                <b>{q.secenekler[h]}</b>
                <span>{q.aciklamalar[h]}</span>
              </li>
            ))}
          </ul>
          <div className="ac-cevap">Cevap: <b>{q.dogru}</b> — {q.secenekler[q.dogru]}</div>
          <p className="ac-ozet"><b>Özet.</b> {q.ozet}</p>
        </section>
      </main>

      <footer className="ac-bar">
        <button type="button" className="ac-oynat" onClick={oynatDuraklat} aria-label={caliyor ? 'Duraklat' : 'Çözümü dinle'}>
          {caliyor ? <Pause aria-hidden /> : <Play aria-hidden />}
        </button>
        <div className="ac-zaman">
          <input
            type="range" min={0} max={Math.max(1, sure)} step={0.1} value={Math.min(anlik, sure || 0)}
            onChange={(e) => { const a = sesRef.current; if (a) { a.currentTime = Number(e.target.value); setAnlik(Number(e.target.value)); } }}
            aria-label="Ses konumu"
          />
          <small>{sureYazi(anlik)} / {sureYazi(sure)}</small>
        </div>
        <label className="ac-hiz">
          <span>Hız</span>
          <select value={hiz} onChange={(e) => setHiz(Number(e.target.value))} aria-label="Oynatma hızı">
            {[1, 1.25, 1.5, 1.75].map((x) => <option key={x} value={x}>{x}×</option>)}
          </select>
        </label>
        <button type="button" className={`ac-oto${oto ? ' is-acik' : ''}`} onClick={() => setOto((x) => !x)} aria-pressed={oto}>
          <Repeat aria-hidden />Otomatik geç
        </button>
        <span className="ac-dinlenen" title="Bu derste dinlenen soru sayısı">
          <ListMusic aria-hidden />{dinlenen.length}/{ders.sorular.length}
        </span>
      </footer>

      <audio
        ref={sesRef}
        preload="auto"
        onTimeUpdate={(e) => setAnlik(e.currentTarget.currentTime)}
        onLoadedMetadata={(e) => setSure(e.currentTarget.duration || q.sure)}
        onEnded={() => {
          const b = ilerlemeOku()[ders.kod]?.bitti || [];
          if (!b.includes(q.no)) ilerlemeYaz(ders.kod, { i: idx, bitti: [...b, q.no] });
          if (otoRef.current && idx < ders.sorular.length - 1) git(idx + 1, true);
          else setCaliyor(false);
        }}
        onPause={() => setCaliyor(false)}
        onPlay={() => setCaliyor(true)}
      />
    </div>
  );
};

export default AlternatifCozucuView;
