import React, { useState } from 'react';
import { SayfaBasligi, IstatistikIzgara, IstatistikKart, Rozet, Hata, Yukleniyor, adminIstek, bildir, onayIste, useAdminSorgu, zamanMetni, type Ton } from '../kit';
import type { SayfaProps } from '../menu';
import './ortak/ts16.css';

type Servis = { id: string; label: string; actions: string[]; self?: boolean; note?: string; active: string; sub?: string; since?: string };
const sure = (sn: number) => (sn > 86400 ? `${Math.floor(sn / 86400)} g ${Math.floor((sn % 86400) / 3600)} sa` : sn > 3600 ? `${Math.floor(sn / 3600)} sa ${Math.floor((sn % 3600) / 60)} dk` : `${Math.floor(sn / 60)} dk`);
const eylemAdi: Record<string, string> = { restart: 'Yeniden başlat', stop: 'Durdur', start: 'Başlat' };

/** Sistem › Sağlık — sunucu, meds-pg, vektörleme servisleri, SSE, bellek, son hatalar ve servis denetimi. */
export default function Saglik({ git }: SayfaProps) {
  const s = useAdminSorgu<any>('/api/admin/sistem/saglik', { aralikMs: 15000 });
  const sv = useAdminSorgu<{ machine: string; helperOnline: boolean; statusAt: string; services: Servis[] }>('/api/admin/servis/list', { aralikMs: 30000 });
  const [log, setLog] = useState<{ id: string; metin: string } | null>(null);
  const v = s.veri;
  const ton = (ok: boolean): Ton => (ok ? 'iyi' : 'kotu');
  const eylem = async (x: Servis, a: string) => {
    if (!(await onayIste({ baslik: `${x.label}: ${eylemAdi[a] || a}?`, aciklama: x.note || (a === 'stop' ? 'Servis durur; ona bağlı özellikler çalışmaz.' : undefined), tehlikeli: a !== 'start', onayMetni: eylemAdi[a] || a }))) return;
    try { const r = await adminIstek<any>('/api/admin/servis/action', { yontem: 'POST', govde: { service: x.id, action: a } }); bildir(r.message || 'Tamam.', 'iyi'); setTimeout(() => void sv.yenile(), 1500); }
    catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
  };
  const logAc = async (x: Servis) => {
    try { const r = await adminIstek<any>('/api/admin/servis/logs', { sorgu: { service: x.id, lines: 200 } }); setLog({ id: x.label, metin: r.lines || '(boş)' }); }
    catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
  };
  return (
    <>
      <SayfaBasligi baslik="Sağlık" aciklama={v ? `${v.sunucu.ana} · Node ${v.sunucu.node} · 15 sn'de bir tazelenir` : 'Sunucu ve servis durumu'}
        eylemler={<button type="button" className="m16-btn" onClick={() => { void s.yenile(); void sv.yenile(); }}>Yenile</button>} />
      {s.hata && <Hata hata={s.hata} yenile={s.yenile} />}
      {!v && !s.hata && <Yukleniyor satir={3} />}
      {v && (
        <IstatistikIzgara>
          <IstatistikKart etiket="meds-pg" deger={v.pg.cevrimici ? `${v.pg.ms} ms` : 'Çevrimdışı'} ton={ton(v.pg.cevrimici)} alt={v.pg.cevrimici ? `${v.pg.boyutMb} MB · ${v.pg.baglanti} bağlantı (${v.pg.etkin} etkin)` : v.pg.hata} />
          <IstatistikKart etiket="Vektörleme bge-m3" deger={v.embed.bge.ok ? `${v.embed.bge.ms} ms` : 'Yanıt yok'} ton={ton(v.embed.bge.ok)} alt={v.embed.bge.hata || `HTTP ${v.embed.bge.durum}`} />
          <IstatistikKart etiket="Vektörleme e5-small" deger={v.embed.e5.ok ? `${v.embed.e5.ms} ms` : 'Yanıt yok'} ton={v.embed.e5.ok ? 'iyi' : 'uyari'} alt={v.embed.e5.hata || `HTTP ${v.embed.e5.durum}`} />
          <IstatistikKart etiket="SSE bağlantısı" deger={v.sseIstemci} alt="açık canlı akış" />
          <IstatistikKart etiket="Node yığını" deger={`${v.bellek.yiginMb} MB`} alt={`RSS ${v.bellek.rssMb} MB · sistem boş ${Math.round(v.bellek.sistemBosMb / 1024 * 10) / 10} / ${Math.round(v.bellek.sistemToplamMb / 1024)} GB`} ton={v.bellek.sistemBosMb < 800 ? 'uyari' : 'notr'} />
          <IstatistikKart etiket="Yük (1/5/15 dk)" deger={v.yuk.join(' · ')} alt={`${v.cekirdek} çekirdek`} ton={v.yuk[0] > v.cekirdek ? 'uyari' : 'notr'} />
          <IstatistikKart etiket="Çalışma süresi" deger={sure(v.sunucu.calismaSn)} alt={`pid ${v.sunucu.pid}`} />
          <IstatistikKart etiket="İstemci hatası (24 sa)" deger={v.istemci.son24s} ton={v.istemci.son24s ? 'uyari' : 'iyi'} onClick={() => git('sistem/hata')} alt={v.istemci.son ? `${zamanMetni(v.istemci.son.at)}: ${String(v.istemci.son.mesaj).slice(0, 60)}` : 'kayıt yok'} />
        </IstatistikIzgara>
      )}
      <div className="m16-ts-izgara">
        <section className="m16-kart">
          <h2>Son sunucu hatası (5xx)</h2>
          {v?.sonSunucuHatasi ? (
            <p><Rozet ton="kotu">{v.sonSunucuHatasi.durum}</Rozet> <code>{v.sonSunucuHatasi.yontem} {v.sonSunucuHatasi.uc}</code> · {zamanMetni(v.sonSunucuHatasi.at)}
              {v.sonSunucuHatasi.hata && <><br /><small>{v.sonSunucuHatasi.hata}</small></>}<br />
              <a href="#" onClick={(e) => { e.preventDefault(); git('sistem/denetim?s.durum=hata'); }}>Tüm hatalı işlemler</a></p>
          ) : <p className="m16-ts-not">Denetim kaydında 5xx yok.</p>}
        </section>
        {log && (
          <section className="m16-kart">
            <h2>{log.id} günlüğü <button type="button" className="m16-btn hayalet" onClick={() => setLog(null)}>Kapat</button></h2>
            <pre className="m16-ts-log">{log.metin}</pre>
          </section>
        )}
      </div>
      <section className="m16-kart" style={{ marginTop: 12 }}>
        <h2>Servisler {sv.veri && <small>({sv.veri.machine === 'oracle' ? `Oracle · yardımcı ${sv.veri.helperOnline ? 'çevrimiçi' : 'çevrimdışı'}` : 'bu cihaz'})</small>}</h2>
        {sv.hata ? <Hata hata={sv.hata} yenile={sv.yenile} /> : !sv.veri ? <Yukleniyor satir={4} /> : (
          <ul className="m16-liste">
            {sv.veri.services.map((x) => (
              <li key={x.id}>
                <Rozet ton={x.active === 'active' ? 'iyi' : x.active === 'failed' ? 'kotu' : 'notr'}>{x.active}</Rozet>
                <span className="m16-kisalt" title={x.id}>{x.label}</span>
                <span className="m16-ts-eylem">
                  <button type="button" className="m16-btn hayalet" onClick={() => logAc(x)}>Günlük</button>
                  {x.actions.map((a) => <button key={a} type="button" className="m16-btn hayalet" onClick={() => eylem(x, a)}>{eylemAdi[a] || a}</button>)}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </>
  );
}
