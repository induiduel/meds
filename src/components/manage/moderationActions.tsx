/**
 * Moderasyon eylemleri (ön yüz): yan kayıt (atama, etiket, ret, yanıt, erteleme, aktarma) okuma/yazma,
 * gerçek zamanlı yenileme ve tekli/toplu eylem çekmecesi. Sunucu: src/services/moderationActionsRoutes.ts
 */
import React, { useCallback, useEffect, useState } from 'react';
import { safeJsonFetch } from '../../services/api';
import { getLocalAdminSession, auth } from '../../services/auth';
import { realtimeEventService } from '../../services/realtimeEvents';
import { toast } from '../ui/Toast';
import { Drawer, Field, Switch } from './consoleUi';
import { Card14, Pill } from '../v14/pageKit';

export interface ModerationMetaClient {
  id: string;
  kind?: string;
  assignee?: string;
  tags?: string[];
  rejected?: { reason: string; at: string; by: string } | null;
  snoozedUntil?: string | null;
  escalated?: { at: string; by: string } | null;
  replies?: { text: string; at: string; by: string; delivered: boolean }[];
  updatedAt?: string;
}

export type ModerationActionKind = 'assign' | 'tags' | 'add_tags' | 'remove_tags' | 'reject' | 'reopen' | 'reply' | 'snooze' | 'unsnooze' | 'escalate' | 'unescalate';

export const currentAdminEmail = () => getLocalAdminSession()?.email || auth?.currentUser?.email || 'nofrostlife@gmail.com';
const adminHeader = () => ({ 'x-admin-email': currentAdminEmail() });

export async function runModerationAction(
  ids: string[],
  action: ModerationActionKind,
  extra: Record<string, unknown> = {},
): Promise<{ ok: boolean; items: Record<string, ModerationMetaClient>; results: { id: string; ok: boolean; error?: string }[]; error?: string }> {
  const res = await safeJsonFetch<any>('/api/admin/moderation/actions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...adminHeader() },
    body: JSON.stringify({ ids, action, ...extra }),
  });
  if (!res.ok || !res.data) return { ok: false, items: {}, results: [], error: res.data?.error || res.error || 'Sunucu yanıt vermedi.' };
  return { ok: true, items: res.data.items || {}, results: res.data.results || [] };
}

/** Yan kaydı yükler; başka bir yönetici değiştirince SSE ile tazelenir. */
export function useModerationMeta() {
  const [meta, setMeta] = useState<Record<string, ModerationMetaClient>>({});
  const reload = useCallback(async () => {
    const res = await safeJsonFetch<{ items: Record<string, ModerationMetaClient> }>('/api/admin/moderation/meta', { headers: adminHeader() });
    if (res.ok && res.data?.items && typeof res.data.items === 'object') setMeta(res.data.items);
  }, []);
  useEffect(() => {
    void reload();
    let t: ReturnType<typeof setTimeout> | undefined;
    const bump = () => { clearTimeout(t); t = setTimeout(() => void reload(), 400); };
    const offs = [realtimeEventService.on('moderation_meta_changed', bump), realtimeEventService.on('resync', bump)];
    return () => { clearTimeout(t); offs.forEach((off) => off()); };
  }, [reload]);
  /** Eylemi çalıştırır, sonucu yerelde hemen uygular ve özet bildirir */
  const act = useCallback(async (ids: string[], action: ModerationActionKind, extra: Record<string, unknown> = {}) => {
    const r = await runModerationAction(ids, action, extra);
    if (!r.ok) { toast.error(r.error || 'İşlem yapılamadı.'); return false; }
    setMeta((prev) => ({ ...prev, ...r.items }));
    const bad = r.results.filter((x) => !x.ok || x.error);
    if (bad.length) toast.error(`${r.results.length - bad.length} başarılı, ${bad.length} sorunlu. ${bad[0].error || ''}`.trim());
    else toast.success(`${r.results.length} kayıt güncellendi.`);
    return true;
  }, []);
  return { meta, reload, act };
}

export const isSnoozed = (m?: ModerationMetaClient) => !!m?.snoozedUntil && new Date(m.snoozedUntil).getTime() > Date.now();
export const isRejected = (m?: ModerationMetaClient) => !!m?.rejected;
export const isMine = (m?: ModerationMetaClient) => !!m?.assignee && m.assignee.toLocaleLowerCase('tr-TR') === currentAdminEmail().toLocaleLowerCase('tr-TR');

const shortDate = (iso: string) => new Date(iso).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });

