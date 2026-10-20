import React, { useEffect, useState } from 'react';
import '../../styles/v14/manage.css';

/**
 * v14 yönetim parçaları (canvas: Bilesenler.dc.html, VeritabaniGezgini.dc.html).
 * - BulkBar: yalnız seçim varken görünen toplu işlem çubuğu; yıkıcı eylem iki dokunuşla onaylanır.
 * - JsonView: JSON değeri türüne göre kart / etiket / tablo / açılır nesne olarak gösterir.
 * - JsonCell: tablo hücresinde nesne/dizi özeti ("{ } 7 alan", "[5]").
 * - useSelection: kimlik kümesiyle çoklu seçim (sayfadakilerin tümü, tersine çevir, temizle).
 */

export type BulkAction = {
  label: string;
  run: () => void | Promise<void>;
  kind?: 'main' | 'danger';
  /** danger için ikinci dokunuşta gösterilen metin */
  confirm?: string;
  disabled?: boolean;
};

export const BulkBar: React.FC<{ count: number; noun?: string; actions: BulkAction[]; onClear: () => void; busy?: boolean }> = ({ count, noun = 'öge', actions, onClear, busy }) => {
  const [armed, setArmed] = useState(-1);
  useEffect(() => {
    if (armed < 0) return;
    const t = window.setTimeout(() => setArmed(-1), 4000);
    return () => window.clearTimeout(t);
  }, [armed]);
  if (count <= 0) return null;
  return (
    <div className="bk14" role="region" aria-label="Toplu işlem">
      <span className="n" aria-live="polite">{count.toLocaleString('tr-TR')} {noun} seçili</span>
      {actions.map((a, i) => (
        <button
          key={a.label}
          type="button"
          disabled={busy || a.disabled}
          className={`${a.kind || ''} ${armed === i ? 'is-armed' : ''}`}
          onClick={() => {
            if (a.kind === 'danger' && armed !== i) return setArmed(i);
            setArmed(-1);
            void a.run();
          }}
        >
          {armed === i ? a.confirm || `${count} ${noun} için onayla` : a.label}
        </button>
      ))}
      <button type="button" className="clear" onClick={onClear} disabled={busy}>Seçimi kaldır</button>
    </div>
  );
};

export function useSelection<K extends string | number>() {
  const [sel, setSel] = useState<Set<K>>(() => new Set());
  return {
    sel,
    count: sel.size,
    has: (k: K) => sel.has(k),
    toggle: (k: K) => setSel((s) => { const n = new Set(s); if (n.has(k)) n.delete(k); else n.add(k); return n; }),
    /** keys hepsi seçiliyse kaldırır, değilse ekler */
    toggleAll: (keys: K[]) => setSel((s) => { const all = keys.length > 0 && keys.every((k) => s.has(k)); const n = new Set(s); keys.forEach((k) => (all ? n.delete(k) : n.add(k))); return n; }),
    allOf: (keys: K[]) => keys.length > 0 && keys.every((k) => sel.has(k)),
    someOf: (keys: K[]) => keys.some((k) => sel.has(k)),
    clear: () => setSel(new Set()),
  };
}

/** Başlıktaki "tümünü seç" kutusu: kısmi seçimde yarım işaret */
export const SelectAllBox: React.FC<{ all: boolean; some: boolean; onChange: () => void; label?: string }> = ({ all, some, onChange, label = 'Sayfadakilerin tümünü seç' }) => (
  <input
    type="checkbox"
    className="jv14-check"
    checked={all}
    ref={(el) => { if (el) el.indeterminate = !all && some; }}
    onChange={onChange}
    onClick={(e) => e.stopPropagation()}
    aria-label={label}
    style={{ width: 18, height: 18, accentColor: 'var(--color-accent)' }}
  />
);

