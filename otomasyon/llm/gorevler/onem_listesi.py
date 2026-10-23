"""Görev `onem_listesi` — ders zincirinin `onem` adımı (TALIMAT_ONEM.md) sayfa grubu başına (ICERIK_MOTORU_V3.md §14, R4).

Hedef: `<brans>:<kod>/parca/<n>` (W = meds_temp/spot_cozucu/<brans>, sınamada `--ayar w=…`). Parçalar `_spot.parcalar`
(≤10 sayfa, ≤2.600 sözcük); madde/örnek/zorluk hedefleri ders düzeyinden belirlenimci paylaştırılır (`_spot.parca_plani`).
Girdi: parçanın sayfa satırları (L etiketli, sayfa başına önem haritası puanı) + bu sayfalara düşen çıkmış temsilciler (Q).
Model yazar: maddeler (puan, başlık, bilgi, alt, tür, alıntı = L etiketleri, neden, detay, bağlı Q'lar, örnek sorular) +
bu parçadaki her Q için karar (bağla ya da `elenen`). Alıntı metnini model YAZMAZ: derleyici L satırlarını birebir alır.
Kapı: resmî `scripts/spot_cozucu/onem_dogrula.py` parçaya uygulanır (ders düzeyi sayım/bant kuralları birleştirmeye kalır) +
parça hedefleri (madde ±2, örnek sayısı ve zorluk dağılımı birebir, her Q'ya karar).
Uygulama: W/gorev/<kod>/onem_parca_<n>.json; birleştirme `otomasyon/llm/spot_birlestir.py onem`.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

from .. import cekirdek as c
from . import _spot

OGE = ("maddeler", "liste")   # kısmi düzeltme: yalnız hatalı maddeler (oge_hatalari, yonlendir.kismi_duzeltme)
KURALLAR = ["onem_yazimi", "ornek_soru_spot", "turkce_uslup", "cikti_disiplini"]
TUR = ["tanim", "en_sik", "karakteristik", "sayi", "eslesme", "mekanizma", "siniflama", "tuzak", "tani_tedavi"]
ELEN = ["pdf_disi", "anahtar_celiskili", "gorsel", "belirsiz"]


def hazirla(hedef: str, ayar: dict | None = None) -> dict:
    W, kod, n = _spot.hedef_coz(hedef, ayar, "parca")
    plan = _spot.parca_plani(W, kod)
    if n >= len(plan["parcalar"]):
        raise SystemExit(f"{kod}: {len(plan['parcalar'])} parça var (0–{len(plan['parcalar']) - 1})")
    a, b = plan["parcalar"][n]
    S = _spot.sayfalar(W, kod)
    oh = {s["sayfa"]: s for s in (c.oku(W / "onem_haritasi" / f"{kod}.json") or {}).get("sayfalar", [])}
    C = {x["id"]: x for x in _spot.cikmislar(W, kod)}
    et = c.Etiketler()
    q_sayfa = {}
    for cid in plan["cikmis"][n]:
        Q = et.ekle("Q", cid)
        q_sayfa[Q] = cid
    diger = []
    for x in _spot.cikmislar(W, kod):
        if x["id"] not in q_sayfa.values():
            K = et.ekle("K", x["id"])
            diger.append(f"{K}: {x['kok'][:160]} → {x['secenekler'].get(x['dogru'], '')[:60]}")
    satir_metin = {}
    bloklar = []
    for no in range(a, b + 1):
        if no not in S:
            continue
        o = oh.get(no) or {}
        ust = f"### Sayfa {no}" + (f" (sınav puanı {o.get('puan')})" if o.get("puan") is not None else "")
        st = []
        for s in _spot.satirlar(S[no]):
            L = et.ekle("L", f"{no}|{len(satir_metin)}")
            satir_metin[L] = (no, s)
            st.append(f"{L}: {s}")
        bloklar.append(ust + "\n" + ("\n".join(st) if st else "(bu sayfada metin yok)"))
    cik_blok = []
    for Q, cid in q_sayfa.items():
        x = C[cid]
        cik_blok.append(f"{Q} ({', '.join(x.get('yillar') or [x.get('yil', '')])}; {1 + len(x.get('tekrar') or [])} kez): {x['kok']}\n"
                        + "\n".join(f"  {h}) {t}" for h, t in sorted(x["secenekler"].items())) + f"\n  Doğru: {x['dogru']}"
                        + ("  (kayıt şüpheli)" if x.get("dikkat") else ""))
    hm, ho, zr = plan["madde"][n], plan["ornek"][n], plan["zorluk"][n]
    ornek = {"maddeler": [{"puan": 92, "baslik": "…", "bilgi": "… **terim** …", "alt": [], "tur": "eslesme",
                           "alinti": ["L12", "L13"], "neden": "…", "detay": "- **…:** …\n- **…:** …", "cikmis": ["Q1"],
                           "ornek": [{"kok": "…?", "secenekler": {h: "…" for h in "ABCDE"}, "dogru": "C", "zorluk": "orta",
                                      "aciklama": "…", "sayfa": [a]}]}],
             "elenen": [{"q": "Q2", "neden": "pdf_disi", "not": "kısa gerekçe, sayfa n"}],
             "parca_ozeti": "Bu bölümde işlenen konuların 1 cümlelik özeti ('sayfa', 'parça' sözcükleri olmadan)."}
    girdi = (f"Ders: {json.loads((W / 'girdi' / f'{kod}.json').read_text())['ad']} — sayfa {a}–{b} (parça {n + 1}/{len(plan['parcalar'])})\n\n"
             + "\n\n".join(bloklar)
             + ("\n\n## Bu sayfalarla eşleşen çıkmış sorular (her biri için karar ver)\n" + "\n".join(cik_blok) if cik_blok else
                "\n\n## Bu sayfalarla eşleşen çıkmış soru yok")
             + ("\n\n## Dersin öteki çıkmış soruları (karar verme; örnek soruların bunlarla AYNI bilgiyi sormaması gerekir)\n"
                + "\n".join(diger) if diger else ""))
    return {
        "amac": (f"Bu ders PDF'inin {a}–{b}. sayfaları için sınav odaklı önem listesi yaz: TAM OLARAK {hm} madde (±1 kabul) ve "
                 f"maddelere dağıtılmış TAM OLARAK {ho} örnek soru (kolay {zr['kolay']}, orta {zr['orta']}, zor {zr['zor']}). "
                 f"Her çıkmış soru (Q) için karar ver: onu çözdürecek bilgiyi taşıyan maddenin `cikmis` listesine koy (en çok 2 madde) "
                 f"ya da `elenen`e yaz."),
        "kurallar": KURALLAR,
        "ek_kurallar": [
            f"`tur` şunlardan biri: {', '.join(TUR)}. `elenen.neden` şunlardan biri: {', '.join(ELEN)} ya da `tekrar:Qn` (aynı bilgiyi soran başka Q).",
            "Bir maddede en çok 2 örnek soru; örnek sorular parçanın farklı önemli bilgilerine yayılsın.",
            "Çıkmış sorunun kökü/şıkları/anahtarı değiştirilmez; anahtar satırlarla çelişiyorsa `anahtar_celiskili` ile ele.",
            "Bağlanan Q'nun maddesi yüksek puanlı olur (çoğu 80+).",
        ],
        "girdi": girdi,
        "cikti_bicimi": "Yalnız şu JSON:\n" + json.dumps(ornek, ensure_ascii=False, indent=1),
        "denetim_listesi": [f"{hm}±1 madde, {ho}±1 örnek (kolay {zr['kolay']}/orta {zr['orta']}/zor {zr['zor']})",
                            "her Q bağlandı ya da elendi", "alıntı L etiketleri girdide, bilgiyi içeren satırlar",
                            "bilgi/alt'taki sayılar satırlarda birebir", "detay 60–250 kelime, maddeli, bağlı soruları çözdürür"],
        "esleme": et.esleme,
        "meta": {"_esleme": dict(et.esleme), "w": str(W), "kod": kod, "parca": n, "sayfa": [a, b], "madde": hm, "ornek": ho, "zorluk": zr,
                 "q": q_sayfa, "satir": {L: list(v) for L, v in satir_metin.items()}, "kurul": None},
    }


def _alinti(Ler: list[str], meta: dict) -> tuple[list[dict], list[str]]:
    """L etiketleri → {sayfa, metin} (ardışık satırlar birleşir; ≤30 kelime, birebir önek)."""
    e, gruplar = [], []
    for L in Ler:
        v = meta["satir"].get(L)
        if not v:
            e.append(f"girdide olmayan satır etiketi {L}"); continue
        sayfa, metin = v
        if gruplar and gruplar[-1]["sayfa"] == sayfa and gruplar[-1]["son"] == int(L[1:]) - 1:
            gruplar[-1]["metin"] += " " + metin; gruplar[-1]["son"] = int(L[1:])
        else:
            gruplar.append({"sayfa": sayfa, "metin": metin, "son": int(L[1:])})
    out = []
    sira = sorted(meta["satir"].items(), key=lambda kv: int(kv[0][1:]))
    for g in gruplar[:3]:
        # kısa alıntı (başlık satırı) aynı sayfanın sonraki satırlarıyla ≥4 sözcüğe tamamlanır (ardışık → yine birebir)
        sonraki = [t for L, (sy, t) in sira if sy == g["sayfa"] and int(L[1:]) > g["son"]]
        while len(g["metin"].split()) < 4 and sonraki:
            g["metin"] += " " + sonraki.pop(0)
        w = g["metin"].split()
        out.append({"sayfa": g["sayfa"], "metin": " ".join(w[:30])})
    return out, e


def derle(cevap, esleme: dict, meta: dict):
    j = c.json_cikar(cevap)
    if not isinstance(j, dict) or not isinstance(j.get("maddeler"), list):
        return None, ["cevap JSON değil ya da 'maddeler' dizisi yok"]
    e, maddeler = [], []
    kod = meta["kod"]
    for i, m in enumerate(j["maddeler"], 1):
        if not isinstance(m, dict):
            e.append(f"madde {i}: nesne değil"); continue
        Ler = [str(x).strip() for x in (m.get("alinti") or [])]
        al, ea = _alinti(Ler, meta)
        e += [f"madde {i}: {x}" for x in ea]
        cik = []
        for Q in m.get("cikmis") or []:
            if str(Q).strip() in meta["q"]:
                cik.append(meta["q"][str(Q).strip()])
            else:
                e.append(f"madde {i}: bilinmeyen çıkmış etiketi {Q}")
        orn = []
        for q in m.get("ornek") or []:
            if isinstance(q, dict):
                sy = [int(x) for x in (q.get("sayfa") or []) if str(x).isdigit()]
                kok = str(q.get("kok") or "").strip()
                if kok and not kok.endswith("?"):
                    kok = kok.rstrip(".:") + "?"                # biçim: soru kökü "?" ile biter
                orn.append({"kok": kok, "secenekler": {str(h).strip().upper()[:1]: str(t).strip()
                            for h, t in (q.get("secenekler") or {}).items()}, "dogru": str(q.get("dogru") or "").strip().upper()[:1],
                            "zorluk": q.get("zorluk"), "aciklama": str(q.get("aciklama") or "").strip(), "sayfa": sy})
        maddeler.append({"id": f"{kod}-{i:02d}", "puan": m.get("puan"), "baslik": str(m.get("baslik") or "").strip(),
                         "bilgi": str(m.get("bilgi") or "").strip(), "alt": [str(x).strip() for x in (m.get("alt") or [])],
                         "tur": m.get("tur"), "alinti": al, "_alinti_L": Ler, "neden": str(m.get("neden") or "").strip(),
                         "detay": str(m.get("detay") or "").strip(), "cikmis": cik, "ornek": orn})
    elenen = []
    for x in j.get("elenen") or []:
        Q = str(x.get("q") or "").strip()
        if Q not in meta["q"]:
            e.append(f"elenen: bilinmeyen çıkmış etiketi {Q}"); continue
        neden = str(x.get("neden") or "")
        m = re.fullmatch(r"tekrar:(Q\d+)", neden)
        if m:
            if m.group(1) not in meta["q"]:
                e.append(f"elenen {Q}: tekrar edilen {m.group(1)} bu parçada yok"); continue
            neden = f"tekrar:{meta['q'][m.group(1)]}"
        elenen.append({"id": meta["q"][Q], "neden": neden, "not": str(x.get("not") or "").strip()})
    return {"surum": 1, "kod": kod, "parca": meta["parca"], "sayfa": meta["sayfa"], "maddeler": maddeler,
            "elenen_cikmis": elenen, "parca_ozeti": str(j.get("parca_ozeti") or "").strip()}, e


# ders düzeyi kurallar (parçada değil birleştirmede sağlanır)
DERS_DUZEYI = re.compile(r"madde sayısı|bandında|örnek soru \d+ \(beklenen|zorluk |harf dağılımı|karar yok|ozet|neden_onemli|baslik eksik|pdf eksik")


def resmi_kapi(onem: dict, W: Path, kod: str) -> tuple[list[str], list[str]]:
    """Resmî onem_dogrula.check'i geçici bir çalışma klasöründe çalıştırır (pdf_metin/girdi/cikmis bağlantı)."""
    sys.path.insert(0, str(c.KOK / "scripts" / "spot_cozucu"))
    import onem_dogrula as OD
    with tempfile.TemporaryDirectory(prefix="onem_kapi_") as t:
        T = Path(t)
        for alt in ("pdf_metin", "girdi", "cikmis"):
            (T / alt).mkdir()
            kaynak = W / alt / f"{kod}.{'md' if alt == 'pdf_metin' else 'json'}"
            if kaynak.exists():
                (T / alt / kaynak.name).symlink_to(kaynak)
        (T / "onem").mkdir()
        p = T / "onem" / f"{kod}.json"
        p.write_text(json.dumps(onem, ensure_ascii=False), encoding="utf-8")
        e, w, _ = OD.check(p)
    return e, w


