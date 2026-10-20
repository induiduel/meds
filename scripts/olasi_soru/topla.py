#!/usr/bin/env python3
"""Olası soru motoru — 1. adım: kanıt toplama + 100 yuvaya kümeleme + uzlaşı (yerel, modelsiz/CPU).

Bir kurul sınavında 100 soru vardır. Öğrencilerin sınav sonrası eklediği binlerce kayıt
(soru, parça/ipucu, şık, cevap iddiası, birleştirilmiş uydu taslak, defter katkısı) aslında
bu 100 sorunun parçalarıdır. Bu betik her kaydı bir "kanıt" satırına çevirir, yuvaya atar
(numara verilmişse o numara; verilmemişse bge-m3 benzerliğiyle en yakın yuva) ve her yuva için
uzlaşı özeti çıkarır: en çok desteklenen kök cümleleri, şık adayları + destek sayısı,
cevap iddiaları + oy, katkıda bulunan kişi sayısı, branş.

Çıktı (sonraki adım TALIMAT.md ile Claude'un olası soruyu kurması):
  meds_temp/olasi_soru/k<N>/kanit.jsonl   — her kanıt bir satır (kimlik: kanit id'si kararlı)
  meds_temp/olasi_soru/k<N>/yuvalar.json  — yuva → uzlaşı özeti
  meds_temp/olasi_soru/k<N>/parmak_izi.txt — girdi karması; değişmediyse gece işi atlanır

Kullanım: python3 topla.py --kurul 1 [--esik 0.80] [--modelsiz]
"""
import argparse, collections, hashlib, json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
MEDS = KOK / "meds"
sys.path.insert(0, str(MEDS / "scripts/agents"))

YER_TUTUCU = re.compile(r"^\s*şık\s*[a-e]\s*$", re.I)


