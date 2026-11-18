#!/usr/bin/env python3
"""Okunuş farkı raporu — mevcut klipler ortak yolla (ses_metin.hazirla) yeniden üretilseydi motora giden okunuş DEĞİŞİR miydi?

SES ÜRETMEZ, GPU/LLM KULLANMAZ. Klip karması (dosya adı) değişmez; bu rapor yalnız "yeniden üretim ADAYI" listesidir —
üretimi kullanıcı komutuyla GPU'da yapılır (cozucu_ses_gpu.sh).

Kaynak metne ulaşma: kayit.json satırları metin tutmaz (Öğren `cumleler`, terim `m` dışında). Klip metni, üreten betiğin kendi
`klipler()` işleviyle girdisinden yeniden kurulur ve KAYITTAKİ KARMAYLA DOĞRULANIR (eşleşmeyen klip "kaynak yok" sayılır;
eski girdisi değişmiş ya da başka betikçe yazılmış klipler — hoca ara soru, çıkmış not — burada açıkça raporlanır).
Eski yol = 2026-11-16 öncesi her betiğin motora verdiği metin (çözücü/spot: klip metni aynen; patoloji asistanı/ek modül:
okunus.duzelt; Öğren/sesli ders: ema_isci anahtar yolu; terim: Kurul 2 yolu).

Çıktı: ../meds_temp/ses_ortak/okunus_farki.jsonl (değişecek her klip: modül, klasör, klip, eski/yeni okunuş) + ozet.json + ekrana tablo.
Kullanım: python3 scripts/uretim/ses_ortak/okunus_farki.py [--ornek 5]
"""
from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path

_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import collections  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

MEDS = _kok.MEDS
U = _kok.SCRIPTS / "uretim"
for _p in ("ses_ortak", "sesli_anlatim", "patoloji_cozucu", "patoloji_onem", "ogren_ses"):
    sys.path.insert(0, str(U / _p))
import ses_klip as SK  # noqa: E402
import ses_metin as SM  # noqa: E402

CIKTI = MEDS.parent / "meds_temp/ses_ortak"
TEMP = MEDS.parent / "meds_temp"


def _yukle(ad: str, yol: Path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(ad, yol)
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(yol.parent))
    spec.loader.exec_module(m)
    return m


def parcalar(cumleler: list[str]) -> list[str]:
    return [p.strip() for c in cumleler for p, _ in re.findall(r"(.+?)(\|\||\||$)", c.strip()) if p.strip()]


class Rapor:
    def __init__(self, ornek: int):
        self.say = collections.defaultdict(lambda: collections.Counter())
        self.out = (CIKTI / "okunus_farki.jsonl").open("w", encoding="utf-8")
        self.ornekler: list[dict] = []
        self.ornek = ornek

    def klip(self, modul: str, klasor: str, klip: str, cumleler: list[str] | None, eski, yeni):
        s = self.say[modul]
        s["klip"] += 1
        if cumleler is None:
            s["kaynak_yok"] += 1
            return
        fark = [(p, e, n) for p in parcalar(cumleler) if (e := eski(p)) != (n := yeni(p))]
        if not fark:
            return
        s["degisecek"] += 1
        # cumleler + her parçanın yeni okunuşu: yeniden üretim (ses_klip --yeniden) motora tam olarak bunu verir (2026-11-17)
        satir = {"modul": modul, "klasor": klasor, "klip": klip,
                 "fark": [{"metin": p, "eski": e, "yeni": n} for p, e, n in fark],
                 "cumleler": cumleler, "okunus": {p: yeni(p) for p in parcalar(cumleler)}}
        self.out.write(json.dumps(satir, ensure_ascii=False) + "\n")
        if len([o for o in self.ornekler if o["modul"] == modul]) < 1 and len(self.ornekler) < 40:
            self.ornekler.append({"modul": modul, "klip": f"{klasor}/{klip}", "eski": fark[0][1][:160], "yeni": fark[0][2][:160]})


