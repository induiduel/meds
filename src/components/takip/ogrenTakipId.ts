import { DECK_CATALOG } from '../../data/deckStore';

/** Etkileşimli ders takip kimliği: sürümlü derste grup kimliği (V1/V2 aynı konu sayılır). */
const GRUP = new Map(DECK_CATALOG.map((d) => [d.id, String(d.versionGroup || d.id)]));
export const ogrenTakipId = (id: string) => GRUP.get(id) || id;
