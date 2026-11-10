/**
 * Taş Masası oda sunucusu: /api/masa/ws (WebSocket) + /api/masa/* (REST). Motordan bağımsızdır; kuralın tamamı motor/<oyun>.ts'te.
 *
 * - Kimlik: ilk mesaj `gir {jeton}` (MeDSor erişim jetonu, yerelde HMAC ile doğrulanır). Oyuncu kimliği = açık profil kimliği (uid dışarı çıkmaz).
 * - Her değişiklikte her oyuncuya KENDİ görünümü (`durum`) + o hamlenin olayları gider; istemci ekranı yalnız son görünümden çizer.
 * - Odalar RAM'dedir, 1 sn gecikmeli meds-pg `masa_oda`'ya yazılır; sunucu yeniden başlayınca (dağıtım) oyunlar kaldığı yerden sürer.
 * - El sonuçları `masa_el` / `masa_el_oyuncu` (genel ve rakibe göre istatistik).
 * - Botlar sunucuda oynar (motor.botHamle); odada bağlı insan yokken bot yürümez. LLM, zamanlanmış iş yok.
 */
import { createRequire } from 'module';
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import type express from 'express';
import { pgDb } from '../pgDb';
import { verifiedUid } from '../adminAuth';
import { erisimJetonuDogrula } from '../kimlikDogrulama';
import { bayrakAcik } from '../yonetim16/siteAyar';
import { MOTORLAR } from './motorlar';
import {
  EL_SECENEK, OKEY_TEMALAR, OYUNCU_SINIR, OYUN_ADI, TEPKILER, UNO_TEMALAR, VARSAYILAN_RENKLER, UNO_MODLAR, GO_SURELER,
  type ElOzet, type ElSonuc, type Istatistik, type IstemciMesaj, type OdaAsama, type OdaAyar, type OdaGorunum, type OdaOzet,
  type Olay, type OyunTur, type Rng, type SunucuMesaj, type Takim,
} from './tipler';

const require = createRequire(import.meta.url);
const wsModule = require('ws');
const WebSocketServer = wsModule.Server || wsModule.WebSocketServer;

interface Koltuk { id: string; uid: string | null; ad: string; bot: boolean; takim?: Takim; foto?: string }
interface Oda {
  kod: string; tur: OyunTur; ayar: OdaAyar; asama: OdaAsama; durdu: boolean; kurucu: string;
  oyuncular: Koltuk[]; elNo: number; baslayan: number; durum: unknown | null; elSonuc?: ElSonuc;
  skor: Record<string, number>; eller: ElOzet[]; surum: number; olusturma: number; guncel: number;
  /** Geri al: sırası olan oyuncunun bu turdaki per açma / işleme hamlelerinden önceki durumlar (son eleman en yeni) */
  geri?: { kim: string; durumlar: unknown[] };
  /** Durdurulduğu an (süreli oyunda saat durakta işlemesin) */
  durduZ?: number;
  /** Koltuk devri: izleyicinin bağlantı kimliği → oturduğu (eski bot) koltuk kimliği */
  devir?: Record<string, string>;
}
interface Bag { ws: any; uid: string; id: string; ad: string; kod: string | null; son: number; sayac: number; pencere: number }
interface Deps {
  rootDir: string;
  isPgOnline: () => boolean;
  kisiKimlik: (uid: string) => string;
  kisiAd: (uid: string) => string;
  foto?: (uid: string) => string | undefined;
  /** Açık profil kimliği → uid (davet için) */
  uidBul: (kimlik: string) => string | null;
  notifyStudent: (target: { uid?: string | null }, n: { type: string; title: string; message: string; deepLinkUrl?: string; dedupeKey?: string }) => unknown;
}

const TURLER: OyunTur[] = ['yedili', 'takim', 'yuzbir', 'uno', 'go', 'cizgi', 'xox', 'remi', 'kastet', 'duz', 'pisti', 'domino'];
const BOT_ADLARI = ['Defne', 'Aras', 'Mira', 'Kaan', 'Ece', 'Poyraz', 'Lina'];
const KOD = /^[A-Z0-9]{5}$/;
const HEX = /^#[0-9a-f]{6}$/i;
const rng: Rng = () => crypto.randomInt(0x100000000) / 0x100000000;
const kodUret = () => Array.from({ length: 5 }, () => 'ABCDEFGHJKLMNPRSTUVYZ23456789'[crypto.randomInt(29)]).join('');
const temiz = (s: unknown, n: number) => String(s ?? '').replace(/[\u0000-\u001f<>]/g, '').trim().slice(0, n);
const GUN = 86_400_000;

class MasaSunucu {
  private wss: any = null;
  private odalar = new Map<string, Oda>();
  /** kod → oyuncu kimliği → bağlantı */
  private baglar = new Map<string, Map<string, Bag>>();
  private tum = new Set<Bag>();
  private botZaman = new Map<string, any>();
  private sureZaman = new Map<string, any>();
  /** kod → izleyici bağlantı kimliği → ad + istediği bot koltuğu (oyun başlamışken gelenler) */
  private izleyici = new Map<string, Map<string, { ad: string; istek?: string }>>();
  /** `kod:koltuk` → bağlantının koptuğu an */
  private kopZ = new Map<string, number>();
  private kayitZaman = new Map<string, any>();
  private d!: Deps;
  private sema = false;
  private yuklendi = false;

  /* ------------------------------------------------------------ kurulum ------------------------------------------------------------ */

  initialize(server: any, d: Deps) {
    if (!server || this.wss) return;
    this.d = d;
    this.wss = new WebSocketServer({ noServer: true, maxPayload: 16 * 1024 });
    server.on('upgrade', (request: any, socket: any, head: any) => {
      const url = new URL(request.url || '', `http://${request.headers.host || 'localhost'}`);
      if (url.pathname !== '/api/masa/ws') return;
      this.wss.handleUpgrade(request, socket, head, (ws: any) => this.baglan(ws));
    });
    void this.yukle();
    // Süpürge: sessiz bağlantılar, terk edilmiş odalar (LLM değil; yalnız RAM temizliği)
    setInterval(() => this.supur(), 60_000).unref?.();
    console.log('🀄 [Masa] WebSocket sunucusu /api/masa/ws üzerinde aktif.');
  }

  private async semaKur(): Promise<boolean> {
    if (this.sema || !this.d.isPgOnline()) return this.sema;
    try { await pgDb.query(fs.readFileSync(path.join(this.d.rootDir, 'deploy', 'pg', 'sql', 'masa.sql'), 'utf8')); this.sema = true; }
    catch (e: any) { console.warn('[Masa] şema:', e?.message); }
    return this.sema;
  }

