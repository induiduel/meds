/**
 * Yönetim › Puan ve ATP (/manage/puan-atp): kişi bazında başarım hesabı.
 * - Liste: puan (toplam/hafta/kurul), ATP bakiyesi + kuyruk, kilitler, gizli unvan; ara, sırala.
 * - Kişi: puan/ATP ekle-düş, kuyruğu aktar/sil, kilit ver/geri al (iadeli), dönem/kurul, gizli unvan (sınır muafiyeti),
 *   ödül geri alma; ödül defteri ve o kişinin yönetim geçmişi.
 * - Günlük: tüm yönetici işlemleri (önce/sonra) — sunucuda data/basarim/yonetim_gunlugu.jsonl (yalnız ekleme).
 * Her işlem gerekçe ister. Uçlar: /api/admin/basarim/* (src/services/basarim/basarimRoutes.ts).
 */
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { Coins, Crown, History, RefreshCw, RotateCcw, Users } from 'lucide-react';
import { adminCall } from '../../services/peopleService';
import { Panel, EmptyState, Drawer, Seg, SearchBox, timeLabel } from './consoleUi';
import { AtpIkon, OdulCip } from '../basarim/ortak';
import type { Odul, Tanim } from '../../services/basarimIstemci';
import '../../styles/basarim.css';
import './manage-basarim.css';

interface Satir {
  uid: string; ad: string; email: string; donem: number | null; kurul: number | null; birlesti: string | null;
  puan: number; hafta: number; kurulPuan: number; atp: number; kuyruk: number; kilit: number; basarim: number; sonGiris: string;
  ozel: { unvan: string; muaf: boolean; gorunur: boolean; at: string; by: string } | null;
  kidem?: string; tavan?: number | null;
}
interface Gunluk { at: string; by: string; uid: string; ad: string; tur: string; gerekce: string; ayrinti: any; once: any; sonra: any }
interface KisiAyrinti {
  kisi: { uid: string; ad: string; email?: string; donem: number | null; kurul: number | null; defter: Odul[]; kilit: Record<string, string>; atp: { bakiye: number; kuyruk: { id: string; a: number; ad: string; at: string }[] }; eylem: { toplam: Record<string, number> }; ozel?: Satir['ozel']; birlesti?: string };
  ozet: { puan: { toplam: number; bugun: number }; seri: number; siralama: Record<'hafta' | 'kurul' | 'tum', { sira: number | null; kisi: number; puan: number }> };
  gunluk: Gunluk[];
}

const sayi = (n: number) => Math.round(n || 0).toLocaleString('tr-TR');
const TUR_AD: Record<string, string> = {
  puan: 'Puan', atp: 'ATP', kuyruk_aktar: 'Kuyruğu aktar', kuyruk_sil: 'Kuyruğu sil', kilit_ver: 'Kilit verildi', kilit_al: 'Kilit geri alındı',
  profil: 'Dönem/kurul', ozel: 'Gizli unvan', ozel_kaldir: 'Unvan kaldırıldı', odul_geri: 'Ödül geri alındı',
};
type Sirala = 'puan' | 'hafta' | 'atp' | 'son';
const fold = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '');

