import React, { useEffect, useMemo, useState } from 'react';
import { ArrowLeftRight, ChevronLeft, ChevronRight, Headphones } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { fetchMyAccess } from '../../services/moderatorSession';
import { linkClick, navigateTo, pathFor } from '../../router';
import { KURULLAR, aktifKurul, bugun } from '../../services/kurulTakvimi';
import { useDersListesi } from './dersVeri';
import { useV15Baslik } from './baslik';
import '../../styles/v15/ogren.css';
import '../../styles/v15/dersler.css';
import '../../styles/v15/program.css';

/**
 * v15 · Ders programı (tasarım sistemi v15 › AA "Ders programı"). Yeni sayfa: /program ↔ /dersler/program.
 * Veri yalnız ders kayıt defterinden (src/data/dersler/kN.json: tarih, saat, branş, konu, öğretim üyesi; kaynak resmî ders
 * programı PDF'i). Görünümler: Gün (önceki/sonraki gün), Hafta (Pzt–Cum), Liste (kurulun bütün dersleri).
 * Sesli dersi yayında olan satır ders ayrıntısına götürür; olmayan yalnız bilgi satırıdır.
 */
interface ProgDers { id: string; brans: string; konu: string; ogretim_uyesi?: string; tarih: string; saat?: string; saat_sayisi?: number }
type Gorunum = 'gun' | 'hafta' | 'ay' | 'liste';

const KAYITLAR = import.meta.glob('../../data/dersler/k[1-6].json');
const tarih = (g: string) => new Date(`${g}T12:00:00`);
const iso = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const ekle = (g: string, n: number) => { const d = tarih(g); d.setDate(d.getDate() + n); return iso(d); };
const pazartesi = (g: string) => { const d = tarih(g); return ekle(g, -((d.getDay() + 6) % 7)); };
const gunYaz = (g: string, uzun = true) =>
  tarih(g).toLocaleDateString('tr-TR', uzun ? { weekday: 'long', day: 'numeric', month: 'long' } : { weekday: 'short', day: 'numeric' });
