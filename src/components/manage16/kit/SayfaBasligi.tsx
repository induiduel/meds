import React from 'react';

/** Sayfa başlığı: başlık + açıklama + sağda eylemler; altında isteğe bağlı sekme/süzgeç alanı */
export const SayfaBasligi: React.FC<{ baslik: React.ReactNode; aciklama?: React.ReactNode; eylemler?: React.ReactNode; children?: React.ReactNode }> = ({ baslik, aciklama, eylemler, children }) => (
  <header className="m16-sayfabaslik">
    <div className="m16-sayfabaslik-ust">
      <div className="m16-sayfabaslik-metin">
        <h1>{baslik}</h1>
        {aciklama && <p>{aciklama}</p>}
      </div>
      {eylemler && <div className="m16-sayfabaslik-eylem">{eylemler}</div>}
    </div>
    {children}
  </header>
);
