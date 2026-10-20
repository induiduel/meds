/**
 * Dışa aktarım için ders PDF'inden slayt başlıklarını okur ("15. Patolojinin Klinik Önemi").
 * Başlık = sayfanın üst kısmındaki, gövde yazısından belirgin büyük punto satır(lar). Paragraf → sayfa eşlemesi mevcut
 * ses–slayt hizalamasından (`detay.pdf.paragraflar`). PDF açılamazsa / süre aşılırsa boş döner: dışa aktarım başlıksız sürer.
 */
import * as pdfjs from 'pdfjs-dist';
import workerUrl from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import { getCustomApiUrl } from '../../services/api';
import { resolveDeckPdf } from '../../services/deckPdfService';
import type { CdDetay } from './canliDersStore';

pdfjs.GlobalWorkerOptions.workerSrc = workerUrl;

/** "dosya:sayfa" → başlık */
export type SlaytBasliklari = Map<string, string>;

const SURE_MS = 25_000;

function sayfaBasligi(items: { str: string; transform: number[]; height: number; width: number }[], sayfaH: number): string {
  const satir = items
    .filter((it) => it.str.trim())
    .map((it) => ({ t: it.str, x: it.transform[4], y: it.transform[5], w: it.width || 0, h: it.height || Math.hypot(it.transform[2], it.transform[3]) }));
  if (satir.length < 2) return '';
  const hs = satir.map((s) => s.h).sort((a, b) => a - b);
  const orta = hs[Math.floor(hs.length / 2)];
  const ust = satir.filter((s) => s.y >= sayfaH * 0.6);
  if (!ust.length) return '';
  const enBuyuk = Math.max(...ust.map((s) => s.h));
  if (enBuyuk < orta * 1.2) return '';
  const secili = ust.filter((s) => s.h >= enBuyuk * 0.85).sort((a, b) => b.y - a.y || a.x - b.x);
  // Başlık en çok 2 satır (y farkı ≤ 2,2 satır yüksekliği)
  const ilkY = secili[0].y;
  // Aynı satırda bitişik parçalar ("Patoloji" + "nin") boşluksuz birleşir
  let t = '';
  let onceki: (typeof secili)[number] | null = null;
  for (const s of secili.filter((s) => ilkY - s.y <= enBuyuk * 2.2)) {
    const bitisik = onceki && Math.abs(onceki.y - s.y) < s.h * 0.3 && s.x - (onceki.x + onceki.w) < s.h * 0.12
      && !/\s$/.test(onceki.t) && !/^\s/.test(s.t);
    t += (onceki && !bitisik ? ' ' : '') + s.t;
    onceki = s;
  }
  t = t
    .replace(/\s+/g, ' ').replace(/\s+([,.;:])/g, '$1').trim();
  const harf = t.replace(/[^\p{L}]/gu, '');
  if (harf.length < 3 || t.length > 110) return '';
  // Tablo/şekil sayfası konu başlığı değildir: önceki alt başlık sürer
  if (/^(Tablo|Şekil|Resim|Figür|Grafik)\s*\d/iu.test(t)) return '';
  return t;
}

export async function cdSlaytBasliklari(detay: CdDetay): Promise<SlaytBasliklari> {
  const out: SlaytBasliklari = new Map();
  const pdf = detay.pdf;
  if (!pdf?.deckId || !pdf.paragraflar?.length) return out;
  const gerek = new Map<number, Set<number>>();
  for (const e of pdf.paragraflar) if (e) (gerek.get(e.dosya) ?? gerek.set(e.dosya, new Set()).get(e.dosya)!).add(e.sayfa);
  const is = (async () => {
    const bilgi = await resolveDeckPdf(pdf.deckId);
    const base = `${getCustomApiUrl() || ''}/vendor/pdfjs/`;
    for (const [dosya, sayfalar] of gerek) {
      const url = bilgi.files[dosya]?.url;
      if (!url) continue;
      const d = await pdfjs.getDocument({
        url, rangeChunkSize: 512 * 1024, disableStream: true, isEvalSupported: false,
        standardFontDataUrl: `${base}standard_fonts/`, cMapUrl: `${base}cmaps/`, cMapPacked: true,
      }).promise;
      try {
        for (const s of sayfalar) {
          if (s < 1 || s > d.numPages) continue;
          const p = await d.getPage(s);
          const tc = await p.getTextContent();
          const b = sayfaBasligi(tc.items as any, p.getViewport({ scale: 1 }).height);
          if (b) out.set(`${dosya}:${s}`, b);
        }
      } finally { d.destroy(); }
    }
  })();
  await Promise.race([is.catch((e) => console.warn('slayt başlıkları', e)), new Promise((r) => setTimeout(r, SURE_MS))]);
  return out;
}
