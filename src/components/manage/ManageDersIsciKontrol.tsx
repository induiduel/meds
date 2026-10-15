import React, { useEffect, useState } from 'react';
import { Pause, Play, Radar, Save, SlidersHorizontal } from 'lucide-react';
import { toast } from '../ui/Toast';
import { Field, Panel, Switch } from './consoleUi';

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
  api: (yol: string, init?: RequestInit) => Promise<{ ok: boolean; data?: any }>;
  durum: IsciDurum;
  /** Ayar ya da tarama sonrası listeyi tazele */
  onDegisti: () => void;
  /** Liste yenilemesinde artar: ayar formu düzenlenmiyorsa sunucudaki son değerle eşitlenir */
  tazele: number;
}> = ({ api, durum, onDegisti, tazele }) => {
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
    if (!r.ok) return toast.error(r.data?.hata || 'Ayar kaydedilemedi.');
    setVeri((v) => (v ? { ...v, ayar: r.data.ayar } : v));
    setTaslak(r.data.ayar);
    toast.success(mesaj);
    onDegisti();
  };
  const tara = async () => {
    setBusy(true);
    const r = await api('/tara', { method: 'POST', body: '{}' });
    setBusy(false);
    if (!r.ok) return toast.error(r.data?.hata || 'Tarama istenemedi.');
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

  return (
    <Panel
      title="İşçi denetimi"
      icon={SlidersHorizontal}
      desc="Ders işçisinin canlı durumu ve çalışma kuralları. Değişiklikler kaydedilince en geç 30 saniyede uygulanır."
      tools={
        <>
          <button type="button" className="ms-btn is-sm" disabled={busy} onClick={tara}>
            <Radar aria-hidden /> Drive'ı şimdi tara
          </button>
          {a && (
            <button
              type="button"
              className={`ms-btn is-sm ${a.duraklat ? 'is-ok' : 'is-warn'}`}
              disabled={busy}
              onClick={() => kaydet({ duraklat: !a.duraklat }, a.duraklat ? 'İşçi sürdürülüyor.' : 'İşçi duraklatıldı; yeni ders başlamaz.')}
            >
              {a.duraklat ? <Play aria-hidden /> : <Pause aria-hidden />} {a.duraklat ? 'Sürdür' : 'Duraklat'}
            </button>
          )}
        </>
      }
    >
      <dl className="grid gap-x-6 gap-y-2 text-sm" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))' }}>
        <div>
          <dt className="text-ink-3">Durum</dt>
          <dd className="m-0">
            {a?.duraklat ? (
              <b className="text-warn">Duraklatıldı</b>
            ) : durum.calisan ? (
              <b>İşliyor · {sure(durum.calisan.basladi)}</b>
            ) : (
              <b>Bekliyor</b>
            )}
          </dd>
        </div>
        <div>
          <dt className="text-ink-3">Şu an işlenen</dt>
          <dd className="m-0">{durum.calisan ? durum.calisan.baslik : '—'}</dd>
        </div>
        <div>
          <dt className="text-ink-3">Bugün başlanan</dt>
          <dd className="m-0">
            <b>{durum.bugun}</b> / {a?.gunluk_sinir ?? '?'}
          </dd>
        </div>
        <div>
          <dt className="text-ink-3">Sıradaki başlama</dt>
          <dd className="m-0">{durum.bekleyen ? `~${saat(durum.sonraki)} (${durum.bekleyen} bekleyen)` : 'kuyruk boş'}</dd>
        </div>
        <div>
          <dt className="text-ink-3">Son Drive taraması</dt>
          <dd className="m-0">
            {saat(durum.sonTarama)}
            {a ? ` · ${a.otomatik_tarama ? `${a.tarama_dk} dk'da bir` : 'otomatik kapalı'}` : ''}
          </dd>
        </div>
        <div>
          <dt className="text-ink-3">Kural</dt>
          <dd className="m-0">
            {a
              ? `günde ≤${a.gunluk_sinir} · ${a.ders_arasi_dk} dk arayla · ${String(a.saat_bas).padStart(2, '0')}–${String(a.saat_bit).padStart(2, '0')} · ${MODEL_AD[a.model] || a.model}`
              : '…'}
          </dd>
        </div>
      </dl>

      <details className="mt-3" open={acik} onToggle={(e) => setAcik((e.target as HTMLDetailsElement).open)}>
        <summary className="text-sm font-semibold" style={{ cursor: 'pointer' }}>
          Ayarlar{kirli ? ' · kaydedilmemiş değişiklik' : ''}
        </summary>
        {taslak && (
          <div className="flex flex-col gap-3 mt-3">
            <div className="grid gap-3" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
              {sayi('gunluk_sinir', 'Günlük ders sınırı', 'Bir günde işlenmeye başlanan en çok ders (PDF).', [0, 48])}
              {sayi('ders_arasi_dk', 'İki ders arası (dk)', 'İki dersin başlangıcı arasında en az bu kadar dakika; 60 = saatte 1.', [0, 1440])}
              {sayi('saat_bas', 'İşleme başlangıç saati', 'TR saati, 0–23.', [0, 23])}
              {sayi('saat_bit', 'İşleme bitiş saati', '1–24 (24 = gece yarısı). Başlangıçtan küçükse gece boyunca.', [1, 24])}
              {sayi('tarama_dk', 'Drive tarama aralığı (dk)', 'Drive yeni PDF için bu sıklıkla taranır.', [10, 1440])}
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
            <div className="flex flex-wrap gap-2">
              <button type="button" className="ms-btn is-primary" disabled={busy || !kirli} onClick={() => kaydet(taslak, 'Ayarlar kaydedildi.')}>
                <Save aria-hidden /> Kaydet
              </button>
              <button type="button" className="ms-btn" disabled={busy || !kirli} onClick={() => veri && setTaslak(veri.ayar)}>
                Vazgeç
              </button>
            </div>
          </div>
        )}
      </details>
    </Panel>
  );
};
