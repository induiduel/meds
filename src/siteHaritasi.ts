/**
 * Site haritası ve adres şeması (2026-10-21) — TEK KAYNAK. Kurallar: docs/SITE_HARITASI_KURALLARI.md
 *
 * Öğrencinin gördüğü adres "ne yapmak istiyorum" sırasıyla iç içedir:
 *
 *   /<kategori>/<araç>/kurul<N>/<branş>/<öğe>          (dersler, sorular)
 *   /kamplar/kurul<N>/<araç>/<branş|konu>/<sürüm>/<bölüm>  (kamplar: kurul önce gelir)
 *
 *   /dersler                                 Ders çalış merkezi
 *   /dersler/interaktif[/<desteId>]          Etkileşimli ders (Öğren)
 *   /dersler/canliders[/kurul1[/tbg]]        Sesli ders listesi (kurul / branş süzgeci)
 *   /dersler/canliders/kurul1/<dersKey>      Tek sesli ders
 *   /dersler/ozetler[/<id>] · /dersler/kartlar
 *   /sorular                                 Soru çöz merkezi
 *   /sorular/soru-cozucu[/kurul1/patoloji]   Sesli soru çözücü (?ders=&coz= korunur)
 *   /sorular/cikmis[/<id>] · /sorular/havuz[/<id>] · /sorular/deneme · /sorular/ornek · /sorular/olasi
 *   /kamplar[/kurul1]                        Sınava hazırlan merkezi (sekmeler: Son Prova, Kamplar, Check Up, En önemliler)
 *   /kamplar/kurul1/son-prova/...            Son Prova
 *   /kamplar/kurul1/cikmis-cozucu[/<branş>]  Çıkmış çözücü (?ders=<paket>&coz=1)
 *   /kamplar/kurul1/kamp[/<branş>]           Hoca tüyolarından kurul kampı
 *   /kamplar/kurul1/checkup/patoloji         Patoloji Check Up
 *   /kamplar/kurul1/checkup/tbg/v1/{sesli-ders,soru-coz,kaliplar,deneme}   TBG Sınav Kampı (her bölüm ayrı sayfa)
 *   /kamplar/kurul1/en-onemliler/<branş> · /kamplar/spotlar · /kamplar/sinav-plani
 *   /kaynaklar                               Başvuru merkezi (sözlük, hastalıklar … kendi düz adreslerinde kalır)
 *
 * Ekranlar ve eski bağlantılar hâlâ "iç adres" biçimini konuşur (/canliders/<key>, /soru-cozucu?brans=…,
 * /son-prova/…, /kamp/<N>/<b>, /genetik-check-up?b=…). Bu dosya iki yönü çevirir:
 *   icYol(adres)  görünen adres → iç adres (yönlendirici ve adresi kendisi okuyan ekranlar `icKonum()` kullanır)
 *   disYol(adres) iç adres → görünen adres (history.pushState/replaceState sarmalayıcısı her yazımı buna çevirir)
 * Böylece eski paylaşım bağlantıları, bildirimler ve çevrimdışı paketleri bozulmadan yeni adrese oturur.
 */

import { aktifKurul } from './services/kurulTakvimi';

/* ——— branş adres adları ——— */

/** Kurul 1 branş kimliği → adres adı (öğrencinin kullandığı ad). Kurul 2+: k2noroloji ↔ kurul2/noroloji. */
const K1_SLUG: Record<string, string> = {
  patoloji: 'patoloji', enfeksiyon: 'enfeksiyon', uroloji: 'uroloji', genetik: 'tbg',
  halksagligi: 'halk-sagligi', kadindogum: 'kadin-dogum', farmakoloji: 'farmakoloji',
};
const K1_KIMLIK: Record<string, string> = {
  ...Object.fromEntries(Object.entries(K1_SLUG).map(([k, v]) => [v, k])),
  genetik: 'genetik', halksagligi: 'halksagligi', kadindogum: 'kadindogum',
};

/** Branş kimliği (patoloji, genetik, k2noroloji) → { kurul, slug } */
export function bransAdresi(id: string): { kurul: number; slug: string } {
  const m = /^k(\d)([a-z0-9-]+)$/.exec(id);
  if (m) return { kurul: Number(m[1]), slug: m[2] };
  return { kurul: 1, slug: K1_SLUG[id] || id };
}
/** { kurul, slug } → branş kimliği; tanınmazsa null */
export function bransKimligi(kurul: number, slug: string): string | null {
  if (!/^[a-z0-9-]{2,40}$/.test(slug)) return null;
  if (kurul === 1) return K1_KIMLIK[slug] || null;
  return `k${kurul}${slug.replace(/-/g, '')}`;
}
const kurulSeg = (s: string | undefined) => {
  const m = /^kurul([1-6])$/.exec(s || '');
  return m ? Number(m[1]) : null;
};

