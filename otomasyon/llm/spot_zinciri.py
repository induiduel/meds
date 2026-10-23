#!/usr/bin/env python3
"""Ders zincirinin `onem` ve `cozucu` adımlarını GÖREV yoluyla yürütür (R4; Claude'suz ya da Claude yedekli).

  spot_zinciri.py onem   W kod [--katman A|Ü|C] [--golge]
  spot_zinciri.py cozucu W kod [--katman A|Ü|C] [--golge]
  spot_zinciri.py asistan W kod [--katman A|Ü|C] [--golge]   (plan: scripts/spot_cozucu/asistan_plan.py önceden)
  spot_zinciri.py sesli   TASLAK - [--katman A|Ü|C]         (ders işçisi taslağı → konusma_v2.json; Oracle bağlantısı ayrı adım)

onem  : her sayfa grubu için `onem_listesi` (hazırla → yönlendirici → kapı → uygula) → `spot_birlestir.onem` → W/onem/<kod>.json
asistan: `asistan_iskelet` (bölümler, taşıma, giriş/kapanış) → `asistan_nokta` partileri (≤3 nokta) bütün noktalar kabul
        edilene dek → `asistan_nokta.birlestir` → W/asistan/cikti/<kod>.json
cozucu: `cozucu_sorusu` partileri (her seferinde bekleyenlerin ilk 4'ü; kısmi kabul) bütün sorular kabul edilene dek
        (tavan: soru sayısı/2 + 6 parti) → `cozucu_sorusu.birlestir` → W/cozucu/<kod>.json
--golge: Claude'un dosyalarını EZMEZ — W/_golge/ aynasında çalışır (pdf_metin/girdi/cikmis/onem_haritasi bağlantı; çözücüde
         aynanın kendi önem listesi kullanılır). Ders zinciri `mod: golge` iken Claude adımından sonra bunu çağırır.
Çıkış: 0 tamam · 1 kapı/birleştirme HATA · 3 elle bekliyor · 4 Claude bütçesi · 5 model yanıt yok.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from llm import cekirdek as c  # noqa: E402
from llm import yonlendir  # noqa: E402
from llm.gorevler import _spot  # noqa: E402


def ayna(W: Path) -> Path:
    G = W / "_golge"
    for alt in ("pdf_metin", "girdi", "cikmis", "onem_haritasi", "asistan/plan"):
        (G / alt).mkdir(parents=True, exist_ok=True)
        for f in (W / alt).glob("*") if (W / alt).exists() else []:
            h = G / alt / f.name
            if not h.exists():
                h.symlink_to(f)
    return G


def _gorev(gorev: str, hedef: str, W: Path, katman: str | None, log) -> int:
    m = c.modul(gorev)
    is_id = c.is_ac(gorev, hedef, m.hazirla(hedef, {"w": str(W)}))
    d = c.durum(is_id)
    # kabul edilmiş iş her seferinde yeniden UYGULANIR (ucuz, aynı sonuç): çalışma klasörü yeniden kurulduysa
    # (prova taşındı, W silindi) "uygulandi" işareti hedef dosyanın varlığını garanti etmez (2026-10-23 prova)
    kabul = d.get("durum") in ("dogrulandi", "uygulandi")
    if kabul:
        h = yonlendir.kapi(is_id, c.oku(c.is_klasoru(is_id) / "cikti.json"))
        if h:                                  # kapı kabulden sonra sıkılaştı: iş yeniden koşar (önbellek + düzeltme turu)
            log(f"kabul edilmiş iş güncel kapıdan geçmiyor ({len(h)} HATA: {h[0][:80]}) → yeniden")
            c.durum_yaz(is_id, durum="hazir", neden="kabulden sonra kapı sıkılaştı", hatalar=h[:20]); kabul = False
    kod = 0 if kabul else yonlendir.calistir(is_id, katman, None, log=log)
    if kod != 0:
        return kod
    _, pj = c.paket(is_id)
    dosya = m.uygula(c.oku(c.is_klasoru(is_id) / "cikti.json"), pj["meta"], None, True)
    c.durum_yaz(is_id, durum="uygulandi", uygulandi=c.simdi())
    defter_yaz(W, pj["meta"].get("kod"), is_id, gorev, hedef, dosya)
    return 0


def defter_yaz(W: Path, kod: str | None, is_id: str, gorev: str, hedef: str, dosya) -> None:
    """Dersin kullandığı işler W/gorev/<kod>/isler.json: denetim ve düzeltme YALNIZ bunlara bakar (aynı W yolunda eski
    provalardan kalan işler karışmasın, 2026-10-24). Aynı dosyaya yazan eski iş defterden düşer."""
    if not kod:
        return
    p = W / "gorev" / kod / "isler.json"
    d = c.oku(p, {}) or {}
    dosya = str(dosya) if dosya else None
    d = {k: v for k, v in d.items() if not (dosya and v.get("dosya") == dosya and k != is_id)}
    d[is_id] = {"gorev": gorev, "hedef": hedef, "dosya": dosya, "zaman": c.simdi()}
    c.yaz(p, d)


def defter(W: Path, kod: str) -> dict:
    """Defter; dosyası artık olmayan (yerini yeni partiye bırakmış) iş kaydı düşer."""
    p = W / "gorev" / kod / "isler.json"
    d = c.oku(p, {}) or defter_kur(W, kod)
    temiz = {k: v for k, v in d.items() if not v.get("dosya") or Path(v["dosya"]).exists()}
    if len(temiz) != len(d):
        c.yaz(p, temiz)
    return temiz


def defter_kur(W: Path, kod: str) -> dict:
    """Defteri olmayan (2026-10-24 öncesi) klasör: W/gorev/<kod>/ altındaki parça/parti dosyalarını, içeriği birebir aynı
    olan kabul edilmiş işle eşler. Eşleşmeyen dosya defterde yer almaz (uyarı yazılır)."""
    import json as _j
    dosyalar = {f: _j.dumps(c.oku(f), sort_keys=True) for f in (W / "gorev" / kod).glob("*.json")
                if f.name.startswith(("onem_parca_", "cozucu_parti_"))}
    if not dosyalar:
        return {}
    ters = {v: k for k, v in dosyalar.items()}
    d = {}
    for pk in c.IS_DIZIN.glob("*/paket.json"):
        pj = c.oku(pk) or {}
        if pj.get("gorev") not in ("onem_listesi", "cozucu_sorusu") or (pj.get("meta") or {}).get("w") != str(W) \
                or pj["meta"].get("kod") != kod:
            continue
        ck = pk.parent / "cikti.json"
        f = ters.get(_j.dumps(c.oku(ck), sort_keys=True)) if ck.exists() else None
        if f:
            d[pk.parent.name] = {"gorev": pj["gorev"], "hedef": pj.get("hedef"), "dosya": str(f), "zaman": c.simdi(), "kuruldu": True}
    eksik = set(map(str, dosyalar)) - {v["dosya"] for v in d.values()}
    if eksik:
        print(f"  defter: {len(eksik)} dosya hiçbir işle eşleşmedi: {sorted(Path(x).name for x in eksik)[:4]}")
    c.yaz(W / "gorev" / kod / "isler.json", d)
    return d


def onem(W: Path, kod: str, katman: str | None = None, log=print) -> int:
    from llm import spot_birlestir
    P = _spot.parcalar(W, kod)
    for n in range(len(P)):
        k = _gorev("onem_listesi", f"x:{kod}/parca/{n}", W, katman, lambda s: log("   " + s))
        log(f"  onem parça {n + 1}/{len(P)} (s. {P[n][0]}–{P[n][1]}): kod {k}")
        if k != 0:
            return k
    return spot_birlestir.onem(W, kod, log=lambda s: log("  " + s))


def cozucu(W: Path, kod: str, katman: str | None = None, log=print) -> int:
    from llm.gorevler import cozucu_sorusu as CS
    eski = CS.eskiyen(W, kod)
    if eski:                    # önem listesi değişmiş: eskiyen kayıtlar düşer, aşağıdaki partilerde yeniden üretilir
        log(f"  {kod}: {CS.eskiyenleri_dusur(W, kod, eski)} eskimiş çözücü kaydı düştü ({sorted(eski)[:3]})")
    toplam = len(CS.sorular(W, kod))
    tavan = toplam // 2 + 6
    for i in range(tavan):
        b = CS.bekleyen(W, kod)
        if not b:
            break
        k = _gorev("cozucu_sorusu", f"x:{kod}/parti/0", W, katman, lambda s: log("   " + s))
        log(f"  çözücü parti {i + 1}: {len(b)} bekleyen → kod {k}")
        if k != 0:
            return k
    else:
        log(f"  {kod}: {len(CS.bekleyen(W, kod))} soru {tavan} partide kabul edilemedi"); return 1
    return CS.birlestir(W, kod, log=lambda s: log("  " + s))


def asistan(W: Path, kod: str, katman: str | None = None, log=print) -> int:
    from llm.gorevler import _asistan, asistan_nokta as AN
    k = _gorev("asistan_iskelet", f"x:{kod}/iskelet/0", W, katman, lambda s: log("   " + s))
    log(f"  asistan iskeleti: kod {k}")
    if k != 0:
        return k
    toplam = len(_asistan.son_noktalar(W, kod))
    tavan = toplam // 2 + 6
    for i in range(tavan):
        if not _asistan.bekleyen_parti(W, kod):
            break
        k = _gorev("asistan_nokta", f"x:{kod}/nokta/0", W, katman, lambda s: log("   " + s))
        kalan = toplam - len(_asistan.yapilan(W, kod))
        log(f"  asistan parti {i + 1}: kalan {kalan} nokta → kod {k}")
        if k != 0:
            return k
    else:
        log(f"  {kod}: noktalar {tavan} partide bitmedi"); return 1
    return AN.birlestir(W, kod, log=lambda s: log("  " + s))


def sesli(W: Path, kod: str = "", katman: str | None = None, log=print) -> int:
    """W = ders işçisi taslak klasörü (kaynak.md, sayfa_haritasi.json, deck.json …): bölüm bölüm `sesli_bolum` → birleştirme."""
    from llm.gorevler import sesli_bolum as SB
    B = SB.bolumler(W)
    if not B:
        log("sayfa_haritasi.json bölümü yok"); return 2
    for n in range(len(B)):
        k = _gorev("sesli_bolum", f"{SB.ders_id(W) or 'ders'}/bolum/{n}", W, katman, lambda s: log("   " + s))
        log(f"  sesli bölüm {n + 1}/{len(B)} ({B[n]['baslik'][:40]}): kod {k}")
        if k != 0:
            return k
    return SB.birlestir(W, log=lambda s: log("  " + s))


def _denetle(W: Path, kod: str, isler: list[str], katman, log) -> int:
    """Verilen işleri toplu paketlerle denetler; her işin denetim.json'u + durum.denetim yazılır."""
    D = c.modul("denetim")
    gruplar: dict[str, list] = {}
    for is_id in isler:
        gruplar.setdefault(c.durum(is_id).get("aile") or "?", []).append(is_id)
    paketler = []
    for aile, L in gruplar.items():
        paket, boy = [], 0
        for is_id in L:
            g, o, _, _ = D.is_goster(is_id)
            n = len(g) + len(o)
            if paket and boy + n > D.TOPLU_SINIR:
                paketler.append((aile, paket)); paket, boy = [], 0
            paket.append(is_id); boy += n
        if paket:
            paketler.append((aile, paket))
    for i, (aile, paket) in enumerate(paketler, 1):
        hedef = f"toplu:{kod}:{aile}:{c.sha(','.join(paket), 10)}"
        den = c.is_ac("denetim", hedef, D.hazirla(hedef, {"isler": paket}))
        k = yonlendir.calistir(den, katman, None, log=lambda m: log("   " + m))
        log(f"  denetim paketi {i}/{len(paketler)} ({len(paket)} iş, yazar {aile}): kod {k}")
        if k != 0:
            return k
        D.uygula(c.oku(c.is_klasoru(den) / "cikti.json"), c.paket(den)[1]["meta"])
        for is_id in paket:
            c.durum_yaz(is_id, denetci=c.durum(den).get("model"))
    return 0


