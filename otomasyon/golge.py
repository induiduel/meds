#!/usr/bin/env python3
"""R3 gölge kipi — ücretsiz modellerin görevlere HAZIR olup olmadığını ölçer (ICERIK_MOTORU_V3.md §10 R3).

Yayına dokunmaz. Her gece küçük, belirlenimci örneklemlerle (Kurul 1 verisi SALT OKUNUR; çıktılar `--cikis` ile
meds_temp/golge/cikti/'ya) görevleri Ü katmanında (Claude yok) koşar ve kaydeder:
  - kapı: ilk turda / düzeltmeyle geçti mi, tur sayısı, model, süre;
  - bağımsız denetim (yazarın ailesi hariç, Ü): gecer / duzelt;
  - referans uyumu (varsa): kanit_bagla → örnek sorunun elle konan kanıt sayfası (±1 sayfa ya da cevap o sayfada da geçiyor);
    som_sec → elle doğrulanmış sabit sorgular.
Özet `meds_temp/golge/ozet.json` görev başına son 30 günü toplar; `gorevler.json` → `gecis_esigi` aşılınca görev
"geçişe hazır" görünür (öneri; Claude zincirinin görevi devretmesi kullanıcı kararıdır — R4).
Çağrı sayısı tavanlı (`--butce`, varsayılan 24/gece); kota bitince durur, sessizce boş geçmez (çıkış 4).

Kullanım: python3 meds/otomasyon/golge.py [--butce 24] [--gorev kanit_bagla] [--ozet]
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm import cekirdek as c  # noqa: E402
from llm import yonlendir  # noqa: E402

GOLGE = c.TEMP / "golge"
CIKIS = GOLGE / "cikti"
SOM_REFERANS = [  # k1-03 s16 (Robbins Şekil 1.21) — gözle doğrulandı 2026-10-23
    ("k1-03-p16", "hipertrofiye uğramış adapte miyosit", "1"),
    ("k1-03-p16", "geri dönüşümlü hasarlı miyosit", "3"),
    ("k1-03-p16", "hücre ölümü, ölü miyokard hücresi", "6"),
    ("k1-03-p16", "nekroz gösteren kalp enine kesiti", "5"),
    ("k1-03-p16", "normal miyosit", "2"),
]
VARSAYILAN_ESIK = {"en_az_ornek": 30, "kapi": 0.95, "denetim": 0.90, "referans": 0.95}


def _gun() -> str:
    return time.strftime("%Y-%m-%d")


def _kaydet(kayit: dict):
    GOLGE.mkdir(parents=True, exist_ok=True)
    with open(GOLGE / f"{_gun()}.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"zaman": c.simdi(), **kayit}, ensure_ascii=False) + "\n")


def _isle(gorev: str, hedef: str, ayar: dict | None, denetle: bool) -> dict:
    """Bir gölge işi: hazırla → Ü ile çalıştır → (denetim) — çıktı yalnız meds_temp'e."""
    m = c.modul(gorev)
    t0 = time.time()
    try:
        is_id = c.is_ac(gorev, hedef, m.hazirla(hedef, ayar or {}))
    except SystemExit as e:
        return {"gorev": gorev, "hedef": hedef, "durum": "hazirlanamadi", "neden": str(e)[:200]}
    onceki = len(list(c.is_klasoru(is_id).glob("cevap_*.txt")))
    os.environ["MEDS_AJAN_CLAUDE"] = "0"          # gölge = Claude dışı yol (ajan CLI'leri, 2026-10-24)
    kod = yonlendir.calistir(is_id, "A", None, log=lambda *_: None)
    d = c.durum(is_id)
    r = {"gorev": gorev, "hedef": hedef, "is_id": is_id, "kod": kod, "kapi": kod == 0, "model": d.get("model"),
         "tur": len(list(c.is_klasoru(is_id).glob("cevap_*.txt"))) - onceki, "kismi": d.get("kismi"),
         "sure_sn": round(time.time() - t0, 1)}
    if kod == 0 and denetle:
        try:
            den = c.is_ac("denetim", is_id, c.modul("denetim").hazirla(is_id, {}))
            if yonlendir.calistir(den, "A", None, log=lambda *_: None) == 0:
                cik = c.oku(c.is_klasoru(den) / "cikti.json") or {}
                r["denetim"] = cik.get("karar")
                r["denetim_bulgu"] = len(cik.get("bulgular", []))
                r["denetim_turler"] = sorted({b["tur"] for b in cik.get("bulgular", [])})
                engel = set(c.kayit(gorev).get("denetim_engelleyen") or [])
                r["denetim_engel"] = bool(set(r["denetim_turler"]) & engel) if engel else r["denetim"] == "duzelt"
        except SystemExit:
            pass
    return r


