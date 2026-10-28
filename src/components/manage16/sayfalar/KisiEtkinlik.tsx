import React, { useEffect, useState } from 'react';
import { SayfaBasligi, adminIstek, Rozet, Hata, Yukleniyor, BosDurum, bildir, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';
import { KisiBag, olayEtiket, tarihMetni } from './kisiOrtak';

/** Kullanıcılar › Etkinlik günlüğü: tüm kullanıcıların olayları (user_events), imleçli; tür/kişi/metin süzgeci. */
export default function KisiEtkinlik({ git }: SayfaProps) {
  const ilk = new URLSearchParams(window.location.search);
  const [tur, setTur] = useState(ilk.get('tur') || '');
  const [kim, setKim] = useState(ilk.get('uid') || '');
  const [q, setQ] = useState(ilk.get('q') || '');
  const [debQ, setDebQ] = useState(q);
  const [ogeler, setOgeler] = useState<any[]>([]);
  const [turler, setTurler] = useState<any[]>([]);
  const [sonraki, setSonraki] = useState<number | null>(null);
  const [durum, setDurum] = useState<{ yuk: boolean; hata: any; db: boolean }>({ yuk: true, hata: null, db: true });
  useEffect(() => { const t = setTimeout(() => setDebQ(q), 300); return () => clearTimeout(t); }, [q]);
  const getir = async (imlec?: number | null) => {
    setDurum((d) => ({ ...d, yuk: true }));
    try {
      const r = await adminIstek<any>('/api/admin/events', { sorgu: { tur, uid: kim, q: debQ, boyut: 100, imlec: imlec || undefined } });
      setOgeler((x) => (imlec ? [...x, ...r.ogeler] : r.ogeler)); setSonraki(r.sonraki); setTurler(r.turler || []);
      setDurum({ yuk: false, hata: null, db: r.veritabani !== false });
    } catch (e: any) { if (imlec) bildir(e.message, 'kotu'); setDurum({ yuk: false, hata: e, db: true }); }
  };
  useEffect(() => {
    const u = new URL(window.location.href);
    for (const [k, v] of [['tur', tur], ['uid', kim], ['q', debQ]]) v ? u.searchParams.set(k, v) : u.searchParams.delete(k);
    history.replaceState(history.state, '', u);
    void getir(null);
  }, [tur, kim, debQ]); // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <>
      <SayfaBasligi baslik="Etkinlik günlüğü" aciklama="Öğrenci eylemleri (yorum, bildirim, soru, not, oy…) — meds-pg user_events, en yeni üstte.">
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', padding: '8px 0' }}>
          <input className="m16-girdi" placeholder="Metin ara…" value={q} onChange={(e) => setQ(e.target.value)} aria-label="Metin ara" />
          <input className="m16-girdi" placeholder="uid / e-posta / cihaz" value={kim} onChange={(e) => setKim(e.target.value.trim())} aria-label="Kişi" />
        </div>
        <div className="m16-cip-grup">
          <button className={`m16-cip${!tur ? ' on' : ''}`} onClick={() => setTur('')}>Tümü</button>
          {turler.map((t) => <button key={t.kind} className={`m16-cip${tur === t.kind ? ' on' : ''}`} onClick={() => setTur(t.kind)}>{olayEtiket(t.kind)} <em>{t.n}</em></button>)}
        </div>
      </SayfaBasligi>
      {durum.hata ? <Hata hata={durum.hata} yenile={() => getir(null)} /> : !durum.db ? <BosDurum baslik="Veritabanı kapalı" /> : !ogeler.length && durum.yuk ? <Yukleniyor satir={10} /> : !ogeler.length ? <BosDurum baslik="Olay yok" /> : (
        <section className="m16-kart">
          <ul className="m16-liste">
            {ogeler.map((o) => (
              <li key={o.id}>
                <Rozet>{olayEtiket(o.kind)}</Rozet>
                <span style={{ minWidth: 110, maxWidth: 180 }} className="m16-kisalt"><KisiBag anahtar={o.kisi} git={git}>{o.ad || o.email || 'misafir'}</KisiBag></span>
                <span className="m16-kisalt" title={o.body || o.label}>{o.label}{o.body ? ` — ${o.body}` : ''}</span>
                <time dateTime={o.at} title={tarihMetni(o.at)}>{zamanMetni(o.at)}</time>
              </li>
            ))}
          </ul>
          {sonraki ? <button className="m16-btn" style={{ marginTop: 8 }} disabled={durum.yuk} onClick={() => getir(sonraki)}>{durum.yuk ? 'Yükleniyor…' : 'Daha eski'}</button> : null}
        </section>
      )}
    </>
  );
}
