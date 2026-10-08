import React, { useState, useEffect, useMemo } from 'react';
import { PageHeader } from './ui/PageHeader';
import { 
  Compass, 
  Search, 
  BookOpen, 
  Presentation, 
  CheckCircle2, 
  Archive, 
  Layers, 
  BookOpenText, 
  ChevronDown, 
  ChevronRight, 
  ExternalLink,
  GraduationCap,
  Sparkles,
  Target,
  FileText,
  Filter,
  Check,
  X
} from 'lucide-react';
import { SectionLoader } from './ui/Animations';
import { StemText } from './ui/StemText';
import { SourceText } from './ui/SourceText';
import { pathFor } from '../router';

interface KazanimItem {
  id: string;
  metin: string;
  slaytlar: Array<{ kaynak: string; sayfa: number; alinti?: string; deckId?: string }>;
  cikmisSorular: Array<{
    id: string;
    questionNumber?: number;
    stem: string;
    correctAnswer: string;
    options: Array<{ key: string; text: string }>;
    year: string;
    discipline: string;
    topic: string;
    explanation?: string;
  }>;
  ornekSorular: Array<{
    id: string;
    kazanimNo?: number;
    zorluk?: string;
    soru: string;
    secenekler: Record<string, string>;
    dogru: string;
    aciklama?: string;
  }>;
  sozlukTerimleri: Array<{
    term: string;
    definition: string;
    pearl?: string;
  }>;
  ozetler: string[];
}

interface KonuGroup {
  konu: string;
  kazanimlar: KazanimItem[];
}

interface DersGroup {
  ders: string;
  count: number;
  konular: KonuGroup[];
}

interface KurulData {
  kurul: number;
  name: string;
  totalCount: number;
  dersler: DersGroup[];
}

interface KurulIndexItem {
  kurul: number;
  name: string;
  totalCount: number;
  dersler: Array<{ ders: string; count: number }>;
}

const loaders: Record<number, () => Promise<{ default: any }>> = {
  1: () => import('../data/kazanimlar/k1.json'),
  2: () => import('../data/kazanimlar/k2.json'),
  3: () => import('../data/kazanimlar/k3.json'),
  4: () => import('../data/kazanimlar/k4.json'),
  5: () => import('../data/kazanimlar/k5.json'),
  6: () => import('../data/kazanimlar/k6.json'),
};

interface Props {
  onNavigateToLearn?: (deckId?: string, slideNumber?: number) => void;
  onNavigateToPastExams?: (query?: string) => void;
  onNavigateToOrnek?: () => void;
}

