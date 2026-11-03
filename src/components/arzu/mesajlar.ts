/**
 * Arzu'ya notlar: sayfaya ve saate göre seçilen kısa, sade cümleler. Günlük konuşma Türkçesi; abartı ve klişe yok.
 */
import type { AppRoute } from '../../router';

export type Fisilti = { metin: string };

const GENEL: string[] = [
  'Seni seviyorum Arzu. Bugün de, yarın da.',
  'Çalışırken bile aklımdasın.',
  'Yorulduysan biraz ara ver, acelesi yok.',
  'Su içmeyi unutma.',
  'Bugün bir şeyler yedin mi?',
  'Gözlerin yorulduysa bir dakika kapat.',
  'İyi ki varsın.',
  'Bugün nasıl geçiyor? Merak ediyorum.',
  'Küçük bir not: seni seviyorum.',
  'Zorlandığında bana yaz, birlikte bakarız.',
  'Biraz gerin, omuzlarını indir.',
  'Bitirince haber ver, seni dinlemek istiyorum.',
];

const DERS: string[] = [
  'Bu ders bitince biraz dinlen.',
  'Her ders bir adım. Seninle gurur duyuyorum.',
  'Anlamadığın yer olursa not al, sonra birlikte bakarız.',
  'Bir konu bittiyse kısa bir mola iyi gelir.',
  'Zor konu olabilir, takılma; yavaş yavaş oturur.',
];

const SORU: string[] = [
  'Yanlış yaptıysan dert etme; şimdi öğrenmek sınavda öğrenmekten iyi.',
  'Bir soru daha bitti. Aferin.',
  'Acele etme, soruyu sonuna kadar oku.',
  'Çeldiriciye takılma, bildiğin gibi çöz.',
  'Doğru sayısından çok ne öğrendiğin önemli.',
];

const BUGUN: string[] = [
  'Bugün iyi geçsin. İyi ki varsın.',
  'Program ne kadar dolu olursa olsun kendine de zaman ayır.',
  'Önce kahvaltı, sonra ders.',
];

const SIRALAMA: string[] = [
  'Sıralamaya çok takılma, kendi hızında ilerliyorsun.',
  'Puanlar iner çıkar, sen yoluna bak.',
];

const AYAR: string[] = [
  'Temayı gözünü en az yoran şekilde seç.',
  'Yazıyı büyütürsen gözlerin daha az yorulur.',
];

const MUZIK: string[] = [
  'Müzik açıp biraz dinlen.',
  'Bana da bir şarkı önerirsin, merak ettim.',
];

const NOT: string[] = [
  'Notlarını okumayı seviyorum.',
  'Buraya bir not da benden: seni seviyorum.',
];

const SAAT = {
  sabah: ['Günaydın Arzu.', 'Günaydın. Kahvaltı yapmadan başlama.'],
  ogle: ['Yemek yedin mi?', 'Öğle oldu, biraz ayağa kalk.'],
  aksam: ['Bugün yine çok çalıştın. Seninle gurur duyuyorum.', 'Akşam oldu, biraz dinlen.'],
  gece: ['Saat geç oldu. Uyumayı unutma.', 'Bu saatte hâlâ çalışıyorsun; yarın da var, dinlen artık.'],
};

const DERS_ROTALARI: AppRoute[] = ['study', 'learn', 'canli_ders', 'summaries', 'spots', 'flashcards', 'glossary', 'kazanimlar', 'oncelikli_dersler', 'diseases', 'booklet', 'transcripts'];
const SORU_ROTALARI: AppRoute[] = ['questions', 'practice', 'past_exams', 'ornek_sorular', 'soru_cozucu', 'cikmis_cozucu', 'test_cikmis', 'quick_add', 'matrix', 'son_prova', 'sinav_calisma', 'alternatif_cozucu'];

export function saatDilimi(d = new Date()): keyof typeof SAAT {
  const h = d.getHours();
  if (h >= 5 && h < 11) return 'sabah';
  if (h >= 11 && h < 17) return 'ogle';
  if (h >= 17 && h < 22) return 'aksam';
  return 'gece';
}

function havuz(rota: AppRoute | null | undefined): string[] {
  if (!rota) return GENEL;
  if (DERS_ROTALARI.includes(rota)) return DERS;
  if (SORU_ROTALARI.includes(rota)) return SORU;
  if (rota === 'today') return BUGUN;
  if (rota === 'leaderboard' || rota === 'stats') return SIRALAMA;
  if (rota === 'settings') return AYAR;
  if (rota === 'music') return MUZIK;
  if (rota === 'notes') return NOT;
  return GENEL;
}

let sonlar: string[] = [];
function sec(liste: string[]): string {
  const aday = liste.filter((m) => !sonlar.includes(m));
  const l = aday.length ? aday : liste;
  const m = l[Math.floor(Math.random() * l.length)];
  sonlar = [...sonlar.slice(-7), m];
  return m;
}

/** Sayfaya uygun bir not; üç seferde bir genel havuzdan, ara sıra saat dilimine göre. */
export function fisiltiSec(rota: AppRoute | null | undefined, sayac: number): Fisilti {
  if (Math.random() < 0.2) return { metin: sec(SAAT[saatDilimi()]) };
  const liste = sayac % 3 === 2 ? GENEL : havuz(rota);
  return { metin: sec(liste) };
}

/** Karşılama ekranındaki günün cümlesi (güne göre sabit: aynı gün aynı cümle). */
export function gununCumlesi(d = new Date()): string {
  const hepsi = [...GENEL, ...DERS, ...BUGUN];
  const gun = Math.floor(d.getTime() / 86_400_000);
  return hepsi[gun % hepsi.length];
}

export function karsilamaSelam(d = new Date()): string {
  switch (saatDilimi(d)) {
    case 'sabah': return 'Günaydın';
    case 'ogle': return 'İyi günler';
    case 'aksam': return 'İyi akşamlar';
    default: return 'İyi geceler';
  }
}
