import React, { useCallback, useEffect, useState } from 'react';
import { Gamepad2, MessageCircle, Search, UserCheck, UserPlus, Users, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { type KisiKart, arkadasIslem, basHarf, git, mesajAc, once, profilYolu, sure, useArkadasCanli } from '../../services/arkadasIstemci';
import { useV15Baslik } from './baslik';
import { DavetPencere } from './KisiProfilV15';
import GizlilikAnahtari from './GizlilikAnahtari';
import '../../styles/v15/kisi.css';

/**
 * v15 · Arkadaşlar (/arkadaslar, Menü › Topluluk). Kişi bulma (ad ile), gelen/giden istekler, arkadaş listesi
 * (en son neye çalıştı, bu haftaki süre), Mesaj / Davet. "Profilim herkese açık" anahtarı. Sunucu: services/arkadaslik.ts.
 */
interface Liste { girisli: boolean; kimlik?: string; arkadaslar: KisiKart[]; gelen: KisiKart[]; giden: KisiKart[] }

export default function ArkadaslarV15() {
  const [l, setL] = useState<Liste | null>(null);
  const [hata, setHata] = useState('');
  const [q, setQ] = useState('');
  const [sonuc, setSonuc] = useState<KisiKart[] | null>(null);
  const [davet, setDavet] = useState<KisiKart | null>(null);
  useV15Baslik({ baslik: 'Arkadaşlar', alt: 'Topluluk' });

  const yukle = useCallback(() => safeJsonFetch<Liste>('/api/arkadas').then((r) => {
    if (r.ok && r.data) { setL(r.data); setHata(''); } else setHata((r.data as any)?.error || r.error || 'Liste alınamadı.');
  }), []);
  useEffect(() => { void yukle(); }, [yukle]);
  useArkadasCanli(() => void yukle());

  useEffect(() => {
    const t = q.trim();
    if (t.length < 2) { setSonuc(null); return; }
    const id = setTimeout(() => {
      void safeJsonFetch<{ kisiler: KisiKart[] }>(`/api/kisi/ara?q=${encodeURIComponent(t)}`).then((r) => setSonuc(r.ok ? r.data?.kisiler || [] : []));
    }, 300);
    return () => clearTimeout(id);
  }, [q]);

  const islem = async (tur: 'istek' | 'kabul' | 'reddet' | 'cikar', k: KisiKart) => {
    const r = await arkadasIslem(tur, k.kimlik);
    if (r.hata) { setHata(r.hata); return; }
    if (sonuc) setSonuc(sonuc.map((x) => (x.kimlik === k.kimlik ? { ...x, iliski: r.iliski } : x)));
    void yukle();
  };

  // H167: "Giriş gerekli" kartında giriş düğmesi yoktu; App'teki giriş penceresini olayla açar
  if (l && !l.girisli) return (
    <div className="ks15">
      <div className="v15-card ks15-bos">
        <b>Giriş gerekli</b>
        <p>Arkadaş eklemek ve mesajlaşmak için giriş yap.</p>
        <button type="button" className="v15-btn" onClick={() => window.dispatchEvent(new Event('medsoru:giris-ac'))}>Giriş yap</button>
      </div>
    </div>
  );

  return (
    <div className="ks15">
      <label className="v15-card ks15-ara">
        <Search aria-hidden />
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Ad ile kişi ara" aria-label="Ad ile kişi ara" />
        {q && <button type="button" className="v15-btn is-ghost" aria-label="Aramayı temizle" onClick={() => setQ('')}><X aria-hidden /></button>}
      </label>
      {hata && <p className="ks15-not ks15-hata" role="alert">{hata}</p>}

      {sonuc && (
        <section className="v15-card ks15-kutu">
          <h3>Arama sonuçları</h3>
          {sonuc.length ? <ul>{sonuc.map((k) => (
            <Satir key={k.kimlik} k={k} alt={[k.universite, k.donem ? `${k.donem}. dönem` : ''].filter(Boolean).join(' · ')}>
              {k.iliski === 'yok' && <button type="button" className="v15-btn" onClick={() => void islem('istek', k)}><UserPlus aria-hidden /> Ekle</button>}
              {k.iliski === 'giden' && <span className="v15-tag">İstek gönderildi</span>}
              {k.iliski === 'gelen' && <button type="button" className="v15-btn" onClick={() => void islem('kabul', k)}><UserCheck aria-hidden /> Kabul et</button>}
              {k.iliski === 'arkadas' && <span className="v15-tag">Arkadaşın</span>}
            </Satir>
          ))}</ul> : <p className="ks15-not">Bu adla herkese açık profil bulunamadı. Sıralamada ya da Topluluk sohbetinde kişinin adına dokunarak da profilini açabilirsin.</p>}
        </section>
      )}

      {!!l?.gelen.length && (
        <section className="v15-card ks15-kutu">
          <h3>Gelen istekler</h3>
          <ul>{l.gelen.map((k) => (
            <Satir key={k.kimlik} k={k} alt={once(k.at)}>
              <button type="button" className="v15-btn" onClick={() => void islem('kabul', k)}><UserCheck aria-hidden /> Kabul et</button>
              <button type="button" className="v15-btn is-ghost" onClick={() => void islem('reddet', k)}>Reddet</button>
            </Satir>
          ))}</ul>
        </section>
      )}

      <section className="v15-card ks15-kutu">
        <h3>Arkadaşlarım{l ? ` (${l.arkadaslar.length})` : ''}</h3>
        {!l ? <p className="ks15-not">Yükleniyor…</p> : l.arkadaslar.length ? (
          <ul>{l.arkadaslar.map((k) => (
            <Satir key={k.kimlik} k={k} alt={k.gizli ? 'Profili gizli' : k.son ? `En son: ${k.son.ad} · ${once(k.son.at)}` : 'Henüz çalışma kaydı yok'} sag={k.haftaSn ? `bu hafta ${sure(k.haftaSn)}` : undefined}>
              <button type="button" className="v15-btn is-ghost" aria-label={`${k.ad} ile mesajlaş`} onClick={() => void mesajAc(k.kimlik).then((h) => h && setHata(h))}><MessageCircle aria-hidden /></button>
              <button type="button" className="v15-btn is-ghost" aria-label={`${k.ad} kişisini soru çözmeye davet et`} onClick={() => setDavet(k)}><Gamepad2 aria-hidden /></button>
            </Satir>
          ))}</ul>
        ) : (
          <div className="ks15-bos-ic"><Users aria-hidden /><p>Henüz arkadaşın yok. Yukarıdan adıyla ara ya da Sıralama'da bir kişiye dokunup profilinden "Arkadaş ekle"ye bas.</p></div>
        )}
      </section>

      {!!l?.giden.length && (
        <section className="v15-card ks15-kutu">
          <h3>Gönderdiğin istekler</h3>
          <ul>{l.giden.map((k) => (
            <Satir key={k.kimlik} k={k} alt={`Gönderildi · ${once(k.at)}`}>
              <button type="button" className="v15-btn is-ghost" onClick={() => void islem('cikar', k)}>Geri çek</button>
            </Satir>
          ))}</ul>
        </section>
      )}

      <div className="ks15-dugmeler">
        <button type="button" className="v15-btn is-soft" onClick={() => git('/siralama')}>Sıralamayı aç</button>
        {l?.kimlik && <button type="button" className="v15-btn is-soft" onClick={() => git(profilYolu(l.kimlik!))}>Profilimi gör</button>}
      </div>
      <GizlilikAnahtari />
      {davet && <DavetPencere kimlik={davet.kimlik} ad={davet.ad} kapat={() => setDavet(null)} />}
    </div>
  );
}

function Satir({ k, alt, sag, children }: { k: KisiKart; alt?: string; sag?: string; children?: React.ReactNode }) {
  return (
    <li className="ks15-sat">
      <button type="button" className="ks15-sat-ac" onClick={() => git(profilYolu(k.kimlik))} aria-label={`${k.ad} profilini aç`}>
        <span className="ks15-av" aria-hidden>{k.foto ? <img src={k.foto} alt="" loading="lazy" /> : basHarf(k.ad)}</span>
        <span className="ks15-sat-ad"><b>{k.ad}</b>{alt && <small>{alt}</small>}{sag && <small>{sag}</small>}</span>
      </button>
      <span className="ks15-sat-eylem">{children}</span>
    </li>
  );
}
