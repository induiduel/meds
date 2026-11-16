#!/usr/bin/env python3
"""Yapı koruma kapısı (2026-11-16 yeniden yapılandırmasından sonra) — aynı hataların geri dönmesini engeller.

Yalnız stdlib, <5 sn, yerelden bağımsız (tüm desenler Python regex; sed/grep `[a-z]` tuzağı yok, H577).

Denetimler (her bulgu dosya:satır ile):
  D1 HATA   interactive_learning_decks.json'ı deste deposu dışında açan/yazan kod (scripts/ arsiv hariç, src/, server.ts)
  D2 HATA   .py'de Path(__file__)…parents[N≥2] ya da .parent.parent.parent ile kök hesabı (kok.py kullan)
  D3 HATA   deploy/oracle/tasinan_yollar.txt: yeni yol var olmalı, eski yol yeniden oluşmamalı
  D4 HATA   KURUL2_YAPILMAYACAK_HATALAR.md dizini ↔ docs/hatalar/*.md (kural_secici.py --denetle)
  D5 HATA   src/services/** + server.ts: src/data'ya writeFileSync/renameSync, writableContent kullanmadan (H580)
  D6 UYARI  token bütçesi: AGENTS.md / hata defteri / docs/hatalar/*.md / MEMORY.md kelime tavanları
  D7 HATA   scripts/ kökünde HARITA.md'de anılmayan yeni alt dizin

İzin listeleri bu dosyadadır; IZINLI_ESKI listeleri yalnız AZALABİLİR (düzeltilen kalem listeden silinir; artık
ihlal etmeyen kalem UYARI verir). Yeni ihlali izin listesine eklemek yerine kodu düzelt.

  python3 scripts/kapilar/yapi_koruma.py            # tam
  python3 scripts/kapilar/yapi_koruma.py --hizli    # pre-commit: D6 (yalnız uyarı) atlanır, temizse sessiz
  python3 scripts/kapilar/yapi_koruma.py --json
Çıkış: HATA varsa 1, yoksa 0.
"""
from __future__ import annotations

import io
import json
import re
import subprocess
import sys
import tokenize
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

MEDS: Path = _kok.MEDS
SCRIPTS: Path = _kok.SCRIPTS
PROJE: Path = _kok.PROJE

KOD_UZANTI = {".py", ".ts", ".tsx", ".mts", ".mjs", ".js", ".cjs", ".sh"}
ATLA_DIZIN = {"__pycache__", "node_modules", ".git", ".venv", ".venv-ocr"}

# ---------------------------------------------------------------- D1
DESTE = "interactive_learning_decks.json"
D1_IZINLI_DOSYA = {  # destenin tek okuma/yazma noktaları ve katman altyapısı
    "scripts/deste_deposu.py",
    "src/services/desteDeposu.ts",
    "scripts/icerik_katman.py",
    "src/services/contentOverlay.ts",
    "src/services/dataCatalogService.ts",
    "scripts/altyapi/vite/splitLearningDecks.ts",
    "scripts/kapilar/yapi_koruma.py",  # bu kapı (dizeyi desen olarak taşır)
}
# (dosya, satırda geçen parça) → gerekçe. Satır numarası kaymasına dayanıklı.
D1_IZINLI_SATIR = {
    ("scripts/uretim/ders_isci/yayinla.py", '"src/data/interactive_learning_decks.json", "src/data/summaries/kurul1.json"'):
        "git add yol listesi (açma/yazma değil)",
    ("scripts/build_deck_packages.py", '"kaynak": "src/data/interactive_learning_decks.json"'):
        "paket üst verisinde kaynak etiketi",
    ("scripts/hat/paket/medspak_uret.py", 'help="deste kaynağı (varsayılan src/data/interactive_learning_decks.json)"'):
        "argparse yardım metni",
    ("scripts/asistan/kaynaklar.py", "'src/data/interactive_learning_decks.json', dk.get('discipline'"):
        "arama belgesinde kaynak etiketi (okuma deste_deposu ile)",
    ("src/components/manage16/sayfalar/Desteler.tsx", "<code>interactive_learning_decks.json</code>"):
        "yönetim ekranında gösterilen kaynak adı",
}
# Mevcut doğrudan açan kod (2026-11-16). Yalnız azalabilir → deste_deposu'na taşındıkça sil.
D1_IZINLI_ESKI = {
    ("scripts/orchestrate_drive_curriculum_ai.mjs", "const DECKS_PATH = path.resolve(PROJECT_ROOT, 'src', 'data', 'interactive_learning_decks.json');"),
}

