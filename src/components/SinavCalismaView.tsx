/**
 * Sınav Çalışması (/sinav-calisma) — Kurul 1'in her kazanımı için kısa özet + örnek ve çıkmış sorular.
 * İskelet (v12 dili, Örnek sorular / Kazanımlar ile aynı): başlık + sayaç · arama · ders sekmesi · durum süzgeci,
 * geniş ekranda solda konu listesi, telefonda konu seçici; kazanım satırı açılınca özet, slayt bağlantıları,
 * adım adım soru çözme ve sesli çözücü. Veri konu başına parça parça gelir (sinavCalisma/sinavVeri.ts).
 * Adres: ?ders=<sıra>&konu=<dosya>&kz=<kazanım id> — paylaşılabilir, geri tuşu sayfadan çıkar (replaceState).
 * Stil: styles/sinav-calisma.css (.scw-*), yalnız palet tokenı; her tasarımda (v10/v11/v12) ve temada çalışır.
 */
import React, { useCallback, useDeferredValue, useEffect, useId, useMemo, useRef, useState } from 'react';
import {
  BookOpen, Check, ChevronDown, ChevronLeft, ChevronRight, Copy, Headphones, Lightbulb, Presentation, RotateCcw, Search, X,
} from 'lucide-react';
import { SoruCozucu } from './spots/cozucu/SoruCozucu';
import type { Harf, Sonuc as CozucuSonuc } from './spots/cozucu/cozucuVeri';
import { toast } from './ui/Toast';
import { navigateTo } from '../router';
import {
  cozucuSorulari, dizinYukle, ilerlemeOku, ilerlemeYaz, katla, konuYukle, ILERLEME_KEY,
  type Ilerleme, type KonuOzet, type KzAyrinti, type KzOzet, type SinavDizin, type SSoru, type Zorluk,
} from './sinavCalisma/sinavVeri';
import '../styles/sinav-calisma.css';

const HARF: Harf[] = ['A', 'B', 'C', 'D', 'E'];
const sayi = (n: number) => n.toLocaleString('tr-TR');
type Durum = 'hepsi' | 'baslanmadi' | 'devam' | 'tamam';
const DURUMLAR: { id: Durum; ad: string }[] = [
  { id: 'hepsi', ad: 'Tümü' },
  { id: 'baslanmadi', ad: 'Başlanmadı' },
  { id: 'devam', ad: 'Yarım kalan' },
  { id: 'tamam', ad: 'Bitti' },
];
type SoruSuzgec = 'hepsi' | Zorluk | 'cikmis';
const ZORLUK_AD: Record<Zorluk, string> = { kolay: 'Kolay', orta: 'Orta', zor: 'Zor' };

const adresOku = () => {
  try {
    const p = new URLSearchParams(window.location.search);
    return { ders: Math.max(0, parseInt(p.get('ders') || '0', 10) || 0), konu: p.get('konu') || 'hepsi', kz: p.get('kz') };
  } catch {
    return { ders: 0, konu: 'hepsi', kz: null as string | null };
  }
};
const adresYaz = (v: { ders: number; konu: string; kz: string | null }) => {
  try {
    const u = new URL(window.location.href);
    if (v.ders) u.searchParams.set('ders', String(v.ders)); else u.searchParams.delete('ders');
    if (v.konu !== 'hepsi') u.searchParams.set('konu', v.konu); else u.searchParams.delete('konu');
    if (v.kz) u.searchParams.set('kz', v.kz); else u.searchParams.delete('kz');
    window.history.replaceState(window.history.state, '', u.pathname + u.search + u.hash);
  } catch { /* adres yazılamadı: sayfa yine çalışır */ }
};

/** Açıklamalardaki **kalın** ve satır sonlarını gösterir (tam markdown gerekmez) */
const Metin: React.FC<{ metin: string }> = ({ metin }) => (
  <>
    {metin.split(/\n+/).filter(Boolean).map((p, i) => (
      <p key={i}>
        {p.replace(/^\s*[-•]\s+/, '• ').split(/(\*\*[^*]+\*\*)/).map((x, j) =>
          x.startsWith('**') && x.endsWith('**') ? <strong key={j}>{x.slice(2, -2)}</strong> : <React.Fragment key={j}>{x}</React.Fragment>,
        )}
      </p>
    ))}
  </>
);

