#!/usr/bin/env python3
"""Metin değişince PDF/ders katmanlarını değişmeyen paragraflara taşır (klipli ders altyapısı, 2026-10-28).

Konuşma metni (metin/<key>.md) düzeltilince metinHash'e bağlı katmanların hepsi geçersiz sayılıyordu: tek paragraf
değişse bile çizim, çapa, işaret, çıkmış konumu baştan üretilmek zorundaydı. Bu araç eski ve yeni metnin paragraflarını
birebir metin eşitliğiyle eşler (difflib) ve her katmanda yalnız AYNEN kalan paragrafların kaydını yeni dizine taşır.
Değişen ya da yeni paragrafın kaydı taşınmaz (cümle sırası değişmiş olabilir); o paragraflar raporda "yeniden üret"
diye listelenir. Ses ve zaman katmanları (cumle_zaman, kelime_zaman) taşınmaz: yeni sesten yeniden ölçülür (klipli
derste Whisper yalnız yeni klipleri çözer, bkz. kelime_zaman.py::klipli_isle).

Taşınan katmanlar (data/sesli_anlatim/<katman>/<key>.json):
  hizalama      paragraflar[i] (+ sayfaKaynak[i]); yeni paragraf önceki paragrafın sayfasını alır, guven 0 + "tasima": "yeni"
  capa          p[i]; yeni paragraf [] (capa_dogrula yeni paragrafları eksik gösterir → yalnız onlar yazılır); mdSha1 yenilenir
  isaret        c[i]; metinHash yenilenir, hizHash "tasindi" → pdf_isaret.py bir sonraki koşuda tümünü (ucuz, deterministik) yeniler
  cizim         p[i]; metinHash yenilenir (LLM ürünü, asıl kazanç burada)
  vurgu         p[i] (karakter aralıkları paragraf içi; aynen kalan paragrafta geçerli)
  cikmis_konum  q[*].p yeniden dizinlenir; değişen paragraftaki eşleme düşürülür (raporda listelenir)
  v2            bölümler yeni metnin @@ yapısıyla yeniden kurulur; aynen kalan paragraf nesnesi korunur, yeni olan boş cümleli
Her katman yalnız ESKİ metinle tutarlıysa (hash ya da paragraf sayısı) taşınır; zaten yeni metinle tutarlıysa dokunulmaz.
Yazmadan önce özgün dosyalar data/sesli_anlatim/.tasima_yedek/<key>/<zaman>/ altına kopyalanır.

Kullanım:
  klip_tasi.py <key> [--eski ESKI.md] [--kuru]
    --eski verilmezse eski metin git HEAD'deki metin/<key>.md'dir (metin işlenmeden önce çalıştırılmalı).
Çıkış: 0 tamam · 1 hata · 2 yeniden üretilecek paragraf var (rapor yazdırılır).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from difflib import SequenceMatcher
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
KOK = Path(os.environ.get("MEDS_SA_KOK") or MEDS / "data" / "sesli_anlatim")  # sınama: kopya kök


def paragraflar(md: str) -> list[dict]:
    """sesliAnlatim.ts::metinParagraflari ile BİREBİR aynı bölme: [{t, bolumBasi, bolumBaslik}]."""
    out: list[dict] = []
    bolum_basi, baslik, tampon = True, "", []

    def bitir():
        nonlocal bolum_basi, tampon
        t = re.sub(r"[ \t]+", " ", "\n".join(tampon)).strip()
        if t:
            out.append({"t": t, "bolumBasi": bolum_basi, "bolumBaslik": baslik})
            bolum_basi = False
        tampon = []

    for s in re.split(r"\r?\n", md):
        if s.startswith("# "):
            continue
        if s.startswith("@@"):
            bitir()
            bolum_basi, baslik = True, s[2:].strip()
            continue
        if not s.strip():
            bitir()
        else:
            tampon.append(s.strip())
    bitir()
    return out


def metin_hash(pars: list[dict]) -> str:
    return hashlib.sha1("\n".join(p["t"] for p in pars).encode("utf-8")).hexdigest()


def eslestir(eski: list[dict], yeni: list[dict]) -> dict[int, int]:
    """yeni dizin → eski dizin; yalnız metni birebir aynı kalan paragraflar."""
    sm = SequenceMatcher(None, [p["t"] for p in eski], [p["t"] for p in yeni], autojunk=False)
    m: dict[int, int] = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            m[b + k] = a + k
    return m


def oku(f: Path):
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("key")
    ap.add_argument("--eski", help="eski metin dosyası (varsayılan: git HEAD)")
    ap.add_argument("--kuru", action="store_true", help="yazmadan raporla")
    a = ap.parse_args()
    key = a.key
    md_yol = KOK / "metin" / f"{key}.md"
    if not md_yol.exists():
        print(f"metin yok: {md_yol}", file=sys.stderr)
        return 1
    yeni_md = md_yol.read_bytes()
    if a.eski:
        eski_md = Path(a.eski).read_bytes()
    else:
        r = subprocess.run(["git", "-C", str(MEDS), "show", f"HEAD:data/sesli_anlatim/metin/{key}.md"], capture_output=True)
        if r.returncode:
            print("eski metin git HEAD'de yok; --eski verin", file=sys.stderr)
            return 1
        eski_md = r.stdout
    if eski_md == yeni_md:
        print(f"{key}: metin değişmemiş, taşınacak bir şey yok")
        return 0
    E, Y = paragraflar(eski_md.decode("utf-8")), paragraflar(yeni_md.decode("utf-8"))
    eh, yh = metin_hash(E), metin_hash(Y)
    eski_md_sha, yeni_md_sha = hashlib.sha1(eski_md).hexdigest(), hashlib.sha1(yeni_md).hexdigest()
    m = eslestir(E, Y)
    yeniden = [i for i in range(len(Y)) if i not in m]
    rapor: list[str] = [f"{key}: {len(E)} → {len(Y)} paragraf, {len(m)} aynen kaldı, {len(yeniden)} değişti/yeni: "
                        + (", ".join(str(i) for i in yeniden) or "—")]
    yazilacak: dict[Path, object] = {}

    def tasi_dict(d: dict) -> dict:
        return {str(y): d[str(e)] for y, e in sorted(m.items()) if str(e) in d}

    # hizalama
    f = KOK / "hizalama" / f"{key}.json"
    j = oku(f)
    if j and isinstance(j.get("paragraflar"), list):
        if len(j["paragraflar"]) == len(E):
            hp = []
            for i in range(len(Y)):
                if i in m:
                    hp.append(j["paragraflar"][m[i]])
                else:
                    onceki = hp[-1] if hp else (j["paragraflar"][0] if j["paragraflar"] else {"dosya": 0, "sayfa": 1})
                    hp.append({"dosya": onceki.get("dosya", 0), "sayfa": onceki.get("sayfa", 1), "guven": 0, "tasima": "yeni"})
            j["paragraflar"] = hp
            if isinstance(j.get("sayfaKaynak"), list) and len(j["sayfaKaynak"]) == len(E):
                j["sayfaKaynak"] = [j["sayfaKaynak"][m[i]] if i in m else None for i in range(len(Y))]
            yazilacak[f] = j
            rapor.append(f"  hizalama: taşındı ({len(yeniden)} yeni paragrafa önceki sayfa, guven 0 — pdf_hizala/çapa ile doğrulayın)")
        elif len(j["paragraflar"]) == len(Y):
            rapor.append("  hizalama: zaten yeni metinle tutarlı, dokunulmadı")
        else:
            rapor.append(f"  hizalama: ATLANDI (paragraf sayısı {len(j['paragraflar'])} eski {len(E)} / yeni {len(Y)} ile tutmuyor)")

    # capa
    f = KOK / "capa" / f"{key}.json"
    j = oku(f)
    if j:
        if j.get("mdSha1") == eski_md_sha and len(j.get("p") or []) == len(E):
            j["p"] = [j["p"][m[i]] if i in m else [] for i in range(len(Y))]
            j["mdSha1"] = yeni_md_sha
            yazilacak[f] = j
            rapor.append("  capa: taşındı (yeni paragraflar boş → yalnız onlara çapa yazılmalı)")
        elif j.get("mdSha1") == yeni_md_sha:
            rapor.append("  capa: zaten güncel")
        else:
            rapor.append("  capa: ATLANDI (mdSha1 eski metinle tutmuyor)")

    # metinHash'li sözlük katmanları
    for katman, alan, ek in (("isaret", "c", {"hizHash": "tasindi"}), ("cizim", "p", {})):
        f = KOK / katman / f"{key}.json"
        j = oku(f)
        if not j:
            continue
        if j.get("metinHash") == eh:
            once = len(j.get(alan) or {})
            j[alan] = tasi_dict(j.get(alan) or {})
            j["metinHash"] = yh
            j.update(ek)
            yazilacak[f] = j
            rapor.append(f"  {katman}: {len(j[alan])}/{once} paragraf kaydı taşındı")
        elif j.get("metinHash") == yh:
            rapor.append(f"  {katman}: zaten güncel")
        else:
            rapor.append(f"  {katman}: ATLANDI (metinHash eski metinle tutmuyor)")

    # vurgu: hash yok; paragraf dizinleri eski metne göre kabul edilir (anahtarlar eski paragraf sayısını aşmamalı)
    f = KOK / "vurgu" / f"{key}.json"
    j = oku(f)
    if j and isinstance(j.get("p"), dict):
        if all(k.isdigit() and int(k) < len(E) for k in j["p"]):
            once = len(j["p"])
            j["p"] = tasi_dict(j["p"])
            yazilacak[f] = j
            rapor.append(f"  vurgu: {len(j['p'])}/{once} paragraf kaydı taşındı")
        else:
            rapor.append("  vurgu: ATLANDI (dizinler eski metne uymuyor)")

    # cikmis_konum
    f = KOK / "cikmis_konum" / f"{key}.json"
    j = oku(f)
    if j and isinstance(j.get("q"), list):
        if j.get("metinHash") == eh:
            ters = {e: y for y, e in m.items()}
            kalan, dusen = [], []
            for q in j["q"]:
                if isinstance(q.get("p"), int) and q["p"] in ters:
                    kalan.append({**q, "p": ters[q["p"]]})
                else:
                    dusen.append(str(q.get("id")))
            j["q"], j["metinHash"] = kalan, yh
            yazilacak[f] = j
            rapor.append(f"  cikmis_konum: {len(kalan)} eşleme taşındı" + (f", {len(dusen)} düştü (değişen paragraf): {', '.join(dusen)}" if dusen else ""))
        elif j.get("metinHash") == yh:
            rapor.append("  cikmis_konum: zaten güncel")
        else:
            rapor.append("  cikmis_konum: ATLANDI (metinHash eski metinle tutmuyor)")

    # v2
    f = KOK / "v2" / f"{key}.json"
    j = oku(f)
    if j and isinstance(j.get("bolumler"), list):
        duz = [(b, p) for b in j["bolumler"] for p in (b.get("paragraflar") or [])]
        sade = lambda t: re.sub(r"\s+", " ", t or "").strip()  # noqa: E731
        # v2 metinle birlikte düzenlendiyse (cümle sesleri yeni paragraflarla aynı) dokunulmaz — paragraf sayısı değişmediğinde
        # eski kontrol bunu eski metinle tutarlı sanıp değişen paragrafları boşaltıyordu (2026-10-30, k2-05-v2).
        yeni_tutarli = len(duz) == len(Y) and all(
            sade(" ".join(c.get("ses", "") for c in (pp.get("cumleler") or []))) == sade(Y[i]["t"]) for i, (_, pp) in enumerate(duz))
        if yeni_tutarli:
            rapor.append("  v2: zaten yeni metinle tutarlı")
        elif len(duz) == len(E):
            yeni_b: list[dict] = []
            for i, p in enumerate(Y):
                if p["bolumBasi"] or not yeni_b:
                    kaynak = next((duz[m[k]][0] for k in range(i, len(Y)) if k in m and (k == i or not Y[k]["bolumBasi"])), None)
                    b = {kk: vv for kk, vv in (kaynak or {"id": f"{key}-yeni-b{len(yeni_b) + 1}"}).items() if kk != "paragraflar"}
                    b["baslik"] = p["bolumBaslik"] or b.get("baslik", "")
                    b["paragraflar"] = []
                    yeni_b.append(b)
                yeni_b[-1]["paragraflar"].append(duz[m[i]][1] if i in m else {"id": f"{key}-yeni-p{i + 1:03d}", "cumleler": []})
            j["bolumler"] = yeni_b
            yazilacak[f] = j
            rapor.append(f"  v2: {len(yeni_b)} bölüm yeniden kuruldu, {len(yeniden)} paragraf boş (konusma_v2 ile yazılmalı)")
        elif len(duz) == len(Y):
            rapor.append("  v2: zaten yeni metinle tutarlı")
        else:
            rapor.append("  v2: ATLANDI (paragraf sayısı tutmuyor)")

    if yeniden:
        rapor.append("Yeniden üret (yalnız bu paragraflar): çapa, çizim (cizim_kapisi 0 HATA), çıkmış konumu, v2; "
                     "sonra pdf_isaret.py (tümü, deterministik) ve ses → cumle_zaman/kelime_zaman.")
    print("\n".join(rapor))
    if a.kuru or not yazilacak:
        return 2 if yeniden else 0
    yedek = KOK / ".tasima_yedek" / key / time.strftime("%Y%m%d-%H%M%S")
    yedek.mkdir(parents=True, exist_ok=True)
    for f, j in yazilacak.items():
        shutil.copy2(f, yedek / f"{f.parent.name}.json")
        tmp = f.with_suffix(".tmp")
        tmp.write_text(json.dumps(j, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        tmp.replace(f)
    print(f"yedek: {yedek}")
    return 2 if yeniden else 0


if __name__ == "__main__":
    sys.exit(main())
