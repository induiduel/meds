/** Oyun türü → kural motoru. Yeni oyun: motor/<ad>.ts + buraya satır + tipler.ts OyunTur. */
import type { Motor, OyunTur } from './tipler';
import { yediliMotor, takimMotor } from './motor/yedili';
import { yuzbirMotor } from './motor/yuzbir';
import { unoMotor } from './motor/uno';
import { kastetMotor, remiMotor } from './motor/acikMasa';
import { duzMotor } from './motor/duzOkey';
import { pistiMotor } from './motor/pisti';
import { dominoMotor } from './motor/domino';
import { goMotor } from './motor/go';
import { cizgiMotor } from './motor/cizgi';
import { xoxMotor } from './motor/xox';

export const MOTORLAR: Record<OyunTur, Motor> = { yedili: yediliMotor, takim: takimMotor, yuzbir: yuzbirMotor, uno: unoMotor, go: goMotor, cizgi: cizgiMotor, xox: xoxMotor, remi: remiMotor, kastet: kastetMotor, duz: duzMotor, pisti: pistiMotor, domino: dominoMotor };