const isObj = (v: unknown): v is Record<string, unknown> => !!v && typeof v === 'object' && !Array.isArray(v);
const DATE_RE = /^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?)?$/;
const fmtDate = (s: string) => {
  const d = new Date(s);
  return Number.isNaN(d.getTime()) ? s : d.toLocaleString('tr-TR', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
};
const typeName = (v: unknown) =>
  v === null || v === undefined ? 'boş' : Array.isArray(v) ? 'dizi' : typeof v === 'number' ? 'sayı' : typeof v === 'boolean' ? 'evet/hayır'
    : typeof v === 'string' ? (DATE_RE.test(v) ? 'tarih' : 'metin') : 'nesne';

/** JSON hücresi: tabloda uzun JSON yerine kısa özet */
export const JsonCell: React.FC<{ value: unknown }> = ({ value }) => {
  let v = value;
  if (typeof v === 'string' && /^[[{]/.test(v.trim())) { try { v = JSON.parse(v); } catch { /* metin */ } }
  if (Array.isArray(v)) return <span className="jv14-cell"><span>[{v.length}]</span>{v.slice(0, 3).every((x) => typeof x === 'string') && v.slice(0, 3).map((x, i) => <span key={i}>{String(x).slice(0, 24)}</span>)}</span>;
  if (isObj(v)) {
    const keys = Object.keys(v);
    return <span className="jv14-cell"><span>{'{ }'} {keys.length} alan</span>{keys.slice(0, 3).map((k) => <span key={k}>{k}</span>)}</span>;
  }
  return <>{v === null || v === undefined ? '∅' : String(v).slice(0, 140)}</>;
};

const Scalar: React.FC<{ v: unknown }> = ({ v }) => {
  if (v === null || v === undefined) return <span className="jv14-v null">boş</span>;
  if (typeof v === 'boolean') return <span className={`jv14-v ${v ? 'bool-t' : 'bool-f'}`}>{v ? 'Evet' : 'Hayır'}</span>;
  if (typeof v === 'number') return <span className="jv14-v num">{v.toLocaleString('tr-TR')}</span>;
  const s = String(v);
  if (DATE_RE.test(s)) return <span className="jv14-v" title={s}>{fmtDate(s)}</span>;
  return <span className={`jv14-v ${s.length > 80 ? 'long' : ''}`}>{s}</span>;
};

/** Görsel JSON: düz alanlar kart ızgarası; metin dizileri etiket; nesne dizileri tablo; iç nesneler açılır bölüm */
export const JsonView: React.FC<{ value: unknown; depth?: number }> = ({ value, depth = 0 }) => {
  let v = value;
  if (typeof v === 'string' && /^[[{]/.test(v.trim())) { try { v = JSON.parse(v); } catch { /* metin */ } }
  if (!isObj(v) && !Array.isArray(v)) return <Scalar v={v} />;
  if (Array.isArray(v)) return <ArrayView k="" arr={v} depth={depth} />;
  const entries = Object.entries(v);
  const scalars = entries.filter(([, x]) => !isObj(x) && !Array.isArray(x) && !(typeof x === 'string' && x.length > 160));
  const longText = entries.filter(([, x]) => typeof x === 'string' && x.length > 160);
  const complex = entries.filter(([, x]) => isObj(x) || Array.isArray(x));
  return (
    <div className="jv14">
      {scalars.length > 0 && (
        <div className="jv14-grid">
          {scalars.map(([k, x]) => (
            <div key={k} className="jv14-card">
              <span className="jv14-k"><b>{k}</b><span>{typeName(x)}</span></span>
              <Scalar v={x} />
            </div>
          ))}
        </div>
      )}
      {longText.map(([k, x]) => (
        <div key={k} className="jv14-sec">
          <span className="jv14-k"><b>{k}</b><span>· uzun metin · {String(x).length.toLocaleString('tr-TR')} karakter</span></span>
          <div className="jv14-card"><span className="jv14-v long">{String(x)}</span></div>
        </div>
      ))}
      {complex.map(([k, x]) =>
        Array.isArray(x) ? (
          <ArrayView key={k} k={k} arr={x} depth={depth} />
        ) : (
          <details key={k} className="jv14-obj" open={depth < 1}>
            <summary><b>{k}</b> · nesne · {Object.keys(x as object).length} alan</summary>
            <JsonView value={x} depth={depth + 1} />
          </details>
        ),
      )}
      {entries.length === 0 && <span className="jv14-v null">boş nesne</span>}
    </div>
  );
};

const ArrayView: React.FC<{ k: string; arr: unknown[]; depth: number }> = ({ k, arr, depth }) => {
  const head = (kind: string) => (
    <span className="jv14-k">{k && <b>{k}</b>}<span>· dizi ({kind}) · {arr.length.toLocaleString('tr-TR')} öge</span></span>
  );
  if (arr.length === 0) return <div className="jv14-sec">{head('boş')}</div>;
  if (arr.every((x) => !isObj(x) && !Array.isArray(x))) {
    return (
      <div className="jv14-sec">
        {head(typeName(arr[0]))}
        <div className="jv14-chips">{arr.slice(0, 200).map((x, i) => <span key={i}>{x === null ? 'boş' : String(x)}</span>)}</div>
      </div>
    );
  }
  if (arr.every(isObj)) {
    const cols = Array.from(new Set(arr.slice(0, 200).flatMap((x) => Object.keys(x as object)))).slice(0, 12);
    return (
      <div className="jv14-sec">
        {head('nesne · tablo')}
        <div className="jv14-tbl">
          <table>
            <thead><tr><th>#</th>{cols.map((c) => <th key={c}>{c}</th>)}</tr></thead>
            <tbody>
              {arr.slice(0, 200).map((row, i) => (
                <tr key={i}>
                  <td>{i + 1}</td>
                  {cols.map((c) => {
                    const x = (row as Record<string, unknown>)[c];
                    return <td key={c}>{isObj(x) || Array.isArray(x) ? <JsonCell value={x} /> : <Scalar v={x} />}</td>;
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
  return (
    <div className="jv14-sec">
      {head('karışık')}
      {arr.slice(0, 100).map((x, i) => (
        <details key={i} className="jv14-obj" open={depth < 1 && i < 3}>
          <summary><b>[{i}]</b> · {typeName(x)}</summary>
          <JsonView value={x} depth={depth + 1} />
        </details>
      ))}
    </div>
  );
};
