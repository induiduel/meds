import React, { useEffect, useMemo, useRef, useState } from 'react';
import { CornerDownLeft, Sparkles, Wand2, ArrowRight, HelpCircle } from 'lucide-react';
import { ApiService } from '../../services/api';
import { smartComposerService, loadComposerModel, AssistOption, AssistResult } from '../../services/smartComposerService';

/**
 * MedSoru Akıllı Soru Yazma Yardımcısı (ComposerAssist)
 *
 *  - Masaüstü ve mobil tam ekran yazmada anlık (0ms-30ms) akıllı metin tamamlama,
 *    klinik vaka devamı ve güvenli yazım düzeltmesi.
 *  - Cümle İçi Devam (isExpanding) ile Soruyu Kapatma (isQuestionReady) ayrımını yapar:
 *    Kullanıcı vaka yazarken gereksizce "hangisidir?" ile soruyu kesmez; klinik devam önerir.
 *  - Bütün cümleyi dikkate alır (organ, semptom, hastalık, tetkik bağlamı).
 *  - Ayna katmanı (ca-mirror) textarea ile %100 piksel uyumlu hizalanır.
 *  - Tab ya da imleç sondayken → ile soluk hayalet metin (ghost) anında kabul edilir.
 */

export const ComposerAssist: React.FC<{
  active: boolean;
  value: string;
  onChange: (v: string) => void;
  textareaId: string;
  committeeId?: string;
}> = ({ active, value, onChange, textareaId, committeeId }) => {
  const [sources, setSources] = useState<string[]>([]);
  const [localResult, setLocalResult] = useState<AssistResult | null>(null);
  // Derlem modeli (ayrı parça) yüklenince önerileri yeniden hesapla
  const [modelReady, setModelReady] = useState(smartComposerService.hasModel());
  useEffect(() => {
    if (!active || modelReady) return;
    let alive = true;
    loadComposerModel().then(() => { if (alive) setModelReady(smartComposerService.hasModel()); });
    return () => { alive = false; };
  }, [active, modelReady]);
  const [box, setBox] = useState<{
    top: number;
    left: number;
    width: number;
    height: number;
    scroll: number;
    paddingTop: string;
    paddingRight: string;
    paddingBottom: string;
    paddingLeft: string;
    fontSize: string;
    fontFamily: string;
    lineHeight: string;
    letterSpacing: string;
  } | null>(null);

  const mirrorRef = useRef<HTMLDivElement>(null);
  const reqId = useRef(0);

  // 1. Anlık Yerel Hesaplama (30ms micro-debounce — sıfır kasma, anlık yanıt)
  useEffect(() => {
    if (!active || !value.trim()) {
      setLocalResult(null);
      return;
    }

    const t = window.setTimeout(() => {
      const res = smartComposerService.getAssist(value, sources);
      setLocalResult(res);
    }, 30);

    return () => window.clearTimeout(t);
  }, [value, active, sources, modelReady]);

  // 2. Arka Planda Çıkmış Soru Kaynaklarını Çekme (Non-blocking, UI thread'ini dondurmaz)
  useEffect(() => {
    if (!active || value.trim().length < 8) return;
    const currentId = ++reqId.current;
    const query = value.trim();

    const idleTimer = window.setTimeout(() => {
      // Arka planda benzer soruları sorgula; hata verirse sessizce yoksay
      // Sunucudaki benzer çıkmış soru araması (POST /api/past-questions/similar)
      ApiService.findSimilarPastQuestions(query.slice(-400), committeeId)
        .then((rows) => {
          if (currentId !== reqId.current) return;
          setSources(rows.slice(0, 5).map((x) => String(x.stem || '')).filter(Boolean));
        })
        .catch(() => {});
    }, 400);

    return () => window.clearTimeout(idleTimer);
  }, [value, active, committeeId]);

  // 2b. Yerel sözlük yazım hatası bulamazsa (ör. 5 harften kısa "Dwn") sunucunun derlem yazım önerisine sor
  const [serverSpell, setServerSpell] = useState<{ q: string; text: string; changes: { from: string; to: string }[] } | null>(null);
  const localHasSpell = !!localResult?.spell;
  useEffect(() => {
    const q = value;
    if (!active || localHasSpell || q.trim().split(/\s+/).length < 2) { setServerSpell(null); return; }
    const ctrl = new AbortController();
    const t = window.setTimeout(() => {
      ApiService.suggestSpelling(q, ctrl.signal).then((r) => {
        if (ctrl.signal.aborted) return;
        setServerSpell(r?.text && r.text !== q && r.changes?.length ? { q, text: r.text, changes: r.changes } : null);
      });
    }, 400);
    return () => { ctrl.abort(); window.clearTimeout(t); };
  }, [value, active, localHasSpell]);

  // 3. Ayna Katmanı (ca-mirror) Textarea ile Birebir Piksel Eşleme
  useEffect(() => {
    if (!active) {
      setBox(null);
      return;
    }
    const ta = document.getElementById(textareaId) as HTMLTextAreaElement | null;
    if (!ta) return;

    const measure = () => {
      const cs = window.getComputedStyle(ta);
      setBox({
        top: ta.offsetTop,
        left: ta.offsetLeft,
        width: ta.offsetWidth,
        height: ta.offsetHeight,
        scroll: ta.scrollTop,
        paddingTop: cs.paddingTop,
        paddingRight: cs.paddingRight,
        paddingBottom: cs.paddingBottom,
        paddingLeft: cs.paddingLeft,
        fontSize: cs.fontSize,
        fontFamily: cs.fontFamily,
        lineHeight: cs.lineHeight,
        letterSpacing: cs.letterSpacing,
      });
    };

    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(ta);
    ta.addEventListener('scroll', measure);

    // Tab veya imleç en sondayken ArrowRight tuşuyla hayalet metni kabul et
    const onKey = (e: KeyboardEvent) => {
      const g = ta.dataset.ghost || '';
      if (!g) return;
      const atEnd = ta.selectionStart === ta.value.length && ta.selectionEnd === ta.value.length;
      if (e.key === 'Tab' || (e.key === 'ArrowRight' && atEnd)) {
        e.preventDefault();
        accept(g);
      }
    };

    ta.addEventListener('keydown', onKey);
    return () => {
      ro.disconnect();
      ta.removeEventListener('scroll', measure);
      ta.removeEventListener('keydown', onKey);
    };
  }, [active, textareaId, onChange]);

  const ghost = localResult?.ghost || '';

  // Kabul kısayolu için hayalet metni textarea dataset'ine iliştir
  useEffect(() => {
    const ta = document.getElementById(textareaId) as HTMLTextAreaElement | null;
    if (ta) ta.dataset.ghost = active ? ghost : '';
  }, [ghost, active, textareaId]);

  if (!active || !value.trim()) return null;

  const accept = (textToAdd: string) => {
    onChange(value + textToAdd);
    const ta = document.getElementById(textareaId) as HTMLTextAreaElement | null;
    ta?.focus();
    window.setTimeout(() => {
      if (ta) {
        const nextLen = ta.value.length;
        ta.setSelectionRange(nextLen, nextLen);
      }
    }, 0);
  };

  const options = localResult?.options || [];
  // Sunucu önerisi yalnız tam o metin için geçerli (yazmaya devam edilince eski öneri uygulanmaz)
  const spell = localResult?.spell || (serverSpell && serverSpell.q === value ? serverSpell : null);
  let fix = localResult?.fix || null;
  if (spell && !localResult?.spell) {
    // Sunucu yazım düzeltmesini noktalama düzeltmesiyle birleştir
    const punct = smartComposerService.getPunctuationFix(value, spell.text);
    const sc = spell.changes.map((c) => `${c.from} → ${c.to}`);
    fix = punct ? { text: punct.text, changes: [...sc, ...punct.changes] } : { text: spell.text, changes: sc };
  }

  // Düzeltme seçeneği: hem noktalama hem yazım hatalarını birleştirir
  const activeFix = fix || (spell ? { text: spell.text, changes: spell.changes.map((c) => `${c.from} → ${c.to}`) } : null);

  const hasItems = options.length > 0 || !!activeFix;

  return (
    <>
      {/* 1. Piksel Uyumlu Hayalet Metin Katmanı (Ghost Text Overlay) */}
      {box && ghost && (
        <div
          ref={mirrorRef}
          className="ca-mirror"
          aria-hidden
          style={{
            top: box.top,
            left: box.left,
            width: box.width,
            height: box.height,
            paddingTop: box.paddingTop,
            paddingRight: box.paddingRight,
            paddingBottom: box.paddingBottom,
            paddingLeft: box.paddingLeft,
            fontSize: box.fontSize,
            fontFamily: box.fontFamily,
            lineHeight: box.lineHeight,
            letterSpacing: box.letterSpacing,
          }}
        >
          <div style={{ transform: `translateY(${-box.scroll}px)` }}>
            <span className="ca-typed">{value}</span>
            <button
              type="button"
              tabIndex={-1}
              className="ca-ghost"
              onPointerDown={(e) => {
                e.preventDefault();
                accept(ghost);
              }}
              title="Kabul etmek için Tab veya ⇥ tuşuna basın"
            >
              {ghost}
            </button>
          </div>
        </div>
      )}

      {/* 2. Akıllı Öneri Çubuğu (Toolbar & Chips) */}
      <div
        className={`ca-bar ${hasItems ? 'is-on' : ''}`}
        role="toolbar"
        aria-label="Akıllı tıp yazma ve tamamlama önerileri"
      >
        {/* Güvenli Yazım & Biçim Düzeltme Çipi */}
        {activeFix && (
          <button
            type="button"
            className="ca-chip is-fix"
            onPointerDown={(e) => e.preventDefault()}
            onClick={() => onChange(activeFix.text)}
            title={`Yazımı düzelt: ${activeFix.changes.join(', ')}`}
          >
            <Wand2 aria-hidden className="w-3.5 h-3.5 text-ai shrink-0" />
            <span className="ca-fix-l">Düzelt</span>
            <span className="ca-fix-d">
              {activeFix.changes.slice(0, 2).join(' · ')}
              {activeFix.changes.length > 2 ? ` +${activeFix.changes.length - 2}` : ''}
            </span>
          </button>
        )}

        {/* Cümle İçi Devam ve Soru Kapatma Çipleri */}
        {options.map((opt, i) => {
          const isContinue = opt.type === 'continue';
          const isComplete = opt.type === 'complete';
          const isTop = opt.isTop || i === 0;

          return (
            <button
              key={`${opt.type}-${opt.text}-${i}`}
              type="button"
              className={`ca-chip ${isTop ? 'is-top' : ''} ${isContinue ? 'is-continue' : ''} ${isComplete ? 'is-complete' : ''}`}
              onPointerDown={(e) => e.preventDefault()}
              onClick={() => accept(opt.text)}
              title={isContinue ? 'Klinik vaka anlatımına devam et' : 'Soruyu bu kök ile tamamla'}
            >
              {isContinue ? (
                <ArrowRight aria-hidden className="w-3.5 h-3.5 text-accent shrink-0" />
              ) : isComplete ? (
                <HelpCircle aria-hidden className="w-3.5 h-3.5 text-ai shrink-0" />
              ) : (
                <Sparkles aria-hidden className="w-3.5 h-3.5 text-ink-3 shrink-0" />
              )}

              <span className={`ca-badge ${isContinue ? 'is-continue' : isComplete ? 'is-complete' : ''}`}>
                {opt.label}
              </span>

              <span>{opt.preview}</span>

              {isTop && (
                <CornerDownLeft aria-hidden className="w-3 h-3 text-ink-3 opacity-60 ml-auto shrink-0 hidden sm:inline" />
              )}
            </button>
          );
        })}
      </div>
    </>
  );
};
