import React from 'react';
import { KatalogSayfasi, adminIstek, bildir, onayIste } from '../kit';
import type { SayfaProps } from '../menu';

/** Kaynaklar › Çöp kutusu: katalogdan silinenler; geri yükle ya da kalıcı sil. */
export default function Cop(_p: SayfaProps) {
  const geri = async (ids: string[], temizle: () => void) => {
    try {
      const r = await adminIstek<{ restored: number; errors: string[] }>('/api/admin/catalog/trash/restore', { yontem: 'POST', govde: { ids } });
      bildir(`${r.restored} kayıt geri yüklendi${r.errors?.length ? ` · ${r.errors.join('; ')}` : ''}`, r.errors?.length ? 'kotu' : 'iyi');
      temizle();
    } catch (e: any) { bildir(e?.message || 'Geri yüklenemedi', 'kotu'); }
  };
  const sil = async (ids: string[], temizle: () => void) => {
    if (!(await onayIste({ baslik: `${ids.length} kayıt kalıcı olarak silinsin mi?`, aciklama: 'Bu işlem geri alınamaz.', tehlikeli: true, yazilacak: 'SIL', onayMetni: 'Kalıcı sil' }))) return;
    try {
      const r = await adminIstek<{ deleted: number }>('/api/admin/catalog/trash/delete', { yontem: 'POST', govde: { ids } });
      bildir(`${r.deleted} kayıt kalıcı silindi`);
      temizle();
    } catch (e: any) { bildir(e?.message || 'Silinemedi', 'kotu'); }
  };
  return <KatalogSayfasi varlik="trash" kimlik="kaynak-cop" baslik="Çöp kutusu"
    topluEylemler={(ids, t) => <>
      <button type="button" className="m16-btn birincil" onClick={() => void geri(ids, t)}>Geri yükle</button>
      <button type="button" className="m16-btn tehlike" onClick={() => void sil(ids, t)}>Kalıcı sil</button>
    </>} />;
}
