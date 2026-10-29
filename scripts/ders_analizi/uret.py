#!/usr/bin/env python3
"""Ders analizi + ders özeti üretimi (LLM yok; yalnız dersin doğrulanmış verisinden derlenir).

  python3 scripts/ders_analizi/uret.py k2-01 [k2-02 …]      # yoksa: değerlendirme paketi olan tüm Kurul 2+ dersleri
  python3 scripts/ders_analizi/uret.py --dogrula k2-01       # yalnız doğrulama (0 HATA beklenir)

Ders analizi (sesli dersten ÖNCE okunur/dinlenir): derste ne anlatılacak, dersin sonunda bilinmesi gerekenler, en önemli
yerler, çıkmış sorularda ne soruldu, hocanın soru üslubu ve nelere odaklanılmalı.
Ders özeti: dersin içerikleri (önem listesi + sesli çözücü) tamamlandıktan SONRA, onlardan derlenir; en önemli yerleri anlatır.
İçerikler eksikse `ozet: null` + `ozetEksik` yazılır, ekran "hazırlanıyor" gösterir.

Girdiler (tek doğruluk kaynakları):
  meds_database_v2/ders_bilgi/<key>/degerlendirme/paket.json   bilgi paketleri, atomik envanter, hoca vurguları
  data/sesli_anlatim/metin/<key>-*.md                         sesli ders bölüm başlıkları (@@)
  data/sesli_anlatim/cikmis_konum/<key>-*.json                doğrulanmış çıkmış eşlemeleri (yalnız dogrulandi)
  src/data/k<N><slug>_onem/<kod>.json                          önem listesi (özet, neden önemli, maddeler)
  src/data/hoca_profilleri/                                    hoca üslubu profili (scripts/hoca_profili/profil_oku.py)
  src/data/k<N><slug>_cozucu/<kod>.json                        sesli örnek soru çözücü (özet koşulu)
Çıktı: src/data/ders_analizi/<key>.json (ön yüz paketinde). Ses: scripts/ders_analizi/ses.py (EMA, GPU başlatıcısıyla).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
KOK = MEDS.parent
sys.path.insert(0, str(MEDS / "scripts/hoca_profili"))
sys.path.insert(0, str(MEDS / "scripts"))
CIKTI = MEDS / "src/data/ders_analizi"
SURUM = 1

BILGI_TURU = {
    "tanim_kavram": "tanım ve kavram", "tani_ayirici": "tanı ve ayırıcı tanı", "siniflama_ad": "sınıflama ve adlandırma",
    "mekanizma": "mekanizma", "onleme_halk_sagligi": "korunma ve halk sağlığı", "ilac_endikasyon": "ilaç ve endikasyon",
    "epidemiyoloji_sayi": "sıklık ve sayısal bilgi", "etiyoloji_risk": "neden ve risk etkeni", "tedavi": "tedavi",
    "morfoloji": "morfoloji", "klinik_bulgu": "klinik bulgu", "tetkik": "tetkik",
}
KALIP = {
    "dogrudan": "doğrudan bilgi sorusu", "vaka": "vaka sorusu", "olumsuz": "olumsuz kök (hangisi değildir)",
    "sayi": "sayı soran kök", "onculu": "öncüllü soru", "yanlis_bul": "yanlış ifadeyi bulma",
    "en_tipik": "en tipik bulguyu sorma", "dogru_ifade": "doğru ifadeyi bulma",
}
CELDIRICI = {
    "ayni_turden_ayri_kavram": "aynı türden başka bir kavram", "ayni_ailede_komsu_kavram": "aynı ailedeki komşu kavram",
    "sayisal_yakin_deger": "birbirine yakın sayısal değer", "bilesik_yer_degistirmeli": "yer değiştirilmiş eşleştirme",
    "mutlak_ifade_tuzagi": "her zaman, asla gibi mutlak ifade",
}
DUZEY = {"L1_hatirlama": "hatırlama", "L2_anlama_iliski": "anlama ve ilişki kurma", "L3_uygulama": "uygulama"}


def sade(s: str) -> str:
    """Markdown işaretlerini ve fazla boşluğu atar (ekran + ses ortak düz metin)."""
    s = re.sub(r"\*\*|__|`", "", s or "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def nokta(s: str) -> str:
    s = s.strip()
    return s if not s or s[-1] in ".!?…" else s + "."


def yuzde(x: float) -> str:
    return f"%{round(x * 100)}"


def ilk(d: dict, n: int = 2) -> list[tuple[str, float]]:
    return sorted(((k, v) for k, v in (d or {}).items() if v), key=lambda kv: -kv[1])[:n]


def dosya(klasor: Path, key: str, uzanti: str) -> Path | None:
    adaylar = sorted(klasor.glob(f"{key}-*{uzanti}"))
    adaylar = [a for a in adaylar if "-v" not in a.stem[len(key):]] or adaylar  # v2 metni varsa ilk tam metin yeterli
    return adaylar[0] if adaylar else None


def kayit_bul(key: str) -> tuple[dict, dict]:
    kurul = int(key[1])
    dersler = json.loads((MEDS / f"src/data/dersler/k{kurul}.json").read_text(encoding="utf-8"))["dersler"]
    d = next((x for x in dersler if x["id"] == key), None)
    if not d:
        raise SystemExit(f"{key}: ders kayıt defterinde yok")
    branslar = json.loads((MEDS / "src/data/dersler/branslar.json").read_text(encoding="utf-8"))["branslar"]
    harf = re.match(r"\d([a-z])", d["kod"]).group(1)
    b = next(x for x in branslar if x["harf"] == harf)
    return d, b


def bolum_basliklari(key: str) -> list[str]:
    md = dosya(MEDS / "data/sesli_anlatim/metin", key, ".md")
    if not md:
        return []
    return [sade(m) for m in re.findall(r"^@@\s*(.+)$", md.read_text(encoding="utf-8"), re.M)]


def cikmislar(key: str) -> list[dict]:
    f = dosya(MEDS / "data/sesli_anlatim/cikmis_konum", key, ".json")
    if not f:
        return []
    q = json.loads(f.read_text(encoding="utf-8")).get("q", [])
    return [x for x in q if x.get("dogrulandi")]


def profil(ders_ad: str, kisa: str, konu: str) -> tuple[dict, dict | None, str]:
    from profil_oku import konu_bul, profil_yukle

    for ad in (ders_ad, kisa):
        u, harita = profil_yukle(ad)
        if not u.get("not"):
            return u, konu_bul(harita, konu), ad
    return u, None, ders_ad


def ses_metni(b: dict) -> list[str]:
    """Bölümün EMA'ya okunacak cümleleri: başlık + giriş + maddeler (yalnız ekranda görünen bilgi)."""
    c = [nokta(b["baslik"])]
    if b.get("giris"):
        c.append(nokta(b["giris"]))
    for m in b["maddeler"]:
        c.append(nokta(f"{m['baslik']}: {m['metin']}" if m.get("baslik") else m["metin"]))
        if m.get("cevap"):
            c.append(nokta(f"Cevap: {m['cevap']}"))
    return c


