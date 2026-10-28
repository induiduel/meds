// H303: "Tümünü gör" birleşik Çevrimdışı ve indirmeler sayfasının iş listesine gider
import { useEffect, useRef, useState } from 'react';
import { Clapperboard, Download, Loader2, RefreshCw } from 'lucide-react';
import { useArkaPlanOzet } from '../../services/arkaPlanIsleri';
import { navigateTo, pathFor } from '../../router';

/**
 * v15 üst bar › arka plan göstergesi (tasarım AB02): indirme, video ya da çevrimdışıyken bekleyen eşitleme varsa dönen simge
 * + iş sayısı; dokununca kısa liste ve "Tümünü gör" (/arka-plan). İş yokken hiç çizilmez.
 */
export default function ArkaPlanGosterge() {
  const { s, video, kv, kuyruk, esitleme, toplam } = useArkaPlanOzet();
  const [acik, setAcik] = useState(false);
  const kok = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!acik) return;
    const d = (e: Event) => { if (!kok.current?.contains(e.target as Node)) setAcik(false); };
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') setAcik(false); };
    document.addEventListener('pointerdown', d); document.addEventListener('keydown', k);
    return () => { document.removeEventListener('pointerdown', d); document.removeEventListener('keydown', k); };
  }, [acik]);
  if (!toplam) return null;
  const a = s.aktif;
  const ad = (id: string) => s.katalog.find((p) => p.id === id)?.baslik || s.kayitlar[id]?.baslik || id;
  const sira = s.kuyruk.filter((id) => id !== a?.id).length;
  return (
    <div className="ap15g" ref={kok}>
      <button type="button" className="v15-ib ap15g-b" onClick={() => setAcik((v) => !v)} aria-haspopup="menu" aria-expanded={acik} aria-label={`Arka planda ${toplam} iş`} title="Arka plan işleri">
        <Loader2 className="ap15g-spin" aria-hidden />
        <b aria-hidden>{toplam}</b>
      </button>
      {acik && (
        <div className="ap15g-m v15-card" role="menu">
          <p className="v15-label">Arka planda {toplam} iş</p>
          {a && (
            <button type="button" role="menuitem" onClick={() => { setAcik(false); navigateTo(`${pathFor('cevrimdisi')}#isler`); }}>
              <Download aria-hidden /><span>{ad(a.id)} {a.bekliyor ? '· bekliyor' : a.toplam ? `%${Math.round((a.alinan / a.toplam) * 100)}` : ''}</span>
            </button>
          )}
          {sira > 0 && <button type="button" role="menuitem" onClick={() => { setAcik(false); navigateTo(`${pathFor('cevrimdisi')}#isler`); }}><Download aria-hidden /><span>{sira} paket sırada</span></button>}
          {video && <button type="button" role="menuitem" onClick={() => { setAcik(false); navigateTo(`${pathFor('cevrimdisi')}#isler`); }}><Clapperboard aria-hidden /><span>Video %{Math.floor(video.ilerleme.oran * 100)}</span></button>}
          {esitleme && <button type="button" role="menuitem" onClick={() => { setAcik(false); navigateTo(`${pathFor('cevrimdisi')}#isler`); }}><RefreshCw aria-hidden /><span>Eşitleme bekliyor · {kv + kuyruk} kayıt</span></button>}
          <button type="button" role="menuitem" className="ap15g-all" onClick={() => { setAcik(false); navigateTo(`${pathFor('cevrimdisi')}#isler`); }}>Tümünü gör</button>
        </div>
      )}
    </div>
  );
}
