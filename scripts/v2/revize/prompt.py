"""Revize v2 — AI promptu (INSTRUCTIONS.md §3 ile birebir)."""
from __future__ import annotations

TEMPLATE = """Sen bir tıp fakültesi sınav sorusu editörüsün. Aşağıdaki soruyu, SADECE verilen ders notu \
kanıtlarına ve müfredat kazanımına dayanarak düzelt ve tamamla. Dışarıdan bilgi uydurma.

KURALLAR:
1) Soru kökü yoksa şıklardan/metinden uygun bir kök oluştur. Kök tıbbi olarak doğru ve net olsun.
2) Soru kökünün YÖNÜNÜ koru (olumlu/olumsuz; "yanlıştır/değildir/hariç" aynen kalsın). Değiştirme.
3) 4 veya 5 şık üret (A..E). Her şık soruyla ilişkili, kısa ve net olsun. Gereksiz uzun şık yazma.
4) Tüm şıklar doğru veya tüm şıklar yanlış olmasın.
5) Doğru şıkkı kanıta dayanarak seç; kanıt yoksa "dogru_secenek": null ve "belirsiz": true bırak.
6) Öncüllü soruysa öncülleri ayrı listele; şıklar öncülleri harf/sayı ile temsil etsin (ör. "Yalnız I").
7) OCR hatalarını, soru no/öğrenci/slayt/ders adı gibi gürültüleri temizle. Soru formatını bozma.
8) Açıklama kısa, tıbbi olarak doğru ve KANITA DAYALI olsun; ama kaynağa/ders notuna ATIF YAPMA.
11) YASAK: açıklamada veya kökte "kaynakta", "slaytta", "ders notunda", "kanıtta", "kanıt", "alıntı",
    "[Kaynak: ...]", "metinde" gibi ATIF/META ifadeler KULLANMA. Bunlar ayrı alanda (kullanilan_kaynaklar) tutulur.
12) YASAK: "yanlış ifade olarak", "doğru ifade olarak", "soru ... demektedir", "belirtilmektedir ki" gibi
    DOLAYLI/ANLATICI üslup. Açıklama, sınav çözümü gibi DOĞRUDAN klinik gerekçe yazsın.
13) Soru kökü SINAV FORMATINI korusun ("... hangisidir?", "... değildir?" vb.). Kök, açıklama/anlatı
    cümlesine dönüşmesin. Tıbbi literatüre ve müfredat kazanımına uygun, ölçülü ve net olsun.
14) aciklama_maddeleri: 3-6 madde; her madde tek bir klinik/tıbbi gerekçe. Doğru şıkkın nedenini ve
    gerektiğinde çeldiricilerin neden yanlış olduğunu belirt (ör. "A seçeneği aort stenozuna aittir").
    Sınav çözümü üslubu; kaynağa/ders notuna ATIF YOK; tıbbi literatüre uygun.

ÖRNEK AÇIKLAMA (bu üslubu kullan):
• Norplant, yavaş salınımlı levonorgestrel salgılayan klasik bir subdermal implant sistemidir.
• Levonorgestrel endometriyumu gebeliğe elverişsiz hale getirir, servikal mukusu kalınlaştırır ve ovulasyonu baskılar.
• C seçeneği beta-laktam hücre duvarına etki eder; bu soru protein sentezi ile ilgili olduğundan yanlıştır.
9) Soru gerçekten soru değilse (ders notu/başlık/şık yığını) ve kurtarılamıyorsa soru_degil=true ver.
10) Kanıt yetersizse zorla düzeltme; karantina=true ve neden yaz.

SORU (mevcut sürüm):
{kok}
ŞIKLAR: {secenekler}
İŞARETLİ CEVAP: {dogru}

MÜFREDAT: Ders={ders} | Kurul={kurul} | Konu={konu} | Kazanım={kazanim}

DERS NOTU KANITLARI (yalnız bunlara dayan):
{kanit}

YALNIZCA şu JSON'u döndür:
{{"soru_degil": false, "karantina": false, "neden": "", "soru_koku": "...", "oncul": [], \
"secenekler": {{"A":"...","B":"...","C":"...","D":"...","E":"..."}}, "dogru_secenek": "A", \
"belirsiz": false, "aciklama": "...", "aciklama_maddeleri": [], "kullanilan_kaynaklar": [], \
"ders_adi": "...", "kurul_adi": "...", "konu_adi": "...", "kazanim": "...", \
"degisiklikler": [{{"alan":"soru_koku","eski":"...","yeni":"...","neden":"..."}}]}}
"""


def build(question: dict, tax: dict, evidence: list[dict]) -> str:
    opts = question.get("secenekler") or {}
    opts_txt = ", ".join(f"{k}) {v}" for k, v in sorted(opts.items())) or "(şıklar yok)"
    kanit = "\n".join(
        f"[kaynak: {e.get('chunk_id')} | s.{e.get('sayfa')}] {e.get('text','')[:800]}"
        for e in evidence
    ) or "(kanıt bulunamadı)"
    return TEMPLATE.format(
        kok=question.get("soru_koku") or "(soru kökü yok)",
        secenekler=opts_txt,
        dogru=question.get("dogru_secenek") or "?",
        ders=tax.get("ders") or question.get("ders_adi") or "?",
        kurul=tax.get("kurul") or question.get("kurul_adi") or "?",
        konu=tax.get("konu") or "?",
        kazanim=tax.get("kazanim") or "?",
        kanit=kanit,
    )
