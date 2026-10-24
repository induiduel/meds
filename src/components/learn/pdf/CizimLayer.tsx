import { memo } from 'react';

/**
 * Canlı çizim katmanı (R6, ICERIK_MOTORU_V3.md §4): hoca konuşurken PDF üstünde kontur / akış oku / eğri fazı / şema.
 * Komutlar scripts/cizim/cizim_uret.py'den (kapı cizim_dogrula.py), sunucu cümle işaretine `z` olarak ekler. İlerleme
 * imleçle aynı sayaçtan: cümle içi konuşulan karakter `k[0]`→`k[1]` aralığında 0→1. Aralığa gelmeden çizim yok, geçince
 * tam kalır (cümle bitene dek). Koordinatlar sayfa oranı (0–1); SVG sayfayı kaplar, çizgi kalınlığı ölçekten bağımsız.
 */
export interface CizimKomut {
  tur: 'kontur' | 'akis' | 'egri_faz' | 'sema';
  s: number;
  k: [number, number];
  nokta?: number[][];
  a?: number[];
  b?: number[];
  iliski?: 'aktive' | 'inhibe' | 'donusur';
  fazlar?: { aralik: [number, number]; faz: 'yukselis' | 'inis' | 'plato' }[];
  dugum?: { id: string; metin: string }[];
  kenar?: { a: string; b: string; tur: string; etiket?: string }[];
  /** şema panel türü (cizim_uret.panel_tipi) */
  tip?: 'zincir' | 'grup' | 'dal' | 'maske' | 'karsit';
  /** şablonlu panel (scripts/cizim/sablon.py, sablonlar.json): düzen + alanlar */
  sablon?: string;
  sablon_ad?: string;
  duzen?: 'tablo' | 'zincir' | 'grup' | 'dal' | 'karsit' | 'maske' | 'liste' | 'adimlar';
  basliklar?: string[];
  bag?: string;
  satirlar?: string[][];
  ogeler?: string[];
  kaynaklar?: string[];
  sonuc?: string;
  soru?: string;
  dallar?: string[][];
  gorunen?: string;
  altta?: string[];
  kutuplar?: string[];
  baslik?: string;
  numarali?: boolean;
  /** tasarım sürümü (cizim_uret.SURUMLER): dizilim ve yazı ölçeği */
  yon?: 'yatay' | 'dikey';
  olcek?: number;
  etiket?: string;
  /** yerleşim (cizim_uret.yerlesim, içeriğin önü kapanmasın): ok kavisinin denetim noktası, asıl hedef, etiketin ve
   *  şema panelinin boş yerdeki konumu (sayfa oranı) */
  c?: number[];
  hedef?: number[];
  /** ok rotası (cizim_uret.ok_yerlesimi): düz / dirsek / kavis noktaları; hedef yazının kutusu */
  yol?: number[][];
  rota?: 'duz' | 'dirsek' | 'kavis';
  hedef_kutu?: number[];
  kaynak_kutu?: number[];
  /** resimdeki mevcut ok/bölge: yeni ok yerine çerçeve + etiket */
  odak?: number[];
  /** dallı ok: aynı kaynaktan çıkan dalların grubu, sırası, sayısı */
  dal?: { g: string; i: number; n: number };
  etiket_konum?: number[];
  etiket_genislik?: number;
  konum?: number[];
  genislik?: number;
}

const AZ_HAREKET = typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
const V = 1000;
const P = (n: number[]) => `${(n[0] * V).toFixed(1)} ${(n[1] * V).toFixed(1)}`;

