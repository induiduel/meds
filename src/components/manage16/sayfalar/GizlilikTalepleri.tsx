import React, { useState } from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, adminIstek, bildir, zamanMetni, type Ton } from '../kit';
import type { SayfaProps } from '../menu';

/**
 * Kullanıcılar › Gizlilik talepleri — veri dışa aktarma / silme / düzeltme talepleri (KVKK). Öğrenci POST /api/gizlilik/talep ile yollar
 * (doğrulanmış oturum). Bu sayfa durumu yönetir; silme/dışa aktarma işleminin kendisi Kişi 360 ve Yedek sayfalarından elle yapılır.
 */
type Satir = { id: string; at: string; uid: string; email: string; tur: string; not: string; durum: string; yanit?: string; guncellendi?: string };
const TUR: Record<string, string> = { 'disa-aktar': 'Verimi indir', sil: 'Hesabımı sil', duzelt: 'Düzeltme' };
const DURUM: Record<string, { ad: string; ton: Ton }> = {
  bekliyor: { ad: 'Bekliyor', ton: 'uyari' }, isleniyor: { ad: 'İşleniyor', ton: 'bilgi' }, tamam: { ad: 'Tamam', ton: 'iyi' }, reddedildi: { ad: 'Reddedildi', ton: 'kotu' },
};

function Ayrinti({ t, kapat, git }: { t: Satir; kapat: () => void; git: SayfaProps['git'] }) {
  const [yanit, setYanit] = useState(t.yanit || '');
  const [mesgul, setMesgul] = useState(false);
  const kaydet = async (durum: string) => {
    setMesgul(true);
    try { await adminIstek(`/api/admin/gizlilik/${encodeURIComponent(t.id)}`, { yontem: 'PUT', govde: { durum, yanit } }); bildir('Kaydedildi', 'iyi'); kapat(); }
    catch (e: any) { bildir(e?.message || 'Kaydedilemedi', 'kotu'); } finally { setMesgul(false); }
  };
  return (
    <AyrintiCekmecesi acik kapat={kapat} baslik={TUR[t.tur] || t.tur} altBaslik={`${t.email || t.uid} · ${zamanMetni(t.at)}`} kayit={t} hedef={`gizlilik:${t.id}`}
      eylemler={<>
        {Object.entries(DURUM).filter(([k]) => k !== t.durum).map(([k, v]) => <button key={k} type="button" className="m16-btn" disabled={mesgul} onClick={() => kaydet(k)}>{v.ad}</button>)}
      </>}>
      <div className="m16-kart">
        <dl className="m16-satirlar">
          <dt>Durum</dt><dd><Rozet ton={DURUM[t.durum]?.ton || 'notr'}>{DURUM[t.durum]?.ad || t.durum}</Rozet></dd>
          <dt>Kişi</dt><dd><a href={`/manage/kisi/${encodeURIComponent(t.uid)}`} onClick={(e) => { e.preventDefault(); git(`kisi/${encodeURIComponent(t.uid)}`); }}>{t.email || t.uid}</a></dd>
          <dt>Not</dt><dd>{t.not || '—'}</dd>
        </dl>
      </div>
      <div className="m16-kart">
        <h2>Yanıt notu</h2>
        <textarea className="m16-girdi" rows={4} style={{ width: '100%' }} value={yanit} onChange={(e) => setYanit(e.target.value)} placeholder="Ne yapıldı (iç not)" />
      </div>
    </AyrintiCekmecesi>
  );
}

export default function GizlilikTalepleri({ git }: SayfaProps) {
  const [acik, setAcik] = useState<Satir | null>(null);
  return (
    <>
      <SayfaBasligi baslik="Gizlilik talepleri" aciklama="Öğrencilerin veri indirme, silme ve düzeltme talepleri. İşlemi yaptıktan sonra durumu buradan kapatın." />
      <VeriTablosu<Satir>
        kimlik="kisi-gizlilik" kaynak="/api/admin/gizlilik" aramaYeri="E-posta, uid ya da not ara…" satirKimligi={(s) => s.id} etkin={acik?.id || null}
        satirTikla={(s) => setAcik(s)} canliOlay={['gizlilik_changed']}
        suzgecler={[
          { anahtar: 'durum', etiket: 'Durum', secenekler: Object.entries(DURUM).map(([k, v]) => ({ deger: k, etiket: v.ad })) },
          { anahtar: 'tur', etiket: 'Tür', secenekler: Object.entries(TUR).map(([k, v]) => ({ deger: k, etiket: v })) },
        ]}
        sutunlar={[
          { anahtar: 'at', baslik: 'Zaman', sirala: true, genislik: '110px', hucre: (s) => <time title={s.at}>{zamanMetni(s.at)}</time> },
          { anahtar: 'email', baslik: 'Kişi', genislik: 'minmax(180px,2fr)', hucre: (s) => s.email || s.uid },
          { anahtar: 'tur', baslik: 'Talep', genislik: '130px', hucre: (s) => TUR[s.tur] || s.tur },
          { anahtar: 'not', baslik: 'Not', genislik: 'minmax(160px,2fr)' },
          { anahtar: 'durum', baslik: 'Durum', sirala: true, genislik: '110px', hucre: (s) => <Rozet ton={DURUM[s.durum]?.ton || 'notr'}>{DURUM[s.durum]?.ad || s.durum}</Rozet> },
        ]}
      />
      {acik && <Ayrinti t={acik} git={git} kapat={() => setAcik(null)} />}
    </>
  );
}
