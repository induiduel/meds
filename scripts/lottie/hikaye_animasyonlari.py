#!/usr/bin/env python3
"""Mola penceresi için hikâye anlatan, karakterli Lottie animasyonları (kod ile elle tasarım).
Çıktı: src/assets/lottie/{zirve,calisma,sevgi,gunes}.json — 160×160, 60 fps, 5 sn döngü.
Yeniden üretim: python3 scripts/lottie/hikaye_animasyonlari.py

Akıcılık: her hareket yumuşak giriş-çıkışlı (ease-in-out), sıçramalar yay çizer, inişte ezilip uzama (squash & stretch),
karakterler göz kırpar, ağızlar biçim değiştirir (somurtma → gülümseme); döngü başı ile sonu aynı durumda birleşir.
  zirve   : sevimli top karakter basamakları zıplayarak çıkar, zirvede sevinçle zıplar, bayrak dalgalanır, yıldızlar saçılır
  calisma : gözlüklü kitap okur, sayfalar akar, üstteki ampul uyanır, "aha!" diye gülümser ve parıldar
  sevgi   : iki utangaç kalp yarısı birbirine kayar, birleşir, kalp pazılarını şişirip güç gösterir, sevgi halkaları yayılır
  gunes   : ağlayan bulutun arkasından güneş göz kırparak çıkar, bulutu iter, güneş gözlüğü takar; bulut gülümser, gökkuşağı
"""
import json, math
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "src/assets/lottie"
W = H = 160
FR = 60
OP = 300

# ---------------------------------------------------------------- yardımcılar
IO = ({"x": [0.42], "y": [0]}, {"x": [0.58], "y": [1]})      # yumuşak giriş-çıkış
OUTE = ({"x": [0.2], "y": [0]}, {"x": [0.3], "y": [1]})      # hızlı başla, yumuşak dur

def A(keys, e=IO):
    """keys: [(kare, değer)] → animasyonlu özellik; değer sayı ya da liste."""
    k = []
    for i, (t, v) in enumerate(keys):
        d = {"t": t, "s": v if isinstance(v, list) else [v]}
        if i < len(keys) - 1:
            d["o"], d["i"] = e[0], e[1]
        k.append(d)
    return {"a": 1, "k": k}
def S(v): return {"a": 0, "k": v}
def col(h):
    h = h.lstrip("#"); return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)] + [1]
def tr(p=(0, 0), s=(100, 100), r=0, o=100):
    return {"ty": "tr", "p": p if isinstance(p, dict) else S(list(p)), "a": S([0, 0]),
            "s": s if isinstance(s, dict) else S(list(s)), "r": r if isinstance(r, dict) else S(r),
            "o": o if isinstance(o, dict) else S(o), "sk": S(0), "sa": S(0)}
def fill(c, o=100): return {"ty": "fl", "c": S(col(c)), "o": o if isinstance(o, dict) else S(o), "r": 1}
def stroke(c, w, o=100, lc=2): return {"ty": "st", "c": S(col(c)), "o": o if isinstance(o, dict) else S(o), "w": S(w), "lc": lc, "lj": 2, "ml": 4}
def el(w, h=None, p=(0, 0)): return {"ty": "el", "p": S(list(p)), "s": S([w, h or w])}
def rc(w, h, r=0, p=(0, 0)): return {"ty": "rc", "p": S(list(p)), "s": S([w, h]), "r": S(r)}
def shp(pts, closed=True, ins=None, outs=None):
    n = len(pts)
    return {"v": [list(p) for p in pts], "i": ins or [[0, 0]] * n, "o": outs or [[0, 0]] * n, "c": closed}
def path(pts, closed=True, ins=None, outs=None): return {"ty": "sh", "ks": S(shp(pts, closed, ins, outs))}
def morph(keys):  # [(kare, shp)] → biçim değiştiren yol
    return {"ty": "sh", "ks": A([(t, [s]) for t, s in keys])}
def trim(e): return {"ty": "tm", "s": S(0), "e": e, "o": S(0), "m": 1}
def grp(*it, t=None): return {"ty": "gr", "it": list(it) + [t or tr()]}
def ks(p=(0, 0), s=None, o=None, r=None, a=(0, 0)):
    return {"o": o or S(100), "r": r or S(0),
            "p": p if isinstance(p, dict) else S([p[0], p[1], 0]),
            "a": S([a[0], a[1], 0]), "s": s or S([100, 100, 100])}
_ind = [0]
def L(nm, shapes, k, parent=None):
    _ind[0] += 1
    d = {"ddd": 0, "ind": _ind[0], "ty": 4, "nm": nm, "sr": 1, "ks": k, "ao": 0, "shapes": shapes,
         "ip": 0, "op": OP, "st": 0, "bm": 0}
    if parent: d["parent"] = parent
    return d
def NUL(nm, k):
    _ind[0] += 1
    return {"ddd": 0, "ind": _ind[0], "ty": 3, "nm": nm, "sr": 1, "ks": k, "ao": 0, "ip": 0, "op": OP, "st": 0, "bm": 0}
