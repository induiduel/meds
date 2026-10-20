/**
 * Yönetim › Hat panosu (/manage/hat): otomasyon/hat.json aşama defteri + meds_temp/hat/durum.json son çalışma durumu +
 * hat.log son satırları (GET /api/admin/hat). Salt okunur; çalıştırma `hat.py --calistir <id>` ile yapılır.
 * v14 (canvas HatPanosu.dc.html): sayılar → sekmeler + renk anlamı → seçimli aşama tablosu (renkli durum hücresi) →
 * satır → tam sayfa ayrıntı (takılan kapı, günlük satırları). Ders × aşama verisi uçta yok; satırlar aşamalardır.
 * Stil: hat.css (.mh-*), ortak kabuk consoleUi (ms-panel …).
 */
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { GitBranch, RefreshCw, ScrollText } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { EmptyState, Panel, Drawer, logTone, timeLabel } from './consoleUi';
import { PageActions, StatRow, Toolbar, Tabs14, DataTable, DetailNav, DetailLayout, FactList, Card14, type Col } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';
import './hat.css';

type Asama = {
  id: string; kapsam?: string; durum?: 'hazir' | 'el' | 'plan' | string; gerekir?: string[]; tetik?: string[];
  komut?: string; kapi?: string; cikti?: string[]; eksik?: string; not?: string;
};
type Defter = { surum?: number; aciklama?: string; tetikleyiciler?: Record<string, string>; asamalar?: Asama[] };
type CalismaDurumu = { son?: string; kod?: number | null; son_basari?: string };
type Yanit = { defter: Defter | null; durum: Record<string, CalismaDurumu>; log: string[] };
type Suzgec = 'hepsi' | 'hazir' | 'el' | 'plan' | 'hata';

const DURUM_AD: Record<string, { ad: string; cls: string }> = {
  hazir: { ad: 'Otomatik', cls: 'is-ok' },
  el: { ad: 'Elle', cls: 'is-warn' },
  plan: { ad: 'Planlandı', cls: '' },
};
const KAPSAM_AD: Record<string, string> = { genel: 'Genel', ders: 'Ders başına', kurul: 'Kurul başına' };
const zaman = (s?: string) => (s ? timeLabel(s, true) : '—');

