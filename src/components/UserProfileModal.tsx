import React, { useState } from 'react';
import { 
  X, 
  User, 
  Hash, 
  Mail, 
  CheckCircle2, 
  AlertCircle, 
  Save, 
  Award, 
  BookOpen, 
  ShieldCheck 
} from 'lucide-react';
import { AppUser, updateUserProfileData } from '../services/auth';
import { QuestionItem } from '../types';

interface UserProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentUser: AppUser | null;
  onUpdateUser: (updatedUser: AppUser) => void;
  questions: QuestionItem[];
}

export const UserProfileModal: React.FC<UserProfileModalProps> = ({
  isOpen,
  onClose,
  currentUser,
  onUpdateUser,
  questions,
}) => {
  if (!isOpen || !currentUser) return null;

  const [displayName, setDisplayName] = useState(currentUser.displayName || '');
  const [studentNumber, setStudentNumber] = useState(currentUser.studentNumber || '');
  const [isSaving, setIsSaving] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleStudentNumberChange = (val: string) => {
    const numeric = val.replace(/\D/g, '').slice(0, 12);
    setStudentNumber(numeric);
  };

  // Find user's contributed questions
  const myContributedQuestions = questions.filter(
    (q) =>
      q.contributedByUid === currentUser.uid ||
      q.fragments.some((f) => f.authorUid === currentUser.uid || (currentUser.displayName && f.author === currentUser.displayName)) ||
      q.options.some((o) => o.suggestedByUid === currentUser.uid || (currentUser.displayName && o.suggestedBy === currentUser.displayName))
  );

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    const cleanNum = studentNumber.replace(/\D/g, '');

    setIsSaving(true);
    try {
      const updated = await updateUserProfileData(currentUser, {
        displayName: displayName.trim() || undefined,
        studentNumber: cleanNum || undefined,
      });

      onUpdateUser(updated);
      setSuccess('Profil bilgileriniz ve öğrenci numaranız başarıyla güncellendi!');
      setTimeout(() => {
        setSuccess(null);
      }, 4000);
    } catch (err: any) {
      setError(err.message || 'Güncelleme sırasında hata oluştu.');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-fadeIn">
      <div 
        className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-lg overflow-hidden relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-teal-900 via-teal-800 to-slate-900 p-5 text-white flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-500/20 border border-teal-400/30 flex items-center justify-center text-teal-300 font-bold text-lg">
              {(currentUser.displayName || currentUser.email || 'Ö')[0].toUpperCase()}
            </div>
            <div>
              <h3 className="font-bold text-base leading-tight">
                Öğrenci Profilim & Ayarlar
              </h3>
              <p className="text-xs text-teal-200/80">
                {currentUser.email}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-white/70 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Stats Bar */}
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-teal-50/70 border border-teal-200 rounded-xl p-3.5 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-teal-600 text-white">
                <BookOpen className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[11px] font-semibold text-teal-800 block">Katkıda Bulunduğum</span>
                <span className="text-lg font-black text-teal-950">{myContributedQuestions.length} Soru</span>
              </div>
            </div>

            <div className="bg-emerald-50/70 border border-emerald-200 rounded-xl p-3.5 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-emerald-600 text-white">
                <Award className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[11px] font-semibold text-emerald-800 block">Tebrik E-postası</span>
                <span className="text-xs font-bold text-emerald-950 mt-1 block">
                  {currentUser.congratsSentCommittees && currentUser.congratsSentCommittees.length > 0
                    ? `${currentUser.congratsSentCommittees.length} Kurulda Alındı`
                    : 'İlk Katkıda Gelecek'}
                </span>
              </div>
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSave} className="space-y-4">
            {error && (
              <div className="bg-rose-50 border border-rose-200 text-rose-800 text-xs p-3 rounded-lg flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}
            {success && (
              <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs p-3 rounded-lg flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>{success}</span>
              </div>
            )}

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                İsim / Soyisim (Görünen Ad)
              </label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                <input
                  type="text"
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  placeholder="Adınızı ve soyadınızı giriniz"
                  className="w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-hidden focus:border-teal-600"
                />
              </div>
              <p className="text-[11px] text-slate-500 mt-1">
                Soru ve şık eklerken adınız otomatik hatırlanacaktır.
              </p>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1 flex items-center justify-between">
                <span>Öğrenci Numarası <span className="text-slate-400 font-normal">(İsteğe bağlı)</span></span>
                {studentNumber && (
                  <span className={`text-[11px] font-bold px-2 py-0.5 rounded ${studentNumber.length === 11 ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' : 'bg-teal-50 text-teal-800 border border-teal-200'}`}>
                    {studentNumber.length === 11 ? '✓ 11 Haneli Standart No (Geçerli)' : `${studentNumber.length} Hane (Kabul Edildi ✓)`}
                  </span>
                )}
              </label>
              <div className="relative">
                <Hash className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                <input
                  type="text"
                  inputMode="numeric"
                  maxLength={16}
                  value={studentNumber}
                  onChange={(e) => handleStudentNumberChange(e.target.value)}
                  placeholder="Örn: 20241054012"
                  className="w-full pl-9 pr-3 py-2 text-sm font-mono border border-slate-300 rounded-lg focus:outline-hidden focus:border-teal-600"
                />
              </div>
              <p className="text-[11px] text-slate-500 mt-1">
                Boşluklu veya tireli yapıştırsanız bile otomatik temizlenir.
              </p>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Kayıtlı E-posta Adresi
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                <input
                  type="text"
                  disabled
                  value={currentUser.email || 'Girilmedi'}
                  className="w-full pl-9 pr-3 py-2 text-sm border border-slate-200 bg-slate-50 text-slate-500 rounded-lg cursor-not-allowed"
                />
              </div>
              <p className="text-[10px] text-teal-700 mt-1 font-medium">
                Her kurulda ilk soru katkınız için teşekkür e-postası bu adrese otomatik iletilir.
              </p>
            </div>

            <div className="pt-2 flex items-center justify-end gap-2.5">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-800 hover:bg-slate-100 rounded-lg cursor-pointer"
              >
                Kapat
              </button>
              <button
                type="submit"
                disabled={isSaving}
                className="bg-teal-700 hover:bg-teal-800 text-white font-bold px-5 py-2 rounded-lg text-xs flex items-center gap-1.5 shadow-sm transition-all cursor-pointer disabled:opacity-50"
              >
                <Save className="w-4 h-4" />
                <span>{isSaving ? 'Kaydediliyor...' : 'Bilgileri Kaydet'}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
