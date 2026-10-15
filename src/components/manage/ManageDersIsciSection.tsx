import React, { Suspense, useEffect, useMemo, useState } from 'react';
import { BookOpenCheck, CheckCircle2, ClipboardList, Eye, FileWarning, RefreshCw, RotateCcw, XCircle, PenLine, Library, Play, ArrowUp, ArrowDown, Trash2, ListPlus, ShieldOff } from 'lucide-react';
import { CalendarClock, Cpu, FileSearch, RefreshCcw, ShieldCheck, Hourglass, AlertTriangle, Ban, Wrench, Inbox, Layers } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';
import { NoteMarkdown } from '../ui/NoteMarkdown';
import { ChipBar, EmptyState, Panel } from './consoleUi';
import { IsciKontrol, type IsciDurum } from './ManageDersIsciKontrol';

const LessonPlayer = React.lazy(() => import('../learn/lesson/LessonPlayer').then((m) => ({ default: m.LessonPlayer })));

/**
 * "Yeni dersler": Oracle'daki ders işçisinin (scripts/ders_isci) Drive'dan yakalayıp Claude ile ürettiği ders paketleri.
 * Yönetici taslağı inceler (rapor, deste önizlemesi, sorular, sözlük, hastalıklar, bilgi havuzu, çıkmış bağları, kitaptan
 * tamamlanan bilgiler) ve karar verir. Karar taslağa yazılır; yayına birleştirme ayrı adımdır (onaylananlar).
 * Veri: /api/admin/ders-isci/* (sunucu → işçinin iç API'si).
 */
type Program = { kurul?: number; ders?: string; konu?: string; ogretim_uyesi?: string; tarih?: string; guven?: string; skor?: number };
type Karar = { karar: 'onayla' | 'reddet' | 'duzelt'; not?: string; kim?: string; zaman?: number } | null;
type Taslak = {
  is_id: string;
  durum: string;
  ozet: string;
  ders_id?: string;
  deste_id?: string;
  mod?: 'yeni' | 'guncelleme';
  uyari?: string;
  pdf?: string;
  program: Program;
  sayilar: Record<string, number>;
  denetim_hata?: number;
  referans?: number;
  karar: Karar;
  zaman?: number;
  yayin?: { durum?: string; hatalar?: string[]; yayin_zamani?: string; site_derlendi?: boolean } | null;
};
type Ayrinti = Taslak & { rapor: string; denetim: { hatalar?: string[]; uyarilar?: string[]; referansla_tamamlanan?: string[] }; dosyalar: string[] };
type Sekme = 'rapor' | 'deste' | 'sorular' | 'sozluk' | 'hastaliklar' | 'havuz' | 'cikmis' | 'kaynak';
/** Kuyruk kaydı (işçi /kuyruk ← kuyruk.json): durum bekliyor | isleniyor | taslak | hata. */
type KuyrukIs = {
  is_id: string;
  yol: string;
  durum: string;
  eklendi?: number;
  deneme?: number;
  son_mesaj?: string;
  sonra?: number;
  basladi?: number;
  uyari?: string;
  konular?: string[];
};
/** İşçi /zamanlama: izle.sira_isle() kurallarıyla bekleyen işlerin tahmini başlama saati. */
type Zamanlama = { gunluk_sinir: number; ders_arasi_sn: number; saatler: string; aralik_sn: number; duraklat?: boolean; bugun_islenen: number; plan: { is_id: string; tahmini: number }[] };
/** Checklist satırı (işçi /checklist ← checklist.json konular[]). */
type KonuSatiri = { kurul?: number; tarih?: string; ders?: string; konu?: string; hoca?: string; durum: string; deste_id?: string | null; pdf_2627?: { pdf: string; sayfa?: string }[] };

/**
 * Kategoriler — her biri yalnız gerçek durum alanlarından türetilir:
 * programlandi: kuyruk.durum=bekliyor (saat: /zamanlama plan, yoksa kuyruk.sonra) · isleniyor: kuyruk.durum=isleniyor ya da
 * taslak durum.json'u henüz yok · goruldu: checklist durum=islenmeli (26-27 PDF'i var, ders yok, henüz kuyrukta değil) ·
 * yenilenmeli: checklist durum=yenilenmeli · onay: durum=onay_bekliyor ve karar yok · duzelt: karar=duzelt ·
 * onaylandi: karar=onayla, yayin.json yok/beklemede · yayinda: durum=yayinlandi · hata: kuyruk.durum=hata, yayin.durum=
 * denetim_hatasi ya da site_derlendi=false · reddedildi: karar=reddet / durum=reddedildi.
 */
type Filtre = 'hepsi' | 'onay' | 'programlandi' | 'isleniyor' | 'goruldu' | 'yenilenmeli' | 'duzelt' | 'onaylandi' | 'yayinda' | 'hata' | 'reddedildi';
const KATEGORI: Record<Exclude<Filtre, 'hepsi'>, { label: string; cls: string; icon: React.ElementType }> = {
  onay: { label: 'Onay bekliyor', cls: 'is-warn', icon: Inbox },
  programlandi: { label: 'Zamanlayıcı programlandı', cls: '', icon: CalendarClock },
  isleniyor: { label: 'İşleniyor', cls: '', icon: Cpu },
  goruldu: { label: 'PDF görüldü, işlenmedi', cls: '', icon: FileSearch },
  yenilenmeli: { label: 'Yenilenmeli', cls: 'is-warn', icon: RefreshCcw },
  duzelt: { label: 'Düzeltme istendi', cls: 'is-warn', icon: Wrench },
  onaylandi: { label: 'Onaylandı · yayın sırasında', cls: 'is-ok', icon: Hourglass },
  yayinda: { label: 'Onaylandı · yayında', cls: 'is-ok', icon: ShieldCheck },
  hata: { label: 'Hata', cls: 'is-bad', icon: AlertTriangle },
  reddedildi: { label: 'Reddedildi', cls: 'is-bad', icon: Ban },
};
const SIRA: Exclude<Filtre, 'hepsi'>[] = ['onay', 'programlandi', 'isleniyor', 'goruldu', 'yenilenmeli', 'duzelt', 'onaylandi', 'yayinda', 'hata', 'reddedildi'];
type Satir = {
  anahtar: string;
  kat: Exclude<Filtre, 'hepsi'>;
  baslik: string;
  etiketler: string[];
  mesaj?: string;
  uyari?: string;
  zamanNot?: string;
  taslak?: Taslak;
  /** 'goruldu' / 'yenilenmeli' satırlarında elle kuyruğa alınacak 2026-27 PDF yolları */
  pdfler?: string[];
};
const saat = (t?: number) =>
  t ? new Date(t * 1000).toLocaleString('tr-TR', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : '';
const pdfAdi = (yol: string) => yol.split('/').pop()?.replace(/\.pdf$/i, '').replace(/^\s*\d+\s*\)\s*/, '') || yol;

