/**
 * Canlı ders · "Video oluştur": dersin PDF slaytları + okunan metin + sesinden senkron MP4 (60 fps) üretir.
 * Kodlama tamamen kullanıcının cihazında yapılır (cdVideo.ts); motor tembel yüklenir.
 */
import React, { useEffect, useRef, useState } from 'react';
import { Clapperboard } from 'lucide-react';
import { Dialog } from '../ui/Dialog';
import { toast } from '../ui/Toast';
import { cdSesKisa, cdTercihVaryant, fmtSure, type CdDetay } from './canliDersStore';
import { cdDersEtiketi } from './canliDersKategori';
import type { CdVideoCozunurluk, CdVideoIlerleme } from './cdVideo';
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
      {acik && <VideoPenceresi detay={detay} onKapat={() => setAcik(false)} />}
    </>
  );
}

function VideoPenceresi({ detay, onKapat }: { detay: CdDetay; onKapat: () => void }) {
  const sesli = detay.varyantlar.filter((v) => v.zamanlama?.length);
  const [vid, setVid] = useState(() => (cdTercihVaryant(sesli) || sesli[0])?.id || '');
  const [coz, setCoz] = useState<CdVideoCozunurluk>('720p');
  const [uygun, setUygun] = useState<Partial<Record<CdVideoCozunurluk, boolean>>>({});
  const [ilerleme, setIlerleme] = useState<CdVideoIlerleme | null>(null);
  const [hata, setHata] = useState('');
  const iptal = useRef<AbortController | null>(null);
  const v = sesli.find((x) => x.id === vid);
  const calisiyor = !!ilerleme;

  useEffect(() => {
    let canli = true;
    import('./cdVideo').then(async (m) => {
      const r: Partial<Record<CdVideoCozunurluk, boolean>> = {};
      for (const c of COZ) r[c] = !!(await m.cdVideoKodlanabilir(c));
      if (canli) setUygun(r);
    });
    return () => { canli = false; iptal.current?.abort(); };
  }, []);

  const kapat = () => {
    if (calisiyor && !window.confirm('Video oluşturma sürüyor. İptal edilsin mi?')) return;
    iptal.current?.abort();
    onKapat();
  };

  const baslat = async () => {
    if (!v) return;
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
    const ac = new AbortController();
    iptal.current = ac;
    setIlerleme({ asama: 'hazirlik', oran: 0, t: 0, sure: 0 });
    try {
      const m = await import('./cdVideo');
      const blob = await m.cdVideoOlustur({ detay, varyant: v, cozunurluk: coz, etiket, dosya, sinyal: ac.signal, onIlerleme: setIlerleme });
      if (blob) {
        const u = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = u; a.download = ad; a.click();
        setTimeout(() => URL.revokeObjectURL(u), 60_000);
      }
      toast.success('Video hazır', ad);
      onKapat();
    } catch (e: any) {
      if (e?.name === 'AbortError') { try { await dosya?.abort(); } catch { /* */ } setIlerleme(null); return; }
      console.error('video', e);
      setHata(e?.message || 'Video oluşturulamadı.');
      setIlerleme(null);
    }
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
        <button type="button" className="ms-btn is-ghost" onClick={kapat}>{calisiyor ? 'İptal' : 'Vazgeç'}</button>
        {!calisiyor && <button type="button" className="ms-btn is-primary" onClick={baslat} disabled={!v || !uygun[coz]}><Clapperboard aria-hidden /> Oluştur</button>}
      </div>
    </div>
  );

  return (
    <Dialog title="Video oluştur" subtitle={detay.baslik} onClose={kapat} footer={footer} width="max-w-md">
      <div className="cd-cd-p cd-vid">
        <p className="cd-vid-not">Slaytlar, okunan metin (kelime kelime) ve ses senkron bir MP4 videoda birleşir. Video bu cihazda oluşturulur; sekme açık kalmalı.</p>
        <fieldset className="cd-vid-grup" disabled={calisiyor}>
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
            <select value={vid} onChange={(e) => setVid(e.target.value)} disabled={calisiyor}>
              {sesli.map((x) => <option key={x.id} value={x.id}>{cdSesKisa(x)}</option>)}
            </select>
          </label>
        )}
        {!sesli.length && <p className="cd-vid-hata">Bu dersin sesinde zamanlama yok; video oluşturulamaz.</p>}
        {calisiyor && <progress className="cd-vid-bar" max={1} value={ilerleme!.oran} />}
        {hata && <p className="cd-vid-hata" role="alert">{hata}</p>}
      </div>
    </Dialog>
  );
}
