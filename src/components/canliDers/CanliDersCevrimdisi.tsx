/**
 * Canlı ders · çevrimdışı arayüzü: "Çevrimdışı kullan" düğmesi (liste satırı + ders ekranı), inecek ses seçimi penceresi, internet yokken liste
 * şeridi ve kurul bitiminden 3 gün sonra çıkan silme sorusu (CanliDersDockGate tembel yükler).
 */
import React, { useEffect, useMemo, useState } from 'react';
import { createPortal } from 'react-dom';
import { Check, CheckCircle2, CloudDownload, FileText, RefreshCw, Trash2, WifiOff, X } from 'lucide-react';
import { Dialog } from '../ui/Dialog';
import { toast } from '../ui/Toast';
import { userNotificationService } from '../../services/userNotificationService';
import { cdDetayGetir, cdSesKisa, fmtMb, fmtSure, useCd, type CdListeDers, type CdVaryant } from './canliDersStore';
import {
  cdCevrimdisiAyarla, cdCevrimdisiDogrula, cdCevrimdisiHataSil, cdCevrimdisiIptal, cdCevrimdisiPdfBilgi, cdCevrimdisiSil, cdKurulBilgisi, cdSesEski,
  tercihVid, useCdCevrimdisi,
} from './canliDersCevrimdisi';
import { cdCevrimdisiKayitlari, cdKayitSesleri, cdSilinebilirKurullar, cdSoruDurumu, cdSoruYaz } from './canliDersCevrimdisiKayit';
import '../../styles/canli-ders-cevrimdisi.css';

let dogrulandi = false;

export function useCevrimici(): boolean {
  const [on, setOn] = useState(() => (typeof navigator === 'undefined' ? true : navigator.onLine));
  useEffect(() => {
    const f = () => setOn(navigator.onLine);
    window.addEventListener('online', f);
    window.addEventListener('offline', f);
    return () => {
      window.removeEventListener('online', f);
      window.removeEventListener('offline', f);
    };
  }, []);
  return on;
}

/** Boş yer: 1 GB üstünde GB */
const fmtYer = (b: number) => (b >= 1073741824 ? `${(b / 1073741824).toFixed(1).replace('.', ',')} GB` : fmtMb(b) || '0 MB');
const tarihTr = (ms: number) => new Date(ms).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' });

