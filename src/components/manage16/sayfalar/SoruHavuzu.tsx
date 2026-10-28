import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, Form, Yukleniyor, Hata, adminIstek, useAdminSorgu, onayIste, bildir, zamanMetni, type AlanTanim } from '../kit';
import type { SayfaProps } from '../menu';

/** Sorular › Havuz — sunucu sayfalı havuz (db.questions); düzenle, gizle/göster, birleştir (taslak birleştirme ucu). */
type Satir = { id: string; kurul: string; ders: string; konu: string; no: number; durum: string; kaynak: string; gizli: boolean; kok: string; cevap: string; katki: number; sikayet: number; guncellendi: string };
const DURUM: Record<string, string> = { completed: 'Tamamlandı', reconstructing: 'Kuruluyor', gathering: 'Toplanıyor', empty: 'Boş' };
const KAYNAK: Record<string, string> = { cikmis: 'Çıkmış', ogrenci: 'Öğrenci', diger: 'Diğer' };
const KURUL = ['1', '2', '3', '4', '5', '6'].map((k) => ({ deger: k, etiket: `Kurul ${k}` }));

const ALANLAR: AlanTanim[] = [
  { ad: 'topic', etiket: 'Konu', enFazla: 200 },
  { ad: 'discipline', etiket: 'Ders' },
  { ad: 'questionNumber', etiket: 'Soru no', tur: 'sayi', enAz: 0 },
  { ad: 'status', etiket: 'Durum', tur: 'secim', secenekler: Object.entries(DURUM).map(([deger, etiket]) => ({ deger, etiket })) },
  { ad: 'claimedAnswer', etiket: 'Öne sürülen cevap', enFazla: 4 },
  { ad: 'tags', etiket: 'Etiketler', tur: 'etiketler' },
  { ad: 'adminNote', etiket: 'Yönetici notu', tur: 'uzun' },
  { ad: 'hidden', etiket: 'Öğrencilerden gizle', tur: 'anahtar' },
];

export function Ayrinti({ id, kapat }: { id: string; kapat: () => void }) {
  const { veri, hata, yukleniyor, yenile, setVeri } = useAdminSorgu<{ kayit: any }>(`/api/admin/sorular/havuz/${encodeURIComponent(id)}`);
  const [kirli, setKirli] = React.useState(false);
  const q = veri?.kayit;
  const kaydet = async (_y: any, degisen: Record<string, unknown>) => {
    const r = await adminIstek<{ kayit: any }>(`/api/admin/sorular/havuz/${encodeURIComponent(id)}`, { yontem: 'PATCH', govde: { yama: degisen } });
    setVeri({ kayit: r.kayit }); setKirli(false); bildir('Kaydedildi', 'iyi');
  };
  const gizle = async () => {
    const yeni = !q?.hidden;
    if (!(await onayIste({ baslik: yeni ? 'Soru öğrencilerden gizlensin mi?' : 'Soru yeniden gösterilsin mi?', onayMetni: yeni ? 'Gizle' : 'Göster' }))) return;
    await kaydet(null, { hidden: yeni });
  };
  return (
    <AyrintiCekmecesi acik kapat={kapat} kirli={kirli} baslik={q?.topic || id} altBaslik={q ? `${q.committeeId} · ${q.discipline} · #${q.questionNumber}` : ''} kayit={q} hedef={`soru:${id}`}
      eylemler={q && <button type="button" className="m16-btn" onClick={gizle}>{q.hidden ? 'Göster' : 'Gizle'}</button>}>
      {hata ? <Hata hata={hata} yenile={yenile} /> : yukleniyor && !q ? <Yukleniyor satir={6} /> : q && (
        <>
          <div className="m16-kart"><h2>Soru kökü</h2><p>{q.reconstruction?.stem || q.rawStem || '—'}</p>
            <ul className="m16-liste">{(q.reconstruction?.options || q.options || []).map((o: any) => <li key={o.key}><b>{o.key})</b> {o.text}</li>)}</ul>
            <p>Cevap: <b>{q.reconstruction?.correctAnswer || q.correctAnswer || q.claimedAnswer || '—'}</b> · Katkı: {(q.fragments || []).length}</p>
          </div>
          <Form alanlar={ALANLAR} deger={q} kaydet={kaydet} kirliDegisti={setKirli} />
        </>
      )}
    </AyrintiCekmecesi>
  );
}

