import React, { useMemo, useState } from 'react';
import { Copy, Check } from 'lucide-react';

/** Salt okunur JSON (kopyala düğmeli) */
export const JsonGoruntuleyici: React.FC<{ veri: unknown; enYuksek?: number }> = ({ veri, enYuksek = 480 }) => {
  const metin = useMemo(() => { try { return JSON.stringify(veri, null, 2); } catch { return String(veri); } }, [veri]);
  const [kopya, setKopya] = useState(false);
  return (
    <div className="m16-json">
      <button type="button" className="m16-btn hayalet ikon m16-json-kopya" aria-label="Kopyala"
        onClick={() => { void navigator.clipboard?.writeText(metin); setKopya(true); setTimeout(() => setKopya(false), 1200); }}>
        {kopya ? <Check aria-hidden="true" /> : <Copy aria-hidden="true" />}
      </button>
      <pre style={{ maxHeight: enYuksek }} tabIndex={0}>{metin}</pre>
    </div>
  );
};

/** JSON düzenleyici: geçersiz JSON'da kaydet kapalı, hata satırı gösterilir */
export const JsonDuzenleyici: React.FC<{ deger: unknown; kaydet: (yeni: unknown) => void | Promise<void>; iptal?: () => void; satir?: number }> = ({ deger, kaydet, iptal, satir = 18 }) => {
  const ilk = useMemo(() => JSON.stringify(deger, null, 2), [deger]);
  const [metin, setMetin] = useState(ilk);
  const [mesgul, setMesgul] = useState(false);
  const hata = useMemo(() => { try { JSON.parse(metin); return ''; } catch (e: any) { return e.message; } }, [metin]);
  return (
    <div className="m16-jsonduz">
      <textarea className="m16-girdi m16-kod" rows={satir} value={metin} onChange={(e) => setMetin(e.target.value)} spellCheck={false} aria-invalid={Boolean(hata)} />
      {hata && <p className="m16-alan-hata">{hata}</p>}
      <div className="m16-form-eylem">
        {iptal && <button type="button" className="m16-btn hayalet" onClick={iptal}>Vazgeç</button>}
        <button type="button" className="m16-btn birincil" disabled={Boolean(hata) || metin === ilk || mesgul}
          onClick={async () => { setMesgul(true); try { await kaydet(JSON.parse(metin)); } finally { setMesgul(false); } }}>Kaydet</button>
      </div>
    </div>
  );
};
