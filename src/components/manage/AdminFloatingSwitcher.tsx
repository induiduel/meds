import React, { useState, useEffect } from 'react';
import { ShieldCheck, SlidersHorizontal, ChevronUp, ChevronDown, Database, Users, Activity } from 'lucide-react';
import type { AppRoute } from '../../router';
import { writeLocation } from '../../router';
import { realtimeEventService, type RealtimeConnectionStatus } from '../../services/realtimeEvents';
import { getPanelTarget, isAdminAppMode } from '../../config/deployment';

interface ContextualAdminLink {
  slug: string;
  label: string;
}

function getContextualAdminTarget(route: AppRoute): ContextualAdminLink {
  switch (route) {
    case 'canli_ders':
      return { slug: 'sesli-anlatim', label: 'Sesli Anlatım Yönetimi' };
    case 'learn':
      return { slug: 'veri-katalogu', label: 'Deste & Katalog Yönetimi' };
    case 'questions':
    case 'quick_add':
    case 'hub_sorular':
      return { slug: 'soru-havuzu', label: 'Soru Havuzu Yönetimi' };
    case 'past_exams':
    case 'cikmis_cozucu':
      return { slug: 'veri-katalogu', label: 'Çıkmış Soru Verisi' };
    case 'kamp':
    case 'hub_kamplar':
    case 'son_prova':
      return { slug: 'kamp-tuyolari', label: 'Kamp Tüyoları Yönetimi' };
    case 'leaderboard':
    case 'basarimlar':
      return { slug: 'puan-atp', label: 'Puan & ATP Yönetimi' };
    case 'olasi_sorular':
      return { slug: 'serbest-girdiler', label: 'Serbest Girdiler' };
    case 'glossary':
    case 'diseases':
    case 'summaries':
      return { slug: 'veri-katalogu', label: 'Veri Kataloğunda Aç' };
    default:
      return { slug: 'genel-bakis', label: 'Genel Bakış Panosu' };
  }
}

export const AdminFloatingSwitcher: React.FC<{
  activeTab: AppRoute;
  onGoManage: (slug?: string) => void;
  visible: boolean;
}> = ({ activeTab, onGoManage, visible }) => {
  const [collapsed, setCollapsed] = useState<boolean>(() => {
    try { return localStorage.getItem('medsoru_admin_float_collapsed') === '1'; } catch { return false; }
  });
  const [liveStatus, setLiveStatus] = useState<RealtimeConnectionStatus>(() => realtimeEventService.getStatus());

  useEffect(() => {
    return realtimeEventService.onStatusChange(setLiveStatus);
  }, []);

  if (!visible || activeTab === 'manage' || activeTab === 'admin' || activeTab === 'practice') {
    return null;
  }

  const ctx = getContextualAdminTarget(activeTab);
  const target = getPanelTarget();
  const inAppMode = isAdminAppMode();

  const toggleCollapse = () => {
    const next = !collapsed;
    setCollapsed(next);
    try { localStorage.setItem('medsoru_admin_float_collapsed', next ? '1' : '0'); } catch { /* */ }
  };

  const jumpToSection = (slug: string) => {
    try {
      localStorage.setItem('medsoru_manage_section', slug);
    } catch { /* */ }
    writeLocation('manage', slug);
    onGoManage(slug);
  };

  if (collapsed) {
    return (
      <div
        className="fixed z-[85] right-3 bottom-[76px] sm:bottom-4 flex items-center gap-1 bg-[var(--color-ink)] text-[var(--color-white)] rounded-full shadow-xl border border-white/15 p-1"
        role="region"
        aria-label="Hızlı Yönetim Çubuğu"
      >
        <button
          type="button"
          onClick={() => jumpToSection('genel-bakis')}
          className="flex items-center gap-1.5 h-8 px-3 rounded-full bg-[var(--color-accent)] text-white text-xs font-bold cursor-pointer border-0"
          title="Yönetim Konsoluna Dön"
        >
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Yönetim</span>
        </button>
        <button
          type="button"
          onClick={toggleCollapse}
          className="w-7 h-7 rounded-full flex items-center justify-center bg-transparent text-white/80 hover:text-white cursor-pointer border-0"
          aria-label="Yönetim araçlarını genişlet"
          title="Genişlet"
        >
          <ChevronUp className="w-3.5 h-3.5" />
        </button>
      </div>
    );
  }

  return (
    <div
      className="fixed z-[85] right-3 bottom-[76px] sm:bottom-4 flex flex-wrap items-center gap-1.5 bg-[var(--color-ink)] text-[var(--color-white)] rounded-2xl shadow-2xl border border-white/15 px-2.5 py-1.5 max-w-[calc(100vw-24px)]"
      role="region"
      aria-label="Hızlı Yönetim Denetim Çubuğu"
    >
      <button
        type="button"
        onClick={() => jumpToSection('genel-bakis')}
        className="flex items-center gap-1.5 h-8 px-3 rounded-xl bg-[var(--color-accent)] text-white text-xs font-bold cursor-pointer border-0 shrink-0"
        title="Yönetim Konsoluna Dön (/manage)"
      >
        <ShieldCheck className="w-3.5 h-3.5" />
        <span>{inAppMode ? 'Yönetim Konsolu' : 'Yönetim'}</span>
      </button>

      <button
        type="button"
        onClick={() => jumpToSection(ctx.slug)}
        className="flex items-center gap-1.5 h-8 px-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-medium cursor-pointer border-0 shrink-0"
        title={`Bu ekranın yönetim bölümünü aç: ${ctx.label}`}
      >
        <SlidersHorizontal className="w-3.5 h-3.5" />
        <span className="truncate max-w-[140px]">{ctx.label}</span>
      </button>

      <button
        type="button"
        onClick={() => jumpToSection('kisiler')}
        className="hidden xs:flex items-center gap-1 h-8 px-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs cursor-pointer border-0"
        title="Canlı Kişiler & Çevrimiçi Öğrenciler"
      >
        <Users className="w-3.5 h-3.5" />
      </button>

      <button
        type="button"
        onClick={() => jumpToSection('veritabani-gezgini')}
        className="hidden xs:flex items-center gap-1 h-8 px-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs cursor-pointer border-0"
        title="meds-pg Veritabanı Gezgini"
      >
        <Database className="w-3.5 h-3.5" />
      </button>

      <button
        type="button"
        onClick={() => jumpToSection('hat')}
        className="hidden sm:flex items-center gap-1 h-8 px-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs cursor-pointer border-0"
        title="Hat Panosu & Otomasyon"
      >
        <Activity className="w-3.5 h-3.5" />
      </button>

      <span
        className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] bg-white/10 text-white/85"
        title={`Hedef: ${target === 'oracle' ? 'Canlı (Oracle)' : 'Yerel'} · Kanal: ${liveStatus}`}
      >
        <span
          className={`w-2 h-2 rounded-full ${
            liveStatus === 'connected' ? 'bg-emerald-400' : liveStatus === 'connecting' ? 'bg-amber-400' : 'bg-rose-400'
          }`}
        />
        <span>{target === 'oracle' ? 'Canlı' : 'Yerel'}</span>
      </span>

      <button
        type="button"
        onClick={toggleCollapse}
        className="w-7 h-7 rounded-lg flex items-center justify-center bg-transparent text-white/70 hover:text-white cursor-pointer border-0"
        aria-label="Çubuğu küçült"
        title="Küçült"
      >
        <ChevronDown className="w-3.5 h-3.5" />
      </button>
    </div>
  );
};
