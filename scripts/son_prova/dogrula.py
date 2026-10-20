#!/usr/bin/env python3
"""Son Prova aşama parçası doğrulayıcısı (TALIMAT.md). TBG kampı doğrulayıcısının genel (her branş, her kurul) sürümü.

Kullanım:
  python3 meds_temp/son_prova/dogrula.py meds_temp/son_prova/parca/<part>/a03.json [...]   → 0 HATA ise çıkış 0
  python3 meds_temp/son_prova/dogrula.py --part <part-key>   → partın tüm aşamaları + part düzeyi denetim
     (soru tekrarı, check-up sayısı, çıkmış kapsamı, kelime/süre hedefi)
"""
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent
ROOT = KOK.parents[1]
sys.path.insert(0, str(ROOT / "meds" / "scripts"))
from turkce_uslup import denetle as uslup  # noqa: E402
from sik_aciklama import denetle as sik_denetle  # noqa: E402

PLAN = json.loads((KOK / "plan.json").read_text(encoding="utf-8"))
PARTLAR = {p["key"]: p for p in PLAN["partlar"]}
DAKIKA_KELIME = PLAN["dakika_kelime"]
AZAMI_DAKIKA = 88  # part başına en fazla bir buçuk saat (kullanıcı kuralı); EMA hızı ölçülünce derle.py ayrıca denetler

# canliDersStore.ts::cumleSinirlari ile aynı kural
SON = re.compile(r"[.!?…]+[\"'”’)\]]*(?:\s+|$)")


def sinirlar(m: str) -> list[int]:
    out = []
    for x in SON.finditer(m):
        e = x.end()
        s = m[e:e + 1]
        if s and s != s.upper() and s == s.lower():
            continue
        if e > (out[-1] if out else 0):
            out.append(e)
    if not out or out[-1] < len(m):
        out.append(len(m))
    return out


YASAK_SIMGE = re.compile(r"[*#|>\[\]{}=_`~%↑↓→←±≈≥≤×/+<()\"“”‘⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉αβγδκλμθπσΔ;]")
NOKTALI_KISA = re.compile(r"\b(vs|vb|örn|Dr|Prof|St|bkz|yy|yak|ort|Doç)\.", re.I)
SURECI_DIL = re.compile(r"\b(PDF'?te|slaytta yok|aday|bağlandı|kaynakta geçmiyor|ders notunda|katalog|havuz)\b", re.I)
SORU_BILGI = re.compile(r"\b(\d{4}|şık|seçenek|[A-E] şıkkı)\b")


def part_bul(p: Path) -> dict:
    return PARTLAR[p.parent.name]


def havuz_refleri(part: dict) -> dict[str, dict]:
    b = part["brans"]
    out = {}
    d = ROOT / "meds" / f"src/data/{b}_cozucu"
    for ders in part["dersler"]:
        kod = ders["kod"]
        fs = [d / f"{kod}.json"] if (d / f"{kod}.json").exists() else sorted(d.glob(f"{kod}-*.json"))
        for f in fs:
            for q in json.loads(f.read_text(encoding="utf-8"))["sorular"]:
                out[f"{b}/{f.stem}#{q['no']}"] = {**q, "_ders": kod}
    return out


def cikmis_idleri(part: dict) -> dict[str, str]:
    """çıkmış id → ders kodu (havuz kataloglarından)"""
    out = {}
    for ders in part["dersler"]:
        t = (ROOT / ders["havuz_katalog"]).read_text(encoding="utf-8")
        bolum = t.split("## Soru havuzu")[0]
        for m in re.finditer(r"^- \*\*([^*]+)\*\* ·", bolum, re.M):
            out[m.group(1)] = ders["kod"]
    return out


