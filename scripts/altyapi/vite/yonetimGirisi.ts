import type { Plugin } from 'vite';

/**
 * Geliştirme sunucusunda /manage* gezinmelerine manage.html (yönetim ayrı girişi) verilir.
 * Üretimde aynı işi server.ts yapar. Varlık/modül istekleri (uzantılı yollar, /@vite, /src) dokunulmaz.
 */
export function yonetimGirisi(): Plugin {
  return {
    name: 'meds-yonetim-girisi',
    configureServer(server) {
      server.middlewares.use((req, _res, next) => {
        const url = req.url || '';
        const yol = url.split('?')[0];
        if (/^\/manage(\/|$)/.test(yol) && !/\.[a-z0-9]+$/i.test(yol) && String(req.headers.accept || '').includes('text/html')) {
          req.url = '/manage.html' + (url.includes('?') ? url.slice(url.indexOf('?')) : '');
        }
        next();
      });
    },
  };
}
