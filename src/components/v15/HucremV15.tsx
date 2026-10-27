import React, { Suspense, lazy, useEffect, useMemo, useState } from 'react';
import { ArrowLeftRight, Check, ChevronLeft, ChevronRight, Droplet, Lock, Share2, Trophy, X, Zap } from 'lucide-react';
import { createPortal } from 'react-dom';
import { linkClick, navigateTo, pathFor } from '../../router';
import { hucreSiralamaGetir, satinAl, sayi, sureYaz, useBasarim, yenile, type HucreSatir, type KilitT } from '../../services/basarimIstemci';
import { useV15Baslik } from './baslik';
import '../../styles/v15/ogren.css';
import '../../styles/v15/hucrem.css';

/**
 * v15 · Hücrem (tasarım sistemi v15 › M "Hücrem"). Yeni sayfa: /hucrem (Menü › Topluluk).
 * Çalışarak kazandığın ATP ya da glukozla hücreni 28 evrim basamağında büyütürsün: lipit keseciğinden hekim hücresine. Basamaklar
 * başarım tanımındaki `tur: "hucre"` kilitleridir (src/data/basarim/tanim.json); satın alma, ATP defteri ve eşitleme
 * mevcut başarım motorundan (POST /api/basarim/satin-al; sunucu "önceki basamak" şartını denetler). Her basamak bir
 * tıbbi bilgi açar. 3B sahne (Hucre3D, three.js) açılan basamağa göre katman katman büyür; glukoz bakiyesi akan parçacık sayısını, canlılık solgunluğu belirler. WebGL yoksa SVG çizim.
 */
const Hucre3D = lazy(() => import('./Hucre3D'));

/** 3B sahne (WebGL); yüklenene ya da WebGL yoksa düz SVG çizim */
function Sahne({ n, glukoz, canlilik }: { n: number; glukoz: number; canlilik: number }) {
  const [yok, setYok] = useState(false);
  if (yok) return <Hucre n={n} />;
  return (
    <Suspense fallback={<Hucre n={n} />}>
      <Hucre3D n={n} glukoz={glukoz} canlilik={canlilik} onHata={() => setYok(true)} />
    </Suspense>
  );
}

