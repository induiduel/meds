import { useEffect, useMemo, useState } from 'react';
import { CalendarClock } from 'lucide-react';
import { linkClick, navigateTo, pathFor } from '../../router';
import { aktifKurul, bugun } from '../../services/kurulTakvimi';
import { programYukle, saatBas, saatBitis, type ProgDers } from '../../services/programVeri';
import { useKisiselProgram } from '../../services/kisiselProgram';
import { saatYaz, useBolge } from '../../services/bolgeTercih';
import '../../styles/v15/kisisel.css';

/**
 * Bugün › ders programı kartı (tasarım AA07 dpWidget): şu an süren ders (kalan dakika) ve sıradaki ders.
 * Kaynak: aktif kurulun ders kayıt defteri (programVeri) + öğrencinin kişisel etkinlikleri. Bugün ders yoksa kart çizilmez.
 */
const dk = (hhmm: string) => { const [h, m] = hhmm.split(':').map(Number); return h * 60 + (m || 0); };
interface Satir { ad: string; alt: string; bas: string; bit: string }

export default function ProgramSimdiKarti() {
  const g = bugun();
  const kurul = aktifKurul(g);
  const kisisel = useKisiselProgram();
  const bolge = useBolge();
  const [dersler, setDersler] = useState<ProgDers[] | null>(null);
  const [simdi, setSimdi] = useState(() => new Date());
  useEffect(() => {
    let c = true;
    programYukle(kurul.kurul).then((d) => c && setDersler(d.filter((x) => x.tarih === g)), () => c && setDersler([]));
    return () => { c = false; };
  }, [kurul.kurul, g]);
  useEffect(() => { const t = window.setInterval(() => setSimdi(new Date()), 30_000); return () => window.clearInterval(t); }, []);

  const satirlar = useMemo<Satir[]>(() => {
    const l: Satir[] = (dersler || []).filter((d) => d.saat).map((d) => ({ ad: d.konu, alt: d.brans, bas: saatBas(d.saat), bit: saatBitis(d) }));
    for (const e of kisisel) if (e.tarih === g) l.push({ ad: e.baslik, alt: e.yer ? `Kişisel · ${e.yer}` : 'Kişisel', bas: e.bas, bit: e.bit });
    return l.sort((a, b) => a.bas.localeCompare(b.bas));
  }, [dersler, kisisel, g]);

  if (!satirlar.length) return null;
  const n = simdi.getHours() * 60 + simdi.getMinutes();
  const suren = satirlar.find((s) => dk(s.bas) <= n && n < dk(s.bit));
  const sonraki = satirlar.find((s) => dk(s.bas) > n);
  const ana = suren || sonraki;
  const href = pathFor('ders_programi');
  if (!ana) {
    return (
      <a className="t15-pg v15-card" href={href} onClick={linkClick(() => navigateTo(href))}>
        <span className="v15-tile is-n"><CalendarClock aria-hidden /></span>
        <span className="t15-pg-t"><span className="v15-cap">Ders programı</span><b>Bugünkü {satirlar.length} ders bitti</b></span>
      </a>
    );
  }
  const ust = suren ? `Şimdi · ${dk(suren.bit) - n} dk kaldı` : `Sıradaki · ${saatYaz(ana.bas, bolge)}${dk(ana.bas) - n <= 90 ? ` (${dk(ana.bas) - n} dk sonra)` : ''}`;
  const ikinci = suren ? sonraki : satirlar.find((s) => s !== ana && dk(s.bas) > dk(ana.bas));
  return (
    <a className="t15-pg v15-card" href={href} onClick={linkClick(() => navigateTo(href))} aria-label={`Ders programı: ${ust}, ${ana.ad}`}>
      <span className={`v15-tile ${suren ? 'is-ai' : ''}`}><CalendarClock aria-hidden /></span>
      <span className="t15-pg-t">
        <span className="v15-cap">{ust}</span>
        <b>{ana.ad}</b>
        <small>{ana.alt}</small>
      </span>
      {ikinci && <span className="t15-pg-s v15-cap">Sonra {saatYaz(ikinci.bas, bolge)}<br />{ikinci.ad}</span>}
    </a>
  );
}
