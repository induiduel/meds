import React, { useEffect, useState, useMemo, useLayoutEffect, useRef } from 'react';
import { Segmented } from './ui/kit';
import { PageHeader } from './ui/PageHeader';
import '../styles/v12/secondary.css';
import { EmptySearch } from './ui/Animations';
import { Award, ChevronDown, Search } from 'lucide-react';
import { QuestionItem, Committee } from '../types';
import { AppUser } from '../services/auth';
import { calismaGetir, siralamaGetir, sureYaz, useBasarim, type SiraSatir } from '../services/basarimIstemci';
import { AtpIkon } from './basarim/ortak';
import { navigateTo, pathFor } from '../router';
import '../styles/basarim.css';

interface LeaderboardViewProps {
  questions: QuestionItem[];
  committees: Committee[];
  selectedCommitteeId: string;
  onSelectCommittee: (id: string) => void;
  currentUser: AppUser | null;
  onOpenContributeModal: () => void;
}


/**
 * Sıralama (/siralama): sunucudaki başarım puanı (services/basarim) — dönem içinde Bu hafta / Bu kurul / Tüm zamanlar.
 * Puan çalışma süresi, çözülen soru, bitirilen ders, hedef/başarım ödülleri ve topluluk katkılarından gelir.
 * Haftalık ve kurul sonu ilk 5'e ATP verilir (rozetlerle gösterilir). Unvan ve çerçeve kilit mağazasından gelir.
 */
