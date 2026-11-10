/**
 * Taş Masası tarayıcı istemcisi (sunucu: services/masa/sunucu.ts, sözleşme: tipler.ts).
 *
 * - Tek soket, kendiliğinden yeniden bağlanır (artan bekleme) ve son masaya kendiliğinden geri oturur.
 * - Ekran YALNIZ `useMasa().oda`'dan çizilir (sunucu her değişiklikte tam görünüm yollar). Olaylar yalnız animasyon içindir:
 *   `masa.olayDinle(fn)`; her çağrıda o hamlenin olayları + yeni oda görünümü birlikte gelir.
 * - Bileşenler `masa.gonder(...)` / kısayollarla (hamle, kur, katil…) konuşur; hata `useMasa().hata` (kısa süreli bildirim).
 */
import { useSyncExternalStore } from 'react';
import { getCustomApiUrl } from '../api';
import { auth, getRememberedStudentInfo } from '../auth';
import { hamleTahmini } from './tahmin';
import type { Hamle, IstemciMesaj, OdaAyar, OdaGorunum, Olay, OyunTur, SunucuMesaj, Takim } from './tipler';

export interface MasaDurum {
  /** kapali: henüz bağlanılmadı · baglaniyor · hazir: kimlik doğrulandı · koptu: yeniden deneniyor */
  baglanti: 'kapali' | 'baglaniyor' | 'hazir' | 'koptu';
  ben: string;
  ad: string;
  oda: OdaGorunum | null;
  /** Son sunucu hatası (4 sn sonra kendiliğinden silinir) */
  hata: { mesaj: string; kod?: string; at: number } | null;
  /** Gidiş-dönüş gecikmesi (ms) */
  gecikme: number;
  /** Sunucudan yanıt beklenen istek (kur, katıl, başlat, hamle…): bekleme ekranı bundan çizilir */
  bekliyor: { ne: string; at: number } | null;
  /** Kopukken: kaçıncı yeniden deneme ve bir sonrakinin zamanı */
  deneme: number;
  sonrakiDeneme: number;
}
type OlayDinleyici = (olaylar: Olay[], oda: OdaGorunum, onceki: OdaGorunum | null) => void;

const AD_KEY = 'medsoru_masa_ad';
const SON_KEY = 'medsoru_masa_son';
export const masaAdi = (): string => {
  try { const a = localStorage.getItem(AD_KEY) || localStorage.getItem('medsoru_topluluk_ad'); if (a) return a; } catch { /* yok */ }
  return (auth.currentUser?.displayName || getRememberedStudentInfo().name || 'Oyuncu').split(' ')[0];
};

/** Elle yazılan kod: Türkçe büyük harf, boşluk/tire atılır (O/0, I/1 karışıklığını sunucu çözer) */
export const kodDuzelt = (s: string) => s.toLocaleUpperCase('tr-TR').replace(/İ/g, 'I').replace(/[^A-Z0-9]/g, '').slice(0, 5);

/** Yanıtı beklenen istekler ve bekleme ekranındaki açıklaması */
const BEKLEME: Partial<Record<IstemciMesaj['t'], string>> = {
  kur: 'Masa kuruluyor', katil: 'Masaya oturuluyor', baslat: 'Taşlar dağıtılıyor', sonrakiEl: 'Yeni el dağıtılıyor', hamle: 'Hamlen gönderiliyor', geriAl: 'Hamle geri alınıyor',
};

class MasaIstemci {
  private ws: WebSocket | null = null;
  private durum: MasaDurum = { baglanti: 'kapali', ben: '', ad: '', oda: null, hata: null, gecikme: 0, bekliyor: null, deneme: 0, sonrakiDeneme: 0 };
  private aboneler = new Set<() => void>();
  private olayAboneleri = new Set<OlayDinleyici>();
  private deneme = 0;
  private yeniden: any = null;
  private nabiz: any = null;
  private hataZaman: any = null;
  private istekli = false;
  /** Bağlantı doğrulanınca gönderilecek iş (kur/katıl ve kopukken basılan başlat/sonraki el) */
  private bekleyen: IstemciMesaj[] = [];
  private bekleZaman: any = null;
  private sonKod = '';
  /** Son sunucu onaylı görünüm (iyimser tahmin reddedilirse buna dönülür) */
  private onayli: OdaGorunum | null = null;
  private tahminZaman: any = null;
  /** Dışarıdan sınama için sahte kimlik (yalnız MEDS_MASA_TEST=1 sunucuda geçer): ?masatest=<ad> */
  private testAd = (() => { try { return new URLSearchParams(window.location.search).get('masatest') || ''; } catch { return ''; } })();

