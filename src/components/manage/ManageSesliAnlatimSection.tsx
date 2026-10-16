import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { AudioLines, Download, Play, Plus, RotateCcw, X, ArrowUp, Star, Trash2, FileText, Wallet, Pause, ListOrdered, Cpu } from 'lucide-react';
import { safeJsonFetch, getCustomApiUrl } from '../../services/api';
import { toast } from '../ui/Toast';
import { confirmDialog } from '../ui/ConfirmDialog';
import { ChipBar, ConfirmButton, EmptyState, Panel, SearchBox, timeLabel } from './consoleUi';
import { useLiveEvent } from '../../hooks/useLiveEvent';
import { auth } from '../../services/auth';
import './sesli-anlatim.css';

/**
 * Sesli anlatım: her Kurul 1 dersi için konuşma metni ve MP3'ler (src/services/sesliAnlatim.ts).
 * Varsayılan ses Microsoft Edge Emel (ücretsiz). "Alternatif oluştur" ile Gemini sesi (ücretsiz anahtar havuzu ya da
 * ücretli anahtar — bütçe kilidi 850 TL, tavan 900 TL) üretilir; ücretli üretim yalnız buradan elle başlar.
 */
type Saglayici = 'edge-emel' | 'gemini-ucretsiz' | 'gemini-ucretli' | 'xtts-yerel' | 'ema-yerel';
type Varyant = {
  id: string; saglayici: Saglayici; ses: string; etiket: string; ucretli: boolean; sureSn: number; bayt: number; parca: number;
  olusturuldu: string; maliyetTL?: number; metinGuncel?: boolean; dogrulama?: { parca: number; toplam: number; ortalama: number | null };
};
type Is = {
  id: string; key: string; saglayici: Saglayici; ses: string; durum: string; ilerleme: { bitti: number; toplam: number };
  olusturuldu: string; basladi?: string; bitti?: string; sonrakiDeneme?: string; hata?: string; notlar?: string[]; maliyetTL?: number;
};
type Ders = { key: string; no: number; baslik: string; sira: number; metin: boolean; kelime: number; bolum: number; tahminiDk: number; varyantlar: Varyant[]; isler: Is[] };
type SaglayiciBilgi = { id: Saglayici; etiket: string; ucretli: boolean; sesler: string[]; varsayilanSes: string };
type Durum = {
  dersler: Ders[]; kuyruk: Is[]; saglayicilar: SaglayiciBilgi[];
  butce: { tavanTL: number; kilitTL: number; harcananTL: number; kalanTL: number; varsayim: string; anahtarVar: boolean };
  isci: { aktif: boolean; calisiyor: boolean };
  /** Coqui XTTS v2: yöneticinin bilgisayarındaki işçi (scripts/sesli_anlatim/xtts_isci.py); eski sunucuda yok */
  yerel?: YerelOzet & { aktif: boolean; isciler?: Partial<Record<Saglayici, YerelOzet>> };
  ucretliAktif: boolean;
  /** Yerel ses planı: ders → yerel sağlayıcı + konuşmacı (sunucuda yerel_plan.json) */
  yerelPlan?: Record<string, { saglayici: Saglayici; ses: string; at?: string }>;
  /** Örneği olan konuşmacılar "<saglayici>/<ses>" (panelde Dinle) */
  ornekler?: string[];
};

/** Konuşmacı örneği: tek paylaşılan oynatıcı; başka örnek başlayınca öncekini durdurur. */
let ornekSes: HTMLAudioElement | null = null;
const OrnekDinle: React.FC<{ d: Durum; saglayici?: Saglayici | ''; ses?: string; url: (sag: string, ses: string) => string }> = ({ d, saglayici, ses, url }) => {
  const [caliyor, setCaliyor] = useState(false);
  const benim = React.useRef<HTMLAudioElement | null>(null);
  useEffect(() => () => benim.current?.pause(), []); // satır kapanınca yalnız kendi örneğini durdurur
  if (!saglayici || !ses || !d.ornekler?.includes(`${saglayici}/${ses}`)) return null;
  const tikla = () => {
    if (caliyor) {
      benim.current?.pause();
      return setCaliyor(false);
    }
    ornekSes?.pause(); // başka düğmenin örneği: kendi pause dinleyicisi onu kapatır
    const a = new Audio(url(saglayici, ses));
    ornekSes = a;
    benim.current = a;
    a.addEventListener('ended', () => setCaliyor(false), { once: true });
    a.addEventListener('pause', () => setCaliyor(false), { once: true });
    setCaliyor(true);
    a.play().catch(() => {
      setCaliyor(false);
      toast.error('Örnek çalınamadı.');
    });
  };
  return (
    <button type="button" className="ms-btn is-sm" onClick={tikla} title={`${ses} örneğini dinle`} aria-label={`${ses} örneğini ${caliyor ? 'durdur' : 'dinle'}`}>
      {caliyor ? <Pause /> : <Play />}
    </button>
  );
};
type YerelOzet = { cevrimici: boolean; ad: string | null; sonSinyal: string | null; not: string | null };
/** Yazma uçları doğrulanmış yönetici ister: Firebase oturum jetonu eklenir (yerelde loopback yeter). */
async function yetkili(h: Record<string, string>): Promise<Record<string, string>> {
  const u = auth.currentUser;
  if (!u) return h;
  try {
    return { ...h, Authorization: `Bearer ${await u.getIdToken()}` };
  } catch {
    return h;
  }
}
type Filtre = 'hepsi' | 'hazir' | 'kuyrukta' | 'metin' | 'bekliyor';

