"""Görev `kanit_bagla` — betiğin kesinleştiremediği kanıt bölgelerini modele seçtirir (ICERIK_MOTORU_V3.md §16.2 adım 4).

Hedef: `<ders>/parti/<n>` — dersin kanıt dosyasındaki (l1/kanit.json) `olasi` ve `bagsiz` soruların belirlenimci sırayla
n. 6'lık partisi; ya da `<ders>/<soru_id>` tek soru. Girdi: her soru (kök, şıklar, doğru cevap) + o sorunun aday birimleri
(S etiketi, sayfa no; en iyi 3 sayfa + planın sayfaları + betiğin önerdiği sayfa; soru başına ≤ 14 birim).
Model yalnız etiket seçer: `{"sorular": {"Q1": {"dogru": ["S3"], "celdirici": {"B": "S7"}, "yok": false}}}`.
Kapı (betik): etiket o sorunun adayı; olumsuz olmayan soruda seçilen birimde doğru cevabın en az bir içerik kökü/sayısı;
olumsuz kökte ("…değildir") seçilen birimlerde en az 2 çeldiricinin kökü; çeldirici bağı o şıkkın kökünü içermeli.
Uygulama: l1/kanit.json'da sorunun doğru bölgesi `kesin` (yontem `kanit_bagla`), `tekrar` yalnız olumsuz olmayan + cevabın
TÜM kökleri birimde; `yok` = model "derste yok" dedi → `bagsiz` kalır, `model_bagsiz` işaretlenir. Dosya kilitli yazılır.
"""
from __future__ import annotations

import fcntl
import json
import re
import sys
from pathlib import Path

from .. import cekirdek as c

sys.path.insert(0, str(c.KOK / "scripts" / "kroki"))
sys.path.insert(0, str(c.KOK / "scripts" / "cikmis_dizin"))

OGRENCI_METNI = False   # çıktı iç veri (kısa etiket taşır); ortak etiket sızıntısı kapısı uygulanmaz
OGE, OGE_ETIKET = ("sorular", "dict"), r"Q\d+"   # kısmi düzeltme: yalnız hatalı Q'lar (yonlendir.kismi_duzeltme)
KURALLAR = ["kaynak_sadakati", "cikti_disiplini"]
PARTI = 6
BIRIM_SINIR = 14


def _moduller():
    import dizin as D  # noqa: F401
    import kanit as K
    import plan as P
    from ortak import DEPO, kokler, oku, sayilar, vektorle
    return D, K, P, DEPO, kokler, oku, sayilar, vektorle


DENEME_TAVAN = 2


def denemeyi_say(ders: str, soru_idleri: list[str]) -> None:
    """Kapıdan geçemeyen soruların deneme sayısı (l1/kanit_model.json → denemeler); tavanı aşan soru `model_cozemedi`."""
    _, _, _, DEPO, _, oku, _, _ = _moduller()
    d = DEPO / ders / "l1"
    with open(d / "kanit.kilit", "w") as kilit:
        fcntl.flock(kilit, fcntl.LOCK_EX)
        km = oku(d / "kanit_model.json") or {}
        kn = oku(d / "kanit.json") or {}
        if km.get("pdf_sha") != kn.get("pdf_sha"):
            km = {"pdf_sha": kn.get("pdf_sha"), "kararlar": {}}
        den = km.setdefault("denemeler", {})
        for sid in soru_idleri:
            den[sid] = den.get(sid, 0) + 1
        km["model_cozemedi"] = sorted(k for k, v in den.items() if v >= DENEME_TAVAN and k not in km.get("kararlar", {}))
        c.yaz(d / "kanit_model.json", km)


def bekleyenler(ders: str) -> list[str]:
    """Betiğin kesinleştiremediği sorular (olası + bağsız), belirlenimci sırada; deneme tavanını aşanlar hariç."""
    _, _, _, DEPO, _, oku, _, _ = _moduller()
    kn = oku(DEPO / ders / "l1" / "kanit.json") or {}
    cozemedi = set((oku(DEPO / ders / "l1" / "kanit_model.json") or {}).get("model_cozemedi", []))
    olasi = [r["soru"] for r in kn.get("sorular", []) if r["bolgeler"][0]["guven"] == "olasi"
             and not r["bolgeler"][0].get("yontem", "").startswith("kanit_bagla")]
    return [x for x in sorted(olasi) + sorted(x for x in kn.get("bagsiz", []) if x not in set(kn.get("model_bagsiz", [])))
            if x not in cozemedi]


