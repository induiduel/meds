import React, { useState } from 'react';
import { BookOpen, Check, GraduationCap, ChevronDown, FileText, History, HelpCircle, RotateCcw, Sparkles, Star } from 'lucide-react';
import { kucuk } from '../spotsShared';
import { TUR_AD, TUR_IPUCU, bantOf, dersAdi, type Cikmis, type Ders, type Madde, type Soru } from './onemVeri';

/**
 * Önem listesi madde kartı. Anatomi: puan rozeti · etiketler · tek cümle bilgi (+ alt maddeler) · öğrendim düğmesi;
 * altta sekme çipleri (Açıklama · PDF s.N · Örnek soru · Çıkmış n). Çipe dokununca ayrıntı o sekmede açılır,
 * aynı çipe yeniden dokununca kapanır. Bilgi metnine dokunmak da ayrıntıyı açar/kapatır (metin seçimi bozulmaz).
 * Tekrar modunda kalın terimler gizlenir; her biri dokununca açılır.
 */

export type Sekme = 'aciklama' | 'alinti' | 'soru' | 'cikmis';

/** Aranan sözcükleri <mark> ile işaretler (Türkçe büyük/küçük harf duyarsız; tr küçültme uzunluğu korur). */
const isaretle = (s: string, terimler: string[]): React.ReactNode => {
  if (!terimler.length || !s) return s;
  const k = kucuk(s);
  if (k.length !== s.length) return s;
  const araliklar: [number, number][] = [];
  for (const t of terimler) {
    let i = k.indexOf(t);
    while (i >= 0 && t) { araliklar.push([i, i + t.length]); i = k.indexOf(t, i + t.length); }
  }
  if (!araliklar.length) return s;
  araliklar.sort((a, b) => a[0] - b[0]);
  const birlesik: [number, number][] = [];
  for (const a of araliklar) {
    const son = birlesik[birlesik.length - 1];
    if (son && a[0] <= son[1]) son[1] = Math.max(son[1], a[1]); else birlesik.push([...a]);
  }
  const out: React.ReactNode[] = []; let p = 0;
  birlesik.forEach(([a, b], i) => {
    if (a > p) out.push(s.slice(p, a));
    out.push(<mark key={i} className="on-mark">{s.slice(a, b)}</mark>);
    p = b;
  });
  if (p < s.length) out.push(s.slice(p));
  return out;
};

const Gizli: React.FC<{ metin: string }> = ({ metin }) => {
  const [acik, setAcik] = useState(false);
  if (acik) return <strong className="on-acilan">{metin}</strong>;
  return (
    <button type="button" className="on-gizli" onClick={(e) => { e.stopPropagation(); setAcik(true); }} aria-label="Gizli terimi göster">
      <span aria-hidden>{metin}</span>
    </button>
  );
};

/** **kalın** → <strong>; tekrar modunda kalın = gizli terim; arama terimleri işaretlenir */
export const Metin: React.FC<{ metin: string; gizle?: boolean; terimler?: string[] }> = ({ metin, gizle, terimler = [] }) => (
  <>
    {String(metin || '').split(/(\*\*[^*]+\*\*)/g).map((p, i) => {
      if (p.length > 4 && p.startsWith('**') && p.endsWith('**')) {
        const ic = p.slice(2, -2);
        return gizle ? <Gizli key={i} metin={ic} /> : <strong key={i}>{isaretle(ic, terimler)}</strong>;
      }
      return <React.Fragment key={i}>{isaretle(p, terimler)}</React.Fragment>;
    })}
  </>
);

/** detay: "- **Başlık:** metin" satırları → madde listesi; diğer satırlar paragraf */
const Detay: React.FC<{ metin: string; terimler: string[] }> = ({ metin, terimler }) => {
  const satirlar = metin.split('\n').map((s) => s.trim()).filter(Boolean);
  const out: React.ReactNode[] = []; let liste: string[] = [];
  const bosalt = () => { if (liste.length) { out.push(<ul key={out.length}>{liste.map((x, i) => <li key={i}><Metin metin={x} terimler={terimler} /></li>)}</ul>); liste = []; } };
  for (const s of satirlar) {
    if (/^[-•]\s+/.test(s)) liste.push(s.replace(/^[-•]\s+/, ''));
    else { bosalt(); out.push(<p key={out.length}><Metin metin={s} terimler={terimler} /></p>); }
  }
  bosalt();
  return <div className="on-detay">{out}</div>;
};

