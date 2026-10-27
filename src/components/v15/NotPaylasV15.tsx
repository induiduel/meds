import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { Copy, Inbox, Link2, MessagesSquare, Search, Send, Undo2, Users, User } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { auth, getRememberedStudentInfo } from '../../services/auth';
import { useLiveEvent } from '../../hooks/useLiveEvent';
import { linkClick, navigateTo } from '../../router';
import { Sheet } from '../ui/Sheet';
import { geriAlinabilir } from '../ui/Toast';

/**
 * v15 · K05 Notu paylaş (alt sayfa) + K06 Benimle paylaşılanlar (Notlarım › ?gorunum=paylasilan).
 * Hedef bir topluluk sohbet odasıdır (grup = topluluk, birebir = kişi); sunucu services/notPaylas.ts.
 * Kişiyle birebir sohbet Topluluk'ta bir mesajın yazarından açılır; burada yalnız mevcut sohbetler listelenir.
 */
export interface PaylasNot { baslik: string; metin: string; renk: string }
interface SohbetOzet { id: number; tur: 'dm' | 'grup'; ad: string; uyeN: number }
export interface PaylasilanNot { id: number; odaId: number; odaTur: 'dm' | 'grup'; odaAd: string; sahipAd: string; benim: boolean; baslik: string; metin: string; renk: string; at: number; uzunluk: number }

const AD_KEY = 'medsoru_topluluk_ad';
const benimAd = () => { try { const a = localStorage.getItem(AD_KEY); if (a) return a; } catch { /* yok */ } return (auth.currentUser?.displayName || getRememberedStudentInfo().name || 'Öğrenci').split(' ')[0]; };
const post = <T,>(url: string, body?: any) => safeJsonFetch<T>(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) });
const fold = (s: string) => s.toLocaleLowerCase('tr-TR');
const bas = (s: string) => s.split(/\s+/).filter(Boolean).slice(0, 2).map((x) => x[0]).join('').toLocaleUpperCase('tr-TR') || '?';
const zaman = (t: number) => {
  const d = (Date.now() - t) / 60000;
  if (d < 1) return 'şimdi'; if (d < 60) return `${Math.round(d)} dk`; if (d < 1440) return `${Math.round(d / 60)} sa`;
  return new Date(t).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
};

