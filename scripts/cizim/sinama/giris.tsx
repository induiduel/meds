// Çizim sınama sayfası (panel_sinama.mjs): her şema/etiket kendi sayfa görüntüsü üstünde, gerçek CizimLayer + pdfDoc.css ile
import { createRoot } from 'react-dom/client';
import { CizimLayer } from '../../../src/components/learn/pdf/CizimLayer';
import '../../../src/components/learn/pdf/pdfDoc.css';

const q = new URLSearchParams(location.search);
const W = Number(q.get('w') ?? 567);
const T = Number(q.get('t') ?? 1);
function Sayfa({ s, x, oran }: { s: string; x: any; oran: number }) {
  const H = W / oran;
  const ek = x.ek_alt || 0;
  return (
    <div className="kart" data-s={s} data-kh={x.kutu_h || ''} style={{ position: 'relative', height: H * (1 + ek) + 16, width: W, margin: '0 auto' }}>
      <div className={`pdv-page${ek ? ' has-ek' : ''}`} style={{ position: 'absolute', left: W / 2, top: 0, width: W, height: H, ['--ek-h' as any]: `${H * ek}px`, ['--ek-renk' as any]: x.ek_renk }}>
        {ek ? <span className="pdv-page-ek" /> : null}
        <img src={`s${s}.png`} style={{ position: 'absolute', inset: 0, width: W, height: H }} />
        <div className="pdv-marks"><CizimLayer z={[x]} useChar={() => x.k[0] + (x.k[1] - x.k[0]) * T} /></div>
      </div>
    </div>
  );
}
fetch('veri.json').then((r) => r.json()).then((v: { oran: Record<string, number>; komut: Record<string, any[]> }) => {
  createRoot(document.getElementById('r')!).render(
    <div>{Object.entries(v.komut).flatMap(([s, z]) => z.map((x, i) => <Sayfa key={s + i} s={s} x={x} oran={v.oran[s] || 4 / 3} />))}</div>,
  );
  (window as any).__hazir = true;
});
