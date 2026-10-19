import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowLeft,
  BookOpen,
  Check,
  CheckCircle2,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Dna,
  Download,
  FileSpreadsheet,
  FileText,
  HelpCircle,
  Layers,
  LifeBuoy,
  Maximize2,
  Pause,
  Play,
  RotateCcw,
  Search,
  Sparkles,
  Target,
  Volume2,
  XCircle,
  Zap,
} from 'lucide-react';
import { getCustomApiUrl } from '../../services/api';
import { PatolojiAsistan } from '../spots/asistan/PatolojiAsistan';
import {
  GENETIK_BOLUMLER,
  GENETIK_SORU_CEVAPLAR,
  GENETIK_SORULAR,
  GENETIK_SPOTLAR,
  GENETIK_TABLOLAR,
  GenetikBolumId,
  GenetikZenginSoru,
  KALIP_META,
  SecenekHarf,
} from './genetikCheckupVeri';
import { GENETIK_PDF_MODLAR, GenetikPdfMod, genetikCheckupPdfIndir } from './genetikCheckupPdf';
import g07Raw from '../../data/genetik_asistan/g07.json';
import genetikDizinRaw from '../../data/genetik_asistan/index.json';
import '../../styles/checkup.css';

type SekmeTipi = 'anlatici' | 'hepsi' | 'tablolar' | 'spotlar' | 'soru_cevap' | 'sorular';
type SoruFiltreTipi = 'hepsi' | 'cikmis' | 'ornek';

interface KlipVeri {
  v: string;
  sure: number;
  zaman: [number, number][];
}

interface AsistanSoru {
  k: string;
  tur: 'cikmis' | 'ornek';
  sinav?: string;
  kok: string;
  secenekler: Record<string, string>;
  dogru: string;
  dogruMetin: string;
  yanlis: Record<string, string>;
  yardim: Record<string, string>;
}

interface AsistanNokta {
  id: string;
  bolum: number;
  puan: number;
  aday: number | null;
  kategori: string;
  baslik: string;
  bilgi: string;
  cumleler: string[];
  sorular: AsistanSoru[];
}

interface AsistanDers {
  kod: string;
  no: number;
  baslik: string;
  giris: string[];
  kapanis: string[];
  bolumler: { baslik: string; neden: string }[];
  noktalar: AsistanNokta[];
  klip: Record<string, KlipVeri>;
}

const g07 = g07Raw as unknown as AsistanDers;
const DIZIN_DERSLER = (genetikDizinRaw as any).dersler as {
  kod: string;
  no: number;
  baslik: string;
  adim: number;
  soru: number;
  sure: number;
}[];

const BOLUM_HARITASI: Record<number, GenetikBolumId[]> = {
  0: ['sendrom-dismorfoloji-kromozom'],
  1: ['sendrom-dismorfoloji-kromozom'],
  2: ['sendrom-cinsiyet-gelisim'],
  3: ['sendrom-kanser-yatkinlik', 'kanser-ilac-tedavileri', 'kanser-prenatal-belirtecler'],
  4: ['kanser-prenatal-belirtecler'],
};

const ASAMA_TABLO_HARITASI: Record<string, string[]> = {
  'g07-01': ['gt-anomali-mekanizma'],
  'g07-02': ['gt-dismorfik-mikrodelesyon'],
  'g07-03': ['gt-dismorfik-mikrodelesyon'],
  'g07-04': ['gt-trizomi-gonozom'],
  'g07-05': ['gt-gonad-genler'],
  'g07-06': ['gt-cgb-ayirici'],
  'g07-07': ['gt-rcc-sendrom', 'gt-meme-over-endometriyum-sendrom'],
  'g07-08': ['gt-kanser-hedef-ilac'],
  'g07-09': ['gt-rcc-endometriyum-ilac'],
  'g07-10': ['gt-kanser-belirtecler'],
  'g07-11': ['gt-prenatal-pgt-belirtecler'],
};

const HIZ_SECENEKLERI = [0.75, 1, 1.15, 1.25, 1.5, 1.75, 2];

/** Markdown **kalın** ifadeleri React düğümüne çevirir */
function RichText({ text }: { text: string }) {
  const parts = String(text || '').split(/(\*\*[^*]+\*\*)/g);
  return (
    <>
      {parts.map((p, i) =>
        p.startsWith('**') && p.endsWith('**') ? (
          <strong key={i} className="gcu-bold-term">
            {p.slice(2, -2)}
          </strong>
        ) : (
          <React.Fragment key={i}>{p}</React.Fragment>
        ),
      )}
    </>
  );
}

interface GenetikCheckUpProps {
  onBack?: () => void;
}

