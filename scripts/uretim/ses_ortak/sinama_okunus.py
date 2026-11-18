#!/usr/bin/env python3
"""Okunuş sınaması — ses_metin.hazirla girdi → beklenen okunuş (2026-11-16; SES ÜRETMEZ, GPU/LLM yok).

Her satır bir hatanın ya da korunan doğru davranışın kanıtıdır (H586/H587 güncellemesi): şık etiketi, "O" zamiri,
"de de" bağlacı, kesmeli ek, TAMAMI BÜYÜK Türkçe başlık, Roma rakamı I, küçük harfli sıradan sözcük, kutu çizimi,
kurul seçimi (Öğren destesi, k1-67…, y25-k2-…, k2p-…, klasör adları). 0 HATA → çıkış 0.
Kullanım: python3 scripts/uretim/ses_ortak/sinama_okunus.py [-v]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ses_metin as S  # noqa: E402

# (girdi, yol, beklenen okunuş)
OKUNUS = [
    # şık etiketi ve zamir harf adıyla okunmaz
    ("A, Williams sendromu.", "uzun", "A, Vilyıms sendromu."),
    ("B) Down sendromu", "uzun", "B) Davn sendromu"),
    ("C. Purinler", "uzun", "C. Purinler"),
    ("Doğru cevap E, doğum kanalı.", "uzun", "Doğru cevap E, doğum kanalı."),
    ("O zaman bu böyle olur.", "uzun", "O zaman bu böyle olur."),
    ("O da bu en ve de.", "uzun", "O da bu en ve de."),
    # tek harf anlamlı yerde harf adıyla
    ("X kromozomu ve hepatit A.", "uzun", "iks kromozomu ve hepatit aa."),
    ("E vitamini desteği.", "uzun", "ee vitamini desteği."),
    ("T hücre aracılı yanıt.", "uzun", "tee hücre aracılı yanıt."),
    ("Streptolizin O ise streptokoktan.", "uzun", "Streptolizin O ise streptokoktan."),
    # bağlaç dizisi ve kesmeli ek kısaltma sayılmaz
    ("LGV'de de görülür.", "uzun", "lee gee vee de de görülür."),
    ("Bubo de de görülür.", "uzun", "Bubo de de görülür."),
    ("HIV'in yapısı.", "uzun", "haa ıı vee in yapısı."),
    ("Onkogen değil, de ne a hasarı.", "uzun", "Onkogen değil, dee nee aa hasarı."),
    ("ha pe ve ilişkili lezyon.", "uzun", "haa pee vee ilişkili lezyon."),
    # büyük harfli Türkçe başlık harf harf okunmaz; bilinen kısaltma okunur
    ("[SINAV SPOTU] Dekortike M3.", "uzun", "[sınav spotu] Dekortike mee üç."),
    ("TOPUK KANI İLE YAPILAN TESTLER: 3 ila 5 gün.", "uzun", "topuk kanı ile yapılan testler: üç ila beş gün."),
    ("DİKKAT: HIV ELISA ile.", "uzun", "dikkat: haa ıı vee eliza ile."),
    ("BOS dansitesinde.", "uzun", "bos dansitesinde."),
    ("MSS ilaçları.", "uzun", "mee see see ilaçları."),
    ("IL-6 ve BRCA1, NMDA.", "uzun", "interlökin altı ve bercea bir, nee mee dee aa."),
    # Roma rakamı
    ("Cevap: I ve III.", "uzun", "Cevap: bir ve üç."),
    ("II ve IV birleşimi.", "uzun", "iki ve dört birleşimi."),
    # küçük harfli sıradan sözcük eponim/yabancı okunuş almaz; büyük harfli eponim alır
    ("sperm hücresi engel olur, Engel sendromu", "uzun", "sperm hücresi engel olur, Engıl sendromu"),
    ("Dede ile yürüdük, dedemiz geldi.", "uzun", "Dede ile yürüdük, dedemiz geldi."),
    ("Bu checkpoint sayfası", "uzun", "Bu çekpoint sayfası"),
    ("İn vivo deney.", "uzun", "İn vivo deney."),
    ("Bu checkpointte salgın, Checkpoint inhibitörü.", "uzun", "Bu çekpointte salgın, Çekpoint inhibitörü."),
    ("CHECKPOINT KONTROLÜ yapılır.", "uzun", "çekpoint kontrolü yapılır."),
    ("nedeni 'sperm seleksiyonu'dur.", "uzun", "nedeni 'sperm seleksiyonu'dur."),
    ("Strike dip için DDD gösterimidir.", "uzun", "Strike dip için dee dee dee gösterimidir."),
    ("Escherichia coli enterik çomaktır.", "uzun", "Eşerişya koli enterik çomaktır."),
    ("Alzheimer ve Huntington hastalığı.", "uzun", "Alzhaymır ve Hantingtın hastalığı."),
    # kutu çizimi (H587) temizlenir
    ("┌──┐ │ TÜMÖR │ └──┘ metin", "uzun", "tümör, metin"),
    ("│ └────┴────┘.", "uzun", "."),
    # bitişik yol (Kurul 1) kutu temizliği ve şık etiketi
    ("┌──┐ │ Benign │ └──┘", "bitisik", "Benign"),
    # 2026-11-17 (tumor-biyolojisi 18/24/32): ok ve geometrik şekil (▼◄►), yalnız çizimden oluşan parça, "<%0.1'dir"
    ("│ (Simetrik 2 Kutup) │ └──┬──┘ ▼ ▼ ◄──► (2 Kutup) ▼", "uzun", "(Simetrik iki Kutup), (iki Kutup)"),
    ("│ └─────┴─────┘.", "bitisik", "."),
    ("Leyomiyomun sarkoma dönüşüm riski <%0.1'dir.", "uzun", "Leyomiyomun sarkoma dönüşüm riski yüzde sıfır virgül bir den küçüktür."),
    ("uzak metastaz sıklığı <%0.01'dir (SIFIRDIR)", "uzun", "uzak metastaz sıklığı yüzde sıfır virgül sıfır bir den küçüktür (sıfırdır)"),
    ("olasılık yüksektir (>%50).", "uzun", "olasılık yüksektir (yüzde elli den büyük)."),
    # 2026-11-17: yüzdesiz karşılaştırma (birimli/birimsiz); önü harfli "<" (p<0.05) dokunulmaz
    ("Çap < 5 mm ise", "uzun", "Çap beş mm'den küçük ise"),
    ("> 2 cm tümör", "uzun", "iki cm'den büyük tümör"),
    ("değer ≥0.5 olur", "uzun", "değer sıfır virgül beş ten büyük ya da eşit olur"),
    ("≥ %10 olur", "uzun", "yüzde on dan büyük ya da eşit olur"),
    ("p<0.05 anlamlı", "uzun", "p<0.05 anlamlı"),
    ("A, Williams sendromu.", "bitisik", "A, Vilyıms sendromu."),
]

# (anahtar, tür, beklenen kurul)
KURUL = [
    ("learn-tromboz-patofizyolojisi-tam", "ders", 1),
    ("learn-tumor-biyolojisi-terminolojisi", "ders", 1),
    ("deck-urinary-obstruction", "ders", 1),
    ("k1-67-gebelik-hastaliklari", "ders", 1),
    ("k1-69-mikroorganizmalarda-direnc-sorunu", "ders", 1),
    ("k1-09-x", "ders", 1),
    ("k2-09-sss-ilaclari", "ders", 2),
    ("k2p-k2-01-norolojik-hastaya-yaklasim", "ders", 2),
    ("k1p-k1-11-ornek", "ders", 1),
    ("y25-k2-09-arsiv", "ders", 2),
    ("k3-kamp", "ders", 3),
    ("k2noroloji_cozucu", "modul", 2),
    ("patoloji_cozucu", "modul", 1),
    ("patoloji_cozucu_alt", "modul", 1),
    ("k2dersanaliz_cozucu", "modul", 2),
    ("kmb_cozucu", "modul", 1),
    ("yuruyus-kampcilik", "modul", 2),
]


# (çok satırlı girdi, beklenen) — ses_metin.kutu_tablo_duz: hücreler sütun sütun birleşir, çerçeve satırı parça üretmez
TABLO = [
    ("┌──────┬──────┐\n│ A1   │ B1   │\n│ A2   │ B2   │\n├──────┼──────┤\n│ C    │ D    │\n└──────┴──────┘", "A1 A2, B1 B2. C, D."),
    ("metin\n```\n┌──┐   ┌──┐\n│ X│   │ Y│\n└┬─┘   └┬─┘\n ▼      ▼\nsol    sağ\n```\nson", "metin\n```\nX, Y. sol, sağ.\n```\nson"),
    ("düz metin", "düz metin"),
]


def main() -> int:
    v = "-v" in sys.argv
    hata = 0
    for girdi, yol, bek in OKUNUS:
        al = S.hazirla(girdi, yol=yol)
        if al != bek:
            hata += 1
            print(f"HATA  [{yol}] {girdi!r}\n      beklenen: {bek!r}\n      alınan  : {al!r}")
        elif v:
            print(f"ok    [{yol}] {girdi!r} → {al!r}")
    for anahtar, tur, bek in KURUL:
        al = S.ders_kurulu(anahtar) if tur == "ders" else S.modul_kurulu(anahtar)
        if al != bek:
            hata += 1
            print(f"HATA  kurul {tur} {anahtar}: beklenen {bek}, alınan {al}")
        elif v:
            print(f"ok    kurul {tur} {anahtar} → {al}")
    for girdi, bek in TABLO:
        al = S.kutu_tablo_duz(girdi)
        if al != bek:
            hata += 1
            print(f"HATA  tablo {girdi!r}\n      beklenen: {bek!r}\n      alınan  : {al!r}")
    n = len(OKUNUS) + len(KURUL) + len(TABLO)
    print(f"{n} sınama, {hata} HATA (sözlük {S.SOZLUK_SURUM})")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
