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
  * Sürüm 2 (2026-10-06 denetimi: kabul edilenlerin ~%75'i doğruydu): model emin/orta/zayif verir; yalnızca
    "emin" + doğrulanmış ≥5 kelimelik alıntı "uygulanir"; kısa/şıksız sorular atlanır; anahtar_suphesi işaretlenir.
    Sürüm 1 kararları yeniden sorulur. Uygulama: publish_to_database.py.
Model zinciri: Groq gpt-oss-120b → qwen3.8-27b → Gemini flash (kota dolunca sıradaki); yanıt yoksa kayıt sonraki tura kalır.

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
from phase7_question_metadata_v2 import quote_ok, NEG, GROQ_KEYS, ENV  # noqa: E402
import urllib.error  # noqa: E402
import urllib.request  # noqa: E402

TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or P8.PROJECT / "meds_temp")
OUT = TEMP / "hakem"
TREES = [TEMP / "phase10" / "soru_kazanim.jsonl", TEMP / "phase9" / "soru_kazanim.jsonl"]
SLIDES = TEMP / "phase11" / "soru_slayt.jsonl"

SYSTEM = """Sen tıp fakültesi müfredat hakemisin. Yalnızca verilen aday metinlere dayanırsın; kendi bilgini kanıt
yerine koymazsın. Seçimini, seçtiğin adayın metninden kelimesi kelimesine bir alıntıyla gerekçelendirirsin.
Hiçbir aday soruyla ilgili değilse "hicbiri" dersin. Yanıtın yalnızca geçerli JSON'dur."""


def log(m):
    print(f"[{time.strftime('%H:%M:%S')}] [hakem] {m}", flush=True)


# Model zinciri: Groq gpt-oss-120b (günlük 200k token) → Groq qwen3.8-27b → Gemini flash. Kota (429) dolan
# model bu çalıştırmada bir daha denenmez. Kararın hangi modelden geldiği kayda yazılır.
MODELS = [("groq", "openai/gpt-oss-120b"), ("groq", "qwen/qwen3.8-27b"), ("gemini", "gemini-flash-latest"),
          ("gemini", "gemini-3.5-flash")]
_exhausted: set = set()
_last_model = {"ad": None}


def _groq(model, prompt):
    body = {"model": model, "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
            "temperature": 0.1, "max_tokens": 1200, "response_format": {"type": "json_object"}}
    req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {GROQ_KEYS[0]}", "Content-Type": "application/json",
                                          "User-Agent": "medsor-hakem/2"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]