/** Çevrimdışı kullan / Cihazda / Güncelle düğmesi. `varyantlar`: ses seçimi ve güncel sürüm karşılaştırması için. */
export function CevrimdisiDugme({ dersKey, baslik, varyantlar, kucuk }: { dersKey: string; baslik: string; varyantlar?: CdVaryant[]; kucuk?: boolean }) {
  const { kayit, is } = useCdCevrimdisi(dersKey);
  const caliyorVid = useCd((s) => (s.key === dersKey ? s.vid : null));
  const online = useCevrimici();
  const [pencere, setPencere] = useState(false);
  useEffect(() => {
    if (!dogrulandi) { dogrulandi = true; void cdCevrimdisiDogrula(); }
  }, []);
  const sesler = cdKayitSesleri(kayit);
  const eskiler = (varyantlar || []).filter((v) => cdSesEski(kayit, v));

  const uygula = async (vidler: string[] | null) => {
    const vardi = !!kayit;
    try {
      await cdCevrimdisiAyarla(dersKey, vidler, { caliyorVid });
      const k = cdCevrimdisiKayitlari()[dersKey];
      if (!k) { toast.info('Ders cihazdan silindi', baslik); return; }
      const n = cdKayitSesleri(k).length;
      const kb = cdKurulBilgisi(dersKey);
      toast.success(
        vardi ? 'Cihazdaki ders güncellendi' : 'Ders cihaza indirildi',
        `${baslik}: ${n > 1 ? `${n} ses` : 'ses'}, metin ve slaytlar internetsiz açılır${kb ? `; Kurul ${kb.kurul} boyunca (${tarihTr(kb.silinebilir)} tarihine dek) cihazda kalır` : ''}.${k.bayt ? ` Toplam ${fmtMb(k.bayt)}.` : ''}`,
      );
    } catch (e: any) {
      toast.error('Ders indirilemedi', e?.message || 'Bağlantını kontrol edip tekrar dene.');
    }
  };
  const ac = () => {
    cdCevrimdisiHataSil(dersKey);
    // Tek sesli derste seçilecek bir şey yok: doğrudan indir
    if (!kayit && (varyantlar?.length ?? 0) <= 1) void uygula(null);
    else setPencere(true);
  };
  const pencereEl = pencere && (
    <CevrimdisiSesPenceresi
      dersKey={dersKey}
      baslik={baslik}
      varyantlar={varyantlar}
      caliyorVid={caliyorVid}
      onKapat={() => setPencere(false)}
      onUygula={(vidler) => { setPencere(false); void uygula(vidler); }}
    />
  );

  if (is && !is.hata) {
    const yuzde = Math.round(is.oran * 100);
    return (
      <button
        type="button"
        className={`cd-btn cd-cd-dugme is-iniyor${kucuk ? ' is-ince' : ''}`}
        onClick={() => cdCevrimdisiIptal(dersKey)}
        aria-label={`İndiriliyor %${yuzde}: ${baslik}. Durdurmak için dokun`}
        title="İndiriliyor — durdurmak için dokun"
        style={{ '--cd-oran': is.oran } as React.CSSProperties}
      >
        <span className="cd-spin" aria-hidden />
        <span>%{yuzde}</span>
      </button>
    );
  }
  if (kayit) {
    const kb = cdKurulBilgisi(dersKey);
    return (
      <span className="cd-cd-grup">
        <button
          type="button"
          className={`cd-btn cd-cd-dugme is-cihazda${kucuk ? ' is-ince' : ''}`}
          onClick={() => setPencere(true)}
          aria-haspopup="dialog"
          aria-label={`Cihazda: ${baslik}, ${sesler.length} ses${kayit.bayt ? `, ${fmtMb(kayit.bayt)}` : ''}. Sesleri düzenlemek ya da silmek için dokun`}
          title={`Cihazda · ${sesler.map((x) => x.etiket || x.vid).join(', ')}${kayit.bayt ? ` · ${fmtMb(kayit.bayt)}` : ''}${kb ? ` · Kurul ${kb.kurul} bitiminden 3 gün sonra (${tarihTr(kb.silinebilir)}) silmek için sorulur` : ''}. Sesleri düzenlemek için dokun.`}
        >
          <CheckCircle2 aria-hidden />
          <span>Cihazda</span>
          {sesler.length > 1 && <span className="cd-cd-sayi" aria-hidden>{sesler.length}</span>}
        </button>
        {eskiler.length > 0 && online && (
          <button
            type="button"
            className={`cd-btn is-ikon cd-cd-guncelle${kucuk ? ' is-ince' : ''}`}
            onClick={() => void uygula(sesler.map((x) => x.vid))}
            aria-label={`Güncelle: ${baslik} (${eskiler.length} ses yenilendi)`}
            title={`${eskiler.map(cdSesKisa).join(', ')} yenilendi — cihazdaki kopyayı güncelle`}
          >
            <RefreshCw aria-hidden />
          </button>
        )}
        {pencereEl}
      </span>
    );
  }
  return (
    <>
      <button
        type="button"
        className={`cd-btn cd-cd-dugme${is?.hata ? ' is-hata' : ''}${kucuk ? ' is-ince' : ''}`}
        onClick={ac}
        disabled={!online}
        aria-haspopup={(varyantlar?.length ?? 0) > 1 ? 'dialog' : undefined}
        aria-label={`Çevrimdışı kullan: ${baslik} (ses, metin ve slaytları cihaza indir)`}
        title={is?.hata ? `${is.hata} Tekrar dene.` : online ? ((varyantlar?.length ?? 0) > 1 ? 'İnecek sesleri seç — internetsiz dinle' : 'Ses, metin ve slaytları cihaza indir — internetsiz dinle') : 'İndirmek için internet gerekir'}
      >
        <CloudDownload aria-hidden />
        <span>{is?.hata ? 'Tekrar dene' : 'Çevrimdışı'}</span>
      </button>
      {pencereEl}
    </>
  );
}

/** Kaynak rozeti: "Edge", "Gemini" … (ses adıyla birlikte cdSesKisa'dan ayrıştırılır) */
const sesParca = (v: CdVaryant) => {
  const [ad, kaynak] = cdSesKisa(v).split(' · ');
  return { ad, kaynak: kaynak || '' };
};

/**
 * Çevrimdışı ses seçimi: dersin seslerinden hangilerinin cihaza ineceği (çoklu seçim). Cihazdakiler işaretli gelir;
 * işareti kaldırılan ses silinir, hepsi kaldırılırsa ders cihazdan çıkar. Metin ve slaytlar her durumda bir kez iner.
 */
