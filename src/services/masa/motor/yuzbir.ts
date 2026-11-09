/**
 * 101 Okey kural motoru (jokerli). Saf: durum düz JSON, `uygula` girdiyi değiştirmez, kural dışı her hamle `{ hata }`.
 * Kuralların ortak parçaları (per çözümü, işleme yerleri, açılış araması, bot kararı) `yuzbirAsistan.ts`'tedir.
 *
 * Taş kimliği: r*26 + (s-1)*2 + kopya (0–103); sahte okeyler 104–105 (s=0).
 */
import type { Ceza, ElSatir, ElSonuc, Motor, OkeyGorunum, Olay, Per, Renk, Tas } from '../tipler';
import { ACILIS_CIFT, ACILIS_ESIK, botSec, elDegeri, etkin, gercek, islemeYerleri, jokerMi, okeyBul, perCoz, type Okey } from './yuzbirAsistan';

export interface YuzbirOyuncu {
  id: string;
  el: Tas[];
  acti: boolean;
  ciftActi: boolean;
  cezalar: Ceza[];
  /** Attığı taşlar (son eleman en üstte) */
  atiklar: Tas[];
}

export interface YuzbirDurum {
  tur: 'yuzbir';
  elNo: number;
  oyuncular: YuzbirOyuncu[];
  /** Sırası olan oyuncunun dizini */
  sira: number;
  /** Son eleman en üstte */
  deste: Tas[];
  gosterge: Tas;
  okey: Okey;
  perler: Per[];
  perNo: number;
  cekti: boolean;
  hamleYapti: boolean;
  /** Bu turda yandan alınan ve henüz kullanılmayan taş */
  yandanAlinan: number | null;
  /** Sıradaki oyuncu bu turda açtı (elden bitme) */
  buTurActi: boolean;
  sonuc: ElSonuc | null;
}

const CEZA = -101;
const eksi = (n: number) => `−${n}`;
const tam = (x: unknown): x is number => typeof x === 'number' && Number.isInteger(x);

function elBitir(d: YuzbirDurum, neden: 'bitti' | 'deste', kazanan: number, olaylar: Olay[]): void {
  const elden = neden === 'bitti' && d.buTurActi;
  const satirlar: ElSatir[] = d.oyuncular.map((o, i) => {
    const cezaTop = o.cezalar.reduce((a, c) => a + c.puan, 0);
    const parca: string[] = [];
    let puan: number;
    if (i === kazanan) {
      puan = elden ? 202 : 101;
      parca.push(elden ? 'Elden bitti (+202)' : 'Bitirdi (+101)');
    } else {
      let kayip: number;
      if (!o.acti) { kayip = 202; parca.push('Açmadı'); }
      else {
        kayip = elDegeri(o.el, d.okey) * (o.ciftActi ? 2 : 1);
        parca.push(`${o.el.length} taş`);
        if (o.ciftActi) parca.push('çiftle açtı ×2');
      }
      if (elden) { kayip *= 2; parca.push('elden bitme ×2'); }
      puan = -kayip;
      parca[0] += ` (${eksi(kayip)})`;
    }
    if (o.cezalar.length) parca.push(`${o.cezalar.length} ceza (${eksi(-cezaTop)})`);
    return { id: o.id, puan: puan + cezaTop, kalan: o.el.length, kazandi: i === kazanan, cezalar: o.cezalar, aciklama: parca.join(' · ') };
  });
  d.sonuc = { neden, kazananlar: kazanan >= 0 ? [d.oyuncular[kazanan].id] : [], satirlar };
  olaylar.push({ t: 'elBitti', neden, kazananlar: d.sonuc.kazananlar });
}

/** Elden taşları çıkarır (hepsi eldeyse); değilse null ve el değişmez */
function eldenAl(o: YuzbirOyuncu, ids: number[]): Tas[] | null {
  const al = new Set(ids);
  if (al.size !== ids.length) return null;
  const alinan = ids.map((id) => o.el.find((t) => t.id === id));
  if (alinan.some((t) => !t)) return null;
  o.el = o.el.filter((t) => !al.has(t.id));
  return alinan as Tas[];
}

