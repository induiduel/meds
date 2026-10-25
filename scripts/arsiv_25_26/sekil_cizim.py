#!/usr/bin/env python3
"""Arşiv derslerinde şekil/tablo anlatan cümlelere görselin ÜSTÜNDE çizim (kontur, ok, dallı ok, eğri) üretir (H59).

Lazer işareti (isaret/<key>.json) resim ya da tablo olan cümle = şekil cümlesi. Yalnız bu cümlelerin sayfaları için
TALIMAT_CIZIM.md paketi hazırlanır; her şekil cümlesi ★ ile işaretlenir ve görselde anlattığı yapıyı kontur/ok ile
göstermesi istenir (sınama dersleri k2-02 / k2-07 düzeyi). Eski adayların o sayfalardaki komutları yenileriyle
değişir; sonra arsiv_yayinla.cizim_dogrula_ve_yerlestir (kapı + yerleşim) ve .medspak cizim tablosu yenilenir.

Kullanım (.venv-ocr):
  sekil_cizim.py hazirla <key>...      # meds_database_25_26/taslak/<key>/cizim_sekil/partiNN/sayfalar.md
  sekil_cizim.py calistir <key>... [--paralel 4]   # claude -p, parti başına cizim.json (var olan atlanır)
  sekil_cizim.py birlestir <key>...    # cizim_aday.json + doğrulama + .medspak
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / "scripts" / "sesli_anlatim"))
sys.path.insert(0, str(MEDS / "scripts" / "cizim"))
sys.path.insert(0, str(MEDS / "scripts" / "arsiv_25_26"))
import pymupdf  # noqa: E402
import arsiv_yayinla as AY  # noqa: E402
import cizim_uret as CU  # noqa: E402
import pdf_isaret as PI  # noqa: E402

SA_KOK = AY.SA_KOK
DB = AY.DB_25_26
PARTI = 5
ISTEM = (
    f"{CU.TALIMAT} talimatını uygula. Çalışma dizinindeki sayfalar.md'yi oku; listelenen her sayfa görüntüsünü (PNG) Read "
    "aracıyla aç ve dikkatle incele.\n\n"
    "BU İŞİN ODAĞI: ★ ile işaretli cümleler slayttaki bir görseli (resim, şema, radyoloji, fotoğraf, tablo) anlatıyor. "
    "Her ★ cümle için görselin üstünde, cümlenin anlattığı yapıyı gösteren EN AZ BİR çizim yaz:\n"
    "- `kontur`: anlatılan yapı/lezyon/bölge/tablo satırı-sütunu; 5–20 nokta, görüntüdeki gerçek kenarın üstünde, "
    "işaretli R# (ya da T#) kutusunun İÇİNDE. Tüm resmi çevreleme; yalnız anlatılan parçayı dolan. Tablo anlatılıyorsa "
    "anlatılan satır ya da hücre grubunu dolan.\n"
    "- `akis`: iki yapı arasındaki ilişki/yol (ör. kitle → kanal basısı); görseldeki mevcut oku kopyalama.\n"
    "- birden çok yere giden ilişki için `dallar`; grafikte `egri_faz`.\n"
    "- `bas`/`son`: yapının adının söylendiği kelime numaraları; çizim tam o anda başlar.\n"
    "- Etiket kısa (≤5 kelime) ve cümlede geçen terim. Cümle başına en çok 2, sayfa başına en çok 8 çizim.\n"
    "- Bu sayfalarda `sema` (panel) YAZMA. ★ olmayan cümleler için çizim zorunlu değil; yalnız gerçekten görseli "
    "anlatıyorsa yaz.\n"
    "- Slayt şablonu, logo, kapak deseni, yazının arkasındaki kart görseli resim değildir: bunlara çizim yapma.\n"
    "- Görselde cümlenin anlattığı yapı gerçekten seçilemiyorsa o ★ cümleyi atla (uydurma yok) ve "
    "`atlanan`: [{\"cumle\": ..., \"neden\": ...}] listesine yaz.\n"
    "Çıktıyı `cizim.json` dosyasına `{\"komutlar\": [...], \"atlanan\": [...]}` olarak kaydet. Bitince: BİTTİ."
)


def ders(key: str):
    taslak = DB / "taslak" / key
    baglam = json.loads((taslak / "baglam.json").read_text(encoding="utf-8"))
    pdf_yol = AY.ROOT / baglam["pdf_yolu"]
    pars = AY.metin_paragraflari((SA_KOK / "metin" / f"{key}.md").read_text(encoding="utf-8"))
    isr = json.loads((SA_KOK / "isaret" / f"{key}.json").read_text(encoding="utf-8"))["c"]
    return taslak, pdf_yol, pars, isr


def cumleler(pars: list[dict]) -> dict[str, str]:
    C = {}
    for pi, p in enumerate(pars):
        m, a = p["t"], 0
        for ci, e in enumerate(PI.cumle_sonlari(m)):
            C[f"P{pi}.C{ci}"] = m[a:e].strip()
            a = e
    return C


def hazirla(key: str) -> int:
    taslak, pdf_yol, pars, isr = ders(key)
    C = cumleler(pars)
    sayfa_cumle: dict[int, list[tuple[str, bool]]] = {}
    for pn, l in isr.items():
        for ci, i in enumerate(l):
            if i and i.get("s"):
                sayfa_cumle.setdefault(int(i["s"]), []).append((f"P{pn}.C{ci}", i["t"] in ("resim", "tablo")))
    sayfalar = sorted(s for s, cs in sayfa_cumle.items() if any(y for _, y in cs))
    belge = pymupdf.open(pdf_yol)
    dok = taslak / "cizim_dok"
    CU.dok_uret(belge, dok, force=True)  # tekil R# + T# kutularıyla yeniden
    W = taslak / "cizim_sekil"
    for i in range(0, len(sayfalar), PARTI):
        d = W / f"parti{i // PARTI:02d}"
        d.mkdir(parents=True, exist_ok=True)
        satir = ["# Bu partinin sayfaları (★ = görseli anlatan cümle)", ""]
        for s in sayfalar[i:i + PARTI]:
            satir.append(f"## Sayfa {s} — görüntü: {dok / f's{s:02d}.png'}")
            txt = dok / f"s{s:02d}.txt"
            satir += [x for x in txt.read_text(encoding="utf-8").splitlines() if x.startswith(("R", "T", "M"))][:40]
            ao, ae = CU.adaylar(belge[s - 1])
            for x in ao:
                satir.append(f"Aday ok {x['id']} (PDF çiziminden, kesin): kuyruk {x['a']} → uç {x['b']} ({x['iliski']})")
            for x in ae:
                satir.append(f"Aday eğri {x['id']}: {len(x['nokta'])} nokta, fazlar "
                             + ", ".join(f"{f['faz']} {f['aralik']}" for f in x["fazlar"]))
            for cid, yildiz in sayfa_cumle[s]:
                ks = C.get(cid, "").split()
                satir.append(("★ " if yildiz else "") + f"{cid}: " + " ".join(f"[{j}]{w}" for j, w in enumerate(ks)))
            satir.append("")
        (d / "sayfalar.md").write_text("\n".join(satir), encoding="utf-8")
        (d / "sablonlar.json").write_text(CU.SB.YOL.read_text(encoding="utf-8"), encoding="utf-8")
    W.mkdir(parents=True, exist_ok=True)
    (W / "sayfalar.json").write_text(json.dumps(sayfalar), encoding="utf-8")
    return len(sayfalar)


def calistir(keys: list[str], paralel: int, alt: str = "cizim_sekil", istem: str = ISTEM):
    isler = [d for k in keys for d in sorted((DB / "taslak" / k / alt).glob("parti*")) if not (d / "cizim.json").exists()]
    print(f"{len(isler)} parti", flush=True)

    def bir(d: Path):
        t = time.time()
        r = CU.claude(d, istem)
        return d, round((time.time() - t) / 60, 1), (d / "cizim.json").exists(), r.strip()[-60:]

    with ThreadPoolExecutor(max_workers=paralel) as ex:
        for d, dk, ok, r in ex.map(bir, isler):
            print(f"  {d.parent.parent.name}/{d.name}: {dk} dk {'tamam' if ok else 'ÇIKTI YOK ' + r}", flush=True)


def birlestir(key: str) -> dict:
    taslak, pdf_yol, pars, isr = ders(key)
    W = taslak / "cizim_sekil"
    sayfalar = set(json.loads((W / "sayfalar.json").read_text()))
    yeni, atlanan = [], []
    for f in sorted(W.glob("parti*/cizim.json")) + sorted(taslak.glob("cizim_sekil_onar*/parti*/cizim.json")):
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        yeni += [k for k in j.get("komutlar") or [] if k.get("tur") != "sema"]
        atlanan += j.get("atlanan") or []
    aday_yol = taslak / "cizim_aday.json"
    yedek = taslak / "cizim_aday.oncesi_h59.json"
    if aday_yol.exists() and not yedek.exists():
        yedek.write_text(aday_yol.read_text(encoding="utf-8"), encoding="utf-8")
    eski = json.loads(yedek.read_text(encoding="utf-8")).get("komutlar", []) if yedek.exists() else []
    # Eski adaylardan korunanlar: işlenmeyen sayfalar + elle/odaklı yazılmış görsel komutları (radyoloji lezyon odağı,
    # zenginlestir_tum_radyoloji.py). Şekil sayfasındaki eski panel/genel komutlar yenileriyle değişir.
    kalan = [k for k in eski if int(k.get("sayfa") or 0) not in sayfalar or (k.get("odak") and k.get("tur") != "sema")]
    odakli = {str(k.get("cumle")) for k in kalan if k.get("odak")}
    yeni = [k for k in yeni if str(k.get("cumle")) not in odakli]  # aynı cümlede odaklı çizim varsa o kalır
    aday_yol.write_text(json.dumps({"komutlar": kalan + yeni}, ensure_ascii=False, indent=1), encoding="utf-8")

    capa = json.loads((SA_KOK / "capa" / f"{key}.json").read_text(encoding="utf-8"))["p"]
    v2 = json.loads((SA_KOK / "v2" / f"{key}.json").read_text(encoding="utf-8"))
    metin_sha1 = hashlib.sha1("\n".join(p["t"] for p in pars).encode("utf-8")).hexdigest()
    cz = AY.cizim_dogrula_ve_yerlestir(taslak, key, pdf_yol, pars, capa, metin_sha1, v2)

    # .medspak cizim tablosu (cümle kimliği v2 sırasıyla, arsiv_yayinla.medspak_uret_yerel ile aynı)
    m = DB / "medspak" / "kurul2" / f"{key}.medspak"
    if m.exists():
        db = sqlite3.connect(m)
        db.execute("DELETE FROM cizim")
        for cid, pi, ci in db.execute("SELECT id, paragraf, sira FROM cumle").fetchall():
            for si, z in enumerate(((cz.get("p") or {}).get(str(pi)) or {}).get(str(ci)) or []):
                db.execute("INSERT INTO cizim VALUES (?,?,?)", (cid, si, json.dumps(z, ensure_ascii=False)))
        db.commit()
        db.close()

    sekil = [(pn, ci) for pn, l in isr.items() for ci, i in enumerate(l) if i and i["t"] in ("resim", "tablo")]
    P = cz.get("p") or {}
    cizimli = sum(1 for pn, ci in sekil if (P.get(pn) or {}).get(str(ci)))
    import cizim_kapisi as KAPI
    kapi_h, _ = KAPI.denetle(key, SA_KOK)
    return {"kapi_hata": len(kapi_h), "sekil": len(sekil), "cizimli": cizimli, "aday": len(yeni), "atlanan": len(atlanan),
            "gecti": cz["rapor"]["gecti"], "ret": cz["rapor"]["ret"]}


def onar_hazirla(key: str, alt: str = "cizim_sekil_onar") -> int:
    """Çizimsiz kalan ★ cümleler için ikinci tur: reddedilen komut ve kapının nedeni pakete yazılır."""
    taslak, pdf_yol, pars, isr = ders(key)
    C = cumleler(pars)
    cz = json.loads((SA_KOK / "cizim" / f"{key}.json").read_text(encoding="utf-8"))
    P = cz.get("p") or {}
    ret: dict[str, list] = {}
    for r in (cz.get("rapor") or {}).get("ret_ayrinti") or []:
        ret.setdefault(r["cumle"], []).append(r)
    eksik: dict[int, list[str]] = {}
    for pn, l in isr.items():
        for ci, i in enumerate(l):
            if i and i["t"] in ("resim", "tablo") and not (P.get(pn) or {}).get(str(ci)):
                eksik.setdefault(int(i["s"]), []).append(f"P{pn}.C{ci}")
    dok = taslak / "cizim_dok"
    W = taslak / alt
    sayfalar = sorted(eksik)
    for i in range(0, len(sayfalar), PARTI):
        d = W / f"parti{i // PARTI:02d}"
        d.mkdir(parents=True, exist_ok=True)
        satir = ["# İkinci tur: bu ★ cümlelerin çizimi yok ya da kapıdan geçmedi", ""]
        for s in sayfalar[i:i + PARTI]:
            satir.append(f"## Sayfa {s} — görüntü: {dok / f's{s:02d}.png'}")
            satir += [x for x in (dok / f"s{s:02d}.txt").read_text(encoding="utf-8").splitlines() if x.startswith(("R", "T", "M"))][:40]
            for cid in eksik[s]:
                ks = C.get(cid, "").split()
                satir.append(f"★ {cid}: " + " ".join(f"[{j}]{w}" for j, w in enumerate(ks)))
                for r in ret.get(cid, []):
                    satir.append(f"   önceki deneme REDDEDİLDİ ({r['tur']}): {r['neden']} — {json.dumps(r['komut'], ensure_ascii=False)}")
            satir.append("")
        (d / "sayfalar.md").write_text("\n".join(satir), encoding="utf-8")
        (d / "sablonlar.json").write_text(CU.SB.YOL.read_text(encoding="utf-8"), encoding="utf-8")
    W.mkdir(parents=True, exist_ok=True)
    (W / "sayfalar.json").write_text(json.dumps(sayfalar), encoding="utf-8")
    return sum(len(v) for v in eksik.values())


ONAR_EK = (
    "\n\nİKİNCİ TUR: Reddedilen denemelerin nedeni yazılı. Kapı kontur noktalarının en az %70'inin görüntüdeki gerçek "
    "koyu çizgi/kenar üstünde olmasını ister: noktaları yapının görünen sınır çizgisinin TAM üstüne koy (görüntüyü "
    "yakından incele; gerekirse az ama isabetli nokta). Sınırı çizgi olmayan bölge (yumuşak doku, tablo satırı, yazı "
    "bloğu) için kontur yerine `akis` kullan: `a` yapının yanındaki boş noktadan `b` yapının üstüne kısa ok + etiket. "
    "Mevcut çizimleri tekrar yazma; yalnız buradaki ★ cümleler."
)


SUS = ("süs", "kapak", "şablon", "arka plan", "logo", "dekoratif", "görselde yok", "görünmüyor", "başlık yazısı",
       "görselde karşılığı yok", "resim yok", "görüntü yok")


def sus_temizle(key: str) -> int:
    """Modelin görüntüye bakıp "bu görsel süs/şablon ya da cümlenin anlattığı şey görselde yok" diye atladığı cümlelerde
    yazarın şekil çapası yanlıştır: kaldırılır (lazer yazıya döner). El ile yazılmış (el: true) çapaya dokunulmaz."""
    import pdf_isaret as PI_
    taslak, pdf_yol, pars, isr = ders(key)
    ats = []
    for f in taslak.glob("cizim_sekil*/parti*/cizim.json"):
        try:
            ats += json.loads(f.read_text(encoding="utf-8")).get("atlanan") or []
        except Exception:
            pass
    hedef = {str(a.get("cumle")) for a in ats if any(w in str(a.get("neden", "")).lower() for w in SUS)}
    if not hedef:
        return 0
    capa = json.loads((SA_KOK / "capa" / f"{key}.json").read_text(encoding="utf-8"))
    v2 = json.loads((SA_KOK / "v2" / f"{key}.json").read_text(encoding="utf-8"))
    vs = {c["ses"].strip()[:40]: c for b in v2["bolumler"] for p in b["paragraflar"] for c in p["cumleler"]}
    n = 0
    for cid in hedef:
        try:
            pn, ci = int(cid[1:].split(".C")[0]), int(cid.split(".C")[1])
            cc = PI_.cumle_capalari(pars[pn]["t"], PI_.cumle_sonlari(pars[pn]["t"]), capa["p"][pn])[ci]
        except (ValueError, IndexError):
            continue
        for c in cc:
            if c.get("el") or not (c.get("sekil") or c.get("tablo")):
                continue
            c["sekil"] = None
            c.pop("tablo", None)
            v = vs.get(c["ses"][:40])
            if v and isinstance(v.get("slayt"), dict):
                v["slayt"]["sekil"] = None
                v["slayt"].pop("tablo", None)
            n += 1
    (SA_KOK / "capa" / f"{key}.json").write_text(json.dumps(capa, ensure_ascii=False, indent=1), encoding="utf-8")
    (SA_KOK / "v2" / f"{key}.json").write_text(json.dumps(v2, ensure_ascii=False, indent=1), encoding="utf-8")
    if (taslak / "konusma_capalari.json").exists():
        (taslak / "konusma_capalari.json").write_text(json.dumps(capa["p"], ensure_ascii=False, indent=1), encoding="utf-8")
    if (taslak / "konusma_v2.json").exists():
        (taslak / "konusma_v2.json").write_text(json.dumps(v2, ensure_ascii=False, indent=1), encoding="utf-8")
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("adim", choices=["hazirla", "calistir", "birlestir", "onar", "sus"])
    ap.add_argument("keys", nargs="+")
    ap.add_argument("--paralel", type=int, default=4)
    ap.add_argument("--tur", type=int, default=2, help="onar turu (2, 3, …): her tur ayrı dizin")
    a = ap.parse_args()
    if a.adim == "hazirla":
        for k in a.keys:
            print(k, hazirla(k), "sayfa", flush=True)
    elif a.adim == "calistir":
        calistir(a.keys, a.paralel)
    elif a.adim == "onar":  # hazırla + çalıştır (ikinci tur); sonra birlestir iki turu birlikte okur
        alt = "cizim_sekil_onar" if a.tur == 2 else f"cizim_sekil_onar{a.tur}"
        for k in a.keys:
            print(k, onar_hazirla(k, alt), "eksik ★", flush=True)
        calistir(a.keys, a.paralel, alt, ISTEM + ONAR_EK)
    elif a.adim == "sus":  # sonra: uygula_lazer_takip.py <key> (işaret) + birlestir
        for k in a.keys:
            print(k, sus_temizle(k), "şekil çapası kaldırıldı (süs/görselde yok)", flush=True)
    else:
        for k in a.keys:
            print(k, json.dumps(birlestir(k), ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
