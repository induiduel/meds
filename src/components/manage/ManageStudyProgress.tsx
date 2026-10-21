import React, { useEffect, useMemo, useState } from 'react';
import { BookOpenCheck, ChevronDown, ChevronRight, ExternalLink, RefreshCw, Search } from 'lucide-react';
import { fmtDuration, loadStudyMatrix, relTime, type StudyMatrixPerson } from '../../services/peopleService';
import { EmptyState } from './consoleUi';
import { MODUL, adlariYukle, type Ad } from './PersonStudy';
import '../../styles/manage-people.css';

/**
 * Ders ilerlemesi: tüm öğrencilerin konu bazlı çalışma takibi (profil kv `medsoru_calisma_takip_v1`) tek ekranda.
 * "Dersler" görünümü konu başına kaç kişinin başladığını/bitirdiğini ve kimin nerede olduğunu, "Öğrenciler" görünümü
 * kişi başına bitirilen konu, süre ve konu listesini gösterir. Profil eşitlendikçe (`user_data_changed`) kendini tazeler.
 */
type Konu = StudyMatrixPerson['konular'][string];
const DURUM: Record<string, string> = { bitti: 'Bitti', tekrar: 'Tekrarda', acik: 'Devam' };
const modulOf = (id: string) => (id.includes(':') ? id.slice(0, id.indexOf(':')) : 'diger');
const kisiLink = (key: string) => `/manage/kisiler/${encodeURIComponent(key)}?sekme=calisma`;
const yuzde = (sn: number, beklenen?: number) => (beklenen ? Math.min(100, Math.round((sn / beklenen) * 100)) : null);

const Durum: React.FC<{ k: Konu; a?: Ad }> = ({ k, a }) => {
  const d = k.durum || 'acik';
  const p = yuzde(k.sn, a?.beklenen);
  return (
    <span className={`sp-durum is-${d}`}>
      {DURUM[d] || d}
      {d !== 'bitti' && p !== null ? ` · %${p}` : ''}
    </span>
  );
};

