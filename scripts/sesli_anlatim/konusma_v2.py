#!/usr/bin/env python3
"""Sesli ders metni v2 — cümle kimlikli, slayt bağlı, vurgu kodlu (GELECEK_PLANLAMASI §5, P1.4).

Kurul 2'den itibaren ders işçisi (TALIMAT_SESLI.md §v2) `konusma_v2.json` yazar. Eski biçim (`konusma_metni.md` +
`konusma_sayfalari.json`) bundan TÜRETİLİR; canlı ders, EMA kuyruğu ve vurgu hattı değişmeden çalışır.

Şema:
{"surum": 2, "ders_id": "k2-07", "baslik": "...",
 "bolumler": [{"id": "k2-07-b01", "baslik": "...",
   "paragraflar": [{"id": "k2-07-p001", "sayfa": 4,
     "cumleler": [{"id": "k2-07-c0001",
                   "ses": "Doktorun öğrenciye anlatır gibi kurduğu, okunacak tam cümle.",
                   "ekran": "Ekranda gösterilen kısa madde; **vurgu** işaretli",
                   "duzey": 0,                       # madde girinti düzeyi (0 ana, 1 alt)
                   "vurgu": [{"metin": "…", "tur": "terim|sayi|tuzak|cikmis|tanim"}],
                   "slayt_adim": "k2-07-d-s05" | null,  # Öğren destesi adımı
                   "cikmis": ["<çıkmış soru id>"],     # bu cümlenin cevapladığı çıkmışlar
                   "spot": "k2-07-s03" | null,
                   "slayt": {"sayfa": 5,              # anlatılan slayt (yoksa paragrafın sayfası)
                             "satir": ["<kaynak.md o sayfasından BİREBİR kopyalanmış madde/satır>", …],
                             "sekil": "<anlatılan resim/şema/tablo kısa tarifi>" | null,
                             "tablo": true | null} | null}]}]}]}
Slayt çapası (canlı derste kelime kelime PDF işareti, pdf_isaret.py): her cümle anlattığı slayt satır(lar)ını
`satir`'a harfi harfine kopyalar; resim/şema/tablo anlatılıyorsa `sekil` dolar (lazer o resme/tabloya gider; şekil
çapası madde eşlemesine üstün gelir). Anlatılan bir tabloysa (PDF'te resim de olsa) `tablo: true` eklenir.
`madde`/`resim` dizinleri elle ya da toplu betikle UYDURULMAZ (her cümleye madde/R0 basmak işareti bozar, H-çapa).
Bağlam/geçiş cümlesi `slayt: null` olabilir (en çok %25). Kapı: her satır o sayfanın metninde geçmeli.
Kimlik kuralları: bölüm b NN, paragraf p NNN, cümle c NNNN; ders içinde tekil. Kimlik kalıcıdır: düzeltmede var olan
cümlenin kimliği değişmez, araya eklenen cümle kullanılmamış bir sonraki numarayı alır (sıra şartı yok).
Deeplink: /k/k2-07-c0142.

  konusma_v2.py --dogrula DIZIN            (konusma_v2.json + kaynak.md) → HATA sayısı, çıkış 1
  konusma_v2.py --turet DIZIN              → konusma_metni.md + konusma_sayfalari.json (eski biçim)
  konusma_v2.py --k1-donustur KEY          data/sesli_anlatim/metin/KEY.md + hizalama → v2 (geri doldurma; ekran=ses)
"""
import argparse, json, re, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MEDS / "scripts"))
VURGU_TUR = {"terim", "sayi", "tuzak", "cikmis", "tanim"}
CUMLE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9\"“(])")


def cumlelere(paragraf):
    return [c.strip() for c in CUMLE.split(paragraf.strip()) if c.strip()]


def _katla(t):
    return re.sub(r"[^0-9a-zçğıöşü]+", " ", (t or "").replace("I", "ı").replace("İ", "i").lower()).strip()


CAPA_BOS_TAVAN = 0.25  # slayt çapası olmayan (bağlam/geçiş) cümle oranı en çok


