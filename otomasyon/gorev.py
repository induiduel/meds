#!/usr/bin/env python3
"""Görev sözleşmesi — her LLM'in yapabileceği betikleştirilmiş içerik işleri (ICERIK_MOTORU_V3.md §14).

  gorev.py hazirla  <gorev> <hedef> [--ayar k=v …]   paket.md + paket.json (çözücü); is_id yazar
  gorev.py calistir <is_id> [--katman A|B|Ü|C|elle] [--aile opencode|commandcode|antigravity|claude (A) · gemini|groq|openrouter (Ü)]
                                                     yönlendirici: betik → ücretsiz bulut → Claude (bütçeli) → kapı
  gorev.py derle    <is_id> [--cevap DOSYA]          elle/dış cevabı derle + doğrula (cevap.txt varsayılan)
  gorev.py dogrula  <is_id>                          cikti.json'u yeniden doğrula
  gorev.py uygula   <is_id> [--cikis DİZİN] [--k1-izin] [--denetimsiz]
  gorev.py yap      <gorev> <hedef> [--katman …] [--denetle] [--uygula] [--cikis DİZİN]   hepsi bir arada
  gorev.py durum    [<is_id>]                        tek iş ya da son 30 iş
  gorev.py defter                                    görevler, katmanlar, Claude bütçesi
  gorev.py [--profil P] …                              ajan profili (karma | opencode | antigravity | claude | commandcode)
  gorev.py profil [P]                                  profilleri ve kullanımı göster; P verilirse kalıcı varsayılan olur
  gorev.py kuyruk [--surdur] [--json]                  oturum kuyruğu (profil oturum): paketler, sürdürülecek zincirler
  gorev.py duzeltme-derle <is_id>                      oturumun denetim bulgusu düzeltmesini kapılardan geçir
  gorev.py sinama                                    gidiş-dönüş + kapı öz-sınaması (model çağırmaz)
Çıkış: 0 tamam · 1 kapı HATA/reddedildi · 2 kullanım · 3 elle bekliyor · 4 bütçe bekliyor · 5 model yanıt vermedi.
İş klasörü: meds_temp/gorev/<is_id>/ (paket.md, paket.json, durum.json, cevap_N.txt, cikti.json, rapor.json, denetim.json).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm import cekirdek as c  # noqa: E402
from llm import yonlendir  # noqa: E402


def _ayar(liste):
    out = {}
    for x in liste or []:
        k, _, v = x.partition("=")
        out[k] = v
    return out


def hazirla(gorev: str, hedef: str, ayar: dict | None = None) -> str:
    m = c.modul(gorev)
    is_id = c.is_ac(gorev, hedef, m.hazirla(hedef, ayar or {}))
    print(is_id)
    return is_id


def derle(is_id: str, cevap_yolu: str | None = None) -> int:
    d = c.is_klasoru(is_id)
    p = Path(cevap_yolu) if cevap_yolu else d / "cevap.txt"
    if not p.exists():
        print(f"cevap yok: {p}")
        return 2
    cevap = p.read_text(encoding="utf-8")
    if p != d / "cevap.txt":
        (d / "cevap.txt").write_text(cevap, encoding="utf-8")
    cikti, hatalar = yonlendir.degerlendir(is_id, cevap)
    ad = "oturum" if c.durum(is_id).get("bekleyen") == "oturum" else "elle"     # oturum kuyruğundan gelen cevap
    yonlendir.kaydet_sonuc(is_id, cikti, hatalar, katman="elle", model=ad)
    for h in hatalar:
        print("  HATA", h)
    if hatalar and ad == "oturum":          # oturum düzeltip yeniden derler; iş kuyrukta kalır
        c.durum_yaz(is_id, hatalar=hatalar[:20])
    else:
        c.durum_yaz(is_id, durum="dogrulandi" if not hatalar else "reddedildi", katman="elle", aile=ad, model=ad,
                    **({"hatalar": hatalar[:20]} if hatalar else {}))
    if not hatalar and ad == "oturum":
        c.kuyruk_cikar(is_id)
    print(f"{len(hatalar)} HATA")
    return 0 if not hatalar else 1


def dogrula(is_id: str) -> int:
    _, pj = c.paket(is_id)
    cikti = c.oku(c.is_klasoru(is_id) / "cikti.json")
    if cikti is None:
        print("cikti.json yok")
        return 1
    hatalar = yonlendir.kapi(is_id, cikti)
    for h in hatalar:
        print("  HATA", h)
    print(f"{len(hatalar)} HATA")
    return 0 if not hatalar else 1


def uygula(is_id: str, cikis: str | None = None, k1_izin: bool = False, denetimsiz: bool = False) -> int:
    d = c.durum(is_id)
    if d.get("durum") not in ("dogrulandi", "uygulandi"):
        print(f"uygulanamaz: durum {d.get('durum')}")
        return 1
    _, pj = c.paket(is_id)
    k = c.kayit(pj["gorev"])
    den = d.get("denetim") or {}
    engel = set(k.get("denetim_engelleyen") or ["tibbi_hata", "kaynak_disi", "celiski", "cevap_hatali", "belirsiz_soru",
                                                    "uslup", "bicim", "diger"])
    engelleyen = sorted(set(den.get("turler") or ([] if den.get("karar") != "duzelt" else ["diger"])) & engel)
    if den.get("karar") == "duzelt" and engelleyen:
        print(f"uygulanamaz: bağımsız denetim engelleyici bulgu {engelleyen} — {c.is_klasoru(is_id) / 'denetim.json'}")
        return 1
    if k.get("denetim_zorunlu") and not den and not denetimsiz and cikis is None:
        print("uygulanamaz: bu görevde bağımsız denetim zorunlu (gorev.py yap denetim <is_id>)")
        return 1
    if dogrula(is_id) != 0:
        return 1
    cikti = c.oku(c.is_klasoru(is_id) / "cikti.json")
    yol = c.modul(pj["gorev"]).uygula(cikti, pj["meta"], Path(cikis) if cikis else None, k1_izin)
    if cikis is None:
        c.durum_yaz(is_id, durum="uygulandi", uygulandi=c.simdi(), yazildi=str(yol))
    print(f"yazıldı: {yol}")
    return 0


def durum_goster(is_id: str | None):
    if is_id:
        import json
        print(json.dumps(c.durum(is_id), ensure_ascii=False, indent=1))
        return
    isler = sorted((p for p in c.IS_DIZIN.glob("*/durum.json")), key=lambda p: p.stat().st_mtime)[-30:]
    for p in isler:
        d = c.oku(p, {})
        den = (d.get("denetim") or {}).get("karar", "")
        print(f"{d.get('durum', '?'):15} {d.get('model', '') or '':38} {den:7} {p.parent.name}")


def defter_goster():
    for g in c.defter().values():
        print(f"{g['id']:14} {'/'.join(g['katmanlar']):5} aileler={','.join(g.get('yazar_aileleri', []))} "
              f"risk={g.get('risk')} denetim_zorunlu={g.get('denetim_zorunlu')}  hedef: {g['hedef']}")
    print(f"Claude bütçesi bugün kalan: {yonlendir.claude_kalan()} çağrı")


def yap(a) -> int:
    is_id = hazirla(a.gorev, a.hedef, _ayar(a.ayar))
    kod = yonlendir.calistir(is_id, a.katman, a.aile)
    if kod != 0:
        return kod
    if a.denetle:
        den = hazirla("denetim", is_id)
        kd = yonlendir.calistir(den, None, None)
        if kd != 0:
            return kd
        dur = uygula(den)
        if dur != 0:
            return dur
        print(f"denetim: {c.durum(is_id).get('denetim')}")
    if a.uygula or a.cikis:
        return uygula(is_id, a.cikis, a.k1_izin)
    return 0


def duzeltme_derle(is_id: str) -> int:
    """Oturum kuyruğu: duzeltme_paket.md'ye yazılan duzeltme_cevap.txt → bütün kapılar; geçerse çıktı yazılır, zincir
    sürdürülünce (kuyruk --surdur) yeniden uygulanır ve yeniden denetlenir."""
    d = c.is_klasoru(is_id)
    p = d / "duzeltme_cevap.txt"
    if not p.exists():
        print(f"cevap yok: {p}"); return 2
    _, kabul = yonlendir._bulgu_hazirla(is_id, (c.oku(d / "denetim.json") or {}).get("bulgular", []))
    yeni, h = yonlendir.bulgu_degerlendir(is_id, p.read_text(encoding="utf-8"), kabul)
    for x in h:
        print("  HATA", x)
    if not h and yeni is not None:
        yonlendir.bulgu_kabul(is_id, yeni, "oturum", "oturum")
        c.durum_yaz(is_id, oturum_duzeltme="hazir")
        c.kuyruk_cikar(is_id)
    print(f"{len(h)} HATA")
    return 0 if not h else 1


def kuyruk_komut(surdur: bool, json_cikti: bool) -> int:
    """Oturum kuyruğu (profil `oturum`): çözülecek paketler + kaldığı yerden sürdürülecek zincirler."""
    import json
    import subprocess
    k = c.kuyruk()
    for is_id in list(k["isler"]):                      # çözülmüş ya da artık beklemeyen kayıtlar düşer
        du = c.durum(is_id)
        tip = k["isler"][is_id]["tip"]
        if (tip == "is" and du.get("durum") != "elle_bekliyor") or (tip == "duzeltme" and du.get("oturum_duzeltme") != "bekliyor"):
            c.kuyruk_cikar(is_id)
    k = c.kuyruk()
    if surdur:
        for anahtar, z in list(k["zincirler"].items()):
            print(f"▶ sürdürülüyor: {' '.join(z['argv'][1:])[:160]}", flush=True)
            r = subprocess.run(z["argv"], cwd=z.get("cwd"), env={**__import__("os").environ, **z.get("ortam", {})})
            print(f"  kod {r.returncode}{' (yeni paket kuyrukta)' if r.returncode == 3 else ''}", flush=True)
            if r.returncode != 3:
                c.kuyruk_cikar(zincir_anahtar=anahtar)
        return kuyruk_komut(False, json_cikti)
    satirlar = []
    for is_id, v in k["isler"].items():
        _, pj = c.paket(is_id)
        dd = c.is_klasoru(is_id)
        paket = dd / ("paket.md" if v["tip"] == "is" else "duzeltme_paket.md")
        cevap = dd / ("cevap.txt" if v["tip"] == "is" else "duzeltme_cevap.txt")
        satirlar.append({"is_id": is_id, "tip": v["tip"], "gorev": pj["gorev"], "paket": str(paket), "cevap": str(cevap),
                         "boyut": paket.stat().st_size if paket.exists() else 0,
                         "bagimsiz": pj["gorev"] == "denetim",
                         "derle": f"python3 {Path(__file__).resolve()} {'derle' if v['tip'] == 'is' else 'duzeltme-derle'} {is_id}",
                         "son_hatalar": c.durum(is_id).get("hatalar", [])[:5]})
    if json_cikti:
        print(json.dumps({"isler": satirlar, "zincirler": list(k["zincirler"].values())}, ensure_ascii=False, indent=1))
        return 0
    print(f"Oturum kuyruğu: {len(satirlar)} paket, {len(k['zincirler'])} bekleyen zincir")
    for x in satirlar:
        print(f"- {x['tip']:9s} {x['gorev']:16s} {x['boyut']:>7d} bayt{'  [BAĞIMSIZ: yeni bağlamlı alt ajan]' if x['bagimsiz'] else ''}\n"
              f"    paket: {x['paket']}\n    cevap: {x['cevap']}\n    sına : {x['derle']}"
              + (f"\n    son hatalar: {x['son_hatalar']}" if x["son_hatalar"] else ""))
    for z in k["zincirler"].values():
        print(f"- zincir: {' '.join(z['argv'][1:])[:150]}")
    if not satirlar and k["zincirler"]:
        print("Paket kalmadı → sürdür: gorev.py kuyruk --surdur")
    return 0


def profil_komut(ad: str | None) -> int:
    """Profilleri, etkin olanı ve bugünkü ajan/Claude kullanımını gösterir; ad verilirse kalıcı varsayılanı değiştirir."""
    import json
    p = c.LLM / "butce.json"
    b = json.loads(p.read_text(encoding="utf-8"))
    P = {k: v for k, v in b["profiller"].items() if k != "aciklama"}
    if ad:
        if ad not in P:
            print(f"bilinmeyen profil {ad}; seçenekler: {', '.join(P)}"); return 2
        b["etkin_profil"] = ad
        p.write_text(json.dumps(b, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"kalıcı profil: {ad}")
    etkin = yonlendir.profil()[0]
    for k, v in P.items():
        print(f"{'▶' if k == etkin else ' '} {k:12s} yazar: {' → '.join(v['yazar'])}  ·  denetçi: {' → '.join(v['denetci'])}"
              f"  ·  son çare: {', '.join(v.get('son_care') or [])}")
    s = yonlendir._ajan_sayac()
    print(f"bugün ({s['gun']}): " + ", ".join(f"{a} {n}" for a, n in s["cagri"].items()) +
          f" · Claude {yonlendir._sayac()['cagri']} (kalan {yonlendir.claude_kalan()})")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profil", help="bu çağrı için ajan profili (karma | opencode | antigravity | claude | commandcode)")
    alt = ap.add_subparsers(dest="komut", required=True)
    h = alt.add_parser("hazirla"); h.add_argument("gorev"); h.add_argument("hedef"); h.add_argument("--ayar", action="append")
    r = alt.add_parser("calistir"); r.add_argument("is_id"); r.add_argument("--katman", choices=["A", "B", "Ü", "C", "elle"])
    r.add_argument("--aile")
    dr = alt.add_parser("derle"); dr.add_argument("is_id"); dr.add_argument("--cevap")
    dg = alt.add_parser("dogrula"); dg.add_argument("is_id")
    u = alt.add_parser("uygula"); u.add_argument("is_id"); u.add_argument("--cikis"); u.add_argument("--k1-izin", action="store_true")
    u.add_argument("--denetimsiz", action="store_true")
    y = alt.add_parser("yap"); y.add_argument("gorev"); y.add_argument("hedef"); y.add_argument("--ayar", action="append")
    y.add_argument("--katman", choices=["A", "B", "Ü", "C", "elle"]); y.add_argument("--aile"); y.add_argument("--denetle", action="store_true")
    y.add_argument("--uygula", action="store_true"); y.add_argument("--cikis"); y.add_argument("--k1-izin", action="store_true")
    s = alt.add_parser("durum"); s.add_argument("is_id", nargs="?")
    alt.add_parser("defter")
    alt.add_parser("sinama")
    pf = alt.add_parser("profil"); pf.add_argument("ad", nargs="?", help="verilirse kalıcı varsayılan profil olur (gece hattı)")
    kq = alt.add_parser("kuyruk"); kq.add_argument("--surdur", action="store_true"); kq.add_argument("--json", action="store_true")
    dd = alt.add_parser("duzeltme-derle"); dd.add_argument("is_id")
    a = ap.parse_args()
    if a.profil:
        import os
        os.environ["MEDS_AJAN_PROFIL"] = a.profil
    if a.komut == "profil":
        return profil_komut(a.ad)
    if a.komut == "kuyruk":
        return kuyruk_komut(a.surdur, a.json)
    if a.komut == "duzeltme-derle":
        return duzeltme_derle(a.is_id)
    if a.komut == "hazirla":
        hazirla(a.gorev, a.hedef, _ayar(a.ayar)); return 0
    if a.komut == "calistir":
        return yonlendir.calistir(a.is_id, a.katman, a.aile)
    if a.komut == "derle":
        return derle(a.is_id, a.cevap)
    if a.komut == "dogrula":
        return dogrula(a.is_id)
    if a.komut == "uygula":
        return uygula(a.is_id, a.cikis, a.k1_izin, a.denetimsiz)
    if a.komut == "yap":
        return yap(a)
    if a.komut == "durum":
        durum_goster(a.is_id); return 0
    if a.komut == "defter":
        defter_goster(); return 0
    if a.komut == "sinama":
        from llm.sinama import sinama
        return sinama.main()
    return 2


if __name__ == "__main__":
    sys.exit(main())
