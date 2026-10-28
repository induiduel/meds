import React, { useMemo, useState } from 'react';
import { BookmarkPlus, CheckCircle2, CircleHelp, Flag, Heart, NotebookPen, PenLine, XCircle } from 'lucide-react';
import { dayKey, getActivity, getStudySeconds, type ActivityKind } from '../../services/activityLog';
import { profilOku } from '../../services/profilKurulum';
import '../../styles/v15/liste2.css';

/**
 * v15 · Çalışma masam üst bölümü (tasarım B21 b2masa): hafta şeridi (çalıştığın günler noktalı), seçili günün akışı
 * (cihazdaki etkinlik günlüğünden saatli: çözülen/yanlış soru, test, bitirilen ders, not…), yanda bugünkü süre (profil
 * hedefine göre çubuk) ve seri. Uydurma plan yok: akış yalnız yaptığın işlerden oluşur.
 */
const IKON: Record<ActivityKind, [React.ElementType, string, string]> = {
  coz: [CheckCircle2, 'is-ok', 'Soru çözdün'],
  yanlis: [XCircle, 'is-b', 'Yanlış yaptın'],
  test: [CircleHelp, '', 'Test'],
  bitir: [Flag, 'is-ok', 'Bitirdin'],
  not: [NotebookPen, 'is-w', 'Not'],
  begen: [Heart, 'is-b', 'Beğendin'],
  kaydet: [BookmarkPlus, '', 'Kaydettin'],
  katki: [PenLine, 'is-ai', 'Katkı'],
};
const GUN = ['Pt', 'Sa', 'Ça', 'Pe', 'Cu', 'Ct', 'Pz'];
const dk = (sn: number) => { const m = Math.round(sn / 60), h = Math.floor(m / 60); return h ? `${h} sa ${m % 60} dk` : `${m} dk`; };

/** Bugün sayfasına gömülü (H220): yan kartlar (bugünkü süre, seri) Bugün'ün halkası ve şeridiyle aynı bilgi; gizlenir */
export default function MasaGunV15({ gomulu = false }: { gomulu?: boolean } = {}) {
  const saniye = useMemo(() => getStudySeconds(), []);
  const olay = useMemo(() => getActivity(), []);
  const bugun = new Date();
  const [sec, setSec] = useState(dayKey(bugun));
  const hafta = useMemo(() => {
    const pzt = new Date(bugun); pzt.setDate(bugun.getDate() - ((bugun.getDay() + 6) % 7));
    return Array.from({ length: 7 }, (_, i) => { const d = new Date(pzt); d.setDate(pzt.getDate() + i); return d; });
  }, []);
  const gunOlay = olay.filter((e) => dayKey(new Date(e.at)) === sec).sort((a, b) => a.at.localeCompare(b.at));
  // aynı türden ardışık olaylar tek satırda toplanır (20 soru çözümü = 1 satır)
  const akis = gunOlay.reduce<{ kind: ActivityKind; at: string; son: string; n: number; text: string }[]>((a, e) => {
    const s = a[a.length - 1];
    if (s && s.kind === e.kind && (e.kind === 'coz' || e.kind === 'yanlis')) { s.n += 1; s.son = e.at; } else a.push({ kind: e.kind, at: e.at, son: e.at, n: 1, text: e.text });
    return a;
  }, []);
  const bugunSn = saniye[dayKey(bugun)] || 0;
  const hedefSn = (profilOku().hedef?.dk || 0) * 60;
  const seri = (() => { let n = 0; const d = new Date(bugun); if (!(saniye[dayKey(d)] > 0)) d.setDate(d.getDate() - 1); while (saniye[dayKey(d)] > 0) { n += 1; d.setDate(d.getDate() - 1); } return n; })();
  const enUzun = (() => {
    const g = Object.keys(saniye).filter((k) => saniye[k] > 0).sort();
    let en = 0, cur = 0, onceki = '';
    g.forEach((k) => { const d = new Date(`${k}T12:00:00`); d.setDate(d.getDate() - 1); cur = onceki === dayKey(d) ? cur + 1 : 1; en = Math.max(en, cur); onceki = k; });
    return en;
  })();
  const saat = (iso: string) => new Date(iso).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });

  return (
    <section className={`ms15${gomulu ? ' is-gomulu' : ''}`} aria-label="Yaptıkların">
      <div className="ms15-hafta" role="tablist" aria-label="Hafta">
        {hafta.map((d, i) => {
          const k = dayKey(d);
          const gelecek = d > bugun && k !== dayKey(bugun);
          return (
            <button key={k} type="button" role="tab" aria-selected={sec === k} disabled={gelecek} className={sec === k ? 'is-on' : ''} onClick={() => setSec(k)}
              aria-label={`${d.toLocaleDateString('tr-TR', { weekday: 'long', day: 'numeric', month: 'long' })}${saniye[k] ? `, ${dk(saniye[k])} çalıştın` : ''}`}>
              <small>{GUN[i]}</small><b>{d.getDate()}</b>{saniye[k] > 0 && <i aria-hidden />}
            </button>
          );
        })}
      </div>
      <div className="ms15-cols">
        <div className="v15-card ms15-akis">
          <div className="ms15-bas"><b>{sec === dayKey(bugun) ? 'Bugün yaptıkların' : new Date(`${sec}T12:00:00`).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', weekday: 'long' })}</b><span className="v15-cap">{akis.length ? `${gunOlay.length} etkinlik` : ''}</span></div>
          {akis.length ? (
            <ol className="ms15-liste">
              {akis.slice(-12).map((e, i) => {
                const [Ik, ton, ad] = IKON[e.kind] || IKON.test;
                return (
                  <li key={i}>
                    <span className="ms15-saat">{saat(e.at)}</span>
                    <span className={`v15-tile ${ton}`}><Ik aria-hidden /></span>
                    <span className="ms15-t"><b>{e.n > 1 ? `${e.n} soru ${e.kind === 'coz' ? 'çözdün' : 'yanlış'}` : ad}</b><small>{e.n > 1 ? `${saat(e.at)}–${saat(e.son)}` : e.text}</small></span>
                  </li>
                );
              })}
            </ol>
          ) : <p className="ms15-bos">{sec === dayKey(bugun) ? 'Bugün henüz bir şey yapmadın. Soru çözdükçe, ders bitirdikçe akış burada oluşur.' : 'Bu gün kayıtlı etkinlik yok.'}</p>}
        </div>
        {!gomulu && <div className="ms15-yan">
          <div className="v15-card ms15-mini"><span className="v15-label">Bugün</span><b>{dk(bugunSn)}</b>
            {hedefSn > 0 && <><span className="v15-bar"><span style={{ width: `${Math.min(100, (bugunSn / hedefSn) * 100)}%` }} /></span><small>hedef {dk(hedefSn)}</small></>}
          </div>
          <div className="v15-card ms15-mini"><span className="v15-label">Seri</span><b>{seri} gün</b><small>en uzun {Math.max(seri, enUzun)} gün</small></div>
        </div>}
      </div>
    </section>
  );
}
