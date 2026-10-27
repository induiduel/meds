/**
 * Çevrimdışı › İndirilenler: cihazdaki paketler kurul → ders olarak gruplu. Her ders: boyut, bölümler, aç, ses/PDF seç,
 * test et (ağsız denetim), onar, sil. Kurula bağlı olmayan içerik (soru bankası, başvuru verileri, uygulama) ayrı grupta.
 */
import { useMemo, useState } from 'react';
import { AlertTriangle, Check, ChevronDown, ExternalLink, HardDriveDownload, Loader2, RefreshCw, ShieldCheck, VolumeX, Wrench } from 'lucide-react';
import {
  kuyrugaEkle, paketDurumu, paketiDenetle, paketOnar, secimAl, secimDegistir, secimliBayt, useCevrimdisi, type DenetimSonuc, type Paket,
} from '../../services/cevrimdisi/paketMotoru';
import { boyutYaz, dersBirimleri, UYE_AD, type DersBirimi } from '../../services/cevrimdisi/dersBirimleri';
import { navigateTo } from '../../router';
import { EkCip, OnayliSil, uyeAdresi } from './cvOrtak';

const MODUL_AD: Record<string, string> = {
  uygulama: 'Uygulama dosyaları', db: 'Çıkmış sorular ve havuz', veri: 'Sözlük, özetler, notlar', ...UYE_AD,
};
const cihazdami = (d: string) => d === 'tamam' || d === 'guncelleme';

interface Grup { anahtar: string; ad: string; dersler: { b: DersBirimi; uyeler: Paket[] }[]; tekil: { id: string; baslik: string; modul: string; p?: Paket }[] }

