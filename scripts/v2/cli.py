"""Komut satırı arayüzü: `python -m v2 <audit|ingest|status>`."""
from __future__ import annotations

import argparse

from . import audit, config, pipeline


def _cmd_status(_args) -> int:
    print("MedSoru Core v2 — durum")
    for key, val in config.describe().items():
        print(f"  {key:24} {val}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m v2", description="MedSoru Core v2 (bağımsız çekirdek)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("audit", help="Mevcut tüm veriyi denetle (salt okunur)")
    a.add_argument("--only", default="", help="virgülle ayrılmış küme adları")
    a.add_argument("--limit", type=int, default=None)

    i = sub.add_parser("ingest", help="Yeni veriyi oku/işle/yayınla")
    i.add_argument("target", help="dosya veya klasör")
    i.add_argument("--dataset", default="ingest")
    i.add_argument("--ders", default=None)
    i.add_argument("--konu", default=None)
    i.add_argument("--ocr", action="store_true", help="metin katmanı zayıfsa Tesseract OCR (CPU)")
    i.add_argument("--match", action="store_true", dest="match_existing", help="mevcut parçalarla eşleştir")
    i.add_argument("--enrich", action="store_true", help="ücretsiz bulut LLM ile zenginleştir")
    i.add_argument("--no-publish", action="store_true", help="yayınlamadan yalnız işle (deneme)")

    sub.add_parser("status", help="Yapılandırma/yol özeti")

    ia = sub.add_parser("ingest-all", help="Klasörleri/arşivi toplu işle (checkpoint ile)")
    ia.add_argument("roots", nargs="+", help="bir veya daha fazla klasör/dosya")
    ia.add_argument("--dataset", default="archive")
    ia.add_argument("--limit", type=int, default=None, help="en fazla N yeni dosya")
    ia.add_argument("--ocr", action="store_true")

    c = sub.add_parser("cycle", help="Bağımsız orkestratör (tek tur veya --watch)")
    c.add_argument("--roots", nargs="+", default=None)
    c.add_argument("--interval", type=int, default=600)
    c.add_argument("--limit", type=int, default=None)
    c.add_argument("--dataset", default="archive")
    c.add_argument("--ocr", action="store_true")
    c.add_argument("--dry-run", action="store_true")
    c.add_argument("--watch", action="store_true")
    c.add_argument("--post", action="store_true", help="ingest sonrası müfredat/cevap/vektör/hub adımları")
    c.add_argument("--answers-limit", type=int, default=0)

    es = sub.add_parser("export-site", help="v2 çıktısını site hub'ına bağla (ortak/veri)")
    es.add_argument("--dry-run", action="store_true")

    cu = sub.add_parser("curriculum", help="Soruları ders/konu/kazanım ile eşle")
    cu.add_argument("--dataset", default="archive")

    an = sub.add_parser("answers", help="Eksik cevaplı soruları kanıtlı LLM ile tamamla")
    an.add_argument("--dataset", default="archive")
    an.add_argument("--limit", type=int, default=40)
    an.add_argument("--include-faz14", action="store_true", help="Faz 14'ün incelediklerini de işle")

    em = sub.add_parser("embed", help="CORE parçalarını CPU e5 ile vektörleştir")
    em.add_argument("--force", action="store_true")

    sub.add_parser("notes", help="Ders notları + özetleri düzeltip CORE'a al")
    li = sub.add_parser("link", help="Soruları ders notu parçalarına bağla (kaynak sayfa + alıntı)")
    li.add_argument("--dataset", default="archive")
    ve = sub.add_parser("verify", help="Cevaplı soruların tıbbi doğruluğunu denetle (kanıt desteği)")
    ve.add_argument("--dataset", default="archive")
    gr = sub.add_parser("graph", help="Kavram grafı üret (ders/konu/kazanım/terim)")
    gr.add_argument("--dataset", default="archive")
    cl = sub.add_parser("cluster", help="Toplu soru tamamlama: parçaları kümele/birleştir")
    cl.add_argument("--dataset", default="archive")
    cp = sub.add_parser("cleanup", help="Kök/şık metinlerini temizle (mojibake vb.)")
    cp.add_argument("--dataset", default="archive")
    rv = sub.add_parser("revalidate", help="issues/status'u tazele (site filtreleri için)")
    rv.add_argument("--dataset", default="archive")
    st = sub.add_parser("study", help="Sözlük + çalışma kartları: prepare (denetim paketleri) / build (birleştir)")
    st.add_argument("adim", choices=["prepare", "build"])
    st.add_argument("--export", action="store_true", help="build: site verisini yedekleyerek güncelle")

    sub.add_parser("decks-k1", help="Kurul 1 ders paketlerini Öğren destelerine dönüştürür (yedekli)")
    nt = sub.add_parser("notes-k1", help="Kurul 1 ders notları: prepare (paketler) / build (denetim, --export)")
    nt.add_argument("adim", choices=["prepare", "build"])
    nt.add_argument("--export", action="store_true")

    os_ = sub.add_parser("ornek-k1", help="Kurul 1 örnek soruları: prepare (kitler) / build (denetim, --export)")
    os_.add_argument("adim", choices=["prepare", "build"])
    os_.add_argument("--ders", default=None)
    os_.add_argument("--export", action="store_true")

    pg = sub.add_parser("purge", help="Gerçek soru kökü olmayan kayıtları ele")
    pg.add_argument("--dataset", default="archive")

    args = parser.parse_args(argv)
    if args.cmd == "audit":
        only = {s.strip() for s in args.only.split(",") if s.strip()} or None
        audit.run(only=only, limit=args.limit, verbose=True)
        return 0
    if args.cmd == "ingest":
        summary = pipeline.run_ingest(
            args.target, dataset=args.dataset, ocr=args.ocr, match_existing=args.match_existing,
            enrich=args.enrich, ders=args.ders, konu=args.konu, publish=not args.no_publish,
        )
        pipeline.print_summary(summary)
        return 0
    if args.cmd == "status":
        return _cmd_status(args)
    if args.cmd == "ingest-all":
        counts = pipeline.run_ingest_all(args.roots, dataset=args.dataset, limit=args.limit, ocr=args.ocr)
        print(f"ingest-all: {counts}")
        return 0
    if args.cmd == "cycle":
        from . import cycle

        roots = args.roots or [str(config.DOWNLOADS_DIR)]
        if args.watch:
            cycle.watch(roots, interval=args.interval, dataset=args.dataset, limit=args.limit, ocr=args.ocr,
                        answers_limit=args.answers_limit)
            return 0
        counts = cycle.run_once(roots, dataset=args.dataset, limit=args.limit, ocr=args.ocr,
                                dry_run=args.dry_run, post=args.post, answers_limit=args.answers_limit)
        print(f"cycle: {counts}")
        return 0
    if args.cmd == "export-site":
        from . import export_site

        print(f"export-site: {export_site.export(dry_run=args.dry_run)}")
        return 0
    if args.cmd == "curriculum":
        print(f"curriculum: {pipeline.run_curriculum(args.dataset)}")
        return 0
    if args.cmd == "answers":
        print(f"answers: {pipeline.run_answers(args.dataset, limit=args.limit, skip_faz14=not args.include_faz14)}")
        return 0
    if args.cmd == "embed":
        print(f"embed: {pipeline.run_embed(force=args.force)}")
        return 0
    if args.cmd == "notes":
        print(f"notes: {pipeline.run_notes()}")
        return 0
    if args.cmd == "link":
        print(f"link: {pipeline.run_link(args.dataset)}")
        return 0
    if args.cmd == "notes-k1":
        from .stages import s14_notes
        if args.adim == "prepare":
            print(s14_notes.prepare())
        else:
            s14_notes.build(export=args.export)
        return 0
    if args.cmd == "ornek-k1":
        from .stages import s16_ornek_sorular
        if args.adim == "prepare":
            print(s16_ornek_sorular.prepare(ders=args.ders))
        else:
            s16_ornek_sorular.build(export=args.export)
        return 0
    if args.cmd == "decks-k1":
        from .stages import s15_k1_decks
        s15_k1_decks.run()
        return 0
    if args.cmd == "study":
        from .stages import s13_study
        if args.adim == "prepare":
            s13_study.prepare()
        else:
            s13_study.build(export=args.export)
        return 0
    if args.cmd == "verify":
        print(f"verify: {pipeline.run_verify(args.dataset)}")
        return 0
    if args.cmd == "graph":
        print(f"graph: {pipeline.run_graph(args.dataset)}")
        return 0
    if args.cmd == "cluster":
        print(f"cluster: {pipeline.run_cluster(args.dataset)}")
        return 0
    if args.cmd == "cleanup":
        print(f"cleanup: {pipeline.run_cleanup(args.dataset)}")
        return 0
    if args.cmd == "revalidate":
        print(f"revalidate: {pipeline.run_revalidate(args.dataset)}")
        return 0
    if args.cmd == "purge":
        print(f"purge: {pipeline.run_purge(args.dataset)}")
        return 0
    parser.error("bilinmeyen komut")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