/** Şıkka dokunarak çözülen soru: doğru yeşil, yanlış seçim kırmızı, açıklama altta; "Yeniden çöz" sıfırlar. */
export const SoruKart: React.FC<{ s: Soru | Cikmis; baslik: string; ust?: string }> = ({ s, baslik, ust }) => {
  const [secim, setSecim] = useState<string | null>(null);
  const cozuldu = secim !== null;
  const dogru = secim === s.dogru;
  return (
    <div className={`on-soru${cozuldu ? (dogru ? ' is-dogru' : ' is-yanlis') : ''}`}>
      <div className="on-soru-h"><span>{baslik}</span>{ust && <em>{ust}</em>}</div>
      <p className="on-soru-k">{s.kok}</p>
      <div className="on-soru-s" role="group" aria-label="Şıklar">
        {Object.entries(s.secenekler).map(([k, v]) => {
          const durum = !cozuldu ? '' : k === s.dogru ? ' is-dogru' : k === secim ? ' is-yanlis' : ' is-sonuk';
          return (
            <button key={k} type="button" className={`on-sik${durum}`} disabled={cozuldu} onClick={() => setSecim(k)} aria-label={`${k} şıkkı: ${v}`}>
              <b>{k}</b><span>{v}</span>
              {cozuldu && k === s.dogru && <Check className="on-sik-i" aria-hidden />}
            </button>
          );
        })}
      </div>
      {cozuldu ? (
        <div className="on-soru-c" aria-live="polite">
          <p><b>{dogru ? 'Doğru.' : `Yanlış — doğru cevap ${s.dogru}.`}</b>{'aciklama' in s && s.aciklama ? <> {s.aciklama}</> : null}</p>
          <button type="button" className="on-link" onClick={() => setSecim(null)}><RotateCcw aria-hidden />Yeniden çöz</button>
        </div>
      ) : (
        <p className="on-soru-ipucu">Bir şıkka dokun</p>
      )}
    </div>
  );
};

export interface MaddeProps {
  m: Madde; d: Ders;
  /** çok dersli görünümde ders adı etiketi */
  gosterDers: boolean;
  acik: boolean; sekme: Sekme;
  onAc: (id: string, sekme: Sekme | null) => void;
  ogrenildi: boolean; onOgren: (id: string, v: boolean) => void;
  gizle: boolean; terimler: string[];
  odak: boolean;
  /** ders adına dokununca o derse git */
  onDers?: (kod: string, id: string) => void;
}

const ZORLUK_AD = { kolay: 'Kolay', orta: 'Orta', zor: 'Zor' } as const;

