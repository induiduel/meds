import React, { useState } from 'react';
import { AlertTriangle, Info, Megaphone, X } from 'lucide-react';
import { useSiteAyar } from '../../services/siteAyar';
import { aktifKurul } from '../../services/kurulTakvimi';

/**
 * Site üstü duyuru bandı (Yönetim › Site › Duyurular → site_ayar.duyuru; SSE site_ayar_changed ile canlı).
 * Gösterim: acik + başlangıç geldi + bitiş geçmedi + (hedef kurul yoksa herkes, varsa takvimdeki aktif kurul).
 * Kapatılabilir duyuru kapatılınca bu cihazda o metin için bir daha gösterilmez (metin değişirse yeniden çıkar).
 */
const KEY = 'medsoru_duyuru_kapatilan';
const imza = (s: string) => { let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; return String(h >>> 0); };
const kapatilan = (): string[] => { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch { return []; } };

export default function DuyuruBandi({ git }: { git?: (yol: string) => void }) {
  const { duyuru: d } = useSiteAyar();
  const [, yenile] = useState(0);
  if (!d || !d.acik || !d.metin?.trim()) return null;
  const simdi = Date.now();
  if (d.baslangic && Date.parse(d.baslangic) > simdi) return null;
  if (d.bitis && Date.parse(d.bitis) < simdi) return null;
  if (d.kurul?.length) {
    let k = 0;
    try { k = aktifKurul().kurul; } catch { /* takvim yok */ }
    if (!d.kurul.includes(k)) return null;
  }
  const id = imza(`${d.ton}|${d.metin}|${d.baglanti || ''}`);
  if (d.kapatilabilir !== false && kapatilan().includes(id)) return null;
  const Ik = d.ton === 'hata' ? AlertTriangle : d.ton === 'uyari' ? Megaphone : Info;
  const ic = d.baglanti && /^\//.test(d.baglanti);
  return (
    <div className={`sh-duyuru is-${d.ton}`} role={d.ton === 'hata' ? 'alert' : 'status'}>
      <Ik aria-hidden="true" />
      <span>
        {d.metin}
        {d.baglanti && (
          <>
            {' '}
            <a
              href={d.baglanti}
              {...(ic ? {} : { target: '_blank', rel: 'noopener noreferrer' })}
              onClick={(e) => { if (ic && git) { e.preventDefault(); git(d.baglanti!); } }}
            >Ayrıntı</a>
          </>
        )}
      </span>
      {d.kapatilabilir !== false && (
        <button type="button" aria-label="Duyuruyu kapat" onClick={() => {
          try { localStorage.setItem(KEY, JSON.stringify([...kapatilan().filter((x) => x !== id), id].slice(-20))); } catch { /* */ }
          yenile((n) => n + 1);
        }}><X aria-hidden="true" /></button>
      )}
    </div>
  );
}
