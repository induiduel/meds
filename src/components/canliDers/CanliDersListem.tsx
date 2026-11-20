/**
 * Canlı ders · "Listem" arayüzü: liste görünümü (liste sayfasında sekme), listeye ekle düğmesi, tekrar seçici ve
 * oynatıcıdaki önceki/sonraki ders denetimi. Durum canliDersListe.ts'tedir.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  BarChart3, CalendarDays, Check, CloudOff, Download, GripVertical, Headphones, ListChecks, ListCheck, Pencil, Plus, ListMusic, ListPlus, Pause, Play, Repeat, Repeat1, SkipBack, SkipForward, Trash2, X,
} from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import { cdTercihVaryant, cdToggle, fmtSure, useCd, type CdListeDers } from './canliDersStore';
import { cdDersEtiketi } from './canliDersKategori';
import { CD_CEVRIMDISI_DEGISTI, cdCevrimdisiKayitlari } from './canliDersCevrimdisiKayit';
import { useCevrimici } from './CanliDersCevrimdisi';
import { denemeGruplari, denemeKod, denemeKur, denemeSonuc, type DenemeGrup } from './listeDeneme';
import { bransTanim } from '../spots/brans';
import { cozucuDizinYukle, useIlerleme } from '../spots/cozucu/cozucuVeri';
import { guvenliLazy } from '../../utils/guvenliLazy';
import { toast } from '../ui/Toast';

const SoruCozucu = guvenliLazy(() => import('../spots/cozucu/SoruCozucu'));

// Liste sonuna gelinince deneme önerisi (Listem ekranı açık olmasa da)
if (typeof window !== 'undefined') {
  window.addEventListener('cd:liste-bitti', () => {
    toast.info('Liste bitti', 'Bu listenin derslerinden kısa bir sesli soru denemesi çözmek ister misin?', {
      label: 'Denemeyi aç', onClick: () => navigateTo(`${pathFor('canli_ders')}#liste-deneme`),
    });
  });
}
import {
  CD_TEKRAR_SAYILAR, cdListeAdlandir, cdListeSec, cdListeSil, cdListeTopluEkle, cdListeYeni, cdListeAtla, cdListeCikar, cdListeDegistir, cdListeKonumla, cdListeOzetleri, cdListeOynat, cdListeTasi, cdListeTemizle, cdTekrarAyarla,
  tekrarSayiYaz, useCdListe, useCdListeSira, type CdTekrarMod,
} from './canliDersListe';

/* ---------------- listeye ekle ---------------- */

export function ListeEkleDugme({ dersKey, baslik, etiketli }: { dersKey: string; baslik: string; etiketli?: boolean }) {
  const ekli = useCdListe((s) => s.keys.includes(dersKey));
  const ad = ekli ? 'Listemden çıkar' : 'Listeme ekle';
  return (
    <button
      type="button"
      className={`cd-btn${etiketli ? '' : ' is-ikon'}${ekli ? ' is-on' : ''}`}
      onClick={() => cdListeDegistir(dersKey)}
      aria-pressed={ekli}
      aria-label={`${ad}: ${baslik}`}
      title={ad}
    >
      {ekli ? <ListCheck aria-hidden /> : <ListPlus aria-hidden />}
      {etiketli && <span>{ekli ? 'Listemde' : 'Listeme ekle'}</span>}
    </button>
  );
}

/** Sesli ders ekranından listelere tek dokunuşla geçiş (seçili liste adı + ders sayısı) */
export function ListelerimDugme() {
  const l = useCdListe((s) => s.listeler.find((x) => x.id === s.seciliId));
  return (
    <button type="button" className="cd-btn" onClick={() => navigateTo(`${pathFor('canli_ders')}#listem`)} title="Oynatma listelerimi aç">
      <ListMusic aria-hidden /> <span>Listelerim{l ? ` · ${l.ad} (${l.keys.length})` : ''}</span>
    </button>
  );
}

/* ---------------- toplu ekle ---------------- */

