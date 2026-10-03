import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const envExamplePath = path.join(__dirname, '.env.example');
const envPath = path.join(__dirname, '.env');
const keysJsonPath = path.join(__dirname, 'local-supabase-keys.json');

console.log('Generating Supabase self-host secrets and keys...');

// Helper random functions
const genHex = (bytes) => crypto.randomBytes(bytes).toString('hex');
const genBase64 = (bytes) => crypto.randomBytes(bytes).toString('base64');
const base64UrlEncode = (strOrBuf) => {
  const buf = Buffer.isBuffer(strOrBuf) ? strOrBuf : Buffer.from(strOrBuf);
  return buf.toString('base64url');
};

const jwtSecret = genBase64(30);

// Generate HS256 JWTs
const iat = Math.floor(Date.now() / 1000);
const exp = iat + 5 * 365 * 24 * 3600; // 5 years

function genHS256Token(role) {
  const header = { alg: 'HS256', typ: 'JWT' };
  const payload = { role, iss: 'supabase', iat, exp };
  const headerB64 = base64UrlEncode(JSON.stringify(header));
  const payloadB64 = base64UrlEncode(JSON.stringify(payload));
  const signedContent = `${headerB64}.${payloadB64}`;
  const sig = crypto.createHmac('sha256', jwtSecret).update(signedContent).digest('base64url');
  return `${signedContent}.${sig}`;
}

const anonKey = genHS256Token('anon');
const serviceRoleKey = genHS256Token('service_role');

// Asymmetric keys (ES256)
const { privateKey } = crypto.generateKeyPairSync('ec', { namedCurve: 'P-256' });
const jwkPrivate = privateKey.export({ format: 'jwk' });
const kid = crypto.randomUUID();

const octKey = {
  kty: 'oct',
  k: Buffer.from(jwtSecret).toString('base64url'),
  alg: 'HS256'
};

const jwksKeypair = {
  keys: [
    {
      kty: 'EC',
      kid,
      use: 'sig',
      key_ops: ['sign', 'verify'],
      alg: 'ES256',
      ext: true,
      crv: jwkPrivate.crv,
      x: jwkPrivate.x,
      y: jwkPrivate.y,
      d: jwkPrivate.d
    },
    octKey
  ]
};

const jwksPublic = {
  keys: [
    {
      kty: 'EC',
      kid,
      use: 'sig',
      key_ops: ['verify'],
      alg: 'ES256',
      ext: true,
      crv: jwkPrivate.crv,
      x: jwkPrivate.x,
      y: jwkPrivate.y
    },
    octKey
  ]
};

// Opaque keys
const PROJECT_REF = 'supabase-self-hosted';
function generateOpaqueKey(prefix) {
  const random = crypto.randomBytes(17).toString('base64url').slice(0, 22);
  const intermediate = prefix + random;
  const checksum = crypto.createHash('sha256')
    .update(PROJECT_REF + '|' + intermediate)
    .digest('base64url')
    .slice(0, 8);
  return intermediate + '_' + checksum;
}

const publishableKey = generateOpaqueKey('sb_publishable_');
const secretKey = generateOpaqueKey('sb_secret_');

// Additional secrets
const postgresPassword = genHex(16);
const dashboardPassword = genHex(12);
const secretKeyBase = genBase64(48);
const realtimeDbEncKey = genHex(8);
const vaultEncKey = genHex(16);
const pgMetaCryptoKey = genBase64(24);
const logflarePublicAccessToken = genBase64(24);
const logflarePrivateAccessToken = genBase64(24);
const s3AccessKeyId = genHex(16);
const s3AccessKeySecret = genHex(32);

// Read .env.example
let content = fs.readFileSync(envExamplePath, 'utf8');

