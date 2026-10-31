/**
 * KMB sahne kitaplığı — ORTAK sözleşme (tipler, degrade tanımları, boru yardımcısı). Sahne dosyaları
 * (sahneler.tsx, sahneler_2b_*.tsx) buradan alır; döngüsel içe aktarma olmaz. 2B düz çizgi film stili: docs/KMB_2B_STIL.md.
 */
import React from 'react';

export type OgeDurum = { gor?: boolean; renk?: string; vurgu?: number; etiket?: boolean; ciz?: number };
export type SahneDurum = Record<string, OgeDurum>;
export type OgeProps = (id: string) => Record<string, unknown>;

export type Sahne = {
  ad: string;
  zemin?: string;
  gizli: string[];
  etiket: Record<string, [number, number, string]>;
  Ciz: React.FC<{ o: OgeProps }>;
};

export const u = (id: string) => `url(#kmb-${id})`;

/** Ortak degrade ve süzgeçler — her sahne SVG'sine bir kez eklenir */
export function Ortak() {
  return (
    <defs>
      <radialGradient id="kmb-zemin-klinik" cx="50%" cy="40%" r="75%">
        <stop offset="0" stopColor="#fbfcfd" /><stop offset="1" stopColor="#e4e9ef" />
      </radialGradient>
      <linearGradient id="kmb-zemin-tepsi" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#dfe6ec" /><stop offset="1" stopColor="#c7d1da" />
      </linearGradient>
      <radialGradient id="kmb-deri" cx="45%" cy="35%" r="70%">
        <stop offset="0" stopColor="#f6d6bd" /><stop offset=".7" stopColor="#e9b896" /><stop offset="1" stopColor="#d49a76" />
      </radialGradient>
      <linearGradient id="kmb-deri-kesit" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#e8b493" /><stop offset="1" stopColor="#f3cdb1" />
      </linearGradient>
      <linearGradient id="kmb-yag" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#f6e3a6" /><stop offset="1" stopColor="#efd283" />
      </linearGradient>
      <linearGradient id="kmb-kas" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#b5524a" /><stop offset=".5" stopColor="#cf6b5f" /><stop offset="1" stopColor="#a8463f" />
      </linearGradient>
      <radialGradient id="kmb-kemik" cx="40%" cy="35%" r="75%">
        <stop offset="0" stopColor="#fbf6e9" /><stop offset=".75" stopColor="#eadfc4" /><stop offset="1" stopColor="#cdbd98" />
      </radialGradient>
      <radialGradient id="kmb-ilik" cx="50%" cy="50%" r="60%">
        <stop offset="0" stopColor="#e9c9a0" /><stop offset="1" stopColor="#d9b07e" />
      </radialGradient>
      <radialGradient id="kmb-mesane" cx="40%" cy="35%" r="75%">
        <stop offset="0" stopColor="#f6c2bb" /><stop offset=".7" stopColor="#e39a92" /><stop offset="1" stopColor="#c8746c" />
      </radialGradient>
      <radialGradient id="kmb-idrar" cx="45%" cy="40%" r="70%">
        <stop offset="0" stopColor="#fff3b8" /><stop offset="1" stopColor="#f2cf55" />
      </radialGradient>
      <linearGradient id="kmb-idrar-torba" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#f8dd6c" stopOpacity=".85" /><stop offset="1" stopColor="#e7b82e" stopOpacity=".95" />
      </linearGradient>
      <radialGradient id="kmb-prostat" cx="40%" cy="35%" r="75%">
        <stop offset="0" stopColor="#e7b3a0" /><stop offset="1" stopColor="#b97a66" />
      </radialGradient>
      <linearGradient id="kmb-rektum" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#b98a77" /><stop offset=".5" stopColor="#d6a995" /><stop offset="1" stopColor="#ad7c69" />
      </linearGradient>
      <linearGradient id="kmb-korpus" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#c9787a" /><stop offset=".5" stopColor="#e0999a" /><stop offset="1" stopColor="#b9686b" />
      </linearGradient>
      <linearGradient id="kmb-spongiosum" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#e8a9a6" /><stop offset="1" stopColor="#cf8784" />
      </linearGradient>
      <radialGradient id="kmb-glans" cx="40%" cy="35%" r="75%">
        <stop offset="0" stopColor="#f2b4ae" /><stop offset="1" stopColor="#c97c77" />
      </radialGradient>
      <radialGradient id="kmb-testis" cx="40%" cy="35%" r="70%">
        <stop offset="0" stopColor="#f3e0dc" /><stop offset="1" stopColor="#cfa7a1" />
      </radialGradient>
      <radialGradient id="kmb-mukoza" cx="50%" cy="40%" r="70%">
        <stop offset="0" stopColor="#f2a9a6" /><stop offset="1" stopColor="#c86e6c" />
      </radialGradient>
      <radialGradient id="kmb-bagirsak" cx="40%" cy="35%" r="70%">
        <stop offset="0" stopColor="#f3d0c3" /><stop offset="1" stopColor="#d9a594" />
      </radialGradient>
      {/* kateter: silindir ışığı */}
      <linearGradient id="kmb-lateks" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#c99a2c" /><stop offset=".3" stopColor="#f6d77a" /><stop offset=".55" stopColor="#e9bd47" /><stop offset="1" stopColor="#a87b1d" />
      </linearGradient>
      <linearGradient id="kmb-silikon" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#b9c3cf" /><stop offset=".3" stopColor="#ffffff" /><stop offset=".6" stopColor="#e6ebf1" /><stop offset="1" stopColor="#9aa6b4" />
      </linearGradient>
      <linearGradient id="kmb-plastik" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#eef3f8" stopOpacity=".95" /><stop offset=".5" stopColor="#ffffff" stopOpacity=".7" /><stop offset="1" stopColor="#c9d3de" stopOpacity=".95" />
      </linearGradient>
      <linearGradient id="kmb-torba" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#e9eef3" stopOpacity=".9" /><stop offset=".4" stopColor="#ffffff" stopOpacity=".75" /><stop offset="1" stopColor="#d3dbe4" stopOpacity=".9" />
      </linearGradient>
      <linearGradient id="kmb-metal" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#8b96a3" /><stop offset=".4" stopColor="#eef2f6" /><stop offset="1" stopColor="#6d7884" />
      </linearGradient>
      <linearGradient id="kmb-eldiven" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#d9e8f8" /><stop offset="1" stopColor="#9fbfe3" />
      </linearGradient>
      <linearGradient id="kmb-eldiven-steril" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#fbf3e6" /><stop offset="1" stopColor="#e7d3b3" />
      </linearGradient>
      <linearGradient id="kmb-ortu" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#5f9fd6" /><stop offset="1" stopColor="#3b7bb8" />
      </linearGradient>
      <linearGradient id="kmb-povidon" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#7a3410" /><stop offset=".5" stopColor="#b5551d" /><stop offset="1" stopColor="#6d2c0c" />
      </linearGradient>
      <linearGradient id="kmb-us-isin" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#7fb8ff" stopOpacity=".55" /><stop offset="1" stopColor="#7fb8ff" stopOpacity="0" />
      </linearGradient>
      <linearGradient id="kmb-yatak" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#f4f7fa" /><stop offset="1" stopColor="#d6dee7" />
      </linearGradient>
      <linearGradient id="kmb-onluk" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#8fc1c9" /><stop offset="1" stopColor="#5e9aa5" />
      </linearGradient>
      <linearGradient id="kmb-beyaz-onluk" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#ffffff" /><stop offset="1" stopColor="#d5dde6" />
      </linearGradient>
      {/* ——— 2B düz çizgi film paleti (2026-11-01, docs/KMB_2B_STIL.md): yumuşak iki duraklı degrade, kontur rengi yorumda ——— */}
      <linearGradient id="kmb-2b-deri" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#f3c8a3" /><stop offset="1" stopColor="#e2a37c" /></linearGradient>{/* kontur #b9805a */}
      <linearGradient id="kmb-2b-deri-koyu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#e9b48d" /><stop offset="1" stopColor="#d18f68" /></linearGradient>
      <radialGradient id="kmb-2b-mesane" cx="45%" cy="40%" r="70%"><stop offset="0" stopColor="#c9655a" /><stop offset="1" stopColor="#a8433a" /></radialGradient>{/* kontur #7a2e26 */}
      <radialGradient id="kmb-2b-idrar" cx="45%" cy="35%" r="75%"><stop offset="0" stopColor="#fbe58a" /><stop offset="1" stopColor="#efc53f" /></radialGradient>
      <linearGradient id="kmb-2b-kateter" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#f7c75a" /><stop offset="1" stopColor="#d9962a" /></linearGradient>{/* kontur #b47a1a */}
      <linearGradient id="kmb-2b-silikon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#ffffff" /><stop offset="1" stopColor="#dde4ec" /></linearGradient>{/* kontur #8a96a6 */}
      <radialGradient id="kmb-2b-balon" cx="40%" cy="35%" r="70%"><stop offset="0" stopColor="#ffffff" /><stop offset="1" stopColor="#d7dee6" /></radialGradient>{/* kontur #2e9e5b (doğru) */}
      <linearGradient id="kmb-2b-ortu" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#5aa893" /><stop offset="1" stopColor="#3f8a76" /></linearGradient>{/* kontur #2f6f5f */}
      <linearGradient id="kmb-2b-yatak" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#9fd3d6" /><stop offset="1" stopColor="#6fb4b9" /></linearGradient>{/* kontur #4f9aa0 */}
      <linearGradient id="kmb-2b-eldiven" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#dcedf9" /><stop offset="1" stopColor="#b3d4ec" /></linearGradient>{/* kontur #3f6f9c (mavi nitril) */}
      <linearGradient id="kmb-2b-eldiven-steril" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#fbf3e6" /><stop offset="1" stopColor="#e7d3b3" /></linearGradient>{/* kontur #b59c72 */}
      <radialGradient id="kmb-2b-mukoza" cx="50%" cy="40%" r="70%"><stop offset="0" stopColor="#f0a8a4" /><stop offset="1" stopColor="#d07f7b" /></radialGradient>{/* kontur #a85f5a */}
      <radialGradient id="kmb-2b-prostat" cx="40%" cy="35%" r="75%"><stop offset="0" stopColor="#e2a48c" /><stop offset="1" stopColor="#c98468" /></radialGradient>{/* kontur #9a5a44 */}
      <radialGradient id="kmb-2b-kemik" cx="40%" cy="35%" r="75%"><stop offset="0" stopColor="#f7efdd" /><stop offset="1" stopColor="#e6d7b4" /></radialGradient>{/* kontur #b9a479 */}
      <linearGradient id="kmb-2b-kas" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stopColor="#d26a5f" /><stop offset="1" stopColor="#b6514a" /></linearGradient>{/* kontur #8d2f28 */}
      <linearGradient id="kmb-2b-metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#dfe6ee" /><stop offset="1" stopColor="#aeb9c6" /></linearGradient>{/* kontur #5b6676 */}
      <linearGradient id="kmb-2b-plastik" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#f4f8fc" /><stop offset="1" stopColor="#d8e2ec" /></linearGradient>{/* kontur #6b7a90 */}
      <linearGradient id="kmb-2b-kuvet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#4f94d6" /><stop offset="1" stopColor="#3570b3" /></linearGradient>{/* kontur #1f4e79 */}
      <linearGradient id="kmb-2b-onluk" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#8fc1c9" /><stop offset="1" stopColor="#5e9aa5" /></linearGradient>{/* kontur #3f7680 */}
      <linearGradient id="kmb-2b-jel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#bfe0ff" stopOpacity=".75" /><stop offset="1" stopColor="#8fc7ff" stopOpacity=".6" /></linearGradient>
      <filter id="kmb-golge" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="3" stdDeviation="3.5" floodColor="#1d2733" floodOpacity=".22" />
      </filter>
      <filter id="kmb-yumusak" x="-10%" y="-10%" width="120%" height="120%">
        <feGaussianBlur stdDeviation="1.2" />
      </filter>
      <pattern id="kmb-kil" width="9" height="9" patternUnits="userSpaceOnUse">
        <path d="M2 7 q1 -4 3 -5" stroke="#6b4a33" strokeWidth=".9" fill="none" opacity=".5" />
      </pattern>
      <marker id="kmb-ok" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M0 0 L10 5 L0 10 Z" fill="#2f6fd6" />
      </marker>
    </defs>
  );
}

/** Silindir boru (kateter, hortum): gövde + ince parlama */
export const Boru = ({ d, g = 'lateks', w = 10, cz = false, cls = 'boya-cizgi' }: { d: string; g?: string; w?: number; cz?: boolean; cls?: string }) => (
  <>
    <path d={d} stroke="#5a4a2a" strokeOpacity={0.35} strokeWidth={w + 2} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    <path className={`${cz ? 'cz ' : ''}${cls}`} pathLength={cz ? 1 : undefined} d={d} stroke={g === 'lateks' ? '#e3b544' : g === 'silikon' ? '#eef2f6' : '#dfe6ee'} strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    <path d={d} stroke="#fff" strokeOpacity={0.55} strokeWidth={Math.max(1.5, w / 4)} fill="none" strokeLinecap="round" strokeLinejoin="round" transform={`translate(0 ${-w / 4})`} />
  </>
);

