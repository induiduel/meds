import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Users, Search, Smartphone, Monitor, Tablet, Clock, MessageSquare, Flag, PenLine, ListPlus, ThumbsUp, StickyNote, Activity,
  ExternalLink, Link2, Mail, Trash2, CheckCircle2, ArrowLeft, RefreshCw, Shield, Award, CircleDot, Copy, Pencil, X, Vote, Save,
} from 'lucide-react';
import { realtimeEventService } from '../../services/realtimeEvents';
import {
  loadPeople, loadPerson, forgetDevice, deletePersonEvent, personDeepLink, siteLink, fmtDuration, relTime,
  type PeopleList, type PersonRow, type PersonDetail, type PersonItem,
} from '../../services/peopleService';
import { deletePastComment, resolveInboxReport, sendUserEmail, deleteManageUser } from '../../services/manageConsoleService';
import { ApiService } from '../../services/api';
import { EmptyState, ConfirmButton } from './consoleUi';
import '../../styles/manage-people.css';
import { useAppearance } from '../../utils/appearance';
import { ManagePeopleV12 } from '../v12/ManagePeopleV12';

/**
 * Kişiler: her kullanıcının (hesaplı ya da girişsiz cihaz) tüm izi tek ekranda — cihazlar, kullanım süresi, skorlar,
 * etkinlik, yorumlar, notlar, yazdığı sorular, şık/ipucu katkıları, beğeniler, bildirimler. Liste + ayrıntı bölmesi;
 * adres `/manage/kisiler/<anahtar>?sekme=…` (kopyalanabilir derin bağlantı). Veri meds-pg tetikleyicisi → SSE
 * `people_changed` ile canlı: olay gelince açık liste ve kişi sessizce yeniden çekilir.
 */
interface Props {
  adminEmail: string;
  notify: (msg: string) => void;
}

type Filter = 'all' | 'online' | 'accounts' | 'guests' | 'reporters' | 'contributors';
type Sort = 'seen' | 'usage' | 'contrib';
type Tab = 'ozet' | 'etkinlik' | 'katkilar' | 'bildirimler' | 'notlar' | 'skorlar' | 'cihazlar';
export type PeopleFilter = Filter;
export type PeopleSort = Sort;
export type PeopleTab = Tab;
const TABS: { id: Tab; label: string }[] = [
  { id: 'ozet', label: 'Özet' },
  { id: 'etkinlik', label: 'Etkinlik' },
  { id: 'katkilar', label: 'Katkılar' },
  { id: 'bildirimler', label: 'Bildirimler' },
  { id: 'notlar', label: 'Notlar' },
  { id: 'skorlar', label: 'Skorlar' },
  { id: 'cihazlar', label: 'Cihazlar' },
];
const KIND_META: Record<string, { label: string; icon: React.ElementType }> = {
  comment: { label: 'Yorum', icon: MessageSquare },
  report: { label: 'Bildirim', icon: Flag },
  question: { label: 'Soru', icon: PenLine },
  fragment: { label: 'İpucu', icon: ListPlus },
  option: { label: 'Şık', icon: ListPlus },
  like: { label: 'Beğeni', icon: ThumbsUp },
  vote: { label: 'Oy', icon: Vote },
  note: { label: 'Not', icon: StickyNote },
  answer: { label: 'Cevap', icon: CheckCircle2 },
  feedback: { label: 'Geri bildirim', icon: Activity },
};
const SOURCE_LABEL: Record<string, string> = { past: 'Çıkmış', pool: 'Havuz', learn: 'Öğren', ornek: 'Örnek soru', notebook: 'Defter' };
const ACT_LABEL: Record<string, string> = { dogru: 'Doğru', yanlis: 'Yanlış', katki: 'Katkı', ogren: 'Öğren', test: 'Test', kart: 'Kart' };

const fold = (t: string) => t.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');
const initial = (s?: string | null) => (s || '?').trim().charAt(0).toLocaleUpperCase('tr-TR') || '?';
const fmtDateTime = (iso?: string | null) =>
  iso ? new Date(iso).toLocaleString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—';
const contribTotal = (r: PersonRow) => r.counts.comment + r.counts.question + r.counts.fragment + r.counts.option + r.counts.report + r.counts.note;
const deviceIcon = (label: string) => (/iphone|android|mobile|telefon/i.test(label) ? Smartphone : /ipad|tablet/i.test(label) ? Tablet : Monitor);

/** Adres: /manage/kisiler/<anahtar>?sekme=<tab> */
const readUrl = (): { key: string | null; tab: Tab } => {
  const segs = window.location.pathname.split('/').filter(Boolean);
  const key = segs[0] === 'manage' && segs[1] === 'kisiler' && segs[2] ? decodeURIComponent(segs[2]) : null;
  const t = new URLSearchParams(window.location.search).get('sekme') as Tab | null;
  return { key, tab: t && TABS.some((x) => x.id === t) ? t : 'ozet' };
};
const writeUrl = (key: string | null, tab: Tab, replace = false) => {
  const path = `/manage/kisiler${key ? `/${encodeURIComponent(key)}` : ''}${key && tab !== 'ozet' ? `?sekme=${tab}` : ''}`;
  if (window.location.pathname + window.location.search === path) return;
  try {
    window.history[replace ? 'replaceState' : 'pushState']({ route: 'manage', param: 'kisiler' }, '', path);
  } catch {
    /* korumalı çerçeve */
  }
};