/** Catmull-Rom → kübik Bezier (noktalardan geçen yumuşak eğri) */
function egri(nk: number[][], kapali = false): string {
  const p = nk.map((n) => [n[0] * V, n[1] * V]);
  if (p.length < 2) return '';
  const g = kapali ? [p[p.length - 1], ...p, p[0], p[1]] : [p[0], ...p, p[p.length - 1]];
  let d = `M${p[0][0].toFixed(1)} ${p[0][1].toFixed(1)}`;
  for (let i = 1; i < g.length - 2; i++) {
    const [p0, p1, p2, p3] = [g[i - 1], g[i], g[i + 1], g[i + 2]];
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += ` C${c1[0].toFixed(1)} ${c1[1].toFixed(1)}, ${c2[0].toFixed(1)} ${c2[1].toFixed(1)}, ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
  }
  return d;
}

const ilerleme = (z: CizimKomut, c: number) => (c < z.k[0] ? -1 : AZ_HAREKET ? 1 : Math.min(1, (c - z.k[0]) / Math.max(1, z.k[1] - z.k[0])));

/** Etiket yalnız betiğin boş bulduğu yerde (etiket_konum); yoksa gösterilmez — yazının üstüne binmesin */
function Etiket({ z }: { z: CizimKomut }) {
  if (!z.etiket || !z.etiket_konum) return null;
  return (
    <div className="pdv-cz-etiket-kap" style={{ left: `${z.etiket_konum[0] * 100}%`, top: `${z.etiket_konum[1] * 100}%`, maxWidth: `${(z.etiket_genislik || 0.3) * 100}%` }}>
      <span className="pdv-cz-etiket">{z.etiket}</span>
    </div>
  );
}

/** Yol → SVG: dirsekte köşe yuvarlatılır (yarıçap kısa kenarın en çok yarısı) */
function yolD(y: number[][], rota?: string): string {
  if (rota === 'dirsek' && y.length === 3) {
    const [a, k, b] = y;
    const r = Math.min(0.018, Math.hypot(k[0] - a[0], k[1] - a[1]) / 2, Math.hypot(b[0] - k[0], b[1] - k[1]) / 2);
    const yon = (u: number[], v: number[]) => { const L = Math.hypot(v[0] - u[0], v[1] - u[1]) || 1; return [(v[0] - u[0]) / L, (v[1] - u[1]) / L]; };
    const d1 = yon(a, k), d2 = yon(k, b);
    return `M${P(a)} L${P([k[0] - d1[0] * r, k[1] - d1[1] * r])} Q${P(k)} ${P([k[0] + d2[0] * r, k[1] + d2[1] * r])} L${P(b)}`;
  }
  return `M${P(y[0])}` + y.slice(1).map((q) => ` L${P(q)}`).join('');
}

/** Yol boyunca u (0–1) oranındaki nokta (hareketli parçacık) */
function yolNokta(y: number[][], u: number): number[] {
  const seg = y.slice(1).map((q, i) => Math.hypot(q[0] - y[i][0], q[1] - y[i][1]));
  let kalan = u * seg.reduce((a, b) => a + b, 0);
  for (let i = 0; i < seg.length; i++) {
    if (kalan <= seg[i] || i === seg.length - 1) {
      const f = seg[i] ? Math.min(1, kalan / seg[i]) : 0;
      return [y[i][0] + (y[i + 1][0] - y[i][0]) * f, y[i][1] + (y[i + 1][1] - y[i][1]) * f];
    }
    kalan -= seg[i];
  }
  return y[y.length - 1];
}

function Komut({ z, t }: { z: CizimKomut; t: number }) {
  const ciz = { pathLength: 1, strokeDasharray: 1, strokeDashoffset: 1 - t } as const;
  if (z.tur === 'kontur' && z.nokta) {
    return (
      <g className="pdv-cz-kontur">
        {t > 0 && <path d={egri(z.nokta, true)} className="pdv-cz-boya" style={{ opacity: Math.min(1, t * 1.5) }} />}
        <path d={egri(z.nokta, true)} {...ciz} className="pdv-cz-hale" vectorEffect="non-scaling-stroke" />
        <path d={egri(z.nokta, true)} {...ciz} vectorEffect="non-scaling-stroke" />
      </g>
    );
  }
  if (z.tur === 'akis' && z.odak) {
    const o = z.odak;
    return (
      <g className="pdv-cz-akis is-odak">
        <rect x={o[0] * V} y={o[1] * V} width={(o[2] - o[0]) * V} height={(o[3] - o[1]) * V} rx={8} className="pdv-cz-hale" pathLength={1}
              strokeDasharray={1} strokeDashoffset={1 - t} vectorEffect="non-scaling-stroke" />
        <rect x={o[0] * V} y={o[1] * V} width={(o[2] - o[0]) * V} height={(o[3] - o[1]) * V} rx={8} className="pdv-cz-odak" pathLength={1}
              strokeDasharray={1} strokeDashoffset={1 - t} vectorEffect="non-scaling-stroke" />
      </g>
    );
  }
  if (z.tur === 'akis' && z.a && z.b) {
    const [a, b] = [z.a, z.b];
    const yol = z.yol?.length ? z.yol : z.c ? Array.from({ length: 17 }, (_, i) => {
      const u = i / 16, c = z.c!;
      return [(1 - u) ** 2 * a[0] + 2 * (1 - u) * u * c[0] + u * u * b[0], (1 - u) ** 2 * a[1] + 2 * (1 - u) * u * c[1] + u * u * b[1]];
    }) : [a, b];
    const m = yolNokta(yol, t);
    const ui = z.iliski === 'inhibe';
    const hk = z.hedef_kutu;
    const kk = z.kaynak_kutu;
    return (
      <g className={`pdv-cz-akis is-${z.iliski || 'aktive'}${z.dal ? ' is-dal' : ''}`}>
        {(!z.dal || z.dal.i === 0) && (kk ? (
          <rect x={kk[0] * V} y={kk[1] * V} width={(kk[2] - kk[0]) * V} height={(kk[3] - kk[1]) * V} rx={6} className="pdv-cz-kaynak" vectorEffect="non-scaling-stroke" />
        ) : (
          <circle cx={yol[0][0] * V} cy={yol[0][1] * V} r={6} className="pdv-cz-baslangic" />
        ))}
        <path d={yolD(yol, z.rota)} {...ciz} className="pdv-cz-hale" vectorEffect="non-scaling-stroke" />
        <path d={yolD(yol, z.rota)} {...ciz} markerEnd={t >= 1 ? `url(#pdv-cz-${ui ? 'dur' : 'ok'})` : undefined} vectorEffect="non-scaling-stroke" />
        {t > 0 && t < 1 && <circle cx={m[0] * V} cy={m[1] * V} r={4} className="pdv-cz-parca" />}
        {t >= 1 && hk && (
          <rect x={hk[0] * V} y={hk[1] * V} width={(hk[2] - hk[0]) * V} height={(hk[3] - hk[1]) * V} rx={6} className="pdv-cz-hedef" vectorEffect="non-scaling-stroke" />
        )}
      </g>
    );
  }
  if (z.tur === 'egri_faz' && z.nokta) {
    const n = z.nokta.length;
    const ulasilan = Math.max(1, Math.round(t * (n - 1)));
    const fazOf = (i: number) => z.fazlar?.find((f) => i >= f.aralik[0] && i < f.aralik[1])?.faz || 'plato';
    return (
      <g className="pdv-cz-egri">
        {z.nokta.slice(0, ulasilan).map((p, i) => (
          <path key={i} className={`is-${fazOf(i)}`} d={`M${P(p)} L${P(z.nokta![i + 1])}`} vectorEffect="non-scaling-stroke" />
        ))}
        <circle cx={z.nokta[ulasilan][0] * V} cy={z.nokta[ulasilan][1] * V} r={4} className="pdv-cz-parca" />
      </g>
    );
  }
  return null;
}

