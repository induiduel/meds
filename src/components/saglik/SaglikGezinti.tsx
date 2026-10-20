import React from 'react';
import { createPortal } from 'react-dom';
import {
  HeartPulse,
  ArrowLeft, ArrowRight, Check, ChevronLeft, ChevronRight, History, LayoutDashboard, LayoutGrid, List, ListTree, Presentation, Rows3, Rows4,
  SlidersHorizontal, Target, TriangleAlert,
} from 'lucide-react';
import { Dialog } from '../ui/Dialog';
import { linkClick, pathFor } from '../../router';
import { BOLUMLER, BOLUM_GRUPLARI, type BolumId, type BolumTanim, type SaglikVeri } from './saglikVeri';
import type { GorunumModu } from './saglikBaglam';
import { tarihTR } from './SaglikOrtak';

/**
 * Sağlık Bakanlığı gezintisi (2026-10-16 yeniden kurulum): giriş sayfasında gruplu bölüm dizini, bölüm sayfalarında
 * tek satırlık çubuk (tüm bölümler · bölüm seç · görünüm), bölüm sonunda önceki/sonraki. Görünüm ayarları ve işaret
 * açıklaması pencerede (telefonda alttan sayfa) — sayfanın üstünde kalıcı yer kaplamaz.
 */

export const bolumYolu = (b: BolumTanim) => `${pathFor('health_ministry')}${b.slug ? `/${b.slug}` : ''}`;

/** Okuma sırası: Sınav → Veriler → Sistem ve kavramlar (Genel bakış giriş sayfasıdır, sıraya girmez) */
export const BOLUM_SIRASI: BolumTanim[] = BOLUM_GRUPLARI.flatMap((g) => BOLUMLER.filter((b) => b.grup === g.id && b.id !== 'genel'));

const GRUP_ALT: Record<BolumTanim['grup'], string> = {
  sinav: 'Çıkmış sorulardan çıkarılan bilinmesi gerekenler',
  veri: 'Resmî sayılar · Türkiye ve Karabük',
  sistem: 'Ders konuları · kavram, sistem, mevzuat',
};

type Git = (id: BolumId) => void;

const soruSayisi = (v: SaglikVeri | null, id: BolumId) => v?.baglantilar.bolumler[id]?.soru_sayisi || 0;

/** Liste satırı: simge · ad + tek satır açıklama · çıkmış soru sayısı · ok (seçiliyse ✓) */
const BolumSatir: React.FC<{ b: BolumTanim; v: SaglikVeri | null; git: Git; aktif?: boolean; aciklamasiz?: boolean }> = ({ b, v, git, aktif, aciklamasiz }) => {
  const Ic = b.icon;
  const n = soruSayisi(v, b.id);
  return (
    <li>
      <a href={bolumYolu(b)} className="sbk-satir-l" aria-current={aktif ? 'page' : undefined} onClick={linkClick(() => git(b.id))}>
        <span className="sbk-satir-l-ic" aria-hidden><Ic /></span>
        <span className="sbk-satir-l-m">
          <span className="sbk-satir-l-t">{b.ad}</span>
          {!aciklamasiz && <span className="sbk-satir-l-a">{b.aciklama}</span>}
        </span>
        {n > 0 && <span className="sbk-satir-l-n" title={`${n} çıkmış soru bu bölümün konularından`}><b data-num>{n}</b> soru</span>}
        {aktif ? <Check aria-hidden className="sbk-satir-l-ok is-aktif" /> : <ChevronRight aria-hidden className="sbk-satir-l-ok" />}
      </a>
    </li>
  );
};

