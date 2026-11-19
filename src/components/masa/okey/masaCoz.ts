/**
 * Masayı yeniden diz: masadaki TÜM taşları (zorunlu) ve isteğe bağlı eldeki taşları geçerli perlere yeniden bölüştürür.
 * Tam örtü arar (her masa taşı tam bir perde); eldeki taşlardan olabildiğince çoğunu masaya katar.
 * Her aday per oyunun kendi doğrulayıcısıyla (gecerli) sınanır; tohum değişince farklı bir dizilim çıkar.
 * Joker (deger null) eksik yuvaya geçer.
 */
export type Deger = { s: number; r: number } | null;
interface T { id: number; d: Deger; zorunlu: boolean }

export interface CozSecenek {
  masa: number[];
  el: number[];
  /** Elden en çok kaç taş kullanılabilir (101'de atacak taş kalmalı) */
  elSinir: number;
  deger(id: number): Deger;
  gecerli(ids: number[]): boolean;
  tohum: number;
  /** Bu dizilimle aynı çıkan çözüm reddedilir (aynı perler, yalnız sıra farklıysa da aynıdır) */
  mevcut: number[][];
  adimSinir?: number;
  /** Arama süresi, ms */
  sure?: number;
}

const imza = (l: number[][]) => l.map((g) => g.slice().sort((a, b) => a - b).join(',')).sort().join('|');

export function tamCoz(o: CozSecenek): { perler: number[][]; elden: number[] } | null {
  let rnd = (o.tohum * 2654435761) >>> 0 || 1;
  const rand = () => { rnd ^= rnd << 13; rnd >>>= 0; rnd ^= rnd >> 17; rnd ^= rnd << 5; rnd >>>= 0; return rnd / 4294967296; };
  const karistir = <X,>(l: X[]) => { for (let i = l.length - 1; i > 0; i--) { const j = Math.floor(rand() * (i + 1)); [l[i], l[j]] = [l[j], l[i]]; } return l; };

  const tum: T[] = [...o.masa.map((id) => ({ id, d: o.deger(id), zorunlu: true })), ...o.el.map((id) => ({ id, d: o.deger(id), zorunlu: false }))];
  const kul = new Set<number>();
  const cozum: number[][] = [];
  const mevcut = imza(o.mevcut);
  let en: { perler: number[][]; elden: number; } | null = null;
  let adim = 0;
  const sinir = o.adimSinir ?? 8000;
  const bitis = Date.now() + (o.sure ?? 700);
  const zorunluMu = new Map(tum.map((t) => [t.id, t.zorunlu]));
  const elKul = () => { let n = 0; for (const p of cozum) for (const id of p) if (!zorunluMu.get(id)) n++; return n; };
  const gecerliOnbellek = new Map<string, boolean>();
  const gecerli = (ids: number[]) => { const k = ids.slice().sort((a, b) => a - b).join(','); let v = gecerliOnbellek.get(k); if (v === undefined) { v = o.gecerli(ids); gecerliOnbellek.set(k, v); } return v; };

  /** t taşını içeren aday perler (kullanılmamış taşlardan) */
  const adaylar = (t: T): number[][] => {
    const bos = tum.filter((x) => !kul.has(x.id) && x.id !== t.id);
    const jok = bos.filter((x) => !x.d);
    const out: number[][] = [];
    const sec = (l: T[]) => { const z = l.filter((x) => x.zorunlu); const e = l.filter((x) => !x.zorunlu); return [...karistir(z), ...karistir(e)][0]; };
    const d = t.d!;
    // Grup: aynı sayı, farklı renk (3 ya da 4); eksik renk jokerle
    const renkler = [0, 1, 2, 3].filter((r) => r !== d.r);
    for (const boy of karistir([3, 4])) {
      const kombin = (k: number, bas: number, acc: number[]): void => {
        if (acc.length === k) {
          const ids = [t.id]; let j = 0; let olur = true;
          for (const r of acc) { const x = sec(bos.filter((y) => y.d && y.d.s === d.s && y.d.r === r && !ids.includes(y.id))); if (x) ids.push(x.id); else if (j < jok.length) ids.push(jok[j++].id); else { olur = false; break; } }
          if (olur) out.push(ids);
          return;
        }
        for (let i = bas; i < renkler.length; i++) kombin(k, i + 1, [...acc, renkler[i]]);
      };
      kombin(boy - 1, 0, []);
    }
    // Seri: aynı renk ardışık, t'yi içeren [a..b]
    for (let a = Math.max(1, d.s - 12); a <= d.s; a++) for (let b = Math.max(d.s, a + 2); b <= Math.min(13, a + 12); b++) {
      const ids = [t.id]; let j = 0; let olur = true;
      for (let v = a; v <= b; v++) { if (v === d.s) continue; const x = sec(bos.filter((y) => y.d && y.d.s === v && y.d.r === d.r && !ids.includes(y.id))); if (x) ids.push(x.id); else if (j < jok.length) ids.push(jok[j++].id); else { olur = false; break; } }
      if (!olur) { if (b > d.s) break; continue; }
      out.push(ids);
    }
    return karistir(out.filter((ids) => ids.length >= 3 && gecerli(ids)));
  };

  const ara = (): boolean => {
    if (++adim > sinir || Date.now() > bitis) return true;
    const kalan = tum.filter((t) => t.zorunlu && !kul.has(t.id) && t.d);
    if (!kalan.length) {
      // Zorunlu jokerler: mevcut bir pere eklenebiliyorsa ekle
      const jk = tum.filter((t) => t.zorunlu && !kul.has(t.id));
      const ekle: [number, number][] = [];
      for (const j of jk) { const i = cozum.findIndex((p, k) => !ekle.some((e) => e[0] === k) && gecerli([...p, j.id])); if (i < 0) return false; ekle.push([i, j.id]); }
      const perler = cozum.map((p, k) => [...p, ...ekle.filter((e) => e[0] === k).map((e) => e[1])]);
      const elden = elKul();
      if (elden > o.elSinir) return false;
      if (elden === 0 && imza(perler) === mevcut) return false;
      if (!en || elden > en.elden) en = { perler, elden };
      return en.elden >= Math.min(o.elSinir, o.el.length);
    }
    // En az seçenekli taştan başla (dallanmayı küçültür)
    let secilen = kalan[0], secAday: number[][] | null = null;
    for (const t of kalan.slice(0, 6)) { const a = adaylar(t); if (!secAday || a.length < secAday.length) { secilen = t; secAday = a; } if (!a.length) return false; }
    void secilen;
    for (const p of secAday!) {
      if (p.filter((id) => !zorunluMu.get(id)).length + elKul() > o.elSinir) continue;
      p.forEach((id) => kul.add(id)); cozum.push(p);
      const bitti = ara();
      cozum.pop(); p.forEach((id) => kul.delete(id));
      if (bitti) return true;
    }
    return false;
  };
  ara();
  if (!en) return null;
  const sonuc = en as { perler: number[][]; elden: number };
  const elSet = new Set(o.el);
  return { perler: sonuc.perler, elden: sonuc.perler.flat().filter((id) => elSet.has(id)) };
}