const OK = (tur?: string) => (tur === 'inhibe' ? '⊣' : tur === 'donusur' ? '⇒' : tur === 'karsit' ? '↔' : '→');
type Dugum = { id: string; metin: string };

/** Düğüm: belirince süzülür; vurgulu (hedef) mavi dolgu */
const D = ({ d, hedef, gecikme = 0 }: { d: Dugum; hedef?: boolean; gecikme?: number }) => (
  <span className={`pdv-cz-dugum${hedef ? ' is-hedef' : ''}`} style={{ animationDelay: `${gecikme}ms` }}>{d.metin}</span>
);

/** Bağ: çizgi soldan uzayarak çizilir, ucunda ilişki işareti; varsa üstünde kısa açıklama */
const Bag = ({ tur, etiket, dikey, gecikme = 0 }: { tur?: string; etiket?: string; dikey?: boolean; gecikme?: number }) => (
  <span className={`pdv-cz-bag is-${tur || 'aktive'}${dikey ? ' is-dikey' : ''}${etiket ? ' has-etiket' : ''}`} style={{ ['--g' as any]: `${gecikme}ms` }}>
    {etiket && <span className="pdv-cz-bag-etiket">{etiket}</span>}
    <span className="pdv-cz-bag-ok">
      <span className="pdv-cz-bag-cizgi" />
      <span className="pdv-cz-bag-uc">{tur === 'inhibe' ? '⊣' : '▶'}</span>
    </span>
  </span>
);

