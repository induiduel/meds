import slidePdfMappingsRaw from '../data/slidePdfMappings.json';
import { getDeckOriginalPdf, DeckPdfMeta } from '../data/deckPdfCatalog';
import type { SlideItem } from '../components/learn/InteractiveDeckView';

export interface SlidePdfLocation {
  deckId: string;
  slideNumber: number;
  fileName: string;
  fileId?: string;
  driveUrl?: string;
  startPage: number;
  endPage: number;
  primaryPage: number;
  pageRange: [number, number];
  citation: string;
  totalPages: number;
}

const slidePdfMappings = slidePdfMappingsRaw as unknown as Record<
  string,
  {
    deckId: string;
    deckTitle: string;
    fileName: string;
    fileId?: string;
    driveUrl?: string;
    totalPdfPages: number;
    slides: Record<
      string,
      {
        slideNumber: number;
        title: string;
        primaryPage: number;
        startPage: number;
        endPage: number;
        pageRange: [number, number];
        citation: string;
        fileName: string;
      }
    >;
  }
>;

/**
 * Returns mapped PDF page information for a specific slide in an interactive deck.
 * Falls back to proportional heuristic if no exact pre-calculated mapping exists.
 */
export function getSlidePdfLocation(
  deckId: string,
  slideNumber: number,
  slide?: SlideItem,
  totalSlides?: number
): SlidePdfLocation {
  // 1. Check if slide itself contains sourcePdf
  if (slide?.sourcePdf?.startPage) {
    const sp = slide.sourcePdf;
    const startP = sp.startPage;
    const endP = sp.endPage || startP;
    const primP = sp.primaryPage || startP;
    const meta = getDeckOriginalPdf(deckId);
    return {
      deckId,
      slideNumber,
      fileName: sp.fileName || meta?.fileName || 'Ders_Notu.pdf',
      fileId: sp.fileId || meta?.fileId,
      driveUrl: meta?.driveUrl,
      startPage: startP,
      endPage: endP,
      primaryPage: primP,
      pageRange: [startP, endP],
      citation: sp.citation || (startP === endP ? `Sayfa ${startP}` : `Sayfa ${startP}-${endP}`),
      totalPages: meta ? 60 : 50,
    };
  }

  // 2. Check pre-calculated JSON mappings
  const deckMap = slidePdfMappings[deckId];
  if (deckMap) {
    const slideMap = deckMap.slides[String(slideNumber)];
    if (slideMap) {
      return {
        deckId,
        slideNumber,
        fileName: slideMap.fileName || deckMap.fileName,
        fileId: deckMap.fileId,
        driveUrl: deckMap.driveUrl,
        startPage: slideMap.startPage,
        endPage: slideMap.endPage,
        primaryPage: slideMap.primaryPage,
        pageRange: slideMap.pageRange,
        citation: slideMap.citation,
        totalPages: deckMap.totalPdfPages,
      };
    }
  }

  // 3. Fallback: Proportional mapping using catalog
  const meta: DeckPdfMeta | undefined = getDeckOriginalPdf(deckId);
  const nSlides = totalSlides || 30;
  const totalPages = deckMap?.totalPdfPages || 60;
  const estimatedPage = Math.max(1, Math.min(totalPages, Math.round((slideNumber / nSlides) * totalPages)));
  const startPage = Math.max(1, estimatedPage - 1);
  const endPage = Math.min(totalPages, estimatedPage + 1);

  return {
    deckId,
    slideNumber,
    fileName: meta?.fileName || 'Ders_Notu.pdf',
    fileId: meta?.fileId,
    driveUrl: meta?.driveUrl,
    startPage,
    endPage,
    primaryPage: estimatedPage,
    pageRange: [startPage, endPage],
    citation: startPage === endPage ? `Sayfa ${startPage}` : `Sayfa ${startPage}-${endPage}`,
    totalPages,
  };
}
