/**
 * Canlı ders · "Video oluştur": dersin PDF slaytları + okunan metin + sesinden senkron MP4 (60 fps) üretir.
 * Kodlama tamamen kullanıcının cihazında yapılır (cdVideo.ts); motor tembel yüklenir.
 * İş pencereden bağımsızdır (cdVideoIs.ts): pencere kapanınca arka planda sürer, ilerleme CdVideoRozet'te görünür.
 * Pencere gövdeye taşınır (portal): ⋯ menüsünün yığın bağlamında kalınca telefonda oynatıcı/alt çubuk altını örtüyordu.
 */
import React, { useEffect, useState, useSyncExternalStore } from 'react';
import { createPortal } from 'react-dom';
import { Clapperboard } from 'lucide-react';
import { Dialog } from '../ui/Dialog';
import { cdVideoIptal, cdVideoIsAl, cdVideoIsBaslat, cdVideoIsDinle } from './cdVideoIs';
import { cdSesKisa, cdTercihVaryant, fmtSure, type CdDetay } from './canliDersStore';
import { cdDersEtiketi } from './canliDersKategori';
import type { CdVideoCozunurluk, CdVideoIlerleme } from './cdVideo';
import { CdVideoGpu, cdYoneticiMi } from './CanliDersVideoGpu';
import '../../styles/canli-ders-cevrimdisi.css';

