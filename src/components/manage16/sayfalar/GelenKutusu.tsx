import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, IstatistikIzgara, IstatistikKart, useAdminSorgu, zamanMetni, type Ton } from '../kit';
import { manageAdres, type SayfaProps } from '../menu';

/**
 * Genel › Gelen — bekleyen her şey tek listede (GET /api/admin/gelen): soru şikâyetleri, topluluk mesaj şikâyetleri, Öğren geri
 * bildirimleri, son 24 saatin istemci hataları (gruplu), gizlilik talepleri, Faz 14 bekleyenleri, kamp tüyo önerileri.
 * Her satır kendi yönetim sayfasına gider; işlem orada yapılır.
 */
type Satir = { id: string; tur: string; at: string; baslik: string; ayrinti: string; kim: string; ek: string; hedef: string };
const TUR: Record<string, { ad: string; ton: Ton }> = {
  soru: { ad: 'Soru şikâyeti', ton: 'kotu' }, topluluk: { ad: 'Topluluk şikâyeti', ton: 'uyari' }, 'geri-bildirim': { ad: 'Geri bildirim', ton: 'bilgi' },
  hata: { ad: 'İstemci hatası', ton: 'kotu' }, gizlilik: { ad: 'Gizlilik', ton: 'vurgu' }, faz14: { ad: 'Faz 14', ton: 'notr' }, tuyo: { ad: 'Tüyo önerisi', ton: 'iyi' },
};
const KAYNAK_TUR: Record<string, string> = { soru: 'soru', topluluk: 'topluluk', geriBildirim: 'geri-bildirim', hata: 'hata', gizlilik: 'gizlilik', faz14: 'faz14', tuyo: 'tuyo' };

export default function GelenKutusu({ git }: SayfaProps) {
  const ozet = useAdminSorgu<{ kaynaklar: Record<string, { toplam: number; hata?: boolean }> }>('/api/admin/gelen', { sorgu: { boyut: 1 } });
  const k = ozet.veri?.kaynaklar || {};
  const suz = (tur: string) => { const u = new URL(window.location.href); u.searchParams.set('s.tur', tur); u.searchParams.delete('sayfa'); git(`gelen${u.search}`, { degistir: true }); };
  return (
    <>
      <SayfaBasligi baslik="Gelen" aciklama="Bekleyen her şey tek listede. Satıra tıklayınca ilgili sayfa açılır; çözüm orada yapılır." />
      <IstatistikIzgara>
        {Object.entries(KAYNAK_TUR).map(([anahtar, tur]) => (
          <IstatistikKart key={anahtar} etiket={TUR[tur].ad} yukleniyor={!ozet.veri && ozet.yukleniyor}
            deger={k[anahtar]?.hata ? '—' : (k[anahtar]?.toplam ?? 0)} alt={k[anahtar]?.hata ? 'okunamadı' : undefined}
            ton={(k[anahtar]?.toplam || 0) > 0 ? TUR[tur].ton : 'notr'} onClick={() => suz(tur)} />
        ))}
      </IstatistikIzgara>
      <VeriTablosu<Satir>
        kimlik="genel-gelen" kaynak="/api/admin/gelen" aramaYeri="Başlık, ayrıntı ya da kişi ara…" satirKimligi={(s) => s.id}
        satirTikla={(s) => git(s.hedef)}
        canliOlay={['reports_changed', 'learn_feedback_changed', 'gizlilik_changed', 'topluluk_changed']}
        suzgecler={[{ anahtar: 'tur', etiket: 'Tür', secenekler: Object.entries(TUR).map(([d, v]) => ({ deger: d, etiket: v.ad })) }]}
        sutunlar={[
          { anahtar: 'at', baslik: 'Zaman', sirala: true, genislik: '110px', hucre: (s) => s.at ? <time title={s.at}>{zamanMetni(s.at)}</time> : '—' },
          { anahtar: 'tur', baslik: 'Tür', sirala: true, genislik: '140px', hucre: (s) => <Rozet ton={TUR[s.tur]?.ton || 'notr'}>{TUR[s.tur]?.ad || s.tur}</Rozet> },
          { anahtar: 'baslik', baslik: 'Konu', genislik: 'minmax(180px,2fr)', hucre: (s) => <a href={manageAdres(s.hedef)} onClick={(e) => { e.preventDefault(); e.stopPropagation(); git(s.hedef); }}>{s.baslik || '—'}</a> },
          { anahtar: 'ayrinti', baslik: 'Ayrıntı', genislik: 'minmax(200px,3fr)' },
          { anahtar: 'kim', baslik: 'Kim', genislik: '140px' },
          { anahtar: 'ek', baslik: 'Ek', genislik: '160px' },
        ]}
      />
    </>
  );
}
