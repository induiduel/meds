import React, { useEffect, useState } from 'react';
import {
  Database, Globe, HardDrive, Link2, Users, Boxes, Activity, Github, Flame, Cloud, KeyRound, FolderOpen, Terminal, Copy, Server, Search, FileUp, NotebookPen, CloudUpload, FolderPlus, ShieldCheck,
} from 'lucide-react';
import { Panel } from './consoleUi';
import { PageActions, Toolbar, SearchField, Pill, Card14 } from '../v14/pageKit';
import { NAV_TREE } from '../shell/navModel';
import { pathFor } from '../../router';
import { siteLink } from '../../services/peopleService';
import { ORACLE_API_URL, PANEL_ON_ORACLE_AT_BOOT } from '../../config/deployment';
import { FIREBASE_PROJECT_ID } from '../../services/auth';
import { DRIVE_FOLDER_URL } from '../../data/driveCatalog';
import './db-explorer.css';

/**
 * Yönetim › Kısayollar: panelin veri ekranları, canlı sitenin her sayfası, API/sağlık uçları, dış yönetim konsolları
 * (Drive, GitHub, Firebase, Oracle, Cloudflare, AI anahtarları) ve veritabanına bağlanma komutları tek yerde.
 * v14 (canvas Kisayollar.dc.html): üstte uç sağlığı rozetleri, arama, gruplu bağlantı kartları ve klavye kısayolları.
 */
type Card = { label: string; hint: string; icon: React.ElementType; href?: string; section?: string };

const goSection = (slug: string) => {
  window.history.pushState({ route: 'manage', param: slug }, '', `/manage/${slug}`);
  window.dispatchEvent(new PopStateEvent('popstate'));
};
const apiBase = () => (PANEL_ON_ORACLE_AT_BOOT ? ORACLE_API_URL.replace(/\/$/, '') : window.location.origin);

const VERI: Card[] = [
  { label: 'Veritabanı gezgini', hint: 'meds-pg tüm tablolar: ara, düzenle, ekle, sil', icon: Database, section: 'veritabani-gezgini' },
  { label: 'Kişiler ve çalışma', hint: 'Kim ne çalıştı, kaç saat, neleri bitirdi', icon: Users, section: 'kisiler' },
  { label: 'Veri kataloğu', hint: 'Çıkmış, örnek soru, deste, sözlük, kart, hastalık', icon: Boxes, section: 'veri-katalogu' },
  { label: 'Veritabanı ve yedek', hint: 'Etkin veritabanı, eşitleme, dışa/içe aktarım', icon: HardDrive, section: 'veritabani' },
  { label: 'Sistem ve günlükler', hint: 'Servis sağlığı, AI, tarayıcı konsolu', icon: Activity, section: 'sistem' },
];

const act = (k: string) => window.dispatchEvent(new CustomEvent('meds:admin-action', { detail: k }));
const ISLEM: { label: string; hint: string; icon: React.ElementType; k: string }[] = [
  { label: 'Faz 14 · test edilen çıkmışlar', hint: 'Çıkmış soru test sonuçları', icon: Activity, k: 'faz14' },
  { label: 'Veritabanı ve limitler', hint: 'Kota ve kullanım tanılaması', icon: Activity, k: 'diagnostics' },
  { label: 'Çıkmış soru yükle', hint: 'PDF/metinden çıkmış soru içe aktar', icon: FileUp, k: 'pastExam' },
  { label: 'NotebookLM / Gemini', hint: 'Kaynak paketi ve istem', icon: NotebookPen, k: 'notebooklm' },
  { label: "Drive'a kaydet", hint: 'Yedeği Drive’a yükle', icon: CloudUpload, k: 'drive' },
  { label: 'Yeni kurul ekle', hint: 'Kurul oluştur', icon: FolderPlus, k: 'newCommittee' },
  { label: 'AI alt ajan izleme', hint: 'Çalışan alt ajanlar', icon: ShieldCheck, k: 'subagents' },
];

