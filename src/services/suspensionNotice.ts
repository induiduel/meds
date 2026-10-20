/**
 * "Hesabınız askıya alındı" bildirimi. Sunucu askıdaki hesabın yazma isteğini 403 + code 'ACCOUNT_SUSPENDED' ile
 * reddeder (src/services/userAdminRoutes.ts); safeJsonFetch bunu görünce burayı çağırır. React'a bağlı değildir:
 * sayfanın altına sabit bir uyarı şeridi ekler, kapatılabilir; aynı oturumda yinelenen hatalarda yeniden açılır.
 */
export const SUSPENDED_CODE = 'ACCOUNT_SUSPENDED';
export const SUSPENDED_EVENT = 'medsor:account-suspended';

export function showSuspendedNotice(info: { error?: string; reason?: string; until?: string | null }) {
  if (typeof document === 'undefined') return;
  try {
    window.dispatchEvent(new CustomEvent(SUSPENDED_EVENT, { detail: info }));
  } catch {
    /* eski tarayıcı */
  }
  let box = document.getElementById('medsor-suspended-notice');
  if (!box) {
    box = document.createElement('div');
    box.id = 'medsor-suspended-notice';
    box.setAttribute('role', 'alert');
    box.style.cssText = [
      'position:fixed', 'left:16px', 'right:16px', 'bottom:16px', 'z-index:2147483000', 'max-width:560px', 'margin:0 auto',
      'box-sizing:border-box', 'padding:14px 16px', 'border-radius:14px',
      'background:var(--surface, var(--bg-elev, #fff))', 'color:var(--ink, var(--text, #1c1c1e))',
      'border:1px solid var(--danger, var(--red, #d70015))', 'box-shadow:0 10px 30px rgba(0,0,0,.18)',
      'font:14px/1.45 inherit', 'display:flex', 'gap:12px', 'align-items:flex-start', 'overflow-wrap:anywhere',
    ].join(';');
    document.body.appendChild(box);
  }
  const until = info.until ? new Date(info.until).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }) : '';
  box.innerHTML = '';
  const text = document.createElement('div');
  text.style.cssText = 'flex:1;min-width:0';
  const title = document.createElement('strong');
  title.textContent = 'Hesabınız askıya alındı';
  title.style.cssText = 'display:block;margin-bottom:4px;color:var(--danger, var(--red, #d70015))';
  const body = document.createElement('span');
  body.textContent =
    `${until ? `Askı ${until} tarihine kadar sürüyor. ` : ''}Bu sürede içerikleri okuyabilirsiniz, ancak gönderme ve değiştirme işlemleri yapılamaz.` +
    (info.reason ? ` Gerekçe: ${info.reason}` : '');
  text.append(title, body);
  const close = document.createElement('button');
  close.type = 'button';
  close.textContent = 'Kapat';
  close.style.cssText = 'flex:none;border:0;background:transparent;color:inherit;font:inherit;font-weight:600;cursor:pointer;padding:4px 6px;min-height:32px';
  close.onclick = () => box?.remove();
  box.append(text, close);
}
