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
# Kota ya da kimlik sorunu: iş "bekle" olur, deneme hakkı harcanmaz (anahtar yenilenince kaldığı yerden sürer)
KOTA_RE = re.compile(r"usage limit|rate.?limit|limit (?:reached|exceeded)|quota|\b429\b|overloaded|credit balance|"
                     r"\b401\b|authenticat|invalid.*token|oauth", re.I)
_FOLD = str.maketrans("çğıöşüâîûÇĞİÖŞÜÂÎÛ", "cgiosuaiucgiosuaiu")


def fold(s: str) -> str:
    s = str(s).replace("İ", "i").replace("I", "ı").lower().translate(_FOLD)
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", fold(s)).strip("-")[:50].strip("-")


# ------------------------------------------------------------------ bağlam paketi
def _embed(metinler: list[str]) -> list[list[float]] | None:
    try:
        req = urllib.request.Request(os.environ.get("MEDS_EMBED_URL", "http://meds-embed:8094/embed"),
                                     json.dumps({"texts": metinler, "kind": "query"}).encode(), {"Content-Type": "application/json"})
        return json.load(urllib.request.urlopen(req, timeout=180))["vectors"]
    except Exception as e:  # noqa: BLE001
        log(f"anlam benzerliği hesaplanamadı (embed): {e}")
        return None


def _baslik_alani(metin: str) -> str:
    """PDF'in ilk 2 sayfasındaki anlamlı satırlar (kapak/başlık; hoca adı, uyarı satırları hariç)."""
    satirlar = []
    for sayfa in metin.split("=== SAYFA ")[1:3]:
        for x in sayfa.split("\n")[1:]:
            x = x.strip()
            if 4 <= len(x) <= 120 and not re.search(r"dr\.|prof|doç|üyesi|unutmay|telif|paylaş|şahsınıza|amaçlıdır|gösteriniz|platform|hassasiyet|fikri mülkiyet", x, re.I):
                satirlar.append(x)
    return " ".join(satirlar[:8])


def program_eslesmesi(yol: str, metin: str = "") -> dict:
    """PDF'i ders programındaki AYNI KURULUN konularından birine eşler. Tarih KULLANILMAZ (konu kurul içinde başka gün
    işlenebilir; tarih yalnız bilgi). Puan = ad benzerliği (parse_ders_programi puanlaması) + kapak başlığı benzerliği +
    içerik anlam benzerliği (bge-m3, ilk sayfalar ↔ konu adı). Güven, puan VE ikinci adaya fark ile belirlenir."""
    parts = Path(yol).parts
    kurul = next((int(m.group(1)) for p in parts if (m := re.match(r"Kurul\s*(\d)", p, re.I))), None)
    ders_klasoru = parts[-2] if len(parts) >= 2 else ""
    stem = re.sub(r"^\s*\d+\s*[\)\.\-]\s*", "", Path(yol).stem).strip()
    stem = re.sub(r"^[\s'\"“”‘’]+|[\s'\"“”‘’.]+$", "", stem).replace("_", " ").strip()   # 'BAŞLIK.' → BAŞLIK
    if stem.isupper():
        stem = stem.title()
    prog = oku(DATABASE / "taxonomy" / "donem3_ders_programi.json", {})
    konular = [x for k in prog.get("kurullar") or [] if kurul is None or k.get("kurul") == kurul
               for x in k.get("konular") or [] if x.get("tur", "ders") == "ders" and x.get("konu")]
    out = {"kurul": kurul, "ders_klasoru": ders_klasoru, "pdf_basligi": stem, "skor": 0.0, "guven": "dusuk",
           "ders": ders_klasoru, "konu": stem, "programda": False}
    if not konular:
        return out
    baslik = _baslik_alani(metin)
    giris = " ".join(metin.split("=== SAYFA ")[1:5])[:1800] if metin else ""

    def ad_puani(konu: dict) -> float:
        t, pf = fold(konu["konu"]), fold(stem)
        r = difflib.SequenceMatcher(None, t, pf).ratio()
        tw, pw = set(t.split()), set(pf.split())
        jac = len(tw & pw) / max(1, len(tw | pw))
        ayni = bool(konu.get("ders")) and fold(konu["ders"]) == fold(ders_klasoru)
        return min(1.0, 0.6 * r + 0.4 * jac + (0.1 if ayni else 0))

    def baslik_puani(konu: dict) -> float:
        if not baslik:
            return 0.0
        t = fold(konu["konu"])
        return 1.0 if t and t in fold(baslik) else difflib.SequenceMatcher(None, t, fold(baslik)[: len(t) + 20]).ratio()

    anlam = [0.0] * len(konular)
    v = _embed([giris or stem] + [k["konu"] for k in konular]) if (giris or stem) else None
    if v:
        import math
        q = v[0]
        for i, kv in enumerate(v[1:]):
            anlam[i] = sum(a * b for a, b in zip(q, kv)) / (math.sqrt(sum(a * a for a in q)) * math.sqrt(sum(b * b for b in kv)) or 1)

    puanlar = []
    for i, konu in enumerate(konular):
        ad, bs = ad_puani(konu), baslik_puani(konu)
        ayni_ders = bool(konu.get("ders")) and fold(konu["ders"]) == fold(ders_klasoru)
        # bge-m3 kosinüsü ~0.3–0.8 aralığında; 0.45 altı ilgisiz sayılır
        an = max(0.0, min(1.0, (anlam[i] - 0.45) / 0.35))
        top = 0.45 * ad + 0.25 * bs + 0.30 * an + (0.05 if ayni_ders else 0)
        puanlar.append((round(top, 3), konu, {"ad": round(ad, 3), "baslik": round(bs, 3), "anlam": round(anlam[i], 3)}))
    puanlar.sort(key=lambda x: -x[0])
    (s1, k1, d1), s2 = puanlar[0], (puanlar[1][0] if len(puanlar) > 1 else 0.0)
    fark = s1 - s2
    guven = "yuksek" if (s1 >= 0.70 and fark >= 0.10) else "orta" if (s1 >= 0.50 and fark >= 0.05) else "dusuk"
    out.update({"skor": s1, "fark": round(fark, 3), "guven": guven, "ayrinti": d1,
                "adaylar": [{"konu": k["konu"], "ders": k.get("ders"), "tarih": k.get("tarih"), "puan": sc} for sc, k, _ in puanlar[:3]]})
    if guven != "dusuk":
        out.update({k: k1.get(k) for k in ("ders", "konu", "ogretim_uyesi", "tarih", "hafta", "saat")})
        out["kurul"] = k1.get("kurul") or kurul
        out["programda"] = True
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


