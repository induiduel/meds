/** Düz Okey kuralları. Metin motorla birebir: services/masa/motor/duzOkey.ts. */
import React from 'react';
import { Taslar, renkSec } from './ortak';

export default function DuzKurallar({ renkler }: { renkler?: string[] }) {
  const rk = renkSec(renkler);
  const ok = { s: 7, r: 0 as const };
  return (
    <article className="mk-kural" role="tabpanel">
      <p className="mk-kural-giris">Klasik okey. 2–4 oyuncu, 106 taş: 104 sayı taşı + 2 sahte okey. Herkese <b>14 taş</b>, eli başlatana 15 taş verilir. Amaç 14 taşının hepsini perlere ayırıp son taşını atarak <b>bitirmek</b>.</p>
      <h3>Gösterge, okey ve sahte okey</h3>
      <p>Göstergenin aynı renkteki bir üstü <b>okeydir</b> (13’ün üstü 1); okey jokerdir. <b>Sahte okey</b> okeyin sayısını ve rengini taşıyan sıradan taştır.</p>
      <div className="mk-ornekler">
        <Taslar rk={rk} t={[[6, 0]]} ad="Gösterge kırmızı 6 ise…" />
        <Taslar rk={rk} t={[[7, 0]]} ad="…okey kırmızı 7" okey={ok} />
      </div>
      <h3>Sıran gelince</h3>
      <ol>
        <li><b>Taş çek:</b> desteden ya da <b>yandan</b> (senden önceki oyuncunun son attığı taş). Eli başlatan ilk turda çekmez.</li>
        <li><b>Bir taş at.</b> Tur taş atınca biter. Yere per açılmaz, taş işlenmez.</li>
      </ol>
      <h3>Bitiş</h3>
      <p>14 taşının tamamı seri (aynı renk ardışık, en az 3; 12-13-1 olmaz) ve gruplara (aynı sayı farklı renk, 3–4) ya da <b>7 çifte</b> ayrılıyorsa son taşını atarak bitirirsin: gruplarını ıstakada boşlukla ayır, atacağın taşı seç ve <b>Bitir</b>’e bas. Okey eksik taşın yerine geçer.</p>
      <div className="mk-ornekler">
        <Taslar rk={rk} t={[[3, 2], [4, 2], [5, 2]]} ad="Seri" iyi />
        <Taslar rk={rk} t={[[9, 0], [9, 1], [9, 3]]} ad="Grup" iyi />
        <Taslar rk={rk} t={[[8, 1], [8, 1]]} ad="Çift (yalnız 7 çiftle bitişte)" iyi />
      </div>
      <h3>Gösterge göstermek</h3>
      <p>İlk turunda, taş atmadan önce göstergenin aynısı elindeyse <b>Gösterge göster</b>’e basabilirsin: diğer oyunculara birer kez −1 yazılır.</p>
      <h3>Puan</h3>
      <table className="mk-kural-tablo">
        <tbody>
          <tr><th scope="row">Eli bitiren</th><td>0</td></tr>
          <tr><th scope="row">Diğerleri</th><td className="is-eksi">−2</td></tr>
          <tr><th scope="row">Okey atarak ya da 7 çiftle bitince</th><td className="is-eksi">Diğerleri −4</td></tr>
          <tr><th scope="row">Okey atarak 7 çiftle bitince</th><td className="is-eksi">Diğerleri −8</td></tr>
          <tr><th scope="row">Gösterge</th><td className="is-eksi">Gösterilen herkese −1</td></tr>
          <tr><th scope="row">Deste biterse</th><td>El berabere biter (yalnız gösterge cezaları yazılır)</td></tr>
        </tbody>
      </table>
    </article>
  );
}
