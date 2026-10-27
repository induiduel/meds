import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Check, Copy, Crown, Gamepad2, Heart, Link2, LogOut, Timer, Users, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { auth, getRememberedStudentInfo } from '../../services/auth';
import { quizSocketClient, type PreFetchedQuestion } from '../../services/quiz/quizSocketClient';
import { icKonum } from '../../siteHaritasi';
import { useV15Baslik } from './baslik';
import OyunSoloV15, { type SoloMod } from './OyunSoloV15';
import OyunEslestirV15, { ESLESTIR_KATEGORI } from './OyunEslestirV15';
import OyunBoslukV15 from './OyunBoslukV15';
import '../../styles/v15/ogren.css';
import '../../styles/v15/oyun.css';

/**
 * v15 · Oyunlar (tasarım sistemi v15 › F/N "Oyunlar merkezi" · düello / sınıf yarışması). Yeni sayfa: /oyunlar ↔ /sorular/oyunlar.
 * Canlı yarışma: oda kur (branş + isteğe bağlı ders + soru sayısı) → kodu paylaş → herkes "Hazırım" → aynı anda aynı soru.
 * Sunucu: /api/quiz/ws (services/quiz/quizRealtimeServer, oda RAM'de; puan = doğru 1000 + hız ≤500 + seri ≤250).
 * Sorular yalnız yayındaki sesli soru çözücü setlerinden (services/quiz/oyunSoruKaynagi); tek kişi de oynanır.
 */
interface Kaynak { brans: string; ad: string; kurul: number; ders: { kod: string; baslik: string; n: number }[]; n: number }
interface Oyuncu { userId: string; displayName: string; score: number; streak: number; isReady?: boolean }
type Asama = 'giris' | 'lobi' | 'geri' | 'soru' | 'acik' | 'bitti';

const AD_KEY = 'medsoru_oyun_ad';
const KIMLIK_KEY = 'medsoru_oyun_kimlik';
const kimlik = () => {
  const u = auth.currentUser?.uid;
  if (u) return u;
  try {
    let k = localStorage.getItem(KIMLIK_KEY);
    if (!k) { k = `m${Math.random().toString(36).slice(2, 10)}`; localStorage.setItem(KIMLIK_KEY, k); }
    return k;
  } catch { return `m${Math.random().toString(36).slice(2, 10)}`; }
};
const ilkAd = () => {
  try { const s = localStorage.getItem(AD_KEY); if (s) return s; } catch { /* yok */ }
  return (auth.currentUser?.displayName || getRememberedStudentInfo().name || '').split(' ')[0] || '';
};
/** karışmayan harfler (0/O, 1/I yok) */
const kodUret = () => Array.from({ length: 5 }, () => 'ABCDEFGHJKLMNPRSTUVYZ23456789'[Math.floor(Math.random() * 29)]).join('');
const tr = (n: number) => n.toLocaleString('tr-TR');