  private async yukle() {
    for (let i = 0; i < 30 && !(await this.semaKur()); i++) await new Promise((r) => setTimeout(r, 2000));
    if (!this.sema) { this.yuklendi = true; return; }
    try {
      await pgDb.query(`delete from masa_oda where guncel < now() - interval '14 days' or (asama in ('bitti','lobi') and guncel < now() - interval '1 day')`);
      const { rows } = await pgDb.query(`select veri from masa_oda`);
      for (const r of rows as any[]) {
        const o = r.veri as Oda;
        if (o?.kod && TURLER.includes(o.tur) && !this.odalar.has(o.kod)) this.odalar.set(o.kod, o);
      }
      if (rows.length) console.log(`[Masa] ${rows.length} oda geri yüklendi.`);
    } catch (e: any) { console.warn('[Masa] yükleme:', e?.message); }
    this.yuklendi = true;
  }

  private kaydetPlanla(oda: Oda) {
    if (this.kayitZaman.has(oda.kod)) return;
    this.kayitZaman.set(oda.kod, setTimeout(() => { this.kayitZaman.delete(oda.kod); void this.kaydet(oda.kod); }, 1000));
  }
  private async kaydet(kod: string) {
    const oda = this.odalar.get(kod);
    if (!(await this.semaKur())) return;
    try {
      if (!oda) { await pgDb.query(`delete from masa_oda where kod = $1`, [kod]); return; }
      await pgDb.query(
        `insert into masa_oda (kod, veri, asama, uidler, guncel) values ($1, $2::jsonb, $3, $4, now())
         on conflict (kod) do update set veri = excluded.veri, asama = excluded.asama, uidler = excluded.uidler, guncel = now()`,
        [kod, JSON.stringify({ ...oda, geri: undefined }), oda.asama, oda.oyuncular.map((k) => k.uid).filter(Boolean)]);
    } catch (e: any) { console.warn('[Masa] kayıt:', e?.message); }
  }

  /* ------------------------------------------------------------ bağlantı ------------------------------------------------------------ */

  private yolla(b: Bag | { ws: any }, m: SunucuMesaj) {
    try { if (b.ws.readyState === 1) b.ws.send(JSON.stringify(m)); } catch { /* kapanmış */ }
  }
  private hata(b: Bag | { ws: any }, mesaj: string, kod?: Extract<SunucuMesaj, { t: 'hata' }>['kod']) { this.yolla(b, { t: 'hata', mesaj, kod }); }

  private baglan(ws: any) {
    let b: Bag | null = null;
    const ilk = { sayac: 0 };
    ws.on('message', (ham: any) => {
      let m: IstemciMesaj;
      try { m = JSON.parse(ham.toString()); } catch { return; }
      if (!m || typeof m !== 'object' || typeof (m as any).t !== 'string') return;
      const simdi = Date.now();
      if (!b) {
        if (m.t === 'ping') return this.yolla({ ws }, { t: 'pong', z: Number(m.z) || 0, s: simdi });
        if (m.t !== 'gir') return this.hata({ ws }, 'Bağlantı henüz doğrulanmadı; birazdan yeniden dene.', 'kimlik-bekle');
        if (++ilk.sayac > 5) return ws.close();
        if (!bayrakAcik('oyun_masa')) return this.hata({ ws }, 'Oyun şu an kapalı.', 'kapali');
        const uid = this.kimlikCoz(String(m.jeton || ''));
        if (!uid) return this.hata({ ws }, 'Oturumun doğrulanamadı. Sayfayı yenileyip yeniden dene.', 'kimlik');
        const ad = temiz(m.ad, 24) || this.d.kisiAd(uid) || 'Oyuncu';
        b = { ws, uid, id: this.d.kisiKimlik(uid), ad, kod: null, son: simdi, sayac: 0, pencere: simdi };
        this.tum.add(b);
        return this.yolla(b, { t: 'girdi', ben: b.id, ad });
      }
      b.son = simdi;
      if (simdi - b.pencere > 1000) { b.pencere = simdi; b.sayac = 0; }
      if (++b.sayac > 40) return ws.close();
      try { this.isle(b, m); }
      catch (e: any) { console.warn('[Masa] mesaj hatası:', m.t, e?.message); this.hata(b, 'Beklenmeyen bir hata oldu.'); }
    });
    ws.on('close', () => { if (b) { this.tum.delete(b); this.kopar(b); } });
    ws.on('error', () => { /* close izler */ });
  }

  private kimlikCoz(jeton: string): string | null {
    if (process.env.MEDS_MASA_TEST === '1' && /^test:[a-z0-9]{1,16}$/i.test(jeton)) return `masa-test-${jeton.slice(5).toLowerCase()}`;
    try { return erisimJetonuDogrula(jeton)?.uid || null; } catch { return null; }
  }

  /** Bağlantı kimliği → koltuk kimliği (koltuk devri yoksa aynısı) */
  private sid(oda: Oda, id: string) { return oda.devir?.[id] || id; }
  /** Şu an bağlı koltuklar */
  private bagliSet(oda: Oda) { return new Set([...(this.baglar.get(oda.kod)?.keys() || [])].map((id) => this.sid(oda, id))); }

  /** Bağlantı odadan düşer (koltuk kalır) */
  private kopar(b: Bag) {
    if (!b.kod) return;
    const m = this.baglar.get(b.kod);
    if (m?.get(b.id) === b) {
      m.delete(b.id);
      if (!m.size) this.baglar.delete(b.kod);
      const oda = this.odalar.get(b.kod);
      if (this.izleyici.get(b.kod)?.delete(b.id)) { /* izleyici gitti */ }
      else if (oda) this.kopZ.set(`${b.kod}:${this.sid(oda, b.id)}`, Date.now());
      if (oda) this.yayin(oda, [], false);
    }
    b.kod = null;
  }

  private otur(b: Bag, oda: Oda) {
    if (b.kod && b.kod !== oda.kod) this.ayril(b);
    let m = this.baglar.get(oda.kod);
    if (!m) this.baglar.set(oda.kod, (m = new Map()));
    const eski = m.get(b.id);
    if (eski && eski !== b) { eski.kod = null; this.yolla(eski, { t: 'cikti' }); }
    m.set(b.id, b);
    b.kod = oda.kod;
    this.kopZ.delete(`${oda.kod}:${this.sid(oda, b.id)}`);
  }