export const OnemMadde: React.FC<MaddeProps> = React.memo(({ m, d, gosterDers, acik, sekme, onAc, ogrenildi, onOgren, gizle, terimler, odak, onDers }) => {
  const aday = (d.sinavAdaylari || []).find((a) => a.id === m.id);
  const enOlasi = !!aday && aday.sira <= (d.soruSayisi || 1);
  const cs = (m.cikmis || []).map((id) => [id, d.cikmis?.[id]] as const).filter((x): x is readonly [string, Cikmis] => !!x[1]);
  const sayfalar = [...new Set(m.alinti.map((a) => a.sayfa))].sort((a, b) => a - b);
  const ornekSay = (m.ornek_soru ? 1 : 0) + (m.ornek26?.length || 0);
  const sekmeler: { k: Sekme; ad: string; ikon: React.ReactNode; var: boolean }[] = [
    { k: 'aciklama', ad: 'Açıklama', ikon: <BookOpen aria-hidden />, var: true },
    { k: 'alinti', ad: sayfalar.length ? `PDF s. ${sayfalar.join(', ')}` : 'PDF alıntısı', ikon: <FileText aria-hidden />, var: m.alinti.length > 0 },
    { k: 'soru', ad: ornekSay > 1 ? `Örnek soru ${ornekSay}` : 'Örnek soru', ikon: <HelpCircle aria-hidden />, var: ornekSay > 0 },
    { k: 'cikmis', ad: `Çıkmış ${cs.length}`, ikon: <History aria-hidden />, var: cs.length > 0 },
  ];
  const tikla = (k: Sekme) => onAc(m.id, acik && sekme === k ? null : k);
  const govdeTikla = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest('button,a')) return;
    if (window.getSelection?.()?.toString()) return; // metin seçiliyorsa açma/kapatma yok
    onAc(m.id, acik ? null : sekme);
  };
  const panelId = `on-p-${m.id}`;
  const dis = m.sinavUygun === false;
  return (
    <li id={`on-m-${m.id}`} data-mid={m.id}
      className={`on-m b${bantOf(m.puan)}${acik ? ' is-open' : ''}${ogrenildi ? ' is-ogr' : ''}${dis ? ' is-dis' : ''}${aday ? ' is-aday' : ''}${odak ? ' is-odak' : ''}`}>
      <div className="on-m-ana">
        <span className="on-puan" aria-label={`${m.puan} puan`} title={`${m.puan} / 100`}>{m.puan}</span>
        <div className="on-m-govde" onClick={govdeTikla}>
          <div className="on-m-meta">
            <span className={`on-tur t-${m.tur}`} title={TUR_IPUCU[m.tur]}>{TUR_AD[m.tur] || m.tur}</span>
            {aday && <span className={`on-aday${enOlasi ? ' is-en' : ''}`}><Star aria-hidden />{enOlasi ? 'En olası soru' : `Sınav adayı ${aday.sira}`}</span>}
            {m.ogrenci && <span className={`on-ogrn is-${m.ogrenci.oncelik}`} title="Geçen yılın öğrenci notunda en önemli yerler arasında">
              <GraduationCap aria-hidden />{m.ogrenci.oncelik === 'A' ? 'Öğrenciler buraya çalıştı' : 'Öğrenci notunda'}</span>}
            {m.kaynak === 'tablo' && <span className="on-dis">Tablo · sorulmaz</span>}
            {m.kaynak === 'sekil' && <span className="on-dis">Şekil · sorulmaz</span>}
            {m.klinik && <span className="on-dis">Klinik bulgu · sorulmaz</span>}
            {m.kategori === 'prognoz' && <span className="on-kat k-prognoz">Prognoz · sorulabilir</span>}
            {m.kategori === 'tedavi' && <span className="on-kat k-tedavi">Tedavi · sorulabilir</span>}
            {gosterDers && (onDers
              ? <button type="button" className="on-dersad" onClick={() => onDers(d.kod, m.id)} title="Bu derse git">{dersAdi(d)}</button>
              : <span className="on-dersad">{dersAdi(d)}</span>)}
          </div>
          <p className="on-bilgi"><Metin key={gizle ? 'g' : 'a'} metin={m.bilgi} gizle={gizle} terimler={terimler} /></p>
          {m.alt && m.alt.length > 0 && (
            <ul className="on-alt">{m.alt.map((x, i) => <li key={i}><Metin key={gizle ? 'g' : 'a'} metin={x} gizle={gizle} terimler={terimler} /></li>)}</ul>
          )}
        </div>
        <button type="button" className={`on-ogr${ogrenildi ? ' is-on' : ''}`} aria-pressed={ogrenildi}
          onClick={() => onOgren(m.id, !ogrenildi)} title={ogrenildi ? 'Öğrendim işaretini kaldır (x)' : 'Öğrendim olarak işaretle (x)'}
          aria-label={ogrenildi ? 'Öğrendim işaretini kaldır' : 'Öğrendim olarak işaretle'}>
          <Check aria-hidden />
        </button>
      </div>
      <div className="on-m-sekmeler">
        <div className="on-m-tablist" role="tablist" aria-label="Ayrıntı">
        {sekmeler.filter((s) => s.var).map((s) => (
          <button key={s.k} type="button" role="tab" aria-selected={acik && sekme === s.k} aria-controls={panelId}
            className={`on-sekme${acik && sekme === s.k ? ' is-on' : ''}${s.k === 'cikmis' ? ' is-cik' : ''}`} onClick={() => tikla(s.k)}>
            {s.ikon}<span>{s.ad}</span>
          </button>
        ))}
        </div>
        <button type="button" className="on-ac" onClick={() => onAc(m.id, acik ? null : sekme)} aria-expanded={acik} aria-controls={panelId}
          aria-label={acik ? 'Ayrıntıyı kapat' : 'Ayrıntıyı aç'}>
          <ChevronDown aria-hidden />
        </button>
      </div>
      {acik && (
        <div className="on-m-detay" id={panelId} role="tabpanel">
          {m.neden && (
            <p className="on-neden"><Sparkles aria-hidden /><span><b>Neden önemli:</b> {m.neden}</span></p>
          )}
          {m.ogrenci?.not && <p className="on-ogrn-g"><GraduationCap aria-hidden /><span><b>Geçen yılın öğrenci notu:</b> {m.ogrenci.not}</span></p>}
          {aday && <p className="on-aday-g"><Star aria-hidden /><span><b>{enOlasi ? 'En olası soru' : `Sınav adayı ${aday.sira}`}:</b> {aday.gerekce}</span></p>}
          {dis && <p className="on-dis-g">Hocanın açıklamasına göre {m.kaynak === 'tablo' ? 'tablolardan' : m.kaynak === 'sekil' ? 'resim/şekillerden' : 'klinik bulgulardan'} soru sorulmayacak; bilgi olarak bilinmesi yeterli.</p>}
          {sekme === 'aciklama' && <Detay metin={m.detay} terimler={terimler} />}
          {sekme === 'alinti' && m.alinti.map((a, i) => (
            <blockquote key={i} className="on-alinti">“{a.metin}”<cite>{d.pdf} · sayfa {a.sayfa}</cite></blockquote>
          ))}
          {sekme === 'soru' && (m.ornek26 || []).map((q, i) => <SoruKart key={`y${i}`} s={q} baslik={q.zorluk ? `Örnek soru · ${ZORLUK_AD[q.zorluk]}` : 'Örnek soru · 2026-27'} />)}
          {sekme === 'soru' && m.ornek_soru && <SoruKart s={m.ornek_soru} baslik="Örnek soru" />}
          {sekme === 'cikmis' && cs.map(([id, c]) => <SoruKart key={id} s={c} baslik="Çıkmış soru" ust={c.tekrar?.length ? `${c.sinav} · ayrıca ${c.tekrar.join(', ')}` : c.sinav} />)}
        </div>
      )}
    </li>
  );
});
OnemMadde.displayName = 'OnemMadde';