function taslakKategorisi(t: Taslak): Exclude<Filtre, 'hepsi'> {
  if (t.yayin?.durum === 'denetim_hatasi' || (t.yayin?.durum === 'yayinlandi' && t.yayin.site_derlendi === false)) return 'hata';
  if (t.durum === 'yayinlandi') return 'yayinda';
  if (t.durum === 'reddedildi' || t.karar?.karar === 'reddet') return 'reddedildi';
  if (t.karar?.karar === 'onayla') return 'onaylandi';
  if (t.karar?.karar === 'duzelt') return 'duzelt';
  if (t.durum === 'onay_bekliyor') return 'onay';
  return 'isleniyor';
}

/** İşçi /olaylar: günlükten iş yaşam döngüsü (Drive'dan gelen PDF kuyruğa alındı → işleniyor → taslak → karar). */
interface OlayAkisi {
  son_tarama: { zaman: number; yeni: number } | null;
  olaylar: { zaman: number; tur: 'kuyruga' | 'isleniyor' | 'taslak' | 'karar' | 'yeniden' | 'simdi' | 'panel' | 'hata'; metin: string }[];
}
const OLAY_ETIKET: Record<OlayAkisi['olaylar'][number]['tur'], { label: string; cls: string }> = {
  kuyruga: { label: "Drive'dan yeni PDF · kuyruğa alındı", cls: 'is-accent' },
  isleniyor: { label: 'İşlenmeye başladı', cls: '' },
  taslak: { label: 'Taslak hazır', cls: 'is-ok' },
  karar: { label: 'Karar', cls: '' },
  yeniden: { label: 'Yeniden kuyrukta', cls: '' },
  simdi: { label: 'Panelden hemen işle', cls: 'is-accent' },
  panel: { label: 'Panel', cls: '' },
  hata: { label: 'Hata', cls: 'is-bad' },
};

/** Drive etkinliği: son tarama + son 24 saatte kuyruğa alınan PDF'ler öne çıkar, altında açılır olay akışı. */
const DriveEtkinligi: React.FC<{ akis: OlayAkisi }> = ({ akis }) => {
  const gun = Date.now() / 1000 - 86400;
  const yeniler = akis.olaylar.filter((o) => o.tur === 'kuyruga' && o.zaman >= gun);
  const pdf = (m: string) => pdfAdi(m.split(' → ')[0]);
  return (
    <div className="mb-2" style={{ padding: '10px 12px', border: '1px solid var(--color-line)', borderRadius: 10 }}>
      <p className="text-sm text-ink-2" style={{ margin: 0 }}>
        <b>Drive etkinliği</b> · son tarama {akis.son_tarama ? `${saat(akis.son_tarama.zaman)} (${akis.son_tarama.yeni} yeni PDF kuyruğa alındı)` : 'kaydı yok'}
      </p>
      {yeniler.length > 0 && (
        <ul className="flex flex-col gap-1 mt-2" style={{ margin: '8px 0 0', padding: 0, listStyle: 'none' }}>
          {yeniler.map((o) => (
            <li key={o.zaman + o.metin} className="text-sm">
              <span className="ms-tag is-accent">Yeni PDF kuyruğa alındı</span> <b>{pdf(o.metin)}</b>
              <span className="text-ink-3"> · {saat(o.zaman)}{o.metin.includes(' → ') ? ` · ${o.metin.split(' → ').slice(1).join(' → ')}` : ''}</span>
            </li>
          ))}
        </ul>
      )}
      <details className="mt-2">
        <summary className="text-sm text-ink-2" style={{ cursor: 'pointer' }}>Son {akis.olaylar.length} olay</summary>
        <ul className="flex flex-col gap-1 mt-2" style={{ padding: 0, listStyle: 'none' }}>
          {akis.olaylar.map((o) => (
            <li key={o.zaman + o.tur + o.metin} className="text-sm">
              <span className="text-ink-3">{saat(o.zaman)}</span> <span className={`ms-tag ${OLAY_ETIKET[o.tur].cls}`}>{OLAY_ETIKET[o.tur].label}</span>{' '}
              {o.tur === 'kuyruga' || o.tur === 'isleniyor' ? pdf(o.metin) : o.metin}
            </li>
          ))}
        </ul>
      </details>
    </div>
  );
};

