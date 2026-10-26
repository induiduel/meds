/**
 * Öğrenci Drive API uçları:
 *   GET  /api/admin/ogrenci-drive/envanter      - Öğrenci Drive'ındaki dosya envanterini döner
 *   POST /api/admin/ogrenci-drive/tara          - Öğrenci Drive klasörünü yeniden tarar
 *   GET  /api/admin/ogrenci-drive/eslesmeler   - Belirli bir kurul için materyal ve PDF eşleşmelerini döner
 *   POST /api/admin/ogrenci-drive/indir         - Seçili öğrenci dosyasını yerel diske indirir
 */
import { Router } from 'express';
import fs from 'fs';
import path from 'path';
import { execFile } from 'child_process';
import { promisify } from 'util';

const execFileAsync = promisify(execFile);

export function ogrenciDriveRouter(): Router {
  const router = Router();
  const appDir = path.resolve(process.cwd());
  const envanterDosyasi = path.join(appDir, 'data', 'ogrenci_drive_envanter.json');
  const pythonScript = path.join(appDir, 'scripts', 'ogrenci_drive', 'ogrenci_drive.py');

  router.get('/envanter', async (_req, res) => {
    try {
      if (fs.existsSync(envanterDosyasi)) {
        const raw = await fs.promises.readFile(envanterDosyasi, 'utf-8');
        return res.json({ ok: true, envanter: JSON.parse(raw) });
      }
      return res.json({ ok: true, envanter: null, mesaj: 'Henüz tarama yapılmamış' });
    } catch (e: any) {
      return res.status(500).json({ ok: false, error: e?.message || 'Envanter okunamadı' });
    }
  });

  router.post('/tara', async (_req, res) => {
    try {
      const { stdout, stderr } = await execFileAsync('python3', [pythonScript, '--tara'], { timeout: 60000 });
      let envanter = null;
      if (fs.existsSync(envanterDosyasi)) {
        const raw = await fs.promises.readFile(envanterDosyasi, 'utf-8');
        envanter = JSON.parse(raw);
      }
      return res.json({ ok: true, envanter, log: stdout || stderr });
    } catch (e: any) {
      return res.status(500).json({ ok: false, error: e?.message || 'Tarama hatası' });
    }
  });

  router.get('/eslesmeler', async (req, res) => {
    try {
      const kurul = Number(req.query.kurul) || 2;
      const { stdout } = await execFileAsync('python3', [pythonScript, '--esle', '--kurul', String(kurul)], { timeout: 30000 });
      return res.json({ ok: true, kurul, cikti: stdout });
    } catch (e: any) {
      return res.status(500).json({ ok: false, error: e?.message || 'Eşleşme hatası' });
    }
  });

  router.post('/indir', async (req, res) => {
    try {
      const { id, hedef } = req.body || {};
      if (!id || !hedef) {
        return res.status(400).json({ ok: false, error: 'id ve hedef alanları zorunludur' });
      }
      const hedefYol = path.resolve(appDir, hedef);
      const { stdout, stderr } = await execFileAsync('python3', [pythonScript, '--indir', '--id', id, '--hedef', hedefYol], { timeout: 120000 });
      return res.json({ ok: true, hedef: hedefYol, log: stdout || stderr });
    } catch (e: any) {
      return res.status(500).json({ ok: false, error: e?.message || 'İndirme hatası' });
    }
  });

  return router;
}
