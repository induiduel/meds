#!/usr/bin/env python3
"""
Faz 8 — Müfredat Bilgi Ağacı: Soru ↔ Kazanım ↔ Kurul ↔ Ders ↔ Konu ↔ Kaynak (slayt/özet) ↔ Müfredat

Tamamen yerel ve deterministik çalışır (bulut AI yok, token harcamaz). Mevcut veriyi DEĞİŞTİRMEZ;
yalnızca `meds_temp/phase8/` (hazırlık alanı) altına yeni dosyalar yazar (silinip yeniden üretilebilir).

Kurallar (kullanıcı tanımı):
  * Her kurulda farklı dersler vardır.                 → yapı: resmi ders programı (taxonomy)
  * Müfredatta her dersin birden fazla konusu vardır.   → konu: ders programındaki ders satırları
  * Her dersin birden fazla kazanımı vardır.
  * Her kazanım mutlaka bir dersin konusuna aittir.     → kazanım.konu_id zorunlu
  * PDF (ders notu/özeti/slaytı) bir dersin belli bir konusuna bağlıdır.
  * Soru içeriği mutlaka bir kazanım içerir.            → her soruya ≥1 kazanım (emin değilse birden fazla aday)
  * Kazanım; bir slayt/özetteki belli bir sayfadaki belli bir metindir → kanıt: kaynak + sayfa + metin

Kazanımlar UYDURULMAZ: resmi kazanım listesi bulunmadığı için her kazanım konunun kendi kaynağından
çıkarılır (slayt başlığı + o başlığın metni ya da özetteki ana madde). Kaynağı bulunamayan konu için
"konu geneli" kazanımı açılır ve `kanit_yok` olarak işaretlenir.

Kaynak önceliği: resmi ders programı (taxonomy) > ders PDF'leri (sources + chunks) > ders özetleri >
müfredat dosyası (kurul kodları programla çelişebilir; çelişki rapora yazılır, yapı programdan alınır).

Çıktılar (meds_temp/phase8/):
  agac.json            Hiyerarşi: müfredat → kurul → ders → konu → kazanım (kanıtlarla) + kaynak listeleri
  konular.jsonl        Konu kayıtları (kurul, ders, tarih, hoca, müfredat konusu, kaynaklar)
  kazanimlar.jsonl     Kazanım kayıtları (konu_id zorunlu, kanıt: kaynak/sayfa/metin)
  kaynak_konu.jsonl    Her PDF/özetin bağlandığı konu (skor ve gerekçe)
  soru_kazanim.jsonl   Her soru için kazanım(lar), konu, ders, kurul, en iyi slayt sayfası ve güven
  review_queue.jsonl   Düşük güvenli / çok adaylı / kanıtsız kayıtlar
  rapor.json           Sayılar, kural doğrulamaları, tutarlılık ölçümleri, elle kontrol örneği

Çalıştırma:
  python3 scripts/advanced_ai/phase8_curriculum_graph.py            # tam üretim
  python3 scripts/advanced_ai/phase8_curriculum_graph.py --sample 40 # rapora elle kontrol örneği ekle
"""
from __future__ import annotations

import argparse
import ast
import collections
import glob
import hashlib
import json
import math
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]                     # meds/
PROJECT = ROOT.parent
DB = Path(os.environ.get("MEDS_DATABASE_DIR") or PROJECT / "meds_database")
# Şimdilik ana veritabanından AYRI hazırlık alanına yazılır (meds_temp/phase8). Doğrulama sonrası
# taşıma talimatları: docs/FAZ8_DUZELTME_TALIMATLARI.md
OUT = Path(os.environ.get("MEDS_TEMP_DIR") or PROJECT / "meds_temp") / "phase8"
PHASE5_DIR = PROJECT / "meds_database_v2" / "questions"
TAXONOMY = DB / "taxonomy" / "donem3_ders_programi.json"
CURRICULUM = ROOT / "curriculum" / "kbu_tip_donem3_curriculum.json"
SUMMARIES_META = ROOT / "src" / "data" / "summaries_meta.json"
SUMMARIES_ENRICH = ROOT / "src" / "data" / "summaries_enrichment.json"

# --------------------------------------------------------------------------- metin yardımcıları
STOP = set("""
ve ile veya ama icin için bir bu su şu olan olarak gibi daha cok çok en de da ki mi mı mu mü ne hangisi hangisidir
asagidakilerden aşağıdakilerden asagidaki aşağıdaki yanlistir yanlıştır dogrudur doğrudur degildir değildir
hakkinda hakkında ilgili ile olur olan olarak sonra once önce kadar nedir hasta hastada hastanin yas yaş
yasinda yaşında erkek kadin kadın ders slayt sayfa konu kurul donem dönem tibbi tıbbi
""".split())
TR = str.maketrans({"ı": "i", "İ": "i", "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g", "ö": "o", "Ö": "o",
                    "ş": "s", "Ş": "s", "ü": "u", "Ü": "u", "â": "a", "î": "i", "û": "u", "I": "i"})


