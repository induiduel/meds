import React, { useEffect, useState } from 'react';
import { Lock, Trophy, Users } from 'lucide-react';
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
type Olcu = 'puan' | 'calisma';
const SEKMELER: [Sekme, string][] = [['sinif', 'Sınıfım'], ['uni', 'Üniversite'], ['tr', 'Türkiye'], ['arkadas', 'Arkadaşlar']];
const KAPSAMLAR: Record<Olcu, [Kapsam, string][]> = {
  puan: [['hafta', 'Bu hafta'], ['kurul', 'Bu kurul'], ['tum', 'Tümü']],
  calisma: [['gun', 'Bugün'], ['hafta', 'Bu hafta']],
};
type Satir = SiraSatir & { kimlik?: string; sn?: number; gizli?: boolean; dersler?: { ad: string }[] };
interface Yanit { donem?: number; universite?: string; arkadasN?: number; satir: Satir[] }

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
  const [sekme, setSekme] = useState<Sekme>('sinif');
  const [olcu, setOlcu] = useState<Olcu>('puan');
  const [kapsam, setKapsam] = useState<Kapsam>('hafta');
  const [tazele, setTazele] = useState(0);
  useLiveEvent('siralama_changed', () => setTazele((n) => n + 1), { debounceMs: 2000 });
  useLiveEvent('arkadas_changed', () => { if (sekme === 'arkadas') setTazele((n) => n + 1); }, { debounceMs: 800 });
  const olcuSec = (o: Olcu) => { setOlcu(o); setKapsam(o === 'calisma' ? 'gun' : 'hafta'); };
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
    void safeJsonFetch<any>(`/api/kisi/siralama?olcu=${olcu}&kapsam=${kapsam}&yer=${yer}`).then((r) => {
      if (vazgec) return;
      if (!r.ok) setHata(r.data?.error || r.error || 'Sıralama alınamadı.');
      else setVeri(r.data as Yanit);
    }).finally(() => { if (!vazgec) setYukleniyor(false); });
    return () => { vazgec = true; };
  }, [sekme, olcu, kapsam, uni, uniGonderildi, yerli, tazele]);

  const satir = veri?.satir || [];
  const podyum = satir.slice(0, 3);
  const kalan = satir.slice(3);

  let govde: React.ReactNode;
  const deger = (s: Satir) => (olcu === 'calisma' ? sure(s.sn || 0) : sayi(s.puan));
  const ac = (s: Satir) => { if (s.kimlik) git(profilYolu(s.kimlik)); };
  if (sekme === 'arkadas' && veri && !veri.arkadasN) {
    govde = (
      <div className="v15-card sr15-bos">
        <span className="v15-tile"><Users aria-hidden /></span>
        <b>Henüz arkadaş yok</b>
        <p>Diğer sekmelerde bir kişiye dokunup profilinden arkadaş ekle ya da Arkadaşlar sayfasında adıyla ara.</p>
        <button type="button" className="v15-btn is-soft" onClick={() => git('/arkadaslar')}>Arkadaş bul</button>
      </div>
    );
  } else if (yerli && !uni) {
    govde = <Bos ikon={<Users aria-hidden />} baslik="Üniversiten belli değil" metin="Profil kurulumunda üniversiteni seçince sınıfının ve üniversitenin sıralaması burada görünür."
      /* H166: boş durumda profil kurulumunu açan eylem */ eylem={{ ad: 'Üniversiteni seç', f: profilKurulumAc }} />;
  } else if (hata) {
    govde = <Bos ikon={<Trophy aria-hidden />} baslik="Sıralama alınamadı" metin={hata} />;
  } else if (!veri || (yukleniyor && !satir.length)) {
    govde = <p className="sr15-not">Yükleniyor…</p>;
  } else if (!satir.length) {
    const ne = olcu === 'calisma' ? 'çalışma kaydı' : 'puan';
    govde = <Bos ikon={<Trophy aria-hidden />} baslik={`Bu aralıkta ${ne} yok`} metin={yerli ? `Seninle aynı üniversiteyi seçmiş ve bu aralıkta ${ne} olan kimse yok. Çalıştıkça ilk sen yer alırsın.` : `Bu aralıkta henüz kimsenin ${ne} yok.`} />;
  } else {
    const sira = [podyum[1], podyum[0], podyum[2]].filter(Boolean) as Satir[];
    govde = (
      <>
        <div className="sr15-podyum" aria-label="İlk üç">
          {sira.map((s) => (
            <button type="button" key={s.sira} className={`sr15-pd is-${s.sira} ${s.ben ? 'is-ben' : ''}`} onClick={() => ac(s)} disabled={!s.kimlik} aria-label={`${s.sira}. ${s.ben ? 'Sen' : s.ad}${s.kimlik ? ', profili aç' : ''}`}>
              <Avatar s={s} boy={s.sira === 1 ? 'b' : undefined} />
              <b className="sr15-pd-ad">{s.ben ? 'Sen' : s.ad}</b>
              <span className={`v15-tag ${s.sira === 1 ? 'is-w' : ''}`}>{s.sira}.</span>
              <span className="sr15-pd-puan">{deger(s)}</span>
              <div className="sr15-pd-kaide" />
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

  return (
    <div className="sr15">
      <div className="v15-seg" role="tablist" aria-label="Sıralama kapsamı">
        {SEKMELER.map(([id, t]) => (
          <button key={id} type="button" role="tab" aria-selected={sekme === id} aria-current={sekme === id ? 'page' : undefined} onClick={() => setSekme(id)}>{t}</button>
        ))}
      </div>
      <div className="sr15-kapsam" role="group" aria-label="Sıralama ölçüsü">
        {([['puan', 'Puan'], ['calisma', 'Çalışma süresi']] as [Olcu, string][]).map(([id, t]) => (
          <button key={id} type="button" className={`v15-tag ${olcu === id ? 'is-on' : ''}`} aria-pressed={olcu === id} onClick={() => olcuSec(id)}>{t}</button>
        ))}
      </div>
      {(
        <div className="sr15-kapsam" role="group" aria-label="Zaman aralığı">
          {KAPSAMLAR[olcu].map(([id, t]) => (
            <button key={id} type="button" className={`v15-tag ${kapsam === id ? 'is-on' : ''}`} aria-pressed={kapsam === id} onClick={() => setKapsam(id)}>{t}</button>
          ))}
        </div>
      )}
      {yerli && uni && <p className="sr15-not">{uni}{sekme === 'sinif' && veri?.donem && veri.donem > 0 ? ` · ${veri.donem}. dönem` : ''}</p>}
      {govde}
      <p className="sr15-not">{olcu === 'calisma' ? 'Sıra etkin çalışma süresine göre. Bir kişiye dokununca profilini açarsın.' : 'Sıra başarım puanına göre; puan çalışma, soru ve başarımlarla kazanılır. Bir kişiye dokununca profilini açarsın.'}</p>
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
