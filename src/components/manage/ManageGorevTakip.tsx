import React, { useEffect, useMemo, useState } from 'react';
import { RefreshCw, Search } from 'lucide-react';
import { fmtDuration, loadGorevTakip, type GorevKisi } from '../../services/peopleService';
import { EmptyState } from './consoleUi';
import '../../styles/manage-people.css';

/**
 * Giriş ve görevler: ardışık giriş serisi + günlük/haftalık görevler (çalışma süresi, soru çözme süresi).
 * Hedefler bu tarayıcıda saklanır (yalnız yönetici görünümü); veri profil eşitlemesinden gelir.
 */
type Hedef = { gunCalisma: number; haftaCalisma: number; gunSoru: number; haftaSoru: number };
const VARSAYILAN: Hedef = { gunCalisma: 60, haftaCalisma: 420, gunSoru: 20, haftaSoru: 140 };
const KEY = 'medsoru_gorev_hedef_v1';
const hedefOku = (): Hedef => {
  try {
    return { ...VARSAYILAN, ...JSON.parse(localStorage.getItem(KEY) || '{}') };
  } catch {
    return VARSAYILAN;
  }
};
const dk = (sn: number) => Math.round(sn / 60);

export const ManageGorevTakip: React.FC<{ notify: (m: string) => void }> = ({ notify }) => {
  const [veri, setVeri] = useState<{ bugun: string; kisiler: GorevKisi[] } | null>(null);
  const [h, setH] = useState<Hedef>(hedefOku);
  const [q, setQ] = useState('');
  const [sirala, setSirala] = useState<'seri' | 'gorev'>('seri');
  const [yuk, setYuk] = useState(false);

  const yukle = async (sessiz = false) => {
    if (!sessiz) setYuk(true);
    try {
      setVeri(await loadGorevTakip());
    } catch (e: any) {
      if (!sessiz) notify(e?.message || 'Görev verisi alınamadı.');
    } finally {
      setYuk(false);
    }
  };
  useEffect(() => {
    void yukle();
    let t: number | undefined;
    const kapat: (() => void)[] = [];
    let on = true;
    void import('../../services/realtimeEvents').then(({ realtimeEventService }) => {
      if (!on) return;
      const bump = () => {
        window.clearTimeout(t);
        t = window.setTimeout(() => void yukle(true), 4000);
      };
      kapat.push(realtimeEventService.on('user_data_changed', bump));
    });
    return () => {
      on = false;
      window.clearTimeout(t);
      kapat.forEach((f) => typeof f === 'function' && f());
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const hedefDegis = (k: keyof Hedef, v: number) => {
    const n = { ...h, [k]: Math.max(1, v || 1) };
    setH(n);
    try {
      localStorage.setItem(KEY, JSON.stringify(n));
    } catch { /* yok say */ }
  };

  const satirlar = useMemo(() => {
    const t = q.trim().toLocaleLowerCase('tr-TR');
    return (veri?.kisiler || [])
      .filter((p) => p.kind !== 'guest')
      .filter((p) => !t || `${p.ad} ${p.email || ''}`.toLocaleLowerCase('tr-TR').includes(t))
      .map((p) => {
        const bugun = p.gun[p.gun.length - 1];
        const hafta = p.gun.slice(-7);
        const hc = hafta.reduce((a, g) => a + g.calisma, 0);
        const hs = hafta.reduce((a, g) => a + g.soru, 0);
        const gorevler = [
          dk(bugun.calisma) >= h.gunCalisma, dk(bugun.soru) >= h.gunSoru,
          dk(hc) >= h.haftaCalisma, dk(hs) >= h.haftaSoru,
        ];
        return { p, bugun, hc, hs, tamam: gorevler.filter(Boolean).length, gorevler };
      })
      .sort((a, b) => (sirala === 'seri' ? b.p.seri - a.p.seri : b.tamam - a.tamam || b.p.seri - a.p.seri));
  }, [veri, q, h, sirala]);

  const hucre = (deger: number, hedef: number) => (
    <td style={{ color: dk(deger) >= hedef ? 'var(--color-ok, #1c8a4d)' : undefined, fontVariantNumeric: 'tabular-nums' }}>
      {fmtDuration(deger)} <span style={{ opacity: 0.6 }}>/ {hedef} dk</span>
    </td>
  );

  return (
    <div style={{ display: 'grid', gap: 12, minWidth: 0 }}>
      <div className="pp-tools">
        <label style={{ position: 'relative', flex: 1, minWidth: 0 }}>
          <Search size={14} style={{ position: 'absolute', left: 10, top: 11, opacity: 0.6 }} />
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Kişi ara" style={{ width: '100%', padding: '8px 10px 8px 30px' }} />
        </label>
        <select value={sirala} onChange={(e) => setSirala(e.target.value as 'seri' | 'gorev')} aria-label="Sıralama">
          <option value="seri">Seriye göre</option>
          <option value="gorev">Tamamlanan göreve göre</option>
        </select>
        <button type="button" className="m14-btn" onClick={() => void yukle()} disabled={yuk} aria-label="Yenile"><RefreshCw size={14} /></button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: 8 }}>
        {([['gunCalisma', 'Günlük çalışma (dk)'], ['haftaCalisma', 'Haftalık çalışma (dk)'], ['gunSoru', 'Günlük soru çözme (dk)'], ['haftaSoru', 'Haftalık soru çözme (dk)']] as [keyof Hedef, string][]).map(([k, l]) => (
          <label key={k} style={{ display: 'grid', gap: 2, fontSize: 12 }}>
            {l}
            <input type="number" min={1} value={h[k]} onChange={(e) => hedefDegis(k, Number(e.target.value))} style={{ padding: '6px 8px' }} />
          </label>
        ))}
      </div>

      {!veri ? <EmptyState title="Yükleniyor…" /> : !satirlar.length ? <EmptyState title="Kayıt yok" /> : (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
            <thead>
              <tr style={{ textAlign: 'left' }}>
                <th>Kişi</th><th>Seri</th><th>En uzun</th><th>Son 14 gün</th>
                <th>Bugün çalışma</th><th>Bugün soru</th><th>Hafta çalışma</th><th>Hafta soru</th><th>Görev</th>
              </tr>
            </thead>
            <tbody>
              {satirlar.map(({ p, bugun, hc, hs, tamam }) => (
                <tr key={p.key} style={{ borderTop: '1px solid var(--color-line)' }}>
                  <td>{p.ad || p.email || p.key}</td>
                  <td style={{ fontWeight: 700 }}>{p.seri} gün</td>
                  <td>{p.enUzun} gün</td>
                  <td>
                    <span style={{ display: 'inline-flex', gap: 2 }} title={p.gun.map((g) => `${g.d}${g.giris ? ' ✓' : ''}`).join('\n')}>
                      {p.gun.map((g) => (
                        <i key={g.d} style={{ width: 8, height: 14, borderRadius: 2, background: g.giris ? '#1c8a4d' : 'rgba(127,127,127,.25)' }} />
                      ))}
                    </span>
                  </td>
                  {hucre(bugun.calisma, h.gunCalisma)}
                  {hucre(bugun.soru, h.gunSoru)}
                  {hucre(hc, h.haftaCalisma)}
                  {hucre(hs, h.haftaSoru)}
                  <td>{tamam}/4</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
