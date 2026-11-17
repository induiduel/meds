#!/usr/bin/env python3
"""Onarım paketi — kapıdan kalan YALNIZ hatalı parçaları, kapı mesajları ve kaynak sayfalarıyla TEK dosyada toplar (LLM yok).

Neden (kullanıcı kararı 2026-11-17, TAM_HAT_HIZLI_AKIS §0 "yeniden yazım yalnız hatalı parça"): kural vardı ama bunu
hazırlayan araç yoktu; onarım turunda alt ajan bütün soru dosyasını (≈160 KB), standart belgeyi ve slaytları yeniden
okuyordu. Bu betik kapıyı koşar, hata satırlarındaki kimliklerden (…-q63.A gibi) yalnız ilgili soruları ve şıkları çıkarır,
o soruların atıf yaptığı PDF sayfalarının metnini ve aşamanın kısa kural özetini ekler. Alt ajan yalnız bu dosyayı okur,
yalnız listelenen alanları yeniden yazar; kapı tekrar koşulur.

  python3 scripts/hat/tam_hat/onarim_paketi.py ornek_soru <soru dosyası> --uslup <soru_uslubu.json> --ders <k2-xx> --sayfalar <sayfalar.json>
      → meds_temp/onarim/<dosya adı>.md  (+ düz kimlik listesi .json) · çıkış 0 = kapı zaten temiz, 1 = paket yazıldı
  --en-cok N   pakete en çok N soru (varsayılan 25; büyük onarım parti parti yapılır)
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

_d = Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
sys.path.append(str(_d))
import kok as _kok  # noqa: E402

KOK = _kok.MEDS
CIKTI = KOK.parent / "meds_temp" / "onarim"
ID = re.compile(r"(k\d-\d{2}[\w-]*?-q\d+)(?:\.([A-E]))?")


def sorular(dosya: Path) -> dict[str, dict]:
    d = json.loads(dosya.read_text(encoding="utf-8"))
    out = {}
    for k in d.get("kazanimlar", []):
        for q in k.get("sorular", []):
            out[q["id"]] = {**q, "_kazanim": k.get("metin", "")}
    return out


def sayfa_no(q: dict) -> list[int]:
    """Sorunun atıf yaptığı PDF sayfaları: açıklama ve şık açıklamalarındaki "(s. 2 ve 5)" biçimleri."""
    metin = json.dumps(q, ensure_ascii=False)
    s = set()
    for m in re.finditer(r"s\.\s*(\d+(?:\s*(?:ve|,|-|–)\s*\d+)*)", metin):
        s.update(int(x) for x in re.findall(r"\d+", m.group(1)))
    return sorted(x for x in s if x < 400)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("asama", choices=["ornek_soru"])
    ap.add_argument("dosya", type=Path)
    ap.add_argument("--uslup", required=True)
    ap.add_argument("--ders", required=True)
    ap.add_argument("--sayfalar", required=True, type=Path)
    ap.add_argument("--en-cok", type=int, default=25)
    a = ap.parse_args()

    p = subprocess.run([sys.executable, "scripts/kapilar/kos.py", "ornek_soru", f"dosya={a.dosya}", f"uslup={a.uslup}",
                        f"ders={a.ders}", f"sayfalar={a.sayfalar}"], cwd=KOK, capture_output=True, text=True, errors="replace")
    satir = [x.strip() for x in (p.stdout + p.stderr).splitlines() if x.strip()]
    if p.returncode == 0:
        print("kapı temiz (0 HATA) — onarım gerekmez")
        return 0
    Q = sorular(a.dosya if a.dosya.is_absolute() else KOK / a.dosya)
    hata: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)  # soru → [(şık|'', mesaj)]
    genel = []
    for x in satir:
        m = ID.search(x)
        if m and m.group(1) in Q:
            hata[m.group(1)].append((m.group(2) or "", x[m.end():].lstrip(" :").strip()))
        elif re.search(r"\bHATA\b", x) and not re.search(r"(?<!\d)\d+ HATA", x):
            genel.append(x)
    say = sorted(hata, key=lambda q: -len(hata[q]))
    sec = say[: a.en_cok]
    sp = json.loads(a.sayfalar.read_text(encoding="utf-8")) if a.sayfalar.exists() else {}
    sp = sp if isinstance(sp, dict) else {str(i + 1): (x.get("metin") if isinstance(x, dict) else str(x)) for i, x in enumerate(sp)}
    # Yalnız hata veren kapının kuralı (genel aşama özeti ilgisiz maddeler getiriyordu)
    KURAL = {
        "sik_aciklama": "Şık açıklaması (AGENTS 14, SIK_ACIKLAMA_STANDARDI): her şıkta 2–3 cümle — (1) şıktaki kavram NEDİR, (2) ne işe yarar / "
                        "nerede görülür, (3) bu soruda NEDEN doğru ya da yanlış. 'soruda aranan yanıt', 'listesinde yer almaz', 'bu şık yanlıştır' "
                        "gibi geçiştirme ve aynı cümleyi şıklar arasında tekrarlamak YASAK. Yalnız verilen kaynak sayfalarındaki bilgi; sonunda (s. N).",
        "turkce_uslup": "Türkçe üslup (TURKCE_USLUP_STANDARDI): çeviri mecaz, iç yazım etiketi, kalıp giriş yok; doğal, kısa cümle.",
        "profil": "Hoca profili: set/kök kalıbı oranları profil aralığında olmalı; mesajdaki '→ ±N soru' kadar soru o türe çevrilir (yeni soru yazmak yerine kök biçimi değişir).",
    }
    etiket = {m.group(1) for x in satir if (m := re.match(r"\[(\w+)\]", x))}
    ozet = "\n".join(f"- **{e}:** {KURAL[e]}" for e in sorted(etiket) if e in KURAL) or "- Kapı mesajındaki yönergeyi uygula."

    # en sık kapı mesajı kalıpları (alt ajan önce ortak nedeni görsün)
    kalip = collections.Counter(re.sub(r"'[^']*'", "'…'", m) for q in hata for _, m in hata[q])
    L = [f"# Onarım paketi · {a.dosya.name}", "",
         f"Kapı: {sum(len(v) for v in hata.values())} hatalı alan, {len(hata)} soru. Bu pakette {len(sec)} soru"
         + (f" (kalan {len(say) - len(sec)} soru sonraki parti)" if len(say) > len(sec) else "") + ".", "",
         "**Görev:** yalnız aşağıda ✗ ile işaretli alanları yeniden yaz; diğer alanlara, soru köküne ve doğru cevaba DOKUNMA.",
         "Her yeni metin yalnız verilen kaynak sayfalarına dayanır; kapıyı geçmek için dolgu/kalıp cümle YASAK (H555).", "",
         "## En sık kapı mesajları", ""] + [f"- {n}× {k}" for k, n in kalip.most_common(6)] + [""]
    if genel:
        L += ["## Dosya geneli kapı mesajları (soruya bağlı değil)", ""] + [f"- {g}" for g in genel[:15]] + [""]
    L += ["## Kural (yalnız hata veren kapılar)", "", ozet, ""]
    sayfalar_gerekli: set[int] = set()
    for qid in sec:
        q = Q[qid]
        L += [f"## {qid}  ·  kazanım: {q['_kazanim']}", "", f"**Kök:** {q.get('soru', '')}", ""]
        siklar = {s for s, _ in hata[qid] if s}
        for h, met in (q.get("secenekler") or {}).items():
            isaret = "✗" if h in siklar else " "
            L.append(f"- {isaret} **{h}{' (doğru)' if h == q.get('dogru') else ''}** {met}")
            if h in siklar:
                L.append(f"    - şık açıklaması (yeniden yaz): {q.get('sik_aciklamalari', {}).get(h, '')}")
        L.append("")
        L += ["**Kapı mesajları:**"] + [f"- {('şık ' + s + ': ') if s else ''}{m}" for s, m in hata[qid]] + [""]
        sn = sayfa_no(q)
        sayfalar_gerekli.update(sn)
        L += [f"**Kaynak sayfalar:** {', '.join(map(str, sn)) or '—'}", ""]
    L += ["## Kaynak sayfa metinleri (yalnız yukarıdaki sorularınkiler)", ""]
    for n in sorted(sayfalar_gerekli):
        t = sp.get(str(n)) or ""
        L += [f"### s.{n}", "", (t if isinstance(t, str) else json.dumps(t, ensure_ascii=False))[:2500].strip(), ""]
    CIKTI.mkdir(parents=True, exist_ok=True)
    md = CIKTI / f"{a.dosya.stem}.md"
    md.write_text("\n".join(L), encoding="utf-8")
    (CIKTI / f"{a.dosya.stem}.json").write_text(json.dumps({q: [s for s, _ in hata[q]] for q in sec}, ensure_ascii=False, indent=1), encoding="utf-8")
    kelime = len(md.read_text(encoding="utf-8").split())
    tam = len(a.dosya.read_text(encoding="utf-8").split()) if a.dosya.exists() else 0
    print(f"onarım paketi: {md}  ({len(sec)} soru, {kelime} kelime; bütün soru dosyası {tam} kelime)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
