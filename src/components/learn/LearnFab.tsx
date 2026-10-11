import React from 'react';

interface LearnFabProps {
  children: React.ReactNode;
  /** Eski hızlı eylem menüsünün bağlantıları; çağıran (App.tsx) değişmesin diye kabul edilir */
  onOpenGlossary?: () => void;
  onOpenPdf?: () => void;
}

/**
 * Öğren sekmesinin kabuğu. v9'da telefondaki yüzen "+" hızlı eylem düğmesi (tam ekran, başa dön, sözlük,
 * PDF) kaldırıldı: alt gezinmenin ortasındaki birincil "+ Ekle" ile karışıyordu. Bu eylemler ders içindeki
 * Araçlar menüsünde ve deste satırlarında (PDF) duruyor.
 */
export const LearnFab: React.FC<LearnFabProps> = ({ children }) => <div>{children}</div>;
