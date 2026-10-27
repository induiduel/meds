#!/usr/bin/env python3
"""Ders işçisi — B2 yayın: yöneticinin onayladığı taslakları kanonik kaynaklara birleştirir.

ORACLE (asıl yol; systemd `meds-ders-yayin.timer`, 10 dk'da bir — deploy/oracle/meds-ders-yayin.*):
  python3 scripts/ders_isci/yayinla.py --sunucu
    · /home/ubuntu/medsor/ders_isci/taslak/* içinde karar=onayla ve yayin.json'u olmayan taslakları yayınlar,
    · asıl yayın defteri durum klasöründedir (ders_isci/yayin_kaydi.json); cihazdan yapılan bir dağıtım repo
      kopyasındaki yayını ezdiyse (scripts/ders_isci/yayin_kaydi.json'da eksik) izinden YENİDEN uygular,
    · bir şey yazıldıysa meds-app'i yeniden derler (/tmp/meds-deploy.lock), taslağı `yayinlandi` işaretler, bildirim atar.
CİHAZ:
  .venv-ocr/bin/python scripts/ders_isci/yayinla.py --esitle      # Oracle'da yayınlananları yerel kaynaklara işle
    (deploy-code.sh ve sync-data.sh --to-oracle bunu önce çalıştırır; eşit değilse dağıtım durur)
  ... yayinla.py --deneme --is <is_id>                              # bir taslağı yalnız denetle (yazmaz)

Akış (her taslak için önce TÜM denetimler, sonra yazım; bir hata → o taslak hiç yazılmaz; yazım idempotent upsert):
  deck.json          → meds/src/data/interactive_learning_decks.json (aynı kimlik varsa değiştirilir)
  ders_paketi.json   → meds_database_v2/kurul1_ders_paketleri/<id>.json + index.json
  ders_notu.md       → meds_temp/study/k1/NN_slug.md + site özetleri (s14 kayıt biçimi; yalnız bu ders güncellenir)
  ornek_sorular.json → meds_temp/study/ornek/sorular/<id>.json → s16 çıktısı → site (yalnız bu ders, upsert)
  sozluk.json        → editor_glossary_new/fix.jsonl (s13 kalıcılığı) + medical_glossary.json + ansiklopedi
  cikmis_baglantilari→ meds_database/derived/learn_links_ders_isci.json + learn_links.json (ilgili, güven ≥ orta)
  bilgi_havuzu.jsonl → meds_database_v2/bilgi_havuzu/<id>.jsonl
  hastaliklar.json   → meds_database_v2/ders_isci/hastalik_onerileri/<id>.json (diseases.json'a ayrı adımla)
  taslağın tamamı    → meds_database_v2/ders_isci/yayinlanan/<is_id>/ (iz; yeniden uygulama ve cihaz eşitlemesi buradan)
  kayıt              → scripts/ders_isci/yayin_kaydi.json (s14 LESSONS'a ek/güncelleme; checklist de okur)
Yazılan her dosya önce <yedek>/ders_isci_yayin/<zaman>/ altına yedeklenir.
"""
from __future__ import annotations

import argparse
import json
import os
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
# v2/config.py kökü varsayılan /home/indu/medsor'dur; Oracle'da (/home/ubuntu/medsor) yanlış yola okur/yazardı
os.environ.setdefault("MEDS_PROJECT_ROOT", str(ROOT))
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

from v2.stages import s14_notes as s14  # noqa: E402
from v2.stages import s16_ornek_sorular as s16  # noqa: E402
from v2.stages.s15_k1_decks import COMMITTEE, RENK  # noqa: E402

ONAYLANAN = ROOT / "meds_temp" / "ders_isci" / "onaylanan"
KAYIT = HERE / "yayin_kaydi.json"
SUNUCU = Path("/home/ubuntu/medsor/ders_isci").is_dir() and str(ROOT) == "/home/ubuntu/medsor"
YEDEK = (Path("/home/ubuntu/medsor-yedek") if SUNUCU else Path("/home/indu/medsor-yedek")) / "ders_isci_yayin"
DURUM_KAYIT = Path("/home/ubuntu/medsor/ders_isci/yayin_kaydi.json")   # Oracle: asıl yayın defteri (rsync'e kapalı)
L_TASLAK = Path("/home/ubuntu/medsor/ders_isci/taslak")
DOWNLOADS_MANIFEST = Path(__file__).resolve().parents[3] / "meds_downloads" / "_manifest.json"
L_MANIFEST = Path("/home/ubuntu/medsor/meds_downloads/_manifest.json")
KILIT = "/tmp/meds-deploy.lock"
SITE = MEDS / "src" / "data"
DECKS = SITE / "interactive_learning_decks.json"
GLOSSARY = SITE / "medical_glossary.json"
ENCYCLOPEDIA = SITE / "medical_encyclopedia.json"
PAKET = s16.PAKET_DIR
KURUL = 1  # süreç başına tek kurul (kurula_bagla); uygula() bir çağrıda yalnız bir kurulu işler


def kurula_bagla(k: int) -> None:
    """Kurul 2+ yayını (2026-10-20): s14/s16 yolları, ders listesi (ders defteri), paket klasörü, deste kurul adı."""
    global KURUL, PAKET, COMMITTEE
    if k == KURUL:
        return
    s14.kurul_ayarla(k); s16.kurul_ayarla(k)
    KURUL, PAKET = k, s16.PAKET_DIR
    t = next((x for x in json.loads((SITE / "kurul_takvimi_ozet.json").read_text(encoding="utf-8"))["kurullar"]
              if x["kurul"] == k), None)
    def tr_baslik(x: str) -> str:  # Türkçe: İ→i, I→ı küçült; kelime başı i→İ, ı→I büyüt ("ve" küçük)
        k_ = x.replace("İ", "i").replace("I", "ı").lower()
        return " ".join(w if w == "ve" else (w[0].replace("i", "İ").replace("ı", "I").upper() + w[1:]) for w in k_.split())
    ad = tr_baslik(t["ad"]) if t else ""
    COMMITTEE = f"Kurul {k} - {ad}" if ad else f"Kurul {k}"