  /* ------------------------------------------------------------ mesajlar ------------------------------------------------------------ */

  private isle(b: Bag, m: IstemciMesaj) {
    if (m.t === 'ping') return this.yolla(b, { t: 'pong', z: Number(m.z) || 0, s: Date.now() });
    if (m.t === 'gir') return;
    if (!bayrakAcik('oyun_masa')) return this.hata(b, 'Oyun şu an kapalı.', 'kapali');
    if (m.t === 'kur') return this.kur(b, m.tur, m.ayar);
    if (m.t === 'katil') return this.katil(b, String(m.kod || '').toUpperCase());
    const oda = b.kod ? this.odalar.get(b.kod) : null;
    if (!oda) return this.hata(b, 'Oda bulunamadı.', 'oda-yok');
    const id = this.sid(oda, b.id);
    const koltuk = oda.oyuncular.find((k) => k.id === id);
    if (!koltuk) return this.izleyiciIsle(b, oda, m);
    const kurucu = oda.kurucu === id;
    const yalnizKurucu = () => { if (!kurucu) this.hata(b, 'Bunu yalnız odayı kuran yapabilir.'); return kurucu; };
    const motor = MOTORLAR[oda.tur];
    const [, enCok] = OYUNCU_SINIR[oda.tur];

    switch (m.t) {
      case 'ayar': {
        if (!yalnizKurucu()) return;
        oda.ayar = this.ayarDuzelt(oda.tur, { ...oda.ayar, ...(m.ayar || {}) }, oda.asama === 'lobi' ? null : oda.ayar);
        return this.yayin(oda);
      }
      case 'takim': {
        if (oda.tur !== 'takim' || oda.asama !== 'lobi') return;
        const hedef = m.hedef && kurucu ? oda.oyuncular.find((k) => k.id === m.hedef) : koltuk;
        if (!hedef || (m.takim !== 'A' && m.takim !== 'B')) return;
        hedef.takim = m.takim;
        return this.yayin(oda);
      }
      case 'botEkle': {
        if (!yalnizKurucu() || oda.asama !== 'lobi') return;
        if (oda.oyuncular.length >= enCok) return this.hata(b, 'Masa dolu.', 'dolu');
        const ad = BOT_ADLARI.find((a) => !oda.oyuncular.some((k) => k.bot && k.ad === `${a} (bot)`)) || `Bot ${oda.oyuncular.length}`;
        oda.oyuncular.push({ id: `bot-${crypto.randomBytes(3).toString('hex')}`, uid: null, ad: `${ad} (bot)`, bot: true, takim: oda.tur === 'takim' ? this.azTakim(oda) : undefined });
        return this.yayin(oda);
      }
      case 'cikar': {
        if (!yalnizKurucu() || oda.asama !== 'lobi' || m.hedef === id) return;
        const i = oda.oyuncular.findIndex((k) => k.id === m.hedef);
        if (i < 0) return;
        oda.oyuncular.splice(i, 1);
        const hb = this.baglar.get(oda.kod)?.get(m.hedef);
        if (hb) { this.baglar.get(oda.kod)!.delete(m.hedef); hb.kod = null; this.yolla(hb, { t: 'cikti' }); this.hata(hb, 'Kurucu seni masadan çıkardı.'); }
        return this.yayin(oda, [{ t: 'ayrildi', o: m.hedef }]);
      }
      case 'baslat': {
        if (!yalnizKurucu() || (oda.asama !== 'lobi' && oda.asama !== 'bitti')) return; // bitti → aynı masada yeni maç
        const [enAz] = OYUNCU_SINIR[oda.tur];
        if (oda.oyuncular.length < enAz) return this.hata(b, `En az ${enAz} oyuncu gerekir. Arkadaşını çağır ya da bot ekle.`);
        if (oda.oyuncular.length > enCok) return this.hata(b, `En çok ${enCok} oyuncu oynayabilir.`);
        if (oda.tur === 'takim') {
          const A = oda.oyuncular.filter((k) => k.takim === 'A'), B = oda.oyuncular.filter((k) => k.takim !== 'A');
          if (!A.length || A.length !== B.length) return this.hata(b, 'Takımlar eşit sayıda olmalı (1–1, 2–2 ya da 3–3).');
          B.forEach((k) => { k.takim = 'B'; });
          oda.oyuncular = A.flatMap((k, i) => [k, B[i]]); // karşılıklı oturma: A, B, A, B…
        }
        oda.skor = Object.fromEntries(oda.oyuncular.map((k) => [k.id, 0]));
        oda.eller = []; oda.elNo = 0; oda.baslayan = crypto.randomInt(oda.oyuncular.length) - 1;
        return this.elBaslat(oda);
      }
      case 'sonrakiEl': {
        if (oda.asama !== 'elSonu') return;
        if (!kurucu && this.bagliSet(oda).has(oda.kurucu)) return this.hata(b, 'Sonraki eli kurucu başlatır.');
        return this.elBaslat(oda);
      }
      case 'hamle': {
        if (oda.asama !== 'oyun' || oda.durum == null) return this.hata(b, 'Şu an hamle yapılamaz.', 'hamle');
        if (oda.durdu) return this.hata(b, 'Oyun durduruldu. Kurucunun devam ettirmesi bekleniyor.', 'hamle');
        return this.hamle(oda, id, m.h, b);
      }
      case 'geriAl': {
        if (oda.asama !== 'oyun' || oda.durdu || oda.durum == null) return this.hata(b, 'Şu an geri alınamaz.', 'hamle');
        const y = oda.geri;
        if (!y || y.kim !== id || !y.durumlar.length) return this.hata(b, 'Geri alınacak hamle yok. Taş çekme ve eli devretme geri alınmaz.', 'hamle');
        oda.durum = y.durumlar.pop();
        return this.yayin(oda, [{ t: 'geriAldi', o: id }]);
      }
      case 'durdur': case 'devam': {
        if (!yalnizKurucu() || (oda.asama !== 'oyun' && oda.asama !== 'elSonu')) return;
        const yeni = m.t === 'durdur';
        if (oda.durdu === yeni) return;
        oda.durdu = yeni;
        const motorD = MOTORLAR[oda.tur];
        if (yeni) oda.durduZ = Date.now();
        else if (oda.durduZ && motorD.saatKaydir && oda.durum != null) { oda.durum = motorD.saatKaydir(oda.durum, Date.now() - oda.durduZ); oda.durduZ = undefined; }
        return this.yayin(oda, [{ t: yeni ? 'durdu' : 'devam', o: id }]);
      }
      case 'bitir': {
        if (!yalnizKurucu() || oda.asama === 'lobi' || oda.asama === 'bitti') return;
        oda.asama = 'bitti'; oda.durdu = false;
        if (!motor.sonuc(oda.durum)) oda.elSonuc = undefined; // yarım el puanlanmaz
        return this.yayin(oda, [{ t: 'macBitti', o: id }]);
      }
      case 'botDevral': {
        if (!yalnizKurucu() || oda.asama === 'lobi' || oda.asama === 'bitti') return;
        const h = oda.oyuncular.find((k) => k.id === m.hedef);
        if (!h || h.bot || h.id === id) return;
        if (this.bagliSet(oda).has(h.id)) return this.hata(b, 'Bu oyuncu hâlâ bağlı.');
        h.bot = true;
        return this.yayin(oda, [{ t: 'botDevraldi', o: h.id }]);
      }
      case 'tepki': {
        if (!(TEPKILER as readonly string[]).includes(m.e)) return;
        return this.yayin(oda, [{ t: 'tepki', o: id, e: m.e }], false);
      }
      case 'koltukVer': {
        // Kurucu, izleyicinin bir bot koltuğunu almasını onaylar (koltuk kimliği aynı kalır, motor durumu bozulmaz)
        if (!yalnizKurucu() || oda.asama === 'lobi' || oda.asama === 'bitti') return;
        const iz = this.izleyici.get(oda.kod);
        const kisi = iz?.get(m.kime);
        const ib = this.baglar.get(oda.kod)?.get(m.kime);
        const hedef = oda.oyuncular.find((k) => k.id === (m.hedef || kisi?.istek));
        if (!kisi || !ib) return this.hata(b, 'Bu izleyici artık masada değil.');
        if (!hedef || !hedef.bot) return this.hata(b, 'Bu koltukta bot oynamıyor; başka koltuk seç.');
        for (const [k, v] of Object.entries(oda.devir || {})) if (v === hedef.id) delete oda.devir![k];
        oda.devir = { ...(oda.devir || {}), [m.kime]: hedef.id };
        hedef.bot = false; hedef.ad = ib.ad; hedef.uid = ib.uid; hedef.foto = this.d.foto?.(ib.uid);
        iz!.delete(m.kime);
        return this.yayin(oda, [{ t: 'katildi', o: hedef.id }, { t: 'koltukAldi', o: hedef.id }]);
      }
      case 'koltukRed': {
        if (!yalnizKurucu()) return;
        const kisi = this.izleyici.get(oda.kod)?.get(m.kime);
        if (!kisi?.istek) return;
        kisi.istek = undefined;
        const ib = this.baglar.get(oda.kod)?.get(m.kime);
        if (ib) this.hata(ib, 'Kurucu koltuk isteğini şimdilik kabul etmedi. İzlemeye devam edebilirsin.');
        return this.yayin(oda, [], false);
      }
      case 'cik': return this.ayril(b);
      default: return;
    }
  }

