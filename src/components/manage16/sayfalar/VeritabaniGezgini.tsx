import React, { useEffect, useMemo, useState } from 'react';
import { SayfaBasligi, AyrintiCekmecesi, JsonDuzenleyici, Rozet, Hata, Yukleniyor, BosDurum, adminIstek, bildir, onayIste, useAdminSorgu } from '../kit';
import type { SayfaProps } from '../menu';
import './ortak/ts16.css';

type Col = { name: string; type: string; udt: string; nullable: boolean };
type Tablo = { name: string; rows: number; bytes: number; columns: Col[]; pk: string[]; mirror: string | null };
type Satirlar = { rows: Record<string, any>[]; total: number; exact: boolean; limit: number; offset: number };
type SqlSonuc = { fields: string[]; rows: unknown[][]; total: number; truncated: boolean; ms: number };

const boyutMetni = (b: number) => (b > 1 << 30 ? `${(b / (1 << 30)).toFixed(1)} GB` : b > 1 << 20 ? `${(b / (1 << 20)).toFixed(1)} MB` : `${Math.round(b / 1024)} KB`);
const hucre = (v: unknown) => (v === null || v === undefined ? '∅' : typeof v === 'object' ? JSON.stringify(v) : String(v));
const LIMIT = 50;

function csvIndir(ad: string, alanlar: string[], satirlar: unknown[][]) {
  const k = (v: unknown) => { const s = hucre(v); return /[",\n;]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
  const metin = [alanlar.map(k).join(','), ...satirlar.map((r) => r.map(k).join(','))].join('\n');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob(['﻿' + metin], { type: 'text/csv;charset=utf-8' }));
  a.download = ad;
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 2000);
}

/** Sistem › Veritabanı gezgini — meds-pg tabloları (pgAdminRoutes). SQL konsolu salt okunur rolle çalışır. */
export default function VeritabaniGezgini({ id, git }: SayfaProps) {
  const [sekme, setSekme] = useState<'tablo' | 'sql'>(id === '_sql' ? 'sql' : 'tablo');
  const t = useAdminSorgu<{ tables: Tablo[]; databaseBytes: number; version: string }>('/api/admin/pg/tables');
  const [suz, setSuz] = useState('');
  const secili = t.veri?.tables.find((x) => x.name === id) || null;
  const tablolar = (t.veri?.tables || []).filter((x) => !suz || x.name.includes(suz.toLowerCase()));
  return (
    <>
      <SayfaBasligi baslik="Veritabanı gezgini" aciklama={t.veri ? `${t.veri.version} · ${boyutMetni(t.veri.databaseBytes)} · ${t.veri.tables.length} tablo` : 'meds-pg tabloları'}>
        <div className="m16-sekmeler" role="tablist">
          <button type="button" role="tab" aria-selected={sekme === 'tablo'} className={sekme === 'tablo' ? 'on' : ''} onClick={() => { setSekme('tablo'); if (id === '_sql') git('sistem/db', { degistir: true }); }}>Tablolar</button>
          <button type="button" role="tab" aria-selected={sekme === 'sql'} className={sekme === 'sql' ? 'on' : ''} onClick={() => { setSekme('sql'); git('sistem/db/_sql', { degistir: true }); }}>Salt okunur SQL</button>
        </div>
      </SayfaBasligi>
      {t.hata && <Hata hata={t.hata} yenile={t.yenile} />}
      {sekme === 'sql' ? <SqlKonsolu /> : (
        <div className="m16-ts-sol">
          <section className="m16-kart">
            <input className="m16-girdi" placeholder="Tablo süz…" value={suz} onChange={(e) => setSuz(e.target.value)} aria-label="Tablo süz" style={{ width: '100%' }} />
            <div className="m16-ts-tablolar" style={{ marginTop: 8 }}>
              {!t.veri && !t.hata && <Yukleniyor satir={6} />}
              {tablolar.map((x) => (
                <button type="button" key={x.name} className={x.name === id ? 'on' : ''} onClick={() => git(`sistem/db/${x.name}`)}>
                  <span className="m16-kisalt">{x.name}</span><small>{x.rows.toLocaleString('tr-TR')}</small>
                </button>
              ))}
            </div>
          </section>
          <section className="m16-kart" style={{ minWidth: 0 }}>
            {secili ? <TabloGorunumu key={secili.name} t={secili} /> : <BosDurum baslik="Tablo seçin" aciklama="Soldaki listeden bir tablo seçin. Satır okumaları kişisel veri olabileceği için denetim kaydına yazılır." />}
          </section>
        </div>
      )}
    </>
  );
}

