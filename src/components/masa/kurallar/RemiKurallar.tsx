/** Remi kuralları. Metin motorla birebir: services/masa/motor/acikMasa.ts (remiMotor). */
import React from 'react';
import { ArrowDown, Layers, SkipForward } from 'lucide-react';
import { TasOrnek } from '../kabukOrtak';
import { Taslar, renkSec } from './ortak';
import { Akis, Kunye, TanitSatir, TasTanitim } from './gorsel';

export default function RemiKurallar({ renkler }: { renkler?: string[] }) {
  const rk = renkSec(renkler);
  return (
    <article className="mk-kural" role="tabpanel">
      <Kunye tur="remi" malzeme="106 taş: 104 + 2 joker" amac="elindeki taşları masaya dizip ilk bitiren olmak" />
      <p className="mk-kural-giris">2–4 oyuncu, 106 taş: 104 sayı taşı + 2 joker. Gösterge yoktur. Herkese <b>14 taş</b> dağıtılır. Taş atılmaz; elini <b>ilk bitiren</b> kazanır.</p>
      <h3>Taşları tanı</h3>
      <TasTanitim rk={rk} ek={
        <TanitSatir ad="Joker" alt="her taşın yerine geçer">
          <TasOrnek s={0} r={0} renkler={rk} boy={30} /><TasOrnek s={0} r={0} renkler={rk} boy={30} />
          <span className="mk-tanit-esit">= 106 taş</span>
        </TanitSatir>
      } />
      <h3>Joker</h3>
      <p>İki joker (yonca desenli taş) her taşın yerine geçer. Perde en az 2 gerçek taş bulunur.</p>
      <div className="mk-ornekler">
        <Taslar rk={rk} t={[[5, 2], [0, 0], [7, 2]]} ad="Joker 6’nın yerine: 5+6+7 = 18" iyi />
      </div>
      <h3>İlk açılış</h3>
      <p>İlk açılışı yalnız <b>elindeki taşlarla</b> yaparsın: açtığın perlerin sayı toplamı en az <b>30</b> olmalı (joker, yerine geçtiği taşın sayısıyla sayılır). Açılıştan önce masadaki taşlara dokunamazsın. Perlerini ıstakada boşlukla ayır; toplam rozette görünür, 30’a ulaşınca <b>Aç</b>’a bas.</p>
      <div className="mk-ornekler">
        <Taslar rk={rk} t={[[10, 0], [11, 0], [12, 0]]} ad="10+11+12 = 33: açılış olur" iyi />
        <Taslar rk={rk} t={[[3, 1], [4, 1], [5, 1]]} ad="3+4+5 = 12: tek başına yetmez" iyi={false} />
      </div>
      <h3>Sıran gelince</h3>
      <Akis adimlar={[
        { ikon: <Layers size={18} />, ad: 'Yere aç', metin: 'İlk açılış elinden en az 30 sayı; sonra masayı serbestçe yeniden diz.' },
        { ikon: <ArrowDown size={18} />, ad: 'Taş çek', metin: 'Açamıyorsan 1 taş çek; sıra geçer.', bag: 'yada' },
        { ikon: <SkipForward size={18} />, ad: 'Pas', metin: 'Açtıysan Pas ile sırayı geçir.' },
      ]} />
      <ul>
        <li><b>Ya yere açarsın ya taş çekersin.</b> Açamayan 1 taş çeker, sıra geçer. Açan o tur taş çekemez; istediği kadar koyduktan sonra <b>Pas</b> ile sırayı geçirir.</li>
        <li>Deste bitince çekilmez; açamıyorsan pas geçersin.</li>
      </ul>
      <h3>Masayı düzenleme</h3>
      <p>Açtıktan sonra masa serbesttir: masadaki taşları elindekilerle birleştirip yeni perler kurabilir, serileri bölebilir, taşların yerini değiştirebilirsin. Her hamlede elinden en az bir taş koyarsın; masadaki taşlar ele dönmez ve hamle bitince her per geçerli olmalıdır (seri: aynı renk ardışık, 12-13-1 olmaz; grup: aynı sayı farklı renk, 3–4 taş).</p>
      <h3>Bitiş ve puan</h3>
      <table className="mk-kural-tablo">
        <tbody>
          <tr><th scope="row">Son taşını koyup elini bitiren</th><td className="is-arti">Rakiplerin elde kalan toplamı kadar artı</td></tr>
          <tr><th scope="row">Diğerleri</th><td className="is-eksi">Elde kalan sayıların toplamı kadar eksi</td></tr>
          <tr><th scope="row">Elde kalan joker</th><td className="is-eksi">30 sayılır</td></tr>
          <tr><th scope="row">Kimse çekemiyor ve herkes art arda pas geçti</th><td>El kazanansız biter; herkes elindeki toplam kadar eksi alır</td></tr>
        </tbody>
      </table>
    </article>
  );
}