  /** Koltuğu olmayan bağlantı: oyun başlamışken gelen izleyici (yalnız izler, tepki atar, bot koltuğu ister ya da kalkar) */
  private izleyiciIsle(b: Bag, oda: Oda, m: IstemciMesaj) {
    const kisi = this.izleyici.get(oda.kod)?.get(b.id);
    if (!kisi) return this.hata(b, 'Bu odada değilsin.', 'oda-yok');
    if (m.t === 'cik') return this.ayril(b);
    if (m.t === 'tepki') return (TEPKILER as readonly string[]).includes(m.e) ? this.yayin(oda, [{ t: 'tepki', o: b.id, e: m.e }], false) : undefined;
    if (m.t === 'koltukIste') {
      const hedef = oda.oyuncular.find((k) => k.id === m.hedef);
      if (oda.asama === 'lobi' || oda.asama === 'bitti') return this.hata(b, 'Şu an koltuk devri yapılamaz.');
      if (!hedef?.bot) return this.hata(b, 'Yalnız bot oynayan koltuk istenebilir.');
      kisi.istek = hedef.id;
      return this.yayin(oda, [{ t: 'koltukIstek', o: b.id, kime: oda.kurucu }], false);
    }
    return this.hata(b, 'İzleyicisin: oynamak için bot oynayan bir koltuğu iste (kurucu onaylar).', 'hamle');
  }

  private azTakim(oda: Oda): Takim {
    const a = oda.oyuncular.filter((k) => k.takim === 'A').length;
    return a <= oda.oyuncular.length - a ? 'A' : 'B';
  }

  /** kilit: oyun başladıktan sonra yalnız görsel ayarlar (tema, renk) değişir */
  private ayarDuzelt(tur: OyunTur, a: Partial<OdaAyar>, kilit: OdaAyar | null): OdaAyar {
    const temalar: readonly string[] = tur === 'uno' ? UNO_TEMALAR : OKEY_TEMALAR;
    const renkler = Array.isArray(a.renkler) && a.renkler.length === 4 && a.renkler.every((r) => typeof r === 'string' && HEX.test(r))
      && new Set(a.renkler.map((r) => r.toLowerCase())).size === 4 ? a.renkler.map((r) => r.toLowerCase()) : [...VARSAYILAN_RENKLER];
    return {
      elSayisi: kilit ? kilit.elSayisi : (EL_SECENEK as readonly number[]).includes(Number(a.elSayisi)) ? Number(a.elSayisi) : 3,
      asistan: kilit ? kilit.asistan : a.asistan !== false,
      tasSayisi: kilit ? (kilit.tasSayisi === 14 ? 14 : 7) : Number(a.tasSayisi) === 14 ? 14 : 7,
      unoMod: kilit ? (kilit.unoMod ?? 'klasik') : UNO_MODLAR.some((m) => m.id === a.unoMod) ? a.unoMod : 'klasik',
      tema: temalar.includes(String(a.tema)) ? String(a.tema) : 'klasik',
      renkler,
      // Tahta oyunları (go/cizgi/xox)
      goBoyut: kilit ? kilit.goBoyut : ([9, 13, 19] as const).find((n) => n === Number(a.goBoyut)) ?? 9,
      goHandikap: kilit ? kilit.goHandikap : Number.isInteger(Number(a.goHandikap)) ? Math.max(0, Math.min(9, Number(a.goHandikap))) : 0,
      goSure: kilit ? kilit.goSure : GO_SURELER.find((x) => x.id === a.goSure)?.id ?? 'yok',
      komi: kilit ? kilit.komi : Number.isFinite(Number(a.komi)) && Number(a.komi) >= 0 && Number(a.komi) <= 15 ? Math.round(Number(a.komi) * 2) / 2 : 6.5,
      cizgiKare: kilit ? kilit.cizgiKare : ([32, 64, 96, 128] as const).find((n) => n === Number(a.cizgiKare)) ?? 64,
      xoxBoyut: kilit ? kilit.xoxBoyut : ([3, 4, 5, 6] as const).find((n) => n === Number(a.xoxBoyut)) ?? 3,
      botZorluk: kilit ? (kilit.botZorluk ?? 'orta') : (['kolay', 'orta', 'zor'] as const).find((z) => z === a.botZorluk) ?? 'orta',
    };
  }

