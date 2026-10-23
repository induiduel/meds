"""Görev `sesli_bolum` — Kurul 2+ sesli ders metni v2 (`konusma_v2.json`) bölüm bölüm (TALIMAT_SESLI.md §v2; R4).

Hedef: `<ad>/bolum/<n>` ve `--ayar w=<ders işçisi taslak klasörü>` (kaynak.md, sayfa_haritasi.json, deck.json,
cikmis_baglantilari.json, baglam.json). Bölümler `sayfa_haritasi.basliklar` (sayfa + deste adımı aralığı) — anlatım sırası.
Girdi: bölümün sayfa satırları (L etiketli), destenin o adımlarının anlatımı (D), bu bölüme düşen ilgili çıkmışlar (Q: kök +
doğru cevap), önceki bölümün başlığı ve son cümlesi (bağ). Model yazar: paragraflar → cümleler {ses, ekran, duzey, vurgu,
satir: [L…] | sekil, adim: D, cikmis: [Q]}. Slayt satırını model KOPYALAMAZ: derleyici L etiketinden birebir kurar
(kapının "slayt satırı birebir yok" hatası yapısal olarak kalkar). Kimlikler birleştirmede sırayla verilir.
Kapı: `konusma_v2.dogrula` (biçim, ses işaretlemesi, ekran ≤28 kelime, vurgu ekranda, Türkçe üslup, çapa, %25 çapasız
tavanı) + `metin_denetle` dolgu/telaffuz kuralları (ders düzeyi kelime sınırı birleştirmede) + bölümdeki her ilgili çıkmış
bir cümlede işlenmiş ve o cümlede "Burası önemli" + bölüm sayfalarındaki sayı+birim/yüzde ekran metninde (sıfır kayıp).
Uygulama: W/gorev_sesli/bolum_<n>.json; birleştirme `sesli_bolum.birlestir(W)` → W/konusma_v2.json (+ --turet).
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

from .. import cekirdek as c

SES_ONAR = True   # ses alanlarında kısaltma/Roma rakamı okunuşu betikle (cekirdek.ses_onar)
KURALLAR = ["kaynak_sadakati", "sesli_yazimi", "ses_yazimi", "turkce_uslup", "cikti_disiplini"]


def _sa():
    for p in (c.KOK / "scripts" / "sesli_anlatim", c.KOK / "scripts", c.KOK / "scripts" / "kroki"):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    import konusma_v2 as KV
    return KV


def _w(hedef: str, ayar: dict | None) -> tuple[Path, int]:
    m = re.fullmatch(r"[^/]+/bolum/(\d+)", hedef)
    W = Path((ayar or {}).get("w") or "")
    if not m or not (W / "kaynak.md").exists():
        raise SystemExit("sesli_bolum hedefi '<ad>/bolum/<n>' ve --ayar w=<taslak klasörü (kaynak.md)>")
    return W, int(m.group(1))


def _dogru_cevaplar() -> dict[str, str]:
    """Çıkmış soru kimliği → doğru şık METNİ (baglam.json'daki adaylarda cevap boş olabiliyor): çıkmış dizini, yoksa
    soru bankası (data/pastQuestions.json)."""
    d = c.oku(c.DB2 / "cikmis_dizin" / "dizin.json")
    if d:
        return {q["id"]: q["dogru_metin"] for q in d["sorular"]}
    out = {}
    for q in c.oku(c.KOK / "data" / "pastQuestions.json") or []:
        sec = {(o.get("key") or "")[:1]: o.get("text") for o in q.get("options") or []}
        if q.get("correctAnswer") in sec:
            out[q["id"]] = sec[q["correctAnswer"]]
    return out


def bolumler(W: Path) -> list[dict]:
    return (c.oku(W / "sayfa_haritasi.json") or {}).get("basliklar") or []


def ders_id(W: Path) -> str:
    did = (c.oku(W / "baglam.json") or {}).get("ders_id") or ""
    return "-".join(did.split("-")[:2])


def hazirla(hedef: str, ayar: dict | None = None) -> dict:
    KV = _sa()
    W, n = _w(hedef, ayar)
    B = bolumler(W)
    if n >= len(B):
        raise SystemExit(f"{len(B)} bölüm var (0–{len(B) - 1})")
    b = B[n]
    a, s = b["sayfalar"][0], b["sayfalar"][-1]
    km = KV.kaynak_metin(W)
    et = c.Etiketler()
    satirlar, meta_L = [], {}
    for no in range(a, s + 1):
        if no not in km:
            continue
        st = []
        for t in (x.strip() for x in km[no].splitlines()):
            t = re.sub(r"^[•●▪➢–\-o]\s+", "", t)
            if len(t) > 2:
                L = et.ekle("L", f"{no}|{len(meta_L)}")
                meta_L[L] = [no, t]
                st.append(f"{L}: {t}")
        satirlar.append(f"### Sayfa {no}\n" + ("\n".join(st) if st else "(metinsiz sayfa — görsel)"))
    deck = c.oku(W / "deck.json") or {}
    did = ders_id(W)
    adim_a, adim_b = (b.get("adimlar") or [0, -1])[0], (b.get("adimlar") or [0, -1])[-1]
    deste, meta_D = [], {}
    for sl in deck.get("slides") or []:
        no = sl.get("slideNumber")
        if isinstance(no, int) and adim_a <= no <= adim_b:
            D = et.ekle("D", f"{did}-d-s{no:02d}")
            meta_D[D] = f"{did}-d-s{no:02d}"
            deste.append(f"{D} ({sl.get('title', '')}): {' '.join(str(sl.get('synthesisNarrative') or '').split()[:110])}")
    bg = c.oku(W / "baglam.json") or {}
    aday = {x.get("id") or x.get("soru_id"): x for x in bg.get("cikmis_adaylari") or []}
    dogrular = _dogru_cevaplar()
    cik, meta_Q = [], {}
    for x in c.oku(W / "cikmis_baglantilari.json") or []:
        if not x.get("ilgili"):
            continue
        sn = x.get("slideNumber")
        if not (isinstance(sn, int) and adim_a <= sn <= adim_b):
            continue
        q = aday.get(x["soru_id"]) or {}
        sec = q.get("secenekler") or []
        dogru = dogrular.get(x["soru_id"]) or q.get("cevap") or "?"
        Q = et.ekle("Q", x["soru_id"])
        meta_Q[Q] = x["soru_id"]
        cik.append(f"{Q}: {q.get('kok', '')[:300]} → doğru cevap: {dogru}")
    onceki = c.oku(W / "gorev_sesli" / f"bolum_{n - 1}.json") if n else None
    bag = (f"Önceki bölüm: {B[n - 1]['baslik']}; son cümle: {onceki['paragraflar'][-1]['cumleler'][-1]['ses']}"
           if onceki else ("Önceki bölüm: " + B[n - 1]["baslik"] if n else "Dersin ilk bölümü: doğrudan ilk tıbbi kavramla başla."))
    ornek = {"paragraflar": [{"sayfa": a, "cumleler": [
        {"ses": "Doktorun öğrenciye anlatır gibi kurduğu tam cümle.", "ekran": "Kısa madde, **kilit kavram**", "duzey": 0,
         "vurgu": [{"metin": "kilit kavram", "tur": "terim"}], "satir": ["L3"], "sekil": None, "adim": "D1", "cikmis": []}]}]}
    return {
        "amac": (f"Sesli dersin \"{b['baslik']}\" bölümünü (sayfa {a}–{s}) yaz: bu sayfalardaki her tıbbi bilgiyi sırayla, "
                 f"paragraflar halinde anlat. Her cümle iki yüzlü: `ses` (okunacak doğal anlatım) ve `ekran` (aynı bilginin madde hâli)."),
        "kurallar": KURALLAR,
        "ek_kurallar": [
            "Her cümlenin anlattığı slayt satır(lar)ını `satir` alanına L etiketleriyle ver (aynı sayfadan); `ses` cümlesini o satırın "
            "terimleriyle aynı sırada kur. Metinsiz resim/şema anlatıyorsan `satir: []` ve `sekil`e kısa tarif. Yalnız geçiş "
            "cümlesinde ikisi de boş olabilir (bölümün en çok %25'i).",
            "Her Q (çıkmış soru) için o bilgiyi anlatan cümlenin `cikmis` listesine Q'yu koy ve o cümlenin `vurgu`suna "
            "`{\"metin\": <ekrandaki cevap ifadesi>, \"tur\": \"cikmis\"}` ekle. \"Burası önemli\" bölümde EN ÇOK BİR kez, "
            "bölümün en kritik çıkmış bilgisinde (H22: önem vurgusu yalnız dayanaklı ve seyrek); soru yılı/şık harfi okunmaz.",
            "`ekran` en çok 28 kelime; `vurgu.metin` ekran metninde birebir geçer; `vurgu.tur` terim|sayi|tuzak|cikmis|tanim; "
            "`duzey` 0 ana madde, 1 alt madde. Paragraf `sayfa`sı anlattığı ilk sayfa.",
            "Dolgu yok: \"hoca vurguladı\", \"şimdi gelelim\", \"daha önce söylediğimiz gibi\", \"özetlemek gerekirse\" yazma.",
        ],
        "girdi": "\n\n".join(satirlar) + ("\n\n## Destenin bu bölümdeki adımları (anlatım dayanağı; `adim` alanına D etiketi)\n"
                                          + "\n".join(deste) if deste else "")
                 + ("\n\n## Bu bölüme düşen çıkmış sorular\n" + "\n".join(cik) if cik else ""),
        "baglam": bag,
        "cikti_bicimi": "Yalnız şu JSON:\n" + json.dumps(ornek, ensure_ascii=False, indent=1),
        "denetim_listesi": ["sayfalardaki her bilgi anlatıldı (sayı ve birimler ekranda)", "her Q bir cümlede ve orada 'Burası önemli'",
                            "satir L etiketleri bilgiyi taşıyan satırlar", "ses alanında işaret yok; rakam/kısaltma okunuşla",
                            "ekran ≤28 kelime, vurgu ekranda birebir"],
        "esleme": et.esleme,
        "meta": {"w": str(W), "bolum": n, "baslik": b["baslik"], "sayfa": [a, s], "ders_id": did, "L": meta_L, "D": meta_D,
                 "Q": meta_Q, "kurul": int(did[1]) if did[1:2].isdigit() else None},
    }


def derle(cevap, esleme: dict, meta: dict):
    j = c.json_cikar(cevap)
    if not isinstance(j, dict) or not isinstance(j.get("paragraflar"), list):
        return None, ["cevap JSON değil ya da 'paragraflar' yok"]
    e, par = [], []
    for pi, p in enumerate(j["paragraflar"], 1):
        cum = []
        for ci, x in enumerate(p.get("cumleler") or [], 1):
            yer = f"P{pi}.C{ci}"
            Ls = [str(L).strip() for L in (x.get("satir") or [])]
            bil = [L for L in Ls if L not in meta["L"]]
            if bil:
                e.append(f"{yer}: girdide olmayan satır etiketi {bil}")
            Ls = [L for L in Ls if L in meta["L"]]
            sayfa = meta["L"][Ls[0]][0] if Ls else None
            satir = [meta["L"][L][1] for L in Ls if meta["L"][L][0] == sayfa]
            sekil = x.get("sekil") or None
            slayt = {"sayfa": sayfa or p.get("sayfa"), "satir": satir, "sekil": sekil} if (satir or sekil) else None
            adim = meta["D"].get(str(x.get("adim") or "").strip())
            cq = [meta["Q"][q] for q in (x.get("cikmis") or []) if q in meta["Q"]]
            cum.append({"ses": str(x.get("ses") or "").strip(), "ekran": str(x.get("ekran") or "").strip(),
                        "duzey": x.get("duzey", 0) if x.get("duzey") in (0, 1, 2) else 0,
                        "vurgu": [v for v in (x.get("vurgu") or []) if isinstance(v, dict)],
                        "slayt_adim": adim, "cikmis": cq, "spot": None, "slayt": slayt, "_yer": yer, "_L": Ls})
        sy = p.get("sayfa")
        par.append({"sayfa": int(sy) if str(sy).isdigit() else meta["sayfa"][0], "cumleler": cum})
    return {"surum": 1, "bolum": meta["bolum"], "baslik": meta["baslik"], "paragraflar": par}, e


def _kimlikle(did: str, bolum_listesi: list[dict]) -> dict:
    """Bölüm çıktıları → konusma_v2 şeması (kimlikler sırayla: bNN, pNNN, cNNNN)."""
    b_out, pn, cn = [], 0, 0
    for bi, b in enumerate(bolum_listesi, 1):
        ps = []
        for p in b["paragraflar"]:
            pn += 1
            cs = []
            for x in p["cumleler"]:
                cn += 1
                cs.append({"id": f"{did}-c{cn:04d}", **{k: v for k, v in x.items() if not k.startswith("_")}})
            ps.append({"id": f"{did}-p{pn:03d}", "sayfa": p["sayfa"], "cumleler": cs})
        b_out.append({"id": f"{did}-b{bi:02d}", "baslik": b["baslik"], "paragraflar": ps})
    return {"surum": 2, "ders_id": did, "bolumler": b_out}


def _metin_denetle(md: str, ders_duzeyi: bool) -> list[str]:
    import subprocess
    with tempfile.TemporaryDirectory(prefix="sesli_md_") as t:
        p = Path(t) / "konusma_metni.md"
        p.write_text(md, encoding="utf-8")
        r = subprocess.run([sys.executable, str(c.KOK / "scripts" / "sesli_anlatim" / "metin_denetle.py"), str(p)],
                           capture_output=True, text=True)
    h = [ln.strip()[5:].strip() for ln in r.stdout.splitlines() if ln.strip().startswith("HATA ")]
    if not ders_duzeyi:
        h = [x for x in h if not re.search(r"kelime|bölüm sayısı|bölüm \d|ilk satır|süre|dakika|önem vurgusu", x)]
    return h


def dogrula(cikti: dict, meta: dict) -> list[str]:
    KV = _sa()
    W = Path(meta["w"])
    d = _kimlikle(meta["ders_id"], [cikti])
    yer = {cc["id"]: x["_yer"] for cc, x in zip((cc for b in d["bolumler"] for p in b["paragraflar"] for cc in p["cumleler"]),
                                                 (x for p in cikti["paragraflar"] for x in p["cumleler"]))}
    e = []
    for h in KV.dogrula(d, KV.kaynak_sayfa(W), KV.kaynak_metin(W)):
        m = re.match(r"(\S+?):", h)
        e.append(yer.get(m.group(1), m.group(1)) + h[len(m.group(1)):] if m else h)
    md, _ = KV.turet(d)
    e += _metin_denetle(md, ders_duzeyi=False)
    # anlatım üslubu (betikle ölçülebilen kısım): tam cümle, slayt okuma değil anlatma
    cum = [x for p in cikti["paragraflar"] for x in p["cumleler"]]
    for x in cum:
        ses = x["ses"].strip()
        if ses and (not ses[0].isupper() or ses[-1] not in ".!?"):
            e.append(f"{x['_yer']}: ses büyük harfle başlayan, noktalamayla biten tam cümle olmalı")
    if cum:
        kisa = sum(1 for x in cum if len(x["ses"].split()) < 6)
        if kisa > 0.2 * len(cum):
            e.append(f"{kisa}/{len(cum)} ses cümlesi 6 kelimeden kısa — madde okuma değil, doktor anlatımı (neden-sonuç bağıyla)")
        oran = sum(len(x["ses"].split()) for x in cum) / max(sum(len(x["ekran"].replace("**", "").split()) for x in cum), 1)
        if oran < 1.3:
            e.append(f"ses/ekran uzunluk oranı {oran:.2f} (≥1,3) — ses ekran maddesini okumamalı; mekanizmayı ve bağlamı anlatmalı")
    # her ilgili çıkmış işlendi + "Burası önemli"
    for Q, sid in meta["Q"].items():
        cs = [x for p in cikti["paragraflar"] for x in p["cumleler"] if sid in x["cikmis"]]
        if not cs:
            e.append(f"{Q}: hiçbir cümlede işlenmedi (o bilgiyi anlatan cümlenin cikmis listesine koy)")
        elif not any(v.get("tur") == "cikmis" for x in cs for v in x["vurgu"]):
            e.append(f"{Q}: işlendiği cümlede tur=cikmis vurgusu yok")
    onem = sum(len(re.findall(r"burası önemli", x["ses"].lower())) for p in cikti["paragraflar"] for x in p["cumleler"])
    if onem > 1:
        e.append(f"\"Burası önemli\" bu bölümde {onem} kez — en çok 1 (öteki çıkmışlar vurgu tur=cikmis ile)")
    # sıfır kayıp: sayfalardaki sayı+birim / yüzde ekranda
    # sayı+birim / yüzde değerinin SAYISI ekranda geçmeli ("280 gün" ↔ "280 günlük" aynı bilgidir); her sayı bir kez
    import varlik
    ekran = " ".join(x["ekran"] for p in cikti["paragraflar"] for x in p["cumleler"]).replace(",", ".")
    eksik: dict[str, list] = {}
    ocr = set((c.oku(Path(meta["w"]) / "baglam.json") or {}).get("ocr_sayfalar") or [])
    ekran_sayi = set(re.findall(r"\d+(?:\.\d+)?", ekran))
    for L, (no, t) in meta["L"].items():
        if no in ocr:
            continue                                  # OCR sayfası: bozuk sayı düzeltilerek anlatılır (185-249 → 18,5–24,9)
        for v in varlik.cikar(t):
            if not v.startswith("s:"):
                continue
            sayi = re.match(r"s:(\d+(?:\.\d+)?)", v).group(1)
            ondalik = {sayi[:i] + "." + sayi[i:] for i in range(1, len(sayi))} if "." not in sayi else set()
            if not re.search(rf"(?<![\d.]){re.escape(sayi)}(?![\d])", ekran) and not (ondalik & ekran_sayi):
                eksik.setdefault(f"{sayi} ({v[2 + len(sayi):]})", []).append(no)
    for k, sy in eksik.items():
        e.append(f"sayı {k} (sayfa {sorted(set(sy))}) ekran metinlerinde RAKAMLA yok — ya anlatılmamış (sıfır kayıp) ya da "
                 f"ekranda yazıyla yazılmış (ekranda rakam kullan, okunuş yalnız ses alanında)")
    return list(dict.fromkeys(e))


def tersine(cikti: dict, esleme: dict, meta: dict) -> str:
    ters_D = {v: k for k, v in meta["D"].items()}
    ters_Q = {v: k for k, v in meta["Q"].items()}
    return json.dumps({"paragraflar": [{"sayfa": p["sayfa"], "cumleler": [
        {"ses": x["ses"], "ekran": x["ekran"], "duzey": x["duzey"], "vurgu": x["vurgu"], "satir": x["_L"],
         "sekil": (x["slayt"] or {}).get("sekil"), "adim": ters_D.get(x["slayt_adim"]), "cikmis": [ters_Q[q] for q in x["cikmis"]]}
        for x in p["cumleler"]]} for p in cikti["paragraflar"]]}, ensure_ascii=False, indent=1)


ozet = tersine


def uygula(cikti: dict, meta: dict, cikis: Path | None = None, k1_izin: bool = False) -> Path:
    W = Path(cikis) if cikis else Path(meta["w"])
    p = W / "gorev_sesli" / f"bolum_{meta['bolum']}.json"
    c.yaz(p, cikti)
    return p


ONEM = re.compile(r"\bburası önemli\b[,:;.!]?\s*", re.I)


def onem_sinirla(d: dict) -> int:
    """metin_denetle (H22) ders toplamında "Burası önemli" ≤ max(3, bölüm/2): fazlası, çok sorulan çıkmışa bağlı olanlar
    korunarak (önce çıkmış sayısı fazla, sonra metin sırası) cümleden çıkarılır; cümle büyük harfle sürer."""
    sinir = max(3, len(d["bolumler"]) // 2)
    cs = [x for b in d["bolumler"] for p in b["paragraflar"] for x in p["cumleler"] if ONEM.search(x["ses"])]
    tut = set(id(x) for x in sorted(cs, key=lambda x: -len(x.get("cikmis") or []))[:sinir])
    n = 0
    for x in cs:
        if id(x) in tut:
            continue
        yeni = ONEM.sub("", x["ses"], count=1).strip()
        x["ses"] = yeni[:1].upper() + yeni[1:] if yeni else x["ses"]
        n += 1
    return n


def birlestir(W: Path, log=print) -> int:
    """Bölüm çıktıları → W/konusma_v2.json + eski biçim türevi; konusma_v2 --dogrula ve metin_denetle (ders düzeyi) 0 HATA."""
    KV = _sa()
    B = bolumler(W)
    parca = []
    for n in range(len(B)):
        o = c.oku(W / "gorev_sesli" / f"bolum_{n}.json")
        if not o:
            log(f"bölüm {n} yok — önce sesli_bolum görevi"); return 2
        parca.append(o)
    d = _kimlikle(ders_id(W), parca)
    azaltilan = onem_sinirla(d)
    if azaltilan:
        log(f"  \"Burası önemli\" ders sınırı için {azaltilan} cümleden kalıp çıkarıldı (çıkmış vurgusu kalır)")
    e = KV.dogrula(d, KV.kaynak_sayfa(W), KV.kaynak_metin(W))
    md, sayfa = KV.turet(d)
    e += _metin_denetle(md, ders_duzeyi=True)
    for x in e[:30]:
        log(f"  HATA {x}")
    n_c = sum(len(p["cumleler"]) for b in d["bolumler"] for p in b["paragraflar"])
    log(f"sesli v2: {len(d['bolumler'])} bölüm, {n_c} cümle, {len(md.split())} kelime · {len(e)} HATA")
    if e:
        c.yaz(W / "gorev_sesli" / "konusma_v2_hatali.json", d)
        return 1
    c.yaz(W / "konusma_v2.json", d)
    (W / "konusma_metni.md").write_text(md, encoding="utf-8")
    (W / "konusma_sayfalari.json").write_text(json.dumps(sayfa), encoding="utf-8")
    (W / "konusma_capalari.json").write_text(json.dumps(KV.capalar(d), ensure_ascii=False), encoding="utf-8")
    return 0
