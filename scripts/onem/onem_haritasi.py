#!/usr/bin/env python3
"""Önem haritası (GELECEK_PLANLAMASI P2.2): ders PDF'inin her sayfası için "sınava konu olma" puanı.

Girdi: kaynak.md (=== SAYFA n === ayraçlı) + bu derse eşlenmiş çıkmış sorular (aday_hazirla.grupla biçimi: temsilci +
tekrar + yillar). Yöntem (yerel, CPU; bge-m3 servisi :8094):
  1. Her sayfa metni ve her çıkmış (kök + doğru şık) vektörlenir.
  2. Her çıkmış (kökü genelse kök + tüm şıklarla) en benzer sayfaya (ve 0.92×en iyi üstündeki komşulara) bağlanır; bağ eşiği 0.55.
  3. Sayfa puanı = Σ çıkmış ağırlığı × benzerlik; ağırlık = soruldu sayısı (temsilci + tekrar) × yakınlık
     (son 3 yıl 1.0, 4–6 yıl 0.7, daha eski 0.5). 0–100'e ölçeklenir (dersin en yüksek sayfası 100).
  4. Hocanın vurgusu: sayfada "önemli/dikkat/sık/mutlaka/sınav" geçerse +%10; sayfalar.json varsa renkli/kalın ifade
     sayısına göre en çok +%15.
Çıktı: {"surum":1,"kod","sayfalar":[{"sayfa","puan","cikmis":[{"id","benzerlik","kez","yillar"}],"vurgu"}],
        "baglanamayan":[id…]}  — baglanamayan = PDF'te karşılığı bulunamayan çıkmışlar (müfredat dışı ya da eşleme hatası).
Tüm üreticiler (spot/önem, çözücü, örnek soru, sesli metin vurgusu) bu haritayı girdi alır.

  onem_haritasi.py KAYNAK_MD CIKMIS_JSON [--kod 2n03] [--yaz CIKTI]
"""
import argparse, json, re, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / "scripts/agents"))
VURGU = re.compile(r"(?i)\b(önemli|dikkat|sık(?:lıkla)?|mutlaka|sınav|en sık|unutmayın|klasik)\b")
ESIK, KOMSU = 0.55, 0.92


def sayfalar(md):
    parca = re.split(r"=== SAYFA (\d+) ===", md)
    return [(int(parca[i]), parca[i + 1].strip()) for i in range(1, len(parca) - 1, 2)]


def yakinlik(yillar, simdi=2026):
    if not yillar:
        return 0.6
    son = max(int(str(y)[:4]) for y in yillar)
    fark = simdi - son
    return 1.0 if fark <= 3 else 0.7 if fark <= 6 else 0.5


def hesapla(md, cikmis, kod="", sayfa_vurgu=None):
    from lib import embed
    import numpy as np
    S = [(n, t) for n, t in sayfalar(md) if len(t) >= 40]
    if not S:
        return {"surum": 1, "kod": kod, "sayfalar": [], "baglanamayan": [c["id"] for c in cikmis]}
    A = np.array(embed([t[:1800] for _, t in S], model="bge-m3"))
    A /= np.linalg.norm(A, axis=1, keepdims=True)
    puan = np.zeros(len(S)); bag = [[] for _ in S]; kopuk = []
    if cikmis:
        Q = np.array(embed([(c["kok"] + " " + c["secenekler"].get(c["dogru"], ""))[:1200] for c in cikmis], model="bge-m3"))
        Q /= np.linalg.norm(Q, axis=1, keepdims=True)
        B = Q @ A.T
        # 2. geçiş: kökü genel olan sorular ("hangisi yanlıştır?") bilgiyi şıklarda taşır → kök + tüm şıklar
        zayif = [i for i in range(len(cikmis)) if float(B[i].max()) < ESIK]
        if zayif:
            Q2 = np.array(embed([(cikmis[i]["kok"] + " " + " ".join(cikmis[i]["secenekler"].values()))[:1500] for i in zayif],
                                model="bge-m3"))
            Q2 /= np.linalg.norm(Q2, axis=1, keepdims=True)
            for k, i in enumerate(zayif):
                B[i] = Q2[k] @ A.T
        for i, c in enumerate(cikmis):
            en = float(B[i].max())
            if en < ESIK:
                kopuk.append(c["id"]); continue
            kez = 1 + len(c.get("tekrar") or [])
            w = kez * yakinlik(c.get("yillar"))
            for j in np.where(B[i] >= max(ESIK, KOMSU * en))[0]:
                b = float(B[i, j]); puan[j] += w * b
                bag[j].append({"id": c["id"], "benzerlik": round(b, 3), "kez": kez, "yillar": c.get("yillar") or []})
    vurgu = [bool(VURGU.search(t)) for _, t in S]
    # hoca vurgusu: sözcük ("önemli", "dikkat" …) +%10; sayfalar.json'daki renkli/kalın ifade sayısı en çok +%15
    sv = sayfa_vurgu or {}
    carpan = [1 + (0.10 if v else 0) + 0.15 * min(1.0, sv.get(n, 0) / 8) for (n, _), v in zip(S, vurgu)]
    vurgu = [v or sv.get(n, 0) >= 3 for (n, _), v in zip(S, vurgu)]
    puan = puan * np.array(carpan)
    tepe = float(puan.max()) or 1.0
    out = [{"sayfa": n, "puan": round(100 * float(p) / tepe), "cikmis": sorted(b, key=lambda x: -x["benzerlik"]),
            "vurgu": v} for (n, _), p, b, v in zip(S, puan, bag, vurgu)]
    return {"surum": 1, "kod": kod, "cikmis_sayisi": len(cikmis), "sayfalar": out, "baglanamayan": kopuk}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("kaynak"); ap.add_argument("cikmis"); ap.add_argument("--kod", default=""); ap.add_argument("--yaz")
    ap.add_argument("--sayfalar", help="ders işçisinin sayfalar.json'u (renkli/kalın hoca vurgusu)")
    a = ap.parse_args()
    sv = None
    if a.sayfalar and Path(a.sayfalar).exists():
        sv = {x["sayfa"]: sum(1 for v in x.get("vurgulu", []) if v["tur"] in ("renk", "kalin"))
              for x in json.loads(Path(a.sayfalar).read_text())}
    h = hesapla(Path(a.kaynak).read_text(), json.loads(Path(a.cikmis).read_text()), a.kod, sv)
    ust = sorted(h["sayfalar"], key=lambda s: -s["puan"])[:8]
    print(f"{a.kod}: {len(h['sayfalar'])} sayfa · {h.get('cikmis_sayisi', 0)} çıkmış · bağlanamayan {len(h['baglanamayan'])}")
    for s in ust:
        print(f"  s.{s['sayfa']:>3} puan {s['puan']:>3} · {len(s['cikmis'])} çıkmış{' · hoca vurgusu' if s['vurgu'] else ''}")
    if a.yaz:
        Path(a.yaz).parent.mkdir(parents=True, exist_ok=True)
        Path(a.yaz).write_text(json.dumps(h, ensure_ascii=False, indent=1))