def analiz_kur(key, d, b, paket, onem, basliklar, cik, prf) -> list[dict]:
    u, kh, prf_ad = prf
    bolumler = []

    # 1) Derste ne anlatılacak
    m = [{"metin": x} for x in basliklar] or [{"metin": sade(p["baslik"])} for p in paket.get("bilgi_paketleri", [])]
    bolumler.append({"id": "anlatim", "baslik": "Bu derste ne anlatılacak",
                     "giris": sade(onem.get("ozet", "")) if onem else "", "maddeler": m})

    # 2) Kazanımlar: bilgi paketleri (slayt sırasıyla) — dersin sonunda bilinmesi gerekenler
    paketler = sorted(paket.get("bilgi_paketleri", []), key=lambda p: (min(p.get("s") or [0]), p["id"]))
    bolumler.append({"id": "kazanim", "baslik": "Dersin sonunda bilmen gerekenler",
                     "giris": "Bu ders bittiğinde aşağıdaki başlıkları açıklayabilmelisin.",
                     "maddeler": [{"baslik": sade(p["baslik"]), "metin": sade(p["maddeler"][0]) if p.get("maddeler") else "",
                                   "s": p.get("s", [])} for p in paketler]})

    # 3) En önemli yerler: önem listesinin en yüksek puanlı maddeleri (çıkmış ya da profil kanıtlı)
    if onem:
        en = sorted(onem.get("maddeler", []), key=lambda x: -x.get("puan", 0))[:8]
        bolumler.append({"id": "onemli", "baslik": "En önemli yerler", "giris": sade(onem.get("neden_onemli", "")),
                         "maddeler": [{"baslik": sade(x["baslik"]), "metin": sade(x["bilgi"]), "neden": sade(x.get("neden", "")),
                                       "s": sorted({a["sayfa"] for a in x.get("alinti", []) if a.get("sayfa")}),
                                       "cikmis": bool(x.get("cikmis"))} for x in en]})

    # 4) Çıkmış sorularda ne soruldu (yalnız doğrulanmış eşleme)
    if cik:
        bolumler.append({"id": "cikmis", "baslik": "Çıkmış sorularda ne soruldu",
                         "giris": f"Bu dersin konusundan doğrulanmış {len(cik)} çıkmış soru var.",
                         "maddeler": [{"baslik": ({"Hatırlanan": "Öğrenci hatırlaması"}.get(sade(str(x.get('yil', ''))), sade(str(x.get('yil', '')))) or None), "metin": sade(x["kok"]),
                                       "cevap": sade(x.get("cevap", "")), "s": [x["s"]] if x.get("s") else []} for x in cik]})
        for m in bolumler[-1]["maddeler"]:
            if m["baslik"] is None:
                m.pop("baslik")
    else:
        bolumler.append({"id": "cikmis", "baslik": "Çıkmış sorularda ne soruldu",
                         "giris": "Bu dersin konusuyla doğrulanmış bir çıkmış soru eşlemesi henüz yok.", "maddeler": []})

    # 5) Hoca üslubu: ders profili + varsa konu kazanım haritası
    us = []
    kal = ilk(u.get("kok_kalibi", {}), 2)
    if kal:
        us.append({"baslik": "Soru kökü", "metin": "Sorular çoğunlukla " + " ve ".join(f"{KALIP.get(k, k)} ({yuzde(v)})" for k, v in kal) + " biçimindedir."})
    tur = (kh or {}).get("neden_sorulur") or [{"bilgi_turu": k, "pay": v} for k, v in ilk(u.get("bilgi_turu", {}), 2)]
    if tur:
        us.append({"baslik": "Sorulan bilgi", "metin": "En çok " + " ve ".join(f"{BILGI_TURU.get(t['bilgi_turu'], t['bilgi_turu'])} ({yuzde(t['pay'])})" for t in tur[:2]) + " sorulur."})
        for t in tur[:2]:
            if t.get("gerekce"):
                us.append({"baslik": BILGI_TURU.get(t["bilgi_turu"], t["bilgi_turu"]).capitalize(), "metin": sade(t["gerekce"])})
    dz = ilk(((kh or {}).get("nasil_sorulur") or {}).get("bilissel_duzey") or u.get("bilissel_duzey", {}), 2)
    if dz:
        us.append({"baslik": "Düzey", "metin": "Soruların düzeyi " + " ve ".join(f"{DUZEY.get(k, k)} ({yuzde(v)})" for k, v in dz) + " ağırlıklıdır."})
    cel = ilk(((kh or {}).get("hangi_bilgilerle") or {}).get("celdirici") or u.get("celdirici_stratejisi", {}), 2)
    if cel:
        us.append({"baslik": "Çeldiriciler", "metin": "Yanlış şıklar genellikle " + " ya da ".join(CELDIRICI.get(k, k) for k, _ in cel) + " olarak kurulur."})
    if kh and kh.get("zorluk"):
        us.append({"baslik": "Zorluk", "metin": nokta(f"Bu konunun sorularının zorluğu {sade(kh['zorluk'])}")})
    guven = (kh or u).get("guven", u.get("guven", "dusuk"))
    giris = {"yuksek": "Hocanın çok sayıda çıkmış sorusuna dayanan, güvenilir bir profil.",
             "orta": "Hocanın çıkmış sorularına dayanan profil; yol göstericidir, kesin değildir.",
             "dusuk": "Bu konuda çıkmış soru az; profil yalnız genel bir eğilim gösterir."}.get(guven, "")
    bolumler.append({"id": "uslup", "baslik": "Hoca nasıl soru sorar", "giris": giris, "guven": guven, "maddeler": us})

    # 6) Nelere odaklanmalısın: tekrar eden çekirdek kavramlar + çıkmışla eşleşen önem maddeleri
    od = []
    for c in ((kh or {}).get("cekirdek_kavramlar") or [])[:4]:
        od.append({"baslik": sade(c["kavram"]), "metin": nokta(f"Çıkmışlarda {c.get('kez', 1)} kez soruldu. Örnek kök: {sade(c.get('ornek_kok', ''))}")})
    if onem:
        for x in [x for x in sorted(onem.get("maddeler", []), key=lambda x: -x.get("puan", 0)) if x.get("cikmis")][:4]:
            if not any(o["baslik"] == sade(x["baslik"]) for o in od):
                od.append({"baslik": sade(x["baslik"]), "metin": nokta(sade(x.get("neden", "")) or "Çıkmış soruyla eşleşen yer.")})
    if tur:
        od.append({"baslik": "Çalışma yolu",
                   "metin": f"Okurken her başlıkta {BILGI_TURU.get(tur[0]['bilgi_turu'], tur[0]['bilgi_turu'])} bilgisini ayrı not et; hoca en çok bunu soruyor."})
    bolumler.append({"id": "odak", "baslik": "Nelere odaklanmalısın", "giris": "", "maddeler": od})
    return bolumler


