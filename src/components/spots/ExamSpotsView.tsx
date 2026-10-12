import React, { useEffect, useMemo, useState } from 'react';
import { AlertTriangle, BookMarked, Check, ChevronDown, Eye, EyeOff, Search, Star, X } from 'lucide-react';
import { PageHeader } from '../ui/PageHeader';
import { disciplineClass } from '../../utils/discipline';

/**
 * Sınav spotları (Kurul 1). Veri: src/data/exam_spots_k1.json — scripts/sinav_spotlari/birlestir.py üretir;
 * her spotun ders notundan birebir alıntısı dogrula.py ile denetlenir. Sayfa yalnız gösterir.
 * Yapı: başlık · Oku/Kendini sına · arama + ders/disiplin süzgeci · kategori şeridi · ders ders (ya da kategori
 * kategori) gruplanmış spot kartları. "Öğrendim" işareti tarayıcıda (medsoru_spot_ogrendim) tutulur.
 * Stil: styles/spots.css (.xs-*).
 */

type Kategori = 'en_sik' | 'karakteristik' | 'sayi' | 'eslesme' | 'tani_tedavi' | 'mekanizma' | 'tuzak' | 'siniflama';

interface Spot {
  id: string;
  ders: number;
  kategori: Kategori;
  onem: 1 | 2 | 3;
  baslik: string;
  spot: string;
  maddeler?: string[];
  soru?: string;
  cevap?: string;
  tuzak?: string;
  karsilastir?: { basliklar: string[]; satirlar: string[][] } | null;
  etiketler?: string[];
  kaynak: { satir?: number; alinti: string }[];
}
interface Ders { no: number; id: string; baslik: string; disiplin: string; hoca?: string; sayi: number }
interface Veri { dersler: Ders[]; spotlar: Spot[] }

export const KATEGORILER: { id: Kategori; ad: string; kisa: string; aciklama: string }[] = [
  { id: 'en_sik', ad: 'En sık · en az · tek', kisa: 'En sık', aciklama: 'En sık, en az, en çok, tek, ilk ifadeleri' },
  { id: 'karakteristik', ad: 'Karakteristik bulgu', kisa: 'Karakteristik', aciklama: 'Patognomonik, tipik görünüm, triad' },
  { id: 'tuzak', ad: 'Tuzak & çeldirici', kisa: 'Tuzak', aciklama: 'Karıştırılan kavramlar, klasik çeldiriciler' },
  { id: 'eslesme', ad: 'Eşleştir', kisa: 'Eşleştir', aciklama: 'Etken → hastalık, gen → sendrom, belirteç → tümör' },
  { id: 'sayi', ad: 'Sayı & oran', kisa: 'Sayı', aciklama: 'Yüzde, eşik, süre, doz' },
  { id: 'tani_tedavi', ad: 'Tanı & tedavi', kisa: 'Tanı/Tedavi', aciklama: 'İlk tercih, altın standart, tanı testi' },
  { id: 'mekanizma', ad: 'Mekanizma', kisa: 'Mekanizma', aciklama: 'Sınavda sorulan neden–sonuç' },
  { id: 'siniflama', ad: 'Sınıflama', kisa: 'Sınıflama', aciklama: 'Tip, evre, derece ayrımı' },
];
const KAT = Object.fromEntries(KATEGORILER.map((k) => [k.id, k])) as Record<Kategori, (typeof KATEGORILER)[number]>;

const ANAHTAR = 'medsoru_spot_ogrendim';
const okuOgrenilen = (): Set<string> => {
  try { return new Set(JSON.parse(localStorage.getItem(ANAHTAR) || '[]')); } catch { return new Set(); }
};
const yazOgrenilen = (s: Set<string>) => {
  try { localStorage.setItem(ANAHTAR, JSON.stringify([...s])); } catch { /* özel pencere */ }
};

const kucuk = (s: string) => s.toLocaleLowerCase('tr-TR');

/** **kalın** → <strong>; başka biçim yok */
const Zengin: React.FC<{ metin: string }> = ({ metin }) => (
  <>
    {metin.split(/(\*\*[^*]+\*\*)/g).map((p, i) =>
      p.startsWith('**') && p.endsWith('**') ? <strong key={i}>{p.slice(2, -2)}</strong> : <React.Fragment key={i}>{p}</React.Fragment>
    )}
  </>
);

