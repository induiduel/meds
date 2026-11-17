#!/usr/bin/env python3
"""Kurul 3 arşiv dersi metin üretici: sayfa metni → metin.tsv (ses/ekran/çapa) — betik + ücretsiz bulut LLM.

Kural 20/22: yalnız elle verilen komutla çalışır (MEDS_LLM_ELLE=1).

  env -u INVOCATION_ID MEDS_LLM_ELLE=1 python3 scripts/uretim/arsiv_25_26/k3_uret.py <key> [seçenekler]
    --parca-sayfa N   bir istekte üretilecek sayfa sayısı (varsayılan 5)
    --sayfa 2-8,11    yalnız bu sayfalar
    --zorla           önbelleği (uretim.json) yok say, yeniden üret

Tasarım (izlenebilirlik = PDF metin takibi kalitesi):
  Model sayfayı MADDE MADDE üretir: her madde = slayttaki bir satır (harfi harfine) + o satırı anlatan cümleler +
  o satırın ekran karşılığı. Böylece her cümle bir slayt satırına bağlanır (slayt.satir), PDF vurgusu cümle cümle
  doğru yere gider (H605 dersi: çapasız cümle sayfaya düşer).
  Betik sayfa metninde geçmeyen satırı ATAR (uydurma çapa yok); satırı olmayan madde bağlamsız cümle sayılır.

Kapılar: k3_metin.py (konusma_v2.dogrula + metin_denetle) + k3_yayinla.kapsam (sayfa/görsel kapsamı).
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

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

MEDS = _kok.MEDS
DB = MEDS.parent / "meds_database_25_26"

sys.path.insert(0, str(MEDS / "otomasyon"))
sys.path.insert(0, str(MEDS / "scripts"))
from llm_kilit import kilit as _kilit  # noqa: E402
sys.path.insert(0, str(MEDS / "scripts" / "altyapi" / "agents"))

SISTEM = (
    "Sen tıp fakültesi Dönem 3 öğrencisine sesli ders anlatan deneyimli bir klinik hocasısın. "
    "Yalnız verilen slayt metnindeki bilgiyi kullanırsın; slaytta olmayan sayı, ilaç, gen, sınıflama, eşik eklemezsin. "
    "Slaytı okumazsın, öğretirsin: her maddenin neden öyle olduğunu ve klinik sonucunu söylersin. "
    "Yanıtı SADECE istenen JSON biçiminde verirsin."
)

KURALLAR = """KURALLAR
1. Her slayt sayfası için bir nesne yaz; verilen sayfa numarasını aynen kullan. Sayfayı atlamak yasak.
2. "maddeler": sayfadaki bilgi satırlarının HER BİRİ için bir nesne (satır atlamak yasak; slaytta kaç bilgi satırı
   varsa o kadar). Her madde:
   - "satir": o bilgiyi taşıyan satırı slayttan HARFİ HARFİNE kopyala (kırılmış satırı birleştir, madde imini at).
     Slaytta yazı yoksa (yalnız görsel/şema) "satir": "" yaz ve "sekil" doldur.
   - "sekil": bu madde bir resim/şema/grafik/tablo anlatıyorsa kısa tarif ("ince barsak villus şeması"), yoksa null.
   - "cumleler": o maddeyi anlatan 1–3 ses cümlesi. İlk cümle maddenin kavramını ADIYLA söyler (asla "bu durum",
     "bu hastalık", "burada" diye başlamaz). Sonraki cümleler mekanizma/klinik sonuç ekler.
   - "ekran": o maddenin ekranda görünen kısa hâli (en çok 12 kelime, 1 satır, kilit kavram **kalın**).
3. Ses cümlesi kuralları (seslendirilecek):
   - Tek cümle, tam ve doğal Türkçe, hoca anlatımı; 8–28 kelime.
   - RAKAM ve SİMGE YASAK, yazıyla: "yüzde on sekiz", "iki bin yirmi iki", "üç buçuk", "eşit ya da büyük",
     "mililitre bölü dakika". Tarih, oran, doz hep yazıyla.
   - BÜYÜK HARFLİ KISALTMA YASAK, okunuşla: "de ne a", "a ce te ha", "pe pee ay", "ha pee vee", "ce re aktive protein",
     "helikobakter pilori", "immünoglobulin a", "vi pi pi". Kısaltmanın açılımı Türkçe ise açılımı yaz.
   - Markdown, madde imi, parantez, iki nokta üst üste, tırnak YASAK (kalın yalnız ekranda).
   - Slayttaki terimi aynı biçimde kullan; eş anlamlısına çevirme. Kısaltma yoksa da terimi koru.
   - Tekrar yasak: aynı kalıpla başlama, önceki sayfada söyleneni yineleme.
