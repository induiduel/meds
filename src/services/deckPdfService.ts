/**
 * Öğren destesi → ders PDF'i (istemci). Eşleşmeler içerikle doğrulanmıştır (`scripts/build_deck_pdf_sources.py`);
 * doğrulanmamış deste için PDF gösterilmez (tahmin yok).
 *  - Sunucu: `GET /api/lecture-pdf/deck/:id` → dosyalar (sıra sabit), slayt → [başlangıç, bitiş, dosyaIndeksi?],
 *    PDF yoksa ders tarihi; `/api/lecture-pdf/deck/:id/:i` Range destekli akış; `/api/lecture-pdf/decks` katalog listesi.
 *  - Sunucu yoksa (GitHub Pages) derlemeyle gelen `src/data/deckPdfSources.json` (tembel) → Drive önizlemesi.
 */
import { useEffect, useState } from 'react';
import { getCustomApiUrl } from './api';

export interface DeckPdfFile {
  name: string;
  /** Drive'daki ders dalı klasörü */
  folder?: string;
  size?: number;
  pages?: number;
  fileId?: string;
  /** Sunucudan akış adresi (dosya sunucuda yoksa tanımsız → Drive) */
  url?: string;
}

/** [başlangıç, bitiş] ya da [başlangıç, bitiş, dosyaIndeksi] */
export type SlidePages = number[];

export interface DeckPdfInfo {
  files: DeckPdfFile[];
  slides?: Record<string, SlidePages>;
  /** PDF yoksa: ders programındaki tarih (YYYY-AA-GG) */
  missingDate?: string;
  /** true: en az bir dosya sunucuda (PDF.js ile açılır) */
  hasServerFile: boolean;
}

type SourceEntry = { title: string; files: (DeckPdfFile & { path?: string })[]; slides?: Record<string, SlidePages>; missing?: { tarih?: string } };
type SourcesFile = { decks: Record<string, SourceEntry> };
type ServerFile = DeckPdfFile & { available?: boolean };

const apiBase = () => getCustomApiUrl() || '';

let sourcesP: Promise<SourcesFile> | null = null;
function loadBundledSources(): Promise<SourcesFile> {
  if (!sourcesP) {
    sourcesP = import('../data/deckPdfSources.json')
      .then((m) => ((m as any).default || m) as SourcesFile)
      .catch(() => {
        sourcesP = null;
        return { decks: {} };
      });
  }
  return sourcesP;
}

let availP: Promise<Record<string, ServerFile[]> | null> | null = null;
let availAt = 0;
/** Sunucuda açılabilen PDF'ler (5 dk önbellek). Sunucuya ulaşılamazsa null. */
function fetchAvailability(): Promise<Record<string, ServerFile[]> | null> {
  if (availP && Date.now() - availAt < 5 * 60 * 1000) return availP;
  availAt = Date.now();
  availP = fetch(`${apiBase()}/api/lecture-pdf/decks`)
    .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
    .then((j) => (j?.decks || {}) as Record<string, ServerFile[]>)
    .catch(() => {
      availAt = 0;
      return null;
    });
  return availP;
}

const fileUrl = (deckId: string, i: number, f: DeckPdfFile) =>
  `${apiBase()}/api/lecture-pdf/deck/${encodeURIComponent(deckId)}/${i}?v=${f.size || 0}`;

const infoCache = new Map<string, Promise<DeckPdfInfo>>();

export function resolveDeckPdf(deckId: string): Promise<DeckPdfInfo> {
  const hit = infoCache.get(deckId);
  if (hit) return hit;
  const p = (async (): Promise<DeckPdfInfo> => {
    try {
      const r = await fetch(`${apiBase()}/api/lecture-pdf/deck/${encodeURIComponent(deckId)}`);
      if (r.ok) {
        const j = await r.json();
        const files: DeckPdfFile[] = (j.files || []).map((f: ServerFile, i: number) => ({
          name: f.name,
          folder: f.folder,
          size: f.size,
          pages: f.pages,
          fileId: f.fileId,
          url: f.available ? fileUrl(deckId, i, f) : undefined,
        }));
        return { files, slides: j.slides || undefined, missingDate: j.missing?.tarih, hasServerFile: files.some((f) => f.url) };
      }
    } catch {
      /* sunucu yok → paketteki eşleme */
    }
    const e = (await loadBundledSources()).decks[deckId];
    return {
      files: (e?.files || []).map(({ path: _p, ...f }) => f),
      slides: e?.slides,
      missingDate: e?.missing?.tarih,
      hasServerFile: false,
    };
  })();
  infoCache.set(deckId, p);
  p.then((r) => { if (!r.files.length) setTimeout(() => infoCache.delete(deckId), 60_000); });
  return p;
}

export const drivePreviewUrl = (fileId: string) => `https://drive.google.com/file/d/${fileId}/preview`;
export const driveViewUrl = (fileId: string) => `https://drive.google.com/file/d/${fileId}/view`;

/** Bileşen kancası: yüklenene kadar null. */
export function useDeckPdf(deckId: string): DeckPdfInfo | null {
  const [info, setInfo] = useState<DeckPdfInfo | null>(null);
  useEffect(() => {
    let live = true;
    setInfo(null);
    resolveDeckPdf(deckId).then((r) => live && setInfo(r));
    return () => {
      live = false;
    };
  }, [deckId]);
  return info;
}

/** Öğren kataloğu: PDF'i açılabilen desteler (sunucuda dosya; sunucu yoksa Drive kimliği olan). */
export function useDeckPdfIds(): Set<string> | null {
  const [ids, setIds] = useState<Set<string> | null>(null);
  useEffect(() => {
    let live = true;
    fetchAvailability().then(async (avail) => {
      let s: Set<string>;
      if (avail) s = new Set(Object.keys(avail));
      else {
        const src = await loadBundledSources();
        s = new Set(Object.entries(src.decks).filter(([, e]) => e.files.some((f) => f.fileId)).map(([id]) => id));
      }
      if (live) setIds(s);
    });
    return () => {
      live = false;
    };
  }, []);
  return ids;
}
