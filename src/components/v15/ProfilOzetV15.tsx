import React, { useMemo } from 'react';
import { sureYaz, useTakip } from '../../services/calismaTakip';
import { getActivity } from '../../services/activityLog';
import { useBasarim } from '../../services/basarimIstemci';

/**
 * v15 · Profil özeti (tasarım G04 profil): Seri gün · Çözülen soru · Biten konu · Rozet ve haftalık etkinlik çubukları.
 * Veri: çalışma takibi (gün gün süre, biten konular), etkinlik günlüğü (çözülen/yanlış), başarım durumu (açılan seviyeler).
 */
const GUN = 86_400_000;
const anahtar = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const GADI = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'];

export default function ProfilOzetV15() {
  const takip = useTakip();
  const { durum } = useBasarim();
  const v = useMemo(() => {
    const gunluk: Record<string, number> = {};
    for (const g of Object.values(takip.g)) for (const [d, sn] of Object.entries(g || {})) gunluk[d] = (gunluk[d] || 0) + sn;
    const simdi = new Date();
    let seri = 0;
    for (let i = 0; i < 365; i++) { const sn = gunluk[anahtar(new Date(simdi.getTime() - i * GUN))] || 0; if (sn >= 600) seri++; else if (i > 0) break; }
    const soru = getActivity().filter((e) => e.kind === 'coz' || e.kind === 'yanlis').length;
    const biten = Object.values(takip.k).filter((k) => k.durum === 'bitti').length;
    const pzt = new Date(simdi); pzt.setDate(pzt.getDate() - ((pzt.getDay() + 6) % 7));
    const hafta = Array.from({ length: 7 }, (_, i) => { const t = new Date(pzt.getTime() + i * GUN); return { t, sn: gunluk[anahtar(t)] || 0, bugun: anahtar(t) === anahtar(simdi) }; });
    return { seri, soru, biten, hafta, enCok: Math.max(1, ...hafta.map((h) => h.sn)), toplam: hafta.reduce((a, h) => a + h.sn, 0) };
  }, [takip]);
  const rozet = (durum?.basarimlar || []).reduce((a, b) => a + (b.alinan || 0), 0);
  return (
    <section className="pf15-oz" aria-label="Özet">
      <div className="pf15-oz-stat">
        <div className="v15-card"><b>{v.seri}</b><small>Seri gün</small></div>
        <div className="v15-card"><b>{v.soru.toLocaleString('tr-TR')}</b><small>Soru</small></div>
        <div className="v15-card"><b>{v.biten}</b><small>Biten konu</small></div>
        <div className="v15-card"><b>{rozet}</b><small>Rozet</small></div>
      </div>
      <div className="v15-card pf15-oz-hafta">
        <div className="pf15-oz-bas"><b>Haftalık etkinlik</b><small>{v.toplam ? sureYaz(v.toplam) : 'bu hafta çalışma yok'}</small></div>
        <div className="pf15-oz-cubuk" role="img" aria-label={`Bu hafta ${sureYaz(v.toplam)} çalışma`}>
          {v.hafta.map((h, i) => <span key={i} className={h.bugun ? 'is-on' : ''} title={`${GADI[i]}: ${h.sn ? sureYaz(h.sn) : 'çalışma yok'}`}><i style={{ height: h.sn ? `max(4px, ${(h.sn / v.enCok) * 100}%)` : 0 }} /><small>{GADI[i]}</small></span>)}
        </div>
      </div>
    </section>
  );
}