function TabloGorunumu({ t }: { t: Tablo }) {
  const [q, setQ] = useState('');
  const [debQ, setDebQ] = useState('');
  const [offset, setOffset] = useState(0);
  const [sira, setSira] = useState<{ col: string; dir: 'asc' | 'desc' } | null>(null);
  const [acik, setAcik] = useState<Record<string, any> | null>(null);
  const [tam, setTam] = useState<Record<string, any> | null>(null);
  useEffect(() => { const x = setTimeout(() => { setDebQ(q); setOffset(0); }, 300); return () => clearTimeout(x); }, [q]);
  const sorgu = useMemo(() => ({ table: t.name, limit: LIMIT, offset, q: debQ, order: sira?.col, dir: sira?.dir }), [t.name, offset, debQ, sira]);
  const s = useAdminSorgu<Satirlar>('/api/admin/pg/rows', { sorgu });
  const anahtar = (r: Record<string, any>) => (t.pk.length ? Object.fromEntries(t.pk.map((k) => [k, r[k]])) : { ctid: r.__ctid });
  const cols = t.columns.map((c) => c.name);

  useEffect(() => {
    setTam(null);
    if (!acik) return;
    adminIstek<{ row: Record<string, any> }>('/api/admin/pg/row', { sorgu: { table: t.name, key: JSON.stringify(anahtar(acik)) } })
      .then((r) => setTam(r.row), (e) => bildir(e?.message || String(e), 'kotu'));
  }, [acik]); // eslint-disable-line react-hooks/exhaustive-deps

  const kaydet = async (yeni: unknown) => {
    if (!tam || !yeni || typeof yeni !== 'object') return;
    const set: Record<string, unknown> = {};
    for (const c of t.columns) {
      if (c.udt === 'vector' || !(c.name in (yeni as any))) continue;
      if (JSON.stringify((yeni as any)[c.name]) !== JSON.stringify(tam[c.name])) set[c.name] = (yeni as any)[c.name];
    }
    if (!Object.keys(set).length) { bildir('Değişiklik yok.', 'bilgi'); return; }
    if (!(await onayIste({ baslik: `${Object.keys(set).length} sütun güncellensin mi?`, aciklama: <>{Object.keys(set).join(', ')}{t.mirror ? <><br />Bu tablo <b>{t.mirror}</b> kaynağından yansır; düzeltme sonraki eşitlemede ezilebilir.</> : null}</>, onayMetni: 'Güncelle', tehlikeli: true }))) return;
    try { await adminIstek('/api/admin/pg/row', { yontem: 'PATCH', govde: { table: t.name, key: anahtar(tam), set } }); bildir('Satır güncellendi.', 'iyi'); setAcik(null); void s.yenile(); }
    catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
  };
  const sil = async () => {
    if (!tam) return;
    if (!(await onayIste({ baslik: 'Satır kalıcı silinsin mi?', tehlikeli: true, yazilacak: 'SIL', onayMetni: 'Kalıcı sil', aciklama: <>Tablo <code>{t.name}</code>, anahtar <code>{JSON.stringify(anahtar(tam))}</code>. Geri alınamaz; gece yedeğinden döner.</> }))) return;
    try { await adminIstek('/api/admin/pg/row', { yontem: 'DELETE', govde: { table: t.name, key: anahtar(tam), onay: 'SIL' } }); bildir('Satır silindi.', 'iyi'); setAcik(null); void s.yenile(); }
    catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
  };
  const toplam = s.veri?.total ?? t.rows;
  return (
    <>
      <div className="m16-tablo-arac" style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center' }}>
        <strong>{t.name}</strong>
        <Rozet>{t.pk.length ? `anahtar: ${t.pk.join(', ')}` : 'anahtarsız (ctid)'}</Rozet>
        {t.mirror && <Rozet ton="uyari" title="Asıl kaynak JSON">{t.mirror}</Rozet>}
        <Rozet>{boyutMetni(t.bytes)}</Rozet>
        <input className="m16-girdi" placeholder="Satırlarda ara…" value={q} onChange={(e) => setQ(e.target.value)} aria-label="Satırlarda ara" style={{ flex: '1 1 180px' }} />
        <button type="button" className="m16-btn" disabled={!s.veri?.rows.length} onClick={() => csvIndir(`${t.name}.csv`, cols, (s.veri?.rows || []).map((r) => cols.map((c) => r[c])))}>Bu sayfayı CSV</button>
      </div>
      {s.hata ? <Hata hata={s.hata} yenile={s.yenile} /> : !s.veri ? <Yukleniyor satir={8} /> : (
        <div className="m16-ts-grid" style={{ marginTop: 8 }}>
          <table>
            <thead><tr>{cols.map((c) => (
              <th key={c} aria-sort={sira?.col === c ? (sira.dir === 'asc' ? 'ascending' : 'descending') : undefined}>
                <button type="button" className="m16-sirala" onClick={() => setSira(sira?.col === c && sira.dir === 'desc' ? { col: c, dir: 'asc' } : { col: c, dir: 'desc' })}>{c}{sira?.col === c ? (sira.dir === 'asc' ? ' ↑' : ' ↓') : ''}</button>
              </th>))}</tr></thead>
            <tbody>
              {s.veri.rows.map((r) => (
                <tr key={r.__ctid} tabIndex={0} onClick={() => setAcik(r)} onKeyDown={(e) => { if (e.key === 'Enter') setAcik(r); }}>
                  {cols.map((c) => <td key={c} title={hucre(r[c])}>{hucre(r[c])}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <div className="m16-sayfala" style={{ display: 'flex', gap: 8, alignItems: 'center', marginTop: 8 }}>
        <button type="button" className="m16-btn" disabled={offset === 0} onClick={() => setOffset(Math.max(0, offset - LIMIT))}>Önceki</button>
        <span>{toplam ? `${offset + 1}–${Math.min(offset + LIMIT, toplam)} / ${s.veri?.exact ? '' : '~'}${toplam.toLocaleString('tr-TR')}` : '0'}</span>
        <button type="button" className="m16-btn" disabled={offset + LIMIT >= toplam} onClick={() => setOffset(offset + LIMIT)}>Sonraki</button>
      </div>
      <AyrintiCekmecesi acik={!!acik} kapat={() => setAcik(null)} genis baslik={`${t.name} satırı`} altBaslik={acik ? JSON.stringify(anahtar(acik)) : ''}
        eylemler={tam && <button type="button" className="m16-btn tehlike" onClick={sil}>Satırı sil…</button>}>
        {!tam ? <Yukleniyor satir={6} /> : (
          <>
            <p className="m16-ts-not">JSON'u düzenleyip kaydedin; yalnız değişen sütunlar gönderilir. Vektör sütunları düzenlenmez.</p>
            <JsonDuzenleyici deger={Object.fromEntries(Object.entries(tam).filter(([k]) => k !== '__ctid'))} kaydet={kaydet} satir={22} />
          </>
        )}
      </AyrintiCekmecesi>
    </>
  );
}

function SqlKonsolu() {
  const [sql, setSql] = useState(() => { try { return localStorage.getItem('m16_sql') || 'select relname, n_live_tup from pg_stat_user_tables order by 2 desc limit 20'; } catch { return ''; } });
  const [sonuc, setSonuc] = useState<SqlSonuc | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const [calisiyor, setCalisiyor] = useState(false);
  const calistir = async () => {
    setCalisiyor(true); setHata(null);
    try { localStorage.setItem('m16_sql', sql); } catch { /* */ }
    try { setSonuc(await adminIstek<SqlSonuc>('/api/admin/pg/sql', { yontem: 'POST', govde: { sql } })); }
    catch (e: any) { setHata(e?.message || String(e)); setSonuc(null); }
    finally { setCalisiyor(false); }
  };
  return (
    <section className="m16-kart" style={{ marginTop: 12 }}>
      <h2>Salt okunur SQL</h2>
      <p className="m16-ts-not">Tek deyim (SELECT/WITH/EXPLAIN/VALUES/TABLE/SHOW), READ ONLY işlem, yazma yetkisi olmayan <code>meds_salt_okur</code> rolü, 10 sn zaman aşımı, en çok 1000 satır. Ctrl+Enter çalıştırır.</p>
      <textarea className="m16-girdi m16-ts-sql" value={sql} onChange={(e) => setSql(e.target.value)} spellCheck={false} aria-label="SQL sorgusu"
        onKeyDown={(e) => { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) void calistir(); }} />
      <div className="m16-ts-eylem" style={{ margin: '8px 0' }}>
        <button type="button" className="m16-btn birincil" disabled={calisiyor || !sql.trim()} onClick={calistir}>{calisiyor ? 'Çalışıyor…' : 'Çalıştır'}</button>
        {sonuc && <button type="button" className="m16-btn" onClick={() => csvIndir('sorgu.csv', sonuc.fields, sonuc.rows)}>CSV indir</button>}
        {sonuc && <span className="m16-ts-not">{sonuc.total} satır · {sonuc.ms} ms{sonuc.truncated ? ' · ilk 1000 gösteriliyor' : ''}</span>}
      </div>
      {hata && <div className="m16-durum-hata" role="alert">{hata}</div>}
      {sonuc && (
        <div className="m16-ts-grid">
          <table>
            <thead><tr>{sonuc.fields.map((f, i) => <th key={i}>{f}</th>)}</tr></thead>
            <tbody>{sonuc.rows.map((r, i) => <tr key={i}>{r.map((v, j) => <td key={j} title={hucre(v)}>{hucre(v)}</td>)}</tr>)}</tbody>
          </table>
        </div>
      )}
    </section>
  );
}
