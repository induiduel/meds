import React, { useState, useEffect, useMemo } from 'react';
import { PageHeader } from './ui/PageHeader';
import { 
  FileText, 
  Sparkles, 
  Search, 
  RefreshCw, 
  BookOpen, 
  CheckCircle2, 
  Copy, 
  Check, 
  ChevronRight,
  ExternalLink,
  Layers
} from 'lucide-react';
import { safeJsonFetch } from '../services/api';

interface TesterOzetItem {
  id: string;
  fileName: string;
  title: string;
  wordCount: number;
  tableCount: number;
  questionCount: number;
  content: string;
  mtime: string;
}

export function TesterOzetView() {
  const [items, setItems] = useState<TesterOzetItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [copied, setCopied] = useState(false);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const res = await safeJsonFetch<{ success: boolean; items: TesterOzetItem[] }>('/api/tester/ozet');
      const data = res?.data;
      if (data && data.items) {
        setItems(data.items);
        if (data.items.length > 0 && !selectedId) {
          setSelectedId(data.items[0].id);
        }
      }
    } catch (e) {
      console.error('Tester özet yükleme hatası:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
    const interval = setInterval(fetchItems, 10000); // 10 saniyede bir yeni üretilenleri tazele
    return () => clearInterval(interval);
  }, []);

  const filteredItems = useMemo<TesterOzetItem[]>(() => {
    if (!search.trim()) return items;
    const q = search.toLowerCase();
    return items.filter(it => it.title.toLowerCase().includes(q) || it.fileName.toLowerCase().includes(q));
  }, [items, search]);

  const activeItem = useMemo<TesterOzetItem | null>(() => {
    return items.find(it => it.id === selectedId) || items[0] || null;
  }, [items, selectedId]);

  const copyContent = () => {
    if (!activeItem) return;
    navigator.clipboard.writeText(activeItem.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="w-full min-w-0 pb-12 space-y-6">
      <PageHeader
        title="2026-2027 Ders Notları Test Laboratuvarı (/tester/ozet)"
        description="Bulut API'leri tarafından dinamik uzunluk ve karşılaştırmalı tablolarla üretilen yeni ders notları canlı önizlemesi."
        actions={
          <button
            onClick={fetchItems}
            disabled={loading}
            className="flex items-center gap-2 h-10 px-4 rounded-xl border border-line-2 bg-white hover:bg-surface text-ink text-[14px] font-medium transition cursor-pointer"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Yenile
          </button>
        }
      />

      {/* İstatistik Çubuğu */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-2xl bg-white border border-line flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-accent-light text-accent flex items-center justify-center font-bold">
            <BookOpen className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[20px] font-bold text-ink">{items.length}</div>
            <div className="text-[12px] text-ink-3">Üretilen Yeni Not</div>
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-white border border-line flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-ok-soft text-ok flex items-center justify-center font-bold">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[20px] font-bold text-ink">
              {items.reduce((acc, it) => acc + it.wordCount, 0).toLocaleString()}
            </div>
            <div className="text-[12px] text-ink-3">Toplam Kelime Hacmi</div>
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-white border border-line flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-accent-soft text-accent flex items-center justify-center font-bold">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[20px] font-bold text-ink">
              {items.reduce((acc, it) => acc + it.tableCount, 0)}
            </div>
            <div className="text-[12px] text-ink-3">Tıbbi Tablo Sayısı</div>
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-white border border-line flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-warn-soft text-warn flex items-center justify-center font-bold">
            <CheckCircle2 className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[20px] font-bold text-ink">
              {items.reduce((acc, it) => acc + it.questionCount, 0)}
            </div>
            <div className="text-[12px] text-ink-3">Entegre Çıkmış Soru</div>
          </div>
        </div>
      </div>

      {/* İki Sütunlu Okuyucu & İnceleme Alanı */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Sol Sütun: Ders Listesi */}
        <div className="lg:col-span-4 bg-white rounded-2xl border border-line overflow-hidden flex flex-col max-h-[820px]">
          <div className="p-4 border-b border-line">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-3 text-ink-3" />
              <input
                type="text"
                placeholder="Ders notlarında ara..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded-xl border border-line-2 bg-surface text-[14px] text-ink placeholder:text-ink-4 outline-none focus:border-accent"
              />
            </div>
          </div>

          <div className="flex-1 overflow-y-auto divide-y divide-line p-2">
            {filteredItems.length === 0 ? (
              <div className="py-8 text-center text-ink-4 text-[14px]">
                {loading ? 'Yükleniyor...' : 'Henüz not bulunamadı.'}
              </div>
            ) : (
              filteredItems.map(item => {
                const isSelected = item.id === selectedId;
                return (
                  <button
                    key={item.id}
                    onClick={() => setSelectedId(item.id)}
                    className={`w-full p-3.5 text-left rounded-xl transition flex flex-col gap-1.5 cursor-pointer ${
                      isSelected ? 'bg-accent/10 border-accent/30' : 'hover:bg-surface'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[12px] font-bold text-accent">
                        {item.wordCount.toLocaleString()} kelime
                      </span>
                      <span className="text-[11px] text-ink-4">
                        {item.tableCount} Tablo · {item.questionCount} Soru
                      </span>
                    </div>
                    <div className="text-[14px] font-semibold text-ink line-clamp-2">
                      {item.title}
                    </div>
                    <div className="text-[11px] text-ink-3 truncate">
                      {item.fileName}
                    </div>
                  </button>
                );
              })
            )}
          </div>
        </div>

        {/* Sağ Sütun: Notun Detaylı Görünümü */}
        <div className="lg:col-span-8 bg-white rounded-2xl border border-line p-6 sm:p-8 space-y-6 max-h-[820px] overflow-y-auto">
          {activeItem ? (
            <>
              <div className="flex items-start justify-between gap-4 border-b border-line pb-4">
                <div>
                  <h2 className="text-[20px] sm:text-[22px] font-bold text-ink">
                    {activeItem.title}
                  </h2>
                  <div className="text-[13px] text-ink-3 mt-1 flex items-center gap-3">
                    <span>Dosya: {activeItem.fileName}</span>
                    <span>·</span>
                    <span>Hacim: {activeItem.wordCount.toLocaleString()} kelime</span>
                    <span>·</span>
                    <span>Tablolar: {activeItem.tableCount}</span>
                  </div>
                </div>

                <button
                  onClick={copyContent}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-line-2 bg-surface hover:bg-line text-ink text-[13px] transition cursor-pointer"
                >
                  {copied ? <Check className="w-4 h-4 text-ok" /> : <Copy className="w-4 h-4 text-ink-3" />}
                  {copied ? 'Kopyalandı' : 'Markdown Kopyala'}
                </button>
              </div>

              {/* Rendered Markdown Metni */}
              <div className="prose max-w-none text-ink text-[15px] leading-relaxed whitespace-pre-wrap font-sans">
                {activeItem.content}
              </div>
            </>
          ) : (
            <div className="py-20 text-center text-ink-4">
              İncelemek için sol listeden bir ders notu seçin.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
