#!/usr/bin/env python3
"""bag.py — dosya bağımlılık indeksi (stdlib, artımlı).

"Bu dosyayı kim kullanıyor / neye bağlı / değişirse ne etkilenir" sorularını dev grep'ler
yerine tek indeksten cevaplar. İndeks git ls-files (scripts/arsiv hariç) üzerinden kurulur,
~/.cache/meds/bag.json'a yazılır (git dışı) ve dosya mtime+boyutuyla artımlı tazelenir.

Kenar türleri:
  kod  : TS/TSX/MTS/MJS/JS import/export from, import(), require(); Python import/from
  veri : kod içi dize atıfları (src/data/..., 'src','data','x', data/..., betik yolu dizeleri),
         deste_deposu/desteDeposu kullanımı → src/data/interactive_learning_decks.json
  cagri: .sh/.service/.timer/package.json/matris.json/scripts-meta.json içindeki betik yolları

Kullanım:
  bag.py kim <yol> [--json]
  bag.py ne <yol> [--json]
  bag.py etki <yol> [--derinlik 2] [--json]
  bag.py yetim [--klasor src/services] [--json]
  bag.py kur            (indeksi zorla baştan kur)
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

MEDS = Path(__file__).resolve()
while not (MEDS / "server.ts").exists() and MEDS != MEDS.parent:
    MEDS = MEDS.parent
CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "meds" / "bag.json"
SURUM = 3
DESTE_JSON = "src/data/interactive_learning_decks.json"

JS_EXT = (".ts", ".tsx", ".mts", ".mjs", ".js", ".cjs", ".jsx")
KOD_EXT = JS_EXT + (".py",)
CAGRI_EXT = (".sh", ".service", ".timer")
CAGRI_DOSYA = {"package.json", "scripts/kapilar/matris.json", "scripts/scripts-meta.json"}
MAKS_BOYUT = 3_000_000

GIRIS_SABIT = {"server.ts", "src/main.tsx", "vite.config.ts"}

# --- desenler ---------------------------------------------------------------
RE_JS = re.compile(
    r"""(?:\bfrom\s*|\bimport\s*\(\s*|\brequire\s*\(\s*|^\s*import\s+)(['"])([^'"\n]+)\1""",
    re.M,
)
RE_PY_IMPORT = re.compile(r"^\s*import\s+([\w.]+(?:\s+as\s+\w+)?(?:\s*,\s*[\w.]+(?:\s+as\s+\w+)?)*)", re.M)
RE_PY_FROM = re.compile(r"^\s*from\s+(\.*[\w.]*)\s+import\s+(\(?[^\n#]*)", re.M)
RE_STR = re.compile(r"""(['"`])((?:\.{1,2}/|/)?[\w./@-]*?(?:src/data/|data/|scripts/|otomasyon/|deploy/)[^'"`\s${}]*)\1""")
RE_JOIN = re.compile(r"""['"]src['"]\s*,\s*['"]data['"]\s*,\s*['"]([^'"]+)['"]""")
RE_PATHSEG = re.compile(r"""(?:scripts|otomasyon|deploy|src)/[\w./-]+\.(?:py|mjs|mts|ts|tsx|js|sh|json)""")
RE_DESTE = re.compile(r"\bdeste_deposu\b|\bdesteDeposu\b")


def git_dosyalar() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=MEDS, capture_output=True, check=True).stdout
    return [p for p in out.decode("utf-8", "replace").split("\0") if p and not p.startswith("scripts/arsiv/")]


def taranir(p: str) -> bool:
    return p.endswith(KOD_EXT) or p.endswith(CAGRI_EXT) or p in CAGRI_DOSYA


def cikar(p: str, metin: str) -> list[list[str]]:
    """Ham (çözülmemiş) atıflar: [tur, spec]. tur: js | py | pyrel | str | join | yol | deste"""
    r: list[list[str]] = []
    if p.endswith(JS_EXT):
        for m in RE_JS.finditer(metin):
            r.append(["js", m.group(2)])
    elif p.endswith(".py"):
        for m in RE_PY_IMPORT.finditer(metin):
            for parca in m.group(1).split(","):
                ad = parca.strip().split()[0] if parca.strip() else ""
                if ad:
                    r.append(["py", ad])
        for m in RE_PY_FROM.finditer(metin):
            mod = m.group(1)
            adlar = [a.strip().split()[0] for a in m.group(2).strip("() \t").split(",") if a.strip() and a.strip()[0].isalpha()]
            if mod.startswith("."):
                r.append(["pyrel", mod + "|" + ",".join(adlar)])
            else:
                r.append(["py", mod])
                for a in adlar:
                    r.append(["pyalt", mod + "." + a])
    if p.endswith(KOD_EXT):
        for m in RE_STR.finditer(metin):
            r.append(["str", m.group(2)])
        for m in RE_JOIN.finditer(metin):
            r.append(["join", m.group(1)])
        if RE_DESTE.search(metin):
            r.append(["deste", ""])
    else:
        for m in RE_PATHSEG.finditer(metin):
            r.append(["yol", m.group(0)])
    # tekrarları at
    gor, tek = set(), []
    for x in r:
        k = (x[0], x[1])
        if k not in gor:
            gor.add(k)
            tek.append(x)
    return tek


# --- indeks -----------------------------------------------------------------
def indeks_kur(zorla: bool = False) -> dict:
    eski = {}
    if CACHE.exists() and not zorla:
        try:
            d = json.loads(CACHE.read_text())
            if d.get("surum") == SURUM:
                eski = d.get("dosyalar", {})
        except Exception:
            eski = {}
    dosyalar = git_dosyalar()
    yeni: dict = {}
    degisti = False
    for p in dosyalar:
        if not taranir(p):
            continue
        tam = MEDS / p
        try:
            st = tam.stat()
        except OSError:
            continue
        imza = [int(st.st_mtime_ns), st.st_size]
        e = eski.get(p)
        if e and e["i"] == imza:
            yeni[p] = e
            continue
        degisti = True
        ham: list = []
        if st.st_size <= MAKS_BOYUT:
            try:
                with open(tam, "r", encoding="utf-8", errors="replace") as f:
                    ham = cikar(p, f.read())
            except OSError:
                ham = []
        yeni[p] = {"i": imza, "a": ham}
    if degisti or set(yeni) != set(eski):
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        tmp = CACHE.with_suffix(".tmp")
        tmp.write_text(json.dumps({"surum": SURUM, "dosyalar": yeni}, separators=(",", ":")))
        tmp.replace(CACHE)
    return {"dosyalar": dosyalar, "tarama": yeni}


class Cozucu:
    def __init__(self, dosyalar: list[str]):
        self.dosya = set(dosyalar)
        self.dizin: set[str] = set()
        for p in dosyalar:
            q = p
            while "/" in q:
                q = q.rsplit("/", 1)[0]
                if q in self.dizin:
                    break
                self.dizin.add(q)
        self.py_ad: dict[str, list[str]] = defaultdict(list)
        for p in dosyalar:
            if p.endswith(".py"):
                b = p.rsplit("/", 1)[-1][:-3]
                if b == "__init__":
                    b = p.rsplit("/", 2)[-2] if p.count("/") else ""
                self.py_ad[b].append(p)
        self.py_kok = ["scripts", "scripts/altyapi", "", "otomasyon", "scripts/hat", "scripts/uretim"]

    @staticmethod
    def _norm(yol: str) -> str:
        parca: list[str] = []
        for s in yol.split("/"):
            if s in ("", "."):
                continue
            if s == "..":
                if parca:
                    parca.pop()
                continue
            parca.append(s)
        return "/".join(parca)

    def js(self, kaynak: str, spec: str) -> str | None:
        if spec.startswith("."):
            taban = self._norm(kaynak.rsplit("/", 1)[0] + "/" + spec if "/" in kaynak else spec)
        elif spec.startswith("@/"):
            taban = self._norm("src/" + spec[2:])
        elif spec.startswith("/"):
            taban = self._norm(spec)
        else:
            return None  # paket
        taban = re.sub(r"\?.*$", "", taban)
        if taban in self.dosya:
            return taban
        kok = re.sub(r"\.(js|mjs|cjs)$", "", taban)
        for ek in (".ts", ".tsx", ".mts", ".mjs", ".js", ".cjs", ".jsx", ".json", ".d.ts"):
            if kok + ek in self.dosya:
                return kok + ek
        for ek in ("/index.ts", "/index.tsx", "/index.js", "/index.mjs"):
            if taban + ek in self.dosya:
                return taban + ek
        return None

    def _py_yol(self, mod_yolu: str) -> str | None:
        for c in (mod_yolu + ".py", mod_yolu + "/__init__.py"):
            if c in self.dosya:
                return c
        return None

    def py(self, kaynak: str, mod: str, kokleri_dene: bool = True) -> str | None:
        rel = mod.replace(".", "/")
        dz = kaynak.rsplit("/", 1)[0] if "/" in kaynak else ""
        adaylar = [dz] + self.py_kok
        # kaynak dizininin üstleri (paket içi mutlak içe aktarma)
        q = dz
        while "/" in q:
            q = q.rsplit("/", 1)[0]
            adaylar.append(q)
        for k in adaylar:
            r = self._py_yol((k + "/" + rel) if k else rel)
            if r:
                return r
        if kokleri_dene and "." not in mod:
            ad = self.py_ad.get(mod, [])
            if len(ad) == 1:
                return ad[0]
        return None

    def pyrel(self, kaynak: str, spec: str) -> list[str]:
        mod, adlar = spec.split("|", 1)
        nokta = len(mod) - len(mod.lstrip("."))
        dz = kaynak.rsplit("/", 1)[0] if "/" in kaynak else ""
        for _ in range(nokta - 1):
            dz = dz.rsplit("/", 1)[0] if "/" in dz else ""
        govde = mod.lstrip(".").replace(".", "/")
        taban = (dz + "/" + govde).strip("/") if govde else dz
        r = []
        b = self._py_yol(taban)
        if b:
            r.append(b)
        for a in filter(None, adlar.split(",")):
            x = self._py_yol((taban + "/" + a).strip("/"))
            if x:
                r.append(x)
        return r

    def yol(self, kaynak: str, s: str) -> str | None:
        s = s.split("?")[0].split("#")[0].rstrip("/")
        if not s:
            return None
        aday = []
        if "meds/" in s:
            aday.append(s.split("meds/", 1)[1])
        if s.startswith("."):
            dz = kaynak.rsplit("/", 1)[0] if "/" in kaynak else ""
            aday.append(self._norm(dz + "/" + s))
        for t in ("src/data/", "scripts/", "otomasyon/", "deploy/", "data/"):
            i = s.find(t)
            if i >= 0 and (i == 0 or s[i - 1] in "/."):
                aday.append(s[i:])
        aday.append(self._norm(s))
        for a in aday:
            a = self._norm(a)
            if a in self.dosya or a in self.dizin:
                return a
        return None


def kenarlar(idx: dict) -> tuple[dict, dict, set]:
    coz = Cozucu(idx["dosyalar"])
    ileri: dict[str, dict[str, str]] = defaultdict(dict)
    for p, e in idx["tarama"].items():
        for tur, spec in e["a"]:
            hedefler: list[tuple[str, str]] = []
            if tur == "js":
                h = coz.js(p, spec)
                if h:
                    hedefler.append((h, "veri" if h.endswith(".json") else "kod"))
            elif tur == "py":
                h = coz.py(p, spec)
                if h:
                    hedefler.append((h, "kod"))
            elif tur == "pyalt":
                h = coz.py(p, spec, kokleri_dene=False)
                if h:
                    hedefler.append((h, "kod"))
            elif tur == "pyrel":
                hedefler += [(h, "kod") for h in coz.pyrel(p, spec)]
            elif tur in ("str", "yol"):
                h = coz.yol(p, spec)
                if h:
                    knd = "cagri" if tur == "yol" else ("kod" if h.endswith(KOD_EXT) else "veri")
                    if tur == "str" and h.endswith(KOD_EXT):
                        knd = "cagri"
                    hedefler.append((h, knd))
            elif tur == "join":
                h = coz.yol(p, "src/data/" + spec)
                if h:
                    hedefler.append((h, "veri"))
            elif tur == "deste":
                if DESTE_JSON in coz.dosya:
                    hedefler.append((DESTE_JSON, "veri"))
            for h, knd in hedefler:
                if h != p and (h not in ileri[p] or ileri[p][h] != "kod"):
                    ileri[p][h] = knd
    geri: dict[str, dict[str, str]] = defaultdict(dict)
    for a, hs in ileri.items():
        for b, knd in hs.items():
            geri[b][a] = knd
    return ileri, geri, coz.dosya | coz.dizin


# --- sorgular ---------------------------------------------------------------
def yol_normal(y: str, bilinen: set) -> str:
    p = Path(y)
    if p.is_absolute():
        try:
            y = str(p.resolve().relative_to(MEDS))
        except ValueError:
            pass
    y = y.removeprefix("./").removeprefix("meds/").rstrip("/")
    if y not in bilinen:
        # kısa ad: tek eşleşme varsa kabul
        es = [b for b in bilinen if b.endswith("/" + y) or b == y]
        if len(es) == 1:
            return es[0]
        if es:
            sys.exit("Belirsiz yol, şunlardan biri: " + ", ".join(sorted(es)[:10]))
        sys.exit(f"Bilinmeyen yol (git'te yok): {y}")
    return y


def grupla(d: dict[str, str]) -> dict[str, list[str]]:
    g: dict[str, list[str]] = defaultdict(list)
    for k, v in d.items():
        g[v].append(k)
    return {k: sorted(v) for k, v in sorted(g.items())}


def dizine_dusen(geri: dict, hedef: str) -> dict[str, str]:
    """Dizin hedefleri: dizin atfı + içindeki dosyalara atıfları birleştir."""
    if hedef in geri and not hedef.endswith("/"):
        sonuc = dict(geri.get(hedef, {}))
    else:
        sonuc = {}
    # dosyanın üst dizinine (ör. 'src/data/k2_cozucu') yapılan atıfları dolaylı say
    return sonuc


def yazdir_grup(baslik: str, g: dict[str, list[str]]):
    toplam = sum(len(v) for v in g.values())
    print(f"{baslik} ({toplam})")
    for tur, lst in g.items():
        print(f"  [{tur}] {len(lst)}")
        for x in lst:
            print(f"    {x}")


def etki_hesap(geri: dict, hedef: str, derinlik: int) -> dict[str, int]:
    seviye = {hedef: 0}
    sinir = [hedef]
    for d in range(1, derinlik + 1):
        yeni = []
        for x in sinir:
            for y, knd in geri.get(x, {}).items():
                if y not in seviye:
                    seviye[y] = d
                    yeni.append(y)
        sinir = yeni
        if not sinir:
            break
    seviye.pop(hedef)
    return seviye


def sunucu_ulasir(geri: dict, hedef: str) -> tuple[bool, bool]:
    gor, yigin = {hedef}, [hedef]
    sunucu = vite = False
    while yigin:
        x = yigin.pop()
        if x == "server.ts":
            sunucu = True
        if x.startswith("src/components/") or x in ("src/main.tsx", "src/App.tsx"):
            vite = True
        for y, knd in geri.get(x, {}).items():
            if knd == "kod" and y not in gor and y.endswith(JS_EXT):
                gor.add(y)
                yigin.append(y)
    return sunucu, vite


def giris_noktalari(geri: dict, dosyalar: set) -> set[str]:
    g = set(GIRIS_SABIT)
    for p in dosyalar:
        if p.startswith("deploy/") or p.endswith(".test.ts") or p.endswith(".spec.ts") or "/tests/" in p or p.endswith(".d.ts"):
            g.add(p)
    return g


def main(argv: list[str]) -> int:
    import argparse

    ap = argparse.ArgumentParser(prog="bag.py", description=(__doc__ or "").split("\n")[0])
    ap.add_argument("komut", choices=["kim", "ne", "etki", "yetim", "kur"])
    ap.add_argument("yol", nargs="?")
    ap.add_argument("--derinlik", type=int, default=2)
    ap.add_argument("--klasor")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sure", action="store_true", help="süreyi stderr'e yaz")
    a = ap.parse_args(argv)
    t0 = time.perf_counter()
    idx = indeks_kur(zorla=a.komut == "kur")
    ileri, geri, bilinen = kenarlar(idx)
    out: dict = {}

    if a.komut == "kur":
        out = {"dosya": len(idx["tarama"]), "kenar": sum(len(v) for v in ileri.values()), "onbellek": str(CACHE)}
        print(json.dumps(out, ensure_ascii=False) if a.json else f"İndeks: {out['dosya']} dosya, {out['kenar']} kenar → {CACHE}")
    elif a.komut in ("kim", "ne"):
        if not a.yol:
            ap.error("yol gerekli")
        y = yol_normal(a.yol, bilinen)
        if a.komut == "kim":
            d = dict(geri.get(y, {}))
            # dizin ise içindeki dosyalara atıfları da topla
            if y not in idx["tarama"] and y + "/" and any(k.startswith(y + "/") for k in geri):
                for k, v in geri.items():
                    if k.startswith(y + "/"):
                        for s, knd in v.items():
                            d.setdefault(s, knd)
            g = grupla(d)
        else:
            g = grupla(ileri.get(y, {}))
        if a.json:
            print(json.dumps({"yol": y, a.komut: g}, ensure_ascii=False, indent=1))
        else:
            yazdir_grup(f"{y} — {'kullananlar' if a.komut == 'kim' else 'bağımlılıklar'}", g)
    elif a.komut == "etki":
        if not a.yol:
            ap.error("yol gerekli")
        y = yol_normal(a.yol, bilinen)
        sev = etki_hesap(geri, y, a.derinlik)
        sunucu, vite = sunucu_ulasir(geri, y)
        notlar = []
        if sunucu or y == "server.ts":
            notlar.append("server.ts'e ulaşıyor → sunucu yeniden başlatma gerekir (systemctl --user restart meds-web)")
        if vite:
            notlar.append("ön yüze ulaşıyor → npx vite build")
        if a.json:
            print(json.dumps({"yol": y, "etkilenen": sev, "sunucu": sunucu, "vite": vite, "notlar": notlar}, ensure_ascii=False, indent=1))
        else:
            print(f"{y} — etki (derinlik {a.derinlik}): {len(sev)} dosya")
            for d in range(1, a.derinlik + 1):
                lst = sorted(k for k, v in sev.items() if v == d)
                if lst:
                    print(f"  derinlik {d}: {len(lst)}")
                    for x in lst[:60]:
                        print(f"    {x}")
                    if len(lst) > 60:
                        print(f"    … +{len(lst) - 60}")
            for n in notlar:
                print("NOT: " + n)
    elif a.komut == "yetim":
        giris = giris_noktalari(geri, set(idx["tarama"]))
        k = (a.klasor or "").rstrip("/")
        yetim = sorted(
            p for p in idx["tarama"]
            if p.endswith(KOD_EXT) and (not k or p.startswith(k + "/"))
            and p not in giris and not geri.get(p)
            and not p.endswith("__init__.py")
        )
        if a.json:
            print(json.dumps({"klasor": k, "yetim": yetim}, ensure_ascii=False, indent=1))
        else:
            print(f"Yetim kod dosyaları{' (' + k + ')' if k else ''}: {len(yetim)}")
            for x in yetim:
                print("  " + x)
    if a.sure:
        print(f"[süre {time.perf_counter() - t0:.2f} sn]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
