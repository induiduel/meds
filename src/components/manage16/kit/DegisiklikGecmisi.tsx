import React from 'react';
import { useAdminSorgu, type ListeYaniti } from './api';
import { BosDurum, Hata, Yukleniyor } from './Durumlar';
import { Rozet, durumTonu } from './Rozet';

export type DenetimSatiri = { id: number; at: string; tur: 'yazma' | 'okuma'; kim: string; via?: string; yontem: string; uc: string; hedef: string; durum: number; sure_ms?: number; ozet?: any };

export const zamanMetni = (iso: string) => {
  const t = Date.parse(iso);
  if (!t) return '';
  const fark = (Date.now() - t) / 1000;
  if (fark < 60) return 'az önce';
  if (fark < 3600) return `${Math.floor(fark / 60)} dk önce`;
  if (fark < 86400) return `${Math.floor(fark / 3600)} sa önce`;
  return new Date(t).toLocaleString('tr-TR', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
};

/** Bir kaydın denetim geçmişi (GET /api/admin/denetim?hedef=). hedef ya da uc öneki verin. */
export const DegisiklikGecmisi: React.FC<{ hedef?: string; uc?: string; boyut?: number }> = ({ hedef, uc, boyut = 30 }) => {
  const { veri, yukleniyor, hata, yenile } = useAdminSorgu<ListeYaniti<DenetimSatiri>>(hedef || uc ? '/api/admin/denetim' : null, { sorgu: { hedef, uc, boyut }, canliOlay: ['denetim_eklendi'] });
  if (hata) return <Hata hata={hata} yenile={yenile} />;
  if (yukleniyor && !veri) return <Yukleniyor satir={4} />;
  if (!veri?.ogeler.length) return <BosDurum baslik="Geçmiş yok" aciklama="Bu kayıt için denetim satırı bulunmadı." />;
  return (
    <ol className="m16-gecmis">
      {veri.ogeler.map((s) => (
        <li key={s.id}>
          <div className="m16-gecmis-ust">
            <Rozet ton={durumTonu(s.durum)}>{s.yontem} {s.durum}</Rozet>
            <strong>{s.kim}</strong>
            <time dateTime={s.at} title={new Date(s.at).toLocaleString('tr-TR')}>{zamanMetni(s.at)}</time>
          </div>
          <code className="m16-gecmis-uc">{s.uc}</code>
          {s.ozet?.fark && (
            <ul className="m16-fark">
              {Object.entries(s.ozet.fark as Record<string, { once: unknown; sonra: unknown }>).map(([k, f]) => (
                <li key={k}><b>{k}</b>: <del>{JSON.stringify(f.once)}</del> → <ins>{JSON.stringify(f.sonra)}</ins></li>
              ))}
            </ul>
          )}
        </li>
      ))}
    </ol>
  );
};
