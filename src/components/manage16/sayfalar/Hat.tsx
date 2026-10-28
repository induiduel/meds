import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, Hata, Yukleniyor, IstatistikIzgara, IstatistikKart, adminIstek, bildir, onayIste, useAdminSorgu, zamanMetni, type Ton } from '../kit';
import type { SayfaProps } from '../menu';
import './ortak/ts16.css';

/**
 * Sistem › Hat — otomasyon/hat.json aşama defteri (salt okunur) + aşama durumları (meds_temp/hat/durum.json) + Kurul 2+ ders zinciri.
 * Uçlar: GET /api/admin/hat, /api/admin/hat/dersler, /api/admin/hat/eylemler, /api/admin/hat/gece.
 * Kural 20: ders zinciri eylemleri ve gece hattı Claude kullanır → yalnız elle, yazılı onayla (POST /api/admin/hat/eylem, /hat/gece/calistir).
 * Zamanlayıcılar maskelidir; buradan zamanlayıcı kurulmaz.
 */
const SEKME = [['asamalar', 'Aşama defteri'], ['dersler', 'Ders zinciri'], ['eylemler', 'Eylemler'], ['gunluk', 'Günlük']] as const;
const DURUM_TON: Record<string, Ton> = { hazir: 'iyi', el: 'uyari', plan: 'notr' };
const HUCRE_TON: Record<string, Ton> = { gecti: 'iyi', takildi: 'kotu', calisiyor: 'vurgu', bekliyor: 'notr' };
const EYLEM: Record<string, { ad: string; tehlikeli?: boolean }> = { surdur: { ad: 'Takılan aşamadan sürdür' }, denetci: { ad: 'Denetçiye gönder' }, bastan: { ad: 'Baştan üret', tehlikeli: true }, cek: { ad: 'Yayından çek', tehlikeli: true } };

function Asamalar({ v }: { v: any }) {
  const asamalar: any[] = v?.defter?.asamalar || [];
  const durum = v?.durum || {};
  const satirlar = asamalar.map((a) => ({ ...a, son: durum[a.id]?.son || '', kod: durum[a.id]?.kod, sonBasari: durum[a.id]?.son_basari || '' }));
  return (
    <>
      <p className="m16-ts-not" style={{ margin: '0 0 8px' }}>{v?.defter?.aciklama}</p>
      <VeriTablosu<any> kimlik="sistem-hat-asama" ogeler={satirlar} satirKimligi={(a) => a.id} aramaYeri="Aşama, komut ya da not ara…" adresteDurum={false}
        sutunlar={[
          { anahtar: 'id', baslik: 'Aşama', genislik: '150px', deger: (a) => a.id },
          { anahtar: 'kapsam', baslik: 'Kapsam', genislik: '80px', deger: (a) => a.kapsam },
          { anahtar: 'durum', baslik: 'Defter', genislik: '80px', deger: (a) => a.durum, hucre: (a) => <Rozet ton={DURUM_TON[a.durum] || 'notr'}>{a.durum}</Rozet> },
          { anahtar: 'tetik', baslik: 'Tetik', genislik: '110px', hucre: (a) => (a.tetik || []).join(', ') },
          { anahtar: 'gerekir', baslik: 'Gerekir', genislik: 'minmax(100px,1fr)', hucre: (a) => (a.gerekir || []).join(', ') || '—' },
          { anahtar: 'son', baslik: 'Son çalışma', genislik: '130px', deger: (a) => a.son, hucre: (a) => a.son ? <span title={a.son}>{zamanMetni(a.son)} {a.kod === 0 ? <Rozet ton="iyi">0</Rozet> : a.kod != null ? <Rozet ton="kotu">{a.kod}</Rozet> : null}</span> : '—' },
          { anahtar: 'komut', baslik: 'Komut', genislik: 'minmax(200px,2fr)', hucre: (a) => <code style={{ fontSize: 11 }}>{a.komut || '—'}</code> },
          { anahtar: 'not', baslik: 'Not', genislik: 'minmax(200px,2fr)', gizli: true, deger: (a) => a.not || '' },
        ]} />
    </>
  );
}