def _soru_kaynagi(ders: str) -> dict[str, dict]:
    D, K, _, _, _, _, _, _ = _moduller()
    d, _ = D.yukle()
    out = {q["id"]: {**q, "kaynak": "cikmis"} for q in d["sorular"]}
    for q in K.ornek_sorulari(ders):
        out[q["id"]] = q
    return out


def _hedef_sorulari(hedef: str) -> tuple[str, list[str]]:
    m = re.fullmatch(r"(k\d-\d{2})/parti/(\d+)", hedef)
    if m:
        ders, n = m.group(1), int(m.group(2))
        b = bekleyenler(ders)
        parca = b[n * PARTI:(n + 1) * PARTI]
        if not parca:
            raise SystemExit(f"{hedef}: bu partide soru yok ({len(b)} bekleyen, {PARTI}'lık parti)")
        return ders, parca
    m = re.fullmatch(r"(k\d-\d{2})/(.+)", hedef)
    if not m:
        raise SystemExit(f"kanit_bagla hedefi '<ders>/parti/<n>' ya da '<ders>/<soru_id>': {hedef}")
    return m.group(1), [m.group(2)]


def hazirla(hedef: str, ayar: dict | None = None) -> dict:
    D, K, P, DEPO, kokler, oku, sayilar, vektorle = _moduller()
    import numpy as np
    ders, ids = _hedef_sorulari(hedef)
    l0 = oku(DEPO / ders / "l0" / "sayfalar.json")
    kn = oku(DEPO / ders / "l1" / "kanit.json") or {}
    plan = oku(DEPO / ders / "l1" / "tarama_plani.json") or {}
    if not l0:
        raise SystemExit(f"{ders}: L0 yok")
    B = K.birimler(l0)
    T = K.Tfidf([b["metin"] for b in B])
    sayfa_no, SV = P.sayfa_vektorleri(l0)
    kaynak = _soru_kaynagi(ders)
    plan_sayfa = {b["id"]: b["sayfalar"] for b in plan.get("bagli", [])}
    onceki = {r["soru"]: r["bolgeler"][0]["sayfa"] for r in kn.get("sorular", [])}
    et = c.Etiketler()
    bloklar, meta_sorular = [], {}
    for qi, sid in enumerate(ids, 1):
        q = kaynak.get(sid)
        if not q:
            raise SystemExit(f"{sid}: soru bulunamadı")
        qv = vektorle([f"{q['kok']} {q['dogru_metin']}"])[0]
        ps = qv @ SV.T
        sayfalar = [sayfa_no[k] for k in np.argsort(-ps)[:3]] + list(plan_sayfa.get(sid, [])) + \
            ([onceki[sid]] if sid in onceki else [])
        sayfalar = list(dict.fromkeys(sayfalar))
        aday = [i for i, b in enumerate(B) if b["sayfa"] in sayfalar and not b["baslik"]]
        tq = T.vek(f"{q['kok']} {q['dogru_metin']} " + " ".join(q["secenekler"].values()))
        aday = sorted(aday, key=lambda i: -T.cos(T.birim[i], tq))[:BIRIM_SINIR]
        aday.sort(key=lambda i: (B[i]["sayfa"], B[i]["satirlar"][0]))
        Q = et.ekle("Q", sid)
        satirlar = [f"### {Q}", f"Soru: {q['kok']}"] + [f"{h}) {t}" for h, t in sorted(q["secenekler"].items())] + \
                   [f"Doğru cevap: {q['dogru']}) {q['dogru_metin']}", "Aday ders birimleri:"]
        kisa = []
        for i in aday:
            S = et.ekle("S", f"{ders}|{B[i]['sayfa']}|{','.join(map(str, B[i]['satirlar']))}")
            kisa.append(S)
            satirlar.append(f"{S} (sayfa {B[i]['sayfa']}): {B[i]['metin'][:400]}")
        bloklar.append("\n".join(satirlar))
        meta_sorular[Q] = {"id": sid, "olumsuz": bool(K.OLUMSUZ.search(q["kok"])), "adaylar": kisa,
                           "dogru": q["dogru"], "dogru_metin": q["dogru_metin"], "secenekler": q["secenekler"],
                           "birim": {S: B[i]["metin"] for S, i in zip(kisa, aday)},
                           "bbox": {S: B[i]["bbox"] for S, i in zip(kisa, aday)}}
    ornek = {"sorular": {"Q1": {"dogru": ["S2"], "celdirici": {"B": "S5"}, "yok": False}}}
    return {
        "amac": ("Her soru için, doğru cevabı DOĞRU kılan bilginin ders slaytında geçtiği birimi seç. Olumsuz kökte "
                 "(\"…değildir\", \"…yanlıştır\", \"…sayılmaz\") öteki şıkların sayıldığı birimi seç. Yanlış şıklardan biri "
                 "derste ayrıca anlatılıyorsa onun birimini `celdirici` altında ver. Hiçbir aday birim bilgiyi "
                 "içermiyorsa `yok: true` yaz; tahminle birim seçme."),
        "kurallar": KURALLAR,
        "ek_kurallar": [
            "Yalnız o sorunun kendi aday birimlerinden (S etiketleri) seç; başka sorunun birimini kullanma.",
            "`dogru` en çok 3 etiket; bilgiyi açıkça taşıyan en dar birim(ler).",
            "Konu başlığı ya da yalnız konuya değinen birim kanıt değildir; cevabı destekleyen ifade içinde geçmeli.",
        ],
        "girdi": "\n\n".join(bloklar),
        "cikti_bicimi": "Yalnız şu JSON (girdideki her Q için bir kayıt):\n" + json.dumps(ornek, ensure_ascii=False, indent=1),
        "denetim_listesi": ["her Q için kayıt var", "etiketler o sorunun adayı",
                            "seçilen birimde doğru cevabın bilgisi geçiyor (olumsuzda öteki şıklar)", "emin değilsen yok: true"],
        "esleme": et.esleme,
        "meta": {"ders_id": ders, "kurul": int(ders[1]), "sorular": meta_sorular, "_esleme": dict(et.esleme),
                 "pdf_sha": l0["pdf_sha"]},
    }


