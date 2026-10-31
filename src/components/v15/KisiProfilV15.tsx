import React, { useCallback, useEffect, useState } from 'react';
import { Activity, Award, BookOpen, CalendarDays, CheckCircle2, ChevronRight, Clock, Flame, Medal, Gamepad2, Lock, MessageCircle, Target, Trophy, UserCheck, UserMinus, UserPlus, X } from 'lucide-react';
import { sayi, useBasarim } from '../../services/basarimIstemci';
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
  const { durum } = useBasarim();
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

  if (hata) return <div className="apr15"><Bos baslik="Profil açılamadı" metin={hata} /></div>;
  if (!p) return <div className="apr15"><p className="apr15-not">Yükleniyor…</p></div>;

  const dugmeler = !p.ben && (
    <div className="apr15-dugmeler is-tam">
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
      <div className="apr15">
        <div className="v15-card apr15-bas">
          <span className="apr15-av is-b" aria-hidden><Lock /></span>
          <div className="apr15-kim"><b>Gizli kullanıcı</b><small>Bu kişi profilini herkese kapattı.</small></div>
        </div>
        {dugmeler}
        {mesaj && <p className="apr15-not" role="status">{mesaj}</p>}
      </div>
    );
  }

  const cozulen = (p.dogru || 0) + (p.yanlis || 0);
  const oran = cozulen ? Math.round(((p.dogru || 0) / cozulen) * 100) : null;
  // 2026-10-31: modül dağılımı (çalışma süresi) ve en çok çalışılan dersler çubuk grafiği
  const dersler = p.dersler || [];
  const modul = new Map<string, number>();
  for (const d of dersler) modul.set(d.modul || 'Diğer', (modul.get(d.modul || 'Diğer') || 0) + (d.sn || 0));
  const modulToplam = [...modul.values()].reduce((a, b) => a + b, 0);
  const moduller = [...modul.entries()].sort((a, b) => b[1] - a[1]).slice(0, 5);
  const enCok = [...dersler].sort((a, b) => (b.sn || 0) - (a.sn || 0)).slice(0, 6);
  const enCokMax = enCok[0]?.sn || 0;
  const bitenDers = dersler.filter((d) => d.bitti).length;
  const gunlukOrt = (p.calisma?.hafta || 0) / 7;
  const kidem = p.ben ? durum?.kidem : undefined;
  const kidemYuzde = kidem && durum && kidem.sonraki && kidem.tavan > 0 ? Math.min(100, Math.round((durum.puan.toplam / kidem.tavan) * 100)) : null;
  const sira = p.ben ? durum?.siralama : undefined;
  return (
    <div className="apr15">
      <div className="v15-card apr15-bas apr15-hero is-tam">
        <span className="apr15-av is-b" aria-hidden>{p.foto ? <img src={p.foto} alt="" /> : basHarf(p.ad)}</span>
        <div className="apr15-kim">
          <b>{p.ad}</b>
          <small>{[p.universite, p.donem ? `${p.donem}. dönem` : '', p.unvan || p.kidem].filter(Boolean).join(' · ') || 'Üniversite belirtilmemiş'}</small>
          <small>{p.arkadasN || 0} arkadaş{p.ben ? '' : p.iliski === 'arkadas' ? ' · arkadaşın' : ''}</small>
          <span className="apr15-cipler">
            {p.puan && <span className="apr15-cip"><Trophy aria-hidden /> {sayi(p.puan.toplam)} puan</span>}
            {!!p.basarim && <span className="apr15-cip"><Award aria-hidden /> {p.basarim} başarım</span>}
            {p.ben && !!durum?.seri && <span className="apr15-cip is-seri"><Flame aria-hidden /> {durum.seri} gün seri</span>}
          </span>
        </div>
      </div>
      <Durum p={p} />
      {kidem && (
        <div className="v15-card apr15-kidem">
          <div><small>Kıdem</small><b>{kidem.ad}</b></div>
          {kidem.sonraki && kidemYuzde != null ? (
            <div className="apr15-kidem-ilerle">
              <i className="apr15-bar" aria-hidden><i style={{ width: `${kidemYuzde}%` }} /></i>
              <small>Sonraki: {kidem.sonraki.ad} · %{kidemYuzde}</small>
            </div>
          ) : <small>En üst kıdemdesin.</small>}
        </div>
      )}
      {dugmeler}
      {mesaj && <p className="apr15-not is-tam" role="status">{mesaj}</p>}

      <div className="v15-card apr15-son">
        <span className="v15-tile"><BookOpen aria-hidden /></span>
        <div>
          <small>En son çalıştığı</small>
          {p.son ? <b>{p.son.ad}</b> : <b>Henüz kayıtlı çalışma yok</b>}
          {p.son && <small>{p.son.modul} · {once(p.son.at)}</small>}
        </div>
      </div>

      <div className="v15-card apr15-ozet">
        <Halka yuzde={oran} />
        <div className="apr15-ozet-sag">
          <b>{oran == null ? 'Henüz cevap yok' : oran >= 75 ? 'Çok iyi gidiyor' : oran >= 55 ? 'İyi gidiyor' : 'Gelişiyor'}</b>
          <small>{cozulen ? `${sayi(p.dogru || 0)} doğru · ${sayi(p.yanlis || 0)} yanlış` : 'Soru çözdükçe doğru oranı burada görünür.'}</small>
          <small>Günlük ortalama (bu hafta): {sure(gunlukOrt)}{p.puan ? ` · bu hafta ${sayi(p.puan.hafta)} puan` : ''}</small>
        </div>
      </div>

      {sira && (
        <button type="button" className="v15-card apr15-sira" onClick={() => git('/siralama')}>
          {([['hafta', 'Hafta'], ['kurul', 'Kurul'], ['tum', 'Tümü']] as const).map(([k, t]) => (
            <span key={k}><small>{t}</small><b>{sira[k]?.sira ? `#${sira[k].sira}` : '—'}</b><small>{sira[k]?.kisi ? `${sayi(sira[k].kisi)} kişi` : ''}</small></span>
          ))}
          <ChevronRight aria-hidden className="apr15-sira-ok" />
        </button>
      )}

      <div className="apr15-olcu is-tam">
        <Olcu ikon={<Clock aria-hidden />} ad="Bugün" deger={sure(p.calisma?.bugun)} />
        <Olcu ikon={<Clock aria-hidden />} ad="Bu hafta" deger={sure(p.calisma?.hafta)} />
        <Olcu ikon={<Clock aria-hidden />} ad="Toplam çalışma" deger={sure(p.calisma?.toplam)} />
        <Olcu ikon={<Target aria-hidden />} ad="Çözülen soru" deger={(p.soru?.toplam || 0).toLocaleString('tr-TR')} alt={p.soru?.hafta ? `bu hafta ${p.soru.hafta}` : undefined} />
        <Olcu ikon={<Target aria-hidden />} ad="Doğru oranı" deger={oran == null ? '—' : `%${oran}`} alt={cozulen ? `son ${cozulen} cevaptan` : 'cevap kaydı yok'} />
        <Olcu ikon={<BookOpen aria-hidden />} ad="Bitirilen konu" deger={String(p.bitirilen || 0)} alt={dersler.length ? `${dersler.length} derste çalıştı · ${bitenDers} bitti` : undefined} />
      </div>

      <Gunluk p={p} />

      {!!p.bitenler?.length && (
        <section className="v15-card apr15-kutu">
          <h3><CheckCircle2 aria-hidden /> Bitirdiği dersler <span className="apr15-say">{p.bitenler.length}</span></h3>
          <ul className="apr15-biten">{p.bitenler.map((d, i) => (
            <li key={i}><CheckCircle2 aria-hidden /><span><b>{d.ad}</b><small>{d.modul}{d.at ? ` · ${once(d.at)}` : ''}</small></span></li>
          ))}</ul>
        </section>
      )}

      {!!p.siralamaBasari?.length && (
        <section className="v15-card apr15-kutu">
          <h3><Medal aria-hidden /> Sıralama başarıları <span className="apr15-say">{p.siralamaBasari.length}</span></h3>
          <ul className="apr15-basari">{p.siralamaBasari.map((b, i) => {
            const m = /·\s*(\d+)\.\s*$/.exec(b.ad); const no = m ? Number(m[1]) : /birinci|en çok çalışanı/i.test(b.ad) ? 1 : 0;
            return (
              <li key={i}>
                <span className={`apr15-madalya is-${no && no <= 3 ? no : 0}`} aria-hidden>{no || <Trophy />}</span>
                <span><b>{b.ad.replace(/\s*·\s*\d+\.\s*$/, '')}</b><small>{tarih(b.g)}{no ? ` · ${no}. oldu` : ''}</small></span>
                {b.a > 0 && <em>+{sayi(b.a)} ATP</em>}
              </li>
            );
          })}</ul>
        </section>
      )}

      {moduller.length > 0 && modulToplam > 0 && (
        <section className="v15-card apr15-kutu">
          <h3>Çalışma dağılımı</h3>
          <div className="apr15-yigin" aria-hidden>{moduller.map(([m, sn], i) => <i key={m} className={`is-r${i}`} style={{ width: `${(sn / modulToplam) * 100}%` }} />)}</div>
          <ul className="apr15-lejant">{moduller.map(([m, sn], i) => <li key={m}><span><i className={`is-r${i}`} /> {m}</span><em>{sure(sn)} · %{Math.round((sn / modulToplam) * 100)}</em></li>)}</ul>
        </section>
      )}

      {enCok.length > 1 && enCokMax > 0 && (
        <section className="v15-card apr15-kutu">
          <h3>En çok çalışılan dersler</h3>
          <ul className="apr15-cubuk">{enCok.map((d, i) => (
            <li key={i}><span><b>{d.ad}</b><i className="apr15-bar" aria-hidden><i style={{ width: `${Math.max(4, ((d.sn || 0) / enCokMax) * 100)}%` }} /></i></span><em>{sure(d.sn)}</em></li>
          ))}</ul>
        </section>
      )}

      {!!p.haftaDersler?.length && (
        <section className="v15-card apr15-kutu">
          <h3>Bu hafta en çok çalıştığı</h3>
          <ul>{p.haftaDersler.map((d, i) => <li key={i}><span><b>{d.ad}</b><small>{d.modul}</small></span><em>{sure(d.sn)}</em></li>)}</ul>
        </section>
      )}
      <section className="v15-card apr15-kutu">
        <h3>Çalıştığı dersler</h3>
        {p.dersler?.length ? (
          <ul>{p.dersler.map((d, i) => (
            <li key={i}>
              <span><b>{d.ad}</b><small>{d.modul}{d.bitti ? ' · bitirdi' : ''} · {once(d.at)}</small></span>
              <em>{sure(d.sn)}{d.soru ? ` · ${d.soru} soru` : ''}</em>
            </li>
          ))}</ul>
        ) : <p className="apr15-not">Henüz ders çalışma kaydı yok. Sesli ders, Öğren ya da soru çözücüde çalışınca burada görünür.</p>}
      </section>

      {p.ben && <div className="is-tam"><GizlilikAnahtari /></div>}
      {davet && <DavetPencere kimlik={p.kimlik} ad={p.ad} kapat={() => setDavet(false)} />}
    </div>
  );
}

