import React, { useEffect, useMemo, useState } from 'react';
import { ArrowRight, BookOpenCheck, Check, ChevronRight, FileDown, FileText, GraduationCap, Headphones, Lightbulb, ListChecks, NotebookText, Tent, ThumbsDown, ThumbsUp, Timer, Volume2, X, Zap } from 'lucide-react';
import { icKonum } from '../../../siteHaritasi';
import { linkClick, navigateTo } from '../../../router';
import { useV15Baslik } from '../baslik';
import { KurulSecici, useSeciliKurul } from '../../kurul/KurulSecici';
import { KurulBos } from '../../kurul/KurulSuzgec';
import {
  EK_MODULLER, denemeKur, ekDenemeYaz, ekDinlendi, ekKurullar, ekModulYukle, ekSoruYaz, genelSorular, gorselUrl, konuSorulari, konulariAl, pdfKlip, useEkIlerleme,
  type EkModul, type SetSoru,
} from './ekVeri';
import { EkMd, Etkinlik, GECIS_KEY, OynatCubugu, dk, otoGecisAcik, useSira } from './ekOrtak';
import { HocaSetCoz, HocaSetler } from './EkHoca';
import { FoyKonu, FoyListe } from './EkFoy';
import { EkPdfDers } from './EkPdfDers';
import '../../../styles/v15/ekmodul.css';

/**
 * v15 · Ek modüller (/dersler/ek-moduller/kurul<N>/<modül>/<bölüm>/<konu>; iç /ek-moduller/<modül>?kurul=&b=&konu=).
 * Kurul müfredatı dışındaki seçmeli/geçici dersler. Her modülde üç anlatıcı (sesli ders, spot bilgiler, sınav öncesi) +
 * sesli çözümlü sorular (konu soruları: yalnız o konuya kadar öğretilenler; genel tekrar; sınav denemesi) + PDF kitapçıkları.
 * Ekranda not biçimi (`ekran`) durur; EMA ayrı yazılmış konuşma metnini (`ses`) okur — okuma metni ekranda gösterilmez.
 */
type Bolum = '' | 'ders' | 'spot' | 'sinav-oncesi' | 'sorular' | 'hoca' | 'foy';
interface Adres { kurul: number | null; modul: string | null; b: Bolum; konu: string | null }

const oku = (): Adres => {
  const k = icKonum();
  const sp = new URLSearchParams(k.search);
  const n = Number(sp.get('kurul'));
  let modul: string | null = null;
  try { modul = decodeURIComponent(k.pathname.split('/')[2] || '') || null; } catch { /* bozuk adres */ }
  return { kurul: Number.isInteger(n) && n >= 1 && n <= 6 ? n : null, modul, b: (sp.get('b') || '') as Bolum, konu: sp.get('konu') };
};
const adres = (kurul: number, modul?: string, b?: Bolum, konu?: string | null) =>
  `/dersler/ek-moduller/kurul${kurul}${modul ? `/${modul}` : ''}${modul && b ? `/${b}` : ''}${modul && b && konu ? `/${konu}` : ''}`;
const Bag: React.FC<{ to: string; className?: string; children: React.ReactNode; 'aria-label'?: string }> = ({ to, children, ...p }) => (
  <a href={to} onClick={linkClick(() => navigateTo(to))} {...p}>{children}</a>
);

