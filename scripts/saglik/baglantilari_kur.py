#!/usr/bin/env python3
"""
Sağlık Bakanlığı sekmesi (/saglik) — ders bağlarını üretir (yerel, modelsiz).

Her bölüm için müfredattaki karşılıkları bulur:
  - çıkmış sorular  (src/data/pastQuestions.json: disiplin+konu eşleşmesi ya da kökte anahtar kelime)
  - kazanımlar      (src/data/kazanimlar/lite/k*.json)
  - Öğren desteleri (src/data/interactive_learning_decks.json; aynı sürüm grubundan en yenisi)
  - sınav spotları  (src/data/exam_spots_k1.json)
  - "Derste" çapaları: resmî veri bloğunu dersteki slayta bağlar (slayt başlığında anahtar kelime)

Çıktı:
  src/data/saglik/baglantilar.json      — hafif özet (sayılar, desteler, kazanımlar, spotlar, çapalar)
  src/data/saglik/sorular/<bolum>.json  — "Kendini sına" için soru metinleri (bölüm açılınca tembel yüklenir)

Kullanım: python3 scripts/saglik/baglantilari_kur.py
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
DATA = MEDS / "src" / "data"
OUT = DATA / "saglik"

HALK = {"Halk Sağlığı"}
ANNE_COCUK = {"Halk Sağlığı", "Kadın Hastalıkları ve Doğum", "Çocuk Sağlığı ve Hastalıkları", "Aile Hekimliği", "Tıbbi Genetik"}
ENF = {"Halk Sağlığı", "Enfeksiyon Hastalıkları", "Tıbbi Mikrobiyoloji", "Çocuk Sağlığı ve Hastalıkları"}

# Bölüm tanımları. konular: çıkmış soru "topic" ve kazanım "konu" adları (birebir). anahtar: kökte aranır
# (yalnız `disiplinler` içindeki sorularda). capalar: sayfadaki veri bloğu → dersteki slayt (başlıkta aranır).
BOLUMLER: dict[str, dict] = {
    "asi": {
        "konular": ["Bağışıklama ve önemi"],
        "disiplinler": (ENF | ANNE_COCUK) - {"Tıbbi Genetik"},
        "deste_konulari": ["Ana-Çocuk Sağlığı Düzeyinin İzlenmesi", "Halk Sağlığı Tarihçesi", "Gebelik ve Emzirme Döneminde Beslenme"],
        "anahtar": [r"\başı(?!r)", r"bağışıklama", r"\bBCG\b", r"\bKKK\b", r"DaBT", r"soğuk zincir", r"toksoid", r"immünizasyon", r"aşılama"],
        "capalar": {
            "takvim": [r"aşı takvim", r"bağışıklama"],
            "gebe_asi": [r"bağışıklama", r"tetanoz"],
            "tarihce": [r"aşı(?!r)", r"çiçek"],
        },
    },
    "yenidogan": {
        "konular": ["Bebek Beslenmesi", "Çocuk Sağlığı", "Fetal Dolaşım ve Neonatal adaptasyon", "Solunum sıkıntısı olan yeni doğana yaklaşım", "Neonatal Kolestaz"],
        "disiplinler": ANNE_COCUK - {"Tıbbi Genetik"},
        "ek": [(r"fenilketon|topuk kan|yenidoğan tarama|konjenital hipotiroid|biyotinidaz", {"Tıbbi Genetik", "Tıbbi Biyokimya"})],
        "deste_konulari": ["Ana-Çocuk Sağlığı Düzeyinin İzlenmesi"],
        "anahtar": [r"yenidoğan", r"yeni doğan", r"topuk kan", r"fenilketon", r"konjenital hipotiroid", r"anne sütü", r"emzir", r"bebek ölüm", r"neonatal ölüm", r"perinatal", r"D vitamini", r"demir desteğ", r"kolostrum"],
        "capalar": {
            "bebek_izlem": [r"bebek izlem takvim", r"bebek ve çocuk izlem"],
            "cocuk_izlem": [r"çocuk izlem takvim"],
            "yenidogan_muayene": [r"yenidoğanın ilk", r"ilk ziyaret"],
            "k_vitamini": [r"K vitamini"],
            "buyume": [r"büyüme", r"tartı", r"gelişim basamak"],
            "anne_sutu": [r"anne sütü", r"emzirme"],
            "tamamlayici": [r"tamamlayıcı", r"ek gıda"],
            "destekler": [r"demir", r"d vitamini"],
            "gostergeler": [r"bebek ölüm", r"gösterge"],
        },
    },
    "anne_kadin": {
        "konular": ["Ana-Çocuk Sağlığı Düzeyinin İzlenmesi", "Gebelik ve Emzirme Döneminde Beslenme", "Abortus", "Gebelik Terminolojisi/Kavramları", "İntrauterin Enfeksiyonlar"],
        "disiplinler": ANNE_COCUK,
        "anahtar": [r"\bgebe", r"lohusa", r"loğusa", r"anne ölüm", r"doğum öncesi bakım", r"kessner", r"sezaryen", r"aile planlaması", r"kontrasep", r"doğurganlık"],
        "capalar": {
            "anne_olum": [r"anne ölüm"],
            "dob": [r"doğum öncesi bakım", r"\bDÖB\b"],
            "gebe_izlem": [r"gebe izlem"],
            "kessner": [r"kessner"],
            "tehlike": [r"tehlike işaret"],
            "lohusa": [r"lohusa", r"loğusa"],
            "kadin_izlem": [r"15-49"],
            "tnsa": [r"TNSA"],
            "beslenme": [r"gebelik.*beslenme", r"emzirme dönemi", r"enerji", r"folik"],
        },
    },
    "tarama": {
        "konular": ["Kanser Hastalıkları Epidemiyolojisi", "Prenatal Tanı Yöntemleri", "Aile Hekimliğinde Periyodik Muayeneler 1", "Aile Hekimliğinde Periyodik Muayeneler 2", "Koruyucu Sağlık Hizmetleri"],
        "disiplinler": HALK | {"Aile Hekimliği", "Kadın Hastalıkları ve Doğum"},
        "ek": [(r"tarama|üçlü test|ikili test|ense kalınlığı", {"Tıbbi Genetik"})],
        "deste_konulari": ["Ana-Çocuk Sağlığı Düzeyinin İzlenmesi"],
        "anahtar": [r"tarama", r"KETEM", r"mamograf", r"smear", r"\bHPV\b", r"gaitada gizli kan", r"erken tanı", r"erken teşhis", r"duyarlılı", r"seçicili", r"sensitivite", r"spesifite", r"kestirim değer", r"prediktif"],
        "capalar": {
            "prenatal": [r"kombine tarama", r"üçlü test", r"ense"],
            "kanser": [r"kanser tarama", r"meme kanser", r"serviks kanser", r"kolorektal"],
            "periyodik": [r"periyodik"],
        },
    },
    "salgin": {
        "konular": ["Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri", "Enfeksiyon Hastalıklarının Epidemiyolojisi", "Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler", "İzolasyon Yöntemleri", "Kırım-Kongo kanamalı ateşi", "Kolera", "Zoonotik Enfeksiyonlar", "İnfluenza", "Cinsel yolla bulaşan hastalıklarda profilaksi ve korunma"],
        "disiplinler": ENF - {"Çocuk Sağlığı ve Hastalıkları"},
        "anahtar": [r"salgın", r"sürveyans", r"bildirim", r"ihbar", r"karantina", r"izolasyon", r"filyasyon", r"atak hızı", r"kuluçka", r"epidemi", r"pandemi", r"endemi", r"portör"],
        "capalar": {
            "surveyans": [r"sürveyans"],
            "bildirim": [r"bildirim", r"ihbar"],
            "inceleme": [r"salgın incele", r"basamak", r"aşama"],
            "kontrol": [r"kontrol", r"korunma", r"karantina", r"izolasyon"],
            "zincir": [r"bulaş zinciri", r"enfeksiyon zinciri", r"halka"],
        },
    },
    "cevre": {
        "konular": ["Çevre Sağlığına Giriş ve Genel Bilgiler", "Meslek hastalıkları", "İş kazaları", "Halk sağlığını etkileyen faktörler"],
        "disiplinler": HALK,
        "deste_konulari": ["Genetik, Pediatrik ve Çevresel Patoloji"],
        "anahtar": [r"çevre sağlığı", r"içme suyu", r"\bklor", r"hava kirlili", r"gürültü", r"atık", r"meslek hastalı", r"iş kazası", r"pnömokonyoz", r"silikoz"],
        "capalar": {"su": [r"\bsu\b", r"klor"], "hava": [r"hava kirlili", r"hava"], "meslek": [r"meslek", r"iş kazası", r"pnömokonyoz"], "cevre_patoloji": [r"çevre", r"çevresel"]},
    },
    "kurumlar": {
        "konular": ["Türkiye’de Sağlık Hizmetleri", "Sağlığın Sosyalleştirilmesi ve Temel Sağlık Hizmetleri (TSH)", "Sağlık Yönetimi", "Halk Sağlığı Tarihçesi", "Aile Hekimliğine Yaklaşım", "Koruyucu Sağlık Hizmetleri"],
        "disiplinler": HALK | {"Aile Hekimliği"},
        "anahtar": [r"aile hekim", r"sağlık ocağı", r"basamak", r"sevk zinciri", r"\b224\b", r"sosyalleştir", r"Alma.?Ata", r"toplum sağlığı merkezi", r"Umumi Hıfzıssıhha", r"sağlıkta dönüşüm"],
        "capalar": {
            "basamak": [r"basamak"],
            "tarihce": [r"cumhuriyet", r"türkiye.{0,20}(tarih|dönem)"],
            "aile_hekimligi": [r"aile hekim"],
            "sosyalizasyon": [r"224", r"sosyalleştir"],
        },
    },
    "istatistik": {
        "konular": ["Sağlık Göstergeleri", "Epidemiyolojiye Giriş", "Vaka-Kontrol çalışmaları", "Kohort Çalışmaları", "Deneysel ve Kesitsel Çalışmalar", "Kardiyovasküler sistem hastalıklarının epidemiyolojisi", "Yaşlı Sağlığı Sorunları ve Sağlık Hizmetleri", "Yaşlı Sağlığı Sorunları ve Sağlık"],
        "disiplinler": HALK,
        "deste_konulari": ["Ana-Çocuk Sağlığı Düzeyinin İzlenmesi", "Bebek Beslenmesi", "Enfeksiyon Hastalıklarının Epidemiyolojisi"],
        "anahtar": [r"ölüm hızı", r"doğum hızı", r"doğurganlık hızı", r"insidans", r"prevalans", r"yaşam süresi", r"bebek ölüm", r"\bhız\b", r"oran(ı|i)\b", r"gösterge"],
        "capalar": {"gostergeler": [r"demografik gösterge", r"gösterge"], "anne_olum": [r"anne ölüm oranı"], "bebek_olum": [r"bebek ölüm"], "tnsa": [r"TNSA"], "olcutler": [r"insidans", r"prevalans", r"hız"]},
    },
    "halk_sagligi": {
        "konular": ["Halk Sağlığı Tarihçesi", "Sağlığın geliştirilmesi", "Sağlık Eğitimi", "Yeterli ve Dengeli Beslenme", "Önemli Beslenme Sorunları", "Okul Sağlığı", "Mobbing", "Akılcı İlaç Kullanımı", "Koruyucu Sağlık Hizmetleri"],
        "disiplinler": HALK,
        "anahtar": [],
        "capalar": {"koruma_duzeyleri": [r"koruyucu", r"korunma düzey"], "tarihce": [r"tarih"]},
    },
}
# Karabük ve genel bakış kendi sorularını taşımaz; ilgili bölümlerin bağlarını kullanır.
KARABUK_BOLUMLERI = ["kurumlar", "cevre", "istatistik"]

MUFREDAT_DERSLERI = {"Halk Sağlığı", "Aile Hekimliği"}
SORU_SINIRI = 80  # bölüm başına "Kendini sına" havuzu
TIER_PUAN = {"altin": 4, "saglam": 3, "yuksek": 3, "orta": 2, "kritik": 0, "zayif": 0}


def katla(s: str) -> str:
    s = (s or "").replace("’", "'").replace("İ", "i").replace("I", "ı").lower()
    return unicodedata.normalize("NFC", s)


def konu_anahtar(s: str) -> str:
    return re.sub(r"\s+", " ", katla(s).replace("'", "").replace("’", "")).strip()


def yukle(p: Path):
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def soru_metin(q: dict) -> str:
    return q.get("stem") or (q.get("reconstruction") or {}).get("stem") or ""


def secenekler(q: dict) -> list[dict]:
    ops = q.get("options") or (q.get("reconstruction") or {}).get("options") or []
    out = []
    for o in ops:
        if isinstance(o, dict):
            t = (o.get("text") or "").strip()
            k = (o.get("key") or o.get("label") or "").strip()
            if t and k:
                out.append({"k": k, "t": t})
    return out


def kurul_no(q: dict):
    k = q.get("kurul")
    if isinstance(k, int):
        return k
    m = re.search(r"kurul(\d)", q.get("committeeId") or "")
    return int(m.group(1)) if m else None


def main() -> None:
    sorular = yukle(DATA / "pastQuestions.json")
    desteler = yukle(DATA / "interactive_learning_decks.json")
    spot_veri = yukle(DATA / "exam_spots_k1.json")
    pdf_kaynak = yukle(DATA / "deckPdfSources.json").get("decks", {})

    # --- kazanımlar: konu adı → [(kurul, ders, konu, kazanım)]
    kz_konu: dict[str, list] = defaultdict(list)
    for k in range(1, 7):
        p = DATA / "kazanimlar" / "lite" / f"k{k}.json"
        if not p.exists():
            continue
        for ders in yukle(p).get("dersler", []):
            for konu in ders.get("konular", []):
                kz_konu[konu_anahtar(konu["konu"])].append((k, ders["ders"], konu["konu"], konu.get("kazanimlar", [])))

    # --- desteler: sürüm grubundan en yenisini (V2 > V1) tut
    grup: dict[str, dict] = {}
    for d in desteler:
        g = d.get("versionGroup") or re.sub(r"-v\d+$", "", d["id"])
        eski = grup.get(g)
        if eski is None or (d.get("versionLabel") or "V1") > (eski.get("versionLabel") or "V1"):
            grup[g] = d
    guncel = list(grup.values())
    not_to_deste = {}
    for d in guncel:
        if d.get("matchedNoteId"):
            not_to_deste[d["matchedNoteId"]] = d

    def deste_konu(d: dict) -> str:
        return konu_anahtar(d.get("matchedNoteTitle") or d.get("title") or "")

    # --- spotlar: ders başlığı → spotlar
    spot_ders = {d["no"]: d for d in spot_veri.get("dersler", [])}
    spot_konu: dict[str, list] = defaultdict(list)
    for s in spot_veri.get("spotlar", []):
        d = spot_ders.get(s.get("ders"))
        if d:
            spot_konu[konu_anahtar(d["baslik"])].append((d, s))

    def konu_esles(a: str, b: str) -> bool:
        a, b = konu_anahtar(a), konu_anahtar(b)
        if not a or not b:
            return False
        if a == b:
            return True
        # "Ana-Çocuk Sağlığı Düzeyinin İzlenmesi" ~ "Ana Çocuk Sağlığı Düzeyinin İzlenmesi"
        sade = lambda x: re.sub(r"[^a-zçğıöşü0-9 ]", " ", x).split()
        sa, sb = sade(a), sade(b)
        return sa == sb or (len(sa) >= 3 and " ".join(sa) in " ".join(sb)) or (len(sb) >= 3 and " ".join(sb) in " ".join(sa))

    sonuc: dict = {"uretildi": date.today().isoformat(), "bolumler": {}}
    (OUT / "sorular").mkdir(parents=True, exist_ok=True)

    for bid, tan in BOLUMLER.items():
        konular = tan["konular"]
        desen = re.compile("|".join(tan["anahtar"]), re.I) if tan["anahtar"] else None

        # ---- çıkmış sorular
        secilen = []
        for q in sorular:
            if q.get("status") == "quarantined":
                continue
            if q.get("donem") not in ("Dönem 3", 3):
                continue
            neden = None
            if any(konu_esles(q.get("topic") or "", k) for k in konular):
                neden = "konu"
            elif desen and q.get("discipline") in tan["disiplinler"] and desen.search(soru_metin(q)):
                neden = "anahtar"
            elif any(q.get("discipline") in dis and re.search(rx, soru_metin(q), re.I) for rx, dis in tan.get("ek", [])):
                neden = "anahtar"
            if not neden:
                continue
            ops = secenekler(q)
            dogru = (q.get("correctAnswer") or "").strip()
            if len(ops) < 2 or dogru not in {o["k"] for o in ops}:
                continue
            secilen.append((q, neden, ops, dogru))

        yil_say = Counter((q.get("examYear") or "Bilinmiyor") for q, *_ in secilen)
        konu_say = Counter((q.get("topic") or "—") for q, *_ in secilen)
        kurul_say = Counter(str(kurul_no(q) or "?") for q, *_ in secilen)

        def puan(t):
            q, neden, *_ = t
            return (1 if neden == "konu" else 0, TIER_PUAN.get(q.get("qualityTier") or "", 1), q.get("examYear") or "")

        havuz = sorted(secilen, key=puan, reverse=True)[:SORU_SINIRI]
        soru_dosya = []
        for q, neden, ops, dogru in havuz:
            soru_dosya.append({
                "id": q["id"],
                "kok": soru_metin(q).strip(),
                "secenekler": ops,
                "dogru": dogru,
                "aciklama": (q.get("explanation") or "").strip()[:1600],
                "yil": q.get("examYear") or "",
                "kurul": kurul_no(q),
                "ders": q.get("discipline") or "",
                "konu": q.get("topic") or "",
            })
        with (OUT / "sorular" / f"{bid}.json").open("w", encoding="utf-8") as f:
            json.dump(soru_dosya, f, ensure_ascii=False, separators=(",", ":"))

        # ---- kazanımlar
        kz_list = []
        for k in konular:
            for kurul, ders, konu, kzs in kz_konu.get(konu_anahtar(k), []):
                if ders not in tan["disiplinler"] and ders not in HALK:
                    continue
                kz_list.append({
                    "kurul": kurul, "ders": ders, "konu": konu, "anahtar": f"{ders}::{konu}",
                    "kazanimlar": [{"id": z.get("id"), "metin": z.get("metin")} for z in kzs][:15],
                    "cikmis": sum(int(z.get("totalCikmisCount") or 0) for z in kzs),
                })

        # ---- desteler (bölüm konuları + yalnız slayt bağı için ek konular; ek desteler sona)
        dst = []
        gorulen = set()
        for d in sorted(guncel, key=lambda x: not any(konu_esles(deste_konu(x), k) for k in konular)):
            if d["id"] in gorulen:
                continue
            if any(konu_esles(deste_konu(d), k) or konu_esles(d.get("title") or "", k) for k in konular + tan.get("deste_konulari", [])):
                gorulen.add(d["id"])
                pdf = pdf_kaynak.get(d["id"]) or {}
                dst.append({
                    "id": d["id"], "baslik": d.get("title"), "kisa": d.get("shortTitle") or d.get("title"),
                    "ders": d.get("discipline"), "kurul": d.get("committee"), "hoca": d.get("instructor") or "",
                    "slayt": len(d.get("slides") or []), "pdf": bool(pdf.get("files")),
                    "ozet": (d.get("overview") or "")[:400],
                    "ek": not any(konu_esles(deste_konu(d), k) or konu_esles(d.get("title") or "", k) for k in konular),
                })

        # ---- çapalar: veri bloğu → deste slaytı
        capalar = {}
        for cid, desenler in tan.get("capalar", {}).items():
            rx = [re.compile(x, re.I) for x in desenler]
            bulunan = []
            for d in dst:
                tam = next((x for x in guncel if x["id"] == d["id"]), None)
                if not tam:
                    continue
                for i, sl in enumerate(tam.get("slides") or []):
                    t = sl.get("title") or ""
                    if "CHECKPOINT" in t or "OYUN SAYFASI" in t:
                        continue
                    if any(r.search(t) for r in rx):
                        bulunan.append({"deste": d["id"], "kisa": d["kisa"], "slayt": i + 1, "baslik": t})
                        break
            if bulunan:
                capalar[cid] = bulunan[:3]

        # ---- spotlar
        spt = []
        for k in konular:
            for dk, liste in spot_konu.items():
                if konu_esles(dk, k):
                    for d, s in liste:
                        spt.append({"id": s["id"], "baslik": s.get("baslik"), "spot": s.get("spot"), "onem": s.get("onem", 1), "ders": d["baslik"]})
        spt.sort(key=lambda x: -int(x.get("onem") or 0))

        sonuc["bolumler"][bid] = {
            "konular": konular,
            "soru_sayisi": len(secilen),
            "havuz": len(soru_dosya),
            "yillar": dict(sorted(yil_say.items(), reverse=True)),
            "konu_dagilimi": dict(konu_say.most_common(12)),
            "kurul_dagilimi": dict(sorted(kurul_say.items())),
            "kazanimlar": kz_list,
            "desteler": dst,
            "capalar": capalar,
            "spotlar": spt[:24],
        }
        print(f"{bid:13s} soru={len(secilen):4d} havuz={len(soru_dosya):3d} kazanım-konu={len(kz_list):2d} deste={len(dst):2d} çapa={len(capalar):2d} spot={len(spt):3d}")

    # ---- müfredat haritası: tüm kurullardaki Halk Sağlığı (+ Aile Hekimliği) konuları
    konu_soru = Counter(konu_anahtar(q.get("topic") or "") for q in sorular
                        if q.get("status") != "quarantined" and q.get("discipline") in MUFREDAT_DERSLERI)
    mufredat = []
    for liste in kz_konu.values():
        for kurul, ders, konu, kzs in liste:
            if ders not in MUFREDAT_DERSLERI:
                continue
            deste = next((d["id"] for d in guncel if konu_esles(deste_konu(d), konu)), None)
            mufredat.append({"kurul": kurul, "ders": ders, "konu": konu, "anahtar": f"{ders}::{konu}",
                             "kazanim": len(kzs), "cikmis": konu_soru.get(konu_anahtar(konu), 0), "deste": deste})
    mufredat.sort(key=lambda x: (x["kurul"], x["ders"], -x["cikmis"]))
    sonuc["mufredat"] = mufredat
    print("müfredat konusu:", len(mufredat))

    sonuc["karabuk_bolumleri"] = KARABUK_BOLUMLERI
    with (OUT / "baglantilar.json").open("w", encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=1)
    print("yazıldı:", OUT / "baglantilar.json")


if __name__ == "__main__":
    main()
