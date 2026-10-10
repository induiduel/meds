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
import { validateNamePolicy } from '../utils/namePolicy';

interface UserProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentUser: AppUser | null;
  onUpdateUser: (updatedUser: AppUser) => void;
  questions: QuestionItem[];
  onOpenAdminPanel?: () => void;
}

export const UserProfileModal: React.FC<UserProfileModalProps> = (props) => {
  if (!props.isOpen || !props.currentUser) return null;
  return <UserProfileModalContent {...props} currentUser={props.currentUser} />;
};

const UserProfileModalContent: React.FC<UserProfileModalProps & { currentUser: NonNullable<UserProfileModalProps['currentUser']> }> = ({
  onClose,
  currentUser,
  onUpdateUser,
  questions,
  onOpenAdminPanel,
}) => {
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

    if (displayName.trim()) {
      const nameCheck = validateNamePolicy(displayName.trim(), { adminEmail: currentUser?.email });
      if (!nameCheck.isValid) {
        setError(nameCheck.errorMessage || 'Geçersiz isim girdiniz.');
        return;
      }
    }

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
    <div className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/60 backdrop-blur-xs animate-fadeIn">
      <div 
        className="ms-modal-panel bg-white rounded-2xl shadow-2xl border border-line w-full max-w-lg overflow-hidden relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-ink-surface p-5 text-white flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-ok/20 border border-ok/30 flex items-center justify-center text-ok font-bold text-lg">
              {(currentUser.displayName || currentUser.email || 'Ö')[0].toUpperCase()}
            </div>
            <div>
              <h3 className="font-bold text-base leading-tight">
                Öğrenci Profilim & Ayarlar
              </h3>
              <p className="text-xs text-ok-soft/80">
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
            <div className="bg-ok-soft/70 border border-ok/30 rounded-xl p-3.5 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-ok text-white">
                <BookOpen className="w-4 h-4" />
              </div>
              <div>
                <span className="text-2xs font-semibold text-ok block">Katkıda Bulunduğum</span>
                <span className="text-lg font-black text-ok">{myContributedQuestions.length} Soru</span>
              </div>
            </div>

            <div className="bg-ok-soft/70 border border-ok/30 rounded-xl p-3.5 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-ok text-white">
                <Award className="w-4 h-4" />
              </div>
              <div>
                <span className="text-2xs font-semibold text-ok block">Tebrik E-postası</span>
                <span className="text-xs font-bold text-ok mt-1 block">
                  {currentUser.congratsSentCommittees && currentUser.congratsSentCommittees.length > 0
                    ? `${currentUser.congratsSentCommittees.length} Kurulda Alındı`
                    : 'İlk Katkıda Gelecek'}
                </span>
              </div>
            </div>
          </div>

          {/* Admin Panel Quick Access if Admin */}
          {currentUser.email?.toLowerCase() === 'nofrostlife@gmail.com' && onOpenAdminPanel && (
            <div className="bg-warn-soft border border-warn/30 rounded-xl p-3.5 flex items-center justify-between gap-3 shadow-2xs">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-lg bg-warn text-ink font-bold">
                  <ShieldCheck className="w-5 h-5" />
                </div>
                <div>
                  <span className="font-extrabold text-xs text-warn block">Sistem Yöneticisi Yetkisi Aktif</span>
                  <span className="text-2xs text-warn">Soru silme, kullanıcı yönetimi & otomasyonlar</span>
                </div>
              </div>
              <button
                type="button"
                onClick={() => {
                  onClose();
                  onOpenAdminPanel();
                }}
                className="bg-warn hover:bg-warn text-ink font-bold px-3 py-1.5 rounded-lg text-xs cursor-pointer shadow-xs transition-all active:scale-95 shrink-0"
              >
                Yönetici Panelini Aç               </button>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSave} className="space-y-4">
            {error && (
              <div className="bg-bad-soft border border-bad/30 text-bad-text text-xs p-3 rounded-lg flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-bad-text shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}
            {success && (
              <div className="bg-ok-soft border border-ok/30 text-ok text-xs p-3 rounded-lg flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-ok shrink-0 mt-0.5" />
                <span>{success}</span>
              </div>
            )}

            <div>
              <label className="block text-xs font-bold text-ink-2 mb-1">
                İsim / Soyisim (Görünen Ad)
              </label>
              <div className="relative">
                <User className="w-4 h-4 text-ink-3 absolute left-3 top-2.5" />
                <input
                  type="text"
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  placeholder="Adınızı ve soyadınızı giriniz"
                  className="w-full pl-9 pr-3 py-2 text-sm border border-line-2 rounded-lg focus:outline-hidden focus:border-ok"
                />
              </div>
              <p className="text-2xs text-ink-3 mt-1">
                Soru ve şık eklerken adınız otomatik hatırlanacaktır.
              </p>
            </div>

            <div>
              <label className="block text-xs font-bold text-ink-2 mb-1 flex items-center justify-between">
                <span>Öğrenci Numarası <span className="text-ink-3 font-normal">(İsteğe bağlı)</span></span>
                {studentNumber && (
                  <span className={`text-2xs font-bold px-2 py-0.5 rounded ${studentNumber.length === 11 ? 'bg-ok-soft text-ok border border-ok/30' : 'bg-ok-soft text-ok border border-ok/30'}`}>
                    {studentNumber.length === 11 ? '✓ 11 Haneli Standart No (Geçerli)' : `${studentNumber.length} Hane (Kabul Edildi ✓)`}
                  </span>
                )}
              </label>
              <div className="relative">
                <Hash className="w-4 h-4 text-ink-3 absolute left-3 top-2.5" />
                <input
                  type="text"
                  inputMode="numeric"
                  maxLength={16}
                  value={studentNumber}
                  onChange={(e) => handleStudentNumberChange(e.target.value)}
                  placeholder="Örn: 20241054012"
                  className="w-full pl-9 pr-3 py-2 text-sm font-mono border border-line-2 rounded-lg focus:outline-hidden focus:border-ok"
                />
              </div>
              <p className="text-2xs text-ink-3 mt-1">
                Boşluklu veya tireli yapıştırsanız bile otomatik temizlenir.
              </p>
            </div>

            <div>
              <label className="block text-xs font-bold text-ink-2 mb-1">
                Kayıtlı E-posta Adresi
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 text-ink-3 absolute left-3 top-2.5" />
                <input
                  type="text"
                  disabled
                  value={currentUser.email || 'Girilmedi'}
                  className="w-full pl-9 pr-3 py-2 text-sm border border-line bg-field text-ink-3 rounded-lg cursor-not-allowed"
                />
              </div>
              <p className="text-2xs text-ok mt-1 font-medium">
                Her kurulda ilk soru katkınız için teşekkür e-postası bu adrese otomatik iletilir.
              </p>
            </div>

            <div className="pt-2 flex items-center justify-end gap-2.5">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-xs font-semibold text-ink-2 hover:text-ink hover:bg-field rounded-lg cursor-pointer"
              >
                Kapat
              </button>
              <button
                type="submit"
                disabled={isSaving}
                className="bg-ok hover:bg-ok text-white font-bold px-5 py-2 rounded-lg text-xs flex items-center gap-1.5 shadow-sm transition-all cursor-pointer disabled:opacity-50"
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