  private kur(b: Bag, tur: OyunTur, ayar?: Partial<OdaAyar>) {
    if (!TURLER.includes(tur)) return this.hata(b, 'Bilinmeyen oyun.');
    const benim = [...this.odalar.values()].filter((o) => o.kurucu === b.id && o.asama !== 'bitti');
    if (benim.length >= 8) return this.hata(b, 'Çok fazla açık masan var. Önce yarım kalanlardan birini bitir.');
    let kod = kodUret();
    while (this.odalar.has(kod)) kod = kodUret();
    const simdi = Date.now();
    const oda: Oda = {
      kod, tur, ayar: this.ayarDuzelt(tur, ayar || {}, null), asama: 'lobi', durdu: false, kurucu: b.id,
      oyuncular: [{ id: b.id, uid: b.uid, ad: b.ad, bot: false, takim: tur === 'takim' ? 'A' : undefined, foto: this.d.foto?.(b.uid) }],
      elNo: 0, baslayan: 0, durum: null, skor: {}, eller: [], surum: 0, olusturma: simdi, guncel: simdi,
    };
    this.odalar.set(kod, oda);
    this.otur(b, oda);
    this.yayin(oda);
  }

  /** Kodda bulunmayan, karıştırılan karakterler (O/0 → D, I/1 → L/J/T…) için var olan odayı bulur */
  private kodBenzer(kod: string): string {
    if (this.odalar.has(kod) || /^[ABCDEFGHJKLMNPRSTUVYZ2-9]{5}$/.test(kod)) return kod;
    const es: Record<string, string[]> = { O: ['D'], '0': ['D'], Q: ['D'], I: ['L', 'J', 'T'], '1': ['L', 'J', 'T'], W: ['V'], X: ['Y', 'K'] };
    let adaylar = [''];
    for (const c of kod) adaylar = adaylar.flatMap((x) => (es[c] || [c]).map((y) => x + y)).slice(0, 200);
    return adaylar.find((k) => this.odalar.has(k)) || kod;
  }

  private katil(b: Bag, kod: string) {
    kod = kod.replace(/[^A-Z0-9]/g, '');
    if (!KOD.test(kod)) return this.hata(b, 'Masa kodu 5 karakterdir (harf ve rakam). Bağlantıyla geldiysen bağlantıyı yeniden aç.', 'oda-yok');
    kod = this.kodBenzer(kod);
    let oda = this.odalar.get(kod);
    if (!oda && !this.yuklendi) {
      // Sunucu yeni açıldı, odalar henüz geri yüklenmedi: istemcinin kendiliğinden geri oturması boşa düşmesin
      void this.tekYukle(kod).then(() => { if (b.ws.readyState === 1 && !b.kod) this.katilHazir(b, kod); });
      return;
    }
    this.katilHazir(b, kod);
  }

  private async tekYukle(kod: string) {
    for (let i = 0; i < 15 && !(await this.semaKur()); i++) await new Promise((r) => setTimeout(r, 1000));
    if (!this.sema || this.odalar.has(kod)) return;
    try {
      const { rows } = await pgDb.query(`select veri from masa_oda where kod = $1`, [kod]);
      const o = (rows as any[])[0]?.veri as Oda | undefined;
      if (o?.kod === kod && TURLER.includes(o.tur) && !this.odalar.has(kod)) this.odalar.set(kod, o);
    } catch (e: any) { console.warn('[Masa] tek yükleme:', e?.message); }
  }

  private katilHazir(b: Bag, kod: string) {
    const oda = this.odalar.get(kod);
    if (!oda) return this.hata(b, 'Bu kodla bir masa yok. Kodu kontrol et.', 'oda-yok');
    // Koltuğu devredilmiş eski sahibi geri gelirse izleyici olur (koltuk yeni oyuncuda)
    const devredildi = !oda.devir?.[b.id] && Object.values(oda.devir || {}).includes(b.id);
    const koltuk = devredildi ? undefined : oda.oyuncular.find((k) => k.id === this.sid(oda, b.id));
    if (koltuk) {
      const dondu = koltuk.bot; // yerine bot oynuyorduysa koltuğunu geri alır
      koltuk.bot = false; koltuk.ad = b.ad;
      this.otur(b, oda);
      return this.yayin(oda, dondu ? [{ t: 'katildi', o: b.id }] : [], dondu);
    }
    if (oda.asama === 'bitti') return this.hata(b, 'Bu masadaki maç bitti. Yeni bir masa kur ya da arkadaşından yeni kod iste.', 'basladi');
    if (oda.asama !== 'lobi' || devredildi) {
      // Oyun sürüyor: izleyici olarak oturur; bot koltuğunu kurucu onayıyla alabilir
      let iz = this.izleyici.get(oda.kod);
      if (!iz) this.izleyici.set(oda.kod, (iz = new Map()));
      if (!iz.has(b.id) && iz.size >= 12) return this.hata(b, 'Bu masada çok izleyici var. Oyun bitince yeniden dene.', 'dolu');
      iz.set(b.id, { ad: b.ad, istek: iz.get(b.id)?.istek });
      this.otur(b, oda);
      return this.yayin(oda, [{ t: 'izleyici', o: b.id }], false);
    }
    const [, enCokK] = OYUNCU_SINIR[oda.tur];
    if (oda.oyuncular.length >= enCokK) return this.hata(b, `Masa dolu (${enCokK}/${enCokK}). Kurucudan bir botu çıkarmasını iste ya da yeni masa kur.`, 'dolu');
    oda.oyuncular.push({ id: b.id, uid: b.uid, ad: b.ad, bot: false, takim: oda.tur === 'takim' ? this.azTakim(oda) : undefined, foto: this.d.foto?.(b.uid) });
    this.otur(b, oda);
    this.yayin(oda, [{ t: 'katildi', o: b.id }]);
  }

