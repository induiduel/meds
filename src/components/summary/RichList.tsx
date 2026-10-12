import React from 'react';
import { ArrowRight, Check, CircleHelp, Info, Pill } from 'lucide-react';
import type { InlineListKind, RegimenBlock, RichGroup, RichItem } from './summaryStructure';

/**
 * Özet maddeleri: konu kartı (başlıklı grup), numaralı adım, onay listesi, etiket bulutu ve tedavi rejimi.
 * Renkler yalnız token: konu grubunun tonu .sr-tn-0…5 sınıfından (--tn / --tn-soft) gelir, aynı başlık
 * her bölümde aynı tonu alır. Stil: styles/summary.css (.sr-rl-*).
 */
type RenderText = (text: string) => React.ReactNode;

const TONES = 6;
const toneFor = (title: string) => {
  let h = 0;
  for (const ch of title.toLocaleLowerCase('tr')) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return h % TONES;
};

const InlineList: React.FC<{ kind: InlineListKind; items: string[]; renderText: RenderText }> = ({ kind, items, renderText }) => {
  if (kind === 'steps') {
    return (
      <ol className="sr-rl-steps">
        {items.map((it, i) => (
          <li key={i}>
            <b aria-hidden>{i + 1}</b>
            <span>{renderText(it)}</span>
          </li>
        ))}
      </ol>
    );
  }
  if (kind === 'checks') {
    return (
      <ul className="sr-rl-checks">
        {items.map((it, i) => (
          <li key={i}>
            <Check aria-hidden />
            <span>{renderText(it)}</span>
          </li>
        ))}
      </ul>
    );
  }
  // Kısa maddeler etiket gibi yan yana; uzunlar alt alta
  if (items.every((it) => it.length <= 36)) {
    return (
      <div className="sr-rl-chips">
        {items.map((it, i) => (
          <span key={i}>{renderText(it)}</span>
        ))}
      </div>
    );
  }
  return (
    <ul className="sr-rl-bullets">
      {items.map((it, i) => (
        <li key={i}>{renderText(it)}</li>
      ))}
    </ul>
  );
};

const Regimens: React.FC<{ block: RegimenBlock; renderText: RenderText }> = ({ block, renderText }) => (
  <div className="sr-rx">
    <ol>
      {block.items.map((r, i) => (
        <li key={i}>
          <div className="sr-rx-h">
            <b>{i + 1}</b>
            {block.items.length > 1 && <span>Seçenek</span>}
            {r.condition && <em>{renderText(r.condition)}</em>}
          </div>
          <ul>
            {r.drugs.map((d, di) => (
              <li key={di}>
                <i aria-hidden>{di > 0 ? '+' : <Pill />}</i>
                <span>
                  <strong>{renderText(d.name)}</strong>
                  {d.route && <small>{d.route}</small>}
                  {d.doses.map((dose, k) => (
                    <React.Fragment key={k}>
                      {k > 0 && <span className="sr-rx-or">veya</span>}
                      <span className="sr-rx-dose">{renderText(dose)}</span>
                    </React.Fragment>
                  ))}
                </span>
              </li>
            ))}
          </ul>
          {r.then && (
            <p className="sr-rx-then">
              <ArrowRight aria-hidden />
              <span>{renderText(r.then)}</span>
            </p>
          )}
          {r.note && (
            <p className="sr-rx-note">
              <Info aria-hidden />
              <span>{renderText(r.note)}</span>
            </p>
          )}
        </li>
      ))}
    </ol>
    {block.after && <p className="sr-rx-after">{renderText(block.after)}</p>}
  </div>
);

const Item: React.FC<{ item: RichItem; depth: number; renderText: RenderText }> = ({ item, depth, renderText }) => {
  // Yalnız listeden oluşan madde kendi işaretlerini taşır; ayrıca nokta konmaz
  const bare = !item.label && !item.text && (item.list || item.regimens);
  return (
    <li className={`sr-rl-item ${depth ? 'is-sub' : ''} ${bare ? 'is-bare' : ''}`}>
      {item.label && (
        <p className="sr-rl-label">
          {item.label.endsWith('?') && <CircleHelp aria-hidden />}
          <span>{renderText(item.label)}</span>
        </p>
      )}
      {item.text && <p className="sr-rl-text">{renderText(item.text)}</p>}
      {item.list && <InlineList kind={item.list.kind} items={item.list.items} renderText={renderText} />}
      {item.regimens && <Regimens block={item.regimens} renderText={renderText} />}
      {item.children.length > 0 && (
        <ul className="sr-rl-children">
          {item.children.map((c, i) => (
            <Item key={i} item={c} depth={depth + 1} renderText={renderText} />
          ))}
        </ul>
      )}
    </li>
  );
};

export const RichList: React.FC<{ groups: RichGroup[]; renderText: RenderText }> = ({ groups, renderText }) => (
  <div className="sr-rl">
    {groups.map((g, gi) => (
      <div key={gi} className={`sr-card sr-rl-group ${g.title ? `sr-tn-${toneFor(g.title)} has-title` : ''}`}>
        {g.title && (
          <div className="sr-rl-gh">
            <h4>{renderText(g.title)}</h4>
            <span>{g.items.length}</span>
          </div>
        )}
        <ul className="sr-rl-items">
          {g.items.map((it, i) => (
            <Item key={i} item={it} depth={0} renderText={renderText} />
          ))}
        </ul>
      </div>
    ))}
  </div>
);
