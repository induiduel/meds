import React, { useState } from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, Yukleniyor, Hata, useAdminSorgu, JsonGoruntuleyici, adminIstek, bildir, onayIste, zamanMetni, type Ton } from '../kit';
import type { SayfaProps } from '../menu';

/** Sorular › Serbest girdiler — öğrencilerin tek kutuya yazdığı metinler ve ayrıştırma sonucu (sunucu sayfalı). */
type Satir = { id: string; at: string; kurul: string; ders: string; metin: string; durum: string; birim: number; eski: boolean; soru: string; deneme: number; hata: string };
const TON: Record<string, Ton> = { bekliyor: 'notr', isleniyor: 'bilgi', ayristirildi: 'iyi', icerik_yok: 'uyari', hata: 'kotu' };

function Ayrinti({ id, kapat }: { id: string; kapat: () => void }) {
  const { veri, hata, yukleniyor, yenile } = useAdminSorgu<any>(`/api/admin/sorular/serbest/${encodeURIComponent(id)}`);
  const [mesgul, setMesgul] = useState(false);
  const yeniden = async () => {
    // Ayrıştırma ücretsiz bulut LLM'ine gider: yalnız elle ve onayla (kural 20)
    if (!(await onayIste({ baslik: 'Yeniden ayrıştırılsın mı?', aciklama: 'Girdi ayrıştırma kuyruğuna alınır (ücretsiz LLM, elle başlatılan tek iş).', onayMetni: 'Kuyruğa al' }))) return;
    setMesgul(true);
    try { await adminIstek(`/api/admin/question-intake/${encodeURIComponent(id)}/reparse`, { yontem: 'POST' }); bildir('Kuyruğa alındı', 'iyi'); yenile(); }
    catch (e: any) { bildir(e?.message || 'Olmadı', 'kotu'); } finally { setMesgul(false); }
  };
  const birimler: any[] = veri?.parse?.units || [];
  return (
    <AyrintiCekmecesi acik genis kapat={kapat} baslik={id} altBaslik={veri?.raw ? zamanMetni(veri.raw.createdAt) : ''} kayit={veri} hedef={`girdi:${id}`}
      eylemler={<button type="button" className="m16-btn" disabled={mesgul} onClick={yeniden}>Yeniden ayrıştır</button>}>
      {hata ? <Hata hata={hata} yenile={yenile} /> : yukleniyor && !veri ? <Yukleniyor satir={6} /> : veri && (
        <>
          <div className="m16-kart"><h2>Öğrencinin metni</h2><p style={{ whiteSpace: 'pre-wrap' }}>{veri.raw.rawText}</p></div>
          <div className="m16-kart">
            <h2>Ayrıştırma ({birimler.length} birim{veri.parse && veri.parse.promptVersion !== veri.promptVersion ? ' · eski sürüm' : ''})</h2>
            {birimler.length ? birimler.map((u, i) => <JsonGoruntuleyici key={i} veri={u} enYuksek={220} />) : <p>Henüz ayrıştırılmadı.</p>}
          </div>
        </>
      )}
    </AyrintiCekmecesi>
  );
}

export default function SerbestGirdiler({ id, git }: SayfaProps) {
  return (
    <>
      <SayfaBasligi baslik="Serbest girdiler" aciklama="Öğrencilerin hatırladığını serbest metinle yazdığı girdiler ve ayrıştırma durumu." />
      <VeriTablosu<Satir>
        kimlik="sorular-serbest" kaynak="/api/admin/sorular/serbest" aramaYeri="Metin, ders ya da kimlik ara…" satirKimligi={(s) => s.id} etkin={id || null}
        satirTikla={(s) => git(`sorular/serbest/${encodeURIComponent(s.id)}${window.location.search}`)}
        suzgecler={[
          { anahtar: 'durum', etiket: 'Durum', secenekler: ['bekliyor', 'isleniyor', 'ayristirildi', 'icerik_yok', 'hata', 'eski'].map((d) => ({ deger: d, etiket: d === 'eski' ? 'Eski sürüm' : d })) },
          { anahtar: 'kurul', etiket: 'Kurul', secenekler: ['1', '2', '3', '4', '5', '6'].map((k) => ({ deger: k, etiket: `Kurul ${k}` })) },
        ]}
        sutunlar={[
          { anahtar: 'at', baslik: 'Zaman', sirala: true, genislik: '110px', hucre: (s) => <time title={s.at}>{zamanMetni(s.at)}</time> },
          { anahtar: 'metin', baslik: 'Metin', genislik: 'minmax(260px,3fr)' },
          { anahtar: 'ders', baslik: 'Ders', genislik: 'minmax(100px,1fr)' },
          { anahtar: 'birim', baslik: 'Birim', sirala: true, genislik: '64px', hizala: 'sag' },
          { anahtar: 'durum', baslik: 'Durum', genislik: '130px', hucre: (s) => <><Rozet ton={TON[s.durum] || 'notr'}>{s.durum}</Rozet>{s.eski && <Rozet ton="uyari">eski</Rozet>}</> },
        ]}
      />
      {id && <Ayrinti id={id} kapat={() => git(`sorular/serbest${window.location.search}`)} />}
    </>
  );
}