export const ManagePeopleSection: React.FC<Props> = ({ adminEmail, notify }) => {
  const v12 = useAppearance().design === 'v12';
  const [list, setList] = useState<PeopleList | null>(null);
  const [listErr, setListErr] = useState('');
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState<Filter>('all');
  const [sort, setSort] = useState<Sort>('seen');
  const [{ key: openKey, tab }, setSel] = useState(readUrl);
  const [detail, setDetail] = useState<PersonDetail | null>(null);
  const [detailErr, setDetailErr] = useState('');
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [pulse, setPulse] = useState(0); // canlı güncelleme göstergesi
  const [, setTick] = useState(0);
  const openKeyRef = useRef(openKey);
  openKeyRef.current = openKey;

  const refreshList = useCallback(async () => {
    try {
      setList(await loadPeople());
      setListErr('');
    } catch (e: any) {
      setListErr(e?.message || 'Kişiler yüklenemedi.');
    }
  }, []);
  const refreshDetail = useCallback(async (key: string | null, quiet = false) => {
    if (!key) return setDetail(null);
    if (!quiet) setLoadingDetail(true);
    try {
      const d = await loadPerson(key);
      if (openKeyRef.current === key) {
        setDetail(d);
        setDetailErr('');
      }
    } catch (e: any) {
      if (openKeyRef.current === key) setDetailErr(e?.message || 'Kişi yüklenemedi.');
    } finally {
      if (!quiet) setLoadingDetail(false);
    }
  }, []);

  useEffect(() => {
    void refreshList();
  }, [refreshList]);
  useEffect(() => {
    setDetail((d) => (d && d.person.key === openKey ? d : null));
    void refreshDetail(openKey);
  }, [openKey, refreshDetail]);

  // Canlı: veritabanı olayı → 700 ms toplu tazeleme (liste + açık kişi). Ayrıca 60 sn'de bir (çevrimiçi durumu düşer).
  useEffect(() => {
    let timer: ReturnType<typeof setTimeout> | null = null;
    const bump = () => {
      if (timer) return;
      timer = setTimeout(() => {
        timer = null;
        setPulse((n) => n + 1);
        void refreshList();
        if (openKeyRef.current) void refreshDetail(openKeyRef.current, true);
      }, 700);
    };
    const offs = [
      realtimeEventService.on('people_changed', bump),
      realtimeEventService.on('inbox_update', bump),
      realtimeEventService.on('resync', bump),
      realtimeEventService.on('database_sync', (p: any) => {
        if (p?.table === 'users' || p?.table === 'past_question_reports') bump();
      }),
      realtimeEventService.on('learn_feedback_changed', bump),
      realtimeEventService.on('learn_social', bump),
    ];
    const iv = setInterval(() => {
      if (!document.hidden) bump();
      setTick((n) => n + 1);
    }, 60_000);
    return () => {
      offs.forEach((o) => o());
      clearInterval(iv);
      if (timer) clearTimeout(timer);
    };
  }, [refreshList, refreshDetail]);

  // Geri/ileri tuşları
  useEffect(() => {
    const onPop = () => setSel(readUrl());
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);

  const open = (key: string | null, t: Tab = 'ozet') => {
    setSel({ key, tab: t });
    writeUrl(key, t);
  };
  const setTab = (t: Tab) => {
    setSel((s) => ({ ...s, tab: t }));
    writeUrl(openKey, t, true);
  };

  const rows = useMemo(() => {
    const all = list?.people || [];
    const q = fold(query.trim());
    let r = all.filter((p) => {
      if (filter === 'online' && !p.online) return false;
      if (filter === 'accounts' && p.kind !== 'account') return false;
      if (filter === 'guests' && p.kind !== 'guest') return false;
      if (filter === 'reporters' && !p.counts.report) return false;
      if (filter === 'contributors' && !contribTotal(p)) return false;
      if (!q) return true;
      return fold([p.name, p.email, p.studentNumber, p.phone, p.uid, ...p.deviceNames].filter(Boolean).join(' ')).includes(q);
    });
    if (sort === 'usage') r = [...r].sort((a, b) => b.totalSeconds - a.totalSeconds);
    if (sort === 'contrib') r = [...r].sort((a, b) => contribTotal(b) - contribTotal(a));
    return r;
  }, [list, query, filter, sort]);

  const t = list?.totals;
  const FILTERS: [Filter, string, number?][] = [
    ['all', 'Tümü', t?.people],
    ['online', 'Çevrimiçi', t?.online],
    ['accounts', 'Hesaplar', t?.accounts],
    ['guests', 'Misafir'],
    ['reporters', 'Bildirim yapanlar'],
    ['contributors', 'Katkı yapanlar'],
  ];

  // v12 "Net": denetim düzeni (kayıtlı görünümler, süzgeç çubuğu, seçimli tablo, sağ ayrıntı çekmecesi); veri ve işlevler aynı
  if (v12)
    return (
      <ManagePeopleV12
        list={list}
        listErr={listErr}
        rows={rows}
        filters={FILTERS}
        filter={filter}
        setFilter={setFilter}
        query={query}
        setQuery={setQuery}
        sort={sort}
        setSort={setSort}
        pulse={pulse}
        onRefresh={() => void refreshList()}
        openKey={openKey}
        tab={tab}
        open={open}
        setTab={setTab}
        detail={detail}
        detailErr={detailErr}
        loadingDetail={loadingDetail}
        adminEmail={adminEmail}
        notify={notify}
        reload={() => {
          void refreshDetail(openKey, true);
          void refreshList();
        }}
        parts={PEOPLE_V12_PARTS}
      />
    );

  return (
    <div className={`pp-root ${openKey ? 'has-open' : ''}`}>
      <section className="pp-list" aria-label="Kişi listesi">
        <div className="pp-kpis" role="list">
          <Kpi icon={Users} label="Kişi" value={t?.people ?? '—'} />
          <Kpi icon={CircleDot} label="Şu an çevrimiçi" value={t?.online ?? '—'} tone="ok" />
          <Kpi icon={Monitor} label="Cihaz" value={t?.devices ?? '—'} />
          <Kpi icon={Clock} label="Son 7 gün" value={t ? fmtDuration(t.weekSeconds) : '—'} />
        </div>
        <div className="pp-tools">
          <label className="pp-search">
            <Search aria-hidden />
            <input type="search" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Ad, e-posta, numara, cihaz…" aria-label="Kişi ara" />
          </label>
          <select className="pp-sort" value={sort} onChange={(e) => setSort(e.target.value as Sort)} aria-label="Sırala">
            <option value="seen">Son görülme</option>
            <option value="usage">Kullanım süresi</option>
            <option value="contrib">Katkı sayısı</option>
          </select>
          <button type="button" className="ms-btn is-sm" onClick={() => void refreshList()} title="Yenile" aria-label="Yenile">
            <RefreshCw key={pulse} className="pp-spin-once" />
          </button>
        </div>
        <div className="pp-chips" role="tablist" aria-label="Süzgeç">
          {FILTERS.map(([id, label, n]) => (
            <button key={id} type="button" role="tab" aria-selected={filter === id} className={`pp-chip ${filter === id ? 'is-on' : ''}`} onClick={() => setFilter(id)}>
              {label}
              {n !== undefined && <span>{n}</span>}
            </button>
          ))}
        </div>
        {list && !list.database && <p className="pp-warn">Veritabanı şu an bağlı değil: cihaz ve etkinlik verisi geçici olarak eksik; yazımlar kuyrukta bekliyor.</p>}
        {listErr && <p className="pp-error">{listErr}</p>}
        <div className="pp-rows" role="list">
          {!list && !listErr && <div className="pp-skel" aria-busy="true">Yükleniyor…</div>}
          {list && rows.length === 0 && <EmptyState icon={Users} title="Eşleşen kişi yok">Süzgeci ya da aramayı değiştir.</EmptyState>}
          {rows.map((p) => (
            <button key={p.key} type="button" role="listitem" className={`pp-row ${openKey === p.key ? 'is-on' : ''}`} onClick={() => open(p.key)}>
              <Avatar name={p.name} photo={p.photoURL} online={p.online} />
              <span className="pp-row-main">
                <span className="pp-row-top">
                  <b>{p.name}</b>
                  {p.role === 'admin' && <span className="pp-tag is-accent">Yönetici</span>}
                  {p.kind === 'guest' && <span className="pp-tag">Misafir</span>}
                  <span className="pp-row-seen">{p.online ? 'çevrimiçi' : relTime(p.lastSeen)}</span>
                </span>
                <span className="pp-row-sub">
                  {[p.email, p.studentNumber && `No ${p.studentNumber}`, p.deviceCount ? `${p.deviceCount} cihaz` : null].filter(Boolean).join(' · ') || 'Girişsiz cihaz'}
                </span>
                <span className="pp-row-stats">
                  <span title="Toplam kullanım"><Clock aria-hidden />{fmtDuration(p.totalSeconds)}</span>
                  {p.counts.comment > 0 && <span title="Yorum"><MessageSquare aria-hidden />{p.counts.comment}</span>}
                  {p.counts.report > 0 && <span title="Bildirim" className="is-warn"><Flag aria-hidden />{p.counts.report}</span>}
                  {p.counts.question + p.counts.fragment + p.counts.option > 0 && (
                    <span title="Soru / ipucu / şık"><PenLine aria-hidden />{p.counts.question + p.counts.fragment + p.counts.option}</span>
                  )}
                  {p.counts.like > 0 && <span title="Beğeni"><ThumbsUp aria-hidden />{p.counts.like}</span>}
                  {p.accuracy !== null && <span title="Test doğruluğu"><Award aria-hidden />%{p.accuracy}</span>}
                </span>
              </span>
            </button>
          ))}
        </div>
      </section>

      <section className="pp-detail" aria-label="Kişi ayrıntısı">
        {!openKey && <EmptyState icon={Users} title="Bir kişi seç">Soldan bir kişiye dokun: cihazları, kullanım süresi, skorları ve tüm katkıları burada açılır.</EmptyState>}
        {openKey && detailErr && !detail && <p className="pp-error">{detailErr}</p>}
        {openKey && !detail && !detailErr && <div className="pp-skel" aria-busy="true">{loadingDetail ? 'Yükleniyor…' : ''}</div>}
        {openKey && detail && (
          <PersonPane
            key={detail.person.key}
            d={detail}
            tab={tab}
            setTab={setTab}
            onBack={() => open(null)}
            adminEmail={adminEmail}
            notify={notify}
            reload={() => {
              void refreshDetail(openKey, true);
              void refreshList();
            }}
          />
        )}
      </section>
    </div>
  );
};

const Kpi: React.FC<{ icon: React.ElementType; label: string; value: React.ReactNode; tone?: 'ok' }> = ({ icon: Icon, label, value, tone }) => (
  <div className={`pp-kpi ${tone ? `is-${tone}` : ''}`} role="listitem">
    <Icon aria-hidden />
    <span className="pp-kpi-v">{value}</span>
    <span className="pp-kpi-l">{label}</span>
  </div>
);

const Avatar: React.FC<{ name: string; photo?: string | null; online?: boolean; big?: boolean }> = ({ name, photo, online, big }) => (
  <span className={`pp-av ${big ? 'is-big' : ''}`}>
    {photo ? <img src={photo} alt="" referrerPolicy="no-referrer" /> : <span>{initial(name)}</span>}
    {online && <i className="pp-dot" aria-label="çevrimiçi" />}
  </span>
);

/* ------------------------------------------------------------------ */

const PersonPane: React.FC<{
  d: PersonDetail;
  tab: Tab;
  setTab: (t: Tab) => void;
  onBack: () => void;
  adminEmail: string;
  notify: (m: string) => void;
  reload: () => void;
}> = ({ d, tab, setTab, onBack, adminEmail, notify, reload }) => {
  const p = d.person;
  const [mode, setMode] = useState<'none' | 'mail' | 'edit'>('none');
  const online = d.devices.some((x) => x.online);
  const reports = d.items.filter((i) => i.kind === 'report');
  const contribs = d.items.filter((i) => ['comment', 'question', 'fragment', 'option', 'like', 'vote'].includes(i.kind));
  const notes = d.items.filter((i) => i.kind === 'note');
  const counts: Partial<Record<Tab, number>> = {
    etkinlik: d.events.length + d.activityLog.length,
    katkilar: contribs.length,
    bildirimler: reports.length,
    notlar: notes.length,
    skorlar: d.score.testCount,
    cihazlar: d.devices.length,
  };

  const copy = async (text: string, msg: string) => {
    try {
      await navigator.clipboard.writeText(text);
      notify(msg);
    } catch {
      notify(text);
    }
  };

  return (
    <div className="pp-pane">
      <header className="pp-head">
        <button type="button" className="pp-back ms-btn is-sm" onClick={onBack} aria-label="Listeye dön">
          <ArrowLeft />
        </button>
        <Avatar name={p.name} photo={p.photoURL} online={online} big />
        <div className="pp-head-main">
          <h2>
            {p.name}
            {p.role === 'admin' && <span className="pp-tag is-accent"><Shield aria-hidden /> Yönetici</span>}
            {p.kind === 'guest' && <span className="pp-tag">Misafir cihaz</span>}
            {online && <span className="pp-tag is-ok">çevrimiçi</span>}
          </h2>
          <dl className="pp-facts">
            {p.email && (<><dt>E-posta</dt><dd><a href={`mailto:${p.email}`}>{p.email}</a></dd></>)}
            {p.studentNumber && (<><dt>Numara</dt><dd>{p.studentNumber}</dd></>)}
            {p.phone && (<><dt>Telefon</dt><dd><a href={`tel:${p.phone}`}>{p.phone}</a></dd></>)}
            <dt>Kayıt</dt><dd>{fmtDateTime(p.createdAt)}</dd>
            <dt>Son giriş</dt><dd>{relTime(p.lastLoginAt || p.lastBackupAt)}</dd>
            {p.uid && (<><dt>Kimlik</dt><dd className="pp-mono">{p.uid}</dd></>)}
          </dl>
        </div>
        <div className="pp-head-actions">
          <button type="button" className="ms-btn is-sm" onClick={() => copy(personDeepLink(p.key, tab), 'Kişi bağlantısı kopyalandı.')} title="Bu kişinin panel bağlantısını kopyala">
            <Link2 /> Bağlantı
          </button>
          {p.email && (
            <button type="button" className={`ms-btn is-sm ${mode === 'mail' ? 'is-primary' : ''}`} onClick={() => setMode(mode === 'mail' ? 'none' : 'mail')}>
              <Mail /> E-posta
            </button>
          )}
          {p.uid && p.kind === 'account' && (
            <button type="button" className={`ms-btn is-sm ${mode === 'edit' ? 'is-primary' : ''}`} onClick={() => setMode(mode === 'edit' ? 'none' : 'edit')}>
              <Pencil /> Düzenle
            </button>
          )}
        </div>
      </header>

      {mode === 'mail' && p.email && <MailBox to={p.email} name={p.name} notify={notify} onDone={() => setMode('none')} />}
      {mode === 'edit' && p.uid && <EditBox d={d} adminEmail={adminEmail} notify={notify} onDone={() => { setMode('none'); reload(); }} />}

      <nav className="pp-tabs" role="tablist" aria-label="Kişi bölümleri">
        {TABS.map((x) => (
          <button key={x.id} type="button" role="tab" aria-selected={tab === x.id} className={`pp-tab ${tab === x.id ? 'is-on' : ''}`} onClick={() => setTab(x.id)}>
            {x.label}
            {counts[x.id] ? <span>{counts[x.id]}</span> : null}
          </button>
        ))}
      </nav>

      <div className="pp-body" role="tabpanel">
        {tab === 'ozet' && <Overview d={d} setTab={setTab} />}
        {tab === 'etkinlik' && <Timeline d={d} reload={reload} notify={notify} />}
        {tab === 'katkilar' && <ItemList items={contribs} adminEmail={adminEmail} notify={notify} reload={reload} empty="Yorum, soru, ipucu, şık ya da beğeni yok." filterable />}
        {tab === 'bildirimler' && <ItemList items={reports} adminEmail={adminEmail} notify={notify} reload={reload} empty="Hata bildirimi ya da öneri yok." />}
        {tab === 'notlar' && <ItemList items={notes} adminEmail={adminEmail} notify={notify} reload={reload} empty="Not yok." />}
        {tab === 'skorlar' && <Scores d={d} />}
        {tab === 'cihazlar' && <Devices d={d} notify={notify} reload={reload} />}
      </div>

      {p.uid && p.kind === 'account' && p.role !== 'admin' && (
        <footer className="pp-danger">
          <span>Hesabı sil: kullanıcı kaydı kalkar, katkıları kalır.</span>
          <ConfirmButton
            confirmLabel="Evet, sil"
            icon={Trash2}
            onConfirm={async () => {
              const r = await deleteManageUser(adminEmail, p.uid!);
              notify(r.message);
              if (r.ok) reload();
            }}
          >
            Hesabı sil
          </ConfirmButton>
        </footer>
      )}
    </div>
  );
};

/* ------------------------------ Özet ------------------------------ */

const Overview: React.FC<{ d: PersonDetail; setTab: (t: Tab) => void }> = ({ d, setTab }) => {
  // Son 30 gün: cihaz sayacı (sunucu) ile uygulama sayacından (profil) büyüğü
  const days = useMemo(() => {
    const m = new Map<string, number>();
    for (const x of d.usage.studyDaily) m.set(x.day, x.seconds);
    for (const x of d.usage.daily) m.set(x.day, Math.max(m.get(x.day) || 0, x.seconds));
    const out: { day: string; seconds: number }[] = [];
    for (let i = 29; i >= 0; i--) {
      const dt = new Date(Date.now() - i * 86400_000);
      const key = dt.toLocaleDateString('sv-SE', { timeZone: 'Europe/Istanbul' });
      out.push({ day: key, seconds: m.get(key) || 0 });
    }
    return out;
  }, [d]);
  const max = Math.max(60, ...days.map((x) => x.seconds));
  const week = days.slice(-7).reduce((a, x) => a + x.seconds, 0);
  const recent = useMemo(() => mergeTimeline(d).slice(0, 8), [d]);
  const s = d.score;
  return (
    <div className="pp-ov">
      <div className="pp-tiles">
        <Tile label="Toplam kullanım" value={fmtDuration(d.usage.totalSeconds)} sub={`${d.usage.sessions || 0} oturum`} />
        <Tile label="Son 7 gün" value={fmtDuration(week)} />
        <Tile label="Cihaz" value={d.devices.length} sub={d.devices[0]?.label} onClick={() => setTab('cihazlar')} />
        <Tile label="Test" value={s.testCount} sub={s.accuracy !== null ? `%${s.accuracy} doğru · net ${s.net}` : 'çözülmedi'} onClick={() => setTab('skorlar')} />
        <Tile label="Bildirim" value={d.items.filter((i) => i.kind === 'report').length} onClick={() => setTab('bildirimler')} tone="warn" />
        <Tile label="Katkı" value={d.items.filter((i) => ['comment', 'question', 'fragment', 'option'].includes(i.kind)).length} onClick={() => setTab('katkilar')} />
      </div>
      <div className="pp-card">
        <h3>Günlük kullanım <small>son 30 gün</small></h3>
        <div className="pp-bars" role="img" aria-label={`Son 30 günde toplam ${fmtDuration(days.reduce((a, x) => a + x.seconds, 0))}`}>
          {days.map((x) => (
            <span key={x.day} className="pp-bar" title={`${new Date(x.day).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })}: ${fmtDuration(x.seconds)}`}>
              <i style={{ height: `${Math.max(x.seconds ? 4 : 0, (x.seconds / max) * 100)}%` }} />
            </span>
          ))}
        </div>
        <div className="pp-bars-axis"><span>30 gün önce</span><span>bugün</span></div>
      </div>
      <div className="pp-card">
        <h3>Çalışma</h3>
        <ul className="pp-kv">
          <li><span>Öğren ilerlemesi</span><b>{d.study.progress} ders</b></li>
          <li><span>Hata defteri</span><b>{d.study.review}</b></li>
          <li><span>Favori</span><b>{d.study.favorites}</b></li>
          <li><span>Kart</span><b>{d.study.flashcards}</b></li>
          <li><span>Eşitlenen ayar</span><b>{d.study.kvCount}</b></li>
        </ul>
      </div>
      <div className="pp-card">
        <h3>Son hareketler <button type="button" className="pp-link" onClick={() => setTab('etkinlik')}>tümü</button></h3>
        {recent.length === 0 ? <p className="pp-muted">Henüz kayıt yok.</p> : <TimelineList rows={recent} />}
      </div>
    </div>
  );
};

const Tile: React.FC<{ label: string; value: React.ReactNode; sub?: React.ReactNode; onClick?: () => void; tone?: 'warn' }> = ({ label, value, sub, onClick, tone }) => {
  const Tag = onClick ? 'button' : 'div';
  return (
    <Tag type={onClick ? 'button' : undefined} className={`pp-tile ${tone ? `is-${tone}` : ''}`} onClick={onClick}>
      <span className="pp-tile-l">{label}</span>
      <span className="pp-tile-v">{value}</span>
      {sub ? <span className="pp-tile-s">{sub}</span> : null}
    </Tag>
  );
};

/* ---------------------------- Etkinlik ---------------------------- */

type TRow = { id: string; kind: string; label: string; body?: string; at: string; link?: string; device?: string | null; eventId?: number; src: 'db' | 'log' };
const mergeTimeline = (d: PersonDetail): TRow[] => {
  const devName = new Map(d.devices.map((x) => [x.device_id, x.label]));
  const rows: TRow[] = [
    ...d.events.map((e) => ({ id: `e${e.id}`, kind: e.kind, label: e.label, body: e.body, at: e.at, link: e.link, device: e.device_id ? devName.get(e.device_id) || 'cihaz' : null, eventId: e.id, src: 'db' as const })),
    ...d.activityLog.map((a, i) => ({ id: `a${i}`, kind: a.kind, label: a.text, at: a.at, src: 'log' as const })),
  ];
  return rows.filter((r) => r.at).sort((a, b) => String(b.at).localeCompare(String(a.at)));
};

const TimelineList: React.FC<{ rows: TRow[]; onDelete?: (r: TRow) => void }> = ({ rows, onDelete }) => {
  let lastDay = '';
  return (
    <ol className="pp-tl">
      {rows.map((r) => {
        const day = new Date(r.at).toLocaleDateString('tr-TR', { weekday: 'short', day: 'numeric', month: 'long' });
        const head = day !== lastDay ? day : '';
        lastDay = day;
        const Icon = KIND_META[r.kind]?.icon || Activity;
        return (
          <React.Fragment key={r.id}>
            {head && <li className="pp-tl-day">{head}</li>}
            <li className={`pp-tl-row is-${r.kind}`}>
              <span className="pp-tl-ic"><Icon aria-hidden /></span>
              <span className="pp-tl-main">
                <span className="pp-tl-top">
                  <b>{r.label}</b>
                  <time dateTime={r.at}>{new Date(r.at).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })}</time>
                </span>
                {r.body && <span className="pp-tl-body">{r.body}</span>}
                <span className="pp-tl-meta">
                  {r.src === 'log' ? 'uygulama günlüğü' : KIND_META[r.kind]?.label || r.kind}
                  {r.device ? ` · ${r.device}` : ''}
                  {r.link && (
                    <a href={siteLink(r.link)} target="_blank" rel="noreferrer">
                      <ExternalLink aria-hidden /> sitede aç
                    </a>
                  )}
                  {onDelete && r.eventId && (
                    <button type="button" className="pp-link is-danger" onClick={() => onDelete(r)}>
                      kaydı sil
                    </button>
                  )}
                </span>
              </span>
            </li>
          </React.Fragment>
        );
      })}
    </ol>
  );
};

