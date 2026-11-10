import React, { useMemo, useState } from 'react';
import { Check, ChevronRight, FileDown, ListChecks, Loader2, PencilLine, ToggleLeft } from 'lucide-react';
import { printDocument, renderPdfOnServer } from '../../pdf/pdfDocument';
import { gorselUrl, konulariAl, type EkModul } from './ekVeri';
import { EkMd } from './ekOrtak';
import { HocaSetCoz } from './EkHoca';
import { TUR_AD, TUR_SIRA, foyBelge, foySorulari, sanalSet, type Tur } from './ekFoyBelge';

/**
 * Çalışma föyü: hocanın çalışma soruları KONUYA göre düzenlenmiş hâli (foy.json: konu → bilgi özeti + set/no listeleri).
 * Konu sayfası: görsel + "Bilmen gerekenler" + üç alıştırma (boşluk doldurma, doğru–yanlış, çoktan seçmeli).
 * "PDF oluştur": seçilen konuların föyü (cevap anahtarlı ya da anahtarsız) sunucuda PDF'e çevrilir (/api/pdf/render),
 * sunucu yanıt vermezse tarayıcının yazdırma penceresi açılır.
 */
async function gorselleriAl(m: EkModul, dosyalar: string[]): Promise<Record<string, string>> {
  const out: Record<string, string> = {};
  await Promise.all([...new Set(dosyalar)].map(async (d) => {
    try {
      const r = await fetch(gorselUrl(m.ozet.id, d));
      if (r.ok) out[d] = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(await r.text())}`;
    } catch { /* görselsiz basılır */ }
  }));
  return out;
}

/** PDF oluşturma kutusu: konu seçimi + cevap anahtarı; tek konu sayfasında yalnız o konu */
export const FoyPdf: React.FC<{ m: EkModul; yalniz?: string }> = ({ m, yalniz }) => {
  const konular = konulariAl(m);
  const [secili, setSecili] = useState<string[]>(yalniz ? [yalniz] : konular.map((k) => k.id));
  const [anahtar, setAnahtar] = useState(true);
  const [durum, setDurum] = useState<'' | 'is' | 'hata'>('');
  const uret = async () => {
    if (!secili.length || durum === 'is') return;
    setDurum('is');
    const sira = konular.filter((k) => secili.includes(k.id));
    const g = await gorselleriAl(m, [m.ozet.kapak, ...sira.map((k) => k.gorsel)]);
    const html = foyBelge(m, secili, anahtar, g);
    const ad = `${m.ozet.id}-calisma-foyu${sira.length === 1 ? `-${sira[0].id}` : ''}.pdf`;
    try {
      const blob = await renderPdfOnServer(html, `${m.ozet.ad} — Çalışma föyü`, ad);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = ad; document.body.appendChild(a); a.click(); a.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 30000);
      setDurum('');
    } catch {
      // sunucu PDF üretemedi: tarayıcının yazdırma penceresi ("PDF olarak kaydet")
      try { await printDocument(html); setDurum(''); } catch { setDurum('hata'); }
    }
  };
  const degis = (id: string) => setSecili((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]));
  return (
    <section className="ekm-foy-pdf v15-card" aria-label="PDF oluştur">
      <h3><FileDown aria-hidden /> PDF oluştur</h3>
      {!yalniz && (
        <>
          <div className="ekm-foy-sec">
            <button type="button" className="ekm-kucuk" onClick={() => setSecili(secili.length === konular.length ? [] : konular.map((k) => k.id))}>{secili.length === konular.length ? 'Hiçbiri' : 'Hepsi'}</button>
            {konular.map((k) => (
              <button key={k.id} type="button" className={`ekm-kucuk${secili.includes(k.id) ? ' is-on' : ''}`} aria-pressed={secili.includes(k.id)} onClick={() => degis(k.id)} title={k.baslik}>{k.id}</button>
            ))}
          </div>
          <p className="ekm-foy-not">{secili.length} konu seçili. Föyde her konunun görseli, bilgi özeti ve çalışma soruları basılır.</p>
        </>
      )}
      <div className="ekm-foy-alt">
        <button type="button" className={`ekm-kucuk is-oto${anahtar ? ' is-on' : ''}`} aria-pressed={anahtar} onClick={() => setAnahtar(!anahtar)}><Check aria-hidden /> Cevap anahtarı</button>
        <button type="button" className="v15-btn" onClick={uret} disabled={!secili.length || durum === 'is'}>
          {durum === 'is' ? <><Loader2 aria-hidden className="ekm-don" /> Hazırlanıyor…</> : <><FileDown aria-hidden /> {yalniz ? 'Bu konunun föyünü indir' : 'Föyü PDF olarak indir'}</>}
        </button>
      </div>
      {durum === 'hata' && <p className="ekm-foy-not is-hata">PDF oluşturulamadı. Bağlantını denetleyip yeniden dene.</p>}
    </section>
  );
};

export const FoyListe: React.FC<{ m: EkModul; ac: (konu: string) => void }> = ({ m, ac }) => (
  <>
    <ol className="ekm-foy-liste" role="list">
      {konulariAl(m).map((k) => {
        const s = foySorulari(m, k.id);
        const n = s.bosluk.length + s.dy.length + s.cs.length;
        return (
          <li key={k.id}>
            <button type="button" className="v15-card" onClick={() => ac(k.id)}>
              <i>{k.id}</i>
              <span><b>{k.baslik}</b><small>{n} soru · {s.bosluk.length} boşluk · {s.dy.length} doğru–yanlış · {s.cs.length} çoktan seçmeli</small></span>
              <ChevronRight aria-hidden />
            </button>
          </li>
        );
      })}
    </ol>
    <FoyPdf m={m} />
  </>
);

export const FoyKonu: React.FC<{ m: EkModul; konuId: string }> = ({ m, konuId }) => {
  const konu = konulariAl(m).find((k) => k.id === konuId)!;
  const f = m.foy?.konular.find((x) => x.id === konuId);
  const s = useMemo(() => foySorulari(m, konuId), [m, konuId]);
  const [tur, setTur] = useState<Tur | null>(null);
  if (tur) {
    return (
      <div className="ekm">
        <button type="button" className="v15-btn is-ghost ekm-goster" onClick={() => setTur(null)}>← {konu.baslik}</button>
        <HocaSetCoz key={tur} set={sanalSet(konuId, tur, s[tur])} />
      </div>
    );
  }
  const SIMGE = { bosluk: PencilLine, dy: ToggleLeft, cs: ListChecks };
  return (
    <div className="ekm">
      <figure className="ekm-gorsel v15-card"><img src={gorselUrl(m.ozet.id, konu.gorsel)} alt={konu.gorsel_alt} /></figure>
      <section className="ekm-foy-bilgi v15-card">
        <h3>Bilmen gerekenler</h3>
        <ul>{(f?.bilgiler || []).map((x) => <li key={x}><EkMd md={x} /></li>)}</ul>
      </section>
      <div className="ekm-foy-turler">
        {TUR_SIRA.filter((t) => s[t].length).map((t) => {
          const S = SIMGE[t];
          return (
            <button key={t} type="button" className={`v15-card is-${t}`} onClick={() => setTur(t)}>
              <S aria-hidden /><b>{TUR_AD[t]}</b><span>{s[t].length} soru</span>
            </button>
          );
        })}
      </div>
      <FoyPdf m={m} yalniz={konuId} />
    </div>
  );
};
