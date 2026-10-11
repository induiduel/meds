// ecosystem.config.cjs — Oracle VM üzerinde PM2 süreçleri.
// server.ts production modda dist/ varsa onu sunar (README: npm run build sonrası).
// Cihazda `npm run dev` aynen kalır; bu dosya yalnız Oracle içindir.
const path = require('path');

const APP_DIR = process.env.MEDS_APP_DIR || path.resolve(__dirname, '..', '..');

module.exports = {
  apps: [
    {
      name: 'meds-server',
      cwd: APP_DIR,
      script: 'node_modules/.bin/tsx',
      args: 'server.ts',
      interpreter: 'none',
      instances: 1,
      exec_mode: 'fork',
      env: {
        NODE_ENV: 'production',
        PORT: '3000',
      },
      max_memory_restart: '1.5G',
      min_uptime: '10s',
      max_restarts: 20,
      error_file: path.join(APP_DIR, 'deploy', 'oracle', 'logs', 'server-error.log'),
      out_file: path.join(APP_DIR, 'deploy', 'oracle', 'logs', 'server-out.log'),
      time: true,
    },
  ],
};