export default function HucremV15() {
  const { tanim, durum, hata } = useBasarim();
  const [is, setIs] = useState(false);
  const [mesaj, setMesaj] = useState('');
  const [detay, setDetay] = useState<number | null>(null);
  const [kutlama, setKutlama] = useState<number | null>(null);
  const [cagSec, setCagSec] = useState<string | null>(null);
  const [karsi, setKarsi] = useState<HucreSatir | null>(null);
  const [sira, setSira] = useState<{ satir: HucreSatir[]; benim: number | null; odul: number[]; carpan: number[] } | null>(null);
  useEffect(() => { void yenile(); }, []);
  useEffect(() => { let vazgec = false; void hucreSiralamaGetir().then((r) => !vazgec && setSira(r), () => 0); return () => { vazgec = true; }; }, [durum?.hucre?.basamak]);
  const basamaklar = useMemo(() => tanim.kilitler.filter((k) => k.tur === 'hucre' && k.etkin), [tanim]);
  const acik = durum?.kilit || {};
  const n = basamaklar.filter((b) => acik[b.id]).length;
  const sonraki = basamaklar.find((b) => !acik[b.id]);
  const simdiki = n ? basamaklar[n - 1] : null;
  const bakiye = durum?.atp.bakiye ?? 0;
  useV15Baslik({ baslik: 'Hücrem', alt: `${n}/${basamaklar.length} basamak · ${simdiki?.cag || 'Başlangıç'}` });

  const cag = useMemo(() => {
    const m = new Map<string, KilitT[]>();
    for (const b of basamaklar) { const c = b.cag || 'Diğer'; m.set(c, [...(m.get(c) || []), b]); }
    return [...m];
  }, [basamaklar]);

  const hc = durum?.hucre;
  const glukozFiyat = sonraki ? Math.ceil(sonraki.fiyat * (hc?.glukozFiyatCarpan ?? 1)) : 0;
  const ac = async (odeme: 'atp' | 'glukoz') => {
    if (!sonraki || is) return;
    setIs(true); setMesaj('');
    try { await satinAl(sonraki.id, odeme); setMesaj(`${sonraki.ad} açıldı!`); setKutlama(basamaklar.indexOf(sonraki) + 1); }
    catch (e: any) { setMesaj(e?.message || 'Açılamadı.'); }
    setIs(false);
  };

  if (!durum) {
    return (
      <div className="hc15">
        <section className="v15-card hc15-bos">
          <Sahne n={0} glukoz={0} canlilik={100} />
          <b>Hücreni büyütmek için giriş yap</b>
          <p>Ders çalışıp soru çözdükçe glukoz kazanırsın; glukoz hücreni yaşatır, ATP ya da glukozla hücren lipit keseciğinden hekim hücresine 28 basamakta evrimleşir. {hata && <small>({hata})</small>}</p>
        </section>
      </div>
    );
  }

  return (
    <div className="hc15">
      <h1 className="sr-only">Hücrem</h1>
      <section className="v15-card hc15-sahne">
        <Sahne n={n} glukoz={hc?.glukoz ?? 0} canlilik={hc?.canlilik ?? 100} />
        <div className="hc15-durum">
          <span className="hc15-cag">{simdiki?.cag || 'Başlangıç'}</span>
          <b>{simdiki ? simdiki.ad : 'Henüz boş bir damla'}</b>
          <div className="v15-bar hc15-bar" aria-label={`${n} / ${basamaklar.length} basamak`}><span style={{ width: `${(n / Math.max(1, basamaklar.length)) * 100}%` }} /></div>
          <span className="hc15-atp"><Zap aria-hidden /> {sayi(bakiye)} mol ATP{durum.atp.kuyrukta ? ` · ${sayi(durum.atp.kuyrukta)} kuyrukta` : ''}</span>
          {hc && <>
            <span className="hc15-atp hc15-glk"><Droplet aria-hidden /> {sayi(hc.glukoz)} glukoz{hc.saatKaldi != null ? ` · ~${hc.saatKaldi} saat yeter` : ''}</span>
            <div className={`hc15-can${hc.uyku ? ' is-uyku' : hc.canlilik < 35 ? ' is-az' : ''}`}>
              <span>{hc.uyku ? 'Hücren uykuda' : hc.canlilik < 35 ? 'Hücren aç kalıyor' : 'Canlılık'}</span>
              <div className="v15-bar" role="meter" aria-valuemin={0} aria-valuemax={100} aria-valuenow={hc.canlilik} aria-label="Canlılık"><span style={{ width: `${hc.canlilik}%` }} /></div>
              <b>%{hc.canlilik}</b>
            </div>
          </>}
        </div>
      </section>

      {hc && (
        <section className="v15-card hc15-enerji">
          <h2 className="v15-cap">Hücren nasıl yaşar?</h2>
          <ul>
            <li><b>Glukoz kazan:</b> her çalışma dakikası {hc.glukozDk}, her çözülen soru {hc.glukozSoru} glukoz verir{hc.carpan > 1 ? ` (sıralamadaki yerin sayesinde ×${hc.carpan})` : ''}.</li>
            <li><b>Hücre yer:</b> saatte {hc.saatlik.toLocaleString('tr-TR')} glukoz harcar; büyüdükçe daha çok yer. Glukoz biterse canlılık düşer, hücre uykuya geçer (sıralamada yarım sayılır). Çalışınca toparlanır.</li>
            <li><b>Büyüt:</b> yeni basamağı ATP ile ya da glukozla açabilirsin.</li>
          </ul>
          <dl className="hc15-ist">
            <div><dt>Çalışma</dt><dd>{sureYaz(hc.calismaSn)}</dd></div>
            <div><dt>Çözülen soru</dt><dd>{sayi(hc.soru)}</dd></div>
            <div><dt>Kazanılan glukoz</dt><dd>{sayi(hc.kazanilan)}</dd></div>
            <div><dt>Harcanan (büyüme)</dt><dd>{sayi(hc.harcanan)}</dd></div>
            <div><dt>Yaşam gideri</dt><dd>{sayi(hc.metabolik)}</dd></div>
            <div><dt>Kazanılan ATP</dt><dd>{sayi(hc.atpKazanilan)}</dd></div>
            <div><dt>Başarım</dt><dd>{sayi(hc.basarim)}</dd></div>
            <div><dt>Hücre sırası</dt><dd>{hc.sira ? `${hc.sira}. / ${hc.kisi}` : '—'}</dd></div>
          </dl>
        </section>
      )}

      {sonraki ? (
        <section className="v15-card hc15-sonraki">
          <div>
            <span className="v15-cap">Sıradaki basamak · {basamaklar.indexOf(sonraki) + 1}</span>
            <b>{sonraki.ad}</b>
            <p>{sonraki.cag} çağı. Açınca bu basamağın tıbbi bilgisi ve hücrendeki yeni parçası görünür.</p>
          </div>
          <div className="hc15-odeme">
            <button type="button" className="hc15-ac" onClick={() => ac('atp')} disabled={is || bakiye < sonraki.fiyat}>
              <Zap aria-hidden /> {sayi(sonraki.fiyat)} mol ATP ile aç
            </button>
            <button type="button" className="hc15-ac is-glk" onClick={() => ac('glukoz')} disabled={is || (hc?.glukoz ?? 0) < glukozFiyat}>
              <Droplet aria-hidden /> {sayi(glukozFiyat)} glukozla aç
            </button>
          </div>
          {bakiye < sonraki.fiyat && (hc?.glukoz ?? 0) < glukozFiyat && <p className="v15-cap hc15-eksik">ATP için {sayi(sonraki.fiyat - bakiye)} mol, glukoz için {sayi(glukozFiyat - (hc?.glukoz ?? 0))} eksik. Ders çalışıp soru çözerek glukoz kazan.{' '}
            <a href={pathFor('basarimlar')} onClick={linkClick(() => navigateTo(pathFor('basarimlar')))}>Hedeflere bak</a></p>}
          {mesaj && <p className="hc15-mesaj" role="status">{mesaj}</p>}
        </section>
      ) : (
        <section className="v15-card hc15-sonraki is-bitti"><b>Evrim tamamlandı.</b><p>28 basamağın hepsini açtın. Hücrelerin uyumu artık sensin.</p>{mesaj && <p className="hc15-mesaj">{mesaj}</p>}</section>
      )}

      {sira && (
        <section className="hc15-cagbolum">
          <h2 className="v15-cap"><Trophy aria-hidden className="hc15-kupa" /> En büyük hücreler{sira.benim ? ` · sen ${sira.benim}.` : ''}</h2>
          <p className="v15-cap hc15-ipucu">İlk üç haftalık ATP kazanır ({sira.odul.join(' / ')}) ve glukoz kazancı ×{sira.carpan.join(' / ×')} olur.</p>
          {sira.satir.length ? (
            <ol className="hc15-liste v15-card hc15-sira">
              {sira.satir.slice(0, 20).map((x) => (
                <li key={x.sira + x.ad} className={`hc15-b hc15-s${x.ben ? ' is-ben' : ''}${x.uyku ? ' is-uyku' : ''}`}>
                  <span className="hc15-no" aria-hidden>{x.sira}</span>
                  <span className="hc15-bt">
                    <b>{x.ad}{x.ben ? ' (sen)' : ''}</b>
                    <span>{x.basamak}. basamak · {x.cag}{x.uyku ? ' · uykuda' : ''}</span>
                    <span>{sureYaz(x.calismaSn)} ders · {sayi(x.soru)} soru · {sayi(x.glukoz)} glukoz · {sayi(x.basarim)} başarım</span>
                  </span>
                  <span className="hc15-boyut" title="Canlılık">%{x.canlilik}</span>
                  {!x.ben && <button type="button" className="hc15-kars-b" onClick={() => setKarsi(x)} aria-label={`Hücreni ${x.ad} ile karşılaştır`} title="Karşılaştır"><ArrowLeftRight aria-hidden /></button>}
                </li>
              ))}
            </ol>
          ) : <p className="v15-card hc15-bos">Henüz sıralamada hücre yok. İlk basamağı aç!</p>}
        </section>
      )}

      {/* M17 Hücre karşılaştır: sıralamadan seçilen kullanıcıyla yan yana (hücre-sıralama verisi; benim satırım listede yoksa durumdan) */}
      {karsi && (() => {
        const benS: HucreSatir | null = sira?.satir.find((x) => x.ben) || (hc ? {
          sira: hc.sira || 0, ad: 'Sen', ben: true, basamak: hc.basamak, cag: simdiki?.cag || 'Başlangıç', canlilik: hc.canlilik, uyku: hc.uyku,
          glukoz: hc.glukoz, calismaSn: hc.calismaSn, soru: hc.soru, atp: hc.atpKazanilan, basarim: hc.basarim,
        } : null);
        if (!benS) return null;
        const olcu: [string, (x: HucreSatir) => number, (x: HucreSatir) => string][] = [
          ['Basamak', (x) => x.basamak, (x) => `${x.basamak}`],
          ['Canlılık', (x) => x.canlilik, (x) => `%${x.canlilik}`],
          ['Glukoz', (x) => x.glukoz, (x) => sayi(x.glukoz)],
          ['Ders süresi', (x) => x.calismaSn, (x) => sureYaz(x.calismaSn)],
          ['Soru', (x) => x.soru, (x) => sayi(x.soru)],
          ['ATP', (x) => x.atp, (x) => sayi(x.atp)],
          ['Başarım', (x) => x.basarim, (x) => sayi(x.basarim)],
        ];
        return createPortal(
          <div className="hc15-kars-ort" role="presentation" onClick={() => setKarsi(null)}>
            <section className="hc15-kars v15-card" role="dialog" aria-modal="true" aria-label="Hücre karşılaştırma" onClick={(e) => e.stopPropagation()}>
              <div className="hc15-kars-ust"><b>Hücre karşılaştır</b><button type="button" className="hc15-kars-x" onClick={() => setKarsi(null)} aria-label="Kapat"><X aria-hidden /></button></div>
              <div className="hc15-kars-iki">
                {[benS, karsi].map((x, i) => (
                  <div key={i} className={i === 0 ? 'is-ben' : ''}>
                    <Hucre n={x.basamak} />
                    <b>{i === 0 ? 'Sen' : x.ad}</b>
                    <small>{x.sira ? `${x.sira}. sıra · ` : ''}{x.cag}{x.uyku ? ' · uykuda' : ''}</small>
                  </div>
                ))}
              </div>
              <dl className="hc15-kars-tab">
                {olcu.map(([ad, d, y]) => {
                  const a = d(benS), b = d(karsi);
                  return (
                    <div key={ad}>
                      <dd className={a > b ? 'is-ust' : ''}>{y(benS)}</dd>
                      <dt>{ad}</dt>
                      <dd className={b > a ? 'is-ust' : ''}>{y(karsi)}</dd>
                    </div>
                  );
                })}
              </dl>
            </section>
          </div>, document.body);
      })()}

      {/* Çağlar (tasarım M13–M16): çağ sekmesi + basamak kartları; karta dokununca evrim ayrıntısı */}
      {cag.length > 0 && (() => {
        const secili = cagSec || simdiki?.cag || cag[0][0];
        const liste = cag.find(([ad]) => ad === secili)?.[1] || [];
        const ilk = basamaklar.indexOf(liste[0]) + 1, son = basamaklar.indexOf(liste[liste.length - 1]) + 1;
        return (
          <section className="hc15-cagbolum">
            <div className="v15-seg hc15-cagseg" role="tablist" aria-label="Çağlar">
              {cag.map(([ad, l]) => (
                <button key={ad} type="button" role="tab" aria-selected={ad === secili} aria-current={ad === secili ? 'page' : undefined} onClick={() => setCagSec(ad)}>
                  {ad.replace(/ çağı$/i, '')}<small>{l.filter((b) => acik[b.id]).length}/{l.length}</small>
                </button>
              ))}
            </div>
            <h2 className="v15-cap">{secili} · basamak {ilk}–{son}</h2>
            <ul className="hc15-kartlar" role="list">
              {liste.map((b) => {
                const no = basamaklar.indexOf(b) + 1;
                const durumu = acik[b.id] ? 'acik' : b === sonraki ? 'sirada' : 'kilitli';
                return (
                  <li key={b.id}>
                    <button type="button" className={`v15-card hc15-kart is-${durumu}`} onClick={() => setDetay(no)}>
                      <span className="hc15-kart-r"><Hucre n={durumu === 'kilitli' ? Math.max(0, no - 1) : no} /></span>
                      <span className="hc15-kart-t"><b>{no} · {b.ad}</b>
                        <span className={`v15-tag ${durumu === 'acik' ? 'is-ok' : durumu === 'sirada' ? 'is-a' : ''}`}>{durumu === 'acik' ? 'Açık' : durumu === 'sirada' ? `${sayi(b.fiyat)} mol` : <><Lock aria-hidden /> Kilitli</>}</span>
                      </span>
                      <small>{durumu === 'acik' ? b.aciklama : durumu === 'sirada' ? 'Sıradaki basamak' : 'Önceki basamağı aç'}</small>
                    </button>
                  </li>
                );
              })}
            </ul>
          </section>
        );
      })()}

      {detay != null && basamaklar[detay - 1] && (
        <EvrimDetay no={detay} basamaklar={basamaklar} acik={acik} onGit={setDetay} onKapat={() => setDetay(null)} glukoz={hc?.glukoz ?? 0} canlilik={hc?.canlilik ?? 100} />
      )}
      {kutlama != null && basamaklar[kutlama - 1] && (
        <SeviyeAtla no={kutlama} b={basamaklar[kutlama - 1]} toplam={basamaklar.length} onKapat={() => setKutlama(null)} />
      )}
    </div>
  );
}