/**
 * Şema paneli (R6; kullanıcı 2026-10-24): sayfadaki yazılar arasına ok çizmek okunmadığında ilişki betiğin boş bulduğu
 * yerde (konum) bir panelde canlandırılır. Tür ilişki yapısından seçilir (cizim_uret.panel_tipi):
 *  zincir A → B → C · grup (çok → bir, "}") · dal (bir → çok, karar) · maske (görünen neden, perde kalkınca altta
 *  yatan) · karşıt (iki kutup yan yana). Düğümler konuşmayla (t) sırayla belirir.
 */
function SemaParca({ z, t, ic }: { z: CizimKomut; t: number; ic?: boolean }) {
  const dg = z.dugum || [];
  const kn = z.kenar || [];
  const gorunen = Math.max(1, Math.ceil(t * dg.length));
  const sira = new Map(dg.map((d, i) => [d.id, i]));
  const bul = (id: string) => dg.find((d) => d.id === id);
  const gor = (id: string) => (sira.get(id) ?? 99) < gorunen;
  const stil = z.konum ? { left: `${z.konum[0] * 100}%`, top: `${z.konum[1] * 100}%`, right: 'auto', bottom: 'auto', maxWidth: `${(z.genislik || 0.6) * 100}%` } : undefined;
  const say = (k: 'a' | 'b') => { const m = new Map<string, typeof kn>(); for (const e of kn) m.set(e[k], [...(m.get(e[k]) || []), e]); return m; };
  const tip = ic ? tipBul(kn) : z.tip || tipBul(kn);
  const kap = (icerik: React.ReactNode) => ic ? <div className={`pdv-cz-sema-parca is-${tip}`}>{icerik}</div> : (
    <div className={`pdv-cz-sema is-${tip}${surumSinif(z)}`} role="img" aria-label={dg.map((d) => d.metin).join(', ')} style={stil}>{icerik}</div>
  );

  if (tip === 'maske' && kn[0]) {
    const e = kn[0]; const ust = bul(e.a); const alt = kn.filter((x) => x.a === e.a).map((x) => bul(x.b)).filter(Boolean) as Dugum[];
    const acik = t >= 0.5;
    return kap(
      <div className="pdv-cz-maske">
        <span className="pdv-cz-maske-baslik">Görünen</span>
        {ust && <D d={ust} />}
        <span className="pdv-cz-maske-baslik">Altta aranacak</span>
        <div className={`pdv-cz-maske-alt${acik ? ' is-acik' : ''}`}>
          {alt.map((d, i) => <D key={d.id} d={d} hedef gecikme={i * 120} />)}
          <span className="pdv-cz-perde" aria-hidden>{e.etiket || '?'}</span>
        </div>
      </div>,
    );
  }
  if (tip === 'karsit' && kn[0]) {
    const a = bul(kn[0].a), b = bul(kn[0].b);
    return kap(
      <div className="pdv-cz-karsit">
        {a && <D d={a} />}
        <span className="pdv-cz-karsit-vs">{kn[0].etiket || 'ayırt et'}</span>
        {b && gor(b.id) && <D d={b} />}
      </div>,
    );
  }
  if (tip === 'grup' || tip === 'dal') {
    const harita = say(tip === 'grup' ? 'b' : 'a');
    const [mid, es] = [...harita.entries()].sort((x, y) => y[1].length - x[1].length)[0] || ['', []];
    const merkez = bul(mid);
    const uclar = es.map((e) => bul(tip === 'grup' ? e.a : e.b)).filter(Boolean) as Dugum[];
    const goren = uclar.filter((d) => gor(d.id));
    const tamam = goren.length === uclar.length;
    const liste = (
      <div className="pdv-cz-grup-kaynak">
        {goren.map((d, i) => (
          <span key={d.id} className="pdv-cz-dal-satir">
            {tip === 'dal' && es[i]?.etiket && <span className="pdv-cz-dal-kosul">{es[i].etiket}</span>}
            <D d={d} gecikme={i * 90} />
          </span>
        ))}
      </div>
    );
    return kap(
      <div className="pdv-cz-grup">
        {tip === 'grup' ? (
          <>{liste}{tamam && <span className="pdv-cz-kume" aria-hidden />}{tamam && merkez && <><Bag tur={es[0]?.tur} etiket={es[0]?.etiket} /><D d={merkez} hedef /></>}</>
        ) : (
          <>{merkez && <D d={merkez} />}<span className="pdv-cz-kume is-ters" aria-hidden />{liste}</>
        )}
      </div>,
    );
  }
  return kap(
    <div className="pdv-cz-zincir">
      {dg.slice(0, gorunen).map((d, i) => {
        const g = kn.find((e) => sira.get(e.b) === i && (sira.get(e.a) ?? 99) < i);
        return (
          <span key={d.id} className="pdv-cz-dugum-kap">
            {g && <Bag tur={g.tur} etiket={g.etiket} />}
            <D d={d} hedef={i === dg.length - 1 && dg.length > 1} />
          </span>
        );
      })}
    </div>,
  );
}

