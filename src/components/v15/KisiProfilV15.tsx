import React, { useCallback, useEffect, useState } from 'react';
import { BookOpen, Clock, Gamepad2, Lock, MessageCircle, Target, UserCheck, UserMinus, UserPlus, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { parseLocation } from '../../router';
import { type AcikProfil, arkadasIslem, basHarf, davetEt, git, mesajAc, once, sure, useArkadasCanli } from '../../services/arkadasIstemci';
import { useV15Baslik } from './baslik';
import GizlilikAnahtari from './GizlilikAnahtari';
import '../../styles/v15/kisi.css';

/**
 * v15 · Açık profil (/kisi/<kimlik>). Sunucu: GET /api/kisi/:kimlik (services/arkadaslik.ts). Herkese açık istatistikler:
 * çalışma saati (bugün/hafta/toplam), çözülen soru, doğru oranı, son çalışılan dersler, "en son neye çalıştı".
 * Düğmeler: Arkadaş ekle / Mesaj gönder / Soru çözmeye davet et (arkadaşsa). Kimlik açık profil özetidir; uid değil.
 */
const kimlikOku = () => { const { route, param } = parseLocation(); return route === 'kisi' ? param || '' : ''; };

export default function KisiProfilV15() {
  const [kimlik, setKimlik] = useState(kimlikOku);
  useEffect(() => { const f = () => setKimlik(kimlikOku()); window.addEventListener('popstate', f); return () => window.removeEventListener('popstate', f); }, []);
  const [p, setP] = useState<AcikProfil | null>(null);
  const [hata, setHata] = useState('');
  const [mesaj, setMesaj] = useState('');
  const [mesgul, setMesgul] = useState(false);
  const [davet, setDavet] = useState(false);
  useV15Baslik({ baslik: p?.ben ? 'Profilim' : p?.ad || 'Profil', alt: 'Açık profil', geri: '/arkadaslar' });

  const yukle = useCallback(() => {
    if (!kimlik) { setHata('Profil adresi eksik.'); return; }
    void safeJsonFetch<AcikProfil>(`/api/kisi/${encodeURIComponent(kimlik)}`).then((r) => {
      if (r.ok && r.data) { setP(r.data); setHata(''); } else setHata((r.data as any)?.error || r.error || 'Profil alınamadı.');
    });
  }, [kimlik]);
  useEffect(() => { setP(null); yukle(); }, [yukle]);
  useArkadasCanli(yukle);

  const islem = async (tur: 'istek' | 'kabul' | 'reddet' | 'cikar') => {
    if (!p) return;
    if (tur === 'cikar' && !window.confirm(`${p.ad} arkadaş listenden çıkarılsın mı?`)) return;
    setMesgul(true); setMesaj('');
    const r = await arkadasIslem(tur, p.kimlik);
    setMesgul(false);
    if (r.hata) setMesaj(r.hata); else { setP({ ...p, iliski: r.iliski || p.iliski }); if (tur === 'istek' && r.iliski === 'giden') setMesaj('Arkadaşlık isteği gönderildi.'); }
  };

  if (hata) return <div className="ks15"><Bos baslik="Profil açılamadı" metin={hata} /></div>;
  if (!p) return <div className="ks15"><p className="ks15-not">Yükleniyor…</p></div>;

  const dugmeler = !p.ben && (
    <div className="ks15-dugmeler">
      {p.iliski === 'yok' && <button type="button" className="v15-btn" disabled={mesgul} onClick={() => void islem('istek')}><UserPlus aria-hidden /> Arkadaş ekle</button>}
      {p.iliski === 'giden' && <button type="button" className="v15-btn is-soft" disabled={mesgul} onClick={() => void islem('cikar')}><X aria-hidden /> İsteği geri çek</button>}
      {p.iliski === 'gelen' && <>
        <button type="button" className="v15-btn" disabled={mesgul} onClick={() => void islem('kabul')}><UserCheck aria-hidden /> İsteği kabul et</button>
        <button type="button" className="v15-btn is-ghost" disabled={mesgul} onClick={() => void islem('reddet')}>Reddet</button>
      </>}
      {!p.gizli && <button type="button" className="v15-btn is-soft" disabled={mesgul} onClick={() => void mesajAc(p.kimlik).then((h) => h && setMesaj(h))}><MessageCircle aria-hidden /> Mesaj gönder</button>}
      {p.iliski === 'arkadas' && <button type="button" className="v15-btn is-soft" onClick={() => setDavet(true)}><Gamepad2 aria-hidden /> Soru çözmeye davet et</button>}
      {p.iliski === 'arkadas' && <button type="button" className="v15-btn is-ghost" disabled={mesgul} onClick={() => void islem('cikar')}><UserMinus aria-hidden /> Arkadaşlıktan çıkar</button>}
    </div>
  );

  if (p.gizli) {
    return (
      <div className="ks15">
        <div className="v15-card ks15-bas">
          <span className="ks15-av is-b" aria-hidden><Lock /></span>
          <div className="ks15-kim"><b>Gizli kullanıcı</b><small>Bu kişi profilini herkese kapattı.</small></div>
        </div>
        {dugmeler}
        {mesaj && <p className="ks15-not" role="status">{mesaj}</p>}
      </div>
    );
  }

  const cozulen = (p.dogru || 0) + (p.yanlis || 0);
  const oran = cozulen ? Math.round(((p.dogru || 0) / cozulen) * 100) : null;
  return (
    <div className="ks15">
      <div className="v15-card ks15-bas">
        <span className="ks15-av is-b" aria-hidden>{p.foto ? <img src={p.foto} alt="" /> : basHarf(p.ad)}</span>
        <div className="ks15-kim">
          <b>{p.ad}</b>
          <small>{[p.universite, p.donem ? `${p.donem}. dönem` : '', p.unvan || p.kidem].filter(Boolean).join(' · ') || 'Üniversite belirtilmemiş'}</small>
          <small>{p.arkadasN || 0} arkadaş{p.ben ? '' : p.iliski === 'arkadas' ? ' · arkadaşın' : ''}</small>
        </div>
      </div>
      {dugmeler}
      {mesaj && <p className="ks15-not" role="status">{mesaj}</p>}

      <div className="v15-card ks15-son">
        <span className="v15-tile"><BookOpen aria-hidden /></span>
        <div>
          <small>En son çalıştığı</small>
          {p.son ? <b>{p.son.ad}</b> : <b>Henüz kayıtlı çalışma yok</b>}
          {p.son && <small>{p.son.modul} · {once(p.son.at)}</small>}
        </div>
      </div>

      <div className="ks15-olcu">
        <Olcu ikon={<Clock aria-hidden />} ad="Bugün" deger={sure(p.calisma?.bugun)} />
        <Olcu ikon={<Clock aria-hidden />} ad="Bu hafta" deger={sure(p.calisma?.hafta)} />
        <Olcu ikon={<Clock aria-hidden />} ad="Toplam çalışma" deger={sure(p.calisma?.toplam)} />
        <Olcu ikon={<Target aria-hidden />} ad="Çözülen soru" deger={(p.soru?.toplam || 0).toLocaleString('tr-TR')} alt={p.soru?.hafta ? `bu hafta ${p.soru.hafta}` : undefined} />
        <Olcu ikon={<Target aria-hidden />} ad="Doğru oranı" deger={oran == null ? '—' : `%${oran}`} alt={cozulen ? `son ${cozulen} cevaptan` : 'cevap kaydı yok'} />
        <Olcu ikon={<BookOpen aria-hidden />} ad="Bitirilen konu" deger={String(p.bitirilen || 0)} />
      </div>

      {!!p.haftaDersler?.length && (
        <section className="v15-card ks15-kutu">
          <h3>Bu hafta en çok çalıştığı</h3>
          <ul>{p.haftaDersler.map((d, i) => <li key={i}><span><b>{d.ad}</b><small>{d.modul}</small></span><em>{sure(d.sn)}</em></li>)}</ul>
        </section>
      )}
      <section className="v15-card ks15-kutu">
        <h3>Çalıştığı dersler</h3>
        {p.dersler?.length ? (
          <ul>{p.dersler.map((d, i) => (
            <li key={i}>
              <span><b>{d.ad}</b><small>{d.modul}{d.bitti ? ' · bitirdi' : ''} · {once(d.at)}</small></span>
              <em>{sure(d.sn)}{d.soru ? ` · ${d.soru} soru` : ''}</em>
            </li>
          ))}</ul>
        ) : <p className="ks15-not">Henüz ders çalışma kaydı yok. Sesli ders, Öğren ya da soru çözücüde çalışınca burada görünür.</p>}
      </section>

      {p.ben && <GizlilikAnahtari />}
      {davet && <DavetPencere kimlik={p.kimlik} ad={p.ad} kapat={() => setDavet(false)} />}
    </div>
  );
}

function Olcu({ ikon, ad, deger, alt }: { ikon: React.ReactNode; ad: string; deger: string; alt?: string }) {
  return <div className="v15-card ks15-o"><span className="ks15-o-ik">{ikon}</span><small>{ad}</small><b>{deger}</b>{alt && <small>{alt}</small>}</div>;
}

/** Davet: Oyunlar'da kurulan odanın kodu arkadaşa bildirim + sohbet mesajı olarak gider; tıklayınca odaya katılır. */
export function DavetPencere({ kimlik, ad, kapat }: { kimlik: string; ad: string; kapat: () => void }) {
  const [oda, setOda] = useState('');
  const [durum, setDurum] = useState('');
  const [mesgul, setMesgul] = useState(false);
  const gonder = async () => {
    if (oda.length < 4) { setDurum('Oda kodu 5 karakterdir.'); return; }
    setMesgul(true);
    const h = await davetEt(kimlik, oda);
    setMesgul(false);
    setDurum(h || `${ad} davet edildi. Bildirim ve sohbet mesajı gönderildi.`);
  };
  return (
    <div className="ks15-perde" role="dialog" aria-modal="true" aria-label="Soru çözmeye davet et" onClick={kapat}>
      <div className="v15-card ks15-pencere" onClick={(e) => e.stopPropagation()}>
        <div className="ks15-pencere-bas"><b>{ad} kişisini davet et</b><button type="button" className="v15-btn is-ghost" aria-label="Kapat" onClick={kapat}><X aria-hidden /></button></div>
        <p className="ks15-not">Önce Oyunlar'da bir oda kur, ekrandaki oda kodunu buraya yaz. Arkadaşın davete dokununca aynı odaya katılır.</p>
        <label className="ks15-alan"><span>Oda kodu</span>
          <input value={oda} onChange={(e) => setOda(e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 6))} placeholder="Örn. K7MPA" autoCapitalize="characters" onKeyDown={(e) => { if (e.key === 'Enter') void gonder(); }} />
        </label>
        {durum && <p className="ks15-not" role="status">{durum}</p>}
        <div className="ks15-dugmeler">
          <button type="button" className="v15-btn" disabled={mesgul} onClick={() => void gonder()}>Davet gönder</button>
          <button type="button" className="v15-btn is-soft" onClick={() => git('/sorular/oyunlar')}>Oyunlar'da oda kur</button>
        </div>
      </div>
    </div>
  );
}

export function Bos({ baslik, metin }: { baslik: string; metin: string }) {
  return <div className="v15-card ks15-bos"><b>{baslik}</b><p>{metin}</p></div>;
}