def denetle(p: Path, ozet: dict | None = None) -> int:
    H, U = [], []
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"{p.name}: JSON okunamadı: {e}")
        return 1
    try:
        part = part_bul(p)
    except KeyError:
        print(f"{p}: part klasörü plan.json'da yok")
        return 1
    sayfa = {x["slayt_kod"]: x["sayfa"] for x in part["dersler"]}
    for a in ("asama", "ders", "baslik", "giris", "bolumler", "sorular", "checkup"):
        if a not in d:
            H.append(f"alan yok: {a}")
    if d.get("ders") not in sayfa:
        H.append(f"ders kodu bu partta yok: {d.get('ders')} (olası: {', '.join(sayfa)})")
    kelime = 0
    onemli = 0
    baska_ders = 0

    def cumle(t, k, yer):
        nonlocal kelime, onemli, baska_ders
        if not isinstance(t, str) or not t.strip():
            H.append(f"{yer}: boş cümle")
            return
        if t != t.strip() or "  " in t:
            H.append(f"{yer}: fazla boşluk")
        w = len(t.split())
        kelime += w
        if w < 4:
            H.append(f"{yer}: çok kısa cümle ({w} kelime): {t}")
        if w > 40:
            H.append(f"{yer}: çok uzun cümle ({w} kelime) — böl: {t[:60]}…")
        elif w > 32:
            U.append(f"{yer}: uzun cümle ({w}): {t[:60]}…")
        if not re.search(r"[.!?]$", t):
            H.append(f"{yer}: cümle . ? ! ile bitmeli: …{t[-30:]}")
        if len(sinirlar(t)) != 1:
            H.append(f"{yer}: cümle içinde cümle sınırı var (nokta+boşluk+büyük harf): {t[:80]}")
        if "..." in t or "…" in t:
            H.append(f"{yer}: üç nokta")
        ilk = t[0]
        if ilk != ilk.upper() and ilk == ilk.lower():
            H.append(f"{yer}: cümle küçük harfle başlıyor (sınır kayar): {t[:40]}")
        # gen/kısaltma adlarındaki rakam serbest (BRCA1, IL-6, CD31, PD-L1, C3a); diğer rakamlar yazıyla
        t_gensiz = re.sub(r"[A-Za-zÇĞİÖŞÜçğıöşü0-9-]+", lambda m: "GEN" if re.match(r"([A-Z]|p\d)", m.group()) and re.search(r"\d", m.group()) and re.search(r"[A-Z]|^p\d", m.group()) else m.group(), t)
        if re.search(r"\d", t_gensiz):
            H.append(f"{yer}: rakam (yazıyla yaz): {re.findall(r'.{0,12}[0-9]+.{0,8}', t_gensiz)[0]}")
        m = YASAK_SIMGE.search(t)
        if m:
            H.append(f"{yer}: simge/parantez/tırnak/noktalı virgül '{m.group()}': {t[:70]}")
        if NOKTALI_KISA.search(t):
            H.append(f"{yer}: noktalı kısaltma: {t[:60]}")
        if re.match(r"\s*[-•–]", t):
            H.append(f"{yer}: madde imi")
        m = SURECI_DIL.search(t)
        if m:
            H.append(f"{yer}: iç süreç dili '{m.group()}': {t[:70]}")
        if re.search(r"[Bb]urası önemli|çıkmış soru|sınavda soru|sınavda sorul", t):
            onemli += 1
        for e in uslup(t, yer):
            H.append(f"üslup {e}")
        if k is not None:
            mm = re.fullmatch(r"([a-z]?\d{2}b?):(\d+)", str(k))
            if not mm:
                H.append(f"{yer}: slayt biçimi 'kod:sayfa' olmalı (ör. p07:23, e05:12): {k}")
            elif mm.group(1) not in sayfa:
                H.append(f"{yer}: slayt kodu bu partta yok: {k}")
            elif not 1 <= int(mm.group(2)) <= sayfa[mm.group(1)]:
                H.append(f"{yer}: sayfa aralık dışı: {k} (en çok {sayfa[mm.group(1)]})")
            elif mm.group(1) != d.get("ders"):
                baska_ders += 1

    cumle(d.get("giris", ""), d.get("giris_k"), "giris")
    if d.get("giris_k") is None:
        H.append("giris_k (girişin slaytı) zorunlu")
    bs = d.get("bolumler") or []
    if not 2 <= len(bs) <= 10:
        U.append(f"alt başlık sayısı {len(bs)} (3–8 önerilir)")
    kyok = 0
    toplam_c = 0
    for bi, b in enumerate(bs):
        bb = str(b.get("baslik", "")).strip()
        if not bb:
            H.append(f"b{bi + 1}: başlık yok")
        elif len(bb) > 70:
            U.append(f"b{bi + 1}: başlık uzun ({len(bb)} karakter)")
        if "·" in bb:
            H.append(f"b{bi + 1}: başlıkta '·' kullanma")
        ps = b.get("paragraflar") or []
        if not 1 <= len(ps) <= 5:
            U.append(f"b{bi + 1}: paragraf sayısı {len(ps)}")
        for pi, par in enumerate(ps):
            yer = f"b{bi + 1}p{pi + 1}"
            if not isinstance(par, list) or not par:
                H.append(f"{yer}: paragraf cümle listesi olmalı")
                continue
            w = sum(len(str(c.get('t', '')).split()) for c in par)
            if w < 30 or w > 170:
                (H if w < 20 or w > 200 else U).append(f"{yer}: paragraf {w} kelime (40–150)")
            if len(par) > 10:
                U.append(f"{yer}: {len(par)} cümle (3–8 önerilir)")
            if par and par[0].get("k") is None:
                U.append(f"{yer}: paragrafın ilk cümlesinin slaytı yok (paragraf slaytı önceki paragraftan kalır)")
            for ci, c in enumerate(par):
                toplam_c += 1
                if c.get("k") is None:
                    kyok += 1
                cumle(c.get("t"), c.get("k"), f"{yer}c{ci + 1}")
            birlesik = " ".join(str(c.get("t", "")) for c in par)
            if len(sinirlar(birlesik)) != len(par):
                H.append(f"{yer}: birleşik paragrafta cümle sayısı {len(sinirlar(birlesik))} ≠ {len(par)}")
    if toplam_c and kyok / toplam_c > 0.2:
        U.append(f"slaytsız cümle oranı yüksek: {kyok}/{toplam_c}")
    if toplam_c and baska_ders / toplam_c > 0.15:
        U.append(f"başka dersin slaytına giden cümle çok: {baska_ders}/{toplam_c}")

    # sorular
    refs = havuz_refleri(part)
    sor = d.get("sorular") or []
    chk = d.get("checkup") or []
    if not 3 <= len(sor) <= 6:
        H.append(f"aşama sonu soru sayısı {len(sor)} (3–6)")
    if not 2 <= len(chk) <= 6:
        H.append(f"check-up adayı sayısı {len(chk)} (2–6)")
    for r in sor + chk:
        if r not in refs:
            H.append(f"soru ref havuzda yok: {r}")
    if len(set(sor + chk)) != len(sor + chk):
        H.append("aynı soru iki kez seçilmiş (sorular + checkup ayrık olmalı)")
    tur = [refs[r].get("tur") for r in sor if r in refs]
    if sor and "cikmis" not in tur and any(q.get("tur") == "cikmis" and q["_ders"] == d.get("ders", "").lstrip("p") for q in refs.values()):
        U.append("aşama sonu sorularında hiç çıkmış yok (varsa en az bir çıkmış seç)")
    # yeni örnek sorular (aşama başına 2; yalnız bu aşamada anlatılan bilgiyle, çıkmış üslubunda)
    ys = d.get("yeni_sorular")
    if ys is not None:
        if not 2 <= len(ys) <= 3:
            H.append(f"yeni_sorular {len(ys)} (2–3)")
        for qi, q in enumerate(ys, 1):
            yer = f"yeni{qi}"
            sec = q.get("secenekler") or {}
            if sorted(sec) != list("ABCDE"):
                H.append(f"{yer}: 5 şık (A–E) olmalı")
            if q.get("dogru") not in sec:
                H.append(f"{yer}: doğru şık geçersiz")
            if len({str(v).strip().lower() for v in sec.values()}) != len(sec):
                H.append(f"{yer}: aynı şık iki kez")
            if q.get("zorluk") not in ("kolay", "orta", "zor"):
                H.append(f"{yer}: zorluk kolay/orta/zor")
            kok = str(q.get("soru", ""))
            if len(kok.split()) < 6:
                H.append(f"{yer}: soru kökü çok kısa")
            ip = str(q.get("ipucu", ""))
            dt = str(sec.get(q.get("dogru"), "")).lower()
            if not ip or (dt and len(dt) > 3 and dt in ip.lower()):
                H.append(f"{yer}: ipucu yok ya da cevabı sızdırıyor")
            sk = q.get("siklar") or {}
            for h in "ABCDE":
                if not sk.get(h):
                    H.append(f"{yer}: {h} şıkkının açıklaması yok")
                else:
                    for e in sik_denetle(sk[h], f"{yer}{h}"):
                        H.append(f"şık {e}")
            if len(str(q.get("cozum", "")).split()) < 12:
                H.append(f"{yer}: çözüm çok kısa")
            for alan in ("soru", "ipucu", "cozum"):
                for e in uslup(str(q.get(alan, "")), f"{yer}.{alan}"):
                    H.append(f"üslup {e}")
    kc = d.get("karsilanan_cikmis") or []
    if not isinstance(kc, list):
        H.append("karsilanan_cikmis liste olmalı")
    at = d.get("atlanan_cikmis") or {}
    if not isinstance(at, dict):
        H.append("atlanan_cikmis {id: neden} olmalı")

    if ozet is not None:
        ozet.setdefault("kelime", 0)
        ozet["kelime"] += kelime
        ozet.setdefault("sorular", []).extend(sor)
        ozet.setdefault("checkup", []).extend(chk)
        ozet.setdefault("kc", set()).update(kc)
        ozet.setdefault("at", {}).update(at)
        ozet.setdefault("ders_kelime", {}).setdefault(d.get("ders"), 0)
        ozet["ders_kelime"][d.get("ders")] += kelime

    print(f"{p.parent.name}/{p.name}: aşama {d.get('asama')} · {d.get('ders')} · {kelime} kelime ≈ {kelime / DAKIKA_KELIME:.1f} dk · "
          f"{len(bs)} alt başlık · {sum(len(b.get('paragraflar') or []) for b in bs)} paragraf · {toplam_c} cümle · "
          f"önemli/çıkmış atfı {onemli} · soru {len(sor)} + check-up {len(chk)} · çıkmış {len(kc)}")
    for h in H[:80]:
        print("  HATA", h)
    if len(H) > 80:
        print(f"  … {len(H) - 80} hata daha")
    for u in U[:30]:
        print("  uyarı", u)
    print(f"  {len(H)} HATA, {len(U)} uyarı")
    return len(H)


