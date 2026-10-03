/**
 * Veritabanı anahtarları (dbFlags.ts)
 *
 * FIREBASE_DB_ENABLED=false iken Firestore'a hiçbir ağ isteği yapılmaz;
 * tüm okuma/yazma/silme Supabase + yerel sunucu üzerinden yürür.
 * Yeniden açmak için true yapmanız yeterlidir.
 */
export const FIREBASE_DB_ENABLED = false;
