import React, { useEffect, useMemo, useState } from 'react';
import { ChevronLeft, ChevronRight, Headphones } from 'lucide-react';
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
type Gorunum = 'gun' | 'hafta' | 'liste';

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

  useEffect(() => {
    let c = true;
    setVeri(null);
    const yukle = KAYITLAR[`../../data/dersler/k${kurul}.json`];
    if (!yukle) { setVeri([]); return; }
    yukle().then((m) => {
      const d = ((m as { default?: { dersler: ProgDers[] } }).default ?? (m as { dersler: ProgDers[] })).dersler || [];
      if (c) setVeri([...d].sort((a, b) => a.tarih.localeCompare(b.tarih) || saatBas(a.saat).localeCompare(saatBas(b.saat))));
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
    // gün görünümünde dersi olmayan günleri (hafta sonu, tatil) atla
    const sonraki = n > 0 ? gunler.find((x) => x > gun) : [...gunler].reverse().find((x) => x < gun);
    if (sonraki) setGun(sonraki);
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
    const cls = `pg15-r${gecti ? ' is-gecti' : ''}${d.tarih === g ? ' is-bugun' : ''}`;
    return (
      <li key={d.id}>
        {key ? (
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
          {([['gun', 'Gün'], ['hafta', 'Hafta'], ['liste', 'Liste']] as const).map(([id, ad]) => (
            <button key={id} type="button" role="tab" aria-selected={gorunum === id} className={gorunum === id ? 'is-on' : ''} onClick={() => setGorunum(id)}>{ad}</button>
          ))}
        </div>
        {gorunum !== 'liste' && (
          <div className="pg15-gez">
            <button type="button" className="pg15-ok" aria-label={gorunum === 'gun' ? 'Önceki ders günü' : 'Önceki hafta'} onClick={() => kaydir(-1)}><ChevronLeft /></button>
            <b>{gorunum === 'gun' ? gunYaz(gun) : `${tarih(hafta[0]).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })} – ${tarih(hafta[4]).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })}`}</b>
            <button type="button" className="pg15-ok" aria-label={gorunum === 'gun' ? 'Sonraki ders günü' : 'Sonraki hafta'} onClick={() => kaydir(1)}><ChevronRight /></button>
            {gun !== g && g >= kb.baslangic && g <= kb.bitis && <button type="button" className="pg15-bugun" onClick={() => setGun(g)}>Bugün</button>}
          </div>
        )}
      </div>

      {!veri ? (
        <span className="v15-skel b15-skel" aria-hidden />
      ) : !veri.length ? (
        <p className="b15-bos v15-card">Kurul {kurul} için ders programı henüz yok.</p>
      ) : gorunum === 'gun' ? (
        (gunluk.get(gun) || []).length ? (
          <ul className="pg15-l v15-card">{(gunluk.get(gun) || []).map((d) => satir(d))}</ul>
        ) : (
          <p className="b15-bos v15-card">{gunYaz(gun)} ders yok.{gun === kb.sinav ? ' Bugün kurul sınavı.' : ''}</p>
        )
      ) : gorunum === 'hafta' ? (
        <div className="pg15-hafta">
          {hafta.map((h) => (
            <section key={h} className={`pg15-hg${h === g ? ' is-bugun' : ''}`}>
              <h2 className="v15-cap">{gunYaz(h, false)}{h === kb.sinav ? ' · Sınav' : ''}</h2>
              {(gunluk.get(h) || []).length ? <ul className="pg15-l v15-card">{(gunluk.get(h) || []).map((d) => satir(d))}</ul>
                : <p className="pg15-yok">Ders yok</p>}
            </section>
          ))}
        </div>
      ) : (
        <div className="pg15-hafta is-liste">
          {gunler.map((h) => (
            <section key={h} className={`pg15-hg${h === g ? ' is-bugun' : ''}`}>
              <h2 className="v15-cap">{gunYaz(h)}</h2>
              <ul className="pg15-l v15-card">{(gunluk.get(h) || []).map((d) => satir(d))}</ul>
            </section>
          ))}
        </div>
      )}
      <p className="v15-cap pg15-ac">Kaynak: {kb.ad.toLocaleLowerCase('tr-TR').replace(/(^|\s)(\p{L})/gu, (_, a: string, b: string) => a + b.toLocaleUpperCase('tr-TR'))} resmî ders programı. Kulaklık simgeli derslerin sesli anlatımı hazır; dokununca açılır.</p>
    </div>
  );
}
