/** Sesli sınav asistanı içerik dosyaları (ders başına tembel). Sayfa yalnız varlığını sorar; içerik asistan açılınca iner. */
const DOSYA = import.meta.glob('../../../data/patoloji_asistan/[0-9]*.json');
export const asistanYolu = (kod: string) => `../../../data/patoloji_asistan/${kod}.json`;
export const asistanDersVar = (kod: string) => !!DOSYA[asistanYolu(kod)];
export const asistanDosyasi = (kod: string) => DOSYA[asistanYolu(kod)] as (() => Promise<{ default: unknown }>) | undefined;
export const asistanDersleri = () => Object.keys(DOSYA).map((k) => k.replace(/^.*\/(\w+)\.json$/, '$1'));
