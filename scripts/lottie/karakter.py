"""Eklemli insan karakteri (Lottie katmanları). zirve_sahne.py'deki düzenin genel hâli.

G (boş): tutma/konum noktası, kalçanın 26 px (ölçek 80'de) üstü → R (boş): kalça → gövde → baş, kollar; R → bacaklar.
Açılar derece: kol 0 = aşağı sarkık, 180 = yukarı; uyluk 0 = aşağı, -90 = öne (oturma); baldır + bükülme.
"""

def _sirala(k):
    d = {}
    for t, v in k:
        d[int(round(t))] = v
    return sorted(d.items())

def insan(h, nm, G_p, eklem, agiz_k, kirp, renk=None, G_r=None, G_s=80, R_s=None, kas_k=None, sac="kisa",
          on_el=None, goz_buyu=None, agiz_ic=None, yanak_o=55):
    A, S, P, SC, OP_, L, NUL, grp, el, rc, path, shp, fill, stroke, tr, ks = (
        h.A, h.S, h.P, h.SC, h.OP_, h.L, h.NUL, h.grp, h.el, h.rc, h.path, h.shp, h.fill, h.stroke, h.tr, h.ks)
    r = {"ten": "#F2C39B", "ten2": "#E5AE86", "sac": "#5B3A29", "ust": "#5B8DEF", "ust2": "#4A78D6", "alt": "#3B4A6B", "alt2": "#323F5C",
         "ayak": "#3A2E28", **(renk or {})}
    def RK(k): return A([(t, [v]) for t, v in _sirala(k)])
    G = NUL(f"{nm}_G", ks(p=P(_sirala(G_p)), s=S([G_s, G_s, 100]), r=RK(G_r) if G_r else S(0)))
    R = NUL(f"{nm}_R", ks(p=(0, 32), s=SC(_sirala(R_s)) if R_s else None))
    R["parent"] = G["ind"]
    def uzuv(ad, p, k, uz, c, kal, uc=None, uc_c=None, ekstra=None):
        sh = [grp(path([(0, 0), (0, uz)], False), h.stroke(c, kal))]
        if uc is not None: sh.insert(0, grp(uc, fill(uc_c)))
        if ekstra: sh = ekstra + sh
        return L(f"{nm}_{ad}", sh, ks(p=p, r=RK(k)))
    on_ust = uzuv("onkol", (2, -17), eklem.get("kol_on", [(0, 0)]), 8, r["ust"], 4.6)
    on_alt = uzuv("ondirsek", (0, 8), eklem.get("dirsek_on", [(0, 0)]), 7.5, r["ten"], 3.6, el(4.6, 4.6, (0, 8)), r["ten"], ekstra=on_el)
    ar_ust = uzuv("arkakol", (-2, -17), eklem.get("kol_arka", [(0, 0)]), 8, r["ust2"], 4.6)
    ar_alt = uzuv("arkadirsek", (0, 8), eklem.get("dirsek_arka", [(0, 0)]), 7.5, r["ten2"], 3.6, el(4.6, 4.6, (0, 8)), r["ten2"])
    on_uy = uzuv("onuyluk", (2, 0), eklem.get("uyluk_on", [(0, 0)]), 9, r["alt"], 5)
    on_ba = uzuv("onbaldir", (0, 9), eklem.get("baldir_on", [(0, 0)]), 9, r["alt"], 4.4, rc(8, 4, 2, p=(2, 9.5)), r["ayak"])
    ar_uy = uzuv("arkauyluk", (-2, 0), eklem.get("uyluk_arka", [(0, 0)]), 9, r["alt2"], 5)
    ar_ba = uzuv("arkabaldir", (0, 9), eklem.get("baldir_arka", [(0, 0)]), 9, r["alt2"], 4.4, rc(8, 4, 2, p=(2, 9.5)), r["ayak"])
    govde = L(f"{nm}_govde", [grp(rc(13, 21, 5, p=(0, -10.5)), fill(r["ust"])), grp(path([(-5, -14), (0, -11), (5, -14)], False), stroke(r["ust2"], 1.4)),
                              grp(rc(13, 4, 2, p=(0, -1.5)), fill(r["alt2"]))], ks(r=RK(eklem.get("govde", [(0, 0)]))))
    saclar = {
        "kisa": [grp(path([(-8, -3), (-6, -8), (0, -9.5), (6, -8), (7, -5), (2, -6), (-3, -4.5), (-6, -1)]), fill(r["sac"]))],
        "atkuyrugu": [grp(path([(-8, -2), (-7, -8), (0, -10), (7, -8), (8, -4), (3, -6), (-2, -5), (-5, 0)]), fill(r["sac"])),
                      grp(el(7, 11, (-10, 0)), fill(r["sac"]), t=tr(r=A([(0, [-10]), (60, [10]), (120, [-10])]) if False else 0)),
                      grp(el(3, 3, (-7.5, -4)), fill("#FF5C8A"))],
    }
    yuz = [grp(grp(h.morph(_sirala(agiz_k)), stroke("#6B2E1F", 1.4), *( [fill("#B5483A", agiz_ic)] if agiz_ic else [])), t=tr(p=(3, 0))),
           grp(h.goz(0, 0, kirp, 1.6), t=tr(p=(4, -2), s=goz_buyu or S([100, 100]))),
           *( [grp(h.morph(_sirala(kas_k)), stroke(r["sac"], 1.3), t=tr(p=(4, -5.4)))] if kas_k else []),
           h.yanak(5.5, 3, yanak_o), grp(el(3, 3.4, (8.4, 0.6)), fill("#E7A986")), grp(el(3.4, 4.4, (-4.6, 0.4)), fill("#E7A986"))]
    bas = L(f"{nm}_bas", yuz + saclar[sac] + [grp(el(16, 17), fill(r["ten"])), grp(el(5, 5), fill(r["ten"]), t=tr(p=(0, 8)))],
            ks(p=(1, -22), r=RK(eklem.get("bas", [(0, 0)]))))
    bas["parent"] = govde["ind"]; govde["parent"] = R["ind"]
    on_ust["parent"] = govde["ind"]; ar_ust["parent"] = govde["ind"]
    on_alt["parent"] = on_ust["ind"]; ar_alt["parent"] = ar_ust["ind"]
    on_uy["parent"] = R["ind"]; ar_uy["parent"] = R["ind"]
    on_ba["parent"] = on_uy["ind"]; ar_ba["parent"] = ar_uy["ind"]
    katmanlar = [on_alt, on_ust, bas, govde, on_ba, on_uy, ar_ba, ar_uy, ar_alt, ar_ust, G, R]
    return katmanlar, {"G": G["ind"], "R": R["ind"], "bas": bas["ind"], "govde": govde["ind"], "on_el": on_alt["ind"]}