/** Tablo hücresi: atanan kişi, etiketler, erteleme, ret, aktarma */
export const MetaPills: React.FC<{ m?: ModerationMetaClient }> = ({ m }) => {
  if (!m) return <span className="text-ink-3">—</span>;
  const tags = m.tags || [];
  const any = m.assignee || tags.length || isSnoozed(m) || m.rejected || m.escalated;
  if (!any) return <span className="text-ink-3">—</span>;
  return (
    <span className="inline-flex gap-1 flex-wrap min-w-0">
      {m.rejected && <Pill tone="bad">Reddedildi</Pill>}
      {isSnoozed(m) && <Pill tone="warn">{shortDate(m.snoozedUntil!)} tarihine ertelendi</Pill>}
      {m.escalated && <Pill tone="acc">Moderasyonda</Pill>}
      {m.assignee && <Pill>{isMine(m) ? 'Bana atandı' : m.assignee}</Pill>}
      {tags.slice(0, 3).map((t) => <Pill key={t} tone="acc">{t}</Pill>)}
      {tags.length > 3 && <Pill>+{tags.length - 3}</Pill>}
    </span>
  );
};

/** Ayrıntı yan paneli için satırlar */
export const metaFacts = (m?: ModerationMetaClient): { k: string; v: React.ReactNode }[] => {
  if (!m) return [];
  const out: { k: string; v: React.ReactNode }[] = [];
  if (m.assignee) out.push({ k: 'Atanan', v: <span className="[overflow-wrap:anywhere]">{m.assignee}</span> });
  if (m.tags?.length) out.push({ k: 'Etiketler', v: <span className="inline-flex gap-1 flex-wrap">{m.tags.map((t) => <Pill key={t} tone="acc">{t}</Pill>)}</span> });
  if (isSnoozed(m)) out.push({ k: 'Ertelendi', v: new Date(m.snoozedUntil!).toLocaleString('tr-TR', { dateStyle: 'medium', timeStyle: 'short' }) });
  if (m.rejected) out.push({ k: 'Ret gerekçesi', v: <span className="[overflow-wrap:anywhere]">{m.rejected.reason}</span> });
  if (m.escalated) out.push({ k: 'Aktarıldı', v: `Moderasyona, ${shortDate(m.escalated.at)}` });
  return out;
};

/** Öğrenciye giden yanıtların geçmişi */
export const ReplyHistory: React.FC<{ m?: ModerationMetaClient }> = ({ m }) =>
  m?.replies?.length ? (
    <Card14 title="Öğrenciye yanıtlar">
      <ol className="m-0 p-0 list-none flex flex-col gap-2">
        {m.replies.map((r, i) => (
          <li key={i} className="rounded-lg border border-line p-2.5 min-w-0">
            <p className="m-0 text-sm text-ink whitespace-pre-wrap [overflow-wrap:anywhere]">{r.text}</p>
            <div className="mt-1 text-xs text-ink-3 flex gap-2 flex-wrap">
              <span>{new Date(r.at).toLocaleString('tr-TR', { dateStyle: 'medium', timeStyle: 'short' })}</span>
              {r.delivered ? <Pill tone="ok">İletildi</Pill> : <Pill tone="warn">İletilemedi</Pill>}
            </div>
          </li>
        ))}
      </ol>
    </Card14>
  ) : null;

export type ActionMode = 'assign' | 'tags' | 'reject' | 'reply' | 'snooze';

const MODE_TITLE: Record<ActionMode, string> = {
  assign: 'Kişiye ata',
  tags: 'Etiket ekle',
  reject: 'Bildirimi reddet',
  reply: 'Öğrenciye yanıt yaz',
  snooze: 'Ertele',
};

