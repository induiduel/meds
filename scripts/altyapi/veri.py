#!/usr/bin/env python3
"""Ajanlar için az tokenlı içerik verisi sorgu aracı (stdlib + sqlite3 FTS5; LLM/ağ/GPU yok).

Kaynak veri SALT OKUNUR; dizin türetilmiştir: ~/.cache/meds/veri.sqlite (silinirse yeniden kurulur).
Artımlı: kaynak dosya başına (yol, mtime, boyut) tutulur, yalnız değişen kaynak yeniden dizinlenir.

  python3 scripts/altyapi/veri.py ders k2-07 [--json]          ders → kayıt + katman dosyaları manifesti
  python3 scripts/altyapi/veri.py bul "epilepsi" [--tur cikmis] [--ders k2-07] [--kurul 2] [--n 8]
  python3 scripts/altyapi/veri.py al cikmis <id> [--alan a,b] [--kisa]   asıl kaynaktan tam kayıt
  python3 scripts/altyapi/veri.py liste ornek --ders k2-07 [--n 50]
  python3 scripts/altyapi/veri.py say | kur [--bastan] | --denetle

Türler: ders cikmis deste ornek sozluk ansiklopedi hastalik ozet not anlatim
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sqlite3
import sys
import time
from pathlib import Path as _P

_s = _P(__file__).resolve()
while not (_s / "kok.py").exists() and _s != _s.parent:
    _s = _s.parent
sys.path.insert(0, str(_s))
from kok import MEDS, PROJE, SCRIPTS  # noqa: E402

import deste_deposu as dd  # noqa: E402  (desteler yalnız bu API'den okunur)

DB = _P(os.environ.get("MEDS_VERI_DB") or _P.home() / ".cache" / "meds" / "veri.sqlite")
SURUM = "1"
DERS_RE = re.compile(r"\bk(\d)-(\d\d)(?!\d)")
KURUL_RE = re.compile(r"kurul\D{0,3}(\d)", re.I)
GOVDE_SINIR = 6000


# ---------------------------------------------------------------- yardımcılar
_KATLA = str.maketrans({"ı": "i", "İ": "i", "I": "i", "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g", "ü": "u", "Ü": "u",
                        "ö": "o", "Ö": "o", "ç": "c", "Ç": "c", "â": "a", "Â": "a", "î": "i", "Î": "i", "û": "u", "Û": "u"})


def katla(s: str) -> str:
    """Türkçe katlama: ascii küçük harf (uzunluk korunur → kesit konumu eşlenir)."""
    t = (s or "").translate(_KATLA)
    k = t.lower()
    return k if len(k) == len(t) else "".join(c.lower() if len(c.lower()) == 1 else c for c in t)


def uyari(m: str) -> None:
    print(f"UYARI: {m}", file=sys.stderr)


def kurul_of(*vals) -> int | None:
    for v in vals:
        if isinstance(v, int) and 0 < v < 10:
            return v
        if isinstance(v, str):
            m = KURUL_RE.search(v)
            if m:
                return int(m.group(1))
    return None


def ders_of(s: str) -> str:
    m = DERS_RE.search(s or "")
    return f"k{m.group(1)}-{m.group(2)}" if m else ""


def metinler(v, out: list, sinir: int = GOVDE_SINIR) -> list:
    """İç içe yapıdaki tüm metinleri toplar (sınırlı)."""
    if sum(map(len, out)) > sinir:
        return out
    if isinstance(v, str):
        if len(v) > 2 and not v.startswith(("http", "/", "data:")):
            out.append(v)
    elif isinstance(v, dict):
        for x in v.values():
            metinler(x, out, sinir)
    elif isinstance(v, list):
        for x in v:
            metinler(x, out, sinir)
    return out


def gov(*parcalar) -> str:
    return " \n".join(metinler(list(parcalar), []))[:GOVDE_SINIR]


def json_yukle(p: _P):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def rel(p) -> str:
    p = _P(p).resolve()
    for kok, on in ((MEDS, ""), (PROJE, "../")):
        try:
            return on + str(p.relative_to(kok))
        except ValueError:
            pass
    return str(p)


# ---------------------------------------------------------------- kaynaklar
# Her tür: dosyalar() → yol listesi; satirlar(yol) → (id, ders, kurul, baslik, konum, govde) üreteci;
# al(yol, id) → asıl kaynaktan tam kayıt.

def _ders_dosyalar():
    return sorted(glob.glob(str(MEDS / "src/data/dersler/k[0-9].json")))


def _ders_satir(p):
    d = json_yukle(_P(p))
    for i, x in enumerate(d["dersler"]):
        yield x["id"], x["id"], x.get("kurul") or d.get("kurul"), f"{x.get('brans', '')} — {x.get('konu', '')}", str(i), \
            gov(x.get("kod"), x.get("brans"), x.get("konu"), x.get("ogretim_uyesi"), x.get("cikmis_konular"))


def _ders_al(p, kid):
    return next((x for x in json_yukle(_P(p))["dersler"] if x["id"] == kid), None)


def _cikmis_satir(p):
    for i, x in enumerate(json_yukle(_P(p))):
        ops = [o.get("text", "") if isinstance(o, dict) else str(o) for o in x.get("options") or []]
        # ders eşlemesi: kayıtta ders anahtarı alanı yok → boş (uydurma eşleme yapılmaz)
        yield x["id"], "", kurul_of(x.get("kurul"), x.get("committeeId")), \
            f"{x.get('discipline', '')} — {x.get('topic', '')} ({x.get('examYear', '')})", str(i), \
            gov(x.get("stem"), ops, f"Cevap: {x.get('correctAnswer', '')}", (x.get("explanation") or "")[:2500])


def _cikmis_al(p, kid):
    return next((x for x in json_yukle(_P(p)) if x.get("id") == kid), None)


def _deste_dosyalar():
    return [str(dd.YOL)]


def _deste_satir(p):
    for d in dd.hepsi(_P(p)):
        did = d.get("id") or d.get("deckId")
        ders, kurul = ders_of(did), kurul_of(d.get("committee"), d.get("category"))
        bas = d.get("shortTitle") or d.get("title") or did
        for j, s in enumerate(d.get("slides") or []):
            no = s.get("slideNumber", j + 1)
            yield f"{did}#{no}", ders, kurul, f"{bas} › {s.get('title', '')}", str(j), \
                gov(s.get("subtitle"), s.get("synthesisNarrative"), s.get("content"), s.get("coreContent"), s.get("spotPearls"))


def _deste_al(p, kid):
    did, _, no = kid.partition("#")
    d = dd.oku(did, _P(p))
    if not d or not no:
        return d
    return next((s for j, s in enumerate(d.get("slides") or []) if str(s.get("slideNumber", j + 1)) == no), None)


def _ornek_dosyalar():
    return sorted(f for f in glob.glob(str(MEDS / "src/data/ornek_sorular/k[0-9]/*.json")) if not f.endswith("index.json"))


def _ornek_satir(p):
    d = json_yukle(_P(p))
    ders = ders_of(_P(p).name)
    for kz in d.get("kazanimlar") or []:
        for q in kz.get("sorular") or []:
            yield q["id"], ders, kurul_of(d.get("kurul"), _P(p).parent.name), f"{d.get('konu', '')} — {q.get('zorluk', '')}", \
                str(kz.get("no")), gov(q.get("soru"), q.get("secenekler"), f"Cevap: {q.get('dogru', '')}", q.get("aciklama"))


def _ornek_al(p, kid):
    d = json_yukle(_P(p))
    return next((q for kz in d.get("kazanimlar") or [] for q in kz.get("sorular") or [] if q.get("id") == kid), None)


def _sozluk_satir(p):
    for k, v in json_yukle(_P(p)).items():
        yield k, "", kurul_of(v.get("committee")), v.get("term") or k, "", \
            gov(v.get("aliases"), v.get("definition"), v.get("description"), v.get("clinicalPearl"), v.get("discipline"))


def _sozluk_al(p, kid):
    return json_yukle(_P(p)).get(kid)


def _liste_satir(baslik_alan, govde_alanlar, kurul_alanlar):
    def f(p):
        for i, x in enumerate(json_yukle(_P(p))):
            yield x["id"], "", kurul_of(*[x.get(a) for a in kurul_alanlar]), x.get(baslik_alan) or x["id"], str(i), \
                gov(*[x.get(a) for a in govde_alanlar]) if govde_alanlar else gov(x)
    return f


def _liste_al(p, kid):
    return next((x for x in json_yukle(_P(p)) if x.get("id") == kid), None)


def _not_satir(p):
    for x in json_yukle(_P(p)):
        kurul = kurul_of(x.get("committeeId"))
        for j, s in enumerate(x.get("pages") or []):
            yield f"{x['id']}#{s.get('pageNumber', j + 1)}", "", kurul, f"{x.get('title', '')} s.{s.get('pageNumber', j + 1)}", \
                str(j), (s.get("content") or "")[:GOVDE_SINIR]


def _not_al(p, kid):
    nid, _, no = kid.partition("#")
    x = next((x for x in json_yukle(_P(p)) if x.get("id") == nid), None)
    if not x or not no:
        return x
    return next((s for j, s in enumerate(x.get("pages") or []) if str(s.get("pageNumber", j + 1)) == no), None)


def _anlatim_dosyalar():
    return sorted(glob.glob(str(MEDS / "data/sesli_anlatim/metin/k*.md")))


def _anlatim_satir(p):
    t = _P(p).read_text(encoding="utf-8")
    ilk = next((l.strip("# ").strip() for l in t.splitlines() if l.strip()), _P(p).stem)
    ders = ders_of(_P(p).name)
    yield _P(p).stem, ders, int(ders[1]) if ders else None, ilk[:120], "", t[:GOVDE_SINIR * 3]


def _anlatim_al(p, kid):
    return {"id": kid, "yol": rel(p), "metin": _P(p).read_text(encoding="utf-8")}


def _tek(yol):
    return lambda: [str(MEDS / yol)]


TURLER = {
    "ders": (_ders_dosyalar, _ders_satir, _ders_al),
    "cikmis": (_tek("data/pastQuestions.json"), _cikmis_satir, _cikmis_al),
    "deste": (_deste_dosyalar, _deste_satir, _deste_al),
    "ornek": (_ornek_dosyalar, _ornek_satir, _ornek_al),
    "sozluk": (_tek("src/data/medical_glossary.json"), _sozluk_satir, _sozluk_al),
    "ansiklopedi": (_tek("src/data/medical_encyclopedia.json"),
                    _liste_satir("term", ["latinName", "aliases", "discipline", "definition", "description", "clinicalPearl"],
                                 ["kurul"]), _liste_al),
    "hastalik": (_tek("src/data/diseases.json"), _liste_satir("name", [], ["kurul", "committee"]), _liste_al),
    "ozet": (lambda: sorted(glob.glob(str(MEDS / "src/data/summaries/kurul*.json"))),
             _liste_satir("title", ["discipline", "keyPoints", "content"], ["kurul"]), _liste_al),
    "not": (_tek("data/lecture_notes.json"), _not_satir, _not_al),
    "anlatim": (_anlatim_dosyalar, _anlatim_satir, _anlatim_al),
}


# ---------------------------------------------------------------- dizin
def baglan() -> sqlite3.Connection:
    DB.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB)
    c.executescript("""
        PRAGMA journal_mode=WAL; PRAGMA synchronous=OFF;
        CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
        CREATE TABLE IF NOT EXISTS kaynak(yol TEXT PRIMARY KEY, tur TEXT, mtime REAL, boyut INT, sayi INT, zaman REAL);
        CREATE TABLE IF NOT EXISTS kayit(rowid INTEGER PRIMARY KEY, tur TEXT, id TEXT, ders TEXT, kurul INT,
            baslik TEXT, yol TEXT, konum TEXT, govde TEXT);
        CREATE INDEX IF NOT EXISTS kayit_tid ON kayit(tur, id);
        CREATE INDEX IF NOT EXISTS kayit_yol ON kayit(yol);
        CREATE INDEX IF NOT EXISTS kayit_ders ON kayit(ders);
        CREATE VIRTUAL TABLE IF NOT EXISTS ara USING fts5(baslik, govde, tokenize='unicode61 remove_diacritics 2');
    """)
    if (c.execute("SELECT v FROM meta WHERE k='surum'").fetchone() or [None])[0] != SURUM:
        c.executescript("DELETE FROM kaynak; DELETE FROM kayit; DELETE FROM ara;")
        c.execute("INSERT OR REPLACE INTO meta VALUES('surum', ?)", (SURUM,))
        c.commit()
    return c


def kaynaklar(turler=None):
    for tur, (dosyalar, _, _) in TURLER.items():
        if turler and tur not in turler:
            continue
        try:
            for y in dosyalar():
                yield tur, y
        except Exception as e:  # noqa: BLE001
            uyari(f"{tur}: kaynak listesi alınamadı ({e}) — tür atlandı")


def tazele(c: sqlite3.Connection, turler=None, sessiz=True) -> dict:
    """Değişen kaynakları yeniden dizinler; {'yenilenen': n, 'hata': [..]}"""
    sonuc = {"yenilenen": 0, "kayit": 0, "hata": []}
    gorulen = set()
    eski = {r[0]: (r[1], r[2]) for r in c.execute("SELECT yol, mtime, boyut FROM kaynak")}
    for tur, y in kaynaklar(turler):
        gorulen.add(y)
        try:
            st = os.stat(y)
        except OSError:
            if y in eski:
                uyari(f"{tur}: kaynak kayboldu, dizinden siliniyor: {rel(y)}")
                _sil(c, y)
            else:
                uyari(f"{tur}: kaynak yok: {rel(y)} — tür atlandı")
            continue
        if eski.get(y) == (st.st_mtime, st.st_size):
            continue
        try:
            satirlar = list(TURLER[tur][1](y))
        except Exception as e:  # noqa: BLE001  bozuk kaynak sessiz "boş" sayılmaz
            uyari(f"{tur}: {rel(y)} okunamadı ({type(e).__name__}: {e}) — eski dizin korunuyor")
            sonuc["hata"].append(rel(y))
            continue
        _sil(c, y)
        for (kid, ders, kurul, baslik, konum, govde) in satirlar:
            cur = c.execute("INSERT INTO kayit(tur,id,ders,kurul,baslik,yol,konum,govde) VALUES(?,?,?,?,?,?,?,?)",
                            (tur, str(kid), ders or "", kurul, baslik or "", y, konum, govde or ""))
            c.execute("INSERT INTO ara(rowid, baslik, govde) VALUES(?,?,?)", (cur.lastrowid, katla(baslik), katla(govde)))
        c.execute("INSERT OR REPLACE INTO kaynak VALUES(?,?,?,?,?,?)", (y, tur, st.st_mtime, st.st_size, len(satirlar), time.time()))
        c.commit()
        sonuc["yenilenen"] += 1
        sonuc["kayit"] += len(satirlar)
        if not sessiz:
            print(f"  {tur:<11} {len(satirlar):>6}  {rel(y)}", file=sys.stderr)
    if not turler:
        for y in set(eski) - gorulen:
            _sil(c, y)
        c.commit()
    return sonuc


def _sil(c, y):
    c.execute("DELETE FROM ara WHERE rowid IN (SELECT rowid FROM kayit WHERE yol=?)", (y,))
    c.execute("DELETE FROM kayit WHERE yol=?", (y,))
    c.execute("DELETE FROM kaynak WHERE yol=?", (y,))


def filtre(a) -> tuple[str, list]:
    w, p = [], []
    if getattr(a, "tur", None):
        w.append("k.tur=?"); p.append(a.tur)
    if getattr(a, "ders", None):
        w.append("k.ders=?"); p.append(a.ders)
    if getattr(a, "kurul", None):
        w.append("k.kurul=?"); p.append(a.kurul)
    return (" AND " + " AND ".join(w)) if w else "", p


def kesit(govde: str, terimler: list[str], n=160) -> str:
    kg = katla(govde)
    i = min((kg.find(t) for t in terimler if kg.find(t) >= 0), default=0)
    bas = max(0, i - 40)
    s = re.sub(r"\s+", " ", govde[bas:bas + n]).strip()
    return ("…" if bas else "") + s + ("…" if len(govde) > bas + n else "")


# ---------------------------------------------------------------- komutlar
def k_bul(a):
    c = baglan()
    tazele(c, [a.tur] if a.tur else None)
    terimler = [t for t in re.findall(r"\w+", katla(a.sorgu)) if t]
    if not terimler:
        print("boş sorgu"); return 2
    w, p = filtre(a)
    satirlar = []
    for bag in (" AND ", " OR "):
        q = bag.join(f'"{t}"*' for t in terimler)
        satirlar = c.execute(f"""SELECT k.tur, k.id, k.ders, k.kurul, k.baslik, k.govde FROM ara JOIN kayit k ON k.rowid=ara.rowid
                                 WHERE ara MATCH ? {w} ORDER BY bm25(ara, 5.0, 1.0) LIMIT ?""", [q, *p, a.n]).fetchall()
        if satirlar or len(terimler) == 1:
            break
    if not satirlar:
        print("sonuç yok"); return 1
    for tur, kid, ders, kurul, baslik, govde in satirlar:
        print(f"[{tur}] {kid}  {ders or '-'} K{kurul or '?'}  {baslik[:90]}")
        print(f"   {kesit(govde, terimler)}")
    return 0


def kirp(v, n=300):
    if isinstance(v, str):
        return v if len(v) <= n else v[:n] + f"…(+{len(v) - n})"
    if isinstance(v, list):
        return [kirp(x, n) for x in v]
    if isinstance(v, dict):
        return {k: kirp(x, n) for k, x in v.items()}
    return v


def k_al(a):
    if a.tur not in TURLER:
        print(f"bilinmeyen tür: {a.tur} ({' '.join(TURLER)})"); return 2
    c = baglan()
    tazele(c, [a.tur])
    r = c.execute("SELECT yol FROM kayit WHERE tur=? AND id=?", (a.tur, a.id)).fetchone()
    yollar = [r[0]] if r else [y for _, y in kaynaklar([a.tur])]
    kayit = None
    for y in yollar:  # asıl kaynaktan oku (dizinden değil)
        try:
            kayit = TURLER[a.tur][2](y, a.id)
        except Exception as e:  # noqa: BLE001
            uyari(f"{rel(y)} okunamadı: {e}")
        if kayit is not None:
            break
    if kayit is None:
        print(f"bulunamadı: {a.tur} {a.id}"); return 1
    if a.alan and isinstance(kayit, dict):
        alanlar = [x.strip() for x in a.alan.split(",")]
        kayit = {k: kayit.get(k) for k in alanlar}
    if a.kisa:
        kayit = kirp(kayit)
    print(json.dumps(kayit, ensure_ascii=False, indent=1))
    return 0


def k_liste(a):
    if a.tur not in TURLER:
        print(f"bilinmeyen tür: {a.tur} ({' '.join(TURLER)})"); return 2
    c = baglan()
    tazele(c, [a.tur])
    w, p = filtre(a)
    top = c.execute(f"SELECT count(*) FROM kayit k WHERE 1 {w}", p).fetchone()[0]
    for kid, ders, baslik in c.execute(f"SELECT id, ders, baslik FROM kayit k WHERE 1 {w} ORDER BY rowid LIMIT ?", [*p, a.n]):
        print(f"{kid}\t{ders or '-'}\t{baslik[:100]}")
    print(f"({min(top, a.n)}/{top})")
    return 0


def k_say(a):
    c = baglan()
    bayat = 0
    for tur, y in kaynaklar():
        r = c.execute("SELECT mtime, boyut FROM kaynak WHERE yol=?", (y,)).fetchone()
        try:
            st = os.stat(y)
            if r != (st.st_mtime, st.st_size):
                bayat += 1
        except OSError:
            bayat += 1
    satir = c.execute("SELECT tur, kurul, count(*) FROM kayit GROUP BY tur, kurul").fetchall()
    tablo: dict = {}
    for tur, kurul, n in satir:
        tablo.setdefault(tur, {})[kurul] = n
    kurullar = sorted({k for t in tablo.values() for k in t if k is not None}) + [None]
    print(f"{'tür':<12}" + "".join(f"{'K' + str(k) if k else '?':>7}" for k in kurullar) + f"{'toplam':>8}")
    for tur in TURLER:
        t = tablo.get(tur, {})
        print(f"{tur:<12}" + "".join(f"{t.get(k, 0):>7}" for k in kurullar) + f"{sum(t.values()):>8}")
    son = c.execute("SELECT max(zaman) FROM kaynak").fetchone()[0]
    print(f"dizin: {DB} ({DB.stat().st_size / 1e6:.1f} MB), son kurulum "
          f"{time.strftime('%Y-%m-%d %H:%M', time.localtime(son)) if son else '-'}, bayat kaynak: {bayat}"
          + (" → `veri.py kur`" if bayat else ""))
    return 0


def k_kur(a):
    t = time.time()
    if a.bastan and DB.exists():
        for ek in ("", "-wal", "-shm"):
            _P(str(DB) + ek).unlink(missing_ok=True)
    c = baglan()
    s = tazele(c, sessiz=False)
    c.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    print(f"{s['yenilenen']} kaynak / {s['kayit']} kayıt dizinlendi, {time.time() - t:.1f} sn, "
          f"{DB.stat().st_size / 1e6:.1f} MB" + (f", {len(s['hata'])} bozuk kaynak" if s["hata"] else ""))
    return 1 if s["hata"] else 0


def k_denetle(a):
    c = baglan()
    tazele(c)
    hata = 0
    for tur, y in kaynaklar():
        try:
            n = sum(1 for _ in TURLER[tur][1](y))
        except Exception as e:  # noqa: BLE001
            print(f"HATA {tur} {rel(y)}: okunamadı ({e})"); hata += 1; continue
        m = c.execute("SELECT count(*) FROM kayit WHERE yol=?", (y,)).fetchone()[0]
        if n != m:
            print(f"HATA {tur} {rel(y)}: kaynak {n} ≠ dizin {m}"); hata += 1
    for tur in TURLER:
        if not c.execute("SELECT 1 FROM kayit WHERE tur=? LIMIT 1", (tur,)).fetchone():
            print(f"UYARI {tur}: dizinde kayıt yok")
    yinelenen = c.execute("SELECT tur, id, count(*) FROM kayit GROUP BY tur, id HAVING count(*)>1 LIMIT 5").fetchall()
    for tur, kid, n in yinelenen:
        print(f"UYARI {tur} {kid}: {n} kez (al ilkini döndürür)")
    toplam = c.execute("SELECT count(*) FROM kayit").fetchone()[0]
    print(f"{toplam} kayıt, {hata} HATA")
    return 1 if hata else 0


# ---------------------------------------------------------------- ders manifesti
KOKLER = [MEDS / "src/data", MEDS / "data", MEDS / "public", PROJE / "meds_database_v2"]
ATLA = {"node_modules", "dist", "assets"}
ANAHTAR_RE = re.compile(r"^(k\d-\d\d)(?!\d)")


def tara() -> dict:
    """katman dizini → {ders: [yollar]} (ad ders anahtarıyla başlayan dosya/dizin)."""
    katman: dict = {}
    for kok in KOKLER:
        if not kok.exists():
            uyari(f"veri kökü yok: {rel(kok)}")
            continue
        for dp, dn, fn in os.walk(kok):
            derin = dp[len(str(kok)):].count(os.sep)
            adlar = list(fn)
            alt = []
            for d in dn:
                if ANAHTAR_RE.match(d):
                    adlar.append(d + "/")
                elif derin < 3 and not d.startswith((".", "_")) and d not in ATLA:
                    alt.append(d)
            dn[:] = alt
            for ad in adlar:
                m = ANAHTAR_RE.match(ad)
                if m:
                    katman.setdefault(rel(dp), {}).setdefault(m.group(1), []).append(os.path.join(dp, ad.rstrip("/")))
    return katman


def kayit_sayisi(p: str):
    if os.path.isdir(p):
        return f"{len(os.listdir(p))} dosya"
    if not p.endswith(".json") or os.path.getsize(p) > 8e6:
        return None
    try:
        v = json_yukle(_P(p))
    except Exception:  # noqa: BLE001
        return "BOZUK JSON"
    if isinstance(v, list):
        return len(v)
    if isinstance(v, dict):
        lst = [x for x in v.values() if isinstance(x, list)]
        return max(map(len, lst)) if lst else f"{len(v)} alan"
    return None


def k_ders(a):
    key = ders_of(a.key)
    if not key:
        print("ders anahtarı biçimi k<N>-<NN>"); return 2
    kurul = int(key[1])
    kayit = None
    for y in _ders_dosyalar():
        try:
            kayit = _ders_al(y, key) or kayit
        except Exception as e:  # noqa: BLE001
            uyari(f"{rel(y)} okunamadı: {e}")
    katman = tara()
    var, eksik = {}, []
    for kd, dersler in sorted(katman.items()):
        if key in dersler:
            var[kd] = [{"yol": rel(p), "boyut": os.path.getsize(p) if os.path.isfile(p) else None, "kayit": kayit_sayisi(p)}
                       for p in sorted(dersler[key])]
        elif sum(1 for d in dersler if d.startswith(f"k{kurul}-")) >= 3:
            eksik.append(f"{kd} ({sum(1 for d in dersler if d.startswith(f'k{kurul}-'))} K{kurul} dersinde var)")
    c = baglan()
    tazele(c)
    dizin = dict(c.execute("SELECT tur, count(*) FROM kayit WHERE ders=? GROUP BY tur", (key,)).fetchall())
    if a.json:
        print(json.dumps({"ders": key, "kayit": kayit, "katmanlar": var, "eksik": eksik, "dizin": dizin}, ensure_ascii=False, indent=1))
        return 0 if kayit else 1
    if kayit:
        print(f"{key} {kayit.get('kod', '')} | {kayit.get('brans', '')} — {kayit.get('konu', '')} | "
              f"{kayit.get('ogretim_uyesi', '')} | {kayit.get('tarih', '')} | pdf: {kayit.get('pdf')}")
    else:
        print(f"{key}: ders kayıt defterinde YOK")
    print(f"Katmanlar ({len(var)}):")
    for kd, lst in var.items():
        for x in lst:
            b = f"{x['boyut'] / 1024:.0f} KB" if x["boyut"] is not None else "dizin"
            k = f", {x['kayit']} kayıt" if isinstance(x["kayit"], int) else (f", {x['kayit']}" if x["kayit"] else "")
            print(f"  {x['yol']}  ({b}{k})")
    print(f"Eksik ({len(eksik)}): " + ("; ".join(eksik) if eksik else "-"))
    print("Dizinde: " + (", ".join(f"{t} {n}" for t, n in dizin.items()) or "-"))
    return 0 if kayit else 1


# ---------------------------------------------------------------- giriş
def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--denetle" in argv:
        return k_denetle(None)
    ap = argparse.ArgumentParser(prog="veri.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = ap.add_subparsers(dest="komut", required=True)
    p = alt.add_parser("ders"); p.add_argument("key"); p.add_argument("--json", action="store_true"); p.set_defaults(f=k_ders)
    p = alt.add_parser("bul"); p.add_argument("sorgu"); p.add_argument("--tur", choices=list(TURLER))
    p.add_argument("--ders"); p.add_argument("--kurul", type=int); p.add_argument("--n", type=int, default=8); p.set_defaults(f=k_bul)
    p = alt.add_parser("al"); p.add_argument("tur"); p.add_argument("id"); p.add_argument("--alan")
    p.add_argument("--kisa", action="store_true"); p.set_defaults(f=k_al)
    p = alt.add_parser("liste"); p.add_argument("tur"); p.add_argument("--ders"); p.add_argument("--kurul", type=int)
    p.add_argument("--n", type=int, default=50); p.set_defaults(f=k_liste)
    alt.add_parser("say").set_defaults(f=k_say)
    p = alt.add_parser("kur"); p.add_argument("--bastan", action="store_true"); p.set_defaults(f=k_kur)
    a = ap.parse_args(argv)
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
