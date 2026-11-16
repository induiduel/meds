#!/usr/bin/env python3
"""Hoca dökümü kırpma (C6, 2026-11-16) — değerlendirme aşaması HAM `hoca_dokum.json`'ı (k2-28: 360 KB, JSON + kelime zaman
damgalarıyla ≈35,8k kelime) okumasın; slayt başına kırpılmış özet okusun. DETERMİNİSTİK: LLM yok.

  python3 scripts/hat/tam_hat/hoca_kirp.py <ders klasörü>              # → <klasör>/hoca_dokum_kirpik.json + .md
  python3 scripts/hat/tam_hat/hoca_kirp.py <ders klasörü> --ham 14     # 14. slaytın HAM döküm cümleleri (gerekirse)
  python3 scripts/hat/tam_hat/hoca_kirp.py <ders klasörü> --ornek 10   # tutulan/atılan örnek cümleler (inceleme)

Yöntem:
  1. Whisper segmentleri noktalamayla cümleye birleştirilir (metin AYNEN; yalnız boşlukla birleşir).
  2. Cümle → slayt: `ses_hizasi.json` (slayt t_bas/t_son) varsa ondan; yoksa cümle↔slayt belirteç örtüşmesiyle MONOTON
     hizalama (dinamik programlama, slayt sırası geri gitmez). Hangisinin kullanıldığı çıktıda `hizalama` alanında yazılı.
  3. Sınıflama (öncelik sırasıyla): vurgu kalıbı → TUT (asla atılmaz) · Whisper sanrısı/kısa dolgu (<4 kök)/yoklama/teknik aksaklık (<8 kök) → AT ·
     örnek/klinik anekdot → TUT · tekrar eden cümle (başka yerde benzeri var) → ilki TUT, kopyası AT · slaytta olmayan
     bilgi (slaytta olmayan kök ≥4 ve oran ≥%50; 4-harf önek toleranslı, ya da slaytta olmayan sayı) → TUT · kalan (slaytı okuyan) → AT.
  4. Güvenlik: tutulan her cümle ham metnin alt dizgisidir (uydurma yok, betik doğrular); vurgu kalıplı cümle atılmışsa
     çıkış 1. Kırpma oranı ve atılan cümle sayısı basılır.
"""
from __future__ import annotations
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402,F401

import argparse
import json
import re
import sys
from pathlib import Path

# Vurgu/sınav işareti — bu kalıbı içeren cümle HİÇBİR koşulda atılmaz (sınama: denetle()).
VURGU = re.compile(r"önemli|önem\w*|sınav|çıkar|çıkıyor|çıkmış|çıkabilir|sorarım|soru(?:lar|yu)?\b|dikkat|bilin|bilmeniz|"
                   r"unutma|mutlaka|özellikle|altını çiz|ezber|aklınız|akılda|kesinlikle|sakın", re.I)
ORNEK = re.compile(r"örneğin|örnek|mesela|misal|hastam|hastamız|bir hasta|vaka|klinikte|kliniğimiz|poliklinik|servis|"
                   r"gördüğümüz|görürsünüz|karşılaş|yaşadı|başvur", re.I)
SANRI = re.compile(r"izlediğiniz için|abone ol|altyazı|teşekkürler\.?$|teşekkür ederim\.?$", re.I)
DOLGU = re.compile(r"yoklama|ses geliyor|duyuyor mu|duyabiliyor|görüyor mu|görebiliyor|mikrofon|bilgisayar|projeksiyon|"
                   r"ara verelim|teneffüs|kapıyı|sessiz olalım|bir saniye|slaytı (?:açayım|geçeyim)|açılmadı|donmuş", re.I)
DOLGU_SOZ = {"evet", "şimdi", "tamam", "peki", "arkadaşlar", "hocam", "yani", "işte", "bu", "şu", "bir", "de", "da", "ve",
             "ama", "hani", "şey", "böyle", "şöyle", "o", "zaman", "hadi", "bakalım", "evet,", "değil", "mi", "var", "çok",
             "gibi", "olarak", "için", "ile", "daha", "sonra", "burada", "bunu", "bunlar", "bunun", "onu", "olan"}