/** Bir branşın / bloğun bütün derslerini seçili listeye ekler; hepsi listedeyse "Listede" gösterir */
export function TopluEkleDugme({ keys, ad }: { keys: string[]; ad: string }) {
  const listeAd = useCdListe((s) => s.listeler.find((l) => l.id === s.seciliId)?.ad || 'Listem');
  const eksik = useCdListe((s) => keys.filter((k) => !s.keys.includes(k)).length);
  const [son, setSon] = useState<number | null>(null);
  useEffect(() => {
    if (son == null) return;
    const t = window.setTimeout(() => setSon(null), 2500);
    return () => window.clearTimeout(t);
  }, [son]);
  if (!keys.length) return null;
  const hepsi = eksik === 0;
  return (
    <button
      type="button"
      className={`cd-btn is-ince cd-toplu${hepsi ? ' is-on' : ''}`}
      onClick={(e) => { e.stopPropagation(); if (!hepsi) setSon(cdListeTopluEkle(keys)); }}
      disabled={hepsi}
      title={hepsi ? `Hepsi "${listeAd}" listesinde` : `${ad}: ${eksik} dersi "${listeAd}" listesine ekle`}
      aria-label={hepsi ? `${ad}: hepsi ${listeAd} listesinde` : `${ad}: ${eksik} dersi ${listeAd} listesine ekle`}
    >
      {hepsi ? <ListCheck aria-hidden /> : <ListPlus aria-hidden />}
      <span>{son != null ? `${son} eklendi` : hepsi ? 'Listede' : `Tümünü ekle (${eksik})`}</span>
    </button>
  );
}

/* ---------------- liste seçici (çoklu liste) ---------------- */

function ListeSecici() {
  const listeler = useCdListe((s) => s.listeler);
  const seciliId = useCdListe((s) => s.seciliId);
  const [duzen, setDuzen] = useState<null | { id: string | null; ad: string }>(null);
  const [silOnay, setSilOnay] = useState<string | null>(null);
  const kaydet = () => {
    if (!duzen) return;
    if (duzen.id) cdListeAdlandir(duzen.id, duzen.ad);
    else cdListeYeni(duzen.ad);
    setDuzen(null);
  };
  return (
    <div className="cd-lsec" role="tablist" aria-label="Listelerim">
      {listeler.map((l) =>
        duzen?.id === l.id ? null : (
          <button key={l.id} type="button" role="tab" aria-selected={l.id === seciliId}
            className={`cd-chip cd-lsec-c${l.id === seciliId ? ' is-on' : ''}`} onClick={() => cdListeSec(l.id)}>
            {l.ad} <small>{l.keys.length}</small>
          </button>
        ),
      )}
      {duzen ? (
        <form className="cd-lsec-form" onSubmit={(e) => { e.preventDefault(); kaydet(); }}>
          <input autoFocus maxLength={40} value={duzen.ad} placeholder="Liste adı" aria-label="Liste adı"
            onChange={(e) => setDuzen({ ...duzen, ad: e.target.value })} onKeyDown={(e) => e.key === 'Escape' && setDuzen(null)} />
          <button type="submit" className="cd-btn is-ikon" aria-label="Kaydet" title="Kaydet"><Check aria-hidden /></button>
          <button type="button" className="cd-btn is-ikon" aria-label="Vazgeç" title="Vazgeç" onClick={() => setDuzen(null)}><X aria-hidden /></button>
        </form>
      ) : (
        <>
          <button type="button" className="cd-btn is-ince" onClick={() => setDuzen({ id: null, ad: '' })} title="Yeni liste">
            <Plus aria-hidden /> <span>Yeni liste</span>
          </button>
          <button type="button" className="cd-btn is-ikon" title="Listeyi yeniden adlandır" aria-label="Seçili listeyi yeniden adlandır"
            onClick={() => setDuzen({ id: seciliId, ad: listeler.find((l) => l.id === seciliId)?.ad || '' })}>
            <Pencil aria-hidden />
          </button>
          {listeler.length > 1 && (
            <button type="button" className={`cd-btn is-ikon${silOnay === seciliId ? ' is-tehlike' : ''}`}
              title={silOnay === seciliId ? 'Silmek için yeniden dokun' : 'Listeyi sil'}
              aria-label={silOnay === seciliId ? 'Emin misin? Listeyi sil' : 'Seçili listeyi sil'}
              onClick={() => (silOnay === seciliId ? (cdListeSil(seciliId), setSilOnay(null)) : setSilOnay(seciliId))}>
              <Trash2 aria-hidden />
            </button>
          )}
        </>
      )}
    </div>
  );
}

