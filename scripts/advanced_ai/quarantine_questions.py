#!/usr/bin/env python3
"""
Soru karantinası — birleşik/bozuk soruları tespit eder; hiçbir soruyu SİLMEZ.

Tespit (soru başına gerekçeli):
  * sikta_baska_soru     : şık metninde başka bir sorunun kökü ("?", "hangisi", "aşağıdaki…")
  * kokte_iki_soru       : kökte ≥ 2 soru işareti (I/II/III öncüllü sorular hariç)
  * sinav_sitesi_kalintisi: "Sıra No", "Anasayfa / Sınav Sonucu", sinav.karabuk…, "DÖNEM 3 BÜTÜNLEME SORU…" sayfa başlığı
  * sik_sayisi_bozuk     : < 2 ya da > 6 şık, ya da aynı harf iki kez (A, B, C, D, A, B…)
  * kesik_kok            : kök "000 nüfuslu…" gibi rakam/küçük harfle ortadan başlıyor ve çok kısa
Kaynaklar: data/pastQuestions.json (site arşivi) ve $MEDS_DATABASE_DIR/questions (veritabanı).
Çıktı: $MEDS_DATABASE_DIR/derived/quarantine/karantina.json  {kimlik: {neden: [...], kaynak, dosya}}
Sunucu (/api/past-exams) ve faz çıktıları bu listeyi okuyup karantinadaki soruları göstermez/kullanmaz.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = Path(os.environ.get("MEDS_DATABASE_DIR") or ROOT.parent / "meds_database")
OUT = DB / "derived" / "quarantine" / "karantina.json"
JUNK = re.compile(r"Anasayfa|S[ıi]nav Sonucu|S[ıi]ra No|sinav\.karab|s෈nav|D[öo]nem \d Kurul \d Sonucu|"
                  r"D[ÖO]NEM\s*\d\s*(B[ÜU]T[ÜU]NLEME|F[İI]NAL|KURUL)\s*SORU|^\s*(No|Duru)\s*$", re.I | re.M)
QPAT = re.compile(r"\?|\bhangisi|\başağıdaki", re.I)
ROMAN = re.compile(r"\b(I|II|III|IV|V)\s*[\.\-\)]")


def opts_of(q) -> list[tuple[str, str]]:
    o = q.get("options")
    if isinstance(o, dict):
        return [(k, v or "") for k, v in o.items()]
    if isinstance(o, list):
        return [(str(x.get("key")), x.get("text") or "") for x in o if isinstance(x, dict)]
    return []


def stem_of(q) -> str:
    s = q.get("stem")
    if not s and isinstance(q.get("reconstruction"), dict):
        s = q["reconstruction"].get("stem")
    if not s and q.get("fragments"):
        s = (q["fragments"][0] or {}).get("text")
    return s or ""


def reasons(q) -> list[str]:
    st, op = stem_of(q), opts_of(q)
    r = []
    if any(QPAT.search(t) for _, t in op):
        r.append("sikta_baska_soru")
    # ayrı soru işareti grupları ("???" tek sayılır) ve aralarında gerçek metin
    qgroups = [m.start() for m in re.finditer(r"\?+", st)]
    if len(qgroups) >= 2 and not ROMAN.search(st) and qgroups[-1] - qgroups[0] > 25:
        r.append("kokte_iki_soru")
    if JUNK.search(st) or any(JUNK.search(t) for _, t in op):
        r.append("sinav_sitesi_kalintisi")
    keys = [k for k, _ in op]
    if len(op) < 2 or len(op) > 6 or len(set(keys)) != len(keys):
        r.append("sik_sayisi_bozuk")
    if re.match(r"^\s*\d{3,}\s+[a-zçğıöşü]", st) or (re.match(r"^\s*[a-zçğıöşü]", st) and len(st) < 80
                                                        and not re.search(r"hangisi|nedir|\?|değildir|doğrudur|yanlıştır", st, re.I)):
        r.append("kesik_kok")
    if not st.strip():
        r.append("bos_kok")
    if op and all(re.fullmatch(r"\s*Se[çc]enek\s+[A-E]\s*", t or "") for _, t in op):
        r.append("yer_tutucu_sik")
    return r


def repair(q):
    """Yalnız sınav sitesi kalıntısı varsa: "Sıra No", tarih/URL satırları ve kalıntı şıklar temizlenir.
    Onarılan soru TÜM kontrollerden geçerse onarım kabul edilir; değilse karantina."""
    st = "\n".join(l for l in stem_of(q).split("\n") if not JUNK.search(l) and not re.search(r"\d{2}\.\d{2}\.\d{4}|https?://|\.html", l))
    st = re.sub(r"^\s*(\S+(\s+\S+){0,3})\s+\1\s+", r"\1 ", st.strip())        # "HALK SAĞLIĞI HALK SAĞLIĞI" tekrarı
    st = " ".join(st.replace("\u200f", "").replace("\u200e", "").split())
    st = re.sub(r"^\d{4}/\d{1,2}/\d{1,2}\s+\w{0,4}\s+", "", st)          # "2021/6/22 Du …"
    st = re.sub(r"^(Du|Duru|Durum)\s+", "", st)
    if re.match(r"^[A-Z]\s+(I|II|III|IV)\b|^(Yalnız|I,)", st):               # önceki sorunun şık artığı
        return None
    op = [(k, " ".join(t.split())) for k, t in opts_of(q) if t and not JUNK.search(t) and not re.search(r"\.html|^[\uf000-\uf0ff\s]*$", t)]
    keys = "ABCDEF"
    op = [(keys[i], t) for i, (_, t) in enumerate(op[:6])]
    # tutucu: şıklarda kalıntı varsa ya da kökte ≥ 2 şık metni tekrar ediyorsa onarma (karantina)
    if any(JUNK.search(t or "") for _, t in opts_of(q)) or len(op) != len(opts_of(q)):
        return None
    if sum(1 for _, t in op if len(t) >= 4 and t.lower() in st.lower()) >= 2:
        return None
    fake = {"stem": st, "options": [{"key": k, "text": t} for k, t in op]}
    return fake if st and not reasons(fake) else None


def main():
    out = {}
    onarim = {}
    stats = {}
    pq = ROOT / "data" / "pastQuestions.json"
    if pq.exists():
        d = json.load(open(pq, encoding="utf-8"))
        d = d if isinstance(d, list) else d.get("questions", [])
        n = 0
        rep = 0
        for q in d:
            r = reasons(q)
            if r == ["sinav_sitesi_kalintisi"]:
                fixed = repair(q)
                if fixed:
                    onarim[str(q.get("id"))] = fixed
                    rep += 1
                    continue
            if r:
                out[str(q.get("id"))] = {"neden": r, "kaynak": "site_arsivi", "dosya": q.get("sourceFile")}
                n += 1
        stats["site_arsivi"] = {"toplam": len(d), "karantina": n, "onarildi": rep}
    # Kuralla yeniden bölünmüş sınav çıktısı soruları (resplit_exam_printout.py): karantinadaki combinepdf sorusu
    # kök benzerliğiyle (≥ 0,55 Jaccard) eşleşirse aynı kimlikle temiz kök/şıklarla geri gelir; cevap doğrulanmamış kalır.
    rs_path = DB / "derived" / "resplit" / "combinepdf_sorular.jsonl"
    rs = [json.loads(l) for l in open(rs_path, encoding="utf-8")] if rs_path.exists() else []
    def toks(x):
        return {w for w in re.sub(r"[^a-zçğıöşü0-9 ]", " ", (x or "").lower()).split() if len(w) > 2}
    rs_t = [(toks(r["stem"]), r) for r in rs]
    rs_used = 0
    if pq.exists():
        for q in d:
            qid = str(q.get("id"))
            if qid not in out or str(q.get("sourceFile")) != "c4259dc9087e":
                continue
            t = toks(stem_of(q))
            best, bj = None, 0.0
            for tr, r in rs_t:
                if t and tr:
                    j = len(t & tr) / len(t | tr)
                    if j > bj:
                        best, bj = r, j
            if best and bj >= 0.55:
                onarim[qid] = {"stem": best["stem"], "options": [{"key": k, "text": v} for k, v in best["options"].items()],
                               "yontem": "yeniden_bolme", "benzerlik": round(bj, 2)}
                del out[qid]
                rs_used += 1
        stats["site_arsivi"]["yeniden_bolme_ile_geri_geldi"] = rs_used
        stats["site_arsivi"]["karantina"] -= rs_used
    n = t = 0
    for p in glob.glob(str(DB / "questions" / "*.jsonl")):
        for line in open(p, encoding="utf-8"):
            try:
                q = json.loads(line)
            except Exception:
                continue
            t += 1
            r = reasons(q)
            if r:
                key = str(q.get("question_id"))
                prev = out.get(key)
                out[key] = {"neden": sorted(set(r) | set((prev or {}).get("neden", []))), "kaynak": "veritabani",
                            "dosya": q.get("source_id")}
                n += 1
    stats["veritabani"] = {"toplam": t, "karantina": n}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".tmp")
    json.dump({"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "sayilar": stats, "sorular": out, "onarim": onarim},
              open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(tmp, OUT)
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
