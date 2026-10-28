import React, { useEffect, useMemo, useState } from 'react';
import { AlertTriangle, Bell, Settings2, BellRing, CalendarClock, CheckCircle2, Headphones, Info, MessageSquare, PenLine, RotateCcw, Sparkles, Trash2, Users, XCircle } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import { userNotificationService, type UserNotification } from '../../services/userNotificationService';
import { openDeepLink } from '../../services/universalRedirectService';
import { aktifKurul, sinavaKalanGun } from '../../services/kurulTakvimi';
import { cdListeGetir } from '../canliDers/canliDersStore';
import { useYanlislar, yanlisGruplari } from '../../services/yanlislarim';
import { hatirlatOku, kisiselOku } from '../../services/sinavlarim';
import { confirmDialog } from '../ui/ConfirmDialog';
import { toast } from '../ui/Toast';
import { useV15Baslik } from './baslik';
import BildirimTercihV15 from './BildirimTercihV15';
import { hesapTuru, turAcik, useBildirimTercih, type BildirimTur } from '../../services/bildirimTercih';
import '../../styles/v15/ogren.css';
import '../../styles/v15/dersler.css';
import '../../styles/v15/bildirim.css';

/**
 * v15 · Bildirim merkezi (tasarım A06). Adres /bildirimler; üst bardaki zil buraya gelir.
 * Sekmeler Tümü · Ders · Soru · Sistem. Kaynaklar:
 *  - Hesaba yazılan bildirimler (userNotificationService: yorum, katkı, revizyon, yapay zekâ → Soru; app_* → Sistem).
 *  - Cihazdaki gerçek veriden türeyenler (uydurma yok): listede ilk kez görülen sesli ders → "Yeni sesli ders hazır",
 *    kurul sınavına ≤14 gün → hatırlatma (Ders); tekrar zamanı gelen yanlışlar (Soru).
 * Türeyenlerin okundu/silindi bilgisi cihazda (`medsoru_v15_bildirim_durum`). İlk açılışta mevcut dersler "görüldü"
 * sayılır, yalnız sonradan eklenenler bildirim olur.
 */
type Sekme = 'tum' | 'ders' | 'soru' | 'sistem';
interface Satir { id: string; sekme: Exclude<Sekme, 'tum'>; baslik: string; ileti: string; at: number; okundu: boolean; icon: React.ElementType; ton: string; git?: () => void; sil?: () => void; turetilmis?: boolean }

const DURUM_KEY = 'medsoru_v15_bildirim_durum';
const GORULEN_KEY = 'medsoru_v15_bildirim_dersler';
interface Durum { okundu: Record<string, 1>; silindi: Record<string, 1> }
const durumOku = (): Durum => { try { return { okundu: {}, silindi: {}, ...JSON.parse(localStorage.getItem(DURUM_KEY) || '{}') }; } catch { return { okundu: {}, silindi: {} }; } };
const durumYaz = (d: Durum) => { try { localStorage.setItem(DURUM_KEY, JSON.stringify(d)); } catch { /* yok */ } };

const TUR: Record<UserNotification['type'], { icon: React.ElementType; ton: string }> = {
  ai_reconstruction_complete: { icon: Sparkles, ton: 'ai' },
  ai_queued: { icon: Sparkles, ton: 'ai' },
  comment_added: { icon: MessageSquare, ton: 'a' },
  comment_deleted: { icon: MessageSquare, ton: 'n' },
  contribution_added: { icon: Users, ton: 'a' },
  report_filed: { icon: AlertTriangle, ton: 'w' },
  report_resolved: { icon: CheckCircle2, ton: 'ok' },
  question_revised: { icon: PenLine, ton: 'ok' },
  app_success: { icon: CheckCircle2, ton: 'ok' },
  app_info: { icon: Info, ton: 'n' },
  app_error: { icon: XCircle, ton: 'w' },
};