  /** Yalnız ?masatest kipinde sınama kancası: yapay gecikme (ms) ve belirli süre bağlanamama */
  private testGecikme = 0;
  private testEngel = 0;
  constructor() {
    if (this.testAd && typeof window !== 'undefined') (window as any).__masaTest = {
      gecikme: (ms: number) => { this.testGecikme = Math.max(0, ms | 0); },
      kopar: (sn: number) => { this.testEngel = Date.now() + sn * 1000; try { this.ws?.close(); } catch { /* yok */ } },
      // Başsız tarayıcı sınaması: mesaj gönder, durumu oku, Uno asistan önerisini al
      gonder: (m: IstemciMesaj) => this.gonder(m),
      oku: () => this.durum,
      unoOneri: async () => { const o = this.durum.oda; return o?.oyun?.tur === 'uno' ? (await import('./motor/unoAsistan')).oneri(o.oyun, o.ben) : null; },
    };
  }

  abone = (fn: () => void) => { this.aboneler.add(fn); return () => { this.aboneler.delete(fn); }; };
  oku = () => this.durum;
  olayDinle(fn: OlayDinleyici) { this.olayAboneleri.add(fn); return () => { this.olayAboneleri.delete(fn); }; }

  private yaz(p: Partial<MasaDurum>) { this.durum = { ...this.durum, ...p }; this.aboneler.forEach((f) => f()); }

  private adres() {
    const ozel = getCustomApiUrl('/api/masa/ws');
    const kok = ozel ? new URL(ozel, window.location.href) : new URL(window.location.href);
    return `${kok.protocol === 'https:' ? 'wss:' : 'ws:'}//${kok.host}/api/masa/ws`;
  }

