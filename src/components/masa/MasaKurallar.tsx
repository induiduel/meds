/**
 * Kurallar (sekmeli). Metin motorlarla birebir: motor/yedili.ts, yuzbir.ts (+ yuzbirAsistan.ts), uno.ts (+ unoAsistan.ts).
 * Kural değişirse önce motor, sonra bu sayfa güncellenir.
 */
import React, { useState } from 'react';
import { ArrowDown, Check, Layers, Plus, SkipForward, Upload, X } from 'lucide-react';
import { OYUN_ADI, VARSAYILAN_RENKLER, type OyunTur, type UnoMod } from '../../services/masa/tipler';
import { CEZA_BILGI, TasOrnek } from './kabukOrtak';
import DuzKurallar from './kurallar/DuzKurallar';
import UnoKurallar from './kurallar/UnoKurallar';
import KastetKurallar from './kurallar/KastetKurallar';
import RemiKurallar from './kurallar/RemiKurallar';
import PistiKurallar from './kurallar/PistiKurallar';
import DominoKurallar from './kurallar/DominoKurallar';
import { CizgiKurallar, GoKurallar, XoxKurallar } from './kurallar/TahtaKurallar';
import { Akis, Kunye, TanitSatir, TasTanitim } from './kurallar/gorsel';
import { KATEGORILER } from './oyunKatalog';

/** `uno:<mod>`: Uno sekmesini o modun sayfasıyla açar (lobi ve merkezdeki "Kartları ve kuralları gör") */
export type KuralSekme = OyunTur | 'ceza' | 'ipucu' | `uno:${UnoMod}`;
type Sekme = OyunTur | 'ceza' | 'ipucu';
/** Sekmeler merkezdeki kategori sırasıyla gruplanır; sonda oyunlardan bağımsız genel bölümler */
const SEKME_GRUPLAR: { ad: string; sekmeler: [Sekme, string][] }[] = [
  ...KATEGORILER.map((k) => ({ ad: k.ad, sekmeler: k.turler.map((t): [Sekme, string] => [t, OYUN_ADI[t]]) })),
  { ad: 'Genel', sekmeler: [['ceza', 'Cezalar ve puan'], ['ipucu', 'Masa ve ipuçları']] },
];

type T = [number, 0 | 1 | 2 | 3];

