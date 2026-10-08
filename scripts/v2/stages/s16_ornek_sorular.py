"""Kurul 1 örnek soruları: kazanım temelli, ders paketine (özet + bilgi paketi) dayalı.

prepare  → her ders için yazım kiti: müfredat kazanımları (K1..Kn), kazanıma bağlı bilgi paketi
           maddeleri, ders özeti ve anlamca en yakın Dönem 3 çıkmış soruları (kazanım bazında).
           Çıktı: meds_temp/study/ornek/kits/<id>.md + baglar.json (kazanım → çıkmış soru id).
build    → meds_temp/study/ornek/sorular/<id>.json (editör yazımı) dosyalarını denetler:
           şema, kazanım başına 3-10 soru, en az bir kolay/orta/zor, fazlası çoğunlukla orta,
           her şık için açıklama, çıkmış soruyla birebir benzerlik. Sorunsuz dersler
           meds_database_v2/ornek_sorular_k1/ altına yazılır; --export ile site verisine
           (src/data/ornek_sorular/k1/) kopyalanır.
"""
from __future__ import annotations

import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime

from .. import config

PAKET_DIR = config.PROJECT_ROOT / "meds_database_v2" / "kurul1_ders_paketleri"
SORU_DIR = config.PROJECT_ROOT / "meds_database_v2" / "questions"
WORK = config.TEMP_DIR / "study" / "ornek"
KIT_DIR = WORK / "kits"
YAZIM_DIR = WORK / "sorular"
OUT_DIR = config.PROJECT_ROOT / "meds_database_v2" / "ornek_sorular_k1"
SITE_DIR = config.MEDS_DIR / "src" / "data" / "ornek_sorular" / "k1"

HARFLER = "ABCDE"
ZORLUK = ("kolay", "orta", "zor")
_DUR = set("""ve ile veya bir bu şu o da de ki için gibi olan olarak daha en çok az ise hangisi hangisidir
aşağıdakilerden aşağıdaki doğru yanlış değildir değil mi mu olur olması olup sonra önce kadar göre
ilgili ilişkin her tüm bazı sık genellikle yer alır alan""".split())


def _fold(s: str) -> str:
    s = (s or "").replace("İ", "i").replace("I", "ı").lower()
    s = s.translate(str.maketrans("çğıöşü", "cgiosu"))
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def _terimler(s: str) -> list[str]:
    out = []
    for w in re.findall(r"[a-z0-9]+", _fold(s)):
        if len(w) < 4 or w in {_fold(x) for x in _DUR}:
            continue
        out.append(w[:5])
    return out