def dogrula(cikti: dict, meta: dict) -> list[str]:
    W, kod = Path(meta["w"]), meta["kod"]
    tum = {"kod": kod, "baslik": "x", "pdf": "x", "ozet": "geçici özet " * 4, "neden_onemli": "geçici gerekçe " * 4,
           "maddeler": cikti["maddeler"], "elenen_cikmis": cikti["elenen_cikmis"]}
    e, _ = resmi_kapi(tum, W, kod)
    parca_q = set(meta["q"].values())
    etiket = {v: k for k, v in meta.get("_esleme", {}).items() if k[0] in "QK"}
    e = [re.sub(r"(çıkmış )(\S+)", lambda m: m.group(1) + etiket.get(m.group(2), m.group(2)), x) for x in e]
    parca_et = set(meta["q"])
    e = [x for x in e if not DERS_DUZEYI.search(x)
         or (re.search(r"çıkmış (\S+): karar yok", x) and re.search(r"çıkmış (\S+):", x).group(1) in parca_et)]
    e = [x for x in e if "karar yok" not in x]              # karar denetimi aşağıda parça Q'larıyla yapılır
    # parça hedefleri
    n = len(cikti["maddeler"])
    if abs(n - meta["madde"]) > 1:
        e.append(f"{n} madde — {meta['madde']}±1 olmalı")
    orn = [q for m in cikti["maddeler"] for q in m["ornek"]]
    if abs(len(orn) - meta["ornek"]) > 1:
        e.append(f"{len(orn)} örnek soru — {meta['ornek']}±1 olmalı")
    for z, k in meta["zorluk"].items():
        v = sum(1 for q in orn if q.get("zorluk") == z)
        if abs(v - k) > 1 or (z == "zor" and v < k):     # zor eksik kalamaz: ders oranı %15–25 (H32)
            e.append(f"zorluk {z}: {v} — {k} olmalı ({'en az ' + str(k) if z == 'zor' else '±1'})")
    karar = {x["id"] for x in cikti["elenen_cikmis"]} | {cc for m in cikti["maddeler"] for cc in m["cikmis"]}
    for cid in parca_q - karar:
        Q = next(k for k, v in meta["q"].items() if v == cid)
        e.append(f"çıkmış {Q}: karar yok (bir maddeye bağla ya da elenen'e yaz)")
    for m in cikti["maddeler"]:
        if not m["alinti"]:
            e.append(f"{m['id']}: alinti boş (bilgiyi taşıyan L etiketlerini ver)")
    # çözülebilirlik (TALIMAT_ONEM): bağlanan çıkmış, maddedeki bilgiyle çözülebilmeli
    C = {x["id"]: x for x in _spot.cikmislar(W, kod)}
    ters = {v: k for k, v in meta["q"].items()}
    olumsuz = re.compile(r"değil|yanlış|yer almaz|almaz|bulunmaz|görülmez|beklenmez|olamaz|dışında", re.I)
    for m in cikti["maddeler"]:
        mk = c.kokler(" ".join([m["bilgi"], *m["alt"], m["detay"]]), en_az=3) | c.sayilar(m["detay"] + " " + m["bilgi"])
        for cid in m["cikmis"]:
            x = C.get(cid)
            if not x:
                continue
            Q = ters.get(cid, cid)
            if olumsuz.search(x["kok"]):
                oteki = [t for h, t in x["secenekler"].items() if h != x["dogru"] and c.kokler(t, en_az=3)]
                tutan = sum(1 for t in oteki if c.kokler(t, en_az=3) & mk)
                if oteki and tutan < min(2, len(oteki)):
                    e.append(f"{m['id']}: bağlı {Q} (olumsuz kök) maddeyle çözülemiyor — öteki şıkların bilgisi detayda yok "
                             f"({tutan}/{len(oteki)}); detayı satırlardan genişlet ya da {Q}'yu pdf_disi ile ele")
            else:
                dogru_t = x["secenekler"].get(x["dogru"], "")
                hk = c.kokler(dogru_t, en_az=3) | c.sayilar(dogru_t)
                # hesap sorusu (doğru şık yalnız tarih/sayı/birim: Naegele, doz, oran): cevap maddede yazmaz, kuraldan
                # hesaplanır → kökteki kural/kavram terimlerinden en az ikisi maddede olmalı (H31)
                hesap = bool(re.search(r"\d", dogru_t)) and not re.sub(r"[\d\s.,/:%–-]|\b(gün|hafta|ay|yıl|saat|dk|mg|ml|kg|g|cm|mm)\b",
                                                                       "", dogru_t, flags=re.I)
                if hesap and len(c.kokler(x["kok"], en_az=4) & mk) >= 2:
                    continue
                if hk and not (hk & mk):
                    e.append(f"{m['id']}: bağlı {Q} maddeyle çözülemiyor — doğru cevabın bilgisi bilgi/alt/detayda yok; "
                             f"detayı satırlardan genişlet ya da {Q}'yu ele")
    if re.search(r"\b(sayfa\w*|parça\w*)\b", cikti.get("parca_ozeti", ""), re.I):
        e.append("parca_ozeti: 'sayfa/parça' sözcüğü olmadan dersin bu bölümünün konusunu söyle")
    return e


