/**
 * v16 ikon ara modülü (vite.config.ts › v16LucideEklentisi): uygulamadaki tüm `from 'lucide-react'` içe aktarmaları buraya
 * yönlenir. lucide'in her şeyi aynen geçer; v16 setinde karşılığı olan ikonlar `v16Ikonlu` ile sarılır — v16 açıkken
 * (yalnız yönetici denemesi) tuvaldeki çizim, kapalıyken lucide. Bu dosyanın kendi `lucide-react` isteği gerçek pakete gider.
 * Bilinçli olarak eşlenmeyenler: Flag (hata bildir anlamı), Layers, Sparkles, dolu daire ikonları (CheckCircle2 vb.), Loader2 (döner).
 */
import {
  AlertTriangle as L1, ArrowLeft as L2, Bell as L3, BookOpen as L4, Check as L5, ChevronDown as L6, ChevronLeft as L7,
  ChevronRight as L8, ChevronUp as L9, CircleHelp as L10, Clock as L11, Copy as L12, Dna as L13, Download as L14, FileText as L15,
  Gamepad2 as L16, Headphones as L17, Heart as L18, HelpCircle as L19, House as L20, Info as L21, LayoutGrid as L22, Library as L23,
  Lightbulb as L24, LineChart as L25, List as L26, ListOrdered as L27, Lock as L28, MessageCircle as L29, MessageSquare as L30,
  MessagesSquare as L31, Minus as L32, MoreHorizontal as L33, Pause as L34, Pencil as L35, PenTool as L36, Play as L37, Plus as L38,
  RotateCcw as L39, RotateCw as L40, Search as L41, Send as L42, ShieldCheck as L43, SkipBack as L44, SkipForward as L45,
  SlidersHorizontal as L46, Star as L47, Stethoscope as L48, Target as L49, Timer as L50, Trash2 as L51, TriangleAlert as L52,
  Trophy as L53, User as L54, UserRound as L55, X as L56, Zap as L57,
} from 'lucide-react';
import { v16Ikonlu } from './Ikon';

export * from 'lucide-react';

export const AlertTriangle = v16Ikonlu(L1, 'uyari');
export const ArrowLeft = v16Ikonlu(L2, 'geri');
export const Bell = v16Ikonlu(L3, 'zil');
export const BookOpen = v16Ikonlu(L4, 'kitap');
export const Check = v16Ikonlu(L5, 'tik');
export const ChevronDown = v16Ikonlu(L6, 'asagi');
export const ChevronLeft = v16Ikonlu(L7, 'geri');
export const ChevronRight = v16Ikonlu(L8, 'sag');
export const ChevronUp = v16Ikonlu(L9, 'yukari');
export const CircleHelp = v16Ikonlu(L10, 'soru');
export const Clock = v16Ikonlu(L11, 'saat');
export const Copy = v16Ikonlu(L12, 'kart');
export const Dna = v16Ikonlu(L13, 'dna');
export const Download = v16Ikonlu(L14, 'indir');
export const FileText = v16Ikonlu(L15, 'not');
export const Gamepad2 = v16Ikonlu(L16, 'oyun');
export const Headphones = v16Ikonlu(L17, 'kulak');
export const Heart = v16Ikonlu(L18, 'kalp');
export const HelpCircle = v16Ikonlu(L19, 'soru');
export const House = v16Ikonlu(L20, 'ev');
export const Info = v16Ikonlu(L21, 'bilgi');
export const LayoutGrid = v16Ikonlu(L22, 'izgara');
export const Library = v16Ikonlu(L23, 'klasor');
export const Lightbulb = v16Ikonlu(L24, 'isik');
export const LineChart = v16Ikonlu(L25, 'grafik');
export const List = v16Ikonlu(L26, 'liste');
export const ListOrdered = v16Ikonlu(L27, 'liste');
export const Lock = v16Ikonlu(L28, 'kilit');
export const MessageCircle = v16Ikonlu(L29, 'sohbet');
export const MessageSquare = v16Ikonlu(L30, 'sohbet');
export const MessagesSquare = v16Ikonlu(L31, 'sohbet');
export const Minus = v16Ikonlu(L32, 'eksi');
export const MoreHorizontal = v16Ikonlu(L33, 'daha');
export const Pause = v16Ikonlu(L34, 'duraklat');
export const Pencil = v16Ikonlu(L35, 'kalem');
export const PenTool = v16Ikonlu(L36, 'kalem');
export const Play = v16Ikonlu(L37, 'oynat');
export const Plus = v16Ikonlu(L38, 'arti');
export const RotateCcw = v16Ikonlu(L39, 'geri10');
export const RotateCw = v16Ikonlu(L40, 'ileri10');
export const Search = v16Ikonlu(L41, 'ara');
export const Send = v16Ikonlu(L42, 'gonder');
export const ShieldCheck = v16Ikonlu(L43, 'kalkan');
export const SkipBack = v16Ikonlu(L44, 'onceki');
export const SkipForward = v16Ikonlu(L45, 'sonraki');
export const SlidersHorizontal = v16Ikonlu(L46, 'ayar');
export const Star = v16Ikonlu(L47, 'yildiz');
export const Stethoscope = v16Ikonlu(L48, 'steto');
export const Target = v16Ikonlu(L49, 'hedef');
export const Timer = v16Ikonlu(L50, 'saat');
export const Trash2 = v16Ikonlu(L51, 'cop');
export const TriangleAlert = v16Ikonlu(L52, 'uyari');
export const Trophy = v16Ikonlu(L53, 'kupa');
export const User = v16Ikonlu(L54, 'kisi');
export const UserRound = v16Ikonlu(L55, 'kisi');
export const X = v16Ikonlu(L56, 'kapat');
export const Zap = v16Ikonlu(L57, 'simsek');
