/**
 * Ses öğesinin oynatma kilidini kullanıcı dokunuşu sırasında açar (iOS/Safari, H-KMB-ses).
 * Kök neden: ses `await fetch(...)` sonrasında ya da rAF döngüsünde `play()` edildiği için dokunuşun dışında kalıyor,
 * tarayıcı NotAllowedError veriyor, görüntü sessiz sürüyordu; ancak ikinci dokunuşta ses geliyordu.
 * Çözüm: dokunuş anında (eşzamanlı) öğe sessizce oynatılıp kilidi açılır; aynı öğe sonra src değişse de serbestçe çalar.
 * Gerçek oynatmadan önce `a.muted = false` yapılmalı (kilit açma oynatması yalnız hâlâ sessizse duraklatılır).
 */
export function sesKilidiAc(a: HTMLAudioElement, src?: string) {
  if (a.dataset.acik) return;
  if (!a.getAttribute('src') && src) a.src = src;
  if (!a.getAttribute('src')) return;
  a.dataset.acik = '1';
  a.muted = true;
  a.play()
    .then(() => { if (a.muted) a.pause(); })
    .catch((e) => { if (e?.name === 'NotAllowedError') delete a.dataset.acik; })
    .finally(() => { a.muted = false; });
}
