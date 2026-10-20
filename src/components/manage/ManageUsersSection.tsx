import React, { useMemo, useState } from 'react';
import { Mail, Trash2, ShieldCheck, Send, Users, Eraser, ArrowLeft, Bell } from 'lucide-react';
import type { Committee, QuestionItem } from '../../types';
import {
  InboxReport,
  InboxComment,
  UserActivityRow,
  ManageUser,
  normKey,
  sendUserEmail,
  sendAdminNotification,
  deleteManageUser,
  purgeAuthorContributions,
} from '../../services/manageConsoleService';
import { EmptyState, Seg, ConfirmButton, Drawer, Field } from './consoleUi';
import { PageActions, StatRow, Toolbar, Tabs14, SearchField, DataTable, Pill, DetailNav, type Col } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';

/**
 * Kullanıcılar (v14, canvas Kullanicilar.dc.html): sayılar → sekme + arama → toplu işlem → seçimli tablo.
 * Satıra dokununca ayrıntı tam sayfa çalışma alanında açılır (önceki/sonraki); e-posta ve bildirim de oradan.
 * Toplu e-posta / bildirim / silme tekil işlevleri sırayla çağırır ve yalnız "Gönder" ya da onayla başlar.
 */
interface Props {
  adminEmail: string;
  committees: Committee[];
  questions: QuestionItem[];
  pastQuestions: QuestionItem[];
  reports: InboxReport[];
  comments: InboxComment[];
  registeredUsers: ManageUser[];
  setRegisteredUsers: React.Dispatch<React.SetStateAction<ManageUser[]>>;
  activity: UserActivityRow[];
  notify: (msg: string) => void;
  onRefreshData: () => Promise<void>;
  reloadInbox: () => Promise<void>;
}

