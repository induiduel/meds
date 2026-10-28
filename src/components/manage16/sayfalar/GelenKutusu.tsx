import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, IstatistikIzgara, IstatistikKart, AyrintiCekmecesi, useAdminSorgu, adminIstek, bildir, onayIste, gerekceIste, yazimHedefi, zamanMetni, type Ton } from '../kit';
import { manageAdres, type SayfaProps } from '../menu';

/**
 * Genel › Gelen — bekleyen her şey tek listede (GET /api/admin/gelen): soru şikâyetleri, topluluk mesaj şikâyetleri, Öğren geri
 * bildirimleri, son 24 saatin istemci hataları (gruplu), gizlilik talepleri, Faz 14 bekleyenleri, kamp tüyo önerileri.
 * H290: işlem satırda / çekmecede yapılır (soru: Çözüldü·Yok say, topluluk: Yok say·Mesajı gizle, geri bildirim: Kapat + iç not,
 * hata: Görüldü). Gizlilik, Faz 14, tüyo ilgili sayfaya gider. Aynı türden satırlar toplu işlenir; işlenen satır listeden düşer.
 */
type Satir = { id: string; tur: string; at: string; baslik: string; ayrinti: string; kim: string; ek: string; hedef: string };
const TUR: Record<string, { ad: string; ton: Ton }> = {
  soru: { ad: 'Soru şikâyeti', ton: 'kotu' }, topluluk: { ad: 'Topluluk şikâyeti', ton: 'uyari' }, 'geri-bildirim': { ad: 'Geri bildirim', ton: 'bilgi' },
  hata: { ad: 'İstemci hatası', ton: 'kotu' }, gizlilik: { ad: 'Gizlilik', ton: 'vurgu' }, faz14: { ad: 'Faz 14', ton: 'notr' }, tuyo: { ad: 'Tüyo önerisi', ton: 'iyi' },
};
const KAYNAK_TUR: Record<string, string> = { soru: 'soru', topluluk: 'topluluk', geriBildirim: 'geri-bildirim', hata: 'hata', gizlilik: 'gizlilik', faz14: 'faz14', tuyo: 'tuyo' };
const SORU_SAYFA: Record<string, string> = { cikmis: 'sorular/cikmis', havuz: 'sorular/havuz', ornek: 'sorular/ornek' };

// H290: satır kimliği "<tür>:<kimlik>"; soru şikâyetinde kimlik "<kaynak>:<soruId>:<raporId>" (sorular.ts tumSikayetler)
const turu = (id: string) => (id.startsWith('geri-bildirim:') ? 'geri-bildirim' : id.slice(0, id.indexOf(':')));
const kimligi = (id: string) => id.slice(turu(id).length + 1);
const soruParca = (id: string) => {
  const p = kimligi(id).split(':');
  return { kaynak: p[0], soruId: p.slice(1, -1).join(':'), raporId: p[p.length - 1] };
};

type Eylem = 'coz' | 'yoksay' | 'gizle' | 'kapat' | 'goruldu';
const EYLEM_AD: Record<Eylem, string> = { coz: 'Çözüldü', yoksay: 'Yok say', gizle: 'Mesajı gizle', kapat: 'Kapat', goruldu: 'Görüldü' };
const TUR_EYLEM: Record<string, Eylem[]> = { soru: ['coz', 'yoksay'], topluluk: ['yoksay', 'gizle'], 'geri-bildirim': ['kapat'], hata: ['goruldu'] };

/** H290: tek satır işlemi; var olan uçlar (yoksay şikâyet için de "resolved" yazar: soru bildiriminde ayrı "reddedildi" durumu yok) */
async function tekIslem(id: string, e: Eylem, not?: string) {
  const tur = turu(id);
  if (tur === 'soru') {
    const s = soruParca(id);
    await adminIstek('/api/admin/sorular/sikayet/coz', { yontem: 'POST', govde: { ...s, durum: 'resolved' } });
  } else if (tur === 'topluluk') {
    const m = encodeURIComponent(kimligi(id));
    if (e === 'gizle') await adminIstek(`/api/admin/topluluk/mesajlar/${m}/gizle`, { yontem: 'POST', govde: { gizli: true } });
    else await adminIstek(`/api/admin/topluluk/sikayetler/${m}/yoksay`, { yontem: 'POST' });
  } else if (tur === 'geri-bildirim') {
    await adminIstek(`/api/admin/topluluk/geri-bildirim/${encodeURIComponent(kimligi(id))}`, { yontem: 'PUT', govde: { durum: 'cozuldu', ...(not ? { yanit: not } : {}) } });
  } else if (tur === 'hata') {
    await adminIstek('/api/admin/gelen/hata/goruldu', { yontem: 'POST', govde: { kimlikler: [kimligi(id)] } });
  } else throw new Error('Bu tür burada işlenmez.');
}

