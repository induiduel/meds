/**
 * Çevrimdışı eksik giderici (H483). Cihazda indirilmiş içeriği tarar, internetsiz çalışması için gereken ama eksik kalan
 * parçaları yalnız onları indirerek tamamlar:
 *  - Sesli ders: defterdeki PDF'ler, PDF eşlemesi (deste JSON'u), ders ayrıntısı; sunucuda PDF'i olduğu hâlde PDF'siz
 *    indirilmiş dersler. Eksik varsa cdCevrimdisiAyarla aynı seslerle yeniden çağrılır (yalnız eksik/eski parçalar iner).
 *  - PDF.js yardımcıları (yazı tipi, wasm): sesli ders önbelleğine (cdCevrimdisiOnIsit).
 *  - Çevrimdışı merkezi paketleri: paketiDenetle → bozuk/eksik olanlar paketOnar ile kuyruğa.
 * Açılışta internet varken en çok 12 saatte bir (sürüm değişince hemen) kendiliğinden çalışır; ağ yoksa hiçbir şey yapmaz.
 */
import { durumAl, katalogYenile, paketiDenetle, paketOnar, bildir } from './paketMotoru';

const DAMGA_KEY = 'medsoru_cevrimdisi_eksik_gider_v1';
const ARALIK = 12 * 3600_000;
let suruyor: Promise<EksikRapor> | null = null;

export interface EksikRapor { sesliOnarilan: string[]; paketOnarilan: string[]; hata: string[] }

/** Onarım kuralı değişince artırılır: her cihazda bir kez beklemeden yeniden taranır */
const ONARIM_SURUM = 'H483';
const surum = () => ONARIM_SURUM;

async function sesliEksikler(): Promise<string[]> {
  const mod = await import('../../components/canliDers/canliDersCevrimdisi');
  const { cdCevrimdisiKayitlari } = await import('../../components/canliDers/canliDersCevrimdisiKayit');
  const { cdListeGetir } = await import('../../components/canliDers/canliDersStore');
  const kayitlar = cdCevrimdisiKayitlari();
  const keys = Object.keys(kayitlar);
  if (!keys.length) return [];
  const cache = await caches.open(mod.CD_OFFLINE_CACHE);
  const var_ = new Set((await cache.keys()).map((r) => r.url));
  // Sunucuda PDF'i olan dersler (PDF'siz indirilmiş eski kayıtları yakalamak için)
  const liste = await Promise.all([cdListeGetir().catch(() => []), cdListeGetir(false, '2025-2026').catch(() => [])]);
  const pdfli = new Set(liste.flat().filter((d) => d.pdf).map((d) => d.key));
  const eksik: string[] = [];
  for (const key of keys) {
    const k = kayitlar[key];
    const pdfler = k.pdfler || [];
    let sorun = pdfler.some((u) => !var_.has(u));
    if (!sorun && k.deckId) sorun = ![...var_].some((u) => u.endsWith(`/api/lecture-pdf/deck/${encodeURIComponent(k.deckId!)}`));
    if (!sorun && !pdfler.length && pdfli.has(key)) sorun = true;
    if (!sorun) sorun = !(await mod.cdYerelDetay(key).catch(() => null));
    if (sorun) eksik.push(key);
  }
  return eksik;
}

/** Tüm indirilenleri tarar ve eksikleri giderir. `zorla` damgayı yok sayar. */
export function eksikleriGider(zorla = false): Promise<EksikRapor> {
  if (suruyor) return suruyor;
  suruyor = (async () => {
    const rapor: EksikRapor = { sesliOnarilan: [], paketOnarilan: [], hata: [] };
    if (!navigator.onLine || typeof caches === 'undefined') return rapor;
    try {
      const d = JSON.parse(localStorage.getItem(DAMGA_KEY) || '{}');
      if (!zorla && d.surum === surum() && Date.now() - (d.at || 0) < ARALIK) return rapor;
    } catch { /* depo yok */ }
    const mod = await import('../../components/canliDers/canliDersCevrimdisi');
    const { cdCevrimdisiKayitlari, cdKayitSesleri } = await import('../../components/canliDers/canliDersCevrimdisiKayit');
    const kayitSay = Object.keys(cdCevrimdisiKayitlari()).length;
    if (kayitSay) await mod.cdCevrimdisiOnIsit().catch(() => {});
    // Sesli dersler: yalnız eksik parçalar (aynı sesler) yeniden iner
    for (const key of await sesliEksikler().catch(() => [] as string[])) {
      if (!navigator.onLine) break;
      try {
        const vidler = cdKayitSesleri(cdCevrimdisiKayitlari()[key]).map((x) => x.vid);
        await mod.cdCevrimdisiAyarla(key, vidler.length ? vidler : null);
        rapor.sesliOnarilan.push(key);
      } catch (e: any) { rapor.hata.push(`${key}: ${e?.message || e}`); }
    }
    // Çevrimdışı merkezi paketleri (sesli olanlar yukarıda onarıldı)
    await katalogYenile().catch(() => {});
    const bozuk: string[] = [];
    for (const k of Object.values(durumAl().kayitlar)) {
      if (k.yarim || k.modul === 'sesli') continue;
      const s = await paketiDenetle(k.id);
      if (!s.ok) bozuk.push(k.id);
    }
    if (bozuk.length) { await paketOnar(bozuk); rapor.paketOnarilan = bozuk; }
    try { localStorage.setItem(DAMGA_KEY, JSON.stringify({ surum: surum(), at: Date.now() })); } catch { /* yok */ }
    const n = rapor.sesliOnarilan.length + rapor.paketOnarilan.length;
    if (n) bildir(`Çevrimdışı içerikte ${n} eksik bulundu ve tamamlanıyor (PDF, slayt eşlemesi, dosyalar).`);
    return rapor;
  })().finally(() => { suruyor = null; });
  return suruyor;
}
