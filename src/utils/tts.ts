// Ortak seslendirme: öncelikle EMA Lightning ses dosyası (/api/ogren-ses/); bulunamazsa /api/tts veya tarayıcı sesine düşer.
import { getCustomApiUrl } from '../services/api';

let audio: HTMLAudioElement | null = null;
let ctrl: AbortController | null = null;
const listeners = new Set<(on: boolean) => void>();
const emit = (on: boolean) => listeners.forEach((f) => f(on));

export const onSpeakingChange = (f: (on: boolean) => void) => {
  listeners.add(f);
  return () => void listeners.delete(f);
};

export function stopSpeaking() {
  ctrl?.abort();
  ctrl = null;
  if (audio) { audio.pause(); audio.src = ''; audio = null; }
  if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  emit(false);
}

const browserSpeak = (text: string) => {
  if (!('speechSynthesis' in window)) return emit(false);
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'tr-TR';
  const tr = window.speechSynthesis.getVoices().filter((v) => /^tr/i.test(v.lang));
  const v = tr.find((x) => /emel|natural|online/i.test(x.name)) || tr[0];
  if (v) u.voice = v;
  u.onend = u.onerror = () => emit(false);
  window.speechSynthesis.speak(u);
};

export async function speak(text: string) {
  stopSpeaking();
  const clean = text.replace(/\*\*|__|`|#+\s|>\s*\[!\w+\]/g, '').replace(/\s+/g, ' ').trim();
  if (!clean) return;
  emit(true);
  const c = (ctrl = new AbortController());
  try {
    const r = await fetch('/api/tts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: clean }),
      signal: c.signal,
    });
    if (!r.ok) throw new Error(String(r.status));
    const url = URL.createObjectURL(await r.blob());
    if (c.signal.aborted) return;
    const a = (audio = new Audio(url));
    a.onended = a.onerror = () => { URL.revokeObjectURL(url); if (audio === a) emit(false); };
    await a.play();
  } catch (e: any) {
    if (e?.name === 'AbortError' || c.signal.aborted) return;
    browserSpeak(clean);
  }
}

/**
 * İnteraktif öğrenme ders adımını seslendir:
 * Öncelikle EMA ile üretilmiş statik ses dosyasını (/api/ogren-ses/:deckId/:step.mp3) çalar.
 * Dosya bulunamazsa genel speak() fonksiyonuna (fallback) yönlendirir.
 */
export async function speakOgrenStep(deckId: string, stepNumber: number, fallbackText: string) {
  stopSpeaking();
  const clean = fallbackText.replace(/\*\*|__|`|#+\s|>\s*\[!\w+\]/g, '').replace(/\s+/g, ' ').trim();
  emit(true);
  const c = (ctrl = new AbortController());
  const baseUrl = (getCustomApiUrl() || '').replace(/\/$/, '');
  const audioUrl = `${baseUrl}/api/ogren-ses/${encodeURIComponent(deckId)}/${stepNumber}.mp3`;

  try {
    const headRes = await fetch(audioUrl, { method: 'HEAD', signal: c.signal });
    if (headRes.ok) {
      if (c.signal.aborted) return;
      const a = (audio = new Audio(audioUrl));
      a.onended = a.onerror = () => {
        if (audio === a) {
          audio = null;
          emit(false);
        }
      };
      await a.play();
      return;
    }
  } catch (e: any) {
    if (e?.name === 'AbortError' || c.signal.aborted) return;
  }

  // Statik EMA dosyası yoksa genel seslendiriciye yönlendir
  if (clean) {
    speak(clean);
  } else {
    emit(false);
  }
}

