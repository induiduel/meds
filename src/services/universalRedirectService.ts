/**
 * src/services/universalRedirectService.ts
 *
 * Evrensel Derin Bağlantı (Deep Linking) ve Metin Vurgulama Servisi
 *
 * Sitedeki HER BİR:
 * - Çıkmış soruya ve havuz sorusuna (`past_question`, `practice_question`)
 * - Soru şıklarına (`option`: A, B, C, D, E)
 * - Soru köküne ve metinlerine (`stem`, `text`, `paragraph`)
 * - Yorumlara (`comment`)
 * - Açıklamalara (`explanation`, `reconstruction`, `audit`)
 * - Sınav spotu ve klinik uyarılara (`spot`, `pearl`, `warning`)
 * - İnteraktif tablolara (`table`, `interactive_table`, `venn_grid`)
 * - Terimlere ve sözlük verilerine (`term`, `glossary`, `encyclopedia`)
 * - Terim açıklamalarına (tanım, mekanizma, ayırıcı tanı vb.)
 * - Akıl kartlarına (`flashcard`)
 *
 * doğrudan erişim sağlayan akıllı URL'ler üretir, paylaşır ve sayfada hedef
 * ögeye yumuşakça odaklanıp 1-2 kez parıldayan nefes alan bir vurgu (fade highlight)
 * animasyonuyla gösterir.
 */

import { icKonum, icUrl } from '../siteHaritasi';
import { toast } from '../components/ui/Toast';
import { navigateTo } from '../router';

const APP_HOST_RE = /(^|\.)nofrostlife\.com\.tr$/i;

/**
 * Bildirim / paylaşım bağlantısını sayfayı yenilemeden açar: adres yazılır, App popstate ile rotayı kurar,
 * initDeepLinkAutoScroll hedef öğe çizilince ona kaydırıp vurgular. nofrostlife.com.tr bağlantıları
 * (push ve e-posta mutlak adres taşır) hangi hostta açılırsa açılsın bu uygulamanın yoluna çevrilir.
 */
export function openDeepLink(url: string): void {
  if (!url || typeof window === 'undefined') return;
  try {
    const u = new URL(url, window.location.origin);
    if (u.origin !== window.location.origin && !APP_HOST_RE.test(u.hostname)) {
      window.open(u.href, '_blank', 'noopener');
      return;
    }
    navigateTo(u.pathname + u.search + u.hash);
  } catch {
    window.location.assign(url);
  }
}

/** Mutlak bildirim adresinden bu sitenin yolunu çıkarır (bağlantı href'i için); dış adreste null. */
export function inAppPath(url?: string): string | null {
  if (!url || typeof window === 'undefined') return null;
  try {
    const u = new URL(url, window.location.origin);
    if (u.origin !== window.location.origin && !APP_HOST_RE.test(u.hostname)) return null;
    return u.pathname + u.search + u.hash;
  } catch {
    return null;
  }
}

export type UniversalReportType =
  | 'past_question'
  | 'practice_question'
  | 'pool_question'
  | 'interactive_deck'
  | 'learn_slide'
  | 'interactive_element'
  | 'table'
  | 'term'
  | 'disease'
  | 'flashcard'
  | 'spot'
  | 'lecture_summary'
  | 'lecture_note'
  | 'comment'
  | 'explanation'
  | 'option';

export interface DeepLinkTarget {
  type: UniversalReportType;
  id?: string;
  targetId?: string;
  committeeId?: string;
  subTarget?: string | {
    slideNumber?: number;
    targetKey?: string;
    elementKey?: string;
    tableId?: string;
    termId?: string;
    diseaseId?: string;
    cardId?: string;
    commentId?: string;
    pageNumber?: number;
    optionKey?: string; // 'A' | 'B' | 'C' | 'D' | 'E'
    section?: 'stem' | 'explanation' | 'comments' | 'definition' | 'mechanism' | 'differential' | 'pearls' | 'table' | 'treatment' | 'diagnosis' | 'etiology' | 'pathology' | 'symptoms';
  };
  highlightText?: string;
  title?: string;
}

export type UniversalReportTarget = DeepLinkTarget;

