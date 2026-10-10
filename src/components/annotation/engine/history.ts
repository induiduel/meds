import type { Stroke } from '../types';

/**
 * Geri/İleri Al: komut tabanlı. Piksel verisi değil, yalnızca hangi çizgilerin
 * eklendiği/kaldırıldığı saklanır → bellek dostu ve sınırsıza yakın derinlik.
 *
 * - add:    yeni çizgi(ler) eklendi (kalem, fosforlu, piksel silgi izi)
 * - remove: çizgi(ler) kaldırıldı (nesne silgisi, "tümünü temizle")
 */
export type Command = { kind: 'add'; strokes: Stroke[] } | { kind: 'remove'; strokes: Stroke[] };

const LIMIT = 300;

export class History {
  private undoStack: Command[] = [];
  private redoStack: Command[] = [];

  push(cmd: Command): void {
    this.undoStack.push(cmd);
    if (this.undoStack.length > LIMIT) this.undoStack.shift();
    this.redoStack = [];
  }

  /** Komutu tersine uygular ve yeni çizgi listesini döner. */
  undo(strokes: Stroke[]): Stroke[] | null {
    const cmd = this.undoStack.pop();
    if (!cmd) return null;
    this.redoStack.push(cmd);
    return cmd.kind === 'add' ? without(strokes, cmd.strokes) : withStrokes(strokes, cmd.strokes);
  }

  redo(strokes: Stroke[]): Stroke[] | null {
    const cmd = this.redoStack.pop();
    if (!cmd) return null;
    this.undoStack.push(cmd);
    return cmd.kind === 'add' ? withStrokes(strokes, cmd.strokes) : without(strokes, cmd.strokes);
  }

  reset(): void {
    this.undoStack = [];
    this.redoStack = [];
  }

  get canUndo(): boolean {
    return this.undoStack.length > 0;
  }

  get canRedo(): boolean {
    return this.redoStack.length > 0;
  }
}

function without(strokes: Stroke[], remove: Stroke[]): Stroke[] {
  const ids = new Set(remove.map((s) => s.id));
  return strokes.filter((s) => !ids.has(s.id));
}

/** Geri gelen çizgiler `seq` ile sıralanır; piksel silgi izleri doğru sırada kalır. */
function withStrokes(strokes: Stroke[], add: Stroke[]): Stroke[] {
  return [...strokes, ...add].sort((a, b) => a.seq - b.seq);
}