type Kapsam = 'hafta' | 'kurul' | 'tum';
export const LeaderboardView: React.FC<LeaderboardViewProps> = ({ currentUser }) => {
  const { durum, tanim } = useBasarim();
  const [kapsam, setKapsam] = useState<Kapsam>('hafta');
  const [tur, setTur0] = useState<'puan' | 'calisma'>(() => { try { return new URLSearchParams(location.search).get('tur') === 'calisma' ? 'calisma' : 'puan'; } catch { return 'puan'; } });
  const setTur = (t: 'puan' | 'calisma') => { setTur0(t); try { const u = new URL(location.href); if (t === 'calisma') u.searchParams.set('tur', t); else u.searchParams.delete('tur'); history.replaceState(history.state, '', u); } catch { /* */ } };
  const [donem, setDonem] = useState<number | null>(null);
  const [veri, setVeri] = useState<{ donem: number; pencere: { ad: string; bas: string; son: string }; satir: SiraSatir[]; atpOdul: number[] } | null>(null);
  const [hata, setHata] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const listRef = useRef<HTMLOListElement>(null);
  const lastPos = useRef<Map<string, number>>(new Map());
  const etkinDonem = donem || durum?.profil.donem || 3;

  useEffect(() => {
    let canli = true;
    const al = () => siralamaGetir(kapsam, etkinDonem).then((v) => { if (canli) { setVeri(v); setHata(''); } }, (e) => canli && setHata(e.message));
    void al();
    const t = window.setInterval(() => { if (document.visibilityState === 'visible') void al(); }, 60_000);
    // Herhangi bir öğrencinin puanı değişince sunucu `siralama_changed` yayar: anında tazele
    let kapat: (() => void) | null = null;
    void import('../services/realtimeEvents').then(({ realtimeEventService }) => {
      if (canli) kapat = realtimeEventService.on('siralama_changed', () => { if (document.visibilityState === 'visible') void al(); });
    }).catch(() => 0);
    return () => { canli = false; window.clearInterval(t); kapat?.(); };
  }, [kapsam, etkinDonem, durum?.puan.toplam]);

  const leaderboard = veri?.satir || [];
  const filteredLeaderboard = useMemo(() => {
    if (!searchTerm.trim()) return leaderboard;
    const term = searchTerm.toLocaleLowerCase('tr-TR');
    return leaderboard.filter((item) => item.ad.toLocaleLowerCase('tr-TR').includes(term));
  }, [leaderboard, searchTerm]);
  const top3 = leaderboard.slice(0, 3);
  const me = leaderboard.find((x) => x.ben);

  // Canlı sıralama: sıra değişince satırlar eski yerinden yenisine kayar (FLIP)
  useLayoutEffect(() => {
    const ol = listRef.current;
    if (!ol) return;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const next = new Map<string, number>();
    ol.querySelectorAll<HTMLElement>('li[data-id]').forEach((li) => {
      const id = li.dataset.id!;
      const top = li.offsetTop;
      next.set(id, top);
      const prev = lastPos.current.get(id);
      if (!reduce && prev !== undefined && prev !== top) {
        li.animate([{ transform: `translateY(${prev - top}px)` }, { transform: 'none' }], { duration: 320, easing: 'cubic-bezier(.32,.72,0,1)' });
      }
    });
    lastPos.current = next;
  });
  const maxPoints = Math.max(1, leaderboard[0]?.puan || 1);
  const initials = (name: string) =>
    name.split(/[^\p{L}\p{N}]+/u).filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toLocaleUpperCase('tr-TR') || '?';
  const esik = kapsam === 'hafta' ? tanim.atp.siralamaEsikPuan.hafta : kapsam === 'kurul' ? tanim.atp.siralamaEsikPuan.kurul : 0;
  const atpRozet = (sira: number, puan: number) => {
    const a = veri?.atpOdul?.[sira - 1];
    return a && puan >= esik ? <span className="lbx-atp" title={`Dönem sonunda ${a} mol ATP`}><AtpIkon boyut={10} />{a}</span> : null;
  };
  const cerceve = (c?: string) => (c ? ` bs-cerceve ${c}` : '');

  return (
    <div className="ds-page o12-page o12-lb">
      <PageHeader
        title="Sıralama"
        stats={[
          { label: 'kişi', value: leaderboard.length },
          ...(me ? [{ label: 'senin sıran', value: `${me.sira}.`, tone: 'accent' as const }] : []),
        ]}
        description={`${etkinDonem}. Dönem · ${veri?.pencere.ad || ''}. Puan çalışma, soru, bitirilen ders, hedef ve katkılardan gelir; ${kapsam === 'tum' ? 'haftalık ve kurul sonu ilk 5 ATP kazanır' : `ilk 5 ATP kazanır (en az ${esik.toLocaleString('tr-TR')} puan)`}.`}
        actions={
          <button type="button" onClick={() => navigateTo(pathFor('basarimlar'))} className="ms-btn is-primary">
            <Award aria-hidden />
            Başarımlarım
          </button>
        }
      />

      <div className="ds-toolbar">
        <Segmented<'puan' | 'calisma'>
          className="lb-scope"
          label="Sıralama türü"
          value={tur}
          onChange={setTur}
          options={[{ value: 'puan', label: 'Puan' }, { value: 'calisma', label: 'Çalışma süresi' }]}
        />
        {tur === 'puan' && <Segmented<Kapsam>
          className="lb-scope"
          label="Kapsam"
          value={kapsam}
          onChange={setKapsam}
          options={[{ value: 'hafta', label: 'Bu hafta' }, { value: 'kurul', label: 'Bu kurul' }, { value: 'tum', label: 'Tüm zamanlar' }]}
        />}
        <label className="ds-select">
          <span>Dönem</span>
          <select value={etkinDonem} onChange={(e) => setDonem(Number(e.target.value))} aria-label="Dönem">
            {[1, 2, 3, 4, 5, 6].map((d) => <option key={d} value={d}>{d}. Dönem</option>)}
          </select>
          <ChevronDown aria-hidden />
        </label>
      </div>
      {hata && <p className="lbx-hata" role="status">{hata}</p>}

      {tur === 'calisma' ? <CalismaSiralama donem={etkinDonem} photo={currentUser?.photoURL || null} /> : (<>
      {top3.some((t) => t.puan > 0) && (
        <ol className="lbx-podium" aria-label="İlk üç">
          {[1, 0, 2].map((i) => {
            const item = top3[i];
            if (!item) return <li key={i} className="lbx-col is-empty" aria-hidden />;
            const photo = (item.ben && currentUser?.photoURL) || item.foto || null;
            return (
              <li key={`${item.sira}-${item.ad}`} className={`lbx-col t${i + 1} ${item.ben ? 'is-me' : ''}`}>
                <span className="lbx-who">
                  {i === 0 && <CrownIcon className="lbx-crown" />}
                  <span className={`lbx-av${cerceve(item.cerceve)}`}>{photo ? <img src={photo} alt="" referrerPolicy="no-referrer" /> : initials(item.ad)}</span>
                  <b className={item.renk ? `bs-isim ${item.renk}` : undefined}>{item.ad}</b>
                  {item.unvan && <span className={`lbx-unvan${item.ozel ? " bs-ozel-unvan" : ""}`}>{item.unvan}</span>}
                </span>
                <span className="lbx-step">
                  <span className="lbx-rk">{i + 1}</span>
                  <span className="lbx-pt">{item.puan.toLocaleString('tr-TR')} puan</span>
                  {kapsam !== 'tum' && atpRozet(i + 1, item.puan)}
                </span>
              </li>
            );
          })}
        </ol>
      )}

      <section className="lbx-list" aria-label="Sıralama listesi">
        <label className="lbx-search">
          <Search aria-hidden />
          <input type="search" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} placeholder="Rumuz ara" aria-label="Kişi ara" />
          <span className="lbx-count">{filteredLeaderboard.length} kişi</span>
        </label>
        <div className="lbx-row is-head" aria-hidden><span>SIRA</span><span /><span>KİŞİ</span><span>PUAN</span><span /></div>
        {!veri && !hata ? (
          <div className="ds-empty"><b>Yükleniyor…</b></div>
        ) : filteredLeaderboard.length === 0 ? (
          <div className="ds-empty"><EmptySearch size={56} /><b>{searchTerm ? 'Aramaya uyan kişi yok' : 'Bu dönemde henüz puan alan yok'}</b></div>
        ) : (
          <ol className="lbx-rows" ref={listRef}>
            {filteredLeaderboard.map((item) => (
              <li key={`${item.sira}-${item.ad}`} data-id={`${item.ad}`} className={`lbx-row ${item.ben ? 'is-me' : ''}`}>
                <span className={`lbx-rank ${item.sira <= 3 ? `t${item.sira}` : ''}`}>{item.sira}</span>
                <span className={`lbx-av is-sm${cerceve(item.cerceve)}`}>{(item.ben && currentUser?.photoURL) || item.foto ? <img src={(item.ben && currentUser?.photoURL) || item.foto} alt="" referrerPolicy="no-referrer" /> : initials(item.ad)}</span>
                <span className="lbx-name">
                  <b className={item.renk ? `bs-isim ${item.renk}` : undefined}>{item.ad}{item.ben && <span className="lbx-me">Sen</span>}</b>
                  <span>{item.kidem ? `${item.kidem} · ` : ''}{item.unvan ? `${item.unvan} · ` : ''}{item.basarim} başarım seviyesi{kapsam !== 'tum' && item.sira <= 5 ? ' · ' : ''}{kapsam !== 'tum' && item.sira <= 5 && atpRozet(item.sira, item.puan)}</span>
                </span>
                <span className="lbx-bar" aria-hidden><i style={{ width: `${Math.max(item.puan > 0 ? 3 : 0, (item.puan / maxPoints) * 100)}%` }} /></span>
                <span className="lbx-pts">{item.puan.toLocaleString('tr-TR')}</span>
              </li>
            ))}
          </ol>
        )}
      </section>
      </>)}
    </div>
  );
};

