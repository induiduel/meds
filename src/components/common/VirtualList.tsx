/**
 * src/components/common/VirtualList.tsx
 *
 * 6. Madde: Sanal Kaydırma (Virtual Scrolling / Windowing)
 *
 * Sayfada binlerce satırlık veri listelenmesi gerektiğinde, tüm veriyi bir anda çekip
 * DOM'a yüklemek hem bellek tüketimini patlatır hem de arayüzü kilitler.
 *
 * Çözüm: `@tanstack/react-virtual` ile yalnızca kullanıcının ekranında o an fiziksel
 * olarak görünen 15-20 satır DOM'da tutulur. Sayfada 5.000+ soru veya terim olsa bile
 * DOM düğüm sayısı sabit kalır; tarayıcı 60-120 FPS akıcılıkta çalışır.
 */

import React, { useRef } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';

export interface VirtualListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  estimateSize?: (index: number) => number;
  overscan?: number;
  height?: number | string;
  className?: string;
  itemClassName?: string;
  getItemKey?: (item: T, index: number) => string | number;
  emptyPlaceholder?: React.ReactNode;
}

export function VirtualList<T>({
  items,
  renderItem,
  estimateSize = () => 90,
  overscan = 5,
  height = '600px',
  className = '',
  itemClassName = '',
  getItemKey,
  emptyPlaceholder,
}: VirtualListProps<T>) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize,
    overscan,
    getItemKey: (index) => (getItemKey ? getItemKey(items[index], index) : index),
  });

  if (items.length === 0) {
    return <>{emptyPlaceholder || null}</>;
  }

  const virtualItems = virtualizer.getVirtualItems();

  return (
    <div
      ref={parentRef}
      className={`overflow-auto relative ${className}`}
      style={{
        height: typeof height === 'number' ? `${height}px` : height,
        contain: 'strict',
      }}
    >
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          width: '100%',
          position: 'relative',
        }}
      >
        {virtualItems.map((virtualRow) => {
          const item = items[virtualRow.index];
          return (
            <div
              key={virtualRow.key}
              ref={virtualizer.measureElement}
              data-index={virtualRow.index}
              className={itemClassName}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                transform: `translateY(${virtualRow.start}px)`,
              }}
            >
              {renderItem(item, virtualRow.index)}
            </div>
          );
        })}
      </div>
    </div>
  );
}