/* ——— kategoriler (merkez sayfaları ve gezinme) ——— */

export type KategoriId = 'dersler' | 'sorular' | 'kamplar' | 'kaynaklar';

export interface KategoriTanim {
  id: KategoriId;
  yol: string;
  ad: string;
  /** Merkez sayfasında öğrenciye sorulan soru */
  soru: string;
  alt: string;
}

export const KATEGORILER: KategoriTanim[] = [
  { id: 'dersler', yol: '/dersler', ad: 'Ders çalış', soru: 'Konuyu öğrenmek istiyorum', alt: 'Dersi dinle, adım adım çalış, özetini oku' },
  { id: 'sorular', yol: '/sorular', ad: 'Soru çöz', soru: 'Soru çözmek istiyorum', alt: 'Sesli çözücü, çıkmışlar, deneme sınavı' },
  { id: 'kamplar', yol: '/kamplar', ad: 'Sınava hazırlan', soru: 'Sınav yaklaştı, toparlamak istiyorum', alt: 'Son Prova, kamplar, check-up, en önemliler' },
  { id: 'kaynaklar', yol: '/kaynaklar', ad: 'Başvuru', soru: 'Bir şeye bakmak istiyorum', alt: 'Sözlük, hastalıklar, resmî veriler' },
];

/* ——— iç adres → görünen adres ——— */

interface Ayrik { yol: string; sp: URLSearchParams; hash: string }

function ayir(adres: string): Ayrik | null {
  try {
    const base = typeof location !== 'undefined' ? location.href : 'https://x.invalid/';
    const u = new URL(adres, base);
    if (typeof location !== 'undefined' && u.origin !== location.origin) return null;
    return { yol: (u.pathname.replace(/^\/meds(?=\/|$)/, '').replace(/\/+$/, '') || '/'), sp: u.searchParams, hash: u.hash };
  } catch {
    return null;
  }
}
const birlestir = (yol: string, sp: URLSearchParams, hash: string) => {
  const q = sp.toString();
  return `${yol}${q ? `?${q}` : ''}${hash}`;
};
const enc = (s: string) => encodeURIComponent(s);
const parcala = (yol: string) => yol.split('/').filter(Boolean).map((s) => { try { return decodeURIComponent(s); } catch { return s; } });

/** Sesli ders anahtarından kurul (k2-07… → 2; önek yoksa 1) */
const anahtarKurul = (key: string) => {
  const m = /^k(\d)/.exec(key);
  return m ? Number(m[1]) : 1;
};

