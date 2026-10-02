import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const envPath = path.join(ROOT_DIR, '.env');
const localKeysPath = path.join(ROOT_DIR, 'supabase-server', 'local-supabase-keys.json');

if (!fs.existsSync(localKeysPath)) {
  console.error('Error: local-supabase-keys.json not found in supabase-server directory.');
  process.exit(1);
}

const localKeys = JSON.parse(fs.readFileSync(localKeysPath, 'utf8'));
let envContent = fs.readFileSync(envPath, 'utf8');

// Backup current .env if .env.cloud.bak doesn't exist
const cloudBakPath = path.join(ROOT_DIR, '.env.cloud.bak');
if (!fs.existsSync(cloudBakPath)) {
  fs.copyFileSync(envPath, cloudBakPath);
  console.log('Saved backup of cloud .env to .env.cloud.bak');
}

// Replace Supabase variables with local ones (Self-Hosted uses JWT keys)
envContent = envContent.replace(/^SUPABASE_URL=.*$/m, `SUPABASE_URL=http://localhost:8000`);
envContent = envContent.replace(/^SUPABASE_PUBLISHABLE_KEY=.*$/m, `SUPABASE_PUBLISHABLE_KEY=${localKeys.ANON_KEY}`);
envContent = envContent.replace(/^SUPABASE_SECRET_KEY=.*$/m, `SUPABASE_SECRET_KEY=${localKeys.SERVICE_ROLE_KEY}`);
envContent = envContent.replace(/^SUPABASE_JWKS_URL=.*$/m, `SUPABASE_JWKS_URL=http://localhost:8000/auth/v1/.well-known/jwks.json`);

fs.writeFileSync(envPath, envContent, 'utf8');

console.log('Successfully switched project .env to LOCAL Supabase:');
console.log('- SUPABASE_URL: http://localhost:8000');
console.log('- SUPABASE_PUBLISHABLE_KEY: ' + localKeys.SUPABASE_PUBLISHABLE_KEY);
