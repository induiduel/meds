#!/usr/bin/env python3
"""Ders işçisi — B2 yayın: yöneticinin onayladığı taslakları kanonik kaynaklara birleştirir (CİHAZDA çalışır).

  ../.venv-ocr/bin/python scripts/ders_isci/yayinla.py            # Oracle'dan onaylananları çek + birleştir
  ... yayinla.py --deneme                                          # yalnız denetle, hiçbir şey yazma
  ... yayinla.py --is 20261011-e1c2ffa86e                          # tek taslak
  ... yayinla.py --cekme                                           # Oracle'a bağlanma, yereldekileri işle

Akış (her taslak için önce TÜM denetimler, sonra yazım; bir hata → o taslak hiç yazılmaz):
  deck.json          → meds/src/data/interactive_learning_decks.json (aynı kimlik varsa değiştirilir)
  ders_paketi.json   → meds_database_v2/kurul1_ders_paketleri/<id>.json + index.json
  ders_notu.md       → meds_temp/study/k1/NN_slug.md + site özetleri (s14 kayıt biçimi; yalnız bu ders güncellenir)
  ornek_sorular.json → meds_temp/study/ornek/sorular/<id>.json → s16 build --export (korumalı)
  sozluk.json        → editor_glossary_new/fix.jsonl (s13 kalıcılığı) + medical_glossary.json + ansiklopedi
  cikmis_baglantilari→ meds_database/derived/learn_links_ders_isci.json + learn_links.json (ilgili, güven ≥ orta)
  bilgi_havuzu.jsonl → meds_database_v2/bilgi_havuzu/<id>.jsonl
  hastaliklar.json   → meds_database_v2/ders_isci/hastalik_onerileri/<id>.json (diseases.json'a ELLE/ayrı adımla)
  taslağın tamamı    → meds_database_v2/ders_isci/yayinlanan/<is_id>/ (iz)
  kayıt              → scripts/ders_isci/yayin_kaydi.json (s14 LESSONS'a ek/güncelleme; checklist de okur)
Yazılan her dosya önce /home/indu/medsor-yedek/ders_isci_yayin/<zaman>/ altına yedeklenir. Sonda Oracle'daki
taslak `yayinlandi` olarak işaretlenir. Commit ve dağıtım ayrı adımdır (çıktıda listelenir).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEDS = HERE.parents[1]
ROOT = MEDS.parent
sys.path.insert(0, str(MEDS / "scripts"))

from v2.stages import s14_notes as s14  # noqa: E402
from v2.stages import s16_ornek_sorular as s16  # noqa: E402
from v2.stages.s15_k1_decks import COMMITTEE, RENK  # noqa: E402

ONAYLANAN = ROOT / "meds_temp" / "ders_isci" / "onaylanan"
KAYIT = HERE / "yayin_kaydi.json"
YEDEK = Path("/home/indu/medsor-yedek/ders_isci_yayin")
SITE = MEDS / "src" / "data"
DECKS = SITE / "interactive_learning_decks.json"
GLOSSARY = SITE / "medical_glossary.json"
ENCYCLOPEDIA = SITE / "medical_encyclopedia.json"
PAKET = s16.PAKET_DIR
STUDY = ROOT / "meds_temp" / "study"
DB2 = ROOT / "meds_database_v2"
LINKS = ROOT / "meds_database" / "derived" / "learn_links.json"
LINKS_ISCI = ROOT / "meds_database" / "derived" / "learn_links_ders_isci.json"
ORACLE = "medsor-oracle"
O_TASLAK = "/home/ubuntu/medsor/ders_isci/taslak"
O_MANIFEST = "/home/ubuntu/medsor/meds_downloads/_manifest.json"
GIT_HEDEF = [  # yazılan ve commit'lenecek repo yolları; başka oturumun yarım işi varsa yayın durur
    "src/data/interactive_learning_decks.json", "src/data/summaries/kurul1.json", "src/data/summaries_meta.json",
    "src/data/summaries_enrichment.json", "src/data/lectureSummariesCatalog.json", "data/lectureSummariesCatalog.json",
    "src/data/medical_glossary.json", "src/data/medical_encyclopedia.json", "src/data/ornek_sorular/k1",
    "scripts/ders_isci/yayin_kaydi.json",
]


def oku(p: Path, vars_=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return vars_


def yaz_json(p: Path, obj, indent=1):
    """Atomik yazım; dosya varsa mevcut biçimi (girinti, sondaki satır sonu) korunur — git diff'i yalnız içerik olsun."""
    p.parent.mkdir(parents=True, exist_ok=True)
    son = "\n"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            bas = f.read(64)
        m = re.match(r"^[\[{]\n( +)", bas)
        indent = len(m.group(1)) if m else (None if bas[:1] in "[{" and "\n" not in bas else indent)
        with open(p, "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 1))
            son = "\n" if f.read(1) == b"\n" else ""
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=indent) + son, encoding="utf-8")
    tmp.replace(p)


