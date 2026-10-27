/**
 * Çevrimdışı merkezi › Dersler: her ders tek satır; sesli ders, ders paketi (.medspak), etkileşimli ders, soru çözücü, en önemliler
 * ve alternatif çözücü birlikte iner, birlikte denenir, birlikte silinir. Arama + branş + durum süzgeci, tek dokunuşla "tümünü test et".
 */
import { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle, Check, ChevronDown, CloudDownload, Download, ExternalLink, Loader2, RefreshCw, Search, ShieldCheck, Trash2, Wrench, X,
} from 'lucide-react';
import {
  kuyrugaEkle, paketDurumu, paketiDenetle, paketOnar, paketSil, secimAl, secimliBayt, useCevrimdisi, type DenetimSonuc, type Paket,
} from '../../services/cevrimdisi/paketMotoru';
import { birimDurumu, boyutYaz, dersBirimleri, katla, UYE_AD, type BirimDurum, type DersBirimi } from '../../services/cevrimdisi/dersBirimleri';
import { navigateTo } from '../../router';

type Suz = 'tum' | 'tam' | 'kismi' | 'yok' | 'guncelleme';
const SUZ_AD: Record<Suz, string> = { tum: 'Tümü', tam: 'Tam cihazda', kismi: 'Yarım kalan', yok: 'İndirilmedi', guncelleme: 'Güncelleme var' };
const DURUM_AD: Record<BirimDurum, string> = { tam: 'Tam cihazda', kismi: 'Kısmen', yok: 'İndirilmedi', iniyor: 'İniyor', guncelleme: 'Güncelleme var', hata: 'Hata' };
const SAYFA = 40;

/** Üyenin ilgili sayfası: çevrimdışı iken açılarak gerçek kullanımda denenir */
function uyeAdresi(p: Paket): string | null {
  const [m, a, b] = p.id.split(':');
  if (m === 'sesli') return `/canliders/${a}`;
  if (m === 'ogren') return `/ogren/${a}`;
  if (m === 'cozucu') return `/soru-cozucu?brans=${a}&ders=${b}`;
  if (m === 'onem') return `/en-onemliler?brans=${a}&ders=${b}`;
  if (m === 'alt') return `/alternatif-cozucu?ders=${a}`;
  return null;
}