def tersine(cikti: dict, esleme: dict, meta: dict) -> str:
    ters_q = {v: k for k, v in meta["q"].items()}
    out = {"maddeler": [{"puan": m["puan"], "baslik": m["baslik"], "bilgi": m["bilgi"], "alt": m["alt"], "tur": m["tur"],
                         "alinti": m["_alinti_L"], "neden": m["neden"], "detay": m["detay"],
                         "cikmis": [ters_q[x] for x in m["cikmis"]], "ornek": m["ornek"]} for m in cikti["maddeler"]],
           "elenen": [{"q": ters_q[x["id"]], "neden": (f"tekrar:{ters_q[x['neden'][7:]]}" if x["neden"].startswith("tekrar:")
                                                       else x["neden"]), "not": x["not"]} for x in cikti["elenen_cikmis"]],
           "parca_ozeti": cikti["parca_ozeti"]}
    return json.dumps(out, ensure_ascii=False, indent=1)


ozet = tersine


def uygula(cikti: dict, meta: dict, cikis: Path | None = None, k1_izin: bool = False) -> Path:
    """Parça çıktısı W/gorev/<kod>/onem_parca_<n>.json (birleştirici okur). W kurulun çalışma klasörüdür; Kurul 1
    klasörüne yazmak için --cikis (sınama) ya da --k1-izin."""
    W = Path(cikis) if cikis else Path(meta["w"])
    if cikis is None and "/spot_cozucu/" in str(W) and not k1_izin and re.match(r"^[a-z]", meta["kod"]):
        raise SystemExit("Kurul 1 branş klasörüne yazım yok: --cikis ile sınama klasörü ver ya da --k1-izin")
    p = W / "gorev" / meta["kod"] / f"onem_parca_{meta['parca']}.json"
    c.yaz(p, cikti)
    return p