export default function GelenKutusu({ id, git }: SayfaProps) {
  const ozet = useAdminSorgu<{ kaynaklar: Record<string, { toplam: number; hata?: boolean }> }>('/api/admin/gelen', { sorgu: { boyut: 1 } });
  const k = ozet.veri?.kaynaklar || {};
  const suz = (tur: string) => { const u = new URL(window.location.href); u.searchParams.set('s.tur', tur); u.searchParams.delete('sayfa'); git(`gelen${u.search}`, { degistir: true }); };
  // H290: işlenen satırlar istemcide hemen düşer (sunucu önbelleği de silinir; SSE yenilemesi gelince zaten yoktur)
  const [islenen, setIslenen] = React.useState<Set<string>>(() => new Set());
  const [acik, setAcik] = React.useState<Satir | null>(null);
  const [mesgul, setMesgul] = React.useState(false);
  const dusur = (ids: string[]) => setIslenen((s) => { const n = new Set(s); ids.forEach((x) => n.add(x)); return n; });

  const isle = async (ids: string[], e: Eylem, not?: string) => {
    if (!ids.length) return;
    if (ids.length > 1 && !(await onayIste({ baslik: `${ids.length} satır için "${EYLEM_AD[e]}" uygulansın mı?`, aciklama: `Hedef: ${yazimHedefi()}.`, onayMetni: EYLEM_AD[e] }))) return;
    setMesgul(true);
    let tamam: string[] = [];
    let hata = 0; let sonHata = '';
    if (e === 'goruldu') {
      // H292: hata grupları tek istekte
      try { await adminIstek('/api/admin/gelen/hata/goruldu', { yontem: 'POST', govde: { kimlikler: ids.map(kimligi) } }); tamam = ids; }
      catch (x: any) { hata = ids.length; sonHata = x.message; }
    } else {
      for (const x of ids) {
        try { await tekIslem(x, e, not); tamam.push(x); } catch (y: any) { hata++; sonHata = y.message; }
      }
    }
    setMesgul(false);
    dusur(tamam);
    if (acik && tamam.includes(acik.id)) setAcik(null);
    if (hata) bildir(`${tamam.length} işlendi, ${hata} başarısız: ${sonHata}`, 'kotu');
    else bildir(ids.length > 1 ? `${tamam.length} satır: ${EYLEM_AD[e]}` : EYLEM_AD[e], 'iyi');
    void ozet.yenile();
  };
  const notluKapat = async (s: Satir) => {
    const not = await gerekceIste({ baslik: 'Geri bildirim kapatılsın mı?', aciklama: 'İç not öğrenciye gönderilmez.', onayMetni: 'Kapat', gerekce: { etiket: 'İç not', enAz: 0, yerTutucu: 'İsteğe bağlı' } });
    if (not === null) return;
    await isle([s.id], 'kapat', not || undefined);
  };
  const soruAc = (s: Satir) => { const p = soruParca(s.id); git(`${SORU_SAYFA[p.kaynak] || 'sorular/sikayet'}/${encodeURIComponent(p.soruId)}`); };

  const eylemDugmeleri = (s: Satir, kucuk = false) => {
    const cls = kucuk ? 'm16-btn hayalet' : 'm16-btn';
    const dur = (f: () => void) => (ev: React.MouseEvent) => { ev.stopPropagation(); f(); };
    const ev = TUR_EYLEM[s.tur];
    if (!ev) return <button type="button" className={cls} onClick={dur(() => git(s.hedef))}>Sayfaya git</button>;
    return (
      <>
        {ev.map((e) => (
          <button key={e} type="button" disabled={mesgul} className={e === 'gizle' ? `${cls} tehlike` : e === ev[0] && !kucuk ? 'm16-btn birincil' : cls}
            onClick={dur(() => void (e === 'kapat' && !kucuk ? notluKapat(s) : isle([s.id], e)))}>{EYLEM_AD[e]}</button>
        ))}
        {s.tur === 'soru' && <button type="button" className={cls} onClick={dur(() => soruAc(s))}>Soruyu aç</button>}
      </>
    );
  };

  return (
    <>
      <SayfaBasligi baslik="Gelen" aciklama="Bekleyen her şey tek listede. Şikâyet, geri bildirim ve hatalar burada işlenir; gizlilik, Faz 14 ve tüyo kendi sayfasına gider." />
      {/* H175: sıfır kartlar gizlenir (okunamayan kaynak görünür kalır); hepsi sıfırsa tek satır bilgi */}
      {ozet.veri && !Object.keys(KAYNAK_TUR).some((a) => k[a]?.hata || (k[a]?.toplam || 0) > 0) ? (
        <p className="m16-istat-alt">Bekleyen iş yok.</p>
      ) : (
      <IstatistikIzgara sik>
        {Object.entries(KAYNAK_TUR).filter(([anahtar]) => !ozet.veri || k[anahtar]?.hata || (k[anahtar]?.toplam || 0) > 0).map(([anahtar, tur]) => (
          <IstatistikKart key={anahtar} etiket={TUR[tur].ad} yukleniyor={!ozet.veri && ozet.yukleniyor}
            deger={k[anahtar]?.hata ? '—' : (k[anahtar]?.toplam ?? 0)} alt={k[anahtar]?.hata ? 'okunamadı' : undefined}
            ton={(k[anahtar]?.toplam || 0) > 0 ? TUR[tur].ton : 'notr'} onClick={() => suz(tur)} />
        ))}
      </IstatistikIzgara>
      )}
      <VeriTablosu<Satir>
        kimlik="genel-gelen" kaynak="/api/admin/gelen" aramaYeri="Başlık, ayrıntı ya da kişi ara…" satirKimligi={(s) => s.id}
        satirTikla={(s) => (TUR_EYLEM[s.tur] ? setAcik(s) : git(s.hedef))} etkin={acik?.id || id || null}
        dusur={(s) => islenen.has(s.id)}
        secim
        topluEylemler={(secili, temizle) => {
          // H290: toplu işlem yalnız aynı türden satırlarda (eylemler türe özgü)
          const turler = [...new Set(secili.map(turu))];
          if (turler.length !== 1) return <span className="m16-istat-alt">Toplu işlem için aynı türden satırlar seçin.</span>;
          const ev = TUR_EYLEM[turler[0]];
          if (!ev) return <span className="m16-istat-alt">Bu tür kendi sayfasında işlenir.</span>;
          return ev.map((e) => <button key={e} type="button" disabled={mesgul} className={e === 'gizle' ? 'm16-btn tehlike' : 'm16-btn'} onClick={() => void isle(secili, e).then(temizle)}>{EYLEM_AD[e]}</button>);
        }}
        canliOlay={['reports_changed', 'learn_feedback_changed', 'gizlilik_changed', 'topluluk_changed']}
        suzgecler={[{ anahtar: 'tur', etiket: 'Tür', secenekler: Object.entries(TUR).map(([d, v]) => ({ deger: d, etiket: v.ad })) }]}
        sutunlar={[
          { anahtar: 'at', baslik: 'Zaman', sirala: true, genislik: '110px', hucre: (s) => s.at ? <time title={s.at}>{zamanMetni(s.at)}</time> : '—' },
          { anahtar: 'tur', baslik: 'Tür', sirala: true, genislik: '140px', hucre: (s) => <Rozet ton={TUR[s.tur]?.ton || 'notr'}>{TUR[s.tur]?.ad || s.tur}</Rozet> },
          { anahtar: 'baslik', baslik: 'Konu', genislik: 'minmax(180px,2fr)', hucre: (s) => <a href={manageAdres(s.hedef)} onClick={(e) => { e.preventDefault(); e.stopPropagation(); git(s.hedef); }}>{s.baslik || '—'}</a> },
          { anahtar: 'ayrinti', baslik: 'Ayrıntı', genislik: 'minmax(200px,3fr)' },
          { anahtar: 'kim', baslik: 'Kim', genislik: '140px', gizli: true },
          { anahtar: 'ek', baslik: 'Ek', genislik: '160px' },
          { anahtar: 'islem', baslik: 'İşlem', genislik: 'minmax(200px,1.4fr)', hucre: (s) => <span style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>{eylemDugmeleri(s, true)}</span> },
        ]}
      />
      {acik && (
        <AyrintiCekmecesi acik kapat={() => setAcik(null)} baslik={acik.baslik || TUR[acik.tur]?.ad} altBaslik={`${TUR[acik.tur]?.ad || acik.tur} · ${acik.at ? zamanMetni(acik.at) : ''}`}
          kayit={acik} eylemler={<>{eylemDugmeleri(acik)}<button type="button" className="m16-btn hayalet" onClick={() => git(acik.hedef)}>Sayfada aç</button></>}>
          <dl className="m16-satirlar">
            <dt>Ayrıntı</dt><dd style={{ whiteSpace: 'pre-wrap' }}>{acik.ayrinti || '—'}</dd>
            <dt>Kim</dt><dd>{acik.kim || '—'}</dd>
            <dt>Ek</dt><dd>{acik.ek || '—'}</dd>
          </dl>
        </AyrintiCekmecesi>
      )}
    </>
  );
}

