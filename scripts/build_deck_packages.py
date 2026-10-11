#!/usr/bin/env python3
"""Öğren destelerinin dışa aktarım paketlerini TEK kaynaktan üretir.

Kaynak: src/data/interactive_learning_decks.json (tek doğruluk kaynağı; items/ derlemede üretilir).
Çıktı:  $MEDS_DECK_PACKAGES_DIR (varsayılan <proje>/meds_export/deste_paketleri)/<deste-id>/
          deck.json            destenin birebir kopyası
          deck.md              başlık, künye, özet, yüksek verimli bilgiler ve slayt anlatımları (NotebookLM/okuma)
          flashcards_anki.txt  ön<TAB>arka (Anki içe aktarma)
          manifest.json        sayımlar + deck.json SHA256 + üretim zamanı

Paketler uygulama tarafından OKUNMAZ; elle düzenlenmez, her zaman bu betikle yeniden üretilir.
Üretim önce geçici klasöre yapılır, sonra eski klasörle yer değiştirir (yarım paket kalmaz).
Kullanım: python3 scripts/build_deck_packages.py [--out DİZİN]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
import time
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
SRC = APP / "src" / "data" / "interactive_learning_decks.json"
DEFAULT_OUT = Path(os.environ.get("MEDS_DECK_PACKAGES_DIR") or APP.parent / "meds_export" / "deste_paketleri")


def first(d: dict, *keys: str) -> str:
    for k in keys:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def deck_markdown(deck: dict) -> str:
    out = [f"# {deck.get('title', deck['id'])}", ""]
    meta = [
        ("Eğitmen", first(deck, "instructor", "lecturer")),
        ("Bölüm", first(deck, "discipline", "department")),
        ("Kurul", first(deck, "committee")),
    ]
    meta_line = " · ".join(f"**{k}:** {v}" for k, v in meta if v)
    if meta_line:
        out += [meta_line, ""]
    summary = first(deck, "overview", "description", "summary", "subtitle")
    if summary:
        out += [summary, ""]
    pearls = deck.get("highYieldPearls") or []
    if pearls:
        out += ["## Yüksek Verimli Bilgiler", ""]
        out += [f"- {p if isinstance(p, str) else first(p, 'text', 'content', 'pearl')}" for p in pearls]
        out.append("")
    out += ["## Slaytlar", ""]
    for i, s in enumerate(deck.get("slides") or [], 1):
        out += [f"### Slayt {s.get('slideNumber', i)}: {s.get('title', '').strip()}", ""]
        body = first(s, "synthesisNarrative", "content")
        if body:
            out += [body, ""]
    return "\n".join(out).rstrip() + "\n"


def flashcards_tsv(deck: dict) -> str:
    rows = []
    for c in deck.get("flashcards") or []:
        front, back = first(c, "front", "question"), first(c, "back", "answer")
        if front and back:
            rows.append(f"{' '.join(front.split())}\t{' '.join(back.split())}")
    return "\n".join(rows) + ("\n" if rows else "")


def write_package(root: Path, deck: dict) -> dict:
    d = root / deck["id"]
    d.mkdir(parents=True)
    raw = json.dumps(deck, ensure_ascii=False, indent=2)
    (d / "deck.json").write_text(raw, encoding="utf-8")
    (d / "deck.md").write_text(deck_markdown(deck), encoding="utf-8")
    cards = flashcards_tsv(deck)
    (d / "flashcards_anki.txt").write_text(cards, encoding="utf-8")
    slides = deck.get("slides") or []
    manifest = {
        "id": deck["id"],
        "title": deck.get("title"),
        "slaytlar": len(slides),
        "etkilesimler": sum(len(s.get("interactiveElements") or []) for s in slides),
        "kartlar": cards.count("\n"),
        "deck_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "kaynak": "src/data/interactive_learning_decks.json",
    }
    (d / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    a = ap.parse_args()
    data = json.loads(SRC.read_text(encoding="utf-8"))
    decks = data if isinstance(data, list) else data["decks"]
    ids = [d["id"] for d in decks]
    if len(ids) != len(set(ids)):
        raise SystemExit("HATA: kaynakta tekrarlanan deste kimliği var")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix=".paketler_", dir=a.out.parent))
    manifests = [write_package(tmp, d) for d in decks]
    (tmp / "INDEX.json").write_text(json.dumps({
        "uretim": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "deste": len(manifests),
        "paketler": manifests,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    old = a.out.with_name(a.out.name + ".eski")
    if a.out.exists():
        a.out.rename(old)
    tmp.rename(a.out)
    shutil.rmtree(old, ignore_errors=True)
    print(f"[paketler] {len(manifests)} deste → {a.out}  "
          f"(slayt {sum(m['slaytlar'] for m in manifests)}, kart {sum(m['kartlar'] for m in manifests)})")


if __name__ == "__main__":
    main()
