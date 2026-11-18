#!/usr/bin/env python3
"""Read-once ders bağlamı — aşamalar ham slaytı/şablonu/kapı-kaynağını TEKRAR TEKRAR okumasın (kullanıcı kararı 2026-11-16).

Sorun (ölçüldü): her downstream aşama (anlatım, örnek soru, önem/çözücü) ~82k token okuyor — 33k şablon dosyası +
30k kural özeti + 13k standart belge. Şablon (örn. k2-58 örnek sorular, 54 soru) yalnız "biçim öğrensin" diye okunuyor.

Çözüm: paket (atomlar + bilgi paketleri) zaten slaytların DOĞRULANMIŞ, DAMITILMIŞ hâli. Bir kez
  <klasör>/baglam/kaynak.md  — kompakt tek-kaynak: slayt dizini + bilgi paketleri + atomlar + çıkmış + üslup + kısaltma
  <klasör>/baglam/sema.md    — çıktı şemaları + mikro örnek + kapı komutu (33k şablon + kapı-kaynağı yerine ~2k)
üretilir; aşama istemleri YALNIZ bunu + ilgili kural özetini okur (ham slayt/şablon/standart belge DEĞİL). Kesin
sözcük gerektiğinde (atom/çıkmış kanıtı) ilgili TEK slayt sayfalar.json'dan açılır — hepsi değil.

  python3 scripts/hat/tam_hat/baglam.py <ders klasörü> --ders <key> [--mod tasarruf]
"""
from __future__ import annotations
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import argparse
import json
import re
import sys
from pathlib import Path

KOK = _kok.MEDS
DEPO = KOK.parent / "meds_database_v2" / "ders_bilgi"


def _ilk_satir(metin: str, n: int = 110) -> str:
    for s in (metin or "").splitlines():
        s = re.sub(r"[•▪●■◦✓•▪●o]\s*", "", s).strip()
        if len(s) >= 4:
            return s[:n]
    return "(boş)"


# Dilimler (2026-11-16, ölçüm k2-28: kaynak.md 8,5k kelime ve önem + çıkmış analizi + örnek soru aşamalarında üç kez BÜTÜN
# okunuyordu). Her aşama yalnız kendi dilimini okur (DILIM_ASAMA); kaynak.md geriye uyum için dilimlerin birleşimidir.
#   atom   = slayt dizini + bilgi paketleri + atomlar (temel gerçekler)
#   hoca   = hoca vurguları + öğrenci önem notları (önem/rozet dayanağı)
#   cikmis = doğrulanmış çıkmışlar
#   uslup  = soru üslubu kalıp payları
DILIMLER = ("atom", "hoca", "cikmis", "uslup")
DILIM_ASAMA = {
    "onem_listesi": ("atom", "hoca", "cikmis"),
    "cikmis_analiz": ("cikmis", "atom"),
    "ornek_soru": ("atom", "cikmis", "uslup"),
}


SENTEZ = KOK.parent / "meds_temp" / "ogrenci_sentez" / "ders"
_SINAV_TETIK = re.compile(r"(?i)hoca|tuza|sor[ua]|sordu|[cç][ıi]km|tus|s[ıi]nav")


def _sentez_dilimi(ders: str) -> tuple[list[str], list[str]]:
    p = SENTEZ / f"{ders}.json"
    if not p.exists():
        return [], []
    v = json.loads(p.read_text(encoding="utf-8"))
    L = ["\n## Öğrenci sentez notu — hocanın SÖZLÜ vurguları (öğrenci+YZ derlemesi; betikle ayıklandı, kayıpsız)",
         "> KULLANIM: yalnız 2026-27 slaytında karşılığı olan bilgi anlatıma/önem listesine girer (slaytla eşle, s = sentez",
         "> sayfası, slayt DEĞİL). İçindeki \"çıkmış/fakülte sorusu\" iddiası doğrulanmış çıkmış DEĞİL → çıkmış damgası/rozeti YASAK;",
         "> hoca adı/\"amfide söyledi\" iddiası sesle doğrulanmadan \"hoca vurguladı\" denmez (H-dolgu kuralı). Slaytla çelişen bilgi atılır."]
    LS = []
    for k in v.get("kaynaklar", []):
        for b in k.get("birimler", []):
            if b.get("baslik"):
                continue
            metin = re.sub(r"\s+", " ", b.get("metin", "")).strip()
            sat = f"ös{b.get('sayfa')} «{str(b.get('yol',''))[:60]}» [{','.join(b.get('tetik', []))[:40]}]: {metin}"
            L.append(sat)
            if _SINAV_TETIK.search(" ".join(b.get("tetik", []))):
                LS.append(sat)
    if LS:
        LS.insert(0, "\n## Öğrenci sentez notu — sınav/hoca vurgulu birimler (çıkmış damgası DEĞİL; slaytla eşle)")
    return L, LS