/**
 * Derin bağlantı (Deep Link) URL'i üretir.
 * Hem modern Text-Fragments (#:~:text=...) hem de URL query parametreleri ve hash desteği içerir.
 */
export function buildDeepLinkUrl(target: DeepLinkTarget): string {
  const { type, subTarget, highlightText } = target;
  const targetId = target.targetId || target.id || '';
  const subObj = typeof subTarget === 'object' && subTarget !== null ? subTarget : undefined;
  const subStr = typeof subTarget === 'string' ? subTarget : undefined;
  let basePath = '/';
  const queryParams = new URLSearchParams();
  let hashAnchor = '';

  switch (type) {
    case 'past_question': {
      basePath = `/cikmis/${encodeURIComponent(targetId)}`;
      if (subObj?.optionKey || (subStr && subStr.startsWith('opt-'))) {
        const optK = subObj?.optionKey || subStr?.replace('opt-', '');
        hashAnchor = `opt-${targetId}-${optK?.toUpperCase()}`;
        queryParams.set('opt', (optK || '').toUpperCase());
      } else if (subObj?.section === 'explanation' || subStr === 'explanation' || subStr === 'expl') {
        hashAnchor = `expl-${targetId}`;
        queryParams.set('sec', 'explanation');
      } else if (subObj?.section === 'comments' || subObj?.commentId || subStr === 'comments') {
        hashAnchor = subObj?.commentId ? `comm-${subObj.commentId}` : `comments-${targetId}`;
        queryParams.set('sec', 'comments');
      } else if (subObj?.section === 'stem' || subStr === 'stem') {
        hashAnchor = `stem-${targetId}`;
      } else {
        hashAnchor = `q-${targetId}`;
      }
      break;
    }

    case 'pool_question':
    case 'practice_question': {
      // Havuz sorusu kendi yolunda açılır (eskiden "/?committeeId=…?questionId=…" → çift "?" ve Çıkmış'a düşüyordu).
      basePath = `/sorular/${encodeURIComponent(targetId)}`;
      if (subObj?.optionKey || (subStr && subStr.startsWith('opt-'))) {
        const optK = subObj?.optionKey || subStr?.replace('opt-', '');
        hashAnchor = `opt-${targetId}-${optK?.toUpperCase()}`;
        queryParams.set('opt', (optK || '').toUpperCase());
      } else if (subObj?.section === 'explanation' || subStr === 'explanation' || subStr === 'expl') {
        hashAnchor = `expl-${targetId}`;
        queryParams.set('sec', 'explanation');
      } else if (subObj?.section === 'stem' || subStr === 'stem') {
        hashAnchor = `stem-${targetId}`;
      } else {
        hashAnchor = `q-${targetId}`;
      }
      break;
    }

    case 'interactive_deck':
    case 'learn_slide': {
      basePath = `/ogren/${encodeURIComponent(targetId)}`;
      if (subObj?.slideNumber) {
        queryParams.set('slide', String(subObj.slideNumber));
        hashAnchor = `slide-${subObj.slideNumber}`;
      }
      if (subObj?.targetKey || subObj?.elementKey) {
        const k = subObj.targetKey || subObj.elementKey;
        queryParams.set('target', k!);
        hashAnchor = `element-${k}`;
      }
      break;
    }

    case 'interactive_element':
    case 'table': {
      basePath = `/ogren/${encodeURIComponent(targetId)}`;
      if (subObj?.slideNumber) {
        queryParams.set('slide', String(subObj.slideNumber));
      }
      const tKey = subObj?.tableId || subObj?.elementKey || subObj?.targetKey || 'interactive';
      queryParams.set('target', tKey);
      hashAnchor = `table-${tKey}`;
      break;
    }

    case 'spot': {
      basePath = `/ogren/${encodeURIComponent(targetId)}`;
      if (subObj?.slideNumber) {
        queryParams.set('slide', String(subObj.slideNumber));
      }
      queryParams.set('target', 'spots');
      hashAnchor = 'spots';
      break;
    }

    case 'term': {
      const termId = subObj?.termId || (subStr && !subStr.startsWith('sec-') ? subStr : targetId);
      basePath = '/sozluk';
      queryParams.set('id', termId);
      const sec = subObj?.section || (subStr && subStr.startsWith('sec-') ? subStr.replace('sec-', '') : undefined);
      if (sec) {
        queryParams.set('section', sec);
        hashAnchor = `term-${termId}-${sec}`;
      } else {
        hashAnchor = `term-${termId}`;
      }
      break;
    }

    case 'disease': {
      const diseaseId = subObj?.diseaseId || (subStr && !subStr.startsWith('sec-') ? subStr : targetId);
      basePath = '/hastaliklar';
      queryParams.set('id', diseaseId);
      const sec = subObj?.section || (subStr && subStr.startsWith('sec-') ? subStr.replace('sec-', '') : undefined);
      if (sec) {
        queryParams.set('section', sec);
        hashAnchor = `disease-${diseaseId}-${sec}`;
      } else {
        hashAnchor = `disease-${diseaseId}`;
      }
      break;
    }

    case 'flashcard': {
      const cardId = subObj?.cardId || subStr || targetId;
      basePath = '/kartlar';
      queryParams.set('id', cardId);
      hashAnchor = `card-${cardId}`;
      break;
    }

    case 'lecture_summary': {
      basePath = '/ozetler';
      queryParams.set('noteId', targetId);
      if (subObj?.pageNumber) {
        queryParams.set('page', String(subObj.pageNumber));
      }
      break;
    }

    case 'lecture_note': {
      basePath = '/notlar';
      queryParams.set('id', targetId);
      if (subObj?.pageNumber) {
        queryParams.set('page', String(subObj.pageNumber));
      }
      break;
    }

    case 'comment': {
      basePath = `/cikmis/${encodeURIComponent(targetId)}`;
      if (subObj?.commentId || subStr) {
        const cId = subObj?.commentId || subStr;
        hashAnchor = `comment-${cId}`;
        queryParams.set('sec', 'comments');
      }
      break;
    }

    case 'explanation': {
      basePath = `/cikmis/${encodeURIComponent(targetId)}`;
      hashAnchor = `q-${targetId}-explanation`;
      queryParams.set('sec', 'explanation');
      break;
    }

    case 'option': {
      basePath = `/cikmis/${encodeURIComponent(targetId)}`;
      const optKey = subObj?.optionKey || subStr;
      if (optKey) {
        hashAnchor = `q-${targetId}-opt-${optKey.toUpperCase()}`;
        queryParams.set('opt', optKey.toUpperCase());
      }
      break;
    }

    default:
      basePath = '/';
  }

  // Cümle/Metin Etiketleme ve Web Standard Text-Fragment
  let textFragment = '';
  if (highlightText && highlightText.trim()) {
    const cleanSnippet = highlightText.trim().slice(0, 100);
    queryParams.set('highlight', cleanSnippet);
    textFragment = `#:~:text=${encodeURIComponent(cleanSnippet)}`;
  } else if (hashAnchor) {
    textFragment = `#${encodeURIComponent(hashAnchor)}`;
  }

  const qs = queryParams.toString();
  return `${basePath}${qs ? `?${qs}` : ''}${textFragment}`;
}

