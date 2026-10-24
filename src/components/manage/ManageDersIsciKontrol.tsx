import React, { useEffect, useState } from 'react';
import { Pause, Play, Radar, Save, SlidersHorizontal } from 'lucide-react';
import { toast } from '../ui/Toast';
import { Drawer, Field, Switch } from './consoleUi';
import { FactList, PageActions, StatRow, type Stat } from '../v14/pageKit';

/**
 * Ders işçisi denetimi: canlı durum (şu an işlenen, bugün başlanan/sınır, sonraki başlama), duraklat/sürdür, Drive'ı şimdi
 * tara ve işçinin tüm çalışma ayarları. Ayarlar işçide STATE/ayar.json'a yazılır; döngü her turda (30 sn) okur,
 * yeniden başlatma gerekmez. Veri: /api/admin/ders-isci/ayarlar · /tara (işçi iç API'si, scripts/ders_isci/api.py).
 */
export type IsciAyar = {
  duraklat: boolean;
  otomatik_tarama: boolean;
  otomatik_kuyruk: boolean;
  gunluk_sinir: number;
  ders_arasi_dk: number;
  saat_bas: number;
  saat_bit: number;
  tarama_dk: number;
  hizli_bakis_dk?: number;
  model: string;
  effort: string;
  sadakat_esigi: number;
};
type AyarYanit = { ayar: IsciAyar; modeller: string[]; eforlar: string[]; sinirlar: Record<string, [number, number]> };

export type IsciDurum = {
  calisan?: { baslik: string; basladi?: number } | null;
  bugun: number;
  sonraki?: number;
  bekleyen: number;
  sonTarama?: number;
};

const MODEL_AD: Record<string, string> = {
  'claude-opus-5-5': 'Opus 5.5',
  'claude-sonnet-5-5': 'Sonnet 5.5',
  'claude-fable-5-1': 'Fable 5.1',
  'claude-haiku-4-5-20251001': 'Haiku 4.5',
};
const EFOR_AD: Record<string, string> = { '': 'CLI varsayılanı', low: 'Düşük', medium: 'Orta', high: 'Yüksek' };