def derle(cevap, esleme: dict, meta: dict):
    j = c.json_cikar(cevap)
    if not isinstance(j, dict) or not isinstance(j.get("sorular"), dict):
        return None, ["cevap JSON değil ya da 'sorular' nesnesi yok"]
    out, e = {}, []
    for Q, ms in meta["sorular"].items():
        r = j["sorular"].get(Q)
        if not isinstance(r, dict):
            e.append(f"{Q}: cevapta kayıt yok"); continue
        dogru = r.get("dogru") or []
        if isinstance(dogru, str):
            dogru = re.findall(r"S\d+", dogru)
        cel = r.get("celdirici") or {}
        # çeldirici bağı isteğe bağlı zenginleştirme: geçersiz olanı atılır, soru düşmez (atılan sayısı kayıtta)
        _, _, _, _, kokler, _, _, _ = _moduller()
        temiz, atilan = {}, 0
        for h, sl in cel.items():
            h, sl = str(h).strip().upper()[:1], str(sl).strip()
            t = ms["secenekler"].get(h)
            if sl and t and h != ms["dogru"] and sl in ms["adaylar"] and kokler(t) & kokler(ms["birim"].get(sl, "")):
                temiz[h] = sl
            else:
                atilan += 1
        out[Q] = {"dogru": [str(x).strip() for x in dogru], "celdirici": temiz, "yok": bool(r.get("yok")),
                  **({"atilan_celdirici": atilan} if atilan else {})}
    return {"surum": 1, "ders_id": meta["ders_id"], "sorular": out}, e