  /** Oyuncu masadan kalkar: lobide koltuk silinir, oyunda yerine bot oynar (kodla dönerse koltuğunu geri alır) */
  private ayril(b: Bag) {
    const oda = b.kod ? this.odalar.get(b.kod) : null;
    const m = b.kod ? this.baglar.get(b.kod) : null;
    if (m?.get(b.id) === b) { m.delete(b.id); if (!m.size) this.baglar.delete(b.kod!); }
    b.kod = null;
    this.yolla(b, { t: 'cikti' });
    if (!oda) return;
    if (this.izleyici.get(oda.kod)?.delete(b.id)) return this.yayin(oda, [], false);
    const sid = this.sid(oda, b.id);
    const i = oda.oyuncular.findIndex((k) => k.id === sid);
    if (i < 0) return;
    const olaylar: Olay[] = [{ t: 'ayrildi', o: sid }];
    if (oda.asama === 'lobi' || oda.asama === 'bitti') oda.oyuncular.splice(i, 1);
    else { oda.oyuncular[i].bot = true; olaylar.push({ t: 'botDevraldi', o: sid }); }
    const insanlar = oda.oyuncular.filter((k) => !k.bot);
    if (!insanlar.length) { this.odaSil(oda.kod); return; }
    if (oda.kurucu === sid) oda.kurucu = (insanlar.find((k) => this.bagliSet(oda).has(k.id)) || insanlar[0]).id;
    this.yayin(oda, olaylar);
  }

  private odaSil(kod: string) {
    this.odalar.delete(kod);
    for (const b of this.baglar.get(kod)?.values() || []) { b.kod = null; this.yolla(b, { t: 'cikti' }); }
    this.baglar.delete(kod);
    this.izleyici.delete(kod);
    clearTimeout(this.botZaman.get(kod)); this.botZaman.delete(kod);
    clearTimeout(this.sureZaman.get(kod)); this.sureZaman.delete(kod);
    void this.kaydet(kod);
  }

  /* ------------------------------------------------------------ oyun ------------------------------------------------------------ */

  private elBaslat(oda: Oda) {
    const motor = MOTORLAR[oda.tur];
    if (oda.ayar.elSayisi > 0 && oda.elNo >= oda.ayar.elSayisi) { oda.asama = 'bitti'; return this.yayin(oda, [{ t: 'macBitti' }]); }
    oda.elNo += 1;
    oda.baslayan = (oda.baslayan + 1) % oda.oyuncular.length;
    oda.durum = motor.elBaslat({ oyuncular: oda.oyuncular.map((k) => ({ id: k.id, takim: k.takim })), elNo: oda.elNo, baslayan: oda.baslayan, rng, ayar: oda.ayar });
    oda.geri = undefined;
    oda.elSonuc = undefined; oda.asama = 'oyun'; oda.durdu = false;
    this.yayin(oda, [{ t: 'dagit' }]);
  }

  private hamle(oda: Oda, oyuncu: string, h: unknown, b?: Bag) {
    const motor = MOTORLAR[oda.tur];
    // Süreli oyun: saat yalnız sunucu zamanıyla işler (istemcinin yolladığı z yok sayılır)
    if (motor.sureSonu && h && typeof h === 'object') h = { ...(h as object), z: Date.now() };
    let r: ReturnType<typeof motor.uygula>;
    try { r = motor.uygula(oda.durum, oyuncu, h, rng); }
    catch (e: any) { console.error('[Masa] motor istisnası:', oda.tur, JSON.stringify(h), e?.stack || e); r = { hata: 'Bu hamle işlenemedi.' }; }
    if ('hata' in r) { if (b) this.hata(b, r.hata, 'hamle'); return false; }
    const onceki = oda.durum;
    oda.durum = r.durum;
    const olaylar = [...r.olaylar];
    // Geri al yalnız gizli bilgi açmayan, turu bitirmeyen per açma / işleme hamlelerinde (çekme, devretme, atma, hediye geri alınmaz)
    const hm = (h as any)?.t;
    const geriAlinir = oda.tur !== 'uno' && (hm === 'ac' || hm === 'ac101' || hm === 'isle' || hm === 'duzenle')
      && !olaylar.some((o) => o.t === 'hediye' || o.t === 'elBitti' || o.t === 'sira' || o.t === 'cektim');
    // Go / XOX bota karşı: insanın taş koyması (bot yanıtıyla birlikte) geri alınabilir; botun hamlesi yığını silmez
    const ben = oda.oyuncular.find((k) => k.id === oyuncu);
    const botaKarsi = (oda.tur === 'go' || oda.tur === 'xox') && oda.oyuncular.every((k) => k.id === oyuncu || k.bot);
    const tahtaGeri = botaKarsi && !ben?.bot && hm === 'koy' && !(onceki as { saat?: unknown })?.saat && !olaylar.some((o) => o.t === 'elBitti');
    if (geriAlinir || tahtaGeri) {
      if (oda.geri?.kim !== oyuncu) oda.geri = { kim: oyuncu, durumlar: [] };
      oda.geri.durumlar.push(onceki);
      if (oda.geri.durumlar.length > 30) oda.geri.durumlar.shift();
    } else if (!((oda.tur === 'go' || oda.tur === 'xox') && ben?.bot)) oda.geri = undefined;
    const s = motor.sonuc(oda.durum);
    if (s) {
      oda.asama = 'elSonu'; oda.elSonuc = s;
      const puanlar: Record<string, number> = {};
      for (const satir of s.satirlar) { puanlar[satir.id] = satir.puan; oda.skor[satir.id] = (oda.skor[satir.id] || 0) + satir.puan; }
      oda.eller.push({ no: oda.elNo, neden: s.neden, kazananlar: s.kazananlar, puanlar });
      if (oda.eller.length > 200) oda.eller.shift();
      void this.elYaz(oda, s);
      if (oda.ayar.elSayisi > 0 && oda.elNo >= oda.ayar.elSayisi) { oda.asama = 'bitti'; olaylar.push({ t: 'macBitti' }); }
    }
    this.yayin(oda, olaylar);
    return true;
  }

