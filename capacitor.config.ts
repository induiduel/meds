import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'tr.com.nofrostlife.medsor.admin',
  appName: 'MeDSor Yönetim',
  webDir: 'dist-android',
  server: {
    androidScheme: 'https',
    cleartext: true,
    allowNavigation: [
      'nofrostlife.com.tr',
      '*.nofrostlife.com.tr',
      '192.168.*.*',
      '100.*.*.*',
      'localhost',
      '127.0.0.1',
    ],
  },
  android: {
    allowMixedContent: true,
    backgroundColor: '#F4F6F9',
  },
};

export default config;