def ozet_kur(onem, cozucu_var) -> tuple[list[dict] | None, list[str]]:
    eksik = []
    if not onem:
        eksik.append("önem listesi")
    if not cozucu_var:
        eksik.append("sesli örnek soru çözücü")
    if eksik:
        return None, eksik
    madde = sorted(onem["maddeler"], key=lambda x: (min([a["sayfa"] for a in x.get("alinti", []) if a.get("sayfa")] or [999]), x["id"]))
    bolumler = [{"id": "giris", "baslik": "Dersin özü", "giris": sade(onem.get("ozet", "")), "maddeler": []}]
    # en önemli yerler: en yüksek puanlı 10 madde, slayt sırasıyla; her biri kendi detay maddeleriyle
    secili = {x["id"] for x in sorted(madde, key=lambda x: -x.get("puan", 0))[:10]}
    for x in [x for x in madde if x["id"] in secili]:
        alt = [sade(re.sub(r"^-\s*", "", s)) for s in (x.get("detay") or "").splitlines() if s.strip().startswith("-")]
        alt = [re.sub(r"^([^:]{1,40}):\s*", "", s) for s in alt if not s.lower().startswith("çıkmış soruda")]
        bolumler.append({"id": x["id"], "baslik": sade(x["baslik"]), "giris": sade(x["bilgi"]),
                         "s": sorted({a["sayfa"] for a in x.get("alinti", []) if a.get("sayfa")}),
                         "cikmis": bool(x.get("cikmis")), "maddeler": [{"metin": s} for s in alt if s]})
    return bolumler, []


