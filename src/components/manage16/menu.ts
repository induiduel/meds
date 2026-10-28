/**
 * Yönetim v16 — menü ve rota kayıt defteri (TEK KAYNAK).
 * Sayfa eklemek: ilgili gruba { yol, etiket, ikon, yukle: () => import('./sayfalar/...') } ekleyin (docs/YONETIM_V16_KIT.md §2).
 * `yukle` yoksa sayfa menüde görünür ve "yakında" boş durumuyla açılır (v14Slug varsa eski panele bağlantı verir).
 * Adres: /manage/<yol>[/<id>]; çözüm en uzun yol eşleşmesiyle yapılır, kalan parçalar sayfaya `altYol` olarak gelir.
 */
import type React from 'react';
import {
  LayoutDashboard, Inbox, CalendarRange, BookOpen, Layers, FileQuestion, History, GitMerge, ListChecks, Archive,
  TextCursorInput, FilePen, Snowflake, Sparkles, GraduationCap, Mic, Star, Target, Award, CreditCard, Tent,
  BookA, Stethoscope, FileText, Music, Trash2, Eye, Menu as MenuIcon, Construction, Flag, Megaphone, Radio, Tag,
  Users, ShieldCheck, Coins, TrendingUp, CalendarCheck, Activity, Lock, AlertTriangle, MessagesSquare, MessageSquare,
  UserPlus, StickyNote, MessageCircleHeart, Gamepad2, Puzzle, Database, HeartPulse, Bot, Terminal, GitBranch,
  HardDriveDownload, ScrollText, CloudCog, Network, FlaskConical, Link2,
  Package, Landmark, PieChart,
} from 'lucide-react';

export type SayfaProps = {
  /** Sayfa yolundan sonra kalan ilk parça (ör. /manage/kisi/<id>) */
  id?: string;
  /** Sayfa yolundan sonra kalan tüm parçalar */
  altYol: string[];
  /** Panel içi gezinme: git('kisi/abc') ya da git('sistem/denetim?hedef=x') */
  git: (yol: string, o?: { degistir?: boolean }) => void;
};

export type SayfaTanim = {
  yol: string;
  etiket: string;
  ikon: React.ComponentType<{ className?: string; 'aria-hidden'?: boolean | 'true' }>;
  oncelik: 'P0' | 'P1' | 'P2';
  aciklama?: string;
  /** Eski (v14) paneldeki karşılık: "yakında" ekranında bağlantı verilir */
  v14Slug?: string;
  /** Arama için ek sözcükler */
  anahtar?: string;
  yukle?: () => Promise<{ default: React.ComponentType<SayfaProps> }>;
};

export type GrupTanim = { id: string; etiket: string; sayfalar: SayfaTanim[] };

