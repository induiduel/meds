/**
 * Kopya soru birleştirme katmanı (server-only).
 *
 * Aynı çıkmış soru farklı sınav dökümlerinden farklı kimliklerle birden çok kez girilmiş. Gruplar
 * scripts/advanced_ai/merge_duplicate_questions.py ile hesaplanır ve
 * $MEDS_DATABASE_DIR/../meds_database_v2/soru_birlestirme/birlestirmeler.json dosyasında tutulur.
 * Veri dosyası (pastQuestions.json) değişmez: okuma sırasında her gruptan yalnız "asil" soru gösterilir, kopyalar
 * gizlenir. Asıl soruya yönetici için anahtarlar eklenir (kullanıcı arayüzünde gösterilmez):
 *   mergedFrom: string[]   — gizlenen kopya kimlikleri
 *   mergeGroupId: string   — grup kimliği (/manage → Birleştirilen sorular)
 *   mergeIdentical: bool   — kopyalar birebir aynı mı (değilse yönetici seçim yapmalı)
 * Yönetici kararları: durum 'onayli' (birleştirme doğru), 'ayrildi' (birleştirme geri alındı, hepsi gösterilir),
 * asil değiştirilebilir.
 */
import fs from 'fs';
import path from 'path';

export interface MergeGroup {
  id: string;
  asil: string;
  uyeler: string[];
  birebir_ayni: boolean;
  benzerlik: number;
  durum: 'otomatik' | 'onayli' | 'ayrildi';
  olusturma?: string;
  karar_zamani?: string;
}

export const mergeFile = () =>
  path.join(
    path.dirname(process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database')),
    'meds_database_v2',
    'soru_birlestirme',
    'birlestirmeler.json',
  );

let cache: { mtime: number; groups: MergeGroup[]; hidden: Map<string, MergeGroup>; primary: Map<string, MergeGroup> } | null = null;

function load() {
  try {
    const st = fs.statSync(mergeFile());
    if (cache && cache.mtime === st.mtimeMs) return cache;
    const groups: MergeGroup[] = JSON.parse(fs.readFileSync(mergeFile(), 'utf-8')).gruplar || [];
    const hidden = new Map<string, MergeGroup>();
    const primary = new Map<string, MergeGroup>();
    for (const g of groups) {
      if (g.durum === 'ayrildi') continue;
      primary.set(g.asil, g);
      for (const u of g.uyeler) if (u !== g.asil) hidden.set(u, g);
    }
    cache = { mtime: st.mtimeMs, groups, hidden, primary };
  } catch {
    cache = { mtime: 0, groups: [], hidden: new Map(), primary: new Map() };
  }
  return cache;
}

/** Dosya değişim zamanı (HTTP önbellek doğrulaması için). */
export function mergeMtime(): number {
  return load().mtime;
}

export function readMergeGroups(): MergeGroup[] {
  return load().groups;
}

/** Faz 14 ve diğer okuyucular için: bu soru başka bir sorunun gizlenen kopyası mı? */
export function mergedInto(id: string): string | null {
  return load().hidden.get(String(id))?.asil || null;
}

/** Kopyaları gizler, asıl soruya yönetici anahtarlarını ekler (veri dosyası değişmez). */
export function applyMergeOverlay<T extends Record<string, any>>(list: T[]): T[] {
  const { groups } = load();
  if (!groups.length) return list;
  // Asıl soru listede yoksa (ör. karantina gizlediyse) grubun listede olan ilk üyesi gösterilir: soru siteden kaybolmaz
  const present = new Set(list.map((q) => String(q.id ?? '')));
  const hidden = new Map<string, MergeGroup>();
  const primary = new Map<string, MergeGroup>();
  for (const g of groups) {
    if (g.durum === 'ayrildi') continue;
    const shown = present.has(g.asil) ? g.asil : g.uyeler.find((u) => present.has(u));
    if (!shown) continue;
    primary.set(shown, g);
    for (const u of g.uyeler) if (u !== shown) hidden.set(u, g);
  }
  const out: T[] = [];
  for (const q of list) {
    const id = String(q.id ?? '');
    if (hidden.has(id)) continue;
    const g = primary.get(id);
    out.push(
      g
        ? ({ ...q, mergedFrom: g.uyeler.filter((u) => u !== id), mergeGroupId: g.id, mergeIdentical: !!g.birebir_ayni } as T)
        : q,
    );
  }
  return out;
}

/** Yönetici kararı: asıl soruyu değiştir, birleştirmeyi onayla ya da grubu ayır. */
export function updateMergeGroup(
  groupId: string,
  action: { type: 'primary'; asil: string } | { type: 'confirm' } | { type: 'split' } | { type: 'restore' },
): MergeGroup {
  const file = mergeFile();
  const data = JSON.parse(fs.readFileSync(file, 'utf-8'));
  const g: MergeGroup | undefined = (data.gruplar || []).find((x: MergeGroup) => x.id === groupId);
  if (!g) throw new Error('Birleştirme grubu bulunamadı.');
  if (action.type === 'primary') {
    if (!g.uyeler.includes(action.asil)) throw new Error('Seçilen soru bu grupta değil.');
    g.asil = action.asil;
    g.durum = 'onayli';
  } else if (action.type === 'confirm') {
    g.durum = 'onayli';
  } else if (action.type === 'split') {
    g.durum = 'ayrildi';
  } else {
    g.durum = 'onayli';
  }
  g.karar_zamani = new Date().toISOString();
  data.guncelleme = g.karar_zamani;
  const tmp = file + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(data, null, 1), 'utf-8');
  fs.renameSync(tmp, file);
  cache = null;
  return g;
}