export const ManageStudyProgress: React.FC<{ notify: (m: string) => void }> = ({ notify }) => {
  const [veri, setVeri] = useState<{ at: string; kisiler: StudyMatrixPerson[] } | null>(null);
  const [adlar, setAdlar] = useState<Map<string, Ad> | null>(null);
  const [gorunum, setGorunum] = useState<'dersler' | 'ogrenciler'>('dersler');
  const [mod, setMod] = useState('hepsi');
  const [q, setQ] = useState('');
  const [acik, setAcik] = useState<string | null>(null);
  const [yukleniyor, setYukleniyor] = useState(false);
  const [misafir, setMisafir] = useState(false);
  const gorunen = useMemo(() => (veri?.kisiler || []).filter((p) => misafir || p.kind !== 'guest'), [veri, misafir]);

  const yukle = async (sessiz = false) => {
    if (!sessiz) setYukleniyor(true);
    try {
      setVeri(await loadStudyMatrix());
    } catch (e: any) {
      if (!sessiz) notify(e?.message || 'Ders ilerlemesi alınamadı.');
    } finally {
      setYukleniyor(false);
    }
  };

  useEffect(() => {
    let on = true;
    void yukle();
    void adlariYukle().then((m) => on && setAdlar(m));
    // Öğrenci profili eşitlendikçe sessizce tazele (birkaç saniyede bir en fazla)
    let t: number | undefined;
    const kapat: (() => void)[] = [];
    void import('../../services/realtimeEvents').then(({ realtimeEventService }) => {
      if (!on) return;
      const bump = () => {
        window.clearTimeout(t);
        t = window.setTimeout(() => void yukle(true), 4000);
      };
      kapat.push(realtimeEventService.on('user_data_changed', bump), realtimeEventService.on('people_changed', bump));
    });
    return () => {
      on = false;
      window.clearTimeout(t);
      kapat.forEach((f) => typeof f === 'function' && f());
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const kisiler = useMemo(() => {
    const t = q.trim().toLocaleLowerCase('tr-TR');
    return gorunen
      .map((p) => {
        const konular = Object.entries(p.konular).filter(([id]) => mod === 'hepsi' || modulOf(id) === mod);
        const bitti = konular.filter(([, k]) => k.durum === 'bitti').length;
        const sn = konular.reduce((a, [, k]) => a + k.sn, 0);
        const soru = konular.reduce((a, [, k]) => a + k.soru, 0);
        return { p, konular, bitti, sn, soru };
      })
      .filter((x) => x.konular.length && (!t || `${x.p.ad} ${x.p.email || ''}`.toLocaleLowerCase('tr-TR').includes(t)))
      .sort((a, b) => b.bitti - a.bitti || b.sn - a.sn);
  }, [gorunen, mod, q]);

  /** Ders (katalogdaki ders/branş adı) → konu → kişiler */
  const dersler = useMemo(() => {
    const t = q.trim().toLocaleLowerCase('tr-TR');
    const konuMap = new Map<string, { id: string; ad: string; ders: string; beklenen: number; kayit: { p: StudyMatrixPerson; k: Konu }[] }>();
    for (const p of gorunen)
      for (const [id, k] of Object.entries(p.konular)) {
        if (mod !== 'hepsi' && modulOf(id) !== mod) continue;
        let r = konuMap.get(id);
        if (!r) {
          const a = adlar?.get(id);
          const m = modulOf(id);
          r = { id, ad: a?.ad || id.slice(id.indexOf(':') + 1), ders: `${MODUL[m] || m} · ${a?.ders || 'Katalogda yok'}`, beklenen: a?.beklenen || 0, kayit: [] };
          konuMap.set(id, r);
        }
        r.kayit.push({ p, k });
      }
    const grup = new Map<string, typeof konuMap extends Map<any, infer V> ? V[] : never>();
    for (const r of konuMap.values()) {
      if (t && !`${r.ad} ${r.ders}`.toLocaleLowerCase('tr-TR').includes(t)) continue;
      r.kayit.sort((a, b) => (a.k.durum === 'bitti' ? 0 : 1) - (b.k.durum === 'bitti' ? 0 : 1) || b.k.sn - a.k.sn);
      grup.set(r.ders, [...(grup.get(r.ders) || []), r]);
    }
    return [...grup.entries()]
      .map(([ders, konular]) => ({ ders, konular: konular.sort((a, b) => b.kayit.length - a.kayit.length || a.ad.localeCompare(b.ad, 'tr')) }))
      .sort((a, b) => a.ders.localeCompare(b.ders, 'tr'));
  }, [gorunen, adlar, mod, q]);

  if (veri && !veri.kisiler.length)
    return (
      <EmptyState icon={BookOpenCheck} title="Henüz çalışma kaydı yok">
        Öğrenciler sesli ders, etkileşimli ders, soru çözücü ya da En önemliler'de çalıştıkça ve profilleri eşitlendikçe burada görünür.
      </EmptyState>
    );

  const toplamBitti = kisiler.reduce((a, x) => a + x.bitti, 0);
  const toplamSn = kisiler.reduce((a, x) => a + x.sn, 0);

  return (
    <div className="pp-ov ps-study sp-root">
      <div className="pp-tiles">
        <div className="pp-tile"><span className="pp-tile-l">Çalışan öğrenci</span><span className="pp-tile-v">{kisiler.length}</span><span className="pp-tile-s">konu kaydı olan</span></div>
        <div className="pp-tile"><span className="pp-tile-l">Bitirilen konu</span><span className="pp-tile-v">{toplamBitti}</span><span className="pp-tile-s">toplam</span></div>
        <div className="pp-tile"><span className="pp-tile-l">Toplam çalışma</span><span className="pp-tile-v">{fmtDuration(toplamSn)}</span><span className="pp-tile-s">konu takibinde</span></div>
        <div className="pp-tile"><span className="pp-tile-l">Güncellendi</span><span className="pp-tile-v ps-small">{veri ? relTime(veri.at) : '—'}</span><span className="pp-tile-s">profil eşitlendikçe tazelenir</span></div>
      </div>

      <div className="pp-card">
        <div className="ps-bar">
          <div className="ps-seg" role="tablist" aria-label="Görünüm">
            {(['dersler', 'ogrenciler'] as const).map((g) => (
              <button key={g} type="button" role="tab" aria-selected={gorunum === g} className={`pp-chip ${gorunum === g ? 'is-on' : ''}`} onClick={() => { setGorunum(g); setAcik(null); }}>
                {g === 'dersler' ? 'Dersler' : 'Öğrenciler'}
              </button>
            ))}
          </div>
          <label className="pp-search ps-q">
            <Search aria-hidden="true" />
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder={gorunum === 'dersler' ? 'Ders ya da konu ara' : 'Öğrenci ara'} aria-label="Ara" />
          </label>
          <select className="ps-sel" value={mod} onChange={(e) => setMod(e.target.value)} aria-label="Modül">
            <option value="hepsi">Tüm modüller</option>
            {Object.entries(MODUL).filter(([m]) => m !== 'diger').map(([m, l]) => <option key={m} value={m}>{l}</option>)}
          </select>
          <label className="pp-muted"><input type="checkbox" checked={misafir} onChange={(e) => setMisafir(e.target.checked)} /> Girişsiz cihazlar ({(veri?.kisiler || []).filter((p) => p.kind === 'guest').length})</label>
          <button className="ms-btn is-sm" onClick={() => void yukle()} disabled={yukleniyor}>
            <RefreshCw aria-hidden="true" /> Yenile
          </button>
        </div>

        {!veri ? (
          <p className="pp-muted">Yükleniyor…</p>
        ) : gorunum === 'dersler' ? (
          dersler.length ? (
            dersler.map((g) => (
              <section key={g.ders} className="sp-grup">
                <h3 className="sp-baslik">{g.ders}</h3>
                <div className="pp-table-wrap">
                  <table className="pp-table ps-table">
                    <thead><tr><th>Konu</th><th className="n">Başlayan</th><th className="n">Bitiren</th><th className="n">Ort. süre</th><th className="n">Soru</th></tr></thead>
                    <tbody>
                      {g.konular.map((r) => {
                        const bit = r.kayit.filter((x) => x.k.durum === 'bitti').length;
                        const ort = r.kayit.reduce((a, x) => a + x.k.sn, 0) / r.kayit.length;
                        const ac = acik === r.id;
                        return (
                          <React.Fragment key={r.id}>
                            <tr className="sp-satir" onClick={() => setAcik(ac ? null : r.id)} aria-expanded={ac}>
                              <td className="ps-konu">{ac ? <ChevronDown aria-hidden="true" /> : <ChevronRight aria-hidden="true" />} {r.ad}</td>
                              <td className="n">{r.kayit.length}</td>
                              <td className="n">{bit} <small className="ps-pct">%{Math.round((bit / r.kayit.length) * 100)}</small></td>
                              <td className="n">{fmtDuration(ort)}{r.beklenen ? <small className="ps-pct"> / {fmtDuration(r.beklenen)}</small> : null}</td>
                              <td className="n">{r.kayit.reduce((a, x) => a + x.k.soru, 0)}</td>
                            </tr>
                            {ac && (
                              <tr className="sp-ic"><td colSpan={5}>
                                <ul className="sp-kisiler">
                                  {r.kayit.map(({ p, k }) => (
                                    <li key={p.key}>
                                      <a href={kisiLink(p.key)}>{p.ad}</a>
                                      <Durum k={k} a={adlar?.get(r.id)} />
                                      <span className="pp-muted">{fmtDuration(k.sn)}{k.soru ? ` · ${k.soru} soru` : ''} · {relTime(k.bittiAt || k.sonAt)}</span>
                                    </li>
                                  ))}
                                </ul>
                              </td></tr>
                            )}
                          </React.Fragment>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </section>
            ))
          ) : (
            <p className="pp-muted">Süzgece uyan konu yok.</p>
          )
        ) : kisiler.length ? (
          <div className="pp-table-wrap">
            <table className="pp-table ps-table">
              <thead><tr><th>Öğrenci</th><th className="n">Bitti</th><th className="n">Konu</th><th className="n">Süre</th><th className="n">7 gün</th><th className="n">Soru</th><th>Son</th></tr></thead>
              <tbody>
                {kisiler.map(({ p, konular, bitti, sn, soru }) => {
                  const ac = acik === p.key;
                  return (
                    <React.Fragment key={p.key}>
                      <tr className="sp-satir" onClick={() => setAcik(ac ? null : p.key)} aria-expanded={ac}>
                        <td className="ps-konu">
                          {ac ? <ChevronDown aria-hidden="true" /> : <ChevronRight aria-hidden="true" />} {p.ad}
                          {p.kind === 'guest' && <small className="ps-pct"> misafir</small>}
                        </td>
                        <td className="n">{bitti}</td>
                        <td className="n">{konular.length}</td>
                        <td className="n">{fmtDuration(sn)}</td>
                        <td className="n">{fmtDuration(p.ozet.haftaSn)}</td>
                        <td className="n">{soru}</td>
                        <td>{relTime(p.ozet.son)}</td>
                      </tr>
                      {ac && (
                        <tr className="sp-ic"><td colSpan={7}>
                          <ul className="sp-kisiler">
                            {konular
                              .sort(([, a], [, b]) => String(b.sonAt || '').localeCompare(String(a.sonAt || '')))
                              .map(([id, k]) => {
                                const a = adlar?.get(id);
                                return (
                                  <li key={id}>
                                    <span>{a?.ad || id}<small className="pp-muted"> · {MODUL[modulOf(id)] || modulOf(id)}{a?.ders ? ` · ${a.ders}` : ''}</small></span>
                                    <Durum k={k} a={a} />
                                    <span className="pp-muted">{fmtDuration(k.sn)}{k.soru ? ` · ${k.soru} soru` : ''} · {relTime(k.bittiAt || k.sonAt)}</span>
                                  </li>
                                );
                              })}
                          </ul>
                          <a className="ms-btn is-sm" href={kisiLink(p.key)}><ExternalLink aria-hidden="true" /> Kişinin çalışma sekmesi (düzenle)</a>
                        </td></tr>
                      )}
                    </React.Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="pp-muted">Süzgece uyan öğrenci yok.</p>
        )}
      </div>
    </div>
  );
};