def tr_title(s: str) -> str:
    """Türkçe başlık biçimi (Python .title() 'İ' harfini bozar)."""
    out = []
    for i, w in enumerate((s or "").split()):
        lw = w.replace("I", "ı").replace("İ", "i").lower()
        if i > 0 and lw in ("ve", "ile", "veya"):
            out.append(lw)
            continue
        f = {"i": "İ", "ı": "I"}.get(lw[:1], lw[:1].upper())
        out.append(f + lw[1:])
    return " ".join(out)


def fold(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").translate(TR).lower()).strip()


def stems(s: str) -> list[str]:
    """Türkçe katlama + 5 harf kök (uygulamadaki BM25 ile aynı yaklaşım)."""
    out = []
    for w in fold(s).split():
        if len(w) < 3 or w in STOP or w.isdigit():
            continue
        out.append(w[:5])
    return out


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def overlap(a: set, b: set) -> float:
    """Kısa tarafa göre örtüşme (başlık ↔ uzun ad karşılaştırmasında adil)."""
    return len(a & b) / min(len(a), len(b)) if a and b else 0.0


def sid(*parts: str) -> str:
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:10]


def read_jsonl(path: Path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue


# --------------------------------------------------------------------------- BM25
class BM25:
    def __init__(self, docs: list[list[str]], k1: float = 1.4, b: float = 0.72):
        self.k1, self.b = k1, b
        self.tf = [collections.Counter(d) for d in docs]
        self.len = [len(d) for d in docs]
        self.avg = (sum(self.len) / len(self.len)) if docs else 1
        df = collections.Counter()
        for d in self.tf:
            df.update(d.keys())
        n = len(docs)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
        self.post = collections.defaultdict(list)
        for i, d in enumerate(self.tf):
            for t in d:
                self.post[t].append(i)

    def scores(self, q: collections.Counter) -> dict[int, float]:
        out: dict[int, float] = collections.defaultdict(float)
        for t, qw in q.items():
            idf = self.idf.get(t)
            if not idf:
                continue
            for i in self.post[t]:
                tf = self.tf[i][t]
                out[i] += qw * idf * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg))
        return out


# --------------------------------------------------------------------------- ders adı eşleme
DERS_ALIAS = {
    "patoloji": "patoloji", "farmakoloji": "farmakoloji", "genetik": "genetik", "enfeksiyon": "enfeksiyon",
    "mikrobiyoloji": "enfeksiyon", "halk saglig": "halk", "halk": "halk", "uroloji": "uroloji",
    "kadin": "kadin", "obstetrik": "kadin", "jinekoloji": "kadin", "noroloji": "noroloji", "psikiyatri": "psikiyatri",
    "aile": "aile", "anestezi": "anestezi", "ftr": "ftr", "fizik tedavi": "ftr", "beyin": "beyin",
    "norosirurji": "beyin", "cocuk": "cocuk", "pediatri": "cocuk", "ic hastalik": "ic", "dahiliye": "ic",
    "gastroenteroloji": "ic", "kardiyoloji": "kardiyoloji", "gogus hastalik": "gogushast",
    "gogus cerrahi": "goguscer", "kalp ve damar": "kalpdamar", "kalp damar": "kalpdamar", "acil": "acil",
    "ortopedi": "ortopedi", "biyokimya": "biyokimya", "radyoloji": "radyoloji",
}


def ders_key(name: str) -> str:
    f = fold(name)
    for k in sorted(DERS_ALIAS, key=len, reverse=True):
        if k in f:
            return DERS_ALIAS[k]
    return f.split()[0] if f else ""


def clean_heading(h: str) -> str:
    h = re.sub(r"^\s*(slayt|slide|sayfa)\s*\d+\s*[–\-:.]*\s*", "", h or "", flags=re.I)
    h = re.sub(r"\s+", " ", h).strip(" -–:;•.")
    return h


def is_useful_heading(h: str, ders_name: str) -> bool:
    if len(h) < 6 or len(h) > 140:
        return False
    f = fold(h)
    if not f or f.isdigit() or len(stems(h)) < 1:
        return False
    if f in {fold(ders_name), "patoloji", "farmakoloji", "giris", "ozet", "kaynaklar", "tesekkurler", "sorular"}:
        return False
    if re.match(r"^(komite|kurul|donem)\b", f):
        return False
    return True


