#!/usr/bin/env python3
"""
Faz 6 doğrulayıcı — yapay zekâ kullanmaz, yalnızca CPU (faz zincirinde Faz 6'dan sonra çalışır).

Faz 6 (gemma3:4b) çıktısında uydurma hastalık adları ("İçime Bakma Bozukluğu") ve yanlış ICD kodları görüldü.
Her öğe ders materyaline (sınav dökümleri hariç) ve ICD-10 yapısına karşı denetlenir:

  * ICD-10 kodu   : biçim (A00–Z99[.x]) + resmî listeye göre kod–ad uyumu (liste yoksa hiçbir kod kabul edilmez)
                    + hastalık adının materyalde kanıtı
  * ayırıcı tanı  : hastalık adının içerik kelimeleri (5 harf kök) materyalde AYNI slayt/sayfada birlikte geçmeli
  * arama etiketi : aynı ölçüt
Sonuç öğe bazında: "kanitli" | "kanitsiz" | "gecersiz_kod".

Çıktı (Faz 6 verisine DOKUNMAZ): meds_database_v2/deep_metadata_validated/
  * dogrulama.jsonl — soru başına yalnızca kanıtlı öğeler + atılanların listesi
  * rapor.json
Daha önce doğrulanmış sorular atlanır (artımlı); --full ile hepsi yeniden denetlenir.
"""
from __future__ import annotations

import collections
import glob
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase8_curriculum_graph as P8  # noqa: E402

V2 = P8.PROJECT / "meds_database_v2"
IN_DIR = V2 / "deep_metadata"
OUT = V2 / "deep_metadata_validated"
# Resmî ICD-10 kod listesi (kod<TAB>ad ya da JSON {kod: ad}). Yoksa kod–ad uyumu doğrulanamaz ve hiçbir kod
# "kanıtlı" sayılmaz: elle kontrolde adı doğru ama kodu yanlış kayıtlar çoğunluktaydı (R50.9 "hemoraji", J10 "romatizmal ateş").
ICD_REF = Path(os.environ.get("MEDS_ICD10_FILE") or V2 / "reference" / "icd10.tsv")
ICD_RE = re.compile(r"^[A-TV-Z][0-9]{2}(\.[0-9A-Z]{1,4})?$")
# ICD-10 bölümleri (harf + sayı aralığı)
ICD_CHAPTERS = [
    ("A00", "B99", "Enfeksiyon ve parazit hastalıkları"), ("C00", "D48", "Neoplazmlar"),
    ("D50", "D89", "Kan ve bağışıklık"), ("E00", "E90", "Endokrin, beslenme, metabolizma"),
    ("F00", "F99", "Ruhsal ve davranışsal bozukluklar"), ("G00", "G99", "Sinir sistemi"),
    ("H00", "H59", "Göz"), ("H60", "H95", "Kulak"), ("I00", "I99", "Dolaşım sistemi"),
    ("J00", "J99", "Solunum sistemi"), ("K00", "K93", "Sindirim sistemi"), ("L00", "L99", "Deri"),
    ("M00", "M99", "Kas-iskelet ve bağ dokusu"), ("N00", "N99", "Genitoüriner sistem"),
    ("O00", "O99", "Gebelik, doğum, lohusalık"), ("P00", "P96", "Perinatal dönem"),
    ("Q00", "Q99", "Konjenital malformasyonlar"), ("R00", "R99", "Semptom ve bulgular"),
    ("S00", "T98", "Yaralanma ve zehirlenme"), ("V01", "Y98", "Dış nedenler"), ("Z00", "Z99", "Sağlık hizmeti faktörleri"),
]
GENERIC = set("hastalik hasta bozukluk sendrom durum tablo klinik tani tedavi diger benzer ilgili akut kronik tip "
              "primer sekonder genel".split())


def icd_chapter(code: str) -> str | None:
    k = code[:3]
    for a, b, name in ICD_CHAPTERS:
        if a <= k <= b:
            return name
    return None


def load_icd_ref() -> dict:
    if not ICD_REF.exists():
        return {}
    if ICD_REF.suffix == ".json":
        return {k.upper(): v for k, v in json.load(open(ICD_REF, encoding="utf-8")).items()}
    ref = {}
    for line in open(ICD_REF, encoding="utf-8"):
        if line.startswith("#"):
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) >= 2:
            ref[parts[0].strip().upper()] = parts[1].strip()
    return ref


def name_matches(name: str, ref_name: str) -> bool:
    """Kod–ad uyumu: genel kelimeler hariç, adın içerik köklerinin en az yarısı referans adda geçmeli."""
    a = {x for x in P8.stems(name) if x not in GENERIC and x not in ICD_GENERIC}
    b = set(P8.stems(ref_name))
    return bool(a) and len(a & b) / len(a) >= 0.5


ICD_GENERIC = set("bagim bozuk enfek belir spesi diger ilisk komplik tumor kanse hasta sendr".split())


