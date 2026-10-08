"""M5 — Site entegrasyonu: v2 çıktısını paylaşımlı hub'a (meds_database/ortak/veri) bağlar.

Yaptıkları (yalnız `meds_database/ortak/` altına yazar; kaynak veri kümelerine dokunmaz):
  1. En son denetim raporunun özetini `ortak/veri/v2_denetim.json` (+ CORE `reports/audit_latest.json`) yazar.
  2. CORE içeriğinden `ortak/veri/v2_katalog.json` üretir (kayıt sayılarıyla).
  3. Kırık/bayat hub symlink'lerini onarır: eski `Masaüstü/MedSoru Project` yolu → güncel `PROJECT_ROOT`.
  4. v2 veri kümeleri için hub symlink'leri oluşturur (hedef varsa).

Site bu dosyaları `/api/v2/audit` ve `/api/v2/katalog` uçlarından da okuyabilir.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from . import config
from .core import store

OLD_PREFIX = "/home/indu/Masaüstü/MedSoru Project"
HUB = ("ortak", "veri")


def _hub_dir() -> Path:
    return config.DATABASE_DIR.joinpath(*HUB)


def _count_lines(paths) -> int:
    n = 0
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                n += sum(1 for line in fh if line.strip())
        except OSError:
            continue
    return n


def _latest_audit() -> dict | None:
    reports = sorted(config.REPORTS_DIR.glob("audit_*.json"))
    reports = [r for r in reports if r.name != "audit_latest.json"]
    return store.read_json(reports[-1]) if reports else None


def _audit_summary(report: dict) -> dict:
    return {
        "zaman": report.get("zaman"),
        "toplam": report.get("toplam"),
        "inceleme_kuyrugu": report.get("inceleme_kuyrugu"),
        "kaynaklar": {
            k: {"kayit": v.get("kayit"), "blocking": v.get("blocking"), "review": v.get("review")}
            for k, v in (report.get("kaynaklar") or {}).items()
        },
    }


def _v2_katalog() -> dict:
    kumeler = [
        {"ad": "v2_sorular", "yol": str(config.QUESTIONS_DIR), "tur": "jsonl_dizin",
         "aciklama": "Core v2 doğrulanmış/yayınlanmış sorular", "guvenilirlik": "aday",
         "kayit": _count_lines(config.QUESTIONS_DIR.glob("*.jsonl")) if config.QUESTIONS_DIR.exists() else 0},
        {"ad": "v2_ders_parcalari", "yol": str(config.CHUNKS_DIR), "tur": "jsonl_dizin",
         "aciklama": "Core v2 ders parçaları", "guvenilirlik": "kaynak",
         "kayit": _count_lines(config.CHUNKS_DIR.glob("*.jsonl")) if config.CHUNKS_DIR.exists() else 0},
        {"ad": "v2_ders_kaynaklari", "yol": str(config.SOURCES_DIR), "tur": "json_dizin",
         "aciklama": "Core v2 ders kaynakları", "guvenilirlik": "kaynak",
         "kayit": len(list(config.SOURCES_DIR.glob("*.json"))) if config.SOURCES_DIR.exists() else 0},
    ]
    return {"zaman": store.now_iso(), "uretici": config.PIPELINE_GENERATION, "veri_kumeleri": kumeler}


def repair_hub_links(dry_run: bool = False, log=print) -> dict:
    """Kırık/bayat symlink'leri onarır ve v2 hub bağlarını kurar. Var olan sağlam bağlara dokunmaz."""
    hub = _hub_dir()
    if not hub.exists():
        return {"duzeltilen": 0, "olusturulan": 0, "hub": str(hub), "uyari": "hub yok"}
    fixed = created = 0

    # 1) Eski yola işaret eden kırık bağları güncel yola çevir
    for link in sorted(hub.iterdir()):
        if not link.is_symlink():
            continue
        target = os.readlink(link)
        if target.startswith(OLD_PREFIX):
            new_target = target.replace(OLD_PREFIX, str(config.PROJECT_ROOT), 1)
            if Path(new_target).exists():
                if dry_run:
                    log(f"(kuru) onarılacak: {link.name} -> {new_target}")
                else:
                    link.unlink()
                    link.symlink_to(new_target)
                    log(f"onarıldı: {link.name} -> {new_target}")
                fixed += 1

    # 2) v2 veri kümeleri için hub bağları (hedef varsa, yoksa oluştur)
    for name, target in (("v2_sorular_veritabani", config.QUESTIONS_DIR),
                         ("v2_ders_parcalari", config.CHUNKS_DIR),
                         ("v2_ders_kaynaklari", config.SOURCES_DIR)):
        link = hub / name
        if not target.exists() or link.exists():
            continue
        if dry_run:
            log(f"(kuru) oluşturulacak: {name} -> {target}")
        else:
            link.symlink_to(target)
            log(f"oluşturuldu: {name} -> {target}")
        created += 1
    return {"duzeltilen": fixed, "olusturulan": created, "hub": str(hub)}


def export(dry_run: bool = False, log=print) -> dict:
    config.ensure_core_dirs()
    out: dict = {"hub": str(_hub_dir()), "yazilanlar": [], "kuru": dry_run}

    report = _latest_audit()
    if report is None:
        log("denetim raporu yok; önce `python -m v2 audit` çalıştırın.")
    else:
        ozet = _audit_summary(report)
        targets = {
            config.REPORTS_DIR / "audit_latest.json": ozet,
            _hub_dir() / "v2_denetim.json": ozet,
            _hub_dir() / "v2_katalog.json": _v2_katalog(),
        }
        for path, payload in targets.items():
            if dry_run:
                log(f"(kuru) yazılacak: {path}")
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            store.atomic_write_json(path, payload)
            out["yazilanlar"].append(str(path))
            log(f"yazıldı: {path}")
        out["toplam_kayit"] = (report.get("toplam") or {}).get("kayit")

    out["linkler"] = repair_hub_links(dry_run=dry_run, log=log)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m v2 export-site", description="v2 çıktısını site hub'ına bağla")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    print(f"export-site: {export(dry_run=args.dry_run)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
