/** Topluluk sayfalarının ortak mesaj tablosu (Şikâyetler, Mesajlar, Oda ayrıntısı). Sayfa değil, yardımcı modül. */
import React, { useState } from 'react';
import { VeriTablosu, AyrintiCekmecesi, Rozet, adminIstek, bildir, onayIste, zamanMetni, type Sutun, type Suzgec } from '../../kit';
import './ts16.css';

export type MesajSatiri = {
  id: number; kanal: string; uid: string; ad: string; metin: string; yanit_id: number | null; at: string;
  silindi: boolean; silen: string | null; sikayet: number; ek: unknown; oda_ad: string | null; oda_tur: string | null;
};

export const kanalEtiketi = (m: { kanal: string; oda_ad?: string | null; oda_tur?: string | null }) =>
  m.kanal.startsWith('oda:') ? (m.oda_tur === 'dm' ? `Birebir #${m.kanal.slice(4)}` : `Oda: ${m.oda_ad || m.kanal.slice(4)}`) : `#${m.kanal}`;

export async function mesajGizle(m: MesajSatiri, gizli: boolean) {
  if (gizli && !(await onayIste({ baslik: 'Mesaj gizlensin mi?', aciklama: 'Mesaj öğrencilere görünmez olur. Geri açılabilir.', onayMetni: 'Gizle' }))) return false;
  await adminIstek(`/api/admin/topluluk/mesajlar/${m.id}/gizle`, { yontem: 'POST', govde: { gizli } });
  bildir(gizli ? 'Mesaj gizlendi.' : 'Mesaj yeniden görünür.', 'iyi');
  return true;
}

export async function mesajSil(m: MesajSatiri) {
  const ok = await onayIste({
    baslik: 'Mesaj kalıcı silinsin mi?', tehlikeli: true, yazilacak: 'SIL', onayMetni: 'Kalıcı sil',
    aciklama: <>Bu işlem geri alınamaz. Çoğu durumda <b>Gizle</b> yeterlidir. Silinen metnin ilk 200 karakteri denetim kaydında kalır.</>,
  });
  if (!ok) return false;
  await adminIstek(`/api/admin/topluluk/mesajlar/${m.id}`, { yontem: 'DELETE', govde: { onay: 'SIL' } });
  bildir('Mesaj silindi.', 'iyi');
  return true;
}