const DIS: Card[] = [
  { label: 'Canlı site', hint: 'nofrostlife.com.tr', icon: Globe, href: 'https://nofrostlife.com.tr' },
  { label: 'Canlı yönetim paneli', hint: 'nofrostlife.com.tr/manage', icon: Server, href: 'https://nofrostlife.com.tr/manage' },
  { label: 'Drive ders klasörü', hint: 'Ders işçisinin izlediği PDF klasörü', icon: FolderOpen, href: DRIVE_FOLDER_URL },
  { label: 'GitHub deposu', hint: 'induiduel/meds', icon: Github, href: 'https://github.com/induiduel/meds' },
  { label: 'Firebase konsolu', hint: `${FIREBASE_PROJECT_ID} · kimlik doğrulama`, icon: Flame, href: `https://console.firebase.google.com/project/${FIREBASE_PROJECT_ID}/authentication/users` },
  { label: 'Oracle Cloud', hint: 'VM, disk, ağ (92.5.55.109)', icon: Cloud, href: 'https://cloud.oracle.com/compute/instances' },
  { label: 'Cloudflare', hint: 'Alan adı, tünel (meds-tunnel)', icon: Cloud, href: 'https://dash.cloudflare.com' },
  { label: 'Gemini API anahtarları', hint: 'Google AI Studio', icon: KeyRound, href: 'https://aistudio.google.com/app/apikey' },
];

const KOMUT: [string, string][] = [
  ['Canlı veritabanına tünel (sonra psql/DBeaver: localhost:54331, kullanıcı ve veritabanı meds)', 'meds/deploy/oracle/db-yonet.sh'],
  ['Canlı psql (tünel açıkken)', 'psql -h 127.0.0.1 -p 54331 -U meds -d meds'],
  ['Yerel veritabanı (bu bilgisayar)', 'docker exec -it meds-pg psql -U meds -d meds'],
  ['Oracle sunucusuna bağlan', 'ssh medsor-oracle'],
  ['Canlı uygulama günlüğü', 'docker --context oracle logs -f --tail 200 meds-app'],
  ['Yerel sunucuyu yeniden başlat', 'systemctl --user restart meds-web'],
];

const CardView: React.FC<{ c: Card }> = ({ c }) => {
  const Icon = c.icon;
  const body = (
    <>
      <Icon aria-hidden />
      <span><b>{c.label}</b><small>{c.hint}</small></span>
    </>
  );
  return c.section ? (
    <button type="button" className="ksy-card" onClick={() => goSection(c.section!)}>{body}</button>
  ) : (
    <a className="ksy-card" href={c.href} target="_blank" rel="noreferrer">{body}</a>
  );
};

