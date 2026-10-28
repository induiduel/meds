import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, AyrintiCekmecesi, Rozet, Hata, Yukleniyor, GorunurlukBaglantisi, useAdminSorgu, zamanMetni } from '../kit';
import { manageAdres, type SayfaProps } from '../menu';
import SesKuyrugu from './SesKuyrugu';

type Satir = { key: string; baslik: string; kurul: number | null; varyant: number; sureSn: number; saglayici: string; olusturuldu: string; dosya: Record<string, boolean>; eksik: number; kayitli: boolean; gorunurluk: string };
const DOSYA_AD: Record<string, string> = { metin: 'Metin', cumle_zaman: 'Cümle zamanı', kelime_zaman: 'Kelime zamanı', isaret: 'PDF işareti', cizim: 'Çizim', terim: 'Terim', kisaltma: 'Kısaltma', cikmis_konum: 'Çıkmış chip', vurgu: 'Vurgu', v2: 'V2' };

/** Öğrenme › Sesli ders: kayıtlar (data/sesli_anlatim), ses varyantları ve katman dosyaları; görünürlük sesli:<key>. Ses üretimi eski panelde/oturumda. */
// H421: iki sekme — Dersler (varsayılan) ve Ses kuyruğu (?sekme=kuyruk; iş çekmecesi ogrenme/sesli/<iş>?sekme=kuyruk)
type Sekme = 'dersler' | 'kuyruk';
const sekmeOku = (): Sekme => (new URLSearchParams(window.location.search).get('sekme') === 'kuyruk' ? 'kuyruk' : 'dersler');

export default function SesliDersler(p: SayfaProps) {
  const { git } = p;
  const [sekme, setSekme] = useState<Sekme>(() => (p.id ? 'kuyruk' : sekmeOku()));
  React.useEffect(() => { setSekme(p.id ? 'kuyruk' : sekmeOku()); }, [p.id, p.altYol.join('/')]); // eslint-disable-line react-hooks/exhaustive-deps
  React.useEffect(() => { const f = () => setSekme(sekmeOku()); window.addEventListener('popstate', f); return () => window.removeEventListener('popstate', f); }, []);
  const sec = (s: Sekme) => { if (s === sekme) return; setSekme(s); git(s === 'kuyruk' ? 'ogrenme/sesli?sekme=kuyruk' : 'ogrenme/sesli', { degistir: true }); };
  const baslik = (
    <SayfaBasligi baslik="Sesli ders" aciklama={sekme === 'kuyruk' ? undefined : 'Sunucudaki sesli ders kayıtları. Eksik = metin, ses, zamanlama, işaret, çizim, terim, kısaltma ya da çıkmış chip dosyalarından biri yok.'}>
      <div className="m16-sekmeler" role="tablist" aria-label="Sesli ders bölümü">
        {([['dersler', 'Dersler'], ['kuyruk', 'Ses kuyruğu']] as const).map(([k, e]) => (
          <button key={k} type="button" role="tab" aria-selected={sekme === k} className={sekme === k ? 'on' : ''} onClick={() => sec(k)}>{e}</button>
        ))}
      </div>
    </SayfaBasligi>
  );
  if (sekme === 'kuyruk') return <>{baslik}<SesKuyrugu {...p} gomulu /></>;
  return <>{baslik}<DerslerSekmesi git={git} /></>;
}

