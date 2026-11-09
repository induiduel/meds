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
}
type OlayDinleyici = (olaylar: Olay[], oda: OdaGorunum, onceki: OdaGorunum | null) => void;

const AD_KEY = 'medsoru_masa_ad';
const SON_KEY = 'medsoru_masa_son';
export const masaAdi = (): string => {
  try { const a = localStorage.getItem(AD_KEY) || localStorage.getItem('medsoru_topluluk_ad'); if (a) return a; } catch { /* yok */ }
  return (auth.currentUser?.displayName || getRememberedStudentInfo().name || 'Oyuncu').split(' ')[0];
};

class MasaIstemci {
  private ws: WebSocket | null = null;
  private durum: MasaDurum = { baglanti: 'kapali', ben: '', ad: '', oda: null, hata: null, gecikme: 0 };
  private aboneler = new Set<() => void>();
  private olayAboneleri = new Set<OlayDinleyici>();
  private deneme = 0;
  private yeniden: any = null;
  private nabiz: any = null;
  private hataZaman: any = null;
  private istekli = false;
  /** Bağlantı kurulunca yapılacak ilk iş (kur/katıl) */
  private bekleyen: IstemciMesaj | null = null;
  private sonKod = '';
  /** Dışarıdan sınama için sahte kimlik (yalnız MEDS_MASA_TEST=1 sunucuda geçer): ?masatest=<ad> */
  private testAd = (() => { try { return new URLSearchParams(window.location.search).get('masatest') || ''; } catch { return ''; } })();

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
    ws.onmessage = (e) => { let m: SunucuMesaj; try { m = JSON.parse(e.data); } catch { return; } this.al(m); };
    ws.onclose = () => { if (this.ws !== ws) return; this.ws = null; clearInterval(this.nabiz); if (this.istekli) this.tekrarPlanla(); else this.yaz({ baglanti: 'kapali' }); };
    ws.onerror = () => { /* onclose izler */ };
  }

  private tekrarPlanla() {
    this.yaz({ baglanti: 'koptu' });
    clearTimeout(this.yeniden);
    this.yeniden = setTimeout(() => this.baglan(), Math.min(8000, 600 * 2 ** this.deneme++));
  }

  /** Sayfadan çıkarken: soket kapanır, koltuk sunucuda kalır (geri dönülebilir) */
  kapat() {
    this.istekli = false;
    clearTimeout(this.yeniden); clearInterval(this.nabiz);
    const ws = this.ws; this.ws = null;
    try { ws?.close(); } catch { /* yok */ }
    this.yaz({ baglanti: 'kapali', oda: null });
  }

  private yolla(m: IstemciMesaj) {
    if (this.ws?.readyState === WebSocket.OPEN) { this.ws.send(JSON.stringify(m)); return true; }
    return false;
  }

  private al(m: SunucuMesaj) {
    switch (m.t) {
      case 'girdi': {
        this.deneme = 0;
        this.yaz({ baglanti: 'hazir', ben: m.ben, ad: m.ad });
        clearInterval(this.nabiz);
        this.nabiz = setInterval(() => this.yolla({ t: 'ping', z: Date.now() }), 20_000);
        this.yolla({ t: 'ping', z: Date.now() });
        const ilk = this.bekleyen || (this.sonKod ? ({ t: 'katil', kod: this.sonKod } as IstemciMesaj) : null);
        this.bekleyen = null;
        if (ilk) this.yolla(ilk);
        break;
      }
      case 'durum': {
        const onceki = this.durum.oda;
        if (onceki && onceki.kod === m.oda.kod && m.oda.surum < onceki.surum) break; // sırası bozulmuş eski paket
        this.sonKod = m.oda.kod;
        try { localStorage.setItem(SON_KEY, m.oda.kod); } catch { /* yok */ }
        this.yaz({ oda: m.oda });
        if (m.olaylar.length) this.olayAboneleri.forEach((f) => { try { f(m.olaylar, m.oda, onceki); } catch (e) { console.warn('[masa] olay dinleyici', e); } });
        break;
      }
      case 'cikti': {
        this.sonKod = '';
        try { localStorage.removeItem(SON_KEY); } catch { /* yok */ }
        this.yaz({ oda: null });
        break;
      }
      case 'hata': {
        if (m.kod === 'oda-yok' || m.kod === 'basladi' || m.kod === 'dolu') { this.sonKod = ''; }
        this.yaz({ hata: { mesaj: m.mesaj, kod: m.kod, at: Date.now() } });
        clearTimeout(this.hataZaman);
        this.hataZaman = setTimeout(() => this.yaz({ hata: null }), 4000);
        break;
      }
      case 'pong': this.yaz({ gecikme: Math.max(0, Date.now() - m.z) }); break;
    }
  }

  hataSil() { clearTimeout(this.hataZaman); this.yaz({ hata: null }); }

  /** Bağlıysa hemen, değilse bağlanınca gönderir (yalnız kur/katıl kuyruğa alınır) */
  gonder(m: IstemciMesaj) {
    if (this.yolla(m)) return;
    if (m.t === 'kur' || m.t === 'katil') { this.bekleyen = m; this.baglan(); }
  }

  kur(tur: OyunTur, ayar?: Partial<OdaAyar>) { this.gonder({ t: 'kur', tur, ayar }); }
  katil(kod: string) { this.gonder({ t: 'katil', kod: kod.trim().toUpperCase() }); }
  hamle(h: Hamle) { this.gonder({ t: 'hamle', h }); }
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
