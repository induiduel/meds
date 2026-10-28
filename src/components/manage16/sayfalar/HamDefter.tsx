import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, Yukleniyor, Hata, useAdminSorgu, JsonGoruntuleyici, zamanMetni , bildir } from '../kit';
import type { SayfaProps } from '../menu';

/** Sorular › Ham defter — append-only soru defteri. SALT OKUNUR: bu sayfada silme/değiştirme yoktur (YZ silemez, ezemez). */
type Satir = { id: string; baslik: string; kurul: string; ders: string; no: number; silinmis: boolean; katki: number; yz: number };

function Ayrinti({ id, kapat }: { id: string; kapat: () => void }) {
  const { veri, hata, yukleniyor, yenile } = useAdminSorgu<any>(`/api/admin/raw-pool/${encodeURIComponent(id)}`);
  const olaylar: any[] = veri?.events || [];
  return (
    <AyrintiCekmecesi acik genis kapat={kapat} baslik={id} altBaslik={`${olaylar.length} olay · salt okunur`} kayit={veri} hedef={`soru:${id}`}>
      {hata ? <Hata hata={hata} yenile={yenile} /> : yukleniyor && !veri ? <Yukleniyor satir={8} /> : veri && (
        <div className="m16-kart">
          <h2>Olaylar (eskiden yeniye)</h2>
          <ol className="m16-liste">
            {olaylar.map((e) => (
              <li key={`${e.seq}`}>
                <b>#{e.seq}</b> <Rozet ton={e.actor?.kind === 'ai' ? 'uyari' : e.actor?.kind === 'admin' ? 'vurgu' : 'bilgi'}>{e.type}</Rozet> {e.actor?.name || e.actor?.kind} · <time title={e.ts}>{zamanMetni(e.ts)}</time>
                <JsonGoruntuleyici veri={e.payload} enYuksek={180} />
              </li>
            ))}
          </ol>
        </div>
      )}
    </AyrintiCekmecesi>
  );
}

// H257: açıklama düğmeyle çelişiyordu; indirme hatası sessiz kalmaz
async function indir() {
  const r = await fetch('/api/admin/raw-pool/export?format=jsonl', { cache: 'no-store' });
  if (!r.ok) { bildir(`Dışa aktarım başarısız (${r.status})`, 'kotu'); return; }
  const url = URL.createObjectURL(await r.blob());
  const a = document.createElement('a'); a.href = url; a.download = `ham_defter_${new Date().toISOString().slice(0, 10)}.jsonl`; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}

export default function HamDefter({ id, git }: SayfaProps) {
  return (
    <>
      <SayfaBasligi baslik="Ham soru defteri" aciklama="Öğrenci katkılarının değiştirilemez kaydı. Yalnız görüntülenir; tamamı “JSONL indir” ile dışa aktarılır."
        eylemler={<button type="button" className="m16-btn" onClick={indir}>JSONL indir</button>} />
      <VeriTablosu<Satir>
        kimlik="sorular-ham" kaynak="/api/admin/sorular/ham" aramaYeri="Kimlik, başlık ya da ders ara…" satirKimligi={(s) => s.id} etkin={id || null}
        satirTikla={(s) => git(`sorular/ham/${encodeURIComponent(s.id)}${window.location.search}`)}
        suzgecler={[
          { anahtar: 'kurul', etiket: 'Kurul', secenekler: ['1', '2', '3', '4', '5', '6'].map((k) => ({ deger: k, etiket: `Kurul ${k}` })) },
          { anahtar: 'silinmis', etiket: 'Havuzda', secenekler: [{ deger: 'hayir', etiket: 'Var' }, { deger: 'evet', etiket: 'Kaldırılmış' }] },
        ]}
        sutunlar={[
          { anahtar: 'no', baslik: 'No', sirala: true, genislik: '56px', hizala: 'sag' },
          { anahtar: 'baslik', baslik: 'Soru', genislik: 'minmax(240px,3fr)' },
          { anahtar: 'ders', baslik: 'Ders', genislik: 'minmax(100px,1fr)' },
          { anahtar: 'katki', baslik: 'Katkı', sirala: true, genislik: '64px', hizala: 'sag' },
          { anahtar: 'yz', baslik: 'YZ', sirala: true, genislik: '56px', hizala: 'sag' },
          { anahtar: 'silinmis', baslik: 'Durum', genislik: '110px', hucre: (s) => (s.silinmis ? <Rozet ton="uyari">Havuzdan kalktı</Rozet> : <Rozet ton="iyi">Havuzda</Rozet>) },
        ]}
      />
      {id && <Ayrinti id={id} kapat={() => git(`sorular/ham${window.location.search}`)} />}
    </>
  );
}
