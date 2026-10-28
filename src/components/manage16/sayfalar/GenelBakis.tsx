import React from 'react';
import { RefreshCw, Users, AlertTriangle, MessageCircleHeart, Tent, Bot, FlaskConical, Bug, Construction, Megaphone, EyeOff } from 'lucide-react';
import { useAdminSorgu, SayfaBasligi, IstatistikKart, IstatistikIzgara, Hata, Yukleniyor, Rozet, Durum, durumTonu, zamanMetni, BosDurum, type DenetimSatiri } from '../kit';
import { TUM_SAYFALAR, manageAdres, type SayfaProps } from '../menu';

type Ozet = {
  zaman: string;
  saglik: { pg: boolean; calismaSn: number; yiginMb: number; rssMb: number; yuk: number; sseIstemci: number; sunucu: string };
  kullanici: { bugun: number; simdi: number; hafta: number };
  bekleyen: { sikayet: number; geriBildirim: number; tuyo: number; onarim: number; faz14: number };
  hata: { istemci24s: number };
  site: { bakim: boolean; duyuru: boolean; gizliSayfa: number };
  surum: { onem: number | null; baslik: string | null; commit: string | null; dagitim: string | null };
  sonDenetim: DenetimSatiri[];
  sureMs: number;
};

const sure = (sn: number) => (sn < 3600 ? `${Math.floor(sn / 60)} dk` : sn < 86400 ? `${Math.floor(sn / 3600)} sa` : `${Math.floor(sn / 86400)} gün`);
const HIZLI = ['gelen', 'kisi', 'topluluk/sikayet', 'sorular/cikmis', 'site/gorunurluk', 'site/bakim', 'sistem/llm', 'sistem/denetim'];

