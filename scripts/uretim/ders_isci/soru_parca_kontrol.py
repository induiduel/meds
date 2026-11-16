"""Yenileme örnek soru parçası denetimi: python3 soru_parca_kontrol.py <taslak> <parca.json> → 0 = HATA yok.
Şema (A–E, gerekçeli şık açıklamaları, zorluk, kazanım aralığı) + kanıt alıntısının kaynak.md'de birebir varlığı."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from denetle import Denetim, norm  # noqa: E402

d, f = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
f = f if f.is_absolute() else d / f
den = Denetim(d)
kaz = len(json.loads((d / "ders_paketi.json").read_text(encoding="utf-8")).get("kazanimlar") or [])
cik = {c.get("id") or c.get("question_id") for c in json.loads((d / "baglam.json").read_text(encoding="utf-8")).get("cikmis_adaylari") or []}
sorular = json.loads(f.read_text(encoding="utf-8")).get("sorular") or []
for q in sorular:
    qid = q.get("id", "?")
    sec = q.get("secenekler") or {}
    if list(sec) != list("ABCDE") or len({norm(str(v)) for v in sec.values()}) != 5:
        den.hata(f"{qid}: şıklar A–E tam ve tekrarsız olmalı")
    if q.get("dogru") not in list("ABCDE"):
        den.hata(f"{qid}: dogru A–E olmalı")
    sa = q.get("sik_aciklamalari") or {}
    if sorted(sa) != list("ABCDE") or any(len(str(v).strip()) < 20 for v in sa.values()):
        den.hata(f"{qid}: her şıkkın gerekçeli açıklaması (≥20 karakter) gerekli")
    if len(str(q.get("aciklama", "")).strip()) < 20:
        den.hata(f"{qid}: açıklama kısa")
    if len(str(q.get("soru", "")).strip()) < 15:
        den.hata(f"{qid}: kök kısa")
    if q.get("zorluk") not in ("kolay", "orta", "zor"):
        den.hata(f"{qid}: zorluk")
    if not isinstance(q.get("kazanim"), int) or not 1 <= q["kazanim"] <= kaz:
        den.hata(f"{qid}: kazanım 1–{kaz} olmalı")
    if not isinstance(q.get("bilgi"), list):
        den.hata(f"{qid}: bilgi liste olmalı")
    for c in q.get("benzer_cikmis") or []:
        if c not in cik:
            den.hata(f"{qid}: benzer_cikmis {c} çıkmış adaylarında yok")
    den.kanit(q.get("kanit"), f"soru {qid}")
from collections import Counter  # noqa: E402
for kn in sorted({q.get("kazanim") for q in sorular if isinstance(q.get("kazanim"), int)}):
    z = Counter(q.get("zorluk") for q in sorular if q.get("kazanim") == kn)
    if any(z[x] < 1 for x in ("kolay", "orta", "zor")):
        den.hata(f"K{kn}: kolay/orta/zor her biri en az 1 olmalı ({dict(z)})")
    elif sum(z.values()) > 3 and z["orta"] < max(z["kolay"], z["zor"]):
        den.hata(f"K{kn}: orta sayısı kolay ve zordan az olmamalı ({dict(z)})")
kokler = [norm(q.get("soru", "")) for q in sorular]
for k in {k for k in kokler if kokler.count(k) > 1}:
    den.hata(f"tekrarlayan kök: {k[:60]}")
for h in den.hatalar[:80]:
    print("HATA", h)
print(f"{f.name}: {len(sorular)} soru · {len(den.hatalar)} HATA")
sys.exit(1 if den.hatalar else 0)