4. "sekil_ozet": sayfada resim/tablo varsa ve bu sayfada hiçbir madde onu anlatmıyorsa, görseli anlatan madde ekle
   (satir boş, sekil dolu). Yoksa null.
5. "cikmis": yalnız verilen çıkmış sorulardan bu sayfanın bilgisiyle yanıtlanabilen varsa kimliğini yaz. Varsa
   ilgili maddenin İLK cümlesinde "bu bilgi çıkmış sınavda sorulmuştur" gibi doğal bir uyarı geçsin.
6. Kapsam: sayfadaki her bilgi satırı anlatılır; şekil/tablo varsa ne gösterdiği ve kilit bulgusu söylenir.
7. TABLO sayfası: tabloyu hücre hücre okuma; satırları gurupla ("Cushing sendromu en sık küçük hücreli akciğer
   kanserinde görülür" gibi). Tablo İngilizce/OCR bozuksa doğru tıbbi Türkçe terimlerle yaz (çeviri serbest,
   yeni bilgi eklemek yasak). "satir" alanına tablodan kısa bir satır parçası yeterlidir.
"""

CIKTI = """ÇIKTI BİÇİMİ (yalnız JSON)
{"sayfalar":[{"sayfa":<no>,"maddeler":[{"satir":"slayttan birebir satır","sekil":null,
  "cumleler":["cümle"],"ekran":"**kavram** kısa madde"}],"cikmis":[]}]}"""


def sayfalar(taslak: Path) -> dict[int, str]:
    kaynak = (taslak / "kaynak.md").read_text(encoding="utf-8")
    out = {}
    par = re.split(r"^=== SAYFA (\d+) ===$", kaynak, flags=re.M)
    for i in range(1, len(par), 2):
        out[int(par[i])] = par[i + 1].strip()
    return out


def varlik(taslak: Path) -> dict[int, dict]:
    p = taslak / "sayfalar.json"
    return {int(x["sayfa"]): x for x in json.loads(p.read_text(encoding="utf-8"))} if p.exists() else {}


def ocr_metni(taslak: Path, n: int) -> str:
    """Görsel/şema sayfasında PDF metin katmanı yetersizse sayfa görüntüsünü Tesseract ile oku (önbellekli).

    Neden: şema/taranmış slaytlarda gömülü metin ya yok ya bozuk; model görsel anlatacak bilgi bulamayınca o sayfa
    'anlatılmamış' kalıyordu (kapsam kapısı). OCR yerel ve ücretsizdir; bulut görsel modeli bakiyesi yok (H612).
    """
    onbellek = taslak / "ocr" / f"{n}.txt"
    if onbellek.exists():
        return onbellek.read_text(encoding="utf-8")
    png = taslak / "sayfa_goruntu" / f"{n}.png"
    if not png.exists():
        return ""
    r = subprocess.run(["tesseract", str(png), "stdout", "-l", "tur+eng", "--psm", "3"],
                       capture_output=True, text=True)
    t = (r.stdout or "").strip()
    # OCR gürültüsü: tek karakterli satırlar, aşırı noktalama ve uzun rakam dizileri atılır
    satir = []
    for s in t.splitlines():
        s = re.sub(r"\s+", " ", s).strip()
        if len(s) < 3 or not re.search(r"[A-Za-zÇĞİÖŞÜçğıöşü]{3,}", s):
            continue
        satir.append(s)
    t = "\n".join(satir[:60])
    onbellek.parent.mkdir(parents=True, exist_ok=True)
    onbellek.write_text(t, encoding="utf-8")
    return t


def sayfa_metni(taslak: Path, n: int, smetin: dict[int, str], varl: dict[int, dict]) -> str:
    """Modelin göreceği sayfa metni: gömülü metin + (görsel sayfada) OCR katmanı."""
    t = smetin.get(n) or ""
    v = varl.get(n) or {}
    gorsel = (v.get("gorsel_orani") or 0) >= 0.18 or (v.get("cizim") or 0) >= 25 or bool(v.get("tablolar"))
    if not gorsel:
        return t
    if len(t.split()) >= 45:
        return t
    o = ocr_metni(taslak, n)
    if not o:
        return t
    ek = [s for s in o.splitlines() if s and s.lower() not in t.lower()]
    return (t + "\n" + "\n".join(ek)).strip() if ek else t


def katla(s: str) -> str:
    s = (s or "").replace("İ", "i").replace("I", "ı").lower()
    return " ".join(re.sub(r"[^0-9a-zçğıöşü ]+", " ", s).split())


def satir_gecer(st: str, kat_sayfa: str) -> bool:
    """Çapa satırı sayfada mı: birebir katlanmış eşleşme ya da kelimelerinin ≥%70'i sayfada (tablo/sütun kırılması)."""
    k = katla(st)
    if not k:
        return False
    if k in kat_sayfa:
        return True
    kel = [w for w in k.split() if len(w) > 2 or w.isdigit()]
    if len(kel) < 3:
        return False
    return sum(1 for w in kel if w in kat_sayfa) / len(kel) >= 0.7


