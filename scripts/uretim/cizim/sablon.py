"""Canlı çizim panel şablonları (docs/CIZIM_KURALLARI.md §2b; kullanıcı 2026-10-24).

Panel, anlatılan tıbbi ilişkinin anlamına göre bir şablona bağlanır (`sablonlar.json`): örn. "durum → bakılacak tetkik"
başlıklı tablodur, okla "hastalık testi doğurur" gibi okunmaz. Şablonlar dersten bağımsızdır; model uygun şablon
bulamazsa `yeni_sablon` önerir, kapıdan geçen öneri kütüphaneye eklenir ve sonraki derslerde de kullanılır.
Düzenler istemcide (CizimLayer.SablonPanel) geneldir; yeni şablon için kod değişmez.

Komut biçimi (tur "sema" + "sablon"):
  tablo   : "satirlar": [["hücre", "hücre"], ...]          (sütun sayısı = başlık sayısı)
  karsit  : "kutuplar": ["A", "B"], "satirlar": [["özellik", "A'da", "B'de"], ...]
  zincir  : "ogeler": ["A", "B", "C"]                        (bag: oklar üstündeki söz, şablondan ya da "baglar")
  adimlar : "ogeler": ["1. adım", "2. adım", ...]
  liste   : "baslik": "üst başlık", "ogeler": ["alt tür", ...]
  grup    : "kaynaklar": ["A", "B"], "sonuc": "C"
  dal     : "soru": "koşul?", "dallar": [["evet", "sonuç"], ["hayır", "sonuç"]]
  maske   : "gorunen": "A", "altta": ["B", "C"]
  deger   : "deger": "3", "birim": "g/dL", "aciklama": "eksüda/transüda protein eşiği", "cikmis": 2 (isteğe bağlı;
            yalnız doğrulanmış çıkmış eşlemesi sayısı — kural 21)
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

YOL = Path(__file__).resolve().parent / "sablonlar.json"


def kutuphane() -> dict:
    return json.loads(YOL.read_text(encoding="utf-8"))


def _metin(x) -> str:
    return re.sub(r"\s+", " ", str(x or "")).strip()


def hucreler(k: dict) -> list[str]:
    """Panelin öğrenciye görünen bütün metin parçaları (ileri sızıntı ve anlam denetimi için)."""
    out = [k.get("baslik"), k.get("sonuc"), k.get("soru"), k.get("gorunen"), k.get("deger"), k.get("birim"), k.get("aciklama")]
    for x in (k.get("ogeler") or []) + (k.get("kaynaklar") or []) + (k.get("altta") or []) + (k.get("kutuplar") or []):
        out.append(x)
    for r in (k.get("satirlar") or []) + (k.get("dallar") or []):
        out += list(r) if isinstance(r, (list, tuple)) else [r]
    return [_metin(x) for x in out if _metin(x)]


def coz(k: dict, kut: dict | None = None) -> tuple[dict, str | None]:
    """Şablonlu paneli doğrular ve düzen/başlık/bağ bilgisini komuta ekler. → (komut, ret nedeni ya da None)."""
    kut = kut or kutuphane()
    sid = str(k.get("sablon") or "")
    s = (kut.get("sablonlar") or {}).get(sid)
    if not s:
        return k, f"şablon '{sid}' kütüphanede yok"
    d = s["duzen"]
    k = {**k, "duzen": d, "sablon_ad": s.get("ad", sid)}
    if s.get("basliklar") and not k.get("basliklar"):
        k["basliklar"] = s["basliklar"]
    if s.get("bag") and not k.get("bag"):
        k["bag"] = s["bag"]
    if d == "tablo":
        sat = k.get("satirlar") or []
        n = len(k.get("basliklar") or [])
        if not 1 <= len(sat) <= 7 or any(not isinstance(r, list) or len(r) != n or not all(_metin(c) for c in r) for r in sat):
            return k, f"tablo: 1–7 satır, her satır {n} dolu hücre"
    elif d == "karsit":
        kp, sat = k.get("kutuplar") or [], k.get("satirlar") or []
        if len(kp) != 2 or not 1 <= len(sat) <= 6 or any(not isinstance(r, list) or len(r) != 3 for r in sat):
            return k, "karşıt: 2 kutup, 1–6 satır [özellik, A, B]"
    elif d in ("zincir", "adimlar"):
        og = k.get("ogeler") or []
        if not 2 <= len(og) <= 7:
            return k, f"{d}: 2–7 öğe"
    elif d == "liste":
        if not _metin(k.get("baslik")) or not 2 <= len(k.get("ogeler") or []) <= 8:
            return k, "liste: başlık + 2–8 öğe"
    elif d == "grup":
        if not 2 <= len(k.get("kaynaklar") or []) <= 6 or not _metin(k.get("sonuc")):
            return k, "grup: 2–6 kaynak + sonuc"
    elif d == "dal":
        dl = k.get("dallar") or []
        if not _metin(k.get("soru")) or not 2 <= len(dl) <= 4 or any(not isinstance(x, list) or len(x) != 2 for x in dl):
            return k, "dal: soru + 2–4 dal [koşul, sonuç]"
    elif d == "maske":
        if not _metin(k.get("gorunen")) or not 1 <= len(k.get("altta") or []) <= 4:
            return k, "maske: görünen + 1–4 altta"
    elif d == "deger":
        dg, cm = _metin(k.get("deger")), k.get("cikmis")
        if not dg or len(dg) > 12 or not re.search(r"\d", dg) or not _metin(k.get("aciklama")) or len(_metin(k.get("birim"))) > 12:
            return k, "değer: sayı içeren deger (≤12 karakter) + aciklama (+ birim ≤12)"
        if cm is not None and (not isinstance(cm, int) or isinstance(cm, bool) or cm < 0):
            return k, "değer: cikmis tam sayı (doğrulanmış eşleme sayısı)"
    else:
        return k, f"düzen '{d}' tanımsız"
    if any(len(c) > 60 for c in hucreler(k)):
        return k, "hücre 60 karakterden uzun"
    return k, None


def yeni_ekle(tanim: dict, kaynak: str) -> str | None:
    """Modelin önerdiği yeni şablonu doğrulayıp kütüphaneye ekler. → eklenen kimlik ya da None."""
    kut = kutuphane()
    sid = str(tanim.get("id") or "")
    if not re.fullmatch(r"[a-z][a-z0-9_]{2,40}", sid) or sid in kut["sablonlar"]:
        return sid if sid in kut["sablonlar"] else None
    if tanim.get("duzen") not in kut["duzenler"] or not _metin(tanim.get("ad")) or not _metin(tanim.get("ne_zaman")):
        return None
    if tanim["duzen"] == "tablo" and not (isinstance(tanim.get("basliklar"), list) and 2 <= len(tanim["basliklar"]) <= 3):
        return None
    kut["sablonlar"][sid] = {x: tanim[x] for x in ("ad", "duzen", "basliklar", "ne_zaman", "bag", "ornek") if tanim.get(x)}
    kut["sablonlar"][sid]["eklenme"] = {"kaynak": kaynak, "zaman": time.strftime("%Y-%m-%d")}
    YOL.write_text(json.dumps(kut, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return sid


def okunus(k: dict) -> str:
    """Panelin öğrencinin okuyacağı biçimde düz metni (anlam denetçisi için)."""
    d = k.get("duzen")
    b = k.get("basliklar") or []
    if d == "tablo":
        return " ; ".join(" | ".join(f"{b[i] if i < len(b) else ''}: {c}" for i, c in enumerate(r)) for r in k.get("satirlar") or [])
    if d == "karsit":
        a, bb = (k.get("kutuplar") or ["", ""])[:2]
        return " ; ".join(f"{r[0]}: {a} → {r[1]}, {bb} → {r[2]}" for r in k.get("satirlar") or [])
    if d in ("zincir", "adimlar"):
        return f" → ({k.get('bag') or ''}) → ".join(k.get("ogeler") or []) if d == "zincir" else " ; ".join(
            f"{i + 1}. {x}" for i, x in enumerate(k.get("ogeler") or []))
    if d == "liste":
        return f"{k.get('baslik')}: " + ", ".join(k.get("ogeler") or [])
    if d == "grup":
        return ", ".join(k.get("kaynaklar") or []) + f" → ({k.get('bag') or ''}) → {k.get('hedef')}"
    if d == "dal":
        return f"{k.get('soru')} " + " ; ".join(f"{x[0]} → {x[1]}" for x in k.get("dallar") or [])
    if d == "maske":
        return f"görünen: {k.get('gorunen')} ; altta aranacak: " + ", ".join(k.get("altta") or [])
    if d == "deger":
        return f"{k.get('aciklama')}: {k.get('deger')} {k.get('birim') or ''}".strip()
    return json.dumps({x: k.get(x) for x in ("dugum", "kenar")}, ensure_ascii=False)


def boyu(k: dict, g: float, oran: float, em: float, yon: str = "yatay", olcek: float = 1.0) -> float:
    """Şablonlu panelin yüksekliği (sayfa yüksekliği oranı); istemci düzeninin em kopyası, %25 pay."""
    W = g / (em * olcek)
    gw = lambda t: len(_metin(t)) * 0.58 + 1.4
    satir = lambda t, sutun: max(1, -(-gw(t) // max(3.0, sutun)))
    d = k.get("duzen")
    toplam = 1.6 + (1.4 if k.get("sablon_ad") else 0)          # iç boşluk + şablon başlığı
    if d == "tablo" or d == "karsit":
        sat = k.get("satirlar") or []
        n = len(sat[0]) if sat else 2
        sutun = (W - 1.0) / n
        toplam += 1.5                                         # başlık satırı
        for r in sat:
            toplam += max(satir(c, sutun) for c in r) * 1.3 + 0.55
    elif d == "zincir":
        og = k.get("ogeler") or []
        bag_w = max(3.0, len(_metin(k.get("bag"))) * 0.46 + 1.2)
        if yon != "dikey" and sum(gw(x) for x in og) + bag_w * (len(og) - 1) > W:
            return 9.0            # yatay zincir tek satıra sığmıyor: kutular içinde kırılıyordu (H51) → dikey sürüm
        if yon == "dikey":
            toplam += sum(satir(x, W) * 1.3 + 0.55 for x in og) + (len(og) - 1) * (1.4 + (1.1 if k.get("bag") else 0))
        else:
            toplam += 1.85 + (1.2 if k.get("bag") else 0)
    elif d in ("adimlar", "liste"):
        og = k.get("ogeler") or []
        toplam += (1.6 if d == "liste" else 0) + sum(satir(x, W - 2.0) * 1.3 + 0.5 for x in og)
    elif d == "grup":
        kn = k.get("kaynaklar") or []
        sutun = W * 0.5
        toplam += max(sum(satir(x, sutun) * 1.3 + 0.55 for x in kn), satir(k.get("sonuc"), W * 0.4) * 1.3 + 0.55)
    elif d == "dal":
        dl = k.get("dallar") or []
        toplam += satir(k.get("soru"), W) * 1.3 + 0.8 + sum(satir(x[1], W * 0.6) * 1.3 + 0.6 for x in dl)
    elif d == "maske":
        toplam += 2 * 1.85 + 1.3 + 0.7 + max(0, sum(gw(x) + 0.3 for x in k.get("altta") or []) - (W - 9)) / max(4.0, W - 9) * 1.85
    elif d == "deger":
        toplam += 2.4 + satir(k.get("aciklama"), W) * 1.3 + (1.4 if k.get("cikmis") else 0)
    return toplam * em * olcek * oran * 1.32
