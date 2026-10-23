"""Görev `asistan_nokta` — sesli sınav asistanının nokta anlatımı + soruların açıklamaları (TALIMAT_ASISTAN.md; R4).

Hedef: `<brans>:<kod>/nokta/0` — iskeletin son düzenindeki henüz kabul edilmemiş noktaların ilk partisi (≤3 nokta, ≤4 soru;
`_asistan.bekleyen_parti`). Girdi: her nokta (N) için bölüm başlığı, önceki noktanın başlığı (bağ), madde alanları (bilgi,
alt, detay, neden), sayfa metni; noktanın soruları (anahtar, kök, şıklar, doğru, örnekte açıklama).
Model yazar: nokta başlığı + 3–7 cümle {metin, ses}; her soru için kok_ses, dogru, yanlis (doğru dışı her şık), yardim (tüm şıklar).
Kapı: resmî `asistan_dogrula.check` geçici bir çıktıyla (iskelet + yalnız bu partinin noktaları) koşar; ders düzeyi kurallar
(eksik nokta/soru, bölüm sayısı, giriş/kapanış) birleştirmeye kalır. Kısmi kabul nokta düzeyinde (hatalı nokta düşer).
Uygulama: W/gorev/<kod>/asistan_nokta_<n>.json; birleştirme `asistan_nokta.birlestir(W, kod)` → W/asistan/cikti/<kod>.json.
"""
from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path

from .. import cekirdek as c
from . import _asistan, _spot

SES_ONAR = True   # ses alanlarında kısaltma/Roma rakamı okunuşu betikle (cekirdek.ses_onar)
OGE, OGE_ETIKET = ("noktalar", "dict"), r"N\d+"  # kısmi düzeltme: yalnız hatalı N'ler (yonlendir.kismi_duzeltme)
KURALLAR = ["kaynak_sadakati", "asistan_yazimi", "ses_yazimi", "sik_aciklama", "turkce_uslup", "cikti_disiplini"]
DERS_DUZEYI = re.compile(r"zorunlu nokta eksik|soru eksik/fazla|bolumler 3|nokta 1–|^giris|^kapanis|bolum\[\d+\]")


def hazirla(hedef: str, ayar: dict | None = None) -> dict:
    W, kod, _ = _spot.hedef_coz(hedef, ayar, "nokta")
    P = _asistan.plan(W, kod)
    PN = {n["id"]: n for n in P["noktalar"]}
    PS = {s["anahtar"]: s for n in P["noktalar"] for s in n["sorular"]}
    ik = _asistan.iskelet(W, kod)
    parti = _asistan.bekleyen_parti(W, kod)
    if not parti:
        raise SystemExit(f"{kod}: anlatılmamış nokta kalmadı")
    tum = _asistan.son_noktalar(W, kod)
    sira = [n["id"] for n in tum]
    S = _spot.sayfalar(W, kod)
    et = c.Etiketler()
    bloklar, meta_n = [], {}
    for n in parti:
        pn = PN[n["id"]]
        N = et.ekle("N", n["id"])
        i = sira.index(n["id"])
        onceki = PN[sira[i - 1]]["baslik"] if i else "—"
        sayfa = " ".join(" ".join(S.get(s, "").split()) for s in pn["sayfalar"][:2])[:1500]
        sor = []
        for k in n["sorular"]:
            s = PS[k]
            sor.append(f"  {k} ({'çıkmış' if s['tur'] == 'cikmis' else 'örnek'}): {s['kok']}\n"
                       + "\n".join(f"    {h}) {t}" for h, t in sorted(s["secenekler"].items())) + f"\n    Doğru: {s['dogru']}"
                       + (f"\n    Açıklama: {s['aciklama']}" if s.get("aciklama") else ""))
        bloklar.append("\n".join([
            f"### {N} — bölüm: {ik['bolumler'][n['bolum']]['baslik']} (önceki nokta: {onceki})",
            f"Başlık: {pn['baslik']}", f"Bilgi: {pn['bilgi']}", *(f"- {a}" for a in pn.get("alt") or []),
            f"Detay:\n{pn.get('detay', '')}", f"Neden önemli: {pn.get('neden', '')}", f"Sayfa metni: {sayfa}",
            "Sorular:\n" + ("\n".join(sor) if sor else "  (yok)")]))
        meta_n[N] = {"id": n["id"], "sorular": n["sorular"]}
    ornek = {"noktalar": {"N1": {"baslik": "…", "cumleler": [{"metin": "…", "ses": "…"}] * 3,
                                 "sorular": {"s3": {"kok_ses": "…", "dogru": {"metin": "Doğru! …", "ses": "Doğru! …"},
                                                    "yanlis": {"A": {"metin": "… Doğrusu: …", "ses": "… Doğrusu, …"}},
                                                    "yardim": {h: {"metin": "…", "ses": "…"} for h in "ABCDE"}}}}}}
    return {
        "amac": ("Aşağıdaki her nokta için sesli sınav asistanının anlatımını (başlık + 3–7 cümle) ve noktanın her sorusu için "
                 "`kok_ses`, `dogru`, `yanlis` (doğru şık dışındaki her şık) ve `yardim` (tüm şıklar) metinlerini yaz; her metin "
                 "`{metin, ses}` çiftidir."),
        "kurallar": KURALLAR,
        "ek_kurallar": ["Anlatım önceki noktadan devam eder; noktanın başında genel tanımı tekrar etme.",
                        "Soru, şıklar ve doğru cevap sabittir; çıktıya yazma (yalnız açıklama metinleri)."],
        "girdi": f"Ders: {P['baslik']}\n\n" + "\n\n".join(bloklar),
        "cikti_bicimi": "Yalnız şu JSON (girdideki her N ve her soru anahtarı için):\n" + json.dumps(ornek, ensure_ascii=False, indent=1),
        "denetim_listesi": ["her nokta 3–7 cümle, toplam 45–140 kelime", "her soruda dogru 'Doğru!' ile başlar",
                            "yanlis her yanlış şık için ve 'Doğrusu' içerir", "yardim beş şık için 2–3 cümle",
                            "ses alanlarında rakam/simge/büyük harfli kısaltma/tek büyük harf yok"],
        "esleme": et.esleme,
        "meta": {"w": str(W), "kod": kod, "kurul": None, "n": meta_n},
    }


