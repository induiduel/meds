#!/usr/bin/env python3
"""2025-2026 Kurul 3 (GİS) arşiv ders eşlemesi — TEK KAYNAK.

Her satır bir PDF = bir arşiv dersi. `program` alanı bu dersin 2026-2027 k3 programındaki hangi ders(ler)e
karşılık geldiğini söyler (boş = programda yok, yine de arşivde yaşar; kullanıcı kararı 2026-11-17).

  k3_eslesme.py yaz      → meds_database_25_26/kurul3_eslesme.json (envanterle doğrulanır: 58/58 dosya eşleşmeli)
  k3_eslesme.py denetle  → eşleşmeyen dosya / var olmayan id
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

import json
import sys
from pathlib import Path

MEDS = _kok.MEDS
DB = MEDS.parent / "meds_database_25_26"

# (file_id, anahtar, branş, branş no, başlık, hoca, program dersleri)
MAP = [
    # ── İç Hastalıkları (dahiliye) ────────────────────────────────────────────────────────────────
    ("17k0sN8eV122ODr4RMbzyT1hFEnghl7yz", "y25-k3-01-gastroenteritler-ve-bakteriyel-ishaller", "İç Hastalıkları", 1,
     "Gastroenteritler ve Bakteriyel İshaller", "Dr. Ceren Çevik", ["k3-01", "k3-02"]),
    ("1zrQMHoRlVhfb3eENeQ3fdiK79ri5Sf6p", "y25-k3-02-gis-motilite-bozukluklari", "İç Hastalıkları", 2,
     "Gastrointestinal Sistem Motilite Bozuklukları", "Uzm. Dr. Murat Ayberk Aytemiz", ["k3-03"]),
    ("1dZVFb389hpGmPY9knWhZOpqFLFf0UvXV", "y25-k3-03-ailesel-akdeniz-atesi", "İç Hastalıkları", 3,
     "Ailesel Akdeniz Ateşi (FMF)", "Uzm. Dr. Murat Ayberk Aytemiz", ["k3-04"]),
    ("1x0u6rntxrKzwKACjFtV9BYjw_QYFsPbv", "y25-k3-04-peptik-ulser-hastaligi", "İç Hastalıkları", 4,
     "Peptik Ülser Hastalığı", "Dr. Öğr. Üyesi Kenan Koşar", ["k3-09"]),
    ("1V1L9rIZtHnesfd56LhDOnNlKQ2_74gXa", "y25-k3-05-sarilikli-hastaya-yaklasim", "İç Hastalıkları", 5,
     "Sarılıklı Hastaya Yaklaşım", "Dr. Öğr. Üyesi Kenan Koşar", ["k3-10"]),
    ("1ARFFzR9y8bdqeINVkTg9Iz-SHjYX7TZ6", "y25-k3-06-gis-kanamalari", "İç Hastalıkları", 6,
     "Gastrointestinal Sistem Kanamaları", "Dr. Öğr. Üyesi Kenan Koşar", ["k3-11", "k3-12"]),
    ("1DfchVzVBs799Yo5ht_lUCv-qV5-D1txC", "y25-k3-07-gis-parazitozlari", "İç Hastalıkları", 7,
     "Gastrointestinal Sistem Parazitozları", "Uzm. Dr. Abdurrahim Yıldırım", ["k3-16"]),
    ("1sWPD0Wn78dxVuAgp9b13KzKVYrL0XkBt", "y25-k3-08-besin-zehirlenmeleri", "İç Hastalıkları", 8,
     "Besin Zehirlenmeleri", "Uzm. Dr. Abdurrahim Yıldırım", []),
    ("1l5nD2L-Gx4NecBvREG8CLGZsnDjG5i_z", "y25-k3-09-akut-hepatitler", "İç Hastalıkları", 9,
     "Akut Hepatitler", "Doç. Dr. Fatih İnci", ["k3-43"]),
    ("11fMVsKXgjljS741TU9sr-YpOUZMeBZun", "y25-k3-10-akut-pankreatit", "İç Hastalıkları", 10,
     "Akut Pankreatit", "Uzm. Dr. Betül Danapınar", ["k3-37"]),
    ("1iTe5if7SdB7U5CQOGbPoHeil_RNhv5kT", "y25-k3-11-sindirim-sistemi-kanserleri", "İç Hastalıkları", 11,
     "Sindirim Sistemi Kanserleri", "Prof. Dr. Fatih Karataş", ["k3-33"]),
    ("1RBsLDfAZqDbLHwlZZea4ALqG0BUqUbJU", "y25-k3-12-kolonun-premalign-lezyonlari", "İç Hastalıkları", 12,
     "Kolonun Premalign Lezyonları", "Prof. Dr. Fatih Karataş", ["k3-34"]),
    ("1tSfXIlsR_-7E97QqiVQMc456Cn71Np9I", "y25-k3-13-kronik-diare-ve-malabsorbsiyon", "İç Hastalıkları", 13,
     "Kronik Diare ve Malabsorbsiyon Sendromları", "Uzm. Dr. Sinem İpor", ["k3-44"]),
    ("1247iviOO46zQt-WT9cLA9U3NoUC4rrKb", "y25-k3-14-gist", "İç Hastalıkları", 14,
     "Gastrointestinal Stromal Tümör (GIST)", "Prof. Dr. Fatih Karataş", []),
    ("1CVTHwC2cc_3OptIZibhYaWD1uMt6KRHx", "y25-k3-15-noroendokrin-tumorler", "İç Hastalıkları", 15,
     "Nöroendokrin Tümörler", "Prof. Dr. Fatih Karataş", []),
    ("15_r2qODF4L52SEzLfcmcEfJlqC8UBuG8", "y25-k3-16-primer-biliyer-kolanjit", "İç Hastalıkları", 16,
     "Primer Biliyer Kolanjit", "Uzm. Dr. Betül Danapınar", ["k3-47"]),
    # ── Tıbbi Farmakoloji ────────────────────────────────────────────────────────────────────────
    ("16A7kUZaoXycT7-_If0ZuSHKaq53DnRx5", "y25-k3-17-sulfonamidler-trimetoprim-kinolonlar", "Tıbbi Farmakoloji", 1,
     "Sülfonamidler, Trimetoprim ve Kinolonlar", "Dr. Öğr. Üyesi Namık Bilici", ["k3-05"]),
    ("1L-nbskICw9HTqlFW4r5iJ0jlwxUaZnLm", "y25-k3-18-antihelmintik-ilaclar", "Tıbbi Farmakoloji", 2,
     "Antihelmintik İlaçlar", "Dr. Öğr. Üyesi Namık Bilici", ["k3-06"]),
    ("1so9cYP8aGx68PmCl4IDz8b9trPZwx4Q5", "y25-k3-19-aminoglikozidler-ve-spektinomisin", "Tıbbi Farmakoloji", 3,
     "Aminoglikozidler ve Spektinomisin", "Prof. Dr. Mehmet Özdemir", ["k3-07"]),
    ("1tWnf7W1TxAEybtiiY7A6ZFRRUeAJiysy", "y25-k3-20-tetrasiklinler-makrolidler-kloramfenikol", "Tıbbi Farmakoloji", 4,
     "Tetrasiklinler, Makrolidler ve Kloramfenikol", "Prof. Dr. Mehmet Özdemir", ["k3-08"]),
    ("1PcFdH7-3CcouGroanKaC2qYa87yjp7P3", "y25-k3-21-gis-ilaclari-1", "Tıbbi Farmakoloji", 5,
     "Gastrointestinal Sistem İlaçları 1", "Dr. Öğr. Üyesi Namık Bilici", ["k3-17"]),
    ("18uBRgLuoRva_AaE5TLtooJ8cElgbk2wc", "y25-k3-22-gis-ilaclari-2", "Tıbbi Farmakoloji", 6,
     "Gastrointestinal Sistem İlaçları 2", "Dr. Öğr. Üyesi Namık Bilici", ["k3-21"]),
    ("1VWZXEE6_YUnCEGxL8BsAe_N0KG4hCrVH", "y25-k3-23-antiemetik-ilaclar", "Tıbbi Farmakoloji", 7,
     "Antiemetik İlaçlar", "Dr. Öğr. Üyesi Namık Bilici", ["k3-20"]),
    ("1WxYStEhsTXMr0ItRtERoNLihqPe1S3fg", "y25-k3-24-dislipidemide-kullanilan-ilaclar", "Tıbbi Farmakoloji", 8,
     "Dislipidemide Kullanılan İlaçlar", "Prof. Dr. Mehmet Özdemir", ["k3-18"]),
    ("13iowBt9IImgrEimef5b0-JFXDH6nRuva", "y25-k3-25-antifungal-ajanlar", "Tıbbi Farmakoloji", 9,
     "Antifungal Ajanlar", "Prof. Dr. Mehmet Özdemir", ["k3-19"]),
    ("1EBBR4d__MtCZFfXNQLYTBt9ayyWihP0v", "y25-k3-26-antimikobakteriyel-ilaclar", "Tıbbi Farmakoloji", 10,
     "Antimikobakteriyel İlaçlar", "Dr. Öğr. Üyesi Namık Bilici", ["k3-30"]),
    ("1scY2g-p1DJH24Z0dWF-UFGSSFRHjZ_fz", "y25-k3-27-antimikrobik-ajanlarin-klinik-kullanimi", "Tıbbi Farmakoloji", 11,
     "Antimikrobik Ajanların Klinik Kullanımı", "Prof. Dr. Mehmet Özdemir", ["k3-31"]),
    ("1wRZsHsACMzdh2dvLa36_TXpplDah-IhW", "y25-k3-28-beta-laktam-antibiyotikler", "Tıbbi Farmakoloji", 12,
     "Beta Laktam ve Hücre Duvarı Aktif Antibiyotikler", "Prof. Dr. Mehmet Özdemir", ["k3-55"]),
    ("1hpC1JEXxchv0CjrFnTFcyAeWM6Bw11sx", "y25-k3-29-antiviral-ilaclar", "Tıbbi Farmakoloji", 13,
     "Antiviral İlaçlar", "Dr. Öğr. Üyesi Namık Bilici", ["k3-53"]),
    ("1NuU35NRsyuUYwIsLKg1SbHvCIrKGjtPS", "y25-k3-30-dezenfektan-ve-sterilizanlar", "Tıbbi Farmakoloji", 14,
     "Dezenfektan ve Sterilizan Ajanlar", "Dr. Öğr. Üyesi Namık Bilici", ["k3-45"]),
    ("1x3VkRGkx3pILS1IDoQGh21Zj3GhK4QWi", "y25-k3-31-otc-ilaclarin-terapotik-ve-toksik-etkileri", "Tıbbi Farmakoloji", 15,
     "OTC İlaçların Terapötik ve Toksik Etkileri", "Dr. Öğr. Üyesi Namık Bilici", ["k3-46"]),
    ("1YKvtZAkxokNj7ilTOJEUW6EV0fDjThpH", "y25-k3-32-vazoaktif-peptidler-ve-eikozanoidler", "Tıbbi Farmakoloji", 16,
     "Vazoaktif Peptidler ve Eikozanoidler", "Dr. Öğr. Üyesi Namık Bilici", ["k3-54"]),
    ("1lTNJIVSUsEq_4pB9GvOCwmZUVAWk9xfD", "y25-k3-33-zehirlenmeler-ve-yonetimi", "Tıbbi Farmakoloji", 17,
     "Zehirlenmeler ve Zehirlenmelerde Genel Yönetim", "Dr. Öğr. Üyesi Namık Bilici", ["k3-39"]),
    # ── Tıbbi Patoloji ───────────────────────────────────────────────────────────────────────────
    ("1TgYuDXixgTDM1PewdZiyS7Ms_WKUaFMr", "y25-k3-34-ozofagus-hastaliklari-1", "Tıbbi Patoloji", 1,
     "Özofagus Hastalıkları 1: Özofajitler ve Motilite", "Dr. Alpay Aktümen", ["k3-13"]),
    ("188t2amgXwFDzcdA-UaHAVNy-Taaigrv9", "y25-k3-35-ozofagus-hastaliklari-2", "Tıbbi Patoloji", 2,
     "Özofagus Hastalıkları 2: Tümörler ve Variköz Venler", "Dr. Alpay Aktümen", ["k3-13"]),
    ("1JIG-IasKQQU0Z_TiQNulF2kJoqTPiO7t", "y25-k3-36-oral-mukoza-inflamatuar-hastaliklari", "Tıbbi Patoloji", 3,
     "Oral Mukozanın İnflamatuar Hastalıkları", "Dr. Alpay Aktümen", []),
    ("1NQQ3D-B2Ht4ltSKrZN5ZbaBlSc7_X4w_", "y25-k3-37-oral-mukoza-proliferatif-neoplastik", "Tıbbi Patoloji", 4,
     "Oral Mukozanın Proliferatif ve Neoplastik Hastalıkları", "Dr. Alpay Aktümen", []),
    ("1D60S8B_tbSSKqXqIg7ii_4ip8VmMyP44", "y25-k3-38-tukruk-bezi-hastaliklari", "Tıbbi Patoloji", 5,
     "Tükürük Bezi Hastalıkları", "Dr. Alpay Aktümen", []),
    ("1fzlaaPPz_yiBtbjctj1T-ENL8JTN7ouR", "y25-k3-39-midenin-inflamatuar-hastaliklari", "Tıbbi Patoloji", 6,
     "Midenin İnflamatuar Hastalıkları: Gastrit Tipleri ve Peptik Ülser", "Prof. Dr. Hikmet Keleş", ["k3-14", "k3-22"]),
    ("1Py_OzorTaGGV-q5Jsb0Mzahtp7-OEVU7", "y25-k3-40-mide-polipleri-ve-tumorleri", "Tıbbi Patoloji", 7,
     "Mide Polipleri ve Mide Tümörleri", "Dr. Alpay Aktümen", ["k3-23"]),
    ("1bQz-JjGgykdEh23iIT9bMNzvun4ckK9b", "y25-k3-41-inflamatuar-barsak-hastaligi", "Tıbbi Patoloji", 8,
     "İnflamatuar Bağırsak Hastalığı: Crohn ve Ülseratif Kolit", "Prof. Dr. Hikmet Keleş", ["k3-27", "k3-28"]),
    ("1bHPgmebEqUz5_cAqzTC71A4AODDMoQG0", "y25-k3-42-divertikuler-hastalik-ve-apendiks", "Tıbbi Patoloji", 9,
     "Divertiküler Hastalık ve Apendiks", "Prof. Dr. Hikmet Keleş", ["k3-26", "k3-36"]),
    ("1QcZNFhETlhvSkw_mD8U9TWpEtUbTt2eD", "y25-k3-43-barsak-tikanmalari-ve-damarsal-hastaliklari", "Tıbbi Patoloji", 10,
     "Barsak Tıkanmaları ve Barsağın Damarsal Hastalıkları", "Prof. Dr. Hikmet Keleş", []),
    ("1vHWQdafGbIJZGcquva4GpjX_OsXy1ebF", "y25-k3-44-kolon-polipleri", "Tıbbi Patoloji", 11,
     "Kolon Polipleri ve Polipozis Sendromları", "Prof. Dr. Hikmet Keleş", ["k3-29"]),
    ("1HhUnB5c1whlj22iD48laalxJgQFDcYc5", "y25-k3-45-kolorektal-karsinom", "Tıbbi Patoloji", 12,
     "Kolorektal Karsinom", "Prof. Dr. Hikmet Keleş", ["k3-35", "k3-36"]),
    ("1TFT8Nlmh-xsyjqnyXHEPV5QFlQJ2KhEq", "y25-k3-46-amiloidoz", "Tıbbi Patoloji", 13,
     "Amiloidoz", "Prof. Dr. Hikmet Keleş", []),
    ("185lWXzzZmDr4Zn6PR-6bKDo3SWhjMEjI", "y25-k3-47-paraneoplastik-sendromlar", "Tıbbi Patoloji", 14,
     "Paraneoplastik Sendromlar", "Prof. Dr. Hikmet Keleş", []),
    ("1vIYVENB4f6ZHcM9Yr2kX9CZD2mDfZajR", "y25-k3-48-karaciger-klinik-sendromlari-1", "Tıbbi Patoloji", 15,
     "Karaciğer Hastalığının Klinik Sendromları 1: Yetmezlik, Sarılık, Kolestaz", "Prof. Dr. Hikmet Keleş", ["k3-15"]),
    ("1mzRaYTTmaEs27SkBJ9j-d-1XpXeYjOv0", "y25-k3-49-karaciger-klinik-sendromlari-2", "Tıbbi Patoloji", 16,
     "Karaciğer Hastalığının Klinik Sendromları 2: Siroz ve Portal Hipertansiyon", "Prof. Dr. Hikmet Keleş", ["k3-48"]),
    ("1m-dTQHT6mK2XgmLOI-PUQhRE7wh4r3mo", "y25-k3-50-karaciger-nodulleri-ve-neoplazileri", "Tıbbi Patoloji", 17,
     "Karaciğer Nodülleri ve Neoplazileri", "Prof. Dr. Hikmet Keleş", ["k3-49"]),
    ("14p4z_MVlF28-M5Q1revDtGHoRVmgvE-B", "y25-k3-51-kolestatik-karaciger-hastaliklari", "Tıbbi Patoloji", 18,
     "Kolestatik Karaciğer Hastalıkları", "Prof. Dr. Hikmet Keleş", ["k3-47"]),
    # ── Çocuk Sağlığı ve Hastalıkları ────────────────────────────────────────────────────────────
    ("1ITd2gStI1JA0a5cabqxwFJ9EyedrmE2G", "y25-k3-52-konjenital-gis-malformasyonlari", "Çocuk Sağlığı ve Hastalıkları", 1,
     "Konjenital Gastrointestinal Sistem Malformasyonları", "Doç. Dr. Eylem Sevinç", ["k3-32"]),
    ("1jBa9FledM2w8aRrKDhNwAopdp9hvUo9g", "y25-k3-53-biliyer-atrezi-ve-safra-yolu-anomalileri", "Çocuk Sağlığı ve Hastalıkları", 2,
     "Biliyer Atrezi ve Diğer Safra Yolu Anomalileri", "Doç. Dr. Eylem Sevinç", ["k3-51"]),
    ("1W5Mnz5IMHGmsbZGnsLGrPHaua-wJFjGS", "y25-k3-54-neonatal-kolestaz", "Çocuk Sağlığı ve Hastalıkları", 3,
     "Neonatal Kolestaz", "Doç. Dr. Eylem Sevinç", ["k3-52"]),
    # ── Enfeksiyon Hastalıkları ──────────────────────────────────────────────────────────────────
    ("1_v3Ml8YNOishAxPzUXijCvSwfvblwNVQ", "y25-k3-55-kolera", "Enfeksiyon Hastalıkları", 1,
     "Kolera", "Dr. Öğr. Üyesi Begüm Şahin", ["k3-24"]),
    ("1fPkptWJ7vOp7Xp7IfBYZlSCL2QRnAF3h", "y25-k3-56-zoonotik-enfeksiyonlar", "Enfeksiyon Hastalıkları", 2,
     "Zoonotik Enfeksiyonlar", "Dr. Öğr. Üyesi Begüm Şahin", ["k3-58"]),
    # ── Tıbbi Genetik ────────────────────────────────────────────────────────────────────────────
    ("1Jr6C8CUYR7cMg-OkdOHFNTik_2zs-b_o", "y25-k3-57-gis-hastaliklarinin-genetigi", "Tıbbi Genetik", 1,
     "Gastrointestinal Hastalıkların Genetiği", "Dr. Öğr. Üyesi Serap Arslan", ["k3-38"]),
    ("151TOgagV3mEGvwE3ny-Qh04wANcb3MCB", "y25-k3-58-gis-tumorlerinin-genetigi", "Tıbbi Genetik", 2,
     "Gastrointestinal Tümörlerin Genetiği", "Dr. Öğr. Üyesi Serap Arslan", ["k3-40"]),
]

ESLESME = DB / "kurul3_eslesme.json"
KAYNAK = DB / "kurul3_kaynak.json"
METIN = DB / "kurul3_metin.json"


def yaz() -> int:
    env = json.loads(KAYNAK.read_text(encoding="utf-8"))
    var = {d["id"]: d for d in env["dosyalar"]}
    metin = json.loads(METIN.read_text(encoding="utf-8")) if METIN.exists() else {}
    out, hata = {}, []
    for sira, (fid, key, brans, no, baslik, hoca, program) in enumerate(MAP, 1):
        d = var.get(fid)
        if not d:
            hata.append(f"{key}: dosya {fid} envanterde yok")
            continue
        m = metin.get(fid) or {}
        out[key] = {
            "file_id": fid, "dosya": d["ad"], "klasor": d["klasor"], "mime": d["mime"],
            "brans": brans, "brans_no": no, "baslik": baslik, "hoca": hoca,
            "program": program, "kurul_no": sira,
            "sayfa": int(m.get("sayfa") or 0),
            "pdf": f"pdf/kurul3/{key}.pdf",
        }
    kalan = sorted(set(var) - {f for f, *_ in MAP})
    if kalan:
        hata.append("eşleşmeyen dosyalar: " + ", ".join(var[k]["ad"] for k in kalan))
    for h in hata:
        print("HATA", h)
    if hata:
        return 1
    ESLESME.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(out)} ders eşlendi → {ESLESME}")
    return 0


def denetle() -> int:
    env = json.loads(KAYNAK.read_text(encoding="utf-8"))
    var = {d["id"] for d in env["dosyalar"]}
    eksik = [f for f, *_ in MAP if f not in var]
    cift = {f for f, *_ in MAP if [x[0] for x in MAP].count(f) > 1}
    anahtar = [k[1] for k in MAP]
    print(f"dosya {len(MAP)} · envanter {len(var)} · eşleşmeyen {len(var - {f for f, *_ in MAP})}")
    print("eksik id:", eksik)
    print("çift id:", cift)
    print("çift anahtar:", [k for k in set(anahtar) if anahtar.count(k) > 1])
    return 0 if not eksik and not cift else 1


if __name__ == "__main__":
    sys.exit({"yaz": yaz, "denetle": denetle}[(sys.argv[1] if len(sys.argv) > 1 else "denetle")]())