# --------------------------------------------------------------------------- 1) Ders programı ağacı
def build_program():
    tax = json.load(open(TAXONOMY, encoding="utf-8"))
    kurullar, dersler, konular = [], {}, {}
    for k in tax["kurullar"]:
        kno = int(k["kurul"])
        kurullar.append({"kurul": kno, "kod": k["kod"].replace(" ", ""), "ad": tr_title(k["ad"]), "dersler": []})
        for d in k.get("dersler", []):
            did = f"K{kno}.{sid(str(kno), d['ders'])}"
            dersler[did] = {"ders_id": did, "kurul": kno, "ad": d["ders"], "key": ders_key(d["ders"]),
                            "saat": d.get("toplam_saat"), "hocalar": [o.get("ad") for o in d.get("ogretim_uyeleri", [])],
                            "konu_ids": []}
            kurullar[-1]["dersler"].append(did)
        for c in k.get("konular", []):
            if c.get("tur") != "ders" or not c.get("konu"):
                continue
            did = next((x for x, v in dersler.items() if v["kurul"] == kno and v["ad"] == c["ders"]), None)
            if not did:
                continue
            kid = f"{did}.{sid(fold(c['konu']))}"
            if kid not in konular:
                konular[kid] = {"konu_id": kid, "ders_id": did, "kurul": kno, "ders": c["ders"], "ad": c["konu"].strip(),
                                "tarihler": [], "hoca": c.get("ogretim_uyesi"), "saat": 0,
                                "pdf_adaylari": [], "mufredat_konusu": None, "kaynaklar": [], "kazanim_ids": []}
                dersler[did]["konu_ids"].append(kid)
            kn = konular[kid]
            if c.get("tarih"):
                kn["tarihler"].append(c["tarih"])
            kn["saat"] += c.get("saat") or 0
            for p in c.get("pdf_adaylari") or []:
                if p.get("skor", 0) >= 0.6:
                    kn["pdf_adaylari"].append(Path(p["pdf"]).name)
    return kurullar, dersler, konular


# --------------------------------------------------------------------------- 2) Müfredat dosyası ↔ program
def attach_curriculum(kurullar, konular, report):
    if not CURRICULUM.exists():
        report["mufredat"] = {"durum": "dosya yok"}
        return
    cur = json.load(open(CURRICULUM, encoding="utf-8"))
    conflicts, links = [], 0
    for code, c in (cur.get("committees") or {}).items():
        cname = stems(c.get("name", ""))
        best = max(kurullar, key=lambda k: jaccard(set(cname), set(stems(k["ad"]))))
        sim = jaccard(set(cname), set(stems(best["ad"])))
        if code.replace(" ", "") != best["kod"]:
            conflicts.append({"mufredat_kodu": code, "mufredat_adi": c.get("name"), "programdaki_kod": best["kod"],
                              "programdaki_ad": best["ad"], "ad_benzerligi": round(sim, 2)})
        if sim < 0.2:
            continue
        for t in c.get("core_topics", []):
            tt = set(stems(t))
            cand = [kn for kn in konular.values() if kn["kurul"] == best["kurul"]]
            if not cand:
                continue
            kn = max(cand, key=lambda x: overlap(tt, set(stems(x["ad"]))))
            if overlap(tt, set(stems(kn["ad"]))) >= 0.5 and not kn["mufredat_konusu"]:
                kn["mufredat_konusu"] = t
                links += 1
    report["mufredat"] = {"kod_celiskileri": conflicts, "konuya_baglanan_mufredat_basligi": links,
                          "not": "Yapı resmi ders programından alınır; müfredat dosyası yalnızca konu başlığı eşleşmesi için kullanıldı."}


# --------------------------------------------------------------------------- 3) Kaynaklar (PDF + özet) ↔ konu
def load_sources():
    src = {}
    for p in glob.glob(str(DB / "sources" / "*.json")):
        try:
            s = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        src[s["source_id"]] = s
    return src


def load_chunks():
    by_src = collections.defaultdict(list)
    for p in glob.glob(str(DB / "chunks" / "*.jsonl")):
        for c in read_jsonl(Path(p)):
            if c.get("text"):
                by_src[c.get("source_id")].append(c)
    return by_src


def heading_of(c) -> str:
    hp = c.get("heading_path")
    if isinstance(hp, str):
        try:
            hp = ast.literal_eval(hp)
        except Exception:
            hp = [hp]
    hp = [h for h in (hp or []) if h]
    return clean_heading(hp[-1]) if hp else ""