def klipli(bolumler: list[dict], onek: str) -> list[dict]:
    for b in bolumler:
        b["klip"] = f"{onek}-{b['id']}"
        b["ses"] = ses_metni(b)
        b["v"] = hashlib.sha1("\n".join(b["ses"]).encode()).hexdigest()[:10]
    return bolumler


def uret(key: str) -> Path:
    d, b = kayit_bul(key)
    pp = KOK / f"meds_database_v2/ders_bilgi/{key}/degerlendirme/paket.json"
    if not pp.exists():
        raise SystemExit(f"{key}: değerlendirme paketi yok ({pp})")
    paket = json.loads(pp.read_text(encoding="utf-8"))
    klas = f"k{d['kurul']}{b['slug']}"
    op = MEDS / f"src/data/{klas}_onem/{d['kod']}.json"
    onem = json.loads(op.read_text(encoding="utf-8")) if op.exists() else None
    cozucu_var = (MEDS / f"src/data/{klas}_cozucu/{d['kod']}.json").exists()
    prf = profil(b["ad"], b.get("kisa", b["ad"]), d["konu"])

    analiz = klipli(analiz_kur(key, d, b, paket, onem, bolum_basliklari(key), cikmislar(key), prf), "a")
    ozet, eksik = ozet_kur(onem, cozucu_var)
    o = {"surum": SURUM, "key": key, "kod": d["kod"], "kurul": d["kurul"], "brans": b["kisa"], "konu": d["konu"],
         "ogretim_uyesi": paket.get("ogretim_uyesi") or d.get("ogretim_uyesi"), "profil": prf[2],
         "sesKlasor": {"brans": f"k{d['kurul']}dersanaliz", "kod": d["kod"]},
         "analiz": analiz, "ozet": klipli(ozet, "o") if ozet else None}
    if eksik:
        o["ozetEksik"] = eksik
    CIKTI.mkdir(parents=True, exist_ok=True)
    f = CIKTI / f"{key}.json"
    f.write_text(json.dumps(o, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return f


def dogrula(key: str) -> list[str]:
    from turkce_uslup import denetle

    hata = []
    f = CIKTI / f"{key}.json"
    if not f.exists():
        return [f"{key}: çıktı yok"]
    o = json.loads(f.read_text(encoding="utf-8"))
    gerekli = {"anlatim", "kazanim", "cikmis", "uslup", "odak"}
    var = {b["id"] for b in o["analiz"]}
    if gerekli - var:
        hata.append(f"eksik analiz bölümü: {sorted(gerekli - var)}")
    for ad in ("analiz", "ozet"):
        for b in o.get(ad) or []:
            if not b.get("ses") or not all(c.strip() for c in b["ses"]):
                hata.append(f"{ad}/{b['id']}: boş ses metni")
            if b["id"] not in ("cikmis",) and ad == "analiz" and not b["maddeler"] and b["id"] != "odak":
                hata.append(f"{ad}/{b['id']}: madde yok")
            for c in b["ses"]:
                if re.search(r"\*\*|[#`]|\[\!", c):
                    hata.append(f"{ad}/{b['id']}: biçim işareti sesli metinde: {c[:60]}")
                for h in denetle(c, f"{ad}/{b['id']}") or []:
                    hata.append(str(h))
    if o.get("ozet") is None and not o.get("ozetEksik"):
        hata.append("özet yok ama eksik gerekçesi de yok")
    return hata


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("keyler", nargs="*")
    ap.add_argument("--dogrula", action="store_true")
    a = ap.parse_args()
    keyler = a.keyler or sorted(p.parent.parent.name for p in (KOK / "meds_database_v2/ders_bilgi").glob("k[2-6]-*/degerlendirme/paket.json"))
    toplam = 0
    for k in keyler:
        if not a.dogrula:
            f = uret(k)
            o = json.loads(f.read_text(encoding="utf-8"))
            print(f"{k}: {len(o['analiz'])} analiz bölümü, özet {'var (' + str(len(o['ozet'])) + ' bölüm)' if o['ozet'] else 'yok: ' + ', '.join(o['ozetEksik'])}")
        h = dogrula(k)
        toplam += len(h)
        for x in h:
            print(f"  HATA {k}: {x}")
    print(f"{toplam} HATA")
    sys.exit(1 if toplam else 0)


if __name__ == "__main__":
    main()
