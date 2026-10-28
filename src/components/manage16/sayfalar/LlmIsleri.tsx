import React from 'react';
import { SayfaBasligi, IstatistikIzgara, IstatistikKart, Rozet, Hata, Yukleniyor, adminIstek, bildir, onayIste, useAdminSorgu } from '../kit';
import type { SayfaProps } from '../menu';
import './ortak/ts16.css';

/**
 * Sistem › LLM işleri (AGENTS.md kural 20): yalnız durum + ELLE başlat/durdur. Zamanlayıcı ya da otomatik tetik yok;
 * her başlatma yazılı onay ister ve denetim kaydına düşer. MEDS_LLM_OTOMATIK panelden değiştirilemez.
 */
export default function LlmIsleri({ git }: SayfaProps) {
  const s = useAdminSorgu<any>('/api/admin/llm-durum');
  const v = s.veri;
  const calistir = async (f: () => Promise<any>, ok: string) => {
    try { const r = await f(); bildir(r?.message || ok, 'iyi'); void s.yenile(); } catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
  };
  const faz14 = async () => {
    if (!(await onayIste({
      baslik: 'Faz 14 kullanıcı kuyruğu başlatılsın mı?', tehlikeli: true, yazilacak: 'BASLAT', onayMetni: 'Elle başlat',
      aciklama: <>Bekleyen {v?.faz14.bekleyen ?? 0} istek ücretsiz LLM anahtarlarıyla işlenir. Bu bir kerelik elle başlatmadır; kuyruk boşalınca işleyici durur, kendiliğinden yeniden başlamaz.</>,
    }))) return;
    await calistir(async () => {
      const r = await adminIstek<any>('/api/admin/faz14-kuyruk/baslat', { yontem: 'POST', govde: {} });
      return { message: r.basladi ? 'Faz 14 işleyicisi başlatıldı.' : 'Başlatılmadı (kuyruk boş ya da işleyici zaten çalışıyor).' };
    }, '');
  };
  const onarim = async (ac: boolean) => {
    if (ac && !(await onayIste({
      baslik: 'Gemini onarım işçisi açılsın mı?', tehlikeli: true, yazilacak: 'BASLAT', onayMetni: 'Elle aç',
      aciklama: <>Bekleyen {v?.onarim.bekleyen ?? 0} hata bildirimi Gemini ile işlenir. İşçi siz durdurana ya da sunucu yeniden başlayana dek açık kalır (açılışta duraklatılmış başlar).</>,
    }))) return;
    if (!ac && !(await onayIste({ baslik: 'Onarım işçisi duraklatılsın mı?', onayMetni: 'Duraklat' }))) return;
    await calistir(() => adminIstek('/api/admin/auto-repair/toggle-worker', { yontem: 'POST', govde: { paused: !ac } }), ac ? 'Onarım işçisi açıldı.' : 'Onarım işçisi duraklatıldı.');
  };
  return (
    <>
      <SayfaBasligi baslik="LLM işleri" aciklama="LLM kullanan işler yalnız buradan, elle ve onayla başlar (kural 20). Zamanlayıcı yoktur."
        eylemler={<button type="button" className="m16-btn" onClick={() => void s.yenile()}>Yenile</button>} />
      {s.hata && <Hata hata={s.hata} yenile={s.yenile} />}
      {!v && !s.hata && <Yukleniyor satir={3} />}
      {v && (
        <>
          <IstatistikIzgara>
            <IstatistikKart etiket="Otomatik LLM" deger={v.kilit.otomatik ? 'AÇIK' : 'Kapalı'} ton={v.kilit.otomatik ? 'kotu' : 'iyi'} alt="MEDS_LLM_OTOMATIK (salt okunur)" />
            <IstatistikKart etiket="Claude anahtarı (.env)" deger={v.kilit.claudeAnahtari ? 'Tanımlı' : 'Kapalı'} ton={v.kilit.claudeAnahtari ? 'uyari' : 'iyi'} alt="CLAUDE_CODE_OAUTH_TOKEN" />
            {v.zamanlayicilar.map((z: any) => (
              <IstatistikKart key={z.ad} etiket={z.ad.replace('.timer', '')} deger={z.durum || 'yok'} ton={z.durum === 'enabled' ? 'kotu' : 'iyi'} alt="systemd zamanlayıcı" />
            ))}
          </IstatistikIzgara>
          <div className="m16-ts-izgara">
            <section className="m16-kart">
              <h2>Faz 14 kullanıcı kuyruğu</h2>
              <dl className="m16-satirlar">
                <dt>Bekleyen istek</dt><dd>{v.faz14.bekleyen}</dd>
                <dt>İşleyici</dt><dd>{v.faz14.calisiyor ? <Rozet ton="vurgu">Çalışıyor</Rozet> : <Rozet>Durgun</Rozet>}</dd>
              </dl>
              <div className="m16-ts-eylem" style={{ marginTop: 8 }}>
                <button type="button" className="m16-btn birincil" disabled={v.faz14.calisiyor || !v.faz14.bekleyen} onClick={faz14}>Elle başlat…</button>
              </div>
              <p className="m16-ts-not">Durdurma: işleyici kuyruk boşalınca kendisi çıkar. Acil durdurma Betikler/servis üzerinden yapılır.</p>
            </section>
            <section className="m16-kart">
              <h2>Gemini onarım işçisi</h2>
              <dl className="m16-satirlar">
                <dt>Durum</dt><dd>{v.onarim.aktif ? <Rozet ton="vurgu">Açık</Rozet> : <Rozet>Duraklatılmış</Rozet>}</dd>
                <dt>Bekleyen</dt><dd>{v.onarim.bekleyen}</dd>
                <dt>İşleniyor</dt><dd>{v.onarim.isleniyor}</dd>
                <dt>Hatalı</dt><dd>{v.onarim.hata}</dd>
              </dl>
              <div className="m16-ts-eylem" style={{ marginTop: 8 }}>
                {v.onarim.aktif
                  ? <button type="button" className="m16-btn tehlike" onClick={() => onarim(false)}>Duraklat</button>
                  : <button type="button" className="m16-btn birincil" onClick={() => onarim(true)}>Elle aç…</button>}
              </div>
            </section>
            <section className="m16-kart">
              <h2>Ders işçisi</h2>
              <dl className="m16-satirlar">
                <dt>İşçi</dt><dd>{v.dersIsci.ulasilabilir ? <Rozet ton="uyari">Ulaşılabilir</Rozet> : <Rozet ton="iyi">Durdurulmuş</Rozet>}</dd>
              </dl>
              <p className="m16-ts-not">Oracle ders işçisi 2026-10-27'de durduruldu; yeni dersler oturumda elle üretilir (el kitabı §19). Panelden başlatma yok.</p>
              <a href="/manage?kabuk=v14" onClick={(e) => { e.preventDefault(); window.location.href = '/manage/yeni-dersler?kabuk=v14'; }}>Eski arşiv ekranı</a>
            </section>
          </div>
          <p className="m16-ts-not">Başlatma ve durdurmalar <a href="#" onClick={(e) => { e.preventDefault(); git('sistem/denetim?q=faz14'); }}>denetim kaydına</a> yazılır.</p>
        </>
      )}
    </>
  );
}
