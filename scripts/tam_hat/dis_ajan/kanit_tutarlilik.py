#!/usr/bin/env python3
"""Kanıt tutarlılık kapısı (dış ajan protokolü §12-2). LLM yok.

  python3 scripts/tam_hat/dis_ajan/kanit_tutarlilik.py <uretim_bolum.json> <kanit_bolum.json>

Girdi `uretim`: liste; kayıt {"id":"u1","metin":"yazılan cümle","kanit":["k1","k2"],"olumsuz_gerekce":"(gerekirse)"}
Denetler (her biri yazılan cümle ile bağlı kanıtların alıntıları arasında):
  * kanıt var ve bağlı kanıtlar geçerli id'lerdir;
  * cümledeki her sayı kanıtta vardır (uydurma sayı yok);
  * cümlede olumsuzluk varsa kanıtta da vardır; kanıtta olumsuzluk varsa cümlede de olmalıdır
    (kasıtlı değişiklik için `olumsuz_gerekce` yaz);
  * yön (artar/azalır, yüksek/düşük) kanıtın tersine çevrilmemiştir;
  * cümle kanıtla konu bakımından örtüşür (5 harf kök örtüşmesi ≥ %30);
  * yasak desen: Türkçe üslup, dolgu, kaçamak meta cümle (turkce_uslup.py + metin_denetle.py kalıpları);
  * her kanıt en az bir cümlede kullanılmıştır (UYARI: kanıtlanmış ama anlatılmamış bilgi).
Tanım cümlesi (müfredat sözlüğüne bağlı, 2026-10-29): kayıt `"tur":"tanim","terim":"homeotik","sozluk":"<sozluk_ara.py anahtarı>"`.
  Koşullar: sözlükte var; terim bağlı kanıt alıntısında geçer ve cümlede geçer; cümle sözlük tanımından türer (kök örtüşmesi ≥ %50);
  ≤ 35 kelime; rakam yok; «örneğin/mesela/diyelim/hayal et…» örnek kalıbı yok; yeni kısaltma/gen adı yok; bölümde en çok %20.
--iddia: anlatım olmayan içerik (soru/deste/çözücü) iddia dosyaları için; paragraf (`p`) ve tekrar denetimi yapılmaz.
Çıkış 0 = HATA yok.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak import ASAGI, OLUMSUZ, YUKARI, katla, kokler, sayilar, yukle  # noqa: E402
from okunus_oner import oner  # noqa: E402

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK / "scripts"))
sys.path.insert(0, str(KOK / "scripts" / "sesli_anlatim"))
try:
    import turkce_uslup  # type: ignore
except Exception:  # noqa: BLE001
    turkce_uslup = None
try:
    import metin_denetle as _md  # type: ignore
except Exception:  # noqa: BLE001
    _md = None


def main() -> int:
    iddia = "--iddia" in sys.argv
    argv = [a for a in sys.argv if a != "--iddia"]
    if len(argv) != 3:
        print(__doc__)
        return 2
    uretim = yukle(Path(argv[1]))
    kanit = {k["id"]: k for k in yukle(Path(argv[2])) if isinstance(k, dict) and k.get("id")}
    try:
        from sozluk_ara import yukle_hepsi
        sozluk = yukle_hepsi()
    except Exception:  # noqa: BLE001
        sozluk = {}
    n_tanim = sum(1 for u in uretim if isinstance(u, dict) and u.get("tur") == "tanim")
    if uretim and n_tanim > max(1, len(uretim) // 5):
        print(f"HATA [TANIM-01] {n_tanim} tanım cümlesi, bölümde en çok %20 ({max(1, len(uretim)//5)}). Yapılacak: yalnız ilk geçişte gerçekten anlaşılmayan terimleri tanımla.")
    hata: list[str] = []
    uyari: list[str] = []
    kullanilan: set[str] = set()
    if not isinstance(uretim, list) or not uretim:
        print("HATA [URETIM-00] üretim dosyası boş ya da liste değil. Yapılacak: {id,metin,kanit} kayıtları listesi yaz.")
        return 1
    for i, u in enumerate(uretim):
        kim = u.get("id", f"#{i}") if isinstance(u, dict) else f"#{i}"
        if not isinstance(u, dict) or not str(u.get("metin", "")).strip():
            hata.append(f"[URETIM-01] {kim}: metin boş. Yapılacak: cümleyi yaz ya da kaydı sil.")
            continue
        ids = u.get("kanit") or []
        if not ids:
            hata.append(f"[URETIM-02] {kim}: kanıt yok. Yapılacak: bu cümleyi dayandıran kanıt id'lerini ekle; kanıtı olmayan cümleyi SİL.")
            continue
        yok = [x for x in ids if x not in kanit]
        if yok:
            hata.append(f"[URETIM-03] {kim}: kanıt id'leri kanıt dosyasında yok: {yok}. Yapılacak: doğru id'yi yaz ya da önce kanıt kaydını ekle.")
            continue
        kullanilan.update(ids)
        metin = str(u["metin"])
        kn = " ".join(str(kanit[x].get("alinti", "")) + " " + str(kanit[x].get("bilgi", "")) for x in ids)
        tanim_tanimi = ""
        if u.get("tur") == "tanim":
            terim, skey = str(u.get("terim", "")).strip(), str(u.get("sozluk", "")).strip()
            kayit = sozluk.get(skey) or next((v for k, v in sozluk.items() if katla(k) == katla(skey)), None)
            if not terim or not kayit:
                hata.append(f"[TANIM-02] {kim}: 'terim' ya da geçerli 'sozluk' anahtarı yok. Yapılacak: sozluk_ara.py ile terimi ara, çıkan anahtarı AYNEN yaz; bulunmuyorsa tanım yazma.")
                continue
            tanim_tanimi = str(kayit.get("definition", ""))
            if katla(terim) not in katla(" ".join(str(kanit[x].get("alinti", "")) for x in ids)):
                hata.append(f"[TANIM-03] {kim}: '{terim}' bağlı kanıt alıntısında geçmiyor. Yapılacak: yalnız kaynakta geçen terimi tanımla; kanıtı terimin geçtiği alıntıya bağla.")
            if katla(terim) not in katla(str(u["metin"])):
                hata.append(f"[TANIM-04] {kim}: cümlede '{terim}' yok. Yapılacak: tanım cümlesi terimi adıyla anmalı.")
            m_ = str(u["metin"])
            if len(m_.split()) > 35 or re.search(r"\d", m_):
                hata.append(f"[TANIM-05] {kim}: tanım ≤35 kelime olmalı ve rakam içermemeli. Yapılacak: kısalt, sayıyı çıkar.")
            if re.search(r"örneğin|mesela|diyelim|düşün(ün|elim)|hayal|farz|gibi bir hasta|bir hasta|düşünelim", katla(m_)) or re.search(r"\b(orne[gk]in|mesela|diyelim|hayal)\b", katla(m_)):
                hata.append(f"[TANIM-06] {kim}: tanım cümlesinde örnek/senaryo kalıbı var. Yapılacak: örnek verme; yalnız sözlük anlamını yaz.")
            okok = kokler(m_)
            if okok and len(okok & kokler(tanim_tanimi)) / len(okok) < 0.50:
                hata.append(f"[TANIM-07] {kim}: cümle sözlük tanımından türemiyor (kök örtüşmesi <%50). Yapılacak: sozluk_ara.py'nin verdiği tanıma bağlı kal, kendi yorumunu ekleme.")
            for tk in re.findall(r"\b[A-ZÇĞİÖŞÜ]{2,}[A-Za-z0-9]*\b", m_):
                if tk not in kn and tk not in tanim_tanimi:
                    hata.append(f"[TANIM-08] {kim}: '{tk}' kanıtta ve sözlük tanımında yok (yeni kısaltma/gen adı). Yapılacak: çıkar.")
            # tekrar: terimi adıyla anıp tanımlayan bir cümle zaten varsa («adı verilir», «denir»…) ikinci tanım gereksizdir (Sıfır Tekrar kuralı)
            for x in uretim:
                if not isinstance(x, dict) or x is u or x.get("tur") == "tanim":
                    continue
                xm = katla(str(x.get("metin", "")))
                if katla(str(u.get("terim", ""))) in xm and re.search(r"adi verilir|adlandirilir|denir\b|denilir|olarak taninir|olarak tanimlanir|anlamina gelir|demektir", xm):
                    hata.append(f"[TANIM-09] {kim}: «{u.get('terim')}» terimi {x.get('id')} cümlesinde zaten tanımlanıyor; ikinci tanım tekrar olur. Yapılacak: tanım cümlesini sil.")
                    break
            kn = kn + " " + tanim_tanimi
        mk, kk = katla(metin), katla(kn)
        fazla = sayilar(metin) - sayilar(kn)
        if fazla:
            hata.append(f"[URETIM-04] {kim}: cümledeki {sorted(fazla)} sayısı bağlı kanıtta yok. Yapılacak: sayıyı kanıttaki değerle düzelt ya da doğru kanıtı bağla.")
        m_neg, k_neg = bool(OLUMSUZ.search(mk)), bool(OLUMSUZ.search(kk))
        if m_neg and not k_neg:
            hata.append(f"[URETIM-05] {kim}: cümlede olumsuzluk var, kanıtta yok. Yapılacak: olumsuzlamayı kaldır ya da olumsuzluğu gösteren alıntıyı kanıta ekle.")
        if k_neg and not m_neg and not u.get("olumsuz_gerekce"):
            hata.append(f"[URETIM-06] {kim}: kanıtta olumsuzluk var, cümlede yok (anlam çevrilmiş olabilir). Yapılacak: olumsuzluğu cümleye taşı; kasıtlıysa 'olumsuz_gerekce' yaz.")
        mu, ma = bool(YUKARI.search(mk)), bool(ASAGI.search(mk))
        ku, ka = bool(YUKARI.search(kk)), bool(ASAGI.search(kk))
        if (mu and not ma and ka and not ku) or (ma and not mu and ku and not ka):
            hata.append(f"[URETIM-07] {kim}: cümle kanıtın TERS yönünü söylüyor (artış/azalış). Yapılacak: yönü kanıttaki gibi yaz.")
        # Tıbbi niteleyici şişirme: kapsam/kesinlik/yer/kalıtım sözcüğü kanıtta yoksa cümleye eklenemez (en sık sessiz tıbbi hata)
        NIT = re.compile(r"\b(her|tum|tumu|butun|hepsi|daima|hep|asla|yalniz\w*|sadece|kesin\w*|mutlaka|genellikle|cogunlukla|cogu|bazi|nadiren|sik\s?sik|"
                         r"otozomal\s+(?:dominant|resesif)|x.?e\s+bagli|proksimal\w*|distal\w*|anterior|posterior|ventral\w*|dorsal\w*|"
                         r"baslica|temel|tek\s+neden|ana\s+neden|ilk\s+basamak|erken|gec|akut|kronik|tum\s+vakalar)\b")
        fz = {m.group(0) for m in NIT.finditer(mk)} - {m.group(0) for m in NIT.finditer(kk)}
        fz = {x for x in fz if x not in kk}
        if fz and u.get("tur") != "tanim":
            hata.append(f"[NITELE-01] {kim}: cümlede {sorted(fz)} niteleyicisi var, bağlı kanıtta yok (kapsam/kesinlik/yer/kalıtım bilgisi uydurma olabilir). Yapılacak: niteleyiciyi çıkar ya da onu söyleyen alıntıyı kanıta ekleyip bağla.")
        NED = re.compile(r"(neden olur|neden olmakta|yol acar|yol acmakta|sonucunda|nedeniyle|nedeni|kaynaklan\w*|sebep\w*|bu yuzden|dolayisiyla|tetikler|baskilar|bozar|bozulur|yetersiz\w* nedeniyle)")
        NEDK = re.compile(r"(neden|yol ac|sonuc|kaynaklan|sebep|yuzunden|dolay|tetik|baskila|bozul|bozar|gelisir|olusur|ortaya cik|ile iliskili|iliskilidir|etkiler|ilgilidir|yerlesti|gozlen)")
        if NED.search(mk) and not NEDK.search(kk) and not u.get("cikarim") and u.get("tur") != "tanim":
            hata.append(f"[NEDEN-01] {kim}: cümle neden-sonuç bağı kuruyor ama bağlı kanıt böyle bir ilişki söylemiyor. Yapılacak: ilişkiyi söyleyen alıntıyı kanıta ekle; ilişki iki ayrı alıntıdan çıkıyorsa her ikisini bağla ve kayda \"cikarim\": true yaz (en az 2 kanıt gerekir); olmuyorsa ilişkiyi söyleme.")
        if u.get("cikarim") and len(u.get("kanit") or []) < 2:
            hata.append(f"[NEDEN-02] {kim}: «cikarim» cümlesi en az 2 ayrı kanıta dayanmalı (tek alıntıdan çıkarım yapılmaz).")
        ortak_k = kokler(metin) & kokler(kn)
        mk_set = kokler(metin)
        if mk_set and len(ortak_k) / len(mk_set) < 0.30:
            hata.append(f"[URETIM-08] {kim}: cümle bağlı kanıtla konu bakımından örtüşmüyor (%{100*len(ortak_k)//max(1,len(mk_set))}). Yapılacak: doğru kanıtı bağla ya da cümleyi kanıtın söylediğine indir.")
        # Kısaltma/gen sembolü: sitenin gerçek hattı (metin_denetle, --yazim YOK) büyük harfli kısaltmayı HATA sayar; okunuşla yazılır.
        # Okunuş UYDURULMAZ: okunus_oner.py çıktısı AYNEN yazılır ("hoks de on üç", "o te iks iki"). Benzer ama farklı yazım = uydurma.
        def iskelet(x: str) -> str:
            return re.sub(r"[aeıioöuü0-9]", "", katla(x).replace("x", "ks"))
        kn_kelime = set(re.findall(r"[a-z0-9]+", katla(kn)))
        mk_cumle = " " + " ".join(re.findall(r"[a-zçğıöşüa-z0-9]+", katla(metin))) + " "
        for tok in sorted(set() if iddia else {t for x in ids for t in {t.upper() if re.fullmatch(r"(?i)(hox|otx|pax|sox|msx|pitx|tbx|fgf|shh|wnt|bmp)\w*", t) else t for t in re.findall(r"\b(?:[A-ZÇĞİÖŞÜ]{2,}|(?i:hox|otx|pax|sox|msx|pitx|tbx|fgf|shh|wnt|bmp))[A-Za-z0-9]*\b", str(kanit[x].get("alinti", "")))}}):  # --iddia (soru/çözücü/deste) ekran metnidir: PDF yazımı korunur
            beklenen = oner(tok)
            if not beklenen:
                continue
            sk = iskelet(tok)
            if len(sk) < 3:
                continue
            if re.search(r"\b" + re.escape(tok) + r"\b", metin, re.I):  # Hox/hOX gibi karma yazım da (sese yanlış gider)
                hata.append(f"[URETIM-15] {kim}: '{tok}' büyük harfle yazılmış; sitenin ses denetimi bunu reddeder. Yapılacak: okunuşla yaz → «{beklenen}» (okunus_oner.py).")
                continue
            ilk = katla(beklenen).split(" ")[0]
            anmis = ilk in mk_cumle.split() or any(iskelet(w) and (iskelet(w) == sk or sk.startswith(iskelet(w))) and len(iskelet(w)) >= 3 and katla(w) not in kn_kelime for w in re.findall(r"[a-zçğıöşü]{3,}", metin.lower()))
            if anmis and (" " + katla(beklenen) + " ") not in mk_cumle:
                hata.append(f"[URETIM-15] {kim}: «{tok}» için okunuş uydurulmuş ya da eksik. Yapılacak: AYNEN «{beklenen}» yaz (python3 scripts/tam_hat/dis_ajan/okunus_oner.py {tok}).")
        if turkce_uslup:
            for h in turkce_uslup.denetle(metin, kim):
                hata.append(f"[URETIM-09] {h}. Yapılacak: doğal, düz Türkçeyle yeniden yaz.")
        if _md:
            for r in tuple(getattr(_md, "DOLGU", ())) + tuple(getattr(_md, "KACAMAK", ())):
                if re.search(r, metin, re.I):
                    hata.append(f"[URETIM-10] {kim}: dolgu/kaçamak kalıp ({r[:30]}…). Yapılacak: cümleyi sil ya da kaynaktan yeni bilgi taşıyan cümleyle değiştir.")
                    break
    # Paragraf başı bağlam: her kayıt "p" (paragraf no) taşır; paragrafın ilk cümlesi bağlamsız zamirle/bağlaçla başlayamaz
    gorulen_p: set = set()
    for u in uretim:
        if not isinstance(u, dict):
            continue
        p = u.get("p")
        if iddia:
            continue
        if p is None:
            hata.append(f"[URETIM-12] {u.get('id')}: 'p' (paragraf numarası) yok. Yapılacak: her cümleye paragraf no ver; sıra paragrafı kurar.")
            continue
        if p not in gorulen_p:
            gorulen_p.add(p)
            ilk = katla(str(u.get("metin", "")).strip()).split(" ")[0] if str(u.get("metin", "")).strip() else ""
            if ilk in ("bu", "bunlar", "bunlarin", "bunun", "bunlari", "su", "o", "onlar", "ayrica", "ancak", "ayni", "boylece", "bunlara") or ilk.startswith("bu"):
                hata.append(f"[URETIM-13] {u.get('id')}: paragraf '{ilk}' ile başlıyor; önceki cümle bu paragrafta yok, dinleyici neyi kastettiğini bilemez. Yapılacak: konuyu adıyla anarak başlat (örn. 'Homeodomain proteinleri…').")
    # Yapay tekrar: aynı paragrafta ardışık 3+ cümle aynı iki sözcükle başlıyor
    from itertools import groupby
    for p, grp in ([] if iddia else groupby([u for u in uretim if isinstance(u, dict)], key=lambda u: u.get("p"))):
        bas = [" ".join(katla(str(u.get("metin", ""))).split()[:2]) for u in grp]
        for k, g in groupby(bas):
            if len(list(g)) >= 3:
                uyari.append(f"[URETIM-14] paragraf {p}: ardışık 3+ cümle '{k}' ile başlıyor (robotik). Yapılacak: çeşitlendir ('bu genler', 'bunlar' paragraf içinde serbest) ya da cümleleri birleştir.")
    for kid in kanit:
        if kid not in kullanilan:
            uyari.append(f"[URETIM-11] {kid}: kanıtlanmış ama hiçbir cümlede kullanılmamış bilgi. Önemliyse anlatıma ekle, değilse kanıttan çıkar.")
    for u in uyari:
        print("UYARI", u)
    for h in hata:
        print("HATA", h)
    print(f"{'BAŞARISIZ' if hata else 'GEÇTİ'}: {len(uretim)} cümle, {len(hata)} hata, {len(uyari)} uyarı")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