def link_sources(konular, dersler, sources, chunks_by_src, report):
    rows = []
    by_kd = collections.defaultdict(list)
    for kn in konular.values():
        by_kd[(kn["kurul"], dersler[kn["ders_id"]]["key"])].append(kn)
    pdf_name_to_konu = {}
    for kn in konular.values():
        for n in kn["pdf_adaylari"]:
            pdf_name_to_konu.setdefault(fold(Path(n).stem), kn["konu_id"])

    for s in sources.values():
        if is_exam_dump(s, chunks_by_src):
            rows.append({"kaynak_id": s["source_id"], "tip": "sinav_dokumu", "ad": s.get("name"), "yol": s.get("path"),
                         "kurul": s.get("kurul"), "ders_kaynakta": s.get("ders"), "konu_id": None, "skor": 0,
                         "gerekce": "soru/sinav dökümü — ders materyali değil (CLAUDE.md kuralı)"})
            continue
        kurul = s.get("kurul")
        try:
            kurul = int(kurul)
        except (TypeError, ValueError):
            kurul = None
        dk = ders_key(s.get("ders") or "")
        name = s.get("name") or Path(s.get("path") or "").name
        heads = [heading_of(c) for c in chunks_by_src.get(s["source_id"], [])[:12]]
        meta = s.get("metadata") or {}
        sig_title = set(stems(re.sub(r"_\d{6}_\d{6}$", "", name)))
        sig_body = set(stems(" ".join(heads) + " " + str(meta.get("ozet", ""))[:600]))
        # (a) Kurul 1: ders programındaki PDF adayıyla dosya adı birebir
        direct = pdf_name_to_konu.get(fold(Path(name).stem))
        best, score, why = None, 0.0, ""
        if direct:
            best, score, why = konular[direct], 1.0, "ders_programi_pdf_adayi"
        else:
            cands = by_kd.get((kurul, dk), []) if kurul else []
            if not cands and kurul:  # ders adı eşleşmedi: o kurulun tüm konuları
                cands = [kn for kn in konular.values() if kn["kurul"] == kurul]
            for kn in cands:
                kt = set(stems(kn["ad"]))
                sc = 0.7 * overlap(sig_title, kt) + 0.3 * overlap(sig_body, kt)
                if sc > score:
                    best, score, why = kn, sc, "ad_ve_icerik_benzerligi"
        rec = {"kaynak_id": s["source_id"], "tip": "slayt" if s.get("doc_type") == "lecture_slide" else (s.get("doc_type") or "pdf"),
               "ad": name, "yol": s.get("path"), "kurul": kurul, "ders_kaynakta": s.get("ders"), "sayfa": s.get("pages"),
               "konu_id": best["konu_id"] if best and score >= 0.34 else None, "skor": round(score, 3), "gerekce": why}
        rows.append(rec)
        if rec["konu_id"]:
            konular[rec["konu_id"]]["kaynaklar"].append({"tip": rec["tip"], "kaynak_id": rec["kaynak_id"], "ad": name,
                                                         "yol": rec["yol"], "skor": rec["skor"]})

    # Özetler
    meta = json.load(open(SUMMARIES_META, encoding="utf-8")) if SUMMARIES_META.exists() else []
    enr = json.load(open(SUMMARIES_ENRICH, encoding="utf-8")) if SUMMARIES_ENRICH.exists() else {}
    for m in meta:
        e = enr.get(m["id"], {})
        kurul = m.get("kurul")
        disc = e.get("discipline") or m.get("discipline") or ""
        title = e.get("lessonTitle") or m.get("title") or ""
        cands = by_kd.get((kurul, ders_key(disc)), []) or [kn for kn in konular.values() if kn["kurul"] == kurul]
        tt = set(stems(title)); kp = set(stems(" ".join(m.get("keyPoints", [])[:8])))
        best, score = None, 0.0
        for kn in cands:
            kt = set(stems(kn["ad"]))
            sc = 0.75 * overlap(tt, kt) + 0.25 * overlap(kp, kt)
            if fold(kn["ad"]) == fold(title):
                sc = 1.0
            if sc > score:
                best, score = kn, sc
        rec = {"kaynak_id": m["id"], "tip": "ozet", "ad": title, "yol": m.get("fileName"), "kurul": kurul,
               "ders_kaynakta": disc, "konu_id": best["konu_id"] if best and score >= 0.4 else None,
               "skor": round(score, 3), "gerekce": "ozet_basligi", "keyPoints": m.get("keyPoints", []),
               "pdf_adi": e.get("pdfName"), "pdf_yili": e.get("sourceYear")}
        rows.append(rec)
        if rec["konu_id"]:
            konular[rec["konu_id"]]["kaynaklar"].append({"tip": "ozet", "kaynak_id": m["id"], "ad": title,
                                                         "yol": m.get("fileName"), "skor": rec["skor"]})
    linked = sum(1 for r in rows if r["konu_id"])
    report["kaynaklar"] = {"toplam": len(rows), "konuya_baglanan": linked,
                           "slayt": sum(1 for r in rows if r["tip"] != "ozet"), "ozet": sum(1 for r in rows if r["tip"] == "ozet")}
    return rows


EXAM_PAT = re.compile(r"(sinav\.karab|sınav\.karab|sıra no\s*cevap|cevabınız|hangisidir\?|aşağıdakilerden hangisi)", re.I)


def is_exam_dump(s, chunks_by_src) -> bool:
    """Ders notu gibi yüklenmiş soru/sınav dökümleri (sayfalarının çoğu soru) kaynak sayılmaz."""
    path = fold((s.get("path") or "") + " " + (s.get("name") or ""))
    if re.search(r"\b(cikmis|sinav|soru|final|butunleme|d3k1)\b", path) and (s.get("ders") or "").upper() in ("D3K1", "", "NONE"):
        return True
    # "Kurul III Sınavı", "Kurul IV Cevap Anahtarı" gibi belgeler ders etiketiyle geldiğinde yukarıdaki kuraldan kaçıyordu
    if re.search(r"\b(sinavi|cevap anahtari|soru bankasi|cikmis sorular)\b", path):
        return True
    cs = chunks_by_src.get(s["source_id"], [])
    if len(cs) >= 4:
        hits = sum(1 for c in cs[:40] if EXAM_PAT.search(c.get("text") or ""))
        return hits / min(len(cs), 40) >= 0.5
    return False


