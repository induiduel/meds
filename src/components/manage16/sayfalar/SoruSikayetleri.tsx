import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, adminIstek, bildir, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';

/** Sorular › Şikâyetler — soru hata bildirimleri (çıkmış + havuz + örnek). Sohbet/mesaj şikâyetleri Topluluk › Şikâyetler'de. */
type Satir = { id: string; raporId: string; kaynak: 'cikmis' | 'havuz' | 'ornek'; soruId: string; ders: string; kurul: string; neden: string; ayrinti: string; kim: string; at: string; durum: string; kok: string };
const KAYNAK: Record<string, string> = { cikmis: 'Çıkmış', havuz: 'Havuz', ornek: 'Örnek soru' };
const SAYFA: Record<string, string> = { cikmis: 'sorular/cikmis', havuz: 'sorular/havuz', ornek: 'sorular/ornek' };

export default function SoruSikayetleri({ git }: SayfaProps) {
  const coz = async (s: Satir, durum: 'resolved' | 'pending') => {
    try { await adminIstek('/api/admin/sorular/sikayet/coz', { yontem: 'POST', govde: { kaynak: s.kaynak, soruId: s.soruId, raporId: s.raporId, durum } }); bildir(durum === 'resolved' ? 'Çözüldü olarak işaretlendi' : 'Yeniden açıldı', 'iyi'); }
    catch (e: any) { bildir(e.message, 'kotu'); }
  };
  return (
    <>
      <SayfaBasligi baslik="Soru şikâyetleri" aciklama="Öğrencilerin soru hata bildirimleri. Soruyu açıp düzeltin, sonra bildirimi çözüldü işaretleyin." />
      <VeriTablosu<Satir>
        kimlik="sorular-sikayet" kaynak="/api/admin/sorular/sikayet" canliOlay={['reports_changed', 'past_question_updated', 'past_questions_changed']}
        aramaYeri="Neden, ayrıntı, soru ya da kişi ara…" satirKimligi={(s) => s.id}
        suzgecler={[
          { anahtar: 'durum', etiket: 'Durum', secenekler: [{ deger: 'acik', etiket: 'Açık' }, { deger: 'cozuldu', etiket: 'Çözüldü' }, { deger: 'hepsi', etiket: 'Hepsi' }] },
          { anahtar: 'kaynak', etiket: 'Kaynak', secenekler: Object.entries(KAYNAK).map(([deger, etiket]) => ({ deger, etiket })) },
        ]}
        sutunlar={[
          { anahtar: 'at', baslik: 'Zaman', sirala: true, genislik: '100px', hucre: (s) => (s.at ? zamanMetni(s.at) : '—') },
          { anahtar: 'kaynak', baslik: 'Kaynak', genislik: '96px', hucre: (s) => <Rozet ton="bilgi">{KAYNAK[s.kaynak]}</Rozet> },
          { anahtar: 'neden', baslik: 'Bildirim', genislik: 'minmax(220px,2fr)', hucre: (s) => <span title={s.ayrinti}><b>{s.neden}</b>{s.ayrinti && ` — ${s.ayrinti}`}</span> },
          { anahtar: 'kok', baslik: 'Soru', genislik: 'minmax(160px,1.5fr)', hucre: (s) => <a href={`/manage/${SAYFA[s.kaynak]}/${encodeURIComponent(s.soruId)}`} onClick={(e) => { e.preventDefault(); git(`${SAYFA[s.kaynak]}/${encodeURIComponent(s.soruId)}`); }}>{s.kok || s.soruId}</a> },
          { anahtar: 'kim', baslik: 'Kim', genislik: 'minmax(90px,0.8fr)', gizli: true },
          { anahtar: 'durum', baslik: 'İşlem', genislik: '130px', hucre: (s) => (s.durum === 'acik'
            ? <button type="button" className="m16-btn" onClick={(e) => { e.stopPropagation(); void coz(s, 'resolved'); }}>Çözüldü</button>
            : <button type="button" className="m16-btn hayalet" onClick={(e) => { e.stopPropagation(); void coz(s, 'pending'); }}>Yeniden aç</button>) },
        ]}
      />
    </>
  );
}
