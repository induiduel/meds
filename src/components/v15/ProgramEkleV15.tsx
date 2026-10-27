import React, { useEffect, useMemo, useState } from 'react';
import { CalendarCheck, Plus, Trash2 } from 'lucide-react';
import { linkClick, navigateTo, pathFor } from '../../router';
import { aktifKurul, bugun } from '../../services/kurulTakvimi';
import { programYukle } from '../../services/programVeri';
import { kisiselEkle, kisiselSil, useKisiselProgram } from '../../services/kisiselProgram';
import { saatYaz, tarihYaz, useBolge } from '../../services/bolgeTercih';
import { useV15Baslik } from './baslik';
import '../../styles/v15/kisisel.css';

/**
 * v15 · Programa ekle (tasarım AA06 dpEkle) — /dersler/program/ekle (iç /program-ekle).
 * Hazır sınıf programı: ders kayıt defterindeki resmî kurul programı (zaten Ders programı sayfasında).
 * Elle ekleme: öğrencinin kendi etkinlikleri (lab, telafi, grup çalışması) — profil anahtarı medsoru_kisisel_program_v1;
 * Ders programı sayfasında ve Bugün kartında resmî derslerin yanında görünür. PDF/fotoğraftan okuma yok (uydurma seçenek gösterilmez).
 */
export default function ProgramEkleV15() {
  const g = bugun();
  const kurul = aktifKurul(g);
  const bolge = useBolge();
  const liste = useKisiselProgram();
  const [say, setSay] = useState<number | null>(null);
  const [f, setF] = useState({ baslik: '', tarih: g, bas: '13:00', bit: '14:00', yer: '' });
  const [hata, setHata] = useState('');
  const [tamam, setTamam] = useState('');
  useV15Baslik({ baslik: 'Programa ekle', alt: 'Ders programı', geri: pathFor('ders_programi') });
  useEffect(() => { let c = true; programYukle(kurul.kurul).then((d) => c && setSay(d.length), () => c && setSay(0)); return () => { c = false; }; }, [kurul.kurul]);

  const gruplar = useMemo(() => {
    const m = new Map<string, typeof liste>();
    for (const e of liste) m.set(e.tarih, [...(m.get(e.tarih) || []), e]);
    return [...m];
  }, [liste]);

  const gonder = (e: React.FormEvent) => {
    e.preventDefault();
    setTamam('');
    const baslik = f.baslik.trim();
    if (!baslik) return setHata('Etkinliğe bir ad ver.');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(f.tarih)) return setHata('Tarih seç.');
    if (!f.bas || !f.bit || f.bit <= f.bas) return setHata('Bitiş saati başlangıçtan sonra olmalı.');
    kisiselEkle({ baslik: baslik.slice(0, 80), tarih: f.tarih, bas: f.bas, bit: f.bit, yer: f.yer.trim().slice(0, 60) || undefined });
    setHata('');
    setTamam(`${baslik} eklendi.`);
    setF((x) => ({ ...x, baslik: '', yer: '' }));
  };
  const programHref = pathFor('ders_programi');

  return (
    <div className="kp15">
      <h1 className="sr-only">Programa ekle</h1>
      <a className="kp15-hazir v15-card" href={programHref} onClick={linkClick(() => navigateTo(programHref))}>
        <span className="v15-tile is-ok"><CalendarCheck aria-hidden /></span>
        <span className="kp15-t">
          <b>Sınıf programı (hazır)</b>
          <span className="v15-cap">{kurul.ad.toLocaleLowerCase('tr-TR').replace(/(^|\s)(\p{L})/gu, (_, a: string, b: string) => a + b.toLocaleUpperCase('tr-TR'))}{say != null ? ` · ${say} ders` : ''} · resmî ders programından</span>
        </span>
        <span className="v15-tag is-ok">Hazır</span>
      </a>

      <form className="kp15-form v15-card" onSubmit={gonder} noValidate>
        <h2 className="v15-h2">Elle etkinlik ekle</h2>
        <p className="v15-cap">Laboratuvar, telafi dersi ya da grup çalışması gibi kendi etkinliklerin ders programında resmî derslerin yanında görünür. Yalnız sende görünür, hesabınla cihazların arasında eşitlenir.</p>
        <label className="kp15-f"><span>Ad</span><input value={f.baslik} maxLength={80} onChange={(e) => setF({ ...f, baslik: e.target.value })} placeholder="Örn. Mikrobiyoloji lab" /></label>
        <div className="kp15-row">
          <label className="kp15-f"><span>Tarih</span><input type="date" value={f.tarih} onChange={(e) => setF({ ...f, tarih: e.target.value })} /></label>
          <label className="kp15-f"><span>Başlangıç</span><input type="time" value={f.bas} onChange={(e) => setF({ ...f, bas: e.target.value })} /></label>
          <label className="kp15-f"><span>Bitiş</span><input type="time" value={f.bit} onChange={(e) => setF({ ...f, bit: e.target.value })} /></label>
        </div>
        <label className="kp15-f"><span>Yer (isteğe bağlı)</span><input value={f.yer} maxLength={60} onChange={(e) => setF({ ...f, yer: e.target.value })} placeholder="Örn. Amfi 2" /></label>
        {hata && <p className="kp15-hata" role="alert">{hata}</p>}
        {tamam && <p className="kp15-ok" role="status">{tamam}</p>}
        <button type="submit" className="v15-btn"><Plus aria-hidden /> Programa ekle</button>
      </form>

      <section aria-labelledby="kp15-l">
        <h2 id="kp15-l" className="v15-label kp15-sec">Eklediklerin</h2>
        {!gruplar.length ? (
          <p className="b15-bos v15-card kp15-bos">Henüz kendi etkinliğin yok. Eklediğin etkinlikler burada ve ders programında listelenir.</p>
        ) : (
          <div className="kp15-gruplar">
            {gruplar.map(([t, l]) => (
              <div key={t}>
                <h3 className={`v15-cap kp15-gun${t < g ? ' is-gecti' : ''}`}>{tarihYaz(t, bolge)}</h3>
                <ul className="kp15-l v15-card">
                  {l.map((e) => (
                    <li key={e.id}>
                      <span className="kp15-s">{saatYaz(e.bas, bolge)}<small>{saatYaz(e.bit, bolge)}</small></span>
                      <span className="kp15-t"><b>{e.baslik}</b>{e.yer && <span className="v15-cap">{e.yer}</span>}</span>
                      <button type="button" className="v15-ib kp15-sil" onClick={() => kisiselSil(e.id)} aria-label={`${e.baslik} etkinliğini sil`} title="Sil"><Trash2 aria-hidden /></button>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