export const KazanimlarView: React.FC<Props> = ({
  onNavigateToLearn,
  onNavigateToPastExams,
  onNavigateToOrnek,
}) => {
  const [selectedKurul, setSelectedKurul] = useState<number>(1);
  const [selectedDers, setSelectedDers] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [kurulData, setKurulData] = useState<KurulData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Active resource expansion per kazanim id: 'none' | 'slayt' | 'ornek' | 'cikmis' | 'sozluk' | 'ozet'
  const [activeTabByKazanim, setActiveTabByKazanim] = useState<Record<string, string>>({});
  // Solved state for sample questions
  const [ornekAnswers, setOrnekAnswers] = useState<Record<string, string>>({});

  useEffect(() => {
    let alive = true;
    setLoading(true);
    setSelectedDers('all');
    const loader = loaders[selectedKurul];
    if (loader) {
      loader()
        .then((m) => {
          if (alive) {
            setKurulData(m ? (m.default || m) : null);
            setLoading(false);
          }
        })
        .catch(() => {
          if (alive) setLoading(false);
        });
    }
    return () => {
      alive = false;
    };
  }, [selectedKurul]);

  const dersList = useMemo(() => {
    if (!kurulData) return [];
    return kurulData.dersler.map((d) => ({ ders: d.ders, count: d.count }));
  }, [kurulData]);

  // Filtered dersler and konular
  const filteredDersler = useMemo(() => {
    if (!kurulData) return [];
    const q = searchQuery.trim().toLowerCase();

    return kurulData.dersler
      .filter((d) => selectedDers === 'all' || d.ders === selectedDers)
      .map((d) => {
        const filteredKonular = d.konular
          .map((k) => {
            const filteredKazanimlar = k.kazanimlar.filter((item) => {
              if (!q) return true;
              return (
                item.metin.toLowerCase().includes(q) ||
                k.konu.toLowerCase().includes(q) ||
                d.ders.toLowerCase().includes(q) ||
                item.sozlukTerimleri.some((s) => s.term.toLowerCase().includes(q))
              );
            });
            return {
              ...k,
              kazanimlar: filteredKazanimlar,
            };
          })
          .filter((k) => k.kazanimlar.length > 0);

        return {
          ...d,
          konular: filteredKonular,
          count: filteredKonular.reduce((acc, curr) => acc + curr.kazanimlar.length, 0),
        };
      })
      .filter((d) => d.konular.length > 0);
  }, [kurulData, selectedDers, searchQuery]);

  const totalFilteredCount = useMemo(() => {
    return filteredDersler.reduce((acc, curr) => acc + curr.count, 0);
  }, [filteredDersler]);

  const toggleTab = (kid: string, tab: string) => {
    setActiveTabByKazanim((prev) => ({
      ...prev,
      [kid]: prev[kid] === tab ? '' : tab,
    }));
  };

  return (
    <div className="ms-page pb-20">
      <PageHeader
        title="Kazanımlar & Müfredat Haritası"
        description="Her dersin, her konusunun kazanımları ve o kazanıma bağlı amfi slaytları, sözlük kavramları, örnek ve çıkmış sorular."
      />

      {/* Kurul Selector Bar (Kaydırılabilir) */}
      <div
        className="ms-chipbar overflow-x-auto scroll-smooth py-1"
        role="toolbar"
        aria-label="Kurul seçimi"
        onWheel={(e) => {
          if (e.deltaY !== 0) {
            e.currentTarget.scrollLeft += e.deltaY;
          }
        }}
      >
        {[1, 2, 3, 4, 5, 6].map((k) => {
          const on = selectedKurul === k;
          return (
            <button
              key={k}
              type="button"
              onClick={() => setSelectedKurul(k)}
              className={`ms-fchip ${on ? 'is-on' : ''}`}
            >
              <Compass className="w-3.5 h-3.5" />
              <span>Kurul {k}</span>
            </button>
          );
        })}
      </div>

      {/* Arama ve Ders Filtreleri */}
      <div className="flex flex-col sm:flex-row gap-2.5 my-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-ink-3 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
          <input
            type="search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Kazanım, konu, terim veya patoloji ara..."
            className="w-full h-10 pl-9 pr-3 rounded-xl bg-white border border-line text-[13.5px] text-ink placeholder:text-ink-3 focus:outline-hidden focus:border-accent"
          />
          {searchQuery && (
            <button
              type="button"
              onClick={() => setSearchQuery('')}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-ink-3 hover:text-ink p-1"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        {/* Ders Seçici */}
        <label className="ms-select-chip shrink-0 sm:max-w-[260px]">
          <span className="text-ink-3 shrink-0">Ders</span>
          <select
            value={selectedDers}
            onChange={(e) => setSelectedDers(e.target.value)}
            aria-label="Ders Filtresi"
          >
            <option value="all">Tüm Dersler ({kurulData?.totalCount || 0})</option>
            {dersList.map((d) => (
              <option key={d.ders} value={d.ders}>
                {d.ders} ({d.count})
              </option>
            ))}
          </select>
          <ChevronDown className="w-4 h-4 text-ink-3 shrink-0 pointer-events-none" />
        </label>
      </div>

      {/* Sonuç Sayısı ve Bilgi */}
      <div className="flex items-center justify-between gap-2 text-[12.5px] text-ink-3 mb-3">
        <span>
          Kurul {selectedKurul}: <b className="text-ink">{totalFilteredCount}</b> kazanım listeleniyor
        </span>
        {kurulData && <span className="truncate max-w-[280px]">{kurulData.name}</span>}
      </div>

      {/* İçerik */}
      {loading ? (
        <SectionLoader variant="book" label={`Kurul ${selectedKurul} kazanımları yükleniyor…`} />
      ) : filteredDersler.length === 0 ? (
        <div className="rounded-2xl border border-line bg-white p-8 text-center flex flex-col items-center gap-2">
          <Compass className="w-8 h-8 text-ink-3 opacity-60" />
          <h3 className="m-0 text-[15px] font-semibold text-ink">Eşleşen kazanım bulunamadı</h3>
          <p className="m-0 text-[13px] text-ink-3">Arama terimini değiştirebilir ya da filtreyi temizleyebilirsiniz.</p>
        </div>
      ) : (
        <div className="flex flex-col gap-6">
          {filteredDersler.map((dersGroup) => (
            <section key={dersGroup.ders} className="flex flex-col gap-3">
              {/* Ders Başlığı */}
              <div className="flex items-center gap-2 pb-1.5 border-b border-line-2">
                <span className="w-2.5 h-2.5 rounded-full bg-accent" />
                <h2 className="m-0 text-[15px] font-bold text-ink">{dersGroup.ders}</h2>
                <span className="ms-tag text-[11px] ml-auto font-medium">{dersGroup.count} kazanım</span>
              </div>

              {/* Konular ve Kazanımlar */}
              <div className="flex flex-col gap-3">
                {dersGroup.konular.map((konuGroup) => (
                  <div
                    key={konuGroup.konu}
                    className="rounded-2xl bg-white border border-line flex flex-col shadow-2xs overflow-hidden"
                  >
                    <div className="flex items-center justify-between gap-2 px-4 py-2.5 border-b border-line-soft">
                      <h3 className="m-0 text-[13.5px] font-semibold text-ink flex items-center gap-1.5">
                        <BookOpen className="w-4 h-4 text-accent shrink-0" />
                        <span>{konuGroup.konu}</span>
                      </h3>
                      <span className="text-[11.5px] text-ink-3 shrink-0">
                        {konuGroup.kazanimlar.length} hedef
                      </span>
                    </div>

                    {/* Kazanım Listesi */}
                    <div className="flex flex-col divide-y divide-line-soft">
                      {konuGroup.kazanimlar.map((kazanim, kIdx) => {
                        const activeTab = activeTabByKazanim[kazanim.id] || '';
                        const hasSlides = kazanim.slaytlar.length > 0;
                        const hasOrnek = kazanim.ornekSorular.length > 0;
                        const hasCikmis = kazanim.cikmisSorular.length > 0;
                        const hasGlossary = kazanim.sozlukTerimleri.length > 0;
                        const hasSummaries = kazanim.ozetler.length > 0;

                        return (
                          <div
                            key={kazanim.id || kIdx}
                            className="px-4 py-2 flex flex-col gap-2 transition-colors hover:bg-canvas/60"
                          >
                            <div className="flex flex-col lg:flex-row lg:items-start gap-1 lg:gap-4">
                            {/* Kazanım Metni */}
                            <div className="flex items-start gap-2 flex-1 min-w-0">
                              <span className="w-5 h-5 rounded-md bg-accent-soft text-accent text-[11px] font-bold flex items-center justify-center shrink-0 mt-0.5">
                                {kIdx + 1}
                              </span>
                              <p className="m-0 text-[13.5px] text-ink font-medium leading-snug flex-1 min-w-0 pt-0.5">
                                {kazanim.metin}
                              </p>
                            </div>

                            {/* İlişkili Kaynak Butonları (Pills) */}
                            <div className="flex flex-wrap items-center gap-0.5 pl-7 lg:pl-0 lg:justify-end shrink-0">
                              {hasSlides && (
                                <button
                                  type="button"
                                  onClick={() => toggleTab(kazanim.id, 'slayt')}
                                  className={`ms-btn is-sm ${activeTab === 'slayt' ? 'is-on' : 'is-ghost'} h-7! px-2! text-[12px]!`}
                                  title="Bağlı amfi slaytlarını ve sayfaları incele"
                                >
                                  <Presentation className="w-3.5 h-3.5" />
                                  <span className="sr-only">Slayt</span><span className="tabular-nums">{kazanim.slaytlar.length}</span>
                                </button>
                              )}

                              {hasCikmis && (
                                <button
                                  type="button"
                                  onClick={() => toggleTab(kazanim.id, 'cikmis')}
                                  className={`ms-btn is-sm ${activeTab === 'cikmis' ? 'is-on' : 'is-ghost'} h-7! px-2! text-[12px]! text-ok!`}
                                  title="Bu kazanımla eşleşen çıkmış sınav soruları"
                                >
                                  <Archive className="w-3.5 h-3.5" />
                                  <span className="sr-only">Çıkmış</span><span className="tabular-nums">{kazanim.cikmisSorular.length}</span>
                                </button>
                              )}

                              {hasOrnek && (
                                <button
                                  type="button"
                                  onClick={() => toggleTab(kazanim.id, 'ornek')}
                                  className={`ms-btn is-sm ${activeTab === 'ornek' ? 'is-on' : 'is-ghost'} h-7! px-2! text-[12px]! text-accent!`}
                                  title="Kazanım temelli örnek sorular"
                                >
                                  <Target className="w-3.5 h-3.5" />
                                  <span className="sr-only">Örnek Soru</span><span className="tabular-nums">{kazanim.ornekSorular.length}</span>
                                </button>
                              )}

                              {hasGlossary && (
                                <button
                                  type="button"
                                  onClick={() => toggleTab(kazanim.id, 'sozluk')}
                                  className={`ms-btn is-sm ${activeTab === 'sozluk' ? 'is-on' : 'is-ghost'} h-7! px-2! text-[12px]!`}
                                  title="İlgili tıbbi terim ve tanımlar"
                                >
                                  <BookOpenText className="w-3.5 h-3.5" />
                                  <span className="sr-only">Sözlük</span><span className="tabular-nums">{kazanim.sozlukTerimleri.length}</span>
                                </button>
                              )}

                              {hasSummaries && (
                                <button
                                  type="button"
                                  onClick={() => toggleTab(kazanim.id, 'ozet')}
                                  className={`ms-btn is-sm ${activeTab === 'ozet' ? 'is-on' : 'is-ghost'} h-7! px-2! text-[12px]!`}
                                  title="Ders özeti kilit noktaları"
                                >
                                  <Sparkles className="w-3.5 h-3.5" />
                                  <span className="sr-only">Özet</span><span className="tabular-nums">{kazanim.ozetler.length}</span>
                                </button>
                              )}
                            </div>
                            </div>

                            {/* Açılır Panel: Slaytlar */}
                            {activeTab === 'slayt' && (
                              <div className="rounded-xl bg-white p-3 border border-line-2 flex flex-col gap-2 ms-pop-in">
                                <span className="text-[12px] font-bold text-ink-2 flex items-center gap-1.5 pb-1 border-b border-line-2">
                                  <Presentation className="w-3.5 h-3.5 text-accent" /> İlgili Ders Notu & Slaytlar
                                </span>
                                <div className="flex flex-col gap-2">
                                  {kazanim.slaytlar.map((sl, sIdx) => (
                                    <div
                                      key={sIdx}
                                      className="rounded-lg bg-canvas p-2.5 flex items-center justify-between gap-2 border border-line-2/50"
                                    >
                                      <div className="min-w-0 flex-1">
                                        <p className="m-0 text-[13px] font-semibold text-ink truncate">
                                          {sl.kaynak}{' '}
                                          <span className="font-normal text-ink-3">· sayfa {sl.sayfa}</span>
                                        </p>
                                        {sl.alinti && (
                                          <p className="m-0 text-[12px] text-ink-2 mt-0.5 line-clamp-2">
                                            {sl.alinti}
                                          </p>
                                        )}
                                      </div>
                                      {onNavigateToLearn && (
                                        <button
                                          type="button"
                                          onClick={() => onNavigateToLearn(sl.deckId, sl.sayfa)}
                                          className="ms-btn is-tonal is-sm shrink-0"
                                          title="Öğren modunda aç"
                                        >
                                          <GraduationCap className="w-3.5 h-3.5" /> Slayta Git
                                        </button>
                                      )}
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Açılır Panel: Çıkmış Sorular */}
                            {activeTab === 'cikmis' && (
                              <div className="rounded-xl bg-white p-3 border border-line-2 flex flex-col gap-2 ms-pop-in">
                                <div className="flex items-center justify-between pb-1 border-b border-line-2">
                                  <span className="text-[12px] font-bold text-ink-2 flex items-center gap-1.5">
                                    <Archive className="w-3.5 h-3.5 text-ok" /> Bağlı Çıkmış Sınav Soruları
                                  </span>
                                  {onNavigateToPastExams && (
                                    <button
                                      type="button"
                                      onClick={() => onNavigateToPastExams(konuGroup.konu)}
                                      className="text-[11.5px] font-semibold text-accent hover:underline flex items-center gap-1 cursor-pointer"
                                    >
                                      Çıkmış'ta Tümünü Gör <ExternalLink className="w-3 h-3" />
                                    </button>
                                  )}
                                </div>
                                <div className="flex flex-col gap-2.5">
                                  {kazanim.cikmisSorular.map((q) => (
                                    <div
                                      key={q.id}
                                      className="rounded-lg bg-canvas p-3 border border-line-2 flex flex-col gap-2"
                                    >
                                      <div className="flex items-center justify-between text-[11.5px] text-ink-3">
                                        <span className="font-semibold text-ink">
                                          Soru #{q.questionNumber || '–'} · {q.year || 'Arşiv'}
                                        </span>
                                        {q.correctAnswer && (
                                          <span className="ms-tag is-ok text-[11px] font-bold">
                                            Doğru: {q.correctAnswer}
                                          </span>
                                        )}
                                      </div>
                                      <p className="m-0 text-[12.5px] text-ink font-medium leading-relaxed">
                                        {q.stem}
                                      </p>
                                      {q.options && q.options.length > 0 && (
                                        <ul className="m-0 p-0 list-none flex flex-col gap-1 text-[12px] text-ink-2">
                                          {q.options.map((opt) => (
                                            <li
                                              key={opt.key}
                                              className={`px-2 py-0.5 rounded flex items-center gap-1.5 ${
                                                opt.key === q.correctAnswer ? 'bg-ok-soft font-semibold text-ok' : ''
                                              }`}
                                            >
                                              <span className="font-mono font-bold shrink-0">{opt.key})</span>
                                              <span>{opt.text}</span>
                                            </li>
                                          ))}
                                        </ul>
                                      )}
                                      {q.explanation && (
                                        <div className="text-[11.5px] text-ink-3 pt-1 border-t border-line-2/40 italic">
                                          {q.explanation}
                                        </div>
                                      )}
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Açılır Panel: Örnek Sorular */}
                            {activeTab === 'ornek' && (
                              <div className="rounded-xl bg-white p-3 border border-line-2 flex flex-col gap-2 ms-pop-in">
                                <div className="flex items-center justify-between pb-1 border-b border-line-2">
                                  <span className="text-[12px] font-bold text-ink-2 flex items-center gap-1.5">
                                    <Target className="w-3.5 h-3.5 text-accent" /> Kazanım Odaklı Örnek Çalışma Sorusu
                                  </span>
                                  {onNavigateToOrnek && (
                                    <button
                                      type="button"
                                      onClick={onNavigateToOrnek}
                                      className="text-[11.5px] font-semibold text-accent hover:underline flex items-center gap-1 cursor-pointer"
                                    >
                                      Örnek Sorular Modu <ExternalLink className="w-3 h-3" />
                                    </button>
                                  )}
                                </div>
                                <div className="flex flex-col gap-3">
                                  {kazanim.ornekSorular.map((oq) => {
                                    const userPick = ornekAnswers[oq.id];
                                    const solved = !!userPick;
                                    const isCorrect = userPick === oq.dogru;

                                    return (
                                      <div
                                        key={oq.id}
                                        className="rounded-lg bg-canvas p-3 border border-line-2 flex flex-col gap-2"
                                      >
                                        <div className="flex items-center justify-between text-[11.5px] text-ink-3">
                                          <span className="ms-tag is-accent text-[11px]">
                                            {oq.zorluk || 'Standart'}
                                          </span>
                                          {solved && (
                                            <span
                                              className={`ms-tag font-bold text-[11px] ${
                                                isCorrect ? 'is-ok' : 'is-bad'
                                              }`}
                                            >
                                              {isCorrect ? '✓ Doğru' : `Yanıt: ${oq.dogru}`}
                                            </span>
                                          )}
                                        </div>
                                        <p className="m-0 text-[12.5px] text-ink font-medium leading-relaxed">
                                          {oq.soru}
                                        </p>
                                        <div className="flex flex-col gap-1 text-[12px]">
                                          {Object.entries(oq.secenekler || {}).map(([key, text]) => {
                                            const picked = userPick === key;
                                            const corr = key === oq.dogru;
                                            let cls = 'bg-white hover:bg-field border-line-2 text-ink-2';
                                            if (solved) {
                                              if (corr) cls = 'bg-ok-soft text-ok font-semibold border-ok/30';
                                              else if (picked) cls = 'bg-bad-soft text-bad-text border-bad/30';
                                            }
                                            return (
                                              <button
                                                key={key}
                                                type="button"
                                                disabled={solved}
                                                onClick={() =>
                                                  setOrnekAnswers((p) => ({ ...p, [oq.id]: key }))
                                                }
                                                className={`text-left p-1.5 rounded-lg border flex items-start gap-2 cursor-pointer transition-colors ${cls}`}
                                              >
                                                <span className="font-mono font-bold shrink-0">{key})</span>
                                                <span className="leading-snug">{text}</span>
                                              </button>
                                            );
                                          })}
                                        </div>
                                        {solved && oq.aciklama && (
                                          <p className="m-0 text-[11.5px] text-ink-2 bg-field p-2 rounded-lg border border-line-2">
                                            <b>Açıklama:</b> {oq.aciklama}
                                          </p>
                                        )}
                                      </div>
                                    );
                                  })}
                                </div>
                              </div>
                            )}

                            {/* Açılır Panel: Sözlük Terimleri */}
                            {activeTab === 'sozluk' && (
                              <div className="rounded-xl bg-white p-3 border border-line-2 flex flex-col gap-2 ms-pop-in">
                                <span className="text-[12px] font-bold text-ink-2 flex items-center gap-1.5 pb-1 border-b border-line-2">
                                  <BookOpenText className="w-3.5 h-3.5 text-accent" /> İlgili Tıbbi Sözlük Kavramları
                                </span>
                                <div className="flex flex-col gap-2">
                                  {kazanim.sozlukTerimleri.map((t, idx) => (
                                    <div
                                      key={idx}
                                      className="rounded-lg bg-canvas p-2.5 border border-line-2 flex flex-col gap-1"
                                    >
                                      <h4 className="m-0 text-[13px] font-bold text-ink">{t.term}</h4>
                                      <p className="m-0 text-[12px] text-ink-2 leading-relaxed">
                                        {t.definition}
                                      </p>
                                      {t.pearl && (
                                        <p className="m-0 text-[11.5px] text-ink-3 italic mt-0.5">
                                          💡 {t.pearl}
                                        </p>
                                      )}
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Açılır Panel: Ders Özeti */}
                            {activeTab === 'ozet' && (
                              <div className="rounded-xl bg-white p-3 border border-line-2 flex flex-col gap-2 ms-pop-in">
                                <span className="text-[12px] font-bold text-ink-2 flex items-center gap-1.5 pb-1 border-b border-line-2">
                                  <Sparkles className="w-3.5 h-3.5 text-accent" /> İlgili Ders Özeti Noktaları
                                </span>
                                <ul className="m-0 pl-4 list-disc flex flex-col gap-1 text-[12.5px] text-ink-2">
                                  {kazanim.ozetler.map((bullet, idx) => (
                                    <li key={idx} className="leading-relaxed">
                                      {bullet}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          ))}
        </div>
      )}
    </div>
  );
};
