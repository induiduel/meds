/** PDF Stüdyosu ortak parçaları: kapak sayfası ve kapaksız belgenin başlık şeridi. */
import React from 'react';

export interface CoverInfo {
  kicker: string;
  title: string;
  subtitle?: string;
  stats: { value: string | number; label: string }[];
  tags: string[];
  /** Öğrenci kitapçığında ad / numara alanları */
  studentFields?: boolean;
}

const today = () => new Date().toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' });

export const Cover: React.FC<{ info: CoverInfo }> = ({ info }) => (
  <section className="pd-cover">
    <div className="pd-cover-brand"><i>M</i> MedSoru</div>
    <p className="pd-cover-kicker">{info.kicker}</p>
    <h1>{info.title}</h1>
    {info.subtitle && <p className="pd-cover-sub">{info.subtitle}</p>}
    {info.stats.length > 0 && (
      <div className="pd-cover-stats">
        {info.stats.map((s) => (
          <div key={s.label} className="pd-cover-stat">
            <b>{s.value}</b>
            <span>{s.label}</span>
          </div>
        ))}
      </div>
    )}
    {info.tags.length > 0 && (
      <div className="pd-cover-tags">
        {info.tags.map((t) => <span key={t} className="ms-tag">{t}</span>)}
      </div>
    )}
    {info.studentFields && (
      <div className="pd-cover-form">
        <div>Ad soyad</div>
        <div>Öğrenci no</div>
        <div>Tarih</div>
        <div>Puan</div>
      </div>
    )}
    <div className="pd-cover-foot">
      <span>Dönem 3 · {today()}</span>
      <span>medsoru · kişisel çalışma kopyası</span>
    </div>
  </section>
);

export const Masthead: React.FC<{ info: CoverInfo }> = ({ info }) => (
  <header className="pd-masthead">
    <div className="pd-mh-main">
      <p className="m-0 mb-1 text-[11.5px] font-bold uppercase tracking-[0.08em] text-accent">{info.kicker}</p>
      <h1>{info.title}</h1>
      {info.subtitle && <p>{info.subtitle}</p>}
    </div>
    <div className="pd-mh-side">
      {info.stats.slice(0, 3).map((s) => (
        <div key={s.label}>{s.value} {s.label.toLocaleLowerCase('tr-TR')}</div>
      ))}
      <div>{today()}</div>
    </div>
  </header>
);
