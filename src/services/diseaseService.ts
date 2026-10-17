import { DiseaseProfile } from '../types/disease';
import { isV2, normalizeDisease } from './diseaseModel';
import { safeJsonFetch } from './api';
import { contentReady, isContentChanged, onContentChanged } from './contentLive';

// 470 profil (~1 MB gzip) sayfa koduyla birlikte değil, ayrı parça olarak eşzamansız yüklenir
let seed: DiseaseProfile[] | null = null;
let loading: Promise<DiseaseProfile[]> | null = null;

const CUSTOM_DISEASES_STORAGE_KEY = 'medsor_custom_diseases_v1';
const FAVORITES_STORAGE_KEY = 'medsor_favorite_diseases_v1';

export const DiseaseService = {
  /** Tohum veriyi bir kez yükler (sonraki çağrılar önbellekten) */
  load(): Promise<DiseaseProfile[]> {
    if (seed) return Promise.resolve(seed);
    if (!loading) {
      loading = (async () => {
        try {
          // Panelden değiştirildiyse paketteki kopya eskidir: sunucudan (canlı içerik katmanı)
          await contentReady(1500).catch(() => {});
          let raw: unknown[] | null = null;
          if (isContentChanged('diseases')) {
            const r = await safeJsonFetch<unknown[]>('/api/content/diseases', { cache: 'no-store' }).catch(() => null);
            if (r && r.ok && Array.isArray(r.data)) raw = r.data;
          }
          if (!raw) {
            const m = await import('../data/diseases.json');
            raw = ((m as { default?: unknown }).default ?? m) as unknown[];
          }
          seed = raw.map(normalizeDisease);
          return seed;
        } catch (err) {
          console.error('[DiseaseService] Yükleme hatası:', err);
          loading = null;
          throw err;
        }
      })();
    }
    return loading;
  },

  isLoaded(): boolean {
    return seed !== null;
  },

  /**
   * Tüm hastalıkları getirir (varsayılan veritabanı + kullanıcının eklediği/düzenlediği)
   */
  getAllDiseases(): DiseaseProfile[] {
    const list: DiseaseProfile[] = [...(seed || [])];
    
    if (typeof localStorage !== 'undefined') {
      try {
        const rawCustom = localStorage.getItem(CUSTOM_DISEASES_STORAGE_KEY);
        if (rawCustom) {
          // Eski (şema 1) yerel katkılar da şema 2'ye çevrilir; birleştirilmiş eski kimlik kanonik kayda düşer
          for (const rawItem of JSON.parse(rawCustom) as unknown[]) {
            const item = normalizeDisease(rawItem);
            const idx = list.findIndex(d => d.id === item.id || (d.aliases || []).includes(item.id));
            // Şema 1 düzenlemesi eski şablon verisinin kopyasıdır: yeniden yazılmış kanonik kaydı ezmez
            if (idx >= 0 && !isV2(rawItem)) continue;
            if (idx >= 0) {
              list[idx] = { ...list[idx], ...item, id: list[idx].id };
            } else {
              list.unshift(item);
            }
          }
        }
      } catch (e) {
        console.warn('[DiseaseService] Özel hastalıklar yüklenemedi:', e);
      }
    }
    
    return list;
  },

  /** Kimlik ya da birleştirilmiş eski kimlik (alias) ile */
  getDiseaseById(id: string): DiseaseProfile | undefined {
    const all = this.getAllDiseases();
    return all.find(d => d.id === id) || all.find(d => (d.aliases || []).includes(id));
  },

  /**
   * Yeni hastalık ekler veya mevcut olanı günceller
   */
  saveDisease(profile: DiseaseProfile): boolean {
    if (typeof localStorage === 'undefined') return false;
    try {
      const rawCustom = localStorage.getItem(CUSTOM_DISEASES_STORAGE_KEY);
      const customList: DiseaseProfile[] = rawCustom ? JSON.parse(rawCustom) : [];
      const nowIso = new Date().toISOString();
      const updated: DiseaseProfile = {
        ...profile,
        updatedAt: nowIso,
        isCustom: true
      };

      const idx = customList.findIndex(d => d.id === updated.id);
      if (idx >= 0) {
        customList[idx] = updated;
      } else {
        customList.unshift(updated);
      }

      localStorage.setItem(CUSTOM_DISEASES_STORAGE_KEY, JSON.stringify(customList));
      return true;
    } catch (e) {
      console.error('[DiseaseService] Hastalık kaydedilemedi:', e);
      return false;
    }
  },

  /**
   * Hastalığı siler (Özel eklenenler veya admin sildiği zaman)
   */
  deleteDisease(id: string): boolean {
    if (typeof localStorage === 'undefined') return false;
    try {
      const rawCustom = localStorage.getItem(CUSTOM_DISEASES_STORAGE_KEY);
      if (!rawCustom) return false;
      const customList: DiseaseProfile[] = JSON.parse(rawCustom);
      const filtered = customList.filter(d => d.id !== id);
      localStorage.setItem(CUSTOM_DISEASES_STORAGE_KEY, JSON.stringify(filtered));
      return true;
    } catch (e) {
      console.error('[DiseaseService] Hastalık silinemedi:', e);
      return false;
    }
  },

  /**
   * Favori yönetimi
   */
  getFavoriteIds(): Set<string> {
    if (typeof localStorage === 'undefined') return new Set();
    try {
      const raw = localStorage.getItem(FAVORITES_STORAGE_KEY);
      const ids: string[] = raw ? JSON.parse(raw) : [];
      // Birleştirilen eski kimlikler kanonik kimliğe çevrilir
      const canon = new Map<string, string>();
      for (const d of seed || []) for (const a of d.aliases || []) canon.set(a, d.id);
      return new Set(ids.map((id) => canon.get(id) || id));
    } catch {
      return new Set();
    }
  },

  isFavorite(id: string): boolean {
    return this.getFavoriteIds().has(id);
  },

  toggleFavorite(id: string): boolean {
    if (typeof localStorage === 'undefined') return false;
    const favs = this.getFavoriteIds();
    let isNowFav = false;
    if (favs.has(id)) {
      favs.delete(id);
    } else {
      favs.add(id);
      isNowFav = true;
    }
    try {
      localStorage.setItem(FAVORITES_STORAGE_KEY, JSON.stringify(Array.from(favs)));
    } catch {}
    return isNowFav;
  }
};

// Panel değişikliği: yeniden yüklenir, açık ekran `medsoru:diseases-changed` ile tazelenir
if (typeof window !== 'undefined') setTimeout(() => {
  onContentChanged('diseases', () => {
    if (!seed) return; // hiç açılmadıysa ilk açılışta zaten güncel olanı alır
    seed = null;
    loading = null;
    void DiseaseService.load().then(() => window.dispatchEvent(new CustomEvent('medsoru:diseases-changed')));
  });
}, 0);
