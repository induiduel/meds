import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, AyrintiCekmecesi, Hata, useAdminSorgu, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';
import './ortak/ts16.css';

type Kayit = { at: string; mesaj: string; yigin: string; bilesen: string; adres: string; surum: string; ua: string };

/** Sistem › İstemci hataları — tarayıcıdan bildirilen hatalar (/api/admin/istemci-hata, son 500). */
export default function IstemciHatalari(_p: SayfaProps) {
  const s = useAdminSorgu<{ kayitlar: Kayit[] }>('/api/admin/istemci-hata', { sorgu: { n: 500 } });
  const [acik, setAcik] = useState<Kayit | null>(null);
  const ogeler = (s.veri?.kayitlar || []).map((k, i) => ({ ...k, _id: `${k.at}-${i}` }));
  return (
    <>
      <SayfaBasligi baslik="İstemci hataları" aciklama="Öğrenci tarayıcılarının bildirdiği hatalar (son 500 kayıt; dosya 5 MB'ta döner)."
        eylemler={<button type="button" className="m16-btn" onClick={() => void s.yenile()}>Yenile</button>} />
      {s.hata && <Hata hata={s.hata} yenile={s.yenile} />}
      <VeriTablosu<Kayit & { _id: string }>
        kimlik="sistem-istemci-hata" ogeler={ogeler}
        aramaYeri="Mesaj, adres ya da sürüm…" satirKimligi={(k) => k._id} etkin={acik ? (acik as any)._id : null} satirTikla={setAcik}
        bosMetin={s.yukleniyor ? 'Yükleniyor…' : 'Kayıt yok.'}
        sutunlar={[
          { anahtar: 'at', baslik: 'Zaman', sirala: true, genislik: '110px', deger: (k) => k.at, hucre: (k) => <time dateTime={k.at} title={new Date(k.at).toLocaleString('tr-TR')}>{zamanMetni(k.at)}</time> },
          { anahtar: 'mesaj', baslik: 'Hata', genislik: 'minmax(220px,3fr)', hucre: (k) => <span className="m16-kisalt" title={k.mesaj}>{k.mesaj}</span> },
          { anahtar: 'adres', baslik: 'Sayfa', genislik: 'minmax(140px,1fr)', hucre: (k) => <code className="m16-kisalt">{k.adres}</code> },
          { anahtar: 'surum', baslik: 'Sürüm', sirala: true, genislik: '110px' },
          { anahtar: 'ua', baslik: 'Tarayıcı', genislik: 'minmax(140px,1fr)', gizli: true },
        ]}
      />
      <AyrintiCekmecesi acik={!!acik} kapat={() => setAcik(null)} genis baslik={acik?.mesaj.slice(0, 80) || ''} altBaslik={acik ? `${new Date(acik.at).toLocaleString('tr-TR')} · ${acik.surum}` : ''} kayit={acik || undefined}>
        {acik && (
          <>
            <dl className="m16-satirlar"><dt>Sayfa</dt><dd><code>{acik.adres}</code></dd><dt>Tarayıcı</dt><dd>{acik.ua}</dd></dl>
            <h3>Mesaj</h3><pre className="m16-ts-log">{acik.mesaj}</pre>
            {acik.yigin && <><h3>Yığın</h3><pre className="m16-ts-log">{acik.yigin}</pre></>}
            {acik.bilesen && <><h3>Bileşen yığını</h3><pre className="m16-ts-log">{acik.bilesen}</pre></>}
          </>
        )}
      </AyrintiCekmecesi>
    </>
  );
}
