/**
 * Olası sorular (/olasi-sorular?kurul=N): sınavdan sonra öğrencilerin eklediği hatıralardan her gece kurulan
 * 100 yuvalık olası soru seti (scripts/olasi_soru → data/olasi_sorular/kN.json → GET /api/olasi-sorular/:kurul).
 * Kart: yuva no, güven rozeti, branş, kök, şıkları çözme (seç → doğru/yanlış + her şıkkın açıklaması), kaynak/destek,
 * ders bağı, benzer çıkmışlar ve geri bildirim (buydu / değildi / düzeltme). Stil: styles/olasi-sorular.css (.os-*).
 */
import React, { useEffect, useMemo, useState } from 'react';
import { BookOpen, Check, CircleHelp, MessageSquarePlus, Search, Sparkles, SquarePen, ThumbsDown, ThumbsUp, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { KURULLAR, ekranGunu, gunFarki, kurulAdi, tarihYaz, tarihteYaz } from '../../services/kurulPencere';
import { aktifKurul, sonSinavKurul } from '../../services/kurulTakvimi';
import { linkClick, navigateTo } from '../../router';
import SCHEDULE from '../../data/deckSchedule.json';
import '../../styles/olasi-sorular.css';

type Sik = { harf: string; metin: string; kaynak?: 'ogrenci' | 'ders'; destek?: number; aciklama?: string };
export type OlasiSoru = {
  id: string; yuva: string; brans?: string; kok: string; siklar: Sik[]; cevap?: string; cevap_ders?: string | null;
  guven?: number; belirsizlik?: string; gerekce?: string; kanit_idleri?: string[];
  ders_ref?: { ders_id?: string; sayfa?: number | null; cumle_id?: string | null } | null; benzer_cikmis?: string[];
};
type OlasiSet = { surum: number; kurul: number; uretildi?: string; sorular: OlasiSoru[] };
type Durum = { yuk: true } | { yok: true } | { hata: string } | { set: OlasiSet };
type Karar = 'boyleydi' | 'degildi' | 'duzeltme';

const GB_KEY = 'medsoru_olasi_geri_bildirim_v1';
const gbOku = (): Record<string, Karar> => { try { return JSON.parse(localStorage.getItem(GB_KEY) || '{}') || {}; } catch { return {}; } };
const gbYaz = (m: Record<string, Karar>) => { try { localStorage.setItem(GB_KEY, JSON.stringify(m)); } catch { /* özel pencere */ } };

const katla = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');
const yuvaNo = (y: string) => { const n = parseInt(y, 10); return Number.isFinite(n) ? n : 999; };
const guvenSinif = (g = 0) => (g >= 70 ? { cls: 'is-yuksek', ad: 'Yüksek güven' } : g >= 40 ? { cls: 'is-orta', ad: 'Orta güven' } : { cls: 'is-dusuk', ad: 'Düşük güven' });
const HARFLER = ['A', 'B', 'C', 'D', 'E'];

const urlKurul = (): number => {
  try { const n = Number(new URLSearchParams(location.search).get('kurul')); if (n >= 1 && n <= 6) return n; } catch { /* yok */ }
  return sonSinavKurul(ekranGunu())?.kurul ?? aktifKurul(ekranGunu()).kurul;
};

/** ders_ref.ders_id ("k1-02-…") → Öğren destesi (k1p-k1-02-…) varsa o, yoksa ders notu */
const dersBagi = (ref?: OlasiSoru['ders_ref']): { url: string; ad: string } | null => {
  const id = ref?.ders_id;
  if (!id) return null;
  const m = /^k(\d)-/.exec(id);
  const deste = m ? `k${m[1]}p-${id}` : id;
  if ((SCHEDULE as Record<string, unknown>)[deste]) return { url: `/ogren/${encodeURIComponent(deste)}`, ad: 'Etkileşimli derste aç' };
  return { url: `/notlar?id=${encodeURIComponent(id)}${ref?.sayfa ? `&page=${ref.sayfa}` : ''}`, ad: ref?.sayfa ? `Ders notu, sayfa ${ref.sayfa}` : 'Ders notunda aç' };
};

const Bag: React.FC<{ url: string; className?: string; children: React.ReactNode }> = ({ url, className, children }) => (
  <a href={url} className={className} onClick={linkClick(() => navigateTo(url))}>{children}</a>
);

export default function OlasiSorularView({ uid }: { uid?: string }) {
  const gun = ekranGunu();
  const [kurul, setKurul0] = useState<number>(urlKurul);
  const [durum, setDurum] = useState<Durum>({ yuk: true });
  const [setler, setSetler] = useState<{ kurul: number; soru: number }[]>([]);
  const [ara, setAra] = useState('');
  const [brans, setBrans] = useState('hepsi');
  const [gb, setGb] = useState<Record<string, Karar>>(gbOku);

  useEffect(() => { document.title = 'Olası sorular · MeDSor'; }, []);
  useEffect(() => {
    safeJsonFetch<{ setler: { kurul: number; soru: number }[] }>('/api/olasi-sorular').then((r) => { if (r.ok && r.data) setSetler(r.data.setler || []); });
  }, []);
  useEffect(() => {
    let canli = true;
    setDurum({ yuk: true });
    safeJsonFetch<OlasiSet>(`/api/olasi-sorular/${kurul}`).then((r) => {
      if (!canli) return;
      if (r.ok && r.data && Array.isArray(r.data.sorular)) setDurum({ set: r.data });
      else if (r.status === 404) setDurum({ yok: true });
      else setDurum({ hata: r.error || 'Olası sorular alınamadı.' });
    });
    return () => { canli = false; };
  }, [kurul]);

  const setKurul = (k: number) => {
    setKurul0(k); setBrans('hepsi'); setAra('');
    try {
      const u = new URL(location.href); u.searchParams.set('kurul', String(k));
      history.replaceState(history.state, '', u.pathname + u.search + u.hash);
    } catch { /* yok */ }
  };

  const sorular = 'set' in durum ? durum.set.sorular : [];
  const branslar = useMemo(() => {
    const m = new Map<string, number>();
    sorular.forEach((s) => { const b = s.brans || 'Diğer'; m.set(b, (m.get(b) || 0) + 1); });
    return [...m.entries()].sort((a, b) => b[1] - a[1]);
  }, [sorular]);
  const liste = useMemo(() => {
    const q = katla(ara.trim());
    return sorular
      .filter((s) => brans === 'hepsi' || (s.brans || 'Diğer') === brans)
      .filter((s) => !q || katla(`${s.yuva} ${s.kok} ${s.siklar.map((x) => x.metin).join(' ')}`).includes(q))
      .sort((a, b) => yuvaNo(a.yuva) - yuvaNo(b.yuva) || a.id.localeCompare(b.id));
  }, [sorular, brans, ara]);

  const kb = KURULLAR.find((k) => k.kurul === kurul) || KURULLAR[0];
  const sinavaKalan = gunFarki(gun, kb.sinav);

  const geriBildir = async (s: OlasiSoru, karar: Karar, ek?: { metin?: string; cevap?: string }) => {
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (uid) headers['x-user-uid'] = uid;
    const r = await safeJsonFetch(`/api/olasi-sorular/${kurul}/${encodeURIComponent(s.id)}/geri-bildirim`, {
      method: 'POST', headers, body: JSON.stringify({ karar, ...ek }),
    });
    if (r.ok) { const m = { ...gb, [s.id]: karar }; setGb(m); gbYaz(m); }
    return r.ok;
  };

  return (
    <div className="os">
      <header className="os-bas">
        <span className="os-ic" aria-hidden><Sparkles /></span>
        <div className="os-bas-m">
          <h1>Olası sorular</h1>
          <p>{kurulAdi(kb)} · sınav {tarihYaz(kb.sinav, gun)}. Sınavdan sonra eklenen hatıralardan her gece yeniden kurulur.</p>
        </div>
        <label className="os-kurul">
          <span className="sr-only">Kurul</span>
          <select value={kurul} onChange={(e) => setKurul(Number(e.target.value))}>
            {KURULLAR.map((k) => {
              const n = setler.find((x) => x.kurul === k.kurul)?.soru;
              return <option key={k.kurul} value={k.kurul}>Kurul {k.kurul}{n ? ` · ${n} soru` : ''}</option>;
            })}
          </select>
        </label>
      </header>

      {'yuk' in durum && <div className="os-bos" role="status"><span className="os-spin" aria-hidden /> Olası sorular yükleniyor…</div>}
      {'hata' in durum && <div className="os-bos"><p>Olası sorular alınamadı. Bağlantını kontrol edip sayfayı yenile.</p></div>}
      {'yok' in durum && (
        <div className="os-bos">
          <CircleHelp aria-hidden className="os-bos-i" />
          {sinavaKalan > 0 ? (
            <>
              <b>Sınav {tarihteYaz(kb.sinav)}</b>
              <p>Sınavdan sonra soruları ekledikçe her gece olası sorular burada oluşur. Hatırladığın her parça, kaçıncı soru olduğunu biliyorsan numarasıyla, seti güçlendirir.</p>
            </>
          ) : (
            <>
              <b>{sinavaKalan === 0 ? 'Sınav bugün' : `Sınav ${tarihteYaz(kb.sinav)} yapıldı`}</b>
              <p>Bu kurul için henüz olası soru seti oluşmadı. Hatırladığın soruları ekle; set her gece yeni kayıtlarla yeniden kurulur.</p>
            </>
          )}
          <Bag url="/" className="os-dug is-ana"><SquarePen aria-hidden /> Soru ekle</Bag>
        </div>
      )}

      {'set' in durum && (
        <>
          <div className="os-arac">
            <label className="os-ara">
              <Search aria-hidden />
              <input value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Kökte, şıkta ya da numarada ara" aria-label="Olası sorularda ara" />
              {ara && <button type="button" onClick={() => setAra('')} aria-label="Aramayı temizle"><X aria-hidden /></button>}
            </label>
            {branslar.length > 1 && (
              <div className="os-suz" role="group" aria-label="Branşa göre süz">
                <button type="button" aria-pressed={brans === 'hepsi'} className={brans === 'hepsi' ? 'is-on' : ''} onClick={() => setBrans('hepsi')}>Tümü <span>{sorular.length}</span></button>
                {branslar.map(([b, n]) => (
                  <button key={b} type="button" aria-pressed={brans === b} className={brans === b ? 'is-on' : ''} onClick={() => setBrans(b)}>{b} <span>{n}</span></button>
                ))}
              </div>
            )}
          </div>
          {durum.set.uretildi && <p className="os-not">Son güncelleme: {new Date(durum.set.uretildi).toLocaleString('tr-TR', { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' })} · {sorular.length} soru</p>}
          <div className="os-liste">
            {liste.map((s) => <OlasiKart key={s.id} s={s} karar={gb[s.id]} onGeriBildirim={geriBildir} />)}
            {liste.length === 0 && <div className="os-bos"><p>{ara ? `“${ara}” ile eşleşen soru yok.` : 'Bu süzgeçte soru yok.'}</p></div>}
          </div>
        </>
      )}
    </div>
  );
}

const OlasiKart: React.FC<{
  s: OlasiSoru; karar?: Karar;
  onGeriBildirim: (s: OlasiSoru, k: Karar, ek?: { metin?: string; cevap?: string }) => Promise<boolean>;
}> = ({ s, karar, onGeriBildirim }) => {
  const [secim, setSecim] = useState<string | null>(null);
  const [duzelt, setDuzelt] = useState(false);
  const [metin, setMetin] = useState('');
  const [cevabim, setCevabim] = useState('');
  const [gonderiliyor, setGonderiliyor] = useState(false);
  const [hata, setHata] = useState('');
  const g = guvenSinif(s.guven);
  const bag = dersBagi(s.ders_ref);
  const cozuldu = secim !== null;

  const gonder = async (k: Karar, ek?: { metin?: string; cevap?: string }) => {
    setGonderiliyor(true); setHata('');
    const ok = await onGeriBildirim(s, k, ek);
    setGonderiliyor(false);
    if (ok) setDuzelt(false); else setHata('Gönderilemedi, biraz sonra yeniden dene.');
  };

  return (
    <article className="os-kart" aria-labelledby={`${s.id}-k`}>
      <div className="os-kart-ust">
        <span className="os-yuva">{/^\d+$/.test(s.yuva) ? `${s.yuva}. soru` : 'Numarasız'}</span>
        <span className={`os-guven ${g.cls}`} title={`Güven ${s.guven ?? 0}/100`}>{g.ad}</span>
        {s.brans && <span className="os-brans">{s.brans}</span>}
      </div>
      <p id={`${s.id}-k`} className="os-kok">{s.kok}</p>
      {s.belirsizlik && <p className="os-belirsiz">{s.belirsizlik}</p>}

      <ul className="os-siklar">
        {s.siklar.map((x) => {
          const dogru = x.harf === s.cevap;
          const cls = !cozuldu ? '' : dogru ? ' is-dogru' : x.harf === secim ? ' is-yanlis' : ' is-soluk';
          return (
            <li key={x.harf} className={`os-sik${cls}`}>
              <button type="button" disabled={cozuldu} aria-pressed={secim === x.harf} onClick={() => setSecim(x.harf)}>
                <span className="os-harf">{cozuldu && dogru ? <Check aria-hidden /> : cozuldu && x.harf === secim ? <X aria-hidden /> : x.harf}</span>
                <span className="os-sik-m">{x.metin}</span>
                <span className="os-kaynak" title={x.kaynak === 'ders' ? 'Şık ders kaynağından tamamlandı' : `${x.destek || 0} öğrenci bu şıkkı hatırladı`}>
                  {x.kaynak === 'ders' ? 'ders' : `öğrenci${x.destek ? ` · ${x.destek}` : ''}`}
                </span>
              </button>
              {cozuldu && x.aciklama && <p className="os-acik">{x.aciklama}</p>}
            </li>
          );
        })}
      </ul>

      {cozuldu && (
        <div className={`os-sonuc ${secim === s.cevap ? 'is-dogru' : 'is-yanlis'}`} role="status">
          {secim === s.cevap ? 'Doğru.' : `Yanlış. Öğrenci oylarına göre cevap ${s.cevap || 'belirsiz'}.`}
          {s.cevap_ders && s.cevap_ders !== s.cevap && <> Ders notuna göre cevap {s.cevap_ders}.</>}
          <button type="button" className="os-link" onClick={() => setSecim(null)}>Yeniden çöz</button>
        </div>
      )}

      {(bag || (s.benzer_cikmis && s.benzer_cikmis.length > 0)) && (
        <div className="os-baglar">
          {bag && <Bag url={bag.url} className="os-dug"><BookOpen aria-hidden /> {bag.ad}</Bag>}
          {(s.benzer_cikmis || []).slice(0, 3).map((id, i) => (
            <Bag key={id} url={`/cikmis/${encodeURIComponent(id)}`} className="os-dug">Benzer çıkmış {i + 1}</Bag>
          ))}
        </div>
      )}

      <div className="os-gb">
        {karar ? (
          <p className="os-gb-ok"><Check aria-hidden /> Geri bildirimin alındı: {karar === 'boyleydi' ? 'sınavdaki soru buydu' : karar === 'degildi' ? 'bu değildi' : 'düzeltme önerdin'}. Teşekkürler.</p>
        ) : (
          <>
            <span className="os-gb-l">Sınavdaki soru bu muydu?</span>
            <div className="os-gb-d">
              <button type="button" disabled={gonderiliyor} onClick={() => gonder('boyleydi')}><ThumbsUp aria-hidden /> Buydu</button>
              <button type="button" disabled={gonderiliyor} onClick={() => gonder('degildi')}><ThumbsDown aria-hidden /> Bu değildi</button>
              <button type="button" disabled={gonderiliyor} aria-expanded={duzelt} onClick={() => setDuzelt((d) => !d)}><MessageSquarePlus aria-hidden /> Düzeltme öner</button>
            </div>
          </>
        )}
        {duzelt && !karar && (
          <form className="os-duzelt" onSubmit={(e) => { e.preventDefault(); if (metin.trim() || cevabim) void gonder('duzeltme', { metin: metin.trim(), cevap: cevabim }); }}>
            <label>
              <span>Soru nasıldı? Hatırladığın farkı yaz</span>
              <textarea rows={3} value={metin} onChange={(e) => setMetin(e.target.value)} maxLength={2000} placeholder="Örneğin: kökte yaş 45 değil 62'ydi; D şıkkı farklıydı…" />
            </label>
            <div className="os-duzelt-alt">
              <label className="os-cevabim">
                <span>Benim cevabım</span>
                <select value={cevabim} onChange={(e) => setCevabim(e.target.value)}>
                  <option value="">Bilmiyorum</option>
                  {HARFLER.map((h) => <option key={h} value={h}>{h}</option>)}
                </select>
              </label>
              <button type="submit" className="os-dug is-ana" disabled={gonderiliyor || (!metin.trim() && !cevabim)}>Gönder</button>
            </div>
          </form>
        )}
        {hata && <p className="os-gb-hata" role="alert">{hata}</p>}
      </div>
    </article>
  );
};