export default function SoruHavuzu({ id, git }: SayfaProps) {
  const birlestir = async (ids: string[], temizle: () => void) => {
    if (ids.length < 2) { bildir('En az iki soru seçin', 'bilgi'); return; }
    // H153: asıl soru onay penceresinde açıkça seçilir (eskiden görünmeyen seçim sırası belirliyordu)
    let capa = ids[0];
    if (!(await onayIste({
      baslik: `${ids.length} soru birleştirilsin mi?`,
      aciklama: (
        <>
          <label className="m16-alan">
            <span>Asıl kalacak soru</span>
            <select className="m16-girdi" defaultValue={capa} onChange={(e) => { capa = e.target.value; }}>
              {ids.map((x) => <option key={x} value={x}>{x}</option>)}
            </select>
          </label>
          <p>Diğer {ids.length - 1} soru kaldırılır. Ham defter kaldırılanları saklar.</p>
        </>
      ),
      tehlikeli: true, yazilacak: 'BIRLESTIR', onayMetni: 'Birleştir',
    }))) return;
    const uydular = ids.filter((x) => x !== capa);
    try {
      const { kayit } = await adminIstek<{ kayit: any }>(`/api/admin/sorular/havuz/${encodeURIComponent(capa)}`);
      await adminIstek('/api/admin/drafts/merge', { yontem: 'POST', govde: { consolidated: kayit, mergedIds: uydular } });
      bildir('Birleştirildi', 'iyi'); temizle();
    } catch (e: any) { bildir(e.message, 'kotu'); }
  };
  const topluGizle = async (ids: string[], gizli: boolean, temizle: () => void) => {
    if (!(await onayIste({ baslik: `${ids.length} soru ${gizli ? 'gizlensin' : 'gösterilsin'} mi?` }))) return;
    let n = 0;
    for (const x of ids) { try { await adminIstek(`/api/admin/sorular/havuz/${encodeURIComponent(x)}`, { yontem: 'PATCH', govde: { yama: { hidden: gizli } } }); n++; } catch { /* */ } }
    bildir(`${n}/${ids.length} soru güncellendi`, n === ids.length ? 'iyi' : 'kotu'); temizle();
  };
  return (
    <>
      <SayfaBasligi baslik="Soru havuzu" aciklama="Öğrencilerin hatırladığı parçalardan kurulan güncel havuz. Liste sunucuda sayfalanır." />
      <VeriTablosu<Satir>
        kimlik="sorular-havuz" kaynak="/api/admin/sorular/havuz" canliOlay={['questions_changed', 'question_updated']}
        aramaYeri="Kimlik, konu, kök ya da etiket ara…" satirKimligi={(s) => s.id} etkin={id || null}
        satirTikla={(s) => git(`sorular/havuz/${encodeURIComponent(s.id)}${window.location.search}`)}
        secim topluEylemler={(sec, tem) => (<>
          <button type="button" className="m16-btn" onClick={() => topluGizle(sec, true, tem)}>Gizle</button>
          <button type="button" className="m16-btn" onClick={() => topluGizle(sec, false, tem)}>Göster</button>
          <button type="button" className="m16-btn tehlike" onClick={() => birlestir(sec, tem)}>Birleştir</button>
        </>)}
        suzgecler={[
          { anahtar: 'kurul', etiket: 'Kurul', secenekler: KURUL },
          { anahtar: 'durum', etiket: 'Durum', secenekler: Object.entries(DURUM).map(([deger, etiket]) => ({ deger, etiket })) },
          { anahtar: 'kaynak', etiket: 'Kaynak', secenekler: Object.entries(KAYNAK).map(([deger, etiket]) => ({ deger, etiket })) },
          { anahtar: 'gizli', etiket: 'Görünürlük', secenekler: [{ deger: 'evet', etiket: 'Gizli' }, { deger: 'hayir', etiket: 'Açık' }] },
        ]}
        sutunlar={[
          { anahtar: 'no', baslik: 'No', sirala: true, genislik: '60px', hizala: 'sag' },
          { anahtar: 'kok', baslik: 'Soru', genislik: 'minmax(240px,3fr)', hucre: (s) => <span title={s.kok}>{s.kok || s.konu || s.id}</span> },
          { anahtar: 'ders', baslik: 'Ders', sirala: true, genislik: 'minmax(110px,1fr)' },
          { anahtar: 'kurul', baslik: 'Kurul', genislik: '64px', hucre: (s) => s.kurul || '—' },
          { anahtar: 'durum', baslik: 'Durum', genislik: '120px', hucre: (s) => <>{s.gizli && <Rozet ton="uyari">Gizli</Rozet>} <Rozet ton={s.durum === 'completed' ? 'iyi' : 'notr'}>{DURUM[s.durum] || s.durum}</Rozet></> },
          { anahtar: 'katki', baslik: 'Katkı', sirala: true, genislik: '64px', hizala: 'sag' },
          { anahtar: 'kaynak', baslik: 'Kaynak', genislik: '80px', gizli: true, hucre: (s) => KAYNAK[s.kaynak] },
          { anahtar: 'guncellendi', baslik: 'Güncellendi', sirala: true, genislik: '110px', hucre: (s) => (s.guncellendi ? zamanMetni(s.guncellendi) : '—') },
        ]}
      />
      {id && <Ayrinti id={id} kapat={() => git(`sorular/havuz${window.location.search}`)} />}
    </>
  );
}