const kzDurum = (kz: KzOzet, il: Ilerleme): Exclude<Durum, 'hepsi'> => {
  const n = Object.keys(il[kz.id] || {}).length;
  return n === 0 ? 'baslanmadi' : n >= kz.soru ? 'tamam' : 'devam';
};

export const SinavCalismaView: React.FC = () => {
  const ilk = useRef(adresOku()).current;
  const [dizin, setDizin] = useState<SinavDizin | null>(null);
  const [hata, setHata] = useState(false);
  const [dersI, setDersI] = useState(ilk.ders);
  const [konu, setKonu] = useState(ilk.konu);
  const [acik, setAcik] = useState<string | null>(ilk.kz);
  const [arama, setArama] = useState('');
  const q = useDeferredValue(arama);
  const [durum, setDurum] = useState<Durum>('hepsi');
  const [ilerleme, setIlerleme] = useState<Ilerleme>(ilerlemeOku);
  const [cozucu, setCozucu] = useState<{ baslik: string; sorular: SSoru[]; kzId: string; anlatim?: string[] } | null>(null);

  const yukle = useCallback(() => {
    setHata(false);
    dizinYukle().then(setDizin).catch(() => setHata(true));
  }, []);
  useEffect(yukle, [yukle]);

  // Profil eşitlemesi başka cihazdan ilerleme getirirse ekrana yansısın
  useEffect(() => {
    const yenile = (e: StorageEvent) => { if (!e.key || e.key === ILERLEME_KEY) setIlerleme(ilerlemeOku()); };
    window.addEventListener('storage', yenile);
    return () => window.removeEventListener('storage', yenile);
  }, []);

  const dersler = dizin?.dersler ?? [];
  const ders = dersler[Math.min(dersI, Math.max(0, dersler.length - 1))];

  useEffect(() => { if (dizin) adresYaz({ ders: dersI, konu, kz: acik }); }, [dizin, dersI, konu, acik]);
  // Adresle gelen kazanım: ekrana kaydır
  useEffect(() => {
    if (!dizin || !ilk.kz) return;
    const t = window.setTimeout(() => document.getElementById(`scw-kz-${ilk.kz}`)?.scrollIntoView({ block: 'start', behavior: 'smooth' }), 120);
    return () => window.clearTimeout(t);
  }, [dizin, ilk.kz]);

  const sonucYaz = useCallback((kzId: string, soruId: string, s: 'd' | 'y') => {
    setIlerleme((prev) => {
      const next = { ...prev, [kzId]: { ...(prev[kzId] || {}), [soruId]: s } };
      ilerlemeYaz(next);
      return next;
    });
  }, []);
  const kzSifirla = useCallback((kzId: string) => {
    setIlerleme((prev) => {
      const next = { ...prev };
      delete next[kzId];
      ilerlemeYaz(next);
      return next;
    });
  }, []);

  // Arama: kazanım metni ya da konu adı (katlanmış). Ders sekmelerinde eşleşme sayısı görünür.
  const qk = katla(q.trim());
  const eslesir = useCallback((k: KonuOzet, kz: KzOzet) => !qk || katla(kz.metin).includes(qk) || katla(k.ad).includes(qk), [qk]);

  const dersSayac = useMemo(
    () => dersler.map((d) => d.konular.reduce((t, k) => t + k.kazanimlar.filter((kz) => eslesir(k, kz)).length, 0)),
    [dersler, eslesir],
  );

  const konular = useMemo(() => {
    if (!ders) return [];
    return ders.konular
      .filter((k) => konu === 'hepsi' || k.dosya === konu)
      .map((k) => ({ ...k, kazanimlar: k.kazanimlar.filter((kz) => eslesir(k, kz) && (durum === 'hepsi' || kzDurum(kz, ilerleme) === durum)) }))
      .filter((k) => k.kazanimlar.length > 0);
  }, [ders, konu, eslesir, durum, ilerleme]);

  const genel = useMemo(() => {
    let cozulen = 0, dogru = 0;
    for (const v of Object.values(ilerleme)) for (const s of Object.values(v)) { cozulen++; if (s === 'd') dogru++; }
    return { cozulen, dogru };
  }, [ilerleme]);

  const konuIlerleme = (k: KonuOzet) => {
    let t = 0, c = 0;
    for (const kz of k.kazanimlar) { t += kz.soru; c += Math.min(kz.soru, Object.keys(ilerleme[kz.id] || {}).length); }
    return { t, c };
  };

  if (hata) {
    return (
      <div className="scw">
        <div className="scw-empty" role="alert">
          <h1 className="scw-h1">Sınav Çalışması</h1>
          <p>Veri yüklenemedi. Bağlantını kontrol edip yeniden dene.</p>
          <button type="button" className="scw-btn is-pri" onClick={yukle}><RotateCcw aria-hidden />Yeniden dene</button>
        </div>
      </div>
    );
  }
  if (!dizin || !ders) {
    return (
      <div className="scw" aria-busy="true">
        <div className="scw-skel" aria-label="Yükleniyor"><i /><i /><i /><i /><i /></div>
      </div>
    );
  }

  const toplamPay = dizin.toplam.soru ? Math.min(100, Math.round((genel.cozulen / dizin.toplam.soru) * 100)) : 0;
  const dersSec = (i: number) => { setDersI(i); setKonu('hepsi'); setAcik(null); };

  return (
    <div className="scw">
      <header className="scw-head">
        <div className="scw-title">
          <h1 className="scw-h1">Sınav Çalışması</h1>
          <span className="scw-count"><b>{sayi(dizin.toplam.kazanim)}</b> kazanım · <b>{sayi(dizin.toplam.soru)}</b> soru</span>
        </div>
        <p className="scw-desc">Kurul {dizin.kurul} · her kazanım için kısa özet, örnek ve çıkmış sorular. Burada çöz ya da sesli çözücüyle dinle.</p>
        <div className="scw-prog" aria-label={`${sayi(genel.cozulen)} soru çözüldü`}>
          <span className="scw-bar" aria-hidden><i style={{ width: `${toplamPay}%` }} /></span>
          <span className="scw-prog-t">
            <b>{sayi(genel.cozulen)}</b> çözüldü
            {genel.cozulen > 0 && <> · <b>%{Math.round((genel.dogru / genel.cozulen) * 100)}</b> doğru</>}
          </span>
        </div>
      </header>

      <div className="scw-tool">
        <label className="scw-search">
          <Search aria-hidden />
          <input
            type="search"
            value={arama}
            onChange={(e) => setArama(e.target.value)}
            placeholder="Kazanım ya da konu ara"
            aria-label="Kazanım ya da konu ara"
            data-page-search
          />
          {arama && <button type="button" className="scw-clear" onClick={() => setArama('')} aria-label="Aramayı temizle"><X aria-hidden /></button>}
        </label>
        <div className="scw-seg is-ders" role="tablist" aria-label="Ders">
          {dersler.map((d, i) => (
            <button key={d.ad} type="button" role="tab" aria-selected={i === dersI} className={i === dersI ? 'is-on' : ''} onClick={() => dersSec(i)}>
              {d.ad.replace(/^Tıbbi /, '')}
              <span className="scw-n">{sayi(dersSayac[i] ?? 0)}</span>
            </button>
          ))}
        </div>
        <div className="scw-row">
          <div className="scw-chips" role="radiogroup" aria-label="Durum">
            {DURUMLAR.map((d) => (
              <button key={d.id} type="button" role="radio" aria-checked={durum === d.id} className={durum === d.id ? 'is-on' : ''} onClick={() => setDurum(d.id)}>{d.ad}</button>
            ))}
          </div>
          <label className="scw-konu-sec">
            <span className="scw-sr">Konu</span>
            <select value={konu} onChange={(e) => { setKonu(e.target.value); setAcik(null); }}>
              <option value="hepsi">Tüm konular ({ders.konular.length})</option>
              {ders.konular.map((k) => <option key={k.dosya} value={k.dosya}>{k.ad}</option>)}
            </select>
            <ChevronDown aria-hidden />
          </label>
        </div>
      </div>

      <div className="scw-body">
        <nav className="scw-side" aria-label="Konular">
          <button type="button" className={`scw-side-i${konu === 'hepsi' ? ' is-on' : ''}`} aria-current={konu === 'hepsi' || undefined} onClick={() => { setKonu('hepsi'); setAcik(null); }}>
            <span className="scw-side-t">Tüm konular</span>
            <span className="scw-n">{ders.konular.length}</span>
          </button>
          {ders.konular.map((k) => {
            const p = konuIlerleme(k);
            return (
              <button key={k.dosya} type="button" className={`scw-side-i${konu === k.dosya ? ' is-on' : ''}`} aria-current={konu === k.dosya || undefined} onClick={() => { setKonu(k.dosya); setAcik(null); }}>
                <span className="scw-side-t">{k.ad}</span>
                <span className="scw-n">{p.c > 0 ? `${p.c}/${p.t}` : k.kazanimlar.length}</span>
              </button>
            );
          })}
        </nav>

        <div className="scw-list">
          {konular.length === 0 ? (
            <div className="scw-empty">
              <p>{qk ? `“${q.trim()}” için bu derste kazanım yok.` : 'Bu süzgeçte kazanım yok.'}</p>
              <button type="button" className="scw-btn" onClick={() => { setArama(''); setDurum('hepsi'); setKonu('hepsi'); }}>Süzgeçleri temizle</button>
            </div>
          ) : konular.map((k) => {
            const p = konuIlerleme(ders.konular.find((x) => x.dosya === k.dosya) || k);
            return (
              <section key={k.dosya} className="scw-konu" aria-labelledby={`scw-k-${k.dosya}`}>
                <h2 className="scw-konu-h" id={`scw-k-${k.dosya}`}>
                  <span className="scw-konu-t">{k.ad}</span>
                  <span className="scw-m">{k.kazanimlar.length} kazanım{p.c > 0 && ` · ${p.c}/${p.t} soru`}</span>
                </h2>
                <ul className="scw-kzs">
                  {k.kazanimlar.map((kz) => (
                    <KazanimSatir
                      key={kz.id}
                      kz={kz}
                      konu={k}
                      ilerleme={ilerleme[kz.id]}
                      acik={acik === kz.id}
                      onToggle={() => setAcik((a) => (a === kz.id ? null : kz.id))}
                      onSonuc={sonucYaz}
                      onSifirla={kzSifirla}
                      onSesli={(sorular, anlatim) => setCozucu({ baslik: `${k.ad} · Kazanım ${kz.no}`, sorular, kzId: kz.id, anlatim })}
                    />
                  ))}
                </ul>
              </section>
            );
          })}
        </div>
      </div>

      {cozucu && (
        <SesliCozucu
          {...cozucu}
          onClose={() => setCozucu(null)}
          onSonuc={sonucYaz}
        />
      )}
    </div>
  );
};