/** sürüm sınıfı ve yazı ölçeği: dikey (alt alta, oklar aşağı) ve kompakt (olcek < 1) */
const surumSinif = (z: CizimKomut) => ((z.yon === 'dikey' || (z.genislik || 1) < 0.32) ? ' is-dar' : '') + (z.olcek && z.olcek < 1 ? ' is-kompakt' : '');

/**
 * Şablonlu panel (kullanıcı 2026-10-24): anlam şablonunun düzeni genel çizilir; yeni şablon için kod değişmez.
 * Kurallar (docs/CIZIM_KURALLARI.md §2b): ilişki yönü olmayan eşleşmeler (durum → tetkik, zehir → antidot, bulgu → tanı)
 * ok değil başlıklı tablodur; satırlar/sütunlar kesikli çizgiyle ayrılır (karışmasın); aynı gruptaki sıralı öğeler
 * numaralı, ayrı şeyler madde imli; konuşmayla satır satır belirir.
 */
function SablonPanel({ z, t }: { z: CizimKomut; t: number }) {
  const stil = z.konum ? { left: `${z.konum[0] * 100}%`, top: `${z.konum[1] * 100}%`, right: 'auto', bottom: 'auto', maxWidth: `${(z.genislik || 0.6) * 100}%` } : undefined;
  const say = (n: number) => Math.max(1, Math.ceil(t * n));
  const sinif = `pdv-cz-sema pdv-sb is-${z.duzen}${surumSinif(z)}`;
  const kap = (ic: React.ReactNode) => (
    <div className={sinif} style={stil} role="img" aria-label={[z.baslik, ...(z.basliklar || [])].filter(Boolean).join(', ')}>
      {z.baslik && z.duzen !== 'liste' && <div className="pdv-sb-baslik">{z.baslik}</div>}
      {ic}
    </div>
  );
  const ok = (dikey?: boolean) => (
    <span className={`pdv-sb-ok${dikey ? ' is-dikey' : ''}`} aria-hidden>
      {z.bag && <span className="pdv-sb-bag">{z.bag}</span>}
      <span className="pdv-sb-ok-cizgi" />
    </span>
  );
  switch (z.duzen) {
    case 'tablo':
    case 'karsit': {
      const bas = z.duzen === 'karsit' ? [z.basliklar?.[0] || 'Özellik', ...(z.kutuplar || [])] : z.basliklar || [];
      const sat = z.satirlar || [];
      return kap(
        <table className="pdv-sb-tablo">
          {bas.length > 0 && <thead><tr>{bas.map((b, i) => <th key={i}>{b}</th>)}</tr></thead>}
          <tbody>{sat.slice(0, say(sat.length)).map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j} className={j === r.length - 1 && z.duzen === 'tablo' ? 'is-sonuc' : ''}>{c}</td>)}</tr>)}</tbody>
        </table>,
      );
    }
    case 'liste':
    case 'adimlar': {
      const og = z.ogeler || [];
      const Liste = (z.duzen === 'adimlar' || z.numarali ? 'ol' : 'ul') as 'ol';
      return kap(
        <>
          {z.duzen === 'liste' && z.baslik && <div className="pdv-sb-baslik">{z.baslik}</div>}
          <Liste className="pdv-sb-liste">{og.slice(0, say(og.length)).map((x, i) => <li key={i}>{x}</li>)}</Liste>
        </>,
      );
    }
    case 'zincir': {
      const og = z.ogeler || [];
      const dikey = z.yon === 'dikey' || (z.genislik || 1) < 0.32;
      return kap(
        <div className={`pdv-sb-zincir${dikey ? ' is-dikey' : ''}`}>
          {og.slice(0, say(og.length)).map((x, i) => (
            <span key={i} className="pdv-sb-zincir-oge">{i > 0 && ok(dikey)}<span className={`pdv-sb-kutu${i === og.length - 1 ? ' is-sonuc' : ''}`}>{x}</span></span>
          ))}
        </div>,
      );
    }
    case 'grup': {
      const kn = z.kaynaklar || [];
      const n = say(kn.length + 1);
      return kap(
        <div className="pdv-sb-grup">
          <ol className="pdv-sb-liste is-kaynak">{kn.slice(0, Math.min(n, kn.length)).map((x, i) => <li key={i}>{x}</li>)}</ol>
          {n > kn.length && <>
            <span className="pdv-cz-kume" aria-hidden />{ok()}<span className="pdv-sb-kutu is-sonuc">{z.sonuc}</span>
          </>}
        </div>,
      );
    }
    case 'dal': {
      const dl = z.dallar || [];
      return kap(
        <div className="pdv-sb-dal">
          <span className="pdv-sb-kutu">{z.soru}</span>
          <div className="pdv-sb-dallar">
            {dl.slice(0, say(dl.length)).map((d, i) => (
              <div key={i} className="pdv-sb-dal-satir"><span className="pdv-sb-kosul">{d[0]}</span><span className="pdv-sb-ok-kisa" aria-hidden>→</span><span className="pdv-sb-kutu is-sonuc">{d[1]}</span></div>
            ))}
          </div>
        </div>,
      );
    }
    case 'maske': {
      const acik = t >= 0.5;
      return kap(
        <div className="pdv-cz-maske">
          <span className="pdv-cz-maske-baslik">Görünen</span>
          <span className="pdv-sb-kutu">{z.gorunen}</span>
          <span className="pdv-cz-maske-baslik">Altta aranacak</span>
          <div className={`pdv-cz-maske-alt${acik ? ' is-acik' : ''}`}>
            {(z.altta || []).map((x, i) => <span key={i} className="pdv-sb-kutu is-sonuc">{x}</span>)}
            <span className="pdv-cz-perde" aria-hidden>{z.bag || '?'}</span>
          </div>
        </div>,
      );
    }
    default:
      return null;
  }
}

