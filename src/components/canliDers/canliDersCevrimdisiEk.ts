/**
 * Sesli dersin çevrimdışı EK dosyaları (ses + PDF + metin dışında kalan, ders içinde internetsizken de lazım olan her şey):
 *  - Hocanın sorabileceği ara sorular (CdHocaAra): soru/çözüm/anlatım/şık klipleri + ortak klipler (/api/cozucu-ses/…)
 *  - Ders analizi / ders özeti bölüm sesleri (CdDersAnaliz, /api/cozucu-ses/k<N>dersanaliz/…)
 *  - Çıkmış soru chip'i: cümleye bağlı çıkmış soruların tam verisi (/api/past-exams/tek/<id>)
 *  - Örnek soru chip'i: derlemeye gömülü değilse canlı içerik ucu (/api/content/ornek/k<N>/<id>)
 *  - PDF terim/kısaltma yardımcısının EMA sesleri (/api/terim-ses?b=&g=)
 *  - Ders günlüğü (/api/canli-ders/<key>/gunluk), ara resim Lottie animasyonları (/ara_resim/<key>/<ad>.json)
 * Hepsi `medsoru-canli-ders-offline` önbelleğine yazılır; ses klipleri sürüm sorgusu olmadan (yol) + `X-Cd-Surum` başlığıyla
 * saklanır, sw.js aynı yolu Range/206 ile verir. JSON tam adresle saklanır; sw.js ağ yokken `onbellekte()` ile bulur.
 * Eksik ya da 404 dönen bir ek dosya indirmeyi BOZMAZ (ders sesi/PDF'i asıl; ekler "elden geldiğince").
 */
import { getCustomApiUrl } from '../../services/api';
import { klipYolu } from '../spots/cozucu/cozucuVeri';
import { hocaAraYukle } from './CdHocaAra';
import { dersAnalizYukle } from './CdDersAnaliz';
import { ornekApiAdresi, ornekSorulariYukle } from './CdOrnekChip';
import { araResimLottieYolu, araResimleri } from './araResimVeri';
import type { CdDetay } from './canliDersStore';

export interface CdEkDosya {
  /** önbellek anahtarı (ses: sorgusuz tam adres; JSON: tam adres) */
  anahtar: string;
  /** ağdan istenen adres (ses: ?v=<sürüm> ile) */
  url: string;
  tur: 'ses' | 'json';
  surum?: string;
  /** isteğe bağlı: bulunamazsa (404) sessizce geçilir */
  istege?: boolean;
}

const mutlak = (p: string) => new URL(`${(getCustomApiUrl(p) || '').replace(/\/$/, '')}${p}`, location.href).href;
const sorgusuz = (u: string) => { const x = new URL(u); x.search = ''; return x.href; };

