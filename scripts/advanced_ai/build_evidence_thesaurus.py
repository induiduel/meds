#!/usr/bin/env python3
"""
Kanıtlı tıbbi sözlük — ders materyalinden (sınav dökümleri hariç) çıkarılır, yapay zekâ kullanılmaz.

Yöntemler (her eşleşme kaynak + sayfa + alıntı ile kaydedilir):
  1. kisaltma        : "Konjenital adrenal hiperplazi (KAH)" — Schwartz–Hearst: kısaltmanın harfleri önceki kelimelerin
                       içinde sırayla, ilk harf bir kelime başıyla eşleşmeli. Aynı kısaltmanın birden çok açılımı varsa
                       en sık açılım ≥ %70 değilse kısaltma "belirsiz" sayılır ve atılır. Materyalde çoğunlukla küçük harfle
                       yazılan (normal kelime olan) kısaltmalar atılır.
  2. parantez_esdeger: "Epinefrin (adrenalin)" — iki tarafı da 1–4 kelimelik terim; en az 2 FARKLI kaynakta görülmeli.
                       Elle kontrolde yalnızca ~%25'i gerçek eş anlamlı çıktı ("enfeksiyon (tüberküloz)" gibi örnekler):
                       güven "inceleme" — onaylanmadan kullanılmaz.
  3. yazim_varyanti  : helicobacter ~ helikobakter, nucleus ~ nukleus, atrophy ~ atrofi — Latince/İngilizce → Türkçe harf
                       dönüşümü (c→k, ph→f, y→i, th→t…) sonrası BİREBİR aynı kelimeler (≥ 6 harf, ikisi de ≥ 2 kez).
                       Türkçe ek farkları (sorunu/soruna) elenir.

Çıktı (normal sözlükten AYRI): meds_database_v2/evidence_thesaurus/
  * kanitli_sozluk.json     — medical_thesaurus.json ile aynı biçim (anahtar → {turkce, latin, esanlamlilar, ...})
                              + "kanit" ve "guven" alanları; doğrudan birleştirilebilir.
  * eklenecek_ciftler.jsonl — her satır bir terim–eş anlamlı çifti (tur, guven, siklik, kanitlar): tek tek gözden
                              geçirip ana sözlüğe eklemek için.
  * rapor.json
Ana sözlük (medical_thesaurus.json) DEĞİŞTİRİLMEZ. Boş sonuç mevcut dosyanın üzerine yazılmaz.
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase8_curriculum_graph as P8  # noqa: E402

OUT = P8.PROJECT / "meds_database_v2" / "evidence_thesaurus"
W = r"[A-Za-zÇĞİÖŞÜçğıöşüâîû][\wÇĞİÖŞÜçğıöşüâîû\-]*"
ABBR_RE = re.compile(rf"((?:{W}[ \t]+){{0,7}}{W})[ \t]*\([ \t]*([A-ZÇĞİÖŞÜ][A-Za-zÇĞİÖŞÜ0-9\-]{{1,9}})[ \t]*\)")
PAREN_RE = re.compile(rf"((?:{W}[ \t]+){{0,3}}{W})[ \t]*\([ \t]*((?:{W}[ \t]+){{0,3}}{W})[ \t]*\)")
STOPW = P8.STOP | set("ve veya ile ya da için gibi olan olarak bir bu şu çok daha en ilk ikinci tip grup örn örneğin "
                      "ise de da the of and or in to for with ilk tercih nadir sık sıklık".split())
UNITS = {"mg", "ml", "kg", "mm", "cm", "mmhg", "iu", "dl", "gr", "sn", "dk", "hz", "mv", "abd", "who", "dsö"}


def norm(t: str) -> str:
    return " ".join(str(t or "").replace("i̇", "i").replace("̇", "").split())


def translit_light(w: str) -> str:
    """Yalnızca harf dönüşümü (son ek silme yok): nucleus→nukleus, atrophy→atrofi, endometriyum→endometrium."""
    w = P8.fold(w)
    for a, b in (("ph", "f"), ("th", "t"), ("ch", "k"), ("ae", "e"), ("oe", "e"), ("rh", "r"), ("qu", "kv"),
                 ("x", "ks"), ("c", "k"), ("y", "i"), ("w", "v")):
        w = w.replace(a, b)
    return re.sub(r"(.)\1", r"\1", w)


def translit(w: str) -> str:
    """Latince/İngilizce yazımı Türkçe okunuşa yaklaştırır (yazım varyantı anahtarı)."""
    w = P8.fold(w)
    for a, b in (("ph", "f"), ("th", "t"), ("ch", "k"), ("ae", "e"), ("oe", "e"), ("rh", "r"), ("qu", "kv"),
                 ("x", "ks"), ("c", "k"), ("y", "i"), ("w", "v"), ("j", "c")):
        w = w.replace(a, b)
    w = re.sub(r"(.)\1", r"\1", w)          # çift harf
    w = re.sub(r"(us|um|is|ia|ae|a|e|i|u)$", "", w)  # Latince son ekler
    return w


def schwartz_hearst(words: list[str], abbr: str) -> list[str] | None:
    """Kısaltmanın en kısa açılımı (kelime listesinin sonundan)."""
    a = [c for c in P8.fold(abbr) if c.isalpha()]
    if len(a) < 2:
        return None
    fw = [P8.fold(w) for w in words]
    ai = len(a) - 1
    wi = len(fw) - 1
    ci = len(fw[wi]) - 1 if fw else -1
    while ai >= 0 and wi >= 0:
        word = fw[wi]
        found = False
        while ci >= 0:
            if word[ci] == a[ai] and (ai > 0 or ci == 0):
                found = True
                ci -= 1
                ai -= 1
                break
            ci -= 1
        if not found or ci < 0:
            if ai >= 0 and not found:
                wi -= 1
                ci = len(fw[wi]) - 1 if wi >= 0 else -1
                continue
            if ai >= 0:
                wi -= 1
                ci = len(fw[wi]) - 1 if wi >= 0 else -1
    if ai >= 0 or wi < 0:
        return None
    exp = words[wi:]
    # ilk harf kelime başı olmalı; açılım kısaltmadan uzun ve en fazla len(abbr)+3 kelime
    if not P8.fold(exp[0]).startswith(a[0]) or len(exp) > len(a) + 3 or len(exp) < 1:
        return None
    if len(exp) == 1 and len(P8.fold(exp[0])) <= len(a) + 1:
        return None
    if any(P8.fold(w) in STOPW for w in exp):  # "SAĞLAM OLANLARDAN NE KADARINI…" gibi cümle parçaları
        return None
    return exp


def is_term(s: str) -> bool:
    f = P8.fold(s)
    ws = f.split()
    return (1 <= len(ws) <= 4 and len(f) >= 4 and not any(w.isdigit() for w in ws)
            and ws[0] not in STOPW and ws[-1] not in STOPW)


def main():
    t0 = time.time()
    sources = P8.load_sources()
    chunks_by_src = P8.load_chunks()
    dumps = {s for s, src in sources.items() if P8.is_exam_dump(src, chunks_by_src)}
    material = [(sid, c) for sid, cs in chunks_by_src.items() if sid not in dumps for c in cs]
    name = {s: (src.get("name") or src.get("title") or s) for s, src in sources.items()}

    def ev(sid, c, m):
        t = c.get("text") or ""
        a, b = max(0, m.start() - 20), min(len(t), m.end() + 20)
        return {"source_id": sid, "kaynak": name.get(sid, sid), "sayfa": c.get("page"), "chunk_id": c.get("chunk_id"),
                "alinti": " ".join(t[a:b].split())}

    # ---- 1) kısaltmalar
    abbr_exp = collections.defaultdict(collections.Counter)
    abbr_ev = collections.defaultdict(list)
    case = collections.Counter()  # kısaltma: büyük harfli / küçük harfli görülme
    for sid, c in material:
        t = c.get("text") or ""
        for m in ABBR_RE.finditer(t):
            words, ab = m.group(1).split(), m.group(2)
            exp = schwartz_hearst(words, ab)
            if not exp:
                continue
            e = " ".join(exp)
            key = P8.fold(ab)
            abbr_exp[key][P8.fold(e)] += 1
            if len(abbr_ev[(key, P8.fold(e))]) < 3:
                abbr_ev[(key, P8.fold(e))].append({**ev(sid, c, m), "ifade": norm(e), "kisaltma": ab})
    corpus_text = "\n".join(c.get("text") or "" for _, c in material)
    for key in abbr_exp:
        for m in re.finditer(rf"(?<![\wçğıöşü]){re.escape(key)}(?![\wçğıöşü])", corpus_text, re.I):
            s = m.group(0)
            case["U" + key if any(ch.isupper() for ch in s) else "L" + key] += 1

    pairs = []  # (terim, es_anlamli, tur, guven, siklik, kanitlar)
    stats = collections.Counter()
    for key, cnt in abbr_exp.items():
        exp, n = cnt.most_common(1)[0]
        tot = sum(cnt.values())
        if key in UNITS or len(key) < 2:
            stats["kisaltma_birim_veya_kisa"] += 1
            continue
        if n / tot < 0.7:
            stats["kisaltma_belirsiz"] += 1
            continue
        lower, upper = case["L" + key], case["U" + key]
        if lower > 0.2 * (lower + upper):
            stats["kisaltma_normal_kelime"] += 1
            continue
        evs = abbr_ev[(key, exp)]
        disp = norm(evs[0]["kisaltma"]) if evs else key.upper()
        guven = "yuksek" if n >= 2 and len(key) >= 3 else "orta"
        pairs.append((norm(evs[0]["ifade"]) if evs else exp, disp, "kisaltma", guven, n, evs))
        stats["kisaltma_kabul"] += 1

    # ---- 2) parantez içi eşdeğerler (≥ 2 farklı kaynak)
    pc = collections.defaultdict(set)
    pev = collections.defaultdict(list)
    for sid, c in material:
        t = c.get("text") or ""
        for m in PAREN_RE.finditer(t):
            l_, r_ = m.group(1).split(), m.group(2)
            if r_.isupper() or not is_term(r_):
                continue
            # sol taraf: sağdakiyle aynı kelime sayısına yakın son kelimeler
            k = min(len(l_), max(1, len(r_.split())) + 1)
            for kk in range(1, k + 1):
                left = " ".join(l_[-kk:])
                if not is_term(left):
                    continue
                key = (P8.fold(left), P8.fold(r_))
                if key[0] == key[1] or set(key[0].split()) & set(key[1].split()):
                    continue
                pc[key].add(sid)
                if len(pev[key]) < 3:
                    pev[key].append({**ev(sid, c, m), "ifade": norm(left), "es": norm(r_)})
    for key, srcs in pc.items():
        if len(srcs) >= 2:
            e0 = pev[key][0]
            # elle kontrolde ~%25 doğru: yalnızca inceleme için kaydedilir, Faz 9 kullanmaz
            pairs.append((e0["ifade"], e0["es"], "parantez_esdeger", "inceleme", len(srcs), pev[key]))
            stats["parantez_kabul"] += 1

    # ---- 3) yazım varyantları
    vocab = collections.Counter()
    first_ev = {}
    for sid, c in material:
        for m in re.finditer(W, c.get("text") or ""):
            w = P8.fold(m.group(0))
            if len(w) >= 6 and not w.isdigit():
                vocab[w] += 1
                if w not in first_ev:
                    first_ev[w] = ev(sid, c, m)
    groups = collections.defaultdict(list)
    for w, n in vocab.items():
        if n >= 2:
            groups[translit(w)].append(w)
    for k, ws in groups.items():
        if len(ws) < 2 or len(k) < 5:
            continue
        ws.sort(key=lambda w: -vocab[w])
        head = ws[0]
        for other in ws[1:]:
            # aynı kelimenin Türkçe ekli hâllerini ele (kök farkı değil, harf farkı olmalı)
            if other.startswith(head) or head.startswith(other):
                continue
            # yalnızca saf yazım farkı: harf dönüşümü sonrası birebir aynı olmalı (Türkçe ek farkları elenir)
            if translit_light(head) != translit_light(other):
                stats["yazim_ek_farki_red"] += 1
                continue
            pairs.append((head, other, "yazim_varyanti", "yuksek" if vocab[other] >= 3 else "orta", vocab[other],
                          [first_ev[head], first_ev[other]]))
            stats["yazim_varyanti_kabul"] += 1

    if not pairs:
        print("Hiç çift bulunamadı; mevcut sözlük korunuyor.")
        return 1

    # ---- birleştir: medical_thesaurus.json biçimi
    entries: dict[str, dict] = {}
    for term, syn, tur, guven, n, evs in pairs:
        k = P8.fold(term)
        e = entries.setdefault(k, {"turkce": norm(term), "latin": "", "esanlamlilar": [], "anahtar_bilesenler": [],
                                    "kurul": None, "brans": None, "ozgulluk_agirligi": None,
                                    "kaynak": "kanitli_sozluk", "kanit": {}, "guven": {}})
        if syn not in e["esanlamlilar"]:
            e["esanlamlilar"].append(syn)
            e["kanit"][syn] = {"tur": tur, "siklik": n, "ornekler": evs[:2]}
            e["guven"][syn] = guven
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "kanitli_sozluk.json.tmp"
    json.dump(dict(sorted(entries.items())), open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, OUT / "kanitli_sozluk.json")
    with open(OUT / "eklenecek_ciftler.jsonl.tmp", "w", encoding="utf-8") as f:
        for term, syn, tur, guven, n, evs in sorted(pairs, key=lambda x: (x[2], -x[4])):
            f.write(json.dumps({"terim": term, "es_anlamli": syn, "tur": tur, "guven": guven, "siklik": n,
                                "kanitlar": evs[:2], "onay": None}, ensure_ascii=False) + "\n")
    os.replace(OUT / "eklenecek_ciftler.jsonl.tmp", OUT / "eklenecek_ciftler.jsonl")
    rep = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "materyal_chunk": len(material), "sinav_dokumu_kaynak": len(dumps),
           "terim": len(entries), "cift": len(pairs), **dict(stats),
           "guven": dict(collections.Counter(p[3] for p in pairs)), "sure_sn": round(time.time() - t0, 1)}
    json.dump(rep, open(OUT / "rapor.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