export function MesajTablosu(p: {
  kimlik: string; kaynak: string; suzgecler?: Suzgec[]; ekSorgu?: Record<string, unknown>; adresteDurum?: boolean;
  sikayetModu?: boolean; kanalGit?: (kanal: string) => void;
  /** H142: panel içi gezinme — yazandan Kişi 360'a ve kişinin tüm mesajlarına geçiş */
  git?: (yol: string) => void;
}) {
  const [acik, setAcik] = useState<MesajSatiri | null>(null);
  const [surum, setSurum] = useState(0);
  const sonra = (ok: boolean) => { if (ok) { setAcik(null); setSurum((x) => x + 1); } };
  const hata = (e: any) => bildir(e?.message || String(e), 'kotu');
  const sutunlar: Sutun<MesajSatiri>[] = [
    { anahtar: 'at', baslik: 'Zaman', sirala: true, genislik: '104px', hucre: (m) => <time dateTime={m.at} title={new Date(m.at).toLocaleString('tr-TR')}>{zamanMetni(m.at)}</time> },
    { anahtar: 'ad', baslik: 'Yazan', sirala: true, genislik: 'minmax(110px,1fr)',
      hucre: (m) => (p.git ? <a href={`/manage/kisi/${encodeURIComponent(m.uid)}`} title="Kişi 360" onClick={(e) => { e.preventDefault(); e.stopPropagation(); p.git!(`kisi/${encodeURIComponent(m.uid)}`); }}>{m.ad || m.uid.slice(0, 10)}</a> : m.ad) },
    { anahtar: 'metin', baslik: 'Mesaj', genislik: 'minmax(200px,3fr)', hucre: (m) => <span className="m16-kisalt" title={m.metin}>{m.metin}</span> },
    { anahtar: 'kanal', baslik: 'Kanal / oda', sirala: true, genislik: 'minmax(110px,1fr)', hucre: (m) => kanalEtiketi(m) },
    { anahtar: 'sikayet', baslik: 'Şikâyet', sirala: true, genislik: '76px', hizala: 'sag', hucre: (m) => (m.sikayet ? <Rozet ton={m.sikayet >= 3 ? 'kotu' : 'uyari'}>{m.sikayet}</Rozet> : '—') },
    { anahtar: 'silindi', baslik: 'Durum', genislik: '84px', hucre: (m) => (m.silindi ? <Rozet ton="notr" title={m.silen || ''}>Gizli</Rozet> : <Rozet ton="iyi">Görünür</Rozet>) },
  ];
  return (
    <>
      <VeriTablosu<MesajSatiri>
        key={surum}
        kimlik={p.kimlik}
        kaynak={p.kaynak}
        ekSorgu={p.ekSorgu}
        adresteDurum={p.adresteDurum}
        canliOlay={['topluluk_changed', 'topluluk', 'topluluk_sohbet']}
        aramaYeri="Metin, yazan ya da kanal ara…"
        satirKimligi={(m) => String(m.id)}
        etkin={acik ? String(acik.id) : null}
        satirTikla={setAcik}
        suzgecler={p.suzgecler}
        sutunlar={sutunlar}
        bosMetin={p.sikayetModu ? 'Şikâyet edilmiş mesaj yok.' : 'Mesaj yok.'}
      />
      <AyrintiCekmecesi
        acik={!!acik} kapat={() => setAcik(null)}
        baslik={acik ? `${acik.ad} · ${kanalEtiketi(acik)}` : ''}
        altBaslik={acik ? `#${acik.id} · ${new Date(acik.at).toLocaleString('tr-TR')}` : ''}
        kayit={acik || undefined} hedef={acik ? `mesaj:${acik.id}` : undefined}
        eylemler={acik && (
          <div className="m16-ts-eylem">
            {p.sikayetModu && acik.sikayet > 0 && (
              <button type="button" className="m16-btn" onClick={async () => {
                try { await adminIstek(`/api/admin/topluluk/sikayetler/${acik.id}/yoksay`, { yontem: 'POST', govde: {} }); bildir('Şikâyet yok sayıldı.', 'iyi'); sonra(true); } catch (e) { hata(e); }
              }}>Şikâyeti yok say</button>
            )}
            <button type="button" className="m16-btn" onClick={() => mesajGizle(acik, !acik.silindi).then(sonra, hata)}>{acik.silindi ? 'Yeniden göster' : 'Gizle'}</button>
            <button type="button" className="m16-btn tehlike" onClick={() => mesajSil(acik).then(sonra, hata)}>Kalıcı sil</button>
          </div>
        )}
      >
        {acik && (
          <>
            <div className="m16-ts-metin">{acik.metin}</div>
            <dl className="m16-satirlar">
              <dt>Kanal</dt><dd>{p.kanalGit ? <a href="#" onClick={(e) => { e.preventDefault(); p.kanalGit!(acik.kanal); }}>{kanalEtiketi(acik)}</a> : kanalEtiketi(acik)}</dd>
              <dt>Yazan</dt><dd>{p.git ? (
                <>
                  <a href={`/manage/kisi/${encodeURIComponent(acik.uid)}`} onClick={(e) => { e.preventDefault(); p.git!(`kisi/${encodeURIComponent(acik.uid)}`); }}>{acik.ad || acik.uid}</a>
                  {' · '}
                  <a href={`/manage/topluluk/mesaj?s.uid=${encodeURIComponent(acik.uid)}`} onClick={(e) => { e.preventDefault(); p.git!(`topluluk/mesaj?s.uid=${encodeURIComponent(acik.uid)}`); }}>Tüm mesajları</a>
                </>
              ) : (acik.ad || acik.uid)}</dd>
              <dt>Kullanıcı kimliği</dt><dd><code>{acik.uid}</code></dd>
              <dt>Şikâyet sayısı</dt><dd>{acik.sikayet}</dd>
              <dt>Durum</dt><dd>{acik.silindi ? `Gizli (${acik.silen || 'kullanıcı'})` : 'Görünür'}</dd>
              {acik.yanit_id && <><dt>Yanıtladığı</dt><dd>#{acik.yanit_id}</dd></>}
            </dl>
            <p className="m16-ts-not">Mesaj listelerinin her okunuşu kişisel veri okuması olarak denetim kaydına yazılır.</p>
          </>
        )}
      </AyrintiCekmecesi>
    </>
  );
}
