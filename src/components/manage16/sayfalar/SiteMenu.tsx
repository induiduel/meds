import React, { useEffect } from 'react';
import { SayfaBasligi } from '../kit';
import type { SayfaProps } from '../menu';

/**
 * H329: Site › Menü artık ayrı yazım yapmaz. Menü gizleme (site_ayar.menu) Görünürlük › Sayfalar sekmesindeki "Menüde"
 * sütunuyla aynı veriydi; iki yerden düzenlenmesin diye bu adres oraya yönlenir (eski yol `site/menu` kırılmaz).
 */
export default function SiteMenu({ git }: SayfaProps) {
  useEffect(() => { git('site/gorunurluk', { degistir: true }); }, [git]);
  return (
    <>
      <SayfaBasligi baslik="Menü" aciklama="Menü gizleme Görünürlük › Sayfalar sekmesine taşındı." />
      <p><a href="/manage/site/gorunurluk" onClick={(e) => { e.preventDefault(); git('site/gorunurluk'); }}>Görünürlük sayfasına git</a></p>
    </>
  );
}
