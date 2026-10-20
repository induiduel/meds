#!/usr/bin/env python3
"""Ders bilgi deposu — her PDF BİR KEZ okunur, sonraki her ürün buradan beslenir (kullanıcı kararı 2026-10-20).

PDF yalnız ders işçisinde (`cikar.py`) ve yalnız PDF karması değişince okunur; çıkan her şey yayımlanan taslak klasöründe
(`meds_database_v2/ders_isci/yayinlanan/<is_id>/`) ve ders zincirinin branş klasöründe durur. Bu modül bunları ders
kimliğiyle tek yerden bulur ve **ders özeti** (`ozet.md`) derler: yeni bir ürün (kurul kampı, Check Up, ileride başka
sayfalar) PDF'i yeniden okumaz, bu özeti ve gerektiğinde depodaki dosyaları kullanır.

Depo: meds_database_v2/ders_bilgi/<ders kimliği>/
  manifest.json  {ders_id, kod, kurul, brans, konu, pdf, pdf_sha, kaynak_dizin, zincir_dizin, dosyalar{…}, ozet_sha, guncellendi}
  ozet.md        bilgi paketi maddeleri (sayfalı) + önem maddeleri (puanlı, çıkmış bağlı) + tablolar + hoca vurgusu +
                 görsel sayfa listesi + çıkmış soru kökleri/cevapları — her satır kaynak sayfasını taşır (kod:sayfa)
Yeniden üretim yalnız girdilerin karması değişince (aynı girdi → aynı özet; boşuna iş yok).

  bilgi_deposu.py --kurul 2 [--ders k2-07] [--zorla]     depoyu kur/güncelle
  bilgi_deposu.py --liste [--kurul 2]                   hangi dersin deposu hazır
Python: from bilgi_deposu import ozet_yolu, manifest
"""
import argparse, datetime as dt, hashlib, json, re, subprocess, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]; KOK = MEDS.parent
DEPO = KOK / "meds_database_v2/ders_bilgi"
YAYIN = KOK / "meds_database_v2/ders_isci/yayinlanan"
SPOT = KOK / "meds_temp/spot_cozucu"