# --------------------------------------------------------------------------- 4) Kazanımlar (kaynaktan, uydurmadan)
def build_kazanimlar(konular, dersler, chunks_by_src, source_rows):
    kazanimlar = {}
    ozet_by_id = {r["kaynak_id"]: r for r in source_rows if r["tip"] == "ozet"}
    for kn in konular.values():
        ders_name = dersler[kn["ders_id"]]["ad"]
        groups: dict[str, dict] = {}

        def add(text: str, evidence: dict, src_type: str):
            t = clean_heading(text)
            if not is_useful_heading(t, ders_name):
                return
            key = " ".join(sorted(set(stems(t))))
            if not key:
                return
            # Benzer başlıkları birleştir (aynı kazanımın farklı kaynaklardaki kanıtları)
            for g in groups.values():
                if jaccard(set(key.split()), set(g["_key"].split())) >= 0.7:
                    g["kanitlar"].append(evidence)
                    g["kaynak_tipleri"].add(src_type)
                    return
            groups[key] = {"_key": key, "metin": t, "kanitlar": [evidence], "kaynak_tipleri": {src_type}}

        for ks in kn["kaynaklar"]:
            if ks["tip"] == "ozet":
                for i, kp in enumerate(ozet_by_id.get(ks["kaynak_id"], {}).get("keyPoints", [])):
                    add(kp, {"tip": "ozet", "kaynak_id": ks["kaynak_id"], "kaynak_adi": ks["ad"], "madde_no": i + 1,
                             "metin": kp[:300]}, "ozet")
            else:
                for c in chunks_by_src.get(ks["kaynak_id"], []):
                    h = heading_of(c)
                    if h:
                        add(h, {"tip": "slayt", "kaynak_id": ks["kaynak_id"], "kaynak_adi": ks["ad"], "chunk_id": c["chunk_id"],
                                "sayfa": c.get("page"), "metin": re.sub(r"\s+", " ", c["text"])[:300]}, "slayt")
        items = list(groups.values())
        if not items:  # kaynak yok: konu geneli kazanım (işaretli)
            items = [{"_key": "", "metin": kn["ad"], "kanitlar": [], "kaynak_tipleri": set()}]
        for g in items:
            kid = f"{kn['konu_id']}.{sid(g['_key'] or kn['ad'])}"
            kazanimlar[kid] = {"kazanim_id": kid, "konu_id": kn["konu_id"], "ders_id": kn["ders_id"], "kurul": kn["kurul"],
                               "ders": kn["ders"], "konu": kn["ad"], "metin": g["metin"],
                               "kaynak_tipleri": sorted(g["kaynak_tipleri"]), "kanitlar": g["kanitlar"][:8],
                               "durum": "kaynaktan" if g["kanitlar"] else "konu_geneli_kanit_yok"}
            kn["kazanim_ids"].append(kid)
    return kazanimlar


# --------------------------------------------------------------------------- 5) Soru ↔ kazanım ↔ slayt
def load_phase5(dump_ids: set) -> dict:
    """Faz 5 metaverisi: doğrulanmış ders, pedagojik amaç, tıbbi varlıklar, ders slaytı eşleşmeleri
    (sınav dökümü kaynaklı eşleşmeler atılır)."""
    out = {}
    for p in glob.glob(str(PHASE5_DIR / "*.jsonl")):
        for o in read_jsonl(Path(p)):
            ca = o.get("classification_audit") or {}
            sm = [m for m in (o.get("slide_matches") or []) if m.get("source_id") not in dump_ids]
            ent = o.get("tibbi_varliklar") or {}
            ent_text = " ".join(" ".join(map(str, v)) if isinstance(v, list) else str(v) for v in ent.values()) if isinstance(ent, dict) else ""
            out[o["question_id"]] = {"ders": ca.get("verified_ders"), "konu": ca.get("verified_konu"),
                                     "amac": o.get("pedagogik_amac") or "", "varlik": ent_text,
                                     "slayt_src": {m.get("source_id") for m in sm[:3]},
                                     "slayt_chunk": {m.get("chunk_id") for m in sm[:3]}}
    return out