  /** Soketi açar (açıksa dokunmaz). Sayfa açıkken bir kez çağrılır. */
  baglan() {
    this.istekli = true;
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) return;
    clearTimeout(this.yeniden);
    if (Date.now() < this.testEngel) return this.tekrarPlanla();
    this.yaz({ baglanti: this.deneme ? 'koptu' : 'baglaniyor' });
    let ws: WebSocket;
    try { ws = new WebSocket(this.adres()); } catch { return this.tekrarPlanla(); }
    this.ws = ws;
    ws.onopen = async () => {
      let jeton = '';
      if (this.testAd) jeton = `test:${this.testAd}`;
      else { try { await auth.authStateReady(); jeton = (await auth.currentUser?.getIdToken()) || ''; } catch { /* aşağıda hata */ } }
      if (this.ws !== ws) return;
      this.yolla({ t: 'gir', jeton, ad: this.testAd || masaAdi() });
    };
    ws.onmessage = (e) => {
      let m: SunucuMesaj; try { m = JSON.parse(e.data); } catch { return; }
      if (this.testGecikme) setTimeout(() => this.al(m), this.testGecikme / 2); else this.al(m);
    };
    ws.onclose = () => { if (this.ws !== ws) return; this.ws = null; clearInterval(this.nabiz); if (this.istekli) this.tekrarPlanla(); else this.yaz({ baglanti: 'kapali' }); };
    ws.onerror = () => { /* onclose izler */ };
  }

  private tekrarPlanla() {
    clearTimeout(this.yeniden);
    const bekle = Math.min(8000, 600 * 2 ** this.deneme++);
    this.yaz({ baglanti: 'koptu', deneme: this.deneme, sonrakiDeneme: Date.now() + bekle });
    this.yeniden = setTimeout(() => this.baglan(), bekle);
  }

  /** Sayfadan çıkarken: soket kapanır, koltuk sunucuda kalır (geri dönülebilir) */
  kapat() {
    this.istekli = false;
    clearTimeout(this.yeniden); clearInterval(this.nabiz);
    const ws = this.ws; this.ws = null;
    try { ws?.close(); } catch { /* yok */ }
    this.onayli = null; clearTimeout(this.tahminZaman);
    this.yaz({ baglanti: 'kapali', oda: null });
  }

  /** Kimlik doğrulanmadan (girdi gelmeden) sunucu gir/ping dışında mesaj işlemez: yalnız hazırken gönderilir */
  private yolla(m: IstemciMesaj) {
    const hazir = m.t === 'gir' || m.t === 'ping' || this.durum.baglanti === 'hazir';
    if (hazir && this.ws?.readyState === WebSocket.OPEN) {
      const ws = this.ws, veri = JSON.stringify(m);
      if (this.testGecikme) setTimeout(() => { if (ws.readyState === WebSocket.OPEN) ws.send(veri); }, this.testGecikme / 2); else ws.send(veri);
      return true;
    }
    return false;
  }

  private bekle(ne: string | null) {
    clearTimeout(this.bekleZaman);
    this.yaz({ bekliyor: ne ? { ne, at: Date.now() } : null });
    if (!ne) return;
    // Yanıt gelmezse kullanıcı sonsuz beklemesin: hata göster, soketi yenile
    this.bekleZaman = setTimeout(() => {
      this.yaz({ bekliyor: null });
      this.hataYaz('Sunucu yanıt vermedi. Bağlantı yenileniyor, birazdan yeniden dene.');
      try { this.ws?.close(); } catch { /* yok */ }
    }, 15_000);
  }

  private hataYaz(mesaj: string, kod?: string) {
    this.yaz({ hata: { mesaj, kod, at: Date.now() } });
    clearTimeout(this.hataZaman);
    this.hataZaman = setTimeout(() => this.yaz({ hata: null }), 4000);
  }

  private al(m: SunucuMesaj) {
    switch (m.t) {
      case 'girdi': {
        this.deneme = 0;
        this.yaz({ baglanti: 'hazir', ben: m.ben, ad: m.ad, deneme: 0, sonrakiDeneme: 0 });
        clearInterval(this.nabiz);
        this.nabiz = setInterval(() => this.yolla({ t: 'ping', z: Date.now() }), 8_000);
        this.yolla({ t: 'ping', z: Date.now() });
        const kuyruk = this.bekleyen.length ? this.bekleyen : this.sonKod ? [{ t: 'katil', kod: this.sonKod } as IstemciMesaj] : [];
        this.bekleyen = [];
        // Kopukken basılan başlat/sonraki el için önce masaya geri oturulur
        if (this.sonKod && kuyruk.length && kuyruk[0].t !== 'kur' && kuyruk[0].t !== 'katil') kuyruk.unshift({ t: 'katil', kod: this.sonKod });
        kuyruk.forEach((m) => this.yolla(m));
        break;
      }
      case 'durum': {
        const onceki = this.onayli;
        if (onceki && onceki.kod === m.oda.kod && m.oda.surum < onceki.surum) break; // sırası bozulmuş eski paket
        this.onayli = m.oda; clearTimeout(this.tahminZaman);
        this.sonKod = m.oda.kod;
        try { localStorage.setItem(SON_KEY, m.oda.kod); } catch { /* yok */ }
        this.yaz({ oda: m.oda });
        if (this.durum.bekliyor) this.bekle(null);
        if (m.olaylar.length) this.olayAboneleri.forEach((f) => { try { f(m.olaylar, m.oda, onceki); } catch (e) { console.warn('[masa] olay dinleyici', e); } });
        break;
      }
      case 'cikti': {
        this.sonKod = ''; this.onayli = null;
        try { localStorage.removeItem(SON_KEY); } catch { /* yok */ }
        this.yaz({ oda: null });
        if (this.durum.bekliyor) this.bekle(null);
        break;
      }
      case 'hata': {
        if (m.kod === 'oda-yok' || m.kod === 'basladi' || m.kod === 'dolu') { this.sonKod = ''; }
        if (this.durum.bekliyor) this.bekle(null);
        this.tahminGeriAl();
        this.hataYaz(m.mesaj, m.kod);
        break;
      }
      case 'pong': this.yaz({ gecikme: Math.max(0, Date.now() - m.z) }); break;
    }
  }

  /** Kopukken "Şimdi dene": beklemeyi atlar */
  simdiDene() { if (this.durum.baglanti === 'koptu') { clearTimeout(this.yeniden); this.baglan(); } }

  hataSil() { clearTimeout(this.hataZaman); this.yaz({ hata: null }); }

  /** Bağlıysa hemen, değilse bağlanınca gönderir (yalnız kur/katıl kuyruğa alınır) */
  gonder(m: IstemciMesaj) {
    const ne = BEKLEME[m.t];
    if (this.yolla(m)) { if (ne) this.bekle(ne); return; }
    if (m.t === 'kur' || m.t === 'katil' || m.t === 'baslat' || m.t === 'sonrakiEl') {
      // Bağlantı hazır değil: sessizce düşmesin, doğrulanınca gönderilsin
      this.bekleyen = [...this.bekleyen.filter((x) => x.t !== m.t), m];
      if (ne) this.bekle(ne);
      this.baglan();
      return;
    }
    if (m.t === 'hamle' || m.t === 'geriAl') this.hataYaz('Bağlantı yeniden kuruluyor; hamlen gönderilemedi. Birazdan yeniden dene.');
  }

  kur(tur: OyunTur, ayar?: Partial<OdaAyar>) { this.gonder({ t: 'kur', tur, ayar }); }
  katil(kod: string) { this.gonder({ t: 'katil', kod: kodDuzelt(kod) }); }
  koltukIste(hedef: string) { this.gonder({ t: 'koltukIste', hedef }); }
  koltukVer(kime: string, hedef?: string) { this.gonder({ t: 'koltukVer', kime, hedef }); }
  koltukRed(kime: string) { this.gonder({ t: 'koltukRed', kime }); }
  /** Hamle: tahmin edilebiliyorsa sunucu yanıtı beklenmeden ekrana yansır (tahmin.ts); sunucu durumu her zaman son sözdür */
  hamle(h: Hamle) {
    const oda = this.durum.oda;
    const t = oda ? hamleTahmini(oda, h) : null;
    if (!t || !this.yolla({ t: 'hamle', h })) return this.gonder({ t: 'hamle', h });
    this.yaz({ oda: t });
    // Yanıt hiç gelmezse tahmin ekranda takılı kalmasın: onaylı görünüme dön, soketi yenile
    clearTimeout(this.tahminZaman);
    this.tahminZaman = setTimeout(() => {
      this.tahminGeriAl();
      this.hataYaz('Sunucu yanıt vermedi. Bağlantı yenileniyor, birazdan yeniden dene.');
      try { this.ws?.close(); } catch { /* yok */ }
    }, 15_000);
  }
  private tahminGeriAl() {
    clearTimeout(this.tahminZaman);
    if (this.onayli && this.durum.oda && this.durum.oda !== this.onayli && this.durum.oda.kod === this.onayli.kod) this.yaz({ oda: this.onayli });
  }
  geriAl() { this.gonder({ t: 'geriAl' }); }
  ayar(ayar: Partial<OdaAyar>) { this.gonder({ t: 'ayar', ayar }); }
  takim(takim: Takim, hedef?: string) { this.gonder({ t: 'takim', takim, hedef }); }
  botEkle() { this.gonder({ t: 'botEkle' }); }
  cikar(hedef: string) { this.gonder({ t: 'cikar', hedef }); }
  baslat() { this.gonder({ t: 'baslat' }); }
  sonrakiEl() { this.gonder({ t: 'sonrakiEl' }); }
  durdur() { this.gonder({ t: 'durdur' }); }
  devam() { this.gonder({ t: 'devam' }); }
  bitir() { this.gonder({ t: 'bitir' }); }
  botDevral(hedef: string) { this.gonder({ t: 'botDevral', hedef }); }
  tepki(e: string) { this.gonder({ t: 'tepki', e }); }
  /** Masadan kalk (oyundaysa yerine bot oynar) */
  cik() { this.gonder({ t: 'cik' }); }
  adYaz(ad: string) { try { localStorage.setItem(AD_KEY, ad.trim().slice(0, 24)); } catch { /* yok */ } }
}

export const masa = new MasaIstemci();
export function useMasa(): MasaDurum { return useSyncExternalStore(masa.abone, masa.oku, masa.oku); }