export default function GenelBakis({ git }: SayfaProps) {
  const { veri: o, hata, yukleniyor, yenile } = useAdminSorgu<Ozet>('/api/admin/ozet', { canliOlay: ['denetim_eklendi', 'site_ayar_changed'], aralikMs: 60_000 });
  const y = yukleniyor && !o;
  const ton = (n?: number): 'uyari' | 'notr' => (n ? 'uyari' : 'notr');
  return (
    <>
      <SayfaBasligi
        baslik="Genel bakış"
        aciklama={o ? `Sunucu ${o.saglik.sunucu} · ${zamanMetni(o.zaman)} güncellendi` : 'Sitenin durumu ve bekleyen işler'}
        eylemler={<button type="button" className="m16-btn" onClick={() => void yenile()} disabled={yukleniyor}><RefreshCw className={yukleniyor ? 'm16-don' : ''} aria-hidden="true" />Yenile</button>}
      />
      {hata && !o ? <Hata hata={hata} yenile={yenile} /> : (
        <>
          <IstatistikIzgara>
            <IstatistikKart etiket="Şu an çevrimiçi" ikon={<Users aria-hidden="true" />} deger={o?.kullanici.simdi ?? '–'} alt={o ? `bugün ${o.kullanici.bugun} · 7 gün ${o.kullanici.hafta}` : undefined} yukleniyor={y} onClick={() => git('kisi')} />
            <IstatistikKart etiket="Bekleyen şikâyet" ikon={<AlertTriangle aria-hidden="true" />} deger={o?.bekleyen.sikayet ?? '–'} ton={ton(o?.bekleyen.sikayet)} yukleniyor={y} onClick={() => git('topluluk/sikayet')} />
            <IstatistikKart etiket="Açık geri bildirim" ikon={<MessageCircleHeart aria-hidden="true" />} deger={o?.bekleyen.geriBildirim ?? '–'} ton={ton(o?.bekleyen.geriBildirim)} yukleniyor={y} onClick={() => git('topluluk/geri-bildirim')} />
            <IstatistikKart etiket="Tüyo önerisi" ikon={<Tent aria-hidden="true" />} deger={o?.bekleyen.tuyo ?? '–'} ton={ton(o?.bekleyen.tuyo)} yukleniyor={y} onClick={() => git('ogrenme/kamp')} />
            <IstatistikKart etiket="Onarım kuyruğu" ikon={<Bot aria-hidden="true" />} deger={o?.bekleyen.onarim ?? '–'} alt={o ? `Faz 14: ${o.bekleyen.faz14}` : undefined} yukleniyor={y} onClick={() => git('sistem/llm')} />
            <IstatistikKart etiket="İstemci hatası (24 sa)" ikon={<Bug aria-hidden="true" />} deger={o?.hata.istemci24s ?? '–'} ton={o?.hata.istemci24s ? 'kotu' : 'notr'} yukleniyor={y} onClick={() => git('sistem/saglik')} />
          </IstatistikIzgara>

          <div className="m16-izgara-2">
            <section className="m16-kart" aria-labelledby="gb-denetim">
              <h2 id="gb-denetim">Son yönetici işlemleri <a className="m16-btn hayalet" href={manageAdres('sistem/denetim')} onClick={(e) => { e.preventDefault(); git('sistem/denetim'); }}>Tümü</a></h2>
              {y ? <Yukleniyor satir={5} /> : !o?.sonDenetim.length ? <BosDurum baslik="Henüz kayıt yok" aciklama="Yönetici yazma işlemleri burada görünür." /> : (
                <ul className="m16-liste">
                  {o.sonDenetim.map((d) => (
                    <li key={d.id}>
                      <Rozet ton={durumTonu(d.durum)}>{d.tur === 'okuma' ? 'OKUMA' : d.yontem}</Rozet>
                      <code className="m16-kisalt" title={d.uc}>{d.uc}{d.hedef ? ` · ${d.hedef}` : ''}</code>
                      <time dateTime={d.at}>{zamanMetni(d.at)}</time>
                    </li>
                  ))}
                </ul>
              )}
            </section>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <section className="m16-kart" aria-labelledby="gb-saglik">
                <h2 id="gb-saglik">Sağlık</h2>
                {y ? <Yukleniyor satir={4} /> : o && (
                  <dl className="m16-satirlar">
                    <dt>Veritabanı</dt><dd><Durum ton={o.saglik.pg ? 'iyi' : 'kotu'}>{o.saglik.pg ? 'bağlı' : 'kopuk'}</Durum></dd>
                    <dt>Çalışma süresi</dt><dd>{sure(o.saglik.calismaSn)}</dd>
                    <dt>Bellek</dt><dd>{o.saglik.yiginMb} / {o.saglik.rssMb} MB</dd>
                    <dt>Yük (1 dk)</dt><dd>{o.saglik.yuk.toFixed(2)}</dd>
                    <dt>Canlı bağlantı</dt><dd>{o.saglik.sseIstemci}</dd>
                    <dt>Sürüm</dt><dd title={o.surum.baslik || ''}>{o.surum.onem ?? '–'}{o.surum.commit ? ` · ${o.surum.commit.slice(0, 7)}` : ''}</dd>
                  </dl>
                )}
              </section>
              <section className="m16-kart" aria-labelledby="gb-site">
                <h2 id="gb-site">Site</h2>
                {o && (
                  <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                    <Rozet ton={o.site.bakim ? 'kotu' : 'iyi'}><Construction aria-hidden="true" />{o.site.bakim ? 'Bakımda' : 'Yayında'}</Rozet>
                    <Rozet ton={o.site.duyuru ? 'vurgu' : 'notr'}><Megaphone aria-hidden="true" />{o.site.duyuru ? 'Duyuru açık' : 'Duyuru yok'}</Rozet>
                    <Rozet ton={o.site.gizliSayfa ? 'uyari' : 'notr'}><EyeOff aria-hidden="true" />{o.site.gizliSayfa} sayfa ayarı</Rozet>
                  </div>
                )}
              </section>
              <section className="m16-kart" aria-labelledby="gb-hizli">
                <h2 id="gb-hizli">Hızlı bağlantılar</h2>
                <div className="m16-hizli">
                  {HIZLI.flatMap((yol) => TUM_SAYFALAR.filter((s) => s.yol === yol)).map((s) => (
                    <a key={s.yol} href={manageAdres(s.yol)} onClick={(e) => { e.preventDefault(); git(s.yol); }}><s.ikon aria-hidden="true" />{s.etiket}</a>
                  ))}
                  <a href={manageAdres('sistem/fazlar')} onClick={(e) => { e.preventDefault(); git('sistem/fazlar'); }}><FlaskConical aria-hidden="true" />Fazlar</a>
                </div>
              </section>
            </div>
          </div>
        </>
      )}
    </>
  );
}
