import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, Form, Rozet, Hata, Yukleniyor, GorunurlukRozeti, GorunurlukSecici, DegisiklikGecmisi, JsonGoruntuleyici, useAdminSorgu, adminIstek, bildir, type AlanTanim } from '../kit';
import { manageAdres, type SayfaProps } from '../menu';

type Katman = { paket: boolean; sesli: number; deste: number; onem: number; asistan: number; cozucu: number };
type Ders = { id: string; kod: string; kurul: number; brans: string; konu: string; ogretim_uyesi?: string; tarih?: string; saat?: string; katman: Katman; gorunurluk: string };

const KATMAN_SEC = [
  { deger: 'sesli', etiket: 'Sesli' }, { deger: 'deste', etiket: 'Deste' }, { deger: 'paket', etiket: 'Paket' },
  { deger: 'onem', etiket: 'Önem' }, { deger: 'cozucu', etiket: 'Çözücü' }, { deger: 'eksik', etiket: 'Hiçbiri' },
];

const KatmanCipleri: React.FC<{ k: Katman }> = ({ k }) => (
  <span className="m16-cip-grup">
    {k.sesli > 0 && <Rozet ton="iyi">ses {k.sesli}</Rozet>}
    {k.deste > 0 && <Rozet ton="bilgi">deste {k.deste}</Rozet>}
    {k.paket && <Rozet ton="vurgu">paket</Rozet>}
    {k.onem > 0 && <Rozet ton="notr" title="önem maddesi">önem {k.onem}</Rozet>}
    {k.cozucu > 0 && <Rozet ton="notr" title="çözücü sorusu">çöz {k.cozucu}</Rozet>}
  </span>
);

/** Kurullar ve dersler › Dersler: kayıt defteri (dersler/kN.json) listesi; /icerik/dersler/<id> ders ayrıntısı. */
export default function Dersler({ id, git }: SayfaProps) {
  const br = useAdminSorgu<{ branslar: { ad: string }[] }>('/api/admin/branslar');
  if (id) return <DersAyrinti id={id} git={git} branslar={(br.veri?.branslar || []).map((b) => b.ad)} />;
  return (
    <>
      <SayfaBasligi baslik="Dersler" aciklama="Ders kimliği ve kodu kalıcıdır (k2-07, 2f01). Satıra tıklayınca derse bağlı tüm katmanlar açılır." />
      <VeriTablosu<Ders>
        kimlik="icerik-dersler"
        kaynak="/api/admin/dersler"
        canliOlay={['content_changed', 'site_ayar_changed']}
        aramaYeri="Kimlik, kod, konu, hoca…"
        satirKimligi={(x) => x.id}
        satirTikla={(x) => git(`icerik/dersler/${x.id}`)}
        suzgecler={[
          { anahtar: 'kurul', etiket: 'Kurul', secenekler: [1, 2, 3, 4, 5, 6].map((k) => ({ deger: String(k), etiket: String(k) })) },
          { anahtar: 'katman', etiket: 'Katman', secenekler: KATMAN_SEC },
          { anahtar: 'gorunurluk', etiket: 'Görünürlük', secenekler: [{ deger: 'gizli', etiket: 'Gizli' }, { deger: 'yalniz-yonetici', etiket: 'Yalnız yönetici' }] },
        ]}
        sutunlar={[
          { anahtar: 'id', baslik: 'Kimlik', sirala: true, genislik: '76px', hucre: (x) => <a href={manageAdres(`icerik/dersler/${x.id}`)} onClick={(e) => { /* H254: Ctrl/⌘/orta tık yeni sekmede açar, satır tıklamasına düşmez */ if (e.ctrlKey || e.metaKey || e.shiftKey || e.button === 1) { e.stopPropagation(); return; } e.preventDefault(); }}><code>{x.id}</code></a> },
          { anahtar: 'kod', baslik: 'Kod', genislik: '60px', hucre: (x) => <code>{x.kod}</code> },
          { anahtar: 'konu', baslik: 'Konu', sirala: true, genislik: 'minmax(220px,3fr)', hucre: (x) => <span className="m16-kisalt" title={x.konu}>{x.konu}</span> },
          { anahtar: 'brans', baslik: 'Branş', sirala: true, genislik: 'minmax(110px,1fr)' },
          { anahtar: 'tarih', baslik: 'Tarih', sirala: true, genislik: '104px' },
          { anahtar: 'katman', baslik: 'Katmanlar', genislik: 'minmax(180px,2fr)', hucre: (x) => <KatmanCipleri k={x.katman} /> },
          { anahtar: 'gorunurluk', baslik: 'Görünürlük', genislik: '110px', hucre: (x) => <GorunurlukRozeti deger={x.gorunurluk} /> },
          { anahtar: 'ogretim_uyesi', baslik: 'Hoca', genislik: 'minmax(140px,1fr)', gizli: true },
        ]}
      />
    </>
  );
}

