import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, adminIstek, onayIste, bildir, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';

/** Sorular › Faz 14 kuyruğu — öğrencilerin Faz 14'e gönderdiği sorular. Görünüm; başlatma yalnız elle (AGENTS.md kural 20). */
type Satir = { id: string; soruId: string; durum: string; not: number; son: string; ilkNot: string; kim: string };
const DURUM: Record<string, [string, 'uyari' | 'vurgu' | 'iyi' | 'notr' | 'kotu']> = { bekliyor: ['Bekliyor', 'uyari'], yonetici_onayi: ['Yönetici onayı', 'vurgu'], uygulandi: ['Uygulandı', 'iyi'], reddedildi: ['Reddedildi', 'notr'], guncellendi: ['Güncellendi', 'iyi'], hata: ['Hata', 'kotu'] };

export default function Faz14Kuyrugu({ git }: SayfaProps) {
  const baslat = async () => {
    const ok = await onayIste({ baslik: 'Faz 14 kullanıcı kuyruğu şimdi işlensin mi?', aciklama: 'Bekleyen sorular ücretsiz LLM anahtarlarıyla tek seferlik işlenir. Zamanlayıcı kurulmaz (kural 20).', tehlikeli: true, yazilacak: 'BASLAT', onayMetni: 'Başlat' });
    if (!ok) return;
    try { const r: any = await adminIstek('/api/admin/faz14-kuyruk/baslat', { yontem: 'POST' }); bildir(r?.message || r?.durum || 'Başlatıldı', 'iyi'); }
    catch (e: any) { bildir(e.message, 'kotu'); }
  };
  return (
    <>
      <SayfaBasligi baslik="Çıkmış inceleme kuyruğu (Faz 14)" aciklama="Öğrencilerin incelemeye gönderdiği çıkmış sorular ve hata bildirimleri. İşleme yalnız elle başlatılır."
        eylemler={<button type="button" className="m16-btn" onClick={baslat}>Elle başlat…</button>} />
      <VeriTablosu<Satir>
        kimlik="sorular-faz14" kaynak="/api/admin/sorular/faz14" aramaYeri="Soru kimliği, not ya da kişi ara…" satirKimligi={(s) => s.id}
        satirTikla={(s) => (s.soruId ? git(`sorular/cikmis/${encodeURIComponent(s.soruId)}`) : bildir('Bu kaydın bağlı bir soru kimliği yok.', 'bilgi'))} /* H258: soru kimliği yoksa geri bildirim */
        suzgecler={[{ anahtar: 'durum', etiket: 'Durum', secenekler: Object.entries(DURUM).map(([deger, [etiket]]) => ({ deger, etiket })) }]}
        sutunlar={[
          { anahtar: 'son', baslik: 'Son', sirala: true, genislik: '100px', hucre: (s) => (s.son ? zamanMetni(s.son) : '—') },
          { anahtar: 'durum', baslik: 'Durum', genislik: '120px', hucre: (s) => <Rozet ton={DURUM[s.durum]?.[1] || 'notr'}>{DURUM[s.durum]?.[0] || s.durum}</Rozet> },
          { anahtar: 'soruId', baslik: 'Soru', genislik: 'minmax(120px,1fr)', hucre: (s) => <code>{s.soruId}</code> },
          { anahtar: 'ilkNot', baslik: 'İlk not', genislik: 'minmax(220px,2.5fr)' },
          { anahtar: 'not', baslik: 'Not', sirala: true, genislik: '56px', hizala: 'sag' },
          { anahtar: 'kim', baslik: 'Kim', genislik: 'minmax(90px,0.8fr)', gizli: true },
        ]}
      />
    </>
  );
}
