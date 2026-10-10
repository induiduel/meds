import React, { useMemo, useState } from 'react';
import { Mail, Trash2, ShieldCheck, Send, Users, Eraser, ArrowLeft } from 'lucide-react';
import type { Committee, QuestionItem } from '../../types';
import {
  InboxReport,
  InboxComment,
  UserActivityRow,
  ManageUser,
  normKey,
  sendUserEmail,
  deleteManageUser,
  purgeAuthorContributions,
} from '../../services/manageConsoleService';
import { EmptyState, SearchBox, Seg, ConfirmButton, Drawer, Field } from './consoleUi';

/**
 * Kullanıcılar: kayıtlı hesaplar ve katkı istatistikleri iki tabloda. Satıra dokununca ayrıntı
 * yan çekmecede açılır (katkıları, parçaları, bildirimleri, yorumları); e-posta da oradan yazılır.
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
  const [mode, setMode] = useState<'detail' | 'mail'>('detail');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [sending, setSending] = useState(false);
  const [busy, setBusy] = useState<string | null>(null);

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

  const open = (key: string, m: 'detail' | 'mail' = 'detail') => {
    setOpenKey(normKey(key));
    setMode(m);
    if (m === 'mail') {
      setSubject('');
      setBody('');
    }
  };

  // --- Çekmecedeki kişi ---
  const sel = useMemo(() => {
    if (!openKey) return null;
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

  const RowActions: React.FC<{ uid?: string; email?: string; rowKey: string; hasAccount: boolean; total: number }> = ({ uid, email, rowKey, hasAccount, total }) => (
    <div className="flex items-center justify-end gap-1" onClick={(e) => e.stopPropagation()}>
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

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <div className="flex flex-col md:flex-row md:items-center gap-2">
        <Seg
          label="Kullanıcı görünümü"
          value={tab}
          onChange={(v) => setTab(v)}
          options={[
            { id: 'registered', label: 'Kayıtlı hesaplar', n: registeredUsers.length },
            { id: 'activity', label: 'Katkılar', n: activity.length },
          ]}
        />
        <SearchBox
          value={query}
          onChange={setQuery}
          placeholder={tab === 'registered' ? 'İsim, e-posta ya da öğrenci no' : 'İsim ya da e-posta'}
          count={tab === 'registered' ? `${regRows.length} hesap` : `${actRows.length} kişi`}
          className="flex-1"
        />
      </div>
      {tab === 'registered' && registeredUsers.length > 0 && (
        <p className="m-0 text-[12.5px] text-ink-3">
          {registeredUsers.length - admins} öğrenci, {admins} yönetici. Hesaplar Supabase ve yerel veritabanından birleştirilir.
        </p>
      )}

      {tab === 'registered' ? (
        <div className="ms-table-wrap">
          {regRows.length === 0 ? (
            <EmptyState icon={Users} title={query ? 'Aramaya uyan hesap yok' : 'Kayıtlı hesap yok'} />
          ) : (
            <table className="ms-table min-w-[760px]">
              <thead>
                <tr>
                  <th scope="col">Kullanıcı</th>
                  <th scope="col">Öğrenci no</th>
                  <th scope="col">Rol</th>
                  <th scope="col">Kayıt</th>
                  <th scope="col">Son giriş</th>
                  <th scope="col" className="text-right"><span className="sr-only">İşlemler</span></th>
                </tr>
              </thead>
              <tbody>
                {regRows.map((u) => {
                  const key = normKey(u.email || u.uid || u.displayName);
                  const admin = u.role === 'admin' || isOwner(u.email);
                  return (
                    <tr key={u.uid || u.email} onClick={() => open(u.email || u.uid || u.displayName || '')} className={`is-button ${openKey === key ? 'is-on' : ''}`}>
                      <td>
                        <div className="flex items-center gap-2.5 min-w-0">
                          <span className={`ms-avatar ${admin ? 'is-accent' : ''}`}>{initial(u.displayName || u.email)}</span>
                          <div className="min-w-0">
                            <div className="font-semibold truncate max-w-[240px]">{u.displayName || 'İsimsiz öğrenci'}</div>
                            <div className="text-[12.5px] text-ink-3 truncate max-w-[260px]">{u.email || '—'}</div>
                          </div>
                        </div>
                      </td>
                      <td className="font-mono text-[12.5px]">{u.studentNumber || <span className="text-ink-3 font-sans">—</span>}</td>
                      <td>{admin ? <span className="ms-tag is-accent"><ShieldCheck /> Yönetici</span> : <span className="ms-tag">Öğrenci</span>}</td>
                      <td className="text-ink-2 whitespace-nowrap">{fmtDate(u.createdAt)}</td>
                      <td className="text-ink-2 whitespace-nowrap">{fmtDate(u.lastLoginAt)}</td>
                      <td><RowActions uid={u.uid} email={u.email} rowKey={key} hasAccount total={0} /></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      ) : (
        <div className="ms-table-wrap">
          {actRows.length === 0 ? (
            <EmptyState icon={Users} title={query ? 'Aramaya uyan kişi yok' : 'Katkı kaydı yok'} />
          ) : (
            <table className="ms-table min-w-[760px]">
              <thead>
                <tr>
                  <th scope="col">Kişi</th>
                  <th scope="col" className="is-num">Soru</th>
                  <th scope="col" className="is-num">Düzenleme</th>
                  <th scope="col" className="is-num">Parça</th>
                  <th scope="col" className="is-num">Şık</th>
                  <th scope="col" className="is-num">Bildirim</th>
                  <th scope="col" className="is-num">Yorum</th>
                  <th scope="col" className="is-num">Toplam</th>
                  <th scope="col"><span className="sr-only">İşlemler</span></th>
                </tr>
              </thead>
              <tbody>
                {actRows.slice(0, 200).map((u) => {
                  const reg = regOf(u.key) || (u.email ? registeredUsers.find((r) => r.email && normKey(r.email) === normKey(u.email)) : undefined);
                  return (
                    <tr key={u.key} onClick={() => open(u.key)} className={`is-button ${openKey === u.key ? 'is-on' : ''}`}>
                      <td>
                        <div className="font-semibold truncate max-w-[260px]">{u.name}</div>
                        {u.email && <div className="text-[12.5px] text-ink-3 truncate max-w-[260px]">{u.email}</div>}
                      </td>
                      <td className="is-num">{u.questions}</td>
                      <td className="is-num">{u.revisions || 0}</td>
                      <td className="is-num">{u.fragments}</td>
                      <td className="is-num">{u.options}</td>
                      <td className="is-num">{u.reports}</td>
                      <td className="is-num">{u.comments}</td>
                      <td className="is-num font-semibold">{u.total}</td>
                      <td><RowActions uid={reg?.uid} email={u.email || reg?.email} rowKey={u.key} hasAccount={!!reg} total={u.total} /></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      )}

      <Drawer
        open={!!sel}
        onClose={() => setOpenKey(null)}
        label="Kullanıcı ayrıntısı"
        title={mode === 'mail' ? 'E-posta yaz' : sel?.name || 'Kullanıcı'}
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
          ) : (
            <>
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
              <p className="m-0 text-[13.5px] text-ink-2">
                Alıcı: <b className="text-ink">{sel.name}</b> · <span className="font-mono text-[12.5px]">{sel.email}</span>
              </p>
              <Field label="Konu">
                <input value={subject} onChange={(e) => setSubject(e.target.value)} placeholder="Konu başlığı" className="ms-input" autoFocus />
              </Field>
              <Field label="Mesaj">
                <textarea value={body} onChange={(e) => setBody(e.target.value)} rows={8} placeholder="Mesajını yaz" className="ms-input" />
              </Field>
            </>
          ) : (
            <>
              <div className="flex items-center gap-3">
                <span className={`ms-avatar is-lg ${sel.reg?.role === 'admin' || isOwner(sel.email) ? 'is-accent' : ''}`}>{initial(sel.name)}</span>
                <div className="min-w-0 flex flex-col gap-1">
                  <span className="flex flex-wrap gap-1">
                    {sel.reg ? <span className="ms-tag is-ok">Kayıtlı hesap</span> : <span className="ms-tag is-warn">Hesabı yok, yalnız katkı izi</span>}
                    {(sel.reg?.role === 'admin' || isOwner(sel.email)) && <span className="ms-tag is-accent"><ShieldCheck /> Yönetici</span>}
                  </span>
                  {sel.email && <span className="font-mono text-[12.5px] text-ink-2 truncate">{sel.email}</span>}
                </div>
              </div>
              <dl className="ms-kv">
                {sel.studentNumber && (<><dt>Öğrenci no</dt><dd className="font-mono">{sel.studentNumber}</dd></>)}
                {sel.reg?.createdAt && (<><dt>Kayıt</dt><dd>{fmtDate(sel.reg.createdAt)}</dd></>)}
                {sel.reg?.lastLoginAt && (<><dt>Son giriş</dt><dd>{new Date(sel.reg.lastLoginAt).toLocaleString('tr-TR', { dateStyle: 'medium', timeStyle: 'short' })}</dd></>)}
                {sel.reg?.uid && (<><dt>UID</dt><dd className="font-mono text-[12px]">{sel.reg.uid}</dd></>)}
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
      <p className="m-0 text-[13px] text-ink-3">{empty}</p>
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
