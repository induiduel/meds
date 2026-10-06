#!/usr/bin/env python3
"""
Kesin müfredat ataması: her site sorusu için kurul / ders / konu (resmî Dönem 3 ders programı) + kararın kaynağı.

Öncelik (en güvenilirden):
  1. sinav_basligi : sınav sistemi çıktısında (combinepdf) her sorunun üstünde yazan DERS + KONU başlığı → resmî konu.
                     Ders adı eşlenir (T. Patoloji → Tıbbi Patoloji …), konu adı programdaki o dersin konularıyla
                     kelime örtüşmesiyle eşleşir; kurul konudan gelir.
  2. faz8_yuksek   : Faz 8/9/10 birleşik çıktısında yüksek güven (+ hakem kararları).
  (Kaynak ders etiketi yolu denendi; denetimde ~%60 doğru çıktığı için kullanılmıyor.)
Örnek hata (2026-10-06): "Mide polipleri…" sorusu kayıtta Kurul 1 / Tıbbi Patoloji, Faz 8'de Kurul 3 / İç Hastalıkları /
Kolonun Prekanseröz Lezyonları; doğrusu Kurul 3 / Tıbbi Patoloji / Mide Tümörleri (sınav başlığında yazıyor).
Çıktı: $MEDS_DATABASE_DIR/derived/curriculum_links/soru_mufredat.json  {soru_id: {kurul, ders, konu, konu_id, kaynak, ...}}
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase8_curriculum_graph as P8  # noqa: E402
import resplit_exam_printout as RS  # noqa: E402

TEMP = Path(os.environ.get("MEDS_TEMP_DIR") or P8.PROJECT / "meds_temp")
OUT = P8.DB / "derived" / "curriculum_links" / "soru_mufredat.json"
DERS_MAP = {
    "t patoloji": "Tıbbi Patoloji", "tibbi patoloji": "Tıbbi Patoloji", "patoloji": "Tıbbi Patoloji",
    "t farmakoloji": "Tıbbi Farmakoloji", "tibbi farmakoloji": "Tıbbi Farmakoloji", "farmakoloji": "Tıbbi Farmakoloji",
    "t genetik": "Tıbbi Genetik", "tibbi genetik": "Tıbbi Genetik", "genetik": "Tıbbi Genetik",
    "ic hastaliklari": "İç Hastalıkları", "dahiliye": "İç Hastalıkları",
    "enfeksiyon": "Enfeksiyon Hastalıkları", "enfeksiyon hastaliklari": "Enfeksiyon Hastalıkları", "enfeksiyon hs": "Enfeksiyon Hastalıkları",
    "halk sagligi": "Halk Sağlığı", "cocuk sag ve hast": "Çocuk Sağlığı ve Hastalıkları",
    "cocuk sagligi ve hastaliklari": "Çocuk Sağlığı ve Hastalıkları", "ortopedi ve trav": "Ortopedi ve Travmatoloji",
    "ortopedi ve travmatoloji": "Ortopedi ve Travmatoloji", "anestezi": "Anesteziyoloji ve Reanimasyon",
    "anestezi ve reanimasyon": "Anesteziyoloji ve Reanimasyon", "beyin cerrahisi": "Beyin ve Sinir Cerrahisi",
    "kalp damar cerrahisi": "Kalp ve Damar Cerrahisi", "acil tip": "Acil Tıp", "aile hekimligi": "Aile Hekimliği",
    "ftr": "FTR", "fiziksel tip ve rehabilitasyon": "FTR", "kardiyoloji": "Kardiyoloji", "noroloji": "Nöroloji",
    "psikiyatri": "Psikiyatri", "uroloji": "Üroloji", "gogus hastaliklari": "Göğüs Hastalıkları",
    "gogus cerrahisi": "Göğüs Cerrahisi", "tibbi biyokimya": "Tıbbi Biyokimya", "biyokimya": "Tıbbi Biyokimya",
    "kadin hastaliklari ve dogum": "Kadın Hastalıkları ve Doğum",
}


def ders_norm(name: str) -> str | None:
    f = P8.fold(name or "")
    if f in DERS_MAP:
        return DERS_MAP[f]
    for k, v in DERS_MAP.items():
        if f.startswith(k) and len(k) >= 6:
            return v
    return None


def toks(s):
    return {w[:5] for w in P8.fold(s or "").split() if len(w) >= 3 and w not in P8.STOP}


def main():
    konular = [json.loads(l) for l in open(TEMP / "phase8" / "konular.jsonl", encoding="utf-8")]
    for k in konular:   # programda "Anestezi ve Reanimasyon" / "Anesteziyoloji…" iki yazım
        if k["ders"] == "Anestezi ve Reanimasyon":
            k["ders"] = "Anesteziyoloji ve Reanimasyon"
    by_ders = collections.defaultdict(list)
    for k in konular:
        by_ders[k["ders"]].append(k)

    def best_konu(ders: str, text: str, kurul: int | None = None, header: str = ""):
        cands = [k for k in by_ders.get(ders, []) if kurul is None or k["kurul"] == kurul]
        if not cands:
            return None, 0.0
        dt = toks(ders) | {"giris", "hasta", "tibbi"}            # ders adı/genel kelimeler konu ayırt etmez ("Patoloji")
        ht, qt = toks(header) - dt, toks(text) - dt
        best, bs = None, 0.0
        for k in cands:
            kt = toks(k["ad"] + " " + (k.get("mufredat_konusu") or "")) - dt
            if not kt:
                continue
            sc = (len(kt & ht) / len(kt)) * 2.0 if ht else 0.0      # başlık örtüşmesi (kesin bilgi)
            sc += len(kt & qt) / len(kt)                             # soru metni örtüşmesi
            if sc > bs:
                best, bs = k, sc
        return best, bs

    # 1) sınav çıktısı başlıkları: ders + konu + kök başı
    chunks = list(P8.read_jsonl(P8.DB / "chunks" / "c4259dc9087e.jsonl"))
    chunks.sort(key=lambda c: c.get("page") or 0)
    lines = [l for c in chunks for l in RS.lines_of(c.get("text") or "")]
    headers = []
    i = 0
    while i < len(lines) - 4:
        a, b = lines[i], lines[i + 1]
        d = ders_norm(a) if a and a == b else None
        if d:
            body = [x for x in lines[i + 2:i + 22] if x and not RS.HEADER.match(x)]
            qend = next((k for k, x in enumerate(body) if x.rstrip().endswith("?")), None)
            if qend is not None:
                blob = " ".join(body[:qend + 1])
                headers.append({"ders": d, "baslik_ve_kok": blob})
            i += 2
            continue
        i += 1
    hidx = collections.defaultdict(list)
    for h in headers:
        for w in toks(h["baslik_ve_kok"]):
            hidx[w].append(h)

    tree = {}
    clp = P8.DB / "derived" / "curriculum_links" / "soru_kazanim.jsonl"
    if clp.exists():
        for r in P8.read_jsonl(clp):
            k = (r.get("kazanimlar") or [{}])[0]
            if k.get("kurul"):
                tree[r["soru_id"]] = k
    pq = json.load(open(P8.ROOT / "data" / "pastQuestions.json", encoding="utf-8"))
    pq = pq if isinstance(pq, list) else pq.get("questions", [])
    out, st = {}, collections.Counter()
    for q in pq:
        qid = str(q.get("id"))
        stem = q.get("stem") or (q.get("reconstruction") or {}).get("stem") or ""
        opts = " ".join(o.get("text", "") for o in (q.get("options") or []) if isinstance(o, dict))
        text = stem + " " + opts
        rec = None
        # 1) sınav başlığı (yalnız sınav sistemi çıktısı kaynaklı sorular)
        if str(q.get("sourceFile")) == "c4259dc9087e" and len(stem) >= 20 and len(toks(stem)) >= 4:
            qt = toks(stem)
            cnt = collections.Counter(id(h) for w in qt for h in hidx.get(w, []))
            hmap = {id(h): h for w in qt for h in hidx.get(w, [])}
            for hid, c in cnt.most_common(3):
                h = hmap[hid]
                ht = toks(h["baslik_ve_kok"])
                if len(qt & ht) / max(1, len(qt)) >= 0.7:
                    k, sc = best_konu(h["ders"], text, header=h["baslik_ve_kok"])
                    if k and sc >= 1.0:
                        rec = {"kurul": k["kurul"], "ders": k["ders"], "konu": k["ad"], "konu_id": k["konu_id"], "kaynak": "sinav_basligi"}
                    break
        # 2) kaynak dersi yolu kaldırıldı: elle denetimde ~%60 (bazı kaynakların ders etiketi yanlış) < Faz 8 yüksek
        # 3) Faz 8 yüksek / hakem
        if rec is None and qid in tree:
            t = tree[qid]
            rec = {"kurul": int(t["kurul"]), "ders": t.get("ders"), "konu": t.get("konu"), "konu_id": t.get("konu_id"),
                   "kazanim": t.get("kazanim"), "kaynak": "faz8_yuksek"}
        if rec:
            if qid in tree and tree[qid].get("konu_id") == rec.get("konu_id"):
                rec["kazanim"] = tree[qid].get("kazanim")
            out[qid] = rec
            st[rec["kaynak"]] += 1
    if not out:
        print("atama yok; önceki dosya korunuyor")
        return 1
    tmp = OUT.with_suffix(".tmp")
    json.dump({"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "sorular": out}, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(tmp, OUT)
    print(json.dumps({"soru": len(pq), "atanan": len(out), **dict(st), "sinav_basligi_sayisi": len(headers)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
