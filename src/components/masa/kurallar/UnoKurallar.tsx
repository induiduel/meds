/**
 * Uno kuralları: ortak temel + mod seçici + seçili modun sayfası (nasıl oynanır, kartları tanı, özel kurallar, puan, ipuçları).
 * Metin ve kart tablosu uno/kartRehber.ts'ten gelir; o dosya motorla (motor/uno.ts) birebirdir.
 */
import React, { useEffect, useRef, useState } from 'react';
import { ArrowDown, Check, Info, Layers, Lightbulb, Megaphone, Target, Upload, Users, X } from 'lucide-react';
import { UNO_MODLAR, UNO_MOD_GRUPLAR, unoModTanim, type UnoDeger, type UnoMod, type UnoModTanim, type UnoRenk } from '../../../services/masa/tipler';
import { KartOrnek } from '../kabukOrtak';
import { Figur, type FigurAd } from '../uno/figurler';
import { MOD_REHBER, modKartlari, type ModKart } from '../uno/kartRehber';
import { Akis, Kunye } from './gorsel';
import '../../../styles/masa/uno-rehber.css';

type K = [UnoRenk | null, UnoDeger];
const ZORLUK = ['', 'Kolay', 'Orta', 'Zor'];
const FIGURLER: readonly string[] = ['kitty', 'batman', 'kuromi', 'pony'];
const GRUP_AD: Record<ModKart['grup'], string> = { sayi: 'Sayı kartları', aksiyon: 'Renkli aksiyon kartları', joker: 'Jokerler', ozel: 'Karakter kartları' };
const GRUP_SIRA: ModKart['grup'][] = ['sayi', 'aksiyon', 'joker', 'ozel'];

export const oyuncuAraligi = (m: UnoModTanim) => (m.cift ? '4, 6 ya da 8 oyuncu' : `${m.enAz}–${m.enCok} oyuncu`);

function Kartlar({ k, ad, iyi }: { k: K[]; ad: string; iyi?: boolean }) {
  return (
    <figure className={`mk-ornek${iyi === false ? ' is-kotu' : iyi ? ' is-iyi' : ''}`}>
      <div className="mk-ornek-sira is-kart">{k.map(([renk, deger], i) => <KartOrnek key={i} renk={renk} deger={deger} boy={40} />)}</div>
      <figcaption>{iyi !== undefined && (iyi ? <Check size={15} /> : <X size={15} />)} {ad}</figcaption>
    </figure>
  );
}

/** Zorluk noktaları (1–3) */
export function ZorlukNokta({ z }: { z: 1 | 2 | 3 }) {
  return (
    <span className="mk-zorluk" role="img" aria-label={`Zorluk: ${ZORLUK[z]}`}>
      {[1, 2, 3].map((i) => <i key={i} className={i <= z ? 'is-dolu' : ''} />)}
    </span>
  );
}

function KartKutu({ k, tema }: { k: ModKart; tema: string }) {
  const figur = FIGURLER.includes(k.yuz.deger) ? (k.yuz.deger as FigurAd) : null;
  const yuzler = k.ornekler ?? [k.yuz];
  return (
    <li className={`mk-urk${k.taraf === 'koyu' ? ' is-koyu' : ''}`}>
      <div className="mk-urk-resim" aria-hidden="true">
        {yuzler.map((y, i) => <KartOrnek key={i} yuz={y} tema={tema} boy={yuzler.length > 1 ? 40 : 58} />)}
        {figur && <Figur ad={figur} boy={44} className="mk-urk-figur" />}
      </div>
      <div className="mk-urk-metin">
        <div className="mk-urk-bas">
          <b>{k.bilgi.ad}</b>
          <span className="mk-urk-adet">{k.adet} kart</span>
          <span className="mk-urk-puan">{k.bilgi.puan < 0 ? 'sayı kadar puan' : `${k.bilgi.puan} puan`}</span>
        </div>
        {k.flexBilgi ? (
          <dl className="mk-urk-flex">
            <div><dt>Düz yüz</dt><dd>{k.bilgi.etki}</dd></div>
            <div className="is-flex"><dt>Flex yüz</dt><dd>{k.flexBilgi.etki}</dd></div>
          </dl>
        ) : <p>{k.bilgi.etki}</p>}
        {k.bilgi.ipucu && <small className="mk-urk-ipucu"><Lightbulb size={14} aria-hidden="true" /> {k.bilgi.ipucu}</small>}
      </div>
    </li>
  );
}

