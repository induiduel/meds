#!/usr/bin/env python3
"""Çıkmış soru → sesli ders cümlesi → PDF konumu (data/sesli_anlatim/cikmis_konum/<key>.json).

vurgu_uret.py ile aynı kaynak seçimi (örnek soruların ilgili_cikmis bağları + konu = ders başlığı olan çıkmışlar);
her soru (kök + doğru cevap) bge-m3 (CPU, :8094) ile dersin cümlelerine eşlenir, en iyi cümle saklanır.
Cümle dizini pdf_isaret.py ile aynı sınırlarla (cumle_sinirlari) sayılır; ön yüz PDF sayfasını/kutusunu
isaret[p][c]'den alır (yoksa paragrafın hizalama sayfası). Metin değişirse (metinHash) sunucu dosyayı göndermez.
Çıktı: {"surum":1,"metinHash":…,"q":[{"id","kok","cevap","yil","p","c","skor"}]}

Kullanım: python3 scripts/sesli_anlatim/cikmis_konum.py [--ders KEY] [--esik 0.65] [--eksik]
"""
import argparse, hashlib, json, os, re, sys, urllib.error, urllib.request
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "scripts" / "agents"))
sys.path.insert(0, str(KOK / "scripts" / "sesli_anlatim"))
from lib import embed, fold  # noqa: E402
from pdf_hizala import cumle_sinirlari  # noqa: E402

CIKTI = KOK / "data" / "sesli_anlatim" / "cikmis_konum"


def duz(s) -> str:
    return re.sub(r"\*\*", "", str(s or "")).strip()


def sorular(key: str, baslik: str, cikmislar) -> list[dict]:
    out, gor = [], set()

    def ekle(qid, kok, sec, dogru, yil=None):
        kok = duz(kok)
        if not qid or not kok or qid in gor:
            return
        gor.add(qid)
        c = duz((sec or {}).get(dogru)) if dogru else ""
        out.append({"id": str(qid), "kok": kok, "cevap": c, "yil": yil})

    byid = {q["id"]: q for q in cikmislar}
    f = KOK / "src/data/ornek_sorular/k1" / f"{key}.json"
    if f.exists():
        for k in json.load(open(f)).get("kazanimlar", []):
            for q in k.get("ilgili_cikmis") or []:
                if isinstance(q, dict):
                    ekle(q.get("id"), q.get("soru"), q.get("secenekler"), q.get("cevap"), (byid.get(q.get("id")) or {}).get("examYear"))
    hedef = fold(baslik)
    for q in cikmislar:
        if fold(q.get("topic") or "") != hedef:
            continue
        r = q.get("reconstruction") or {}
        ops = r.get("options") or q.get("options") or []
        sec = {o.get("key"): o.get("text") for o in ops if isinstance(o, dict)}
        ekle(q["id"], r.get("stem") or q.get("stem"), sec, q.get("correctAnswer"), q.get("examYear"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ders"); ap.add_argument("--esik", type=float, default=0.65)
    ap.add_argument("--eksik", action="store_true", help="çıktısı olanları atla")
    a = ap.parse_args()
    cikmislar = [q for q in json.load(open(KOK / "src/data/pastQuestions.json"))
                 if q.get("committeeId") == "donem3-kurul1" and not q.get("hidden") and not q.get("iptal")]
    dersler = json.load(open(KOK / "data/sesli_anlatim/dersler.json"))
    CIKTI.mkdir(parents=True, exist_ok=True)
    for d in dersler:
        key = d["key"]
        if a.ders and key != a.ders: continue
        if a.eksik and (CIKTI / f"{key}.json").exists(): continue
        baslik = re.sub(r"\s*—\s*Sınav Odaklı (?:Özet|Anlatım)(?: \(V\d\))?$", "", d["baslik"])
        qs = sorular(re.sub(r"-v\d$", "", key), baslik, cikmislar)
        try:
            det = json.load(urllib.request.urlopen(urllib.request.Request(
                f"{os.environ.get('MEDS_API', 'http://127.0.0.1:3000')}/api/canli-ders/{key}",
                headers={"User-Agent": "medsor-cikmis-konum/1"}), timeout=60))
        except urllib.error.URLError as e:
            print(f"{key}: ders okunamadı ({e}) — atlandı"); continue
        pars = [p for b in det["bolumler"] for p in b["paragraflar"]]
        cs = []  # (paragraf i, cümle dizini, metin)
        for p in pars:
            m, s = p["metin"], 0
            for ci, e in enumerate(cumle_sinirlari(m)):
                t = m[s:e].strip()
                if len(t) > 3: cs.append((p["i"], ci, t))
                s = e
        if not qs or not cs:
            print(f"{key}: soru {len(qs)}, cümle {len(cs)} — atlandı"); continue
        sim = embed([f"{q['kok']} {q['cevap']}".strip() for q in qs]) @ embed([c[2] for c in cs]).T
        q_out, kokler = [], set()
        for qi, q in enumerate(qs):
            ik = fold(q["kok"])[:70]
            if ik in kokler: continue  # aynı sorunun kopyaları (ilgili_cikmis + havuz) tek kez
            kokler.add(ik)
            ci = int(sim[qi].argmax())
            v = float(sim[qi, ci])
            if v < a.esik: continue
            ayni = (cs[ci][0], cs[ci][1], fold(q["cevap"]))  # aynı cümle + aynı cevap = aynı sorunun başka yazımı
            if ayni in kokler: continue
            kokler.add(ayni)
            q_out.append({**q, "kok": q["kok"][:220], "p": cs[ci][0], "c": cs[ci][1], "skor": round(v, 3)})
        q_out.sort(key=lambda x: (x["p"], x["c"]))
        h = hashlib.sha1("\n".join(p["metin"] for p in pars).encode()).hexdigest()
        (CIKTI / f"{key}.json").write_text(json.dumps({"surum": 1, "metinHash": h, "q": q_out}, ensure_ascii=False, separators=(",", ":")))
        print(f"{key}: soru {len(qs)}, eşlenen {len(q_out)}", flush=True)


if __name__ == "__main__":
    main()
