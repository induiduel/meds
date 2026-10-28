import React, { useCallback, useEffect, useRef, useState } from 'react';
import { ChevronRight, Pause, Play, RotateCcw, X } from 'lucide-react';
import './tanitim-video.css';

/* ------------------------------------------------------------------
 * Tanıtım videoları: sitenin kendisini canlandıran, imleçli 4 kısa "reklam".
 *   1) Sesli ders: metin takibi, canlı çizim, lazer, çıkmış soru çipi
 *   2) Soru çözücü: örnek/çıkmış soru, şık şık "Yardım al", sesli çözüm
 *   3) Öğren + oyunlar: etkileşimli slayt, boşluk doldurma, ders sonu oyunu
 *   4) İlerleme: istatistik, sıralama, başarımlar, KMB
 * Gerçek video dosyası yok; her kare zaman çizelgesinden (t sn) türetilir, bekleme ekranı yok.
 * İlk video bittikten sonra "Geç" açılır. `medsoru:tanitim` olayı yeniden açar.
 * ------------------------------------------------------------------ */

const GORULDU = 'medsoru_tanitim_v1';
export const tanitimGoruldu = () => { try { return localStorage.getItem(GORULDU) === '1'; } catch { return false; } };
const isaretle = () => { try { localStorage.setItem(GORULDU, '1'); } catch { /* yok */ } };

/** t, x%, y%, tıklama — ya da t, hedef (data-tv), tıklama: hedef öğenin o anki gerçek merkezine gider (sabit yüzde ekran
 *  boyutuyla kayıyor, imleç düğmenin yanına tıklıyordu) */
type Imlec = [number, number, number, boolean?] | [number, string, boolean?];
/** oynatma hızı: sahneler 1,25× hızlı akar (kullanıcı 2026-10-28: ~%20 daha kısa) */
const HIZ = 1.25;
type Video = { baslik: string; etiket: string; sure: number; imlec: Imlec[]; altyazi: [number, string][]; Sahne: React.FC<{ t: number }> };

/** a→b arasında 0..1 ilerleme */
const ar = (t: number, a: number, b: number) => Math.min(1, Math.max(0, (t - a) / (b - a)));
const yumusak = (p: number) => p * p * (3 - 2 * p);

type Nokta = { x: number; y: number; tik: boolean };
/** Hedefli noktayı sahnedeki öğenin merkezine çözer; öğe henüz yoksa son ölçülen yer (ya da önceki nokta) kullanılır. */
function coz(k: Imlec, sahne: HTMLElement | null, bellek: Map<string, [number, number]>, onceki: [number, number]): [number, number] {
  if (typeof k[1] === 'number') return [k[1], k[2] as number];
  const ad = k[1];
  const el = sahne?.querySelector(`[data-tv="${ad}"]`) as HTMLElement | null;
  if (el && sahne) {
    const r = el.getBoundingClientRect(), S = sahne.getBoundingClientRect();
    if (S.width > 0 && r.width > 0) {
      const xy: [number, number] = [((r.left + r.width / 2 - S.left) / S.width) * 100, ((r.top + r.height / 2 - S.top) / S.height) * 100];
      bellek.set(ad, xy);
    }
  }
  return bellek.get(ad) ?? onceki;
}
const tikMi = (k: Imlec) => (typeof k[1] === 'number' ? !!k[3] : !!k[2]);

function imlecKonumu(k: Imlec[], t: number, sahne: HTMLElement | null, bellek: Map<string, [number, number]>): Nokta {
  let i = 0;
  while (i < k.length - 1 && k[i + 1][0] <= t) i++;
  let onceki: [number, number] = [50, 50];
  for (let n = 0; n < i; n++) onceki = coz(k[n], null, bellek, onceki);
  const A = coz(k[i], sahne, bellek, onceki);
  const B = coz(k[Math.min(i + 1, k.length - 1)], sahne, bellek, A);
  const a = k[i][0], b = k[Math.min(i + 1, k.length - 1)][0];
  const p = b === a ? 0 : yumusak(ar(t, a, b));
  const tik = k.some(x => tikMi(x) && t >= x[0] && t < x[0] + 0.35);
  return { x: A[0] + (B[0] - A[0]) * p, y: A[1] + (B[1] - A[1]) * p, tik };
}

