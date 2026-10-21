import React, { useEffect, useState } from 'react';
import { GitMerge } from 'lucide-react';
import { loadMergeInfo, mergeAccount, type MergeInfo } from '../../services/peopleService';
import { ConfirmButton } from './consoleUi';

/**
 * Kişiler › Çalışma üstü: aynı öğrencinin ikinci hesabını asıl hesaba bağla. İkinci hesap sıralamadan çıkar (kayıt
 * silinmez, geri alınabilir); "çalışma verisini aktar" seçiliyse asılda olmayan konular eklenir, süre/soru büyüğü
 * alınır, konu durumu asıl hesabınki kalır. Aktarımdan önce asıl hesabın yedeği sunucuda saklanır.
 */
export const HesapBirlestir: React.FC<{ personKey: string; notify: (m: string) => void; reload: () => void }> = ({ personKey, notify, reload }) => {
  const [info, setInfo] = useState<MergeInfo | null>(null);
  const [hedef, setHedef] = useState('');
  const [aktar, setAktar] = useState(true);
  const [busy, setBusy] = useState(false);
  const [acik, setAcik] = useState(false);

  const yukle = (h = hedef) => loadMergeInfo(personKey, h || undefined).then(setInfo, () => setInfo(null));
  useEffect(() => { setHedef(''); setAcik(false); void loadMergeInfo(personKey).then(setInfo, () => setInfo(null)); }, [personKey]);
  useEffect(() => { if (hedef) void yukle(hedef); }, [hedef]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!info?.uid) return null;
  const run = async (body: Parameters<typeof mergeAccount>[1], msg: string) => {
    setBusy(true);
    try {
      const r = await mergeAccount(personKey, body);
      notify(r.aktarim ? `${msg} ${r.aktarim.eklenen} konu eklendi, ${r.aktarim.artan} konuda süre/soru güncellendi.` : msg);
      setHedef(''); setAcik(false);
      await yukle('');
      reload();
    } catch (e: any) {
      notify(e?.message || 'Birleştirilemedi.');
    } finally {
      setBusy(false);
    }
  };

  if (info.bag)
    return (
      <div className="pp-card hb-kart">
        <GitMerge aria-hidden="true" />
        <span>Bu hesap <b>{info.bag.ad}</b> hesabına bağlı; sıralamada görünmüyor.{info.bag.key && <> <a href={`/manage/kisiler/${encodeURIComponent(info.bag.key)}?sekme=calisma`}>Asıl hesabı aç</a></>}</span>
        <ConfirmButton className="ms-btn is-sm" disabled={busy} confirmLabel="Evet, kaldır" onConfirm={() => run({ geriAl: true }, 'Bağ kaldırıldı; hesap yeniden sıralamada.')}>Bağı kaldır</ConfirmButton>
      </div>
    );

  if (!acik)
    return (
      <div className="pp-card hb-kart">
        <GitMerge aria-hidden="true" />
        <span>Bu öğrencinin ikinci hesabı mı? Asıl hesaba bağlayıp sıralamada tek satıra indirebilirsin.</span>
        <button type="button" className="ms-btn is-sm" onClick={() => setAcik(true)}>Hesap birleştir</button>
      </div>
    );

  const o = info.onizleme;
  return (
    <div className="pp-card hb-kart is-acik">
      <div className="hb-satir">
        <GitMerge aria-hidden="true" />
        <b>Bu hesabı şu hesaba bağla (asıl hesap kalır):</b>
        <select className="ps-sel" value={hedef} onChange={(e) => setHedef(e.target.value)} aria-label="Asıl hesap">
          <option value="">Asıl hesabı seç…</option>
          {info.adaylar.map((a) => <option key={a.key} value={a.key}>{a.ad}{a.email ? ` · ${a.email}` : ''}</option>)}
        </select>
      </div>
      <label className="hb-satir"><input type="checkbox" checked={aktar} onChange={(e) => setAktar(e.target.checked)} /> Çalışma verisini asıl hesaba aktar (kayıpsız birleşim)</label>
      {hedef && o && (
        <p className="pp-muted">
          Bu hesapta {o.kaynakKonu}, asıl hesapta {o.hedefKonu} konu var. Aktarımda <b>{o.eklenen}</b> konu eklenecek, <b>{o.artan}</b> konuda süre/soru büyüyecek.
          {o.durumFarki > 0 && <> {o.durumFarki} konuda durum farklı; asıl hesabın durumu korunur.</>}
          {o.eklenen === 0 && o.artan === 0 && ' Asıl hesap bu hesabın tüm verisini zaten kapsıyor.'}
        </p>
      )}
      <div className="hb-satir">
        <ConfirmButton className="ms-btn is-sm is-primary" disabled={busy || !hedef} confirmLabel="Evet, birleştir" onConfirm={() => run({ hedef, calismaAktar: aktar }, 'Hesap birleştirildi.')}>Birleştir</ConfirmButton>
        <button type="button" className="ms-btn is-sm" onClick={() => { setAcik(false); setHedef(''); }}>Vazgeç</button>
      </div>
      <p className="pp-muted">Bu hesap silinmez; yalnız sıralamadan çıkar ve istediğin an bağı kaldırabilirsin. Aktarımdan önce asıl hesabın yedeği alınır.</p>
    </div>
  );
};
