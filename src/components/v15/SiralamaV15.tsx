import React, { useEffect, useState } from 'react';
import { Trophy, Users } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { sayi, useBasarim, type SiraSatir } from '../../services/basarimIstemci';
import { useProfil } from '../../services/profilKurulum';
import { useV15Baslik } from './baslik';
import '../../styles/v15/siralama.css';

/**
 * v15 · Sıralama (tasarım sistemi v15 › `siralama`). Rota: leaderboard (v15 açıkken).
 * Veri: başarım motoru puan sıralaması (GET /api/basarim/siralama). Sınıfım = aynı üniversite + aynı dönem (yer=sinif),
 * Üniversite = aynı üniversitenin tüm dönemleri (yer=uni), Türkiye = dönemdeki herkes. Üniversite profil kurulumundan
 * (profilKurulum) POST /api/basarim/universite ile sunucuya bildirilir. Arkadaş altyapısı yok → boş durum.
 */
type Sekme = 'sinif' | 'uni' | 'tr' | 'arkadas';
type Kapsam = 'hafta' | 'kurul' | 'tum';
const SEKMELER: [Sekme, string][] = [['sinif', 'Sınıfım'], ['uni', 'Üniversite'], ['tr', 'Türkiye'], ['arkadas', 'Arkadaşlar']];
const KAPSAMLAR: [Kapsam, string][] = [['hafta', 'Bu hafta'], ['kurul', 'Bu kurul'], ['tum', 'Tümü']];
interface Yanit { donem: number; universite?: string; satir: SiraSatir[] }

const bas = (ad: string) => ad.split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toLocaleUpperCase('tr-TR') || '?';
function Avatar({ s, boy }: { s: SiraSatir; boy?: 'b' }) {
  return (
    <span className={`sr15-av ${boy === 'b' ? 'is-b' : ''}`} aria-hidden>
      {s.foto ? <img src={s.foto} alt="" loading="lazy" /> : bas(s.ad)}
    </span>
  );
}

export default function SiralamaV15() {
  const profil = useProfil();
  const { durum } = useBasarim();
  const [sekme, setSekme] = useState<Sekme>('sinif');
  const [kapsam, setKapsam] = useState<Kapsam>('hafta');
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
    if (sekme === 'arkadas' || (yerli && (!uni || !uniGonderildi))) { setVeri(null); return; }
    let vazgec = false;
    setYukleniyor(true); setHata('');
    const yer = yerli ? `&yer=${sekme}` : '';
    void safeJsonFetch<any>(`/api/basarim/siralama?kapsam=${kapsam}${yer}`).then((r) => {
      if (vazgec) return;
      if (!r.ok) setHata(r.data?.error || r.error || 'Sıralama alınamadı.');
      else setVeri(r.data as Yanit);
    }).finally(() => { if (!vazgec) setYukleniyor(false); });
    return () => { vazgec = true; };
  }, [sekme, kapsam, uni, uniGonderildi, yerli]);

  const satir = veri?.satir || [];
  const podyum = satir.slice(0, 3);
  const kalan = satir.slice(3);

  let govde: React.ReactNode;
  if (sekme === 'arkadas') {
    govde = <Bos ikon={<Users aria-hidden />} baslik="Henüz arkadaş yok" metin="Arkadaş ekleyince burada görünür." />;
  } else if (yerli && !uni) {
    govde = <Bos ikon={<Users aria-hidden />} baslik="Üniversiten belli değil" metin="Profil kurulumunda üniversiteni seçince sınıfının ve üniversitenin sıralaması burada görünür." />;
  } else if (hata) {
    govde = <Bos ikon={<Trophy aria-hidden />} baslik="Sıralama alınamadı" metin={hata} />;
  } else if (!veri || (yukleniyor && !satir.length)) {
    govde = <p className="sr15-not">Yükleniyor…</p>;
  } else if (!satir.length) {
    govde = <Bos ikon={<Trophy aria-hidden />} baslik="Bu aralıkta puan yok" metin={yerli ? 'Seninle aynı üniversiteyi seçmiş ve bu aralıkta puan toplamış kimse yok. Çalıştıkça ilk sen yer alırsın.' : 'Bu aralıkta henüz kimse puan toplamadı.'} />;
  } else {
    const sira = [podyum[1], podyum[0], podyum[2]].filter(Boolean) as SiraSatir[];
    govde = (
      <>
        <div className="sr15-podyum" aria-label="İlk üç">
          {sira.map((s) => (
            <div key={s.sira} className={`sr15-pd is-${s.sira} ${s.ben ? 'is-ben' : ''}`}>
              <Avatar s={s} boy={s.sira === 1 ? 'b' : undefined} />
              <b className="sr15-pd-ad">{s.ben ? 'Sen' : s.ad}</b>
              <span className={`v15-tag ${s.sira === 1 ? 'is-w' : ''}`}>{s.sira}.</span>
              <span className="sr15-pd-puan">{sayi(s.puan)}</span>
              <div className="sr15-pd-kaide" />
            </div>
          ))}
        </div>
        {kalan.length > 0 && (
          <ol className="v15-card sr15-liste">
            {kalan.map((s) => (
              <li key={s.sira} className={`sr15-sat ${s.ben ? 'is-ben' : ''}`} aria-current={s.ben ? 'true' : undefined}>
                <span className="sr15-no">{s.sira}</span>
                <Avatar s={s} />
                <span className="sr15-ad">
                  <b>{s.ben ? 'Sen' : s.ad}</b>
                  {(s.unvan || s.kidem) && <small>{s.unvan || s.kidem}</small>}
                </span>
                <span className="sr15-puan">{sayi(s.puan)}</span>
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
      {sekme !== 'arkadas' && (
        <div className="sr15-kapsam" role="group" aria-label="Zaman aralığı">
          {KAPSAMLAR.map(([id, t]) => (
            <button key={id} type="button" className={`v15-tag ${kapsam === id ? 'is-on' : ''}`} aria-pressed={kapsam === id} onClick={() => setKapsam(id)}>{t}</button>
          ))}
        </div>
      )}
      {yerli && uni && <p className="sr15-not">{uni}{sekme === 'sinif' && veri?.donem && veri.donem > 0 ? ` · ${veri.donem}. dönem` : ''}</p>}
      {govde}
      {sekme !== 'arkadas' && <p className="sr15-not">Sıra başarım puanına göre; puan çalışma, soru ve başarımlarla kazanılır.</p>}
    </div>
  );
}

function Bos({ ikon, baslik, metin }: { ikon: React.ReactNode; baslik: string; metin: string }) {
  return (
    <div className="v15-card sr15-bos">
      <span className="v15-tile">{ikon}</span>
      <b>{baslik}</b>
      <p>{metin}</p>
    </div>
  );
}
