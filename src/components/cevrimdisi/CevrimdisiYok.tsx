/**
 * İnternet yokken açılamayan bölüm için sade bilgi ekranı (App.wrapLazy ve kök hata sınırı kullanır). Bağlantı gelince sayfa
 * kendiliğinden yenilenir; kullanıcı Çevrimdışı merkezine geçip bölümü cihaza alabilir. Stil: index.css (.cv-yok).
 */
import React, { useEffect } from 'react';
import { CloudOff } from 'lucide-react';

export default function CevrimdisiYok({ baslik = 'Bu bölüm cihazında yok' }: { baslik?: string }) {
  useEffect(() => {
    const f = () => window.location.reload();
    window.addEventListener('online', f);
    return () => window.removeEventListener('online', f);
  }, []);
  return (
    <div className="cv-yok" role="status">
      <CloudOff aria-hidden="true" />
      <b>{baslik}</b>
      <p>İnternet bağlantısı yok ve bu bölüm henüz indirilmemiş. Bağlantı gelince sayfa kendiliğinden açılır. İnternetsiz kullanmak için Çevrimdışı sayfasından indirebilirsin.</p>
      <div>
        <button type="button" className="ui-btn" onClick={() => (window.history.length > 1 ? window.history.back() : (window.location.href = '/'))}>Geri dön</button>
        <button type="button" className="ui-btn is-primary" onClick={() => { window.location.href = '/cevrimdisi'; }}>Çevrimdışı sayfası</button>
      </div>
    </div>
  );
}
