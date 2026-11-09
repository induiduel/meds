/** Yedili Okey (ana mod) ve Takım Yedili kural motoru. Saf: durum düz JSON, `uygula` girdiyi değiştirmez. */
import { takimElTas } from '../tipler';
import type { Ceza, ElSatir, ElSonuc, Motor, OkeyGorunum, Olay, Per, Rng, Takim, Tas } from '../tipler';
import { bolunmus, islemeUcu, islenmis, karistir, perDiz, perTuru, sonrakiPerId, tasSeti } from './okeyOrtak';
import { planCekirdek, zorunluCekirdek } from './yediliAsistan';

export interface YediliOyuncu { id: string; takim?: Takim; el: Tas[]; acti: boolean; cezalar: Ceza[] }
export interface YediliDurum {
  tur: 'yedili' | 'takim';
  elNo: number;
  /** Oturma sırasıyla */
  oyuncular: YediliOyuncu[];
  /** Sıradaki oyuncunun oturma dizini */
  sira: number;
  /** Son eleman en üstte */
  deste: Tas[];
  perler: Per[];
  cekti: boolean;
  hamleYapti: boolean;
  /** Deste boşken art arda taş eritilmeden biten tur sayısı (kilit sayacı) */
  kuru: number;
  bitti: boolean;
  sonuc: ElSonuc | null;
}

const EL_TAS = 7;
const CEZA: Record<'islek' | 'per', Ceza> = {
  islek: { tur: 'islek', puan: -5, aciklama: 'İşlek taşı işlemedi' },
  per: { tur: 'per', puan: -5, aciklama: 'Açabileceği peri bekletti' },
};

const hak = (d: YediliDurum, i: number): boolean => {
  const o = d.oyuncular[i];
  return d.tur === 'takim' ? d.oyuncular.some((x) => x.takim === o.takim && x.acti) : o.acti;
};
const zorunluluk = (d: YediliDurum, i: number) => zorunluCekirdek(d.oyuncular[i].el, d.perler, hak(d, i));

function satir(o: YediliOyuncu, kazandi: boolean, kalanSayilir: boolean): ElSatir {
  const kalan = o.el.length, cezaTop = o.cezalar.reduce((t, c) => t + c.puan, 0);
  const parca: string[] = [];
  if (kazandi) parca.push(kalan ? `Takımı kazandı · ${kalan} taş sayılmadı` : 'Elini bitirdi');
  else parca.push(`${kalan} taş (−${kalan})`);
  if (o.cezalar.length) parca.push(`${o.cezalar.length} ceza (−${-cezaTop})`);
  return { id: o.id, puan: (kalanSayilir ? 0 - kalan : 0) + cezaTop, kalan, kazandi, cezalar: o.cezalar.slice(), aciklama: parca.join(' · ') };
}

function bitir(d: YediliDurum, olaylar: Olay[], kazanan: number | null): void {
  const k = kazanan === null ? null : d.oyuncular[kazanan];
  const kazandi = (o: YediliOyuncu) => !!k && (d.tur === 'takim' ? o.takim === k.takim : o === k);
  const kazananlar = d.oyuncular.filter(kazandi).map((o) => o.id);
  d.bitti = true;
  d.sonuc = { neden: k ? 'bitti' : 'berabere', kazananlar, satirlar: d.oyuncular.map((o) => satir(o, kazandi(o), !kazandi(o))) };
  if (k && d.tur === 'takim') d.sonuc.kazananTakim = k.takim;
  olaylar.push({ t: 'elBitti', neden: d.sonuc.neden, kazananlar });
}

/** Desteden bir taş çektirir (boşsa false); taş yalnız `kime` ile duyurulur */
function tasCek(d: YediliDurum, i: number, olaylar: Olay[]): boolean {
  const tas = d.deste.pop();
  if (!tas) return false;
  d.oyuncular[i].el.push(tas);
  olaylar.push({ t: 'cektim', kime: d.oyuncular[i].id, tas });
  return true;
}

function turBitir(d: YediliDurum, olaylar: Olay[], eritti: boolean): void {
  d.kuru = d.deste.length === 0 && !eritti ? d.kuru + 1 : 0;
  if (d.kuru >= d.oyuncular.length) return bitir(d, olaylar, null);
  d.sira = (d.sira + 1) % d.oyuncular.length;
  d.cekti = false;
  d.hamleYapti = false;
  olaylar.push({ t: 'sira', o: d.oyuncular[d.sira].id });
}

/** Takım: grup 4'e tamamlandı → rakip takımın oyuncuları (hamleyi yapandan sonraki oturma sırasıyla) birer taş çeker */
function hediye(d: YediliDurum, i: number, olaylar: Olay[]): void {
  const n = d.oyuncular.length, kimler: string[] = [], gizli: Olay[] = [];
  for (let k = 1; k < n && d.deste.length; k++) {
    const j = (i + k) % n;
    if (d.oyuncular[j].takim === d.oyuncular[i].takim) continue;
    tasCek(d, j, gizli);
    kimler.push(d.oyuncular[j].id);
  }
  if (kimler.length) olaylar.push({ t: 'hediye', o: d.oyuncular[i].id, kimler }, ...gizli);
}