/** panel türü (cizim_uret.panel_tipi ile aynı kural) */
function tipBul(kn: NonNullable<CizimKomut['kenar']>): NonNullable<CizimKomut['tip']> {
  if (kn.some((e) => e.tur === 'karsit')) return 'karsit';
  if (kn.some((e) => e.tur === 'maske')) return 'maske';
  const gir = new Map<string, number>(), cik = new Map<string, number>();
  for (const e of kn) { gir.set(e.b, (gir.get(e.b) || 0) + 1); cik.set(e.a, (cik.get(e.a) || 0) + 1); }
  if ([...gir.values()].some((n) => n >= 2)) return 'grup';
  if ([...cik.values()].some((n) => n >= 2)) return 'dal';
  return 'zincir';
}

/**
 * Şema: birbirine bağlı olmayan ilişkiler ayrı satırlara bölünür (kullanıcı 2026-10-24 s.43: "uzamış kanama zamanı →
 * intrakraniyal kanama" ile "trombositopeni → kanama, sepsis" yan yana dizilince tek zincir gibi okunuyordu). Her bağlı
 * bileşen kendi türüyle (zincir / grup / dal / maske / karşıt) çizilir, aralarında ince ayraç.
 */
function Sema({ z, t }: { z: CizimKomut; t: number }) {
  const dg = z.dugum || [], kn = z.kenar || [];
  const kok = new Map(dg.map((d) => [d.id, d.id]));
  const bul = (x: string): string => (kok.get(x) === x ? x : bul(kok.get(x)!));
  for (const e of kn) if (kok.has(e.a) && kok.has(e.b)) kok.set(bul(e.a), bul(e.b));
  const gruplar = new Map<string, string[]>();
  for (const d of dg) gruplar.set(bul(d.id), [...(gruplar.get(bul(d.id)) || []), d.id]);
  if (gruplar.size <= 1) return <SemaParca z={z} t={t} />;
  const gorunen = new Set(dg.slice(0, Math.max(1, Math.ceil(t * dg.length))).map((d) => d.id));
  const stil = z.konum ? { left: `${z.konum[0] * 100}%`, top: `${z.konum[1] * 100}%`, right: 'auto', bottom: 'auto', maxWidth: `${(z.genislik || 0.6) * 100}%` } : undefined;
  // Her parça tek "A → B" ise hizalı tablo: kaynak | ok | hedef sütunları (kullanıcı 2026-10-24: satırlar farklı kırılıp
  // biri tek satır, öteki iki satır görünüyordu)
  const parcalar = [...gruplar.values()];
  if (parcalar.every((ids) => ids.length === 2 && kn.filter((e) => ids.includes(e.a)).length === 1)) {
    return (
      <div className={`pdv-cz-sema is-tablo${surumSinif(z).replace(' is-dar', '')}`} role="img" aria-label={dg.map((d) => d.metin).join(', ')} style={stil}>
        {parcalar.map((ids, i) => {
          const e = kn.find((x) => ids.includes(x.a))!;
          const a = dg.find((d) => d.id === e.a), b = dg.find((d) => d.id === e.b);
          if (!a || !gorunen.has(a.id)) return null;
          return (
            <div key={i} className="pdv-cz-tablo-satir">
              <D d={a} />
              {b && gorunen.has(b.id) ? <><Bag tur={e.tur} etiket={e.etiket} /><D d={b} hedef /></> : <><span /><span /></>}
            </div>
          );
        })}
      </div>
    );
  }
  return (
    <div className={`pdv-cz-sema is-coklu${surumSinif(z)}`} role="img" aria-label={dg.map((d) => d.metin).join(', ')} style={stil}>
      {[...gruplar.values()].map((ids, i) => {
        const g = ids.filter((x) => gorunen.has(x)).length;
        if (!g) return null;
        const sub = { ...z, konum: undefined, dugum: dg.filter((d) => ids.includes(d.id)), kenar: kn.filter((e) => ids.includes(e.a)) };
        return <SemaParca key={i} z={sub} t={g / ids.length} ic />;
      })}
    </div>
  );
}

