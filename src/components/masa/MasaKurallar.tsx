/**
 * Kurallar (sekmeli). Metin motorlarla birebir: motor/yedili.ts, yuzbir.ts (+ yuzbirAsistan.ts), uno.ts (+ unoAsistan.ts).
 * Kural değişirse önce motor, sonra bu sayfa güncellenir.
 */
import React, { useState } from 'react';
import { Check, X } from 'lucide-react';
import { OYUN_ADI, VARSAYILAN_RENKLER, type OyunTur, type UnoDeger, type UnoRenk } from '../../services/masa/tipler';
import { CEZA_BILGI, KartOrnek, TasOrnek } from './kabukOrtak';
import DuzKurallar from './kurallar/DuzKurallar';
import KastetKurallar from './kurallar/KastetKurallar';
import RemiKurallar from './kurallar/RemiKurallar';
import PistiKurallar from './kurallar/PistiKurallar';
import DominoKurallar from './kurallar/DominoKurallar';
import { CizgiKurallar, GoKurallar, XoxKurallar } from './kurallar/TahtaKurallar';

export type KuralSekme = OyunTur | 'ceza' | 'ipucu';
const SEKMELER: [KuralSekme, string][] = [['yedili', OYUN_ADI.yedili], ['takim', OYUN_ADI.takim], ['yuzbir', OYUN_ADI.yuzbir], ['duz', OYUN_ADI.duz], ['kastet', OYUN_ADI.kastet], ['remi', OYUN_ADI.remi], ['domino', OYUN_ADI.domino], ['uno', OYUN_ADI.uno], ['pisti', OYUN_ADI.pisti], ['go', OYUN_ADI.go], ['cizgi', OYUN_ADI.cizgi], ['xox', OYUN_ADI.xox], ['ceza', 'Cezalar ve puan'], ['ipucu', 'Masa ve ipuçları']];

type T = [number, 0 | 1 | 2 | 3];
type K = [UnoRenk | null, UnoDeger];