const tarih = (g: string) => { const d = new Date(`${g}T12:00:00`); return Number.isNaN(d.getTime()) ? g : d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }); };
const GUN_AD = ['Pz', 'Pt', 'Sa', 'Ça', 'Pe', 'Cu', 'Ct'];

/** Çevrimiçi / şu an ne yapıyor / son görülme. Çevrimiçi: son 3 dakikada etkin. */
function Durum({ p }: { p: AcikProfil }) {
  const g = p.gorulme;
  if (!g?.at && !p.simdi) return null;
  const fark = g?.at ? Date.now() - g.at : Infinity;
  const cevrim = fark < 3 * 60_000;
  const zaman = g?.at ? new Date(g.at) : null;
  const tamZaman = zaman ? zaman.toLocaleString('tr-TR', { day: 'numeric', month: 'long', year: zaman.getFullYear() === new Date().getFullYear() ? undefined : 'numeric', hour: '2-digit', minute: '2-digit' }) : '';
  return (
    <div className={`v15-card apr15-durum ${cevrim ? 'is-cevrim' : ''}`}>
      <span className="apr15-nokta" aria-hidden />
      <div>
        <b>{cevrim ? 'Şu an çevrimiçi' : `Son görülme: ${once(g?.at)}`}</b>
        {cevrim && (g?.etkinlik || p.simdi) && <small><Activity aria-hidden /> {p.simdi ? `Şu an ${p.simdi.ad} çalışıyor (${p.simdi.modul})` : g?.etkinlik}</small>}
        {!cevrim && p.simdi && <small><Activity aria-hidden /> Az önce {p.simdi.ad} çalışıyordu</small>}
        {!cevrim && tamZaman && <small><CalendarDays aria-hidden /> {tamZaman}</small>}
      </div>
    </div>
  );
}

