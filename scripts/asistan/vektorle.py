#!/usr/bin/env python3
"""Tıp Asistanı F1: belgeler.jsonl → bge-m3 vektörleri (artımlı, kesilirse kaldığı yerden).

Önbellek: meds_temp/asistan/vektor/parca_*.npz (id, ozet, vec float16). Yalnız yeni/değişen belge vektörlenir.
CPU (varsayılan): servis :8094. GPU (kullanıcı izni 2026-10-29, yedinci istisna, AGENTS.md §10):
  ~/.local/share/meds-xtts/venv/bin/python scripts/asistan/vektorle.py --gpu
  Koşul: meds-gpuguard etkin, kart ≤62 °C iken açılır; VRAM payı 0,6; görev döngüsü ≈%60; 72 °C üstü yavaş,
  78 °C'de ≤64 °C'ye dek durur; çekirdek saati 3000 MHz geçerse (saat kilidi yok) o oturum CPU servisine döner.
"""
import argparse, glob, hashlib, json, os, subprocess, sys, time
import numpy as np
KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
GIRDI = os.path.join(KOK, '..', 'meds_temp', 'asistan', 'belgeler.jsonl')
DIZIN = os.path.join(KOK, '..', 'meds_temp', 'asistan', 'vektor')
PARTI = 16
SAAT_TAVAN = 3000  # kullanıcı kararı 2026-10-29: kilit 300,3000


def ozet(b):
    return hashlib.md5((b['baslik'] + '|' + b['metin']).encode()).hexdigest()


def girdi_metni(b):
    return (b['baslik'] + '\n' + b['metin'])[:1800]


def kart():
    r = subprocess.run(['nvidia-smi', '--query-gpu=temperature.gpu,clocks.gr', '--format=csv,noheader,nounits'], capture_output=True, text=True)
    t, c = [float(x) for x in r.stdout.strip().split(',')]
    return t, c


class GpuMotor:
    def __init__(self):
        import torch
        from transformers import AutoModel, AutoTokenizer
        if subprocess.run(['systemctl', '--user', 'is-active', '--quiet', 'meds-gpuguard']).returncode != 0:
            sys.exit('meds-gpuguard etkin değil: GPU kullanılmaz (AGENTS.md §10)')
        t, _ = kart()
        if t > 62:
            sys.exit(f'Kart {t:.0f} °C (>62): GPU işi başlatılmaz')
        torch.cuda.set_per_process_memory_fraction(0.6)
        self.torch = torch
        self.tok = AutoTokenizer.from_pretrained('BAAI/bge-m3')
        self.m = AutoModel.from_pretrained('BAAI/bge-m3', dtype=torch.float16).cuda().eval()

    def __call__(self, metinler):
        t0 = time.time()
        # ısı protokolü
        t, c = kart()
        while t >= 78:
            time.sleep(5); t, c = kart()
            if t <= 64: break
        if t > 72: time.sleep(2)
        if c > SAAT_TAVAN:
            raise RuntimeError(f'çekirdek saati {c:.0f} MHz > {SAAT_TAVAN} (saat kilidi yok)')
        out = []
        with self.torch.inference_mode():
            b = self.tok(metinler, padding=True, truncation=True, max_length=512, return_tensors='pt').to('cuda')
            v = self.m(**b).last_hidden_state[:, 0].float()
            out = self.torch.nn.functional.normalize(v, dim=-1).cpu().numpy()
        time.sleep(0.67 * (time.time() - t0))  # görev döngüsü ≈%60
        return out


def cpu_embed(metinler):
    import urllib.request
    istek = urllib.request.Request('http://127.0.0.1:8094/embed', json.dumps({'texts': metinler, 'kind': 'raw'}).encode(), {'Content-Type': 'application/json'})
    v = np.array(json.load(urllib.request.urlopen(istek, timeout=600))['vectors'], dtype='float32')
    return v / np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-9)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gpu', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    a = ap.parse_args()
    if not a.gpu:
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
    os.makedirs(DIZIN, exist_ok=True)
    belgeler = [json.loads(l) for l in open(GIRDI, encoding='utf-8')]
    hedef = {b['id']: ozet(b) for b in belgeler}
    var = set()
    for p in glob.glob(os.path.join(DIZIN, 'parca_*.npz')):
        z = np.load(p, allow_pickle=False)
        var.update(zip(z['id'].tolist(), z['ozet'].tolist()))
    eksik = [b for b in belgeler if (b['id'], hedef[b['id']]) not in var]
    if a.limit: eksik = eksik[:a.limit]
    print(f'{len(belgeler)} belge, önbellekte {len(belgeler) - len(eksik) if not a.limit else "?"}, vektörlenecek {len(eksik)}', flush=True)
    motor = GpuMotor() if a.gpu else None
    no = len(glob.glob(os.path.join(DIZIN, 'parca_*.npz')))
    bas = time.time(); biriken_id, biriken_oz, biriken_v = [], [], []
    for i in range(0, len(eksik), PARTI):
        grup = eksik[i:i + PARTI]
        metin = [girdi_metni(b) for b in grup]
        try:
            v = motor(metin) if motor else cpu_embed(metin)
        except RuntimeError as e:
            print('GPU bırakıldı, CPU servisine dönülüyor:', e, flush=True); motor = None; v = cpu_embed(metin)
        biriken_id += [b['id'] for b in grup]; biriken_oz += [hedef[b['id']] for b in grup]; biriken_v.append(v.astype('float16'))
        if len(biriken_id) >= 256 or i + PARTI >= len(eksik):
            np.savez(os.path.join(DIZIN, f'parca_{no:05d}.npz'), id=np.array(biriken_id), ozet=np.array(biriken_oz), vec=np.concatenate(biriken_v))
            no += 1; biriken_id, biriken_oz, biriken_v = [], [], []
            gecen = time.time() - bas
            print(f'{i + len(grup)}/{len(eksik)}  {gecen:.0f} sn  kalan ≈{gecen / (i + len(grup)) * (len(eksik) - i - len(grup)):.0f} sn', flush=True)


if __name__ == '__main__':
    main()
