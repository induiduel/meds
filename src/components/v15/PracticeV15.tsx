import { NEDENLER, yanlisKaydet, yanlisNeden } from '../../services/yanlislarim';
import { navigateTo } from '../../router';
import React, { useEffect, useMemo, useState } from 'react';
import { Bookmark, BookmarkCheck, Check, ChevronLeft, FileText, Pause, Play, RotateCcw, Sparkles, X } from 'lucide-react';
import type { QuestionItem } from '../../types';
import { Sheet } from '../ui/Sheet';
import { Halka } from './Halka';
import '../../styles/v15/soru.css';

/**
 * v15 · Soru çöz (tasarım sistemi v15 › C02 soru, C03 doğru, C04 yanlış çekmecesi, C08 sonuç). Durum PracticeMode'da;
 * bu bileşen yalnız düzendir (v12'deki PracticeV12 ile aynı sözleşme).
 *  - Üst: çık · test adı · n/N · bölümlü ilerleme (doğru/yanlış/cevaplı/şu an) · ✓/✗ sayaçları · süre
 *  - Orta: yıl · ders · konu etiketleri, işaretle, kök, şıklar. Cevaplama iki adım: seç → "Cevapla" (yanlış dokunuşla
 *    cevap kilitlenmesin). Doğruda yeşil satır + kısa açıklama; yanlışta alt çekmece: "Birlikte toparlayalım".
 *  - Alt: önceki · Bilmiyorum (atla) · Cevapla / Sonraki / Testi bitir
 *  - Sonuç: yüzde halkası, doğru/yanlış/boş/süre, ders dökümü, yanlışları çöz · yeniden başla
 */
export interface PracticeV15Props {
  title: string;
  subtitle?: string;
  items: QuestionItem[];
  index: number;
  answers: Record<string, string>;
  marked: Set<string>;
  elapsed: number;
  paused: boolean;
  finished: boolean;
  shortExplanation: string;
  onSelect: (key: string) => void;
  onToggleMark: () => void;
  onGo: (i: number) => void;
  onFinish: () => void;
  onRestart: () => void;
  onReview: () => void;
  onTogglePause: () => void;
  onOpenAi: () => void;
  onOpenQuestion?: (q: QuestionItem) => void;
  onExit?: () => void;
  /** Sınav kipi: test bitene dek doğru/yanlış gösterilmez, sonuçtan sonra incelemede açılır */
  sinav?: boolean;
}

const saat = (s: number) => {
  const m = Math.floor(s / 60);
  return m >= 60 ? `${Math.floor(m / 60)}:${String(m % 60).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}` : `${m}:${String(s % 60).padStart(2, '0')}`;
};
const kalin = (t: string) => t.split(/\*\*(.+?)\*\*/g).map((p, i) => (i % 2 ? <b key={i}>{p}</b> : p));