/** Günlük ortalamalar (etkin gün başına) + son 14 gün çubuk grafiği */
function Gunluk({ p }: { p: AcikProfil }) {
  const gunler = p.gunler || [];
  if (!gunler.length) return null;
  const aktif14 = gunler.filter((x) => x.sn >= 60 || x.soru > 0);
  const n = Math.max(1, aktif14.length);
  const ortSn = aktif14.reduce((a, x) => a + x.sn, 0) / n;
  const ortSoru = Math.round(aktif14.reduce((a, x) => a + x.soru, 0) / n);
  const ortDers = (p.dersler?.length || 0) && p.aktifGun ? Math.max(1, Math.round(((p.dersler?.length || 0) / p.aktifGun) * 10) / 10) : 0;
  const max = Math.max(1, ...gunler.map((x) => x.sn));
  const enIyi = gunler.reduce((a, x) => (x.sn > a.sn ? x : a), gunler[0]);
  return (
    <section className="v15-card apr15-kutu apr15-gunluk is-tam">
      <h3><CalendarDays aria-hidden /> Günlük istatistikler <span className="apr15-say">son 14 gün · {aktif14.length} gün etkin</span></h3>
      <div className="apr15-gun-ort">
        <span><small>Günlük çalışma</small><b>{sure(ortSn)}</b></span>
        <span><small>Günlük soru</small><b>{sayi(ortSoru)}</b></span>
        <span><small>Günlük ders</small><b>{ortDers ? String(ortDers).replace('.', ',') : '—'}</b></span>
        <span><small>Toplam etkin gün</small><b>{sayi(p.aktifGun || 0)}</b></span>
      </div>
      <div className="apr15-grafik" role="img" aria-label={`Son 14 gün çalışma; en yoğun gün ${sure(enIyi.sn)}`}>
        {gunler.map((x) => {
          const d = new Date(`${x.g}T12:00:00`);
          return (
            <span key={x.g} className="apr15-gun" title={`${d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })}: ${sure(x.sn)}, ${x.soru} soru`}>
              <i style={{ height: `${x.sn ? Math.max(6, (x.sn / max) * 100) : 0}%` }} className={x.g === enIyi.g && x.sn ? 'is-tepe' : ''} />
              {x.soru > 0 && <em>{x.soru}</em>}
              <small>{GUN_AD[d.getDay()]}</small>
            </span>
          );
        })}
      </div>
      <p className="apr15-not apr15-gun-not">Ortalamalar çalışılan günlere göredir. Sütun yüksekliği çalışma süresi, üstündeki sayı çözülen sorudur.</p>
    </section>
  );
}