def P(keys, e=IO): return A([(t, [x, y, 0]) for t, (x, y) in keys], e)
def SC(keys, e=IO): return A([(t, [x, y, 100]) if isinstance(v, tuple) else (t, [v, v, 100]) for t, v in keys for x, y in [v if isinstance(v, tuple) else (v, v)]], e)
def OP_(keys): return A([(t, [v]) for t, v in keys])
def star(r1, r2, n=5):
    pts = []
    for i in range(n * 2):
        a = -math.pi / 2 + i * math.pi / n
        r = r1 if i % 2 == 0 else r2
        pts.append((r * math.cos(a), r * math.sin(a)))
    return path(pts)
def goz(x, y, kirp, r=3.4, renk="#1F2937"):
    """Göz: kırpma kareleri listesi; kırparken dikey ölçek 10'a iner."""
    k = [(0, (100, 100))]
    for t in kirp:
        k += [(t, (100, 100)), (t + 5, (100, 10)), (t + 10, (100, 100))]
    k.append((OP - 1, (100, 100)))
    return grp(el(r * 2, r * 2.3), fill(renk), grp(el(r * 0.8), fill("#FFFFFF"), t=tr(p=(-r * 0.3, -r * 0.4))),
               t=tr(p=(x, y), s=SC(k)))
def agiz(keys, renk="#1F2937", w=2.2):
    return grp(morph(keys), stroke(renk, w))
def gul(w=7, d=4, y=0):  # gülümseme (d>0 güler, d<0 somurtur); her ağız 3 köşeli kapalı biçim → biçimler arası geçiş kırılmaz
    return shp([(-w, y), (w, y), (0, y + d * 0.9)], True,
               [[w * 0.5, 0], [w * 0.5, d * 0.85], [w * 0.5, 0]], [[w * 0.5, d * 0.85], [-w * 0.5, 0], [-w * 0.5, 0]])
def yanak(x, y, o=60): return grp(el(6, 4), fill("#FF8FA3", o), t=tr(p=(x, y)))
def _tekil(o):
    """lottie-web tek anahtarlı animasyonu yanlış çizer (dönüş 90° kayıyordu): durağana çevir."""
    if isinstance(o, dict):
        if o.get("a") == 1 and isinstance(o.get("k"), list) and len(o["k"]) == 1:
            v = o["k"][0]["s"]
            o["a"], o["k"] = 0, (v[0] if isinstance(v, list) and len(v) == 1 and not isinstance(v[0], dict) else (v[0] if isinstance(v, list) and len(v) == 1 else v))
        for x in o.values(): _tekil(x)
    elif isinstance(o, list):
        for x in o: _tekil(x)

def save(nm, layers):
    _tekil(layers)
    _ind[0] = 0
    d = {"v": "5.7.4", "fr": FR, "ip": 0, "op": OP, "w": W, "h": H, "nm": nm, "ddd": 0, "assets": [], "layers": layers}
    (OUT / f"{nm}.json").write_text(json.dumps(d, separators=(",", ":")))
    print(nm, len(layers), "katman", round(len(json.dumps(d)) / 1024, 1), "KB")

