import React from 'react';

/** Pişti kuralları (motor `services/masa/motor/pisti.ts` ile birebir) */
export default function PistiKurallar(_: { renkler?: string[] }) {
  return (
    <article className="mk-kural" role="tabpanel">
      <p className="mk-kural-giris">2 ya da 4 oyuncuyla, 52 kartlık iskambil destesiyle oynanır (♠ ♥ ♦ ♣; As, 2–10, Vale, Kız, Papaz). Dört kişide karşılıklı oturanlar ortaktır ve puanları birlikte sayılır. Amaç yerdeki kartları toplayıp <b>en çok puanı</b> almak.</p>
      <h3>Dağıtım</h3>
      <ul>
        <li>Yere 4 kart konur: 3’ü kapalı, en üstteki açık. Açık kart Vale çıkarsa yer kartları desteye karılır ve yeniden açılır.</li>
        <li>Herkese 4 kart dağıtılır. Bütün eller bitince desteden yeniden 4’er kart verilir; deste bitip son kartlar da oynanınca el biter.</li>
      </ul>
      <h3>Oynanış</h3>
      <ul>
        <li>Sıra gelen elinden bir kart atar.</li>
        <li>Attığın kart yerdeki en üst kartla <b>aynı değerdeyse</b> (7’ye 7, Papaz’a Papaz) yerdeki bütün kartları alırsın; kapalı kartlar da sana gelir.</li>
        <li><b>Vale</b> her kartı alır. Yer boşken atılan Vale ise yalnızca yere bırakılır.</li>
        <li>Yerde <b>tek kart</b> varken onu aynı değerdeki kartla alırsan <b>Pişti</b> yaparsın: 10 puan. Tek Vale’yi Vale ile alırsan pişti 20 puandır. Tek kartı (Vale olmayan) Vale ile almak pişti sayılmaz.</li>
        <li>El sonunda yerde kalan kartlar, yeri <b>en son alan</b> oyuncuya gider.</li>
      </ul>
      <h3>Puanlar</h3>
      <table className="mk-kural-tablo">
        <tbody>
          <tr><th scope="row">Her As</th><td className="is-arti">+1</td></tr>
          <tr><th scope="row">Her Vale</th><td className="is-arti">+1</td></tr>
          <tr><th scope="row">Sinek 2 (♣2)</th><td className="is-arti">+2</td></tr>
          <tr><th scope="row">Karo 10 (♦10)</th><td className="is-arti">+3</td></tr>
          <tr><th scope="row">En çok kartı alan (eşitlikte kimse almaz)</th><td className="is-arti">+3</td></tr>
          <tr><th scope="row">Pişti</th><td className="is-arti">+10</td></tr>
          <tr><th scope="row">Vale ile Vale piştisi</th><td className="is-arti">+20</td></tr>
        </tbody>
      </table>
      <p>El, en çok puanı toplayanın (dört kişide en çok puanı toplayan takımın) olur; eşitlikte iki taraf da kazanmış sayılır. Maç puanı ellerin toplamıdır.</p>
      <h3>Yardımcı</h3>
      <p>Normal modda sıra sendeyken <b>İpucu</b> hangi kartı neden atman gerektiğini söyler: pişti fırsatı varsa onu, yoksa eşleşen kartı; yer büyüdüyse Vale ile almayı; hiçbiri yoksa Vale’yi saklayıp en değersiz kartı atmayı önerir. Zorlu modda ipucu yoktur.</p>
      <p>Kartı oynamak için seçip yeniden dokun, yere dokun ya da sürükleyip yere bırak.</p>
    </article>
  );
}
