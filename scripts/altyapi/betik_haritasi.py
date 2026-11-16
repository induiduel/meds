"""meds/scripts/HARITA.md "Kök dosyalar" bölümünü üretir: scripts/ kökündeki her dosya için tek satır amaç.

Amaç dosya başındaki docstring/yorumun ilk anlamlı satırından alınır (≤90 karakter); bulunamazsa ELLE sözlüğü.
Bölüm `<!-- kok-dosyalar:bas -->` … `<!-- kok-dosyalar:son -->` arasıdır; dışı elle yazılır, dokunulmaz.

Kullanım: python3 scripts/altyapi/betik_haritasi.py            (kök dosya eklenince/silinince)
          python3 scripts/altyapi/betik_haritasi.py --denetle  (yazmaz; bayatsa çıkış 1 — yapi_koruma D8)
"""
import re
import sys as _sys
from pathlib import Path as _Path

_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

HARITA = _kok.SCRIPTS / "HARITA.md"
BAS, SON = "<!-- kok-dosyalar:bas -->", "<!-- kok-dosyalar:son -->"
ATLA = {"HARITA.md"}
# Başında okunur yorum olmayan dosyalar için elle amaç
ELLE = {
    "kok.py": "konum-bağımsız kök yolları: SCRIPTS / MEDS / PROJE",
    "detect-faulty-ocr.mjs": "data/pastQuestions.json'da bozuk OCR'lı soruları listeler",
    "run-verify-answers.bat": "Windows: soru/cevap doğrulama motorunu çalıştırır (eski)",
    "start-answer-verifier-daemon.bat": "Windows: soru izleyici + doğrulama servisini başlatır (eski)",
    "extract_curriculum.py": "müfredat PDF'inden Dönem 3 müfredat listesini çıkarır (eski, Windows yolu)",
    "build_android_apk.sh": "Android APK derlemesi (Capacitor, Android SDK)",
    "auto-git-sync.mjs": "proje değişikliklerini otomatik git commit/push ile eşitler (eski)",
    "crawl-all-drive-folders.mjs": "Drive çıkmış/dönem klasörlerini tarayıp dosya listesini çıkarır",
    "download-all-slides.mjs": "Drive'daki ders slaytlarını toplu indirir",
    "enrich-drive-slides.mjs": "driveAutomation.ts slayt kataloğuna şablon sayfa içeriği ekler (eski)",
    "sync_user_drive_folder.mjs": "öğrenci Drive klasörünü özyineli tarar",
    "test-drive-folders.mjs": "Drive klasör kimliklerine erişimi sınar",
    "update-drive-catalog.mjs": "data/real_drive_slides.json'dan Drive slayt kataloğunu üretir",
    "inspect-sources.mjs": "çıkmış sorularını kaynak dosyaya göre sayar (inceleme)",
    "rebuild-all-past-questions.mjs": "meds_sorular_txt'ten tüm çıkmış soru verisini yeniden kurar",
    "manage-service.ps1": "Windows: otomasyon servisini kur/başlat/durdur/durum (eski)",
    "show-notification.ps1": "Windows: masaüstü bildirimi gösterir (eski)",
    "test-filter-donem3.mjs": "Dönem 3 müfredat süzgecini çıkmış sorularda sınar",
    "test-sample-pdfs.mjs": "örnek Drive PDF'lerini indirip okumayı sınar",
    "scripts-meta.json": "betik üstverisi (eski otomasyon panelinin listesi)",
    "deck_pdf_slide_duzeltme.json": "deste ↔ PDF slayt eşleme düzeltmeleri (build_deck_pdf_sources girdisi)",
    "surum_gunlugu_turler.json": "sürüm günlüğü değişiklik türleri (surum_gunlugu.py girdisi)",
}
GRUPLAR = [  # (başlık, ad deseni) — ilk eşleşen kazanır
    ("Kapılar / doğrulayıcılar", r"^(sik_aciklama|turkce_uslup|validate_|ders_icerik_dogrula|detect-faulty|audit-|self-healing|verify-|run-verify|start-answer)"),
    ("Deste / ders içeriği", r"^(deste_|build_deck|build_learning|build_kazanim|ders_icerik|ders_pdf|icerik_katman|sinav_calisma|generate_medical|extract_curriculum)"),
    ("Derleme / dağıtım", r"^(build|prepare-|prune-|surum_gunlugu)"),
    ("Senkron / Drive / bulut", r"(sync|drive|download|crawl|supabase|cloud|transcribe|update-drive|enrich-drive)"),
    ("Veri düzeltme / eşleme", r"^(fix-|merge-|migrate-|filter-|rebuild-|link-|match-|deep-|manage-slide|slide-matching|process-|extract-|index-rag|detect-database|inspect-)"),
]


def amac(p: _Path) -> str:
    if p.name in ELLE:
        return ELLE[p.name]
    try:
        bas = p.read_text(encoding="utf-8", errors="ignore").splitlines()[:40]
    except OSError:
        return "—"
    for s in bas:
        t = s.strip()
        if not t or t.startswith(("#!", "import ", "from ", "'use strict'", '"use strict"', "@echo", "set ", "param(")):
            continue
        t = re.sub(r'^(/\*\*?|\*/?|//+|#+|r?"""|r?\'\'\'|REM\b|::|<#)\s*', "", t).strip()
        t = re.sub(r'("""|\'\'\'|\*/|#>)$', "", t).strip()
        t = re.sub(r"^(scripts/)?" + re.escape(p.name) + r"\s*", "", t).strip(" —-:")  # yalnız dosya adı yazan satır
        if not t or re.fullmatch(r"[-=*_ ]+|-\*-.*-\*-|eslint.*|@ts-.*|noqa.*|type: ?ignore.*", t):
            continue
        if re.match(r"^(const|let|var|async|function|def|class|export|require|\$|if|for)\b", t):
            break
        return (t[:87] + "…") if len(t) > 90 else t
    return "— (başında açıklama yok)"


def uret() -> str:
    dosyalar = sorted(p for p in _kok.SCRIPTS.iterdir() if p.is_file() and p.name not in ATLA and not p.name.startswith("."))
    kovalar: dict = {g: [] for g, _ in GRUPLAR}
    kovalar["Diğer"] = []
    for p in dosyalar:
        g = next((g for g, d in GRUPLAR if re.search(d, p.name)), "Diğer")
        kovalar[g].append(f"- `{p.name}` — {amac(p)}")
    out = [BAS, f"## Kök dosyalar ({len(dosyalar)}) — otomatik: `python3 scripts/altyapi/betik_haritasi.py`", ""]
    for g, satirlar in kovalar.items():
        if satirlar:
            out += [f"**{g}** ({len(satirlar)})", *satirlar, ""]
    out.append(SON)
    return "\n".join(out)


def main() -> int:
    eski = HARITA.read_text(encoding="utf-8")
    blok = uret()
    if BAS in eski and SON in eski:
        yeni = eski[: eski.index(BAS)] + blok + eski[eski.index(SON) + len(SON):]
    else:
        yeni = eski.rstrip("\n") + "\n\n" + blok + "\n"
    if "--denetle" in _sys.argv[1:]:
        if yeni != eski:
            print("scripts/HARITA.md kök dosyalar bölümü bayat — yeniden üret: python3 scripts/altyapi/betik_haritasi.py")
            return 1
        return 0
    HARITA.write_text(yeni, encoding="utf-8")
    print(f"scripts/HARITA.md: kök dosyalar bölümü yazıldı ({blok.count(chr(10) + '- `')} dosya)")
    return 0


if __name__ == "__main__":
    _sys.exit(main())