function KartGalerisi({ mod, tema }: { mod: UnoMod; tema: string }) {
  const kartlar = modKartlari(mod);
  const bolum = (baslik: string | null, liste: ModKart[], anahtar: string) => (
    <div key={anahtar} className="mk-urk-bolum">
      {baslik && <h4>{baslik}</h4>}
      {GRUP_SIRA.filter((g) => liste.some((k) => k.grup === g)).map((g) => (
        <div key={g} className="mk-urk-grup">
          <span className="mk-urk-grup-ad">{GRUP_AD[g]}</span>
          <ul className="mk-urkler">{liste.filter((k) => k.grup === g).map((k, i) => <KartKutu key={`${g}${i}`} k={k} tema={tema} />)}</ul>
        </div>
      ))}
    </div>
  );
  if (mod === 'flip') {
    return (
      <>
        {bolum('Açık yüz (oyun bununla başlar)', kartlar.filter((k) => k.taraf === 'acik'), 'acik')}
        {bolum('Koyu yüz (Flip oynanınca)', kartlar.filter((k) => k.taraf === 'koyu'), 'koyu')}
      </>
    );
  }
  return bolum(null, kartlar, 'tek');
}

function ModSayfasi({ mod, tema }: { mod: UnoMod; tema: string }) {
  const t = unoModTanim(mod);
  const r = MOD_REHBER[mod];
  return (
    <section className="mk-umod" aria-label={`${t.ad} modu`}>
      <header className="mk-umod-bas">
        <div className="mk-umod-kartlar" aria-hidden="true">
          {t.ornek.map(([renk, deger], i) => <KartOrnek key={i} renk={renk} deger={deger} tema={tema} boy={52} />)}
        </div>
        <div className="mk-umod-kimlik">
          <h3>{t.ad}</h3>
          <p className="mk-umod-slogan">{r.slogan}</p>
          <div className="mk-kunye-cipler">
            <span><Layers size={14} aria-hidden="true" /> {t.deste} kart</span>
            <span>Kişi başı {t.elKart} kart</span>
            <span><Users size={14} aria-hidden="true" /> {oyuncuAraligi(t)}</span>
            <span><ZorlukNokta z={t.zorluk} /> {ZORLUK[t.zorluk]}</span>
            {t.hedef > 0 && <span className="is-amac"><Target size={14} aria-hidden="true" /> Hedef {t.hedef} puan</span>}
          </div>
        </div>
      </header>
      <p className="mk-kural-giris">{r.ozet}</p>

      <h3>Nasıl oynanır</h3>
      <ol className="mk-adimlar mk-umod-adimlar">{r.nasil.map((s) => <li key={s}>{s}</li>)}</ol>

      {mod === 'klasik' && (
        <>
          <h3>Hangi kart oynanır</h3>
          <div className="mk-ornekler">
            <Kartlar k={[['k', '7'], ['k', '2']]} ad="Aynı renk" iyi />
            <Kartlar k={[['k', '7'], ['m', '7']]} ad="Aynı sayı" iyi />
            <Kartlar k={[['y', 'pas'], ['m', 'pas']]} ad="Aynı simge" iyi />
            <Kartlar k={[['k', '7'], ['y', '3']]} ad="Renk de sayı da tutmuyor" iyi={false} />
          </div>
        </>
      )}

      <h3>Kartları tanı</h3>
      <KartGalerisi mod={mod} tema={tema} />

      <h3>Bu modun kuralları</h3>
      <dl className="mk-ukural">
        {r.ozelKurallar.map((k) => (
          <div key={k.baslik}><dt>{k.baslik}</dt><dd>{k.metin}</dd></div>
        ))}
      </dl>

      <h3>Puan</h3>
      <table className="mk-kural-tablo">
        <tbody>{r.puan.map(([ad, p]) => <tr key={ad}><th scope="row">{ad}</th><td>{p}</td></tr>)}</tbody>
      </table>
      <p>
        {mod === 'takim'
          ? 'El bitince kazanan takımın iki oyuncusu da rakiplerin elindeki kartların toplam değerini alır; kaybedenler kendi ellerindeki kartların değeri kadar eksi alır.'
          : 'El bitince kaybedenler ellerindeki kartların değeri kadar eksi alır; kazanan bu değerlerin toplamını artı olarak alır.'}
        {t.hedef > 0 ? ` Maç, seçilen el sayısı dolunca ya da bir oyuncu ${t.hedef} puana ulaşınca biter.` : ' Maç, lobide seçilen el sayısı dolunca biter.'}
      </p>

      <h3>İpuçları</h3>
      <ul className="mk-uipucu">{r.ipuclari.map((s) => <li key={s}><Lightbulb size={16} aria-hidden="true" /><span>{s}</span></li>)}</ul>

      {r.kaynakNotu && <p className="mk-ukaynak"><Info size={15} aria-hidden="true" /> <span>{r.kaynakNotu}</span></p>}
    </section>
  );
}

