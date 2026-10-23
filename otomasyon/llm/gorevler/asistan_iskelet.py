"""Görev `asistan_iskelet` — sesli sınav asistanının ders iskeleti (TALIMAT_ASISTAN.md "Hiyerarşi"; R4).

Hedef: `<brans>:<kod>/iskelet/0` (W; sınamada `--ayar w=…`). Girdi: asistan planının noktaları (N etiketli: zorunlu/seçmeli,
puan, sayfa, başlık, bilgi) ve her noktanın soruları (anahtar + kısa kök). Model yazar: 3–8 bölüm (başlık + `neden` {metin,ses},
nokta sırası), atlanan seçmeli noktalar, kronoloji için soru taşıma (bir soru, bilgisi daha sonraki bir noktada anlatılıyorsa
oraya), giriş (1–2 cümle) ve kapanış (2–4 cümle). Küçük çıktı; ağır anlatım `asistan_nokta` görevindedir.
Kapı (betik): zorunlu noktaların hepsi tam bir kez; seçmeli ya yer alır ya atlanır; bölüm 3–8 ve bölüm başına 1–10 nokta;
soru yalnız SONRAKİ bir noktaya taşınır; giriş/kapanış/neden resmî `asistan_dogrula.cift` kurallarıyla (ses yazımı, üslup).
Uygulama: W/gorev/<kod>/asistan_iskelet.json.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .. import cekirdek as c
from . import _asistan, _spot

SES_ONAR = True   # ses alanlarında kısaltma/Roma rakamı okunuşu betikle (cekirdek.ses_onar)
KURALLAR = ["kaynak_sadakati", "asistan_yazimi", "ses_yazimi", "turkce_uslup", "cikti_disiplini"]


def hazirla(hedef: str, ayar: dict | None = None) -> dict:
    W, kod, _ = _spot.hedef_coz(hedef, ayar, "iskelet")
    P = _asistan.plan(W, kod)
    et = c.Etiketler()
    satir = []
    for n in P["noktalar"]:
        N = et.ekle("N", n["id"])
        sor = "; ".join(f"{s['anahtar']}: {s['kok'][:90]}" for s in n["sorular"])
        satir.append(f"{N} ({'zorunlu' if n['zorunlu'] else 'seçmeli'}, puan {n['puan']}, s. {','.join(map(str, n['sayfalar'])) or '-'}): "
                     f"{n['baslik']} — {re.sub(r'[*]', '', n['bilgi'])[:220]}" + (f"\n    Sorular: {sor}" if sor else ""))
    ornek = {"bolumler": [{"baslik": "…", "neden": {"metin": "…", "ses": "…"}, "noktalar": ["N1", "N2"]}],
             "atlanan": ["N7"], "soru_tasima": {"s5": "N9"},
             "giris": [{"metin": "…", "ses": "…"}], "kapanis": [{"metin": "…", "ses": "…"}, {"metin": "…", "ses": "…"}]}
    return {
        "amac": ("Bu dersin sesli sınav asistanı için iskelet kur: noktaları slayttaki mantıksal akışla 3–8 bölüme ayır (genelden "
                 "özele: tanım → mekanizma → morfoloji → ayırıcı nokta → tedavi), her bölüme kısa başlık ve 1–2 cümlelik `neden` "
                 "(bu bölüm neden önemli, önceki bölümle bağı) yaz; dersin giriş ve kapanış cümlelerini yaz."),
        "kurallar": KURALLAR,
        "ek_kurallar": [
            "Zorunlu noktaların HEPSİ tam bir kez yer alır; seçmeli noktadan anlatıma değer katmayanı `atlanan`a yaz.",
            "Bir sorunun bilgisi daha SONRAKİ bir noktada anlatılıyorsa `soru_tasima` ile o noktaya taşı (kronoloji); geriye taşıma yok.",
            "Bölüm başlığı en çok 9 kelime; `giris` 1–2 cümle (dersin sınavdaki ağırlığı ve en çok sorulan 2–3 konu; selamlama yok); "
            "`kapanis` 2–4 cümle (akılda tutulacak 3–4 nokta).",
        ],
        "girdi": f"Ders: {P['baslik']}\nÖzet: {P.get('ozet', '')}\nSınavdaki önemi: {P.get('neden_onemli', '')}\n\n## Noktalar\n"
                 + "\n".join(satir),
        "cikti_bicimi": "Yalnız şu JSON:\n" + json.dumps(ornek, ensure_ascii=False, indent=1),
        "denetim_listesi": ["zorunlu noktalar tam bir kez", "her seçmeli ya bölümde ya atlanan'da", "3–8 bölüm, bölüm başına 1–10 nokta",
                            "taşıma yalnız sonraki noktaya", "ses alanlarında rakam/simge/kısaltma yok"],
        "esleme": et.esleme,
        "meta": {"w": str(W), "kod": kod, "kurul": None, "_esleme": dict(et.esleme)},
    }


def derle(cevap, esleme: dict, meta: dict):
    j = c.json_cikar(cevap)
    if not isinstance(j, dict) or not isinstance(j.get("bolumler"), list):
        return None, ["cevap JSON değil ya da 'bolumler' yok"]
    et = c.Etiketler(esleme)
    e = []
    bol = []
    for i, b in enumerate(j["bolumler"]):
        ids = []
        for N in b.get("noktalar") or []:
            u = et.uzun(str(N))
            if not u:
                e.append(f"bölüm {i + 1}: bilinmeyen nokta {N}")
            else:
                ids.append(u)
        bol.append({"baslik": str(b.get("baslik") or "").strip(), "neden": b.get("neden"), "noktalar": ids})
    atl = [et.uzun(str(N)) for N in j.get("atlanan") or []]
    if None in atl:
        e.append("atlanan: bilinmeyen nokta etiketi")
    tas = {}
    for k, N in (j.get("soru_tasima") or {}).items():
        u = et.uzun(str(N))
        if not u:
            e.append(f"soru_tasima {k}: bilinmeyen nokta {N}")
        else:
            tas[str(k).strip()] = u
    return {"surum": 1, "kod": meta["kod"], "bolumler": bol, "atlanan": [x for x in atl if x], "soru_tasima": tas,
            "giris": j.get("giris") or [], "kapanis": j.get("kapanis") or []}, e


def dogrula(cikti: dict, meta: dict) -> list[str]:
    W, kod = Path(meta["w"]), meta["kod"]
    P = _asistan.plan(W, kod)
    PN = {n["id"]: n for n in P["noktalar"]}
    ters = {v: k for k, v in c.Etiketler(meta.get("_esleme") or {}).esleme.items()}
    lab = lambda i: ters.get(i, i)  # noqa: E731
    AD = _asistan.ad()
    e = []
    if not 3 <= len(cikti["bolumler"]) <= 8:
        e.append(f"{len(cikti['bolumler'])} bölüm — 3–8 olmalı")
    sira = [nid for b in cikti["bolumler"] for nid in b["noktalar"]]
    if len(sira) != len(set(sira)):
        e.append("bir nokta birden çok yerde")
    for i, b in enumerate(cikti["bolumler"]):
        if not b["baslik"] or len(b["baslik"].split()) > 9:
            e.append(f"bölüm {i + 1}: başlık 1–9 kelime")
        if not 1 <= len(b["noktalar"]) <= 10:
            e.append(f"bölüm {i + 1}: {len(b['noktalar'])} nokta (1–10)")
        AD.cift(e, f"bölüm {i + 1}.neden", b["neden"], 6, 48)
    for nid, n in PN.items():
        if n["zorunlu"] and nid not in sira:
            e.append(f"zorunlu nokta {lab(nid)} bölümlerde yok")
        if not n["zorunlu"] and nid not in sira and nid not in cikti["atlanan"]:
            e.append(f"seçmeli nokta {lab(nid)} ne bölümde ne atlanan'da")
        if nid in cikti["atlanan"] and (n["zorunlu"] or n["sorular"]):
            e.append(f"{lab(nid)} atlanamaz ({'zorunlu' if n['zorunlu'] else 'sorusu var'})")
    soru_yeri = {s["anahtar"]: nid for nid, n in PN.items() for s in n["sorular"]}
    for k, hedef in cikti["soru_tasima"].items():
        if k not in soru_yeri:
            e.append(f"soru_tasima: {k} planda yok"); continue
        a = soru_yeri[k]
        if hedef not in sira or a not in sira or sira.index(hedef) <= sira.index(a):
            e.append(f"soru_tasima {k}: yalnız SONRAKİ bir noktaya taşınabilir ({lab(a)} → {lab(hedef)})")
    if not 1 <= len(cikti["giris"]) <= 2:
        e.append("giris 1–2 cümle")
    for i, x in enumerate(cikti["giris"]):
        AD.cift(e, f"giris[{i}]", x, 4, 45)
    if not 2 <= len(cikti["kapanis"]) <= 4:
        e.append("kapanis 2–4 cümle")
    for i, x in enumerate(cikti["kapanis"]):
        AD.cift(e, f"kapanis[{i}]", x, 4, 45)
    return [re.sub(r"\b([a-z]\d+-\d{2})\b", lambda m: lab(m.group(1)), x) for x in e]


def tersine(cikti: dict, esleme: dict, meta: dict) -> str:
    et = c.Etiketler(esleme)
    return json.dumps({"bolumler": [{"baslik": b["baslik"], "neden": b["neden"], "noktalar": [et.kisa(i) for i in b["noktalar"]]}
                                    for b in cikti["bolumler"]],
                       "atlanan": [et.kisa(i) for i in cikti["atlanan"]],
                       "soru_tasima": {k: et.kisa(v) for k, v in cikti["soru_tasima"].items()},
                       "giris": cikti["giris"], "kapanis": cikti["kapanis"]}, ensure_ascii=False, indent=1)


ozet = tersine


def uygula(cikti: dict, meta: dict, cikis: Path | None = None, k1_izin: bool = False) -> Path:
    W = Path(cikis) if cikis else Path(meta["w"])
    if cikis is None and "/spot_cozucu/" in str(W) and not k1_izin and re.match(r"^[a-z]", meta["kod"]):
        raise SystemExit("Kurul 1 branş klasörüne yazım yok: --cikis ya da --k1-izin")
    p = W / "gorev" / meta["kod"] / "asistan_iskelet.json"
    c.yaz(p, cikti)
    return p