/* ---------------- 1) Sesli ders ---------------- */
const CUMLELER = [
  'Nefrotik sendromda glomerül bazal membranı proteine geçirgen hâle gelir.',
  'Günlük 3,5 gramı aşan proteinüri tanının temel ölçütüdür.',
  'Şekilde podosit ayaksı çıkıntılarının silindiği görülüyor.',
  'Hipoalbüminemi ödemi, karaciğer yanıtı ise hiperlipidemiyi açıklar.',
];
const SesliDers: React.FC<{ t: number }> = ({ t }) => {
  const aktif = Math.min(3, Math.floor(t / 4.2));
  const cizim = ar(t, 9, 11.2);
  const cipGorunur = t > 12.5;
  const soru = t > 14.6 && t < 22.5;
  const secti = t > 18.2;
  const kelime = Math.floor(ar(t, aktif * 4.2, aktif * 4.2 + 3.6) * CUMLELER[aktif].split(' ').length);
  return (
    <div className="tv-app">
      <div className="tv-top"><b>Sesli ders</b><span>Kurul 2 · Patoloji · Böbrek</span><i className={`tv-ses ${soru ? 'dur' : ''}`}>{[0, 1, 2, 3, 4].map(n => <em key={n} style={{ animationDelay: `${n * 0.12}s` }} />)}</i></div>
      <div className="tv-ders">
        <div className="tv-slayt">
          <div className="tv-slayt-b">Nefrotik Sendrom</div>
          <ul>
            <li className={aktif === 0 ? 'on' : ''}>GBM geçirgenliği ↑</li>
            <li className={aktif === 1 ? 'on' : ''}>Proteinüri &gt; 3,5 g/gün</li>
            <li className={aktif === 3 ? 'on' : ''}>Ödem · hiperlipidemi</li>
          </ul>
          <div className="tv-resim" data-tv="resim">
            <svg viewBox="0 0 120 70" aria-hidden>
              <rect width="120" height="70" rx="6" fill="#efe7da" />
              {[0, 1, 2, 3, 4, 5].map(n => <ellipse key={n} cx={18 + n * 17} cy={44} rx={7} ry={4 + (n % 2) * 2} fill="#d9b8a8" />)}
              <path d="M8 50 Q60 30 112 50" stroke="#b07a68" strokeWidth="3" fill="none" />
              <ellipse cx="62" cy="42" rx="22" ry="13" fill="none" stroke="#e0533d" strokeWidth="2.4"
                strokeDasharray="110" strokeDashoffset={110 * (1 - cizim)} />
              {cizim >= 1 && <path d="M98 12 L78 32" stroke="#e0533d" strokeWidth="2.4" markerEnd="url(#ok)" />}
              <defs><marker id="ok" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6z" fill="#e0533d" /></marker></defs>
            </svg>
            {aktif === 2 && <span className="tv-lazer" style={{ left: `${30 + cizim * 22}%`, top: `${52 + Math.sin(t * 3) * 4}%` }} />}
          </div>
          {cipGorunur && <span className="tv-cip" data-tv="cip">★ Çıkmışta soruldu</span>}
        </div>
        <div className="tv-metin">
          <div className="tv-k">Metin takibi</div>
          {CUMLELER.map((c, i) => (
            <p key={i} className={i === aktif ? 'on' : i < aktif ? 'gecti' : ''}>
              {i === aktif ? c.split(' ').map((w, j) => <span key={j} className={j <= kelime ? 'ok' : ''}>{w} </span>) : c}
            </p>
          ))}
        </div>
      </div>
      {soru && (
        <div className="tv-modal tv-in">
          <div className="tv-k">2024 · Kurul 2 çıkmış soru</div>
          <p className="tv-kok">Nefrotik sendromda ödemin temel nedeni hangisidir?</p>
          {['Hipertansiyon', 'Hipoalbüminemi', 'Hiperlipidemi', 'Hematüri'].map((s, i) => (
            <div key={s} data-tv={`m-sik-${i}`} className={`tv-sik ${secti && i === 1 ? 'dogru' : ''}`}><b>{'ABCD'[i]}</b>{s}</div>
          ))}
          {secti && <div className="tv-aciklama tv-in">Doğru! Ders kaldığı yerden sürüyor…</div>}
        </div>
      )}
    </div>
  );
};