  private gorunum(oda: Oda, bagId: string): OdaGorunum {
    const bagli = this.bagliSet(oda);
    const sid = this.sid(oda, bagId);
    const izliyor = !oda.oyuncular.some((k) => k.id === sid);
    const ben = izliyor ? bagId : sid;
    const simdi = Date.now();
    const iz = this.izleyici.get(oda.kod);
    return {
      kod: oda.kod, tur: oda.tur, ayar: oda.ayar, asama: oda.asama, durdu: oda.durdu, kurucu: oda.kurucu, ben,
      oyuncular: oda.oyuncular.map((k) => {
        const kz = !k.bot && !bagli.has(k.id) ? this.kopZ.get(`${oda.kod}:${k.id}`) : undefined;
        return { id: k.id, ad: k.ad, bot: k.bot || undefined, takim: k.takim, bagli: k.bot || bagli.has(k.id), foto: k.foto, kopSn: kz ? Math.floor((simdi - kz) / 1000) : undefined };
      }),
      izliyor: izliyor || undefined,
      izleyiciler: iz?.size ? [...iz].map(([id, v]) => ({ id, ad: v.ad, istek: v.istek })) : undefined,
      elNo: oda.elNo,
      oyun: oda.durum != null && oda.asama !== 'lobi' ? MOTORLAR[oda.tur].gorunum(oda.durum, izliyor ? null : ben) : undefined,
      elSonuc: oda.elSonuc, skor: oda.skor, eller: oda.eller.slice(-30), surum: oda.surum,
      geriAl: oda.geri?.kim === ben ? oda.geri.durumlar.length : 0,
    };
  }

  /** Herkese kendi görünümünü yollar. kalici=false: yalnız bağlantı/tepki gibi kayda değmeyen değişiklik */
  private yayin(oda: Oda, olaylar: Olay[] = [], kalici = true) {
    oda.surum += 1;
    oda.guncel = Date.now();
    for (const b of this.baglar.get(oda.kod)?.values() || []) {
      const sid = this.sid(oda, b.id);
      try { this.yolla(b, { t: 'durum', oda: this.gorunum(oda, b.id), olaylar: olaylar.filter((o) => !o.kime || o.kime === sid) }); }
      catch (e: any) { console.error('[Masa] görünüm hatası:', oda.tur, e?.stack || e); }
    }
    if (kalici) this.kaydetPlanla(oda);
    this.botPlanla(oda);
    this.surePlanla(oda);
  }

  /** Süreli oyunlarda sıradakinin süresi bitince el kaybettirilir (bot zamanlayıcısı kalıbı; durakta işlemez) */
  private surePlanla(oda: Oda) {
    clearTimeout(this.sureZaman.get(oda.kod)); this.sureZaman.delete(oda.kod);
    const motor = MOTORLAR[oda.tur];
    if (!motor.sureSonu || oda.asama !== 'oyun' || oda.durdu || oda.durum == null) return;
    const sonu = motor.sureSonu(oda.durum);
    if (sonu == null) return;
    this.sureZaman.set(oda.kod, setTimeout(() => {
      this.sureZaman.delete(oda.kod);
      if (this.odalar.get(oda.kod) !== oda || oda.asama !== 'oyun' || oda.durdu) return;
      const sira = (motor.gorunum(oda.durum, null) as { sira?: string }).sira;
      if (sira) this.hamle(oda, sira, { t: 'sureBitti' });
    }, Math.min(2 ** 31 - 1, Math.max(0, sonu - Date.now()) + 60)));
  }

  private botPlanla(oda: Oda) {
    if (this.botZaman.has(oda.kod) || oda.asama !== 'oyun' || oda.durdu || oda.durum == null) return;
    if (!this.baglar.get(oda.kod)?.size) return; // izleyen insan yokken bot yürümez
    const motor = MOTORLAR[oda.tur];
    const sec = (): { id: string; h: unknown } | null => {
      for (const k of oda.oyuncular) {
        if (!k.bot) continue;
        try { const h = motor.botHamle(oda.durum, k.id, rng); if (h) return { id: k.id, h }; }
        catch (e: any) { console.error('[Masa] bot istisnası:', oda.tur, e?.stack || e); }
      }
      return null;
    };
    if (!sec()) return;
    this.botZaman.set(oda.kod, setTimeout(() => {
      this.botZaman.delete(oda.kod);
      const guncel = this.odalar.get(oda.kod);
      if (guncel !== oda || oda.asama !== 'oyun' || oda.durdu) return;
      const s = sec();
      if (!s) return;
      if (!this.hamle(oda, s.id, s.h)) console.error('[Masa] bot hamlesi reddedildi:', oda.tur, JSON.stringify(s.h)); // döngüye girmesin: yeniden planlanmaz
    }, 750 + Math.floor(rng() * 650)));
  }

  private supur() {
    const simdi = Date.now();
    for (const b of this.tum) if (simdi - b.son > 90_000) { try { b.ws.terminate(); } catch { /* yok */ } }
    for (const oda of [...this.odalar.values()]) {
      if (this.baglar.get(oda.kod)?.size) continue;
      const bos = simdi - oda.guncel;
      if ((oda.asama === 'lobi' && bos > 30 * 60_000) || (oda.asama === 'bitti' && bos > 10 * 60_000) || bos > 14 * GUN) this.odaSil(oda.kod);
    }
  }

  /* ------------------------------------------------------------ istatistik ------------------------------------------------------------ */

  private async elYaz(oda: Oda, s: ElSonuc) {
    if (!(await this.semaKur())) return;
    try {
      const { rows } = await pgDb.query(`insert into masa_el (kod, tur, el_no, neden) values ($1, $2, $3, $4) returning id`, [oda.kod, oda.tur, oda.elNo, s.neden]);
      const elId = (rows as any[])[0]?.id;
      if (!elId) return;
      for (const satir of s.satirlar) {
        const k = oda.oyuncular.find((x) => x.id === satir.id);
        if (!k) continue;
        await pgDb.query(
          `insert into masa_el_oyuncu (el_id, uid, kimlik, ad, bot, takim, puan, kalan, ceza, kazandi) values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)`,
          [elId, k.bot ? null : k.uid, k.id, k.ad, k.bot, k.takim || null, satir.puan, satir.kalan, satir.cezalar.length, satir.kazandi]);
      }
    } catch (e: any) { console.warn('[Masa] el kaydı:', e?.message); }
  }