export const buildUniversalReportUrl = buildDeepLinkUrl;

/**
 * Paylaşılabilir mutlak link üretir (origin dahil)
 */
export function buildAbsoluteDeepLinkUrl(target: DeepLinkTarget): string {
  const relative = buildDeepLinkUrl(target);
  if (typeof window !== 'undefined' && window.location.origin) {
    return `${window.location.origin}${relative}`;
  }
  return `https://nofrostlife.com.tr${relative}`;
}

/**
 * Evrensel Paylaşım Yöneticisi:
 * Mobil cihazlarda yerel paylaşım penceresini açar (Web Share API),
 * masaüstü veya desteklenmeyen tarayıcılarda panoya kopyalar ve toast gösterir.
 */
export async function shareDeepLink(
  target: DeepLinkTarget,
  fallbackTitle?: string,
  extraText?: string
): Promise<boolean> {
  const url = buildAbsoluteDeepLinkUrl(target);
  const breadcrumb = getUniversalLocationBreadcrumb(target);
  const title = fallbackTitle || breadcrumb.badge;
  const text = extraText || breadcrumb.fullLocation;

  if (typeof navigator !== 'undefined' && navigator.share && window.matchMedia?.('(pointer: coarse)').matches) {
    try {
      await navigator.share({ title, text, url });
      return true;
    } catch (e: any) {
      if (e?.name === 'AbortError') return false;
    }
  }

  try {
    if (typeof navigator !== 'undefined' && navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(url);
      toast.success('Bağlantı kopyalandı', `${breadcrumb.badge} doğrudan bağlantısı panoya kopyalandı.`);
      return true;
    }
  } catch {}

  toast.info('Bağlantı', url);
  return true;
}

