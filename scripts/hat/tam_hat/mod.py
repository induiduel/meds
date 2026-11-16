#!/usr/bin/env python3
"""Tam içerik hattı · çalışma kipi (tam | tasarruf). Kipin tek kaynağı bu dosyadır; işçi, hazırlık betiği ve rapor buradan okur.

  python3 scripts/hat/tam_hat/mod.py --liste [--mod tasarruf]        # katman tablosu
  python3 scripts/hat/tam_hat/mod.py --yaz <ders klasörü> --mod tasarruf   # <klasör>/mod.json
  python3 scripts/hat/tam_hat/mod.py --rapor <ders klasörü>          # katman katman yapılacak/atlanacak

Tasarruf kipi (kullanıcı kararı 2026-11-07): yalnız sesli ders ve onu öğrenciye kaliteli sunan katmanlar. Çizim, ara resim/ara
soru sayfası, quiz, Öğren destesi ve ek LLM/GPU tüketen katmanlar ÜRETİLMEZ; "atlandı — tasarruf kipi" diye raporlanır ve
eksiklikleri dersi tamamlanmamış saymaz. Kalite kapıları (0 HATA + tek bağımsız denetçi) iki kipte de aynıdır.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# (anahtar, açıklama, tam kipte, tasarruf kipinde)
KATMANLAR = [
    ("hazirlik", "E0 hazırlık: sayfa metni/görüntü, hoca dökümü, öğrenci notu, çıkmış aday, öğrenci önem", True, True),
    ("degerlendirme", "değerlendirme paketi (degerlendirme_dogrula.py)", True, True),
    ("anlatim", "sesli ders anlatım metni + metin_denetle + turkce_uslup", True, True),
    ("ders_ekle", "ders-ekle yayını", True, True),
    ("ema_ses", "EMA sesi (GPU, klipli)", True, True),
    ("zaman_isaret", "cümle/kelime zamanı + PDF işareti (metin vurgusu, takip sistemi)", True, True),
    ("cikmis_chip", "doğrulanmış çıkmış chip'i", True, True),
    ("cikmis_analiz", "ayrıntılı çıkmış analizi + ders analizi/özeti + sesi (AGENTS 29)", True, True),
    ("terim_kisaltma", "terim + kısaltma katmanı (betik)", True, True),
    ("onem_listesi", "En önemlileri: önem listesi (spot_onem, sinav_asistani)", True, True),
    ("ornek_soru", "örnek sorular + sesli çözücü + EMA sesi", True, True),
    ("ders_icerik", "ders içerik paketi (ders_icerik_uret.py, betik)", True, True),
    ("denetci", "betik kapıları + tek bağımsız denetçi", True, True),
    ("yayin", "commit + dagit.sh + canlı doğrulama", True, True),
    ("capa_cizim", "anlamsal çapa + canlı çizim (çizim partileri, cizim_kapisi)", True, False),
    ("ara_resim", "ara resim katmanı (src/data/ara_resim, ARA_RESIM_KURALLARI.md)", True, False),
    ("ara_soru", "hocanın sorabileceği ara soru sayfası + k<N>hocaara sesi (kural 27)", True, False),
    ("hoca_sorulari", "patoloji 'Hoca soruları' + sesli hoca çözücü ayrı kartı (kural 26)", True, True),
    ("atomik_envanter", "atomik bilgi envanteri", True, False),
    ("pdf_tasarim", "ders PDF'i dışa aktarım + pdf_tarama", True, False),
    ("ogren_deste", "Öğren destesi + ders sonu oyunları (zaten askıda)", False, False),
    ("quiz", "quiz havuzu (zaten kapalı)", False, False),
]
KIPLER = ("tam", "tasarruf")

# Katman → doğrudan girdi bağımlılığı (2026-11-16; koşucunun "birlikte başlatılabilir" gruplarının TEK kaynağı). Girdiler
# kodla doğrulandı: anlatım/önem/örnek soru/çıkmış analizi yalnız paket + baglam okur (baglam.py DILIM_ASAMA, kosucu EYLEM);
# çıkmış analizi JSON'u cikmis_konum `q` listesinden kurulur (anlatıma bağlı değil), AMA aynı katmandaki ders analizi/özeti
# (ders_analizi/uret.py ozet_kur) önem listesini okur → uret.py önem SONRASI. ders_icerik terim+önem sonrası (EYLEM notu).
BAGIMLILIK: dict[str, tuple[str, ...]] = {
    "hazirlik": (),
    "degerlendirme": ("hazirlik",),
    "anlatim": ("degerlendirme",),
    "onem_listesi": ("degerlendirme",),
    "ornek_soru": ("degerlendirme",),
    "cikmis_analiz": ("degerlendirme",),
    "hoca_sorulari": ("degerlendirme",),
    "atomik_envanter": ("degerlendirme",),
    "ders_ekle": ("anlatim",),
    "ema_ses": ("ders_ekle",),
    "zaman_isaret": ("ema_ses",),
    "cikmis_chip": ("ders_ekle",),
    "terim_kisaltma": ("ders_ekle",),
    "ders_icerik": ("terim_kisaltma", "onem_listesi"),
    "capa_cizim": ("zaman_isaret",),
    "ara_resim": ("anlatim",),
    "ara_soru": ("anlatim",),
    "pdf_tasarim": ("anlatim",),
    "ogren_deste": ("degerlendirme",),
    "quiz": ("degerlendirme",),
    "denetci": ("anlatim", "onem_listesi", "ornek_soru", "cikmis_analiz", "ders_icerik"),
    "yayin": ("denetci",),
}


def paralel_gruplar(mod: str) -> list[list[str]]:
    """Kipte yapılacak katmanları bağımlılık katmanlarına (topolojik düzey) böler: aynı gruptakiler birlikte başlatılabilir."""
    yap = yapilacak(mod)
    duzey: dict[str, int] = {}

    def d(k: str) -> int:
        if k not in duzey:
            duzey[k] = 1 + max((d(b) for b in BAGIMLILIK.get(k, ()) if yap.get(b, True)), default=-1)
        return duzey[k]
    gr: dict[int, list[str]] = {}
    for k, *_ in KATMANLAR:
        if yap[k]:
            gr.setdefault(d(k), []).append(k)
    return [gr[i] for i in sorted(gr)]


def yapilacak(mod: str) -> dict[str, bool]:
    i = 2 if mod == "tam" else 3
    return {k[0]: k[i] for k in KATMANLAR}


def oku(klasor: Path) -> str:
    p = klasor / "mod.json"
    return json.loads(p.read_text()).get("mod", "tam") if p.exists() else "tam"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mod", choices=KIPLER, default="tam")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--liste", action="store_true")
    g.add_argument("--yaz", type=Path)
    g.add_argument("--rapor", type=Path)
    a = ap.parse_args()
    if a.yaz:
        a.yaz.mkdir(parents=True, exist_ok=True)
        (a.yaz / "mod.json").write_text(json.dumps({"mod": a.mod, "katmanlar": yapilacak(a.mod)}, ensure_ascii=False, indent=1))
        print(f"{a.yaz / 'mod.json'}: {a.mod}")
        return 0
    mod = oku(a.rapor) if a.rapor else a.mod
    print(f"kip: {mod}")
    for k, acik, *_ in KATMANLAR:
        y = yapilacak(mod)[k]
        print(f"  {'YAP   ' if y else 'ATLA  '} {k:<16} {acik}" + ("" if y else f"  — atlandı ({'tasarruf kipi' if mod == 'tasarruf' else 'kullanıcı kararı'})"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