export default function Indirilenler({ gotur }: { gotur: () => void }) {
  const S = useCevrimdisi();
  const [acik, setAcik] = useState<Record<string, boolean>>({});
  const [sonuclar, setSonuclar] = useState<Record<string, DenetimSonuc>>({});
  const [deniyor, setDeniyor] = useState<{ yapilan: number; toplam: number } | null>(null);
  const birimler = useMemo(() => dersBirimleri(S.katalog), [S.katalog]);

  const gruplar = useMemo<Grup[]>(() => {
    const kayitli = new Set(Object.values(S.kayitlar).filter((k) => !k.yarim).map((k) => k.id));
    const m = new Map<string, Grup>();
    const al = (anahtar: string, ad: string) => {
      if (!m.has(anahtar)) m.set(anahtar, { anahtar, ad, dersler: [], tekil: [] });
      return m.get(anahtar)!;
    };
    const kullanilan = new Set<string>();
    for (const b of birimler) {
      const uyeler = b.uyeler.filter((u) => kayitli.has(u.id));
      if (!uyeler.length) continue;
      uyeler.forEach((u) => kullanilan.add(u.id));
      al(b.kurul ? `k${b.kurul}` : 'k0', b.kurul ? `Kurul ${b.kurul}` : 'Kurula bağlı olmayan dersler').dersler.push({ b, uyeler });
    }
    for (const id of kayitli) {
      if (kullanilan.has(id)) continue;
      const k = S.kayitlar[id];
      al('zz', 'Soru bankası ve diğer').tekil.push({ id, baslik: k.baslik, modul: k.modul, p: S.katalog.find((p) => p.id === id) });
    }
    return [...m.values()].sort((a, b) => a.anahtar.localeCompare(b.anahtar));
  }, [S.kayitlar, S.katalog, birimler]);

  const bayt = (id: string) => S.kayitlar[id]?.bayt || 0;
  const tumIds = Object.values(S.kayitlar).filter((k) => !k.yarim && k.id !== 'uygulama').map((k) => k.id);
  const sorunlu = Object.values(sonuclar).filter((x) => !x.ok && S.kayitlar[x.id]);
  const saglam = Object.values(sonuclar).filter((x) => x.ok).length;

  async function sina(ids: string[]) {
    const hedef = ids.filter((id) => cihazdami(paketDurumu(id, S)));
    if (!hedef.length) return;
    setDeniyor({ yapilan: 0, toplam: hedef.length });
    const yeni = { ...sonuclar };
    for (let i = 0; i < hedef.length; i++) {
      yeni[hedef[i]] = await paketiDenetle(hedef[i]);
      setSonuclar({ ...yeni });
      setDeniyor({ yapilan: i + 1, toplam: hedef.length });
    }
    setDeniyor(null);
  }

  if (!gruplar.length) {
    return (
      <div className="cv15-bos v15-card">
        <span className="v15-tile is-n"><HardDriveDownload aria-hidden /></span>
        <b>Henüz indirilen yok</b>
        <span className="v15-cap">İndirdiğin dersler burada kurul kurul listelenir; internet olmadan da açılır.</span>
        <button type="button" className="v15-btn is-soft" onClick={gotur}>İndirilebilirlere git</button>
      </div>
    );
  }

  return (
    <div className="cv15-yigin">
      <div className="cv15-arac">
        <button type="button" className="cv15-b" disabled={!tumIds.length || !!deniyor} onClick={() => void sina(tumIds)}>
          {deniyor ? <Loader2 className="cv15-don" aria-hidden /> : <ShieldCheck aria-hidden />}
          <span>{deniyor ? `Sınanıyor ${deniyor.yapilan}/${deniyor.toplam}` : 'Hepsini test et'}</span>
        </button>
        {(saglam > 0 || sorunlu.length > 0) && (
          <span className={`cv15-sonuc${sorunlu.length ? ' is-b' : ' is-ok'}`} role="status">
            {sorunlu.length ? <AlertTriangle aria-hidden /> : <Check aria-hidden />}
            {sorunlu.length ? `${sorunlu.length} pakette sorun, ${saglam} sağlam` : `${saglam} paket sağlam, internetsiz açılır`}
          </span>
        )}
        {sorunlu.length > 0 && <button type="button" className="cv15-b is-a" onClick={() => void paketOnar(sorunlu.map((x) => x.id))}><Wrench aria-hidden /> <span>Hepsini onar</span></button>}
      </div>

      {gruplar.map((g) => {
        const ids = [...g.dersler.flatMap((d) => d.uyeler.map((u) => u.id)), ...g.tekil.map((t) => t.id)];
        const gb = ids.reduce((a, id) => a + bayt(id), 0);
        const sesli = g.dersler.flatMap((d) => d.uyeler).filter((u) => u.ek?.ses && secimAl(u.id, S).ses);
        const sesB = sesli.reduce((a, u) => a + (u.ek?.ses?.b || 0), 0);
        return (
          <section key={g.anahtar} className="cv15-grup v15-card" aria-label={g.ad}>
            <header className="cv15-grup-bas">
              <span className="cv15-grup-ad"><b>{g.ad}</b><span className="v15-cap">{g.dersler.length ? `${g.dersler.length} ders` : `${g.tekil.length} paket`} · {boyutYaz(gb)}</span></span>
              {sesli.length > 1 && (
                <button type="button" className="cv15-b" title="İndirilmiş derslerin seslerini sil; dersler sessiz çalışır" onClick={() => void secimDegistir(sesli.map((u) => u.id), { ses: false })}>
                  <VolumeX aria-hidden /> <span>Sesleri kaldır · {boyutYaz(sesB)}</span>
                </button>
              )}
              <OnayliSil ids={ids.filter((id) => id !== 'uygulama')} etiket="Grubu sil" />
            </header>
            <ul className="cv15-satirlar">
              {g.dersler.map(({ b, uyeler }) => {
                const ac = !!acik[b.id];
                const db = uyeler.reduce((a, u) => a + bayt(u.id), 0);
                const gun = uyeler.filter((u) => paketDurumu(u.id, S) === 'guncelleme');
                const bozuk = uyeler.map((u) => sonuclar[u.id]).filter((r) => r && !r.ok);
                return (
                  <li key={b.id} className="cv15-satir">
                    <div className="cv15-satir-ust">
                      <button type="button" className="cv15-satir-ad" aria-expanded={ac} onClick={() => setAcik({ ...acik, [b.id]: !ac })}>
                        <ChevronDown aria-hidden className={ac ? 'is-ac' : ''} />
                        <span>
                          <b>{b.baslik}</b>
                          <span className="v15-cap">{b.grup} · {uyeler.length}/{b.uyeler.length} bölüm · {boyutYaz(db)}</span>
                        </span>
                      </button>
                      {gun.length > 0 && <span className="v15-tag is-w">Güncelleme</span>}
                      {bozuk.length > 0 && <span className="v15-tag is-b">Sorunlu</span>}
                      <OnayliSil ids={uyeler.map((u) => u.id)} ikon ad={b.baslik} soru="Ders silinsin mi?" />
                    </div>
                    {ac && (
                      <div className="cv15-detay">
                        <div className="cv15-arac">
                          <button type="button" className="cv15-b" disabled={!!deniyor} onClick={() => void sina(uyeler.map((u) => u.id))}><ShieldCheck aria-hidden /> <span>Test et</span></button>
                          {gun.length > 0 && <button type="button" className="cv15-b is-a" onClick={() => kuyrugaEkle(gun.map((u) => u.id), true)}><RefreshCw aria-hidden /> <span>Güncelle</span></button>}
                          {bozuk.length > 0 && <button type="button" className="cv15-b is-a" onClick={() => void paketOnar(bozuk.map((r) => r.id))}><Wrench aria-hidden /> <span>Onar</span></button>}
                        </div>
                        <ul className="cv15-uyeler">
                          {b.uyeler.map((u) => {
                            const ud = paketDurumu(u.id, S);
                            const var_ = cihazdami(ud);
                            const r = sonuclar[u.id];
                            const adres = uyeAdresi(u);
                            const secim = secimAl(u.id, S);
                            return (
                              <li key={u.id}>
                                <span className="cv15-uye-t">
                                  <b>{UYE_AD[u.modul] || u.modul}</b>
                                  <span className="v15-cap">{var_ ? boyutYaz(bayt(u.id)) : `İndirilmedi · ${boyutYaz(secimliBayt(u, secim))}`}{ud === 'hata' ? ` · ${S.hatalar[u.id] || 'hata'}` : ''}</span>
                                  {r && <span className={`v15-cap ${r.ok ? 'cv15-ok' : 'cv15-kotu'}`}>{r.ok ? 'Sağlam' : r.ayrinti}</span>}
                                </span>
                                <span className="cv15-uye-e">
                                  <EkCip p={u} tur="ses" secim={secim} />
                                  <EkCip p={u} tur="pdf" secim={secim} />
                                  {var_ && u.modul === 'medspak' && (
                                    <button type="button" className="cv15-b" onClick={() => window.dispatchEvent(new CustomEvent('cv-medspak-ac', { detail: u.id.slice('medspak:'.length) }))}><ExternalLink aria-hidden /> <span>Paketi aç</span></button>
                                  )}
                                  {var_ && adres && <button type="button" className="cv15-b" onClick={() => navigateTo(adres)}><ExternalLink aria-hidden /> <span>Aç</span></button>}
                                  {!var_ && (ud === 'yok' || ud === 'hata') && <button type="button" className="cv15-b is-a" onClick={() => kuyrugaEkle([u.id])}><span>İndir</span></button>}
                                  {var_ && <OnayliSil ids={[u.id]} ikon ad={UYE_AD[u.modul]} />}
                                </span>
                              </li>
                            );
                          })}
                        </ul>
                      </div>
                    )}
                  </li>
                );
              })}
              {g.tekil.map((t) => {
                const d = paketDurumu(t.id, S);
                return (
                  <li key={t.id} className="cv15-satir">
                    <div className="cv15-satir-ust">
                      <span className="cv15-satir-ad is-duz">
                        <span><b>{t.baslik}</b><span className="v15-cap">{MODUL_AD[t.modul] || t.modul} · {boyutYaz(bayt(t.id))}</span></span>
                      </span>
                      {d === 'guncelleme' && <button type="button" className="cv15-b is-a" onClick={() => kuyrugaEkle([t.id], true)}><RefreshCw aria-hidden /> <span>Güncelle</span></button>}
                      {!t.p?.zorunlu && <OnayliSil ids={[t.id]} ikon ad={t.baslik} />}
                    </div>
                  </li>
                );
              })}
            </ul>
          </section>
        );
      })}
    </div>
  );
}
