/**
 * İçerik kilidi (2026-10-20): `tanim.json` › kilitler içindeki `tur: "icerik"` ögesi ATP ile açılmadan içeriği göstermez.
 * Yönetici ve yapay zekâ test oturumu kapıdan geçer. Kilit etkin değilse (etkin:false) içerik herkese açıktır.
 */
import React, { useState } from 'react';
import { Lock, Sparkles } from 'lucide-react';
import { kilitOnbellek, satinAl, sayi, useBasarim, yenile } from '../../services/basarimIstemci';
import { cevrimdisiGibi } from '../../services/cevrimdisi/baglanti';
import { auth, ADMIN_EMAIL } from '../../services/auth';
import { navigateTo, pathFor } from '../../router';
import { AtpIkon } from './ortak';
import '../../styles/basarim.css';

export function KilitKapisi({ kilit, aciklama, children }: { kilit: string; aciklama?: string; children: React.ReactNode }) {
  const { tanim, durum, uid, hata } = useBasarim();
  const [bekle, setBekle] = useState(false);
  const [ileti, setIleti] = useState('');
  const item = tanim.kilitler.find((k) => k.id === kilit);
  const yonetici = String(auth?.currentUser?.email || '').toLowerCase() === ADMIN_EMAIL.toLowerCase();
  if (!item || !item.etkin || yonetici || uid === 'ai-test' || durum?.kilit[kilit] || durum?.ozel?.muaf) return <>{children}</>;
  // İnternetsiz: daha önce açılmışsa cihazdaki kayıtla geçer; açılmamışsa iskelet yerine açık bilgi
  if (!durum && kilitOnbellek()[kilit]) return <>{children}</>;
  if (!durum && (cevrimdisiGibi() || hata)) {
    return (
      <div className="bs bs-kilit"><div className="bs-kilit-kart">
        <span className="bs-kilit-ikon" aria-hidden><Lock /></span>
        <h1>{item.ad}</h1>
        <p>Bu içerik ATP ile açılır. Kilidin durumunu görmek ya da açmak için internet gerekir; bir kez açtıktan sonra internetsiz de açılır.</p>
        <button type="button" className="bs-dk-kaydet" onClick={() => void yenile(true)}>Yeniden dene</button>
      </div></div>
    );
  }
  if (!durum) {
    return <div className="bs"><div className="bs-iskelet" aria-busy="true" aria-label="Yükleniyor" />{hata && <p className="bs-bos">{hata} <button type="button" className="bs-baglanti" onClick={() => void yenile(true)}>Yeniden dene</button></p>}</div>;
  }
  const eksik = item.fiyat - durum.atp.bakiye;
  const ac = async () => {
    setBekle(true); setIleti('');
    try { await satinAl(item.id); } catch (e: any) { setIleti(e?.message || 'Açılamadı'); } finally { setBekle(false); }
  };
  return (
    <div className="bs bs-kilit">
      <div className="bs-kilit-kart">
        <span className="bs-kilit-ikon" aria-hidden><Lock /></span>
        <h1>{item.ad}</h1>
        <p>{aciklama || 'Bu içerik ATP ile açılır. Bir kez açtığında hesabında kalıcı olarak açık kalır.'}</p>
        <div className="bs-kilit-fiyat">
          <span><AtpIkon boyut={16} canli /> <b>{sayi(item.fiyat)} mol</b> gerekli</span>
          <span>Hesabında: <b>{sayi(durum.atp.bakiye)} mol</b></span>
        </div>
        {ileti && <p className="bs-dk-hata" role="alert">{ileti}</p>}
        {eksik > 0 ? (
          <>
            <p className="bs-kilit-eksik">{sayi(eksik)} mol eksik. Hedeflerin üst seviyeleri, başarımlar ve haftalık sıralamada ilk 5 ATP kazandırır.</p>
            <button type="button" className="bs-dk-kaydet" onClick={() => navigateTo(pathFor('basarimlar'))}><Sparkles aria-hidden /> Hedeflerime git</button>
          </>
        ) : (
          <button type="button" className="bs-dk-kaydet is-atp" disabled={bekle} onClick={ac}>{bekle ? 'Açılıyor…' : `${sayi(item.fiyat)} mol ile kilidi aç`}</button>
        )}
      </div>
    </div>
  );
}
