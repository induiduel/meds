import React, { useEffect, useState } from 'react';
import { Award, ChevronDown, CircleCheck, Clock, Crown, Dna, Flag, Gamepad2, Info, Lock, Trophy, Users } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { sayi, useBasarim, type SiraSatir } from '../../services/basarimIstemci';
import { useProfil } from '../../services/profilKurulum';
import { useV15Baslik } from './baslik';
import { profilKurulumAc } from './ProfilKurulumV15';
import { git, profilYolu, sure } from '../../services/arkadasIstemci';
import { useLiveEvent } from '../../hooks/useLiveEvent';
import '../../styles/v15/siralama.css';

/**
 * v15 · Sıralama (tasarım sistemi v15 › `siralama`). Rota: leaderboard (v15 açıkken).
 * Veri: başarım motoru puan sıralaması (GET /api/basarim/siralama). Sınıfım = aynı üniversite + aynı dönem (yer=sinif),
 * Üniversite = aynı üniversitenin tüm dönemleri (yer=uni), Türkiye = dönemdeki herkes. Üniversite profil kurulumundan
 * (profilKurulum) POST /api/basarim/universite ile sunucuya bildirilir.
 * 2026-10-27: tek uç GET /api/kisi/siralama (services/arkadaslik.ts): ölçü Puan | Çalışma süresi, aralık puan için
 * hafta/kurul/tüm, çalışma için bugün/hafta; Arkadaşlar sekmesi arkadaş listesine göre. Satıra dokununca açık profil
 * (/kisi/<kimlik>); profilini gizleyen "Gizli kullanıcı" olarak görünür ve açılmaz.
 */
type Sekme = 'sinif' | 'uni' | 'tr' | 'arkadas';
type Kapsam = 'hafta' | 'kurul' | 'tum' | 'gun';
type Olcu = 'puan' | 'calisma' | 'soru' | 'bitir' | 'oyun' | 'hucre' | 'basarim';
const SEKMELER: [Sekme, string][] = [['sinif', 'Sınıfım'], ['uni', 'Üniversite'], ['tr', 'Türkiye'], ['arkadas', 'Arkadaş']];
/**
 * 2026-10-29: ölçüler tek şeritte (oyun, hücre, soru, bitirilen konu, başarım eklendi). Her ölçünün kendi zaman aralıkları,
 * birimi ve açıklaması burada; zaman aralığı olmayan ölçüde (hücre, başarım, oyun) aralık satırı gizlenir.
 */
const OLCULER: { id: Olcu; ad: string; ic: React.ComponentType<{ size?: number; 'aria-hidden'?: boolean }>; birim: string; aciklama: string; kapsam: [Kapsam, string][] }[] = [
  { id: 'puan', ad: 'Puan', ic: Trophy, birim: 'puan', aciklama: 'Başarım puanı: çalışma, soru ve başarımlarla kazanılır.', kapsam: [['hafta', 'Bu hafta'], ['kurul', 'Bu kurul'], ['tum', 'Tümü']] },
  { id: 'calisma', ad: 'Çalışma', ic: Clock, birim: '', aciklama: 'Etkin çalışma süresi (ekran açıkken ve çalışırken).', kapsam: [['gun', 'Bugün'], ['hafta', 'Bu hafta']] },
  { id: 'soru', ad: 'Soru', ic: CircleCheck, birim: 'soru', aciklama: 'Çözülen soru sayısı.', kapsam: [['gun', 'Bugün'], ['hafta', 'Bu hafta'], ['tum', 'Tümü']] },
  { id: 'bitir', ad: 'Bitirilen', ic: Flag, birim: 'konu', aciklama: 'Bitti olarak işaretlenen konu sayısı.', kapsam: [['hafta', 'Bu hafta'], ['tum', 'Tümü']] },
  { id: 'oyun', ad: 'Oyun', ic: Gamepad2, birim: 'puan', aciklama: 'Oyunlardaki en iyi skorların toplamı (her oyun ve ders için en iyisi). Eşleştir süre tuttuğu için girmez.', kapsam: [] },
  { id: 'hucre', ad: 'Hücre', ic: Dna, birim: '', aciklama: 'Hücrem’de açılan evrim basamağı; eşitlikte toplam kazanılan ATP öne geçirir.', kapsam: [] },
  { id: 'basarim', ad: 'Başarım', ic: Award, birim: 'başarım', aciklama: 'Kazanılan başarım rozeti sayısı.', kapsam: [] },
];
const OYUN_AD: Record<string, string> = { blitz: 'Blitz', hayatta: 'Hayatta kal', gorsel: 'Görselli soru', kaydir: 'Kaydır', sirala: 'Sırala', izgara: 'Eşleştirme ızgarası', bosluk: 'Terimi bul', solo: 'Tek kişilik' };
type Satir = SiraSatir & { kimlik?: string; sn?: number; deger?: number; gizli?: boolean; dersler?: { ad: string }[] };
interface Yanit { donem?: number; universite?: string; arkadasN?: number; benim?: number | null; kisi?: number; oyunlar?: string[]; satir: Satir[] }