/** Sesli çözücü köprüsü: sorular bir kez dönüştürülür (kimlik sabit kalsın), sonuçlar kazanım ilerlemesine yazılır */
const SesliCozucu: React.FC<{
  baslik: string; sorular: SSoru[]; kzId: string; anlatim?: string[];
  onClose: () => void; onSonuc: (kzId: string, soruId: string, s: 'd' | 'y') => void;
}> = ({ baslik, sorular, kzId, anlatim, onClose, onSonuc }) => {
  const cs = useMemo(() => cozucuSorulari(sorular), [sorular]);
  const yazilan = useRef<Record<string, CozucuSonuc>>({});
  const onOzelSonuc = useCallback((s: Record<string, CozucuSonuc>) => {
    for (const [no, v] of Object.entries(s)) {
      if (yazilan.current[no] === v) continue;
      yazilan.current[no] = v;
      const soru = sorular[Number(no) - 1];
      if (soru) onSonuc(kzId, soru.id, v === 'd' ? 'd' : 'y');
    }
  }, [sorular, kzId, onSonuc]);
  return <SoruCozucu kod="sinav_calisma" onClose={onClose} ozelSorular={cs} ozelBaslik={baslik} kisaAnlatim={anlatim} onOzelSonuc={onOzelSonuc} />;
};

