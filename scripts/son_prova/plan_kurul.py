#!/usr/bin/env python3
"""Son Prova planı — Kurul 2+ (otomatik): partlar ders kayıt defterinden + ders bilgi deposundan (PDF yeniden okunmaz).

plan.py Kurul 1'in elle kurulmuş planıdır (PARTLAR, DUZELT, ELLE). Kurul 2'den itibaren aynı plan.json biçimi burada üretilir:
  - dersler: src/data/dersler/k<N>.json sırasıyla, yalnız bilgi deposu hazır olanlar (meds_database_v2/ders_bilgi/<id>/manifest.json)
  - pdf_metin: depodaki kaynak.md (=== SAYFA N ===), önem / çıkmış: zincir klasörü (meds_temp/spot_cozucu/k<N><slug>/)
  - soru havuzu: src/data/k<N><slug>_cozucu/<kod>.json (part "brans" = bu klasör adı; anahtardaki branş = slug)
  - sınav dağılımı: src/data/son_prova/k<N>/sinav.json (fakülte duyurusu, {slug: soru}) varsa o; yoksa ders saatiyle
    orantılı TAHMİN (plan["sinav_tahmini"] = true, zincir yöneticiye bildirir)
  - part: branş içinde ders sırasıyla, toplam kelime ≤ PART_KELIME (≤ 88 dk); anahtar k<N>-<81+i>-son-prova-<slug>[-<no>]
Kullanım: plan_kurul.py --kurul 2 --kok meds_temp/son_prova_k2
"""
import argparse
import math
import os
import json
import re
import sys
import unicodedata
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
ROOT = MEDS.parent
DEPO = ROOT / "meds_database_v2/ders_bilgi"
DAKIKA_KELIME = 112
PART_KELIME = 9000  # ≈ 80 dk; dogrula.py AZAMI_DAKIKA 88
ILK_NO = 81  # Kurul 1 ile aynı numara alanı (k<N>-81…99); ders kimlikleri ≤ 70


def nfc(s):
    return unicodedata.normalize("NFC", s or "")


def kisalt(s, n):
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def _yol(m, ad):
    """K1 manifesti `yollar`, K2 manifesti `dosyalar` taşır."""
    y = m.get("yollar") or {}
    d = m.get("dosyalar") or {}
    p = {"kaynak": y.get("kaynak_md") or d.get("kaynak.md"),
         "onem": y.get("onem") or next((v for k, v in d.items() if k.startswith("onem/")), None),
         "cikmis": y.get("cikmis") or next((v for k, v in d.items() if k.startswith("cikmis/")), None)}[ad]
    return Path(p) if p and Path(p).exists() else None


def havuz(klasor, kod):
    d = MEDS / f"src/data/{klasor}_cozucu"
    fs = [d / f"{kod}.json"] if (d / f"{kod}.json").exists() else sorted(d.glob(f"{kod}-*.json"))
    return [{"ref": f"{klasor}/{f.stem}#{q['no']}", **q} for f in fs for q in json.loads(f.read_text())["sorular"]]


def ders_hedefi(sayfa, cikmis):
    return int(round(min(2200, max(600, 400 + 10 * sayfa + 30 * cikmis)) / 50) * 50)


