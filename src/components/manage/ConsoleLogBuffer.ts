/**
 * ManageConsole için tarayıcı konsolu yakalama tamponu.
 * console.log/warn/error + window hata olaylarını halka tamponunda tutar,
 * Sistem & Loglar sekmesinde ve sunucuya raporlamada kullanılır.
 */

export type ManageLogLevel = 'log' | 'info' | 'warn' | 'error';

export interface ManageLogEntry {
  id: number;
  ts: string;
  level: ManageLogLevel;
  source: string;
  message: string;
}

type Listener = (entries: ManageLogEntry[]) => void;

const MAX_ENTRIES = 500;

class ConsoleLogBuffer {
  private entries: ManageLogEntry[] = [];
  private listeners = new Set<Listener>();
  private installed = false;
  private seq = 0;

  install() {
    if (this.installed || typeof window === 'undefined') return;
    this.installed = true;
    const fmt = (args: unknown[]) =>
      args
        .map((a) => {
          if (typeof a === 'string') return a;
          try {
            return JSON.stringify(a);
          } catch {
            return String(a);
          }
        })
        .join(' ')
        .slice(0, 2000);

    const push = (level: ManageLogLevel, source: string, message: string) => {
      this.seq += 1;
      this.entries.push({
        id: this.seq,
        ts: new Date().toISOString(),
        level,
        source,
        message: message.slice(0, 2000),
      });
      if (this.entries.length > MAX_ENTRIES) {
        this.entries = this.entries.slice(this.entries.length - MAX_ENTRIES);
      }
      this.emit();
    };

    const origLog = console.log.bind(console);
    const origInfo = (console.info || console.log).bind(console);
    const origWarn = console.warn.bind(console);
    const origError = console.error.bind(console);

    console.log = (...args: unknown[]) => {
      push('log', 'console', fmt(args));
      origLog(...(args as []));
    };
    (console as { info: (...a: unknown[]) => void }).info = (...args: unknown[]) => {
      push('info', 'console', fmt(args));
      origInfo(...(args as []));
    };
    console.warn = (...args: unknown[]) => {
      push('warn', 'console', fmt(args));
      origWarn(...(args as []));
    };
    console.error = (...args: unknown[]) => {
      push('error', 'console', fmt(args));
      origError(...(args as []));
    };

    window.addEventListener('error', (e) => {
      push('error', 'window.onerror', `${e.message || 'Bilinmeyen hata'} @ ${e.filename || ''}:${e.lineno || 0}`);
    });
    window.addEventListener('unhandledrejection', (e) => {
      const msg = (e.reason as { message?: string })?.message || String(e.reason || 'Promise reddedildi');
      push('error', 'unhandledrejection', msg);
    });

    push('info', 'manage-console', 'Konsol yakalama aktif (son 500 kayıt tutulur).');
  }

  subscribe(fn: Listener): () => void {
    this.listeners.add(fn);
    fn([...this.entries]);
    return () => {
      this.listeners.delete(fn);
    };
  }

  private emit() {
    const snap = [...this.entries];
    for (const l of this.listeners) {
      try {
        l(snap);
      } catch {
        /* dinleyici hatası yutulur */
      }
    }
  }

  getEntries(): ManageLogEntry[] {
    return [...this.entries];
  }

  clear() {
    this.entries = [];
    this.emit();
  }
}

export const consoleLogBuffer = new ConsoleLogBuffer();
