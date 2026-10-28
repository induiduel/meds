import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, adminIstek, bildir, onayIste, yazimHedefi, zamanMetni } from '../kit';
import { manageAdres } from '../menu';
import type { SayfaProps } from '../menu';

/** Sorular › Şikâyetler — soru hata bildirimleri (çıkmış + havuz + örnek). Sohbet/mesaj şikâyetleri Topluluk › Şikâyetler'de. */
type Satir = { id: string; raporId: string; kaynak: 'cikmis' | 'havuz' | 'ornek'; soruId: string; ders: string; kurul: string; neden: string; ayrinti: string; kim: string; at: string; durum: string; kok: string };
const KAYNAK: Record<string, string> = { cikmis: 'Çıkmış', havuz: 'Havuz', ornek: 'Örnek soru' };
const SAYFA: Record<string, string> = { cikmis: 'sorular/cikmis', havuz: 'sorular/havuz', ornek: 'sorular/ornek' };

// H294: satır kimliği "<kaynak>:<soruId>:<raporId>" (sorular.ts tumSikayetler) — toplu işlem kimlikten çözülür
const parca = (id: string) => { const p = id.split(':'); return { kaynak: p[0], soruId: p.slice(1, -1).join(':'), raporId: p[p.length - 1] }; };

export default function SoruSikayetleri({ git }: SayfaProps) {
  const [acik, setAcik] = React.useState<Satir | null>(null);
  // H294: kapatılan şikâyet "Açık" süzgecinde SSE yenilemesini beklemeden düşer; "Hepsi"de durumu yerelde güncellenir
  const [yerelDurum, setYerelDurum] = React.useState<Record<string, string>>({});
  const acikSuzgec = () => { const v = new URLSearchParams(window.location.search).get('s.durum'); return !v || v === 'acik'; };
  const coz = async (s: Satir, durum: 'resolved' | 'pending') => {
    try {
      await adminIstek('/api/admin/sorular/sikayet/coz', { yontem: 'POST', govde: { kaynak: s.kaynak, soruId: s.soruId, raporId: s.raporId, durum } });
      setYerelDurum((d) => ({ ...d, [s.id]: durum === 'resolved' ? 'cozuldu' : 'acik' }));
      if (acik?.id === s.id) setAcik(durum === 'resolved' && acikSuzgec() ? null : { ...s, durum: durum === 'resolved' ? 'cozuldu' : 'acik' });
      bildir(durum === 'resolved' ? 'Çözüldü olarak işaretlendi' : 'Yeniden açıldı', 'iyi');
    } catch (e: any) { bildir(e.message, 'kotu'); }
  };
  // H294: toplu çöz / yok say (soru bildiriminde ayrı "reddedildi" durumu yok; ikisi de bildirimi kapatır, denetim kaydında eylem adı ayrılır)
  const toplu = async (ids: string[], ad: 'Çözüldü' | 'Yok say', temizle: () => void) => {
    if (!(await onayIste({ baslik: `${ids.length} şikâyet kapatılsın mı (${ad})?`, aciklama: `Hedef: ${yazimHedefi()}.`, onayMetni: ad }))) return;
    let hata = 0; let son = '';
    const tamam: Record<string, string> = {};
    for (const id of ids) {
      try { await adminIstek('/api/admin/sorular/sikayet/coz', { yontem: 'POST', govde: { ...parca(id), durum: 'resolved', eylem: ad === 'Yok say' ? 'yoksay' : 'coz' } }); tamam[id] = 'cozuldu'; }
      catch (e: any) { hata++; son = e.message; }
    }
    setYerelDurum((d) => ({ ...d, ...tamam }));
    temizle();
    bildir(hata ? `${Object.keys(tamam).length} kapatıldı, ${hata} başarısız: ${son}` : `${ids.length} şikâyet kapatıldı`, hata ? 'kotu' : 'iyi');
  };
  const soruYolu = (s: Satir) => `${SAYFA[s.kaynak]}/${encodeURIComponent(s.soruId)}`;
  const durumu = (s: Satir) => yerelDurum[s.id] || s.durum;
  return (
    <>
      <SayfaBasligi baslik="Soru şikâyetleri" aciklama="Öğrencilerin soru hata bildirimleri. Soruyu açıp düzeltin, sonra bildirimi çözüldü işaretleyin." />
      <VeriTablosu<Satir>
        kimlik="sorular-sikayet" kaynak="/api/admin/sorular/sikayet" canliOlay={['reports_changed', 'past_question_updated', 'past_questions_changed']}
        aramaYeri="Neden, ayrıntı, soru ya da kişi ara…" satirKimligi={(s) => s.id}
        satirTikla={(s) => setAcik(s)} etkin={acik?.id || null}
        dusur={(s) => acikSuzgec() && yerelDurum[s.id] === 'cozuldu'}
        secim topluEylemler={(ids, temizle) => (<>
          <button type="button" className="m16-btn birincil" onClick={() => void toplu(ids, 'Çözüldü', temizle)}>Çözüldü</button>
          <button type="button" className="m16-btn" onClick={() => void toplu(ids, 'Yok say', temizle)}>Yok say</button>
        </>)}
        suzgecler={[
          { anahtar: 'durum', etiket: 'Durum', secenekler: [{ deger: 'acik', etiket: 'Açık' }, { deger: 'cozuldu', etiket: 'Çözüldü' }, { deger: 'hepsi', etiket: 'Hepsi' }] },
          { anahtar: 'kaynak', etiket: 'Kaynak', secenekler: Object.entries(KAYNAK).map(([deger, etiket]) => ({ deger, etiket })) },
        ]}
        sutunlar={[
          { anahtar: 'at', baslik: 'Zaman', sirala: true, genislik: '100px', hucre: (s) => (s.at ? zamanMetni(s.at) : '—') },
          { anahtar: 'kaynak', baslik: 'Kaynak', genislik: '96px', hucre: (s) => <Rozet ton="bilgi">{KAYNAK[s.kaynak]}</Rozet> },
          { anahtar: 'neden', baslik: 'Bildirim', genislik: 'minmax(220px,2fr)', hucre: (s) => <span title={s.ayrinti}><b>{s.neden}</b>{s.ayrinti && ` — ${s.ayrinti}`}</span> },
          { anahtar: 'kok', baslik: 'Soru', genislik: 'minmax(160px,1.5fr)', hucre: (s) => <a href={manageAdres(`${SAYFA[s.kaynak]}/${encodeURIComponent(s.soruId)}`)} /* H255: adres manageAdres ile */ onClick={(e) => { e.preventDefault(); e.stopPropagation(); git(`${SAYFA[s.kaynak]}/${encodeURIComponent(s.soruId)}`); }}>{s.kok || s.soruId}</a> },
          { anahtar: 'kim', baslik: 'Kim', genislik: 'minmax(90px,0.8fr)', gizli: true },
          { anahtar: 'durum', baslik: 'İşlem', genislik: '130px', hucre: (s) => (durumu(s) === 'acik'
            ? <button type="button" className="m16-btn" onClick={(e) => { e.stopPropagation(); void coz(s, 'resolved'); }}>Çözüldü</button>
            : <button type="button" className="m16-btn hayalet" onClick={(e) => { e.stopPropagation(); void coz(s, 'pending'); }}>Yeniden aç</button>) },
        ]}
      />
      {acik && (
        <AyrintiCekmecesi acik kapat={() => setAcik(null)} baslik={acik.neden} altBaslik={`${KAYNAK[acik.kaynak]} · ${acik.soruId} · ${acik.at ? zamanMetni(acik.at) : ''}`} kayit={acik} hedef={`soru:${acik.soruId}`}
          eylemler={<>
            {durumu(acik) === 'acik'
              ? <button type="button" className="m16-btn birincil" onClick={() => void coz(acik, 'resolved')}>Çözüldü</button>
              : <button type="button" className="m16-btn hayalet" onClick={() => void coz(acik, 'pending')}>Yeniden aç</button>}
            <button type="button" className="m16-btn" onClick={() => git(soruYolu(acik))}>Soruyu aç</button>
          </>}>
          {/* H294: soru çekmecesi — şikâyet + soru özeti; düzeltme soru sayfasında, kapatma burada */}
          <dl className="m16-satirlar">
            <dt>Durum</dt><dd><Rozet ton={durumu(acik) === 'acik' ? 'uyari' : 'iyi'}>{durumu(acik) === 'acik' ? 'Açık' : 'Çözüldü'}</Rozet></dd>
            <dt>Bildirim</dt><dd style={{ whiteSpace: 'pre-wrap' }}>{acik.ayrinti || '—'}</dd>
            <dt>Soru</dt><dd>{acik.kok || acik.soruId}</dd>
            <dt>Ders / kurul</dt><dd>{acik.ders || '—'}{acik.kurul ? ` · Kurul ${acik.kurul}` : ''}</dd>
            <dt>Kim</dt><dd>{acik.kim || '—'}</dd>
          </dl>
        </AyrintiCekmecesi>
      )}
    </>
  );
}
