/**
 * Tekil ders paketi okuyucusu (R7, ICERIK_MOTORU_V3.md §6): `.medspak` (SQLite) dosyası tarayıcıda, sunucuya
 * gönderilmeden açılır. sql.js + WASM yalnız paket açılınca yüklenir. Üretici: scripts/paket/medspak_uret.py.
 */
export interface MedspakCumle {
  id: string;
  paragraf: number;
  sira: number;
  ses: string;
  ekran: string;
  duzey: number;
  vurgu: { metin: string; tur: string }[];
  slaytAdim: number | null;
  cikmis: string[];
  cizim: number;
}

export interface MedspakDers {
  meta: Record<string, string>;
  baslik: string;
  desteBaslik: string;
  slaytSayisi: number;
  cumleler: MedspakCumle[];
  paragrafSayisi: number;
  soruSayisi: number;
  ses: { varyant: string; bicim: string; sureSn: number; url: string; zamanlama: number[][] } | null;
}

export async function medspakAc(dosya: File): Promise<MedspakDers> {
  const [{ default: initSqlJs }, { default: wasmUrl }] = await Promise.all([
    import('sql.js'),
    import('sql.js/dist/sql-wasm.wasm?url'),
  ]);
  const SQL = await initSqlJs({ locateFile: () => wasmUrl });
  const db = new SQL.Database(new Uint8Array(await dosya.arrayBuffer()));
  try {
    const satir = (sql: string, p: any[] = []) => {
      const st = db.prepare(sql);
      st.bind(p);
      const out: any[] = [];
      while (st.step()) out.push(st.getAsObject());
      st.free();
      return out;
    };
    const meta: Record<string, string> = {};
    for (const r of satir('SELECT anahtar, deger FROM meta')) meta[r.anahtar] = String(r.deger);
    if (!meta.ders_id || !meta.surum) throw new Error('Bu dosya bir MeDSor ders paketi değil.');
    const cizim: Record<string, number> = {};
    for (const r of satir('SELECT cumle_id, COUNT(*) AS n FROM cizim GROUP BY cumle_id')) cizim[r.cumle_id] = Number(r.n);
    const js = (s: any, yedek: any) => { try { return s ? JSON.parse(s) : yedek; } catch { return yedek; } };
    const cumleler: MedspakCumle[] = satir('SELECT * FROM cumle ORDER BY paragraf, sira').map((r) => ({
      id: r.id, paragraf: Number(r.paragraf), sira: Number(r.sira), ses: String(r.ses || ''), ekran: String(r.ekran || r.ses || ''),
      duzey: Number(r.duzey) || 0, vurgu: js(r.vurgu, []), slaytAdim: r.slayt_adim == null ? null : Number(r.slayt_adim),
      cikmis: js(r.cikmis, []), cizim: cizim[r.id] || 0,
    }));
    const d = satir('SELECT json FROM deste LIMIT 1')[0];
    const deste = d ? js(d.json, null) : null;
    const s = satir('SELECT varyant, bicim, sure_sn, veri, zamanlama FROM ses_parca LIMIT 1')[0];
    const ses = s ? {
      varyant: String(s.varyant), bicim: String(s.bicim), sureSn: Number(s.sure_sn) || 0,
      url: URL.createObjectURL(new Blob([new Uint8Array(s.veri as Uint8Array)], { type: s.bicim === 'opus' ? 'audio/ogg; codecs=opus' : 'audio/mpeg' })),
      zamanlama: js(s.zamanlama, []),
    } : null;
    return {
      meta, baslik: meta.baslik || meta.ders_id, desteBaslik: deste?.title || '', slaytSayisi: deste?.slides?.length || 0,
      cumleler, paragrafSayisi: new Set(cumleler.map((c) => c.paragraf)).size,
      soruSayisi: Number(satir('SELECT COUNT(*) AS n FROM soru')[0]?.n || 0), ses,
    };
  } finally {
    db.close();
  }
}