def kaynak_md(ders: str, klasor: Path) -> str:
    d = kaynak_dilimleri(ders, klasor)
    return d["_bas"] + "".join(d[k] for k in DILIMLER)


def kaynak_dilimleri(ders: str, klasor: Path, yalniz_s: set[int] | None = None) -> dict[str, str]:
    """yalniz_s verilirse atom dilimi (slayt dizini + bilgi paketi + atom) yalnız o slaytlarla sınırlanır."""
    def _al(x) -> bool:
        try:
            return yalniz_s is None or int(x) in yalniz_s
        except (TypeError, ValueError):
            return yalniz_s is None
    sayf = json.loads((klasor / "sayfalar.json").read_text(encoding="utf-8"))
    pk = json.loads((DEPO / ders / "degerlendirme" / "paket.json").read_text(encoding="utf-8"))
    L = [f"# {pk.get('konu', ders)} — read-once ders bağlamı",
         f"> Branş {pk.get('brans','')} · Hoca {pk.get('ogretim_uyesi','')} · {pk.get('kaynaklar',{}).get('sayfa','?')} slayt. "
         f"Aşamalar BUNU okur; ham slayt/şablon/standart belgeyi değil. Kesin sözcük gerekince ilgili TEK slaytı "
         f"`sayfalar.json`/`op/`'tan aç.", ""]
    out: dict[str, str] = {"_bas": "\n".join(L) + "\n"}
    L = []
    L.append("## Slayt dizini (her slaytın özü)")
    for k in sorted(sayf, key=lambda x: int(x)):
        if not _al(k):
            continue
        L.append(f"s{k}: {_ilk_satir(sayf[k])}")
    L.append("\n## Bilgi paketleri (slayt → başlık · maddeler)")
    for b in pk.get("bilgi_paketleri", []):
        if not _al(b.get("s")):
            continue
        md = " · ".join(m.strip()[:140] for m in (b.get("maddeler") or [])[:4])
        L.append(f"[{b.get('id')}] s{b.get('s')} «{b.get('baslik','').strip()[:80]}» — {md}")
    L.append("\n## Atomlar (damıtılmış gerçekler — anlatım/soru bunlardan kurulur; kapak/başlık atomu varsa KULLANMA)")
    for a in pk.get("atomik_bilgi_envanteri", {}).get("atomlar", []):
        if not _al(a.get("s")):
            continue
        ck = f" [çıkmış {','.join(a['cikmis'])}]" if a.get("cikmis") else ""
        L.append(f"{a.get('id')} [{a.get('kategori')}] s{a.get('s')}{ck}: {a.get('ifade','').strip()[:200]}")
    out["atom"] = "\n".join(L) + "\n"
    L = []
    LS: list[str] = []  # hoca_sinav: yalnız sınav vurgusu (tur=sinav) — önem listesinin dayanağı; anlatım alıntıları hariç
    # Hoca vurguları (kural 21 katmanı — baglam'ın ÖNCEDEN düşürdüğü, 2026-11-16 düzeltmesi). Anlatıma girer; çıkmış damgası DEĞİL.
    hv = pk.get("hoca_vurgulari") or []
    if hv:
        L.append("\n## Hoca vurguları (zaman damgalı alıntı — anlatımda dayanak; çıkmış damgası değil)")
        for v in hv:
            metin = str(v.get("alinti") or v.get("ifade") or "").strip().replace("\n", " ")
            L.append(f"s{v.get('s')} t{v.get('t')} [{v.get('tur','')}/{v.get('kategori','')}]: {metin[:220]}")
            if str(v.get("tur", "")) == "sinav":
                LS.append(L[-1])
        if LS:
            LS.insert(0, "\n## Hoca SINAV vurguları (yalnız tur=sinav; anlatım alıntıları için `baglam/kaynak_hoca.md`)")
    # Öğrenci önem notları (geçen yıl; kural 28). A = çıkmış kanıtlı, B = vurgu/el notu.
    on = pk.get("ogrenci_notlari") or []
    if on:
        L.append("\n## Öğrenci önem notları (geçen yıl — A çıkmış-kanıtlı, B vurgu/el notu; rozet dayanağı)")
        for n in on:
            oc = n.get("oncelik") or n.get("birim") or ""
            metin = str(n.get("hedef") or n.get("not") or n.get("ifade") or "").strip().replace("\n", " ")
            L.append(f"s{n.get('s')} [{oc}]: {metin[:180]}")
        LS += L[-len(on) - 1:]
    # Öğrenci SENTEZ notu (2026-11-17): hocanın SÖZLÜ vurgularını YZ ile derleyen arkadaş Drive'ı → betikle ayıklanmış
    # birimler (scripts/uretim/ogrenci_sentez/sentez.py; LLM yok). Sayfa no'su sentez PDF'inindir, slayt değil.
    L2, LS2 = _sentez_dilimi(ders)
    L += L2
    LS += LS2
    out["hoca"] ="\n".join(L) + ("\n" if L else "")
    out["hoca_sinav"] = "\n".join(LS) + ("\n" if LS else "")
    L = []
    # Doğrulanmış çıkmışlar
    ckp = pk.get("cikmis", {}).get("kaynak")
    if ckp and (KOK / ckp).exists():
        q = json.loads((KOK / ckp).read_text(encoding="utf-8")).get("q", [])
        L.append("\n## Doğrulanmış çıkmışlar (vurgu YALNIZ seviye=dogrudan)")
        for x in q:
            L.append(f"{x.get('id')} s{x.get('s')} [{x.get('seviye')}]: {str(x.get('kok','')).strip()[:150]} → {x.get('cevap','')}")
    out["cikmis"] = "\n".join(L) + ("\n" if L else "")
    L = []
    # Soru üslubu
    su = klasor / "soru_uslubu.json"
    if su.exists():
        u = json.loads(su.read_text(encoding="utf-8"))
        kp = u.get("kalip_payi") or {}
        L.append("\n## Soru üslubu (örnek soru kalıp payları — hedef ±%20)")
        L.append(" · ".join(f"{k} %{round(v*100)}" for k, v in kp.items()) + f" · kök ort. {u.get('kok_kelime_ort','?')} kelime")
    # Hoca üslubu profili (kural 26; LLM yok, <1 sn). Eskiden koordinatör ayrı komutla alıp isteme elle koyuyordu — unutulunca
    # profil kapısı örnek soruları reddediyordu. Artık üslup diliminin parçası (≤40 satır).
    pr = _profil(str(pk.get("brans", "")), str(pk.get("konu", "")))
    if pr:
        L.append("\n## Hoca üslubu profili (bağlayıcı hedefler — kapı profil_kapisi.py; `kanit: profil` yalnız yazılı gerekçeyle)")
        L.append(pr)
    out["uslup"] = "\n".join(L) + ("\n" if L else "")
    return out


