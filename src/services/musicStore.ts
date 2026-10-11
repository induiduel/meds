/**
 * Müzik: kullanıcı bazlı kalıcı çalma listesi (server-only).
 * Eklenen parçalar yalnız tarayıcı belleğinde tutulduğu için cihaz değişince ya da site verisi
 * silinince kayboluyordu. Liste artık `data/music_playlists.json` içinde sahip kimliğine göre saklanır.
 * Boş liste ancak istemci açıkça boşaltınca yazılır (bkz. CLAUDE.md "boş sonuçla üzerine yazma").
 */
import fs from 'fs';
import path from 'path';

export interface StoredTrack { id: string; title: string; artist?: string; url: string; videoId?: string; listId?: string }
interface Store { [ownerId: string]: { tracks: StoredTrack[]; updatedAt: string } }

const FILE = path.resolve(process.cwd(), 'data', 'music_playlists.json');
const MAX_TRACKS = 300;

function read(): Store {
  try {
    if (!fs.existsSync(FILE)) return {};
    const v = JSON.parse(fs.readFileSync(FILE, 'utf-8'));
    return v && typeof v === 'object' && !Array.isArray(v) ? v : {};
  } catch {
    return {};
  }
}

function write(store: Store) {
  fs.mkdirSync(path.dirname(FILE), { recursive: true });
  const tmp = `${FILE}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(store, null, 2), 'utf-8');
  fs.renameSync(tmp, FILE);
}

const str = (v: unknown, max: number) => (typeof v === 'string' ? v.trim().slice(0, max) : '');

/** Gelen listeyi doğrular: yalnız http(s) bağlantıları, alan uzunlukları sınırlı, url'ye göre tekil. */
export function sanitizeTracks(input: unknown): StoredTrack[] {
  if (!Array.isArray(input)) return [];
  const seen = new Set<string>();
  const out: StoredTrack[] = [];
  for (const raw of input) {
    if (!raw || typeof raw !== 'object') continue;
    const t = raw as Record<string, unknown>;
    const url = str(t.url, 600);
    if (!/^https?:\/\//i.test(url) || seen.has(url)) continue;
    const title = str(t.title, 200) || url;
    seen.add(url);
    const track: StoredTrack = { id: str(t.id, 80) || `t-${out.length}-${Date.now().toString(36)}`, title, url };
    const artist = str(t.artist, 120);
    const videoId = str(t.videoId, 40);
    const listId = str(t.listId, 80);
    if (artist) track.artist = artist;
    if (videoId) track.videoId = videoId;
    if (listId) track.listId = listId;
    out.push(track);
    if (out.length >= MAX_TRACKS) break;
  }
  return out;
}

export function getPlaylist(ownerId: string): { tracks: StoredTrack[]; updatedAt: string | null } {
  const entry = read()[ownerId];
  return entry ? { tracks: entry.tracks || [], updatedAt: entry.updatedAt || null } : { tracks: [], updatedAt: null };
}

export function savePlaylist(ownerId: string, tracks: StoredTrack[]): { tracks: StoredTrack[]; updatedAt: string } {
  const store = read();
  const updatedAt = new Date().toISOString();
  store[ownerId] = { tracks, updatedAt };
  write(store);
  return { tracks, updatedAt };
}