const OWNER = 'nofrostlife@gmail.com';
const fmtDate = (s?: string) => (s ? new Date(s).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', year: 'numeric' }) : '—');
const initial = (s?: string) => (s || '?').trim().charAt(0).toLocaleUpperCase('tr-TR') || '?';

export const ManageUsersSection: React.FC<Props> = ({
  adminEmail,
  committees,
  questions,
  pastQuestions,
  reports,
  comments,
  registeredUsers,
  setRegisteredUsers,
  activity,
  notify,
  onRefreshData,
  reloadInbox,
}) => {
  const [tab, setTab] = useState<'registered' | 'activity'>('registered');
  const [query, setQuery] = useState('');
  const [openKey, setOpenKey] = useState<string | null>(null);
  const [mode, setMode] = useState<'detail' | 'mail' | 'notify'>('detail');
  const [notifTarget, setNotifTarget] = useState<'single' | 'all'>('single');
  const [notifTitle, setNotifTitle] = useState('');
  const [notifMessage, setNotifMessage] = useState('');
  const [notifType, setNotifType] = useState<'app_info' | 'app_success' | 'app_error'>('app_info');
  const [notifUrl, setNotifUrl] = useState('/');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [sending, setSending] = useState(false);
  const [busy, setBusy] = useState<string | null>(null);
  const regSel = useSelection<string>();
  const actSel = useSelection<string>();
  const [bulk, setBulk] = useState<null | 'mail' | 'notify'>(null);
  const [bulkBusy, setBulkBusy] = useState(false);
  const [bulkDone, setBulkDone] = useState(0);

  const isOwner = (email?: string) => {
    const e = (email || '').toLowerCase();
    return !!e && (e === adminEmail.toLowerCase() || e === OWNER);
  };
  const regOf = (key: string) =>
    registeredUsers.find(
      (r) => (r.email && normKey(r.email) === key) || (r.uid && normKey(r.uid) === key) || (r.displayName && normKey(r.displayName) === key),
    );

  const q = query.toLocaleLowerCase('tr-TR').trim();
  const regRows = useMemo(
    () =>
      !q
        ? registeredUsers
        : registeredUsers.filter((u) => [u.displayName, u.email, u.studentNumber, u.uid].join(' ').toLocaleLowerCase('tr-TR').includes(q)),
    [registeredUsers, q],
  );
  const actRows = useMemo(
    () => (!q ? activity : activity.filter((u) => [u.name, u.email].join(' ').toLocaleLowerCase('tr-TR').includes(q))),
    [activity, q],
  );
  const admins = registeredUsers.filter((u) => u.role === 'admin' || isOwner(u.email)).length;

  const open = (key: string, m: 'detail' | 'mail' | 'notify' = 'detail', target: 'single' | 'all' = 'single') => {
    setOpenKey(key === '__ALL__' ? '__ALL__' : normKey(key));
    setMode(m);
    setNotifTarget(target);
    if (m === 'mail') {
      setSubject('');
      setBody('');
    }
    if (m === 'notify') {
      setNotifTitle('');
      setNotifMessage('');
      setNotifType('app_info');
      setNotifUrl('/');
    }
  };

  // --- Çekmecedeki kişi ---
  const sel = useMemo(() => {
    if (!openKey) return null;
    if (openKey === '__ALL__') {
      return {
        key: '__ALL__',
        reg: null,
        act: null,
        name: 'Tüm Kullanıcılar',
        email: 'Tüm Kayıtlı & Aktif Profiller (Broadcast)',
        studentNumber: '',
        userQuestions: [],
        userRevisions: [],
        fragments: [],
        userReports: [],
        userComments: [],
      };
    }
    const reg = regOf(openKey);
    const regKeys = reg ? [reg.email, reg.uid, reg.displayName].filter(Boolean).map((x) => normKey(x)) : [];
    const act = activity.find((x) => x.key === openKey || regKeys.includes(x.key) || (reg?.email && x.email && normKey(x.email) === normKey(reg.email)));
    const key = act?.key || openKey;
    const all = [...questions, ...pastQuestions];
    const userQuestions = all
      .filter((x) => normKey(x.contributedByUid || x.contributedByName) === key || (x.fragments || []).some((f) => normKey(f.authorUid || f.author) === key))
      .slice(0, 20);
    const fragments: { label: string; text: string }[] = [];
    for (const x of all) {
      for (const f of x.fragments || []) {
        if (normKey(f.authorUid || f.author) === key) fragments.push({ label: `S.${x.questionNumber || '?'} · ${x.topic || x.discipline}`, text: f.text });
      }
      if (fragments.length >= 15) break;
    }
    const userRevisions: { questionLabel: string; changeSummary: string; date: string; version: number }[] = [];
    for (const x of all) {
      for (const rev of x.revisions || []) {
        if (normKey(rev.editorUid || rev.editorName) === key) {
          userRevisions.push({
            questionLabel: `S.${x.questionNumber || '?'} · ${x.topic || x.discipline || 'Soru'}`,
            changeSummary: rev.changeSummary || 'Düzenleme',
            date: fmtDate(rev.editedAt),
            version: rev.version,
          });
        }
      }
    }
    return {
      key,
      reg,
      act,
      name: reg?.displayName || act?.name || reg?.email || openKey,
      email: reg?.email || act?.email,
      studentNumber: reg?.studentNumber || act?.studentNumber,
      userQuestions,
      userRevisions,
      fragments,
      userReports: reports.filter((r) => normKey(r.reportedBy) === key).slice(0, 20),
      userComments: comments.filter((c) => normKey(c.author) === key).slice(0, 20),
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [openKey, registeredUsers, activity, questions, pastQuestions, reports, comments]);

  const deleteAccount = async (uid: string | undefined, email: string | undefined, key: string) => {
    if (!uid) {
      notify('Bu kullanıcının kimlik (UID) bilgisi bulunamadı; yalnızca katkı izi olabilir.');
      return;
    }
    if (isOwner(email)) {
      notify('Ana yönetici hesabı silinemez.');
      return;
    }
    setBusy(`del-${key}`);
    try {
      const res = await deleteManageUser(adminEmail, uid);
      if (res.ok) {
        setRegisteredUsers((prev) => prev.filter((r) => r.uid !== uid && (!email || r.email?.toLowerCase() !== email.toLowerCase())));
        if (openKey === key || openKey === normKey(uid)) setOpenKey(null);
      }
      notify(res.message);
    } finally {
      setBusy(null);
    }
  };

  const purge = async (key: string) => {
    setBusy(`purge-${key}`);
    try {
      const res = await purgeAuthorContributions(committees, key);
      notify(res.message);
      if (res.ok) {
        if (openKey === key) setOpenKey(null);
        await onRefreshData();
        await reloadInbox();
      }
    } finally {
      setBusy(null);
    }
  };

  const sendMail = async () => {
    const to = sel?.email || '';
    if (!to || !subject.trim() || !body.trim()) {
      notify('Alıcı, konu ve mesaj zorunludur.');
      return;
    }
    setSending(true);
    try {
      const res = await sendUserEmail(to, subject.trim(), body.trim());
      notify(res.message);
      if (res.ok) {
        setSubject('');
        setBody('');
        setMode('detail');
      }
    } finally {
      setSending(false);
    }
  };

  const sendNotification = async () => {
    if (!notifTitle.trim() || !notifMessage.trim()) {
      notify('Bildirim başlığı ve mesajı zorunludur.');
      return;
    }
    setSending(true);
    try {
      const res = await sendAdminNotification(adminEmail, {
        target: notifTarget,
        targetUser: notifTarget === 'single' ? { uid: sel?.reg?.uid, email: sel?.email } : undefined,
        title: notifTitle.trim(),
        message: notifMessage.trim(),
        type: notifType,
        deepLinkUrl: notifUrl.trim() || '/',
      });
      notify(res.message);
      if (res.ok) {
        setNotifTitle('');
        setNotifMessage('');
        setMode('detail');
        if (notifTarget === 'all') {
          setOpenKey(null);
        }
      }
    } finally {
      setSending(false);
    }
  };

  const RowActions: React.FC<{ uid?: string; email?: string; rowKey: string; hasAccount: boolean; total: number }> = ({ uid, email, rowKey, hasAccount, total }) => (
    <div className="flex items-center justify-end gap-1" onClick={(e) => e.stopPropagation()}>
      <button
        type="button"
        onClick={() => open(email || uid || rowKey, 'notify', 'single')}
        className="ms-btn is-sm is-ghost text-accent"
        title={`${email || rowKey} kullanıcısına bildirim mesajı gönder`}
      >
        <Bell /> Bildirim
      </button>
      {email && (
        <button type="button" onClick={() => open(email, 'mail')} className="ms-btn is-sm is-ghost" title={`${email} adresine e-posta yaz`}>
          <Mail /> Mail
        </button>
      )}
      {isOwner(email) ? (
        <span className="ms-tag" title="Ana yönetici hesabı silinemez">
          <ShieldCheck /> Korunan
        </span>
      ) : hasAccount ? (
        <ConfirmButton icon={Trash2} confirmLabel="Emin misin? Sil" busy={busy === `del-${rowKey}`} busyLabel="Siliniyor…" onConfirm={() => deleteAccount(uid, email, rowKey)} title="Hesabı kalıcı olarak sil">
          Sil
        </ConfirmButton>
      ) : total > 0 ? (
        <ConfirmButton icon={Eraser} className="ms-btn is-sm is-warn" confirmLabel="Emin misin? Temizle" busy={busy === `purge-${rowKey}`} busyLabel="Temizleniyor…" onConfirm={() => purge(rowKey)} title="Kayıtlı hesabı yok; bu ismin katkı izlerini temizler">
          İzleri temizle
        </ConfirmButton>
      ) : null}
    </div>
  );

  const regKey = (u: ManageUser) => normKey(u.email || u.uid || u.displayName);
  const regCols: Col<ManageUser>[] = [
    {
      key: 'user',
      label: 'Kullanıcı',
      main: true,
      render: (u) => (
        <span className="flex items-center gap-2.5 min-w-0">
          <span className={`ms-avatar ${u.role === 'admin' || isOwner(u.email) ? 'is-accent' : ''}`}>{initial(u.displayName || u.email)}</span>
          <span className="min-w-0 flex flex-col">
            <span className="font-semibold truncate">{u.displayName || 'İsimsiz öğrenci'}</span>
            <span className="text-sm text-ink-3 truncate">{u.email || '—'}</span>
          </span>
        </span>
      ),
    },
    { key: 'role', label: 'Rol', render: (u) => (u.role === 'admin' || isOwner(u.email) ? <Pill tone="acc">Yönetici</Pill> : <Pill>Öğrenci</Pill>) },
    { key: 'no', label: 'Öğrenci no', mono: true, render: (u) => u.studentNumber || '—' },
    { key: 'created', label: 'Kayıt', muted: true, render: (u) => fmtDate(u.createdAt) },
    { key: 'login', label: 'Son giriş', muted: true, render: (u) => fmtDate(u.lastLoginAt) },
    { key: 'act', label: <span className="sr-only">İşlemler</span>, render: (u) => <RowActions uid={u.uid} email={u.email} rowKey={regKey(u)} hasAccount total={0} /> },
  ];
  const actCols: Col<UserActivityRow>[] = [
    {
      key: 'user',
      label: 'Kişi',
      main: true,
      render: (u) => (
        <span className="min-w-0 flex flex-col">
          <span className="font-semibold truncate">{u.name}</span>
          {u.email && <span className="text-sm text-ink-3 truncate">{u.email}</span>}
        </span>
      ),
    },
    { key: 'q', label: 'Soru', right: true, render: (u) => u.questions },
    { key: 'rev', label: 'Düzenleme', right: true, render: (u) => u.revisions || 0 },
    { key: 'frag', label: 'Parça', right: true, render: (u) => u.fragments },
    { key: 'opt', label: 'Şık', right: true, render: (u) => u.options },
    { key: 'rep', label: 'Bildirim', right: true, render: (u) => u.reports },
    { key: 'com', label: 'Yorum', right: true, render: (u) => u.comments },
    { key: 'tot', label: 'Toplam', right: true, render: (u) => <b>{u.total}</b> },
    {
      key: 'act',
      label: <span className="sr-only">İşlemler</span>,
      render: (u) => {
        const reg = regOf(u.key) || (u.email ? registeredUsers.find((r) => r.email && normKey(r.email) === normKey(u.email)) : undefined);
        return <RowActions uid={reg?.uid} email={u.email || reg?.email} rowKey={u.key} hasAccount={!!reg} total={u.total} />;
      },
    },
  ];
  const actShown = actRows.slice(0, 200);
  const activeSel = tab === 'registered' ? regSel : actSel;
  /** Seçilen satırlar → alıcı listesi (ad, e-posta, uid) */
  const targets = useMemo(() => {
    if (tab === 'registered') return regRows.filter((u) => regSel.has(regKey(u))).map((u) => ({ key: regKey(u), name: u.displayName || u.email || '', email: u.email, uid: u.uid }));
    return actShown
      .filter((u) => actSel.has(u.key))
      .map((u) => {
        const reg = regOf(u.key) || (u.email ? registeredUsers.find((r) => r.email && normKey(r.email) === normKey(u.email)) : undefined);
        return { key: u.key, name: u.name, email: u.email || reg?.email, uid: reg?.uid };
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tab, regRows, actShown, regSel.sel, actSel.sel, registeredUsers]);
  const deletable = targets.filter((x) => x.uid && !isOwner(x.email));

  const runBulk = async (fn: (x: (typeof targets)[number]) => Promise<{ ok: boolean }>, list = targets) => {
    setBulkBusy(true);
    let ok = 0;
    let bad = 0;
    for (const x of list) {
      try {
        const r = await fn(x);
        if (r.ok) ok++;
        else bad++;
      } catch {
        bad++;
      }
      setBulkDone(ok + bad);
    }
    setBulkBusy(false);
    notify(`${ok} başarılı, ${bad} hata.`);
    return bad;
  };
  const bulkDelete = async () => {
    await runBulk(async (x) => {
      const res = await deleteManageUser(adminEmail, x.uid!);
      if (res.ok) setRegisteredUsers((prev) => prev.filter((r) => r.uid !== x.uid));
      return res;
    }, deletable);
    activeSel.clear();
  };
  const bulkSend = async () => {
    setBulkDone(0);
    if (bulk === 'mail') {
      if (!subject.trim() || !body.trim()) return;
      const bad = await runBulk((x) => sendUserEmail(x.email!, subject.trim(), body.trim().replace(/\{ad\}/g, x.name)), targets.filter((x) => x.email));
      if (!bad) setBulk(null);
    } else if (bulk === 'notify') {
      if (!notifTitle.trim() || !notifMessage.trim()) return;
      const bad = await runBulk((x) =>
        sendAdminNotification(adminEmail, {
          target: 'single',
          targetUser: { uid: x.uid, email: x.email },
          title: notifTitle.trim(),
          message: notifMessage.trim(),
          type: notifType,
          deepLinkUrl: notifUrl.trim() || '/',
        }),
      );
      if (!bad) setBulk(null);
    }
  };
  const startBulk = (m: 'mail' | 'notify') => {
    setSubject('');
    setBody('Merhaba {ad},\n\n');
    setNotifTitle('');
    setNotifMessage('');
    setNotifType('app_info');
    setNotifUrl('/');
    setBulkDone(0);
    setBulk(m);
  };
  const openRows = tab === 'registered' ? regRows.map((u) => regKey(u)) : actShown.map((u) => u.key);
  const curKey = openKey && openKey !== '__ALL__' ? (sel?.key && openRows.includes(sel.key) ? sel.key : openKey) : null;

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <PageActions note={registeredUsers.length > 0 ? `${registeredUsers.length - admins} öğrenci, ${admins} yönetici. Hesaplar Supabase ve yerel veritabanından birleştirilir.` : undefined}>
        <button
          type="button"
          onClick={() => {
            setOpenKey('__ALL__');
            setNotifTarget('all');
            setMode('notify');
            setNotifTitle('');
            setNotifMessage('');
            setNotifType('app_info');
            setNotifUrl('/');
          }}
          className="m14-btn primary"
          title="Tüm kullanıcılara toplu bildirim / duyuru gönder"
        >
          <Bell aria-hidden="true" /> Herkese duyuru
        </button>
      </PageActions>
      <StatRow
        stats={[
          { label: 'Kayıtlı hesap', value: registeredUsers.length, onClick: () => setTab('registered') },
          { label: 'Katkı yapan', value: activity.length, onClick: () => setTab('activity') },
          { label: 'Yönetici', value: admins },
        ]}
      />
      <Toolbar>
        <Tabs14
          label="Kullanıcı görünümü"
          value={tab}
          onChange={(v) => setTab(v)}
          options={[
            { id: 'registered', label: 'Hesaplar', n: registeredUsers.length },
            { id: 'activity', label: 'Katkılar', n: activity.length },
          ]}
        />
        <SearchField value={query} onChange={setQuery} placeholder={tab === 'registered' ? 'Ad, e-posta, öğrenci no ya da kimlik' : 'Ad ya da e-posta'} label="Kullanıcı ara" />
        <span className="pk14-note">{tab === 'registered' ? `${regRows.length} hesap` : `${actRows.length} kişi`}</span>
      </Toolbar>

      <BulkBar
        count={activeSel.count}
        noun="kişi"
        busy={bulkBusy}
        onClear={activeSel.clear}
        actions={[
          { label: 'Bildirim gönder', kind: 'main', run: () => startBulk('notify') },
          { label: 'E-posta gönder', disabled: !targets.some((x) => x.email), run: () => startBulk('mail') },
          { label: `Hesapları sil (${deletable.length})`, kind: 'danger', disabled: !deletable.length, confirm: `${deletable.length} hesabı kalıcı silmeyi onayla`, run: bulkDelete },
        ]}
      />

      {tab === 'registered' ? (
        regRows.length === 0 ? (
          <EmptyState icon={Users} title={query ? 'Aramaya uyan hesap yok' : 'Kayıtlı hesap yok'} />
        ) : (
          <DataTable rows={regRows} cols={regCols} rowKey={regKey} onOpen={(u) => open(u.email || u.uid || u.displayName || '')} selection={regSel} activeKey={openKey} />
        )
      ) : actRows.length === 0 ? (
        <EmptyState icon={Users} title={query ? 'Aramaya uyan kişi yok' : 'Katkı kaydı yok'} />
      ) : (
        <DataTable rows={actShown} cols={actCols} rowKey={(u) => u.key} onOpen={(u) => open(u.key)} selection={actSel} activeKey={openKey} minWidth={860} />
      )}

      <Drawer
        open={!!bulk}
        onClose={() => !bulkBusy && setBulk(null)}
        title={bulk === 'mail' ? `Toplu e-posta · ${targets.filter((x) => x.email).length} kişi` : `Toplu bildirim · ${targets.length} kişi`}
        foot={
          <>
            <button type="button" className="m14-btn ghost" onClick={() => setBulk(null)} disabled={bulkBusy}>Vazgeç</button>
            <button
              type="button"
              className="m14-btn primary"
              onClick={() => void bulkSend()}
              disabled={bulkBusy || (bulk === 'mail' ? !subject.trim() || !body.trim() : !notifTitle.trim() || !notifMessage.trim())}
            >
              <Send aria-hidden="true" /> {bulkBusy ? `Gönderiliyor… ${bulkDone}` : 'Gönder'}
            </button>
          </>
        }
      >
        {bulk === 'mail' ? (
          <>
            <Field label="Konu">
              <input value={subject} onChange={(e) => setSubject(e.target.value)} placeholder="Konu başlığı" className="ms-input" />
            </Field>
            <Field label="Mesaj">
              <textarea value={body} onChange={(e) => setBody(e.target.value)} rows={8} className="ms-input" />
            </Field>
            <p className="pk14-note">{'{ad}'} her kişinin adıyla değiştirilir. İletiler tek tek, sırayla gönderilir.</p>
          </>
        ) : (
          <>
            <Field label="Bildirim başlığı">
              <input value={notifTitle} onChange={(e) => setNotifTitle(e.target.value)} className="ms-input" />
            </Field>
            <Field label="Bildirim türü">
              <Seg label="Bildirim türü" value={notifType} onChange={setNotifType} options={[{ id: 'app_info', label: 'Bilgi' }, { id: 'app_success', label: 'Başarı' }, { id: 'app_error', label: 'Uyarı' }]} />
            </Field>
            <Field label="Hedef bağlantı (isteğe bağlı)">
              <input value={notifUrl} onChange={(e) => setNotifUrl(e.target.value)} className="ms-input font-mono text-xs" />
            </Field>
            <Field label="Mesaj">
              <textarea value={notifMessage} onChange={(e) => setNotifMessage(e.target.value)} rows={6} className="ms-input" />
            </Field>
          </>
        )}
        <p className="pk14-note">Alıcılar: {targets.map((x) => x.name || x.email).join(', ')}</p>
      </Drawer>

      <Drawer
        open={!!sel}
        onClose={() => setOpenKey(null)}
        label="Kullanıcı ayrıntısı"
        wide
        head={
          openKey !== '__ALL__' && mode === 'detail' ? (
            <DetailNav list={openRows} current={curKey} same={(a, b) => a === b} onGo={(k) => {
              if (tab === 'registered') { const u = regRows.find((x) => regKey(x) === k); if (u) open(u.email || u.uid || u.displayName || ''); }
              else open(k);
            }} />
          ) : undefined
        }
        title={mode === 'mail' ? 'E-posta yaz' : mode === 'notify' ? (notifTarget === 'all' ? 'Toplu Bildirim & Duyuru' : 'Bildirim Gönder') : sel?.name || 'Kullanıcı'}
        foot={
          sel &&
          (mode === 'mail' ? (
            <>
              <button type="button" onClick={() => setMode('detail')} className="ms-btn is-auto">
                <ArrowLeft /> Geri
              </button>
              <button type="button" onClick={() => void sendMail()} disabled={sending || !subject.trim() || !body.trim()} className="ms-btn is-primary">
                <Send /> {sending ? 'Gönderiliyor…' : 'Gönder'}
              </button>
            </>
          ) : mode === 'notify' ? (
            <>
              {openKey !== '__ALL__' && (
                <button type="button" onClick={() => setMode('detail')} className="ms-btn is-auto">
                  <ArrowLeft /> Geri
                </button>
              )}
              <button
                type="button"
                onClick={() => void sendNotification()}
                disabled={sending || !notifTitle.trim() || !notifMessage.trim()}
                className="ms-btn is-primary"
              >
                <Send /> {sending ? 'Gönderiliyor…' : notifTarget === 'all' ? 'Tüm Kullanıcılara İlet' : 'Bildirimi Gönder'}
              </button>
            </>
          ) : (
            <>
              <button type="button" onClick={() => { setNotifTarget('single'); setMode('notify'); }} className="ms-btn is-accent">
                <Bell /> Bildirim gönder
              </button>
              {sel.email && (
                <button type="button" onClick={() => setMode('mail')} className="ms-btn is-primary">
                  <Mail /> E-posta yaz
                </button>
              )}
              {!isOwner(sel.email) && sel.reg && (
                <ConfirmButton icon={Trash2} className="ms-btn is-danger" confirmLabel="Kalıcı silmeyi onayla" busy={busy === `del-${sel.key}`} onConfirm={() => deleteAccount(sel.reg?.uid, sel.email, sel.key)}>
                  Hesabı sil
                </ConfirmButton>
              )}
              {!sel.reg && (sel.act?.total || 0) > 0 && (
                <ConfirmButton icon={Eraser} className="ms-btn is-warn" confirmLabel="Emin misin? Temizle" busy={busy === `purge-${sel.key}`} onConfirm={() => purge(sel.key)}>
                  Katkı izlerini temizle
                </ConfirmButton>
              )}
            </>
          ))
        }
      >
        {sel &&
          (mode === 'mail' ? (
            <>
              <p className="m-0 text-base text-ink-2">
                Alıcı: <b className="text-ink">{sel.name}</b> · <span className="font-mono text-sm">{sel.email}</span>
              </p>
              <Field label="Konu">
                <input value={subject} onChange={(e) => setSubject(e.target.value)} placeholder="Konu başlığı" className="ms-input" autoFocus />
              </Field>
              <Field label="Mesaj">
                <textarea value={body} onChange={(e) => setBody(e.target.value)} rows={8} placeholder="Mesajını yaz" className="ms-input" />
              </Field>
            </>
          ) : mode === 'notify' ? (
            <div className="flex flex-col gap-4">
              <div className="flex items-center gap-3 p-3 bg-accent/10 border border-accent/20 rounded-xl text-accent text-sm">
                <Bell className="w-5 h-5 shrink-0" />
                <div>
                  <b className="block">{notifTarget === 'all' ? 'Toplu Bildirim & Duyuru' : 'Kullanıcıya Özel Bildirim'}</b>
                  <p className="m-0 text-xs text-ink-2">
                    {notifTarget === 'all'
                      ? 'Bu bildirim tüm kayıtlı öğrencilerin profil bildirimlerine, açık cihazlarına ve izin verenlerin telefonuna iletilir.'
                      : `${sel.name} kullanıcısının profil bildirim geçmişine ve aktif cihazlarına iletilir.`}
                  </p>
                </div>
              </div>

              <Field label="Bildirim Başlığı">
                <input
                  value={notifTitle}
                  onChange={(e) => setNotifTitle(e.target.value)}
                  placeholder="Örn: Yeni Sınav Soruları Yüklendi"
                  className="ms-input"
                  autoFocus
                />
              </Field>

              <Field label="Bildirim Türü">
                <div className="flex gap-2">
                  {(
                    [
                      ['app_info', 'Bilgi'],
                      ['app_success', 'Başarı'],
                      ['app_error', 'Uyarı / önemli'],
                    ] as const
                  ).map(([k, lbl]) => (
                    <button
                      key={k}
                      type="button"
                      onClick={() => setNotifType(k)}
                      className={`ms-btn is-sm flex-1 ${notifType === k ? 'is-primary' : 'is-ghost'}`}
                    >
                      {lbl}
                    </button>
                  ))}
                </div>
              </Field>

              <Field label="Hedef Bağlantı (İsteğe bağlı deep link)">
                <input
                  value={notifUrl}
                  onChange={(e) => setNotifUrl(e.target.value)}
                  placeholder="Örn: / veya /ogren veya /cikmis"
                  className="ms-input font-mono text-xs"
                />
              </Field>

              <Field label="Mesaj Metni">
                <textarea
                  value={notifMessage}
                  onChange={(e) => setNotifMessage(e.target.value)}
                  rows={6}
                  placeholder="Öğrenciye iletilecek bildirim mesajını buraya yazın..."
                  className="ms-input"
                />
              </Field>
            </div>
          ) : (
            <>
              <div className="flex items-center gap-3">
                <span className={`ms-avatar is-lg ${sel.reg?.role === 'admin' || isOwner(sel.email) ? 'is-accent' : ''}`}>{initial(sel.name)}</span>
                <div className="min-w-0 flex flex-col gap-1">
                  <span className="flex flex-wrap gap-1">
                    {sel.reg ? <span className="ms-tag is-ok">Kayıtlı hesap</span> : <span className="ms-tag is-warn">Hesabı yok, yalnız katkı izi</span>}
                    {(sel.reg?.role === 'admin' || isOwner(sel.email)) && <span className="ms-tag is-accent"><ShieldCheck /> Yönetici</span>}
                  </span>
                  {sel.email && <span className="font-mono text-sm text-ink-2 truncate">{sel.email}</span>}
                </div>
              </div>
              <dl className="ms-kv">
                {sel.studentNumber && (<><dt>Öğrenci no</dt><dd className="font-mono">{sel.studentNumber}</dd></>)}
                {sel.reg?.createdAt && (<><dt>Kayıt</dt><dd>{fmtDate(sel.reg.createdAt)}</dd></>)}
                {sel.reg?.lastLoginAt && (<><dt>Son giriş</dt><dd>{new Date(sel.reg.lastLoginAt).toLocaleString('tr-TR', { dateStyle: 'medium', timeStyle: 'short' })}</dd></>)}
                {sel.reg?.uid && (<><dt>UID</dt><dd className="font-mono text-xs">{sel.reg.uid}</dd></>)}
              </dl>
              <dl className="ms-statgrid m-0">
                {([['Soru', sel.act?.questions], ['Düzenleme', sel.act?.revisions], ['Parça', sel.act?.fragments], ['Şık', sel.act?.options], ['Bildirim', sel.act?.reports], ['Yorum', sel.act?.comments]] as const).map(([k, v]) => (
                  <div key={k}><dt>{k}</dt><dd>{v || 0}</dd></div>
                ))}
              </dl>
              <DList title="Eklediği ve katkı verdiği sorular" items={sel.userQuestions.map((x) => ({ text: `S.${x.questionNumber || '?'} · ${x.topic || x.discipline}` }))} empty="Katkı kaydı yok" />
              <DList title="Yaptığı soru düzenlemeleri (Revizyonlar)" items={sel.userRevisions.map((r) => ({ label: `${r.questionLabel} · ${r.date} (v${r.version})`, text: r.changeSummary }))} empty="Düzenleme kaydı yok" />
              <DList title="Hafıza parçaları" items={sel.fragments.map((f) => ({ label: f.label, text: f.text.length > 160 ? f.text.slice(0, 160) + '…' : f.text }))} empty="Parça kaydı yok" />
              <DList title="Hata bildirimleri" items={sel.userReports.map((r) => ({ label: r.questionTopic || r.questionId, text: r.reason }))} empty="Bildirim yok" />
              <DList title="Yorumlar" items={sel.userComments.map((c) => ({ label: c.questionTopic || c.questionId, text: c.text }))} empty="Yorum yok" />
            </>
          ))}
      </Drawer>
    </div>
  );
};

const DList: React.FC<{ title: string; items: { label?: string; text: string }[]; empty: string }> = ({ title, items, empty }) => (
  <section className="ms-dsec">
    <h3>
      {title} <span className="n">{items.length}</span>
    </h3>
    {items.length === 0 ? (
      <p className="m-0 text-sm text-ink-3">{empty}</p>
    ) : (
      <ul className="ms-dlist">
        {items.map((it, i) => (
          <li key={i}>
            {it.label && <small>{it.label}</small>}
            {it.text}
          </li>
        ))}
      </ul>
    )}
  </section>
);