export default function EkModullerV15() {
  const [a, setA] = useState(oku);
  useEffect(() => {
    const f = () => setA(oku());
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  const seciliKurul = useSeciliKurul();
  const ozet = a.modul ? EK_MODULLER.find((m) => m.id === a.modul) : null;
  if (a.modul && ozet) return <Modul key={ozet.id} id={ozet.id} a={a} />;
  // modülsüz adres: adresteki kurul, yoksa seçili kurul; o kurulda modül yoksa içeriği olan kurul
  const kurul = a.kurul ?? (ekKurullar().includes(seciliKurul) ? seciliKurul : ekKurullar()[0] ?? seciliKurul);
  return <Liste kurul={kurul} bulunamadi={!!a.modul} />;
}

/* ——— modül listesi ——— */
const Liste: React.FC<{ kurul: number; bulunamadi: boolean }> = ({ kurul, bulunamadi }) => {
  useV15Baslik({ baslik: 'Ek modüller', alt: 'Seçmeli ve geçici dersler' });
  const liste = EK_MODULLER.filter((m) => m.kurul === kurul);
  return (
    <div className="ekm">
      <KurulSecici secili={kurul} yol={(k) => adres(k)} icerik={(k) => ekKurullar().includes(k)} />
      <p className="ekm-giris v15-card"><Tent aria-hidden />
        <span>Kurul derslerinin dışında kalan <b>seçmeli ve geçici dersler</b> burada toplanır. Her modülde sesli ders, spot bilgiler,
          sınav öncesi tekrar ve sesli çözümlü sorular bulunur; hepsi PDF olarak da indirilebilir.</span>
      </p>
      {bulunamadi && <p className="ekm-bos v15-card">Aradığın modül bulunamadı; bu kurulun modülleri aşağıda.</p>}
      {!liste.length ? (
        <KurulBos kurul={kurul} ne="ek modül" onTumu={ekKurullar().length ? () => navigateTo(adres(ekKurullar()[0])) : undefined} tumuEtiket={`Kurul ${ekKurullar()[0]} modüllerine git`} />
      ) : (
        <ul className="ekm-kartlar" role="list">
          {liste.map((m) => (
            <li key={m.id}>
              <Bag to={adres(m.kurul, m.id)} className="ekm-kart v15-card">
                <img src={gorselUrl(m.id, m.kapak)} alt="" loading="lazy" />
                <span className="ekm-tur">{m.tur}</span>
                <b>{m.ad}</b>
                <span className="ekm-kart-ack">{m.aciklama}</span>
                <span className="ekm-kart-git">Modülü aç <ArrowRight aria-hidden /></span>
              </Bag>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

/* ——— modül ——— */
const Modul: React.FC<{ id: string; a: Adres }> = ({ id, a }) => {
  const [m, setM] = useState<EkModul | null | undefined>(undefined);
  useEffect(() => { let canli = true; ekModulYukle(id).then((x) => canli && setM(x), () => canli && setM(null)); return () => { canli = false; }; }, [id]);
  useEffect(() => { window.scrollTo?.(0, 0); }, [a.b, a.konu]);
  if (m === undefined) return <div className="ekm"><span className="v15-skel ekm-skel" aria-hidden /></div>;
  if (!m) return <div className="ekm"><p className="ekm-bos v15-card">Modül yüklenemedi.</p></div>;
  const kurul = m.ozet.kurul;
  const ana = adres(kurul, id);
  const konular = konulariAl(m);
  const konu = a.konu ? konular.find((k) => k.id === a.konu) : null;
  if (a.b === 'ders' && konu) return <Ders key={konu.id} m={m} konuId={konu.id} />;
  if (a.b === 'spot') return <Spot key={a.konu || 'hepsi'} m={m} konuId={konu?.id || null} />;
  if (a.b === 'sinav-oncesi' && m.sinavOncesi) return <SinavOncesi m={m} />;
  if (a.b === 'sorular' && (konu || a.konu === 'genel' || a.konu === 'deneme')) return <Sorular key={a.konu} m={m} set={a.konu as string} />;
  if (a.b === 'hoca' && m.hoca) {
    const set = m.hoca.setler.find((s) => s.id === a.konu);
    return set ? <HocaSayfa key={set.id} m={m} setId={set.id} /> : <HocaSayfa m={m} setId={null} />;
  }
  if (a.b === 'foy' && m.foy) return <FoySayfa key={konu?.id || 'liste'} m={m} konuId={konu?.id || null} />;
  return <ModulAna m={m} ana={ana} />;
};

const ModulAna: React.FC<{ m: EkModul; ana: string }> = ({ m, ana }) => {
  const { ozet } = m;
  useV15Baslik({ baslik: ozet.ad, alt: `${ozet.tur} · Kurul ${ozet.kurul}`, geri: adres(ozet.kurul) });
  const il = useEkIlerleme(ozet.id);
  const konular = konulariAl(m);
  const soruN = konular.reduce((t, k) => t + k.sorular.length, 0) + m.genel.length;
  const cozulen = Object.keys(il.soru).length, dogru = Object.values(il.soru).filter(Boolean).length;
  const dersSure = Object.entries(m.klip).filter(([k]) => k.startsWith('d-')).reduce((t, [, v]) => t + v.sure, 0);
  const sonDeneme = il.deneme?.[il.deneme.length - 1];
  const ilkKonu = konular.find((k) => !il.dinlenen[`d-${k.id}`]) || konular[0];
  return (
    <div className="ekm">
      <header className="ekm-kapak v15-card">
        <img src={gorselUrl(ozet.id, ozet.kapak)} alt="" />
        <div>
          <span className="ekm-tur">{ozet.tur} · Kurul {ozet.kurul}</span>
          <h1>{ozet.ad}</h1>
          <p>{ozet.aciklama}</p>
          <ul className="ekm-sayac" role="list">
            <li><b>{m.basliklar.length}</b> başlık</li>
            <li><b>{konular.length}</b> konu</li>
            <li><b>{soruN}</b> soru</li>
            {dersSure > 0 && <li><b>{dk(dersSure)}</b> sesli ders</li>}
          </ul>
        </div>
      </header>

      <section className="ekm-modlar" aria-label="Çalışma biçimleri">
        {ilkKonu && (
          <Bag to={`${ana}/ders/${ilkKonu.id}`} className="ekm-mod v15-card is-ders">
            <Headphones aria-hidden /><b>Sesli ders</b>
            <span>Konuyu baştan sona dinle; ders kitapçığı sesle birlikte ilerler, anlatılan satır PDF'te işaretlenir.</span>
            <i>{Object.keys(il.dinlenen).filter((k) => k.startsWith('d-')).length} / {konular.length} konu dinlendi</i>
          </Bag>
        )}
        <Bag to={`${ana}/spot`} className="ekm-mod v15-card is-spot">
          <Zap aria-hidden /><b>Spot bilgiler</b>
          <span>Her konunun en akılda kalması gereken tek cümlelik bilgileri art arda okunur.</span>
          <i>{konular.reduce((t, k) => t + k.spotlar.length, 0)} spot</i>
        </Bag>
        {m.sinavOncesi && (
          <Bag to={`${ana}/sinav-oncesi`} className="ekm-mod v15-card is-sinav">
            <GraduationCap aria-hidden /><b>Sınav öncesi</b>
            <span>Bütün dersin son tekrarı: başlık başlık en çok sorulabilecek bilgiler.</span>
            <i>{m.sinavOncesi.partlar.length} bölüm</i>
          </Bag>
        )}
        <Bag to={`${ana}/sorular/deneme`} className="ekm-mod v15-card is-soru">
          <Timer aria-hidden /><b>Sınav denemesi</b>
          <span>Sınavdaki gibi {ozet.sinavSoru} soru; her açılışta {soruN} soruluk havuzdan yeniden seçilir.</span>
          <i>{sonDeneme ? `Son deneme: ${sonDeneme.puan} / ${sonDeneme.n}` : cozulen ? `${cozulen} soru çözüldü · ${dogru} doğru` : 'Sesli çözümlü'}</i>
        </Bag>
      </section>

      <section aria-label="Konular">
        <h2 className="ekm-h2">Konular</h2>
        <ol className="ekm-basliklar" role="list">
          {m.basliklar.map((b) => (
            <li key={b.no} className="v15-card">
              <div className="ekm-baslik-ust"><i>{b.no}</i><div><b>{b.baslik}</b><span>{b.ozet}</span></div></div>
              <ul role="list">
                {b.konular.map((k) => {
                  const cz = k.sorular.filter((q) => il.soru[`${k.id}-${q.no}`] !== undefined).length;
                  return (
                    <li key={k.id} className="ekm-konu">
                      <Bag to={`${ana}/ders/${k.id}`} className="ekm-konu-ad">
                        {il.dinlenen[`d-${k.id}`] ? <Check aria-hidden className="is-ok" /> : <Headphones aria-hidden />}
                        <span><b>{k.baslik}</b><small>{k.ozet}</small></span>
                      </Bag>
                      <div className="ekm-konu-git">
                        <Bag to={`${ana}/spot/${k.id}`} aria-label={`${k.baslik}: spot bilgiler`}><Zap aria-hidden /> Spot</Bag>
                        <Bag to={`${ana}/sorular/${k.id}`} aria-label={`${k.baslik}: sorular`}><ListChecks aria-hidden /> {cz ? `${cz}/${k.sorular.length}` : `${k.sorular.length} soru`}</Bag>
                      </div>
                    </li>
                  );
                })}
              </ul>
            </li>
          ))}
        </ol>
      </section>

      {m.foy && (
        <Bag to={`${ana}/foy`} className="ekm-genel v15-card is-foy">
          <FileDown aria-hidden />
          <span><b>Çalışma föyü</b><small>Hocanın çalışma soruları konu konu: bilgi özeti, boşluk doldurma, doğru–yanlış, çoktan seçmeli. Seçtiğin konuların föyü PDF olur.</small></span>
          <ChevronRight aria-hidden />
        </Bag>
      )}
      {m.hoca && (
        <Bag to={`${ana}/hoca`} className="ekm-genel v15-card is-hoca">
          <BookOpenCheck aria-hidden />
          <span><b>Hocanın çalışma soruları</b><small>{m.hoca.setler.reduce((t, s) => t + s.sorular.length, 0)} soru: boşluk doldurma, doğru–yanlış, çoktan seçmeli. İçerik bu sorulara göre hazırlandı.</small></span>
          <ChevronRight aria-hidden />
        </Bag>
      )}
      {m.genel.length > 0 && (
        <Bag to={`${ana}/sorular/genel`} className="ekm-genel v15-card">
          <BookOpenCheck aria-hidden />
          <span><b>Genel tekrar soruları</b><small>Bütün konuları birlikte yoklayan {m.genel.length} soru; sınavdan önce çöz.</small></span>
          <ChevronRight aria-hidden />
        </Bag>
      )}

      <section aria-label="PDF indir">
        <h2 className="ekm-h2">PDF olarak indir</h2>
        <ul className="ekm-pdfler" role="list">
          {ozet.pdf.map((p) => (
            <li key={p.id}>
              <a className="ekm-pdf v15-card" href={gorselUrl(ozet.id, p.dosya)} download target="_blank" rel="noreferrer">
                <FileDown aria-hidden /><span><b>{p.ad}</b><small>{p.aciklama}</small></span>
              </a>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};

/* ——— çalışma föyü ——— */
const FoySayfa: React.FC<{ m: EkModul; konuId: string | null }> = ({ m, konuId }) => {
  const ana = adres(m.ozet.kurul, m.ozet.id);
  const konu = konuId ? konulariAl(m).find((k) => k.id === konuId) : null;
  useV15Baslik({ baslik: konu ? konu.baslik : 'Çalışma föyü', alt: konu ? 'Çalışma föyü' : m.ozet.ad, geri: konu ? `${ana}/foy` : ana });
  if (konu) return <FoyKonu m={m} konuId={konu.id} />;
  return (
    <div className="ekm">
      <p className="ekm-giris v15-card"><BookOpenCheck aria-hidden />
        <span><b>Çalışma soruları konu konu düzenlendi.</b> Her konuda önce bilmen gerekenleri oku, sonra boşlukları doldur, doğru–yanlışları işaretle,
          soruları çöz. İstediğin konuları seçip föyü PDF olarak da indirebilirsin.</span>
      </p>
      <FoyListe m={m} ac={(id) => navigateTo(`${ana}/foy/${id}`)} />
    </div>
  );
};

/* ——— hocanın çalışma soruları ——— */
const HocaSayfa: React.FC<{ m: EkModul; setId: string | null }> = ({ m, setId }) => {
  const ana = adres(m.ozet.kurul, m.ozet.id);
  const set = m.hoca!.setler.find((s) => s.id === setId) || null;
  useV15Baslik({ baslik: set ? set.ad : 'Hocanın çalışma soruları', alt: set ? 'Hocanın çalışma soruları' : m.ozet.ad, geri: set ? `${ana}/hoca` : ana });
  if (set) return <HocaSetCoz set={set} m={m} />;
  return (
    <div className="ekm">
      <p className="ekm-giris v15-card"><BookOpenCheck aria-hidden />
        <span><b>{m.hoca!.kaynak}.</b> Sorular ve cevaplar hocanın yazdığı gibidir; dersin anlatımı ve diğer sorular bu sorulardaki bilgilere göre hazırlandı.</span>
      </p>
      <HocaSetler m={m} ac={(id) => navigateTo(`${ana}/hoca/${id}`)} />
    </div>
  );
};

/* ——— sesli ders ——— */
// Notlar: bölüm kartları (ilk biçim) · PDF ile: ders kitapçığı sesle birlikte ilerler (klasik sesli ders gibi). Seçim cihazda kalır.
const KIP_KEY = 'medsoru_ek_modul_ders_kip';
const OTO_BASLA = 'medsoru_ek_modul_oto_basla';
type DersKip = 'not' | 'pdf';

const Ders: React.FC<{ m: EkModul; konuId: string }> = ({ m, konuId }) => {
  const konular = konulariAl(m);
  const sira0 = konular.findIndex((k) => k.id === konuId);
  const konu = konular[sira0];
  const ana = adres(m.ozet.kurul, m.ozet.id);
  useV15Baslik({ baslik: konu.baslik, alt: `${konu.baslikNo}. ${konu.baslikAd}`, geri: ana });
  const klipler = useMemo(() => konu.bolumler.map((_, i) => `d-${konu.id}-${i + 1}`), [konu]);
  const sonraki = konular[sira0 + 1];
  const [gecis, setGecis] = useState(otoGecisAcik);
  const gecisDegis = (v: boolean) => { setGecis(v); try { localStorage.setItem(GECIS_KEY, v ? '1' : '0'); } catch { /* yok */ } };
  // konu bitince (ayar açıksa) sonraki konuya geçilir ve ses aynı ortak öğeden sürer — arka planda da
  const sira = useSira(m, klipler, () => {
    ekDinlendi(m.ozet.id, `d-${konu.id}`);
    if (!sonraki || !otoGecisAcik()) return;
    try { sessionStorage.setItem(OTO_BASLA, sonraki.id); } catch { /* yok */ }
    navigateTo(`${ana}/ders/${sonraki.id}`);
  }, (i) => `${konu.baslik} · ${konu.bolumler[i]?.baslik || ''}`);
  useEffect(() => {
    let bekleyen: string | null = null;
    try { bekleyen = sessionStorage.getItem(OTO_BASLA); } catch { /* yok */ }
    if (bekleyen !== konu.id) return;
    try { sessionStorage.removeItem(OTO_BASLA); } catch { /* yok */ }
    sira.cal(0);
  }, [konu.id]); // eslint-disable-line react-hooks/exhaustive-deps
  const pdfVar = useMemo(() => klipler.some((k) => pdfKlip(m, k)), [m, klipler]);
  const [kipSec, setKipSec] = useState<DersKip>(() => { try { return localStorage.getItem(KIP_KEY) === 'not' ? 'not' : 'pdf'; } catch { return 'pdf'; } });
  const kip: DersKip = pdfVar ? kipSec : 'not';
  const kipDegis = (k: DersKip) => { setKipSec(k); try { localStorage.setItem(KIP_KEY, k); } catch { /* yok */ } };
  useEffect(() => {
    if (sira.i < 0 || kip === 'pdf') return;
    document.getElementById(`ekm-b-${sira.i}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, [sira.i, kip]);
  return (
    <div className={`ekm ekm-ders${kip === 'pdf' ? ' ekm-pdfkip' : ''}`}>
      <OynatCubugu sira={sira} n={klipler.length} etiket="Dersi dinle" birim="Bölüm" gecis={sonraki ? { acik: gecis, degis: gecisDegis } : undefined} />
      {pdfVar && (
        <div className="ekm-kip" role="group" aria-label="Ders görünümü">
          <button type="button" className={kip === 'pdf' ? 'is-on' : ''} aria-pressed={kip === 'pdf'} onClick={() => kipDegis('pdf')}><FileText aria-hidden /> PDF ile</button>
          <button type="button" className={kip === 'not' ? 'is-on' : ''} aria-pressed={kip === 'not'} onClick={() => kipDegis('not')}><NotebookText aria-hidden /> Notlar</button>
        </div>
      )}
      {kip === 'pdf' ? <EkPdfDers m={m} konu={konu} klipler={klipler} sira={sira} /> : (<>
      <figure className="ekm-gorsel v15-card">
        <img src={gorselUrl(m.ozet.id, konu.gorsel)} alt={konu.gorsel_alt} />
        <figcaption>{konu.ozet}</figcaption>
      </figure>
      <ol className="ekm-bolumler" role="list">
        {konu.bolumler.map((b, i) => (
          <li key={i} id={`ekm-b-${i}`} className={`v15-card${sira.i === i ? ' is-aktif' : ''}`}>
            <div className="ekm-bolum-ust">
              <i>{i + 1}</i><h3>{b.baslik}</h3>
              {sira.sesVar && (
                <button type="button" className="ekm-kucuk" onClick={() => (sira.i === i ? sira.dugme() : sira.cal(i))} aria-label={`${b.baslik}: buradan dinle`}>
                  <Volume2 aria-hidden />
                </button>
              )}
            </div>
            <EkMd md={b.ekran} />
          </li>
        ))}
      </ol>

      {(konu.ek_gorseller || []).map((g) => (
        <figure key={g.dosya} className="ekm-gorsel v15-card"><img src={gorselUrl(m.ozet.id, g.dosya)} alt={g.alt} loading="lazy" /><figcaption>{g.alt}</figcaption></figure>
      ))}
      <section className="ekm-akilda v15-card">
        <Lightbulb aria-hidden />
        <div><span className="ekm-kod">{konu.akilda.kod}</span><b>{konu.akilda.acilim}</b><p>{konu.akilda.not}</p></div>
      </section>
      <section className="ekm-yy">
        <div className="v15-card is-yap"><h3><ThumbsUp aria-hidden /> Yap</h3><ul>{konu.yap.map((x) => <li key={x}>{x}</li>)}</ul></div>
        <div className="v15-card is-yapma"><h3><ThumbsDown aria-hidden /> Yapma</h3><ul>{konu.yapma.map((x) => <li key={x}>{x}</li>)}</ul></div>
      </section>
      </>)}

      <h2 className="ekm-h2">Pekiştir</h2>
      {konu.etkinlikler.map((e, i) => <Etkinlik key={i} e={e} />)}

      <nav className="ekm-sonra" aria-label="Sıradaki adım">
        <Bag to={`${ana}/spot/${konu.id}`} className="v15-btn is-ghost"><Zap aria-hidden /> Spotları dinle</Bag>
        <Bag to={`${ana}/sorular/${konu.id}`} className="v15-btn"><ListChecks aria-hidden /> {konu.sorular.length} soruyu çöz</Bag>
        {sonraki && <Bag to={`${ana}/ders/${sonraki.id}`} className="v15-btn is-ghost">Sonraki konu: {sonraki.baslik} <ArrowRight aria-hidden /></Bag>}
      </nav>
    </div>
  );
};

/* ——— spot anlatıcı ——— */
const Spot: React.FC<{ m: EkModul; konuId: string | null }> = ({ m, konuId }) => {
  const ana = adres(m.ozet.kurul, m.ozet.id);
  const konular = konulariAl(m).filter((k) => !konuId || k.id === konuId);
  useV15Baslik({ baslik: 'Spot bilgiler', alt: konuId ? konular[0]?.baslik : m.ozet.ad, geri: ana });
  const duz = useMemo(() => konular.flatMap((k) => k.spotlar.map((s, i) => ({ ...s, klip: `s-${k.id}-${i + 1}`, konu: k }))), [m, konuId]); // eslint-disable-line react-hooks/exhaustive-deps
  const sira = useSira(m, duz.map((s) => s.klip), () => konular.forEach((k) => ekDinlendi(m.ozet.id, `s-${k.id}`)));
  useEffect(() => {
    if (sira.i >= 0) document.getElementById(`ekm-s-${sira.i}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, [sira.i]);
  let n = -1;
  return (
    <div className="ekm ekm-spot">
      <OynatCubugu sira={sira} n={duz.length} etiket="Spotları dinle" birim="Spot" />
      {konular.map((k) => (
        <section key={k.id} className="ekm-spot-grup">
          <h2 className="ekm-h2"><span>{k.baslikNo}. {k.baslikAd}</span>{k.baslik}</h2>
          <ol role="list">
            {k.spotlar.map((s) => {
              n += 1;
              const no = n;
              return (
                <li key={no} id={`ekm-s-${no}`} className={`v15-card${sira.i === no ? ' is-aktif' : ''}`}>
                  <button type="button" onClick={() => (sira.i === no ? sira.dugme() : sira.cal(no))} disabled={!sira.sesVar} aria-label="Bu spottan dinle"><Zap aria-hidden /></button>
                  <EkMd md={s.metin} />
                </li>
              );
            })}
          </ol>
          {konuId && <nav className="ekm-sonra"><Bag to={`${ana}/sorular/${k.id}`} className="v15-btn"><ListChecks aria-hidden /> Bu konunun sorularını çöz</Bag></nav>}
        </section>
      ))}
    </div>
  );
};

/* ——— sınav öncesi anlatıcı ——— */
const SinavOncesi: React.FC<{ m: EkModul }> = ({ m }) => {
  const ana = adres(m.ozet.kurul, m.ozet.id);
  const so = m.sinavOncesi!;
  useV15Baslik({ baslik: 'Sınav öncesi tekrar', alt: m.ozet.ad, geri: ana });
  const sira = useSira(m, so.partlar.map((_, i) => `o-${i + 1}`), () => ekDinlendi(m.ozet.id, 'o'));
  useEffect(() => {
    if (sira.i >= 0) document.getElementById(`ekm-o-${sira.i}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, [sira.i]);
  return (
    <div className="ekm ekm-ders">
      <OynatCubugu sira={sira} n={so.partlar.length} etiket="Son tekrarı dinle" birim="Bölüm" />
      {so.giris && <p className="ekm-giris v15-card"><GraduationCap aria-hidden /><span>{so.giris}</span></p>}
      <ol className="ekm-bolumler" role="list">
        {so.partlar.map((p, i) => (
          <li key={i} id={`ekm-o-${i}`} className={`v15-card${sira.i === i ? ' is-aktif' : ''}`}>
            <div className="ekm-bolum-ust">
              <i>{i + 1}</i><h3>{p.baslik.replace(/^\d+\.\s*/, '')}</h3>
              {sira.sesVar && <button type="button" className="ekm-kucuk" onClick={() => (sira.i === i ? sira.dugme() : sira.cal(i))} aria-label={`${p.baslik}: buradan dinle`}><Volume2 aria-hidden /></button>}
            </div>
            <EkMd md={p.ekran} />
          </li>
        ))}
      </ol>
      <nav className="ekm-sonra">
        <Bag to={`${ana}/sorular/genel`} className="v15-btn is-ghost"><BookOpenCheck aria-hidden /> Genel tekrar soruları</Bag>
        <Bag to={`${ana}/sorular/deneme`} className="v15-btn"><Timer aria-hidden /> {m.ozet.sinavSoru} soruluk deneme</Bag>
      </nav>
    </div>
  );
};

/* ——— sorular: konu seti / genel tekrar (anında açıklama) · deneme (sonunda sonuç) ——— */
const HARF = ['A', 'B', 'C', 'D', 'E'];
const OTO_KEY = 'medsoru_ek_modul_oto_ses';

const Sorular: React.FC<{ m: EkModul; set: string }> = ({ m, set }) => {
  const ana = adres(m.ozet.kurul, m.ozet.id);
  const deneme = set === 'deneme';
  const [tur, setTur] = useState(0);
  const sorular = useMemo<SetSoru[]>(() => (deneme ? denemeKur(m) : set === 'genel' ? genelSorular(m) : konuSorulari(m, set)), [m, set, deneme, tur]); // eslint-disable-line react-hooks/exhaustive-deps
  const konu = konulariAl(m).find((k) => k.id === set);
  const ad = deneme ? 'Sınav denemesi' : set === 'genel' ? 'Genel tekrar soruları' : 'Konu soruları';
  useV15Baslik({ baslik: ad, alt: konu ? konu.baslik : m.ozet.ad, geri: ana });
  const [i, setI] = useState(0);
  const [secim, setSecim] = useState<Record<number, string>>({});
  const [bitti, setBitti] = useState(false);
  const [oto, setOto] = useState(() => { try { return localStorage.getItem(OTO_KEY) !== '0'; } catch { return true; } });
  const q = sorular[i];
  const [klipler, setKlipler] = useState<string[]>([]);
  const sira = useSira(m, klipler);
  // klip listesi değişince çal (soru okuma / çözüm): useSira listeyi durum.ref'ten okur, bir sonraki turda başlatılır
  const [calIstek, setCalIstek] = useState(0);
  useEffect(() => { if (calIstek) sira.cal(0); }, [calIstek]); // eslint-disable-line react-hooks/exhaustive-deps
  const dinle = (k: string[]) => { setKlipler(k); setCalIstek((x) => x + 1); };

  if (!sorular.length) return <div className="ekm"><p className="ekm-bos v15-card">Bu sette soru yok.</p></div>;
  const sec = (h: string) => {
    if (secim[i] !== undefined && !deneme) return;
    setSecim({ ...secim, [i]: h });
    if (deneme) return;
    ekSoruYaz(m.ozet.id, q.anahtar, h === q.dogru);
    if (oto) dinle([q.cKlip]);
  };
  const git = (n: number) => { sira.durdur(); setI(n); window.scrollTo?.(0, 0); };
  const bitir = () => {
    sira.durdur();
    const dogru = sorular.filter((s, n) => secim[n] === s.dogru).length;
    if (deneme) { ekDenemeYaz(m.ozet.id, dogru, sorular.length); sorular.forEach((s, n) => secim[n] !== undefined && ekSoruYaz(m.ozet.id, s.anahtar, secim[n] === s.dogru)); }
    setBitti(true);
    window.scrollTo?.(0, 0);
  };
  const yeniden = () => { sira.durdur(); setSecim({}); setI(0); setBitti(false); setTur((t) => t + 1); };
  const otoDegis = () => { const y = !oto; setOto(y); try { localStorage.setItem(OTO_KEY, y ? '1' : '0'); } catch { /* yok */ } if (!y) sira.durdur(); };

  if (bitti) {
    const dogru = sorular.filter((s, n) => secim[n] === s.dogru).length;
    return (
      <div className="ekm ekm-soru">
        <section className="ekm-puan v15-card">
          <b>{dogru} / {sorular.length}</b>
          <span>{dogru >= sorular.length * 0.85 ? 'Çok iyi; sınava hazırsın.' : dogru >= sorular.length * 0.6 ? 'İyi gidiyor; yanlışlarının açıklamalarını oku.' : 'Yanlış yaptığın konuların dersini bir kez daha dinle.'}</span>
          <div className="ekm-sonra">
            <button type="button" className="v15-btn" onClick={yeniden}>{deneme ? 'Yeni deneme' : 'Baştan çöz'}</button>
            <Bag to={ana} className="v15-btn is-ghost">Modüle dön</Bag>
          </div>
        </section>
        <ol className="ekm-inceleme" role="list">
          {sorular.map((s, n) => (
            <li key={s.anahtar} className={`v15-card ${secim[n] === s.dogru ? 'is-ok' : 'is-bad'}`}>
              <p className="ekm-kok"><i>{n + 1}</i>{s.kok}</p>
              <p className="ekm-inc-cvp">
                {secim[n] === undefined ? 'Boş bırakıldı. ' : secim[n] !== s.dogru ? <>Senin cevabın: <b>{secim[n]}) {s.secenekler[secim[n]]}</b> · </> : null}
                Doğru cevap: <b>{s.dogru}) {s.secenekler[s.dogru]}</b>
              </p>
              <p className="ekm-cozum">{s.cozum}</p>
              {secim[n] !== undefined && secim[n] !== s.dogru && <p className="ekm-sik-ack">{s.siklar[secim[n]]}</p>}
              {m.klip[s.cKlip] && <button type="button" className="v15-btn is-ghost ekm-dinle" onClick={() => dinle([s.cKlip])}><Volume2 aria-hidden /> Çözümü dinle</button>}
            </li>
          ))}
        </ol>
      </div>
    );
  }

  const yanit = secim[i];
  const acik = yanit !== undefined && !deneme;
  const son = i === sorular.length - 1;
  const cozulen = Object.keys(secim).length;
  return (
    <div className="ekm ekm-soru">
      <div className="ekm-soru-ust">
        <span><b>{i + 1}</b> / {sorular.length}</span>
        <div className="ekm-ilerle" aria-hidden><i style={{ width: `${(cozulen / sorular.length) * 100}%` }} /></div>
        <span className={`ekm-zorluk is-${q.zorluk}`}>{q.zorluk}</span>
        {!deneme && (
          <button type="button" className={`ekm-kucuk is-oto${oto ? ' is-on' : ''}`} onClick={otoDegis} aria-pressed={oto} title="Cevaptan sonra çözümü sesli anlat">
            <Volume2 aria-hidden /> Sesli çözüm
          </button>
        )}
      </div>
      <article className="ekm-soru-kart v15-card">
        <p className="ekm-kok">{q.kok}</p>
        {m.klip[q.qKlip] && (
          <button type="button" className="v15-btn is-ghost ekm-dinle" onClick={() => (sira.caliyor ? sira.durdur() : dinle([q.qKlip]))}>
            <Volume2 aria-hidden /> {sira.caliyor && klipler[0] === q.qKlip ? 'Durdur' : 'Soruyu dinle'}
          </button>
        )}
        <ul className="ekm-secenekler" role="list">
          {HARF.map((h) => {
            const d = acik ? (h === q.dogru ? ' is-ok' : h === yanit ? ' is-bad' : ' is-sonuk') : yanit === h ? ' is-sec' : '';
            return (
              <li key={h}>
                <button type="button" className={`ekm-secenek${d}`} onClick={() => sec(h)} disabled={acik}>
                  <i>{acik && h === q.dogru ? <Check aria-hidden /> : acik && h === yanit ? <X aria-hidden /> : h}</i><span>{q.secenekler[h]}</span>
                </button>
                {acik && <p className="ekm-sik-ack">{q.siklar[h]}</p>}
              </li>
            );
          })}
        </ul>
        {acik && (
          <div className={`ekm-sonuc ${yanit === q.dogru ? 'is-ok' : 'is-bad'}`}>
            <p><b>{yanit === q.dogru ? 'Doğru.' : `Yanlış. Doğru cevap ${q.dogru}.`}</b> {q.cozum}</p>
            {m.klip[q.cKlip] && (
              <button type="button" className="v15-btn is-ghost ekm-dinle" onClick={() => (sira.caliyor ? sira.durdur() : dinle([q.cKlip]))}>
                <Volume2 aria-hidden /> {sira.caliyor ? 'Durdur' : 'Çözümü dinle'}
              </button>
            )}
          </div>
        )}
      </article>
      <nav className="ekm-soru-alt">
        <button type="button" className="v15-btn is-ghost" onClick={() => git(i - 1)} disabled={i === 0}>Önceki</button>
        {son
          ? <button type="button" className="v15-btn" onClick={bitir} disabled={!cozulen}>{deneme ? 'Denemeyi bitir' : 'Sonucu gör'}</button>
          : <button type="button" className="v15-btn" onClick={() => git(i + 1)}>{yanit === undefined ? 'Boş geç' : 'Sonraki'} <ChevronRight aria-hidden /></button>}
      </nav>
      {deneme && <p className="ekm-not">Denemede açıklamalar sonda gösterilir. İşaretlediğin cevabı bitirene kadar değiştirebilirsin.</p>}
    </div>
  );
};
