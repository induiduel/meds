import { useYanlislar, yanlisGruplari } from '../../services/yanlislarim';
import React, { useEffect, useMemo, useState } from 'react';
import { ChevronDown, ChevronRight, CircleHelp, Clock, Play, RotateCcw } from 'lucide-react';
import { linkClick, navigateTo, pathFor, type AppRoute } from '../../router';
import { NAV_ITEMS } from '../shell/navModel';
import { KURUL_NOLAR, kurulKaydet, useSeciliKurul } from '../kurul/KurulSecici';
import { MERKEZ_ARACLARI } from '../merkez/merkezModel';
import { getProgress } from '../../services/studyStore';
import { useReviewCounts } from '../../hooks/useReviewCounts';
import { OPEN_REVIEW_FLAG } from '../../services/learnReview';
import { useV15Baslik } from './baslik';
import KurulSecV15 from './KurulSecV15';
import '../../styles/v15/dersler.css';

/**
 * v15 · Soru çöz merkezi (tasarım sistemi v15 › C01). Üç özet kartı (çözdüğün sorular · tekrar zamanı · çıkmışlar),
 * kurul seçici ve "ne zaman kullanılır" cümleli araç listesi. Sayılar yalnız gerçek kayıttan: çözümler bu cihazdaki
 * studyStore, tekrar Öğren hata defteri. "Test oluştur": kuruldaki dersler (deneme sınavının kendi ders listesi,
 * services/testBank.disciplineOptions) + soru sayısı → /sorular/deneme?kurul=&ders=&n=&basla=1 (TestHub adresten okur).
 */
const TON: Partial<Record<AppRoute, string>> = { soru_cozucu: 'is-ok', past_exams: 'is-w', practice: '', questions: 'is-ai', ornek_sorular: 'is-c', olasi_sorular: 'is-b' };

const aracYolu = (id: AppRoute, kurul: number) =>
  id === 'soru_cozucu' ? `/sorular/soru-cozucu/kurul${kurul}` : id === 'past_exams' || id === 'olasi_sorular' ? `${pathFor(id)}?kurul=${kurul}` : pathFor(id);
const git = (url: string) => linkClick(() => navigateTo(url));

