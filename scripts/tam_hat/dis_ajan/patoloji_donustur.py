#!/usr/bin/env python3
"""Patoloji soru biçimi → dış ajan örnek soru biçimi (icerik_kontrol 'ornek' kapısı için). LLM yok.

  python3 scripts/tam_hat/dis_ajan/patoloji_donustur.py <sorular.json> <ornek_sorular.json> <ders>-ag-<etiket>

sorular.json (patoloji_soru_isci biçimi): [{onem_id,kalip,kok,siklar[5],cevap,aciklama{A..E},kaynak{sayfa,metin},celdirici_kaynak}]
Çıktı soru id'si `<önek>-q01…`; `kazanim_id` = onem_id (profil/vurgu kimliği). Doğru şık metni `secenekler[dogru]`.
"""
import json
import sys
from pathlib import Path

if len(sys.argv) != 4:
    print(__doc__)
    sys.exit(2)
girdi = json.loads(Path(sys.argv[1]).read_text("utf8"))
girdi = girdi["sorular"] if isinstance(girdi, dict) else girdi
out = []
for n, q in enumerate(girdi, 1):
    h = "ABCDE"
    out.append({
        "id": f"{sys.argv[3]}-q{n:02d}", "kazanim_id": q.get("onem_id"), "zorluk": "orta", "kalip": q.get("kalip"),
        "soru": q["kok"], "secenekler": dict(zip(h, q["siklar"])), "dogru": q["cevap"],
        "aciklama": q["aciklama"][q["cevap"]], "sik_aciklamalari": q["aciklama"],
    })
Path(sys.argv[2]).write_text(json.dumps({"kazanimlar": [{"id": "patoloji", "sorular": out}]}, ensure_ascii=False, indent=1), "utf8")
print(f"{len(out)} soru dönüştürüldü → {sys.argv[2]}")
