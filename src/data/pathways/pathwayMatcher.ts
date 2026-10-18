import type { MechanismPathway } from '../../types/pathway';
import { PATHWAY_CATALOG } from './pathwayCatalog';

interface PathwayMatcherRule {
  pathwayId: string;
  strongKeywords: RegExp[];
  supportingKeywords: RegExp[];
}

const MATCHER_RULES: PathwayMatcherRule[] = [
  {
    pathwayId: 'arasidonik-asit',
    strongKeywords: [
      /ara[sş]idonik\s*asit/i,
      /eikozanoid/i,
      /siklooksijenaz\s*(yola[gğ]|kolu)/i,
      /lipok?sijenaz\s*(yola[gğ]|kolu)/i,
      /fosfolipaz\s*a[₂2]/i,
      /prostanoid/i,
    ],
    supportingKeywords: [
      /\bcox-[123]\b/i,
      /\b5-lox\b/i,
      /prostaglandin/i,
      /tromboksan/i,
      /l[öo]kotrien/i,
      /l[öo]kotriyen/i,
      /prostasiklin/i,
      /pgi[₂2]/i,
      /txa[₂2]/i,
      /nsa[iİı]/i,
      /zileuton/i,
    ],
  },
  {
    pathwayId: 'apoptoz-kaskadi',
    strongKeywords: [
      /kaspaz\s*kaskad/i,
      /apoptozom/i,
      /mitokondriyal\s*(\(i[çc]sel\)\s*)?yol/i,
      /[öo]l[üu]m\s*resept[öo]r[üu]\s*(\(d[ıi][sş]sal\)\s*)?yol/i,
      /bax\s*ve\s*bak/i,
      /bcl-2\s*ailesi/i,
      /sitokrom\s*c\s*sal[ıi]n/i,
    ],
    supportingKeywords: [
      /kaspaz-[3789]/i,
      /\bbax\b/i,
      /\bbak\b/i,
      /\bbcl-2\b/i,
      /\bbcl-xl\b/i,
      /apaf-1/i,
      /fasl\b/i,
      /tnfr1/i,
      /fadd\b/i,
    ],
  },
  {
    pathwayId: 'lokosit-ekstravazasyonu',
    strongKeywords: [
      /l[öo]kosit\s*(g[öo][çc][üu]|al[ıi]m[ıi]|recruitment)/i,
      /marjinasyon\s*ve\s*yuvarlanma/i,
      /transmigrasyon\s*(\(diapedez\))?/i,
      /diapedez/i,
      /selektin\s*ailesi/i,
      /l[öo]kosit\s*adezyon/i,
    ],
    supportingKeywords: [
      /selektin/i,
      /integrin/i,
      /pecam-1/i,
      /\bcd31\b/i,
      /sialyl-lewis/i,
      /icam-1/i,
      /vcam-1/i,
      /kemotaksi/i,
    ],
  },
];

/**
 * Verilen metin veya başlıkta kilit bir mekanizma geçip geçmediğini kontrol eder.
 * Tıbbi olarak güçlü bir eşleşme varsa ilgili MechanismPathway nesnesini döndürür.
 */
export function findMatchingPathway(text: string): MechanismPathway | null {
  if (!text || text.length < 5) return null;

  for (const rule of MATCHER_RULES) {
    // 1. Güçlü bir anahtar kelime var mı?
    const hasStrong = rule.strongKeywords.some((kw) => kw.test(text));
    if (hasStrong) {
      return PATHWAY_CATALOG[rule.pathwayId] || null;
    }

    // 2. Destekleyici anahtar kelimelerden en az 2 tanesi birlikte geçiyor mu?
    let supportCount = 0;
    for (const kw of rule.supportingKeywords) {
      if (kw.test(text)) {
        supportCount++;
      }
    }
    if (supportCount >= 2) {
      return PATHWAY_CATALOG[rule.pathwayId] || null;
    }
  }

  return null;
}
