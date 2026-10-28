import React, { useMemo, useState } from 'react';
import { createPortal } from 'react-dom';
import { Check, ChevronLeft, IdCard, Plus, Search } from 'lucide-react';
import { HEDEFLER, profilOku, profilYaz, UNIVERSITELER, type Profil } from '../../services/profilKurulum';
import { aktifKurul, KURULLAR } from '../../services/kurulTakvimi';
import { kurulKaydet } from '../kurul/KurulSecici';
import { SAVED_STUDENT_NUMBER_KEY } from '../../services/auth';
import '../../styles/v15/kurulum.css';
import { useTamKatman } from '../../utils/tamKatman';

/**
 * v15 · Kayıt adımları (tasarım I07 kayitUni · I08 kayitSinif · I09 kayitKurul · I10 kayitHedef · I11 kayitBitti).
 * Girişten sonra profili eksik öğrenciye bir kez açılır (App, hesaptan eşitleme için kısa gecikmeyle); Profil ›
 * "Bilgilerimi düzenle" ile yeniden açılır. "Sonra" profili tamamlanmış saymaz ama bu oturumda yeniden sormaz.
 * Kurul seçimi sitenin kurul seçicisine (kurulKaydet), hedef Bugün planına yazılır.
 */
const fold = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');
const EGITIM_YILLARI = ['2025–26', '2026–27'];
const ADIM = 4;

