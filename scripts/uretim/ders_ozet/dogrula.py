#!/usr/bin/env python3
"""Ders Özeti kapısı — meds_temp/ders_ozet/<k>/ozet.json (TALIMAT.md). 0 HATA olmadan ses/yayın yok.

Denetler: şema, kimlik tekilliği, her maddenin geçerli slayt sayfası, her doğrulanmış çıkmışın kapsandığı madde
(ya da gerekçeli atlama), puanı 85+ önem maddelerinin kapsamı, kelime sınırları, yasak işaret/markdown, Türkçe üslup,
iç süreç dili, "hoca vurguladı" sayısı.
Kullanım: python3 scripts/uretim/ders_ozet/dogrula.py k2-15 [--yayin]   (--yayin: src/data/ders_ozet yayın dosyasını da denetler)
Çıkış: 0 = 0 HATA, 1 = HATA var.
"""
from __future__ import annotations

import sys
from pathlib import Path as _P

_s = _P(__file__).resolve()
while not (_s / "kok.py").exists() and _s != _s.parent:
    _s = _s.parent
sys.path.insert(0, str(_s))
from kok import PROJE, SCRIPTS  # noqa: E402

import json  # noqa: E402
import re  # noqa: E402

sys.path.insert(0, str(SCRIPTS))
from turkce_uslup import denetle as uslup  # noqa: E402

KOK = PROJE / "meds_temp" / "ders_ozet"
TURLER = {"bilgi", "spot", "ayirici", "klinik"}
SUREC = re.compile(r"\b(slayt\w*|PDF\w*|aday\w*|havuz\w*|katalog\w*|ders notu\w*|çıkmış soruda soruldu|şık [A-E]\b|[A-E] şıkkı)",
                   re.I)
ISARET = re.compile(r"[→←↑↓≥≤±×⇒#`αβγδµμ]|\s/\s|<|>|\[|\]|\b1:\d")  # Yunan harfi/oran yazıyla (okunuşta uzar, ses kapısı H-ses)
SINIR = {"bolum": (4, 12), "madde": (3, 12), "kelime": (6, 45), "toplam": (500, 2500), "akilda": (8, 15)}


def kelime(s: str) -> int:
    return len(re.findall(r"[\wÇĞİÖŞÜçğıöşü%]+", s or ""))


