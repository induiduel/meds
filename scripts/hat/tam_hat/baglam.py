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


def kaynak_md(ders: str, klasor: Path) -> str:
    d = kaynak_dilimleri(ders, klasor)
    return d["_bas"] + "".join(d[k] for k in DILIMLER)


def kaynak_dilimleri(ders: str, klasor: Path) -> dict[str, str]:
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
        L.append(f"s{k}: {_ilk_satir(sayf[k])}")
    L.append("\n## Bilgi paketleri (slayt → başlık · maddeler)")
    for b in pk.get("bilgi_paketleri", []):
        md = " · ".join(m.strip()[:140] for m in (b.get("maddeler") or [])[:4])
        L.append(f"[{b.get('id')}] s{b.get('s')} «{b.get('baslik','').strip()[:80]}» — {md}")
    L.append("\n## Atomlar (damıtılmış gerçekler — anlatım/soru bunlardan kurulur; kapak/başlık atomu varsa KULLANMA)")
    for a in pk.get("atomik_bilgi_envanteri", {}).get("atomlar", []):
        ck = f" [çıkmış {','.join(a['cikmis'])}]" if a.get("cikmis") else ""
        L.append(f"{a.get('id')} [{a.get('kategori')}] s{a.get('s')}{ck}: {a.get('ifade','').strip()[:200]}")
    out["atom"] = "\n".join(L) + "\n"
    L = []
    # Hoca vurguları (kural 21 katmanı — baglam'ın ÖNCEDEN düşürdüğü, 2026-11-16 düzeltmesi). Anlatıma girer; çıkmış damgası DEĞİL.
    hv = pk.get("hoca_vurgulari") or []
    if hv:
        L.append("\n## Hoca vurguları (zaman damgalı alıntı — anlatımda dayanak; çıkmış damgası değil)")
        for v in hv:
            metin = str(v.get("alinti") or v.get("ifade") or "").strip().replace("\n", " ")
            L.append(f"s{v.get('s')} t{v.get('t')} [{v.get('tur','')}/{v.get('kategori','')}]: {metin[:220]}")
    # Öğrenci önem notları (geçen yıl; kural 28). A = çıkmış kanıtlı, B = vurgu/el notu.
    on = pk.get("ogrenci_notlari") or []
    if on:
        L.append("\n## Öğrenci önem notları (geçen yıl — A çıkmış-kanıtlı, B vurgu/el notu; rozet dayanağı)")
        for n in on:
            oc = n.get("oncelik") or n.get("birim") or ""
            metin = str(n.get("hedef") or n.get("not") or n.get("ifade") or "").strip().replace("\n", " ")
            L.append(f"s{n.get('s')} [{oc}]: {metin[:180]}")
    out["hoca"] = "\n".join(L) + ("\n" if L else "")
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
    out["uslup"] = "\n".join(L) + ("\n" if L else "")
    return out


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
Kapı: soru_uslup.py <dosya> --uslup soru_uslubu.json · sik_aciklama.denetle · profil_kapisi.py <dosya> --ders <ders> · kaynak_kapisi.py <dosya> sayfalar.json → 0 HATA.

## önem + çözücü (spot_cozucu çalışma dosyaları; <meds_temp>/spot_cozucu/<brans>/)
girdi/<kod>.json {kod,no,ad,sayfa,brans,cikmis_tekil:[id],ornek_hedef}
cikmis/<kod>.json [{id,sinav,kok,secenekler,dogru,(tekrar)}]
onem/<kod>.json {baslik,ozet,neden_onemli,maddeler:[{puan,bilgi,alt,detay,cikmis:[id],ornek:[{kok,secenekler,dogru,aciklama,zorluk}]}]}
cozucu/<kod>.json {sorular:[{ref,tur:"ornek|cikmis",soru,secenekler,dogru,sayfa:[n],(zorluk),(sinav),
  ipucu:{metin,ses}, siklar:{A:{metin,ses}..E}, cozum:{metin,ses}}]}  (ses = okunuş: %→yazı, kısaltma harf-harf)
Kapı: onem_dogrula.py onem/<kod>.json · cozucu_dogrula.py cozucu/<kod>.json → 0 HATA. birlestir/ses AYRI adım.

Not: paketin atom/bilgi_paketleri/çıkmışı TEK kaynak (baglam/kaynak.md). Kesin kanıt sözcüğü için ilgili slaytı aç.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("klasor", type=Path)
    ap.add_argument("--ders", required=True)
    ap.add_argument("--mod", choices=("tam", "tasarruf"), default="tam")
    a = ap.parse_args()
    bg = a.klasor / "baglam"
    bg.mkdir(parents=True, exist_ok=True)
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
