/**
 * Sesli ders yerel ilerleme temizliği. Yalnız bu cihazdaki kayıtlar: "kaldığın yer" (`medsoru_canli_ders_konum_v1`) ve
 * çalışma takibi (`medsoru_calisma_takip_v1`: süre, bitti işareti, tekrar turu). Ders sesleri, indirilenler ve listem dokunulmaz.
 *  - `SifirlaDugme`: tek ders, iki adımlı onay (satır seçenekleri / ders ayrıntısı).
 *  - `TemizleDiyalog`: görünen listenin dersleri için toplu temizlik (kaldığın yer ve/veya süre+bitti ayrı seçilir).
 */
import React, { useEffect, useMemo, useState, useSyncExternalStore } from 'react';
import { Check, Eraser, RotateCcw, X } from 'lucide-react';
import { CD_KONUM_OLAY, cdKayitliKonum, cdKonumListesi, cdKonumSil, cdKonumlariTemizle } from './canliDersStore';
import { bittiMi, konuSifirla, modulSifirla, sesliKonuId, useKonuKaydi, useTakip } from '../../services/calismaTakip';

let konumSurum = 0;
const konumAbone = (f: () => void) => {
  const g = () => { konumSurum++; f(); };
  window.addEventListener(CD_KONUM_OLAY, g);
  window.addEventListener('storage', g);
  return () => { window.removeEventListener(CD_KONUM_OLAY, g); window.removeEventListener('storage', g); };
};
/** Kaldığın yer kayıtları değiştikçe artan sayaç (bağımlılık olarak kullanılır) */
export const useCdKonumSurum = () => useSyncExternalStore(konumAbone, () => konumSurum, () => 0);
/** Bu dersin kaldığın yer kaydı var mı; üst bileşen biliyorsa onu kullanır, yoksa depodan okur */
const useCdKonumVar = (key: string, bilinen?: boolean) => {
  const s = useCdKonumSurum();
  return useMemo(() => (bilinen != null ? bilinen : !!cdKayitliKonum(key)), [key, bilinen, s]);
};

/** Tek dersin yerel ilerlemesini (kaldığın yer + süre/bitti kaydı) iki adımlı onayla siler. */
export function SifirlaDugme({ dersKey, baslik, konumVar, sinif }: { dersKey: string; baslik: string; /** kaldığın yer kaydı var mı (üst bileşen haritasından) */ konumVar?: boolean; /** düğme sınıfı (v15: 'v15-btn is-ghost') */ sinif?: string }) {
  const kayit = useKonuKaydi('sesli', dersKey);
  const konumVar2 = useCdKonumVar(dersKey, konumVar);
  const [onay, setOnay] = useState(false);
  useEffect(() => {
    if (!onay) return;
    const t = setTimeout(() => setOnay(false), 6000);
    return () => clearTimeout(t);
  }, [onay]);
  if (!konumVar2 && !kayit) return null;
  const btn = sinif || 'cd-btn is-ince';
  const sifirla = () => {
    cdKonumSil(dersKey);
    konuSifirla('sesli', dersKey);
    setOnay(false);
  };
  if (onay) {
    return (
      <span className="cdl-sifirla-onay" role="group" aria-label={`İlerlemeyi sıfırla: ${baslik}`}>
        <small>Kaldığın yer, süre ve bitti işareti silinir.</small>
        <button type="button" className={`${btn} is-tehlike`} onClick={sifirla} autoFocus><RotateCcw aria-hidden /> <span>Evet, sıfırla</span></button>
        <button type="button" className={btn} onClick={() => setOnay(false)}>Vazgeç</button>
      </span>
    );
  }
  return (
    <button type="button" className={`${btn} cdl-sifirla-btn`} onClick={() => setOnay(true)}
      title="Bu dersin yerel ilerlemesini sil: kaldığın yer, dinleme süren ve bitti işareti" aria-label={`İlerlemeyi sıfırla: ${baslik}`}>
      <RotateCcw aria-hidden /> <span>İlerlemeyi sıfırla</span>
    </button>
  );
}

