"""Ders işçisinin PARALEL üretimi (kullanıcı kararı 2026-10-24: "deste bölümleri, ders notu, sorular, sesli metin aynı anda").

Eskiden tek Claude oturumu TALIMAT.md'deki her çıktıyı SIRAYLA yazıyordu (62 sayfalık derste 1–3 saat). Şimdi:
  1. iskelet  (tek çağrı): ders_paketi.json + sayfa_haritasi.json — diğer her şeyin omurgası (bilgi maddeleri, ana
     başlıklar ve adım aralıkları).
  2. paralel  (ayar `paralel`, varsayılan 4 eşzamanlı oturum; her biri ayrı dosya yazar, kendi bağlamında):
       deck_parca/<başlık>.json  — her ANA başlığın slaytları (o başlığın adım aralığı + sonunda checkpoint)
       deck_ust.json             — deste üst bilgisi + ders sonu oyun sayfası
       ders_notu.md
       ornek_sorular.json + cikmis_baglantilari.json
       sozluk.json + hastaliklar.json + bilgi_havuzu.jsonl
       sesli metin (konusma_metni: kendi oturumu, kendi denetimi)
  3. birleştir (betik): deck_ust + parçalar → deck.json (slideNumber/checkpointNumber yeniden), rapor.md yoksa betikle.
Sonra isle.py'nin denetim + düzeltme turları aynen çalışır (tek oturum, yalnız hatalar).
Kronoloji: bir başlığın etkileşimleri yalnız o başlıkta ve ÖNCEKİ başlıklarda anlatılanla kurulur (yazar önceki
başlıkların adım/özetlerini sayfa_haritasi'ndan bilir; parçalar aynı anda yazıldığı için sonraki başlığı görmez).
"""
from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from ayarlar import APP, ayar, log, oku, yaz

TALIMAT = Path(__file__).resolve().parent / "TALIMAT.md"
REHBER = APP / "docs" / "OGREN_ETKILESIM_REHBERI.md"


EK = {"metin": ""}   # isle.py: yönetici düzeltme notu + öğrenci notu açıklaması (her parçanın istemine eklenir)


def _on(d: Path) -> str:
    return EK["metin"] + (f"Talimat dosyası: {TALIMAT} (içindeki /app yolları bu makinede {APP} kökündedir; Öğren rehberi {REHBER}). "
            "Çalışma dizinindeki baglam.json ve kaynak.md'yi oku. ")


def ana_basliklar(d: Path) -> list[dict]:
    h = oku(d / "sayfa_haritasi.json", {}) or {}
    return [b for b in h.get("basliklar", []) if not b.get("ust") and isinstance(b.get("adimlar"), list) and len(b["adimlar"]) == 2]


def _isler(d: Path) -> list[tuple[str, str, list[str]]]:
    """(ad, istem, beklenen dosyalar) — yalnız henüz yazılmamış parçalar."""
    on = _on(d)
    on += "ders_paketi.json ve sayfa_haritasi.json YAZILDI (değiştirme); bunlara dayan. "
    isler = []
    basl = ana_basliklar(d)
    for i, b in enumerate(basl):
        hedef = f"deck_parca/{b['no']}.json"
        if (d / hedef).exists():
            continue
        onceki = "; ".join(f"{x['no']}. {x['baslik']} (adım {x['adimlar'][0]}–{x['adimlar'][1]})" for x in basl[:i]) or "yok"
        isler.append((f"deste {b['no']}", on + (
            f"Görevin: TALIMAT §3 deck.json kurallarıyla YALNIZ ana başlık {b['no']} '{b['baslik']}' için içerik adımları "
            f"{b['adimlar'][0]}–{b['adimlar'][1]} (sayfalar {b.get('sayfalar')}) slaytlarını yaz; başlığın sonuna bu başlığı "
            f"pekiştiren bir '[TEKRAR SAYFASI - CHECKPOINT] {b['baslik']}' slaytı ekle. Önceki başlıklar (anlatılmış sayılır): "
            f"{onceki}. Sonraki başlıkların bilgisi etkileşimlere GİREMEZ. Ders sonu oyun sayfası YAZMA (ayrı iş). "
            f"Rehberi oku. Çıktı: {hedef} dosyasına yalnız {{\"slides\": [...]}} JSON'u (slaytlar talimattaki alanlarla, "
            f"her içerik slaytında bolum/pdfSayfalari/sourcePdf). Başka dosyaya dokunma; bitince tek satır: BİTTİ."), [hedef]))
    if not (d / "deck_ust.json").exists():
        isler.append(("deste üstü + oyun", on + (
            "Görevin: TALIMAT §3'e göre destenin ÜST bilgisini (id, title, shortTitle, discipline, committee, instructor, "
            "matchedNoteId, overview, highYieldPearls) ve ders sonu OYUN SAYFASINI (son slayt, isGameFinale: true; yalnız "
            "sequence_order, estimate_slider, perturbation, fix_the_text; toplam 4–6; dersin tamamından, sayılar ders "
            "paketiyle birebir) yaz. Çıktı: deck_ust.json = {\"deste\": {...üst alanlar...}, \"oyun\": {...oyun slaytı...}}. "
            "Başka dosyaya dokunma; bitince tek satır: BİTTİ."), ["deck_ust.json"]))
    if not (d / "ders_notu.md").exists():
        isler.append(("ders notu", on + "Görevin: TALIMAT §2'ye göre YALNIZ ders_notu.md'yi yaz (## bölümleri sayfa_haritasi ana "
                      "başlıklarıyla aynı sıra ve adla). Başka dosyaya dokunma; bitince tek satır: BİTTİ.", ["ders_notu.md"]))
    if not (d / "ornek_sorular.json").exists():
        isler.append(("sorular", on + "Görevin: TALIMAT §4 ve §6'ya göre YALNIZ ornek_sorular.json ve cikmis_baglantilari.json'u "
                      "yaz. Başka dosyaya dokunma; bitince tek satır: BİTTİ.", ["ornek_sorular.json", "cikmis_baglantilari.json"]))
    if not (d / "sozluk.json").exists():
        isler.append(("sözlük", on + "Görevin: TALIMAT §5, §7, §8'e göre YALNIZ sozluk.json, hastaliklar.json ve bilgi_havuzu.jsonl'u "
                      "yaz. Başka dosyaya dokunma; bitince tek satır: BİTTİ.", ["sozluk.json", "hastaliklar.json", "bilgi_havuzu.jsonl"]))
    return isler