const DURUM_ETIKET: Record<string, string> = {
  bekliyor: 'Sırada', calisiyor: 'Seslendiriliyor', 'kota-bekliyor': 'Kota bekliyor', bitti: 'Bitti', hata: 'Hata', iptal: 'İptal', 'butce-durdu': 'Bütçe kilidi',
};
const sure = (sn: number) => (sn >= 3600 ? `${Math.floor(sn / 3600)} sa ${Math.round((sn % 3600) / 60)} dk` : `${Math.floor(sn / 60)} dk ${String(Math.round(sn % 60)).padStart(2, '0')} sn`);
const mb = (b: number) => `${(b / 1048576).toFixed(1)} MB`;
const kisaEtiket = (v: Varyant) => (v.saglayici === 'edge-emel' ? 'Emel' : v.saglayici === 'xtts-yerel' ? `${v.ses} · XTTS` : `${v.ses}${v.ucretli ? ' · ücretli' : ''}`);

export const ManageSesliAnlatimSection: React.FC<{ adminEmail: string }> = ({ adminEmail }) => {
  const headers = useMemo(() => ({ 'Content-Type': 'application/json', 'x-admin-email': adminEmail || '' }), [adminEmail]);
  const [d, setD] = useState<Durum | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const [filtre, setFiltre] = useState<Filtre>('hepsi');
  const [ara, setAra] = useState('');
  const [acik, setAcik] = useState<string | null>(null);
  const [calan, setCalan] = useState<{ key: string; vid: string } | null>(null);
  const [kuyrukAcik, setKuyrukAcik] = useState(false);

  const yukle = useCallback(async () => {
    const r = await safeJsonFetch<Durum>('/api/sesli-anlatim', { headers });
    if (r.ok && r.data) {
      setD(r.data);
      setHata(null);
    } else setHata(r.error || 'Sesli anlatım durumu alınamadı.');
  }, [headers]);
  useEffect(() => {
    void yukle();
  }, [yukle]);
  useLiveEvent('sesli_anlatim', () => void yukle(), { debounceMs: 600 });
  // Canlı olay kaçarsa diye çalışan iş varken 15 sn'de bir tazele
  const aktifIs = !!d?.kuyruk.some((x) => ['bekliyor', 'calisiyor', 'kota-bekliyor'].includes(x.durum));
  useEffect(() => {
    if (!aktifIs) return;
    const t = window.setInterval(() => void yukle(), 15000);
    return () => window.clearInterval(t);
  }, [aktifIs, yukle]);

  const sesUrl = useCallback((key: string, vid: string, indir = false) => {
    const yol = `/api/sesli-anlatim/ses/${key}/${vid}.mp3`;
    const qs = new URLSearchParams({ adminEmail: adminEmail || '' });
    if (indir) qs.set('indir', '1');
    return `${getCustomApiUrl(yol).replace(/\/$/, '')}${yol}?${qs}`;
  }, [adminEmail]);
  const ornekUrl = useCallback((sag: string, ses: string) => {
    const yol = `/api/sesli-anlatim/ornek/${sag}/${encodeURIComponent(ses)}`;
    return `${getCustomApiUrl(yol).replace(/\/$/, '')}${yol}?${new URLSearchParams({ adminEmail: adminEmail || '' })}`;
  }, [adminEmail]);
  const post = async (yol: string, body?: any) => {
    const r = await safeJsonFetch<any>(yol, { method: 'POST', headers: await yetkili(headers), body: JSON.stringify(body || {}) });
    if (!r.ok) toast.error((r.data as any)?.error || r.error || 'İşlem yapılamadı.');
    await yukle();
    return r.ok;
  };

  const say = useMemo(() => {
    const ds = d?.dersler || [];
    return {
      hepsi: ds.length,
      hazir: ds.filter((x) => x.varyantlar.length).length,
      emel: ds.filter((x) => x.varyantlar.some((v) => v.saglayici === 'edge-emel')).length,
      aoede: ds.filter((x) => x.varyantlar.some((v) => v.saglayici === 'gemini-ucretsiz')).length,
      ucretli: ds.filter((x) => x.varyantlar.some((v) => v.saglayici === 'gemini-ucretli')).length,
      kuyrukta: ds.filter((x) => x.isler.length).length,
      metin: ds.filter((x) => x.metin).length,
      bekliyor: ds.filter((x) => !x.metin).length,
    };
  }, [d]);
  const liste = useMemo(() => {
    const q = ara.trim().toLocaleLowerCase('tr-TR');
    return (d?.dersler || [])
      .filter((x) =>
        filtre === 'hazir' ? x.varyantlar.length : filtre === 'kuyrukta' ? x.isler.length : filtre === 'metin' ? x.metin : filtre === 'bekliyor' ? !x.metin : true,
      )
      .filter((x) => !q || x.baslik.toLocaleLowerCase('tr-TR').includes(q) || String(x.no) === q)
      .sort((a, b) => a.sira - b.sira);
  }, [d, filtre, ara]);
  const toplamSure = useMemo(() => (d?.dersler || []).reduce((t, x) => t + (x.varyantlar[0]?.sureSn || 0), 0), [d]);

  if (hata && !d)
    return (
      <div className="ms-alert">
        {hata} Sunucu bu bölümü henüz tanımıyorsa (yeni özellik canlıya dağıtılmadıysa) panel bağlantısını "Yerel"e alın.
      </div>
    );
  if (!d) return <div className="h-48 rounded-2xl ms-shimmer" role="status" aria-label="Yükleniyor" />;

  const bekleyenIsler = d.kuyruk.filter((x) => ['bekliyor', 'calisiyor', 'kota-bekliyor', 'hata', 'butce-durdu'].includes(x.durum));

  return (
    <div className="sa-wrap flex flex-col gap-3 min-w-0">
      <div className="sa-stats">
        <div>
          <b>{say.metin} / {say.hepsi}</b><span>konuşma metni hazır</span>
          <div className="sa-mini"><i style={{ width: `${(100 * say.metin) / Math.max(1, say.hepsi)}%` }} /></div>
        </div>
        <div>
          <b>{say.emel} / {say.hepsi}</b><span>Emel sesi hazır (varsayılan)</span>
          <div className="sa-mini"><i style={{ width: `${(100 * say.emel) / Math.max(1, say.hepsi)}%` }} /></div>
        </div>
        <div>
          <b>{say.aoede} / {say.hepsi}</b><span>Aoede alternatifi hazır (ücretsiz)</span>
          <div className="sa-mini"><i style={{ width: `${(100 * say.aoede) / Math.max(1, say.hepsi)}%` }} /></div>
        </div>
        <div><b>{say.kuyrukta}</b><span>ders kuyrukta · toplam ses {sure(toplamSure)}</span></div>
        <div className={`sa-paid ${d.butce.harcananTL > d.butce.kilitTL * 0.8 ? 'is-warn' : ''}`} title={d.butce.varsayim}>
          <b>{d.butce.harcananTL.toLocaleString('tr-TR')} TL</b>
          <span><Wallet className="w-3 h-3 inline" /> ücretli harcama · kilit {d.butce.kilitTL} / tavan {d.butce.tavanTL} TL · {say.ucretli} ders</span>
          <label className="sa-switch">
            <input
              type="checkbox"
              checked={d.ucretliAktif}
              disabled={!d.butce.anahtarVar}
              onChange={async (e) => {
                const ac = e.target.checked;
                if (ac && !(await confirmDialog({ title: 'Ücretli üretim açılsın mı?', message: `Açıkken: (1) ücretsiz anahtarların hepsi dolunca sıradaki Aoede sesi aynı dersten ücretli anahtarla tamamlanır, (2) "Alternatif oluştur" ile ücretli Gemini sesi üretilebilir. Kalan bütçe ${d.butce.kalanTL} TL; ${d.butce.kilitTL} TL'de kendiliğinden kilitlenir.`, confirmLabel: 'Aç', tone: 'danger' }))) return;
                await post('/api/sesli-anlatim/ucretli', { aktif: ac });
              }}
            />
            <span>{d.ucretliAktif ? 'Ücretli üretim AÇIK' : 'Ücretli üretim kapalı'}</span>
          </label>
        </div>
      </div>

      {d.yerel && (() => {
        const y = d.yerel;
        // Yerel işçiler: XTTS (GPU ≤ %70 + CPU) ve EMA (yalnız CPU); eski sunucuda yalnız ortak sinyal vardır
        const isciler: { id: Saglayici; ad: string; servis: string; o: YerelOzet }[] = [
          { id: 'xtts-yerel', ad: 'Coqui XTTS v2', servis: 'meds-xtts', o: y.isciler?.['xtts-yerel'] ?? y },
          ...(y.isciler?.['ema-yerel'] ? [{ id: 'ema-yerel' as Saglayici, ad: 'EMA Lightning', servis: 'meds-ema', o: y.isciler['ema-yerel']! }] : []),
        ];
        const herhangi = isciler.some((x) => x.o.cevrimici);
        return (
          <div className={`sa-yerel ${herhangi ? 'is-on' : ''}`}>
            <div className="sa-yerel-bas">
              <Cpu className="w-4 h-4" aria-hidden />
              <b>Bu PC · yerel ses işçileri</b>
              <button type="button" className="ms-btn is-sm sa-yerel-btn" onClick={() => void post('/api/sesli-anlatim/yerel/aktif', { aktif: !y.aktif })}>
                {y.aktif ? <><Pause /> Durdur</> : <><Play /> Aç</>}
              </button>
            </div>
            <ul className="sa-yerel-liste">
              {isciler.map((x) => (
                <li key={x.id}>
                  <span className={`ms-tag ${x.o.cevrimici ? 'is-ok' : ''}`}>{x.o.cevrimici ? 'Çevrimiçi' : 'Çevrimdışı'}</span>
                  <b>{x.ad}</b>
                  <small>
                    {x.o.cevrimici
                      ? `${x.o.not || 'iş bekliyor'} · son sinyal ${timeLabel(x.o.sonSinyal!, true)}`
                      : x.o.sonSinyal
                        ? `son sinyal ${timeLabel(x.o.sonSinyal, true)} — bilgisayar açılınca sıradaki işi kendisi alır`
                        : `bağlanmadı — bilgisayarda: systemctl --user start ${x.servis}`}
                  </small>
                </li>
              ))}
            </ul>
            <small className="sa-yerel-not">
              {y.aktif ? '' : 'Yerel işçiler panelden durduruldu; yeni iş almıyorlar. '}
              "Yerel ses planı" ya da ders satırındaki "Alternatif oluştur" ile onayladığın dersler bu bilgisayarda seslendirilir: XTTS GPU'yu en fazla %70 kullanır (80 °C üstünde yavaşlar), EMA yalnız CPU.
            </small>
          </div>
        );
      })()}

      {d.yerelPlan && <YerelPlan d={d} post={post} ornekUrl={ornekUrl} />}

      <Panel
        title="Seslendirme kuyruğu"
        icon={ListOrdered}
        count={bekleyenIsler.length}
        tools={
          <>
            <span className={`ms-tag ${d.isci.aktif ? 'is-ok' : ''}`} title="Bu sunucudaki Emel / Gemini seslendirme işçisi (yerel XTTS/EMA işçilerinden ayrı)">
              {d.isci.aktif ? 'Sunucu işçisi çalışıyor' : 'Sunucu işçisi durdu'}
            </span>
            <button
              type="button"
              className="ms-btn is-sm"
              title="Emel / Gemini işçisi — yerel XTTS/EMA işçilerini etkilemez"
              onClick={async () => {
                if (!d.isci.aktif && !(await confirmDialog({ title: 'Sunucu işçisi başlatılsın mı?', message: `Bu, bağlı olduğun sunucudaki Emel / Gemini seslendirme işçisidir (yerel XTTS/EMA işçileri bundan bağımsız çalışır).${d.ucretliAktif ? ' Ücretli üretim AÇIK: sıradaki ücretli işler başlar.' : ''} Kuyruk Oracle'da çalışıyorsa yerel sunucuda açma — iki makine aynı işi yapar.`, confirmLabel: 'Başlat', tone: d.ucretliAktif ? 'danger' : undefined }))) return;
                await post('/api/sesli-anlatim/isci', { aktif: !d.isci.aktif });
              }}
            >
              {d.isci.aktif ? <><Pause /> Durdur</> : <><Play /> Başlat</>}
            </button>
            <button type="button" className="ms-btn is-sm" onClick={() => setKuyrukAcik((v) => !v)}>{kuyrukAcik ? 'Gizle' : 'Göster'}</button>
          </>
        }
        desc="Emel, ücretsiz Gemini ve ücretli Gemini üç ayrı şeritte paralel; ücretli işler hiç beklemez, her şerit kendi içinde dersleri sırayla, tek tek seslendirir. Gemini sesi bitmeden sonraki derse geçilmez: önce tüm ücretsiz anahtarlar denenir, hepsi doluysa ücretli üretim açıksa ücretli anahtarla sürer, kapalıysa kota açılınca kaldığı parçadan devam eder."
        flush={!kuyrukAcik}
      >
        {kuyrukAcik &&
          (bekleyenIsler.length ? (
            <ol className="sa-queue">
              {bekleyenIsler.map((x, i) => {
                const ders = d.dersler.find((y) => y.key === x.key);
                return (
                  <li key={x.id} className={`sa-qrow is-${x.durum}`}>
                    <span className="sa-qn">{i + 1}</span>
                    <div className="min-w-0 flex-1">
                      <div className="sa-qtitle">{ders ? `${ders.no}. ${ders.baslik}` : x.key}</div>
                      <div className="sa-qmeta">
                        <span className="ms-tag">{DURUM_ETIKET[x.durum] || x.durum}</span>{' '}
                        {d.saglayicilar.find((s) => s.id === x.saglayici)?.etiket} · {x.ses}
                        {x.sonrakiDeneme && x.durum === 'kota-bekliyor' ? ` · yeniden deneme ${timeLabel(x.sonrakiDeneme, true)}` : ''}
                        {x.maliyetTL ? ` · ${x.maliyetTL.toFixed(2)} TL` : ''}
                      </div>
                      {x.ilerleme.toplam > 0 && (
                        <div className="sa-bar" aria-label={`İlerleme ${x.ilerleme.bitti}/${x.ilerleme.toplam}`}>
                          <i style={{ width: `${(100 * x.ilerleme.bitti) / x.ilerleme.toplam}%` }} />
                          <span>{x.ilerleme.bitti}/{x.ilerleme.toplam} parça</span>
                        </div>
                      )}
                      {x.hata && <div className="sa-err">{x.hata}</div>}
                    </div>
                    <div className="sa-qact">
                      {['hata', 'butce-durdu', 'kota-bekliyor'].includes(x.durum) && (
                        <button type="button" className="ms-btn is-sm" title="Yeniden dene" onClick={() => void post(`/api/sesli-anlatim/kuyruk/${x.id}/yeniden`)}><RotateCcw /></button>
                      )}
                      {['bekliyor', 'kota-bekliyor'].includes(x.durum) && i > 0 && (
                        <button type="button" className="ms-btn is-sm" title="Öne al" onClick={() => void post(`/api/sesli-anlatim/kuyruk/${x.id}/one-al`)}><ArrowUp /></button>
                      )}
                      <button type="button" className="ms-btn is-sm" title="İptal" onClick={() => void post(`/api/sesli-anlatim/kuyruk/${x.id}/iptal`)}><X /></button>
                    </div>
                  </li>
                );
              })}
            </ol>
          ) : (
            <EmptyState icon={ListOrdered} title="Kuyruk boş" />
          ))}
      </Panel>

      <div className="flex flex-wrap items-center gap-2">
        <ChipBar
          label="Süz"
          value={filtre}
          onChange={setFiltre}
          wrap
          options={[
            { id: 'hepsi', label: 'Tümü', n: say.hepsi },
            { id: 'hazir', label: 'Ses hazır', n: say.hazir },
            { id: 'kuyrukta', label: 'Kuyrukta', n: say.kuyrukta },
            { id: 'metin', label: 'Metni hazır', n: say.metin },
            { id: 'bekliyor', label: 'Metin bekliyor', n: say.bekliyor },
          ]}
        />
        <div className="flex-1 min-w-[200px]"><SearchBox value={ara} onChange={setAra} placeholder="Ders adı ya da no" /></div>
      </div>

      <Panel title="Dersler" icon={AudioLines} count={liste.length} flush>
        {liste.length === 0 ? (
          <EmptyState icon={AudioLines} title="Bu süzgeçte ders yok" />
        ) : (
          <ul className="sa-list">
            {liste.map((x) => (
              <DersSatiri
                key={x.key}
                ders={x}
                saglayicilar={d.saglayicilar}
                butce={d.butce}
                ucretliAktif={d.ucretliAktif}
                acik={acik === x.key}
                onAc={() => setAcik((k) => (k === x.key ? null : x.key))}
                calan={calan}
                setCalan={setCalan}
                sesUrl={sesUrl}
                post={post}
                headers={headers}
                yukle={yukle}
                d={d}
                ornekUrl={ornekUrl}
              />
            ))}
          </ul>
        )}
      </Panel>
    </div>
  );
};