export const ManageHatSection: React.FC<{ adminEmail?: string }> = ({ adminEmail }) => {
  const [veri, setVeri] = useState<Yanit | null>(null);
  const [hata, setHata] = useState('');
  const [yuk, setYuk] = useState(false);
  const [suzgec, setSuzgec] = useState<Suzgec>('hepsi');

  const yukle = useCallback(async () => {
    setYuk(true); setHata('');
    const r = await safeJsonFetch<Yanit>('/api/admin/hat', { headers: { 'x-admin-email': adminEmail || '' } });
    setYuk(false);
    if (r.ok && r.data) setVeri(r.data); else setHata(r.error || `Hat durumu alınamadı (${r.status}).`);
  }, [adminEmail]);
  useEffect(() => { void yukle(); }, [yukle]);

  const asamalar = veri?.defter?.asamalar || [];
  const durum = veri?.durum || {};
  const hatali = (a: Asama) => { const d = durum[a.id]; return !!d && d.kod != null && d.kod !== 0; };
  const sayilar = useMemo(() => ({
    hepsi: asamalar.length,
    hazir: asamalar.filter((a) => a.durum === 'hazir').length,
    el: asamalar.filter((a) => a.durum === 'el').length,
    plan: asamalar.filter((a) => a.durum === 'plan').length,
    hata: asamalar.filter(hatali).length,
  }), [asamalar, durum]); // eslint-disable-line react-hooks/exhaustive-deps
  const liste = asamalar.filter((a) => suzgec === 'hepsi' || (suzgec === 'hata' ? hatali(a) : a.durum === suzgec));

  const [acik, setAcik] = useState<string | null>(null);
  const secim = useSelection<string>();
  const cur = asamalar.find((a) => a.id === acik) || null;
  const durumOf = (a: Asama): { k: 'gecti' | 'takildi' | 'bekliyor' | 'el'; ad: string } => {
    const d = durum[a.id];
    if (d && d.kod != null && d.kod !== 0) return { k: 'takildi', ad: `Kapıda takıldı (kod ${d.kod})` };
    if (d && d.kod === 0) return { k: 'gecti', ad: 'Geçti' };
    if (a.durum === 'el') return { k: 'el', ad: 'Elle çalışır' };
    return { k: 'bekliyor', ad: 'Bekliyor' };
  };
  const secili = asamalar.filter((a) => secim.has(a.id));
  const komutKopyala = () => {
    const metin = secili.map((a) => `python3 scripts/hat.py --calistir ${a.id}`).join('\n');
    void navigator.clipboard?.writeText(metin).catch(() => undefined);
  };
  const curLog = cur ? (veri?.log || []).filter((l) => l.includes(cur.id)) : [];

  const kolonlar: Col<Asama>[] = [
    { key: 'id', label: 'Aşama', main: true, render: (a) => <code className="mh-id">{a.id}</code> },
    { key: 'kapsam', label: 'Kapsam', muted: true, render: (a) => KAPSAM_AD[a.kapsam || ''] || a.kapsam || '—' },
    { key: 'tur', label: 'Tür', render: (a) => { const da = DURUM_AD[a.durum || ''] || { ad: a.durum || '?', cls: '' }; return <span className={`mh-rozet ${da.cls}`}>{da.ad}</span>; } },
    { key: 'hucre', label: 'Son çalışma', render: (a) => { const x = durumOf(a); return <span className="mh-hucre-k"><span className={`mh-hucre is-${x.k}`} title={x.ad} aria-hidden="true" /><span>{x.ad}</span></span>; } },
    { key: 'kapi', label: 'Kapı', mono: true, render: (a) => a.kapi || '—' },
    { key: 'son', label: 'Son başarı', muted: true, render: (a) => zaman(durum[a.id]?.son_basari) },
  ];

  return (
    <div className="mh">
      <PageActions note="Kayıt defteri: otomasyon/hat.json. Otomatik aşamalar gece ve Drive tetikleyicisiyle çalışır; elle olanlar hatta bağlı değildir.">
        <button type="button" className="m14-btn" onClick={() => void yukle()} disabled={yuk}>
          <RefreshCw className={yuk ? 'animate-spin' : ''} aria-hidden /> Yenile
        </button>
      </PageActions>
      {hata && <p className="mh-hata" role="alert">{hata}</p>}
      {!veri && !hata && <p className="mh-bilgi">Yükleniyor…</p>}
      {veri && !veri.defter && <EmptyState icon={GitBranch} title="Kayıt defteri okunamadı">otomasyon/hat.json bulunamadı ya da bozuk.</EmptyState>}
      {asamalar.length > 0 && (
        <>
          <StatRow
            stats={[
              { label: 'Aşama', value: sayilar.hepsi, onClick: () => setSuzgec('hepsi') },
              { label: 'Otomatik', value: sayilar.hazir, tone: 'ok', onClick: () => setSuzgec('hazir') },
              { label: 'Elle', value: sayilar.el, tone: 'warn', onClick: () => setSuzgec('el') },
              { label: 'Kapıda takılan', value: sayilar.hata, tone: sayilar.hata ? 'bad' : undefined, onClick: () => setSuzgec('hata') },
            ]}
          />
          <Toolbar>
            <Tabs14
              value={suzgec}
              onChange={setSuzgec}
              label="Aşama durumu"
              options={[
                { id: 'hepsi', label: 'Tümü', n: sayilar.hepsi },
                { id: 'hazir', label: 'Otomatik', n: sayilar.hazir },
                { id: 'el', label: 'Elle', n: sayilar.el },
                { id: 'plan', label: 'Planlandı', n: sayilar.plan },
                { id: 'hata', label: 'Son çalışması hatalı', n: sayilar.hata },
              ]}
            />
            <span className="mh-lejant" aria-label="Renk anlamları">
              <span><i className="mh-hucre is-gecti" />Geçti</span>
              <span><i className="mh-hucre is-takildi" />Kapıda takıldı</span>
              <span><i className="mh-hucre is-el" />Elle</span>
              <span><i className="mh-hucre is-bekliyor" />Bekliyor</span>
            </span>
          </Toolbar>
          <BulkBar
            count={secim.count}
            noun="aşama"
            onClear={secim.clear}
            actions={[{ label: 'Çalıştırma komutlarını kopyala', kind: 'main', run: komutKopyala }]}
          />
          <DataTable rows={liste} cols={kolonlar} rowKey={(a) => a.id} onOpen={(a) => setAcik(a.id)} selection={secim} activeKey={acik} empty="Bu süzgeçte aşama yok." />
        </>
      )}

      <Panel title="Hat günlüğü" icon={ScrollText} count={veri?.log.length ?? 0} desc="meds_temp/hat/hat.log son 60 satır, en yenisi altta.">
        {veri && veri.log.length === 0 ? (
          <EmptyState icon={ScrollText} title="Günlük boş">Hat henüz çalışmadı ya da günlük dosyası yok.</EmptyState>
        ) : (
          <pre className="ms-term mh-log">
            {(veri?.log || []).map((l, i) => <div key={i} className={logTone(l)}>{l}</div>)}
          </pre>
        )}
      </Panel>

      <Drawer
        open={!!cur}
        onClose={() => setAcik(null)}
        title={cur ? cur.id : 'Aşama'}
        wide
        head={<DetailNav list={liste} current={cur} same={(a, b) => a.id === b.id} onGo={(a) => setAcik(a.id)} />}
        foot={
          cur && (
            <button type="button" className="m14-btn" onClick={() => void navigator.clipboard?.writeText(`python3 scripts/hat.py --calistir ${cur.id}`).catch(() => undefined)}>
              Çalıştırma komutunu kopyala
            </button>
          )
        }
      >
        {cur && (() => {
          const d = durum[cur.id];
          const x = durumOf(cur);
          return (
            <DetailLayout
              main={
                <>
                  {x.k === 'takildi' && (
                    <div className="mh-takilan" role="alert">
                      <b>Takılan kapı</b>
                      <span>{cur.kapi ? <code>{cur.kapi}</code> : 'Kapı tanımlı değil'} · son çalışma kod {d?.kod}</span>
                    </div>
                  )}
                  {cur.komut && <p className="mh-komut"><code>{cur.komut}</code></p>}
                  {cur.eksik && <p className="mh-eksik"><b>Eksik:</b> {cur.eksik}</p>}
                  {cur.not && <p className="mh-not">{cur.not}</p>}
                  <Card14 title="Bu aşamanın günlük satırları">
                    {curLog.length === 0 ? <p className="mh-bilgi">Son 60 satırda bu aşamaya ait kayıt yok.</p> : (
                      <pre className="ms-term mh-log">{curLog.map((l, i) => <div key={i} className={logTone(l)}>{l}</div>)}</pre>
                    )}
                  </Card14>
                </>
              }
              side={
                <FactList
                  items={[
                    { k: 'Durum', v: x.ad },
                    { k: 'Tür', v: (DURUM_AD[cur.durum || ''] || { ad: cur.durum || '?' }).ad },
                    { k: 'Kapsam', v: KAPSAM_AD[cur.kapsam || ''] || cur.kapsam },
                    { k: 'Bağımlı', v: cur.gerekir?.length ? cur.gerekir.join(', ') : '—' },
                    { k: 'Tetik', v: cur.tetik?.length ? cur.tetik.join(', ') : '—' },
                    { k: 'Kapı', v: cur.kapi ? <code>{cur.kapi}</code> : '—' },
                    { k: 'Çıktı', v: cur.cikti?.length ? cur.cikti.join(', ') : '—' },
                    { k: 'Son çalışma', v: zaman(d?.son) },
                    { k: 'Son başarı', v: zaman(d?.son_basari) },
                  ]}
                />
              }
            />
          );
        })()}
      </Drawer>
    </div>
  );
};
