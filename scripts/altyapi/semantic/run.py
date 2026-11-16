"""Komut satırı: build | eval | classify | info."""
from __future__ import annotations

import argparse
import json


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m semantic", description="Semantik Veri Modeli")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build", help="Bilgi tabanı + FAISS indeksini üret")
    ev = sub.add_parser("eval", help="1000 soruda başarıyı ölç")
    ev.add_argument("--n", type=int, default=1000)
    ev.add_argument("--seed", type=int, default=42)
    cl = sub.add_parser("classify", help="Tek soruyu analiz et")
    cl.add_argument("soru")
    sub.add_parser("info", help="Durum")
    args = ap.parse_args(argv)

    if args.cmd == "build":
        from . import build
        return build.main()
    if args.cmd == "eval":
        from . import evaluate
        print(json.dumps(evaluate.evaluate(args.n, args.seed), ensure_ascii=False, indent=1))
        return 0
    if args.cmd == "classify":
        from . import pipeline
        eng = pipeline.Engine()
        print(json.dumps(eng.classify(args.soru), ensure_ascii=False, indent=1))
        return 0
    if args.cmd == "info":
        from . import config
        ok = config.INDEX_PATH.exists()
        print(json.dumps({"cek_index": ok, "bolum": str(config.OUT)}, ensure_ascii=False))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
