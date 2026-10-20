/** PDF sayfa düzeni seçici: tek yaprakta 1/2/4/8 sayfa, yön, sıra, çerçeve, kenar boşluğu (Metni indir + Toplu PDF ortak). */
import React from 'react';
import type { PdfDuzen, SayfaSayisi } from '../../services/pdfDuzen';
import '../../styles/pdf-duzen.css';

const NUP: SayfaSayisi[] = [1, 2, 4, 8];

/** Küçük ızgara simgesi: seçeneğin yaprak üstündeki yerleşimini gösterir */
function Simge({ n }: { n: SayfaSayisi }) {
  const [kol, sat, yatay] = n === 2 ? [2, 1, true] : n === 4 ? [2, 2, false] : n === 8 ? [4, 2, true] : [1, 1, false];
  return (
    <span className={`pdz-simge${yatay ? ' is-yatay' : ''}`} style={{ gridTemplateColumns: `repeat(${kol}, 1fr)`, gridTemplateRows: `repeat(${sat}, 1fr)` }} aria-hidden>
      {Array.from({ length: n }, (_, i) => <i key={i} />)}
    </span>
  );
}

export function PdfDuzenSecici({ deger, onDegis, ad = 'pdz' }: { deger: PdfDuzen; onDegis: (d: PdfDuzen) => void; ad?: string }) {
  const set = (p: Partial<PdfDuzen>) => onDegis({ ...deger, ...p });
  return (
    <div className="pdz">
      <div className="pdz-nup" role="radiogroup" aria-label="Bir yaprağa kaç sayfa">
        {NUP.map((n) => (
          <label key={n} className={`pdz-nup-ops${deger.nup === n ? ' is-on' : ''}`}>
            <input type="radio" name={`${ad}-nup`} checked={deger.nup === n} onChange={() => set({ nup: n })} />
            <Simge n={n} />
            <span>{n === 1 ? 'Normal' : `${n} sayfa`}</span>
          </label>
        ))}
      </div>
      {deger.nup > 1 && (
        <div className="pdz-ek">
          <label>Yön
            <select value={deger.yon} onChange={(e) => set({ yon: e.target.value as PdfDuzen['yon'] })}>
              <option value="oto">Otomatik</option><option value="dikey">Dikey</option><option value="yatay">Yatay</option>
            </select>
          </label>
          <label>Sıra
            <select value={deger.sira} onChange={(e) => set({ sira: e.target.value as PdfDuzen['sira'] })}>
              <option value="satir">Soldan sağa</option><option value="sutun">Yukarıdan aşağı</option>
            </select>
          </label>
          <label>Boşluk
            <select value={deger.bosluk} onChange={(e) => set({ bosluk: e.target.value as PdfDuzen['bosluk'] })}>
              <option value="normal">Normal</option><option value="dar">Dar</option>
            </select>
          </label>
          <label className="pdz-kutu"><input type="checkbox" checked={deger.cerceve} onChange={(e) => set({ cerceve: e.target.checked })} /> Sayfa çerçevesi</label>
        </div>
      )}
    </div>
  );
}