const Timeline: React.FC<{ d: PersonDetail; reload: () => void; notify: (m: string) => void }> = ({ d, reload, notify }) => {
  const [kind, setKind] = useState('all');
  const all = useMemo(() => mergeTimeline(d), [d]);
  const kinds = useMemo(() => [...new Set(all.map((r) => r.kind))], [all]);
  const rows = kind === 'all' ? all : all.filter((r) => r.kind === kind);
  return (
    <div>
      <div className="pp-chips">
        <button type="button" className={`pp-chip ${kind === 'all' ? 'is-on' : ''}`} onClick={() => setKind('all')}>Tümü <span>{all.length}</span></button>
        {kinds.map((k) => (
          <button key={k} type="button" className={`pp-chip ${kind === k ? 'is-on' : ''}`} onClick={() => setKind(k)}>
            {KIND_META[k]?.label || ACT_LABEL[k] || k} <span>{all.filter((r) => r.kind === k).length}</span>
          </button>
        ))}
      </div>
      {rows.length === 0 ? (
        <EmptyState icon={Activity} title="Etkinlik yok">Bu kişi henüz bir şey yapmadı ya da günlük yeni başladı.</EmptyState>
      ) : (
        <TimelineList
          rows={rows.slice(0, 400)}
          onDelete={async (r) => {
            try {
              await deletePersonEvent(r.eventId!);
              notify('Kayıt silindi.');
              reload();
            } catch (e: any) {
              notify(e?.message || 'Silinemedi.');
            }
          }}
        />
      )}
    </div>
  );
};