/* ---------------- 2) Soru çözücü ---------------- */
const SIKLAR = ['Minimal değişiklik hastalığı', 'Membranöz nefropati', 'FSGS', 'IgA nefropatisi', 'Post-streptokokal GN'];
const SoruCozucu: React.FC<{ t: number }> = ({ t }) => {
  const sekme = t < 3.2 ? 0 : 1;
  const secim = t > 6.4 ? 0 : -1;
  const yardim = t > 9.4;
  const sesli = t > 14;
  return (
    <div className="tv-app">
      <div className="tv-top"><b>Soru çöz</b><span>Örnek sorular · Çıkmışlar · Sesli çözücü</span></div>
      <div className="tv-sekmeler">
        {['Örnek sorular', 'Çıkmış sorular', 'Sesli çözücü'].map((s, i) => <span key={s} data-tv={`sekme-${i}`} className={(i === 0 && sekme === 0) || (i === 1 && sekme === 1 && !sesli) || (i === 2 && sesli) ? 'on' : ''}>{s}</span>)}
      </div>
      <div className="tv-soru tv-in" key={sekme}>
        <div className="tv-k">{sekme ? '2023 · Kurul 2 · Soru 14' : 'Örnek soru · Böbrek patolojisi'}</div>
        <p className="tv-kok">Elektron mikroskobide podosit ayaksı çıkıntılarının yaygın silinmesi, ışık mikroskobisi normal olan çocukta en olası tanı?</p>
        {SIKLAR.map((s, i) => (
          <div key={s} data-tv={`sik-${i}`} className={`tv-sik ${secim === i ? 'dogru' : ''}`}><b>{'ABCDE'[i]}</b>{s}
            {yardim && i < 2 && <small className="tv-in" style={{ animationDelay: `${i * 0.5}s` }}>
              {i === 0 ? 'Çocukluk çağının en sık nefrotik nedeni; ışıkta normal, EM\'de yalnız ayaksı çıkıntı silinmesi — bu tablo tam olarak bu.' : 'Erişkinde görülür; GBM\'de subepitelyal birikim ve "spike" yapar, ışıkta normal değildir. (Slayt 12)'}
            </small>}
          </div>
        ))}
        <div className="tv-yardim" data-tv="yardim">{yardim ? 'Her şık: ne olduğu · ne işe yaradığı · neden doğru/yanlış' : 'Yardım al'}</div>
      </div>
      {sesli && (
        <div className="tv-oynatici tv-in">
          <span className="tv-oynat" data-tv="oynat">▶</span>
          <div><b>Sesli çözücü</b><small>Şık şık, slayt kaynağıyla anlatır</small></div>
          <i className="tv-ses">{[0, 1, 2, 3, 4, 5, 6].map(n => <em key={n} style={{ animationDelay: `${n * 0.1}s` }} />)}</i>
        </div>
      )}
    </div>
  );
};

/* ---------------- 3) Öğren + oyunlar ---------------- */
const SIRA = ['Podosit hasarı', 'GBM geçirgenliği ↑', 'Proteinüri', 'Hipoalbüminemi', 'Ödem'];
const Ogren: React.FC<{ t: number }> = ({ t }) => {
  const oyun = t > 10;
  const dolu = t > 5.2;
  const yerlesen = Math.floor(ar(t, 12, 18.5) * 5);
  return (
    <div className="tv-app">
      <div className="tv-top"><b>Öğren</b><span>{oyun ? 'Ders sonu oyunları' : 'Etkileşimli ders · Adım 7 / 24'}</span><i className="tv-bar"><em style={{ width: `${oyun ? 100 : 30 + t * 3}%` }} /></i></div>
      {!oyun ? (
        <div className="tv-ogren tv-in">
          <h4>Nefrotik sendromda ödem mekanizması</h4>
          <p>Proteinüri ile kaybedilen albümin plazma onkotik basıncını düşürür; sıvı interstisyuma geçer.</p>
          <div className="tv-kart">
            <div className="tv-k">Boşluk doldurma</div>
            <p>Ödemin temel nedeni plazmadaki <span data-tv="bosluk" className={`tv-bosluk ${dolu ? 'dolu' : ''}`}>{dolu ? 'albümin' : '______'}</span> düzeyinin düşmesidir.</p>
          </div>
          <div className="tv-ciftler" data-tv="ciftler">
            {['Mini soru', 'Gizli tablo', 'Mekanizma zinciri', 'Tuzak avı'].map((x, i) => <span key={x} className={t > 6.5 + i * 0.6 ? 'on' : ''}>{x}</span>)}
          </div>
        </div>
      ) : (
        <div className="tv-oyun tv-in">
          <div className="tv-k">Sıralama oyunu · Olayları doğru sıraya diz</div>
          <div className="tv-sira">
            {SIRA.map((s, i) => <div key={s} data-tv={`sira-${i}`} className={i < yerlesen ? 'yer' : ''} style={{ order: i < yerlesen ? i : 10 - i }}><b>{i < yerlesen ? i + 1 : '?'}</b>{s}</div>)}
          </div>
          {yerlesen >= 5 && <div className="tv-tebrik tv-in">Kusursuz! +40 ATP</div>}
        </div>
      )}
    </div>
  );
};