export function NotPaylasSayfasi({ not, acik, kapat }: { not: PaylasNot; acik: boolean; kapat: () => void }) {
  const [sohbetler, setSohbetler] = useState<SohbetOzet[] | null>(null);
  const [girisli, setGirisli] = useState(true);
  const [ara, setAra] = useState('');
  const [secili, setSecili] = useState<number | null>(null);
  const [durum, setDurum] = useState<{ t: 'bos' | 'gonder' | 'tamam' | 'hata'; m?: string }>({ t: 'bos' });
  useEffect(() => {
    if (!acik) return;
    setDurum({ t: 'bos' }); setSecili(null);
    void safeJsonFetch<{ sohbetler: SohbetOzet[]; girisli: boolean }>('/api/topluluk/sohbetler').then((r) => {
      setGirisli(r.data?.girisli !== false); setSohbetler(r.ok ? r.data?.sohbetler || [] : []);
    });
  }, [acik]);
  const liste = useMemo(() => (sohbetler || []).filter((s) => !ara || fold(s.ad).includes(fold(ara))), [sohbetler, ara]);
  const gonder = async () => {
    if (secili == null) return;
    setDurum({ t: 'gonder' });
    const r = await post<{ id: number }>('/api/not-paylas', { odaId: secili, baslik: not.baslik, metin: not.metin, renk: not.renk, benAd: benimAd() });
    if (r.ok) setDurum({ t: 'tamam', m: `${sohbetler?.find((s) => s.id === secili)?.ad || 'Sohbet'} ile paylaşıldı.` });
    else setDurum({ t: 'hata', m: r.error || 'Paylaşılamadı.' });
  };
  const sistem = async () => {
    const metin = `${not.baslik || 'Not'}\n\n${not.metin}`.trim();
    try {
      if (navigator.share) await navigator.share({ title: not.baslik || 'Not', text: metin });
      else { await navigator.clipboard.writeText(metin); setDurum({ t: 'tamam', m: 'Not panoya kopyalandı.' }); }
    } catch { /* vazgeçti */ }
  };
  const bos = !not.baslik.trim() && !not.metin.trim();

  return (
    <Sheet open={acik} onClose={kapat} title="Notu paylaş" subtitle={not.baslik || 'Başlıksız not'} width={460}
      footer={<button type="button" className="v15-btn np15-gonder" onClick={gonder} disabled={secili == null || bos || durum.t === 'gonder' || durum.t === 'tamam'}><Send aria-hidden />{durum.t === 'gonder' ? 'Gönderiliyor…' : 'Gönder'}</button>}>
      <div className="np15">
        {bos && <p className="np15-uyari">Boş not paylaşılamaz; önce bir şey yaz.</p>}
        {!girisli ? (
          <p className="np15-bos">Notu bir gruba ya da kişiye göndermek için giriş yapmalısın.</p>
        ) : sohbetler == null ? (
          <p className="np15-bos">Sohbetler yükleniyor…</p>
        ) : !sohbetler.length ? (
          <div className="np15-bos">
            <p>Henüz bir sohbetin yok. Topluluk'ta grup kur ya da bir mesajın yazarıyla birebir sohbet aç; sonra notunu oraya gönderebilirsin.</p>
            <a className="v15-btn is-soft" href="/topluluk?gorunum=sohbetler" onClick={linkClick(() => { kapat(); navigateTo('/topluluk?gorunum=sohbetler'); })}><MessagesSquare aria-hidden />Sohbetlere git</a>
          </div>
        ) : (
          <>
            <label className="o15-ara"><Search aria-hidden /><input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Kişi ya da grup ara" aria-label="Kişi ya da grup ara" /></label>
            <ul className="np15-liste" role="radiogroup" aria-label="Paylaşılacak sohbet">
              {liste.map((s) => (
                <li key={s.id}>
                  <button type="button" role="radio" aria-checked={secili === s.id} className="np15-li" onClick={() => setSecili(s.id)}>
                    <span className={`np15-av is-${s.tur}`} aria-hidden>{bas(s.ad)}</span>
                    <span className="np15-ad"><b>{s.ad}</b><small>{s.tur === 'grup' ? `${s.uyeN} kişi · grup` : 'Birebir'}</small></span>
                    {s.tur === 'grup' ? <Users aria-hidden /> : <User aria-hidden />}
                  </button>
                </li>
              ))}
              {!liste.length && <li className="np15-bos">"{ara}" ile eşleşen sohbet yok.</li>}
            </ul>
            <p className="v15-cap">Paylaşınca notun o anki kopyası gider; sohbetteki herkes görebilir, sen istediğinde geri alırsın.</p>
          </>
        )}
        <button type="button" className="np15-sistem" onClick={sistem} disabled={bos}>
          {typeof navigator !== 'undefined' && 'share' in navigator ? <Link2 aria-hidden /> : <Copy aria-hidden />}
          <span>{typeof navigator !== 'undefined' && 'share' in navigator ? 'Başka uygulamayla paylaş' : 'Metni kopyala'}</span>
        </button>
        {durum.m && <p className={`np15-durum is-${durum.t}`} role="status">{durum.m}</p>}
      </div>
    </Sheet>
  );
}