export const PracticeV15: React.FC<PracticeV15Props> = (p) => {
  const { items, index } = p;
  const q = items[index];
  const rec = q.reconstruction!;
  // Sınav kipi: bitip "İncele"ye basılana dek cevaplar gizli (seçilen şık yalnız işaretli görünür)
  const [incelendi, setIncelendi] = useState(false);
  const gizli = !!p.sinav && !incelendi;
  const secilen = p.answers[q.id];
  const answers = gizli ? {} as Record<string, string> : p.answers;
  const cevap = answers[q.id];
  const dogruMu = !!cevap && cevap === rec.correctAnswer;
  const [secim, setSecim] = useState<string | null>(null);
  const [cekmece, setCekmece] = useState(false);
  const [neden, setNeden] = useState<string | null>(null);
  useEffect(() => { setSecim(null); setCekmece(false); }, [q.id]);

  const dogru = items.filter((x) => answers[x.id] && answers[x.id] === x.reconstruction?.correctAnswer).length;
  const yanlis = items.filter((x) => answers[x.id] && answers[x.id] !== x.reconstruction?.correctAnswer).length;
  const sonda = index >= items.length - 1;

  // Seri (tasarım C03): bu testte şu ana dek art arda doğru
  const seri = (() => { let n = 0; for (let i = index; i >= 0; i--) { const a = answers[items[i].id]; if (a && a === items[i].reconstruction?.correctAnswer) n++; else if (a || i < index) break; } return n; })();
  useEffect(() => setNeden(null), [q.id]);
  const cevapla = () => {
    if (!secim) return;
    p.onSelect(secim);
    yanlisKaydet(q, secim === rec.correctAnswer);
    if (gizli) { if (sonda) p.onFinish(); else p.onGo(index + 1); return; }
    if (secim !== rec.correctAnswer) setCekmece(true);
  };
  // Klavye: A–E seçer, Enter cevaplar (PracticeMode'un A–E doğrudan cevaplamasından önce yakalanır)
  useEffect(() => {
    const k = (e: KeyboardEvent) => {
      if (p.finished || p.paused || cevap) return;
      const t = e.target as HTMLElement | null;
      if (t && /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) return;
      const key = e.key.toUpperCase();
      if (/^[A-E]$/.test(key) && rec.options.some((o, i) => (o.key || 'ABCDE'[i]) === key)) { e.stopImmediatePropagation(); setSecim(key); }
      else if (e.key === 'Enter' && secim) { e.preventDefault(); cevapla(); }
    };
    window.addEventListener('keydown', k, true);
    return () => window.removeEventListener('keydown', k, true);
  });

  if (p.finished) {
    const d = items.filter((x) => p.answers[x.id] && p.answers[x.id] === x.reconstruction?.correctAnswer).length;
    const y = items.filter((x) => p.answers[x.id] && p.answers[x.id] !== x.reconstruction?.correctAnswer).length;
    return <SonucV15 {...p} dogru={d} yanlis={y} onReview={() => { setIncelendi(true); p.onReview(); }} />;
  }

  return (
    <div className={`q15${p.paused ? ' is-dur' : ''}`}>
      <header className="q15-bas">
        {p.onExit && <button type="button" className="v15-ib" onClick={p.onExit} aria-label="Testten çık"><X aria-hidden /></button>}
        <div className="q15-bas-o">
          <div className="q15-bas-s">
            <span className="q15-ad">{p.title}</span>
            <b className="q15-no">{index + 1}/{items.length}</b>
          </div>
          <ol className="q15-ilerleme" role="list" aria-label={`Soru ${index + 1} / ${items.length}`}>
            {items.map((x, i) => {
              const a = answers[x.id];
              const c = i === index ? 'is-su' : !a ? '' : a === x.reconstruction?.correctAnswer ? 'is-ok' : 'is-yok';
              return <li key={x.id} className={c}><button type="button" onClick={() => p.onGo(i)} aria-label={`Soru ${i + 1}`} /></li>;
            })}
          </ol>
        </div>
        <span className="v15-tag is-ok q15-say"><Check aria-hidden /> {dogru}</span>
        <span className="v15-tag is-b q15-say"><X aria-hidden /> {yanlis}</span>
        <button type="button" className="q15-sure" onClick={p.onTogglePause} aria-label={p.paused ? 'Sürdür' : 'Duraklat'} title={p.paused ? 'Sürdür (P)' : 'Duraklat (P)'}>
          {p.paused ? <Play aria-hidden /> : <Pause aria-hidden />} {saat(p.elapsed)}
        </button>
      </header>

      <main className="q15-govde">
        <div className="q15-ust">
          {q.examYear && <span className="v15-tag">{q.examYear}</span>}
          {q.discipline && <span className="v15-tag is-a">{q.discipline.replace(/^Tıbbi\s+/, '')}</span>}
          <span className="q15-konu">{q.topic || ''}</span>
          <button type="button" className={`v15-ib${p.marked.has(q.id) ? ' is-on' : ''}`} onClick={p.onToggleMark} aria-pressed={p.marked.has(q.id)} aria-label="İşaretle (M)" title="İşaretle (M)">
            {p.marked.has(q.id) ? <BookmarkCheck aria-hidden /> : <Bookmark aria-hidden />}
          </button>
        </div>
        <p className="q15-kok">{rec.stem}</p>
        <div className="q15-siklar" role="radiogroup" aria-label="Şıklar">
          {rec.options.map((o, i) => {
            const k = (o.key || 'ABCDE'[i]) as string;
            const durum = cevap ? (k === rec.correctAnswer ? 'is-ok' : k === cevap ? 'is-yok' : 'is-soluk') : (secim || (gizli ? secilen : null)) === k ? 'is-sec' : '';
            return (
              <button key={k} type="button" role="radio" aria-checked={(cevap || secim) === k} disabled={!!cevap || p.paused} className={`q15-sik ${durum}`} onClick={() => setSecim(k)}>
                <b>{k}</b><span>{o.text}</span>
                {cevap && k === rec.correctAnswer && <Check className="q15-sik-i" aria-hidden />}
                {cevap && k === cevap && k !== rec.correctAnswer && <X className="q15-sik-i" aria-hidden />}
              </button>
            );
          })}
        </div>
        {cevap && (
          <div className={`q15-sonuc ${dogruMu ? 'is-ok' : 'is-yok'}`}>
            <b>{dogruMu ? <><Check aria-hidden /> Doğru</> : <><X aria-hidden /> Yanlış · doğru cevap {rec.correctAnswer}</>}</b>
            {p.shortExplanation && <p>{kalin(p.shortExplanation)}</p>}
            <span className="q15-sonuc-a">
              <button type="button" className="v15-btn is-soft" onClick={p.onOpenAi}><Sparkles aria-hidden /> Yardım al</button>
              {p.onOpenQuestion && <button type="button" className="v15-btn is-ghost" onClick={() => p.onOpenQuestion!(q)}><FileText aria-hidden /> Soru ayrıntısı</button>}
            </span>
          </div>
        )}
      </main>

      <footer className="q15-alt">
        <button type="button" className="v15-ib q15-geri" onClick={() => p.onGo(index - 1)} disabled={index === 0} aria-label="Önceki soru"><ChevronLeft aria-hidden /></button>
        {!cevap && (
          <button type="button" className="q15-bilmiyorum" onClick={() => (sonda ? p.onFinish() : p.onGo(index + 1))} disabled={p.paused}>Bilmiyorum</button>
        )}
        {cevap && dogruMu && seri > 1 && <span className="v15-tag is-ok q15-seri">Seri {seri}</span>}
        {cevap ? (
          <button type="button" className="v15-btn q15-ana" onClick={() => (sonda ? p.onFinish() : p.onGo(index + 1))}>{sonda ? 'Testi bitir' : 'Sonraki soru'}</button>
        ) : (
          <button type="button" className="v15-btn q15-ana" onClick={cevapla} disabled={!secim || p.paused}>Cevapla</button>
        )}
      </footer>

      <Sheet open={cekmece} onClose={() => setCekmece(false)} title="Birlikte toparlayalım" width={440} className="q15-sheet">
        <div className="q15-cek">
          <span className="v15-tag is-b q15-cek-et">Cevabın doğru değil · doğru cevap {rec.correctAnswer}</span>
          <div className="q15-neden">
            <b>Neden yanlış yaptın?</b>
            <div role="group" aria-label="Yanlış nedeni">
              {NEDENLER.map((n) => (
                <button key={n} type="button" aria-pressed={neden === n} className={neden === n ? 'is-on' : ''} onClick={() => { const y = neden === n ? null : n; setNeden(y); yanlisNeden(q.id, y); }}>{n}</button>
              ))}
            </div>
            {neden && <small>{neden === 'Bilmiyordum' ? 'Yardım al ile her şıkkı öğren; 48 saat sonra yeniden sorulacak.' : neden === 'Karıştırdım' ? 'Doğru şıkla seçtiğin şıkkın farkını Yardım al ile karşılaştır.' : 'Bilgin var; tekrar zamanında acele etmeden oku.'}</small>}
          </div>
          <p className="q15-cek-not">Bu soruyu 48 saat sonra yeniden soracağım. <a href="/sorular/yanlislarim" onClick={(e) => { e.preventDefault(); setCekmece(false); navigateTo('/sorular/yanlislarim'); }}>Yanlışlarım</a></p>
          <ul className="q15-cek-l" role="list">
            <li>
              <button type="button" onClick={() => { setCekmece(false); p.onOpenAi(); }}>
                <span className="v15-tile is-ai"><Sparkles aria-hidden /></span>
                <span><b>Yardım al</b><small>Her şık: ne, ne işe yarar, neden doğru ya da yanlış</small></span>
                <span className="v15-tag is-ai">Önerilen</span>
              </button>
            </li>
            <li>
              <button type="button" onClick={() => setCekmece(false)}>
                <span className="v15-tile"><FileText aria-hidden /></span>
                <span><b>Açıklamayı oku</b><small>{p.shortExplanation ? 'Sorunun altında kısa açıklama' : 'Bu soruda açıklama yok'}</small></span>
              </button>
            </li>
            {p.onOpenQuestion && (
              <li>
                <button type="button" onClick={() => { setCekmece(false); p.onOpenQuestion!(q); }}>
                  <span className="v15-tile is-c"><FileText aria-hidden /></span>
                  <span><b>Soru ayrıntısı</b><small>Kaynak, ders notu ve tartışma</small></span>
                </button>
              </li>
            )}
          </ul>
          <button type="button" className="v15-btn q15-cek-ana" onClick={() => { setCekmece(false); if (sonda) p.onFinish(); else p.onGo(index + 1); }}>
            {sonda ? 'Testi bitir' : 'Sonraki soru'}
          </button>
        </div>
      </Sheet>
    </div>
  );
};

