"""Zirve sahnesi (10 sn): eklemli dağcı karakter. hikaye_animasyonlari.py içinden çağrılır.

Senaryo (60 fps, 600 kare):
  0–190    sırt çantalı, şapkalı dağcı yamaçtan yürüyerek çıkar (adım döngüsü, kol sallama, öne eğilme, ter damlası)
  190–235  zirvede durur, alnının terini siler, derin nefes
  235–300  çantasından bayrak direğini çıkarır, toprağa çakar (toz bulutu), bayrak açılır
  300–345  gururlu duruş: eller belde, göğüs dışarı, kocaman gülümseme, parıltı
  345–375  rüzgâr başlar, şapkası uçup gider, şaşkın yüz
  375–505  direğe tutunur; rüzgârla bayrak gibi yatay dalgalanır, bacakları çırpınır, ağzı "O", yapraklar ve kuş geriye savrulur
  505–560  rüzgâr diner, sarkaç gibi sallanıp ayakları üstüne düşer (ezilme), başında baş dönmesi yıldızları
  560–600  şapkası gökten tam başına düşer, güler ve başparmağını kaldırır; döngü yumuşak kararmayla başa döner
"""
import math

def sahne(h):
    A, S, P, SC, OP_, L, NUL, grp, el, rc, path, shp, morph, fill, stroke, tr, ks, star, goz, agiz, gul, yanak, trim, OUTE = (
        h.A, h.S, h.P, h.SC, h.OP_, h.L, h.NUL, h.grp, h.el, h.rc, h.path, h.shp, h.morph, h.fill, h.stroke, h.tr, h.ks,
        h.star, h.goz, h.agiz, h.gul, h.yanak, h.trim, h.OUTE)
    OP = 600
    LIN = ({"x": [0], "y": [0]}, {"x": [1], "y": [1]})
    Ls = []

    # ------------------------------------------------ zaman çizelgesi
    T_VARIS, T_SIL, T_DIREK, T_CAK, T_GURUR, T_RUZGAR, T_TUT, T_UC, T_DIN, T_YERE, T_SAPKA, T_SON = \
        190, 200, 235, 270, 300, 345, 375, 390, 505, 540, 565, 588

    # ------------------------------------------------ yürüyüş yolu (kalça noktası)
    yol = [(10, 132), (34, 122), (54, 112), (72, 100), (86, 88), (94, 82)]
    def yol_nokta(u):  # u 0..1, parça parça doğrusal
        n = len(yol) - 1
        x = min(n - 1e-9, u * n); i = int(x); f = x - i
        (x0, y0), (x1, y1) = yol[i], yol[i + 1]
        return x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
    ADIM = 30
    gk = []  # G (tutma noktası = kalçanın 32 px üstü) konumu
    for t in range(0, T_VARIS + 1, 5):
        u = t / T_VARIS
        x, y = yol_nokta(u)
        faz = (t % ADIM) / ADIM
        sek = -1.6 * abs(math.sin(faz * 2 * math.pi))  # her adımda hafif yükselme
        gk.append((t, (x, y - 26 + sek)))
    zx, zy = yol[-1]
    DIREK_X = zx + 16
    TUT = (DIREK_X - 1, zy - 16)          # direkte tutunma noktası
    gk += [(T_GURUR, (zx, zy - 26)), (T_RUZGAR + 10, (zx, zy - 26)), (T_TUT, (TUT[0] - 4, TUT[1] + 4)), (T_UC, TUT),
           (T_DIN, TUT), (T_YERE - 12, TUT), (T_YERE, (DIREK_X - 10, zy - 26)), (OP - 1, (DIREK_X - 10, zy - 26))]
    # G dönüşü: rüzgârda bayrak gibi yatay (-88 civarı dalgalı), dinince sarkaç
    rk = [(0, 0), (T_TUT, 0), (T_UC, -40)]
    t = T_UC
    i = 0
    while t < T_DIN:
        rk.append((t + 8, -82 - (9 if i % 2 else 0) - 3 * math.sin(i)))
        t += 8; i += 1
    rk += [(T_DIN + 14, -20), (T_DIN + 26, 16), (T_DIN + 36, -6), (T_YERE - 12, 0), (OP - 1, 0)]

    G = NUL("G", ks(p=P(gk, h.IO), s=S([80, 80, 100]), r=A([(t_, [v]) for t_, v in rk])))
    Ls.append(G)
    gi = G["ind"]
    # R: kalça (G'nin 32 px altı); inişte ezilme
    R = NUL("R", ks(p=(0, 32), s=SC([(0, 100), (T_YERE - 2, 100), (T_YERE, (118, 80)), (T_YERE + 8, (92, 110)), (T_YERE + 16, 100),
                                     (T_CAK - 4, 100), (T_CAK, (104, 96)), (T_CAK + 8, 100)])))
    R["parent"] = gi
    Ls.append(R)
    ri = R["ind"]

    # ------------------------------------------------ eklem açıları (adım döngüsü + sahne pozları)
    def dongu(t0, t1, gen, kayma=0.0, adim=ADIM):
        k = []
        t = t0
        while t <= t1:
            k.append((t, gen * math.sin(2 * math.pi * ((t - t0) / adim + kayma))))
            t += adim / 4
        return k
    def ekle(k, *son):
        return k + list(son)

    yur = (0, T_VARIS - 10)
    # bacaklar
    uyluk_on = ekle(dongu(*yur, 26), (T_VARIS, 4), (T_GURUR, 6), (T_TUT, 0))
    uyluk_arka = ekle(dongu(*yur, 26, 0.5), (T_VARIS, -4), (T_GURUR, -6), (T_TUT, 0))
    # rüzgârda çırpınma
    def cirpin(k, kay):
        t = T_UC; j = 0
        while t < T_DIN:
            k.append((t, 28 * math.sin(j * 1.7 + kay))); t += 6; j += 1
        k += [(T_DIN + 20, 10), (T_YERE - 2, -14), (T_YERE + 8, 0), (OP - 1, 0)]
        return k
    uyluk_on = cirpin(uyluk_on, 0); uyluk_arka = cirpin(uyluk_arka, 2.2)
    baldir_on = [(t_, max(0, -v) * 1.3 + 4) for t_, v in dongu(*yur, 26)] + [(T_VARIS, 2), (T_UC, 2), (T_UC + 20, 30), (T_DIN, 20), (T_YERE, 26), (T_YERE + 12, 0), (OP - 1, 0)]
    baldir_arka = [(t_, max(0, -v) * 1.3 + 4) for t_, v in dongu(*yur, 26, 0.5)] + [(T_VARIS, 2), (T_UC, 2), (T_UC + 26, 34), (T_DIN, 24), (T_YERE, 26), (T_YERE + 12, 0), (OP - 1, 0)]
    # kollar (omuz açısı: 0 = aşağı; 180 = yukarı)
    kol_on = ekle(dongu(*yur, -24, 0), (T_VARIS, 0),
                  (T_SIL, 150), (T_SIL + 26, 150), (T_DIREK, 0), (T_DIREK + 14, -40), (T_CAK - 8, 160), (T_CAK, 120), (T_CAK + 12, 40),
                  (T_GURUR, -45), (T_RUZGAR, -45), (T_RUZGAR + 10, 60), (T_TUT, 175), (T_DIN, 178), (T_YERE, 160), (T_YERE + 10, 20),
                  (T_SAPKA + 10, 20), (T_SON - 10, 150), (OP - 1, 150))
    kol_arka = ekle(dongu(*yur, -24, 0.5), (T_VARIS, 0), (T_GURUR, 45), (T_RUZGAR, 45), (T_RUZGAR + 10, -40), (T_TUT, -178), (T_DIN, -176),
                    (T_YERE, -150), (T_YERE + 10, -20), (OP - 1, -20))
    dirsek_on = [(0, -16), (T_VARIS, -10), (T_SIL, -100), (T_SIL + 26, -100), (T_DIREK, -10), (T_CAK - 8, -20), (T_CAK + 12, -10),
                 (T_GURUR, 110), (T_RUZGAR, 110), (T_RUZGAR + 10, 0), (T_TUT, 0), (T_YERE + 10, -20), (T_SON - 10, -60), (OP - 1, -60)]
    dirsek_arka = [(0, -16), (T_VARIS, -10), (T_GURUR, -110), (T_RUZGAR, -110), (T_RUZGAR + 10, 0), (T_TUT, 0), (T_YERE + 10, 20), (OP - 1, 20)]
    govde_r = [(0, 10), (T_VARIS - 10, 10), (T_VARIS + 6, 0), (T_SIL + 10, -6), (T_SIL + 30, 0), (T_GURUR, -8), (T_RUZGAR, -8),
               (T_RUZGAR + 10, 8), (T_TUT, 0), (T_YERE, 0), (T_YERE + 14, 6), (T_SAPKA + 6, 0), (T_SON, -6), (OP - 1, -6)]
    bas_r = [(0, 4), (T_VARIS, 0), (T_SIL + 6, -10), (T_SIL + 26, 6), (T_GURUR, -12), (T_RUZGAR, -12), (T_RUZGAR + 8, 14), (T_TUT, 0),
             (T_UC, -6), (T_DIN, 6), (T_YERE + 10, -10), (T_YERE + 20, 10), (T_YERE + 30, -8), (T_SAPKA, 0), (T_SAPKA + 8, 8), (T_SON, -6), (OP - 1, -6)]

    def R_(k): return A([(t_, [v]) for t_, v in sorted(k, key=lambda x: x[0])])

    TEN, SAC, GOMLEK, PANT, BOT, CANTA = "#F2C39B", "#5B3A29", "#FF7A45", "#3B5BA9", "#3A2E28", "#8B5E3C"

    def uzuv(nm, parent, p, rot, uz, renk, kal, uc=None, uc_renk=None, z=None):
        sh = [grp(path([(0, 0), (0, uz)], False), stroke(renk, kal))]
        if uc is not None:
            sh.insert(0, grp(uc, fill(uc_renk)))
        lay = L(nm, sh, ks(p=p, r=R_(rot)))
        lay["parent"] = parent
        return lay

    # katman sırası: önce çizilen en üstte. Ön kol, baş, gövde, ön bacak, arka bacak, arka kol
    # --- ön kol
    on_ust = uzuv("on_kol_ust", None, (2, -17), kol_on, 8, GOMLEK, 4.6)
    on_alt = uzuv("on_kol_alt", None, (0, 8), dirsek_on, 7.5, TEN, 3.6, uc=el(4.6, 4.6, (0, 8)), uc_renk=TEN)
    # --- arka kol
    ar_ust = uzuv("arka_kol_ust", None, (-2, -17), kol_arka, 8, "#E0663A", 4.6)
    ar_alt = uzuv("arka_kol_alt", None, (0, 8), dirsek_arka, 7.5, "#E5AE86", 3.6, uc=el(4.6, 4.6, (0, 8)), uc_renk="#E5AE86")
    # --- gövde (kalçada döner)
    govde = L("govde", [
        grp(rc(13, 21, 5, p=(0, -10.5)), fill(GOMLEK)),
        grp(path([(-6, -6), (6, -6)], False), stroke("#E0663A", 1.6)),                       # gömlek dikişi
        grp(rc(13, 4, 2, p=(0, -1.5)), fill("#2C2C2C")),                                     # kemer
        grp(rc(3, 3, 1, p=(1, -1.5)), fill("#D8B24C")),                                      # toka
        grp(path([(-3, -20), (-6, -2)], False), stroke("#6B4428", 1.8)),                    # çanta askısı
        grp(rc(9, 15, 3, p=(-9, -11)), fill(CANTA)), grp(rc(8, 5, 2, p=(-9.5, -5)), fill("#A06E46")),  # sırt çantası
        grp(rc(2, 10, 1, p=(-13, -12)), fill("#6B4428")),
    ], ks(r=R_(govde_r)))
    govde["parent"] = ri
    # --- baş
    kirp = [70, 160, 236, 322, 450]
    agiz_k = [(0, gul(2.5, 0.6, 4)), (T_VARIS, gul(2.5, 0.6, 4)),
              (T_SIL + 4, h.shp([(-2, 4), (2, 4), (0, 6)], True, [[0, 0], [0, 0], [1.5, 0]], [[0, 0], [0, 0], [-1.5, 0]])),   # üfleme
              (T_SIL + 30, gul(3, 1.6, 4)), (T_GURUR, gul(3, 1.6, 4)), (T_GURUR + 8, gul(4.5, 3.2, 3.6)), (T_RUZGAR, gul(4.5, 3.2, 3.6)),
              (T_RUZGAR + 8, h.shp([(-2.6, 4.5), (2.6, 4.5), (0, 8.5)], True, [[0, -2.5], [0, 0], [2.4, 0]], [[0, 0], [0, -2.5], [-2.4, 0]])),  # "O"
              (T_DIN, h.shp([(-2.6, 4.5), (2.6, 4.5), (0, 8.5)], True, [[0, -2.5], [0, 0], [2.4, 0]], [[0, 0], [0, -2.5], [-2.4, 0]])),
              (T_YERE + 6, gul(3, -0.8, 5)),               # dalgalı şaşkın
              (T_SAPKA + 8, gul(3, 2, 4)), (T_SON - 8, h.shp([(-4.5, 3.5), (4.5, 3.5), (0, 9)], True, [[0, 0], [0, 0], [3.4, 0]], [[0, 0], [0, 0], [-3.4, 0]])),
              (OP - 1, h.shp([(-4.5, 3.5), (4.5, 3.5), (0, 9)], True, [[0, 0], [0, 0], [3.4, 0]], [[0, 0], [0, 0], [-3.4, 0]]))]
    kas_k = [(0, shp([(-2.6, 0), (2.6, -0.8)], False)), (T_VARIS, shp([(-2.6, 0), (2.6, -0.8)], False)),
             (T_GURUR, shp([(-2.6, -0.6), (2.6, -0.6)], False)), (T_RUZGAR + 6, shp([(-2.6, -2), (2.6, -2.4)], False)),
             (T_YERE + 30, shp([(-2.6, -2), (2.6, -2.4)], False)), (T_SAPKA + 6, shp([(-2.6, -0.6), (2.6, -0.6)], False)), (OP - 1, shp([(-2.6, -0.6), (2.6, -0.6)], False))]
    goz_buyu = h.SC([(0, 100), (T_RUZGAR, 100), (T_RUZGAR + 6, 130), (T_DIN + 20, 130), (T_DIN + 30, 100), (OP - 1, 100)])
    bas = L("bas", [
        grp(agiz_k and grp(h.morph(agiz_k), stroke("#6B2E1F", 1.4), fill("#B5483A", OP_([(0, 0), (T_SIL + 2, 0), (T_SIL + 4, 100), (T_SIL + 26, 100), (T_SIL + 28, 0),
                                                                                            (T_RUZGAR + 6, 0), (T_RUZGAR + 8, 100), (T_DIN, 100), (T_DIN + 4, 0),
                                                                                            (T_SON - 10, 0), (T_SON - 8, 100)]))), t=tr(p=(3, 0))),
        grp(goz(0, 0, kirp, 1.6), t=tr(p=(4, -2), s=goz_buyu)),
        grp(h.morph(kas_k), stroke(SAC, 1.3), t=tr(p=(4, -5.4))),
        h.yanak(5.5, 3, 55),
        grp(el(3, 3.4, (8.4, 0.6)), fill("#E7A986")),                                          # burun
        grp(el(3.4, 4.4, (-4.6, 0.4)), fill("#E7A986")),                                       # kulak
        grp(path([(-8, -3), (-6, -8), (0, -9.5), (6, -8), (7, -5), (2, -6), (-3, -4.5), (-6, -1)]), fill(SAC)),  # saç
        grp(el(16, 17), fill(TEN)),
        grp(el(5, 5), fill(TEN), t=tr(p=(0, 8))),                                               # boyun
    ], ks(p=(1, -22), r=R_(bas_r)))
    bas["parent"] = govde["ind"] if govde.get("ind") else None
    # --- bacaklar (kalçadan)
    on_uyluk = uzuv("on_uyluk", ri, (2, 0), uyluk_on, 9, PANT, 5)
    on_baldir = uzuv("on_baldir", None, (0, 9), baldir_on, 9, PANT, 4.4, uc=rc(8, 4, 2, p=(2, 9.5)), uc_renk=BOT)
    ar_uyluk = uzuv("arka_uyluk", ri, (-2, 0), uyluk_arka, 9, "#304C8F", 5)
    ar_baldir = uzuv("arka_baldir", None, (0, 9), baldir_arka, 9, "#304C8F", 4.4, uc=rc(8, 4, 2, p=(2, 9.5)), uc_renk="#2C2320")

    # şapka (başa bağlı): rüzgârda uçar, sonda gökten başına düşer
    sapka_p = h.P([(0, (0, -9)), (T_RUZGAR + 10, (0, -9)), (T_RUZGAR + 50, (70, -60)), (T_RUZGAR + 51, (0, -140)), (T_SAPKA - 12, (0, -140)),
                   (T_SAPKA, (0, -9)), (T_SAPKA + 4, (0, -7)), (T_SAPKA + 8, (0, -9)), (OP - 1, (0, -9))])
    sapka = L("sapka", [grp(rc(11, 3, 1.5, p=(4, 0)), fill("#D93A3A")), grp(path([(-7, 0), (-6, -6), (0, -8), (6, -6), (7, 0)]), fill("#EF4B4B")),
                        grp(el(2.4, 2.4, (0, -8)), fill("#FFFFFF"))],
              ks(p=sapka_p, r=A([(0, [0]), (T_RUZGAR + 10, [0]), (T_RUZGAR + 50, [400]), (T_RUZGAR + 51, [-30]), (T_SAPKA, [0]), (OP - 1, [0])]),
                 s=h.SC([(0, 100), (T_SAPKA - 2, 100), (T_SAPKA, (115, 80)), (T_SAPKA + 8, 100)])))

    # baş dönmesi yıldızları (başa bağlı, çevresinde döner)
    yildizlar = []
    for j in range(3):
        k = []
        for s_ in range(0, 46, 3):
            a = j * 2.094 + s_ * 0.28
            k.append((T_YERE + s_, (12 * math.cos(a), -14 + 4 * math.sin(a))))
        yl = L(f"donme{j}", [grp(star(2.8, 1.2), fill("#FFC93C"))],
               ks(p=h.P(k, LIN), o=OP_([(0, 0), (T_YERE, 0), (T_YERE + 2, 100), (T_YERE + 40, 100), (T_YERE + 46, 0)])))
        yildizlar.append(yl)

    # sıralı ekleme + ebeveynler
    def koy(lay, parent):
        Ls.append(lay)
        if parent is not None:
            lay["parent"] = parent
        return lay["ind"]
    # ind değerleri L() çağrısında verildi; sıra listede belirler
    Ls.extend(yildizlar)
    Ls.append(sapka)
    Ls.append(on_alt); Ls.append(on_ust)
    Ls.append(bas)
    Ls.append(govde)
    Ls.append(on_baldir); Ls.append(on_uyluk)
    Ls.append(ar_baldir); Ls.append(ar_uyluk)
    Ls.append(ar_alt); Ls.append(ar_ust)
    gid = govde["ind"]
    for y in yildizlar: y["parent"] = bas["ind"]
    sapka["parent"] = bas["ind"]
    bas["parent"] = gid
    on_ust["parent"] = gid; ar_ust["parent"] = gid
    on_alt["parent"] = on_ust["ind"]; ar_alt["parent"] = ar_ust["ind"]
    on_baldir["parent"] = on_uyluk["ind"]; ar_baldir["parent"] = ar_uyluk["ind"]

    # ------------------------------------------------ dünya ögeleri
    # ter damlası
    ter = L("ter", [grp(path([(0, -3), (2, 1), (0, 3), (-2, 1)], True, [[0, 0], [0, -1], [1.2, 0], [0, 1]], [[0, 0], [0, 1], [-1.2, 0], [0, -1]]), fill("#7FC4FF"))],
            ks(p=h.P([(120, (78, 78)), (150, (82, 88)), (T_SIL - 4, (zx + 6, zy - 24)), (T_SIL + 14, (zx + 12, zy - 12))]),
               o=OP_([(0, 0), (120, 0), (124, 100), (146, 100), (150, 0), (T_SIL - 4, 0), (T_SIL, 100), (T_SIL + 14, 0)])))
    # nefes bulutçuğu
    nefes = L("nefes", [grp(el(5), fill("#FFFFFF")), grp(el(4, 4, (4, -2)), fill("#FFFFFF")), grp(el(3, 3, (8, -1)), fill("#FFFFFF"))],
              ks(p=h.P([(T_SIL + 4, (zx + 9, zy - 17)), (T_SIL + 30, (zx + 24, zy - 24))], OUTE), o=OP_([(0, 0), (T_SIL + 3, 0), (T_SIL + 6, 90), (T_SIL + 30, 0)]),
                 s=h.SC([(T_SIL + 4, 40), (T_SIL + 30, 140)])))
    # bayrak direği: çantadan çıkar, havada döner, toprağa çakılır
    direk_p = h.P([(0, (zx - 8, zy - 12)), (T_DIREK, (zx - 8, zy - 12)), (T_DIREK + 16, (zx - 2, zy - 50)), (T_CAK - 8, (DIREK_X, zy - 44)),
                   (T_CAK, (DIREK_X, zy - 2)), (T_CAK + 4, (DIREK_X, zy)), (OP - 1, (DIREK_X, zy))], h.IO)
    bez0 = shp([(0, 0), (9, 2), (18, 0), (18, 11), (9, 13), (0, 11)], True, [[0, 0], [-4, 0], [0, 0], [0, 0], [4, 0], [0, 0]], [[0, 0], [4, 0], [0, 0], [0, 0], [-4, 0], [0, 0]])
    bez1 = shp([(0, 0), (9, -2), (18, 2), (18, 13), (9, 9), (0, 11)], True, [[0, 0], [-4, 0], [0, 0], [0, 0], [4, 0], [0, 0]], [[0, 0], [4, 0], [0, 0], [0, 0], [-4, 0], [0, 0]])
    bez_k = [(0, bez0)]
    t = T_CAK + 10; j = 0
    while t < OP - 2:
        hiz = 5 if T_UC <= t < T_DIN else 16
        bez_k.append((t, bez1 if j % 2 else bez0)); t += hiz; j += 1
    bez = grp(h.morph(bez_k), fill("#FF4D4F"), grp(star(2.6, 1.1), fill("#FFFFFF"), t=tr(p=(8, 6))),
              t=tr(p=(1, -36), s=h.SC([(0, (0, 100)), (T_CAK + 6, (0, 100)), (T_CAK + 24, (100, 100)), (T_UC, (100, 100)), (T_UC + 8, (125, 86)), (T_DIN, (125, 86)), (T_DIN + 14, (100, 100))])))
    direk = L("direk", [bez, grp(path([(0, 0), (0, -36)], False), stroke("#6B4F3A", 2.4)), grp(el(3.4, 3.4, (0, -37)), fill("#FFC93C"))],
              ks(p=direk_p, r=A([(0, [-70]), (T_DIREK, [-70]), (T_DIREK + 16, [-200]), (T_CAK - 8, [-350]), (T_CAK, [-360]),
                                 (T_UC, [-360]), (T_UC + 20, [-352]), (T_DIN - 20, [-354]), (T_DIN, [-360]), (OP - 1, [-360])]),
                 o=OP_([(0, 0), (T_DIREK - 1, 0), (T_DIREK, 100)])))
    # toz bulutu
    tozlar = []
    for j, (dx, dy) in enumerate([(-12, -4), (-6, -9), (6, -9), (12, -4)]):
        tozlar.append(L(f"toz{j}", [grp(el(6), fill("#D9CBB4"))],
                        ks(p=h.P([(T_CAK, (DIREK_X, zy)), (T_CAK + 24, (DIREK_X + dx, zy + dy))], OUTE), o=OP_([(0, 0), (T_CAK, 0), (T_CAK + 1, 90), (T_CAK + 24, 0)]),
                           s=h.SC([(T_CAK, 30), (T_CAK + 24, 140)]))))
    # gurur parıltısı
    parilti = [L(f"parilti{j}", [grp(star(3.4, 1.2, 4), fill("#FFE066"))],
                 ks(p=(zx + dx, zy - 24 + dy), o=OP_([(0, 0), (T_GURUR + j * 6, 0), (T_GURUR + 4 + j * 6, 100), (T_GURUR + 26 + j * 6, 0)]),
                    s=h.SC([(T_GURUR + j * 6, 30), (T_GURUR + 14 + j * 6, 120), (T_GURUR + 26 + j * 6, 40)]), r=A([(T_GURUR, [0]), (T_GURUR + 40, [90])])))
               for j, (dx, dy) in enumerate([(-12, -4), (14, -10), (2, -18)])]
    # rüzgâr çizgileri ve savrulan yapraklar
    ruzgar = []
    for j in range(7):
        y = 30 + j * 13
        for rep in range(5):
            t0 = T_RUZGAR + j * 5 + rep * 28
            if t0 > T_DIN - 10: continue
            dalga = shp([(0, 0), (16, -3), (32, 0)], False, [[0, 0], [-5, 0], [0, 0]], [[0, 0], [5, 0], [0, 0]])
            ruzgar.append(L(f"r{j}_{rep}", [grp(h.morph([(t0, dalga)]), stroke("#FFFFFF", 2.2), trim(A([(t0, [0]), (t0 + 10, [100])])))],
                            ks(p=h.P([(t0, (-30, y)), (t0 + 30, (170, y + 4))], LIN), o=OP_([(0, 0), (t0, 0), (t0 + 2, 90), (t0 + 24, 90), (t0 + 30, 0)]))))
    for j in range(6):
        t0 = T_UC + j * 18
        ruzgar.append(L(f"yaprak{j}", [grp(path([(0, -4), (3, 0), (0, 4), (-3, 0)], True, [[0, 0], [0, -2], [0, 0], [0, 2]], [[0, 0], [0, 2], [0, 0], [0, -2]]), fill(["#5CB85C", "#F0A030", "#E8684A"][j % 3]))],
                        ks(p=h.P([(t0, (-10, 40 + (j * 23) % 70)), (t0 + 50, (170, 30 + (j * 31) % 80))], LIN), r=A([(t0, [0]), (t0 + 50, [720])], LIN),
                           o=OP_([(0, 0), (t0, 0), (t0 + 2, 100), (t0 + 46, 100), (t0 + 50, 0)]))))
    # geri geri savrulan kuş (kanat çırpar ama geri gider)
    kanat0 = shp([(-6, 0), (0, 2), (6, 0)], False, [[0, 0], [-3, 0], [0, 0]], [[0, 0], [3, 0], [0, 0]])
    kanat1 = shp([(-6, -4), (0, 2), (6, -4)], False, [[0, 0], [-3, 0], [0, 0]], [[0, 0], [3, 0], [0, 0]])
    kk = []; t = T_UC + 10; j = 0
    while t < T_UC + 110:
        kk.append((t, kanat1 if j % 2 else kanat0)); t += 4; j += 1
    kus = L("kus", [grp(h.morph(kk), stroke("#374151", 1.8)), grp(el(3, 3, (0, 2)), fill("#374151"))],
            ks(p=h.P([(T_UC + 10, (140, 26)), (T_UC + 60, (110, 30)), (T_UC + 110, (-20, 40))]),
               r=A([(T_UC + 10, [0]), (T_UC + 70, [-20]), (T_UC + 110, [-200])]),
               o=OP_([(0, 0), (T_UC + 9, 0), (T_UC + 10, 100), (T_UC + 106, 100), (T_UC + 110, 0)])))

    # ------------------------------------------------ zemin
    kar = L("kar", [grp(path([(zx, zy + 6), (zx - 10, zy + 20), (zx - 3, zy + 16), (zx + 3, zy + 22), (zx + 10, zy + 15), (zx + 16, zy + 18), (zx + 22, zy + 10)]), fill("#FFFFFF"))], ks())
    dag = L("dag", [grp(path([(-4, 160), (-4, 144), (10, 139), (34, 129), (54, 119), (72, 107), (86, 95), (zx, zy + 6), (zx + 30, zy + 8), (164, 150), (164, 160)],
                             True), fill("#7E9CCB")),
                    grp(path([(4, 150), (34, 131)], False), stroke("#6C89B8", 2)),
                    grp(path([(120, 120), (140, 140)], False), stroke("#6C89B8", 2))], ks())
    dag2 = L("dag2", [grp(path([(-10, 160), (20, 118), (44, 136), (70, 104), (110, 160)]), fill("#B4C8E6"))], ks())
    gunes = L("gunes", [grp(el(22), fill("#FFE17A")), grp(el(34), fill("#FFF0B8", 60))], ks(p=(30, 30), s=h.SC([(0, 100), (300, 108), (599, 100)])))
    bulutlar = []
    for j, (y, x0, d) in enumerate([(24, 70, 26), (48, 120, 18), (36, -10, 30)]):
        b = [grp(el(14), fill("#FFFFFF"), t=tr(p=(-6, 0))), grp(el(18), fill("#FFFFFF"), t=tr(p=(4, -3))), grp(rc(26, 8, 4, p=(0, 4)), fill("#FFFFFF"))]
        bulutlar.append(L(f"bulut{j}", b, ks(p=h.P([(0, (x0, y)), (T_RUZGAR, (x0 + d * 0.4, y)), (T_DIN, (x0 + d * 0.4 + 70, y)), (OP - 1, (x0 + d * 0.4 + 80, y))], LIN), o=S(90))))
    gok = L("gok", [grp(rc(160, 160), fill("#DDEFFF"))], ks(p=(80, 80)))
    perde = L("perde", [grp(rc(160, 160), fill("#DDEFFF"))], ks(p=(80, 80), o=OP_([(0, 100), (12, 0), (OP - 14, 0), (OP - 1, 100)])))

    dunya_ust = [perde] + ruzgar + [kus, ter, nefes] + parilti + tozlar
    dunya_alt = [direk, kar, dag, dag2] + bulutlar + [gunes, gok]
    karakter = Ls
    return dunya_ust + karakter + dunya_alt
