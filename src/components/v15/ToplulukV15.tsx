import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { Bell, BellOff, Check, CheckCheck, ChevronRight, Eye, EyeOff, Flag, Hash, Heart, Link2, LogOut, Mail, MessageCircle, MessagesSquare, Palette, Reply, Search, Send, Settings2, Share2, SquarePen, Trash2, UserRound, X, Users, UserPlus, MoreVertical, Plus, ArrowDown } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { auth, getRememberedStudentInfo } from '../../services/auth';
import { useLiveEvent } from '../../hooks/useLiveEvent';
import { aktifKurul } from '../../services/kurulTakvimi';
import { navigateTo } from '../../router';
import { useV15Baslik } from './baslik';
import { EkKart, PaylasPaneli, SohbetZemin, TemaSecici, type Ek, type Tema } from './SohbetEkleri';
import '../../styles/v15/ogren.css';
import '../../styles/v15/dersler.css';
import '../../styles/v15/topluluk.css';
import '../../styles/v15/sohbet-ayar.css';

/**
 * v15 · Topluluk (tasarım sistemi v15 › L01–L06). Yeni sayfa: /topluluk[?kanal=…] (Menü › Ben).
 * Kanallar: Genel, Kurul N, ders yorumları (ders:<anahtar>, ders ayrıntısındaki "Yorumlar"dan açılır).
 * Sunucu: services/topluluk.ts (meds-pg, doğrulanmış kimlik, hız sınırı, şikâyet → 3'te gizlenir). Canlı: SSE `topluluk`.
 * Görünen ad cihazda tutulur; e-posta ya da uid hiçbir yerde gösterilmez.
 */
interface Mesaj { id: number; kanal: string; ad: string; metin: string; yanitId: number | null; at: number; yazar: string; benim: boolean; sikayet?: number; ek?: Ek }
interface Diger { ad: string; okunduId: number; okunduAt: number | null; son: number | null; cevrimici: boolean }
interface OdaBilgi { ad: string; tur: string; kod?: string; uyeler: string[]; digerler: Diger[]; ayar: { tema: Tema | null; sessiz: boolean; durumGizli: boolean } }
interface KanalOzet { kanal: string; n: number; son: number }
const AD_KEY = 'medsoru_topluluk_ad';
const kanalAdi = (k: string) => (k === 'genel' ? 'Genel' : k.startsWith('kurul-') ? `Kurul ${k.slice(6)}` : `Ders yorumları · ${k.slice(5).replace(/^y\d+-/, '').replace(/^k\d+-\d+-/, '').replace(/-/g, ' ')}`);
const kanalAlt = (k: string) => (k === 'genel' ? 'Herkesle sohbet' : k.startsWith('kurul-') ? 'Bu kurulun dersleri ve sınavı' : 'Bu ders hakkında soru ve notlar');
const saat = (t: number) => {
  const d = new Date(t), b = new Date();
  return d.toDateString() === b.toDateString() ? d.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }) : d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
};
/** yazar özetinden sabit ton (renk kimlik değil, ayırt etmek için; ad her zaman yazılı) */
const ton = (s: string) => parseInt(s.slice(0, 4), 16) % 360;

interface SohbetOzet { id: number; tur: 'dm' | 'grup'; ad: string; kod?: string; uyeN: number; okunmamis: number; sessiz?: boolean; cevrimici?: boolean; son: { ad: string; metin: string; at: number } | null; at: number }
interface Yorum extends Mesaj { begeni: number; begendim: boolean; yanitlar?: Yorum[] }
const benimAd = () => { try { const a = localStorage.getItem(AD_KEY); if (a) return a; } catch { /* yok */ } return (auth.currentUser?.displayName || getRememberedStudentInfo().name || 'Öğrenci').split(' ')[0]; };
const basHarf = (s: string) => s.split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toLocaleUpperCase('tr-TR') || '?';
const kisaZaman = (t: number) => {
  const dk = Math.round((Date.now() - t) / 60_000);
  if (dk < 1) return 'şimdi'; if (dk < 60) return `${dk} dk`; if (dk < 24 * 60) return `${Math.round(dk / 60)} sa`;
  if (dk < 48 * 60) return 'dün'; return new Date(t).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
};
/** "çevrimiçi" / "son görülme bugün 14:32" */
const sonGorulme = (t: number | null) => {
  if (!t) return 'Son görülme gizli';
  const d = new Date(t), b = new Date(), dun = new Date(b.getTime() - 86_400_000);
  const sa = d.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
  if (d.toDateString() === b.toDateString()) return `Son görülme bugün ${sa}`;
  if (d.toDateString() === dun.toDateString()) return `Son görülme dün ${sa}`;
  return `Son görülme ${d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })} ${sa}`;
};
const post = <T,>(url: string, body?: any) => safeJsonFetch<T>(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) });

type Gorunum = { t: 'kanallar' } | { t: 'kanal'; k: string } | { t: 'sohbetler' } | { t: 'oda'; id: number } | { t: 'yorum'; k: string } | { t: 'katil'; kod: string };
const oku = (): Gorunum => {
  const q = new URLSearchParams(location.search);
  if (q.get('katil')) return { t: 'katil', kod: q.get('katil')! };
  if (Number(q.get('sohbet'))) return { t: 'oda', id: Number(q.get('sohbet')) };
  if (q.get('gorunum') === 'sohbetler') return { t: 'sohbetler' };
  if (q.get('yorum')) return { t: 'yorum', k: q.get('yorum')! };
  if (q.get('kanal')) return { t: 'kanal', k: q.get('kanal')! };
  return { t: 'kanallar' };
};
const git = (adres: string) => { navigateTo(adres); window.dispatchEvent(new PopStateEvent('popstate')); };

const GENIS_MQ = '(min-width: 900px)';
function useGenis() {
  const [g, setG] = useState(() => typeof window !== 'undefined' && window.matchMedia(GENIS_MQ).matches);
  useEffect(() => { const m = window.matchMedia(GENIS_MQ); const f = () => setG(m.matches); m.addEventListener('change', f); return () => m.removeEventListener('change', f); }, []);
  return g;
}
/** Liste zamanı: bugün saat, dün, bu hafta gün adı, daha eski tarih */
const listeZaman = (t: number) => {
  const d = new Date(t), b = new Date();
  const gun = (x: Date) => new Date(x.getFullYear(), x.getMonth(), x.getDate()).getTime();
  const fark = Math.round((gun(b) - gun(d)) / 86_400_000);
  if (fark <= 0) return d.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
  if (fark === 1) return 'Dün';
  if (fark < 7) return d.toLocaleDateString('tr-TR', { weekday: 'long' });
  return d.toLocaleDateString('tr-TR', { day: '2-digit', month: '2-digit', year: '2-digit' });
};
const gunEtiket = (t: number) => {
  const d = new Date(t), b = new Date();
  const gun = (x: Date) => new Date(x.getFullYear(), x.getMonth(), x.getDate()).getTime();
  const fark = Math.round((gun(b) - gun(d)) / 86_400_000);
  if (fark <= 0) return 'Bugün'; if (fark === 1) return 'Dün';
  return d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', ...(d.getFullYear() !== b.getFullYear() ? { year: 'numeric' } : {}), ...(fark < 7 ? { weekday: 'long' } : {}) });
};
const saatKisa = (t: number) => new Date(t).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });

export default function ToplulukV15() {
  const [g, setG] = useState<Gorunum>(oku);
  const genis = useGenis();
  const md = useRef<HTMLDivElement>(null);
  useGorunurYukseklik(md, genis && (g.t === 'oda' || g.t === 'sohbetler'));
  useEffect(() => { const f = () => setG(oku()); window.addEventListener('popstate', f); return () => window.removeEventListener('popstate', f); }, []);
  if (g.t === 'kanal') return <Sohbet key={g.k} kanal={g.k} />;
  if ((g.t === 'oda' || g.t === 'sohbetler') && genis) {
    const id = g.t === 'oda' ? g.id : 0;
    return (
      <div className="tp15-md" ref={md}>
        <SohbetListe secili={id} gomulu />
        <section className="tp15-md-sag" aria-label="Açık sohbet">
          {id ? <Sohbet key={`oda${id}`} kanal={`oda:${id}`} oda={id} gomulu /> : (
            <div className="tp15-detay-bos"><span className="tp15-detay-ik"><MessagesSquare aria-hidden /></span><b>Bir sohbet seç</b><span>Soldaki listeden bir sohbet aç ya da yeni bir grup kur.</span></div>
          )}
        </section>
      </div>
    );
  }
  if (g.t === 'oda') return <Sohbet key={`oda${g.id}`} kanal={`oda:${g.id}`} oda={g.id} />;
  if (g.t === 'sohbetler') return <SohbetListe />;
  if (g.t === 'yorum') return <Yorumlar key={g.k} kanal={g.k} />;
  if (g.t === 'katil') return <Katil kod={g.kod} />;
  return <Kanallar ac={(k) => git(`/topluluk?kanal=${encodeURIComponent(k)}`)} />;
}

type Suzgec = 'hepsi' | 'okunmamis' | 'grup' | 'dm';
const SUZGEC: { id: Suzgec; ad: string }[] = [{ id: 'hepsi', ad: 'Tümü' }, { id: 'okunmamis', ad: 'Okunmamış' }, { id: 'grup', ad: 'Gruplar' }, { id: 'dm', ad: 'Birebir' }];
const avTon = (s: SohbetOzet | { id: number }) => (s.id * 47) % 360;