/** Kalıcı oynatıcı: üst bileşen canlı tazelemede yeniden çizilse de <audio> öğesi korunur (ses kesilmez). */
const Oynatici: React.FC<{
  dersKey: string;
  v: Varyant;
  calan: { key: string; vid: string } | null;
  setCalan: (v: { key: string; vid: string } | null) => void;
  sesUrl: (key: string, vid: string, indir?: boolean) => string;
}> = React.memo(({ dersKey, v, calan, setCalan, sesUrl }) =>
  calan?.key === dersKey && calan.vid === v.id ? (
    <audio className="sa-audio" controls autoPlay preload="metadata" src={sesUrl(dersKey, v.id)} onEnded={() => setCalan(null)} />
  ) : (
    <button type="button" className="ms-btn is-sm is-primary" onClick={() => setCalan({ key: dersKey, vid: v.id })}>
      <Play /> Oynat
    </button>
  ),
);

const DersSatiri: React.FC<{
  ders: Ders;
  saglayicilar: SaglayiciBilgi[];
  butce: Durum['butce'];
  ucretliAktif: boolean;
  acik: boolean;
  onAc: () => void;
  calan: { key: string; vid: string } | null;
  setCalan: (v: { key: string; vid: string } | null) => void;
  sesUrl: (key: string, vid: string, indir?: boolean) => string;
  post: (yol: string, body?: any) => Promise<boolean>;
  headers: Record<string, string>;
  yukle: () => Promise<void>;
  d: Durum;
  ornekUrl: (sag: string, ses: string) => string;
}> = ({ ders, saglayicilar, butce, ucretliAktif, acik, onAc, calan, setCalan, sesUrl, post, headers, yukle, d, ornekUrl }) => {
  const [sag, setSag] = useState<Saglayici>('gemini-ucretsiz');
  const [ses, setSes] = useState('Aoede');
  const [metin, setMetin] = useState<string | null>(null);
  const [metinAcik, setMetinAcik] = useState(false);
  const ana = ders.varyantlar[0];
  const sb = saglayicilar.find((s) => s.id === sag);
  useEffect(() => {
    if (sb && !sb.sesler.includes(ses)) setSes(sb.varsayilanSes);
  }, [sag]); // eslint-disable-line react-hooks/exhaustive-deps

  const tahminiTL = Math.round(((ders.kelime / 112) * 60 * 25 * 1.3 * 18) / 1e6 * 50 * 100) / 100;
  const alternatif = async () => {
    if (sb?.ucretli) {
      const ok = await confirmDialog({
        title: 'Ücretli seslendirme',
        message: `"${ders.baslik}" Gemini ücretli anahtarla (${ses}) seslendirilecek. Temkinli tahmin ~${tahminiTL.toLocaleString('tr-TR')} TL. Harcanan ${butce.harcananTL} TL, kilide kalan ${butce.kalanTL} TL (tavan ${butce.tavanTL} TL aşılamaz).`,
        confirmLabel: 'Ücretli üret',
        tone: 'danger',
      });
      if (!ok) return;
    }
    if (sag === 'xtts-yerel') {
      const ok = await confirmDialog({
        title: 'Bu bilgisayarda seslendirilsin mi?',
        message: `"${ders.baslik}" Coqui XTTS v2 (${ses}) ile senin bilgisayarında seslendirilecek: GPU en fazla %70 (80 °C üstünde yavaşlar), gerisi CPU ve RAM. Tahmini süre ~${Math.max(5, Math.round(ders.tahminiDk * 0.4))} dk; bilgisayar kapalıysa açılınca başlar, yarıda kalırsa kaldığı parçadan sürer. Ücretsiz.`,
        confirmLabel: 'Onayla ve kuyruğa al',
      });
      if (!ok) return;
    }
    if (await post('/api/sesli-anlatim/uret', { key: ders.key, saglayici: sag, ses })) toast.success(sag === 'xtts-yerel' ? 'Ders bu PC\'nin kuyruğuna alındı.' : 'Alternatif ses kuyruğa alındı.');
  };
  const metniAc = async () => {
    setMetinAcik((v) => !v);
    if (metin === null) {
      const r = await safeJsonFetch<{ metin: string }>(`/api/sesli-anlatim/metin/${ders.key}`, { headers });
      setMetin(r.ok && r.data ? r.data.metin : 'Metin alınamadı.');
    }
  };

  return (
    <li className={`sa-row ${acik ? 'is-open' : ''}`}>
      <div className="sa-head">
        <button type="button" className="sa-title" onClick={onAc} aria-expanded={acik}>
          <span className="sa-no">{ders.no}</span>
          <span className="min-w-0">
            <b>{ders.baslik}</b>
            <small>
              {ders.metin ? `${ders.kelime.toLocaleString('tr-TR')} kelime · ~${ders.tahminiDk} dk · ${ders.bolum} bölüm` : 'Konuşma metni hazırlanıyor'}
            </small>
          </span>
        </button>
        <div className="sa-badges">
          {ana ? (
            <span className="ms-tag is-ok" title={ana.etiket}><AudioLines className="w-3 h-3" /> {ana.etiket} · {sure(ana.sureSn)}</span>
          ) : ders.isler.length ? (
            <span className="ms-tag is-accent">{DURUM_ETIKET[ders.isler[0].durum]}{ders.isler[0].ilerleme.toplam ? ` ${ders.isler[0].ilerleme.bitti}/${ders.isler[0].ilerleme.toplam}` : ''}</span>
          ) : (
            <span className="ms-tag">{ders.metin ? 'Ses yok' : 'Metin bekliyor'}</span>
          )}
          {ders.varyantlar.length > 1 && <span className="ms-tag">+{ders.varyantlar.length - 1} alternatif</span>}
        </div>
        {ana && (
          <div className="sa-quick">
            <Oynatici dersKey={ders.key} v={ana} calan={calan} setCalan={setCalan} sesUrl={sesUrl} />
            <a className="ms-btn is-sm" href={sesUrl(ders.key, ana.id, true)} download><Download /> MP3</a>
          </div>
        )}
      </div>

      {acik && (
        <div className="sa-body">
          {ders.varyantlar.length > 0 && (
            <ul className="sa-variants">
              {ders.varyantlar.map((v, i) => (
                <li key={v.id}>
                  <div className="min-w-0 flex-1">
                    <div className="sa-vt">
                      {i === 0 && <Star className="w-3.5 h-3.5" aria-label="Varsayılan" />} <b>{v.etiket}</b>
                      {v.ucretli && <span className="ms-tag">ücretli{v.maliyetTL ? ` · ${v.maliyetTL.toFixed(2)} TL` : ''}</span>}
                      {v.metinGuncel === false && <span className="ms-tag" title="Metin bu ses üretildikten sonra değişti">metin değişti</span>}
                    </div>
                    <small>
                      {sure(v.sureSn)} · {mb(v.bayt)} · {timeLabel(v.olusturuldu, true)}
                      {v.dogrulama ? ` · döküm doğrulaması ${v.dogrulama.parca}/${v.dogrulama.toplam} parça${v.dogrulama.ortalama ? `, ort. %${v.dogrulama.ortalama}` : ''}` : ''}
                    </small>
                  </div>
                  <div className="sa-vact">
                    <Oynatici dersKey={ders.key} v={v} calan={calan} setCalan={setCalan} sesUrl={sesUrl} />
                    <a className="ms-btn is-sm" href={sesUrl(ders.key, v.id, true)} download title={`${kisaEtiket(v)} MP3 indir`}><Download /> İndir</a>
                    {i > 0 && (
                      <button type="button" className="ms-btn is-sm" onClick={() => void post('/api/sesli-anlatim/varsayilan', { key: ders.key, vid: v.id })}>
                        <Star /> Varsayılan yap
                      </button>
                    )}
                    {i > 0 && (
                      <ConfirmButton
                        icon={Trash2}
                        confirmLabel="Silinsin mi?"
                        onConfirm={async () => {
                          const r = await safeJsonFetch<any>(`/api/sesli-anlatim/ses/${ders.key}/${v.id}`, { method: 'DELETE', headers: await yetkili(headers) });
                          if (!r.ok) toast.error((r.data as any)?.error || 'Silinemedi.');
                          await yukle();
                        }}
                      >
                        Sil
                      </ConfirmButton>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          )}

          {ders.isler.map((x) => (
            <div key={x.id} className={`sa-job is-${x.durum}`}>
              <span className="ms-tag">{DURUM_ETIKET[x.durum] || x.durum}</span> {saglayicilar.find((s) => s.id === x.saglayici)?.etiket} · {x.ses}
              {x.ilerleme.toplam > 0 && (
                <div className="sa-bar"><i style={{ width: `${(100 * x.ilerleme.bitti) / x.ilerleme.toplam}%` }} /><span>{x.ilerleme.bitti}/{x.ilerleme.toplam}</span></div>
              )}
              {x.hata && <div className="sa-err">{x.hata}</div>}
            </div>
          ))}

          {ders.metin && (
            <div className="sa-alt">
              <b><Plus className="w-4 h-4 inline" /> Alternatif oluştur</b>
              <select className="ms-input" value={sag} onChange={(e) => setSag(e.target.value as Saglayici)} aria-label="Ses ajanı">
                {saglayicilar.map((s) => (
                  <option key={s.id} value={s.id} disabled={s.ucretli && !ucretliAktif}>
                    {s.etiket}{s.ucretli ? (ucretliAktif ? ' (ücretli)' : ' (ücretli · kapalı)') : ' (ücretsiz)'}
                  </option>
                ))}
              </select>
              <select className="ms-input" value={ses} onChange={(e) => setSes(e.target.value)} aria-label="Ses">
                {(sb?.sesler || []).map((s) => <option key={s} value={s}>{s}</option>)}
              </select>
              <OrnekDinle d={d} saglayici={sag} ses={ses} url={ornekUrl} />
              <button type="button" className={`ms-btn is-sm ${sb?.ucretli ? 'is-danger' : 'is-primary'}`} onClick={() => void alternatif()} disabled={sb?.ucretli && (!butce.anahtarVar || !ucretliAktif)}>
                <AudioLines /> {sb?.ucretli ? `Ücretli oluştur (~${tahminiTL.toLocaleString('tr-TR')} TL)` : 'Oluştur'}
              </button>
              <small className="sa-hint">
                Her ses MP3 olarak indirilebilir. Ücretli seçenek yalnız sen bastığında çalışır; kalan bütçe {butce.kalanTL} TL.
              </small>
            </div>
          )}

          {ders.metin && (
            <div>
              <button type="button" className="ms-btn is-sm" onClick={() => void metniAc()}><FileText /> {metinAcik ? 'Metni gizle' : 'Konuşma metnini göster'}</button>
              {metinAcik && <pre className="sa-text">{metin ?? 'Yükleniyor…'}</pre>}
            </div>
          )}
        </div>
      )}
    </li>
  );
};

/**
 * Yerel ses planı: hangi derse hangi yerel sesle (XTTS konuşmacısı / EMA) alternatif üretileceği. Plan sunucuda tutulur;
 * "Planı kuyruğa al" yalnız henüz hazır ya da sırada olmayan satırları kuyruğa ekler (bu PC işçisi sırayla alır).
 */
const YerelPlan: React.FC<{ d: Durum; post: (yol: string, body?: any) => Promise<boolean>; ornekUrl: (sag: string, ses: string) => string }> = ({ d, post, ornekUrl }) => {
  const [acik, setAcik] = useState(false);
  const [ara, setAra] = useState('');
  const [secili, setSecili] = useState<Set<string>>(new Set());
  const yereller = d.saglayicilar.filter((s) => s.id === 'xtts-yerel' || s.id === 'ema-yerel');
  const [topluSag, setTopluSag] = useState<Saglayici>('xtts-yerel');
  const topluSb = yereller.find((s) => s.id === topluSag) || yereller[0];
  const [topluSes, setTopluSes] = useState(topluSb?.varsayilanSes || '');
  useEffect(() => {
    if (topluSb && !topluSb.sesler.includes(topluSes)) setTopluSes(topluSb.varsayilanSes);
  }, [topluSag]); // eslint-disable-line react-hooks/exhaustive-deps
  const plan = d.yerelPlan || {};

  const durumu = (x: Ders) => {
    const p = plan[x.key];
    if (!p) return null;
    if (x.varyantlar.some((v) => v.saglayici === p.saglayici && v.ses === p.ses)) return 'hazir';
    if (x.isler.some((j) => j.saglayici === p.saglayici && j.ses === p.ses)) return 'sirada';
    return 'bekliyor';
  };
  const dersler = useMemo(() => {
    const q = ara.trim().toLocaleLowerCase('tr-TR');
    return d.dersler
      .filter((x) => x.metin)
      .filter((x) => !q || x.baslik.toLocaleLowerCase('tr-TR').includes(q) || String(x.no) === q)
      .sort((a, b) => a.sira - b.sira);
  }, [d.dersler, ara]);
  const bekleyen = d.dersler.filter((x) => durumu(x) === 'bekliyor');
  const kaydet = (degisiklik: Record<string, { saglayici: Saglayici; ses: string } | null>) => post('/api/sesli-anlatim/yerel/plan', { plan: degisiklik });
  const toplu = async (kaldir: boolean) => {
    if (!secili.size) return toast.error('Önce ders seç.');
    const ok = await kaydet(Object.fromEntries([...secili].map((k) => [k, kaldir ? null : { saglayici: topluSag, ses: topluSes }])));
    if (ok) toast.success(kaldir ? `${secili.size} ders plandan çıkarıldı.` : `${secili.size} derse ${topluSes} atandı.`);
  };
  const kuyrugaAl = async (keys?: string[]) => {
    const hedef = keys ? bekleyen.filter((x) => keys.includes(x.key)) : bekleyen;
    if (!hedef.length) return toast.error('Kuyruğa alınacak plan satırı yok (hepsi hazır ya da sırada).');
    const dk = hedef.reduce((t, x) => t + x.tahminiDk, 0);
    const ok = await confirmDialog({
      title: `${hedef.length} ders bu bilgisayarda seslendirilsin mi?`,
      message: `${hedef.slice(0, 6).map((x) => `${x.no}. ${x.baslik} → ${plan[x.key].ses}`).join('\n')}${hedef.length > 6 ? `\n… ve ${hedef.length - 6} ders daha` : ''}\n\nToplam ~${dk} dk ses; bu PC'de tahmini ~${Math.max(5, Math.round(dk * 0.4))} dk sürer (GPU en fazla %70, 80 °C üstünde yavaşlar). Dersler sırayla alınır, ücretsiz.`,
      confirmLabel: 'Onayla ve kuyruğa al',
    });
    if (!ok) return;
    if (await post('/api/sesli-anlatim/yerel/plan/kuyruga', keys ? { keys } : {})) toast.success(`${hedef.length} ders kuyruğa alındı.`);
  };
  const tumSecili = dersler.length > 0 && dersler.every((x) => secili.has(x.key));

  return (
    <Panel
      title="Yerel ses planı"
      icon={Cpu}
      count={Object.keys(plan).length}
      desc="Hangi derse hangi yerel sesle (Coqui XTTS v2 konuşmacısı ya da EMA) alternatif oluşturulacağını seç. Plan kaydedilir; onayladığında yalnız henüz hazır ya da sırada olmayan dersler bu bilgisayarın kuyruğuna girer."
      flush={!acik}
      tools={
        <>
          <span className="ms-tag">{bekleyen.length} bekliyor</span>
          <button type="button" className="ms-btn is-sm is-primary" disabled={!bekleyen.length} onClick={() => void kuyrugaAl()}>
            <ListOrdered /> Planı kuyruğa al
          </button>
          <button type="button" className="ms-btn is-sm" onClick={() => setAcik((v) => !v)}>{acik ? 'Gizle' : 'Düzenle'}</button>
        </>
      }
    >
      {acik && (
        <div className="sa-plan">
          <div className="sa-plan-bar">
            <label className="sa-plan-chk">
              <input
                type="checkbox"
                checked={tumSecili}
                onChange={() => setSecili(tumSecili ? new Set() : new Set(dersler.map((x) => x.key)))}
              />
              <span>Tümü ({secili.size})</span>
            </label>
            <select className="ms-input" value={topluSag} onChange={(e) => setTopluSag(e.target.value as Saglayici)} aria-label="Toplu atama sağlayıcısı">
              {yereller.map((s) => <option key={s.id} value={s.id}>{s.etiket}</option>)}
            </select>
            <select className="ms-input" value={topluSes} onChange={(e) => setTopluSes(e.target.value)} aria-label="Toplu atama sesi">
              {(topluSb?.sesler || []).map((x) => <option key={x} value={x}>{x}</option>)}
            </select>
            <OrnekDinle d={d} saglayici={topluSag} ses={topluSes} url={ornekUrl} />
            <button type="button" className="ms-btn is-sm" onClick={() => void toplu(false)} disabled={!secili.size}>Seçilenlere ata</button>
            <button type="button" className="ms-btn is-sm" onClick={() => void toplu(true)} disabled={!secili.size}><X /> Plandan çıkar</button>
            {secili.size > 0 && (
              <button type="button" className="ms-btn is-sm" onClick={() => void kuyrugaAl([...secili])}>Seçilenleri kuyruğa al</button>
            )}
            <div className="flex-1 min-w-[180px]"><SearchBox value={ara} onChange={setAra} placeholder="Ders adı ya da no" /></div>
          </div>
          <ul className="sa-plan-list">
            {dersler.map((x) => {
              const p = plan[x.key];
              const sb = yereller.find((s) => s.id === p?.saglayici);
              const dr = durumu(x);
              return (
                <li key={x.key} className={p ? 'is-planned' : ''}>
                  <input
                    type="checkbox"
                    className="sa-plan-chk-i"
                    aria-label={`${x.no}. ${x.baslik} seç`}
                    checked={secili.has(x.key)}
                    onChange={() => setSecili((o) => { const n = new Set(o); if (n.has(x.key)) n.delete(x.key); else n.add(x.key); return n; })}
                  />
                  <span className="sa-plan-t" title={`${x.no}. ${x.baslik}`}>
                    <span className="sa-no">{x.no}</span>
                    <span className="sa-plan-ad">{x.baslik} <small>~{x.tahminiDk} dk</small></span>
                  </span>
                  <select
                    className="ms-input sa-plan-sag"
                    value={p?.saglayici || ''}
                    aria-label={`${x.baslik} yerel ses ajanı`}
                    onChange={(e) => {
                      const sag = e.target.value as Saglayici;
                      const yeni = yereller.find((s) => s.id === sag);
                      void kaydet({ [x.key]: yeni ? { saglayici: sag, ses: yeni.varsayilanSes } : null });
                    }}
                  >
                    <option value="">— yerel ses yok</option>
                    {yereller.map((s) => <option key={s.id} value={s.id}>{s.id === 'xtts-yerel' ? 'XTTS v2' : s.id === 'ema-yerel' ? 'EMA' : s.etiket}</option>)}
                  </select>
                  <select
                    className="ms-input sa-plan-ses"
                    value={p?.ses || ''}
                    disabled={!p}
                    aria-label={`${x.baslik} konuşmacı`}
                    onChange={(e) => void kaydet({ [x.key]: { saglayici: p!.saglayici, ses: e.target.value } })}
                  >
                    {!p && <option value="">—</option>}
                    {(sb?.sesler || []).map((v) => <option key={v} value={v}>{v}</option>)}
                  </select>
                  <span className="sa-plan-dinle"><OrnekDinle d={d} saglayici={p?.saglayici} ses={p?.ses} url={ornekUrl} /></span>
                  <span className={`ms-tag sa-plan-drm ${dr === 'hazir' ? 'is-ok' : dr === 'sirada' ? 'is-accent' : ''}`}>
                    {dr === 'hazir' ? 'Hazır' : dr === 'sirada' ? 'Sırada' : dr === 'bekliyor' ? 'Planlandı' : '—'}
                  </span>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </Panel>
  );
};

export default ManageSesliAnlatimSection;