export const MENU: GrupTanim[] = [
  {
    id: 'genel', etiket: 'Genel bakış', sayfalar: [
      { yol: '', etiket: 'Genel bakış', ikon: LayoutDashboard, oncelik: 'P0', aciklama: 'Sağlık, etkin kullanıcı, bekleyen işler, son denetim kayıtları.', yukle: () => import('./sayfalar/GenelBakis') },
      { yol: 'gelen', etiket: 'Gelen', ikon: Inbox, oncelik: 'P0', aciklama: 'Şikâyet, geri bildirim, tüyo, taslak: tek bekleyen kuyruğu.', v14Slug: 'gelen-kutusu', anahtar: 'bekleyen şikâyet geri bildirim hata gizlilik faz14 tüyo', yukle: () => import('./sayfalar/GelenKutusu') },
    ],
  },
  {
    id: 'icerik', etiket: 'Kurullar ve dersler', sayfalar: [
      { yol: 'icerik/kurullar', etiket: 'Kurullar', ikon: CalendarRange, oncelik: 'P0', aciklama: 'Kurul takvimi ve aktif kurul.', yukle: () => import('./sayfalar/Kurullar') },
      { yol: 'icerik/dersler', etiket: 'Dersler', ikon: BookOpen, oncelik: 'P0', aciklama: 'Ders kayıt defteri ve katman durumu.', yukle: () => import('./sayfalar/Dersler') },
      { yol: 'icerik/branslar', etiket: 'Branşlar', ikon: Layers, oncelik: 'P2', yukle: () => import('./sayfalar/Branslar') },
    ],
  },
  {
    id: 'sorular', etiket: 'Sorular', sayfalar: [
      { yol: 'sorular/havuz', etiket: 'Havuz', ikon: FileQuestion, oncelik: 'P0', v14Slug: 'soru-havuzu', yukle: () => import('./sayfalar/SoruHavuzu') },
      { yol: 'sorular/cikmis', etiket: 'Çıkmış', ikon: History, oncelik: 'P0', v14Slug: 'veri-katalogu', yukle: () => import('./sayfalar/CikmisSorular') },
      { yol: 'sorular/birlesen', etiket: 'Birleşenler', ikon: GitMerge, oncelik: 'P1', v14Slug: 'birlesenler', yukle: () => import('./sayfalar/Birlesenler') },
      { yol: 'sorular/ornek', etiket: 'Örnek sorular', ikon: ListChecks, oncelik: 'P1', v14Slug: 'veri-katalogu', yukle: () => import('./sayfalar/OrnekSorular') },
      { yol: 'sorular/ham', etiket: 'Ham defter', ikon: Archive, oncelik: 'P1', v14Slug: 'ham-havuz', yukle: () => import('./sayfalar/HamDefter') },
      { yol: 'sorular/serbest', etiket: 'Serbest girdiler', ikon: TextCursorInput, oncelik: 'P2', v14Slug: 'serbest-girdiler', yukle: () => import('./sayfalar/SerbestGirdiler') },
      { yol: 'sorular/taslak', etiket: 'Taslaklar', ikon: FilePen, oncelik: 'P2', v14Slug: 'taslaklar', yukle: () => import('./sayfalar/Taslaklar') },
      { yol: 'sorular/dondurma', etiket: 'Havuz dondurma', ikon: Snowflake, oncelik: 'P2', yukle: () => import('./sayfalar/HavuzDondurma') },
      { yol: 'sorular/olasi', etiket: 'Olası sorular', ikon: Sparkles, oncelik: 'P2', yukle: () => import('./sayfalar/OlasiSorular') },
      { yol: 'sorular/sikayet', etiket: 'Soru şikâyetleri', ikon: AlertTriangle, oncelik: 'P0', anahtar: 'hata bildirimi rapor', yukle: () => import('./sayfalar/SoruSikayetleri') },
      { yol: 'sorular/faz14', etiket: 'Faz 14 kuyruğu', ikon: FlaskConical, oncelik: 'P1', anahtar: 'inceleme llm', yukle: () => import('./sayfalar/Faz14Kuyrugu') },
    ],
  },
  {
    id: 'ogrenme', etiket: 'Öğrenme', sayfalar: [
      { yol: 'ogrenme/desteler', etiket: 'Öğren desteleri', ikon: GraduationCap, oncelik: 'P1', v14Slug: 'veri-katalogu', yukle: () => import('./sayfalar/Desteler') },
      { yol: 'ogrenme/sesli', etiket: 'Sesli ders', ikon: Mic, oncelik: 'P1', v14Slug: 'sesli-anlatim', yukle: () => import('./sayfalar/SesliDersler') },
      { yol: 'ogrenme/ses-kuyrugu', etiket: 'Ses kuyruğu', ikon: ListChecks, oncelik: 'P2', anahtar: 'üretim ema xtts iş', yukle: () => import('./sayfalar/SesKuyrugu') },
      { yol: 'ogrenme/onem', etiket: 'Önem ve çözücü', ikon: Star, oncelik: 'P1', yukle: () => import('./sayfalar/OnemCozucu') },
      { yol: 'ogrenme/spot', etiket: 'Sınav spotları', ikon: Target, oncelik: 'P2', yukle: () => import('./sayfalar/Spotlar') },
      { yol: 'ogrenme/kazanim', etiket: 'Kazanımlar', ikon: Award, oncelik: 'P2', v14Slug: 'veri-katalogu', yukle: () => import('./sayfalar/Kazanimlar') },
      { yol: 'ogrenme/kart', etiket: 'Ezber kartları', ikon: CreditCard, oncelik: 'P2', v14Slug: 'veri-katalogu', yukle: () => import('./sayfalar/Kartlar') },
      { yol: 'ogrenme/paket', etiket: 'İçerik paketleri', ikon: Package, oncelik: 'P1', anahtar: 'ders_icerik quiz terim', yukle: () => import('./sayfalar/IcerikPaketleri') },
      { yol: 'ogrenme/kamp', etiket: 'Kamplar', ikon: Tent, oncelik: 'P1', v14Slug: 'kamp-tuyolari', yukle: () => import('./sayfalar/Kamplar') },
    ],
  },
  {
    id: 'kaynak', etiket: 'Kaynaklar', sayfalar: [
      { yol: 'kaynak/sozluk', etiket: 'Sözlük', ikon: BookA, oncelik: 'P1', v14Slug: 'veri-katalogu', anahtar: 'kısaltma terim', yukle: () => import('./sayfalar/Sozluk') },
      { yol: 'kaynak/saglik', etiket: 'Sağlık Bakanlığı', ikon: Landmark, oncelik: 'P2', yukle: () => import('./sayfalar/SaglikBakanligi') },
      { yol: 'kaynak/sinav-dagilimi', etiket: 'Sınav dağılımı', ikon: PieChart, oncelik: 'P2', anahtar: 'baraj 60 plan', yukle: () => import('./sayfalar/SinavDagilimi') },
      { yol: 'kaynak/hastalik', etiket: 'Hastalıklar', ikon: Stethoscope, oncelik: 'P2', v14Slug: 'veri-katalogu', yukle: () => import('./sayfalar/Hastaliklar') },
      { yol: 'kaynak/ozet', etiket: 'Ders özetleri', ikon: FileText, oncelik: 'P2', v14Slug: 'veri-katalogu', yukle: () => import('./sayfalar/Ozetler') },
      { yol: 'kaynak/muzik', etiket: 'Müzik', ikon: Music, oncelik: 'P2', v14Slug: 'veri-katalogu', yukle: () => import('./sayfalar/Muzik') },
      { yol: 'kaynak/cop', etiket: 'Çöp kutusu', ikon: Trash2, oncelik: 'P1', v14Slug: 'veri-katalogu', yukle: () => import('./sayfalar/Cop') },
    ],
  },
  {
    id: 'site', etiket: 'Site', sayfalar: [
      { yol: 'site/gorunurluk', etiket: 'Görünürlük', ikon: Eye, oncelik: 'P0', anahtar: 'gizli kapalı sayfa', yukle: () => import('./sayfalar/SiteGorunurluk') },
      { yol: 'site/menu', etiket: 'Menü', ikon: MenuIcon, oncelik: 'P1', yukle: () => import('./sayfalar/SiteMenu') },
      { yol: 'site/bakim', etiket: 'Bakım', ikon: Construction, oncelik: 'P0', yukle: () => import('./sayfalar/SiteBakim') },
      { yol: 'site/bayraklar', etiket: 'Özellik bayrakları', ikon: Flag, oncelik: 'P1', yukle: () => import('./sayfalar/SiteBayraklar') },
      { yol: 'site/duyurular', etiket: 'Duyurular', ikon: Megaphone, oncelik: 'P1', anahtar: 'bildirim push', yukle: () => import('./sayfalar/SiteDuyurular') },
      { yol: 'site/kanallar', etiket: 'Kanallar', ikon: Radio, oncelik: 'P2', anahtar: 'smtp push e-posta', yukle: () => import('./sayfalar/SiteKanallar') },
      { yol: 'site/surum', etiket: 'Sürüm', ikon: Tag, oncelik: 'P1', anahtar: 'commit dağıtım', yukle: () => import('./sayfalar/SiteSurum') },
    ],
  },
  {
    id: 'kisi', etiket: 'Kullanıcılar', sayfalar: [
      { yol: 'kisi', etiket: 'Kişiler', ikon: Users, oncelik: 'P0', v14Slug: 'kisiler', anahtar: 'kullanıcı öğrenci profil', yukle: () => import('./sayfalar/KisiListe') },
      { yol: 'kisi/erisim', etiket: 'Erişim', ikon: ShieldCheck, oncelik: 'P0', v14Slug: 'kullanicilar', anahtar: 'rol askı moderatör birleştir oturum', yukle: () => import('./sayfalar/KisiErisim') },
      { yol: 'kisi/basarim', etiket: 'Puan ve ATP', ikon: Coins, oncelik: 'P1', v14Slug: 'puan-atp', yukle: () => import('./sayfalar/KisiBasarim') },
      { yol: 'kisi/ilerleme', etiket: 'Ders ilerlemesi', ikon: TrendingUp, oncelik: 'P1', v14Slug: 'ders-ilerlemesi', yukle: () => import('./sayfalar/KisiIlerleme') },
      { yol: 'kisi/gorev', etiket: 'Seri ve görevler', ikon: CalendarCheck, oncelik: 'P2', v14Slug: 'giris-gorev', yukle: () => import('./sayfalar/KisiGorev') },
      { yol: 'kisi/etkinlik', etiket: 'Etkinlik günlüğü', ikon: Activity, oncelik: 'P1', yukle: () => import('./sayfalar/KisiEtkinlik') },
      { yol: 'kisi/gizlilik', etiket: 'Gizlilik talepleri', ikon: Lock, oncelik: 'P2', anahtar: 'kvkk silme dışa aktarma', yukle: () => import('./sayfalar/GizlilikTalepleri') },
    ],
  },
  {
    id: 'topluluk', etiket: 'Topluluk', sayfalar: [
      { yol: 'topluluk/sikayet', etiket: 'Şikâyetler', ikon: AlertTriangle, oncelik: 'P0', v14Slug: 'moderasyon', yukle: () => import('./sayfalar/Sikayetler') },
      { yol: 'topluluk/sohbet', etiket: 'Sohbet odaları', ikon: MessagesSquare, oncelik: 'P0', anahtar: 'oda grup davet kodu', yukle: () => import('./sayfalar/SohbetOdalari') },
      { yol: 'topluluk/mesaj', etiket: 'Mesajlar', ikon: MessageSquare, oncelik: 'P0', yukle: () => import('./sayfalar/Mesajlar') },
      { yol: 'topluluk/kanal', etiket: 'Yorumlar ve kanallar', ikon: Radio, oncelik: 'P1', anahtar: 'yorum kanal moderasyon', yukle: () => import('./sayfalar/Kanallar') },
      { yol: 'topluluk/arkadaslik', etiket: 'Arkadaşlık', ikon: UserPlus, oncelik: 'P2', yukle: () => import('./sayfalar/Arkadaslik') },
      { yol: 'topluluk/not', etiket: 'Paylaşılan notlar', ikon: StickyNote, oncelik: 'P2', yukle: () => import('./sayfalar/PaylasilanNotlar') },
      { yol: 'topluluk/geri-bildirim', etiket: 'Geri bildirim', ikon: MessageCircleHeart, oncelik: 'P1', v14Slug: 'veri-katalogu', anahtar: 'öğren hata bildirimi learn feedback', yukle: () => import('./sayfalar/GeriBildirim') },
    ],
  },
  {
    id: 'oyun', etiket: 'Oyunlar', sayfalar: [
      { yol: 'oyun/odalar', etiket: 'Canlı odalar', ikon: Gamepad2, oncelik: 'P1', yukle: () => import('./sayfalar/OyunOdalar') },
      { yol: 'oyun/kaynak', etiket: 'Soru kaynakları', ikon: Puzzle, oncelik: 'P1', yukle: () => import('./sayfalar/OyunKaynak') },
      { yol: 'oyun/quiz-havuzu', etiket: 'Quiz havuzu', ikon: Database, oncelik: 'P2', yukle: () => import('./sayfalar/QuizHavuzu') },
    ],
  },
  {
    id: 'sistem', etiket: 'Sistem', sayfalar: [
      { yol: 'sistem/saglik', etiket: 'Sağlık', ikon: HeartPulse, oncelik: 'P0', v14Slug: 'sistem', anahtar: 'servis bellek embed sse', yukle: () => import('./sayfalar/Saglik') },
      { yol: 'sistem/llm', etiket: 'LLM işleri', ikon: Bot, oncelik: 'P0', v14Slug: 'bekleyen-islemler', anahtar: 'faz14 onarım kilit', yukle: () => import('./sayfalar/LlmIsleri') },
      { yol: 'sistem/isler', etiket: 'Betikler', ikon: Terminal, oncelik: 'P1', v14Slug: 'betikler', yukle: () => import('./sayfalar/Betikler') },
      { yol: 'sistem/hat', etiket: 'Hat', ikon: GitBranch, oncelik: 'P1', v14Slug: 'hat', anahtar: 'hat.json aşama ders zinciri gece', yukle: () => import('./sayfalar/Hat') },
      { yol: 'sistem/db', etiket: 'Veritabanı gezgini', ikon: Database, oncelik: 'P0', v14Slug: 'veritabani-gezgini', anahtar: 'pg sql tablo', yukle: () => import('./sayfalar/VeritabaniGezgini') },
      { yol: 'sistem/yedek', etiket: 'Yedek', ikon: HardDriveDownload, oncelik: 'P1', v14Slug: 'veritabani', anahtar: 'içe aktar dışa aktar reset tehlikeli', yukle: () => import('./sayfalar/Yedek') },
      { yol: 'sistem/denetim', etiket: 'Denetim kaydı', ikon: ScrollText, oncelik: 'P0', yukle: () => import('./sayfalar/Denetim') },
      { yol: 'sistem/hata', etiket: 'İstemci hataları', ikon: AlertTriangle, oncelik: 'P0', anahtar: 'hata tarayıcı', yukle: () => import('./sayfalar/IstemciHatalari') },
      { yol: 'sistem/dagitim', etiket: 'Dağıtım bilgisi', ikon: Tag, oncelik: 'P1', anahtar: 'commit sürüm onem', yukle: () => import('./sayfalar/Dagitim') },
      { yol: 'sistem/drive', etiket: 'Drive', ikon: CloudCog, oncelik: 'P2', v14Slug: 'otomasyon', anahtar: 'tarama envanter pdf', yukle: () => import('./sayfalar/Drive') },
      { yol: 'sistem/rag', etiket: 'RAG indeksi', ikon: Network, oncelik: 'P2', anahtar: 'vektör bge embed denetle', yukle: () => import('./sayfalar/Rag') },
      { yol: 'sistem/fazlar', etiket: 'Fazlar', ikon: FlaskConical, oncelik: 'P2', v14Slug: 'fazlar', anahtar: 'faz kazanım slayt varlık', yukle: () => import('./sayfalar/Fazlar') },
      { yol: 'sistem/baglanti', etiket: 'Bağlantılar', ikon: Link2, oncelik: 'P2', v14Slug: 'kisayollar', anahtar: 'ders çıkmış terim slayt öğren bağ', yukle: () => import('./sayfalar/Baglantilar') },
    ],
  },
];

