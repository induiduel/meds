import React, { startTransition, useEffect, useMemo, useRef, useState } from 'react';
import {
  Search, RefreshCw, Download, Copy, Link2, Mail, Pencil, Trash2, X, MoreHorizontal, ChevronLeft, ChevronRight, ArrowLeft,
  Shield, UserRound, ExternalLink,
} from 'lucide-react';
import type { PeopleList, PersonRow, PersonDetail } from '../../services/peopleService';
import { fmtDuration, relTime, personDeepLink, siteLink } from '../../services/peopleService';
import { deleteManageUser } from '../../services/manageConsoleService';
import { ConfirmButton } from '../manage/consoleUi';
import type { PeopleV12Parts, PeopleFilter, PeopleSort, PeopleTab } from '../manage/ManagePeopleSection';
import '../../styles/v12/manage.css';

/**
 * Yönetim › Kişiler — v12 "Net" denetim düzeni (canvas: ManageUsers.dc.html).
 * Kayıtlı görünüm hapları (mevcut süzgeçler), süzgeç çubuğu, seçimli tablo + toplu işlem çubuğu, sağda sekmeli ayrıntı.
 * Veri, canlı tazeleme ve adres (/manage/kisiler/<anahtar>?sekme=…) ManagePeopleSection'da kalır.
 * Uyar / kısıtla / askıya al / risk puanı için sunucu ucu yok: bu öğeler bilerek çizilmez.
 */

interface Props {
  list: PeopleList | null;
  listErr: string;
  rows: PersonRow[];
  filters: [PeopleFilter, string, number?][];
  filter: PeopleFilter;
  setFilter: (f: PeopleFilter) => void;
  query: string;
  setQuery: (q: string) => void;
  sort: PeopleSort;
  setSort: (s: PeopleSort) => void;
  pulse: number;
  onRefresh: () => void;
  openKey: string | null;
  tab: PeopleTab;
  open: (key: string | null, t?: PeopleTab) => void;
  setTab: (t: PeopleTab) => void;
  detail: PersonDetail | null;
  detailErr: string;
  loadingDetail: boolean;
  adminEmail: string;
  notify: (m: string) => void;
  reload: () => void;
  parts: PeopleV12Parts;
}

type RoleF = 'all' | 'student' | 'admin';
type SeenF = 'any' | '24h' | '7d' | 'old';
const PAGE = 50;
const DAY = 86_400_000;

