#!/usr/bin/env python3
"""
Sınav Çalışması verisini sayfanın yükleyebileceği küçük parçalara böler.

Girdi : src/data/sinav_calisma_k1.json   (sinav_calisma_olustur.py üretir, ~38 MB — pakete GİRMEZ)
Çıktı : src/data/sinav_calisma/k1/index.json        ders → konu → kazanım özeti (soru sayıları, zorluk dağılımı)
        src/data/sinav_calisma/k1/<ders>-<konu>.json   o konunun kazanım ayrıntısı + soruları (açılınca yüklenir)

Ön yüzde kullanılmayan *_ses alanları (kok/secenek/siklar/ipucu/cozum) atılır; sesli çözücü metni kendisi okunur.
Kazanıma bağlı çıkmış sorular aynı soru biçimine çevrilip `tur: "cikmis"` ile eklenir.
Kullanım: python3 scripts/sinav_calisma_bol.py   (sinav_calisma_olustur.py sonunda da çağrılır)
"""
import json
import re
import shutil
from pathlib import Path

MEDS = Path(__file__).resolve().parent.parent
KAYNAK = MEDS / "src/data/sinav_calisma_k1.json"
HEDEF = MEDS / "src/data/sinav_calisma/k1"
HARFLER = "ABCDE"


def yaz(yol: Path, veri) -> None:
    yol.write_text(json.dumps(veri, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def kz_no(kz: dict, sira: int) -> int:
    m = re.search(r"kz-(\d+)$", kz.get("id", ""))
    return int(m.group(1)) if m else sira


def ornek(s: dict) -> dict:
    o = {
        "id": s["id"],
        "zorluk": s.get("zorluk") or "orta",
        "soru": s["soru"],
        "secenekler": {h: v for h, v in (s.get("secenekler") or {}).items() if h in HARFLER and v},
        "dogru": s.get("dogru"),
        "aciklama": s.get("aciklama") or "",
    }
    if s.get("sik_aciklamalari"):
        o["siklar"] = s["sik_aciklamalari"]
    if s.get("ipucu"):
        o["ipucu"] = s["ipucu"]
    return o


def cikmis(s: dict) -> dict | None:
    secenekler = {x["key"]: x["text"] for x in s.get("options") or [] if x.get("key") in HARFLER and x.get("text")}
    if not s.get("stem") or len(secenekler) < 2 or s.get("correctAnswer") not in secenekler:
        return None
    o = {
        "id": s["id"],
        "tur": "cikmis",
        "zorluk": "orta",
        "soru": s["stem"],
        "secenekler": secenekler,
        "dogru": s["correctAnswer"],
        "aciklama": s.get("explanation") or "",
    }
    if s.get("year"):
        o["yil"] = s["year"]
    return o


def main() -> None:
    veri = json.loads(KAYNAK.read_text(encoding="utf-8"))
    if HEDEF.exists():
        shutil.rmtree(HEDEF)
    HEDEF.mkdir(parents=True)

    dizin = {"kurul": veri.get("kurul", 1), "ad": veri.get("name", ""), "kod": veri.get("code", ""), "dersler": []}
    toplam_soru = toplam_kz = 0
    for di, ders in enumerate(veri["dersler"], 1):
        d_ozet = {"ad": ders["ders"], "konular": []}
        for ki, konu in enumerate(ders["konular"], 1):
            dosya = f"{di}-{ki}"
            k_ozet = {"ad": konu["konu"], "dosya": dosya, "kazanimlar": []}
            k_ayrinti = []
            for si, kz in enumerate(konu["kazanimlar"], 1):
                sorular = [ornek(s) for s in kz.get("ornekSorular") or [] if s.get("soru") and s.get("dogru")]
                sorular += [c for c in (cikmis(s) for s in kz.get("cikmisSorular") or []) if c]
                zd = {"kolay": 0, "orta": 0, "zor": 0}
                for s in sorular:
                    if s.get("tur") != "cikmis":
                        zd[s["zorluk"] if s["zorluk"] in zd else "orta"] += 1
                k_ozet["kazanimlar"].append({
                    "id": kz["id"],
                    "no": kz_no(kz, si),
                    "metin": kz["metin"],
                    "soru": len(sorular),
                    "cikmis": sum(1 for s in sorular if s.get("tur") == "cikmis"),
                    "zorluk": zd,
                })
                ayr = {"id": kz["id"], "sorular": sorular}
                if kz.get("kisa_anlatim"):
                    ayr["anlatim"] = kz["kisa_anlatim"]
                slaytlar = [
                    {"sayfa": s.get("sayfa"), "baslik": s.get("alinti", ""), "deck": s.get("deckId")}
                    for s in kz.get("slaytlar") or [] if s.get("deckId")
                ]
                if slaytlar:
                    ayr["slaytlar"] = slaytlar
                k_ayrinti.append(ayr)
                toplam_soru += len(sorular)
                toplam_kz += 1
            yaz(HEDEF / f"{dosya}.json", {"kazanimlar": k_ayrinti})
            d_ozet["konular"].append(k_ozet)
        dizin["dersler"].append(d_ozet)
    dizin["toplam"] = {"kazanim": toplam_kz, "soru": toplam_soru}
    yaz(HEDEF / "index.json", dizin)
    boyut = sum(p.stat().st_size for p in HEDEF.glob("*.json"))
    en_buyuk = max(HEDEF.glob("*.json"), key=lambda p: p.stat().st_size)
    print(f"{toplam_kz} kazanım, {toplam_soru} soru → {len(list(HEDEF.glob('*.json')))} dosya, "
          f"{boyut / 1e6:.1f} MB (en büyük {en_buyuk.name} {en_buyuk.stat().st_size / 1e6:.2f} MB, "
          f"dizin {(HEDEF / 'index.json').stat().st_size / 1e3:.0f} KB)")


if __name__ == "__main__":
    main()
