/**
 * Yönetim › Hat panosu (/manage/hat): otomasyon/hat.json aşama defteri + meds_temp/hat/durum.json son çalışma durumu +
 * hat.log son satırları (GET /api/admin/hat). Salt okunur; çalıştırma `hat.py --calistir <id>` ile yapılır.
 * Stil: hat.css (.mh-*), ortak kabuk consoleUi (ms-panel …).
 */
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { GitBranch, RefreshCw, ScrollText } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { ChipBar, EmptyState, Panel, logTone, timeLabel } from './consoleUi';
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

  const yenile = (
    <button type="button" className="ms-btn" onClick={() => void yukle()} disabled={yuk}>
      <RefreshCw className={yuk ? 'animate-spin' : ''} aria-hidden /> Yenile
    </button>
  );

  return (
    <div className="mh">
      <Panel
        title="Hat aşamaları" icon={GitBranch} count={asamalar.length} tools={yenile}
        desc={veri?.defter?.aciklama ? 'Kayıt defteri: otomasyon/hat.json. Otomatik aşamalar gece ve Drive tetikleyicisiyle çalışır; elle olanlar hatta bağlı değildir.' : undefined}
      >
        {hata && <p className="mh-hata" role="alert">{hata}</p>}
        {!veri && !hata && <p className="mh-bilgi">Yükleniyor…</p>}
        {veri && !veri.defter && <EmptyState icon={GitBranch} title="Kayıt defteri okunamadı">otomasyon/hat.json bulunamadı ya da bozuk.</EmptyState>}
        {asamalar.length > 0 && (
          <>
            <ChipBar
              value={suzgec}
              onChange={setSuzgec}
              label="Aşama durumu"
              wrap
              options={[
                { id: 'hepsi', label: 'Tümü', n: sayilar.hepsi },
                { id: 'hazir', label: 'Otomatik', n: sayilar.hazir },
                { id: 'el', label: 'Elle', n: sayilar.el },
                { id: 'plan', label: 'Planlandı', n: sayilar.plan },
                { id: 'hata', label: 'Son çalışması hatalı', n: sayilar.hata },
              ]}
            />
            <ul className="mh-liste">
              {liste.map((a) => {
                const d = durum[a.id];
                const da = DURUM_AD[a.durum || ''] || { ad: a.durum || '?', cls: '' };
                const kodCls = d?.kod == null ? '' : d.kod === 0 ? 'is-ok' : 'is-bad';
                return (
                  <li key={a.id} className="mh-asama">
                    <div className="mh-ust">
                      <code className="mh-id">{a.id}</code>
                      <span className={`mh-rozet ${da.cls}`}>{da.ad}</span>
                      {a.kapsam && <span className="mh-rozet is-soluk">{KAPSAM_AD[a.kapsam] || a.kapsam}</span>}
                      {d && (
                        <span className={`mh-kod ${kodCls}`} title="Son çalışmanın çıkış kodu">
                          {d.kod == null ? 'çalışmadı' : d.kod === 0 ? 'son çalışma başarılı' : `son çalışma hata (kod ${d.kod})`}
                        </span>
                      )}
                    </div>
                    {a.komut && <p className="mh-komut"><code>{a.komut}</code></p>}
                    <dl className="mh-meta">
                      {a.gerekir && a.gerekir.length > 0 && <><dt>Bağımlı</dt><dd>{a.gerekir.join(', ')}</dd></>}
                      {a.tetik && a.tetik.length > 0 && <><dt>Tetik</dt><dd>{a.tetik.join(', ')}</dd></>}
                      {a.kapi && <><dt>Kapı</dt><dd><code>{a.kapi}</code></dd></>}
                      {d?.son && <><dt>Son çalışma</dt><dd>{zaman(d.son)}</dd></>}
                      <dt>Son başarı</dt><dd>{zaman(d?.son_basari)}</dd>
                    </dl>
                    {a.eksik && <p className="mh-eksik"><b>Eksik:</b> {a.eksik}</p>}
                    {a.not && <p className="mh-not">{a.not}</p>}
                  </li>
                );
              })}
              {liste.length === 0 && <li className="mh-bilgi">Bu süzgeçte aşama yok.</li>}
            </ul>
          </>
        )}
      </Panel>

      <Panel title="Hat günlüğü" icon={ScrollText} count={veri?.log.length ?? 0} desc="meds_temp/hat/hat.log son 60 satır, en yenisi altta.">
        {veri && veri.log.length === 0 ? (
          <EmptyState icon={ScrollText} title="Günlük boş">Hat henüz çalışmadı ya da günlük dosyası yok.</EmptyState>
        ) : (
          <pre className="ms-term mh-log">
            {(veri?.log || []).map((l, i) => <div key={i} className={logTone(l)}>{l}</div>)}
          </pre>
        )}
      </Panel>
    </div>
  );
};
