import React, { useEffect, useMemo, useState } from 'react';
import { BookOpenCheck, RotateCcw, Save, Search, ExternalLink, CheckCircle2, Circle, Repeat } from 'lucide-react';
import {
  editPersonStudy, fmtDuration, relTime, siteLink,
  type PersonDetail, type StudyEditOp, type StudyModule, type StudyTopic,
} from '../../services/peopleService';
import { EmptyState, ConfirmButton } from './consoleUi';

/**
 * Kişiler › Çalışma: öğrencinin konu bazlı çalışma takibi (calismaTakip.ts → profil kv `medsoru_calisma_takip_v1`),
 * gün × modül süreleri, sayfa ziyaretleri ve kaldığı yerler. Yönetici konu durumunu (bitti/açık/tekrar), süreyi ve
 * soru sayısını düzeltebilir ya da konuyu sıfırlayabilir; kayıt `adm` damgasıyla öğrencinin cihazlarına iner.
 * Konu adları sitenin kendi kataloglarından (Bitirdiklerim ile aynı kaynak) tembel çözülür.
 */
export const MODUL: Record<string, string> = { sesli: 'Sesli ders', ogren: 'Etkileşimli ders', cozucu: 'Soru çözücü', onem: 'En önemliler', diger: 'Diğer' };
const DURUM: Record<string, string> = { bitti: 'Bitti', tekrar: 'Tekrarda', acik: 'Açık' };
export type Ad = { ad: string; ders: string; beklenen: number };

/** Konu kimliği → okunur ad (MODUL_YUKLE kataloglarından, panel oturumu boyunca bir kez) */
let adOnbellek: Promise<Map<string, Ad>> | null = null;
export const adlariYukle = () => {
  if (!adOnbellek)
    adOnbellek = import('../takip/bitirdiklerimVeri')
      .then(async ({ MODUL_YUKLE }) => {
        const m = new Map<string, Ad>();
        await Promise.all(
          (Object.keys(MODUL_YUKLE) as StudyModule[]).map(async (mod) => {
            try {
              for (const d of await MODUL_YUKLE[mod]()) for (const k of d.konular) m.set(`${mod}:${k.id}`, { ad: k.ad, ders: d.ad, beklenen: k.beklenen });
            } catch {
              /* katalog yüklenemezse kimlik gösterilir */
            }
          }),
        );
        return m;
      })
      .catch(() => new Map<string, Ad>());
  return adOnbellek;
};

/** Konunun sitedeki adresi (öğrencinin gördüğü sayfa) */
const konuLink = (t: StudyTopic) => {
  if (t.modul === 'sesli') return `/canliders/${encodeURIComponent(t.konu)}`;
  if (t.modul === 'ogren') return `/ogren/${encodeURIComponent(t.konu)}`;
  if (t.modul === 'cozucu' || t.modul === 'onem') {
    const [brans, ders] = t.konu.split('/');
    const sp = new URLSearchParams({ brans: brans || '' });
    if (ders) sp.set('ders', ders);
    return `${t.modul === 'onem' ? '/en-onemliler' : '/soru-cozucu'}?${sp}`;
  }
  return '';
};

const fmtDT = (v?: string | number | null) =>
  v ? new Date(v).toLocaleString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—';