def _paketler() -> list[dict]:
    sira = {x["id"]: x["sira"] for x in json.loads((PAKET_DIR / "index.json").read_text(encoding="utf-8"))}
    out = []
    for p in sorted(PAKET_DIR.glob("k1-*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        d["sira"] = sira.get(d["id"], 0)
        out.append(d)
    return out


def _cikmislar() -> list[dict]:
    rows = []
    for f in sorted(SORU_DIR.glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            d = json.loads(line)
            if d.get("donem") != 3 or not d.get("stem"):
                continue
            rows.append(d)
    # aynı sorunun kopyalarını tek kayda indir (normalize kök + şıklar)
    seen, out = set(), []
    for d in sorted(rows, key=lambda r: (r.get("answer") is None, -len(r.get("seen_in") or []))):
        key = " ".join(_terimler(d["stem"]))[:160]
        if key in seen:
            continue
        seen.add(key)
        out.append(d)
    return out


def _kazanim_esle(kazanimlar: list[str], metin: str) -> int:
    """Bilgi paketi maddesinin kazanım metnini (yeniden ifade edilmiş olabilir) en yakın kazanıma bağlar."""
    a = set(_terimler(metin))
    best, idx = -1.0, 0
    for i, k in enumerate(kazanimlar):
        b = set(_terimler(k))
        s = len(a & b) / (len(a | b) or 1)
        if s > best:
            best, idx = s, i
    return idx


def _idf(belgeler: list[list[str]]) -> dict[str, float]:
    df = Counter()
    for b in belgeler:
        df.update(set(b))
    n = len(belgeler)
    return {t: math.log((n + 1) / (c + 0.5)) for t, c in df.items()}


def _soru_metni(q: dict) -> str:
    opts = q.get("options") or {}
    return q["stem"] + " " + " ".join(str(v) for v in opts.values())


def prepare(ders: str | None = None) -> dict:
    KIT_DIR.mkdir(parents=True, exist_ok=True)
    YAZIM_DIR.mkdir(parents=True, exist_ok=True)
    paketler = _paketler()
    cik = _cikmislar()
    cik_ter = [_terimler(_soru_metni(q)) for q in cik]
    idf = _idf(cik_ter + [_terimler(p["ders_ozeti"]["ozet"]) for p in paketler])

    avg = sum(len(t) for t in cik_ter) / len(cik_ter)
    cik_tf = [Counter(t) for t in cik_ter]

    def skor(sorgu: Counter, i: int) -> float:
        """BM25 (k1=1.2, b=0.9): uzun soruların baskınlığını kırar."""
        tf, n, s = cik_tf[i], len(cik_ter[i]), 0.0
        for k, w in sorgu.items():
            if k in tf:
                s += min(w, 3) * idf.get(k, 0) * tf[k] * 2.2 / (tf[k] + 1.2 * (0.1 + 0.9 * n / avg))
        return s

    baglar = {}
    for p in paketler:
        if ders and p["ders"] != ders:
            continue
        kaz = p["kazanimlar"]
        gruplar = defaultdict(list)
        for b in p["bilgi_paketi"]:
            gruplar[_kazanim_esle(kaz, b.get("kazanim", ""))].append(b)
        konu_q = Counter(_terimler(p["konu"]) * 3 + _terimler(" ".join(b["bilgi"] for b in p["bilgi_paketi"])) * 2
                         + _terimler(" ".join(p["kazanimlar"])))
        konu_skor = [skor(konu_q, i) * (1.3 if cik[i].get("kurul") in (1, "final", "butunleme", "but") else 1.0)
                     for i in range(len(cik))]
        esik = sorted(konu_skor, reverse=True)[min(50, len(konu_skor) - 1)]
        aday = [i for i, s in enumerate(konu_skor) if s >= esik and s > 0]
        kaz_bag = {}
        for ki, k in enumerate(kaz):
            sorgu = Counter(_terimler(k) * 2 + _terimler(" ".join(f"{b['bilgi']} {b['anlam']}" for b in gruplar[ki])))
            sirali = sorted(aday, key=lambda i: -(skor(sorgu, i) + 0.3 * konu_skor[i]))
            kaz_bag[f"K{ki + 1}"] = [cik[i]["question_id"] for i in sirali[:5]]
        baglar[p["id"]] = {"konu_cikmis": [cik[i]["question_id"] for i in sorted(aday, key=lambda i: -konu_skor[i])[:35]],
                           "kazanim_cikmis": kaz_bag}

        by_id = {q["question_id"]: q for q in cik}
        L = [f"# KİT · {p['sira']:02d} · {p['konu']}", f"Ders: {p['ders']} | Öğretim üyesi: {p['ogretim_uyesi']} | id: {p['id']}", ""]
        L.append("## KAZANIMLAR")
        for ki, k in enumerate(kaz):
            L.append(f"- K{ki + 1}: {k}")
        L.append("\n## BİLGİ PAKETİ (kazanıma göre)")
        for ki, k in enumerate(kaz):
            L.append(f"### K{ki + 1}: {k}")
            for b in gruplar[ki]:
                L.append(f"- [{b['no']}] {b['bilgi']}: {b['anlam']} → {b['sonuc']}")
        L.append("\n## DERS ÖZETİ")
        L.append(p["ders_ozeti"]["ozet"])
        if p.get("anahtar_noktalar"):
            L.append("\n## ANAHTAR NOKTALAR")
            L.extend(f"- {x}" for x in p["anahtar_noktalar"])
        for qid in baglar[p["id"]]["konu_cikmis"]:
            q = by_id[qid]
            opts = " | ".join(f"{k}) {v}" for k, v in (q.get("options") or {}).items())
            L.append(f"- ({qid}) [K{q.get('kurul')}] {' '.join(q['stem'].split())} || {' '.join(opts.split())} || cevap: {q.get('answer') or '?'}")
        (KIT_DIR / f"{p['id']}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (WORK / "baglar.json").write_text(json.dumps(baglar, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"kit": len(baglar), "cikmis_havuz": len(cik)}


def _benzerlik(a: str, b: str) -> float:
    x, y = set(_terimler(a)), set(_terimler(b))
    return len(x & y) / (len(x | y) or 1)


def _denetle(p: dict, d: dict, cik: list[dict], tum_cik: set[str]) -> list[str]:
    sorun = []
    kaz = p["kazanimlar"]
    sayac = defaultdict(list)
    for q in d.get("sorular", []):
        qid = q.get("id", "?")
        kn = q.get("kazanim")
        if not isinstance(kn, int) or not 1 <= kn <= len(kaz):
            sorun.append(f"{qid}: geçersiz kazanım {kn}")
            continue
        sayac[kn].append(q)
        if q.get("zorluk") not in ZORLUK:
            sorun.append(f"{qid}: zorluk {q.get('zorluk')}")
        sec = q.get("secenekler") or {}
        if list(sec) != list(HARFLER) or any(not str(v).strip() for v in sec.values()):
            sorun.append(f"{qid}: şıklar A-E olmalı")
        if len({_fold(v).strip() for v in sec.values()}) != len(sec):
            sorun.append(f"{qid}: tekrarlayan şık")
        if q.get("dogru") not in HARFLER:
            sorun.append(f"{qid}: doğru cevap")
        sa = q.get("sik_aciklamalari") or {}
        if list(sorted(sa)) != list(HARFLER) or any(len(str(v).strip()) < 20 for v in sa.values()):
            sorun.append(f"{qid}: her şık için açıklama gerekli")
        if len(str(q.get("aciklama", "")).strip()) < 20:
            sorun.append(f"{qid}: kısa açıklama eksik")
        if len(str(q.get("soru", "")).strip()) < 15:
            sorun.append(f"{qid}: soru kökü kısa")
        for c in q.get("benzer_cikmis") or []:
            if c not in tum_cik:
                sorun.append(f"{qid}: bilinmeyen çıkmış soru {c}")
        if not isinstance(q.get("bilgi"), list):
            sorun.append(f"{qid}: bilgi listesi eksik")
        metin = q.get("soru", "") + " " + " ".join(sec.values())
        for c in cik:
            if _benzerlik(metin, _soru_metni(c)) >= 0.75:
                sorun.append(f"{qid}: çıkmış soruyla birebir benzer ({c['question_id']})")
                break
    for kn in range(1, len(kaz) + 1):
        qs = sayac.get(kn, [])
        if not 3 <= len(qs) <= 10:
            sorun.append(f"K{kn}: {len(qs)} soru (3-10 olmalı)")
            continue
        z = Counter(q.get("zorluk") for q in qs)
        if any(z[x] < 1 for x in ZORLUK):
            sorun.append(f"K{kn}: kolay/orta/zor her biri en az 1 olmalı ({dict(z)})")
        elif len(qs) > 3 and z["orta"] < max(z["kolay"], z["zor"]):
            sorun.append(f"K{kn}: fazladan sorular çoğunlukla orta olmalı ({dict(z)})")
    return sorun


def build(export: bool = False) -> dict:
    paketler = {p["id"]: p for p in _paketler()}
    cik = _cikmislar()
    by_id = {q["question_id"]: q for q in cik}
    for f in sorted(SORU_DIR.glob("*.jsonl")):  # kopya olarak elenen kayıtlar da kimlikle bulunabilsin
        for line in f.read_text(encoding="utf-8").splitlines():
            d = json.loads(line)
            by_id.setdefault(d["question_id"], d)
    baglar = json.loads((WORK / "baglar.json").read_text(encoding="utf-8")) if (WORK / "baglar.json").exists() else {}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    index, rapor = [], {}
    for f in sorted(YAZIM_DIR.glob("k1-*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        p = paketler[f.stem]
        konu_cik = [by_id[i] for i in baglar.get(p["id"], {}).get("konu_cikmis", []) if i in by_id]
        sorun = _denetle(p, d, konu_cik, set(by_id))
        rapor[p["id"]] = sorun
        if sorun:
            continue
        def cikmis_ozet(i):
            q = by_id[i]
            return {"id": i, "soru": q["stem"], "secenekler": q.get("options") or {}, "cevap": q.get("answer")}

        kazanimlar = []
        for ki, k in enumerate(p["kazanimlar"], 1):
            qs = [q for q in d["sorular"] if q["kazanim"] == ki]
            qs.sort(key=lambda q: ZORLUK.index(q["zorluk"]))
            # ilgili çıkmış sorular: yalnız editörün anlamca teyit ettiği bağlar (otomatik adaylar gösterilmez)
            ilgili = list(dict.fromkeys(c for q in qs for c in q.get("benzer_cikmis") or []))
            kazanimlar.append({"no": ki, "metin": k, "sorular": qs, "ilgili_cikmis": [cikmis_ozet(i) for i in ilgili]})
        out = {"id": p["id"], "sira": p["sira"], "kurul": 1, "ders": p["ders"], "konu": p["konu"],
               "ogretim_uyesi": p["ogretim_uyesi"], "tarih": p["tarih"], "kazanimlar": kazanimlar,
               "soru_sayisi": len(d["sorular"]), "uretim": "editör (Claude), ders paketi + bilgi paketi temelli",
               "guncelleme": datetime.now().isoformat(timespec="seconds")}
        (OUT_DIR / f"{p['id']}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        index.append({k: out[k] for k in ("id", "sira", "ders", "konu", "ogretim_uyesi", "soru_sayisi")} |
                     {"kazanim": len(kazanimlar)})
    index.sort(key=lambda x: x["sira"])
    (OUT_DIR / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    (WORK / "rapor.json").write_text(json.dumps(rapor, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in rapor.items():
        if v:
            print(f"✗ {k}:", *v[:12], sep="\n   ")
    print(f"hazır: {len(index)} ders, {sum(x['soru_sayisi'] for x in index)} soru; sorunlu: {sum(1 for v in rapor.values() if v)}")
    if export:
        SITE_DIR.mkdir(parents=True, exist_ok=True)
        for old in SITE_DIR.glob("*.json"):
            old.unlink()
        for x in index:
            (SITE_DIR / f"{x['id']}.json").write_text((OUT_DIR / f"{x['id']}.json").read_text(encoding="utf-8"), encoding="utf-8")
        (SITE_DIR / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"site: {SITE_DIR} ({len(index)} ders)")
    return rapor
