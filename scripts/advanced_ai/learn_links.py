#!/usr/bin/env python3
"""
Öğren bağlantıları — her çıkmış soru için doğru Öğren destesi slaytını önceden hesaplar.

Sorun: istemcideki learnMatcher, 3 ortak anahtar kelimeyle "en yüksek puanlı" slaytı seçiyordu; genel kelimesi bol
giriş/özet slaytları birçok soruyu topluyordu (sabit/varsayılan yönlendirme gibi görünüyordu).
Yöntem (Faz 11 ile aynı, elle denetimde ~%82–89):
  aday = Öğren destelerindeki slaytlar (başlık + alt başlık + içerik + spot bilgiler + bilgi kartları)
  BM25 + kavram belirteçleri (Faz 10) ∪ multilingual-e5-small → RRF ilk 25 → mMiniLM cross-encoder
  sorgu = soru kökü (+ doğrulanmış/güvenilir cevap metni); ders uyumu (Faz 8/10 güvenilir ders ↔ deste disiplini) bonus
  Eşik altında BAĞLANTI VERİLMEZ (yanlış slayta göndermek yerine "Öğren" düğmesi görünmez).
Çıktı: $MEDS_DATABASE_DIR/derived/learn_links.json  {soru_id: {deckId, deckTitle, slideNumber, slideTitle, skor, guven}}
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
import phase11_question_slide as F11  # noqa: E402

ROOT = P8.ROOT
OUT = P8.DB / "derived" / "learn_links.json"
MIN_CE = float(os.environ.get("MEDS_LEARN_MIN_CE", "2.0"))


def slide_text(d, s) -> str:
    parts = [d.get("title") or "", s.get("title") or "", s.get("subtitle") or "", s.get("badge") or ""]
    for k in ("spotPearls", "spots"):
        v = s.get(k) or []
        parts += [x if isinstance(x, str) else f"{x.get('badge', '')} {x.get('text', '')}" for x in v]
    cc = s.get("coreContent") or {}
    if isinstance(cc, dict):
        for b in cc.get("keyBullets") or []:
            parts.append(f"{b.get('title', '')} {b.get('desc', '')}" if isinstance(b, dict) else str(b))
    parts.append((s.get("content") or s.get("synthesisNarrative") or "")[:1500])
    for fc in s.get("flashcards") or []:
        if isinstance(fc, dict):
            parts.append(f"{fc.get('front', '')} {fc.get('back', '')}")
    return re.sub(r"[#*_>`]+", " ", " ".join(p for p in parts if p))


def main():
    import numpy as np
    from sentence_transformers import CrossEncoder, SentenceTransformer
    t0 = time.time()
    rep = {}
    F11.load_concepts(rep)
    decks = [json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(str(ROOT / "src" / "data" / "decks" / "items" / "*.json")))]
    slides = []
    for d in decks:
        for s in d.get("slides") or []:
            slides.append({"deckId": d.get("id") or d.get("deckId"), "deckTitle": d.get("shortTitle") or d.get("title"),
                           "disiplin": P8.fold(d.get("discipline") or ""), "slideNumber": int(str(s.get("slideNumber") or 1)),
                           "slideTitle": s.get("title") or "", "text": slide_text(d, s)})
    log = lambda m: print(f"[{time.strftime('%H:%M:%S')}] [ogren] {m}", flush=True)  # noqa: E731
    log(f"{len(decks)} deste, {len(slides)} slayt")
    bm = P8.BM25([P8.stems(s["text"]) for s in slides], b=0.6)
    device = F11.pick_device()          # MEDS_FAZ11_DEVICE=auto (zincir GPU'yu boşalttıysa) → cuda
    log(f"cihaz: {device}")
    emb_model = SentenceTransformer(F11.EMB_MODEL, device=device)
    emb = emb_model.encode(["passage: " + s["text"][:1200] for s in slides], batch_size=64, normalize_embeddings=True,
                           show_progress_bar=False, convert_to_numpy=True).astype("float32")
    ce = CrossEncoder(F11.CE_MODEL, device=device, max_length=384)
    # sorular: sitenin çıkmış soru arşivi (kimlikler sitedekiyle aynı)
    pq = json.load(open(ROOT / "data" / "pastQuestions.json", encoding="utf-8"))
    pq = pq if isinstance(pq, list) else pq.get("questions", [])
    tree, _ = F11.load_tree()
    out, st = {}, collections.Counter()
    stems_v = []
    rows = []
    for q in pq:
        stem = q.get("stem") or (q.get("reconstruction") or {}).get("stem") or ""
        if len(stem) < 20:
            continue
        opts = q.get("options") or []
        ans = ""
        if str(q.get("sourceFile")) != "c4259dc9087e":           # öğrenci cevabı kaynağında cevap kullanılmaz
            ans = next((o.get("text", "") for o in opts if isinstance(o, dict) and o.get("key") == q.get("correctAnswer")), "")
        rows.append((q, stem, ans))
    qv = emb_model.encode(["query: " + (s + " " + a)[:600] for _, s, a in rows], batch_size=64, normalize_embeddings=True,
                          show_progress_bar=False, convert_to_numpy=True).astype("float32")
    for n, ((q, stem, ans), v) in enumerate(zip(rows, qv)):
        if n and n % 500 == 0:
            log(f"  {n}/{len(rows)}")
        qc = collections.Counter()
        for w in P8.stems(stem):
            qc[w] += 2.0
        for w in P8.stems(ans):
            qc[w] += 2.5
        ranks = {}
        bs = bm.scores(qc)
        for r, i in enumerate(sorted(bs, key=bs.get, reverse=True)[:25]):
            ranks.setdefault(i, []).append(r)
        sims = emb @ v
        top = np.argpartition(-sims, 25)[:25]
        for r, i in enumerate(top[np.argsort(-sims[top])]):
            ranks.setdefault(int(i), []).append(r)
        cand = sorted(ranks, key=lambda i: sum(1 / (60 + r) for r in ranks[i]), reverse=True)[:12]
        query = (stem + (" Cevap: " + ans if ans else ""))[:500]
        scores = ce.predict([(query, slides[i]["text"][:900]) for i in cand], batch_size=32, show_progress_bar=False)
        t = tree.get(str(q.get("id"))) or {}
        ders = P8.fold(t.get("ders") or "") if t.get("guvenilir") else ""
        best = None
        for i, c in zip(cand, scores):
            bonus = 0.8 if ders and any(w in slides[i]["disiplin"] for w in ders.split() if len(w) >= 5) else 0.0
            sc = float(c) + bonus
            if best is None or sc > best[0]:
                best = (sc, float(c), i)
        if best and best[1] >= MIN_CE:
            s = slides[best[2]]
            out[str(q["id"])] = {"deckId": s["deckId"], "deckTitle": s["deckTitle"], "slideNumber": s["slideNumber"],
                                 "slideTitle": s["slideTitle"], "skor": round(best[0], 2),
                                 "guven": "yuksek" if best[1] >= 5 else "orta"}
            st["baglandi"] += 1
        else:
            st["baglanti_yok"] += 1
    if not out:
        log("bağlantı üretilemedi; önceki dosya korunuyor")
        return 1
    tmp = OUT.with_suffix(".tmp")
    json.dump({"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "esik_ce": MIN_CE, "baglantilar": out}, open(tmp, "w", encoding="utf-8"),
              ensure_ascii=False)
    os.replace(tmp, OUT)
    dist = collections.Counter((v["deckTitle"], v["slideNumber"]) for v in out.values())
    print(json.dumps({"soru": len(rows), **dict(st), "en_cok_baglanan_slayt": dist.most_common(5),
                      "sure_sn": round(time.time() - t0)}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