# ---------------------------------------------------------------- D2
D2_DESEN = re.compile(r"parents\[\s*([0-9]+)\s*\]|\.parent\.parent\.parent")
D2_IZINLI_ESKI = {  # dosya → gerekçe; yalnız azalabilir
    "scripts/altyapi/v2/tests/__init__.py": "bilinçli: v2 paket kabını (scripts/altyapi) sys.path'e ekler; kök değil",
}

# ---------------------------------------------------------------- D5
D5_YAZ = re.compile(r"\b(writeFileSync|renameSync)\s*\(")
D5_SRCDATA = re.compile(r"""src[/\\]data|['"]src['"]\s*,\s*['"]data['"]""")
# Sezgi dosya düzeyindedir: yorum DIŞI bir satırda src/data yolu kuran + writeFileSync/renameSync çağıran +
# writableContent anmayan dosya. 2026-11-16 taramasında böyle olan mevcut dosyalar (yalnız azalabilir):
D5_IZINLI_ESKI_DOSYA = {
    "src/services/autoErrorRepairEngine.ts",
    "src/services/musicStore.ts",          # src/data/musicTracks.json yalnız tohum (okuma); yazım data/
    "src/services/notebooklmBridgeService.ts",
    "src/services/notebooklmManageService.ts",
    "src/services/questionCrossAuditService.ts",
    "src/services/hatActionsRoutes.ts",
    "src/services/knowledge/diseaseGraphBuild.ts",  # derleme betiği (çalışma zamanı yazıcısı değil)
    "src/services/localRagEngine.ts",
    "src/services/queryIntel/build.ts",             # derleme betiği
    "src/services/questionIntake.ts",
}

# ---------------------------------------------------------------- D6
D6_TAVAN = [
    (PROJE / "AGENTS.md", 3200),
    (MEDS / "docs" / "KURUL2_YAPILMAYACAK_HATALAR.md", 7000),
]
D6_HATALAR_TAVAN = 6000
D6_MEMORY = Path.home() / ".claude" / "projects" / "-home-indu-medsor" / "memory" / "MEMORY.md"
D6_MEMORY_TAVAN = 2000

# ---------------------------------------------------------------- D7
D7_IZINLI_ESKI: set = set()  # 2026-11-16'da HARITA.md'de anılmıyordu; haritaya yazılınca sil


bulgular: list[dict] = []


def bul(denetim: str, duzey: str, yol: str, satir: int | None, mesaj: str) -> None:
    bulgular.append({"denetim": denetim, "duzey": duzey, "yol": yol, "satir": satir, "mesaj": mesaj})


def rel(p: Path) -> str:
    return p.relative_to(MEDS).as_posix()


def kod_dosyalari() -> list[Path]:
    out: list[Path] = []
    for kok in (SCRIPTS, MEDS / "src"):
        for p in kok.rglob("*"):
            if p.suffix not in KOD_UZANTI or not p.is_file():
                continue
            parts = p.relative_to(MEDS).parts
            if any(x in ATLA_DIZIN for x in parts):
                continue
            if parts[:2] == ("scripts", "arsiv") or parts[:2] == ("src", "data"):
                continue
            out.append(p)
    st = MEDS / "server.ts"
    if st.exists():
        out.append(st)
    return out


def py_yorum_satirlari(metin: str) -> set[int]:
    """Yorum ve docstring (tek başına dize ifadesi) satırları."""
    s: set[int] = set()
    try:
        onceki = tokenize.NEWLINE
        for tok in tokenize.generate_tokens(io.StringIO(metin).readline):
            if tok.type == tokenize.COMMENT and tok.line.strip().startswith("#"):
                s.add(tok.start[0])
            elif tok.type == tokenize.STRING and onceki in (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.NL):
                s.update(range(tok.start[0], tok.end[0] + 1))
            if tok.type not in (tokenize.COMMENT, tokenize.NL):
                onceki = tok.type
    except (tokenize.TokenError, SyntaxError, IndentationError):
        pass
    return s


