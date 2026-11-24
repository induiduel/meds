#!/usr/bin/env python3
"""Ders analizi + ders özeti üretimi (LLM yok; yalnız dersin doğrulanmış verisinden derlenir).

  python3 scripts/uretim/ders_analizi/uret.py k2-01 [k2-02 …]      # yoksa: değerlendirme paketi olan tüm Kurul 2+ dersleri
  python3 scripts/uretim/ders_analizi/uret.py --dogrula k2-01       # yalnız doğrulama (0 HATA beklenir)

Ders analizi (sesli dersten ÖNCE okunur/dinlenir): derste ne anlatılacak, dersin sonunda bilinmesi gerekenler, en önemli
yerler, çıkmış sorularda ne soruldu, hocanın soru üslubu ve nelere odaklanılmalı.
Ders özeti: dersin içerikleri (önem listesi + sesli çözücü) tamamlandıktan SONRA, onlardan derlenir; en önemli yerleri anlatır.
İçerikler eksikse `ozet: null` + `ozetEksik` yazılır, ekran "hazırlanıyor" gösterir.

Girdiler (tek doğruluk kaynakları):
  meds_database_v2/ders_bilgi/<key>/degerlendirme/paket.json   bilgi paketleri, atomik envanter, hoca vurguları
  data/sesli_anlatim/metin/<key>-*.md                         sesli ders bölüm başlıkları (@@)
  data/sesli_anlatim/cikmis_konum/<key>-*.json                doğrulanmış çıkmış eşlemeleri (yalnız dogrulandi)
  src/data/k<N><slug>_onem/<kod>.json                          önem listesi (özet, neden önemli, maddeler)
  src/data/hoca_profilleri/                                    hoca üslubu profili (scripts/uretim/hoca_profili/profil_oku.py)
  src/data/k<N><slug>_cozucu/<kod>.json                        sesli örnek soru çözücü (özet koşulu)
Çıktı: src/data/ders_analizi/<key>.json (ön yüz paketinde). Ses: scripts/uretim/ders_analizi/ses.py (EMA, GPU başlatıcısıyla).
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
import hashlib
import json
import re
import sys
from pathlib import Path

MEDS = _kok.MEDS
KOK = MEDS.parent
sys.path.insert(0, str(MEDS / "scripts/uretim/hoca_profili"))
sys.path.insert(0, str(MEDS / "scripts"))
CIKTI = MEDS / "src/data/ders_analizi"
SURUM = 2  # 2: kazanım metni tam cümle/başlık, üslup sayımı kök kalıbı düzeltmesi, kesik-cümle kapısı (2026-11-18)

BILGI_TURU = {
    "tanim_kavram": "tanım ve kavram", "tani_ayirici": "tanı ve ayırıcı tanı", "siniflama_ad": "sınıflama ve adlandırma",
    "mekanizma": "mekanizma", "onleme_halk_sagligi": "korunma ve halk sağlığı", "ilac_endikasyon": "ilaç ve endikasyon",
    "epidemiyoloji_sayi": "sıklık ve sayısal bilgi", "etiyoloji_risk": "neden ve risk etkeni", "tedavi": "tedavi",
    "morfoloji": "morfoloji", "klinik_bulgu": "klinik bulgu", "tetkik": "tetkik",
    "prognoz_komplikasyon": "seyir ve komplikasyon",
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
    s = re.sub(r"\bimza bulgusu", "ayırt edici bulgu", s)  # H-uslup: 'imza' doğal Türkçe değil (profil gerekçesi)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def gorsel_at(s: str) -> str:
    """Başlıktaki iç etiketi ' (görsel)' atar (ekranda ve seste okunmaz)."""
    return re.sub(r"\s*\(görsel\)\s*$", "", s or "").strip()


def atom_metni(paket: dict, madde: str) -> str:
    """Paket maddesi 'Atom: <id>' biçiminde bir iç başvurudur: atomik envanterden insan okunur 'ifade'ye çevrilir.
    (H-analiz-atom, 2026-11-18: iç etiket 'Atom: k2-36-a01' öğrenciye ve EMA'ya olduğu gibi gidiyordu.)"""
    m = re.match(r"Atom:\s*(\S+)\s*$", madde or "")
    if not m:
        return re.sub(r"^Görsel:\s*", "", madde or "")
    env = paket.get("atomik_bilgi_envanteri") or {}
    atomlar = env.get("atomlar", []) if isinstance(env, dict) else []
    a = next((x for x in atomlar if x.get("id") == m.group(1)), None)
    return (a or {}).get("ifade", "")


_DUR = set("ve ile için bir bu daha çok olan olarak gibi veya ya da en".split())


def _govde(w: str) -> str:
    w = w.replace("İ", "i").replace("I", "ı").lower()
    return w[:5]


def _kelime_govde(s: str) -> set[str]:
    return {_govde(w) for w in re.findall(r"[^\W\d_]{4,}", s or "") if w.lower() not in _DUR}


def ilk_cumle(s: str) -> str:
    """Atomun yalnız ilk cümlesi (kelime sınırında kesmez; sonuna yapışmış slayt üst başlığını taşımaz)."""
    s = sade(s)
    c = re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9])", s)
    return c[0] if c else s


