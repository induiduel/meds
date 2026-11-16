#!/usr/bin/env python3
"""Aşama başına kural özeti + okuma haritası (tam içerik hattı; kullanıcı kararı 2026-10-28).

Hata defteri (docs/KURUL2_YAPILMAYACAK_HATALAR.md, 1.100+ satır) her alt ajana bütünüyle okutulmaz. Bu betik defteri
madde madde ayrıştırır, her maddenin YALNIZ başlığını ve kural/önleme satırlarını ilgili aşamalara dağıtır:

  python3 scripts/hat/tam_hat/kural_secici.py            → docs/asama_kurallari/<aşama>.md yeniden üretilir
  python3 scripts/hat/tam_hat/kural_secici.py --denetle  → özet defterden eskiyse çıkış 1 (hat başında çalışır)
  python3 scripts/hat/tam_hat/kural_secici.py --oku <aşama>  → o aşamada okunacak dosyaların listesi (alt ajan istemine)

Kural metni değiştirilmez, kısaltılmaz: madde başlığı + "Kural / Kurul 2'de doğrusu / Önleme / Çözüm / Kapı" satırları aynen
taşınır; belirti ve kök neden anlatısı özete girmez (gerekirse madde numarasıyla defterde açılır). Hiçbir aşamaya
uymayan madde "genel"e düşer ve genel özet her aşamada okunur — madde kaybolmaz.
"""
from __future__ import annotations
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import argparse
import re
import sys
from pathlib import Path

KOK = _kok.MEDS
DEFTER = KOK / "docs/KURUL2_YAPILMAYACAK_HATALAR.md"
CIKIS = KOK / "docs/asama_kurallari"

# Aşama → (anahtar sözcükler, defter dışında okunacak dosyalar). Sözcükler küçük harfle, madde metninin tamamında aranır.
ASAMALAR: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "kaynak": (("hoca dök", "hoca_dokum", "ses kaydı", "öğrenci not", "ogrenci_not", "çıkmış eşle", "cikmis_konum", 
                "hizala", "drive", "degerlendirme", "değerlendirme paketi", "hoca vurgu"),
               ("docs/KURUL2_DERS_STANDARDI.md", "docs/HOCA_TAHMIN_REHBERI.md", "docs/OGRENCI_ONEM_YONTEMI.md")),
    "anlatim": (("anlatım", "metin_denetle", "dolgu", "türkçe", "uslup", "üslup", "okunuş", "kısaltma", "anlatım metni",
                 "denetçi", "taslak", "tanımsız"),
                ("docs/ANLATIM_KURGU_STANDARDI.md", "docs/TURKCE_USLUP_STANDARDI.md", "docs/KURUL2_DERS_STANDARDI.md",
                 "docs/OGRENCI_ONEM_YONTEMI.md")),
    "ses": (("ema", "xtts", "seslendir", "cümle zaman", "kelime zaman", "cumle_zaman", "okunuş"), ()),
    "capa_cizim": (("çapa", "capa", "çizim", "cizim", "lazer", "kontur", "panel_sinama", "pdf işareti", "imleç"),
                   ("docs/CIZIM_KURALLARI.md", "scripts/uretim/cizim/TALIMAT_CIZIM.md")),
    "ders_icerik": (("ders_icerik", "içerik paketi", "terim", "kısaltma", "tablo", "karşılaştırma", "sıralı tablo", "slayt s."),
                    ("docs/DERS_ICERIK_BICIMI.md",)),
    "ogren_deste": (("öğren", "deste", "cloze", "micro_quiz", "etkileşim", "oyun", "checkpoint", "validate_learning"),
                    ("docs/OGREN_ETKILESIM_REHBERI.md",)),
    "ornek_soru": (("soru", "şık", "sik_aciklama", "çeldirici", "çözücü", "cozucu", "asistan", "quiz", "önem listesi", "soru kökü", "ara soru", "hoca_ara"),
                   ("docs/SIK_ACIKLAMA_STANDARDI.md", "docs/SORU_USLUBU.md", "docs/HOCA_USLUBU_YONTEMI.md", "scripts/uretim/hoca_ara_soru/TALIMAT.md",
                    "docs/OGRENCI_ONEM_YONTEMI.md")),
    "pdf_tasarim": (("ders pdf", "pdf'i", "yazdır", "css", "taşma", "taşıyor", "mobil", "rozet", "boş sayfa", "kenar boşluğu", "üst üste"),
                    ("docs/DERS_ICERIK_BICIMI.md",)),
    "yayin": (("dağıt", "dagit", "oracle", "birleştir", "yayın", "rsync", "commit", "onem"),
              ("docs/KURUL_OTOMASYON_EL_KITABI.md",)),
}
KURAL_ETIKET = re.compile(r"^- \*\*(Kural|Kurul 2'de doğrusu|Önleme|Çözüm|Kalıcı çözüm|Kapı|Doğrusu)[^*]*\*\*", re.I)
# İleriye-dönük (bir ürün yazan ajana GEREKEN) etiketler. "Çözüm/Kalıcı çözüm" geçmiş kod-hatası düzeltme anlatısıdır;
# özete girmez (token israfı) — yalnız maddede başka ileri-kural yoksa korunur (madde kaybolmasın). (kullanıcı kararı 2026-11-16)
ILERI_ETIKET = ("kural", "kurul 2'de doğrusu", "doğrusu", "önleme", "kapı")


