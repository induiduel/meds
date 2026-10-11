"""Tek bir yeni ders PDF'ini işler: kaynak metin + bağlam paketi → Claude (abonelik, başsız) → denetim → taslak + bildirim.

Claude yalnız taslak/<is_id>/ klasörüne yazar (kod /app salt-okunur). Kota dolarsa oturum kimliği saklanır; sonraki
denemede aynı oturum "kaldığın yerden" sürdürülür (iş baştan yapılmaz, kota boşa harcanmaz).
"""
from __future__ import annotations

import difflib
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ayarlar import API, APP, CLAUDE_BIN, CLAUDE_MODEL, DATABASE, TASLAK, log, oku, yaz  # noqa: E402
from cikar import pdf_metni  # noqa: E402

sys.path.insert(0, str(APP / "scripts" / "agents"))
TALIMAT = Path(__file__).resolve().parent / "TALIMAT.md"
KOTA_RE = re.compile(r"usage limit|rate.?limit|limit (?:reached|exceeded)|quota|\b429\b|overloaded|credit balance", re.I)
_FOLD = str.maketrans("çğıöşüâîûÇĞİÖŞÜÂÎÛ", "cgiosuaiucgiosuaiu")


def fold(s: str) -> str:
    s = str(s).replace("İ", "i").replace("I", "ı").lower().translate(_FOLD)
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", fold(s)).strip("-")[:50].strip("-")


# ------------------------------------------------------------------ bağlam paketi
def program_eslesmesi(yol: str) -> dict:
    """Ders programındaki konulardan bu PDF'e en uygun olanı (parse_ders_programi.match_pdfs ile aynı puanlama)."""
    from parse_ders_programi import match_pdfs  # noqa: E402

    parts = Path(yol).parts
    kurul = next((int(m.group(1)) for p in parts if (m := re.match(r"Kurul\s*(\d)", p, re.I))), None)
    stem = re.sub(r"^\s*\d+\s*[\)\.\-]\s*", "", Path(yol).stem)
    pdf = {"path": yol, "kurul": kurul, "ders_klasoru": parts[-2] if len(parts) >= 2 else "", "ad": Path(yol).stem,
           "fold": fold(stem)}
    prog = oku(DATABASE / "taxonomy" / "donem3_ders_programi.json", {})
    en_iyi, skor = None, 0.0
    for k in prog.get("kurullar") or []:
        for konu in k.get("konular") or []:
            for c in match_pdfs(konu, [pdf]):
                if c["skor"] > skor:
                    en_iyi, skor = konu, c["skor"]
    out = {"kurul": kurul, "ders_klasoru": pdf["ders_klasoru"], "skor": skor,
           "guven": "yuksek" if skor >= 0.75 else "orta" if skor >= 0.55 else "dusuk"}
    if en_iyi:
        out.update({k: en_iyi.get(k) for k in ("ders", "konu", "ogretim_uyesi", "tarih", "hafta", "saat")})
        out["kurul"] = en_iyi.get("kurul") or kurul
    else:
        out.update({"ders": pdf["ders_klasoru"], "konu": stem})
    return out


def sonraki_numara(kurul: int) -> int:
    decks = oku(APP / "src" / "data" / "interactive_learning_decks.json", [])
    decks = decks if isinstance(decks, list) else decks.get("decks", [])
    nums = [int(m.group(1)) for d in decks if (m := re.match(rf"k{kurul}p-k{kurul}-(\d+)-", d.get("id", "")))]
    for t in TASLAK.glob("*/baglam.json"):  # henüz yayınlanmamış taslaklar da numara tutar
        b = oku(t, {})
        if b.get("kurul") == kurul and b.get("numara"):
            nums.append(int(b["numara"]))
    return max(nums, default=0) + 1


def kazanimlar(kurul: int, konu: str) -> list[str]:
    k = oku(APP / "src" / "data" / "kazanimlar" / f"k{kurul}.json", {})
    best, sc = None, 0.0
    for d in k.get("dersler") or []:
        for kn in d.get("konular") or []:
            r = difflib.SequenceMatcher(None, fold(konu), fold(kn.get("konu") or kn.get("baslik") or "")).ratio()
            if r > sc:
                best, sc = kn, r
    if not best or sc < 0.6:
        return []
    return [x.get("metin") for x in best.get("kazanimlar") or [] if x.get("metin")]