export default function ProfilKurulumV15({ onKapat }: { onKapat: () => void }) {
  const ilk = profilOku();
  const [adim, setAdim] = useState(0);
  const [p, setP] = useState<Profil>(() => ({
    egitimYili: '2026–27',
    kurul: aktifKurul().kurul,
    hedef: HEDEFLER[1],
    hatirlatma: '20:00',
    numara: (() => { try { return localStorage.getItem(SAVED_STUDENT_NUMBER_KEY) || ''; } catch { return ''; } })(),
    sinif: 3,
    fakulte: 'Tıp Fakültesi',
    ...ilk,
  }));
  const [ara, setAra] = useState(ilk.universite || '');
  const [elle, setElle] = useState(false);
  const ay = (k: Partial<Profil>) => setP((x) => ({ ...x, ...k }));
  const uniler = useMemo(() => {
    const f = fold(ara.trim());
    return (f ? UNIVERSITELER.filter((u) => fold(u).includes(f)) : UNIVERSITELER).slice(0, 8);
  }, [ara]);

  // tam ekran akış açıkken alt sekme çubuğu gizlenir (telefonda görünür alanın altında kalıp üstte görünüyordu)
  useTamKatman();
  const gecerli = adim === 0 ? !!p.universite : adim === 1 ? !!p.sinif : true;
  const bitir = () => {
    const son: Profil = { ...p, numara: p.numara?.trim() || undefined, tamam: new Date().toISOString() };
    profilYaz(son);
    if (son.kurul) kurulKaydet(son.kurul);
    if (son.numara) { try { localStorage.setItem(SAVED_STUDENT_NUMBER_KEY, son.numara); } catch { /* yok */ } }
    setAdim(ADIM);
  };
  const devam = () => (adim === ADIM - 1 ? bitir() : setAdim((a) => a + 1));

  if (adim === ADIM) {
    return createPortal(
      <div className="kr15k" role="dialog" aria-modal="true" aria-label="Kayıt tamamlandı">
        <div className="kr15k-bitti">
          <svg viewBox="0 0 120 120" className="kr15k-hucre" aria-hidden>
            <circle cx="60" cy="60" r="44" className="kr15k-zar" />
            <circle cx="52" cy="56" r="7" className="kr15k-rna" />
            <circle cx="72" cy="70" r="3" className="kr15k-ribo" />
            <circle cx="66" cy="46" r="2.5" className="kr15k-ribo" />
          </svg>
          <h2>Hücren doğdu</h2>
          <p>Seviye 1 · Protohücre. Çalıştıkça glukoz, başardıkça DNA kazanırsın; hücren evrimleşir.</p>
          <button type="button" className="v15-btn kr15k-ana" onClick={onKapat}>Başla</button>
        </div>
      </div>,
      document.body,
    );
  }

  return createPortal(
    <div className="kr15k" role="dialog" aria-modal="true" aria-labelledby="kr15k-b">
      <header className="kr15k-ust">
        <button type="button" className="v15-ib" onClick={() => (adim ? setAdim(adim - 1) : onKapat())} aria-label={adim ? 'Geri' : 'Sonra'}><ChevronLeft aria-hidden /></button>
        <div className="kr15k-seg" aria-hidden>{Array.from({ length: ADIM }, (_, i) => <i key={i} className={i <= adim ? 'is-on' : ''} />)}</div>
        <span className="kr15k-no">{adim + 1}/{ADIM}</span>
      </header>
      <div className="kr15k-ic">
        {adim === 0 && (
          <>
            <h2 id="kr15k-b">Hangi üniversitedesin?</h2>
            <label className="kr15k-inp"><Search aria-hidden />
              <input value={ara} onChange={(e) => { setAra(e.target.value); setElle(false); }} placeholder="Üniversite ara" aria-label="Üniversite ara" />
            </label>
            {!elle ? (
              <>
                <ul className="v15-card kr15k-liste" role="radiogroup" aria-label="Üniversite">
                  {uniler.map((u) => (
                    <li key={u}>
                      <button type="button" role="radio" aria-checked={p.universite === u} onClick={() => ay({ universite: u })}>
                        <span className={`kr15k-radio${p.universite === u ? ' is-on' : ''}`} />
                        <span><b>{u}</b><small>{p.universite === u ? p.fakulte : 'Tıp Fakültesi'}</small></span>
                      </button>
                    </li>
                  ))}
                  {!uniler.length && <li className="kr15k-yok">Listede bulunamadı.</li>}
                </ul>
                <button type="button" className="kr15k-link" onClick={() => { setElle(true); ay({ universite: ara.trim() || undefined }); }}><Plus aria-hidden /> Listede yok mu? Elle ekle</button>
              </>
            ) : (
              <div className="kr15k-elle">
                <label><span>Üniversite</span><input value={p.universite || ''} onChange={(e) => ay({ universite: e.target.value.slice(0, 80) || undefined })} placeholder="Üniversitenin adı" /></label>
                <label><span>Fakülte</span><input value={p.fakulte || ''} onChange={(e) => ay({ fakulte: e.target.value.slice(0, 60) })} placeholder="Tıp Fakültesi" /></label>
              </div>
            )}
          </>
        )}
        {adim === 1 && (
          <>
            <h2 id="kr15k-b">Kaçıncı sınıftasın?</h2>
            <div className="kr15k-sinif" role="radiogroup" aria-label="Sınıf">
              {[1, 2, 3, 4, 5, 6].map((n) => (
                <button key={n} type="button" role="radio" aria-checked={p.sinif === n} className={`v15-btn ${p.sinif === n ? '' : 'is-soft'}`} onClick={() => ay({ sinif: n })}>{n}. sınıf</button>
              ))}
            </div>
            <span className="kr15k-lbl">Öğrenci numarası (isteğe bağlı)</span>
            <label className="kr15k-inp"><IdCard aria-hidden />
              <input inputMode="numeric" value={p.numara || ''} onChange={(e) => ay({ numara: e.target.value.replace(/[^\d ]/g, '').slice(0, 16) })} placeholder="Öğrenci numaran" aria-label="Öğrenci numarası" />
            </label>
            <p className="kr15k-not">Sınıf sıralamasında görünmek ve katkılarını hesabına bağlamak için kullanılır; başkalarına gösterilmez.</p>
          </>
        )}
        {adim === 2 && (
          <>
            <h2 id="kr15k-b">Bu dönem neredesin?</h2>
            <span className="kr15k-lbl">Eğitim yılı</span>
            <div className="v15-seg" role="radiogroup" aria-label="Eğitim yılı">
              {EGITIM_YILLARI.map((y) => <button key={y} type="button" role="radio" aria-checked={p.egitimYili === y} aria-current={p.egitimYili === y ? 'page' : undefined} onClick={() => ay({ egitimYili: y })}>{y}</button>)}
            </div>
            <span className="kr15k-lbl">Aktif kurul</span>
            <ul className="v15-card kr15k-liste" role="radiogroup" aria-label="Aktif kurul">
              {KURULLAR.map((k) => (
                <li key={k.kurul}>
                  <button type="button" role="radio" aria-checked={p.kurul === k.kurul} onClick={() => ay({ kurul: k.kurul })}>
                    <span className={`kr15k-radio${p.kurul === k.kurul ? ' is-on' : ''}`} />
                    <span><b>Kurul {k.kurul}</b><small>{k.ad}</small></span>
                    {k.kurul === aktifKurul().kurul && <span className="v15-tag is-a">Takvime göre</span>}
                  </button>
                </li>
              ))}
            </ul>
          </>
        )}
        {adim === 3 && (
          <>
            <h2 id="kr15k-b">Günlük hedefin</h2>
            <p className="kr15k-not">Bugün sayfasındaki plan bu hedefe göre ilerler; hücren hedefini tutturdukça glukoz kazanır.</p>
            <div className="kr15k-hedef" role="radiogroup" aria-label="Günlük hedef">
              {HEDEFLER.map((h) => (
                <button key={h.ad} type="button" role="radio" aria-checked={p.hedef?.ad === h.ad} className={p.hedef?.ad === h.ad ? 'is-on' : ''} onClick={() => ay({ hedef: h })}>
                  <span><b>{h.ad}</b><small>{h.dk} dk · {h.soru} soru</small></span>
                  {p.hedef?.ad === h.ad && <Check aria-hidden />}
                </button>
              ))}
            </div>
            <label className="kr15k-saat"><span>Hatırlatma saati</span>
              <input type="time" value={p.hatirlatma || ''} onChange={(e) => ay({ hatirlatma: e.target.value })} aria-label="Hatırlatma saati" />
            </label>
          </>
        )}
      </div>
      <footer className="kr15k-alt">
        <button type="button" className="v15-btn kr15k-ana" onClick={devam} disabled={!gecerli}>{adim === ADIM - 1 ? 'Bitir' : 'Devam'}</button>
        {adim === 0 && !ilk.tamam && <button type="button" className="kr15k-link" onClick={onKapat}>Sonra</button>}
      </footer>
    </div>,
    document.body,
  );
}

