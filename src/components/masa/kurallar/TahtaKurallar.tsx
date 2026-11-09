import React from 'react';
import { GO_SURELER, XOX_HEDEF } from '../../../services/masa/tipler';

/** Go kuralları (motor `services/masa/motor/go.ts` ile birebir) */
export function GoKurallar() {
  return (
    <article className="mk-kural" role="tabpanel">
      <p className="mk-kural-giris">İki kişilik alan oyunu. Tahta 9×9, 13×13 ya da 19×19. Taşlar çizgilerin kesiştiği noktalara konur ve bir daha yer değiştirmez. Amaç tahtanın <b>daha büyük bölümünü</b> çevirmek.</p>
      <h3>Sıra ve taş koyma</h3>
      <ul>
        <li><b>Siyah başlar</b>; sırayla boş bir kesişime bir taş koyarsınız. Her elde renkler değişir.</li>
        <li>Telefonda önce noktaya dokunursun (yarı saydam taş çıkar), sonra <b>Onayla</b> ile koyarsın; aynı noktaya ikinci kez dokunmak da onaylar.</li>
        <li>Sıranı <b>pas</b> geçebilirsin.</li>
      </ul>
      <h3>Özgürlük ve taş alma</h3>
      <ul>
        <li>Yan yana (çaprazlar sayılmaz) aynı renk taşlar bir <b>grup</b>tur. Grubun bitişiğindeki boş noktalar onun <b>özgürlükleridir</b>.</li>
        <li>Koyduğun taş bir rakip grubun son özgürlüğünü kapatırsa o grup tahtadan alınır ve esir olur (kâsede sayılır).</li>
        <li><b>İntihar yasak:</b> taşın kendi grubunu özgürlüksüz bırakıyorsa, rakip taş almıyorsa konamaz.</li>
        <li><b>Ko:</b> tek taş alınan bir hamleden hemen sonra rakip aynı noktaya oynayıp geri alamaz; önce başka yere oynamalıdır (ko noktası küçük kareyle işaretlenir).</li>
        <li><b>Süperko:</b> tahtayı bu elde daha önce görülmüş bir dizilişe döndüren hamle de yasaktır.</li>
      </ul>
      <h3>Sayım</h3>
      <ul>
        <li>Art arda iki pas → <b>sayım</b>. Kurtulamayacak (ölü) grupların taşına dokunarak işaretlersiniz; her değişiklik onayları sıfırlar.</li>
        <li>İkiniz de onaylayınca el biter. Anlaşamazsanız <b>Oyuna dön</b> dersiniz, oyun sürer.</li>
        <li>Puan (alan usulü): tahtadaki diri taşların + yalnız kendi taşlarınla çevrili boş noktaların sayısı. Beyaza <b>komi</b> eklenir (varsayılan 6,5). Çok puanlı kazanır; teslim her an mümkündür.</li>
      </ul>
      <h3>Handikap ve süre</h3>
      <ul>
        <li><b>Handikap 2–9:</b> siyahın taşları yıldız noktalarına önceden konur ve <b>beyaz başlar</b>; komi 0,5 olur.</li>
        <li><b>Süre:</b> {GO_SURELER.filter((s) => s.ana).map((s) => s.ad).join(', ')}. Ana süre bitince byo-yomi başlar: her hamleyi aralık içinde yapmalısın, aşan hamle bir hak yer. Haklar biterse <b>süreyi aşan kaybeder</b>. Sayımda ve durdurulmuş oyunda saat işlemez.</li>
      </ul>
    </article>
  );
}

/** Çizgi Yarışı kuralları (motor `services/masa/motor/cizgi.ts` ile birebir) */
export function CizgiKurallar() {
  return (
    <article className="mk-kural" role="tabpanel">
      <p className="mk-kural-giris">İki kişilik zar yarışı. Kareli bir yolun iki ucunda iki kale var; çizgin kendi kalenden başlar. <b>Rakibin kale satırına ilk ulaşan</b> kazanır.</p>
      <h3>Modlar</h3>
      <ul>
        <li><b>32</b> kare (3 sütun, 2 yan hakkı) · <b>64</b> (5 sütun, 3 hak) · <b>96</b> (5 sütun, 4 hak) · <b>128</b> (7 sütun, 5 hak).</li>
        <li>İki çizgi de orta sütundan başlar.</li>
      </ul>
      <h3>Sıran gelince</h3>
      <ul>
        <li><b>Zar at</b> (1–6). Sonra adımlarını tek tek harcarsın: her adım çizgini bir kare öne uzatır. “Hepsi” düğmesi düz yol açıkken bütün adımları atar.</li>
        <li>Yan sütuna yalnız <b>önün rakip çizgisiyle kapalıyken</b> geçebilirsin; her yan geçiş bir adım ve bir yan hakkı yer.</li>
        <li>Yolun yoksa kalan adımlar yanar.</li>
      </ul>
      <h3>Kapışma</h3>
      <ul>
        <li>İki baş aynı sütunda yüz yüze geldiğinde ve en az biri kendi yarısını geçmişse <b>kapışma</b> olur: sıradaki zar atınca iki zar birden atılır.</li>
        <li>Büyük atan <b>farkı kadar ilerler</b>, küçük atan farkı kadar <b>geriler</b> (çizgisi baştan kısalır). Eşitlikte bir şey olmaz.</li>
        <li>Yalnız kale hücresi kalmış oyuncu kapışmayı yine kaybederse kalesi alınır ve el biter.</li>
        <li>Tam orta çizgide (ikiniz de kendi yarınızdayken) yüz yüze gelmek kapışma değildir: önü kapanan yana geçmelidir.</li>
      </ul>
      <p>Ekranda son dört turun çizgisi parlak, eskiler soluk görünür; geri çekilen kısım kısa bir süre kesik çizgiyle kalır.</p>
    </article>
  );
}

/** XOX kuralları (motor `services/masa/motor/xox.ts` ile birebir) */
export function XoxKurallar() {
  return (
    <article className="mk-kural" role="tabpanel">
      <p className="mk-kural-giris">İki kişilik dizi oyunu. Sırayla boş kareye işaret koyarsınız; <b>yan yana dizi</b> tamamlayan kazanır.</p>
      <ul>
        <li><b>X başlar</b>; her elde başlayan değişir (başlayan hep X’tir).</li>
        <li>Tahta ve gereken dizi: {([3, 4, 5, 6] as const).map((n) => `${n}×${n} → ${XOX_HEDEF[n]}`).join(' · ')}.</li>
        <li>Yatay, dikey ve iki çapraz yön sayılır.</li>
        <li>Tahta dolar ve dizi çıkmazsa el berabere biter. Kazanan 1 puan alır.</li>
      </ul>
    </article>
  );
}
