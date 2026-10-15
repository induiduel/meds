/**
 * Canlı ders · çevrimdışı arayüzü: "Çevrimdışı kullan" düğmesi (liste satırı + ders ekranı), internet yokken liste
 * şeridi ve kurul bitiminden 3 gün sonra çıkan silme sorusu (CanliDersDockGate tembel yükler).
 */
import React, { useEffect, useMemo, useState } from 'react';
import { CheckCircle2, CloudDownload, RefreshCw, WifiOff, X } from 'lucide-react';
import { toast } from '../ui/Toast';
import { userNotificationService } from '../../services/userNotificationService';
import { fmtMb, useCd, type CdListeDers, type CdVaryant } from './canliDersStore';
import {
  cdCevrimdisiDogrula, cdCevrimdisiHataSil, cdCevrimdisiIndir, cdCevrimdisiIptal, cdCevrimdisiSil, cdKurulBilgisi, useCdCevrimdisi,
} from './canliDersCevrimdisi';
import { cdCevrimdisiKayitlari, cdSilinebilirKurullar, cdSoruDurumu, cdSoruYaz } from './canliDersCevrimdisiKayit';
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

const tarihTr = (ms: number) => new Date(ms).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' });

/** Çevrimdışı kullan / Cihazda / Güncelle düğmesi. `varyantlar`: güncel sürüm karşılaştırması için. */
export function CevrimdisiDugme({ dersKey, baslik, varyantlar, kucuk }: { dersKey: string; baslik: string; varyantlar?: CdVaryant[]; kucuk?: boolean }) {
  const { kayit, is } = useCdCevrimdisi(dersKey);
  const caliyorVid = useCd((s) => (s.key === dersKey ? s.vid : null));
  const online = useCevrimici();
  useEffect(() => {
    if (!dogrulandi) { dogrulandi = true; void cdCevrimdisiDogrula(); }
  }, []);
  const guncel = varyantlar?.find((v) => v.id === kayit?.vid);
  const eski = !!kayit && !!guncel && !!((guncel as any).surum || guncel.bayt) && ((guncel as any).surum || guncel.bayt) !== kayit.surum;

  const indir = async () => {
    try {
      await cdCevrimdisiIndir(dersKey, { caliyorVid });
      const k = cdCevrimdisiKayitlari()[dersKey];
      const kb = cdKurulBilgisi(dersKey);
      toast.success('Ders cihaza indirildi', `${baslik}: ses, metin ve slaytlar internetsiz açılır${kb ? `; Kurul ${kb.kurul} boyunca (${tarihTr(kb.silinebilir)} tarihine dek) cihazda kalır` : ''}.${k?.bayt ? ` ${fmtMb(k.bayt)}` : ''}`);
    } catch (e: any) {
      toast.error('Ders indirilemedi', e?.message || 'Bağlantını kontrol edip tekrar dene.');
    }
  };
  const sil = async () => {
    const kb = cdKurulBilgisi(dersKey);
    const kurulSuruyor = kb && Date.now() < kb.silinebilir;
    const msj = kurulSuruyor
      ? `"${baslik}" cihazdan silinsin mi?\n\nKurul ${kb!.kurul} sürüyor (sınav ${kb!.sinav}); silersen internetsiz dinleyemezsin.`
      : `"${baslik}" cihazdan silinsin mi?`;
    if (!window.confirm(msj)) return;
    await cdCevrimdisiSil([dersKey]);
    toast.info('Ders cihazdan silindi', baslik);
  };

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
          onClick={sil}
          aria-label={`Cihazda: ${baslik}${kayit.bayt ? `, ${fmtMb(kayit.bayt)}` : ''}. Silmek için dokun`}
          title={`Cihazda${kayit.bayt ? ` · ${fmtMb(kayit.bayt)}` : ''}${kb ? ` · Kurul ${kb.kurul} bitiminden 3 gün sonra (${tarihTr(kb.silinebilir)}) silmek için sorulur` : ''}. Silmek için dokun.`}
        >
          <CheckCircle2 aria-hidden />
          <span>Cihazda</span>
        </button>
        {eski && online && (
          <button type="button" className={`cd-btn is-ikon cd-cd-guncelle${kucuk ? ' is-ince' : ''}`} onClick={indir} aria-label={`Güncelle: ${baslik} (ses yenilendi)`} title="Ses yenilendi — cihazdaki kopyayı güncelle">
            <RefreshCw aria-hidden />
          </button>
        )}
      </span>
    );
  }
  return (
    <button
      type="button"
      className={`cd-btn cd-cd-dugme${is?.hata ? ' is-hata' : ''}${kucuk ? ' is-ince' : ''}`}
      onClick={() => { cdCevrimdisiHataSil(dersKey); void indir(); }}
      disabled={!online}
      aria-label={`Çevrimdışı kullan: ${baslik} (ses, metin ve slaytları cihaza indir)`}
      title={is?.hata ? `${is.hata} Tekrar dene.` : online ? 'Ses, metin ve slaytları cihaza indir — internetsiz dinle' : 'İndirmek için internet gerekir'}
    >
      <CloudDownload aria-hidden />
      <span>{is?.hata ? 'Tekrar dene' : 'Çevrimdışı'}</span>
    </button>
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
        message: `Cihazında Kurul ${kurul}'e ait ${keys.length} canlı ders indirili. Yer açmak istersen silebilirsin; sen onaylamadan silinmez.`,
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
          Cihazında bu kurula ait <b>{keys.length}</b> canlı ders indirili{bayt ? ` (${fmtMb(bayt)})` : ''}. Silinsin mi? Sen onaylamadan silinmez.
        </p>
        <ul className="cd-cd-soru-liste">
          {keys.slice(0, 4).map((k) => <li key={k}>{kayit[k]?.no}. {kayit[k]?.baslik}</li>)}
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
