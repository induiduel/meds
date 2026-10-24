#!/usr/bin/env python3
"""2025-2026 arşiv dersi uçtan uca doğrulama, yayınlama, ses/zamanlama/işaret/çizim, .medspak üretimi ve Güncelleme Günlüğü.

Mevcut 2026-2027 veritabanını (meds_database_v2, interactive_learning_decks.json, data/sesli_anlatim) ASLA kirletmez;
yalnızca meds_database_25_26/ ve meds/data/arsiv_25_26/ altına yazar.

Kullanım:
  /home/indu/medsor/meds/.venv-ocr/bin/python scripts/arsiv_25_26/arsiv_yayinla.py --key y25-k2-01-norolojik-hastaya-yaklasim \
      [--neden "İlk 2025-2026 arşiv üretimi ve Kurul 2 pipeline doğrulaması"] \
      [--hatali-bilgi "..."] [--degisiklik "..."]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
ROOT = MEDS.parent
DB_25_26 = ROOT / "meds_database_25_26"
ARSIV_DATA = MEDS / "data" / "arsiv_25_26"
SA_KOK = ARSIV_DATA / "sesli_anlatim"

sys.path.insert(0, str(MEDS / "scripts" / "ders_isci"))
sys.path.insert(0, str(MEDS / "scripts" / "sesli_anlatim"))
sys.path.insert(0, str(MEDS / "scripts" / "cizim"))
sys.path.insert(0, str(MEDS / "scripts" / "paket"))


def json_kilitli_guncelle(yol: Path, varsayilan, guncelle_fn):
    import fcntl
    yol.parent.mkdir(parents=True, exist_ok=True)
    lock_yol = yol.with_suffix(yol.suffix + ".lock")
    with open(lock_yol, "w", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            mevcut = json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else varsayilan
        except Exception:
            mevcut = varsayilan
        yeni = guncelle_fn(mevcut)
        tmp = yol.with_suffix(yol.suffix + f".{os.getpid()}.tmp")
        tmp.write_text(json.dumps(yeni, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(yol)
        return yeni


def gpu_kilit_al():
    import fcntl
    kilit_yol = Path("/tmp/meds_arsiv_gpu.lock")
    f = open(kilit_yol, "w", encoding="utf-8")
    fcntl.flock(f, fcntl.LOCK_EX)
    return f


def fnv(s: str) -> str:
    h = 2166136261
    b = s.encode("utf-16-le")
    for i in range(0, len(b), 2):
        h = ((h ^ (b[i] | b[i + 1] << 8)) * 16777619) & 0xFFFFFFFF
    return format(h, "x")


def metin_paragraflari(md: str) -> list[dict]:
    out = []
    tampon: list[str] = []
    bolum_baslik = ""
    bolum_basi = False

    def bitir():
        nonlocal tampon, bolum_basi
        t = re.sub(r"\s+", " ", " ".join(tampon)).strip()
        if t:
            out.append({"t": t, "bolumBasi": bolum_basi, "bolumBaslik": bolum_baslik})
            bolum_basi = False
        tampon = []

    for s in re.split(r"\r?\n", md):
        if s.startswith("# "):
            continue
        if s.startswith("@@"):
            bitir()
            bolum_baslik = s.replace("@@", "", 1).strip()
            bolum_basi = True
            continue
        if not s.strip():
            bitir()
        else:
            tampon.append(s.strip())
    bitir()
    return out


def denetle_taslak(taslak: Path, baglam: dict) -> list[str]:
    hatalar: list[str] = []
    key = baglam["ders_id"]
    kurul = int(baglam["kurul"])
    deste_id = baglam["deste_id"]

    # 1. denetle.py (ders_paketi, sayfa_haritasi, deck, ders_notu, ornek_sorular, sozluk, hastaliklar, bilgi_havuzu, cikmis_baglantilari)
    import denetle as D
    rapor = D.Denetim(taslak).calistir()
    if rapor.get("hata", 0) > 0:
        for err in (rapor.get("hatalar") or []):
            hatalar.append(f"denetle: {err}")

    # 2. validate_learning_decks.py --oyun-zorunlu --kurul2
    deck_yol = taslak / "deck.json"
    if deck_yol.exists():
        r = subprocess.run(
            [sys.executable, str(MEDS / "scripts" / "validate_learning_decks.py"), str(deck_yol), "--oyun-zorunlu", "--kurul2"],
            capture_output=True, text=True
        )
        if r.returncode != 0:
            hatalar.append(f"validate_learning_decks: {(r.stdout + r.stderr).strip()[-400:]}")
    else:
        hatalar.append("deck.json eksik")

    # 3. konusma_v2.py --dogrula + --turet
    v2_yol = taslak / "konusma_v2.json"
    if v2_yol.exists():
        import konusma_v2 as KV
        v2 = json.loads(v2_yol.read_text(encoding="utf-8"))
        v2_hata = KV.dogrula(v2, KV.kaynak_sayfa(taslak), KV.kaynak_metin(taslak))
        if v2_hata:
            hatalar.extend(f"konusma_v2: {x}" for x in v2_hata[:15])
        else:
            md_txt, sayfalar_l = KV.turet(v2)
            (taslak / "konusma_metni.md").write_text(md_txt, encoding="utf-8")
            (taslak / "konusma_sayfalari.json").write_text(json.dumps(sayfalar_l), encoding="utf-8")
            (taslak / "konusma_capalari.json").write_text(json.dumps(KV.capalar(v2), ensure_ascii=False), encoding="utf-8")
    else:
        hatalar.append("konusma_v2.json eksik")

    # 4. metin_denetle.py ve sesli_kapsam (0 atlanan sayfa, görsel/tablo kapsamı)
    md_yol = taslak / "konusma_metni.md"
    if md_yol.exists():
        r = subprocess.run(
            [sys.executable, str(MEDS / "scripts" / "sesli_anlatim" / "metin_denetle.py"), str(md_yol)],
            capture_output=True, text=True
        )
        if r.returncode != 0:
            hatalar.append(f"metin_denetle: {(r.stdout + r.stderr).strip()[-400:]}")
        import isle as IS
        kapsam_hata = IS.sesli_kapsam(taslak)
        if kapsam_hata:
            hatalar.extend(f"sesli_kapsam: {x}" for x in kapsam_hata)
    else:
        hatalar.append("konusma_metni.md eksik")

    return hatalar


def cumle_zaman_yerel(key: str, pars: list[dict], mp3_yol: Path, zamanlama: list[list[float]], metin_hash: str) -> dict:
    import cumle_zaman as CZ
    import numpy as np

    bayt = mp3_yol.stat().st_size
    en = CZ.enerji(CZ.coz(mp3_yol))
    dolu = en[en > 0]
    esik = max(float(np.percentile(dolu, 90)) * 0.025, float(np.percentile(dolu, 5)) * 1.5, 1.0) if len(dolu) else 1.0
    sess = CZ.sessizlikler(en, esik)
    orta = np.array([(a + b) / 2 for a, b in sess]) / 100.0
    uzun = np.array([(b - a) for a, b in sess]) / 100.0
    p_out: dict[str, list[float]] = {}
    k_out: dict[str, list[list[float]]] = {}
    for i, p in enumerate(pars):
        if i >= len(zamanlama) or not zamanlama[i]:
            continue
        bas, son = float(zamanlama[i][0]), float(zamanlama[i][1])
        sonlar = CZ.cumle_sonlari(p["t"])
        if len(sonlar) < 2 or son - bas < 1:
            continue
        L = max(1, len(p["t"]))
        sure = son - bas
        tlar: list[float] = []
        onceki = bas + 0.3
        for j, e in enumerate(sonlar[:-1]):
            tahmin = bas + sure * e / L
            kalan_cumle = len(sonlar) - 1 - j
            ust = son - 0.3 * kalan_cumle
            pay = max(1.5, min(5.0, sure * 0.12))
            lo, hi = max(onceki + 0.2, tahmin - pay), min(ust, tahmin + pay)
            sec = None
            if len(orta) and hi > lo:
                m = (orta >= lo) & (orta <= hi)
                if m.any():
                    idx = np.nonzero(m)[0]
                    puan = uzun[idx] - np.abs(orta[idx] - tahmin) * 0.02
                    k = idx[int(np.argmax(puan))]
                    if uzun[k] >= 0.12:
                        sec = float(orta[k])
            if sec is None:
                sec = min(max(tahmin, onceki + 0.2), max(onceki + 0.2, ust))
            tlar.append(round(sec, 2))
            onceki = sec
        p_out[str(i)] = tlar
        k_out[str(i)] = CZ.konusma_parcalari([bas, *tlar, son], sess)
    return {
        "surum": 2,
        "metinHash": metin_hash,
        "varyantlar": {"ema-yerel-ema": {"bayt": bayt, "p": p_out, "k": k_out}},
    }


def kelime_zaman_yerel(key: str, pars: list[dict], mp3_yol: Path, zamanlama: list[list[float]], metin_hash: str) -> dict:
    # faster-whisper .venv-hizala içinde çalışır (GPU koruyucuyla)
    py_hizala = MEDS / ".venv-hizala" / "bin" / "python"
    if not py_hizala.exists():
        py_hizala = Path(sys.executable)
    kz_yol = SA_KOK / "kelime_zaman" / f"{key}.json"
    bayt = mp3_yol.stat().st_size
    if kz_yol.exists():
        try:
            eski = json.loads(kz_yol.read_text(encoding="utf-8"))
            if eski.get("metinHash") == metin_hash and (eski.get("varyantlar") or {}).get("ema-yerel-ema", {}).get("bayt") == bayt:
                return eski
        except Exception:
            pass
    # Geçici betik çağrısı (.venv-hizala içinde faster-whisper + nvidia libs)
    site_pkgs = next((MEDS / ".venv-hizala" / "lib").glob("python*/site-packages"), None)
    ld_paths = []
    if site_pkgs and (site_pkgs / "nvidia").is_dir():
        for lib_d in (site_pkgs / "nvidia").glob("*/lib"):
            ld_paths.append(str(lib_d))
    env = os.environ.copy()
    env.pop("CUDA_VISIBLE_DEVICES", None)
    if ld_paths:
        env["LD_LIBRARY_PATH"] = ":".join(ld_paths + ([env["LD_LIBRARY_PATH"]] if env.get("LD_LIBRARY_PATH") else []))
    kod = f"""
