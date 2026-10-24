/**
 * Erişilebilir temel bileşenler (shadcn/ui yaklaşımı: Radix ilkelleri + sitenin kendi tasarım belirteçleri).
 * Radix odak yönetimi, Esc/dış tıklama ile kapanma, ekran kenarına çarpınca yer değiştirme ve klavye gezintisini verir;
 * görünüm `styles/ui-radix.css` içindeki `.rx-*` sınıflarında, renkler palet belirteçlerinden (var(--color-*)).
 */
import React from 'react';
import * as PopoverPrim from '@radix-ui/react-popover';
import * as ToggleGroupPrim from '@radix-ui/react-toggle-group';
import '../../styles/ui-radix.css';

export const Popover = PopoverPrim.Root;
export const PopoverTrigger = PopoverPrim.Trigger;
export const PopoverClose = PopoverPrim.Close;

/** Ekran kenarından 16 px içeride kalan, portallı açılır panel */
export const PopoverContent = React.forwardRef<
  React.ElementRef<typeof PopoverPrim.Content>,
  React.ComponentPropsWithoutRef<typeof PopoverPrim.Content>
>(function PopoverContent({ className = '', align = 'end', sideOffset = 6, collisionPadding = 16, ...props }, ref) {
  return (
    <PopoverPrim.Portal>
      <PopoverPrim.Content ref={ref} align={align} sideOffset={sideOffset} collisionPadding={collisionPadding}
        className={`rx-pop ${className}`} {...props} />
    </PopoverPrim.Portal>
  );
});

/** Tek seçimli düğme grubu (ok tuşlarıyla gezilir) */
export const ToggleGroup = React.forwardRef<
  React.ElementRef<typeof ToggleGroupPrim.Root>,
  React.ComponentPropsWithoutRef<typeof ToggleGroupPrim.Root>
>(function ToggleGroup({ className = '', ...props }, ref) {
  return <ToggleGroupPrim.Root ref={ref} className={`rx-tg ${className}`} {...props} />;
});

export const ToggleGroupItem = React.forwardRef<
  React.ElementRef<typeof ToggleGroupPrim.Item>,
  React.ComponentPropsWithoutRef<typeof ToggleGroupPrim.Item>
>(function ToggleGroupItem({ className = '', ...props }, ref) {
  return <ToggleGroupPrim.Item ref={ref} className={`rx-tg-i ${className}`} {...props} />;
});
