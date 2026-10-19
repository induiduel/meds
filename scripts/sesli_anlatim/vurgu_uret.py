#!/usr/bin/env python3
"""Sesli ders metninde önemli cümle + anahtar terim vurguları (data/sesli_anlatim/vurgu/<key>.json).

Kaynaklar (o derse ait): sınav spotları (exam_spots_k1.json, ders = no), çıkmış sorular (pastQuestions.json,
topic = ders başlığı + örnek soruların ilgili_cikmis bağları) ve örnek sorular (ornek_sorular/k1/<key>.json).
Her kaynak öğesi (soru kökü + doğru cevap / spot metni) bge-m3 (CPU, :8094) ile dersin cümlelerine eşlenir;
eşik üstündeki en iyi cümleler "önemli" olur. Önem: 3 = çıkmışta sorulmuş, 2 = spot, 1 = yalnız örnek soru.
Spotlardaki **kalın** terimler ve sorulardaki kısa doğru cevaplar önemli cümlelerde aranır, bulunanlar "terim" olur.
Paragraf metni sunucuyla birebir aynı olsun diye /api/canli-ders/<key> üzerinden okunur (3000 açık olmalı).
Çıktı: {"surum":1,"p":{"<i>":[[bas,son,"c"|"t",onem], ...]}} — aralıklar paragraf içi karakter konumu.

Kullanım: python3 scripts/sesli_anlatim/vurgu_uret.py [--ders KEY] [--esik 0.66] [--eksik]
GPU (kullanıcı izni 2026-10-19; yalnız meds-gpuguard etkin + saat kilidi varken, VRAM payı 0,6):
  ~/.local/share/meds-xtts/venv/bin/python scripts/sesli_anlatim/vurgu_uret.py --gpu --eksik
"""
import argparse, json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path

GPU = "--gpu" in sys.argv
if not GPU:
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "scripts" / "agents"))
from lib import embed, fold  # noqa: E402


_gpu_model = None


def embed_gpu(texts: list[str]):
    """bge-m3 GPU'da (CLS havuzlama + L2, servisle aynı); fp16, VRAM payı 0,6, küçük partiler."""
    global _gpu_model
    import numpy as np
    import torch
    from transformers import AutoModel, AutoTokenizer
    if _gpu_model is None:
        if subprocess.run(["systemctl", "--user", "is-active", "--quiet", "meds-gpuguard"]).returncode != 0:
            sys.exit("meds-gpuguard etkin değil: GPU kullanılmaz (AGENTS.md §10)")
        torch.cuda.set_per_process_memory_fraction(0.6)
        tok = AutoTokenizer.from_pretrained("BAAI/bge-m3")
        _gpu_model = (tok, AutoModel.from_pretrained("BAAI/bge-m3", dtype=torch.float16).cuda().eval())
    tok, m = _gpu_model
    out = []
    with torch.inference_mode():
        for i in range(0, len(texts), 16):
            b = tok(texts[i:i + 16], padding=True, truncation=True, max_length=512, return_tensors="pt").to("cuda")
            v = m(**b).last_hidden_state[:, 0].float()
            out.append(torch.nn.functional.normalize(v, dim=-1).cpu().numpy())
            time.sleep(0.05)  # görev döngüsünü koruyucu sınırının altında tut
    return np.concatenate(out)


CIKTI = KOK / "data" / "sesli_anlatim" / "vurgu"
sys.path.insert(0, str(KOK / "scripts" / "sesli_anlatim"))
from pdf_hizala import cumle_sinirlari  # noqa: E402 — oynatıcının okunan cümlesiyle aynı sınırlar


def cumleler(t: str):
    out = []
    s = 0
    for e in cumle_sinirlari(t):
        b, son = s, e
        while son > b and t[son - 1].isspace(): son -= 1
        if son - b > 3: out.append((b, son))
        s = e
    return out


def duz(s: str) -> str:
    return re.sub(r"\*\*", "", s or "").strip()


def ogeler(key: str, no: int, baslik: str, spotlar, cikmislar) -> list[tuple[str, int, set[str]]]:
    """(eşleme metni, önem, terimler)"""
    out = []
    for s in spotlar:
        if s.get("ders") == no:
            out.append((duz(s.get("baslik", "")) + ". " + duz(s.get("spot", "")), 2, terimler(s)))
    def soru(kok, sec, dogru, onem):
        c = duz(str((sec or {}).get(dogru) or "")) if dogru else ""
        if not kok: return
        ts = {c} if 3 <= len(c) <= 40 else set()
        out.append((f"{kok} {c}".strip(), onem, ts))
    cik_id = set()
    f = KOK / "src/data/ornek_sorular/k1" / f"{key}.json"
    if f.exists():
        for k in json.load(open(f)).get("kazanimlar", []):
            for q in k.get("sorular") or []:
                soru(q.get("soru"), q.get("secenekler"), q.get("dogru"), 1)
            for q in k.get("ilgili_cikmis") or []:
                if isinstance(q, dict) and q.get("id") not in cik_id:
                    cik_id.add(q.get("id")); soru(q.get("soru"), q.get("secenekler"), q.get("cevap"), 3)
    hedef = fold_ayni(baslik)
    for q in cikmislar:
        if q["id"] in cik_id or fold_ayni(q.get("topic") or "") != hedef: continue
        cik_id.add(q["id"])
        r = q.get("reconstruction") or {}
        ops = r.get("options") or q.get("options") or []
        sec = {o.get("key"): o.get("text") for o in ops if isinstance(o, dict)}
        soru(r.get("stem") or q.get("stem"), sec, q.get("correctAnswer"), 3)
    return out


