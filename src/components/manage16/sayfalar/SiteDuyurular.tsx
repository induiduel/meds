import React, { useEffect, useState } from 'react';
import { SayfaBasligi, Hata, Yukleniyor, Rozet, onayIste, yazimHedefi } from '../kit';
import type { SayfaProps } from '../menu';
import { Anahtar, isoTarih, siteAyarYaz, useSiteAyarAdmin, yerelTarih, type Duyuru } from './ortak/siteAyarOrtak';

/**
 * Site › Duyurular: site üstü bant (site_ayar.duyuru; öğrenci tarafı components/system/DuyuruBandi.tsx, SSE ile anında).
 * Tek etkin duyuru. Push/e-posta bildirimi ayrı (Bildirim gönder) — bu sayfa yalnız bandı yönetir.
 */
const BOS: Duyuru = { acik: false, metin: '', ton: 'bilgi' };
const TON: { d: Duyuru['ton']; etiket: string }[] = [{ d: 'bilgi', etiket: 'Bilgi' }, { d: 'uyari', etiket: 'Uyarı' }, { d: 'hata', etiket: 'Kesinti' }];

export default function SiteDuyurular(_p: SayfaProps) {
  const { veri: a, hata, yenile, setVeri } = useSiteAyarAdmin();
  const [f, setF] = useState<Duyuru>(BOS);
  const [kurulMetin, setKurulMetin] = useState('');
  const [mesgul, setMesgul] = useState(false);
  useEffect(() => { if (a) { const d = a.duyuru || BOS; setF(d); setKurulMetin((d.kurul || []).join(', ')); } }, [a?.surum]);
  if (hata && !a) return <><SayfaBasligi baslik="Duyurular" /><Hata hata={hata} yenile={yenile} /></>;
  if (!a) return <><SayfaBasligi baslik="Duyurular" /><Yukleniyor /></>;
  const kurul = kurulMetin.split(/[,\s]+/).map(Number).filter((n) => Number.isInteger(n) && n >= 1 && n <= 12);
  const yayinda = !!a.duyuru?.acik && !(a.duyuru.bitis && Date.parse(a.duyuru.bitis) < Date.now());
  const kaydet = async (acik: boolean) => {
    if (acik && !f.metin.trim()) return;
    const d: Duyuru = { ...f, acik, metin: f.metin.trim(), ...(kurul.length ? { kurul } : { kurul: undefined }) };
    if (!d.baglanti) delete d.baglanti;
    // H181: yayınlama onayı yazım hedefini (canlı site / yerel sunucu) söyler; önceden onaysız gidiyordu
    if (acik && !(await onayIste({ baslik: 'Duyuru yayınlansın mı?', aciklama: <>Açık sekmelerdeki {kurul.length ? `Kurul ${kurul.join(', ')}` : 'tüm'} öğrencilere anında görünür. Hedef: <b>{yazimHedefi()}</b>.</>, onayMetni: 'Yayınla' }))) return;
    setMesgul(true);
    const r = await siteAyarYaz({ duyuru: d }, acik ? 'Duyuru yayında' : 'Duyuru kaydedildi (kapalı)');
    if (r) setVeri(r as any);
    setMesgul(false);
  };
  const set = (p: Partial<Duyuru>) => setF((x) => ({ ...x, ...p }));
  return (
    <>
      <SayfaBasligi baslik="Duyurular" aciklama="Sitenin üstünde görünen bant. Kaydedince açık sekmelere anında gider; öğrenci kapatabilir (metin değişince yeniden çıkar)." />
      <div className="m16-izgara-2">
        <section className="m16-kart">
          <h2>Duyuru {yayinda ? <Rozet ton="iyi">yayında</Rozet> : <Rozet ton="notr">kapalı</Rozet>}</h2>
          <label style={{ display: 'grid', gap: 4 }}>
            <span>Metin</span>
            <textarea className="m16-girdi" rows={3} maxLength={500} value={f.metin} onChange={(e) => set({ metin: e.target.value })} placeholder="ör. Kurul 2 sınav soruları yayında." />
          </label>
          <div style={{ marginTop: 12 }}>
            <span>Tür </span>
            <span className="m16-cip-grup" role="radiogroup" aria-label="Duyuru türü" style={{ display: 'inline-flex' }}>
              {TON.map((t) => <button key={t.d} type="button" role="radio" aria-checked={f.ton === t.d} className={`m16-cip ${f.ton === t.d ? 'on' : ''}`} onClick={() => set({ ton: t.d })}>{t.etiket}</button>)}
            </span>
          </div>
          <label style={{ display: 'grid', gap: 4, marginTop: 12 }}>
            <span>Bağlantı (isteğe bağlı; site içi /… ya da https://…)</span>
            <input className="m16-girdi" maxLength={300} value={f.baglanti || ''} onChange={(e) => set({ baglanti: e.target.value })} placeholder="/guncellemeler" />
          </label>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginTop: 12 }}>
            <label style={{ display: 'grid', gap: 4 }}><span>Başlangıç</span>
              <input type="datetime-local" className="m16-girdi" value={yerelTarih(f.baslangic)} onChange={(e) => set({ baslangic: isoTarih(e.target.value) })} /></label>
            <label style={{ display: 'grid', gap: 4 }}><span>Bitiş</span>
              <input type="datetime-local" className="m16-girdi" value={yerelTarih(f.bitis)} onChange={(e) => set({ bitis: isoTarih(e.target.value) })} /></label>
          </div>
          <label style={{ display: 'grid', gap: 4, marginTop: 12 }}>
            <span>Hedef kurul (boş: herkes; takvimdeki aktif kurula göre)</span>
            <input className="m16-girdi" value={kurulMetin} onChange={(e) => setKurulMetin(e.target.value)} placeholder="ör. 2, 3" />
          </label>
          <label style={{ display: 'flex', gap: 8, alignItems: 'center', marginTop: 12 }}>
            <Anahtar acik={f.kapatilabilir !== false} etiket="Öğrenci kapatabilsin" degistir={(v) => set({ kapatilabilir: v ? undefined : false })} />
            <span>Öğrenci kapatabilsin</span>
          </label>
          <div style={{ display: 'flex', gap: 8, marginTop: 16, flexWrap: 'wrap' }}>
            <button type="button" className="m16-btn birincil" disabled={mesgul || !f.metin.trim()} onClick={() => void kaydet(true)}>Yayınla</button>
            <button type="button" className="m16-btn" disabled={mesgul} onClick={() => void kaydet(false)}>{yayinda ? 'Yayından kaldır' : 'Kapalı kaydet'}</button>
            {a.duyuru && (
              <button type="button" className="m16-btn hayalet" disabled={mesgul} onClick={async () => {
                if (!(await onayIste({ baslik: 'Duyuru silinsin mi?', aciklama: `Metin ve ayarlar temizlenir. Hedef: ${yazimHedefi()}.`, onayMetni: 'Sil' }))) return;
                setMesgul(true); const r = await siteAyarYaz({ duyuru: null }, 'Duyuru silindi'); if (r) setVeri(r as any); setMesgul(false);
              }}>Sil</button>
            )}
          </div>
        </section>
        <section className="m16-kart">
          <h2>Önizleme</h2>
          {f.metin.trim() ? (
            <div className={`sh-duyuru is-${f.ton}`} style={{ borderRadius: 8, padding: '8px 12px', background: `color-mix(in srgb, var(--color-${f.ton === 'hata' ? 'bad' : f.ton === 'uyari' ? 'warn' : 'accent'}) 12%, var(--color-white))` }}>
              <span>{f.metin} {f.baglanti && <u>Ayrıntı</u>}</span>
            </div>
          ) : <p style={{ color: 'var(--color-ink-3)' }}>Metin yazınca bant burada görünür.</p>}
          <dl className="m16-satirlar" style={{ marginTop: 12 }}>
            <dt>Hedef</dt><dd>{kurul.length ? `Kurul ${kurul.join(', ')}` : 'Herkes'}</dd>
            <dt>Zaman</dt><dd>{f.baslangic ? new Date(f.baslangic).toLocaleString('tr-TR') : 'hemen'} → {f.bitis ? new Date(f.bitis).toLocaleString('tr-TR') : 'süresiz'}</dd>
          </dl>
        </section>
      </div>
    </>
  );
}