def derle(cevap, esleme: dict, meta: dict):
    j = c.json_cikar(cevap)
    if not isinstance(j, dict) or not isinstance(j.get("noktalar"), dict):
        return None, ["cevap JSON değil ya da 'noktalar' nesnesi yok"]
    out, e = [], []
    for N, mn in meta["n"].items():
        r = j["noktalar"].get(N)
        if not isinstance(r, dict):
            e.append(f"{N}: cevapta kayıt yok"); continue
        sor = []
        for k in mn["sorular"]:
            s = (r.get("sorular") or {}).get(k)
            if not isinstance(s, dict):
                e.append(f"{N}: soru {k} için kayıt yok"); continue
            sor.append({"anahtar": k, "kok_ses": str(s.get("kok_ses") or "").strip(), "dogru": s.get("dogru"),
                        "yanlis": {str(h).upper()[:1]: v for h, v in (s.get("yanlis") or {}).items()},
                        "yardim": {str(h).upper()[:1]: v for h, v in (s.get("yardim") or {}).items()}})
        out.append({"id": mn["id"], "baslik": str(r.get("baslik") or "").strip(), "cumleler": r.get("cumleler") or [],
                    "sorular": sor, "_etiket": N})
    return {"surum": 1, "kod": meta["kod"], "noktalar": out}, e


def _gecici_cikti(W: Path, kod: str, noktalar: list[dict]) -> dict:
    """İskelet + verilen noktalar (yalnız bunlar) → resmî doğrulayıcının okuyacağı çıktı biçimi."""
    ik = _asistan.iskelet(W, kod)
    ids = {n["id"] for n in noktalar}
    nd = {n["id"]: {k: v for k, v in n.items() if not k.startswith("_")} for n in noktalar}
    return {"kod": kod, "giris": ik["giris"], "kapanis": ik["kapanis"],
            "bolumler": [{"baslik": b["baslik"], "neden": b["neden"], "noktalar": [nd[i] for i in b["noktalar"] if i in ids]}
                         for b in ik["bolumler"]]}