export const ManageBasarim: React.FC<{ notify: (m: string) => void }> = ({ notify }) => {
  const [mod, setMod] = useState<'kisiler' | 'gunluk'>('kisiler');
  const [liste, setListe] = useState<Satir[] | null>(null);
  const [tanim, setTanim] = useState<Tanim | null>(null);
  const [gunluk, setGunluk] = useState<Gunluk[] | null>(null);
  const [hata, setHata] = useState('');
  const [q, setQ] = useState('');
  const [sirala, setSirala] = useState<Sirala>('puan');
  const [acik, setAcik] = useState<string | null>(null);

  const yukle = useCallback(async () => {
    setHata('');
    try {
      const r = await adminCall<{ kisiler: Satir[]; tanim: Tanim }>('/api/admin/basarim/kisiler');
      setListe(r.kisiler); setTanim(r.tanim);
    } catch (e: any) { setHata(e?.message || 'Yüklenemedi'); }
  }, []);
  const gunlukYukle = useCallback(async () => {
    try { setGunluk((await adminCall<{ gunluk: Gunluk[] }>('/api/admin/basarim/gunluk?limit=1000')).gunluk); } catch (e: any) { setHata(e?.message || 'Günlük yüklenemedi'); }
  }, []);
  useEffect(() => { void yukle(); }, [yukle]);
  useEffect(() => { if (mod === 'gunluk') void gunlukYukle(); }, [mod, gunlukYukle]);

  const gorunen = useMemo(() => {
    const f = fold(q.trim());
    const l = (liste || []).filter((x) => !f || fold(`${x.ad} ${x.email} ${x.uid} ${x.ozel?.unvan || ''}`).includes(f));
    const key: Record<Sirala, (x: Satir) => number | string> = { puan: (x) => x.puan, hafta: (x) => x.hafta, atp: (x) => x.atp, son: (x) => x.sonGiris };
    return [...l].sort((a, b) => (key[sirala](b) > key[sirala](a) ? 1 : key[sirala](b) < key[sirala](a) ? -1 : 0));
  }, [liste, q, sirala]);
  const toplam = useMemo(() => (liste || []).reduce((a, x) => ({ atp: a.atp + x.atp, kuyruk: a.kuyruk + x.kuyruk, ozel: a.ozel + (x.ozel ? 1 : 0) }), { atp: 0, kuyruk: 0, ozel: 0 }), [liste]);

  return (
    <>
      <Panel
        title="Puan ve ATP"
        icon={Coins}
        count={liste ? `${liste.length} kişi · ${sayi(toplam.atp)} mol dolaşımda${toplam.kuyruk ? ` · ${sayi(toplam.kuyruk)} kuyrukta` : ''}${toplam.ozel ? ` · ${toplam.ozel} gizli unvan` : ''}` : undefined}
        desc="Kişi bazında puan, ATP, kilit ve gizli unvan yönetimi. Her işlem gerekçe ister, öğrencinin ödül defterine ve kalıcı yönetim günlüğüne (önce/sonra) yazılır."
        tools={
          <>
            <Seg value={mod} onChange={setMod} label="Görünüm" options={[{ id: 'kisiler' as const, label: 'Kişiler' }, { id: 'gunluk' as const, label: 'Yönetim günlüğü' }]} />
            <button type="button" className="ms-btn" onClick={() => { void yukle(); if (mod === 'gunluk') void gunlukYukle(); }}><RefreshCw aria-hidden /> Yenile</button>
          </>
        }
      >
        {hata && <p className="mbs-hata" role="alert">{hata}</p>}
        {mod === 'kisiler' ? (
          <>
            <div className="mbs-arac">
              <SearchBox value={q} onChange={setQ} placeholder="Ad, e-posta, uid ya da unvan ara" count={liste ? `${gorunen.length}` : undefined} />
              <Seg value={sirala} onChange={setSirala} label="Sırala" options={[{ id: 'puan' as const, label: 'Puan' }, { id: 'hafta' as const, label: 'Bu hafta' }, { id: 'atp' as const, label: 'ATP' }, { id: 'son' as const, label: 'Son giriş' }]} />
            </div>
            {!liste ? <p className="mbs-soluk">Yükleniyor…</p> : !gorunen.length ? <EmptyState icon={Users} title="Kişi yok" /> : (
              <div className="mbs-tablokap">
                <table className="mbs-tablo">
                  <thead><tr><th>Kişi</th><th>Dönem</th><th>Kıdem</th><th className="is-sayi">Puan</th><th className="is-sayi">Hafta</th><th className="is-sayi">ATP</th><th className="is-sayi">Kuyruk</th><th className="is-sayi">Kilit</th><th>Son giriş</th></tr></thead>
                  <tbody>
                    {gorunen.map((x) => (
                      <tr key={x.uid} onClick={() => setAcik(x.uid)} className={x.birlesti ? 'is-birlesik' : ''} tabIndex={0} onKeyDown={(e) => { if (e.key === 'Enter') setAcik(x.uid); }}>
                        <td>
                          <b>{x.ad || 'Adsız'}</b>
                          {x.ozel && <span className="bs-ozel-unvan mbs-unvan"><Crown aria-hidden />{x.ozel.unvan}{x.ozel.muaf ? ' · muaf' : ''}</span>}
                          {x.birlesti && <span className="mbs-etiket">ikinci hesap</span>}
                          <small>{x.email || x.uid}</small>
                        </td>
                        <td>{x.donem ? `${x.donem}/${x.kurul}` : '—'}</td>
                        <td>{x.kidem || '—'}<small>{x.tavan == null ? 'sınırsız' : `${x.tavan} mol/gün`}</small></td>
                        <td className="is-sayi">{sayi(x.puan)}</td>
                        <td className="is-sayi">{sayi(x.hafta)}</td>
                        <td className="is-sayi is-atp">{sayi(x.atp)}</td>
                        <td className="is-sayi">{x.kuyruk ? sayi(x.kuyruk) : '—'}</td>
                        <td className="is-sayi">{x.kilit || '—'}</td>
                        <td>{x.sonGiris ? timeLabel(x.sonGiris, true) : '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        ) : !gunluk ? <p className="mbs-soluk">Yükleniyor…</p> : !gunluk.length ? <EmptyState icon={History} title="Henüz yönetici işlemi yok" /> : (
          <GunlukListe gunluk={gunluk} kisiAc={setAcik} />
        )}
      </Panel>
      <Drawer open={!!acik} onClose={() => setAcik(null)} wide title={liste?.find((x) => x.uid === acik)?.ad || 'Kişi'} label="Kişinin puan ve ATP hesabı">
        {acik && tanim && <KisiPaneli uid={acik} tanim={tanim} notify={notify} onDegisti={() => { void yukle(); if (mod === 'gunluk') void gunlukYukle(); }} />}
      </Drawer>
    </>
  );
};

function GunlukListe({ gunluk, kisiAc }: { gunluk: Gunluk[]; kisiAc?: (uid: string) => void }) {
  return (
    <ol className="mbs-gunluk">
      {gunluk.map((g, i) => (
        <li key={`${g.at}-${i}`}>
          <div className="mbs-g-ust">
            <span className="mbs-g-tur">{TUR_AD[g.tur] || g.tur}</span>
            {kisiAc ? <button type="button" className="mbs-baglanti" onClick={() => kisiAc(g.uid)}>{g.ad || g.uid}</button> : null}
            <time dateTime={g.at}>{timeLabel(g.at, true)}</time>
          </div>
          <p className="mbs-g-gerekce">{g.gerekce}</p>
          <p className="mbs-g-fark">
            {g.once?.puan !== g.sonra?.puan && <span>Puan {sayi(g.once?.puan)} → <b>{sayi(g.sonra?.puan)}</b></span>}
            {g.once?.atp !== g.sonra?.atp && <span>ATP {sayi(g.once?.atp)} → <b>{sayi(g.sonra?.atp)}</b></span>}
            {g.once?.kuyruk !== g.sonra?.kuyruk && <span>Kuyruk {sayi(g.once?.kuyruk)} → <b>{sayi(g.sonra?.kuyruk)}</b></span>}
            {g.ayrinti?.id && <span>{g.ayrinti.id}</span>}
            {g.ayrinti?.unvan && <span>Unvan: {g.ayrinti.unvan}</span>}
            <span className="mbs-soluk">· {g.by}</span>
          </p>
        </li>
      ))}
    </ol>
  );
}

function KisiPaneli({ uid, tanim, notify, onDegisti }: { uid: string; tanim: Tanim; notify: (m: string) => void; onDegisti: () => void }) {
  const [v, setV] = useState<KisiAyrinti | null>(null);
  const [hata, setHata] = useState('');
  const [bekle, setBekle] = useState(false);
  const [gerekce, setGerekce] = useState('');
  const [miktar, setMiktar] = useState({ puan: '', atp: '' });
  const [kilitId, setKilitId] = useState('');
  const [iade, setIade] = useState(false);
  const [profil, setProfil] = useState({ donem: '', kurul: '' });
  const [ozel, setOzel] = useState({ unvan: '', muaf: true, gorunur: false });
  const [sekme, setSekme] = useState<'islem' | 'defter' | 'gecmis'>('islem');

  const al = useCallback(async () => {
    try {
      const r = await adminCall<KisiAyrinti>(`/api/admin/basarim/kisi/${encodeURIComponent(uid)}`);
      setV(r);
      setProfil({ donem: String(r.kisi.donem || ''), kurul: String(r.kisi.kurul || '') });
      setOzel({ unvan: r.kisi.ozel?.unvan || '', muaf: r.kisi.ozel?.muaf ?? true, gorunur: r.kisi.ozel?.gorunur ?? false });
    } catch (e: any) { setHata(e?.message || 'Yüklenemedi'); }
  }, [uid]);
  useEffect(() => { setV(null); void al(); }, [al]);

  const islem = async (tur: string, veri: any, onayMetni?: string) => {
    if (gerekce.trim().length < 3) { setHata('Önce gerekçe yaz (en az 3 harf). Gerekçe öğrencinin defterinde ve yönetim günlüğünde görünür.'); return; }
    if (onayMetni && !window.confirm(onayMetni)) return;
    setBekle(true); setHata('');
    try {
      const r = await adminCall<KisiAyrinti>(`/api/admin/basarim/kisi/${encodeURIComponent(uid)}/islem`, { method: 'POST', body: JSON.stringify({ tur, veri, gerekce }) });
      setV(r); setGerekce(''); setMiktar({ puan: '', atp: '' });
      notify(`${TUR_AD[tur] || tur}: kaydedildi.`);
      onDegisti();
    } catch (e: any) { setHata(e?.message || 'İşlem yapılamadı'); } finally { setBekle(false); }
  };

  if (!v) return <p className="mbs-soluk">{hata || 'Yükleniyor…'}</p>;
  const k = v.kisi;
  const kuyruk = k.atp.kuyruk.reduce((a, q) => a + q.a, 0);
  const acikKilitler = tanim.kilitler.filter((x) => k.kilit[x.id]);
  const kapaliKilitler = tanim.kilitler.filter((x) => !k.kilit[x.id]);
  return (
    <div className="mbs-kisi">
      <div className="mbs-ozet">
        <div><span>Puan</span><b>{sayi(v.ozet.puan.toplam)}</b><small>bugün +{sayi(v.ozet.puan.bugun)}</small></div>
        <div className="is-atp"><span><AtpIkon boyut={12} /> ATP</span><b>{sayi(k.atp.bakiye)}</b><small>{kuyruk ? `kuyrukta ${sayi(kuyruk)}` : 'kuyruk boş'}</small></div>
        <div><span>Sıra (hafta / kurul)</span><b>{v.ozet.siralama.hafta.sira ?? '—'} / {v.ozet.siralama.kurul.sira ?? '—'}</b><small>{k.donem ? `${k.donem}. dönem ${k.kurul}. kurul` : 'dönem seçilmedi'}</small></div>
        <div><span>Seri</span><b>{v.ozet.seri} gün</b><small>{Object.entries(k.eylem?.toplam || {}).map(([a, n]) => `${a} ${n}`).join(' · ') || 'topluluk eylemi yok'}</small></div>
      </div>
      {k.ozel && <p className="mbs-ozel-bilgi"><span className="bs-ozel-unvan"><Crown aria-hidden />{k.ozel.unvan}</span> {k.ozel.muaf ? 'Günlük ATP/puan sınırlarından ve içerik kilitlerinden muaf.' : 'Muafiyet yok.'} {k.ozel.gorunur ? 'Sıralamada görünür.' : 'Sıralamada gizli.'} <small>{timeLabel(k.ozel.at, true)} · {k.ozel.by}</small></p>}
      <p className="mbs-soluk mbs-uid">{k.email || ''} · uid {k.uid}</p>

      <Seg value={sekme} onChange={setSekme} label="Bölüm" options={[{ id: 'islem' as const, label: 'İşlemler' }, { id: 'defter' as const, label: `Ödül defteri (${k.defter.length})` }, { id: 'gecmis' as const, label: `Yönetim geçmişi (${v.gunluk.length})` }]} />
      {hata && <p className="mbs-hata" role="alert">{hata}</p>}

      {sekme === 'islem' && (
        <div className="mbs-islemler">
          <label className="mbs-gerekce">
            <span>Gerekçe <em>(her işlem için zorunlu; öğrencinin defterinde görünür)</em></span>
            <input value={gerekce} onChange={(e) => setGerekce(e.target.value)} placeholder="ör. hata bildirimi ödülü, yanlış sayım düzeltmesi" maxLength={300} />
          </label>
          <div className="mbs-kartlar">
            <section>
              <h4>Puan</h4>
              <div className="mbs-satir">
                <input type="number" inputMode="numeric" value={miktar.puan} onChange={(e) => setMiktar((m) => ({ ...m, puan: e.target.value }))} placeholder="ör. 500 ya da -200" aria-label="Puan miktarı" />
                <button type="button" className="ms-btn is-primary" disabled={bekle || !Number(miktar.puan)} onClick={() => void islem('puan', { miktar: Number(miktar.puan) })}>Uygula</button>
              </div>
              <p className="mbs-not">Eksi değer puan düşer. Sıralamaya bugünün puanı olarak işler.</p>
            </section>
            <section>
              <h4>ATP</h4>
              <div className="mbs-satir">
                <input type="number" inputMode="numeric" value={miktar.atp} onChange={(e) => setMiktar((m) => ({ ...m, atp: e.target.value }))} placeholder="ör. 100 ya da -50" aria-label="ATP miktarı" />
                <button type="button" className="ms-btn is-primary" disabled={bekle || !Number(miktar.atp)} onClick={() => void islem('atp', { miktar: Number(miktar.atp) }, Number(miktar.atp) > 0 ? `${miktar.atp} mol doğrudan hesaba eklenecek (günlük sınır uygulanmaz). Onaylıyor musun?` : undefined)}>Uygula</button>
              </div>
              <div className="mbs-satir">
                <button type="button" className="ms-btn is-sm" disabled={bekle || !kuyruk} onClick={() => void islem('kuyruk_aktar', {}, `Kuyruktaki ${kuyruk} mol hemen hesaba geçsin mi?`)}>Kuyruğu hemen aktar</button>
                <button type="button" className="ms-btn is-sm is-danger" disabled={bekle || !kuyruk} onClick={() => void islem('kuyruk_sil', {}, `Kuyruktaki ${kuyruk} mol silinsin mi?`)}>Kuyruğu sil</button>
              </div>
            </section>
            <section>
              <h4>Kilitler</h4>
              <div className="mbs-satir">
                <select value={kilitId} onChange={(e) => setKilitId(e.target.value)} aria-label="Kilit">
                  <option value="">Kilit seç…</option>
                  {kapaliKilitler.length > 0 && <optgroup label="Kapalı (ver)">{kapaliKilitler.map((x) => <option key={x.id} value={x.id}>{x.ad} · {x.fiyat} mol</option>)}</optgroup>}
                  {acikKilitler.length > 0 && <optgroup label="Açık (geri al)">{acikKilitler.map((x) => <option key={x.id} value={x.id}>{x.ad} · açık</option>)}</optgroup>}
                </select>
                {kilitId && !k.kilit[kilitId] && <button type="button" className="ms-btn is-primary" disabled={bekle} onClick={() => void islem('kilit_ver', { id: kilitId })}>Ücretsiz aç</button>}
                {kilitId && k.kilit[kilitId] && <button type="button" className="ms-btn is-danger" disabled={bekle} onClick={() => void islem('kilit_al', { id: kilitId, iade }, `Kilit geri alınsın mı?${iade ? ' Fiyatı iade edilecek.' : ''}`)}>Geri al</button>}
              </div>
              {kilitId && k.kilit[kilitId] && <label className="mbs-onay"><input type="checkbox" checked={iade} onChange={(e) => setIade(e.target.checked)} /> Fiyatı ATP olarak iade et</label>}
              <p className="mbs-not">Açık: {acikKilitler.map((x) => x.ad).join(', ') || 'yok'}</p>
            </section>
            <section>
              <h4>Dönem / kurul</h4>
              <div className="mbs-satir">
                <select value={profil.donem} onChange={(e) => setProfil((p) => ({ ...p, donem: e.target.value }))} aria-label="Dönem">
                  <option value="">Dönem</option>{[1, 2, 3, 4, 5, 6].map((d) => <option key={d} value={d}>{d}. dönem</option>)}
                </select>
                <select value={profil.kurul} onChange={(e) => setProfil((p) => ({ ...p, kurul: e.target.value }))} aria-label="Kurul">
                  <option value="">Kurul</option>{Array.from({ length: 10 }, (_, i) => i + 1).map((d) => <option key={d} value={d}>{d}. kurul</option>)}
                </select>
                <button type="button" className="ms-btn" disabled={bekle || !profil.donem || !profil.kurul} onClick={() => void islem('profil', { donem: Number(profil.donem), kurul: Number(profil.kurul) })}>Kaydet</button>
              </div>
            </section>
            <section className="is-genis">
              <h4><Crown aria-hidden /> Gizli unvan</h4>
              <p className="mbs-not">Mağazada yoktur, yalnız yönetici verir. Muafiyet açıksa günlük ATP sınırı (kuyruk), günlük puan sınırları ve içerik kilitleri bu kişiye uygulanmaz.</p>
              <div className="mbs-satir">
                <input value={ozel.unvan} onChange={(e) => setOzel((o) => ({ ...o, unvan: e.target.value }))} placeholder="ör. Kurucu Tıbbiyeli, Soru Ustası" maxLength={40} aria-label="Unvan" />
                <label className="mbs-onay"><input type="checkbox" checked={ozel.muaf} onChange={(e) => setOzel((o) => ({ ...o, muaf: e.target.checked }))} /> Sınırlardan muaf</label>
                <label className="mbs-onay"><input type="checkbox" checked={ozel.gorunur} onChange={(e) => setOzel((o) => ({ ...o, gorunur: e.target.checked }))} /> Sıralamada göster</label>
              </div>
              <div className="mbs-satir">
                <button type="button" className="ms-btn is-primary" disabled={bekle || !ozel.unvan.trim()} onClick={() => void islem('ozel', ozel)}>{k.ozel ? 'Güncelle' : 'Unvanı ver'}</button>
                {k.ozel && <button type="button" className="ms-btn is-danger" disabled={bekle} onClick={() => void islem('ozel_kaldir', {}, `"${k.ozel!.unvan}" unvanı ve muafiyeti kaldırılsın mı?`)}>Kaldır</button>}
              </div>
            </section>
          </div>
        </div>
      )}

      {sekme === 'defter' && (
        <ol className="bs-defter mbs-defter">
          {k.defter.map((o) => (
            <li key={o.id} className={`is-${o.t}${o.ust ? ' is-ust' : ''}${o.geriAlindi ? ' is-geri' : ''}`}>
              <span className="bs-defter-ad">{o.ad}<time dateTime={o.at}>{timeLabel(o.at, true)}{o.by ? ` · ${o.by}` : ''}{o.geriAlindi ? ` · geri alındı ${timeLabel(o.geriAlindi, true)}` : ''}</time></span>
              <OdulCip p={o.p} a={o.a} kucuk />
              {!o.geriAlindi && o.t !== 'harcama' && (o.p !== 0 || o.a !== 0) && (
                <button type="button" className="ms-btn is-sm" disabled={bekle} title="Bu ödülün puan/ATP etkisini kaldır" onClick={() => void islem('odul_geri', { id: o.id }, `"${o.ad}" geri alınsın mı? Puanı ve ATP'si düşülür.`)}><RotateCcw aria-hidden /> Geri al</button>
              )}
            </li>
          ))}
        </ol>
      )}
      {sekme === 'gecmis' && (v.gunluk.length ? <GunlukListe gunluk={v.gunluk} /> : <p className="mbs-soluk">Bu kişi için yönetici işlemi yok.</p>)}
    </div>
  );
}
