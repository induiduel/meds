import React, { useCallback, useEffect, useRef, useSyncExternalStore } from 'react';
import { Highlighter as PenIcon, Eraser, Trash2 } from 'lucide-react';
import { toast } from './Toast';

/**
 * Fosforlu kalem: select text to paint it, pick a colour, erase or clear.
 * Marks are drawn with the CSS Custom Highlight API (no DOM changes, so React
 * re-renders are safe) and saved per scope (summary / slide) on this device.
 */
export type HlColor = 'yellow' | 'green' | 'pink' | 'blue';
export const HL_COLORS: { id: HlColor; label: string; swatch: string }[] = [
  { id: 'yellow', label: 'Sarı', swatch: '#FDE047' },
  { id: 'green', label: 'Yeşil', swatch: '#86EFAC' },
  { id: 'pink', label: 'Pembe', swatch: '#F9A8D4' },
  { id: 'blue', label: 'Mavi', swatch: '#93C5FD' },
];

// ---------------------------------------------------------------------------
// Tool state (module store; every toolbar and scope sees the same pen)
// ---------------------------------------------------------------------------
interface Tool {
  active: boolean;
  color: HlColor;
  eraser: boolean;
}
let tool: Tool = { active: false, color: 'yellow', eraser: false };
const toolListeners = new Set<() => void>();
const setTool = (patch: Partial<Tool>) => {
  tool = { ...tool, ...patch };
  toolListeners.forEach((l) => l());
};
/** True while the pen (or eraser) is on — gestures like swipe-to-next should pause. */
export const isPenActive = () => tool.active;

const useTool = () =>
  useSyncExternalStore(
    (cb) => {
      toolListeners.add(cb);
      return () => toolListeners.delete(cb);
    },
    () => tool,
    () => tool
  );

// ---------------------------------------------------------------------------
// Persistence
// ---------------------------------------------------------------------------
interface Mark {
  id: string;
  color: HlColor;
  start: number;
  end: number;
  text: string;
}
const STORE_KEY = 'medsoru_highlights_v1';
const readAll = (): Record<string, Mark[]> => {
  try {
    return JSON.parse(localStorage.getItem(STORE_KEY) || '{}');
  } catch {
    return {};
  }
};
const saveScope = (scope: string, marks: Mark[]) => {
  try {
    const all = readAll();
    if (marks.length) all[scope] = marks;
    else delete all[scope];
    localStorage.setItem(STORE_KEY, JSON.stringify(all));
  } catch {
    /* storage unavailable: marks last for this visit */
  }
};

// ---------------------------------------------------------------------------
// Painting: aggregate ranges from every mounted scope into CSS highlights
// ---------------------------------------------------------------------------
const supported = () => typeof CSS !== 'undefined' && 'highlights' in CSS && typeof (window as any).Highlight === 'function';
const painted = new Map<string, { color: HlColor; range: Range }[]>();
const repaint = () => {
  if (!supported()) return;
  const reg = (CSS as any).highlights;
  HL_COLORS.forEach(({ id }) => {
    const hl = new (window as any).Highlight();
    painted.forEach((list) => list.forEach((m) => m.color === id && hl.add(m.range)));
    reg.set(`ms-hl-${id}`, hl);
  });
};

const norm = (s: string) => s.replace(/\s+/g, ' ').trim();

/** Character offset of a DOM position inside the container's text. */
const offsetOf = (root: Node, node: Node, offset: number) => {
  const r = document.createRange();
  r.setStart(root, 0);
  r.setEnd(node, offset);
  return r.toString().length;
};

/** Range for [start, end) character offsets of the container's text. */
const rangeFor = (root: Node, start: number, end: number): Range | null => {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let pos = 0;
  let startNode: Text | null = null;
  let startOff = 0;
  let n: Node | null;
  while ((n = walker.nextNode())) {
    const len = (n as Text).data.length;
    if (!startNode && start <= pos + len) {
      startNode = n as Text;
      startOff = start - pos;
    }
    if (startNode && end <= pos + len) {
      const r = document.createRange();
      r.setStart(startNode, Math.max(0, startOff));
      r.setEnd(n, Math.max(0, end - pos));
      return r;
    }
    pos += len;
  }
  return null;
};

// ---------------------------------------------------------------------------
// Toolbar
// ---------------------------------------------------------------------------
const mounted = new Map<string, () => void>(); // scope -> clear()