# ---------------------------------------------------------------- 1. Zirve
def zirve():
    Ls = []
    # basamak tepeleri (karakterin bastığı noktalar)
    durak = [(26, 128), (46, 112), (66, 96), (86, 80), (106, 62)]
    # zıplama: yay + iniş ezilmesi
    pk, sk = [(0, durak[0])], [(0, (100, 100))]
    t = 24
    for i in range(1, len(durak)):
        (x0, y0), (x1, y1) = durak[i - 1], durak[i]
        pk += [(t, (x0, y0)), (t + 9, ((x0 + x1) / 2, min(y0, y1) - 16)), (t + 18, (x1, y1))]
        sk += [(t - 4, (100, 100)), (t, (118, 82)), (t + 5, (88, 116)), (t + 15, (96, 106)), (t + 18, (124, 78)), (t + 24, (100, 100))]
        t += 30
    # zirve: iki sevinç zıplaması + sonda başlangıca dönüş için kaybolma
    tz = t
    xz, yz = durak[-1]
    pk += [(tz + 6, (xz, yz)), (tz + 18, (xz, yz - 22)), (tz + 30, (xz, yz)), (tz + 42, (xz, yz - 16)), (tz + 54, (xz, yz)), (OP - 1, (xz, yz))]
    sk += [(tz + 6, (120, 80)), (tz + 12, (86, 120)), (tz + 18, (100, 100)), (tz + 30, (122, 80)), (tz + 36, (88, 116)), (tz + 54, (118, 84)), (tz + 62, (100, 100)), (OP - 1, (100, 100))]
    sevinc = tz + 6
    kirp = [60, 150, 250]
    # yıldızlar (zirvede saçılır)
    for i in range(9):
        a = -math.pi / 2 + (i - 4) * 0.36
        x0, y0 = 106, 40
        t0 = sevinc + 6 + (i % 3) * 4
        Ls.append(L(f"yildiz{i}", [grp(star(5 if i % 2 else 3.6, 2), fill(["#FFC93C", "#FF8FA3", "#7CC6FF"][i % 3]))],
                    ks(p=P([(t0, (x0, y0)), (t0 + 40, (x0 + 40 * math.cos(a), y0 + 40 * math.sin(a) + 8))], OUTE),
                       o=OP_([(0, 0), (t0, 0), (t0 + 3, 100), (t0 + 34, 100), (t0 + 48, 0)]),
                       r=A([(t0, [0]), (t0 + 48, [200])]), s=SC([(t0, 30), (t0 + 14, 130), (t0 + 48, 70)]))))
    # bayrak: direk yükselir, bez dalgalanır
    bez0 = shp([(0, 0), (9, 3), (18, 0), (18, 10), (9, 13), (0, 10)], True, [[0, 0], [-4, 0], [0, 0], [0, 0], [4, 0], [0, 0]], [[0, 0], [4, 0], [0, 0], [0, 0], [-4, 0], [0, 0]])
    bez1 = shp([(0, 0), (9, -2), (18, 2), (18, 12), (9, 8), (0, 10)], True, [[0, 0], [-4, 0], [0, 0], [0, 0], [4, 0], [0, 0]], [[0, 0], [4, 0], [0, 0], [0, 0], [-4, 0], [0, 0]])
    dalga = [(sevinc + 8, bez0)]
    for j in range(8):
        dalga.append((sevinc + 18 + j * 14, bez1 if j % 2 == 0 else bez0))
    Ls.append(L("bayrak", [grp(morph(dalga), fill("#FF5A5F"), t=tr(p=(1, -26))),
                           grp(path([(0, 0), (0, -26)], False), stroke("#6B4F3A", 2.4))],
                ks(p=(118, 64), s=A([(0, [100, 0, 100]), (sevinc, [100, 0, 100]), (sevinc + 14, [100, 112, 100]), (sevinc + 22, [100, 100, 100])]))))
    # karakter (top): gövde + yüz + kollar (zirvede havaya kalkar)
    kol_asagi = shp([(-9, 2), (-15, 8)], False); kol_yukari = shp([(-9, -2), (-15, -12)], False)
    kol_asagi2 = shp([(9, 2), (15, 8)], False); kol_yukari2 = shp([(9, -2), (15, -12)], False)
    kollar = [grp(morph([(0, kol_asagi), (sevinc, kol_asagi), (sevinc + 8, kol_yukari)]), stroke("#E89A1E", 3)),
              grp(morph([(0, kol_asagi2), (sevinc, kol_asagi2), (sevinc + 8, kol_yukari2)]), stroke("#E89A1E", 3))]
    yuz = [goz(-4.5, -3, kirp), goz(4.5, -3, kirp), yanak(-8, 2), yanak(8, 2),
           agiz([(0, gul(4, 2, 3)), (sevinc, gul(4, 2, 3)), (sevinc + 8, shp([(-5, 2), (5, 2), (0, 8)], True, [[0, 0], [0, 0], [4, 0]], [[0, 0], [0, 0], [-4, 0]]))])]
    govde = [grp(el(22, 22), fill("#FFC93C")), grp(el(8, 5), fill("#FFFFFF", 70), t=tr(p=(-5, -7), r=-25))]
    Ls.append(L("karakter", yuz + kollar + govde, ks(p=P(pk), s=SC(sk), a=(0, 10))))
    Ls.append(L("golge", [grp(el(18, 4), fill("#1F2937", 18))], ks(p=P([(t_, (x, durak_y + 11)) for t_, (x, _y) in pk for durak_y in [min((dy for dx, dy in durak if abs(dx - x) < 11), default=_y)]]))))
    # basamaklar (yumuşak çizilir)
    yol = path([(16, 139), (36, 139), (36, 123), (56, 123), (56, 107), (76, 107), (76, 91), (96, 91), (96, 73), (120, 73)], False)
    Ls.append(L("yol", [grp(yol, trim(A([(0, [6]), (24, [20]), (sevinc, [100])])), stroke("#FFFFFF", 3.5))], ks()))
    # dağlar
    Ls.append(L("kar", [grp(path([(108, 72), (100, 84), (106, 80), (112, 86), (118, 80)]), fill("#FFFFFF"))], ks(p=(0, -26))))
    Ls.append(L("dag", [grp(path([(0, 152), (56, 84), (74, 100), (108, 46), (160, 152)]), fill("#7E9CCB"))], ks()))
    Ls.append(L("dag2", [grp(path([(-14, 152), (30, 108), (72, 152)]), fill("#AFC4E4"))], ks()))
    # bulutçuklar süzülür
    for j, (y, hiz) in enumerate([(30, 1.0), (52, 0.7)]):
        b = [grp(el(14), fill("#FFFFFF"), t=tr(p=(-6, 0))), grp(el(18), fill("#FFFFFF"), t=tr(p=(4, -3))), grp(rc(26, 8, 4, p=(0, 4)), fill("#FFFFFF"))]
        Ls.append(L(f"bulut{j}", b, ks(p=P([(0, (20 + j * 70, y)), (OP - 1, (20 + j * 70 + 30 * hiz, y))], ({"x": [0], "y": [0]}, {"x": [1], "y": [1]})), o=S(85))))
    Ls.append(L("gok", [grp(rc(160, 160), fill("#E6F2FF"))], ks(p=(80, 80))))
    Ls.append(L("isik", [grp(el(110), fill("#FFF1C4"))], ks(p=(106, 40), o=OP_([(0, 0), (sevinc - 6, 0), (sevinc + 20, 90), (OP - 30, 90), (OP - 1, 0)]), s=SC([(sevinc - 6, 30), (sevinc + 30, 100)]))))
    Ls.insert(len(Ls) - 2, Ls.pop(Ls.index(next(l for l in Ls if l["nm"] == "isik"))))
    save("zirve", Ls)