const saat = (t?: number) =>
  t ? new Date(t * 1000).toLocaleString('tr-TR', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—';
const sure = (t?: number) => {
  if (!t) return '';
  const dk = Math.max(0, Math.round((Date.now() / 1000 - t) / 60));
  return dk < 60 ? `${dk} dk` : `${Math.floor(dk / 60)} sa ${dk % 60} dk`;
};

export const IsciKontrol: React.FC<{
  api: (yol: string, init?: RequestInit) => Promise<{ ok: boolean; data?: any; error?: string }>;
  durum: IsciDurum;
  /** Ayar ya da tarama sonrası listeyi tazele */
  onDegisti: () => void;
  /** Liste yenilemesinde artar: ayar formu düzenlenmiyorsa sunucudaki son değerle eşitlenir */
  tazele: number;
  /** Bölümün kendi sayıları (StatRow başına eklenir) */
  ekStat?: Stat[];
  /** Ek sayfa eylemleri (ör. Yenile) */
  ekEylem?: React.ReactNode;
}> = ({ api, durum, onDegisti, tazele, ekStat, ekEylem }) => {
  const [veri, setVeri] = useState<AyarYanit | null>(null);
  const [taslak, setTaslak] = useState<IsciAyar | null>(null);
  const [acik, setAcik] = useState(false);
  const [busy, setBusy] = useState(false);
  const kirli = !!(veri && taslak && JSON.stringify(veri.ayar) !== JSON.stringify(taslak));

  const yukle = async () => {
    const r = await api('/ayarlar');
    if (r.ok && r.data?.ayar) {
      setVeri(r.data);
      setTaslak((t) => (t && kirli ? t : r.data.ayar));
    }
  };
  useEffect(() => {
    yukle();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tazele]);

  const kaydet = async (degisen: Partial<IsciAyar>, mesaj: string) => {
    setBusy(true);
    const r = await api('/ayarlar', { method: 'POST', body: JSON.stringify({ ayar: degisen }) });
    setBusy(false);
    if (!r.ok) return toast.error(r.data?.hata || r.error || 'Ayar kaydedilemedi.');
    setVeri((v) => (v ? { ...v, ayar: r.data.ayar } : v));
    setTaslak(r.data.ayar);
    toast.success(mesaj);
    onDegisti();
  };
  const tara = async () => {
    setBusy(true);
    const r = await api('/tara', { method: 'POST', body: '{}' });
    setBusy(false);
    if (!r.ok) return toast.error(r.data?.hata || r.error || 'Tarama istenemedi.');
    toast.success('Drive taraması istendi; işçi bir dakika içinde başlar.');
    onDegisti();
  };

  const a = veri?.ayar;
  const sinir = (k: string, vars: [number, number]) => veri?.sinirlar?.[k] || vars;
  const set = (p: Partial<IsciAyar>) => setTaslak((t) => (t ? { ...t, ...p } : t));
  const sayi = (k: keyof IsciAyar, label: string, hint: string, vars: [number, number], adim = 1) => (
    <Field label={label} hint={hint}>
      <input
        type="number"
        className="ms-input"
        min={sinir(k, vars)[0]}
        max={sinir(k, vars)[1]}
        step={adim}
        value={String(taslak?.[k] ?? '')}
        onChange={(e) => set({ [k]: adim < 1 ? parseFloat(e.target.value) : parseInt(e.target.value, 10) } as Partial<IsciAyar>)}
      />
    </Field>
  );

  const durumMetni = a?.duraklat ? 'Duraklatıldı' : durum.calisan ? `İşliyor · ${sure(durum.calisan.basladi)}` : 'Bekliyor';
  return (
    <>
      <PageActions note={durum.calisan ? `Şu an işlenen: ${durum.calisan.baslik}` : undefined}>
        {ekEylem}
        {a && (
          <button
            type="button"
            className="m14-btn"
            disabled={busy}
            onClick={() => kaydet({ duraklat: !a.duraklat }, a.duraklat ? 'İşçi sürdürülüyor.' : 'İşçi duraklatıldı; yeni ders başlamaz.')}
          >
            {a.duraklat ? <Play aria-hidden /> : <Pause aria-hidden />} {a.duraklat ? 'Sürdür' : 'Duraklat'}
          </button>
        )}
        <button type="button" className="m14-btn" onClick={() => setAcik(true)}>
          <SlidersHorizontal aria-hidden /> İşçi ayarları{kirli ? ' ·' : ''}
        </button>
        <button type="button" className="m14-btn primary" disabled={busy} onClick={tara}>
          <Radar aria-hidden /> Drive’ı şimdi tara
        </button>
      </PageActions>
      <StatRow
        stats={[
          ...(ekStat || []),
          { label: 'Bugün başlanan', value: `${durum.bugun} / ${a?.gunluk_sinir ?? '?'}` },
          { label: 'İşçi', value: durumMetni, tone: a?.duraklat ? 'warn' : durum.calisan ? 'acc' : undefined, hint: durum.calisan?.baslik },
          { label: 'Sıradaki başlama', value: durum.bekleyen ? `~${saat(durum.sonraki)}` : 'Kuyruk boş', hint: durum.bekleyen ? `${durum.bekleyen} bekleyen` : undefined },
        ]}
      />

      <Drawer
        open={acik}
        onClose={() => setAcik(false)}
        title="İşçi ayarları"
        foot={
          taslak ? (
            <>
              <button type="button" className="m14-btn" disabled={busy || !kirli} onClick={() => veri && setTaslak(veri.ayar)}>
                Vazgeç
              </button>
              <button type="button" className="m14-btn primary" disabled={busy || !kirli} onClick={() => kaydet(taslak, 'Ayarlar kaydedildi.')}>
                <Save aria-hidden /> Kaydet
              </button>
            </>
          ) : undefined
        }
      >
        <p className="m-0 text-sm text-ink-2">Değişiklikler kaydedilince en geç 30 saniyede uygulanır.{kirli ? ' Kaydedilmemiş değişiklik var.' : ''}</p>
        <FactList
          items={[
            { k: 'Durum', v: durumMetni },
            { k: 'Şu an işlenen', v: durum.calisan ? durum.calisan.baslik : '—' },
            { k: 'Bugün başlanan', v: `${durum.bugun} / ${a?.gunluk_sinir ?? '?'}` },
            { k: 'Sıradaki başlama', v: durum.bekleyen ? `~${saat(durum.sonraki)} (${durum.bekleyen} bekleyen)` : 'kuyruk boş' },
            { k: 'Son Drive taraması', v: `${saat(durum.sonTarama)}${a ? ` · ${a.otomatik_tarama ? `${a.tarama_dk} dk'da bir` : 'otomatik kapalı'}` : ''}` },
            {
              k: 'Kural',
              v: a
                ? `günde ≤${a.gunluk_sinir} · ${a.ders_arasi_dk} dk arayla · ${String(a.saat_bas).padStart(2, '0')}–${String(a.saat_bit).padStart(2, '0')} · ${MODEL_AD[a.model] || a.model}`
                : '…',
            },
          ]}
        />
        {taslak && (
          <div className="flex flex-col gap-3 mt-3">
            <div className="grid gap-3" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(min(200px, 100%), 1fr))' }}>
              {sayi('gunluk_sinir', 'Günlük ders sınırı', 'Bir günde işlenmeye başlanan en çok ders (PDF).', [0, 48])}
              {sayi('ders_arasi_dk', 'İki ders arası (dk)', 'İki dersin başlangıcı arasında en az bu kadar dakika; 60 = saatte 1.', [0, 1440])}
              {sayi('saat_bas', 'İşleme başlangıç saati', 'TR saati, 0–23.', [0, 23])}
              {sayi('saat_bit', 'İşleme bitiş saati', '1–24 (24 = gece yarısı). Başlangıçtan küçükse gece boyunca.', [1, 24])}
              {sayi('tarama_dk', 'Drive tarama aralığı (dk)', 'Drive yeni PDF için bu sıklıkla taranır.', [10, 1440])}
              {sayi('hizli_bakis_dk', 'Hızlı bakış (dk, 0 kapalı)', 'Kök ve aktif kurul klasörüne bu sıklıkla hafifçe bakılır; değişiklik görülürse tam tarama hemen başlar.', [0, 60])}
              {sayi('sadakat_esigi', 'Yayın sadakat eşiği', 'Ders notunun PDF metnine sadakati bunun altındaysa yayın durur (0–1).', [0, 1], 0.01)}
              <Field label="Model" hint="Ders üreten Claude modeli; bir sonraki dersten geçerli.">
                <select className="ms-input" value={taslak.model} onChange={(e) => set({ model: e.target.value })}>
                  {(veri?.modeller || []).map((m) => (
                    <option key={m} value={m}>
                      {MODEL_AD[m] || m}
                    </option>
                  ))}
                </select>
              </Field>
              <Field label="Efor" hint="Düşük efor daha hızlı ve az kota harcar.">
                <select className="ms-input" value={taslak.effort} onChange={(e) => set({ effort: e.target.value })}>
                  {(veri?.eforlar || []).map((m) => (
                    <option key={m} value={m}>
                      {EFOR_AD[m] ?? m}
                    </option>
                  ))}
                </select>
              </Field>
            </div>
            <Switch
              checked={taslak.otomatik_tarama}
              onChange={(v) => set({ otomatik_tarama: v })}
              label="Drive'ı otomatik tara"
              hint="Kapalıyken yalnız 'Drive'ı şimdi tara' ile taranır."
            />
            <Switch
              checked={taslak.otomatik_kuyruk}
              onChange={(v) => set({ otomatik_kuyruk: v })}
              label="Yeni PDF'leri otomatik kuyruğa al"
              hint="Kapalıyken yeni PDF'ler 'PDF görüldü' listesinde bekler; 'Kuyruğa al' ile sen seçersin."
            />
          </div>
        )}
      </Drawer>
    </>
  );
};