const Yildiz: React.FC<{ n: number }> = ({ n }) => (
  <span className="xs-stars" aria-label={`Önem ${n}/3`} title={n === 3 ? 'Kesin sorulur' : n === 2 ? 'Sık sorulur' : 'Destekleyici'}>
    {[1, 2, 3].map((i) => <Star key={i} size={11} className={i <= n ? 'is-on' : ''} aria-hidden />)}
  </span>
);

const SpotKart: React.FC<{ s: Spot; sinav: boolean; ogrenildi: boolean; onOgren: () => void; dersAdi?: string }> = ({ s, sinav, ogrenildi, onOgren, dersAdi }) => {
  const [acik, setAcik] = useState(false);
  const gizli = sinav && !acik;
  return (
    <article className={`xs-card is-${s.kategori} ${ogrenildi ? 'is-done' : ''}`}>
      <header className="xs-card-h">
        <span className={`xs-pill is-${s.kategori}`}>{KAT[s.kategori]?.kisa}</span>
        <Yildiz n={s.onem} />
        {dersAdi && <span className="xs-card-ders">{dersAdi}</span>}
        <button type="button" className={`xs-done ${ogrenildi ? 'is-on' : ''}`} onClick={onOgren} aria-pressed={ogrenildi} title="Öğrendim">
          <Check size={14} aria-hidden /><span>{ogrenildi ? 'Öğrendim' : 'Öğren'}</span>
        </button>
      </header>
      <h3 className="xs-title">{s.baslik}</h3>
      {gizli ? (
        <button type="button" className="xs-ask" onClick={() => setAcik(true)}>
          <span>{s.soru || 'Bu spotu hatırlıyor musun?'}</span>
          <span className="xs-ask-btn"><Eye size={14} aria-hidden /> Cevabı göster</span>
        </button>
      ) : (
        <div className="xs-body">
          {sinav && s.cevap && <p className="xs-answer"><span>Cevap</span> {s.cevap}</p>}
          <p className="xs-spot"><Zengin metin={s.spot} /></p>
          {!!s.maddeler?.length && (
            <ul className="xs-list">{s.maddeler.map((m, i) => <li key={i}><Zengin metin={m} /></li>)}</ul>
          )}
          {s.karsilastir && s.karsilastir.basliklar?.length > 0 && (
            <div className="xs-table-wrap">
              <table className="xs-table">
                <thead><tr><th scope="col" />{s.karsilastir.basliklar.map((b) => <th key={b} scope="col">{b}</th>)}</tr></thead>
                <tbody>
                  {s.karsilastir.satirlar.map((r, i) => (
                    <tr key={i}><th scope="row">{r[0]}</th>{r.slice(1).map((c, j) => <td key={j}><Zengin metin={c} /></td>)}</tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          {s.tuzak && (
            <div className="xs-trap" role="note">
              <AlertTriangle size={15} aria-hidden />
              <p><b>Tuzak:</b> <Zengin metin={s.tuzak} /></p>
            </div>
          )}
          {!!s.kaynak?.length && (
            <details className="xs-src">
              <summary><BookMarked size={13} aria-hidden /> Ders notundaki yeri</summary>
              {s.kaynak.map((k, i) => (
                <blockquote key={i}>“{k.alinti}”{k.satir ? <cite> · satır {k.satir}</cite> : null}</blockquote>
              ))}
            </details>
          )}
        </div>
      )}
    </article>
  );
};

const SAYFA = 40;

export const ExamSpotsView: React.FC = () => {
  const [veri, setVeri] = useState<Veri | null>(null);
  const [hata, setHata] = useState(false);
  const [q, setQ] = useState('');
  const [kat, setKat] = useState<Kategori | 'hepsi'>('hepsi');
  const [ders, setDers] = useState<number | 0>(0);
  const [disiplin, setDisiplin] = useState('');
  const [yalnizOnemli, setYalnizOnemli] = useState(false);
  const [gizleOgrenilen, setGizleOgrenilen] = useState(false);
  const [sinav, setSinav] = useState(false);
  const [grup, setGrup] = useState<'ders' | 'kategori'>('ders');
  const [ogrenilen, setOgrenilen] = useState<Set<string>>(okuOgrenilen);
  const [limit, setLimit] = useState(SAYFA);

  useEffect(() => {
    let iptal = false;
    import('../../data/exam_spots_k1.json')
      .then((m) => { if (!iptal) setVeri((m.default ?? m) as unknown as Veri); })
      .catch(() => { if (!iptal) setHata(true); });
    return () => { iptal = true; };
  }, []);

  useEffect(() => { setLimit(SAYFA); }, [q, kat, ders, disiplin, yalnizOnemli, gizleOgrenilen, grup]);

  const dersMap = useMemo(() => new Map((veri?.dersler || []).map((d) => [d.no, d])), [veri]);
  const disiplinler = useMemo(() => [...new Set((veri?.dersler || []).map((d) => d.disiplin))].sort((a, b) => a.localeCompare(b, 'tr')), [veri]);

  const temelSuzgec = useMemo(() => {
    if (!veri) return [];
    const qq = kucuk(q.trim());
    return veri.spotlar.filter((s) => {
      if (ders && s.ders !== ders) return false;
      if (disiplin && dersMap.get(s.ders)?.disiplin !== disiplin) return false;
      if (yalnizOnemli && s.onem < 3) return false;
      if (gizleOgrenilen && ogrenilen.has(s.id)) return false;
      if (qq) {
        const t = kucuk([s.baslik, s.spot, s.tuzak, s.cevap, ...(s.maddeler || []), ...(s.etiketler || [])].join(' '));
        if (!qq.split(/\s+/).every((w) => t.includes(w))) return false;
      }
      return true;
    });
  }, [veri, q, ders, disiplin, yalnizOnemli, gizleOgrenilen, ogrenilen, dersMap]);

  const katSayi = useMemo(() => {
    const m: Record<string, number> = {};
    for (const s of temelSuzgec) m[s.kategori] = (m[s.kategori] || 0) + 1;
    return m;
  }, [temelSuzgec]);

  const liste = useMemo(() => (kat === 'hepsi' ? temelSuzgec : temelSuzgec.filter((s) => s.kategori === kat))
    .slice().sort((a, b) => (grup === 'ders' ? a.ders - b.ders : 0) || (grup === 'kategori' ? KATEGORILER.findIndex((k) => k.id === a.kategori) - KATEGORILER.findIndex((k) => k.id === b.kategori) : 0) || b.onem - a.onem),
  [temelSuzgec, kat, grup]);

  const gorunen = liste.slice(0, limit);
  const gruplar = useMemo(() => {
    const out: { anahtar: string; baslik: string; alt?: string; disiplin?: string; ogeler: Spot[] }[] = [];
    for (const s of gorunen) {
      const anahtar = grup === 'ders' ? `d${s.ders}` : s.kategori;
      let g = out[out.length - 1];
      if (!g || g.anahtar !== anahtar) {
        const d = dersMap.get(s.ders);
        g = grup === 'ders'
          ? { anahtar, baslik: `${s.ders}. ${d?.baslik || 'Ders'}`, alt: d?.disiplin, disiplin: d?.disiplin, ogeler: [] }
          : { anahtar, baslik: KAT[s.kategori].ad, alt: KAT[s.kategori].aciklama, ogeler: [] };
        out.push(g);
      }
      g.ogeler.push(s);
    }
    return out;
  }, [gorunen, grup, dersMap]);

  const ogren = (id: string) => setOgrenilen((p) => {
    const n = new Set(p);
    if (n.has(id)) n.delete(id); else n.add(id);
    yazOgrenilen(n);
    return n;
  });

  const toplam = veri?.spotlar.length || 0;
  const ogrenilenSayi = veri ? veri.spotlar.filter((s) => ogrenilen.has(s.id)).length : 0;

  return (
    <div className="xs-page">
      <PageHeader
        title="Sınav spotları"
        description="Ders notlarından birebir: en sık sorulanlar, ayırıcı bulgular, sayılar ve tuzaklar."
        stats={veri ? [
          { label: 'spot', value: toplam.toLocaleString('tr-TR') },
          { label: 'ders', value: veri.dersler.length },
          { label: 'öğrendim', value: ogrenilenSayi, tone: 'ok' },
        ] : undefined}
        actions={
          <div className="xs-mode" role="group" aria-label="Görünüm">
            <button type="button" aria-pressed={!sinav} className={!sinav ? 'is-on' : ''} onClick={() => setSinav(false)}><Eye size={14} aria-hidden /> Oku</button>
            <button type="button" aria-pressed={sinav} className={sinav ? 'is-on' : ''} onClick={() => setSinav(true)}><EyeOff size={14} aria-hidden /> Kendini sına</button>
          </div>
        }
      />

      {hata && <p className="xs-empty">Spot verisi yüklenemedi. Sayfayı yenileyip tekrar dene.</p>}
      {!veri && !hata && <p className="xs-empty">Yükleniyor…</p>}

      {veri && (
        <>
          <div className="xs-filters">
            <label className="xs-search">
              <Search size={16} aria-hidden />
              <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Spotlarda ara (ör. en sık, Turner, nefrotik)" aria-label="Spotlarda ara" />
              {q && <button type="button" onClick={() => setQ('')} aria-label="Aramayı temizle"><X size={14} /></button>}
            </label>
            <select className="xs-select" value={disiplin} onChange={(e) => { setDisiplin(e.target.value); setDers(0); }} aria-label="Disiplin">
              <option value="">Tüm disiplinler</option>
              {disiplinler.map((d) => <option key={d} value={d}>{d}</option>)}
            </select>
            <select className="xs-select" value={ders} onChange={(e) => setDers(Number(e.target.value))} aria-label="Ders">
              <option value={0}>Tüm dersler</option>
              {veri.dersler.filter((d) => !disiplin || d.disiplin === disiplin).map((d) => <option key={d.no} value={d.no}>{d.no}. {d.baslik} ({d.sayi})</option>)}
            </select>
          </div>

          <div className="xs-cats" role="tablist" aria-label="Kategori">
            <button type="button" role="tab" aria-selected={kat === 'hepsi'} className={kat === 'hepsi' ? 'is-on' : ''} onClick={() => setKat('hepsi')}>
              Tümü <b>{temelSuzgec.length}</b>
            </button>
            {KATEGORILER.map((k) => (
              <button key={k.id} type="button" role="tab" aria-selected={kat === k.id} title={k.aciklama}
                className={`is-${k.id} ${kat === k.id ? 'is-on' : ''}`} onClick={() => setKat(k.id)} disabled={!katSayi[k.id]}>
                {k.kisa} <b>{katSayi[k.id] || 0}</b>
              </button>
            ))}
          </div>

          <div className="xs-toggles">
            <label><input type="checkbox" checked={yalnizOnemli} onChange={(e) => setYalnizOnemli(e.target.checked)} /> Yalnız ★★★ (kesin sorulur)</label>
            <label><input type="checkbox" checked={gizleOgrenilen} onChange={(e) => setGizleOgrenilen(e.target.checked)} /> Öğrendiklerimi gizle</label>
            <span className="xs-group-by">
              Grupla:
              <button type="button" className={grup === 'ders' ? 'is-on' : ''} onClick={() => setGrup('ders')}>Ders</button>
              <button type="button" className={grup === 'kategori' ? 'is-on' : ''} onClick={() => setGrup('kategori')}>Kategori</button>
            </span>
          </div>

          {liste.length === 0 && <p className="xs-empty">Bu süzgeçle spot yok.</p>}

          {gruplar.map((g) => (
            <section key={g.anahtar} className={`xs-group ${g.disiplin ? disciplineClass(g.disiplin) : `is-${g.anahtar}`}`}>
              <h2 className="xs-group-h"><span>{g.baslik}</span>{g.alt && <small>{g.alt}</small>}</h2>
              <div className="xs-grid">
                {g.ogeler.map((s) => (
                  <SpotKart key={s.id} s={s} sinav={sinav} ogrenildi={ogrenilen.has(s.id)} onOgren={() => ogren(s.id)}
                    dersAdi={grup === 'kategori' ? dersMap.get(s.ders)?.baslik : undefined} />
                ))}
              </div>
            </section>
          ))}

          {liste.length > limit && (
            <button type="button" className="xs-more" onClick={() => setLimit((l) => l + SAYFA * 2)}>
              <ChevronDown size={16} aria-hidden /> Daha fazla göster ({liste.length - limit} kaldı)
            </button>
          )}
        </>
      )}
    </div>
  );
};

export default ExamSpotsView;