def kazanim_madde(paket: dict, p: dict) -> dict:
    """Bir bilgi paketinin kazanım maddesi.

    H-analiz-kazanim (2026-11-18): paket maddesi 'Atom: <id>' değilse ve atom başlığının ilk 50 karakteriyse (kesik), o ham
    metin ses ve ekranda kesik cümle olarak okunuyordu; ayrıca ilk madde başlıkla ilgisiz bir cümle olabiliyordu (k2-39:
    'klinik kullanım alanları' ← sıcaklık cümlesi). Kesik ise ilk maddenin atomunun TAM ilk cümlesi (başlıkla ≥2 özgün gövde örtüşüyorsa), yoksa
    yalnız başlık kullanılır. Eski (tam cümleli) paketler aynen kalır."""
    baslik = sade(gorsel_at(p["baslik"]))
    mad = p.get("maddeler") or []
    env = paket.get("atomik_bilgi_envanteri") or {}
    atomlar = env.get("atomlar", []) if isinstance(env, dict) else []
    if not mad:
        return {"baslik": baslik, "metin": "", "s": p.get("s", [])}
    if str(mad[0]).startswith("Atom:"):
        return {"baslik": baslik, "metin": sade(atom_metni(paket, mad[0])), "s": p.get("s", [])}
    m0 = sade(atom_metni(paket, mad[0]))
    if not any(sade(a.get("baslik", "")) == m0 for a in atomlar):
        return {"baslik": baslik, "metin": m0, "s": p.get("s", [])}  # tam cümleli eski paket biçimi
    # Dersin her yerinde geçen genel gövdeler ('antim', 'ilaçl' …) örtüşme sayılmaz (atomların %25'inden fazlasında geçenler)
    df: dict[str, int] = {}
    for a in atomlar:
        for g in _kelime_govde(a.get("ifade", "")):
            df[g] = df.get(g, 0) + 1
    bs = {g for g in _kelime_govde(baslik) if df.get(g, 0) <= 0.25 * max(1, len(atomlar))}
    en = next(a for a in atomlar if sade(a.get("baslik", "")) == m0)  # paketin ilk maddesi olan atom (tam ifadesiyle)
    cumle = ilk_cumle(en.get("ifade", ""))  # örtüşme yalnız kullanılacak ilk cümlede aranır (atom sonuna yapışan slayt üst başlığı sayılmaz)
    if len(bs & _kelime_govde(cumle)) >= 2:
        return {"baslik": baslik, "metin": nokta(cumle), "s": p.get("s", [])}
    return {"baslik": "", "metin": baslik, "s": p.get("s", [])}  # yalnız başlık (ilgili tam cümle bulunamadı)


