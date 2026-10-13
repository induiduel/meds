import React, { Suspense, useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeftRight, ClipboardList, Copy, Eye, FilePlus2, FileWarning, Library, RefreshCw, RotateCcw, Trash2, Wrench } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';
import { NoteMarkdown } from '../ui/NoteMarkdown';
import { ChipBar, EmptyState, Panel } from './consoleUi';
import { Cikmis, Hastaliklar, Havuz, Sorular, Sozluk } from './ManageDersIsciSection';

const LessonPlayer = React.lazy(() => import('../learn/lesson/LessonPlayer').then((m) => ({ default: m.LessonPlayer })));

/**
 * Revize Ders İşçisi: yayındaki derslerin 2026-27 PDF'inden yeniden üretilmiş taslakları (cihazda, Claude Code oturumu).
 * Her taslak için: Yer değiştir / Güncelle (alternatif varsa) · Ekle (alternatif yoksa) · Her ikisini tut (V1 + V2) · Kaldır.
 * Veri: /api/admin/ders-revize/* (src/services/dersRevizeRoutes.ts) → yayın: scripts/ders_isci/yayinla.py --yerel.
 */
type Olcu = { adim: number; etkilesim: number; kelime: number; boyutKb: number };
type Islem = 'degistir' | 'ekle' | 'kaldir' | 'ikisini_tut';
type Taslak = {
  is_id: string;
  durum: string;
  ozet: string;
  deste_id: string;
  ders_id?: string;
  ders?: string;
  konu?: string;
  pdf?: string;
  denetim_hata?: number;
  sayilar: Record<string, number>;
  referans?: number;
  yeni: (Olcu & { baslik?: string }) | null;
  yayindakiler: (Olcu & { id: string; baslik?: string; surum: string })[];
  alternatif: boolean;
  yayinda?: boolean;
  karar: { karar: string; islem?: Islem; kim?: string } | null;
  yayin: { durum?: string; hatalar?: string[]; kip?: Islem; deste_id?: string; site_derlendi?: boolean; yayin_zamani?: string } | null;
  calisiyor: { asama: string; gunluk: string } | null;
};
type Ayrinti = Taslak & { rapor: string; denetim: { referansla_tamamlanan?: string[] } };
type Sekme = 'rapor' | 'deste' | 'sorular' | 'sozluk' | 'hastaliklar' | 'havuz' | 'cikmis';
type Filtre = 'bekleyen' | 'islenen' | 'hepsi';

const ISLEM_AD: Record<Islem, string> = {
  degistir: 'Yer değiştirildi (güncellendi)',
  ekle: 'Eklendi',
  ikisini_tut: 'İkisi de tutuldu (V1 + V2)',
  kaldir: 'Kaldırıldı',
};

const durumEtiketi = (t: Taslak): { label: string; cls: string } => {
  if (t.calisiyor) return { label: `Yayınlanıyor · ${t.calisiyor.asama}`, cls: 'is-warn' };
  if (t.yayin?.durum === 'yayinlandi') return { label: ISLEM_AD[t.yayin.kip || 'degistir'], cls: 'is-ok' };
  if (t.yayin?.durum === 'yayinlandi' && t.yayin.site_derlendi === false) return { label: 'Yayında · site derlenemedi', cls: 'is-bad' };
  if (t.yayin?.durum === 'kesildi') return { label: 'Yayın kesildi', cls: 'is-bad' };
  if (t.yayin?.durum && t.yayin.durum !== 'yayinlandi') return { label: 'Yayınlanamadı', cls: 'is-bad' };
  if (t.karar?.islem === 'kaldir' || t.durum === 'reddedildi') return { label: 'Kaldırıldı', cls: 'is-bad' };
  if (t.durum === 'onay_bekliyor') return { label: 'Onay bekliyor', cls: 'is-warn' };
  return { label: 'İşleniyor', cls: '' };
};
/** Gönderilmiş ama siteye geçmemiş (hata, kesilme ya da derleme düşmesi): yeniden gönderilebilir. */
const yenidenGonderilebilir = (t: Taslak) =>
  !t.calisiyor &&
  t.karar?.karar === 'onayla' &&
  t.karar?.islem !== 'kaldir' &&
  !!t.yayin &&
  (t.yayin.durum !== 'yayinlandi' || t.yayin.site_derlendi === false);
const bekliyor = (t: Taslak) => t.durum === 'onay_bekliyor' && !t.yayin && !t.calisiyor && t.karar?.islem !== 'kaldir';