const COZ: CdVideoCozunurluk[] = ['720p', '1080p', '2k', '4k'];
const ETIKET: Record<CdVideoCozunurluk, string> = { '720p': '720p', '1080p': '1080p', '2k': '2K', '4k': '4K' };
const MB_SAAT: Record<CdVideoCozunurluk, number> = { '720p': 1900, '1080p': 3700, '2k': 6400, '4k': 12700 }; // üst sınır (bit hızı); sabit slaytta çok daha küçük
const dosyaAdi = (s: string) => s.replace(/[\\/:*?"<>|]+/g, ' ').replace(/\s+/g, ' ').trim();

export function VideoOlusturDugme({ detay }: { detay: CdDetay }) {
  const [acik, setAcik] = useState(false);
  const destek = typeof window !== 'undefined' && 'VideoEncoder' in window;
  return (
    <>
      <button type="button" className="cd-btn" onClick={() => setAcik(true)} disabled={!destek}
        title={destek ? 'Slayt, metin ve sesten senkron video (MP4, 60 fps) oluştur' : 'Bu tarayıcı video oluşturmayı desteklemiyor (Chrome ya da Edge kullan)'}>
        <Clapperboard aria-hidden /> Video oluştur
      </button>
      {acik && createPortal(<VideoPenceresi detay={detay} onKapat={() => setAcik(false)} />, document.body)}
    </>
  );
}

function VideoPenceresi({ detay, onKapat }: { detay: CdDetay; onKapat: () => void }) {
  const sesli = detay.varyantlar.filter((v) => v.zamanlama?.length);
  const [vid, setVid] = useState(() => (cdTercihVaryant(sesli) || sesli[0])?.id || '');
  const [coz, setCoz] = useState<CdVideoCozunurluk>('720p');
  const [uygun, setUygun] = useState<Partial<Record<CdVideoCozunurluk, boolean>>>({});
  const [hata, setHata] = useState('');
  const is = useSyncExternalStore(cdVideoIsDinle, cdVideoIsAl);
  const v = sesli.find((x) => x.id === vid);
  const buDers = is?.dersKey === detay.key;
  const ilerleme = buDers ? is!.ilerleme : null;
  const calisiyor = !!ilerleme;

  useEffect(() => {
    let canli = true;
    import('./cdVideo').then(async (m) => {
      const r: Partial<Record<CdVideoCozunurluk, boolean>> = {};
      for (const c of COZ) r[c] = !!(await m.cdVideoKodlanabilir(c));
      if (canli) setUygun(r);
    });
    return () => { canli = false; };
  }, []);

  // Kapatmak işi durdurmaz: üretim arka planda sürer
  const kapat = () => onKapat();
  const iptal = () => { if (window.confirm('Video oluşturma iptal edilsin mi?')) cdVideoIptal(); };

  const baslat = async () => {
    if (!v || is) return;
    setHata('');
    const etiket = cdDersEtiketi(detay);
    const ad = `${dosyaAdi(`${etiket} - ${detay.baslik}`)} (${ETIKET[coz]} 60fps).mp4`;
    // Chrome/Edge masaüstü: doğrudan diske yaz (büyük dosyada bellek dolmaz)
    let dosya: FileSystemWritableFileStream | undefined;
    const kaydet = (window as any).showSaveFilePicker;
    if (kaydet) {
      try {
        const h = await kaydet({ suggestedName: ad, types: [{ description: 'MP4 video', accept: { 'video/mp4': ['.mp4'] } }] });
        dosya = await h.createWritable();
      } catch (e: any) {
        if (e?.name === 'AbortError') return;
      }
    }
    const r = await cdVideoIsBaslat({ detay, varyant: v, cozunurluk: coz, etiket, ad, dosya });
    if (r === 'tamam') onKapat();
    else if (r !== 'iptal') setHata(r);
  };

  const sure = v?.sureSn || 0;
  const footer = (
    <div className="cd-cd-p-alt">
      <p className="cd-cd-p-ozet" aria-live="polite">
        {calisiyor
          ? ilerleme!.asama === 'hazirlik' ? 'Hazırlanıyor…' : ilerleme!.asama === 'bitiriliyor' ? 'Dosya tamamlanıyor…'
            : `%${Math.floor(ilerleme!.oran * 100)} · ${fmtSure(ilerleme!.t)} / ${fmtSure(ilerleme!.sure)}${ilerleme!.kalanSn != null ? ` · ~${fmtSure(ilerleme!.kalanSn)} kaldı` : ''}`
          : sure ? `${fmtSure(sure)} · en çok ~${Math.round((MB_SAAT[coz] * sure) / 3600)} MB` : ''}
      </p>
      <div className="cd-cd-p-eylem">
        {calisiyor ? (
          <>
            <button type="button" className="ms-btn is-ghost" onClick={iptal}>İptal</button>
            <button type="button" className="ms-btn is-primary" onClick={kapat}>Arka planda sürdür</button>
          </>
        ) : (
          <>
            <button type="button" className="ms-btn is-ghost" onClick={kapat}>Vazgeç</button>
            <button type="button" className="ms-btn is-primary" onClick={baslat} disabled={!v || !uygun[coz] || !!is}><Clapperboard aria-hidden /> Oluştur</button>
          </>
        )}
      </div>
    </div>
  );

  return (
    <Dialog title="Video oluştur" subtitle={detay.baslik} onClose={kapat} footer={footer} width="max-w-md">
      <div className="cd-cd-p cd-vid">
        <p className="cd-vid-not">Slaytlar, okunan metin (kelime kelime) ve ses senkron bir MP4 videoda birleşir. Video bu cihazda oluşturulur; başlayınca pencereyi kapatıp başka sayfaya ya da sekmeye geçebilirsin. Sekmeyi kapatma; telefonda ekran kilitlenirse üretim duraklar.</p>
        {is && !buDers && <p className="cd-vid-hata">Şu an başka bir dersin videosu oluşturuluyor ({is.baslik}). Bitince yenisini başlatabilirsin.</p>}
        <fieldset className="cd-vid-grup" disabled={!!is}>
          <legend>Çözünürlük (60 fps)</legend>
          <div className="cd-vid-secim">
            {COZ.map((c) => (
              <label key={c} className={`cd-vid-sec${coz === c ? ' is-on' : ''}${uygun[c] === false ? ' is-yok' : ''}`}
                title={uygun[c] === false ? 'Bu cihaz bu çözünürlüğü kodlayamıyor' : undefined}>
                <input type="radio" name="cd-vid-coz" value={c} checked={coz === c} disabled={uygun[c] === false} onChange={() => setCoz(c)} />
                {ETIKET[c]}
              </label>
            ))}
          </div>
        </fieldset>
        {sesli.length > 1 && (
          <label className="cd-vid-grup">
            <span>Ses</span>
            <select value={vid} onChange={(e) => setVid(e.target.value)} disabled={!!is}>
              {sesli.map((x) => <option key={x.id} value={x.id}>{cdSesKisa(x)}</option>)}
            </select>
          </label>
        )}
        {!sesli.length && <p className="cd-vid-hata">Bu dersin sesinde zamanlama yok; video oluşturulamaz.</p>}
        {calisiyor && <progress className="cd-vid-bar" max={1} value={ilerleme!.oran} />}
        {hata && <p className="cd-vid-hata" role="alert">{hata}</p>}
        {cdYoneticiMi() && sesli.length > 0 && <CdVideoGpu dersKey={detay.key} vid={vid} cozunurluk={coz} />}
      </div>
    </Dialog>
  );
}