def _kucuk(s: str) -> str:
    return s.replace("İ", "i").replace("I", "ı").lower()


def kokler(s: str) -> list[str]:
    """Kaba Türkçe kök: küçük harf, ≥4 harfli sözcüğün ilk 5 harfi (Whisper yazım bozukluğuna toleranslı)."""
    return [w[:5] for w in re.findall(r"[a-zçğıöşüâîû]+", _kucuk(s)) if len(w) >= 4 and w not in DOLGU_SOZ]


def sayilar(s: str) -> set[str]:
    return set(re.findall(r"\d+(?:[.,]\d+)?", s))


def cumleler(dokum: dict) -> list[dict]:
    """Segmentleri cümleye birleştirir; metin aynen (boşlukla birleşik). t = ilk segmentin başı."""
    out, buf, t0 = [], [], None
    for sg in dokum.get("segmentler", []):
        m = (sg.get("metin") or "").strip()
        if not m:
            continue
        if t0 is None:
            t0 = sg.get("bas", 0.0)
        buf.append(m)
        if re.search(r"[.?!…]$", m):
            out.append({"t": round(t0, 1), "metin": " ".join(buf)})
            buf, t0 = [], None
    if buf:
        out.append({"t": round(t0 or 0.0, 1), "metin": " ".join(buf)})
    return out


def hizala_zaman(cs: list[dict], hiza: list[dict]) -> None:
    hz = sorted(hiza, key=lambda x: x["t_bas"])
    for c in cs:
        s = hz[0]["s"]
        for h in hz:
            if c["t"] >= h["t_bas"] - 0.5:
                s = h["s"]
        c["s"] = s


def hizala_icerik(cs: list[dict], sayf: dict) -> None:
    """Monoton DP: cümle i slayt j'ye; j geri gitmez, en çok 3 slayt atlar. Puan = cümle köklerinin slaytta bulunma oranı."""
    sl = sorted(sayf, key=int)
    sk = [set(kokler(sayf[k])) for k in sl]
    n, m = len(cs), len(sl)
    puan = []
    for c in cs:
        kc = kokler(c["metin"])
        puan.append([(sum(1 for x in kc if x in s) / len(kc)) if kc else 0.0 for s in sk])
    NEG = -1e9
    dp = [[NEG] * m for _ in range(n)]
    gel = [[0] * m for _ in range(n)]
    for j in range(m):
        dp[0][j] = puan[0][j] - 0.05 * j
    for i in range(1, n):
        for j in range(m):
            en, ej = NEG, j
            for p in range(max(0, j - 3), j + 1):
                v = dp[i - 1][p] - (0.02 * (j - p))
                if v > en:
                    en, ej = v, p
            dp[i][j] = en + puan[i][j]
            gel[i][j] = ej
    j = max(range(m), key=lambda x: dp[n - 1][x]) if n else 0
    for i in range(n - 1, -1, -1):
        cs[i]["s"] = int(sl[j])
        j = gel[i][j]