def _gemini(model, prompt):
    key = ENV.get("GEMINI_API_KEY") or ENV.get("GEMINI_FREE_KEY_2")
    if not key:
        raise RuntimeError("anahtar yok")
    body = {"systemInstruction": {"parts": [{"text": SYSTEM}]}, "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1, "maxOutputTokens": 1500}}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]


def llm(prompt: str) -> dict | None:
    for prov, model in MODELS:
        if model in _exhausted:
            continue
        for attempt in range(2):
            try:
                raw = (_groq if prov == "groq" else _gemini)(model, prompt)
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    body = e.read()[:300].decode("utf-8", "replace")
                    if "per day" in body or "TPD" in body or "RPD" in body or "PerDay" in body:
                        log(f"{model}: günlük kota doldu, sonraki modele geçiliyor")
                        _exhausted.add(model)
                        break
                    time.sleep(30)          # dakikalık kota: bekle, aynı modelle tekrar dene
                    continue
                if e.code in (400, 404, 401, 403):
                    _exhausted.add(model)
                    break
                time.sleep(5)
                continue
            except Exception:  # noqa: BLE001
                time.sleep(5)
                continue
            raw = re.sub(r"<think>.*?</think>", "", raw or "", flags=re.S)
            raw = re.sub(r"^```(json)?|```$", "", raw.strip()).strip()
            try:
                d = json.loads(raw)
            except json.JSONDecodeError:
                m = re.search(r"\{.*\}", raw, re.S)
                try:
                    d = json.loads(m.group(0)) if m else None
                except json.JSONDecodeError:
                    d = None
            if d is not None:
                _last_model["ad"] = model
                return d
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
              f"{body}\n\nKurallar: Aday soruyla yalnızca yüzeysel olarak ilgiliyse (aynı kelime, farklı konu) 'hicbiri' de. "
              f"'emin' yalnızca adayın kanıt metni sorunun ölçtüğü bilgiyi açıkça içeriyorsa kullanılır. "
              f"Kayıtlı cevap kanıtla çelişiyorsa anahtar_suphesi=true yap.\n"
              f"JSON: {{\"secim\": 1|2|3|\"hicbiri\", \"emin\": \"emin|orta|zayif\", "
              f"\"alinti\": \"seçilen adayın KANIT METNİ'nden birebir, en az 5 kelime\", "
              f"\"anahtar_suphesi\": false, \"gerekce\": \"tek cümle\"}}")
    d = llm(prompt)
    if d is None:
        return None
    sec = str(d.get("secim")).strip().lower()
    emin = str(d.get("emin") or "zayif").lower()
    extra = {"emin": emin, "anahtar_suphesi": bool(d.get("anahtar_suphesi"))}
    if sec in ("hicbiri", "hiçbiri", "none"):
        return {"karar": "hicbiri", "gerekce": d.get("gerekce"), **extra}
    try:
        i = int(sec)
        _, title, ev, obj = cands[i - 1]
    except (ValueError, IndexError):
        return {"karar": "reddedildi", "neden": f"geçersiz seçim: {sec}"}
    al = (d.get("alinti") or "").strip()
    if len(al.split()) < 5:
        return {"karar": "reddedildi", "neden": "alıntı çok kısa (başlık)", "secim": i, "alinti": al[:200], **extra}
    if not quote_ok(al, ev):
        return {"karar": "reddedildi", "neden": "alıntı adayın kanıtında yok", "secim": i, "alinti": al[:200], **extra}
    return {"karar": "kabul", "uygulanir": emin == "emin", **extra, "secim": i, "secilen": title, "alinti": al[:300], "gerekce": d.get("gerekce"),
            "degisti": i != 1,
            "hedef": ({"konu_id": obj.get("konu_id"), "konu": obj.get("konu"), "ders": obj.get("ders"), "kurul": obj.get("kurul"),
                       "kazanim_id": obj.get("kazanim_id")} if kind == "konu" else
                      {"source_id": obj.get("source_id"), "sayfa": obj.get("sayfa"), "chunk_id": obj.get("chunk_id")})}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=80)
    a = ap.parse_args()
    if not GROQ_KEYS and not (ENV.get("GEMINI_API_KEY") or ENV.get("GEMINI_FREE_KEY_2")):
        log("Groq/Gemini anahtarı yok; hakem kuyruğu atlandı")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "kararlar.jsonl"
    done = set()
    if path.exists():
        for r in P8.read_jsonl(path):
            if r.get("karar") in ("kabul", "hicbiri", "reddedildi", "soru_bozuk") and r.get("surum") == 2:
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
            if len(q["stem"].strip()) < 25 or len(q["options"]) < 2:
                st["soru_bozuk_atlandi"] += 1
                f.write(json.dumps({"anahtar": key, "tur": kind, "soru_id": r["soru_id"], "karar": "soru_bozuk", "surum": 2,
                                    "zaman": time.strftime("%Y-%m-%dT%H:%M:%S")}, ensure_ascii=False) + "\n")
                continue
            res = judge(kind, r, q)
            if res is None:
                st["yanit_yok"] += 1
                if st["yanit_yok"] >= 5 or len(_exhausted) == len(MODELS):
                    log("model art arda yanıt vermiyor; kalanlar sonraki tura")
                    break
                continue
            st[f"{kind}_{res['karar']}"] += 1
            f.write(json.dumps({"anahtar": key, "tur": kind, "soru_id": r["soru_id"], "surum": 2, "model": _last_model["ad"],
                                "zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), **res}, ensure_ascii=False) + "\n")
            f.flush()
            time.sleep(4)               # dakikalık token kotalarını aşmamak için tempo
    rep = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "bekleyen_slayt": len(sl), "bekleyen_konu": len(ko), **dict(st)}
    json.dump(rep, open(OUT / "rapor.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
