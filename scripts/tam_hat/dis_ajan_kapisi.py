#!/usr/bin/env python3
"""Dış ajan izolasyon kapısı (AGENTS kural 24, kullanıcı kararı 2026-10-29). LLM yok.

  python3 scripts/tam_hat/dis_ajan_kapisi.py --ajan <etiket> --ders <k2-07> --anlik yaz        # İŞ BAŞINDA, çalışma öncesi
  python3 scripts/tam_hat/dis_ajan_kapisi.py --ajan <etiket> --ders <k2-07> [--canli URL] [--yayin]

Claude dışındaki her ajan (Gemini, GPT, DeepSeek, Antigravity…) tam içerik işçisini çalıştırırken:
  * etiket  : a-z0-9, 2–12 harf, `claude` olamaz;
  * anahtar : `<ders>-ag-<etiket>` (ör. k2-07-ag-gemini) — mevcut ders anahtarı/sürümü ASLA kullanılmaz, v2/v3 YOK;
  * çalışma : yalnız `meds_temp/dis_ajan/<etiket>/<ders>/` ve `data/sesli_anlatim/**/<anahtar>*` ile `src/data/**/<anahtar>*`;
  * kapı    : bu betik, ajanın değiştirdiği her dosyanın bu izinli kümede olduğunu ve Claude/mevcut verinin bayt bayt
              aynı kaldığını (git diff) denetler; --canli verilirse canlıda ders-ekle sonrası `yalniz-yonetici` olduğunu da.
Çıkış 0 = HATA yok. Ajan bu kapıyı geçmeden `ders-ekle` çağıramaz (el kitabı: DIS_AJAN_YOL_HARITASI.md).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
ETIKET = re.compile(r"^[a-z0-9]{2,12}$")
DERS = re.compile(r"^k\d+-\d+$")


def git(*a: str) -> list[str]:
    r = subprocess.run(["git", "-C", str(KOK), *a], capture_output=True, text=True)
    return [x for x in r.stdout.splitlines() if x]


def kirli() -> list[str]:
    return sorted(set(git("diff", "--name-only", "HEAD") + git("ls-files", "--others", "--exclude-standard")))


def ozet(f: str) -> str:
    import hashlib

    p = KOK / f
    return hashlib.sha1(p.read_bytes()).hexdigest() if p.is_file() else "-"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ajan", required=True)
    ap.add_argument("--ders", required=True)
    ap.add_argument("--canli", help="Oracle/canlı kök adresi; yönetici çerezi gerekmez, öğrenci görünümü 403 beklenir")
    ap.add_argument("--anlik", choices=["yaz"], help="iş başında dosya anlık görüntüsü al (sonradan değişenleri bununla karşılaştırır)")
    ap.add_argument("--kismi", action="store_true", help="kısmi/deneme çalışması: hedef.json zorunlu değil (UYARI verir); yayın için kullanılamaz")
    ap.add_argument("--yayin", action="store_true", help="ders-ekle sonrası denetim (canlı kilit kontrolü zorunlu)")
    a = ap.parse_args()
    hata: list[str] = []
    uyari: list[str] = []

    if not ETIKET.match(a.ajan) or a.ajan == "claude":
        hata.append(f"etiket geçersiz: '{a.ajan}' (a-z0-9, 2–12, 'claude' olamaz)")
    if not DERS.match(a.ders):
        hata.append(f"ders anahtarı geçersiz: '{a.ders}' (örn. k2-07)")
    if hata:
        print("\n".join("HATA " + h for h in hata))
        return 1
    anahtar = f"{a.ders}-ag-{a.ajan}"

    calisma = KOK.parent / "meds_temp" / "dis_ajan" / a.ajan / a.ders
    anlik = calisma / "anlik.json"
    if a.anlik == "yaz":
        calisma.mkdir(parents=True, exist_ok=True)
        anlik.write_text(json.dumps({f: ozet(f) for f in kirli()}, indent=1), "utf8")
        print(f"anlık görüntü yazıldı ({len(kirli())} kirli dosya kaydedildi): {anlik}")
        return 0

    # 1) Çalışma klasörü
    if not calisma.is_dir():
        hata.append(f"çalışma klasörü yok: {calisma} (E0 hazırlık çıktıları buraya konur)")
    kimlik = calisma / "ajan.json"
    if kimlik.exists():
        try:
            k = json.loads(kimlik.read_text("utf8"))
            for f in ("ajan", "model", "tarih"):
                if not k.get(f):
                    hata.append(f"ajan.json '{f}' boş")
            if k.get("ajan") != a.ajan:
                hata.append("ajan.json 'ajan' etiketle eşleşmiyor")
        except Exception as e:  # noqa: BLE001
            hata.append(f"ajan.json okunamadı: {e}")
    else:
        hata.append("ajan.json yok ({\"ajan\",\"model\",\"tarih\",\"surum\"} kimlik dosyası zorunlu)")

    # 2) Mevcut veriye dokunulmadı mı? (izinli küme dışında değişen/yeni dosya)
    izinli = re.compile(rf"(^|/){re.escape(anahtar)}([./_-]|$)")
    if not anlik.exists():
        hata.append("başlangıç anlık görüntüsü yok. Yapılacak: iş başında '--anlik yaz' çalıştır (kirli ağaçta değişikliği doğru ölçmek için).")
        onceki = {}
    else:
        onceki = json.loads(anlik.read_text("utf8"))
    for f in kirli():
        if onceki.get(f) == ozet(f):
            continue  # bu iş başlamadan önce de aynı içerikle kirliydi
        if f.startswith("../meds_temp/dis_ajan/") or f.startswith(f"meds_temp/dis_ajan/{a.ajan}/"):
            continue
        if izinli.search(f):
            continue
        hata.append(f"izinsiz dosya değişti: {f} — yalnız '{anahtar}' adlı dosyalar ve meds_temp/dis_ajan/{a.ajan}/ yazılabilir")

    # 2b) Anlama sınavı ve hedef kilidi (protokol §12-5, §12-10)
    import hashlib

    try:
        g = json.loads((calisma / "sinav_gecti.json").read_text("utf8"))
        sys.path.insert(0, str(KOK / "scripts/tam_hat/dis_ajan"))
        import anlama_sinavi as AS

        bek = AS.imza(a.ajan, a.ders, g.get("tarih"))
        if g.get("imza") != bek or g.get("puan") != g.get("toplam"):
            hata.append("sinav_gecti.json geçersiz, %100 değil ya da sınav/yönerge sonradan değişti. Yapılacak: anlama_sinavi.py ile sınavı yeniden geç.")
    except Exception:  # noqa: BLE001
        hata.append("anlama sınavı geçilmemiş (sinav_gecti.json yok). Yapılacak: anlama_sinavi.py sorular/puanla — %100 olmadan iş başlamaz.")
    r = subprocess.run([sys.executable, "-I", str(KOK / "scripts/tam_hat/dis_ajan/hedef.py"), "dogrula", str(calisma)], capture_output=True, text=True)
    if r.returncode and a.kismi and not a.yayin:
        uyari.append("kısmi çalışma: hedef.json yok/geçersiz (tam ders yayını için zorunlu)")
    elif r.returncode:
        hata.append("hedef.json yok ya da imzası bozuk. Yapılacak: hedef.py yaz ile iş başında bir kez yaz; sonradan değiştirme. " + r.stdout.strip()[:160])

    # 2c) metin.md yalnız kapıdan geçmiş cümlelerden oluşur (kapıdan sonra elle değişiklik yasak)
    md = calisma / "metin.md"
    if md.exists():
        import unicodedata

        def n(t: str) -> str:
            return re.sub(r"\s+", " ", unicodedata.normalize("NFC", t)).strip()

        govde = n(re.sub(r"(?m)^(#|@@).*$", "", md.read_text("utf8")))
        cumleler: list[str] = []
        for f in sorted(calisma.glob("uretim_*.json")):
            try:
                cumleler += [n(str(u.get("metin", ""))) for u in json.loads(f.read_text("utf8")) if isinstance(u, dict)]
            except Exception as e:  # noqa: BLE001
                hata.append(f"{f.name} okunamadı: {e}")
        kalan = govde
        for c in sorted(set(cumleler), key=len, reverse=True):
            kalan = kalan.replace(c, " ")
        kalan = n(kalan)
        if not cumleler:
            hata.append("metin.md var ama uretim_*.json yok: metin kapıdan geçmiş cümlelerden kurulmalı")
        elif kalan:
            hata.append(f"metin.md kapıdan geçmemiş metin içeriyor: «{kalan[:120]}». Yapılacak: bu metni önce uretim_<bolum>.json'a kanıtlı cümle olarak ekle, bolum_kontrol'den geçir; metin.md'yi uretim'den yeniden kur.")
        eksik = [c for c in cumleler if c not in govde]
        if eksik:
            hata.append(f"uretim cümlesi metin.md'de yok/değişmiş ({len(eksik)} adet, ilki: «{eksik[0][:80]}»). Yapılacak: metin.md'yi uretim cümlelerinden aynen kur.")

    # 3) Anahtar önceden var mı? (üstüne yazma / sürüm artırma yasağı)
    metin = KOK / "data" / "sesli_anlatim" / "metin" / f"{anahtar}.md"
    if not a.yayin and metin.exists():
        hata.append(f"{anahtar} zaten var; üstüne yazılmaz. Yeni çalıştırma = yeni etiket (v2/v3 YOK)")
    if (KOK / "data" / "sesli_anlatim" / "metin" / f"{a.ders}.md").exists() or True:
        pass  # Claude'un dersi referanstır; okunur, değiştirilmez (2. adım yakalar)

    # 4) Canlı kilit
    if a.yayin:
        if not a.canli:
            hata.append("--yayin için --canli <kök adres> gerekli")
        else:
            try:
                r = urllib.request.urlopen(f"{a.canli.rstrip('/')}/api/site-ayar", timeout=20)
                g = json.loads(r.read()).get("gorunurluk", {})
                for t in (f"sesli:{anahtar}",):
                    if g.get(t) not in ("yalniz-yonetici", "gizli"):
                        hata.append(f"canlıda {t} kapalı değil (değer: {g.get(t)!r}) — öğrenciye açık, HEMEN yöneticiye bildir")
            except Exception as e:  # noqa: BLE001
                hata.append(f"canlı site ayarı okunamadı: {e}")
            try:
                urllib.request.urlopen(f"{a.canli.rstrip('/')}/api/canli-ders/{anahtar}", timeout=20)
                hata.append("öğrenci isteği 200 döndü; 403 icerikKapali beklenirdi")
            except urllib.error.HTTPError as e:
                if e.code != 403:
                    uyari.append(f"öğrenci isteği {e.code} (403 beklenir)")
            except Exception as e:  # noqa: BLE001
                uyari.append(f"öğrenci isteği denenemedi: {e}")

    for u in uyari:
        print("UYARI", u)
    for h in hata:
        print("HATA", h)
    print(f"{'BAŞARISIZ' if hata else 'GEÇTİ'}: anahtar={anahtar} hata={len(hata)} uyarı={len(uyari)}")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
