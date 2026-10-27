import React, { useEffect, useMemo, useState } from 'react';
import { Check, ChevronLeft, Settings2, X } from 'lucide-react';
import { loadArchiveBank, type StudyQuestion } from '../../services/studyStore';
import { getStatsAttempts, getStatsTests } from '../../services/progressReset';
import { sureYaz, useTakip } from '../../services/calismaTakip';
import { Halka } from './Halka';
import SoruSuzgecV15, { suzgecUyar, type SuzgecDegeri, type SuzgecYonu } from './SoruSuzgecV15';
import '../../styles/v15/grafik.css';
import '../../styles/v15/istat.css';

/**
 * v15 · Soru istatistikleri (tasarım X04 genel · X05 tek tek sorular · X06 soru detayı · X07 puan · X08 konu ·
 * J02 grafik detay · X10 grafik ayarları). İstatistiklerim sayfasında Çalışma grafiklerinin altında.
 *
 * Veri (yalnız gerçek, bu cihaz): çözüm geçmişi `getStatsAttempts` (arşiv + güncel; soru → doğru/yanlış + zaman),
 * soru bilgisi `loadArchiveBank` (ders, konu, kurul, kök, şıklar), denemeler `getStatsTests`, konu süreleri
 * `useTakip` (çalışma takibi). Verisi olmayan bölüm uydurma sayı yerine açıklayıcı boş durum gösterir.
 *
 * Unutma eğrisi (J02) — tahmini hatırlama, Ebbinghaus üstel modeli:
 *   R(t) = exp(−t / S)       t = konunun son çözümünden bu yana geçen gün
 *   S = min(60, 1,5 · 2^(n−1)) · (0,5 + d)   gün; n = konunun çözüldüğü ayrı gün sayısı, d = konudaki doğru oranı (0–1)
 * Her ayrı günde tekrar kararlılığı ikiye katlar (aralıklı tekrar), doğruluk ×0,5–×1,5 ölçekler. Bu bir tahmindir,
 * ölçüm değildir; ekranda da böyle yazılır.
 *
 * Grafik ayarları (X10) yalnız bu cihazda: localStorage `medsoru_grafik_ayar_v1` (try/catch).
 */
const GUN = 86_400_000;
type Sekme = 'genel' | 'soru' | 'konu' | 'puan';
interface Ayar { aralik: 7 | 30 | 90 | 0; tur: 'cubuk' | 'cizgi'; egri: boolean }
const AYAR_KEY = 'medsoru_grafik_ayar_v1';
const AYAR0: Ayar = { aralik: 30, tur: 'cubuk', egri: true };
const ayarOku = (): Ayar => { try { return { ...AYAR0, ...JSON.parse(localStorage.getItem(AYAR_KEY) || '{}') }; } catch { return AYAR0; } };
const ayarYaz = (a: Ayar) => { try { localStorage.setItem(AYAR_KEY, JSON.stringify(a)); } catch { /* özel pencere */ } };
const gk = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const ders = (s?: string) => (s || 'Diğer').replace(/^Tıbbi\s+/, '');
const kurulAd = (id?: string) => { const n = /(\d+)/.exec(id || '')?.[1]; return n ? `Kurul ${n}` : 'Kurul ?'; };
const tarih = (iso: string) => new Date(iso).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', year: 'numeric' });
export const kararlilik = (n: number, d: number) => Math.min(60, 1.5 * 2 ** Math.max(0, n - 1)) * (0.5 + d);
export const hatirlama = (t: number, S: number) => Math.exp(-Math.max(0, t) / S);
const ton = (p: number) => (p >= 70 ? 'is-ok' : p >= 55 ? '' : 'is-w');
/** çalışma takibi konu kimliği → okunur ad (basarimMotor.konuAdi ile aynı kural, ders kayıt defteri olmadan) */
const takipAd = (id: string) => {
  const rest = id.split(':').slice(1).join(':');
  const bk = rest.match(/^([a-zçğıöşü]+)\/[a-z]?0*(\d+)$/i);
  if (bk) return `${bk[1].charAt(0).toLocaleUpperCase('tr-TR')}${bk[1].slice(1)} · ${bk[2]}. ders`;
  const a = rest.replace(/^k\d+p?-/, '').replace(/-v\d+$/, '').replace(/[-_/]+/g, ' ').replace(/^deck /, '').trim();
  return a.charAt(0).toLocaleUpperCase('tr-TR') + a.slice(1);
};

