#!/usr/bin/env python3
"""Tek hat koşucusu — sıralama artık insanda değil, TEK kaynakta (mod.py). (kullanıcı kararı 2026-11-16)

Hat tanımı eskiden 4 yerdeydi (hat.json, mod.py, ders_zinciri.py, el kitabı §19) ve E1–E6 sırası kafada tutuluyordu.
Bu koşucu tek doğruluk kaynağı `mod.py` KATMANLAR'dan sırayı okur; kipe (tam/tasarruf) göre atlanacakları eler; her
katman için YA betiği çalıştırır YA da LLM aşamasının kompakt brifini (read-once `baglam/`'ı okur, ham slayt/şablon değil) basar.

  kosucu.py <klasör> --ders <key> --mod tasarruf              → sıralı runbook (ne yapılacak, hangi komut/brif, hangi kapı)
  kosucu.py <klasör> --ders <key> --mod tasarruf --calistir   → betikle yapılabilen hazırlık adımlarını da çalıştırır (E0 + baglam + iskelet)
  kosucu.py <klasör> --ders <key> --mod tam --olc             → üretmeden aşama girdi kelime/token tablosu (meds_temp/hat_olcum/<key>.json)

LLM aşamaları (anlatım, örnek, önem/çözücü) yine ajan/model yazar; koşucu yalnız HANGİ sırayla + NE okuyarak (baglam) +
HANGİ kapıdan geçerek yapılacağını söyler. Böylece aynı kaynak defalarca okunmaz, sıra tek yerden gelir.

2026-11-17: her LLM aşaması TEK dosya okur — `baglam/is_<katman>.md` (kural paketi + şema + veri dilimleri) ya da veri dilimi
olmayan aşamada `baglam/kural_<aşama>.md`. Standart belgeler bütün okutulmaz (`kural_secici.py --paket`, BOLUM haritası).
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
import json
import subprocess
import time
import sys
from pathlib import Path

KOK = _kok.MEDS
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mod as MOD  # noqa: E402

# Katman → (evre, tür, açıklama). tür: "betik" (koşucu çalıştırabilir) / "llm" (ajan yazar, brif basılır) / "ses" (GPU/CPU).
# Komut/brif şablonlarında {k}=klasör, {d}=ders key, {m}=mod. Sıra mod.py KATMANLAR sırasıdır (tek kaynak).
EYLEM: dict[str, tuple[str, str, str]] = {
    "hazirlik":    ("E0", "betik", "python3 scripts/hat/tam_hat/hazirlik.py {k} --ders {d} --mod {m}  (kilit+denetle dahil; sonunda hoca_kirp.py + iskelet.py uret) && python3 scripts/hat/tam_hat/baglam.py {k} --ders {d} --mod {m} --kural-yalniz"),
    "degerlendirme": ("E1", "llm", "Değerlendirme paketi: baglam yoktur (paketi BU üretir). OKU (kural için TEK dosya) {k}/baglam/kural_kaynak.md + "
                                   "sayfalar.json + op/ + cikmis_aday.json + {k}/hoca_dokum_kirpik.md (HAM hoca_dokum.json DEĞİL; tek slaytın hamı gerekirse: "
                                   "hoca_kirp.py {k} --ham <slayt>). Üret: meds_database_v2/ders_bilgi/{d}/degerlendirme/paket.json + cikmis_konum. "
                                   "Kapı: degerlendirme_dogrula.py {d} --pdf {k}/orijinal.pdf → 0 HATA. SONRA: baglam üret."),
    "_baglam":     ("E1", "betik", "python3 scripts/hat/tam_hat/baglam.py {k} --ders {d} --mod {m} && python3 scripts/hat/tam_hat/iskelet.py uret {k} --ders {d}   (read-once: paket→baglam/is_<katman>.md [kural+şema+veri TEK dosya] + kural_<aşama>.md + kaynak_<dilim>.md + iskelet_<aşama>.json)"),
    "anlatim":     ("E2", "llm", "Anlatım konusma_v2: OKU yalnız 2 dosya — {k}/baglam/is_anlatim.md (kural paketi + şema + hoca vurguları/öğrenci önem; "
                                 "TEK okuma) + {k}/sayfalar.json (TAM slayt — `satir` çapası ve satır-birebir kapısı bunu gerektirir). "
                                 "Standart belgeleri/asama_kurallari'nı AYRICA açma. ÜRET {k}/anlatim/v2/konusma_v2.json "
                                 "(baglam/iskelet_anlatim.json'u doldur: b/p kimliği + sayfa hazır, cümle id'si boş → iskelet.py numarala {k}/anlatim/v2/konusma_v2.json --tur anlatim). "
                                 "TEK KAPI (4 kapı + satır bütünlüğü, tek çağrı; teslimden ÖNCE kendin çalıştır): python3 scripts/hat/tam_hat/anlatim_kapi.py {k}/anlatim/v2 "
                                 "--sayfalar {k}/sayfalar.json --key {d} → 0 HATA. Sonra bağımsız denetçi GEÇER."),
    "ders_ekle":   ("E2", "şablon", "python3 scripts/uretim/ogrenci_drive/sesli_yayinla.py --key {d} --no <N> --baslik \"<konu>\" --v2 {k}/anlatim/v2 --deck k2p-{d} --pdf-yol \"Kurul N/<branş>/<dosya>.pdf\" --pdf-ad \"<dosya>.pdf\" --sayfa <N> --file-id <drive-id>  (ders-özel değerler elle doldurulur; Oracle tüneli 3310 açık olmalı)"),
    "ema_ses":     ("E3", "ses", "EMA ses: ders-ekle kuyruğa koydu → meds-ema (CPU) üretir. Çözücü: ses.py --brans <brans> <kod> (CPU: CUDA_VISIBLE_DEVICES=)."),
    "zaman_isaret": ("E3", "betik", "cumle_zaman.py + kelime_zaman.py (ses sonrası, yalnız yeni klipler) + .venv-ocr/bin/python scripts/uretim/sesli_anlatim/pdf_isaret.py --key {d}. KAPI (H605, atlanamaz): .venv-ocr/bin/python scripts/uretim/sesli_anlatim/takip_kapisi.py {d} → 0 HATA; kelime_zaman/cumle_zaman dosyası yoksa ders yayına girmez."),
    "cikmis_chip": ("E3", "betik", "cikmis_konum.py --ders {d}  (yayınlı paragraflardan p/c)"),
    "cikmis_analiz": ("E3", "llm", "Ayrıntılı çıkmış analizi: OKU yalnız {k}/baglam/is_cikmis_analiz.md (şema + çıkmış + çıkmış slaytlarının atomları; TEK okuma). ÜRET ders_bilgi/{d}/degerlendirme/cikmis_analiz.json (baglam/iskelet_cikmis_analiz.json'u doldur; soru kimlikleri hazır; iskelet.py denetle). ders_analizi/uret.py önem listesi SONRASI. Kapı: ders_analizi/uret.py --dogrula {d}."),
    "terim_kisaltma": ("E3", "betik", "kisaltma_sozlugu.py otomatik {d} --yaz · terim_sozlugu.py otomatik {d} --yaz (MEDS_API=Oracle; yayın SONRASI canli-ders tazeyse)"),
    "onem_listesi": ("E2", "llm", "Önem listesi: OKU yalnız {k}/baglam/is_onem_listesi.md (kural paketi + §önem şeması + atom/hoca/çıkmış; TEK okuma). spot_cozucu çalışma dosyası onem/<kod>.json. Kapı: onem_dogrula.py → 0 HATA."),
    "ornek_soru":  ("E2", "llm", "Örnek sorular TEK kategori (kullanıcı kararı 2026-11-17): genel + hoca üslubu soruları AYNI dosyada (hoca üslubunda yazılan soruya `uslup: \"hoca\"`). "
                                 "Hoca üslubu YENİDEN BELİRLENMEZ/YAZILMAZ — baglam'daki hazır profil (profil_oku) ve varsa soru_uslubu.json kullanılır. Token en azda: kapsam kadar soru, uzun gerekçe yok. "
                                 "OKU yalnız {k}/baglam/is_ornek_soru.md (TEK okuma). ÜRET src/data/ornek_sorular/k2/{d}.json (baglam/iskelet_ornek_soru.json'u doldur; soru id → iskelet.py numarala <dosya> --tur ornek_soru) "
                                 "+ cozucu/<kod>.json — sesli çözücü dosyadaki TÜM soruları (hoca üslubu dahil) kapsar (AYRI alt ajan, önem listesi SONRASI: OKU yalnız {k}/baglam/is_cozucu.md + onem/<kod>.json). "
                                 "TEK KAPI (teslimden ÖNCE kendin çalıştır): python3 scripts/hat/tam_hat/ornek_soru_kapi.py src/data/ornek_sorular/k2/{d}.json "
                                 "--ders \"<ders>\" --sayfalar {k}/sayfalar.json [--uslup {k}/soru_uslubu.json] → 0 HATA. Çözücü ayrı: cozucu_dogrula. Ayrı hoca_uslubu_sorular / k2patolojihoca kartı ÜRETİLMEZ."),
    "hoca_sorulari": ("E2", "llm", "KAPALI (2026-11-17): hoca üslubu soruları ornek_soru katmanında tek kategoride. Eski hoca_uslubu_sorular/k2patolojihoca kayıtlarına dokunulmaz."),
    "ders_icerik": ("E3", "betik", "ders_icerik_uret.py {d} + ders_icerik_dogrula.py {d}  (terim/kısaltma+önem SONRASI)"),
    "capa_cizim":  ("E4", "llm", "Çapa + canlı çizim (capa_dok→çapa→cizim partileri→cizim_kapisi 0 HATA)."),
    "artik_capa":  ("E4", "llm", "Artık çapa (H605, her kipte; çapa+çizim SONRASI): .venv-ocr/bin/python scripts/uretim/sesli_anlatim/artik_capa.py hazirla {d} → "
                                 "OKU yalnız meds_temp/artik_capa/{d}/is.md (TEK dosya, görüntü AÇMA); YAZ meds_temp/artik_capa/{d}/cevap.json "
                                 "(cümle başına madde/resim ya da null; tahmin YASAK). Sonra artik_capa.py birlestir {d} → pdf_isaret + takip_kapisi 0 HATA. "
                                 "Artık cümle yoksa (hazirla 0 der) adım biter."),
    "ara_resim":   ("E4", "llm", "Ara resim katmanı (src/data/ara_resim) — YALNIZ kullanıcı isterse (MEDS_HAT_EKLE=ara_resim)."),
    "ara_soru":    ("E4", "llm", "Hocanın sorabileceği ara soru sayfası + k<N>hocaara sesi (kur.py dogrula --ses 0 HATA)."),
    "atomik_envanter": ("E3", "betik", "atomik_bilgi_envanteri (paket içinde; quiz KAPALI)."),
    "pdf_tasarim": ("E5", "betik", "ders_pdf.mts + pdf_tarama.py → 0 HATA"),
    "zengin_transkript": ("E3", "betik", "python3 scripts/uretim/sesli_anlatim/zengin_transkript.py {d} → 0 HATA (yapı kapısı aynı betikte; LLM yok, metin değişince yeniden koş)."),
    "ogren_deste": ("E2", "llm", "Öğren destesi (ASKIDA — üretilmez)."),
    "quiz":        ("E2", "betik", "quiz havuzu (KAPALI)."),
    "denetci":     ("E5", "llm", "Bütün betik kapıları + TEK bağımsız tıbbi denetçi (GEÇER). Denetçi kural için YALNIZ {k}/baglam/kural_denetci.md okur "
                                 "(yayın/dağıtım kurallarını DEĞİL) + katman dosyaları + sayfalar.json; çıktı denetim.json (kimlik bazlı bulgu). KALIR ise yalnız bulgu kimlikleri düzeltilir ve yalnız onlar yeniden denetlenir."),
    "betik_tamamla": ("E5", "betik", "python3 scripts/hat/tam_hat/betik_tamamla.py {d} [--gpu]  → LLM'siz katmanları (ders analizi, içerik paketi, zengin transkript, "
                                     "kelime zamanı) üretir ve 7 katman kapısını koşar; ✗ satırı düzeltme komutunu verir. Denetçiden ÖNCE; denetçiye eksik katmanla gidilmez."),
    "yayin":       ("E6", "betik", "python3 scripts/hat/tam_hat/betik_tamamla.py {d} --denetle (çıkış 0; eksik katmanla yayın YOK) → python3 scripts/kapilar/kos.py kayit (0 HATA, H610) → commit + bash deploy/oracle/dagit.sh + canlı doğrulama (kural: {k}/baglam/kural_yayin.md). SONRA: ders_kilit.py birak {d}."),
}


# Katman → kural_secici aşaması + baglam dilimleri + ek okunan dosyalar (ölçüm `--olc` için; brif metinleriyle aynı).
OKUMA: dict[str, tuple[str | None, tuple[str, ...], tuple[str, ...]]] = {
    # (2026-11-17) Aşama artık TEK dosya okur: baglam/is_<katman>.md (kural paketi + şema + veri) ya da kural_<aşama>.md.
    # İlk öge None = kural ayrı listeden değil, `ek`teki paket dosyasından sayılır.
    "degerlendirme": (None, (), ("baglam/kural_kaynak.md", "sayfalar.json", "cikmis_aday.json", "hoca_dokum_kirpik.md")),
    "anlatim": (None, (), ("baglam/is_anlatim.md", "sayfalar.json", "baglam/iskelet_anlatim.json")),
    "onem_listesi": (None, (), ("baglam/is_onem_listesi.md",)),
    "ornek_soru": (None, (), ("baglam/is_ornek_soru.md", "baglam/iskelet_ornek_soru.json")),
    "cikmis_analiz": (None, (), ("baglam/is_cikmis_analiz.md", "baglam/iskelet_cikmis_analiz.json")),
    "ornek_soru_cozucu": (None, (), ("baglam/is_cozucu.md",)),
    "ders_icerik": (None, (), ("baglam/kural_ders_icerik.md",)),
    "capa_cizim": (None, (), ("baglam/kural_capa_cizim.md",)),
    "pdf_tasarim": (None, (), ("baglam/kural_pdf_tasarim.md",)),
    "denetci": (None, (), ("baglam/kural_denetci.md",)),
}
TOKEN_KELIME = 1.6  # Türkçe metin: ≈1,6 token/kelime (önceki ölçümde 175k kelime ≈ 280k token)


def _kelime(p: Path) -> int:
    try:
        return len(p.read_text(encoding="utf-8", errors="replace").split())
    except OSError:
        return 0


def olc(klasor: Path, ders: str, mod: str) -> dict:
    """Hiçbir şey üretmeden aşama girdilerinin kelime/tahmini token toplamı. Eksik dosya 0 sayılır ve `eksik`te listelenir."""
    import kural_secici as KS
    yap = MOD.yapilacak(mod)
    satir, eksik = [], []
    for kat, (ks, dilim, ek) in OKUMA.items():
        if not yap.get(kat.replace("_cozucu", ""), False):
            continue
        kural = sum(_kelime(KOK / f) for f in (KS.oku(ks, mod) if ks else []))
        ozet = len(KS.ozet(ks).split()) if ks else 0
        dl = 0
        for x in dilim:
            f = klasor / "baglam" / f"kaynak_{x}.md"
            dl += _kelime(f)
            if not f.exists():
                eksik.append(str(f.relative_to(klasor)))
        ekk = {}
        for x in ek:
            ekk[x] = _kelime(klasor / x)
            if not (klasor / x).exists():
                eksik.append(x)
        top = kural + ozet + dl + sum(ekk.values())
        satir.append({"katman": kat, "kural": kural, "ozet": ozet, "dilim": dl, "ek": ekk, "toplam": top,
                      "token": round(top * TOKEN_KELIME), "dosya": len(dilim) + len(ek)})
    ham = _kelime(klasor / "hoca_dokum.json")
    return {"ders": ders, "mod": mod, "zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "satirlar": satir,
            "toplam_dosya": sum(x["dosya"] for x in satir),
            "toplam_kelime": sum(x["toplam"] for x in satir), "toplam_token": sum(x["token"] for x in satir),
            "hoca_dokum_ham_kelime": ham, "eksik": sorted(set(eksik))}


def olc_bas(o: dict) -> None:
    print(f"# Girdi ölçümü — {o['ders']} · kip {o['mod']} (üretim yok; token ≈ kelime × {TOKEN_KELIME})")
    print(f"{'katman':<15}{'kural':>8}{'özet':>6}{'dilim':>7}{'ek':>8}{'toplam':>8}{'token':>8}  ek dosyalar")
    for x in o["satirlar"]:
        print(f"{x['katman']:<15}{x['kural']:>8}{x['ozet']:>6}{x['dilim']:>7}{sum(x['ek'].values()):>8}{x['toplam']:>8}{x['token']:>8}  "
              + ", ".join(f"{k}={v}" for k, v in x["ek"].items()))
    print(f"{'TOPLAM':<44}{o['toplam_kelime']:>8}{o['toplam_token']:>8}   okunan dosya: {o.get('toplam_dosya', '?')}")
    if o["hoca_dokum_ham_kelime"]:
        print(f"(değerlendirme HAM hoca_dokum.json okusaydı: +{o['hoca_dokum_ham_kelime']} kelime)")
    if o["eksik"]:
        print("eksik (0 sayıldı): " + ", ".join(o["eksik"]))


def manifest_komutu(d: str, katman: str) -> str:
    return f"python3 scripts/hat/tam_hat/manifest.py uret {d} --kapi-sonucu {katman}=<gecti|kaldi>"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("klasor", type=Path)
    ap.add_argument("--ders", required=True)
    ap.add_argument("--mod", choices=MOD.KIPLER, default="tam")
    ap.add_argument("--calistir", action="store_true", help="betikle yapılabilen hazırlık adımlarını çalıştır (E0 + baglam)")
    ap.add_argument("--sentez", action="store_true",
                    help="YÖNETİCİ AÇAR (varsayılan kapalı): PDF görsel okumasını sentez.py ile daralt — metin betikle, PNG yalnız "
                         "temas sayfasında seçilen sayfada (TAM_HAT_HIZLI_AKIS §0.0c). Belirtilmezse standart yol (her sayfa PNG).")
    ap.add_argument("--olc", action="store_true", help="üretmeden aşama girdi kelime/token tablosu → meds_temp/hat_olcum/<key>.json")
    a = ap.parse_args()
    if a.olc:
        o = olc(a.klasor, a.ders, a.mod)
        olc_bas(o)
        hedef = KOK.parent / "meds_temp" / "hat_olcum" / f"{a.ders}.json"
        hedef.parent.mkdir(parents=True, exist_ok=True)
        gecmis = json.loads(hedef.read_text(encoding="utf-8")) if hedef.exists() else {"olcumler": []}
        gecmis["olcumler"].append(o)
        hedef.write_text(json.dumps(gecmis, ensure_ascii=False, indent=1), encoding="utf-8")
        if len(gecmis["olcumler"]) > 1:
            p = gecmis["olcumler"][-2]
            print(f"önceki ölçüm ({p['zaman']}): {p['toplam_kelime']} kelime → fark {o['toplam_kelime'] - p['toplam_kelime']:+d}")
        print(f"yazıldı: {hedef}")
        return 0
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
    print(f"# Tek hat runbook — {a.ders} · kip {a.mod} (tek kaynak: mod.py)" + (" · SENTEZ okuma açık (yönetici)" if a.sentez else "") + "\n")
    if a.sentez:
        print("  [SENTEZ] PDF okuyan aşamalar (değerlendirme/anlatım) op/ PNG'lerini toptan AÇMAZ: önce baglam/sentez.md + temas_N.png, "
              "yalnız seçilen sayfanın PNG'si (sentez_secim.json). Kapılar ve denetçi aynen.\n")
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
            if not atla and k != "_baglam":  # her aşama/kapı sonunda katman manifestine sonuç işlenir (manifest.py, kapıyı çalıştırmaz)
                print(f"  {'':<7} {'':<15} ↳ kapı sonrası: {manifest_komutu(a.ders, k)}")
            if k == "yayin" and not atla:
                r = subprocess.run([sys.executable, "scripts/hat/tam_hat/manifest.py", "goster", a.ders, "--eksik"],
                                   cwd=KOK, capture_output=True, text=True)
                print("  ── yayın öncesi manifest (eksikler; ENGELLEMEZ, yalnız bilgi) ──")
                for ln in (r.stdout or r.stderr).strip().splitlines():
                    print("     " + ln)
        if basildi:
            print()
    # Paralel brif: bağımlılık düzeyine göre (mod.py BAGIMLILIK). Koşucu LLM başlatmaz; yalnız hangi aşamaların AYNI ANDA
    # alt ajana verilebileceğini söyler. Ders kilidi ders düzeyindedir (aşama düzeyinde çakışma koruması YOK): aynı
    # MEDS_OTURUM altındaki paralel alt ajanlar farklı çıktı dosyalarına yazdığı için güvenlidir; aynı dosyaya iki ajan yazmasın.
    print("## Birlikte başlatılabilir gruplar (bağımlılık: mod.py BAGIMLILIK; alt ajan en çok 3)")
    for i, g in enumerate(MOD.paralel_gruplar(a.mod)):
        llm = [k for k in g if EYLEM.get(k, ("", "", ""))[1] == "llm"]
        print(f"  G{i}: {' ∥ '.join(g)}" + (f"   (LLM: {', '.join(llm)})" if llm and len(g) > 1 else ""))
    print()
    if a.calistir:
        # Oturum sahibi koşucudur: kararlı MEDS_OTURUM üret + alt adımlara geçir → kilit tek kimlikle tutulur,
        # yayın adımında `ders_kilit.py birak {d}` ile bırakılır (runbook E6'da yazılı). Varsa dışarıdan geleni koru.
        import os
        env = dict(os.environ)
        env.setdefault("MEDS_OTURUM", f"kosucu-{a.ders}-{os.getpid()}")
        print(f"## Çalıştırılıyor (E0 + baglam) · oturum {env['MEDS_OTURUM']}…")
        # Argümanlar liste olarak (shell yok): enjeksiyon riski yok, ders/klasör metakarakterleri yorumlanmaz.
        adimlar = [("hazirlik", ["python3", "scripts/hat/tam_hat/hazirlik.py", str(a.klasor), "--ders", a.ders, "--mod", a.mod])]
        if a.sentez:  # yönetici kararı; açılmazsa hiçbir şey değişmez
            adimlar.append((None, ["python3", "scripts/hat/tam_hat/sentez.py", str(a.klasor)]))
        adimlar.append((None, ["python3", "scripts/hat/tam_hat/baglam.py", str(a.klasor), "--ders", a.ders, "--mod", a.mod, "--kural-yalniz"]))
        if (KOK.parent / "meds_database_v2" / "ders_bilgi" / a.ders / "degerlendirme" / "paket.json").exists():
            adimlar += [(None, ["python3", "scripts/hat/tam_hat/baglam.py", str(a.klasor), "--ders", a.ders, "--mod", a.mod]),
                        (None, ["python3", "scripts/hat/tam_hat/iskelet.py", "uret", str(a.klasor), "--ders", a.ders])]
        for katman, cmd in adimlar:
            print("$ " + " ".join(cmd))
            r = subprocess.run(cmd, cwd=KOK, env=env)
            if katman:
                subprocess.run(["python3", "scripts/hat/tam_hat/manifest.py", "uret", a.ders, "--kapi-sonucu",
                                f"{katman}={'gecti' if r.returncode == 0 else 'kaldi'}"], cwd=KOK)
            if r.returncode != 0:
                print(f"DURDU: {cmd[1]} çıkış {r.returncode}", file=sys.stderr)
                return r.returncode
        print(f"NOT: ders kilidi oturum '{env['MEDS_OTURUM']}' ile tutuluyor; yayın bitince: "
              f"MEDS_OTURUM='{env['MEDS_OTURUM']}' python3 scripts/hat/tam_hat/ders_kilit.py birak {a.ders}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
