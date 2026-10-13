/**
 * Yönetici bildirimlerinin (push, e-posta, panel) açacağı uygulama içi yol.
 *
 * Bildirimin `questionId` alanı çoğu zaman bir etiket ("Tıbbi Terim: x", "Akıl Kartı: y") olduğu için
 * bağlantı ondan türetilemez; her tetikleyici hedefini burada açıkça adlandırır. Yollar istemci
 * yönlendiricisinin (src/router.ts) ve derin bağlantı odaklamanın (universalRedirectService) okuduğu biçimdedir.
 * Sunucuda da çalışır: DOM / tarayıcı bağımlılığı yoktur.
 */

const enc = encodeURIComponent;

export type NotificationTarget =
  | { kind: 'past_question'; id: string; commentId?: string; section?: 'comments' | 'explanation' }
  | { kind: 'pool_question'; id: string }
  | { kind: 'ornek_question'; id: string }
  | { kind: 'term'; id: string }
  | { kind: 'flashcard'; id: string }
  | { kind: 'disease'; id: string }
  | { kind: 'deck'; id: string; slideNumber?: number; targetKey?: string }
  | { kind: 'summary'; id: string }
  | { kind: 'spot'; id?: string };

export function notificationLinkFor(t: NotificationTarget): string {
  switch (t.kind) {
    case 'past_question': {
      if (t.commentId) return `/cikmis/${enc(t.id)}?sec=comments#comm-${enc(t.commentId)}`;
      if (t.section === 'comments') return `/cikmis/${enc(t.id)}?sec=comments#comments-${enc(t.id)}`;
      if (t.section === 'explanation') return `/cikmis/${enc(t.id)}?sec=explanation#expl-${enc(t.id)}`;
      return `/cikmis/${enc(t.id)}#q-${enc(t.id)}`;
    }
    case 'pool_question':
      return `/sorular/${enc(t.id)}#q-${enc(t.id)}`;
    case 'ornek_question':
      return `/ornek-sorular/${enc(t.id)}`;
    case 'term':
      return `/sozluk/${enc(t.id)}#term-${enc(t.id)}`;
    case 'flashcard':
      return `/kartlar?id=${enc(t.id)}#card-${enc(t.id)}`;
    case 'disease':
      return `/hastaliklar/${enc(t.id)}#disease-${enc(t.id)}`;
    case 'deck': {
      const sp = new URLSearchParams();
      if (t.slideNumber) sp.set('adim', String(t.slideNumber));
      if (t.targetKey) sp.set('hedef', t.targetKey);
      const qs = sp.toString();
      return `/ogren/${enc(t.id)}${qs ? `?${qs}` : ''}`;
    }
    case 'summary':
      return `/ozetler?noteId=${enc(t.id)}`;
    case 'spot':
      return '/spotlar';
  }
}

/**
 * Evrensel hata bildiriminin (targetType + targetId) yolu. İstemcinin gönderdiği `link` yalnız
 * site içi bir yolsa ("/…", "//" değil) kabul edilir.
 */
export function universalReportLink(targetType: string, targetId: string, clientLink?: unknown): string | undefined {
  if (typeof clientLink === 'string' && /^\/(?!\/)/.test(clientLink)) return clientLink.slice(0, 500);
  if (!targetId) return undefined;
  const type = targetType.toLowerCase();
  if (type === 'term' || type === 'glossary' || type === 'encyclopedia') return notificationLinkFor({ kind: 'term', id: targetId });
  if (type === 'flashcard' || type === 'card') return notificationLinkFor({ kind: 'flashcard', id: targetId });
  if (type === 'disease') return notificationLinkFor({ kind: 'disease', id: targetId });
  if (type === 'past_question' || type === 'comment' || type === 'explanation' || type === 'option')
    return notificationLinkFor({ kind: 'past_question', id: targetId });
  if (type === 'pool_question' || type === 'practice_question') return notificationLinkFor({ kind: 'pool_question', id: targetId });
  if (type === 'ornek_question') return notificationLinkFor({ kind: 'ornek_question', id: targetId });
  if (type === 'interactive_deck' || type === 'learn_slide' || type === 'interactive_element' || type === 'table')
    return notificationLinkFor({ kind: 'deck', id: targetId });
  if (type === 'lecture_summary' || type === 'summary') return notificationLinkFor({ kind: 'summary', id: targetId });
  if (type === 'spot') return notificationLinkFor({ kind: 'spot' });
  return undefined;
}

/**
 * Bağlantı üreticisinden önceki kayıtlar adresi etiketten kuruyordu (/cikmis/T%C4%B1bbi%20Terim%3A%20x).
 * Etiket tanınırsa doğru yol döner; tanınmazsa undefined (kayıt olduğu gibi kalır).
 */
export function repairLegacyNotificationPath(questionId?: string): string | undefined {
  const label = String(questionId || '').trim();
  if (!label) return undefined;
  if (/^k\d+-\d+-q\d+$/.test(label)) return notificationLinkFor({ kind: 'ornek_question', id: label });
  const m = label.match(/^([^:]+):\s*(.+)$/);
  if (!m) return undefined;
  const [, kind, id] = m;
  if (kind === 'Tıbbi Terim') return notificationLinkFor({ kind: 'term', id });
  if (kind === 'Akıl Kartı') return notificationLinkFor({ kind: 'flashcard', id });
  return universalReportLink(kind, id);
}
