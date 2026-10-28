/**
 * İçerik görünürlüğü kuralı (Yönetim v16, 2026-10-28) — SAF, bağımlılıksız: hem istemci (services/siteAyar.ts::icerikGizli)
 * hem sunucu (yonetim16/siteAyar.ts::icerikKapisi) bunu kullanır; iki tarafın kararı ayrışmasın.
 *
 * Site ayarı `gorunurluk` haritası anahtarları: `ders:<id>`, `kurul:<n>`, `deste:<id>`, `sesli:<key>`, `paket:<key>`,
 * `onem|asistan|cozucu:<dizin>/<kod>`. Değer `acik | gizli | yalniz-yonetici` (ikisi de öğrenciye kapalı).
 * Kalıtım: içeriğin kimliğinden ders (k2-07) ve kurul (2) çıkarılır; ders ya da kurul kapalıysa altındaki sesli ders, deste,
 * içerik paketi de kapalıdır. Önem/asistan/çözücü dizini `k<N>…` ise kurul N, değilse kurul 1.
 */
export type IcerikTur = 'ders' | 'kurul' | 'deste' | 'sesli' | 'paket' | 'onem' | 'asistan' | 'cozucu';
export type IcerikDurum = 'acik' | 'gizli' | 'yalniz-yonetici';

const DERS_RE = /(?:^|-)(k(\d)-\d+)(?=-|$)/;

/** Kimlikten ders kimliği (k2-07) — sesli anahtarı, deste kimliği (k2p-k2-07-…), paket anahtarı */
export function dersKimligi(id: string): string | null {
  const m = String(id || '').match(DERS_RE);
  return m ? m[1] : null;
}

export function kurulNo(tur: IcerikTur, id: string): number | null {
  if (tur === 'kurul') return Number(id) || null;
  if (tur === 'onem' || tur === 'asistan' || tur === 'cozucu') {
    const m = String(id).match(/^k(\d)/);
    return m ? Number(m[1]) : 1;
  }
  const d = dersKimligi(id);
  if (d) return Number(d.charAt(1));
  const m = String(id).match(/^k(\d)p-/);
  return m ? Number(m[1]) : null;
}

const AGIRLIK: Record<IcerikDurum, number> = { acik: 0, 'yalniz-yonetici': 1, gizli: 2 };

/** En kısıtlayıcı durum (doğrudan anahtar, bağlı ders, bağlı kurul) */
export function icerikDurumu(g: Record<string, string> | undefined | null, tur: IcerikTur, id: string): IcerikDurum {
  if (!g) return 'acik';
  let en: IcerikDurum = 'acik';
  const bak = (k: string) => {
    const v = g[k] as IcerikDurum | undefined;
    if (v && AGIRLIK[v] > AGIRLIK[en]) en = v;
  };
  bak(`${tur}:${id}`);
  if (tur !== 'ders' && tur !== 'kurul') {
    const d = dersKimligi(id);
    if (d) bak(`ders:${d}`);
  }
  const k = kurulNo(tur, id);
  if (k && tur !== 'kurul') bak(`kurul:${k}`);
  return en;
}

/** Haritada en az bir kapalı anahtar var mı (hızlı çıkış) */
export function kapaliAnahtarVar(g: Record<string, string> | undefined | null): boolean {
  return !!g && Object.values(g).some((v) => v === 'gizli' || v === 'yalniz-yonetici');
}