def resmi_kapi(o: dict, W: Path, kod: str) -> list[str]:
    AD = _asistan.ad()
    with tempfile.TemporaryDirectory(prefix="asistan_kapi_") as t:
        T = Path(t)
        (T / "pdf_metin").mkdir()
        (T / "pdf_metin" / f"{kod}.md").symlink_to(W / "pdf_metin" / f"{kod}.md")
        (T / "asistan" / "plan").mkdir(parents=True)
        (T / "asistan" / "plan" / f"{kod}.json").symlink_to(W / "asistan" / "plan" / f"{kod}.json")
        (T / "asistan" / "cikti").mkdir()
        p = T / "asistan" / "cikti" / f"{kod}.json"
        p.write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")
        e, _, _ = AD.check(str(p))
    return e


def dogrula(cikti: dict, meta: dict) -> list[str]:
    W, kod = Path(meta["w"]), meta["kod"]
    e = [x for x in resmi_kapi(_gecici_cikti(W, kod, cikti["noktalar"]), W, kod) if not DERS_DUZEYI.search(x)]
    # nokta/soru kimliği → modelin gördüğü etiket
    et = {n["id"]: n["_etiket"] for n in cikti["noktalar"]}
    soru_et = {s["anahtar"]: n["_etiket"] for n in cikti["noktalar"] for s in n["sorular"]}
    out = []
    for x in e:
        m = re.match(r"([a-z]\d+-\d{2}|s\d+)([.:])", x)
        if m and m.group(1) in et:
            out.append(et[m.group(1)] + x[len(m.group(1)):])
        elif m and m.group(1) in soru_et:
            out.append(f"{soru_et[m.group(1)]}.{x}")
        else:
            out.append(x)
    return out


def kismi_kabul(cikti: dict | None, hatalar: list[str], meta: dict):
    if not cikti:
        return None, hatalar, []
    dusen = set()
    for h in hatalar:
        m = re.match(r"(N\d+)\b", h)
        if not m:
            return None, hatalar, []
        dusen.add(m.group(1))
    kalan = [n for n in cikti["noktalar"] if n["_etiket"] not in dusen]
    if not kalan:
        return None, hatalar, sorted(dusen)
    c2 = {**cikti, "noktalar": kalan}
    return c2, dogrula(c2, meta), sorted(dusen)


def tersine(cikti: dict, esleme: dict, meta: dict) -> str:
    return json.dumps({"noktalar": {n["_etiket"]: {"baslik": n["baslik"], "cumleler": n["cumleler"],
                                                    "sorular": {s["anahtar"]: {k: s[k] for k in ("kok_ses", "dogru", "yanlis", "yardim")}
                                                                for s in n["sorular"]}} for n in cikti["noktalar"]}},
                      ensure_ascii=False, indent=1)


ozet = tersine


def uygula(cikti: dict, meta: dict, cikis: Path | None = None, k1_izin: bool = False) -> Path:
    W = Path(cikis) if cikis else Path(meta["w"])
    if cikis is None and "/spot_cozucu/" in str(W) and not k1_izin and re.match(r"^[a-z]", meta["kod"]):
        raise SystemExit("Kurul 1 branş klasörüne yazım yok: --cikis ya da --k1-izin")
    d = W / "gorev" / meta["kod"]
    p = d / f"asistan_nokta_{len(list(d.glob('asistan_nokta_*.json'))) if d.exists() else 0}.json"
    c.yaz(p, cikti)
    return p


def birlestir(W: Path, kod: str, log=print) -> int:
    """İskelet + tüm nokta partileri → W/asistan/cikti/<kod>.json (resmî doğrulayıcı 0 HATA değilse yazılmaz)."""
    kalan = [n["id"] for n in _asistan.son_noktalar(W, kod) if n["id"] not in _asistan.yapilan(W, kod)]
    if kalan:
        log(f"{kod}: {len(kalan)} nokta henüz anlatılmadı ({kalan[:4]})"); return 2
    noktalar = [n for p in sorted((W / "gorev" / kod).glob("asistan_nokta_*.json")) for n in (c.oku(p) or {}).get("noktalar", [])]
    o = _gecici_cikti(W, kod, noktalar)
    e = resmi_kapi(o, W, kod)
    for x in e:
        log(f"  HATA {x}")
    log(f"{kod}: asistan {len(o['bolumler'])} bölüm, {len(noktalar)} nokta · {len(e)} HATA")
    if e:
        return 1
    c.yaz(W / "asistan" / "cikti" / f"{kod}.json", {**o, "_kaynak": {"yontem": "gorev"}})
    return 0