const zaman = (t: number) => {
  const s = Math.max(0, (Date.now() - t) / 1000);
  if (s < 60) return 'şimdi';
  if (s < 3600) return `${Math.floor(s / 60)} dk önce`;
  if (s < 86400) return `${Math.floor(s / 3600)} sa önce`;
  if (s < 2 * 86400) return 'dün';
  return new Date(t).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
};
const gunAnahtari = () => new Date().toISOString().slice(0, 10);

/** Listede ilk kez görülen sesli dersler: { key: { t, baslik } } (ilk çalıştırmada hepsi sessizce görüldü sayılır) */
function useYeniDersler() {
  const [yeni, setYeni] = useState<{ key: string; baslik: string; brans?: string; t: number }[]>([]);
  useEffect(() => {
    let canli = true;
    cdListeGetir(false).then((ds) => {
      if (!canli) return;
      let g: Record<string, { t: number; b: string; br?: string; yeni?: 1 }> | null = null;
      try { g = JSON.parse(localStorage.getItem(GORULEN_KEY) || 'null'); } catch { g = null; }
      const ilk = !g;
      const m = g || {};
      const simdi = Date.now();
      ds.filter((d) => !d.sinama && !/-son-prova-|-blok-ozet-/.test(d.key)).forEach((d) => {
        if (!m[d.key]) m[d.key] = { t: simdi, b: d.baslik, br: d.brans, ...(ilk ? {} : { yeni: 1 as const }) };
      });
      try { localStorage.setItem(GORULEN_KEY, JSON.stringify(m)); } catch { /* yok */ }
      // son 14 günde eklenen ve "yeni" işaretli dersler
      setYeni(Object.entries(m).filter(([, v]) => v.yeni && simdi - v.t < 14 * 86400000).map(([key, v]) => ({ key, baslik: v.b, brans: v.br, t: v.t })));
    }, () => {});
    return () => { canli = false; };
  }, []);
  return yeni;
}

