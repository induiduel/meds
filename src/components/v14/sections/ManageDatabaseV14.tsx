import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Download, RefreshCw, Upload, Wrench } from 'lucide-react';
import { AdminPanelModal } from '../../AdminPanelModal';
import { Drawer } from '../../manage/consoleUi';
import { ApiService } from '../../../services/api';
import { triggerBackupNow } from '../../../services/manageConsoleService';
import { adminCall } from '../../../services/peopleService';
import { BulkBar, useSelection } from '../manageKit';
import { Card14, DataTable, DetailLayout, DetailNav, FactList, PageActions, Pill, StatRow, Tabs14, Toolbar, type Col } from '../pageKit';

/**
 * v14 "Veritabanı ve yedek" (canvas Yedekler.dc.html).
 * Yedekler: Oracle'daki gece pg_dump yedekleri (GET /api/admin/pg/backups, salt okunur; liste backup.sh'tan gelir).
 * Eşitleme durumu: yerel veri kümeleri ve son eşitleme sonucu.
 * Eşitleme ve içe aktarma hiçbir zaman kendiliğinden çalışmaz; içe aktarma açık onay ister.
 * Eski sekmenin geri kalan araçları (çoklu veritabanı modu, anahtarlar, DeepSeek, slayt onarımı) "Gelişmiş araçlar"da.
 */

type Props = React.ComponentProps<typeof AdminPanelModal>;
type Tab = 'backups' | 'status' | 'io';
type SetRow = { id: string; name: string; count: number | null; where: string };
type SyncResult = { at: string; ok: boolean; message: string };
type Pending = { name: string; questions: number; committees: number; data: any };

const CONFIRM_WORD = 'İÇE AKTAR';