def dogrula(cikti: dict, meta: dict) -> list[str]:
    _, K, _, _, kokler, _, sayilar, _ = _moduller()
    e = []
    for Q, r in cikti["sorular"].items():
        ms = meta["sorular"][Q]
        if r["yok"]:
            if r["dogru"]:
                e.append(f"{Q}: hem yok: true hem dogru etiketi var")
            continue
        if not r["dogru"]:
            e.append(f"{Q}: dogru boş (bilgi yoksa yok: true)"); continue
        if len(r["dogru"]) > 3:
            e.append(f"{Q}: en çok 3 dogru etiketi")
        yabanci = [s for s in r["dogru"] + list(r["celdirici"].values()) if s not in ms["adaylar"]]
        if yabanci:
            e.append(f"{Q}: bu sorunun adayı olmayan etiket {yabanci}"); continue
        metin = " ".join(ms["birim"][s] for s in r["dogru"])
        if ms["olumsuz"]:
            cel = [t for h, t in ms["secenekler"].items() if h != ms["dogru"] and t]
            n = sum(1 for t in cel if kokler(t) & kokler(metin))
            if n < 2:
                e.append(f"{Q}: olumsuz soruda seçilen birimde öteki şıklardan en az 2'si geçmeli ({n} geçiyor)")
        else:
            hk, hs = kokler(ms["dogru_metin"]), sayilar(ms["dogru_metin"])
            if not ((hk & kokler(metin)) or (hs and hs <= sayilar(metin))):
                e.append(f"{Q}: seçilen birimde doğru cevabın ({ms['dogru_metin'][:40]!r}) bilgisi geçmiyor")
        for h, s in r["celdirici"].items():
            t = ms["secenekler"].get(h)
            if not t or h == ms["dogru"]:
                e.append(f"{Q}: çeldirici harfi geçersiz {h}")
            elif not (kokler(t) & kokler(ms["birim"].get(s, ""))):
                e.append(f"{Q}: {h} şıkkının birimi o şıkkı içermiyor")
    return e


def tersine(cikti: dict, esleme: dict, meta: dict) -> str:
    return json.dumps({"sorular": cikti["sorular"]}, ensure_ascii=False, indent=1)


ozet = tersine


def uygula(cikti: dict, meta: dict, cikis: Path | None = None, k1_izin: bool = False) -> Path:
    """Kararlar l1/kanit_model.json'a (kalıcı; betik yeniden koşunca yeniden uygulanır), sonra kanit.json güncellenir.
    Yalnız dersin kendi l1 dosyaları değişir (Kurul 1 içerik verisi değildir). cikis verilirse yalnız oraya yazar."""
    _, K, _, DEPO, kokler, oku, sayilar, _ = _moduller()
    if cikis is not None:
        p = cikis / f"{meta['ders_id']}-{sorted(ms['id'] for ms in meta['sorular'].values())[0]}.json"
        c.yaz(p, cikti)
        return p
    kaynak = _soru_kaynagi(meta["ders_id"])
    kararlar = {}
    for Q, r in cikti["sorular"].items():
        ms = meta["sorular"][Q]
        q = kaynak.get(ms["id"], {})
        ek = {"kaynak": q.get("kaynak", ""), "kez": q.get("kez", 0), "yillar": q.get("yillar", [])}
        if r["yok"]:
            kararlar[ms["id"]] = {"yok": True, **ek}; continue
        metin = " ".join(ms["birim"][s] for s in r["dogru"])
        hk = kokler(ms["dogru_metin"])
        tam = (not ms["olumsuz"]) and bool(hk) and hk <= kokler(metin) and sayilar(ms["dogru_metin"]) <= sayilar(metin)
        bolgeler = []
        for j, s in enumerate(r["dogru"]):
            _, sy, st = meta["_esleme"][s].split("|")
            bolgeler.append({"rol": "dogru", "sayfa": int(sy), "satirlar": [int(x) for x in st.split(",")],
                             "bbox": ms["bbox"][s], "guven": "kesin", "yontem": "kanit_bagla", "tekrar": tam and j == 0,
                             "metin": ms["birim"][s][:200]})
        for h, s in r["celdirici"].items():
            _, sy, st = meta["_esleme"][s].split("|")
            bolgeler.append({"rol": "celdirici", "sik": h, "sayfa": int(sy), "satirlar": [int(x) for x in st.split(",")],
                             "bbox": ms["bbox"][s], "yontem": "kanit_bagla", "metin": ms["birim"][s][:200]})
        kararlar[ms["id"]] = {"bolgeler": bolgeler, **ek}
    d = DEPO / meta["ders_id"] / "l1"
    with open(d / "kanit.kilit", "w") as kilit:
        fcntl.flock(kilit, fcntl.LOCK_EX)
        km = oku(d / "kanit_model.json") or {}
        if km.get("pdf_sha") != meta["pdf_sha"]:
            km = {"pdf_sha": meta["pdf_sha"], "kararlar": {}}
        km.setdefault("kararlar", {}).update(kararlar)
        c.yaz(d / "kanit_model.json", km)
        kn = oku(d / "kanit.json")
        bagsiz = list(kn.get("bagsiz", []))
        K.model_kararlari_uygula(meta["ders_id"], kn["sorular"], bagsiz, meta["pdf_sha"])
        for r in kn["sorular"]:
            r.pop("_vek", None); r.pop("_gercek_sayfa", None)
        kn["bagsiz"] = bagsiz
        kn["model_bagsiz"] = sorted(k for k, v in km["kararlar"].items() if v.get("yok"))
        kn["tekrar"] = K.tekrar_listesi(kn["sorular"])
        kn["ozet"]["kanit_bagla"] = sum(1 for r in kn["sorular"] if r["bolgeler"][0].get("yontem") == "kanit_bagla")
        kn["ozet"]["kesin"] = sum(1 for r in kn["sorular"] if r["bolgeler"][0]["guven"] == "kesin")
        kn["ozet"]["olasi"] = sum(1 for r in kn["sorular"] if r["bolgeler"][0]["guven"] == "olasi")
        kn["ozet"]["bagsiz"] = len(kn["bagsiz"])
        kn["ozet"]["model_bagsiz"] = len(kn["model_bagsiz"])
        kn["ozet"]["tekrar_karti"] = len(kn["tekrar"])
        c.yaz(d / "kanit.json", kn)
    return d / "kanit_model.json"