/** Dersin internetsiz çalışması için gereken ek dosyaların listesi (yinelenenler ayıklanmış) */
export async function cdEkDosyalar(key: string, detay: CdDetay): Promise<CdEkDosya[]> {
  const out = new Map<string, CdEkDosya>();
  const ses = (yol: string, v: string) => {
    const url = mutlak(`${yol}?v=${encodeURIComponent(v)}`);
    const anahtar = sorgusuz(url);
    if (!out.has(anahtar)) out.set(anahtar, { anahtar, url, tur: 'ses', surum: v });
  };
  const json = (yol: string, istege = false) => {
    const url = mutlak(yol);
    if (!out.has(url)) out.set(url, { anahtar: url, url, tur: 'json', istege });
  };

  // 1. Hocanın sorabileceği ara sorular
  try {
    const ara = await hocaAraYukle(key);
    if (ara) {
      const klasor = ara.ders.klasor || ara.ders.kod;
      for (const [ad, k] of Object.entries(ara.ders.klip || {})) ses(klipYolu(ara.brans, 'ema', klasor, ad), k.v);
      for (const [ad, k] of Object.entries(ara.ortak || {})) ses(klipYolu(ara.brans, 'ema', 'ortak', ad), k.v);
    }
  } catch { /* ara soru yok */ }

  // 2. Ders analizi + ders özeti sesleri
  try {
    const an = await dersAnalizYukle(key);
    if (an?.sesKlasor) {
      for (const b of [...(an.analiz || []), ...(an.ozet || [])]) {
        if (b?.klip) ses(`/api/cozucu-ses/${an.sesKlasor.brans}/ema/${encodeURIComponent(an.sesKlasor.kod)}/${b.klip}.mp3`, String(b.v || ''));
      }
    }
  } catch { /* analiz yok */ }

  // 3. Çıkmış soru chip'leri (cümleye bağlı sorular; tam veri ayrı uçtan gelir)
  for (const q of detay.cikmisKonum || []) if (q?.id) json(`/api/past-exams/tek/${encodeURIComponent(q.id)}`, true);

  // 4. Örnek soru chip'i: derlemeye gömülü dosya varsa kod parçası SW'ye girer (yükleme yeter), yoksa API kopyası alınır
  try {
    await ornekSorulariYukle(key);
    const api = ornekApiAdresi(key);
    if (api) json(api, true);
  } catch { /* örnek yok */ }

  // 5. Terim / kısaltma sesleri (klip olmayan terim 404 döner: isteğe bağlı)
  const terimler = new Map<string, string>();
  for (const katman of [detay.terim, detay.kisaltma]) {
    for (const dosya of Object.values(katman || {})) {
      for (const sayfa of Object.values(dosya || {})) {
        for (const x of sayfa?.t || []) {
          const g = x.a || x.acilim || '';
          if (x.t && g && !terimler.has(`${x.t}|${g}`)) terimler.set(`${x.t}|${g}`, g);
        }
      }
    }
  }
  for (const [k, g] of terimler) {
    const b = k.slice(0, k.length - g.length - 1);
    const url = mutlak(`/api/terim-ses?b=${encodeURIComponent(b)}&g=${encodeURIComponent(g)}`);
    if (!out.has(url)) out.set(url, { anahtar: url, url, tur: 'ses', istege: true });
  }

  // 6. Günlük
  if (detay.gunlukVar) json(`/api/canli-ders/${encodeURIComponent(key)}/gunluk`, true);

  // 7. Ara resim Lottie animasyonları (SVG'ler ana indirmede)
  for (const r of araResimleri(key)) {
    const y = araResimLottieYolu(r);
    if (y) { const url = new URL(y, location.href).href; if (!out.has(url)) out.set(url, { anahtar: url, url, tur: 'json', istege: true }); }
  }

  return [...out.values()];
}

/**
 * Ek dosyalardan cihazda olmayan ya da sürümü değişenleri indirir; başarıyla yazılan anahtarları döndürür.
 * `signal` iptal eder; `ilerle(i, n)` ilerleme bildirir. Ağ hatası tek dosyayı atlatır, zinciri durdurmaz.
 */
export async function cdEkDosyalariIndir(
  cache: Cache, liste: CdEkDosya[], opts: { signal?: AbortSignal; ilerle?: (i: number, n: number) => void; esZamanli?: number } = {},
): Promise<{ yazilan: string[]; olan: string[]; hata: number }> {
  const yazilan: string[] = [];
  const olan: string[] = [];
  let hata = 0;
  let i = 0;
  const is = async (d: CdEkDosya) => {
    if (opts.signal?.aborted) return;
    try {
      const hit = await cache.match(d.anahtar);
      if (hit && (d.tur === 'json' || !d.surum || (hit.headers.get('X-Cd-Surum') || '') === d.surum)) { olan.push(d.anahtar); return; }
      const r = await fetch(d.url, { cache: 'no-store', signal: opts.signal });
      if (!r.ok) { if (!d.istege) hata++; return; }
      const blob = await r.blob();
      const headers: Record<string, string> = d.tur === 'ses'
        ? { 'Content-Type': 'audio/mpeg', 'Content-Length': String(blob.size), 'Accept-Ranges': 'bytes', 'X-Cd-Surum': d.surum || '' }
        : { 'Content-Type': r.headers.get('Content-Type') || 'application/json; charset=utf-8', 'Content-Length': String(blob.size) };
      await cache.put(d.anahtar, new Response(blob, { headers }));
      yazilan.push(d.anahtar);
    } catch (e: any) {
      if (e?.name === 'AbortError') throw e;
      hata++;
    } finally {
      i++;
      opts.ilerle?.(i, liste.length);
    }
  };
  // birkaç paralel şerit (küçük dosyalar; sunucuyu boğmadan)
  const n = Math.max(1, opts.esZamanli ?? 4);
  const kuyruk = [...liste];
  await Promise.all(Array.from({ length: n }, async () => { for (;;) { const d = kuyruk.shift(); if (!d) return; await is(d); } }));
  return { yazilan, olan, hata };
}
