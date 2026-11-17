"""Şık açıklama kalite kapısı — meds/docs/SIK_ACIKLAMA_STANDARDI.md (kullanıcı kararı 2026-10-18).

Her şık açıklaması (Yardım al / yanlış şık / çözücü siklar) şıktaki kavramın NE olduğunu, NE İŞE YARADIĞINI ve bu soruyla
bağını anlatmalı; "bu sorunun cevabı değil", "… olarak geçmez" gibi yalnız olumsuzlayan geçiştirme cümleleri HATA'dır.
Kullanım: from sik_aciklama import denetle; e.extend(denetle(metin, yer, enaz=20, encok=55, cumle=(2, 3)))
"""
import re

kelime = lambda s: len(re.findall(r'\w+', s))

# tek başına öğretmeyen kalıplar (şıkkın kimliği/işlevi verilmeden kullanılamaz)
BOS_KALIP = re.compile(
    r"(bu )?sorunun (cevab[ıi]|yan[ıi]t[ıi]) değil|\bcevap değil|olarak geçmez|arasında (yer almaz|geçmez|sayılmaz)"
    r"|ile ilişkilendirilmez|bu soruyla ilgisi yok"
    r"|soruda aranan (yan[ıi]t|cevap)|aranan yan[ıi]t (ise|değil|bu)|listesinde yer almaz"
    r"|seçilecek (ifade|seçenek|şık) bu değil|kökte tarif edilen duruma uyan|dışarıda kalan seçenek ise"
    r"|doğru karşılık ise “[^”]*” seçeneğidir|bu yüzden doğru seçenek budur", re.I)  # H496 + H511 + H619 (kalıp yer değiştirme; ölçüm: yalnız k2-16'da, başka ders 0)
OLUMSUZ = re.compile(r"\b(değil\w*|yapmaz|geçmez|almaz|yoktur|olmaz|etmez|sağlamaz|toplamaz|görülmez|bulunmaz|sayılmaz)\b", re.I)


# Kısaltma noktası cümle sonu değildir: kaynak etiketi "(s. 9 ve 12)" her açıklamada fazladan cümle sayılıyordu
# (2026-11-17 ölçümü: 11.465 şıkın 6.901'inde fazla sayım, 48'i yalnız bu yüzden "2–3 cümle" kuralından kalıyordu — H618).
# Eşik değişmedi (2–3 cümle); yalnız sayım düzeltildi.
_KISALTMA = re.compile(r'\b(s|sf|bkz|vb|vs|Dr|Prof|örn|yak|Tab|Şek|md|mad|no|bk|Doç|Uzm)\.(?=\s)')


def cumleler(m):
    m = _KISALTMA.sub(lambda x: x.group(1) + '\u2024', m.replace('**', '').strip())
    return [c.replace('\u2024', '.') for c in re.split(r'(?<=[.!?])\s+', m) if c.strip()]


def denetle(metin, yer, enaz=20, encok=55, cumle=(2, 3)):
    """Hata listesi döndürür (boşsa geçer)."""
    e = []
    m = (metin or '').strip()
    if not m: return [f'{yer}: şık açıklaması boş']
    k = kelime(m.replace('**', ''))
    if k < enaz: e.append(f'{yer}: şık açıklaması {k} kelime — en az {enaz} (ne olduğu + ne işe yaradığı + bu soruyla bağı)')
    if k > encok: e.append(f'{yer}: şık açıklaması {k} kelime — en çok {encok}')
    C = cumleler(m)
    if not cumle[0] <= len(C) <= cumle[1]: e.append(f'{yer}: {len(C)} cümle ({cumle[0]}–{cumle[1]})')
    g = BOS_KALIP.search(m)
    if g: e.append(f'{yer}: geçiştirici kalıp {g.group()!r} — kavramın ne olduğunu ve ne yaptığını anlat')
    if C and all(OLUMSUZ.search(c) for c in C):
        e.append(f'{yer}: yalnız olumsuz cümleler — en az bir cümle kavramın kimliğini/işlevini olumlu söylemeli')
    return e
