/** Sesli ders molası: ~15–20 dk dinlemeden sonra ders durur, kutlama animasyonu ve kısa bir teşvik sözüyle mola önerilir. */
import React from 'react';
import { Play, Coffee } from 'lucide-react';
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
  if (!m.acik) return null;
  return (
    <Dialog
      title="Mola zamanı"
      subtitle={m.dk > 0 ? `${m.dk} dakikadır kesintisiz dinliyorsun` : undefined}
      width="max-w-sm"
      onClose={() => cdMolaKapat(false)}
      footer={
        <div className="cd-mola-eylem">
          <button type="button" className="cd-btn" onClick={() => cdMolaKapat(false)}><Coffee aria-hidden /><span>Mola veriyorum</span></button>
          <button type="button" className="cd-btn is-ana" onClick={() => cdMolaKapat(true)}><Play aria-hidden /><span>Devam et</span></button>
        </div>
      }
    >
      <div className="cd-mola">
        <Lottie key={m.anim} name={m.anim} className="cd-mola-anim" />
        <b className="cd-mola-baslik">{BASLIK[m.anim]}</b>
        <p className="cd-mola-metin">{m.metin}</p>
        <p className="cd-mola-not">Kaldığın paragraf işaretlendi; devam ettiğinde oradan başlar.</p>
      </div>
    </Dialog>
  );
}
