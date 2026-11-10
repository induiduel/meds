/** Taş Domino kuralları. Metin motorla birebir: services/masa/motor/domino.ts. Kural değişirse önce motor, sonra bu sayfa. */
import React from 'react';
import { ArrowDown, Check, Link2, Plus, X } from 'lucide-react';
import { VARSAYILAN_RENKLER } from '../../../services/masa/tipler';
import { TasOrnek } from '../kabukOrtak';
import { Akis, Kunye, TasDizi, TasTanitim } from './gorsel';

type T = [number, 0 | 1 | 2 | 3];

export default function DominoKurallar({ renkler }: { renkler?: string[] }) {
  const rk = renkler && renkler.length === 4 ? renkler : [...VARSAYILAN_RENKLER];
  const Taslar = ({ t, ad, iyi }: { t: T[]; ad: string; iyi?: boolean }) => (
    <figure className={`mk-ornek${iyi === false ? ' is-kotu' : iyi ? ' is-iyi' : ''}`}>
      <div className="mk-ornek-sira">{t.map(([s, r], i) => <TasOrnek key={i} s={s} r={r} renkler={rk} boy={30} />)}</div>
      <figcaption>{iyi !== undefined && (iyi ? <Check size={15} /> : <X size={15} />)} {ad}</figcaption>
    </figure>
  );

  return (
    <article className="mk-kural" role="tabpanel">
      <Kunye tur="domino" malzeme="104 okey taşı, joker yok" amac="taşlarını zincire ekleyip ilk bitiren olmak" />
      <p className="mk-kural-giris">2–4 oyuncu, 104 okey taşı (1’den 13’e, dört renk, her taştan iki tane). Joker yok. Herkese <b>7 taş</b> dağıtılır, desteden bir taş açılıp masanın ortasına konur: zincir bu taşla başlar. Amaç elindeki taşları zincire ekleyip <b>elini ilk bitiren</b> olmak.</p>

      <h3>Taşları tanı</h3>
      <TasTanitim rk={rk} />

      <h3>Zincir</h3>
      <p>Taşlar yan yana dizilerek bir zincir oluşturur. Yalnız <b>iki uçtaki</b> taşlara ekleme yapılır; ortadaki taşlar artık oyuna karışmaz.</p>
      <div className="mk-ornekler">
        <TasDizi rk={rk} t={[[4, 0], [4, 2], [9, 2], [9, 3], [2, 3]]} etiket={{ 0: 'uç', 4: 'uç' }} ad="Bu zincire kırmızı taş, 4, sarı taş ya da 2 eklenebilir" />
      </div>

      <h3>Hangi taş uyar</h3>
      <p>Zincirin iki açık ucu vardır: baştaki ve sondaki taş. Bir uca, o uçtaki taşla <b>rengi ya da sayısı aynı</b> olan her taş eklenebilir:</p>
      <div className="mk-ornekler">
        <Taslar t={[[7, 0], [2, 0]]} ad="Aynı renk, herhangi bir sayı" iyi />
        <Taslar t={[[7, 0], [7, 2]]} ad="Aynı sayı, herhangi bir renk" iyi />
        <Taslar t={[[7, 0], [8, 1]]} ad="Rengi de sayısı da farklı: uymaz" iyi={false} />
      </div>

      <h3>Sıran gelince</h3>
      <Akis adimlar={[
        { ikon: <Link2 size={18} />, ad: 'Taş koy', metin: 'Rengi ya da sayısı tutan taşı iki uçtan birine ekle.' },
        { ikon: <ArrowDown size={18} />, ad: 'Taş çek', metin: 'Koyamıyorsan uyan taş gelene dek desteden çek.', bag: 'yada' },
        { ikon: <Plus size={18} />, ad: 'Ek hamle', metin: 'Ardışık koyduysan ya da uçlar eşitlendiyse bir taş daha koy.' },
      ]} />
      <ol>
        <li><b>Koy:</b> uyan bir taşını iki uçtan birine koy. Koymak zorunlu değildir.</li>
        <li><b>Ya da çek:</b> desteden bir taş çek. Koyabileceğin bir taş varken çekersen sıra hemen geçer.</li>
        <li><b>Koyamıyorsan çek:</b> uyan bir taş gelene dek desteden çekmeye devam edersin. Gelen uyan taşı hemen koyabilir ya da pas diyebilirsin. Deste uyan taş gelmeden biterse sıra geçer.</li>
        <li><b>Deste bittiyse:</b> koyabiliyorsan koymak zorundasın; koyamıyorsan pas dersin.</li>
      </ol>

      <h3>Ek hamle</h3>
      <p>Şu iki durumdan birinde <b>bir taş daha koyma hakkı</b> kazanırsın:</p>
      <ul>
        <li><b>Ardışık:</b> koyduğun taş, bağlandığı uçtaki taşla aynı renkten ve bir eksik ya da bir fazla sayıdır (ör. kırmızı 7’nin yanına kırmızı 8). 13 ile 1 ardışık sayılmaz.</li>
        <li><b>Eş uç:</b> koyduktan sonra zincirin iki ucu aynı sayı olur (ör. bir uçta kırmızı 4, öbüründe mavi 4).</li>
      </ul>
      <p>Ek hamlede çekemezsin; istemezsen pas dersin. Uyan taşın yoksa hak doğmaz. Ek hamleyle koyduğun taş yeni bir ek hamle doğurmaz: bir turda en çok iki taş koyarsın.</p>
      <div className="mk-ornekler">
        <Taslar t={[[7, 0], [8, 0]]} ad="Aynı renkten ardışık: bir taş daha" iyi />
        <Taslar t={[[4, 3], [9, 0], [4, 0]]} ad="İki uç da 4: bir taş daha" iyi />
        <Taslar t={[[13, 0], [1, 0]]} ad="Uyar ama 13–1 ardışık değil: ek yok" iyi={false} />
      </div>

      <h3>El sonu ve puan</h3>
      <ul>
        <li><b>Eli bitiren kazanır.</b> Her rakip elinde kalan taşların sayı toplamı kadar eksi alır; kazanan bu toplamların hepsini artı alır.</li>
        <li><b>Kilit:</b> deste bitmişken koyamayan herkes art arda pas derse el biter. Elindeki sayı toplamı en düşük olan kazanır (eşitlikte birden çok kazanan olur). Diğerleri kendi toplamı kadar eksi alır; kazananlar bu eksilerin toplamını eşit paylaşır (küsurat atılır).</li>
      </ul>

      <h3>İpucu ve zorlu mod</h3>
      <p>Normal modda sıra sendeyken uyan taşların ve gidebilecekleri uçlar hafifçe parlar, <b>İpucu</b> bir hamle önerir. Zorlu modda vurgu ve ipucu yoktur. Taşı seçip uca dokunabilir ya da uca sürükleyebilirsin; uymayan bir uca bırakılan taş sarsılarak geri döner.</p>
    </article>
  );
}