export const TUM_SAYFALAR: (SayfaTanim & { grup: GrupTanim })[] = MENU.flatMap((g) => g.sayfalar.map((s) => ({ ...s, grup: g })));

/** Eski v14 adresleri → yeni yol (kalan alt parçalar korunur: kisiler/<k> → kisi/<k>) */
export const ESKI_ADRES: Record<string, string> = {
  'genel-bakis': '',
  'gelen-kutusu': 'gelen',
  'bekleyen-islemler': 'sistem/llm',
  moderasyon: 'topluluk/sikayet',
  'soru-havuzu': 'sorular/havuz',
  'veri-katalogu': 'sorular/cikmis',
  'tum-veriler': 'sorular/cikmis',
  fazlar: 'sistem/fazlar',
  'sesli-anlatim': 'ogrenme/sesli',
  'yeni-dersler': 'icerik/dersler',
  'kamp-tuyolari': 'ogrenme/kamp',
  'ham-havuz': 'sorular/ham',
  birlesenler: 'sorular/birlesen',
  'veri-merkezi': '',
  notebooklm: 'sistem/isler',
  'serbest-girdiler': 'sorular/serbest',
  taslaklar: 'sorular/taslak',
  studyo: 'sorular/taslak',
  'puan-atp': 'kisi/basarim',
  kisiler: 'kisi',
  'giris-gorev': 'kisi/gorev',
  'ders-ilerlemesi': 'kisi/ilerleme',
  kullanicilar: 'kisi/erisim',
  betikler: 'sistem/isler',
  sistem: 'sistem/saglik',
  otomasyon: 'sistem/drive',
  hat: 'sistem/hat',
  'veritabani-gezgini': 'sistem/db',
  kisayollar: 'sistem/baglanti',
  veritabani: 'sistem/yedek',
};

