import { useCallback, useEffect, useMemo, useState } from 'react';
import { safeJsonFetch } from '../../services/api';
import { PageActions, StatRow, Tabs14, SearchField, Toolbar, DataTable, DetailNav, DetailLayout, FactList, Card14, type Col } from '../v14/pageKit';
import { BulkBar, useSelection, JsonView } from '../v14/manageKit';
import { Drawer } from './consoleUi';

/**
 * Yönetim konsolu — MeDSor Core v2 bölümü.
 * v2 veri durumu, denetim özeti, kavram grafı ve toplu tamamlama adaylarını gösterir (salt okunur).
 */
type Tab = 'denetim' | 'kume' | 'graf';
type Kume = { i: number; raw: any; stem: string; parca: number };

export function ManageDataCoreSection({ notify }: { notify?: (msg: string) => void }) {
  const [stats, setStats] = useState<any>(null);
  const [audit, setAudit] = useState<any>(null);
  const [graph, setGraph] = useState<any>(null);
  const [clusters, setClusters] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<Tab>('kume');
  const [q, setQ] = useState('');
  const [open, setOpen] = useState<Kume | null>(null);
  const sel = useSelection<string>();

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [s, a, g, c] = await Promise.all([
        safeJsonFetch('/api/v2/stats'),
        safeJsonFetch('/api/v2/audit?summary=1'),
        safeJsonFetch('/api/v2/graph'),
        safeJsonFetch('/api/v2/cluster?limit=20'),
      ]);
      setStats(s.data);
      setAudit(a.data);
      setGraph(g.data);
      setClusters(c.data?.ornekler || []);
    } catch (e: any) {
      notify?.('v2 verisi alınamadı: ' + (e?.message || ''));
    } finally {
      setLoading(false);
    }
  }, [notify]);

  useEffect(() => { load(); }, [load]);

  const kumeler: Kume[] = useMemo(() => clusters.map((c, i) => {
    const m = c.birlesik || c;
    return { i, raw: c, stem: String(m.stem || ''), parca: Number(m.birlesik_parca_sayisi ?? 1) };
  }), [clusters]);
  const shown = useMemo(() => {
    const s = q.trim().toLocaleLowerCase('tr');
    return s ? kumeler.filter((k) => k.stem.toLocaleLowerCase('tr').includes(s)) : kumeler;
  }, [kumeler, q]);

  const cols: Col<Kume>[] = [
    { key: 'stem', label: 'Aday soru kökü', main: true, render: (k) => k.stem || '—' },
    { key: 'parca', label: 'Parça', right: true, width: 90, render: (k) => k.parca },
  ];

  const copySelected = async () => {
    const rows = kumeler.filter((k) => sel.has(String(k.i))).map((k) => k.raw);
    try {
      await navigator.clipboard.writeText(JSON.stringify(rows, null, 2));
      notify?.(`${rows.length} aday panoya kopyalandı`);
      sel.clear();
    } catch {
      notify?.('Panoya kopyalanamadı');
    }
  };

  return (
    <div className="space-y-4">
      <PageActions note="Bağımsız MeDSor Core v2 hattı: kaynaktan doğrulanmış sorular, müfredat/kazanım, ders notu bağları, kavram grafı ve toplu tamamlama. GPU/AI kullanılmaz.">
        <button type="button" className="m14-btn" onClick={load} disabled={loading}>{loading ? 'Yükleniyor…' : 'Yenile'}</button>
      </PageActions>

      {stats && (
        <StatRow stats={[
          { label: 'Soru', value: String(stats.sorular ?? 0) },
          { label: 'Cevaplı', value: String(stats.cevapli ?? 0) },
          { label: 'Açık uçlu', value: String(stats.acik_uclu ?? 0) },
          { label: 'Kazanımlı', value: String(stats.kazanimli ?? 0) },
          { label: 'Kaynağa bağlı', value: String(stats.kaynak_bagli ?? 0) },
          { label: 'Not dosyası', value: String(stats.notlar_dosya ?? 0) },
          { label: 'Özet dosyası', value: String(stats.ozet_dosya ?? 0) },
          { label: 'Vektör', value: String(stats.vektor?.sayi ?? 0) },
        ]} />
      )}

      <Toolbar>
        <Tabs14<Tab> label="Veri merkezi görünümü" value={tab} onChange={setTab} options={[
          { id: 'denetim', label: 'Denetim' },
          { id: 'kume', label: 'Kümeler', n: clusters.length },
          { id: 'graf', label: 'Grafik' },
        ]} />
        {tab === 'kume' && <SearchField value={q} onChange={setQ} placeholder="Aday kökünde ara" />}
      </Toolbar>

      {tab === 'denetim' && (
        <Card14 title={audit?.zaman ? `Eski veri denetimi (${audit.zaman})` : 'Eski veri denetimi'}>
          {audit?.toplam ? (
            <FactList items={[
              { k: 'Kayıt', v: audit.toplam.kayit },
              { k: 'Engelleyici', v: audit.toplam.blocking },
              { k: 'İnceleme', v: audit.toplam.review },
              { k: 'İnceleme kuyruğu', v: audit.inceleme_kuyrugu },
            ]} />
          ) : <p className="pk14-note">{loading ? 'Yükleniyor…' : 'Denetim özeti yok.'}</p>}
        </Card14>
      )}

      {tab === 'graf' && (
        <Card14 title="Kavram grafı">
          {graph ? <FactList items={[{ k: 'Düğüm', v: graph.dugum }, { k: 'Kenar', v: graph.kenar }]} /> : <p className="pk14-note">{loading ? 'Yükleniyor…' : 'Graf verisi yok.'}</p>}
        </Card14>
      )}

      {tab === 'kume' && (
        <>
          <BulkBar count={sel.count} noun="aday" onClear={sel.clear} actions={[{ label: 'JSON olarak kopyala', kind: 'main', run: copySelected }]} />
          <DataTable<Kume>
            rows={shown}
            cols={cols}
            rowKey={(k) => String(k.i)}
            onOpen={setOpen}
            selection={sel}
            busy={loading}
            minWidth={420}
            activeKey={open ? String(open.i) : null}
            empty={loading ? 'Yükleniyor…' : 'Toplu tamamlama adayı yok.'}
          />
        </>
      )}

      <Drawer
        open={!!open}
        onClose={() => setOpen(null)}
        title="Toplu tamamlama adayı"
        wide
        head={<DetailNav list={shown} current={open} same={(a, b) => a.i === b.i} onGo={setOpen} />}
      >
        {open && (
          <DetailLayout
            main={<Card14 title="Kayıt"><JsonView value={open.raw} /></Card14>}
            side={<FactList items={[{ k: 'Sıra', v: open.i + 1 }, { k: 'Parça', v: open.parca }]} />}
          />
        )}
      </Drawer>
    </div>
  );
}