/* ---------------- 4) İlerleme ---------------- */
const SIRALAMA = [['Elif', 1820], ['Sen', 1790], ['Mert', 1655], ['Zeynep', 1540]] as const;
const Ilerleme: React.FC<{ t: number }> = ({ t }) => {
  const ekran = t < 6 ? 0 : t < 11.5 ? 1 : t < 16 ? 2 : 3;
  const g = ar(t, 0.5, 4);
  const ustte = t > 8.8;
  return (
    <div className="tv-app">
      <div className="tv-top"><b>{['İstatistikler', 'Sıralama', 'Başarımlar', 'KMB kampı'][ekran]}</b><span>Kurul 2 · bu hafta</span></div>
      {ekran === 0 && (
        <div className="tv-ista tv-in">
          <div className="tv-sayilar">{[['Çözülen', Math.round(412 * g)], ['Doğru', `%${Math.round(78 * g)}`], ['Ders saati', (14.5 * g).toFixed(1)]].map(([a, b]) => <div key={a as string}><b>{b}</b><small>{a}</small></div>)}</div>
          <div className="tv-grafik">{[40, 62, 55, 80, 70, 92, 85].map((h, i) => <em key={i} style={{ height: `${h * yumusak(ar(t, 0.6 + i * 0.25, 2.2 + i * 0.25))}%` }} />)}</div>
          <small className="tv-not">Zayıf konu: Glomerülonefritler → 12 soru önerildi</small>
        </div>
      )}
      {ekran === 1 && (
        <div className="tv-liste tv-in">
          {(ustte ? [SIRALAMA[1], SIRALAMA[0], ...SIRALAMA.slice(2)] : SIRALAMA).map(([ad, p], i) => (
            <div key={ad} data-tv={ad === 'Sen' ? 'sen' : undefined} className={`tv-satir ${ad === 'Sen' ? 'sen' : ''}`}><b>{i + 1}</b>{ad}<span>{ad === 'Sen' && ustte ? 1835 : p} puan</span></div>
          ))}
          <small className="tv-not">Puan: doğru cevap, seri ve tamamlanan ders — ATP günde 100 ile sınırlı</small>
        </div>
      )}
      {ekran === 2 && (
        <div className="tv-rozet tv-in">
          {['İlk ders', '7 gün seri', 'Çıkmış avcısı', '100 soru', 'Kusursuz oyun', 'Kurul ustası'].map((r, i) => (
            <div key={r} data-tv={`rozet-${i}`} className={i < 4 || t > 13.6 ? 'acik' : ''}><span>{['🎧', '🔥', '🎯', '💯', '🧩', '🏆'][i]}</span>{r}</div>
          ))}
          {t > 13.6 && <div className="tv-tebrik tv-in">Yeni başarım: Kusursuz oyun!</div>}
        </div>
      )}
      {ekran === 3 && (
        <div className="tv-kmb tv-in">
          <div className="tv-k">Klinik mesleki beceri · Görsel asistan</div>
          {['Kan basıncı ölçümü', 'IM enjeksiyon', 'Nazogastrik sonda'].map((s, i) => <div key={s} data-tv={`kmb-${i}`} className={`tv-satir ${t > 17.4 && i === 0 ? 'sen' : ''}`}><b>{i + 1}</b>{s}<span>{i === 0 ? 'Öğret + vaka' : 'Sesli'}</span></div>)}
          {t > 18 && <div className="tv-aciklama tv-in">Adım 3: Manşonu dirsek çukurunun 2–3 cm üstüne sar…</div>}
        </div>
      )}
    </div>
  );
};

