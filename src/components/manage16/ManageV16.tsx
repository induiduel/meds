/**
 * Yönetim v16 kabuğu (2026-10-28). Plan: docs/YONETIM_V16_PLAN.md, kullanım: docs/YONETIM_V16_KIT.md.
 * - Menü/rota tek kaynak: ./menu.ts. Her sayfa React.lazy ile ayrı yığın; /manage açılışı yalnız kabuk + Genel bakış.
 * - Adres: /manage/<grup>/<sayfa>[/<id>]; eski v14 adresleri replaceState ile yeni adrese yönlenir.
 * - Canlı/Yerel hedef seçici ManageConsole davranışının aynısı (localhost'ta varsayılan Oracle vekili, seçim yenileme ister).
 * - v14 kabuğu geçiş süresince ?kabuk=v14 ile açılır (App.tsx; oturum boyunca hatırlanır, ?kabuk=v16 döndürür).
 */
import React, { Suspense, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, ChevronDown, ChevronRight, Menu, Moon, Search, Sun, Construction, ExternalLink, Pin, PinOff, X } from 'lucide-react';
import { MENU, TUM_SAYFALAR, adresCoz, manageAdres, yolGuncelle, type SayfaProps, type SayfaTanim } from './menu';
import { BildirimHost, BosDurum, Hata, OnayHost, SayfaBasligi, Yukleniyor } from './kit';
import { useTheme } from '../../utils/theme';
import { PANEL_ON_ORACLE_AT_BOOT, PANEL_TARGET_KEY, canSwitchPanelTarget, getPanelTarget, isLocalHost } from '../../config/deployment';
import { realtimeEventService, type RealtimeConnectionStatus } from '../../services/realtimeEvents';

const fold = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');

const lazyOnbellek = new Map<string, React.LazyExoticComponent<React.ComponentType<SayfaProps>>>();
/** H423: m16_sabit / m16_son okuması — birleştirilen eski yollar yeni yola çevrilir, tekrarlar süzülür, değişmişse geri yazılır */
function yolListesiOku(anahtar: string): string[] {
  try {
    const ham: unknown = JSON.parse(localStorage.getItem(anahtar) || '[]');
    if (!Array.isArray(ham)) return [];
    const n = [...new Set(ham.filter((y): y is string => typeof y === 'string').map(yolGuncelle))];
    if (JSON.stringify(n) !== JSON.stringify(ham)) localStorage.setItem(anahtar, JSON.stringify(n));
    return n;
  } catch { return []; }
}

function lazySayfa(s: SayfaTanim) {
  if (!s.yukle) return null;
  let c = lazyOnbellek.get(s.yol);
  if (!c) { c = React.lazy(s.yukle); lazyOnbellek.set(s.yol, c); }
  return c;
}

class SayfaSiniri extends React.Component<{ children: React.ReactNode; anahtar: string }, { hata: unknown }> {
  state = { hata: null as unknown };
  static getDerivedStateFromError(hata: unknown) { return { hata }; }
  componentDidUpdate(p: { anahtar: string }) { if (p.anahtar !== this.props.anahtar && this.state.hata) this.setState({ hata: null }); }
  render() { return this.state.hata ? <Hata hata={this.state.hata} yenile={() => this.setState({ hata: null })} /> : this.props.children; }
}

const Yakinda: React.FC<{ s: SayfaTanim }> = ({ s }) => (
  <>
    <SayfaBasligi baslik={s.etiket} aciklama={s.aciklama} />
    <div className="m16-kart">
      <BosDurum
        ikon={<Construction aria-hidden="true" />}
        baslik="Bu sayfa yakında"
        aciklama={`v16'da henüz kurulmadı (öncelik ${s.oncelik}).${s.v14Slug ? ' Şimdilik eski panelden kullanabilirsiniz.' : ''}`}
        eylem={s.v14Slug ? <a className="m16-btn" href={`/manage/${s.v14Slug}?kabuk=v14`}><ExternalLink aria-hidden="true" />Eski panelde aç</a> : undefined}
      />
    </div>
  </>
);