def siniflandir(cs: list[dict], sayf: dict) -> None:
    gorulen: list[tuple[set, int]] = []
    for i, c in enumerate(cs):
        m = c["metin"]
        kc = kokler(m)
        if VURGU.search(m):
            c["neden"] = "vurgu"
        elif SANRI.search(m.strip()) or (DOLGU.search(m) and len(kc) < 8) or len(kc) < 4:
            c["neden"] = "dolgu"
        else:
            st = set()
            for k in (str(c["s"] - 1), str(c["s"]), str(c["s"] + 1)):
                st |= set(kokler(sayf.get(k, "")))
            kume = set(kc)
            kopya = next((j for s, j in gorulen if len(kume & s) / max(1, len(kume | s)) >= 0.6), None)
            st4 = {x[:4] for x in st}  # Whisper yazım bozukluğu: 4 harf öneki eşleşmesi de "slaytta var" sayılır
            yeni = [x for x in kc if x not in st and x[:4] not in st4]
            say_yeni = sayilar(m) - sayilar(sayf.get(str(c["s"]), ""))
            if kopya is not None:
                c["neden"] = "kopya"
                cs[kopya]["tekrar"] = cs[kopya].get("tekrar", 1) + 1
            elif ORNEK.search(m):
                c["neden"] = "ornek"
            elif (len(yeni) >= 4 and len(yeni) / len(kc) >= 0.5) or say_yeni:
                c["neden"] = "yeni_bilgi"
            else:
                c["neden"] = "slayt_okuma"
            gorulen.append((kume, i))
        c["tut"] = c["neden"] in ("vurgu", "ornek", "yeni_bilgi")
    for c in cs:  # tekrar eden cümle (ilk geçiş) vurgu işaretidir → tut
        if c.get("tekrar", 1) > 1 and c["neden"] != "dolgu":
            c["tut"] = True
            if c["neden"] == "slayt_okuma":
                c["neden"] = "tekrar"


def denetle(cs: list[dict], ham: str) -> list[str]:
    h = []
    for c in cs:
        if not c["tut"] and VURGU.search(c["metin"]):
            h.append(f"vurgu kalıplı cümle atılmış: t{c['t']} {c['metin'][:80]}")
        if c["tut"] and c["metin"] not in ham:
            h.append(f"tutulan cümle ham metinde yok (uydurma): t{c['t']}")
    return h


def kirp(klasor: Path) -> dict:
    dk = json.loads((klasor / "hoca_dokum.json").read_text(encoding="utf-8"))
    sayf = json.loads((klasor / "sayfalar.json").read_text(encoding="utf-8"))
    cs = cumleler(dk)
    hp = klasor / "ses_hizasi.json"
    if hp.exists():
        hizala_zaman(cs, json.loads(hp.read_text(encoding="utf-8")))
        hiz = "ses_hizasi.json (slayt zaman aralığı)"
    else:
        hizala_icerik(cs, sayf)
        hiz = "otomatik (cümle↔slayt belirteç örtüşmesi, monoton DP) — ses_hizasi.json yok"
    siniflandir(cs, sayf)
    ham = " ".join((s.get("metin") or "").strip() for s in dk.get("segmentler", []))
    hatalar = denetle(cs, ham)
    ham_json_k = len((klasor / "hoca_dokum.json").read_text(encoding="utf-8").split())
    ham_k = sum(len(c["metin"].split()) for c in cs)
    tut_k = sum(len(c["metin"].split()) for c in cs if c["tut"])
    say: dict[str, int] = {}
    for c in cs:
        say[c["neden"]] = say.get(c["neden"], 0) + 1
    slaytlar: dict[str, list] = {}
    for c in cs:
        if c["tut"]:
            slaytlar.setdefault(str(c["s"]), []).append(
                {"t": c["t"], "neden": c["neden"], **({"tekrar": c["tekrar"]} if c.get("tekrar", 1) > 1 else {}), "metin": c["metin"]})
    return {"kaynak": "hoca_dokum.json", "hizalama": hiz, "yontem": "deterministik (LLM yok) — hoca_kirp.py",
            "istatistik": {"ham_json_kelime": ham_json_k, "ham_metin_kelime": ham_k, "kirpik_kelime": tut_k,
                           "kirpma_orani_metin": round(1 - tut_k / max(1, ham_k), 3),
                           "kirpma_orani_json": round(1 - tut_k / max(1, ham_json_k), 3),
                           "cumle": len(cs), "tutulan": sum(c["tut"] for c in cs), "atilan": sum(not c["tut"] for c in cs),
                           "neden": say},
            "denetim_hatasi": hatalar, "slaytlar": slaytlar, "_cumleler": cs}