/** L01 · Sohbet listesi: arama, süzgeç, yeni grup; geniş ekranda sol bölme (master) */
function SohbetListe({ secili = 0, gomulu = false }: { secili?: number; gomulu?: boolean }) {
  const [liste, setListe] = useState<SohbetOzet[] | null>(null);
  const [girisli, setGirisli] = useState(true);
  const [ara, setAra] = useState('');
  const [suz, setSuz] = useState<Suzgec>('hepsi');
  const [yeni, setYeni] = useState(false);
  const [grupAd, setGrupAd] = useState('');
  const [hata, setHata] = useState('');
  const grupGiris = useRef<HTMLInputElement>(null);
  useV15Baslik({ baslik: 'Sohbetler', alt: 'Topluluk', geri: '/topluluk' });
  const yukle = useCallback(() => safeJsonFetch<{ sohbetler: SohbetOzet[]; girisli: boolean }>('/api/topluluk/sohbetler').then((r) => {
    if (r.ok && r.data) { setListe(r.data.sohbetler); setGirisli(r.data.girisli); setHata(''); }
    else { setListe((l) => l || []); setHata((r.data as any)?.error || 'Sohbetler alınamadı.'); }
  }), []);
  useEffect(() => { void yukle(); }, [yukle, secili]);
  useLiveEvent('topluluk_sohbet', () => void yukle(), { debounceMs: 600 });
  useEffect(() => { if (yeni) grupGiris.current?.focus(); }, [yeni]);
  const olustur = async () => {
    const ad = grupAd.trim(); if (!ad) return;
    const r = await post<{ id: number }>('/api/topluluk/sohbet', { tur: 'grup', ad, benAd: benimAd() });
    if (r.ok && r.data?.id) { setGrupAd(''); setYeni(false); git(`/topluluk?sohbet=${r.data.id}`); } else setHata((r.data as any)?.error || 'Grup kurulamadı.');
  };
  const q = ara.trim().toLocaleLowerCase('tr-TR');
  const tum = liste || [];
  const gorunen = tum.filter((s) => (!q || `${s.ad} ${s.son?.metin || ''}`.toLocaleLowerCase('tr-TR').includes(q))
    && (suz === 'hepsi' || (suz === 'okunmamis' ? s.okunmamis > 0 : s.tur === suz)));
  const okunmamisN = tum.filter((s) => s.okunmamis > 0).length;
  const onizleme = (s: SohbetOzet) => {
    if (!s.son) return s.tur === 'grup' ? `${s.uyeN} üye · henüz mesaj yok` : 'Henüz mesaj yok';
    const kim = s.son.ad === 'Sen' ? 'Sen' : s.tur === 'grup' ? s.son.ad : '';
    return <>{kim && <b className="tp15-on-kim">{kim}: </b>}{s.son.metin}</>;
  };
  return (
    <div className={`tp15 tp15-l${gomulu ? ' is-gomulu' : ''}`}>
      <div className="tp15-l-ust">
        <div className="tp15-l-bas">
          <h1>Sohbetler</h1>
          <button type="button" className="tp15-ib is-acc" onClick={() => setYeni((v) => !v)} aria-label="Yeni grup kur" aria-expanded={yeni} title="Yeni grup"><SquarePen aria-hidden /></button>
        </div>
        <label className="tp15-ara"><Search aria-hidden /><input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Sohbetlerde ara" aria-label="Sohbetlerde ara" />
          {ara && <button type="button" onClick={() => setAra('')} aria-label="Aramayı temizle"><X aria-hidden /></button>}</label>
        {tum.length > 0 && (
          <div className="tp15-cip" role="group" aria-label="Süzgeç">
            {SUZGEC.map((s) => <button key={s.id} type="button" aria-pressed={suz === s.id} className={suz === s.id ? 'is-on' : ''} onClick={() => setSuz(s.id)}>{s.ad}{s.id === 'okunmamis' && okunmamisN > 0 && <span>{okunmamisN}</span>}</button>)}
          </div>
        )}
      </div>
      {yeni && (
        <form className="tp15-yeni" onSubmit={(e) => { e.preventDefault(); void olustur(); }}>
          <b>Yeni grup</b>
          <div className="tp15-giris">
            <input ref={grupGiris} className="tp15-ad" value={grupAd} onChange={(e) => setGrupAd(e.target.value.slice(0, 60))} placeholder="Grup adı (ör. Patoloji çalışma)" aria-label="Grup adı" onKeyDown={(e) => { if (e.key === 'Escape') setYeni(false); }} />
            <button type="submit" className="v15-btn" disabled={!grupAd.trim()}>Kur</button>
          </div>
          <p className="v15-cap">Kurduktan sonra menüden davet bağlantısını kopyalayıp paylaş. Birebir sohbet için bir kişinin profilinden ya da kanaldaki mesajından özel mesaj başlat.</p>
        </form>
      )}
      {hata && <p className="tp15-uyari">{hata}</p>}
      {!girisli ? <div className="tp15-lbos"><span className="tp15-detay-ik"><MessagesSquare aria-hidden /></span><b>Giriş yapmalısın</b><span>Sohbetlerini görmek için hesabınla giriş yap.</span></div>
        : liste === null ? <div className="tp15-iskelet" aria-hidden>{[0, 1, 2, 3, 4].map((i) => <span key={i}><i /><em /></span>)}</div>
        : !tum.length ? (
          <div className="tp15-lbos">
            <span className="tp15-detay-ik"><MessagesSquare aria-hidden /></span>
            <b>Henüz sohbetin yok</b>
            <span>Arkadaşlarınla birebir yazış ya da çalışma grubu kurup birlikte soru çöz.</span>
            <div className="tp15-lbos-is">
              <button type="button" className="v15-btn" onClick={() => setYeni(true)}><Users aria-hidden />Grup kur</button>
              <button type="button" className="v15-btn is-soft" onClick={() => git('/arkadaslar')}><UserPlus aria-hidden />Arkadaş ekle</button>
            </div>
          </div>
        )
        : !gorunen.length ? <p className="tp15-lbos is-k">{q ? `“${ara.trim()}” için sohbet bulunamadı.` : 'Bu süzgeçte sohbet yok.'}</p>
        : (
          <ul className="tp15-sl" aria-label="Sohbetler">
            {gorunen.map((s) => (
              <li key={s.id}>
                <button type="button" className={`tp15-sr${s.id === secili ? ' is-sec' : ''}${s.okunmamis > 0 ? ' is-yeni' : ''}`} aria-current={s.id === secili ? 'true' : undefined}
                  onClick={() => git(`/topluluk?sohbet=${s.id}`)}>
                  <span className="tp15-av" style={{ '--t': avTon(s) } as React.CSSProperties}>
                    {s.tur === 'grup' ? <Users aria-hidden /> : basHarf(s.ad)}
                    {s.tur === 'dm' && s.cevrimici && <i className="tp15-on" aria-label="Çevrimiçi" />}
                  </span>
                  <span className="tp15-sr-t">
                    <span className="tp15-sr-1"><b>{s.ad}</b>{s.sessiz && <BellOff className="tp15-sessiz" aria-label="Sessize alındı" />}<time>{listeZaman(s.son?.at || s.at)}</time></span>
                    <span className="tp15-sr-2"><span className="tp15-on-m">{onizleme(s)}</span>{s.okunmamis > 0 && <span className={`tp15-rozet${s.sessiz ? ' is-sessiz' : ''}`} aria-label={`${s.okunmamis} okunmamış`}>{s.okunmamis > 99 ? '99+' : s.okunmamis}</span>}</span>
                  </span>
                </button>
              </li>
            ))}
          </ul>
        )}
      {girisli && liste !== null && tum.length > 0 && (
        <button type="button" className="tp15-arkadas" onClick={() => git('/arkadaslar')}><UserPlus aria-hidden />Arkadaşlar ve davetler<ChevronRight aria-hidden /></button>
      )}
    </div>
  );
}

function Katil({ kod }: { kod: string }) {
  const [hata, setHata] = useState('');
  useV15Baslik({ baslik: 'Gruba katıl', alt: 'Topluluk', geri: '/topluluk?gorunum=sohbetler' });
  const katil = async () => {
    const r = await post<{ id: number }>('/api/topluluk/sohbet/katil', { kod, benAd: benimAd() });
    if (r.ok && r.data?.id) git(`/topluluk?sohbet=${r.data.id}`); else setHata((r.data as any)?.error || r.error || 'Katılınamadı.');
  };
  return (
    <div className="tp15">
      <div className="b15-bos v15-card">
        <span>Bir sohbet grubuna davet edildin. Katılınca görünen adın grup üyelerine gösterilir.</span>
        {hata && <span className="tp15-hata">{hata}</span>}
        <button type="button" className="v15-btn" onClick={katil}>Gruba katıl</button>
      </div>
    </div>
  );
}