def cikmis_adaylari(metin: str, kurul: int | None, en_cok: int = 40) -> list[dict]:
    """Ders metninin parçalarıyla sitenin benzer-soru aramasını (BM25 + bge-m3) sorgular; tekrar eden adaylar öne çıkar."""
    parcalar = [p.split("\n", 1)[-1].strip() for p in metin.split("=== SAYFA ")]
    parcalar = [" ".join(p.split())[:700] for p in parcalar if len(p) > 120]
    grup = [" ".join(parcalar[i:i + 3])[:1000] for i in range(0, len(parcalar), 3)][:30]
    toplam: dict[str, dict] = {}
    for g in grup:
        body = {"text": g, "limit": 8}
        if kurul:
            body["committeeId"] = f"donem3-kurul{kurul}"
        try:
            req = urllib.request.Request(f"{API}/api/past-questions/similar", json.dumps(body).encode(),
                                         {"Content-Type": "application/json"})
            for r in json.load(urllib.request.urlopen(req, timeout=60)).get("results") or []:
                e = toplam.setdefault(r["id"], {"id": r["id"], "kok": (r.get("stem") or r.get("title") or "")[:400],
                                                "secenekler": [o.get("text") for o in r.get("options") or []],
                                                "cevap": r.get("correctAnswer") or r.get("answer"), "puan": 0.0, "kez": 0})
                e["puan"] = max(e["puan"], float(r.get("score") or 0))
                e["kez"] += 1
        except Exception as ex:  # noqa: BLE001
            log(f"benzer soru araması başarısız: {ex}")
    return sorted(toplam.values(), key=lambda e: (-e["kez"], -e["puan"]))[:en_cok]


def baglam_hazirla(j: dict, d: Path, metin: str, bilgi: dict) -> dict:
    es = program_eslesmesi(j["yol"])
    kurul = es.get("kurul") or 0
    sozluk = oku(APP / "src" / "data" / "medical_glossary.json", {})
    hast = oku(APP / "src" / "data" / "diseases.json", [])
    decks = oku(APP / "src" / "data" / "interactive_learning_decks.json", [])
    # Bu konunun destesi zaten varsa (hoca PDF'i güncelledi / yeniden yükledi): yeni numara açma, mevcut dersi güncelle
    konu_f = fold(es.get("konu") or Path(j["yol"]).stem)
    def benzerlik(d: dict) -> float:  # başlık ya da kimlikteki konu kısmı (k1p-k1-02-patolojiye-giris → patolojiye giris)
        kimlik = re.sub(r"^k\d+p-k\d+-\d+-", "", d.get("id", "")).replace("-", " ")
        return max(difflib.SequenceMatcher(None, konu_f, fold(d.get("title", ""))).ratio(),
                   difflib.SequenceMatcher(None, konu_f, kimlik).ratio())

    mevcut = max(((benzerlik(d), d)
                  for d in (decks if isinstance(decks, list) else []) if d.get("id", "").startswith(f"k{kurul}p-")),
                 key=lambda x: x[0], default=(0.0, None))
    if mevcut[1] is not None and mevcut[0] >= 0.85:
        deste_id = mevcut[1]["id"]
        ders_id = deste_id.split("-", 1)[1]
        n = int(re.match(rf"k{kurul}-(\d+)-", ders_id).group(1))
        mod = "guncelleme"
    else:
        n = sonraki_numara(kurul) if kurul else 0
        ders_id = f"k{kurul}-{n:02d}-{slug(es.get('konu') or Path(j['yol']).stem)}"
        deste_id = f"k{kurul}p-{ders_id}"
        mod = "yeni"
    b = {
        "is_id": j["is_id"], "pdf_yolu": j["yol"], "pdf_adi": Path(j["yol"]).name, "yil": j.get("yil"),
        "uyari": j.get("uyari", ""), "sayfa": bilgi["sayfa"], "ocr_sayfalar": bilgi["ocr_sayfalar"],
        "program": es, "kurul": kurul, "numara": n, "ders_id": ders_id, "deste_id": deste_id, "mod": mod,
        "mevcut_eslesme": round(mevcut[0], 3),
        "committeeId": f"donem3-kurul{kurul}" if kurul else "",
        "mevcut_dersler": [d.get("title") for d in (decks if isinstance(decks, list) else []) if d.get("id", "").startswith(f"k{kurul}p-")],
        "kazanimlar": kazanimlar(kurul, es.get("konu") or "") if kurul else [],
        "sozluk_terimleri": sorted(sozluk.keys()) if isinstance(sozluk, dict) else [],
        "hastaliklar": {h.get("name"): h.get("id") for h in (hast if isinstance(hast, list) else []) if h.get("name")},
        "cikmis_adaylari": cikmis_adaylari(metin, kurul or None),
    }
    yaz(d / "baglam.json", b)
    return b


# ------------------------------------------------------------------ Claude
def claude(d: Path, istem: str, oturum: str | None = None, sure: int = 3 * 3600) -> dict:
    cmd = [CLAUDE_BIN, "-p", istem, "--output-format", "json", "--permission-mode", "bypassPermissions",
           "--add-dir", str(APP)]
    if oturum:
        cmd += ["--resume", oturum]
    if CLAUDE_MODEL:
        cmd += ["--model", CLAUDE_MODEL]
    try:
        r = subprocess.run(cmd, cwd=d, capture_output=True, text=True, timeout=sure)
    except subprocess.TimeoutExpired:
        return {"hata": "zaman aşımı", "kota": False}
    ham = (r.stdout or "") + (r.stderr or "")
    try:
        js = json.loads(r.stdout)
    except Exception:  # noqa: BLE001
        js = {}
    oturum_id = js.get("session_id") or oturum
    if oturum_id:
        yaz(d / "oturum.json", {"session_id": oturum_id, "zaman": time.time()})
    sonuc_metni = str(js.get("result") or "")
    hata = js.get("is_error") or r.returncode != 0
    return {"hata": ham[-600:] if hata else "", "kota": bool(hata and KOTA_RE.search(ham)), "sonuc": sonuc_metni,
            "oturum": oturum_id, "maliyet": js.get("total_cost_usd"), "tur": js.get("num_turns")}