def js_yorum_satirlari(satirlar: list[str], sh: bool) -> set[int]:
    s: set[int] = set()
    blok = False
    for i, l in enumerate(satirlar, 1):
        t = l.strip()
        if sh:
            if t.startswith("#"):
                s.add(i)
            continue
        if blok:
            s.add(i)
            if "*/" in t:
                blok = False
            continue
        if t.startswith("//") or t.startswith("*"):
            s.add(i)
        elif t.startswith("/*"):
            s.add(i)
            blok = "*/" not in t
    return s


def yorumlar(p: Path, metin: str, satirlar: list[str]) -> set[int]:
    if p.suffix == ".py":
        return py_yorum_satirlari(metin)
    return js_yorum_satirlari(satirlar, p.suffix == ".sh")


def d1_d2_d5(dosyalar: list[Path]) -> dict:
    d1_eski_gorulen: set = set()
    d2_eski_gorulen: set = set()
    d5_eski_gorulen: set = set()
    for p in dosyalar:
        r = rel(p)
        try:
            metin = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        has_deste = DESTE in metin
        has_d2 = p.suffix == ".py" and D2_DESEN.search(metin)
        has_d5 = (r.startswith("src/services/") or r == "server.ts") and D5_YAZ.search(metin)
        if not (has_deste or has_d2 or has_d5):
            continue
        satirlar = metin.splitlines()
        yorum = yorumlar(p, metin, satirlar)
        # D1
        if has_deste and r not in D1_IZINLI_DOSYA:
            for i, l in enumerate(satirlar, 1):
                if DESTE not in l or i in yorum:
                    continue
                t = l.strip()
                if any(f == r and parca in t for (f, parca) in D1_IZINLI_SATIR):
                    continue
                eski = next(((f, parca) for (f, parca) in D1_IZINLI_ESKI if f == r and parca in t), None)
                if eski:
                    d1_eski_gorulen.add(eski)
                    continue
                bul("D1", "HATA", r, i, "deste dosyası doğrudan anılıyor — scripts/deste_deposu.py / src/services/desteDeposu.ts kullan")
        # D2
        if has_d2:
            for i, l in enumerate(satirlar, 1):
                if i in yorum:
                    continue
                for m in D2_DESEN.finditer(l):
                    if m.group(1) is not None and int(m.group(1)) < 2:
                        continue
                    if r in D2_IZINLI_ESKI:
                        d2_eski_gorulen.add(r)
                        continue
                    bul("D2", "HATA", r, i, f"sabit kademeli kök hesabı ({m.group(0)}) — scripts/kok.py kullan (HARITA.md §Yeni betik)")
        # D5
        srcdata_kod = has_d5 and any(D5_SRCDATA.search(l) for i, l in enumerate(satirlar, 1) if i not in yorum)
        if srcdata_kod and "writableContent" not in metin:
            for i, l in enumerate(satirlar, 1):
                if i in yorum or not D5_YAZ.search(l):
                    continue
                if r in D5_IZINLI_ESKI_DOSYA:
                    d5_eski_gorulen.add(r)
                    continue
                bul("D5", "HATA", r, i, "src/data'ya writableContent olmadan yazım (H580) — contentOverlay.writableContent kullan")
    for k in D1_IZINLI_ESKI - d1_eski_gorulen:
        bul("D1", "UYARI", k[0], None, "IZINLI_ESKI kalemi artık ihlal etmiyor — listeden sil")
    for k in set(D2_IZINLI_ESKI) - d2_eski_gorulen:
        bul("D2", "UYARI", k, None, "IZINLI_ESKI kalemi artık ihlal etmiyor — listeden sil")
    for k in set(D5_IZINLI_ESKI_DOSYA) - d5_eski_gorulen:
        bul("D5", "UYARI", k, None, "IZINLI_ESKI kalemi artık ihlal etmiyor — listeden sil")
    return {"D1_izinli_dosya": len(D1_IZINLI_DOSYA), "D1_izinli_satir": len(D1_IZINLI_SATIR),
            "D1_izinli_eski": len(D1_IZINLI_ESKI), "D2_izinli_eski": len(D2_IZINLI_ESKI),
            "D5_izinli_eski": len(D5_IZINLI_ESKI_DOSYA), "D7_izinli_eski": len(D7_IZINLI_ESKI)}


