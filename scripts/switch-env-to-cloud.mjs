import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const envPath = path.join(ROOT_DIR, '.env');
const cloudBakPath = path.join(ROOT_DIR, '.env.cloud.bak');

if (!fs.existsSync(cloudBakPath)) {
  console.error('Error: .env.cloud.bak not found. Cannot restore cloud configuration automatically.');
  process.exit(1);
}

fs.copyFileSync(cloudBakPath, envPath);
console.log('Successfully restored project .env to CLOUD Supabase from .env.cloud.bak!');
