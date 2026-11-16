"""Ingest orkestratörü: s1 → s2 → s3 → s4 → (s5) → (s6) → (s7).

Tek çağrıda bir dosya/klasörü işler. Varsayılan olarak yalnız CPU deterministik adımlar çalışır
(match/enrich isteğe bağlı). Yayın idempotenttir: aynı girdi ikinci kez işlenince kopya üretmez.
"""
from __future__ import annotations

from pathlib import Path

from . import config
from .core import cluster, embed, graph, store
from .stages import (s1_extract, s2_normalize, s3_validate, s4_dedupe, s5_match, s6_enrich, s7_publish,
                     s8_curriculum, s9_answer, s10_notes, s11_link, s12_verify)


def run_ingest(target: str | Path, *, dataset: str = "ingest", ocr: bool = False,
               match_existing: bool = False, enrich: bool = False, ders: str | None = None,
               konu: str | None = None, publish: bool = True, near_threshold: float = 0.9,
               log=print) -> dict:
    summary: dict = {"hedef": str(target), "dataset": dataset}

    docs = s1_extract.extract_path(target, ocr=ocr)
    summary["belge"] = len(docs)
    if not docs:
        log(f"belge bulunamadı: {target}")
        return summary

    sources: list[dict] = []
    questions: list[dict] = []
    chunks: list[dict] = []
    for doc in docs:
        sources.append(doc["source"])
        questions.extend(s2_normalize.build_questions(doc, ders=ders, konu=konu))
        chunks.extend(s2_normalize.build_chunks(doc, ders=ders, konu=konu))
    summary["ham_soru"] = len(questions)
    summary["parca"] = len(chunks)

    dd = s4_dedupe.dedupe_records(questions, near_threshold=near_threshold)
    unique = dd.unique
    summary["tekil"] = len(unique)
    summary["tekrar"] = dd.duplicate_count

    by_chunk = {c["chunk_id"]: c["text"] for c in chunks}
    index = None
    if match_existing or chunks:
        index = s5_match.build_index(chunks if chunks else s5_match.load_existing_chunks())
        summary["eslesme"] = s5_match.match_records(unique, index)

    # Doğrulama eşleştirmeden SONRA: kanıt (evidence) eklenmiş hâliyle değerlendirilir.
    summary["dogrulama"] = s3_validate.validate_records(unique)

    if enrich and index is not None:
        summary["zenginlestirme"] = s6_enrich.enrich_records(unique, by_chunk=by_chunk, log=log)

    if publish:
        summary["kaynak_yayin"] = s7_publish.publish_sources(sources)
        summary["parca_yayin"] = s7_publish.publish_chunks(chunks)
        summary["soru_yayin"] = s7_publish.publish_questions(unique, dataset)
        s7_publish.update_katalog(
            summary["soru_yayin"].get("total", 0),
            summary["parca_yayin"].get("eklenen", 0) + len(chunks),
            summary["kaynak_yayin"].get("yazilan", 0),
            dataset,
        )
    return summary


def _supported_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    if root.is_dir():
        return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in s1_extract.SUPPORTED)
    return []


def load_core_questions(dataset: str = "archive") -> list[dict]:
    return store.read_jsonl(config.QUESTIONS_DIR / f"{dataset}.jsonl")


def load_core_chunks() -> list[dict]:
    return embed.load_all_chunks()


def run_curriculum(dataset: str = "archive", log=print) -> dict:
    """CORE sorularına müfredat/kazanım eşlemesi uygular ve geri yayınlar."""
    records = load_core_questions(dataset)
    if not records:
        return {"kayit": 0}
    # Kaynakların ders/kurul bilgisiyle boş alanları doldur (isabeti artırır).
    src: dict[str, dict] = {}
    if config.SOURCES_DIR.exists():
        for p in config.SOURCES_DIR.glob("*.json"):
            s = store.read_json(p, {})
            if s.get("source_id"):
                src[s["source_id"]] = s
    filled = 0
    for rec in records:
        s = src.get(rec.get("source_id"))
        if not s:
            continue
        if not rec.get("ders") and s.get("ders"):
            rec["ders"] = s["ders"]
            filled += 1
        if rec.get("kurul") is None and s.get("kurul") is not None:
            rec["kurul"] = s["kurul"]
    counts = s8_curriculum.apply_curriculum(records)
    counts["kaynaktan_ders"] = filled
    s7_publish.publish_questions(records, dataset, preserve=False)
    log(f"müfredat: {counts}")
    return counts