export const PersonStudy: React.FC<{ d: PersonDetail; notify: (m: string) => void; reload: () => void }> = ({ d, notify, reload }) => {
  const c = d.calisma;
  const [adlar, setAdlar] = useState<Map<string, Ad> | null>(null);
  const [q, setQ] = useState('');
  const [mod, setMod] = useState<string>('hepsi');
  const [durum, setDurum] = useState<string>('hepsi');
  const [edit, setEdit] = useState<Record<string, { dk: string; soru: string }>>({});
  const [busy, setBusy] = useState(false);
  const [goster, setGoster] = useState<'konular' | 'gunler' | 'ziyaret'>('konular');

  useEffect(() => {
    let on = true;
    void adlariYukle().then((m) => on && setAdlar(m));
    return () => {
      on = false;
    };
  }, []);

  const konular = useMemo(() => {
    const t = q.trim().toLocaleLowerCase('tr-TR');
    return (c?.konular || []).filter((k) => {
      if (mod !== 'hepsi' && k.modul !== mod) return false;
      const dur = k.durum || 'acik';
      if (durum !== 'hepsi' && dur !== durum) return false;
      if (!t) return true;
      const a = adlar?.get(k.id);
      return `${k.konu} ${a?.ad || ''} ${a?.ders || ''}`.toLocaleLowerCase('tr-TR').includes(t);
    });
  }, [c, q, mod, durum, adlar]);

  if (!c || (!c.konular.length && !c.ziyaret.length && !c.gunluk.length))
    return (
      <EmptyState icon={BookOpenCheck} title="Çalışma kaydı yok">
        Bu kişinin profilinde konu bazlı çalışma takibi ya da sayfa ziyareti yok. Kayıt, öğrenci sesli ders, etkileşimli ders, soru
        çözücü ya da En önemliler'de çalıştıkça ve profili eşitlendikçe burada görünür.
      </EmptyState>
    );

  const o = c.ozet;
  const run = async (body: { ops?: StudyEditOp[]; hepsiniSifirla?: boolean }, msg: string) => {
    setBusy(true);
    try {
      const r = await editPersonStudy(d.person.key, body);
      notify(`${msg} (${r.changed} konu). Öğrencinin cihazlarına iletildi.`);
      setEdit({});
      reload();
    } catch (e: any) {
      notify(e?.message || 'Kaydedilemedi.');
    } finally {
      setBusy(false);
    }
  };
  const kaydet = (k: StudyTopic) => {
    const e = edit[k.id];
    if (!e) return;
    const dk = Number(String(e.dk).replace(',', '.'));
    const soru = Number(e.soru);
    if (!Number.isFinite(dk) || dk < 0 || !Number.isFinite(soru) || soru < 0) return notify('Süre ve soru sayısı 0 ya da daha büyük olmalı.');
    void run({ ops: [{ id: k.id, sn: Math.round(dk * 60), soru: Math.round(soru) }] }, 'Konu güncellendi');
  };
  const maxGun = Math.max(1, ...c.gunluk.slice(0, 30).map((g) => g.toplam));
  const modToplam = Object.values(o.modul).reduce((a, v) => a + v, 0) || 1;
  const sayilar = { hepsi: c.konular.length, ...Object.fromEntries(Object.keys(MODUL).map((m) => [m, c.konular.filter((k) => k.modul === m).length])) } as Record<string, number>;

  return (
    <div className="pp-ov ps-study">
      <div className="pp-tiles">
        <div className="pp-tile"><span className="pp-tile-l">Toplam çalışma</span><span className="pp-tile-v">{fmtDuration(o.sn)}</span><span className="pp-tile-s">{(o.sn / 3600).toLocaleString('tr-TR', { maximumFractionDigits: 1 })} saat</span></div>
        <div className="pp-tile"><span className="pp-tile-l">Son 7 gün</span><span className="pp-tile-v">{fmtDuration(o.haftaSn)}</span><span className="pp-tile-s">günde ort. {fmtDuration(o.haftaSn / 7)}</span></div>
        <div className="pp-tile"><span className="pp-tile-l">Çalışılan konu</span><span className="pp-tile-v">{o.konu}</span><span className="pp-tile-s">{o.bitti} bitti</span></div>
        <div className="pp-tile"><span className="pp-tile-l">Çözülen soru</span><span className="pp-tile-v">{o.soru}</span><span className="pp-tile-s">konu takibinde</span></div>
        <div className="pp-tile"><span className="pp-tile-l">Son çalışma</span><span className="pp-tile-v ps-small">{relTime(o.son)}</span><span className="pp-tile-s">{c.son ? `son sayfa ${c.son}` : 'son sayfa yok'}</span></div>
      </div>

      {Object.keys(o.modul).length > 0 && (
        <div className="pp-card">
          <h3>Modüllere göre süre</h3>
          <ul className="pp-meter">
            {Object.entries(o.modul).sort((a, b) => b[1] - a[1]).map(([m, sn]) => (
              <li key={m}>
                <span>{MODUL[m] || m}</span>
                <span className="pp-meter-bar"><i style={{ width: `${Math.round((sn / modToplam) * 100)}%` }} /></span>
                <b>{fmtDuration(sn)}</b>
                <small>%{Math.round((sn / modToplam) * 100)}</small>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="ps-seg" role="tablist" aria-label="Çalışma görünümü">
        {([['konular', `Konular (${c.konular.length})`], ['gunler', `Günler (${c.gunluk.length})`], ['ziyaret', `Sayfa ziyaretleri (${c.ziyaret.length})`]] as const).map(([id, l]) => (
          <button key={id} type="button" role="tab" aria-selected={goster === id} className={`pp-chip ${goster === id ? 'is-on' : ''}`} onClick={() => setGoster(id)}>{l}</button>
        ))}
      </div>

      {goster === 'konular' && (
        <div className="pp-card">
          <div className="ps-bar">
            <label className="pp-search ps-q">
              <Search aria-hidden />
              <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Konu ya da ders ara…" aria-label="Konu ara" />
            </label>
            <select className="ps-sel" value={mod} onChange={(e) => setMod(e.target.value)} aria-label="Modül">
              <option value="hepsi">Tüm modüller ({sayilar.hepsi})</option>
              {Object.keys(MODUL).filter((m) => sayilar[m]).map((m) => <option key={m} value={m}>{MODUL[m]} ({sayilar[m]})</option>)}
            </select>
            <select className="ps-sel" value={durum} onChange={(e) => setDurum(e.target.value)} aria-label="Durum">
              <option value="hepsi">Tüm durumlar</option>
              <option value="bitti">Bitti</option>
              <option value="tekrar">Tekrarda</option>
              <option value="acik">Açık</option>
            </select>
            <ConfirmButton
              className="ms-btn is-sm is-danger"
              confirmLabel="Tümü sıfırlansın mı?"
              disabled={busy || !c.konular.length}
              onConfirm={() => run({ hepsiniSifirla: true }, 'Tüm çalışma kaydı sıfırlandı')}
            >
              <RotateCcw /> Tümünü sıfırla
            </ConfirmButton>
          </div>
          {!konular.length ? (
            <p className="pp-muted">Süzgece uyan konu yok.</p>
          ) : (
            <div className="pp-table-wrap">
              <table className="pp-table ps-table">
                <thead>
                  <tr><th>Konu</th><th>Durum</th><th className="n">Süre</th><th className="n">Soru</th><th>Son</th><th><span className="sr-only">İşlemler</span></th></tr>
                </thead>
                <tbody>
                  {konular.map((k) => {
                    const a = adlar?.get(k.id);
                    const e = edit[k.id];
                    const dur = k.durum || 'acik';
                    const link = konuLink(k);
                    return (
                      <tr key={k.id}>
                        <td className="ps-konu">
                          <b>{a?.ad || k.konu}</b>
                          <small>{MODUL[k.modul] || k.modul} · {a ? a.ders : k.konu}{a?.beklenen ? ` · içerik ~${fmtDuration(a.beklenen)}` : ''}{k.tur ? ` · ${k.tur}. tekrar` : ''}{k.adm ? ' · yönetici düzeltti' : ''}</small>
                        </td>
                        <td>
                          <select
                            className={`ps-sel ps-durum is-${dur}`}
                            value={dur}
                            disabled={busy}
                            aria-label="Konu durumu"
                            onChange={(ev) => void run({ ops: [{ id: k.id, durum: ev.target.value as 'bitti' | 'acik' | 'tekrar' }] }, `Durum: ${DURUM[ev.target.value]}`)}
                          >
                            <option value="acik">Açık</option>
                            <option value="bitti">Bitti</option>
                            <option value="tekrar">Tekrarda</option>
                          </select>
                        </td>
                        <td className="n">
                          {e ? (
                            <input className="ps-num" inputMode="decimal" value={e.dk} onChange={(ev) => setEdit({ ...edit, [k.id]: { ...e, dk: ev.target.value } })} aria-label="Süre (dakika)" title="dakika" />
                          ) : (
                            <span>{fmtDuration(k.sn)}{a?.beklenen ? <small className="ps-pct"> %{Math.min(999, Math.round((k.sn / a.beklenen) * 100))}</small> : null}</span>
                          )}
                        </td>
                        <td className="n">
                          {e ? (
                            <input className="ps-num" inputMode="numeric" value={e.soru} onChange={(ev) => setEdit({ ...edit, [k.id]: { ...e, soru: ev.target.value } })} aria-label="Soru sayısı" />
                          ) : (
                            k.soru
                          )}
                        </td>
                        <td title={k.bittiAt ? `bitti: ${fmtDT(k.bittiAt)}` : undefined}>{relTime(k.sonAt)}</td>
                        <td className="ps-act">
                          {e ? (
                            <>
                              <button type="button" className="ms-btn is-sm is-primary" disabled={busy} onClick={() => kaydet(k)}><Save /> Kaydet</button>
                              <button type="button" className="ms-btn is-sm" onClick={() => { const n = { ...edit }; delete n[k.id]; setEdit(n); }}>Vazgeç</button>
                            </>
                          ) : (
                            <>
                              <button type="button" className="ms-btn is-sm" onClick={() => setEdit({ ...edit, [k.id]: { dk: String(Math.round(k.sn / 6) / 10), soru: String(k.soru) } })}>Düzenle</button>
                              {link && <a className="ms-btn is-sm is-ghost" href={siteLink(link)} target="_blank" rel="noreferrer" aria-label="Sitede aç"><ExternalLink /></a>}
                              <ConfirmButton className="ms-btn is-sm is-ghost" confirmLabel="Sıfırla?" disabled={busy} onConfirm={() => run({ ops: [{ id: k.id, sifirla: true }] }, 'Konu sıfırlandı')}>
                                <RotateCcw />
                              </ConfirmButton>
                            </>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
          <p className="pp-muted ps-note">
            <CheckCircle2 aria-hidden /> Bitti · <Repeat aria-hidden /> Tekrarda · <Circle aria-hidden /> Açık. Düzeltme öğrencinin cihazlarına anında iner; günlük
            süre grafiği geçmiş olduğu için değişmez.
          </p>
        </div>
      )}

      {goster === 'gunler' && (
        <div className="pp-card">
          <h3>Günlük çalışma <small>son {Math.min(60, c.gunluk.length)} gün</small></h3>
          {!c.gunluk.length ? (
            <p className="pp-muted">Günlük süre kaydı yok.</p>
          ) : (
            <div className="pp-table-wrap">
              <table className="pp-table ps-table">
                <thead><tr><th>Gün</th><th className="n">Toplam</th><th className="ps-barcol"><span className="sr-only">Grafik</span></th>{Object.keys(MODUL).slice(0, 4).map((m) => <th key={m} className="n">{MODUL[m]}</th>)}</tr></thead>
                <tbody>
                  {c.gunluk.slice(0, 60).map((g) => (
                    <tr key={g.day}>
                      <td>{new Date(`${g.day}T12:00:00`).toLocaleDateString('tr-TR', { weekday: 'short', day: 'numeric', month: 'short' })}</td>
                      <td className="n"><b>{fmtDuration(g.toplam)}</b></td>
                      <td className="ps-barcol"><span className="pp-meter-bar"><i style={{ width: `${Math.round((g.toplam / maxGun) * 100)}%` }} /></span></td>
                      {(['sesli', 'ogren', 'cozucu', 'onem'] as const).map((m) => <td key={m} className="n">{g[m] ? fmtDuration(g[m] || 0) : '—'}</td>)}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {goster === 'ziyaret' && (
        <>
          <div className="pp-card">
            <h3>Sayfa ziyaretleri <small>en yeni üstte · etkin süre</small></h3>
            {!c.ziyaret.length ? (
              <p className="pp-muted">Ziyaret kaydı yok (etkinlik günlüğü 2026-10-20'den beri tutuluyor).</p>
            ) : (
              <div className="pp-table-wrap">
                <table className="pp-table ps-table">
                  <thead><tr><th>Giriş</th><th>Sayfa</th><th className="n">Etkin süre</th><th className="n">Kaydırma</th></tr></thead>
                  <tbody>
                    {c.ziyaret.slice(0, 200).map((z, i) => (
                      <tr key={`${z.g}-${i}`}>
                        <td>{fmtDT(z.g)}</td>
                        <td className="ps-konu"><a href={siteLink(z.p)} target="_blank" rel="noreferrer"><b>{(z.t || '').replace(/ · MeDSor$/, '') || z.p}</b></a><small>{z.p}</small></td>
                        <td className="n">{fmtDuration(z.s)}</td>
                        <td className="n">%{Math.round(z.k || 0)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
          {c.konum.length > 0 && (
            <div className="pp-card">
              <h3>Sayfa başına toplam <small>kaldığı yer dahil</small></h3>
              <div className="pp-table-wrap">
                <table className="pp-table ps-table">
                  <thead><tr><th>Sayfa</th><th className="n">Toplam</th><th className="n">Ziyaret</th><th className="n">Kaldığı yer</th><th>Son</th></tr></thead>
                  <tbody>
                    {[...c.konum].sort((a, b) => b.s - a.s).map((k) => (
                      <tr key={k.p}>
                        <td className="ps-konu"><a href={siteLink(k.p)} target="_blank" rel="noreferrer"><b>{(k.t || '').replace(/ · MeDSor$/, '') || k.p}</b></a><small>{k.p}</small></td>
                        <td className="n">{fmtDuration(k.s)}</td>
                        <td className="n">{k.n}</td>
                        <td className="n">%{Math.round(k.k || 0)}</td>
                        <td>{fmtDT(k.at)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};