/** Tek ölçülü zaman serisi: çubuk ya da çizgi (X10 tercihi). değer null → veri yok. */
function Seri({ v, tur, birim, tavan }: { v: { e: string; d: number | null }[]; tur: Ayar['tur']; birim: string; tavan?: number }) {
  const W = 360, H = 130, P = 8;
  const max = tavan ?? Math.max(1, ...v.map((x) => x.d || 0));
  const x = (i: number) => P + (i * (W - 2 * P)) / Math.max(1, v.length - 1);
  const y = (d: number) => H - P - (d / max) * (H - 2 * P);
  const bw = Math.max(2, (W - 2 * P) / v.length - 2);
  const nk = v.map((s, i) => (s.d == null ? null : { i, s })).filter(Boolean) as { i: number; s: { e: string; d: number } }[];
  return (
    <svg className="is15-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none" role="img" aria-label={`${v.length} dönemlik ${birim} grafiği`}>
      {[0.5, 1].map((f) => <line key={f} x1={P} x2={W - P} y1={y(max * f)} y2={y(max * f)} className="gf15-izgara" />)}
      {tur === 'cubuk'
        ? nk.map(({ i, s }) => <rect key={s.e} x={P + (i * (W - 2 * P)) / v.length + 1} width={bw} y={y(s.d)} height={Math.max(s.d ? 2 : 0, H - P - y(s.d))} rx="2" className="is15-cubuk"><title>{`${s.e}: ${s.d} ${birim}`}</title></rect>)
        : <>
            {nk.length > 1 && <polyline points={nk.map(({ i, s }) => `${x(i)},${y(s.d)}`).join(' ')} className="gf15-cizgi-l" />}
            {nk.map(({ i, s }) => <circle key={s.e} cx={x(i)} cy={y(s.d)} r="3" className="gf15-nokta"><title>{`${s.e}: ${s.d} ${birim}`}</title></circle>)}
          </>}
    </svg>
  );
}

