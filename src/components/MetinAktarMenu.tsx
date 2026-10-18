/** Ders metnini .pdf / .docx / .md / .txt olarak indiren açılır seçici (Sesli ders ve Etkileşimli dersler). */
import React, { useState } from 'react';
import { Download, FileDown, Loader2 } from 'lucide-react';
import type { AktarBelge, AktarBicim } from '../services/metinDisaAktar';
import '../styles/metin-aktar.css';

const BICIMLER: { id: AktarBicim; ad: string; alt: string }[] = [
  { id: 'pdf', ad: 'PDF', alt: 'Yazdırmaya hazır' },
  { id: 'docx', ad: 'Word', alt: '.docx, düzenlenebilir' },
  { id: 'md', ad: 'Markdown', alt: '.md, not uygulamaları' },
  { id: 'txt', ad: 'Düz metin', alt: '.txt' },
];

export function MetinAktarMenu({ belge, dosyaAdi, dugmeSinif = 'cd-btn', etiket = 'Metni dışa aktar' }: {
  belge: () => AktarBelge; dosyaAdi: string; dugmeSinif?: string; etiket?: string;
}) {
  const [acik, setAcik] = useState(false);
  const [calisan, setCalisan] = useState<AktarBicim | null>(null);
  const [hata, setHata] = useState('');
  const indir = async (b: AktarBicim) => {
    setCalisan(b); setHata('');
    try {
      const { metniIndir } = await import('../services/metinDisaAktar');
      await metniIndir(belge(), b, dosyaAdi);
    } catch (e) {
      console.warn('dışa aktarma', e);
      setHata('Dosya oluşturulamadı, yeniden dene.');
    } finally { setCalisan(null); }
  };
  return (
    <div className="cd-aktar">
      <button type="button" className={`${dugmeSinif}${acik ? ' is-on' : ''}`} aria-expanded={acik} onClick={() => setAcik((x) => !x)} title="Ders metnini dosya olarak indir">
        <FileDown aria-hidden /> <span>{etiket}</span>
      </button>
      {acik && (
        <div className="cd-aktar-liste" role="group" aria-label="Dosya biçimi">
          {BICIMLER.map((b) => (
            <button key={b.id} type="button" className="cd-aktar-bicim" disabled={!!calisan} onClick={() => indir(b.id)}>
              {calisan === b.id ? <Loader2 aria-hidden className="cd-aktar-don" /> : <Download aria-hidden />}
              <b>{b.ad}</b><small>{b.alt}</small>
            </button>
          ))}
          {hata && <p className="cd-aktar-hata" role="alert">{hata}</p>}
        </div>
      )}
    </div>
  );
}
