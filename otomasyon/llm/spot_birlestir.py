#!/usr/bin/env python3
"""Görev parçalarını ders zincirinin beklediği dosyalara birleştirir (R4; ICERIK_MOTORU_V3.md §14).

  spot_birlestir.py onem   W kod   → W/gorev/<kod>/onem_parca_*.json → W/onem/<kod>.json      (onem_dogrula.py 0 HATA)
  spot_birlestir.py cozucu W kod   → W/gorev/<kod>/cozucu_parti_*.json → W/cozucu/<kod>.json  (cozucu_dogrula.py 0 HATA)

Ders düzeyi biçim kuralları BETİKLE sağlanır (model sıralamayı/içeriği verir, ölçeği betik kurar):
  - puan bantları (90–100'de 4–8, 80–89 … 50–59'da ≥2): modelin puan SIRALAMASI korunarak bantlara yeniden ölçeklenir;
  - doğru harf dengesi: örnek soruların şıkları yer değiştirerek dağıtılır (açıklamasında harf anılan soruya dokunulmaz);
  - örnek sayısı üst sınırı aşılırsa en düşük puanlı maddelerden kırpılır; alt sınırın altındaysa HATA (parça yeniden üretilir);
  - başlık/pdf (girdi), özet (parça özetleri), "neden önemli" (çıkmış istatistiği) alanları.
Çıktı yazılmadan önce resmî doğrulayıcı geçici dosyada koşar; HATA varsa hedef dosya DEĞİŞMEZ (çıkış 1).
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from llm import cekirdek as c  # noqa: E402
from llm.gorevler import _spot  # noqa: E402

HARF = "ABCDE"


def bant_olcekle(maddeler: list[dict]) -> None:
    """Model puan sırasını koruyarak bant kurallarını sağlar (yerinde)."""
    n = len(maddeler)
    sira = sorted(range(n), key=lambda i: (-(maddeler[i].get("puan") or 0), i))
    k9 = max(4, min(8, round(0.18 * n)))
    model_bant = [min((maddeler[i].get("puan") or 0) // 10, 8) for i in sira[k9:]]
    say = Counter(model_bant)
    hedef = {b: max(2, say.get(b, 0)) if b in (8, 7, 6, 5) else say.get(b, 0) for b in range(8, -1, -1)}
    fazla = sum(hedef.values()) - (n - k9)
    for b in [0, 1, 2, 3, 4, 8, 7, 6, 5]:              # fazlayı önce alt bantlardan, sonra kalabalık üst bantlardan düş
        while fazla > 0 and hedef[b] > (2 if b in (8, 7, 6, 5) else 0):
            hedef[b] -= 1; fazla -= 1
    while fazla < 0:                                    # eksik: en alt dolu banda ekle
        b = min((b for b in hedef if hedef[b] or b == 5), default=5); hedef[b] += 1; fazla += 1
    bantlar = [9] * k9 + [b for b in range(8, -1, -1) for _ in range(hedef[b])]
    for b in set(bantlar):
        idx = [sira[j] for j, x in enumerate(bantlar) if x == b]
        ust, alt = (100, 90) if b == 9 else (b * 10 + 9, b * 10)
        for k, i in enumerate(idx):
            maddeler[i]["puan"] = round(ust - (ust - alt) * (k / max(len(idx) - 1, 1)))


def harf_dengele(maddeler: list[dict]) -> int:
    """Doğru şık harflerini döngüyle dağıtır (şık yeri değişir); açıklaması harf anan soruya dokunmaz."""
    n = 0
    hedefler = [HARF[(i * 3 + 1) % 5] for i in range(200)]
    k = 0
    for m in maddeler:
        for q in m.get("ornek") or []:
            if re.search(r"\b[A-E]\)|\b[A-E] şıkk|şık(kı)? [A-E]\b", q.get("aciklama", "")) or q.get("dogru") not in q.get("secenekler", {}):
                continue
            h = hedefler[k]; k += 1
            if h != q["dogru"]:
                s = q["secenekler"]
                s[h], s[q["dogru"]] = s[q["dogru"]], s[h]
                q["dogru"] = h; n += 1
    return n


def onem(W: Path, kod: str, log=print) -> int:
    sys.path.insert(0, str(c.KOK / "scripts" / "spot_cozucu"))
    import onem_dogrula as OD
    plan = _spot.parca_plani(W, kod)
    parcalar = []
    for i in range(len(plan["parcalar"])):
        p = W / "gorev" / kod / f"onem_parca_{i}.json"
        if not p.exists():
            log(f"{kod}: parça {i} yok ({p}) — önce onem_listesi görevi"); return 2
        parcalar.append(c.oku(p))
    g = json.loads((W / "girdi" / f"{kod}.json").read_text(encoding="utf-8"))
    C = {x["id"]: x for x in _spot.cikmislar(W, kod)}
    maddeler = [m for p in parcalar for m in p["maddeler"]]
    for i, m in enumerate(maddeler, 1):
        m["id"] = f"{kod}-{i:02d}"
        for k in [k for k in m if k.startswith("_")]:
            m.pop(k)
    bant_olcekle(maddeler)
    # örnek üst sınırı
    kullanilan = {cc for m in maddeler for cc in m["cikmis"]}
    alt_s, ust_s = max(g["ornek_hedef"], 20 - len(kullanilan)), g["ornek_hedef"] + 6
    orn = sum(len(m["ornek"]) for m in maddeler)
    for m in sorted(maddeler, key=lambda m: m["puan"]):
        while orn > ust_s and m["ornek"]:
            m["ornek"].pop(); orn -= 1
    degisen = harf_dengele(maddeler)
    elenen = [x for p in parcalar for x in p["elenen_cikmis"]]
    # çıkmış–çıkmış tekrarı (parçalar birbirini görmez): aynı bilgiyi soran ikinciler tekrar:<ilk> olarak elenir
    imza = {cid: OD.soru_imza(C[cid]["kok"], C[cid]["secenekler"], C[cid]["dogru"]) for cid in kullanilan if cid in C}
    sira_c = sorted(imza, key=lambda x: (-(1 + len(C[x].get("tekrar") or [])), x))
    tekrar = {}
    for i, a in enumerate(sira_c):
        if a in tekrar:
            continue
        for b in sira_c[i + 1:]:
            if b not in tekrar and OD.benzer(imza[a], imza[b]) >= 0.8:
                tekrar[b] = a
    for m in maddeler:
        m["cikmis"] = [x for x in m["cikmis"] if x not in tekrar]
    elenen += [{"id": b, "neden": f"tekrar:{a}", "not": f"{a} ile aynı bilgiyi soruyor"} for b, a in tekrar.items()]
    kullanilan -= set(tekrar)
    yillar = sorted({y for cid in kullanilan for y in (C.get(cid, {}).get("yillar") or [C.get(cid, {}).get("yil", "")]) if y})
    en_cok = [m["baslik"] for m in sorted(maddeler, key=lambda m: -len(m["cikmis"])) if m["cikmis"]][:3]
    ozet = " ".join(p.get("parca_ozeti", "") for p in parcalar if p.get("parca_ozeti"))
    neden = (f"Bu dersten {len(kullanilan)} farklı çıkmış soru {yillar[0][:4]}–{yillar[-1][-4:]} sınavlarında soruldu; "
             f"en çok {', '.join(en_cok)} konuları soruluyor." if kullanilan and yillar else
             "Bu dersin bilgisi sınavda tanım, en sık görülen durumlar ve tedavi seçimi biçiminde soruluyor.")
    o = {"kod": kod, "baslik": re.sub(r"^\s*\d+\s*[).-]\s*|\.pdf$", "", g["ad"]).strip(), "pdf": g["ad"],
         "ozet": ozet, "neden_onemli": neden, "maddeler": maddeler, "elenen_cikmis": elenen,
         "_kaynak": {"yontem": "gorev", "parca": len(parcalar), "harf_degisen": degisen}}
    with tempfile.TemporaryDirectory(prefix="onem_birlestir_") as t:
        T = Path(t)
        for alt, uz in (("pdf_metin", "md"), ("girdi", "json"), ("cikmis", "json")):
            (T / alt).mkdir()
            if (W / alt / f"{kod}.{uz}").exists():
                (T / alt / f"{kod}.{uz}").symlink_to(W / alt / f"{kod}.{uz}")
        (T / "onem").mkdir()
        (T / "onem" / f"{kod}.json").write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")
        e, w, s = OD.check(T / "onem" / f"{kod}.json")
    for x in e:
        log(f"  HATA {x}")
    log(f"{kod}: {s} · {len(e)} HATA · {len(w)} UYARI · harf dengesi için {degisen} soru düzenlendi")
    if e:
        c.yaz(W / "gorev" / kod / "onem_birlesik_hatali.json", o)
        return 1
    c.yaz(W / "onem" / f"{kod}.json", o)
    return 0


def main():
    if len(sys.argv) < 4 or sys.argv[1] not in ("onem", "cozucu"):
        print(__doc__); return 2
    W, kod = Path(sys.argv[2]), sys.argv[3]
    if sys.argv[1] == "onem":
        return onem(W, kod)
    from llm.gorevler import cozucu_sorusu
    return cozucu_sorusu.birlestir(W, kod)


if __name__ == "__main__":
    sys.exit(main())