export type Cozum = { sayfa: SayfaTanim & { grup: GrupTanim }; altYol: string[]; yonlendir?: string };

/** /manage sonrası yolu çözer. Eski adresse yonlendir doludur (history.replaceState ile yeni adrese geçin). */
export function adresCoz(pathname: string): Cozum {
  const parcalar = pathname.replace(/^\/(manage|yonetim)\/?/, '').split('/').filter(Boolean).map((p) => decodeURIComponent(p));
  // Eski adres: ilk parça bir grup adı ya da yeni sayfa yolu değilse (ör. 'sistem' artık grup) — tek adım, özyineleme yok
  const grupMu = (x: string) => MENU.some((g) => g.id === x) || TUM_SAYFALAR.some((s) => s.yol === x);
  if (parcalar.length && Object.prototype.hasOwnProperty.call(ESKI_ADRES, parcalar[0]) && !grupMu(parcalar[0])) {
    const hedef = [ESKI_ADRES[parcalar[0]], ...parcalar.slice(1)].filter(Boolean).join('/');
    return { ...adresCoz(`/manage/${hedef}`), yonlendir: hedef };
  }
  let en: (SayfaTanim & { grup: GrupTanim }) | null = null;
  let enUzun = -1;
  for (const s of TUM_SAYFALAR) {
    const sp = s.yol ? s.yol.split('/') : [];
    if (sp.length <= parcalar.length && sp.every((x, i) => x === parcalar[i]) && sp.length > enUzun) { en = s; enUzun = sp.length; }
  }
  // Grup adı tek başına (/manage/sistem) → grubun ilk sayfası
  if (en && en.yol === '' && parcalar.length) {
    const g = MENU.find((x) => x.id === parcalar[0]);
    if (g && parcalar.length === 1) return { sayfa: TUM_SAYFALAR.find((s) => s.yol === g.sayfalar[0].yol)!, altYol: [], yonlendir: g.sayfalar[0].yol };
  }
  return { sayfa: en || TUM_SAYFALAR[0], altYol: parcalar.slice(Math.max(0, enUzun)) };
}

export const manageAdres = (yol: string) => `/manage${yol ? `/${yol.replace(/^\/+/, '')}` : ''}`;
