/**
 * Soruyu panoya kopyalar: yalnız soru kökü ve şıklar. Künye, ders, doğru cevap ve
 * açıklama gibi meta veriler kopyalanmaz.
 */
export interface CopyOption { key?: string; text?: string }

export function formatQuestionForCopy(stem: string, options: CopyOption[] | Record<string, string> = []): string {
  const list: CopyOption[] = Array.isArray(options)
    ? options
    : Object.entries(options).map(([key, text]) => ({ key, text }));
  const lines = list
    .filter((o) => o && String(o.text ?? '').trim())
    .map((o) => `${String(o.key ?? '').trim()}) ${String(o.text).trim()}`);
  return [String(stem || '').trim(), lines.join('\n')].filter(Boolean).join('\n\n');
}

async function writeClipboard(text: string): Promise<boolean> {
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
      return true;
    }
  } catch { /* aşağıdaki yedek yola düş */ }
  try {
    const area = document.createElement('textarea');
    area.value = text;
    area.setAttribute('readonly', '');
    area.style.position = 'fixed';
    area.style.opacity = '0';
    document.body.appendChild(area);
    area.select();
    const ok = document.execCommand('copy');
    area.remove();
    return ok;
  } catch {
    return false;
  }
}

export function copyQuestion(stem: string, options: CopyOption[] | Record<string, string> = []): Promise<boolean> {
  return writeClipboard(formatQuestionForCopy(stem, options));
}
