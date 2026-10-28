import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, Form, Yukleniyor, Hata, adminIstek, useAdminSorgu, onayIste, bildir, zamanMetni, type AlanTanim, type Ton } from '../kit';
import type { SayfaProps } from '../menu';
import { manageAdres } from '../menu';

/** Sorular › Çıkmış — 96 MB pastQuestions.json sunucuda sayfalanır; düzenleme kopya kardeşlere yazılır (syncPastMergeSiblings). */
type Satir = { id: string; kurul: string; ders: string; konu: string; yil: string; no: number; kok: string; cevap: string; sitede: string; durumlar: string[]; grup: string; sikayet: number; gizli: boolean; guncellendi: string };
type Meta = { toplam: number; yil: { deger: string; n: number }[]; kurul: { deger: string; n: number }[]; ders: { deger: string; n: number }[]; durum: { deger: string; n: number }[] };
const DURUM_ETIKET: Record<string, string> = { karantina: 'Karantina', gizli: 'Gizli', asil: 'Grup asılı', kopya: 'Kopya', onayli: 'Check-solve onaylı', faz14: 'Faz 14', sikayet: 'Açık şikâyet', cevapsiz: 'Cevapsız' };
const DURUM_TON: Record<string, Ton> = { karantina: 'kotu', gizli: 'uyari', kopya: 'bilgi', asil: 'vurgu', onayli: 'iyi', faz14: 'bilgi', sikayet: 'uyari', cevapsiz: 'kotu' };
const SITEDE: Record<string, [string, Ton]> = { gorunur: ['Sitede', 'iyi'], karantina: ['Karantinada', 'kotu'], birlesik: ['Kopya (gizli)', 'bilgi'], yok: ['Görünmüyor', 'uyari'] };

const ALANLAR: AlanTanim[] = [
  { ad: 'stem', etiket: 'Soru kökü', tur: 'uzun', zorunlu: true },
  { ad: 'options', etiket: 'Şıklar (JSON)', tur: 'json', zorunlu: true, ipucu: '[{"key":"A","text":"…"}, …]' },
  { ad: 'correctAnswer', etiket: 'Doğru cevap', zorunlu: true, enFazla: 4 },
  { ad: 'explanation', etiket: 'Açıklama', tur: 'uzun' },
  { ad: 'topic', etiket: 'Konu' },
  { ad: 'discipline', etiket: 'Ders' },
  { ad: 'examYear', etiket: 'Yıl' },
  { ad: 'questionNumber', etiket: 'Soru no', tur: 'sayi', enAz: 0 },
  { ad: 'tags', etiket: 'Etiketler', tur: 'etiketler' },
  { ad: 'adminNote', etiket: 'Yönetici notu', tur: 'uzun' },
];

// H256: ayrıntı bağlantıları panel içi git() ile (tam sayfa yenileme yok)
function Ayrinti({ id, kapat, git }: { id: string; kapat: () => void; git: SayfaProps['git'] }) {
  const yol = `/api/admin/sorular/cikmis/${encodeURIComponent(id)}`;
  const { veri, hata, yukleniyor, yenile, setVeri } = useAdminSorgu<any>(yol);
  const [kirli, setKirli] = React.useState(false);
  const [kardes, setKardes] = React.useState(true);
  const q = veri?.kayit;
  const deger = q ? { ...q, options: JSON.stringify(q.options || [], null, 1) } : {};
  const kaydet = async (_y: any, degisen: Record<string, unknown>) => {
    const yama: Record<string, unknown> = { ...degisen };
    if (typeof yama.options === 'string') yama.options = JSON.parse(yama.options as string);
    const r = await adminIstek<{ kayit: any; kardesler: string[] }>(yol, { yontem: 'PATCH', govde: { yama, kardeslereYaz: kardes } });
    setVeri({ ...veri, kayit: r.kayit }); setKirli(false);
    bildir(r.kardesler.length ? `Kaydedildi; ${r.kardesler.length} kopya kardeşe de yazıldı` : 'Kaydedildi', 'iyi');
  };
  const gizle = async () => {
    const yeni = !q?.hidden;
    if (!(await onayIste({ baslik: yeni ? 'Soru öğrencilerden gizlensin mi?' : 'Soru yeniden gösterilsin mi?', onayMetni: yeni ? 'Gizle' : 'Göster' }))) return;
    const r = await adminIstek<{ kayit: any }>(yol, { yontem: 'PATCH', govde: { yama: { hidden: yeni }, kardeslereYaz: false } });
    setVeri({ ...veri, kayit: r.kayit }); bildir(yeni ? 'Gizlendi' : 'Gösteriliyor', 'iyi');
  };
  const s = veri?.site;
  return (
    <AyrintiCekmecesi acik genis kapat={kapat} kirli={kirli} baslik={q?.topic || id} altBaslik={q ? `${q.committeeId} · ${q.discipline} · ${q.examYear || ''} #${q.questionNumber ?? ''}` : ''} kayit={q} hedef={`soru:${id}`}
      eylemler={q && <button type="button" className="m16-btn" onClick={() => gizle().catch((e) => bildir(e.message, 'kotu'))}>{q.hidden ? 'Göster' : 'Gizle'}</button>}>
      {hata ? <Hata hata={hata} yenile={yenile} /> : yukleniyor && !q ? <Yukleniyor satir={8} /> : q && (
        <>
          <div className="m16-kart">
            <h2>Sitedeki durum</h2>
            <dl className="m16-satirlar">
              <dt>Görünüm</dt><dd><Rozet ton={SITEDE[s?.durum]?.[1] || 'notr'}>{SITEDE[s?.durum]?.[0] || s?.durum}</Rozet>{s?.gosteren && <> · gösterilen kopya <a href={manageAdres(`sorular/cikmis/${s.gosteren}`)} onClick={(e) => { e.preventDefault(); git(`sorular/cikmis/${s.gosteren}`); }}>{s.gosteren}</a></>}</dd>
              {s?.karantinaNedeni?.length > 0 && (<><dt>Karantina nedeni</dt><dd>{s.karantinaNedeni.join(', ')}</dd></>)}
              <dt>Cevap anahtarı</dt><dd>{s?.cevap || q.correctAnswer || '—'} {s?.cevapDurumu && <Rozet ton="bilgi">{s.cevapDurumu}</Rozet>} {s?.cevapSupheli && <Rozet ton="uyari">Şüpheli</Rozet>} {s?.cevapNotu && <small>{s.cevapNotu}</small>}</dd>
              <dt>Check-solve</dt><dd>{veri.checkSolve ? `${veri.checkSolve.durum}${veri.checkSolve.gerekce ? ` — ${veri.checkSolve.gerekce}` : ''}` : '—'}</dd>
              <dt>Birleşme grubu</dt><dd>{veri.grup ? <><a href={manageAdres(`sorular/birlesen/${veri.grup.id}`)} onClick={(e) => { e.preventDefault(); git(`sorular/birlesen/${veri.grup.id}`); }}>{veri.grup.id}</a> · {veri.grup.uyeler.length} kopya · asıl {veri.grup.asil === id ? 'bu soru' : veri.grup.asil}</> : '—'}</dd>
              <dt>Şikâyet</dt><dd>{(q.reports || []).length} ({(q.reports || []).filter((r: any) => !r.status || r.status === 'pending').length} açık)</dd>
            </dl>
          </div>
          {veri.grup && <label className="m16-cip"><input type="checkbox" checked={kardes} onChange={(e) => setKardes(e.target.checked)} /> İçerik düzeltmesini gruptaki tüm kopyalara yaz (önerilir)</label>}
          <Form alanlar={ALANLAR} deger={deger} kaydet={kaydet} kirliDegisti={setKirli} />
        </>
      )}
    </AyrintiCekmecesi>
  );
}