# ---------------------------------------------------------------- 2. Çalışma
def calisma():
    Ls = []
    kirp = [40, 120, 220]
    aha = 150
    # parıltılar (aha anında)
    for i in range(8):
        a = i * math.pi / 4 + 0.2
        t0 = aha + (i % 2) * 5
        Ls.append(L(f"pr{i}", [grp(star(4.5, 1.6, 4), fill(["#FFC93C", "#7CC6FF", "#FF8FA3"][i % 3]))],
                    ks(p=P([(t0, (80 + 18 * math.cos(a), 34 + 18 * math.sin(a))), (t0 + 36, (80 + 44 * math.cos(a), 34 + 40 * math.sin(a)))], OUTE),
                       o=OP_([(0, 0), (t0, 0), (t0 + 3, 100), (t0 + 26, 100), (t0 + 40, 0)]), r=A([(t0, [0]), (t0 + 40, [120])]))))
    # ampul ışınları (nabız gibi)
    for i in range(8):
        a = i * math.pi / 4
        p1 = (80 + 21 * math.cos(a), 34 + 21 * math.sin(a)); p2 = (80 + 29 * math.cos(a), 34 + 29 * math.sin(a))
        Ls.append(L(f"isin{i}", [grp(path([p1, p2], False), trim(A([(aha, [0]), (aha + 12, [100])], OUTE)), stroke("#FFB020", 3))],
                    ks(o=OP_([(0, 0), (aha - 1, 0), (aha, 100), (OP - 20, 100), (OP - 1, 0)]))))
    # ampul karakteri: uykulu (yarım göz) → uyanır, gülümser, sallanır
    yari = shp([(-3, 0), (3, 0)], False)
    ampul_yuz = [
        grp(morph([(0, yari), (aha - 2, yari)]), stroke("#4B5563", 1.8), t=tr(p=(-4, -2), o=OP_([(0, 100), (aha - 1, 100), (aha, 0)]))),
        grp(morph([(0, yari), (aha - 2, yari)]), stroke("#4B5563", 1.8), t=tr(p=(4, -2), o=OP_([(0, 100), (aha - 1, 100), (aha, 0)]))),
        grp(goz(-4, -2, [aha + 40, aha + 110], 2.4, "#4B5563"), t=tr(o=OP_([(0, 0), (aha - 1, 0), (aha, 100)]))),
        grp(goz(4, -2, [aha + 40, aha + 110], 2.4, "#4B5563"), t=tr(o=OP_([(0, 0), (aha - 1, 0), (aha, 100)]))),
        agiz([(0, gul(2.5, 0, 4)), (aha, gul(2.5, 0, 4)), (aha + 8, gul(4, 3, 3))], "#4B5563", 1.8),
    ]
    cam = [grp(el(26), fill({"a": 0, "k": col("#FFFFFF")} and "#FFF6D6")),
           grp(el(26), fill("#FFD23F", OP_([(0, 0), (aha - 2, 0), (aha + 6, 100), (OP - 20, 100), (OP - 1, 0)]))),
           grp(el(26), stroke("#4B5563", 2)),
           grp(rc(11, 4, 2, p=(0, 15)), fill("#6B7280")), grp(rc(9, 4, 2, p=(0, 19)), fill("#6B7280"))]
    Ls.append(L("ampul", ampul_yuz + cam,
                ks(p=P([(0, (80, 36)), (60, (80, 33)), (120, (80, 36)), (aha, (80, 36)), (aha + 10, (80, 28)), (aha + 22, (80, 36)), (OP - 1, (80, 36))]),
                   r=A([(0, [0]), (aha, [0]), (aha + 10, [-10]), (aha + 20, [8]), (aha + 30, [-4]), (aha + 40, [0]), (OP - 1, [0])]),
                   s=SC([(0, 100), (aha, 100), (aha + 10, 118), (aha + 24, 100)]))))
    Ls.append(L("hale", [grp(el(56), fill("#FFF0A8"))], ks(p=(80, 34), o=OP_([(0, 0), (aha - 2, 0), (aha + 10, 90), (OP - 20, 60), (OP - 1, 0)]),
                                                            s=SC([(aha - 2, 40), (aha + 14, 112), (aha + 40, 96), (aha + 70, 108), (aha + 100, 96), (OP - 1, 100)]))))
    # "z z" uyku harfleri (aha'dan önce)
    for j in range(2):
        t0 = 20 + j * 50
        Ls.append(L(f"z{j}", [grp(path([(-3, -3), (3, -3), (-3, 3), (3, 3)], False), stroke("#9CA3AF", 1.8))],
                    ks(p=P([(t0, (94, 26)), (t0 + 50, (104, 6))]), o=OP_([(0, 0), (t0, 0), (t0 + 8, 100), (t0 + 40, 100), (t0 + 50, 0)]),
                       s=SC([(t0, 60), (t0 + 50, 120)]))))
    # çevrilen sayfalar (akıcı)
    for j in range(4):
        t0 = 30 + j * 26
        pg = grp(path([(0, 0), (30, -4), (30, 30), (0, 34)]), fill("#FFFFFF"), path([(0, 0), (30, -4), (30, 30), (0, 34)]), stroke("#C9D3E3", 1.1))
        Ls.append(L(f"sayfa{j}", [pg], ks(p=(80, 92), s=A([(0, [100, 100, 100]), (t0, [100, 100, 100]), (t0 + 22, [-100, 100, 100])]),
                                          o=OP_([(0, 0), (t0, 0), (t0 + 1, 100), (t0 + 22, 100), (t0 + 23, 0)]))))
    # kitap karakteri: gözlüklü, okurken gözleri satırlarda gezer, aha'da sevinir
    gozbebek = P([(0, (-2, 0)), (30, (2, 0)), (60, (-2, 0)), (90, (2, 0)), (120, (-2, 0)), (aha, (0, -1)), (OP - 1, (0, -1))])
    gozluk = [grp(el(14), stroke("#1F2937", 1.8), t=tr(p=(-10, 0))), grp(el(14), stroke("#1F2937", 1.8), t=tr(p=(10, 0))),
              grp(path([(-3, 0), (3, 0)], False), stroke("#1F2937", 1.8))]
    bebek = [grp(el(4.4), fill("#1F2937"), t=tr(p=gozbebek)), ]
    kitap_yuz = [grp(*gozluk, grp(el(4.4), fill("#1F2937"), t=tr(p=(-10, 0))), grp(el(4.4), fill("#1F2937"), t=tr(p=(10, 0))), t=tr(p=P([(0, (-2, 0)), (30, (2, 0)), (60, (-2, 0)), (90, (2, 0)), (120, (-2, 0)), (aha, (0, -1)), (OP - 1, (0, -1))]))),
                 agiz([(0, gul(4, 1, 10)), (aha, gul(4, 1, 10)), (aha + 8, gul(7, 4, 9))]),
                 yanak(-17, 8, 0), yanak(17, 8, 0)]
    kitap_yuz[-2]["it"][1]["o"] = OP_([(0, 0), (aha, 0), (aha + 8, 70)])
    kitap_yuz[-1]["it"][1]["o"] = OP_([(0, 0), (aha, 0), (aha + 8, 70)])
    Ls.append(L("kitap_yuz", kitap_yuz, ks(p=(80, 112))))
    sag = grp(path([(0, 0), (34, -6), (34, 32), (0, 38)]), fill("#F5F8FD"), path([(0, 0), (34, -6), (34, 32), (0, 38)]), stroke("#A9BAD3", 1.4))
    sol = grp(path([(0, 0), (-34, -6), (-34, 32), (0, 38)]), fill("#F5F8FD"), path([(0, 0), (-34, -6), (-34, 32), (0, 38)]), stroke("#A9BAD3", 1.4))
    satir = grp(*[path([(-28, 3 + k * 6), (-6, 6 + k * 6)], False) for k in range(3)], *[path([(6, 6 + k * 6), (28, 3 + k * 6)], False) for k in range(3)], stroke("#CBD5E1", 1.5))
    zipla = P([(0, (80, 92)), (aha, (80, 92)), (aha + 8, (80, 84)), (aha + 18, (80, 92)), (OP - 1, (80, 92))])
    Ls.append(L("kitap_ic", [satir, sag, sol], ks(p=zipla, s=SC([(0, (100, 100)), (aha + 16, (100, 100)), (aha + 18, (110, 90)), (aha + 26, (100, 100))]))))
    Ls[-2]["ks"]["p"] = P([(0, (80, 112)), (aha, (80, 112)), (aha + 8, (80, 104)), (aha + 18, (80, 112)), (OP - 1, (80, 112))])
    kapak = grp(path([(-37, -4), (0, 2), (37, -4), (37, 37), (0, 43), (-37, 37)]), fill("#3D7BE0"))
    Ls.append(L("kapak", [kapak], ks(p=zipla)))
    Ls.append(L("golge", [grp(el(86, 8), fill("#1F2937", 14))], ks(p=(80, 140), s=SC([(0, 100), (aha + 8, (80, 100)), (aha + 18, 100)]))))
    Ls.append(L("zemin", [grp(rc(160, 160), fill("#FFF8EC"))], ks(p=(80, 80))))
    save("calisma", Ls)

