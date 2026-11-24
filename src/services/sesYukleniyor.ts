// Ses yükleniyor göstergesi (2026-11-24).
// Belirti: örnek soru çözücü, sesli ders, terim sesi vb. ses dosyası henüz inmeden oynatılınca
// sessizlik oluyor; öğrenci "ses yok" sanıyordu. Kök: her oynatıcı kendi Audio'sunu açıyor ve
// hiçbiri yüklenme/arabellek durumunu göstermiyordu. Çözüm: tek yerden HTMLAudioElement.play
// sarılır; ses çalmaya başlayana kadar (ve takılıp arabelleğe alınırken) küçük bir
// "Ses yükleniyor…" ibaresi gösterilir. Tüm sesli işlevleri kapsar, bileşen değişikliği gerekmez.

const bekleyen = new Set<HTMLMediaElement>();
let kutu: HTMLDivElement | null = null;
let gosterZamani: ReturnType<typeof setTimeout> | null = null;

function kutuyuKur(): HTMLDivElement {
  if (kutu) return kutu;
  const el = document.createElement('div');
  el.className = 'ses-yukleniyor';
  el.setAttribute('role', 'status');
  el.setAttribute('aria-live', 'polite');
  el.innerHTML = '<span class="ses-yukleniyor__donen" aria-hidden="true"></span><span>Ses yükleniyor…</span>';
  document.body.appendChild(el);
  kutu = el;
  return el;
}

function guncelle() {
  if (bekleyen.size > 0) {
    // Önbellekteki seslerde yanıp sönmesin: kısa gecikmeyle göster.
    if (gosterZamani || kutu?.classList.contains('gorunur')) return;
    gosterZamani = setTimeout(() => {
      gosterZamani = null;
      if (bekleyen.size > 0) kutuyuKur().classList.add('gorunur');
    }, 250);
  } else {
    if (gosterZamani) { clearTimeout(gosterZamani); gosterZamani = null; }
    kutu?.classList.remove('gorunur');
  }
}

const izlenen = new WeakSet<HTMLMediaElement>();

function izle(a: HTMLMediaElement) {
  if (izlenen.has(a)) return;
  izlenen.add(a);
  const bitti = () => { bekleyen.delete(a); guncelle(); };
  const bekliyor = () => { if (!a.paused) { bekleyen.add(a); guncelle(); } };
  a.addEventListener('playing', bitti);
  a.addEventListener('pause', bitti);
  a.addEventListener('ended', bitti);
  a.addEventListener('error', bitti);
  a.addEventListener('abort', bitti);
  a.addEventListener('emptied', bitti);
  a.addEventListener('waiting', bekliyor);
}

export function installSesYukleniyor() {
  if (typeof window === 'undefined' || (window as any).__sesYukleniyor) return;
  (window as any).__sesYukleniyor = true;
  const asil = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function (this: HTMLMediaElement) {
    if (this instanceof HTMLAudioElement) {
      izle(this);
      if (this.readyState < 3) { bekleyen.add(this); guncelle(); }
    }
    const s = asil.call(this);
    if (s && typeof (s as Promise<void>).catch === 'function') {
      (s as Promise<void>).catch(() => { bekleyen.delete(this); guncelle(); });
    }
    return s;
  };
}