def cozucu_kaynaklari(sc, C, A_spot, A_pat) -> dict[tuple[str, str], dict[str, list[str]]]:
    """(veri klasörü, kod) → aday klip metinleri (karma ile doğrulanacak)."""
    K: dict[tuple[str, str], dict] = collections.defaultdict(dict)

    class _S:  # spot Ema'nın klip metni dönüşümü (KS.uzat) — model yüklemeden
        surum = ""

        def ses_metni(self, c, ekk):
            return sc_ks.uzat(c, ekk)
    import kisaltma_ses as sc_ks
    S = _S()
    for brans_dir in sorted((TEMP / "spot_cozucu").glob("*")):
        for f in sorted((brans_dir / "cikti_tam").glob("*.json")):
            try:
                K[(f"{brans_dir.name}_cozucu", f.stem)].update(sc.klipler(json.loads(f.read_text(encoding="utf-8")), S))
            except Exception:
                pass
        for f in sorted((brans_dir / "asistan" / "cikti").glob("*.json")):
            try:
                K[(f"{brans_dir.name}_asistan", f.stem)].update(A_spot.klipler(json.loads(f.read_text(encoding="utf-8")), S))
            except Exception:
                pass
    for f in sorted((TEMP / "patoloji_ornek26/cozucu/cikti_tam").glob("*.json")):
        K[("patoloji_cozucu", f.stem)].update(C.klipler(json.loads(f.read_text(encoding="utf-8"))))
    for f in sorted((TEMP / "patoloji_onem/asistan2/cikti").glob("*.json")):
        try:
            K[("patoloji_asistan", f.stem)].update(A_pat.klipler(json.loads(f.read_text(encoding="utf-8"))))
            K[("patoloji_asistan", f.stem + "#spot")].update(A_spot.klipler(json.loads(f.read_text(encoding="utf-8")), S))
        except Exception:
            pass
    K[("ortak", "ortak")].update(C.ORTAK)
    for f in sorted((MEDS / "src/data/ders_analizi").glob("k*.json")):
        try:
            o = json.loads(f.read_text(encoding="utf-8"))
            d = K[(f"{o['sesKlasor']['brans']}_cozucu", o["sesKlasor"]["kod"])]
            for b in [*o["analiz"], *(o.get("ozet") or [])]:
                ekk = sc.kisaltmalar(*b["ses"])
                d[b["klip"]] = [S.ses_metni(c, ekk) for c in b["ses"]]
        except Exception:
            pass
    return K


