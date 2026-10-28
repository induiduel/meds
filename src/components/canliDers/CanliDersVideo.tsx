/**
 * Canlı ders · "Video oluştur": dersin PDF slaytları + okunan metin + sesinden senkron video üretir.
 * Pencere dört adımlıdır: Biçim (kap/kodek, çözünürlük, fps, kalite, ses) → Düzen (slayt + metin, altyazı, yalnız slayt…)
 * → Altyazı (boyut, satır, zemin, vurgu, renk, konum) → Soru çözücü (dersin örnek soruları ders sonunda otomatik çözülür).
 * Üstte seçimlerin canlı önizlemesi (videoyla aynı çizim kodu). Kodlama kullanıcının cihazında, video işçisinde yürür
 * (cdVideoIsci.ts); iş pencereden bağımsızdır (cdVideoIs.ts), ilerleme CdVideoRozet'te görünür.
 */
import React, { useEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react';
import { Check, ChevronLeft, ChevronRight, Clapperboard } from 'lucide-react';
import { Dialog } from '../ui/Dialog';
import { cdVideoBildirimIzni, cdVideoIptal, cdVideoIsAl, cdVideoIsBaslat, cdVideoIsDinle } from './cdVideoIs';
import { cdSesKisa, cdTercihVaryant, fmtSure, type CdDetay } from './canliDersStore';
import { cdDersEtiketi } from './canliDersKategori';
import {
  CD_VIDEO_BICIM, CD_VIDEO_BOYUT, CD_VIDEO_VARSAYILAN, CD_VURGU_RENK, cdVideoBitHizi, cdVideoMetinli,
  type CdAltyaziAyar, type CdVideoAyar, type CdVideoBicim, type CdVideoCozunurluk, type CdVideoDuzen, type CdVideoFps, type CdVideoKalite, type CdVideoSoru,
} from './cdVideoCiz';
import type { CdOnizleyici, CdSoruKaynak } from './cdVideo';
import { CdVideoGpu, cdYoneticiMi } from './CanliDersVideoGpu';
import '../../styles/canli-ders-cevrimdisi.css';

const COZ: CdVideoCozunurluk[] = ['720p', '1080p', '2k', '4k'];
const BICIMLER: CdVideoBicim[] = ['mp4-avc', 'mp4-hevc', 'webm-vp9'];
const FPSLER: CdVideoFps[] = [24, 30, 60];
const KALITE: { id: CdVideoKalite; ad: string; not: string }[] = [
  { id: 'dengeli', ad: 'Dengeli', not: 'Küçük dosya' },
  { id: 'yuksek', ad: 'Yüksek', not: 'Önerilen' },
  { id: 'en-yuksek', ad: 'En yüksek', not: 'Büyük dosya' },
];
const DUZENLER: { id: CdVideoDuzen; ad: string; not: string }[] = [
  { id: 'alt', ad: 'Slayt + metin', not: 'Slayt üstte, okunan cümle altta panelde' },
  { id: 'yan', ad: 'Slayt + yan metin', not: 'Slayt solda, okunan metin sağda' },
  { id: 'altyazi', ad: 'Slayt + altyazı', not: 'Slayt tam alan, altyazı üstüne biner' },
  { id: 'slayt', ad: 'Yalnız slayt', not: 'Metinsiz, temiz slayt görüntüsü' },
  { id: 'metin', ad: 'Yalnız metin', not: 'Slaytsız, büyük okunur metin' },
];
const BOYUTLAR: { id: CdAltyaziAyar['boyut']; ad: string }[] = [{ id: 'k', ad: 'Küçük' }, { id: 'o', ad: 'Orta' }, { id: 'b', ad: 'Büyük' }, { id: 'cb', ad: 'Çok büyük' }];
const ZEMINLER: { id: CdAltyaziAyar['zemin']; ad: string }[] = [{ id: 'kutu', ad: 'Koyu kutu' }, { id: 'yari', ad: 'Yarı saydam' }, { id: 'kontur', ad: 'Zeminsiz (kontur)' }];
const RENK_AD: Record<CdAltyaziAyar['renk'], string> = { sari: 'Sarı', turkuaz: 'Turkuaz', yesil: 'Yeşil', pembe: 'Pembe' };
const ADIMLAR = ['Biçim', 'Düzen', 'Altyazı', 'Soru çözücü'] as const;
const AYAR_KEY = 'medsoru_cd_video_ayar_v1';

const dosyaAdi = (s: string) => s.replace(/[\\/:*?"<>|]+/g, ' ').replace(/\s+/g, ' ').trim();
function ayarOku(): CdVideoAyar {
  try {
    const x = JSON.parse(localStorage.getItem(AYAR_KEY) || 'null');
    if (x && typeof x === 'object') {
      const a = { ...CD_VIDEO_VARSAYILAN, ...x, altyazi: { ...CD_VIDEO_VARSAYILAN.altyazi, ...x.altyazi }, cozucu: { ...CD_VIDEO_VARSAYILAN.cozucu, ...x.cozucu } };
      // bozuk/eski değer: varsayılana dön
      if (!CD_VIDEO_BICIM[a.bicim as CdVideoBicim]) a.bicim = CD_VIDEO_VARSAYILAN.bicim;
      if (!CD_VIDEO_BOYUT[a.cozunurluk as CdVideoCozunurluk]) a.cozunurluk = CD_VIDEO_VARSAYILAN.cozunurluk;
      if (!FPSLER.includes(a.fps)) a.fps = CD_VIDEO_VARSAYILAN.fps;
      if (!DUZENLER.some((d) => d.id === a.duzen)) a.duzen = CD_VIDEO_VARSAYILAN.duzen;
      return a;
    }
  } catch { /* özel pencere / bozuk kayıt */ }
  return CD_VIDEO_VARSAYILAN;
}
const ayarYaz = (a: CdVideoAyar) => { try { localStorage.setItem(AYAR_KEY, JSON.stringify(a)); } catch { /* */ } };

export function VideoOlusturDugme({ detay }: { detay: CdDetay }) {
  const [acik, setAcik] = useState(false);
  const destek = typeof window !== 'undefined' && 'VideoEncoder' in window && 'Worker' in window;
  return (
    <>
      <button type="button" className="cd-btn" onClick={() => setAcik(true)} disabled={!destek}
        title={destek ? 'Slayt, metin ve sesten senkron video oluştur' : 'Bu tarayıcı video oluşturmayı desteklemiyor (Chrome, Edge ya da güncel Safari kullan)'}>
        <Clapperboard aria-hidden /> Video oluştur
      </button>
      {acik && <VideoPenceresi detay={detay} onKapat={() => setAcik(false)} />}
    </>
  );
}

/** Tek seçimli düğme grubu */
function Secim<T extends string | number>({ ad, deger, secenekler, onSec, sutun, kapali }: {
  ad: string; deger: T; secenekler: { id: T; ad: React.ReactNode; not?: string; yok?: boolean }[]; onSec: (v: T) => void; sutun?: number; kapali?: boolean;
}) {
  return (
    <fieldset className="cd-vid-grup" disabled={kapali}>
      <legend>{ad}</legend>
      <div className="cd-vid-secim" style={{ gridTemplateColumns: `repeat(${sutun || secenekler.length}, minmax(0, 1fr))` }}>
        {secenekler.map((s) => (
          <label key={String(s.id)} className={`cd-vid-sec${deger === s.id ? ' is-on' : ''}${s.yok ? ' is-yok' : ''}${s.not ? ' is-iki' : ''}`}
            title={s.yok ? 'Bu cihaz bunu desteklemiyor' : undefined}>
            <input type="radio" name={ad} checked={deger === s.id} disabled={s.yok} onChange={() => onSec(s.id)} />
            <b>{s.ad}</b>
            {s.not && <small>{s.not}</small>}
          </label>
        ))}
      </div>
    </fieldset>
  );
}
function Anahtar({ ad, not, deger, onDegis, kapali }: { ad: string; not?: string; deger: boolean; onDegis: (v: boolean) => void; kapali?: boolean }) {
  return (
    <label className={`cd-vid-anahtar${kapali ? ' is-kapali' : ''}`}>
      <span><b>{ad}</b>{not && <small>{not}</small>}</span>
      <input type="checkbox" role="switch" checked={deger} disabled={kapali} onChange={(e) => onDegis(e.target.checked)} />
    </label>
  );
}

function VideoPenceresi({ detay, onKapat }: { detay: CdDetay; onKapat: () => void }) {
  const sesli = detay.varyantlar.filter((v) => v.zamanlama?.length);
  const [vid, setVid] = useState(() => (cdTercihVaryant(sesli) || sesli[0])?.id || '');
  const [ayar, setAyarHam] = useState<CdVideoAyar>(ayarOku);
  const setAyar = (f: (a: CdVideoAyar) => CdVideoAyar) => setAyarHam((a) => { const y = f(a); ayarYaz(y); return y; });
  const altyazi = (p: Partial<CdAltyaziAyar>) => setAyar((a) => ({ ...a, altyazi: { ...a.altyazi, ...p } }));
  const [adim, setAdim] = useState(0);
  const [uygun, setUygun] = useState<Record<string, boolean>>({});
  const [sesKod, setSesKod] = useState<Partial<Record<CdVideoBicim, boolean>>>({});
  const [kaynak, setKaynak] = useState<CdSoruKaynak | null | undefined>(undefined);
  const [sorular, setSorular] = useState<CdVideoSoru[] | null>(null);
  const [onizKip, setOnizKip] = useState<'ders' | 'soru'>('ders');
  const [hata, setHata] = useState('');
  const is = useSyncExternalStore(cdVideoIsDinle, cdVideoIsAl);
  const v = sesli.find((x) => x.id === vid);
  const buDers = is?.dersKey === detay.key;
  const ilerleme = buDers ? is!.ilerleme : null;
  const calisiyor = !!ilerleme;
  const etiket = cdDersEtiketi(detay);

  // cihaz yetenekleri: her biçim × çözünürlük (seçili fps/kalite ile)
  useEffect(() => {
    let canli = true;
    import('./cdVideo').then(async (m) => {
      const r: Record<string, boolean> = {};
      for (const b of BICIMLER) for (const c of COZ) r[`${b}|${c}`] = await m.cdVideoKodlanabilir({ bicim: b, cozunurluk: c, fps: ayar.fps, kalite: ayar.kalite });
      const s: Partial<Record<CdVideoBicim, boolean>> = {};
      for (const b of BICIMLER) s[b] = await m.cdSesKodlanabilir(b);
      if (canli) { setUygun(r); setSesKod(s); }
    });
    return () => { canli = false; };
  }, [ayar.fps, ayar.kalite]);
  // dersin soru çözücüsü
  useEffect(() => {
    let canli = true;
    import('./cdVideo').then((m) => m.cdCozucuBul(detay)).then((k) => { if (canli) setKaynak(k); }, () => canli && setKaynak(null));
    return () => { canli = false; };
  }, [detay]);
  useEffect(() => {
    if (!kaynak) { setSorular(kaynak === null ? [] : null); return; }
    let canli = true;
    setSorular(null);
    import('./cdVideo').then((m) => m.cdVideoSorulari(kaynak, ayar.cozucu.tur)).then((s) => { if (canli) setSorular(s); }, () => canli && setSorular([]));
    return () => { canli = false; };
  }, [kaynak, ayar.cozucu.tur]);

  // seçilen biçim/çözünürlük bu cihazda yoksa ilk uygun olana geç
  const uygunMu = (b: CdVideoBicim, c: CdVideoCozunurluk) => uygun[`${b}|${c}`] !== false;
  useEffect(() => {
    if (!Object.keys(uygun).length || uygunMu(ayar.bicim, ayar.cozunurluk)) return;
    const c = COZ.find((x) => uygunMu(ayar.bicim, x));
    if (c) setAyar((a) => ({ ...a, cozunurluk: c }));
    else { const b = BICIMLER.find((x) => COZ.some((y) => uygunMu(x, y))); if (b) setAyar((a) => ({ ...a, bicim: b })); }
  }, [uygun]); // eslint-disable-line react-hooks/exhaustive-deps

  const cozucuMumkun = !!sorular?.length && sesKod[ayar.bicim] !== false;
  const cozucuEtkin = ayar.cozucu.acik && cozucuMumkun;
  const webmSesYok = CD_VIDEO_BICIM[ayar.bicim].kap === 'webm' && sesKod[ayar.bicim] === false;
  const metinli = cdVideoMetinli(ayar.duzen);
  const gorunurAdimlar = ADIMLAR.map((_, i) => i).filter((i) => i !== 2 || metinli);

  // önizleme
  const tuval = useRef<HTMLCanvasElement>(null);
  const oniz = useRef<CdOnizleyici | null>(null);
  const [onizHazir, setOnizHazir] = useState(false);
  useEffect(() => {
    if (!v || !tuval.current) return;
    let canli = true;
    import('./cdVideo').then((m) => {
      if (!canli || !tuval.current) return;
      oniz.current?.kapat();
      oniz.current = m.cdVideoOnizleyici(tuval.current, detay, v, etiket);
      setOnizHazir(true);
    });
    return () => { canli = false; oniz.current?.kapat(); oniz.current = null; setOnizHazir(false); };
  }, [detay, v, etiket]);
  const etkinAyar = useMemo(() => ({ ...ayar, cozucu: { ...ayar.cozucu, acik: cozucuEtkin } }), [ayar, cozucuEtkin]);
  useEffect(() => {
    if (!onizHazir || !oniz.current) return;
    const kip = onizKip === 'soru' && cozucuEtkin && sorular?.length ? 'soru' : 'ders';
    void oniz.current.ciz(etkinAyar, kip, sorular || []);
  }, [onizHazir, etkinAyar, onizKip, sorular, cozucuEtkin]);
  useEffect(() => { setOnizKip(adim === 3 && cozucuEtkin ? 'soru' : 'ders'); }, [adim, cozucuEtkin]);

  const kapat = () => onKapat();
  const iptal = () => { if (window.confirm('Video oluşturma iptal edilsin mi?')) cdVideoIptal(); };

  const sesSure = v?.sureSn || 0;
  const soruSure = cozucuEtkin && sorular ? sorular.reduce((t, q) => t + q.q.sure + q.c.sure + ayar.cozucu.dusunSn + 2.4, 3) : 0;
  const toplamSure = sesSure + soruSure;
  const mb = Math.round(((cdVideoBitHizi(ayar) + 128_000) * toplamSure) / 8 / 1e6);
  const uzanti = CD_VIDEO_BICIM[ayar.bicim].kap;

  const baslat = async () => {
    if (!v || is) return;
    setHata('');
    if (!uygunMu(ayar.bicim, ayar.cozunurluk)) { setHata('Bu cihaz seçilen biçim ve çözünürlüğü kodlayamıyor.'); setAdim(0); return; }
    if (webmSesYok) { setHata('Bu tarayıcı WebM sesini kodlayamıyor; MP4 seç.'); setAdim(0); return; }
    const ad = `${dosyaAdi(`${etiket} - ${detay.baslik}`)} (${CD_VIDEO_BOYUT[ayar.cozunurluk].etiket} ${ayar.fps}fps).${uzanti}`;
    if (ayar.bildirim) cdVideoBildirimIzni();
    // Chrome/Edge masaüstü: doğrudan diske yaz (büyük dosyada bellek dolmaz)
    let dosya: FileSystemFileHandle | undefined;
    const kaydet = (window as any).showSaveFilePicker;
    if (kaydet) {
      try {
        dosya = await kaydet({ suggestedName: ad, types: [{ description: uzanti === 'webm' ? 'WebM video' : 'MP4 video', accept: { [uzanti === 'webm' ? 'video/webm' : 'video/mp4']: [`.${uzanti}`] } }] });
      } catch (e: any) {
        if (e?.name === 'AbortError') return;
      }
    }
    const r = await cdVideoIsBaslat({ detay, varyant: v, ayar: etkinAyar, sorular: cozucuEtkin ? sorular || [] : [], etiket, ad, dosya });
    if (r === 'tamam') onKapat();
    else if (r !== 'iptal') setHata(r);
  };

  const sira = gorunurAdimlar.indexOf(adim);
  const sonAdim = sira === gorunurAdimlar.length - 1;
  const ileri = () => setAdim(gorunurAdimlar[Math.min(gorunurAdimlar.length - 1, sira + 1)]);
  const geri = () => setAdim(gorunurAdimlar[Math.max(0, sira - 1)]);

  const footer = (
    <div className="cd-cd-p-alt">
      <p className="cd-cd-p-ozet" aria-live="polite">
        {calisiyor
          ? ilerleme!.asama === 'hazirlik' ? 'Hazırlanıyor…' : ilerleme!.asama === 'bitiriliyor' ? 'Dosya tamamlanıyor…'
            : `%${Math.floor(ilerleme!.oran * 100)} · ${fmtSure(ilerleme!.t)} / ${fmtSure(ilerleme!.sure)}${ilerleme!.kalanSn != null ? ` · ~${fmtSure(ilerleme!.kalanSn)} kaldı` : ''}`
          : toplamSure ? `${fmtSure(toplamSure)} · en çok ~${mb} MB` : ''}
      </p>
      <div className="cd-cd-p-eylem">
        {calisiyor ? (
          <>
            <button type="button" className="ms-btn is-ghost" onClick={iptal}>İptal</button>
            <button type="button" className="ms-btn is-primary" onClick={kapat}>Arka planda sürdür</button>
          </>
        ) : (
          <>
            {sira > 0
              ? <button type="button" className="ms-btn is-ghost" onClick={geri}><ChevronLeft aria-hidden /> Geri</button>
              : <button type="button" className="ms-btn is-ghost" onClick={kapat}>Vazgeç</button>}
            {sonAdim
              ? <button type="button" className="ms-btn is-primary" onClick={baslat} disabled={!v || !!is}><Clapperboard aria-hidden /> Oluştur</button>
              : <button type="button" className="ms-btn is-primary" onClick={ileri}>İleri <ChevronRight aria-hidden /></button>}
          </>
        )}
      </div>
    </div>
  );

  return (
    <Dialog title="Video oluştur" subtitle={detay.baslik} onClose={kapat} footer={footer} width="max-w-2xl">
      <div className="cd-cd-p cd-vid">
        {is && !buDers && <p className="cd-vid-hata">Şu an başka bir dersin videosu oluşturuluyor ({is.baslik}). Bitince yenisini başlatabilirsin.</p>}
        {!sesli.length && <p className="cd-vid-hata">Bu dersin sesinde zamanlama yok; video oluşturulamaz.</p>}

        {calisiyor ? (
          <div className="cd-vid-calisiyor">
            <progress className="cd-vid-bar" max={1} value={ilerleme!.oran} />
            <p className="cd-vid-not">Video bu cihazda, arka plandaki ayrı bir işlemde oluşturuluyor. Bu pencereyi kapatabilir, başka sayfaya ya da sekmeye geçebilir, tarayıcıyı simge durumuna küçültebilirsin; ilerleme sağ altta görünür. Tarayıcıyı ya da bu sekmeyi kapatırsan üretim durur.</p>
          </div>
        ) : (
          <>
            <ol className="cd-vid-adimlar" aria-label="Adımlar">
              {gorunurAdimlar.map((i, n) => (
                <li key={i}>
                  <button type="button" className={`cd-vid-adim${i === adim ? ' is-on' : ''}${n < sira ? ' is-tamam' : ''}`} aria-current={i === adim ? 'step' : undefined} onClick={() => setAdim(i)}>
                    <i aria-hidden>{n < sira ? <Check /> : n + 1}</i>{ADIMLAR[i]}
                  </button>
                </li>
              ))}
            </ol>

            <figure className="cd-vid-oniz">
              <canvas ref={tuval} width={640} height={360} aria-label="Video önizlemesi" />
              <figcaption>
                Önizleme
                {cozucuEtkin && (
                  <span className="cd-vid-oniz-kip" role="group" aria-label="Önizleme sahnesi">
                    <button type="button" className={onizKip === 'ders' ? 'is-on' : ''} onClick={() => setOnizKip('ders')}>Ders</button>
                    <button type="button" className={onizKip === 'soru' ? 'is-on' : ''} onClick={() => setOnizKip('soru')}>Soru</button>
                  </span>
                )}
              </figcaption>
            </figure>

            {adim === 0 && (
              <div className="cd-vid-govde">
                <Secim ad="Biçim" deger={ayar.bicim} sutun={3} onSec={(b) => setAyar((a) => ({ ...a, bicim: b }))}
                  secenekler={BICIMLER.map((b) => ({ id: b, ad: CD_VIDEO_BICIM[b].etiket, not: CD_VIDEO_BICIM[b].aciklama, yok: Object.keys(uygun).length > 0 && !COZ.some((c) => uygunMu(b, c)) }))} />
                <Secim ad="Çözünürlük" deger={ayar.cozunurluk} onSec={(c) => setAyar((a) => ({ ...a, cozunurluk: c }))}
                  secenekler={COZ.map((c) => ({ id: c, ad: CD_VIDEO_BOYUT[c].etiket, yok: !uygunMu(ayar.bicim, c) }))} />
                <Secim ad="Kare hızı" deger={ayar.fps} onSec={(f) => setAyar((a) => ({ ...a, fps: f }))}
                  secenekler={FPSLER.map((f) => ({ id: f, ad: `${f} fps`, not: f === 24 ? 'Sinema' : f === 30 ? 'Önerilen' : 'En akıcı' }))} />
                <Secim ad="Kalite" deger={ayar.kalite} onSec={(k) => setAyar((a) => ({ ...a, kalite: k }))}
                  secenekler={KALITE.map((k) => ({ id: k.id, ad: k.ad, not: k.not }))} />
                {sesli.length > 1 && (
                  <label className="cd-vid-grup">
                    <span>Ses</span>
                    <select value={vid} onChange={(e) => setVid(e.target.value)}>
                      {sesli.map((x) => <option key={x.id} value={x.id}>{cdSesKisa(x)}</option>)}
                    </select>
                  </label>
                )}
                <p className="cd-vid-not">
                  {CD_VIDEO_BICIM[ayar.bicim].kap === 'mp4' && !cozucuEtkin
                    ? 'Ses, dersin orijinal kaydından kayıpsız kopyalanır.'
                    : 'Ses 128 kbps olarak yeniden kodlanır (soru çözücü ya da WebM için gerekli).'}
                  {' '}Bit hızı ~{(cdVideoBitHizi(ayar) / 1e6).toFixed(1)} Mbps; slaytlar çoğunlukla durağan olduğundan dosya genelde bundan küçük olur.
                </p>
                {webmSesYok && <p className="cd-vid-hata">Bu tarayıcı WebM sesini kodlayamıyor; MP4 seç.</p>}
                {cdYoneticiMi() && sesli.length > 0 && <CdVideoGpu dersKey={detay.key} vid={vid} cozunurluk={ayar.cozunurluk} />}
              </div>
            )}

            {adim === 1 && (
              <div className="cd-vid-govde">
                <fieldset className="cd-vid-grup">
                  <legend>Düzen</legend>
                  <div className="cd-vid-duzenler">
                    {DUZENLER.map((d) => (
                      <label key={d.id} className={`cd-vid-duzen${ayar.duzen === d.id ? ' is-on' : ''}`}>
                        <input type="radio" name="cd-vid-duzen" checked={ayar.duzen === d.id} onChange={() => setAyar((a) => ({ ...a, duzen: d.id }))} />
                        <DuzenSimge id={d.id} />
                        <b>{d.ad}</b>
                        <small>{d.not}</small>
                      </label>
                    ))}
                  </div>
                </fieldset>
                <Secim ad="Tema" deger={ayar.tema} onSec={(t) => setAyar((a) => ({ ...a, tema: t }))}
                  secenekler={[{ id: 'koyu' as const, ad: 'Koyu' }, { id: 'acik' as const, ad: 'Açık' }]} />
                <div className="cd-vid-anahtarlar">
                  <Anahtar ad="Başlık şeridi" not="Ders adı ve bölüm üstte" deger={ayar.baslikSerit} onDegis={(x) => setAyar((a) => ({ ...a, baslikSerit: x }))} />
                  <Anahtar ad="İlerleme çubuğu" not="Altta ince süre çizgisi" deger={ayar.ilerleme} onDegis={(x) => setAyar((a) => ({ ...a, ilerleme: x }))} />
                  <Anahtar ad="Slaytta okunan yeri işaretle" not="Okunan satır ve kelime" deger={ayar.slaytIsaret} kapali={ayar.duzen === 'metin'} onDegis={(x) => setAyar((a) => ({ ...a, slaytIsaret: x }))} />
                  {!!detay.ogrenciNot && <Anahtar ad="Öğrenci notu işaretleri" not="Kırmızı işaret ve yıldızlar" deger={ayar.ogrenciNot} kapali={ayar.duzen === 'metin'} onDegis={(x) => setAyar((a) => ({ ...a, ogrenciNot: x }))} />}
                </div>
              </div>
            )}

            {adim === 2 && metinli && (
              <div className="cd-vid-govde">
                <Secim ad="Yazı boyutu" deger={ayar.altyazi.boyut} onSec={(x) => altyazi({ boyut: x })} secenekler={BOYUTLAR} />
                <Secim ad="Satır sayısı" deger={ayar.altyazi.satir} onSec={(x) => altyazi({ satir: x })} secenekler={([1, 2, 3] as const).map((n) => ({ id: n, ad: `${n} satır` }))} />
                <Secim ad="Vurgu" deger={ayar.altyazi.vurgu} onSec={(x) => altyazi({ vurgu: x })}
                  secenekler={[{ id: 'kelime' as const, ad: 'Kelime kelime', not: 'Okunan kelime parlar' }, { id: 'cumle' as const, ad: 'Düz cümle', not: 'Vurgusuz' }]} />
                <fieldset className="cd-vid-grup">
                  <legend>Vurgu rengi</legend>
                  <div className="cd-vid-renkler">
                    {(Object.keys(CD_VURGU_RENK) as CdAltyaziAyar['renk'][]).map((r) => (
                      <label key={r} className={`cd-vid-renk${ayar.altyazi.renk === r ? ' is-on' : ''}`}>
                        <input type="radio" name="cd-vid-renk" checked={ayar.altyazi.renk === r} onChange={() => altyazi({ renk: r })} />
                        <i style={{ background: CD_VURGU_RENK[r] }} aria-hidden />{RENK_AD[r]}
                      </label>
                    ))}
                  </div>
                </fieldset>
                {ayar.duzen === 'altyazi' && (
                  <>
                    <Secim ad="Altyazı zemini" deger={ayar.altyazi.zemin} onSec={(x) => altyazi({ zemin: x })} secenekler={ZEMINLER} />
                    <Secim ad="Konum" deger={ayar.altyazi.konum} onSec={(x) => altyazi({ konum: x })}
                      secenekler={[{ id: 'alt' as const, ad: 'Altta' }, { id: 'ust' as const, ad: 'Üstte' }]} />
                  </>
                )}
                <div className="cd-vid-anahtarlar">
                  <Anahtar ad="Ayrıca altyazı dosyası (.vtt)" not="Videoyla birlikte indirilir; oynatıcıda açılıp kapatılabilir" deger={ayar.vtt} onDegis={(x) => setAyar((a) => ({ ...a, vtt: x }))} />
                </div>
              </div>
            )}

            {adim === 3 && (
              <div className="cd-vid-govde">
                <div className="cd-vid-anahtarlar">
                  <Anahtar ad="Soru çözücüyü ekle" deger={ayar.cozucu.acik && cozucuMumkun} kapali={!cozucuMumkun}
                    not={sorular === null ? 'Dersin soruları aranıyor…'
                      : !sorular.length ? 'Bu ders için sesli soru çözücü bulunamadı'
                      : sesKod[ayar.bicim] === false ? 'Bu tarayıcı sesi yeniden kodlayamıyor'
                      : `Ders bitince ${sorular.length} soru otomatik çözülür`}
                    onDegis={(x) => setAyar((a) => ({ ...a, cozucu: { ...a.cozucu, acik: x } }))} />
                </div>
                <p className="cd-vid-not">Her soruda yalnız soru kökü ve şıklar okunur, kısa bir düşünme arasından sonra doğru cevap ve doğru cevabın açıklaması okunur; doğru şık ekranda işaretlenir.</p>
                {kaynak && (
                  <>
                    <Secim ad="Sorular" deger={ayar.cozucu.tur} kapali={!ayar.cozucu.acik} onSec={(x) => setAyar((a) => ({ ...a, cozucu: { ...a.cozucu, tur: x } }))}
                      secenekler={[{ id: 'hepsi' as const, ad: 'Tümü' }, { id: 'ornek' as const, ad: 'Örnek sorular' }, { id: 'cikmis' as const, ad: 'Çıkmış sorular' }]} />
                    <Secim ad="Düşünme süresi" deger={ayar.cozucu.dusunSn} kapali={!ayar.cozucu.acik} onSec={(x) => setAyar((a) => ({ ...a, cozucu: { ...a.cozucu, dusunSn: x } }))}
                      secenekler={[0, 3, 5, 10].map((n) => ({ id: n, ad: n ? `${n} sn` : 'Yok' }))} />
                  </>
                )}
                <div className="cd-vid-anahtarlar">
                  <Anahtar ad="Bitince bildir" not="Sekme arka plandayken tarayıcı bildirimi gösterilir" deger={ayar.bildirim} onDegis={(x) => setAyar((a) => ({ ...a, bildirim: x }))} />
                </div>
                <p className="cd-vid-not">Video bu cihazda, arka plandaki ayrı bir işlemde oluşturulur: başlayınca pencereyi kapatıp başka sayfaya ya da sekmeye geçebilir, tarayıcıyı küçültebilirsin. Tarayıcıyı ya da sekmeyi kapatırsan üretim durur; telefonda ekran kilitlenirse duraklar.</p>
              </div>
            )}
          </>
        )}
        {hata && <p className="cd-vid-hata" role="alert">{hata}</p>}
      </div>
    </Dialog>
  );
}

/** Düzen seçeneğinin küçük şeması */
function DuzenSimge({ id }: { id: CdVideoDuzen }) {
  const s = 'currentColor';
  return (
    <svg viewBox="0 0 64 36" className="cd-vid-duzen-simge" aria-hidden>
      <rect x=".5" y=".5" width="63" height="35" rx="4" fill="none" stroke={s} opacity=".35" />
      {id === 'alt' && <><rect x="6" y="4" width="52" height="20" rx="2" fill={s} opacity=".28" /><rect x="10" y="27" width="44" height="2.6" rx="1.3" fill={s} /><rect x="10" y="31" width="30" height="2.6" rx="1.3" fill={s} opacity=".6" /></>}
      {id === 'yan' && <><rect x="4" y="5" width="38" height="26" rx="2" fill={s} opacity=".28" /><rect x="46" y="10" width="14" height="2.4" rx="1.2" fill={s} /><rect x="46" y="15" width="12" height="2.4" rx="1.2" fill={s} opacity=".6" /><rect x="46" y="20" width="13" height="2.4" rx="1.2" fill={s} opacity=".6" /></>}
      {id === 'altyazi' && <><rect x="4" y="4" width="56" height="28" rx="2" fill={s} opacity=".28" /><rect x="14" y="24" width="36" height="6" rx="2" fill={s} opacity=".85" /></>}
      {id === 'slayt' && <rect x="4" y="4" width="56" height="28" rx="2" fill={s} opacity=".28" />}
      {id === 'metin' && <><rect x="12" y="12" width="40" height="3" rx="1.5" fill={s} /><rect x="16" y="18" width="32" height="3" rx="1.5" fill={s} opacity=".6" /><rect x="20" y="24" width="24" height="3" rx="1.5" fill={s} opacity=".6" /></>}
    </svg>
  );
}