def d3() -> None:
    dosya = MEDS / "deploy" / "oracle" / "tasinan_yollar.txt"
    r = rel(dosya)
    if not dosya.exists():
        bul("D3", "HATA", r, None, "dosya yok")
        return
    for i, l in enumerate(dosya.read_text(encoding="utf-8").splitlines(), 1):
        t = l.split("#", 1)[0].split()
        if len(t) < 2:
            continue
        eski, yeni = t[0], t[1]
        if not (MEDS / yeni).exists():
            bul("D3", "HATA", r, i, f"yeni yol yok: {yeni}")
        if (MEDS / eski).exists():
            bul("D3", "HATA", r, i, f"eski yol yeniden oluşmuş: {eski} (yeni yer: {yeni})")


def d4() -> None:
    betik = SCRIPTS / "hat" / "tam_hat" / "kural_secici.py"
    try:
        sp = subprocess.run([sys.executable, str(betik), "--denetle"], cwd=MEDS,
                            capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as e:
        bul("D4", "HATA", rel(betik), None, f"çalıştırılamadı: {e}")
        return
    if sp.returncode != 0:
        cikti = (sp.stdout + sp.stderr).strip().splitlines()
        for l in cikti[:20] or ["(çıktı yok)"]:
            bul("D4", "HATA", "docs/KURUL2_YAPILMAYACAK_HATALAR.md", None, f"kural_secici --denetle: {l}")


def kelime(p: Path) -> int:
    return len(p.read_text(encoding="utf-8", errors="replace").split())


def d6() -> None:
    hedefler = list(D6_TAVAN)
    hedefler += [(p, D6_HATALAR_TAVAN) for p in sorted((MEDS / "docs" / "hatalar").glob("*.md"))]
    if D6_MEMORY.exists():
        hedefler.append((D6_MEMORY, D6_MEMORY_TAVAN))
    for p, tavan in hedefler:
        if not p.exists():
            continue
        n = kelime(p)
        if n > tavan:
            bul("D6", "UYARI", str(p), None, f"{n} kelime > {tavan} (token bütçesi)")


def d7() -> None:
    harita = (SCRIPTS / "HARITA.md").read_text(encoding="utf-8")
    for p in sorted(SCRIPTS.iterdir()):
        if not p.is_dir() or p.name in ATLA_DIZIN or p.name.startswith("."):
            continue
        if re.search(r"(?<![\w/])" + re.escape(p.name) + r"/", harita):
            continue
        if p.name in D7_IZINLI_ESKI:
            continue
        bul("D7", "HATA", f"scripts/{p.name}/", None, "HARITA.md'de anılmayan kök alt dizin — doğru gruba (hat/uretim/altyapi/moduller) taşı ya da haritaya yaz")
    for ad in D7_IZINLI_ESKI:
        if not (SCRIPTS / ad).is_dir() or re.search(r"(?<![\w/])" + re.escape(ad) + r"/", harita):
            bul("D7", "UYARI", f"scripts/{ad}/", None, "IZINLI_ESKI kalemi artık gerekmiyor — listeden sil")


def main() -> int:
    argv = sys.argv[1:]
    hizli, js = "--hizli" in argv, "--json" in argv
    sayilar = d1_d2_d5(kod_dosyalari())
    d3()
    d4()
    if not hizli:
        d6()
    d7()
    hata = sum(1 for b in bulgular if b["duzey"] == "HATA")
    uyari = len(bulgular) - hata
    if js:
        print(json.dumps({"hata": hata, "uyari": uyari, "izin_listeleri": sayilar, "bulgular": bulgular},
                         ensure_ascii=False, indent=2))
    else:
        for b in sorted(bulgular, key=lambda b: (b["duzey"] != "HATA", b["denetim"], b["yol"], b["satir"] or 0)):
            yer = f"{b['yol']}:{b['satir']}" if b["satir"] else b["yol"]
            print(f"{b['duzey']} {b['denetim']} {yer}: {b['mesaj']}")
        if not (hizli and not bulgular):
            print(f"yapi_koruma: {hata} HATA, {uyari} UYARI  (izin listeleri: {sayilar})")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
