import React, { useState } from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, JsonGoruntuleyici, adminIstek, bildir, durumTonu, zamanMetni, type DenetimSatiri, type ListeYaniti } from '../kit';
import type { SayfaProps } from '../menu';
import './ortak/ts16.css';

const goster = (v: unknown) => (v === undefined ? '—' : typeof v === 'string' ? v : JSON.stringify(v));

/** Önce/sonra fark tablosu (denetimFark ile yazılan ozet.fark) */
function FarkGorunumu({ fark }: { fark: Record<string, { once: unknown; sonra: unknown }> }) {
  return (
    <div className="m16-ts-fark" role="table" aria-label="Değişen alanlar">
      <strong>Alan</strong><strong>Önce</strong><strong>Sonra</strong>
      {Object.entries(fark).map(([k, f]) => (
        <React.Fragment key={k}><code>{k}</code><span className="once">{goster(f.once)}</span><span className="sonra">{goster(f.sonra)}</span></React.Fragment>
      ))}
    </div>
  );
}

const tarihIso = (v: string, gunSonu = false) => (v ? new Date(`${v}T${gunSonu ? '23:59:59' : '00:00:00'}`).toISOString() : undefined);

/** Sistem › Denetim kaydı — süzgeç (tür, sonuç, yöntem, kişi, tarih), önce/sonra fark görünümü, CSV/JSON dışa aktarım. */
export default function Denetim(_p: SayfaProps) {
  const ilk = new URLSearchParams(window.location.search);
  const [acik, setAcik] = useState<DenetimSatiri | null>(null);
  const [kim, setKim] = useState(ilk.get('kim') || '');
  const [hedef, setHedef] = useState(ilk.get('hedef') || '');
  const [bas, setBas] = useState(ilk.get('baslangic')?.slice(0, 10) || '');
  const [bit, setBit] = useState(ilk.get('bitis')?.slice(0, 10) || '');
  const [aktariyor, setAktariyor] = useState(false);
  const ekSorgu = { kim: kim || undefined, hedef: hedef || undefined, baslangic: tarihIso(bas), bitis: tarihIso(bit, true) };

  const disaAktar = async (bicim: 'csv' | 'json') => {
    setAktariyor(true);
    try {
      const u = new URLSearchParams(window.location.search);
      const sorgu: Record<string, unknown> = { ...ekSorgu, q: u.get('q') || undefined, boyut: 200 };
      u.forEach((v, k) => { if (k.startsWith('s.')) sorgu[k] = v; });
      const satirlar: DenetimSatiri[] = [];
      for (let sayfa = 0; sayfa < 25; sayfa++) {
        const r = await adminIstek<ListeYaniti<DenetimSatiri>>('/api/admin/denetim', { sorgu: { ...sorgu, sayfa } });
        satirlar.push(...r.ogeler);
        if (satirlar.length >= r.toplam || !r.ogeler.length) break;
      }
      let metin: string;
      if (bicim === 'json') metin = JSON.stringify(satirlar, null, 1);
      else {
        const alan = ['id', 'at', 'tur', 'kim', 'via', 'ip', 'yontem', 'uc', 'hedef', 'durum', 'sure_ms', 'ozet'] as const;
        const k = (v: unknown) => { const s = v == null ? '' : typeof v === 'object' ? JSON.stringify(v) : String(v); return /[",\n;]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
        metin = '﻿' + [alan.join(','), ...satirlar.map((s) => alan.map((a) => k((s as any)[a])).join(','))].join('\n');
      }
      const a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([metin], { type: bicim === 'json' ? 'application/json' : 'text/csv;charset=utf-8' }));
      a.download = `denetim-${new Date().toISOString().slice(0, 10)}.${bicim}`;
      a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 2000);
      bildir(`${satirlar.length} kayıt indirildi${satirlar.length >= 5000 ? ' (en çok 5000)' : ''}.`, 'iyi');
    } catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
    finally { setAktariyor(false); }
  };

  return (
    <>
      <SayfaBasligi baslik="Denetim kaydı" aciklama="Tüm yönetici yazma işlemleri ve kişisel veri okumaları (meds-pg yonetici_denetim)."
        eylemler={<div className="m16-ts-eylem">
          <button type="button" className="m16-btn" disabled={aktariyor} onClick={() => disaAktar('csv')}>CSV</button>
          <button type="button" className="m16-btn" disabled={aktariyor} onClick={() => disaAktar('json')}>JSON</button>
        </div>}>
        <div className="m16-ts-eylem" style={{ alignItems: 'center' }}>
          <input className="m16-girdi" placeholder="Kişi (e-posta)" value={kim} onChange={(e) => setKim(e.target.value)} aria-label="Kişiye göre süz" style={{ width: 170 }} />
          <input className="m16-girdi" placeholder="Hedef (ör. oda:3)" value={hedef} onChange={(e) => setHedef(e.target.value)} aria-label="Hedefe göre süz" style={{ width: 150 }} />
          <label className="m16-ts-not">Başlangıç <input className="m16-girdi" type="date" value={bas} onChange={(e) => setBas(e.target.value)} /></label>
          <label className="m16-ts-not">Bitiş <input className="m16-girdi" type="date" value={bit} onChange={(e) => setBit(e.target.value)} /></label>
          {(kim || hedef || bas || bit) && <button type="button" className="m16-btn hayalet" onClick={() => { setKim(''); setHedef(''); setBas(''); setBit(''); }}>Temizle</button>}
        </div>
      </SayfaBasligi>
      <VeriTablosu<DenetimSatiri>
        kimlik="sistem-denetim"
        kaynak="/api/admin/denetim"
        canliOlay={['denetim_eklendi']}
        aramaYeri="Uç, hedef ya da kişi ara…"
        satirKimligi={(s) => String(s.id)}
        etkin={acik ? String(acik.id) : null}
        satirTikla={setAcik}
        suzgecler={[
          { anahtar: 'tur', etiket: 'Tür', secenekler: [{ deger: 'yazma', etiket: 'Yazma' }, { deger: 'okuma', etiket: 'Okuma' }] },
          { anahtar: 'durum', etiket: 'Sonuç', secenekler: [{ deger: 'hata', etiket: 'Hatalı' }] },
          { anahtar: 'yontem', etiket: 'Yöntem', secenekler: ['POST', 'PUT', 'PATCH', 'DELETE', 'GET'].map((y) => ({ deger: y, etiket: y })) },
        ]}
        ekSorgu={ekSorgu}
        sutunlar={[
          { anahtar: 'at', baslik: 'Zaman', sirala: true, genislik: '120px', hucre: (s) => <time dateTime={s.at} title={new Date(s.at).toLocaleString('tr-TR')}>{zamanMetni(s.at)}</time> },
          { anahtar: 'yontem', baslik: 'İşlem', genislik: '112px', hucre: (s) => <Rozet ton={durumTonu(s.durum)}>{s.tur === 'okuma' ? 'OKUMA' : s.yontem} {s.durum}</Rozet> },
          { anahtar: 'uc', baslik: 'Uç', sirala: true, genislik: 'minmax(220px,2fr)', hucre: (s) => <code>{s.uc}</code> },
          { anahtar: 'hedef', baslik: 'Hedef', genislik: 'minmax(120px,1fr)' },
          { anahtar: 'kim', baslik: 'Kim', sirala: true, genislik: 'minmax(140px,1fr)' },
          { anahtar: 'fark', baslik: 'Fark', genislik: '64px', hucre: (s) => ((s.ozet as any)?.fark ? <Rozet ton="bilgi">{Object.keys((s.ozet as any).fark).length}</Rozet> : '') },
          { anahtar: 'sure_ms', baslik: 'Süre', sirala: true, genislik: '72px', hizala: 'sag', gizli: true, hucre: (s) => `${s.sure_ms ?? 0} ms` },
          { anahtar: 'ip', baslik: 'IP', genislik: '120px', gizli: true },
        ]}
      />
      <AyrintiCekmecesi acik={!!acik} kapat={() => setAcik(null)} baslik={acik?.uc || ''} altBaslik={acik ? `${acik.kim} · ${new Date(acik.at).toLocaleString('tr-TR')}` : ''} kayit={acik || undefined} hedef={acik?.hedef || undefined}>
        {acik && (
          <>
            <dl className="m16-satirlar">
              <dt>İşlem</dt><dd>{acik.tur === 'okuma' ? 'Kişisel veri okuması' : acik.yontem} · {acik.durum}</dd>
              <dt>Hedef</dt><dd>{acik.hedef || '—'}</dd>
              <dt>Kim / yol</dt><dd>{acik.kim} ({acik.via || '—'})</dd>
              <dt>IP</dt><dd>{(acik as any).ip || '—'}</dd>
              <dt>Süre</dt><dd>{acik.sure_ms} ms</dd>
            </dl>
            {(acik.ozet as any)?.fark && <><h3>Değişen alanlar</h3><FarkGorunumu fark={(acik.ozet as any).fark} /></>}
            <h3>Özet</h3>
            <JsonGoruntuleyici veri={acik.ozet} enYuksek={9999} />
          </>
        )}
      </AyrintiCekmecesi>
    </>
  );
}
