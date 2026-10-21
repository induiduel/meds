import React, { useEffect, useState, useMemo, useLayoutEffect, useRef } from 'react';
import { Segmented } from './ui/kit';
import { PageHeader } from './ui/PageHeader';
import '../styles/v12/secondary.css';
import { EmptySearch } from './ui/Animations';
import { Award, ChevronDown, Search } from 'lucide-react';
import { QuestionItem, Committee } from '../types';
import { AppUser } from '../services/auth';
import { siralamaGetir, useBasarim, type SiraSatir } from '../services/basarimIstemci';
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
        <Segmented<Kapsam>
          className="lb-scope"
          label="Kapsam"
          value={kapsam}
          onChange={setKapsam}
          options={[{ value: 'hafta', label: 'Bu hafta' }, { value: 'kurul', label: 'Bu kurul' }, { value: 'tum', label: 'Tüm zamanlar' }]}
        />
        <label className="ds-select">
          <span>Dönem</span>
          <select value={etkinDonem} onChange={(e) => setDonem(Number(e.target.value))} aria-label="Dönem">
            {[1, 2, 3, 4, 5, 6].map((d) => <option key={d} value={d}>{d}. Dönem</option>)}
          </select>
          <ChevronDown aria-hidden />
        </label>
      </div>
      {hata && <p className="lbx-hata" role="status">{hata}</p>}

      {top3.some((t) => t.puan > 0) && (
        <ol className="lbx-podium" aria-label="İlk üç">
          {[1, 0, 2].map((i) => {
            const item = top3[i];
            if (!item) return <li key={i} className="lbx-col is-empty" aria-hidden />;
            const photo = item.ben ? currentUser?.photoURL : null;
            return (
              <li key={`${item.sira}-${item.ad}`} className={`lbx-col t${i + 1} ${item.ben ? 'is-me' : ''}`}>
                <span className="lbx-who">
                  {i === 0 && <CrownIcon className="lbx-crown" />}
                  <span className={`lbx-av${cerceve(item.cerceve)}`}>{photo ? <img src={photo} alt="" /> : initials(item.ad)}</span>
                  <b>{item.ad}</b>
                  {item.unvan && <span className="lbx-unvan">{item.unvan}</span>}
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
                <span className={`lbx-av is-sm${cerceve(item.cerceve)}`}>{item.ben && currentUser?.photoURL ? <img src={currentUser.photoURL} alt="" /> : initials(item.ad)}</span>
                <span className="lbx-name">
                  <b>{item.ad}{item.ben && <span className="lbx-me">Sen</span>}</b>
                  <span>{item.unvan ? `${item.unvan} · ` : ''}{item.basarim} başarım seviyesi{kapsam !== 'tum' && item.sira <= 5 ? ' · ' : ''}{kapsam !== 'tum' && item.sira <= 5 && atpRozet(item.sira, item.puan)}</span>
                </span>
                <span className="lbx-bar" aria-hidden><i style={{ width: `${Math.max(item.puan > 0 ? 3 : 0, (item.puan / maxPoints) * 100)}%` }} /></span>
                <span className="lbx-pts">{item.puan.toLocaleString('tr-TR')}</span>
              </li>
            ))}
          </ol>
        )}
      </section>
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
