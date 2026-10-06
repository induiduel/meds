#!/usr/bin/env python3
"""
Hakem kuyruğu — belirsiz eşleştirmeleri büyük bir modelle denetler (faz zincirinde Aşama 1'den sonra).

Kuyruklar
  1. konu  : Faz 10 (yoksa Faz 9) ağacında güveni orta/düşük olan sorular → model aday konulardan (en çok 3) birini seçer.
  2. slayt : Faz 11'de güveni düşük soru–slayt eşleşmeleri → model ilk 3 slayttan birini seçer ya da "hiçbiri" der.
Kurallar
  * Model YALNIZCA verilen aday kanıtlarına dayanır; seçimini adayın kanıt metninden BİREBİR alıntıyla gerekçelendirir.
  * Alıntı adayın metninde doğrulanamazsa karar "reddedildi" sayılır (kabul edilmez).
  * Olumsuz köklü sorular (yanlıştır/değildir…) modele açıkça belirtilir.
  * Kararlar ayrı dosyaya yazılır; Faz 8–11 çıktıları ve ana veritabanı DEĞİŞTİRİLMEZ.
  * Her turda en çok --max kayıt (varsayılan 80); daha önce karar verilen kayıt tekrar sorulmaz.
Model: Groq gpt-oss-120b (sunucu .env içindeki anahtar); yanıt yoksa kayıt sonraki tura kalır.

Çıktı: meds_temp/hakem/kararlar.jsonl, rapor.json
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase8_curriculum_graph as P8  # noqa: E402
from phase7_question_metadata_v2 import call_groq, quote_ok, NEG, GROQ_KEYS  # noqa: E402

TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or P8.PROJECT / "meds_temp")
OUT = TEMP / "hakem"
TREES = [TEMP / "phase10" / "soru_kazanim.jsonl", TEMP / "phase9" / "soru_kazanim.jsonl"]
SLIDES = TEMP / "phase11" / "soru_slayt.jsonl"

SYSTEM = """Sen tıp fakültesi müfredat hakemisin. Yalnızca verilen aday metinlere dayanırsın; kendi bilgini kanıt
yerine koymazsın. Seçimini, seçtiğin adayın metninden kelimesi kelimesine bir alıntıyla gerekçelendirirsin.
Hiçbir aday soruyla ilgili değilse "hicbiri" dersin. Yanıtın yalnızca geçerli JSON'dur."""


def log(m):
    print(f"[{time.strftime('%H:%M:%S')}] [hakem] {m}", flush=True)


def llm(prompt: str) -> dict | None:
    raw = call_groq([{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}], max_tokens=1200)
    if not raw:
        return None
    raw = re.sub(r"^```(json)?|```$", "", raw.strip()).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", raw, re.S)
        try:
            return json.loads(m.group(0)) if m else None
        except json.JSONDecodeError:
            return None


def questions():
    out = {}
    for p in sorted((P8.DB / "questions").glob("*.jsonl")):
        for q in P8.read_jsonl(p):
            opts = q.get("options") if isinstance(q.get("options"), dict) else {}
            out[q["question_id"]] = {"stem": q.get("stem") or "", "options": opts,
                                     "answer": (q.get("answer") or "").strip().upper()}
    return out


def qblock(q):
    opts = "\n".join(f"{k}) {v}" for k, v in q["options"].items())
    tip = "OLUMSUZ KÖK (doğru cevap yanlış/uymayan ifadedir)" if NEG.search(q["stem"]) else "olumlu kök"
    ans = f"Kayıtlı cevap: {q['answer']}" if q["answer"] else "Cevap bilinmiyor"
    return f"SORU ({tip}): {q['stem']}\n{opts}\n{ans}"


def konu_items(done):
    for p in TREES:
        if p.exists():
            for r in P8.read_jsonl(p):
                key = f"konu:{r['soru_id']}"
                if key in done or r.get("guven") == "yuksek" or len(r.get("kazanimlar") or []) < 2:
                    continue
                yield key, r
            return


def slayt_items(done):
    if SLIDES.exists():
        for r in P8.read_jsonl(SLIDES):
            key = f"slayt:{r['soru_id']}"
            if key in done or r.get("guven") != "dusuk" or len(r.get("slaytlar") or []) < 2:
                continue
            yield key, r


