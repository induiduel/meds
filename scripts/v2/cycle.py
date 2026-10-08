"""Bağımsız orkestratör (M4) — yeni veriyi sırayla işler, kaldığı yerden devam eder.

Eski `scripts/agents/phase_cycle.py`'den bağımsızdır, onunla paylaşılan durum yoktur.
Kilit (süreçler arası), checkpoint (`CORE_DIR/_state/cycle.json`) ve adım günlüğü
(`CORE_DIR/_state/cycle.log`) kullanır. GPU kullanmaz (CPU + ücretsiz bulut).
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from . import config, pipeline
from .core import store

LOCK_NAME = "cycle.lock"
STATE_NAME = "cycle"
LOG_NAME = "cycle.log"


class _Logger:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def __call__(self, msg: str) -> None:
        line = f"{store.now_iso()}  {msg}"
        print(line, flush=True)
        try:
            with open(self.path, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except OSError:
            pass


def _pending_files(roots: list[str | Path]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        files.extend(pipeline._supported_files(Path(root)))
    return sorted(set(files))


def run_post_stages(*, dataset: str, answers_limit: int, log) -> dict:
    """Ingest sonrası: notlar → müfredat → kaynak bağı → tıbbi doğrulama → cevap → graf/küme → vektör → hub."""
    from . import export_site

    post: dict = {}
    steps = [
        ("notlar", lambda: pipeline.run_notes(log)),
        ("mufredat", lambda: pipeline.run_curriculum(dataset, log=log)),
        ("kaynak_bagi", lambda: pipeline.run_link(dataset, log=log)),
        ("temizlik", lambda: pipeline.run_cleanup(dataset, log=log)),
        ("tibbi_dogrulama", lambda: pipeline.run_verify(dataset, log=log)),
    ]
    if answers_limit > 0:
        steps.append(("cevaplar", lambda: pipeline.run_answers(dataset, limit=answers_limit, log=log)))
    steps += [
        ("kavram_grafi", lambda: pipeline.run_graph(dataset, log=log)),
        ("toplu_tamamlama", lambda: pipeline.run_cluster(dataset, log=log)),
        ("soru_disi_eleme", lambda: pipeline.run_purge(dataset, log=log)),
        ("yeniden_dogrulama", lambda: pipeline.run_revalidate(dataset, log=log)),
        ("vektor", lambda: pipeline.run_embed(log=log)),
    ]
    for name, fn in steps:
        try:
            post[name] = fn()
        except Exception as exc:  # noqa: BLE001
            log(f"{name} hatası: {exc}")
    try:
        export_site.export(log=log)
    except Exception as exc:  # noqa: BLE001
        log(f"export-site hatası: {exc}")
    return post


def run_once(roots: list[str | Path], *, dataset: str = "archive", limit: int | None = None,
             ocr: bool = False, dry_run: bool = False, post: bool = False,
             answers_limit: int = 0) -> dict:
    """Tek tur: bekleyen dosyaları işler; `post` ise müfredat/cevap/vektör/hub adımlarını koşar."""
    config.ensure_core_dirs()
    logger = _Logger(config.STATE_DIR / LOG_NAME)
    state = store.State(STATE_NAME)
    files = _pending_files(roots)
    pending = [f for f in files if not state.is_done(store.sha1_file(f))]
    if limit is not None:
        pending = pending[:limit]

    counts = {"toplam": len(files), "bekleyen": len(pending), "islenen": 0, "hata": 0, "kuru": dry_run}
    if dry_run:
        logger(f"KURU TUR: {len(pending)} dosya işlenecek (toplam {len(files)})")
        return counts

    with store.FileLock(config.STATE_DIR / LOCK_NAME, timeout=10):
        for f in pending:
            try:
                summary = pipeline.run_ingest(f, dataset=dataset, ocr=ocr, publish=True, log=lambda *_: None)
                state.mark_done(store.sha1_file(f))
                counts["islenen"] += 1
                added = (summary.get("soru_yayin") or {}).get("added", 0)
                logger(f"işlendi: {f.name} (soru+{added})")
            except Exception as exc:  # noqa: BLE001
                counts["hata"] += 1
                logger(f"HATA {f.name}: {exc}")
        if post:
            counts["post"] = run_post_stages(dataset=dataset, answers_limit=answers_limit, log=logger)
    logger(f"tur bitti: {counts}")
    return counts


def watch(roots: list[str | Path], *, interval: int, dataset: str = "archive", limit: int | None = None,
          ocr: bool = False, answers_limit: int = 0) -> None:
    logger = _Logger(config.STATE_DIR / LOG_NAME)
    logger(f"cycle --watch başladı (interval={interval}s, roots={roots}, answers_limit={answers_limit})")
    while True:
        try:
            run_once(roots, dataset=dataset, limit=limit, ocr=ocr, post=True, answers_limit=answers_limit)
        except Exception as exc:  # noqa: BLE001
            logger(f"tur hatası: {exc}")
        time.sleep(max(30, interval))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m v2 cycle", description="MedSoru Core v2 orkestratörü")
    ap.add_argument("--roots", nargs="+", default=[str(config.DOWNLOADS_DIR)])
    ap.add_argument("--interval", type=int, default=600)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--dataset", default="archive")
    ap.add_argument("--ocr", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--post", action="store_true", help="ingest sonrası müfredat/cevap/vektör/hub adımları")
    ap.add_argument("--answers-limit", type=int, default=0, help="tur başına tamamlanacak cevap sayısı")
    ap.add_argument("--watch", action="store_true", help="sürekli çalış (varsayılan: tek tur)")
    args = ap.parse_args(argv)
    if args.watch:
        watch(args.roots, interval=args.interval, dataset=args.dataset, limit=args.limit, ocr=args.ocr,
              answers_limit=args.answers_limit)
        return 0
    counts = run_once(args.roots, dataset=args.dataset, limit=args.limit, ocr=args.ocr,
                      dry_run=args.dry_run, post=args.post, answers_limit=args.answers_limit)
    print(f"cycle: {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
