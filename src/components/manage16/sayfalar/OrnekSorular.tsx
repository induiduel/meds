import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, Yukleniyor, Hata, useAdminSorgu, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';

/** Sorular › Örnek sorular — src/data/ornek_sorular (ders notu sadık, kazanım temelli). Salt okunur; içerik hatta üretilir (kural 4). */
type Satir = { id: string; kurul: string; ders: string; konu: string; soru: string; zorluk: string; cevap: string; kazanim: string; bildirim: number };

function Ayrinti({ id, kapat }: { id: string; kapat: () => void }) {
  const { veri, hata, yukleniyor, yenile } = useAdminSorgu<any>(`/api/admin/sorular/ornek/${encodeURIComponent(id)}`);
  const k = veri?.kayit;
  return (
    <AyrintiCekmecesi acik kapat={kapat} baslik={id} altBaslik={veri ? `${veri.ozet.ders} · ${veri.ozet.konu}` : ''} kayit={k}>
      {hata ? <Hata hata={hata} yenile={yenile} /> : yukleniyor && !veri ? <Yukleniyor satir={6} /> : k && (
        <>
          <div className="m16-kart"><h2>Soru</h2><p>{k.soru}</p>
            <ul className="m16-liste">{Object.entries(k.secenekler || k.siklar || {}).map(([a, b]: any) => <li key={a}><b>{a})</b> {typeof b === 'string' ? b : b?.metin || JSON.stringify(b)}</li>)}</ul>
            <p>Cevap: <b>{k.dogru_cevap || k.cevap || '—'}</b> · Zorluk: {k.zorluk || '—'}</p>
            <p><small>Kazanım: {veri.ozet.kazanim}</small></p>
          </div>
          <div className="m16-kart"><h2>Bildirimler ({veri.bildirimler.length})</h2>
            {veri.bildirimler.length ? <ul className="m16-liste">{veri.bildirimler.map((r: any) => <li key={r.id}><Rozet ton={r.status === 'resolved' ? 'iyi' : 'uyari'}>{r.status === 'resolved' ? 'Çözüldü' : 'Açık'}</Rozet> <b>{r.reason}</b> {r.details} · {zamanMetni(r.timestamp)}</li>)}</ul> : <p>Bildirim yok.</p>}
          </div>
        </>
      )}
    </AyrintiCekmecesi>
  );
}

export default function OrnekSorular({ id, git }: SayfaProps) {
  return (
    <>
      <SayfaBasligi baslik="Örnek sorular" aciklama="Ders notlarına sadık, kazanım temelli örnek sorular. Burada görüntülenir; üretim ve düzeltme ders hattında yapılır." />
      <VeriTablosu<Satir>
        kimlik="sorular-ornek" kaynak="/api/admin/sorular/ornek" aramaYeri="Kimlik, soru, ders ya da kazanım ara…" satirKimligi={(s) => s.id} etkin={id || null}
        satirTikla={(s) => git(`sorular/ornek/${encodeURIComponent(s.id)}${window.location.search}`)}
        suzgecler={[
          { anahtar: 'kurul', etiket: 'Kurul', secenekler: ['1', '2', '3', '4', '5', '6'].map((k) => ({ deger: k, etiket: `Kurul ${k}` })) },
          { anahtar: 'zorluk', etiket: 'Zorluk', secenekler: ['kolay', 'orta', 'zor'].map((k) => ({ deger: k, etiket: k })) },
          { anahtar: 'bildirim', etiket: 'Bildirim', secenekler: [{ deger: 'var', etiket: 'Açık bildirimi olan' }] },
        ]}
        sutunlar={[
          { anahtar: 'id', baslik: 'Kimlik', sirala: true, genislik: '130px', hucre: (s) => <code>{s.id}</code> },
          { anahtar: 'soru', baslik: 'Soru', genislik: 'minmax(240px,3fr)' },
          { anahtar: 'ders', baslik: 'Ders', genislik: 'minmax(100px,1fr)' },
          { anahtar: 'zorluk', baslik: 'Zorluk', genislik: '70px' },
          { anahtar: 'bildirim', baslik: 'Bildirim', sirala: true, genislik: '72px', hizala: 'sag', hucre: (s) => (s.bildirim ? <Rozet ton="uyari">{s.bildirim}</Rozet> : '—') },
        ]}
      />
      {id && <Ayrinti id={id} kapat={() => git(`sorular/ornek${window.location.search}`)} />}
    </>
  );
}