export const yuzbirMotor: Motor = {
  tur: 'yuzbir',
  min: 2,
  max: 4,

  elBaslat({ oyuncular, elNo, baslayan, rng }): YuzbirDurum {
    const n = oyuncular.length;
    if (n < 2 || n > 4) throw new Error('101 Okey 2–4 oyuncuyla oynanır.');
    const deste: Tas[] = [];
    for (let r = 0; r < 4; r++) for (let s = 1; s <= 13; s++) for (let k = 0; k < 2; k++) deste.push({ id: r * 26 + (s - 1) * 2 + k, s, r: r as Renk });
    deste.push({ id: 104, s: 0, r: 0 }, { id: 105, s: 0, r: 0 });
    for (let i = deste.length - 1; i > 0; i--) {
      const j = Math.min(i, Math.floor(rng() * (i + 1)));
      [deste[i], deste[j]] = [deste[j], deste[i]];
    }
    // Gösterge: üstten ilk sahte olmayan taş
    let gi = deste.length - 1;
    while (deste[gi].s === 0) gi--;
    const [gosterge] = deste.splice(gi, 1);
    const ilk = ((baslayan % n) + n) % n;
    const liste: YuzbirOyuncu[] = oyuncular.map((o, i) => ({ id: o.id, el: deste.splice(deste.length - (i === ilk ? 22 : 21)), acti: false, ciftActi: false, cezalar: [], atiklar: [] }));
    return {
      tur: 'yuzbir', elNo, oyuncular: liste, sira: ilk, deste, gosterge, okey: okeyBul(gosterge), perler: [], perNo: 1,
      cekti: true, hamleYapti: false, yandanAlinan: null, buTurActi: false, sonuc: null,
    };
  },

  uygula(durum, oyuncu, hamle) {
    const d0 = durum as YuzbirDurum;
    if (d0.sonuc) return { hata: 'El bitti.' };
    const oi = d0.oyuncular.findIndex((o) => o.id === oyuncu);
    if (oi < 0) return { hata: 'Bu masada oyuncu değilsin.' };
    if (oi !== d0.sira) return { hata: 'Sıra sende değil.' };
    if (!hamle || typeof hamle !== 'object' || Array.isArray(hamle)) return { hata: 'Geçersiz hamle.' };
    const h = hamle as Record<string, unknown>;
    const d = structuredClone(d0);
    const o = d.oyuncular[oi];
    const n = d.oyuncular.length;
    const okey = d.okey;
    const olaylar: Olay[] = [];
    const bitti = () => ({ durum: d, olaylar });
    const yandanKullan = (ids: number[]) => { if (d.yandanAlinan !== null && ids.includes(d.yandanAlinan)) d.yandanAlinan = null; };
    const perEkle = (c: { tur: Per['tur']; taslar: Tas[] }): Per => {
      const p: Per = { id: d.perNo++, tur: c.tur, taslar: c.taslar, sahip: o.id };
      d.perler.push(p);
      return p;
    };

    switch (h.t) {
      case 'cek': {
        if (d.cekti) return { hata: 'Bu turda zaten taş çektin.' };
        const kaynak = h.kaynak ?? 'deste';
        if (kaynak === 'deste') {
          const tas = d.deste.pop();
          if (!tas) { elBitir(d, 'deste', -1, olaylar); return bitti(); }
          o.el.push(tas);
          d.cekti = true;
          olaylar.push({ t: 'cekti', o: o.id, kaynak: 'deste' }, { t: 'cektim', kime: o.id, tas });
          return bitti();
        }
        if (kaynak !== 'atik') return { hata: 'Taş desteden ya da yandan (önceki oyuncunun attığı taş) çekilir.' };
        const tas = d.oyuncular[(oi - 1 + n) % n].atiklar.pop();
        if (!tas) return { hata: 'Yanında alınacak taş yok; desteden çek.' };
        o.el.push(tas);
        d.cekti = true;
        d.yandanAlinan = tas.id;
        olaylar.push({ t: 'cekti', o: o.id, kaynak: 'atik', tas });
        return bitti();
      }

      case 'geriKoy': {
        const id = d.yandanAlinan;
        if (id === null) return { hata: 'Geri koyulacak taş yok: bu turda yandan taş almadın ya da aldığın taşı kullandın.' };
        const [tas] = eldenAl(o, [id]) ?? [];
        if (!tas) return { hata: 'Yandan aldığın taş elinde değil.' };
        d.oyuncular[(oi - 1 + n) % n].atiklar.push(tas);
        d.yandanAlinan = null;
        olaylar.push({ t: 'geriKoydu', o: o.id, tas });
        const yeni = d.deste.pop();
        if (!yeni) { elBitir(d, 'deste', -1, olaylar); return bitti(); }
        o.el.push(yeni);
        olaylar.push({ t: 'cekti', o: o.id, kaynak: 'deste' }, { t: 'cektim', kime: o.id, tas: yeni });
        return bitti();
      }

      case 'ac101': {
        if (!d.cekti) return { hata: 'Önce taş çekmelisin.' };
        if (o.acti) return { hata: 'Zaten açtın; yeni per için tek tek per aç.' };
        const perler = h.perler;
        if (!Array.isArray(perler) || !perler.length || perler.length > 11) return { hata: 'Açılış için perlerini seçmelisin.' };
        const tum: number[] = [];
        for (const p of perler) {
          if (!Array.isArray(p) || p.length < 2 || p.length > 13 || !p.every(tam)) return { hata: 'Her per en az 2 taştan (çift) ya da 3–13 taştan (seri/grup) oluşur.' };
          tum.push(...(p as number[]));
        }
        if (new Set(tum).size !== tum.length) return { hata: 'Aynı taş iki perde kullanılamaz.' };
        if (tum.some((id) => !o.el.some((t) => t.id === id))) return { hata: 'Seçtiğin taşlardan biri elinde değil.' };
        const coz: NonNullable<ReturnType<typeof perCoz>>[] = [];
        for (let k = 0; k < perler.length; k++) {
          const c = perCoz((perler[k] as number[]).map((id) => o.el.find((t) => t.id === id) as Tas), okey);
          if (!c) return { hata: `${k + 1}. per geçerli değil: seri (aynı renk ardışık), grup (aynı sayı farklı renk) ya da çift (özdeş iki taş) olmalı; bir perde en az 2 gerçek taş bulunur.` };
          coz.push(c);
        }
        const ciftSay = coz.filter((c) => c.tur === 'cift').length;
        if (ciftSay && ciftSay !== coz.length) return { hata: 'Açılışta çiftlerle seri/gruplar karıştırılamaz: ya hepsi seri/grup (toplam 101) ya hepsi çift (en az 5).' };
        if (ciftSay && ciftSay < ACILIS_CIFT) return { hata: `Çiftle açmak için en az ${ACILIS_CIFT} çift gerekir (şu an ${ciftSay}).` };
        const toplam = coz.reduce((a, c) => a + c.deger, 0);
        if (!ciftSay && toplam < ACILIS_ESIK) return { hata: `Açmak için perlerin toplamı en az ${ACILIS_ESIK} olmalı (şu an ${toplam}).` };
        if (tum.length >= o.el.length) return { hata: 'Atacak bir taş bırakmalısın.' };
        eldenAl(o, tum);
        o.acti = true;
        o.ciftActi = ciftSay > 0;
        d.buTurActi = true;
        d.hamleYapti = true;
        yandanKullan(tum);
        olaylar.push({ t: 'acti', o: o.id, perler: coz.map(perEkle) });
        return bitti();
      }

      case 'ac': {
        if (!d.cekti) return { hata: 'Önce taş çekmelisin.' };
        if (!o.acti) return { hata: 'Henüz açmadın: önce 101 ile ya da 5 çiftle açmalısın.' };
        const ids = h.taslar;
        if (!Array.isArray(ids) || ids.length < 2 || ids.length > 13 || !ids.every(tam)) return { hata: 'Per için taşlarını seçmelisin.' };
        if (new Set(ids).size !== ids.length) return { hata: 'Aynı taş iki kez seçilemez.' };
        const taslar = (ids as number[]).map((id) => o.el.find((t) => t.id === id));
        if (taslar.some((t) => !t)) return { hata: 'Seçtiğin taşlardan biri elinde değil.' };
        const c = perCoz(taslar as Tas[], okey);
        if (!c) return { hata: 'Bu taşlar per olmuyor: seri (aynı renk ardışık), grup (aynı sayı farklı renk) ya da çift olmalı.' };
        if (o.ciftActi && c.tur !== 'cift') return { hata: 'Çiftle açtın; yalnız yeni çift açabilirsin.' };
        if (!o.ciftActi && c.tur === 'cift') return { hata: 'Seri/grupla açtın; çift açamazsın.' };
        if (ids.length >= o.el.length) return { hata: 'Atacak bir taş bırakmalısın.' };
        eldenAl(o, ids as number[]);
        d.hamleYapti = true;
        yandanKullan(ids as number[]);
        olaylar.push({ t: 'acti', o: o.id, perler: [perEkle(c)] });
        return bitti();
      }

      case 'isle': {
        if (!d.cekti) return { hata: 'Önce taş çekmelisin.' };
        if (!o.acti) return { hata: 'Taş işlemek için önce açmalısın.' };
        if (!tam(h.tas) || !tam(h.per)) return { hata: 'İşlenecek taşı ve peri seçmelisin.' };
        if (h.uc !== undefined && h.uc !== 'bas' && h.uc !== 'son') return { hata: 'Uç yalnız baş ya da son olabilir.' };
        const tas = o.el.find((t) => t.id === h.tas);
        if (!tas) return { hata: 'Bu taş elinde değil.' };
        const per = d.perler.find((p) => p.id === h.per);
        if (!per) return { hata: 'Böyle bir per yok.' };
        if (per.tur === 'cift') return { hata: 'Çifte taş işlenmez.' };
        const yerler = islemeYerleri(tas, [per], okey);
        if (!yerler.length) return { hata: 'Bu taş bu pere işlenmez: seride uçlara, üçlü gruba eksik renk eklenir.' };
        let yer = yerler[0];
        if (per.tur === 'seri') {
          if (h.uc) {
            const sec = yerler.find((y) => y.uc === h.uc);
            if (!sec) return { hata: 'Taş serinin bu ucuna uymuyor.' };
            yer = sec;
          } else if (yerler.length > 1) return { hata: 'Okey serinin iki ucuna da uyuyor: başa mı sona mı koyacağını seç.' };
        }
        if (o.el.length < 2) return { hata: 'Atacak bir taş bırakmalısın.' };
        eldenAl(o, [tas.id]);
        const joker = jokerMi(tas, okey);
        const koy = (s: number, r: Renk): Tas => (joker ? { id: tas.id, s: tas.s, r: tas.r, yerine: { s, r } } : { id: tas.id, s: tas.s, r: tas.r });
        if (per.tur === 'seri') {
          const a = etkin(per.taslar[0], okey);
          if (yer.uc === 'bas') per.taslar.unshift(koy(a.s - 1, a.r));
          else per.taslar.push(koy(etkin(per.taslar[per.taslar.length - 1], okey).s + 1, a.r));
        } else {
          const s = etkin(per.taslar[0], okey).s;
          const dolu = per.taslar.map((t) => etkin(t, okey).r);
          const r = gercek(tas, okey)?.r ?? ([0, 1, 2, 3] as Renk[]).find((q) => !dolu.includes(q)) ?? 0;
          per.taslar.push(koy(s, r));
          per.taslar.sort((x, y) => etkin(x, okey).r - etkin(y, okey).r);
        }
        d.hamleYapti = true;
        yandanKullan([tas.id]);
        olaylar.push({ t: 'isledi', o: o.id, per: per.id, tas, uc: yer.uc });
        return bitti();
      }

      case 'at': {
        if (!d.cekti) return { hata: 'Önce taş çekmelisin.' };
        if (!tam(h.tas)) return { hata: 'Atılacak taşı seçmelisin.' };
        const tas = o.el.find((t) => t.id === h.tas);
        if (!tas) return { hata: 'Bu taş elinde değil.' };
        if (d.yandanAlinan !== null) return { hata: 'Yandan aldığın taşı kullanmalı ya da geri koymalısın.' };
        eldenAl(o, [tas.id]);
        o.atiklar.push(tas);
        olaylar.push({ t: 'atti', o: o.id, tas });
        if (!o.el.length) { elBitir(d, 'bitti', oi, olaylar); return bitti(); }
        const ceza: Ceza | null = jokerMi(tas, okey)
          ? { tur: 'okeyAtti', puan: CEZA, aciklama: 'Okey attı' }
          : islemeYerleri(tas, d.perler, okey).length ? { tur: 'islekAtti', puan: CEZA, aciklama: 'İşlek taş attı' } : null;
        if (ceza) { o.cezalar.push(ceza); olaylar.push({ t: 'ceza', o: o.id, ceza }); }
        d.sira = (oi + 1) % n;
        d.cekti = false;
        d.hamleYapti = false;
        d.buTurActi = false;
        olaylar.push({ t: 'sira', o: d.oyuncular[d.sira].id });
        return bitti();
      }

      default:
        return { hata: 'Bu oyunda böyle bir hamle yok.' };
    }
  },

  gorunum(durum, bakan): OkeyGorunum {
    const d = durum as YuzbirDurum;
    return {
      tur: 'yuzbir',
      elNo: d.elNo,
      sira: d.oyuncular[d.sira].id,
      oyuncular: d.oyuncular.map((o) => ({ id: o.id, tasSayisi: o.el.length, acti: o.acti, ciftActi: o.ciftActi, cezalar: o.cezalar.slice(), atiklar: o.atiklar.slice() })),
      elim: d.oyuncular.find((o) => o.id === bakan)?.el.slice() ?? [],
      perler: d.perler.map((p) => ({ ...p, taslar: p.taslar.slice() })),
      deste: d.deste.length,
      tur_: { cekti: d.cekti, hamleYapti: d.hamleYapti },
      gosterge: d.gosterge,
      okey: d.okey,
      ...(d.yandanAlinan !== null ? { yandanAlinan: d.yandanAlinan } : {}),
      bitti: !!d.sonuc,
    };
  },

  botHamle(durum, bot) {
    const d = durum as YuzbirDurum;
    if (d.sonuc) return null;
    const o = d.oyuncular[d.sira];
    if (o.id !== bot) return null;
    const n = d.oyuncular.length;
    const atik = d.oyuncular[(d.sira - 1 + n) % n].atiklar;
    const hamle = botSec({
      el: o.el, okey: d.okey, perler: d.perler, acti: o.acti, ciftActi: o.ciftActi, cekti: d.cekti,
      yandanAlinan: d.yandanAlinan, oncekiAtik: atik[atik.length - 1] ?? null, deste: d.deste.length,
    });
    if (!('hata' in yuzbirMotor.uygula(d, bot, hamle, Math.random))) return hamle;
    // Emniyet: bot asla takılmaz
    if (!d.cekti) return { t: 'cek', kaynak: 'deste' };
    if (d.yandanAlinan !== null) return { t: 'geriKoy' };
    return { t: 'at', tas: o.el[0].id };
  },

  sonuc(durum) {
    return (durum as YuzbirDurum).sonuc;
  },
};