/** Uygulama kökünde: girişli, profili eksik öğrenciye bir kez açar; `medsoru:profil-kur` olayı her zaman açar. */
export function ProfilKurulumKapisi({ girisli, yonetici }: { girisli: boolean; yonetici: boolean }) {
  const [acik, setAcik] = useState(false);
  React.useEffect(() => {
    const ac = () => setAcik(true);
    window.addEventListener('medsoru:profil-kur', ac);
    return () => window.removeEventListener('medsoru:profil-kur', ac);
  }, []);
  React.useEffect(() => {
    if (!girisli || yonetici) return;
    // hesaptan eşitleme gelsin diye bekle; başka cihazda doldurulmuş profil yeniden sorulmaz
    const t = window.setTimeout(() => {
      let sonra = false;
      try { sonra = !!sessionStorage.getItem('medsoru_profil_sonra'); } catch { /* yok */ }
      if (!profilOku().tamam && !sonra) setAcik(true);
    }, 5000);
    return () => window.clearTimeout(t);
  }, [girisli, yonetici]);
  if (!acik) return null;
  return <ProfilKurulumV15 onKapat={() => { try { sessionStorage.setItem('medsoru_profil_sonra', '1'); } catch { /* yok */ } setAcik(false); }} />;
}
export const profilKurulumAc = () => window.dispatchEvent(new Event('medsoru:profil-kur'));