def _engel(is_id: str) -> list[dict]:
    dj = c.oku(c.is_klasoru(is_id) / "denetim.json") or {}
    engel = set(c.kayit(c.paket(is_id)[1]["gorev"]).get("denetim_engelleyen") or [])
    return [b for b in dj.get("bulgular", []) if b["tur"] in engel]


def _guncel_mi(is_id: str) -> bool:
    """İş, son uygulanışından SONRA denetlendi mi (düzeltilen ya da yeni iş yeniden denetlenir)."""
    d = c.durum(is_id).get("denetim") or {}
    if not d:
        return False
    if d.get("icerik"):
        return d["icerik"] == c.modul("denetim").icerik_izi(is_id)
    return d.get("zaman", "") >= c.durum(is_id).get("uygulandi", "")      # eski kayıt (izsiz)


def denetim(W: Path, kod: str, katman: str | None = None, log=print, duzeltme_turu: int = 2) -> int:
    """Bağımsız denetim + bulgu düzeltme (görev yolu). Dersin defterindeki (`isler.json`) önem parçaları ve çözücü
    partileri yazarın ajanı DIŞINDAN bir denetçiye TOPLU paketlerle gider (D1, D2 …). Engelleyici bulgulu iş, bulgularla
    yazara geri döner (`yonlendir.bulgu_duzelt`), kapıları geçerse yeniden uygulanır; önem değiştiyse ders yeniden
    birleştirilir ve örnek sorusu değişen çözücü kayıtları yeniden üretilir; değişen işler yeniden denetlenir. Kalan
    engelleyici bulgu varsa kod 8. Rapor W/denetim/<kod>.md. Önceden denetlenmiş ve değişmemiş iş yeniden denetlenmez."""
    from llm import spot_birlestir
    from llm.gorevler import cozucu_sorusu as CS
    for tur in range(duzeltme_turu + 1):
        D_ = defter(W, kod)
        isler = [i for i, v in D_.items() if v["gorev"] in ("onem_listesi", "cozucu_sorusu")
                 and c.durum(i).get("durum") in ("dogrulandi", "uygulandi")]
        if not isler:
            log(f"  {kod}: denetlenecek görev işi yok"); return 2
        bekleyen = [i for i in isler if not _guncel_mi(i)]
        log(f"  denetim turu {tur}: {len(isler)} iş, denetlenecek {len(bekleyen)}")
        if bekleyen:
            k = _denetle(W, kod, bekleyen, katman, log)
            if k != 0:
                return k
        engelli = {i: _engel(i) for i in isler if _engel(i)}
        if not engelli or tur == duzeltme_turu:
            break
        duzelen = {"onem_listesi": 0, "cozucu_sorusu": 0}
        bekleyen_oturum = False
        for is_id, eng in engelli.items():
            if int(c.durum(is_id).get("denetim_duzeltme", 0)) >= 2:     # iki düzeltmeden sonra hâlâ engel: insan/Claude kararı
                log(f"  {is_id[-8:]}: iki denetim düzeltmesinden sonra hâlâ {len(eng)} engelleyici bulgu — atlandı"); continue
            bul = (c.oku(c.is_klasoru(is_id) / "denetim.json") or {}).get("bulgular", eng)
            # ikinci düzeltme profilin `son_care` ajanında (karma: yerel Claude — "OpenCode yetmezse Claude", 2026-10-24;
            # tek ajanlı profilde aynı ajanın öteki modeli); MEDS_AJAN_CLAUDE=0 ise Claude atlanır
            son = yonlendir._claudesuz(yonlendir.profil()[1].get("son_care") or [])
            ikinci = int(c.durum(is_id).get("denetim_duzeltme", 0)) >= 1 and son
            k = yonlendir.bulgu_duzelt(is_id, bul, katman, log=lambda m: log("   " + m), ajanlar=son if ikinci else None)
            gorev = D_[is_id]["gorev"]
            log(f"  bulgu düzeltme {gorev} {is_id[-8:]} ({len(eng)} engelleyici): kod {k}")
            bekleyen_oturum = bekleyen_oturum or k == 3
            if k == 0:
                _, pj = c.paket(is_id)
                dosya = c.modul(gorev).uygula(c.oku(c.is_klasoru(is_id) / "cikti.json"), pj["meta"], None, True)
                c.durum_yaz(is_id, durum="uygulandi", uygulandi=c.simdi())
                defter_yaz(W, kod, is_id, gorev, D_[is_id]["hedef"], dosya)
                duzelen[gorev] += 1
        if duzelen["onem_listesi"]:
            spot_birlestir.onem(W, kod, log=lambda s: log("  " + s))
            eski = CS.eskiyen(W, kod)
            if eski:   # örnek sorusu değişen/silinen çözücü kayıtları partilerden düşer, yeniden üretilir
                CS.eskiyenleri_dusur(W, kod, eski)
                log(f"  önem değişti: {len(eski)} örnek soru → çözücü yeniden")
                k = cozucu(W, kod, katman, log)
                if k != 0:
                    return k
            else:
                CS.birlestir(W, kod, log=lambda s: log("  " + s))
        elif duzelen["cozucu_sorusu"]:
            CS.birlestir(W, kod, log=lambda s: log("  " + s))
        if bekleyen_oturum and not any(duzelen.values()):
            return 3                    # oturum kuyruğunda bulgu düzeltmesi bekliyor (gorev.py kuyruk)
        if not any(duzelen.values()):
            break
    # rapor (defterdeki bütün işler)
    satir, engel_say = [f"# Bağımsız denetim — {kod} (görev yolu, toplu, {c.simdi()})", ""], 0
    for is_id, v in defter(W, kod).items():
        if v["gorev"] not in ("onem_listesi", "cozucu_sorusu"):
            continue
        dj = c.oku(c.is_klasoru(is_id) / "denetim.json") or {}
        eng = _engel(is_id)
        engel_say += len(eng)
        du = c.durum(is_id)
        satir.append(f"## {v['gorev']} · {is_id} — karar {dj.get('karar')} ({len(dj.get('bulgular', []))} bulgu, {len(eng)} "
                     f"engelleyici) · yazar {du.get('model')} · denetçi {du.get('denetci')}"
                     + (f" · denetimle düzeltildi ×{du['denetim_duzeltme']}" if du.get("denetim_duzeltme") else ""))
        satir += [f"- [{b['tur']}{' — ENGEL' if b in eng else ''}] {b['yer']}: {b['aciklama']} → {b['oneri']}"
                  for b in dj.get("bulgular", [])]
        satir.append("")
    (W / "denetim").mkdir(parents=True, exist_ok=True)
    (W / "denetim" / f"{kod}.md").write_text("\n".join(satir) + f"\nToplam engelleyici bulgu: {engel_say}\n", encoding="utf-8")
    log(f"  denetim: engelleyici bulgu {engel_say}")
    if any(c.durum(i).get("oturum_duzeltme") == "bekliyor" for i in defter(W, kod)):
        log("  oturum kuyruğunda bulgu düzeltmesi bekliyor (gorev.py kuyruk)"); return 3
    return 0 if engel_say == 0 else 8


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("adim", choices=["onem", "cozucu", "asistan", "sesli", "denetim"]); ap.add_argument("W"); ap.add_argument("kod")
    ap.add_argument("--katman", choices=["A", "Ü", "C"]); ap.add_argument("--golge", action="store_true")
    ap.add_argument("--profil", help="ajan profili: karma | opencode | antigravity | claude | commandcode (butce.json)")
    a = ap.parse_args()
    if a.profil:
        os.environ["MEDS_AJAN_PROFIL"] = a.profil
    yonlendir.profil()                      # bilinmeyen profil burada durur
    W = Path(a.W)
    sonuc = _calistir_adim(a, W)
    if sonuc == 3:                          # oturum kuyruğu: kaldığı yerden sürdürmek için komut kaydı
        c.kuyruk_ekle(zincir=[sys.executable, str(Path(__file__).resolve())] + sys.argv[1:], cwd=os.getcwd(),
                      ortam={k: os.environ[k] for k in ("MEDS_AJAN_PROFIL", "MEDS_AJAN_CLAUDE", "MEDS_GOREV_KATMAN") if k in os.environ})
    return sonuc


def _calistir_adim(a, W: Path) -> int:
    import os
    katman = a.katman or os.environ.get("MEDS_GOREV_KATMAN") or None   # prova: ajan katmanı (A), Claude'suz
    if a.golge:
        os.environ["MEDS_AJAN_CLAUDE"] = "0"     # gölge: Claude'un yaptığını Claude'suz ajanlarla yeniden yap
        W = ayna(W)
    return {"onem": onem, "cozucu": cozucu, "asistan": asistan, "sesli": sesli, "denetim": denetim}[a.adim](W, a.kod, katman)


if __name__ == "__main__":
    sys.exit(main())