export const CizimLayer = memo(function CizimLayer({ z, useChar }: { z: CizimKomut[]; useChar: () => number }) {
  const c = useChar();
  const cizimler = z.filter((x) => x.tur !== 'sema');
  // şema yalnız betiğin boş bulduğu yerde (konum); boş yer yoksa (konum null) sayfanın önü kapanmasın diye gösterilmez
  const sema = z.find((x) => x.tur === 'sema' && (x.konum || x.konum === undefined));
  return (
    <>
      {cizimler.length > 0 && (
        <svg className="pdv-cz" viewBox={`0 0 ${V} ${V}`} preserveAspectRatio="none" aria-hidden>
          <defs>
            <marker id="pdv-cz-ok" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto-start-reverse">
              <path d="M0 0 L10 5 L0 10 z" className="pdv-cz-uc" />
            </marker>
            <marker id="pdv-cz-dur" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto">
              <path d="M5 0 L5 10" className="pdv-cz-uc-dur" />
            </marker>
          </defs>
          {cizimler.map((x, i) => {
            // dallı okta dallar konuşma aralığını paylaşır: i. dal kendi diliminde çizilir (kaynak → 1. hedef → 2. hedef …)
            const t0 = ilerleme(x, c);
            const t = x.dal && t0 >= 0 && x.dal.i > 0 ? (t0 * x.dal.n - x.dal.i < 0 ? -1 : Math.min(1, t0 * x.dal.n - x.dal.i)) : x.dal && t0 > 0 ? Math.min(1, t0 * x.dal.n) : t0;
            return t < 0 ? null : <Komut key={i} z={x} t={t} />;
          })}
        </svg>
      )}
      {/* etiketler HTML katmanında: SVG oransız ölçeklendiği için yazı orada bozulurdu; boyut sayfa genişliğiyle orantılı */}
      {cizimler.map((x, i) => (x.etiket && ilerleme(x, c) >= 1 ? <Etiket key={`e${i}`} z={x} /> : null))}
      {sema && ilerleme(sema, c) >= 0 && (sema.duzen ? <SablonPanel z={sema} t={ilerleme(sema, c)} /> : <Sema z={sema} t={ilerleme(sema, c)} />)}
    </>
  );
});