/* ---------------- tekrar seçici ---------------- */

const MODLAR: { mod: CdTekrarMod; ad: string; alt: string }[] = [
  { mod: 'kapali', ad: 'Tekrar yok', alt: 'Ders / liste bitince durur' },
  { mod: 'ders', ad: 'Dersi tekrarla', alt: 'Biten ders yeniden çalar' },
  { mod: 'liste', ad: 'Listeyi tekrarla', alt: 'Liste bitince başa döner' },
];

export function TekrarSecici({ yukari = true }: { yukari?: boolean }) {
  const mod = useCdListe((s) => s.mod);
  const sayi = useCdListe((s) => s.sayi);
  // Ders tekrarı sürerken kaçıncı tekrarda olunduğu ("1/3"); ilk çalışta yalnız sayı
  const tur = useCdListe((s) => (s.mod === 'ders' ? s.dersTur : s.mod === 'liste' ? s.listeTur : 0));
  const [acik, setAcik] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!acik) return;
    const dis = (e: PointerEvent) => { if (!ref.current?.contains(e.target as Node)) setAcik(false); };
    const esc = (e: KeyboardEvent) => { if (e.key === 'Escape') { e.stopPropagation(); setAcik(false); } };
    document.addEventListener('pointerdown', dis);
    document.addEventListener('keydown', esc, true);
    requestAnimationFrame(() => ref.current?.querySelector<HTMLElement>('.cd-tk-mod[aria-checked="true"]')?.focus());
    return () => {
      document.removeEventListener('pointerdown', dis);
      document.removeEventListener('keydown', esc, true);
    };
  }, [acik]);
  const ozet = mod === 'kapali' ? 'Tekrar kapalı' : `${mod === 'ders' ? 'Ders' : 'Liste'} tekrarı ${sayi === 0 ? 'sınırsız' : `${sayi} kez`}`;
  const Ikon = mod === 'ders' ? Repeat1 : Repeat;
  return (
    <div className="cd-menu-kap" ref={ref}>
      <button
        type="button"
        className={`cd-ib cd-tk-btn${mod !== 'kapali' ? ' is-on' : ''}`}
        aria-haspopup="dialog"
        aria-expanded={acik}
        onClick={() => setAcik((x) => !x)}
        title={ozet}
        aria-label={`Tekrar: ${ozet}`}
      >
        <Ikon aria-hidden />
        {mod === 'kapali'
          ? <span className="cd-tk-ad">Tekrar</span>
          : <span className="cd-tk-sayi">{tur > 0 ? `${tur}/${sayi === 0 ? '∞' : sayi}` : tekrarSayiYaz(sayi)}</span>}
      </button>
      {acik && (
        <div className={`cd-tk-menu${yukari ? '' : ' is-asagi'}`} role="dialog" aria-label="Tekrar">
          <div role="radiogroup" aria-label="Tekrar türü">
            {MODLAR.map((m) => (
              <button
                key={m.mod}
                type="button"
                role="radio"
                aria-checked={mod === m.mod}
                className="cd-tk-mod"
                onClick={() => cdTekrarAyarla(m.mod)}
              >
                <span className="cd-tk-nokta" aria-hidden />
                <span><b>{m.ad}</b><small>{m.alt}</small></span>
              </button>
            ))}
          </div>
          <div className={`cd-tk-sayilar${mod === 'kapali' ? ' is-kapali' : ''}`}>
            <span>Kaç kez</span>
            <div role="radiogroup" aria-label="Tekrar sayısı">
              {CD_TEKRAR_SAYILAR.map((n) => (
                <button
                  key={n}
                  type="button"
                  role="radio"
                  aria-checked={mod !== 'kapali' && sayi === n}
                  aria-label={n === 0 ? 'Sınırsız' : `${n} kez`}
                  title={n === 0 ? 'Sınırsız (döngü)' : `${n} kez daha`}
                  disabled={mod === 'kapali'}
                  onClick={() => cdTekrarAyarla(mod, n)}
                >
                  {tekrarSayiYaz(n)}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ---------------- oynatıcıda liste denetimi ---------------- */

/** Liste çalarken: önceki ders · "Liste 2/5" · sonraki ders */
/** dar: telefonda denetimlerin üstünde ayrı satır (masaüstünde gizli; masaüstünde sol gruptaki görünür) */
export function ListeDockDenetim({ mini, dar }: { mini?: boolean; dar?: boolean }) {
  const sira = useCdListeSira();
  const n = useCdListe((s) => s.keys.length);
  if (sira < 0) return null;
  const git = () => navigateTo(`${pathFor('canli_ders')}#listem`);
  return (
    <div className={`cd-ld${mini ? ' is-mini' : ''}${dar ? ' is-dar' : ''}`}>
      {!mini && (
        <button type="button" className="cd-ib" onClick={() => cdListeAtla(-1)} disabled={sira === 0} aria-label="Listede önceki ders" title="Önceki ders">
          <SkipBack aria-hidden />
        </button>
      )}
      {!mini && (
        <button type="button" className="cd-ld-sira" onClick={git} title="Listemi aç" aria-label={`Listem: ${sira + 1}. ders / ${n}`}>
          <ListMusic aria-hidden />
          <span>{sira + 1}/{n}</span>
        </button>
      )}
      <button type="button" className="cd-ib" onClick={() => cdListeAtla(1)} disabled={sira >= n - 1} aria-label="Listede sonraki ders" title="Sonraki ders">
        <SkipForward aria-hidden />
      </button>
    </div>
  );
}

/* ---------------- liste görünümü ---------------- */

/** Tekrar: tür + kaç kez, açılır menü olmadan doğrudan seçilir (liste ekranı) */
function TekrarSerit() {
  const mod = useCdListe((s) => s.mod);
  const sayi = useCdListe((s) => s.sayi);
  const TURLER: [CdTekrarMod, string, React.ReactNode][] = [
    ['kapali', 'Kapalı', null], ['ders', 'Ders', <Repeat1 key="d" aria-hidden />], ['liste', 'Liste', <Repeat key="l" aria-hidden />],
  ];
  return (
    <div className="cd-lm-tekrar">
      <span className="cd-lm-et">Tekrar</span>
      <div className="cd-lm-seg" role="radiogroup" aria-label="Tekrar türü">
        {TURLER.map(([m, ad, ik]) => (
          <button key={m} type="button" role="radio" aria-checked={mod === m} onClick={() => cdTekrarAyarla(m)}
            title={MODLAR.find((x) => x.mod === m)?.alt}>{ik}{ad}</button>
        ))}
      </div>
      <div className={`cd-lm-seg is-sayi${mod === 'kapali' ? ' is-kapali' : ''}`} role="radiogroup" aria-label="Tekrar sayısı">
        {CD_TEKRAR_SAYILAR.map((n) => (
          <button key={n} type="button" role="radio" aria-checked={mod !== 'kapali' && sayi === n} disabled={mod === 'kapali'}
            aria-label={n === 0 ? 'Sınırsız' : `${n} kez`} title={n === 0 ? 'Sınırsız döngü' : `${n} kez daha çal`}
            onClick={() => cdTekrarAyarla(mod, n)}>{tekrarSayiYaz(n)}</button>
        ))}
      </div>
    </div>
  );
}

/** Listedeki indirilmemiş dersleri sırayla cihaza indirir (çevrimdışı dinleme) */
function ListeIndir({ keys }: { keys: string[] }) {
  const [kayit, setKayit] = useState(() => cdCevrimdisiKayitlari());
  const [is, setIs] = useState<{ i: number; n: number; hata: number } | null>(null);
  const online = useCevrimici();
  useEffect(() => {
    const f = () => setKayit(cdCevrimdisiKayitlari());
    window.addEventListener(CD_CEVRIMDISI_DEGISTI, f);
    return () => window.removeEventListener(CD_CEVRIMDISI_DEGISTI, f);
  }, []);
  const eksik = keys.filter((k) => !kayit[k]);
  const indir = async () => {
    const liste = eksik.slice();
    let hata = 0;
    for (let i = 0; i < liste.length; i++) {
      setIs({ i, n: liste.length, hata });
      try { await (await import('./canliDersCevrimdisi')).cdCevrimdisiIndir(liste[i]); } catch { hata++; }
    }
    setIs(null);
    if (hata) window.alert(`${hata} ders indirilemedi; yeniden dene.`);
  };
  if (is) return <span className="cd-btn is-ince cd-lm-indir is-is" role="status"><span className="cd-spin" aria-hidden />{is.i + 1}/{is.n} iniyor</span>;
  if (!eksik.length) return <span className="cd-lm-cihazda" title="Listedeki bütün dersler cihazda; internetsiz çalar"><CloudOff aria-hidden />Hepsi cihazda</span>;
  return (
    <button type="button" className="cd-btn is-ince cd-lm-indir" onClick={indir} disabled={!online || typeof caches === 'undefined'}
      title={online ? `${eksik.length} dersi internetsiz dinlemek için indir` : 'İndirmek için internet gerekir'}>
      <Download aria-hidden /><span>İndir ({eksik.length})</span>
    </button>
  );
}

const saatYaz = (sn: number) => {
  const dk = Math.round(sn / 60);
  return dk < 60 ? `${dk} dk` : `${Math.floor(dk / 60)} sa ${dk % 60 ? `${dk % 60} dk` : ''}`.trim();
};
const tarihYaz = (ms?: number) => (ms ? new Date(ms).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', year: 'numeric' }) : '—');
const goreli = (ms?: number) => {
  if (!ms) return 'Henüz dinlenmedi';
  const g = Math.floor((Date.now() - ms) / 864e5);
  return g <= 0 ? 'Bugün' : g === 1 ? 'Dün' : `${g} gün önce`;
};

function ListeIstatistik() {
  const l = useCdListe((s) => s.listeler.find((x) => x.id === s.seciliId));
  const i = l?.ist;
  const ogeler: [React.ReactNode, string, string][] = [
    [<Headphones key="h" aria-hidden />, saatYaz(i?.sn || 0), 'Dinlenen süre'],
    [<ListChecks key="b" aria-hidden />, String(i?.ders || 0), 'Bitirilen ders'],
    [<Repeat1 key="t" aria-hidden />, String(i?.tekrar || 0), 'Ders tekrarı'],
    [<Repeat key="l" aria-hidden />, String(i?.tur || 0), 'Liste turu'],
    [<CalendarDays key="c" aria-hidden />, tarihYaz(l?.olusturma), 'Oluşturuldu'],
    [<BarChart3 key="s" aria-hidden />, goreli(i?.son), 'Son dinleme'],
  ];
  return (
    <section className="cd-lm-ist" aria-label="Liste istatistikleri">
      {ogeler.map(([ik, v, ad]) => (
        <div key={ad} className="cd-lm-ist-k"><span className="cd-lm-ist-i">{ik}</span><b>{v}</b><small>{ad}</small></div>
      ))}
    </section>
  );
}

function ListeDeneme({ dersler, onAc }: { dersler: CdListeDers[]; onAc: (g: DenemeGrup) => void }) {
  const seciliId = useCdListe((s) => s.seciliId);
  const ilerleme = useIlerleme();
  const gruplar = useMemo(() => denemeGruplari(dersler), [dersler]);
  if (!dersler.length) return null;
  return (
    <section className="cd-lm-deneme" aria-label="Liste denemesi">
      <div className="cd-lm-deneme-bas">
        <b>Liste sonu deneme</b>
        <small>Listedeki derslerin örnek sorularından sesli çözücü. Liste bitince de önerilir.</small>
      </div>
      {!gruplar.length ? (
        <p className="cd-lm-deneme-yok">Bu listedeki dersler için henüz sesli çözücü sorusu yok.</p>
      ) : (
        <div className="cd-lm-deneme-ler">
          {gruplar.map((g) => {
            const o = ilerleme[denemeKod(seciliId, g.brans)] ? denemeSonuc(seciliId, g.brans, g.soru) : null;
            return (
              <button key={g.brans} type="button" className="cd-lm-deneme-k" onClick={() => onAc(g)}>
                <span className="cd-lm-deneme-ust"><b>{bransTanim(g.brans).ad}</b><small>{g.kodlar.length} ders · {g.soru} soru</small></span>
                {o && o.cozulen > 0 && (
                  <span className="cd-lm-deneme-skor">
                    <span className="cd-lm-deneme-bar" aria-hidden><i style={{ width: `${(o.d / g.soru) * 100}%` }} /><i className="is-y" style={{ width: `${(o.y / g.soru) * 100}%` }} /></span>
                    <small>{o.d} doğru · {o.y} yanlış{o.tamam ? '' : ` · ${o.cozulen}/${g.soru}`}</small>
                  </span>
                )}
                <span className="v15-btn is-primary cd-lm-deneme-git"><Play aria-hidden />{o?.tamam ? 'Yeniden çöz' : o?.cozulen ? 'Devam et' : 'Başla'}</span>
              </button>
            );
          })}
        </div>
      )}
    </section>
  );
}

export function Listem({ dersler, onTumu }: { dersler: CdListeDers[]; onTumu: () => void }) {
  const keys = useCdListe((s) => s.keys);
  const sira = useCdListeSira();
  const playing = useCd((s) => s.playing);
  const online = useCevrimici();
  const [onay, setOnay] = useState(false);
  const [kayit, setKayit] = useState(() => cdCevrimdisiKayitlari());
  useEffect(() => {
    const f = () => setKayit(cdCevrimdisiKayitlari());
    window.addEventListener(CD_CEVRIMDISI_DEGISTI, f);
    return () => window.removeEventListener(CD_CEVRIMDISI_DEGISTI, f);
  }, []);
  // Oynatma kuyruğu eşzamanlı başlasın (mobil izin) — sayfadaki liste özetlerini depoya ver
  useEffect(() => { if (dersler.length) cdListeOzetleri(dersler); }, [dersler]);
  const harita = useMemo(() => new Map(dersler.map((d) => [d.key, d])), [dersler]);
  const ogeler = useMemo(() => keys.map((k) => harita.get(k)).filter((d): d is CdListeDers => !!d), [keys, harita]);
  const toplam = ogeler.reduce((a, d) => a + ((cdTercihVaryant(d.varyantlar) || d.varsayilan)?.sureSn || 0), 0);
  const caliyorKey = sira >= 0 ? keys[sira] : null;
  const listeAd = useCdListe((s) => s.listeler.find((l) => l.id === s.seciliId)?.ad || 'Listem');
  const seciliId = useCdListe((s) => s.seciliId);
  const [deneme, setDeneme] = useState<DenemeGrup | null>(null);
  const denemeAc = (g: DenemeGrup) => setDeneme(g);
  // Liste bitti bildiriminden gelindiyse ilk denemeyi aç
  useEffect(() => {
    const f = () => {
      if (location.hash !== '#liste-deneme') return;
      const g = denemeGruplari(ogeler)[0];
      if (g) setDeneme(g);
      try { history.replaceState(history.state, '', location.pathname + location.search + '#listem'); } catch { /* yok */ }
    };
    f();
    window.addEventListener('hashchange', f);
    return () => window.removeEventListener('hashchange', f);
  }, [ogeler]);
  const denemeKaynak = useMemo(() => (deneme ? {
    ders: () => denemeKur(seciliId, listeAd, deneme),
    dizin: () => cozucuDizinYukle(deneme.brans),
    etiket: `${listeAd} denemesi`,
  } : null), [deneme, seciliId, listeAd]);

  /* sürükle-bırak (fare + dokunmatik, pointer olayları) */
  const olRef = useRef<HTMLOListElement>(null);
  const [surukle, setSurukle] = useState<{ key: string; hedef: number; dy: number } | null>(null);
  const basla = (e: React.PointerEvent, key: string) => {
    if (e.button !== 0) return;
    e.preventDefault();
    const ol = olRef.current; if (!ol) return;
    const li = (e.currentTarget as HTMLElement).closest('li')!;
    const y0 = e.clientY;
    const satirlar = [...ol.children] as HTMLElement[];
    const ortalar = satirlar.map((r) => { const b = r.getBoundingClientRect(); return b.top + b.height / 2; });
    const i0 = satirlar.indexOf(li);
    const sc = ol.closest('.sl15-alan, .cdl-icerik') as HTMLElement | null;
    const s0 = sc?.scrollTop || 0;
    let hedef = i0;
    (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
    setSurukle({ key, hedef, dy: 0 });
    const hareket = (ev: PointerEvent) => {
      const dy = ev.clientY - y0;
      const y = ortalar[i0] + dy + ((sc?.scrollTop || 0) - s0);
      hedef = ortalar.filter((o, j) => j !== i0 && o < y).length;
      setSurukle({ key, hedef, dy });
      // kenara yaklaşınca kaydır
      if (sc) { const b = sc.getBoundingClientRect(); if (ev.clientY < b.top + 40) sc.scrollTop -= 8; else if (ev.clientY > b.bottom - 40) sc.scrollTop += 8; }
    };
    const bitir = () => {
      window.removeEventListener('pointermove', hareket);
      window.removeEventListener('pointerup', bitir);
      window.removeEventListener('pointercancel', bitir);
      cdListeKonumla(key, hedef);
      setSurukle(null);
    };
    window.addEventListener('pointermove', hareket);
    window.addEventListener('pointerup', bitir);
    window.addEventListener('pointercancel', bitir);
  };
  const tusla = (e: React.KeyboardEvent, key: string) => {
    if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
      e.preventDefault();
      cdListeTasi(key, e.key === 'ArrowUp' ? -1 : 1);
      requestAnimationFrame(() => olRef.current?.querySelector<HTMLElement>(`[data-k="${CSS.escape(key)}"] .cd-lm-tut`)?.focus());
    }
  };

  useEffect(() => {
    if (!onay) return;
    const t = window.setTimeout(() => setOnay(false), 4000);
    return () => window.clearTimeout(t);
  }, [onay]);

  // sürüklenirken gösterilecek sıra
  const gorunen = useMemo(() => {
    if (!surukle) return ogeler;
    const a = ogeler.filter((d) => d.key !== surukle.key);
    const d = ogeler.find((x) => x.key === surukle.key);
    if (d) a.splice(surukle.hedef, 0, d);
    return a;
  }, [ogeler, surukle]);

  return (
    <section className="cd-lm" aria-label={listeAd}>
      <ListeSecici />
      {!ogeler.length ? (
        <div className="cd-bos cd-lm-bos">
          <span className="cd-ikon" aria-hidden><ListMusic /></span>
          <p><b>"{listeAd}" boş.</b> Ders satırındaki <ListPlus aria-label="listeye ekle" className="cd-satir-ikon" /> ile tek ders, branş başlığındaki <b>Tümünü ekle</b> ile bütün branşı ekle. Liste sırayla, kendiliğinden çalar.</p>
          <button type="button" className="cd-btn" onClick={onTumu}>Derslere git</button>
        </div>
      ) : (
        <>
          <div className="cd-lm-kart v15-card">
            <div className="cd-lm-bas">
              <span className="cd-lm-kapak" aria-hidden><ListMusic /></span>
              <div className="cd-lm-bilgi">
                <b>{listeAd}</b>
                <small>{ogeler.length} ders · {fmtSure(toplam)}{!online && ' · çevrimdışı'}</small>
              </div>
              {sira >= 0 ? (
                <button type="button" className="v15-btn is-primary cd-lm-oynat" onClick={cdToggle}>
                  {playing ? <Pause aria-hidden /> : <Play aria-hidden />}<span>{playing ? 'Duraklat' : 'Sürdür'}</span>
                </button>
              ) : (
                <button type="button" className="v15-btn is-primary cd-lm-oynat" onClick={() => cdListeOynat()}>
                  <Play aria-hidden /><span>Oynat</span>
                </button>
              )}
            </div>
            <div className="cd-lm-alt">
              <TekrarSerit />
              <div className="cd-lm-sag">
                <ListeIndir keys={ogeler.map((d) => d.key)} />
                <button type="button" className={`cd-btn is-ikon${onay ? ' is-tehlike' : ''}`}
                  onClick={() => (onay ? (cdListeTemizle(), setOnay(false)) : setOnay(true))}
                  aria-label={onay ? 'Emin misin? Listeyi boşalt' : 'Listeyi boşalt'} title={onay ? 'Onaylamak için yeniden dokun' : 'Listeyi boşalt'}>
                  <Trash2 aria-hidden />
                </button>
              </div>
            </div>
          </div>
          <ol className={`cd-lm-ogeler${surukle ? ' is-surukle' : ''}`} ref={olRef}>
            {gorunen.map((d, k) => {
              const v = cdTercihVaryant(d.varyantlar) || d.varsayilan;
              const bu = d.key === caliyorKey;
              const cihazda = !!kayit[d.key];
              const calamaz = !online && !cihazda;
              const tutulan = surukle?.key === d.key;
              return (
                <li key={d.key} data-k={d.key} className={`cd-lm-oge${bu ? ' is-caliyor' : ''}${tutulan ? ' is-tutulan' : ''}${calamaz ? ' is-calamaz' : ''}`}>
                  <button type="button" className="cd-lm-tut" onPointerDown={(e) => basla(e, d.key)} onKeyDown={(e) => tusla(e, d.key)}
                    aria-label={`Sırayı değiştir: ${d.baslik} (ok tuşlarıyla taşı)`} title="Sürükleyerek sırala">
                    <GripVertical aria-hidden />
                  </button>
                  <span className="cd-lm-no" aria-hidden>{bu && playing ? <span className="cd-lm-eq"><i /><i /><i /></span> : k + 1}</span>
                  <button type="button" className="cd-lm-ad" disabled={calamaz}
                    onClick={() => (bu ? cdToggle() : cdListeOynat(d.key))}
                    aria-label={bu ? `${playing ? 'Duraklat' : 'Sürdür'}: ${d.baslik}` : `Listeyi bu dersten oynat: ${d.baslik}`}>
                    <b>{d.baslik}</b>
                    <small>
                      <span>{cdDersEtiketi(d)}</span>
                      {v && <span>{fmtSure(v.sureSn)}</span>}
                      {cihazda && <span className="cd-lm-cd" title="Cihazda, internetsiz çalar"><Download aria-label="Cihazda" /></span>}
                      {calamaz && <span>İnternet gerekir</span>}
                    </small>
                  </button>
                  <button type="button" className="cd-btn is-ikon cd-lm-cikar" onClick={() => cdListeCikar(d.key)} aria-label={`Listeden çıkar: ${d.baslik}`} title="Listeden çıkar">
                    <X aria-hidden />
                  </button>
                </li>
              );
            })}
          </ol>
          <p className="cd-lm-ipucu"><GripVertical aria-hidden /> Sırayı değiştirmek için tutup sürükle.</p>
          <ListeDeneme dersler={ogeler} onAc={denemeAc} />
          <ListeIstatistik />
        </>
      )}
      {deneme && denemeKaynak && (
        <React.Suspense fallback={null}>
          <SoruCozucu key={`${seciliId}-${deneme.brans}`} brans={deneme.brans} kod={denemeKod(seciliId, deneme.brans)}
            kaynak={denemeKaynak} onClose={() => setDeneme(null)} />
        </React.Suspense>
      )}
    </section>
  );
}
