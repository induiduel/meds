/**
 * Kurul seçici (2026-10-24): Kurul 1–6 sekmesi. Merkez sayfaları (Ders çalış · Soru çöz · Sınava hazırlan) ve kurula
 * bağlı araçların başında durur; öğrenci istediği kurulun içeriğine tek dokunuşla geçer.
 *
 * Seçili kurul: adresteki kurul (/…/kurulN ya da ?kurul=N) → öğrencinin son seçimi (cihazda) → takvimdeki aktif kurul
 * (services/kurulTakvimi). Son seçim takvimde yeni kurul başlayınca düşer; öğrenci yeni kurulun içeriğiyle karşılaşır.
 * İçeriği henüz olmayan kurul da seçilebilir: araç kendi boş durumunu gösterir (KurulBos). Stil: styles/kurul-suzgec.css (.ks-*)
 */
import React, { useEffect, useRef, useState } from 'react';
import { linkClick, navigateTo, type AppRoute } from '../../router';
import { KURULLAR, aktifKurul } from '../../services/kurulTakvimi';
import { kurulGizli, useSiteAyar } from '../../services/siteAyar';
import { kurulParam } from './KurulSuzgec';
import '../../styles/kurul-suzgec.css';

export const KURUL_NOLAR = [1, 2, 3, 4, 5, 6] as const;
const ANAHTAR = 'medsoru_secili_kurul';
const takvim = () => { try { return aktifKurul().kurul; } catch { return 1; } };

/** Öğrencinin son kurul seçimi; takvimde aktif kurul değiştiyse geçersiz (null) */
export function kayitliKurul(): number | null {
  try {
    const v = JSON.parse(localStorage.getItem(ANAHTAR) || 'null') as { k?: number; aktif?: number } | null;
    if (!v || v.aktif !== takvim()) return null;
    return Number.isInteger(v.k) && v.k! >= 1 && v.k! <= 6 ? v.k! : null;
  } catch { return null; }
}
export function kurulKaydet(k: number) {
  try { localStorage.setItem(ANAHTAR, JSON.stringify({ k, aktif: takvim() })); } catch { /* özel pencere */ }
}
/** Adreste kurul yoksa açılacak kurul */
export const varsayilanKurul = () => {
  const k = kayitliKurul();
  if (k && !kurulGizli(k)) return k;
  const t = takvim();
  // Panelde kapatılan kurul (kurul:<n>) varsayılan olamaz: takvimdeki kurul kapalıysa açık olan en yakın önceki kurul
  if (!kurulGizli(t)) return t;
  return [...KURUL_NOLAR].sort((a, b) => Math.abs(a - t) - Math.abs(b - t) || a - b).find((x) => !kurulGizli(x)) ?? t;
};

/** Adresteki kurul ya da varsayılan; geri/ileri ve gezinmeyle güncellenir */
export function useSeciliKurul(): number {
  const oku = () => kurulParam() ?? varsayilanKurul();
  const [k, setK] = useState(oku);
  useEffect(() => {
    const f = () => setK(oku());
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  return k;
}

/* ——— kurul başına içerik var mı (veri yüklenmez; yalnız dosya adları) ——— */

const kurulNo = (yol: string, re: RegExp) => Number(re.exec(yol)?.[1]) || 0;
const SON_PROVA = new Set(Object.keys(import.meta.glob('../../data/son_prova/k*/index.json')).map((p) => kurulNo(p, /\/k(\d+)\//)));
const CIKMIS_PAKET = new Set(Object.keys(import.meta.glob('../../data/cikmis_paket/k*.json')).map((p) => kurulNo(p, /\/k(\d+)\.json$/)));
const BRANS_VERI = new Set([1, ...Object.keys({
  ...import.meta.glob('../../data/k[2-6]*_onem/index.json'),
  ...import.meta.glob('../../data/k[2-6]*_cozucu/index.json'),
}).map((p) => kurulNo(p, /\/k(\d)[a-z]+_(?:onem|cozucu)\//))]);
/** Sınav spotlarının kurulları (data/exam_spots_k1.json) */
export const SPOT_KURULLARI = new Set([1]);

/** Aracın bu kurulda içeriği var mı; bilinmiyorsa undefined (rozet gösterilmez) */
export function kurulIcerikVar(arac: AppRoute, kurul: number): boolean | undefined {
  if (arac === 'son_prova') return SON_PROVA.has(kurul);
  if (arac === 'cikmis_cozucu') return CIKMIS_PAKET.has(kurul);
  if (arac === 'soru_cozucu' || arac === 'en_onemliler') return BRANS_VERI.has(kurul);
  if (arac === 'spots') return SPOT_KURULLARI.has(kurul);
  return undefined;
}

/* ——— görünüm ——— */

export interface KurulSeciciProps {
  /** Seçili kurul; null = "Tümü" (yalnız tumuYol verildiyse) */
  secili: number | null;
  /** Kurul sekmesinin adresi */
  yol: (k: number) => string;
  /** Tüm kurulları birlikte gösteren süzgeçsiz adres (sesli ders, çözücü listesi gibi) */
  tumuYol?: string;
  /** Kurulda içerik yoksa sekme soluk görünür (yine seçilebilir) */
  icerik?: (k: number) => boolean | undefined;
  className?: string;
}

export const KurulSecici: React.FC<KurulSeciciProps> = ({ secili, yol, tumuYol, icerik, className }) => {
  const aktif = takvim();
  // Her sayfada bir kurul her zaman seçili: adres → son seçim → takvim. Süzme (secili) ayrı, vurgu ayrı tutulur.
  useSiteAyar();
  const vurgulu = secili ?? varsayilanKurul();
  const git = (url: string, k: number | null) => linkClick(() => { if (k) kurulKaydet(k); navigateTo(url); });
  // Dar ekranda şerit kayar: seçili kurul görünür kalsın (yalnız şeridin kendisi kayar, sayfa değil)
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    const n = ref.current, on = n?.querySelector<HTMLElement>('.is-on');
    if (n && on && n.scrollWidth > n.clientWidth) n.scrollLeft = on.offsetLeft - (n.clientWidth - on.offsetWidth) / 2;
  }, [vurgulu]);
  return (
    <nav ref={ref} className={`ks${className ? ` ${className}` : ''}`} aria-label="Kurul seç">
      {tumuYol && (
        <a href={tumuYol} className="ks-k" onClick={git(tumuYol, null)}>
          Tümü
        </a>
      )}
      {KURUL_NOLAR.filter((k) => k === vurgulu || !kurulGizli(k)).map((k) => {
        const url = yol(k);
        const bos = icerik?.(k) === false;
        const ad = KURULLAR.find((x) => x.kurul === k)?.ad;
        return (
          <a
            key={k} href={url} onClick={git(url, k)}
            className={`ks-k${k === vurgulu ? ' is-on' : ''}${bos ? ' is-bos' : ''}`}
            aria-current={k === vurgulu ? 'true' : undefined}
            title={`${ad ? `Kurul ${k} · ${ad}` : `Kurul ${k}`}${bos ? ' · henüz içerik yok' : ''}`}
          >
            Kurul {k}
            {k === aktif && <small className="ks-simdi">şimdi</small>}
          </a>
        );
      })}
    </nav>
  );
};
