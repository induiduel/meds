import React, { useRef, useState } from 'react';
import { SayfaBasligi, Rozet, Hata, Yukleniyor, bildir, onayIste, useAdminSorgu, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';
import './ortak/ts16.css';

const mb = (b: number) => `${(b / 1048576).toFixed(1)} MB`;

/**
 * Sistem › Yedek ve tehlikeli uçlar — gece pg yedekleri (salt okunur), havuz dışa aktarımı, içe aktarım (çift onay:
 * yazılı ICE-AKTAR + sunucuda x-onay başlığı), sıfırlama (sunucuda kapalı, 410). Hepsi denetim kaydına düşer.
 */
export default function Yedek({ git }: SayfaProps) {
  const y = useAdminSorgu<any>('/api/admin/pg/backups');
  const dosyaRef = useRef<HTMLInputElement>(null);
  const [mesgul, setMesgul] = useState(false);

  const disaAktar = async () => {
    setMesgul(true);
    try {
      const r = await fetch('/api/admin/db/export', { cache: 'no-store' });
      if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
      const a = document.createElement('a');
      a.href = URL.createObjectURL(await r.blob());
      a.download = `medsor-havuz-${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    } catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
    finally { setMesgul(false); }
  };

  const iceAktar = async (f: File) => {
    let veri: any;
    try { veri = JSON.parse(await f.text()); } catch { bildir('Dosya geçerli JSON değil.', 'kotu'); return; }
    const n = Array.isArray(veri?.questions) ? veri.questions.length : 0;
    const k = Array.isArray(veri?.committees) ? veri.committees.length : 0;
    if (!n) { bildir('Dosyada soru yok; boş havuzla ezme engellendi.', 'kotu'); return; }
    const ok = await onayIste({
      baslik: 'Soru havuzu bu dosyayla EZİLSİN mi?', tehlikeli: true, yazilacak: 'ICE-AKTAR', onayMetni: 'Havuzu ez',
      aciklama: <><code>{f.name}</code>: {n} soru, {k} kurul. Mevcut havuz (data/db.json) tamamen değişir. Önce dışa aktarım alın. Ham soru defteri etkilenmez.</>,
    });
    if (!ok) return;
    setMesgul(true);
    try {
      const r = await fetch('/api/admin/db/import', { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-onay': 'ICE-AKTAR' }, body: JSON.stringify(veri) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(j.error || `${r.status}`);
      bildir(j.message || 'İçe aktarıldı.', 'iyi');
    } catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
    finally { setMesgul(false); if (dosyaRef.current) dosyaRef.current.value = ''; }
  };

  const sifirla = async () => {
    await onayIste({ baslik: 'Sıfırlama kapalı', aciklama: 'Havuzu başlangıç verisine döndüren /api/admin/db/reset sunucuda kalıcı olarak kapatıldı (410): kullanıcı kaynaklı ham veri silinemez.', onayMetni: 'Tamam' });
  };

  return (
    <>
      <SayfaBasligi baslik="Yedek ve tehlikeli işlemler" aciklama="Gece yedekleri, havuz dışa/içe aktarımı. Tehlikeli işlemler yazılı onay ister ve denetim kaydına düşer." />
      <div className="m16-ts-izgara">
        <section className="m16-kart">
          <h2>meds-pg gece yedekleri</h2>
          {y.hata ? <Hata hata={y.hata} yenile={y.yenile} /> : !y.veri ? <Yukleniyor satir={3} /> : !y.veri.available ? <p className="m16-ts-not">{y.veri.note}</p> : (
            <ul className="m16-liste">
              {(y.veri.backups || y.veri.yedekler || []).slice(0, 14).map((b: any, i: number) => (
                <li key={i}><span className="m16-kisalt">{b.ad || b.name || b.dosya}</span><small>{b.bayt || b.size ? mb(b.bayt || b.size) : ''}</small><time>{b.at || b.tarih ? zamanMetni(b.at || b.tarih) : ''}</time></li>
              ))}
            </ul>
          )}
          <p className="m16-ts-not">Yedek alma, silme ve geri yükleme sunucudan yapılmaz (Oracle meds-pg-yedek.timer, 03:30, 7 gün).</p>
        </section>
        <section className="m16-kart">
          <h2>Soru havuzu (data/db.json)</h2>
          <div className="m16-ts-eylem">
            <button type="button" className="m16-btn" disabled={mesgul} onClick={disaAktar}>Dışa aktar (JSON)</button>
            <button type="button" className="m16-btn tehlike" disabled={mesgul} onClick={() => dosyaRef.current?.click()}>İçe aktar…</button>
            <input ref={dosyaRef} type="file" accept="application/json,.json" hidden onChange={(e) => { const f = e.target.files?.[0]; if (f) void iceAktar(f); }} />
          </div>
          <p className="m16-ts-not">İçe aktarım havuzu tamamen ezer: istemcide <code>ICE-AKTAR</code> yazılı onayı, sunucuda <code>x-onay</code> başlığı ister; boş dosya reddedilir.</p>
        </section>
        <section className="m16-kart">
          <h2>Tehlikeli uçlar</h2>
          <ul className="m16-liste">
            <li><Rozet ton="kotu">kapalı</Rozet><code className="m16-kisalt">POST /api/admin/db/reset</code><button type="button" className="m16-btn hayalet" onClick={sifirla}>Ayrıntı</button></li>
            <li><Rozet ton="uyari">çift onay</Rozet><code className="m16-kisalt">POST /api/admin/db/import</code></li>
            <li><Rozet ton="uyari">çift onay</Rozet><code className="m16-kisalt">DELETE /api/admin/pg/row</code><button type="button" className="m16-btn hayalet" onClick={() => git('sistem/db')}>Gezgin</button></li>
            <li><Rozet ton="iyi">salt okunur</Rozet><code className="m16-kisalt">POST /api/admin/pg/sql</code><button type="button" className="m16-btn hayalet" onClick={() => git('sistem/db/_sql')}>Konsol</button></li>
            <li><Rozet ton="uyari">çift onay</Rozet><code className="m16-kisalt">DELETE /api/admin/topluluk/mesajlar/:id</code></li>
          </ul>
          <p className="m16-ts-not"><a href="#" onClick={(e) => { e.preventDefault(); git('sistem/denetim?s.yontem=DELETE'); }}>Silme işlemlerinin denetim kaydı</a></p>
        </section>
      </div>
    </>
  );
}