def _oku(p, v=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return v


def _sha(*yollar):
    h = hashlib.sha256()
    for y in yollar:
        y = Path(y)
        if y.is_file():
            h.update(y.name.encode()); h.update(y.read_bytes())
    return h.hexdigest()[:16]


def yayin_kaydi():
    """Yayımlanmış dersler (Oracle asıl kayıt; okunamazsa cihaz kopyası)."""
    try:
        r = subprocess.run(["ssh", "-o", "ConnectTimeout=15", "-o", "BatchMode=yes", "medsor-oracle",
                            "cat /home/ubuntu/medsor/ders_isci/yayin_kaydi.json"], capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and r.stdout.strip().startswith("["):
            return json.loads(r.stdout)
    except subprocess.TimeoutExpired:
        pass
    return _oku(MEDS / "scripts/ders_isci/yayin_kaydi.json", []) or []


def _branslar():
    return {b["ad"]: b["slug"] for b in _oku(MEDS / "src/data/dersler/branslar.json", {}).get("branslar", [])}


def ozet_derle(m: dict) -> str:
    """Depo dosyalarından ders özeti (yalnız depodaki veriden; PDF açılmaz)."""
    kd, kod = Path(m["kaynak_dizin"]), m["kod"]
    zd = Path(m["zincir_dizin"]) if m.get("zincir_dizin") else None
    s = [f"# {m['konu']} ({m['ders_id']} · {kod})", f"Branş: {m['brans']} · Kurul {m['kurul']} · PDF: {m.get('pdf') or '-'}", ""]
    paket = _oku(kd / "ders_paketi.json", {}) or {}
    if paket.get("bilgi_paketi"):
        s.append("## Bilgi paketi (ders PDF'inden atomik bilgiler)")
        for b in paket["bilgi_paketi"]:
            sy = (b.get("kanit") or {}).get("sayfa")
            s.append(f"- [{kod}:{sy}] {b.get('bilgi')}" + (f" — {b['sonuc']}" if b.get("sonuc") else ""))
        s.append("")
    onem = _oku(zd / "onem" / f"{kod}.json", {}) if zd else {}
    if onem and onem.get("maddeler"):
        s.append("## Sınav önemi (önem listesi; puan, çıkmış bağı)")
        for x in sorted(onem["maddeler"], key=lambda x: -int(x.get("puan") or 0)):
            sy = ",".join(str(a.get("sayfa")) for a in x.get("alinti") or [])
            s.append(f"- ({x.get('puan')}) [{kod}:{sy}] **{x.get('baslik')}** — {x.get('bilgi')}"
                     + (f" · çıkmış: {len(x['cikmis'])}" if x.get("cikmis") else ""))
        s.append("")
    sv = _oku(kd / "sayfalar.json", []) or []
    tablolar = [(x["sayfa"], t) for x in sv for t in x.get("tablolar") or []]
    if tablolar:
        s.append("## Tablolar (slayttaki hâliyle)")
        for sy, t in tablolar:
            s.append(f"[{kod}:{sy}]")
            s += ["| " + " | ".join(c.replace("\n", " ") for c in satir) + " |" for satir in t[:25]]
            s.append("")
    vur = [(x["sayfa"], v["metin"]) for x in sv for v in x.get("vurgulu") or [] if v.get("tur") in ("renk", "kalin")]
    if vur:
        s.append("## Hocanın vurguladığı ifadeler (renkli/kalın)")
        s += [f"- [{kod}:{sy}] {t}" for sy, t in vur[:120]]
        s.append("")
    gor = [x["sayfa"] for x in sv if x.get("goruntu")]
    if gor:
        s.append(f"## Görsel ağırlıklı sayfalar (görüntü: {kd}/sayfa_goruntu/<n>.png): {', '.join(map(str, gor))}")
        s.append("")
    cik = _oku(zd / "cikmis" / f"{kod}.json", []) if zd else []
    if cik:
        s.append("## Bu derse eşlenmiş çıkmış sorular (temsilci; tekrar yılları)")
        for c in cik:
            s.append(f"- [{c.get('id')}] {c.get('kok','')[:220]} → {c.get('dogru')}) "
                     f"{(c.get('secenekler') or {}).get(c.get('dogru'), '')[:120]} · {', '.join(c.get('yillar') or [])}")
        s.append("")
    return "\n".join(s).rstrip() + "\n"


def kur(kurul: int, ders: str | None = None, zorla: bool = False) -> list[str]:
    defter = _oku(MEDS / f"src/data/dersler/k{kurul}.json", {}).get("dersler") or []
    kayit, slug = yayin_kaydi(), _branslar()
    yapilan = []
    for d in defter:
        if ders and d["id"] != ders:
            continue
        pk = max((y for y in kayit if y.get("kurul") == kurul and str(y.get("ders_id", "")).startswith(d["id"] + "-")),
                 key=lambda y: y.get("yayin_zamani") or "", default=None)
        if not pk:
            continue
        kd = KOK / Path(pk["kaynak_md"]).parent
        if not (kd / "kaynak.md").exists():  # yayımlanan klasör cihazda yoksa Oracle'dan (yalnız bir kez)
            kd.mkdir(parents=True, exist_ok=True)
            subprocess.run(["rsync", "-az", f"medsor-oracle:/home/ubuntu/medsor/{Path(pk['kaynak_md']).parent}/", f"{kd}/"], timeout=300)
        zd = SPOT / f"k{kurul}{slug.get(d['brans'], '')}"
        girdiler = [kd / "kaynak.md", kd / "sayfalar.json", kd / "ders_paketi.json",
                    zd / "onem" / f"{d['kod']}.json", zd / "cikmis" / f"{d['kod']}.json"]
        m = {"ders_id": d["id"], "kod": d["kod"], "kurul": kurul, "brans": d["brans"], "konu": d["konu"],
             "pdf": pk.get("pdf"), "pdf_sha": _sha(kd / "kaynak.md"), "kaynak_dizin": str(kd),
             "zincir_dizin": str(zd) if zd.exists() else None,
             "dosyalar": {g.name if g.parent == kd else f"{g.parent.name}/{g.name}": str(g) for g in girdiler if g.exists()},
             "ozet_sha": _sha(*girdiler)}
        hedef = DEPO / d["id"]
        eski = _oku(hedef / "manifest.json", {}) or {}
        if not zorla and eski.get("ozet_sha") == m["ozet_sha"] and (hedef / "ozet.md").exists():
            continue
        hedef.mkdir(parents=True, exist_ok=True)
        (hedef / "ozet.md").write_text(ozet_derle(m), encoding="utf-8")
        m["guncellendi"] = dt.datetime.now().isoformat(timespec="seconds")
        (hedef / "manifest.json").write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
        yapilan.append(d["id"])
    return yapilan


def manifest(ders_id: str) -> dict | None:
    return _oku(DEPO / ders_id / "manifest.json")


def ozet_yolu(ders_id: str) -> Path | None:
    p = DEPO / ders_id / "ozet.md"
    return p if p.exists() else None


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--kurul", type=int); ap.add_argument("--ders"); ap.add_argument("--zorla", action="store_true")
    ap.add_argument("--liste", action="store_true")
    a = ap.parse_args()
    if a.liste:
        for p in sorted(DEPO.glob(f"k{a.kurul or ''}*/manifest.json")):
            m = _oku(p, {})
            print(f"{m['ders_id']} {m['kod']:5} {m['konu'][:40]:40} özet {len((p.parent / 'ozet.md').read_text().splitlines())} satır · {m.get('guncellendi')}")
        sys.exit(0)
    kurullar = [a.kurul] if a.kurul else range(2, 7)
    for k in kurullar:
        y = kur(k, a.ders, a.zorla)
        print(f"Kurul {k}: {len(y)} ders deposu güncellendi {y[:8]}")