const SECIM_KEY = 'medsoru_siralama_secim_v1';
interface Secim { sekme: Sekme; olcu: Olcu; kapsam: Kapsam; oyun: string }
const secimOku = (): Secim => {
  const v: Secim = { sekme: 'sinif', olcu: 'puan', kapsam: 'hafta', oyun: '' };
  try { const o = JSON.parse(localStorage.getItem(SECIM_KEY) || '{}'); return { ...v, ...o }; } catch { return v; }
};

const bas = (ad: string) => ad.split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toLocaleUpperCase('tr-TR') || '?';
function Avatar({ s, boy }: { s: Satir; boy?: 'b' }) {
  return (
    <span className={`sr15-av ${boy === 'b' ? 'is-b' : ''}`} aria-hidden>
      {s.gizli ? <Lock size={16} /> : s.foto ? <img src={s.foto} alt="" loading="lazy" /> : bas(s.ad)}
    </span>
  );
}

export default function SiralamaV15() {
  const profil = useProfil();
  const { durum } = useBasarim();
  const [secim, setSecimHam] = useState<Secim>(secimOku);
  const { sekme, olcu, oyun } = secim;
  const tanim = OLCULER.find((o) => o.id === olcu) || OLCULER[0];
  const kapsam: Kapsam = tanim.kapsam.some(([k]) => k === secim.kapsam) ? secim.kapsam : (tanim.kapsam[0]?.[0] || 'tum');
  const setSecim = (p: Partial<Secim>) => setSecimHam((s) => {
    const y = { ...s, ...p };
    try { localStorage.setItem(SECIM_KEY, JSON.stringify(y)); } catch { /* yok */ }
    return y;
  });
  const [tazele, setTazele] = useState(0);
  useLiveEvent('siralama_changed', () => setTazele((n) => n + 1), { debounceMs: 2000 });
  useLiveEvent('arkadas_changed', () => { if (sekme === 'arkadas') setTazele((n) => n + 1); }, { debounceMs: 800 });
  const [veri, setVeri] = useState<Yanit | null>(null);
  const [hata, setHata] = useState('');
  const [yukleniyor, setYukleniyor] = useState(false);
  const [uniGonderildi, setUniGonderildi] = useState(false);
  const uni = (profil.universite || '').trim();
  useV15Baslik({ baslik: 'Sıralama', alt: durum?.profil?.donem ? `${durum.profil.donem}. dönem` : undefined });

  // Profildeki üniversiteyi sunucuya bildir (süzgeç bunu kullanır)
  useEffect(() => {
    setUniGonderildi(false);
    if (!uni) return;
    let vazgec = false;
    void safeJsonFetch('/api/basarim/universite', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ universite: uni }) })
      .finally(() => { if (!vazgec) setUniGonderildi(true); });
    return () => { vazgec = true; };
  }, [uni]);

  const yerli = sekme === 'sinif' || sekme === 'uni';
  useEffect(() => {
    if (yerli && (!uni || !uniGonderildi)) { setVeri(null); return; }
    let vazgec = false;
    setYukleniyor(true); setHata('');
    const yer = sekme === 'tr' ? 'tr' : sekme;
    const ek = olcu === 'oyun' && oyun ? `&oyun=${encodeURIComponent(oyun)}` : '';
    void safeJsonFetch<any>(`/api/kisi/siralama?olcu=${olcu}&kapsam=${kapsam}&yer=${yer}${ek}`).then((r) => {
      if (vazgec) return;
      if (!r.ok) setHata(r.data?.error || r.error || 'Sıralama alınamadı.');
      else setVeri(r.data as Yanit);
    }).finally(() => { if (!vazgec) setYukleniyor(false); });
    return () => { vazgec = true; };
  }, [sekme, olcu, kapsam, oyun, uni, uniGonderildi, yerli, tazele]);

  const satir = veri?.satir || [];
  const podyum = satir.slice(0, 3);
  const kalan = satir.slice(3);
  const ham = (s: Satir) => (olcu === 'calisma' ? s.sn || 0 : olcu === 'puan' ? s.puan : s.deger ?? s.puan ?? 0);
  const yaz = (v: number) => (olcu === 'calisma' ? sure(v) : olcu === 'hucre' ? `${sayi(v)}. basamak` : `${sayi(v)}${tanim.birim ? ` ${tanim.birim}` : ''}`);
  const deger = (s: Satir) => yaz(ham(s));
  const ac = (s: Satir) => { if (s.kimlik) git(profilYolu(s.kimlik)); };
  const ben = satir.find((s) => s.ben);
  const onumdeki = ben && ben.sira > 1 ? satir.find((s) => s.sira === ben.sira - 1) : undefined;
  const fark = ben && onumdeki ? Math.max(0, ham(onumdeki) - ham(ben)) : 0;
  const benGoster = () => document.querySelector('.sr15 [aria-current="true"], .sr15-pd.is-ben')?.scrollIntoView({ behavior: 'smooth', block: 'center' });

  let govde: React.ReactNode;
  if (sekme === 'arkadas' && veri && !veri.arkadasN) {
    govde = <Bos ikon={<Users aria-hidden />} baslik="Henüz arkadaş yok" metin="Diğer sekmelerde bir kişiye dokunup profilinden arkadaş ekle ya da Arkadaşlar sayfasında adıyla ara." eylem={{ ad: 'Arkadaş bul', f: () => git('/arkadaslar') }} />;
  } else if (yerli && !uni) {
    govde = <Bos ikon={<Users aria-hidden />} baslik="Üniversiten belli değil" metin="Profil kurulumunda üniversiteni seçince sınıfının ve üniversitenin sıralaması burada görünür."
      /* H166: boş durumda profil kurulumunu açan eylem */ eylem={{ ad: 'Üniversiteni seç', f: profilKurulumAc }} />;
  } else if (hata) {
    govde = <Bos ikon={<Trophy aria-hidden />} baslik="Sıralama alınamadı" metin={hata} />;
  } else if (!veri || (yukleniyor && !satir.length)) {
    govde = <p className="sr15-not">Yükleniyor…</p>;
  } else if (!satir.length) {
    const ne = olcu === 'oyun' ? 'oyun skoru' : olcu === 'hucre' ? 'hücre basamağı' : olcu === 'calisma' ? 'çalışma kaydı' : tanim.birim || 'kayıt';
    govde = <Bos ikon={<tanim.ic aria-hidden />} baslik={`Burada henüz ${ne} yok`}
      metin={olcu === 'oyun' ? 'Oyunlarda rekor kırdıkça burada yer alırsın; skorlar hesabına eşitlenir.' : yerli ? `Seninle aynı üniversiteyi seçmiş ve bu aralıkta ${ne} olan kimse yok. İlk sen yer alabilirsin.` : `Bu aralıkta henüz kimsenin ${ne} yok.`}
      eylem={olcu === 'oyun' ? { ad: 'Oyunlara git', f: () => git('/sorular/oyunlar') } : olcu === 'hucre' ? { ad: 'Hücreme git', f: () => git('/hucrem') } : undefined} />;
  } else {
    const sira = [podyum[1], podyum[0], podyum[2]].filter(Boolean) as Satir[];
    govde = (
      <>
        <div className="sr15-podyum" aria-label="İlk üç">
          {sira.map((s) => (
            <button type="button" key={s.sira} className={`sr15-pd is-${s.sira} ${s.ben ? 'is-ben' : ''}`} onClick={() => ac(s)} disabled={!s.kimlik} aria-label={`${s.sira}. ${s.ben ? 'Sen' : s.ad}, ${deger(s)}${s.kimlik ? ', profili aç' : ''}`}>
              <span className="sr15-pd-ust">
                <Avatar s={s} boy={s.sira === 1 ? 'b' : undefined} />
                {s.sira === 1 && <Crown className="sr15-tac" size={18} aria-hidden />}
              </span>
              <b className="sr15-pd-ad">{s.ben ? 'Sen' : s.ad}</b>
              <span className="sr15-pd-puan">{deger(s)}</span>
              <span className="sr15-pd-kaide">{s.sira}</span>
            </button>
          ))}
        </div>
        {kalan.length > 0 && (
          <ol className="v15-card sr15-liste">
            {kalan.map((s) => (
              <li key={s.sira} aria-current={s.ben ? 'true' : undefined}>
                <button type="button" className={`sr15-sat ${s.ben ? 'is-ben' : ''}`} onClick={() => ac(s)} disabled={!s.kimlik}>
                  <span className="sr15-no">{s.sira}</span>
                  <Avatar s={s} />
                  <span className="sr15-ad">
                    <b>{s.ben ? 'Sen' : s.ad}</b>
                    {olcu === 'calisma' && s.dersler?.length ? <small>{s.dersler.map((d) => d.ad).join(', ')}</small> : (s.unvan || s.kidem) && <small>{s.unvan || s.kidem}</small>}
                  </span>
                  <span className="sr15-puan">{deger(s)}</span>
                </button>
              </li>
            ))}
          </ol>
        )}
      </>
    );
  }

  const oyunlar = veri?.oyunlar || [];
  return (
    <div className="sr15">
      <div className="sr15-olcu" role="tablist" aria-label="Neye göre sıralansın">
        {OLCULER.map((o) => (
          <button key={o.id} type="button" role="tab" aria-selected={olcu === o.id} className={olcu === o.id ? 'is-on' : ''} onClick={() => setSecim({ olcu: o.id })}>
            <o.ic size={18} aria-hidden />
            <span>{o.ad}</span>
          </button>
        ))}
      </div>

      <div className="v15-card sr15-suz">
        <div className="v15-seg" role="tablist" aria-label="Kimlerle">
          {SEKMELER.map(([id, t]) => (
            <button key={id} type="button" role="tab" aria-selected={sekme === id} onClick={() => setSecim({ sekme: id })}>{t}</button>
          ))}
        </div>
        {(tanim.kapsam.length > 1 || (olcu === 'oyun' && oyunlar.length > 0)) && (
          <div className="sr15-suz-alt">
            {tanim.kapsam.length > 1 && (
              <div className="sr15-aralik" role="group" aria-label="Zaman aralığı">
                {tanim.kapsam.map(([id, t]) => (
                  <button key={id} type="button" aria-pressed={kapsam === id} className={kapsam === id ? 'is-on' : ''} onClick={() => setSecim({ kapsam: id })}>{t}</button>
                ))}
              </div>
            )}
            {olcu === 'oyun' && oyunlar.length > 0 && (
              <label className="sr15-oyun">
                <span className="sr-only">Oyun</span>
                <select value={oyun} onChange={(e) => setSecim({ oyun: e.target.value })}>
                  <option value="">Tüm oyunlar</option>
                  {oyunlar.map((o) => <option key={o} value={o}>{OYUN_AD[o] || o}</option>)}
                </select>
              </label>
            )}
          </div>
        )}
        <p className="sr15-acik"><Info size={14} aria-hidden /> {tanim.aciklama}{yerli && uni ? ` · ${uni}${sekme === 'sinif' && veri?.donem && veri.donem > 0 ? `, ${veri.donem}. dönem` : ''}` : ''}</p>
      </div>

      {ben && satir.length > 0 && (
        <button type="button" className="v15-card sr15-ben" onClick={benGoster} aria-label={`Sıran ${ben.sira}${veri?.kisi ? ` / ${veri.kisi}` : ''}, listede göster`}>
          <span className="sr15-ben-sira"><small>Sıran</small><b>{ben.sira}</b>{veri?.kisi ? <small>/ {sayi(veri.kisi)}</small> : null}</span>
          <span className="sr15-ben-orta">
            <b>{deger(ben)}</b>
            <small>{ben.sira === 1 ? 'Zirvedesin, farkı koru.' : onumdeki ? `${ben.sira - 1}. sıraya ${olcu === 'calisma' ? sure(fark || 60) : yaz(Math.max(1, fark))} kaldı` : ''}</small>
          </span>
          <ChevronDown size={18} aria-hidden className="sr15-ben-ok" />
        </button>
      )}

      {govde}
      <p className="sr15-not">Bir kişiye dokununca profilini açarsın. Profilini gizleyenler “Gizli kullanıcı” olarak görünür.</p>
    </div>
  );
}

function Bos({ ikon, baslik, metin, eylem }: { ikon: React.ReactNode; baslik: string; metin: string; eylem?: { ad: string; f: () => void } }) {
  return (
    <div className="v15-card sr15-bos">
      <span className="v15-tile">{ikon}</span>
      <b>{baslik}</b>
      <p>{metin}</p>
      {eylem && <button type="button" className="v15-btn is-soft" onClick={eylem.f}>{eylem.ad}</button>}
    </div>
  );
}
