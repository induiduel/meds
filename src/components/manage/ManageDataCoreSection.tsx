import { useCallback, useEffect, useState } from 'react';
import { safeJsonFetch } from '../../services/api';

/**
 * Yönetim konsolu — MedSoru Core v2 bölümü.
 * v2 veri durumu, denetim özeti, kavram grafı ve toplu tamamlama adaylarını gösterir (salt okunur).
 */
export function ManageDataCoreSection({ notify }: { notify?: (msg: string) => void }) {
  const [stats, setStats] = useState<any>(null);
  const [audit, setAudit] = useState<any>(null);
  const [graph, setGraph] = useState<any>(null);
  const [clusters, setClusters] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

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

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <p className="text-sm opacity-70">
          Bağımsız MedSoru Core v2 hattı: kaynaktan doğrulanmış sorular, müfredat/kazanım, ders notu bağları,
          kavram grafı ve toplu tamamlama. GPU/AI kullanılmaz.
        </p>
        <button onClick={load} className="text-xs rounded border px-2 py-1">Yenile</button>
      </div>

      {loading && <div className="text-sm opacity-60">Yükleniyor…</div>}

      {stats && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {[
            ['Soru', stats.sorular], ['Cevaplı', stats.cevapli], ['Açık uçlu', stats.acik_uclu],
            ['Kazanımlı', stats.kazanimli], ['Kaynağa bağlı', stats.kaynak_bagli], ['Not dosyası', stats.notlar_dosya],
            ['Özet dosyası', stats.ozet_dosya], ['Vektör', stats.vektor?.sayi ?? 0],
          ].map(([l, v]) => (
            <div key={String(l)} className="rounded-lg border border-black/10 dark:border-white/15 p-3">
              <div className="text-xs opacity-60">{l}</div>
              <div className="text-lg font-semibold">{String(v ?? 0)}</div>
            </div>
          ))}
        </div>
      )}

      {audit?.toplam && (
        <div className="rounded-lg border border-black/10 dark:border-white/15 p-3 text-sm">
          <div className="font-medium mb-1">Eski veri denetimi ({audit.zaman})</div>
          <div className="opacity-80">
            {audit.toplam.kayit} kayıt · engelleyici {audit.toplam.blocking} · inceleme {audit.toplam.review} ·
            inceleme kuyruğu {audit.inceleme_kuyrugu}
          </div>
        </div>
      )}

      {graph && (
        <div className="rounded-lg border border-black/10 dark:border-white/15 p-3 text-sm">
          <div className="font-medium mb-1">Kavram grafı</div>
          <div className="opacity-80">{graph.dugum} düğüm · {graph.kenar} kenar</div>
        </div>
      )}

      <div className="rounded-lg border border-black/10 dark:border-white/15 p-3">
        <div className="font-medium text-sm mb-2">Toplu tamamlama adayları ({clusters.length})</div>
        <ul className="space-y-1 text-xs">
          {clusters.slice(0, 12).map((c, i) => {
            const m = c.birlesik || c;
            return (
              <li key={i} className="truncate opacity-90">
                • {String(m.stem || '').slice(0, 120)}
                <span className="opacity-50"> · {m.birlesik_parca_sayisi ?? 1} parça</span>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}