const tamSayi = (x: unknown): x is number => typeof x === 'number' && Number.isInteger(x);

function motorYap(tur: 'yedili' | 'takim'): Motor {
  return {
    tur, min: 2, max: 6,

    elBaslat({ oyuncular, elNo, baslayan, rng, ayar }) {
      const n = oyuncular.length;
      if (n < 2 || n > 6) throw new Error('Oyuncu sayısı 2–6 olmalı.');
      const deste = karistir(tasSeti(), rng);
      const elTas = tur === 'takim' ? takimElTas(n, ayar?.tasSayisi) : EL_TAS;
      const d: YediliDurum = {
        tur, elNo,
        oyuncular: oyuncular.map((o, i) => ({
          id: o.id, ...(tur === 'takim' ? { takim: o.takim ?? (i % 2 ? 'B' : 'A') } : {}),
          el: deste.splice(deste.length - elTas, elTas), acti: false, cezalar: [],
        })),
        sira: (((tamSayi(baslayan) ? baslayan : 0) % n) + n) % n,
        deste, perler: [], cekti: false, hamleYapti: false, kuru: 0, bitti: false, sonuc: null,
      };
      return d;
    },

    uygula(durum, oyuncu, hamle, _rng) {
      const d = structuredClone(durum) as YediliDurum;
      if (d.bitti) return { hata: 'El bitti.' };
      const i = d.oyuncular.findIndex((o) => o.id === oyuncu);
      if (i < 0) return { hata: 'Bu masada oyuncu değilsin.' };
      if (i !== d.sira) return { hata: 'Sıra sende değil.' };
      if (!hamle || typeof hamle !== 'object') return { hata: 'Geçersiz hamle.' };
      const h = hamle as Record<string, unknown>;
      const ben = d.oyuncular[i], olaylar: Olay[] = [];
      /** Taş eridikten sonra: el bittiyse kazanır, değilse takımda 4'lenen grup hediye verdirir */
      const eridi = (per: Per) => {
        d.hamleYapti = true;
        d.kuru = 0;
        if (!ben.el.length) bitir(d, olaylar, i);
        else if (tur === 'takim' && per.tur === 'grup' && per.taslar.length === 4) hediye(d, i, olaylar);
      };

      if (h.t === 'ac') {
        const ids = h.taslar;
        if (!Array.isArray(ids) || !ids.every(tamSayi)) return { hata: 'Geçersiz hamle.' };
        if (new Set(ids).size !== ids.length) return { hata: 'Aynı taş iki kez seçilemez.' };
        const taslar = ids.map((id) => ben.el.find((t) => t.id === id));
        if (taslar.some((t) => !t)) return { hata: 'Bu taş elinde değil.' };
        const pt = perTuru(taslar as Tas[]);
        if (!pt) return { hata: 'Bu taşlar geçerli bir per değil.' };
        const per: Per = { id: sonrakiPerId(d.perler), tur: pt, taslar: perDiz(taslar as Tas[]), sahip: ben.id };
        ben.el = ben.el.filter((t) => !ids.includes(t.id));
        ben.acti = true;
        d.perler.push(per);
        olaylar.push({ t: 'acti', o: ben.id, perler: [structuredClone(per)] });
        eridi(per);
        return { durum: d, olaylar };
      }

      if (h.t === 'isle') {
        if (!tamSayi(h.tas) || !tamSayi(h.per) || (h.uc !== undefined && h.uc !== 'bas' && h.uc !== 'son')) return { hata: 'Geçersiz hamle.' };
        const tas = ben.el.find((t) => t.id === h.tas);
        if (!tas) return { hata: 'Bu taş elinde değil.' };
        if (!hak(d, i)) return { hata: 'Önce per açmalısın.' };
        const per = d.perler.find((p) => p.id === h.per);
        if (!per) return { hata: 'Böyle bir per yok.' };
        const uc = islemeUcu(tas, per);
        if (uc === undefined) return { hata: 'Bu taş o pere uymuyor.' };
        if (h.uc !== undefined && uc !== null && h.uc !== uc) return { hata: 'Bu taş perin o ucuna uymuyor.' };
        ben.el = ben.el.filter((t) => t !== tas);
        if (uc === 'bol') {
          // Seri bölünür: alt parça eski perde kalır, üst parça hamleyi yapanın yeni peri olur
          const [alt, ust] = bolunmus(per, tas);
          const yeni: Per = { id: sonrakiPerId(d.perler), tur: 'seri', taslar: ust, sahip: ben.id };
          per.taslar = alt;
          d.perler.push(yeni);
          olaylar.push({ t: 'isledi', o: ben.id, per: per.id, tas, uc, yeniPer: yeni.id });
        } else {
          per.taslar = islenmis(per, tas);
          olaylar.push({ t: 'isledi', o: ben.id, per: per.id, tas, uc });
        }
        eridi(per);
        return { durum: d, olaylar };
      }

      if (h.t === 'duzenle') {
        const gr = h.perler;
        if (!Array.isArray(gr) || !gr.length || !gr.every((x) => Array.isArray(x) && x.every(tamSayi))) return { hata: 'Geçersiz hamle.' };
        if (!hak(d, i)) return { hata: 'Masayı düzenlemek için önce per açmalısın.' };
        const masada = new Map(d.perler.flatMap((p) => p.taslar.map((t) => [t.id, t] as const)));
        const ids = gr.flat();
        if (new Set(ids).size !== ids.length) return { hata: 'Aynı taş iki pere konamaz.' };
        if (ids.some((id) => !masada.has(id))) return { hata: 'Masayı düzenlerken elden taş eklenemez.' };
        if (ids.length !== masada.size) return { hata: 'Masadaki taşlar ele geri alınamaz; her taş bir perde kalmalı.' };
        const yeni: Per[] = [];
        // Taşlarının çoğu aynı kalan per kimliğini ve sahibini korur (işleme/animasyon sürekliliği)
        const kullanilan = new Set<number>();
        for (const grup of gr) {
          const taslar = grup.map((id) => masada.get(id)!);
          const pt = perTuru(taslar);
          if (!pt) return { hata: `${taslar.map((t) => t.s).join('-')} geçerli bir per değil: her per aynı renk ardışık ya da aynı sayı farklı renk, en az 3 taş.` };
          const eski = d.perler.filter((p) => !kullanilan.has(p.id)).map((p) => ({ p, ortak: p.taslar.filter((t) => grup.includes(t.id)).length })).sort((x, y) => y.ortak - x.ortak)[0];
          const koru = eski && eski.ortak > 0 ? eski.p : null;
          if (koru) kullanilan.add(koru.id);
          yeni.push({ id: koru ? koru.id : -1, tur: pt, taslar: perDiz(taslar), sahip: koru ? koru.sahip : ben.id });
        }
        for (const p of yeni) if (p.id < 0) { p.id = Math.max(sonrakiPerId(d.perler), sonrakiPerId(yeni)); }
        d.perler = yeni;
        olaylar.push({ t: 'duzenledi', o: ben.id });
        return { durum: d, olaylar };
      }

      if (h.t !== 'cek' && h.t !== 'devret') return { hata: 'Geçersiz hamle.' };
      if (h.t === 'cek' && d.cekti) return { hata: 'Bu turda zaten taş çektin.' };
      if (h.t === 'cek' && d.hamleYapti) return { hata: 'Hamle yaptıktan sonra taş çekemezsin.' };

      const z = zorunluluk(d, i);
      if (z.islek || z.per) {
        // İhlal: her zorunluluk için ceza, bir ceza taşı, tur hemen geçer
        for (const k of ['islek', 'per'] as const) if (z[k]) {
          const ceza = { ...CEZA[k] };
          ben.cezalar.push(ceza);
          olaylar.push({ t: 'ceza', o: ben.id, ceza });
        }
        if (d.deste.length) {
          olaylar.push({ t: 'cekti', o: ben.id, cezaTasi: true });
          tasCek(d, i, olaylar);
        }
        turBitir(d, olaylar, d.hamleYapti);
        return { durum: d, olaylar };
      }

      if (h.t === 'cek') {
        d.cekti = true;
        olaylar.push({ t: 'cekti', o: ben.id, ...(d.deste.length ? {} : { bos: true }) });
        tasCek(d, i, olaylar);
        return { durum: d, olaylar };
      }
      if (!d.hamleYapti && !d.cekti) return { hata: 'Önce taş çekmelisin.' };
      olaylar.push({ t: 'devretti', o: ben.id });
      turBitir(d, olaylar, d.hamleYapti);
      return { durum: d, olaylar };
    },

    gorunum(durum, bakan) {
      const d = durum as YediliDurum;
      const g: OkeyGorunum = {
        tur: d.tur, elNo: d.elNo, sira: d.oyuncular[d.sira].id,
        oyuncular: d.oyuncular.map((o, i) => ({
          id: o.id, tasSayisi: o.el.length, acti: o.acti,
          ...(d.tur === 'takim' ? { takim: o.takim, takimActi: hak(d, i) } : {}),
          cezalar: o.cezalar.map((c) => ({ ...c })),
        })),
        elim: (d.oyuncular.find((o) => o.id === bakan)?.el ?? []).map((t) => ({ ...t })),
        perler: d.perler.map((p) => ({ ...p, taslar: p.taslar.map((t) => ({ ...t })) })),
        deste: d.deste.length,
        tur_: { cekti: d.cekti, hamleYapti: d.hamleYapti },
        bitti: d.bitti,
      };
      return g;
    },

    botHamle(durum, bot, _rng) {
      const d = durum as YediliDurum;
      if (d.bitti || d.oyuncular[d.sira].id !== bot) return null;
      const plan = planCekirdek(d.oyuncular[d.sira].el, d.perler, hak(d, d.sira), bot);
      if (plan.length) return plan[0];
      return !d.cekti && !d.hamleYapti ? { t: 'cek' } : { t: 'devret' };
    },

    sonuc(durum) {
      return (durum as YediliDurum).sonuc ?? null;
    },
  };
}

export const yediliMotor: Motor = motorYap('yedili');
export const takimMotor: Motor = motorYap('takim');