def temiz(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()


def kid(*parca):
    return hashlib.sha1("|".join(map(str, parca)).encode()).hexdigest()[:12]


def sinav_tarihi(kurul):
    t = json.loads((MEDS / "src/data/kurul_takvimi.json").read_text())
    return next(k["sinav"] for k in t["kurullar"] if k["kurul"] == kurul)


def kurul_sorulari(kurul, tum=False):
    """Bu yılın sınavına ait kayıtlar: sınav gününden (dahil) sonra oluşturulanlar.
    Geçmiş yıl çıkmışları (isPastExam / eski examYear) bu sınavın kanıtı değildir."""
    d = json.loads((MEDS / "data/questions.json").read_text())
    q = d["questions"] if isinstance(d, dict) else d
    cid, sinav = f"donem3-kurul{kurul}", sinav_tarihi(kurul)
    yil = int(sinav[:4])
    def uygun(x):
        if not isinstance(x, dict) or x.get("committeeId") != cid or x.get("isPastExam"):
            return False
        if tum:
            return True
        if x.get("examYear") and int(str(x["examYear"])[:4]) < yil:
            return False
        return str(x.get("createdAt", ""))[:10] >= sinav
    return [x for x in q if uygun(x)]


def kanitlar(soru):
    """Bir havuz sorusundan kanıt satırları üretir. Her satır: id, qid, tur, metin, kisi, yuva."""
    qid, no = soru["id"], soru.get("questionNumber") or None
    rec = soru.get("reconstruction") or {}
    taban = {"qid": qid, "yuva": no if no and 1 <= int(no) <= 200 else None,
             "brans": soru.get("discipline") or "", "kurul": soru.get("kurul")}
    out = []

    def ekle(tur, metin, kisi="", **ek):
        metin = temiz(metin)
        if metin and not YER_TUTUCU.match(metin):
            out.append({**taban, "id": kid(qid, tur, metin, kisi), "tur": tur, "metin": metin, "kisi": kisi, **ek})

    ekle("kok", soru.get("stem") or soru.get("rawStem"), soru.get("contributedByUid", ""))
    ekle("kok_kurgu", rec.get("stem"))
    for r in soru.get("revisions") or []:
        ekle("kok_surum", r.get("stem"), r.get("editorUid", ""))
    for f in soru.get("fragments") or []:
        ekle("parca", f.get("text"), f.get("authorUid") or f.get("uid", ""))
    for o in (soru.get("options") or []) + (rec.get("options") or []):
        if not o.get("isAiFilled"):
            ekle("sik", o.get("text"), o.get("authorUid", ""), anahtar=o.get("key"))
    for s in soru.get("mergedSatellites") or []:
        if isinstance(s, dict):
            ekle("uydu", s.get("stem") or s.get("text"), s.get("contributedByUid", ""))
    ca = soru.get("claimedAnswer") or soru.get("correctAnswer")
    if ca:
        ekle("cevap", ca, soru.get("contributedByUid", ""))
    for c in soru.get("comments") or []:
        ekle("yorum", c.get("text"), c.get("authorUid", ""))
    # Defter: kullanıcı katkıları (ai_* olayları ham kanıt sayılmaz)
    defter = MEDS / "data/question_ledger" / (re.sub(r"[^A-Za-z0-9._-]", "_", qid)[:160] + ".jsonl")
    if defter.exists():
        for satir in defter.read_text().splitlines():
            try:
                ev = json.loads(satir)
            except ValueError:
                continue
            if str(ev.get("type", "")).startswith("ai_") or (ev.get("actor") or {}).get("kind") == "ai":
                continue
            p = ev.get("payload") or {}
            metin = p.get("text") or p.get("stem") or p.get("answer") or ""
            if metin:
                ekle("defter:" + ev.get("type", ""), metin, (ev.get("actor") or {}).get("uid", ""))
    return out


def geri_bildirimler(kurul):
    """Olası sorular ekranındaki öğrenci geri bildirimi (data/olasi_sorular/geri_bildirim_k<N>.jsonl) → yuvaya kanıt."""
    p = MEDS / f"data/olasi_sorular/geri_bildirim_k{kurul}.jsonl"
    out = []
    if not p.exists():
        return out
    for satir in p.read_text().splitlines():
        try:
            g = json.loads(satir)
        except ValueError:
            continue
        m = re.fullmatch(rf"k{kurul}-os-(\d{{3}})", g.get("id", ""))
        if not m:
            continue
        metin = temiz(f"[{g.get('karar')}] {g.get('metin', '')} {('cevap ' + g['cevap']) if g.get('cevap') else ''}")
        out.append({"qid": g["id"], "yuva": int(m.group(1)), "brans": "", "kurul": kurul,
                    "id": kid(g["id"], g.get("ts"), metin, g.get("uid")), "tur": "geri_bildirim",
                    "metin": metin, "kisi": g.get("uid", "")})
        if g.get("cevap"):
            out.append({**out[-1], "id": kid(g["id"], g.get("ts"), "cevap", g["cevap"]), "tur": "cevap",
                        "metin": g["cevap"].upper()})
    return out


def yuvala(satirlar, esik, modelsiz):
    """Numarasız kanıtları, numaralı yuvaların köklerine bge-m3 ile en yakın olana atar."""
    numarali = [s for s in satirlar if s["yuva"]]
    bos = [s for s in satirlar if not s["yuva"]]
    if not bos:
        return
    if modelsiz or not numarali:
        for s in bos:
            s["yuva"] = "serbest:" + s["qid"]
        return
    from lib import embed  # CPU bge-m3 servisi (:8094)
    import numpy as np
    kokler = collections.defaultdict(list)
    for s in numarali:
        if s["tur"].startswith("kok"):
            kokler[s["yuva"]].append(s["metin"])
    ad = list(kokler)
    A = np.array(embed([" ".join(kokler[y])[:1500] for y in ad], model="bge-m3"))
    B = np.array(embed([s["metin"][:1500] for s in bos], model="bge-m3"))
    A /= np.linalg.norm(A, axis=1, keepdims=True); B /= np.linalg.norm(B, axis=1, keepdims=True)
    S = B @ A.T
    # Aynı havuz sorusunun bütün numarasız kanıtları birlikte taşınır: qid başına ortalama.
    by_q = collections.defaultdict(list)
    for i, s in enumerate(bos):
        by_q[s["qid"]].append(i)
    for qid, ix in by_q.items():
        ort = S[ix].mean(axis=0); j = int(ort.argmax())
        hedef = ad[j] if ort[j] >= esik else "serbest:" + qid
        for i in ix:
            bos[i]["yuva"] = hedef; bos[i]["benzerlik"] = round(float(ort[j]), 3)


def uzlasi(satirlar):
    yuvalar = collections.defaultdict(list)
    for s in satirlar:
        yuvalar[str(s["yuva"])].append(s)
    out = {}
    for y, ss in yuvalar.items():
        kisiler = {s["kisi"] for s in ss if s["kisi"]}
        kokler = collections.Counter(s["metin"] for s in ss if s["tur"].startswith("kok") or s["tur"] == "uydu")
        siklar = collections.Counter(s["metin"].casefold() for s in ss if s["tur"] == "sik")
        sik_ad = {s["metin"].casefold(): s["metin"] for s in ss if s["tur"] == "sik"}
        cevap = collections.Counter(s["metin"].upper()[:1] if len(s["metin"]) <= 2 else s["metin"]
                                    for s in ss if s["tur"] == "cevap" or s["tur"].endswith("answer"))
        brans = collections.Counter(s["brans"] for s in ss if s["brans"])
        out[y] = {
            "yuva": y, "kanit_sayisi": len(ss), "kisi_sayisi": len(kisiler),
            "brans": brans.most_common(1)[0][0] if brans else "",
            "havuz_sorulari": sorted({s["qid"] for s in ss}),
            "kok_adaylari": [{"metin": m, "destek": n} for m, n in kokler.most_common(8)],
            "parcalar": sorted({s["metin"] for s in ss if s["tur"] in ("parca", "yorum") or s["tur"].startswith("defter:")})[:40],
            "geri_bildirim": [s["metin"] for s in ss if s["tur"] == "geri_bildirim"][-20:],
            "sik_adaylari": [{"metin": sik_ad[m], "destek": n} for m, n in siklar.most_common(12)],
            "cevap_iddialari": [{"cevap": c, "oy": n} for c, n in cevap.most_common()],
            "kanit_idleri": [s["id"] for s in ss],
        }
    return dict(sorted(out.items(), key=lambda kv: (not kv[0].isdigit(), int(kv[0]) if kv[0].isdigit() else 0, kv[0])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kurul", type=int, required=True)
    ap.add_argument("--esik", type=float, default=0.80)
    ap.add_argument("--tum", action="store_true", help="tarih süzgeci olmadan (deneme için)")
    ap.add_argument("--modelsiz", action="store_true", help="vektör servisi olmadan (numarasızlar serbest kalır)")
    a = ap.parse_args()
    hedef = KOK / f"meds_temp/olasi_soru/k{a.kurul}"; hedef.mkdir(parents=True, exist_ok=True)
    sorular = kurul_sorulari(a.kurul, a.tum)
    satirlar = [k for s in sorular for k in kanitlar(s)] + geri_bildirimler(a.kurul)
    iz = hashlib.sha256("\n".join(sorted(s["id"] for s in satirlar)).encode()).hexdigest()
    yuvala(satirlar, a.esik, a.modelsiz)
    with open(hedef / "kanit.jsonl", "w") as f:
        for s in satirlar:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    yv = uzlasi(satirlar)
    (hedef / "yuvalar.json").write_text(json.dumps(
        {"surum": 1, "kurul": a.kurul, "parmak_izi": iz, "havuz_sorusu": len(sorular),
         "kanit": len(satirlar), "yuvalar": yv}, ensure_ascii=False, indent=1))
    onceki = (hedef / "parmak_izi.txt").read_text().strip() if (hedef / "parmak_izi.txt").exists() else ""
    (hedef / "parmak_izi.txt").write_text(iz)
    numarali = sum(1 for k in yv if k.isdigit())
    print(f"Kurul {a.kurul}: {len(sorular)} havuz sorusu → {len(satirlar)} kanıt → {numarali} numaralı yuva + "
          f"{len(yv) - numarali} serbest küme · {'DEĞİŞİKLİK VAR' if iz != onceki else 'değişiklik yok'}")
    sys.exit(0 if iz != onceki else 3)  # 3 = yeni veri yok (gece işi sentezi atlar)


if __name__ == "__main__":
    main()
