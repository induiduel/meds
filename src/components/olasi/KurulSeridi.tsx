/**
 * Ana ekran kurul şeridi: aktif kurul + sınava kalan gün; sınav günü ve sonraki 7 günde olası sorulara ve
 * soru eklemeye çağrı. Takvim istemcide (services/kurulTakvimi) — ağ isteği yok. Stil: styles/olasi-sorular.css (.ks-*).
 */
import React, { useMemo } from 'react';
import { ArrowRight, CalendarClock, Sparkles, SquarePen } from 'lucide-react';
import { gunluBag, kurulAdi, takvimDurumu } from '../../services/kurulPencere';
import { linkClick, navigateTo } from '../../router';
import '../../styles/olasi-sorular.css';

const Git: React.FC<{ url: string; className?: string; children: React.ReactNode }> = ({ url, className, children }) => {
  const u = gunluBag(url);
  return <a href={u} className={className} onClick={linkClick(() => navigateTo(u))}>{children}</a>;
};

export default function KurulSeridi({ soruEkleGoster = true, sola = false }: { soruEkleGoster?: boolean; sola?: boolean }) {
  const t = useMemo(() => takvimDurumu(), []);
  const p = t.pencere;
  if (p) {
    const ne = p.gecenGun === 0 ? 'sınavı bugün' : p.gecenGun === 1 ? 'sınavı dündü' : `sınavı ${p.gecenGun} gün önceydi`;
    return (
      <aside className={`ks is-sinav${sola ? ' is-sol' : ''}`} aria-label="Sınav sonrası">
        <Sparkles aria-hidden className="ks-i" />
        <p className="ks-m">
          <b>Kurul {p.kurul.kurul} {ne}.</b> Hatırladığın soruları kaçıncı soru olduğuyla ekle; olası sorular her gece bunlardan kurulur.
        </p>
        <span className="ks-d">
          {soruEkleGoster && <Git url="/" className="ks-dug is-ana"><SquarePen aria-hidden /> Soru ekle</Git>}
          <Git url={`/olasi-sorular?kurul=${p.kurul.kurul}`} className="ks-dug">Olası sorular <ArrowRight aria-hidden /></Git>
        </span>
      </aside>
    );
  }
  return (
    <aside className={`ks${sola ? ' is-sol' : ''}`} aria-label="Aktif kurul">
      <CalendarClock aria-hidden className="ks-i" />
      <p className="ks-m">
        <b>Kurul {t.aktif.kurul}</b> <span className="ks-ad">{kurulAdi(t.aktif)}</span>
      </p>
      <span className="ks-kalan">{t.kalan > 0 ? <>Sınava <b>{t.kalan}</b> gün</> : 'Sınav bugün'}</span>
    </aside>
  );
}