/** Giriş sayfası dizini: öne çıkan bilgi havuzu + iki gruplu liste (Veriler · Sistem ve kavramlar) */
export const SaglikDizin: React.FC<{ v: SaglikVeri; git: Git }> = ({ v, git }) => {
  const havuz = BOLUMLER.find((b) => b.id === 'havuz');
  const HavuzIc = havuz?.icon;
  return (
    <section className="sbk-dizin" aria-label="Bölümler">
      {havuz && HavuzIc && (
        <a href={bolumYolu(havuz)} className="sbk-dizin-one" onClick={linkClick(() => git(havuz.id))}>
          <span className="sbk-dizin-one-ic" aria-hidden><HavuzIc /></span>
          <span className="sbk-dizin-one-m">
            <span className="sbk-dizin-one-e">Sınava hazırlık</span>
            <span className="sbk-dizin-one-t">{havuz.ad}</span>
            <span className="sbk-dizin-one-a">Halk Sağlığı çıkmış sorularından çıkarılan bilinmesi gerekenler: konu → başlık → madde.</span>
          </span>
          <ArrowRight aria-hidden className="sbk-dizin-one-ok" />
        </a>
      )}
      <div className="sbk-dizin-g">
        {BOLUM_GRUPLARI.filter((g) => g.id !== 'sinav').map((g) => (
          <div key={g.id} className="sbk-dizin-grup">
            <h2>{g.ad} <small>{GRUP_ALT[g.id]}</small></h2>
            <ul className="sbk-liste">
              {BOLUMLER.filter((b) => b.grup === g.id && b.id !== 'genel').map((b) => <BolumSatir key={b.id} b={b} v={v} git={git} />)}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
};

/** Bölüm değiştirici: tüm bölümler gruplu tek listede; seçilince kapanır */
const BolumSecici: React.FC<{ aktif: BolumId; v: SaglikVeri | null; git: Git; onClose: () => void }> = ({ aktif, v, git, onClose }) => {
  const sec: Git = (id) => { onClose(); git(id); };
  const genel = BOLUMLER.find((b) => b.id === 'genel')!;
  return (
    <Dialog title="Bölümler" subtitle="Sağlık Bakanlığı" onClose={onClose} width="max-w-lg">
      <div className="sbk-pen">
        <ul className="sbk-liste">
          <BolumSatir b={{ ...genel, icon: LayoutDashboard }} v={null} git={sec} aktif={aktif === 'genel'} aciklamasiz />
        </ul>
        {BOLUM_GRUPLARI.map((g) => (
          <div key={g.id} className="sbk-pen-grup">
            <h3>{g.ad}</h3>
            <ul className="sbk-liste">
              {BOLUMLER.filter((b) => b.grup === g.id && b.id !== 'genel').map((b) => <BolumSatir key={b.id} b={b} v={v} git={sec} aktif={b.id === aktif} aciklamasiz />)}
            </ul>
          </div>
        ))}
      </div>
    </Dialog>
  );
};

/** Seçenek kartı (radyo): simge · ad · kısa açıklama */
const Secenek: React.FC<{ sec: boolean; onClick: () => void; ic: React.ElementType; ad: string; alt: string }> = ({ sec, onClick, ic: Ic, ad, alt }) => (
  <button type="button" role="radio" aria-checked={sec} className={`sbk-tercih ${sec ? 'is-sec' : ''}`} onClick={onClick}>
    <Ic aria-hidden />
    <span><b>{ad}</b><small>{alt}</small></span>
  </button>
);

export interface GorunumAyar {
  mod: GorunumModu; setMod: (m: GorunumModu) => void;
  kompakt: boolean; setKompakt: (k: boolean) => void;
}

/** Görünüm penceresi: gösterim · yoğunluk · sayfadaki işaretlerin anlamı · veri tarihi */
const GorunumPenceresi: React.FC<GorunumAyar & { guncelleme?: string; dersVar: boolean; onClose: () => void }> = ({ mod, setMod, kompakt, setKompakt, guncelleme, dersVar, onClose }) => (
  <Dialog title="Görünüm" subtitle="Tercihin bu cihazda hatırlanır" onClose={onClose} width="max-w-md">
    <div className="sbk-pen">
      <div className="sbk-pen-grup">
        <h3>Gösterim</h3>
        <div className="sbk-tercih-g" role="radiogroup" aria-label="Gösterim">
          <Secenek sec={mod === 'kart'} onClick={() => setMod('kart')} ic={LayoutGrid} ad="Kart" alt="Grafikler, tablolar, kutular" />
          <Secenek sec={mod === 'madde'} onClick={() => setMod('madde')} ic={List} ad="Madde madde" alt="Okunur liste, hızlı tekrar" />
        </div>
      </div>
      <div className="sbk-pen-grup">
        <h3>Yoğunluk</h3>
        <div className="sbk-tercih-g" role="radiogroup" aria-label="Yoğunluk">
          <Secenek sec={!kompakt} onClick={() => setKompakt(false)} ic={Rows3} ad="Rahat" alt="Açıklamalar görünür" />
          <Secenek sec={kompakt} onClick={() => setKompakt(true)} ic={Rows4} ad="Kompakt" alt="Daha çok içerik, az boşluk" />
        </div>
      </div>
      <div className="sbk-pen-grup">
        <h3>Sayfadaki işaretler</h3>
        <ul className="sbk-isaret-l">
          <li><span className="sbk-atif" aria-hidden>1</span><span><b>Kaynak numarası</b> · dokun, resmî kaynağı aç</span></li>
          <li><span className="sbk-kpi-gecmis" aria-hidden><History /> 15 yıl</span><span><b>Geçmiş yıllar</b> · dokun, grafiği gör</span></li>
          {dersVar && <li><span className="sbk-ders-i-b is-ornek" aria-hidden><Presentation /></span><span><b>Ders slaytında / çıkmış soruda geçiyor</b> · sarı vurgulu değer; dokun, slaytı gör</span></li>}
          {dersVar && <li><span className="sbk-ders-i-b is-ornek is-farkli" aria-hidden><TriangleAlert /></span><span><b>Slaytta farklı değer</b> · aynı yıl için ders slaytı başka sayı veriyor</span></li>}
          {dersVar && <li><span className="sbk-isaret-terim" aria-hidden>terim</span><span><b>Derste geçen terim</b> · noktalı alt çizgi; dokun, slaytı gör</span></li>}
        </ul>
      </div>
      {guncelleme && <p className="sbk-pen-not">Veriler {tarihTR(guncelleme)} tarihinde T.C. Sağlık Bakanlığı, TÜİK ve Karabük İl Sağlık Müdürlüğü kaynaklarından derlendi.</p>}
    </div>
  </Dialog>
);

type Pencere = 'bolum' | 'gorunum' | null;

/** Pencereler gövdeye taşınır (kabuk katmanlarının kırpmasından etkilenmesin) */
const Portal: React.FC<{ children: React.ReactNode }> = ({ children }) => createPortal(children, document.body);

/**
 * Sayfa başı. Girişte: başlık + kısa açıklama + görünüm düğmesi. Bölümde: tüm bölümler · bölüm seç · görünüm çubuğu,
 * altında bölüm başlığı ve (panel yanda değilken) "Derste ve sınavda" kısayolu.
 */
export const SaglikBaslik: React.FC<GorunumAyar & {
  bolum: BolumTanim; v: SaglikVeri | null; git: Git; dersVar: boolean; onPanel?: () => void;
}> = ({ bolum, v, git, dersVar, onPanel, ...ayar }) => {
  const [pencere, setPencere] = React.useState<Pencere>(null);
  const kapat = () => setPencere(null);
  const genel = bolum.id === 'genel';
  const Ic = bolum.icon;
  const n = soruSayisi(v, bolum.id);
  const gorunumBtn = (
    <button type="button" className="sbk-gez-b is-ikon" aria-label="Görünüm ve işaretler" title="Görünüm" onClick={() => setPencere('gorunum')}>
      <SlidersHorizontal aria-hidden /><span className="sbk-gez-y">Görünüm</span>
    </button>
  );
  return (
    <>
      {genel ? (
        <header className="sbk-giris">
          <span className="sbk-giris-ic" aria-hidden><HeartPulse /></span>
          <div className="sbk-giris-m">
            <span className="sbk-giris-ust">Kurul 1 · Halk Sağlığı</span>
            <h1>Sağlık Bakanlığı</h1>
            <p>Resmî veriler; her sayı kaynaklı, dersteki slaytına ve çıkmış sorularına bağlı.</p>
          </div>
          {gorunumBtn}
        </header>
      ) : (
        <>
          <div className="sbk-gez">
            <a href={bolumYolu(BOLUMLER[0])} className="sbk-gez-geri" onClick={linkClick(() => git('genel'))}>
              <ChevronLeft aria-hidden /><span>Tüm bölümler</span>
            </a>
            <div className="sbk-gez-sag">
              <button type="button" className="sbk-gez-b" aria-haspopup="dialog" onClick={() => setPencere('bolum')}>
                <ListTree aria-hidden /><span>Bölüm seç</span>
              </button>
              {gorunumBtn}
            </div>
          </div>
          <div className="sbk-bolum-h">
            <span className="sbk-bolum-ic" aria-hidden><Ic /></span>
            <div className="sbk-bolum-h-m">
              <h1>{bolum.ad}</h1>
              <p>{bolum.aciklama}</p>
              {n > 0 && onPanel && (
                <button type="button" className="sbk-panel-kisa" onClick={onPanel}>
                  <Target aria-hidden /><span><b data-num>{n}</b> çıkmış soru<span className="sbk-panel-kisa-e"> · derste ve sınavda</span></span><ChevronRight aria-hidden />
                </button>
              )}
            </div>
          </div>
        </>
      )}
      {pencere && (
        <Portal>
          {pencere === 'bolum'
            ? <BolumSecici aktif={bolum.id} v={v} git={git} onClose={kapat} />
            : <GorunumPenceresi {...ayar} guncelleme={v?.guncelleme} dersVar={dersVar} onClose={kapat} />}
        </Portal>
      )}
    </>
  );
};

/** Bölüm sonu: okuma sırasında önceki / sonraki bölüm */
export const BolumSonu: React.FC<{ bolum: BolumId; git: Git }> = ({ bolum, git }) => {
  const i = BOLUM_SIRASI.findIndex((b) => b.id === bolum);
  if (i < 0) return null;
  const onceki = BOLUM_SIRASI[i - 1];
  const sonraki = BOLUM_SIRASI[i + 1];
  return (
    <nav className="sbk-sonraki" aria-label="Diğer bölümler">
      {onceki ? (
        <a href={bolumYolu(onceki)} className="is-onceki" onClick={linkClick(() => git(onceki.id))}>
          <ArrowLeft aria-hidden /><span><small>Önceki</small><b>{onceki.ad}</b></span>
        </a>
      ) : <span />}
      {sonraki ? (
        <a href={bolumYolu(sonraki)} className="is-sonraki" onClick={linkClick(() => git(sonraki.id))}>
          <span><small>Sonraki</small><b>{sonraki.ad}</b></span><ArrowRight aria-hidden />
        </a>
      ) : (
        <a href={bolumYolu(BOLUMLER[0])} className="is-sonraki" onClick={linkClick(() => git('genel'))}>
          <span><small>Bitti</small><b>Tüm bölümler</b></span><ArrowRight aria-hidden />
        </a>
      )}
    </nav>
  );
};