/** Kayıtta öğretim üyesi kimi yerde büyük harf: Türkçe kurallarıyla sözcük başı büyük */
const adYaz = (s = '') => s.toLocaleLowerCase('tr-TR').replace(/(^|[\s.(/-])(\p{L})/gu, (_, a: string, b: string) => a + b.toLocaleUpperCase('tr-TR'));
const saatBas = (s?: string) => s?.split('-')[0] || '';
/** Branş başına sabit renk tonu (palet vurgusu üstünde açı); renk sözcüğü değil, ayırt etmek için */
const ton = (b: string) => { let h = 0; for (const c of b) h = (h * 31 + c.charCodeAt(0)) % 360; return h; };

/** Saat çizelgesi: sabah ve öğleden sonra blokları; çok saatlik ders aynı blokta ardışık dilimleri doldurur */
const SABAH = ['08:00-08:40', '08:50-09:30', '09:40-10:20', '10:30-11:10', '11:20-12:00'];
const OGLE = ['13:00-13:40', '13:50-14:30', '14:40-15:20', '15:30-16:10'];

export default function DersProgramiV15() {
  const g = bugun();
  const [kurul, setKurul] = useState(() => aktifKurul(g).kurul);
  const kb = KURULLAR.find((k) => k.kurul === kurul) || aktifKurul(g);
  const [gorunum, setGorunum] = useState<Gorunum>(() => {
    try { return (localStorage.getItem('medsoru_v15_program_gorunum') as Gorunum) || 'gun'; } catch { return 'gun'; }
  });
  const ilkGun = g < kb.baslangic ? kb.baslangic : g > kb.bitis ? kb.baslangic : g;
  const [gun, setGun] = useState(ilkGun);
  const [veri, setVeri] = useState<ProgDers[] | null>(null);
  const { dersler: sesli } = useDersListesi();
  // Yer değiştirme: yalnız yönetici/moderatör (rol sunucudan; yazma ucu da sunucuda denetlenir)
  const [yetkili, setYetkili] = useState(false);
  const [duzenle, setDuzenle] = useState(false);
  const [secili, setSecili] = useState<string | null>(null);
  const [hata, setHata] = useState('');
  useEffect(() => {
    let c = true;
    void fetchMyAccess().then((a) => { if (c) setYetkili(!!a && a.role !== 'student' && !a.suspended); });
    return () => { c = false; };
  }, []);

  useEffect(() => {
    let c = true;
    setVeri(null);
    const yukle = KAYITLAR[`../../data/dersler/k${kurul}.json`];
    if (!yukle) { setVeri([]); return; }
    yukle().then(async (m) => {
      const d = ((m as { default?: { dersler: ProgDers[] } }).default ?? (m as { dersler: ProgDers[] })).dersler || [];
      let duzen: Record<string, { tarih: string; saat?: string }> = {};
      try { duzen = (await safeJsonFetch<{ duzen: typeof duzen }>(`/api/ders-programi/duzen?kurul=${kurul}`)).data?.duzen || {}; } catch { /* resmî program */ }
      if (c) setVeri(d.map((x) => (duzen[x.id] ? { ...x, ...duzen[x.id] } : x)).sort((a, b) => a.tarih.localeCompare(b.tarih) || saatBas(a.saat).localeCompare(saatBas(b.saat))));
    }, () => c && setVeri([]));
    return () => { c = false; };
  }, [kurul]);
  useEffect(() => { try { localStorage.setItem('medsoru_v15_program_gorunum', gorunum); } catch { /* yok */ } }, [gorunum]);

  /** ders kimliği (k2-07) → yayındaki sesli dersin anahtarı */
  const sesliKey = useMemo(() => {
    const m = new Map<string, string>();
    for (const d of sesli || []) { const x = /^(?:y\d+-)?(k\d+-\d+)/.exec(d.key); if (x && !m.has(x[1])) m.set(x[1], d.key); }
    return m;
  }, [sesli]);

  const gunluk = useMemo(() => {
    const m = new Map<string, ProgDers[]>();
    for (const d of veri || []) { const a = m.get(d.tarih) || []; a.push(d); m.set(d.tarih, a); }
    return m;
  }, [veri]);
  const gunler = useMemo(() => [...gunluk.keys()], [gunluk]);
  const pzt = pazartesi(gun);
  const hafta = [0, 1, 2, 3, 4].map((i) => ekle(pzt, i));

  const ozetAlt = veri ? `Kurul ${kurul} · ${veri.length} ders` : `Kurul ${kurul}`;
  useV15Baslik({ baslik: 'Ders programı', alt: ozetAlt });

  const kaydir = (n: number) => {
    if (gorunum === 'hafta') { setGun(ekle(gun, 7 * n)); return; }
    if (gorunum === 'ay') { const d = tarih(gun); d.setDate(1); d.setMonth(d.getMonth() + n); setGun(iso(d)); return; }
    // gün görünümünde dersi olmayan günleri (hafta sonu, tatil) atla
    const sonraki = n > 0 ? gunler.find((x) => x > gun) : [...gunler].reverse().find((x) => x < gun);
    if (sonraki) setGun(sonraki);
  };

  /** İki dersin tarih + saatini değiştirir; sunucuya yazılır, başarısızsa ekran eski haline döner */
  const degistir = async (a: ProgDers, b: ProgDers) => {
    const onceki = veri;
    const yeni = [{ id: a.id, tarih: b.tarih, saat: b.saat }, { id: b.id, tarih: a.tarih, saat: a.saat }];
    setVeri((v) => (v || []).map((x) => { const y = yeni.find((z) => z.id === x.id); return y ? { ...x, tarih: y.tarih, saat: y.saat } : x; })
      .sort((p, q) => p.tarih.localeCompare(q.tarih) || saatBas(p.saat).localeCompare(saatBas(q.saat))));
    const r = await safeJsonFetch(`/api/ders-programi/duzen`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ kurul: String(kurul), degisimler: yeni }) });
    if (!r.ok) { setVeri(onceki); setHata(r.error || 'Kaydedilemedi.'); } else setHata('');
  };
  /** Seçili dersin sığabildiği boş başlangıç saatleri (gün: ISO). Kendi şimdiki yeri boş sayılır. */
  const bosYerler = (h: string): string[] => {
    const sd = secili ? (veri || []).find((x) => x.id === secili) : undefined;
    if (!sd || tarih(h).getDay() % 6 === 0 || h < kb.baslangic || h > kb.bitis || h === kb.sinav) return [];
    const n = Math.max(1, sd.saat_sayisi || 1);
    const dolu = new Set<string>();
    for (const x of gunluk.get(h) || []) {
      if (x.id === sd.id || !x.saat) continue;
      const bas = saatBas(x.saat);
      for (const blok of [SABAH, OGLE]) {
        const i = blok.findIndex((t) => saatBas(t) === bas);
        if (i >= 0) for (let j = i; j < Math.min(blok.length, i + Math.max(1, x.saat_sayisi || 1)); j++) dolu.add(blok[j]);
      }
    }
    const sonuc: string[] = [];
    for (const blok of [SABAH, OGLE]) {
      // 08:00 dilimi yalnız o kurulun kayıtlarında geçiyorsa kullanılır
      const dilimler = blok.filter((t) => t !== SABAH[0] || (veri || []).some((x) => x.saat === t));
      for (let i = 0; i + n <= dilimler.length; i++) {
        if (dilimler.slice(i, i + n).every((t) => !dolu.has(t)) && !(h === sd.tarih && dilimler[i] === sd.saat)) sonuc.push(dilimler[i]);
      }
    }
    return sonuc;
  };
  /** Dersi boş bir yere taşır (tek kayıt) */
  const yerlestir = async (d: ProgDers, h: string, saat: string) => {
    const onceki = veri;
    setSecili(null);
    setVeri((v) => (v || []).map((x) => (x.id === d.id ? { ...x, tarih: h, saat } : x))
      .sort((p, q) => p.tarih.localeCompare(q.tarih) || saatBas(p.saat).localeCompare(saatBas(q.saat))));
    const r = await safeJsonFetch(`/api/ders-programi/duzen`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ kurul: String(kurul), degisimler: [{ id: d.id, tarih: h, saat }] }) });
    if (!r.ok) { setVeri(onceki); setHata(r.error || 'Kaydedilemedi.'); } else setHata('');
  };
  const bosSatiri = (h: string) => {
    if (!duzenle || !secili) return null;
    const sd = (veri || []).find((x) => x.id === secili);
    const b = bosYerler(h);
    if (!sd || !b.length) return null;
    return (
      <div className="pg15-bos" role="group" aria-label="Boş saatler">
        <span className="v15-cap">Boş saat:</span>
        {b.map((t) => <button key={t} type="button" className="pg15-bosbtn" onClick={() => void yerlestir(sd, h, t)}>{saatBas(t)}</button>)}
      </div>
    );
  };
  const sec = (d: ProgDers) => {
    if (!secili) { setSecili(d.id); return; }
    if (secili === d.id) { setSecili(null); return; }
    const a = (veri || []).find((x) => x.id === secili);
    setSecili(null);
    if (a) void degistir(a, d);
  };

  const satir = (d: ProgDers, tarihGoster = false) => {
    const key = sesliKey.get(d.id);
    const gecti = d.tarih < g;
    const ic = (
      <>
        <span className="pg15-s">{d.saat ? saatBas(d.saat) : '—'}{d.saat_sayisi && d.saat_sayisi > 1 ? <small>{d.saat_sayisi} saat</small> : null}</span>
        <span className="pg15-c" style={{ '--t': ton(d.brans) } as React.CSSProperties} aria-hidden />
        <span className="pg15-t">
          <b>{d.konu}</b>
          <small>{d.brans}{d.ogretim_uyesi ? ` · ${adYaz(d.ogretim_uyesi)}` : ''}{tarihGoster ? ` · ${gunYaz(d.tarih, false)}` : ''}</small>
        </span>
        {key && <Headphones className="pg15-i" aria-label="Sesli ders var" />}
      </>
    );
    const cls = `pg15-r${gecti ? ' is-gecti' : ''}${d.tarih === g ? ' is-bugun' : ''}${secili === d.id ? ' is-secili' : ''}`;
    return (
      <li key={d.id}>
        {duzenle ? (
          <button type="button" className={`${cls} pg15-duz`} aria-pressed={secili === d.id} onClick={() => sec(d)}>{ic}</button>
        ) : key ? (
          <a className={cls} href={pathFor('ders_detay', key)} onClick={linkClick(() => navigateTo(pathFor('ders_detay', key)))}>{ic}</a>
        ) : <div className={cls}>{ic}</div>}
      </li>
    );
  };

  const kurullar = KURULLAR.filter((k) => KAYITLAR[`../../data/dersler/k${k.kurul}.json`]);

  return (
    <div className="pg15">
      <h1 className="sr-only">Ders programı</h1>
      <div className="o15-cipler v15-hscroll" role="toolbar" aria-label="Kurul">
        {kurullar.map((k) => (
          <button key={k.kurul} type="button" className={`o15-cip${k.kurul === kurul ? ' is-on' : ''}`} aria-pressed={k.kurul === kurul}
            onClick={() => { setKurul(k.kurul); setGun(g >= k.baslangic && g <= k.bitis ? g : k.baslangic); }}>Kurul {k.kurul}</button>
        ))}
      </div>

      <div className="pg15-ust">
        <div className="pg15-seg" role="tablist" aria-label="Görünüm">
          {([['gun', 'Gün'], ['hafta', 'Hafta'], ['ay', 'Ay'], ['liste', 'Liste']] as const).map(([id, ad]) => (
            <button key={id} type="button" role="tab" aria-selected={gorunum === id} className={gorunum === id ? 'is-on' : ''} onClick={() => setGorunum(id)}>{ad}</button>
          ))}
        </div>
        {yetkili && (
          <button type="button" className={`pg15-duzbtn${duzenle ? ' is-on' : ''}`} aria-pressed={duzenle} onClick={() => { setDuzenle(!duzenle); setSecili(null); setHata(''); }}>
            <ArrowLeftRight /> {duzenle ? 'Düzenlemeyi bitir' : 'Yerleri değiştir'}
          </button>
        )}
        {gorunum !== 'liste' && (
          <div className="pg15-gez">
            <button type="button" className="pg15-ok" aria-label={gorunum === 'gun' ? 'Önceki ders günü' : gorunum === 'ay' ? 'Önceki ay' : 'Önceki hafta'} onClick={() => kaydir(-1)}><ChevronLeft /></button>
            <b>{gorunum === 'gun' ? gunYaz(gun) : gorunum === 'ay' ? tarih(gun).toLocaleDateString('tr-TR', { month: 'long', year: 'numeric' }) : `${tarih(hafta[0]).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })} – ${tarih(hafta[4]).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })}`}</b>
            <button type="button" className="pg15-ok" aria-label={gorunum === 'gun' ? 'Sonraki ders günü' : gorunum === 'ay' ? 'Sonraki ay' : 'Sonraki hafta'} onClick={() => kaydir(1)}><ChevronRight /></button>
            {gun !== g && g >= kb.baslangic && g <= kb.bitis && <button type="button" className="pg15-bugun" onClick={() => setGun(g)}>Bugün</button>}
          </div>
        )}
      </div>

      {duzenle && <p className="v15-cap pg15-duzbilgi" role="status">{secili ? 'Başka bir dersle yer değiştirmek için ikinci dersi seç ya da çizelgedeki boş saatlerden birine tıkla (Hafta görünümünde bütün günlerin boşları görünür).' : 'Taşımak istediğin dersi seç.'} Değişiklik bütün öğrencilerde görünür.</p>}
      {hata && <p className="v15-cap pg15-hata" role="alert">{hata}</p>}
      {!veri ? (
        <span className="v15-skel b15-skel" aria-hidden />
      ) : !veri.length ? (
        <p className="b15-bos v15-card">Kurul {kurul} için ders programı henüz yok.</p>
      ) : gorunum === 'gun' ? (
        (gunluk.get(gun) || []).length ? (
          <><ul className="pg15-l v15-card">{(gunluk.get(gun) || []).map((d) => satir(d))}</ul>{bosSatiri(gun)}</>
        ) : (
          <><p className="b15-bos v15-card">{gunYaz(gun)} ders yok.{gun === kb.sinav ? ' Bugün kurul sınavı.' : ''}</p>{bosSatiri(gun)}</>
        )
      ) : gorunum === 'hafta' ? (
        <div className="pg15-hafta">
          {hafta.map((h) => (
            <section key={h} className={`pg15-hg${h === g ? ' is-bugun' : ''}`}>
              <h2 className="v15-cap">{gunYaz(h, false)}{h === kb.sinav ? ' · Sınav' : ''}</h2>
              {(gunluk.get(h) || []).length ? <ul className="pg15-l v15-card">{(gunluk.get(h) || []).map((d) => satir(d))}</ul>
                : <p className="pg15-yok">Ders yok</p>}
              {bosSatiri(h)}
            </section>
          ))}
        </div>
      ) : gorunum === 'ay' ? (
        <AyIzgara acik={duzenle} baslangic={kb.baslangic} bitis={kb.bitis} gun={gun} bugun={g} sinav={kb.sinav} gunluk={gunluk} sec={(x) => { setGun(x); setGorunum('gun'); }} />
      ) : (
        <div className="pg15-hafta is-liste">
          {gunler.map((h) => (
            <section key={h} className={`pg15-hg${h === g ? ' is-bugun' : ''}`}>
              <h2 className="v15-cap">{gunYaz(h)}</h2>
              <ul className="pg15-l v15-card">{(gunluk.get(h) || []).map((d) => satir(d))}</ul>
              {bosSatiri(h)}
            </section>
          ))}
        </div>
      )}
      <p className="v15-cap pg15-ac">Kaynak: {kb.ad.toLocaleLowerCase('tr-TR').replace(/(^|\s)(\p{L})/gu, (_, a: string, b: string) => a + b.toLocaleUpperCase('tr-TR'))} resmî ders programı. Kulaklık simgeli derslerin sesli anlatımı hazır; dokununca açılır.</p>
    </div>
  );
}