def _ileri_filtre(kural: list[str]) -> list[str]:
    """Kural satır bloklarını ileri-kural (Kural/Doğrusu/Önleme/Kapı) ile sınırla; hiç yoksa ilk bloğu bırak."""
    bloklar: list[dict] = []
    for s in kural:
        if s.startswith("- **"):
            m = re.match(r"- \*\*([^:*]+)", s)
            bloklar.append({"tag": (m.group(1).strip().lower() if m else ""), "satir": [s]})
        elif bloklar:
            bloklar[-1]["satir"].append(s)
    ileri = [b for b in bloklar if any(b["tag"].startswith(t) for t in ILERI_ETIKET)]
    secili = ileri if ileri else bloklar[:1]
    return [l for b in secili for l in b["satir"]]


def maddeler() -> list[tuple[str, str, list[str]]]:
    """(başlık, tam metin, kural satırları) listesi."""
    out, bas, govde = [], None, []
    for satir in DEFTER.read_text().splitlines() + ["## SON"]:
        if satir.startswith("## "):
            if bas:
                kural, ici = [], False
                for g in govde:
                    if g.startswith("- **"):
                        ici = bool(KURAL_ETIKET.match(g))
                    if ici:
                        kural.append(g)
                out.append((bas, "\n".join(govde), kural))
            bas, govde = satir[3:].strip(), []
        elif bas is not None:
            govde.append(satir)
    return out


def uret() -> dict[str, int]:
    CIKIS.mkdir(parents=True, exist_ok=True)
    kova: dict[str, list[str]] = {a: [] for a in [*ASAMALAR, "genel"]}
    for bas, metin, kural in maddeler():
        if not kural:  # etiketsiz (düz anlatımlı) madde: belirti/kök neden dışındaki satırlar aynen
            kural = [g for g in metin.splitlines() if g.strip() and not re.match(r"- \*\*(Belirti|Görülen|Kök)", g)][:14]
        kucuk = (bas + "\n" + "\n".join(kural)).lower()  # eşleme TAM metinle (doğru aşamaya düşsün); çıktı sıkıştırılır
        hedef = [a for a, (soz, _) in ASAMALAR.items() if any(s in kucuk for s in soz)] or ["genel"]
        govde = "\n".join(_ileri_filtre(kural)) if kural else "- (kural satırı yok; ayrıntı defterde)"
        for a in hedef:
            kova[a].append(f"### {bas}\n{govde}\n")
    for a, liste in kova.items():
        (CIKIS / f"{a}.md").write_text(
            f"# Aşama kuralları — {a}\n\n> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç "
            f"`scripts/hat/tam_hat/kural_secici.py`. {len(liste)} madde. Ayrıntı gerekirse madde başlığıyla defterde aç.\n\n"
            + "\n".join(liste))
    return {a: len(l) for a, l in kova.items()}


# Yalnız tam modda okunacak (tasarrufta atlanır) belgeler — kullanıcı kararı 2026-11-16.
#  * HOCA_TAHMIN_REHBERI: hoca tahmin katmanı tasarrufta yok (gereksiz token + kanıtsız önem damgası riski).
#  * hoca_ara_soru/TALIMAT: ara soru katmanı tasarrufta üretilmez (mod.py atlar), ama örnek_soru aşaması iki modda da
#    çağrıldığından TALIMAT özete sızıyordu — tasarrufta ölü ağırlık, elenir.
YALNIZ_TAM = {"docs/HOCA_TAHMIN_REHBERI.md", "scripts/uretim/hoca_ara_soru/TALIMAT.md"}


def oku(asama: str, mod: str = "tam") -> list[str]:
    if asama not in ASAMALAR:
        raise SystemExit(f"bilinmeyen aşama: {asama} ({', '.join(ASAMALAR)})")
    dosya = [f"docs/asama_kurallari/{asama}.md", "docs/asama_kurallari/genel.md", *ASAMALAR[asama][1]]
    if mod == "tasarruf":
        dosya = [d for d in dosya if d not in YALNIZ_TAM]
    return [d for d in dosya if (KOK / d).exists()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--denetle", action="store_true")
    ap.add_argument("--oku")
    ap.add_argument("--mod", choices=("tam", "tasarruf"), default="tam")
    a = ap.parse_args()
    if a.oku:
        print("\n".join(oku(a.oku, a.mod)))
        return 0
    if a.denetle:
        eski = [p.name for p in CIKIS.glob("*.md") if p.stat().st_mtime < DEFTER.stat().st_mtime] or \
               ([] if CIKIS.exists() else ["(yok)"])
        if eski:
            print(f"HATA: aşama özetleri defterden eski ({', '.join(eski)}); kural_secici.py çalıştır", file=sys.stderr)
            return 1
        print("aşama özetleri güncel")
        return 0
    for asama, n in uret().items():
        print(f"{asama:<12} {n:>3} madde")
    return 0


if __name__ == "__main__":
    sys.exit(main())