SH_SISTEM = ("Sen tıp fakültesi Dönem 3 öğrencisine sesli ders anlatan deneyimli bir klinik hocasısın. "
             "Yalnız verilen slayt metnindeki bilgiyi kullanırsın. Yanıtı SADECE istenen JSON biçiminde verirsin.")

SH_KURALLAR = """KURALLAR
1. Sayfa bir şema/akış/tablo/resim sayfasıdır; OCR metni bozuk olabilir. Doğru tıbbi Türkçeyle anlat, slaytta
   olmayan sayı/ilaç/sınıflama EKLEME.
2. En çok 6 madde yaz; her madde bir kutu/dal/satır olsun.
3. "satir": boş ("") bırak. "sekil": o kutunun/dalın kısa tarifi (5–8 kelime).
4. "cumleler": 1 cümle, 8–28 kelime, hoca anlatımı, maddenin kavramını ADIYLA söyle.
   RAKAM ve BÜYÜK HARFLİ KISALTMA YASAK (yazıyla: "yüzde on", "de ne a"). Markdown/parantez/iki nokta YASAK.
5. "ekran": en çok 10 kelime, kilit kavram **kalın**.
6. "cikmis": verilen çıkmış sorulardan bu sayfayla yanıtlanabilen varsa kimliği, yoksa [].
"""

SH_CIKTI = """ÇIKTI BİÇİMİ (yalnız JSON)
{"sayfalar":[{"sayfa":<no>,"maddeler":[{"satir":"","sekil":"kısa tarif",
  "cumleler":["cümle"],"ekran":"**kavram** kısa madde"}],"cikmis":[]}]}"""


def istek_kisa(baglam: dict, smetin: dict[int, str], secili: list[int]) -> dict | None:
    """Görsel/şema sayfası yedeği: kısa istem, küçük çıktı sınırı (uzun istemde model boş dönüyordu, H612)."""
    import cloud_llm as C
    girdi = "\n\n".join(f"--- SAYFA {n} ---\n{(smetin.get(n) or '')[:1200]}" for n in secili)
    istem = (f"Ders: {baglam['konu']} ({baglam['brans']})\n\n{SH_KURALLAR}\n{SH_CIKTI}\n"
             f"GİRDİ · SLAYTLAR\n{girdi}\n")
    modeller = [m.strip() for m in (os.environ.get("MEDS_K3_MODELS") or "opendesign:deepseek-v4.1-flash").split(",") if m.strip()]
    for deneme in range(3):
        r = C.chat(istem, system=SH_SISTEM, as_json=True, max_tokens=3000, temperature=0.2, timeout=240,
                   json_ham=True, models=modeller)
        if r:
            break
        print(f"  [istek-kısa] boş yanıt ({deneme + 1}/3)", flush=True)
        time.sleep(3)
    if not isinstance(r, dict) or not isinstance(r.get("sayfalar"), list):
        return None
    out = {}
    for x in r["sayfalar"]:
        if isinstance(x, dict):
            try:
                out[int(x.get("sayfa"))] = x
            except (TypeError, ValueError):
                continue
    return out or None


