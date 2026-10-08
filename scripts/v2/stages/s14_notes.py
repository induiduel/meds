"""s14 — Kurul ders notlarının yeniden yazımı (editör eliyle, kaynak sadakati ölçülerek).

  prepare → `meds_temp/study/k1/` altına her program dersi için çalışma paketi (`NN_slug.src.txt`):
            program bilgisi (ders, konu, öğretim üyesi, tarih), kaynak PDF'in sayfa sayfa metni ve
            bu derse atanan doğrulanmış çıkmış soru kartları.
  build   → editörün yazdığı `NN_slug.md` notlarını denetler (biçim + kaynak sadakati) ve `--export`
            ile site verisine yazar (yalnız Kurul 1; diğer kurullara dokunmaz, önce yedek alır).

Kaynak sadakati: notun içerik köklerinin kaynak metinde geçme oranı (`sadakat`). Çıkmış soru blokları
hesaba katılmaz. `SADAKAT_ESIK` altı notlar dışa aktarılmaz, inceleme listesine düşer.
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path

from .. import config
from ..core import ids, store, textnorm
from ..core.lectures import LectureCorpus, stems

KURUL = 1
WORK = config.TEMP_DIR / "study" / "k1"
SITE = config.MEDS_DIR / "src" / "data"
SUMMARY_JSON = SITE / "summaries" / f"kurul{KURUL}.json"
META_JSON = SITE / "summaries_meta.json"
ENRICH_JSON = SITE / "summaries_enrichment.json"
CATALOG_JSONS = [config.MEDS_DIR / "data" / "lectureSummariesCatalog.json", SITE / "lectureSummariesCatalog.json"]
QUESTION_CARDS = SITE / "question_cards.json"
SADAKAT_ESIK = 0.80

# Program dersi → kaynak (meds_database/sources kimlikleri). "gecen_yil": bu yılın PDF'i yok, geçen yılınki.
# Program: meds_database/taxonomy/donem3_ders_programi.json (2026-27, Kurul 1, TIP 310).
LESSONS = [
    ("Tıbbi Genetik", "Dismorfolojide Genetik Terminoloji", "Dr. Öğr. Üyesi Serap Arslan", "2026-09-14", ["01de5beebe01"], False),
    ("Tıbbi Patoloji", "Patolojiye Giriş", "Prof. Dr. Hikmet Keleş", "2026-09-14", ["36a5ff0eb59f"], False),
    ("Tıbbi Patoloji", "Hücresel Adaptasyonlar", "Prof. Dr. Hikmet Keleş", "2026-09-14", ["d1e7dc70bc99"], False),
    ("Tıbbi Patoloji", "Hücre Hasarı ve Nekroz - I", "Prof. Dr. Hikmet Keleş", "2026-09-15", ["d5afafc5125b"], False),
    ("Tıbbi Patoloji", "Hücre Hasarı ve Nekroz - II", "Prof. Dr. Hikmet Keleş", "2026-09-15", ["a89e122541a6"], False),
    ("Halk Sağlığı", "Gebelik ve Emzirme Döneminde Beslenme", "Doç. Dr. Nergiz Sevinç", "2026-09-15", ["f9753e10135b"], True),
    ("Tıbbi Patoloji", "Hücre İçi Birikimler ve Kalsifikasyonlar", "Prof. Dr. Hikmet Keleş", "2026-09-16", ["5b06467a44e0"], False),
    ("Tıbbi Patoloji", "Hücresel Yaşlanma", "Prof. Dr. Hikmet Keleş", "", ["2291452989db"], False),
    ("Tıbbi Patoloji", "Akut Enflamasyon: Vasküler Değişiklikler ve Hücresel Olaylar", "Prof. Dr. Hikmet Keleş", "2026-09-16", ["5dac471a7d0b"], False),
    ("Tıbbi Genetik", "Kromozomal Hastalıklar ve Genetik Danışma", "Dr. Öğr. Üyesi Serap Arslan", "2026-09-16", ["390e7f9700ff"], False),
    ("Üroloji", "Üriner Obstrüksiyonun Fizyopatolojisi", "Doç. Dr. Özer Baran", "2026-09-17", ["217a9b946cbf"], False),
    ("Tıbbi Patoloji", "Enflamasyonun Kimyasal Mediyatörleri", "Prof. Dr. Hikmet Keleş", "2026-09-17", ["429b6132cbff"], False),
    ("Tıbbi Patoloji", "Kronik ve Granülomatöz Enflamasyon", "Prof. Dr. Hikmet Keleş", "2026-09-18", ["f47bbb243a50"], False),
    ("Halk Sağlığı", "Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri", "Halk Sağlığı ABD", "2026-09-18", ["6d4b0e257dac"], False),
    ("Tıbbi Patoloji", "Doku Onarımı ve Yara İyileşmesi", "Prof. Dr. Hikmet Keleş", "2026-09-21", ["0ff4c9748dfa"], False),
    ("Tıbbi Patoloji", "Ödem, Hiperemi, Konjesyon ve Kanama", "Prof. Dr. Hikmet Keleş", "2026-09-21", ["177f77bc3030"], False),
    ("Enfeksiyon Hastalıkları", "Cinsel Yolla Bulaşan Enfeksiyonlarda Tedavi", "Dr. Öğr. Üyesi Rüveyda Korkmazer", "2026-09-21", ["af6faf4d791e"], False),
    ("Halk Sağlığı", "Halk Sağlığı Tarihçesi", "Doç. Dr. Nergiz Sevinç", "2026-09-22", ["71576d109ae6"], False),
    ("Tıbbi Genetik", "Doğumsal Kadın/Erkek Genital Gelişim Anomalileri", "Dr. Öğr. Üyesi Serap Arslan", "2026-09-22", ["8825392d5db7"], False),
    ("Tıbbi Patoloji", "Tromboz Patofizyolojisi", "Prof. Dr. Hikmet Keleş", "2026-09-23", ["ff3391d54d30"], False),
    ("Enfeksiyon Hastalıkları", "Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler", "Uz. Dr. Merve Kaçar", "2026-09-23", ["225bce5ed1d8"], False),
    ("Halk Sağlığı", "Bebek Beslenmesi", "Doç. Dr. Nergiz Sevinç", "2026-09-23", ["ece69f6db6bb"], False),
    ("Halk Sağlığı", "Ana-Çocuk Sağlığı Düzeyinin İzlenmesi", "Doç. Dr. Nergiz Sevinç", "2026-09-24", ["26b03da1600b"], False),
    ("Tıbbi Patoloji", "Emboli, Enfarktüs ve Şok", "Prof. Dr. Hikmet Keleş", "", ["66074c027e38"], False),
    ("Tıbbi Patoloji", "Aşırı Duyarlılık ve Otoimmünite", "Prof. Dr. Hikmet Keleş", "2026-09-24", ["04d25f1910ad"], False),
    ("Tıbbi Patoloji", "Genetik, Pediatrik ve Çevresel Patoloji", "Prof. Dr. Hikmet Keleş", "2026-09-25", ["773f5b07ef0c"], False),
    ("Üroloji", "Üriner Sistem Taş Hastalıkları Fizyopatolojisi", "Dr. Öğr. Üyesi Fahrettin Şamil Uysal", "2026-09-25", ["6c2130e67f02"], False),
    ("Tıbbi Patoloji", "Tümör Biyolojisi ve Terminolojisi", "Prof. Dr. Hikmet Keleş", "2026-09-28", ["e3e6efd625e9"], False),
    ("Tıbbi Patoloji", "Karsinojenezin Moleküler Temeli", "Prof. Dr. Hikmet Keleş", "", ["d19be08adaff"], False),
    ("Tıbbi Patoloji", "İleri Tümör Genetiği ve Metabolizması", "Prof. Dr. Hikmet Keleş", "", ["0a30463c4da6"], False),
    ("Tıbbi Genetik", "Ürogenital Sistem Tümörlerinde Genetik Belirteçler ve Kliniğe Yansımaları", "Dr. Öğr. Üyesi Serap Arslan", "2026-09-28", ["104ba40842c6"], False),
    ("Tıbbi Patoloji", "Tümör İmmünolojisi ve Metastaz Mekanizmaları", "Prof. Dr. Hikmet Keleş", "2026-09-29", ["7dca6565c28d"], False),
    ("Tıbbi Patoloji", "Tümör Evrelemesi, Derecelendirme ve Laboratuvar Tanısı", "Prof. Dr. Hikmet Keleş", "", ["a4ad1a106ce1"], False),
    ("Enfeksiyon Hastalıkları", "Genital Enfeksiyonlar", "Dr. Öğr. Üyesi Rüveyda Korkmazer", "2026-09-29", ["279ff9356d0d"], False),
    ("Tıbbi Genetik", "Prenatal Tanı Yöntemleri", "Dr. Öğr. Üyesi Serap Arslan", "2026-09-30", ["ba4731af443f"], False),
    ("Enfeksiyon Hastalıkları", "İzolasyon Yöntemleri", "Enfeksiyon Hastalıkları ABD", "2026-09-30", ["efafa5729c82"], False),
    ("Tıbbi Patoloji", "Glomerüler Hastalıklar: Nefrotik Sendrom", "Prof. Dr. Hikmet Keleş", "2026-10-01", ["2a458550e470"], False),
    ("Tıbbi Patoloji", "Glomerüler Hastalıklar: Nefritik Sendrom", "Prof. Dr. Hikmet Keleş", "2026-10-01", ["700440515761"], False),
    ("Üroloji", "Üriner Sistem Enfeksiyonlarının Epidemiyoloji, Etiyoloji ve Semptomatolojisi", "Üroloji ABD", "2026-10-01", ["6fd043ae190b"], False),
    ("Enfeksiyon Hastalıkları", "Cinsel Yolla Bulaşan Hastalıklarda Profilaksi ve Korunma", "Enfeksiyon Hastalıkları ABD", "2026-10-02", ["ceea5af1bf7f"], True),
    ("Tıbbi Patoloji", "Sistemik Hastalıklarda Böbrek Hasarı", "Prof. Dr. Hikmet Keleş", "2026-10-02", ["c3d05d6f1e7c"], False),
    ("Tıbbi Patoloji", "Tübülointerstisyel Hastalıklar", "Prof. Dr. Hikmet Keleş", "2026-10-05", ["99778f3fc5a9"], False),
    ("Üroloji", "Üriner Sistemin Spesifik Enfeksiyonları", "Dr. Öğr. Üyesi Salih Bürlükkara", "2026-10-05", ["fcd692bfe62d"], False),
    ("Tıbbi Patoloji", "Vasküler ve Kistik Böbrek Hastalıkları", "Prof. Dr. Hikmet Keleş", "2026-10-05", ["de1c485d0870"], False),
    ("Tıbbi Patoloji", "Böbrek Tümörleri", "Prof. Dr. Hikmet Keleş", "2026-10-06", ["6d76c8217dc6"], False),
    ("Tıbbi Patoloji", "Mesane Hastalıkları ve Tümörleri", "Prof. Dr. Hikmet Keleş", "2026-10-06", ["43f8f9f2e770"], False),
    ("Enfeksiyon Hastalıkları", "Bağışıklığı Baskılı Hastalarda Enfeksiyon", "Uz. Dr. Merve Kaçar", "2026-10-06", ["914640ba44a8"], True),
    ("Tıbbi Patoloji", "Vulva, Vajen ve Serviks Hastalıkları", "Prof. Dr. Hikmet Keleş", "2026-10-07", ["e12889578ddc"], False),
    ("Tıbbi Patoloji", "İnvaziv Serviks Kanseri ve Endometriyozis", "Prof. Dr. Hikmet Keleş", "2026-10-07", ["9d9f2e6b1b78"], False),
    ("Enfeksiyon Hastalıkları", "Sifilis", "Dr. Öğr. Üyesi Rüveyda Korkmazer", "2026-10-07", ["a06e81a804e8"], True),
    ("Üroloji", "Üriner Sistem Enfeksiyonları: Laboratuvar Bulguları ve Tedavi", "Doç. Dr. Özer Baran", "2026-10-08", ["8d871e0a1162"], False),
    ("Enfeksiyon Hastalıkları", "Üriner Sistem Enfeksiyonları", "Dr. Öğr. Üyesi Rüveyda Korkmazer", "2026-10-08", ["b044475371ad"], False),
    ("Tıbbi Patoloji", "Endometriyal Hiperplazi ve Kanserleri", "Prof. Dr. Hikmet Keleş", "2026-10-09", ["9f9a7e7be738"], True),
    ("Tıbbi Patoloji", "Uterus Düz Kas ve Trofoblastik Tümörleri", "Prof. Dr. Hikmet Keleş", "2026-10-09", ["9f9a7e7be738", "0bd268420825", "f10fd12c752b"], True),
    ("Tıbbi Patoloji", "Over Tümörleri", "Prof. Dr. Hikmet Keleş", "2026-10-12", ["6ca162c5baf1"], True),
    ("Tıbbi Patoloji", "Memenin Benign Hastalıkları", "Prof. Dr. Hikmet Keleş", "2026-10-12", ["d513b3a9103f"], True),
    ("Enfeksiyon Hastalıkları", "İntrauterin Enfeksiyonlar", "Dr. Öğr. Üyesi Rüveyda Korkmazer", "2026-10-13", ["f94540227341"], True),
    ("Üroloji", "Enürezis Nokturna", "Dr. Öğr. Üyesi Salih Bürlükkara", "2026-10-13", ["52d6e0296bb0"], True),
    ("Tıbbi Farmakoloji", "İmmünofarmakoloji", "Prof. Dr. Mehmet Özdemir", "2026-10-14", ["98b79a509e23"], True),
    ("Tıbbi Genetik", "Preimplantasyon Genetik Tanı (PGT)", "Dr. Öğr. Üyesi Serap Arslan", "2026-10-14", ["e436327a50bf"], True),
    ("Kadın Hastalıkları ve Doğum", "Abortus", "Dr. Öğr. Üyesi Hilal Ezgi Türkmen", "2026-10-15", ["90f59c77b176"], True),
    ("Enfeksiyon Hastalıkları", "Üretral Akıntı", "Uz. Dr. Merve Kaçar", "2026-10-15", ["d6b6b53bbcea"], True),
    ("Halk Sağlığı", "Türkiye'de Sağlık Hizmetleri", "Dr. Öğr. Üyesi Erkay Nacar", "2026-10-16", ["cc24d55eaa51"], True),
    ("Kadın Hastalıkları ve Doğum", "Gebelik Terminolojisi ve Kavramları", "Dr. Öğr. Üyesi Hilal Ezgi Türkmen", "2026-10-16", ["58992bb60e6f"], True),
    ("Tıbbi Patoloji", "Meme Kanseri ve Moleküler Tipleri", "Prof. Dr. Hikmet Keleş", "2026-10-19", ["2767141b0310"], True),
    ("Tıbbi Patoloji", "Erkek Genital Sistem ve Prostat Hastalıkları", "Prof. Dr. Hikmet Keleş", "2026-10-19", ["1cf9f0c9ef38", "307f6b24a5d4", "934cb3dbf174"], True),
]
# Programda olup hiçbir yılda kaynak PDF'i bulunamayanlar (uydurulmaz): Koruyucu Sağlık Hizmetleri,
# Mikroorganizmalarda Direnç Sorunu ve Antimikrobiyal Yönetim.


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", ids.fold_tr(text)).strip("_")[:50]


def lesson_id(n: int, konu: str) -> str:
    return f"k{KURUL}-{n:02d}-{_slug(konu).replace('_', '-')}"


_WORDISH = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşü]{3,}")


def _readable(line: str) -> bool:
    """OCR görsel/tablo artığı satırları eler: kelime oranı düşük veya sembol yoğun satırlar."""
    t = line.strip()
    if not t:
        return False
    words = _WORDISH.findall(t)
    if not words:
        return bool(re.search(r"\d", t)) and len(t) <= 40
    tokens = t.split()
    return len(words) / max(1, len(tokens)) >= 0.5 and sum(ch in "|:;{}[]@#~" for ch in t) <= max(3, len(t) // 15)


def _pages(corpus: LectureCorpus, source_ids: list[str]) -> list[tuple[str, int, str]]:
    out, seen = [], set()
    for sid in source_ids:
        rows = sorted((c for c in corpus.chunks if c["source_id"] == sid), key=lambda c: (c["sayfa"] or 0, c["chunk_id"]))
        for c in rows:
            text = re.sub(r"^\[Komite[^\]]*\]\s*", "", c["text"]).strip()
            lines = [ln for ln in text.split("\n") if _readable(ln) and ids.norm_key(ln) not in seen]
            seen.update(ids.norm_key(ln) for ln in lines if len(ln) > 25)
            if lines:
                out.append((sid, c["sayfa"], "\n".join(lines)))
    return out


_K1_EXAM = re.compile(r"Dönem 3 Çıkmışlar Kurul 1/(?!Dönem 2)|3\. Sınıf/Kurul 1|cikmislar_k1_6_final/kurul 1/|dönem 3 kurul 1", re.I)


def _exam_pool() -> list[dict]:
    """Dönem 3 Kurul 1 sınav dosyalarından gelen tekil sorular (Dönem 2 dökümleri hariç)."""
    from .s13_study import _clean, _strip_leak
    pool, seen = [], set()
    for q in store.iter_jsonl(config.QUESTIONS_DIR / "archive.jsonl"):
        path = (q.get("provenance") or {}).get("kaynak_dosya") or ""
        if not _K1_EXAM.search(path):
            continue
        stem = _clean(q.get("stem"))
        opts = {k: _strip_leak(v) for k, v in sorted((q.get("options") or {}).items())}
        key = ids.norm_key(stem)
        if len(stem) < 15 or key in seen:
            continue
        seen.add(key)
        ans = (q.get("answer") or "").strip().upper()
        pool.append({"id": q["question_id"], "front": stem, "options": opts,
                     "answer": ans if ans in opts else "", "dosya": Path(path).name})
    return pool


def _assign_questions(corpus: LectureCorpus) -> dict[int, list[dict]]:
    """Her Kurul 1 sınav sorusunu en iyi eşleşen tek derse atar (BM25 + kök desteği + marj)."""
    pos: dict[str, list[int]] = {}
    for i, c in enumerate(corpus.chunks):
        pos.setdefault(c["source_id"], []).append(i)
    lesson_chunks = {n: [i for sid in L[4] for i in pos.get(sid, [])] for n, L in enumerate(LESSONS, 1)}
    by: dict[int, list[dict]] = {}
    for q in _exam_pool():
        text = f"{q['front']} {' '.join(q['options'].values())}"
        scores = []
        for n, within in lesson_chunks.items():
            hit = corpus.search(text, 3, within=within)
            scores.append((hit[0][1] if hit else 0.0, n, [i for i, _ in hit]))
        scores.sort(key=lambda x: -x[0])
        (s1, n1, top), (s2, _, _) = scores[0], scores[1]
        if s1 < 10 or s1 < 1.2 * s2 or corpus.support(q["front"], top) < 0.5:
            continue
        by.setdefault(n1, []).append({**q, "_skor": round(s1, 1)})
    for n in by:
        by[n].sort(key=lambda c: -c["_skor"])
    return by


def prepare(log=print) -> dict:
    WORK.mkdir(parents=True, exist_ok=True)
    corpus = LectureCorpus()
    qs = _assign_questions(corpus)
    index = []
    for n, (ders, konu, hoca, tarih, sids, eski) in enumerate(LESSONS, 1):
        pages = _pages(corpus, sids)
        names = [corpus.sources.get(s, {}).get("name", s) for s in sids]
        head = [
            f"# {n:02d} · {konu}", f"Ders: {ders} | Öğretim üyesi: {hoca} | Tarih: {tarih or '-'}",
            f"Kaynak: {'; '.join(names)}" + (" (GEÇEN YILIN NOTU — bu yıl PDF yok)" if eski else ""),
            f"Sayfa/parça: {len(pages)}", "", "=== KAYNAK METİN ===",
        ]
        body = [f"[{sid[:6]} s.{p}] {t}" for sid, p, t in pages]
        qlines = ["", "=== İLGİLİ KURUL 1 ÇIKMIŞ SORULARI (CEVAP ? = anahtar yok) ==="]
        for c in qs.get(n, [])[:20]:
            opts = " | ".join(f"{k}) {v}" for k, v in c["options"].items())
            qlines.append(f"- {c['id']} [{c['dosya']}] {c['front']} || {opts} || CEVAP {c['answer'] or '?'}")
        path = WORK / f"{n:02d}_{_slug(konu)}.src.txt"
        store.atomic_write_text(path, "\n".join(head + body + qlines))
        index.append({"n": n, "id": lesson_id(n, konu), "konu": konu, "ders": ders, "paket": path.name,
                      "parca": len(pages), "soru": len(qs.get(n, [])), "eski": eski})
    store.atomic_write_json(WORK / "index.json", index)
    log(f"{len(index)} ders paketi → {WORK}")
    return {"ders": len(index), "soru_atanan": sum(x["soru"] for x in index)}


# ----------------------------------------------------------------------------------------------
# build
# ----------------------------------------------------------------------------------------------
_QUESTION_BLOCK = re.compile(r"^###\s+Soru.*?(?=^##\s|^###\s(?!Soru)|\Z)", re.S | re.M)


def fidelity(md: str, corpus: LectureCorpus, source_ids: list[str]) -> float:
    """Not metninin (çıkmış soru blokları hariç) içerik köklerinin kaynakta geçme oranı."""
    body = _QUESTION_BLOCK.sub("", md)
    body = re.sub(r"^\*\*(?:Ders Kodu|Öğretim Üyesi|Müfredat|Tıbbi Kaynak|Öğrenci)[^\n]*", "", body, flags=re.M)
    toks = stems(body)
    if not toks:
        return 0.0
    src: set[str] = set()
    for c in corpus.chunks:
        if c["source_id"] in source_ids:
            src.update(stems(c["text"]))
    return round(sum(1 for t in toks if t in src) / len(toks), 3)


def _key_points(md: str) -> list[str]:
    heads = [re.sub(r"^\d+[.)]\s*", "", h).strip() for h in re.findall(r"^##\s+(.+)$", md, flags=re.M)]
    return [h for h in heads if "SPOT" not in h.upper() and "ÇIKMIŞ" not in h.upper()][:8]


def build(export: bool = False, log=print) -> dict:
    corpus = LectureCorpus()
    notes, review = [], []
    for n, (ders, konu, hoca, tarih, sids, eski) in enumerate(LESSONS, 1):
        path = WORK / f"{n:02d}_{_slug(konu)}.md"
        if not path.exists():
            continue
        md = textnorm.nfc(path.read_text(encoding="utf-8")).strip() + "\n"
        problems = []
        if not re.search(r"^##\s+", md, flags=re.M):
            problems.append("bölüm yok")
        sad = fidelity(md, corpus, sids)
        if sad < SADAKAT_ESIK:
            problems.append(f"sadakat {sad}")
        rec = {
            "id": lesson_id(n, konu), "kurul": KURUL, "committeeId": f"donem3-kurul{KURUL}", "discipline": ders,
            "title": konu, "instructor": hoca, "fileName": path.name, "keyPoints": _key_points(md),
            "charCount": len(md), "readingTimeMinutes": max(1, round(len(md.split()) / 180)), "content": md,
            "sourceIds": sids, "lastYearSource": eski, "sadakat": sad, "programDate": tarih or None,
        }
        (review if problems else notes).append({**rec, "sorunlar": problems} if problems else rec)
    report = {"zaman": datetime.now().isoformat(timespec="seconds"), "hazir": len(notes), "inceleme": [
        {"id": r["id"], "sorunlar": r["sorunlar"]} for r in review], "export": export}
    store.atomic_write_json(WORK / "build_report.json", report)
    if export and notes:
        _export(notes)
    log(json.dumps({k: v for k, v in report.items() if k != "inceleme"}, ensure_ascii=False)
        + f" inceleme={len(review)}")
    return report


def _backup(path: Path, stamp: str) -> None:
    dst = config.PROJECT_ROOT / "yedek" / "notlar" / stamp
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dst / path.name)


def _export(notes: list[dict]) -> None:
    """Kurul 1 özetlerini yeni notlarla değiştirir; diğer kurulların kayıtlarına dokunmaz.
    Yalnız tüm dersler hazır olduğunda çağrılmalı (kısmi dışa aktarma eski konuları siler)."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    content_keys = ("content",)
    meta_fields = ("id", "kurul", "committeeId", "discipline", "title", "instructor", "fileName", "keyPoints",
                   "charCount", "readingTimeMinutes")
    old = store.read_json(SUMMARY_JSON, []) or []
    _backup(SUMMARY_JSON, stamp)
    # Eski Kurul 1 özetleri geçen yılın PDF'lerinden üretilmişti; program dersleriyle tümüyle değiştirilir.
    replaced = {o["id"] for o in old}
    store.atomic_write_json(SUMMARY_JSON, [{k: n[k] for k in meta_fields + content_keys} for n in notes], indent=1)

    meta = store.read_json(META_JSON, []) or []
    _backup(META_JSON, stamp)
    meta = [m for m in meta if not (m.get("kurul") == KURUL and (m["id"] in replaced or str(m["id"]).startswith(f"k{KURUL}-")))]
    meta = [{k: n[k] for k in meta_fields} for n in notes] + meta
    store.atomic_write_json(META_JSON, meta, indent=1)

    enrich = store.read_json(ENRICH_JSON, {}) or {}
    _backup(ENRICH_JSON, stamp)
    for n in notes:
        enrich[n["id"]] = {"lessonTitle": n["title"], "discipline": n["discipline"], "instructor": n["instructor"],
                           "programDate": n["programDate"]}
    store.atomic_write_json(ENRICH_JSON, enrich, indent=1)

    for cat in CATALOG_JSONS:
        if not cat.exists():
            continue
        data = store.read_json(cat, []) or []
        _backup(cat, stamp)
        data = [d for d in data if d.get("id") not in replaced and not str(d.get("id", "")).startswith(f"k{KURUL}-")]
        data = [{k: n[k] for k in meta_fields + content_keys} for n in notes] + data
        store.atomic_write_json(cat, data, indent=1)