const VIDEOLAR: Video[] = [
  {
    baslik: 'Sesli dersler ve çıkmış sorular', etiket: 'SESLİ DERS', sure: 24, Sahne: SesliDers,
    imlec: [[0, 80, 80], [2, 62, 40], [8.5, 'resim'], [11, 'resim'], [13.4, 'cip'], [14.4, 'cip', true], [16.5, 'm-sik-0'], [17.7, 'm-sik-1'], [18, 'm-sik-1', true], [21, 60, 75], [24, 60, 75]],
    altyazi: [[0, 'Hoca anlatırken metin kelime kelime takip edilir.'], [8.6, 'Şekil anlatılırken lazer ve canlı çizim tam o yapıyı gösterir.'], [12.4, 'Çıkmışta sorulan yerde çip yanıp söner — tıkla, soruyu çöz.'], [18.4, 'Cevapladığın an ders kaldığı yerden sürer.']],
  },
  {
    baslik: 'Soru çözücü ve örnek sorular', etiket: 'SORU ÇÖZ', sure: 20, Sahne: SoruCozucu,
    imlec: [[0, 70, 70], [2.6, 'sekme-1'], [3, 'sekme-1', true], [5.8, 'sik-0'], [6.2, 'sik-0', true], [8.6, 'yardim'], [9.2, 'yardim', true], [13.4, 'sekme-2'], [13.8, 'sekme-2', true], [16.2, 'oynat'], [16.6, 'oynat', true], [20, 'oynat']],
    altyazi: [[0, 'Ders notuna sadık örnek sorular ve yıl yıl çıkmışlar.'], [5.8, 'Şıkkını seç; anında geri bildirim.'], [9, '"Yardım al": her şık ne, ne işe yarar, neden doğru ya da yanlış.'], [14, 'Sesli çözücü soruyu slayt kaynağıyla anlatır.']],
  },
  {
    baslik: 'Etkileşimli Öğren ve oyunlar', etiket: 'ÖĞREN', sure: 21, Sahne: Ogren,
    imlec: [[0, 70, 30], [4.6, 'bosluk'], [5, 'bosluk', true], [7, 'ciftler'], [9.5, 85, 90], [11.6, 'sira-0'], [12.1, 'sira-0', true], [13.3, 'sira-1', true], [14.6, 'sira-2', true], [15.9, 'sira-3', true], [17.2, 'sira-4', true], [18.5, 'sira-4'], [21, 70, 85]],
    altyazi: [[0, 'Her adım kısa anlatım + 4–6 etkileşim: boşluk doldurma, mini soru, tablo…'], [6.5, 'Yalnızca öğrendiklerinden sorulur — ileri sızıntı yok.'], [10.2, 'Ders sonunda oyunlar: sırala, tahmin et, metni düzelt.'], [18.6, 'Kazandıkça ATP toplanır.']],
  },
  {
    baslik: 'İstatistik, sıralama, başarımlar, KMB', etiket: 'İLERLEME', sure: 22, Sahne: Ilerleme,
    imlec: [[0, 80, 85], [3, 50, 55], [5.8, 40, 70], [8.5, 'sen'], [11, 70, 60], [12.8, 'rozet-4'], [13.2, 'rozet-4', true], [16.4, 'kmb-0'], [17, 'kmb-0', true], [22, 70, 85]],
    altyazi: [[0, 'Ne kadar çalıştığını ve zayıf konularını gör.'], [6, 'Sıralama mantığı: doğru cevap, seri ve tamamlanan ders puanı.'], [11.6, 'Başarımlar açıldıkça rozetler toplanır.'], [16, 'KMB kampı: her beceri sesli öğretim + vaka sınavı.']],
  },
];

