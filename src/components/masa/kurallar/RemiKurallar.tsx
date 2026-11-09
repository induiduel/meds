/** Remi kuralları. Metin motorla birebir: services/masa/motor/acikMasa.ts (remiMotor). */
import React from 'react';
import { Taslar, renkSec } from './ortak';

export default function RemiKurallar({ renkler }: { renkler?: string[] }) {
  const rk = renkSec(renkler);
  return (
    <article className="mk-kural" role="tabpanel">
      <p className="mk-kural-giris">2–4 oyuncu, 106 taş: 104 sayı taşı + 2 joker. Gösterge yoktur. Herkese <b>14 taş</b> dağıtılır. Taş atılmaz; elini <b>ilk bitiren</b> kazanır.</p>
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
