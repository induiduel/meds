import React from 'react';

/**
 * Bento ızgara — sayfa kart/pano ızgaralarının ortak tabanı (styles/bento.css).
 * Sütun eşikleri en yakın kap sorgulu ataya göredir; sayfa kökü `container-type: inline-size` olmalı.
 *
 *   <Bento duo rhythm list as="ul">…<BentoItem as="li" size="wide">…</BentoItem></Bento>
 */
export type BentoSize = 'auto' | 'mini' | 'half' | 'side' | 'wide' | 'full';

const cx = (...parts: (string | false | null | undefined)[]) => parts.filter(Boolean).join(' ');

/** Öğe sınıfı: düz elemanlarda `className={bentoSize('wide', true)}` biçiminde de kullanılabilir. */
export const bentoSize = (size: BentoSize = 'auto', tall = false) => cx(size !== 'auto' && `bt-${size}`, tall && 'bt-tall');

type BentoProps = React.HTMLAttributes<HTMLElement> & {
  as?: React.ElementType;
  /** Geniş kapta en çok 2 kart yan yana (varsayılan 3). */
  duo?: boolean;
  /** Eşit kartlı listelere geniş/dar ritim. */
  rhythm?: boolean;
  /** Akış modunda tek sütuna iner. */
  list?: boolean;
  /** Boşlukları sonraki küçük kartlarla doldur (görsel sıra değişebilir). */
  dense?: boolean;
};

export const Bento = React.forwardRef<HTMLElement, BentoProps>(function Bento(
  { as: Tag = 'div', duo, rhythm, list, dense, className, ...rest },
  ref,
) {
  return <Tag ref={ref} className={cx('bento', duo && 'is-duo', rhythm && 'is-rhythm', list && 'is-list', dense && 'is-dense', className)} {...rest} />;
});

type BentoItemProps = React.HTMLAttributes<HTMLElement> & {
  as?: React.ElementType;
  size?: BentoSize;
  tall?: boolean;
};

export const BentoItem = React.forwardRef<HTMLElement, BentoItemProps>(function BentoItem(
  { as: Tag = 'div', size = 'auto', tall, className, ...rest },
  ref,
) {
  return <Tag ref={ref} className={cx(bentoSize(size, tall), className) || undefined} {...rest} />;
});

export default Bento;
