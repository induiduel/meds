#!/usr/bin/env python3
"""İnteraktif Öğrenme Desteleri — EMA Lightning ile Adım Seslendirme (YALNIZ CPU).

Girdi : meds/src/data/interactive_learning_decks.json
Çıktı : meds/data/ogren_ses/<deck_id>/<adim_no>.mp3 + kayit.json {<adim_no>: {h, sure, zaman: [...]}}

Kullanım:
  ~/.local/share/meds-ema/venv/bin/python scripts/ogren_ses/ogren_ses_uret.py [deck_id ...]
  Varsayılan deste: k1p-k1-11-uriner-obstruksiyonun-fizyopatolojisi-v2
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

# GPU kuralı: EMA_CIHAZ cuda değilse GPU yasak
if os.environ.get("EMA_CIHAZ") != "cuda":
    os.environ["CUDA_VISIBLE_DEVICES"] = ""

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / "scripts/sesli_anlatim"))
import ema_isci as E  # noqa: E402

E.KBPS = 48
SURUM = "ema-1"
SURUM_K2 = "ema-2"  # Kurul 2+: kisaltma_ses.uzat okunuşu (H3)
CUMLE_SN, KISA_SN, UZUN_SN, ON_SN = 0.45, 0.3, 0.7, 0.12

DECKS_FILE = MEDS / "src/data/interactive_learning_decks.json"
CIKTI_KOK = MEDS / "data/ogren_ses"


def temizle_markdown(s: str) -> str:
    s = re.sub(r"\[\[([^\]|]+)(\|[^\]]+)?\]\]", r"\1", s)
    s = re.sub(r"[*_`#=~]", "", s)
    s = re.sub(r">\s*\[!\w+\]", "", s)
    s = re.sub(r"^\s*[-*•]\s+", "", s, flags=re.MULTILINE)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def slide_metni(slide: dict, index: int) -> str:
    """LessonPlayer.tsx'teki text() fonksiyonunun birebir Python karşılığı."""
    raw_title = str(slide.get("title") or f"Adım {index + 1}")
    title = re.sub(
        r"^\s*\[(?:TEKRAR SAYFASI\s*-\s*CHECKPOINT\s*\d+|CHECKPOINT\s*\d+|OYUN SAYFASI)[^\]]*\]\s*",
        "",
        raw_title,
    ).strip()

    subtitle = str(slide.get("subtitle") or "").strip()

    cc = slide.get("coreContent") if isinstance(slide.get("coreContent"), dict) else {}
    narrative = str(slide.get("synthesisNarrative") or slide.get("content") or cc.get("text") or "").strip()

    bullets = cc.get("keyBullets") if isinstance(cc.get("keyBullets"), list) else []
    bullets = [b for b in bullets if isinstance(b, dict) and (b.get("title") or b.get("desc"))]
    keys: list[str] = []
    if len(bullets) > 1 or not narrative:
        for b in bullets:
            bt = str(b.get("title") or "").strip()
            bd = str(b.get("desc") or "").strip()
            if bt and bd:
                keys.append(f"{bt}: {bd}")
            elif bt or bd:
                keys.append(bt or bd)

    parts = [p for p in [title, subtitle, narrative] + keys if p]
    metin = ". ".join(parts)
    return temizle_markdown(metin)


def cumlelere_ayir(metin: str) -> list[str]:
    # Cümle sonlarına göre böl (. ! ?)
    raw = [c.strip() for c in re.split(r"(?<=[.!?])\s+", metin.strip()) if c.strip()]
    out: list[str] = []
    for c in raw:
        # Sonunda noktalama yoksa nokta ekle
        if c[-1:] not in ".!?":
            c = c + "."
        out.append(c)
    return out


