/**
 * Donanım/girdi yardımcıları — cihazlar arası farklar burada toplanır.
 *
 * Pointer Events düğme bit maskesi (W3C):
 *   1  = birincil temas (kalem ucu / sol tık)
 *   2  = kalem yan (barrel) düğmesi / sağ tık
 *   32 = kalem silgi ucu (Surface Pen, Wacom; bazı Huawei M-Pen sürümleri)
 *
 * Cihaz notları:
 * - Samsung S-Pen (Chrome / Samsung Internet): yan düğme `buttons & 2`, basarken
 *   pointerdown'da `button === 2`. Uzun basışta contextmenu tetiklenir → engellenmeli.
 * - Huawei M-Pen (Huawei Browser / Chrome): çoğu sürümde `buttons & 2`, bazılarında
 *   `buttons & 32` / `button === 5`. Bazı eski WebView'lar kalemi 'touch' bildirir →
 *   bunun için arayüzde "Parmakla çiz" yedeği vardır.
 * - Apple Pencil (iPadOS Safari): `pointerType === 'pen'`, basınç var; yan düğme YOK
 *   (Pencil Pro sıkıştırma / çift dokunma web'e açılmaz) → silgi araç çubuğundan seçilir.
 *   Hover destekli iPad'lerde temas olmadan `buttons === 0` pointermove gelir.
 */

const BARREL_BIT = 2;
const ERASER_BIT = 32;
const ERASER_BUTTON = 5;

/**
 * Kalemin yan düğmesi ya da silgi ucu basılı mı (farede sağ tık)?
 * `e.button` yalnızca pointerdown'da güvenilir: pointerup ve akortlu pointermove'da
 * BIRAKILAN düğmeyi bildirir. Diğer olaylarda yalnızca `buttons` maskesine bakılır.
 */
export function isEraserButton(e: PointerEvent): boolean {
  if (e.pointerType === 'pen') {
    if ((e.buttons & (BARREL_BIT | ERASER_BIT)) !== 0) return true;
    return e.type === 'pointerdown' && (e.button === 2 || e.button === ERASER_BUTTON);
  }
  if (e.pointerType === 'mouse') {
    return (e.buttons & BARREL_BIT) !== 0;
  }
  return false;
}

/**
 * Samsung S-Pen + Android Chrome (Galaxy Tab'de ölçüldü): yan düğme `buttons` bit 2
 * olarak HİÇ bildirilmez.
 * - Kalem havadayken düğme basılıysa: `buttons === 1`, `pressure === 0` (normal hover'da 0).
 * - Kalem ekrandayken: düğme basılı olsa da olmasa da olaylar birebir aynıdır.
 * Bu yüzden düğme yalnızca havadayken okunabilir; motor bunu temasa taşır.
 */
export function isHoverBarrel(e: PointerEvent): boolean {
  return e.pointerType === 'pen' && (e.buttons & 1) !== 0 && e.pressure === 0;
}

/**
 * Basıncı okur.
 * - Bazı kalemler (S-Pen, M-Pen) pointerdown'da 0 bildirir → önceki değer ya da 0.5.
 * - Fare ve basınçsız cihazlar spesifikasyon gereği 0.5 bildirir.
 */
export function readPressure(e: PointerEvent, previous?: number): number {
  if (e.pointerType === 'pen' || e.pointerType === 'touch') {
    if (e.pressure > 0) return e.pressure;
    return previous ?? 0.5;
  }
  return 0.5;
}

/**
 * Birleştirilmiş (coalesced) olaylar: 60 Hz pointermove arasında kalemin 120–240 Hz
 * örneklerini verir; hızlı yazıda köşeli çizgiyi önler. Desteklenmiyorsa olayın kendisi.
 */
export function coalesced(e: PointerEvent): PointerEvent[] {
  const list = typeof e.getCoalescedEvents === 'function' ? e.getCoalescedEvents() : [];
  return list.length > 0 ? list : [e];
}

export function makeId(): string {
  // crypto.randomUUID yalnızca güvenli bağlamda (https/localhost) vardır; LAN IP'sinde yedek.
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') return crypto.randomUUID();
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}