export const GenetikCheckUp: React.FC<GenetikCheckUpProps> = ({ onBack }) => {
  const [aktifBolum, setAktifBolum] = useState<GenetikBolumId | 'tumu'>('tumu');
  const [aktifSekme, setAktifSekme] = useState<SekmeTipi>('anlatici');
  const [soruFiltre, setSoruFiltre] = useState<SoruFiltreTipi>('hepsi');
  const [arama, setArama] = useState('');

  // Aşama Aşama Sesli Ders Anlatıcısı Durumu
  const [adimIdx, setAdimIdx] = useState<number>(() => {
    try {
      const saved = Number(localStorage.getItem('medsoru_genetik_anlatici_adim_v1'));
      if (!Number.isNaN(saved) && saved >= 0 && saved < g07.noktalar.length) return saved;
    } catch {}
    return 0;
  });
  const [tamamlananAdimlar, setTamamlananAdimlar] = useState<Record<string, boolean>>(() => {
    try {
      const raw = localStorage.getItem('medsoru_genetik_anlatici_tamam_v1');
      return raw ? JSON.parse(raw) : {};
    } catch {
      return {};
    }
  });
  const [asistanSoruSecim, setAsistanSoruSecim] = useState<Record<string, string>>(() => {
    try {
      const raw = localStorage.getItem('medsoru_genetik_anlatici_soru_v1');
      return raw ? JSON.parse(raw) : {};
    } catch {
      return {};
    }
  });
  const [yardimAcikSoru, setYardimAcikSoru] = useState<Record<string, boolean>>({});
  const [aktifKlipId, setAktifKlipId] = useState<string | null>(null);
  const [caliyor, setCaliyor] = useState(false);
  const [aktifCumleIdx, setAktifCumleIdx] = useState<number>(-1);
  const [hiz, setHiz] = useState<number>(1);
  const [otomatikIlerle, setOtomatikIlerle] = useState<boolean>(true);
  const [ekTabloAcik, setEkTabloAcik] = useState<boolean>(true);

  // Tam ekran PatolojiAsistan modalı
  const [tamEkranKod, setTamEkranKod] = useState<string | null>(null);

  // PDF İndirme Modalı ve Durumu
  const [pdfMenuAcik, setPdfMenuAcik] = useState(false);
  const [pdfYukleniyor, setPdfYukleniyor] = useState<GenetikPdfMod | null>(null);

  // Soru-Cevap ve tüm soru bankası durumları
  const [acikCevaplar, setAcikCevaplar] = useState<Record<string, boolean>>({});
  const [secilenSiklar, setSecilenSiklar] = useState<Record<string, 'A' | 'B' | 'C' | 'D' | 'E'>>(() => {
    try {
      const raw = localStorage.getItem('medsoru_genetik_checkup_answers_v1');
      return raw ? JSON.parse(raw) : {};
    } catch {
      return {};
    }
  });

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const pdfRef = useRef<HTMLDivElement | null>(null);
  const asamaRef = useRef<HTMLElement | null>(null);
  const ilkAdimRef = useRef(true);

  // PDF menüsü dışına tıklanınca ya da Esc ile kapanır
  useEffect(() => {
    if (!pdfMenuAcik) return;
    const kapat = (e: MouseEvent) => {
      if (pdfRef.current && !pdfRef.current.contains(e.target as Node)) setPdfMenuAcik(false);
    };
    const tus = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setPdfMenuAcik(false);
    };
    document.addEventListener('mousedown', kapat);
    document.addEventListener('keydown', tus);
    return () => {
      document.removeEventListener('mousedown', kapat);
      document.removeEventListener('keydown', tus);
    };
  }, [pdfMenuAcik]);

  const aktifNokta = g07.noktalar[adimIdx] || g07.noktalar[0];
  const aktifAnlaticiBolum = g07.bolumler[aktifNokta.bolum] || g07.bolumler[0];
  const aktifBolumKeys = BOLUM_HARITASI[aktifNokta.bolum] || ['sendrom-dismorfoloji-kromozom'];

  useEffect(() => {
    try {
      localStorage.setItem('medsoru_genetik_anlatici_adim_v1', String(adimIdx));
    } catch {}
    // Aşama değişince kartın başı görünmüyorsa oraya kaydır (ilk açılışta değil)
    if (ilkAdimRef.current) {
      ilkAdimRef.current = false;
      return;
    }
    const el = asamaRef.current;
    if (el && el.getBoundingClientRect().top < 0) {
      const azalt = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
      el.scrollIntoView({ behavior: azalt ? 'auto' : 'smooth', block: 'start' });
    }
  }, [adimIdx]);

  useEffect(() => {
    try {
      localStorage.setItem('medsoru_genetik_anlatici_tamam_v1', JSON.stringify(tamamlananAdimlar));
    } catch {}
  }, [tamamlananAdimlar]);

  useEffect(() => {
    try {
      localStorage.setItem('medsoru_genetik_anlatici_soru_v1', JSON.stringify(asistanSoruSecim));
    } catch {}
  }, [asistanSoruSecim]);

  useEffect(() => {
    try {
      localStorage.setItem('medsoru_genetik_checkup_answers_v1', JSON.stringify(secilenSiklar));
    } catch {}
  }, [secilenSiklar]);

  const sesDurdur = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.onended = null;
      audioRef.current.ontimeupdate = null;
    }
    setCaliyor(false);
    setAktifCumleIdx(-1);
  }, []);

  useEffect(() => {
    return () => sesDurdur();
  }, [sesDurdur]);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.playbackRate = hiz;
    }
  }, [hiz]);

  const klipCal = useCallback(
    (klipId: string, baslangicCumle = 0, bittiginde?: () => void) => {
      const k = g07.klip[klipId];
      if (!k) return;

      // Aynı klip çalıyorsa ve başlangıç cümlesi belirtilmemişse duraklat/devam et
      if (aktifKlipId === klipId && audioRef.current && baslangicCumle === 0 && !bittiginde) {
        if (caliyor) {
          audioRef.current.pause();
          setCaliyor(false);
          return;
        } else {
          audioRef.current.playbackRate = hiz;
          audioRef.current.play().catch(() => {});
          setCaliyor(true);
          return;
        }
      }

      sesDurdur();
      const url = `${getCustomApiUrl()}/api/patoloji-asistan/ses/g07/${klipId}.mp3?v=${k.v}`;
      const audio = new Audio(url);
      audio.playbackRate = hiz;
      audioRef.current = audio;
      setAktifKlipId(klipId);

      if (baslangicCumle > 0 && k.zaman[baslangicCumle]) {
        audio.currentTime = Math.max(0, k.zaman[baslangicCumle][0] - 0.05);
      }

      audio.ontimeupdate = () => {
        const t = audio.currentTime;
        const idx = k.zaman.findIndex(([b, s]) => t >= b - 0.08 && t <= s + 0.12);
        if (idx !== -1) setAktifCumleIdx(idx);
      };

      audio.onended = () => {
        setCaliyor(false);
        setAktifCumleIdx(-1);
        if (bittiginde) bittiginde();
      };

      audio.onerror = () => {
        setCaliyor(false);
        setAktifCumleIdx(-1);
      };

      audio
        .play()
        .then(() => {
          setCaliyor(true);
          setAktifCumleIdx(baslangicCumle);
        })
        .catch(() => {
          setCaliyor(false);
        });
    },
    [aktifKlipId, caliyor, hiz, sesDurdur],
  );

  // Aşamayı sesli başlat (cümleler bittiğinde otomatik ilerle açıksa ilk soruyu okur)
  const asamayiSesliAnlat = useCallback(
    (hedefIdx = adimIdx, baslangicCumle = 0) => {
      const nk = g07.noktalar[hedefIdx];
      if (!nk) return;
      const klipId = `a-${nk.id}`;
      klipCal(klipId, baslangicCumle, () => {
        setTamamlananAdimlar((prev) => ({ ...prev, [nk.id]: true }));
        if (otomatikIlerle && nk.sorular.length > 0) {
          const ilkSoru = nk.sorular[0];
          klipCal(`q-${ilkSoru.k}`);
        }
      });
    },
    [adimIdx, klipCal, otomatikIlerle],
  );

  const adimDegistir = useCallback(
    (yeniIdx: number, otomatikOku = false) => {
      const clamped = Math.max(0, Math.min(g07.noktalar.length - 1, yeniIdx));
      sesDurdur();
      setAktifKlipId(null);
      setAdimIdx(clamped);
      if (otomatikOku) {
        setTimeout(() => {
          const nk = g07.noktalar[clamped];
          if (nk) klipCal(`a-${nk.id}`);
        }, 80);
      }
    },
    [klipCal, sesDurdur],
  );

  const asistanSoruSikSec = useCallback(
    (soru: AsistanSoru, harf: string) => {
      setAsistanSoruSecim((prev) => ({ ...prev, [soru.k]: harf }));
      if (harf === soru.dogru) {
        klipCal(`d-${soru.k}`);
      } else {
        klipCal(`y-${soru.k}-${harf}`);
      }
    },
    [klipCal],
  );

  const yardimToggleVeOku = useCallback(
    (soru: AsistanSoru) => {
      setYardimAcikSoru((prev) => ({ ...prev, [soru.k]: true }));
      klipCal(`h-${soru.k}`);
    },
    [klipCal],
  );

  const handlePdfIndir = useCallback(async (mod: GenetikPdfMod) => {
    setPdfYukleniyor(mod);
    try {
      await genetikCheckupPdfIndir(mod);
    } finally {
      setPdfYukleniyor(null);
      setPdfMenuAcik(false);
    }
  }, []);

  const aramaKucuk = arama.trim().toLowerCase();

  const filtrelenmisTablolar = useMemo(() => {
    return GENETIK_TABLOLAR.filter((t) => {
      if (aktifBolum !== 'tumu' && t.bolum !== aktifBolum) return false;
      if (!aramaKucuk) return true;
      const metin = [t.baslik, t.aciklama, ...t.sutunlar, ...t.satirlar.flat()].join(' ').toLowerCase();
      return metin.includes(aramaKucuk);
    });
  }, [aktifBolum, aramaKucuk]);

  const filtrelenmisSpotlar = useMemo(() => {
    return GENETIK_SPOTLAR.filter((s) => {
      if (aktifBolum !== 'tumu' && s.bolum !== aktifBolum) return false;
      if (!aramaKucuk) return true;
      return s.cumle.toLowerCase().includes(aramaKucuk) || s.etiket.toLowerCase().includes(aramaKucuk);
    });
  }, [aktifBolum, aramaKucuk]);

  const filtrelenmisSoruCevaplar = useMemo(() => {
    return GENETIK_SORU_CEVAPLAR.filter((sc) => {
      if (aktifBolum !== 'tumu' && sc.bolum !== aktifBolum) return false;
      if (!aramaKucuk) return true;
      return (
        sc.soru.toLowerCase().includes(aramaKucuk) ||
        sc.cevap.toLowerCase().includes(aramaKucuk) ||
        (sc.ipucu && sc.ipucu.toLowerCase().includes(aramaKucuk))
      );
    });
  }, [aktifBolum, aramaKucuk]);

  const filtrelenmisSorular = useMemo(() => {
    return GENETIK_SORULAR.filter((q) => {
      if (aktifBolum !== 'tumu' && q.bolum !== aktifBolum) return false;
      if (soruFiltre !== 'hepsi' && q.tur !== soruFiltre) return false;
      if (!aramaKucuk) return true;
      const metin = [
        q.kok,
        q.kalipEtiketi,
        q.aciklama,
        q.spotCikarim,
        ...Object.values(q.secenekler),
      ]
        .join(' ')
        .toLowerCase();
      return metin.includes(aramaKucuk);
    });
  }, [aktifBolum, soruFiltre, aramaKucuk]);

  // Aktif aşamanın bağlı olduğu bölümün tabloları ve spotları
  const asamaTablolari = useMemo(() => {
    const hedefTabloIdler = ASAMA_TABLO_HARITASI[aktifNokta.id];
    if (hedefTabloIdler && hedefTabloIdler.length > 0) {
      return GENETIK_TABLOLAR.filter((t) => hedefTabloIdler.includes(t.id));
    }
    return GENETIK_TABLOLAR.filter((t) => aktifBolumKeys.includes(t.bolum));
  }, [aktifNokta.id, aktifBolumKeys]);

  const asamaSpotlari = useMemo(
    () => GENETIK_SPOTLAR.filter((s) => aktifBolumKeys.includes(s.bolum)),
    [aktifBolumKeys],
  );

  const istatistik = useMemo(() => {
    const toplamCikmis = GENETIK_SORULAR.filter((q) => q.tur === 'cikmis').length;
    const toplamOrnek = GENETIK_SORULAR.filter((q) => q.tur === 'ornek').length;
    const cozulen = Object.keys(secilenSiklar).length;
    const dogruSayisi = GENETIK_SORULAR.filter((q) => secilenSiklar[q.id] === q.dogru).length;
    const tamamAdim = Object.keys(tamamlananAdimlar).length;
    return {
      toplamSpot: GENETIK_SPOTLAR.length,
      toplamSoruCevap: GENETIK_SORU_CEVAPLAR.length,
      toplamTablo: GENETIK_TABLOLAR.length,
      toplamCikmis,
      toplamOrnek,
      toplamSoru: GENETIK_SORULAR.length,
      cozulen,
      dogruSayisi,
      tamamAdim,
    };
  }, [secilenSiklar, tamamlananAdimlar]);

  const asistanToplam = useMemo(() => g07.noktalar.reduce((x, n) => x + n.sorular.length, 0), []);
  const asistanDogru = useMemo(
    () => g07.noktalar.reduce((x, n) => x + n.sorular.filter((q) => asistanSoruSecim[q.k] === q.dogru).length, 0),
    [asistanSoruSecim],
  );

  const toggleCevap = (id: string) => {
    setAcikCevaplar((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const tumCevaplariAcKapat = (ac: boolean) => {
    const next: Record<string, boolean> = {};
    if (ac) {
      filtrelenmisSoruCevaplar.forEach((sc) => {
        next[sc.id] = true;
      });
    }
    setAcikCevaplar(next);
  };

  const sikSec = (soruId: string, sik: 'A' | 'B' | 'C' | 'D' | 'E') => {
    setSecilenSiklar((prev) => ({ ...prev, [soruId]: sik }));
  };

  const cevaplariSifirla = () => {
    setSecilenSiklar({});
    setAsistanSoruSecim({});
    setTamamlananAdimlar({});
  };

  const harfler: ('A' | 'B' | 'C' | 'D' | 'E')[] = ['A', 'B', 'C', 'D', 'E'];

  const sekmeler: { id: SekmeTipi; ad: string; ikon: React.ReactNode; say?: number }[] = [
    { id: 'anlatici', ad: 'Sesli ders', ikon: <Volume2 /> },
    { id: 'tablolar', ad: 'Tablolar', ikon: <FileSpreadsheet />, say: filtrelenmisTablolar.length },
    { id: 'spotlar', ad: 'Spotlar', ikon: <Zap />, say: filtrelenmisSpotlar.length },
    { id: 'soru_cevap', ad: 'Soru–cevap', ikon: <HelpCircle />, say: filtrelenmisSoruCevaplar.length },
    { id: 'sorular', ad: 'Sorular', ikon: <BookOpen />, say: filtrelenmisSorular.length },
    { id: 'hepsi', ad: 'Hepsi', ikon: <Layers /> },
  ];

  const tabloKart = (t: (typeof GENETIK_TABLOLAR)[number]) => (
    <article key={t.id} className="gcu-kart">
      <header className="gcu-kart-bas">
        <span className="gcu-ust">
          {KALIP_META[t.kalip].kisa} · Slayt {t.k.join(', ')}
        </span>
        <h3>{t.baslik}</h3>
      </header>
      <div className="gcu-tablo-kap">
        <table className="gcu-tablo">
          <thead>
            <tr>
              {t.sutunlar.map((col, i) => (
                <th key={i}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {t.satirlar.map((row, r) => (
              <tr key={r}>
                {row.map((cell, c) =>
                  c === 0 ? (
                    <th key={c} scope="row">
                      {cell}
                    </th>
                  ) : (
                    <td key={c} data-l={t.sutunlar[c]}>
                      {cell}
                    </td>
                  ),
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </article>
  );

  const spotListe = (liste: typeof GENETIK_SPOTLAR) => (
    <ol className="gcu-spotlar">
      {liste.map((s, i) => (
        <li key={s.id}>
          <span className="gcu-no">{i + 1}</span>
          <div>
            <p>
              <RichText text={s.cumle} />
            </p>
            <small>
              {s.etiket}
              {s.cikmisYil && <b> · Çıkmış {s.cikmisYil}</b>}
            </small>
          </div>
        </li>
      ))}
    </ol>
  );

  const siklar = (
    secenekler: Record<string, string>,
    dogru: string,
    secilen: string | undefined,
    sec: (h: 'A' | 'B' | 'C' | 'D' | 'E') => void,
    aciklama: (h: string) => string | undefined,
    aciklamaGoster: boolean,
    okunanIdx = -1,
  ) => (
    <div className="gcu-siklar">
      {harfler.map((h, hi) => {
        const metin = secenekler[h];
        if (!metin) return null;
        const cozuldu = !!secilen;
        const durum = cozuldu ? (h === dogru ? 'is-dogru' : h === secilen ? 'is-yanlis' : '') : '';
        const not = aciklamaGoster ? aciklama(h) : undefined;
        return (
          <div key={h} className="gcu-sik">
            <button
              type="button"
              className={`gcu-sik-btn ${durum} ${okunanIdx === hi ? 'is-okunuyor' : ''}`}
              onClick={() => sec(h)}
              aria-pressed={secilen === h}
            >
              <span className="gcu-sik-harf">{h}</span>
              <span className="gcu-sik-metin">{metin}</span>
              {durum === 'is-dogru' && <CheckCircle2 className="gcu-sik-ikon" />}
              {durum === 'is-yanlis' && <XCircle className="gcu-sik-ikon" />}
            </button>
            {not && (
              <p className={`gcu-sik-not ${h === dogru && cozuldu ? 'is-dogru' : ''} ${okunanIdx === hi ? 'is-okunuyor' : ''}`}>
                <RichText text={not} />
              </p>
            )}
          </div>
        );
      })}
    </div>
  );

  const anlatimCaliyor = caliyor && aktifKlipId === `a-${aktifNokta.id}`;

  return (
    <div className="gcu">
      {tamEkranKod && (
        <PatolojiAsistan
          kod={tamEkranKod}
          onClose={() => setTamEkranKod(null)}
          onDersDegis={(yeniKod) => setTamEkranKod(yeniKod)}
        />
      )}

      {/* BAŞLIK */}
      <header className="gcu-bas">
        {onBack && (
          <button type="button" className="gcu-geri" onClick={onBack} aria-label="Geri dön">
            <ArrowLeft />
          </button>
        )}
        <span className="gcu-ic" aria-hidden>
          <Dna />
        </span>
        <div className="gcu-bas-t">
          <span className="gcu-ust">Kurul 1 · Tıbbi Biyoloji ve Genetik</span>
          <h1>Genetik sınav kalıbı</h1>
          <p>
            Sorular üç kalıptan gelir: <b>bulgudan sendroma</b>, <b>kanserde hedef ilaç</b> ve{' '}
            <b>kanser ile prenatal belirteçler</b>. 11 aşamalı sesli dersle ilerle, sonra tablo, spot ve sorularla pekiştir.
          </p>
        </div>
        <div className="gcu-bas-arac">
          <button
            type="button"
            className="gcu-btn"
            onClick={() => {
              sesDurdur();
              setTamEkranKod('g07');
            }}
          >
            <Maximize2 />
            <span>Tam ekran asistan</span>
          </button>
          <div className="gcu-pdf" ref={pdfRef}>
            <button
              type="button"
              className="gcu-btn"
              onClick={() => setPdfMenuAcik((v) => !v)}
              disabled={!!pdfYukleniyor}
              aria-expanded={pdfMenuAcik}
            >
              <Download />
              <span>{pdfYukleniyor ? 'Hazırlanıyor…' : 'PDF'}</span>
              <ChevronDown />
            </button>
            {pdfMenuAcik && (
              <div className="gcu-pdf-menu" role="menu">
                {GENETIK_PDF_MODLAR.map((m) => (
                  <button
                    key={m.id}
                    type="button"
                    role="menuitem"
                    disabled={!!pdfYukleniyor}
                    onClick={() => handlePdfIndir(m.id)}
                  >
                    <FileText />
                    <span>
                      <b>{m.baslik}</b>
                      <small>{m.aciklama}</small>
                    </span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </header>

      {/* İLERLEME */}
      <div className="gcu-ilerleme">
        <div className="gcu-ilerleme-oge">
          <span>Sesli ders</span>
          <b className="gcu-mono">
            {istatistik.tamamAdim}/{g07.noktalar.length} aşama
          </b>
          <i style={{ ['--p' as string]: `${(istatistik.tamamAdim / g07.noktalar.length) * 100}%` }} />
        </div>
        <div className="gcu-ilerleme-oge">
          <span>Ders soruları</span>
          <b className="gcu-mono">
            {asistanDogru}/{asistanToplam} doğru
          </b>
          <i style={{ ['--p' as string]: `${(asistanDogru / Math.max(1, asistanToplam)) * 100}%` }} />
        </div>
        <div className="gcu-ilerleme-oge">
          <span>Soru bankası</span>
          <b className="gcu-mono">
            {istatistik.dogruSayisi}/{istatistik.toplamSoru} doğru
          </b>
          <i style={{ ['--p' as string]: `${(istatistik.dogruSayisi / Math.max(1, istatistik.toplamSoru)) * 100}%` }} />
        </div>
        {(istatistik.cozulen > 0 || istatistik.tamamAdim > 0) && (
          <button type="button" className="gcu-metin-btn" onClick={cevaplariSifirla}>
            <RotateCcw />
            Sıfırla
          </button>
        )}
      </div>

      {/* SEKMELER */}
      <nav className="gcu-sekme" aria-label="Bölümler">
        {sekmeler.map((s) => (
          <button
            key={s.id}
            type="button"
            className={aktifSekme === s.id ? 'is-on' : ''}
            aria-current={aktifSekme === s.id ? 'page' : undefined}
            onClick={() => setAktifSekme(s.id)}
          >
            {s.ikon}
            <span>{s.ad}</span>
            {s.say !== undefined && <em className="gcu-mono">{s.say}</em>}
          </button>
        ))}
      </nav>

      {aktifSekme !== 'anlatici' && (
        <div className="gcu-arac">
          <label className="gcu-ara">
            <Search />
            <input
              type="search"
              value={arama}
              onChange={(e) => setArama(e.target.value)}
              placeholder="Sendrom, gen, ilaç, belirteç ara (Turner, FGFR3, olaparib, AFP…)"
            />
            {arama && (
              <button type="button" className="gcu-ara-sil" onClick={() => setArama('')} aria-label="Aramayı temizle">
                <XCircle />
              </button>
            )}
          </label>
          <div className="gcu-cipler" role="group" aria-label="Konu bölümü">
            <button
              type="button"
              className={aktifBolum === 'tumu' ? 'is-on' : ''}
              onClick={() => setAktifBolum('tumu')}
            >
              Tümü
            </button>
            {GENETIK_BOLUMLER.map((b) => (
              <button
                key={b.id}
                type="button"
                className={aktifBolum === b.id ? 'is-on' : ''}
                onClick={() => setAktifBolum(b.id)}
                title={b.kisa}
              >
                {b.ad}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* 1. AŞAMA AŞAMA SESLİ DERS */}
      {aktifSekme === 'anlatici' && (
        <div className="gcu-ders">
          <nav className="gcu-asamalar" aria-label="Ders aşamaları">
            {g07.bolumler.map((b, bi) => (
              <div key={bi} className="gcu-asama-grup">
                <span className="gcu-asama-grup-ad">
                  <span className="gcu-mono">{bi + 1}</span> {b.baslik}
                </span>
                {g07.noktalar.map((nk, idx) => {
                  if (nk.bolum !== bi) return null;
                  const isCurrent = idx === adimIdx;
                  const isDone =
                    !!tamamlananAdimlar[nk.id] || nk.sorular.every((q) => asistanSoruSecim[q.k] === q.dogru);
                  return (
                    <button
                      key={nk.id}
                      type="button"
                      className={`gcu-asama ${isCurrent ? 'is-on' : ''} ${isDone ? 'is-ok' : ''}`}
                      aria-current={isCurrent ? 'step' : undefined}
                      onClick={() => adimDegistir(idx, false)}
                    >
                      <span className="gcu-asama-no gcu-mono">{isDone ? <Check /> : idx + 1}</span>
                      <span className="gcu-asama-ad">{nk.baslik}</span>
                    </button>
                  );
                })}
              </div>
            ))}
          </nav>

          <article className="gcu-asama-kart" ref={asamaRef}>
            <header className="gcu-asama-bas">
              <span className="gcu-ust">
                Bölüm {aktifNokta.bolum + 1} · {aktifAnlaticiBolum.baslik}
              </span>
              <h2>
                <span className="gcu-mono">{adimIdx + 1}.</span> {aktifNokta.baslik}
              </h2>
              <p>{aktifAnlaticiBolum.neden}</p>
              <div className="gcu-onem" title="Sınavda çıkma önemi">
                <Target />
                <span>Sınav önemi</span>
                <b className="gcu-mono">{aktifNokta.puan}</b>
                <i style={{ ['--p' as string]: `${aktifNokta.puan}%` }} />
              </div>
            </header>

            {/* oynatıcı */}
            <div className="gcu-oynatici">
              <button
                type="button"
                className={`gcu-oynat ${anlatimCaliyor ? 'is-caliyor' : ''}`}
                onClick={() => asamayiSesliAnlat(adimIdx)}
              >
                {anlatimCaliyor ? <Pause /> : <Play />}
                <span>{anlatimCaliyor ? 'Duraklat' : aktifKlipId === `a-${aktifNokta.id}` ? 'Devam et' : 'Aşamayı dinle'}</span>
              </button>
              <button
                type="button"
                className="gcu-btn"
                onClick={() => klipCal(`b-${aktifNokta.bolum + 1}`)}
                title="Bölüm girişini sesli dinle"
              >
                <Volume2 />
                <span>Bölüm girişi</span>
              </button>
              {caliyor && !anlatimCaliyor && (
                <button type="button" className="gcu-btn" onClick={sesDurdur} title="Sesi durdur">
                  <Pause />
                  <span>Durdur</span>
                </button>
              )}
              <span className="gcu-oynatici-bosluk" />
              <label className="gcu-hiz">
                <span>Hız</span>
                <select value={hiz} onChange={(e) => setHiz(Number(e.target.value))}>
                  {HIZ_SECENEKLERI.map((s) => (
                    <option key={s} value={s}>
                      {s}×
                    </option>
                  ))}
                </select>
              </label>
              <label className="gcu-anahtar">
                <input
                  type="checkbox"
                  checked={otomatikIlerle}
                  onChange={(e) => setOtomatikIlerle(e.target.checked)}
                />
                <span>Sonra soruyu oku</span>
              </label>
            </div>

            {/* anlatım */}
            <ol className="gcu-anlatim" aria-label="Doktor anlatımı">
              {aktifNokta.cumleler.map((cm, ci) => {
                const okunuyor = anlatimCaliyor && aktifCumleIdx === ci;
                return (
                  <li key={ci}>
                    <button
                      type="button"
                      className={okunuyor ? 'is-okunuyor' : ''}
                      onClick={() => asamayiSesliAnlat(adimIdx, ci)}
                      title="Buradan dinle"
                    >
                      <RichText text={cm} />
                    </button>
                  </li>
                );
              })}
            </ol>

            <aside className="gcu-kural">
              <span className="gcu-ust">
                <Zap /> Sınavda aranan kural
              </span>
              <p>
                <RichText text={aktifNokta.bilgi} />
              </p>
            </aside>

            {/* aşama soruları */}
            {aktifNokta.sorular.length > 0 && (
              <section className="gcu-asama-sorular">
                <h3>
                  Bu aşamanın soruları <span className="gcu-mono">{aktifNokta.sorular.length}</span>
                </h3>
                {aktifNokta.sorular.map((q, qi) => {
                  const secilen = asistanSoruSecim[q.k];
                  const cozuldu = !!secilen;
                  const yardimAcik = !!yardimAcikSoru[q.k];
                  const yardimOkunuyor = caliyor && aktifKlipId === `h-${q.k}`;
                  return (
                    <article
                      key={q.k}
                      className={`gcu-soru ${cozuldu ? (secilen === q.dogru ? 'is-dogru' : 'is-yanlis') : ''}`}
                    >
                      <div className="gcu-soru-bas">
                        <span className="gcu-mono gcu-soru-no">{qi + 1}</span>
                        <span className={`gcu-tur ${q.tur}`}>
                          {q.tur === 'cikmis' ? `Çıkmış · ${q.sinav || 'Kurul 1'}` : 'Örnek soru'}
                        </span>
                        <span className="gcu-oynatici-bosluk" />
                        <button
                          type="button"
                          className={`gcu-metin-btn ${caliyor && aktifKlipId === `q-${q.k}` ? 'is-on' : ''}`}
                          onClick={() => klipCal(`q-${q.k}`)}
                        >
                          <Volume2 />
                          Oku
                        </button>
                        <button
                          type="button"
                          className={`gcu-metin-btn ${yardimOkunuyor ? 'is-on' : ''}`}
                          onClick={() => yardimToggleVeOku(q)}
                        >
                          <LifeBuoy />
                          Yardım al
                        </button>
                      </div>
                      <p className="gcu-soru-kok">{q.kok}</p>
                      {siklar(
                        q.secenekler,
                        q.dogru,
                        secilen,
                        (h) => asistanSoruSikSec(q, h),
                        (h) => q.yardim[h],
                        yardimAcik || cozuldu,
                        yardimOkunuyor ? aktifCumleIdx : -1,
                      )}
                      {cozuldu && (
                        <p className="gcu-cozum">
                          <Sparkles />
                          <span>
                            <RichText text={secilen === q.dogru ? q.dogruMetin : q.yanlis[secilen] || q.dogruMetin} />
                          </span>
                        </p>
                      )}
                    </article>
                  );
                })}
              </section>
            )}

            {/* başvuru: tablo + spot */}
            <details className="gcu-basvuru" open={ekTabloAcik} onToggle={(e) => setEkTabloAcik((e.target as HTMLDetailsElement).open)}>
              <summary>
                <FileSpreadsheet />
                <span>
                  İlgili tablolar <em className="gcu-mono">{asamaTablolari.length}</em> ve spotlar{' '}
                  <em className="gcu-mono">{asamaSpotlari.length}</em>
                </span>
                <ChevronDown className="gcu-basvuru-ok" />
              </summary>
              <div className="gcu-basvuru-ic">
                {asamaTablolari.map(tabloKart)}
                {asamaSpotlari.length > 0 && spotListe(asamaSpotlari)}
              </div>
            </details>

            <footer className="gcu-gezinti">
              <button
                type="button"
                className="gcu-btn"
                disabled={adimIdx === 0}
                onClick={() => adimDegistir(adimIdx - 1, false)}
              >
                <ChevronLeft />
                <span>Önceki</span>
              </button>
              <span className="gcu-mono gcu-gezinti-say">
                {adimIdx + 1} / {g07.noktalar.length}
              </span>
              {adimIdx < g07.noktalar.length - 1 ? (
                <button
                  type="button"
                  className="gcu-btn gcu-btn-ana"
                  onClick={() => {
                    setTamamlananAdimlar((prev) => ({ ...prev, [aktifNokta.id]: true }));
                    adimDegistir(adimIdx + 1, otomatikIlerle);
                  }}
                >
                  <span>Tamamla, sonraki aşama</span>
                  <ChevronRight />
                </button>
              ) : (
                <button
                  type="button"
                  className="gcu-btn gcu-btn-ana"
                  onClick={() => {
                    setTamamlananAdimlar((prev) => ({ ...prev, [aktifNokta.id]: true }));
                    setAktifSekme('sorular');
                  }}
                >
                  <span>Dersi bitir, sorulara geç</span>
                  <ChevronRight />
                </button>
              )}
            </footer>
          </article>

          {/* diğer genetik dersleri */}
          <section className="gcu-dersler">
            <h3>Genetik amfi derslerinin sesli asistanları</h3>
            <div className="gcu-dersler-izgara">
              {DIZIN_DERSLER.map((d) => (
                <button
                  key={d.kod}
                  type="button"
                  className={d.kod === 'g07' ? 'is-on' : ''}
                  onClick={() => {
                    sesDurdur();
                    setTamEkranKod(d.kod);
                  }}
                >
                  <span className="gcu-ust gcu-mono">{d.kod.toUpperCase()}</span>
                  <b>{d.baslik}</b>
                  <small className="gcu-mono">
                    {d.adim} adım · {d.soru} soru · {Math.round(d.sure / 60)} dk
                  </small>
                </button>
              ))}
            </div>
          </section>
        </div>
      )}

      {/* 2. TABLOLAR */}
      {(aktifSekme === 'hepsi' || aktifSekme === 'tablolar') && filtrelenmisTablolar.length > 0 && (
        <section className="gcu-bolum">
          <h2>
            Karşılaştırma tabloları <span className="gcu-mono">{filtrelenmisTablolar.length}</span>
          </h2>
          {filtrelenmisTablolar.map(tabloKart)}
        </section>
      )}

      {/* 3. SPOTLAR */}
      {(aktifSekme === 'hepsi' || aktifSekme === 'spotlar') && filtrelenmisSpotlar.length > 0 && (
        <section className="gcu-bolum">
          <h2>
            Tek satırlık spotlar <span className="gcu-mono">{filtrelenmisSpotlar.length}</span>
          </h2>
          <div className="gcu-kart">{spotListe(filtrelenmisSpotlar)}</div>
        </section>
      )}

      {/* 4. SORU – CEVAP */}
      {(aktifSekme === 'hepsi' || aktifSekme === 'soru_cevap') && filtrelenmisSoruCevaplar.length > 0 && (
        <section className="gcu-bolum">
          <div className="gcu-bolum-bas">
            <h2>
              Soru–cevap kartları <span className="gcu-mono">{filtrelenmisSoruCevaplar.length}</span>
            </h2>
            <div className="gcu-cipler">
              <button type="button" onClick={() => tumCevaplariAcKapat(true)}>
                Tümünü aç
              </button>
              <button type="button" onClick={() => tumCevaplariAcKapat(false)}>
                Tümünü kapat
              </button>
            </div>
          </div>
          <div className="gcu-qa-izgara">
            {filtrelenmisSoruCevaplar.map((sc) => {
              const acik = !!acikCevaplar[sc.id];
              return (
                <button
                  key={sc.id}
                  type="button"
                  className={`gcu-qa ${acik ? 'is-acik' : ''}`}
                  aria-expanded={acik}
                  onClick={() => toggleCevap(sc.id)}
                >
                  <span className="gcu-ust">{sc.odak}</span>
                  <b>{sc.soru}</b>
                  {acik ? (
                    <span className="gcu-qa-cevap">
                      <RichText text={sc.cevap} />
                      {sc.ipucu && <small>{sc.ipucu}</small>}
                    </span>
                  ) : (
                    <span className="gcu-qa-ac">Cevabı göster</span>
                  )}
                </button>
              );
            })}
          </div>
        </section>
      )}

      {/* 5. ÇIKMIŞ + ÖRNEK SORULAR */}
      {(aktifSekme === 'hepsi' || aktifSekme === 'sorular') && (
        <section className="gcu-bolum">
          <div className="gcu-bolum-bas">
            <h2>
              Çıkmış ve örnek sorular <span className="gcu-mono">{filtrelenmisSorular.length}</span>
            </h2>
            <div className="gcu-cipler" role="group" aria-label="Soru türü">
              {(
                [
                  ['hepsi', `Tümü ${GENETIK_SORULAR.length}`],
                  ['cikmis', `Çıkmış ${istatistik.toplamCikmis}`],
                  ['ornek', `Örnek ${istatistik.toplamOrnek}`],
                ] as [SoruFiltreTipi, string][]
              ).map(([id, ad]) => (
                <button key={id} type="button" className={soruFiltre === id ? 'is-on' : ''} onClick={() => setSoruFiltre(id)}>
                  {ad}
                </button>
              ))}
            </div>
          </div>
          {filtrelenmisSorular.length === 0 && <p className="gcu-bos">Bu filtreye uyan soru yok.</p>}
          {filtrelenmisSorular.map((q: GenetikZenginSoru, idx: number) => {
            const secilen = secilenSiklar[q.id];
            const cozuldu = !!secilen;
            return (
              <article
                key={q.id}
                className={`gcu-soru ${cozuldu ? (secilen === q.dogru ? 'is-dogru' : 'is-yanlis') : ''}`}
              >
                <div className="gcu-soru-bas">
                  <span className="gcu-mono gcu-soru-no">{idx + 1}</span>
                  <span className={`gcu-tur ${q.tur}`}>
                    {q.tur === 'cikmis' ? `Çıkmış · ${q.yil || 'Kurul 1'}` : 'Örnek soru'}
                  </span>
                  <span className="gcu-soru-etiket">{q.kalipEtiketi}</span>
                </div>
                <p className="gcu-soru-kok">{q.kok}</p>
                {siklar(q.secenekler, q.dogru, secilen, (h) => sikSec(q.id, h), (h) => q.sikAciklamalari?.[h as SecenekHarf], cozuldu)}
                {cozuldu && q.aciklama && (
                  <p className="gcu-cozum">
                    <Sparkles />
                    <span>{q.aciklama}</span>
                  </p>
                )}
              </article>
            );
          })}
        </section>
      )}

      {aktifSekme !== 'anlatici' &&
        aramaKucuk &&
        !filtrelenmisTablolar.length &&
        !filtrelenmisSpotlar.length &&
        !filtrelenmisSoruCevaplar.length &&
        !filtrelenmisSorular.length && <p className="gcu-bos">“{arama}” için sonuç bulunamadı.</p>}
    </div>
  );
};

export default GenetikCheckUp;
