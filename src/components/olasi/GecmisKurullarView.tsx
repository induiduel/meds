/**
 * Geçmiş kurullar (/gecmis-kurullar): sınavı geçmiş (arşiv) kurulların içeriğine tek yerden erişim.
 * Takvim: services/kurulTakvimi (aktif = sınavı geçmemiş ilk kurul). Yerelde ?gun=YYYY-AA-GG ile tarih denenir.
 * Kurul süzgecini destekleyen sayfalara ?kurul=N ile bağlanır (Öğren, Kazanımlar, Olası sorular); diğerleri sayfanın
 * kendi kurul/ders seçimiyle açılır. Stil: styles/olasi-sorular.css (.gk-*).
 */
import React, { useEffect, useMemo } from 'react';
import {
  Archive, AudioLines, BookOpen, CalendarDays, Compass, Crosshair, GraduationCap, Library, MessageCircleQuestion, Sparkles, Star,
} from 'lucide-react';
import { KURULLAR, gunFarki, gunluBag, kurulAdi, takvimDurumu, tarihYaz, tarihteYaz, type KurulBilgi } from '../../services/kurulPencere';
import { linkClick, navigateTo } from '../../router';
import SCHEDULE from '../../data/deckSchedule.json';
import '../../styles/olasi-sorular.css';

type Bag = { ad: string; url: (k: number) => string; ikon: React.ElementType; suzgecli: boolean };
/** suzgecli: sayfa ?kurul= ile o kurula süzülerek açılır */
const BAGLAR: Bag[] = [
  { ad: 'Olası sorular', url: (k) => `/olasi-sorular?kurul=${k}`, ikon: Sparkles, suzgecli: true },
  { ad: 'Etkileşimli dersler', url: (k) => `/ogren?kurul=${k}`, ikon: BookOpen, suzgecli: true },
  { ad: 'Kazanımlar', url: (k) => `/kazanimlar?kurul=${k}`, ikon: Compass, suzgecli: true },
  { ad: 'Sesli ders', url: () => '/canliders', ikon: AudioLines, suzgecli: false },
  { ad: 'En önemliler', url: () => '/en-onemliler', ikon: Star, suzgecli: false },
  { ad: 'Sınav spotları', url: () => '/spotlar', ikon: Crosshair, suzgecli: false },
  { ad: 'Soru çözücü', url: () => '/soru-cozucu', ikon: MessageCircleQuestion, suzgecli: false },
  { ad: 'Çıkmış sorular', url: () => '/cikmis', ikon: Library, suzgecli: false },
];

const desteSayisi = (k: number) => Object.values(SCHEDULE as Record<string, { k?: number }>).filter((x) => x.k === k).length;

const Git: React.FC<{ url: string; className?: string; children: React.ReactNode }> = ({ url, className, children }) => {
  const u = gunluBag(url);
  return <a href={u} className={className} onClick={linkClick(() => navigateTo(u))}>{children}</a>;
};

export default function GecmisKurullarView() {
  const t = useMemo(() => takvimDurumu(), []);
  useEffect(() => { document.title = 'Geçmiş kurullar · MeDSor'; }, []);
  const arsiv = [...t.arsiv].reverse();

  const durumu = (k: KurulBilgi) =>
    k.sinav < t.gun ? 'gecti' : k.kurul === t.aktif.kurul ? 'aktif' : 'gelecek';

  return (
    <div className="os gk">
      <header className="os-bas">
        <span className="os-ic" aria-hidden><Archive /></span>
        <div className="os-bas-m">
          <h1>Geçmiş kurullar</h1>
          <p>Sınavı biten kurulların dersleri, sesli anlatımları, spotları ve soruları silinmez; buradan açılır.</p>
        </div>
      </header>

      {arsiv.length === 0 ? (
        <div className="os-bos">
          <CalendarDays aria-hidden className="os-bos-i" />
          <b>Henüz geçmiş kurul yok</b>
          <p>
            {kurulAdi(t.aktif)} sınavı {tarihteYaz(t.aktif.sinav)}
            {t.kalan > 0 ? ` (${t.kalan} gün sonra)` : t.kalan === 0 ? ' (bugün)' : ''}. Sınav bitince bu kurulun bütün içeriği burada toplanır.
          </p>
        </div>
      ) : (
        <div className="gk-liste">
          {arsiv.map((k) => (
            <section key={k.kurul} className="gk-kart" aria-labelledby={`gk-${k.kurul}`}>
              <div className="gk-kart-bas">
                <span className="gk-no">Kurul {k.kurul}</span>
                <h2 id={`gk-${k.kurul}`}>{kurulAdi(k)}</h2>
                <p>{k.kod} · {tarihYaz(k.baslangic, t.gun)} – {tarihYaz(k.sinav, t.gun)} · sınavın üzerinden {gunFarki(k.sinav, t.gun)} gün geçti · {desteSayisi(k.kurul)} etkileşimli ders</p>
              </div>
              <ul className="gk-baglar">
                {BAGLAR.map((b) => (
                  <li key={b.ad}>
                    <Git url={b.url(k.kurul)} className="gk-bag">
                      <b.ikon aria-hidden />
                      <span>{b.ad}{!b.suzgecli && <small>tüm kurullar</small>}</span>
                    </Git>
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </div>
      )}

      <section className="gk-takvim" aria-labelledby="gk-takvim-b">
        <h2 id="gk-takvim-b"><GraduationCap aria-hidden /> Dönem takvimi</h2>
        <ol>
          {KURULLAR.map((k) => {
            const d = durumu(k);
            return (
              <li key={k.kurul} className={`is-${d}`}>
                <span className="gk-t-no">K{k.kurul}</span>
                <span className="gk-t-ad">{kurulAdi(k)}</span>
                <span className="gk-t-tarih">sınav {tarihYaz(k.sinav, t.gun)}</span>
                <span className="gk-t-durum">{d === 'gecti' ? 'bitti' : d === 'aktif' ? (t.kalan === 0 ? 'bugün sınav' : `${t.kalan} gün kaldı`) : 'sırada'}</span>
              </li>
            );
          })}
        </ol>
      </section>
    </div>
  );
}