/** Evrim yolculuğu + basamak ayrıntısı (tasarım M12 evrimYol, M03 evrimDetay): büyük hücre, önceki/sonraki, zaman çizgisi */
function EvrimDetay({ no, basamaklar, acik, onGit, onKapat, glukoz, canlilik }: {
  no: number; basamaklar: KilitT[]; acik: Record<string, unknown>; onGit: (n: number) => void; onKapat: () => void; glukoz: number; canlilik: number;
}) {
  const b = basamaklar[no - 1];
  const onceki = no > 1 ? basamaklar[no - 2] : null;
  const ac = !!acik[b.id];
  useEffect(() => {
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') onKapat(); if (e.key === 'ArrowLeft' && no > 1) onGit(no - 1); if (e.key === 'ArrowRight' && no < basamaklar.length) onGit(no + 1); };
    window.addEventListener('keydown', k); document.documentElement.classList.add('tam-katman');
    return () => { window.removeEventListener('keydown', k); document.documentElement.classList.remove('tam-katman'); };
  }, [no, basamaklar.length, onGit, onKapat]);
  return createPortal(
    <div className="hc15-ev" role="dialog" aria-modal="true" aria-label={`Basamak ${no}: ${b.ad}`}>
      <header className="hc15-ev-ust">
        <button type="button" className="v15-ib" onClick={onKapat} aria-label="Kapat"><ChevronLeft aria-hidden /></button>
        <div><b>Evrim yolculuğu</b><small>{b.cag} · basamak {no}/{basamaklar.length}</small></div>
      </header>
      <div className="hc15-ev-ic">
        <section className="v15-card hc15-ev-sahne">
          {ac ? <Sahne n={no} glukoz={glukoz} canlilik={canlilik} /> : <div className="hc15-ev-kilit"><Hucre n={no} /><span><Lock aria-hidden /> Henüz açılmadı</span></div>}
          <div className="hc15-ev-gez">
            <button type="button" className="v15-ib" onClick={() => onGit(no - 1)} disabled={no <= 1} aria-label="Önceki basamak"><ChevronLeft aria-hidden /></button>
            <span><b>{no} · {b.ad}</b><small>{b.cag}</small></span>
            <button type="button" className="v15-ib" onClick={() => onGit(no + 1)} disabled={no >= basamaklar.length} aria-label="Sonraki basamak"><ChevronRight aria-hidden /></button>
          </div>
        </section>
        <div className="hc15-ev-yan">
          <span className="v15-cap">Zaman çizgisi</span>
          <div className="hc15-ev-cizgi" role="list" aria-label="Basamaklar">
            {basamaklar.map((x, i) => (
              <button key={x.id} type="button" role="listitem" className={`${i + 1 === no ? 'is-on' : ''}${acik[x.id] ? '' : ' is-kilit'}`} onClick={() => onGit(i + 1)} aria-label={`${i + 1}. ${x.ad}${acik[x.id] ? '' : ', kilitli'}`} title={`${i + 1} · ${x.ad}`}>
                <Hucre n={i + 1} />
              </button>
            ))}
          </div>
          <section className="v15-card hc15-ev-kart">
            <span className="v15-cap">Bu basamakta</span>
            {onceki && <p className="hc15-ev-gec">{onceki.ad} → <b>{b.ad}</b></p>}
            <p>{ac ? b.aciklama : `Açınca bu basamağın tıbbi bilgisi görünür. ${sayi(b.fiyat)} mol ATP ile açılır${onceki && !acik[onceki.id] ? '; önce bir önceki basamak açılmalı' : ''}.`}</p>
          </section>
        </div>
      </div>
    </div>,
    document.body,
  );
}

