/**
 * Çevrimdışı merkezinin özel paket türleri:
 *  - `sesli:<key>` — sesli ders (canlı ders): ses + konuşma metni + PDF; indirme/silme canliDersCevrimdisi.ts'te (oynatıcı, arka plan
 *    indirme, kurul sonu silme sorusu oradadır). Katalog /api/canli-ders listesinden; sürüm = cihazdaki sesin sürümü.
 *  - `db:sorular` — çıkmış sorular + soru havuzu + komiteler + sözlük/kartlar (IndexedDB, offlineDatabaseService).
 */
import { ekKaydet, ozelKaydet, durumAl, anahtar, medspakAdresi, PAKET_CACHE, type Paket } from './paketMotoru';

const sesliKey = (id: string) => id.slice('sesli:'.length);

/** Her iki dönemin dersleri (.medspak'lı 2025-26 dersleri ayrı listededir); aynı anahtar bir kez */
async function tumDersler() {
  const { cdListeGetir } = await import('../../components/canliDers/canliDersStore');
  const [a, b] = await Promise.all([cdListeGetir().catch(() => []), cdListeGetir(false, '2025-2026').catch(() => [])]);
  const gorulen = new Set<string>();
  return [...a, ...b].filter((d) => !gorulen.has(d.key) && gorulen.add(d.key));
}

export function uyarlayicilariKur() {
  ekKaydet({
    sesli: async () => {
      const [{ cdTercihVaryant }, { cdDersEtiketi }] = await Promise.all([
        import('../../components/canliDers/canliDersStore'),
        import('../../components/canliDers/canliDersKategori'),
      ]);
      const { cdCevrimdisiKayitlari } = await import('../../components/canliDers/canliDersCevrimdisiKayit');
      const cihaz = cdCevrimdisiKayitlari();
      const liste = await tumDersler();
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
          dersNo: Number(d.no) || undefined,
          desteId: d.desteId,
        };
      });
    },
    // .medspak ders paketi (PDF + ses + deste + günlük tek dosyada): ders birimine dahil, kendi sürümüyle güncellenir
    medspak: async () => {
      const { cdDersEtiketi } = await import('../../components/canliDers/canliDersKategori');
      const liste = await tumDersler();
      return liste.filter((d) => d.medspakVar).map((d, i): Paket => ({
        id: `medspak:${d.key}`,
        modul: 'medspak',
        grup: String(d.brans || 'Diğer').replace(/^Tıbbi\s+/, ''),
        baslik: d.baslik,
        alt: `Ders paketi (.medspak) · ${cdDersEtiketi(d as any)}`,
        sira: Number(d.no) || d.sira || i,
        bayt: d.medspakBayt || 0,
        n: 1,
        surum: String(d.medspakSurum || d.medspakBayt || ''),
        dersNo: Number(d.no) || undefined,
        desteId: d.desteId,
      }));
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

  ozelKaydet('medspak', {
    async indir(id, ilerle, signal) {
      const { cdMedspakUrl } = await import('../../components/canliDers/canliDersStore');
      const key = id.slice('medspak:'.length);
      const p = durumAl().katalog.find((x) => x.id === id);
      const r = await fetch(cdMedspakUrl(key), { cache: 'no-store', signal });
      if (!r.ok) throw new Error(r.status === 404 ? 'Bu ders paketi sunucuda yok.' : `Ders paketi alınamadı (${r.status}).`);
      const toplam = Number(r.headers.get('Content-Length')) || p?.bayt || 0;
      const parcalar: BlobPart[] = [];
      let alinan = 0;
      if (r.body) {
        const o = r.body.getReader();
        for (;;) {
          const { done, value } = await o.read();
          if (done) break;
          parcalar.push(value as Uint8Array<ArrayBuffer>);
          alinan += value.byteLength;
          ilerle(alinan, toplam);
        }
      } else parcalar.push(await r.blob());
      const blob = new Blob(parcalar, { type: 'application/vnd.sqlite3' });
      if (toplam && Math.abs(blob.size - toplam) > 1024 && r.headers.get('Content-Length')) throw new Error('Ders paketi eksik indi. Yeniden dene.');
      // Dosya sağlam mı: sql.js ile aç (bozuksa cihaza hiç yazılmaz, hata gösterilir)
      const { medspakAc } = await import('../medspakOku');
      const ders = await medspakAc(new File([blob], `${key}.medspak`));
      ders.ses && URL.revokeObjectURL(ders.ses.url);
      ders.pdfler.forEach((x) => URL.revokeObjectURL(x.url));
      const surum = p?.surum || '';
      const dosya = { u: medspakAdresi(key), v: surum, b: blob.size };
      const cache = await caches.open(PAKET_CACHE);
      await cache.put(anahtar(dosya), new Response(blob, { headers: { 'Content-Type': 'application/vnd.sqlite3', 'Content-Length': String(blob.size), 'X-Paket-Surum': surum } }));
      return { surum, bayt: blob.size, dosyalar: [dosya] };
    },
    async sil(id) {
      const k = durumAl().kayitlar[id];
      const cache = await caches.open(PAKET_CACHE);
      for (const d of k?.dosyalar || []) await cache.delete(anahtar(d));
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
