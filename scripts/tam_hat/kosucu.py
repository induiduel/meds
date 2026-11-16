#!/usr/bin/env python3
"""Tek hat koşucusu — sıralama artık insanda değil, TEK kaynakta (mod.py). (kullanıcı kararı 2026-11-16)

Hat tanımı eskiden 4 yerdeydi (hat.json, mod.py, ders_zinciri.py, el kitabı §19) ve E1–E6 sırası kafada tutuluyordu.
Bu koşucu tek doğruluk kaynağı `mod.py` KATMANLAR'dan sırayı okur; kipe (tam/tasarruf) göre atlanacakları eler; her
katman için YA betiği çalıştırır YA da LLM aşamasının kompakt brifini (read-once `baglam/`'ı okur, ham slayt/şablon değil) basar.

  kosucu.py <klasör> --ders <key> --mod tasarruf              → sıralı runbook (ne yapılacak, hangi komut/brif, hangi kapı)
  kosucu.py <klasör> --ders <key> --mod tasarruf --calistir   → betikle yapılabilen hazırlık adımlarını da çalıştırır (E0 + baglam)

LLM aşamaları (anlatım, örnek, önem/çözücü) yine ajan/model yazar; koşucu yalnız HANGİ sırayla + NE okuyarak (baglam) +
HANGİ kapıdan geçerek yapılacağını söyler. Böylece aynı kaynak defalarca okunmaz, sıra tek yerden gelir.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mod as MOD  # noqa: E402

# Katman → (evre, tür, açıklama). tür: "betik" (koşucu çalıştırabilir) / "llm" (ajan yazar, brif basılır) / "ses" (GPU/CPU).
# Komut/brif şablonlarında {k}=klasör, {d}=ders key, {m}=mod. Sıra mod.py KATMANLAR sırasıdır (tek kaynak).
EYLEM: dict[str, tuple[str, str, str]] = {
    "hazirlik":    ("E0", "betik", "python3 scripts/tam_hat/hazirlik.py {k} --ders {d} --mod {m}  (kilit+denetle dahil)"),
    "degerlendirme": ("E1", "llm", "Değerlendirme paketi: baglam yoktur (paketi BU üretir). Oku: sayfalar.json + op/ + cikmis_aday.json + "
                                   "docs/asama_kurallari/kaynak.md. Üret: meds_database_v2/ders_bilgi/{d}/degerlendirme/paket.json + cikmis_konum. "
                                   "Kapı: degerlendirme_dogrula.py {d} --pdf {k}/orijinal.pdf → 0 HATA. SONRA: baglam üret."),
    "_baglam":     ("E1", "betik", "python3 scripts/tam_hat/baglam.py {k} --ders {d} --mod {m}   (read-once: paket→baglam/kaynak.md+sema.md)"),
    "anlatim":     ("E2", "llm", "Anlatım konusma_v2: OKU {k}/sayfalar.json (TAM slayt — `satir` çapası ve --dogrula satır-birebir kapısı "
                                 "bunu gerektirir; baglam/kaynak YETMEZ, kapıyı zayıflatır — ölçüm 2026-11-16) + baglam/sema.md (§anlatım) + "
                                 "docs/asama_kurallari/anlatim.md. ÜRET {k}/anlatim/v2/konusma_v2.json. "
                                 "TEK KAPI (4 kapı + satır bütünlüğü, tek çağrı): python3 scripts/tam_hat/anlatim_kapi.py {k}/anlatim/v2 "
                                 "--sayfalar {k}/sayfalar.json --key {d} → 0 HATA. Sonra bağımsız denetçi GEÇER."),
    "ders_ekle":   ("E2", "şablon", "python3 scripts/ogrenci_drive/sesli_yayinla.py --key {d} --no <N> --baslik \"<konu>\" --v2 {k}/anlatim/v2 --deck k2p-{d} --pdf-yol \"Kurul N/<branş>/<dosya>.pdf\" --pdf-ad \"<dosya>.pdf\" --sayfa <N> --file-id <drive-id>  (ders-özel değerler elle doldurulur; Oracle tüneli 3310 açık olmalı)"),
    "ema_ses":     ("E3", "ses", "EMA ses: ders-ekle kuyruğa koydu → meds-ema (CPU) üretir. Çözücü: ses.py --brans <brans> <kod> (CPU: CUDA_VISIBLE_DEVICES=)."),
    "zaman_isaret": ("E3", "betik", "cumle_zaman.py / kelime_zaman.py (ses sonrası, yalnız yeni klipler)"),
    "cikmis_chip": ("E3", "betik", "cikmis_konum.py --ders {d}  (yayınlı paragraflardan p/c)"),
    "cikmis_analiz": ("E3", "llm", "Ayrıntılı çıkmış analizi: OKU baglam/kaynak.md (§çıkmış). ÜRET ders_bilgi/{d}/degerlendirme/cikmis_analiz.json. Kapı: ders_analizi/uret.py --dogrula {d}."),
    "terim_kisaltma": ("E3", "betik", "kisaltma_sozlugu.py otomatik {d} --yaz · terim_sozlugu.py otomatik {d} --yaz (MEDS_API=Oracle; yayın SONRASI canli-ders tazeyse)"),
    "onem_listesi": ("E2", "llm", "Önem listesi: OKU baglam/kaynak.md + baglam/sema.md (§önem). spot_cozucu çalışma dosyası onem/<kod>.json. Kapı: onem_dogrula.py → 0 HATA."),
    "ornek_soru":  ("E2", "llm", "Örnek sorular + çözücü: OKU baglam/kaynak.md + baglam/sema.md (§örnek, §çözücü) + docs/asama_kurallari/ornek_soru.md. "
                                 "ÜRET src/data/ornek_sorular/k2/{d}.json + cozucu/<kod>.json. "
                                 "TEK KAPI örnek soru (4 kapı tek çağrıda): python3 scripts/tam_hat/ornek_soru_kapi.py src/data/ornek_sorular/k2/{d}.json "
                                 "--uslup {k}/soru_uslubu.json --ders \"<ders>\" --sayfalar {k}/sayfalar.json → 0 HATA. Çözücü ayrı: cozucu_dogrula."),
    "hoca_sorulari": ("E2", "llm", "(Yalnız patoloji) Hoca soruları kartı + sesli hoca çözücü — patoloji_soru_isci akışı."),
    "ders_icerik": ("E3", "betik", "ders_icerik_uret.py {d} + ders_icerik_dogrula.py {d}  (terim/kısaltma+önem SONRASI)"),
    "capa_cizim":  ("E4", "llm", "Çapa + canlı çizim (capa_dok→çapa→cizim partileri→cizim_kapisi 0 HATA)."),
    "ara_resim":   ("E4", "llm", "Ara resim katmanı (src/data/ara_resim)."),
    "ara_soru":    ("E4", "llm", "Hocanın sorabileceği ara soru sayfası + k<N>hocaara sesi (kur.py dogrula --ses 0 HATA)."),
    "atomik_envanter": ("E3", "betik", "atomik_bilgi_envanteri (paket içinde; quiz KAPALI)."),
    "pdf_tasarim": ("E5", "betik", "ders_pdf.mts + pdf_tarama.py → 0 HATA"),
    "ogren_deste": ("E2", "llm", "Öğren destesi (ASKIDA — üretilmez)."),
    "quiz":        ("E2", "betik", "quiz havuzu (KAPALI)."),
    "denetci":     ("E5", "llm", "Bütün betik kapıları + TEK bağımsız tıbbi denetçi (GEÇER)."),
    "yayin":       ("E6", "betik", "commit + bash deploy/oracle/dagit.sh + canlı doğrulama. SONRA: ders_kilit.py birak {d}."),
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("klasor", type=Path)
    ap.add_argument("--ders", required=True)
    ap.add_argument("--mod", choices=MOD.KIPLER, default="tam")
    ap.add_argument("--calistir", action="store_true", help="betikle yapılabilen hazırlık adımlarını çalıştır (E0 + baglam)")
    a = ap.parse_args()
    yap = MOD.yapilacak(a.mod)
    # mod.py sırası + araya _baglam (E1 paketten sonra). Atlananları (kipte False) eler.
    sira: list[str] = []
    for k, *_ in MOD.KATMANLAR:
        sira.append(k)
        if k == "degerlendirme":
            sira.append("_baglam")
    rep = {"{k}": str(a.klasor), "{d}": a.ders, "{m}": a.mod}
    def doldur(s: str) -> str:
        for x, y in rep.items():
            s = s.replace(x, y)
        return s
    print(f"# Tek hat runbook — {a.ders} · kip {a.mod} (tek kaynak: mod.py)\n")
    evre_sira = ["E0", "E1", "E2", "E3", "E4", "E5", "E6"]
    for ev in evre_sira:
        basildi = False
        for k in sira:
            e = EYLEM.get(k)
            if not e or e[0] != ev:
                continue
            atla = (k != "_baglam") and (not yap.get(k, True))
            if not basildi:
                print(f"## {ev}")
                basildi = True
            durum = "ATLA" if atla else ("BETİK" if e[1] == "betik" else e[1].upper())
            print(f"  [{durum:<5}] {k:<15} {doldur(e[2])}")
        if basildi:
            print()
    if a.calistir:
        # Oturum sahibi koşucudur: kararlı MEDS_OTURUM üret + alt adımlara geçir → kilit tek kimlikle tutulur,
        # yayın adımında `ders_kilit.py birak {d}` ile bırakılır (runbook E6'da yazılı). Varsa dışarıdan geleni koru.
        import os
        env = dict(os.environ)
        env.setdefault("MEDS_OTURUM", f"kosucu-{a.ders}-{os.getpid()}")
        print(f"## Çalıştırılıyor (E0 + baglam) · oturum {env['MEDS_OTURUM']}…")
        # Argümanlar liste olarak (shell yok): enjeksiyon riski yok, ders/klasör metakarakterleri yorumlanmaz.
        adimlar = [["python3", "scripts/tam_hat/hazirlik.py", str(a.klasor), "--ders", a.ders, "--mod", a.mod],
                   ["python3", "scripts/tam_hat/baglam.py", str(a.klasor), "--ders", a.ders, "--mod", a.mod]]
        for cmd in adimlar:
            print("$ " + " ".join(cmd))
            r = subprocess.run(cmd, cwd=KOK, env=env)
            if r.returncode != 0:
                print(f"DURDU: {cmd[1]} çıkış {r.returncode}", file=sys.stderr)
                return r.returncode
        print(f"NOT: ders kilidi oturum '{env['MEDS_OTURUM']}' ile tutuluyor; yayın bitince: "
              f"MEDS_OTURUM='{env['MEDS_OTURUM']}' python3 scripts/tam_hat/ders_kilit.py birak {a.ders}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