export default function IstatistikV15() {
  const [sekme, setSekme] = useState<Sekme>('genel');
  const [ayar, setAyarR] = useState<Ayar>(ayarOku);
  const [ayarAcik, setAyarAcik] = useState(false);
  const setAyar = (a: Ayar) => { setAyarR(a); ayarYaz(a); };
  const [bank, setBank] = useState<StudyQuestion[] | null>(null);
  useEffect(() => { loadArchiveBank().then(setBank).catch(() => setBank([])); }, []);
  const [detay, setDetay] = useState<string | null>(null);
  const [suz, setSuz] = useState<SuzgecDegeri>({});
  const takip = useTakip();

  const tum = useMemo(() => getStatsAttempts().filter(([, a]) => a && a.at && !Number.isNaN(Date.parse(a.at))), []);
  const testler = useMemo(() => getStatsTests().filter((t) => t && t.total > 0).sort((a, b) => a.at.localeCompare(b.at)), []);
  const byId = useMemo(() => new Map((bank || []).map((q) => [q.id, q])), [bank]);
  const bas = ayar.aralik ? Date.now() - ayar.aralik * GUN : 0;
  const donem = useMemo(() => tum.filter(([, a]) => Date.parse(a.at) >= bas), [tum, bas]);

  // Soru başına geçmiş (tümü, tarih sırasıyla) ve dönemdeki son sonuç
  const soru = useMemo(() => {
    const m = new Map<string, { at: string; c: boolean }[]>();
    for (const [id, a] of tum) { const l = m.get(id) || []; l.push({ at: a.at, c: a.correct }); m.set(id, l); }
    m.forEach((l) => l.sort((a, b) => a.at.localeCompare(b.at)));
    return m;
  }, [tum]);
  const donemSorulari = useMemo(() => {
    const s = new Map<string, { at: string; c: boolean }>();
    for (const [id, a] of donem) { const e = s.get(id); if (!e || a.at > e.at) s.set(id, { at: a.at, c: a.correct }); }
    return [...s.entries()].sort((a, b) => b[1].at.localeCompare(a[1].at));
  }, [donem]);

  const genel = useMemo(() => {
    const d = donem.filter(([, a]) => a.correct).length;
    const gunSay = ayar.aralik || Math.min(120, Math.max(7, Math.ceil((Date.now() - Math.min(...donem.map(([, a]) => Date.parse(a.at)), Date.now())) / GUN) + 1));
    const g: Record<string, number> = {};
    for (const [, a] of donem) { const k = gk(new Date(a.at)); g[k] = (g[k] || 0) + 1; }
    const gunler = Array.from({ length: gunSay }, (_, i) => { const t = new Date(Date.now() - (gunSay - 1 - i) * GUN); return { e: t.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' }), d: g[gk(t)] || 0 }; });
    const dm = new Map<string, { n: number; d: number }>();
    for (const [id, a] of donem) { const k = ders(byId.get(id)?.discipline); const r = dm.get(k) || { n: 0, d: 0 }; r.n++; if (a.correct) r.d++; dm.set(k, r); }
    return { n: donem.length, d, y: donem.length - d, p: donem.length ? Math.round((d / donem.length) * 100) : 0, gunler, dersler: [...dm.entries()].sort((a, b) => b[1].n - a[1].n) };
  }, [donem, byId, ayar.aralik]);

  const konular = useMemo(() => {
    const m = new Map<string, { ad: string; ders: string; n: number; d: number; gun: Set<string>; son: number }>();
    for (const [id, a] of donem) {
      const q = byId.get(id); if (!q) continue;
      const ad = (q.topic || '').trim() || ders(q.discipline);
      const k = `${ders(q.discipline)}|${ad}`;
      const r = m.get(k) || { ad, ders: ders(q.discipline), n: 0, d: 0, gun: new Set<string>(), son: 0 };
      r.n++; if (a.correct) r.d++; r.gun.add(gk(new Date(a.at))); r.son = Math.max(r.son, Date.parse(a.at));
      m.set(k, r);
    }
    return [...m.entries()].map(([k, r]) => {
      const dp = r.d / r.n; const S = kararlilik(r.gun.size, dp); const t = (Date.now() - r.son) / GUN;
      return { k, ...r, p: Math.round(dp * 100), S, t, R: hatirlama(t, S) };
    }).sort((a, b) => b.n - a.n);
  }, [donem, byId]);

  const sureKonu = useMemo(() => Object.entries(takip.k).filter(([, r]) => (r.sn || 0) >= 60 && (!bas || (r.sonAt && Date.parse(r.sonAt) >= bas)))
    .sort((a, b) => b[1].sn - a[1].sn).slice(0, 10), [takip, bas]);

  const yonler: SuzgecYonu[] = useMemo(() => {
    const say = (f: (id: string, c: boolean) => string) => { const m = new Map<string, number>(); donemSorulari.forEach(([id, r]) => { const v = f(id, r.c); m.set(v, (m.get(v) || 0) + 1); }); return [...m.entries()].sort((a, b) => b[1] - a[1]).map(([deger, n]) => ({ deger, n })); };
    return [
      { id: 'sonuc', ad: 'Son sonuç', secenekler: say((_, c) => (c ? 'Doğru' : 'Yanlış')) },
      { id: 'ders', ad: 'Ders', secenekler: say((id) => ders(byId.get(id)?.discipline)) },
      { id: 'kurul', ad: 'Kurul', secenekler: say((id) => kurulAd(byId.get(id)?.committeeId)) },
      { id: 'yil', ad: 'Yıl', secenekler: say((id) => byId.get(id)?.year || 'Bilinmiyor') },
    ];
  }, [donemSorulari, byId]);
  const suzulmus = donemSorulari.filter(([id, r]) => { const q = byId.get(id); return suzgecUyar(suz, 'sonuc', r.c ? 'Doğru' : 'Yanlış') && suzgecUyar(suz, 'ders', ders(q?.discipline)) && suzgecUyar(suz, 'kurul', kurulAd(q?.committeeId)) && suzgecUyar(suz, 'yil', q?.year || 'Bilinmiyor'); });

  const aralikAd = ayar.aralik ? `Son ${ayar.aralik} gün` : 'Tüm zamanlar';
  const bosSoru = <p className="gf15-bos">{aralikAd} içinde çözülmüş soru yok. Soru çöz ya da deneme testlerinde cevapladığın sorular burada birikir.</p>;

  if (detay) return <SoruDetay id={detay} q={byId.get(detay)} gecmis={soru.get(detay) || []} geri={() => setDetay(null)} />;

  return (
    <section className="gf15 is15" aria-label="Soru istatistikleri">
      <div className="gf15-ust">
        <h2>Soruların</h2>
        <button type="button" className="v15-ib" onClick={() => setAyarAcik(true)} aria-label="Grafik ayarları" title="Grafik ayarları"><Settings2 aria-hidden /></button>
      </div>
      <div className="v15-seg is15-seg" role="tablist" aria-label="İstatistik bölümü">
        {([['genel', 'Genel'], ['soru', 'Sorular'], ['konu', 'Konular'], ['puan', 'Puan']] as [Sekme, string][]).map(([id, t]) => (
          <button key={id} type="button" role="tab" aria-selected={sekme === id} aria-current={sekme === id ? 'page' : undefined} onClick={() => setSekme(id)}>{t}</button>
        ))}
      </div>

      {sekme === 'genel' && (genel.n === 0 ? <div className="v15-card gf15-kart">{bosSoru}</div> : <>
        <div className="v15-card gf15-kart is15-ozet">
          <Halka pct={genel.p} boyut={104} etiket={`Yüzde ${genel.p} doğru`} yazi={<span className="is15-yuzde">%{genel.p}<small>doğru</small></span>} />
          <div className="is15-uc">
            <div><span className="is15-nokta is-ok" /><small>Doğru</small><b>{genel.d}</b></div>
            <div><span className="is15-nokta is-b" /><small>Yanlış</small><b>{genel.y}</b></div>
            <div><span className="is15-nokta" /><small>Toplam</small><b>{genel.n}</b></div>
          </div>
        </div>
        <div className="v15-card gf15-kart">
          <div className="gf15-kb"><b>Günlük çözülen soru</b><span className="v15-cap">{aralikAd}</span></div>
          <Seri v={genel.gunler} tur={ayar.tur} birim="soru" />
        </div>
        <div className="v15-card gf15-kart">
          <div className="gf15-kb"><b>Derslere göre doğruluk</b><span className="v15-cap">{aralikAd}</span></div>
          {bank === null ? <p className="v15-cap">Soru bilgileri yükleniyor…</p> : (
            <ul className="gf15-mod">
              {genel.dersler.map(([g, r]) => { const p = Math.round((r.d / r.n) * 100); return (
                <li key={g}><span className="gf15-mod-ad">{g}</span><span className={`v15-bar ${ton(p)}`}><span style={{ width: `${p}%` }} /></span><span className="gf15-mod-n">%{p} <small>{r.n} soru</small></span></li>
              ); })}
            </ul>
          )}
        </div>
      </>)}

      {sekme === 'soru' && (donemSorulari.length === 0 ? <div className="v15-card gf15-kart">{bosSoru}</div> : (
        <SoruSuzgecV15 yonler={yonler} deger={suz} onChange={setSuz} kayitAnahtari="istat_soru" sonuc={suzulmus.length}>
          <div className="v15-card gf15-kart">
            <div className="gf15-kb"><b>Tek tek sorular</b><span className="v15-cap">Son sonuç · {aralikAd}</span></div>
            <div className="is15-izgara" role="list" aria-label="Soru sonuçları">
              {suzulmus.slice(0, 300).map(([id, r]) => (
                <button key={id} type="button" role="listitem" className={`is15-q ${r.c ? 'is-ok' : 'is-b'}`} onClick={() => setDetay(id)} aria-label={`${r.c ? 'Doğru' : 'Yanlış'} · ${byId.get(id)?.topic || id}`} title={byId.get(id)?.topic || id} />
              ))}
            </div>
            <div className="gf15-lej"><span><i className="is15-l-ok" /> doğru</span><span><i className="is15-l-b" /> yanlış</span></div>
          </div>
          <ul className="v15-card is15-liste" role="list">
            {suzulmus.slice(0, 60).map(([id, r]) => { const q = byId.get(id); const n = soru.get(id)?.length || 1; return (
              <li key={id}><button type="button" onClick={() => setDetay(id)}>
                <span className={`is15-nokta ${r.c ? 'is-ok' : 'is-b'}`} />
                <span className="is15-l-t"><b>{q?.stem?.slice(0, 100) || 'Soru bilgisi bulunamadı'}{(q?.stem?.length || 0) > 100 ? '…' : ''}</b>
                  <small>{[q && ders(q.discipline), q?.topic, q?.year, tarih(r.at), n > 1 ? `${n} kez çözüldü` : ''].filter(Boolean).join(' · ')}</small></span>
              </button></li>
            ); })}
          </ul>
          {suzulmus.length > 60 && <p className="v15-cap">İlk 60 soru listelendi; süzgeçle daralt.</p>}
        </SoruSuzgecV15>
      ))}

      {sekme === 'konu' && (konular.length === 0 && sureKonu.length === 0 ? <div className="v15-card gf15-kart">{bosSoru}</div> : <>
        {konular.length > 0 && <div className="v15-card gf15-kart">
          <div className="gf15-kb"><b>Konu performansı</b><span className="v15-cap">{aralikAd} · doğru oranı</span></div>
          <ul className="is15-konu" role="list">
            {konular.slice(0, 25).map((k) => (
              <li key={k.k}>
                <span className="is15-k-ad"><b>{k.ad}</b><small>{k.ders} · {k.n} soru · son {k.t < 1 ? 'bugün' : `${Math.floor(k.t)} gün önce`}</small></span>
                <span className={`v15-bar ${ton(k.p)}`}><span style={{ width: `${k.p}%` }} /></span>
                <span className="gf15-mod-n">%{k.p}</span>
              </li>
            ))}
          </ul>
        </div>}
        {ayar.egri && konular.length > 0 && <UnutmaEgrisi konular={konular} />}
        <div className="v15-card gf15-kart">
          <div className="gf15-kb"><b>Konu başına süre</b><span className="v15-cap">Çalışma takibi · {aralikAd}</span></div>
          {sureKonu.length ? (
            <ul className="gf15-mod">
              {sureKonu.map(([id, r]) => (
                <li key={id}><span className="gf15-mod-ad" title={takipAd(id)}>{takipAd(id)}</span><span className="gf15-mod-bar"><span style={{ width: `${(r.sn / sureKonu[0][1].sn) * 100}%` }} /></span><span className="gf15-mod-n">{sureYaz(r.sn)}{r.soru ? <small> · {r.soru} soru</small> : null}</span></li>
              ))}
            </ul>
          ) : <p className="gf15-bos">Bu aralıkta konu süresi kaydı yok. Sesli ders, etkileşimli ders ve soru çözücüde geçen süre konu konu burada görünür.</p>}
        </div>
      </>)}

      {sekme === 'puan' && (testler.length === 0 ? <div className="v15-card gf15-kart"><p className="gf15-bos">Henüz deneme testi çözmedin. Deneme testi bitirdiğinde puanın (doğru yüzdesi) ve ders dökümü burada görünür.</p></div> : <PuanBolumu testler={testler.filter((t) => Date.parse(t.at) >= bas)} tur={ayar.tur} aralikAd={aralikAd} />)}

      {ayarAcik && (
        <div className="sz15-perde" onClick={() => setAyarAcik(false)}>
          <div className="sz15-sayfa" role="dialog" aria-modal="true" aria-label="Grafik ayarları" onClick={(e) => e.stopPropagation()}>
            <div className="sz15-sayfa-b"><b>Grafik ayarları</b><button type="button" className="v15-ib" onClick={() => setAyarAcik(false)} aria-label="Kapat"><X aria-hidden /></button></div>
            <span className="v15-label">Zaman aralığı</span>
            <div className="v15-seg">
              {([[7, '7 gün'], [30, '30 gün'], [90, '90 gün'], [0, 'Tümü']] as [Ayar['aralik'], string][]).map(([v, t]) => (
                <button key={v} type="button" aria-current={ayar.aralik === v ? 'page' : undefined} onClick={() => setAyar({ ...ayar, aralik: v })}>{t}</button>
              ))}
            </div>
            <span className="v15-label">Grafik türü</span>
            <div className="is15-tur">
              {([['cubuk', 'Çubuk'], ['cizgi', 'Çizgi']] as [Ayar['tur'], string][]).map(([v, t]) => (
                <button key={v} type="button" className={`v15-card${ayar.tur === v ? ' is-on' : ''}`} aria-pressed={ayar.tur === v} onClick={() => setAyar({ ...ayar, tur: v })}>
                  <Seri v={[3, 5, 2, 6, 4].map((d, i) => ({ e: String(i), d }))} tur={v} birim="örnek" /><span>{t}{ayar.tur === v && <Check aria-hidden />}</span>
                </button>
              ))}
            </div>
            <label className="is15-anahtar"><span>Unutma eğrisini göster</span><input type="checkbox" checked={ayar.egri} onChange={(e) => setAyar({ ...ayar, egri: e.target.checked })} /></label>
            <p className="v15-cap">Ayarlar yalnız bu cihazda saklanır. Üstteki çalışma grafikleri sayfanın dönem seçimini izler.</p>
            <div className="is15-alt">
              <button type="button" className="v15-btn is-ghost" onClick={() => setAyar(AYAR0)}>Varsayılana dön</button>
              <button type="button" className="v15-btn" onClick={() => setAyarAcik(false)}>Tamam</button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

/* J02 · Unutma eğrisi: en düşük tahmini hatırlamalı 4 konu, son çözümden 30 gün ileriye */
function UnutmaEgrisi({ konular }: { konular: { k: string; ad: string; S: number; t: number; R: number; gun: Set<string> }[] }) {
  const sec = [...konular].sort((a, b) => a.R - b.R).slice(0, 4);
  const W = 360, H = 150, P = 10, GUNLER = 30;
  const x = (t: number) => P + (Math.min(GUNLER, t) / GUNLER) * (W - 2 * P);
  const y = (r: number) => P + (1 - r) * (H - 2 * P);
  const SINIF = ['is15-e1', 'is15-e2', 'is15-e3', 'is15-e4'];
  return (
    <div className="v15-card gf15-kart">
      <div className="gf15-kb"><b>Unutma eğrisi</b><span className="v15-cap">Tahmini hatırlama · son çözümden 30 gün</span></div>
      <svg className="is15-svg is15-egri" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Konulara göre tahmini hatırlama eğrileri">
        {[0.25, 0.5, 0.75].map((r) => <line key={r} x1={P} x2={W - P} y1={y(r)} y2={y(r)} className="gf15-izgara" />)}
        {sec.map((k, i) => {
          const d = Array.from({ length: 31 }, (_, t) => `${t ? 'L' : 'M'}${x(t).toFixed(1)},${y(hatirlama(t, k.S)).toFixed(1)}`).join(' ');
          return <g key={k.k} className={SINIF[i]}><path d={d} className="is15-egri-l" /><circle cx={x(k.t)} cy={y(k.R)} r="4" className="is15-egri-n"><title>{`${k.ad}: bugün ~%${Math.round(k.R * 100)}`}</title></circle></g>;
        })}
      </svg>
      <div className="is15-egri-x v15-cap" aria-hidden><span>son çözüm</span><span>15 gün</span><span>30 gün</span></div>
      <ul className="is15-egri-lej" role="list">
        {sec.map((k, i) => (
          <li key={k.k} className={SINIF[i]}><i /><span>{k.ad}</span><b>~%{Math.round(k.R * 100)}</b><small>{k.gun.size} gün çalışıldı</small></li>
        ))}
      </ul>
      <p className="v15-cap gf15-not">Tahmin: R = e^(−t/S); S = 1,5 · 2^(gün−1) (en çok 60) × (0,5 + doğru oranı). Her ayrı günde tekrar eğriyi yatıştırır. Nokta bugünkü tahmindir; ölçüm değildir.</p>
    </div>
  );
}

/* X07 · Puan: deneme testlerinin doğru yüzdesi zamanla + son testin ders dökümü */
function PuanBolumu({ testler, tur, aralikAd }: { testler: ReturnType<typeof getStatsTests>; tur: Ayar['tur']; aralikAd: string }) {
  if (!testler.length) return <div className="v15-card gf15-kart"><p className="gf15-bos">{aralikAd} içinde deneme testi yok. Grafik ayarlarından aralığı genişletebilirsin.</p></div>;
  const puan = (t: (typeof testler)[number]) => Math.round((t.correct / t.total) * 100);
  const son = testler[testler.length - 1];
  const ort = Math.round(testler.reduce((a, t) => a + puan(t), 0) / testler.length);
  const enIyi = Math.max(...testler.map(puan));
  const fark = testler.length > 1 ? puan(son) - puan(testler[testler.length - 2]) : null;
  return <>
    <div className="gf15-kpi">
      <div className="v15-card"><small>Son puan</small><b>%{puan(son)}</b></div>
      <div className="v15-card"><small>Önceki teste göre</small><b>{fark == null ? '—' : `${fark > 0 ? '+' : fark < 0 ? '−' : '±'}${Math.abs(fark)}`}</b></div>
      <div className="v15-card"><small>Ortalama</small><b>%{ort}</b></div>
      <div className="v15-card"><small>En iyi</small><b>%{enIyi}</b></div>
    </div>
    <div className="v15-card gf15-kart">
      <div className="gf15-kb"><b>Puan değişimi</b><span className="v15-cap">{testler.length} deneme · doğru yüzdesi</span></div>
      <Seri v={testler.slice(-30).map((t) => ({ e: `${tarih(t.at)} · ${t.title}`, d: puan(t) }))} tur={tur} birim="puan" tavan={100} />
    </div>
    {Object.keys(son.byDiscipline || {}).length > 0 && (
      <div className="v15-card gf15-kart">
        <div className="gf15-kb"><b>Son deneme · ders dökümü</b><span className="v15-cap">{son.title} · {tarih(son.at)}</span></div>
        <ul className="gf15-mod">
          {Object.entries(son.byDiscipline).sort((a, b) => b[1].total - a[1].total).map(([g, r]) => { const p = r.total ? Math.round((r.correct / r.total) * 100) : 0; return (
            <li key={g}><span className="gf15-mod-ad">{ders(g)}</span><span className={`v15-bar ${ton(p)}`}><span style={{ width: `${p}%` }} /></span><span className="gf15-mod-n">{r.correct}/{r.total}</span></li>
          ); })}
        </ul>
      </div>
    )}
    <ul className="v15-card is15-liste" role="list">
      {[...testler].reverse().slice(0, 20).map((t) => (
        <li key={t.id}><div className="is15-test"><span className="is15-l-t"><b>{t.title}</b><small>{tarih(t.at)} · {t.correct} D · {t.wrong} Y · {t.blank} B{t.durationSec ? ` · ${sureYaz(t.durationSec) || '<1 dk'}` : ''}</small></span><b className="is15-puan">%{puan(t)}</b></div></li>
      ))}
    </ul>
  </>;
}

/* X06 · Soru detayı: kök, şıklar (doğru işaretli) ve bu sorudaki çözüm geçmişi */
function SoruDetay({ id, q, gecmis, geri }: { id: string; q?: StudyQuestion; gecmis: { at: string; c: boolean }[]; geri: () => void }) {
  const d = gecmis.filter((g) => g.c).length;
  return (
    <section className="gf15 is15" aria-label="Soru detayı">
      <div className="is15-det-b"><button type="button" className="v15-ib" onClick={geri} aria-label="Geri"><ChevronLeft aria-hidden /></button><b>Soru detayı</b></div>
      <div className="v15-card gf15-kart is15-det">
        {q ? <>
          <span className="v15-cap">{[ders(q.discipline), q.topic, kurulAd(q.committeeId), q.year, q.number ? `${q.number}. soru` : ''].filter(Boolean).join(' · ')}</span>
          <p className="is15-kok">{q.stem}</p>
          <ul className="is15-sik" role="list">
            {q.options.map((o) => <li key={o.key} className={o.key === q.answer ? 'is-ok' : ''}><b>{o.key}</b><span>{o.text}</span>{o.key === q.answer && <Check aria-label="Doğru cevap" />}</li>)}
          </ul>
        </> : <p className="gf15-bos">Bu sorunun metni bu cihazdaki soru bankasında bulunamadı (kimlik: {id}). Çözüm geçmişi aşağıda.</p>}
      </div>
      <div className="gf15-kpi">
        <div className="v15-card"><small>Çözülme</small><b>{gecmis.length}</b></div>
        <div className="v15-card"><small>Doğru</small><b>{d}</b></div>
        <div className="v15-card"><small>Yanlış</small><b>{gecmis.length - d}</b></div>
        <div className="v15-card"><small>Başarı</small><b>{gecmis.length ? `%${Math.round((d / gecmis.length) * 100)}` : '—'}</b></div>
      </div>
      <div className="v15-card gf15-kart">
        <div className="gf15-kb"><b>Geçmiş</b><span className="v15-cap">Bu cihazdaki kayıtlar</span></div>
        {gecmis.length ? (
          <ol className="is15-gecmis">
            {[...gecmis].reverse().map((g, i) => <li key={`${g.at}${i}`}><span className={`is15-nokta ${g.c ? 'is-ok' : 'is-b'}`} /><span>{g.c ? 'Doğru' : 'Yanlış'}</span><small>{new Date(g.at).toLocaleString('tr-TR', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })}</small></li>)}
          </ol>
        ) : <p className="gf15-bos">Bu soru için kayıt yok.</p>}
        <p className="v15-cap gf15-not">Her çözümde yalnız son cevap saklanır; ilerleme sıfırlandığında önceki sonuçlar arşivden gelir.</p>
      </div>
    </section>
  );
}