def bildir(baslik: str, ayrinti: str, hedef: str):
    body = {"targetType": "pipeline", "targetId": hedef, "reason": baslik, "details": ayrinti, "reportedBy": "Ders işçisi"}
    h = {"Content-Type": "application/json"}
    if os.environ.get("MEDSORU_API_PASSWORD"):
        h["X-API-Password"] = os.environ["MEDSORU_API_PASSWORD"]
    try:
        urllib.request.urlopen(urllib.request.Request(f"{API}/api/universal-report", json.dumps(body).encode(), h), timeout=30)
    except Exception as e:  # noqa: BLE001
        log(f"bildirim gönderilemedi: {e}")


def denetle(d: Path) -> dict:
    subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "denetle.py"), str(d)], capture_output=True)
    return oku(d / "denetim.json", {"hata": 999, "hatalar": ["denetim çalışmadı"]})


# ------------------------------------------------------------------ ana akış
def isle(j: dict) -> dict:
    if not (os.environ.get("CLAUDE_CODE_OAUTH_TOKEN") or (Path(os.environ.get("HOME", "~")).expanduser() / ".claude").exists()):
        return {"durum": "kota", "mesaj": "Claude anahtarı yok (deploy/oracle/isci-token-yukle.sh)"}
    d = TASLAK / j["is_id"]
    d.mkdir(parents=True, exist_ok=True)
    if not (d / "kaynak.md").exists():
        metin, bilgi = pdf_metni(Path(j["tam"]))
        if bilgi["karakter"] < 300:
            return {"durum": "hata", "mesaj": "PDF'ten okunabilir metin çıkmadı"}
        (d / "kaynak.md").write_text(metin, encoding="utf-8")
        yaz(d / "kaynak_bilgi.json", bilgi)
    if not (d / "baglam.json").exists():
        b = baglam_hazirla(j, d, (d / "kaynak.md").read_text(encoding="utf-8"), oku(d / "kaynak_bilgi.json", {}))
        log(f"bağlam: {b['ders_id']} · eşleşme {b['program'].get('guven')} ({b['program'].get('skor')}) · "
            f"{len(b['cikmis_adaylari'])} çıkmış aday · {len(b['kazanimlar'])} kazanım")
    b = oku(d / "baglam.json", {})

    onceki = oku(d / "oturum.json", {}).get("session_id")
    istem = (f"Talimat dosyası: {TALIMAT}. Önce onu ve çalışma dizinindeki baglam.json + kaynak.md'yi oku, sonra "
             "talimattaki iş sırasıyla tüm çıktıları üret ve denetle.py 0 HATA olana kadar düzelt.")
    if onceki:
        istem = "Kota/kesinti nedeniyle yarım kaldın. Klasördeki mevcut dosyalara bakıp kaldığın yerden devam et; " + istem
    r = claude(d, istem, onceki)
    if r["kota"]:
        return {"durum": "kota", "mesaj": "abonelik kotası doldu; oturum saklandı, sonra sürecek"}
    if r["hata"] and not (d / "deck.json").exists():
        return {"durum": "hata", "mesaj": r["hata"]}

    den = denetle(d)
    for tur in range(2):  # en çok 2 düzeltme turu, aynı oturumda
        if not den.get("hata"):
            break
        hatalar = "\n".join(den.get("hatalar", [])[:60])
        r = claude(d, f"Denetleyici {den['hata']} HATA buldu. Hepsini düzelt (alıntısı kaynakta olmayan kaydı ya kaynaktan "
                      f"doğru alıntıyla düzelt ya da sil), sonra denetle.py'yi yeniden çalıştır:\n{hatalar}", r.get("oturum"))
        if r["kota"]:
            return {"durum": "kota", "mesaj": "düzeltme turunda kota doldu"}
        den = denetle(d)

    s = den.get("sayilar", {})
    ozet = (f"{b.get('program', {}).get('ders')} · {b.get('program', {}).get('konu')} · {s.get('slayt', 0)} slayt · "
            f"{s.get('soru', 0)} soru · {s.get('terim', 0)} terim · {s.get('hastalik', 0)} hastalık · {s.get('havuz', 0)} bilgi · "
            f"{s.get('bag', 0)} çıkmış bağı · denetim {den.get('hata', '?')} HATA")
    yaz(d / "durum.json", {"durum": "onay_bekliyor", "ozet": ozet, "denetim_hata": den.get("hata"), "zaman": time.time(),
                           "deste_id": b.get("deste_id"), "ders_id": b.get("ders_id")})
    bildir("Yeni ders işlendi — onay bekliyor", ozet + (f"\nUyarı: {b['uyari']}" if b.get("uyari") else ""), b.get("ders_id", j["is_id"]))
    log(f"taslak hazır: {j['is_id']} → {ozet}")
    return {"durum": "taslak", "mesaj": ozet}