def sinama_ornekleri(meta: dict) -> tuple[dict, list[dict]]:
    """Öz-sınama: sınama verisindeki altın parça (resmî kapıdan geçmiş) → iyi cevap; bilinen kötüler."""
    altin = c.oku(Path(meta["w"]) / "altin" / f"onem_parca_{meta['parca']}.json")
    iyi = json.loads(tersine(altin, {}, meta))
    kotu = [{"ad": "olmayan satır", "degistir": [[["maddeler", 0, "alinti"], ["L9999"]]], "beklenen": "girdide olmayan satır etiketi"},
            {"ad": "olmayan çıkmış", "degistir": [[["maddeler", 0, "cikmis"], ["Q99"]]], "beklenen": "bilinmeyen çıkmış etiketi"},
            {"ad": "kısa detay", "degistir": [[["maddeler", 0, "detay"], "- **Kısa:** yetersiz açıklama"]], "beklenen": "detay"},
            {"ad": "özet süreç dili", "degistir": [[["parca_ozeti"], "Bu sayfalarda sifiliz anlatılıyor."]], "beklenen": "parca_ozeti"}]
    return iyi, kotu


def oge_hatalari(hatalar: list[str], meta: dict):
    """Kısmi düzeltme: hata → madde indisi (0 tabanlı). `<kod>-03…`, `<kod>/<kod>-03.ornek1…` (1 tabanlı kimlik) ve ortak
    kapıların `maddeler[2]…` yolu. Parça düzeyi hata (sayı, zorluk, karar, özet) varsa None → tam düzeltme istemi."""
    kod = re.escape(meta["kod"])
    out = set()
    for h in hatalar:
        m = re.match(rf"(?:{kod}/)?{kod}-(\d+)\b", h)
        if m:
            out.add(int(m.group(1)) - 1); continue
        m = re.match(r"maddeler\[(\d+)\]", h)
        if m:
            out.add(int(m.group(1))); continue
        return None
    return out