def istek(baglam: dict, smetin: dict[int, str], varl: dict, adaylar: list[dict], secili: list[int],
          geri: dict[int, list[str]] | None = None) -> dict | None:
    import cloud_llm as C
    girdi = []
    for n in secili:
        v = varl.get(n) or {}
        etiket = []
        if (v.get("gorsel_orani") or 0) >= 0.18 or (v.get("cizim") or 0) >= 25:
            etiket.append("GÖRSEL/ŞEMA VAR")
        if v.get("tablolar"):
            etiket.append("TABLO VAR")
        girdi.append(f"--- SAYFA {n} {'· ' + ' · '.join(etiket) if etiket else ''} ---\n"
                     f"{smetin.get(n) or '(sayfada yazı yok — yalnız görsel: sekil_ozet ile anlat)'}")
    ca = "\n".join(f"- {q['id']} ({q.get('konu')}): {re.sub(chr(10), ' ', q.get('soru') or '')[:350]} → doğru: "
                   f"{(q.get('secenekler') or {}).get(q.get('cevap'), '')[:150]}" for q in adaylar) or "(yok)"
    geri_blok = ""
    if geri:
        sat = [f"- s{n}: " + "; ".join(h[:120] for h in hs[:4]) for n, hs in geri.items() if hs]
        if sat:
            geri_blok = ("\n\nÖNCEKİ DENEMENİN KUSURLARI (aynı ders, bu sayfalar — düzeltilerek yeniden üret):\n"
                         + "\n".join(sat) + "\n")
    istem = (f"GÖREV · Ders: {baglam['konu']} ({baglam['brans']})\n\n{KURALLAR}\n{CIKTI}\n{geri_blok}\n"
             f"GİRDİ · SLAYTLAR\n" + "\n\n".join(girdi) + f"\n\nBU SAYFALARA AİT ÇIKMIŞ SORULAR\n{ca}\n")
    modeller = [m.strip() for m in (os.environ.get("MEDS_K3_MODELS") or "opendesign:deepseek-v4.1-flash").split(",") if m.strip()]
    for deneme in range(3):
        r = C.chat(istem, system=SISTEM, as_json=True, max_tokens=9000, temperature=0.25, timeout=420,
                   json_ham=True, models=modeller)
        if r:
            break
        print(f"  [istek] boş yanıt ({deneme + 1}/3) — yineleniyor", flush=True)
        time.sleep(3)
    if not r:
        return None
    if isinstance(r, str):
        m = re.search(r"\{.*\}", r, re.S)
        try:
            r = json.loads(m.group(0)) if m else None
        except ValueError:
            r = None
    if not isinstance(r, dict) or not isinstance(r.get("sayfalar"), list):
        return None
    out = {}
    for x in r["sayfalar"]:
        if not isinstance(x, dict):
            continue
        try:
            out[int(x.get("sayfa"))] = x
        except (TypeError, ValueError):
            continue
    return out


SES_YASAK = re.compile(r"[*#|>\[\]{}_`~]|\d|\s-\s")
KISALTMA = re.compile(r"\b[A-ZÇĞİÖŞÜ]{2,}\b")
BAGLAMSIZ = re.compile(r"^(?:bu|şu|söz\s+konusu|ilgili|yukarıdaki|aynı)\s+(?:\w+\s+)?"
                       r"(?:hastalık|hasta|olgu|tümör|sendrom|tablo|durum|bozukluk|enfeksiyon|lezyon|ilaç|grup|tip|"
                       r"form|mekanizma|süreç|bulgu|kavram|durumlar|hastalıklar|hastalarda|bunlarda)", re.I)


def cumle_sayisi(metin: str) -> int:
    """konusma_v2._cumle_sayisi ile BİREBİR aynı kural (H109 kapısı burada da yakalanır → tur içinde düzeltilir)."""
    out = []
    for m in re.finditer(r"[.!?…]+[\"'”’)\]]*(?:\s+|$)", metin):
        e = m.end()
        if e < len(metin) and metin[e].islower():
            continue
        if e > (out[-1] if out else 0):
            out.append(e)
    if not out or out[-1] < len(metin):
        out.append(len(metin))
    return len(out)


def cumlelere_bol(metin: str) -> list[str]:
    """Tek cümle kuralını KODLA garanti et: cümle sınırından böl (metne dokunmaz, yalnız ayırır)."""
    if cumle_sayisi(metin) <= 1:
        return [metin]
    parcalar, bas = [], 0
    for m in re.finditer(r"[.!?…]+[\"'”’)\]]*(?:\s+|$)", metin):
        e = m.end()
        if e < len(metin) and metin[e].islower():
            continue
        if e <= bas:
            continue
        parcalar.append(metin[bas:e].strip())
        bas = e
    if bas < len(metin) and metin[bas:].strip():
        parcalar.append(metin[bas:].strip())
    return [p for p in parcalar if p] or [metin]



