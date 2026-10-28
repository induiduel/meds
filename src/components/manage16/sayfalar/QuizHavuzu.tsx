import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, Yukleniyor, Hata, useAdminSorgu } from '../kit';
import type { SayfaProps } from '../menu';

/** Oyunlar › Quiz havuzu — yayınlanan derslerin quiz_havuzu.json soruları (kural 19; 2N pozitif/ters çift), salt okunur. */
type Satir = { id: string; ders: string; kurul: string; yon: string; tur: string; soru: string; cevap: string; cift: string };
const YON: Record<string, string> = { positive_direct: 'Pozitif', negative_inverse: 'Ters' };

function Ayrinti({ id, kapat }: { id: string; kapat: () => void }) {
  const { veri, hata, yukleniyor, yenile } = useAdminSorgu<any>(`/api/admin/quiz/havuz/${encodeURIComponent(id)}`);
  return (
    <AyrintiCekmecesi acik kapat={kapat} baslik={id} altBaslik={veri?.topic_id} kayit={veri}>
      {hata ? <Hata hata={hata} yenile={yenile} /> : yukleniyor && !veri ? <Yukleniyor satir={5} /> : veri && (
        <div className="m16-kart">
          <h2>{veri.prompt}</h2>
          <ol className="m16-liste" type="A">
            {Object.entries(veri.options || {}).map(([k, v]) => (
              <li key={k}>{k === (veri.correct_option || veri.correct_answer) ? <b>{String(v)} ✓</b> : String(v)}{veri.option_explanations?.[k] && <small> — {String(veri.option_explanations[k])}</small>}</li>
            ))}
          </ol>
        </div>
      )}
    </AyrintiCekmecesi>
  );
}

export default function QuizHavuzu({ id, git }: SayfaProps) {
  return (
    <>
      <SayfaBasligi baslik="Quiz havuzu" aciklama={<>Derslerin bilgi envanterinden üretilmiş kısa quiz soruları.{/* H172 */}<span className="m16-kaynak"><code>quiz_havuzu.json</code></span></>} />
      <VeriTablosu<Satir>
        kimlik="oyun-quiz-havuzu" kaynak="/api/admin/quiz/havuz" aramaYeri="Soru metni ya da kimlik ara…" satirKimligi={(s) => s.id} etkin={id || null}
        satirTikla={(s) => git(`oyun/quiz-havuzu/${encodeURIComponent(s.id)}${window.location.search}`)}
        suzgecler={[{ anahtar: 'yon', etiket: 'Yön', secenekler: Object.entries(YON).map(([k, v]) => ({ deger: k, etiket: v })) }]}
        sutunlar={[
          { anahtar: 'ders', baslik: 'Ders', sirala: true, genislik: '90px' },
          { anahtar: 'soru', baslik: 'Soru', genislik: 'minmax(280px,4fr)' },
          { anahtar: 'yon', baslik: 'Yön', genislik: '90px', hucre: (s) => <Rozet ton={s.yon === 'negative_inverse' ? 'uyari' : 'bilgi'}>{YON[s.yon] || s.yon}</Rozet> },
          { anahtar: 'tur', baslik: 'Tür', genislik: 'minmax(120px,1fr)', gizli: true },
          { anahtar: 'cevap', baslik: 'Cevap', genislik: '64px', hizala: 'orta' },
        ]}
      />
      {id && <Ayrinti id={id} kapat={() => git(`oyun/quiz-havuzu${window.location.search}`)} />}
    </>
  );
}