def duzeltme_notu(meta: dict) -> str:
    return (f"Hatalardaki `{meta['kod']}-02` biçimli kimlik M2 ögesidir (maddeler[1] = M2). Çıkmış (Q) ve satır (L) "
            "etiketleri aynı kalır.")


def duzeltme_kisiti(onceki: dict, yeni: dict) -> list[str]:
    """Denetim düzeltmesinde (yonlendir.bulgu_duzelt) yapı sabit kalır: madde sayısı, madde başına örnek soru sayısı ve puan.
    Ders birleştirmesi madde kimliklerini ve doğru şık harflerini SIRAYLA verir; yapı değişirse sonraki bütün soruların
    kimliği/harfi kayar ve çözücü kayıtları boşa yeniden üretilir (2026-10-24)."""
    e = []
    a, b = onceki.get("maddeler", []), yeni.get("maddeler", [])
    if len(a) != len(b):
        return [f"madde sayısı {len(b)} — düzeltmede {len(a)} kalmalı (yalnız bulguların gösterdiği içeriği düzelt)"]
    for i, (x, y) in enumerate(zip(a, b), 1):
        if len(x.get("ornek") or []) != len(y.get("ornek") or []):
            e.append(f"{x['id']}: örnek soru sayısı {len(y.get('ornek') or [])} — düzeltmede {len(x.get('ornek') or [])} kalmalı")
        if x.get("puan") != y.get("puan"):
            e.append(f"{x['id']}: puan {y.get('puan')} — düzeltmede {x.get('puan')} kalmalı")
    return e
