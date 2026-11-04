#!/usr/bin/env python3
"""Öğrenci önem kapsama kapısı: geçmiş yıl öğrencilerinin en çok çalıştığı yerler ders katmanlarında karşılık buluyor mu?

  python3 scripts/ogrenci_onem/kapi.py <k2-xx> [--metin <md>] [--onem <json>] [--sorular <json>] [--sayfalar <sayfalar.json>] [--json]

Birim (src/data/ogrenci_onem/<ders>.json) ↔ katman parçası bge-m3 kosinüs benzerliği (CPU :8094):
  anlatım paragrafı (sesli ders metni), önem maddesi (bilgi + detay), örnek soru (kök + doğru şık + açıklama).
Kurallar (docs/OGRENCI_ONEM_YONTEMI.md §5):
  A birimi → anlatımda VAR + önem listesinde VAR + ≥2 örnek soru   (eksik = HATA)
  B birimi → anlatımda VAR + ≥1 örnek soru                          (eksik = UYARI)
  C birimi → yalnız anlatım kapsamı raporlanır                       (bilgi)
Bu yılın (2026-27) PDF'inde karşılığı olmayan birim (--sayfalar verildiyse en iyi sayfa benzerliği < ESIK_SAYFA) HATA
üretmez, "2026-27 slaytında yok" UYARIsı verir: hoca konuyu çıkarmış olabilir; çıkmış kanıtlıysa kısa ek + örnek soru önerilir.
Dosya verilmezse ders kimliğinden bulunur (metin: data/sesli_anlatim/metin/<ders>-*.md en yeni sürüm; örnek soru:
src/data/ornek_sorular/k2/<ders>-*.json; önem: src/data/k2*_onem/<kod>.json). Çıkış: HATA varsa 1.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agents"))
from ortak import CIKTI, KOK, bilgiler, cumleler, jetonlar, oku_json  # noqa: E402

ESIK, ESIK_YAKIN, ESIK_KOK = 0.62, 0.80, 0.5  # cümle düzeyi; kalibrasyon: OGRENCI_ONEM_YONTEMI.md §5
ESIK_CEVAP = 0.55  # çıkmış önermesinde cevap terimini taşıyan cümlenin kök+cevap metnine yakınlığı
ESIK_SORU = 0.65   # birim ↔ örnek soru (kök + doğru şık + açıklama)
ESIK_SAYFA = 0.55
ESIK_SLAYT_KOK = 0.4  # bilgi parçasının köklerinin en az %40'ı bir sayfada geçiyorsa slaytta sayılır (H490)
KAPSAM_A, KAPSAM_B = 0.6, 0.4  # anlatımda kapsanan bilgi payı alt sınırı


def birim_metni(b: dict) -> str:
    el = " ".join(e.get("metin", "") for e in b.get("el_yazisi") or [])
    vur = " ".join(b.get("vurgulu") or [])
    return f"{b.get('baslik', '')}. {vur} {b.get('metin', '')} {el}"[:1500]


SAYI = {"sıfır": 0, "bir": 1, "iki": 2, "üç": 3, "dört": 4, "beş": 5, "altı": 6, "yedi": 7, "sekiz": 8, "dokuz": 9, "on": 10,
        "yirmi": 20, "otuz": 30, "kırk": 40, "elli": 50, "altmış": 60, "yetmiş": 70, "seksen": 80, "doksan": 90, "yüz": 100, "bin": 1000}


EKLER = {"tir", "dir", "tır", "dır", "tür", "dür", "tur", "dur", "i", "ı", "u", "ü", "si", "sı", "su", "sü", "e", "a", "ye", "ya", "de",
         "da", "te", "ta", "den", "dan", "ten", "tan", "inci", "ıncı", "uncu", "üncü", "nci", "ncı", "ncu", "ncü", "lik", "lık", "lük", "luk"}


def sayilastir(t: str) -> str:
    """Sesli metin sayıyı yazıyla yazar ("on beş"); çıkmış rakamla ("15"). Yazıyla sayı dizileri rakama çevrilir (yalnız "bir" çevrilmez)."""
    out, dizi = [], []

    def bosalt():
        if not dizi:
            return
        if dizi == ["bir"]:
            out.append("bir")
        else:
            top, ara = 0, 0
            for w in dizi:
                v = SAYI[w]
                if v in (100, 1000):
                    ara = max(ara, 1) * v
                    if v == 1000: top += ara; ara = 0
                else:
                    ara += v
            out.append(str(top + ara))
        dizi.clear()

    for w in re.split(r"(\s+)", t):
        k = w.strip().lower().strip(",.;:()")
        if k in SAYI:
            dizi.append(k)
            continue
        if w.isspace() and dizi:
            continue
        ek = next((s for s in sorted(SAYI, key=len, reverse=True) if k.startswith(s) and k[len(s):] in EKLER), None)
        if ek and (dizi or ek != "bir"):  # "beştir", "beşi": sayı ekle biter
            dizi.append(ek); bosalt()
            continue
        bosalt(); out.append(w)
    bosalt()
    return " ".join(x for x in out if x and not x.isspace())


def kokler(t: str) -> set[str]:
    t = sayilastir(t)
    return {w[:5] for w in jetonlar(t) if w not in DURAK} | set(re.findall(r"\d+", t))


DURAK = {"aşağıdakilerden", "hangisi", "hangisidir", "olarak", "ile", "için", "veya", "gibi", "daha", "olan", "değildir",
         "yanlıştır", "doğrudur", "denir", "verilir", "görülür", "şeklinde", "durumda", "durumu", "hastada", "hastanın"}


ROMA = ["I", "II", "III", "IV", "V", "VI"]


def roma_ac(bilgi: str, cevap: str) -> str:
    """"I, II ve IV" gibi öncüllü cevap anlatım cümlesinde geçemez: cevabı seçilen öncüllerin metnine açar (H490)."""
    secilen = re.findall(r"\b(I{1,3}|IV|V|VI)\b", cevap or "")
    if not secilen or re.sub(r"[IVX,\sve]+", "", cevap):
        return cevap
    on = dict(re.findall(r"\b(I{1,3}|IV|V|VI)\.\s*(.+?)(?=\s+(?:I{1,3}|IV|V|VI)\.\s|\s+Bunlardan|\?|→|$)", bilgi))
    parca = [on[r] for r in secilen if r in on]
    return " ".join(parca) if len(parca) == len(secilen) else cevap


def kapsandi(bilgi: str, bv, cumle: list[str], CV, ck: list[set], cevap: str = "") -> tuple[bool, float, str]:
    """Bilgi parçası cümlelerden birinde var mı: anlamca çok yakın (≥ ESIK_YAKIN) ya da yakın (≥ ESIK) + kelime kökü
    örtüşmesi ≥ ESIK_KOK. Yalnız vektör yanıltır: "spastisite ve rijidite tonus artışıdır" cümlesi rijiditenin tanımını
    soran bilgiye 0,69 verir ama tanımı içermez."""
    if not cumle:
        return False, 0.0, ""
    s = CV @ bv
    ce = kokler(cevap)
    if ce:  # çıkmış önermesi: uzun vaka kökü cevabı gölgeler → cevabın kökleri aynı cümlede + konu yakınlığı (≥ ESIK_CEVAP)
        for j in s.argsort()[::-1][:25]:
            if float(s[j]) >= ESIK_CEVAP and len(ce & ck[j]) / len(ce) >= 0.6:
                return True, round(float(s[j]), 3), cumle[j]
    bk = kokler(bilgi)
    en = (0.0, -1)
    for j in s.argsort()[::-1][:8]:
        sk = float(s[j])
        ort = len(bk & ck[j]) / len(bk) if bk else 0
        if sk >= ESIK_YAKIN or (sk >= ESIK and ort >= ESIK_KOK):
            return True, round(sk, 3), cumle[j]
        en = max(en, (sk, j))
    return False, round(en[0], 3), cumle[en[1]] if en[1] >= 0 else ""


def dosya_bul(ders: str, kod: str) -> dict:
    mt = sorted((KOK / "data/sesli_anlatim/metin").glob(f"{ders}-*.md"),
                key=lambda p: int(m.group(1)) if (m := re.search(r"-v(\d+)\.md$", p.name)) else 1)
    so = sorted((KOK / "src/data/ornek_sorular/k2").glob(f"{ders}-*.json"))
    on = sorted(KOK.glob(f"src/data/k2*_onem/{kod}.json"))
    return dict(metin=mt[-1] if mt else None, sorular=so[0] if so else None, onem=on[0] if on else None)


def anlatim_cumleleri(md: Path) -> list[str]:
    """Sesli metin okunuşla yazılır ("Düşen", "de me de"); çıkmış ve not yazımla ("Duchenne", "DMD"). v2 dosyası varsa her
    cümlenin ekran maddesi de (yazımla) aday cümle olur — ikisinden biri bilgiyi taşıyorsa kapsanmış sayılır."""
    out = [c for c in cumleler(md.read_text()) if not c.startswith("@@")]
    v2 = oku_json(KOK / "data/sesli_anlatim/v2" / f"{md.stem}.json")
    if v2:
        out += [c["ekran"].replace("**", "") for b in v2.get("bolumler", []) for p in b.get("paragraflar", [])
                for c in p.get("cumleler", []) if len(c.get("ekran", "")) > 15]
    return out


def onem_cumleleri(p: Path) -> list[str]:
    d = oku_json(p, {}) or {}
    out = []
    for m in d.get("maddeler", []):
        out += cumleler(" ".join([m.get("baslik", "") + ".", m.get("bilgi", ""), *(m.get("alt") or []), m.get("detay", "")]))
    return out


def sorular(p: Path) -> list[str]:
    d = oku_json(p, {}) or {}
    out = []
    for k in d.get("kazanimlar", []):
        for q in k.get("sorular", []):
            dg = (q.get("secenekler") or {}).get(q.get("dogru"), "")
            out.append(f"{q.get('soru', '')} {dg}. {q.get('aciklama', '')}"[:1200])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ders")
    ap.add_argument("--metin"); ap.add_argument("--onem"); ap.add_argument("--sorular"); ap.add_argument("--sayfalar")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    from lib import embed  # noqa: E402

    on = oku_json(CIKTI / f"{a.ders}.json")
    if not on:
        print(f"{a.ders}: öğrenci önem verisi yok (bu ders notlarda geçmiyor) — kapı uygulanmaz"); return 0
    f = dosya_bul(a.ders, on["kod"])
    f = {k: Path(getattr(a, k)) if getattr(a, k) else v for k, v in f.items()}
    katman = {"anlatim": anlatim_cumleleri(f["metin"]) if f["metin"] else [],
              "onem": onem_cumleleri(f["onem"]) if f["onem"] else [],
              "soru": sorular(f["sorular"]) if f["sorular"] else []}
    KV = {k: (embed(v, model="bge-m3") if v else None) for k, v in katman.items()}
    KK = {k: [kokler(c) for c in v] for k, v in katman.items()}
    B = on["birimler"]
    UV = embed([birim_metni(b) for b in B], model="bge-m3")
    BL = [bilgiler(b, on) for b in B]
    for L in BL:  # öncüllü çıkmış: karşılaştırma seçilen öncüllerin metniyle, genel ölçütle (H490)
        for x in L:
            ac = roma_ac(x["metin"], x.get("cevap", ""))
            if x.get("cevap") and ac != x["cevap"]:
                x["soru_metni"], x["metin"], x["cevap"] = x["metin"], ac, ""
    duz = [x["metin"] for L in BL for x in L]
    DV = embed(duz, model="bge-m3") if duz else []
    SV = None
    if not a.sayfalar:  # varsayılan: tam hat ders klasörü (meds_temp/ogrenci_ders/<ders>/sayfalar.json)
        vs = KOK.parent / "meds_temp" / "ogrenci_ders" / a.ders / "sayfalar.json"
        if vs.exists(): a.sayfalar = str(vs)
    SL = None  # bu yılın slayt sayfaları: bilgi parçası slaytta AÇIKÇA yoksa kapsamdan çıkar (H490)
    if a.sayfalar:
        _sp = json.loads(Path(a.sayfalar).read_text())
        _sn = [v for v in _sp.values() if len(v.strip()) > 20]
        if _sn:
            SL = (embed([v[:1500] for v in _sn], model="bge-m3"), [kokler(v) for v in _sn])
    if a.sayfalar:
        sp = json.loads(Path(a.sayfalar).read_text())
        sn = [k for k, v in sp.items() if len(v.strip()) > 20]
        SV = (sn, embed([sp[k][:1500] for k in sn], model="bge-m3"))
    hata, uyari, sonuc, bilgi_notu = [], [], [], []
    # Doğrulanmış eşleme (H490): kapının kaçırdığı ama anlatımda BİREBİR bulunan bilgi ya da bu yılın slaytıyla çelişen
    # çıkmış bilgisi. Kapı her kaydı kendisi denetler: cümle anlatımda olmalı + bilgiye yakınlık ≥ ESIK_CEVAP; çelişkide
    # slayt alıntısı o sayfada geçmeli. Denetimi geçmeyen kayıt HATA'dır (uydurma eşleme ile kapı geçilemez).
    ES = oku_json(CIKTI / "esleme" / f"{a.ders}.json") or {"kayitlar": []}
    _sp_es = json.loads(Path(a.sayfalar).read_text()) if a.sayfalar else {}
    _nrm = lambda t: re.sub(r"\s+", " ", t).strip().lower()  # noqa: E731
    _anl = [_nrm(c) for c in katman["anlatim"]]
    esleme = {}
    for k in ES["kayitlar"]:
        etk = f"eşleme {k.get('birim')} «{k.get('bilgi', '')[:40]}»"
        if not k.get("gerekce"):
            hata.append(f"{etk}: gerekçe yok"); continue
        if k.get("tur") == "anlatim":
            cl = k.get("cumle") if isinstance(k.get("cumle"), list) else [k.get("cumle", "")]
            yok = [c for c in cl if len(_nrm(c)) < 15 or not any(_nrm(c) in x for x in _anl)]
            if yok:
                hata.append(f"{etk}: cümle anlatımda yok → {yok[0][:60]}"); continue
            k["cumle"] = " ".join(cl)
            v = embed([k["bilgi"], k["cumle"]], model="bge-m3")
            if float(v[0] @ v[1]) < ESIK_CEVAP:
                # kısa not ↔ uzun cümle: anlam benzerliği doğal olarak düşük → anahtar terim kanıtı (cümlede birebir,
                # notta ≥ 0,8 harf benzerliği: "cingulat" ~ "singulat"); anahtarsız kayıt reddedilir
                from difflib import SequenceMatcher
                an = k.get("anahtar") or []
                bn = _nrm(k["bilgi"])
                def notta(t):
                    t = _nrm(t); n = len(t)
                    return any(SequenceMatcher(None, t, bn[i:i + n]).ratio() >= 0.8 for i in range(max(1, len(bn) - n + 1)))
                eksik = [t for t in an if _nrm(t) not in _nrm(k["cumle"]) or not notta(t)]
                if not an or eksik:
                    hata.append(f"{etk}: benzerlik {float(v[0] @ v[1]):.2f} < {ESIK_CEVAP} ve anahtar kanıtı yok"
                                + (f" ({eksik[0]})" if eksik else "")); continue
        elif k.get("tur") == "celiski":
            sa = _nrm(k.get("slayt_alinti", ""))
            if len(sa) < 8 or sa not in _nrm(_sp_es.get(str(k.get("sayfa")), "")):
                hata.append(f"{etk}: slayt alıntısı s.{k.get('sayfa')} sayfasında yok"); continue
        elif k.get("tur") == "slayt_disi":  # bu yılın slaytında hiç geçmeyen konu: terimlerin YOKLUĞU tüm sayfalarda denetlenir
            yt = k.get("yok_terimler") or []
            tum = _nrm(" ".join(_sp_es.values()))
            var = [t for t in yt if _nrm(t) in tum]
            if len(yt) < 2 or var:
                hata.append(f"{etk}: slayt dışı kanıtı yok" + (f" ('{var[0]}' slaytta geçiyor)" if var else " (en az 2 terim)")); continue
            k["tur"] = "celiski"
        else:
            hata.append(f"{etk}: tür anlatim|celiski|slayt_disi olmalı"); continue
        esleme[(k["birim"], _nrm(k["bilgi"])[:60])] = k
    n = 0
    for b, u, L in zip(B, UV, BL):
        r = dict(id=b["id"], oncelik=b["oncelik"], baslik=b["baslik"], bilgi=[])
        for x in L:
            bv = DV[n]; n += 1
            e = dict(x)
            _es = esleme.get((b["id"], _nrm(x["metin"])[:60]))
            if _es and _es["tur"] == "celiski":
                e["slaytta"] = False; e["celiski"] = _es["gerekce"]
            elif SL is not None:  # slaytta karşılığı olmayan parça anlatıma giremez (kural 28) → kapsamdan çıkar
                _bk = kokler(x["metin"]) - {w for w in kokler(x["metin"]) if w.isdigit() and len(w) < 2}
                _sim = float((SL[0] @ bv).max())
                _ort = max((len(_bk & k) / len(_bk) for k in SL[1]), default=0) if _bk else 1
                # yalnız ikisi de düşükse slayt dışı: anlamca uzak (< ESIK_SAYFA) VE kök örtüşmesi < ESIK_SLAYT_KOK
                e["slaytta"] = not (_sim < ESIK_SAYFA and _ort < ESIK_SLAYT_KOK)
                e["slayt_benzerlik"], e["slayt_kok"] = round(_sim, 3), round(_ort, 2)
            for k in ("anlatim", "onem"):
                if k == "anlatim" and _es and _es["tur"] == "anlatim":
                    e["anlatim"], e["anlatim_benzerlik"], e["en_yakin_cumle"], e["esleme"] = True, 1.0, _es["cumle"][:160], _es["gerekce"]
                    continue
                ok, sk, cm = kapsandi(x["metin"], bv, katman[k], KV[k], KK[k], x.get("cevap", "")) if KV[k] is not None else (None, 0, "")
                e[k] = ok; e[k + "_benzerlik"] = sk
                if k == "anlatim":
                    e["en_yakin_cumle"] = cm[:160]
            r["bilgi"].append(e)
        if KV["soru"] is not None:
            r["soru"] = int(((KV["soru"] @ u) >= ESIK_SORU).sum())
        if SV:
            s2 = SV[1] @ u; j = int(s2.argmax())
            r["y26_sayfa"], r["y26_benzerlik"] = SV[0][j], round(float(s2[j]), 3)
        gecerli = [e for e in r["bilgi"] if e.get("slaytta") is not False]
        r["slayt_disi"] = [e["metin"][:90] for e in r["bilgi"] if e.get("slaytta") is False]
        nb = len(gecerli)
        r["anlatim_kapsam"] = round(sum(bool(e.get("anlatim")) for e in gecerli) / nb, 2) if nb and KV["anlatim"] is not None else None
        r["onem_kapsam"] = round(sum(bool(e.get("onem")) for e in gecerli) / nb, 2) if nb and KV["onem"] is not None else None
        sonuc.append(r)
        if r["slayt_disi"]:
            bilgi_notu.append(f"{b['id']}: slaytta yok, kapsamdan çıkarıldı → " + " | ".join(r["slayt_disi"][:4]))
        yok26 = (SV is not None and r["y26_benzerlik"] < ESIK_SAYFA) or (r["bilgi"] and not gecerli)
        etiket = f"{b['id']} [{b['oncelik']}] {b['baslik'][:60]}"
        eksik_b = [e["metin"][:90] for e in gecerli if e.get("anlatim") is False and (b["oncelik"] == "A" or e["tur"] != "vurgu")]
        if b["oncelik"] == "A":
            eks = []
            if r["anlatim_kapsam"] is not None and r["anlatim_kapsam"] < KAPSAM_A: eks.append(f"anlatım %{int(100 * r['anlatim_kapsam'])}")
            if any(e["tur"] == "cikmis" and e.get("anlatim") is False for e in gecerli): eks.append("çıkmış bilgisi anlatımda yok")
            if r["onem_kapsam"] is not None and r["onem_kapsam"] == 0: eks.append("önem listesinde yok")
            if r.get("soru") is not None and r["soru"] < 2: eks.append(f"örnek soru {r['soru']}<2")
            if eks:
                (uyari if yok26 else hata).append(f"{etiket}: {'; '.join(eks)}" + (" (2026-27 slaytında yok)" if yok26 else "")
                                                   + ("\n        eksik bilgiler: " + " | ".join(eksik_b[:6]) if eksik_b else ""))
        elif b["oncelik"] == "B":
            eks = []
            if r["anlatim_kapsam"] is not None and r["anlatim_kapsam"] < KAPSAM_B: eks.append(f"anlatım %{int(100 * r['anlatim_kapsam'])}")
            if r.get("soru") is not None and r["soru"] < 1: eks.append("örnek soru yok")
            if eks:
                uyari.append(f"{etiket}: {'; '.join(eks)}" + ("\n        eksik bilgiler: " + " | ".join(eksik_b[:6]) if eksik_b else ""))
    eksik_katman = [k for k, v in katman.items() if not v]
    if a.json:
        print(json.dumps(dict(ders=a.ders, dosyalar={k: str(v) if v else None for k, v in f.items()}, eksik_katman=eksik_katman,
                              hata=hata, uyari=uyari, birimler=sonuc), ensure_ascii=False, indent=1))
    else:
        print(f"{a.ders} {on['konu']} · dosyalar: " + ", ".join(f"{k}={v.name if v else '—'}" for k, v in f.items()))
        for k in ("A", "B", "C"):
            rs = [r for r in sonuc if r["oncelik"] == k]
            bl = [e for r in rs for e in r["bilgi"]]
            if rs:
                an = sum(bool(e.get("anlatim")) for e in bl); oo = sum(bool(e.get("onem")) for e in bl); so = sum((r.get("soru") or 0) > 0 for r in rs)
                print(f"  {k}: {len(rs)} birim, {len(bl)} bilgi · anlatımda {an} · önemde {oo} · sorusu olan birim {so}")
        for h in hata: print("  HATA ", h)
        for w in uyari: print("  UYARI", w)
        for x in bilgi_notu: print("  BİLGİ", x)
        if eksik_katman: print("  BİLGİ katman yok:", ", ".join(eksik_katman))
        print(f"  → {len(hata)} HATA, {len(uyari)} UYARI")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