export default function SorularMerkezV15() {
  const kurul = useSeciliKurul();
  const review = useReviewCounts();
  useYanlislar();
  const yanlis = yanlisGruplari();
  const cozum = useMemo(() => {
    const all = Object.values(getProgress());
    const dogru = all.filter((a) => a.correct).length;
    return { n: all.length, pct: all.length ? Math.round((dogru / all.length) * 100) : 0, yanlis: all.length - dogru };
  }, []);
  useV15Baslik({ baslik: 'Soru çöz', alt: `Kurul ${kurul}` });

  // Test oluştur: dersler deneme sınavının kendi listesinden (çıkmış arşivi + örnek/Öğren ögeleri)
  const [dersler, setDersler] = useState<[string, number][] | null>(null);
  const [ders, setDers] = useState('');
  const [adet, setAdet] = useState(20);
  const [kip, setKip] = useState<'ogrenme' | 'sinav' | 'sesli'>('ogrenme');
  // tasarım Y01/Y02: kaynak ve zorluk süzgeci (boş = hepsi)
  const [kaynak, setKaynak] = useState<string[]>([]);
  const [zorluk, setZorluk] = useState<string[]>([]);
  const degis = (l: string[], x: string) => (l.includes(x) ? l.filter((y) => y !== x) : [...l, x]);
  useEffect(() => {
    let canli = true;
    setDersler(null);
    setDers('');
    import('../../services/testBank')
      .then(async (m) => m.disciplineOptions(await m.loadArchiveTests(), `donem3-kurul${kurul}`))
      .then((l) => canli && setDersler(l.filter(([, n]) => n > 0)))
      .catch(() => canli && setDersler([]));
    return () => { canli = false; };
  }, [kurul]);
  const testYolu = kip === 'sesli' ? aracYolu('soru_cozucu', kurul)
    : `/sorular/deneme?${new URLSearchParams({ kurul: String(kurul), ders, n: String(adet), basla: '1', ...(kip === 'sinav' ? { kip: 'sinav' } : {}), ...(kaynak.length ? { kaynak: kaynak.join('|') } : {}), ...(zorluk.length ? { zorluk: zorluk.join('|') } : {}) })}`;
  const karmaYolu = `/sorular/deneme?${new URLSearchParams({ kurul: String(kurul), ders: '', n: '20', basla: '1' })}`;

  const tekrarAc = () => {
    try { sessionStorage.setItem(OPEN_REVIEW_FLAG, '1'); } catch { /* yok say */ }
    navigateTo(pathFor('learn'));
  };
  const araclar = MERKEZ_ARACLARI.sorular.filter((a) => NAV_ITEMS[a.id]);

  return (
    <div className="d15 s15">
      <h1 className="sr-only">Soru çöz</h1>
      <div className="s15-ozet">
        <div className="s15-oz v15-card">
          <span className="s15-oz-h"><span className="v15-label">Çözdüğün</span><span className="v15-tile is-ok"><CircleHelp aria-hidden /></span></span>
          <b className="s15-say">{cozum.n.toLocaleString('tr-TR')}</b>
          <span className="v15-cap">{cozum.n ? `%${cozum.pct} doğru · ${cozum.yanlis} yanlış` : 'Henüz soru çözmedin'}</span>
          <a className="v15-btn" href={karmaYolu} onClick={git(karmaYolu)}><span className="s15-uzun">Karma test başlat</span><span className="s15-kisa">Karma</span></a>
        </div>
        <div className="s15-oz v15-card">
          <span className="s15-oz-h">{/* H159: telefonda üç sütunlu kartta "TEKRAR ZAMANI" kesiliyordu; dar ekranda kısa ad */}<span className="v15-label"><span className="s15-uzun">Tekrar zamanı</span><span className="s15-kisa">Tekrar</span></span><span className="v15-tile is-b"><RotateCcw aria-hidden /></span></span>
          <b className="s15-say">{yanlis.hazir.length}</b>
          <span className="v15-cap">{yanlis.bekleyen.length ? `${yanlis.bekleyen.length} yanlış bekliyor` : 'Yanlış yaptığın sorular 48 saat sonra burada'}{review.total.due ? ` · Öğren'de ${review.total.due} kart` : ''}</span>
          <a className="v15-btn is-ghost" href="/sorular/yanlislarim" onClick={git('/sorular/yanlislarim')}><span className="s15-uzun">Yanlışlarımı çöz</span><span className="s15-kisa">Yanlışlar</span></a>
        </div>
        <div className="s15-oz v15-card">
          <span className="s15-oz-h"><span className="v15-label">Çıkmışlar</span><span className="v15-tile is-w"><Clock aria-hidden /></span></span>
          <b className="s15-say s15-say-k">Yıllar</b>
          <span className="v15-cap">Kurul {kurul} çıkmış soruları, yıla ve konuya göre</span>
          <a className="v15-btn is-ghost" href={aracYolu('past_exams', kurul)} onClick={git(aracYolu('past_exams', kurul))}><span className="s15-uzun">Yıla göre çöz</span><span className="s15-kisa">Çıkmış</span></a>
        </div>
      </div>

      <section className="s15-test v15-card" aria-labelledby="s15-test-h">
        <h2 id="s15-test-h" className="v15-h2">Test oluştur</h2>
        <div className="s15-test-sat">
          <span className="v15-label">Ders</span>
          <div className="s15-cipler v15-hscroll" role="radiogroup" aria-label="Ders">
            <button type="button" role="radio" aria-checked={!ders} className={`s15-cip${!ders ? ' is-on' : ''}`} onClick={() => setDers('')}>Tümü</button>
            {dersler === null ? <span className="v15-skel s15-cip-iskelet" aria-hidden /> : dersler.map(([d, n]) => (
              <button key={d} type="button" role="radio" aria-checked={ders === d} className={`s15-cip${ders === d ? ' is-on' : ''}`} onClick={() => setDers(d)}>
                {d.replace(/^Tıbbi\s+/, '')}<span>{n}</span>
              </button>
            ))}
          </div>
        </div>
        <div className="s15-test-sat">
          <span className="v15-label">Kaynak</span>
          <div className="s15-cipler v15-hscroll" role="group" aria-label="Kaynak">
            <button type="button" aria-pressed={!kaynak.length} className={`s15-cip${!kaynak.length ? ' is-on' : ''}`} onClick={() => setKaynak([])}>Hepsi</button>
            {([['cikmis', 'Çıkmış'], ['ornek', 'Örnek soru'], ['mini', 'Mini soru'], ['vaka', 'Klinik karar'], ['tuzak', 'Tuzak avı'], ['bosluk', 'Boşluk']] as const).map(([id, t]) => (
              <button key={id} type="button" aria-pressed={kaynak.includes(id)} className={`s15-cip${kaynak.includes(id) ? ' is-on' : ''}`} onClick={() => setKaynak((l) => degis(l, id))}>{t}</button>
            ))}
          </div>
        </div>
        <div className="s15-test-alt">
          <div className="s15-test-sat">
            <span className="v15-label">Zorluk</span>
            <div className="s15-cipler" role="group" aria-label="Zorluk (örnek sorular)">
              <button type="button" aria-pressed={!zorluk.length} className={`s15-cip${!zorluk.length ? ' is-on' : ''}`} onClick={() => setZorluk([])}>Hepsi</button>
              {([['kolay', 'Kolay'], ['orta', 'Orta'], ['zor', 'Zor']] as const).map(([id, t]) => (
                <button key={id} type="button" aria-pressed={zorluk.includes(id)} className={`s15-cip${zorluk.includes(id) ? ' is-on' : ''}`} onClick={() => setZorluk((l) => degis(l, id))}>{t}</button>
              ))}
            </div>
          </div>
          <div className="s15-test-sat">
            <span className="v15-label">Soru sayısı</span>
            <div className="v15-seg" role="radiogroup" aria-label="Soru sayısı">
              {[10, 20, 40, 60, 100].map((n) => (
                <button key={n} type="button" role="radio" aria-checked={adet === n} aria-current={adet === n ? 'page' : undefined} onClick={() => setAdet(n)}>{n}</button>
              ))}
            </div>
          </div>
          <div className="s15-test-sat">
            <span className="v15-label">Kip</span>
            <div className="v15-seg" role="radiogroup" aria-label="Kip">
              {([['ogrenme', 'Öğrenme'], ['sinav', 'Sınav'], ['sesli', 'Sesli çözücü']] as const).map(([id, t]) => (
                <button key={id} type="button" role="radio" aria-checked={kip === id} aria-current={kip === id ? 'page' : undefined} onClick={() => setKip(id)}>{t}</button>
              ))}
            </div>
          </div>
          <p className="v15-cap s15-kip-ac">{kip === 'ogrenme' ? 'Her cevaptan sonra doğru/yanlış ve açıklama görünür.' : kip === 'sinav' ? 'Cevaplar test bitince açılır; gerçek sınav gibi.' : 'Konu konu sesli çözüm: her şıkkın nedenini dinlersin.'}</p>
          <a className="v15-btn s15-basla" href={testYolu} onClick={git(testYolu)}><Play aria-hidden /> {kip === 'sesli' ? 'Sesli çözücüyü aç' : 'Testi başlat'}</a>
        </div>
      </section>

      <section aria-labelledby="s15-arac-h">
        <div className="d15-sec-h">
          <h2 id="s15-arac-h" className="v15-h2">Araçlar</h2>
          <KurulSecV15 className="s15-kurul" kurul={kurul} onSec={(k) => navigateTo(`/sorular/kurul${k}`)} />
        </div>
        <ul className="s15-liste v15-card" role="list">
          {araclar.map((a) => {
            const it = NAV_ITEMS[a.id];
            return (
              <li key={a.id}>
                <a className="s15-sat" href={aracYolu(a.id, kurul)} onClick={git(aracYolu(a.id, kurul))}>
                  <span className={`v15-tile ${TON[a.id] || ''}`}><it.icon aria-hidden /></span>
                  <span className="s15-sat-t"><b>{it.label}{a.oner && <span className="v15-tag is-a">Önerilen</span>}</b><span>{a.ne}</span></span>
                  <ChevronRight className="v15-chev" aria-hidden />
                </a>
              </li>
            );
          })}
        </ul>
      </section>
    </div>
  );
}
