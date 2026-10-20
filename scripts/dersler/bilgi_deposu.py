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


def _yollar(m: dict) -> dict:
    """Dosya yolları: manifest["yollar"] (açık) ya da Kurul 2+ düzeni (kaynak_dizin + zincir_dizin/<alt>/<kod>.json)."""
    if m.get("yollar"):
        return {k: Path(v) if v else None for k, v in m["yollar"].items()}
    kd = Path(m["kaynak_dizin"]); zd = Path(m["zincir_dizin"]) if m.get("zincir_dizin") else None
    return {"kaynak_md": kd / "kaynak.md", "sayfalar": kd / "sayfalar.json", "ders_paketi": kd / "ders_paketi.json",
            "onem": zd / "onem" / f"{m['kod']}.json" if zd else None, "cikmis": zd / "cikmis" / f"{m['kod']}.json" if zd else None}


def ozet_derle(m: dict) -> str:
    """Depo dosyalarından ders özeti (yalnız depodaki veriden; PDF açılmaz)."""
    Y, kod = _yollar(m), m["kod"]
    s = [f"# {m['konu']} ({m['ders_id']} · {kod})", f"Branş: {m['brans']} · Kurul {m['kurul']} · PDF: {m.get('pdf') or '-'}", ""]
    paket = _oku(Y["ders_paketi"], {}) if Y.get("ders_paketi") else {}
    paket = paket or {}
    if paket.get("bilgi_paketi"):
        s.append("## Bilgi paketi (ders PDF'inden atomik bilgiler)")
        for b in paket["bilgi_paketi"]:
            sy = (b.get("kanit") or {}).get("sayfa")
            s.append(f"- [{kod}:{sy}] {b.get('bilgi')}" + (f" — {b['sonuc']}" if b.get("sonuc") else ""))
        s.append("")
    onem = _oku(Y["onem"], {}) if Y.get("onem") else {}
    if onem and onem.get("maddeler"):
        s.append("## Sınav önemi (önem listesi; puan, çıkmış bağı)")
        for x in sorted(onem["maddeler"], key=lambda x: -int(x.get("puan") or 0)):
            sy = ",".join(str(a.get("sayfa")) for a in x.get("alinti") or [])
            s.append(f"- ({x.get('puan')}) [{kod}:{sy}] **{x.get('baslik')}** — {x.get('bilgi')}"
                     + (f" · çıkmış: {len(x['cikmis'])}" if x.get("cikmis") else ""))
        s.append("")
    sv = (_oku(Y["sayfalar"], []) if Y.get("sayfalar") else []) or []
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
        s.append(f"## Görsel ağırlıklı sayfalar (görüntü: {Y['sayfalar'].parent}/sayfa_goruntu/<n>.png): {', '.join(map(str, gor))}")
        s.append("")
    cik = _oku(Y["cikmis"], []) if Y.get("cikmis") else []
    if isinstance(cik, dict):  # patoloji: tek dosyada kod → liste
        cik = cik.get(m.get("kaynak_kod") or "", [])
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


def _katla(t):
    return re.sub(r"[^a-z0-9çğıöşü ]+", " ", str(t).replace("İ", "i").replace("I", "ı").lower()).split()