def judge(kind, r, q):
    if kind == "konu":
        cands = []
        for i, k in enumerate(r["kazanimlar"][:3], 1):
            ev = (k.get("kanit") or {}).get("metin") or ""
            cands.append((i, f"{k.get('ders')} / {k.get('konu')} — kazanım: {k.get('kazanim')}", ev, k))
    else:
        cands = [(i, f"{s.get('kaynak')} s.{s.get('sayfa')}", s.get("alinti") or "", s)
                 for i, s in enumerate(r["slaytlar"][:3], 1)]
    body = "\n\n".join(f"[ADAY {i}] {title}\nKANIT METNİ: {ev[:700]}" for i, title, ev, _ in cands)
    prompt = (f"{qblock(q)}\n\n{'Bu soru hangi müfredat konusuna aittir?' if kind == 'konu' else 'Bu sorunun bilgisi hangi slayttadır?'}\n\n"
              f"{body}\n\nJSON: {{\"secim\": 1|2|3|\"hicbiri\", \"alinti\": \"seçilen adayın KANIT METNİ'nden birebir\", "
              f"\"gerekce\": \"tek cümle\"}}")
    d = llm(prompt)
    if d is None:
        return None
    sec = str(d.get("secim")).strip().lower()
    if sec in ("hicbiri", "hiçbiri", "none"):
        return {"karar": "hicbiri", "gerekce": d.get("gerekce")}
    try:
        i = int(sec)
        _, title, ev, obj = cands[i - 1]
    except (ValueError, IndexError):
        return {"karar": "reddedildi", "neden": f"geçersiz seçim: {sec}"}
    al = (d.get("alinti") or "").strip()
    if not quote_ok(al, ev):
        return {"karar": "reddedildi", "neden": "alıntı adayın kanıtında yok", "secim": i, "alinti": al[:200]}
    return {"karar": "kabul", "secim": i, "secilen": title, "alinti": al[:300], "gerekce": d.get("gerekce"),
            "degisti": i != 1,
            "hedef": ({"konu_id": obj.get("konu_id"), "konu": obj.get("konu"), "ders": obj.get("ders"), "kurul": obj.get("kurul"),
                       "kazanim_id": obj.get("kazanim_id")} if kind == "konu" else
                      {"source_id": obj.get("source_id"), "sayfa": obj.get("sayfa"), "chunk_id": obj.get("chunk_id")})}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=80)
    a = ap.parse_args()
    if not GROQ_KEYS:
        log("Groq anahtarı yok; hakem kuyruğu atlandı")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "kararlar.jsonl"
    done = set()
    if path.exists():
        for r in P8.read_jsonl(path):
            if r.get("karar") in ("kabul", "hicbiri", "reddedildi"):
                done.add(r["anahtar"])
    qs = questions()
    st = collections.Counter()
    # sırayla: önce slayt (Faz 11 düşük), sonra konu; iki kuyruk dengeli paylaşır
    queue = []
    sl, ko = list(slayt_items(done)), list(konu_items(done))
    for i in range(max(len(sl), len(ko))):
        if i < len(sl):
            queue.append(("slayt",) + sl[i])
        if i < len(ko):
            queue.append(("konu",) + ko[i])
    log(f"bekleyen: slayt {len(sl)}, konu {len(ko)}; bu tur en çok {a.max}")
    with open(path, "a", encoding="utf-8") as f:
        for kind, key, r in queue[: a.max]:
            q = qs.get(r["soru_id"])
            if not q:
                continue
            res = judge(kind, r, q)
            if res is None:
                st["yanit_yok"] += 1
                if st["yanit_yok"] >= 5:
                    log("model art arda yanıt vermiyor; kalanlar sonraki tura")
                    break
                continue
            st[f"{kind}_{res['karar']}"] += 1
            f.write(json.dumps({"anahtar": key, "tur": kind, "soru_id": r["soru_id"],
                                "zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), **res}, ensure_ascii=False) + "\n")
            f.flush()
            time.sleep(1.2)
    rep = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "bekleyen_slayt": len(sl), "bekleyen_konu": len(ko), **dict(st)}
    json.dump(rep, open(OUT / "rapor.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
