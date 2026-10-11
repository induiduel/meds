#!/usr/bin/env python3
"""Veritabanı analiz araçları — SALT OKUNUR. Hiçbir kaydı değiştirmez, silmez, birleştirmez.

Silme/birleştirme kararı insan onayıyla, ayrı bir adımda verilir. Bu araçlar yalnız rapor üretir ve her kararı
ders kaynaklarına (RAG: ders slaytı, özet, deste, sözlük, hastalık parçaları) dayanan kanıtla destekler.

Alt komutlar:
  ozet   tablo boyutları/satır sayıları + JSON (data/pastQuestions.json) ↔ DB (past_questions) eşlik farkı
  kopya  çıkmış sorularda birebir ve yakın kopyalar (MinHash LSH + rapidfuzz doğrulama); cevabı çelişen kopyalar işaretlenir
  kanit  verilen soru kimlikleri (ya da son kopya raporu) için ders kaynağı kanıtı (bge-m3 vektör araması, yalnız müfredat türleri)

Hedef: --hedef yerel (bu bilgisayardaki supabase-db) | oracle (docker --context oracle). Parola gerekmez (docker exec psql).
Rapor: $MEDS_TEMP_DIR/db_analiz/<zaman>/*.json  (repo dışı)

Örnek:
  .venv-ocr/bin/python scripts/db_analiz/analiz.py ozet --hedef oracle
  .venv-ocr/bin/python scripts/db_analiz/analiz.py kopya --esik 0.9
  .venv-ocr/bin/python scripts/db_analiz/analiz.py kanit --son-kopya-raporu --limit 50
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(APP / "scripts" / "agents"))
from lib import fold  # noqa: E402  (Türkçe katlama; tüm boru hattıyla aynı)

TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or APP.parent / "meds_temp")
OUT_ROOT = TEMP / "db_analiz"
EMBED_URL = os.environ.get("MEDS_EMBED_BGE_URL", "http://127.0.0.1:8094/embed")
# Kanıt yalnız müfredat malzemesinden: AI çıktısı ve soru dökümleri kanıt değildir (CLAUDE.md "Grounding").
KANIT_TURLERI = ["lecture_slide", "summary", "deck_slide", "glossary_term", "disease"]


def psql(sql: str, hedef: str) -> str:
    cmd = ["docker"] + (["--context", "oracle"] if hedef == "oracle" else []) + \
          ["exec", "-i", "supabase-db", "psql", "-U", "postgres", "-At", "-v", "ON_ERROR_STOP=1", "-c", sql]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise SystemExit(f"psql hatası ({hedef}): {r.stderr.strip()[:400]}")
    return r.stdout.strip()


def out_dir() -> Path:
    d = OUT_ROOT / time.strftime("%Y%m%d_%H%M%S")
    d.mkdir(parents=True, exist_ok=True)
    return d


def soru_metni(q: dict) -> tuple[str, list[str], str]:
    rec = q.get("reconstruction") if isinstance(q.get("reconstruction"), dict) else {}
    stem = (rec.get("stem") or q.get("stem") or "").strip()
    opts = rec.get("options") or q.get("options") or []
    texts = [str(o.get("text", "")).strip() for o in opts if isinstance(o, dict)]
    ans = str(rec.get("correctAnswer") or q.get("correctAnswer") or q.get("claimedAnswer") or "").strip().upper()[:1]
    return stem, texts, ans


# ------------------------------------------------------------------ ozet
def ozet(a):
    # n_live_tup istatistiği bayat olabilir; kesin sayım (query_to_xml ile tablo başına count(*))
    rows = psql("select coalesce(json_agg(t),'[]') from (select relname as tablo, "
                "(xpath('/row/c/text()', query_to_xml(format('select count(*) as c from public.%I', relname), false, true, '')))[1]::text::bigint as satir, "
                "pg_size_pretty(pg_total_relation_size(relid)) as boyut, pg_total_relation_size(relid) as bayt "
                "from pg_stat_user_tables where schemaname='public' order by bayt desc) t", a.hedef)
    tablolar = json.loads(rows)
    db_ids = set(filter(None, psql("select id from past_questions", a.hedef).split("\n")))
    js = json.load(open(APP / "data" / "pastQuestions.json", encoding="utf-8"))
    js_ids = {q["id"] for q in js}
    rapor = {
        "hedef": a.hedef,
        "tablolar": tablolar,
        "esitlik_pastQuestions": {
            "json": len(js_ids), "db": len(db_ids),
            "yalniz_json": len(js_ids - db_ids), "yalniz_db": len(db_ids - js_ids),
            "ornek_yalniz_json": sorted(js_ids - db_ids)[:20], "ornek_yalniz_db": sorted(db_ids - js_ids)[:20],
        },
    }
    d = out_dir()
    (d / "ozet.json").write_text(json.dumps(rapor, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[ozet] {a.hedef}: {len(tablolar)} tablo · past_questions JSON {len(js_ids)} / DB {len(db_ids)} "
          f"(yalnız JSON {len(js_ids - db_ids)}, yalnız DB {len(db_ids - js_ids)}) → {d / 'ozet.json'}")
    for t in tablolar[:10]:
        print(f"   {t['tablo']:<28} {t['satir']:>8} satır  {t['boyut']}")


# ------------------------------------------------------------------ kopya
def kopya(a):
    from datasketch import MinHash, MinHashLSH
    from rapidfuzz import fuzz

    qs = json.load(open(APP / "data" / "pastQuestions.json", encoding="utf-8"))
    norm, meta = {}, {}
    for q in qs:
        stem, opts, ans = soru_metni(q)
        t = fold(stem + " " + " ".join(sorted(opts)))
        if len(t.split()) < 4:
            continue
        norm[q["id"]] = t
        meta[q["id"]] = {"cevap": ans, "kurul": q.get("committeeId"), "yil": q.get("examYear"),
                         "ders": q.get("discipline"), "kok": stem[:160]}

    birebir: dict[str, list[str]] = {}
    for i, t in norm.items():
        birebir.setdefault(hashlib.sha1(t.encode()).hexdigest(), []).append(i)
    birebir_gruplar = [g for g in birebir.values() if len(g) > 1]

    lsh = MinHashLSH(threshold=a.esik * 0.85, num_perm=128)
    mh = {}
    for i, t in norm.items():
        w = t.split()
        m = MinHash(num_perm=128)
        for k in range(max(1, len(w) - 2)):
            m.update(" ".join(w[k:k + 3]).encode())
        mh[i] = m
        lsh.insert(i, m)
    gorulen, ciftler = set(), []
    for i in norm:
        for j in lsh.query(mh[i]):
            if j <= i or (i, j) in gorulen:
                continue
            gorulen.add((i, j))
            s = fuzz.token_set_ratio(norm[i], norm[j]) / 100
            if s >= a.esik and norm[i] != norm[j]:
                ciftler.append({"a": i, "b": j, "benzerlik": round(s, 3),
                                "cevap_celiskisi": bool(meta[i]["cevap"] and meta[j]["cevap"] and meta[i]["cevap"] != meta[j]["cevap"]),
                                "a_meta": meta[i], "b_meta": meta[j]})
    ciftler.sort(key=lambda c: (-c["cevap_celiskisi"], -c["benzerlik"]))
    d = out_dir()
    rapor = {"esik": a.esik, "incelenen": len(norm), "birebir_gruplar": [[{"id": x, **meta[x]} for x in g] for g in birebir_gruplar],
             "yakin_ciftler": ciftler}
    (d / "kopyalar.json").write_text(json.dumps(rapor, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[kopya] {len(norm)} soru · birebir grup {len(birebir_gruplar)} "
          f"({sum(len(g) for g in birebir_gruplar)} kayıt) · yakın çift {len(ciftler)} "
          f"(cevap çelişkili {sum(c['cevap_celiskisi'] for c in ciftler)}) → {d / 'kopyalar.json'}")


# ------------------------------------------------------------------ kanit
def embed(texts: list[str]) -> list[list[float]]:
    req = urllib.request.Request(EMBED_URL, json.dumps({"texts": texts, "kind": "query"}).encode(),
                                 {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=300))["vectors"]


def kanit(a):
    qs = {q["id"]: q for q in json.load(open(APP / "data" / "pastQuestions.json", encoding="utf-8"))}
    ids: list[str] = list(a.ids or [])
    if a.son_kopya_raporu:
        son = sorted(OUT_ROOT.glob("*/kopyalar.json"))
        if not son:
            raise SystemExit("Önce 'kopya' çalıştır.")
        r = json.load(open(son[-1], encoding="utf-8"))
        for c in r["yakin_ciftler"]:
            ids += [c["a"], c["b"]]
        for g in r["birebir_gruplar"]:
            ids += [x["id"] for x in g]
    ids = [i for i in dict.fromkeys(ids) if i in qs][: a.limit]
    if not ids:
        raise SystemExit("Kanıt aranacak soru yok.")
    tur = "{" + ",".join(KANIT_TURLERI) + "}"
    sonuc = {}
    for k in range(0, len(ids), 16):
        part = ids[k:k + 16]
        vecs = embed([soru_metni(qs[i])[0][:1500] for i in part])
        for i, v in zip(part, vecs):
            lit = "[" + ",".join(f"{x:.6f}" for x in v) + "]"
            js = psql("select coalesce(json_agg(t),'[]') from (select document_type, title, page_number, committee_id, "
                      "discipline, round(similarity::numeric,3) as benzerlik, left(content,240) as alinti "
                      f"from match_rag_chunks_bge_m3('{lit}'::vector, {a.kac}, '{tur}'::text[], "
                      f"{repr(qs[i].get('committeeId')) if a.kurul_filtresi and qs[i].get('committeeId') else 'NULL'})) t",
                      a.hedef)
            sonuc[i] = {"kok": soru_metni(qs[i])[0][:200], "kaynaklar": json.loads(js)}
    d = out_dir()
    (d / "kanit.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    zayif = sum(1 for v in sonuc.values() if not v["kaynaklar"] or v["kaynaklar"][0]["benzerlik"] < 0.5)
    print(f"[kanit] {len(sonuc)} soru · ders kaynağı zayıf (<0.50) {zayif} → {d / 'kanit.json'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hedef", choices=["yerel", "oracle"], default="yerel")
    sub = ap.add_subparsers(dest="komut", required=True)
    sub.add_parser("ozet")
    k = sub.add_parser("kopya")
    k.add_argument("--esik", type=float, default=0.92, help="rapidfuzz token_set benzerlik eşiği (0-1)")
    e = sub.add_parser("kanit")
    e.add_argument("--ids", nargs="*")
    e.add_argument("--son-kopya-raporu", action="store_true")
    e.add_argument("--limit", type=int, default=100)
    e.add_argument("--kac", type=int, default=3, help="soru başına kaynak sayısı")
    e.add_argument("--kurul-filtresi", action="store_true", help="kaynakları sorunun kuruluyla sınırla")
    for p in sub.choices.values():
        p.add_argument("--hedef", choices=["yerel", "oracle"], default=argparse.SUPPRESS)
    a = ap.parse_args()
    {"ozet": ozet, "kopya": kopya, "kanit": kanit}[a.komut](a)


if __name__ == "__main__":
    main()
