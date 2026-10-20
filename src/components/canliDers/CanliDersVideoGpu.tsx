/**
 * "Video oluştur" penceresi › yalnız yönetici: videoyu yerel bilgisayarın GPU'sunda (NVENC) üretme kuyruğu.
 * Sunucu: src/services/dersVideoIs.ts · işçi: scripts/ders_video/video_uret.py (meds-ders-video; AGENTS.md §10 beşinci istisna).
 */
import React, { useCallback, useEffect, useState } from 'react';
import { Cpu, Download, X } from 'lucide-react';
import { safeJsonFetch, getCustomApiUrl } from '../../services/api';
import { ADMIN_EMAIL, auth, getLocalAdminSession } from '../../services/auth';
import { fmtMb } from './canliDersStore';

interface Is { id: string; key: string; vid: string; cozunurluk: string; durum: string; oran?: number; mesaj?: string; bayt?: number; istendi: string }
interface Liste { isler: Is[]; isci: { gorulme: string; gpu?: string } | null }

const DURUM: Record<string, string> = { bekliyor: 'Sırada', calisiyor: 'Üretiliyor', bitti: 'Hazır', hata: 'Hata', iptal: 'İptal edildi' };

export const cdYoneticiMi = () =>
  String(auth?.currentUser?.email || '').toLowerCase() === ADMIN_EMAIL || !!getLocalAdminSession();

export function CdVideoGpu({ dersKey, vid, cozunurluk }: { dersKey: string; vid: string; cozunurluk: string }) {
  const [liste, setListe] = useState<Liste | null>(null);
  const [hata, setHata] = useState('');
  const yenile = useCallback(async () => {
    const r = await safeJsonFetch<Liste>('/api/canli-ders/video-is');
    if (r.ok && r.data) setListe(r.data); else setHata(r.error || 'Kuyruk okunamadı.');
  }, []);
  useEffect(() => {
    void yenile();
    const t = window.setInterval(yenile, 5000);
    return () => window.clearInterval(t);
  }, [yenile]);

  const iste = async () => {
    setHata('');
    const r = await safeJsonFetch('/api/canli-ders/video-is', {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'x-admin-email': ADMIN_EMAIL }, body: JSON.stringify({ key: dersKey, vid, cozunurluk }),
    });
    if (!r.ok) setHata(r.error || 'İş eklenemedi.');
    void yenile();
  };
  const iptal = async (id: string) => { await safeJsonFetch(`/api/canli-ders/video-is/${id}`, { method: 'DELETE', headers: { 'x-admin-email': ADMIN_EMAIL } }); void yenile(); };
  // x-admin-email yalnız genel yazma kapısını geçer; asıl yetki uçta Firebase yönetici jetonuyla (isStrongAdmin) denetlenir
  const indir = async (id: string) => {
    const r = await safeJsonFetch<{ url: string }>(`/api/canli-ders/video-is/${id}/baglanti`);
    if (!r.ok || !r.data) { setHata(r.error || 'Bağlantı alınamadı.'); return; }
    const a = document.createElement('a');
    a.href = `${(getCustomApiUrl(r.data.url) || '').replace(/\/$/, '')}${r.data.url}`;
    a.download = '';
    a.click();
  };

  const isler = (liste?.isler || []).filter((x) => x.key === dersKey);
  const gorulme = liste?.isci ? (Date.now() - Date.parse(liste.isci.gorulme)) / 1000 : Infinity;
  const isciDurum = gorulme > 300 ? 'İşçi çevrimdışı (yerel bilgisayar kapalı ya da meds-ders-video çalışmıyor)'
    : liste?.isci?.gpu && liste.isci.gpu !== 'hazır' ? `GPU hazır değil: ${liste.isci.gpu}` : 'GPU işçisi hazır';

  return (
    <section className="cd-vid-gpu" aria-label="Yerel GPU (yönetici)">
      <div className="cd-vid-gpu-bas">
        <span><Cpu aria-hidden /> Yerel GPU'da üret <small>yalnız yönetici</small></span>
        <button type="button" className="ms-btn" onClick={iste} disabled={!vid}>Kuyruğa ekle</button>
      </div>
      <p className={`cd-vid-not${gorulme > 300 || (liste?.isci?.gpu && liste.isci.gpu !== 'hazır') ? ' is-uyari' : ''}`}>{liste ? isciDurum : 'Kuyruk yükleniyor…'}</p>
      {isler.length > 0 && (
        <ul className="cd-vid-gpu-liste">
          {isler.map((x) => (
            <li key={x.id}>
              <span className="tk-mono">{x.cozunurluk}</span>
              <span>{DURUM[x.durum] || x.durum}{x.durum === 'calisiyor' && x.oran != null ? ` · %${Math.floor(x.oran * 100)}` : ''}{x.durum === 'bitti' && x.bayt ? ` · ${fmtMb(x.bayt)}` : ''}{x.mesaj && x.durum === 'hata' ? ` · ${x.mesaj}` : ''}</span>
              {x.durum === 'bitti' && <button type="button" className="ms-btn is-ghost" onClick={() => indir(x.id)} aria-label="İndir"><Download aria-hidden /></button>}
              <button type="button" className="ms-btn is-ghost" onClick={() => iptal(x.id)} aria-label={x.durum === 'bekliyor' || x.durum === 'calisiyor' ? 'İptal et' : 'Sil'}><X aria-hidden /></button>
            </li>
          ))}
        </ul>
      )}
      {hata && <p className="cd-vid-hata" role="alert">{hata}</p>}
    </section>
  );
}