def _kokler(s: str) -> set[str]:
    return {w[:5] for w in fold(s).split() if len(w) >= 3 and w not in {"ve", "ile", "icin", "bir", "veya"}}


def kazanimlar(kurul: int, konu: str) -> list[str]:
    """Kazanım dosyasında bu konunun kazanımları. Yalnız konu adının anlamlı kelimelerinin HEPSİ tutarsa (harf benzerliği
    yetmez: 'Gebelik Hastalıkları' ≠ 'Memenin Benign Hastalıkları'). Bulunamazsa boş: Claude kazanımları dersten yazar."""
    k = oku(APP / "src" / "data" / "kazanimlar" / f"k{kurul}.json", {})
    hedef = _kokler(konu)
    best, sc = None, 0.0
    for d in k.get("dersler") or []:
        for kn in d.get("konular") or []:
            ad = kn.get("konu") or kn.get("baslik") or ""
            a = _kokler(ad)
            if not hedef or not a or not (hedef <= a or a <= hedef):
                continue
            r = difflib.SequenceMatcher(None, fold(konu), fold(ad)).ratio()
            if r > sc:
                best, sc = kn, r
    if not best or sc < 0.75:
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
    kz = j.get("konu_zorla")
    if kz:  # kapsam tespitinden gelen konu (çok konulu PDF'te her alt iş kendi konusunu taşır)
        es = {"kurul": kz.get("kurul"), "ders": kz.get("ders"), "konu": kz.get("konu"), "ogretim_uyesi": kz.get("ogretim_uyesi"),
              "tarih": kz.get("tarih"), "programda": bool(kz.get("programda")), "guven": kz.get("guven") or "orta",
              "pdf_basligi": kz.get("konu"), "ders_klasoru": Path(j["yol"]).parts[-2] if len(Path(j["yol"]).parts) > 1 else "",
              "sayfa_araligi": [kz.get("sayfa_bas"), kz.get("sayfa_bit")], "yontem": kz.get("yontem")}
    else:
        es = program_eslesmesi(j["yol"], metin)
    kurul = es.get("kurul") or 0
    sozluk = oku(APP / "src" / "data" / "medical_glossary.json", {})
    hast = oku(APP / "src" / "data" / "diseases.json", [])
    decks = oku(APP / "src" / "data" / "interactive_learning_decks.json", [])
    # Bu konunun destesi zaten varsa (hoca PDF'i güncelledi / yeniden yükledi) yeni numara açma, mevcut dersi güncelle.
    # GÜVENLİK: güncelleme yalnız (a) PDF'in KENDİ adı/başlığı aynı desteyi gösteriyorsa ve (b) program eşleşmesi varsa o da
    # aynı desteyi gösteriyorsa seçilir. Aksi halde yeni taslak + uyarı (yanlış dersin üzerine yazılmasın).
    def benzerlik(ad: str, d: dict) -> float:  # başlık ya da kimlikteki konu kısmı (k1p-k1-02-patolojiye-giris)
        kimlik = re.sub(r"^k\d+p-k\d+-\d+-", "", d.get("id", "")).replace("-", " ")
        f = fold(ad)
        return max(difflib.SequenceMatcher(None, f, fold(d.get("title", ""))).ratio(), difflib.SequenceMatcher(None, f, kimlik).ratio())

    adaylar = [d for d in (decks if isinstance(decks, list) else []) if d.get("id", "").startswith(f"k{kurul}p-")]
    pdf_adi = es.get("pdf_basligi") or Path(j["yol"]).stem
    pdf_en = max(((benzerlik(pdf_adi, d), d) for d in adaylar), key=lambda x: x[0], default=(0.0, None))
    prg_en = (max(((benzerlik(es["konu"], d), d) for d in adaylar), key=lambda x: x[0], default=(0.0, None))
              if es.get("programda") else (0.0, None))
    mevcut = pdf_en
    uyarilar = [j.get("uyari")] if j.get("uyari") else []
    ayni = prg_en[1] is None or (pdf_en[1] is not None and prg_en[1]["id"] == pdf_en[1]["id"])
    if pdf_en[1] is not None and pdf_en[0] >= 0.85 and ayni:
        deste_id = pdf_en[1]["id"]
        ders_id = deste_id.split("-", 1)[1]
        n = int(re.match(rf"k{kurul}-(\d+)-", ders_id).group(1))
        mod = "guncelleme"
    else:
        if pdf_en[1] is not None and pdf_en[0] >= 0.85 and not ayni:
            uyarilar.append(f"PDF adı '{pdf_en[1]['id']}' destesini, program eşleşmesi '{prg_en[1]['id']}' destesini gösteriyor — yeni taslak açıldı, kontrol et")
        if not es.get("programda"):
            uyarilar.append("ders programında güvenle eşleşen konu yok (adaylar rapordadır); ders PDF'in kendi adıyla açıldı")
        n = sonraki_numara(kurul) if kurul else 0
        ad_kaynagi = es.get("konu") if es.get("programda") else pdf_adi
        ders_id = f"k{kurul}-{n:02d}-{slug(ad_kaynagi)}"
        deste_id = f"k{kurul}p-{ders_id}"
        mod = "yeni"
    b = {
        "is_id": j["is_id"], "pdf_yolu": j["yol"], "pdf_adi": Path(j["yol"]).name, "yil": j.get("yil"),
        "uyari": "; ".join(u for u in uyarilar if u), "sayfa": bilgi["sayfa"], "ocr_sayfalar": bilgi["ocr_sayfalar"],
        "program": es, "kurul": kurul, "numara": n, "ders_id": ders_id, "deste_id": deste_id, "mod": mod,
        "mevcut_eslesme": round(mevcut[0], 3),
        "committeeId": f"donem3-kurul{kurul}" if kurul else "",
        "mevcut_dersler": [d.get("title") for d in (decks if isinstance(decks, list) else []) if d.get("id", "").startswith(f"k{kurul}p-")],
        "kazanimlar": kazanimlar(kurul, es.get("konu") or "") if (kurul and es.get("programda")) else [],
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
def _isle_tek(j: dict) -> dict:
    if not (os.environ.get("CLAUDE_CODE_OAUTH_TOKEN") or (Path(os.environ.get("HOME", "~")).expanduser() / ".claude").exists()):
        return {"durum": "kota", "mesaj": "Claude anahtarı yok (deploy/oracle/isci-token-yukle.sh)"}
    d = TASLAK / j["is_id"]
    d.mkdir(parents=True, exist_ok=True)
    if not (d / "kaynak.md").exists():
        metin, bilgi = pdf_metni(Path(j["tam"]))
        if j.get("sayfalar"):  # çok konulu PDF: yalnız bu konunun sayfa aralığı
            bas, bit = j["sayfalar"]
            parcalar = [b for b in metin.split("=== SAYFA ")[1:] if bas <= int(b.split(" ===")[0]) <= bit]
            metin = "\n\n".join("=== SAYFA " + b.rstrip() for b in parcalar)
            bilgi = {**bilgi, "karakter": len(metin), "sayfa_araligi": [bas, bit]}
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


def isle(j: dict) -> dict:
    """Bir PDF işi. Kapsamda birden çok konu varsa her konu ayrı alt iş (kendi sayfa aralığı, kendi ders paketi)."""
    konular = j.get("konular") or []
    if len(konular) <= 1:
        if konular:
            j = {**j, "konu_zorla": konular[0]}
        return _isle_tek(j)
    sonuclar = []
    for i, kz in enumerate(konular, 1):
        alt = {**j, "is_id": f"{j['is_id']}-{i}", "konu_zorla": kz, "sayfalar": (kz.get("sayfa_bas"), kz.get("sayfa_bit"))}
        if oku(TASLAK / alt["is_id"] / "durum.json", {}).get("durum") == "onay_bekliyor":
            sonuclar.append({"durum": "taslak", "mesaj": f"{kz.get('konu')}: zaten hazır"})
            continue
        r = _isle_tek(alt)
        sonuclar.append(r)
        if r["durum"] == "kota":
            return {"durum": "kota", "mesaj": f"{i}/{len(konular)} konuda kota; kalan konular sonra"}
    durum = "taslak" if all(r["durum"] == "taslak" for r in sonuclar) else "hata"
    return {"durum": durum, "mesaj": " | ".join(r.get("mesaj", "")[:120] for r in sonuclar)}
