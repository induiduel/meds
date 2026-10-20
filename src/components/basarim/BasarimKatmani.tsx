/**
 * Uygulama geneli başarım katmanı (App kökünde): oturumla depoyu başlatır, dönem/kurul bilgisi yoksa girişte zorunlu
 * seçim ekranını, yeni ödül varsa kutlamayı gösterir.
 */
import React, { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { GraduationCap } from 'lucide-react';
import takvim from '../../data/kurul_takvimi_ozet.json';
import { aktifKurul } from '../../services/kurulTakvimi';
import { basarimBaslat, profilKaydet, useBasarim } from '../../services/basarimIstemci';
import { KutlamaKatmani } from './KutlamaKatmani';
import { AtpIkon } from './ortak';
import '../../styles/basarim.css';

const TAKVIM_DONEM = Number((takvim as any).donem || 3);
const KURULLAR: { kurul: number; ad: string }[] = (takvim as any).kurullar || [];
const tr = (s: string) => s.toLocaleLowerCase('tr-TR').replace(/(^|\s)\S/g, (m) => m.toLocaleUpperCase('tr-TR'));

/** Dönem + kurul seçici (giriş ekranı ve Başarımlar › profil düzenleme aynı parçayı kullanır). */
export function DonemKurulSecici({ ilk, onKaydet, kaydetYazi = 'Başla' }: { ilk?: { donem: number | null; kurul: number | null }; onKaydet: (d: number, k: number) => Promise<void>; kaydetYazi?: string }) {
  const [donem, setDonem] = useState<number | null>(ilk?.donem ?? null);
  const [kurul, setKurul] = useState<number | null>(ilk?.kurul ?? null);
  const [bekle, setBekle] = useState(false);
  const [hata, setHata] = useState('');
  const takvimli = donem === TAKVIM_DONEM;
  useEffect(() => {
    if (donem === TAKVIM_DONEM && kurul == null) setKurul(aktifKurul().kurul);
  }, [donem]);
  const kurulSec = takvimli ? KURULLAR.map((k) => ({ no: k.kurul, ad: tr(k.ad.replace(/\s*KURULU$/i, '')) })) : Array.from({ length: 8 }, (_, i) => ({ no: i + 1, ad: '' }));
  const kaydet = async () => {
    if (!donem || !kurul) return;
    setBekle(true); setHata('');
    try { await onKaydet(donem, kurul); } catch (e: any) { setHata(e?.message || 'Kaydedilemedi'); } finally { setBekle(false); }
  };
  return (
    <div className="bs-dk">
      <fieldset className="bs-dk-grup">
        <legend>Kaçıncı dönemdesin?</legend>
        <div className="bs-dk-donem">
          {[1, 2, 3, 4, 5, 6].map((d) => (
            <button key={d} type="button" aria-pressed={donem === d} className={donem === d ? 'is-secili' : ''} onClick={() => { setDonem(d); setKurul(null); }}>
              <b>{d}</b><span>Dönem</span>
            </button>
          ))}
        </div>
      </fieldset>
      {donem != null && (
        <fieldset className="bs-dk-grup">
          <legend>Şu an hangi kuruldasın?</legend>
          <div className={`bs-dk-kurul${takvimli ? ' is-adli' : ''}`}>
            {kurulSec.map((k) => (
              <button key={k.no} type="button" aria-pressed={kurul === k.no} className={kurul === k.no ? 'is-secili' : ''} onClick={() => setKurul(k.no)}>
                <b>{k.no}. Kurul</b>{k.ad && <span>{k.ad}</span>}
              </button>
            ))}
          </div>
          {!takvimli && <p className="bs-dk-not">Bu dönemin ders takvimi henüz eklenmedi; kurul hedefleri şimdilik takvim ayına göre sayılır.</p>}
        </fieldset>
      )}
      {hata && <p className="bs-dk-hata" role="alert">{hata}</p>}
      <button type="button" className="bs-dk-kaydet" disabled={!donem || !kurul || bekle} onClick={kaydet}>{bekle ? 'Kaydediliyor…' : kaydetYazi}</button>
    </div>
  );
}

function GirisSecimi({ ad }: { ad?: string | null }) {
  const { tanim } = useBasarim();
  return createPortal(
    <div className="bs-giris" role="dialog" aria-modal="true" aria-labelledby="bs-giris-b">
      <div className="bs-giris-kart">
        <span className="bs-giris-ikon" aria-hidden><GraduationCap /></span>
        <h2 id="bs-giris-b">{ad ? `Hoş geldin, ${ad.split(' ')[0]}` : 'Hoş geldin'}</h2>
        <p>Hedeflerin, kurul takvimin ve sıralaman dönemine göre kurulur. Sıralamada yalnız kendi dönemindekilerle yarışırsın.</p>
        <p className="bs-giris-atp"><AtpIkon boyut={16} canli /> Başlangıç hediyen: <b>{tanim.atp.baslangic} mol ATP</b></p>
        <DonemKurulSecici onKaydet={(d, k) => profilKaydet(d, k, ad || undefined)} />
      </div>
    </div>,
    document.body,
  );
}

export default function BasarimKatmani({ uid, ad, kapali }: { uid: string | null; ad?: string | null; kapali?: boolean }) {
  const { durum } = useBasarim();
  useEffect(() => { basarimBaslat(uid); }, [uid]);
  if (!uid || kapali) return null;
  if (durum && !durum.profil.donem) return <GirisSecimi ad={ad} />;
  return <KutlamaKatmani />;
}
