/**
 * Canlı ders · video işi deposu: üretim pencereden bağımsız sürer (pencere kapanır, başka sayfaya geçilir, sekme
 * arka plana alınır). Tek seferde tek iş. Ağır motor (cdVideo.ts) yalnız iş başlarken yüklenir.
 * Arka plan: Web Lock tutulur (Chrome gizli sekmeyi dondurmaz/atmaz), sayfadan çıkışta uyarı, sekme başlığında yüzde.
 */
import { toast } from '../ui/Toast';
import type { CdDetay, CdVaryant } from './canliDersStore';
import type { CdVideoCozunurluk, CdVideoIlerleme } from './cdVideo';

export interface CdVideoIs {
  dersKey: string;
  baslik: string;
  ad: string;
  ilerleme: CdVideoIlerleme;
}

let is: CdVideoIs | null = null;
let iptalci: AbortController | null = null;
const dinleyiciler = new Set<() => void>();
const yay = () => dinleyiciler.forEach((f) => f());

export const cdVideoIsAl = () => is;
export function cdVideoIsDinle(f: () => void) { dinleyiciler.add(f); return () => { dinleyiciler.delete(f); }; }
export function cdVideoIptal() { iptalci?.abort(); }

const cikisUyar = (e: BeforeUnloadEvent) => { e.preventDefault(); e.returnValue = ''; };
const ON = /^🎬 (%\d+ · )?/;
function baslikYaz() {
  if (!is) return;
  const p = is.ilerleme;
  const on = p.asama === 'kodlama' ? `🎬 %${Math.floor(p.oran * 100)} · ` : '🎬 ';
  document.title = on + document.title.replace(ON, '');
}

export async function cdVideoIsBaslat(o: {
  detay: CdDetay; varyant: CdVaryant; cozunurluk: CdVideoCozunurluk; etiket: string; ad: string; dosya?: FileSystemWritableFileStream;
}): Promise<'tamam' | 'iptal' | string> {
  if (is) return 'Zaten bir video oluşturuluyor.';
  const ac = new AbortController();
  iptalci = ac;
  is = { dersKey: o.detay.key, baslik: o.detay.baslik, ad: o.ad, ilerleme: { asama: 'hazirlik', oran: 0, t: 0, sure: 0 } };
  window.addEventListener('beforeunload', cikisUyar);
  yay();
  let bitir: () => void = () => undefined;
  const kilit = new Promise<void>((r) => { bitir = r; });
  // Web Lock tutan sayfa Chrome'da arka planda dondurulmaz
  try { (navigator as any).locks?.request?.('medsor-video', () => kilit).catch(() => undefined); } catch { /* */ }
  let sonBaslik = 0;
  try {
    const m = await import('./cdVideo');
    const blob = await m.cdVideoOlustur({
      detay: o.detay, varyant: o.varyant, cozunurluk: o.cozunurluk, etiket: o.etiket, dosya: o.dosya, sinyal: ac.signal,
      onIlerleme: (p) => {
        if (!is) return;
        is = { ...is, ilerleme: p };
        yay();
        const simdi = performance.now();
        if (simdi - sonBaslik > 1000) { sonBaslik = simdi; baslikYaz(); }
      },
    });
    if (blob) {
      const u = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = u; a.download = o.ad; a.click();
      setTimeout(() => URL.revokeObjectURL(u), 60_000);
    }
    toast.success('Video hazır', o.ad);
    return 'tamam';
  } catch (e: any) {
    if (e?.name === 'AbortError') { try { await o.dosya?.abort(); } catch { /* */ } return 'iptal'; }
    console.error('video', e);
    const msg = e?.message || 'Video oluşturulamadı.';
    toast.error('Video oluşturulamadı', msg);
    return msg;
  } finally {
    bitir();
    window.removeEventListener('beforeunload', cikisUyar);
    document.title = document.title.replace(ON, '');
    is = null; iptalci = null;
    yay();
  }
}
