"""Görev `cozucu_sorusu` — ders zincirinin `cozucu` adımı (TALIMAT_COZUCU.md) 4'lük soru partileriyle (R4).

Hedef: `<brans>:<kod>/parti/<n>` (W = meds_temp/spot_cozucu/<brans>; sınamada `--ayar w=…`). Soru kümesi resmî
doğrulayıcının beklediğiyle AYNI (`cozucu_dogrula.beklenen`: önem listesindeki örnekler + maddelere bağlı çıkmış
temsilciler), belirlenimci sırada 4'lük partiler. Soru, şıklar, anahtar, ref/tür/onem_id/zorluk/sınav BETİKLE kopyalanır
(model yazmaz → birebirlik garanti). Model yazar: kontrol (tamam | sorunlu + not), kök/şık okunuşu, ipucu, şık açıklamaları,
çözüm, sayfa. Dayanak: sorunun önem maddesi (bilgi + detay) + ilgili sayfaların metni.
Kapı: resmî `scripts/spot_cozucu/cozucu_dogrula.py` partiye uygulanır ("eksik soru" ders düzeyidir) — ses yazımı, ipucu
sızıntısı, şık açıklama standardı, Türkçe üslup dahil. Kısmi kabul: hatalı sorular (≤ yarısı) düşer, sonraki partiyle yeniden.
`sorunlu` soru birleştirmede çıkarılır (örnek → önem listesinden de; çıkmış → `elenen_cikmis`), birleştirici önem
listesini yeniden doğrular.
Uygulama: W/gorev/<kod>/cozucu_parti_<soru kimliklerinin özeti>.json; birleştirme `otomasyon/llm/spot_birlestir.py cozucu W kod`.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

from .. import cekirdek as c
from . import _spot

SES_ONAR = True   # ses alanlarında kısaltma/Roma rakamı okunuşu betikle (cekirdek.ses_onar)
OGE, OGE_ETIKET = ("sorular", "dict"), r"Q\d+"   # kısmi düzeltme: yalnız hatalı Q'lar (yonlendir.kismi_duzeltme)
KURALLAR = ["kaynak_sadakati", "cozucu_yazimi", "ses_yazimi", "sik_aciklama", "turkce_uslup", "cikti_disiplini"]
PARTI = 4


def _od():
    sys.path.insert(0, str(c.KOK / "scripts" / "spot_cozucu"))
    import cozucu_dogrula as CD
    return CD


def sorular(W: Path, kod: str) -> list[tuple[str, dict]]:
    return list(_od().beklenen(W, kod).items())


def bekleyen(W: Path, kod: str) -> list[tuple[str, dict]]:
    """Henüz kabul edilmemiş sorular (önceki partilerde düşenler dahil), belirlenimci sırada."""
    yapilan = set()
    for p in sorted((W / "gorev" / kod).glob("cozucu_parti_*.json")):
        yapilan |= {q["ref"] for q in (c.oku(p) or {}).get("sorular", [])}
    return [(r, b) for r, b in sorular(W, kod) if r not in yapilan]


def hazirla(hedef: str, ayar: dict | None = None) -> dict:
    W, kod, n = _spot.hedef_coz(hedef, ayar, "parti")
    if not (W / "onem" / f"{kod}.json").exists():
        raise SystemExit(f"{kod}: önce önem listesi (W/onem/{kod}.json)")
    liste = bekleyen(W, kod)
    parca = liste[n * PARTI:(n + 1) * PARTI]
    if not parca:
        raise SystemExit(f"{kod}: parti {n} boş ({len(liste)} bekleyen soru)")
    o = c.oku(W / "onem" / f"{kod}.json")
    M = {m["id"]: m for m in o["maddeler"]}
    S = _spot.sayfalar(W, kod)
    et = c.Etiketler()
    bloklar, meta_q = [], {}
    for ref, b in parca:
        Q = et.ekle("Q", ref)
        m = M.get(b["onem_id"], {})
        say = sorted({a["sayfa"] for a in m.get("alinti", [])} | set(next((q.get("sayfa", []) for q in m.get("ornek", [])
                                                                          if q["kok"] == b["soru"]), [])))[:3]
        dayanak = " ".join(" ".join(S.get(s, "").split()) for s in say)[:1800]
        bloklar.append("\n".join([
            f"### {Q} ({'çıkmış soru' if b['tur'] == 'cikmis' else 'örnek soru'})",
            f"Soru: {b['soru']}", *[f"{h}) {t}" for h, t in sorted(b["secenekler"].items())], f"Doğru: {b['dogru']}",
            f"Dayanak — önem maddesi: {m.get('bilgi', '')} {m.get('detay', '')}".strip(),
            f"Dayanak — sayfa {', '.join(map(str, say))} metni: {dayanak}"]))
        meta_q[Q] = {"ref": ref, "sayfa": say}
    ornek = {"sorular": {"Q1": {"kontrol": {"durum": "tamam", "not": ""}, "kok_ses": "…", "secenek_ses": {h: "…" for h in "ABCDE"},
                                "ipucu": {"metin": "…", "ses": "…"},
                                "siklar": {h: {"metin": "…", "ses": "…"} for h in "ABCDE"},
                                "cozum": {"metin": "…", "ses": "…"}, "sayfa": [3]}}}
    return {
        "amac": ("Aşağıdaki her soru için sesli soru çözücünün metinlerini yaz: soruyu denetle (kontrol), kökün ve şıkların okunuşunu, "
                 "tek cümlelik ipucunu, beş şıkkın açıklamasını ve çözümü; her alan `metin` (ekranda) ve `ses` (okunuş) çifti."),
        "kurallar": KURALLAR,
        "ek_kurallar": ["Soru, şıklar ve doğru cevap sabittir; çıktıya yazma.",
                        "`sayfa` sorunun bilgilerinin geçtiği sayfa numaraları (dayanaktaki sayfalardan)."],
        "girdi": "\n\n".join(bloklar),
        "cikti_bicimi": "Yalnız şu JSON (girdideki her Q için):\n" + json.dumps(ornek, ensure_ascii=False, indent=1),
        "denetim_listesi": ["her Q için kayıt", "ses alanlarında rakam/simge/büyük harfli kısaltma yok",
                            "ipucu cevabı sızdırmıyor", "şık açıklamaları 2–3 cümle, 18–60 kelime, ne / ne işe yarar / neden",
                            "doğru şıkkın açıklamasında 'doğru' sözcüğü var"],
        "esleme": et.esleme,
        "meta": {"w": str(W), "kod": kod, "parti": n, "q": meta_q, "kurul": None},
    }


def derle(cevap, esleme: dict, meta: dict):
    j = c.json_cikar(cevap)
    if not isinstance(j, dict) or not isinstance(j.get("sorular"), dict):
        return None, ["cevap JSON değil ya da 'sorular' nesnesi yok"]
    B = dict(sorular(Path(meta["w"]), meta["kod"]))
    out, e = [], []
    for Q, mq in meta["q"].items():
        r = j["sorular"].get(Q)
        if not isinstance(r, dict):
            e.append(f"{Q}: cevapta kayıt yok"); continue
        b = B.get(mq["ref"])
        if not b:
            e.append(f"{Q}: soru kümede yok (önem listesi değişti mi?)"); continue
        k = r.get("kontrol") or {}
        q = {"ref": mq["ref"], "tur": b["tur"], "onem_id": b["onem_id"],
             **({"zorluk": b.get("zorluk")} if b["tur"] == "ornek" else {"sinav": b.get("sinav")}),
             "kontrol": {"durum": "tamam"}, "soru": b["soru"], "secenekler": b["secenekler"], "dogru": b["dogru"],
             "kok_ses": str(r.get("kok_ses") or "").strip(),
             "secenek_ses": {str(h).upper()[:1]: str(v).strip() for h, v in (r.get("secenek_ses") or {}).items()},
             "ipucu": r.get("ipucu"), "siklar": {str(h).upper()[:1]: v for h, v in (r.get("siklar") or {}).items()},
             "cozum": r.get("cozum"), "sayfa": [int(x) for x in (r.get("sayfa") or mq["sayfa"]) if str(x).isdigit()],
             "_etiket": Q}
        if str(k.get("durum")) == "sorunlu":
            q["_sorunlu"] = str(k.get("not") or "").strip()
        out.append(q)
    return {"surum": 1, "kod": meta["kod"], "parti": meta["parti"], "sorular": out}, e


def resmi_kapi(qs: list[dict], W: Path, kod: str) -> list[str]:
    CD = _od()
    with tempfile.TemporaryDirectory(prefix="cozucu_kapi_") as t:
        T = Path(t)
        for alt, uz in (("pdf_metin", "md"), ("girdi", "json"), ("cikmis", "json"), ("onem", "json")):
            (T / alt).mkdir()
            if (W / alt / f"{kod}.{uz}").exists():
                (T / alt / f"{kod}.{uz}").symlink_to(W / alt / f"{kod}.{uz}")
        (T / "cozucu").mkdir()
        p = T / "cozucu" / f"{kod}.json"
        p.write_text(json.dumps({"kod": kod, "sorular": [{k: v for k, v in q.items() if not k.startswith("_")} for q in qs]},
                                ensure_ascii=False), encoding="utf-8")
        e, _, _ = CD.check(p)
    return [x for x in e if not x.startswith("eksik soru")]


def dogrula(cikti: dict, meta: dict) -> list[str]:
    W, kod = Path(meta["w"]), meta["kod"]
    tam = [q for q in cikti["sorular"] if "_sorunlu" not in q]
    e = []
    for q in cikti["sorular"]:
        if "_sorunlu" in q and len(q["_sorunlu"]) < 15:
            e.append(f"{q['_etiket']}: sorunlu denildi ama gerekçe yok (dayanak sayfasıyla açıkla)")
    if len(cikti["sorular"]) - len(tam) > max(1, len(cikti["sorular"]) // 2):
        e.append("partideki soruların yarısından çoğu 'sorunlu' — her soruyu ayrı denetle")
    etiket = {q["ref"]: q["_etiket"] for q in cikti["sorular"]}
    oncullu = {q["_etiket"] for q in tam if re.search(r"(?m)^\s*(I|II|III|IV|V)[.)]\s", q.get("soru") or "")}
    for x in resmi_kapi(tam, W, kod):
        ref = next((r for r in sorted(etiket, key=len, reverse=True) if x.startswith(r)), None)
        x = etiket[ref] + x[len(ref):] if ref else x              # "o:e07-03:1.ipucu: …" → "Q2.ipucu: …"
        Q = re.match(r"(Q\d+)", x)
        if "kökle uzunluk uyumsuz" in x and Q and Q.group(1) in oncullu:
            x += (" — öncüllü soru: kok_ses kök cümlesini VE öncüllerin hepsini okur (\"birinci öncül, …; ikinci öncül, …\"), "
                  "sonra soru cümlesi")
        e.append(x)
    return e


def kismi_kabul(cikti: dict | None, hatalar: list[str], meta: dict):
    if not cikti:
        return None, hatalar, []
    dusen = set()
    for h in hatalar:
        m = re.match(r"(Q\d+)\b", h)
        if not m:
            return None, hatalar, []
        dusen.add(m.group(1))
    kalan = [q for q in cikti["sorular"] if q["_etiket"] not in dusen]
    if not kalan:
        return None, hatalar, sorted(dusen)
    c2 = {**cikti, "sorular": kalan}
    return c2, dogrula(c2, meta), sorted(dusen)


def tersine(cikti: dict, esleme: dict, meta: dict) -> str:
    out = {}
    for q in cikti["sorular"]:
        out[q["_etiket"]] = {"kontrol": {"durum": "sorunlu" if "_sorunlu" in q else "tamam", "not": q.get("_sorunlu", "")},
                             **{k: q[k] for k in ("kok_ses", "secenek_ses", "ipucu", "siklar", "cozum", "sayfa")}}
    return json.dumps({"sorular": out}, ensure_ascii=False, indent=1)


ozet = tersine


def uygula(cikti: dict, meta: dict, cikis: Path | None = None, k1_izin: bool = False) -> Path:
    W = Path(cikis) if cikis else Path(meta["w"])
    if cikis is None and "/spot_cozucu/" in str(W) and not k1_izin and re.match(r"^[a-z]", meta["kod"]):
        raise SystemExit("Kurul 1 branş klasörüne yazım yok: --cikis ile sınama klasörü ver ya da --k1-izin")
    d = W / "gorev" / meta["kod"]
    # dosya adı partinin soru kimliklerinden: aynı parti yeniden uygulanırsa (önbellek, denetim düzeltmesi) aynı dosyanın
    # üzerine yazılır, çoğalmaz (2026-10-24; eskiden her uygulama yeni numaralı dosya açıyordu)
    refs = {q["ref"] for q in cikti["sorular"]}
    p = d / f"cozucu_parti_{c.sha(','.join(sorted(refs)), 10)}.json"
    # aynı soruları taşıyan eski parti dosyalarından o sorular çıkar (yeni kayıt geçerlidir; boşalan dosya silinir)
    for f in d.glob("cozucu_parti_*.json") if d.exists() else []:
        if f == p:
            continue
        eski = c.oku(f) or {}
        kalan = [q for q in eski.get("sorular", []) if q["ref"] not in refs]
        if len(kalan) != len(eski.get("sorular", [])):
            c.yaz(f, {**eski, "sorular": kalan}) if kalan else f.unlink()
    c.yaz(p, cikti)
    return p


def eskiyen(W: Path, kod: str) -> set[str]:
    """Önem listesindeki güncel örnek soruyla (kök, şıklar, doğru) uyuşmayan ya da artık önemde olmayan çözücü kayıtları.
    Önem denetimle düzeltilince çözücü açıklaması eski soruya göre kalabilir (2026-10-24 prova) → yeniden üretilmeli."""
    o = c.oku(W / "onem" / f"{kod}.json") or {}
    on = {f"o:{m['id']}:{i}": q for m in o.get("maddeler", []) for i, q in enumerate(m.get("ornek") or [], 1)}
    out = set()
    for p in (W / "gorev" / kod).glob("cozucu_parti_*.json"):
        for q in (c.oku(p) or {}).get("sorular", []):
            if q["ref"].startswith("o:"):
                x = on.get(q["ref"])
                if not x or (x.get("kok"), x.get("secenekler"), x.get("dogru")) != (q.get("soru"), q.get("secenekler"), q.get("dogru")):
                    out.add(q["ref"])
    return out


def eskiyenleri_dusur(W: Path, kod: str, refs: set[str]) -> int:
    """Eskiyen kayıtlar parti dosyalarından (ve sahibi işlerin çıktısından) çıkar; boşalan dosya silinir. → düşen sayısı."""
    import json as _j
    n = 0
    for f in (W / "gorev" / kod).glob("cozucu_parti_*.json"):
        pj_ = c.oku(f) or {}
        kalan = [q for q in pj_.get("sorular", []) if q["ref"] not in refs]
        if len(kalan) == len(pj_.get("sorular", [])):
            continue
        n += len(pj_["sorular"]) - len(kalan)
        defter = c.oku(W / "gorev" / kod / "isler.json", {}) or {}
        for i, v in defter.items():
            if v.get("dosya") == str(f):
                ck = c.is_klasoru(i) / "cikti.json"
                ci = c.oku(ck) or {}
                c.yaz(ck, {**ci, "sorular": [q for q in ci.get("sorular", []) if q["ref"] not in refs]})
        if kalan:
            c.yaz(f, {**pj_, "sorular": kalan})
        else:
            f.unlink()
    return n


def birlestir(W: Path, kod: str, log=print) -> int:
    """Partiler → W/cozucu/<kod>.json. Sorunlu sorular önem listesinden de çıkarılır (örnek → silinir; çıkmış → elenen)."""
    CD = _od()
    eski = eskiyen(W, kod)
    if eski:
        log(f"  HATA {kod}: {len(eski)} çözücü kaydı önem listesindeki güncel soruyla uyuşmuyor ({sorted(eski)[:4]}) — "
            "eskiyenleri_dusur + çözücü adımı"); return 1
    eksik = bekleyen(W, kod)
    if eksik:
        log(f"{kod}: {len(eksik)} soru henüz üretilmedi ({[r for r, _ in eksik][:4]})"); return 2
    tum = [q for p in sorted((W / "gorev" / kod).glob("cozucu_parti_*.json")) for q in (c.oku(p) or {}).get("sorular", [])]
    sorunlu = {q["ref"]: q["_sorunlu"] for q in tum if "_sorunlu" in q}
    if sorunlu:
        o = c.oku(W / "onem" / f"{kod}.json")
        for m in o["maddeler"]:
            m["ornek"] = [x for i, x in enumerate(m.get("ornek") or [], 1) if f"o:{m['id']}:{i}" not in sorunlu]
            for cid in list(m.get("cikmis") or []):
                if f"c:{cid}" in sorunlu:
                    m["cikmis"].remove(cid)
                    if not any(cid in mm.get("cikmis", []) for mm in o["maddeler"]):
                        o.setdefault("elenen_cikmis", []).append(
                            {"id": cid, "neden": "anahtar_celiskili" if "anahtar" in sorunlu[f"c:{cid}"].lower() else "belirsiz",
                             "not": sorunlu[f"c:{cid}"][:300]})
        c.yaz(W / "onem" / f"{kod}.json", o)
        log(f"{kod}: {len(sorunlu)} sorunlu soru önem listesinden çıkarıldı — örnek ref'leri yeniden numaralandı, çözücü yeniden kurulmalı")
        # örnek ref numaraları kaydı: çıkarılan örnekten sonraki örneklerin ref'i değişir → bu partiler yeniden eşlenir
        B = CD.beklenen(W, kod)
        eski_soru = {(q["soru"], tuple(sorted(q["secenekler"].items()))): q for q in tum if "_sorunlu" not in q}
        tum = []
        for ref, b in B.items():
            q = eski_soru.get((b["soru"], tuple(sorted(b["secenekler"].items()))))
            if q:
                tum.append({**q, "ref": ref, "onem_id": b["onem_id"]})
    out = {"kod": kod, "sorular": [{k: v for k, v in q.items() if not k.startswith("_")} for q in tum
                                   if "_sorunlu" not in q], "_kaynak": {"yontem": "gorev"}}
    with tempfile.TemporaryDirectory(prefix="cozucu_birlestir_") as t:
        T = Path(t)
        for alt, uz in (("pdf_metin", "md"), ("girdi", "json"), ("cikmis", "json"), ("onem", "json")):
            (T / alt).mkdir()
            if (W / alt / f"{kod}.{uz}").exists():
                (T / alt / f"{kod}.{uz}").symlink_to(W / alt / f"{kod}.{uz}")
        (T / "cozucu").mkdir()
        (T / "cozucu" / f"{kod}.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
        e, u, n = CD.check(T / "cozucu" / f"{kod}.json")
    for x in e:
        log(f"  HATA {x}")
    log(f"{kod}: çözücü {n} soru · {len(e)} HATA · {len(u)} UYARI")
    if e:
        return 1
    c.yaz(W / "cozucu" / f"{kod}.json", out)
    return 0


def sinama_ornekleri(meta: dict) -> tuple[dict, list[dict]]:
    """Öz-sınama: sınama verisindeki altın çözücüden (resmî kapıdan geçmiş) bu partinin iyi cevabı + bilinen kötüler."""
    altin = {q["ref"]: q for q in (c.oku(Path(meta["w"]) / "altin" / f"cozucu_{meta['kod']}.json") or {}).get("sorular", [])}
    iyi = {"sorular": {Q: {"kontrol": {"durum": "tamam", "not": ""},
                           **{k: altin[mq["ref"]][k] for k in ("kok_ses", "secenek_ses", "ipucu", "siklar", "cozum", "sayfa")}}
                       for Q, mq in meta["q"].items()}}
    Q1 = next(iter(meta["q"]))
    kotu = [{"ad": "geçiştirici şık", "degistir": [[["sorular", Q1, "siklar", "A", "metin"], "Bu sorunun cevabı değil."]],
             "beklenen": "geçiştirici"},
            {"ad": "seste rakam", "degistir": [[["sorular", Q1, "cozum", "ses"], "Sifiliz 3 hafta sonra şankr ile başlar ve çoğu zaman ağrısızdır."]],
             "beklenen": "ses yasak karakter"},
            {"ad": "eksik soru kaydı", "degistir": [[["sorular"], {}]], "beklenen": "cevapta kayıt yok"}]
    return iyi, kotu