/* ── Kazanım satırı + açılır çalışma paneli ─────────────────────────────── */
const KazanimSatir: React.FC<{
  kz: KzOzet;
  konu: KonuOzet;
  ilerleme?: Record<string, 'd' | 'y'>;
  acik: boolean;
  onToggle: () => void;
  onSonuc: (kzId: string, soruId: string, s: 'd' | 'y') => void;
  onSifirla: (kzId: string) => void;
  onSesli: (sorular: SSoru[], anlatim?: string[]) => void;
}> = ({ kz, konu, ilerleme, acik, onToggle, onSonuc, onSifirla, onSesli }) => {
  const panelId = useId();
  const cozulen = Math.min(kz.soru, Object.keys(ilerleme || {}).length);
  const dogru = Object.values(ilerleme || {}).filter((s) => s === 'd').length;
  const pay = kz.soru ? Math.round((cozulen / kz.soru) * 100) : 0;
  return (
    <li className={`scw-kz${acik ? ' is-open' : ''}`} id={`scw-kz-${kz.id}`}>
      <button type="button" className="scw-kz-b" aria-expanded={acik} aria-controls={panelId} onClick={onToggle}>
        <span className="scw-kz-no" aria-hidden>{kz.no}</span>
        <span className="scw-kz-main">
          <span className="scw-kz-t">{kz.metin}</span>
          <span className="scw-m">
            {kz.soru} soru{kz.cikmis > 0 && ` · ${kz.cikmis} çıkmış`}
            {cozulen > 0 && <> · <span className={dogru === cozulen ? 'is-ok' : ''}>{dogru}/{cozulen} doğru</span></>}
          </span>
        </span>
        <span className={`scw-ring${pay >= 100 ? ' is-done' : ''}`} style={{ '--p': pay } as React.CSSProperties} aria-label={`%${pay} çözüldü`}>
          {pay >= 100 ? <Check aria-hidden /> : null}
        </span>
        <ChevronDown className="scw-chev" aria-hidden />
      </button>
      {acik && (
        <div className="scw-panel" id={panelId}>
          <KazanimPanel kz={kz} konu={konu} ilerleme={ilerleme} onSonuc={onSonuc} onSifirla={onSifirla} onSesli={onSesli} />
        </div>
      )}
    </li>
  );
};

