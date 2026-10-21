#!/usr/bin/env python3
"""Anlamsal slayt çapası kapısı (Kurul 2+ ders zinciri `capa` adımı; TALIMAT_CAPA.md).

Denetler: mdSha1 = sha1(metin/<key>.md); paragraf sayısı = canlı ders paragrafları (GET /api/canli-ders/<key>); her paragrafta
her cümlenin (istemci bölmesi, pdf_isaret.cumle_sonlari) en az bir çapası; `ses` cümlenin başı; sayfa PDF aralığında; madde
dizinleri Sayfa.maddeler, resim dizini Sayfa.resimler içinde; kutu/yol 0–1 aralığında; yol ifadesi cümlede geçer.
Kapsama: madde/resim/kutu taşıyan cümle oranı ≥ ESIK (yalnız sayfa vurgusu kalan cümle az olmalı).
Kullanım: .venv-ocr/bin/python scripts/sesli_anlatim/capa_dogrula.py <key> <capa.json>   (MEDS_API: cümle bölmesi + PDF)
"""
import hashlib, json, sys, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdf_isaret import API, INDIR, KOK, Pdf, cumle_sonlari, pdf_indir  # noqa: E402

ESIK = 0.7
_op = urllib.request.build_opener(); _op.addheaders = [("User-Agent", "medsor-capa/1")]; urllib.request.install_opener(_op)


def main():
    key, yol = sys.argv[1], Path(sys.argv[2])
    H = []
    try:
        cj = json.loads(yol.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"HATA: {yol} okunamadı: {e}\n1 HATA"); return 1
    md = KOK / "metin" / f"{key}.md"
    if cj.get("mdSha1") != hashlib.sha1(md.read_bytes()).hexdigest():
        H.append(f"mdSha1 metin/{key}.md ile tutmuyor (metin değişmiş ya da yanlış hesap)")
    d = json.load(urllib.request.urlopen(f"{API}/api/canli-ders/{key}", timeout=30))
    paras = [p for b in d["bolumler"] for p in b["paragraflar"]]
    hz = json.loads((KOK / "hizalama" / f"{key}.json").read_text(encoding="utf-8"))
    pdfler = []
    for fi, f in enumerate(hz["dosyalar"]):
        p = INDIR / f["path"]
        p = p if p.exists() else pdf_indir(hz["deckId"], f, fi)
        pdfler.append(Pdf(p) if p and Path(p).exists() else None)
    P = cj.get("p") or []
    if len(P) != len(paras):
        H.append(f"paragraf sayısı {len(P)} ≠ canlı ders {len(paras)}")
    toplam = anlamsal = 0
    for pi, (par, caps) in enumerate(zip(paras, P)):
        m = par["metin"]; a = 0
        cumleler = []
        for e in cumle_sonlari(m):
            cumleler.append(m[a:e].strip()); a = e
        if len(caps) != len(cumleler):
            H.append(f"P{pi}: {len(caps)} çapa ≠ {len(cumleler)} cümle")
        for ci, (c, cm) in enumerate(zip(caps, cumleler)):
            yer = f"P{pi}.C{ci}"; toplam += 1
            if not cm.startswith(str(c.get("ses", ""))[:40].strip()):
                H.append(f"{yer}: ses cümlenin başı değil: {str(c.get('ses'))[:40]!r} / {cm[:40]!r}")
            pdf = pdfler[int(c.get("dosya") or 0)] if int(c.get("dosya") or 0) < len(pdfler) else None
            if not pdf:
                H.append(f"{yer}: dosya {c.get('dosya')} PDF'i yok"); continue
            sy = pdf.sayfa(int(c.get("sayfa") or 0))
            if not sy:
                H.append(f"{yer}: sayfa {c.get('sayfa')} aralık dışı (1–{pdf.doc.page_count})"); continue
            ok = False
            if c.get("madde") is not None:
                bad = [i for i in c["madde"] if not 0 <= int(i) < len(sy.maddeler)]
                H += [f"{yer}: madde M{bad} sayfada yok ({len(sy.maddeler)} madde)"] if bad else []
                ok = ok or (bool(c["madde"]) and not bad)
            if c.get("resim") is not None:
                if not 0 <= int(c["resim"]) < len(sy.resimler):
                    H.append(f"{yer}: resim R{c['resim']} sayfada yok")
                else:
                    ok = True
            if c.get("kutu") is not None:
                k = c["kutu"]
                if not (len(k) == 4 and all(0 <= float(v) <= 1 for v in k) and k[0] < k[2] and k[1] < k[3]):
                    H.append(f"{yer}: kutu [x0,y0,x1,y1] 0–1 ve x0<x1, y0<y1 olmalı")
                else:
                    ok = True
            for y in c.get("yol") or []:
                if not (0 <= float(y.get("x", -1)) <= 1 and 0 <= float(y.get("y", -1)) <= 1):
                    H.append(f"{yer}: yol noktası 0–1 dışında")
                if str(y.get("k", "")).lower() not in cm.lower():
                    H.append(f"{yer}: yol ifadesi cümlede yok: {y.get('k')!r}")
            anlamsal += ok
    oran = anlamsal / max(1, toplam)
    if oran < ESIK:
        H.append(f"anlamsal kapsama %{oran * 100:.0f} < %{ESIK * 100:.0f} (madde/resim/kutu taşıyan cümle)")
    for h in H[:80]:
        print("HATA", h)
    print(f"{key}: {toplam} cümle · anlamsal %{oran * 100:.0f} · {len(H)} HATA")
    return 1 if H else 0


if __name__ == "__main__":
    sys.exit(main())