def seslendir(tts, cumleler: list[str]):
    import numpy as np

    sessiz = lambda sn: np.zeros(int(round(sn * E.SR)), dtype=np.float32)  # noqa: E731
    parca, zaman, t, notlar = [sessiz(ON_SN)], [], ON_SN, []

    for c in cumleler:
        bas = t
        for par, ayrac in re.findall(r"(.+?)(\|\||\||$)", c.strip()):
            par = par.strip()
            if not par:
                continue
            wav, n = E.paragraf_seslendir(tts, par)
            if n:
                notlar.append(f"{n}: {par[:50]}")
            parca.append(wav)
            t += len(wav) / E.SR
            if ayrac:
                d = UZUN_SN if ayrac == "||" else KISA_SN
                parca.append(sessiz(d))
                t += d
        zaman.append([bas, t])
        parca.append(sessiz(CUMLE_SN))
        t += CUMLE_SN

    x = np.concatenate(parca)
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()
    mp3 = E.mp3_kodla(pcm)
    gercek = len(mp3) * 8 / (E.KBPS * 1000)
    k = gercek / (len(x) / E.SR)
    return mp3, [[round(a * k, 3), round(b * k, 3)] for a, b in zaman], round(gercek, 3), notlar


def deste_uret(tts, deck: dict, force: bool = False, adim_filtre: int | None = None) -> dict:
    deck_id = deck["id"]
    E.uzun_kisaltma_ayarla(deck_id)
    deck_title = deck.get("title", deck_id)
    slides = deck.get("slides") or []
    cikis_dizin = CIKTI_KOK / deck_id
    cikis_dizin.mkdir(parents=True, exist_ok=True)

    kayit_yolu = cikis_dizin / "kayit.json"
    kayit: dict = {}
    if kayit_yolu.exists():
        try:
            kayit = json.loads(kayit_yolu.read_text(encoding="utf-8"))
        except Exception:
            kayit = {}

    print(f"\n=======================================================")
    print(f"Deste: {deck_title} ({deck_id})")
    print(f"Toplam Slayt/Adım: {len(slides)}")
    print(f"=======================================================")

    t0 = time.time()
    uretilen = 0
    atlanilan = 0
    toplam_sure = 0.0

    for i, slide in enumerate(slides):
        adim_no = slide.get("slideNumber") or (i + 1)
        if adim_filtre is not None and adim_no != adim_filtre:
            continue

        metin = slide_metni(slide, i)
        cumleler = cumlelere_ayir(metin)
        if not cumleler:
            print(f"  [Adım {adim_no:2d}] METİN BOŞ — Atlandı")
            continue

        # Kurul 2+ desteleri uzun harf okunuşuyla (ema-2); Kurul 1 ema-1'de kalır (toplu yeniden üretim yok)
        h = hashlib.sha1(((SURUM_K2 if E.UZUN_KISALTMA else SURUM) + f"|{E.HIZ}|" + "\n".join(cumleler) + E.okunus.sayi_imi(cumleler)).encode()).hexdigest()[:12]
        mp3_yolu = cikis_dizin / f"{adim_no}.mp3"

        mevcut = kayit.get(str(adim_no))
        if not force and mevcut and mevcut.get("h") == h and mp3_yolu.exists():
            atlanilan += 1
            toplam_sure += float(mevcut.get("sure", 0))
            continue

        t_adim = time.time()
        mp3, zamanlar, sure, notlar = seslendir(tts, cumleler)
        mp3_yolu.write_bytes(mp3)

        kayit[str(adim_no)] = {
            "h": h,
            "sure": sure,
            "zaman": zamanlar,
            "cumleler": cumleler,
            "guncellendi": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        uretilen += 1
        toplam_sure += sure
        dt = time.time() - t_adim

        print(
            f"  [Adım {adim_no:2d}/{len(slides)}] {sure:4.1f} sn ses üretildi ({dt:4.1f} sn'de) | {len(cumleler)} cümle"
        )
        if notlar:
            for n in notlar:
                print(f"    ! {n}")

        # Her 5 adımda bir kayit.json'u diske yaz
        if uretilen % 5 == 0:
            kayit_yolu.write_text(json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")

    # Son kayıt
    kayit_yolu.write_text(json.dumps(kayit, ensure_ascii=False, indent=2), encoding="utf-8")
    toplam_gecen = time.time() - t0
    print(f"\n--- Sonuç: {deck_id} ---")
    print(f"Üretilen: {uretilen}, Atlanılan (Değişmeyen): {atlanilan}")
    print(f"Toplam Ses Süresi: {toplam_sure/60:.1f} dk, Üretim Süresi: {toplam_gecen:.1f} sn")
    return {"uretilen": uretilen, "atlanilan": atlanilan, "toplam_sure": toplam_sure, "cikis": cikis_dizin}


def deste_onceligi(deck_id: str) -> tuple[int, str]:
    # 0: Güncel müfredat v2 desteleri
    if "-v2" in deck_id:
        return (0, deck_id)
    # 1: k1p desteleri
    if deck_id.startswith("k1p-"):
        return (1, deck_id)
    # 2: learn- ve diğer desteler
    return (2, deck_id)


def main():
    import subprocess
    parser = argparse.ArgumentParser(description="İnteraktif Öğrenme Desteleri için EMA Seslendirici")
    parser.add_argument("deck_ids", nargs="*", help="İşlenecek deste kimlikleri (boşsa varsayılan üriner obstrüksiyon)")
    parser.add_argument("--hepsi", action="store_true", help="Tüm interaktif desteleri işle")
    parser.add_argument("--v2", action="store_true", help="Yalnızca güncel -v2 destelerini işle")
    parser.add_argument("--force", action="store_true", help="Var olan sesleri yeniden üret")
    parser.add_argument("--adim", type=int, default=None, help="Yalnızca belirtilen adım numarasını üret")
    parser.add_argument("--oracle", action="store_true", help="Her deste bittiğinde Oracle sunucusuna rsync ile aktar")
    args = parser.parse_args()

    if not DECKS_FILE.exists():
        print(f"HATA: {DECKS_FILE} bulunamadı!")
        sys.exit(1)

    with open(DECKS_FILE, encoding="utf-8") as f:
        all_decks = json.load(f)

    deck_map = {d["id"]: d for d in all_decks}

    hedefler = []
    if args.hepsi:
        hedefler = sorted(list(deck_map.keys()), key=deste_onceligi)
    elif args.v2:
        hedefler = sorted([k for k in deck_map if "-v2" in k], key=deste_onceligi)
    elif args.deck_ids:
        for did in args.deck_ids:
            if did in deck_map:
                hedefler.append(did)
            else:
                # Kısmi eşleşme dene
                eslesen = [k for k in deck_map if did in k]
                if eslesen:
                    hedefler.extend(eslesen)
                else:
                    print(f"UYARI: '{did}' ile eşleşen deste bulunamadı!")
    else:
        # Varsayılan: Kullanıcının ekran görüntüsündeki deste
        hedefler = ["k1p-k1-11-uriner-obstruksiyonun-fizyopatolojisi-v2"]

    if not hedefler:
        print("İşlenecek deste bulunamadı.")
        sys.exit(1)

    print(f"İşlenecek deste sayısı: {len(hedefler)}")
    print(f"EMA Lightning yükleniyor...")
    tts = E.model_yukle()

    toplam_deste = len(hedefler)
    for idx, did in enumerate(hedefler, 1):
        deck = deck_map.get(did)
        if deck:
            print(f"\n>>> [{idx}/{toplam_deste}] Deste Başlıyor: {did}")
            res = deste_uret(tts, deck, force=args.force, adim_filtre=args.adim)
            if args.oracle and res.get("uretilen", 0) > 0:
                print(f"  [Oracle] {did} aktarılıyor...")
                r = subprocess.run(["rsync", "-az", "--quiet", str(res["cikis"]), "medsor-oracle:/home/ubuntu/medsor/meds/data/ogren_ses/"])
                if r.returncode == 0:
                    print(f"  [Oracle] {did} başarıyla senkronize edildi.")
                else:
                    print(f"  [Oracle] UYARI: {did} aktarılamadı (kod {r.returncode})")
            # GPU sıcaklığını korumak için desteler arası kısa nefes
            time.sleep(0.5)


if __name__ == "__main__":
    main()