def ornek_kanit(n_parti: int, rng: random.Random) -> list[tuple[str, dict]]:
    """Kanıt bağlama: örnek sorusu (elle kanıt sayfası) bekleyen Kurul 1 derslerinden rastgele partiler."""
    sys.path.insert(0, str(c.KOK / "scripts" / "kroki"))
    from llm.gorevler import kanit_bagla as KB
    dersler = sorted(p.parent.parent.name for p in (c.DB2 / "ders_bilgi").glob("k1-*/l1/kanit.json"))
    rng.shuffle(dersler)
    out = []
    for ders in dersler:
        b = KB.bekleyenler(ders)
        ornekli = [i for i, sid in enumerate(b) if re.fullmatch(rf"{ders}-.+-k\d+-q\d+", sid)]   # örnek soru kimliği
        if ornekli:
            out.append((f"{ders}/parti/{ornekli[0] // KB.PARTI}", {}))
        if len(out) >= n_parti:
            break
    return out


def kanit_referans(r: dict) -> dict:
    """Modelin seçtiği bölge(ler) ↔ örnek sorunun elle konan kanıt sayfası."""
    sys.path.insert(0, str(c.KOK / "scripts" / "cikmis_dizin"))
    import kanit as K
    from ortak import DEPO, oku
    _, pj = c.paket(r["is_id"])
    cik = c.oku(c.is_klasoru(r["is_id"]) / "cikti.json") or {}
    meta = pj["meta"]
    ders = meta["ders_id"]
    gercek = {q["id"]: q for q in K.ornek_sorulari(ders) if q.get("_gercek_sayfa")}
    B = K.birimler(oku(DEPO / ders / "l0" / "sayfalar.json"))
    uy = top = yok = 0
    for Q, k in (cik.get("sorular") or {}).items():
        ms = meta["sorular"][Q]
        q = gercek.get(ms["id"])
        if not q:
            continue
        if k["yok"] or not k["dogru"]:
            yok += 1; continue
        top += 1
        s = k["dogru"][0]
        sayfa = int(meta["_esleme"][s].split("|")[1])
        g = q["_gercek_sayfa"]
        ok = abs(sayfa - g) <= 1 or (K.sozcuksel(q["dogru_metin"], ms["birim"][s]) and
                                      any(K.sozcuksel(q["dogru_metin"], u["metin"]) for u in B if u["sayfa"] == g))
        uy += ok
    return {"referans_n": top, "referans_uyum": uy, "referans_yok": yok}


def calistir(butce: int, yalniz: str | None, n_kanit: int = 4) -> int:
    rng = random.Random(_gun())
    plan: list[tuple[str, str, dict, bool]] = []
    if yalniz in (None, "kanit_bagla"):
        plan += [("kanit_bagla", h, a, False) for h, a in ornek_kanit(n_kanit, rng)]
    if yalniz in (None, "som_sec"):
        plan += [("som_sec", h, {"sorgu": s}, False) for h, s, _ in SOM_REFERANS]
    if yalniz in (None, "sik_aciklama"):
        ornek = sorted((c.KOK / "src" / "data" / "ornek_sorular" / "k1").glob("k1-*.json"))
        for p in rng.sample(ornek, min(3, len(ornek))):
            sor = [q["id"] for kz in (c.oku(p, {}) or {}).get("kazanimlar", []) for q in kz.get("sorular", [])]
            if sor:
                plan.append(("sik_aciklama", rng.choice(sor), {}, True))
    if yalniz in (None, "parca_sorusu"):
        v2 = sorted((c.KOK / "data" / "sesli_anlatim" / "v2").glob("k1-*.json"))
        for p in rng.sample(v2, min(2, len(v2))):
            b = (c.oku(p, {}) or {}).get("bolumler") or []
            if len(b) > 2:
                plan.append(("parca_sorusu", rng.choice(b[1:])["id"], {}, True))
    harcanan = 0
    for gorev, hedef, ayar, denetle in plan:
        if harcanan >= butce:
            print(f"gölge: bütçe ({butce}) doldu"); break
        r = _isle(gorev, hedef, ayar, denetle)
        harcanan += r.get("tur", 0) + (1 if "denetim" in r else 0)
        if gorev == "kanit_bagla" and r.get("kapi"):
            r.update(kanit_referans(r))
        if gorev == "som_sec" and r.get("kapi"):
            cik = c.oku(c.is_klasoru(r["is_id"]) / "cikti.json") or {}
            beklenen = next(b for h, s, b in SOM_REFERANS if h == hedef and s == ayar["sorgu"])
            r.update({"referans_n": 1, "referans_uyum": int(cik.get("numara") == beklenen),
                      "referans_yok": int(cik.get("numara") is None)})
        _kaydet(r)
        print(f"  {gorev:13} {hedef:42} kapı={'✓' if r.get('kapi') else '✗'} tur={r.get('tur')} "
              f"{('denetim=' + str(r.get('denetim'))) if 'denetim' in r else ''} "
              f"{('referans=' + str(r.get('referans_uyum')) + '/' + str(r.get('referans_n'))) if 'referans_n' in r else ''}")
    ozet()
    return 0 if harcanan else 5