def question_text(q) -> tuple[collections.Counter, str]:
    opts = q.get("options") or {}
    otext = " ".join(opts.values()) if isinstance(opts, dict) else " ".join(map(str, opts))
    tm = q.get("taxonomy_metadata") or {}
    ev = q.get("evidence") or []
    evtext = " ".join(e if isinstance(e, str) else json.dumps(e, ensure_ascii=False) for e in ev)[:1200]
    c = collections.Counter()
    for w in stems(q.get("stem") or ""):
        c[w] += 2.0
    for w in stems(otext):
        c[w] += 1.2
    for w in stems(" ".join([str(tm.get("ne_sormus", "")), str(tm.get("neyini_sormus", "")), str(tm.get("alt_konu", ""))])):
        c[w] += 2.5
    for w in stems(" ".join(map(str, tm.get("terimler") or tm.get("tibbi_terimler") or []))):
        c[w] += 2.5
    for w in stems(evtext):
        c[w] += 0.5
    return c, (q.get("stem") or "")


def match_questions(kazanimlar, konular, chunks_by_src, report, sample_n: int, phase5: dict, use_hints: bool = True):
    kz = list(kazanimlar.values())
    docs = []
    for k in kz:
        body = " ".join([k["metin"]] * 3 + [k["konu"]] * 2 + [k["ders"]] + [e.get("metin", "") for e in k["kanitlar"][:4]])
        docs.append(stems(body))
    bm = BM25(docs)
    # 1. aşama: konu düzeyi belgeler (konu adı + ders + müfredat başlığı + kazanım başlıkları + kanıt metni)
    konu_list = list(konular.values())
    kz_by_konu = collections.defaultdict(list)
    for i, k in enumerate(kz):
        kz_by_konu[k["konu_id"]].append(i)
    konu_docs = []
    for kn in konu_list:
        idx = kz_by_konu.get(kn["konu_id"], [])
        heads = " ".join(dict.fromkeys(kz[i]["metin"] for i in idx[:80]))
        evid = " ".join((kz[i]["kanitlar"][0].get("metin", "")[:160] if kz[i]["kanitlar"] else "") for i in idx[:40])
        konu_docs.append(stems(" ".join([kn["ad"]] * 4 + [kn["ders"]] * 2 + [kn.get("mufredat_konusu") or ""] * 2 + [heads, evid])))
    bm_konu = BM25(konu_docs, b=0.5)
    out, review = [], []
    stats = collections.Counter()
    ders_agree = collections.Counter()
    qfiles = sorted(glob.glob(str(DB / "questions" / "*.jsonl")))
    for p in qfiles:
        for q in read_jsonl(Path(p)):
            stats["soru"] += 1
            qc, stem = question_text(q)
            p5 = phase5.get(q["question_id"]) or {}
            for w in stems(p5.get("amac", "") + " " + str(p5.get("konu") or "")):
                qc[w] += 2.0
            for w in stems(p5.get("varlik", "")):
                qc[w] += 1.5
            hint_ders = ders_key(p5["ders"]) if p5.get("ders") else None
            if not qc:
                stats["bos_soru"] += 1
            qk = str(q.get("kurul") or "")
            label_kurul = int(qk) if qk.isdigit() else None
            # 1. aşama: konu
            ks = bm_konu.scores(qc)
            kranked = []
            for i, sc_ in ks.items():
                kn = konu_list[i]
                bonus = 1.08 if label_kurul and kn["kurul"] == label_kurul else 1.0
                if not kn["kaynaklar"]:
                    bonus *= 0.9
                if use_hints:
                    if hint_ders and ders_key(kn["ders"]) == hint_ders:
                        bonus *= 1.35
                    if p5.get("slayt_src") and {x["kaynak_id"] for x in kn["kaynaklar"]} & p5["slayt_src"]:
                        bonus *= 1.6
                kranked.append((sc_ * bonus, i))
            kranked.sort(reverse=True)
            if not kranked:
                rec = {"soru_id": q["question_id"], "durum": "eslesme_yok", "kazanimlar": []}
                out.append(rec); review.append({**rec, "neden": "soru metninde eşleşecek terim yok"})
                stats["eslesme_yok"] += 1
                continue
            top = kranked[0][0]
            second = kranked[1][0] if len(kranked) > 1 else 0.0
            margin = (top - second) / top if top else 0
            if margin >= 0.2 and top >= 8:
                conf, n_konu = "yuksek", 1
            elif margin >= 0.08:
                conf, n_konu = "orta", 2
            else:
                conf, n_konu = "dusuk", 3
            # 2. aşama: seçilen konu(lar)ın içinde en iyi kazanım
            sc = bm.scores(qc)
            picks = []
            for ksc, ki in kranked[:n_konu]:
                cand = []
                for i in kz_by_konu.get(konu_list[ki]["konu_id"], []):
                    v = sc.get(i, 0.0)
                    if use_hints and p5.get("slayt_chunk") and {e.get("chunk_id") for e in kz[i]["kanitlar"]} & p5["slayt_chunk"]:
                        v = v * 1.8 + 1
                    cand.append((v, i))
                if cand:
                    cand.sort(reverse=True)
                    picks.append((ksc, cand[0][1]))
            items = []
            for s, i in picks:
                k = kz[i]
                # Kazanımı içeren en iyi slayt/özet kanıtı
                best_ev, best_s = None, 0.0
                qs = set(qc)
                for e in k["kanitlar"]:
                    es = set(stems(e.get("metin", "")))
                    o = len(qs & es)
                    if o > best_s:
                        best_ev, best_s = e, o
                items.append({"kazanim_id": k["kazanim_id"], "kazanim": k["metin"], "konu_id": k["konu_id"], "konu": k["konu"],
                              "ders": k["ders"], "kurul": k["kurul"], "skor": round(s, 2),
                              "kanit": {kk: best_ev[kk] for kk in ("tip", "kaynak_adi", "sayfa", "madde_no", "chunk_id", "metin") if kk in best_ev} if best_ev else None})
            rec = {"soru_id": q["question_id"], "kurul_etiketi": q.get("kurul"), "ders_etiketi": q.get("ders"),
                   "guven": conf, "fark": round(margin, 3), "kazanimlar": items}
            out.append(rec)
            stats[f"guven_{conf}"] += 1
            if conf != "yuksek":
                review.append({**rec, "neden": "çok adaylı" if conf == "orta" else "düşük skor"})
            # Tutarlılık: kaynağında gerçek ders adı olan sorularda tahmin edilen ders aynı mı?
            dl = q.get("ders")
            if dl and dl not in ("D3K1", "None") and ders_key(dl) in set(DERS_ALIAS.values()):
                ders_agree["olculen"] += 1
                if ders_key(items[0]["ders"]) == ders_key(dl):
                    ders_agree["uyumlu"] += 1
            if hint_ders and hint_ders in set(DERS_ALIAS.values()):
                stats["faz5_ders_olculen"] += 1
                stats["faz5_ders_uyumlu"] += ders_key(items[0]["ders"]) == hint_ders
            if label_kurul:
                stats["kurul_etiketli"] += 1
                stats["kurul_uyumlu"] += items[0]["kurul"] == label_kurul
    report["sorular"] = dict(stats)
    if ders_agree["olculen"]:
        report["sorular"]["ders_etiketi_uyumu_%"] = round(100 * ders_agree["uyumlu"] / ders_agree["olculen"], 1)
        report["sorular"]["ders_etiketi_olculen"] = ders_agree["olculen"]
    if stats["faz5_ders_olculen"]:
        report["sorular"]["faz5_ders_uyumu_%"] = round(100 * stats["faz5_ders_uyumlu"] / stats["faz5_ders_olculen"], 1)
    if stats["kurul_etiketli"]:
        report["sorular"]["kurul_etiketi_uyumu_%"] = round(100 * stats["kurul_uyumlu"] / stats["kurul_etiketli"], 1)
    if sample_n:
        import random
        random.seed(8)
        pick = random.sample(out, min(sample_n, len(out)))
        stems_by_id = {}
        for p in qfiles:
            for q in read_jsonl(Path(p)):
                stems_by_id[q["question_id"]] = (q.get("stem") or "")[:160]
        report["elle_kontrol_ornegi"] = [{"soru": stems_by_id.get(r["soru_id"]), "guven": r.get("guven"),
                                          "kazanim": r["kazanimlar"][0]["kazanim"] if r["kazanimlar"] else None,
                                          "konu": r["kazanimlar"][0]["konu"] if r["kazanimlar"] else None,
                                          "ders": r["kazanimlar"][0]["ders"] if r["kazanimlar"] else None,
                                          "kanit_sayfa": (r["kazanimlar"][0].get("kanit") or {}).get("sayfa") if r["kazanimlar"] else None}
                                         for r in pick]
    return out, review