def uslup_dene(metin: str, yer: str) -> list[str]:
    """turkce_uslup kapısıyla aynı denetim (Kurul 2+ standardı) — tur içinde yakalanır, sonradan HATA olmaz."""
    try:
        from turkce_uslup import denetle as _u
    except ImportError:
        return []
    return _u(metin, yer)


def denetle_sayfa(x: dict, n: int, metin: str, varl: dict | None = None) -> list[str]:
    e, maddeler = [], x.get("maddeler") or []
    vv = (varl or {}).get(n) or {}
    varl_tablo = bool(vv.get("tablolar"))
    varl_gorsel = (vv.get("gorsel_orani") or 0) >= 0.18 or (vv.get("cizim") or 0) >= 25
    if not maddeler:
        e.append(f"s{n}: madde yok")
    kat = katla(metin)
    n_cumle = 0
    parca_i = 0          # paragraf içi cümle sayacı (k3_metin: her 5 cümlede yeni paragraf)
    for m in maddeler:
        if not isinstance(m, dict):
            e.append(f"s{n}: madde biçimi")
            continue
        cumleler = [c for c in (m.get("cumleler") or []) if isinstance(c, str) and c.strip()]
        if not cumleler:
            e.append(f"s{n}: madde cümlesiz ({str(m.get('satir'))[:40]})")
        st = (m.get("satir") or "").strip()
        if st and not satir_gecer(st, kat) and not (varl_tablo or varl_gorsel):
            e.append(f"s{n}: satır slaytta yok: {st[:50]}")
        if not st and not m.get("sekil") and not (varl_tablo or varl_gorsel):
            e.append(f"s{n}: ne satır ne şekil (çapasız madde): {cumleler[0][:40] if cumleler else ''}")
        for c in cumleler:
            n_cumle += 1
            if SES_YASAK.search(c):
                e.append(f"s{n}: ses işaret/rakam: {c[:60]}")
            if KISALTMA.search(c):
                e.append(f"s{n}: ses kısaltma: {KISALTMA.search(c).group(0)} — {c[:60]}")
            if cumle_sayisi(c) > 1 and any(len(p.split()) < 5 for p in cumlelere_bol(c)):
                e.append(f"s{n}: çok cümleli ve kısa parça (H109) — ayrı maddeler yaz: {c[:70]}")
            if not (5 <= len(c.split()) <= 40):
                e.append(f"s{n}: cümle uzunluğu {len(c.split())}: {c[:50]}")
            if parca_i % 5 == 0 and BAGLAMSIZ.match(c.strip()):
                e.append(f"s{n}: paragraf bağlamsız açılıyor: {c[:60]}")
            e += uslup_dene(c, f"s{n}")
            parca_i += 1
        if not (m.get("ekran") or "").strip():
            e.append(f"s{n}: ekran boş")
    if n_cumle < max(3, len(maddeler)):
        e.append(f"s{n}: cümle sayısı {n_cumle} < madde {len(maddeler)}")
    return e


def capa_bul(st: str, metin: str) -> str:
    """Çapa KAPISI birebir arar (konusma_v2.dogrula): dönen satır MUTLAKA sayfa metninde harfi harfine geçer.
    Model satırı birleştirmiş/bozmuşsa, sayfanın kendi satırlarından en çok örtüşeni çapa yapılır; o da yoksa çapa atılır."""
    st = (st or "").strip()
    if not st or not metin:
        return ""
    kat_sayfa = katla(metin)
    k = katla(st)
    if k and k in kat_sayfa:
        return st
    adaylar = [ln.strip() for ln in metin.splitlines() if ln.strip()]
    k_kel = {w for w in k.split() if len(w) > 2 or w.isdigit()}
    en, en_p = "", 0.0
    for ln in adaylar:
        kl = katla(ln)
        if not kl or kl not in kat_sayfa:
            continue
        kel = {w for w in kl.split() if len(w) > 2 or w.isdigit()}
        if not kel:
            continue
        puan = len(k_kel & kel) / len(kel)
        if puan > en_p:
            en, en_p = ln, puan
    return en if en_p >= 0.6 else ""


