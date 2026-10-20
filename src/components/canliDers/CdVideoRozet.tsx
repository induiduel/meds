/**
 * Video oluşturma ilerleme rozeti: App'te bir kez bağlanır, yalnız iş varken görünür (her sayfada).
 * Hafif tutulur: ağır motor ya da ders deposu yüklemez.
 */
import { useSyncExternalStore } from 'react';
import { createPortal } from 'react-dom';
import { Clapperboard, X } from 'lucide-react';
import { cdVideoIptal, cdVideoIsAl, cdVideoIsDinle } from './cdVideoIs';
import '../../styles/cd-video-rozet.css';

const sureYaz = (sn: number) => {
  const d = Math.floor(sn / 60), s = Math.floor(sn % 60);
  return d >= 60 ? `${Math.floor(d / 60)} sa ${d % 60} dk` : `${d}:${String(s).padStart(2, '0')}`;
};

/** Uygulama genelinde ilerleme rozeti (App'te bir kez): video arka planda üretilirken her sayfada görünür */
export function CdVideoRozet() {
  const is = useSyncExternalStore(cdVideoIsDinle, cdVideoIsAl);
  if (!is) return null;
  const p = is.ilerleme;
  const yazi = p.asama === 'hazirlik' ? 'Hazırlanıyor…' : p.asama === 'bitiriliyor' ? 'Tamamlanıyor…'
    : `%${Math.floor(p.oran * 100)}${p.kalanSn != null ? ` · ~${sureYaz(p.kalanSn)}` : ''}`;
  return createPortal(
    <div className="cd-vid-rozet" role="status" aria-live="off" title={`Video oluşturuluyor: ${is.baslik}`}>
      <Clapperboard aria-hidden className="cd-vid-rozet-ikon" />
      <span className="cd-vid-rozet-metin">
        <b>{is.baslik}</b>
        <span>{yazi}</span>
      </span>
      <button type="button" className="cd-vid-rozet-iptal" aria-label="Video oluşturmayı iptal et"
        onClick={() => { if (window.confirm('Video oluşturma iptal edilsin mi?')) cdVideoIptal(); }}>
        <X aria-hidden />
      </button>
      <i className="cd-vid-rozet-bar" style={{ transform: `scaleX(${p.oran})` }} aria-hidden />
    </div>,
    document.body,
  );
}
