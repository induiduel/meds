/** Oyun türü → kural motoru. Yeni oyun: motor/<ad>.ts + buraya satır + tipler.ts OyunTur. */
import type { Motor, OyunTur } from './tipler';
import { yediliMotor, takimMotor } from './motor/yedili';
import { yuzbirMotor } from './motor/yuzbir';
import { unoMotor } from './motor/uno';

export const MOTORLAR: Record<OyunTur, Motor> = { yedili: yediliMotor, takim: takimMotor, yuzbir: yuzbirMotor, uno: unoMotor };