def tsv_yaz(taslak: Path, uretilen: dict[int, dict], smetin: dict[int, str], varl: dict | None = None) -> int:
    satirlar = []
    n_c = 0
    son_bolum = 0
    varl = varl or {}
    for n in sorted(uretilen):
        x = uretilen[n]
        # bölüm başlığı: sayfanın ilk satırı kısa bir başlıksa ve son bölümden ≥4 sayfa geçtiyse yeni bölüm
        ilk = next((s.strip() for s in (smetin.get(n) or "").splitlines() if s.strip()), "")
        if ilk and len(ilk) <= 70 and not ilk.endswith((".", ":", ";", ",")) and (n - son_bolum >= 4):
            satirlar.append("@@ " + re.sub(r"\s+", " ", ilk))
            son_bolum = n
        kat = katla(smetin.get(n) or "")
        ck = [c for c in (x.get("cikmis") or []) if isinstance(c, str)]
        maddeler = [m for m in (x.get("maddeler") or []) if isinstance(m, dict)]
        # görsel/tablolu sayfada hiç şekil tarifi yoksa: sayfanın kendi başlığını/tablo adını şekil çapası yap
        vv = varl.get(n) or {}
        gorsel_sayfa = (vv.get("gorsel_orani") or 0) >= 0.18 or (vv.get("cizim") or 0) >= 25 or bool(vv.get("tablolar"))
        if gorsel_sayfa and maddeler and not any((m.get("sekil") or "").strip() for m in maddeler):
            bas = next((t.strip() for t in (smetin.get(n) or "").splitlines() if t.strip()), "")
            maddeler[0] = {**maddeler[0], "sekil": (bas or "slayt görseli")[:90]}
        for m in maddeler:
            st = capa_bul(m.get("satir") or "", smetin.get(n) or "")
            ekran = re.sub(r"\s+", " ", (m.get("ekran") or "")).strip() or "..."
            sekil = str(m.get("sekil") or "").replace("|", " ").strip()
            for i, c in enumerate([c for c in (m.get("cumleler") or []) if isinstance(c, str) and c.strip()]):
                ses = re.sub(r"\s+", " ", c).strip().replace("|", " ")
                # H109 kapısı (her v2 cümlesi TEK cümle) — model iki cümleyi birleştirdiyse KOD böler,
                # böylece çapa/görsel/çıkmış etiketleri korunur ve tur içinde kapı hatası çıkmaz.
                parcalar = cumlelere_bol(ses)
                # maddenin her cümlesi aynı slayt satırına bağlanır (takip: cümle cümle doğru satır yanar)
                alan = ";;".join([st]) if st else "-"
                for j, parca in enumerate(parcalar):
                    ilk = i == 0 and j == 0
                    satirlar.append(f"s{n}|{parca}|{ekran}|{alan}|{','.join(ck) if ilk else ''}|{sekil if ilk else ''}")
                    n_c += 1
    (taslak / "metin.tsv").write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    return n_c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("key")
    ap.add_argument("--parca-sayfa", type=int, default=3)
    ap.add_argument("--zorla", action="store_true")
    ap.add_argument("--sayfa")
    ap.add_argument("--tsv-yenile", action="store_true", help="LLM'siz: uretim.json'dan metin.tsv'yi yeniden yaz + kapılar")
    a = ap.parse_args()
    _kilit("k3_uret")
    key = a.key
    taslak = DB / "taslak" / key
    baglam = json.loads((taslak / "baglam.json").read_text(encoding="utf-8"))
    smetin = sayfalar(taslak)
    varl = varlik(taslak)
    adaylar = json.loads((taslak / "cikmis_aday.json").read_text(encoding="utf-8")) if (taslak / "cikmis_aday.json").exists() else []

    # kapak (1. sayfa) ve tamamen boş sayfalar atlanır
    hedef = [n for n in sorted(smetin) if n != 1 and (smetin[n].strip() or (varl.get(n) or {}).get("gorsel_orani"))]
    if a.sayfa:
        sec = set()
        for parca in a.sayfa.split(","):
            if "-" in parca:
                x, y = parca.split("-")
                sec |= set(range(int(x), int(y) + 1))
            else:
                sec.add(int(parca))
        hedef = [n for n in hedef if n in sec]

    uret_yol = taslak / "uretim.json"
    uretilen = {} if a.zorla else {int(k): v for k, v in json.loads(uret_yol.read_text(encoding="utf-8")).items()} if uret_yol.exists() else {}

    if a.tsv_yenile:
        # Yalnız biçim/denetim düzeltmesi: LLM çağrısı YOK, mevcut üretim yeniden yazılır (token tasarrufu).
        kalan = [n for n in hedef if n not in uretilen]
        if kalan:
            print(f"[{key}] DİKKAT: {len(kalan)} sayfa hiç üretilmemiş: {kalan[:12]}")
        n = tsv_yaz(taslak, uretilen, smetin, varl)
        print(f"[{key}] metin.tsv (yenilendi): {n} cümle")
        r = subprocess.run([sys.executable, str(MEDS / "scripts" / "uretim" / "arsiv_25_26" / "k3_metin.py"), key])
        return r.returncode

    eksik = [n for n in hedef if n not in uretilen]
    kusur: dict[int, list[str]] = {}
    tur = 0
    while eksik and tur < 4:
        tur += 1
        ilerleme = 0
        for i in range(0, len(eksik), a.parca_sayfa):
            adet = a.parca_sayfa if tur == 1 else 1
            grup = eksik[i:i + adet]
            metin_grup = " ".join((smetin.get(n) or "") for n in grup).lower()
            kokler = set(re.findall(r"[a-zçğıöşü]{5,}", metin_grup))
            yerel = [q for q in adaylar
                     if len(set(re.findall(r"[a-zçğıöşü]{5,}", (q.get("soru") or "").lower())) & kokler) >= 2][:6]
            sonuc = None
            # Görsel/şema sayfası + az yazı: uzun istem modelde boş dönüyor → kısa istem ÖNCE denenir (H612)
            gorsel_agirlikli = all(
                ((varl.get(n) or {}).get("gorsel_orani") or 0) >= 0.18
                and len((smetin.get(n) or "").split()) < 45 for n in grup)
            if gorsel_agirlikli:
                sonuc = istek_kisa(baglam, {n: sayfa_metni(taslak, n, smetin, varl) for n in grup}, grup)
                if sonuc:
                    print(f"  [tur {tur}] s{grup[0]}–{grup[-1]}: görsel sayfa, kısa istemle alındı", flush=True)
            if not sonuc:
                sonuc = istek(baglam, smetin, varl, yerel, grup, {n: kusur[n] for n in grup if kusur.get(n)})
            if not sonuc and not gorsel_agirlikli:
                sonuc = istek_kisa(baglam, {n: sayfa_metni(taslak, n, smetin, varl) for n in grup}, grup)
                if sonuc:
                    print(f"  [tur {tur}] s{grup[0]}–{grup[-1]}: kısa istemle alındı", flush=True)
            if not sonuc and len(grup) > 1:
                yari = (len(grup) + 1) // 2
                for alt in (grup[:yari], grup[yari:]):
                    s2 = istek(baglam, smetin, varl, [], alt, {n: kusur[n] for n in alt if kusur.get(n)})
                    if s2:
                        sonuc = {**(sonuc or {}), **s2}
            if not sonuc:
                print(f"  [tur {tur}] s{grup[0]}–{grup[-1]}: yanıt yok", flush=True)
                continue
            for n in grup:
                x = sonuc.get(n)
                if not x:
                    print(f"  [tur {tur}] s{n}: yanıtta yok", flush=True)
                    continue
                hata = denetle_sayfa(x, n, smetin.get(n) or "", varl)
                if hata:
                    kusur[n] = hata
                    print(f"  [tur {tur}] s{n}: {len(hata)} sorun ({hata[0][:70]})", flush=True)
                    continue
                uretilen[n] = x
                ilerleme += 1
            uret_yol.write_text(json.dumps(uretilen, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  [tur {tur}] s{grup[0]}–{grup[-1]}: {len([n for n in grup if n in uretilen])}/{len(grup)}", flush=True)
        eksik = [n for n in hedef if n not in uretilen]
        if not ilerleme:
            break
    print(f"[{key}] üretilen sayfa {len(uretilen)}/{len(hedef)} · eksik {len(eksik)}{': ' + str(eksik[:15]) if eksik else ''}")
    n = tsv_yaz(taslak, uretilen, smetin, varl)
    print(f"[{key}] metin.tsv: {n} cümle")
    r = subprocess.run([sys.executable, str(MEDS / "scripts" / "uretim" / "arsiv_25_26" / "k3_metin.py"), key])
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