/** L03 · Yorumlar: ders/soru yorumları, En faydalı | En yeni, beğeni (kişi başına bir), yanıtla */
function Yorumlar({ kanal }: { kanal: string }) {
  const [sira, setSira] = useState<'faydali' | 'yeni'>('faydali');
  const [veri, setVeri] = useState<{ yorumlar: Yorum[]; toplam: number; girisli: boolean } | null>(null);
  const [metin, setMetin] = useState('');
  const [yanit, setYanit] = useState<Yorum | null>(null);
  const [hata, setHata] = useState('');
  const [gonderiyor, setGonderiyor] = useState(false);
  const alt = kanal.startsWith('soru:') ? `Soru ${kanal.slice(5)}` : kanalAdi(kanal).replace(/^Ders yorumları · /, '');
  useV15Baslik({ baslik: 'Yorumlar', alt: veri ? `${alt} · ${veri.toplam} yorum` : alt, geri: '/topluluk' });
  const yukle = useCallback(async () => {
    const r = await safeJsonFetch<{ yorumlar: Yorum[]; toplam: number; girisli: boolean }>(`/api/topluluk/yorumlar?kanal=${encodeURIComponent(kanal)}&sira=${sira}`);
    if (r.ok && r.data) { setVeri({ ...r.data, girisli: r.data.girisli || !!auth.currentUser }); }
    else { setVeri((v) => v || { yorumlar: [], toplam: 0, girisli: !!auth.currentUser }); setHata((r.data as any)?.error || 'Yorumlar alınamadı.'); }
  }, [kanal, sira]);
  useEffect(() => { void yukle(); }, [yukle]);
  useLiveEvent('topluluk', (p) => { if (!p || p.resync || p.kanal === kanal) void yukle(); }, { debounceMs: 400 });
  const begen = async (y: Yorum) => {
    const r = await post<{ begendim: boolean; begeni: number }>(`/api/topluluk/mesaj/${y.id}/begen`);
    if (!r.ok || !r.data) return setHata((r.data as any)?.error || 'Beğenilemedi.');
    const { begendim, begeni } = r.data;
    const g = (l: Yorum[]): Yorum[] => l.map((x) => (x.id === y.id ? { ...x, begendim, begeni } : { ...x, yanitlar: x.yanitlar && g(x.yanitlar) }));
    setVeri((v) => v && { ...v, yorumlar: g(v.yorumlar) });
  };
  const gonder = async () => {
    const t = metin.trim(); if (!t || gonderiyor) return;
    setGonderiyor(true); setHata('');
    const r = await post<{ mesaj: Mesaj }>('/api/topluluk/mesaj', { kanal, metin: t, ad: benimAd(), yanitId: yanit?.id });
    setGonderiyor(false);
    if (r.ok) { setMetin(''); setYanit(null); void yukle(); } else setHata((r.data as any)?.error || r.error || 'Gönderilemedi.');
  };
  const satir = (y: Yorum, ic = false) => (
    <div className={ic ? 'tp15-yic' : ''} style={{ '--t': ton(y.yazar) } as React.CSSProperties}>
      <div className="tp15-yb"><span className={`tp15-av${ic ? ' is-k' : ''}`}>{basHarf(y.benim ? 'Sen' : y.ad)}</span><b>{y.benim ? 'Sen' : y.ad}</b></div>
      <p className="tp15-ym">{y.metin}</p>
      <div className="tp15-yis">
        <button type="button" className={y.begendim ? 'is-on' : ''} onClick={() => begen(y)} aria-pressed={y.begendim} aria-label={`Beğen, ${y.begeni} beğeni`} disabled={!veri?.girisli}><Heart aria-hidden />{y.begeni}</button>
        {!ic && veri?.girisli && <button type="button" onClick={() => setYanit(y)}>Yanıtla</button>}
        <time>{kisaZaman(y.at)}</time>
      </div>
    </div>
  );
  return (
    <div className="tp15">
      <h1 className="sr-only">Yorumlar</h1>
      <div className="v15-seg tp15-seg" role="tablist" aria-label="Sıralama">
        {(['faydali', 'yeni'] as const).map((s) => <button key={s} type="button" role="tab" aria-selected={sira === s} className={sira === s ? 'is-on' : ''} onClick={() => setSira(s)}>{s === 'faydali' ? 'En faydalı' : 'En yeni'}</button>)}
      </div>
      {veri === null ? <span className="v15-skel b15-skel" aria-hidden />
        : !veri.yorumlar.length ? <p className="b15-bos v15-card">Henüz yorum yok. İlk yorumu sen yaz.</p>
        : veri.yorumlar.map((y) => (
          <article key={y.id} className="v15-card tp15-yorum">
            {satir(y)}
            {y.yanitlar?.map((x) => <React.Fragment key={x.id}>{satir(x, true)}</React.Fragment>)}
          </article>
        ))}
      <div className="tp15-yaz v15-card">
        {hata && <p className="tp15-hata" role="status">{hata}</p>}
        {!veri?.girisli ? <p className="v15-cap">Yorum yazmak için giriş yapmalısın.</p> : (
          <>
            {yanit && <p className="tp15-yanit"><Reply aria-hidden /><span><b>{yanit.ad}</b> · {yanit.metin.slice(0, 70)}</span><button type="button" onClick={() => setYanit(null)} aria-label="Yanıtı kaldır"><X aria-hidden /></button></p>}
            <div className="tp15-giris">
              <textarea value={metin} onChange={(e) => setMetin(e.target.value.slice(0, 800))} placeholder="Yorum yaz…" rows={1} aria-label="Yorum" />
              <button type="button" className="tp15-gonder" onClick={gonder} disabled={!metin.trim() || gonderiyor} aria-label="Gönder"><Send aria-hidden /></button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function Kanallar({ ac }: { ac: (k: string) => void }) {
  const [ozet, setOzet] = useState<KanalOzet[] | null>(null);
  const [hata, setHata] = useState('');
  useV15Baslik({ baslik: 'Topluluk', alt: 'Sohbet ve ders yorumları' });
  const yukle = useCallback(() => safeJsonFetch<{ kanallar: KanalOzet[] }>('/api/topluluk/kanallar').then((r) => {
    if (r.ok) { setOzet(r.data?.kanallar || []); setHata(''); } else { setOzet([]); setHata(r.data && (r.data as any).error || 'Topluluğa ulaşılamadı.'); }
  }), []);
  useEffect(() => { void yukle(); }, [yukle]);
  useLiveEvent('topluluk', () => void yukle(), { debounceMs: 1500 });
  const m = new Map((ozet || []).map((k) => [k.kanal, k]));
  const ak = aktifKurul().kurul;
  const sabit = ['genel', `kurul-${ak}`, ...[1, 2, 3, 4, 5, 6].filter((k) => k !== ak).map((k) => `kurul-${k}`)];
  const dersler = (ozet || []).filter((k) => k.kanal.startsWith('ders:')).sort((a, b) => b.son - a.son);
  const satir = (k: string) => {
    const o = m.get(k);
    return (
      <li key={k}>
        <button type="button" className="b15-row" onClick={() => (k.startsWith('ders:') ? git(`/topluluk?yorum=${encodeURIComponent(k)}`) : ac(k))}>
          <span className={`v15-tile${o ? '' : ' is-n'}`}>{k.startsWith('ders:') ? <MessageCircle aria-hidden /> : <Hash aria-hidden />}</span>
          <span className="b15-row-t"><b>{kanalAdi(k)}</b><span>{o ? `${o.n} mesaj · son ${saat(o.son)}` : kanalAlt(k)}</span></span>
          <ChevronRight className="v15-chev" aria-hidden />
        </button>
      </li>
    );
  };
  return (
    <div className="tp15">
      <h1 className="sr-only">Topluluk</h1>
      {hata && <p className="tp15-uyari v15-card">{hata}</p>}
      <ul className="b15-list v15-card">
        <li><button type="button" className="b15-row" onClick={() => git('/topluluk?gorunum=sohbetler')}>
          <span className="v15-tile"><MessagesSquare aria-hidden /></span>
          <span className="b15-row-t"><b>Sohbet</b><span>Grup ve birebir sohbetlerin</span></span>
          <ChevronRight className="v15-chev" aria-hidden />
        </button></li>
      </ul>
      <h2 className="v15-cap tp15-h">Kanallar</h2>
      <ul className="b15-list v15-card">{sabit.map(satir)}</ul>
      <h2 className="v15-cap tp15-h">Ders yorumları</h2>
      {dersler.length ? <ul className="b15-list v15-card">{dersler.map((k) => satir(k.kanal))}</ul>
        : <p className="b15-bos v15-card">Henüz ders yorumu yok. Bir dersin sayfasındaki "Yorumlar" ile o derse yorum yazabilirsin.{' '}
            {/* H346: boş durum ders sayfasına yönlendiriyordu ama bağlantı yoktu */}
            <a href="/dersler" onClick={(e) => { e.preventDefault(); navigateTo('/dersler'); }}>Derslere git</a></p>}
      <p className="v15-cap tp15-kural">Saygılı ol; kişisel bilgi, sınav sorusu fotoğrafı ya da reklam paylaşma. Uygunsuz mesajı bayrakla bildir; üç bildirimde mesaj gizlenir.</p>
    </div>
  );
}

/** Kabın yüksekliğini görünür alana (visualViewport) eşitler: mobil klavye açıkken yazma kutusu görünür kalır */
function useGorunurYukseklik(ref: React.RefObject<HTMLDivElement | null>, acik = true) {
  useLayoutEffect(() => {
    const el = ref.current; if (!el || !acik) return;
    const vv = window.visualViewport;
    const f = () => {
      const cs = getComputedStyle(el);
      const zoom = parseFloat(cs.getPropertyValue('--ch-zoom')) || 1;
      const tabs = parseFloat(cs.getPropertyValue('--sh-tabs-h')) || 0;
      const vh = vv ? vv.height + vv.offsetTop : window.innerHeight;
      const klavye = vv ? window.innerHeight - vv.height > 150 : false;
      const alt = klavye ? 6 : tabs * zoom + 12;
      const h = (vh - el.getBoundingClientRect().top - alt) / zoom;
      el.style.height = `${Math.max(320, Math.round(h))}px`;
    };
    f();
    vv?.addEventListener('resize', f); vv?.addEventListener('scroll', f); window.addEventListener('resize', f);
    return () => { vv?.removeEventListener('resize', f); vv?.removeEventListener('scroll', f); window.removeEventListener('resize', f); };
  }, [ref, acik]);
}

function Sohbet({ kanal, oda, gomulu = false }: { kanal: string; oda?: number; gomulu?: boolean }) {
  const [mesajlar, setMesajlar] = useState<Mesaj[] | null>(null);
  const [dahaVar, setDahaVar] = useState(false);
  const [girisli, setGirisli] = useState(true);
  const [metin, setMetin] = useState('');
  const [ad, setAd] = useState(() => { try { return localStorage.getItem(AD_KEY) || ''; } catch { return ''; } });
  const [yanit, setYanit] = useState<Mesaj | null>(null);
  const [hata, setHata] = useState('');
  const [gonderiyor, setGonderiyor] = useState(false);
  const kap = useRef<HTMLDivElement>(null);
  const liste = useRef<HTMLDivElement>(null);
  const yazi = useRef<HTMLTextAreaElement>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const altta = useRef(true);
  const sonId = useRef(0);
  const [yeniVar, setYeniVar] = useState(0);
  const [odaBilgi, setOdaBilgi] = useState<OdaBilgi | null>(null);
  const [panel, setPanel] = useState<'' | 'paylas' | 'tema' | 'ayar' | 'uyeler'>('');
  const [menu, setMenu] = useState(false);
  const [ek, setEk] = useState<Ek | null>(null);
  useGorunurYukseklik(kap, !gomulu);
  useV15Baslik(gomulu ? null : oda ? { baslik: 'Sohbet', alt: 'Topluluk', geri: '/topluluk?gorunum=sohbetler' }
    : { baslik: kanalAdi(kanal), alt: 'Topluluk', geri: '/topluluk' });

  const yukle = useCallback(async () => {
    if (oda) {
      const r = await safeJsonFetch<{ oda: any; mesajlar: Mesaj[]; dahaVar: boolean }>(`/api/topluluk/sohbet/${oda}`);
      if (r.ok && r.data) { setOdaBilgi(r.data.oda); setMesajlar(r.data.mesajlar); setDahaVar(r.data.dahaVar); setGirisli(true); void post(`/api/topluluk/sohbet/${oda}/okundu`); }
      else { setMesajlar((m) => m || []); setHata((r.data as any)?.error || 'Sohbet açılamadı.'); }
      return;
    }
    const r = await safeJsonFetch<{ mesajlar: Mesaj[]; dahaVar: boolean; girisli: boolean }>(`/api/topluluk/mesajlar?kanal=${encodeURIComponent(kanal)}`);
    if (r.ok && r.data) { setMesajlar(r.data.mesajlar); setDahaVar(r.data.dahaVar); setGirisli(r.data.girisli || !!auth.currentUser); }
    else { setMesajlar((m) => m || []); setHata((r.data as any)?.error || 'Mesajlar alınamadı.'); }
  }, [kanal, oda]);
  useEffect(() => { setMesajlar(null); altta.current = true; sonId.current = 0; void yukle(); }, [yukle]);
  // Çevrimiçi nabzı + durum yenileme (yalnız özel sohbet odasında, sekme görünürken)
  useEffect(() => {
    if (!oda) return;
    const f = () => { if (document.visibilityState === 'visible') { void post('/api/topluluk/sohbet/nabiz'); void yukle(); } };
    const t = setInterval(f, 60_000);
    document.addEventListener('visibilitychange', f);
    return () => { clearInterval(t); document.removeEventListener('visibilitychange', f); };
  }, [oda, yukle]);
  useLiveEvent(oda ? 'topluluk_sohbet' : 'topluluk', (p) => { if (!p || p.resync || (oda ? p.oda === oda : p.kanal === kanal)) void yukle(); }, { debounceMs: 200 });
  // Menü: dışarı tıklayınca / Escape ile kapanır
  useEffect(() => {
    if (!menu) return;
    const d = (e: MouseEvent) => { if (!menuRef.current?.contains(e.target as Node)) setMenu(false); };
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') { setMenu(false); (menuRef.current?.querySelector('button') as HTMLButtonElement | null)?.focus(); } };
    document.addEventListener('mousedown', d); document.addEventListener('keydown', k);
    (menuRef.current?.querySelector('[role=menuitem]') as HTMLElement | null)?.focus();
    return () => { document.removeEventListener('mousedown', d); document.removeEventListener('keydown', k); };
  }, [menu]);
  // Açılışta yazma kutusuna odak (yalnız fare/klavye cihazında; mobilde klavyeyi zorla açma)
  useEffect(() => { if (window.matchMedia('(hover: hover)').matches) yazi.current?.focus({ preventScroll: true }); }, [kanal]);

  const eskiler = async () => {
    const ilk = mesajlar?.[0]?.id; if (!ilk) return;
    const el = liste.current; const once = el ? el.scrollHeight - el.scrollTop : 0;
    const r = await safeJsonFetch<{ mesajlar: Mesaj[]; dahaVar: boolean }>(oda ? `/api/topluluk/sohbet/${oda}?once=${ilk}` : `/api/topluluk/mesajlar?kanal=${encodeURIComponent(kanal)}&once=${ilk}`);
    if (r.ok && r.data) {
      altta.current = false; setMesajlar((m) => [...r.data!.mesajlar, ...(m || [])]); setDahaVar(r.data.dahaVar);
      requestAnimationFrame(() => { if (el) el.scrollTop = el.scrollHeight - once; });
    }
  };
  useLayoutEffect(() => {
    const el = liste.current; if (!el || !mesajlar) return;
    const son = mesajlar[mesajlar.length - 1];
    const yeniGeldi = son && son.id > sonId.current && sonId.current > 0;
    if (altta.current) { el.scrollTop = el.scrollHeight; setYeniVar(0); }
    else if (yeniGeldi && !son.benim) setYeniVar((n) => n + mesajlar.filter((m) => m.id > sonId.current).length);
    if (son) sonId.current = Math.max(sonId.current, son.id);
  }, [mesajlar]);
  const enAlta = (yumusak = true) => { const el = liste.current; if (el) el.scrollTo({ top: el.scrollHeight, behavior: yumusak ? 'smooth' : 'auto' }); altta.current = true; setYeniVar(0); };
  const kaydir = () => {
    const el = liste.current; if (!el) return;
    altta.current = el.scrollHeight - el.scrollTop - el.clientHeight < 80;
    if (altta.current && yeniVar) { setYeniVar(0); if (oda) void post(`/api/topluluk/sohbet/${oda}/okundu`); }
  };
  // Otomatik büyüyen yazma kutusu (field-sizing desteklemeyen tarayıcılar için)
  useLayoutEffect(() => { const t = yazi.current; if (!t) return; t.style.height = 'auto'; t.style.height = `${Math.min(t.scrollHeight + 2, 160)}px`; t.style.overflowY = t.scrollHeight > 160 ? 'auto' : 'hidden'; }, [metin]);

  const gonder = async () => {
    const t = metin.trim(); if ((!t && !ek) || gonderiyor) return;
    const gorunen = ad.trim() || (auth.currentUser?.displayName || getRememberedStudentInfo().name || 'Öğrenci').split(' ')[0];
    setGonderiyor(true); setHata('');
    const r = oda ? await post<{ mesaj: Mesaj }>(`/api/topluluk/sohbet/${oda}/mesaj`, { metin: t, yanitId: yanit?.id, ek: ek || undefined })
      : await post<{ mesaj: Mesaj }>('/api/topluluk/mesaj', { kanal, metin: t, ad: gorunen, yanitId: yanit?.id });
    setGonderiyor(false);
    if (r.ok && r.data?.mesaj) {
      altta.current = true; setMetin(''); setYanit(null); setEk(null); setPanel('');
      try { if (ad.trim()) localStorage.setItem(AD_KEY, ad.trim()); } catch { /* yok */ }
      setMesajlar((m) => (m?.some((x) => x.id === r.data!.mesaj.id) ? m : [...(m || []), r.data!.mesaj]));
      yazi.current?.focus();
    } else setHata((r.data as any)?.error || r.error || 'Gönderilemedi.');
  };
  const sil = async (x: Mesaj) => {
    if (!confirm('Mesaj silinsin mi?')) return;
    const r = await safeJsonFetch(`/api/topluluk/mesaj/${x.id}/sil`, { method: 'POST' });
    if (r.ok) setMesajlar((m) => (m || []).filter((y) => y.id !== x.id)); else setHata((r.data as any)?.error || 'Silinemedi.');
  };
  const bildir = async (x: Mesaj) => {
    if (!confirm('Bu mesajı uygunsuz olarak bildir?')) return;
    const r = await safeJsonFetch(`/api/topluluk/mesaj/${x.id}/sikayet`, { method: 'POST' });
    setHata(r.ok ? 'Bildirdin, teşekkürler.' : (r.data as any)?.error || 'Bildirilemedi.');
  };
  const ozel = async (x: Mesaj) => {
    const r = await post<{ id: number }>('/api/topluluk/sohbet', { tur: 'dm', yazar: x.yazar, benAd: benimAd() });
    if (r.ok && r.data?.id) git(`/topluluk?sohbet=${r.data.id}`); else setHata((r.data as any)?.error || 'Sohbet açılamadı.');
  };
  const davet = async () => {
    setMenu(false);
    if (!odaBilgi?.kod) return;
    const url = `${location.origin}/topluluk?katil=${odaBilgi.kod}`;
    try { await navigator.clipboard.writeText(url); setHata('Davet bağlantısı kopyalandı.'); } catch { setHata(url); }
  };
  const ayril = async () => {
    setMenu(false);
    if (!oda || !confirm('Sohbetten ayrılınsın mı?')) return;
    const r = await post(`/api/topluluk/sohbet/${oda}/ayril`);
    if (r.ok) git('/topluluk?gorunum=sohbetler'); else setHata((r.data as any)?.error || 'Ayrılınamadı.');
  };
  const ayarKaydet = async (yama: { sessiz?: boolean; tema?: Tema | null }) => {
    if (!oda) return;
    const r = await post(`/api/topluluk/sohbet/${oda}/ayar`, yama);
    if (!r.ok) { setHata((r.data as any)?.error || r.error || 'Ayar kaydedilemedi.'); return; }
    setOdaBilgi((o) => o && { ...o, ayar: { ...o.ayar, ...yama } });
  };
  const durumGizle = async () => {
    const yeni = !odaBilgi?.ayar.durumGizli;
    const r = await post('/api/topluluk/sohbet/ayar', { durumGizli: yeni });
    if (r.ok) { setOdaBilgi((o) => o && { ...o, ayar: { ...o.ayar, durumGizli: yeni } }); void yukle(); }
    else setHata((r.data as any)?.error || 'Ayar kaydedilemedi.');
  };
  const panelAc = (p: typeof panel) => { setMenu(false); setPanel(panel === p ? '' : p); };
  const tema = odaBilgi?.ayar.tema || null;
  const dm = odaBilgi?.tur === 'dm';
  const grupMu = !dm; // kanal ya da grup: adlar gösterilir
  const diger = dm ? odaBilgi?.digerler[0] : undefined;
  const cevrimiciN = odaBilgi?.digerler.filter((d) => d.cevrimici).length || 0;
  const sonBenimId = useMemo(() => { const l = (mesajlar || []).filter((m) => m.benim); return l.length ? l[l.length - 1].id : 0; }, [mesajlar]);
  const byId = useMemo(() => new Map((mesajlar || []).map((x) => [x.id, x])), [mesajlar]);
  const durumYazi = !odaBilgi ? '' : dm ? (diger?.cevrimici ? 'Çevrimiçi' : sonGorulme(diger?.son ?? null))
    : `${odaBilgi.uyeler.length} üye${cevrimiciN ? ` · ${cevrimiciN} çevrimiçi` : ''}`;
  const okundu = (x: Mesaj) => {
    if (!oda || !x.benim || x.id !== sonBenimId || !odaBilgi) return null;
    const okuyan = odaBilgi.digerler.filter((d) => d.okunduId >= x.id);
    if (!okuyan.length) return <Check className="tp15-tik" aria-label="İletildi" />;
    return <CheckCheck className="tp15-tik is-ok" aria-label={dm ? `Okundu${okuyan[0].okunduAt ? ' ' + saatKisa(okuyan[0].okunduAt) : ''}` : `${okuyan.length} kişi okudu`} />;
  };

  return (
    <div ref={kap} className={`tp15 tp15-s${gomulu ? ' is-gomulu' : ''}`}>
      {oda && (
        <header className="tp15-sb">
          <span className="tp15-av" style={{ '--t': avTon({ id: oda }) } as React.CSSProperties}>
            {odaBilgi?.tur === 'grup' ? <Users aria-hidden /> : basHarf(odaBilgi?.ad || '?')}
            {dm && diger?.cevrimici && <i className="tp15-on" aria-hidden />}
          </span>
          <button type="button" className="tp15-sb-t" onClick={() => panelAc(dm ? 'ayar' : 'uyeler')} aria-label={`${odaBilgi?.ad || 'Sohbet'} bilgileri`}>
            <h1>{odaBilgi?.ad || 'Sohbet'}{odaBilgi?.ayar.sessiz && <BellOff className="tp15-sessiz" aria-label="Sessizde" />}</h1>
            <span className={dm && diger?.cevrimici ? 'is-on' : ''}>{durumYazi || ' '}</span>
          </button>
          <div className="tp15-menu-k" ref={menuRef}>
            <button type="button" className="tp15-ib is-sade" onClick={() => setMenu((v) => !v)} aria-label="Sohbet menüsü" aria-haspopup="menu" aria-expanded={menu}><MoreVertical aria-hidden /></button>
            {menu && odaBilgi && (
              <div className="tp15-menu" role="menu" aria-label="Sohbet menüsü"
                onKeyDown={(e) => {
                  if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
                  e.preventDefault();
                  const l = [...e.currentTarget.querySelectorAll<HTMLElement>('[role=menuitem]')]; const i = l.indexOf(document.activeElement as HTMLElement);
                  l[(i + (e.key === 'ArrowDown' ? 1 : -1) + l.length) % l.length]?.focus();
                }}>
                {!dm && <button type="button" role="menuitem" onClick={() => panelAc('uyeler')}><Users aria-hidden />Üyeler<em>{odaBilgi.uyeler.length}</em></button>}
                {odaBilgi.kod && <button type="button" role="menuitem" onClick={davet}><Link2 aria-hidden />Davet bağlantısını kopyala</button>}
                <button type="button" role="menuitem" onClick={() => { setMenu(false); void ayarKaydet({ sessiz: !odaBilgi.ayar.sessiz }); }}>{odaBilgi.ayar.sessiz ? <Bell aria-hidden /> : <BellOff aria-hidden />}{odaBilgi.ayar.sessiz ? 'Sesi aç' : 'Sessize al'}</button>
                <button type="button" role="menuitem" onClick={() => panelAc('tema')}><Palette aria-hidden />Arka plan teması</button>
                <button type="button" role="menuitem" onClick={() => panelAc('ayar')}><Settings2 aria-hidden />Gizlilik ve bildirim</button>
                <button type="button" role="menuitem" className="is-tehlike" onClick={ayril}><LogOut aria-hidden />Sohbetten ayrıl</button>
              </div>
            )}
          </div>
        </header>
      )}
      {oda && odaBilgi && panel === 'tema' && <TemaSecici aktif={tema} kapat={() => setPanel('')} sec={(t) => { void ayarKaydet({ tema: t }); }} />}
      {oda && odaBilgi && panel === 'uyeler' && (
        <div className="sa-paylas v15-card tp15-uyeler">
          <div className="sa-baslik"><b>Üyeler · {odaBilgi.uyeler.length}</b><button type="button" className="tp15-ib is-sade" onClick={() => setPanel('')} aria-label="Kapat"><X aria-hidden /></button></div>
          <ul>
            {odaBilgi.uyeler.map((u, i) => {
              const d = odaBilgi.digerler.find((x) => x.ad === u);
              return <li key={`${u}${i}`}><span className="tp15-av is-k" style={{ '--t': (i * 67) % 360 } as React.CSSProperties}>{basHarf(u)}</span><b>{u}</b><span className={d?.cevrimici ? 'is-on' : ''}>{d ? (d.cevrimici ? 'Çevrimiçi' : d.son ? sonGorulme(d.son).replace('Son görülme ', '') : '') : 'Sen'}</span></li>;
            })}
          </ul>
          {odaBilgi.kod && <button type="button" className="v15-btn is-soft" onClick={davet}><Link2 aria-hidden />Davet bağlantısını kopyala</button>}
        </div>
      )}
      {oda && odaBilgi && panel === 'ayar' && (
        <div className="sa-paylas v15-card">
          <div className="sa-baslik"><b>Gizlilik ve bildirim</b><button type="button" className="tp15-ib is-sade" onClick={() => setPanel('')} aria-label="Kapat"><X aria-hidden /></button></div>
          <div className="sa-ayar">
            <button type="button" onClick={() => void ayarKaydet({ sessiz: !odaBilgi.ayar.sessiz })}>
              {odaBilgi.ayar.sessiz ? <BellOff aria-hidden /> : <Bell aria-hidden />}Bildirimler<em className={odaBilgi.ayar.sessiz ? '' : 'is-on'}>{odaBilgi.ayar.sessiz ? 'Sessiz' : 'Açık'}</em>
            </button>
            <button type="button" onClick={() => void durumGizle()}>
              {odaBilgi.ayar.durumGizli ? <EyeOff aria-hidden /> : <Eye aria-hidden />}Son görülme ve çevrimiçi<em className={odaBilgi.ayar.durumGizli ? '' : 'is-on'}>{odaBilgi.ayar.durumGizli ? 'Gizli' : 'Görünür'}</em>
            </button>
          </div>
          <p className="v15-cap">Son görülmeyi gizlersen başkalarının son görülmesini de göremezsin. Bildirim ayarı yalnız bu sohbet içindir.</p>
        </div>
      )}
      <div className="tp15-zemin" data-tema={tema || undefined}>
        <SohbetZemin tema={tema} />
        <div ref={liste} className="tp15-liste" onScroll={kaydir} role="log" aria-live="polite" aria-relevant="additions" aria-label="Mesajlar" tabIndex={0}>
          {dahaVar && <button type="button" className="tp15-eski" onClick={eskiler}>Daha eski mesajlar</button>}
          {mesajlar === null ? <div className="tp15-iskelet is-balon" aria-hidden><span /><span className="is-ben" /><span /></div> : !mesajlar.length ? (
            <div className="tp15-bos">
              <span className="tp15-detay-ik"><MessageCircle aria-hidden /></span>
              <b>{oda ? (dm ? 'Sohbete başla' : 'Grup hazır') : kanalAdi(kanal)}</b>
              <span>{oda ? (dm ? 'İlk mesajı sen yaz.' : odaBilgi?.kod ? 'Menüden davet bağlantısını kopyalayıp arkadaşlarını çağır, sonra ilk mesajı yaz.' : 'İlk mesajı sen yaz.') : `${kanalAlt(kanal)}. İlk mesajı sen yaz.`}</span>
            </div>
          ) : mesajlar.map((x, i) => {
            const onceki = mesajlar[i - 1], sonraki = mesajlar[i + 1];
            const yeniGun = !onceki || new Date(onceki.at).toDateString() !== new Date(x.at).toDateString();
            const ilk = yeniGun || !(onceki.yazar === x.yazar && x.at - onceki.at < 5 * 60_000);
            const son = !sonraki || new Date(sonraki.at).toDateString() !== new Date(x.at).toDateString() || !(sonraki.yazar === x.yazar && sonraki.at - x.at < 5 * 60_000);
            const y = x.yanitId ? byId.get(x.yanitId) : null;
            const sadeceEk = !!x.ek && x.metin === `Paylaştı: ${x.ek.baslik}`;
            return (
              <React.Fragment key={x.id}>
                {yeniGun && <div className="tp15-gun" role="separator"><span>{gunEtiket(x.at)}</span></div>}
                <article className={`tp15-m${x.benim ? ' is-ben' : ''}${ilk ? ' is-ilk' : ''}${son ? ' is-son' : ''}${x.ek ? ' is-ek' : ''}`} style={{ '--t': ton(x.yazar) } as React.CSSProperties}
                  aria-label={`${x.benim ? 'Sen' : x.ad}, ${saatKisa(x.at)}`}>
                  <div className="tp15-balon">
                    {grupMu && !x.benim && ilk && <b className="tp15-ad-ust">{x.ad}{x.sikayet ? <span className="tp15-sk"> · {x.sikayet} bildirim</span> : null}</b>}
                    {x.yanitId && <p className="tp15-alinti">{y ? <><b>{y.benim ? 'Sen' : y.ad}</b>{y.metin.slice(0, 90)}</> : 'Silinmiş mesaja yanıt'}</p>}
                    {x.ek && <EkKart ek={x.ek} ac={git} />}
                    {!sadeceEk && <p>{x.metin}<span className="tp15-yer" aria-hidden /></p>}
                    <span className="tp15-saat"><time dateTime={new Date(x.at).toISOString()}>{saatKisa(x.at)}</time>{okundu(x)}</span>
                  </div>
                  <div className="tp15-is">
                    <button type="button" onClick={() => { setYanit(x); yazi.current?.focus(); }} aria-label="Yanıtla"><Reply aria-hidden /></button>
                    {!x.benim && girisli && <button type="button" onClick={() => git(`/kisi/${x.yazar}`)} aria-label="Profilini aç, arkadaş ekle"><UserRound aria-hidden /></button>}
                    {!oda && !x.benim && girisli && <button type="button" onClick={() => ozel(x)} aria-label="Özel mesaj gönder"><Mail aria-hidden /></button>}
                    {x.benim || x.sikayet !== undefined ? <button type="button" onClick={() => sil(x)} aria-label="Sil"><Trash2 aria-hidden /></button>
                      : oda ? null : <button type="button" onClick={() => bildir(x)} aria-label="Uygunsuz olarak bildir"><Flag aria-hidden /></button>}
                  </div>
                </article>
              </React.Fragment>
            );
          })}
        </div>
        {yeniVar > 0 && <button type="button" className="tp15-yenicip" onClick={() => enAlta()}>{yeniVar > 1 ? `${yeniVar} yeni mesaj` : 'Yeni mesaj'}<ArrowDown aria-hidden /></button>}
      </div>
      <div className="tp15-yaz">
        {hata && <p className="tp15-hata" role="status">{hata}<button type="button" onClick={() => setHata('')} aria-label="Uyarıyı kapat"><X aria-hidden /></button></p>}
        {!girisli ? <p className="v15-cap">Yazmak için giriş yapmalısın.</p> : (
          <>
            {yanit && <p className="tp15-yanit"><Reply aria-hidden /><span><b>{yanit.benim ? 'Sen' : yanit.ad}</b>{yanit.metin.slice(0, 70)}</span><button type="button" onClick={() => setYanit(null)} aria-label="Yanıtı kaldır"><X aria-hidden /></button></p>}
            {!ad && !oda && <input className="tp15-ad" value={ad} onChange={(e) => setAd(e.target.value.slice(0, 24))} placeholder="Görünen adın (isteğe bağlı)" aria-label="Görünen ad" />}
            {oda && panel === 'paylas' && <PaylasPaneli kapat={() => setPanel('')} sec={(e) => { setEk(e); setPanel(''); yazi.current?.focus(); }} />}
            {ek && <div className="tp15-yanit"><Share2 aria-hidden /><span><b>{ek.baslik}</b>{ek.alt ? ek.alt.slice(0, 50) : ''}</span><button type="button" onClick={() => setEk(null)} aria-label="Paylaşımı kaldır"><X aria-hidden /></button></div>}
            <div className="tp15-giris">
              {oda && <button type="button" className={`tp15-ib is-sade${panel === 'paylas' ? ' is-on' : ''}`} onClick={() => setPanel(panel === 'paylas' ? '' : 'paylas')} aria-label="Paylaş: sayfa, soru, favori, terim" aria-expanded={panel === 'paylas'}><Plus aria-hidden /></button>}
              <textarea ref={yazi} value={metin} onChange={(e) => setMetin(e.target.value.slice(0, 800))} placeholder={ek ? 'İstersen not ekle…' : 'Mesaj yaz'} rows={1} aria-label="Mesaj" enterKeyHint="send"
                onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) { e.preventDefault(); void gonder(); } }} />
              <button type="button" className="tp15-gonder" onClick={gonder} disabled={(!metin.trim() && !ek) || gonderiyor} aria-label="Gönder"><Send aria-hidden /></button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