export default function MasaKurallar({ ilk = 'yedili', renkler }: { ilk?: KuralSekme; renkler?: string[] }) {
  const [sekme, setSekme] = useState<KuralSekme>(ilk);
  const rk = renkler && renkler.length === 4 ? renkler : [...VARSAYILAN_RENKLER];

  const Taslar = ({ t, ad, iyi, okey }: { t: T[]; ad: string; iyi?: boolean; okey?: { s: number; r: 0 | 1 | 2 | 3 } }) => (
    <figure className={`mk-ornek${iyi === false ? ' is-kotu' : iyi ? ' is-iyi' : ''}`}>
      <div className="mk-ornek-sira">{t.map(([s, r], i) => <TasOrnek key={i} s={s} r={r} renkler={rk} boy={30} okey={okey} />)}</div>
      <figcaption>{iyi !== undefined && (iyi ? <Check size={15} /> : <X size={15} />)} {ad}</figcaption>
    </figure>
  );
  const Kartlar = ({ k, ad, iyi }: { k: K[]; ad: string; iyi?: boolean }) => (
    <figure className={`mk-ornek${iyi === false ? ' is-kotu' : iyi ? ' is-iyi' : ''}`}>
      <div className="mk-ornek-sira is-kart">{k.map(([renk, deger], i) => <KartOrnek key={i} renk={renk} deger={deger} boy={40} />)}</div>
      <figcaption>{iyi !== undefined && (iyi ? <Check size={15} /> : <X size={15} />)} {ad}</figcaption>
    </figure>
  );
  const PerOrnekleri = () => (
    <div className="mk-ornekler">
      <Taslar t={[[5, 2], [6, 2], [7, 2]]} ad="Seri: aynı renk, ardışık sayılar" iyi />
      <Taslar t={[[9, 0], [9, 1], [9, 3]]} ad="Grup: aynı sayı, farklı renkler" iyi />
      <Taslar t={[[1, 0], [2, 0], [3, 0]]} ad="1 yalnız serinin başında durur" iyi />
      <Taslar t={[[12, 1], [13, 1], [1, 1]]} ad="12-13-1 olmaz" iyi={false} />
      <Taslar t={[[4, 0], [4, 0], [4, 2]]} ad="Grupta aynı renk iki kez olmaz" iyi={false} />
    </div>
  );

  return (
    <div className="mk-kurallar">
      <div className="mk-kural-sekmeler" role="tablist" aria-label="Kural bölümleri">
        {SEKMELER.map(([k, ad]) => <button key={k} type="button" role="tab" aria-selected={sekme === k} className={sekme === k ? 'is-on' : ''} onClick={() => setSekme(k)}>{ad}</button>)}
      </div>

      {sekme === 'yedili' && (
        <article className="mk-kural" role="tabpanel">
          <p className="mk-kural-giris">Ana oyun. 2–6 oyuncu, 104 taş (1’den 13’e, dört renk, her taştan iki tane). Joker yok. Herkese <b>7 taş</b> dağıtılır; amaç elindeki taşları masaya eritip <b>elini ilk bitiren</b> olmak.</p>
          <h3>Per nedir</h3>
          <p>Per, en az 3 taşlık geçerli dizidir. İki türü var:</p>
          <PerOrnekleri />
          <ul>
            <li><b>Seri:</b> aynı renkten ardışık sayılar; 3 taştan 13 taşa kadar uzayabilir.</li>
            <li><b>Grup:</b> aynı sayının farklı renkleri; 3 ya da 4 taş.</li>
          </ul>
          <h3>Sıran gelince</h3>
          <ol>
            <li><b>Per aç:</b> elinde per varsa masaya açarsın. Bir turda birden çok per açabilirsin.</li>
            <li><b>Taş işle:</b> per açtıktan sonra masadaki <em>her</em> pere (senin ya da rakibin) taş ekleyebilirsin: serinin iki ucuna sıradaki sayı, üçlü gruba eksik dördüncü renk.</li>
            <li><b>Yapacak hamlen yoksa</b> desteden 1 taş çekersin. Çektiğin taşla per açılıyor ya da taş işleniyorsa oynarsın; olmuyorsa eli devredersin.</li>
            <li><b>Hamle yaptıysan</b> ve yapacak başka şey kalmadıysa taş çekmeden eli devredersin. Hamle yaptıktan sonra taş çekilmez; bir turda en çok 1 taş çekilir.</li>
          </ol>
          <div className="mk-ornekler">
            <Taslar t={[[4, 2], [5, 2], [6, 2], [7, 2], [8, 2]]} ad="5-6-7 serisine 4 baştan, 8 sondan işlenir" iyi />
            <Taslar t={[[9, 0], [9, 1], [9, 2], [9, 3]]} ad="Üçlü gruba dördüncü renk işlenir" iyi />
          </div>
          <h3>Masayı düzenleme</h3>
          <p>Masadaki perler dokunulmaz değildir. Per açtıktan sonra sıran gelince <b>Masayı düzenle</b> ile perlerin yerini değiştirebilir, taşları perler arasında yeniden dizebilirsin: örneğin 3-4-5-6 kırmızı serinin 6’sını 6’lı gruba taşıyıp dörtlü grup yaparsın. Kurallar:</p>
          <ul>
            <li>Masadaki taşların <b>hepsi masada kalır</b>; hiçbir taş ele geri alınamaz, düzenleme sırasında elden taş eklenmez.</li>
            <li>Onayladığında her per yine geçerli olmalıdır (en az 3 taşlık seri ya da grup).</li>
            <li>Düzenleme taş eritmez: ardından elindeki taşları yeni duruma göre işleyebilir ya da per açabilirsin.</li>
          </ul>
          <h3>Geri al</h3>
          <p>Kendi sırandaki per açma, taş işleme ve masa düzenleme hamlelerini <b>Geri al</b> ile tek tek geri alabilirsin; ıstakadaki taş yer değiştirmelerin de geri alınır. Taş çekme, eli devretme ve hediye taş verdiren hamle geri alınmaz (gizli taş açılmıştır).</p>
          <h3>Normal ve zorlu mod</h3>
          <ul>
            <li><b>Normal mod:</b> ipucu, otomatik işleme, en iyi hamle, ıstakayı sıralama ve masayı dizme yardımcıları açıktır.</li>
            <li><b>Zorlu mod:</b> yardımcıların hiçbiri yoktur; ıstakayı ve masayı otomatik dizemezsin, taşlarını elle yerleştirirsin. Masadaki perler yalnız <b>el bitince</b> kendiliğinden dizilir. Masayı düzenleme ve geri al her iki modda da vardır.</li>
          </ul>
          <h3>Seriyi bölerek işleme</h3>
          <p>Masadaki bir serinin <b>ortasındaki</b> bir sayının eş taşı (aynı renk, aynı sayı) elindeyse onu da o seriye işleyebilirsin: seri o taştan <b>ikiye bölünür</b>. Bölünen iki parçanın ikisi de en az 3 taş olmalıdır; bu yüzden en az 5 taşlık serilerde ve uçlardan en az üçüncü sıradaki sayılarda olur.</p>
          <div className="mk-ornekler">
            <Taslar t={[[3, 2], [4, 2], [5, 2], [6, 2], [7, 2]]} ad="Masada 3-4-5-6-7 var, elinde ikinci 5" />
            <Taslar t={[[3, 2], [4, 2], [5, 2]]} ad="Bölününce: 3-4-5…" iyi />
            <Taslar t={[[5, 2], [6, 2], [7, 2]]} ad="…ve 5-6-7" iyi />
            <Taslar t={[[3, 2], [4, 2], [5, 2], [6, 2]]} ad="3-4-5-6’ya ikinci 5 işlenmez: 5-6 iki taş kalır" iyi={false} />
          </div>
          <p>Böyle bir taş da <b>işlek</b> sayılır: bölerek işleyebilecekken taş çekmek ya da eli devretmek “İşlek taşı işlemedi” cezasıdır.</p>
          <h3>Zorunluluk ve ceza</h3>
          <p>Elinde açılabilecek bir per ya da (per açtıysan) masaya işlenebilecek bir taş varken <b>taş çekmek ya da eli devretmek cezadır</b>. Kaçırdığın her zorunluluk ayrı yazılır:</p>
          <ul className="mk-kural-cezalar">
            <li><i className="mk-ceza-rozet is-islek">İşlek taşı işlemedi</i> <b>−5</b></li>
            <li><i className="mk-ceza-rozet is-per">Açabileceği peri bekletti</i> <b>−5</b></li>
          </ul>
          <p>Ceza yazılınca ayrıca desteden 1 ceza taşı çekersin ve sıra hemen geçer. İkisi aynı anda kaçarsa −10 alırsın. Henüz per açmadıysan işleme zorunluluğun yoktur; yalnız per açma zorunluluğun vardır.</p>
          <h3>Elin bitişi ve puan</h3>
          <ul>
            <li>Son taşını eriten <b>eli kazanır</b> ve 0 alır; diğerleri <b>elinde kalan taş sayısı kadar eksi</b> alır (5 taş = −5).</li>
            <li>El içinde yazılan cezalar kazanan dahil herkesin puanından düşer.</li>
            <li><b>Berabere:</b> yığın bittikten sonra herkes art arda hiçbir taş eritemeden turunu geçerse kimse oynayamıyor demektir: el kazanansız biter, herkes kalan taşı kadar eksi alır. Yedili’de bu sık olur.</li>
            <li>Deste boşken “taş çek” yine sıranı ilerletir: taş gelmez, eli devredersin.</li>
            <li>Maç, lobide seçilen el sayısı kadar sürer; toplam puanı en yüksek olan kazanır.</li>
          </ul>
        </article>
      )}

      {sekme === 'takim' && (
        <article className="mk-kural" role="tabpanel">
          <p className="mk-kural-giris">Yedili Okey’in eşli hâli. Takımlar eşit sayıda olur (1–1, 2–2 ya da 3–3); A ve B oyuncuları masada <b>sırayla, ortaklar karşılıklı</b> oturur. Taşlar, perler, seriyi bölerek işleme, masayı düzenleme, geri al, zorunluluk ve −5’lik cezalar Yedili Okey ile aynıdır. Farklar:</p>
          <h3>Kişi başı taş</h3>
          <ul>
            <li><b>2–4 oyuncu</b> (1–1, 2–2): kurucu lobide <b>7 ya da 14 taş</b> seçer. 14 taşla eller uzun sürer, takım açılışı ve işleme fırsatı artar; 4 oyuncuda destede 48 taş kalır.</li>
            <li><b>5–6 oyuncu</b> (3–3): herkese <b>4 taş</b> dağıtılır, destede 80 taş kalır. Elde per açacak taş azdır; çoğu tur taş çekerek geçer, ortağın açması takım için daha da değerlidir.</li>
            <li>Ceza puanları değişmez: kaybeden kalan taşı kadar eksi alır (14 taşlı ellerde eksiler doğal olarak büyür).</li>
          </ul>
          <h3>Takım açılışı ortaktır</h3>
          <p>Takımdan biri per açtığında <b>ortağı da masadaki perlere taş işleyebilir</b>; kendi peri olmasa bile. Bu yüzden işleme zorunluluğu da ortağın açmasıyla başlar: ortağın açtıysa ve elinde işlek taş varsa, çekmek ya da devretmek ceza getirir.</p>
          <h3>Hediye taş</h3>
          <p>Bir grup <b>4 taşa tamamlanınca</b> (üçlüye dördüncü renk işlenince ya da dörtlü grup açılınca) rakip takımın her oyuncusu desteden 1 “hediye taş” çeker. Deste biterse hediye verilmez.</p>
          <div className="mk-ornekler"><Taslar t={[[7, 0], [7, 1], [7, 2], [7, 3]]} ad="Dörtlenen grup: rakiplere birer hediye taş" iyi /></div>
          <h3>Bitiş ve puan</h3>
          <ul>
            <li>Takımdan biri elini bitirince <b>takım kazanır</b>.</li>
            <li>Kazanan takımda elinde taş kalan ortağın taşları <b>sayılmaz</b> (0 alır).</li>
            <li>Kaybeden takımın her oyuncusu kalan taşı kadar eksi alır.</li>
            <li>Cezalar kazanan takım dahil kişiye yazılır. Maç sıralaması takım toplamına göredir.</li>
          </ul>
        </article>
      )}

      {sekme === 'yuzbir' && (
        <article className="mk-kural" role="tabpanel">
          <p className="mk-kural-giris">2–4 oyuncu, 106 taş: 104 sayı taşı + 2 sahte okey. Herkese <b>21 taş</b>, eli başlatana 22 taş verilir. Amaç perlerini açıp taşlarını eritmek ve <b>son taşını yere atarak</b> bitirmek.</p>
          <h3>Gösterge, okey ve sahte okey</h3>
          <p>Dağıtımda bir taş açılır: <b>gösterge</b>. Göstergenin aynı renkteki bir üstü o elin <b>okeyidir</b> (13’ün üstü 1). Okey jokerdir: her taşın yerine geçer. <b>Sahte okey</b> joker değildir; okey taşının kendi sayısını ve rengini taşır.</p>
          <div className="mk-ornekler">
            <Taslar t={[[6, 0]]} ad="Gösterge kırmızı 6 ise…" />
            <Taslar t={[[7, 0]]} ad="…okey kırmızı 7’dir (joker)" okey={{ s: 7, r: 0 }} />
            <Taslar t={[[0, 0]]} ad="Sahte okey: kırmızı 7 sayılır" okey={{ s: 7, r: 0 }} />
          </div>
          <h3>Sıran gelince</h3>
          <ol>
            <li><b>Taş çek:</b> desteden ya da <b>yandan</b> (senden önceki oyuncunun son attığı taş). Eli başlatan ilk turda çekmez.</li>
            <li>Yandan aldığın taşı <b>o tur kullanmak zorundasın</b> (açtığın bir perde ya da işleyerek). Kullanamıyorsan taşı geri koyar, desteden çekersin; cezası yoktur. Geri koymadan taş atamazsın.</li>
            <li>İstersen aç, işle, ek per aç.</li>
            <li><b>Bir taş at.</b> Tur taş atınca biter. Her hamleden sonra elinde atacak en az 1 taş kalmalıdır.</li>
          </ol>
          <h3>Açılış</h3>
          <p>İlk açılış tek hamlede yapılır ve iki yolu vardır; ikisi karıştırılmaz:</p>
          <ul>
            <li><b>101 ile:</b> seri ve gruplarının taş sayıları toplamı en az 101 olmalı. Okey, yerine geçtiği taşın değeriyle sayılır.</li>
            <li><b>Çiftle:</b> en az 5 çift. Çift, sayısı ve rengi özdeş iki taştır (okey bir taşın eşi olabilir).</li>
          </ul>
          <div className="mk-ornekler">
            <Taslar t={[[10, 1], [11, 1], [12, 1], [13, 1]]} ad="Seri: 10+11+12+13 = 46" iyi />
            <Taslar t={[[11, 0], [11, 2], [11, 3]]} ad="Grup: 33" iyi />
            <Taslar t={[[8, 2], [8, 2]]} ad="Çift: özdeş iki taş" iyi />
          </div>
          <ul>
            <li>Seri aynı renk ardışıktır (1 yalnız başta; 12-13-1 olmaz), grup aynı sayının farklı renkleridir (3–4 taş). Her perde en az 2 gerçek taş bulunur.</li>
            <li>Seri/grupla açan sonradan yalnız seri/grup, çiftle açan yalnız yeni çift açabilir.</li>
            <li><b>İşleme:</b> açtıktan sonra masadaki serilerin uçlarına ve üçlü gruplara taş işleyebilirsin. Çifte taş işlenmez. Okeyi serinin iki ucuna da koyabiliyorsan hangi uca koyacağını seçersin.</li>
          </ul>
          <h3>Bitiş ve puan</h3>
          <table className="mk-kural-tablo">
            <tbody>
              <tr><th scope="row">Son taşını atıp bitiren</th><td className="is-arti">+101</td></tr>
              <tr><th scope="row">Elden biten (aynı turda açıp bitiren)</th><td className="is-arti">+202; diğerlerinin kaybı 2 kat</td></tr>
              <tr><th scope="row">Açamayan</th><td className="is-eksi">−202</td></tr>
              <tr><th scope="row">Açan ama bitiremeyen</th><td className="is-eksi">Elde kalan taşların sayı toplamı kadar eksi</td></tr>
              <tr><th scope="row">Çiftle açan</th><td className="is-eksi">Kalan toplamın 2 katı</td></tr>
              <tr><th scope="row">Elde kalan okey</th><td className="is-eksi">101 sayılır (sahte okey: okeyin sayısı)</td></tr>
            </tbody>
          </table>
          <ul className="mk-kural-cezalar">
            <li><i className="mk-ceza-rozet is-islek">İşlek taş attı</i> <b>−101</b> <span>Masadaki bir pere işlenebilecek taşı yere atmak. Açmamış olsan da yazılır.</span></li>
            <li><i className="mk-ceza-rozet is-okey">Okey attı</i> <b>−101</b> <span>Okeyi yere atmak.</span></li>
          </ul>
          <p>Bitirirken attığın son taşa ceza yazılmaz. <b>Deste biterse</b> el kazanansız biter: açamayan −202, açan elindeki taşların toplamı kadar eksi alır.</p>
        </article>
      )}

      {sekme === 'uno' && (
        <article className="mk-kural" role="tabpanel">
          <p className="mk-kural-giris">2–8 oyuncu, 108 kart: dört renkte (kırmızı, sarı, yeşil, mavi) birer 0, ikişer 1–9, ikişer Atlat, Yön ve +2; ayrıca 4 Joker ve 4 +4. Herkese <b>7 kart</b> dağıtılır. Amaç elindeki kartları <b>ilk bitiren</b> olmak. Masada resmî Uno kuralları geçerlidir; kurucu lobide başka bir mod seçebilir.</p>
          <h3>Dağıtım ve ilk kart</h3>
          <ul>
            <li>Deste tamamen rastgele karılır. <b>Dengeli dağıtım:</b> bir ele 2’den çok Joker/+4 (en çok bir +4) ya da 3’ten çok aksiyon kartı (Atlat, Yön, +2) düşerse fazlası destedeki rastgele bir sayı kartıyla değiştirilir. Elinde zaten 3 Joker/+4 olan oyuncu desteden dördüncüsünü çekmez. Böylece bir oyuncu jokerlerle eli birkaç turda bitiremez.</li>
            <li>Ortaya bir kart açılır. <b>+4</b> açılırsa desteye geri konur, yeni kart açılır.</li>
            <li><b>Joker</b> açılırsa ilk oyuncu rengi seçer, sonra oynar.</li>
            <li><b>Atlat</b> açılırsa ilk oyuncunun sırası geçer; <b>Yön</b> açılırsa sıra ters döner ve ilk oyuncunun sağındaki başlar; <b>+2</b> açılırsa ilk oyuncu 2 kart çeker, sırası geçer.</li>
          </ul>
          <h3>Kart oynama</h3>
          <p>Ortadaki kartla <b>rengi</b>, <b>sayısı</b> ya da <b>simgesi</b> aynı olan kartı atarsın. Joker her zaman oynanır.</p>
          <div className="mk-ornekler">
            <Kartlar k={[['k', '7'], ['k', '2']]} ad="Aynı renk" iyi />
            <Kartlar k={[['k', '7'], ['m', '7']]} ad="Aynı sayı" iyi />
            <Kartlar k={[['y', 'pas'], ['m', 'pas']]} ad="Aynı simge" iyi />
            <Kartlar k={[['k', '7'], ['y', '3']]} ad="Renk de sayı da tutmuyor" iyi={false} />
          </div>
          <p>Oynayacak kartın yoksa (ya da oynamak istemiyorsan) desteden <b>1 kart çekersin</b>. Çektiğin kart uyuyorsa hemen oynayabilirsin; o tur başka kart oynayamazsın. Uymuyorsa sırayı geçersin. Deste biterse ortadaki kartlar (en üstteki hariç) karılıp yeni deste olur.</p>
          <h3>Özel kartlar</h3>
          <div className="mk-ornekler">
            <Kartlar k={[['y', 'pas']]} ad="Atlat: sıradaki oyuncu oynayamaz" />
            <Kartlar k={[['s', 'yon']]} ad="Yön: sıra tersine döner; 2 kişide atlat sayılır" />
            <Kartlar k={[['m', '+2']]} ad="+2: sıradaki 2 kart çeker, sırası geçer" />
            <Kartlar k={[[null, 'joker']]} ad="Joker: rengi sen seçersin" />
            <Kartlar k={[[null, '+4']]} ad="+4: rengi seçersin; sıradaki 4 kart çeker, sırası geçer" />
          </div>
          <h3>+4 ve itiraz</h3>
          <p>+4’ü yalnız elinde <b>ortadaki renkten kart yokken</b> oynayabilirsin (aynı sayı ya da başka joker olması sorun değildir). Yine de oynanabilir; ama sıradaki oyuncu iki seçenekten birini seçer:</p>
          <ul>
            <li><b>Kabul et:</b> 4 kart çeker, sırası geçer.</li>
            <li><b>İtiraz et:</b> oynayanın eli kontrol edilir. Elinde o renkten kart vardıysa +4 kuralsızdır: <b>oynayan 4 kart çeker</b>, itiraz eden normal oynar. Kart yoktuysa itiraz boşa çıkar: <b>itiraz eden 6 kart çeker</b>, sırası geçer.</li>
          </ul>
          <p>Klasik kuralda +2 ve +4 <b>üst üste eklenmez</b>: kart çeken oyuncu karşılık veremez.</p>
          <h3>UNO demek</h3>
          <p>Sondan bir önceki kartını oynarken <b>UNO</b> dersin. Demeyi unutursan, sıradaki oyuncu hamle yapana dek herhangi bir rakip seni <b>yakalayabilir</b>: 2 kart çekersin. Yakalanmadan önce fark edip UNO dersen kurtulursun.</p>
          <h3>Oyun modları</h3>
          <ul>
            <li><b>Klasik:</b> yukarıdaki resmî kurallar.</li>
            <li><b>Yığma:</b> +2’nin üstüne +2 ya da +4, +4’ün üstüne +4 eklenebilir; ceza birikir (ör. +2, +2, +4 = 8 kart). Ekleyecek kartı olmayan biriken kartların hepsini çeker ve sırası geçer. Bu modda +4’e itiraz yoktur.</li>
            <li><b>7-0:</b> 7 oynayan, elini en az kartı olan rakibiyle değiştirir. 0 oynanınca herkes elini oyun yönündeki komşusuna verir. Takastan sonra UNO durumu yeniden sayılır.</li>
            <li><b>Atlama:</b> ortadaki kartın <b>tıpkısı</b> (aynı renk ve aynı sayı ya da simge) elindeyse sıranı beklemeden atarsın; sıra senden devam eder, atlanan oyuncular sırasını kaybeder. Joker ve +4 ile atlanmaz. En hızlı davranan kazanır.</li>
            <li><b>Hızlı:</b> herkese 7 yerine 5 kart dağıtılır; kurallar klasikle aynıdır, eller kısa sürer.</li>
            <li><b>Çek-çek:</b> oynayamıyorsan uyan bir kart gelene dek çekmeye devam edersin; gelen kartı hemen oynayabilir ya da geçebilirsin.</li>
          </ul>
          <h3>Puan</h3>
          <table className="mk-kural-tablo">
            <tbody>
              <tr><th scope="row">Sayı kartı (0–9)</th><td>Üstündeki sayı</td></tr>
              <tr><th scope="row">Atlat, Yön, +2</th><td>20</td></tr>
              <tr><th scope="row">Joker, +4</th><td>50</td></tr>
            </tbody>
          </table>
          <p>El bitince kaybedenler <b>ellerindeki kartların değeri kadar eksi</b> alır; kazanan bu değerlerin <b>toplamını artı</b> olarak alır. Son kart +2 ya da +4 ise sıradaki oyuncu yine çeker ve o kartlar da sayılır.</p>
        </article>
      )}

      {sekme === 'duz' && <DuzKurallar renkler={rk} />}
      {sekme === 'kastet' && <KastetKurallar renkler={rk} />}
      {sekme === 'remi' && <RemiKurallar renkler={rk} />}
      {sekme === 'domino' && <DominoKurallar renkler={rk} />}
      {sekme === 'pisti' && <PistiKurallar />}

      {sekme === 'go' && <GoKurallar />}
      {sekme === 'cizgi' && <CizgiKurallar />}
      {sekme === 'xox' && <XoxKurallar />}

      {sekme === 'ceza' && (
        <article className="mk-kural" role="tabpanel">
          <p className="mk-kural-giris">Her elin sonunda puanlar ve cezalar ayrı ayrı gösterilir. Puanı yüksek olan iyidir; maçı toplam puanı en yüksek oyuncu (takım oyununda takım) kazanır.</p>
          <h3>Cezalar</h3>
          <table className="mk-kural-tablo is-ceza">
            <thead><tr><th scope="col">Ceza</th><th scope="col">Oyun</th><th scope="col">Bedel</th></tr></thead>
            <tbody>
              <tr><th scope="row"><i className="mk-ceza-rozet is-islek">{CEZA_BILGI.islek.ad}</i><small>{CEZA_BILGI.islek.ne}</small></th><td>Yedili, Takım</td><td className="is-eksi">−5 + 1 ceza taşı, sıra geçer</td></tr>
              <tr><th scope="row"><i className="mk-ceza-rozet is-per">{CEZA_BILGI.per.ad}</i><small>{CEZA_BILGI.per.ne}</small></th><td>Yedili, Takım</td><td className="is-eksi">−5 + 1 ceza taşı, sıra geçer</td></tr>
              <tr><th scope="row"><i className="mk-ceza-rozet is-islek">{CEZA_BILGI.islekAtti.ad}</i><small>{CEZA_BILGI.islekAtti.ne}</small></th><td>101 Okey</td><td className="is-eksi">−101</td></tr>
              <tr><th scope="row"><i className="mk-ceza-rozet is-okey">{CEZA_BILGI.okeyAtti.ad}</i><small>{CEZA_BILGI.okeyAtti.ne}</small></th><td>101 Okey</td><td className="is-eksi">−101</td></tr>
              <tr><th scope="row"><i className="mk-ceza-rozet is-uno">{CEZA_BILGI.uno.ad}</i><small>Tek kart kalınca UNO demeyip yakalanmak.</small></th><td>Uno</td><td className="is-eksi">2 kart çeker (puanı el sonunda kart değeriyle yansır)</td></tr>
            </tbody>
          </table>
          <p>101 Okey’de açamadan biten el ceza değil, el puanıdır: <b>−202</b>.</p>
          <h3>El puanı</h3>
          <table className="mk-kural-tablo">
            <thead><tr><th scope="col">Oyun</th><th scope="col">Kazanan</th><th scope="col">Diğerleri</th></tr></thead>
            <tbody>
              <tr><th scope="row">Yedili Okey</th><td>0</td><td className="is-eksi">Kalan taş sayısı kadar eksi</td></tr>
              <tr><th scope="row">Takım Yedili</th><td>Takımın ikisi de 0</td><td className="is-eksi">Kalan taş sayısı kadar eksi</td></tr>
              <tr><th scope="row">101 Okey</th><td className="is-arti">+101 (elden +202)</td><td className="is-eksi">Açamayan −202; açan kalan taş toplamı (çiftle açan 2 kat, okey 101)</td></tr>
              <tr><th scope="row">Uno</th><td className="is-arti">Rakip kartlarının toplam değeri</td><td className="is-eksi">Elindeki kartların değeri kadar eksi</td></tr>
            </tbody>
          </table>
          <p>Cezalar el puanına eklenir ve kazanan dahil herkese yazılır. Kurucu maçı el ortasında bitirirse <b>yarım el puanlanmaz</b>.</p>
          <h3>İstatistik</h3>
          <p>Biten her el kaydedilir: oyun türüne göre kazanma oranın, toplam puanın, ceza sayın; ayrıca her arkadaşına karşı kaç el kazandığın. Botlarla oynanan eller genel sayılara girer, “Rakiplere karşı” listesine girmez.</p>
        </article>
      )}

      {sekme === 'ipucu' && (
        <article className="mk-kural" role="tabpanel">
          <h3>Masa kurma ve katılma</h3>
          <ul>
            <li>Bir oyun seç, <b>Arkadaşlarla oyna</b> de: masa kurulur ve 5 karakterli kod verilir. Kodu ya da bağlantıyı paylaş; arkadaşların “Kodla katıl” ile oturur.</li>
            <li>Eksik koltuklara lobide <b>bot</b> ekleyebilirsin. <b>Bota karşı oyna</b> dersen botlar oturur, oyun hemen başlar.</li>
            <li>El sayısı, tema, taş renkleri ve yardımcı asistan lobide ayarlanır; yalnız kurucu değiştirir. Tema ve renkler oyun sırasında da değişebilir.</li>
          </ul>
          <h3>Durdur, devam et, bitir</h3>
          <ul>
            <li>Kurucu menüden oyunu <b>durdurabilir</b>; devam ettirene dek kimse hamle yapamaz.</li>
            <li><b>Oyunu bitir</b> maçı o anki toplam puanlarla sonuçlandırır; yarım kalan el puanlanmaz.</li>
            <li>Bağlantısı kopan oyuncunun yerine kurucu <b>bot oynatabilir</b>; oyuncu geri dönünce koltuğunu alır.</li>
          </ul>
          <h3>Yarım kalan oyuna dönme</h3>
          <ul>
            <li>Sayfayı kapatsan da koltuğun durur. Oyunlar sayfasını açınca son masana kendiliğinden oturursun; diğerleri “Yarım kalan oyunların” listesindedir.</li>
            <li><b>Masadan kalk</b> dersen yerine bot oynar; aynı kodla dönünce elini bottan geri alırsın.</li>
            <li><b>Merkeze dön (oyun sürsün)</b> koltuğunu boşaltmaz; sıra sana gelince oyun seni bekler.</li>
          </ul>
          <h3>Yardımcı asistan</h3>
          <ul>
            <li>Açıkken: açabileceğin perleri ve işlek taşlarını gösterir, taşlarını dizer, istenirse en iyi hamleyi senin yerine oynar.</li>
            <li>Yedili’de ceza yememek için en büyük yardımcın odur: taş çekmeden önce işlek taşın ya da perin kalıp kalmadığına bak.</li>
            <li>Kapalıyken ipucu verilmez; kurallar ve cezalar aynen işler.</li>
          </ul>
          <h3>Taş ve kart oynatma</h3>
          <ul>
            <li><b>Sürükle bırak:</b> taşı ya da kartı tutup hedefe bırak. Geçerli hedefler sürüklerken belirir; yanlış yere bırakırsan taş yerine döner.</li>
            <li><b>Dokun, seç:</b> sürüklemek yerine önce taşa, sonra hedefe dokun. Per açmak için taşları sırayla seç.</li>
            <li><b>Basılı tut:</b> ıstakandaki taşı basılı tutup kaydırarak dizilişini değiştir.</li>
            <li>Kural dışı hamlede sunucu hamleyi geri çevirir ve nedenini kısa bir bildirimle söyler.</li>
          </ul>
          <h3>Üst çubuk</h3>
          <ul>
            <li><b>Skor:</b> el el puan tablosu ve bu elin cezaları.</li>
            <li><b>Tepki:</b> masadakilere kısa bir emoji gönder.</li>
            <li><b>2B / 3B:</b> okey masasını düz ya da derinlikli görünümde oyna; istediğin an değiştir.</li>
            <li><b>Ses</b> ve <b>titreşim</b> menüdeki görünüm tercihlerinden de açılıp kapanır. Sağdaki nokta bağlantını ve gecikmeyi gösterir.</li>
          </ul>
        </article>
      )}
    </div>
  );
}
