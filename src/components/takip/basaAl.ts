/** "Tekrar et" yardımcıları: konunun kalınan yerini başa alır (içerik ve öğrenildi işaretleri korunur). */

const ASISTAN_KEY = 'medsoru_onem_asistan_v1';
/** En önemliler: sesli asistanın kaldığı nokta silinir (baştan anlatır). */
export const onemAsistanBasaAl = (kod: string) => {
  try {
    const t = JSON.parse(localStorage.getItem(ASISTAN_KEY) || '{}');
    if (t && t[kod]) { delete t[kod]; localStorage.setItem(ASISTAN_KEY, JSON.stringify(t)); }
  } catch { /* özel pencere */ }
};

const LEARN_PROGRESS_KEY = 'medsoru_learn_progress_v1';
/** Etkileşimli ders: verilen destelerde kalınan adım başa alınır (görülen adımlar korunur). */
export const ogrenBasaAl = (ids: string[]) => {
  try {
    const p = JSON.parse(localStorage.getItem(LEARN_PROGRESS_KEY) || '{}') as Record<string, { last?: number; seen?: number[] } | undefined>;
    for (const id of ids) if (p[id]) p[id] = { ...p[id], last: 0 };
    localStorage.setItem(LEARN_PROGRESS_KEY, JSON.stringify(p));
  } catch { /* özel pencere */ }
};