def run_answers(dataset: str = "archive", limit: int = s9_answer.DEFAULT_LIMIT,
                skip_faz14: bool = True, log=print) -> dict:
    """Eksik cevaplı (ve Faz 14'ün incelemediği) soruları kanıtlı LLM ile tamamlar."""
    records = load_core_questions(dataset)
    if not records:
        return {"kayit": 0}
    by_chunk = {c["chunk_id"]: c.get("text") or "" for c in load_core_chunks()}
    state = store.State("answer_tried")
    tried = set(state.data.get("tamamlanan", []))
    counts = s9_answer.fill_answers(records, by_chunk=by_chunk, limit=limit,
                                    skip_faz14=skip_faz14, skip_ids=tried, log=log)
    tried.update(x for x in counts.pop("_denenen_idler", []) if x)
    state.data["tamamlanan"] = sorted(tried)
    state.save()
    s7_publish.publish_questions(records, dataset)
    log(f"cevap tamamlama: {counts}")
    return counts


def run_embed(force: bool = False, log=print) -> dict:
    """CORE parçalarını CPU e5 ile vektörleştirir (değişmediyse atlar)."""
    chunks = load_core_chunks()
    if not chunks:
        return {"vektor": 0, "yazildi": False, "neden": "parça yok"}
    man = embed.manifest()
    if not force and man.get("sayi") == len(chunks) and (config.VECTORS_DIR / "e5.npy").exists():
        log("vektörler güncel; atlandı")
        return {"vektor": man.get("sayi", 0), "yazildi": False, "neden": "güncel"}
    result = embed.build(chunks, log=log)
    log(f"vektörleştirme: {result}")
    return result


def run_notes(log=print) -> dict:
    """Ders notları ve özetlerini düzeltip CORE'a alır."""
    return {"notlar": s10_notes.ingest_notes(log), "ozetler": s10_notes.ingest_summaries(log)}


def run_link(dataset: str = "archive", log=print) -> dict:
    """Soruları ders notu parçalarına bağlar (kaynak sayfa + alıntı) ve geri yayınlar."""
    records = load_core_questions(dataset)
    if not records:
        return {"kayit": 0}
    chunks = load_core_chunks()
    by_id = {c["chunk_id"]: c for c in chunks}
    counts = s11_link.link_questions(records, None, chunks_by_id=by_id)
    s7_publish.publish_questions(records, dataset)
    log(f"kaynak ilişkilendirme: {counts}")
    return counts


def run_verify(dataset: str = "archive", log=print) -> dict:
    """Cevaplı soruların tıbbi doğruluğunu kanıt desteğiyle denetler."""
    records = load_core_questions(dataset)
    if not records:
        return {"kayit": 0}
    by_chunk = {c["chunk_id"]: c.get("text") or "" for c in load_core_chunks()}
    counts = s12_verify.verify_records(records, by_chunk=by_chunk)
    s7_publish.publish_questions(records, dataset)
    log(f"tıbbi doğrulama: {counts}")
    return counts


def run_cleanup(dataset: str = "archive", log=print) -> dict:
    """Kök/açıklama/şık metinlerini temizler (mojibake, ligatür, kontrol karakteri). Kimlik korunur."""
    from .core import textnorm

    records = load_core_questions(dataset)
    fixed = 0
    for rec in records:
        changed = False
        for field in ("stem", "explanation"):
            val = rec.get(field)
            if isinstance(val, str):
                new = textnorm.clean_text(val)
                if new != val:
                    rec[field] = new
                    changed = True
        opts = rec.get("options")
        if isinstance(opts, dict):
            for k, v in list(opts.items()):
                if isinstance(v, str):
                    new = textnorm.clean_text(v)
                    if new != v:
                        opts[k] = new
                        changed = True
        if changed:
            fixed += 1
    if fixed:
        s7_publish.publish_questions(records, dataset)
    log(f"veri temizliği: {fixed} kayıt düzeltildi")
    return {"kayit": len(records), "duzeltilen": fixed}