const inDays = (n: number) => {
  const d = new Date();
  d.setDate(d.getDate() + n);
  d.setHours(9, 0, 0, 0);
  const pad = (x: number) => String(x).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T09:00`;
};

/**
 * Tekli ya da toplu eylem çekmecesi. Gönderim yalnız alttaki düğmeyle olur; toplu yanıt ayrıca
 * kaç öğrenciye gideceğini düğmede yazar.
 */
export const ModerationActionDrawer: React.FC<{
  mode: ActionMode | null;
  ids: string[];
  kind?: string;
  current?: ModerationMetaClient;
  onClose: () => void;
  act: (ids: string[], action: ModerationActionKind, extra?: Record<string, unknown>) => Promise<boolean>;
}> = ({ mode, ids, kind, current, onClose, act }) => {
  const [text, setText] = useState('');
  const [tags, setTags] = useState('');
  const [replace, setReplace] = useState(false);
  const [until, setUntil] = useState(inDays(1));
  const [notifyStudent, setNotifyStudent] = useState(false);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!mode) return;
    setText(mode === 'assign' ? current?.assignee || '' : '');
    setTags(mode === 'tags' && ids.length === 1 ? (current?.tags || []).join(', ') : '');
    setReplace(mode === 'tags' && ids.length === 1);
    setUntil(inDays(1));
    setNotifyStudent(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mode, ids.join('|')]);

  const n = ids.length;
  const many = n > 1;
  const submit = async () => {
    if (!mode) return;
    setBusy(true);
    try {
      let ok = false;
      if (mode === 'assign') ok = await act(ids, 'assign', { assignee: text.trim(), kind });
      else if (mode === 'tags') ok = await act(ids, replace ? 'tags' : 'add_tags', { tags, kind });
      else if (mode === 'reject') ok = await act(ids, 'reject', { reason: text.trim(), notify: notifyStudent, kind });
      else if (mode === 'reply') ok = await act(ids, 'reply', { text: text.trim(), kind });
      else if (mode === 'snooze') ok = await act(ids, 'snooze', { until: new Date(until).toISOString(), kind });
      if (ok) onClose();
    } finally {
      setBusy(false);
    }
  };

  const disabled =
    busy ||
    (mode === 'reject' && !text.trim()) ||
    (mode === 'reply' && !text.trim()) ||
    (mode === 'tags' && !tags.trim() && !replace) ||
    (mode === 'snooze' && !(new Date(until).getTime() > Date.now()));

  const submitLabel =
    mode === 'reply' ? (many ? `${n} öğrenciye gönder` : 'Yanıtı gönder')
    : mode === 'reject' ? (many ? `${n} bildirimi reddet` : 'Reddet')
    : mode === 'assign' ? (text.trim() ? 'Ata' : 'Atamayı kaldır')
    : mode === 'snooze' ? 'Ertele'
    : 'Etiketleri kaydet';

  return (
    <Drawer
      open={!!mode}
      onClose={onClose}
      title={mode ? MODE_TITLE[mode] : ''}
      label="Moderasyon eylemi"
      head={<span className="text-xs text-ink-3">{many ? `${n} kayıt seçili` : 'Tek kayıt'}</span>}
      foot={
        <>
          <button type="button" onClick={onClose} className="m14-btn ghost">Vazgeç</button>
          {mode === 'snooze' && current?.snoozedUntil && (
            <button type="button" disabled={busy} onClick={async () => { if (await act(ids, 'unsnooze', { kind })) onClose(); }} className="m14-btn">Ertelemeyi kaldır</button>
          )}
          {mode === 'reject' && current?.rejected && (
            <button type="button" disabled={busy} onClick={async () => { if (await act(ids, 'reopen', { kind })) onClose(); }} className="m14-btn">Reddi geri al</button>
          )}
          <button type="button" disabled={disabled} onClick={() => void submit()} className={`m14-btn ${mode === 'reject' ? 'danger' : 'primary'}`}>
            {busy ? 'Gönderiliyor…' : submitLabel}
          </button>
        </>
      }
    >
      {mode && (
        <Card14>
          <div className="flex flex-col gap-3 min-w-0">
            {mode === 'assign' && (
              <>
                <Field label="Kişi" hint="Ad ya da e-posta. Boş bırakırsan atama kaldırılır.">
                  <input type="text" value={text} onChange={(e) => setText(e.target.value)} className="ms-input" placeholder="ornek@eposta.com" />
                </Field>
                <button type="button" onClick={() => setText(currentAdminEmail())} className="m14-btn ghost self-start">Bana ata</button>
              </>
            )}
            {mode === 'tags' && (
              <>
                <Field label="Etiketler" hint="Virgülle ayır, en çok 20 etiket.">
                  <input type="text" value={tags} onChange={(e) => setTags(e.target.value)} className="ms-input" placeholder="cevap anahtarı, yazım, acil" />
                </Field>
                <Switch checked={replace} onChange={setReplace} label="Var olan etiketlerin yerine yaz" />
              </>
            )}
            {mode === 'reject' && (
              <>
                <Field label="Ret gerekçesi" hint="Bildirim kapanır ama çözüldü sayılmaz; gerekçe kayıtta kalır.">
                  <textarea value={text} onChange={(e) => setText(e.target.value)} rows={4} className="ms-input" placeholder="Soru ders notuyla uyumlu; doğru cevap değişmiyor." />
                </Field>
                <Switch checked={notifyStudent} onChange={setNotifyStudent} label="Gerekçeyi öğrenciye de bildir" />
              </>
            )}
            {mode === 'reply' && (
              <Field label="Yanıt" hint={many ? `Aynı metin ${n} bildirimin sahibine ayrı ayrı gider.` : 'Öğrencinin bildirim kutusuna ve telefonuna düşer.'}>
                <textarea value={text} onChange={(e) => setText(e.target.value)} rows={5} className="ms-input" placeholder="Bildirimin için teşekkürler, soruyu düzelttik." />
              </Field>
            )}
            {mode === 'snooze' && (
              <>
                <Field label="Şu zamana kadar ertele">
                  <input type="datetime-local" value={until} onChange={(e) => setUntil(e.target.value)} className="ms-input" />
                </Field>
                <div className="flex gap-1.5 flex-wrap">
                  {[[1, 'Yarın'], [3, '3 gün'], [7, '1 hafta']].map(([d, l]) => (
                    <button key={String(d)} type="button" onClick={() => setUntil(inDays(Number(d)))} className="m14-btn ghost">{l}</button>
                  ))}
                </div>
              </>
            )}
          </div>
        </Card14>
      )}
    </Drawer>
  );
};
