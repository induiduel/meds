/**
 * Güncelleme ve geliştirme günlüğü (/guncellemeler).
 * Veri: src/data/surum_gunlugu.json ← scripts/surum_gunlugu.py (git geçmişi + guncelleme_notu.json; `npm run build` öncesi).
 * Hiyerarşi: gün → sürüm kartı → öğrenci notu (Eklenen / Değişen / Düzeltilen / Kaldırılan) → açılır geliştirme ayrıntısı
 * (commit konuları + dosya sayıları). En altta ilk sürüm öncesi günlük ara sürümler. Stil: styles/guncellemeler.css (.gg-*).
 */
import React, { useEffect, useMemo, useState } from 'react';
import { ChevronDown, FileMinus2, FilePen, FilePlus2, Minus, Plus, RefreshCw, ScrollText, Search, Wrench } from 'lucide-react';
import VERI from '../../data/surum_gunlugu.json';
import '../../styles/guncellemeler.css';

type Tur = 'eklenen' | 'degisen' | 'duzeltilen' | 'silinen';
type Not = { tur: Tur; metin: string; commit: string; tarih: string };
type Surum = {
  surum: number; tarih: string; commit: string; baslik: string;
  ogrenci: Record<Tur, string[]>; gelistirme: Not[];
  dosyalar: { eklenen: number; silinen: number; degisen: number; ornekEklenen: string[]; ornekSilinen: string[] };
};
type Veri = { uretildi: string | null; surumler: Surum[]; yayinlanmamis: Not[]; oncesi: { gun: string; gelistirme: Not[] }[] };
const D = VERI as unknown as Veri;

const TURLER: { id: Tur; ad: string; ikon: React.ElementType }[] = [
  { id: 'eklenen', ad: 'Eklenen', ikon: Plus },
  { id: 'degisen', ad: 'Değişen', ikon: RefreshCw },
  { id: 'duzeltilen', ad: 'Düzeltilen', ikon: Wrench },
  { id: 'silinen', ad: 'Kaldırılan', ikon: Minus },
];

const gunYaz = (iso: string) => new Date(iso).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric', weekday: 'long' });
const saatYaz = (iso: string) => new Date(iso).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
const kucuk = (s: string) => s.toLocaleLowerCase('tr-TR');

function NotListesi({ notlar, suzgec }: { notlar: Not[]; suzgec: Tur | null }) {
  const g = suzgec ? notlar.filter((n) => n.tur === suzgec) : notlar;
  if (!g.length) return <p className="gg-bos-k">Bu türde geliştirme notu yok.</p>;
  return (
    <ul className="gg-dev">
      {g.map((n) => {
        const t = TURLER.find((x) => x.id === n.tur)!;
        return (
          <li key={n.commit} data-tur={n.tur}>
            <span className="gg-nokta" aria-label={t.ad} title={t.ad}><t.ikon /></span>
            <span className="gg-dev-m">{n.metin}</span>
            <code>{n.commit}</code>
          </li>
        );
      })}
    </ul>
  );
}

/** H150: öğrenci maddelerine sızan dosya yolu / kod parçası temizlenir; temizlenince anlamsız kalan madde gösterilmez */
const YOL = /(`[^`]*`|\b(?:meds|src|scripts|data|docs|public)\/[\w./*<>-]+|\b[\w-]+\.(?:tsx?|py|json|css|mjs|sh|md)\b)/g;
function ogrenciMaddeleri(l?: string[]): string[] {
  return (l || []).map((m) => m.replace(/\s*\([^()]*(?:`|\/|\.(?:tsx?|py|json|css|sh))[^()]*\)/g, '').replace(YOL, '').replace(/\s{2,}/g, ' ').replace(/\s+([,.;:])/g, '$1').replace(/[,;:]\s*$/, '').trim())
    .filter((m) => m.split(' ').length >= 3);
}