/* ── Sonuç ── */
const SonucV15: React.FC<PracticeV15Props & { dogru: number; yanlis: number }> = (p) => {
  const n = p.items.length;
  const bos = n - p.dogru - p.yanlis;
  const pct = n ? Math.round((p.dogru / n) * 100) : 0;
  const cevaplanan = p.dogru + p.yanlis;
  const ilkYanlis = p.items.findIndex((x) => p.answers[x.id] && p.answers[x.id] !== x.reconstruction?.correctAnswer);
  const dokum = useMemo(() => {
    const m = new Map<string, { n: number; d: number }>();
    p.items.forEach((x) => {
      const g = (x.discipline || 'Diğer').replace(/^Tıbbi\s+/, '');
      const r = m.get(g) || { n: 0, d: 0 };
      r.n += 1;
      if (p.answers[x.id] && p.answers[x.id] === x.reconstruction?.correctAnswer) r.d += 1;
      m.set(g, r);
    });
    return [...m.entries()].sort((a, b) => b[1].n - a[1].n);
  }, [p.items, p.answers]);
  const mesaj = pct >= 80 ? 'Çok iyi gidiyor' : pct >= 60 ? 'İyi gidiyor' : pct >= 40 ? 'Yanlışlara bir göz at' : 'Konuyu tekrar etmek iyi olur';
  return (
    <div className="q15 q15-son">
      <header className="q15-bas">
        {p.onExit && <button type="button" className="v15-ib" onClick={p.onExit} aria-label="Çık"><ChevronLeft aria-hidden /></button>}
        <div className="q15-bas-o"><span className="q15-ad q15-son-ad">Test sonucu</span><span className="q15-konu">{p.title}</span></div>
      </header>
      <main className="q15-govde q15-son-g">
        <section className="q15-son-hero v15-card">
          <Halka pct={pct} boyut={112} etiket={`%${pct} doğru`} yazi={<span className="q15-son-yuzde">%{pct}<small>{p.dogru} / {n}</small></span>} />
          <div className="q15-son-t">
            <b>{mesaj}</b>
            <span>{cevaplanan ? `Soru başına ortalama ${Math.round(p.elapsed / cevaplanan)} sn` : 'Hiç soru cevaplanmadı'}</span>
            <span className="q15-son-a">
              {ilkYanlis >= 0 && <button type="button" className="v15-btn" onClick={() => { p.onReview(); p.onGo(ilkYanlis); }}>Yanlışları gözden geçir</button>}
              <button type="button" className="v15-btn is-ghost" onClick={p.onRestart}><RotateCcw aria-hidden /> Yeniden başla</button>
            </span>
          </div>
        </section>
        <div className="q15-son-sayi">
          {[['Doğru', p.dogru, 'is-ok'], ['Yanlış', p.yanlis, 'is-yok'], ['Boş', bos, ''], ['Süre', saat(p.elapsed), '']].map(([t, v, c]) => (
            <div key={t as string} className={`v15-card ${c}`}><span>{t}</span><b>{v}</b></div>
          ))}
        </div>
        {dokum.length > 0 && (
          <section className="q15-dokum v15-card" aria-label="Ders dökümü">
            <h2 className="v15-h2">Ders dökümü</h2>
            <ul role="list">
              {dokum.map(([g, r]) => {
                const yp = Math.round((r.d / r.n) * 100);
                return (
                  <li key={g}>
                    <span className="q15-dokum-s"><span>{g}</span><b>%{yp}</b></span>
                    <span className={`v15-bar ${yp >= 75 ? 'is-ok' : yp >= 50 ? '' : 'is-w'}`}><span style={{ width: `${yp}%` }} /></span>
                  </li>
                );
              })}
            </ul>
          </section>
        )}
      </main>
    </div>
  );
};