export const ManageDatabaseV14: React.FC<Props> = (props) => {
  const { adminEmail, committees, questions, onRefreshData } = props;
  const [tab, setTab] = useState<Tab>('backups');
  const [pgOnline, setPgOnline] = useState<boolean | null>(null);
  const [checking, setChecking] = useState(false);
  const [syncing, setSyncing] = useState(false);
  const [syncArmed, setSyncArmed] = useState(false);
  const [lastSync, setLastSync] = useState<SyncResult | null>(null);
  const [msg, setMsg] = useState<{ tone: 'ok' | 'bad'; text: string } | null>(null);
  const [advanced, setAdvanced] = useState(false);
  const [detail, setDetail] = useState<SetRow | null>(null);
  const [pending, setPending] = useState<Pending | null>(null);
  const [typed, setTyped] = useState('');
  const [importing, setImporting] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const checkHealth = useCallback(async () => {
    setChecking(true);
    try {
      const r = await fetch('/api/health');
      const j = await r.json();
      setPgOnline(!!j?.database?.online);
    } catch {
      setPgOnline(false);
    } finally {
      setChecking(false);
    }
  }, []);
  useEffect(() => { void checkHealth(); }, [checkHealth]);

  useEffect(() => {
    if (!syncArmed) return;
    const t = window.setTimeout(() => setSyncArmed(false), 4000);
    return () => window.clearTimeout(t);
  }, [syncArmed]);

  const runSync = async () => {
    if (!syncArmed) return setSyncArmed(true);
    setSyncArmed(false);
    setSyncing(true);
    setMsg(null);
    const r = await triggerBackupNow(adminEmail);
    setLastSync({ at: new Date().toISOString(), ok: r.ok, message: r.message });
    setMsg({ tone: r.ok ? 'ok' : 'bad', text: r.message });
    setSyncing(false);
    void checkHealth();
  };

  const exportJson = async () => {
    try {
      const data = await ApiService.adminExportDb();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `medsoru_database_backup_${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
      setMsg({ tone: 'ok', text: 'JSON yedeği indirildi.' });
    } catch (e: any) {
      setMsg({ tone: 'bad', text: `Dışa aktarılamadı: ${e?.message || 'bilinmeyen hata'}` });
    }
  };

  const pickFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    e.target.value = '';
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const json = JSON.parse(String(reader.result || ''));
        setPending({ name: file.name, questions: json?.questions?.length || 0, committees: json?.committees?.length || 0, data: json });
        setTyped('');
      } catch {
        setMsg({ tone: 'bad', text: 'Dosya geçerli bir JSON değil.' });
      }
    };
    reader.readAsText(file);
  };

  const confirmImport = async () => {
    if (!pending || typed.trim().toLocaleUpperCase('tr-TR') !== CONFIRM_WORD) return;
    setImporting(true);
    try {
      await ApiService.adminImportDb(adminEmail, pending.data);
      setMsg({ tone: 'ok', text: `İçe aktarıldı: ${pending.questions.toLocaleString('tr-TR')} soru.` });
      setPending(null);
      await onRefreshData();
    } catch (e: any) {
      setMsg({ tone: 'bad', text: `İçe aktarılamadı: ${e?.message || 'bilinmeyen hata'}` });
    } finally {
      setImporting(false);
    }
  };

  const rows: SetRow[] = [
    { id: 'questions', name: 'Soru havuzu', count: questions.length, where: 'yerel JSON → meds-pg' },
    { id: 'committees', name: 'Kurullar', count: committees.length, where: 'yerel JSON → meds-pg' },
  ];
  const cols: Col<SetRow>[] = [
    { key: 'n', label: 'Veri kümesi', main: true, render: (r) => r.name },
    { key: 'c', label: 'Kayıt', right: true, render: (r) => (r.count ?? 0).toLocaleString('tr-TR') },
    { key: 'w', label: 'Konum', mono: true, render: (r) => r.where },
    {
      key: 's', label: 'Son eşitleme', render: () =>
        lastSync ? <Pill tone={lastSync.ok ? 'ok' : 'bad'}>{lastSync.ok ? 'Eşitlendi' : 'Hata'}</Pill> : <Pill tone="">Bu oturumda yok</Pill>,
    },
  ];
  const fmt = (iso: string) => new Date(iso).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });

  return (
    <div style={{ display: "grid", gap: 16, minWidth: 0 }}>
      <PageActions note="Yerel veriler 6 saatte bir kendiliğinden meds-pg'ye eşitlenir. Elle eşitleme yalnız bu düğmeyle, onayla çalışır.">
        <button type="button" className="m14-btn" onClick={() => setAdvanced(true)}>
          <Wrench aria-hidden="true" /> Gelişmiş araçlar
        </button>
        <button type="button" className="m14-btn" onClick={exportJson}>
          <Download aria-hidden="true" /> JSON yedeği indir
        </button>
        <button type="button" className="m14-btn primary" onClick={runSync} disabled={syncing} aria-live="polite">
          <RefreshCw aria-hidden="true" className={syncing ? 'animate-spin' : ''} />
          {syncing ? 'Eşitleniyor' : syncArmed ? 'Onaylamak için tekrar dokun' : 'Şimdi eşitle (yerel → meds-pg)'}
        </button>
      </PageActions>

      <StatRow
        stats={[
          {
            label: 'Etkin veritabanı',
            value: pgOnline === null ? '…' : pgOnline ? 'meds-pg' : 'Ulaşılamıyor',
            tone: pgOnline === null ? undefined : pgOnline ? 'ok' : 'bad',
            onClick: () => void checkHealth(),
            hint: checking ? 'Denetleniyor' : 'Yeniden denetlemek için dokun',
          },
          { label: 'Son eşitleme', value: lastSync ? fmt(lastSync.at) : '—', tone: lastSync ? (lastSync.ok ? 'ok' : 'bad') : undefined },
          { label: 'Soru', value: questions.length.toLocaleString('tr-TR') },
          { label: 'Kurul', value: committees.length.toLocaleString('tr-TR') },
        ]}
      />

      {msg && (
        <p role="status" className={`pk14-note`} style={{ color: msg.tone === 'ok' ? 'var(--color-ok)' : 'var(--color-bad)' }}>
          {msg.text}
        </p>
      )}

      <Toolbar>
        <Tabs14<Tab>
          label="Veritabanı görünümü"
          value={tab}
          onChange={setTab}
          options={[{ id: 'backups', label: 'Gece yedekleri' }, { id: 'status', label: 'Eşitleme durumu' }, { id: 'io', label: 'İçe / dışa aktarma' }]}
        />
      </Toolbar>

      {tab === 'backups' && <YedekListesi />}

      {tab === 'status' && (
        <DataTable rows={rows} cols={cols} rowKey={(r) => r.id} onOpen={setDetail} activeKey={detail?.id} minWidth={520} />
      )}

      {tab === 'io' && (
        <>
          <Card14 title="Dışa aktarma">
            <p className="pk14-note">Soru havuzu ve kurulların tamamı tek JSON dosyası olarak indirilir.</p>
            <button type="button" className="m14-btn" onClick={exportJson}><Download aria-hidden="true" /> JSON yedeği indir</button>
          </Card14>
          <Card14 title="İçe aktarma">
            <p className="pk14-note">Seçilen dosyadaki veriler mevcut verinin üzerine yazılır. Dosya seçmek hiçbir şeyi değiştirmez; ardından açık onay istenir.</p>
            <input ref={fileRef} type="file" accept="application/json,.json" onChange={pickFile} hidden />
            <button type="button" className="m14-btn" onClick={() => fileRef.current?.click()}><Upload aria-hidden="true" /> JSON dosyası seç</button>
          </Card14>
          <Card14 title="Sıfırlama">
            <p className="pk14-note">Toptan sıfırlama sunucuda kapalıdır; kullanıcı kaynaklı ham veri silinemez.</p>
          </Card14>
        </>
      )}

      <Drawer open={!!detail} onClose={() => setDetail(null)} title={detail?.name || ''} label="Veri kümesi ayrıntısı">
        {detail && (
          <>
            <FactList
              items={[
                { k: 'Kayıt sayısı', v: (detail.count ?? 0).toLocaleString('tr-TR') },
                { k: 'Konum', v: detail.where },
                { k: 'Etkin veritabanı', v: pgOnline ? 'meds-pg (çevrimiçi)' : 'meds-pg ulaşılamıyor' },
                { k: 'Son eşitleme', v: lastSync ? `${fmt(lastSync.at)}: ${lastSync.message}` : 'Bu oturumda yapılmadı' },
              ]}
            />
            <Card14 title="Yedekten geri yükleme">
              <p className="pk14-note">Geri yükleme bir JSON yedeğinden yapılır ve mevcut verinin üzerine yazar. Önce güncel yedeği indirin, sonra dosyayı seçip onay kelimesini yazın.</p>
              <div className="pk14-actions-btns">
                <button type="button" className="m14-btn" onClick={exportJson}><Download aria-hidden="true" /> Önce güncel yedeği indir</button>
                <button type="button" className="m14-btn" onClick={() => fileRef.current?.click()}><Upload aria-hidden="true" /> Yedek dosyası seç</button>
              </div>
              {tab !== 'io' && <input ref={fileRef} type="file" accept="application/json,.json" onChange={pickFile} hidden />}
            </Card14>
          </>
        )}
      </Drawer>

      <Drawer
        open={!!pending}
        onClose={() => !importing && setPending(null)}
        title="Yedek içe aktarılsın mı?"
        label="İçe aktarma onayı"
        foot={
          <div className="pk14-actions-btns">
            <button type="button" className="m14-btn" onClick={() => setPending(null)} disabled={importing}>Vazgeç</button>
            <button
              type="button"
              className="m14-btn primary"
              onClick={confirmImport}
              disabled={importing || typed.trim().toLocaleUpperCase('tr-TR') !== CONFIRM_WORD}
            >
              {importing ? 'İçe aktarılıyor' : 'İçe aktar ve üzerine yaz'}
            </button>
          </div>
        }
      >
        {pending && (
          <>
            <FactList
              items={[
                { k: 'Dosya', v: <span style={{ overflowWrap: 'anywhere' }}>{pending.name}</span> },
                { k: 'Dosyadaki soru', v: pending.questions.toLocaleString('tr-TR') },
                { k: 'Dosyadaki kurul', v: pending.committees.toLocaleString('tr-TR') },
                { k: 'Şu anki soru', v: questions.length.toLocaleString('tr-TR') },
              ]}
            />
            <label className="pk14-note" style={{ display: 'block', marginTop: 12 }}>
              Onaylamak için <strong>{CONFIRM_WORD}</strong> yazın
              <input
                type="text"
                value={typed}
                onChange={(e) => setTyped(e.target.value)}
                className="pk14-search"
                style={{ display: 'block', width: '100%', maxWidth: 320, marginTop: 6, padding: '8px 10px', border: '1px solid var(--color-line)', borderRadius: 8, background: 'var(--color-field)', color: 'var(--color-ink)' }}
                autoComplete="off"
              />
            </label>
          </>
        )}
      </Drawer>

      <Drawer open={advanced} onClose={() => setAdvanced(false)} title="Gelişmiş araçlar" label="Eski veritabanı araçları" wide>
        {advanced && <AdminPanelModal {...props} variant="embedded" tab="database" isOpen />}
      </Drawer>
    </div>
  );
};

export default ManageDatabaseV14;

type Yedek = { ad: string; boyut: number; tarih: string; ogeler: number; tablolar: number; dogrulandi: boolean };
type YedekYaniti = { available: boolean; note?: string; guncellendi?: string; klasor?: string; saklama_gun?: number; backups: Yedek[]; geri_yukleme?: string };

const tarihYaz = (iso: string) => new Date(iso).toLocaleString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
const boyutYaz = (b: number) => (b > 1e9 ? `${(b / 1e9).toFixed(2)} GB` : `${Math.round(b / 1e6)} MB`);
const kopyala = (t: string) => navigator.clipboard?.writeText(t).catch(() => {});

/** Gece yedekleri: listeleme, içindekiler denetimi sonucu, geri yükleme komutu (geri yükleme sunucudan elle yapılır). */
const YedekListesi: React.FC = () => {
  const [veri, setVeri] = useState<YedekYaniti | null>(null);
  const [hata, setHata] = useState('');
  const [acik, setAcik] = useState<Yedek | null>(null);
  const [bilgi, setBilgi] = useState('');
  const sec = useSelection<string>();
  const yukle = useCallback(async () => {
    try { setVeri(await adminCall<YedekYaniti>('/api/admin/pg/backups')); setHata(''); }
    catch (e: any) { setHata(e?.message || 'Yedek listesi alınamadı.'); }
  }, []);
  useEffect(() => { void yukle(); }, [yukle]);
  const liste = veri?.backups || [];
  const komut = (y: Yedek) => (veri?.geri_yukleme || 'docker exec -i meds-pg pg_restore -U meds -d meds --clean --if-exists < DOSYA').replace('DOSYA', `${veri?.klasor || '~/yedek/meds-pg'}/${y.ad}`);
  const cols: Col<Yedek>[] = [
    { key: 'ad', label: 'Yedek', main: true, render: (y) => y.ad },
    { key: 'd', label: 'Doğrulama', render: (y) => <Pill tone={y.dogrulandi ? 'ok' : 'bad'}>{y.dogrulandi ? 'Doğrulandı' : 'Sorunlu'}</Pill> },
    { key: 'b', label: 'Boyut', right: true, render: (y) => boyutYaz(y.boyut) },
    { key: 't', label: 'Tablo verisi', right: true, render: (y) => y.tablolar.toLocaleString('tr-TR') },
    { key: 'z', label: 'Tarih', muted: true, render: (y) => tarihYaz(y.tarih) },
  ];
  if (hata) return <p className="pk14-note" role="alert" style={{ color: 'var(--color-bad)' }}>{hata}</p>;
  if (!veri) return <p className="pk14-note">Yükleniyor…</p>;
  if (!veri.available) return <Card14 title="Gece yedekleri"><p className="pk14-note">{veri.note}</p></Card14>;
  const secili = liste.filter((y) => sec.has(y.ad));
  return (
    <>
      <p className="pk14-note">
        {liste.length} yedek · her gece 03:30 alınır, son {veri.saklama_gun ?? 7} gün saklanır · liste {veri.guncellendi ? tarihYaz(veri.guncellendi) : '—'} tarihinde güncellendi.
        Doğrulama, dosyanın içindekiler listesinin okunabildiğini ve tablo verisi içerdiğini gösterir.
      </p>
      {bilgi && <p className="pk14-note" role="status">{bilgi}</p>}
      <BulkBar
        count={sec.count}
        noun="yedek"
        onClear={sec.clear}
        actions={[
          { label: 'Geri yükleme komutlarını kopyala', kind: 'main', run: () => { void kopyala(secili.map(komut).join('\n')); setBilgi(`${secili.length} komut panoya kopyalandı.`); } },
          { label: 'Listeyi JSON indir', run: () => {
            const a = document.createElement('a');
            a.href = URL.createObjectURL(new Blob([JSON.stringify(secili, null, 2)], { type: 'application/json' }));
            a.download = 'yedekler.json';
            a.click();
            setTimeout(() => URL.revokeObjectURL(a.href), 2000);
          } },
        ]}
      />
      <DataTable rows={liste} cols={cols} rowKey={(y) => y.ad} onOpen={setAcik} activeKey={acik?.ad} selection={sec} minWidth={620} />
      <Drawer
        open={!!acik}
        onClose={() => setAcik(null)}
        title={acik?.ad || ''}
        head={acik ? <DetailNav list={liste} current={acik} same={(a, b) => a.ad === b.ad} onGo={setAcik} /> : undefined}
        foot={acik ? <button type="button" className="m14-btn primary" onClick={() => { void kopyala(komut(acik)); setBilgi('Geri yükleme komutu panoya kopyalandı.'); }}>Geri yükleme komutunu kopyala</button> : undefined}
      >
        {acik && (
          <DetailLayout
            main={
              <Card14 title="Geri yükleme">
                <p className="pk14-note">
                  Geri yükleme canlı veritabanının üzerine yazar ve panelden çalıştırılmaz. Oracle sunucusunda önce yeni bir yedek alın
                  (<code>bash deploy/pg/backup.sh</code>), sonra aşağıdaki komutu çalıştırın.
                </p>
                <pre className="jv14-raw">{komut(acik)}</pre>
              </Card14>
            }
            side={<FactList items={[
              { k: 'Durum', v: <Pill tone={acik.dogrulandi ? 'ok' : 'bad'}>{acik.dogrulandi ? 'Doğrulandı' : 'Sorunlu'}</Pill> },
              { k: 'Boyut', v: boyutYaz(acik.boyut) },
              { k: 'Tarih', v: tarihYaz(acik.tarih) },
              { k: 'İçindekiler', v: `${acik.ogeler.toLocaleString('tr-TR')} öge` },
              { k: 'Tablo verisi', v: acik.tablolar.toLocaleString('tr-TR') },
              { k: 'Klasör', v: veri.klasor },
            ]} />}
          />
        )}
      </Drawer>
    </>
  );
};
