#!/usr/bin/env python3
"""nereye.py — serbest görev metninden okunacak dosyaları bulur (stdlib, LLM yok).

  python3 scripts/altyapi/nereye.py "k2-30 pdf geldi tam hat"
  python3 scripts/altyapi/nereye.py --liste | --json "<metin>" | --denetle
  python3 scripts/altyapi/nereye.py hata "<sorgu>"   # yalnız ilgili hata maddeleri (docs/hatalar/_dizin.json)
Katalog: docs/yonlendirme.json (yollar meds/ köküne göre).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_d = Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
sys.path.insert(0, str(_d))
import kok as _kok  # noqa: E402

MEDS = _kok.MEDS
KATALOG = MEDS / "docs" / "yonlendirme.json"
AGENTS = _kok.PROJE / "AGENTS.md"
TR = str.maketrans("ıİşŞğĞüÜöÖçÇâÂîÎûÛ", "iissgguuoocCaaiiuu")


def katla(s: str) -> str:
    s = s.translate(TR).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def yukle() -> list[dict]:
    return json.loads(KATALOG.read_text(encoding="utf-8"))["gorevler"]


def puanla(metin: str, g: dict) -> float:
    m = katla(metin)
    kel = set(m.split())
    p = 0.0
    for a in g["anahtarlar"] + [g["ad"]]:
        a = katla(a)
        if not a:
            continue
        if " " in a:
            if re.search(rf"\b{re.escape(a)}\b", m):
                p += 3 + len(a.split())
        elif a in kel:
            p += 3
        elif len(a) >= 4 and any(k.startswith(a) or (len(k) >= 4 and a.startswith(k)) for k in kel):
            p += 1.5  # Türkçe ek: "dağıt" ~ "dağıtım", "sözlükte" ~ "sözlük"
    return p


HATA_DIZIN = MEDS / "docs" / "hatalar" / "_dizin.json"


# Belirti dili → maddelerde geçen teknik kelimeler (kullanıcı "kayıyor" der, madde "zamanlama/senkron" yazar)
ES_ANLAM = {
    "kayiyor": "zamanlama senkron erken gec cumle aktif", "kayma": "zamanlama senkron erken gec cumle aktif",
    "erken": "zamanlama senkron", "gec": "zamanlama senkron", "donuyor": "donma performans takilma",
    "takiliyor": "takilma performans donma", "yavas": "performans hantal", "bos": "eksik bulunamadi",
    "cokuyor": "coker hata cikis", "kayboluyor": "katman kaybolur dagitim", "gorunmuyor": "gorunmez katman eksik",
    "cizim": "cizim capa kontur lazer", "ses": "ses ema klip", "dagit": "dagitim oracle dagit",
}


def hata_ara(sorgu: str, dosyalar: list[str] | None = None, n: int = 8) -> list[tuple[float, dict]]:
    """Sorgu kelimelerini madde anahtarlarıyla puanlar (IDF ağırlıklı: tam kelime, başlıkta ×1.5, 5 harf kök ×0.6)."""
    if not HATA_DIZIN.exists():
        return []
    maddeler = json.loads(HATA_DIZIN.read_text(encoding="utf-8"))["maddeler"]
    kel = [k for k in katla(sorgu).split() if len(k) >= 2]
    kel += [w for k in list(kel) for w in ES_ANLAM.get(k, "").split() if w not in kel]
    idler = {k.upper() for k in kel if re.fullmatch(r"h\d+", k)}
    import math
    hazir = []
    df: dict[str, int] = {}
    for m in maddeler:
        anah = {katla(a) for a in m["anahtarlar"]}
        tek = {w for a in anah for w in a.split()}
        kok = {w[:5] for w in tek if len(w) >= 5}
        for w in tek | {"~" + k for k in kok}:
            df[w] = df.get(w, 0) + 1
        hazir.append((m, anah, tek, kok, set(katla(m["baslik"]).split())))
    N = len(maddeler)

    def idf(w: str) -> float:
        return math.log(1 + N / (1 + df.get(w, 0)))

    sonuc = []
    for m, anah, tek, kok, bas in hazir:
        p = 0.0
        esles = 0
        for k in kel:
            if len(k) < 3:
                continue
            if k in tek:
                p += idf(k) * (1.5 if k in bas else 1.0)
                esles += 1
            elif len(k) >= 5 and k[:5] in kok:
                p += idf("~" + k[:5]) * (0.9 if any(w[:5] == k[:5] for w in bas) else 0.6)
                esles += 1
        p *= (esles / max(1, sum(len(k) >= 3 for k in kel))) ** 0.5  # çok terim kapsayan öne
        konu = set(katla(Path(m["dosya"]).stem).split())
        if konu & set(kel):
            p *= 1.6  # sorgu konu dosyasını adlandırıyor (cizim, ses, ...)
        if m["id"] in idler:
            p += 10
        if p and dosyalar and m["dosya"] in dosyalar:
            p *= 1.15
        if p >= 4:
            sonuc.append((p, m))
    sonuc.sort(key=lambda x: (-x[0], x[1]["kelime"]))
    return sonuc[:n]


def bas_hatalar(bulgu: list[tuple[float, dict]]) -> str:
    s = ["İlgili hatalar (yalnız bu aralıkları oku: Read offset=satır_baş limit=satır_son-satır_baş+1):"]
    s += [f"  {m['baslik'][:110]} — {m['dosya']}:{m['satir_bas']}-{m['satir_son']} ({m['kelime']} kelime)"
          for _, m in bulgu]
    return "\n".join(s)


_YOL = re.compile(r"(?:scripts|docs|otomasyon)/[\w./-]+\.(?:py|sh|mjs|mts|md|json)")


def var_mi(metin: str) -> bool:
    """Metindeki somut yolların hepsi diskte var mı (yer tutucu <...> ve * içerenler sayılmaz)."""
    return all((MEDS / y).exists() for y in _YOL.findall(metin) if "<" not in y and "*" not in y)


def suz(g: dict) -> dict:
    """Diskte olmayan yolu öneren oku/kapı satırlarını eler (önerilmiş ama yazılmamış betikler)."""
    g = dict(g)
    g["oku"] = [o for o in g["oku"] if var_mi(o["yol"])]
    g["kapilar"] = [k for k in g["kapilar"] if var_mi(k)]
    return g


def bas(g: dict) -> str:
    s = [f"## {g['ad']}  [{g['id']}]", "Oku:"]
    s += [f"  {i}. {o['yol']} — {o['neden']}" for i, o in enumerate(g["oku"], 1)]
    if g["kurallar"]:
        s.append("Kurallar (AGENTS.md): " + ", ".join(g["kurallar"]))
    if g["kapilar"]:
        s.append("Kapılar:")
        s += [f"  $ {k}" for k in g["kapilar"]]
    if g["hatalar"]:
        s.append("Hatalar: " + ", ".join(g["hatalar"]))
    if g.get("asama"):
        s.append(f"Aşama özeti: python3 scripts/hat/tam_hat/kural_secici.py --oku {g['asama']}")
    return "\n".join(s)


def denetle(gorevler: list[dict]) -> int:
    hata = []
    metin = AGENTS.read_text(encoding="utf-8") if AGENTS.exists() else ""
    kurallar = set(re.findall(r"^(\d+[a-z]?)\. ", metin, re.M))
    if not metin:
        hata.append(f"AGENTS.md yok: {AGENTS}")
    idler = set()
    for g in gorevler:
        if g["id"] in idler:
            hata.append(f"{g['id']}: yinelenen id")
        idler.add(g["id"])
        if len(g["oku"]) > 6:
            hata.append(f"{g['id']}: oku > 6")
        for y in [o["yol"] for o in g["oku"]] + g["hatalar"]:
            if not (MEDS / y).exists():
                hata.append(f"{g['id']}: yol yok {y}")
        for k in g["kurallar"]:
            if k not in kurallar:
                hata.append(f"{g['id']}: kural {k} AGENTS.md'de yok")
        if g.get("asama") == "genel" or g.get("asama") and not (MEDS / "docs/asama_kurallari" / f"{g['asama']}.md").exists():
            hata.append(f"{g['id']}: aşama {g['asama']} yok")
    for h in hata:
        print("HATA", h)
    print(f"{len(gorevler)} görev, {len(hata)} HATA")
    return 1 if hata else 0


def main(argv: list[str]) -> int:
    if argv[:1] == ["hata"]:
        sorgu = " ".join(argv[1:])
        bulgu = hata_ara(sorgu)
        print(bas_hatalar(bulgu) if bulgu else "Eşleşen hata maddesi yok.")
        return 0
    gorevler = yukle()
    if "--denetle" in argv:
        return denetle(gorevler)
    if "--liste" in argv:
        for g in gorevler:
            print(f"{g['id']:<18} {g['ad']}")
        return 0
    js = "--json" in argv
    metin = " ".join(a for a in argv if not a.startswith("--"))
    if not metin:
        print(__doc__)
        return 2
    sirali = sorted(((puanla(metin, g), g) for g in gorevler), key=lambda x: -x[0])
    en = sirali[0][0]
    secilen = [suz(g) for p, g in sirali[:2] if p > 0 and p >= en * 0.6]
    hsorgu = metin + " " + " ".join(a for g in secilen for a in g["anahtarlar"][:6])
    bulgu = hata_ara(hsorgu, [h for g in secilen for h in g["hatalar"]]) if secilen else hata_ara(metin)
    if js:
        print(json.dumps({"sorgu": metin, "gorevler": secilen, "hatalar": [
                              {k: m[k] for k in ("id", "baslik", "dosya", "satir_bas", "satir_son", "kelime")} for _, m in bulgu],
                          "oneri": [g["id"] for _, g in sirali[:3]] if not secilen else []},
                         ensure_ascii=False, indent=1))
        return 0
    if not secilen:
        print("Eşleşme yok. En yakın görevler: " + ", ".join(g["id"] for _, g in sirali[:3]))
        print("Haritalar: scripts/HARITA.md (betikler), docs/HARITA.md (belgeler), "
              "docs/KURUL2_YAPILMAYACAK_HATALAR.md (hatalar); tüm liste: --liste")
        if bulgu:
            print(bas_hatalar(bulgu))
        return 0
    print("\n\n".join(bas(g) for g in secilen))
    if bulgu:
        print("\n" + bas_hatalar(bulgu))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