export default function MasaKurallar({ ilk = 'yedili', renkler }: { ilk?: KuralSekme; renkler?: string[] }) {
  const unoMod = typeof ilk === 'string' && ilk.startsWith('uno:') ? (ilk.slice(4) as UnoMod) : undefined;
  const [sekme, setSekme] = useState<Sekme>(unoMod ? 'uno' : (ilk as Sekme));
  const rk = renkler && renkler.length === 4 ? renkler : [...VARSAYILAN_RENKLER];

  const Taslar = ({ t, ad, iyi, okey }: { t: T[]; ad: string; iyi?: boolean; okey?: { s: number; r: 0 | 1 | 2 | 3 } }) => (
    <figure className={`mk-ornek${iyi === false ? ' is-kotu' : iyi ? ' is-iyi' : ''}`}>
      <div className="mk-ornek-sira">{t.map(([s, r], i) => <TasOrnek key={i} s={s} r={r} renkler={rk} boy={30} okey={okey} />)}</div>
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
        {SEKME_GRUPLAR.map((g) => (
          <div key={g.ad} className="mk-kural-sekme-grup" role="presentation">
            <span aria-hidden="true">{g.ad}</span>
            {g.sekmeler.map(([k, ad]) => <button key={k} type="button" role="tab" aria-selected={sekme === k} className={sekme === k ? 'is-on' : ''} onClick={() => setSekme(k)}>{ad}</button>)}
          </div>
        ))}
      </div>

      {sekme === 'yedili' && (
        <article className="mk-kural" role="tabpanel">
          <Kunye tur="yedili" malzeme="104 taş, joker yok" amac="elindeki taşları masaya eritip ilk bitiren olmak" />
          <p className="mk-kural-giris">Ana oyun. 2–6 oyuncu, 104 taş (1’den 13’e, dört renk, her taştan iki tane). Joker yok. Herkese <b>7 taş</b> dağıtılır; amaç elindeki taşları masaya eritip <b>elini ilk bitiren</b> olmak.</p>
          <h3>Taşları tanı</h3>
          <TasTanitim rk={rk} />
          <h3>Per nedir</h3>
          <p>Per, en az 3 taşlık geçerli dizidir. İki türü var:</p>
          <PerOrnekleri />
          <ul>
            <li><b>Seri:</b> aynı renkten ardışık sayılar; 3 taştan 13 taşa kadar uzayabilir.</li>
            <li><b>Grup:</b> aynı sayının farklı renkleri; 3 ya da 4 taş.</li>
          </ul>
          <h3>Sıran gelince</h3>
          <Akis adimlar={[
            { ikon: <Layers size={18} />, ad: 'Per aç', metin: 'Elinde en az 3 taşlık seri ya da grup varsa masaya aç.' },
            { ikon: <Plus size={18} />, ad: 'Taş işle', metin: 'Per açtıysan masadaki her pere uyan taşını ekle.' },
            { ikon: <ArrowDown size={18} />, ad: 'Taş çek', metin: 'Yapacak hamlen yoksa desteden 1 taş çek.', bag: 'yada' },
            { ikon: <SkipForward size={18} />, ad: 'Eli devret', metin: 'Hamle kalmayınca sıra sonraki oyuncuya geçer.' },
          ]} />
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
            <li>Masadaki taşların <b>hepsi masada kalır</b>; hiçbir taş ele geri alınamaz.</li>
            <li><b>Elinden taş katabilirsin:</b> masadaki bir taşı perinden alıp elindeki taşlarla yeni per kurarsın. Örneğin dörtlü 10 grubundaki sarı 10’u alır, elindeki sarı 9 ve 11 ile 9-10-11 serisi yaparsın; geride üçlü 10 grubu kalır.</li>
            <li>Onayladığında her per yine geçerli olmalıdır (en az 3 taşlık seri ya da grup).</li>
            <li><b>Düğmeye basmak şart değil:</b> elindeki taşları seçip <b>Per aç</b>’a basarsan (ya da masadaki taşa dokunursan) eksik taş masadan kendiliğinden alınır; hangi renk olursa olsun, taşı veren per geçerli kalıyorsa olur. Doğrudan olmuyorsa masadaki taşa dokunmak düzenlemeyi başlatır.</li>
            <li><b>Sırala</b> ıstakanı perlere, renge ya da sayıya göre; <b>Masayı diz</b> masadaki perleri renge ya da sayıya göre dizer, aradığın taşı kolay bulursun.</li>
            <li>Elinden taş kattıysan bu bir hamledir (o turda artık taş çekilmez); yalnız yer değiştirdiysen ardından işleyebilir, per açabilir ya da taş çekebilirsin.</li>
          </ul>
          <h3>Geri al</h3>
          <p>Kendi sırandaki per açma, taş işleme ve masa düzenleme hamlelerini <b>Geri al</b> ile tek tek geri alabilirsin; ıstakadaki taş yer değiştirmelerin de geri alınır. Taş çekme, eli devretme ve hediye taş verdiren hamle geri alınmaz (gizli taş açılmıştır).</p>
          <h3>Normal ve zorlu mod</h3>
          <ul>
            <li><b>Normal mod:</b> ipucu, otomatik işleme, en iyi hamle, ıstakayı sıralama ve masayı dizme yardımcıları açıktır.</li>
            <li><b>Zorlu mod:</b> ipucu, otomatik işle ve en iyi hamle yoktur. Istakayı sıralama, masayı dizme, masayı düzenleme ve geri al her iki modda da vardır.</li>
            <li><b>Otomatik sıralama:</b> menüdeki “Istakayı otomatik sırala” açıkken çektiğin taş son seçtiğin sıralamaya (renk ya da sayı) göre yerine girer; kapatırsan taşlar elle dizdiğin gibi kalır.</li>
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
          <Kunye tur="takim" malzeme="104 taş, joker yok" amac="takımdan birinin elini bitirmesi" />
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
          <Kunye tur="yuzbir" malzeme="106 taş: 104 + 2 sahte okey" amac="perlerini açıp son taşını atarak bitirmek" />
          <p className="mk-kural-giris">2–4 oyuncu, 106 taş: 104 sayı taşı + 2 sahte okey. Herkese <b>21 taş</b>, eli başlatana 22 taş verilir. Amaç perlerini açıp taşlarını eritmek ve <b>son taşını yere atarak</b> bitirmek.</p>
          <h3>Taşları tanı</h3>
          <TasTanitim rk={rk} ek={
            <TanitSatir ad="Okey ve sahte okey" alt="gösterge 6 ise okey 7">
              <TasOrnek s={6} r={0} renkler={rk} boy={30} /><span className="mk-tanit-ok" aria-hidden="true">→</span>
              <TasOrnek s={7} r={0} renkler={rk} boy={30} okey={{ s: 7, r: 0 }} /><TasOrnek s={0} r={0} renkler={rk} boy={30} okey={{ s: 7, r: 0 }} />
              <span className="mk-tanit-esit">= 106 taş</span>
            </TanitSatir>
          } />
          <h3>Gösterge, okey ve sahte okey</h3>
          <p>Dağıtımda bir taş açılır: <b>gösterge</b>. Göstergenin aynı renkteki bir üstü o elin <b>okeyidir</b> (13’ün üstü 1). Okey jokerdir: her taşın yerine geçer. <b>Sahte okey</b> joker değildir; okey taşının kendi sayısını ve rengini taşır.</p>
          <div className="mk-ornekler">
            <Taslar t={[[6, 0]]} ad="Gösterge kırmızı 6 ise…" />
            <Taslar t={[[7, 0]]} ad="…okey kırmızı 7’dir (joker)" okey={{ s: 7, r: 0 }} />
            <Taslar t={[[0, 0]]} ad="Sahte okey: kırmızı 7 sayılır" okey={{ s: 7, r: 0 }} />
          </div>
          <h3>Sıran gelince</h3>
          <Akis adimlar={[
            { ikon: <ArrowDown size={18} />, ad: 'Taş çek', metin: 'Desteden ya da yandan (önceki oyuncunun attığı taş).' },
            { ikon: <Layers size={18} />, ad: 'Aç ve işle', metin: 'İstersen 101 ile ya da 5 çiftle aç; açtıysan taş işle.' },
            { ikon: <Upload size={18} />, ad: 'Bir taş at', metin: 'Tur taş atınca biter; son taşını atan eli bitirir.' },
          ]} />
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
            <li><b>Masayı düzenle:</b> açtıktan sonra, taşını çekince masadaki seri ve grupları yeniden dizebilir, bir taşı perinden alıp elindeki taşlarla yeni per kurabilirsin (dörtlü 10 grubundan sarı 10 + elindeki sarı 9 ve 11). Her per yine geçerli kalmalı, hiçbir taş ele dönmez, çiftlere dokunulmaz, atacak bir taşın kalmalıdır.</li>
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

      {sekme === 'uno' && <UnoKurallar mod={unoMod} />}

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