def part_denetle(key: str) -> int:
    part = PARTLAR[key]
    dosyalar = sorted((KOK / "parca" / key).glob("a*.json"))
    if not dosyalar:
        print(f"{key}: aşama dosyası yok")
        return 1
    oz: dict = {}
    hata = sum(denetle(p, oz) for p in dosyalar)
    H, U = [], []
    tum = oz.get("sorular", []) + oz.get("checkup", [])
    tekrar = sorted({r for r in tum if tum.count(r) > 1})
    if tekrar:
        H.append(f"aşamalar arasında tekrar eden soru: {tekrar[:8]}")
    if not 10 <= len(oz.get("checkup", [])) <= 50:
        H.append(f"part check-up adayı toplamı {len(oz.get('checkup', []))} (10–50)")
    cik = cikmis_idleri(part)
    kc = oz.get("kc", set())
    at = oz.get("at", {})
    eksik = [c for c in cik if c not in kc and c not in at]
    yabanci = [c for c in kc if c not in cik]
    if eksik:
        H.append(f"karşılanmamış çıkmış ({len(eksik)}/{len(cik)}): {eksik[:12]}")
    if yabanci:
        U.append(f"karsilanan_cikmis içinde bu partta olmayan kimlik: {yabanci[:6]}")
    for c, n in at.items():
        if len(str(n)) < 15:
            H.append(f"atlanan çıkmış gerekçesi yetersiz: {c}")
    if len(at) > max(2, len(cik) // 10):
        U.append(f"atlanan çıkmış çok: {len(at)}")
    dk = oz["kelime"] / DAKIKA_KELIME
    if dk > AZAMI_DAKIKA:
        H.append(f"part süresi {dk:.0f} dk > {AZAMI_DAKIKA} dk")
    hedef = part.get("hedef_kelime") or 0
    if hedef and not 0.8 * hedef <= oz["kelime"] <= 1.25 * hedef:
        U.append(f"part kelimesi {oz['kelime']} hedef {hedef} (±%20)")
    dersler = {x["slayt_kod"]: x for x in part["dersler"]}
    for k, x in dersler.items():
        w = oz.get("ders_kelime", {}).get(k, 0)
        if not w:
            H.append(f"ders hiç anlatılmamış: {k} {x['ad']}")
        elif x.get("hedef_kelime") and not 0.6 * x["hedef_kelime"] <= w <= 1.6 * x["hedef_kelime"]:
            U.append(f"{k} kelime {w} (hedef {x['hedef_kelime']})")
    print(f"== PART {key}: {len(dosyalar)} aşama · {oz['kelime']} kelime ≈ {dk:.0f} dk · aşama sorusu {len(oz.get('sorular', []))} · "
          f"check-up {len(oz.get('checkup', []))} · çıkmış {len(kc & set(cik))}/{len(cik)} (+{len(at)} gerekçeli atlama)")
    for h in H:
        print("  HATA", h)
    for u in U:
        print("  uyarı", u)
    print(f"  PART: {len(H)} HATA, {len(U)} uyarı")
    return hata + len(H)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--part":
        sys.exit(1 if sum(part_denetle(k) for k in a[1:]) else 0)
    sys.exit(1 if sum(denetle(Path(x)) for x in a) else 0)