def dogrula(d, kaynak_sayfalar=None, kaynak_metin=None):
    """kaynak_metin: {sayfa: metin} (kaynak.md) — verilirse slayt çapası satırları birebir denetlenir."""
    h = []
    capa_bos = capa_top = 0
    km = {k: _katla(v) for k, v in (kaynak_metin or {}).items()}
    did = d.get("ders_id", "")
    if d.get("surum") != 2: h.append("surum 2 değil")
    if not re.fullmatch(r"k\d-\d{2}", did): h.append(f"ders_id biçimi: {did!r}")
    gor = set()  # kimlik: biçim + tekillik (sıra şartı yok: araya eklenen cümle yeni numara alır, eskiler korunur)
    try:
        from turkce_uslup import denetle as uslup
    except ImportError:
        uslup = None
    for b in d.get("bolumler", []):
        for tur, x in [("b", b)] + [("p", p) for p in b.get("paragraflar", [])] + \
                [("c", c) for p in b.get("paragraflar", []) for c in p.get("cumleler", [])]:
            i = x.get("id", "")
            m = re.fullmatch(rf"{re.escape(did)}-{tur}(\d+)", i)
            if not m: h.append(f"{i or '?'}: kimlik biçimi ({tur})"); continue
            if i in gor: h.append(f"{i}: çift kimlik")
            gor.add(i)
        if not b.get("baslik"): h.append(f"{b.get('id')}: başlık boş")
        for p in b.get("paragraflar", []):
            if kaynak_sayfalar is not None and p.get("sayfa") not in kaynak_sayfalar:
                h.append(f"{p.get('id')}: sayfa {p.get('sayfa')} kaynakta yok")
            if not p.get("cumleler"): h.append(f"{p.get('id')}: cümle yok")
            for c in p.get("cumleler", []):
                i, ses, ekran = c.get("id"), (c.get("ses") or "").strip(), (c.get("ekran") or "").strip()
                if not ses or not ekran: h.append(f"{i}: ses/ekran boş"); continue
                # yalnız markdown işaretleri (tıbbi gösterim serbest: "2n = 46", "benzo[a]piren")
                if re.search(r"\*\*|==|`|\||^\s*[#>]|^\s*-\s|\[\[", ses): h.append(f"{i}: ses metninde işaretleme (okunur)")
                if ses.endswith(("...", "…")) or ekran.endswith(("...", "…")): h.append(f"{i}: kesik metin")
                if len(ekran.replace("**", "").split()) > 28: h.append(f"{i}: ekran maddesi 28 kelimeden uzun")
                if c.get("duzey", 0) not in (0, 1, 2): h.append(f"{i}: duzey 0–2")
                for v in c.get("vurgu", []):
                    if v.get("tur") not in VURGU_TUR: h.append(f"{i}: vurgu türü {v.get('tur')!r}")
                    if v.get("metin", "").casefold() not in ekran.replace("**", "").casefold():
                        h.append(f"{i}: vurgu {v.get('metin')!r} ekran metninde yok")
                if uslup:
                    h += uslup(ses, f"{i}/ses") + uslup(ekran.replace("**", ""), f"{i}/ekran")
                if "slayt" in c or km:
                    capa_top += 1
                    sl = c.get("slayt")
                    if "slayt" not in c:
                        h.append(f"{i}: slayt çapası yok (satir/sekil ya da açıkça null)")
                    elif sl is None or not (sl.get("satir") or sl.get("sekil")):
                        capa_bos += 1
                    else:
                        sy = sl.get("sayfa", p.get("sayfa"))
                        if km and sy not in km:
                            h.append(f"{i}: slayt sayfası {sy} kaynakta yok")
                        for st in sl.get("satir") or []:
                            if km and sy in km and _katla(st) not in km[sy]:
                                h.append(f"{i}: slayt satırı s.{sy} metninde birebir yok: {st[:60]!r}")
    if capa_top and capa_bos / capa_top > CAPA_BOS_TAVAN:
        h.append(f"slayt çapası olmayan cümle %{100 * capa_bos // capa_top} (tavan %{int(CAPA_BOS_TAVAN * 100)})")
    return h


