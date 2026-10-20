import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { Database, RefreshCw, Search, Plus, Save, Trash2, Play, Download, AlertTriangle, ChevronLeft, ChevronRight, Table2, TerminalSquare } from 'lucide-react';
import { adminCall } from '../../services/peopleService';
import { Panel, EmptyState, ConfirmButton, Drawer, Seg } from './consoleUi';
import { PANEL_ON_ORACLE_AT_BOOT } from '../../config/deployment';
import './db-explorer.css';

/**
 * Yönetim › Veritabanı gezgini: meds-pg'deki her tabloyu listeler; satırları arar, sıralar, düzenler, ekler ve siler;
 * salt okunur SQL çalıştırır (CSV alınabilir). Sunucu: src/services/pgAdminRoutes.ts (güçlü yönetici yetkisi).
 * data/*.json'dan yansıyan tablolar uyarı taşır: kalıcı düzeltme için ilgili bölüme (Veri kataloğu vb.) yönlendirir.
 */
type Col = { name: string; type: string; udt: string; nullable: boolean; def: string | null };
type Table = { name: string; rows: number; bytes: number; columns: Col[]; pk: string[]; mirror: string | null };
type Tables = { tables: Table[]; databaseBytes: number; version: string; at: string };
type Rows = { table: string; rows: Record<string, any>[]; total: number; exact: boolean; limit: number; offset: number };
type SqlRes = { fields: string[]; rows: any[][]; total: number; truncated: boolean; ms: number };

/** Tablo → panelde kalıcı düzenlemenin yapıldığı bölüm */
const KAYNAK_BOLUM: Record<string, { slug: string; label: string }> = {
  past_questions: { slug: 'veri-katalogu', label: 'Veri kataloğu › Çıkmış sorular' },
  questions: { slug: 'soru-havuzu', label: 'Soru havuzu' },
  practice_questions: { slug: 'veri-katalogu', label: 'Veri kataloğu › Örnek sorular' },
  lecture_notes: { slug: 'tum-veriler', label: 'Tüm veriler' },
  committees: { slug: 'soru-havuzu', label: 'Soru havuzu' },
  user_data: { slug: 'kisiler', label: 'Kişiler' },
  user_devices: { slug: 'kisiler', label: 'Kişiler' },
  user_events: { slug: 'kisiler', label: 'Kişiler' },
  users: { slug: 'kullanicilar', label: 'Kullanıcılar' },
};