/** Seviye atlama kutlaması (tasarım M06): yeni basamağın hücresi, adı, bilgisi; Paylaş + Harika */
function SeviyeAtla({ no, b, toplam, onKapat }: { no: number; b: KilitT; toplam: number; onKapat: () => void }) {
  const paylas = async () => {
    const metin = `MeDSor'da hücrem ${no}. basamağa evrimleşti: ${b.ad}`;
    try { if (navigator.share) await navigator.share({ title: 'Hücrem', text: metin }); else { await navigator.clipboard.writeText(metin); setKopya(true); } } catch { /* vazgeçti */ }
  };
  const [kopya, setKopya] = useState(false);
  return createPortal(
    <div className="hc15-sa-perde" role="dialog" aria-modal="true" aria-label={`Seviye ${no}: ${b.ad}`} onClick={onKapat}>
      <div className="hc15-sa v15-card" onClick={(e) => e.stopPropagation()}>
        <button type="button" className="v15-ib hc15-sa-x" onClick={onKapat} aria-label="Kapat"><X aria-hidden /></button>
        <div className="hc15-sa-r"><Hucre n={no} /></div>
        <span className="v15-tag is-ai">Seviye {no} / {toplam}</span>
        <h2>{b.ad}</h2>
        {b.aciklama && <p>{b.aciklama}</p>}
        <div className="hc15-sa-d">
          <button type="button" className="v15-btn is-soft" onClick={paylas}><Share2 aria-hidden /> {kopya ? 'Kopyalandı' : 'Paylaş'}</button>
          <button type="button" className="v15-btn" onClick={onKapat}>Harika</button>
        </div>
      </div>
    </div>,
    document.body,
  );
}