export default function CikmisSorular({ id, git }: SayfaProps) {
  const { veri: meta } = useAdminSorgu<Meta>('/api/admin/sorular/cikmis/meta');
  const sec = (l?: { deger: string; n: number }[], f: (x: string) => string = (x) => x) => (l || []).map((x) => ({ deger: x.deger, etiket: f(x.deger) }));
  return (
    <>
      <SayfaBasligi baslik="Çıkmış sorular" aciklama={`Ham kayıt + sitedeki görünüm (karantina, birleşme, Faz 14). ${meta ? `${meta.toplam.toLocaleString('tr-TR')} soru.` : ''}`} />
      <VeriTablosu<Satir>
        kimlik="sorular-cikmis" kaynak="/api/admin/sorular/cikmis" canliOlay={['past_questions_changed', 'past_question_updated']}
        aramaYeri="Kimlik, kök, konu, ders ya da sınav ara…" satirKimligi={(s) => s.id} etkin={id || null}
        satirTikla={(s) => git(`sorular/cikmis/${encodeURIComponent(s.id)}${window.location.search}`)}
        suzgecler={[
          { anahtar: 'kurul', etiket: 'Kurul', secenekler: sec(meta?.kurul, (k) => (/^\d$/.test(k) ? `Kurul ${k}` : k)) },
          { anahtar: 'yil', etiket: 'Yıl', secenekler: sec(meta?.yil) },
          { anahtar: 'durum', etiket: 'Durum', secenekler: sec(meta?.durum, (k) => DURUM_ETIKET[k] || k) },
          { anahtar: 'sitede', etiket: 'Sitede', secenekler: Object.entries(SITEDE).map(([deger, [etiket]]) => ({ deger, etiket })) },
          { anahtar: 'ders', etiket: 'Ders', secenekler: sec(meta?.ders) },
        ]}
        sutunlar={[
          { anahtar: 'no', baslik: 'No', sirala: true, genislik: '56px', hizala: 'sag' },
          { anahtar: 'kok', baslik: 'Soru', genislik: 'minmax(240px,3fr)', hucre: (s) => <span title={s.kok}>{s.kok || s.konu}</span> },
          { anahtar: 'ders', baslik: 'Ders', sirala: true, genislik: 'minmax(100px,1fr)' },
          { anahtar: 'yil', baslik: 'Yıl', sirala: true, genislik: '96px' },
          { anahtar: 'cevap', baslik: 'Cevap', genislik: '72px', hizala: 'orta' }, // H176: 56px'te başlık "Cev…" kesiliyordu
          { anahtar: 'sitede', baslik: 'Sitede', genislik: '110px', hucre: (s) => <Rozet ton={SITEDE[s.sitede]?.[1]}>{SITEDE[s.sitede]?.[0]}</Rozet> },
          { anahtar: 'durumlar', baslik: 'Bayraklar', genislik: 'minmax(140px,1.2fr)', hucre: (s) => <>{s.durumlar.filter((d) => d !== 'onayli').map((d) => <Rozet key={d} ton={DURUM_TON[d]}>{DURUM_ETIKET[d] || d}</Rozet>)}</> },
          { anahtar: 'sikayet', baslik: 'Şikâyet', sirala: true, genislik: '64px', hizala: 'sag', gizli: true },
          { anahtar: 'guncellendi', baslik: 'Güncellendi', sirala: true, genislik: '104px', hucre: (s) => (s.guncellendi ? zamanMetni(s.guncellendi) : '—') },
        ]}
      />
      {id && <Ayrinti id={id} git={git} kapat={() => git(`sorular/cikmis${window.location.search}`)} />}
    </>
  );
}