def turet(d):
    """v2 → eski biçim: bölüm başlığı '@@', paragraf = cümlelerin `ses` hâli; sayfa listesi paragraf başına."""
    satir, sayfalar = [f"# {d.get('baslik', '')}", ""], []
    for b in d["bolumler"]:
        satir.append(f"@@ {b['baslik']}")
        for p in b["paragraflar"]:
            satir += [" ".join(c["ses"].strip() for c in p["cumleler"]), ""]
            sayfalar.append(p["sayfa"])
    return "\n".join(satir).rstrip() + "\n", sayfalar


def vurgu_turet(d):
    """v2 → sesli ders vurgu dosyası (data/sesli_anlatim/vurgu/<anahtar>.json; vurgu_uret.py biçimi):
    {"surum": 1, "kaynak": "konusma_v2", "p": {"<paragraf sırası>": [[bas, son, "c"|"t", onem], …]}}
    Aralıklar turet() ile oluşan paragraf metninde (cümlelerin `ses` hâli, boşlukla birleşik). Önemli cümle: çıkmışa bağlı = 3,
    tuzak/sayı/tanım vurgusu = 2. Terim: vurgu ifadesi ses metninde geçiyorsa "t" (ekran ile ses farklıysa bulunmayan atlanır)."""
    out, i = {}, 0
    for b in d["bolumler"]:
        for p in b["paragraflar"]:
            konum, aralik = 0, []
            for j, c in enumerate(p["cumleler"]):
                ses = c["ses"].strip()
                bas, son = konum, konum + len(ses)
                turler = {v.get("tur") for v in c.get("vurgu", [])}
                onem = 3 if (c.get("cikmis") or "cikmis" in turler) else 2 if turler & {"tuzak", "sayi", "tanim"} else 0
                if onem:
                    aralik.append([bas, son, "c", onem])
                kucuk = ses.casefold()
                for v in c.get("vurgu", []):
                    m = (v.get("metin") or "").replace("**", "").strip()
                    k = kucuk.find(m.casefold()) if m else -1
                    if k >= 0:
                        aralik.append([bas + k, bas + k + len(m), "t", 0])
                konum = son + 1  # turet(): cümleler tek boşlukla birleşir
            if aralik:
                out[str(i)] = aralik
            i += 1
    return {"surum": 1, "kaynak": "konusma_v2", "p": out}


def k1_donustur(key):
    """Eski Kurul 1 metnine kimlik ver (içerik değişmez; ekran = ses; vurgu boş). Deeplink ve referans için."""
    md = (MEDS / f"data/sesli_anlatim/metin/{key}.md").read_text()
    hz = MEDS / f"data/sesli_anlatim/hizalama/{key}.json"
    psay = [p.get("sayfa") for p in json.loads(hz.read_text()).get("paragraflar", [])] if hz.exists() else []
    m = re.match(r"k(\d)-(\d{2})", key); did = f"k{m.group(1)}-{m.group(2)}"
    baslik = (re.search(r"^# (.+)$", md, re.M) or [None, key])[1]
    out = {"surum": 2, "ders_id": did, "anahtar": key, "baslik": baslik, "kaynak": "k1-donusum", "bolumler": []}
    nb = np_ = nc = 0; b = None
    for blok in re.split(r"\n\s*\n", md):
        for ln in blok.strip().splitlines():
            if ln.startswith("@@"):
                nb += 1; b = {"id": f"{did}-b{nb:02d}", "baslik": ln[2:].strip(), "paragraflar": []}
                out["bolumler"].append(b)
        govde = " ".join(ln for ln in blok.strip().splitlines() if not ln.startswith(("@@", "# "))).strip()
        if not govde:
            continue
        if b is None:
            nb += 1; b = {"id": f"{did}-b{nb:02d}", "baslik": baslik, "paragraflar": []}; out["bolumler"].append(b)
        cs = []
        for c in cumlelere(govde):
            nc += 1; cs.append({"id": f"{did}-c{nc:04d}", "ses": c, "ekran": c, "duzey": 0, "vurgu": []})
        sayfa = psay[np_] if np_ < len(psay) else None
        np_ += 1
        b["paragraflar"].append({"id": f"{did}-p{np_:03d}", "sayfa": sayfa, "cumleler": cs})
    return out