def sinama_ornekleri(meta: dict) -> tuple[dict, list[dict]]:
    """Öz-sınama (model yok): paket veriden kurulduğu için iyi/kötü cevaplar pakete göre üretilir."""
    _, _, _, _, kokler, _, _, _ = _moduller()
    iyi, bilgisiz = {"sorular": {}}, None
    for Q, ms in meta["sorular"].items():
        hk = kokler(ms["dogru_metin"])
        uygun = [S for S in ms["adaylar"] if hk & kokler(ms["birim"][S])]
        if ms["olumsuz"] or not uygun:
            iyi["sorular"][Q] = {"dogru": [], "celdirici": {}, "yok": True}
        else:
            iyi["sorular"][Q] = {"dogru": [uygun[0]], "celdirici": {}, "yok": False}
            bos = [S for S in ms["adaylar"] if not (hk & kokler(ms["birim"][S]))]
            if bos and bilgisiz is None:
                bilgisiz = (Q, bos[0])
    Q1 = next(iter(meta["sorular"]))
    kotu = [{"ad": "aday olmayan etiket", "degistir": [[["sorular", Q1, "dogru"], ["S999"]], [["sorular", Q1, "yok"], False]],
             "beklenen": "adayı olmayan"},
            {"ad": "yok + etiket", "degistir": [[["sorular", Q1, "dogru"], [meta["sorular"][Q1]["adaylar"][0]]],
                                                [["sorular", Q1, "yok"], True]], "beklenen": "hem yok"}]
    if bilgisiz:
        kotu.append({"ad": "bilgisiz birim", "degistir": [[["sorular", bilgisiz[0], "dogru"], [bilgisiz[1]]],
                                                          [["sorular", bilgisiz[0], "yok"], False]], "beklenen": "bilgisi geçmiyor"})
    return iyi, kotu


def kismi_kabul(cikti: dict | None, hatalar: list[str], meta: dict) -> tuple[dict | None, list[str], list[str]]:
    """Parti içinde hatalı sorular (yalnız "Qn: …" hataları) düşürülür, geçenler kabul edilir; düşenler `bekleyen` kalır
    ve sonraki partide yeniden sorulur. Soru dışı hata (biçim) varsa kısmi kabul yok."""
    if not cikti:
        return None, hatalar, []
    dusen = set()
    for h in hatalar:
        m = re.match(r"(Q\d+):", h)
        if not m:
            return None, hatalar, []
        dusen.add(m.group(1))
    kalan = {Q: r for Q, r in cikti["sorular"].items() if Q not in dusen}
    if not kalan:
        return None, hatalar, sorted(dusen)
    c2 = {**cikti, "sorular": kalan}
    return c2, dogrula(c2, meta), sorted(dusen)