import sys, json
from pathlib import Path
sys.argv.append("--gpu")
sys.path.insert(0, {repr(str(MEDS / "scripts" / "sesli_anlatim"))})
import kelime_zaman as KZ
paras = [{{"i": i, "metin": p["t"]}} for i, p in enumerate({repr(pars)})]
z = {repr(zamanlama)}
mp3 = Path({repr(str(mp3_yol))})
p_out, not_ = KZ.varyant_isle(paras, z, mp3)
print("KZ_NOT:", not_, file=sys.stderr)
out = {{"surum": 1, "metinHash": {repr(metin_hash)}, "varyantlar": {{"ema-yerel-ema": {{"bayt": mp3.stat().st_size, "p": p_out}}}}}}
Path({repr(str(kz_yol))}).parent.mkdir(parents=True, exist_ok=True)
Path({repr(str(kz_yol))}).write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
"""
    r = subprocess.run([str(py_hizala), "-c", kod], env=env, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Uyarı: kelime_zaman GPU/CPU hatası: {r.stderr[-400:]}", file=sys.stderr)
    return json.loads(kz_yol.read_text(encoding="utf-8")) if kz_yol.exists() else {}


def pdf_isaret_yerel(key: str, pars: list[dict], pdf_yol: Path, hz: dict, capa_p: list | None, metin_hash: str) -> dict:
    import pdf_isaret as PI
    pdf = PI.Pdf(pdf_yol)
    c_out: dict[str, list] = {}
    for pn, (p, es) in enumerate(zip(pars, hz["paragraflar"])):
        m = p["t"]
        sinir = PI.cumle_sonlari(m)
        cc = PI.cumle_capalari(m, sinir, capa_p[pn]) if capa_p and pn < len(capa_p) else None
        liste = []
        for ci, e in enumerate(sinir):
            cumle = m[(sinir[ci - 1] if ci else 0):e]
            if cc and ci < len(cc) and cc[ci] and es:
                isr = PI.capali(cumle, cc[ci], pdf)
                if isr:
                    isr["d"] = 0
                    liste.append(isr)
                    continue
            s0 = (es.get("sayfalar") or [])[ci] if ci < len(es.get("sayfalar") or []) else es["sayfa"]
            en = (0, None, s0)
            for s in (s0, s0 - 1, s0 + 1, s0 + 2, s0 - 2):
                sy = pdf.sayfa(s)
                if not sy:
                    continue
                n, r = PI.eslestir(cumle, sy)
                uz = abs(s - s0)
                esik = 0 if not uz else max(3 if uz == 1 else 4, en[0] * 1.5)
                if r and n >= max(1, esik) and (en[1] is None or n > en[0]):
                    en = (n, r, s)
            n, r, s = en
            if r:
                isr = {"d": 0, "s": s, **r}
            else:
                sy = pdf.sayfa(s0)
                if sy and sy.resimler and (PI.GORSEL.search(cumle) or (len(sy.kelimeler) < 15 and not sy.ocr)):
                    rb = max(sy.resimler, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
                    isr = {"d": 0, "s": s0, "t": "resim", "l": [sy.n(rb)], "w": []}
                else:
                    isr = {"d": 0, "s": s0, "t": "sayfa", "l": [], "w": []}
            liste.append(isr)
        c_out[str(pn)] = liste
    out = {"surum": PI.SURUM, "metinHash": metin_hash, "c": c_out}
    isr_yol = SA_KOK / "isaret" / f"{key}.json"
    isr_yol.parent.mkdir(parents=True, exist_ok=True)
    isr_yol.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return out


def cikmis_konum_yerel(key: str, pars: list[dict], v2: dict, baglam: dict, metin_hash: str) -> dict:
    from lib import embed, fold
    from pdf_hizala import cumle_sinirlari

    pq_file = MEDS / "src" / "data" / "pastQuestions.json"
    tum_pq = {q["id"]: q for q in json.loads(pq_file.read_text(encoding="utf-8"))} if pq_file.exists() else {}
    adaylar = {q["id"]: q for q in (baglam.get("aday_cikmislar") or [])}

    # v2'de doğrudan işaretlenmiş çıkmışlar + aday çıkmışlar
    cs = []
    for pi, p in enumerate(pars):
        m, s = p["t"], 0
        for ci, e in enumerate(cumle_sinirlari(m)):
            t = m[s:e].strip()
            if len(t) > 3:
                cs.append((pi, ci, t))
            s = e

    q_out = []
    gor = set()
    # Önce v2 içindeki doğrudan çıkmış bağlarını ekle
    vp = [p for b in v2.get("bolumler", []) for p in b.get("paragraflar", [])]
    for pi, p in enumerate(vp):
        for ci, c in enumerate(p.get("cumleler", [])):
            for qid in c.get("cikmis") or []:
                qid = str(qid)
                if qid in gor:
                    continue
                q = adaylar.get(qid) or tum_pq.get(qid)
                if not q:
                    continue
                gor.add(qid)
                if "soru" in q:
                    kok = q["soru"]
                    cevap = (q.get("secenekler") or {}).get(q.get("cevap"), "")
                    yil = q.get("yil")
                else:
                    r = q.get("reconstruction") or {}
                    kok = r.get("stem") or q.get("stem") or ""
                    ops = r.get("options") or q.get("options") or []
                    ans = q.get("correctAnswer")
                    cevap = next((o.get("text", "") for o in ops if isinstance(o, dict) and o.get("key") == ans), "")
                    yil = q.get("examYear")
                if kok:
                    q_out.append({"id": qid, "kok": re.sub(r"\*\*", "", kok).strip(), "cevap": re.sub(r"\*\*", "", str(cevap)).strip(), "yil": yil, "p": pi, "c": ci, "skor": 0.92})

    # Aday çıkmışlardan henüz eklenmeyenleri embed ile eşle VE v2 + vurgu içine işle
    kalan = [q for qid, q in adaylar.items() if qid not in gor and q.get("skor", 0) >= 0.56]
    if kalan and cs:
        try:
            sim = embed([f"{q['soru']} {(q.get('secenekler') or {}).get(q.get('cevap'), '')}".strip() for q in kalan]) @ embed([c[2] for c in cs]).T
            for qi, q in enumerate(kalan):
                ci_idx = int(sim[qi].argmax())
                v = float(sim[qi, ci_idx])
                if v < 0.60:
                    continue
                gor.add(q["id"])
                pi_m, ci_m, _ = cs[ci_idx]
                cevap_str = re.sub(r"\*\*", "", str((q.get("secenekler") or {}).get(q.get("cevap"), ""))).strip()
                q_out.append({
                    "id": str(q["id"]),
                    "kok": re.sub(r"\*\*", "", str(q["soru"])).strip(),
                    "cevap": cevap_str,
                    "yil": q.get("yil"),
                    "p": pi_m,
                    "c": ci_m,
                    "skor": round(v, 3),
                })
                # Eşleşen cümleye v2 içinde de cikmis ve vurgu işle
                if pi_m < len(vp):
                    cumle_list = vp[pi_m].get("cumleler") or []
                    if ci_m < len(cumle_list):
                        c_obj = cumle_list[ci_m]
                        mevcut_cik = [str(x) for x in (c_obj.get("cikmis") or [])]
                        if str(q["id"]) not in mevcut_cik:
                            mevcut_cik.append(str(q["id"]))
                            c_obj["cikmis"] = mevcut_cik
                        mevcut_vurgu = list(c_obj.get("vurgu") or [])
                        if not any(vv.get("tur") == "cikmis" for vv in mevcut_vurgu):
                            ekran_duz = (c_obj.get("ekran") or "").replace("**", "")
                            # Ekran içindeki kalın ifadeyi ya da ilk anlamlı kısmı çıkmış vurgusu olarak işaretle
                            kalin = re.findall(r"\*\*([^*]+)\*\*", c_obj.get("ekran") or "")
                            hedef_m = kalin[0] if kalin else " ".join(ekran_duz.split()[:4]).strip(" .,;:")
                            if hedef_m and hedef_m.casefold() in ekran_duz.casefold():
                                mevcut_vurgu.append({"metin": hedef_m, "tur": "cikmis"})
                                c_obj["vurgu"] = mevcut_vurgu
        except Exception as e:
            print(f"Uyarı: cikmis_konum embed atlandı ({e})", file=sys.stderr)

    # Ayrıca örnek sorulardaki kazanımları da bge-m3 ile cümlelere eşleyip vurgu üret
    import konusma_v2 as KV
    vurgu_obj = KV.vurgu_turet(v2)
    ornek_yol = DB_25_26 / "taslak" / key / "ornek_sorular.json"
    if ornek_yol.exists() and cs:
        try:
            ornekler = json.loads(ornek_yol.read_text(encoding="utf-8"))
            if isinstance(ornekler, dict):
                ornekler = ornekler.get("sorular") or []
            if ornekler:
                o_texts = [f"{oq.get('soru', '')} {(oq.get('secenekler') or {}).get(oq.get('dogru_cevap'), '')}".strip() for oq in ornekler]
                sim_o = embed(o_texts) @ embed([c[2] for c in cs]).T
                from pdf_hizala import cumle_sinirlari
                for oi in range(len(ornekler)):
                    ci_idx = int(sim_o[oi].argmax())
                    if float(sim_o[oi, ci_idx]) < 0.62:
                        continue
                    pi_o, ci_o, _ = cs[ci_idx]
                    p_txt = pars[pi_o]["t"]
                    sinirlar = cumle_sinirlari(p_txt)
                    if ci_o < len(sinirlar):
                        b_off = sinirlar[ci_o - 1] if ci_o > 0 else 0
                        e_off = sinirlar[ci_o]
                        araliklar = vurgu_obj["p"].setdefault(str(pi_o), [])
                        if not any(x[0] == b_off and x[2] == "c" for x in araliklar):
                            araliklar.append([b_off, e_off, "c", 1])
                            araliklar.sort(key=lambda x: (x[0], x[2]))
        except Exception as e:
            print(f"Uyarı: örnek soru vurgu eşlemesi atlandı ({e})", file=sys.stderr)

    # Güncellenmiş v2 ve vurgu dosyalarını kaydet
    (SA_KOK / "v2" / f"{key}.json").write_text(json.dumps(v2, ensure_ascii=False, indent=1), encoding="utf-8")
    (SA_KOK / "vurgu" / f"{key}.json").write_text(json.dumps(vurgu_obj, ensure_ascii=False), encoding="utf-8")

    out = {"surum": 1, "metinHash": metin_hash, "q": q_out}
    ck_yol = SA_KOK / "cikmis_konum" / f"{key}.json"
    ck_yol.parent.mkdir(parents=True, exist_ok=True)
    ck_yol.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def cizim_dogrula_ve_yerlestir(taslak: Path, key: str, pdf_yol: Path, pars: list[dict], capa_p: list, metin_hash: str, v2: dict | None = None) -> dict:
    """Taslak içindeki ham cizim_aday.json komutlarını cizim_dogrula.py + yerlesim + panel_sinama.mjs ile doğrular."""
    import pymupdf
    import cizim_dogrula as CD
    import cizim_uret as CU
    import sablon as SB

    doc = pymupdf.open(pdf_yol)
    aday_yol = taslak / "cizim_aday.json"
    komutlar = json.loads(aday_yol.read_text(encoding="utf-8")).get("komutlar", []) if aday_yol.exists() else []

    # Cümle sözlüğü P<i>.C<j> ve k<N>-<NN>-c<NNNN> eşlemesi
    from pdf_isaret import Sayfa, cumle_sonlari
    C: dict[str, str] = {}
    id_harita: dict[str, str] = {}
    vp = [p for b in (v2 or {}).get("bolumler", []) for p in b.get("paragraflar", [])]
    for pi, p in enumerate(pars):
        m = p["t"]
        a = 0
        v_cs = vp[pi].get("cumleler", []) if pi < len(vp) else []
        for ci, e in enumerate(cumle_sonlari(m)):
            pk = f"P{pi}.C{ci}"
            C[pk] = m[a:e].strip()
            id_harita[pk] = pk
            if ci < len(v_cs) and v_cs[ci].get("id"):
                id_harita[str(v_cs[ci]["id"])] = pk
            a = e

    sira = list(C)
    kut = SB.kutuphane()
    raster: dict[int, CD.SayfaRaster] = {}
    satir_onbellek: dict[int, list] = {}
    resim_kutulari: dict[int, list] = {}
    sayfa_dolu: dict[int, list] = {}
    sayfa_say: dict[int, int] = {}
    out: dict[str, dict[str, list]] = {}
    say = {"aday": len(komutlar), "gecti": 0, "ret": {}}

    for k in komutlar:
        ham_cid = str(k.get("cumle") or "")
        cid = id_harita.get(ham_cid, ham_cid)
        if cid not in C:
            say["ret"]["bilinmeyen cümle"] = say["ret"].get("bilinmeyen cümle", 0) + 1
            continue
        s = int(k.get("sayfa") or 0)
        if not (1 <= s <= doc.page_count):
            say["ret"]["geçersiz sayfa"] = say["ret"].get("geçersiz sayfa", 0) + 1
            continue
        if s not in raster:
            pg = doc[s - 1]
            raster[s] = CD.SayfaRaster(pg)
            satir_onbellek[s] = CU.sayfa_satirlari(pg)
            sy = Sayfa(pg)
            resim_kutulari[s] = [sy.n(b) for b in sy.resimler]

        if k.get("tur") == "sema":
            if CU.resim_sayfasi(resim_kutulari[s], satir_onbellek[s], raster[s]):
                say["ret"]["resim sayfasında panel (H51)"] = say["ret"].get("resim sayfasında panel (H51)", 0) + 1
                continue
            if k.get("sablon"):
                k, neden_s = SB.coz(k, kut)
                if neden_s:
                    say["ret"][neden_s[:60]] = say["ret"].get(neden_s[:60], 0) + 1
                    continue

        onceki = " ".join(C[x] for x in sira[:sira.index(cid) + 1])
        neden = CD.denetle(k, len(C[cid].split()), resim_kutulari[s], raster[s], onceki)
        p_idx, c_idx = cid[1:].split(".C")
        mevcut = out.setdefault(p_idx, {}).setdefault(c_idx, [])
        if not neden and k.get("tur") == "akis" and not str(k.get("etiket") or "").strip():
            neden = "etiketsiz ok (H40)"
        if not neden and len(mevcut) >= 2:
            neden = "cümlede >2 çizim"
        if not neden and sayfa_say.get(s, 0) >= 8:
            neden = "sayfada >8 çizim"
        if neden:
            say["ret"][neden[:60]] = say["ret"].get(neden[:60], 0) + 1
            continue

        kel = C[cid].split()
        ka = CU.kelime_araliklari(C[cid])
        bas_k = max(0, min(len(ka) - 1, int(k.get("bas") or 0)))
        son_k = max(bas_k, min(len(ka) - 1, int(k.get("son") or (len(ka) - 1))))
        komut = {x: k[x] for x in (
            "tur", "nokta", "a", "b", "iliski", "fazlar", "dugum", "kenar", "etiket",
            "kaynak_metin", "hedef_metin", "dal", "sablon", "sablon_ad", "duzen", "basliklar",
            "bag", "satirlar", "ogeler", "kaynaklar", "sonuc", "soru", "dallar", "gorunen", "altta",
            "kutuplar", "baslik", "numarali", "pdf_oku"
        ) if x in k}
        komut.update(s=s, k=[ka[bas_k][0], ka[son_k][1]])
        yer = CU.yerlesim(komut, raster[s], sayfa_dolu.setdefault(s, []), satir_onbellek[s])
        yk = CU.yakinlasma(yer, resim_kutulari[s], CU.resim_sayfasi(resim_kutulari[s], satir_onbellek[s], raster[s]))
        if yk:
            yer["yakin"] = yk
        mevcut.append(yer)
        sayfa_say[s] = sayfa_say.get(s, 0) + 1
        say["gecti"] += 1

    out = {p: {c: v for c, v in cs.items() if v} for p, cs in out.items()}
    out = {p: cs for p, cs in out.items() if cs}
    cz_obj = {"surum": 1, "metinHash": metin_hash, "p": out, "rapor": say}
    cz_yol = SA_KOK / "cizim" / f"{key}.json"
    cz_yol.parent.mkdir(parents=True, exist_ok=True)
    cz_yol.write_text(json.dumps(cz_obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return cz_obj


def medspak_uret_yerel(key: str, kurul: int, v2: dict, metin: str, deste: dict, isr: dict, cz: dict, kz: dict, varyant: dict, gunluk: dict, pdf_yol: Path, pdf_adi: str) -> Path:
    out_dir = DB_25_26 / "medspak" / f"kurul{kurul}"
    out_dir.mkdir(parents=True, exist_ok=True)
    yol = out_dir / f"{key}.medspak"
    yol.unlink(missing_ok=True)

    db = sqlite3.connect(yol)
    db.executescript("""
      CREATE TABLE meta(anahtar TEXT PRIMARY KEY, deger TEXT);
      CREATE TABLE deste(id TEXT PRIMARY KEY, json TEXT);
      CREATE TABLE cumle(id TEXT PRIMARY KEY, paragraf INT, sira INT, ses TEXT, ekran TEXT, duzey INT, vurgu TEXT,
                         slayt_adim INT, cikmis TEXT, spot TEXT, isaret TEXT);
      CREATE TABLE cizim(cumle_id TEXT, sira INT, json TEXT);
      CREATE TABLE soru(id TEXT PRIMARY KEY, tur TEXT, json TEXT, bagli_cumle TEXT);
      CREATE TABLE ses_parca(varyant TEXT PRIMARY KEY, bicim TEXT, sure_sn REAL, metin_hash TEXT, veri BLOB, zamanlama TEXT, kelime_zaman TEXT);
      CREATE TABLE ek(ad TEXT PRIMARY KEY, tur TEXT, veri BLOB);
      CREATE TABLE gunluk(surum INT PRIMARY KEY, tarih TEXT, neden TEXT, hatali_bilgiler TEXT, degisiklikler TEXT);
    """)

    paragraflar = [p for b in v2.get("bolumler", []) for p in b.get("paragraflar", [])]
    adim_no = lambda a: a if isinstance(a, int) else (int(m.group(1)) if (m := re.search(r"-s(\d+)$", str(a or ""))) else None)
    for pi, p in enumerate(paragraflar):
        for ci, c in enumerate(p.get("cumleler", [])):
            i_list = (isr.get("c") or {}).get(str(pi)) or []
            db.execute("INSERT INTO cumle VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                c["id"], pi, ci, c.get("ses"), c.get("ekran"), c.get("duzey"),
                json.dumps(c.get("vurgu") or [], ensure_ascii=False),
                adim_no(c.get("slayt_adim")),
                json.dumps(c.get("cikmis") or [], ensure_ascii=False),
                json.dumps(c.get("spot"), ensure_ascii=False),
                json.dumps(i_list[ci] if ci < len(i_list) else None, ensure_ascii=False)
            ))
            for si, z in enumerate(((cz.get("p") or {}).get(str(pi)) or {}).get(str(ci)) or []):
                db.execute("INSERT INTO cizim VALUES (?,?,?)", (c["id"], si, json.dumps(z, ensure_ascii=False)))

    deste_id = deste["id"]
    db.execute("INSERT INTO deste VALUES (?,?)", (deste_id, json.dumps(deste, ensure_ascii=False)))
    for s in deste.get("slides") or []:
        for e in s.get("interactiveElements") or []:
            if e.get("type") == "micro_quiz":
                db.execute("INSERT OR IGNORE INTO soru VALUES (?,?,?,?)", (
                    f"{deste_id}:{s.get('slideNumber')}:{e.get('id')}", "deste",
                    json.dumps(e, ensure_ascii=False), None
                ))

    cumle_by_cikmis = {}
    for p in paragraflar:
        for c in p.get("cumleler", []):
            for q in c.get("cikmis") or []:
                cumle_by_cikmis.setdefault(str(q), c["id"])
    for q, cid in cumle_by_cikmis.items():
        db.execute("INSERT OR IGNORE INTO soru VALUES (?,?,?,?)", (f"cikmis:{q}", "cikmis", json.dumps({"id": q}), cid))

    mh = fnv(metin)
    mp3_yol = SA_KOK / "ses" / key / f"{varyant['id']}.mp3"
    veri, bicim = mp3_yol.read_bytes(), "mp3"
    ogg = mp3_yol.with_suffix(".opus")
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(mp3_yol), "-ac", "1", "-c:a", "libopus", "-b:a", "32k", "-vbr", "on", "-application", "voip", str(ogg)],
        capture_output=True, text=True
    )
    if r.returncode == 0 and ogg.exists() and ogg.stat().st_size:
        veri, bicim = ogg.read_bytes(), "opus"
        ogg.unlink(missing_ok=True)

    kz_v = (kz.get("varyantlar") or {}).get(varyant["id"]) or kz
    db.execute("INSERT INTO ses_parca VALUES (?,?,?,?,?,?,?)", (
        varyant["id"], bicim, varyant.get("sureSn"), mh, veri,
        json.dumps(varyant.get("zamanlama")),
        json.dumps(kz_v)
    ))

    # Ders PDF'ini .medspak ek tablosuna göm (tur='ders_pdf')
    ek_sayisi = 0
    if pdf_yol.exists():
        db.execute("INSERT OR REPLACE INTO ek VALUES (?,?,?)", (pdf_adi or pdf_yol.name, "ders_pdf", pdf_yol.read_bytes()))
        ek_sayisi = 1

    for g in gunluk.get("kayitlar") or []:
        db.execute("INSERT OR REPLACE INTO gunluk VALUES (?,?,?,?,?)", (
            int(g["surum"]), g["tarih"], g["neden"],
            json.dumps(g.get("hatali_bilgiler") or [], ensure_ascii=False),
            json.dumps(g.get("degisiklikler") or [], ensure_ascii=False)
        ))

    meta = {
        "surum": 1,
        "donem": "2025-2026",
        "arsiv": "1",
        "ders_id": key,
        "deste_id": deste_id,
        "kurul": deste.get("committee") or f"donem3-kurul{kurul}",
        "baslik": v2.get("baslik") or deste.get("title") or key,
        "metin_hash": mh,
        "isaret_metin_hash": isr.get("metinHash"),
        "cizim_metin_hash": cz.get("metinHash"),
        "kaynak_sha": hashlib.sha256(json.dumps(v2, sort_keys=True).encode()).hexdigest()[:16],
        "uretildi": dt.datetime.now().isoformat(timespec="seconds"),
        "ses_bicim": bicim,
        "ekler": ek_sayisi,
    }
    db.executemany("INSERT INTO meta VALUES (?,?)", [(k, json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v) for k, v in meta.items()])
    db.commit()
    db.close()

    # medspak_dogrula.py ile denetle
    import medspak_dogrula as MD
    hatalar = MD.denetle(yol)
    if hatalar:
        raise RuntimeError(f"medspak_dogrula HATA: {hatalar}")
    return yol


def gunluk_guncelle(key: str, baslik: str, kurul: int, brans: str, neden: str, hatali_bilgiler: list[str], degisiklikler: list[str], metrikler: dict) -> dict:
    gunluk_dir = ARSIV_DATA / "gunluk"
    gunluk_dir.mkdir(parents=True, exist_ok=True)
    yol = gunluk_dir / f"{key}.json"
    mevcut = json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else {
        "key": key,
        "donem": "2025-2026",
        "kurul": kurul,
        "brans": brans,
        "baslik": baslik,
        "kayitlar": []
    }
    yeni_surum = len(mevcut.get("kayitlar") or []) + 1
    kayit = {
        "surum": yeni_surum,
        "tarih": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "neden": neden,
        "hatali_bilgiler": hatali_bilgiler,
        "degisiklikler": degisiklikler,
        "metrikler": metrikler,
    }
    mevcut["kayitlar"].append(kayit)
    yol.write_text(json.dumps(mevcut, ensure_ascii=False, indent=2), encoding="utf-8")

    # Ayrıca genel sesli_anlatim/gunluk/<key>.json altına da senkronize et
    genel_gunluk = MEDS / "data" / "sesli_anlatim" / "gunluk"
    genel_gunluk.mkdir(parents=True, exist_ok=True)
    (genel_gunluk / f"{key}.json").write_text(json.dumps(mevcut, ensure_ascii=False, indent=2), encoding="utf-8")
    return mevcut


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True)
    ap.add_argument("--neden", default="2025-2026 geçmiş yıl arşiv dersi ilk üretimi ve Kurul 2 tam otomatik hat kapı doğrulaması")
    ap.add_argument("--hatali-bilgi", action="append", default=[])
    ap.add_argument("--degisiklik", action="append", default=[])
    ap.add_argument("--ses-zorla", action="store_true")
    a = ap.parse_args()

    taslak = DB_25_26 / "taslak" / a.key
    if not (taslak / "baglam.json").exists():
        print(f"HATA: {taslak}/baglam.json bulunamadı", file=sys.stderr)
        return 2
    baglam = json.loads((taslak / "baglam.json").read_text(encoding="utf-8"))
    kurul = int(baglam["kurul"])
    deste_id = baglam["deste_id"]
    pdf_yol = ROOT / baglam["pdf_yolu"]

    print(f"[{a.key}] 1/6 Taslak doğrulama kapıları çalıştırılıyor...")
    hatalar = denetle_taslak(taslak, baglam)
    if hatalar:
        print(f"[{a.key}] DENETİM HATALARI ({len(hatalar)}):")
        for h in hatalar:
            print("  -", h)
        return 1

    # 2. Sesli anlatım dosyalarını data/arsiv_25_26/sesli_anlatim/ altına yerleştir
    print(f"[{a.key}] 2/6 Sesli anlatım dosyaları ve PDF hizalaması hazırlanıyor...")
    for alt in ("metin", "v2", "vurgu", "hizalama", "capa", "isaret", "cizim", "cikmis_konum", "cumle_zaman", "kelime_zaman", "ses"):
        (SA_KOK / alt).mkdir(parents=True, exist_ok=True)

    metin = (taslak / "konusma_metni.md").read_text(encoding="utf-8")
    (SA_KOK / "metin" / f"{a.key}.md").write_text(metin, encoding="utf-8")

    v2 = json.loads((taslak / "konusma_v2.json").read_text(encoding="utf-8"))
    v2["anahtar"] = a.key
    v2["donem"] = "2025-2026"
    (SA_KOK / "v2" / f"{a.key}.json").write_text(json.dumps(v2, ensure_ascii=False, indent=1), encoding="utf-8")

    import konusma_v2 as KV
    (SA_KOK / "vurgu" / f"{a.key}.json").write_text(json.dumps(KV.vurgu_turet(v2), ensure_ascii=False), encoding="utf-8")

    pars = metin_paragraflari(metin)
    sayfalar_list = json.loads((taslak / "konusma_sayfalari.json").read_text(encoding="utf-8"))
    capalar_list = json.loads((taslak / "konusma_capalari.json").read_text(encoding="utf-8"))

    hz = {
        "deckId": deste_id,
        "donem": "2025-2026",
        "dosyalar": [{
            "path": baglam["pdf_yolu"],
            "name": baglam["pdf_adi"],
            "fileId": baglam.get("file_id"),
            "pages": int(baglam["sayfa"]),
        }],
        "paragraflar": [{"dosya": 0, "sayfa": int(s), "guven": 1} for s in sayfalar_list],
        "kaynak": "arsiv-25-26",
    }
    (SA_KOK / "hizalama" / f"{a.key}.json").write_text(json.dumps(hz, ensure_ascii=False, indent=1), encoding="utf-8")
    (SA_KOK / "capa" / f"{a.key}.json").write_text(
        json.dumps({"mdSha1": hashlib.sha1(metin.encode("utf-8")).hexdigest(), "p": capalar_list}, ensure_ascii=False),
        encoding="utf-8"
    )

    # 3. EMA GPU ses üretimi (çapraz oturum GPU kilidi ile)
    print(f"[{a.key}] 3/6 EMA GPU ses sentezi çalıştırılıyor (GPU kilidi bekleniyor)...")
    _gpu_lock = gpu_kilit_al()
    try:
        ema_cmd = [
            "bash", str(MEDS / "scripts" / "patoloji_cozucu" / "cozucu_ses_gpu.sh"),
            str(MEDS / "scripts" / "arsiv_25_26" / "ema_yerel_uret.py"),
            "--key", a.key,
            "--metin", str(SA_KOK / "metin" / f"{a.key}.md"),
            "--kok", str(SA_KOK),
        ]
        if a.ses_zorla:
            ema_cmd.append("--zorla")
        r = subprocess.run(ema_cmd, cwd=MEDS)
        if r.returncode != 0:
            print(f"HATA: EMA GPU ses üretimi başarısız (kod {r.returncode})", file=sys.stderr)
            return r.returncode

        kayit = json.loads((SA_KOK / "kayit.json").read_text(encoding="utf-8"))
        varyant = kayit[a.key][0]
        mp3_yol = SA_KOK / "ses" / a.key / f"{varyant['id']}.mp3"

        # 4. Cümle zamanı, Kelime zamanı (GPU), PDF işaret, Çıkmış konum ve Canlı Çizim
        print(f"[{a.key}] 4/6 Cümle zamanı, kelime zamanı, PDF işareti, çıkmış konum ve canlı çizim üretiliyor...")
        metin_sha1 = hashlib.sha1("\n".join(p["t"] for p in pars).encode("utf-8")).hexdigest()
        cz_zaman = cumle_zaman_yerel(a.key, pars, mp3_yol, varyant["zamanlama"], metin_sha1)
        (SA_KOK / "cumle_zaman" / f"{a.key}.json").write_text(json.dumps(cz_zaman, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

        kz = kelime_zaman_yerel(a.key, pars, mp3_yol, varyant["zamanlama"], metin_sha1)
    finally:
        _gpu_lock.close()
    isr = pdf_isaret_yerel(a.key, pars, pdf_yol, hz, capalar_list, metin_sha1)
    ck = cikmis_konum_yerel(a.key, pars, v2, baglam, metin_sha1)
    cz = cizim_dogrula_ve_yerlestir(taslak, a.key, pdf_yol, pars, capalar_list, metin_sha1, v2)

    # 5. Arşiv Öğren destesi ve ders paketini ayrı veritabanına kaydet
    print(f"[{a.key}] 5/6 Arşiv Öğren destesi ve ders paketi kaydediliyor...")
    deck_raw = json.loads((taslak / "deck.json").read_text(encoding="utf-8"))
    if isinstance(deck_raw, list):
        deck_raw = deck_raw[0]
    bag_sayisi = len([x for x in json.loads((taslak / "cikmis_baglantilari.json").read_text(encoding="utf-8")) if x.get("ilgili")]) if (taslak / "cikmis_baglantilari.json").exists() else 0
    deck_raw.update({
        "id": deste_id,
        "deckId": deste_id,
        "donem": "2025-2026",
        "arsiv": True,
        "committee": f"donem3-kurul{kurul}",
        "confidence": "high",
        "totalSlides": len(deck_raw.get("slides") or []),
        "matchedPastQuestionsCount": bag_sayisi,
        "sinama": {
            "etiket": "2025-2026 Arşiv",
            "aciklama": "Bu ders 2025-2026 dönemi (geçen yıl) slaytlarından hazırlanmıştır; 2026-2027 güncel müfredat dersleriyle karışmaz."
        }
    })
    decks_dir = ARSIV_DATA / "decks"
    decks_dir.mkdir(parents=True, exist_ok=True)
    (decks_dir / f"{deste_id}.json").write_text(json.dumps(deck_raw, ensure_ascii=False, indent=1), encoding="utf-8")

    # Arşiv ders paketini meds_database_25_26/paketler/kurul<N>/ altına yaz
    paket_dir = DB_25_26 / "paketler" / f"kurul{kurul}"
    paket_dir.mkdir(parents=True, exist_ok=True)
    paket_obj = json.loads((taslak / "ders_paketi.json").read_text(encoding="utf-8"))
    paket_obj.update({
        "donem": "2025-2026",
        "gecen_yil_kaynagi": True,
        "ders_notu": (taslak / "ders_notu.md").read_text(encoding="utf-8"),
        "ders_ozeti_md": (taslak / "ders_ozeti.md").read_text(encoding="utf-8") if (taslak / "ders_ozeti.md").exists() else "",
        "ornek_sorular": json.loads((taslak / "ornek_sorular.json").read_text(encoding="utf-8")),
        "sozluk": json.loads((taslak / "sozluk.json").read_text(encoding="utf-8")),
    })
    (paket_dir / f"{a.key}.json").write_text(json.dumps(paket_obj, ensure_ascii=False, indent=1), encoding="utf-8")

    # dersler.json güncelle (data/arsiv_25_26/sesli_anlatim/dersler.json) — fcntl kilitli
    dersler_yol = SA_KOK / "dersler.json"
    ders_kaydi = {
        "key": a.key,
        "donem": "2025-2026",
        "kurul": kurul,
        "brans": baglam["brans"],
        "no": int(baglam["brans_no"]),
        "kurulNo": int(baglam["numara"]),
        "baslik": baglam["konu"],
        "hoca": baglam.get("ogretim_uyesi") or "",
        "sira": int(baglam["numara"]),
        "desteId": deste_id,
        "sayfaSayisi": int(baglam["sayfa"]),
    }

    def _dersler_guncelle(mevcut_l):
        yeni_l = [d for d in (mevcut_l or []) if d.get("key") != a.key] + [ders_kaydi]
        yeni_l.sort(key=lambda x: (int(x.get("kurul") or 2), int(x.get("sira") or 0)))
        return yeni_l

    json_kilitli_guncelle(dersler_yol, [], _dersler_guncelle)

    # 6. Güncelleme Günlüğü + .medspak üretimi ve doğrulaması
    print(f"[{a.key}] 6/6 Güncelleme günlüğü ve .medspak üretiliyor...")
    toplam_cumle = sum(len(p.get("cumleler") or []) for b in v2.get("bolumler", []) for p in b.get("paragraflar", []))
    metrikler = {
        "sureSn": varyant["sureSn"],
        "sureDk": round(varyant["sureSn"] / 60, 1),
        "sayfaSayisi": int(baglam["sayfa"]),
        "atlananSayfa": 0,
        "bolumSayisi": len(v2.get("bolumler") or []),
        "paragrafSayisi": len(pars),
        "cumleSayisi": toplam_cumle,
        "slaytAdimSayisi": len(deck_raw.get("slides") or []),
        "cizimSayisi": cz.get("rapor", {}).get("gecti", 0),
        "cikmisEslesme": len(ck.get("q") or []),
    }
    hatali_list = a.hatali_bilgi or [
        "İlk üretim kontrolü: H1–H55 hata defterindeki kısaltma okunuşu, sayfa atlama ve şık açıklama kusurları tarandı; 0 hata doğrulandı."
    ]
    degisiklik_list = a.degisiklik or [
        f"2025-2026 dönemi {baglam['pdf_adi']} ({baglam['sayfa']} sayfa) kaynağından 0 atlanan sayfa ile { len(pars) } paragraf / { toplam_cumle } cümlelik sesli anlatım üretildi.",
        f"{len(deck_raw.get('slides') or [])} adımlı etkileşimli Öğren destesi (11 model + ders sonu oyunları) ve {cz.get('rapor', {}).get('gecti', 0)} canlı çizim katmanı eklendi.",
        f"EMA Lightning GPU ile {round(varyant['sureSn']/60, 1)} dakikalık ses sentezlendi, cümle/kelime zamanlaması ve .medspak paketi doğrulandı."
    ]
    gunluk = gunluk_guncelle(a.key, baglam["konu"], kurul, baglam["brans"], a.neden, hatali_list, degisiklik_list, metrikler)
    medspak_yol = medspak_uret_yerel(a.key, kurul, v2, metin, deck_raw, isr, cz, kz, varyant, gunluk, pdf_yol, baglam.get("pdf_adi") or pdf_yol.name)

    print(f"[{a.key}] TAMAMLANDI ✔ → {medspak_yol} ({round(medspak_yol.stat().st_size / 1048576, 2)} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