function satirlariKur(liste: Taslak[], kuyruk: KuyrukIs[], zam: Zamanlama | null, konular: KonuSatiri[]): Satir[] {
  const taslakMap = new Map(liste.map((t) => [t.is_id, t]));
  const plan = new Map((zam?.plan || []).map((p) => [p.is_id, p.tahmini]));
  const out: Satir[] = [];
  const kuyruktaAktif = new Set<string>();
  const simdi = Date.now() / 1000;
  for (const j of kuyruk) {
    if (!['bekliyor', 'isleniyor', 'hata'].includes(j.durum)) continue; // 'taslak': taslak listesinden gelir
    kuyruktaAktif.add(j.is_id);
    const t = taslakMap.get(j.is_id);
    const kat = j.durum === 'bekliyor' ? 'programlandi' : j.durum === 'isleniyor' ? 'isleniyor' : 'hata';
    const tahmini = plan.get(j.is_id) ?? (j.sonra && j.sonra > simdi ? j.sonra : undefined);
    out.push({
      anahtar: 'k:' + j.is_id,
      kat,
      baslik: t?.program?.konu || (j.konular || []).filter(Boolean).join(' · ') || pdfAdi(j.yol),
      etiketler: [j.yol.split('/').slice(-2, -1)[0] || '', t?.karar?.karar === 'duzelt' ? 'düzeltme turu' : '', j.deneme ? `deneme ${j.deneme}` : ''].filter(Boolean),
      mesaj: j.son_mesaj,
      uyari: j.uyari,
      zamanNot:
        kat === 'programlandi'
          ? tahmini
            ? `Planlanan başlama: ~${saat(tahmini)}${zam ? ` (günde ≤${zam.gunluk_sinir}, iki ders arası ${Math.round(zam.ders_arasi_sn / 60)} dk)` : ''}`
            : zam?.duraklat
              ? 'İşçi duraklatıldı; "Hemen işle" ile yine başlatabilirsin'
              : 'Bir dakika içinde başlar'
          : kat === 'isleniyor'
            ? `Başladı: ${saat(j.basladi)}`
            : `Eklendi: ${saat(j.eklendi)}`,
      taslak: t,
    });
  }
  for (const t of liste) {
    if (kuyruktaAktif.has(t.is_id)) continue;
    const kat = taslakKategorisi(t);
    out.push({
      anahtar: 't:' + t.is_id,
      kat,
      baslik: t.program?.konu || t.ders_id || t.is_id,
      etiketler: [t.program?.ders || '', t.program?.kurul ? `K${t.program.kurul}` : '', t.mod === 'guncelleme' ? `güncelleme · ${t.deste_id}` : 'yeni ders'].filter(Boolean),
      mesaj: t.ozet,
      uyari: t.uyari,
      zamanNot:
        kat === 'yayinda' && t.yayin?.yayin_zamani
          ? `Yayın: ${t.yayin.yayin_zamani}`
          : kat === 'onaylandi'
            ? 'Sunucu en geç 10 dakika içinde siteye ekler'
            : t.zaman
              ? saat(t.zaman)
              : undefined,
      taslak: t,
    });
  }
  for (const k of konular) {
    if (k.durum !== 'islenmeli' && k.durum !== 'yenilenmeli') continue;
    out.push({
      anahtar: `c:${k.kurul}:${k.ders}:${k.konu}`,
      kat: k.durum === 'islenmeli' ? 'goruldu' : 'yenilenmeli',
      baslik: k.konu || '?',
      etiketler: [k.ders || '', k.kurul ? `K${k.kurul}` : '', k.tarih || '', k.deste_id ? `deste · ${k.deste_id}` : ''].filter(Boolean),
      mesaj:
        k.durum === 'islenmeli'
          ? '26-27 PDF\'i algılandı, ders henüz yok. Otomatik kuyruk açıksa bir sonraki taramada kuyruğa girer; "Kuyruğa al" ile hemen alabilirsin.'
          : 'Ders geçen yılın kaynağıyla hazırlanmış; bu yılın PDF\'i geldi, yeniden üretilmeli.',
      zamanNot: (k.pdf_2627 || []).map((p) => `PDF: ${p.pdf}${p.sayfa && p.sayfa !== 'tümü' ? ` (s. ${p.sayfa})` : ''}`).join(' · ') || undefined,
      pdfler: (k.pdf_2627 || []).map((p) => p.pdf).filter(Boolean),
    });
  }
  return out;
}

const DURUM: Record<string, { label: string; cls: string }> = {
  onay_bekliyor: { label: 'Onay bekliyor', cls: 'is-warn' },
  isleniyor: { label: 'İşleniyor', cls: '' },
  onayla: { label: 'Onaylandı', cls: 'is-ok' },
  reddet: { label: 'Reddedildi', cls: 'is-bad' },
  duzelt: { label: 'Düzeltme istendi', cls: 'is-warn' },
  yayinlandi: { label: 'Yayınlandı', cls: 'is-ok' },
  reddedildi: { label: 'Reddedildi', cls: 'is-bad' },
};

const ManageDersRevizeSection = React.lazy(() => import('./ManageDersRevizeSection').then((m) => ({ default: m.ManageDersRevizeSection })));

type Kategori = 'otomatik' | 'revize';

/** Yeni dersler: Otomatik (Oracle'daki işçi, Drive'dan) ve Revize (cihazda yeniden üretilen mevcut dersler). */
export const ManageDersIsciSection: React.FC<{ adminEmail: string }> = ({ adminEmail }) => {
  const [kategori, setKategori] = useState<Kategori>(() => {
    try {
      return (localStorage.getItem('manage:dersIsciKategori') as Kategori) || 'otomatik';
    } catch {
      return 'otomatik';
    }
  });
  const sec = (k: Kategori) => {
    setKategori(k);
    try {
      localStorage.setItem('manage:dersIsciKategori', k);
    } catch {}
  };
  return (
    <div className="flex flex-col gap-3">
      <ChipBar<Kategori>
        label="Ders işçisi kategorisi"
        value={kategori}
        onChange={sec}
        options={[
          { id: 'otomatik', label: 'Otomatik Ders İşçisi' },
          { id: 'revize', label: 'Revize Ders İşçisi' },
        ]}
      />
      {kategori === 'otomatik' ? (
        <OtomatikDersIsci adminEmail={adminEmail} />
      ) : (
        <Suspense fallback={<p className="text-sm text-ink-2">Yükleniyor…</p>}>
          <ManageDersRevizeSection adminEmail={adminEmail} />
        </Suspense>
      )}
    </div>
  );
};

