/**
 * KMB "Eksiklerim": hata istatistiği (kmbHata.ts) + unutulan noktaların hedefli tekrarı.
 * Özet (deneme, doğruluk, zayıf/öğrenilen), kaynak başına doğruluk, son 14 gün, öğretim adımına göre gruplanmış zayıf
 * noktalar ("adımı yeniden çalış"), ve tekrar oturumu: unutulan OSCE basamağı için "bundan sonra ne yaparsın?",
 * yanlış vaka yeniden, yapıyı sahnede yeniden bul, hedefi kendin anlatıp öz değerlendirme. Doğru iki kez üst üste
 * yapılan nokta listeden düşer.
 */
import React, { useMemo, useState } from 'react';
import { SAHNELER, SahneCiz, type SahneDurum } from './sahneler';
import { uygula } from './eylem';
import { KAYNAK_AD, hataKaydet, hataSifirla, ozet, useHata, zayiflar, type Kaynak, type Kavram } from './kmbHata';
import { karistir, yollar, type Basamak, type Ders } from './kmbVeri';

type Z = Kavram & { id: string };

function Ozet({ ders, onTekrar, adimaGit }: { ders: Ders; onTekrar: () => void; adimaGit: (adim: string) => void }) {
  const v = useHata(ders.kod);
  const o = ozet(v);
  const Z = zayiflar(v);
  const gruplar = useMemo(() => {
    const m = new Map<string, Z[]>();
    for (const z of Z) { const k = z.adim || ''; m.set(k, [...(m.get(k) || []), z]); }
    // ders sırasına göre (öğrenci baştan sona çalışsın)
    return [...m.entries()].sort(([a], [b]) => ders.adimlar.findIndex((x) => x.id === a) - ders.adimlar.findIndex((x) => x.id === b));
  }, [Z, ders]);
  const gunler = useMemo(() => {
    const r: { g: string; d: number; y: number }[] = [];
    for (let i = 13; i >= 0; i--) {
      const t = new Date(Date.now() - i * 864e5);
      const g = new Date(t.getTime() - t.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
      const [d, y] = v.g[g] || [0, 0];
      r.push({ g, d, y });
    }
    return r;
  }, [v]);
  const enCok = Math.max(1, ...gunler.map((x) => x.d + x.y));
  if (!o.deneme) {
    return (
      <div className="kmb-eks-bos">
        <b>Henüz deneme yok</b>
        <p>Sınav sekmesinde vaka, OSCE sırası, sahnede bul, etiketleme ya da kontrol listesi çözdükçe her yanlışın burada toplanır;
          unuttuğun basamaklar ve eksik kaldığın adımlar ayrı ayrı gösterilir, onları hedefli olarak tekrar edersin.</p>
      </div>
    );
  }
  return (
    <div className="kmb-eks">
      <div className="kmb-eks-kartlar">
        <div><small>Deneme</small><b>{o.deneme}</b></div>
        <div><small>Doğruluk</small><b className={o.oran >= 80 ? 'iyi' : o.oran >= 60 ? 'orta' : 'zayif'}>%{o.oran}</b></div>
        <div><small>Eksik nokta</small><b className={o.zayif ? 'zayif' : 'iyi'}>{o.zayif}</b></div>
        <div><small>Telafi edilen</small><b className="iyi">{o.ogrenilen}</b></div>
      </div>
      {!!Z.length && (
        <button className="kmb-eks-basla" onClick={onTekrar}>
          <b>Eksiklerini çalış</b><span>{Math.min(Z.length, 10)} soruluk hedefli tekrar · iki kez üst üste doğru yapılan nokta listeden düşer</span>
        </button>
      )}
      <div className="kmb-eks-iki">
        <section className="kmb-eks-kutu">
          <h3>Bölümlere göre doğruluk</h3>
          <ul className="kmb-eks-kaynak">
            {(Object.keys(KAYNAK_AD) as Kaynak[]).filter((k) => v.s[k]).map((k) => {
              const [d, y] = v.s[k]!;
              const p = Math.round((d / Math.max(1, d + y)) * 100);
              return (
                <li key={k}><span>{KAYNAK_AD[k]}</span><span className="cubuk"><i style={{ width: `${p}%` }} className={p >= 80 ? 'iyi' : p >= 60 ? 'orta' : 'zayif'} /></span>
                  <small>%{p} · {d + y}</small></li>
              );
            })}
          </ul>
        </section>
        <section className="kmb-eks-kutu">
          <h3>Son 14 gün</h3>
          <div className="kmb-eks-gun" role="img" aria-label="Son 14 günde günlük doğru ve yanlış sayısı">
            {gunler.map((x) => (
              <span key={x.g} title={`${new Date(x.g).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })}: ${x.d} doğru, ${x.y} yanlış`}>
                <i className="y" style={{ height: `${(x.y / enCok) * 100}%` }} /><i className="d" style={{ height: `${(x.d / enCok) * 100}%` }} />
              </span>
            ))}
          </div>
          <p className="kmb-eks-lejant"><i className="d" /> doğru <i className="y" /> yanlış</p>
        </section>
      </div>
      <section className="kmb-eks-kutu">
        <h3>Eksik kaldığın adımlar</h3>
        {!gruplar.length ? <p className="kmb-not">Açık eksik yok. Yanlış yaptığın her noktayı iki kez üst üste doğru yaptın.</p> : (
          <ol className="kmb-eks-adimlar">
            {gruplar.map(([adim, L]) => {
              const a = ders.adimlar.find((x) => x.id === adim);
              const no = ders.adimlar.findIndex((x) => x.id === adim) + 1;
              return (
                <li key={adim}>
                  <div className="bas">
                    <span className="no">{no || '•'}</span>
                    <b>{a?.baslik || 'Genel'}</b>
                    {a && <button onClick={() => adimaGit(adim)}>Adımı yeniden çalış ›</button>}
                  </div>
                  <ul>
                    {L.map((z) => (
                      <li key={z.id}><span className={`tur ${z.tur}`}>{z.tur === 'basamak' ? 'Basamak' : z.tur === 'vaka' ? 'Vaka' : z.tur === 'yapi' ? 'Yapı' : 'Hedef'}</span>
                        <span className="ad">{z.ad}</span><small>{z.y} yanlış{z.d ? ` · ${z.d} doğru` : ''}</small></li>
                    ))}
                  </ul>
                </li>
              );
            })}
          </ol>
        )}
      </section>
      <p className="kmb-not">İstatistik hesabında saklanır, cihazlar arasında eşitlenir.{' '}
        <button className="kmb-bag" onClick={() => { if (window.confirm('Bu becerinin hata istatistiği silinsin mi?')) hataSifirla(ders.kod); }}>İstatistiği sıfırla</button></p>
    </div>
  );
}

/** Kavram → tekrar sorusu */
type Soru =
  | { tur: 'basamak'; z: Z; akis: string; soru: string; secenekler: string[]; dogru: string; b: Basamak }
  | { tur: 'vaka'; z: Z; s: Ders['sinav']['senaryolar'][number] }
  | { tur: 'yapi'; z: Z; sahne: string; hedef: string; yonerge: string; aciklama?: string }
  | { tur: 'hedef'; z: Z; k: NonNullable<Ders['hedefCalisma']>[number] };

function soruKur(ders: Ders, z: Z, tohum: number): Soru | null {
  const [on, a, b, ...kalan] = z.id.split(':');
  if (on === 'b') {
    const ak = ders.sinav.akislar.find((x) => x.id === a);
    const metin = [b, ...kalan].join(':');
    if (!ak) return null;
    for (const y of yollar(ak.basamaklar)) {
      const i = y.basamaklar.findIndex((x) => x.metin === metin);
      if (i < 0) continue;
      const L = y.basamaklar;
      const onceki = L[i - 1];
      // çeldiriciler aynı akışın komşu basamakları (gerçek karışıklık), sonra kalanlar
      const komsu = [L[i + 1], L[i + 2], L[i - 2], L[i + 3], L[i - 3], ...L].filter((x): x is Basamak => !!x && x.metin !== metin && x.metin !== onceki?.metin);
      const celdirici = [...new Set(komsu.map((x) => x.metin))].slice(0, 3);
      return {
        tur: 'basamak', z, akis: ak.ad, b: L[i], dogru: metin,
        soru: onceki ? `“${onceki.metin}” basamağından hemen sonra ne yaparsın?` : 'Bu uygulamada ilk basamak hangisi?',
        secenekler: karistir([metin, ...celdirici], tohum),
      };
    }
    return null;
  }
  if (on === 'v') { const s = ders.sinav.senaryolar.find((x) => x.id === a); return s ? { tur: 'vaka', z, s } : null; }
  if (on === 'u') { const g = ders.sinav.bul.find((x) => x.id === a); return g ? { tur: 'yapi', z, sahne: g.sahne, hedef: g.hedef, yonerge: g.yonerge, aciklama: g.aciklama } : null; }
  if (on === 'e') { const ad = SAHNELER[a]?.etiket[b]?.[2]; return ad ? { tur: 'yapi', z, sahne: a, hedef: b, yonerge: `Sahnede “${ad}” yapısını göster.` } : null; }
  if (on === 'h') { const k = ders.hedefCalisma?.find((x) => String(x.no) === a); return k ? { tur: 'hedef', z, k } : null; }
  return null;
}

function Tekrar({ ders, liste, onBitir, adimaGit }: { ders: Ders; liste: Z[]; onBitir: () => void; adimaGit: (adim: string) => void }) {
  const [tohum] = useState(() => Date.now() % 10000);
  const sorular = useMemo(() => liste.map((z, i) => soruKur(ders, z, tohum + i)).filter((x): x is Soru => !!x), [liste, ders, tohum]);
  const [i, setI] = useState(0);
  const [cevap, setCevap] = useState<{ dogru: boolean; secim?: number | string } | null>(null);
  const [acik, setAcik] = useState(false);
  const [skor, setSkor] = useState({ d: 0, y: 0 });
  const [isaret, setIsaret] = useState<{ id: string; dogru: boolean } | null>(null);
  const s = sorular[i];
  const meta = (z: Z) => ({ tur: z.tur, ad: z.ad, adim: z.adim });
  const yanitla = (dogru: boolean, secim?: number | string) => {
    if (cevap) return;
    setCevap({ dogru, secim });
    setSkor((x) => (dogru ? { ...x, d: x.d + 1 } : { ...x, y: x.y + 1 }));
    hataKaydet(ders.kod, s.z.id, dogru, 'tekrar', meta(s.z));
  };
  const ileri = () => { setCevap(null); setAcik(false); setIsaret(null); setI((n) => n + 1); };
  const durum = useMemo<SahneDurum>(() => {
    if (!s) return {};
    if (s.tur === 'vaka') return uygula({}, s.s.eylem);
    if (s.tur === 'hedef') return uygula({}, s.k.eylem);
    if (s.tur === 'yapi' && cevap) return { [s.hedef]: { vurgu: 1, etiket: true, gor: true } };
    return {};
  }, [s, cevap]);

  if (!s) {
    return (
      <div className="kmb-eks-sonuc">
        <b>Tekrar bitti</b>
        <p>{skor.d} doğru, {skor.y} yanlış. {skor.y ? 'Yanlış yaptıkların listede kaldı; ilgili adımı yeniden izleyip tekrar dene.' : 'Hepsini bildin.'}</p>
        <div className="kmb-denetim"><button className="ana" onClick={onBitir}>Eksiklerime dön</button></div>
      </div>
    );
  }
  const adim = s.z.adim ? ders.adimlar.find((x) => x.id === s.z.adim) : undefined;
  return (
    <div className="kmb-eks-tekrar">
      <div className="kmb-eks-tekrar-ust">
        <button className="kmb-bag" onClick={onBitir}>‹ Eksiklerim</button>
        <span className="kmb-sayac">{i + 1} / {sorular.length} · {skor.d} doğru</span>
      </div>
      <div className="kmb-eks-ilerleme"><i style={{ width: `${(i / sorular.length) * 100}%` }} /></div>

      {s.tur === 'basamak' && (
        <div className="kmb-eks-soru">
          <p className="kmb-eks-etiket">Unuttuğun basamak · {s.akis}</p>
          <h3>{s.soru}</h3>
          <div className="kmb-secenekler">
            {s.secenekler.map((m, j) => (
              <button key={m} disabled={!!cevap} onClick={() => yanitla(m === s.dogru, j)}
                className={!cevap ? '' : m === s.dogru ? 'dogru' : cevap.secim === j ? 'yanlis' : 'soluk'}>
                <b>{'ABCD'[j]}</b> {m}
              </button>
            ))}
          </div>
          {cevap && <div className={`kmb-kutu ${cevap.dogru ? 'puf' : 'dikkat'}`}><b>{cevap.dogru ? 'Doğru' : `Doğrusu: ${s.dogru}`}</b><p>{s.b.aciklama}</p></div>}
        </div>
      )}

      {s.tur === 'vaka' && (
        <div className="kmb-senaryo-govde">
          <div className="kmb-sahne-kap kucuk"><SahneCiz sahne={s.s.sahne} durum={durum} /></div>
          <div className="kmb-eks-soru">
            <p className="kmb-eks-etiket">Yanlış yaptığın vaka · {s.s.baslik}</p>
            <h3>{s.s.soru}</h3>
            <div className="kmb-secenekler">
              {s.s.secenekler.map((c, j) => (
                <button key={j} disabled={!!cevap} onClick={() => yanitla(c.dogru, j)}
                  className={!cevap ? '' : c.dogru ? 'dogru' : cevap.secim === j ? 'yanlis' : 'soluk'}>
                  <b>{'ABCDE'[j]}</b> {c.metin}
                  {cevap && (cevap.secim === j || c.dogru) && <span className="kmb-aciklama">{c.aciklama}</span>}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {s.tur === 'yapi' && (
        <div className="kmb-eks-soru">
          <p className="kmb-eks-etiket">Sahnede bul</p>
          <h3>{s.yonerge}</h3>
          <div className="kmb-sahne-kap"><SahneCiz sahne={s.sahne} durum={durum} secilebilir={!cevap} isaret={isaret} onSec={(id) => {
            if (cevap) return;
            const d = id === s.hedef;
            setIsaret({ id, dogru: d });
            yanitla(d);
          }} /></div>
          {cevap && <div className={`kmb-kutu ${cevap.dogru ? 'puf' : 'dikkat'}`}><b>{cevap.dogru ? 'Doğru' : 'Yanlış yer; doğrusu yeşil işaretli'}</b>{s.aciklama && <p>{s.aciklama}</p>}</div>}
        </div>
      )}

      {s.tur === 'hedef' && (
        <div className="kmb-eks-soru">
          <p className="kmb-eks-etiket">Hedef {s.k.no} · önce kendin anlat</p>
          <h3>{s.k.hoca}</h3>
          {!acik ? <div className="kmb-denetim"><button className="ana" onClick={() => setAcik(true)}>Cevabı aç</button></div> : (
            <>
              <div className="kmb-hedef-bolum"><b>Ne yaparsın</b><p>{s.k.ne}</p></div>
              <div className="kmb-hedef-bolum"><b>Nasıl</b>{s.k.nasil.map((c) => <p key={c}>{c}</p>)}</div>
              <div className="kmb-hedef-bolum"><b>Neden</b><p>{s.k.neden}</p></div>
              {!cevap && (
                <div className="kmb-denetim">
                  <span>Anlattığın bununla örtüşüyor mu?</span>
                  <button className="ana" onClick={() => yanitla(true)}>Evet, tamdı</button>
                  <button onClick={() => yanitla(false)}>Eksik kaldı</button>
                </div>
              )}
            </>
          )}
        </div>
      )}

      {cevap && (
        <div className="kmb-denetim">
          <button className="ana" onClick={ileri}>{i + 1 < sorular.length ? 'Sonraki ›' : 'Sonucu gör ›'}</button>
          {adim && !cevap.dogru && <button onClick={() => adimaGit(adim.id)}>“{adim.baslik}” adımını yeniden izle</button>}
        </div>
      )}
    </div>
  );
}

export default function Eksikler({ ders, adimaGit }: { ders: Ders; adimaGit: (adim: string) => void }) {
  const v = useHata(ders.kod);
  const [tekrar, setTekrar] = useState<Z[] | null>(null);
  if (tekrar) return <Tekrar ders={ders} liste={tekrar} onBitir={() => setTekrar(null)} adimaGit={adimaGit} />;
  return <Ozet ders={ders} onTekrar={() => setTekrar(zayiflar(v).slice(0, 10))} adimaGit={adimaGit} />;
}