def build_index():
    sources = P8.load_sources()
    chunks_by_src = P8.load_chunks()
    dumps = {s for s, src in sources.items() if P8.is_exam_dump(src, chunks_by_src)}
    post = collections.defaultdict(set)
    n = 0
    for sid, cs in chunks_by_src.items():
        if sid in dumps:
            continue
        for c in cs:
            for st in set(P8.stems(c.get("text") or "")):
                post[st].add(n)
            n += 1
    return post, n


def attested(name: str, post) -> bool:
    """Adın içerik kökleri materyalde aynı chunk içinde birlikte geçiyor mu?"""
    sts = [s for s in dict.fromkeys(P8.stems(name)) if s not in GENERIC and len(s) >= 4]
    if not sts:
        return False
    sets = [post.get(s) for s in sts]
    if any(not x for x in sets):
        return False
    sets.sort(key=len)
    inter = set(sets[0])
    for x in sets[1:]:
        inter &= x
        if not inter:
            return False
    return True


def main():
    full = "--full" in sys.argv
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    out_path = OUT / "dogrulama.jsonl"
    done = set()
    if out_path.exists() and not full:
        for line in open(out_path, encoding="utf-8"):
            try:
                done.add(json.loads(line)["question_id"])
            except Exception:
                pass
    todo = []
    for p in sorted(glob.glob(str(IN_DIR / "*_deep_metadata.jsonl"))):
        if Path(p).name.startswith("lecture"):
            continue
        for r in P8.read_jsonl(Path(p)):
            qid = r.get("question_id")
            if qid and qid not in done and r.get("deep_metadata"):
                done.add(qid)
                todo.append(r)
    if not todo:
        print("Doğrulanacak yeni Faz 6 kaydı yok.")
        return 0
    post, nchunk = build_index()
    icd_ref = load_icd_ref()
    st = collections.Counter()
    mode = "w" if full else "a"
    with open(out_path, mode, encoding="utf-8") as f:
        for r in todo:
            dm = r["deep_metadata"]
            keep = {"icd10": [], "ayirici_tani": [], "etiketler": []}
            drop = []
            for x in dm.get("icd10_ve_protokoller") or []:
                if not isinstance(x, dict):
                    continue
                code = str(x.get("kod") or "").strip().upper()
                name = str(x.get("ad") or "")
                if not ICD_RE.match(code) or not icd_chapter(code):
                    drop.append({"tur": "icd10", "deger": f"{code} {name}", "neden": "gecersiz_kod"}); st["icd_gecersiz"] += 1
                elif not icd_ref:
                    drop.append({"tur": "icd10", "deger": f"{code} {name}", "neden": "referans_yok"}); st["icd_referans_yok"] += 1
                elif code not in icd_ref or not name_matches(name, icd_ref[code]):
                    drop.append({"tur": "icd10", "deger": f"{code} {name}", "neden": "kod_ad_uyumsuz"}); st["icd_kod_ad_uyumsuz"] += 1
                elif not attested(name, post):
                    drop.append({"tur": "icd10", "deger": f"{code} {name}", "neden": "kanitsiz"}); st["icd_kanitsiz"] += 1
                else:
                    keep["icd10"].append({"kod": code, "ad": name, "icd_bolumu": icd_chapter(code)}); st["icd_kanitli"] += 1
            for x in dm.get("ayirici_tani_listesi") or []:
                if not isinstance(x, dict):
                    continue
                h = str(x.get("hastalik") or "")
                if attested(h, post):
                    keep["ayirici_tani"].append({"hastalik": h, "ozellik": x.get("ayirici_ozellik")}); st["ayirici_kanitli"] += 1
                else:
                    drop.append({"tur": "ayirici_tani", "deger": h, "neden": "kanitsiz"}); st["ayirici_kanitsiz"] += 1
            for t in dm.get("hiper_arama_etiketleri") or []:
                if isinstance(t, str) and attested(t, post):
                    keep["etiketler"].append(t); st["etiket_kanitli"] += 1
                else:
                    st["etiket_kanitsiz"] += 1
            f.write(json.dumps({"question_id": r["question_id"], "dogrulandi": time.strftime("%Y-%m-%dT%H:%M:%S"),
                                **keep, "atilan": drop}, ensure_ascii=False) + "\n")
            st["soru"] += 1
    rep = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "materyal_chunk": nchunk, **dict(st),
           "sure_sn": round(time.time() - t0, 1)}
    for k in ("icd", "ayirici", "etiket"):
        ok, bad = st[f"{k}_kanitli"], sum(v for kk, v in st.items() if kk.startswith(k + "_") and kk != f"{k}_kanitli")
        rep[f"{k}_kanitli_%"] = round(100 * ok / (ok + bad), 1) if ok + bad else None
    json.dump(rep, open(OUT / "rapor.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
