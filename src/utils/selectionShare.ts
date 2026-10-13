/**
 * Seçili metni derin bağlantıyla paylaş (v10).
 *
 * Kullanıcı sayfa içeriğinde (`.sh-main`) bir metin seçince küçük bir çubuk çıkar: "Paylaş" ve "Bağlantıyı kopyala".
 * Bağlantı, bulunulan sayfanın adresine `?vurgu=<seçimin başı>` ekler ve tarayıcının yerel metin parçası
 * (`#:~:text=`) sözdizimini de taşır. Bağlantı açıldığında:
 *  - Chromium tabanlı tarayıcılar yerel parçayla zaten kayar;
 *  - her tarayıcıda bu modül `vurgu` parametresini okur, içerik yüklenene kadar (en çok 10 sn) metni arar,
 *    bulunca görünür alanın ortasına kaydırır ve 3 sn vurgular (CSS Highlight API ya da geçici işaret).
 * Telefonda çubuk alt gezinmenin hemen üstünde sabit durur (sistem seçim menüsüyle çakışmaz);
 * geniş ekranda seçimin üstünde açılır. Stil: styles/layout-modes.css (.ss-*).
 */
import { toast } from '../components/ui/Toast';

const PARAM = 'vurgu';
const MIN = 6;
const MAX = 600;
let installed = false;

const norm = (s: string) => s.replace(/\s+/g, ' ').trim();

/** Seçimden paylaşılacak adres: ?vurgu= + yerel metin parçası */
export function buildDeepLink(text: string): string {
  const clean = norm(text);
  const url = new URL(window.location.href);
  url.searchParams.set(PARAM, clean.slice(0, 160));
  const words = clean.split(' ');
  const enc = (s: string) => encodeURIComponent(s).replace(/-/g, '%2D').replace(/,/g, '%2C');
  const frag = words.length > 10 ? `${enc(words.slice(0, 5).join(' '))},${enc(words.slice(-5).join(' '))}` : enc(clean);
  url.hash = `:~:text=${frag}`;
  return url.toString();
}

function selectionText(): { text: string; rect: DOMRect | null } | null {
  const sel = window.getSelection();
  if (!sel || sel.isCollapsed || sel.rangeCount === 0) return null;
  const range = sel.getRangeAt(0);
  const host = (range.commonAncestorContainer.nodeType === 1 ? range.commonAncestorContainer : range.commonAncestorContainer.parentElement) as Element | null;
  if (!host?.closest('.sh-main') || host.closest('input, textarea, [contenteditable="true"], .ss-bar')) return null;
  const text = norm(sel.toString());
  if (text.length < MIN || text.length > MAX) return null;
  return { text, rect: range.getBoundingClientRect() };
}

async function share(text: string) {
  const url = buildDeepLink(text);
  const snippet = text.length > 140 ? `${text.slice(0, 137)}…` : text;
  const nav = navigator as Navigator & { share?: (d: ShareData) => Promise<void> };
  if (nav.share) {
    try {
      await nav.share({ title: document.title, text: `“${snippet}”`, url });
      return;
    } catch (e) {
      if ((e as DOMException)?.name === 'AbortError') return;
    }
  }
  await copy(url);
}

async function copy(url: string) {
  try {
    await navigator.clipboard.writeText(url);
    toast.success('Bağlantı kopyalandı', 'Açan kişi doğrudan seçtiğin yere gider.');
  } catch {
    toast.info('Bağlantı', url);
  }
}

function makeBar() {
  const bar = document.createElement('div');
  bar.className = 'ss-bar';
  bar.setAttribute('role', 'toolbar');
  bar.setAttribute('aria-label', 'Seçili metin');
  bar.hidden = true;
  bar.innerHTML = `
    <button type="button" data-a="share" class="is-primary"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12M7 8l5-5 5 5M5 14v6h14v-6"/></svg>Paylaş</button>
    <button type="button" data-a="copy"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4 4 0 0 0 6 0l3-3a4 4 0 0 0-6-6l-1 1M14 10a4 4 0 0 0-6 0l-3 3a4 4 0 0 0 6 6l1-1"/></svg>Bağlantı</button>
    <button type="button" data-a="close" aria-label="Kapat" class="is-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button>`;
  document.body.appendChild(bar);
  return bar;
}