export default function UnoKurallar({ mod: ilkMod = 'klasik', tema = 'klasik' }: { mod?: UnoMod; tema?: string }) {
  const [mod, setMod] = useState<UnoMod>(UNO_MODLAR.some((m) => m.id === ilkMod) ? ilkMod : 'klasik');
  const sayfaRef = useRef<HTMLDivElement>(null);
  const ilkCizim = useRef(true);
  useEffect(() => { setMod(UNO_MODLAR.some((m) => m.id === ilkMod) ? ilkMod : 'klasik'); }, [ilkMod]);
  // Mod değişince (ilk açılış hariç) sayfanın başı görünür olsun
  useEffect(() => {
    if (ilkCizim.current) { ilkCizim.current = false; return; }
    sayfaRef.current?.scrollIntoView?.({ block: 'start', behavior: 'smooth' });
  }, [mod]);
  return (
    <article className="mk-kural mk-uno-kural" role="tabpanel">
      <Kunye tur="uno" malzeme="16 mod, 56–168 kart" amac="elindeki kartları ilk bitiren olmak" />
      <p className="mk-kural-giris">Uno’nun özü her modda aynıdır: ortadaki kartla <b>rengi</b>, <b>sayısı</b> ya da <b>simgesi</b> tutan kartı atarsın, atamıyorsan kart çekersin, tek kartın kalınca <b>UNO</b> dersin. Modlar bu temelin üstüne kendi destesini ve kurallarını ekler; kurucu modu lobide seçer.</p>
      <Akis adimlar={[
        { ikon: <Upload size={18} />, ad: 'Kart at', metin: 'Ortadaki kartla rengi, sayısı ya da simgesi tutan kartı at.' },
        { ikon: <ArrowDown size={18} />, ad: 'Kart çek', metin: 'Oynayamıyorsan kart çek; uyuyorsa hemen atabilirsin.', bag: 'yada' },
        { ikon: <Megaphone size={18} />, ad: 'UNO de', metin: 'Tek kartın kalınca UNO de; unutup yakalanırsan ceza çekersin.' },
      ]} />

      <h3 id="mk-uno-modlar">Modunu seç</h3>
      <div className="mk-umodlar" role="tablist" aria-label="Uno modları">
        {UNO_MOD_GRUPLAR.map((g) => (
          <div key={g.id} className="mk-umodlar-grup" role="presentation">
            <span className="mk-umodlar-ad">{g.ad}</span>
            <div className="mk-umodlar-sira">
              {UNO_MODLAR.filter((m) => m.grup === g.id).map((m) => (
                <button key={m.id} type="button" role="tab" aria-selected={mod === m.id} className={`mk-umod-cip${mod === m.id ? ' is-on' : ''}`} onClick={() => setMod(m.id)}>
                  <b>{m.ad}</b><small>{m.kisa}</small>
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div ref={sayfaRef} className="mk-umod-capa" />
      <ModSayfasi key={mod} mod={mod} tema={tema} />
    </article>
  );
}