# Çıkmış kökü kalıpları (soru_uslup_ornek.kalip ile aynı sözcük listesi; orada sınıflar dışlayıcı, burada her soru için ayrı sayılır)
ONCULLU_KOK = re.compile(r"(?:^|[\s(:])(?:I{1,3}|IV)\.\s|ifadelerden|öncül|hangileri|I-IV", re.I)
OLUMSUZ_KOK = re.compile(r"değildir|yanlıştır|yoktur|beklenmez|olamaz|söylenemez|dışında|bulunmaz|görülmez|engellenemez|kullanılmaz|"
                         r"olmaz|etmez|yapmaz|sağlamaz|yer almaz|hangisi değil", re.I)


_HAM_KOK: dict[str, str] | None = None


def _ham_kok() -> dict[str, str]:
    """data/pastQuestions.json → {çıkmış id: ham soru kökü (stem)}; bir kez yüklenir."""
    global _HAM_KOK
    if _HAM_KOK is None:
        try:
            raw = json.loads((MEDS / "data/pastQuestions.json").read_text(encoding="utf-8"))
            lst = raw if isinstance(raw, list) else raw.get("questions", [])
            _HAM_KOK = {str(q.get("id")): str(q.get("stem") or "") for q in lst if isinstance(q, dict)}
        except Exception:
            _HAM_KOK = {}
    return _HAM_KOK


def uslup_kendi(cik: list[dict]) -> list[dict]:
    """Profil güveni düşükken (az çıkmış soru) yalnız bu dersin doğrulanmış sorularından SAYILAN üslup bilgisi."""
    kok = [sade(x.get("kok", "")) for x in cik]
    n = len(kok)
    olumsuz = sum(bool(OLUMSUZ_KOK.search(k)) for k in kok)
    ham = _ham_kok()
    # öncüllü sayımı: yeniden yazılmış kökten DEĞİL, çıkmış bankasındaki ham kökten (k2-39: yeniden yazım öncülleri düşürüyordu)
    oncullu = sum(bool(ONCULLU_KOK.search(k)) or bool(ONCULLU_KOK.search(ham.get(str(x.get("id")), ""))) for k, x in zip(kok, cik))
    kurgu = sum(k.startswith("Kurgu Soru") for k in kok)
    sayfa = sorted({s for x in cik for s in ([x["s"]] if isinstance(x.get("s"), int) else (x.get("s") or []))})
    us = [{"baslik": "Soru kökü", "metin": f"Bu dersten doğrulanmış {n} çıkmış soru var; {oncullu} tanesi öncüllü, {olumsuz} tanesi olumsuz köklüdür."}]
    if kurgu:
        us.append({"baslik": "Kurgu sorular", "metin": f"{kurgu} soru kaynak belgeden yeniden kurulmuş kurgu sorudur."})
    if sayfa:
        us.append({"baslik": "Sorulan sayfalar", "metin": "Çıkmış sorular şu ders sayfalarına denk gelir: " + ", ".join(str(s) for s in sayfa) + "."})
    return us


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
    # ders anahtarı (key) "k2-62-kraniyal-sinir-muayenesi" biçimindedir; kayıt defterindeki id yalnız "k2-62" (H570).
    dersler = json.loads((MEDS / f"src/data/dersler/k{kurul}.json").read_text(encoding="utf-8"))["dersler"]
    key = "-".join(key.split("-")[:2]) if key[:1] == "k" and key[2] == "-" else key
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


def cikmis_analizi(key: str) -> dict:
    f = KOK / "meds_database_v2/ders_bilgi" / key / "degerlendirme/cikmis_analiz.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


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
        c += [nokta(a) for a in m.get("aciklama", [])]
        if m.get("ornek"):
            c.append(nokta(f"Örnek: {m['ornek']}"))
        if m.get("tuzak"):
            c.append(nokta(f"Tuzak: {m['tuzak']}"))
    return c