def sinav_dagilimi(kurul, dersler, slug_ad):
    duyuru = MEDS / f"src/data/son_prova/k{kurul}/sinav.json"
    if duyuru.exists():
        j = json.loads(duyuru.read_text())
        return {s: {"ad": slug_ad[s], "soru": int(n)} for s, n in j.items() if s in slug_ad}, False
    saat = {}
    for d in dersler:
        saat[d["_slug"]] = saat.get(d["_slug"], 0) + (d.get("saat_sayisi") or 1)
    top = sum(saat.values()) or 1
    ham = {s: 100 * v / top for s, v in saat.items()}
    n = {s: int(v) for s, v in ham.items()}
    for s in sorted(ham, key=lambda s: ham[s] - n[s], reverse=True)[: 100 - sum(n.values())]:
        n[s] += 1
    return {s: {"ad": slug_ad[s], "soru": n[s]} for s in sorted(n, key=lambda s: -n[s]) if n[s]}, True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kurul", type=int, required=True)
    ap.add_argument("--kok", required=True)
    a = ap.parse_args()
    K = a.kurul
    kok = Path(os.path.abspath(a.kok))
    (kok / "havuz").mkdir(parents=True, exist_ok=True)
    br = json.loads((MEDS / "src/data/dersler/branslar.json").read_text())["branslar"]
    ad_slug = {b["ad"]: b["slug"] for b in br}
    slug_ad = {b["slug"]: b["ad"] for b in br}
    kisa = {b["slug"]: b.get("kisa") or b["ad"] for b in br}
    defter = json.loads((MEDS / f"src/data/dersler/k{K}.json").read_text())["dersler"]
    hazir = []
    for d in defter:
        mp = DEPO / d["id"] / "manifest.json"
        if not mp.exists():
            continue
        m = json.loads(mp.read_text())
        if not _yol(m, "kaynak"):
            continue
        d = {**d, "_m": m, "_slug": ad_slug.get(d["brans"]) or re.sub(r"[^a-z]", "", nfc(d["brans"]).lower())}
        hazir.append(d)
    if not hazir:
        print(f"Kurul {K}: bilgi deposu hazır ders yok"); return 2
    sinav, tahmini = sinav_dagilimi(K, hazir, slug_ad)
    plan = {"kurul": K, "dakika_kelime": DAKIKA_KELIME, "sinav": {}, "sinav_tahmini": tahmini, "partlar": [],
            "eksik_depo": [d["id"] for d in defter if d.get("pdf") and d["id"] not in {h["id"] for h in hazir}]}
    no = ILK_NO
    for slug in sinav:
        ds = [d for d in hazir if d["_slug"] == slug]
        if not ds:
            continue
        klasor = f"k{K}{slug}"
        plan["sinav"][klasor] = sinav[slug]
        kayitlar = []
        for d in ds:
            m, kod = d["_m"], d["kod"]
            km = _yol(m, "kaynak")
            sayfa = len(re.findall(r"^=== SAYFA \d+", km.read_text(encoding="utf-8"), re.M))
            cp = _yol(m, "cikmis")
            cik = json.loads(cp.read_text()) if cp else []
            if isinstance(cik, dict):  # Kurul 1 patoloji: {ders no: [...]} tek dosya
                cik = cik.get(str(m.get("kaynak_kod") or kod).lstrip("p0") or "0", [])
            hv = havuz(klasor, kod)
            sesli = sorted((MEDS / "data/sesli_anlatim/metin").glob(f"{d['id']}-*.md"))
            pdf = m.get("pdf") or ""
            x = {"kod": kod, "slayt_kod": kod, "ad": d["konu"], "pdf_ad": Path(pdf).name or d["konu"],
                 "no": str(int(re.sub(r"\D", "", kod[-2:]) or 0)), "ders_id": d["id"], "sayfa": sayfa,
                 "cikmis": len(cik), "havuz": len(hv), "pdf_metin": str(km.relative_to(ROOT)) if km.is_relative_to(ROOT) else str(km),
                 "sesli_anlatim": str(sesli[0].relative_to(ROOT)) if sesli else None, "ders_notu": None,
                 "onem": str(_yol(m, "onem").relative_to(ROOT)) if _yol(m, "onem") else None,
                 "havuz_katalog": str((kok / "havuz" / f"{kod}.md").relative_to(ROOT)),
                 "drive_yol": pdf if "/" in pdf else None,
                 "hedef_kelime": ders_hedefi(sayfa, len(cik))}
            if not sayfa:
                x["pdf_yok"] = True
            md = [f"# {d['konu']} — slayt kodu {kod} ({sayfa} sayfa)", "", f"## Çıkmış sorular ({len(cik)}) — her birinin bilgisi metinde geçmeli", ""]
            for c in cik:
                sec = c.get("secenekler") or {}
                md.append(f"- **{c.get('id')}** · {c.get('sinav', '')} · {kisalt(c.get('kok', ''), 400)}")
                md.append("  " + " | ".join(f"{h}) {kisalt(v, 90)}" for h, v in sorted(sec.items())) + f" → **{c.get('dogru')}**")
            md += ["", f"## Soru havuzu ({len(hv)}) — aşama sorusu ve check-up adayı seçmek için (ref ile)", ""]
            for q in hv:
                dg = q.get("dogru")
                md.append(f"- `{q['ref']}` · {q.get('tur')}{'/' + q['zorluk'] if q.get('zorluk') else ''} · s.{q.get('sayfa', '?')} · "
                          f"{kisalt(q.get('soru', ''), 260)} → **{dg}) {kisalt((q.get('secenekler') or {}).get(dg, ''), 80)}**")
            (kok / "havuz" / f"{kod}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
            kayitlar.append(x)
        # branş içinde ders sırasıyla partlara böl
        # branş içinde ders sırasıyla, eşit boylu partlara böl (artık küçük part kalmasın)
        top = sum(y["hedef_kelime"] for y in kayitlar)
        hedef_part = top / max(1, math.ceil(top / PART_KELIME))
        gruplar, cur = [], []
        for x in kayitlar:
            t = sum(y["hedef_kelime"] for y in cur)
            if cur and (t + x["hedef_kelime"] > PART_KELIME or t >= hedef_part):
                gruplar.append(cur); cur = []
            cur.append(x)
        gruplar.append(cur)
        for i, g in enumerate(gruplar, 1):
            if no > 99:
                print("HATA: part numarası 99'u aştı (PART_KELIME büyütülmeli)"); return 1
            key = f"k{K}-{no}-son-prova-{slug}" + (f"-{i}" if len(gruplar) > 1 else "")
            hedef = sum(y["hedef_kelime"] for y in g)
            plan["partlar"].append({
                "key": key, "brans": klasor, "brans_ad": slug_ad[slug], "kisa": kisa[slug], "no": i,
                "drive_klasor": str(Path(g[0]["drive_yol"]).parent.name) if g[0].get("drive_yol") else slug_ad[slug],
                "baslik": ", ".join(y["ad"] for y in g[:3]) + (" ve diğerleri" if len(g) > 3 else ""),
                "hedef_kelime": hedef, "hedef_dakika": round(hedef / DAKIKA_KELIME), "dersler": g,
                "yazar_gruplari": [[y["kod"] for y in g[j:j + 3]] for j in range(0, len(g), 3)],
            })
            no += 1
    (kok / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    for p in plan["partlar"]:
        print(p["key"], p["hedef_kelime"], f"{p['hedef_dakika']} dk", [(d["kod"], d["hedef_kelime"], d["cikmis"], d["havuz"]) for d in p["dersler"]])
    if tahmini:
        print("UYARI: sınav dağılımı ders saatinden TAHMİN — fakülte duyurusu gelince src/data/son_prova/k%d/sinav.json yazılmalı" % K)
    return 0


if __name__ == "__main__":
    sys.exit(main())
