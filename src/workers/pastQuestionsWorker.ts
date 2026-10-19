/**
 * Çıkmış soruların ilk yüklemesi: ~40 MB'lık listeyi indirme, JSON ayrıştırma ve IndexedDB'ye yazma
 * ana iş parçacığının dışında yapılır (ana iş parçacığında 4 sn'lik donmaydı). Sunucu listeyi zaten
 * istemci biçiminde (toClientPastQuestion) gönderir; burada yeniden sadeleştirme yapılmaz.
 * İstemci: pastQuestionsCache.initialLoadInWorker
 */
type Req = { url: string; dbName: string; dbVersion: number; store: string; metaStore: string };

const ctx = self as unknown as {
  onmessage: ((e: MessageEvent<Req>) => void) | null;
  postMessage: (m: unknown) => void;
};

function openDb(r: Req): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(r.dbName, r.dbVersion);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(r.store)) {
        const s = db.createObjectStore(r.store, { keyPath: 'id' });
        s.createIndex('by_committee', 'committeeId', { unique: false });
        s.createIndex('by_discipline', 'discipline', { unique: false });
        s.createIndex('by_updatedAt', 'updatedAt', { unique: false });
      }
      if (!db.objectStoreNames.contains(r.metaStore)) db.createObjectStore(r.metaStore, { keyPath: 'key' });
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

ctx.onmessage = async (e) => {
  const r = e.data;
  try {
    const res = await fetch(r.url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const json = await res.json();
    const questions: any[] = Array.isArray(json?.questions) ? json.questions.filter((q: any) => q && q.id) : [];
    let maxTime = '';
    for (const q of questions) if (q.updatedAt && q.updatedAt > maxTime) maxTime = q.updatedAt;
    let stored = false;
    if (questions.length) {
      try {
        const db = await openDb(r);
        await new Promise<void>((resolve, reject) => {
          const tx = db.transaction(r.store, 'readwrite');
          const s = tx.objectStore(r.store);
          for (const q of questions) s.put(q);
          tx.oncomplete = () => resolve();
          tx.onerror = () => reject(tx.error);
          tx.onabort = () => reject(tx.error);
        });
        db.close();
        stored = true;
      } catch { /* depolama kapalı/dolu: liste yine döner, ana iş parçacığı bellekte tutar */ }
    }
    ctx.postMessage({ ok: true, questions, maxTime, stored });
  } catch (err: any) {
    ctx.postMessage({ ok: false, error: String(err?.message || err) });
  }
};