const KazanimPanel: React.FC<{
  kz: KzOzet;
  konu: KonuOzet;
  ilerleme?: Record<string, 'd' | 'y'>;
  onSonuc: (kzId: string, soruId: string, s: 'd' | 'y') => void;
  onSifirla: (kzId: string) => void;
  onSesli: (sorular: SSoru[], anlatim?: string[]) => void;
}> = ({ kz, konu, ilerleme, onSonuc, onSifirla, onSesli }) => {
  const [veri, setVeri] = useState<KzAyrinti | null>(null);
  const [hata, setHata] = useState(false);
  const [suzgec, setSuzgec] = useState<SoruSuzgec>('hepsi');
  const [i, setI] = useState(0);
  const [secim, setSecim] = useState<Record<string, Harf>>({});
  const [ipucu, setIpucu] = useState<Record<string, boolean>>({});
  const soruRef = useRef<HTMLDivElement>(null);

  const yukle = useCallback(() => {
    setHata(false);
    konuYukle(konu.dosya).then((m) => { const v = m.get(kz.id); if (v) setVeri(v); else setHata(true); }).catch(() => setHata(true));
  }, [konu.dosya, kz.id]);
  useEffect(yukle, [yukle]);

  const sorular = useMemo(() => {
    const t = veri?.sorular ?? [];
    if (suzgec === 'hepsi') return t;
    if (suzgec === 'cikmis') return t.filter((s) => s.tur === 'cikmis');
    return t.filter((s) => s.tur !== 'cikmis' && s.zorluk === suzgec);
  }, [veri, suzgec]);
  useEffect(() => { setI(0); }, [suzgec]);
  // İlk açılışta çözülmemiş ilk soruya git
  const ilkKonum = useRef(false);
  useEffect(() => {
    if (!veri || ilkKonum.current) return;
    ilkKonum.current = true;
    const j = veri.sorular.findIndex((s) => !ilerleme?.[s.id]);
    if (j > 0) setI(j);
  }, [veri, ilerleme]);

  if (hata) {
    return (
      <div className="scw-p-msg" role="alert">
        Sorular yüklenemedi. <button type="button" className="scw-link" onClick={yukle}>Yeniden dene</button>
      </div>
    );
  }
  if (!veri) return <div className="scw-p-msg" aria-busy="true">Sorular yükleniyor…</div>;

  const s = sorular[Math.min(i, sorular.length - 1)];
  const sec = s ? secim[s.id] : undefined;
  const onceki = s ? ilerleme?.[s.id] : undefined;
  const cevapla = (h: Harf) => {
    if (!s || sec) return;
    setSecim((p) => ({ ...p, [s.id]: h }));
    onSonuc(kz.id, s.id, h === s.dogru ? 'd' : 'y');
  };
  const git = (j: number) => {
    setI(Math.max(0, Math.min(sorular.length - 1, j)));
    soruRef.current?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  };
  const kopyala = () => {
    if (!s) return;
    const t = `${s.soru}\n${HARF.filter((h) => s.secenekler[h]).map((h) => `${h}) ${s.secenekler[h]}`).join('\n')}`;
    navigator.clipboard?.writeText(t).then(() => toast.success('Soru panoya kopyalandı')).catch(() => toast.error('Kopyalanamadı'));
  };
  const say = (f: SoruSuzgec) => (veri.sorular.filter((x) => (f === 'cikmis' ? x.tur === 'cikmis' : x.tur !== 'cikmis' && x.zorluk === f)).length);
  const suzgecler: { id: SoruSuzgec; ad: string; n: number }[] = [
    { id: 'hepsi' as SoruSuzgec, ad: 'Tümü', n: veri.sorular.length },
    ...(['kolay', 'orta', 'zor'] as Zorluk[]).map((z) => ({ id: z as SoruSuzgec, ad: ZORLUK_AD[z], n: say(z) })),
    { id: 'cikmis' as SoruSuzgec, ad: 'Çıkmış', n: say('cikmis') },
  ].filter((x) => x.id === 'hepsi' || x.n > 0);

  return (
    <>
      <div className="scw-p-acts">
        <button type="button" className="scw-btn is-pri" onClick={() => onSesli(sorular, veri.anlatim)} disabled={!sorular.length}>
          <Headphones aria-hidden />Sesli çöz
        </button>
        {veri.slaytlar?.[0] && (
          <button type="button" className="scw-btn" onClick={() => navigateTo(`/ogren/${veri.slaytlar![0].deck}?slide=${veri.slaytlar![0].sayfa}`)}>
            <Presentation aria-hidden />Derste aç
          </button>
        )}
        {ilerleme && Object.keys(ilerleme).length > 0 && (
          <button type="button" className="scw-btn is-ghost" onClick={() => { onSifirla(kz.id); setSecim({}); setI(0); }}>
            <RotateCcw aria-hidden />Sıfırla
          </button>
        )}
      </div>

      {veri.anlatim && veri.anlatim.length > 0 && (
        <details className="scw-ozet" open>
          <summary><BookOpen aria-hidden />Bilinmesi gerekenler</summary>
          <ul>{veri.anlatim.map((m, j) => <li key={j}>{m}</li>)}</ul>
          {veri.slaytlar && veri.slaytlar.length > 1 && (
            <div className="scw-slaytlar">
              {veri.slaytlar.map((sl) => (
                <button key={`${sl.deck}-${sl.sayfa}`} type="button" className="scw-tag" onClick={() => navigateTo(`/ogren/${sl.deck}?slide=${sl.sayfa}`)}>
                  s. {sl.sayfa}{sl.baslik ? ` · ${sl.baslik.replace(/\s*\([^)]*\)\s*$/, '')}` : ''}
                </button>
              ))}
            </div>
          )}
        </details>
      )}

      {suzgecler.length > 2 && (
        <div className="scw-chips is-sm" role="radiogroup" aria-label="Soru türü">
          {suzgecler.map((f) => (
            <button key={f.id} type="button" role="radio" aria-checked={suzgec === f.id} className={suzgec === f.id ? 'is-on' : ''} onClick={() => setSuzgec(f.id)}>
              {f.ad} <span className="scw-n">{f.n}</span>
            </button>
          ))}
        </div>
      )}

      {s ? (
        <div className="scw-q" ref={soruRef}>
          <nav className="scw-dots" aria-label="Sorular">
            {sorular.map((x, j) => {
              const r = ilerleme?.[x.id];
              return (
                <button
                  key={x.id}
                  type="button"
                  className={`${j === i ? 'is-cur' : ''}${r === 'd' ? ' is-ok' : r === 'y' ? ' is-bad' : ''}`}
                  aria-label={`Soru ${j + 1}${r === 'd' ? ', doğru' : r === 'y' ? ', yanlış' : ''}`}
                  aria-current={j === i || undefined}
                  onClick={() => git(j)}
                >{j + 1}</button>
              );
            })}
          </nav>

          <article className="scw-card" aria-labelledby={`scw-st-${s.id}`}>
            <div className="scw-card-h">
              <span className="scw-m">Soru {i + 1}/{sorular.length}</span>
              <span className={`scw-tag t-${s.tur === 'cikmis' ? 'cikmis' : s.zorluk}`}>{s.tur === 'cikmis' ? `Çıkmış${s.yil ? ` · ${s.yil}` : ''}` : ZORLUK_AD[s.zorluk]}</span>
              {onceki && !sec && <span className={`scw-m ${onceki === 'd' ? 'is-ok' : 'is-bad'}`}>Önceki deneme: {onceki === 'd' ? 'doğru' : 'yanlış'}</span>}
              <span className="scw-grow" />
              <button type="button" className="scw-ibtn" onClick={kopyala} aria-label="Soruyu kopyala" title="Soruyu kopyala"><Copy aria-hidden /></button>
            </div>
            <p className="scw-stem" id={`scw-st-${s.id}`}>{s.soru}</p>
            <div className="scw-opts" role="radiogroup" aria-labelledby={`scw-st-${s.id}`}>
              {HARF.filter((h) => s.secenekler[h]).map((h) => {
                const dogruMu = h === s.dogru;
                const cls = !sec ? '' : dogruMu ? ' is-ok' : h === sec ? ' is-bad' : ' is-dim';
                return (
                  <button key={h} type="button" role="radio" aria-checked={sec === h} aria-disabled={!!sec || undefined} className={`scw-opt${cls}`} onClick={() => cevapla(h)}>
                    <span className="k" aria-hidden>{h}</span>
                    <span className="t">{s.secenekler[h]}</span>
                    {sec && dogruMu && <Check className="r" aria-label="Doğru cevap" />}
                    {sec && h === sec && !dogruMu && <X className="r" aria-label="Senin cevabın, yanlış" />}
                  </button>
                );
              })}
            </div>

            {!sec && s.ipucu && (
              ipucu[s.id]
                ? <p className="scw-ipucu"><Lightbulb aria-hidden /><span>{s.ipucu}</span></p>
                : <button type="button" className="scw-link" onClick={() => setIpucu((p) => ({ ...p, [s.id]: true }))}><Lightbulb aria-hidden />İpucu</button>
            )}

            {sec && (
              <div className={`scw-cozum${sec === s.dogru ? ' is-ok' : ' is-bad'}`} aria-live="polite">
                <b>{sec === s.dogru ? 'Doğru' : `Yanlış · doğru cevap ${s.dogru}`}</b>
                {s.aciklama && <Metin metin={s.aciklama} />}
                {s.siklar && Object.keys(s.siklar).length > 0 && (
                  <details className="scw-siklar">
                    <summary>Seçeneklerin açıklaması</summary>
                    <ul>
                      {HARF.filter((h) => s.siklar?.[h]).map((h) => (
                        <li key={h} className={h === s.dogru ? 'is-ok' : ''}><b>{h}</b><span>{s.siklar![h]}</span></li>
                      ))}
                    </ul>
                  </details>
                )}
              </div>
            )}

            <div className="scw-card-f">
              <button type="button" className="scw-btn" onClick={() => git(i - 1)} disabled={i === 0} aria-label="Önceki soru"><ChevronLeft aria-hidden /><span className="scw-hide-xs">Önceki</span></button>
              {sec && <button type="button" className="scw-btn is-ghost" onClick={() => setSecim((p) => { const n = { ...p }; delete n[s.id]; return n; })}><RotateCcw aria-hidden />Yeniden çöz</button>}
              <span className="scw-grow" />
              <button type="button" className={`scw-btn${sec ? ' is-pri' : ''}`} onClick={() => git(i + 1)} disabled={i >= sorular.length - 1}>
                <span>Sonraki</span><ChevronRight aria-hidden />
              </button>
            </div>
          </article>
        </div>
      ) : (
        <div className="scw-p-msg">Bu türde soru yok.</div>
      )}
    </>
  );
};

export default SinavCalismaView;
