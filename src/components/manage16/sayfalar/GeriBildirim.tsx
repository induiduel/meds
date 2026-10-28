import React, { useState } from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, adminIstek, bildir, zamanMetni, useAdminSorgu } from '../kit';
import type { SayfaProps } from '../menu';

/**
 * Topluluk › Geri bildirim — Öğren ekranında öğrencilerin bildirdiği içerik hataları (data/learn_feedback.json).
 * Durum (açık/çözüldü) ve iç yanıt notu: PUT /api/admin/topluluk/geri-bildirim/:id. Bildirim öğrenciye ayrıca gönderilmez.
 */
type Satir = { id: string; at: string; deste: string; deckId: string; adim: number; yer: string; alan: string; neden: string; kim: string; kimId: string; durum: string; yukari: number; asagi: number; baglanti: string; yanit: string; yanitAt: string; yanitKim: string };

function Ayrinti({ s, kapat, git }: { s: Satir; kapat: () => void; git: SayfaProps['git'] }) {
  const [yanit, setYanit] = useState(s.yanit);
  const [mesgul, setMesgul] = useState(false);
  const kaydet = async (durum?: string) => {
    setMesgul(true);
    try {
      await adminIstek(`/api/admin/topluluk/geri-bildirim/${encodeURIComponent(s.id)}`, { yontem: 'PUT', govde: { ...(durum ? { durum } : {}), yanit } });
      bildir('Kaydedildi', 'iyi'); kapat();
    } catch (e: any) { bildir(e?.message || 'Kaydedilemedi', 'kotu'); } finally { setMesgul(false); }
  };
  return (
    <AyrintiCekmecesi acik kapat={kapat} baslik={s.alan || 'Geri bildirim'} altBaslik={`${s.deste} · adım ${s.adim} · ${zamanMetni(s.at)}`} kayit={s} hedef={`geri-bildirim:${s.id}`}
      kirli={yanit !== s.yanit}
      eylemler={<>
        <button type="button" className="m16-btn" disabled={mesgul || yanit === s.yanit} onClick={() => kaydet()}>Notu kaydet</button>
        {s.durum === 'acik'
          ? <button type="button" className="m16-btn birincil" disabled={mesgul} onClick={() => kaydet('cozuldu')}>Çözüldü</button>
          : <button type="button" className="m16-btn" disabled={mesgul} onClick={() => kaydet('acik')}>Yeniden aç</button>}
      </>}>
      <div className="m16-kart">
        <dl className="m16-satirlar">
          <dt>Durum</dt><dd><Rozet ton={s.durum === 'acik' ? 'uyari' : 'iyi'}>{s.durum === 'acik' ? 'Açık' : 'Çözüldü'}</Rozet></dd>
          <dt>Yer</dt><dd>{s.yer}</dd>
          <dt>Hangi bilgi</dt><dd>{s.alan}</dd>
          <dt>Neden</dt><dd>{s.neden}</dd>
          <dt>Bildiren</dt><dd>{s.kimId ? <a href={`/manage/kisi/${encodeURIComponent(s.kimId)}`} onClick={(e) => { e.preventDefault(); git(`kisi/${encodeURIComponent(s.kimId)}`); }}>{s.kim}</a> : s.kim}</dd>
          <dt>Oy</dt><dd>▲ {s.yukari} · ▼ {s.asagi}</dd>
          <dt>Öğede aç</dt><dd>{s.baglanti ? <a href={s.baglanti} target="_blank" rel="noreferrer">Ders ekranında aç ↗</a> : '—'}</dd>
          <dt>Deste</dt><dd><a href="/manage/ogrenme/desteler" onClick={(e) => { e.preventDefault(); git(`ogrenme/desteler?q=${encodeURIComponent(s.deckId)}`); }}>{s.deckId}</a></dd>
        </dl>
      </div>
      <div className="m16-kart">
        <h2>Yanıt (iç not)</h2>
        <textarea className="m16-girdi" rows={4} style={{ width: '100%' }} value={yanit} onChange={(e) => setYanit(e.target.value)} placeholder="Ne yapıldı, kim düzeltti…" />
        {s.yanitAt && <p className="m16-ts-not">Son: {s.yanitKim} · {zamanMetni(s.yanitAt)}</p>}
      </div>
    </AyrintiCekmecesi>
  );
}

export default function GeriBildirim({ id, git }: SayfaProps) {
  const [acik, setAcik] = useState<Satir | null>(null);
  const dogrudan = useAdminSorgu<{ ogeler: Satir[] }>(id && !acik ? '/api/admin/topluluk/geri-bildirim' : null, { sorgu: { q: id, 's.durum': 'hepsi', boyut: 1 } });
  const secili = acik || (id ? dogrudan.veri?.ogeler?.find((x) => x.id === id) || null : null);
  const kapat = () => { setAcik(null); if (id) git('topluluk/geri-bildirim', { degistir: true }); };
  return (
    <>
      <SayfaBasligi baslik="Geri bildirim" aciklama="Öğrencilerin Öğren ekranında bildirdiği içerik hataları. Düzelttikten sonra çözüldü olarak kapatın." />
      <VeriTablosu<Satir>
        kimlik="topluluk-geri-bildirim" kaynak="/api/admin/topluluk/geri-bildirim" aramaYeri="Deste, bilgi, neden ya da kişi ara…" satirKimligi={(s) => s.id}
        etkin={secili?.id || null} satirTikla={(s) => setAcik(s)} canliOlay={['learn_feedback_changed']}
        suzgecler={[{ anahtar: 'durum', etiket: 'Durum', secenekler: [{ deger: 'acik', etiket: 'Açık' }, { deger: 'cozuldu', etiket: 'Çözüldü' }, { deger: 'hepsi', etiket: 'Hepsi' }] }]}
        sutunlar={[
          { anahtar: 'at', baslik: 'Zaman', sirala: true, genislik: '110px', hucre: (s) => <time title={s.at}>{zamanMetni(s.at)}</time> },
          { anahtar: 'deste', baslik: 'Deste', sirala: true, genislik: 'minmax(140px,1fr)', hucre: (s) => `${s.deste} · ${s.adim}` },
          { anahtar: 'alan', baslik: 'Hangi bilgi', genislik: 'minmax(180px,2fr)' },
          { anahtar: 'neden', baslik: 'Neden', genislik: 'minmax(180px,2fr)' },
          { anahtar: 'kim', baslik: 'Bildiren', genislik: '130px' },
          { anahtar: 'yukari', baslik: 'Oy', sirala: true, genislik: '70px', hizala: 'sag', hucre: (s) => `${s.yukari}/${s.asagi}` },
          { anahtar: 'durum', baslik: 'Durum', genislik: '100px', hucre: (s) => <Rozet ton={s.durum === 'acik' ? 'uyari' : 'iyi'}>{s.durum === 'acik' ? 'Açık' : 'Çözüldü'}</Rozet> },
        ]}
      />
      {secili && <Ayrinti key={secili.id} s={secili} git={git} kapat={kapat} />}
    </>
  );
}