def run_revalidate(dataset: str = "archive", log=print) -> dict:
    """Zenginleştirme sonrası issues/status'u tazeler (site filtreleri doğru olsun)."""
    records = load_core_questions(dataset)
    if not records:
        return {"kayit": 0}
    counts = s3_validate.validate_records(records)
    s7_publish.publish_questions(records, dataset)
    log(f"yeniden doğrulama: {counts}")
    return counts


def run_purge(dataset: str = "archive", log=print) -> dict:
    """Gerçek soru kökü taşımayan kayıtları (başlık/şık/ders içeriği) CORE'dan çıkarır."""
    from .core import quality

    records = load_core_questions(dataset)
    if not records:
        return {"once": 0, "kalan": 0, "elenen": 0}
    kept = [r for r in records if quality.is_question_stem(r.get("stem") or "")]
    removed = len(records) - len(kept)
    if removed:
        store.write_core_jsonl(config.QUESTIONS_DIR / f"{dataset}.jsonl", kept, guard=True)
    log(f"soru dışı eleme: {removed} kayıt çıkarıldı, {len(kept)} kaldı")
    return {"once": len(records), "kalan": len(kept), "elenen": removed}


def run_graph(dataset: str = "archive", log=print) -> dict:
    """Sorulardan kavram grafı üretir (ders/konu/kazanım/terim)."""
    records = load_core_questions(dataset)
    g = graph.build(records)
    store.write_core_json(config.DERIVED_DIR / "kavram_grafi.json", g)
    info = graph.summary(g)
    log(f"kavram grafı: {info}")
    return info


def run_cluster(dataset: str = "archive", log=print) -> dict:
    """Aynı soruya ait parçaları kümeleyip birleştirir (toplu soru tamamlama)."""
    records = load_core_questions(dataset)
    res = cluster.cluster_and_merge(records)
    store.write_core_jsonl(config.DERIVED_DIR / "birlesik_sorular.jsonl",
                           [{"birlesik": m} for m in res.merged], guard=False)
    info = {"grup": len(res.groups), "birlesik": len(res.merged)}
    log(f"toplu tamamlama: {info}")
    return info


def run_ingest_all(roots: list[str | Path], *, dataset: str = "archive", limit: int | None = None,
                   ocr: bool = False, log=print) -> dict:
    """Tüm arşivi/klasörleri işler; işlenen dosyaları checkpoint ile atlar (kaldığı yerden devam).
    Yayın idempotent olduğundan aynı soru farklı dosyalarda tekrar gelse kopya üretilmez."""
    config.ensure_core_dirs()
    state = store.State("ingest_all")
    files: list[Path] = []
    for root in roots:
        files.extend(_supported_files(Path(root)))
    files = sorted(set(files))

    counts = {"dosya": len(files), "islenen": 0, "atlanan": 0, "hata": 0}
    for f in files:
        key = store.sha1_file(f)
        if state.is_done(key):
            counts["atlanan"] += 1
            continue
        if limit is not None and counts["islenen"] >= limit:
            break
        try:
            summary = run_ingest(f, dataset=dataset, ocr=ocr, publish=True, log=lambda *_: None)
            state.mark_done(key)
            counts["islenen"] += 1
            added = (summary.get("soru_yayin") or {}).get("added", 0)
            log(f"[{counts['islenen']}] {f.name}: soru+{added}")
        except Exception as exc:  # noqa: BLE001
            counts["hata"] += 1
            log(f"HATA {f}: {exc}")
    return counts


def print_summary(s: dict) -> None:
    print(f"hedef        : {s.get('hedef')}")
    print(f"belge        : {s.get('belge')}  ham_soru={s.get('ham_soru')}  parça={s.get('parca')}")
    if "dogrulama" in s:
        d = s["dogrulama"]
        print(f"doğrulama    : kayıt={d['kayit']} blocking={d['blocking']} review={d['review']} ok={d['ok']}")
    print(f"tekil        : {s.get('tekil')}  (tekrar elenen: {s.get('tekrar')})")
    if "eslesme" in s:
        print(f"eşleşme      : {s['eslesme']}")
    if "zenginlestirme" in s:
        print(f"zenginleştir.: {s['zenginlestirme']}")
    if "soru_yayin" in s:
        print(f"yayın        : soru={s['soru_yayin']}  parça={s.get('parca_yayin')}  kaynak={s.get('kaynak_yayin')}")
    print(f"çıktı dizini : {config.CORE_DIR}")