def analiz_kur(key, d, b, paket, onem, basliklar, cik, prf) -> list[dict]:
    u, kh, prf_ad = prf
    bolumler = []

    # 1) Derste ne anlatılacak
    m = []
    for x in basliklar or [sade(p["baslik"]) for p in paket.get("bilgi_paketleri", [])]:
        x = gorsel_at(x)
        if x and not (m and m[-1]["metin"] == x):
            m.append({"metin": x})
    bolumler.append({"id": "anlatim", "baslik": "Bu derste ne anlatılacak",
                     "giris": sade(onem.get("ozet", "")) if onem else "", "maddeler": m})

    # 2) Kazanımlar: bilgi paketleri (slayt sırasıyla) — dersin sonunda bilinmesi gerekenler
    paketler = sorted(paket.get("bilgi_paketleri", []), key=lambda p: (min(p.get("s") or [0]), p["id"]))
    # 'Görsel: …' paketleri şema tarifidir (içerik aynı konudaki metin paketinde); kazanım olarak sayılmaz.
    paketler = [p for p in paketler if not (p.get("maddeler") and str(p["maddeler"][0]).startswith("Görsel:"))]
    paketler = [p for p in paketler if sade(p["baslik"]).lower() not in ("kaynak", "kaynaklar", "kaynakça")]  # kaynak künyesi kazanım değildir
    kaz = [kazanim_madde(paket, p) for p in paketler]
    bolumler.append({"id": "kazanim", "baslik": "Dersin sonunda bilmen gerekenler",
                     "giris": "Bu ders bittiğinde aşağıdaki başlıkları açıklayabilmelisin.",
                     "maddeler": [({k: v for k, v in x.items() if not (k == "baslik" and not v)}) for x in kaz if x["metin"]]})

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
        # Ayrıntılı çıkmış analizi (ZORUNLU, 2026-11-06): degerlendirme/cikmis_analiz.json — soru başına
        # aciklama (ne soruldu, kavram, neden bu cevap, çeldiriciler), ornek (pekiştiren klinik/ders örneği), tuzak
        ca = cikmis_analizi(key)
        if ca.get("giris"):
            bolumler[-1]["giris"] = sade(ca["giris"])
        for m, x in zip(bolumler[-1]["maddeler"], cik):
            if m["baslik"] is None:
                m.pop("baslik")
            e = ca.get("sorular", {}).get(str(x.get("id")))
            if e:
                m["aciklama"] = [sade(a) for a in e.get("aciklama", []) if sade(a)]
                for k in ("ornek", "tuzak"):
                    if e.get(k):
                        m[k] = sade(e[k])
    else:
        bolumler.append({"id": "cikmis", "baslik": "Çıkmış sorularda ne soruldu",
                         "giris": "Bu dersin konusuyla doğrulanmış bir çıkmış soru eşlemesi henüz yok.", "maddeler": []})

    # 5) Hoca üslubu: ders profili + varsa konu kazanım haritası
    guven = (kh or u).get("guven", u.get("guven", "dusuk"))
    if guven == "dusuk" and cik:
        # düşük güven: dal profilindeki yüzdeler (kaynağı başka konuların soruları) gösterilmez
        bolumler.append({"id": "uslup", "baslik": "Hoca nasıl soru sorar", "guven": guven,
                         "giris": f"Hocanın soru üslubu profili bu konuda güvenilir değil; aşağıda yalnız bu dersin doğrulanmış {len(cik)} çıkmış sorusundan sayılanlar var.",
                         "maddeler": uslup_kendi(cik)})
        us = None
    else:
        us = []
    kal = ilk(u.get("kok_kalibi", {}), 2) if us is not None else []
    if kal:
        us.append({"baslik": "Soru kökü", "metin": "Sorular çoğunlukla " + " ve ".join(f"{KALIP.get(k, k)} ({yuzde(v)})" for k, v in kal) + " biçimindedir."})
    tur = ((kh or {}).get("neden_sorulur") or [{"bilgi_turu": k, "pay": v} for k, v in ilk(u.get("bilgi_turu", {}), 2)]) if us is not None else []
    if tur:
        us.append({"baslik": "Sorulan bilgi", "metin": "En çok " + " ve ".join(f"{BILGI_TURU.get(t['bilgi_turu'], t['bilgi_turu'])} ({yuzde(t['pay'])})" for t in tur[:2]) + " sorulur."})
        for t in tur[:2]:
            if t.get("gerekce"):
                us.append({"baslik": BILGI_TURU.get(t["bilgi_turu"], t["bilgi_turu"]).capitalize(), "metin": sade(t["gerekce"])})
    dz = ilk(((kh or {}).get("nasil_sorulur") or {}).get("bilissel_duzey") or u.get("bilissel_duzey", {}), 2) if us is not None else []
    if dz:
        us.append({"baslik": "Düzey", "metin": "Soruların düzeyi " + " ve ".join(f"{DUZEY.get(k, k)} ({yuzde(v)})" for k, v in dz) + " ağırlıklıdır."})
    cel = ilk(((kh or {}).get("hangi_bilgilerle") or {}).get("celdirici") or u.get("celdirici_stratejisi", {}), 2) if us is not None else []
    if cel:
        us.append({"baslik": "Çeldiriciler", "metin": "Yanlış şıklar genellikle " + " ya da ".join(CELDIRICI.get(k, k) for k, _ in cel) + " olarak kurulur."})
    if us is not None and kh and kh.get("zorluk"):
        us.append({"baslik": "Zorluk", "metin": nokta(f"Bu konunun sorularının zorluğu {sade(kh['zorluk'])}")})
    giris = {"yuksek": "Hocanın çok sayıda çıkmış sorusuna dayanan, güvenilir bir profil.",
             "orta": "Hocanın çıkmış sorularına dayanan profil; yol göstericidir, kesin değildir.",
             "dusuk": "Bu konuda çıkmış soru az; profil yalnız genel bir eğilim gösterir."}.get(guven, "")
    if us is not None:
        bolumler.append({"id": "uslup", "baslik": "Hoca nasıl soru sorar", "giris": giris, "guven": guven, "maddeler": us})

    # 6) Nelere odaklanmalısın: tekrar eden çekirdek kavramlar + çıkmışla eşleşen önem maddeleri
    od = []
    # Odak, bu dersin DOĞRULANMIŞ çıkmışlarından kurulur. Dal profilindeki çekirdek kavramlar başka konuların sorularından
    # gelebilir (k2-36'da palyatif bakım / üreme sağlığı sorusu görünmüştü): yalnız güven düşük değilse ve çıkmış yoksa kullanılır.
    if cik:
        ca = cikmis_analizi(key).get("sorular", {})
        grup: dict[str, list[str]] = {}
        for x in cik:
            sayf = [x["s"]] if isinstance(x.get("s"), int) else list(x.get("s") or [])
            pk = next((p for p in paket.get("bilgi_paketleri", []) if sayf and sayf[0] in (p.get("s") or []) and not str(p["maddeler"][:1]).startswith("['Görsel:")), None)
            bas = sade(gorsel_at(pk["baslik"])) if pk else (f"Sayfa {sayf[0]}" if sayf else sade(x.get("cevap", ""))[:60])
            e = ca.get(str(x.get("id"))) or {}
            ac = e.get("aciklama") or []
            # önce çıkmışın tuzağı (öğrenciye en yararlı uyarı), yoksa 'ne ölçülüyor' cümlesi
            grup.setdefault(bas, []).append(nokta("Sık yapılan hata: " + sade(e["tuzak"])) if e.get("tuzak") else
                                            nokta(sade(ac[0])) if ac else nokta(f"Çıkmış soru: {sade(x.get('kok', ''))[:140]}"))
        for bas, ml in list(grup.items())[:6]:
            od.append({"baslik": bas, "metin": " ".join(ml[:1] + [s.replace("Sık yapılan hata: ", "Ayrıca: ", 1) for s in ml[1:2]])})
    elif guven != "dusuk":
        for c in ((kh or {}).get("cekirdek_kavramlar") or [])[:4]:
            od.append({"baslik": sade(c["kavram"]), "metin": nokta(f"Çıkmışlarda {c.get('kez', 1)} kez soruldu. Örnek kök: {sade(c.get('ornek_kok', ''))}")})
    if onem:
        for x in [x for x in sorted(onem.get("maddeler", []), key=lambda x: -x.get("puan", 0)) if x.get("cikmis")][:4]:
            if not any(o["baslik"] == sade(x["baslik"]) for o in od):
                od.append({"baslik": sade(x["baslik"]), "metin": nokta(sade(x.get("neden", "")) or "Çıkmış soruyla eşleşen yer.")})
    if cik or tur:
        od.append({"baslik": "Çalışma yolu",
                   "metin": "Okurken yukarıdaki başlıklarda çıkmış soruların sorduğu bilgiyi ayrı not et; tanımı ve sayıları kendi cümlenle tekrar et."
                   if (guven == "dusuk" or not tur) else
                   f"Okurken her başlıkta {BILGI_TURU.get(tur[0]['bilgi_turu'], tur[0]['bilgi_turu'])} bilgisini ayrı not et; profilde en yüksek payı bu tür alıyor."})
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
    # 40'tan çok sorulu çözücü birlestir.py'de ardışık setlere bölünür (<kod>-1, <kod>-2): onlar da çözücü sayılır
    cz = MEDS / f"src/data/{klas}_cozucu"
    cozucu_var = (cz / f"{d['kod']}.json").exists() or (cz / f"{d['kod']}-1.json").exists()
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
    # Ayrıntılı çıkmış analizi kapısı (2026-11-06, H-cikmis-analiz): 2026-11-06 sonrası her derste her çıkmış maddesi
    # ≥3 cümlelik aciklama + ornek taşır (kural: KURUL_OTOMASYON_EL_KITABI §11d, AGENTS 21)
    if (KOK / "meds_database_v2/ders_bilgi" / key / "degerlendirme/cikmis_analiz.json").exists() or o.get("_cikmisAnalizZorunlu"):
        for b in o["analiz"]:
            if b["id"] == "cikmis":
                for i, m in enumerate(b["maddeler"]):
                    if len(m.get("aciklama", [])) < 3 or not m.get("ornek"):
                        hata.append(f"çıkmış {i+1}: ayrıntılı analiz eksik (aciklama ≥3 cümle + ornek)")
    if o.get("surum", 1) >= 2:  # kesik-cümle kapısı (2026-11-18): yalnız yeni sürüm çıktıları; eski çıktılar yeniden üretilince geçer
        for b in o["analiz"]:
            if b["id"] != "kazanim":
                continue
            for i, m in enumerate(b["maddeler"]):
                t = (m.get("metin") or "").strip()
                if m.get("baslik") and t[-1:] not in ".!?…":
                    hata.append(f"kazanim {i+1}: kesik cümle (noktalama yok): {t[:60]}")
                if m.get("baslik") and len(_kelime_govde(m["baslik"]) & _kelime_govde(t)) < 2:
                    hata.append(f"kazanim {i+1}: metin başlıkla örtüşmüyor: {m['baslik'][:40]} ← {t[:50]}")
    for ad in ("analiz", "ozet"):
        for b in o.get(ad) or []:
            if not b.get("ses") or not all(c.strip() for c in b["ses"]):
                hata.append(f"{ad}/{b['id']}: boş ses metni")
            if b["id"] not in ("cikmis",) and ad == "analiz" and not b["maddeler"] and b["id"] != "odak":
                hata.append(f"{ad}/{b['id']}: madde yok")
            for c in b["ses"]:
                if re.search(r"\bAtom: |\bk\d-\d+-a\d+\b|\(görsel\)|^Görsel: |\w_\w+_\w+", c) or re.search(r"\bprognoz_komplikasyon\b|\b\w+_\w+\b", c):
                    hata.append(f"{ad}/{b['id']}: iç etiket/ham anahtar sesli metinde: {c[:60]}")
                if re.search(r"\*\*|[#`]|\[\!", c):
                    hata.append(f"{ad}/{b['id']}: biçim işareti sesli metinde: {c[:60]}")
                for h in denetle(c, f"{ad}/{b['id']}") or []:
                    hata.append(str(h))
    if o.get("ozet") is None and not o.get("ozetEksik"):
        hata.append("özet yok ama eksik gerekçesi de yok")
    if "ozetEksik" in o and not (isinstance(o["ozetEksik"], list) and all(isinstance(x, str) for x in o["ozetEksik"])):
        hata.append("ozetEksik metin listesi olmalı (ekran .join çağırır; düz metin sayfayı çökertir — H: k2-41)")
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
