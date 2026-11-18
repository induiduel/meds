/**
 * Ses öğesinin oynatma kilidini kullanıcı dokunuşu sırasında açar (iOS/Safari, H636).
 * Kök neden: ses `await fetch(...)` sonrasında ya da rAF döngüsünde `play()` edildiği için dokunuşun dışında kalıyor,
 * tarayıcı NotAllowedError veriyordu. Çözüm: dokunuş anında (eşzamanlı) öğe kısa SESSİZ bir klipte oynatılıp kilidi
 * açılır; gerçek ses (blob) inince aynı öğeye konur. Gerçek klip burada AĞDAN akıtılmaz: akışta her konumlama tampon
 * bekletir, cümle başları kesilir (H637).
 */
const SESSIZ = (() => {
  // 0,05 sn, 8 kHz, 8 bit mono sessiz WAV
  const n = 400, b = new Uint8Array(44 + n), v = new DataView(b.buffer);
  const yaz = (o: number, s: string) => { for (let i = 0; i < s.length; i++) b[o + i] = s.charCodeAt(i); };
  yaz(0, 'RIFF'); v.setUint32(4, 36 + n, true); yaz(8, 'WAVEfmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true);
  v.setUint16(22, 1, true); v.setUint32(24, 8000, true); v.setUint32(28, 8000, true); v.setUint16(32, 1, true);
  v.setUint16(34, 8, true); yaz(36, 'data'); v.setUint32(40, n, true); b.fill(128, 44);
  let s = ''; b.forEach((x) => { s += String.fromCharCode(x); });
  return `data:audio/wav;base64,${btoa(s)}`;
})();
/** src henüz gerçek ses değil (boş ya da kilit açma klibi) */
export const sesYok = (a: HTMLAudioElement) => !a.src || a.src.startsWith('data:');

export function sesKilidiAc(a: HTMLAudioElement) {
  if (a.dataset.acik) return;
  a.dataset.acik = '1';
  const gercek = !sesYok(a);
  if (!gercek) a.src = SESSIZ;
  a.muted = true;
  a.play()
    .then(() => { if (a.muted) a.pause(); })
    .catch((e) => { if (e?.name === 'NotAllowedError') delete a.dataset.acik; })
    .finally(() => {
      a.muted = false;
      if (a.src === SESSIZ) { a.removeAttribute('src'); a.load(); }
    });
}