export const ManageShortcuts: React.FC<{ notify: (m: string) => void }> = ({ notify }) => {
  const api = apiBase();
  const API: Card[] = [
    { label: 'Sağlık', hint: `${api}/api/health`, icon: Activity, href: `${api}/api/health` },
    { label: 'Vektör kapsamı', hint: '/api/rag/vectors/health', icon: Search, href: `${api}/api/rag/vectors/health` },
    { label: 'Herkese açık API dizini', hint: '/v1', icon: Link2, href: `${api}/v1` },
    { label: 'API belgesi', hint: '/v1/documentation', icon: Link2, href: `${api}/v1/documentation` },
  ];
  const [q, setQ] = useState('');
  const [health, setHealth] = useState<Record<string, number | 'hata' | null>>({ health: null, vec: null });
  useEffect(() => {
    let alive = true;
    const probe = (k: string, url: string) =>
      fetch(url, { cache: 'no-store' })
        .then((r) => alive && setHealth((h) => ({ ...h, [k]: r.status })))
        .catch(() => alive && setHealth((h) => ({ ...h, [k]: 'hata' })));
    void probe('health', `${api}/api/health`);
    void probe('vec', `${api}/api/rag/vectors/health`);
    return () => { alive = false; };
  }, [api]);
  const fq = q.toLocaleLowerCase('tr-TR').trim();
  const match = (c: Card) => !fq || `${c.label} ${c.hint}`.toLocaleLowerCase('tr-TR').includes(fq);
  const tone = (v: number | 'hata' | null) => (v === null ? '' : v === 200 ? 'ok' : 'bad');
  const copy = (s: string) => {
    void navigator.clipboard?.writeText(s).then(() => notify('Komut panoya kopyalandı.'), () => notify(s));
  };
  const kartlar = (list: Card[]) => {
    const l = list.filter(match);
    return l.length ? <div className="ksy-grid">{l.map((c) => <CardView key={c.label} c={c} />)}</div> : <p className="pk14-note">Aramaya uyan bağlantı yok.</p>;
  };
  return (
    <div className="ksy">
      <PageActions>
        <Pill tone={tone(health.health)}>/api/health {health.health ?? '…'}</Pill>
        <Pill tone={tone(health.vec)}>Vektör servisi {health.vec ?? '…'}</Pill>
      </PageActions>
      <Toolbar>
        <SearchField value={q} onChange={setQ} placeholder="Bağlantı ya da yol ara" label="Kısayol ara" />
      </Toolbar>
      <Panel title="Veri ve veritabanı" icon={Database} desc="Panelin içindeki veri ekranları — tüm site verisi buradan görülür ve düzenlenir.">
        {kartlar(VERI)}
      </Panel>
      <Panel title="Yönetici işlemleri" icon={ShieldCheck} desc="Hesap menüsünden buraya taşındı.">
        <div className="ksy-grid">
          {ISLEM.filter((c) => match(c)).map((c) => (
            <button key={c.k} type="button" className="ksy-card" onClick={() => act(c.k)}>
              <c.icon aria-hidden /><span><b>{c.label}</b><small>{c.hint}</small></span>
            </button>
          ))}
        </div>
      </Panel>
      <Panel title="Veritabanına bağlan" icon={Terminal} desc="Masaüstü araçla (psql, DBeaver, TablePlus) doğrudan bağlanmak için. Parola Oracle'da ~/medsor/meds/.env → MEDS_PG_PASSWORD.">
        <div className="ksy-grid" style={{ gridTemplateColumns: 'minmax(0,1fr)' }}>
          {KOMUT.filter(([l, cmd]) => !fq || `${l} ${cmd}`.toLocaleLowerCase('tr-TR').includes(fq)).map(([l, cmd]) => (
            <div key={cmd} className="ksy-cmd">
              <span style={{ flex: '0 1 300px', minWidth: 0 }}>{l}</span>
              <code>{cmd}</code>
              <button type="button" className="m14-btn icon" onClick={() => copy(cmd)} aria-label={`Kopyala: ${cmd}`}><Copy aria-hidden /></button>
            </div>
          ))}
        </div>
      </Panel>
      <Panel title="Sitenin sayfaları" icon={Globe} desc={PANEL_ON_ORACLE_AT_BOOT || !/localhost|127\.0\.0\.1/.test(window.location.hostname) ? 'Canlı sitede yeni sekmede açılır.' : 'Bu sunucuda yeni sekmede açılır.'}>
        {NAV_TREE.map((g, i) => {
          const items = g.items.map((it) => ({ label: it.label, hint: pathFor(it.id), icon: it.icon, href: siteLink(pathFor(it.id)), id: it.id })).filter(match);
          if (!items.length) return null;
          return (
            <div key={g.label || i} style={{ marginBottom: 10 }}>
              {g.label && <h3 className="ms-panel-desc" style={{ margin: '0 0 6px', fontWeight: 600 }}>{g.label}</h3>}
              <div className="ksy-grid">
                {items.map((it) => <CardView key={it.id} c={it} />)}
              </div>
            </div>
          );
        })}
      </Panel>
      <Panel title="API ve sağlık" icon={Link2}>
        {kartlar(API)}
      </Panel>
      <Panel title="Dış yönetim konsolları" icon={Cloud}>
        {kartlar(DIS)}
      </Panel>
      <Card14 title="Klavye">
        <ul className="flex flex-wrap gap-x-5 gap-y-2 m-0 p-0 list-none text-sm text-ink-2">
          <li><kbd className="m14-kbd">Ctrl K</kbd> sayfa ara</li>
          <li><kbd className="m14-kbd">X</kbd> ya da <kbd className="m14-kbd">Boşluk</kbd> satırı seç</li>
          <li><kbd className="m14-kbd">Enter</kbd> ayrıntıyı aç</li>
          <li><kbd className="m14-kbd">Esc</kbd> listeye dön</li>
        </ul>
      </Card14>
    </div>
  );
};