const Karsilastir: React.FC<{ t: Taslak }> = ({ t }) => {
  const satirlar: { ad: string; o?: Olcu; yeni?: boolean }[] = [
    ...t.yayindakiler.map((y) => ({ ad: `${y.surum} · yayında`, o: y })),
    { ad: 'Revize taslak', o: t.yeni || undefined, yeni: true },
  ];
  return (
    <table className="text-sm w-full max-w-xl">
      <thead>
        <tr className="text-ink-3 text-left">
          <th className="font-normal py-1">Sürüm</th>
          <th className="font-normal">Adım</th>
          <th className="font-normal">Etkileşim</th>
          <th className="font-normal">Kelime</th>
          <th className="font-normal">Boyut</th>
        </tr>
      </thead>
      <tbody>
        {satirlar.map((s) => (
          <tr key={s.ad} className={s.yeni ? 'font-semibold' : ''}>
            <td className="py-0.5 pr-3">{s.ad}</td>
            <td>{s.o?.adim ?? '–'}</td>
            <td>{s.o?.etkilesim ?? '–'}</td>
            <td>{s.o?.kelime?.toLocaleString('tr-TR') ?? '–'}</td>
            <td>{s.o ? `${s.o.boyutKb} KB` : '–'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export const ManageDersRevizeSection: React.FC<{ adminEmail: string }> = ({ adminEmail }) => {
  const headers = useMemo(() => ({ 'Content-Type': 'application/json', 'x-admin-email': adminEmail || '' }), [adminEmail]);
  const api = (yol: string, init?: RequestInit) => safeJsonFetch<any>(`/api/admin/ders-revize${yol}`, { headers, ...init });
  const [liste, setListe] = useState<Taslak[] | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const [filtre, setFiltre] = useState<Filtre>('bekleyen');
  const [secili, setSecili] = useState<string | null>(null);
  const [ayr, setAyr] = useState<Ayrinti | null>(null);
  const [sekme, setSekme] = useState<Sekme>('rapor');
  const [dosya, setDosya] = useState<Record<string, any>>({});
  const [onizle, setOnizle] = useState<any | null>(null);
  const [busy, setBusy] = useState(false);
  const [calisan, setCalisan] = useState<any>(null);
  const seciliRef = useRef(secili);
  seciliRef.current = secili;

  const yukle = async () => {
    const r = await api('/taslaklar');
    if (!r.ok) {
      setHata((r.data as any)?.hata || 'Revize taslakları alınamadı.');
      setListe([]);
      return;
    }
    setHata(null);
    setListe(r.data?.taslaklar || []);
    setCalisan(r.data?.is || null);
    if (seciliRef.current) {
      const a = await api(`/taslak/${seciliRef.current}`);
      if (a.ok) setAyr(a.data);
    }
  };
  useEffect(() => {
    yukle();
  }, []);
  // yayın sürerken (kaynaklara yazım + site derlemesi birkaç dakika) durumu izle
  useEffect(() => {
    if (!calisan) return;
    const t = window.setInterval(yukle, 4000);
    return () => window.clearInterval(t);
  }, [calisan?.id]);

  useEffect(() => {
    if (!secili) return;
    setAyr(null);
    setDosya({});
    setSekme('rapor');
    api(`/taslak/${secili}`).then((r) => (r.ok ? setAyr(r.data) : toast.error('Taslak alınamadı.')));
  }, [secili]);

  const dosyaAl = async (ad: string) => {
    if (dosya[ad] != null || !secili) return dosya[ad];
    const r = await fetch(`/api/admin/ders-revize/taslak/${secili}/dosya/${ad}`, { headers }).catch(() => null);
    if (!r || !r.ok) {
      setDosya((d) => ({ ...d, [ad]: null }));
      return null;
    }
    const txt = await r.text();
    const v = ad.endsWith('.jsonl') ? txt.split('\n').filter(Boolean).map((x) => JSON.parse(x)) : ad.endsWith('.json') ? JSON.parse(txt) : txt;
    setDosya((d) => ({ ...d, [ad]: v }));
    return v;
  };
  useEffect(() => {
    const ad = { sorular: 'ornek_sorular.json', sozluk: 'sozluk.json', hastaliklar: 'hastaliklar.json', havuz: 'bilgi_havuzu.jsonl', cikmis: 'cikmis_baglantilari.json' }[
      sekme as string
    ];
    if (ad) dosyaAl(ad);
  }, [sekme, secili]);

  const uygula = async (islem: Islem, hedef?: Taslak | null) => {
    const t = hedef || ayr;
    if (!t) return;
    const soru: Record<Islem, string> = {
      degistir: `Yayındaki "${t.konu}" dersi bu revize sürümle değiştirilsin mi? Ders notu, örnek sorular ve sözlük de güncellenir.`,
      ekle: `"${t.konu}" yeni ders olarak eklensin mi?`,
      ikisini_tut: `İki sürüm de tutulsun mu? Yayındaki ders V1, revize ders V2 olur; öğrenci dersi açarken hangisini istediğini seçer.`,
      kaldir: `Bu revize taslak kaldırılsın mı? Yayındaki ders değişmez.`,
    };
    if (!window.confirm(soru[islem])) return;
    setBusy(true);
    const r = await api(`/taslak/${t.is_id}/islem`, { method: 'POST', body: JSON.stringify({ islem }) });
    setBusy(false);
    if (!r.ok) return toast.error((r.data as any)?.hata || 'İşlem başlatılamadı.');
    toast.success(islem === 'kaldir' ? 'Taslak kaldırıldı.' : 'Sıraya alındı; kaynaklara yazılıp site derlenecek (birkaç dakika).');
    yukle();
  };

  const yenidenGonder = async (t?: Taslak) => {
    const hedefler = t ? [t] : (liste || []).filter(yenidenGonderilebilir);
    if (!hedefler.length) return toast.error('Yeniden gönderilecek taslak yok.');
    if (!t && !window.confirm(`${hedefler.length} taslak yeniden gönderilsin mi? Site en sonda bir kez derlenir.`)) return;
    setBusy(true);
    const r = t ? await api(`/taslak/${t.is_id}/yeniden`, { method: 'POST', body: '{}' }) : await api('/yeniden', { method: 'POST', body: '{}' });
    setBusy(false);
    if (!r.ok) return toast.error((r.data as any)?.hata || 'Yeniden gönderilemedi.');
    toast.success(t ? 'Yeniden sıraya alındı.' : `${(r.data?.alinan || []).length} taslak yeniden sıraya alındı.`);
    yukle();
  };

  const topluGonder = async () => {
    const bek = (liste || []).filter(bekliyor).filter((t) => !t.denetim_hata);
    if (!bek.length) return toast.error('Gönderilecek bekleyen taslak yok.');
    const iki = bek.filter((t) => t.alternatif).length;
    if (
      !window.confirm(
        `${bek.length} taslak gönderilsin mi?\n• ${iki} ders: Her ikisini tut (yayındaki V1 kalır, revize V2 olur)\n• ${bek.length - iki} ders: Ekle (yayında sürümü yok)\nSite en sonda bir kez derlenir.`,
      )
    )
      return;
    setBusy(true);
    const r = await api('/toplu', { method: 'POST', body: '{}' });
    setBusy(false);
    if (!r.ok) return toast.error((r.data as any)?.hata || 'Toplu gönderim başlatılamadı.');
    const d = r.data || {};
    toast.success(`${(d.alinan || []).length} taslak sıraya alındı${d.atlanan?.length ? `, ${d.atlanan.length} atlandı` : ''}.`);
    yukle();
  };

  const Dugmeler: React.FC<{ t: Taslak; kucuk?: boolean }> = ({ t, kucuk }) => {
    const k = kucuk ? ' is-sm' : '';
    const kapali = busy || !!t.denetim_hata;
    return (
      <div className="flex flex-wrap gap-2">
        <button type="button" disabled={kapali || !t.alternatif} className={`ms-btn is-ok${k}`} onClick={() => uygula('degistir', t)}>
          <ArrowLeftRight aria-hidden /> Yer değiştir / Güncelle
        </button>
        <button type="button" disabled={kapali || t.alternatif} className={`ms-btn is-ok${k}`} onClick={() => uygula('ekle', t)}>
          <FilePlus2 aria-hidden /> Ekle
        </button>
        <button type="button" disabled={kapali || !t.alternatif} className={`ms-btn${k}`} onClick={() => uygula('ikisini_tut', t)}>
          <Copy aria-hidden /> Her ikisini tut
        </button>
        <button type="button" disabled={busy} className={`ms-btn is-bad${k}`} onClick={() => uygula('kaldir', t)}>
          <Trash2 aria-hidden /> Kaldır
        </button>
      </div>
    );
  };

  const gorunen = (liste || []).filter((t) => (filtre === 'hepsi' ? true : filtre === 'bekleyen' ? bekliyor(t) : !bekliyor(t)));
  const s = ayr?.sayilar || {};

  return (
    <div className="flex flex-col gap-3">
      <Panel
        title="Revize Ders İşçisi"
        icon={Wrench}
        count={liste ? liste.length : undefined}
        desc="Yayındaki derslerin 2026-27 PDF'inden yeniden üretilmiş sürümleri. Karşılaştır, önizle; yer değiştir, ekle, ikisini tut ya da kaldır."
        tools={
          <div className="flex flex-wrap gap-2">
            <button type="button" className="ms-btn is-sm is-primary" disabled={busy || !(liste || []).some(bekliyor)} onClick={topluGonder}>
              <Copy aria-hidden /> Tümünü ikili gönder
            </button>
            {(liste || []).some(yenidenGonderilebilir) && (
              <button type="button" className="ms-btn is-sm is-bad" disabled={busy} onClick={() => yenidenGonder()}>
                <RotateCcw aria-hidden /> Hatalıları yeniden gönder ({(liste || []).filter(yenidenGonderilebilir).length})
              </button>
            )}
            <button type="button" className="ms-btn is-sm" onClick={yukle}>
              <RefreshCw aria-hidden /> Yenile
            </button>
          </div>
        }
      >
        {calisan && (
          <p className="text-sm text-warn mb-2">
            Yayın sürüyor: <code>{calisan.id}</code> · {calisan.asama}
          </p>
        )}
        <ChipBar<Filtre>
          label="Taslak süzgeci"
          value={filtre}
          onChange={setFiltre}
          options={[
            { id: 'bekleyen', label: 'Onay bekleyen', n: (liste || []).filter(bekliyor).length },
            { id: 'islenen', label: 'İşlem yapılan', n: (liste || []).filter((t) => !bekliyor(t)).length },
            { id: 'hepsi', label: 'Hepsi', n: (liste || []).length },
          ]}
        />
        {hata && <EmptyState icon={FileWarning} title="Revize taslakları alınamadı">{hata}</EmptyState>}
        {!hata && liste && gorunen.length === 0 && <EmptyState icon={ClipboardList} title="Bu süzgeçte taslak yok" />}
        <ul className="flex flex-col gap-2 mt-2">
          {gorunen.map((t) => {
            const d = durumEtiketi(t);
            return (
              <li key={t.is_id} className={`ms-panel p-3 ${secili === t.is_id ? 'is-on' : ''}`}>
                <button type="button" onClick={() => setSecili(t.is_id)} aria-pressed={secili === t.is_id} className="w-full text-left cursor-pointer">
                  <div className="flex flex-wrap items-center gap-2">
                    <b className="min-w-0">{t.konu || t.ders_id}</b>
                    <span className="ms-tag">{t.ders}</span>
                    <span className="ms-tag">{t.alternatif ? `alternatifi var · ${t.yayindakiler.map((y) => y.surum).join(', ')}` : 'yayında yok'}</span>
                    <span className={`ms-tag ${d.cls}`}>{d.label}</span>
                    {!!t.denetim_hata && <span className="ms-tag is-bad">denetim {t.denetim_hata} hata</span>}
                  </div>
                  <p className="text-sm text-ink-2 mt-1">
                    {t.yayindakiler[0] ? `${t.yayindakiler[0].adim} → ` : ''}
                    <b>{t.yeni?.adim ?? '?'}</b> adım · {t.yayindakiler[0] ? `${t.yayindakiler[0].etkilesim} → ` : ''}
                    <b>{t.yeni?.etkilesim ?? '?'}</b> etkileşim · {t.sayilar?.soru ?? 0} soru · {t.referans ?? 0} kitaptan
                  </p>
                </button>
                {bekliyor(t) && (
                  <div className="mt-2">
                    <Dugmeler t={t} kucuk />
                  </div>
                )}
                {yenidenGonderilebilir(t) && (
                  <div className="mt-2">
                    <button type="button" disabled={busy} className="ms-btn is-sm is-bad" onClick={() => yenidenGonder(t)}>
                      <RotateCcw aria-hidden /> Yeniden gönder
                    </button>
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      </Panel>

      {secili && (
        <Panel title={ayr?.konu || 'Taslak yükleniyor…'} icon={Library} desc={ayr ? `${ayr.ders || ''} · ${ayr.deste_id} · PDF: ${ayr.pdf || ''}` : undefined}>
          {ayr && (
            <>
              <Karsilastir t={ayr} />
              <p className="text-sm mt-2 mb-2">
                <b>{s.soru || 0}</b> soru · <b>{s.terim || 0}</b> terim · <b>{s.hastalik || 0}</b> hastalık · <b>{s.havuz || 0}</b> bilgi ·{' '}
                <b>{s.bag || 0}</b> çıkmış bağı · <b>{ayr.referans || 0}</b> kitaptan · denetim{' '}
                <b className={ayr.denetim_hata ? 'text-bad' : 'text-ok'}>{ayr.denetim_hata ?? '?'} hata</b>
              </p>
              <ChipBar<Sekme>
                label="Taslak bölümleri"
                wrap
                value={sekme}
                onChange={setSekme}
                options={[
                  { id: 'rapor', label: 'Rapor' },
                  { id: 'deste', label: 'Deste', n: ayr.yeni?.adim },
                  { id: 'sorular', label: 'Sorular', n: s.soru },
                  { id: 'sozluk', label: 'Sözlük', n: s.terim },
                  { id: 'hastaliklar', label: 'Hastalıklar', n: s.hastalik },
                  { id: 'havuz', label: 'Bilgi havuzu', n: s.havuz },
                  { id: 'cikmis', label: 'Çıkmış bağları', n: s.bag },
                ]}
              />
              <div className="mt-3">
                {sekme === 'rapor' && <NoteMarkdown text={ayr.rapor || '_Rapor yok._'} />}
                {sekme === 'deste' && (
                  <button
                    type="button"
                    className="ms-btn is-primary self-start"
                    onClick={async () => {
                      const d = await dosyaAl('deck.json');
                      if (d) setOnizle(d);
                      else toast.error('Deste dosyası alınamadı.');
                    }}
                  >
                    <Eye aria-hidden /> Revize desteyi önizle
                  </button>
                )}
                {sekme === 'sorular' && <Sorular veri={dosya['ornek_sorular.json']} />}
                {sekme === 'sozluk' && <Sozluk veri={dosya['sozluk.json']} />}
                {sekme === 'hastaliklar' && <Hastaliklar veri={dosya['hastaliklar.json']} />}
                {sekme === 'havuz' && <Havuz veri={dosya['bilgi_havuzu.jsonl']} />}
                {sekme === 'cikmis' && <Cikmis veri={dosya['cikmis_baglantilari.json']} />}
              </div>

              <div className="mt-4 border-t border-line pt-3 flex flex-col gap-2">
                {ayr.calisiyor ? (
                  <p className="text-sm text-warn">Yayınlanıyor · {ayr.calisiyor.asama}…</p>
                ) : ayr.yayin ? (
                  <>
                    <p className="text-sm">
                      {durumEtiketi(ayr).label}
                      {ayr.yayin.deste_id ? (
                        <>
                          {' '}
                          · deste <code>{ayr.yayin.deste_id}</code>
                        </>
                      ) : null}
                      {ayr.yayin.durum === 'yayinlandi' && (ayr.yayin.site_derlendi === false ? ' · site derlenemedi (npx vite build)' : ' · sitede')}
                    </p>
                    {!!ayr.yayin.hatalar?.length && (
                      <ul className="text-sm text-ink-2 list-disc pl-5">
                        {ayr.yayin.hatalar.slice(0, 8).map((h, i) => (
                          <li key={i}>{h}</li>
                        ))}
                      </ul>
                    )}
                  </>
                ) : null}
                {yenidenGonderilebilir(ayr) && (
                  <button type="button" disabled={busy} className="ms-btn is-bad self-start" onClick={() => yenidenGonder(ayr)}>
                    <RotateCcw aria-hidden /> {ayr.yayin?.durum === 'yayinlandi' ? 'Siteyi yeniden derle' : 'Yeniden gönder'}
                  </button>
                )}
                {bekliyor(ayr) ? (
                  <>
                    <p className="text-sm text-ink-2">
                      {ayr.alternatif
                        ? 'Bu dersin yayında bir sürümü var: yer değiştirebilir ya da ikisini birden tutabilirsin.'
                        : 'Bu dersin yayında sürümü yok: doğrudan eklenir.'}
                    </p>
                    <Dugmeler t={ayr} />
                  </>
                ) : null}
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