/**
 * Güçlü arama: küçük masada önce tam çözüm; kalabalık masada (ya da tam çözüm bulunamazsa) yerel komşuluk araması —
 * mevcut geçerli dizilimden başlar, ortak renk/sayıyı paylaşan 2–4 peri ve onlarla ilgili el taşlarını küçük bir alt
 * problem olarak yeniden çözer, sonucu yerine koyar; süre bitene dek yineler. Her adım geçerli kaldığı için sonuç hep geçerlidir.
 */
export function masayiCoz(o: CozSecenek): { perler: number[][]; elden: number[] } | null {
  const toplam = o.sure ?? 1200, bas = Date.now();
  const masaSay = o.masa.length;
  let en: { perler: number[][]; elden: number[] } | null = null;
  if (masaSay <= 24) {
    en = tamCoz({ ...o, sure: Math.min(400, toplam / 2) });
    if (en && en.elden.length >= Math.min(o.elSinir, o.el.length)) return en;
  }
  let rnd = ((o.tohum + 7) * 2246822519) >>> 0 || 3;
  const rand = () => { rnd ^= rnd << 13; rnd >>>= 0; rnd ^= rnd >> 17; rnd ^= rnd << 5; rnd >>>= 0; return rnd / 4294967296; };
  const ilk = imza(o.mevcut);
  let cur = o.mevcut.map((p) => p.slice());
  let elKalan = o.el.slice();
  let elden: number[] = [];
  const ilgili = (a: number[], b: number[]) => {
    const da = a.map(o.deger).filter(Boolean) as { s: number; r: number }[], db = b.map(o.deger).filter(Boolean) as { s: number; r: number }[];
    return da.some((x) => db.some((y) => x.r === y.r || x.s === y.s));
  };
  let deneme = 0;
  while (Date.now() - bas < toplam && cur.length) {
    deneme++;
    // Çekirdek per: önce elden taş alabilecek olanlar, sonra rastgele
    const adayCekirdek = cur.map((p, i) => ({ i, puan: elKalan.some((e) => ilgili(p, [e])) ? 1 + rand() : rand() })).sort((a, b) => b.puan - a.puan);
    const ci = adayCekirdek[Math.floor(rand() * Math.min(adayCekirdek.length, 4))].i;
    const komsu = cur.map((p, i) => i).filter((i) => i !== ci && ilgili(cur[ci], cur[i]));
    for (let i = komsu.length - 1; i > 0; i--) { const j = Math.floor(rand() * (i + 1)); [komsu[i], komsu[j]] = [komsu[j], komsu[i]]; }
    const secilen = [ci, ...komsu.slice(0, 1 + Math.floor(rand() * 3))];
    const altPer = secilen.map((i) => cur[i]);
    const altEl = elKalan.filter((e) => altPer.some((p) => ilgili(p, [e])));
    const kalanSinir = o.elSinir - elden.length;
    const r = tamCoz({ ...o, masa: altPer.flat(), el: kalanSinir > 0 ? altEl : [], elSinir: Math.max(0, kalanSinir), mevcut: altPer, tohum: o.tohum * 131 + deneme, adimSinir: 2500, sure: 120 });
    if (!r) continue;
    const sec = new Set(secilen);
    cur = [...cur.filter((_, i) => !sec.has(i)), ...r.perler];
    const kul = new Set(r.elden);
    elKalan = elKalan.filter((e) => !kul.has(e));
    elden = [...elden, ...r.elden];
    // El taşları bittiyse ve masa yeterince değiştiyse erken bitir
    if ((elden.length >= Math.min(o.elSinir, o.el.length) || !elKalan.length) && deneme >= 6) break;
  }
  if (imza(cur) === ilk && !elden.length) return en;
  const yeni = { perler: cur, elden };
  return en && en.elden.length >= yeni.elden.length ? en : yeni;
}
