#!/usr/bin/env python3
"""Yayımlanmış sesli derste metin düzeltmesinden sonra PDF katmanlarını onarır (H448; LLM yok).

Sıra: (1) metin/<key>.md + v2/<key>.json birlikte düzeltilir → (2) `klip_tasi.py <key>` (eski metin git HEAD) → (3) `sesli_yayinla.py`
(ders-ekle: metin + EMA işi; Oracle çapayı v2 satırlarından KABA yazar) → (4) BU BETİK → (5) EMA bitince Oracle `meds-cumle-zaman`
ve yerel `meds-kelime-zaman-hat`.

  .venv-ocr/bin/python scripts/sesli_anlatim/duzeltme_katman.py <key> [--kuru]

Yaptıkları (yalnız değişen paragraflar; değişmeyenler klip_tasi ile taşınmış hâliyle kalır):
  capa          Oracle'ın satır çapası alınır; cümle metni değişmemişse git HEAD'deki (elle yazılmış madde/resim/kutu/yol) çapa
                geri gelir, yeni cümlenin satırları `pdf_isaret.capa_maddeleri` ile madde dizinine çevrilir; mdSha1 yeni metin.
  cizim         eski cümle aynen kaldıysa çizimi yeni cümle sırasına taşınır (cümle sırası kaydığında çizim kaybolmasın).
  cikmis_konum  değişen paragraftan düşen eşleme, cümlesi aynen kaldıysa yeni sıraya yerleşir.
  hizalama      Oracle'dan alınır (ders-ekle v2 sayfalarından yazar; klip_tasi yeni paragrafa önceki sayfayı verir).
Sonra capa/cizim/cikmis_konum Oracle'a yazılır ve Oracle'da `pdf_isaret.py --key <key> --zorla` çalışır (H93).
Dosyaların kendi JSON biçimi korunur (git farkı yalnız içerik).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from klip_tasi import KOK, paragraflar  # noqa: E402
from pdf_isaret import INDIR, Pdf, capa_maddeleri, cumle_sonlari  # noqa: E402

ORACLE = "medsor-oracle"
ORACLE_KOK = "/home/ubuntu/medsor/meds/data/sesli_anlatim"
MEDS = Path(__file__).resolve().parents[2]


def git_head(rel: str) -> str:
    return subprocess.run(["git", "-C", str(MEDS), "show", f"HEAD:{rel}"], capture_output=True, text=True).stdout


def bol(t: str) -> list[str]:
    out, b = [], 0
    for s in cumle_sonlari(t):
        out.append(t[b:s].strip()); b = s
    return out


def bicim(eski: str):
    """Dosyanın JSON biçimini (sıkıştırılmış / indent) bulur; yazarken aynısı kullanılır."""
    try:
        d = json.loads(eski)
    except ValueError:
        return None, None, True
    for ind, sep in ((None, (",", ":")), (1, None), (2, None), (None, None)):
        if json.dumps(d, ensure_ascii=False, indent=ind, separators=sep).strip() == eski.strip():
            return ind, sep, eski.endswith("\n")
    return 1, None, True


def yaz(p: Path, veri, ornek: str) -> None:
    ind, sep, nl = bicim(ornek)
    p.write_text(json.dumps(veri, ensure_ascii=False, indent=ind, separators=sep) + ("\n" if nl else ""))


def oracle_oku(rel: str) -> dict:
    return json.loads(subprocess.run(["ssh", ORACLE, f"cat {ORACLE_KOK}/{rel}"], capture_output=True, text=True, check=True).stdout)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("key"); ap.add_argument("--kuru", action="store_true")
    a = ap.parse_args()
    k = a.key
    E = paragraflar(git_head(f"data/sesli_anlatim/metin/{k}.md"))
    Y = paragraflar((KOK / "metin" / f"{k}.md").read_text())
    if len(E) != len(Y):
        sys.exit("paragraf sayısı değişti: bu betik yalnız paragraf içi düzeltmede kullanılır (yeni paragrafta çapa/çizim oturumda yazılır)")
    deg = [i for i, (e, y) in enumerate(zip(E, Y)) if e["t"] != y["t"]]
    print(f"{k}: değişen paragraflar {deg}")
    # hizalama
    hz_o = oracle_oku(f"hizalama/{k}.json")
    hz_p = KOK / "hizalama" / f"{k}.json"
    # capa
    cp = KOK / "capa" / f"{k}.json"
    cap_ham = cp.read_text()
    cap = json.loads(cap_ham)
    cap_o = oracle_oku(f"capa/{k}.json")
    cap_e = json.loads(git_head(f"data/sesli_anlatim/capa/{k}.json") or "{}")
    pdf = Pdf(INDIR / hz_o["dosyalar"][0]["path"])
    an = lambda t: re.sub(r"\W+", "", t.lower())[:40]  # noqa: E731
    for i in deg:
        eski = {an(c["ses"]): c for c in (cap_e.get("p") or [[]] * len(E))[i]}
        yeni = []
        for c in cap_o["p"][i]:
            o = eski.get(an(c["ses"]))
            if o:
                yeni.append(dict(o)); continue
            e = {"ses": c["ses"][:60], "dosya": c.get("dosya", 0), "sayfa": c["sayfa"]}
            ms = sorted(capa_maddeleri(pdf.sayfa(c["sayfa"]), c.get("satir") or [])) if c.get("satir") else []
            if ms:
                e["madde"] = ms
            if c.get("sekil"):
                e["sekil"] = c["sekil"]
            yeni.append(e)
        cap["p"][i] = yeni
    cap["mdSha1"] = cap_o["mdSha1"]
    # cizim
    zp = KOK / "cizim" / f"{k}.json"
    cz_ham = zp.read_text() if zp.exists() else ""
    cz = json.loads(cz_ham) if cz_ham else None
    cz_e = json.loads(git_head(f"data/sesli_anlatim/cizim/{k}.json") or "null")
    if cz and cz_e:
        for i in deg:
            if str(i) not in cz_e["p"]:
                continue
            ec, yc = bol(E[i]["t"]), bol(Y[i]["t"])
            tasinan = {}
            for ci, v in cz_e["p"][str(i)].items():
                s = ec[int(ci)] if int(ci) < len(ec) else ""
                if s in yc:
                    tasinan[str(yc.index(s))] = v
                else:
                    print(f"  çizim p{i} c{ci} TAŞINAMADI (cümle değişti, oturumda yeniden yazılmalı): {s[:70]}")
            if tasinan:
                cz["p"][str(i)] = tasinan
    # cikmis_konum
    kp = KOK / "cikmis_konum" / f"{k}.json"
    ck_ham = kp.read_text() if kp.exists() else ""
    ck = json.loads(ck_ham) if ck_ham else None
    ck_e = json.loads(git_head(f"data/sesli_anlatim/cikmis_konum/{k}.json") or "null")
    if ck and ck_e:
        var = {q["id"] for q in ck["q"]}
        for q in ck_e["q"]:
            if q["id"] in var or q["p"] not in deg:
                continue
            s = bol(E[q["p"]]["t"])[q["c"]]
            yc = bol(Y[q["p"]]["t"])
            if s in yc:
                ck["q"].append(dict(q, c=yc.index(s))); print(f"  çıkmış {q['id']} → p{q['p']} c{yc.index(s)}")
            else:
                print(f"  çıkmış {q['id']} YERLEŞMEDİ (cümle değişti): {s[:70]}")
    if a.kuru:
        print("kuru: yazılmadı"); return 0
    yaz(hz_p, hz_o, hz_p.read_text() if hz_p.exists() else "")
    yaz(cp, cap, cap_ham)
    if cz:
        yaz(zp, cz, cz_ham)
    if ck:
        yaz(kp, ck, ck_ham)
    for alt, p in (("capa", cp), ("cizim", zp), ("cikmis_konum", kp)):
        if p.exists():
            subprocess.run(["scp", "-q", str(p), f"{ORACLE}:/tmp/{alt}_{k}.json"], check=True)
            subprocess.run(["ssh", ORACLE, f"sudo cp /tmp/{alt}_{k}.json {ORACLE_KOK}/{alt}/{k}.json && sudo chown ubuntu:ubuntu {ORACLE_KOK}/{alt}/{k}.json"], check=True)
    r = subprocess.run(["ssh", ORACLE, "cd /home/ubuntu/medsor/meds && sudo -u ubuntu env CUDA_VISIBLE_DEVICES= MEDS_API=http://127.0.0.1:3000 "
                        f"/home/ubuntu/medsor/venv-cumle/bin/python scripts/sesli_anlatim/pdf_isaret.py --key {k} --zorla 2>&1 | grep -v pymupdf_layout | tail -2"],
                       capture_output=True, text=True)
    print(r.stdout.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