function Halka({ yuzde }: { yuzde: number | null }) {
  const r = 30, c = 2 * Math.PI * r, v = yuzde ?? 0;
  return (
    <svg className="apr15-halka" viewBox="0 0 72 72" role="img" aria-label={yuzde == null ? 'Doğru oranı yok' : `Doğru oranı yüzde ${yuzde}`}>
      <circle cx="36" cy="36" r={r} className="apr15-halka-iz" />
      <circle cx="36" cy="36" r={r} className="apr15-halka-dol" strokeDasharray={`${(v / 100) * c} ${c}`} transform="rotate(-90 36 36)" />
      <text x="36" y="41" textAnchor="middle">{yuzde == null ? '—' : `%${yuzde}`}</text>
    </svg>
  );
}

function Olcu({ ikon, ad, deger, alt }: { ikon: React.ReactNode; ad: string; deger: string; alt?: string }) {
  return <div className="v15-card apr15-o"><span className="apr15-o-ik">{ikon}</span><small>{ad}</small><b>{deger}</b>{alt && <small>{alt}</small>}</div>;
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
    <div className="apr15-perde" role="dialog" aria-modal="true" aria-label="Soru çözmeye davet et" onClick={kapat}>
      <div className="v15-card apr15-pencere" onClick={(e) => e.stopPropagation()}>
        <div className="apr15-pencere-bas"><b>{ad} kişisini davet et</b><button type="button" className="v15-btn is-ghost" aria-label="Kapat" onClick={kapat}><X aria-hidden /></button></div>
        <p className="apr15-not">Önce Oyunlar'da bir oda kur, ekrandaki oda kodunu buraya yaz. Arkadaşın davete dokununca aynı odaya katılır.</p>
        <label className="apr15-alan"><span>Oda kodu</span>
          <input value={oda} onChange={(e) => setOda(e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 6))} placeholder="Örn. K7MPA" autoCapitalize="characters" onKeyDown={(e) => { if (e.key === 'Enter') void gonder(); }} />
        </label>
        {durum && <p className="apr15-not" role="status">{durum}</p>}
        <div className="apr15-dugmeler">
          <button type="button" className="v15-btn" disabled={mesgul} onClick={() => void gonder()}>Davet gönder</button>
          <button type="button" className="v15-btn is-soft" onClick={() => git('/sorular/oyunlar')}>Oyunlar'da oda kur</button>
        </div>
      </div>
    </div>
  );
}

export function Bos({ baslik, metin }: { baslik: string; metin: string }) {
  return <div className="v15-card apr15-bos"><b>{baslik}</b><p>{metin}</p></div>;
}