const fmtBytes = (b: number) => (b > 1e9 ? `${(b / 1e9).toFixed(1)} GB` : b > 1e6 ? `${(b / 1e6).toFixed(1)} MB` : `${Math.round(b / 1e3)} KB`);
const show = (v: any) => {
  if (v === null || v === undefined) return '∅';
  if (typeof v === 'object') return JSON.stringify(v);
  return String(v);
};
const isJson = (c: Col) => c.udt === 'json' || c.udt === 'jsonb' || c.type === 'ARRAY';
const toEdit = (c: Col, v: any) => (v === null || v === undefined ? '' : isJson(c) ? JSON.stringify(v, null, 2) : String(v));
const fromEdit = (c: Col, s: string, wasNull: boolean): any => {
  if (s === '' && (wasNull || c.nullable)) return null;
  if (isJson(c)) return JSON.parse(s);
  if (c.udt === 'bool') return /^(true|1|evet|t)$/i.test(s.trim());
  return s;
};
const csv = (fields: string[], rows: any[][]) =>
  [fields, ...rows].map((r) => r.map((v) => { const s = show(v); return /[",\n;]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; }).join(',')).join('\n');
const indir = (name: string, text: string) => {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob(['﻿' + text], { type: 'text/csv;charset=utf-8' }));
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 2000);
};
const goSection = (slug: string) => {
  window.history.pushState({ route: 'manage', param: slug }, '', `/manage/${slug}`);
  window.dispatchEvent(new PopStateEvent('popstate'));
};

export const ManageDatabaseExplorer: React.FC<{ notify: (m: string) => void }> = ({ notify }) => {
  const [mode, setMode] = useState<'tables' | 'sql'>('tables');
  const [meta, setMeta] = useState<Tables | null>(null);
  const [err, setErr] = useState('');
  const [tq, setTq] = useState('');
  const [sel, setSel] = useState<string>(() => new URLSearchParams(window.location.search).get('tablo') || '');
  const [rows, setRows] = useState<Rows | null>(null);
  const [rowsErr, setRowsErr] = useState('');
  const [q, setQ] = useState('');
  const [qCol, setQCol] = useState('');
  const [order, setOrder] = useState<{ col: string; dir: 'asc' | 'desc' }>({ col: '', dir: 'desc' });
  const [page, setPage] = useState(0);
  const [limit, setLimit] = useState(50);
  const [loading, setLoading] = useState(false);
  const [edit, setEdit] = useState<{ row: Record<string, any> | null; vals: Record<string, string> } | null>(null);
  const [busy, setBusy] = useState(false);

  const table = meta?.tables.find((t) => t.name === sel) || null;

  const loadMeta = useCallback(async (force = false) => {
    try {
      const m = await adminCall<Tables>(`/api/admin/pg/tables${force ? '?yenile=1' : ''}`);
      if (!Array.isArray(m?.tables)) throw new Error('Sunucu tablo listesi döndürmedi (bu sunucuda veritabanı gezgini ucu yok olabilir; Canlı/Yerel seçimini kontrol et).');
      setMeta(m);
      setErr('');
      setSel((s) => s || m.tables.slice().sort((a, b) => b.rows - a.rows).find((t) => t.name !== 'rag_chunks')?.name || '');
    } catch (e: any) {
      setErr(e?.message || 'Tablolar yüklenemedi.');
    }
  }, []);
  useEffect(() => { void loadMeta(); }, [loadMeta]);

  const loadRows = useCallback(async () => {
    if (!sel) return;
    setLoading(true);
    try {
      const sp = new URLSearchParams({ table: sel, limit: String(limit), offset: String(page * limit) });
      if (q.trim()) sp.set('q', q.trim());
      if (qCol) sp.set('col', qCol);
      if (order.col) { sp.set('order', order.col); sp.set('dir', order.dir); }
      else sp.set('dir', order.dir);
      setRows(await adminCall<Rows>(`/api/admin/pg/rows?${sp}`));
      setRowsErr('');
    } catch (e: any) {
      setRowsErr(e?.message || 'Satırlar yüklenemedi.');
    } finally {
      setLoading(false);
    }
  }, [sel, q, qCol, order, page, limit]);
  useEffect(() => {
    const t = setTimeout(() => void loadRows(), q ? 300 : 0);
    return () => clearTimeout(t);
  }, [loadRows, q]);

  // Tablo değişince arama/sayfa sıfırlanır ve adres güncellenir (kopyalanabilir)
  const pick = (name: string) => {
    setSel(name);
    setQ('');
    setQCol('');
    setPage(0);
    setOrder({ col: '', dir: 'desc' });
    setRows(null);
    try { window.history.replaceState(window.history.state, '', `/manage/veritabani-gezgini?tablo=${encodeURIComponent(name)}`); } catch { /* çerçeve */ }
  };

  const keyOf = (r: Record<string, any>) => (table?.pk.length ? Object.fromEntries(table.pk.map((k) => [k, r[k]])) : { ctid: r.__ctid });

  /** Listede büyük alanlar kısaltılmış gelir: düzenlemeden önce satırın tam hali çekilir */
  const openRow = async (r: Record<string, any>) => {
    if (!table) return;
    try {
      const sp = new URLSearchParams({ table: table.name, key: JSON.stringify(keyOf(r)) });
      const { row } = await adminCall<{ row: Record<string, any> }>(`/api/admin/pg/row?${sp}`);
      setEdit({ row, vals: Object.fromEntries(cols.map((c) => [c.name, toEdit(c, row[c.name])])) });
    } catch (e: any) {
      notify(e?.message || 'Satır açılamadı.');
    }
  };

  const save = async () => {
    if (!table || !edit) return;
    setBusy(true);
    try {
      const out: Record<string, any> = {};
      for (const c of table.columns) {
        if (c.udt === 'vector') continue;
        const s = edit.vals[c.name] ?? '';
        const before = edit.row ? toEdit(c, edit.row[c.name]) : '';
        if (edit.row && s === before) continue;
        if (!edit.row && s === '') continue;
        try { out[c.name] = fromEdit(c, s, edit.row ? edit.row[c.name] == null : true); }
        catch { throw new Error(`${c.name}: geçerli JSON değil.`); }
      }
      if (!Object.keys(out).length) { notify('Değişiklik yok.'); return; }
      if (edit.row) await adminCall('/api/admin/pg/row', { method: 'PATCH', body: JSON.stringify({ table: table.name, key: keyOf(edit.row), set: out }) });
      else await adminCall('/api/admin/pg/row', { method: 'POST', body: JSON.stringify({ table: table.name, values: out }) });
      notify(edit.row ? 'Satır kaydedildi.' : 'Satır eklendi.');
      setEdit(null);
      void loadRows();
    } catch (e: any) {
      notify(e?.message || 'Kaydedilemedi.');
    } finally {
      setBusy(false);
    }
  };
  const remove = async () => {
    if (!table || !edit?.row) return;
    setBusy(true);
    try {
      await adminCall('/api/admin/pg/row', { method: 'DELETE', body: JSON.stringify({ table: table.name, key: keyOf(edit.row) }) });
      notify('Satır silindi.');
      setEdit(null);
      void loadRows();
    } catch (e: any) {
      notify(e?.message || 'Silinemedi.');
    } finally {
      setBusy(false);
    }
  };

  const tables = useMemo(() => {
    const t = tq.trim().toLowerCase();
    return (meta?.tables || []).filter((x) => !t || x.name.includes(t)).sort((a, b) => a.name.localeCompare(b.name));
  }, [meta, tq]);
  const cols = table?.columns || [];
  const total = rows?.total ?? 0;
  const pages = Math.max(1, Math.ceil(total / limit));
  const kaynak = table ? KAYNAK_BOLUM[table.name] : undefined;

  return (
    <div className="dbx">
      <Panel
        title="Veritabanı gezgini"
        icon={Database}
        count={meta ? `${meta.tables.length} tablo · ${fmtBytes(meta.databaseBytes)}` : undefined}
        desc={
          <>
            meds-pg ({meta?.version || 'PostgreSQL'}) — {PANEL_ON_ORACLE_AT_BOOT ? <b>CANLI (Oracle) veritabanı</b> : <b>bu sunucunun veritabanı</b>}. Satırları ara, düzenle, ekle, sil; SQL sekmesi
            salt okunurdur (10 sn, 1000 satır).
          </>
        }
        tools={
          <>
            <Seg value={mode} onChange={setMode} label="Görünüm" options={[{ id: 'tables' as const, label: 'Tablolar' }, { id: 'sql' as const, label: 'SQL' }]} />
            <button type="button" className="ms-btn" onClick={() => { void loadMeta(true); void loadRows(); }} aria-label="Yenile"><RefreshCw aria-hidden /> Yenile</button>
          </>
        }
      >
        {err && <p className="dbx-err" role="alert">{err}</p>}
        {!meta && !err && <p className="dbx-muted">Yükleniyor…</p>}
        {meta && mode === 'sql' && <SqlBox notify={notify} tables={meta.tables} />}
        {meta && mode === 'tables' && (
          <div className="dbx-grid">
            <nav className="dbx-side" aria-label="Tablolar">
              <label className="dbx-search">
                <Search aria-hidden />
                <input value={tq} onChange={(e) => setTq(e.target.value)} placeholder="Tablo ara…" aria-label="Tablo ara" />
              </label>
              <ul>
                {tables.map((t) => (
                  <li key={t.name}>
                    <button type="button" className={`dbx-t ${t.name === sel ? 'is-on' : ''}`} onClick={() => pick(t.name)} aria-current={t.name === sel ? 'true' : undefined}>
                      <span className="nm">{t.name}</span>
                      <span className="n">{t.rows.toLocaleString('tr-TR')}</span>
                    </button>
                  </li>
                ))}
              </ul>
            </nav>
            <div className="dbx-main">
              {!table ? (
                <EmptyState icon={Table2} title="Tablo seç">Soldan bir tablo seç.</EmptyState>
              ) : (
                <>
                  <div className="dbx-head">
                    <h3>{table.name} <small>{total.toLocaleString('tr-TR')}{rows && !rows.exact ? ' (yaklaşık)' : ''} satır · {cols.length} sütun · {fmtBytes(table.bytes)} · anahtar: {table.pk.join(', ') || 'yok (ctid)'}</small></h3>
                    <button type="button" className="ms-btn is-sm is-primary" onClick={() => setEdit({ row: null, vals: {} })}><Plus aria-hidden /> Yeni satır</button>
                    <button type="button" className="ms-btn is-sm" disabled={!rows?.rows.length} onClick={() => rows && indir(`${table.name}.csv`, csv(cols.map((c) => c.name), rows.rows.map((r) => cols.map((c) => r[c.name]))))}>
                      <Download aria-hidden /> Bu sayfa CSV
                    </button>
                  </div>
                  {table.mirror && (
                    <p className="dbx-warn">
                      <AlertTriangle aria-hidden /> Bu tablo <b>{table.mirror}</b> kaynağının kopyasıdır; burada yapılan değişiklik bir sonraki eşitlemede ezilebilir.
                      {kaynak && <> Kalıcı düzenleme için <button type="button" className="dbx-link" onClick={() => goSection(kaynak.slug)}>{kaynak.label}</button>.</>}
                    </p>
                  )}
                  {!table.mirror && kaynak && (
                    <p className="dbx-muted">Bu verinin panel ekranı: <button type="button" className="dbx-link" onClick={() => goSection(kaynak.slug)}>{kaynak.label}</button></p>
                  )}
                  <div className="dbx-bar">
                    <label className="dbx-search dbx-grow">
                      <Search aria-hidden />
                      <input value={q} onChange={(e) => { setQ(e.target.value); setPage(0); }} placeholder={qCol ? `${qCol} içinde ara…` : 'Tüm sütunlarda ara…'} aria-label="Satır ara" />
                    </label>
                    <select className="dbx-sel" value={qCol} onChange={(e) => { setQCol(e.target.value); setPage(0); }} aria-label="Arama sütunu">
                      <option value="">Tüm sütunlar</option>
                      {cols.filter((c) => c.udt !== 'vector').map((c) => <option key={c.name} value={c.name}>{c.name}</option>)}
                    </select>
                    <select className="dbx-sel" value={limit} onChange={(e) => { setLimit(Number(e.target.value)); setPage(0); }} aria-label="Sayfa boyu">
                      {[25, 50, 100, 250].map((n) => <option key={n} value={n}>{n} / sayfa</option>)}
                    </select>
                  </div>
                  {rowsErr && <p className="dbx-err" role="alert">{rowsErr}</p>}
                  <div className="dbx-tablewrap" aria-busy={loading}>
                    <table className="dbx-table">
                      <thead>
                        <tr>
                          {cols.map((c) => (
                            <th key={c.name} aria-sort={order.col === c.name ? (order.dir === 'asc' ? 'ascending' : 'descending') : undefined}>
                              <button type="button" onClick={() => { setOrder((o) => ({ col: c.name, dir: o.col === c.name && o.dir === 'desc' ? 'asc' : 'desc' })); setPage(0); }} title={`${c.type}${c.nullable ? '' : ' · zorunlu'}`}>
                                {table.pk.includes(c.name) ? '🔑 ' : ''}{c.name}{order.col === c.name ? (order.dir === 'asc' ? ' ↑' : ' ↓') : ''}
                              </button>
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {rows?.rows.map((r) => (
                          <tr key={r.__ctid} tabIndex={0} onClick={() => void openRow(r)} onKeyDown={(e) => { if (e.key === 'Enter') (e.currentTarget as HTMLElement).click(); }}>
                            {cols.map((c) => <td key={c.name} className={r[c.name] == null ? 'is-null' : ''}>{show(r[c.name]).slice(0, 140)}</td>)}
                          </tr>
                        ))}
                        {rows && !rows.rows.length && <tr><td colSpan={cols.length || 1} className="dbx-muted">Satır yok.</td></tr>}
                      </tbody>
                    </table>
                  </div>
                  <div className="dbx-pager">
                    <button type="button" className="ms-btn is-sm" disabled={page === 0} onClick={() => setPage(page - 1)} aria-label="Önceki sayfa"><ChevronLeft aria-hidden /></button>
                    <span>Sayfa {page + 1} / {pages.toLocaleString('tr-TR')}</span>
                    <button type="button" className="ms-btn is-sm" disabled={page + 1 >= pages} onClick={() => setPage(page + 1)} aria-label="Sonraki sayfa"><ChevronRight aria-hidden /></button>
                    <span className="dbx-muted">Satıra tıkla: düzenle / sil</span>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </Panel>

      <Drawer
        open={!!edit && !!table}
        onClose={() => setEdit(null)}
        wide
        title={edit?.row ? `${table?.name} · satırı düzenle` : `${table?.name} · yeni satır`}
        foot={
          <>
            {edit?.row && (
              <ConfirmButton onConfirm={remove} confirmLabel="Kalıcı silinsin mi?" disabled={busy}>
                <Trash2 aria-hidden /> Sil
              </ConfirmButton>
            )}
            <span style={{ flex: 1 }} />
            <button type="button" className="ms-btn" onClick={() => setEdit(null)}>Vazgeç</button>
            <button type="button" className="ms-btn is-primary" onClick={() => void save()} disabled={busy}><Save aria-hidden /> {busy ? 'Kaydediliyor…' : 'Kaydet'}</button>
          </>
        }
      >
        {edit && table && (
          <div className="dbx-form">
            {table.mirror && <p className="dbx-warn"><AlertTriangle aria-hidden /> Kopya tablo: kalıcı kaynak {table.mirror}.</p>}
            {cols.map((c) => {
              const v = edit.vals[c.name] ?? '';
              const long = isJson(c) || v.length > 80;
              return (
                <label key={c.name} className="dbx-field">
                  <span>
                    {c.name} <small>{c.type}{c.nullable ? '' : ' · zorunlu'}{c.def ? ` · varsayılan ${c.def.slice(0, 40)}` : ''}{table.pk.includes(c.name) ? ' · anahtar' : ''}</small>
                  </span>
                  {c.udt === 'vector' ? (
                    <input value={v} disabled aria-readonly />
                  ) : long ? (
                    <textarea value={v} rows={Math.min(14, Math.max(2, v.split('\n').length))} onChange={(e) => setEdit({ ...edit, vals: { ...edit.vals, [c.name]: e.target.value } })} spellCheck={false} />
                  ) : (
                    <input value={v} onChange={(e) => setEdit({ ...edit, vals: { ...edit.vals, [c.name]: e.target.value } })} placeholder={edit.row ? '' : c.def ? 'boş = varsayılan' : c.nullable ? 'boş = NULL' : ''} />
                  )}
                </label>
              );
            })}
          </div>
        )}
      </Drawer>
    </div>
  );
};

const SqlBox: React.FC<{ notify: (m: string) => void; tables: Table[] }> = ({ notify, tables }) => {
  const [sql, setSql] = useState(() => {
    try { return localStorage.getItem('medsoru_dbx_sql') || 'select * from user_devices order by last_seen desc limit 50'; } catch { return 'select 1'; }
  });
  const [res, setRes] = useState<SqlRes | null>(null);
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);
  const run = async () => {
    setBusy(true);
    try { localStorage.setItem('medsoru_dbx_sql', sql); } catch { /* özel pencere */ }
    try {
      setRes(await adminCall<SqlRes>('/api/admin/pg/sql', { method: 'POST', body: JSON.stringify({ sql }) }));
      setErr('');
    } catch (e: any) {
      setErr(e?.message || 'Sorgu çalışmadı.');
      setRes(null);
    } finally {
      setBusy(false);
    }
  };
  const ornek = [
    ['Son görülen cihazlar', 'select display_name, email, label, last_seen, active_seconds from user_devices order by last_seen desc limit 100'],
    ['Günlük kullanım (14 gün)', "select day, sum(active_seconds)/3600.0 as saat, count(distinct coalesce(uid, device_id)) as kisi from user_usage_daily where day > current_date - 14 group by day order by day desc"],
    ['Son öğrenci olayları', 'select at, display_name, kind, action, label from user_events order by at desc limit 100'],
    ['Tablo boyutları', "select relname, n_live_tup, pg_size_pretty(pg_total_relation_size(relid)) from pg_stat_user_tables order by pg_total_relation_size(relid) desc"],
  ];
  return (
    <div className="dbx-sql">
      <div className="dbx-chips">
        {ornek.map(([l, s]) => <button key={l} type="button" className="ms-btn is-sm" onClick={() => setSql(s)}>{l}</button>)}
      </div>
      <textarea
        className="dbx-sqlbox"
        value={sql}
        onChange={(e) => setSql(e.target.value)}
        onKeyDown={(e) => { if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); void run(); } }}
        rows={6}
        spellCheck={false}
        aria-label="SQL sorgusu"
      />
      <div className="dbx-bar">
        <button type="button" className="ms-btn is-primary" onClick={() => void run()} disabled={busy}><Play aria-hidden /> {busy ? 'Çalışıyor…' : 'Çalıştır'} <kbd>Ctrl ↵</kbd></button>
        {res && <button type="button" className="ms-btn" onClick={() => indir('sorgu.csv', csv(res.fields, res.rows))}><Download aria-hidden /> CSV</button>}
        {res && <span className="dbx-muted">{res.total.toLocaleString('tr-TR')} satır · {res.ms} ms{res.truncated ? ' · ilk 1000 gösteriliyor' : ''}</span>}
        <span className="dbx-muted dbx-grow" style={{ textAlign: 'right' }}><TerminalSquare aria-hidden className="dbx-ic" /> Tablolar: {tables.map((t) => t.name).join(', ')}</span>
      </div>
      {err && <p className="dbx-err" role="alert">{err}</p>}
      {res && (
        <div className="dbx-tablewrap">
          <table className="dbx-table">
            <thead><tr>{res.fields.map((f, i) => <th key={i}><span>{f}</span></th>)}</tr></thead>
            <tbody>
              {res.rows.map((r, i) => (
                <tr key={i} onClick={() => { void navigator.clipboard?.writeText(r.map(show).join('\t')); notify('Satır panoya kopyalandı.'); }}>
                  {r.map((v, j) => <td key={j} className={v == null ? 'is-null' : ''}>{show(v).slice(0, 200)}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
