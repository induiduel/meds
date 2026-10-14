import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { ChevronDown, FileText, RefreshCw, Trash2 } from 'lucide-react';
import { offlineDatabaseService, OfflineState, OfflineStoreKind } from '../../services/offlineDatabaseService';
import { clientCache } from '../../services/clientCache';
import { CacheItem, CacheKind, deleteCacheItems, fmtBytes, listCacheItems, storageEstimate } from '../../services/deviceStorage';
import { confirmDialog } from '../ui/ConfirmDialog';
import { toast } from '../ui/Toast';

const nf = (n: number) => n.toLocaleString('tr-TR');
const sum = (xs: CacheItem[]) => xs.reduce((a, b) => a + b.bytes, 0);
const tally = (xs: CacheItem[]) => (xs.length ? `${nf(xs.length)} · ${fmtBytes(sum(xs))}` : '—');

/** Cihazda tutulan her şey: indirilmiş PDF'ler, çevrimdışı depolar, yanıt ve uygulama önbellekleri — tek tek silinebilir. */
export const DeviceStorageSection: React.FC<{ o: OfflineState }> = ({ o }) => {
  const [items, setItems] = useState<CacheItem[] | null>(null);
  const [est, setEst] = useState<{ usage: number; quota: number } | null>(null);
  const [kvCount, setKvCount] = useState(0);
  const [busy, setBusy] = useState('');
  const [openKind, setOpenKind] = useState<CacheKind | null>('pdf');

  const refresh = useCallback(async () => {
    const [list, e, kv] = await Promise.all([listCacheItems(), storageEstimate(), clientCache.count()]);
    setItems(list);
    setEst(e);
    setKvCount(kv);
  }, []);
  useEffect(() => { void refresh(); }, [refresh]);

  const byKind = useMemo(() => {
    const g: Record<CacheKind, CacheItem[]> = { pdf: [], data: [], app: [] };
    (items || []).forEach((it) => g[it.kind].push(it));
    // Aynı PDF birden çok önbellekte durabilir: listede tek satır
    const seen = new Map<string, CacheItem>();
    g.pdf.forEach((it) => { if (!seen.has(it.url)) seen.set(it.url, it); });
    g.pdf = [...seen.values()].sort((a, b) => a.name.localeCompare(b.name, 'tr'));
    return g;
  }, [items]);

  const run = async (key: string, fn: () => Promise<void>, msg: string) => {
    setBusy(key);
    try {
      await fn();
      toast.success(msg);
    } catch {
      toast.error('Silinemedi.');
    } finally {
      setBusy('');
      void refresh();
    }
  };

  const removePdf = (it: CacheItem) =>
    run(it.url, () => deleteCacheItems((items || []).filter((x) => x.url === it.url)), `${it.name} cihazdan silindi.`);

  const clearKind = async (kind: CacheKind, label: string, warn?: string) => {
    if (!(await confirmDialog({ title: `${label} silinsin mi?`, message: warn || 'Gerektiğinde internetten yeniden indirilir.', confirmLabel: 'Sil', tone: 'danger' }))) return;
    await run(`k:${kind}`, () => deleteCacheItems((items || []).filter((x) => x.kind === kind)), `${label} silindi.`);
  };

  const s = o.stats;
  const stores: [OfflineStoreKind, string, number][] = [
    ['past', 'Çıkmış sorular', s.pastQuestionsCount],
    ['pool', 'Havuz soruları', s.poolQuestionsCount],
    ['committees', 'Kurullar', s.committeesCount],
    ['decks', 'Öğren desteleri', s.decksCount],
    ['glossary', 'Sözlük', s.glossaryCount],
    ['flashcards', 'Ezber kartları', s.flashcardsCount],
  ];

  const clearStore = async (kind: OfflineStoreKind, label: string) => {
    if (!(await confirmDialog({ title: `${label} cihazdan silinsin mi?`, message: 'Çevrimdışı kopyası silinir; internet varken uygulama sunucudan okur.', confirmLabel: 'Sil', tone: 'danger' }))) return;
    await run(`s:${kind}`, () => offlineDatabaseService.clearStore(kind), `${label} silindi.`);
  };

  const groups: [CacheKind, string, string | undefined][] = [
    ['data', 'Sunucu yanıt önbelleği', undefined],
    ['app', 'Uygulama dosyaları', 'Uygulama dosyaları silinirse internet yokken uygulama açılmayabilir; ilk açılışta yeniden indirilir.'],
  ];

  return (
    <section className="of-sec dvs" aria-label="Cihazdaki veriler">
      <div className="dvs-head">
        <h3>Cihazdaki veriler</h3>
        {est && est.usage > 0 && <span className="dvs-usage">{fmtBytes(est.usage)} kullanılıyor</span>}
        <button type="button" className="ms-btn is-ghost is-sm" onClick={() => void refresh()} aria-label="Yenile"><RefreshCw /></button>
      </div>

      <div className="dvs-group">
        <button type="button" className="dvs-row is-head" aria-expanded={openKind === 'pdf'} onClick={() => setOpenKind(openKind === 'pdf' ? null : 'pdf')}>
          <FileText aria-hidden />
          <span>İndirilmiş PDF'ler</span>
          <b>{items ? tally(byKind.pdf) : '…'}</b>
          <ChevronDown aria-hidden className="dvs-chev" />
        </button>
        {openKind === 'pdf' && (
          byKind.pdf.length ? (
            <ul className="dvs-list">
              {byKind.pdf.map((it) => (
                <li key={it.url}>
                  <span title={it.name}>{it.name}</span>
                  <small>{fmtBytes(it.bytes)}</small>
                  <button type="button" className="ms-btn is-ghost is-sm is-danger" disabled={busy === it.url} onClick={() => void removePdf(it)} aria-label={`${it.name} sil`}><Trash2 /></button>
                </li>
              ))}
              {byKind.pdf.length > 1 && (
                <li className="is-all">
                  <button type="button" className="ms-btn is-danger is-sm" disabled={!!busy} onClick={() => void clearKind('pdf', "Tüm PDF'ler")}><Trash2 /> Tümünü sil</button>
                </li>
              )}
            </ul>
          ) : <p className="dvs-empty">Cihazda kayıtlı PDF yok.</p>
        )}
      </div>

      <ul className="dvs-list is-rows">
        {stores.map(([k, label, n]) => (
          <li key={k}>
            <span>{label}</span>
            <small>{n ? `${nf(n)} kayıt` : '—'}</small>
            <button type="button" className="ms-btn is-ghost is-sm is-danger" disabled={!n || !!busy || o.isDownloading} onClick={() => void clearStore(k, label)} aria-label={`${label} sil`}><Trash2 /></button>
          </li>
        ))}
        {groups.map(([k, label, warn]) => (
          <li key={k}>
            <span>{label}</span>
            <small>{items ? tally(byKind[k]) : '…'}</small>
            <button type="button" className="ms-btn is-ghost is-sm is-danger" disabled={!byKind[k].length || !!busy} onClick={() => void clearKind(k, label, warn)} aria-label={`${label} sil`}><Trash2 /></button>
          </li>
        ))}
        <li>
          <span>Hızlı erişim önbelleği</span>
          <small>{kvCount ? `${nf(kvCount)} kayıt` : '—'}</small>
          <button
            type="button"
            className="ms-btn is-ghost is-sm is-danger"
            disabled={!kvCount || !!busy}
            onClick={async () => {
              if (!(await confirmDialog({ title: 'Hızlı erişim önbelleği silinsin mi?', message: 'Veriler sonraki açılışta sunucudan yeniden gelir.', confirmLabel: 'Sil', tone: 'danger' }))) return;
              await run('kv', () => clientCache.clearAll(), 'Önbellek silindi.');
            }}
            aria-label="Hızlı erişim önbelleğini sil"
          ><Trash2 /></button>
        </li>
      </ul>
    </section>
  );
};
