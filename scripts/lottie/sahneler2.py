"""Uzun, ayrıntılı sahneler: güneş (9 sn), sevgi (8 sn), çalışma (9 sn). hikaye_animasyonlari.py çağırır.

gunes  : şemsiyeli kız kara bulutun yağmuru altında üzgün → güneş tepenin ardından göz kırparak çıkar → ışın kolunu uzatıp
         bulutu gıdıklar → bulut kıkırdar, beyazlar, uzaklaşır → kız şemsiyeyi kapatır, yanında çiçek açar, gökkuşağı,
         sevinçle iki kez zıplar.
sevgi  : küçük kalp halteri kaldırmaya çalışır, titrer, terler, düşürür (güm!) → ikinci kalp el sallayarak gelir, omzuna
         dokunur → sarılırlar, birleşip büyük kalp olurlar → büyük kalp halteri tek kolla kaldırır, öbür koluyla pazı yapar.
calisma: öğrenci masada uyuklar (baş düşer, "z") → kahveyi yudumlar, gözleri fal taşı, saçı dikilir → hızlı hızlı yazar,
         kitaplar üst üste dizilir → "?" kafasını kaşır → ampul yanar "!" → sandalyeden fırlayıp sevinir, sandalye kayar →
         geri oturup başparmağını kaldırır.
"""
import math
import karakter

def _ac(h):
    return (h.A, h.S, h.P, h.SC, h.OP_, h.L, h.grp, h.el, h.rc, h.path, h.shp, h.morph, h.fill, h.stroke, h.tr, h.ks, h.star, h.trim, h.OUTE)

LIN = ({"x": [0], "y": [0]}, {"x": [1], "y": [1]})

def perde(h, OP, renk):
    return h.L("perde", [h.grp(h.rc(160, 160), h.fill(renk))], h.ks(p=(80, 80), o=h.OP_([(0, 100), (12, 0), (OP - 14, 0), (OP - 1, 100)])))

def gul(h, w, d, y): return h.gul(w, d, y)
def acik(h, w=4.5, y=3.5, d=5.5):  # açık gülen ağız
    return h.shp([(-w, y), (w, y), (0, y + d)], True, [[0, 0], [0, 0], [w * 0.75, 0]], [[0, 0], [0, 0], [-w * 0.75, 0]])
def somurt(h, w=2.6, y=5): return h.gul(w, -1.6, y)