function SurumKarti({ s, suzgec, gelistirici, ilk }: { s: Surum; suzgec: Tur | null; gelistirici: boolean; ilk: boolean }) {
  const [acik, setAcik] = useState(false);
  const bolumler = TURLER.filter((t) => (!suzgec || suzgec === t.id) && ogrenciMaddeleri(s.ogrenci[t.id]).length);
  const f = s.dosyalar;
  return (
    <article className={`gg-kart${ilk ? ' is-son' : ''}`} id={`v${s.surum}`}>
      <header className="gg-kart-bas">
        <a className="gg-rozet" href={`#v${s.surum}`}>v{s.surum}</a>
        <div className="gg-kart-m">
          <h3>{s.baslik}</h3>
          <p>{saatYaz(s.tarih)}{ilk && <span className="gg-guncel">Kullandığın sürüm</span>}</p>
        </div>
      </header>

      {bolumler.length > 0 && (
        <div className="gg-bolumler">
          {bolumler.map((t) => (
            <section key={t.id} className="gg-bolum" data-tur={t.id}>
              <h4><t.ikon /> {t.ad}</h4>
              <ul>{ogrenciMaddeleri(s.ogrenci[t.id]).map((m, i) => <li key={i}>{m}</li>)}</ul>
            </section>
          ))}
        </div>
      )}

      {gelistirici && (
        <div className="gg-ayr">
          <button type="button" className="gg-ayr-btn" aria-expanded={acik} onClick={() => setAcik((a) => !a)}>
            <span>Geliştirme ayrıntıları</span>
            <span className="gg-sayac">{s.gelistirme.length} değişiklik</span>
            <span className="gg-dosya" title="src/, server.ts, scripts/ altındaki dosyalar">
              <span data-tur="eklenen"><FilePlus2 />{f.eklenen}</span>
              <span data-tur="degisen"><FilePen />{f.degisen}</span>
              <span data-tur="silinen"><FileMinus2 />{f.silinen}</span>
            </span>
            <ChevronDown className="gg-ok" />
          </button>
          {acik && (
            <div className="gg-ayr-ic">
              <NotListesi notlar={s.gelistirme} suzgec={suzgec} />
              {(f.ornekEklenen.length > 0 || f.ornekSilinen.length > 0) && (
                <div className="gg-dosyalar">
                  {f.ornekEklenen.length > 0 && <div><b>Yeni dosyalar</b>{f.ornekEklenen.map((x) => <code key={x}>{x}</code>)}</div>}
                  {f.ornekSilinen.length > 0 && <div><b>Silinen dosyalar</b>{f.ornekSilinen.map((x) => <code key={x}>{x}</code>)}</div>}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </article>
  );
}

export default function GuncellemeGunluguView() {
  const [suzgec, setSuzgec] = useState<Tur | null>(null);
  const [ara, setAra] = useState('');
  const [gelistirici, setGelistirici] = useState(() => { try { return localStorage.getItem('medsoru_gunluk_gelistirici') === '1'; } catch { return false; } });
  const [oncesiAcik, setOncesiAcik] = useState(false);
  useEffect(() => { document.title = 'Güncelleme günlüğü · MeDSor'; }, []);
  useEffect(() => { try { localStorage.setItem('medsoru_gunluk_gelistirici', gelistirici ? '1' : '0'); } catch { /* yok */ } }, [gelistirici]);

  const toplam = useMemo(() => {
    const t: Record<Tur, number> = { eklenen: 0, degisen: 0, duzeltilen: 0, silinen: 0 };
    D.surumler.forEach((s) => TURLER.forEach(({ id }) => { t[id] += s.ogrenci[id]?.length || 0; }));
    return t;
  }, []);

  const gunler = useMemo(() => {
    const q = kucuk(ara.trim());
    const uyar = (s: Surum) => {
      if (suzgec && !s.ogrenci[suzgec]?.length && !(gelistirici && s.gelistirme.some((n) => n.tur === suzgec))) return false;
      if (!q) return true;
      const metin = [s.baslik, `v${s.surum}`, ...TURLER.flatMap((t) => s.ogrenci[t.id] || []), ...(gelistirici ? s.gelistirme.map((n) => n.metin) : [])];
      return metin.some((m) => kucuk(m).includes(q));
    };
    const g = new Map<string, Surum[]>();
    D.surumler.filter(uyar).forEach((s) => { const k = s.tarih.slice(0, 10); g.set(k, [...(g.get(k) || []), s]); });
    return [...g.entries()];
  }, [ara, suzgec, gelistirici]);

  const son = D.surumler[0];
  return (
    <div className="gg">
      <header className="gg-bas">
        <div className="gg-ic"><ScrollText /></div>
        <div className="gg-bas-m">
          <h1>Güncelleme günlüğü</h1>
          <p>Her sürümde nelerin eklendiğini, değiştiğini, düzeltildiğini ve kaldırıldığını buradan izleyebilirsin.</p>
        </div>
      </header>

      {son && (
        <div className="gg-ozet">
          <div><b>v{son.surum}</b><span>Güncel sürüm</span></div>
          <div><b>{D.surumler.length}</b><span>Sürüm</span></div>
          {TURLER.map((t) => <div key={t.id} data-tur={t.id}><b>{toplam[t.id]}</b><span>{t.ad}</span></div>)}
        </div>
      )}

      <div className="gg-arac">
        <label className="gg-ara">
          <Search />
          <input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Sürümlerde ara (ör. çevrimdışı, sesli ders)" aria-label="Sürümlerde ara" />
        </label>
        <div className="gg-haplar" role="group" aria-label="Değişiklik türü">
          <button type="button" aria-pressed={!suzgec} onClick={() => setSuzgec(null)}>Tümü</button>
          {TURLER.map((t) => (
            <button key={t.id} type="button" data-tur={t.id} aria-pressed={suzgec === t.id} onClick={() => setSuzgec(suzgec === t.id ? null : t.id)}>
              <t.ikon /> {t.ad}
            </button>
          ))}
          <label className="gg-anahtar">
            <input type="checkbox" checked={gelistirici} onChange={(e) => setGelistirici(e.target.checked)} />
            <span>Geliştirme notları</span>
          </label>
        </div>
      </div>

      {gelistirici && D.yayinlanmamis.length > 0 && !ara && (
        <section className="gg-gun">
          <h2 className="gg-gun-bas"><span>Yayınlanmamış</span><small>Bir sonraki sürüme girecek</small></h2>
          <div className="gg-kart is-taslak"><NotListesi notlar={D.yayinlanmamis} suzgec={suzgec} /></div>
        </section>
      )}

      {gunler.length === 0 && <p className="gg-bos">Aramana uyan sürüm bulunamadı.</p>}
      {gunler.map(([gun, ss]) => (
        <section key={gun} className="gg-gun">
          <h2 className="gg-gun-bas"><span>{gunYaz(ss[0].tarih)}</span><small>{ss.length} sürüm</small></h2>
          <div className="gg-zaman">
            {ss.map((s) => <SurumKarti key={s.surum} s={s} suzgec={suzgec} gelistirici={gelistirici} ilk={s === son} />)}
          </div>
        </section>
      ))}

      {gelistirici && !ara && D.oncesi.length > 0 && (
        <section className="gg-gun gg-oncesi">
          <button type="button" className="gg-ayr-btn" aria-expanded={oncesiAcik} onClick={() => setOncesiAcik((a) => !a)}>
            <span>İlk sürümden önceki geliştirmeler</span>
            <span className="gg-sayac">{D.oncesi.length} gün · {D.oncesi.reduce((n, g) => n + g.gelistirme.length, 0)} değişiklik</span>
            <ChevronDown className="gg-ok" />
          </button>
          {oncesiAcik && D.oncesi.map((g) => (
            <div key={g.gun} className="gg-kart is-taslak">
              <h3 className="gg-ara-gun">{gunYaz(g.gun + 'T12:00:00')}</h3>
              <NotListesi notlar={g.gelistirme} suzgec={suzgec} />
            </div>
          ))}
        </section>
      )}
    </div>
  );
}