def capalar(d):
    """Paragraf başına cümle çapaları (yayinla.py → data/sesli_anlatim/capa/<key>.json → pdf_isaret.py)."""
    out = []
    for b in d["bolumler"]:
        for p in b["paragraflar"]:
            para_capa = []
            for c in p["cumleler"]:
                sl = c.get("slayt") or {}
                it = {
                    "ses": c["ses"].strip(),
                    "sayfa": sl.get("sayfa", p.get("sayfa")),
                    "satir": sl.get("satir") or [],
                    "sekil": sl.get("sekil"),
                }
                if sl.get("madde") is not None:
                    it["madde"] = sl["madde"]
                if sl.get("resim") is not None:
                    it["resim"] = sl["resim"]
                if sl.get("tablo") not in (None, False):
                    it["tablo"] = sl["tablo"]
                para_capa.append(it)
            out.append(para_capa)
    return out


def kaynak_metin(dizin):
    k = Path(dizin) / "kaynak.md"
    if not k.exists():
        return None
    out, cur = {}, None
    for ln in k.read_text().splitlines():
        m = re.match(r"=== SAYFA (\d+) ===", ln)
        if m:
            cur = int(m.group(1)); out[cur] = ""
        elif cur is not None:
            out[cur] += ln + "\n"
    return out


def kaynak_sayfa(dizin):
    k = Path(dizin) / "kaynak.md"
    return {int(x) for x in re.findall(r"=== SAYFA (\d+) ===", k.read_text())} if k.exists() else None


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dogrula"); g.add_argument("--turet"); g.add_argument("--k1-donustur")
    ap.add_argument("--yaz", help="--k1-donustur çıktısı (varsayılan stdout özeti)")
    a = ap.parse_args()
    if a.dogrula:
        d = json.loads((Path(a.dogrula) / "konusma_v2.json").read_text())
        h = dogrula(d, kaynak_sayfa(a.dogrula), kaynak_metin(a.dogrula))
        for x in h[:80]: print("HATA", x)
        n = sum(len(p["cumleler"]) for b in d["bolumler"] for p in b["paragraflar"])
        print(f"{len(d['bolumler'])} bölüm · {n} cümle · {len(h)} HATA"); sys.exit(1 if h else 0)
    if a.turet:
        d = json.loads((Path(a.turet) / "konusma_v2.json").read_text())
        md, s = turet(d)
        (Path(a.turet) / "konusma_metni.md").write_text(md)
        (Path(a.turet) / "konusma_sayfalari.json").write_text(json.dumps(s))
        (Path(a.turet) / "konusma_capalari.json").write_text(json.dumps(capalar(d), ensure_ascii=False))
        print(f"türetildi: {len(s)} paragraf")
    if a.k1_donustur:
        d = k1_donustur(a.k1_donustur)
        # K1 metni üslup kapısından ve madde uzunluğundan muaf (ekran = ses; toplu düzeltme yok, KURUL2 defteri)
        h = [x for x in dogrula(d) if "/ses" not in x and "/ekran" not in x and "28 kelime" not in x]
        n = sum(len(p["cumleler"]) for b in d["bolumler"] for p in b["paragraflar"])
        print(f"{d['ders_id']}: {len(d['bolumler'])} bölüm · {n} cümle · yapı HATA {len(h)}")
        for x in h[:10]: print("HATA", x)
        if a.yaz:
            Path(a.yaz).write_text(json.dumps(d, ensure_ascii=False, indent=1))