def terimler(sp) -> set[str]:
    ts = set()
    for src in [sp.get("spot", "")] + list(sp.get("maddeler") or []):
        for b in re.findall(r"\*\*([^*]+)\*\*", src):
            b = b.strip(" .,;:")
            if 3 <= len(b) <= 60: ts.add(b)
    c = (sp.get("cevap") or "").strip(" .")
    if 3 <= len(c) <= 40: ts.add(c)
    return ts


_TR = str.maketrans("ÇĞİIÖŞÜçğıöşüâîû", "cgiiosucgiosuaiu")


def katla(s: str) -> str:
    """uzunluğu koruyan Türkçe katlama (konumlar metinle aynı kalır)"""
    return "".join(c.lower() if len(c.lower()) == 1 else c for c in s.translate(_TR))


def fold_ayni(s: str) -> str:
    return fold(s)


def bul(metin: str, terim: str):
    """büyük/küçük ve Türkçe harf duyarsız arama; sözcük başında başlayan eşleşmeler"""
    fm, ft = katla(metin), katla(terim.strip())
    if not ft: return []
    out, i = [], fm.find(ft)
    while i >= 0:
        sol = i == 0 or not fm[i - 1].isalnum()
        if sol: out.append((i, i + len(ft)))
        i = fm.find(ft, i + 1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ders"); ap.add_argument("--esik", type=float, default=0.66)
    ap.add_argument("--gpu", action="store_true"); ap.add_argument("--eksik", action="store_true", help="vurgu dosyası olanları atla")
    ap.add_argument("--tavan", type=float, default=0.22, help="önemli cümle oranı üst sınırı")
    a = ap.parse_args()
    spotlar = json.load(open(KOK / "src/data/exam_spots_k1.json"))["spotlar"]
    cikmislar = [q for q in json.load(open(KOK / "src/data/pastQuestions.json"))
                 if q.get("committeeId") == "donem3-kurul1" and not q.get("hidden") and not q.get("iptal")]
    dersler = json.load(open(KOK / "data/sesli_anlatim/dersler.json"))
    CIKTI.mkdir(parents=True, exist_ok=True)
    for d in dersler:
        key = d["key"]
        if a.ders and key != a.ders: continue
        if a.eksik and (CIKTI / f"{key}.json").exists(): continue
        sp = ogeler(key, d["no"], d["baslik"], spotlar, cikmislar)
        det = json.load(urllib.request.urlopen(f"http://127.0.0.1:3000/api/canli-ders/{key}", timeout=60))
        pars = [p for b in det["bolumler"] for p in b["paragraflar"]]
        cs = [(p["i"], s, e, p["metin"][s:e]) for p in pars for s, e in cumleler(p["metin"])]
        if not sp or not cs:
            print(f"{key}: öğe {len(sp)}, cümle {len(cs)} — atlandı"); continue
        emb = embed_gpu if a.gpu else embed
        sv = emb([o[0] for o in sp])
        cv = emb([c[3] for c in cs])
        sim = sv @ cv.T  # spot × cümle
        puan: dict[int, tuple[float, int]] = {}
        sec_terim: dict[int, set[str]] = {}
        for si, s in enumerate(sp):
            sira = sim[si].argsort()[::-1][:2]
            for k, ci in enumerate(sira):
                v = float(sim[si, ci])
                if v < a.esik + (0.04 if s[1] == 1 else 0) or (k and v < sim[si, sira[0]] - 0.03): continue
                eski = puan.get(ci)
                if not eski or (s[1], v) > (eski[1], eski[0]): puan[ci] = (v, s[1])
                sec_terim.setdefault(ci, set()).update(s[2])
        tavan = max(3, int(len(cs) * a.tavan))
        secili = sorted(puan, key=lambda ci: (-puan[ci][1], -puan[ci][0]))[:tavan]
        p_out: dict[str, list] = {}
        for ci in sorted(secili):
            i, s, e, txt = cs[ci]
            r = p_out.setdefault(str(i), [])
            r.append([s, e, "c", puan[ci][1]])
            dolu: list[tuple[int, int]] = []
            for t in sorted(sec_terim.get(ci, ()), key=len, reverse=True):
                for ts, te in bul(txt, t):
                    if any(ts < y and te > x for x, y in dolu): continue
                    dolu.append((ts, te)); r.append([s + ts, s + te, "t", 0])
        for r in p_out.values(): r.sort(key=lambda x: (x[0], x[2]))
        (CIKTI / f"{key}.json").write_text(json.dumps({"surum": 1, "p": p_out}, ensure_ascii=False, separators=(",", ":")))
        nt = sum(1 for r in p_out.values() for x in r if x[2] == "t")
        print(f"{key}: öğe {len(sp)}, cümle {len(cs)}, önemli {len(secili)}, terim {nt}", flush=True)


if __name__ == "__main__":
    main()
