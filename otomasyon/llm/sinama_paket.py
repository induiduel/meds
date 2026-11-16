#!/usr/bin/env python3
"""Görev paketleme katmanının saf (LLM'siz, ağsız) birim sınamaları — 2026-11-16.

Sınanan: önbellek dostu paket sırası, iş/önbellek anahtarı kararlılığı ve geriye dönük okuma, kimlik bazlı yama
birleştirmesi (örnek JSON), daraltılmış denetim seçimi, rol → model eşlemesinin ayrı aileye çözülmesi, ESLEME ↔
rotalar.json tutarlılığı. Hiçbir model/API çağrılmaz; iş klasörleri geçici dizinde açılır.

Çalıştır: python3 otomasyon/llm/sinama_paket.py   (0 hata → çıkış 0)
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

OTO = Path(__file__).resolve().parents[1]           # meds/otomasyon
sys.path.insert(0, str(OTO))
_TMP = tempfile.mkdtemp(prefix="sinama_paket_")
os.environ["MEDS_GOREV_DIR"] = _TMP                  # gerçek işlere dokunma (cekirdek içe aktarılmadan önce)
for _d in ("MEDS_AJAN_MODEL", "MEDS_AJAN_MODEL_DENETCI", "MEDS_AJAN_MODEL_HIZLI", "MEDS_HAT_ROL", "MEDS_HAT_ONBELLEK_SIRA",
           "MEDS_HAT_YAMA", "MEDS_HAT_DAR_DENETIM"):
    os.environ.pop(_d, None)

from llm import cekirdek as c                        # noqa: E402
from llm import model_sec as ms                      # noqa: E402
from llm import opendesign as od                     # noqa: E402
from llm import yonlendir as y                       # noqa: E402
from llm.gorevler import denetim as den              # noqa: E402

HATA: list[str] = []


def bekle(kosul: bool, ad: str):
    print(("  tamam  " if kosul else "  HATA   ") + ad)
    if not kosul:
        HATA.append(ad)


P = {"amac": "Sına.", "kurallar": [], "ek_kurallar": ["kural bir"], "girdi": "### Q1\nbir\n### Q2\niki",
     "baglam": "arka plan", "cikti_bicimi": "{\"sorular\": {}}", "denetim_listesi": ["madde"]}


def sina_sira():
    md = c.paket_md(P)
    basliklar = [s for s in md.splitlines() if s.startswith("# ")]
    bekle([b.split(" (")[0] for b in basliklar] == ["# GÖREV", "# KURALLAR", "# ÇIKTI BİÇİMİ", "# DENETİM LİSTESİ",
                                                     "# GİRDİ", "# BAĞLAM"], "paket sırası: sabit önek → GİRDİ · BAĞLAM")
    P2 = {**P, "girdi": "### Q9\nbaşka girdi", "baglam": ""}
    md2 = c.paket_md(P2)
    onek = md[:md.index("# GİRDİ")]
    bekle(md2.startswith(onek), "farklı girdide sabit önek bayt bayt aynı (istem önbelleği)")
    eski = c.paket_md(P, sira=False)
    bekle([s for s in eski.splitlines() if s.startswith("# ")][2] == "# GİRDİ", "eski sıra (sira=False) korunuyor")
    os.environ["MEDS_HAT_ONBELLEK_SIRA"] = "0"
    bekle(c.paket_md(P) == eski, "MEDS_HAT_ONBELLEK_SIRA=0 → eski sıra")
    os.environ.pop("MEDS_HAT_ONBELLEK_SIRA")
    # _girdi_suz başlık adıyla çalışır: Q2 bölümü düşer, ÇIKTI BİÇİMİ/DENETİM aynen kalır
    suz = y._girdi_suz(md, {"Q1"})
    bekle("### Q1" in suz and "### Q2" not in suz and "# ÇIKTI BİÇİMİ" in suz and "# BAĞLAM" in suz,
          "_girdi_suz yeni sırada başlık adına göre çalışıyor")


def sina_anahtar():
    a1, a2 = c.is_anahtari("parca_sorusu", P), c.is_anahtari("parca_sorusu", dict(reversed(list(P.items()))))
    bekle(a1 == a2, "iş anahtarı alan sırasından bağımsız ve kararlı")
    bekle(a1 != c.is_anahtari("parca_sorusu", {**P, "girdi": "farklı"}), "girdi değişince anahtar değişir")
    bekle(a1 != c.is_anahtari("denetim", P), "rol (görev) anahtara giriyor")
    # geriye dönük: eski anahtarla açılmış iş aynen döner (yeniden çağrı yok)
    hedef = "sinama-hedef"
    eski_id = f"parca_sorusu--{hedef}--{c.sha(c.paket_md(P, sira=False), 8)}"
    (Path(_TMP) / eski_id).mkdir(parents=True)
    (Path(_TMP) / eski_id / "durum.json").write_text("{}", encoding="utf-8")
    bekle(c.is_ac("parca_sorusu", hedef, {**P, "esleme": {}, "meta": {}}) == eski_id, "eski anahtarlı iş geriye dönük bulunuyor")
    yeni = c.is_ac("parca_sorusu", "sinama-yeni", {**P, "esleme": {}, "meta": {}})
    bekle(yeni.endswith(a1) and c.is_ac("parca_sorusu", "sinama-yeni", {**P, "esleme": {}, "meta": {}}) == yeni,
          "yeni iş girdi karmalı ve idempotent")
    k1 = y.onbellek_anahtari("A", "opendesign", "istem", "yazar")
    bekle(k1 == y.onbellek_anahtari("A", "opendesign", "istem", "yazar") and k1 != y.onbellek_anahtari("A", "opendesign", "istem", "denetci"),
          "önbellek anahtarı kararlı, role duyarlı")


def sina_yama():
    onceki = json.dumps({"sorular": {"Q1": {"kok": "a", "cozum": "x"}, "Q2": {"kok": "b", "cozum": "y"},
                                     "Q3": {"kok": "c", "cozum": "z"}}})
    bul = [{"yer": "Q2 çözüm", "tur": "tibbi_hata", "aciklama": "yanlış", "oneri": "düzelt"}]
    yi = y.yama_istemi("# GÖREV\ng\n# GİRDİ\n### Q1\nbir\n### Q2\niki\n### Q3\nüç", onceki, bul, "sorular", r"Q\d+")
    bekle(yi is not None and yi[1] == {"Q2"} and "### Q2" in yi[0] and "### Q1" not in yi[0] and '"Q1"' not in yi[0],
          "yama istemi yalnız bulgudaki kimliği ve onun girdi dilimini taşıyor")
    iyi = y.yama_birlestir(onceki, json.dumps({"sorular": {"Q2": {"kok": "b", "cozum": "Y"}}}), "sorular", {"Q2"})
    j = json.loads(iyi) if iyi else {}
    bekle(bool(j) and j["sorular"]["Q2"]["cozum"] == "Y" and j["sorular"]["Q1"]["cozum"] == "x" and list(j["sorular"]) == ["Q1", "Q2", "Q3"],
          "yama birleştirme: yalnız Q2 değişti, sıra/kimlikler korundu")
    bekle(y.yama_birlestir(onceki, json.dumps({"sorular": {"Q2": {"kok": "b"}}}), "sorular", {"Q2"}) is None,
          "alan eksik kayıt → None (tam yola düşer)")
    bekle(y.yama_birlestir(onceki, json.dumps({"sorular": {"Q2": {"kok": "b", "cozum": "y"}, "Q9": {}}}), "sorular", {"Q2"}) is None,
          "fazla/yabancı kimlik → None")
    bekle(y.yama_birlestir(onceki, "JSON değil", "sorular", {"Q2"}) is None, "ayrıştırılamayan cevap → None")
    bekle(y.yama_kimlikleri([{"yer": "genel üslup", "aciklama": "her yerde"}], {"Q1"}, r"Q\d+") is None,
          "kimliksiz bulgu → tam yazım")
    bekle(y.yama_istemi("# GİRDİ", onceki, [{"yer": "Q1 Q2 Q3"}], "sorular", r"Q\d+") is None,
          "bütün kimlikler bulgulu → yama yok (kazanç yok)")
    bekle(not y.yama_acik() and not den.dar_acik(), "yama ve dar denetim bayrakları varsayılan KAPALI")


def sina_dar():
    once = {f"Q{i}": {"v": i} for i in range(1, 31)}
    simdi = {**once, "Q3": {"v": 99}, "Q31": {"v": 31}}
    deg, orn = den.dar_sec(once, simdi, "tohum")
    bekle(deg == {"Q3", "Q31"}, "dar denetim: değişen ve yeni kimlikler seçildi")
    bekle(len(orn) == 3 and not (orn & deg), "örneklem değişmeyenlerin %10'u (29 → 3), değişenlerle kesişmez")
    bekle(den.dar_sec(once, simdi, "tohum")[1] == orn, "örneklem aynı tohumla belirlenimci")
    bekle(den.dar_sec({"Q1": 1}, {"Q1": 1}, "t")[1] == {"Q1"}, "tek kayıtta en az 1 örneklem")


def sina_rol():
    ya, de, hi = ms.ajan_model("yazar"), ms.ajan_model("denetci"), ms.ajan_model("hizli")
    print(f"    yazar {ya} → {od.model_id(ya)} · denetçi {de} → {od.model_id(de)} · hızlı {hi} → {od.model_id(hi)}")
    bekle(ms.aile(de) != ms.aile(ya), "denetçi yazardan AYRI aileye çözülüyor")
    bekle(ms.aile(ms.DENETCI) != ms.aile(ms.VARSAYILAN), "varsayılan DENETCI sabiti ayrı aile")
    os.environ["MEDS_AJAN_MODEL"] = "claude-opus-5-5"
    bekle(ms.aile(ms.ajan_model("denetci")) != "deepseek", "MEDS_AJAN_MODEL hepsini deepseek'e çekse de denetçi ayrı aile")
    os.environ.pop("MEDS_AJAN_MODEL")
    bekle(c.rol_sec("denetim") == "denetci" and c.rol_sec("kanit_bagla") == "hizli" and c.rol_sec("parca_sorusu") == "yazar",
          "görev → rol eşlemesi")
    os.environ["MEDS_HAT_ROL"] = "0"
    bekle(c.rol_sec("denetim") == "yazar", "MEDS_HAT_ROL=0 → rol bağlama kapalı")
    os.environ.pop("MEDS_HAT_ROL")
    yazar_aile = ms.aile(ya)
    dl = y._rol_modelleri(["deepseek-v4.1-flash", "glm-5.3-flash"], "denetci")
    bekle(dl == ["glm-5.3-flash"], "opendesign denetçi listesinden yazar ailesi atıldı")
    bekle(all(od.aile(x) != yazar_aile for x in y._rol_modelleri(["deepseek-v4.1-flash"], "denetci")),
          "yalnız yazar ailesi varken denetçi modeline düşülür")
    bekle(y._rol_modelleri(["a", "b"], "yazar") == ["a", "b"], "yazar rolünde model listesi aynen")
    for x in ms.DENETCI_YEDEK:
        bekle(od.model_id(x) != x, f"DENETCI_YEDEK {x} ESLEME'de tanımlı")


def sina_esleme():
    r = json.loads((OTO.parent / "scripts/altyapi/opendesign/rotalar.json").read_text(encoding="utf-8"))
    rot = {x["advertised"]: x["upstream"] for x in r["routes"]}
    uyumsuz = [f"{k}: ESLEME {v} ≠ rotalar {rot.get(k)}" for k, v in od.ESLEME.items() if rot.get(k) != v]
    bekle(not uyumsuz, "ESLEME ↔ rotalar.json tutarlı (statik)" + (f" — {uyumsuz}" if uyumsuz else ""))
    bekle(set(rot.values()) <= set(od.MODELLER), "rotalardaki her geçit kimliği MODELLER'de")


if __name__ == "__main__":
    for f in (sina_sira, sina_anahtar, sina_yama, sina_dar, sina_rol, sina_esleme):
        print(f.__name__)
        try:
            f()
        except Exception as e:  # noqa: BLE001
            bekle(False, f"{f.__name__} istisna: {e!r}")
    print(f"\n{len(HATA)} HATA")
    sys.exit(1 if HATA else 0)
