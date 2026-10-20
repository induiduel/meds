/**
 * Öğrencinin hoca tüyosu önerisi (POST /api/kamp/tuyo-oner). Öneri yönetici onayından sonra kampa girer
 * (Yönetim › Kamp tüyoları). Branş ve ders listesi her kurulda (Kurul 1 dahil, data/dersler/k1.json) ders defterinden.
 */
import React, { useMemo, useState } from 'react';
import { CheckCircle2, Lightbulb, Send, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { KURULLAR } from '../../services/kurulTakvimi';
import { bransBul, dersNo, kurulBranslari, kurulDersleri } from './kampVeri';

const hataMetni = (status: number, e?: string) => {
  if (status === 429) return 'Bir saat içinde çok fazla öneri gönderildi. Biraz sonra yeniden deneyin.';
  if (status === 400) {
    if (e && /metin/.test(e)) return 'Tüyo metni en az 8, en çok 1500 karakter olmalı.';
    if (e && /brans/.test(e)) return 'Lütfen bir branş seçin.';
    if (e && /ders/.test(e)) return 'Seçilen ders tanınmadı; dersi boş bırakıp yeniden deneyin.';
    return 'Bilgiler eksik ya da hatalı; alanları kontrol edin.';
  }
  if (status === 0) return 'Sunucuya ulaşılamadı. İnternet bağlantınızı kontrol edip yeniden deneyin.';
  return 'Öneri gönderilemedi. Biraz sonra yeniden deneyin.';
};

export const TuyoFormu: React.FC<{ kurul: number; brans?: string; onKapat: () => void }> = ({ kurul: ilkKurul, brans: ilkBrans, onKapat }) => {
  const [kurul, setKurul] = useState(ilkKurul);
  const [brans, setBrans] = useState(ilkBrans || '');
  const [ders, setDers] = useState('');
  const [metin, setMetin] = useState('');
  const [ad, setAd] = useState('');
  const [durum, setDurum] = useState<'bos' | 'gidiyor' | 'tamam'>('bos');
  const [hata, setHata] = useState('');

  const branslar = useMemo(() => kurulBranslari(kurul), [kurul]);
  const dersler = useMemo(() => kurulDersleri(kurul).filter((d) => bransBul(d.brans)?.slug === brans), [kurul, brans]);

  const gonder = async (e: React.FormEvent) => {
    e.preventDefault();
    setHata('');
    if (!brans) { setHata('Lütfen bir branş seçin.'); return; }
    if (metin.trim().length < 8) { setHata('Tüyo metni en az 8 karakter olmalı.'); return; }
    setDurum('gidiyor');
    const r = await safeJsonFetch<{ success?: boolean }>('/api/kamp/tuyo-oner', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ kurul, brans, ders_id: ders || undefined, metin: metin.trim(), ad: ad.trim() || undefined }),
    });
    if (r.ok && r.data?.success) { setDurum('tamam'); return; }
    setDurum('bos');
    setHata(hataMetni(r.status, r.error));
  };

  if (durum === 'tamam') {
    return (
      <section className="km-form km-form-tamam" role="status">
        <CheckCircle2 aria-hidden />
        <div>
          <b>Teşekkürler, yönetici onayından sonra kampa eklenecek.</b>
          <p>Onaylanan tüyolar bir sonraki gece güncellemesinde kampa işlenir.</p>
        </div>
        <span className="km-form-arac">
          <button type="button" className="tk-btn" onClick={() => { setMetin(''); setDurum('bos'); }}>Bir tane daha ekle</button>
          <button type="button" className="tk-btn" onClick={onKapat}>Kapat</button>
        </span>
      </section>
    );
  }

  return (
    <form className="km-form" onSubmit={gonder} aria-labelledby="km-form-b">
      <div className="km-form-bas">
        <h2 id="km-form-b"><Lightbulb aria-hidden /> Hocanın tüyosunu ekle</h2>
        <button type="button" className="tk-metin-btn" onClick={onKapat} aria-label="Formu kapat"><X aria-hidden /></button>
      </div>
      <p className="km-form-acik">Hocanız derste “bunu mutlaka sorarım”, “bu tabloyu bilin” gibi bir şey söylediyse yazın. Yönetici onayladıktan sonra kampa eklenir.</p>
      <div className="km-form-izgara">
        <label>Kurul
          <select value={kurul} onChange={(e) => { setKurul(Number(e.target.value)); setBrans(''); setDers(''); }}>
            {KURULLAR.map((k) => <option key={k.kurul} value={k.kurul}>Kurul {k.kurul}</option>)}
          </select>
        </label>
        <label>Branş
          <select value={brans} onChange={(e) => { setBrans(e.target.value); setDers(''); }} required>
            <option value="">Seçin</option>
            {branslar.map((b) => <option key={b.slug} value={b.slug}>{b.ad}</option>)}
          </select>
        </label>
        <label className="km-form-genis">Ders (isteğe bağlı)
          <select value={ders} onChange={(e) => setDers(e.target.value)} disabled={!dersler.length}>
            <option value="">{dersler.length ? 'Belirtmeyeceğim' : brans ? 'Bu branşın ders listesi yok' : 'Önce branş seçin'}</option>
            {dersler.map((d) => <option key={d.id} value={d.id}>Ders {dersNo(d)} · {d.konu}</option>)}
          </select>
        </label>
      </div>
      <label className="km-form-metin">Hocanın söylediği
        <textarea value={metin} onChange={(e) => setMetin(e.target.value)} rows={4} maxLength={1500} required
          placeholder="Örnek: Genel anesteziklerde MAC değerlerini mutlaka sorarım, tabloyu bilin." />
        <small className="tk-mono">{metin.trim().length}/1500</small>
      </label>
      <label className="km-form-ad">Adınız (isteğe bağlı)
        <input type="text" value={ad} onChange={(e) => setAd(e.target.value)} maxLength={60} autoComplete="off" />
      </label>
      {hata && <p className="km-form-hata" role="alert">{hata}</p>}
      <div className="km-form-arac">
        <button type="submit" className="tk-btn tk-btn-ana" disabled={durum === 'gidiyor'}><Send aria-hidden /> {durum === 'gidiyor' ? 'Gönderiliyor…' : 'Öneriyi gönder'}</button>
      </div>
    </form>
  );
};
