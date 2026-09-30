import React, { useState } from 'react';
import { X, FolderPlus, Check } from 'lucide-react';

interface AddCommitteeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAddCommittee: (data: {
    name: string;
    year: number;
    term: string;
    targetCount: number;
    description: string;
  }) => Promise<void>;
}

export const AddCommitteeModal: React.FC<AddCommitteeModalProps> = ({
  isOpen,
  onClose,
  onAddCommittee,
}) => {
  const [name, setName] = useState('');
  const [year, setYear] = useState(3);
  const [term, setTerm] = useState('2025-2026');
  const [targetCount, setTargetCount] = useState(100);
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    setIsSubmitting(true);
    try {
      await onAddCommittee({
        name: name.trim(),
        year: Number(year),
        term: term.trim(),
        targetCount: Number(targetCount),
        description: description.trim(),
      });
      onClose();
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-md w-full shadow-2xl border border-slate-200 overflow-hidden">
        <div className="bg-teal-700 text-white p-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FolderPlus className="w-5 h-5 text-teal-200" />
            <h3 className="font-bold text-sm">Yeni Kurul / Komite Sınavı Ekle</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-white/70 hover:text-white rounded hover:bg-white/10 cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Kurul Sınavı Adı *
            </label>
            <input
              type="text"
              placeholder="Ör: Dönem 3 - Kurul 4: Endokrin & Ürogenital Sistem"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-900 focus:bg-white focus:outline-hidden focus:ring-1 focus:ring-teal-500"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Tıp Dönemi</label>
              <select
                value={year}
                onChange={(e) => setYear(Number(e.target.value))}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs text-slate-800"
              >
                <option value={1}>Dönem 1</option>
                <option value={2}>Dönem 2</option>
                <option value={3}>Dönem 3</option>
                <option value={4}>Dönem 4 (Staj)</option>
                <option value={5}>Dönem 5 (Staj)</option>
                <option value={6}>Dönem 6 (İntörn / TUS)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Soru Sayısı</label>
              <select
                value={targetCount}
                onChange={(e) => setTargetCount(Number(e.target.value))}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs text-slate-800"
              >
                <option value={50}>50 Soru</option>
                <option value={100}>100 Soru</option>
                <option value={120}>120 Soru</option>
                <option value={150}>150 Soru</option>
                <option value={200}>200 Soru</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Akademik Yıl / Dönem</label>
            <input
              type="text"
              placeholder="2025-2026 Güz"
              value={term}
              onChange={(e) => setTerm(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 text-xs text-slate-800"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Kısa Açıklama & Dersler</label>
            <textarea
              rows={2}
              placeholder="Patoloji, Farmakoloji, Dahiliye soruları..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-xs text-slate-800"
            />
          </div>

          <div className="pt-3 border-t border-slate-100 flex items-center justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-3.5 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-100 rounded-lg cursor-pointer"
            >
              Vazgeç
            </button>
            <button
              type="submit"
              disabled={isSubmitting || !name.trim()}
              className="bg-teal-700 hover:bg-teal-800 text-white px-4 py-1.5 text-xs font-bold rounded-lg cursor-pointer disabled:opacity-50"
            >
              {isSubmitting ? 'Ekleniyor...' : 'Kurulu Oluştur'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
