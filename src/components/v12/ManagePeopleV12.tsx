import React, { startTransition, useEffect, useMemo, useState } from 'react';
import { RefreshCw, Download, Link2, Mail, Pencil, Trash2, ChevronLeft, ChevronRight, Shield, ExternalLink } from 'lucide-react';
import type { PeopleList, PersonRow, PersonDetail } from '../../services/peopleService';
import { fmtDuration, relTime, personDeepLink, siteLink } from '../../services/peopleService';
import { deleteManageUser, sendUserEmail } from '../../services/manageConsoleService';
import { ConfirmButton, Drawer } from '../manage/consoleUi';
import { PageActions, StatRow, Toolbar, Tabs14, SearchField, DataTable, Pill, DetailNav, Card14, type Col } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';
import type { PeopleV12Parts, PeopleFilter, PeopleSort, PeopleTab } from '../manage/ManagePeopleSection';
import { AccessBulkDrawer, AccessPills, AccessSection, useUserAccess, type UserAccessApi } from '../manage/UserAccessControls';
import '../../styles/v12/manage.css';

/**
 * Yönetim › Kişiler — v14 düzeni (canvas: Kisiler.dc.html): sayılar, görünüm sekmeleri + arama, toplu işlem çubuğu, seçimli tablo;
 * satıra tıklayınca tam sayfa 360° profil (Drawer, önceki/sonraki). Toplu e-posta tek e-posta işlevini sırayla çağırır.
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

type RoleF = 'all' | 'student' | 'moderator' | 'admin' | 'suspended';
const OWNER = 'nofrostlife@gmail.com';
const isOwnerEmail = (e?: string | null) => (e || '').toLowerCase() === OWNER;
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
const roleOf = (p: { kind: string; role: string; agent?: string }) =>
  p.role === 'admin' ? 'Yönetici' : p.agent === 'bot' ? 'Bot' : p.agent === 'otomasyon' ? 'Otomasyon' : p.agent === 'bos' ? 'Boş kayıt' : p.kind === 'guest' ? 'Misafir' : 'Öğrenci';

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
  const head = ['Ad', 'E-posta', 'Öğrenci no', 'Telefon', 'Tür', 'Çevrimiçi', 'Son görülme', 'Kayıt', 'Kullanım (sn)', 'Son 7 gün (sn)', 'Çalışma (sn)', 'Çalışma 7 gün (sn)', 'Çalışılan konu', 'Biten konu', 'Cihaz', 'Katkı', 'Bildirim', 'Beğeni', 'Test', 'Doğruluk (%)', 'Anahtar'];
  const lines = rows.map((r) =>
    [r.name, r.email, r.studentNumber, r.phone, roleOf(r), r.online ? 'evet' : 'hayır', r.lastSeen, r.createdAt, r.totalSeconds, r.weekSeconds, r.study?.sn ?? '', r.study?.haftaSn ?? '', r.study?.konu ?? '', r.study?.bitti ?? '', r.deviceCount, contrib(r), r.counts.report, r.counts.like, r.testCount, r.accuracy, r.key]
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

export const ManagePeopleV12: React.FC<Props> = (p) => {
  const { list, rows, parts } = p;
  const [q, setQ] = useState(p.query);
  const [role, setRole] = useState<RoleF>('all');
  const [seen, setSeen] = useState<SeenF>('any');
  const [page, setPage] = useState(0);
  const sel = useSelection<string>();
  const [bulkMail, setBulkMail] = useState(false);
  const [busy, setBusy] = useState(false);
  const access = useUserAccess(p.notify);
  const [accessBulk, setAccessBulk] = useState<null | 'role' | 'suspend'>(null);
  const accOf = (r: PersonRow) => (r.uid ? access.map[r.uid] : undefined);

  const filtered = useMemo(
    () =>
      rows.filter((r) => {
        const acc = accOf(r);
        const rr = isOwnerEmail(r.email) ? 'admin' : acc?.role || (r.role === 'admin' ? 'admin' : 'student');
        if (role === 'suspended' && !acc?.suspended) return false;
        if (role === 'admin' && rr !== 'admin') return false;
        if (role === 'moderator' && rr !== 'moderator') return false;
        if (role === 'student' && (rr !== 'student' || r.kind !== 'account')) return false;
        if (seen !== 'any') {
          const a = r.online ? 0 : ageMs(r.lastSeen);
          if (seen === '24h' && a > DAY) return false;
          if (seen === '7d' && a > 7 * DAY) return false;
          if (seen === 'old' && a <= 30 * DAY) return false;
        }
        return true;
      }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [rows, role, seen, access.map],
  );
  useEffect(() => setPage(0), [p.filter, p.query, p.sort, role, seen]);
  const pages = Math.max(1, Math.ceil(filtered.length / PAGE));
  const pg = Math.min(page, pages - 1);
  const pageRows = filtered.slice(pg * PAGE, pg * PAGE + PAGE);

  const selRows = useMemo(() => filtered.filter((r) => sel.has(r.key)), [filtered, sel.sel]); // eslint-disable-line react-hooks/exhaustive-deps
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
  const deletable = selRows.filter((r) => r.uid && r.kind === 'account' && r.role !== 'admin');
  const accessable = selRows.filter((r) => r.uid && r.kind === 'account' && !isOwnerEmail(r.email));
  const unsuspendable = accessable.filter((r) => accOf(r)?.suspended);
  const bulkUnsuspend = async () => {
    setBusy(true);
    try {
      if (await access.unsuspend(unsuspendable.map((r) => r.uid!))) sel.clear();
    } finally {
      setBusy(false);
    }
  };
  const current = p.openKey ? filtered.find((r) => r.key === p.openKey) || rows.find((r) => r.key === p.openKey) || null : null;

  const bulkDelete = async () => {
    setBusy(true);
    let ok = 0;
    let bad = 0;
    for (const r of deletable) {
      const res = await deleteManageUser(p.adminEmail, r.uid!);
      if (res.ok) ok++;
      else bad++;
    }
    setBusy(false);
    p.notify(`${ok} başarılı, ${bad} hata.`);
    sel.clear();
    p.reload();
  };

  const cols: Col<PersonRow>[] = [
    {
      key: 'user',
      label: 'Kişi',
      main: true,
      render: (r) => (
        <span className="m12-user" style={{ pointerEvents: 'none' }}>
          <Avatar name={r.name} photo={r.photoURL} online={r.online} />
          <span className="m12-user-tx">
            <span className="nm m12-clamp1">{r.name}</span>
            <span className="em m12-clamp1">{parts.personSubline(r)}</span>
          </span>
        </span>
      ),
    },
    { key: 'role', label: 'Rol', render: (r) => (r.kind === 'account' ? <AccessPills access={accOf(r)} fallbackRole={r.role} owner={isOwnerEmail(r.email)} /> : <Pill>{roleOf(r)}</Pill>) },
    { key: 'state', label: 'Durum', render: (r) => (r.online ? <Pill tone="ok">Çevrim içi</Pill> : <Pill>Çevrim dışı</Pill>) },
    { key: 'contrib', label: 'Katkı', right: true, render: (r) => parts.contribTotal(r) },
    { key: 'report', label: 'Bildirim', right: true, render: (r) => r.counts.report },
    { key: 'use', label: 'Kullanım', right: true, render: (r) => fmtDuration(r.totalSeconds) },
    {
      key: 'study',
      label: 'Çalışma',
      right: true,
      render: (r) =>
        r.study?.konu ? (
          <button type="button" className="m12-linkbtn" onClick={(e) => { e.stopPropagation(); p.open(r.key, 'calisma'); }} title={`${r.study.konu} konu · son 7 gün ${fmtDuration(r.study.haftaSn)}`}>
            {fmtDuration(r.study.sn)} · {r.study.bitti} bitti
          </button>
        ) : '—',
    },
    { key: 'seen', label: 'Son görülme', muted: true, render: (r) => (r.online ? 'şimdi' : relTime(r.lastSeen)) },
    { key: 'dev', label: 'Cihaz', right: true, render: (r) => r.deviceCount },
  ];

  return (
    <div className="m12-pp">
      <PageActions
        note={
          <span>
            <span className="m12-av-dot" style={{ position: 'static', display: 'inline-block', marginRight: 6 }} aria-hidden="true" />
            Şu an çevrim içi: {t?.online ?? '—'}
          </span>
        }
      >
        <button type="button" className="m14-btn" onClick={() => downloadCsv(filtered, parts.contribTotal)} disabled={!filtered.length}>
          <Download aria-hidden="true" /> Dışa aktar
        </button>
        <button type="button" className="m14-btn" onClick={p.onRefresh} aria-label="Listeyi yenile">
          <RefreshCw key={p.pulse} className="m12-spin-once" aria-hidden="true" /> Yenile
        </button>
      </PageActions>

      <StatRow
        stats={[
          { label: 'Kişi', value: t?.people ?? '—' },
          { label: 'Şu an çevrim içi', value: t?.online ?? '—', tone: 'ok', onClick: () => p.setFilter('online') },
          { label: 'Cihaz', value: t?.devices ?? '—' },
          { label: 'Son 7 gün', value: t ? fmtDuration(t.weekSeconds) : '—' },
        ]}
      />

      <Toolbar>
        <Tabs14 label="Kayıtlı görünümler" value={p.filter} onChange={p.setFilter} options={p.filters.map(([id, label, n]) => ({ id, label, n }))} />
        <SearchField
          value={q}
          onChange={(v) => {
            setQ(v);
            startTransition(() => p.setQuery(v));
          }}
          placeholder="Ad, e-posta, numara, cihaz…"
          label="Kişi ara"
        />
        <select className="m14-select" value={role} onChange={(e) => setRole(e.target.value as RoleF)} aria-label="Rol">
          <option value="all">Her rol</option>
          <option value="student">Öğrenci</option>
          <option value="moderator">Moderatör</option>
          <option value="admin">Yönetici</option>
          <option value="suspended">Askıdakiler</option>
        </select>
        <select className="m14-select" value={seen} onChange={(e) => setSeen(e.target.value as SeenF)} aria-label="Son görülme">
          <option value="any">Her zaman</option>
          <option value="24h">Son 24 saat</option>
          <option value="7d">Son 7 gün</option>
          <option value="old">30 günden eski</option>
        </select>
        <select className="m14-select" value={p.sort} onChange={(e) => p.setSort(e.target.value as PeopleSort)} aria-label="Sırala">
          <option value="seen">Son görülmeye göre</option>
          <option value="usage">Kullanım süresine göre</option>
          <option value="study">Çalışma süresine göre</option>
          <option value="contrib">Katkı sayısına göre</option>
        </select>
        {dirty && <button type="button" className="m14-btn ghost" onClick={clear}>Temizle</button>}
      </Toolbar>

      {list && !list.database && <p className="m12-note warn">Veritabanı şu an bağlı değil: cihaz ve etkinlik verisi geçici olarak eksik; yazımlar kuyrukta bekliyor.</p>}
      {p.listErr && <p className="m12-note bad">{p.listErr}</p>}

      <BulkBar
        count={selRows.length}
        noun="kişi"
        busy={busy}
        onClear={sel.clear}
        actions={[
          { label: 'E-posta gönder', kind: 'main', disabled: !emails.length, run: () => setBulkMail(true) },
          { label: 'E-postaları kopyala', disabled: !emails.length, run: () => copyText(emails.join(', '), p.notify, `${emails.length} e-posta kopyalandı.`) },
          { label: 'Seçileni dışa aktar', run: () => downloadCsv(selRows, parts.contribTotal) },
          { label: `Rol değiştir (${accessable.length})`, disabled: !accessable.length, run: () => setAccessBulk('role') },
          { label: `Askıya al (${accessable.length})`, disabled: !accessable.length, run: () => setAccessBulk('suspend') },
          { label: `Askıyı kaldır (${unsuspendable.length})`, kind: 'danger', disabled: !unsuspendable.length, confirm: `${unsuspendable.length} hesabın askısını kaldırmayı onayla`, run: bulkUnsuspend },
          { label: `Hesapları sil (${deletable.length})`, kind: 'danger', disabled: !deletable.length, confirm: `${deletable.length} hesabı silmeyi onayla`, run: bulkDelete },
        ]}
      />

      <DataTable
        rows={pageRows}
        cols={cols}
        rowKey={(r) => r.key}
        onOpen={(r) => p.open(r.key)}
        selection={sel}
        activeKey={p.openKey}
        busy={!list && !p.listErr}
        empty={!list ? 'Yükleniyor…' : 'Eşleşen kişi yok. Süzgeci ya da aramayı değiştir.'}
        minWidth={900}
      />
      <div className="pk14-actions">
        <p className="pk14-note">
          {filtered.length
            ? `${(pg * PAGE + 1).toLocaleString('tr-TR')}–${Math.min(filtered.length, pg * PAGE + PAGE).toLocaleString('tr-TR')} / ${filtered.length.toLocaleString('tr-TR')}`
            : '0 kişi'}
        </p>
        <div className="pk14-actions-btns">
          <button type="button" className="m14-btn icon" aria-label="Önceki sayfa" disabled={pg === 0} onClick={() => setPage(pg - 1)}><ChevronLeft aria-hidden="true" /></button>
          <button type="button" className="m14-btn icon" aria-label="Sonraki sayfa" disabled={pg >= pages - 1} onClick={() => setPage(pg + 1)}><ChevronRight aria-hidden="true" /></button>
        </div>
      </div>

      <AccessBulkDrawer
        mode={accessBulk}
        uids={accessable.map((r) => r.uid!)}
        names={accessable.map((r) => r.name || r.email || '')}
        api={access}
        onClose={() => setAccessBulk(null)}
        onDone={() => {
          setAccessBulk(null);
          sel.clear();
        }}
      />

      <BulkMail open={bulkMail} onClose={() => setBulkMail(false)} rows={selRows.filter((r) => r.email)} notify={p.notify} />

      <Drawer
        open={!!p.openKey}
        onClose={() => p.open(null)}
        title={p.detail?.person.name || current?.name || 'Kişi'}
        label="Kişi profili"
        wide
        head={<DetailNav list={filtered} current={current} same={(a, b) => a.key === b.key} onGo={(r) => p.open(r.key, p.tab)} />}
      >
        {p.detailErr && !p.detail && <p className="m12-note bad">{p.detailErr}</p>}
        {!p.detail && !p.detailErr && <div className="m12-td-empty" aria-busy="true">{p.loadingDetail ? 'Yükleniyor…' : ''}</div>}
        {p.detail && <PersonDrawer key={p.detail.person.key} {...p} d={p.detail} access={access} />}
      </Drawer>
    </div>
  );
};

/** Toplu e-posta: her kişiye mevcut tek e-posta işleviyle sırayla; yalnız "Gönder" düğmesiyle başlar */
const BulkMail: React.FC<{ open: boolean; onClose: () => void; rows: PersonRow[]; notify: (m: string) => void }> = ({ open, onClose, rows, notify }) => {
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('Merhaba {ad},\n\n');
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(0);
  const send = async () => {
    if (!subject.trim() || !body.trim() || !rows.length) return;
    setBusy(true);
    setDone(0);
    let ok = 0;
    let bad = 0;
    for (const r of rows) {
      const res = await sendUserEmail(r.email!, subject.trim(), body.replace(/\{ad\}/g, r.name || ''));
      if (res.ok) ok++;
      else bad++;
      setDone(ok + bad);
    }
    setBusy(false);
    notify(`${ok} başarılı, ${bad} hata.`);
    if (!bad) onClose();
  };
  return (
    <Drawer
      open={open}
      onClose={() => !busy && onClose()}
      title={`Toplu e-posta · ${rows.length} kişi`}
      foot={
        <>
          <button type="button" className="m14-btn ghost" onClick={onClose} disabled={busy}>Vazgeç</button>
          <button type="button" className="m14-btn primary" onClick={() => void send()} disabled={busy || !subject.trim() || !body.trim() || !rows.length}>
            <Mail aria-hidden="true" /> {busy ? `Gönderiliyor… ${done} / ${rows.length}` : `${rows.length} kişiye gönder`}
          </button>
        </>
      }
    >
      <Card14 title="İleti">
        <div className="pp-form">
          <input value={subject} onChange={(e) => setSubject(e.target.value)} placeholder="Konu" aria-label="Konu" />
          <textarea value={body} onChange={(e) => setBody(e.target.value)} rows={8} aria-label="İleti" />
          <p className="pk14-note">{'{ad}'} her kişinin adıyla değiştirilir. İletiler sırayla tek tek gönderilir.</p>
        </div>
      </Card14>
      <Card14 title="Alıcılar">
        <p className="m12-meta">{rows.map((r) => r.email).join(', ') || 'E-postası olan kişi seçilmedi.'}</p>
      </Card14>
    </Drawer>
  );
};