function Dersler({ git }: { git: SayfaProps['git'] }) {
  const s = useAdminSorgu<any>('/api/admin/hat/dersler');
  const v = s.veri;
  const eylem = async (ad: string, dersler: string[], temizle: () => void) => {
    const e = EYLEM[ad];
    if (!(await onayIste({
      baslik: `${e.ad}: ${dersler.length} ders`, tehlikeli: true, yazilacak: 'BASLAT', onayMetni: 'Elle başlat',
      aciklama: <>Ders zinciri Claude oturumları açar (kural 20: yalnız elle). Seçilen dersler sıraya alınır ve işleyici bu cihazda çalışır. {e.tehlikeli ? 'Bu eylem mevcut çıktıyı değiştirir.' : ''}</>,
    }))) return;
    try {
      const r = await adminIstek<any>('/api/admin/hat/eylem', { yontem: 'POST', govde: { eylem: ad, dersler, onay: true } });
      bildir(`${r.kuyruga?.length || 0} iş sıraya alındı${r.atlanan?.length ? `, ${r.atlanan.length} atlandı` : ''}`, r.success ? 'iyi' : 'bilgi');
      temizle(); void s.yenile();
    } catch (er: any) { bildir(er?.message || String(er), 'kotu'); }
  };
  if (s.hata) return <Hata hata={s.hata} yenile={s.yenile} />;
  if (!v) return <Yukleniyor satir={5} />;
  const asamalar: any[] = v.asamalar || [];
  return (
    <>
      {!v.cihaz && <p className="m16-ts-not">Bu sunucu cihaz değil: pano salt okunur, eylemler yalnız yerel panelden (Yerel hedef) başlar.</p>}
      {v.oracleHata && <p className="m16-ts-not">{v.oracleHata}</p>}
      <VeriTablosu<any> kimlik="sistem-hat-ders" ogeler={v.dersler || []} satirKimligi={(d) => d.id} aramaYeri="Ders ara…" adresteDurum={false}
        secim={v.cihaz} topluEylemler={(sec, temizle) => <>{Object.entries(EYLEM).map(([k, e]) => <button key={k} type="button" className={`m16-btn${e.tehlikeli ? ' tehlike' : ''}`} onClick={() => eylem(k, sec, temizle)}>{e.ad}…</button>)}</>}
        satirTikla={(d) => git(`icerik/dersler/${encodeURIComponent(d.id)}`)}
        sutunlar={[
          { anahtar: 'id', baslik: 'Ders', genislik: '90px', deger: (d) => d.id },
          { anahtar: 'ad', baslik: 'Konu', genislik: 'minmax(160px,2fr)', deger: (d) => `${d.ad} ${d.brans}` },
          ...asamalar.map((a) => ({
            anahtar: `h-${a.id}`, baslik: a.ad, genislik: '90px', deger: (d: any) => d.hucreler?.find((h: any) => h.asama === a.id)?.durum || '',
            hucre: (d: any) => { const h = d.hucreler?.find((x: any) => x.asama === a.id); return h ? <span title={h.not || ''}><Rozet ton={HUCRE_TON[h.durum] || 'notr'}>{h.durum}</Rozet></span> : '—'; },
          })),
          { anahtar: 'is', baslik: 'İş', genislik: '110px', hucre: (d) => d.is ? <Rozet ton="vurgu">{d.is.durum}</Rozet> : '' },
        ]} />
    </>
  );
}

