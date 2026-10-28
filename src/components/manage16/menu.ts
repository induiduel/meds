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
      { yol: 'gelen', etiket: 'Gelen', ikon: Inbox, oncelik: 'P0', aciklama: 'Şikâyet, geri bildirim, tüyo, taslak: tek bekleyen kuyruğu.', v14Slug: 'gelen-kutusu' },
    ],
  },
  {
    id: 'icerik', etiket: 'Kurullar ve dersler', sayfalar: [
      { yol: 'icerik/kurullar', etiket: 'Kurullar', ikon: CalendarRange, oncelik: 'P0', aciklama: 'Kurul takvimi ve aktif kurul.' },
      { yol: 'icerik/dersler', etiket: 'Dersler', ikon: BookOpen, oncelik: 'P0', aciklama: 'Ders kayıt defteri ve katman durumu.' },
      { yol: 'icerik/branslar', etiket: 'Branşlar', ikon: Layers, oncelik: 'P2' },
    ],
  },
  {
    id: 'sorular', etiket: 'Sorular', sayfalar: [
      { yol: 'sorular/havuz', etiket: 'Havuz', ikon: FileQuestion, oncelik: 'P0', v14Slug: 'soru-havuzu' },
      { yol: 'sorular/cikmis', etiket: 'Çıkmış', ikon: History, oncelik: 'P0', v14Slug: 'veri-katalogu' },
      { yol: 'sorular/birlesen', etiket: 'Birleşenler', ikon: GitMerge, oncelik: 'P1', v14Slug: 'birlesenler' },
      { yol: 'sorular/ornek', etiket: 'Örnek sorular', ikon: ListChecks, oncelik: 'P1', v14Slug: 'veri-katalogu' },
      { yol: 'sorular/ham', etiket: 'Ham defter', ikon: Archive, oncelik: 'P1', v14Slug: 'ham-havuz' },
      { yol: 'sorular/serbest', etiket: 'Serbest girdiler', ikon: TextCursorInput, oncelik: 'P2', v14Slug: 'serbest-girdiler' },
      { yol: 'sorular/taslak', etiket: 'Taslaklar', ikon: FilePen, oncelik: 'P2', v14Slug: 'taslaklar' },
      { yol: 'sorular/dondurma', etiket: 'Havuz dondurma', ikon: Snowflake, oncelik: 'P2' },
      { yol: 'sorular/olasi', etiket: 'Olası sorular', ikon: Sparkles, oncelik: 'P2' },
    ],
  },
  {
    id: 'ogrenme', etiket: 'Öğrenme', sayfalar: [
      { yol: 'ogrenme/desteler', etiket: 'Öğren desteleri', ikon: GraduationCap, oncelik: 'P1', v14Slug: 'veri-katalogu' },
      { yol: 'ogrenme/sesli', etiket: 'Sesli ders', ikon: Mic, oncelik: 'P1', v14Slug: 'sesli-anlatim' },
      { yol: 'ogrenme/onem', etiket: 'Önem ve çözücü', ikon: Star, oncelik: 'P1' },
      { yol: 'ogrenme/spot', etiket: 'Sınav spotları', ikon: Target, oncelik: 'P2' },
      { yol: 'ogrenme/kazanim', etiket: 'Kazanımlar', ikon: Award, oncelik: 'P2', v14Slug: 'veri-katalogu' },
      { yol: 'ogrenme/kart', etiket: 'Ezber kartları', ikon: CreditCard, oncelik: 'P2', v14Slug: 'veri-katalogu' },
      { yol: 'ogrenme/kamp', etiket: 'Kamplar', ikon: Tent, oncelik: 'P1', v14Slug: 'kamp-tuyolari' },
    ],
  },
  {
    id: 'kaynak', etiket: 'Kaynaklar', sayfalar: [
      { yol: 'kaynak/sozluk', etiket: 'Sözlük', ikon: BookA, oncelik: 'P1', v14Slug: 'veri-katalogu', anahtar: 'kısaltma terim' },
      { yol: 'kaynak/hastalik', etiket: 'Hastalıklar', ikon: Stethoscope, oncelik: 'P2', v14Slug: 'veri-katalogu' },
      { yol: 'kaynak/ozet', etiket: 'Ders özetleri', ikon: FileText, oncelik: 'P2', v14Slug: 'veri-katalogu' },
      { yol: 'kaynak/muzik', etiket: 'Müzik', ikon: Music, oncelik: 'P2', v14Slug: 'veri-katalogu' },
      { yol: 'kaynak/cop', etiket: 'Çöp kutusu', ikon: Trash2, oncelik: 'P1', v14Slug: 'veri-katalogu' },
    ],
  },
  {
    id: 'site', etiket: 'Site', sayfalar: [
      { yol: 'site/gorunurluk', etiket: 'Görünürlük', ikon: Eye, oncelik: 'P0', anahtar: 'gizli kapalı sayfa' },
      { yol: 'site/menu', etiket: 'Menü', ikon: MenuIcon, oncelik: 'P1' },
      { yol: 'site/bakim', etiket: 'Bakım', ikon: Construction, oncelik: 'P0' },
      { yol: 'site/bayraklar', etiket: 'Özellik bayrakları', ikon: Flag, oncelik: 'P1' },
      { yol: 'site/duyurular', etiket: 'Duyurular', ikon: Megaphone, oncelik: 'P1', anahtar: 'bildirim push' },
      { yol: 'site/kanallar', etiket: 'Kanallar', ikon: Radio, oncelik: 'P2', anahtar: 'smtp whatsapp e-posta' },
      { yol: 'site/surum', etiket: 'Sürüm', ikon: Tag, oncelik: 'P1', anahtar: 'commit dağıtım' },
    ],
  },
  {
    id: 'kisi', etiket: 'Kullanıcılar', sayfalar: [
      { yol: 'kisi', etiket: 'Kişiler', ikon: Users, oncelik: 'P0', v14Slug: 'kisiler', anahtar: 'kullanıcı öğrenci profil' },
      { yol: 'kisi/erisim', etiket: 'Erişim', ikon: ShieldCheck, oncelik: 'P0', v14Slug: 'kullanicilar', anahtar: 'rol askı moderatör birleştir' },
      { yol: 'kisi/basarim', etiket: 'Puan ve ATP', ikon: Coins, oncelik: 'P1', v14Slug: 'puan-atp' },
      { yol: 'kisi/ilerleme', etiket: 'Ders ilerlemesi', ikon: TrendingUp, oncelik: 'P1', v14Slug: 'ders-ilerlemesi' },
      { yol: 'kisi/gorev', etiket: 'Seri ve görevler', ikon: CalendarCheck, oncelik: 'P2', v14Slug: 'giris-gorev' },
      { yol: 'kisi/etkinlik', etiket: 'Etkinlik günlüğü', ikon: Activity, oncelik: 'P1' },
      { yol: 'kisi/gizlilik', etiket: 'Gizlilik talepleri', ikon: Lock, oncelik: 'P2' },
    ],
  },
  {
    id: 'topluluk', etiket: 'Topluluk', sayfalar: [
      { yol: 'topluluk/sikayet', etiket: 'Şikâyetler', ikon: AlertTriangle, oncelik: 'P0', v14Slug: 'moderasyon' },
      { yol: 'topluluk/sohbet', etiket: 'Sohbet odaları', ikon: MessagesSquare, oncelik: 'P0' },
      { yol: 'topluluk/mesaj', etiket: 'Mesajlar', ikon: MessageSquare, oncelik: 'P0' },
      { yol: 'topluluk/arkadaslik', etiket: 'Arkadaşlık', ikon: UserPlus, oncelik: 'P2' },
      { yol: 'topluluk/not', etiket: 'Paylaşılan notlar', ikon: StickyNote, oncelik: 'P2' },
      { yol: 'topluluk/geri-bildirim', etiket: 'Geri bildirim', ikon: MessageCircleHeart, oncelik: 'P1', v14Slug: 'veri-katalogu' },
    ],
  },
  {
    id: 'oyun', etiket: 'Oyunlar', sayfalar: [
      { yol: 'oyun/odalar', etiket: 'Canlı odalar', ikon: Gamepad2, oncelik: 'P1' },
      { yol: 'oyun/kaynak', etiket: 'Soru kaynakları', ikon: Puzzle, oncelik: 'P1' },
      { yol: 'oyun/quiz-havuzu', etiket: 'Quiz havuzu', ikon: Database, oncelik: 'P2' },
    ],
  },
  {
    id: 'sistem', etiket: 'Sistem', sayfalar: [
      { yol: 'sistem/saglik', etiket: 'Sağlık', ikon: HeartPulse, oncelik: 'P0', v14Slug: 'sistem' },
      { yol: 'sistem/llm', etiket: 'LLM işleri', ikon: Bot, oncelik: 'P0', v14Slug: 'bekleyen-islemler', anahtar: 'faz14 onarım kilit' },
      { yol: 'sistem/isler', etiket: 'Betikler', ikon: Terminal, oncelik: 'P1', v14Slug: 'betikler' },
      { yol: 'sistem/hat', etiket: 'Hat', ikon: GitBranch, oncelik: 'P1', v14Slug: 'hat' },
      { yol: 'sistem/db', etiket: 'Veritabanı gezgini', ikon: Database, oncelik: 'P0', v14Slug: 'veritabani-gezgini' },
      { yol: 'sistem/yedek', etiket: 'Yedek', ikon: HardDriveDownload, oncelik: 'P1', v14Slug: 'veritabani' },
      { yol: 'sistem/denetim', etiket: 'Denetim kaydı', ikon: ScrollText, oncelik: 'P0', yukle: () => import('./sayfalar/Denetim') },
      { yol: 'sistem/drive', etiket: 'Drive', ikon: CloudCog, oncelik: 'P2', v14Slug: 'otomasyon' },
      { yol: 'sistem/rag', etiket: 'RAG indeksi', ikon: Network, oncelik: 'P2' },
      { yol: 'sistem/fazlar', etiket: 'Fazlar', ikon: FlaskConical, oncelik: 'P2', v14Slug: 'fazlar' },
      { yol: 'sistem/baglanti', etiket: 'Bağlantılar', ikon: Link2, oncelik: 'P2', v14Slug: 'kisayollar' },
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