/** /bildirimler?gorunum=tercih → tercihler (AB06); aksi halde bildirim listesi */
export default function BildirimlerV15() {
  const [tercihGor, setTercihGor] = useState(() => new URLSearchParams(location.search).get('gorunum') === 'tercih');
  useEffect(() => {
    const f = () => setTercihGor(new URLSearchParams(location.search).get('gorunum') === 'tercih');
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  return tercihGor ? <BildirimTercihV15 /> : <BildirimListesi />;
}

function BildirimListesi() {
  const [tercih] = useBildirimTercih();
  const [liste, setListe] = useState<UserNotification[]>(() => userNotificationService.getAll());
  const [durum, setDurum0] = useState<Durum>(durumOku);
  const [sekme, setSekme] = useState<Sekme>('tum');
  const [, tik] = useState(0);
  useYanlislar();
  const yeniDersler = useYeniDersler();
  const setDurum = (f: (d: Durum) => Durum) => setDurum0((d) => { const n = f(d); durumYaz(n); return n; });
  useEffect(() => userNotificationService.subscribe(setListe), []);
  useEffect(() => { const t = window.setInterval(() => tik((x) => x + 1), 30000); return () => window.clearInterval(t); }, []);

  const satirlar = useMemo<Satir[]>(() => {
    const tur = (id: string, s: Omit<Satir, 'okundu' | 'sil' | 'turetilmis'>, bt: BildirimTur): Satir | null =>
      durum.silindi[id] || !turAcik(bt, tercih) ? null : { ...s, okundu: !!durum.okundu[id], turetilmis: true, sil: () => setDurum((d) => ({ ...d, silindi: { ...d.silindi, [id]: 1 } })) };
    const out: (Satir | null)[] = [];
    yeniDersler.forEach((d) => out.push(tur(`ders:${d.key}`, {
      id: `ders:${d.key}`, sekme: 'ders', baslik: 'Yeni sesli ders hazır', ileti: [d.brans?.replace(/^Tıbbi\s+/, ''), d.baslik].filter(Boolean).join(' · '),
      at: d.t, icon: Headphones, ton: 'a', git: () => navigateTo(pathFor('canli_ders', d.key)),
    }, 'yeni_ders')));
    const kalan = sinavaKalanGun();
    if (kalan >= 0 && kalan <= 14) {
      const k = aktifKurul();
      const bugunBas = new Date(); bugunBas.setHours(8, 0, 0, 0);
      out.push(tur(`sinav:${k.kurul}:${gunAnahtari()}`, {
        id: `sinav:${k.kurul}:${gunAnahtari()}`, sekme: 'ders', baslik: kalan === 0 ? `Kurul ${k.kurul} sınavı bugün` : `Kurul ${k.kurul} sınavına ${kalan} gün`,
        ileti: 'Sınav planında bugün ne çalışacağın hazır', at: Math.min(Date.now(), bugunBas.getTime()), icon: CalendarClock, ton: 'w', git: () => navigateTo(pathFor('sinav_plani')),
      }, 'sinav'));
    }
    // D06 pratik hatırlatması: kurul ve kişisel sınavdan 5/3/1 gün önce
    if (hatirlatOku()) {
      const bg = new Date(); bg.setHours(0, 0, 0, 0);
      const sinavlar = [{ ad: `Kurul ${aktifKurul().kurul} sınavı`, gun: aktifKurul().sinav }, ...kisiselOku().map((x) => ({ ad: x.ad, gun: x.gun }))];
      sinavlar.forEach((x) => {
        const n = Math.round((new Date(`${x.gun}T00:00:00`).getTime() - bg.getTime()) / 86400000);
        if (n === 5 || n === 3 || n === 1) {
          const id = `pratik:${x.gun}:${x.ad}:${n}`;
          out.push(tur(id, { id, sekme: 'soru', baslik: `${x.ad} için pratik: ${n} gün kaldı`, ileti: '20 soruluk karma test hazır', at: bg.getTime() + 18 * 3600000 > Date.now() ? bg.getTime() : bg.getTime() + 18 * 3600000, icon: Bell, ton: 'w', git: () => navigateTo(pathFor('hub_sorular')) }, 'pratik'));
        }
      });
    }
    const hazir = yanlisGruplari().hazir;
    if (hazir.length) {
      out.push(tur(`yanlis:${gunAnahtari()}`, {
        id: `yanlis:${gunAnahtari()}`, sekme: 'soru', baslik: `${hazir.length} sorunun tekrar zamanı geldi`, ileti: 'Yanlış yaptığın sorular seni bekliyor',
        at: Math.max(...hazir.map((e) => e.due)), icon: RotateCcw, ton: 'b', git: () => navigateTo(pathFor('yanlislarim')),
      }, 'yanlis'));
    }
    liste.forEach((n) => {
      if (!turAcik(hesapTuru(n.type), tercih)) return;
      const m = TUR[n.type] || { icon: Bell, ton: 'n' };
      out.push({
        id: n.id, sekme: n.type.startsWith('app_') ? 'sistem' : 'soru', baslik: n.title, ileti: n.message, at: new Date(n.createdAt).getTime() || 0,
        okundu: n.read, icon: m.icon, ton: m.ton,
        git: n.deepLinkUrl ? () => openDeepLink(n.deepLinkUrl) : undefined,
        sil: () => userNotificationService.remove(n.id),
      });
    });
    return (out.filter(Boolean) as Satir[]).sort((a, b) => b.at - a.at);
  }, [liste, durum, yeniDersler, tercih]);

  const goster = sekme === 'tum' ? satirlar : satirlar.filter((s) => s.sekme === sekme);
  const okunmamis = satirlar.filter((s) => !s.okundu).length;
  const sayi = (s: Exclude<Sekme, 'tum'>) => satirlar.filter((x) => x.sekme === s && !x.okundu).length;
  useV15Baslik({ baslik: 'Bildirimler', alt: okunmamis ? `${okunmamis} okunmamış` : 'Hepsi okundu' });

  const okundu = (s: Satir) => {
    if (s.okundu) return;
    if (s.turetilmis) setDurum((d) => ({ ...d, okundu: { ...d.okundu, [s.id]: 1 } }));
    else userNotificationService.markAsRead(s.id);
  };
  const hepsiOkundu = () => {
    userNotificationService.markAllAsRead();
    setDurum((d) => ({ ...d, okundu: { ...d.okundu, ...Object.fromEntries(satirlar.filter((s) => s.turetilmis).map((s) => [s.id, 1 as const])) } }));
  };
  const temizle = async () => {
    if (!(await confirmDialog({ title: 'Bildirimler temizlensin mi?', message: 'Okunmuş bildirimler silinir; okunmamışlar kalır.', confirmLabel: 'Temizle', tone: 'danger' }))) return;
    satirlar.filter((s) => s.okundu).forEach((s) => s.sil?.());
    toast.success('Temizlendi', 'Okunmuş bildirimler silindi.');
  };

  return (
    <div className="b15 bd15">
      <h1 className="sr-only">Bildirimler</h1>
      <div className="bd15-ust">
        <div className="v15-seg bd15-seg" role="tablist" aria-label="Bildirim türü">
          {([['tum', 'Tümü', okunmamis], ['ders', 'Ders', sayi('ders')], ['soru', 'Soru', sayi('soru')], ['sistem', 'Sistem', sayi('sistem')]] as [Sekme, string, number][]).map(([id, t, n]) => (
            <button key={id} type="button" role="tab" aria-selected={sekme === id} aria-current={sekme === id ? 'page' : undefined} onClick={() => setSekme(id)}>
              {t}{n > 0 && <i className="bd15-n">{n}</i>}
            </button>
          ))}
        </div>
      </div>
      {/* H168: telefonda "Okunmuşları temizle" taşıp "Ok" diye kesiliyordu (satır kırılmıyordu); türetilmiş (silinemeyen)
          okunmuş satırlar temizle düğmesini boşuna etkin tutuyordu — yalnız silinebilen okunmuş varsa etkin */}
      {/* H341: bildirim yokken "Tümünü okundu say" / "Okunmuşları temizle" boşuna duruyordu; liste boşken gizlenir */}
      <div className="bd15-eylem">
        {satirlar.length > 0 && <button type="button" className="v15-btn is-ghost" onClick={hepsiOkundu} disabled={!okunmamis}>Tümünü okundu say</button>}
        <button type="button" className="v15-btn is-ghost" onClick={() => navigateTo('/bildirimler?gorunum=tercih')}><Settings2 aria-hidden /> Tercihler</button>
        {satirlar.length > 0 && <button type="button" className="v15-btn is-ghost" onClick={temizle} disabled={!satirlar.some((s) => s.okundu && s.sil)}><Trash2 aria-hidden /> Okunmuşları temizle</button>}
      </div>
      {goster.length ? (
        <ul className="b15-list v15-card" role="list">
          {goster.map((s) => (
            <li key={s.id} className={`bd15-sat${s.okundu ? '' : ' is-yeni'}`}>
              <button type="button" className="b15-row" onClick={() => { okundu(s); s.git?.(); }}>
                <span className={`v15-tile is-${s.ton}`}><s.icon aria-hidden /></span>
                <span className="b15-row-t">
                  <b>{s.baslik}</b>
                  <span>{s.ileti}{s.ileti ? ' · ' : ''}{zaman(s.at)}</span>
                </span>
                {!s.okundu && <span className="bd15-nokta" aria-label="Okunmamış" />}
              </button>
              {s.sil && <button type="button" className="v15-ib bd15-sil" onClick={s.sil} aria-label="Bildirimi sil" title="Sil"><Trash2 aria-hidden /></button>}
            </li>
          ))}
        </ul>
      ) : (
        <div className="v15-card bd15-bos">
          <BellRing aria-hidden />
          <b>{sekme === 'tum' ? 'Bildirim yok' : 'Bu sekmede bildirim yok'}</b>
          <p>Yeni sesli ders eklendiğinde, sınav yaklaştığında, yanlışlarının tekrar zamanı geldiğinde ve sorularına yorum ya da düzeltme geldiğinde burada görürsün.</p>
        </div>
      )}
    </div>
  );
}
