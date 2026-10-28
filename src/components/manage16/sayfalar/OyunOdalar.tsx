import React, { useState } from 'react';
import { RefreshCw } from 'lucide-react';
import { SayfaBasligi, VeriTablosu, Rozet, Hata, AyrintiCekmecesi, adminIstek, bildir, onayIste, useAdminSorgu } from '../kit';
import type { SayfaProps } from '../menu';

/** Oyunlar › Canlı odalar: quizRealtimeServer RAM odaları (5 sn'de bir tazelenir), oyuncular, kapat. Uç: /api/admin/quiz/odalar */
type Oyuncu = { userId: string; ad: string; puan: number; hazir: boolean; takim: string | null; bagli: boolean };
type Oda = { roomId: string; baslik: string; kaynak: string; ders: string; durum: string; takimli: boolean; soru: number; sira: number; kurucu: string; oyuncular: Oyuncu[] };
const DURUM: Record<string, string> = { lobby: 'Lobide', countdown: 'Geri sayım', in_round: 'Soruda', reveal: 'Cevap', finished: 'Bitti' };

export default function OyunOdalar({ git }: SayfaProps) {
  const { veri, hata, yukleniyor, yenile } = useAdminSorgu<{ ogeler: Oda[]; toplam: number; oyunlarAcik: boolean }>('/api/admin/quiz/odalar', { aralikMs: 5000 });
  const [acik, setAcik] = useState<string | null>(null);
  const oda = veri?.ogeler.find((o) => o.roomId === acik) || null;
  const kapat = async (o: Oda) => {
    if (!(await onayIste({ baslik: `${o.roomId} odası kapatılsın mı?`, aciklama: `${o.oyuncular.length} oyuncuya "oda kapatıldı" bildirilir.`, tehlikeli: true, onayMetni: 'Kapat' }))) return;
    try { await adminIstek(`/api/admin/quiz/odalar/${encodeURIComponent(o.roomId)}`, { yontem: 'DELETE' }); bildir('Oda kapatıldı', 'iyi'); setAcik(null); void yenile(); }
    catch (e: any) { bildir(e?.message || 'Kapatılamadı', 'kotu'); }
  };
  if (hata && !veri) return <><SayfaBasligi baslik="Canlı odalar" /><Hata hata={hata} yenile={yenile} /></>;
  return (
    <>
      <SayfaBasligi baslik="Canlı odalar" aciklama={`Sunucu belleğindeki yarışma odaları (oyun bitince ya da herkes çıkınca silinir).${veri && !veri.oyunlarAcik ? ' Oyunlar bayrağı KAPALI: yeni oda kurulmaz.' : ''}`}
        eylemler={<>
          <button type="button" className="m16-btn" onClick={() => git('oyun/kaynak')}>Kaynaklar ve modlar</button>
          <button type="button" className="m16-btn" onClick={() => void yenile()} disabled={yukleniyor}><RefreshCw className={yukleniyor ? 'm16-don' : ''} aria-hidden="true" />Yenile</button>
        </>} />
      <VeriTablosu<Oda>
        kimlik="oyun-odalar"
        ogeler={veri?.ogeler || []}
        satirKimligi={(o) => o.roomId}
        adresteDurum={false}
        etkin={acik}
        satirTikla={(o) => setAcik(o.roomId)}
        sutunlar={[
          { anahtar: 'roomId', baslik: 'Kod', genislik: '90px', sirala: true, deger: (o) => o.roomId, hucre: (o) => <code>{o.roomId}</code> },
          { anahtar: 'baslik', baslik: 'Kaynak', genislik: 'minmax(200px,2fr)', deger: (o) => `${o.baslik} ${o.kaynak}`, hucre: (o) => o.baslik || o.kaynak },
          { anahtar: 'durum', baslik: 'Durum', genislik: '110px', deger: (o) => o.durum, hucre: (o) => <Rozet ton={o.durum === 'lobby' ? 'notr' : o.durum === 'finished' ? 'notr' : 'iyi'}>{DURUM[o.durum] || o.durum}</Rozet> },
          { anahtar: 'soru', baslik: 'Soru', genislik: '80px', hizala: 'sag', deger: (o) => o.sira, hucre: (o) => `${Math.min(o.sira + 1, o.soru)}/${o.soru}` },
          { anahtar: 'oyuncu', baslik: 'Oyuncu', genislik: '80px', hizala: 'sag', sirala: true, deger: (o) => o.oyuncular.length, hucre: (o) => o.oyuncular.length },
          { anahtar: 'mod', baslik: 'Mod', genislik: '80px', deger: (o) => (o.takimli ? 'takim' : 'canli'), hucre: (o) => (o.takimli ? 'Takım' : 'Canlı') },
          { anahtar: 'eylem', baslik: '', genislik: '90px', hucre: (o) => <button type="button" className="m16-btn tehlike" onClick={(e) => { e.stopPropagation(); void kapat(o); }}>Kapat</button> },
        ]}
      />
      <AyrintiCekmecesi acik={!!oda} kapat={() => setAcik(null)} baslik={oda ? `Oda ${oda.roomId}` : ''} altBaslik={oda?.baslik} kayit={oda || undefined} hedef={oda ? `quiz-oda:${oda.roomId}` : undefined}
        eylemler={oda ? <button type="button" className="m16-btn tehlike" onClick={() => void kapat(oda)}>Odayı kapat</button> : undefined}>
        {oda && (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead><tr><th align="left">Oyuncu</th><th align="right">Puan</th><th>Takım</th><th>Hazır</th><th>Bağlı</th></tr></thead>
            <tbody>{[...oda.oyuncular].sort((a, b) => b.puan - a.puan).map((p) => (
              <tr key={p.userId}><td>{p.ad}</td><td align="right">{p.puan}</td><td align="center">{p.takim || '–'}</td><td align="center">{p.hazir ? '✓' : ''}</td><td align="center">{p.bagli ? '✓' : '×'}</td></tr>
            ))}</tbody>
          </table>
        )}
      </AyrintiCekmecesi>
    </>
  );
}