def main() -> int:
    a = sys.argv[1:]
    ornek = int(a[a.index("--ornek") + 1]) if "--ornek" in a else 5
    CIKTI.mkdir(parents=True, exist_ok=True)
    R = Rapor(ornek)
    import ema_isci as E
    import okunus as O
    sc = _yukle("spot_ses", U / "spot_cozucu/ses.py")
    A_spot = _yukle("spot_asistan_ses", U / "spot_cozucu/asistan_ses.py")
    sys.modules["ses"] = sc
    C = _yukle("cozucu_ses", U / "patoloji_cozucu/cozucu_ses.py")
    A_pat = _yukle("pat_asistan_ses", U / "patoloji_onem/asistan_ses.py")
    hiz = E.HIZ
    kaynak = cozucu_kaynaklari(sc, C, A_spot, A_pat)

    def ayni(p):
        return p

    uzun = SM.okuyucu(yol="uzun")
    # 1) çözücü / asistan klasörleri (spot + patoloji + ders analizi + hoca ara soru …)
    for kp in sorted(MEDS.glob("data/*_cozucu/ses/*/kayit.json")) + sorted(MEDS.glob("data/*_asistan/ses/*/kayit.json")):
        veri = kp.relative_to(MEDS / "data").parts[0]  # data/<veri>/ses/<kod>/kayit.json
        kod = kp.parent.name
        kayit = SK.kayit_oku(kp)
        pat_asistan = veri == "patoloji_asistan"
        adaylar = {**kaynak.get((veri, kod), {}), **(kaynak.get(("ortak", "ortak")) if kod == "ortak" else {})}
        spot_aday = kaynak.get((veri, kod + "#spot"), {})
        for klip, satir in kayit.items():
            cum, eski = None, ayni
            h = satir.get("h")
            for surum in (f"ema-2|{hiz}", f"ema-1|{hiz}"):
                for aday in (adaylar, spot_aday):
                    c = aday.get(klip)
                    if c is not None and SK.klip_karmasi(surum, c) == h:
                        cum = c
                        # patoloji_onem/asistan_ses (ema-1) motora okunus.duzelt veriyordu; spot yolu (ema-2) metni aynen
                        eski = O.duzelt if surum.startswith("ema-1") and pat_asistan else ayni
                        break
                if cum is not None:
                    break
            yeni = SM.okuyucu(modul=veri) if eski is O.duzelt else uzun
            R.klip(veri, kod, klip, cum, eski, yeni)
    # 2) patoloji_cozucu_alt (metin girdisi data/patoloji_cozucu_alt/metin; eski motor: metin aynen)
    for kp in sorted(MEDS.glob("data/patoloji_cozucu_alt/ses/*/kayit.json")):
        g = MEDS / "data/patoloji_cozucu_alt/metin" / f"{kp.parent.name}.json"
        sorular = {str(q["no"]): q for q in json.loads(g.read_text(encoding="utf-8"))["sorular"]} if g.exists() else {}
        for klip, satir in SK.kayit_oku(kp).items():
            q = sorular.get(klip)
            cum = [c for st in q["ses"].splitlines() for c in SK.cumlele(st) if any(ch.isalpha() for ch in c)] if q else None
            if cum is not None and SK.klip_karmasi(f"alt-1|{hiz}", cum) != satir.get("h"):
                cum = None
            R.klip("patoloji_cozucu_alt", kp.parent.name, klip, cum, ayni, uzun)
    # 3) Öğren (kayıt cümleleri tutar)
    for kp in sorted(MEDS.glob("data/ogren_ses/*/kayit.json")):
        deste = kp.parent.name
        yeni = SM.okuyucu(ders=deste)
        for klip, satir in SK.kayit_oku(kp).items():
            R.klip("ogren_ses", deste, klip, satir.get("cumleler"), lambda p, d=deste: SM.eski_ders_okunus(p, d), yeni)
    # 4) terim sesleri (kayıt okunan metni `m` tutar; motor: konus(m))
    ts = _yukle("terim_ses_uret", U / "sesli_anlatim/terim_ses_uret.py")
    for h, satir in SK.kayit_oku(MEDS / "data/terim_ses/kayit.json").items():
        m = satir.get("m")
        R.klip("terim_ses", "terim_ses", h, [ts.konus(m)] if m else None,
               lambda p: SM.eski_ders_okunus(p, "k2-00-"), uzun)
    # 5) ek modüller (klip.json `v` = metin özeti)
    ek = _yukle("ek_ses", U / "ek_modul/ses.py")
    for dz in sorted((MEDS / "src/data/ek_moduller").glob("*/klip.json")):
        modul = dz.parent.name
        try:
            K = ek.klipler(modul)
        except Exception:
            K = {}
        yeni = SM.okuyucu(modul=modul)
        for klip, satir in json.loads(dz.read_text(encoding="utf-8")).items():
            c = K.get(klip)
            if c is not None and hashlib.sha1("\n".join(c).encode()).hexdigest()[:12] != satir.get("v"):
                c = None
            # ek modül paragrafları (| ayırıcısı yok): parça = paragraf
            R.klip(f"ek_modul:{modul}", modul, klip, [x.replace("|", " ") for x in c] if c else c, O.duzelt, yeni)
    # 6) sesli ders (klipli; okunan metin klip özetinde): MEDS_OKUNUS_ORTAK=1 açılırsa değişecek paragraflar
    for md in sorted((MEDS / "data/sesli_anlatim/metin").glob("*.md")):
        key = md.stem
        paras = [p.strip() for p in md.read_text(encoding="utf-8").split("\n\n") if p.strip() and not p.lstrip().startswith("#")]
        yeni = SM.okuyucu(ders=key)
        for i, p in enumerate(paras):
            R.klip("sesli_ders(MEDS_OKUNUS_ORTAK=1)", key, f"p{i + 1}", [p.replace("|", " ")],
                   lambda x, k=key: SM.eski_ders_okunus(x, k), yeni)
    R.out.close()
    ozet = {m: dict(s) for m, s in sorted(R.say.items())}
    (CIKTI / "ozet.json").write_text(json.dumps({"sozluk_surum": SM.SOZLUK_SURUM, "moduller": ozet, "ornekler": R.ornekler},
                                                ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{'modül':42} {'klip':>7} {'değişecek':>10} {'kaynak yok':>11}")
    top = collections.Counter()
    for m, s in ozet.items():
        top.update(s)
        print(f"{m:42} {s.get('klip', 0):7} {s.get('degisecek', 0):10} {s.get('kaynak_yok', 0):11}")
    print(f"{'TOPLAM':42} {top['klip']:7} {top['degisecek']:10} {top['kaynak_yok']:11}")
    print(f"→ {CIKTI / 'okunus_farki.jsonl'} · {CIKTI / 'ozet.json'} (sözlük {SM.SOZLUK_SURUM})")
    for o in R.ornekler[:ornek]:
        print(f"  [{o['modul']}] {o['klip']}\n    eski: {o['eski']}\n    yeni: {o['yeni']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