def ozet(gun: int = 30) -> dict:
    sinir = time.time() - gun * 86400
    toplam: dict[str, dict] = {}
    for p in sorted(GOLGE.glob("20*.jsonl")):
        for satir in p.read_text(encoding="utf-8").splitlines():
            r = json.loads(satir)
            if time.mktime(time.strptime(r["zaman"][:19], "%Y-%m-%dT%H:%M:%S")) < sinir:
                continue
            t = toplam.setdefault(r["gorev"], {"n": 0, "kapi": 0, "tur": 0, "denetim_n": 0, "denetim_gecer": 0,
                                               "referans_n": 0, "referans_uyum": 0, "referans_yok": 0, "modeller": {}})
            t["n"] += 1
            t["kapi"] += bool(r.get("kapi"))
            t["tur"] += r.get("tur", 0)
            if "denetim" in r:
                # engelleyici bulgu yoksa geçer sayılır (ör. şık açıklamasında kaynak_dışı kimlik cümlesi engel değil)
                t["denetim_n"] += 1; t["denetim_gecer"] += not r.get("denetim_engel", r["denetim"] == "duzelt")
            for k in ("referans_n", "referans_uyum", "referans_yok"):
                t[k] += r.get(k, 0)
            if r.get("model"):
                t["modeller"][r["model"]] = t["modeller"].get(r["model"], 0) + 1
    defter = c.defter()
    for g, t in toplam.items():
        esik = {**VARSAYILAN_ESIK, **(defter.get(g, {}).get("gecis_esigi") or {})}
        t["kapi_orani"] = round(t["kapi"] / max(t["n"], 1), 3)
        t["denetim_orani"] = round(t["denetim_gecer"] / t["denetim_n"], 3) if t["denetim_n"] else None
        t["referans_orani"] = round(t["referans_uyum"] / t["referans_n"], 3) if t["referans_n"] else None
        kosul = [t["n"] >= esik["en_az_ornek"], t["kapi_orani"] >= esik["kapi"],
                 t["denetim_orani"] is None or t["denetim_orani"] >= esik["denetim"],
                 t["referans_orani"] is None or t["referans_orani"] >= esik["referans"]]
        t["gecise_hazir"] = all(kosul)
        t["esik"] = esik
    c.yaz(GOLGE / "ozet.json", {"zaman": c.simdi(), "gun": gun, "gorevler": toplam})
    for g, t in sorted(toplam.items()):
        print(f"ÖZET {g:13} n={t['n']:3} kapı %{100 * t['kapi_orani']:.0f}"
              + (f" denetim %{100 * t['denetim_orani']:.0f}" if t["denetim_orani"] is not None else "")
              + (f" referans %{100 * t['referans_orani']:.0f} (yok {t['referans_yok']})" if t["referans_orani"] is not None else "")
              + f" → {'GEÇİŞE HAZIR' if t['gecise_hazir'] else 'ölçüm sürüyor'}")
    return toplam


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--butce", type=int, default=24)
    ap.add_argument("--gorev")
    ap.add_argument("--ozet", action="store_true")
    ap.add_argument("--n-kanit", type=int, default=4, help="kanit_bagla örneklemi (parti sayısı)")
    a = ap.parse_args()
    if a.ozet:
        ozet(); return 0
    return calistir(a.butce, a.gorev, a.n_kanit)


if __name__ == "__main__":
    sys.exit(main())