/** Basamak sayısına göre katman katman büyüyen hücre çizimi */
function Hucre({ n }: { n: number }) {
  const g = (min: number) => n >= min;
  const cok = g(22);
  return (
    <svg className="hc15-svg" viewBox="0 0 240 200" role="img" aria-label={`Hücre: ${n} basamak açık`}>
      <defs>
        <radialGradient id="hc15-sit" cx="45%" cy="40%" r="65%"><stop offset="0" stopColor="var(--color-white)" /><stop offset="1" stopColor="var(--color-accent-soft)" /></radialGradient>
      </defs>
      {/* su damlası / ilkel çorba */}
      <ellipse cx="120" cy="100" rx={g(1) ? 104 : 70} ry={g(1) ? 86 : 56} className="hc15-su" />
      {g(2) && [30, 70, 180, 205, 60, 150].map((x, i) => <circle key={i} cx={x} cy={30 + ((i * 47) % 140)} r="3" className="hc15-mol" />)}
      {cok && <circle cx="58" cy="62" r="34" className="hc15-zar is-yan" />}
      {cok && <circle cx="186" cy="146" r="28" className="hc15-zar is-yan" />}
      {g(9) && <ellipse cx="120" cy="100" rx="78" ry="64" className="hc15-duvar" />}
      {g(10) && <path d="M196 104 q14 -8 22 4 t22 2" className="hc15-kamci" />}
      {g(5) ? <ellipse cx="120" cy="100" rx="72" ry="58" className="hc15-zar" fill="url(#hc15-sit)" /> : g(3) && <circle cx="120" cy="100" r="22" className="hc15-zar is-proto" />}
      {g(4) && !g(7) && <path d="M100 100 q10 -14 20 0 t20 0" className="hc15-rna" />}
      {g(20) && <g className="hc15-iskelet">{[[60, 80, 180, 120], [70, 130, 170, 70], [120, 44, 120, 156]].map(([a, b, c, d], i) => <line key={i} x1={a} y1={b} x2={c} y2={d} />)}</g>}
      {g(16) && <path d="M70 120 q10 -10 20 0 t20 0 t20 0" className="hc15-er" />}
      {g(17) && <g className="hc15-golgi">{[0, 6, 12].map((d) => <path key={d} d={`M150 ${66 + d} q12 -8 24 0`} />)}</g>}
      {g(15) ? <g><circle cx="118" cy="96" r="22" className="hc15-cekirdek" /><circle cx="122" cy="92" r="6" className="hc15-cekirdekcik" /></g>
        : g(7) && <path d="M98 100 c8 -12 16 12 24 0 s16 12 24 0" className="hc15-dna" />}
      {g(8) && [[84, 70], [150, 120], [96, 132], [140, 64], [160, 98]].map(([x, y], i) => <circle key={i} cx={x} cy={y} r="2.6" className="hc15-ribozom" />)}
      {g(11) && [[80, 108], [158, 134]].map(([x, y], i) => <ellipse key={i} cx={x} cy={y} rx="9" ry="5" className="hc15-kloro" />)}
      {g(18) && [[86, 84, -20], [152, 108, 25], [104, 136, 10]].map(([x, y, r], i) => <ellipse key={i} cx={x} cy={y} rx="11" ry="6" transform={`rotate(${r} ${x} ${y})`} className="hc15-mito" />)}
      {g(19) && [[138, 140], [72, 96]].map(([x, y], i) => <circle key={i} cx={x} cy={y} r="4.5" className="hc15-lizo" />)}
      {g(25) && <path d="M28 150 l18 -10 l10 14 l14 -6" className="hc15-sinir" />}
      {g(28) && <text x="120" y="190" textAnchor="middle" className="hc15-insan">37 trilyon hücre</text>}
    </svg>
  );
}
