/** Canlı ders tanıtım turlarının "görüldü" durumu (localStorage). Tur bileşeni tembel yüklenir; bu dosya küçük kalır. */

/** bugun: Bugün ekranı koç turu (H05) · secim: sesli derste uzun basma turu (H06). İkisinin görüldü bilgisi yalnız cihazda. */
export type CdTurTuru = 'liste' | 'ders' | 'bugun' | 'secim';

export const CD_TUR_ANAHTAR: Record<CdTurTuru, string> = {
  liste: 'medsoru_canli_ders_tur_liste_v1',
  ders: 'medsoru_canli_ders_tur_ders_v1',
  bugun: 'medsoru_bugun_tur_v1',
  secim: 'medsoru_cd_secim_tur_v1',
};

export const cdTurGoruldu = (tur: CdTurTuru) => {
  try {
    return !!localStorage.getItem(CD_TUR_ANAHTAR[tur]);
  } catch {
    return true; // depolama yoksa her açılışta kendiliğinden başlamasın
  }
};

export const cdTurIsaretle = (tur: CdTurTuru, nasil: 'basladi' | 'bitti' | 'atlandi') => {
  try {
    localStorage.setItem(CD_TUR_ANAHTAR[tur], `${nasil}:${new Date().toISOString()}`);
  } catch {
    /* özel pencere */
  }
};