function DerslerSekmesi({ git }: { git: SayfaProps['git'] }) {
  const [acik, setAcik] = useState<string | null>(() => new URLSearchParams(location.search).get('ac'));
  const a = useAdminSorgu<Satir & { varyantlar: any[]; ders: any }>(acik ? `/api/admin/sesli-dersler/${encodeURIComponent(acik)}` : null);
  return (
    <>
      <VeriTablosu<Satir>
        kimlik="ogrenme-sesli" kaynak="/api/admin/sesli-dersler" canliOlay={['site_ayar_changed']} aramaYeri="Anahtar ya da başlık…"
        satirKimligi={(x) => x.key} etkin={acik} satirTikla={(x) => setAcik(x.key)}
        suzgecler={[
          { anahtar: 'kurul', etiket: 'Kurul', secenekler: [1, 2, 3, 4, 5, 6].map((k) => ({ deger: String(k), etiket: String(k) })) },
          { anahtar: 'durum', etiket: 'Durum', secenekler: [{ deger: 'tam', etiket: 'Tam' }, { deger: 'eksik', etiket: 'Eksik' }, { deger: 'sessiz', etiket: 'Ses yok' }] },
          { anahtar: 'gorunurluk', etiket: 'Görünürlük', secenekler: [{ deger: 'gizli', etiket: 'Gizli' }, { deger: 'yalniz-yonetici', etiket: 'Yalnız yönetici' }] },
        ]}
        sutunlar={[
          { anahtar: 'key', baslik: 'Anahtar', sirala: true, genislik: 'minmax(200px,2fr)', hucre: (x) => <code className="m16-kisalt" title={x.key}>{x.key}</code> },
          { anahtar: 'baslik', baslik: 'Başlık', genislik: 'minmax(180px,2fr)', hucre: (x) => <span className="m16-kisalt" title={x.baslik}>{x.baslik}</span> },
          { anahtar: 'sureSn', baslik: 'Süre', sirala: true, genislik: '70px', hizala: 'sag', hucre: (x) => (x.varyant ? `${Math.round(x.sureSn / 60)} dk` : <Rozet ton="kotu">yok</Rozet>) },
          { anahtar: 'eksik', baslik: 'Katman', sirala: true, genislik: '96px', hucre: (x) => (x.eksik ? <Rozet ton="uyari">{x.eksik} eksik</Rozet> : <Rozet ton="iyi">tam</Rozet>) },
          { anahtar: 'gorunurluk', baslik: 'Görünürlük', genislik: '170px', hucre: (x) => <GorunurlukBaglantisi anahtar={`sesli:${x.key}`} deger={x.gorunurluk} git={git} /> } /* H322 */,
          { anahtar: 'olusturuldu', baslik: 'Üretildi', sirala: true, genislik: '100px', gizli: true, hucre: (x) => (x.olusturuldu ? zamanMetni(x.olusturuldu) : '—') },
        ]}
      />
      <AyrintiCekmecesi acik={!!acik} kapat={() => setAcik(null)} baslik={a.veri?.baslik || acik || ''} altBaslik={<code>{acik}</code>} kayit={a.veri} hedef={acik ? `sesli:${acik}` : undefined}>
        {a.hata ? <Hata hata={a.hata} yenile={a.yenile} /> : !a.veri ? <Yukleniyor satir={4} /> : (
          <>
            <div className="m16-kart"><h2>Görünürlük</h2><GorunurlukBaglantisi anahtar={`sesli:${a.veri.key}`} deger={a.veri.gorunurluk} git={git} />{/* H322 */}</div>
            {a.veri.ders && <p>Ders: <a href={manageAdres(`icerik/dersler/${a.veri.ders.id}`)} onClick={(e) => { e.preventDefault(); git(`icerik/dersler/${a.veri!.ders.id}`); }}>{a.veri.ders.id} · {a.veri.ders.konu}</a></p>}
            <div className="m16-kart"><h2>Katman dosyaları</h2>
              <span className="m16-cip-grup">{Object.entries(a.veri.dosya).map(([k, v]) => <Rozet key={k} ton={v ? 'iyi' : 'kotu'}>{DOSYA_AD[k] || k}</Rozet>)}</span>
            </div>
            <div className="m16-kart"><h2>Ses varyantları ({a.veri.varyantlar.length})</h2>
              <ul className="m16-liste">{a.veri.varyantlar.map((v) => <li key={v.id}><code>{v.id}</code> · {v.etiket} · {Math.round((v.sureSn || 0) / 60)} dk · {v.olusturuldu ? zamanMetni(v.olusturuldu) : ''}</li>)}</ul>
            </div>
          </>
        )}
      </AyrintiCekmecesi>
    </>
  );
}