type PaletOge = { id: string; etiket: string; alt?: string; ikon?: React.ReactNode; git: () => void };

const Palet: React.FC<{ kapat: () => void; git: (yol: string) => void }> = ({ kapat, git }) => {
  const [q, setQ] = useState('');
  const [i, setI] = useState(0);
  const ogeler = useMemo<PaletOge[]>(() => {
    const f = fold(q.trim());
    const sayfalar = TUM_SAYFALAR.filter((s) => !f || fold(`${s.etiket} ${s.grup.etiket} ${s.yol} ${s.anahtar || ''}`).includes(f)).map((s) => ({
      id: `s:${s.yol}`, etiket: s.etiket, alt: s.grup.etiket, ikon: <s.ikon aria-hidden="true" />, git: () => git(s.yol),
    }));
    // Global kayıt araması: hedef sayfaya ?q= ile gider (sayfa VeriTablosu adres durumunu okur)
    const kayit: PaletOge[] = q.trim().length >= 2 ? [
      ['kisi', 'Kişilerde ara'], ['sorular/cikmis', 'Çıkmış sorularda ara'], ['sorular/havuz', 'Havuzda ara'], ['topluluk/mesaj', 'Mesajlarda ara'], ['sistem/denetim', 'Denetim kaydında ara'],
    ].map(([yol, et]) => ({ id: `k:${yol}`, etiket: `${et}: “${q.trim()}”`, alt: 'Kayıt araması', ikon: <Search aria-hidden="true" />, git: () => git(`${yol}?q=${encodeURIComponent(q.trim())}`) })) : [];
    return [...sayfalar.slice(0, 40), ...kayit];
  }, [q, git]);
  useEffect(() => setI(0), [q]);
  // Kapanınca odak paleti açan ögeye döner (gezinme olduysa içerik zaten odak alır)
  useEffect(() => { const once = document.activeElement as HTMLElement | null; return () => { if (once?.isConnected && document.activeElement === document.body) once.focus(); }; }, []);
  const sec = (o?: PaletOge) => { if (!o) return; o.git(); kapat(); };
  return (
    <div className="m16-perde" onMouseDown={(e) => { if (e.target === e.currentTarget) kapat(); }}>
      <div className="m16-palet" role="dialog" aria-modal="true" aria-label="Sayfaya git ve ara">
        <input autoFocus value={q} onChange={(e) => setQ(e.target.value)} placeholder="Sayfa adı ya da aranacak kayıt…" aria-label="Ara"
          role="combobox" aria-expanded="true" aria-controls="m16-palet-l" aria-activedescendant={ogeler[i] ? `m16p-${i}` : undefined}
          onKeyDown={(e) => {
            if (e.key === 'Escape') kapat();
            else if (e.key === 'ArrowDown') { e.preventDefault(); setI((x) => Math.min(ogeler.length - 1, x + 1)); }
            else if (e.key === 'ArrowUp') { e.preventDefault(); setI((x) => Math.max(0, x - 1)); }
            else if (e.key === 'Enter') { e.preventDefault(); sec(ogeler[i]); }
          }} />
        <ul id="m16-palet-l" role="listbox">
          {ogeler.length === 0 && <li className="m16-palet-baslik">Sonuç yok</li>}
          {ogeler.map((o, k) => (
            <li key={o.id}>
              <button type="button" id={`m16p-${k}`} role="option" aria-selected={k === i} onMouseEnter={() => setI(k)} onClick={() => sec(o)}>
                {o.ikon}<span>{o.etiket}</span>{o.alt && <small>{o.alt}</small>}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export const ManageV16: React.FC<{ adminEmail: string; onExit: () => void }> = ({ adminEmail, onExit }) => {
  const [konum, setKonum] = useState(() => window.location.pathname);
  const [gezinti, setGezinti] = useState(0);
  const [menuAcik, setMenuAcik] = useState(false);
  const [paletAcik, setPaletAcik] = useState(false);
  // H312: kayıt yoksa (null) varsayılan = yalnız Genel + aktif sayfanın grubu açık; dokunulunca kayıt başlar.
  const [kapaliKayit, setKapaliKayit] = useState<Set<string> | null>(() => {
    try { const v = localStorage.getItem('m16_kapali_grup'); return v === null ? null : new Set(JSON.parse(v)); } catch { return null; }
  });
  // H310: sabitlenen sayfalar (yol listesi), H311: son açılan sayfalar.
  const [sabit, setSabit] = useState<string[]>(() => yolListesiOku('m16_sabit'));
  const [son, setSon] = useState<string[]>(() => yolListesiOku('m16_son'));
  // H313: menü içi süzgeç
  const [menuAra, setMenuAra] = useState('');
  const [canli, setCanli] = useState<RealtimeConnectionStatus>(() => realtimeEventService.getStatus());
  const { theme, toggle } = useTheme();
  const icerikRef = useRef<HTMLElement>(null);

  const cozum = useMemo(() => adresCoz(konum), [konum]);

  const git = useCallback((yol: string, o?: { degistir?: boolean }) => {
    const [p, qs] = yol.split('?');
    const url = `${manageAdres(p)}${qs ? `?${qs}` : ''}`;
    const onceYol = window.location.pathname;
    const onceSayfa = adresCoz(onceYol).sayfa.yol;
    if (o?.degistir) window.history.replaceState(window.history.state, '', url); else window.history.pushState(window.history.state, '', url);
    setKonum(window.location.pathname);
    setMenuAcik(false);
    // Aynı sayfa içinde alt yol değişimi (satır çekmecesi aç/kapa, sekme): sayfa yeniden kurulmaz, odak/kaydırma
    // korunur. Eskiden her git() sayfayı yeniden bağlayıp listeyi baştan çekiyor, çekmece kapanınca odak satıra
    // dönmeyip <main>'e gidiyordu (H131c). Farklı sayfa ya da aynı menü ögesine yeniden tıklama: sıfırla.
    const ayniSayfa = adresCoz(window.location.pathname).sayfa.yol === onceSayfa;
    if (!ayniSayfa || window.location.pathname === onceYol) {
      setGezinti((n) => n + 1);
      icerikRef.current?.focus({ preventScroll: true });
      window.scrollTo({ top: 0 });
    }
  }, []);

  // Eski adres yönlendirmesi
  useEffect(() => {
    // H423: yönlendirme hedefi sorgu taşıyabilir (?sekme=kuyruk); mevcut sorguyla birleştir (hedefinki önce gelir)
    if (cozum.yonlendir === undefined) return;
    const [p, hq = ''] = cozum.yonlendir.split('?');
    const q = new URLSearchParams(hq);
    new URLSearchParams(window.location.search).forEach((v, k) => { if (k !== 'kabuk' && !q.has(k)) q.set(k, v); });
    const qs = q.toString();
    git(`${p}${qs ? `?${qs}` : ''}`, { degistir: true });
  }, [cozum.yonlendir, git]);

  useEffect(() => {
    const f = () => setKonum(window.location.pathname);
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  useEffect(() => realtimeEventService.onStatusChange(setCanli), []);

  // ⌘K / Ctrl+K
  useEffect(() => {
    const f = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); setPaletAcik((v) => !v); }
    };
    document.addEventListener('keydown', f);
    return () => document.removeEventListener('keydown', f);
  }, []);

  // Yerel panel → Oracle (ManageConsole ile aynı kural): hedef açılıştakinden farklıysa bir kez yenile
  const yerelMakine = isLocalHost();
  const degistirebilir = canSwitchPanelTarget();
  const hedef = getPanelTarget();
  useEffect(() => {
    if (!yerelMakine) return;
    if ((hedef === 'oracle') !== PANEL_ON_ORACLE_AT_BOOT) window.location.reload();
    return () => {
      if (PANEL_ON_ORACLE_AT_BOOT) setTimeout(() => { if (!/^\/manage(\/|$)/.test(window.location.pathname)) window.location.reload(); }, 0);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  const hedefSec = (t: 'oracle' | 'yerel') => {
    try { localStorage.setItem(PANEL_TARGET_KEY, t); } catch { /* */ }
    window.location.reload();
  };
  const kaynakCanli = yerelMakine ? PANEL_ON_ORACLE_AT_BOOT : hedef === 'oracle';

  useEffect(() => {
    document.documentElement.classList.add('m16-on');
    return () => document.documentElement.classList.remove('m16-on');
  }, []);

  const s = cozum.sayfa;
  const bulunamadi = s.yol === '' && cozum.altYol.length > 0;
  const Sayfa = bulunamadi ? null : lazySayfa(s);
  // H311: son kullanılanlar (en çok 5, aktif sayfa başa)
  useEffect(() => {
    if (bulunamadi) return;
    setSon((x) => {
      const n = [s.yol, ...x.filter((y) => y !== s.yol)].slice(0, 8);
      try { localStorage.setItem('m16_son', JSON.stringify(n)); } catch { /* */ }
      return n;
    });
  }, [s.yol, bulunamadi]);
  const sabitDegistir = (yol: string) => setSabit((x) => {
    const n = x.includes(yol) ? x.filter((y) => y !== yol) : [...x, yol];
    try { localStorage.setItem('m16_sabit', JSON.stringify(n)); } catch { /* */ }
    return n;
  });
  const yoldan = (y: string) => TUM_SAYFALAR.find((x) => x.yol === y);
  const sabitSayfalar = sabit.map(yoldan).filter(Boolean) as typeof TUM_SAYFALAR;
  // Son: aktif sayfanın kendisi hariç değil — sabitlenmişler hariç, ilk 5
  const sonSayfalar = (son.map(yoldan).filter((x) => x && !sabit.includes(x.yol)) as typeof TUM_SAYFALAR).slice(0, 5);
  const araF = fold(menuAra.trim());
  const eslesir = (x: SayfaTanim) => !araF || fold(`${x.etiket} ${x.anahtar || ''}`).includes(araF);
  // H310: menü ögesi + raptiye düğmesi (üzerine gelince/odakta görünür; sabitliyse hep görünür)
  const oge = (x: SayfaTanim) => {
    const sabitMi = sabit.includes(x.yol);
    return (
      <div key={x.yol} className={`m16-menu-oge ${sabitMi ? 'sabit' : ''}`}>
        <a href={manageAdres(x.yol)} aria-current={x.yol === s.yol && !bulunamadi ? 'page' : undefined} className={x.yukle ? '' : 'bos'}
          onClick={(e) => { if (e.metaKey || e.ctrlKey || e.shiftKey) return; e.preventDefault(); setMenuAra(''); git(x.yol); }}>
          <x.ikon aria-hidden="true" />{x.etiket}{!x.yukle && <span className="m16-yakinda">yakında</span>}
        </a>
        <button type="button" className="m16-raptiye" aria-pressed={sabitMi} aria-label={sabitMi ? `${x.etiket}: sabitlemeyi kaldır` : `${x.etiket}: sabitle`}
          title={sabitMi ? 'Sabitlemeyi kaldır' : 'Sabitle'} onClick={() => sabitDegistir(x.yol)}>
          {sabitMi ? <PinOff aria-hidden="true" /> : <Pin aria-hidden="true" />}
        </button>
      </div>
    );
  };
  useEffect(() => { document.title = `${degistirebilir ? (kaynakCanli ? '[Canlı] ' : '[Yerel] ') : ''}${bulunamadi ? 'Bulunamadı' : s.etiket} · MeDSor Yönetim`; }, [s, bulunamadi, degistirebilir, kaynakCanli]);

  // H312: etkin kapalı küme = kayıt ya da varsayılan
  const kapaliGrup = useMemo(() => kapaliKayit ?? new Set(MENU.map((g) => g.id).filter((id) => id !== 'genel' && id !== s.grup.id)), [kapaliKayit, s.grup.id]);
  const grupDegistir = (id: string) => setKapaliKayit(() => {
    const n = new Set(kapaliGrup); if (n.has(id)) n.delete(id); else n.add(id);
    try { localStorage.setItem('m16_kapali_grup', JSON.stringify([...n])); } catch { /* */ }
    return n;
  });

  return (
    <div className="m16-kok" data-kabuk="v16">
      <header className="m16-ust">
        <button type="button" className="m16-btn hayalet ikon m16-menu-ac" aria-label="Menüyü aç" aria-expanded={menuAcik} onClick={() => setMenuAcik(true)}><Menu aria-hidden="true" /></button>
        <a className="m16-marka" href="/manage" onClick={(e) => { e.preventDefault(); git(''); }}><b>M</b><span>Yönetim</span></a>
        <button type="button" className="m16-ust-ara" onClick={() => setPaletAcik(true)} aria-label="Sayfaya git ya da kayıt ara (Ctrl+K)">
          <Search aria-hidden="true" /><span>Sayfaya git ya da ara…</span><kbd>⌘K</kbd>
        </button>
        <div className="m16-ust-sag">
          <span className="m16-durumnokta" title={`Canlı kanal: ${canli === 'connected' ? 'bağlı' : canli === 'connecting' ? 'bağlanıyor' : 'kopuk'}`}>
            <i aria-hidden="true" style={{ background: canli === 'connected' ? 'var(--color-ok)' : canli === 'connecting' ? 'var(--color-warn)' : 'var(--color-bad)' }} />
          </span>
          {degistirebilir ? (
            <div className="m16-hedef" role="group" aria-label="Veri hedefi">
              <button type="button" className={kaynakCanli ? 'on canli' : ''} aria-pressed={kaynakCanli} onClick={() => !kaynakCanli && hedefSec('oracle')} title="Değişiklikler doğrudan canlı siteye (Oracle) yazılır">Canlı</button>
              <button type="button" className={!kaynakCanli ? 'on' : ''} aria-pressed={!kaynakCanli} onClick={() => kaynakCanli && hedefSec('yerel')} title="Yerel sunucu (bu makine)">Yerel</button>
            </div>
          ) : null}
          <button type="button" className="m16-btn hayalet ikon" onClick={toggle} aria-label={theme === 'dark' ? 'Açık temaya geç' : 'Koyu temaya geç'}>{theme === 'dark' ? <Sun aria-hidden="true" /> : <Moon aria-hidden="true" />}</button>
          <button type="button" className="m16-btn hayalet ikon" onClick={onExit} aria-label="Siteye dön" title={adminEmail}><ArrowLeft aria-hidden="true" /></button>
        </div>
      </header>
      {kaynakCanli && degistirebilir && <div className="m16-canlibant" role="note">Canlı veriye bağlısınız: yaptığınız değişiklikler doğrudan siteye yazılır.</div>}
      {/* H153: Yerel kipte de hangi veriye bakıldığı görünür (eskiden yalnız Canlı'da bant vardı) */}
      {!kaynakCanli && degistirebilir && <div className="m16-canlibant is-yerel" role="note">Yerel sunucuya bağlısınız: gördüğünüz veri bu makinedeki kopya, değişiklikler canlı siteyi etkilemez.</div>}
      <div className="m16-govde">
        {menuAcik && <div className="m16-menu-perde" onClick={() => setMenuAcik(false)} aria-hidden="true" />}
        <nav className={`m16-menu ${menuAcik ? 'acik' : ''}`} aria-label="Yönetim menüsü">
          {/* H313: menü içi süzgeç (etiket + anahtar); Esc temizler */}
          <div className="m16-menu-ara">
            <Search aria-hidden="true" />
            <input type="search" value={menuAra} placeholder="Menüde ara" aria-label="Menüde ara"
              onChange={(e) => setMenuAra(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Escape' && menuAra) { e.preventDefault(); e.stopPropagation(); setMenuAra(''); } }} />
            {menuAra && <button type="button" aria-label="Süzgeci temizle" onClick={() => setMenuAra('')}><X aria-hidden="true" /></button>}
          </div>
          {!araF && sabitSayfalar.length > 0 && (
            <div className="m16-menu-grup m16-menu-ozel" data-grup="sabit">
              <div className="m16-menu-baslik">Sabitlenenler</div>
              {sabitSayfalar.map((x) => oge(x))}
            </div>
          )}
          {!araF && sonSayfalar.length > 0 && (
            <div className="m16-menu-grup m16-menu-ozel" data-grup="son">
              <div className="m16-menu-baslik">Son kullanılanlar</div>
              {sonSayfalar.map((x) => oge(x))}
            </div>
          )}
          {MENU.map((g) => {
            const liste = g.sayfalar.filter(eslesir);
            if (araF && liste.length === 0) return null;
            const acik = !!araF || g.id === 'genel' || !kapaliGrup.has(g.id);
            return (
              <div key={g.id} className="m16-menu-grup" data-grup={g.id}>
                {g.id !== 'genel' && (
                  <button type="button" aria-expanded={acik} disabled={!!araF} onClick={() => grupDegistir(g.id)}>
                    {g.etiket}{acik ? <ChevronDown aria-hidden="true" /> : <ChevronRight aria-hidden="true" />}
                  </button>
                )}
                {acik ? liste.map((x) => oge(x)) : null}
              </div>
            );
          })}
          {araF && !TUM_SAYFALAR.some(eslesir) && <p className="m16-menu-bos">Eşleşen sayfa yok.</p>}
        </nav>
        <main ref={icerikRef} className="m16-icerik" tabIndex={-1} style={{ outline: 'none' }}>
          {s.yol !== '' && !bulunamadi && (
            <nav className="m16-kirinti" aria-label="Konum">
              <a href="/manage" onClick={(e) => { e.preventDefault(); git(''); }}>Yönetim</a><ChevronRight aria-hidden="true" />
              {/* H366: Genel bakış grubunun ilk sayfası "Yönetim" ile aynı yer; Gelen gibi kardeş sayfalar onun alt sayfası gibi görünmesin */}
              {s.grup.sayfalar[0].yol !== '' && <><a href={manageAdres(s.grup.sayfalar[0].yol)} onClick={(e) => { e.preventDefault(); git(s.grup.sayfalar[0].yol); }}>{s.grup.etiket}</a><ChevronRight aria-hidden="true" /></>}
              {cozum.altYol.length ? <a href={manageAdres(s.yol)} onClick={(e) => { e.preventDefault(); git(s.yol); }}>{s.etiket}</a> : <span aria-current="page">{s.etiket}</span>}
              {cozum.altYol.length > 0 && <><ChevronRight aria-hidden="true" /><span aria-current="page">{cozum.altYol.join(' / ')}</span></>}
            </nav>
          )}
          <SayfaSiniri anahtar={konum}>
            {bulunamadi ? (
              <BosDurum baslik="Sayfa bulunamadı" aciklama={`/manage/${cozum.altYol.join('/')} adresi yok.`} eylem={<button type="button" className="m16-btn" onClick={() => git('')}>Genel bakışa dön</button>} />
            ) : Sayfa ? (
              <Suspense fallback={<Yukleniyor satir={6} />}>
                <Sayfa key={`${s.yol}#${gezinti}`} id={cozum.altYol[0]} altYol={cozum.altYol} git={git} />
              </Suspense>
            ) : <Yakinda s={s} />}
          </SayfaSiniri>
        </main>
      </div>
      {paletAcik && <Palet kapat={() => setPaletAcik(false)} git={git} />}
      <OnayHost />
      <BildirimHost />
    </div>
  );
};

export default ManageV16;
