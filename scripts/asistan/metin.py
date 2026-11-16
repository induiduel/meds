"""Tıp Asistanı metin normalleştirme (bağımlılık yok). İndeks ve sorgu AYNI işlevi kullanmak zorundadır."""
import re, unicodedata
_FOLD = str.maketrans("çğıöşüâîûÇĞİÖŞÜ", "cgiosuaiucgiosu")
_SOZ = re.compile(r"[a-z0-9]+")


def fold(s: str) -> str:
    s = (s or "").replace("İ", "i").replace("I", "ı").lower().translate(_FOLD)
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip()


def kokler(f: str) -> str:
    """Katlanmış metin → tam sözcük + (5 harften uzunsa) 5 harfli kök; ek farklarını yakalar."""
    out = []
    for w in _SOZ.findall(f):
        out.append(w)
        if len(w) > 5:
            out.append(w[:5])
    return " ".join(out)


# Soru kalıbı sözcükleri: sözcüksel aramada gürültü (indekse girer, sorguda atılır). Niyet sözcükleri F2'de ayrıca okunur.
DUR = set("""nedir ne neler nelerdir hangi hangisi hangileri nasil nerede nereye nereden kim kimdir mi mu midir var yok icin ile ve veya
bir bu su o da de ki gibi daha cok en hakkinda ilgili bana goster ver anlat soyle bul git ac gruptan grubundan sinifindan olarak olan olur olursa""".split())


def sorgu(s: str):
    f = fold(s)
    kalan = " ".join(w for w in f.split() if w not in DUR) or f
    return f, kokler(kalan)