# =====================================================================================================  GÜNEŞ
def gunes(h, OP=540):
    A, S, P, SC, OP_, L, grp, el, rc, path, shp, morph, fill, stroke, tr, ks, star, trim, OUTE = _ac(h)
    CIK, GIDIK, KIKIR, GIT, KAPA, CICEK, ZIP = 150, 210, 250, 290, 340, 380, 440
    Ls = []
    zemin = 132
    kx = 58
    G_y = zemin - 14.4 - 25.6
    # --- kız (şemsiye ön elde)
    sems_acik = shp([(-20, 26), (0, 40), (20, 26)], True, [[0, 0], [-11, 0], [0, 9]], [[0, 9], [11, 0], [0, 0]])
    sems_kapali = shp([(-3, 26), (0, 40), (3, 26)], True, [[0, 0], [-1.5, 0], [0, 6]], [[0, 6], [1.5, 0], [0, 0]])
    on_el = [grp(morph([(0, sems_acik), (KAPA, sems_acik), (KAPA + 16, sems_kapali), (OP - 1, sems_kapali)]), fill("#7A5CFF")),
             grp(path([(-20, 26), (-10, 28), (0, 26), (10, 28), (20, 26)], False), stroke("#5A3FE0", 1.4),
                 t=tr(o=OP_([(0, 100), (KAPA, 100), (KAPA + 8, 0)]))),
             grp(path([(0, 6), (0, 40)], False), stroke("#4B5563", 1.6)),
             grp(path([(0, 6), (0, 3), (-3, 2)], False, [[0, 0], [0, 1], [1.5, 0]], [[0, -1], [-1, 0], [0, 0]]), stroke("#4B5563", 1.6))]
    kirp = [60, 150, 240, 360, 470]
    zip_G = [(0, (kx, G_y)), (ZIP, (kx, G_y))]
    zip_R = [(0, 100), (ZIP - 6, 100)]
    for j in range(2):
        t0 = ZIP + j * 34
        zip_G += [(t0 + 4, (kx, G_y)), (t0 + 15, (kx, G_y - 16)), (t0 + 26, (kx, G_y))]
        zip_R += [(t0, (116, 84)), (t0 + 6, (90, 112)), (t0 + 15, 100), (t0 + 26, (118, 82)), (t0 + 32, 100)]
    zip_G.append((OP - 1, (kx, G_y)))
    eklem = {
        "kol_on": [(0, 172), (60, 168), (120, 174), (KAPA, 172), (KAPA + 20, 20), (ZIP, 20), (ZIP + 8, 165), (ZIP + 70, 165), (ZIP + 80, 20), (OP - 1, 20)],
        "dirsek_on": [(0, -6), (KAPA, -6), (KAPA + 20, -10), (OP - 1, -10)],
        "kol_arka": [(0, -10), (KAPA, -10), (KAPA + 30, -10), (ZIP, -10), (ZIP + 8, -165), (ZIP + 70, -165), (ZIP + 80, -10), (OP - 1, -10)],
        "dirsek_arka": [(0, -20), (OP - 1, -20)],
        "uyluk_on": [(0, 4), (ZIP, 4), (ZIP + 15, -24), (ZIP + 26, 4), (ZIP + 49, -24), (ZIP + 60, 4), (OP - 1, 4)],
        "baldir_on": [(0, 2), (ZIP, 2), (ZIP + 15, 40), (ZIP + 26, 2), (ZIP + 49, 40), (ZIP + 60, 2), (OP - 1, 2)],
        "uyluk_arka": [(0, -4), (ZIP, -4), (ZIP + 15, 18), (ZIP + 26, -4), (ZIP + 49, 18), (ZIP + 60, -4), (OP - 1, -4)],
        "baldir_arka": [(0, 2), (ZIP, 2), (ZIP + 15, 34), (ZIP + 26, 2), (ZIP + 49, 34), (ZIP + 60, 2), (OP - 1, 2)],
        "govde": [(0, 4), (KAPA, 4), (KAPA + 20, 0), (OP - 1, 0)],
        "bas": [(0, 10), (CIK, 10), (CIK + 10, -8), (GIDIK, -14), (GIT, -14), (KAPA + 20, -20), (CICEK, -10), (CICEK + 20, 10), (ZIP, 0), (OP - 1, 0)],
    }
    agiz_k = [(0, somurt(h)), (CIK + 10, somurt(h)), (CIK + 20, h.gul(2.5, 0.4, 4.5)), (KIKIR, h.gul(3, 1.6, 4)), (KAPA + 20, h.gul(3.4, 2.4, 3.8)),
              (ZIP, acik(h, 3.8, 3.4, 4.6)), (OP - 1, acik(h, 3.8, 3.4, 4.6))]
    kas_k = [(0, shp([(-2.6, -1.4), (2.6, 0.4)], False)), (CIK + 10, shp([(-2.6, -1.4), (2.6, 0.4)], False)), (CIK + 20, shp([(-2.6, -0.6), (2.6, -0.6)], False)), (OP - 1, shp([(-2.6, -0.8), (2.6, -0.8)], False))]
    kiz, kid = karakter.insan(h, "kiz", zip_G, eklem, agiz_k, kirp, renk={"ust": "#FFB84D", "ust2": "#F09A2A", "alt": "#E8547A", "alt2": "#C9446A", "sac": "#3B2416"},
                              R_s=zip_R, kas_k=kas_k, sac="atkuyrugu", on_el=on_el, agiz_ic=OP_([(0, 0), (ZIP - 1, 0), (ZIP, 100)]))
    # --- güneş: tepenin ardından çıkar, göz kırpar, ışın kolu uzatır
    gx0, gy0, gx1, gy1 = 136, 140, 126, 56
    g_p = P([(0, (gx0, gy0)), (CIK, (gx0, gy0)), (CIK + 30, (gx1, gy1 + 10)), (CIK + 44, (gx1, gy1)), (GIT, (gx1, gy1)), (GIT + 40, (108, 40)), (OP - 1, (108, 40))])
    g_kirp = h.goz(-6, -3, [CIK + 36, GIT + 60, 470], 3)
    goz_sag = grp(h.goz(6, -3, [CIK + 36, 400], 3))
    gyuz = [g_kirp, goz_sag, h.yanak(-11, 4, 70), h.yanak(11, 4, 70),
            grp(morph([(0, h.gul(4, 2, 5)), (GIDIK, h.gul(4, 2, 5)), (GIDIK + 10, h.gul(5, 3.4, 4.4)), (KIKIR + 20, acik(h, 5.5, 3.6, 6)), (OP - 1, acik(h, 5.5, 3.6, 6))]), stroke("#9A5B00", 2),
                fill("#C0462F", OP_([(0, 0), (KIKIR + 19, 0), (KIKIR + 20, 100)])))]
    Ls.append(L("gunes_yuz", gyuz + [grp(el(36), fill("#FFC83D")), grp(el(26), fill("#FFDD6E"), t=tr(p=(-4, -4)))],
                ks(p=g_p, r=A([(0, [0]), (CIK + 44, [0]), (CIK + 54, [-8]), (CIK + 66, [0])]))))
    isinlar = [path([(23 * math.cos(i * math.pi / 5), 23 * math.sin(i * math.pi / 5)), (31 * math.cos(i * math.pi / 5), 31 * math.sin(i * math.pi / 5))], False) for i in range(10)]
    Ls.append(L("gunes_isin", [grp(*isinlar, stroke("#FFB020", 3.4))], ks(p=g_p, r=A([(0, [0]), (OP - 1, [90])], LIN),
                                                                          s=SC([(0, 70), (CIK + 44, 100), (GIT + 40, 114), (GIT + 80, 100), (GIT + 120, 112), (OP - 1, 104)]))))
    # ışın kolu (gıdıklama): güneşten buluta uzanan dalgalı ışın, ucu kıpır kıpır
    kol0 = shp([(gx1 - 18, gy1 + 2), (gx1 - 20, gy1 + 2)], False)
    kol1 = shp([(gx1 - 18, gy1 + 2), (100, 58), (84, 46)], False, [[0, 0], [6, 4], [0, 0]], [[0, 0], [-6, -4], [0, 0]])
    kol2 = shp([(gx1 - 18, gy1 + 2), (100, 54), (84, 50)], False, [[0, 0], [6, 4], [0, 0]], [[0, 0], [-6, -4], [0, 0]])
    kk = [(0, kol0), (GIDIK, kol0), (GIDIK + 16, kol1)]
    t = GIDIK + 22; j = 0
    while t < KIKIR + 30:
        kk.append((t, kol2 if j % 2 else kol1)); t += 5; j += 1
    kk += [(KIKIR + 44, kol0), (OP - 1, kol0)]
    Ls.append(L("isin_kol", [grp(morph(kk), stroke("#FFB020", 3.4, lc=2))], ks(o=OP_([(0, 0), (GIDIK - 1, 0), (GIDIK, 100), (KIKIR + 44, 100), (KIKIR + 45, 0)]))))
    # --- bulut: üzgün, ağlar → kıkırdar (titrer), beyazlar, uzaklaşır
    def bulut_par(c, o=None):
        f = lambda: fill(c, o) if o is not None else fill(c)
        return [grp(el(34), f(), t=tr(p=(-14, 4))), grp(el(42), f(), t=tr(p=(6, -4))), grp(el(30), f(), t=tr(p=(24, 6))), grp(rc(62, 18, 9, p=(4, 12)), f())]
    beyaz_o = OP_([(0, 0), (KIKIR, 0), (KIKIR + 30, 100)])
    bul_agiz = [(0, h.gul(4, -3, 12)), (GIDIK + 16, h.gul(4, -3, 12)), (GIDIK + 24, acik(h, 5, 10, 5)), (OP - 1, acik(h, 5, 10, 5))]
    goz_bul = [h.goz(-4, 2, [60, 140], 3), h.goz(12, 2, [60, 140], 3)]
    # kıkırdarken gözler kapalı yay (^ ^)
    kapali = [grp(path([(-3, 1), (0, -2), (3, 1)], False), stroke("#374151", 1.8), t=tr(p=(-4, 2))), grp(path([(-3, 1), (0, -2), (3, 1)], False), stroke("#374151", 1.8), t=tr(p=(12, 2)))]
    for g in goz_bul: g["it"][-1]["o"] = OP_([(0, 100), (GIDIK + 18, 100), (GIDIK + 20, 0), (KIKIR + 30, 0), (KIKIR + 32, 100)])
    for g in kapali: g["it"][-1]["o"] = OP_([(0, 0), (GIDIK + 18, 0), (GIDIK + 20, 100), (KIKIR + 30, 100), (KIKIR + 32, 0)])
    gozyasi = grp(el(3.4, 5), fill("#7FC4FF"), t=tr(p=P([(10, (-6, 6)), (50, (-6, 18)), (51, (-6, 6)), (90, (-6, 18)), (91, (-6, 6)), (130, (-6, 18))]),
                                                    o=OP_([(0, 0), (10, 100), (GIDIK, 100), (GIDIK + 4, 0)])))
    titre = [(0, (0, 0)), (GIDIK + 18, (0, 0))]
    t = GIDIK + 20; j = 0
    while t < KIKIR + 30:
        titre.append((t, (2.4 if j % 2 else -2.4, -1 if j % 2 else 1))); t += 3; j += 1
    titre.append((KIKIR + 32, (0, 0)))
    b_p = P([(0, (70, 44)), (60, (74, 46)), (120, (68, 44)), (GIT, (70, 44)), (GIT + 60, (-30, 36)), (OP - 1, (-30, 36))])
    Ls.append(L("bulut", [grp(*goz_bul, *kapali, gozyasi, grp(morph(bul_agiz), stroke("#374151", 2), fill("#E05555", OP_([(0, 0), (GIDIK + 23, 0), (GIDIK + 24, 100)]))),
                              *bulut_par("#FFFFFF", beyaz_o), *bulut_par("#7B8494"), t=tr(p=P(titre, LIN)))],
                ks(p=b_p, s=SC([(0, 100), (GIT, 100), (GIT + 60, 80)]))))
    # "hi hi" yazısı yerine kıkırdama notaları
    for j in range(3):
        t0 = GIDIK + 24 + j * 14
        Ls.append(L(f"kikir{j}", [grp(star(3, 1.2, 4), fill("#FFFFFF"))], ks(p=P([(t0, (96, 30)), (t0 + 30, (104 + j * 4, 14))]), o=OP_([(0, 0), (t0, 0), (t0 + 3, 100), (t0 + 30, 0)]))))
    # yağmur (kıkırdayana dek)
    for i in range(8):
        x = 48 + (i % 4) * 13 + (i // 4) * 6
        for rep in range(9):
            a = (i * 7) % 26 + rep * 26
            if a > KIKIR: continue
            Ls.append(L(f"d{i}_{rep}", [grp(path([(0, 0), (-2, 8)], False), stroke("#8EC5FF", 2.4))],
                        ks(p=P([(a, (x, 66)), (a + 24, (x - 6, 128))], ({"x": [0.5], "y": [0]}, {"x": [1], "y": [1]})), o=OP_([(0, 0), (a, 0), (a + 1, 90), (a + 20, 90), (a + 24, 0)]))))
    # şemsiyeye çarpan damla sıçramaları
    for j in range(4):
        t0 = 20 + j * 34
        Ls.append(L(f"sicra{j}", [grp(el(2.4), fill("#BFE0FF"))], ks(p=P([(t0, (kx - 6 + j * 4, 70)), (t0 + 14, (kx - 18 + j * 10, 64)), (t0 + 24, (kx - 22 + j * 12, 76))]),
                                                                  o=OP_([(0, 0), (t0, 0), (t0 + 1, 100), (t0 + 24, 0)]))))
    # gökkuşağı
    renk = ["#FF5A5F", "#FFA53D", "#FFD93D", "#4CD07D", "#4DA3FF", "#9B6BFF"]
    for k, c in enumerate(renk):
        rr = 70 - k * 5
        yay = path([(-rr, 0), (0, -rr), (rr, 0)], False, [[0, 0], [-rr * 0.552, 0], [0, -rr * 0.552]], [[0, -rr * 0.552], [rr * 0.552, 0], [0, 0]])
        Ls.append(L(f"gk{k}", [grp(yay, trim(A([(0, [0]), (CICEK + k * 3, [0]), (CICEK + 50 + k * 3, [100])], OUTE)), stroke(c, 4.6, lc=1))],
                    ks(p=(80, 140), o=OP_([(0, 0), (CICEK - 1, 0), (CICEK, 85), (OP - 16, 85), (OP - 1, 0)]))))
    # çiçek büyür
    cicek = [grp(el(7), fill("#FFC83D")), *[grp(el(7, 9), fill("#FF8FA3"), t=tr(p=(6 * math.cos(i * 1.2566), 6 * math.sin(i * 1.2566)))) for i in range(5)]]
    Ls.append(L("cicek_tac", cicek, ks(p=P([(0, (104, zemin)), (CICEK, (104, zemin)), (CICEK + 30, (104, zemin - 18))]), s=SC([(0, 0), (CICEK + 20, 0), (CICEK + 34, 120), (CICEK + 42, 100)]),
                                      r=A([(CICEK + 34, [-10]), (CICEK + 70, [10]), (CICEK + 110, [-6]), (OP - 1, [0])]))))
    Ls.append(L("cicek_sap", [grp(path([(104, zemin), (104, zemin - 16)], False), trim(A([(CICEK, [0]), (CICEK + 30, [100])])), stroke("#3FA65A", 2.4)),
                              grp(el(7, 4, (108, zemin - 8)), fill("#4CC06A", OP_([(0, 0), (CICEK + 20, 0), (CICEK + 26, 100)])))], ks()))
    # su birikintisi küçülür
    Ls.append(L("birikinti", [grp(el(34, 5), fill("#9CC9F5"))], ks(p=(kx + 4, zemin + 2), s=SC([(0, (30, 100)), (KIKIR, (100, 100)), (KAPA + 40, (100, 100)), (CICEK + 40, (0, 100))]))))
    Ls[0:0] = []
    # zemin, tepe, gök
    alt = [L("tepe", [grp(path([(96, 160), (120, 112), (150, 104), (170, 118), (170, 160)], True, [[0, 0], [-10, 8], [-8, 0], [0, 0], [0, 0]], [[0, 0], [8, -6], [8, 0], [0, 0], [0, 0]]), fill("#7CCB8C"))], ks()),
           L("cimen", [grp(rc(160, 30, 0, p=(80, 148)), fill("#9BE0A8"))], ks()),
           L("gok_acik", [grp(rc(160, 160), fill("#DDEEFF"))], ks(p=(80, 80), o=OP_([(0, 0), (KIKIR, 0), (GIT + 30, 100), (OP - 16, 100), (OP - 1, 0)]))),
           L("gok_gri", [grp(rc(160, 160), fill("#C9D0DA"))], ks(p=(80, 80)))]
    ust = [perde(h, OP, "#C9D0DA")]
    # tepe güneşin önünde olmalı: güneş tepeden sonra çizilir
    gunes_l = [l for l in Ls if l["nm"].startswith("gunes")]
    diger = [l for l in Ls if not l["nm"].startswith("gunes") and l["nm"] not in ("birikinti",) and not l["nm"].startswith("gk")]
    gk = [l for l in Ls if l["nm"].startswith("gk")]
    birik = [l for l in Ls if l["nm"] == "birikinti"]
    return ust + diger + kiz + birik + gk + [alt[0]] + gunes_l + alt[1:]

# =====================================================================================================  SEVGİ
def sevgi(h, OP=480):
    A, S, P, SC, OP_, L, grp, el, rc, path, shp, morph, fill, stroke, tr, ks, star, trim, OUTE = _ac(h)
    TUT, ZOR, DUS, GEL, DOKUN, SARIL, BIR, KALDIR, PAZI = 50, 70, 150, 190, 236, 262, 290, 316, 360
    Ls = []
    kv = [[0, 26], [-30, -2], [-15, -25], [0, -14], [15, -25], [30, -2]]
    ki = [[12, -12], [0, 14], [-10, 0], [-3, -7], [-8, 0], [0, -14]]
    ko = [[-12, -12], [0, -14], [8, 0], [3, -7], [10, 0], [0, 14]]
    kalp = lambda: path(kv, ins=ki, outs=ko)
    zemin = 134

    def yuz(kirp, agiz_k, kapali_o=None, buyuk=1.0, agiz_ic=None, renk="#7A1631"):
        k = [h.goz(-9, -4, kirp, 3.4), h.goz(9, -4, kirp, 3.4), h.yanak(-16, 4, 80), h.yanak(16, 4, 80),
             grp(morph(agiz_k), stroke(renk, 2.2), *([fill("#B0263F", agiz_ic)] if agiz_ic else []))]
        if kapali_o is not None:  # zorlanırken sıkılmış gözler > <
            for g in k[:2]: g["it"][-1]["o"] = OP_([(0, 100)] + [(t, 0 if v else 100) for t, v in kapali_o])
            k += [grp(path([(-12, -6), (-7, -4), (-12, -2)], False), stroke("#7A1631", 1.8), t=tr(o=OP_([(0, 0)] + [(t, 100 if v else 0) for t, v in kapali_o]))),
                  grp(path([(12, -6), (7, -4), (12, -2)], False), stroke("#7A1631", 1.8), t=tr(o=OP_([(0, 0)] + [(t, 100 if v else 0) for t, v in kapali_o])))]
        return k

    # ---------------- küçük kalp (sol)
    zig = acik(h, 4.5, 5.5, 2.4)
    kucuk_agiz = [(0, h.gul(4, 2, 6)), (TUT, h.gul(4, 2, 6)), (ZOR, zig), (DUS, zig), (DUS + 8, h.gul(4, 0.3, 7)), (DUS + 20, h.gul(4, -2.4, 8)),
                  (DOKUN + 6, h.gul(4, -2.4, 8)), (DOKUN + 16, h.gul(4, 2.6, 6)), (OP - 1, h.gul(4, 2.6, 6))]
    kapali = [(ZOR, True), (DUS, False)]
    # kollar (kalbin yerel koordinatı): dinlenme / tutma / üzgün / dokunulunca
    kolL = [(0, shp([(-26, 2), (-32, 14)], False)), (TUT, shp([(-26, 2), (-32, 14)], False)), (TUT + 12, shp([(-24, 6), (-18, 24)], False)),
            (DUS, shp([(-24, 6), (-18, 24)], False)), (DUS + 6, shp([(-26, 2), (-34, 12)], False)), (OP - 1, shp([(-26, 2), (-34, 12)], False))]
    kolR = [(0, shp([(26, 2), (32, 14)], False)), (TUT, shp([(26, 2), (32, 14)], False)), (TUT + 12, shp([(24, 6), (18, 24)], False)),
            (DUS, shp([(24, 6), (18, 24)], False)), (DUS + 6, shp([(26, 2), (34, 12)], False)), (OP - 1, shp([(26, 2), (34, 12)], False))]
    bacak = [grp(path([(-8, 22), (-10, 34)], False), stroke("#C9365A", 3.6)), grp(path([(8, 22), (10, 34)], False), stroke("#C9365A", 3.6)),
             grp(el(7, 4, (-11, 35)), fill("#C9365A")), grp(el(7, 4, (11, 35)), fill("#C9365A"))]
    titre = [(0, 0), (ZOR, 0)]
    t = ZOR + 2; j = 0
    while t < DUS:
        titre.append((t, 3.5 if j % 2 else -3.5)); t += 3; j += 1
    titre += [(DUS + 2, 0), (OP - 1, 0)]
    kucuk = L("kucuk", yuz([30, DUS + 40], kucuk_agiz, kapali) + [grp(morph(kolL), stroke("#C9365A", 3.6)), grp(morph(kolR), stroke("#C9365A", 3.6))] + bacak + [
        grp(el(10, 6), fill("#FFFFFF", 60), t=tr(p=(-15, -14), r=-30)), grp(kalp(), fill("#FF6B8E"))],
        ks(p=P([(0, (54, zemin - 36)), (TUT, (54, zemin - 36)), (TUT + 12, (54, zemin - 30)), (DUS, (54, zemin - 30)), (DUS + 8, (54, zemin - 36)), (SARIL, (62, zemin - 36)), (BIR, (80, zemin - 40))]),
           r=A([(t_, [v]) for t_, v in titre]), s=SC([(0, 70), (TUT + 12, (74, 64)), (DUS, (74, 64)), (DUS + 4, (64, 76)), (DUS + 12, 70), (SARIL, 70), (BIR, 70)]),
           o=OP_([(0, 100), (BIR - 1, 100), (BIR, 0)])))
    # ter damlaları
    for j in range(3):
        t0 = ZOR + 10 + j * 22
        Ls.append(L(f"ter{j}", [grp(path([(0, -3), (2, 1), (0, 3), (-2, 1)], True, [[0, 0], [0, -1], [1.2, 0], [0, 1]], [[0, 0], [0, 1], [-1.2, 0], [0, -1]]), fill("#7FC4FF"))],
                    ks(p=P([(t0, (62 + (j % 2) * 10 - 5, zemin - 58)), (t0 + 20, (70 + (j % 2) * 18 - 9, zemin - 46))]), o=OP_([(0, 0), (t0, 0), (t0 + 2, 100), (t0 + 20, 0)]))))
    # halter: yerde → titrek kalkış → düşer (güm) → büyük kalp tek kolla kaldırır
    hy = [(0, (54, zemin - 4)), (ZOR, (54, zemin - 4))]
    t = ZOR + 4; j = 0
    while t < DUS - 6:
        hy.append((t, (54 + (1 if j % 2 else -1), zemin - 8 - (j % 3)))); t += 4; j += 1
    hy += [(DUS, (54, zemin - 9)), (DUS + 6, (54, zemin - 4)), (DUS + 9, (54, zemin - 6)), (DUS + 12, (54, zemin - 4)), (KALDIR, (60, zemin - 4)),
           (KALDIR + 26, (106, 50)), (KALDIR + 34, (106, 56)), (PAZI + 10, (106, 52)), (PAZI + 30, (106, 56)), (PAZI + 50, (106, 52)), (OP - 1, (106, 54))]
    halter = L("halter", [grp(rc(36, 3, 1.5), fill("#6B7280")), grp(rc(6, 16, 2, p=(-17, 0)), fill("#374151")), grp(rc(6, 16, 2, p=(17, 0)), fill("#374151")),
                          grp(rc(4, 12, 1.5, p=(-22, 0)), fill("#4B5563")), grp(rc(4, 12, 1.5, p=(22, 0)), fill("#4B5563"))],
               ks(p=P(hy), r=A([(0, [0]), (KALDIR, [0]), (KALDIR + 26, [-90]), (OP - 1, [-90])]), s=SC([(0, 100), (KALDIR, 100), (KALDIR + 26, 80)])))
    # güm! tozu ve yıldızı
    for j, (dx, dy) in enumerate([(-24, -6), (-14, -12), (14, -12), (24, -6)]):
        Ls.append(L(f"toz{j}", [grp(el(7), fill("#E8D5DD"))], ks(p=P([(DUS + 6, (54, zemin)), (DUS + 30, (54 + dx, zemin + dy))], OUTE), o=OP_([(0, 0), (DUS + 6, 0), (DUS + 7, 90), (DUS + 30, 0)]),
                                                                  s=SC([(DUS + 6, 30), (DUS + 30, 150)]))))
    # ---------------- ikinci kalp (sağdan gelir, el sallar)
    yuru = [(0, (180, zemin - 36)), (GEL, (180, zemin - 36))]
    t = GEL; j = 0
    while t < DOKUN - 8:
        x = 180 - (t - GEL) * (180 - 82) / (DOKUN - 8 - GEL)
        yuru.append((t, (x, zemin - 36 - (4 if j % 2 else 0)))); t += 8; j += 1
    yuru += [(DOKUN - 8, (82, zemin - 36)), (SARIL, (74, zemin - 36)), (BIR, (80, zemin - 40))]
    salla = [(0, shp([(-26, 2), (-32, 14)], False)), (GEL, shp([(-26, 2), (-32, 14)], False))]
    t = GEL + 4; j = 0
    while t < DOKUN - 10:
        salla.append((t, shp([(-24, 0), (-34, -14)], False) if j % 2 else shp([(-24, 0), (-28, -18)], False))); t += 7; j += 1
    salla += [(DOKUN - 4, shp([(-26, 2), (-32, 14)], False)), (OP - 1, shp([(-26, 2), (-32, 14)], False))]
    dokun = [(0, shp([(26, 2), (32, 14)], False)), (DOKUN - 6, shp([(26, 2), (32, 14)], False)), (DOKUN, shp([(26, 0), (40, -4)], False)), (DOKUN + 18, shp([(26, 0), (40, -4)], False)),
             (SARIL, shp([(26, 0), (44, 2)], False)), (OP - 1, shp([(26, 0), (44, 2)], False))]
    ikinci = L("ikinci", yuz([GEL + 30, DOKUN + 40], [(0, h.gul(4, 3, 6)), (OP - 1, h.gul(4, 3, 6))]) + [grp(morph(salla), stroke("#C48A00", 3.6)), grp(morph(dokun), stroke("#C48A00", 3.6))] +
               [grp(path([(-8, 22), (-10, 34)], False), stroke("#C48A00", 3.6)), grp(path([(8, 22), (10, 34)], False), stroke("#C48A00", 3.6)),
                grp(el(10, 6), fill("#FFFFFF", 60), t=tr(p=(-15, -14), r=-30)), grp(kalp(), fill("#FFC23D"))],
               ks(p=P(yuru), s=SC([(0, (-70, 70)), (SARIL, (-70, 70)), (BIR, (-70, 70))]), o=OP_([(0, 100), (BIR - 1, 100), (BIR, 0)])))
    # sarılma parlaması
    Ls.append(L("flas", [grp(el(70), fill("#FFFFFF"))], ks(p=(80, zemin - 42), o=OP_([(0, 0), (BIR - 8, 0), (BIR, 100), (BIR + 14, 0)]), s=SC([(BIR - 8, 40), (BIR + 14, 160)]))))
    # ---------------- büyük kalp
    kolL_b = [(0, shp([(-26, 2), (-34, 12)], False)), (KALDIR, shp([(-26, 2), (-34, 12)], False)), (PAZI, shp([(-26, 2), (-34, 12)], False)),
              (PAZI + 10, shp([(-26, 2), (-40, 0), (-38, -14)], False, [[0, 0], [0, 4], [0, 0]], [[0, 0], [0, -4], [0, 0]])), (OP - 1, shp([(-26, 2), (-40, 0), (-38, -14)], False, [[0, 0], [0, 4], [0, 0]], [[0, 0], [0, -4], [0, 0]]))]
    kolR_b = [(0, shp([(26, 2), (34, 12)], False)), (KALDIR, shp([(26, 2), (34, 12)], False)), (KALDIR + 26, shp([(26, 0), (30, -26)], False)), (OP - 1, shp([(26, 0), (30, -26)], False))]
    pazi_o = OP_([(0, 0), (PAZI + 6, 0), (PAZI + 10, 100)])
    buyuk = L("buyuk", yuz([BIR + 40, 420], [(0, h.gul(5, 3, 6)), (BIR + 10, h.gul(5, 3, 6)), (PAZI + 6, acik(h, 6, 5, 7)), (OP - 1, acik(h, 6, 5, 7))], agiz_ic=OP_([(0, 0), (PAZI + 5, 0), (PAZI + 6, 100)])) + [
        grp(morph(kolL_b), stroke("#B8123E", 4.4)), grp(morph(kolR_b), stroke("#B8123E", 4.4)),
        grp(el(9, 8), fill("#B8123E", pazi_o), t=tr(p=(-38, -4), s=SC([(PAZI + 8, 40), (PAZI + 16, 140), (PAZI + 24, 100), (PAZI + 50, 130), (PAZI + 60, 100)]))),
        grp(path([(-8, 22), (-11, 36)], False), stroke("#B8123E", 4.4)), grp(path([(8, 22), (11, 36)], False), stroke("#B8123E", 4.4)),
        grp(el(10, 6), fill("#FFFFFF", 60), t=tr(p=(-15, -14), r=-30)), grp(kalp(), fill("#FF3D6E"))],
        ks(p=(80, zemin - 40), s=SC([(0, 0), (BIR - 1, 0), (BIR, 90), (BIR + 10, 112), (BIR + 20, 96), (BIR + 30, 100), (PAZI, 100), (PAZI + 10, 106), (PAZI + 20, 100), (OP - 1, 100)]),
           o=OP_([(0, 0), (BIR - 1, 0), (BIR, 100)])))
    # sevgi halkaları + mini kalpler + "ding" parıltısı
    for j in range(3):
        t0 = BIR + 6 + j * 40
        Ls.append(L(f"halka{j}", [grp(el(64), stroke("#FF7AA2", 3))], ks(p=(80, zemin - 42), s=SC([(t0, 70), (t0 + 56, 210)], OUTE), o=OP_([(0, 0), (t0, 0), (t0 + 2, 70), (t0 + 56, 0)]))))
    mini = path([[0, 6], [-7, -1], [-3.5, -6], [0, -3], [3.5, -6], [7, -1]], True, [[3, -3], [0, 3], [-2, 0], [-1, -2], [-2, 0], [0, -3]], [[-3, -3], [0, -3], [2, 0], [1, -2], [2, 0], [0, 3]])
    for i in range(7):
        t0 = PAZI + 6 + i * 12
        x = 24 + i * 18
        Ls.append(L(f"mini{i}", [grp(mini, fill(["#FF5C8A", "#FF9EB8", "#FFC93C"][i % 3]))],
                    ks(p=P([(t0, (x, 124)), (t0 + 60, (x + (6 if i % 2 else -6), 26))]), o=OP_([(0, 0), (t0, 0), (t0 + 6, 100), (t0 + 44, 100), (t0 + 60, 0)]),
                       r=A([(t0, [-15]), (t0 + 30, [15]), (t0 + 60, [-10])]), s=SC([(t0, 50), (t0 + 20, 110), (t0 + 60, 80)]))))
    Ls.append(L("ding", [grp(star(6, 2, 4), fill("#FFE066"))], ks(p=(112, 40), o=OP_([(0, 0), (KALDIR + 28, 0), (KALDIR + 30, 100), (KALDIR + 50, 0)]), s=SC([(KALDIR + 28, 30), (KALDIR + 40, 140), (KALDIR + 50, 60)]))))
    alt = [L("golge1", [grp(el(40, 6), fill("#B03A5B", 14))], ks(p=(80, zemin + 1))),
           L("zemin", [grp(rc(160, 30, 0, p=(80, 150)), fill("#FFE3EA"))], ks()),
           L("gok", [grp(rc(160, 160), fill("#FFF4F7"))], ks(p=(80, 80)))]
    return [perde(h, OP, "#FFF4F7")] + Ls + [buyuk, halter, kucuk, ikinci] + alt

# =====================================================================================================  ÇALIŞMA
def calisma(h, OP=540):
    A, S, P, SC, OP_, L, grp, el, rc, path, shp, morph, fill, stroke, tr, ks, star, trim, OUTE = _ac(h)
    YUDUM, UYAN, YAZ, SORU, AHA, FIRLA, OTUR = 120, 150, 190, 300, 345, 375, 450
    Ls = []
    zemin = 134
    kx, ky = 64, 112          # kalça (oturma)
    G_y = ky - 25.6
    fy = [(0, (kx, G_y)), (FIRLA, (kx, G_y)), (FIRLA + 10, (kx + 4, G_y - 4)), (FIRLA + 22, (kx + 6, G_y - 30)), (FIRLA + 34, (kx + 6, G_y - 6)),
          (FIRLA + 46, (kx + 6, G_y - 26)), (FIRLA + 58, (kx + 6, G_y - 6)), (OTUR - 10, (kx + 6, G_y - 6)), (OTUR + 6, (kx, G_y)), (OP - 1, (kx, G_y))]
    R_s = [(0, 100), (FIRLA + 32, 100), (FIRLA + 34, (116, 84)), (FIRLA + 40, (92, 110)), (FIRLA + 46, 100), (FIRLA + 56, 100), (FIRLA + 58, (116, 84)), (FIRLA + 66, 100),
           (OTUR + 6, (110, 90)), (OTUR + 14, 100)]
    # baş: uyuklama (ileri düşer, irkilir)
    bas = [(0, 4)]
    for j in range(3):
        t0 = 10 + j * 36
        bas += [(t0, 4), (t0 + 22, 32), (t0 + 26, 26), (t0 + 30, -4)]
    bas += [(YUDUM, 0), (UYAN, -16), (UYAN + 14, 6), (YAZ, 14), (SORU, 14), (SORU + 10, -10), (AHA, -14), (FIRLA, -6), (FIRLA + 30, -16), (OTUR, 0), (OTUR + 20, -8), (OP - 1, -8)]
    yaz_dirsek = [(YAZ, -40)]
    t = YAZ; j = 0
    while t < SORU:
        yaz_dirsek.append((t, -50 if j % 2 else -30)); t += 4; j += 1
    eklem = {
        "uyluk_on": [(0, -88), (FIRLA, -88), (FIRLA + 10, -20), (FIRLA + 22, 0), (FIRLA + 58, 0), (OTUR, -40), (OTUR + 6, -88), (OP - 1, -88)],
        "baldir_on": [(0, 88), (FIRLA, 88), (FIRLA + 10, 30), (FIRLA + 22, 10), (FIRLA + 58, 4), (OTUR, 40), (OTUR + 6, 88), (OP - 1, 88)],
        "uyluk_arka": [(0, -84), (FIRLA, -84), (FIRLA + 10, -10), (FIRLA + 22, 6), (FIRLA + 58, 2), (OTUR, -40), (OTUR + 6, -84), (OP - 1, -84)],
        "baldir_arka": [(0, 96), (FIRLA, 96), (FIRLA + 10, 20), (FIRLA + 22, 20), (FIRLA + 58, 4), (OTUR, 40), (OTUR + 6, 96), (OP - 1, 96)],
        "govde": [(0, 10), (YUDUM, 4), (UYAN, -10), (UYAN + 14, 4), (YAZ, 14), (SORU, 10), (FIRLA, 0), (OTUR + 6, 6), (OP - 1, 2)],
        "bas": bas,
        "kol_on": [(0, -60), (YUDUM - 10, -60), (YUDUM, -130), (UYAN + 10, -130), (YAZ, -70), (SORU, -70), (SORU + 10, -160), (AHA, -160), (AHA + 10, -60),
                   (FIRLA, -60), (FIRLA + 10, -170), (OTUR - 10, -170), (OTUR + 10, -60), (OTUR + 30, -110), (OP - 1, -110)],
        "dirsek_on": [(0, -40), (YUDUM - 10, -40), (YUDUM, -100), (UYAN + 10, -100)] + yaz_dirsek + [(SORU + 10, -90), (AHA, -90), (AHA + 10, -40), (FIRLA, -40), (FIRLA + 10, 0),
                                                                                                   (OTUR - 10, 0), (OTUR + 10, -40), (OTUR + 30, -70), (OP - 1, -70)],
        "kol_arka": [(0, -50), (FIRLA, -50), (FIRLA + 10, 170), (OTUR - 10, 170), (OTUR + 10, -50), (OP - 1, -50)],
        "dirsek_arka": [(0, -40), (FIRLA, -40), (FIRLA + 10, 0), (OTUR - 10, 0), (OTUR + 10, -40), (OP - 1, -40)],
    }
    agiz_k = [(0, h.gul(2, 0, 4.5)), (40, h.shp([(-2.4, 4), (2.4, 4), (0, 8)], True, [[0, -2], [0, 0], [2, 0]], [[0, 0], [0, -2], [-2, 0]])), (60, h.gul(2, 0, 4.5)),  # esneme
              (UYAN, h.shp([(-2.4, 4), (2.4, 4), (0, 7)], True, [[0, -2], [0, 0], [2, 0]], [[0, 0], [0, -2], [-2, 0]])), (UYAN + 20, h.gul(2.6, 1, 4)),
              (SORU, h.gul(2.6, -0.6, 4.5)), (AHA, acik(h, 3.6, 3.4, 4.6)), (OP - 1, acik(h, 3.6, 3.4, 4.6))]
    goz_buyu = SC([(0, (100, 60)), (UYAN - 2, (100, 60)), (UYAN, (140, 150)), (UYAN + 30, (140, 150)), (UYAN + 50, 100), (OP - 1, 100)])
    kupa = [grp(rc(6, 7, 1.5, p=(0, 10)), fill("#FFFFFF")), grp(rc(6, 7, 1.5, p=(0, 10)), stroke("#9CA3AF", 1)), grp(rc(4, 2, 0.5, p=(0, 7.5)), fill("#6B3F1D"))]
    for g in kupa: g["it"][-1]["o"] = OP_([(0, 0), (YUDUM - 12, 0), (YUDUM - 10, 100), (UYAN + 10, 100), (UYAN + 12, 0)])
    ogr, oid = karakter.insan(h, "ogr", fy, eklem, agiz_k, [80, 220, 330, 470], renk={"ust": "#3EB489", "ust2": "#2E9C74", "alt": "#3B4A6B", "alt2": "#323F5C"},
                              R_s=R_s, on_el=kupa, goz_buyu=goz_buyu, agiz_ic=OP_([(0, 0), (35, 0), (40, 100), (58, 100), (60, 0), (UYAN - 1, 0), (UYAN, 100), (UYAN + 18, 100), (UYAN + 20, 0), (AHA - 1, 0), (AHA, 100)]),
                              kas_k=[(0, shp([(-2.6, 0), (2.6, 0)], False)), (SORU, shp([(-2.6, -1.6), (2.6, 0)], False)), (AHA, shp([(-2.6, -1.2), (2.6, -1.2)], False)), (OP - 1, shp([(-2.6, -1), (2.6, -1)], False))])
    # dikilen saç (kahve sonrası)
    dik = L("dik_sac", [grp(path([(-3, 0), (-4, -7)], False), path([(0, 0), (0, -9)], False), path([(3, 0), (4, -7)], False), stroke("#5B3A29", 1.8))],
            ks(p=(0, -9), s=SC([(0, (100, 0)), (UYAN - 2, (100, 0)), (UYAN + 4, (100, 120)), (UYAN + 40, (100, 100)), (UYAN + 60, (100, 0))])))
    dik["parent"] = oid["bas"]
    # "z z" uyku
    for j in range(3):
        t0 = 6 + j * 36
        Ls.append(L(f"z{j}", [grp(path([(-3, -3), (3, -3), (-3, 3), (3, 3)], False), stroke("#9CA3AF", 1.8))],
                    ks(p=P([(t0, (60, 70)), (t0 + 40, (70, 50))]), o=OP_([(0, 0), (t0, 0), (t0 + 6, 100), (t0 + 30, 100), (t0 + 40, 0)]), s=SC([(t0, 60), (t0 + 40, 130)]))))
    # kahve buharı (masadaki kupada, yudumdan önce)
    for j in range(2):
        Ls.append(L(f"buhar{j}", [grp(path([(0, 0), (2, -4), (0, -8), (2, -12)], False, [[0, 0], [0, 2], [0, 0], [0, 2]], [[0, -2], [0, -2], [0, -2], [0, 0]]), stroke("#CBD5E1", 1.4))],
                    ks(p=P([(j * 30, (100 + j * 3, 102)), (j * 30 + 60, (100 + j * 3, 94))]), o=OP_([(0, 0), (j * 30, 0), (j * 30 + 10, 80), (j * 30 + 50, 80), (j * 30 + 60, 0)]))))
    Ls.append(L("masa_kupa", [grp(rc(7, 8, 1.5), fill("#FFFFFF")), grp(rc(7, 8, 1.5), stroke("#9CA3AF", 1)), grp(path([(3.5, -2), (6, 0), (3.5, 2)], False), stroke("#9CA3AF", 1.2))],
                ks(p=(101, 108), o=OP_([(0, 100), (YUDUM - 12, 100), (YUDUM - 10, 0), (UYAN + 10, 0), (UYAN + 12, 100)]))))
    # "!" (uyanınca), "?" (soru), ampul (aha)
    unlem = L("unlem", [grp(rc(2.6, 9, 1.3, p=(0, -3)), fill("#FF5A5F")), grp(el(3, 3, (0, 4)), fill("#FF5A5F"))],
              ks(p=(54, 52), s=SC([(0, 0), (UYAN, 0), (UYAN + 8, 130), (UYAN + 14, 100), (UYAN + 40, 100), (UYAN + 48, 0)])))
    soru = L("soru", [grp(path([(-3, -4), (0, -7), (3, -4), (0, 0), (0, 2)], False, [[0, 0], [-2, 0], [0, -2], [0, 0], [0, 0]], [[0, -2], [2, 0], [0, 2], [0, 0], [0, 0]]), stroke("#4B5563", 2)),
                      grp(el(2.4, 2.4, (0, 5)), fill("#4B5563"))],
             ks(p=(58, 50), s=SC([(0, 0), (SORU, 0), (SORU + 8, 120), (SORU + 14, 100), (AHA - 4, 100), (AHA, 0)]), r=A([(SORU, [0]), (SORU + 20, [-10]), (SORU + 40, [10]), (AHA, [0])])))
    ampul = L("ampul", [grp(el(14), fill("#FFD23F")), grp(el(14), stroke("#B7791F", 1.2)), grp(rc(6, 4, 1, p=(0, 9)), fill("#6B7280")),
                        grp(path([(-2, 1), (0, -2), (2, 1)], False), stroke("#B7791F", 1))],
              ks(p=P([(AHA, (52, 46)), (AHA + 10, (52, 38))]), s=SC([(0, 0), (AHA, 0), (AHA + 8, 130), (AHA + 14, 100), (FIRLA + 60, 100), (FIRLA + 70, 0)])))
    hale = L("hale", [grp(el(36), fill("#FFF3B0"))], ks(p=(52, 38), o=OP_([(0, 0), (AHA + 4, 0), (AHA + 10, 90), (FIRLA + 60, 60), (FIRLA + 70, 0)]), s=SC([(AHA + 4, 40), (AHA + 16, 110)])))
    for i in range(8):
        a = i * math.pi / 4
        t0 = AHA + 8
        Ls.append(L(f"pr{i}", [grp(star(3.4, 1.2, 4), fill(["#FFC93C", "#7CC6FF", "#FF8FA3"][i % 3]))],
                    ks(p=P([(t0, (52 + 10 * math.cos(a), 38 + 10 * math.sin(a))), (t0 + 30, (52 + 30 * math.cos(a), 38 + 28 * math.sin(a)))], OUTE),
                       o=OP_([(0, 0), (t0, 0), (t0 + 2, 100), (t0 + 22, 100), (t0 + 30, 0)]))))
    # masadaki defter: sayfalar çevrilir, yazı satırları belirir; kitap yığını büyür
    sayfa = []
    for j in range(4):
        t0 = YAZ + 10 + j * 26
        sayfa.append(L(f"sayfa{j}", [grp(path([(0, 0), (16, -2), (16, -10), (0, -8)]), fill("#FFFFFF")), grp(path([(0, 0), (16, -2), (16, -10), (0, -8)]), stroke("#CBD5E1", 0.8))],
                       ks(p=(84, 112), s=A([(0, [100, 100, 100]), (t0, [100, 100, 100]), (t0 + 14, [-100, 100, 100])]), o=OP_([(0, 0), (t0, 0), (t0 + 1, 100), (t0 + 14, 100), (t0 + 15, 0)]))))
    satirlar = L("satir", [grp(*[path([(68, 109 - k * 2.2), (82, 108 - k * 2.2)], False) for k in range(3)], trim(A([(YAZ, [0]), (SORU, [100])], LIN)), stroke("#94A3B8", 0.9))], ks())
    defter = L("defter", [grp(path([(66, 112), (84, 112), (84, 104), (66, 102)]), fill("#FFFFFF")), grp(path([(84, 112), (102, 110), (102, 102), (84, 104)]), fill("#F8FAFC")),
                          grp(path([(66, 112), (84, 112), (102, 110)], False), stroke("#CBD5E1", 1))], ks())
    kitaplar = []
    for j, c in enumerate(["#FF7A59", "#5B8DEF", "#FFC23D", "#9B6BFF"]):
        t0 = YAZ + 20 + j * 24
        kitaplar.append(L(f"kitap{j}", [grp(rc(22, 5, 1.2), fill(c)), grp(rc(18, 3, 0.8, p=(1, 0)), fill("#FFFFFF", 60))],
                          ks(p=P([(t0, (128, 40)), (t0 + 12, (128, 109 - j * 5.4))], OUTE), s=SC([(t0 + 10, 100), (t0 + 12, (116, 80)), (t0 + 18, 100)]),
                             r=A([(t0, [30]), (t0 + 12, [(-3 if j % 2 else 3)])]), o=OP_([(0, 0), (t0, 0), (t0 + 1, 100), (OP - 16, 100), (OP - 1, 0)]))))
    # sandalye: fırlayınca kayıp döner, geri gelir
    sandalye = L("sandalye", [grp(rc(20, 4, 1.5, p=(0, 0)), fill("#8B5E3C")), grp(rc(4, 24, 1.5, p=(-9, -12)), fill("#8B5E3C")),
                              grp(path([(-7, 2), (-9, 20)], False), path([(7, 2), (9, 20)], False), stroke("#6B4428", 2.4)),
                              grp(el(4, 4, (-9, 21)), fill("#374151")), grp(el(4, 4, (9, 21)), fill("#374151"))],
                 ks(p=P([(0, (kx, ky + 2)), (FIRLA + 6, (kx, ky + 2)), (FIRLA + 30, (kx - 26, ky + 2)), (OTUR - 20, (kx - 20, ky + 2)), (OTUR, (kx, ky + 2)), (OP - 1, (kx, ky + 2))]),
                    r=A([(0, [0]), (FIRLA + 6, [0]), (FIRLA + 30, [-20]), (FIRLA + 40, [6]), (FIRLA + 50, [0]), (OP - 1, [0])])))
    masa = L("masa", [grp(rc(76, 5, 1.5, p=(120, 114.5)), fill("#C08552")), grp(rc(4, 20, 1, p=(88, 127)), fill("#A06E46")), grp(rc(4, 20, 1, p=(152, 127)), fill("#A06E46")),
                      grp(path([(146, 112), (140, 84), (150, 80)], False), stroke("#4B5563", 2)), grp(path([(144, 80), (156, 80), (152, 72), (148, 72)]), fill("#5B8DEF")),
                      grp(el(26, 18, (150, 98)), fill("#FFF3B0", 40))], ks())
    alt = [L("zemin", [grp(rc(160, 26, 0, p=(80, 150)), fill("#E9DCC9"))], ks()),
           L("pencere", [grp(rc(40, 34, 4, p=(30, 34)), fill("#CFE6FF")), grp(rc(40, 34, 4, p=(30, 34)), stroke("#FFFFFF", 3)), grp(path([(30, 17), (30, 51)], False), stroke("#FFFFFF", 2)),
                         grp(el(8, 8, (40, 28)), fill("#FFE17A"))], ks()),
           L("duvar", [grp(rc(160, 160), fill("#FFF8EC"))], ks(p=(80, 80)))]
    return [perde(h, OP, "#FFF8EC"), unlem, soru, ampul, hale] + Ls + [dik] + kitaplar + sayfa + [satirlar, defter, masa] + ogr + [sandalye] + alt