/** `?vurgu=` ile gelen sayfada metni bul, kaydır, vurgula */
function findAndHighlight(needle: string): boolean {
  const root = document.querySelector('.sh-main');
  if (!root) return false;
  const target = norm(needle).toLocaleLowerCase('tr-TR');
  if (target.length < MIN) return false;
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode: (n) => (n.parentElement?.closest('script, style, .ss-bar') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT),
  });
  // Boşlukları tek boşluğa indirgeyerek düz metin + (düğüm, konum) eşlemesi kur
  let flat = '';
  const map: { node: Text; off: number }[] = [];
  let prevSpace = true;
  for (let n = walker.nextNode() as Text | null; n; n = walker.nextNode() as Text | null) {
    const t = n.data;
    for (let i = 0; i < t.length; i++) {
      const isSpace = /\s/.test(t[i]);
      if (isSpace) {
        if (prevSpace) continue;
        flat += ' ';
      } else flat += t[i];
      map.push({ node: n, off: i });
      prevSpace = isSpace;
    }
    if (!prevSpace) { flat += ' '; map.push({ node: n, off: t.length }); prevSpace = true; }
  }
  const idx = flat.toLocaleLowerCase('tr-TR').indexOf(target);
  if (idx < 0) return false;
  const a = map[idx];
  const b = map[Math.min(idx + target.length - 1, map.length - 1)];
  const range = document.createRange();
  range.setStart(a.node, a.off);
  range.setEnd(b.node, Math.min(b.off + 1, b.node.data.length));
  const rect = range.getBoundingClientRect();
  const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  window.scrollTo({ top: Math.max(0, window.scrollY + rect.top - window.innerHeight / 2 + rect.height / 2), behavior: reduce ? 'auto' : 'smooth' });
  const H = (window as unknown as { Highlight?: new (...r: Range[]) => unknown }).Highlight;
  const reg = (CSS as unknown as { highlights?: Map<string, unknown> }).highlights;
  if (H && reg) {
    reg.set('ss-vurgu', new H(range));
    window.setTimeout(() => reg.delete('ss-vurgu'), 3500);
  } else {
    // Yedek: seçim olarak göster (tek düğüm dışına taşan aralıklarda da çalışır)
    const sel = window.getSelection();
    sel?.removeAllRanges();
    sel?.addRange(range);
    window.setTimeout(() => sel?.removeAllRanges(), 3500);
  }
  return true;
}

/** Parametre kurulumda (React yönlendiricisi adresi yeniden yazmadan önce) okunur. */
function handleIncoming(needle: string | null) {
  if (!needle) return;
  const started = Date.now();
  let done = false;
  const finish = () => {
    done = true;
    obs.disconnect();
    // Yeniden yüklemede tekrar kaydırmasın: parametre ve parça adresten silinir
    const url = new URL(window.location.href);
    if (url.searchParams.has(PARAM) || url.hash.startsWith('#:~:')) {
      url.searchParams.delete(PARAM);
      window.history.replaceState(window.history.state, '', url.pathname + url.search);
    }
  };
  const attempt = () => {
    if (done) return;
    if (findAndHighlight(needle)) finish();
    else if (Date.now() - started > 10000) finish();
  };
  let t = 0;
  const obs = new MutationObserver(() => {
    window.clearTimeout(t);
    t = window.setTimeout(attempt, 250);
  });
  obs.observe(document.body, { childList: true, subtree: true });
  window.setTimeout(attempt, 600);
  window.setTimeout(attempt, 10100);
}

export function installSelectionShare() {
  if (installed || typeof document === 'undefined') return;
  installed = true;
  const bar = makeBar();
  let current = '';
  const coarse = window.matchMedia('(pointer: coarse)');
  let timer = 0;
  const place = () => {
    const s = selectionText();
    if (!s) { bar.hidden = true; current = ''; return; }
    current = s.text;
    bar.hidden = false;
    if (coarse.matches || !s.rect) {
      bar.classList.add('is-dock');
      bar.style.left = bar.style.top = '';
    } else {
      bar.classList.remove('is-dock');
      const w = bar.offsetWidth || 220;
      const x = Math.min(Math.max(8, s.rect.left + s.rect.width / 2 - w / 2), window.innerWidth - w - 8);
      const above = s.rect.top - 48;
      bar.style.left = `${x}px`;
      bar.style.top = `${above > 60 ? above : s.rect.bottom + 8}px`;
    }
  };
  // Seçim tutamaçları sürüklenirken her olayda ölçme: durulunca bir kez yerleştir
  document.addEventListener('selectionchange', () => {
    window.clearTimeout(timer);
    timer = window.setTimeout(() => requestAnimationFrame(place), 220);
  });
  window.addEventListener('scroll', () => { if (!bar.hidden && !bar.classList.contains('is-dock')) bar.hidden = true; }, { passive: true });
  // Düğmeye basınca seçim kaybolmasın
  bar.addEventListener('mousedown', (e) => e.preventDefault());
  bar.addEventListener('click', (e) => {
    const a = (e.target as Element).closest('button')?.getAttribute('data-a');
    if (!a) return;
    const text = current;
    if (a === 'close' || !text) { bar.hidden = true; window.getSelection()?.removeAllRanges(); return; }
    if (a === 'share') void share(text);
    if (a === 'copy') void copy(buildDeepLink(text));
    bar.hidden = true;
  });
  const needle = new URL(window.location.href).searchParams.get(PARAM);
  if (needle) {
    if (document.readyState === 'complete') handleIncoming(needle);
    else window.addEventListener('load', () => handleIncoming(needle), { once: true });
  }
}