/* ----------------------------- Öğeler ----------------------------- */

const ItemList: React.FC<{ items: PersonItem[]; adminEmail: string; notify: (m: string) => void; reload: () => void; empty: string; filterable?: boolean }> = ({
  items, adminEmail, notify, reload, empty, filterable,
}) => {
  const [kind, setKind] = useState('all');
  const kinds = useMemo(() => [...new Set(items.map((i) => i.kind))], [items]);
  const rows = kind === 'all' ? items : items.filter((i) => i.kind === kind);
  if (!items.length) return <EmptyState icon={MessageSquare} title={empty} />;

  const act = async (fn: () => Promise<{ ok: boolean; message: string }>) => {
    const r = await fn();
    notify(r.message);
    if (r.ok) reload();
  };

  return (
    <div>
      {filterable && kinds.length > 1 && (
        <div className="pp-chips">
          <button type="button" className={`pp-chip ${kind === 'all' ? 'is-on' : ''}`} onClick={() => setKind('all')}>Tümü <span>{items.length}</span></button>
          {kinds.map((k) => (
            <button key={k} type="button" className={`pp-chip ${kind === k ? 'is-on' : ''}`} onClick={() => setKind(k)}>
              {KIND_META[k]?.label || k} <span>{items.filter((i) => i.kind === k).length}</span>
            </button>
          ))}
        </div>
      )}
      <ul className="pp-items">
        {rows.map((it) => {
          const Icon = KIND_META[it.kind]?.icon || Activity;
          const resolved = it.status === 'resolved' || it.status === 'closed';
          return (
            <li key={`${it.kind}-${it.id}`} className={`pp-item is-${it.kind} ${resolved ? 'is-done' : ''}`}>
              <span className="pp-tl-ic"><Icon aria-hidden /></span>
              <div className="pp-item-main">
                <div className="pp-item-top">
                  <span className="pp-tag">{SOURCE_LABEL[it.source] || it.source}</span>
                  <b>{it.action === 'dislike' ? `Beğenmedi · ${it.title}` : it.title}</b>
                  {it.weak && <span className="pp-tag is-soft" title="Kayıtta hesap kimliği yok; adı eşleşti">ad eşleşmesi</span>}
                  {it.status && <span className={`pp-tag ${resolved ? 'is-ok' : 'is-warn'}`}>{resolved ? 'çözüldü' : 'bekliyor'}</span>}
                </div>
                {it.body && <p className="pp-item-body">{it.body}</p>}
                <div className="pp-item-meta">
                  <span>{it.at ? fmtDateTime(it.at) : 'tarih yok'}</span>
                  {it.link && (
                    <a href={siteLink(it.link)} target="_blank" rel="noreferrer"><ExternalLink aria-hidden /> Sitede aç</a>
                  )}
                  {it.link && (
                    <button type="button" className="pp-link" onClick={() => navigator.clipboard?.writeText(siteLink(it.link)).then(() => notify('Bağlantı kopyalandı.'))}>
                      <Copy aria-hidden /> bağlantı
                    </button>
                  )}
                  {it.kind === 'comment' && it.source === 'past' && it.questionId && (
                    <ConfirmButton className="pp-link is-danger" confirmLabel="Sil" onConfirm={() => act(() => deletePastComment(adminEmail, it.questionId!, it.id))}>
                      Yorumu sil
                    </ConfirmButton>
                  )}
                  {it.kind === 'report' && it.source === 'past' && !resolved && it.questionId && (
                    <button type="button" className="pp-link" onClick={() => act(() => resolveInboxReport(adminEmail, { id: it.id, questionId: it.questionId!, reason: it.title }))}>
                      <CheckCircle2 aria-hidden /> Çözüldü
                    </button>
                  )}
                  {it.kind === 'report' && it.source === 'learn' && !resolved && !it.messageId && (
                    <button
                      type="button"
                      className="pp-link"
                      onClick={() =>
                        act(async () => {
                          const r = await fetch(`/api/admin/learn-feedback/${encodeURIComponent(it.id)}/resolve`, { method: 'POST', headers: { 'x-admin-email': adminEmail } });
                          return { ok: r.ok, message: r.ok ? 'Bildirim çözüldü.' : 'Çözülemedi.' };
                        })
                      }
                    >
                      <CheckCircle2 aria-hidden /> Çözüldü
                    </button>
                  )}
                  {it.source === 'learn' && (it.kind === 'note' || it.messageId) && (
                    <ConfirmButton
                      className="pp-link is-danger"
                      confirmLabel="Sil"
                      onConfirm={() =>
                        act(async () => {
                          const url = it.kind === 'note' ? `/api/learn/social/notes/${encodeURIComponent(it.id)}` : `/api/learn/social/messages/${encodeURIComponent(it.messageId!)}`;
                          const r = await fetch(url, { method: 'DELETE', headers: { 'x-admin-email': adminEmail } });
                          return { ok: r.ok, message: r.ok ? 'Silindi.' : 'Silinemedi.' };
                        })
                      }
                    >
                      Sil
                    </ConfirmButton>
                  )}
                </div>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

/* ----------------------------- Skorlar ----------------------------- */

const Scores: React.FC<{ d: PersonDetail }> = ({ d }) => {
  const s = d.score;
  const byDisc = useMemo(() => {
    const m = new Map<string, { total: number; correct: number }>();
    for (const t of s.tests) for (const [k, v] of Object.entries(t.byDiscipline || {})) {
      const cur = m.get(k) || { total: 0, correct: 0 };
      cur.total += Number(v?.total) || 0;
      cur.correct += Number(v?.correct) || 0;
      m.set(k, cur);
    }
    return [...m.entries()].map(([k, v]) => ({ k, ...v, pct: v.total ? Math.round((v.correct / v.total) * 100) : 0 })).sort((a, b) => a.pct - b.pct);
  }, [s]);
  if (!s.testCount) return <EmptyState icon={Award} title="Test çözülmemiş">Bu kişinin kayıtlı test sonucu yok.</EmptyState>;
  return (
    <div className="pp-ov">
      <div className="pp-tiles">
        <Tile label="Test" value={s.testCount} />
        <Tile label="Doğru / Yanlış" value={`${s.correct} / ${s.wrong}`} sub={`${s.total} soru`} />
        <Tile label="Doğruluk" value={s.accuracy !== null ? `%${s.accuracy}` : '—'} sub={s.answeredAccuracy !== null ? `cevaplananda %${s.answeredAccuracy}` : undefined} />
        <Tile label="Net" value={s.net} sub="D − Y/4" />
      </div>
      {byDisc.length > 0 && (
        <div className="pp-card">
          <h3>Derslere göre</h3>
          <ul className="pp-meter">
            {byDisc.map((x) => (
              <li key={x.k}>
                <span>{x.k}</span>
                <span className="pp-meter-bar"><i style={{ width: `${x.pct}%` }} /></span>
                <b>%{x.pct}</b>
                <small>{x.correct}/{x.total}</small>
              </li>
            ))}
          </ul>
        </div>
      )}
      <div className="pp-card">
        <h3>Testler</h3>
        <div className="pp-table-wrap">
          <table className="pp-table">
            <thead><tr><th>Tarih</th><th>Test</th><th>D</th><th>Y</th><th>B</th><th>Süre</th></tr></thead>
            <tbody>
              {s.tests.map((t, i) => (
                <tr key={t.id || i}>
                  <td>{fmtDateTime(t.at)}</td>
                  <td>{t.title}</td>
                  <td className="is-ok">{t.correct}</td>
                  <td className="is-bad">{t.wrong}</td>
                  <td>{t.blank}</td>
                  <td>{fmtDuration(t.durationSec)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

/* ----------------------------- Cihazlar ----------------------------- */

const Devices: React.FC<{ d: PersonDetail; notify: (m: string) => void; reload: () => void }> = ({ d, notify, reload }) => {
  if (!d.devices.length)
    return <EmptyState icon={Monitor} title="Cihaz kaydı yok">Cihaz takibi yeni başladı: kişi siteyi bir sonraki açışında cihazı burada görünür.</EmptyState>;
  return (
    <ul className="pp-devs">
      {d.devices.map((x) => {
        const Icon = deviceIcon(`${x.label} ${x.platform}`);
        return (
          <li key={x.device_id} className="pp-dev">
            <span className="pp-dev-ic"><Icon aria-hidden />{x.online && <i className="pp-dot" />}</span>
            <div className="pp-dev-main">
              <b>{x.label || 'Cihaz'}</b>
              <span>{[x.platform, x.browser, x.model].filter(Boolean).join(' · ')}</span>
              <span className="pp-muted">
                İlk {fmtDateTime(x.first_seen)} · Son {x.online ? 'şimdi' : relTime(x.last_seen)} · {fmtDuration(x.active_seconds)} · {x.sessions} oturum
                {x.verified ? ' · hesapla doğrulandı' : ''}
              </span>
              {x.last_path && <span className="pp-muted pp-mono">{x.last_path}</span>}
            </div>
            <ConfirmButton
              className="pp-link is-danger"
              confirmLabel="Unut"
              onConfirm={async () => {
                try {
                  await forgetDevice(x.device_id);
                  notify('Cihaz unutuldu.');
                  reload();
                } catch (e: any) {
                  notify(e?.message || 'Silinemedi.');
                }
              }}
            >
              Unut
            </ConfirmButton>
          </li>
        );
      })}
    </ul>
  );
};

/* ----------------------------- Eylemler ----------------------------- */

const MailBox: React.FC<{ to: string; name: string; notify: (m: string) => void; onDone: () => void }> = ({ to, name, notify, onDone }) => {
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState(`Merhaba ${name},\n\n`);
  const [busy, setBusy] = useState(false);
  return (
    <form
      className="pp-form"
      onSubmit={async (e) => {
        e.preventDefault();
        if (!subject.trim() || !body.trim()) return;
        setBusy(true);
        const r = await sendUserEmail(to, subject.trim(), body);
        setBusy(false);
        notify(r.message);
        if (r.ok) onDone();
      }}
    >
      <div className="pp-form-top"><b>E-posta · {to}</b><button type="button" className="pp-link" onClick={onDone} aria-label="Kapat"><X /></button></div>
      <input value={subject} onChange={(e) => setSubject(e.target.value)} placeholder="Konu" aria-label="Konu" required />
      <textarea value={body} onChange={(e) => setBody(e.target.value)} rows={5} aria-label="İleti" required />
      <button type="submit" className="ms-btn is-sm is-primary" disabled={busy}><Mail /> {busy ? 'Gönderiliyor…' : 'Gönder'}</button>
    </form>
  );
};

const EditBox: React.FC<{ d: PersonDetail; adminEmail: string; notify: (m: string) => void; onDone: () => void }> = ({ d, adminEmail, notify, onDone }) => {
  const p = d.person;
  const [name, setName] = useState(p.name || '');
  const [num, setNum] = useState(p.studentNumber || '');
  const [phone, setPhone] = useState(p.phone || '');
  const [role, setRole] = useState(p.role === 'admin' ? 'admin' : 'student');
  const [busy, setBusy] = useState(false);
  return (
    <form
      className="pp-form"
      onSubmit={async (e) => {
        e.preventDefault();
        setBusy(true);
        try {
          await ApiService.adminUpdateUser(adminEmail, p.uid!, { displayName: name.trim(), studentNumber: num.trim() || null, phone: phone.trim() || null, role });
          notify('Kullanıcı güncellendi.');
          onDone();
        } catch (err: any) {
          notify(err?.message || 'Güncellenemedi.');
        } finally {
          setBusy(false);
        }
      }}
    >
      <div className="pp-form-top"><b>Hesabı düzenle</b><button type="button" className="pp-link" onClick={onDone} aria-label="Kapat"><X /></button></div>
      <div className="pp-form-grid">
        <label>Ad<input value={name} onChange={(e) => setName(e.target.value)} /></label>
        <label>Öğrenci no<input value={num} onChange={(e) => setNum(e.target.value)} inputMode="numeric" /></label>
        <label>Telefon<input value={phone} onChange={(e) => setPhone(e.target.value)} inputMode="tel" /></label>
        <label>Rol
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="student">Öğrenci</option>
            <option value="admin">Yönetici</option>
          </select>
        </label>
      </div>
      <button type="submit" className="ms-btn is-sm is-primary" disabled={busy}><Save /> {busy ? 'Kaydediliyor…' : 'Kaydet'}</button>
    </form>
  );
};

/** v12 görünümünün yeniden kullandığı parçalar (ManagePeopleV12'ye prop olarak geçer; döngüsel içe aktarma yok). */
const PEOPLE_V12_PARTS = { Timeline, ItemList, Scores, Devices, MailBox, EditBox, mergeTimeline, contribTotal };
export type PeopleV12Parts = typeof PEOPLE_V12_PARTS;