  private async istatistik(uid: string): Promise<Istatistik> {
    const bos: Istatistik = { genel: [], rakipler: [], son: [] };
    if (!(await this.semaKur())) return bos;
    const [g, r, s] = await Promise.all([
      pgDb.query(
        `select e.tur, count(*)::int el, count(*) filter (where o.kazandi)::int kazanma, coalesce(sum(o.puan),0)::int puan, coalesce(sum(o.ceza),0)::int ceza,
                max(o.puan)::int en_iyi, min(o.puan)::int en_kotu
         from masa_el_oyuncu o join masa_el e on e.id = o.el_id where o.uid = $1 group by e.tur order by el desc`, [uid]),
      pgDb.query(
        `select r.kimlik, (array_agg(r.ad order by e.at desc))[1] ad, count(*)::int el,
                count(*) filter (where b.kazandi and not r.kazandi)::int ben_kazandim, count(*) filter (where r.kazandi and not b.kazandi)::int o_kazandi,
                coalesce(sum(b.puan),0)::int ben_puan, coalesce(sum(r.puan),0)::int o_puan, jsonb_object_agg(e.tur, 0) turler_ham,
                array_agg(e.tur) turler
         from masa_el_oyuncu b join masa_el e on e.id = b.el_id
         join masa_el_oyuncu r on r.el_id = b.el_id and r.kimlik <> b.kimlik and not r.bot
         where b.uid = $1 group by r.kimlik order by el desc limit 100`, [uid]),
      pgDb.query(
        `select e.kod, e.tur, e.el_no, extract(epoch from e.at)::bigint * 1000 at, b.puan, b.kalan, b.ceza, b.kazandi,
                (select coalesce(array_agg(x.ad order by x.ad), '{}') from masa_el_oyuncu x where x.el_id = e.id and x.kimlik <> b.kimlik) rakipler
         from masa_el_oyuncu b join masa_el e on e.id = b.el_id where b.uid = $1 order by e.at desc limit 40`, [uid]),
    ]);
    return {
      genel: (g.rows as any[]).map((x) => ({ tur: x.tur, el: x.el, kazanma: x.kazanma, puan: x.puan, ceza: x.ceza, enIyi: x.en_iyi, enKotu: x.en_kotu })),
      rakipler: (r.rows as any[]).map((x) => {
        const turler: Partial<Record<OyunTur, number>> = {};
        for (const t of (x.turler || []) as OyunTur[]) turler[t] = (turler[t] || 0) + 1;
        return { kimlik: x.kimlik, ad: x.ad, el: x.el, benKazandim: x.ben_kazandim, oKazandi: x.o_kazandi, benPuan: x.ben_puan, oPuan: x.o_puan, turler };
      }),
      son: (s.rows as any[]).map((x) => ({ kod: x.kod, tur: x.tur, elNo: x.el_no, at: Number(x.at), puan: x.puan, kalan: x.kalan, ceza: x.ceza, kazandi: x.kazandi, rakipler: x.rakipler || [] })),
    };
  }

  /* ------------------------------------------------------------ REST ------------------------------------------------------------ */

  registerRoutes(app: express.Express) {
    const kim = (req: express.Request, res: express.Response): string | null => {
      const uid = verifiedUid(req);
      if (!uid) { res.status(401).json({ error: 'Giriş gerekli.' }); return null; }
      if (!bayrakAcik('oyun_masa')) { res.status(403).json({ error: 'Oyun şu an kapalı.' }); return null; }
      return uid;
    };

    app.get('/api/masa/odalarim', (req, res) => {
      const uid = kim(req, res); if (!uid) return;
      const ben = this.d.kisiKimlik(uid);
      const ogeler: OdaOzet[] = [...this.odalar.values()]
        .filter((o) => o.asama !== 'bitti' && o.oyuncular.some((k) => k.id === ben))
        .sort((a, b) => b.guncel - a.guncel).slice(0, 20)
        .map((o) => ({ kod: o.kod, tur: o.tur, asama: o.asama, durdu: o.durdu, oyuncular: o.oyuncular.filter((k) => k.id !== ben).map((k) => k.ad), elNo: o.elNo, guncel: o.guncel, kurucuBen: o.kurucu === ben }));
      res.json({ ogeler });
    });

    app.get('/api/masa/istatistik', async (req, res) => {
      const uid = kim(req, res); if (!uid) return;
      try { res.json(await this.istatistik(uid)); }
      catch (e: any) { console.warn('[Masa] istatistik:', e?.message); res.status(500).json({ error: 'İstatistik okunamadı.' }); }
    });

    const davetSon = new Map<string, number>();
    app.post('/api/masa/davet', async (req, res) => {
      const uid = kim(req, res); if (!uid) return;
      const kod = String(req.body?.kod || '').toUpperCase();
      const oda = this.odalar.get(kod);
      const ben = this.d.kisiKimlik(uid);
      if (!oda || !oda.oyuncular.some((k) => k.id === ben)) return res.status(404).json({ error: 'Masa bulunamadı.' });
      const hedef = this.d.uidBul(String(req.body?.kimlik || ''));
      if (!hedef || hedef === uid) return res.status(404).json({ error: 'Kişi bulunamadı.' });
      const anahtar = `${uid}:${hedef}`;
      if (Date.now() - (davetSon.get(anahtar) || 0) < 15_000) return res.status(429).json({ error: 'Az önce davet ettin; biraz bekle.' });
      try {
        const { rows } = await pgDb.query(`select 1 from arkadas_istek where durum = 'kabul' and ((gonderen = $1 and alan = $2) or (gonderen = $2 and alan = $1)) limit 1`, [uid, hedef]);
        if (!rows.length) return res.status(403).json({ error: 'Yalnız arkadaşlarını davet edebilirsin.' });
      } catch { return res.status(503).json({ error: 'Davet şu an gönderilemiyor.' }); }
      davetSon.set(anahtar, Date.now());
      if (davetSon.size > 5000) davetSon.clear();
      const ad = oda.oyuncular.find((k) => k.id === ben)?.ad || 'Arkadaşın';
      this.d.notifyStudent({ uid: hedef }, {
        type: 'davet', title: `${OYUN_ADI[oda.tur]} daveti`, message: `${ad} seni ${OYUN_ADI[oda.tur]} masasına çağırıyor (kod ${kod}).`,
        deepLinkUrl: `/sorular/oyunlar?masa=${kod}`, dedupeKey: `masa:${ben}:${kod}:${this.d.kisiKimlik(hedef)}`,
      });
      res.json({ ok: true });
    });
  }

  /** Yönetim: açık masalar (panel) */
  ozet() {
    return [...this.odalar.values()].map((o) => ({ kod: o.kod, tur: o.tur, asama: o.asama, durdu: o.durdu, oyuncu: o.oyuncular.length, bagli: this.baglar.get(o.kod)?.size || 0, elNo: o.elNo, guncel: o.guncel }));
  }
}

export const masaSunucu = new MasaSunucu();