def birlestir_deste(d: Path) -> int:
    """deck_ust.json + deck_parca/*.json → deck.json. → slayt sayısı (0 = eksik parça)."""
    ust = oku(d / "deck_ust.json", {}) or {}
    basl = ana_basliklar(d)
    parcalar = []
    for b in basl:
        p = oku(d / "deck_parca" / f"{b['no']}.json", None)
        if not p or not isinstance(p.get("slides"), list):
            log(f"paralel: deste parçası eksik/bozuk: {b['no']}"); return 0
        parcalar.append(p["slides"])
    if not ust.get("deste") or not ust.get("oyun"):
        log("paralel: deck_ust.json eksik"); return 0
    slaytlar = [s for p in parcalar for s in p] + [ust["oyun"]]
    cp = 0
    for i, s in enumerate(slaytlar, 1):
        s["slideNumber"] = i
        if s.get("isCheckpoint") or str(s.get("title", "")).startswith("[TEKRAR SAYFASI"):
            cp += 1
            s["isCheckpoint"] = True
            s["checkpointNumber"] = cp
            s["title"] = str(s.get("title", "")).replace("[TEKRAR SAYFASI - CHECKPOINT]", f"[TEKRAR SAYFASI - CHECKPOINT {cp}]")
    deste = {**ust["deste"], "slides": slaytlar, "totalSlides": len(slaytlar)}
    eo = sum(len(s.get("interactiveElements") or []) for s in slaytlar)
    deste["totalInteractiveElements"] = eo
    deste["interactiveRatio"] = round(eo / max(1, len(slaytlar)), 2)
    yaz(d / "deck.json", deste)
    return len(slaytlar)


def uret(d: Path, claude, konusma_metni, ek: str = "") -> dict:
    """→ {"hata": str, "kota": bool, "sure": sn, "sesli": konusma_metni sonucu | None}. claude = isle.claude."""
    t0 = time.time()
    EK["metin"] = (ek.strip() + " ") if ek.strip() else ""
    if not ((d / "ders_paketi.json").exists() and (d / "sayfa_haritasi.json").exists() and ana_basliklar(d)):
        log("paralel 1/3: iskelet (ders_paketi + sayfa_haritasi)")
        r = claude(d, _on(d) + "Görevin YALNIZ TALIMAT §1 ders_paketi.json ve §1b sayfa_haritasi.json'u yazmak (deste adım planı "
                      "dahil: her ana başlığın adimlar aralığı, toplam 60–100 içerik adımı). Başka dosya YAZMA; bitince tek satır: BİTTİ.",
                   oturum_dosya="oturum_iskelet.json")
        if r["kota"]:
            return {"hata": "", "kota": True}
        if not ana_basliklar(d):
            return {"hata": "iskelet yazılmadı: " + (r.get("hata") or "sayfa_haritasi ana başlık/adimlar yok")[:300], "kota": False}
    isler = _isler(d)
    n = int(ayar().get("paralel", 4) or 4)
    log(f"paralel 2/3: {len(isler)} parça + sesli metin, {n} eşzamanlı ({', '.join(a for a, _, _ in isler)})")
    sonuc: dict = {"kota": False, "hata": "", "sesli": None}

    def calis(i):
        ad, istem, beklenen = i
        t = time.time()
        r = claude(d, istem, oturum_dosya=f"oturum_{ad.replace(' ', '_').replace('+', '')}.json")
        eksik = [b for b in beklenen if not (d / b).exists()]
        log(f"paralel: {ad} {round((time.time() - t) / 60, 1)} dk" + (f" · EKSİK {eksik}" if eksik else "") +
            (" · KOTA" if r["kota"] else ""))
        return ad, r, eksik

    with ThreadPoolExecutor(max_workers=n) as ex:
        ses = ex.submit(konusma_metni, d) if konusma_metni else None
        for ad, r, eksik in ex.map(calis, isler):
            sonuc["kota"] |= r["kota"]
            if eksik and not r["kota"]:
                sonuc["hata"] += f"{ad}: {eksik} yazılmadı; "
        if ses:
            sonuc["sesli"] = ses.result()
    if sonuc["kota"]:
        return sonuc
    log("paralel 3/3: deste birleştirme")
    if not birlestir_deste(d):
        sonuc["hata"] += "deste birleştirilemedi; "
    if not (d / "rapor.md").exists():
        (d / "rapor.md").write_text(
            "# Ders işçisi raporu (paralel üretim)\n\n" + "\n".join(f"- {a}: üretildi" for a, _, _ in isler)
            + f"\n- Süre: {round((time.time() - t0) / 60, 1)} dk\n", encoding="utf-8")
    sonuc["sure"] = round(time.time() - t0)
    log(f"paralel üretim bitti: {round(sonuc['sure'] / 60, 1)} dk" + (f" · {sonuc['hata']}" if sonuc["hata"] else ""))
    return sonuc
