/** Sesli ders molası: ~15–20 dk dinlemeden sonra ders durur, kutlama animasyonu ve kısa bir teşvik sözüyle mola önerilir. */
import React, { useEffect, useState } from 'react';
import { Play, Coffee, SkipForward, Check } from 'lucide-react';
import { useCd } from './canliDersStore';
import { Dialog } from '../ui/Dialog';
import { Lottie } from '../ui/Lottie';
import { cdMolaKapat, useCdMola, type MolaAnim } from './canliDersMotivasyon';

const BASLIK: Record<MolaAnim, string> = {
  zirve: 'Adım adım zirveye',
  calisma: 'Emeğin ışığa dönüşüyor',
  sevgi: 'Sevgiyle, güçle',
  gunes: 'Zor günler geçer',
  kutlama: 'Harika gidiyorsun',
};

export default function CanliDersMola() {
  const m = useCdMola();
  const simdiki = useCd((s) => s.key);
  const bitis = m.tip === 'bitis';
  // Ders sonunda pekiştirme penceresi açılacaksa (öneri eşzamansız bulunur) kısa süre beklenir; açılırsa bu pencere çıkmaz
  const [hazir, setHazir] = useState(false);
  useEffect(() => {
    setHazir(false);
    if (!m.acik || !bitis) return;
    const t = window.setTimeout(() => setHazir(true), 700);
    return () => window.clearTimeout(t);
  }, [m.acik, bitis, m.key]);
  if (!m.acik || (bitis && (m.birlesik || !hazir))) return null;
  // Oynatma listesi sonraki dersi yüklediyse pencereden ona geçilir
  const sonraki = bitis && !!simdiki && simdiki !== m.key;
  return (
    <Dialog
      title={bitis ? 'Ders bitti, tebrikler!' : 'Mola zamanı'}
      subtitle={bitis ? m.baslik : m.dk > 0 ? `${m.dk} dakikadır kesintisiz dinliyorsun` : undefined}
      width="max-w-sm"
      onClose={() => cdMolaKapat(false)}
      footer={
        <div className="cd-mola-eylem">
          {bitis ? <>
            <button type="button" className={`cd-btn${sonraki ? '' : ' is-ana'}`} onClick={() => cdMolaKapat(false)}>{sonraki ? <Coffee aria-hidden /> : <Check aria-hidden />}<span>{sonraki ? 'Biraz dinleneyim' : 'Tamam'}</span></button>
            {sonraki && <button type="button" className="cd-btn is-ana" onClick={() => cdMolaKapat(true)}><SkipForward aria-hidden /><span>Sonraki derse geç</span></button>}
          </> : <>
            <button type="button" className="cd-btn" onClick={() => cdMolaKapat(false)}><Coffee aria-hidden /><span>Mola veriyorum</span></button>
            <button type="button" className="cd-btn is-ana" onClick={() => cdMolaKapat(true)}><Play aria-hidden /><span>Devam et</span></button>
          </>}
        </div>
      }
    >
      <div className="cd-mola">
        <Lottie key={m.anim} name={m.anim} className="cd-mola-anim" />
        <b className="cd-mola-baslik">{BASLIK[m.anim]}</b>
        <p className="cd-mola-metin">{m.metin}</p>
        {!bitis && <p className="cd-mola-not">Kaldığın paragraf işaretlendi; devam ettiğinde oradan başlar.</p>}
      </div>
    </Dialog>
  );
}