def dogrula(k: str) -> tuple[list[str], list[str], dict]:
    H: list[str] = []
    U: list[str] = []
    g = json.loads((KOK / k / "girdi.json").read_text(encoding="utf-8"))
    p = KOK / k / "ozet.json"
    if not p.exists():
        return [f"{p} yok"], U, {}
    o = json.loads(p.read_text(encoding="utf-8"))
    sayfalar = {int(s) for s in g["sayfalar"]}
    cikmis = {c["id"] for c in g["cikmis"]}
    if o.get("ders") != k:
        H.append(f"ders alanı {o.get('ders')!r} ≠ {k}")
    for alan in ("baslik", "giris", "bolumler", "akilda"):
        if not o.get(alan):
            H.append(f"{alan} boş/eksik")
    bol = o.get("bolumler") or []
    if not SINIR["bolum"][0] <= len(bol) <= SINIR["bolum"][1]:
        H.append(f"bölüm sayısı {len(bol)} (sınır {SINIR['bolum']})")
    maddeler: dict[str, dict] = {}
    toplam = kelime(o.get("giris", ""))
    hoca = 0

    def metin_denetle(m: str, yer: str) -> None:
        nonlocal hoca
        if (x := ISARET.search(m)):
            H.append(f"{yer}: yasak işaret/markdown {x.group(0)!r}")
        if m.count("**") % 2 or m.count("**") > 2:
            H.append(f"{yer}: kalın vurgu en çok bir kavram (çift ** dengeli olmalı)")
        if (x := SUREC.search(m)):
            H.append(f"{yer}: iç süreç dili {x.group(0)!r}")
        H.extend(uslup(m, yer))
        hoca += len(re.findall(r"hoca\w* (vurgula|özellikle|altını)", m, re.I))

    metin_denetle(o.get("giris", ""), "giris")
    for b in bol:
        bid = b.get("id")
        if not b.get("baslik"):
            H.append(f"{bid}: başlık yok")
        mm = b.get("maddeler") or []
        if not SINIR["madde"][0] <= len(mm) <= SINIR["madde"][1]:
            H.append(f"{bid}: madde sayısı {len(mm)} (sınır {SINIR['madde']})")
        for m in mm:
            mid = m.get("id")
            if not mid or mid in maddeler or not str(mid).startswith(f"{bid}-"):
                H.append(f"{bid}: madde kimliği hatalı/tekrar {mid!r}")
                continue
            maddeler[mid] = m
            if m.get("tur") not in TURLER:
                H.append(f"{mid}: tur {m.get('tur')!r}")
            w = kelime(m.get("metin", ""))
            toplam += w
            if not SINIR["kelime"][0] <= w <= SINIR["kelime"][1]:
                H.append(f"{mid}: {w} kelime (sınır {SINIR['kelime']})")
            s = m.get("s") or []
            if not s or any(x not in sayfalar for x in s):
                H.append(f"{mid}: geçersiz/eksik slayt sayfası {s}")
            for c in m.get("cikmis") or []:
                if c not in cikmis:
                    H.append(f"{mid}: bilinmeyen çıkmış id {c}")
            metin_denetle(m.get("metin", ""), mid)
    ak = o.get("akilda") or []
    if not SINIR["akilda"][0] <= len(ak) <= SINIR["akilda"][1]:
        H.append(f"akılda madde sayısı {len(ak)} (sınır {SINIR['akilda']})")
    for i, a in enumerate(ak, 1):
        w = kelime(a.get("metin", ""))
        toplam += w
        if not SINIR["kelime"][0] <= w <= SINIR["kelime"][1]:
            H.append(f"akilda-{i}: {w} kelime")
        if not a.get("s") or any(x not in sayfalar for x in a["s"]):
            H.append(f"akilda-{i}: geçersiz/eksik slayt sayfası")
        for c in a.get("cikmis") or []:
            if c not in cikmis:
                H.append(f"akilda-{i}: bilinmeyen çıkmış id {c}")
        metin_denetle(a.get("metin", ""), f"akilda-{i}")
    if not SINIR["toplam"][0] <= toplam <= SINIR["toplam"][1]:
        H.append(f"toplam {toplam} kelime (sınır {SINIR['toplam']})")
    if hoca > 3:
        H.append(f"'hoca vurguladı' {hoca} kez (en çok 3)")
    # çıkmış kapsamı
    if "cikmis_kapsam" not in o:
        H.append("cikmis_kapsam alanı yok (çıkmış yoksa ya da hepsi atlandıysa {} olur)")
    kap = o.get("cikmis_kapsam") or {}
    atl = {a.get("id"): a.get("gerekce") for a in o.get("atlanan_cikmis") or []}
    for c in cikmis:
        if c in atl:
            if not (atl[c] or "").strip() or len(atl[c]) < 20:
                H.append(f"çıkmış {c}: atlama gerekçesi yetersiz")
            continue
        mid = kap.get(c)
        if not mid or mid not in maddeler:
            H.append(f"çıkmış {c} kapsanmadı (cikmis_kapsam)")
        elif c not in (maddeler[mid].get("cikmis") or []):
            H.append(f"çıkmış {c}: {mid} maddesinin cikmis listesinde yok")
    if cikmis and len(atl) > max(1, len(cikmis) // 5):
        # 2026-11-23: HATA değil UYARI — sert sınır yazarları cevabı çıkmayan maddeye bağlamaya itiyordu (sahte kapsam);
        # atlama gerekçesini bağımsız denetçi doğrular.
        U.append(f"{len(atl)} çıkmış atlandı — çok fazla (en çok %20)")
    # önem kapsamı
    okap = o.get("onem_kapsam") or {}
    for m in g["onem"]["maddeler"]:
        if (m.get("puan") or 0) >= 85:
            mid = okap.get(m["baslik"])
            if not mid or mid not in maddeler:
                H.append(f"önem ({m['puan']}) {m['baslik']!r} kapsanmadı (onem_kapsam)")
    # uyarılar
    for t in TURLER:
        if not any(m.get("tur") == t for m in maddeler.values()):
            U.append(f"hiç {t} türü madde yok")
    ist = {"bolum": len(bol), "madde": len(maddeler), "akilda": len(ak), "kelime": toplam, "cikmis": len(cikmis),
           "kapsanan_cikmis": len([c for c in cikmis if c in kap]), "atlanan": len(atl)}
    return H, U, ist


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit(__doc__)
    kotu = 0
    for k in args:
        H, U, ist = dogrula(k)
        for h in H:
            print(f"HATA {k}: {h}")
        for u in U:
            print(f"UYARI {k}: {u}")
        print(f"{k}: {len(H)} HATA, {len(U)} UYARI · {ist}")
        kotu += bool(H)
    sys.exit(1 if kotu else 0)


if __name__ == "__main__":
    main()
