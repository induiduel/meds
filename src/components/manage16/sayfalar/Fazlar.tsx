import React, { useState } from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, JsonGoruntuleyici, Hata, Yukleniyor, useAdminSorgu, type Sutun } from '../kit';
import type { SayfaProps } from '../menu';

/**
 * Sistem › Fazlar — eski faz çıktıları (Faz 5–14: kazanım, slayt, Öğren bağı, terim, varlık…), SALT OKUNUR.
 * Liste: GET /api/admin/sistem/fazlar/:kategori; ayrıntı: GET /api/admin/phases/question/:id. Elle düzeltme ve yeniden inceleme
 * eski konsolda (?kabuk=v14 › Fazlar) kaldı.
 */
type Kat = { id: string; label: string; desc: string; satir: number; soru: number; alanlar: string[] };

function Ayrinti({ id, kapat }: { id: string; kapat: () => void }) {
  const s = useAdminSorgu<any>(`/api/admin/phases/question/${encodeURIComponent(id)}`);
  return (
    <AyrintiCekmecesi acik genis kapat={kapat} baslik={id} altBaslik="Faz kayıtları (salt okunur)" kayit={s.veri}>
      {s.hata && <Hata hata={s.hata} yenile={s.yenile} />}
      {!s.veri && !s.hata && <Yukleniyor satir={4} />}
      {s.veri && <>
        <div className="m16-kart"><h2>Sitede görünen</h2><JsonGoruntuleyici veri={s.veri.gorunen} enYuksek={320} /></div>
        {s.veri.duzeltme && <div className="m16-kart"><h2>Elle düzeltme</h2><JsonGoruntuleyici veri={s.veri.duzeltme} enYuksek={240} /></div>}
        <div className="m16-kart"><h2>Türetilmiş kayıtlar</h2><JsonGoruntuleyici veri={s.veri.kayitlar} enYuksek={400} /></div>
      </>}
    </AyrintiCekmecesi>
  );
}

export default function Fazlar({ id, altYol, git }: SayfaProps) {
  const kats = useAdminSorgu<{ kategoriler: Kat[] }>('/api/admin/phases/categories');
  const liste = kats.veri?.kategoriler || [];
  const kat = liste.find((k) => k.id === id) || liste[0];
  const [soru, setSoru] = useState<string | null>(null);
  const sutunlar: Sutun<any>[] = (kat?.alanlar || []).map((a) => ({
    anahtar: a, baslik: a, sirala: true, genislik: a === 'soru_id' ? 'minmax(160px,1fr)' : a.length > 6 || /gerekce|metin|kazanim|slayt/.test(a) ? 'minmax(140px,2fr)' : '110px',
    hucre: (t: any) => { const v = t[a]; return v == null || v === '' ? '—' : typeof v === 'object' ? JSON.stringify(v) : String(v); },
  }));
  if (kat) sutunlar.push(
    { anahtar: '_kok', baslik: 'Soru kökü', genislik: 'minmax(180px,2fr)', gizli: true },
    { anahtar: '_durum', baslik: 'Elle', genislik: '90px', hucre: (t: any) => (t._durum ? <Rozet ton="uyari">{t._durum}</Rozet> : t._elle ? <Rozet ton="bilgi">düzeltildi</Rozet> : '') },
  );
  void altYol;
  return (
    <>
      <SayfaBasligi baslik="Fazlar" aciklama="Eski faz çıktıları, salt okunur. Arama tüm alanlarda geçer; '=değer' tam eşleşme, 'bos'/'dolu' boşluk süzgecidir.">
        <div className="m16-sekmeler" role="tablist">
          {liste.map((k) => <button key={k.id} type="button" role="tab" aria-selected={k.id === kat?.id} className={k.id === kat?.id ? 'on' : ''} title={k.desc}
            onClick={() => git(`sistem/fazlar/${k.id}`, { degistir: true })}>{k.label} <small>{k.satir}</small></button>)}
        </div>
      </SayfaBasligi>
      {kats.hata && <Hata hata={kats.hata} yenile={kats.yenile} />}
      {!kat && !kats.hata && <Yukleniyor satir={4} />}
      {kat && <>
        <p className="m16-ts-not" style={{ margin: '0 0 8px' }}>{kat.desc} · {kat.soru} soru</p>
        <VeriTablosu<any> key={kat.id} kimlik={`sistem-fazlar-${kat.id}`} kaynak={`/api/admin/sistem/fazlar/${kat.id}`} aramaYeri="Değer ara (ör. =yuksek, bos)…"
          satirKimligi={(t) => t._id} satirTikla={(t) => setSoru(String(t.soru_id))} sutunlar={sutunlar} />
      </>}
      {soru && <Ayrinti id={soru} kapat={() => setSoru(null)} />}
    </>
  );
}