def git_hedef() -> list[str]:
    ek = [f"src/data/summaries/kurul{k}.json" for k in range(2, 7)] + [f"src/data/ornek_sorular/k{k}" for k in range(2, 7)]
    return GIT_HEDEF + [x for x in ek if (MEDS / x).exists()]
STUDY = ROOT / "meds_temp" / "study"
DB2 = ROOT / "meds_database_v2"
LINKS = ROOT / "meds_database" / "derived" / "learn_links.json"
LINKS_ISCI = ROOT / "meds_database" / "derived" / "learn_links_ders_isci.json"
ORACLE = "medsor-oracle"
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
        # revize taslakları (cihaz, Yönetim → Yeni dersler → Revize): degistir | ekle | ikisini_tut
        self.kip = self.karar.get("islem") or "degistir"

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
        var = any(x.get("id") == b.get("deste_id") for x in oku(DECKS, []))
        if self.kip == "ekle" and var:
            self.hata.append("bu dersin yayında bir sürümü var: 'Yer değiştir' ya da 'Her ikisini tut' seç")
        if self.kip in ("degistir", "ikisini_tut") and not var and b.get("revize"):
            self.hata.append("yayında alternatif yok: 'Ekle' seç")
        if any(x.get("revizeIsId") == self.d.name for x in oku(DECKS, [])):
            self.hata.append("bu revize zaten yayında (aynı revize ikinci kez gönderilemez)")
        if k.get("karar") != "onayla":
            self.hata.append(f"karar onayla değil ({k.get('karar')})")
        if b.get("kurul") != KURUL:  # uygula() kurula_bagla ile bu kurula geçti; tutarsızlık = programlama hatası
            self.hata.append(f"kurul {b.get('kurul')} bu yayın turunun kurulu ({KURUL}) değil")
        den = oku(self.d / "denetim.json", {})
        if den.get("hata"):
            self.hata.append(f"işçi denetimi {den.get('hata')} HATA")
        self.n = int(b.get("numara") or 0)
        self.ders_id = b.get("ders_id") or ""
        self.deste_id = b.get("deste_id") or ""
        if p.get("id") != self.ders_id or self.deck.get("id") != self.deste_id or not re.fullmatch(rf"k{KURUL}p-{re.escape(self.ders_id)}(-v\d+)?", self.deste_id):
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
        if KURUL >= 2 and self.n not in mevcut:
            self.hata.append(f"Kurul {KURUL}: numara {self.n} ders kayıt defterinde yok (dersler/k{KURUL}.json)")
        self.kayit = {"is_id": self.d.name, "kurul": KURUL, "numara": self.n, "ders_id": self.ders_id,
                      "deste_id": self.deste_id, "ders": ders, "konu": konu, "hoca": p.get("ogretim_uyesi") or hoca,
                      "tarih": p.get("tarih") or tarih or "", "kaynak_idleri": [kaynak_id] if kaynak_id else [],
                      "pdf": b.get("pdf_yolu"), "mod": b.get("mod"),
                      "kaynak_md": f"meds_database_v2/ders_isci/yayinlanan/{self.d.name}/kaynak.md",
                      "onaylayan": k.get("kim"), "onay_zamani": k.get("zaman")}

        # deste
        tmp = self.yedek / "_deneme_deck.json"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps([self._deste()], ensure_ascii=False), encoding="utf-8")
        # Kurul 2+: Türkçe üslup + şık açıklama kapıları HATA (AGENTS.md 14). Toplu denetim (toplu_adimlar) bayraksız
        # kalır: Kurul 1 desteleri toplu düzeltilmez (KURUL2_YAPILMAYACAK_HATALAR.md).
        k2 = ["--kurul2"] if int(b.get("kurul") or 0) >= 2 else []
        r = subprocess.run([sys.executable, str(MEDS / "scripts" / "validate_learning_decks.py"), str(tmp), "--ozet"] + k2,
                           capture_output=True, text=True)
        tmp.unlink()
        if r.returncode != 0:
            self.hata.append("deste doğrulayıcı: " + r.stdout.strip().splitlines()[-1])
        if b.get("hafif"):  # hafif revize: yalnız V2 destesi + sözlük + bağlar; notu/soruları V1'inkiler kalır
            if self.kip != "ikisini_tut":
                self.hata.append("hafif revize yalnız 'Her ikisini tut' ile yayınlanır")
            self.sadakat = None
            return not self.hata
        # ders notu sadakati (işçinin PDF metnine karşı)
        md = (self.d / "ders_notu.md").read_text(encoding="utf-8")
        self.sadakat = s14.fidelity(md, _BosDerlem(), [], (self.d / "kaynak.md").read_text(encoding="utf-8"))
        # eşik: panel ayarı (işçi ayar.json · sadakat_esigi), yoksa s14; panelden "eşiği yok say" denen taslakta uygulanmaz
        esik = float((oku(L_TASLAK.parent / "ayar.json", {}) or {}).get("sadakat_esigi", s14.SADAKAT_ESIK))
        if self.sadakat < esik and not k.get("esik_atla"):
            self.hata.append(f"ders notu sadakati {self.sadakat} < {esik}")
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
        if self.kip == "ikisini_tut":
            grup = self.deste_id
            mevcut = [x for x in oku(DECKS, []) if x.get("id") == grup or x.get("versionGroup") == grup]
            n = max([int(str(x.get("versionLabel") or "V1")[1:] or 1) for x in mevcut] or [1]) + 1
            d.update({"id": f"{grup}-v{n}", "deckId": f"{grup}-v{n}", "versionGroup": grup, "versionLabel": f"V{n}", "revizeIsId": self.d.name,
                      "versionNote": "Revize ders işçisi (2026-27 PDF'inden yeniden üretildi)"})
        elif self.kip == "degistir":
            eski = next((x for x in oku(DECKS, []) if x.get("id") == self.deste_id), None)
            if eski and eski.get("versionGroup"):
                d.update({k: eski[k] for k in ("versionGroup", "versionLabel") if eski.get(k)})
            if self.b.get("revize"):
                d["revizeIsId"] = self.d.name
        return d

    # ------------------------------------------------------------------ 2. yazım
    def yaz(self):
        p, n, did = self.paket, self.n, self.ders_id
        md = (self.d / "ders_notu.md").read_text(encoding="utf-8") if (self.d / "ders_notu.md").exists() else ""
        deste = self._deste()
        self.son_deste = deste["id"]
        # deste
        decks = oku(DECKS, [])
        if self.kip == "ikisini_tut":
            for x in decks:
                if x.get("id") == self.deste_id:
                    x.setdefault("versionGroup", self.deste_id)
                    x.setdefault("versionLabel", "V1")
        yer = next((i for i, x in enumerate(decks) if x.get("id") == deste["id"]), None)
        if yer is None:
            decks.append(deste)
        else:
            decks[yer] = deste  # yer değiştir: listedeki sırası korunur
        self._yaz(DECKS, decks)
        if self.kip == "ikisini_tut":  # V1'in notu, paketi ve örnek soruları yerinde kalır; yalnız deste + sözlük + bağlar
            self._sozluk()
            self._baglar()
            return
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
        for f in ([] if self.d.resolve() == iz.resolve() else self.d.iterdir()):  # izden yeniden uygulamada kopya yok
            if f.is_file() and f.name not in ("oturum.json",):
                shutil.copy2(f, iz / f.name)
        # kayıt
        kayit = [y for y in oku(KAYIT, []) if y["ders_id"] != did]
        kayit.append(self.kayit | {"yayin_zamani": time.strftime("%Y-%m-%dT%H:%M:%S"), "sadakat": self.sadakat})
        self._yaz(KAYIT, sorted(kayit, key=lambda y: (y["kurul"], y["numara"])))

    def _not_kayitlari(self, md: str):
        k = self.kayit
        rec = {"id": self.ders_id, "kurul": KURUL, "committeeId": f"donem3-kurul{KURUL}", "discipline": k["ders"], "title": k["konu"],
               "instructor": k["hoca"] or "", "fileName": f"{self.n:02d}_{s14._slug(k['konu'])}.md", "keyPoints": s14._key_points(md),
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
        en[self.ders_id] = {"lessonTitle": k["konu"], "discipline": k["ders"], "instructor": k["hoca"] or "",
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
            var = g.get(key) or g.get(mevcut.get(norm_key(term), ""))
            if var and (var.get("dogrulama") or {}).get("is_id") != self.d.name:   # başkasının terimi: dokunma
                self.not_.append(f"sözlük: '{term}' zaten var, eklenmedi")
                continue
            if var:  # yeniden uygulama: aynı taslağın terimi aynı anahtarla yeniden yazılır
                key = mevcut.get(norm_key(term), key)
            kanit = t.get("kanit") or {}
            rec = {"term": term, "category": t.get("category") or "terim", "definition": t["definition"],
                   "description": t["definition"], "discipline": t.get("discipline") or k["ders"], "committee": ""}
            if t.get("pearl"):
                rec["clinicalPearl"] = t["pearl"]
            if t.get("aliases"):
                rec["aliases"] = t["aliases"]
            rec["dogrulama"] = {"durum": "ders_isci", "destek": 1.0, "uretici": "s13_study", "is_id": self.d.name}
            rec["kaynaklar"] = [{"chunk_id": None, "kaynak": k["pdf"], "ders": k["ders"], "kurul": KURUL,
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
            if z["pearl"].strip() not in eski:  # yeniden uygulamada ikinci kez eklenmez
                g[key]["clinicalPearl"] = (eski + " · " if eski else "") + z["pearl"].strip()
            fix_satir.append({"key": key, "pearl": g[key]["clinicalPearl"], "isci": {"is_id": self.d.name}})
        self._yaz(GLOSSARY, g, indent=2)
        for ad, satirlar in (("editor_glossary_new.jsonl", yeni_satir), ("editor_glossary_fix.jsonl", fix_satir)):
            f = STUDY / ad
            eski = [x for x in (f.read_text(encoding="utf-8") if f.exists() else "").splitlines() if x.strip()]
            # yeniden uygulamada aynı taslağın satırları tekrarlanmasın: bu is_id'nin eski satırları yenilerle değişir
            kalan = [x for x in eski if f'"is_id": "{self.d.name}"' not in x]
            if satirlar or len(kalan) != len(eski):
                self._yaz_metin(f, "".join(x + "\n" for x in kalan)
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


def kaynak_kimligi(pdf_yolu: str, manifest: dict | None) -> str | None:
    """Drive manifestinde PDF'in source_id'si (s14 kaynak kimliği). Yol karşılaştırması boşluklara duyarsız."""
    sade = lambda s: re.sub(r"\s+", "", s or "")  # noqa: E731
    for it in (manifest or {}).get("items", []):
        if sade(it.get("path")) == sade(pdf_yolu):
            return it.get("source_id")
    return None


def kaynak_kimligi_esnek(pdf_yolu: str, manifest: dict | None, ders_id: str = "") -> str | None:
    """Revize taslakları için: tam yol → Drive ad temizliği (':'→'_', boşluk) → aynı klasörde numara öneki
    olmadan başlık (tekilse) → aynı dersin önceki yayın kaydındaki kimlik. (Drive dosya adlarında ':' '_' olur
    ve numara önekleri yıllar arasında kayar: 26)Mesane ↔ 27)Mesane.)"""
    import unicodedata
    nfc = lambda x: unicodedata.normalize("NFC", x or "")  # noqa: E731
    yol = nfc(re.sub(r"^drive_root/", "", pdf_yolu or ""))
    items = [{**i, "path": nfc(i.get("path"))} for i in (manifest or {}).get("items", [])]
    if (k := kaynak_kimligi(yol, {"items": items})):
        return k
    sade = lambda s: re.sub(r"[\s:_]+", "", s or "").casefold()  # noqa: E731
    if (k := next((i.get("source_id") for i in items if sade(i["path"]) == sade(yol)), None)):
        return k
    klasor = lambda s: sade(s.rsplit("/", 1)[0]) if "/" in s else ""  # noqa: E731
    baslik = lambda s: sade(re.sub(r"^\d+\)\s*", "", s.rsplit("/", 1)[-1]))  # noqa: E731
    aday = [i.get("source_id") for i in items if klasor(i["path"]) == klasor(yol) and baslik(i["path"]) == baslik(yol)]
    if len(set(aday)) == 1:
        return aday[0]
    # H88: Drive'da klasör yeniden adlandırılmış olabilir (Patoloji → Tıbbi Patoloji) ve '/' içeren ad alt klasör gibi
    # görünür: tam dosya yolu (klasör hariç) ya da numarasız başlık manifestte TEKSE onu kullan.
    kuyruk = lambda s: sade(s.split("/", 2)[-1]) if s.count("/") >= 2 else sade(s)  # noqa: E731  (Kurul N/<branş>/ sonrası)
    aday = [i.get("source_id") for i in items if kuyruk(i["path"]) == kuyruk(yol)]
    if len(set(aday)) == 1:
        return aday[0]
    return next((y["kaynak_idleri"][0] for y in oku(KAYIT, []) if ders_id and y.get("ders_id") == ders_id
                 and y.get("kaynak_idleri")), None)


def yayin_kaydi_bul(is_id: str, kaynak: list[dict]) -> str | None:
    return next((y["kaynak_idleri"][0] for y in kaynak if y["is_id"] == is_id and y.get("kaynak_idleri")), None)


def git_kirli() -> list[str]:
    r = subprocess.run(["git", "status", "--porcelain", "--", *git_hedef()], cwd=MEDS, capture_output=True, text=True)
    return [x for x in r.stdout.splitlines() if x.strip()]


def uygula(dizinler: list[Path], kimlik, deneme: bool = False) -> tuple[list[Yayin], list[Yayin]]:
    """Denetle + yaz. `kimlik(Yayin) -> source_id`. Dönüş: (yazılanlar, denetimden kalanlar)."""
    yedek = YEDEK / time.strftime("%Y%m%d_%H%M%S")
    ok_, red = [], []
    # Tek kurul: s14/s16 modül durumu kurula bağlı. En küçük kurul işlenir, diğerleri sonraki turda (10 dk).
    kurullar = {d: int((oku(d / "baglam.json", {}) or {}).get("kurul") or 1) for d in dizinler}
    if kurullar:
        k = min(kurullar.values())
        ertelenen = [d.name for d, x in kurullar.items() if x != k]
        if ertelenen:
            print(f"Kurul {k} işleniyor; sonraki tura kalan:", ertelenen)
        kurula_bagla(k)
        dizinler = [d for d in dizinler if kurullar[d] == k]
    for d in dizinler:
        y = Yayin(d, deneme, yedek)
        # sınama dersi (2026-10-24, kullanıcı kararı): Drive'a konmayan geçen yıl PDF'i — kaynak kimliği PDF özetinden;
        # deste "sinama" etiketini taşır (sitede "Sınama" etiketiyle herkese açık). Gerçek PDF gelince aynı dersi günceller.
        sinama = (y.b.get("sinama") or {}) if isinstance(y.b.get("sinama"), dict) else {}
        ok = y.denetle(f"sinama-{sinama['sha256'][:12]}" if sinama.get("sha256") else kimlik(y))
        if sinama and isinstance(getattr(y, "deck", None), dict):
            y.deck["sinama"] = {"etiket": "Sınama", "aciklama": sinama.get("aciklama") or "Geçen yılın slaytından hazırlanmış sınama dersi."}
        print(f"== {d.name} · {y.b.get('ders_id')} · sadakat {getattr(y, 'sadakat', '?')} · "
              f"{'DENETİM TAMAM' if ok else 'DENETİM HATALI'}")
        for h in y.hata:
            print("  HATA", h)
        if not ok:
            red.append(y)
            continue
        if deneme:
            continue
        y.yaz()
        for x in y.not_:
            print("  ·", x)
        ok_.append(y)
    if ok_:
        print("yedek:", yedek)
    eski = sorted(x for x in YEDEK.glob("2*") if x.is_dir())
    for x in eski[:-5]:  # yedeklerin son 5'i tutulur (her biri ~100 MB)
        shutil.rmtree(x, ignore_errors=True)
    return ok_, red


def toplu_adimlar(sonuc: list[Yayin]) -> bool:
    """Tüm desteler doğrulayıcıdan geçmeli; örnek sorular yalnız bu dersler için siteye (upsert)."""
    r = subprocess.run([sys.executable, str(MEDS / "scripts" / "validate_learning_decks.py"), "--ozet"],
                       capture_output=True, text=True, cwd=MEDS)
    print("deste doğrulayıcı:", (r.stdout.strip().splitlines() or ["?"])[-1])
    if r.returncode != 0:
        return False
    rapor = s16.build(export=False)  # yalnız meds_database_v2/ornek_sorular_k1 — site toptan yazılmaz
    sorunlu = [y.ders_id for y in sonuc if rapor.get(y.ders_id) is None or rapor.get(y.ders_id)]
    if sorunlu:
        print("örnek sorular siteye AKTARILMADI (s16 denetimi):", sorunlu)
    s16.disa_aktar([y.ders_id for y in sonuc if y.ders_id not in sorunlu])
    return True


# ---------------------------------------------------------------------------------------------- Oracle
def _kilit():
    import fcntl
    f = open(KILIT, "w")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return None
    return f


def _bildir(baslik: str, ayrinti: str):
    import urllib.request
    h = {"Content-Type": "application/json"}
    for satir in (MEDS / ".env").read_text(encoding="utf-8").splitlines() if (MEDS / ".env").exists() else []:
        if satir.startswith("MEDSORU_API_PASSWORD="):
            h["X-API-Password"] = satir.split("=", 1)[1].strip().strip('"')
    body = {"targetType": "pipeline", "targetId": "ders-isci-yayin", "reason": baslik, "details": ayrinti,
            "reportedBy": "Ders işçisi"}
    try:
        urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:3000/api/universal-report",
                                                      json.dumps(body).encode(), h), timeout=30)
    except Exception as e:  # noqa: BLE001
        print("bildirim gönderilemedi:", e)


def _env(ad: str) -> str:
    for satir in (MEDS / ".env").read_text(encoding="utf-8").splitlines() if (MEDS / ".env").exists() else []:
        if satir.startswith(ad + "="):
            return satir.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def _pdf_eslesme_yenile() -> str:
    """H56 (2026-10-24, k2-07): deste → ders PDF eşlemesi yalnız işçinin Drive taramasında (50 dk) yenileniyordu; yeni
    ders o arada uygulamada PDF'siz açılıyordu. Yayından hemen sonra aynı eşleyici işçi kapsayıcısında koşar
    (PyMuPDF + indirme klasörüne yazma orada; çıktı DOWNLOADS/_deck_pdf_sources.json, sunucu yenisini okur)."""
    try:
        r = subprocess.run(["docker", "exec", "meds-ders-isci", "python3", "-c",
                            "import sys; sys.path.insert(0, '/app/scripts/ders_isci'); import izle; izle.pdf_eslesme_guncelle()"],
                           capture_output=True, text=True, timeout=1200)
    except Exception as e:  # noqa: BLE001  (işçi taramasında yine yenilenir)
        return f"çalışmadı ({e}); bir sonraki Drive taramasında yenilenecek"
    return "yenilendi" if r.returncode == 0 else f"hata {r.returncode}: {(r.stderr or r.stdout)[-300:]}"


def _canli_ders_ekle(y) -> str:
    """Yayınlanan dersi canlı derse ekler (sunucu: POST /api/sesli-anlatim/ders-ekle): konuşma metni, ders listesi,
    PDF hizalaması (konusma_sayfalari.json) ve iki ses işi — Emel (varsayılan) + EMA. Metin yoksa atlanır.
    Döner: tek satırlık sonuç (bildirime eklenir)."""
    import urllib.request
    f = y.d / "konusma_metni.md"
    if not f.exists():
        return f"{y.ders_id}: konuşma metni yok (canlı derse eklenmedi)"
    b = oku(y.d / "baglam.json", {}) or {}
    v2 = y.d / "konusma_v2.json"  # Kurul 2+: cümle kimlikli metin → data/sesli_anlatim/v2/<anahtar>.json (deeplink /k/<id>)
    if v2.exists():
        hedef = MEDS / "data" / "sesli_anlatim" / "v2" / f"{y.ders_id}.json"
        hedef.parent.mkdir(parents=True, exist_ok=True)
        d2 = json.loads(v2.read_text(encoding="utf-8")); d2["anahtar"] = y.ders_id
        hedef.write_text(json.dumps(d2, ensure_ascii=False, indent=1), encoding="utf-8")
        # sesli ders ekranının vurguları (önemli cümle + terim) v2 vurgu kodlarından (vurgu_uret.py Kurul 1'e bağlı)
        sys.path.insert(0, str(MEDS / "scripts" / "sesli_anlatim"))
        import konusma_v2 as _kv
        vy = MEDS / "data" / "sesli_anlatim" / "vurgu" / f"{y.ders_id}.json"
        vy.parent.mkdir(parents=True, exist_ok=True)
        vy.write_text(json.dumps(_kv.vurgu_turet(d2), ensure_ascii=False), encoding="utf-8")
    yol = b.get("pdf_yolu") or ""
    indirilen = oku(ROOT / "meds_downloads" / "_downloads.json", {}) or {}
    file_id = next((fid for fid, v in indirilen.items() if isinstance(v, dict) and v.get("path") == f"drive_root/{yol}"), None)
    govde = {"key": y.ders_id, "no": y.kayit.get("numara"), "baslik": y.kayit.get("konu") or b.get("program", {}).get("konu"),
             "metin": f.read_text(encoding="utf-8"), "sayfalar": oku(y.d / "konusma_sayfalari.json", []) or [],
             "deckId": y.deste_id,
             # Kurul 2+: cümle başına slayt çapası (konusma_v2.py --turet) → canlı derste kelime kelime PDF işareti
             "capalar": oku(y.d / "konusma_capalari.json", None),
             "dosya": {"path": yol, "name": b.get("pdf_adi") or Path(yol).name, "pages": b.get("sayfa"), "fileId": file_id}}
    h = {"Content-Type": "application/json", "x-panel-secret": _env("MEDS_PANEL_SECRET")}
    if _env("MEDSORU_API_PASSWORD"):
        h["X-API-Password"] = _env("MEDSORU_API_PASSWORD")
    try:
        with urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:3000/api/sesli-anlatim/ders-ekle",
                                                           json.dumps(govde).encode(), h), timeout=60) as r:
            c = json.loads(r.read() or b"{}")
        return (f"{y.ders_id}: canlı derse {'eklendi' if c.get('yeni') else 'güncellendi'} · {c.get('paragraf')} paragraf · "
                f"PDF hizalaması {c.get('hizalama')} · {len(c.get('isler') or [])} ses işi (Emel + EMA)")
    except Exception as e:  # noqa: BLE001
        return f"{y.ders_id}: canlı derse eklenemedi ({e})"


def _site_derle() -> bool:
    c = ["docker", "compose", "--env-file", str(MEDS / ".env"), "-f", str(MEDS / "deploy" / "oracle" / "docker-compose.oracle.yml")]
    for adim in (["build", "-q", "meds-app"], ["up", "-d", "--no-deps", "meds-app"]):
        r = subprocess.run(["nice", *c, *adim], cwd=MEDS, capture_output=True, text=True)
        if r.returncode != 0:
            print("meds-app derleme hatası:", r.stderr[-1500:])
            return False
    for _ in range(60):
        if subprocess.run(["curl", "-sf", "-m", "5", "http://127.0.0.1:3000/api/health"], capture_output=True).returncode == 0:
            return True
        time.sleep(2)
    print("sağlık kontrolü geçmedi")
    return False


def sunucu() -> int:
    kilit = _kilit()
    if not kilit:
        print("başka dağıtım/yayın sürüyor; sonraki turda")
        return 0
    asil = oku(DURUM_KAYIT, []) or []
    repo = {y["is_id"] for y in oku(KAYIT, [])}
    # 1) cihazdan yapılan dağıtım repo kopyasındaki yayını ezdiyse: izden yeniden uygula
    yeniden = [DB2 / "ders_isci" / "yayinlanan" / y["is_id"] for y in asil if y["is_id"] not in repo]
    # 2) yeni onaylar
    yeni = []
    for d in sorted(L_TASLAK.glob("*")):
        k = oku(d / "karar.json", {}) or {}
        if d.is_dir() and k.get("karar") == "onayla" and not (d / "yayin.json").exists() \
                and d.name not in repo and d.name not in {y["is_id"] for y in asil}:
            hedef = ONAYLANAN / d.name
            if hedef.exists():
                shutil.rmtree(hedef)
            shutil.copytree(d, hedef, ignore=shutil.ignore_patterns("oturum.json", "oturum_sesli.json"))
            yeni.append(hedef)
    derle_iste = L_TASLAK / "derle_iste.json"
    if not yeniden and not yeni:
        if not derle_iste.exists():
            return 0
        # panelden "Siteyi yeniden derle": yayınlanmış ama site derlemesi düşmüş taslaklar
        derle_iste.unlink(missing_ok=True)
        derlendi = _site_derle()
        for t in L_TASLAK.glob("*"):
            yp = t / "yayin.json"
            yv = oku(yp, None) if t.is_dir() else None
            if yv and yv.get("durum") == "yayinlandi" and yv.get("site_derlendi") is False:
                yaz_json(yp, yv | {"site_derlendi": derlendi})
        _bildir("Site yeniden derlendi" if derlendi else "Site yine derlenemedi", "Panelden istenen yeniden derleme.")
        return 0 if derlendi else 4
    derle_iste.unlink(missing_ok=True)
    manifest = oku(L_MANIFEST, {})
    print(time.strftime("[%Y-%m-%d %H:%M:%S]"), "yeniden uygulanacak:", [d.name for d in yeniden],
          "yeni:", [d.name for d in yeni])
    sonuc, red = uygula([d for d in yeniden if d.is_dir()] + yeni,
                        lambda y: yayin_kaydi_bul(y.d.name, asil) or kaynak_kimligi_esnek(y.b.get("pdf_yolu") or "", manifest, y.b.get("ders_id") or ""))  # H88
    for y in red:  # denetimden geçmeyen onaylı taslak: yöneticiye bildir, bir daha denenmesin diye işaretle
        if y.d.parent == ONAYLANAN:
            yaz_json(L_TASLAK / y.d.name / "yayin.json", {"durum": "denetim_hatasi", "hatalar": y.hata[:20],
                                                           "zaman": time.strftime("%Y-%m-%dT%H:%M:%S")})
            _bildir("Onaylanan ders yayınlanamadı", f"{y.d.name} · {y.ders_id}: " + "; ".join(y.hata[:5]))
    if not sonuc:
        return 1 if red else 0
    if not toplu_adimlar(sonuc):
        _bildir("Ders yayını durdu", "Deste doğrulayıcı tüm destelerde 0 HATA vermedi; yedekten geri alınabilir.")
        return 3
    derlendi = _site_derle()
    for y in sonuc:
        asil = [x for x in asil if x["is_id"] != y.d.name] + [y.kayit | {"yayin_zamani": time.strftime("%Y-%m-%dT%H:%M:%S")}]
        if y.d.parent == ONAYLANAN:
            t = L_TASLAK / y.d.name
            yaz_json(t / "yayin.json", {"durum": "yayinlandi", "yayin_zamani": time.strftime("%Y-%m-%dT%H:%M:%S"),
                                        "ders_id": y.ders_id, "deste_id": y.deste_id, "site_derlendi": derlendi})
            yaz_json(t / "durum.json", (oku(t / "durum.json", {}) or {}) | {"durum": "yayinlandi", "zaman": time.time()})
    yaz_json(DURUM_KAYIT, sorted(asil, key=lambda y: (y["kurul"], y["numara"])))
    yeni_adlar = [f"{y.kayit['konu']} ({y.ders_id})" for y in sonuc if y.d.parent == ONAYLANAN]
    # canlı ders (2026-10-16): yeni onaylanan derslerin konuşma metni + Emel/EMA sesi; site derlendikten sonra (meds-app
    # yeniden kurulurken kuyruğa alınan ses işi yarıda kalmasın)
    canli = [_canli_ders_ekle(y) for y in sonuc if y.d.parent == ONAYLANAN] if derlendi else []
    for c in canli:
        print("canlı ders:", c)
    if yeni_adlar:
        print("PDF eşleşmesi:", _pdf_eslesme_yenile())
    if yeni_adlar:
        _bildir("Ders yayınlandı" if derlendi else "Ders yayınlandı, site derlenemedi",
                "Sitede: " + ", ".join(yeni_adlar) + ("" if derlendi else " — meds-app derlemesi başarısız, kayıtlara bakın.")
                + ("\nCanlı ders: " + "; ".join(canli) if canli else ""))
    return 0 if derlendi else 4


# ---------------------------------------------------------------------------------------------- cihaz
def esitle() -> int:
    """Oracle'da yayınlanan dersleri yerel kaynaklara işler (dağıtımdan önce zorunlu). 0 = eşit."""
    r = ssh(f"cat {DURUM_KAYIT}")
    if r.returncode != 0:
        print("Oracle yayın defteri okunamadı:", r.stderr.strip()[:200])
        return 5
    asil = json.loads(r.stdout or "[]")
    yerel = {y["is_id"] for y in oku(KAYIT, [])}
    eksik = [y for y in asil if y["is_id"] not in yerel]
    if not eksik:
        print("yayınlar eşit:", len(asil), "ders")
        return 0
    kirli_once = git_kirli()
    ONAYLANAN.mkdir(parents=True, exist_ok=True)
    for y in eksik:
        subprocess.run(["rsync", "-a", "--delete", f"{ORACLE}:/home/ubuntu/medsor/meds_database_v2/ders_isci/yayinlanan/{y['is_id']}/",
                        str(ONAYLANAN / y["is_id"]) + "/"], check=True)
    sonuc, red = uygula([ONAYLANAN / y["is_id"] for y in eksik], lambda yy: yayin_kaydi_bul(yy.d.name, asil))
    if red or not sonuc or not toplu_adimlar(sonuc):
        print("EŞİTLENEMEDİ — dağıtım yapma")
        return 6
    subprocess.run(["npm", "run", "-s", "decks:packages"], cwd=MEDS, check=False)
    if kirli_once:
        print("Hedef dosyalarda başka değişiklikler vardı; commit ATILMADI (elle commit'le):", *kirli_once, sep="\n  ")
    else:
        mesaj = "ders işçisi: Oracle yayınları eşitlendi — " + ", ".join(y.ders_id for y in sonuc)
        subprocess.run(["git", "add", "--", *git_hedef()], cwd=MEDS, check=True)
        subprocess.run(["git", "commit", "-q", "-m", mesaj + "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>",
                        "--", *git_hedef()], cwd=MEDS, check=False)
    print("eşitlendi:", [y.ders_id for y in sonuc])
    return 0


def yerel(is_id: str, deneme: bool = False) -> int:
    """Revize taslağı (cihazda üretildi) yerel kaynaklara yayınlar; karar.json'daki `islem` kipini uygular.
    Sonuç taslak/<is>/yayin.json'a yazılır. Commit/dağıtım yapmaz."""
    d = ROOT / "ders_isci" / "taslak" / is_id
    if not (d / "baglam.json").exists():
        print("taslak yok:", d)
        return 2
    # Aynı kaynak dosyalara (107 MB deste json'u, sözlük, kayıt) yazan eşzamanlı yayınlar birbirinin
    # yazdığını eziyordu (panel sırası + başka oturumun betiği) → tüm yerel yayınlar tek kilitle sıralanır.
    import fcntl
    kilit = open(ROOT / "ders_isci" / ".yayin.lock", "w")
    fcntl.flock(kilit, fcntl.LOCK_EX)
    zaman = time.strftime("%Y-%m-%dT%H:%M:%S")
    yayinda = next((x for x in oku(DECKS, []) if x.get("revizeIsId") == is_id), None)
    if yayinda and not deneme:  # önceki çalıştırma desteyi yazıp durum kaydını bitiremeden kesilmiş: kaydı onar
        yaz_json(d / "yayin.json", (oku(d / "yayin.json", {}) or {}) | {"durum": "yayinlandi", "deste_id": yayinda["id"],
                                                                       "onarildi": zaman})
        yaz_json(d / "durum.json", (oku(d / "durum.json", {}) or {}) | {"durum": "yayinlandi", "zaman": time.time()})
        print("zaten yayında (kayıt onarıldı):", yayinda["id"])
        return 0
    manifest = oku(DOWNLOADS_MANIFEST, {})
    kimlik = lambda y: kaynak_kimligi_esnek(y.b.get("pdf_yolu") or "", manifest, y.b.get("ders_id") or "")  # noqa: E731
    sonuc, red = uygula([d], kimlik, deneme=deneme)
    if red:
        yaz_json(d / "yayin.json", {"durum": "denetim_hatasi", "hatalar": red[0].hata[:20], "zaman": zaman})
        return 1
    if deneme:
        return 0
    ok = toplu_adimlar(sonuc)
    subprocess.run(["npm", "run", "-s", "decks:packages"], cwd=MEDS, check=False, capture_output=True)
    y = sonuc[0]
    yaz_json(d / "yayin.json", {"durum": "yayinlandi" if ok else "dogrulayici_hatasi", "yayin_zamani": zaman, "kip": y.kip,
                                "deste_id": getattr(y, "son_deste", None), "yazilan": y.yazilan})
    yaz_json(d / "durum.json", (oku(d / "durum.json", {}) or {}) | {"durum": "yayinlandi" if ok else "yayin_hatasi",
                                                                   "zaman": time.time()})
    return 0 if ok else 3


def esitle_ve_hastaliklar() -> int:
    r = esitle()
    if r == 0:
        hastaliklari_uygula()  # başka oturum diseases.json'u bitirince ilk dağıtımda kendiliğinden eklenir
    return r


DISEASES = SITE / "diseases.json"
HASTALIK_ONERI = DB2 / "ders_isci" / "hastalik_onerileri" / "sema2"
HASTALIK_UYGULANAN = DB2 / "ders_isci" / "hastalik_onerileri" / "uygulanan.json"


def _hastalik_hata() -> int | None:
    r = subprocess.run([sys.executable, str(MEDS / "scripts" / "diseases" / "hastalik_profilleri.py"), "denetle"],
                       capture_output=True, text=True, cwd=MEDS, env=os.environ | {"HASTALIK_DOGRULAMA_ZORUNLU": "0"})
    m = re.search(r"·\s*(\d+)\s*HATA", r.stdout)
    return int(m.group(1)) if m else None


def hastaliklari_uygula() -> int:
    """Şema 2'ye çevrilmiş hastalık önerilerini (sema2/<id>.json) src/data/diseases.json'a upsert eder (cihaz).
    diseases.json'da commit'lenmemiş değişiklik varsa (başka oturum çalışıyor) BEKLER; denetim hatası artarsa geri alır."""
    import hashlib
    dosyalar = sorted(HASTALIK_ONERI.glob("*.json")) if HASTALIK_ONERI.is_dir() else []
    uyg = oku(HASTALIK_UYGULANAN, {}) or {}
    bekleyen = [f for f in dosyalar if uyg.get(f.stem) != hashlib.sha1(f.read_bytes()).hexdigest()]
    if not bekleyen:
        return 0
    kirli = subprocess.run(["git", "status", "--porcelain", "--", "src/data/diseases.json"], cwd=MEDS,
                           capture_output=True, text=True).stdout.strip()
    if kirli:
        print(f"hastalık önerileri ({len(bekleyen)}) BEKLİYOR: diseases.json'da commit'lenmemiş değişiklik var (başka oturum)")
        return 0
    once = _hastalik_hata()
    yedek = YEDEK / ("hastalik_" + time.strftime("%Y%m%d_%H%M%S"))
    yedek.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DISEASES, yedek / DISEASES.name)
    kayitlar = oku(DISEASES, [])
    sira = {r.get("id"): i for i, r in enumerate(kayitlar)}
    for i, r in enumerate(kayitlar):  # başka oturum kayıtları birleştirdiyse eski kimlik `aliases`'ta yaşar
        for e in r.get("aliases") or []:
            sira.setdefault(e, i)
    simdi = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for f in bekleyen:
        yeni = json.loads(f.read_text(encoding="utf-8"))
        eski = kayitlar[sira[yeni["id"]]] if yeni["id"] in sira else None
        if eski and eski.get("id") != yeni["id"]:  # birleştirilmiş kayıt: onun kimliğiyle güncelle
            yeni = yeni | {"id": eski["id"], "aliases": [*(yeni.get("aliases") or []), yeni["id"]]}
        if eski:  # mevcut kayıt: oluşturma zamanı, ders bağları, eş adlar korunur
            yeni["createdAt"] = eski.get("createdAt") or simdi
            yeni["relatedLectures"] = list(dict.fromkeys([*(eski.get("relatedLectures") or []), *(yeni.get("relatedLectures") or [])]))
            for alan in ("aliases", "altNames"):
                yeni[alan] = list(dict.fromkeys([*(eski.get(alan) or []), *(yeni.get(alan) or [])]))
            for alan in ("icd_code",):
                yeni.setdefault(alan, eski.get(alan))
            kayitlar[sira[yeni["id"]]] = yeni | {"updatedAt": simdi}
        else:
            yeni.setdefault("aliases", [])
            yeni.setdefault("altNames", [])
            kayitlar.append(yeni | {"createdAt": simdi, "updatedAt": simdi})
            sira[yeni["id"]] = len(kayitlar) - 1
    yaz_json(DISEASES, kayitlar)
    sonra = _hastalik_hata()
    if sonra is None or (once is not None and sonra > once):
        shutil.copy2(yedek / DISEASES.name, DISEASES)
        print(f"hastalık önerileri GERİ ALINDI: denetim hatası {once} → {sonra}")
        return 7
    for f in bekleyen:
        uyg[f.stem] = hashlib.sha1(f.read_bytes()).hexdigest()
    yaz_json(HASTALIK_UYGULANAN, uyg)
    subprocess.run(["git", "commit", "-q", "-m", f"hastalıklar: ders işçisi önerileri eklendi ({len(bekleyen)} profil: "
                    + ", ".join(f.stem for f in bekleyen)[:300] + ")\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>",
                    "--", "src/data/diseases.json"], cwd=MEDS, check=False)
    print(f"hastalık önerileri eklendi: {len(bekleyen)} profil (denetim {once} → {sonra} HATA)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sunucu", action="store_true", help="Oracle: onaylıları yayınla + site derle (timer)")
    ap.add_argument("--esitle", action="store_true", help="cihaz: Oracle yayınlarını yerel kaynaklara işle")
    ap.add_argument("--hastaliklar", action="store_true", help="cihaz: şema 2 hastalık önerilerini diseases.json'a ekle")
    ap.add_argument("--deneme", action="store_true", help="cihaz: --is taslağını yalnız denetle")
    ap.add_argument("--is", dest="tek")
    ap.add_argument("--yerel", action="store_true", help="cihaz: ders_isci/taslak/<is> revize taslağını yerelde yayınla")
    a = ap.parse_args()
    if a.sunucu:
        if not SUNUCU:
            print("--sunucu yalnız Oracle'da çalışır")
            return 2
        return sunucu()
    if a.esitle:
        return esitle_ve_hastaliklar()
    if a.hastaliklar:
        return hastaliklari_uygula()
    if a.yerel and a.tek:
        return yerel(a.tek, a.deneme)
    if a.deneme and a.tek:
        hedef = ONAYLANAN / a.tek
        subprocess.run(["rsync", "-a", "--delete", f"{ORACLE}:{L_TASLAK}/{a.tek}/", str(hedef) + "/"], check=True)
        r = ssh(f"cat {L_MANIFEST}")
        manifest = json.loads(r.stdout) if r.returncode == 0 else {}
        uygula([hedef], lambda y: kaynak_kimligi_esnek(y.b.get("pdf_yolu") or "", manifest, y.b.get("ders_id") or ""), deneme=True)
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
