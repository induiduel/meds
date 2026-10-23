"""Önem listesi ve soru çözücü görevlerinin ortak veri katmanı (ders zinciri çalışma klasörü W).

W = meds_temp/spot_cozucu/<brans>/ (ders zinciri; sınamada başka klasör): girdi/<kod>.json, cikmis/<kod>.json,
pdf_metin/<kod>.md (=== SAYFA n ===), onem_haritasi/<kod>.json (varsa). Görev ara çıktıları W/gorev/<kod>/.
Hedef biçimi: `<brans>:<kod>/parca/<n>` ya da `<brans>:<kod>/parti/<n>`; `--ayar w=<klasör>` W'yi değiştirir (sınama).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .. import cekirdek as c

SPOT = c.TEMP / "spot_cozucu"
PARCA_SAYFA, PARCA_KELIME = 10, 2600


def hedef_coz(hedef: str, ayar: dict | None, tur: str) -> tuple[Path, str, int]:
    m = re.fullmatch(rf"([a-z0-9_]+):([a-z0-9]+)/{tur}/(\d+)", hedef)
    if not m:
        raise SystemExit(f"hedef '<brans>:<kod>/{tur}/<n>' biçiminde olmalı: {hedef}")
    W = Path((ayar or {}).get("w") or SPOT / m.group(1))
    if not (W / "pdf_metin" / f"{m.group(2)}.md").exists():
        raise SystemExit(f"{W}/pdf_metin/{m.group(2)}.md yok")
    return W, m.group(2), int(m.group(3))


def sayfalar(W: Path, kod: str) -> dict[int, str]:
    t = (W / "pdf_metin" / f"{kod}.md").read_text(encoding="utf-8")
    parca = re.split(r"\n=== SAYFA (\d+) ===\n", t)
    return {int(parca[i]): parca[i + 1] for i in range(1, len(parca) - 1, 2)}


def satirlar(metin: str) -> list[str]:
    return [s.strip() for s in metin.splitlines() if s.strip() and len(s.strip()) > 1]


def parcalar(W: Path, kod: str) -> list[tuple[int, int]]:
    """Sayfa grupları: ≤ PARCA_SAYFA sayfa ve ≤ PARCA_KELIME sözcük; belirlenimci."""
    S = sayfalar(W, kod)
    out, bas, kel = [], None, 0
    for no in sorted(S):
        k = len(S[no].split())
        if bas is not None and (no - bas + 1 > PARCA_SAYFA or kel + k > PARCA_KELIME):
            out.append((bas, no - 1)); bas, kel = None, 0
        if bas is None:
            bas = no
        kel += k
    if bas is not None:
        out.append((bas, max(S)))
    return out


def cikmislar(W: Path, kod: str) -> list[dict]:
    p = W / "cikmis" / f"{kod}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def cikmis_sayfasi(W: Path, kod: str) -> dict[str, int]:
    """Her çıkmış temsilcisinin en uygun sayfası: önem haritası bağı, yoksa bge-m3 (soru ↔ sayfa) en iyisi."""
    out: dict[str, int] = {}
    oh = c.oku(W / "onem_haritasi" / f"{kod}.json") or {}
    for s in oh.get("sayfalar", []):
        for x in s.get("cikmis", []):
            if x.get("id") and (x["id"] not in out or x.get("benzerlik", 0) > out.get("_" + x["id"], 0)):
                out[x["id"]] = s["sayfa"]; out["_" + x["id"]] = x.get("benzerlik", 0)
    out = {k: v for k, v in out.items() if not k.startswith("_")}
    C = [x for x in cikmislar(W, kod) if x["id"] not in out]
    if C:
        import sys
        sys.path.insert(0, str(c.KOK / "scripts" / "kroki"))
        from ortak import vektorle
        S = sayfalar(W, kod)
        no = [n for n in sorted(S) if len(S[n].split()) >= 5]
        SV = vektorle([" ".join(S[n].split())[:2000] for n in no])
        QV = vektorle([f"{x['kok']} {x['secenekler'].get(x['dogru'], '')}" for x in C])
        for x, v in zip(C, QV):
            out[x["id"]] = no[int((SV @ v).argmax())]
    return out


def madde_hedefi(sayfa: int) -> int:
    """TALIMAT_ONEM: 20 sayfa ~20–25, 50+ sayfa ~35–45 madde."""
    return max(20, min(45, round(10 + 0.6 * sayfa)))


def paylastir(toplam: int, agirlik: list[float], en_az: int = 0) -> list[int]:
    """En büyük kalan yöntemiyle tamsayı paylaştırma."""
    s = sum(agirlik) or 1
    ham = [toplam * a / s for a in agirlik]
    out = [max(en_az, int(h)) for h in ham]
    kalan = toplam - sum(out)
    for i in sorted(range(len(ham)), key=lambda i: -(ham[i] - int(ham[i]))):
        if kalan <= 0:
            break
        out[i] += 1; kalan -= 1
    return out


def parca_plani(W: Path, kod: str) -> dict:
    """Ders düzeyi hedeflerin (madde, örnek, zorluk) parçalara belirlenimci dağıtımı + çıkmışların parçası."""
    g = json.loads((W / "girdi" / f"{kod}.json").read_text(encoding="utf-8"))
    S = sayfalar(W, kod)
    P = parcalar(W, kod)
    agirlik = [sum(len(S[n].split()) for n in S if a <= n <= b) + 30 for a, b in P]
    C = cikmislar(W, kod)
    cs = cikmis_sayfasi(W, kod)
    n_madde = madde_hedefi(g.get("sayfa") or len(S))
    n_ornek = min(g["ornek_hedef"] + 6, max(g["ornek_hedef"] + 2, 20 - len(C)))
    plan = {"madde": paylastir(n_madde, agirlik, 2), "ornek": paylastir(n_ornek, agirlik, 1), "parcalar": P}
    plan["zorluk"] = zorluk_dagit(plan["ornek"])
    plan["cikmis"] = [[x["id"] for x in C if a <= cs.get(x["id"], a) <= b] for a, b in P]
    return plan


ZORLUK_ORAN = (("kolay", 0.2), ("orta", 0.6), ("zor", 0.2))


def zorluk_dagit(ornek: list[int]) -> list[dict]:
    """Zorluk DERS düzeyinde dağıtılır, sonra parçalara birikimli yuvarlamayla bölünür (H32). Eskiden her parça kendi
    içinde yuvarlanıyordu: 3 soruluk parçada %20 zor → 0, ders toplamı %9 zor kalıp birleştirme kapısında duruyordu.
    Kolay birikimi yukarı, zor birikimi aşağı yuvarlanır: kolay sorular dersin başına, zor sorular sonuna doğru düşer
    (sona doğru öğrenci daha çok bilgiyle karşılaşır); son parçada toplamlar tam hedefe eşitlenir."""
    import math
    N = sum(ornek)
    if not N:
        return [{"kolay": 0, "orta": 0, "zor": 0} for _ in ornek]
    Tk, _, Tz = paylastir(N, [o for _, o in ZORLUK_ORAN])
    out, onek, k0, z0 = [], 0, 0, 0
    for i, n in enumerate(ornek):
        onek += n
        son = i == len(ornek) - 1
        k1 = Tk if son else min(Tk, math.ceil(Tk * onek / N - 1e-9))
        z1 = Tz if son else min(Tz, math.floor(Tz * onek / N + 1e-9))
        k, z = k1 - k0, z1 - z0
        if k + z > n:                                   # küçük parça: önce kolayı kıs (zor eksik kalmasın)
            k = max(0, n - z); z = min(z, n - k)
        out.append({"kolay": k, "orta": n - k - z, "zor": z})
        k0 += k; z0 += z
    return out