/* ------------------------------------------------------------------ */

const TABS: { id: PeopleTab; label: string }[] = [
  { id: 'ozet', label: 'Özet' },
  { id: 'calisma', label: 'Çalışma' },
  { id: 'etkinlik', label: 'Etkinlik' },
  { id: 'katkilar', label: 'Katkılar' },
  { id: 'bildirimler', label: 'Bildirimler' },
  { id: 'notlar', label: 'Notlar' },
  { id: 'skorlar', label: 'Skorlar' },
  { id: 'cihazlar', label: 'Cihazlar' },
];

const PersonDrawer: React.FC<Props & { d: PersonDetail; access: UserAccessApi }> = ({ d, tab, setTab, open, adminEmail, notify, reload, parts, access }) => {
  const pr = d.person;
  const [mode, setMode] = useState<'none' | 'mail' | 'edit' | 'access'>('none');
  const acc = pr.uid ? access.map[pr.uid] : undefined;
  const online = d.devices.some((x) => x.online);
  const reports = d.items.filter((i) => i.kind === 'report');
  const contribs = d.items.filter((i) => ['comment', 'question', 'fragment', 'option', 'like', 'vote'].includes(i.kind));
  const notes = d.items.filter((i) => i.kind === 'note');
  const counts: Partial<Record<PeopleTab, number>> = {
    calisma: d.calisma?.konular.length || 0,
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
        <Avatar name={pr.name} photo={pr.photoURL} online={online} big />
        <div className="m12-dh-t">
          <h2 className="m12-h2 m12-clamp1">{pr.name}</h2>
          {pr.email && <a className="m12-meta m12-clamp1" href={`mailto:${pr.email}`}>{pr.email}</a>}
          <span className="m12-dh-b">
            <Pill tone={pr.role === 'admin' ? 'acc' : ''}>{pr.role === 'admin' ? <><Shield aria-hidden="true" /> Yönetici</> : pr.kind === 'guest' ? 'Misafir cihaz' : 'Öğrenci'}</Pill>
            {online ? <Pill tone="ok">Çevrim içi</Pill> : <Pill>Çevrim dışı</Pill>}
            {acc?.role === 'moderator' && <Pill tone="ok">Moderatör</Pill>}
            {acc?.suspended && <Pill tone="bad">Askıda</Pill>}
            {pr.kind === 'account' && <Pill tone={pr.verified ? '' : 'warn'}>{pr.verified ? 'Doğrulanmış' : 'Doğrulanmamış'}</Pill>}
          </span>
        </div>
      </div>

      <div className="pk14-actions">
        <div className="pk14-actions-btns">
          <button type="button" className="m14-btn" onClick={() => copyText(personDeepLink(pr.key, tab), notify, 'Kişi bağlantısı kopyalandı.')}>
            <Link2 aria-hidden="true" /> Bağlantı
          </button>
          {pr.email && (
            <button type="button" className={`m14-btn ${mode === 'mail' ? 'primary' : ''}`} aria-expanded={mode === 'mail'} onClick={() => setMode(mode === 'mail' ? 'none' : 'mail')}>
              <Mail aria-hidden="true" /> E-posta gönder
            </button>
          )}
          {pr.uid && pr.kind === 'account' && (
            <button type="button" className={`m14-btn ${mode === 'edit' ? 'primary' : ''}`} aria-expanded={mode === 'edit'} onClick={() => setMode(mode === 'edit' ? 'none' : 'edit')}>
              <Pencil aria-hidden="true" /> Düzenle
            </button>
          )}
          {pr.uid && pr.kind === 'account' && (
            <button type="button" className={`m14-btn ${mode === 'access' ? 'primary' : ''}`} aria-expanded={mode === 'access'} onClick={() => setMode(mode === 'access' ? 'none' : 'access')}>
              <Shield aria-hidden="true" /> {acc?.suspended ? 'Askıyı yönet' : 'Rol ve askı'}
            </button>
          )}
          {canDelete && (
            <ConfirmButton
              className="m14-btn danger"
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
          )}
        </div>
      </div>

      {mode === 'access' && pr.uid && (
        <div className="m12-dform">
          <AccessSection uid={pr.uid} email={pr.email || undefined} owner={isOwnerEmail(pr.email)} api={access} />
        </div>
      )}
      {(mode === 'mail' || mode === 'edit') && (
        <div className="m12-dform">
          {mode === 'mail' && pr.email && <parts.MailBox to={pr.email} name={pr.name} notify={notify} onDone={() => setMode('none')} />}
          {mode === 'edit' && pr.uid && <parts.EditBox d={d} adminEmail={adminEmail} notify={notify} onDone={() => { setMode('none'); reload(); }} />}
        </div>
      )}

      <Tabs14 label="Profil bölümleri" value={tab} onChange={setTab} options={TABS.map((x) => ({ id: x.id, label: x.label, n: counts[x.id] || undefined }))} />

      <div className="m12-dbody" role="tabpanel">
        {tab === 'ozet' && <Summary d={d} setTab={setTab} parts={parts} />}
        {tab !== 'ozet' && (
          <div className="m12-dsec m12-pp-legacy">
            {tab === 'calisma' && <parts.PersonStudy d={d} reload={reload} notify={notify} />}
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
