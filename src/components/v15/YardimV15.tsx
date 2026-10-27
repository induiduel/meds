import React, { useMemo, useState } from 'react';
import { ChevronDown, Flag, Keyboard, MessagesSquare, Search } from 'lucide-react';
import { linkClick, navigateTo, pathFor, type AppRoute } from '../../router';
import { katla } from '../../services/cevrimdisi/dersBirimleri';
import { useV15Baslik } from './baslik';
import '../../styles/v15/ogren.css';
import '../../styles/v15/kisisel.css';

/**
 * v15 · Yardım merkezi (tasarım AB14 yardimMerkezi) — /yardim. İçerik sitenin gerçekte var olan özelliklerini anlatır
 * (kaynak: ilgili ekranların kodu); yeni özellik eklenince buraya madde eklenir. Arama: başlık + metin, Türkçe katlamalı.
 */
type Kat = 'Sesli ders' | 'Soru' | 'Program' | 'Hücrem' | 'Hesap' | 'Çevrimdışı';
interface Sss { k: Kat; s: string; c: string; git?: [AppRoute, string] }

const SSS: Sss[] = [
  { k: 'Sesli ders', s: 'Sesli derste slaytın köşesinde yanıp sönen işaret ne?', c: 'O slayttaki bilgi geçmiş yıllarda sınavda sorulmuş demektir. Dokununca anlatım durur ve çıkmış soru açılır; soruyu kapatınca ders kaldığı yerden sürer. İşaret yalnız doğrulanmış eşleşmelerde görünür.', git: ['canli_ders', 'Sesli derslere git'] },
  { k: 'Sesli ders', s: 'Ses ile PDF neden ayrı yerlerde duruyor?', c: 'Anlatım cümle cümle PDF sayfasına bağlıdır; konuşulan cümleye göre sayfa ve işaret ilerler. Ekran darsa PDF ile oynatıcı alt alta dizilir. Tam ekranda ikisi yan yana ya da üst üste görünür.' },
  { k: 'Sesli ders', s: 'Sesli derste hangi klavye kısayolları var?', c: 'Tam ekranda Boşluk oynatır ya da duraklatır, sol ve sağ ok 10 saniye geri ve ileri sarar, Shift ile birlikte ok bir önceki ya da sonraki bölüme geçer. + ve − yazıyı büyütüp küçültür, Esc tam ekrandan çıkar.' },
  { k: 'Sesli ders', s: 'Bir bilgiyi sonra tekrar etmek için nasıl saklarım?', c: 'Ders sayfasındaki terim, hastalık ya da bilgi kartında yıldıza dokun. Yıldızlı kayıtlar Bugün sayfasındaki favoriler bölümünde toplanır ve PDF olarak yazdırılabilir.' },
  { k: 'Soru', s: 'Cevap anahtarı ya da soru hatalıysa ne yaparım?', c: 'Soru kartındaki bayrak simgesine (Hata bildir) dokun ve hatayı kısaca yaz. Bildirim moderatör inceleme sırasına girer.', git: ['past_exams', 'Çıkmış sorulara git'] },
  { k: 'Soru', s: 'Yanlış yaptığım sorular nereye gidiyor?', c: 'Soru çözüm ve deneme ekranlarında yanlış yaptığın sorular Yanlışlarım sayfasında toplanır. Tekrar zamanı gelenleri “Hazır olanları çöz” ile yeniden çözersin; doğru cevap verdikçe tekrar aralığı uzar.', git: ['yanlislarim', 'Yanlışlarım'] },
  { k: 'Soru', s: 'Arkadaşlarımla aynı anda nasıl soru çözerim?', c: 'Oyunlar sayfasında oda kur, branş ve soru sayısını seç, oda kodunu paylaş. Herkes “Hazırım” deyince aynı soru aynı anda gelir; puan doğruluk, hız ve seriye göre hesaplanır. Tek başına da oynanabilir.', git: ['oyunlar', 'Oyunlar'] },
  { k: 'Program', s: 'Ders programına kendi etkinliğimi ekleyebilir miyim?', c: 'Evet. Ders programı sayfasındaki “Ekle” düğmesiyle laboratuvar, telafi ya da grup çalışması gibi etkinlikler eklersin. Bunlar yalnız sende, resmî derslerin yanında görünür ve hesabınla eşitlenir.', git: ['program_ekle', 'Programa ekle'] },
  { k: 'Program', s: 'Tarih ve saat biçimini değiştirebilir miyim?', c: 'Dil ve bölge sayfasından tarih biçimini (29 Ekim 2026 ya da 29.10.2026), saat biçimini (24 ya da 12 saat) ve haftanın ilk gününü seçebilirsin. Site şimdilik yalnız Türkçedir.', git: ['dil_bolge', 'Dil ve bölge'] },
  { k: 'Hücrem', s: 'Hücrem nedir, nasıl büyür?', c: 'Çalışarak kazandığın ATP ya da glukozla hücreni 28 evrim basamağında büyütürsün. Her basamak bir önceki açılınca alınabilir ve yeni bir tıbbi bilgi açar. Glukoz bakiyen sahnedeki akışı, canlılığın hücrenin rengini belirler.', git: ['hucrem', 'Hücrem'] },
  { k: 'Hesap', s: 'İlerlemem başka cihazımda da görünür mü?', c: 'Giriş yaptığında çözdüğün sorular, çalışma süren, notların, favorilerin ve ders ilerlemen hesabına eşitlenir. Görünüm tercihleri (tema, yerleşim, dil ve bölge) ise her cihazda ayrı saklanır.' },
  { k: 'Hesap', s: 'Profil bilgilerimi nasıl değiştiririm?', c: 'Profil ve ayarlar sayfasındaki “Okul ve hedef” satırından üniversite, sınıf, kurul ve günlük hedefini güncelleyebilirsin. Günlük hedef Bugün sayfasındaki plan halkasını belirler.', git: ['settings', 'Profil ve ayarlar'] },
  { k: 'Çevrimdışı', s: 'Çevrimdışıyken neler çalışır?', c: 'Çevrimdışı sayfasından indirdiğin dersler (sesli anlatım, PDF, soru çözücü, Öğren destesi) internetsiz açılır. Bu sırada çözdüğün sorular ve çalışma süren cihazda bekler, bağlantı gelince kendiliğinden gönderilir.', git: ['cevrimdisi', 'Çevrimdışı'] },
  { k: 'Çevrimdışı', s: 'İndirme neden bekliyor?', c: 'İnternet yoksa ya da “Yalnız Wi-Fi” açıkken hücresel veriye bağlıysan indirme bekler. Süren ve bekleyen işleri Arka plan işleri sayfasında görür, duraklatır ya da sıradan çıkarırsın.', git: ['arka_plan', 'Arka plan işleri'] },
];
const KATLAR: Kat[] = ['Sesli ders', 'Soru', 'Program', 'Hücrem', 'Hesap', 'Çevrimdışı'];
const KISAYOL: [string, string][] = [
  ['Ctrl + K  ya da  /', 'Aramayı aç (Mac: ⌘ + K)'],
  ['Boşluk', 'Sesli ders tam ekranda oynat / duraklat'],
  ['← / →', 'Sesli derste 10 sn geri / ileri'],
  ['Shift + ← / →', 'Önceki / sonraki bölüm (zaman çubuğu seçiliyken)'],
  ['[ / ]', 'Sesli derste hızı düşür / artır'],
  ['?', 'Yardım merkezini aç'],
  ['+ / −', 'Tam ekranda yazı boyutu'],
  ['Esc', 'Pencereyi ya da tam ekranı kapat'],
];