type Ayrinti = {
  ders: Record<string, any>; brans: Record<string, any> | null; gorunurluk: string;
  katmanlar: {
    paket: { key: string; baslik: string; sayilar: Record<string, number>; gorunurluk: string } | null;
    sesli: { key: string; baslik: string; varyant: number; sureSn: number; eksik: number; dosya: Record<string, boolean>; gorunurluk: string }[];
    desteler: { id: string; title: string; slideCount: number; gorunurluk: string }[];
    envanter: { dizin: string; tur: string; kod: string; baslik: string; madde: number; gorunurluk: string }[];
    ornek: { dosya: string; soru: number } | null;
    cikmis: { konular: number; paket: number };
    quiz: number;
  };
};
const TUR_AD: Record<string, string> = { onem: 'Önem listesi', asistan: 'Sınav asistanı', cozucu: 'Soru çözücü' };

function DersAyrinti({ id, git, branslar }: { id: string; git: SayfaProps['git']; branslar: string[] }) {
  const { veri, hata, yenile } = useAdminSorgu<Ayrinti>(`/api/admin/dersler/${encodeURIComponent(id)}`, { canliOlay: ['content_changed', 'site_ayar_changed'] });
  const [sekme, setSekme] = useState<'katman' | 'alan' | 'gecmis' | 'json'>('katman');
  if (hata) return <Hata hata={hata} yenile={yenile} />;
  if (!veri) return <Yukleniyor satir={8} />;
  const d = veri.ders, k = veri.katmanlar;
  const alanlar: AlanTanim[] = [
    { ad: 'konu', etiket: 'Konu', zorunlu: true, enFazla: 200 },
    { ad: 'brans', etiket: 'Branş', tur: 'secim', secenekler: branslar.map((b) => ({ deger: b, etiket: b })), ipucu: 'Yalnız aynı harfi paylaşan yazıma geçilebilir (kod kalıcı).' },
    { ad: 'ogretim_uyesi', etiket: 'Öğretim üyesi', enFazla: 120 },
    { ad: 'tarih', etiket: 'Tarih', tur: 'tarih', desen: /^\d{4}-\d{2}-\d{2}$/ },
    { ad: 'saat', etiket: 'Saat', desen: /^\d{2}:\d{2}-\d{2}:\d{2}$/, yerTutucu: '08:50-09:30' },
    { ad: 'id', etiket: 'Kimlik', salt: true }, { ad: 'kod', etiket: 'Kod', salt: true },
  ];
  const baglanti = (yol: string, metin: React.ReactNode) => <a href={manageAdres(yol)} onClick={(e) => { e.preventDefault(); git(yol); }}>{metin}</a>;
  return (
    <>
      <SayfaBasligi baslik={<>{d.konu} <code>{d.id}</code></>} aciklama={`${d.brans} · kod ${d.kod} · Kurul ${d.kurul}${d.tarih ? ` · ${d.tarih}` : ''}${d.ogretim_uyesi ? ` · ${d.ogretim_uyesi}` : ''}`}
        eylemler={<button type="button" className="m16-btn hayalet" onClick={() => git('icerik/dersler')}>← Dersler</button>}>
        <div className="m16-sekmeler" role="tablist">
          {([['katman', 'Katmanlar'], ['alan', 'Alanlar'], ['gecmis', 'Geçmiş'], ['json', 'JSON']] as const).map(([s, e]) => (
            <button key={s} type="button" role="tab" aria-selected={sekme === s} className={sekme === s ? 'on' : ''} onClick={() => setSekme(s)}>{e}</button>
          ))}
        </div>
      </SayfaBasligi>
      {sekme === 'katman' && (
        <div className="m16-izgara-2">
          <div className="m16-kart"><h2>Ders görünürlüğü</h2><GorunurlukSecici anahtar={`ders:${d.id}`} deger={veri.gorunurluk} degisti={() => void yenile()} /></div>
          <div className="m16-kart"><h2>Sesli ders ({k.sesli.length})</h2>
            {k.sesli.length ? <ul className="m16-liste">{k.sesli.map((s) => (
              <li key={s.key}>{baglanti(`ogrenme/sesli?ac=${encodeURIComponent(s.key)}`, s.key)} · {s.varyant ? `${Math.round(s.sureSn / 60)} dk` : <Rozet ton="kotu">ses yok</Rozet>} {s.eksik ? <Rozet ton="uyari">{s.eksik} katman eksik</Rozet> : <Rozet ton="iyi">tam</Rozet>}
                <div><GorunurlukSecici anahtar={`sesli:${s.key}`} deger={s.gorunurluk} /></div></li>
            ))}</ul> : <p className="m16-alan-ipucu">Sesli ders yok.</p>}
          </div>
          <div className="m16-kart"><h2>Öğren destesi ({k.desteler.length})</h2>
            {k.desteler.length ? <ul className="m16-liste">{k.desteler.map((x) => (
              <li key={x.id}>{baglanti(`ogrenme/desteler?ac=${encodeURIComponent(x.id)}`, x.title || x.id)} · {x.slideCount} adım
                <div><GorunurlukSecici anahtar={`deste:${x.id}`} deger={x.gorunurluk} /></div></li>
            ))}</ul> : <p className="m16-alan-ipucu">Deste yok.</p>}
          </div>
          <div className="m16-kart"><h2>İçerik paketi</h2>
            {k.paket ? <>
              <p>{baglanti(`ogrenme/paket?ac=${encodeURIComponent(k.paket.key)}`, k.paket.key)}</p>
              <dl className="m16-satirlar">{Object.entries(k.paket.sayilar).map(([a, n]) => <React.Fragment key={a}><dt>{a}</dt><dd>{n}</dd></React.Fragment>)}</dl>
              <GorunurlukSecici anahtar={`paket:${k.paket.key}`} deger={k.paket.gorunurluk} />
            </> : <p className="m16-alan-ipucu">Paket yok.</p>}
          </div>
          <div className="m16-kart"><h2>Önem, asistan, çözücü</h2>
            {k.envanter.length ? <ul className="m16-liste">{k.envanter.map((x) => (
              <li key={`${x.dizin}/${x.kod}`}>{TUR_AD[x.tur] || x.tur}: <code>{x.dizin}/{x.kod}</code> · {x.madde}
                <div><GorunurlukSecici anahtar={`${x.tur}:${x.dizin}/${x.kod}`} deger={x.gorunurluk} /></div></li>
            ))}</ul> : <p className="m16-alan-ipucu">Kayıt yok.</p>}
          </div>
          <div className="m16-kart"><h2>Sorular</h2>
            <dl className="m16-satirlar">
              <dt>Örnek soru</dt><dd>{k.ornek ? baglanti(`sorular/ornek?q=${encodeURIComponent(d.konu)}`, `${k.ornek.soru} soru`) : '—'}</dd>
              <dt>Quiz</dt><dd>{k.quiz || '—'}</dd>
              <dt>Çıkmış eşlemesi</dt><dd>{k.cikmis.paket || k.cikmis.konular ? `${k.cikmis.paket} pakette · ${k.cikmis.konular} konu` : '—'}</dd>
            </dl>
            {/* H152: dersten o dersin sorularına süzgeçli geçiş (eskiden yalnız sayı vardı) */}
            <p className="m16-alan-ipucu">
              {baglanti(`sorular/cikmis?q=${encodeURIComponent(d.konu)}`, 'Bu konunun çıkmış soruları')} · {baglanti(`sorular/havuz?q=${encodeURIComponent(d.konu)}`, 'Havuzdaki soruları')}
            </p>
          </div>
        </div>
      )}
      {sekme === 'alan' && (
        <div className="m16-kart">
          <Form alanlar={alanlar} deger={{ konu: d.konu, brans: d.brans, ogretim_uyesi: d.ogretim_uyesi || '', tarih: d.tarih || '', saat: d.saat || '', id: d.id, kod: d.kod }}
            kaydet={async (_y, deg) => { const { id: _i, kod: _k, ...g } = deg as any; await adminIstek(`/api/admin/dersler/${d.id}`, { yontem: 'PUT', govde: g }); bildir('Kaydedildi'); await yenile(); }} />
        </div>
      )}
      {sekme === 'gecmis' && <div className="m16-kart"><DegisiklikGecmisi hedef={`ders:${d.id}`} /></div>}
      {sekme === 'json' && <div className="m16-kart"><JsonGoruntuleyici veri={veri} enYuksek={9999} /></div>}
    </>
  );
}