const initial = (s?: string | null) => (s || '?').trim().charAt(0).toLocaleUpperCase('tr-TR') || '?';
const fmtDateTime = (iso?: string | null) =>
  iso ? new Date(iso).toLocaleString('tr-TR', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : '—';
const ageMs = (iso?: string | null) => {
  const t = iso ? new Date(iso).getTime() : NaN;
  return Number.isFinite(t) ? Date.now() - t : Infinity;
};
const roleOf = (p: { kind: string; role: string }) => (p.role === 'admin' ? 'Yönetici' : p.kind === 'guest' ? 'Misafir' : 'Öğrenci');
const roleCls = (p: { kind: string; role: string }) => (p.role === 'admin' ? 'm12-badge acc' : p.kind === 'guest' ? 'm12-role' : 'm12-badge');

const copyText = async (text: string, notify: (m: string) => void, msg: string) => {
  try {
    await navigator.clipboard.writeText(text);
    notify(msg);
  } catch {
    notify(text);
  }
};

const csvCell = (v: unknown) => {
  const s = v === null || v === undefined ? '' : String(v);
  return /[",;\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
};
const downloadCsv = (rows: PersonRow[], contrib: (r: PersonRow) => number) => {
  const head = ['Ad', 'E-posta', 'Öğrenci no', 'Telefon', 'Tür', 'Çevrimiçi', 'Son görülme', 'Kayıt', 'Kullanım (sn)', 'Son 7 gün (sn)', 'Cihaz', 'Katkı', 'Bildirim', 'Beğeni', 'Test', 'Doğruluk (%)', 'Anahtar'];
  const lines = rows.map((r) =>
    [r.name, r.email, r.studentNumber, r.phone, roleOf(r), r.online ? 'evet' : 'hayır', r.lastSeen, r.createdAt, r.totalSeconds, r.weekSeconds, r.deviceCount, contrib(r), r.counts.report, r.counts.like, r.testCount, r.accuracy, r.key]
      .map(csvCell)
      .join(','),
  );
  const blob = new Blob([`﻿${[head.join(','), ...lines].join('\n')}`], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `kisiler-${new Date().toLocaleDateString('sv-SE')}.csv`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
};

const Avatar: React.FC<{ name: string; photo?: string | null; online?: boolean; big?: boolean }> = ({ name, photo, online, big }) => (
  <span className={`m12-av ${big ? 'lg' : ''}`} aria-hidden="true">
    {photo ? <img src={photo} alt="" referrerPolicy="no-referrer" /> : <span>{initial(name)}</span>}
    {online && <i className="m12-av-dot" />}
  </span>
);

/** Yerli onay kutusu; "kısmen" durumu DOM özelliğiyle */
const Check: React.FC<{ checked: boolean; mixed?: boolean; onChange: () => void; label: string }> = ({ checked, mixed, onChange, label }) => {
  const ref = useRef<HTMLInputElement>(null);
  useEffect(() => {
    if (ref.current) ref.current.indeterminate = !!mixed && !checked;
  }, [mixed, checked]);
  return <input ref={ref} type="checkbox" className="m12-cb" checked={checked} onChange={onChange} aria-label={label} />;
};

export const ManagePeopleV12: React.FC<Props> = (p) => {
  const { list, rows, parts } = p;
  const [q, setQ] = useState(p.query);
  const [role, setRole] = useState<RoleF>('all');
  const [seen, setSeen] = useState<SeenF>('any');
  const [page, setPage] = useState(0);
  const [sel, setSel] = useState<Set<string>>(() => new Set());
  const [menu, setMenu] = useState<string | null>(null);

  const filtered = useMemo(
    () =>
      rows.filter((r) => {
        if (role === 'admin' && r.role !== 'admin') return false;
        if (role === 'student' && (r.role === 'admin' || r.kind !== 'account')) return false;
        if (seen !== 'any') {
          const a = r.online ? 0 : ageMs(r.lastSeen);
          if (seen === '24h' && a > DAY) return false;
          if (seen === '7d' && a > 7 * DAY) return false;
          if (seen === 'old' && a <= 30 * DAY) return false;
        }
        return true;
      }),
    [rows, role, seen],
  );
  useEffect(() => setPage(0), [p.filter, p.query, p.sort, role, seen]);
  const pages = Math.max(1, Math.ceil(filtered.length / PAGE));
  const pg = Math.min(page, pages - 1);
  const pageRows = filtered.slice(pg * PAGE, pg * PAGE + PAGE);

  // Seçim: görünmeyen (süzgeçle düşen) kişiler seçimden çıkar
  useEffect(() => {
    setSel((cur) => {
      if (!cur.size) return cur;
      const keep = new Set(filtered.map((r) => r.key));
      const next = new Set([...cur].filter((k) => keep.has(k)));
      return next.size === cur.size ? cur : next;
    });
  }, [filtered]);
  const selRows = useMemo(() => filtered.filter((r) => sel.has(r.key)), [filtered, sel]);
  const pageSel = pageRows.filter((r) => sel.has(r.key)).length;
  const allOn = pageRows.length > 0 && pageSel === pageRows.length;
  const toggleAll = () =>
    setSel((cur) => {
      const next = new Set(cur);
      if (allOn) pageRows.forEach((r) => next.delete(r.key));
      else pageRows.forEach((r) => next.add(r.key));
      return next;
    });
  const toggle = (k: string) =>
    setSel((cur) => {
      const next = new Set(cur);
      if (next.has(k)) next.delete(k);
      else next.add(k);
      return next;
    });

  // Satır menüsü: dışarı tıklayınca ya da Esc ile kapanır
  useEffect(() => {
    if (!menu) return;
    const onDown = (e: MouseEvent) => {
      if (!(e.target as HTMLElement).closest?.('.m12-rowmenu')) setMenu(null);
    };
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setMenu(null);
    document.addEventListener('mousedown', onDown);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDown);
      document.removeEventListener('keydown', onKey);
    };
  }, [menu]);

  const t = list?.totals;
  const dirty = !!q || role !== 'all' || seen !== 'any' || p.sort !== 'seen';
  const clear = () => {
    setQ('');
    p.setQuery('');
    setRole('all');
    setSeen('any');
    p.setSort('seen');
  };
  const emails = selRows.map((r) => r.email).filter(Boolean) as string[];

  return (
    <div className={`m12-pp ${p.openKey ? 'has-open' : ''}`}>
      <div className="m12-pp-split">
        <div className="m12-pp-list">
          <div className="m12-pp-row1">
            <div className="m12-chips" role="group" aria-label="Kayıtlı görünümler">
              {p.filters.map(([id, label, n]) => (
                <button key={id} type="button" className={`m12-pill ${p.filter === id ? 'on' : ''}`} aria-pressed={p.filter === id} onClick={() => p.setFilter(id)}>
                  <span>{label}</span>
                  {n !== undefined && <b className="m12-num">{n.toLocaleString('tr-TR')}</b>}
                </button>
              ))}
            </div>
            <span className="m12-grow" />
            <button type="button" className="m12-btn sm" onClick={() => downloadCsv(filtered, parts.contribTotal)} disabled={!filtered.length}>
              <Download aria-hidden="true" />
              Dışa aktar
            </button>
            <button type="button" className="m12-btn sm icon" onClick={p.onRefresh} aria-label="Listeyi yenile" title="Listeyi yenile">
              <RefreshCw key={p.pulse} className="m12-spin-once" aria-hidden="true" />
            </button>
          </div>

          <div className="m12-filters">
            <label className="m12-field m12-qs">
              <Search aria-hidden="true" />
              <span className="sr-only">Kişi ara</span>
              <input
                type="search"
                value={q}
                placeholder="Ad, e-posta, numara, cihaz…"
                onChange={(e) => {
                  const v = e.target.value;
                  setQ(v);
                  startTransition(() => p.setQuery(v));
                }}
              />
            </label>
            <label className="m12-field m12-f">
              <span className="fl">Rol</span>
              <select value={role} onChange={(e) => setRole(e.target.value as RoleF)}>
                <option value="all">Tümü</option>
                <option value="student">Öğrenci</option>
                <option value="admin">Yönetici</option>
              </select>
            </label>
            <label className="m12-field m12-f">
              <span className="fl">Son görülme</span>
              <select value={seen} onChange={(e) => setSeen(e.target.value as SeenF)}>
                <option value="any">Her zaman</option>
                <option value="24h">Son 24 saat</option>
                <option value="7d">Son 7 gün</option>
                <option value="old">30 günden eski</option>
              </select>
            </label>
            <label className="m12-field m12-f">
              <span className="fl">Sırala</span>
              <select value={p.sort} onChange={(e) => p.setSort(e.target.value as PeopleSort)}>
                <option value="seen">Son görülme</option>
                <option value="usage">Kullanım süresi</option>
                <option value="contrib">Katkı sayısı</option>
              </select>
            </label>
            {dirty && (
              <button type="button" className="m12-btn sm ghost" onClick={clear}>
                Temizle
              </button>
            )}
          </div>

          {list && !list.database && (
            <p className="m12-note warn">Veritabanı şu an bağlı değil: cihaz ve etkinlik verisi geçici olarak eksik; yazımlar kuyrukta bekliyor.</p>
          )}
          {p.listErr && <p className="m12-note bad">{p.listErr}</p>}

          <section className="m12-panel" aria-label="Kişiler">
            {selRows.length > 0 ? (
              <div className="m12-bar bulk" role="toolbar" aria-label="Toplu işlemler">
                <b>{selRows.length.toLocaleString('tr-TR')} seçili</b>
                <span className="m12-grow" />
                {emails.length > 0 && (
                  <button type="button" className="m12-btn sm" onClick={() => copyText(emails.join(', '), p.notify, `${emails.length} e-posta kopyalandı.`)}>
                    <Copy aria-hidden="true" />
                    E-postaları kopyala
                  </button>
                )}
                <button type="button" className="m12-btn sm" onClick={() => downloadCsv(selRows, parts.contribTotal)}>
                  <Download aria-hidden="true" />
                  Seçileni dışa aktar
                </button>
                <button type="button" className="m12-btn sm ghost" onClick={() => setSel(new Set())}>
                  Seçimi kaldır
                </button>
              </div>
            ) : (
              <div className="m12-bar">
                <span className="m12-meta m12-grow">
                  <span className="m12-num">{filtered.length.toLocaleString('tr-TR')}</span> kişi
                  {t ? (
                    <>
                      {' · '}
                      <span className="m12-num">{t.online}</span> çevrimiçi · <span className="m12-num">{t.devices}</span> cihaz · son 7 gün{' '}
                      <span className="m12-num">{fmtDuration(t.weekSeconds)}</span>
                    </>
                  ) : null}
                </span>
              </div>
            )}

            <div className="m12-tbl-box">
              <table className="m12-tbl m12-ptbl">
                <thead>
                  <tr>
                    <th className="c-cb">
                      <Check checked={allOn} mixed={pageSel > 0} onChange={toggleAll} label="Bu sayfadakilerin tümünü seç" />
                    </th>
                    <th>Kişi</th>
                    <th>Rol</th>
                    <th>Durum</th>
                    <th className="n">Katkı</th>
                    <th className="n">Bildirim</th>
                    <th className="n">Kullanım</th>
                    <th>Son görülme</th>
                    <th className="n">Cihaz</th>
                    <th className="c-act"><span className="sr-only">İşlemler</span></th>
                  </tr>
                </thead>
                <tbody>
                  {!list && !p.listErr && (
                    <tr>
                      <td colSpan={10} className="m12-td-empty" aria-busy="true">Yükleniyor…</td>
                    </tr>
                  )}
                  {list && pageRows.length === 0 && (
                    <tr>
                      <td colSpan={10} className="m12-td-empty">Eşleşen kişi yok. Süzgeci ya da aramayı değiştir.</td>
                    </tr>
                  )}
                  {pageRows.map((r, i) => {
                    const on = sel.has(r.key);
                    const cur = p.openKey === r.key;
                    const contrib = parts.contribTotal(r);
                    return (
                      <tr key={r.key} className={cur ? 'cur' : on ? 'sel' : ''}>
                        <td className="c-cb">
                          <Check checked={on} onChange={() => toggle(r.key)} label={`Seç: ${r.name}`} />
                        </td>
                        <td className="c-user">
                          <button type="button" className="m12-user" onClick={() => p.open(r.key)} aria-current={cur ? 'true' : undefined}>
                            <Avatar name={r.name} photo={r.photoURL} online={r.online} />
                            <span className="tx">
                              <span className="nm m12-clamp1">{r.name}</span>
                              <span className="em m12-clamp1">
                                {[r.email, r.studentNumber && `No ${r.studentNumber}`].filter(Boolean).join(' · ') || 'Girişsiz cihaz'}
                              </span>
                            </span>
                          </button>
                        </td>
                        <td><span className={roleCls(r)}>{roleOf(r)}</span></td>
                        <td>{r.online ? <span className="m12-badge ok">çevrimiçi</span> : <span className="m12-meta">çevrimdışı</span>}</td>
                        <td className="n"><span className="m12-num">{contrib}</span></td>
                        <td className="n"><span className={`m12-num ${r.counts.report ? 'warn' : ''}`}>{r.counts.report}</span></td>
                        <td className="n"><span className="m12-num">{fmtDuration(r.totalSeconds)}</span></td>
                        <td><span className="m12-meta">{r.online ? 'şimdi' : relTime(r.lastSeen)}</span></td>
                        <td className="n"><span className="m12-num">{r.deviceCount}</span></td>
                        <td className="c-act">
                          <div className="m12-rowmenu">
                            <button
                              type="button"
                              className="m12-btn sm ghost icon"
                              aria-label={`${r.name} için işlemler`}
                              aria-haspopup="menu"
                              aria-expanded={menu === r.key}
                              onClick={() => setMenu(menu === r.key ? null : r.key)}
                            >
                              <MoreHorizontal aria-hidden="true" />
                            </button>
                            {menu === r.key && (
                              <div className={`m12-pop m12-menu ${i >= pageRows.length - 3 && pageRows.length > 4 ? 'up' : ''}`} role="menu">
                                <button type="button" role="menuitem" onClick={() => { setMenu(null); p.open(r.key); }}>
                                  <UserRound aria-hidden="true" /> Profili aç
                                </button>
                                <button type="button" role="menuitem" onClick={() => { setMenu(null); void copyText(personDeepLink(r.key), p.notify, 'Kişi bağlantısı kopyalandı.'); }}>
                                  <Link2 aria-hidden="true" /> Bağlantıyı kopyala
                                </button>
                                {r.email && (
                                  <button type="button" role="menuitem" onClick={() => { setMenu(null); void copyText(r.email!, p.notify, 'E-posta kopyalandı.'); }}>
                                    <Copy aria-hidden="true" /> E-postayı kopyala
                                  </button>
                                )}
                              </div>
                            )}
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            <div className="m12-panel-f">
              <span className="m12-meta m12-grow">
                {filtered.length
                  ? `${(pg * PAGE + 1).toLocaleString('tr-TR')}–${Math.min(filtered.length, pg * PAGE + PAGE).toLocaleString('tr-TR')} / ${filtered.length.toLocaleString('tr-TR')}`
                  : '0 kişi'}
              </span>
              <button type="button" className="m12-btn sm icon" aria-label="Önceki sayfa" disabled={pg === 0} onClick={() => setPage(pg - 1)}>
                <ChevronLeft aria-hidden="true" />
              </button>
              <button type="button" className="m12-btn sm icon" aria-label="Sonraki sayfa" disabled={pg >= pages - 1} onClick={() => setPage(pg + 1)}>
                <ChevronRight aria-hidden="true" />
              </button>
            </div>
          </section>
        </div>

        {p.openKey && (
          <aside className="m12-panel m12-pp-drawer" aria-label="Kişi ayrıntısı">
            {p.detailErr && !p.detail && (
              <div className="m12-dsec">
                <button type="button" className="m12-btn sm" onClick={() => p.open(null)}><ArrowLeft aria-hidden="true" /> Listeye dön</button>
                <p className="m12-note bad">{p.detailErr}</p>
              </div>
            )}
            {!p.detail && !p.detailErr && <div className="m12-td-empty" aria-busy="true">{p.loadingDetail ? 'Yükleniyor…' : ''}</div>}
            {p.detail && <PersonDrawer key={p.detail.person.key} {...p} d={p.detail} />}
          </aside>
        )}
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------ */

const TABS: { id: PeopleTab; label: string }[] = [
  { id: 'ozet', label: 'Özet' },
  { id: 'etkinlik', label: 'Etkinlik' },
  { id: 'katkilar', label: 'Katkılar' },
  { id: 'bildirimler', label: 'Bildirimler' },
  { id: 'notlar', label: 'Notlar' },
  { id: 'skorlar', label: 'Skorlar' },
  { id: 'cihazlar', label: 'Cihazlar' },
];

const PersonDrawer: React.FC<Props & { d: PersonDetail }> = ({ d, tab, setTab, open, adminEmail, notify, reload, parts }) => {
  const pr = d.person;
  const [mode, setMode] = useState<'none' | 'mail' | 'edit'>('none');
  const online = d.devices.some((x) => x.online);
  const reports = d.items.filter((i) => i.kind === 'report');
  const contribs = d.items.filter((i) => ['comment', 'question', 'fragment', 'option', 'like', 'vote'].includes(i.kind));
  const notes = d.items.filter((i) => i.kind === 'note');
  const counts: Partial<Record<PeopleTab, number>> = {
    etkinlik: d.events.length + d.activityLog.length,
    katkilar: contribs.length,
    bildirimler: reports.length,
    notlar: notes.length,
    skorlar: d.score.testCount,
    cihazlar: d.devices.length,
  };
  const canDelete = !!pr.uid && pr.kind === 'account' && pr.role !== 'admin';

  return (
    <div className="m12-dr">
      <div className="m12-dh">
        <button type="button" className="m12-btn sm icon ghost m12-pp-back" onClick={() => open(null)} aria-label="Listeye dön">
          <ArrowLeft aria-hidden="true" />
        </button>
        <Avatar name={pr.name} photo={pr.photoURL} online={online} big />
        <div className="m12-dh-t">
          <h2 className="m12-h2 m12-clamp1">{pr.name}</h2>
          {pr.email && <a className="m12-meta m12-clamp1" href={`mailto:${pr.email}`}>{pr.email}</a>}
          <span className="m12-dh-b">
            <span className={roleCls(pr)}>{pr.role === 'admin' ? <><Shield aria-hidden="true" /> Yönetici</> : pr.kind === 'guest' ? 'Misafir cihaz' : 'Öğrenci'}</span>
            {online ? <span className="m12-badge ok">çevrimiçi</span> : <span className="m12-badge">çevrimdışı</span>}
            {pr.kind === 'account' && <span className={`m12-badge ${pr.verified ? '' : 'warn'}`}>{pr.verified ? 'doğrulanmış' : 'doğrulanmamış'}</span>}
          </span>
        </div>
        <button type="button" className="m12-btn sm icon ghost m12-dh-x" onClick={() => open(null)} aria-label="Ayrıntıyı kapat">
          <X aria-hidden="true" />
        </button>
      </div>

      <div className="m12-acts">
        <button type="button" className="m12-btn sm" onClick={() => copyText(personDeepLink(pr.key, tab), notify, 'Kişi bağlantısı kopyalandı.')}>
          <Link2 aria-hidden="true" /> Bağlantı
        </button>
        {pr.email && (
          <button type="button" className={`m12-btn sm ${mode === 'mail' ? 'is-on' : ''}`} aria-expanded={mode === 'mail'} onClick={() => setMode(mode === 'mail' ? 'none' : 'mail')}>
            <Mail aria-hidden="true" /> E-posta
          </button>
        )}
        {pr.uid && pr.kind === 'account' && (
          <button type="button" className={`m12-btn sm ${mode === 'edit' ? 'is-on' : ''}`} aria-expanded={mode === 'edit'} onClick={() => setMode(mode === 'edit' ? 'none' : 'edit')}>
            <Pencil aria-hidden="true" /> Düzenle
          </button>
        )}
        {canDelete && (
          <>
            <span className="m12-grow" />
            <span className="vr" aria-hidden="true" />
            <ConfirmButton
              className="m12-btn sm danger"
              confirmLabel="Evet, sil"
              icon={Trash2}
              title="Kullanıcı kaydı kalkar, katkıları kalır"
              onConfirm={async () => {
                const r = await deleteManageUser(adminEmail, pr.uid!);
                notify(r.message);
                if (r.ok) {
                  open(null);
                  reload();
                }
              }}
            >
              Hesabı sil
            </ConfirmButton>
          </>
        )}
      </div>

      {(mode === 'mail' || mode === 'edit') && (
        <div className="m12-dform">
          {mode === 'mail' && pr.email && <parts.MailBox to={pr.email} name={pr.name} notify={notify} onDone={() => setMode('none')} />}
          {mode === 'edit' && pr.uid && <parts.EditBox d={d} adminEmail={adminEmail} notify={notify} onDone={() => { setMode('none'); reload(); }} />}
        </div>
      )}

      <nav className="m12-tabs" role="tablist" aria-label="Kişi sekmeleri">
        {TABS.map((x) => (
          <button key={x.id} type="button" role="tab" aria-selected={tab === x.id} className={tab === x.id ? 'on' : ''} onClick={() => setTab(x.id)}>
            {x.label}
            {counts[x.id] ? <span className="m12-num">{counts[x.id]}</span> : null}
          </button>
        ))}
      </nav>

      <div className="m12-dbody" role="tabpanel">
        {tab === 'ozet' && <Summary d={d} setTab={setTab} parts={parts} />}
        {tab !== 'ozet' && (
          <div className="m12-dsec m12-pp-legacy">
            {tab === 'etkinlik' && <parts.Timeline d={d} reload={reload} notify={notify} />}
            {tab === 'katkilar' && <parts.ItemList items={contribs} adminEmail={adminEmail} notify={notify} reload={reload} empty="Yorum, soru, ipucu, şık ya da beğeni yok." filterable />}
            {tab === 'bildirimler' && <parts.ItemList items={reports} adminEmail={adminEmail} notify={notify} reload={reload} empty="Hata bildirimi ya da öneri yok." />}
            {tab === 'notlar' && <parts.ItemList items={notes} adminEmail={adminEmail} notify={notify} reload={reload} empty="Not yok." />}
            {tab === 'skorlar' && <parts.Scores d={d} />}
            {tab === 'cihazlar' && <parts.Devices d={d} notify={notify} reload={reload} />}
          </div>
        )}
      </div>
    </div>
  );
};

const Summary: React.FC<{ d: PersonDetail; setTab: (t: PeopleTab) => void; parts: PeopleV12Parts }> = ({ d, setTab, parts }) => {
  const pr = d.person;
  // Son 30 gün: cihaz sayacı (sunucu) ile uygulama sayacından (profil) büyüğü — Kişiler v10 özetiyle aynı hesap
  const days = useMemo(() => {
    const m = new Map<string, number>();
    for (const x of d.usage.studyDaily) m.set(x.day, x.seconds);
    for (const x of d.usage.daily) m.set(x.day, Math.max(m.get(x.day) || 0, x.seconds));
    const out: { day: string; seconds: number }[] = [];
    for (let i = 29; i >= 0; i--) {
      const key = new Date(Date.now() - i * DAY).toLocaleDateString('sv-SE', { timeZone: 'Europe/Istanbul' });
      out.push({ day: key, seconds: m.get(key) || 0 });
    }
    return out;
  }, [d]);
  const max = Math.max(60, ...days.map((x) => x.seconds));
  const week = days.slice(-7).reduce((a, x) => a + x.seconds, 0);
  const month = days.reduce((a, x) => a + x.seconds, 0);
  const recent = useMemo(() => parts.mergeTimeline(d).slice(0, 8), [d, parts]);
  const s = d.score;

  let lastDay = '';
  return (
    <>
      <section className="m12-dsec">
        <dl className="m12-dl">
          <dt>Kayıt</dt><dd>{fmtDateTime(pr.createdAt)}</dd>
          <dt>Son giriş</dt><dd>{relTime(pr.lastLoginAt || pr.lastBackupAt)}</dd>
          {pr.studentNumber && (<><dt>Öğrenci no</dt><dd className="m12-num">{pr.studentNumber}</dd></>)}
          {pr.phone && (<><dt>Telefon</dt><dd><a href={`tel:${pr.phone}`}>{pr.phone}</a></dd></>)}
          <dt>Cihazlar</dt>
          <dd>{d.devices.length ? d.devices.map((x) => x.label || 'Cihaz').join(', ') : '—'}</dd>
          <dt>Kullanım</dt>
          <dd>{fmtDuration(d.usage.totalSeconds)} <span className="m12-meta">· {d.usage.sessions || 0} oturum · son 7 gün {fmtDuration(week)}</span></dd>
          <dt>Test</dt>
          <dd>{s.testCount ? <>{s.testCount} test <span className="m12-meta">· {s.accuracy !== null ? `%${s.accuracy} doğru · net ${s.net}` : 'doğruluk yok'}</span></> : 'çözülmedi'}</dd>
          <dt>Çalışma</dt>
          <dd>{d.study.progress} ders · {d.study.review} hata defteri · {d.study.favorites} favori · {d.study.flashcards} kart</dd>
          {pr.uid && (<><dt>Kimlik</dt><dd className="m12-num m12-mono">{pr.uid}</dd></>)}
        </dl>
      </section>
      <section className="m12-dsec" aria-labelledby="m12-use-h">
        <div className="m12-dsec-h"><span id="m12-use-h" className="m12-grow">Günlük kullanım</span><span className="m12-meta">son 30 gün · {fmtDuration(month)}</span></div>
        <div className="m12-bars" role="img" aria-label={`Son 30 günde toplam ${fmtDuration(month)}`}>
          {days.map((x) => (
            <span key={x.day} title={`${new Date(x.day).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })}: ${fmtDuration(x.seconds)}`}>
              <i style={{ height: `${Math.max(x.seconds ? 4 : 0, (x.seconds / max) * 100)}%` }} />
            </span>
          ))}
        </div>
      </section>
      <section className="m12-dsec" aria-labelledby="m12-tl-h">
        <div className="m12-dsec-h">
          <span id="m12-tl-h" className="m12-grow">Son etkinlik</span>
          <button type="button" className="m12-btn sm ghost" onClick={() => setTab('etkinlik')}>Tümü <ChevronRight aria-hidden="true" /></button>
        </div>
        {recent.length === 0 ? (
          <p className="m12-meta">Henüz kayıt yok.</p>
        ) : (
          <div className="m12-tl">
            {recent.map((r) => {
              const day = new Date(r.at).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' });
              const head = day !== lastDay ? day : '';
              lastDay = day;
              return (
                <React.Fragment key={r.id}>
                  {head && <span className="m12-day">{head}</span>}
                  <span className="tm">{new Date(r.at).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })}</span>
                  <span className="ev">
                    <span className="m12-clamp1">{r.label}{r.device ? <span className="m12-meta"> · {r.device}</span> : null}</span>
                    {r.link && (
                      <a href={siteLink(r.link)} target="_blank" rel="noreferrer" aria-label={`${r.label}: sitede aç`}>
                        <ExternalLink aria-hidden="true" />
                      </a>
                    )}
                  </span>
                </React.Fragment>
              );
            })}
          </div>
        )}
      </section>
    </>
  );
};
