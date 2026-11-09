/** Kastet kuralları. Metin motorla birebir: services/masa/motor/acikMasa.ts (kastetMotor). */
import React from 'react';
import { Taslar, renkSec } from './ortak';

export default function KastetKurallar({ renkler }: { renkler?: string[] }) {
  const rk = renkSec(renkler);
  const ok = { s: 7, r: 0 as const };
  return (
    <article className="mk-kural" role="tabpanel">
      <p className="mk-kural-giris">2–4 oyuncu, 106 taş: 104 sayı taşı + 2 sahte okey. Herkese <b>14 taş</b> dağıtılır. Taş atılmaz; amaç bütün taşlarını yere açıp elini <b>ilk bitiren</b> olmak.</p>
      <h3>Gösterge, okey ve sahte okey</h3>
      <p>Dağıtımda bir taş açılır: <b>gösterge</b>. Göstergenin aynı renkteki bir üstü <b>okeydir</b> (13’ün üstü 1). Okey jokerdir, her taşın yerine geçer. <b>Sahte okey</b> joker değildir; okeyin sayısını ve rengini taşıyan sıradan bir taştır.</p>
      <div className="mk-ornekler">
        <Taslar rk={rk} t={[[6, 0]]} ad="Gösterge kırmızı 6 ise…" />
        <Taslar rk={rk} t={[[7, 0]]} ad="…okey kırmızı 7’dir" okey={ok} />
        <Taslar rk={rk} t={[[0, 0]]} ad="Sahte okey: kırmızı 7" okey={ok} />
      </div>
      <h3>Sıran gelince</h3>
      <ul>
        <li><b>Ya yere açarsın ya taş çekersin.</b> Taş çeken o tur açamaz; çekince sıra kendiliğinden geçer. Açan o tur taş çekemez; istediği kadar açtıktan sonra <b>Pas</b> ile sırayı geçirir.</li>
        <li>Elinde en çok <b>22 taş</b> tutabilirsin. 22 taştaysan çekemezsin: aç ya da pas geç.</li>
        <li>Deste bitince taş çekilmez; açamıyorsan pas geçersin.</li>
      </ul>
      <h3>Perler</h3>
      <p>Seri aynı renkte ardışık sayılardır (1 yalnız başta; 12-13-1 olmaz), grup aynı sayının farklı renkleridir (3–4 taş). Her per en az 3 taştır ve içinde en az 2 gerçek taş bulunur.</p>
      <h3>Masa herkesin</h3>
      <p>Yere açılan taşlar ortak maldır. Masadaki taşları elindekilerle birleştirip yeni perler kurabilir, serileri bozmadan taşların yerini değiştirebilirsin. Her hamlede elinden en az bir taş koymalısın; masadaki hiçbir taş ele dönmez ve hamle bitince masadaki her per geçerli olmalıdır.</p>
      <div className="mk-ornekler">
        <Taslar rk={rk} t={[[5, 1], [6, 1], [7, 1], [8, 1]]} ad="Yerde siyah 5-6-7-8…" />
        <Taslar rk={rk} t={[[5, 1], [5, 0], [5, 2]]} ad="…elindeki kırmızı ve mavi 5’le siyah 5’i alıp grup kur; yerde 6-7-8 kalır" iyi />
        <Taslar rk={rk} t={[[7, 1], [8, 1], [9, 1]]} ad="Yerde 5-6-7-8-9, elinde siyah 7: 5-6-7 ve 7-8-9 olur" iyi />
      </div>
      <h3>Seri alanı ve çift alanı</h3>
      <p>Masada en çok <b>26 seri alanı</b> (seri ya da grup) vardır. 26 alan dolmadan çift açılamaz. Dolunca elindeki özdeş çiftleri (sayısı ve rengi aynı iki taş) ayrı <b>çift alanına</b> açarsın. Çift alanındaki taşların yeri değiştirilmez, onlara taş eklenmez.</p>
      <h3>Bitiş ve puan</h3>
      <p>Bütün taşlarını yere açtığında elin boşalır; el boşken <b>Pas</b>’a basınca el biter.</p>
      <table className="mk-kural-tablo">
        <tbody>
          <tr><th scope="row">Eli bitiren</th><td className="is-arti">+50</td></tr>
          <tr><th scope="row">Diğerleri</th><td className="is-eksi">Elde kalan sayıların toplamı kadar eksi</td></tr>
          <tr><th scope="row">Elde kalan okey</th><td className="is-eksi">25 sayılır (sahte okey: okeyin sayısı)</td></tr>
          <tr><th scope="row">Kimse çekemiyor ve herkes art arda pas geçti</th><td>El kazanansız biter; herkes elindeki toplam kadar eksi alır</td></tr>
        </tbody>
      </table>
    </article>
  );
}
