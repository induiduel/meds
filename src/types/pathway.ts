/**
 * Dinamik Mekanizma ve Yolak Görselleştirme Tipleri
 * (Step-by-step Animated Pathway & Mechanism Player)
 */

export type PathwayNodeType =
  | 'substrate'       // Başlangıç maddesi (örn. Membran fosfolipidleri)
  | 'enzyme'          // Enzim / Katalizör (örn. Fosfolipaz A2, COX-1, 5-LOX)
  | 'intermediate'    // Ara ürün (örn. Araşidonik asit, PGG2/PGH2)
  | 'product'         // Son ürün / Mediyatör (örn. Tromboksan A2, PGI2, Lökotriyenler)
  | 'drug_inhibitor'  // İnhibitör ilaç / blokör (örn. Kortikosteroid, NSAİİ, Zileuton)
  | 'drug_activator'  // Uyarıcı / Agonist (örn. Bradikinin, Trombin)
  | 'receptor'        // Hücre yüzey veya sitoplazmik reseptör (örn. Fas, TNFR1, CysLT1)
  | 'cell'            // Hücre veya doku tipi (örn. Endotel, Trombosit, Nötrofil)
  | 'clinical_effect';// Klinik / Fizyopatolojik etki (örn. Vazodilatasyon, Trombosit agregasyonu)

export interface PathwayNode {
  id: string;
  label: string;
  sublabel?: string;
  type: PathwayNodeType;
  /** Konum koordinatları (0-100 arası yüzde) */
  x: number;
  y: number;
  /** İsteğe bağlı açıklama veya detay */
  tooltip?: string;
  /** Vurgu rengi veya özel etiket */
  badge?: string;
}

export type PathwayEdgeType =
  | 'conversion'   // Bir molekülün diğerine dönüşümü (ok)
  | 'inhibition'   // İnhibisyon / Blokaj (kırmızı T çizgisi: ⊣)
  | 'activation'   // Aktivasyon / Uyarım (yeşil + veya oklu)
  | 'synthesis';   // Sentez / Salınım

export interface PathwayEdge {
  id: string;
  from: string; // Kaynak node id
  to: string;   // Hedef node id
  type: PathwayEdgeType;
  label?: string;
  /** Eğrilik derecesi (-50 ile +50 arası) */
  curvature?: number;
}

export interface PathwayStep {
  stepNumber: number;
  title: string;
  subtitle?: string;
  /** Markdown destekli fizyopatolojik açıklama metni */
  description: string;
  /** EMA veya TTS tarafından seslendirilecek konuşma metni */
  narration: string;
  /** Bu aşamada odaklanılan / aydınlatılan düğümler */
  activeNodeIds: string[];
  /** Bu aşamada parlayan veya akışı gösterilen oklar */
  activeEdgeIds: string[];
  /** İsteğe bağlı: Bu adıma kadar ortaya çıkmış düğümler (kümülatif) */
  visibleNodeIds?: string[];
  /** Sınav spotu veya klinik püf noktası */
  spotlight?: string;
  /** Özel EMA mp3 ses dosyasının yolu varsa */
  audioUrl?: string;
  /** Otomatik video akışında bu adımın minimum bekleme süresi (saniye) */
  durationSeconds?: number;
}

export interface MechanismPathway {
  id: string;
  title: string;
  subtitle: string;
  discipline: string; // 'Patoloji' | 'Farmakoloji' | 'Biyokimya' vb.
  summary: string;
  nodes: PathwayNode[];
  edges: PathwayEdge[];
  steps: PathwayStep[];
  examPoints?: string[];
}
