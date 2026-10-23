"""Görev modüllerinin ortak veri bulucuları ve soru kapısı (betik; model yok)."""
from __future__ import annotations

import re
from pathlib import Path

from .. import cekirdek as c

HARFLER = "ABCDE"
SESLI_V2 = c.KOK / "data" / "sesli_anlatim" / "v2"


# ── veri bulucular ────────────────────────────────────────────────────────────────────────────────────────────────
def konusma_bul(ders_id: str) -> tuple[Path, dict]:
    """Sesli ders metni v2 (cümle kimlikli). Kurul 1 geri doldurması ve Kurul 2+ yayını aynı klasörde."""
    for p in sorted(SESLI_V2.glob(f"{ders_id}*.json")):
        d = c.oku(p, {})
        if d.get("ders_id") == ders_id:
            return p, d
    raise SystemExit(f"sesli ders v2 metni yok: {ders_id} ({SESLI_V2})")


def kaynak_sayfalar(ders_id: str) -> dict[int, str]:
    """Ders bilgi deposundaki kaynak.md (=== SAYFA n ===) → {sayfa: metin}. Depo yoksa boş (çağıran karar verir)."""
    man = c.oku(c.DB2 / "ders_bilgi" / ders_id / "manifest.json", {}) or {}
    yol = (man.get("yollar") or {}).get("kaynak_md")
    if not yol or not Path(yol).exists():
        return {}
    out: dict[int, str] = {}
    for parca in Path(yol).read_text(encoding="utf-8").split("=== SAYFA ")[1:]:
        bas, _, govde = parca.partition("===")
        if bas.strip().isdigit():
            out[int(bas.strip())] = govde
    return out


def sade(metin: str, sinir: int = 0) -> str:
    """Slayt metnini tek satıra indirir (madde işaretleri ve boş satırlar atılır)."""
    s = re.sub(r"[•▪●◦–\-]\s*\n", " ", metin or "")
    s = " ".join(s.split())
    return s[:sinir] if sinir else s


# ── soru kapısı ───────────────────────────────────────────────────────────────────────────────────────────────────
ON_EK = re.compile(r"^\s*(Doğru|Yanlış)\.\s*")
HARF_ANMA = re.compile(r"\b[A-E]\s*şıkk|\bşık\s*[A-E]\b|\([A-E]\)")


def sik_aciklamasi_denetle(harf: str, metin: str, dogru: str, yer: str) -> list[str]:
    from sik_aciklama import denetle as sik_denetle
    from turkce_uslup import denetle as uslup
    e = []
    m = ON_EK.match(metin or "")
    beklenen = "Doğru" if harf == dogru else "Yanlış"
    if not m:
        e.append(f"{yer}: açıklama '{beklenen}.' ile başlamalı")
    elif m.group(1) != beklenen:
        e.append(f"{yer}: açıklama '{m.group(1)}.' diyor ama bu şık {beklenen.lower()}")
    govde = ON_EK.sub("", metin or "")
    govde = re.sub(r"\s*\(s\.\s*\d+(?:[–-]\d+)?\)\s*\.?\s*$", "", govde).strip()
    e += sik_denetle(govde, yer, enaz=20, encok=65, cumle=(2, 4))
    e += uslup(metin or "", yer)
    if HARF_ANMA.search(govde):
        e.append(f"{yer}: harf anılmış ({HARF_ANMA.search(govde).group()!r}) — şıkkı kavram adıyla an")
    return e


def soru_denetle(q: dict, yer: str, dayanak: str | None = None) -> list[str]:
    """q: {kok, secenekler{A..E}, dogru, aciklama?, sik_aciklamalari{A..E}}. dayanak: doğru cevabı taşıması gereken metin."""
    from turkce_uslup import denetle as uslup
    e: list[str] = []
    kok = (q.get("kok") or "").strip()
    sec = q.get("secenekler") or {}
    dogru = q.get("dogru")
    if len(kok.split()) < 6:
        e.append(f"{yer}: soru kökü çok kısa")
    if sorted(sec) != list(HARFLER):
        e.append(f"{yer}: şıklar tam olarak A–E olmalı (var: {''.join(sorted(sec))})")
    if dogru not in HARFLER:
        e.append(f"{yer}: doğru cevap A–E harfi olmalı ({dogru!r})")
    metinler = [(h, (sec.get(h) or "").strip()) for h in HARFLER]
    if any(not t for _, t in metinler):
        e.append(f"{yer}: boş şık var")
    katli = [c.katla(t) for _, t in metinler if t]
    if len(set(katli)) != len(katli):
        e.append(f"{yer}: aynı metinli şıklar var")
    e += uslup(kok, f"{yer}.kok")
    for h, t in metinler:
        e += uslup(t, f"{yer}.{h}")
    if q.get("aciklama") is not None:
        if c.kelime_say(q["aciklama"]) < 12:
            e.append(f"{yer}: genel açıklama çok kısa (≥12 kelime, gerekçeli)")
        e += uslup(q["aciklama"], f"{yer}.aciklama")
    sa = q.get("sik_aciklamalari") or {}
    for h in HARFLER:
        e += sik_aciklamasi_denetle(h, sa.get(h, ""), dogru, f"{yer}.{h}.aciklama")
    if dogru in sec and all(t for _, t in metinler):
        # uzunluk ipucu: doğru şık ötekilerden belirgin uzunsa öğrenci bilgiye değil uzunluğa bakarak bulur
        uz = {h: c.kelime_say(t) for h, t in metinler}
        diger = sorted(v for h, v in uz.items() if h != dogru)
        if uz[dogru] >= 6 and uz[dogru] > 1.6 * diger[len(diger) // 2] and uz[dogru] > max(diger):
            e.append(f"{yer}: doğru şık ötekilerden belirgin uzun ({uz[dogru]} kelime, ortanca {diger[len(diger) // 2]}) — uzunluk ipucu")
    if dogru in sec:
        dk = c.kokler(sec[dogru])
        # kök sızıntısı: doğru şıkkın içerik kökleri kökte geçiyorsa (≥2 kök) cevap ele veriliyor
        if len(dk) >= 2 and dk <= c.kokler(kok):
            e.append(f"{yer}: soru kökü doğru şıkkın kelimelerini içeriyor (cevabı ele veriyor)")
        # sözcüksel dayanak (ICERIK_MOTORU_V3 §16.2): doğru şıkkın bilgisi dayanak metinde geçmeli
        if dayanak is not None:
            dm = c.kokler(dayanak, en_az=3) | c.sayilar(dayanak)
            hedef = c.kokler(sec[dogru], en_az=3) | c.sayilar(sec[dogru])
            if hedef and not (hedef & dm):
                e.append(f"{yer}: doğru şık ({sec[dogru][:60]!r}) kanıt cümlelerinde hiç geçmiyor — kanıtı ya da şıkkı düzelt")
            elif len(hedef) >= 3 and len(hedef & dm) / len(hedef) < 0.34:
                e.append(f"{yer}: doğru şıkkın kanıt cümleleriyle örtüşmesi zayıf ({len(hedef & dm)}/{len(hedef)})")
    return e