export function CevrimdisiSesPenceresi({
  dersKey, baslik, varyantlar: verilen, caliyorVid, onKapat, onUygula,
}: {
  dersKey: string;
  baslik: string;
  varyantlar?: CdVaryant[];
  caliyorVid?: string | null;
  onKapat: () => void;
  onUygula: (vidler: string[]) => void;
}) {
  const { kayit } = useCdCevrimdisi(dersKey);
  const online = useCevrimici();
  const [varyantlar, setVaryantlar] = useState<CdVaryant[] | null>(verilen?.length ? verilen : null);
  const [pdf, setPdf] = useState<{ bayt: number; sayi: number; cihazda: boolean } | null>(null);
  const [bos, setBos] = useState<number | null>(null);
  const cihazdaki = useMemo(() => new Set(cdKayitSesleri(kayit).map((x) => x.vid)), [kayit]);
  const [secim, setSecim] = useState<Set<string>>(() => {
    if (cihazdaki.size) return new Set(cihazdaki);
    const t = verilen?.length ? tercihVid(verilen, caliyorVid) : null;
    return new Set(t ? [t] : []);
  });
  const [silOnay, setSilOnay] = useState(false);

  useEffect(() => {
    let iptal = false;
    if (!varyantlar) {
      cdDetayGetir(dersKey).then((d) => {
        if (iptal) return;
        setVaryantlar(d.varyantlar);
        if (!cihazdaki.size) { const t = tercihVid(d.varyantlar, caliyorVid); if (t) setSecim(new Set([t])); }
      }).catch(() => !iptal && setVaryantlar([]));
    }
    cdCevrimdisiPdfBilgi(dersKey).then((p) => !iptal && setPdf(p)).catch(() => {});
    navigator.storage?.estimate?.().then((e) => {
      if (!iptal && e.quota != null) setBos(Math.max(0, e.quota - (e.usage || 0)));
    }).catch(() => {});
    return () => { iptal = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dersKey]);

  const vs = varyantlar || [];
  const degistir = (id: string) => {
    setSilOnay(false);
    setSecim((s) => {
      const n = new Set(s);
      if (n.has(id)) n.delete(id); else n.add(id);
      return n;
    });
  };
  const secilebilir = (v: CdVaryant) => online || cihazdaki.has(v.id);
  const hepsi = vs.filter(secilebilir);
  const hepsiSecili = hepsi.length > 0 && hepsi.every((v) => secim.has(v.id));

  const inecek = vs.filter((v) => secim.has(v.id) && (!cihazdaki.has(v.id) || cdSesEski(kayit, v)));
  const silinecek = vs.filter((v) => cihazdaki.has(v.id) && !secim.has(v.id));
  const pdfInecek = secim.size > 0 && pdf && !pdf.cihazda ? pdf.bayt : 0;
  const inecekBayt = inecek.reduce((a, v) => a + (v.bayt || 0), 0) + pdfInecek;
  const acilacakBayt = silinecek.reduce((a, v) => a + (v.bayt || 0), 0);
  const tumunuSil = !!kayit && secim.size === 0;
  const degisiklikYok = !inecek.length && !silinecek.length && !tumunuSil;
  const yerYetmez = bos != null && inecekBayt > bos;

  const ozet = tumunuSil
    ? `Ders cihazdan silinir${kayit?.bayt ? ` · ${fmtMb(kayit.bayt)} yer açılır` : ''}`
    : [
        inecek.length ? `${inecek.length} ses${pdfInecek ? ' + slaytlar' : ''} inecek` : pdfInecek ? 'Slaytlar inecek' : '',
        inecekBayt ? fmtMb(inecekBayt) : '',
        silinecek.length ? `${silinecek.length} ses silinecek${acilacakBayt ? ` (${fmtMb(acilacakBayt)})` : ''}` : '',
      ].filter(Boolean).join(' · ') || (secim.size ? 'Seçtiğin sesler zaten cihazda' : 'İnecek sesi seç');

  const anaEtiket = tumunuSil
    ? 'Cihazdan sil'
    : kayit
      ? 'Değişiklikleri uygula'
      : `İndir${secim.size ? ` (${secim.size} ses)` : ''}`;
  const kb = cdKurulBilgisi(dersKey);

  const footer = (
    <div className="cd-cd-p-alt">
      <p className={`cd-cd-p-ozet${tumunuSil ? ' is-sil' : ''}${yerYetmez ? ' is-uyari' : ''}`} aria-live="polite">
        {yerYetmez ? `Cihazda yeterli yer yok (boş ~${fmtYer(bos!)}).` : ozet}
      </p>
      <div className="cd-cd-p-eylem">
        <button type="button" className="ms-btn is-ghost" onClick={onKapat}>Vazgeç</button>
        <button
          type="button"
          className={`ms-btn ${tumunuSil ? 'is-danger' : 'is-primary'}`}
          disabled={degisiklikYok || yerYetmez || !varyantlar}
          onClick={() => {
            if (tumunuSil && kb && Date.now() < kb.silinebilir && !silOnay) { setSilOnay(true); return; }
            onUygula(vs.filter((v) => secim.has(v.id)).map((v) => v.id));
          }}
        >
          {tumunuSil ? <Trash2 aria-hidden /> : <CloudDownload aria-hidden />}
          {silOnay ? 'Evet, sil' : anaEtiket}
        </button>
      </div>
    </div>
  );

  return createPortal(
    <Dialog title="Çevrimdışı dinle" subtitle={baslik} onClose={onKapat} footer={footer} width="max-w-md">
      <div className="cd-cd-p">
        <div className="cd-cd-p-bas">
          <span className="cd-cd-p-baslik" id={`cd-cd-p-${dersKey}`}>Cihaza inecek sesler</span>
          {hepsi.length > 1 && (
            <button type="button" className="cd-cd-p-hepsi" onClick={() => { setSilOnay(false); setSecim(hepsiSecili ? new Set() : new Set(hepsi.map((v) => v.id))); }}>
              {hepsiSecili ? 'Hiçbiri' : 'Tümünü seç'}
            </button>
          )}
        </div>

        {!varyantlar ? (
          <div className="cd-cd-p-yuk" role="status"><span className="cd-spin" aria-hidden /> Sesler yükleniyor…</div>
        ) : !vs.length ? (
          <p className="cd-cd-p-bos">Bu dersin sesi yok.</p>
        ) : (
          <ul className="cd-cd-p-liste" role="group" aria-labelledby={`cd-cd-p-${dersKey}`}>
            {vs.map((v) => {
              const { ad, kaynak } = sesParca(v);
              const on = secim.has(v.id);
              const var_ = cihazdaki.has(v.id);
              const eski = cdSesEski(kayit, v);
              const kilit = !secilebilir(v);
              return (
                <li key={v.id}>
                  <label className={`cd-cd-p-ses${on ? ' is-on' : ''}${kilit ? ' is-kilit' : ''}`} title={v.etiket}>
                    <input type="checkbox" checked={on} disabled={kilit} onChange={() => degistir(v.id)} />
                    <span className="cd-cd-p-kutu" aria-hidden><Check /></span>
                    <span className="cd-cd-p-ad">
                      <b>{ad}</b>
                      <span className="cd-cd-p-meta">
                        {kaynak && <span className="cd-cd-p-kaynak">{kaynak}</span>}
                        {v.sureSn > 0 && <span>{fmtSure(v.sureSn)}</span>}
                        {v.bayt > 0 && <span>{fmtMb(v.bayt)}</span>}
                      </span>
                    </span>
                    <span className="cd-cd-p-rozet">
                      {var_ && !eski && (on ? <i className="is-var">Cihazda</i> : <i className="is-sil">Silinecek</i>)}
                      {var_ && eski && <i className="is-yeni">{on ? 'Güncellenecek' : 'Silinecek'}</i>}
                      {!var_ && caliyorVid === v.id && <i>Oynatıcıda</i>}
                      {kilit && <i>İnternet gerekir</i>}
                    </span>
                  </label>
                </li>
              );
            })}
          </ul>
        )}

        <div className="cd-cd-p-not">
          <FileText aria-hidden />
          <span>
            Metin ve slaytlar{pdf?.bayt ? ` (${fmtMb(pdf.bayt)})` : ''} {pdf?.cihazda && pdf.sayi ? 'zaten cihazda' : 'seçtiğin seslerle bir kez iner'}; her ses ayrı yer tutar.
            {kb ? ` Kurul ${kb.kurul} boyunca kalır, ${tarihTr(kb.silinebilir)} sonrası silmek için sorulur.` : ''}
          </span>
        </div>
        {bos != null && <p className="cd-cd-p-yer">Cihazda boş yer: ~{fmtYer(bos)}</p>}
        {silOnay && kb && (
          <p className="cd-cd-p-uyari" role="alert">Kurul {kb.kurul} sürüyor (sınav {kb.sinav}); silersen bu dersi internetsiz dinleyemezsin.</p>
        )}
      </div>
    </Dialog>,
    document.body,
  );
}

/** İnternet yokken liste: yalnız cihazdaki dersler (diğerleri açılamaz) + bilgi şeridi */
export function useCevrimdisiSuzgec(liste: CdListeDers[]): { liste: CdListeDers[]; serit: React.ReactNode } {
  const online = useCevrimici();
  const n = useMemo(() => liste.filter((d) => cdCevrimdisiKayitlari()[d.key]).length, [liste, online]);
  if (online) return { liste, serit: null };
  const kayit = cdCevrimdisiKayitlari();
  return {
    liste: liste.filter((d) => kayit[d.key]),
    serit: (
      <div className="cd-cd-serit" role="status">
        <WifiOff aria-hidden />
        <span>
          <b>İnternet yok.</b>{' '}
          {n ? `Cihazdaki ${n} ders gösteriliyor; ses, metin ve slaytlar internetsiz çalışır.` : 'Cihaza indirilmiş ders yok. İnternet gelince bir dersi "Çevrimdışı" ile indir.'}
        </span>
      </div>
    ),
  };
}

/** Kurul bitiminden 3 gün sonra: bildirim düşülür ve silmek için sorulur (kendiliğinden silinmez). */
export default function CanliDersCevrimdisiSoru() {
  const [kurullar, setKurullar] = useState(() => cdSilinebilirKurullar());
  const [mesgul, setMesgul] = useState(false);
  const ilk = [...kurullar.entries()][0];

  useEffect(() => {
    // Bildirim merkezine bir kez (sistem bildirimi açıksa telefona da düşer)
    const soru = cdSoruDurumu();
    for (const [kurul, keys] of kurullar) {
      if (soru[kurul]?.bildirildi) continue;
      userNotificationService.addNotification({
        type: 'app_info',
        title: `Kurul ${kurul} bitti: çevrimdışı dersler silinebilir`,
        message: `Cihazında Kurul ${kurul}'e ait ${keys.length} sesli ders indirili. Yer açmak istersen silebilirsin; sen onaylamadan silinmez.`,
        deepLinkUrl: '/canliders',
        targetType: 'app',
        targetId: `cd-cevrimdisi-kurul-${kurul}`,
      });
      cdSoruYaz(kurul, { bildirildi: true });
    }
  }, [kurullar]);

  if (!ilk) return null;
  const [kurul, keys] = ilk;
  const kayit = cdCevrimdisiKayitlari();
  const bayt = keys.reduce((a, k) => a + (kayit[k]?.bayt || 0), 0);
  const kapat = () => setKurullar(cdSilinebilirKurullar());

  return (
    <div className="cd-cd-soru" role="alertdialog" aria-labelledby="cd-cd-soru-b" aria-describedby="cd-cd-soru-m">
      <div className="cd-cd-soru-kart">
        <button type="button" className="cd-cd-soru-x" onClick={() => { cdSoruYaz(kurul, { ertele: Date.now() + 86_400_000 }); kapat(); }} aria-label="Sonra sor">
          <X aria-hidden />
        </button>
        <b id="cd-cd-soru-b">Kurul {kurul} bitti</b>
        <p id="cd-cd-soru-m">
          Cihazında bu kurula ait <b>{keys.length}</b> sesli ders indirili{bayt ? ` (${fmtMb(bayt)})` : ''}. Silinsin mi? Sen onaylamadan silinmez.
        </p>
        <ul className="cd-cd-soru-liste">
          {keys.slice(0, 4).map((k) => <li key={k}>{kayit[k]?.no} · {kayit[k]?.baslik}</li>)}
          {keys.length > 4 && <li>+{keys.length - 4} ders</li>}
        </ul>
        <div className="cd-cd-soru-eylem">
          <button type="button" className="cd-btn" disabled={mesgul} onClick={() => { cdSoruYaz(kurul, { ertele: Date.now() + 14 * 86_400_000 }); kapat(); }}>
            Sakla (2 hafta sonra sor)
          </button>
          <button
            type="button"
            className="cd-btn is-ana"
            disabled={mesgul}
            onClick={async () => {
              setMesgul(true);
              try {
                await cdCevrimdisiSil(keys);
                toast.success('Çevrimdışı dersler silindi', `Kurul ${kurul}: ${keys.length} ders${bayt ? `, ${fmtMb(bayt)} yer açıldı` : ''}.`);
              } finally {
                setMesgul(false);
                kapat();
              }
            }}
          >
            Sil
          </button>
        </div>
      </div>
    </div>
  );
}
