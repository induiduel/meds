"""Revize v2 — komut satırı: run | report | vectorize."""
from __future__ import annotations

import argparse
import json
import time

from ..core import store
from . import config


def _report() -> dict:
    recs = list(store.iter_jsonl(config.QUESTIONS_OUT))
    revize = [r for r in recs if r.get("durum") == "revize"]
    karantina = [r for r in recs if r.get("durum") == "karantina"]
    destek = [r.get("support_ratio", 0.0) for r in recs]
    yapili = [r for r in recs if r.get("soru_koku") and 4 <= len(r.get("secenekler") or {}) <= 5]
    cevapli = [r for r in recs if r.get("dogru_secenek")]
    report = {
        "revize": config.REVIZE_TAG,
        "toplam": len(recs),
        "revize_edilen": len(revize),
        "karantina": len(karantina),
        "yapisal_gecerli_orani": round(len(yapili) / len(recs), 4) if recs else 0.0,
        "cevapli_orani": round(len(cevapli) / len(recs), 4) if recs else 0.0,
        "ortalama_destek": round(sum(destek) / len(destek), 4) if destek else 0.0,
        "degisiklik_kaydi": len(list(store.iter_jsonl(config.CHANGES_OUT))),
    }
    config.REPORT_OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    return report


def _vectorize(log=print) -> dict:
    recs = [r for r in store.iter_jsonl(config.QUESTIONS_OUT) if r.get("soru_koku")]
    if not recs:
        return {"vektor": 0, "yazildi": False}
    from semantic import embeddings  # type: ignore

    import numpy as np

    vecs = embeddings.embed_passages([r["soru_koku"] for r in recs])
    config.ensure_dirs()
    np.save(config.VECTORS / "e5.npy", np.asarray(vecs, dtype="float32"))
    store.write_jsonl(config.VECTORS / "e5_ids.jsonl",
                      [{"id": r.get("id"), "revize": config.REVIZE_TAG} for r in recs], guard=False)
    store.atomic_write_json(config.VECTORS / "manifest.json",
                            {"model": "multilingual-e5-small", "sayi": len(recs),
                             "boyut": int(np.asarray(vecs).shape[1]), "zaman": store.now_iso()})
    log(f"vektörleştirme: {len(recs)} soru")
    return {"vektor": len(recs), "yazildi": True}


def _watch(limit: int, interval: int, log=print) -> None:
    from . import engine

    log(f"revize v2 --watch (limit={limit}, interval={interval}s)")
    while True:
        try:
            counts = engine.run(limit, log=log)
        except Exception as exc:  # noqa: BLE001
            log(f"tur hatası: {exc}")
            counts = {}
        if counts.get("api_basarisiz"):
            log("revize v2: API çalışmıyor — izleme durduruldu.")
            return
        time.sleep(max(30, interval))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m v2.revize", description="Revize v2")
    sub = ap.add_subparsers(dest="cmd", required=True)
    rn = sub.add_parser("run", help="Faz 14 sorularını revize et")
    rn.add_argument("--limit", type=int, default=20)
    rn.add_argument("--watch", action="store_true", help="sürekli çalış")
    rn.add_argument("--interval", type=int, default=120)
    sub.add_parser("report", help="Özet + ölçüm")
    sub.add_parser("vectorize", help="Revize soruları vektörle")
    args = ap.parse_args(argv)

    from . import engine

    if args.cmd == "run":
        if args.watch:
            _watch(args.limit, args.interval)
            return 0
        print(json.dumps(engine.run(args.limit), ensure_ascii=False))
        return 0
    if args.cmd == "report":
        print(json.dumps(_report(), ensure_ascii=False, indent=1))
        return 0
    if args.cmd == "vectorize":
        print(json.dumps(_vectorize(), ensure_ascii=False))
        return 0
    return 2
