import { cdDersSesSurumuAyarla, cdDurum, cdVaryant, fmtSure, type CdSurum } from '../canliDers/canliDersStore';
import { linkClick, navigateTo } from '../../router';
import { dersYolu } from './dersVeri';

/**
 * Ders sürümü seçici (V1 / V2 / V3): ders düzeyindeki sürümler (…-v2) ve metni düzeltilip yeniden seslendirilen dersin eski/yeni
 * sesi (kayit.json `surumAd`). Seçim ders için cihazda hatırlanır; oynatıcı o dersi açınca bu sesi çalar (cdOynat). En yeni sürüm "güncel".
 * `aktif`: ders sayfasında seçili sürüm; listede seçili ya da güncel olan vurgulanır.
 */
export default function SurumSecV15({ surumler, aktif, sinif = 'sl15-surum' }: { surumler: CdSurum[]; aktif?: CdSurum | null; sinif?: string }) {
  if (surumler.length < 2) return null;
  const sec = (s: CdSurum) => {
    cdDersSesSurumuAyarla(s.key, s.vid || null);
    if (s.vid && cdDurum().key === s.key) cdVaryant(s.vid);
  };
  return (
    <span className={sinif} role="group" aria-label="Ders sürümü">
      {surumler.map((s) => {
        const on = !!aktif && aktif.key === s.key && (aktif.vid || '') === (s.vid || '');
        const baslik = `${s.ad}${s.yeni ? ' · güncel' : ' · önceki sürüm'}${s.sureSn ? ` · ${fmtSure(s.sureSn)}` : ''}`;
        return (
          <a key={`${s.key}:${s.vid || ''}`} href={dersYolu(s.key)} className={`${on ? 'is-on' : ''}${s.yeni ? ' is-yeni' : ''}`}
            aria-current={on ? 'true' : undefined} title={baslik}
            onClick={linkClick(() => { sec(s); navigateTo(dersYolu(s.key)); })}>
            {s.ad}{s.yeni && <small>güncel</small>}
          </a>
        );
      })}
    </span>
  );
}
