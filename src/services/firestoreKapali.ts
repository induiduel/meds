/**
 * firebase/firestore yerine geçen hafif modül (başarım turu 2026-10-20).
 *
 * dbFlags.ts'de FIREBASE_DB_ENABLED=false iken vite.config.ts `firebase/firestore`
 * içe aktarımını buraya yönlendirir: Firestore SDK'sı (~1,5 MB kaynak, ilk yüklemede
 * ~120 KB gzip) pakete girmez. Tüm çağrılar zaten bayrakla korunuyor; korunmayan
 * birkaç yol (CloudBridge) ağ isteği yapmadan sessizce boş döner.
 * Bayrak true yapılınca takma ad kendiliğinden kalkar, gerçek SDK kullanılır.
 */
const kapali = () => Promise.reject(new Error('Firebase veritabanı devre dışı'));
const ref = (..._a: unknown[]) => ({ __firestoreKapali: true });
export const getFirestore = ref;
export const collection = ref;
export const doc = ref;
export const query = ref;
export const where = ref;
export const orderBy = ref;
export const limit = ref;
export const getDoc = kapali;
export const getDocs = kapali;
export const setDoc = kapali;
export const addDoc = kapali;
export const deleteDoc = kapali;
export const onSnapshot = (..._a: unknown[]) => () => {};
export const writeBatch = () => ({
  set() { return this; }, update() { return this; }, delete() { return this; },
  commit: kapali,
});