# ---------------------------------------------------------------- 3. Sevgi ve güç
def sevgi():
    Ls = []
    kv = [[0, 26], [-30, -2], [-15, -25], [0, -14], [15, -25], [30, -2]]
    ki = [[12, -12], [0, 14], [-10, 0], [-3, -7], [-8, 0], [0, -14]]
    ko = [[-12, -12], [0, -14], [8, 0], [3, -7], [10, 0], [0, 14]]
    bir = 96       # birleşme
    guc = 150      # pazı gösterisi
    kirp = [140, 210, 262]
    # sevgi halkaları
    for j in range(3):
        t0 = bir + 4 + j * 40
        Ls.append(L(f"halka{j}", [grp(el(60), stroke("#FF7AA2", 3))],
                    ks(p=(80, 80), s=SC([(t0, 70), (t0 + 56, 200)], OUTE), o=OP_([(0, 0), (t0, 0), (t0 + 2, 70), (t0 + 56, 0)]))))
    # küçük kalpler yükselir
    mini = path([[0, 6], [-7, -1], [-3.5, -6], [0, -3], [3.5, -6], [7, -1]], True, [[3, -3], [0, 3], [-2, 0], [-1, -2], [-2, 0], [0, -3]], [[-3, -3], [0, -3], [2, 0], [1, -2], [2, 0], [0, 3]])
    for i in range(6):
        t0 = guc + 10 + i * 12
        x = 36 + i * 18
        Ls.append(L(f"mini{i}", [grp(mini, fill(["#FF5C8A", "#FF9EB8", "#FFC93C"][i % 3]))],
                    ks(p=P([(t0, (x, 120)), (t0 + 60, (x + (6 if i % 2 else -6), 30))]), o=OP_([(0, 0), (t0, 0), (t0 + 6, 100), (t0 + 44, 100), (t0 + 60, 0)]),
                       r=A([(t0, [-15]), (t0 + 30, [15]), (t0 + 60, [-10])]), s=SC([(t0, 50), (t0 + 20, 110), (t0 + 60, 80)]))))
    # bütün kalp: yüz + pazılar
    kol_l0 = shp([(-26, 4), (-34, 10)], False)
    kol_l1 = shp([(-26, 4), (-38, 0), (-36, -12)], False, [[0, 0], [0, 4], [0, 0]], [[0, 0], [0, -4], [0, 0]])
    kol_r0 = shp([(26, 4), (34, 10)], False)
    kol_r1 = shp([(26, 4), (38, 0), (36, -12)], False, [[0, 0], [0, 4], [0, 0]], [[0, 0], [0, -4], [0, 0]])
    pazi = OP_([(0, 0), (guc + 6, 0), (guc + 10, 100), (OP - 30, 100), (OP - 20, 0)])
    kollar = [grp(morph([(0, kol_l0), (guc, kol_l0), (guc + 10, kol_l1), (OP - 30, kol_l1), (OP - 18, kol_l0)]), stroke("#E2365E", 4)),
              grp(morph([(0, kol_r0), (guc, kol_r0), (guc + 10, kol_r1), (OP - 30, kol_r1), (OP - 18, kol_r0)]), stroke("#E2365E", 4)),
              grp(el(8, 7), fill("#E2365E", pazi), t=tr(p=(-36, -3), s=SC([(guc + 8, 40), (guc + 16, 130), (guc + 24, 100), (guc + 50, 120), (guc + 60, 100)]))),
              grp(el(8, 7), fill("#E2365E", pazi), t=tr(p=(36, -3), s=SC([(guc + 8, 40), (guc + 16, 130), (guc + 24, 100), (guc + 50, 120), (guc + 60, 100)])))]
    yuz = [goz(-9, -4, kirp, 3.6), goz(9, -4, kirp, 3.6), yanak(-16, 4, 80), yanak(16, 4, 80),
           agiz([(0, gul(5, 3, 6)), (guc, gul(5, 3, 6)), (guc + 8, shp([(-7, 5), (7, 5), (0, 13)], True, [[0, 0], [0, 0], [5, 0]], [[0, 0], [0, 0], [-5, 0]]))], "#7A1631", 2.2)]
    nabiz = [(bir, 100), (bir + 10, 124), (bir + 22, 96), (bir + 32, 106), (bir + 44, 100), (guc, 100), (guc + 10, 112), (guc + 22, 100),
             (guc + 50, 108), (guc + 62, 100), (guc + 90, 108), (guc + 102, 100), (OP - 1, 100)]
    Ls.append(L("kalp", yuz + kollar + [grp(el(10, 6), fill("#FFFFFF", 60), t=tr(p=(-15, -14), r=-30)),
                                        grp(path(kv, ins=ki, outs=ko), fill("#FF4F7B"))],
                ks(p=P([(0, (80, 84)), (guc, (80, 84)), (guc + 10, (80, 80)), (OP - 1, (80, 84))]), s=SC(nabiz), o=OP_([(0, 0), (bir - 1, 0), (bir, 100), (OP - 14, 100), (OP - 1, 0)]))))
    Ls.append(L("parlama", [grp(el(84), fill("#FFD6E3"))], ks(p=(80, 82), o=OP_([(0, 0), (bir - 2, 0), (bir + 12, 90), (OP - 20, 70), (OP - 1, 0)]),
                                                              s=SC([(bir - 2, 40), (bir + 18, 112), (bir + 40, 100), (guc + 10, 115), (guc + 40, 100)]))))
    # iki utangaç yarı: yan yan kayar, birbirine bakar, sıçrar ve birleşir
    sol = path([[0, 26], [-30, -2], [-15, -25], [0, -14]], True, ki[:4], ko[:4])
    sag = path([[0, 26], [0, -14], [15, -25], [30, -2]], True, [[12, -12], [3, -7], [-8, 0], [0, -14]], [[-12, -12], [-3, -7], [10, 0], [0, 14]])
    for nm, yarı, x0, gx, r0 in (("sol", sol, 26, -14, -18), ("sag", sag, 134, 14, 18)):
        yuz_y = [goz(gx, -6, [30], 3), yanak(gx - (4 if gx < 0 else -4), 3, 90)]
        Ls.append(L(nm, yuz_y + [grp(yarı, fill("#FF9EB8"))],
                    ks(p=P([(0, (x0, 96)), (14, (x0, 96)), (50, ((x0 + 80) / 2, 92)), (66, ((x0 + 80) / 2, 92)), (80, ((x0 + 80) / 2 + (8 if x0 < 80 else -8), 72)), (bir, (80, 84))]),
                       r=A([(0, [r0]), (50, [r0 * 0.6]), (66, [r0 * 0.3]), (80, [0])]), s=SC([(0, 60), (14, 100), (66, (100, 100)), (72, (112, 88)), (80, (94, 108)), (bir, 100)]),
                       o=OP_([(0, 0), (10, 100), (bir, 100), (bir + 1, 0)]))))
    Ls.append(L("zemin", [grp(rc(160, 160), fill("#FFF3F6"))], ks(p=(80, 80))))
    save("sevgi", Ls)

