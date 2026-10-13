// Edge "Emel Online (Natural)" sesiyle Türkçe seslendirme; mp3 diskte önbelleklenir.
import type { Express } from 'express';
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import { MsEdgeTTS, OUTPUT_FORMAT } from 'msedge-tts';

const VOICE = 'tr-TR-EmelNeural';
const CACHE = path.join(process.cwd(), 'data', 'tts_cache');
const MAX_CHARS = 3000;

const synth = async (text: string): Promise<Buffer> => {
  const tts = new MsEdgeTTS();
  await tts.setMetadata(VOICE, OUTPUT_FORMAT.AUDIO_24KHZ_48KBITRATE_MONO_MP3);
  const { audioStream } = tts.toStream(text);
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    const timer = setTimeout(() => reject(new Error('tts timeout')), 30000);
    audioStream.on('data', (d: Buffer) => chunks.push(d));
    audioStream.on('end', () => { clearTimeout(timer); tts.close(); resolve(Buffer.concat(chunks)); });
    audioStream.on('error', (e: Error) => { clearTimeout(timer); reject(e); });
  });
};

const escapeXml = (s: string) => s.replace(/[<>&"']/g, (c) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&apos;' })[c]!);

export function registerTtsRoute(app: Express) {
  app.post('/api/tts', async (req, res) => {
    const text = String(req.body?.text || '').replace(/\s+/g, ' ').trim().slice(0, MAX_CHARS);
    if (!text) return res.status(400).json({ error: 'text gerekli' });
    const file = path.join(CACHE, crypto.createHash('sha1').update(VOICE + text).digest('hex') + '.mp3');
    try {
      if (!fs.existsSync(file)) {
        const buf = await synth(escapeXml(text));
        if (!buf.length) throw new Error('boş ses');
        fs.mkdirSync(CACHE, { recursive: true });
        fs.writeFileSync(file, buf);
      }
      res.setHeader('Content-Type', 'audio/mpeg');
      res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
      fs.createReadStream(file).pipe(res);
    } catch (e: any) {
      res.status(502).json({ error: e?.message || 'tts hatası' });
    }
  });
}