const OtomatikDersIsci: React.FC<{ adminEmail: string }> = ({ adminEmail }) => {
  const headers = useMemo(() => ({ 'Content-Type': 'application/json', 'x-admin-email': adminEmail || '' }), [adminEmail]);
  const [liste, setListe] = useState<Taslak[] | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const [ozet, setOzet] = useState<{ sayim?: Record<string, number>; uretim?: string } | null>(null);
  const [secili, setSecili] = useState<string | null>(null);
  const [ayr, setAyr] = useState<Ayrinti | null>(null);
  const [sekme, setSekme] = useState<Sekme>('rapor');
  const [filtre, setFiltreHam] = useState<Filtre>(() => {
    try {
      return (localStorage.getItem('manage:dersIsciFiltre') as Filtre) || 'onay';
    } catch {
      return 'onay';
    }
  });
  const setFiltre = (f: Filtre) => {
    setFiltreHam(f);
    try {
      localStorage.setItem('manage:dersIsciFiltre', f);
    } catch {}
  };
  const [kuyruk, setKuyruk] = useState<KuyrukIs[]>([]);
  const [zam, setZam] = useState<Zamanlama | null>(null);
  const [konular, setKonular] = useState<KonuSatiri[]>([]);
  const [olay, setOlay] = useState<OlayAkisi | null>(null);
  const [dosya, setDosya] = useState<Record<string, any>>({});
  const [onizle, setOnizle] = useState<any | null>(null);
  const [not, setNot] = useState('');
  const [busy, setBusy] = useState(false);

  const api = (yol: string, init?: RequestInit) => safeJsonFetch<any>(`/api/admin/ders-isci${yol}`, { headers, ...init });

  const [tazele, setTazele] = useState(0);
  const yukle = async () => {
    setTazele((n) => n + 1);
    setHata(null);
    // /kuyruk ve /zamanlama isteğe bağlı: eski işçi sürümünde yoksa yalnız taslak/checklist kategorileri dolar
    const [t, c, k, z, o] = await Promise.all([api('/taslaklar'), api('/checklist'), api('/kuyruk'), api('/zamanlama'), api('/olaylar')]);
    setOlay(o.ok && o.data && Array.isArray(o.data.olaylar) ? o.data : null);
    if (!t.ok) {
      setHata((t.data as any)?.hata || 'Ders işçisine ulaşılamıyor.');
      setListe([]);
      return;
    }
    setListe(t.data || []);
    if (c.ok && c.data) {
      setOzet({ sayim: c.data.sayim, uretim: c.data.uretim });
      setKonular(Array.isArray(c.data.konular) ? c.data.konular : []);
    }
    setKuyruk(k.ok && Array.isArray(k.data) ? k.data : []);
    setZam(z.ok && z.data && Array.isArray(z.data.plan) ? z.data : null);
  };
  useEffect(() => {
    yukle();
    // Canlı: sekme görünürken 20 sn'de bir sessizce tazele (kuyruk, işlenen ders, olaylar)
    const t = window.setInterval(() => {
      if (document.visibilityState === 'visible') yukle();
    }, 20000);
    return () => window.clearInterval(t);
  }, []);

  useEffect(() => {
    if (!secili) return;
    setAyr(null);
    setDosya({});
    setNot('');
    setSekme('rapor');
    api(`/taslak/${secili}`).then((r) => (r.ok ? setAyr(r.data) : toast.error('Taslak alınamadı.')));
  }, [secili]);

  const dosyaAl = async (ad: string) => {
    if ((dosya[ad] !== undefined && dosya[ad] !== null) || !secili) return dosya[ad];
    const iste = () => fetch(`/api/admin/ders-isci/taslak/${secili}/dosya/${ad}`, { headers }).catch(() => null);
    let r = await iste();
    if (!r || !r.ok) {
      await new Promise((t) => setTimeout(t, 1500)); // geçici aksaklık (yeniden başlatma, ağ): bir kez daha dene
      r = await iste();
    }
    if (!r || !r.ok) {
      setDosya((d) => ({ ...d, [ad]: null })); // önbelleğe "kalıcı" yazılmaz: sekmeye/düğmeye yeniden basınca tekrar denenir
      return null;
    }
    const txt = await r.text();
    const v = ad.endsWith('.jsonl') ? txt.split('\n').filter(Boolean).map((x) => JSON.parse(x)) : ad.endsWith('.json') ? JSON.parse(txt) : txt;
    setDosya((d) => ({ ...d, [ad]: v }));
    return v;
  };
  useEffect(() => {
    const ad = { sorular: 'ornek_sorular.json', sozluk: 'sozluk.json', hastaliklar: 'hastaliklar.json', havuz: 'bilgi_havuzu.jsonl', cikmis: 'cikmis_baglantilari.json' }[sekme as string];
    if (ad) dosyaAl(ad);
  }, [sekme, secili]);

  const karar = async (k: 'onayla' | 'reddet' | 'duzelt') => {
    if (!secili) return;
    if (k !== 'onayla' && !not.trim()) return toast.error('Reddetme ya da düzeltme için kısa bir not yaz.');
    setBusy(true);
    const r = await api(`/taslak/${secili}/karar`, { method: 'POST', body: JSON.stringify({ karar: k, not }) });
    setBusy(false);
    if (!r.ok) return toast.error((r.data as any)?.hata || 'Karar kaydedilemedi.');
    toast.success(k === 'onayla' ? 'Onaylandı; yayına birleştirme sırasına alındı.' : k === 'reddet' ? 'Reddedildi.' : 'Düzeltme istendi.');
    await yukle();
    api(`/taslak/${secili}`).then((x) => x.ok && setAyr(x.data));
  };

  const yenidenGonder = async () => {
    if (!secili) return;
    setBusy(true);
    const r = await api(`/taslak/${secili}/yeniden`, { method: 'POST', body: '{}' });
    setBusy(false);
    if (!r.ok) return toast.error((r.data as any)?.hata || 'Yeniden gönderilemedi.');
    toast.success('Yeniden gönderildi; sunucu en geç 10 dakika içinde yeniden dener.');
    await yukle();
    api(`/taslak/${secili}`).then((x) => x.ok && setAyr(x.data));
  };

  const kuyrukEylem = async (isId: string, eylem: 'one-al' | 'sona-at' | 'kaldir' | 'yeniden-dene', baslik: string) => {
    if (eylem === 'kaldir' && !window.confirm(`"${baslik}" kuyruktan çıkarılsın mı? Bu PDF bir daha kendiliğinden kuyruğa alınmaz ("Kuyruğa al" ile yine alınabilir).`)) return;
    setBusy(true);
    const r = await api(`/kuyruk/${isId}/${eylem}`, { method: 'POST', body: '{}' });
    setBusy(false);
    if (!r.ok) return toast.error((r.data as any)?.hata || 'Yapılamadı.');
    toast.success({ 'one-al': 'Sıranın başına alındı.', 'sona-at': 'Sıranın sonuna alındı.', kaldir: 'Kuyruktan çıkarıldı.', 'yeniden-dene': 'Yeniden kuyrukta.' }[eylem]);
    await yukle();
  };
  const kuyrugaAl = async (yollar: string[], baslik: string) => {
    if (!yollar.length) return toast.error('Bu konunun 2026-27 PDF\'i yok.');
    setBusy(true);
    const r = await api('/pdf/kuyruga', { method: 'POST', body: JSON.stringify({ yollar }) });
    setBusy(false);
    if (!r.ok) return toast.error((r.data as any)?.hata || 'Kuyruğa alınamadı.');
    toast.success(`"${baslik}" kuyruğa alınıyor; işçi bir dakika içinde ekler.`);
    await yukle();
  };
  const esikAtla = async () => {
    if (!secili || !window.confirm('Ders notu sadakat eşiği bu taslak için yok sayılsın ve yeniden yayına gönderilsin mi?')) return;
    setBusy(true);
    const r = await api(`/taslak/${secili}/esik-atla`, { method: 'POST', body: '{}' });
    setBusy(false);
    if (!r.ok) return toast.error((r.data as any)?.hata || 'Gönderilemedi.');
    toast.success('Yeniden gönderildi; sunucu en geç 10 dakika içinde yayınlar.');
    await yukle();
    api(`/taslak/${secili}`).then((x) => x.ok && setAyr(x.data));
  };

  // Programlanmış dersi zamanlayıcıyı (saat penceresi, günlük sınır, ders arası) beklemeden başlat
  const hemenIsle = async (isId: string, baslik: string) => {
    if (!window.confirm(`"${baslik}" zamanlayıcı beklenmeden şimdi işlensin mi? (yaklaşık 30–60 dk sürer; sonraki ders bundan sonraki ders arası kadar bekler)`)) return;
    setBusy(true);
    const r = await api(`/kuyruk/${isId}/simdi`, { method: 'POST', body: '{}' });
    setBusy(false);
    if (!r.ok) return toast.error((r.data as any)?.hata || 'Başlatılamadı.');
    toast.success('İşleme alındı; ders işçisi şimdi başladı.');
    await yukle();
  };

  const satirlar = useMemo(() => satirlariKur(liste || [], kuyruk, zam, konular), [liste, kuyruk, zam, konular]);
  const sayim = useMemo(() => {
    const n: Partial<Record<Filtre, number>> = {};
    for (const x of satirlar) n[x.kat] = (n[x.kat] || 0) + 1;
    return n;
  }, [satirlar]);
  // Seçili süzgeç boşsa (ör. kayıtlı 'Onay bekliyor' artık 0) ilk dolu kategoriye geç; boş liste görünmesin
  useEffect(() => {
    if (!liste || filtre === 'hepsi' || sayim[filtre]) return;
    const ilk = SIRA.find((id) => sayim[id]);
    if (ilk) setFiltreHam(ilk);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [liste, sayim]);
  const isciDurum = useMemo<IsciDurum>(() => {
    const c = kuyruk.find((j) => j.durum === 'isleniyor');
    const t = c ? (liste || []).find((x) => x.is_id === c.is_id) : undefined;
    return {
      calisan: c ? { baslik: t?.program?.konu || (c.konular || []).filter(Boolean).join(' · ') || pdfAdi(c.yol), basladi: c.basladi } : null,
      bugun: zam?.bugun_islenen ?? 0,
      sonraki: zam?.plan?.[0]?.tahmini,
      bekleyen: kuyruk.filter((j) => j.durum === 'bekliyor').length,
      sonTarama: olay?.son_tarama?.zaman,
    };
  }, [kuyruk, liste, zam, olay]);
  const gorunen = satirlar
    .filter((x) => filtre === 'hepsi' || x.kat === filtre)
    .sort((a, b) => (filtre === 'hepsi' ? SIRA.indexOf(a.kat) - SIRA.indexOf(b.kat) : 0));

  const s = ayr?.sayilar || {};
  return (
    <div className="flex flex-col gap-3">
      {!hata && <IsciKontrol api={api} durum={isciDurum} onDegisti={yukle} tazele={tazele} />}
      <Panel
        title="Otomatik Ders İşçisi"
        icon={BookOpenCheck}
        count={liste ? satirlar.length : undefined}
        desc="Drive'a eklenen ders PDF'lerinden ders işçisinin ürettiği paketler. İncele, önizle, karar ver; onaylananlar yayına birleştirilir."
        tools={
          <button type="button" className="ms-btn is-sm" onClick={yukle}>
            <RefreshCw aria-hidden /> Yenile
          </button>
        }
      >
        {ozet?.sayim && (
          <p className="text-sm text-ink-2 mb-2">
            <b>2026-27 checklist</b> ({ozet.uretim}): tamam {ozet.sayim.tamam_2627 || 0} · onay bekliyor {ozet.sayim.onay_bekliyor || 0} ·
            kuyrukta {(ozet.sayim.kuyrukta || 0) + (ozet.sayim.isleniyor || 0)} · yenilenmeli {ozet.sayim.yenilenmeli || 0} · işlenmeli{' '}
            {ozet.sayim.islenmeli || 0} · geçen yıl kaynaklı {ozet.sayim.gecen_yil_kaynakli || 0} · PDF bekleniyor {ozet.sayim.pdf_bekleniyor || 0}
          </p>
        )}
        {olay && <DriveEtkinligi akis={olay} />}
        <ChipBar<Filtre>
          label="Ders durumu süzgeci"
          wrap
          value={filtre}
          onChange={setFiltre}
          options={[
            ...SIRA.filter((id) => sayim[id] || id === filtre || id === 'onay').map((id) => ({
              id,
              label: KATEGORI[id].label,
              icon: KATEGORI[id].icon,
              n: sayim[id] || 0,
            })),
            { id: 'hepsi' as Filtre, label: 'Hepsi', icon: Layers, n: satirlar.length },
          ]}
        />
        {hata && <EmptyState icon={FileWarning} title="Ders işçisine ulaşılamıyor">{hata}</EmptyState>}
        {!hata && liste && gorunen.length === 0 && <EmptyState icon={ClipboardList} title="Bu kategoride ders yok" />}
        <ul className="flex flex-col gap-2 mt-2">
          {gorunen.map((x) => {
            const d = KATEGORI[x.kat];
            const icerik = (
              <>
                <div className="flex flex-wrap items-center gap-2">
                  <b className="min-w-0">{x.baslik}</b>
                  {x.etiketler.map((e) => (
                    <span key={e} className="ms-tag">
                      {e}
                    </span>
                  ))}
                  <span className={`ms-tag ${d.cls}`}>{d.label}</span>
                </div>
                {x.mesaj && <p className="text-sm text-ink-2 mt-1">{x.mesaj}</p>}
                {x.zamanNot && <p className="text-xs text-ink-3 mt-1">{x.zamanNot}</p>}
                {x.uyari && <p className="text-sm text-warn mt-1">⚠ {x.uyari}</p>}
              </>
            );
            const id = x.taslak?.is_id;
            return (
              <li key={x.anahtar}>
                {id ? (
                  <button
                    type="button"
                    onClick={() => setSecili(id)}
                    aria-pressed={secili === id}
                    className={`ms-panel w-full text-left p-3 ${secili === id ? 'is-on' : ''}`}
                  >
                    {icerik}
                  </button>
                ) : (
                  <div className="ms-panel w-full p-3">{icerik}</div>
                )}
                {x.anahtar.startsWith('k:') && (x.kat === 'programlandi' || x.kat === 'hata') && (
                  <div className="flex flex-wrap justify-end gap-1.5 mt-1">
                    <button type="button" className="ms-btn is-sm is-primary" disabled={busy} onClick={() => hemenIsle(x.anahtar.slice(2), x.baslik)}>
                      <Play aria-hidden /> Hemen işle
                    </button>
                    {x.kat === 'programlandi' ? (
                      <>
                        <button type="button" className="ms-btn is-sm" disabled={busy} onClick={() => kuyrukEylem(x.anahtar.slice(2), 'one-al', x.baslik)}>
                          <ArrowUp aria-hidden /> Öne al
                        </button>
                        <button type="button" className="ms-btn is-sm" disabled={busy} onClick={() => kuyrukEylem(x.anahtar.slice(2), 'sona-at', x.baslik)}>
                          <ArrowDown aria-hidden /> Sona at
                        </button>
                      </>
                    ) : (
                      <button type="button" className="ms-btn is-sm" disabled={busy} onClick={() => kuyrukEylem(x.anahtar.slice(2), 'yeniden-dene', x.baslik)}>
                        <RotateCcw aria-hidden /> Yeniden dene
                      </button>
                    )}
                    <button type="button" className="ms-btn is-sm is-ghost" disabled={busy} onClick={() => kuyrukEylem(x.anahtar.slice(2), 'kaldir', x.baslik)}>
                      <Trash2 aria-hidden /> Kuyruktan çıkar
                    </button>
                  </div>
                )}
                {(x.kat === 'goruldu' || x.kat === 'yenilenmeli') && !!x.pdfler?.length && (
                  <div className="flex justify-end mt-1">
                    <button type="button" className="ms-btn is-sm" disabled={busy} onClick={() => kuyrugaAl(x.pdfler || [], x.baslik)}>
                      <ListPlus aria-hidden /> Kuyruğa al
                    </button>
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      </Panel>

      {secili && (
        <Panel
          title={ayr?.program?.konu || 'Taslak yükleniyor…'}
          icon={Library}
          desc={
            ayr
              ? `${ayr.program?.ders || ''} · Kurul ${ayr.program?.kurul ?? '?'} · ${ayr.program?.ogretim_uyesi || 'hoca belirsiz'} · program eşleşmesi: ${ayr.program?.guven || '?'} · PDF: ${ayr.pdf || ''}`
              : undefined
          }
        >
          {ayr && (
            <>
              <p className="text-sm mb-2">
                <b>{s.slayt || 0}</b> slayt · <b>{s.soru || 0}</b> soru · <b>{s.terim || 0}</b> terim · <b>{s.hastalik || 0}</b> hastalık ·{' '}
                <b>{s.havuz || 0}</b> bilgi · <b>{s.bag || 0}</b> çıkmış bağı · <b>{ayr.referans || 0}</b> kitaptan tamamlanan · denetim{' '}
                <b className={ayr.denetim_hata ? 'text-bad' : 'text-ok'}>{ayr.denetim_hata ?? '?'} hata</b>
              </p>
              {ayr.uyari && <p className="text-sm text-warn mb-2">⚠ {ayr.uyari}</p>}
              <ChipBar<Sekme>
                label="Taslak bölümleri"
                wrap
                value={sekme}
                onChange={setSekme}
                options={[
                  { id: 'rapor', label: 'Rapor' },
                  { id: 'deste', label: 'Deste', n: s.slayt },
                  { id: 'sorular', label: 'Sorular', n: s.soru },
                  { id: 'sozluk', label: 'Sözlük', n: s.terim },
                  { id: 'hastaliklar', label: 'Hastalıklar', n: s.hastalik },
                  { id: 'havuz', label: 'Bilgi havuzu', n: s.havuz },
                  { id: 'cikmis', label: 'Çıkmış bağları', n: s.bag },
                  { id: 'kaynak', label: 'Kitaptan', n: ayr.referans },
                ]}
              />
              <div className="mt-3">
                {sekme === 'rapor' && <NoteMarkdown text={ayr.rapor || '_Rapor yok._'} />}
                {sekme === 'deste' && (
                  <div className="flex flex-col gap-2">
                    <p className="text-sm text-ink-2">
                      Deste, sitedeki ders oynatıcısıyla açılır; öğrencinin göreceğinin aynısıdır. Kimlik: <code>{ayr.deste_id}</code>
                      {ayr.mod === 'guncelleme' ? ' (onaylanırsa mevcut destenin yerine geçer)' : ' (yeni deste)'}.
                    </p>
                    <button
                      type="button"
                      className="ms-btn is-primary self-start"
                      onClick={async () => {
                        const d = await dosyaAl('deck.json');
                        if (d) setOnizle(d);
                        else toast.error('Deste dosyası alınamadı.');
                      }}
                    >
                      <Eye aria-hidden /> Desteyi önizle
                    </button>
                  </div>
                )}
                {sekme === 'sorular' && <Sorular veri={dosya['ornek_sorular.json']} />}
                {sekme === 'sozluk' && <Sozluk veri={dosya['sozluk.json']} />}
                {sekme === 'hastaliklar' && <Hastaliklar veri={dosya['hastaliklar.json']} />}
                {sekme === 'havuz' && <Havuz veri={dosya['bilgi_havuzu.jsonl']} />}
                {sekme === 'cikmis' && <Cikmis veri={dosya['cikmis_baglantilari.json']} />}
                {sekme === 'kaynak' && (
                  <ul className="flex flex-col gap-1 text-sm">
                    {(ayr.denetim?.referansla_tamamlanan || []).map((r, i) => (
                      <li key={i}>📚 {r}</li>
                    ))}
                    {!ayr.denetim?.referansla_tamamlanan?.length && <li>Kitaptan tamamlanan bilgi yok; her bilgi ders PDF'inden alıntıyla doğrulandı.</li>}
                  </ul>
                )}
              </div>

              <div className="mt-4 border-t border-line pt-3 flex flex-col gap-2">
                {ayr.karar ? (
                  <>
                    <p className="text-sm">
                      Karar: <b>{DURUM[ayr.karar.karar]?.label}</b>
                      {ayr.karar.not ? ` — ${ayr.karar.not}` : ''}
                      {ayr.karar.kim ? ` (${ayr.karar.kim})` : ''}
                      {ayr.karar.karar === 'onayla' &&
                        (ayr.yayin?.durum === 'yayinlandi' && ayr.yayin.site_derlendi === false
                          ? ' · Kaynaklara yazıldı ama site derlenemedi.'
                          : ayr.durum === 'yayinlandi'
                          ? ' · Sitede yayında.'
                          : ayr.yayin?.durum === 'denetim_hatasi'
                            ? ' · Yayınlanamadı (yayın denetimi):'
                            : ' · Sunucu en geç 10 dakika içinde siteye ekler.')}
                    </p>
                    {ayr.yayin?.durum === 'denetim_hatasi' && (
                      <ul className="text-sm text-ink-2 list-disc pl-5">
                        {(ayr.yayin.hatalar || []).slice(0, 8).map((h) => (
                          <li key={h}>{h}</li>
                        ))}
                      </ul>
                    )}
                    {ayr.yayin?.durum === 'denetim_hatasi' && (
                      <>
                        <p className="text-sm text-ink-2">
                          {(ayr.yayin.hatalar || []).every((h) => h.includes('sadakati'))
                            ? 'Yalnız sadakat eşiğine takıldı: eşiği bu ders için yok sayabilir ya da düzeltme isteyebilirsin.'
                            : 'Bu hata yeniden göndermekle geçmez: düzeltme iste (işçi notunla yeniden üretir) ya da reddet.'}
                        </p>
                        <textarea
                          aria-label="Düzeltme ya da ret notu"
                          className="ms-input min-h-[64px]"
                          placeholder="Düzeltme ya da ret notu"
                          value={not}
                          onChange={(e) => setNot(e.target.value)}
                        />
                        <div className="flex flex-wrap gap-2">
                          {(ayr.yayin.hatalar || []).every((h) => h.includes('sadakati')) && (
                            <button type="button" disabled={busy} className="ms-btn is-ok" onClick={esikAtla}>
                              <ShieldOff aria-hidden /> Eşiği yok say ve yayınla
                            </button>
                          )}
                          <button type="button" disabled={busy} className="ms-btn" onClick={() => karar('duzelt')}>
                            <PenLine aria-hidden /> Düzeltme iste
                          </button>
                          <button type="button" disabled={busy} className="ms-btn is-bad" onClick={() => karar('reddet')}>
                            <XCircle aria-hidden /> Reddet
                          </button>
                        </div>
                      </>
                    )}
                    {ayr.karar.karar === 'onayla' &&
                      ayr.yayin &&
                      ayr.yayin.durum !== 'denetim_hatasi' &&
                      (ayr.yayin.durum !== 'yayinlandi' || ayr.yayin.site_derlendi === false) && (
                        <button type="button" disabled={busy} className="ms-btn is-bad self-start" onClick={yenidenGonder}>
                          <RotateCcw aria-hidden /> {ayr.yayin.durum === 'yayinlandi' ? 'Siteyi yeniden derle' : 'Yeniden gönder'}
                        </button>
                      )}
                  </>
                ) : ayr.durum === 'onay_bekliyor' ? (
                  <>
                    <label className="text-sm text-ink-2" htmlFor="isci-not">
                      Not (reddetme ya da düzeltme için gerekli; düzeltmede işçi bu notla taslağı yeniden üretir)
                    </label>
                    <textarea id="isci-not" className="ms-input min-h-[72px]" value={not} onChange={(e) => setNot(e.target.value)} />
                    <div className="flex flex-wrap gap-2">
                      <button type="button" disabled={busy} className="ms-btn is-ok" onClick={() => karar('onayla')}>
                        <CheckCircle2 aria-hidden /> Onayla
                      </button>
                      <button type="button" disabled={busy} className="ms-btn" onClick={() => karar('duzelt')}>
                        <PenLine aria-hidden /> Düzeltme iste
                      </button>
                      <button type="button" disabled={busy} className="ms-btn is-bad" onClick={() => karar('reddet')}>
                        <XCircle aria-hidden /> Reddet
                      </button>
                    </div>
                  </>
                ) : (
                  <p className="text-sm text-ink-2">Taslak hâlâ işleniyor.</p>
                )}
              </div>
            </>
          )}
        </Panel>
      )}

      {onizle && (
        <Suspense fallback={null}>
          <LessonPlayer deck={onizle} startAt={0} onProgress={() => {}} onClose={() => setOnizle(null)} />
        </Suspense>
      )}
    </div>
  );
};

const Yukleniyor: React.FC<{ veri: any }> = ({ veri }) =>
  veri === undefined ? <p className="text-sm text-ink-2">Yükleniyor…</p> : veri === null ? <p className="text-sm text-bad">Dosya alınamadı.</p> : null;

const Kanit: React.FC<{ k?: any }> = ({ k }) =>
  !k ? null : k.referans ? (
    <span className="text-xs text-ink-3">📚 {k.referans}</span>
  ) : (
    <span className="text-xs text-ink-3">
      s.{k.sayfa}: “{k.alinti}”
    </span>
  );

export const Sorular: React.FC<{ veri: any }> = ({ veri }) => {
  if (!veri) return <Yukleniyor veri={veri} />;
  return (
    <ol className="flex flex-col gap-3">
      {(veri.sorular || []).map((q: any) => (
        <li key={q.id} className="text-sm">
          <p>
            <span className="ms-tag">{q.zorluk}</span> <span className="ms-tag">kazanım {q.kazanim}</span> {q.soru}
          </p>
          <ul className="ml-4 mt-1">
            {Object.entries(q.secenekler || {}).map(([h, m]) => (
              <li key={h} className={h === q.dogru ? 'text-ok font-semibold' : ''}>
                {h}) {String(m)}
              </li>
            ))}
          </ul>
          <details className="mt-1">
            <summary className="cursor-pointer text-ink-2">Açıklama</summary>
            <p className="mt-1">{q.aciklama}</p>
            <Kanit k={q.kanit} />
          </details>
        </li>
      ))}
    </ol>
  );
};

export const Sozluk: React.FC<{ veri: any }> = ({ veri }) => {
  if (!veri) return <Yukleniyor veri={veri} />;
  return (
    <div className="flex flex-col gap-3 text-sm">
      <b>Yeni terimler ({(veri.yeni || []).length})</b>
      {(veri.yeni || []).map((t: any, i: number) => (
        <p key={i}>
          <b>{t.term}</b> <span className="ms-tag">{t.category}</span> — {t.definition} <Kanit k={t.kanit} />
        </p>
      ))}
      <b>Zenginleştirilen ({(veri.zenginlestir || []).length})</b>
      {(veri.zenginlestir || []).map((t: any, i: number) => (
        <p key={i}>
          <b>{t.key}</b>: {t.definition || t.pearl || ''} <span className="text-ink-3">({t.neden})</span> <Kanit k={t.kanit} />
        </p>
      ))}
    </div>
  );
};

const ALANLAR: [string, string][] = [
  ['etiology', 'Etiyoloji'],
  ['physiology_pathophysiology', 'Patofizyoloji'],
  ['morphology_pathology', 'Morfoloji'],
  ['symptoms_clinical', 'Klinik'],
  ['pathognomonic_features', 'Patognomonik'],
  ['diagnostic_methods', 'Tanı'],
  ['imaging_findings', 'Görüntüleme'],
  ['treatment', 'Tedavi'],
];

export const Hastaliklar: React.FC<{ veri: any }> = ({ veri }) => {
  if (!veri) return <Yukleniyor veri={veri} />;
  return (
    <div className="flex flex-col gap-3 text-sm">
      {(veri || []).map((h: any) => (
        <details key={h.id} className="ms-panel p-2">
          <summary className="cursor-pointer">
            <b>{h.name}</b> {h.mevcut ? <span className="ms-tag">mevcut kayda ekleme</span> : <span className="ms-tag is-ok">yeni</span>}
          </summary>
          {ALANLAR.filter(([a]) => (h[a] || []).length).map(([a, ad]) => (
            <div key={a} className="mt-1">
              <b>{ad}:</b>
              <ul className="ml-4 list-disc">
                {h[a].map((m: string, i: number) => (
                  <li key={i}>
                    {m} <Kanit k={(h.kanitlar || []).find((k: any) => k.alan === a && k.madde === i)} />
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </details>
      ))}
    </div>
  );
};

export const Havuz: React.FC<{ veri: any }> = ({ veri }) => {
  if (!veri) return <Yukleniyor veri={veri} />;
  return (
    <ul className="flex flex-col gap-1 text-sm">
      {(veri || []).map((b: any, i: number) => (
        <li key={i}>
          <span className="ms-tag">{b.tur}</span> <b>{b.varlik}</b> <i>{b.iliski}</i> <b>{b.hedef}</b> — {b.bilgi} <Kanit k={b.kanit} />
        </li>
      ))}
    </ul>
  );
};

export const Cikmis: React.FC<{ veri: any }> = ({ veri }) => {
  if (!veri) return <Yukleniyor veri={veri} />;
  const ilgili = (veri || []).filter((c: any) => c.ilgili);
  return (
    <ul className="flex flex-col gap-2 text-sm">
      {ilgili.map((c: any) => (
        <li key={c.soru_id}>
          <span className={`ms-tag ${c.guven === 'yuksek' ? 'is-ok' : ''}`}>{c.guven}</span> <code>{c.soru_id}</code> → slayt {c.slideNumber}: {c.slideTitle}
          <p className="text-ink-2">{c.gerekce}</p>
        </li>
      ))}
      <li className="text-ink-3">{(veri || []).length - ilgili.length} aday "bu derste anlatılmıyor" diye ayrıldı.</li>
    </ul>
  );
};
