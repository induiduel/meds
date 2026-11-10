import React from 'react';
import { CircleDot, Dices, Footprints, Scale, SkipForward, Swords } from 'lucide-react';
import { Akis, CizgiSema, GoLejant, GoSema, Kunye, XoxSema, Zar } from './gorsel';
import { GO_SURELER, XOX_HEDEF } from '../../../services/masa/tipler';

/** Go kuralları (motor `services/masa/motor/go.ts` ile birebir) */
export function GoKurallar() {
  return (
    <article className="mk-kural" role="tabpanel">
      <Kunye tur="go" malzeme="Tahta, siyah ve beyaz taşlar" amac="tahtanın daha büyük bölümünü çevirmek" />
      <p className="mk-kural-giris">İki kişilik alan oyunu. Tahta 9×9, 13×13 ya da 19×19. Taşlar çizgilerin kesiştiği noktalara konur ve bir daha yer değiştirmez. Amaç tahtanın <b>daha büyük bölümünü</b> çevirmek.</p>
      <Akis adimlar={[
        { ikon: <CircleDot size={18} />, ad: 'Taş koy', metin: 'Boş bir kesişime bir taş koy; taş bir daha yer değiştirmez.' },
        { ikon: <SkipForward size={18} />, ad: 'Pas geç', metin: 'Kazançlı hamle kalmadıysa sıranı geç.', bag: 'yada' },
        { ikon: <Scale size={18} />, ad: 'Sayım', metin: 'Art arda iki pas olunca ölü taşlar işaretlenir, alanlar sayılır.' },
      ]} />
      <h3>Sıra ve taş koyma</h3>
      <ul>
        <li><b>Siyah başlar</b>; sırayla boş bir kesişime bir taş koyarsınız. Her elde renkler değişir.</li>
        <li>Telefonda önce noktaya dokunursun (yarı saydam taş çıkar), sonra <b>Onayla</b> ile koyarsın; aynı noktaya ikinci kez dokunmak da onaylar.</li>
        <li>Sıranı <b>pas</b> geçebilirsin.</li>
      </ul>
      <h3>Özgürlük ve taş alma</h3>
      <GoLejant />
      <div className="mk-ornekler">
        <GoSema taslar={[[2, 2, 'S']]} isaret={[[2, 1, 'o'], [1, 2, 'o'], [3, 2, 'o'], [2, 3, 'o']]} ad="Tek taşın 4 özgürlüğü var: yanındaki boş noktalar (çaprazlar sayılmaz)" />
        <GoSema taslar={[[2, 2, 'S'], [3, 2, 'S']]} isaret={[[2, 1, 'o'], [3, 1, 'o'], [1, 2, 'o'], [4, 2, 'o'], [2, 3, 'o'], [3, 3, 'o']]} ad="Yan yana taşlar gruptur; özgürlükleri ortaktır (6)" />
        <GoSema taslar={[[2, 2, 'B'], [2, 1, 'S'], [1, 2, 'S'], [2, 3, 'S']]} isaret={[[3, 2, 'h']]} ad="Beyazın tek özgürlüğü kaldı: siyah oraya koyarsa…" />
        <GoSema taslar={[[2, 2, 'B', true], [2, 1, 'S'], [1, 2, 'S'], [2, 3, 'S'], [3, 2, 'S']]} ad="…beyaz taş tahtadan alınır, siyahın esiri olur" iyi />
        <GoSema taslar={[[2, 1, 'B'], [1, 2, 'B'], [3, 2, 'B'], [2, 3, 'B']]} isaret={[[2, 2, 'x']]} ad="İntihar: siyah buraya koyamaz (özgürlüğü olmaz, taş da almaz)" iyi={false} />
        <GoSema taslar={[[2, 1, 'S'], [1, 2, 'S'], [2, 3, 'S'], [3, 2, 'S'], [3, 1, 'B'], [4, 2, 'B'], [3, 3, 'B']]} isaret={[[2, 2, 'ko']]} ad="Ko: siyah kareli noktadaki tek taşı aldı; beyaz hemen oraya oynayıp geri alamaz" iyi={false} />
      </div>
      <ul>
        <li>Yan yana (çaprazlar sayılmaz) aynı renk taşlar bir <b>grup</b>tur. Grubun bitişiğindeki boş noktalar onun <b>özgürlükleridir</b>.</li>
        <li>Koyduğun taş bir rakip grubun son özgürlüğünü kapatırsa o grup tahtadan alınır ve esir olur (kâsede sayılır).</li>
        <li><b>İntihar yasak:</b> taşın kendi grubunu özgürlüksüz bırakıyorsa, rakip taş almıyorsa konamaz.</li>
        <li><b>Ko:</b> tek taş alınan bir hamleden hemen sonra rakip aynı noktaya oynayıp geri alamaz; önce başka yere oynamalıdır (ko noktası küçük kareyle işaretlenir).</li>
        <li><b>Süperko:</b> tahtayı bu elde daha önce görülmüş bir dizilişe döndüren hamle de yasaktır.</li>
      </ul>
      <h3>Sayım</h3>
      <div className="mk-ornekler">
        <GoSema
          taslar={[0, 1, 2, 3, 4].flatMap((y): [number, number, 'S' | 'B'][] => [[2, y, 'S'], [3, y, 'B']])}
          isaret={[0, 1, 2, 3, 4].flatMap((y): [number, number, 'aS' | 'aB'][] => [[0, y, 'aS'], [1, y, 'aS'], [4, y, 'aB']])}
          ad="Siyah: 5 taş + 10 nokta = 15. Beyaz: 5 taş + 5 nokta = 10, üstüne komi"
        />
      </div>
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
      <Kunye tur="cizgi" malzeme="Kareli yol, bir zar" amac="rakibin kale satırına ilk ulaşmak" />
      <p className="mk-kural-giris">İki kişilik zar yarışı. Kareli bir yolun iki ucunda iki kale var; çizgin kendi kalenden başlar. <b>Rakibin kale satırına ilk ulaşan</b> kazanır.</p>
      <Akis adimlar={[
        { ikon: <Dices size={18} />, ad: 'Zar at', metin: '1–6 arası adım kazanırsın.' },
        { ikon: <Footprints size={18} />, ad: 'İlerle', metin: 'Her adım çizgini bir kare öne uzatır; önün kapalıysa yana geç.' },
        { ikon: <Swords size={18} />, ad: 'Kapışma', metin: 'Rakip sahada yüz yüze gelince iki zar atılır; büyük atan ilerler.' },
      ]} />
      <div className="mk-ornekler">
        <CizgiSema
          kirmizi={[[1, 9], [1, 8], [1, 7]]} mavi={[[1, 0], [1, 1], [1, 2]]} plan={{ renk: 'k', yol: [[1, 7], [1, 6], [1, 5], [1, 4]] }}
          zarlar={<><Zar n={3} renk="#e4572e" /><span>3 adım</span></>}
          ad="Zar 3: kırmızı çizgi üç kare ilerler. Renkli satırlar kaleler, kesik çizgi orta çizgi"
        />
        <CizgiSema
          kirmizi={[[1, 9], [1, 8], [1, 7], [1, 6], [1, 5]]} mavi={[[1, 0], [1, 1], [1, 2], [1, 3], [1, 4]]} plan={{ renk: 'k', yol: [[1, 5], [2, 5], [2, 4]] }}
          zarlar={<span>yan hak<br />−1</span>}
          ad="Orta çizgide yüz yüze: kapışma olmaz. Önü kapanan yan sütuna geçer"
        />
        <CizgiSema
          kirmizi={[[1, 9], [1, 8], [1, 7], [1, 6], [1, 5], [1, 4], [1, 3]]} mavi={[[1, 0], [1, 1], [1, 2]]}
          zarlar={<><span className="mk-cizgi-zarlar"><Zar n={5} renk="#e4572e" /><Zar n={3} renk="#2563eb" /></span><span>fark 2</span></>}
          ad="Kırmızı rakip sahada, yüz yüze: kapışma. 5’e 3: kırmızı 2 ilerler, mavi 2 geriler"
        />
      </div>
      <h3>Modlar</h3>
      <ul>
        <li><b>32</b> kare (3 sütun, 2 yan hakkı) · <b>64</b> (5 sütun, 3 hak) · <b>96</b> (5 sütun, 4 hak) · <b>128</b> (7 sütun, 5 hak).</li>
        <li>İki çizgi de orta sütundan başlar.</li>
        <li><b>Klasik</b>: yukarıdaki kurallar. <b>Eğlenceli</b>: aynı kurallar + pistte özel kareler (aşağıda).</li>
      </ul>
      <h3>Eğlenceli mod: özel kareler</h3>
      <ul>
        <li>Kareler iki oyuncu için ayna simetrik dağıtılır; çizginin başı bir kareye basınca kare etkisini gösterip kaybolur.</li>
        <li><b>⏩ İleri</b>: bu tura 3 adım eklenir. <b>↔ Yan</b>: 1 yan hakkı kazanırsın. <b>🎲 Zar</b>: tur bitince yeniden zar atarsın.</li>
        <li><b>💥 Tuzak</b>: çizgin 2 kare geri çekilir (kale kalır) ve turun biter.</li>
        <li>Önündeki tuzağı görüp yana geçmek mümkün değil (yan geçiş yalnız önün rakiple kapalıyken); ama hangi sütunda olduğun önemlidir. Kapışmada basılan kareler etkisizdir.</li>
      </ul>
      <h3>Sıran gelince</h3>
      <ul>
        <li><b>Zar at</b> (1–6). Çizgin zar kadar kare öne uzar. “Otomatik ilerle” açıkken bu kendiliğinden olur ve yalnız yana geçmen gerektiğinde durur; kapalıyken adımları tek tek ya da “Hepsi” ile atarsın.</li>
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
      <Kunye tur="xox" malzeme="Kareli tahta, X ve O" amac="işaretlerini yan yana dizmek" />
      <p className="mk-kural-giris">İki kişilik dizi oyunu. Sırayla boş kareye işaret koyarsınız; <b>yan yana dizi</b> tamamlayan kazanır.</p>
      <ul>
        <li><b>X başlar</b>; her elde başlayan değişir (başlayan hep X’tir).</li>
        <li>Tahta ve gereken dizi: {([3, 4, 5, 6] as const).map((n) => `${n}×${n} → ${XOX_HEDEF[n]}`).join(' · ')}.</li>
        <li>Yatay, dikey ve iki çapraz yön sayılır.</li>
        <li>Tahta dolar ve dizi çıkmazsa el berabere biter. Kazanan 1 puan alır.</li>
      </ul>
      <div className="mk-ornekler">
        <XoxSema satirlar={['X.O', '.XO', '..X']} dizi={[[0, 0], [2, 2]]} ad="3×3: çapraz üçlü, X kazanır" iyi />
        <XoxSema satirlar={['O....', '.XXXX', '.O...', '..O..', '.....']} dizi={[[1, 1], [1, 4]]} ad="5×5: dört işaret yan yana yeter" iyi />
        <XoxSema satirlar={['XOX', 'XOO', 'OXX']} ad="Tahta doldu, dizi yok: berabere" iyi={false} />
      </div>
    </article>
  );
}
