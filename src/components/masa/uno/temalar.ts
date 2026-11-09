/** Uno temaları: renk tonları, adlar, yazı karakteri. Kart ve masa çizimi buradan okur (çizimler özgündür). */
import type { UnoDeger, UnoRenk } from '../../../services/masa/tipler';

export interface UnoRenkTon { ad: string; ana: string; koyu: string; acik: string; ikincil: string }
export interface UnoTemaTanim {
  ad: string;
  renk: Record<UnoRenk, UnoRenkTon>;
  /** Joker kartının zemini */
  joker: string;
  /** Kart kenarı ve orta amblem zemini */
  kenar: string;
  amblem: string;
  yazi: string;
  /** Aksiyon kartlarının alt yazısı (yalnız büyücü temasında görünür) */
  altYazi?: Partial<Record<UnoDeger, string>>;
}

export const UNO_TEMA: Record<string, UnoTemaTanim> = {
  klasik: {
    ad: 'Klasik',
    renk: {
      k: { ad: 'Kırmızı', ana: '#e0242f', koyu: '#a3111b', acik: '#ff6b73', ikincil: '#ffffff' },
      s: { ad: 'Sarı', ana: '#f5c400', koyu: '#b98d00', acik: '#ffe066', ikincil: '#ffffff' },
      y: { ad: 'Yeşil', ana: '#27a04b', koyu: '#157032', acik: '#66d488', ikincil: '#ffffff' },
      m: { ad: 'Mavi', ana: '#1a66d6', koyu: '#0e449a', acik: '#6aa5ff', ikincil: '#ffffff' },
    },
    joker: '#17171b', kenar: '#ffffff', amblem: '#ffffff',
    yazi: '"Arial Black", "Helvetica Neue", Impact, system-ui, sans-serif',
  },
  stitch: {
    ad: 'Tropik',
    renk: {
      k: { ad: 'Mercan', ana: '#ff6a5c', koyu: '#c9402f', acik: '#ffa399', ikincil: '#fff4e0' },
      s: { ad: 'Güneş', ana: '#ffc531', koyu: '#c98f00', acik: '#ffe08a', ikincil: '#fff4e0' },
      y: { ad: 'Palmiye', ana: '#1fa56e', koyu: '#0f6f48', acik: '#6fd9a8', ikincil: '#fff4e0' },
      m: { ad: 'Lagün', ana: '#18a4d6', koyu: '#0b6f96', acik: '#7fd6f2', ikincil: '#fff4e0' },
    },
    joker: '#3b2a6b', kenar: '#fff8ea', amblem: '#fff4e0',
    yazi: 'ui-rounded, "Nunito", "Baloo 2", "Trebuchet MS", "Segoe UI", system-ui, sans-serif',
  },
  buyucu: {
    ad: 'Büyücü',
    renk: {
      k: { ad: 'Kızıl', ana: '#8e1b25', koyu: '#5e0f16', acik: '#c9525b', ikincil: '#d9aa3c' },
      s: { ad: 'Sarı', ana: '#e2aa17', koyu: '#a87a05', acik: '#f5d262', ikincil: '#1d1a16' },
      y: { ad: 'Zümrüt', ana: '#166a4a', koyu: '#0b4630', acik: '#4fae8a', ikincil: '#cfd6dc' },
      m: { ad: 'Lacivert', ana: '#1d3272', koyu: '#101d49', acik: '#6079c4', ikincil: '#b9814a' },
    },
    joker: '#241c14', kenar: '#c9a24a', amblem: '#f1e3bf',
    yazi: '"Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif',
    altYazi: { pas: 'Atlat', yon: 'Yön', '+2': '+2 Çek', joker: 'Joker', '+4': '+4 Çek' },
  },
};

export const temaAl = (tema: string | undefined): UnoTemaTanim => UNO_TEMA[tema || ''] || UNO_TEMA.klasik;
export const temaKod = (tema: string | undefined): string => (tema && UNO_TEMA[tema] ? tema : 'klasik');
export const UNO_SIRA: readonly UnoRenk[] = ['k', 's', 'y', 'm'];