/** K06 · Benimle paylaşılanlar / Paylaştıklarım. kaydet: notu kendi notlarına kopyalar, geri alma işlevi döner (NotlarimV15 verir). */
export function Paylasilanlar({ kaydet }: { kaydet: (n: PaylasNot) => () => void }) {
  const [sekme, setSekme] = useState<'benimle' | 'benim'>('benimle');
  const [veri, setVeri] = useState<{ notlar: PaylasilanNot[]; girisli: boolean } | null>(null);
  const [acik, setAcik] = useState<PaylasilanNot | null>(null);
  const [ara, setAra] = useState('');
  const yukle = useCallback(() => safeJsonFetch<{ notlar: PaylasilanNot[]; girisli: boolean }>(`/api/not-paylas/${sekme}`)
    .then((r) => setVeri(r.ok && r.data ? r.data : { notlar: [], girisli: true })), [sekme]);
  useEffect(() => { setVeri(null); void yukle(); }, [yukle]);
  useLiveEvent('not_paylas', () => void yukle(), { debounceMs: 600 });
  const ac = async (n: PaylasilanNot) => {
    const r = await safeJsonFetch<{ not: PaylasilanNot }>(`/api/not-paylas/${n.id}`);
    setAcik(r.ok && r.data ? r.data.not : n);
  };
  const kaldir = async (n: PaylasilanNot) => {
    const r = await post(`/api/not-paylas/${n.id}/kaldir`);
    if (r.ok) { setAcik(null); void yukle(); }
  };
  const liste = (veri?.notlar || []).filter((n) => !ara || fold(`${n.baslik} ${n.metin} ${n.sahipAd} ${n.odaAd}`).includes(fold(ara)));

  return (
    <div className="np15-sayfa">
      <div className="v15-seg" role="tablist" aria-label="Paylaşılan notlar">
        <button type="button" role="tab" aria-selected={sekme === 'benimle'} onClick={() => setSekme('benimle')}>Benimle paylaşılanlar</button>
        <button type="button" role="tab" aria-selected={sekme === 'benim'} onClick={() => setSekme('benim')}>Paylaştıklarım</button>
      </div>
      <label className="o15-ara"><Search aria-hidden /><input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Paylaşılan notlarda ara" aria-label="Paylaşılan notlarda ara" /></label>
      {veri == null ? <p className="b15-bos v15-card">Yükleniyor…</p>
        : !veri.girisli ? <p className="b15-bos v15-card">Paylaşılan notları görmek için giriş yapmalısın.</p>
        : !liste.length ? (
          <div className="v15-card nt15-bos">
            <Inbox aria-hidden />
            <b>{ara ? `"${ara}" geçen paylaşım yok` : sekme === 'benimle' ? 'Seninle paylaşılan not yok' : 'Henüz not paylaşmadın'}</b>
            <p>{sekme === 'benimle' ? 'Üyesi olduğun gruplarda ya da birebir sohbetlerde biri not paylaşınca burada görünür.' : 'Bir notu açıp Paylaş düğmesiyle bir gruba ya da kişiye gönderebilirsin.'}</p>
          </div>
        ) : (
          <ul className="np15-izgara">
            {liste.map((n) => (
              <li key={n.id}>
                <button type="button" className={`v15-card np15-kart is-${n.renk}`} onClick={() => void ac(n)}>
                  <span className="np15-kart-ust"><span className={`np15-av is-${n.odaTur} is-k`} aria-hidden>{bas(n.sahipAd)}</span><span className="np15-kim">{n.sahipAd} · {n.odaTur === 'grup' ? n.odaAd : 'Birebir'}</span><small>{zaman(n.at)}</small></span>
                  <b>{n.baslik || 'Başlıksız not'}</b>
                  <span className="np15-ozet">{n.metin || 'Boş not'}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      <Sheet open={!!acik} onClose={() => setAcik(null)} title={acik?.baslik || 'Başlıksız not'} subtitle={acik ? `${acik.sahipAd} · ${acik.odaTur === 'grup' ? acik.odaAd : 'Birebir'} · ${zaman(acik.at)}` : undefined} width={560}
        footer={acik && (acik.benim
          ? <button type="button" className="v15-btn is-soft" onClick={() => void kaldir(acik)}><Undo2 aria-hidden />Paylaşımı geri al</button>
          : <button type="button" className="v15-btn" onClick={() => { const geri = kaydet({ baslik: acik.baslik, metin: acik.metin, renk: acik.renk }); setAcik(null); geriAlinabilir('Notlarına kopyalandı', geri); }}><Copy aria-hidden />Notlarıma kopyala</button>)}>
        <div className="np15-oku">{acik?.metin || 'Boş not'}</div>
      </Sheet>
    </div>
  );
}