/** Kamplar araçlarında kurul belirtilmemişse bulunulan kamplar adresinin kurulu (aynı kurulda gezinti kopmasın) */
const mevcutKampKurulu = (): number | null => {
  try { return kurulSeg(location.pathname.split('/')[2]); } catch { return null; }
};
const sorguKurul = (sp: URLSearchParams): number | null => {
  const n = Number(sp.get('kurul'));
  return Number.isInteger(n) && n >= 1 && n <= 6 ? n : null;
};
/** Son Prova'nın kendi varsayılanı: içeriği olan en yeni kurul (spVeri.spKurullar ile aynı kural; veri yüklenmez) */
function sonProvaKurulu(): number | null {
  try {
    const l = Object.keys(import.meta.glob('./data/son_prova/k*/index.json')).map((k) => Number(/\/k(\d+)\//.exec(k)?.[1])).filter(Boolean);
    return l.length ? Math.max(...l) : null;
  } catch { return null; }
}
const takvimKurulu = (): number | null => { try { return aktifKurul().kurul; } catch { return null; } };
const kampOnek = (kurul: number | null) => `/kamplar${kurul ? `/kurul${kurul}` : ''}`;

const TBG_BOLUM: Record<string, string> = { ders: 'soru-coz', kalip: 'kaliplar', deneme: 'deneme' };
const TBG_BOLUM_TERS: Record<string, string> = { 'soru-coz': 'ders', kaliplar: 'kalip', deneme: 'deneme' };
export const TBG_YOL = '/kamplar/kurul1/checkup/tbg/v1';

/** İç (eski) adres → görünen adres. Görünen adres verilirse olduğu gibi döner. */
export function disYol(adres: string): string {
  const a = ayir(adres);
  if (!a) return adres;
  const { yol, sp, hash } = a;
  const s = parcala(yol);
  const ilk = s[0] || '';

  switch (ilk) {
    case 'ogren':
      return birlestir(`/dersler/interaktif${s[1] ? `/${enc(s[1])}` : ''}`, sp, hash);
    case 'ozetler':
      return birlestir(`/dersler/ozetler${s[1] ? `/${enc(s[1])}` : ''}`, sp, hash);
    case 'kartlar':
      return birlestir(`/dersler/kartlar${s[1] ? `/${enc(s[1])}` : ''}`, sp, hash);
    case 'canliders': {
      const k = sorguKurul(sp);
      const b = sp.get('brans');
      sp.delete('kurul'); sp.delete('brans');
      if (s[1]) return birlestir(`/dersler/canliders/kurul${anahtarKurul(s[1])}/${enc(s[1])}`, sp, hash);
      if (k && b) return birlestir(`/dersler/canliders/kurul${k}/${enc(b)}`, sp, hash);
      return birlestir(`/dersler/canliders${k ? `/kurul${k}` : ''}`, sp, hash);
    }
    case 'soru-merkezi':
      return birlestir('/sorular', sp, hash);
    case 'ders-merkezi':
      return birlestir('/dersler', sp, hash);
    case 'kaynak-merkezi':
      return birlestir('/kaynaklar', sp, hash);
    case 'soru-cozucu': {
      const b = sp.get('brans');
      sp.delete('brans');
      if (b) {
        const { kurul, slug } = bransAdresi(b);
        sp.delete('kurul');
        return birlestir(`/sorular/soru-cozucu/kurul${kurul}/${enc(slug)}`, sp, hash);
      }
      return birlestir('/sorular/soru-cozucu', sp, hash);
    }
    case 'cikmis':
      return birlestir(`/sorular/cikmis${s[1] ? `/${s.slice(1).map(enc).join('/')}` : ''}`, sp, hash);
    case 'test':
      if (s[1]) return adres; // /test/cikmis (yönetici)
      return birlestir('/sorular/deneme', sp, hash);
    case 'ornek-sorular':
      return birlestir('/sorular/ornek', sp, hash);
    case 'olasi-sorular':
      return birlestir('/sorular/olasi', sp, hash);
    case 'havuz':
      return birlestir(`/sorular/havuz${s[1] ? `/${s.slice(1).map(enc).join('/')}` : ''}`, sp, hash);
    case 'sorular': {
      // eski soru havuzu: /sorular/<soruId>; görünen /sorular/<araç>/… olduğu gibi kalır
      if (s[1] && !SORU_ARACLARI.has(s[1])) return birlestir(`/sorular/havuz/${s.slice(1).map(enc).join('/')}`, sp, hash);
      return birlestir(yol, sp, hash);
    }
    case 'kamp-merkezi': {
      const k = sorguKurul(sp);
      sp.delete('kurul');
      const sek = sp.get('sekme');
      sp.delete('sekme');
      return birlestir(`${kampOnek(k)}${sek ? `/${enc(sek)}` : ''}`, sp, hash);
    }
    case 'son-prova': {
      const k = sorguKurul(sp) ?? mevcutKampKurulu() ?? sonProvaKurulu();
      sp.delete('kurul');
      return birlestir(`${kampOnek(k)}/son-prova${s.length > 1 ? `/${s.slice(1).map(enc).join('/')}` : ''}`, sp, hash);
    }
    case 'kamp': {
      const yk = s[1] && /^[1-6]$/.test(s[1]) ? Number(s[1]) : null;
      const k = yk ?? sorguKurul(sp) ?? mevcutKampKurulu() ?? takvimKurulu();
      sp.delete('kurul');
      return birlestir(`${kampOnek(k)}/kamp${yk && s[2] ? `/${enc(s[2])}` : ''}`, sp, hash);
    }
    case 'cikmis-cozucu': {
      const b = sp.get('brans');
      sp.delete('brans');
      if (b) {
        const { kurul, slug } = bransAdresi(b);
        sp.delete('kurul');
        return birlestir(`/kamplar/kurul${kurul}/cikmis-cozucu/${enc(slug)}`, sp, hash);
      }
      const k = sorguKurul(sp) ?? mevcutKampKurulu() ?? takvimKurulu();
      sp.delete('kurul');
      return birlestir(`${kampOnek(k)}/cikmis-cozucu`, sp, hash);
    }
    case 'genetik-check-up': {
      const b = sp.get('b') || '';
      sp.delete('b');
      return birlestir(`${TBG_YOL}/${TBG_BOLUM[b] || 'sesli-ders'}`, sp, hash);
    }
    case 'patoloji-check-up': {
      const k = sorguKurul(sp) ?? 1;
      sp.delete('kurul');
      return birlestir(`/kamplar/kurul${k}/checkup/patoloji`, sp, hash);
    }
    case 'en-onemliler': {
      const b = sp.get('brans');
      sp.delete('brans');
      if (b) {
        const { kurul, slug } = bransAdresi(b);
        sp.delete('kurul');
        return birlestir(`/kamplar/kurul${kurul}/en-onemliler/${enc(slug)}`, sp, hash);
      }
      return birlestir(`${kampOnek(mevcutKampKurulu())}/en-onemliler`, sp, hash);
    }
    case 'sinav-plani':
      return birlestir('/kamplar/sinav-plani', sp, hash);
    case 'spotlar':
      if (sp.get('gorunum')) return adres; // eski /spotlar?gorunum=… ExamSpotsView'da yönlenir
      return birlestir('/kamplar/spotlar', sp, hash);
    default:
      return adres;
  }
}

/** /sorular/<x> altında araç olan adlar (gerisi eski havuz soru kimliğidir) */
const SORU_ARACLARI = new Set(['soru-cozucu', 'cikmis', 'havuz', 'deneme', 'ornek', 'olasi']);

/* ——— görünen adres → iç adres ——— */

/** Görünen adres → iç adres. İç adres verilirse olduğu gibi döner. */
export function icYol(adres: string): string {
  const a = ayir(adres);
  if (!a) return adres;
  const { yol, sp, hash } = a;
  const s = parcala(yol);
  const ilk = s[0] || '';
  // yol parçasından gelen değer sorguda açıkça verilmiş olanı ezmez
  const koy = (k: string, v: string | number | null | undefined) => { if (v != null && v !== '' && !sp.has(k)) sp.set(k, String(v)); };

  if (ilk === 'dersler') {
    const arac = s[1];
    if (!arac) return birlestir('/ders-merkezi', sp, hash);
    if (arac === 'interaktif') return birlestir(`/ogren${s[2] && !kurulSeg(s[2]) ? `/${enc(s[2])}` : s[3] ? `/${enc(s[3])}` : ''}`, sp, hash);
    if (arac === 'ozetler') return birlestir(`/ozetler${s[2] ? `/${enc(s[2])}` : ''}`, sp, hash);
    if (arac === 'kartlar') return birlestir(`/kartlar${s[2] ? `/${enc(s[2])}` : ''}`, sp, hash);
    if (arac === 'canliders' || arac === 'sesli-ders') {
      const k = kurulSeg(s[2]);
      if (!k) return birlestir(`/canliders${s[2] ? `/${enc(s[2])}` : ''}`, sp, hash);
      const sonraki = s[3];
      // kurulN/<branş>[/<key>] ya da kurulN/<key>
      if (sonraki && bransKimligi(k, sonraki) && !s[4] && !/^k\d-/.test(sonraki)) {
        koy('kurul', k); koy('brans', sonraki);
        return birlestir('/canliders', sp, hash);
      }
      const key = s[4] || sonraki;
      if (key) return birlestir(`/canliders/${enc(key)}`, sp, hash);
      koy('kurul', k);
      return birlestir('/canliders', sp, hash);
    }
    return birlestir('/ders-merkezi', sp, hash);
  }

  if (ilk === 'sorular') {
    const arac = s[1];
    if (!arac) return birlestir('/soru-merkezi', sp, hash);
    if (arac === 'soru-cozucu') {
      const k = kurulSeg(s[2]);
      if (k && s[3]) koy('brans', bransKimligi(k, s[3]) || s[3]);
      else if (k) koy('kurul', k);
      return birlestir('/soru-cozucu', sp, hash);
    }
    if (arac === 'cikmis') return birlestir(`/cikmis${s[2] ? `/${s.slice(2).map(enc).join('/')}` : ''}`, sp, hash);
    if (arac === 'havuz') return birlestir(`/havuz${s[2] ? `/${s.slice(2).map(enc).join('/')}` : ''}`, sp, hash);
    if (arac === 'deneme') return birlestir('/test', sp, hash);
    if (arac === 'ornek') return birlestir(`/ornek-sorular${s[2] ? `/${enc(s[2])}` : ''}`, sp, hash);
    if (arac === 'olasi') return birlestir('/olasi-sorular', sp, hash);
    // eski havuz soru bağlantısı /sorular/<soruId>
    return birlestir(`/havuz/${s.slice(1).map(enc).join('/')}`, sp, hash);
  }

  if (ilk === 'kamplar') {
    let i = 1;
    const k = kurulSeg(s[1]);
    if (k) i = 2;
    const arac = s[i];
    const geri = s.slice(i + 1);
    if (!arac || (arac === 'checkup' && !geri.length)) {
      koy('kurul', k);
      if (arac) koy('sekme', arac);
      return birlestir('/kamp-merkezi', sp, hash);
    }
    if (arac === 'son-prova') {
      koy('kurul', k);
      return birlestir(`/son-prova${geri.length ? `/${geri.map(enc).join('/')}` : ''}`, sp, hash);
    }
    if (arac === 'cikmis-cozucu') {
      if (geri[0]) koy('brans', bransKimligi(k || 1, geri[0]) || geri[0]);
      koy('kurul', k);
      return birlestir('/cikmis-cozucu', sp, hash);
    }
    if (arac === 'kamp') {
      if (geri[0]) return birlestir(`/kamp/${k || 1}/${enc(geri[0])}`, sp, hash);
      koy('kurul', k);
      return birlestir('/kamp', sp, hash);
    }
    if (arac === 'checkup') {
      if (geri[0] === 'patoloji') { koy('kurul', k); return birlestir('/patoloji-check-up', sp, hash); }
      if (geri[0] === 'tbg' || geri[0] === 'genetik') {
        const b = TBG_BOLUM_TERS[geri[2] || ''];
        if (b) koy('b', b);
        return birlestir('/genetik-check-up', sp, hash);
      }
      koy('kurul', k); koy('sekme', 'checkup');
      return birlestir('/kamp-merkezi', sp, hash);
    }
    if (arac === 'en-onemliler') {
      if (geri[0]) koy('brans', bransKimligi(k || 1, geri[0]) || geri[0]);
      return birlestir('/en-onemliler', sp, hash);
    }
    if (arac === 'spotlar') return birlestir('/spotlar', sp, hash);
    if (arac === 'sinav-plani') return birlestir('/sinav-plani', sp, hash);
    koy('kurul', k);
    return birlestir('/kamp-merkezi', sp, hash);
  }

  if (ilk === 'kaynaklar') return birlestir('/kaynak-merkezi', sp, hash);
  return adres;
}

/** Her iki biçimden de tek görünen adres */
export const kanonik = (adres: string) => disYol(icYol(adres));

/** Bulunulan sayfanın iç adresi — adresi kendisi okuyan ekranlar window.location yerine bunu kullanır */
export function icKonum(): { pathname: string; search: string; hash: string } {
  try {
    const u = new URL(icYol(location.pathname + location.search + location.hash), location.origin);
    return { pathname: u.pathname, search: u.search, hash: u.hash };
  } catch {
    return { pathname: '/', search: '', hash: '' };
  }
}

/**
 * history.pushState / replaceState sarmalayıcısı: ekranlar hangi biçimde yazarsa yazsın adres çubuğunda görünen
 * adres olur. main.tsx'te uygulama kurulmadan önce bir kez çağrılır.
 */
export function adresKatmaniniKur() {
  if (typeof window === 'undefined' || (window as unknown as { __adresKatmani?: 1 }).__adresKatmani) return;
  (window as unknown as { __adresKatmani?: 1 }).__adresKatmani = 1;
  for (const ad of ['pushState', 'replaceState'] as const) {
    const asil = history[ad].bind(history);
    history[ad] = ((veri: unknown, baslik: string, url?: string | URL | null) => {
      if (url != null && url !== '') {
        try {
          const ham = typeof url === 'string' ? url : url.toString();
          const u = new URL(ham, location.href);
          if (u.origin === location.origin) url = kanonik(u.pathname + u.search + u.hash);
        } catch { /* olduğu gibi yaz */ }
      }
      return asil(veri, baslik, url);
    }) as History['pushState'];
  }
  // Açılışta eski biçimli adres (bildirim, paylaşım, yer imi) görünen adrese döner
  try {
    const simdi = location.pathname + location.search + location.hash;
    const yeni = kanonik(simdi);
    if (yeni !== simdi) history.replaceState(history.state, '', yeni);
  } catch { /* yok */ }
}

/** Bulunulan sayfanın iç adresi URL olarak — parametre ekleyip silen ekranlar `new URL(location.href)` yerine bunu kullanır */
export function icUrl(): URL {
  const k = icKonum();
  return new URL(k.pathname + k.search + k.hash, location.origin);
}