# --------------------------------------------------------------------------- 6) Kural doğrulama + çıktı
def validate(kurullar, dersler, konular, kazanimlar, matches, report):
    checks = {
        "her_kurulda_ders_var": all(k["dersler"] for k in kurullar),
        "her_derste_konu_var_orani": round(sum(1 for d in dersler.values() if d["konu_ids"]) / len(dersler), 3),
        "her_derste_kazanim_var_orani": round(sum(1 for d in dersler.values()
                                                 if any(konular[c]["kazanim_ids"] for c in d["konu_ids"])) / len(dersler), 3),
        "her_kazanim_bir_konuya_ait": all(k["konu_id"] in konular for k in kazanimlar.values()),
        "kaynaktan_kazanim_orani": round(sum(1 for k in kazanimlar.values() if k["durum"] == "kaynaktan") / max(1, len(kazanimlar)), 3),
        "kaynagi_olan_konu_orani": round(sum(1 for k in konular.values() if k["kaynaklar"]) / max(1, len(konular)), 3),
        "her_sorunun_en_az_bir_kazanimi_var_orani": round(sum(1 for m in matches if m["kazanimlar"]) / max(1, len(matches)), 3),
    }
    report["kural_dogrulama"] = checks
    report["sayilar"] = {"kurul": len(kurullar), "ders": len(dersler), "konu": len(konular), "kazanim": len(kazanimlar),
                         "soru_baglantisi": len(matches)}