def kur_k1(zorla: bool = False) -> list[str]:
    """Kurul 1: dersler branş klasörlerinden (meds_temp/spot_cozucu/<brans>/, patoloji meds_temp/patoloji_onem/) — PDF
    metni, önem listesi, çıkmışlar zaten var. Eşleme: aynı branşta PDF adı ↔ defter konusu benzerliği (≥0,5 ve tekil);
    belirsiz ders atlanır (uydurma yok). Kod etiketi defter kodu (1e07…), dosyalar eski koddan (e07)."""
    import difflib
    defter = _oku(MEDS / "src/data/dersler/k1.json", {}).get("dersler") or []
    kaynaklar = [(b, SPOT / slug, "onem/{k}.json", "cikmis/{k}.json") for b, slug in
                 [("Enfeksiyon Hastalıkları", "enfeksiyon"), ("Üroloji", "uroloji"), ("Tıbbi Genetik", "genetik"),
                  ("Halk Sağlığı", "halksagligi"), ("Kadın Hastalıkları ve Doğum", "kadindogum"), ("Tıbbi Farmakoloji", "farmakoloji")]]
    kaynaklar.append(("Tıbbi Patoloji", KOK / "meds_temp/patoloji_onem", "cikti/{k}.json", "cikmis_pdf.json"))
    yapilan, kullanilan = [], set()
    for brans, W, onem_k, cikmis_k in kaynaklar:
        liste = _oku(W / "pdf_liste.json", []) or []
        adaylar = [d for d in defter if d["brans"] == brans]
        # Eşleme KESİN olmalı (yanlış ders = kampta yanlış bilgi): isim benzerliği değil, hattın kendi konu tablosu.
        #  · patoloji dışı: spot_cozucu/aday_hazirla.BRANS (kod → müfredat konu adları) ↔ defter konusu, tam ad eşitliği
        #  · patoloji: src/data/patoloji_onem/index.json ders başlığı ↔ defter konusu, benzerlik ≥0,9
        sys.path.insert(0, str(MEDS / "scripts/spot_cozucu")); import aday_hazirla as AH
        nk = lambda t: " ".join(_katla(t))
        pato = {x["kod"]: x.get("baslik", "") for x in (_oku(MEDS / "src/data/patoloji_onem/index.json", {}) or {}).get("dersler", [])}
        for x in liste:
            ad = re.sub(r"^\s*\d+\s*[\)\.\-]\s*", "", Path(x.get("ad") or "").stem)
            if brans == "Tıbbi Patoloji":
                adlar = {nk(pato.get(x["kod"], ""))} - {""}
            else:
                adlar = {nk(k) for k in (AH.BRANS.get(W.name, ("", {}))[1].get(x["kod"]) or [])}
            bos = [d for d in adaylar if d["id"] not in kullanilan]
            es = [d for d in bos if nk(d["konu"]) in adlar]  # 1) tam ad eşitliği
            on = [d for d in bos if len(nk(d["konu"])) >= 20 and any(a_.startswith(nk(d["konu"])) for a_ in adlar)]
            if len(es) == 1:
                puan, tamam = [(1.0, es[0])], True
            elif not es and len(on) == 1:  # 1b) başlık defter konusunun uzatılmış hâli ("Mesane … Tümörleri; Cinsel …")
                puan, tamam = [(1.0, on[0])], True
            else:  # 2) yüksek eşikli benzerlik (≥0,9 ve ikinciden ≥0,03 önde)
                puan = sorted(((max([difflib.SequenceMatcher(None, a_, nk(d["konu"])).ratio() for a_ in adlar] or [0]), d)
                               for d in bos), key=lambda t: -t[0])
                tamam = bool(puan) and puan[0][0] >= 0.9 and (len(puan) < 2 or puan[0][0] - puan[1][0] >= 0.03)
            if not tamam:
                print(f"   atlandı (kesin eşleşme yok): {brans} {x['kod']} {ad[:40]}"); continue
            d = puan[0][1]; kullanilan.add(d["id"])
            # sayfa varlıkları (tablo/görsel/hoca vurgusu): PDF'ten YALNIZ BİR KEZ çıkarılır, depoda kalır
            sv_yol = DEPO / d["id"] / "sayfalar.json"
            if not sv_yol.exists():
                pdf = next(iter(sorted((KOK / "meds_downloads/drive_root/Kurul 1").glob(f"*/{x.get('ad')}"))), None)
                try:
                    sys.path.insert(0, str(MEDS / "scripts/ders_isci")); from cikar import sayfa_varliklari
                    if pdf:
                        (DEPO / d["id"]).mkdir(parents=True, exist_ok=True); sayfa_varliklari(pdf, DEPO / d["id"])
                except ImportError:
                    pass  # PyMuPDF yok (sistem python'u): varlıklar .venv-ocr ile bir kez üretilir
            Y = {"kaynak_md": str(W / "pdf_metin" / f"{x['kod']}.md"),
                 "sayfalar": str(sv_yol) if sv_yol.exists() else None, "ders_paketi": None,
                 "onem": str(W / onem_k.format(k=x["kod"])), "cikmis": str(W / cikmis_k.format(k=x["kod"]))}
            m = {"ders_id": d["id"], "kod": d["kod"], "kaynak_kod": x["kod"], "kurul": 1, "brans": brans, "konu": d["konu"],
                 "pdf": x.get("ad"), "pdf_sha": _sha(Y["kaynak_md"]), "kaynak_dizin": str(W / "pdf_metin"), "yollar": Y,
                 "ozet_sha": _sha(*[v for v in Y.values() if v])}
            hedef = DEPO / d["id"]
            eski = _oku(hedef / "manifest.json", {}) or {}
            if not zorla and eski.get("ozet_sha") == m["ozet_sha"] and (hedef / "ozet.md").exists():
                continue
            # özet satır etiketleri defter kodunu taşır: ozet_derle m["kod"] kullanır
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
    kurullar = [a.kurul] if a.kurul else range(1, 7)
    for k in kurullar:
        y = kur_k1(a.zorla) if k == 1 else kur(k, a.ders, a.zorla)
        print(f"Kurul {k}: {len(y)} ders deposu güncellendi {y[:8]}")