/** "Dönem 3 - Kurul 1: TIP 310 - Ürogenital ve Obstetrik Kurulu" → "Kurul 1 · Ürogenital ve Obstetrik Kurulu" (seçim kutusu dar ekranda kesmesin) */
function committeeLabel(c: Committee) {
  const no = c.name.match(/Kurul\s*(\d+)/i)?.[1];
  const head = no ? `Kurul ${no}` : /final/i.test(c.id + c.name) ? 'Final' : /b[uü]t[uü]nleme/i.test(c.id + c.name) ? 'Bütünleme' : '';
  const topic = (c.name.split(':')[1] || '').replace(/^\s*TIP\s*\d+\s*[-–]\s*/i, '').replace(/\s+kurulu\s*$/i, '').trim();
  return head ? (topic ? `${head} · ${topic}` : head) : c.name;
}

function CrownIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5zm14 3c0 .6-.4 1-1 1H6c-.6 0-1-.4-1-1v-1h14v1z" />
    </svg>
  );
}

/** Çalışma süresi sıralaması: bugün / bu hafta; her satırda en çok çalışılan dersler. Hafta birincisine ATP. */
function CalismaSiralama({ donem, photo }: { donem: number; photo: string | null }) {
  const [kapsam, setKapsam] = useState<'gun' | 'hafta'>('hafta');
  const [veri, setVeri] = useState<Awaited<ReturnType<typeof calismaGetir>> | null>(null);
  const [hata, setHata] = useState('');
  const [acik, setAcik] = useState<number | null>(null);
  useEffect(() => {
    let canli = true;
    const al = () => calismaGetir(kapsam, donem).then((v) => { if (canli) { setVeri(v); setHata(''); } }, (e) => canli && setHata(e.message));
    void al();
    const t = window.setInterval(() => { if (document.visibilityState === 'visible') void al(); }, 60_000);
    return () => { canli = false; window.clearInterval(t); };
  }, [kapsam, donem]);
  const enCok = Math.max(1, veri?.satir[0]?.sn || 1);
  const bas = (ad: string) => ad.split(/[^\p{L}\p{N}]+/u).filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toLocaleUpperCase('tr-TR') || '?';
  return (
    <section className="lbx-list lbc" aria-label="Çalışma süresi sıralaması">
      <div className="lbc-ust">
        <Segmented<'gun' | 'hafta'> className="lb-scope" label="Dönem aralığı" value={kapsam} onChange={setKapsam} options={[{ value: 'gun', label: 'Bugün' }, { value: 'hafta', label: 'Bu hafta' }]} />
        {kapsam === 'hafta' && !!veri?.odul && (
          <span className="lbc-odul"><AtpIkon boyut={11} /> Haftanın birincisine {veri.odul} mol ATP{veri.esikSn ? ` (en az ${Math.round(veri.esikSn / 3600)} sa)` : ''}</span>
        )}
        {veri?.benim && <span className="lbc-ben">Senin sıran: <b>{veri.benim}.</b></span>}
      </div>
      {hata && <p className="lbx-hata" role="status">{hata}</p>}
      {!veri && !hata ? <div className="ds-empty"><b>Yükleniyor…</b></div> : !veri?.satir.length ? (
        <div className="ds-empty"><EmptySearch size={56} /><b>{kapsam === 'gun' ? 'Bugün henüz çalışan yok' : 'Bu hafta henüz çalışan yok'}</b></div>
      ) : (
        <ol className="lbc-satirlar">
          {veri.satir.map((x) => (
            <li key={`${x.sira}-${x.ad}`} className={`lbc-satir${x.ben ? ' is-me' : ''}${x.sira <= 3 ? ` t${x.sira}` : ''}`}>
              <button type="button" className="lbc-bas" onClick={() => setAcik(acik === x.sira ? null : x.sira)} aria-expanded={acik === x.sira}>
                <span className={`lbx-rank ${x.sira <= 3 ? `t${x.sira}` : ''}`}>{x.sira}</span>
                <span className={`lbx-av is-sm${x.cerceve ? ` bs-cerceve ${x.cerceve}` : ''}`}>{(x.ben && photo) || x.foto ? <img src={(x.ben && photo) || x.foto} alt="" referrerPolicy="no-referrer" /> : bas(x.ad)}</span>
                <span className="lbc-kim">
                  <b className={x.renk ? `bs-isim ${x.renk}` : undefined}>{x.ad}{x.ben && <span className="lbx-me">Sen</span>}</b>
                  <small>{x.kidem ? `${x.kidem} · ` : ''}{x.dersler[0] ? `en çok: ${x.dersler[0].ad}` : 'ders bilgisi yok'}</small>
                </span>
                <span className="lbc-cubuk" aria-hidden><i style={{ width: `${(x.sn / enCok) * 100}%` }} /></span>
                <span className="lbc-sure">{sureYaz(x.sn)}</span>
              </button>
              {acik === x.sira && x.dersler.length > 0 && (
                <ol className="lbc-dersler">
                  {x.dersler.map((d) => (
                    <li key={d.id}><span>{d.ad}<small>{d.modul}</small></span><b>{sureYaz(d.sn)}</b></li>
                  ))}
                </ol>
              )}
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