export default function YardimV15() {
  const [q, setQ] = useState('');
  const [kat, setKat] = useState<Kat | null>(null);
  const [acik, setAcik] = useState<number | null>(null);
  useV15Baslik({ baslik: 'Yardım', alt: 'Sık sorulanlar ve kısayollar' });
  const liste = useMemo(() => {
    const t = katla(q.trim());
    return SSS.map((x, i) => ({ ...x, i })).filter((x) => (!kat || x.k === kat) && (!t || katla(`${x.s} ${x.c} ${x.k}`).includes(t)));
  }, [q, kat]);
  const git = (r: AppRoute) => (e: React.MouseEvent) => linkClick(() => navigateTo(pathFor(r)))(e);
  const topluluk = pathFor('topluluk');
  return (
    <div className="ym15">
      <h1 className="sr-only">Yardım</h1>
      <label className="ym15-ara v15-card">
        <Search aria-hidden />
        <input type="search" value={q} onChange={(e) => { setQ(e.target.value); setAcik(null); }} placeholder="Sorunu yaz: “indirme bekliyor”" aria-label="Yardımda ara" />
      </label>
      <div className="o15-cipler v15-hscroll ym15-cip" role="toolbar" aria-label="Konu">
        <button type="button" className={`o15-cip${!kat ? ' is-on' : ''}`} aria-pressed={!kat} onClick={() => setKat(null)}>Tümü</button>
        {KATLAR.map((k) => <button key={k} type="button" className={`o15-cip${kat === k ? ' is-on' : ''}`} aria-pressed={kat === k} onClick={() => setKat(kat === k ? null : k)}>{k}</button>)}
      </div>

      {!liste.length ? (
        <p className="b15-bos v15-card kp15-bos">“{q}” için yanıt bulunamadı. Aşağıdaki Topluluk kanallarından sorabilirsin.</p>
      ) : (
        <ul className="ym15-l v15-card">
          {liste.map((x) => (
            <li key={x.i}>
              <button type="button" className="ym15-s" aria-expanded={acik === x.i} onClick={() => setAcik(acik === x.i ? null : x.i)}>
                <span><b>{x.s}</b><span className="v15-cap">{x.k}</span></span>
                <ChevronDown aria-hidden />
              </button>
              {acik === x.i && (
                <div className="ym15-c">
                  <p>{x.c}</p>
                  {x.git && <a href={pathFor(x.git[0])} onClick={git(x.git[0])}>{x.git[1]}</a>}
                </div>
              )}
            </li>
          ))}
        </ul>
      )}

      <section className="v15-card ym15-k" aria-labelledby="ym15-kh">
        <h2 id="ym15-kh" className="v15-h2"><Keyboard aria-hidden /> Klavye kısayolları</h2>
        <dl>{KISAYOL.map(([t, a]) => <div key={t}><dt><kbd>{t}</kbd></dt><dd>{a}</dd></div>)}</dl>
      </section>

      <div className="ym15-g2">
        <a className="v15-card ym15-i" href={topluluk} onClick={git('topluluk')}>
          <span className="v15-tile"><MessagesSquare aria-hidden /></span>
          <span className="kp15-t"><b>Toplulukta sor</b><span className="v15-cap">Sohbet kanallarında öğrencilere ve moderatörlere yaz</span></span>
        </a>
        <div className="v15-card ym15-i">
          <span className="v15-tile is-n"><Flag aria-hidden /></span>
          <span className="kp15-t"><b>İçerik hatası bildir</b><span className="v15-cap">Soru kartındaki bayrak simgesiyle; moderatör inceler</span></span>
        </div>
      </div>
    </div>
  );
}
