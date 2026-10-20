#!/usr/bin/env python3
"""Kurul kampı kapısı: şema, kaynak (kod:sayfa ders metninde var), onaylı tüyoların hepsi işlenmiş, şık açıklaması + Türkçe üslup.
  dogrula.py kamp.json --girdi girdi.json   → 0 HATA değilse çıkış 1
"""
import json, re, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / "scripts"))
from sik_aciklama import denetle as sik  # noqa: E402
from turkce_uslup import denetle_yapi as uslup  # noqa: E402


def main():
    k = json.loads(Path(sys.argv[1]).read_text())
    g = json.loads(Path(sys.argv[sys.argv.index("--girdi") + 1]).read_text())
    H = []
    sayfalar = {}
    for d in g["dersler"]:
        t = Path(d["kaynak"]).read_text() if Path(d["kaynak"]).exists() else ""
        sayfalar[d["kod"]] = {int(n) for n in re.findall(r"=== SAYFA (\d+) ===", t)}
    def kaynak(v, yer):
        for x in ([v] if isinstance(v, str) else v or []):
            m = re.fullmatch(r"(\d[a-z]\d{2}):(\d+)", str(x))
            if not m: H.append(f"{yer}: kaynak biçimi {x!r} (kod:sayfa)")
            elif m.group(1) not in sayfalar: H.append(f"{yer}: {m.group(1)} bu kampın dersi değil")
            elif int(m.group(2)) not in sayfalar[m.group(1)]: H.append(f"{yer}: {m.group(1)} dersinde sayfa {m.group(2)} yok")
        if not v: H.append(f"{yer}: kaynak yok")
    for a in ("surum", "kurul", "brans", "baslik", "kisa", "anlatim", "kalipler", "deneme"):
        if not k.get(a): H.append(f"{a} eksik")
    onayli = {t["id"] for t in g["tuyolar"]}
    kullanilan = set()
    ids = set()
    for i, a in enumerate(k.get("anlatim") or []):
        yer = f"anlatim {a.get('id', i)}"
        if a.get("id") in ids: H.append(f"{yer}: çift kimlik")
        ids.add(a.get("id"))
        n = len(str(a.get("metin", "")).split())
        if not 40 <= n <= 220: H.append(f"{yer}: {n} kelime (40–220)")
        kaynak(a.get("k"), yer)
        if a.get("tuyo"): kullanilan.add(a["tuyo"])
    for t in k.get("kalipler") or []:
        yer = f"kalıp {t.get('id')}"
        if len(t.get("sutun") or []) < 2: H.append(f"{yer}: en az 2 sütun")
        for j, s in enumerate(t.get("satir") or []):
            if not (s.get("s") and s.get("t")): H.append(f"{yer} satır {j+1}: boş hücre")
            kaynak(s.get("k"), f"{yer} satır {j+1}")
        if t.get("tuyo"): kullanilan.add(t["tuyo"])
    for q in k.get("deneme") or []:
        yer = f"deneme {q.get('id')}"
        if q.get("id") in ids: H.append(f"{yer}: çift kimlik")
        ids.add(q.get("id"))
        sec = q.get("secenekler") or {}
        if sorted(sec) != list("ABCDE"[:len(sec)]) or len(sec) < 4: H.append(f"{yer}: şıklar A–E")
        if q.get("dogru") not in sec: H.append(f"{yer}: doğru şık yok")
        for h, ac in (q.get("aciklama") or {}).items():
            H.extend(sik(ac, f"{yer}/{h}"))
        if set(q.get("aciklama") or {}) != set(sec): H.append(f"{yer}: her şıkka açıklama")
        kaynak(q.get("k"), yer)
        if q.get("tuyo"): kullanilan.add(q["tuyo"])
    for t in sorted(kullanilan - onayli): H.append(f"tüyo {t}: onaylı listede yok")
    for t in sorted(onayli - kullanilan): H.append(f"tüyo {t}: kampta işlenmemiş")
    H.extend(uslup({x: k.get(x) for x in ("baslik", "kisa", "anlatim", "kalipler", "deneme")}, "kamp"))
    for h in H[:80]: print("HATA", h)
    print(f"{len(k.get('anlatim') or [])} anlatım · {len(k.get('kalipler') or [])} kalıp · {len(k.get('deneme') or [])} soru · "
          f"{len(kullanilan & onayli)}/{len(onayli)} tüyo · {len(H)} HATA")
    sys.exit(1 if H else 0)


if __name__ == "__main__":
    main()
