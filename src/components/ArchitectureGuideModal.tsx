import React from 'react';
import { 
  X, 
  Layers, 
  Database, 
  Cpu, 
  Globe, 
  ArrowRight, 
  Users, 
  Sparkles, 
  CheckCircle2, 
  FileCode2,
  Server,
  Zap,
  BookOpen
} from 'lucide-react';

interface ArchitectureGuideModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ArchitectureGuideModal: React.FC<ArchitectureGuideModalProps> = ({
  isOpen,
  onClose,
}) => {
  if (!isOpen) return null;

  return (
    <div className="ms-overlay fixed inset-0 z-50 bg-ink/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="ms-modal-panel bg-white rounded-2xl max-w-3xl w-full shadow-2xl border border-line overflow-hidden my-6">
        {/* Header */}
        <div className="bg-ink-surface text-white p-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-ok/20 border border-ok/30 flex items-center justify-center">
              <Zap className="w-5 h-5 text-ok" />
            </div>
            <div>
              <h3 className="text-base font-bold">
                Tıp Öğrencisi İçin Sistem Mimarisi: "Nasıl Yapılır?"
              </h3>
              <p className="text-xs text-ok-soft/80">
                Arayüz, Veritabanı ve Yapay Zekayı bir araya getiren 4 temel yapı taşı
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-white/70 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6 max-h-[75dvh] overflow-y-auto text-xs leading-relaxed text-ink-2">
          {/* Welcome note */}
          <div className="bg-ok-soft/70 border border-ok/30 rounded-xl p-4">
            <h4 className="text-sm font-bold text-ok mb-1 flex items-center gap-1.5">
              <BookOpen className="w-4 h-4 text-ok" />
              Sevgili Meslektaş Adayımız (Dönem 3):
            </h4>
            <p className="text-ok">
              Sorduğun soru tıp fakültelerinde her kurul çıkışı yaşanan en büyük probleme nokta atışı bir çözüm önerisidir:
              <strong> "Tek tek herkes sorunun bir kısmını hatırlar ama kimse tam halini bilmez. Ancak herkes parçaları bir havuza atarsa ve yapay zeka bu parçaları birleştirirse %100 doğrulukta bir kurul arşivi doğar."</strong>
              Aşağıda yazılım bilmeden bile mantığını kavrayabileceğin mimariyi adım adım açıkladık:
            </p>
          </div>

          {/* Diagram Flow */}
          <div className="bg-field border border-line rounded-xl p-4 space-y-3">
            <span className="font-bold text-ink text-xs uppercase tracking-wider block">
              Sistemin Çalışma Döngüsü (Mimari Şema)
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-4 gap-2 text-center text-xs">
              <div className="bg-white p-3 rounded-lg border border-line shadow-2xs">
                <Users className="w-5 h-5 text-ok mx-auto mb-1" />
                <span className="font-bold block text-ink">1. Öğrenci Katkısı</span>
                <span className="text-2xs text-ink-3">Soru kökü, şık veya vaka ipucu girilir</span>
              </div>
              <div className="bg-white p-3 rounded-lg border border-line shadow-2xs">
                <Database className="w-5 h-5 text-accent mx-auto mb-1" />
                <span className="font-bold block text-ink">2. Veritabanı Havuzu</span>
                <span className="text-2xs text-ink-3">Girdiler anında diskte JSON/DB'ye kaydedilir</span>
              </div>
              <div className="bg-white p-3 rounded-lg border border-line shadow-2xs">
                <Sparkles className="w-5 h-5 text-ai mx-auto mb-1" />
                <span className="font-bold block text-ink">3. Gemini 3.8 Flash</span>
                <span className="text-2xs text-ink-3">Tüm parçaları sentezler, 5 şıkkı ve çözümü üretir</span>
              </div>
              <div className="bg-white p-3 rounded-lg border border-line shadow-2xs">
                <Globe className="w-5 h-5 text-ok mx-auto mb-1" />
                <span className="font-bold block text-ink">4. Canlı Arayüz & Test</span>
                <span className="text-2xs text-ink-3">Tüm dönem arkadaşları soruyu çözer ve onaylar</span>
              </div>
            </div>
          </div>

          {/* The 4 Core Layers Explained */}
          <div className="space-y-4">
            <h4 className="text-sm font-bold text-ink border-b pb-1">
              Bu Sistemi Oluşturan 4 Temel Katman:
            </h4>

            {/* Layer 1: Frontend */}
            <div className="flex gap-3 items-start">
              <div className="p-2 rounded-lg bg-ok-soft text-ok shrink-0 font-bold">1</div>
              <div>
                <h5 className="font-bold text-ink text-xs">
                  Kullanıcı Arayüzü (Frontend - React & Tailwind CSS)
                </h5>
                <p className="text-ink-2 mt-0.5">
                  Öğrencilerin gördüğü butonlar, 1-100 soru haritası kutucukları, formlar ve soru kartlarıdır.
                  Kullanıcı "Hafızayı Ekle" veya "Şık Ekle" butonuna bastığında tarayıcı bu bilgiyi paketleyip sunucuya (Backend) iletir.
                </p>
              </div>
            </div>

            {/* Layer 2: Backend */}
            <div className="flex gap-3 items-start">
              <div className="p-2 rounded-lg bg-accent-soft text-accent shrink-0 font-bold">2</div>
              <div>
                <h5 className="font-bold text-ink text-xs">
                  Sunucu ve API Katmanı (Backend - Express.js)
                </h5>
                <p className="text-ink-2 mt-0.5">
                  Arka planda çalışan Node.js ve Express motorudur. Frontend'den gelen istekleri karşılar (<code className="bg-field px-1 py-0.5 rounded text-2xs">/api/questions</code>), veritabanına kaydeder ve gerektiğinde Google Gemini yapay zekasına güvenli bir şekilde bağlanır. API anahtarları asla tarayıcıya açık edilmez, sunucuda korunur.
                </p>
              </div>
            </div>

            {/* Layer 3: Database */}
            <div className="flex gap-3 items-start">
              <div className="p-2 rounded-lg bg-accent-soft text-accent shrink-0 font-bold">3</div>
              <div>
                <h5 className="font-bold text-ink text-xs">
                  Kalıcı Veritabanı Havuzu (Database - JSON / SQLite / Firestore)
                </h5>
                <p className="text-ink-2 mt-0.5">
                  Öğrencilerin girdiği her hafıza parçası, şık ve upvote bu havuzda saklanır. Sayfa yenilense veya sunucu yeniden başlasa bile veriler kaybolmaz. Bu uygulamada veriler <code className="bg-field px-1 py-0.5 rounded text-2xs">data/questions.json</code> dosyasında yapılandırılmış JSON veritabanı olarak güvenle saklanmaktadır.
                </p>
              </div>
            </div>

            {/* Layer 4: AI Engine */}
            <div className="flex gap-3 items-start">
              <div className="p-2 rounded-lg bg-ai-soft text-ai shrink-0 font-bold">4</div>
              <div>
                <h5 className="font-bold text-ink text-xs">
                  Yapay Zeka Rekonstrüksiyon Motoru (Google Gemini 3.8 Flash)
                </h5>
                <p className="text-ink-2 mt-0.5">
                  Öğrenciler farklı amfilerden farklı parçalar getirdiğinde (ör. biri "yaşlı adam otel kliması dedi", diğeri "sodyum düşüktü dedi", bir diğeri "şıkta Legionella vardı dedi"), Gemini bu parçaları tıbbi literatürle (Robbins, Katzung vb.) harmanlar; dilbilgisi kusursuz bir vaka sorusu, 5 tane birbiriyle çelişmeyen şık, doğru cevap ve doyurucu bir patofizyolojik açıklama üretir.
                </p>
              </div>
            </div>
          </div>

          {/* Tips for Medical Students */}
          <div className="bg-field border border-line rounded-xl p-4 space-y-2">
            <span className="font-bold text-ink text-xs block">
              Sınav Çıkışında Arkadaşlarınızla En Yüksek Verimi Almak İçin:
            </span>
            <ul className="space-y-1 text-ink-2 list-disc list-inside">
              <li>Sınavdan hemen sonra amfi WhatsApp grubuna sitenin linkini paylaşın.</li>
              <li>Her öğrenciye 5'er 10'ar soru paylaşımı yapın (ör: 1-15 Ali, 16-30 Zeynep).</li>
              <li>Tam hatırlayamasanız bile anahtar kelimeleri ve ilaç isimlerini ekleyin.</li>
              <li>2-3 girdi toplandığında <strong>"AI ile Rekonstrükte Et"</strong> butonuna basın, sistem anında soruyu ayağa kaldıracaktır!</li>
            </ul>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-field border-t border-line flex items-center justify-end">
          <button
            onClick={onClose}
            className="bg-ok hover:bg-ok text-white font-bold px-4 py-1.5 rounded-lg text-xs cursor-pointer"
          >
            Anladım, Soru Havuzuna Dön
          </button>
        </div>
      </div>
    </div>
  );
};