/**
 * Bildirilen ögenin insan tarafından kolay okunabilir konum rozeti ve başlığı.
 */
export function getUniversalLocationBreadcrumb(target: DeepLinkTarget): {
  badge: string;
  fullLocation: string;
  category: string;
} {
  const targetId = target.targetId || target.id || '';
  const subObj = typeof target.subTarget === 'object' && target.subTarget !== null ? target.subTarget : undefined;
  const subStr = typeof target.subTarget === 'string' ? target.subTarget : undefined;

  switch (target.type) {
    case 'past_question': {
      const opt = subObj?.optionKey || (subStr && subStr.startsWith('opt-') ? subStr.replace('opt-', '') : '');
      const optStr = opt ? ` · Şık ${opt.toUpperCase()}` : '';
      const sec = (subObj?.section === 'explanation' || subStr === 'explanation') ? ' · Açıklama' : (subObj?.section === 'comments' || subStr === 'comments') ? ' · Yorumlar' : '';
      return {
        badge: `Çıkmış Soru #${targetId}${optStr}${sec}`,
        fullLocation: `Çıkmış Sınav Soruları › Soru #${targetId}${optStr}${sec}`,
        category: 'Çıkmış Soru',
      };
    }
    case 'pool_question':
    case 'practice_question': {
      const opt = subObj?.optionKey || (subStr && subStr.startsWith('opt-') ? subStr.replace('opt-', '') : '');
      const optStr = opt ? ` · Şık ${opt.toUpperCase()}` : '';
      return {
        badge: `Havuz Sorusu #${targetId}${optStr}`,
        fullLocation: `Soru Havuzu & Örnek Sorular › Soru #${targetId}${optStr}`,
        category: 'Örnek Soru',
      };
    }
    case 'interactive_deck':
    case 'learn_slide':
      return {
        badge: `Öğren: ${targetId}${subObj?.slideNumber ? ` · Slayt ${subObj.slideNumber}` : ''}`,
        fullLocation: `İnteraktif Öğrenme › ${targetId} › ${subObj?.slideNumber ? `${subObj.slideNumber}. Slayt` : 'Deste'}`,
        category: 'Öğrenme Slaytı',
      };
    case 'interactive_element':
    case 'table':
      return {
        badge: `Öğren Tablo: ${targetId} (Slayt ${subObj?.slideNumber || 1})`,
        fullLocation: `İnteraktif Öğrenme › ${targetId} › Slayt ${subObj?.slideNumber || 1} › Tablo / Etkileşim`,
        category: 'İnteraktif Tablo & Öğe',
      };
    case 'term': {
      const termName = subObj?.termId || (subStr && !subStr.startsWith('sec-') ? subStr : targetId);
      const sec = subObj?.section === 'definition' ? ' (Tanım)' : subObj?.section === 'mechanism' ? ' (Mekanizma)' : '';
      return {
        badge: `Tıbbi Terim: ${termName}${sec}`,
        fullLocation: `Tıbbi Sözlük & Ansiklopedi › ${termName}${sec}`,
        category: 'Tıbbi Sözlük',
      };
    }
    case 'disease': {
      const diseaseName = subObj?.diseaseId || (subStr && !subStr.startsWith('sec-') ? subStr : targetId);
      const sec = subObj?.section ? ` (${subObj.section})` : '';
      return {
        badge: `Hastalık: ${diseaseName}${sec}`,
        fullLocation: `Hastalıklar & Klinik Atlas › ${diseaseName}${sec}`,
        category: 'Hastalık Atlası',
      };
    }
    case 'flashcard': {
      const cardId = subObj?.cardId || subStr || targetId;
      return {
        badge: `Akıl Kartı: #${cardId}`,
        fullLocation: `Ezber & Akıl Kartları › #${cardId}`,
        category: 'Akıl Kartı',
      };
    }
    case 'spot':
      return {
        badge: `Sınav Spotu: ${targetId}`,
        fullLocation: `Öğrenme Destesi › Slayt ${subObj?.slideNumber || 1} › Sınav Spotları`,
        category: 'Spot Bilgi',
      };
    case 'lecture_summary':
      return {
        badge: `Ders Özeti: ${targetId}`,
        fullLocation: `Ders Özetleri › Not #${targetId}${subObj?.pageNumber ? ` › Sayfa ${subObj.pageNumber}` : ''}`,
        category: 'Ders Özeti',
      };
    case 'lecture_note':
      return {
        badge: `Ders Notu / PDF: ${targetId}`,
        fullLocation: `Amfi Ders Notları › Not #${targetId}${subObj?.pageNumber ? ` › Sayfa ${subObj.pageNumber}` : ''}`,
        category: 'Ders Notu',
      };
    case 'comment':
      return {
        badge: `Yorum Bildirimi: Soru #${targetId}`,
        fullLocation: `Soru Tartışması & Yorumlar › Soru #${targetId}`,
        category: 'Kullanıcı Yorumu',
      };
    default:
      return {
        badge: targetId || 'İçerik',
        fullLocation: targetId || 'İçerik Detayı',
        category: 'İçerik',
      };
  }
}