def norm_key(s: str) -> str:
    return s14.ids.norm_key(s)


class Yayin:
    def __init__(self, d: Path, deneme: bool, yedek: Path):
        self.d, self.deneme, self.yedek = d, deneme, yedek
        self.hata: list[str] = []
        self.not_: list[str] = []
        self.yazilan: list[str] = []
        self.b = oku(d / "baglam.json", {})
        self.paket = oku(d / "ders_paketi.json", {})
        self.deck = oku(d / "deck.json", {})
        self.karar = oku(d / "karar.json", {})

    # ------------------------------------------------------------------ yardımcılar
    def _yedekle(self, p: Path):
        if p.exists():
            hedef = self.yedek / p.relative_to(ROOT)
            if not hedef.exists():
                hedef.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, hedef)
        self.yazilan.append(str(p.relative_to(ROOT)))

    def _yaz(self, p: Path, obj, indent=1):
        self._yedekle(p)
        yaz_json(p, obj, indent)

    def _yaz_metin(self, p: Path, txt: str):
        self._yedekle(p)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(txt, encoding="utf-8")

    # ------------------------------------------------------------------ 1. denetim (hiçbir şey yazmaz)
    def denetle(self, kaynak_id: str | None) -> bool:
        b, p, k = self.b, self.paket, self.karar
        if k.get("karar") != "onayla":
            self.hata.append(f"karar onayla değil ({k.get('karar')})")
        if b.get("kurul") != 1:
            self.hata.append(f"şimdilik yalnız Kurul 1 yayınlanır (kurul={b.get('kurul')})")
        den = oku(self.d / "denetim.json", {})
        if den.get("hata"):
            self.hata.append(f"işçi denetimi {den.get('hata')} HATA")
        self.n = int(b.get("numara") or 0)
        self.ders_id = b.get("ders_id") or ""
        self.deste_id = b.get("deste_id") or ""
        if p.get("id") != self.ders_id or self.deck.get("id") != self.deste_id or self.deste_id != f"k1p-{self.ders_id}":
            self.hata.append(f"kimlikler tutarsız: paket={p.get('id')} deste={self.deck.get('id')} bağlam={self.ders_id}")
        mevcut = dict(enumerate(s14.LESSONS, 1))
        if self.n in mevcut:  # güncelleme: ders kimliği ve konusu LESSONS'taki gibi kalmalı (kimlik konudan üretilir)
            ders, konu, hoca, tarih, _, _ = mevcut[self.n]
        else:
            ders, konu, hoca, tarih = p.get("ders"), p.get("konu"), p.get("ogretim_uyesi"), p.get("tarih") or ""
        if s14.lesson_id(self.n, konu) != self.ders_id:
            self.hata.append(f"ders kimliği {self.ders_id} ≠ s14 kimliği {s14.lesson_id(self.n, konu)}")
        diger = [y for y in oku(KAYIT, []) if y["numara"] == self.n and y["is_id"] != self.d.name]
        if self.n not in mevcut and any(y["ders_id"] != self.ders_id for y in diger):
            self.hata.append(f"numara {self.n} başka bir yayınlanmış derse ait")
        if not kaynak_id:
            self.hata.append("PDF'in kaynak kimliği (manifest) bulunamadı")
        self.kayit = {"is_id": self.d.name, "kurul": 1, "numara": self.n, "ders_id": self.ders_id,
                      "deste_id": self.deste_id, "ders": ders, "konu": konu, "hoca": p.get("ogretim_uyesi") or hoca,
                      "tarih": p.get("tarih") or tarih or "", "kaynak_idleri": [kaynak_id] if kaynak_id else [],
                      "pdf": b.get("pdf_yolu"), "mod": b.get("mod"),
                      "kaynak_md": f"meds_database_v2/ders_isci/yayinlanan/{self.d.name}/kaynak.md",
                      "onaylayan": k.get("kim"), "onay_zamani": k.get("zaman")}

        # deste
        tmp = self.yedek / "_deneme_deck.json"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps([self._deste()], ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([sys.executable, str(MEDS / "scripts" / "validate_learning_decks.py"), str(tmp), "--ozet"],
                           capture_output=True, text=True)
        tmp.unlink()
        if r.returncode != 0:
            self.hata.append("deste doğrulayıcı: " + r.stdout.strip().splitlines()[-1])
        # ders notu sadakati (işçinin PDF metnine karşı)
        md = (self.d / "ders_notu.md").read_text(encoding="utf-8")
        self.sadakat = s14.fidelity(md, _BosDerlem(), [], (self.d / "kaynak.md").read_text(encoding="utf-8"))
        if self.sadakat < s14.SADAKAT_ESIK:
            self.hata.append(f"ders notu sadakati {self.sadakat} < {s14.SADAKAT_ESIK}")
        if not re.search(r"^##\s+", md, flags=re.M):
            self.hata.append("ders notunda bölüm yok")
        # örnek sorular (s16 kuralları)
        sor = oku(self.d / "ornek_sorular.json", {})
        cik = s16._cikmislar()
        tum = {q["question_id"] for q in cik}
        for f in sorted(s16.SORU_DIR.glob("*.jsonl")):
            for line in f.read_text(encoding="utf-8").splitlines():
                tum.add(json.loads(line)["question_id"])
        tum |= {q["question_id"] for q in s16._site_cikmislar()}
        sorun = s16._denetle({**p, "kazanimlar": p.get("kazanimlar") or []}, sor, [], tum)
        if sorun:
            self.hata += [f"örnek soru: {x}" for x in sorun[:10]]
        if not p.get("kazanimlar"):
            self.hata.append("ders paketinde kazanım yok")
        # sözlük
        sz = oku(self.d / "sozluk.json", {})
        for t in sz.get("yeni", []):
            if not (t.get("term") and t.get("definition")):
                self.hata.append(f"sözlük: eksik terim {t}")
        return not self.hata

    def _deste(self) -> dict:
        d = {k: v for k, v in self.deck.items() if k not in ("isNew", "version", "totalInteractiveElements", "interactiveRatio")}
        bag = [x for x in oku(self.d / "cikmis_baglantilari.json", []) if x.get("ilgili")]
        d.update({"committee": COMMITTEE, "themeColor": RENK.get(d.get("discipline"), "slate"), "confidence": "high",
                  "audioFile": "", "audioDuration": "", "programDate": self.paket.get("tarih") or None,
                  "totalSlides": len(d.get("slides") or []), "matchedPastQuestionsCount": len(bag),
                  "deckId": d["id"]})
        return d

    # ------------------------------------------------------------------ 2. yazım
    def yaz(self):
        p, n, did = self.paket, self.n, self.ders_id
        md = (self.d / "ders_notu.md").read_text(encoding="utf-8")
        deste = self._deste()
        # deste
        decks = oku(DECKS, [])
        decks = [x for x in decks if x.get("id") != deste["id"]]
        decks.append(deste)
        self._yaz(DECKS, decks)
        # ders paketi + dizin
        paket = {**{k: v for k, v in p.items()}, "gecen_yil_kaynagi": False, "ders_notu": md,
                 "ogrenim_slaytlari": p.get("ogrenim_slaytlari") or [], "kaynak": "ders_isci", "is_id": self.d.name}
        self._yaz(PAKET / f"{did}.json", paket)
        idx = [x for x in oku(PAKET / "index.json", []) if x.get("id") != did]
        idx.append({"sira": n, "id": did, "ders": self.kayit["ders"], "konu": self.kayit["konu"],
                    "ogretim_uyesi": self.kayit["hoca"], "tarih": self.kayit["tarih"], "gecen_yil": False,
                    "kazanim": len(p.get("kazanimlar") or []), "bilgi_paketi": len(p.get("bilgi_paketi") or []),
                    "slayt": deste["totalSlides"], "ozet_kelime": len(json.dumps(p.get("ders_ozeti") or {}).split()),
                    "not_karakter": len(md), "kaynak_kapsama": None, "dosya": f"{did}.json", "sorunlar": []})
        self._yaz(PAKET / "index.json", sorted(idx, key=lambda x: x["sira"]))
        # ders notu: çalışma dosyası + site kayıtları (yalnız bu ders)
        eski = [x for x in s14.WORK.glob(f"{n:02d}_*.md")]
        for e in eski:
            self._yedekle(e)
            e.unlink()
        self._yaz_metin(s14.WORK / f"{n:02d}_{s14._slug(self.kayit['konu'])}.md", s14.textnorm.nfc(md).strip() + "\n")
        self._not_kayitlari(md)
        # örnek sorular (dosya; s16 derlemesi toplu adımda)
        sor = oku(self.d / "ornek_sorular.json", {})
        self._yaz(s16.YAZIM_DIR / f"{did}.json", {"sorular": sor.get("sorular", [])})
        # sözlük
        self._sozluk()
        # çıkmış bağları
        self._baglar()
        # bilgi havuzu + hastalık önerileri + iz
        hv = [json.loads(x) | {"ders_id": did, "is_id": self.d.name}
              for x in (self.d / "bilgi_havuzu.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
        self._yaz_metin(DB2 / "bilgi_havuzu" / f"{did}.jsonl", "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in hv))
        self._yaz(DB2 / "ders_isci" / "hastalik_onerileri" / f"{did}.json",
                  {"is_id": self.d.name, "ders_id": did, "durum": "oneri (diseases.json'a henüz yazılmadı)",
                   "profiller": oku(self.d / "hastaliklar.json", [])})
        iz = DB2 / "ders_isci" / "yayinlanan" / self.d.name
        iz.mkdir(parents=True, exist_ok=True)
        for f in self.d.iterdir():
            if f.is_file() and f.name not in ("oturum.json",):
                shutil.copy2(f, iz / f.name)
        # kayıt
        kayit = [y for y in oku(KAYIT, []) if y["ders_id"] != did]
        kayit.append(self.kayit | {"yayin_zamani": time.strftime("%Y-%m-%dT%H:%M:%S"), "sadakat": self.sadakat})
        self._yaz(KAYIT, sorted(kayit, key=lambda y: (y["kurul"], y["numara"])))

    def _not_kayitlari(self, md: str):
        k = self.kayit
        rec = {"id": self.ders_id, "kurul": 1, "committeeId": "donem3-kurul1", "discipline": k["ders"], "title": k["konu"],
               "instructor": k["hoca"], "fileName": f"{self.n:02d}_{s14._slug(k['konu'])}.md", "keyPoints": s14._key_points(md),
               "charCount": len(md), "readingTimeMinutes": max(1, round(len(md.split()) / 180)), "content": md}
        meta_f = ("id", "kurul", "committeeId", "discipline", "title", "instructor", "fileName", "keyPoints",
                  "charCount", "readingTimeMinutes")

        def upsert(lst, obj):
            out = [x for x in lst if x.get("id") != obj["id"]]
            out.append(obj)
            return out

        def sira(x):  # Kurul 1 kayıtları ders numarasına göre, diğerleri olduğu yerde
            m = re.match(r"^k1-(\d+)-", str(x.get("id")))
            return (0, int(m.group(1))) if m else (1, 0)

        self._yaz(s14.SUMMARY_JSON, sorted(upsert(oku(s14.SUMMARY_JSON, []), rec), key=sira))
        self._yaz(s14.META_JSON, sorted(upsert(oku(s14.META_JSON, []), {f: rec[f] for f in meta_f}), key=sira))
        en = oku(s14.ENRICH_JSON, {})
        en[self.ders_id] = {"lessonTitle": k["konu"], "discipline": k["ders"], "instructor": k["hoca"],
                            "programDate": k["tarih"] or None}
        self._yaz(s14.ENRICH_JSON, en)
        for cat in s14.CATALOG_JSONS:
            if cat.exists():
                self._yaz(cat, sorted(upsert(oku(cat, []), rec), key=sira))

    def _sozluk(self):
        sz = oku(self.d / "sozluk.json", {})
        g = oku(GLOSSARY, {})
        mevcut = {norm_key(v.get("term") or ""): key for key, v in g.items()}
        yeni_satir, fix_satir, eklenen = [], [], []
        k = self.kayit
        for t in sz.get("yeni", []):
            term = t["term"].strip()
            key = term.replace("I", "ı").replace("İ", "i").lower()
            if key in g or norm_key(term) in mevcut:
                self.not_.append(f"sözlük: '{term}' zaten var, eklenmedi")
                continue
            kanit = t.get("kanit") or {}
            rec = {"term": term, "category": t.get("category") or "terim", "definition": t["definition"],
                   "description": t["definition"], "discipline": t.get("discipline") or k["ders"], "committee": ""}
            if t.get("pearl"):
                rec["clinicalPearl"] = t["pearl"]
            if t.get("aliases"):
                rec["aliases"] = t["aliases"]
            rec["dogrulama"] = {"durum": "ders_isci", "destek": 1.0, "uretici": "s13_study", "is_id": self.d.name}
            rec["kaynaklar"] = [{"chunk_id": None, "kaynak": k["pdf"], "ders": k["ders"], "kurul": 1,
                                 "sayfa": kanit.get("sayfa"), "alinti": kanit.get("alinti")}]
            g[key] = rec
            mevcut[norm_key(term)] = key
            eklenen.append(key)
            yeni_satir.append({"term": term, "category": rec["category"], "discipline": rec["discipline"],
                               "definition": t["definition"], "kaynak": [], "aliases": t.get("aliases") or [],
                               "pearl": t.get("pearl"), "isci": {"is_id": self.d.name, "ders_id": self.ders_id,
                                                                  "kaynak": rec["kaynaklar"][0]}})
        for z in sz.get("zenginlestir", []):
            key = z.get("key") or ""
            if key not in g:
                key = mevcut.get(norm_key(key), "")
            if not key or not z.get("pearl"):
                self.not_.append(f"sözlük zenginleştirme: '{z.get('key')}' bulunamadı")
                continue
            eski = (g[key].get("clinicalPearl") or "").strip()
            if z["pearl"].strip() in eski:
                continue
            g[key]["clinicalPearl"] = (eski + " · " if eski else "") + z["pearl"].strip()
            fix_satir.append({"key": key, "pearl": g[key]["clinicalPearl"], "isci": {"is_id": self.d.name}})
        self._yaz(GLOSSARY, g, indent=2)
        for ad, satirlar in (("editor_glossary_new.jsonl", yeni_satir), ("editor_glossary_fix.jsonl", fix_satir)):
            if satirlar:
                f = STUDY / ad
                eski = f.read_text(encoding="utf-8") if f.exists() else ""
                self._yaz_metin(f, eski + ("" if not eski or eski.endswith("\n") else "\n")
                                + "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in satirlar))
        # ansiklopedi: s13'ün yeni terim biçimi
        enc = oku(ENCYCLOPEDIA, [])
        have = {norm_key(e.get("term") or e.get("title") or "") for e in enc}
        for key in eklenen:
            t = g[key]
            if norm_key(t["term"]) in have:
                continue
            src = t["kaynaklar"][0]
            enc.append({"id": f"s13-{s14._slug(t['term'])}", "term": t["term"], "aliases": t.get("aliases") or [],
                        "category": t["category"], "kurul": "Kurul 1", "discipline": t["discipline"],
                        "instructorAndSource": f"Ders notu: {Path(src['kaynak'] or '').stem} s.{src['sayfa']}",
                        "definition": t["definition"], "lectureContextNotes": "", "examSpotPearls": t.get("clinicalPearl") or "",
                        "uretici": "s13_study",
                        "aiAudit": {"verified": True, "verifiedAt": time.strftime("%Y-%m-%d"), "accuracyScore": 100,
                                    "auditSummary": "Tanım ders işçisinde ders PDF'i alıntısıyla doğrulandı; yönetici onayladı."}})
        self._yaz(ENCYCLOPEDIA, enc, indent=2)
        self.not_.append(f"sözlük: {len(eklenen)} yeni, {len(fix_satir)} zenginleştirme")

    def _baglar(self):
        bag = [x for x in oku(self.d / "cikmis_baglantilari.json", [])
               if x.get("ilgili") and x.get("guven") in ("yuksek", "orta") and x.get("slideNumber")]
        slaytlar = {s.get("slideNumber"): s.get("title") for s in self.deck.get("slides") or []}
        isci = oku(LINKS_ISCI, {}) or {}
        isci = {q: v for q, v in isci.items() if v.get("deckId") != self.deste_id}
        for x in bag:
            isci[str(x["soru_id"])] = {"deckId": self.deste_id, "deckTitle": self.deck.get("shortTitle") or self.deck.get("title"),
                                       "slideNumber": int(x["slideNumber"]),
                                       "slideTitle": slaytlar.get(x["slideNumber"]) or x.get("slideTitle") or "",
                                       "skor": 10.0 if x["guven"] == "yuksek" else 6.0, "guven": x["guven"],
                                       "kaynak": "ders_isci", "is_id": self.d.name}
        self._yaz(LINKS_ISCI, isci)
        ll = oku(LINKS, {"baglantilar": {}})
        ll.setdefault("baglantilar", {}).update(isci)
        self._yaz(LINKS, ll, indent=None)
        self.not_.append(f"çıkmış bağı: {len(bag)} (ilgili + güven ≥ orta)")


class _BosDerlem:
    chunks: list = []


def ssh(cmd: str, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(["ssh", ORACLE, cmd], capture_output=True, text=True, timeout=120, **kw)


def cek(tek: str | None) -> list[str]:
    """Oracle'da onaylanmış ama yayınlanmamış taslakları yerel `onaylanan/` altına çeker."""
    r = ssh(f"cd {O_TASLAK} && for d in */; do d=${{d%/}}; [ -f $d/karar.json ] && [ ! -f $d/yayin.json ] && "
            f"grep -q '\"onayla\"' $d/karar.json && echo $d; done; true")
    ids = [x for x in r.stdout.split() if re.match(r"^[0-9]{8}-[0-9a-f]{10}(?:-\d+)?$", x) and (not tek or x == tek)]
    ONAYLANAN.mkdir(parents=True, exist_ok=True)
    for i in ids:
        subprocess.run(["rsync", "-a", "--delete", f"{ORACLE}:{O_TASLAK}/{i}/", str(ONAYLANAN / i) + "/"], check=True)
    return ids


def kaynak_kimligi(pdf_yolu: str) -> str | None:
    """Drive manifestinde PDF'in source_id'si (s14 kaynak kimliği). Yol karşılaştırması boşluklara duyarsız."""
    r = ssh(f"cat {O_MANIFEST}")
    if r.returncode != 0:
        return None
    sade = lambda s: re.sub(r"\s+", "", s or "")  # noqa: E731
    for it in json.loads(r.stdout).get("items", []):
        if sade(it.get("path")) == sade(pdf_yolu):
            return it.get("source_id")
    return None


def isaretle(is_id: str, ozet: dict):
    """Oracle'daki taslağı yayınlandı işaretler (dosyalar işçi kullanıcısına ait → konteyner içinden)."""
    js = json.dumps(ozet, ensure_ascii=False).replace("'", "'\\''")
    kod = ("import json,sys,time;d='/isci/taslak/%s';o=json.loads(sys.argv[1]);"
           "json.dump(o,open(d+'/yayin.json','w'),ensure_ascii=False,indent=1);"
           "du=json.load(open(d+'/durum.json'));du.update(durum='yayinlandi',zaman=time.time());"
           "json.dump(du,open(d+'/durum.json','w'),ensure_ascii=False,indent=1)") % is_id
    r = ssh(f"docker exec meds-ders-isci python3 -c \"{kod}\" '{js}'")
    return r.returncode == 0, r.stderr.strip()


def git_kirli() -> list[str]:
    r = subprocess.run(["git", "status", "--porcelain", "--", *GIT_HEDEF], cwd=MEDS, capture_output=True, text=True)
    return [x for x in r.stdout.splitlines() if x.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deneme", action="store_true")
    ap.add_argument("--is", dest="tek")
    ap.add_argument("--cekme", action="store_true")
    a = ap.parse_args()

    if not a.cekme:
        print("Oracle'dan çekilen:", cek(a.tek) or "yok")
    yayinli = {y["is_id"] for y in oku(KAYIT, [])}
    adaylar = sorted(d for d in ONAYLANAN.glob("*") if d.is_dir() and (not a.tek or d.name == a.tek)
                     and d.name not in yayinli and (oku(d / "karar.json", {}) or {}).get("karar") == "onayla")
    if not adaylar:
        print("yayınlanacak onaylı taslak yok")
        return 0
    kirli = git_kirli()
    if kirli and not a.deneme:
        print("DURDU: hedef dosyalarda commit'lenmemiş değişiklik var (başka oturum?):", *kirli, sep="\n  ")
        return 2
    yedek = YEDEK / time.strftime("%Y%m%d_%H%M%S")
    sonuc = []
    for d in adaylar:
        y = Yayin(d, a.deneme, yedek)
        kid = kaynak_kimligi(y.b.get("pdf_yolu") or "")
        ok = y.denetle(kid)
        print(f"\n== {d.name} · {y.b.get('ders_id')} · sadakat {getattr(y, 'sadakat', '?')} · "
              f"{'DENETİM TAMAM' if ok else 'DENETİM HATALI'}")
        for h in y.hata:
            print("  HATA", h)
        if not ok or a.deneme:
            continue
        y.yaz()
        for x in y.not_:
            print("  ·", x)
        sonuc.append(y)
    if not sonuc:
        return 0 if a.deneme else 1

    # toplu adımlar: deste doğrulama, örnek soru derlemesi (korumalı), paketler
    r = subprocess.run([sys.executable, str(MEDS / "scripts" / "validate_learning_decks.py"), "--ozet"],
                       capture_output=True, text=True, cwd=MEDS)
    print("deste doğrulayıcı:", r.stdout.strip().splitlines()[-1])
    if r.returncode != 0:
        print("DURDU: tüm desteler doğrulamadan geçmedi; yedek:", yedek)
        return 3
    rapor = s16.build(export=False)  # yalnız meds_database_v2/ornek_sorular_k1 (çıktı) — site toptan yazılmaz
    sorunlu = [y.ders_id for y in sonuc if rapor.get(y.ders_id) is None or rapor.get(y.ders_id)]
    if sorunlu:
        print("örnek sorular siteye AKTARILMADI (s16 denetimi):", sorunlu)
    s16.disa_aktar([y.ders_id for y in sonuc if y.ders_id not in sorunlu])
    subprocess.run(["npm", "run", "-s", "decks:packages"], cwd=MEDS, check=False)
    for y in sonuc:
        ok, err = isaretle(y.d.name, {"yayin_zamani": time.strftime("%Y-%m-%dT%H:%M:%S"), "ders_id": y.ders_id,
                                      "deste_id": y.deste_id, "yedek": str(yedek)})
        print(f"Oracle işareti {y.d.name}: {'tamam' if ok else 'BAŞARISIZ ' + err}")
    print("\nYedek:", yedek)
    print("Commit edilecek repo yolları:", *GIT_HEDEF, sep="\n  ")
    print("Sonra: vite build + Oracle dağıtımı (src/data, data/, meds_database/derived/learn_links.json).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