# ---------------------------------------------------------------- 4. Zor günler geçer
def gunes():
    Ls = []
    cik = 70       # güneş çıkar
    it = 110       # bulutu iter
    gozluk = 170   # güneş gözlüğü düşer
    kirp = [cik + 30, 230]
    # gökkuşağı
    renk = ["#FF5A5F", "#FFA53D", "#FFD93D", "#4CD07D", "#4DA3FF", "#9B6BFF"]
    for k, c in enumerate(renk):
        r = 64 - k * 5
        yay = path([(-r, 0), (0, -r), (r, 0)], False, [[0, 0], [-r * 0.552, 0], [0, -r * 0.552]], [[0, -r * 0.552], [r * 0.552, 0], [0, 0]])
        Ls.append(L(f"gk{k}", [grp(yay, trim(A([(0, [0]), (it + 20 + k * 3, [0]), (it + 70 + k * 3, [100])], OUTE)), stroke(c, 4.6, lc=1))],
                    ks(p=(80, 146), o=OP_([(0, 0), (it + 19, 0), (it + 20, 90), (OP - 16, 90), (OP - 1, 0)]))))
    # güneş: gözlük + yüz + ışınlar
    g_gozluk = [grp(rc(13, 8, 3, p=(-7, -3)), fill("#1F2937")), grp(rc(13, 8, 3, p=(7, -3)), fill("#1F2937")),
                grp(path([(-1, -4), (1, -4)], False), stroke("#1F2937", 2)), grp(el(4, 2.4), fill("#FFFFFF", 70), t=tr(p=(-9, -5)))]
    gyuz = [grp(*g_gozluk, t=tr(p=P([(0, (0, -40)), (gozluk, (0, -40)), (gozluk + 14, (0, 1)), (gozluk + 20, (0, -2)), (gozluk + 26, (0, 0))], OUTE),
                                  o=OP_([(0, 0), (gozluk - 1, 0), (gozluk, 100), (OP - 14, 100), (OP - 1, 0)]))),
            goz(-6, -3, kirp, 3), goz(6, -3, kirp, 3), yanak(-11, 4), yanak(11, 4),
            agiz([(0, gul(4, 2, 5)), (it, gul(4, 2, 5)), (it + 10, gul(6, 4, 4)), (gozluk + 20, gul(6, 4, 4)),
                  (gozluk + 28, shp([(-6, 4), (6, 4), (0, 11)], True, [[0, 0], [0, 0], [4, 0]], [[0, 0], [0, 0], [-4, 0]]))], "#9A5B00", 2)]
    isinlar = []
    for i in range(10):
        a = i * math.pi / 5
        isinlar.append(path([(23 * math.cos(a), 23 * math.sin(a)), (31 * math.cos(a), 31 * math.sin(a))], False))
    Ls.append(L("gunes_yuz", gyuz + [grp(el(36), fill("#FFC83D")), grp(el(26), fill("#FFDD6E"), t=tr(p=(-4, -4)))],
                ks(p=P([(0, (122, 150)), (cik, (122, 150)), (cik + 30, (112, 66)), (it, (100, 62)), (it + 20, (80, 60)), (OP - 1, (80, 60))]),
                   r=A([(0, [0]), (cik + 30, [0]), (it, [-8]), (it + 20, [6]), (it + 34, [0])]),
                   s=SC([(0, 100), (it + 18, (100, 100)), (it + 20, (116, 88)), (it + 28, 100)]))))
    Ls.append(L("gunes_isin", [grp(*isinlar, stroke("#FFB020", 3.4))],
                ks(p=P([(0, (122, 150)), (cik, (122, 150)), (cik + 30, (112, 66)), (it, (100, 62)), (it + 20, (80, 60)), (OP - 1, (80, 60))]),
                   r=A([(0, [0]), (OP - 1, [72])], ({"x": [0], "y": [0]}, {"x": [1], "y": [1]})),
                   s=SC([(0, 70), (cik + 30, 100), (it + 40, 112), (it + 70, 100), (it + 100, 110), (it + 130, 100), (OP - 1, 104)]))))
    # bulut: üzgün ağlar → itilir → beyazlaşıp güler, uzaklaşır
    bulut_gri = [grp(el(34), fill("#7B8494"), t=tr(p=(-14, 4))), grp(el(42), fill("#7B8494"), t=tr(p=(6, -4))),
                 grp(el(30), fill("#7B8494"), t=tr(p=(24, 6))), grp(rc(62, 18, 9, p=(4, 12)), fill("#7B8494"))]
    bulut_beyaz = [grp(el(34), fill("#FFFFFF", OP_([(0, 0), (it + 10, 0), (it + 40, 100)])), t=tr(p=(-14, 4))),
                   grp(el(42), fill("#FFFFFF", OP_([(0, 0), (it + 10, 0), (it + 40, 100)])), t=tr(p=(6, -4))),
                   grp(el(30), fill("#FFFFFF", OP_([(0, 0), (it + 10, 0), (it + 40, 100)])), t=tr(p=(24, 6))),
                   grp(rc(62, 18, 9, p=(4, 12)), fill("#FFFFFF", OP_([(0, 0), (it + 10, 0), (it + 40, 100)])))]
    kas_uzgun = shp([(-3, -2), (3, 0)], False); kas_mutlu = shp([(-3, 0), (3, 0)], False)
    byuz = [goz(-4, 2, [40, it + 60], 3), goz(12, 2, [40, it + 60], 3),
            grp(morph([(0, kas_uzgun), (it + 10, kas_uzgun), (it + 24, kas_mutlu)]), stroke("#374151", 1.6), t=tr(p=(-4, -5))),
            grp(morph([(0, shp([(-3, 0), (3, -2)], False)), (it + 10, shp([(-3, 0), (3, -2)], False)), (it + 24, kas_mutlu)]), stroke("#374151", 1.6), t=tr(p=(12, -5))),
            agiz([(0, gul(4, -3, 12)), (it + 10, gul(4, -3, 12)), (it + 26, gul(5, 3, 11))], "#374151", 2),
            grp(el(3.6, 5), fill("#7FC4FF", OP_([(0, 0), (20, 100), (it, 100), (it + 8, 0)])), t=tr(p=P([(20, (-6, 6)), (60, (-6, 16)), (61, (-6, 6)), (100, (-6, 16))])))]
    Ls.append(L("bulut", byuz + bulut_beyaz + bulut_gri,
                ks(p=P([(0, (74, 52)), (40, (78, 54)), (80, (72, 52)), (it, (74, 52)), (it + 14, (54, 56)), (it + 40, (30, 60)), (OP - 40, (24, 62)), (OP - 1, (74, 52))]),
                   r=A([(0, [0]), (it, [0]), (it + 10, [-10]), (it + 26, [4]), (it + 40, [0])]),
                   s=SC([(0, 100), (it, 100), (it + 12, (90, 110)), (it + 26, 80), (OP - 40, 74), (OP - 1, 100)]),
                   o=OP_([(0, 100), (OP - 30, 100), (OP - 16, 0), (OP - 1, 100)]))))
    # yağmur (itilene dek)
    for i in range(8):
        x = 54 + (i % 4) * 13 + (i // 4) * 6
        for rep in range(4):
            a = (i * 7) % 26 + rep * 26
            if a > it - 6: continue
            Ls.append(L(f"d{i}_{rep}", [grp(path([(0, 0), (-2, 8)], False), stroke("#8EC5FF", 2.4))],
                        ks(p=P([(a, (x, 70)), (a + 24, (x - 6, 132))], ({"x": [0.5], "y": [0]}, {"x": [1], "y": [1]})),
                           o=OP_([(0, 0), (a, 0), (a + 1, 90), (a + 20, 90), (a + 24, 0)]))))
    # su birikintisi → çiçek açar
    Ls.append(L("cicek", [grp(el(7), fill("#FFC83D")),
                          *[grp(el(7, 9), fill("#FF8FA3"), t=tr(p=(6 * math.cos(i * 1.2566), 6 * math.sin(i * 1.2566)))) for i in range(5)],
                          grp(path([(0, 4), (0, 18)], False), stroke("#3FA65A", 2.4))],
                ks(p=(132, 128), s=SC([(0, 0), (it + 60, 0), (it + 76, 116), (it + 86, 100), (OP - 16, 100), (OP - 1, 0)]), r=A([(it + 76, [-8]), (it + 120, [8]), (it + 160, [-4])]))))
    Ls.append(L("cimen", [grp(rc(160, 26, 0, p=(80, 150)), fill("#9BE0A8"))], ks()))
    Ls.append(L("gok_acik", [grp(rc(160, 160), fill("#DDEEFF"))], ks(p=(80, 80), o=OP_([(0, 0), (cik, 0), (it + 30, 100), (OP - 16, 100), (OP - 1, 0)]))))
    Ls.append(L("gok_gri", [grp(rc(160, 160), fill("#CDD3DC"))], ks(p=(80, 80))))
    save("gunes", Ls)

def zirve_v3():
    global OP
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import zirve_sahne
    OP = 600
    _ind[0] = 0
    Ls = zirve_sahne.sahne(sys.modules[__name__])
    save("zirve", Ls)
    OP = 300

def uzun(ad, op):
    global OP
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import sahneler2
    OP = op
    _ind[0] = 0
    Ls = getattr(sahneler2, ad)(sys.modules[__name__], op)
    save(ad, Ls)
    OP = 300

zirve_v3(); uzun("gunes", 540); uzun("sevgi", 480); uzun("calisma", 540)