/**
 * Sayfada hedeflenen ögeyi (soru, şık, açıklama, yorum, terim, kart vb.) bulur,
 * kapalı akordeon/details varsa açar, merkeze yumuşakça kaydırır ve
 * 1-2 kez parıldayan nefes alan bir vurgu animasyonu (`deep-link-highlight-pulse`) uygular.
 */
export function executeDeepLinkFocus(target?: string | {
  targetId?: string;
  selector?: string;
  text?: string;
  section?: string;
  optionKey?: string;
}): boolean {
  if (typeof window === 'undefined') return false;

  let options: { targetId?: string; selector?: string; text?: string; section?: string; optionKey?: string; } | undefined;
  if (typeof target === 'string') {
    if (target.includes('#')) {
      const hashPart = target.split('#')[1];
      options = { targetId: hashPart };
    } else {
      options = { targetId: target };
    }
  } else {
    options = target;
  }

  const urlParams = new URLSearchParams(icKonum().search);
  const hash = window.location.hash ? decodeURIComponent(window.location.hash.slice(1)) : '';
  // Kimlik sorguda yoksa yoldan okunur: /cikmis/<id>, /sorular/<id>
  const pathId = (() => {
    const m = icKonum().pathname.match(/\/(?:cikmis|sorular|havuz)\/([^/?#]+)/);
    return m ? decodeURIComponent(m[1]) : '';
  })();
  const targetId = options?.targetId || urlParams.get('id') || urlParams.get('q') || pathId || '';
  const section = options?.section || urlParams.get('sec') || urlParams.get('section') || '';
  const opt = options?.optionKey || urlParams.get('opt') || '';
  const highlightSnippet = options?.text || urlParams.get('highlight') || '';

  // 1. Olası DOM element ID'lerini sırayla dene
  const candidateIds: string[] = [];
  if (options?.selector) {
    const el = document.querySelector(options.selector) as HTMLElement | null;
    if (el) return applyPulseAndScroll(el);
  }

  if (options?.targetId) {
    candidateIds.push(options.targetId);
  }

  if (hash) {
    // Text fragment temizliği (#:~:text=...)
    const cleanHash = hash.replace(/:~:text=.*$/, '');
    if (cleanHash) candidateIds.push(cleanHash);
  }

  if (targetId) {
    if (opt) candidateIds.push(`q-${targetId}-opt-${opt.toUpperCase()}`, `opt-${targetId}-${opt.toUpperCase()}`);
    if (section === 'explanation') candidateIds.push(`expl-${targetId}`);
    if (section === 'comments') candidateIds.push(`comments-${targetId}`);
    if (section) candidateIds.push(`q-${targetId}-${section}`, `term-${targetId}-${section}`);
    candidateIds.push(
      `q-${targetId}`,
      `term-${targetId}`,
      `card-${targetId}`,
      `comment-${targetId}`,
      `term-card-${targetId}`,
      targetId
    );
  }

  for (const id of candidateIds) {
    const el = document.getElementById(id);
    if (el) {
      return applyPulseAndScroll(el);
    }
  }

  // 2. Metin Düğümü Araması (TreeWalker)
  if (highlightSnippet && highlightSnippet.trim().length >= 3) {
    return triggerDomHighlightAndScroll(highlightSnippet);
  }

  return false;
}

/**
 * Elemanı görünür kılar (kapalı parent'ları açar), kaydırır ve animasyonu başlatır
 */
function applyPulseAndScroll(el: HTMLElement): boolean {
  try {
    // 1. Gizli veya kapalı üst ögeleri aç (details, accordion, collapsible)
    let parent = el.parentElement;
    while (parent) {
      if (parent.tagName === 'DETAILS' && !(parent as HTMLDetailsElement).open) {
        (parent as HTMLDetailsElement).open = true;
      }
      if (parent.classList.contains('hidden')) {
        parent.classList.remove('hidden');
      }
      if (parent.getAttribute('aria-expanded') === 'false') {
        parent.setAttribute('aria-expanded', 'true');
      }
      parent = parent.parentElement;
    }

    // 2. Yumuşakça merkeze kaydır
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // 3. Vurgu animasyonunu uygula (önceki varsa kaldırıp yeniden başlat)
    el.classList.remove('deep-link-highlight-pulse');
    // Reflow tetikle
    void el.offsetWidth;
    el.classList.add('deep-link-highlight-pulse');

    // 4. Klavye odağı ver
    if (!el.getAttribute('tabindex')) {
      el.setAttribute('tabindex', '-1');
    }
    el.focus({ preventScroll: true });

    // 5. Animasyon bitince temizle
    setTimeout(() => {
      el.classList.remove('deep-link-highlight-pulse');
    }, 2600);

    return true;
  } catch (e) {
    console.warn('[DeepLink] Focus animasyonu uygulanamadı:', e);
    return false;
  }
}

/**
 * Sayfada etiketlenen metni bulup yumuşakça kaydırır ve altın rengi/indigo vurgu ile parlatır.
 */
export function triggerDomHighlightAndScroll(textToHighlight?: string): boolean {
  if (typeof window === 'undefined' || !textToHighlight) return false;

  const targetSnippet = textToHighlight.trim().toLowerCase();
  if (targetSnippet.length < 3) return false;

  try {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
    let node: Node | null = null;

    while ((node = walker.nextNode())) {
      const content = (node.textContent || '').toLowerCase();
      if (content.includes(targetSnippet)) {
        const parent = node.parentElement;
        if (parent && !['SCRIPT', 'STYLE', 'TEXTAREA', 'INPUT'].includes(parent.tagName)) {
          return applyPulseAndScroll(parent);
        }
      }
    }
  } catch (_) {}

  return false;
}

/**
 * Sayfa ilk yüklendiğinde veya rota değiştiğinde derin bağlantı odağını otomatik başlatır
 */
export function initDeepLinkAutoScroll(): () => void {
  if (typeof window === 'undefined') return () => {};

  // Hedef liste veri yüklendikten sonra çizilir: bulunana kadar ~6 sn boyunca aralıklı dene.
  let timer = 0;
  const handle = () => {
    window.clearTimeout(timer);
    const { search, hash } = window.location;
    if (!hash && !/[?&](opt|sec|section|highlight|id|q)=/.test(search)) return;
    let n = 0;
    const tryFocus = () => {
      if (executeDeepLinkFocus() || ++n > 15) return;
      timer = window.setTimeout(tryFocus, 400);
    };
    timer = window.setTimeout(tryFocus, 280);
  };

  if (document.readyState === 'complete') {
    handle();
  } else {
    window.addEventListener('load', handle, { once: true });
  }

  window.addEventListener('hashchange', handle);
  window.addEventListener('popstate', handle);

  return () => {
    window.removeEventListener('hashchange', handle);
    window.removeEventListener('popstate', handle);
  };
}