function Eylemler() {
  const s = useAdminSorgu<any>('/api/admin/hat/eylemler', { aralikMs: 15000 });
  const g = useAdminSorgu<any>('/api/admin/hat/gece');
  const iptal = async (id: string) => {
    if (!(await onayIste({ baslik: 'Sıradaki iş iptal edilsin mi?', onayMetni: 'İptal et' }))) return;
    try { await adminIstek(`/api/admin/hat/eylem/${id}/iptal`, { yontem: 'POST', govde: {} }); bildir('İptal edildi', 'iyi'); void s.yenile(); } catch (e: any) { bildir(e?.message, 'kotu'); }
  };
  const gece = async () => {
    if (!(await onayIste({
      baslik: 'Gece hattı şimdi elle çalıştırılsın mı?', tehlikeli: true, yazilacak: 'BASLAT', onayMetni: 'Elle çalıştır',
      aciklama: <>hat.py --gece kurul geneli aşamaları ve ders zincirini çalıştırır; ders zinciri Claude kullanır (kural 20). Zamanlayıcı maskeli kalır, bu tek seferliktir.</>,
    }))) return;
    try { await adminIstek('/api/admin/hat/gece/calistir', { yontem: 'POST', govde: { onay: true } }); bildir('Gece hattı başlatıldı', 'iyi'); void g.yenile(); } catch (e: any) { bildir(e?.message, 'kotu'); }
  };
  return (
    <>
      <div className="m16-kart">
        <h2>Gece hattı</h2>
        <dl className="m16-satirlar">
          <dt>Durum</dt><dd>{g.veri ? (g.veri.calisiyor ? <Rozet ton="vurgu">Çalışıyor</Rozet> : <Rozet>{g.veri.durum}</Rozet>) : '…'}</dd>
          <dt>Son</dt><dd>{g.veri?.baslama ? `${zamanMetni(g.veri.baslama)} · ${g.veri.sonuc || ''}` : '—'}</dd>
        </dl>
        <div className="m16-ts-eylem" style={{ marginTop: 8 }}><button type="button" className="m16-btn" disabled={!g.veri?.cihaz || g.veri?.calisiyor} onClick={gece}>Elle çalıştır…</button></div>
      </div>
      {s.hata && <Hata hata={s.hata} yenile={s.yenile} />}
      <VeriTablosu<any> kimlik="sistem-hat-eylem" ogeler={s.veri?.isler || []} satirKimligi={(j) => j.id} adresteDurum={false}
        sutunlar={[
          { anahtar: 'olusturma', baslik: 'Zaman', genislik: '110px', deger: (j) => j.olusturma, hucre: (j) => zamanMetni(j.olusturma) },
          { anahtar: 'ders', baslik: 'Ders', genislik: '90px', deger: (j) => j.ders },
          { anahtar: 'eylem', baslik: 'Eylem', genislik: 'minmax(150px,1fr)', hucre: (j) => EYLEM[j.eylem]?.ad || j.eylem },
          { anahtar: 'durum', baslik: 'Durum', genislik: '100px', hucre: (j) => <Rozet ton={j.durum === 'hata' ? 'kotu' : j.durum === 'tamam' ? 'iyi' : 'notr'}>{j.durum}</Rozet> },
          { anahtar: 'kim', baslik: 'Kim', genislik: '140px' },
          { anahtar: 'x', baslik: '', genislik: '80px', hucre: (j) => j.durum === 'bekliyor' ? <button type="button" className="m16-btn hayalet" onClick={(e) => { e.stopPropagation(); void iptal(j.id); }}>İptal</button> : null },
        ]} />
    </>
  );
}

export default function Hat({ id, git }: SayfaProps) {
  const sekme = (SEKME.find(([k]) => k === id) || SEKME[0])[0];
  const s = useAdminSorgu<any>('/api/admin/hat');
  const v = s.veri;
  const asamalar: any[] = v?.defter?.asamalar || [];
  const hataliAsama = asamalar.filter((a) => v?.durum?.[a.id]?.kod && v.durum[a.id].kod !== 0).length;
  return (
    <>
      <SayfaBasligi baslik="Hat" aciklama="Aşama defteri (otomasyon/hat.json) salt okunur. LLM kullanan adımlar yalnız elle ve onayla başlar (kural 20)."
        eylemler={<button type="button" className="m16-btn" onClick={() => void s.yenile()}>Yenile</button>}>
        <nav className="m16-sekmeler">{SEKME.map(([k, ad]) => <button key={k} type="button" className={sekme === k ? 'on' : ''} onClick={() => git(`sistem/hat${k === 'asamalar' ? '' : `/${k}`}`, { degistir: true })}>{ad}</button>)}</nav>
      </SayfaBasligi>
      {s.hata && <Hata hata={s.hata} yenile={s.yenile} />}
      {v && (
        <IstatistikIzgara>
          <IstatistikKart etiket="Aşama" deger={asamalar.length} alt={`${asamalar.filter((a) => a.durum === 'hazir').length} hazır · ${asamalar.filter((a) => a.durum === 'el').length} elle · ${asamalar.filter((a) => a.durum === 'plan').length} plan`} />
          <IstatistikKart etiket="Son çalışmada hatalı" deger={hataliAsama} ton={hataliAsama ? 'kotu' : 'iyi'} />
          <IstatistikKart etiket="Tetikleyici" deger={Object.keys(v.defter?.tetikleyiciler || {}).length} alt="gece/açılış zamanlayıcıları maskeli" />
        </IstatistikIzgara>
      )}
      {sekme === 'asamalar' && (v ? <Asamalar v={v} /> : !s.hata && <Yukleniyor satir={5} />)}
      {sekme === 'dersler' && <Dersler git={git} />}
      {sekme === 'eylemler' && <Eylemler />}
      {sekme === 'gunluk' && <div className="m16-kart"><h2>hat.log (son 60 satır)</h2><pre className="m16-ts-log">{(v?.log || []).join('\n') || 'Günlük yok.'}</pre></div>}
    </>
  );
}