export default function TanitimVideo({ onClose }: { onClose: () => void }) {
  const [i, setI] = useState(0);
  const [t, setT] = useState(0);
  const [oynuyor, setOynuyor] = useState(true);
  const [ilkBitti, setIlkBitti] = useState(tanitimGoruldu());
  const v = VIDEOLAR[i];
  const son = useRef(0);
  const sahneRef = useRef<HTMLDivElement>(null);
  const bellek = useRef(new Map<string, [number, number]>());

  useEffect(() => {
    if (!oynuyor) return;
    let id = 0;
    son.current = performance.now();
    const adim = (now: number) => {
      const dt = ((now - son.current) / 1000) * HIZ;
      son.current = now;
      setT(x => {
        const y = Math.min(v.sure, x + dt);
        if (y >= v.sure) setOynuyor(false);
        return y;
      });
      id = requestAnimationFrame(adim);
    };
    id = requestAnimationFrame(adim);
    return () => cancelAnimationFrame(id);
  }, [oynuyor, v.sure]);

  useEffect(() => { if (t >= v.sure && i === 0) { setIlkBitti(true); isaretle(); } }, [t, v.sure, i]);

  const kapat = useCallback(() => { if (ilkBitti) isaretle(); onClose(); }, [ilkBitti, onClose]);
  const git = (n: number) => { bellek.current.clear(); setI(n); setT(0); setOynuyor(true); };
  const ileri = () => (i < VIDEOLAR.length - 1 ? git(i + 1) : kapat());

  useEffect(() => {
    const tus = (e: KeyboardEvent) => {
      if (e.key === 'Escape') kapat();
      if (e.key === ' ') { e.preventDefault(); setOynuyor(o => !o); }
    };
    window.addEventListener('keydown', tus);
    return () => window.removeEventListener('keydown', tus);
  }, [kapat]);

  const im = imlecKonumu(v.imlec, t, sahneRef.current, bellek.current);
  const altyazi = [...v.altyazi].reverse().find(a => t >= a[0])?.[1] ?? '';
  const bitti = t >= v.sure;
  const sn = (x: number) => `0:${String(Math.floor(x / HIZ)).padStart(2, '0')}`; // gerçek (hızlandırılmış) süre

  return (
    <div className="tv-ort" role="dialog" aria-modal="true" aria-label="MeDSor tanıtımı" onClick={e => e.target === e.currentTarget && kapat()}>
      <div className="tv-pencere">
        <header className="tv-bas">
          <span className="tv-logo">M</span>
          <b>MeDSor</b><span className="tv-alt">· {v.baslik}</span>
          <div className="tv-noktalar">{VIDEOLAR.map((x, n) => <button key={n} type="button" aria-label={x.baslik} className={n === i ? 'on' : ''} disabled={n > 0 && !ilkBitti} onClick={() => git(n)} />)}</div>
          <button type="button" className="tv-x" aria-label="Kapat" onClick={kapat}><X size={18} /></button>
        </header>
        <div className="tv-sahne" ref={sahneRef} onClick={() => (bitti ? git(i) : setOynuyor(o => !o))}>
          <div className="tv-ic" key={i}><v.Sahne t={t} /></div>
          <div className={`tv-imlec ${im.tik ? 'tik' : ''}`} style={{ left: `${im.x}%`, top: `${im.y}%` }}>
            <svg width="22" height="22" viewBox="0 0 24 24"><path d="M4 2l16 10-7 1.5L9.5 21z" fill="#fff" stroke="#1d2a28" strokeWidth="1.6" strokeLinejoin="round" /></svg>
          </div>
          {bitti && (
            <div className="tv-son tv-in">
              <b>{i < VIDEOLAR.length - 1 ? `Sırada: ${VIDEOLAR[i + 1].baslik}` : 'Hazırsın — hemen başla!'}</b>
              <div>
                <button type="button" className="tv-ikinci" onClick={e => { e.stopPropagation(); git(i); }}><RotateCcw size={15} /> Tekrar</button>
                <button type="button" className="tv-birinci" onClick={e => { e.stopPropagation(); ileri(); }}>{i < VIDEOLAR.length - 1 ? 'İleri' : 'Başla'} <ChevronRight size={16} /></button>
              </div>
            </div>
          )}
        </div>
        <footer className="tv-alt-bar">
          <div className="tv-altyazi"><b>{v.etiket}</b><span key={altyazi} className="tv-in">{altyazi}</span></div>
          <div className="tv-kontrol">
            <button type="button" className="tv-oyna" onClick={() => (bitti ? git(i) : setOynuyor(o => !o))}>{oynuyor ? <Pause size={15} /> : <Play size={15} />}{oynuyor ? 'Duraklat' : 'Oynat'}</button>
            <span className="tv-zaman">{sn(t)} / {sn(v.sure)}</span>
            <div className="tv-ilerleme"><em style={{ width: `${(t / v.sure) * 100}%` }} /></div>
            {ilkBitti && i < VIDEOLAR.length - 1 && <button type="button" className="tv-gec" onClick={kapat}>Geç</button>}
            <button type="button" className="tv-ileri" disabled={i === 0 && !ilkBitti} onClick={ileri}>{i < VIDEOLAR.length - 1 ? 'İleri' : 'Bitir'} <ChevronRight size={15} /></button>
          </div>
        </footer>
      </div>
    </div>
  );
}
