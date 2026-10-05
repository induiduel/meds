import React, { useState } from 'react';
import { X } from 'lucide-react';

const KEY = 'medsor_love_note_hidden_v1';

/** Ana ekranda kapatılabilen sevgi notu: SVG + CSS ile Lottie benzeri kalp animasyonu. */
export const LoveNote: React.FC = () => {
  const [hidden, setHidden] = useState(() => {
    try { return localStorage.getItem(KEY) === '1'; } catch { return false; }
  });
  if (hidden) return null;

  return (
    <section className="ms-love" aria-label="Arzu Türk için sevgi notu">
      <div className="ms-love-art" aria-hidden="true">
        <svg viewBox="0 0 120 100" className="ms-love-svg">
          <path className="ms-love-big" d="M60 88 C20 62 8 42 18 26 C27 12 46 13 60 30 C74 13 93 12 102 26 C112 42 100 62 60 88 Z" />
          <path className="ms-love-line" d="M8 52 H34 L40 40 L48 64 L56 46 L62 52 H112" />
        </svg>
        {[0, 1, 2, 3, 4, 5].map((i) => (
          <span key={i} className="ms-love-float" style={{ left: `${10 + i * 15}%`, animationDelay: `${i * 0.55}s` }}>♥</span>
        ))}
      </div>
      <div className="min-w-0 flex-1">
        <p className="ms-love-to">Arzu Türk'e</p>
        <p className="ms-love-msg">
          Bu satırların arasında, her sorunun ve her slaytın arkasında hep sen varsın. İyi ki varsın,
          iyi ki yanımdasın. Seni çok seviyorum.
        </p>
      </div>
      <button
        type="button"
        onClick={() => { setHidden(true); try { localStorage.setItem(KEY, '1'); } catch { /* gizli pencere */ } }}
        aria-label="Notu kapat"
        className="ms-love-close"
      >
        <X className="w-4 h-4" />
      </button>
    </section>
  );
};
