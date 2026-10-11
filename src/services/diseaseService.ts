import { DiseaseProfile } from '../types/disease';
import seedDiseases from '../data/diseases.json';

const CUSTOM_DISEASES_STORAGE_KEY = 'medsor_custom_diseases_v1';
const FAVORITES_STORAGE_KEY = 'medsor_favorite_diseases_v1';

export const DiseaseService = {
  /**
   * Tüm hastalıkları getirir (varsayılan veritabanı + kullanıcının eklediği/düzenlediği)
   */
  getAllDiseases(): DiseaseProfile[] {
    const list: DiseaseProfile[] = [...(seedDiseases as unknown as DiseaseProfile[])];
    
    if (typeof localStorage !== 'undefined') {
      try {
        const rawCustom = localStorage.getItem(CUSTOM_DISEASES_STORAGE_KEY);
        if (rawCustom) {
          const customList: DiseaseProfile[] = JSON.parse(rawCustom);
          for (const item of customList) {
            const idx = list.findIndex(d => d.id === item.id);
            if (idx >= 0) {
              list[idx] = { ...list[idx], ...item };
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

  getDiseaseById(id: string): DiseaseProfile | undefined {
    return this.getAllDiseases().find(d => d.id === id);
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
      return new Set(raw ? JSON.parse(raw) : []);
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