def _profil(brans: str, konu: str, satir: int = 40) -> str:
    import subprocess
    betik = KOK / "scripts/uretim/hoca_profili/profil_oku.py"
    if not (brans and betik.exists()):
        return ""
    try:
        r = subprocess.run([sys.executable, str(betik), "--ders", brans, "--konu", konu], cwd=KOK, capture_output=True,
                           text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if r.returncode != 0 or not r.stdout.strip():
        return ""
    return "\n".join(x[:300] for x in r.stdout.strip().splitlines()[:satir])


SEMA = """# Aşama çıktı şemaları (read-once; 33k şablon + kapı-kaynağı yerine bu)

## anlatım · konusma_v2.json  (meds_temp/ogrenci_ders/<key>/anlatim/v2/konusma_v2.json)
{surum:2, ders_id, baslik, anahtar:<key>, bolumler:[{id:"<key>-bNN", baslik,
  paragraflar:[{id:"<key>-pNNN", sayfa:int,
    cumleler:[{ses:<okunan doğal cümle>, ekran:<kısa not>, duzey:0-1,
      vurgu:[{metin,tur:"terim|cikmis"}], slayt_adim:null, cikmis:[<dogrudan çıkmış id>],
      spot:null, ogrenci:null, hoca:null, slayt:{sayfa,satir:[<slayttan birebir>]}, id:"<key>-cNNNN"}]}]}]}
Kural: 1→N sırayla, katı kronoloji, dolgu yok, "çıkmışta soruldu" YALNIZ seviye=dogrudan cümlede. ≥1150 kelime.
Kapı: konusma_v2.py --turet DIZIN · --dogrula DIZIN · metin_denetle.py konusma_metni.md · turkce_uslup.denetle → hepsi 0 HATA.

## örnek sorular · src/data/ornek_sorular/k2/<key>.json
{id:<key>, sira, kurul:2, ders, konu, ogretim_uyesi, tarih,
 kazanimlar:[{no, metin, sorular:[{kazanim, zorluk:"kolay|orta|zor", soru,
   secenekler:["A şık",...5 şık], dogru:"A", aciklama,
   sik_aciklamalari:{A:<ne/ne işe yarar/neden, 2-3 cümle>, ...E}}]}]}
Kural: 50<n≤100, hoca üslubu (üslup paylarına ±%20), yalnız o slayta kadarki bilgi, "hepsi/hiçbiri" yok,
doğru şık en uzun değil, şık açıklamada geçiştirme ("cevabı değil") yok.
Kapı (TEK, 2026-11-17): ornek_soru_kapi.py <dosya> --ders <ders> --sayfalar sayfalar.json [--uslup soru_uslubu.json] → 0 HATA. Genel + hoca üslubu soruları AYNI dosyada (hoca üslubundakine uslup:"hoca"); hepsi sesli çözücüye girer; hoca üslubu yeniden belirlenmez, aşağıdaki hazır profil kullanılır.

## önem + çözücü (spot_cozucu çalışma dosyaları; <meds_temp>/spot_cozucu/<brans>/)
girdi/<kod>.json {kod,no,ad,sayfa,brans,cikmis_tekil:[id],ornek_hedef}
cikmis/<kod>.json [{id,sinav,kok,secenekler,dogru,(tekrar)}]
onem/<kod>.json {baslik,ozet,neden_onemli,maddeler:[{puan,bilgi,alt,detay,cikmis:[id],ornek:[{kok,secenekler,dogru,aciklama,zorluk}]}]}
cozucu/<kod>.json {sorular:[{ref,tur:"ornek|cikmis",soru,secenekler,dogru,sayfa:[n],(zorluk),(sinav),
  ipucu:{metin,ses}, siklar:{A:{metin,ses}..E}, cozum:{metin,ses}}]}  (ses = okunuş: %→yazı, kısaltma harf-harf)
Kapı: onem_dogrula.py onem/<kod>.json · cozucu_dogrula.py cozucu/<kod>.json → 0 HATA. birlestir/ses AYRI adım.

## çıkmış analizi · meds_database_v2/ders_bilgi/<key>/degerlendirme/cikmis_analiz.json  (baglam/iskelet_cikmis_analiz.json doldurulur)
{sorular:{<çıkmış id>:{aciklama:[<≥3 tam cümle: soru neyi ölçüyor · doğru cevap neden doğru (slayttaki bilgiyle) · güçlü çeldirici neden yanlış>],
  ornek:<aynı bilgiyi başka biçimde soran tek cümlelik örnek ya da somut vaka>, tuzak:<öğrencinin en sık düştüğü karışıklık, tek cümle>}}}
Kural: soru + cevabı yinelemekten ibaret analiz YASAK; kaynak (slayt/atom) dışı bilgi YASAK; iskeletteki `_s/_kok/_cevap` bağlamdır, silinmez.
Sesli okunur: biçim işareti (** # ` [!) yok, kısaltma ilk geçişte açık. Kapı: iskelet.py denetle · ders_analizi/uret.py --dogrula <key> → 0 HATA.

Not: paketin atom/bilgi_paketleri/çıkmışı TEK kaynak (baglam/kaynak.md). Kesin kanıt sözcüğü için ilgili slaytı aç.
"""


# ── Tek dosyalık iş girdisi (2026-11-17). Ölçüm: alt ajan tokenini girdi boyutundan çok ARAÇ ÇAĞRISI sayısı belirliyor
# (aynı ders 12 çağrıda 132k, 36 çağrıda 181k); aşama başına 6–9 ayrı dosya (kural listesi 5–7 + şema + 2–3 dilim) okunuyordu.
# `baglam/is_<katman>.md` = kural paketi (dersten bağımsız, sabit — başta: önbellek dostu) + o aşamanın şema bölümü +
# kaynak dilimleri (ortak başlık bir kez). Aşama bunu TEK okumayla alır; ayrıca yalnız doldurulacak iskelet JSON'u okunur.
#   katman → (kural paketi aşaması | None, şema bölüm başlığı önekleri, dilimler)
IS: dict[str, tuple[str | None, tuple[str, ...], tuple[str, ...]]] = {
    "anlatim": ("anlatim", ("anlatım",), ("hoca",)),
    "onem_listesi": ("ornek_soru", ("önem",), ("atom", "hoca_sinav", "cikmis")),
    "ornek_soru": ("ornek_soru", ("örnek sorular", "önem"), ("atom", "cikmis", "uslup")),
    "cikmis_analiz": (None, ("çıkmış analizi",), ("cikmis", "atom_dar")),
    # çözücü: veri = önem listesinin kendisi (onem/<kod>.json; ayrıca okunur) → dilim yok, yalnız talimat + şık/üslup kuralı
    "cozucu": (None, ("önem",), ()),
}
# Aşamanın kendi yazar talimatı (2026-11-17, k2-39 koşusunda görüldü: önem listesi ve çözücünün asıl kuralı
# spot_cozucu/TALIMAT_*.md'dir; kural paketinde yoktu, eski brif zinciri elle okutuyordu). (belge, bölüm önekleri; boş = bütün)
IS_EK: dict[str, tuple[tuple[str, tuple[str, ...]], ...]] = {
    "onem_listesi": (("scripts/uretim/spot_cozucu/TALIMAT_ONEM.md", ()),),
    "cozucu": (("scripts/uretim/spot_cozucu/TALIMAT_COZUCU.md", ()),
               ("docs/SIK_ACIKLAMA_STANDARDI.md", ("Kural:", "Biçim", "Kaynak sırası")),
               ("docs/TURKCE_USLUP_STANDARDI.md", ())),
}
# Kendi katmanı olmayan iş dosyası → bağlı olduğu katman (mod.py'de çözücü, örnek soru katmanının parçasıdır)
IS_KATMAN = {"cozucu": "ornek_soru"}

# Başka aşamaların kural paketleri (veri dilimi yok; yalnız kural): katman → paket aşaması
KURAL_KATMAN = {"degerlendirme": "kaynak", "ders_icerik": "ders_icerik", "ema_ses": "ses", "capa_cizim": "capa_cizim",
                "pdf_tasarim": "pdf_tasarim", "ogren_deste": "ogren_deste", "denetci": "denetci", "yayin": "yayin"}


def sema_bolum(onekler: tuple[str, ...]) -> str:
    out, al = [], False
    for satir in SEMA.splitlines():
        if satir.startswith("## "):
            al = any(satir[3:].startswith(o) for o in onekler)
        if al:
            out.append(satir)
    return "\n".join(out).strip()


def cikmis_slaytlari(ders: str) -> set[int]:
    """Doğrulanmış çıkmışların slaytları ±1 (kaynak_kapisi toleransıyla aynı) — çıkmış analizinin dar atom dilimi."""
    pk = json.loads((DEPO / ders / "degerlendirme" / "paket.json").read_text(encoding="utf-8"))
    ckp = pk.get("cikmis", {}).get("kaynak")
    out: set[int] = set()
    if ckp and (KOK / ckp).exists():
        for x in json.loads((KOK / ckp).read_text(encoding="utf-8")).get("q", []):
            try:
                n = int(x.get("s"))
            except (TypeError, ValueError):
                continue
            out |= {n - 1, n, n + 1}
    return out


def kural_paketleri(klasor: Path, mod: str) -> dict[str, int]:
    """Kipte YAPILACAK katmanların kural paketleri → baglam/kural_<aşama>.md (paket.json gerekmez; E0 sonunda da çağrılır)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import kural_secici as KS
    import mod as MOD
    yap = MOD.yapilacak(mod)
    asama = {a for k, a in KURAL_KATMAN.items() if yap.get(k, False)} | \
            {v[0] for k, v in IS.items() if yap.get(k, False) and v[0]}
    return KS.paket_yaz(klasor, mod, tuple(a for a in KS.PAKET_ASAMALAR if a in asama))


def is_dosyalari(klasor: Path, ders: str, mod: str, dl: dict[str, str]) -> dict[str, int]:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import kural_secici as KS
    import mod as MOD
    yap = MOD.yapilacak(mod)
    bg = klasor / "baglam"
    out: dict[str, int] = {}
    dar = None
    for kat, (ks, sema, dilim) in IS.items():
        if not yap.get(IS_KATMAN.get(kat, kat), False):
            continue
        p = [KS.paket(ks, mod)] if ks else []
        for yol, onek in IS_EK.get(kat, ()):
            if (KOK / yol).exists():
                p += [f"\n# YAZAR TALİMATI: {yol}" + (" (yalnız ilgili bölümler)" if onek else ""), KS.bolum_sec(yol, onek)[0]]
        p += ["\n# ÇIKTI ŞEMASI ve KAPI", sema_bolum(sema)]
        if dilim:
            p += ["\n# DERS VERİSİ", dl["_bas"]]
        for d in dilim:
            if d == "atom_dar":
                if dar is None:
                    dar = kaynak_dilimleri(ders, klasor, cikmis_slaytlari(ders))["atom"]
                p.append("> Atom dilimi yalnız çıkmışın geçtiği slaytlar ±1; başka slayt gerekirse `baglam/kaynak_atom.md`.\n" + dar)
            else:
                p.append(dl[d])
        t = "\n".join(p)
        (bg / f"is_{kat}.md").write_text(t, encoding="utf-8")
        out[kat] = len(t.split())
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("klasor", type=Path)
    ap.add_argument("--ders", required=True)
    ap.add_argument("--mod", choices=("tam", "tasarruf"), default="tam")
    ap.add_argument("--kural-yalniz", action="store_true",
                    help="yalnız baglam/kural_<aşama>.md (paket.json gerekmez; E0 sonunda değerlendirme aşaması için)")
    a = ap.parse_args()
    bg = a.klasor / "baglam"
    bg.mkdir(parents=True, exist_ok=True)
    kp = kural_paketleri(a.klasor, a.mod)
    print("kural paketleri: " + " · ".join(f"kural_{k}.md {n}" for k, n in kp.items()))
    if a.kural_yalniz:
        return 0
    if not (DEPO / a.ders / "degerlendirme" / "paket.json").exists():
        print(f"HATA: {a.ders} değerlendirme paketi yok — önce E1 (paket) üretilmeli", file=sys.stderr)
        return 2
    dl = kaynak_dilimleri(a.ders, a.klasor)
    for k in DILIMLER:  # dilim başı: ortak üst bilgi (konu/branş/hoca) her dilimde kısa tutulur
        (bg / f"kaynak_{k}.md").write_text(dl["_bas"] + dl[k], encoding="utf-8")
    (bg / "kaynak.md").write_text(dl["_bas"] + "".join(dl[k] for k in DILIMLER), encoding="utf-8")
    (bg / "sema.md").write_text(SEMA, encoding="utf-8")
    import os
    k = os.path.getsize(bg / "kaynak.md") // 4 + os.path.getsize(bg / "sema.md") // 4
    print(f"baglam yazıldı: {bg} (~{k} token; aşamalar ham slayt/şablon yerine bunu okur)")
    for k2 in DILIMLER:
        print(f"  kaynak_{k2}.md {len((bg / f'kaynak_{k2}.md').read_text(encoding='utf-8').split())} kelime")
    for kat, n in is_dosyalari(a.klasor, a.ders, a.mod, dl).items():
        print(f"  is_{kat}.md {n} kelime  (aşamanın TEK okuma dosyası: kural + şema + veri)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
