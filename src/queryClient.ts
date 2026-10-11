import { QueryClient } from '@tanstack/react-query';

/**
 * Global TanStack QueryClient yapılandırması.
 * 
 * - staleTime: 5 dakika (varsayılan taze kalma süresi; bu sürede sayfa/sekme geçişlerinde ağ isteği atılmaz)
 * - gcTime: 30 dakika (kullanılmayan sorguların bellekte tutulma süresi)
 * - refetchOnWindowFocus: false (sekme değiştirip dönünce sunucuya gereksiz istek yığılmasını önler)
 * - retry: 1 (başarısız isteklerde 1 kez yeniden dener)
 */
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 dakika
      gcTime: 1000 * 60 * 30,    // 30 dakika
      refetchOnWindowFocus: false,
      refetchOnReconnect: true,
      retry: 1,
    },
  },
});