def write_outputs(kurullar, dersler, konular, kazanimlar, source_rows, matches, review, report):
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_name(OUT.name + ".tmp")
    if tmp.exists():
        for f in tmp.iterdir():
            f.unlink()
    tmp.mkdir(exist_ok=True)

    def wl(name, rows):
        with open(tmp / name, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    soru_by_kazanim = collections.defaultdict(list)
    for m in matches:
        for it in m["kazanimlar"][:1]:
            soru_by_kazanim[it["kazanim_id"]].append(m["soru_id"])
    tree = {"mufredat": "KBÜ Tıp Fakültesi Dönem 3 (resmi ders programı 2026-2027)", "uretim": report["uretim"], "kurullar": []}
    for k in kurullar:
        kn = {"kurul": k["kurul"], "kod": k["kod"], "ad": k["ad"], "dersler": []}
        for did in k["dersler"]:
            d = dersler[did]
            dn = {"ders_id": did, "ad": d["ad"], "saat": d["saat"], "hocalar": d["hocalar"], "konular": []}
            for cid in d["konu_ids"]:
                c = konular[cid]
                dn["konular"].append({"konu_id": cid, "ad": c["ad"], "tarihler": sorted(set(c["tarihler"])), "hoca": c["hoca"],
                                      "mufredat_konusu": c["mufredat_konusu"],
                                      "kaynaklar": [{kk: s[kk] for kk in ("tip", "ad", "yol")} for s in c["kaynaklar"]],
                                      "kazanimlar": [{"kazanim_id": z, "metin": kazanimlar[z]["metin"], "durum": kazanimlar[z]["durum"],
                                                      "kanit_sayisi": len(kazanimlar[z]["kanitlar"]),
                                                      "soru_sayisi": len(soru_by_kazanim.get(z, []))} for z in c["kazanim_ids"]]})
            kn["dersler"].append(dn)
        tree["kurullar"].append(kn)
    json.dump(tree, open(tmp / "agac.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    wl("konular.jsonl", konular.values())
    wl("kazanimlar.jsonl", kazanimlar.values())
    wl("kaynak_konu.jsonl", source_rows)
    wl("soru_kazanim.jsonl", matches)
    wl("review_queue.jsonl", review)
    json.dump(report, open(tmp / "rapor.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # Atomik değiştir: önceki üretim <klasör>.prev olarak saklanır (geri dönüş için)
    prev = OUT.with_name(OUT.name + ".prev")
    if prev.exists():
        for f in prev.iterdir():
            f.unlink()
        prev.rmdir()
    if any(OUT.iterdir()):
        OUT.rename(prev)
    else:
        OUT.rmdir()
    tmp.rename(OUT)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--sample", type=int, default=30, help="rapora eklenecek elle kontrol örneği sayısı")
    ap.add_argument("--no-hints", action="store_true", help="faz 5 ders/slayt ipuçlarını kapat (bağımsız doğruluk ölçümü için)")
    ap.add_argument("--dry-run", action="store_true", help="çıktı yazmadan yalnızca ölçümleri yazdır")
    args = ap.parse_args()
    t0 = time.time()
    report = {"uretim": {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "betik": "phase8_curriculum_graph.py",
                         "yontem": "ders programı kısıtlı, kaynaktan çıkarılmış kazanımlar + BM25 (Türkçe katlama, 5 harf kök)",
                         "veritabani_degistirildi": False}}
    kurullar, dersler, konular = build_program()
    attach_curriculum(kurullar, konular, report)
    sources = load_sources()
    chunks_by_src = load_chunks()
    source_rows = link_sources(konular, dersler, sources, chunks_by_src, report)
    kazanimlar = build_kazanimlar(konular, dersler, chunks_by_src, source_rows)
    dump_ids = {r["kaynak_id"] for r in source_rows if r["tip"] == "sinav_dokumu"}
    phase5 = load_phase5(dump_ids)
    report["faz5_metaveri"] = {"soru": len(phase5), "ders_ipucu": sum(1 for v in phase5.values() if v["ders"]),
                               "slayt_ipucu": sum(1 for v in phase5.values() if v["slayt_src"]), "ipuclari_kullanildi": not args.no_hints}
    matches, review = match_questions(kazanimlar, konular, chunks_by_src, report, args.sample, phase5, use_hints=not args.no_hints)
    validate(kurullar, dersler, konular, kazanimlar, matches, report)
    report["uretim"]["sure_sn"] = round(time.time() - t0, 1)
    if not args.dry_run:
        write_outputs(kurullar, dersler, konular, kazanimlar, source_rows, matches, review, report)
    print(json.dumps({k: report[k] for k in ("sayilar", "kural_dogrulama", "kaynaklar", "faz5_metaveri", "sorular")}, ensure_ascii=False, indent=1))
    print(f"\nÇıktı: {OUT}")


if __name__ == "__main__":
    sys.exit(main())