export default function DersBirimleriPano() {
  const S = useCevrimdisi();
  const birimler = useMemo(() => dersBirimleri(S.katalog), [S.katalog]);
  const [ara, setAra] = useState('');
  const [grup, setGrup] = useState('');
  const [suz, setSuz] = useState<Suz>('tum');
  const [acik, setAcik] = useState<Record<string, boolean>>({});
  const [limit, setLimit] = useState(SAYFA);
  const [sonuclar, setSonuclar] = useState<Record<string, DenetimSonuc>>({});
  const [deniyor, setDeniyor] = useState<{ yapilan: number; toplam: number } | null>(null);

  const grupAdlari = useMemo(() => {
    const m = new Map<string, number>();
    birimler.forEach((b) => m.set(b.grup, (m.get(b.grup) || 0) + 1));
    return [...m.entries()].sort((a, b) => b[1] - a[1]);
  }, [birimler]);
  const durumlar = useMemo(() => {
    const m = new Map<string, ReturnType<typeof birimDurumu>>();
    birimler.forEach((b) => m.set(b.id, birimDurumu(b, S)));
    return m;
  }, [birimler, S]);

  const say = useMemo(() => {
    let tam = 0, kismi = 0, bayt = 0;
    durumlar.forEach((d) => { if (d.durum === 'tam' || d.durum === 'guncelleme') tam++; else if (d.durum === 'kismi' || d.durum === 'iniyor') kismi++; });
    Object.values(S.kayitlar).forEach((k) => { if (!k.yarim) bayt += k.bayt; });
    return { tam, kismi, bayt };
  }, [durumlar, S.kayitlar]);

  const liste = useMemo(() => {
    const q = katla(ara.trim());
    return birimler.filter((b) => {
      if (grup && b.grup !== grup) return false;
      if (q && !katla(`${b.baslik} ${b.grup} ${b.uyeler.map((u) => UYE_AD[u.modul]).join(' ')}`).includes(q)) return false;
      const d = durumlar.get(b.id)!.durum;
      if (suz === 'tam') return d === 'tam';
      if (suz === 'kismi') return d === 'kismi' || d === 'iniyor';
      if (suz === 'yok') return d === 'yok' || d === 'hata';
      if (suz === 'guncelleme') return d === 'guncelleme';
      return true;
    });
  }, [birimler, ara, grup, suz, durumlar]);
  useEffect(() => { setLimit(SAYFA); }, [ara, grup, suz]);

  const cihazdaki = (ids: string[]) => ids.filter((id) => ['tamam', 'guncelleme'].includes(paketDurumu(id, S)));
  async function sina(ids: string[]) {
    const hedef = cihazdaki(ids);
    if (!hedef.length) return;
    setDeniyor({ yapilan: 0, toplam: hedef.length });
    const yeni = { ...sonuclar };
    for (let i = 0; i < hedef.length; i++) {
      yeni[hedef[i]] = await paketiDenetle(hedef[i]);
      setSonuclar({ ...yeni });
      setDeniyor({ yapilan: i + 1, toplam: hedef.length });
    }
    setDeniyor(null);
  }
  const tumCihazIds = useMemo(() => Object.values(S.kayitlar).filter((k) => !k.yarim && k.id !== 'uygulama').map((k) => k.id), [S.kayitlar]);
  const sorunlu = Object.values(sonuclar).filter((x) => !x.ok && S.kayitlar[x.id]);
  const saglam = Object.values(sonuclar).filter((x) => x.ok).length;

  const indir = (b: DersBirimi) => {
    const ids = b.uyeler.filter((u) => ['yok', 'hata'].includes(paketDurumu(u.id, S))).map((u) => u.id);
    const gun = b.uyeler.filter((u) => paketDurumu(u.id, S) === 'guncelleme').map((u) => u.id);
    if (ids.length) kuyrugaEkle(ids);
    if (gun.length) kuyrugaEkle(gun, true);
  };

  return (
    <section className="cv-dersler" aria-label="Dersler">
      <div className="cv-ozet" role="status">
        <div><b>{say.tam}</b><small>ders tam cihazda</small></div>
        <div><b>{say.kismi}</b><small>kısmen inmiş</small></div>
        <div><b>{boyutYaz(say.bayt)}</b><small>cihazda</small></div>
        <div className="cv-ozet-eylem">
          <button type="button" className="cv-btn" disabled={!tumCihazIds.length || !!deniyor} onClick={() => void sina(tumCihazIds)}>
            {deniyor ? <Loader2 className="cv-don" aria-hidden="true" /> : <ShieldCheck aria-hidden="true" />}
            <span>{deniyor ? `Sınanıyor ${deniyor.yapilan}/${deniyor.toplam}` : 'İndirdiklerimi test et'}</span>
          </button>
        </div>
      </div>

      {(saglam > 0 || sorunlu.length > 0) && (
        <div className={`cv-serit${sorunlu.length ? ' is-hata' : ''}`} role="status">
          {sorunlu.length ? <AlertTriangle aria-hidden="true" /> : <Check aria-hidden="true" />}
          <span>{sorunlu.length ? `${sorunlu.length} pakette sorun var, ${saglam} paket sağlam.` : `Sınanan ${saglam} paketin hepsi sağlam: internetsiz açılır.`}</span>
          {sorunlu.length > 0 && <button type="button" className="cv-btn is-birincil" onClick={() => void paketOnar(sorunlu.map((x) => x.id))}><Wrench aria-hidden="true" /> <span>Hepsini onar</span></button>}
        </div>
      )}

      <div className="cv-arac">
        <label className="cv-ara">
          <Search aria-hidden="true" />
          <input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Ders ara (ad, branş, “sesli”…)" aria-label="Ders ara" />
          {ara && <button type="button" onClick={() => setAra('')} aria-label="Aramayı temizle"><X aria-hidden="true" /></button>}
        </label>
        <div className="cv-suz" role="group" aria-label="Durum süzgeci">
          {(Object.keys(SUZ_AD) as Suz[]).map((s) => (
            <button key={s} type="button" className={`cv-cip${suz === s ? ' is-on' : ''}`} aria-pressed={suz === s} onClick={() => setSuz(s)}>{SUZ_AD[s]}</button>
          ))}
        </div>
      </div>
      <div className="cv-brans" role="group" aria-label="Branş">
        <button type="button" className={`cv-cip${!grup ? ' is-on' : ''}`} aria-pressed={!grup} onClick={() => setGrup('')}>Tüm branşlar</button>
        {grupAdlari.map(([g, n]) => (
          <button key={g} type="button" className={`cv-cip${grup === g ? ' is-on' : ''}`} aria-pressed={grup === g} onClick={() => setGrup(grup === g ? '' : g)}>{g} <small>{n}</small></button>
        ))}
      </div>

      {!liste.length ? <div className="cv-bos">Bu süzgeçte ders yok.</div> : (
        <ul className="cv-dliste">
          {liste.slice(0, limit).map((b, i) => {
            const d = durumlar.get(b.id)!;
            const ac = !!acik[b.id];
            const sonuc = b.uyeler.map((u) => sonuclar[u.id]).filter(Boolean);
            const bozuk = sonuc.filter((x) => !x.ok);
            const oncekiGrup = i > 0 ? liste[i - 1].grup : '';
            return (
              <li key={b.id} className={`cv-ders is-${d.durum}`}>
                {!grup && oncekiGrup !== b.grup && <div className="cv-ders-grup">{b.grup}</div>}
                <div className="cv-ders-ust">
                  <button type="button" className="cv-ders-ad" aria-expanded={ac} onClick={() => setAcik({ ...acik, [b.id]: !ac })}>
                    <ChevronDown aria-hidden="true" className={ac ? '' : 'is-kapali'} />
                    <span>
                      <b>{b.no && b.uyeler.every((u) => u.modul !== 'ogren' || b.uyeler.length > 1) ? `${b.no}. ` : ''}{b.baslik}</b>
                      <small>
                        <em className={`cv-etiket is-d-${d.durum}`}>{DURUM_AD[d.durum]}</em>
                        {' '}{d.tamam}/{d.toplam} bölüm · {boyutYaz(d.durum === 'tam' ? d.toplamBayt : d.kalanBayt || d.toplamBayt)}{d.durum !== 'tam' && d.kalanBayt ? ' kalan' : ''}
                      </small>
                    </span>
                  </button>
                  <span className="cv-ders-eylem">
                    {d.durum !== 'tam' && d.durum !== 'iniyor' && (
                      <button type="button" className="cv-btn is-birincil" onClick={() => indir(b)}>
                        {d.durum === 'guncelleme' ? <RefreshCw aria-hidden="true" /> : <Download aria-hidden="true" />}
                        <span>{d.durum === 'guncelleme' ? 'Güncelle' : d.tamam ? 'Eksikleri indir' : 'Hepsini indir'}</span>
                        <em>{boyutYaz(d.kalanBayt)}</em>
                      </button>
                    )}
                    {d.durum === 'iniyor' && <span className="cv-etiket is-acc"><Loader2 className="cv-don" aria-hidden="true" /> iniyor</span>}
                    {d.tamam > 0 && (
                      <button type="button" className="cv-btn" disabled={!!deniyor} onClick={() => void sina(b.uyeler.map((u) => u.id))} title="Cihazdaki dosyaları ağsız denetle">
                        <ShieldCheck aria-hidden="true" /> <span>Test et</span>
                      </button>
                    )}
                  </span>
                </div>
                <div className="cv-uyeler" aria-label="Bu dersin bölümleri">
                  {b.uyeler.map((u) => {
                    const ud = paketDurumu(u.id, S);
                    const r = sonuclar[u.id];
                    return <span key={u.id} className={`cv-uye is-${ud}${r ? (r.ok ? ' is-sag' : ' is-boz') : ''}`} title={r?.ayrinti || ''}>
                      {r ? (r.ok ? <ShieldCheck aria-hidden="true" /> : <AlertTriangle aria-hidden="true" />) : ud === 'tamam' || ud === 'guncelleme' ? <Check aria-hidden="true" /> : ud === 'iniyor' ? <Loader2 className="cv-don" aria-hidden="true" /> : <CloudDownload aria-hidden="true" />}
                      {UYE_AD[u.modul]}
                    </span>;
                  })}
                </div>
                {bozuk.length > 0 && (
                  <div className="cv-serit is-hata" role="alert">
                    <AlertTriangle aria-hidden="true" />
                    <span>{bozuk.map((x) => `${UYE_AD[x.id.split(':')[0]] || x.ad}: ${x.ayrinti}`).join(' · ')}</span>
                    <button type="button" className="cv-btn is-birincil" onClick={() => void paketOnar(bozuk.map((x) => x.id))}><Wrench aria-hidden="true" /> <span>Onar</span></button>
                  </div>
                )}
                {ac && (
                  <ul className="cv-uye-liste">
                    {b.uyeler.map((u) => {
                      const ud = paketDurumu(u.id, S);
                      const adres = uyeAdresi(u);
                      const r = sonuclar[u.id];
                      const cihazda = ud === 'tamam' || ud === 'guncelleme';
                      return (
                        <li key={u.id}>
                          <span className="cv-uye-metin">
                            <b>{UYE_AD[u.modul]}</b>
                            <small>{u.alt || u.baslik} · {boyutYaz(cihazda ? S.kayitlar[u.id]?.bayt || secimliBayt(u, secimAl(u.id, S)) : secimliBayt(u, secimAl(u.id, S)))}{ud === 'guncelleme' ? ' · güncelleme var' : ''}{ud === 'hata' ? ` · ${S.hatalar[u.id] || 'hata'}` : ''}</small>
                            {r && <small className={r.ok ? 'cv-sag' : 'cv-hata'}>{r.ok ? '✓ ' : '✗ '}{r.ayrinti}</small>}
                          </span>
                          <span className="cv-satir-eylem">
                            {cihazda && u.modul === 'medspak' && (
                              <button type="button" className="cv-btn" onClick={() => window.dispatchEvent(new CustomEvent('cv-medspak-ac', { detail: u.id.slice('medspak:'.length) }))}>
                                <ExternalLink aria-hidden="true" /> <span>Paketi aç</span>
                              </button>
                            )}
                            {cihazda && adres && <button type="button" className="cv-btn" onClick={() => navigateTo(adres)}><ExternalLink aria-hidden="true" /> <span>Aç</span></button>}
                            {(ud === 'yok' || ud === 'hata') && <button type="button" className="cv-btn is-birincil" onClick={() => kuyrugaEkle([u.id])}><Download aria-hidden="true" /> <span>İndir</span></button>}
                            {cihazda && <button type="button" className="cv-btn is-sil" onClick={() => void paketSil([u.id])}><Trash2 aria-hidden="true" /> <span>Sil</span></button>}
                          </span>
                        </li>
                      );
                    })}
                    {d.tamam > 1 && <li><SilDugmesi ids={b.uyeler.filter((u) => ['tamam', 'guncelleme'].includes(paketDurumu(u.id, S))).map((u) => u.id)} /></li>}
                  </ul>
                )}
              </li>
            );
          })}
        </ul>
      )}
      {liste.length > limit && <button type="button" className="cv-btn cv-daha" onClick={() => setLimit(limit + SAYFA)}>Daha fazla göster ({liste.length - limit})</button>}
    </section>
  );
}

function SilDugmesi({ ids }: { ids: string[] }) {
  const [onay, setOnay] = useState(false);
  useEffect(() => {
    if (!onay) return;
    const t = window.setTimeout(() => setOnay(false), 3500);
    return () => window.clearTimeout(t);
  }, [onay]);
  return (
    <button type="button" className={`cv-btn is-sil${onay ? ' is-onay' : ''}`} onClick={() => (onay ? (setOnay(false), void paketSil(ids)) : setOnay(true))}>
      <Trash2 aria-hidden="true" /> <span>{onay ? 'Bu dersin hepsi silinsin mi?' : 'Dersin hepsini sil'}</span>
    </button>
  );
}