/** Toplu temizlik: görünen dönemin derslerinde kaldığın yer kayıtları ve/veya çalışma takibi (süre, bitti) silinir. */
export function TemizleDiyalog({ keys, onKapat }: { /** kapsam: görünen listenin ders anahtarları */ keys: string[]; onKapat: () => void }) {
  const takip = useTakip();
  const konumSurum = useCdKonumSurum();
  const konumN = useMemo(() => { const s = new Set(cdKonumListesi().map((k) => k.key)); return keys.filter((k) => s.has(k)).length; }, [keys, konumSurum]);
  const takipKeys = useMemo(() => keys.filter((k) => takip.k[`sesli:${sesliKonuId(k)}`]), [keys, takip]);
  const bittiN = takipKeys.filter((k) => bittiMi(takip.k[`sesli:${sesliKonuId(k)}`])).length;
  const [secKonum, setSecKonum] = useState(true);
  const [secTakip, setSecTakip] = useState(false);
  const [sonuc, setSonuc] = useState<string | null>(null);
  const kapatRef = React.useRef<HTMLButtonElement>(null);
  useEffect(() => {
    kapatRef.current?.focus();
    const f = (e: KeyboardEvent) => { if (e.key === 'Escape') onKapat(); };
    document.addEventListener('keydown', f);
    return () => document.removeEventListener('keydown', f);
  }, [onKapat]);
  const temizle = () => {
    const parca: string[] = [];
    if (secKonum) { const n = cdKonumlariTemizle(keys); parca.push(`${n} kaldığın yer kaydı`); }
    if (secTakip) { const n = modulSifirla('sesli', takipKeys); parca.push(`${n} dersin süre/bitti kaydı`); }
    setSonuc(parca.length ? `Silindi: ${parca.join(', ')}. Derslere istediğin yerden yeniden başlayabilirsin.` : 'Seçim yapılmadı.');
  };
  const hicYok = !secKonum && !secTakip;
  return (
    <div className="cd-dlg" role="presentation" onClick={(e) => { if (e.target === e.currentTarget) onKapat(); }}>
      <div className="cd-dlg-kart" role="dialog" aria-modal="true" aria-labelledby="cd-tmz-b">
        <header className="cd-dlg-bas">
          <b id="cd-tmz-b" className="cd-dlg-baslik"><Eraser aria-hidden /> Sesli ders ilerlemesini temizle</b>
          <button ref={kapatRef} type="button" className="cd-btn is-ikon" onClick={onKapat} aria-label="Kapat"><X aria-hidden /></button>
        </header>
        <div className="cd-dlg-govde cdl-temizle-govde">
          {sonuc ? (
            <>
              <p className="cdl-temizle-sonuc" role="status"><Check aria-hidden /> {sonuc}</p>
              <div className="cdl-temizle-eylem"><button type="button" className="cd-btn" onClick={onKapat}>Tamam</button></div>
            </>
          ) : (
            <>
              <p className="cdl-temizle-aciklama">Yalnız bu cihazdaki yerel kayıtlar silinir; ders sesleri, indirilenler ve listen durur. Hangi kayıtların silineceğini seç:</p>
              <label className="cdl-temizle-sec">
                <input type="checkbox" checked={secKonum} onChange={(e) => setSecKonum(e.target.checked)} disabled={!konumN} />
                <span><b>Kaldığın yer kayıtları</b><small>{konumN ? `${konumN} yarım kalan ders başa alınır; "Yarım kalanlar" boşalır.` : 'Yarım kalan ders yok.'}</small></span>
              </label>
              <label className="cdl-temizle-sec">
                <input type="checkbox" checked={secTakip} onChange={(e) => setSecTakip(e.target.checked)} disabled={!takipKeys.length} />
                <span><b>Bitti işaretleri ve dinleme süreleri</b><small>{takipKeys.length ? `${takipKeys.length} dersin kaydı (${bittiN} bitti işareti) silinir; Bitirdiklerim ve branş çubukları sıfırlanır.` : 'Kayıtlı ders yok.'}</small></span>
              </label>
              <div className="cdl-temizle-eylem">
                <button type="button" className="cd-btn" onClick={onKapat}>Vazgeç</button>
                <button type="button" className="cd-btn is-tehlike" onClick={temizle} disabled={hicYok}><Eraser aria-hidden /> <span>Temizle</span></button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