// Replace standard variables
content = content.replace(/^POSTGRES_PASSWORD=.*$/m, `POSTGRES_PASSWORD=${postgresPassword}`);
content = content.replace(/^JWT_SECRET=.*$/m, `JWT_SECRET=${jwtSecret}`);
content = content.replace(/^ANON_KEY=.*$/m, `ANON_KEY=${anonKey}`);
content = content.replace(/^SERVICE_ROLE_KEY=.*$/m, `SERVICE_ROLE_KEY=${serviceRoleKey}`);
content = content.replace(/^SUPABASE_PUBLISHABLE_KEY=.*$/m, `SUPABASE_PUBLISHABLE_KEY=${publishableKey}`);
content = content.replace(/^SUPABASE_SECRET_KEY=.*$/m, `SUPABASE_SECRET_KEY=${secretKey}`);
content = content.replace(/^JWT_KEYS=.*$/m, `JWT_KEYS='${JSON.stringify(jwksKeypair.keys)}'`);
content = content.replace(/^JWT_JWKS=.*$/m, `JWT_JWKS='${JSON.stringify(jwksPublic)}'`);
content = content.replace(/^DASHBOARD_USERNAME=.*$/m, `DASHBOARD_USERNAME=admin`);
content = content.replace(/^DASHBOARD_PASSWORD=.*$/m, `DASHBOARD_PASSWORD=${dashboardPassword}`);
content = content.replace(/^SECRET_KEY_BASE=.*$/m, `SECRET_KEY_BASE=${secretKeyBase}`);
content = content.replace(/^REALTIME_DB_ENC_KEY=.*$/m, `REALTIME_DB_ENC_KEY=${realtimeDbEncKey}`);
content = content.replace(/^VAULT_ENC_KEY=.*$/m, `VAULT_ENC_KEY=${vaultEncKey}`);
content = content.replace(/^PG_META_CRYPTO_KEY=.*$/m, `PG_META_CRYPTO_KEY=${pgMetaCryptoKey}`);
content = content.replace(/^LOGFLARE_PUBLIC_ACCESS_TOKEN=.*$/m, `LOGFLARE_PUBLIC_ACCESS_TOKEN=${logflarePublicAccessToken}`);
content = content.replace(/^LOGFLARE_PRIVATE_ACCESS_TOKEN=.*$/m, `LOGFLARE_PRIVATE_ACCESS_TOKEN=${logflarePrivateAccessToken}`);
content = content.replace(/^S3_PROTOCOL_ACCESS_KEY_ID=.*$/m, `S3_PROTOCOL_ACCESS_KEY_ID=${s3AccessKeyId}`);
content = content.replace(/^S3_PROTOCOL_ACCESS_KEY_SECRET=.*$/m, `S3_PROTOCOL_ACCESS_KEY_SECRET=${s3AccessKeySecret}`);

// Write .env
fs.writeFileSync(envPath, content, 'utf8');

// Write metadata keys json
const keysSummary = {
  SUPABASE_URL: 'http://localhost:8000',
  SUPABASE_PUBLISHABLE_KEY: publishableKey,
  SUPABASE_SECRET_KEY: secretKey,
  ANON_KEY: anonKey,
  SERVICE_ROLE_KEY: serviceRoleKey,
  POSTGRES_PASSWORD: postgresPassword,
  POSTGRES_PORT: 5432,
  POSTGRES_USER: 'postgres',
  POSTGRES_DB: 'postgres',
  DASHBOARD_URL: 'http://localhost:8000',
  DASHBOARD_USERNAME: 'admin',
  DASHBOARD_PASSWORD: dashboardPassword,
  generatedAt: new Date().toISOString()
};

fs.writeFileSync(keysJsonPath, JSON.stringify(keysSummary, null, 2), 'utf8');

console.log('Successfully created supabase-server/.env and local-supabase-keys.json!');
console.log('Credentials Summary:');
console.log(`- Studio URL: http://localhost:8000`);
console.log(`- Studio User: admin`);
console.log(`- Studio Password: ${dashboardPassword}`);
console.log(`- DB Port: 5432`);
console.log(`- DB Password: ${postgresPassword}`);
