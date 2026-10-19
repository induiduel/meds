/**
 * Çevrimdışı merkezinin özel paket türleri:
 *  - `sesli:<key>` — sesli ders (canlı ders): ses + konuşma metni + PDF; indirme/silme canliDersCevrimdisi.ts'te (oynatıcı, arka plan
 *    indirme, kurul sonu silme sorusu oradadır). Katalog /api/canli-ders listesinden; sürüm = cihazdaki sesin sürümü.
 *  - `db:sorular` — çıkmış sorular + soru havuzu + komiteler + sözlük/kartlar (IndexedDB, offlineDatabaseService).
 */
import { ekKaydet, ozelKaydet, durumAl, type Paket } from './paketMotoru';

const sesliKey = (id: string) => id.slice('sesli:'.length);

export function uyarlayicilariKur() {
  ekKaydet({
    sesli: async () => {
      const [{ cdListeGetir, cdTercihVaryant }, { cdDersEtiketi }] = await Promise.all([
        import('../../components/canliDers/canliDersStore'),
        import('../../components/canliDers/canliDersKategori'),
      ]);
      const { cdCevrimdisiKayitlari } = await import('../../components/canliDers/canliDersCevrimdisiKayit');
      const cihaz = cdCevrimdisiKayitlari();
      const liste = await cdListeGetir();
      return liste.map((d, i): Paket => {
        // Cihazdaki ses varsa sürüm onunla karşılaştırılır (sunucuda yeniden üretildiyse "güncelleme var")
        const k = cihaz[d.key];
        const v = (k && d.varyantlar.find((x) => x.id === k.vid)) || cdTercihVaryant(d.varyantlar) || d.varsayilan;
        return {
          id: `sesli:${d.key}`,
          modul: 'sesli',
          grup: String(d.brans || 'Diğer').replace(/^Tıbbi\s+/, ''),
          baslik: d.baslik,
          alt: `${cdDersEtiketi(d as any)}${v?.sureSn ? ` · ${Math.round(v.sureSn / 60)} dk` : ''}${d.pdf ? ' · PDF' : ''}`,
          sira: Number(d.no) || d.sira || i,
          bayt: v?.bayt || 0,
          n: 1 + (d.pdf ? 1 : 0),
          surum: String((v as any)?.surum || v?.bayt || ''),
        };
      });
    },
    db: async () => [{
      id: 'db:sorular', modul: 'db', grup: 'Başvuru', baslik: 'Çıkmış sorular ve soru havuzu',
      alt: 'Tüm çıkmış sınav soruları, havuz soruları, komiteler, sözlük ve kartlar', sira: -1, bayt: 30_000_000, n: 1, surum: '',
    }],
  });

  ozelKaydet('sesli', {
    async indir(id, ilerle, signal) {
      const m = await import('../../components/canliDers/canliDersCevrimdisi');
      const key = sesliKey(id);
      const p = durumAl().katalog.find((x) => x.id === id);
      const toplam = p?.bayt || 0;
      const off = m.cdAbone(() => {
        const d = m.cdIsDurumu(key);
        if (d) ilerle(Math.round(d.oran * toplam), toplam);
      });
      const iptal = () => m.cdCevrimdisiIptal(key);
      signal.addEventListener('abort', iptal, { once: true });
      try {
        // Cihazda bu dersin sesi varsa aynı sesler güncellenir, yoksa tercih edilen ses iner
        const { cdCevrimdisiKayitlari, cdKayitSesleri } = await import('../../components/canliDers/canliDersCevrimdisiKayit');
        const onceki = cdKayitSesleri(cdCevrimdisiKayitlari()[key]).map((x) => x.vid);
        await m.cdCevrimdisiAyarla(key, onceki.length ? onceki : null);
        if (signal.aborted) throw Object.assign(new Error('İptal'), { name: 'AbortError' });
        const k = cdCevrimdisiKayitlari()[key];
        if (!k) throw new Error(m.cdIsDurumu(key)?.hata || 'Sesli ders indirilemedi.');
        return { surum: String(k.surum || ''), bayt: k.bayt };
      } finally {
        off();
        signal.removeEventListener('abort', iptal);
      }
    },
    async sil(id) {
      const m = await import('../../components/canliDers/canliDersCevrimdisi');
      await m.cdCevrimdisiSil([sesliKey(id)]);
    },
  });

  ozelKaydet('db', {
    async indir(_id, ilerle, signal) {
      const { offlineDatabaseService } = await import('../offlineDatabaseService');
      const tahmini = 30_000_000;
      if (signal.aborted) throw Object.assign(new Error('İptal'), { name: 'AbortError' });
      const ok = await offlineDatabaseService.downloadEntireDatabase((p) => ilerle(Math.round((p.percent / 100) * tahmini), tahmini), { yalnizSorular: true });
      if (!ok) throw new Error(offlineDatabaseService.getState().progress.stage || 'Veritabanı indirilemedi.');
      const st = await offlineDatabaseService.loadStats();
      return { surum: st.downloadedAt || String(Date.now()), bayt: Math.round(st.estimatedSizeMb * 1024 * 1024) };
    },
    async sil() {
      const { offlineDatabaseService } = await import('../offlineDatabaseService');
      await offlineDatabaseService.clearDatabase();
    },
  });

  // Daha önce (bu merkezden önce) indirilmiş sesli dersler ve veritabanı deftere alınır
  void (async () => {
    const { cdCevrimdisiKayitlari } = await import('../../components/canliDers/canliDersCevrimdisiKayit');
    const { kayitEkleDisaridan } = await import('./paketMotoru');
    for (const [key, k] of Object.entries(cdCevrimdisiKayitlari())) {
      await kayitEkleDisaridan({ id: `sesli:${key}`, surum: String(k.surum || ''), bayt: k.bayt, dosyalar: [], at: k.at, baslik: k.baslik, modul: 'sesli', grup: '' });
    }
    const { offlineDatabaseService } = await import('../offlineDatabaseService');
    const st = await offlineDatabaseService.loadStats().catch(() => null);
    if (st?.downloadedAt && st.totalItems > 0) {
      await kayitEkleDisaridan({ id: 'db:sorular', surum: st.downloadedAt, bayt: Math.round(st.estimatedSizeMb * 1024 * 1024), dosyalar: [], at: Date.parse(st.downloadedAt) || Date.now(), baslik: 'Çıkmış sorular ve soru havuzu', modul: 'db', grup: 'Başvuru' });
    }
  })().catch(() => {});

  // Sesli ders ekranından indirilen/silinen dersler defterle eş tutulur
  window.addEventListener('medsoru:cd-cevrimdisi', () => {
    void (async () => {
      const { cdCevrimdisiKayitlari } = await import('../../components/canliDers/canliDersCevrimdisiKayit');
      const { kayitEkleDisaridan, kayitSilDisaridan } = await import('./paketMotoru');
      const cd = cdCevrimdisiKayitlari();
      for (const [key, k] of Object.entries(cd)) {
        await kayitEkleDisaridan({ id: `sesli:${key}`, surum: String(k.surum || ''), bayt: k.bayt, dosyalar: [], at: k.at, baslik: k.baslik, modul: 'sesli', grup: '' });
      }
      for (const id of Object.keys(durumAl().kayitlar)) {
        if (id.startsWith('sesli:') && !cd[sesliKey(id)] && durumAl().aktif?.id !== id) await kayitSilDisaridan(id);
      }
    })();
  });
}