/** Ay görünümü: pazartesiden başlayan 6×7 ızgara; her günde ders sayısı noktaları, dokununca o günün listesi */
function AyIzgara({ acik, baslangic, bitis, gun, bugun, sinav, gunluk, sec }: { acik: boolean; baslangic: string; bitis: string; gun: string; bugun: string; sinav: string; gunluk: Map<string, ProgDers[]>; sec: (g: string) => void }) {
  const ilk = tarih(gun); ilk.setDate(1);
  const ay = ilk.getMonth();
  const bas = pazartesi(iso(ilk));
  const gunler = Array.from({ length: 42 }, (_, i) => ekle(bas, i));
  const haftaSay = gunler.findIndex((x, i) => i % 7 === 0 && tarih(x).getMonth() !== ay && i > 7);
  const goster = haftaSay > 0 ? gunler.slice(0, haftaSay) : gunler;
  return (
    <div className="pg15-ay v15-card" role="grid" aria-label="Ay görünümü">
      {['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'].map((x) => <span key={x} className="pg15-ay-b" role="columnheader">{x}</span>)}
      {goster.map((x) => {
        const n = (gunluk.get(x) || []).length;
        const disarida = tarih(x).getMonth() !== ay;
        return (
          <button key={x} type="button" role="gridcell" disabled={!n && x !== sinav && !(acik && x >= baslangic && x <= bitis && tarih(x).getDay() % 6 !== 0)} onClick={() => sec(x)}
            className={`pg15-ay-g${disarida ? ' is-dis' : ''}${x === bugun ? ' is-bugun' : ''}${x === sinav ? ' is-sinav' : ''}`}
            aria-label={`${tarih(x).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' })}: ${x === sinav ? 'kurul sınavı' : n ? `${n} ders` : 'ders yok'}`}>
            <b>{tarih(x).getDate()}</b>
            {x === sinav ? <small>Sınav</small> : n ? <span className="pg15-ay-n">{Array.from({ length: Math.min(n, 4) }, (_, i) => <i key={i} />)}</span> : null}
          </button>
        );
      })}
    </div>
  );
}
