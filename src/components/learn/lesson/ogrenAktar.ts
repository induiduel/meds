/**
 * Etkileşimli ders metni (her adımın başlığı, alt başlığı ve anlatımı) → dışa aktarma belgesi. Oynatıcıdaki
 * "Ders metnini dışa aktar" ile kitaplıktaki "Toplu PDF" aynı belgeyi kullanır.
 */
import type { InteractiveDeck } from '../InteractiveDeckView';
import type { AktarBelge } from '../../../services/metinDisaAktar';
import { mdDuzenle } from '../../../services/maddeDuzen';
import { konusmaRedakte } from '../../../services/konusmaRedakte';
import { deckName } from '../../../data/deckStore';

/** Sesli dersle aynı düzen: PDF'de adım başlığı + alt başlık + maddeler bölünmez, sıralamalar "1 -", konuşma
 *  kalıpları ders notu üslubuna redakte edilir. */
export function ogrenAktarBelgesi(deck: InteractiveDeck): AktarBelge {
  const ust = [deck.discipline, deck.instructor].filter(Boolean).join(' · ');
  return {
    baslik: deckName(deck),
    dersDuzeni: true,
    alt: `${ust ? `${ust} · ` : ''}Etkileşimli ders metni`,
    bolumler: (deck.slides || [])
      .map((sl: any) => ({ sl, md: String(sl.synthesisNarrative || sl.content || '').trim() }))
      .filter((x) => x.md)
      .map(({ sl, md }) => ({ baslik: `${sl.slideNumber}. ${String(sl.title || '').replace(/^\[[^\]]+\]\s*/, '')}`, alt: sl.subtitle || undefined, md: konusmaRedakte(mdDuzenle(md)) })),
  };
}