export default function OyunlarV15() {
  const benim = useMemo(kimlik, []);
  const [ad, setAd] = useState(ilkAd);
  const [kaynaklar, setKaynaklar] = useState<Kaynak[] | null>(null);
  const [brans, setBrans] = useState('');
  const [ders, setDers] = useState('');
  const [adet, setAdet] = useState(10);
  const [kodGir, setKodGir] = useState(() => (new URLSearchParams(icKonum().search).get('oda') || '').toUpperCase());
  const [hata, setHata] = useState('');

  const [asama, setAsama] = useState<Asama>('giris');
  const [oda, setOda] = useState('');
  const [baslik, setBaslik] = useState('');
  const [kurucu, setKurucu] = useState('');
  const [oyuncular, setOyuncular] = useState<Oyuncu[]>([]);
  const [toplamSoru, setToplamSoru] = useState(0);
  const [soru, setSoru] = useState<(PreFetchedQuestion & { sira: number }) | null>(null);
  const [bitis, setBitis] = useState(0);
  const [sure, setSure] = useState(10);
  const [secim, setSecim] = useState<string | null>(null);
  const [ack, setAck] = useState<{ isCorrect: boolean; pointsAwarded: number } | null>(null);
  const [acik, setAcik] = useState<{ correctOption: string; optionExplanations: Record<string, string> } | null>(null);
  const [cevaplayan, setCevaplayan] = useState<Set<string>>(new Set());
  const [kalan, setKalan] = useState(0);
  const [bagli, setBagli] = useState(true);
  const [kopyalandi, setKopyalandi] = useState(false);
  const raf = useRef(0);
  const [solo, setSolo] = useState<SoloMod | null>(null);
  const [eslestir, setEslestir] = useState<string | null>(null);
  const [sozlukMod, setSozlukMod] = useState<'eslestir' | 'bosluk'>('eslestir');
  const [mod, setMod] = useState<'canli' | 'katil' | 'blitz' | 'hayatta' | 'eslestir' | 'bosluk'>(() => (new URLSearchParams(icKonum().search).get('oda') ? 'katil' : 'canli'));

  useV15Baslik({ baslik: 'Oyunlar', alt: oda ? `Oda ${oda}${baslik ? ` · ${baslik}` : ''}` : 'Canlı soru yarışması' });

  useEffect(() => {
    safeJsonFetch<{ kaynaklar: Kaynak[] }>('/api/oyun/kaynaklar').then((r) => {
      const k = r.ok && r.data?.kaynaklar ? r.data.kaynaklar : [];
      setKaynaklar(k);
      if (k[0]) setBrans((b) => b || k[0].brans);
    });
  }, []);

  // sunucu olayları
  useEffect(() => {
    const c = quizSocketClient;
    const ofset = () => c.timeOffsetMs || 0;
    const h: Record<string, (m: any) => void> = {
      room_joined: (m) => {
        setHata('');
        setOda(m.roomId); setBaslik(m.baslik || ''); setKurucu(m.kurucu || '');
        setOyuncular(m.players || []); setToplamSoru((m.questions || []).length);
        if (m.status === 'lobby') setAsama('lobi');
        else if (m.status === 'finished') setAsama('bitti');
        try { const u = new URL(location.href); u.searchParams.set('oda', m.roomId); history.replaceState(history.state, '', u); } catch { /* yok */ }
      },
      room_error: (m) => { setHata(m.mesaj || 'Odaya girilemedi.'); setAsama('giris'); setOda(''); },
      player_joined: (m) => setOyuncular((o) => [...o.filter((x) => x.userId !== m.player.userId), m.player]),
      player_left: (m) => setOyuncular((o) => o.filter((x) => x.userId !== m.userId)),
      player_ready_changed: (m) => setOyuncular((o) => o.map((x) => (x.userId === m.userId ? { ...x, isReady: m.isReady } : x))),
      game_countdown: (m) => { setAsama('geri'); setBitis(m.startTime - ofset()); },
      round_started: (m) => {
        if (!m.question) return;
        setSoru({ ...m.question, sira: m.questionIndex });
        setSure(m.durationSec); setBitis(m.deadlineMs - ofset());
        setSecim(null); setAck(null); setAcik(null); setCevaplayan(new Set());
        setAsama('soru');
      },
      answer_ack: (m) => setAck({ isCorrect: m.isCorrect, pointsAwarded: m.pointsAwarded }),
      player_answered: (m) => setCevaplayan((s) => new Set(s).add(m.userId)),
      round_revealed: (m) => { setAcik(m); setOyuncular((o) => mergeSkor(o, m.leaderboard)); setAsama('acik'); },
      game_finished: (m) => { setOyuncular((o) => mergeSkor(o, m.finalLeaderboard)); setAsama('bitti'); },
      baglanti: (m) => setBagli(!!m.bagli),
    };
    for (const [e, f] of Object.entries(h)) c.on(e as never, f);
    return () => { for (const [e, f] of Object.entries(h)) c.off(e as never, f); c.disconnect(); };
  }, []);

  // geri sayım / süre çubuğu
  useEffect(() => {
    if (asama !== 'soru' && asama !== 'geri') return;
    const t = () => { setKalan(Math.max(0, bitis - Date.now())); raf.current = requestAnimationFrame(t); };
    raf.current = requestAnimationFrame(t);
    return () => cancelAnimationFrame(raf.current);
  }, [asama, bitis]);

  const adKaydet = () => { try { localStorage.setItem(AD_KEY, ad.trim()); } catch { /* yok */ } };
  const kaynak = kaynaklar?.find((k) => k.brans === brans);
  const kur = () => {
    if (!kaynak) return;
    adKaydet();
    const d = kaynak.ders.find((x) => x.kod === ders);
    quizSocketClient.connect(kodUret(), benim, ad.trim() || 'Öğrenci', undefined, undefined, {
      brans, ders: ders || undefined, n: adet, baslik: d ? `${kaynak.ad} · ${d.baslik}` : `${kaynak.ad} · karışık`,
    });
  };
  const katil = () => {
    const k = kodGir.trim().toUpperCase();
    if (k.length < 4) { setHata('Oda kodu 5 harften oluşur.'); return; }
    adKaydet();
    quizSocketClient.connect(k, benim, ad.trim() || 'Öğrenci');
  };
  const cik = () => {
    quizSocketClient.disconnect();
    setAsama('giris'); setOda(''); setOyuncular([]); setSoru(null);
    try { const u = new URL(location.href); u.searchParams.delete('oda'); history.replaceState(history.state, '', u); } catch { /* yok */ }
  };
  const cevapla = (h: string) => {
    if (secim || !soru) return;
    setSecim(h);
    quizSocketClient.submitAnswer(soru.id, h);
  };
  const paylas = async () => {
    const url = `${location.origin}/sorular/oyunlar?oda=${oda}`;
    try {
      if (navigator.share) await navigator.share({ title: 'MeDSor oyunu', text: `Oda kodu: ${oda}`, url });
      else { await navigator.clipboard.writeText(url); setKopyalandi(true); setTimeout(() => setKopyalandi(false), 1800); }
    } catch { /* vazgeçti */ }
  };

  const ben = oyuncular.find((o) => o.userId === benim);
  if (eslestir !== null) return <div className="oy15">{sozlukMod === 'bosluk' ? <OyunBoslukV15 kategori={eslestir} onCik={() => setEslestir(null)} /> : <OyunEslestirV15 kategori={eslestir} onCik={() => setEslestir(null)} />}</div>;
  if (solo && kaynak) {
    const d = kaynak.ders.find((x) => x.kod === ders);
    return <div className="oy15"><OyunSoloV15 mod={solo} brans={brans} ders={ders || undefined} baslik={d ? `${kaynak.ad} · ${d.baslik}` : `${kaynak.ad} · karışık`} onCik={() => setSolo(null)} /></div>;
  }
  const sirali = [...oyuncular].sort((a, b) => b.score - a.score);

  return (
    <div className="oy15">
      <h1 className="sr-only">Oyunlar</h1>
      {!bagli && asama !== 'giris' && <p className="oy15-uyari v15-card">Bağlantı koptu, yeniden bağlanılıyor…</p>}

      {asama === 'giris' && (() => {
        // Önce mod seçilir (renkli kartlar), ayarlar altta seçilen moda göre (kullanıcı isteği 2026-10-27)
        const MODLAR: { id: typeof mod; ad: string; alt: string; ic: React.ElementType; ton: string }[] = [
          { id: 'canli', ad: 'Canlı yarışma', alt: 'Oda kur, arkadaşlarınla aynı anda', ic: Users, ton: 'a' },
          { id: 'katil', ad: 'Koda katıl', alt: 'Arkadaşının odasına gir', ic: Link2, ton: 'c' },
          { id: 'blitz', ad: 'Blitz', alt: '60 saniyede kaç doğru?', ic: Timer, ton: 'w' },
          { id: 'hayatta', ad: 'Hayatta kal', alt: '3 can, her yanlış bir can', ic: Heart, ton: 'b' },
          { id: 'eslestir', ad: 'Eşleştir', alt: 'Terim ↔ tanım, en kısa sürede', ic: Gamepad2, ton: 'ai' },
          { id: 'bosluk', ad: 'Terimi bul', alt: 'Tanımı oku, terimi yaz', ic: Crown, ton: 'ok' },
        ];
        const sozluk = mod === 'eslestir' || mod === 'bosluk';
        const basla = () => {
          if (mod === 'canli') kur();
          else if (mod === 'katil') katil();
          else if (mod === 'blitz' || mod === 'hayatta') setSolo(mod);
        };
        return (
          <>
            <section aria-label="Oyun modları">
              <ul className="oy15-modlar" role="radiogroup" aria-label="Oyun modu">
                {MODLAR.map((m) => (
                  <li key={m.id}>
                    <button type="button" role="radio" aria-checked={mod === m.id} className={`oy15-mod is-${m.ton}${mod === m.id ? ' is-on' : ''}`} onClick={() => { setMod(m.id); setHata(''); }}>
                      <span className="oy15-mod-ic"><m.ic aria-hidden /></span>
                      <b>{m.ad}</b>
                      <small>{m.alt}</small>
                    </button>
                  </li>
                ))}
              </ul>
            </section>

            <section className="v15-card oy15-ayar" aria-label="Ayarlar">
              <h2>{MODLAR.find((m) => m.id === mod)?.ad} · ayarlar</h2>
              {(mod === 'canli' || mod === 'katil') && (
                <label className="oy15-alan"><span>Adın</span>
                  <input value={ad} onChange={(e) => setAd(e.target.value.slice(0, 24))} placeholder="Oyunda görünecek ad" maxLength={24} />
                </label>
              )}
              {mod === 'katil' && (
                <label className="oy15-alan"><span>Oda kodu</span>
                  <input className="oy15-kod-in" value={kodGir} onChange={(e) => setKodGir(e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 5))}
                    placeholder="Örn. K7MPA" aria-label="Oda kodu" autoCapitalize="characters" onKeyDown={(e) => { if (e.key === 'Enter') katil(); }} />
                </label>
              )}
              {(mod === 'canli' || mod === 'blitz' || mod === 'hayatta') && (
                kaynaklar === null ? <span className="v15-skel b15-skel" aria-hidden /> : !kaynaklar.length ? (
                  <p className="v15-cap">Oyun sunucusuna ulaşılamadı ya da oyuna uygun soru yok.</p>
                ) : (
                  <div className="oy15-ayar-iki">
                    <label className="oy15-alan"><span>Ders</span>
                      <select value={brans} onChange={(e) => { setBrans(e.target.value); setDers(''); }}>
                        {kaynaklar.map((k) => <option key={k.brans} value={k.brans}>Kurul {k.kurul} · {k.ad} ({tr(k.n)} soru)</option>)}
                      </select>
                    </label>
                    {kaynak && (
                      <label className="oy15-alan"><span>Konu</span>
                        <select value={ders} onChange={(e) => setDers(e.target.value)}>
                          <option value="">Karışık (bütün konular)</option>
                          {kaynak.ders.map((d) => <option key={d.kod} value={d.kod}>{d.baslik} ({d.n})</option>)}
                        </select>
                      </label>
                    )}
                  </div>
                )
              )}
              {mod === 'canli' && (
                <div className="oy15-alan"><span>Soru sayısı</span>
                  <div className="pg15-seg" role="radiogroup" aria-label="Soru sayısı">
                    {[5, 10, 15, 20].map((n) => <button key={n} type="button" role="radio" aria-checked={adet === n} className={adet === n ? 'is-on' : ''} onClick={() => setAdet(n)}>{n}</button>)}
                  </div>
                </div>
              )}
              {sozluk ? (
                <>
                  <p className="v15-cap">{mod === 'eslestir' ? 'Sözlükten 5 terimi tanımıyla eşleştir; 3 tur, en kısa sürede.' : 'Tanımı oku, terimi yaz; 10 soru, ipucu harf açar.'} Konu seç, oyun başlasın:</p>
                  <div className="oy15-es-kat">
                    {ESLESTIR_KATEGORI.map(([k, a]) => <button key={k || 'karisik'} type="button" className="o15-cip" onClick={() => { setSozlukMod(mod === 'bosluk' ? 'bosluk' : 'eslestir'); setEslestir(k); }}>{a}</button>)}
                  </div>
                </>
              ) : (
                <button type="button" className="v15-btn oy15-ana" onClick={basla} disabled={mod !== 'katil' && !kaynak}>
                  {mod === 'canli' ? 'Oda kur' : mod === 'katil' ? 'Odaya katıl' : 'Başla'}
                </button>
              )}
              {hata && <p className="oy15-hata" role="alert">{hata}</p>}
            </section>
          </>
        );
      })()}

      {asama === 'lobi' && (
        <section className="v15-card oy15-kart oy15-lobi">
          <span className="v15-cap">Oda kodu</span>
          <b className="oy15-kod">{oda}</b>
          <span className="v15-cap">{baslik} · {toplamSoru} soru</span>
          <button type="button" className="oy15-paylas" onClick={paylas}>{kopyalandi ? <Check aria-hidden /> : <Copy aria-hidden />}{kopyalandi ? 'Bağlantı kopyalandı' : 'Davet bağlantısını paylaş'}</button>
          <ul className="oy15-oyuncular">
            {oyuncular.map((o) => (
              <li key={o.userId} className={o.isReady ? 'is-hazir' : ''}>
                {o.userId === kurucu && <Crown aria-label="Odayı kuran" />}
                <span>{o.displayName}{o.userId === benim ? ' (sen)' : ''}</span>
                <small>{o.isReady ? 'Hazır' : 'Bekliyor'}</small>
              </li>
            ))}
          </ul>
          <p className="v15-cap"><Users aria-hidden className="oy15-ic" /> Herkes "Hazırım" deyince oyun başlar.</p>
          <div className="oy15-alt">
            <button type="button" className="oy15-cik" onClick={cik}><LogOut aria-hidden />Çık</button>
            <button type="button" className="v15-btn oy15-ana" disabled={!!ben?.isReady} onClick={() => quizSocketClient.setReady()}>{ben?.isReady ? 'Diğerleri bekleniyor…' : 'Hazırım'}</button>
          </div>
        </section>
      )}

      {asama === 'geri' && (
        <section className="oy15-geri" aria-live="assertive"><b>{Math.max(1, Math.ceil(kalan / 1000))}</b><span>Hazır ol</span></section>
      )}

      {(asama === 'soru' || asama === 'acik') && soru && (
        <section className="oy15-soru">
          <div className="oy15-ust">
            <span className="v15-cap">Soru {soru.sira + 1}/{toplamSoru}</span>
            <span className="v15-cap">{tr(ben?.score || 0)} puan{ben && ben.streak > 1 ? ` · ${ben.streak} seri` : ''}</span>
          </div>
          <div className="v15-bar oy15-sure" aria-hidden><span style={{ width: asama === 'soru' ? `${(kalan / (sure * 1000)) * 100}%` : 0 }} /></div>
          <p className="oy15-kok">{soru.prompt}</p>
          <ul className="oy15-siklar">
            {Object.entries(soru.options).map(([h, t]) => {
              const dogru = acik?.correctOption === h;
              const benimki = secim === h;
              const cls = acik ? (dogru ? ' is-dogru' : benimki ? ' is-yanlis' : ' is-sonuk') : benimki ? ' is-secili' : '';
              return (
                <li key={h}>
                  <button type="button" className={`oy15-sik${cls}`} disabled={!!secim || asama !== 'soru'} onClick={() => cevapla(h)}>
                    <b>{h}</b><span>{t}</span>{acik && dogru && <Check aria-hidden />}{acik && benimki && !dogru && <X aria-hidden />}
                  </button>
                </li>
              );
            })}
          </ul>
          {asama === 'soru' && (
            <p className="v15-cap oy15-durum">{secim ? (ack ? (ack.isCorrect ? `Doğru! +${tr(ack.pointsAwarded)}` : 'Yanlış.') : 'Gönderildi…') + ' Diğerleri bekleniyor.' : `${cevaplayan.size} kişi cevapladı · ${Math.ceil(kalan / 1000)} sn`}</p>
          )}
          {asama === 'acik' && acik && (
            <div className="v15-card oy15-aciklama">
              <b>{secim ? (secim === acik.correctOption ? 'Doğru bildin.' : `Doğru cevap ${acik.correctOption}.`) : `Süre doldu. Doğru cevap ${acik.correctOption}.`}</b>
              {acik.optionExplanations?.[acik.correctOption] && <p>{acik.optionExplanations[acik.correctOption]}</p>}
              {secim && secim !== acik.correctOption && acik.optionExplanations?.[secim] && <p className="oy15-senin"><b>{secim}:</b> {acik.optionExplanations[secim]}</p>}
              <ol className="oy15-tablo">{sirali.slice(0, 5).map((o) => <li key={o.userId} className={o.userId === benim ? 'is-ben' : ''}><span>{o.displayName}</span><b>{tr(o.score)}</b></li>)}</ol>
            </div>
          )}
        </section>
      )}

      {asama === 'bitti' && (
        <section className="v15-card oy15-kart oy15-son">
          <Crown aria-hidden className="oy15-tac" />
          <b className="oy15-kazanan">{sirali[0] ? (sirali[0].userId === benim ? 'Kazandın!' : `${sirali[0].displayName} kazandı`) : 'Oyun bitti'}</b>
          <ol className="oy15-tablo">{sirali.map((o, i) => <li key={o.userId} className={o.userId === benim ? 'is-ben' : ''}><span>{i + 1}. {o.displayName}</span><b>{tr(o.score)}</b></li>)}</ol>
          <button type="button" className="v15-btn oy15-ana" onClick={cik}>Yeni oyun</button>
        </section>
      )}
    </div>
  );
}

function mergeSkor(o: Oyuncu[], lb: Oyuncu[] | undefined): Oyuncu[] {
  if (!lb) return o;
  const m = new Map(o.map((x) => [x.userId, x]));
  for (const x of lb) m.set(x.userId, { ...m.get(x.userId), ...x });
  return [...m.values()];
}