export const HighlighterToolbar: React.FC<{ className?: string }> = ({ className = '' }) => {
  const t = useTool();
  const togglePen = () => {
    if (!supported()) {
      toast.error('Fosforlu kalem çalışmıyor', 'Tarayıcın metin vurgulamayı desteklemiyor. Chrome, Edge ya da güncel Safari dene.');
      return;
    }
    setTool({ active: !t.active, eraser: false });
    if (!t.active) toast.info('Fosforlu kalem açık', 'Boyamak istediğin metni seç. Silmek için silgiyi seç.');
  };
  return (
    <div className={`flex items-center gap-1 ${className}`} role="group" aria-label="Fosforlu kalem">
      <button
        type="button"
        onClick={togglePen}
        aria-pressed={t.active}
        title={t.active ? 'Kalemi kapat' : 'Fosforlu kalem'}
        className={`w-9 h-9 shrink-0 rounded-[10px] flex items-center justify-center cursor-pointer transition-colors ${
          t.active ? 'bg-[#FEF3C7] text-[#92400E] ring-1 ring-inset ring-[#F59E0B]/50' : 'text-ink-2 hover:bg-canvas hover:text-ink'
        }`}
      >
        <PenIcon className="w-[18px] h-[18px]" />
      </button>
      {t.active && (
        <div className="ms-pop-in flex items-center gap-1 h-9 px-1 rounded-[10px] bg-canvas">
          {HL_COLORS.map((c) => {
            const on = !t.eraser && t.color === c.id;
            return (
              <button
                key={c.id}
                type="button"
                onClick={() => setTool({ color: c.id, eraser: false })}
                aria-pressed={on}
                aria-label={`${c.label} kalem`}
                title={c.label}
                className={`w-7 h-7 rounded-full flex items-center justify-center cursor-pointer ${on ? 'bg-white shadow-[0_1px_3px_rgba(14,26,38,0.18)]' : ''}`}
              >
                <span className="w-4 h-4 rounded-full border border-black/10" style={{ background: c.swatch }} />
              </button>
            );
          })}
          <button
            type="button"
            onClick={() => setTool({ eraser: !t.eraser })}
            aria-pressed={t.eraser}
            aria-label="Silgi"
            title="Silgi: işaretin üstüne dokun ya da seç"
            className={`w-7 h-7 rounded-full flex items-center justify-center cursor-pointer ${t.eraser ? 'bg-white text-ink shadow-[0_1px_3px_rgba(14,26,38,0.18)]' : 'text-ink-2'}`}
          >
            <Eraser className="w-4 h-4" />
          </button>
          <button
            type="button"
            onClick={() => {
              if (!mounted.size) return;
              mounted.forEach((clear) => clear());
              toast.info('İşaretler temizlendi');
            }}
            aria-label="Bu sayfadaki işaretleri temizle"
            title="Bu sayfadaki işaretleri temizle"
            className="w-7 h-7 rounded-full flex items-center justify-center text-ink-2 hover:text-[#B4233C] cursor-pointer"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
};

// ---------------------------------------------------------------------------
// Scope: wraps text that can be highlighted
// ---------------------------------------------------------------------------
export const Highlightable: React.FC<{ scope: string; className?: string; style?: React.CSSProperties; children: React.ReactNode }> = ({
  scope,
  className = '',
  style,
  children,
}) => {
  const t = useTool();
  const ref = useRef<HTMLDivElement>(null);
  const marks = useRef<Mark[]>(readAll()[scope] || []);

  const apply = useCallback(() => {
    const root = ref.current;
    if (!root || !supported()) return;
    const text = root.textContent || '';
    const list: { color: HlColor; range: Range }[] = [];
    marks.current.forEach((m) => {
      let { start, end } = m;
      // Content shifted (e.g. edited text)? Re-find the marked phrase.
      if (norm(text.slice(start, end)) !== norm(m.text)) {
        const at = text.indexOf(m.text);
        if (at < 0) return;
        start = at;
        end = at + m.text.length;
      }
      const r = rangeFor(root, start, end);
      if (r) list.push({ color: m.color, range: r });
    });
    painted.set(scope, list);
    repaint();
  }, [scope]);

  const commit = useCallback(
    (next: Mark[]) => {
      marks.current = next;
      saveScope(scope, next);
      apply();
    },
    [scope, apply]
  );

  // Load + repaint when the scope or its content changes
  useEffect(() => {
    marks.current = readAll()[scope] || [];
    apply();
    const root = ref.current;
    if (!root) return;
    let timer = 0;
    const mo = new MutationObserver(() => {
      window.clearTimeout(timer);
      timer = window.setTimeout(apply, 120);
    });
    mo.observe(root, { childList: true, subtree: true, characterData: true });
    mounted.set(scope, () => commit([]));
    return () => {
      mo.disconnect();
      window.clearTimeout(timer);
      mounted.delete(scope);
      painted.delete(scope);
      repaint();
    };
  }, [scope, apply, commit]);

  const onPointerUp = (e: React.PointerEvent) => {
    if (!t.active) return;
    const root = ref.current;
    if (!root) return;
    // Let the browser finish updating the selection first
    window.setTimeout(() => {
      const sel = window.getSelection();
      if (sel && !sel.isCollapsed && sel.rangeCount) {
        const r = sel.getRangeAt(0);
        if (!root.contains(r.commonAncestorContainer)) return;
        const start = offsetOf(root, r.startContainer, r.startOffset);
        const end = offsetOf(root, r.endContainer, r.endOffset);
        if (end - start < 1) return;
        const overlapping = (m: Mark) => m.start < end && m.end > start;
        if (t.eraser) {
          commit(marks.current.filter((m) => !overlapping(m)));
        } else {
          const text = (root.textContent || '').slice(start, end);
          // Repainting over an old mark replaces it
          commit([...marks.current.filter((m) => !overlapping(m)), { id: `${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`, color: t.color, start, end, text }]);
        }
        sel.removeAllRanges();
        return;
      }
      // Eraser tap on a single mark
      if (t.eraser) {
        const doc: any = document;
        const caret = doc.caretPositionFromPoint
          ? doc.caretPositionFromPoint(e.clientX, e.clientY)
          : doc.caretRangeFromPoint?.(e.clientX, e.clientY);
        if (!caret) return;
        const node = caret.offsetNode || caret.startContainer;
        const off = caret.offset ?? caret.startOffset;
        if (!node || !root.contains(node)) return;
        const pos = offsetOf(root, node, off);
        const next = marks.current.filter((m) => !(pos >= m.start && pos <= m.end));
        if (next.length !== marks.current.length) commit(next);
      }
    }, 10);
  };

  return (
    <div
      ref={ref}
      onPointerUp={onPointerUp}
      className={`${className} ${t.active ? (t.eraser ? 'ms-pen-eraser' : `ms-pen ms-pen-${t.color}`) : ''}`}
      style={style}
    >
      {children}
    </div>
  );
};