def md(o: dict, klasor: Path) -> str:
    st = o["istatistik"]
    L = [f"# Hoca dökümü — kırpılmış (slayt başına; {o['yontem']})",
         f"> Hizalama: {o['hizalama']}. Ham {st['ham_metin_kelime']} kelime → {st['kirpik_kelime']} kelime "
         f"(%{round(st['kirpma_orani_metin'] * 100)} kırpıldı; atılan {st['atilan']} cümle: slaytı okuyan/dolgu/kopya).",
         f"> Tutulan: hocanın slaytta OLMAYAN bilgisi, vurgu/sınav işareti (asla atılmaz), örnek/klinik anekdot, tekrar eden cümle.",
         f"> Bir slaytın HAM dökümü gerekirse: `python3 scripts/hat/tam_hat/hoca_kirp.py {klasor} --ham <slayt>` "
         f"(ya da `hoca_dokum.json`, aşağıdaki t aralığı). Alıntı (`alinti`) yalnız dökümde geçen sözdür.", ""]
    for s in sorted(o["slaytlar"], key=int):
        xs = o["slaytlar"][s]
        L.append(f"## s{s} (t {xs[0]['t']:.0f}–{xs[-1]['t']:.0f})")
        for x in xs:
            tk = f"×{x['tekrar']}" if x.get("tekrar") else ""
            L.append(f"- t{x['t']:.0f} [{x['neden']}{tk}] {x['metin']}")
    return "\n".join(L) + "\n"


def yaz(klasor: Path) -> dict:
    o = kirp(klasor)
    cs = o.pop("_cumleler")
    (klasor / "hoca_dokum_kirpik.json").write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding="utf-8")
    (klasor / "hoca_dokum_kirpik.md").write_text(md(o, klasor), encoding="utf-8")
    o["_cumleler"] = cs
    return o


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("klasor", type=Path)
    ap.add_argument("--ham", type=int, help="bu slaytın HAM döküm cümlelerini bas (yazmaz)")
    ap.add_argument("--ornek", type=int, help="tutulan/atılan örnek cümle sayısı (yazar + basar)")
    a = ap.parse_args()
    if not (a.klasor / "hoca_dokum.json").exists():
        print(f"hoca_dokum.json yok: {a.klasor} — kırpma atlandı (ses kaydı olmayan ders)")
        return 0
    if a.ham is not None:
        o = kirp(a.klasor)
        for c in o["_cumleler"]:
            if c["s"] == a.ham:
                print(f"t{c['t']:.0f} [{c['neden']}{'' if c['tut'] else ' · atıldı'}] {c['metin']}")
        return 0
    o = yaz(a.klasor)
    st = o["istatistik"]
    print(f"hizalama: {o['hizalama']}")
    print(f"ham JSON {st['ham_json_kelime']} kelime · ham metin {st['ham_metin_kelime']} → kırpık {st['kirpik_kelime']} kelime "
          f"(metne göre %{round(st['kirpma_orani_metin'] * 100)}, JSON'a göre %{round(st['kirpma_orani_json'] * 100)} azalma)")
    print(f"cümle {st['cumle']}: tutulan {st['tutulan']} · atılan {st['atilan']} · nedenler {st['neden']}")
    if a.ornek:
        cs = o["_cumleler"]
        import random
        r = random.Random(28)
        for ad, kume in (("TUTULAN", [c for c in cs if c["tut"]]), ("ATILAN", [c for c in cs if not c["tut"]])):
            print(f"\n## {ad} (rastgele {a.ornek})")
            for c in sorted(r.sample(kume, min(a.ornek, len(kume))), key=lambda c: c["t"]):
                print(f"  s{c['s']} t{c['t']:.0f} [{c['neden']}] {c['metin'][:150]}")
    for h in o["denetim_hatasi"]:
        print("HATA", h)
    print(f"yazıldı: {a.klasor / 'hoca_dokum_kirpik.json'} + .md · denetim {len(o['denetim_hatasi'])} HATA")
    return 1 if o["denetim_hatasi"] else 0


if __name__ == "__main__":
    sys.exit(main())
