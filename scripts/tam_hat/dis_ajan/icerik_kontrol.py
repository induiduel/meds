#!/usr/bin/env python3
"""Anlatım dışı içerik kapısı: örnek soru / sesli çözücü / Öğren destesi (dış ajan protokolü §12). LLM yok.

  python3 scripts/tam_hat/dis_ajan/icerik_kontrol.py <ornek|cozucu|deste> <icerik.json> <iddia.json> <kanit.json> <sayfalar.json>

İçerik, deponun KENDİ biçiminde yazılır (soru dosyası / çözücü dosyası / deste); proje kapıları (sik_aciklama, soru_uslup, cozucu_dogrula,
validate_learning_decks) ayrıca çalışır. Bu kapı İÇERİĞİ KANITA BAĞLAR:
  iddia.json: [{"id","eleman":"<soru/etkileşim kimliği>","metin":"içerikteki cümle AYNEN","kanit":["k1"]}]
  1) kanıt dosyası kanit_dogrula'dan, iddialar kanit_tutarlilik --iddia'dan geçer;
  2) her iddia metni gerçek içerikte AYNEN geçer (kanıt zinciri süs olamaz);
  3) içeriğin doğrulanması gereken her cümlesi (ornek: soru kökü + doğru şık + her şık açıklaması + açıklama; cozucu: soru kökü + her şık
     açıklaması; deste: anlatım cümleleri + her etkileşimin açıklama/cümle metni) bir iddiayla karşılanır;
  4) iddia `eleman`'ı içerikteki gerçek öğe kimliğidir ve her öğenin ≥1 iddiası vardır.
Çıkış 0 = HATA yok.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
from ortak import norm, yukle  # noqa: E402


def md_temizle(t: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[*_`>#]|^\s*[-•]\s+", "", str(t), flags=re.M)).strip()


def cumleler(t: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<=[.!?])\s+|\n+", md_temizle(t)) if len(c.strip()) >= 25]


def hedefler(tur: str, d: dict) -> dict:
    """{eleman_id: [dogrulanmasi gereken metinler]}"""
    out: dict[str, list[str]] = {}
    if tur == "ornek":
        for k in d.get("kazanimlar", []):
            for q in k.get("sorular", []):
                t = [q.get("soru", ""), (q.get("secenekler") or {}).get(q.get("dogru"), ""), q.get("aciklama", "")]
                t += list((q.get("sik_aciklamalari") or {}).values())
                out[q["id"]] = [x for x in t if x]
    elif tur == "cozucu":
        for q in d.get("sorular", []):
            t = [q.get("soru", "")] + list((q.get("siklar") or {}).values())
            out[f"no{q.get('no')}"] = [x for x in t if x]
    elif tur == "deste":
        dk = d if "slides" in d else (d.get("decks") or [d])[0]
        for sl in dk.get("slides", []):
            sn = sl.get("slideNumber")
            ts = cumleler(sl.get("synthesisNarrative", "") or sl.get("content", ""))
            out[f"s{sn}"] = ts
            for i, el in enumerate(sl.get("interactiveElements") or []):
                t = []
                for key in ("question", "explanation", "sentence", "maskedTerm"):
                    if isinstance(el.get(key), str):
                        t.append(el[key])
                for o in el.get("microQuizOptions") or []:
                    if isinstance(o, dict) and o.get("explanation"):
                        t.append(o["explanation"])
                out[f"s{sn}.e{i}"] = [x for x in t if len(str(x)) >= 12]
    return out


def main() -> int:
    if len(sys.argv) != 6 or sys.argv[1] not in ("ornek", "cozucu", "deste"):
        print(__doc__)
        return 2
    tur, icerik_y, iddia_y, kanit_y, sayfa_y = sys.argv[1], *sys.argv[2:]
    kod = 0
    for ad, args in (("KANIT", ["kanit_dogrula.py", kanit_y, sayfa_y]), ("İDDİA", ["kanit_tutarlilik.py", iddia_y, kanit_y, "--iddia"])):
        print(f"--- {ad} ---")
        r = subprocess.run([sys.executable, "-I", str(D / args[0]), *args[1:]], capture_output=True, text=True)
        print(r.stdout.rstrip())
        kod |= r.returncode
    icerik, iddia = yukle(Path(icerik_y)), yukle(Path(iddia_y))
    hata: list[str] = []
    tum = norm(md_temizle(json.dumps(icerik, ensure_ascii=False)))
    tum_ham = norm(md_temizle(" ".join(re.findall(r'"((?:[^"\\]|\\.)*)"', json.dumps(icerik, ensure_ascii=False)))))
    print("--- BAĞ (iddia ↔ gerçek içerik) ---")
    claim_norm = {}
    for c in iddia:
        cid, m = c.get("id"), norm(md_temizle(c.get("metin", "")))
        claim_norm[cid] = (c.get("eleman"), m)
        if m not in tum_ham and m not in tum:
            hata.append(f"[BAG-01] {cid}: iddia metni içerikte AYNEN yok. Yapılacak: iddiayı içerikten kopyala (ya da içeriği iddiaya göre düzelt); kanıt zinciri içerikle birebir olmalı.")
    hd = hedefler(tur, icerik)
    if not hd:
        hata.append(f"[BAG-02] içerikte öğe bulunamadı (tür={tur}). Yapılacak: deponun biçimini kullan (ornek: kazanimlar[].sorular[]; cozucu: sorular[]; deste: slides[].interactiveElements[]).")
    elemanlar = {e for e, _ in claim_norm.values()}
    for e in hd:
        if e not in elemanlar:
            hata.append(f"[BAG-03] {e}: hiçbir iddia bu öğeyi kanıtlamıyor. Yapılacak: bu öğenin cümleleri için kanıtlı iddia ekle.")
    for e in sorted(elemanlar - set(hd) - {None}):
        hata.append(f"[BAG-04] iddia 'eleman' = {e} içerikte yok. Yapılacak: gerçek öğe kimliğini yaz ({', '.join(list(hd)[:3])}…).")
    tum_claims = " | ".join(m for _, m in claim_norm.values())
    for e, metinler in hd.items():
        for t in metinler:
            nt = norm(md_temizle(t))
            if nt and nt not in tum_claims and not any(m and m in nt for _, m in claim_norm.values() if len(m) > 20):
                hata.append(f"[BAG-05] {e}: «{t[:80]}…» hiçbir iddia ile karşılanmıyor. Yapılacak: bu cümle için kanıtlı iddia ekle ya da cümleyi içerikten çıkar.")
    # Örnek soru: muhakeme, çıkmış-benzeri kök, sızıntı, sayfa yayılımı ve (varsa) ders profili (kazanım haritası)
    uyari: list[str] = []
    if tur == "ornek":
        kn = {k.get("id"): k for k in yukle(Path(kanit_y))}
        per: dict[str, set] = {}
        for c in iddia:
            per.setdefault(c.get("eleman"), set()).update(c.get("kanit") or [])
        sorular = [q for k in icerik.get("kazanimlar", []) for q in k.get("sorular", [])]
        from ortak import kokler
        ezber = 0
        sayfalar_kul: set = set()
        for q in sorular:
            kid = q.get("id")
            ids = per.get(kid, set())
            sayfalar_kul |= {kn[i].get("s") for i in ids if i in kn}
            gerek = 3 if q.get("zorluk") in ("zor", 3, "3") else 2
            if len(ids) < gerek:
                hata.append(f"[SORU-01] {kid}: soru {len(ids)} ayrı kanıta dayanıyor, {gerek} gerekli. Yapılacak: soru en az {gerek} AYRI bilgiyi birleştirip muhakeme istesin (ör. mekanizma + sonuç, iki komşu kavramın ayrımı, bulgu + tanı); tek cümlelik ezber sorusu yazma.")
            kok = str(q.get("soru", ""))
            if len(kok.split()) < 14 and re.search(r"(hangisidir|hangi (gen|protein|yapı|hastalık|sendrom)\w*|nedir|nelerdir)\s*\??\s*$", kok.lower()):
                ezber += 1
            dog = (q.get("secenekler") or {}).get(q.get("dogru"), "")
            # SORU-06: cevap ile soru kökü aynı kanıtta birlikte geçmeli; geçmiyorsa soru kaynağın söylemediği bir ilişkiyi (çıkarımı) sorar
            if len(dog.split()) <= 8:
                dr, sr = kokler(dog) - kokler(kok), kokler(kok)
                diger = set()
                for h_, t_ in (q.get("secenekler") or {}).items():
                    if h_ != q.get("dogru"):
                        diger |= kokler(t_)
                sr -= diger  # tüm şıklarda ortak/genel sözcükler kökün ayırt edici kısmı değildir
                if dr and not q.get("cikarim_gerekce"):
                    esle = any(len(dr & kokler(str(kn[i].get("alinti", "")))) >= 0.6 * len(dr) and len(sr & kokler(str(kn[i].get("alinti", "")))) >= min(2, len(sr)) for i in ids if i in kn)
                    if not esle:
                        hata.append(f"[SORU-06] {kid}: doğru şıkla soru kökündeki ayırt edici sözcükler HİÇBİR tek kanıtta birlikte geçmiyor; soru kaynağın açıkça söylemediği bir ilişkiyi soruyor olabilir. Yapılacak: ilişkiyi söyleyen alıntıyı kanıta ekle ve bağla; kaynakta böyle bir cümle yoksa soruyu değiştir.")
            dk = {w for w in kokler(dog)}
            if dk and dk <= kokler(kok) and len(dk) >= 1 and len(dog.split()) <= 4:
                hata.append(f"[SORU-04] {kid}: doğru şıkkın sözcükleri soru kökünde zaten geçiyor (cevap sızıyor). Yapılacak: kökü cevabı ele vermeyecek biçimde yeniden kur.")
        if sorular and ezber / len(sorular) > 0.25:
            hata.append(f"[SORU-02] soruların {ezber}/{len(sorular)} kadarı kısa «hangisidir / hangi gen» ezber kökü (en çok %25). Yapılacak: vaka, bulgu→mekanizma, iki kavramı ayırt etme ya da «şunların hangisi yanlıştır» gibi muhakeme kökleri yaz.")
        sayfa_say = {k.get("s") for k in kn.values()}
        if len(sorular) >= 6 and len(sayfa_say) >= 3 and len(sayfalar_kul) < max(2, len(sayfa_say) // 2):
            hata.append(f"[SORU-05] sorular yalnız {len(sayfalar_kul)} sayfaya yaslanıyor (kanıt {len(sayfa_say)} sayfada). Yapılacak: önemli bilgileri taşıyan diğer sayfalardan da soru yaz.")
        prof = Path(icerik_y).parent / "profil"
        harita_y = prof / "kazanim_haritasi.json"
        if harita_y.exists():
            harita = yukle(harita_y)
            hid = {h.get("id"): h for h in harita}
            kullanilan: dict[str, int] = {}
            for q in sorular:
                kz = q.get("kazanim_id")
                if kz not in hid:
                    hata.append(f"[PROFIL-01] {q.get('id')}: kazanim_id='{kz}' kazanım haritasında yok. Yapılacak: her soruya haritadaki gerçek kazanım kimliğini yaz ({', '.join(list(hid)[:4])}…).")
                else:
                    kullanilan[kz] = kullanilan.get(kz, 0) + 1
            for h in harita:
                gerek = 2 if (h.get("onem") == "yuksek" and h.get("hoca_vurgu")) else (1 if h.get("onem") == "yuksek" else 0)
                if kullanilan.get(h.get("id"), 0) < gerek:
                    hata.append(f"[PROFIL-02] kazanım {h.get('id')} («{str(h.get('kazanim'))[:50]}»): önem={h.get('onem')}, hoca_vurgu={bool(h.get('hoca_vurgu'))}; en az {gerek} soru gerekli, {kullanilan.get(h.get('id'), 0)} var. Yapılacak: bu kazanımı sorgulayan soru ekle.")
        else:
            uyari.append("[PROFIL-00] profil/kazanim_haritasi.json yok: soru seçimi yalnız slayt vurgusuna göre yapıldı. Kullanıcı hoca üslubu ve kazanım haritası verince profil/ klasörüne konur ve kapı onu zorlar.")
    # Deste: açıklama önermeyi/cümleyi tekrarlamamalı, yeni bilgi (gerekçe, ilişki, ayrım) taşımalı
    if tur == "deste":
        from ortak import kokler
        dk = icerik if "slides" in icerik else (icerik.get("decks") or [icerik])[0]
        for sl in dk.get("slides", []):
            for i, el in enumerate(sl.get("interactiveElements") or []):
                for pr in (el.get("items") or el.get("statements") or []):
                    if isinstance(pr, dict) and pr.get("text") and pr.get("explanation"):
                        yeni = kokler(pr["explanation"]) - kokler(pr["text"]) - {"dogru", "tuzak", "yanli"}
                        if len(yeni) < 2:
                            hata.append(f"[DESTE-01] s{sl.get('slideNumber')}.e{i}: açıklama önermeyi tekrarlıyor, yeni bilgi yok («{pr['text'][:60]}…»). Yapılacak: açıklamaya kaynaktaki gerekçeyi/ilişkiyi/ayrımı ekle (yalnız kanıtlı bilgi); olmuyorsa önermeyi değiştir.")
    # Proje kapıları: şık açıklaması standardı (kural 14) ve çözücü ipucu sızıntısı
    if tur in ("ornek", "cozucu"):
        sys.path.insert(0, str(D.parents[1]))
        try:
            import sik_aciklama as SA
        except Exception as e:  # noqa: BLE001
            SA = None
            hata.append(f"[PROJE-00] sik_aciklama.py yüklenemedi: {e}")
        sorular = [q for k in icerik.get("kazanimlar", []) for q in k.get("sorular", [])] if tur == "ornek" else icerik.get("sorular", [])
        for q in sorular:
            kim = q.get("id") or f"no{q.get('no')}"
            siklar = q.get("sik_aciklamalari") if tur == "ornek" else q.get("siklar")
            for harf, txt in (siklar or {}).items():
                if SA:
                    for e in SA.denetle(str(txt), f"{kim}.{harf}", enaz=20, encok=55, cumle=(2, 3)):
                        hata.append(f"[SIK] {e}. Yapılacak: kavram NE / NE İŞE YARAR / bu soruda neden doğru-yanlış (2–3 cümle); «cevabı değil» türü geçiştirme yok.")
            ops = q.get("secenekler") or {}
            gond = [h for h, t in ops.items() if re.search(r"(kaynakta|kaynağa|slayt|derste|metinde|belirtilmez|bahsedilmez|söz edilmez|hocan)", str(t).lower())]
            if gond:
                hata.append(f"[SORU-07] {kim}: {gond} şıkkında kaynak/slayt göndermesi ya da «belirtilmez» kalıbı var. Yapılacak: şık bir tıbbi iddia olsun (öğretilmiş komşu kavramdan çeldirici); kaynağa gönderme ve «hiçbir fark yok/belirtilmez» tipi dolgu şık yazma.")
            mut = [h for h, t in ops.items() if h != q.get("dogru") and re.search(r"\b(yalnız\w*|sadece|hiçbir\w*|her zaman|daima|tüm\w*|hepsi)\b", str(t).lower())]
            if len(mut) > 1:
                hata.append(f"[SORU-08] {kim}: {len(mut)} çeldirici mutlaklaştırılmış («yalnız/hiçbir/hepsi»). Yapılacak: en çok 1; diğer çeldiricileri öğretilmiş komşu kavramla kur (hoca üslubu: kopya+çevirme tek şıkta, geri kalan komşu kavram).")
            if len(re.findall(r"doğru seçenek budur|yanlış(tır| seçenek)", " ".join(map(str, (q.get("siklar") or q.get("sik_aciklamalari") or {}).values())).lower())) >= 4:
                hata.append(f"[SORU-09] {kim}: şık açıklamaları kalıp cümleyle bitiyor («… yanlıştır», «Doğru seçenek budur»). Yapılacak: her şıkta kavramı ve bu soruda neden doğru/yanlış olduğunu mekanizmayla anlat; kapanış kalıbı yazma.")
            if tur == "cozucu" and q.get("ipucu"):
                from ortak import kokler
                dog = (q.get("secenekler") or {}).get(q.get("dogru"), "")
                ortak_k = kokler(q["ipucu"]) & kokler(dog)
                if ortak_k:
                    hata.append(f"[IPUCU] {kim}: ipucu doğru şıkkın sözcük köklerini içeriyor {sorted(ortak_k)}. Yapılacak: ipucu cevabı ele vermeden mantığı hatırlatsın.")
    for u in (uyari if tur == "ornek" else []):
        print("UYARI", u)
    for h in hata:
        print("HATA", h)
    print(f"{'BAŞARISIZ' if hata or kod else 'GEÇTİ'}: {len(hd)} öğe, {len(iddia)} iddia, {len(hata)} bağ hatası")
    return 1 if hata or kod else 0


if __name__ == "__main__":
    sys.exit(main())
