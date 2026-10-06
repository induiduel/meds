#!/usr/bin/env python3
"""
Faz 12 — Ders notu temizleme (OCR/glif/yazım hataları) — kural tabanlı, doğrulanabilir, yapay zekâ metin üretmez.

Ölçülen hata türleri (2026-10-06, 22.612 materyal chunk'ı):
  * Sembol/Wingdings özel alan glifleri (U+F0xx): PowerPoint madde işaretleri ve Symbol yazı tipi Yunan harfleri
    ("\\uf062-laktamaz" = β-laktamaz)  → bağlama göre "•" ya da Yunan harfi
  * Görsel üzerindeki OCR çöpü ("N LA * — R, » . iğ | ~ me")  → satır düzeyinde sözlük-kelime oranıyla atılır
  * Bitişik harfler (ﬁ, ﬂ), bozuk kodlama (Ã¼…)  → ftfy + NFKC
  * URL / "Sıra No" / yalnız sayfa numarası / kaynakta tekrarlayan üst-alt bilgi satırları
  * Satır sonu tirelemesi ("hasta-\\nlık"), kopmuş kelimeler ("k nuşma"), nadir yazım hataları
Yazım düzeltmesi (SymSpell, materyal sözlüğü) VARSAYILAN KAPALI: elle denetimde Türkçe çekimleri bozdu
(çözünüp→çözünür, Atomik→Atopik). MEDS_FAZ12_SPELL=1 ile açılabilir. Silinen her satır kayda yazılır (silinen_satirlar).
OCR çöpü satır kuralı sayısal tıbbi bilgiyi korur (≤5 mm, 0,5 mg/kg, 18q21.2, %48-54, HbA1c).
Güvenlik: temizlenmiş metin özgün harflerin < %50'sini koruyorsa "şüpheli" — özgün metin korunur.
Kaynak chunk'lar DEĞİŞTİRİLMEZ. Çıktı: $MEDS_DATABASE_DIR/derived/clean_notes/<source_id>.jsonl, rapor.json,
ornekler.json (önce/sonra, elle denetim için). Artımlı: chunk metni değişmediyse yeniden işlenmez (--full: hepsi).
"""
from __future__ import annotations

import collections
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase8_curriculum_graph as P8  # noqa: E402

OUT = P8.DB / "derived" / "clean_notes"
WORD = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşüâîûÂÎÛ]+")

# Symbol yazı tipi (U+F000 + ASCII) → Yunan harfleri / işaretler
SYMBOL_GREEK = {0x61: "α", 0x62: "β", 0x67: "γ", 0x64: "δ", 0x65: "ε", 0x6B: "κ", 0x6C: "λ", 0x6D: "μ", 0x70: "π",
                0x73: "σ", 0x74: "τ", 0x66: "φ", 0x77: "ω", 0x71: "θ", 0x44: "Δ", 0x57: "Ω", 0xB3: "≥", 0xA3: "≤",
                0xAE: "→", 0xAC: "←", 0xAD: "↑", 0xAF: "↓", 0xB1: "±", 0xB4: "×", 0xB0: "°"}
WING_ARROWS = {0xE0: "→", 0xE8: "→", 0xDF: "←", 0xE1: "↑", 0xE2: "↓", 0xF0: "⇒"}
JUNK_LINE = re.compile(r"(https?://\S+|www\.\S+|s[ıi]nav\.karab\S*|^\s*S[ıi]ra No\s*$|^\s*\d{1,3}\s*$|^\s*Sayfa \d+\s*$)", re.I)
BULLETS = "•▪‣➢❖⚫◆■□●○◦✓✔➤►▸"
LIGATURES = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st"}


def fold(w: str) -> str:
    return P8.fold(w)


def fix_glyph(m: re.Match, text: str) -> str:
    ch = m.group(0)
    code = ord(ch) - 0xF000
    prev = text[m.start() - 1] if m.start() > 0 else " "
    nxt = text[m.end()] if m.end() < len(text) else " "
    # Yunan harfi bağlamı: kelimenin içinde ya da hemen ardından tire/harf/rakam ("β-laktamaz", "TNF-α", "IL-1β")
    if code in SYMBOL_GREEK and (nxt in "-–" or prev in "-–" or (prev.isalnum() and not prev.isspace())):
        return SYMBOL_GREEK[code]
    if code in WING_ARROWS:
        return WING_ARROWS[code]
    if code in SYMBOL_GREEK and code >= 0xA0:
        return SYMBOL_GREEK[code]
    return "• "                                       # madde işareti


class Cleaner:
    def __init__(self, vocab: collections.Counter):
        from symspellpy import SymSpell, Verbosity
        self.v = vocab
        self.stems = collections.Counter()
        for w, c in vocab.items():
            if len(w) >= 5:
                self.stems[w[:5]] += c
        self.Verbosity = Verbosity
        self.sym = SymSpell(max_dictionary_edit_distance=1, prefix_length=7)
        for w, c in vocab.items():
            if c >= 20 and len(w) >= 4:
                self.sym.create_dictionary_entry(w, c)
        self.stats = collections.Counter()
        # Yazım düzeltmesi KAPALI: denetimde Türkçe çekimleri bozdu (çözünüp→çözünür, Atomik→Atopik, Tromboplastik→Tromboplastin)
        self.spell = os.environ.get("MEDS_FAZ12_SPELL") == "1"

    def known(self, w: str) -> bool:
        """Türkçe ekler yüzünden birebir biçim nadir olabilir ("sokmasıyla"): 5 harf kökü de sayılır."""
        f = fold(w)
        return self.v.get(f, 0) >= 3 or (len(f) >= 5 and self.stems.get(f[:5], 0) >= 5)

    def word_ratio(self, line: str) -> float:
        toks = WORD.findall(line)
        if not toks:
            return 0.0
        good = sum(len(t) for t in toks if len(t) >= 2 and self.known(t))
        return good / max(1, sum(len(t) for t in toks))

    MEDICAL_SYM = set("|_.,;:%-–+/()[]°<>≤≥=±×~'\"’‘“”*&#•→←↑↓αβγδεκλμπσφωθΔΩ²³⁹⁰¹⁴⁵⁶⁷⁸")
    NUMERIC_INFO = re.compile(r"\d+[.,]?\d*\s*(%|mg|g|kg|ml|mL|dl|L|mm|cm|µ|μ|mmHg|IU|U|saat|gün|hafta|yıl|ay|°)|[%≤≥<>±]\s*\d|\d+\s*[-–]\s*\d+|\b\d+[pq]\d|HbA1c|\bIL-?\d", re.I)

    def is_junk(self, s: str) -> bool:
        """OCR çöpü mü? Sayısal/ölçü bilgisi (≤5 mm, 0,5 mg/kg, 18q21.2, %48-54) KORUNUR."""
        if len(s) < 6:
            return len(s.strip(BULLETS + " ")) == 0
        if self.NUMERIC_INFO.search(s) and self.word_ratio(s) >= 0.2 or (self.NUMERIC_INFO.search(s) and len(WORD.findall(s)) <= 2):
            return False
        if re.fullmatch(r"[\w\s]*\d+\s*(,\s*[\dXYxy]+\s*){2,}[\w\s,]*", s):   # "13, 18, 21, X, Y"
            return False
        if re.search(r"\b(?:[A-Z][a-z]?\d{0,3}){3,}\b", s) and re.search(r"[A-Z][a-z]?\d", s) and len(s) < 40:
            return False                                      # kimyasal formül: NH4C5H3N4O3, HCO3
        odd = sum(1 for ch in s if not ch.isalnum() and not ch.isspace() and ch not in self.MEDICAL_SYM)
        toks = WORD.findall(s)
        if not toks:
            return odd > 0 or not any(ch.isdigit() for ch in s)
        short = sum(1 for t in toks if len(t) <= 2) / len(toks)
        avg = sum(len(t) for t in toks) / len(toks)
        wr = self.word_ratio(s)
        if odd / len(s) > 0.2 and wr < 0.6:
            return True
        # çöp örüntüsü: kısa parçalar yığını ve sözlük dışı ("v mek eyi e am! iğ", "Wa a e NA. e")
        if len(toks) >= 3 and wr < 0.35 and (short > 0.4 or avg < 3.5):
            return True
        if len(toks) >= 5 and short > 0.65:
            return True
        return False

    def clean(self, text: str, header_lines: set) -> tuple[str, collections.Counter]:
        st = collections.Counter()
        removed = self.removed = []
        t = text
        try:
            import ftfy
            if re.search(r"[ÃÄÅ][\x80-\xbf±ŸŞ§¼¶]", t):          # yalnız bozuk kodlama (mojibake) şüphesi varsa
                t2 = ftfy.fix_encoding(t)
                if t2 != t:
                    st["kodlama"] += 1
                    t = t2
        except Exception:
            pass
        # Yalnız bitişik harfler; NFKC kullanılmaz (cm² → cm2, 10⁹ → 109 gibi tıbbi bilgiyi bozar)
        n = sum(t.count(k) for k in LIGATURES)
        if n:
            for k, v in LIGATURES.items():
                t = t.replace(k, v)
            st["bitisik_harf"] += n
        t = unicodedata.normalize("NFC", t)
        n = len(re.findall(r"[-]", t))
        if n:
            t = re.sub(r"[-]", lambda m: fix_glyph(m, t), t)
            st["glif"] += n
        # satır sonu tirelemesi: "hasta-\nlık" → "hastalık" (birleşik kelime sözlükte varsa)
        def dehyph(m):
            w = m.group(1) + m.group(2)
            if self.known(w):
                st["tire"] += 1
                return w
            return m.group(0)
        t = re.sub(r"([A-Za-zçğıöşüÇĞİÖŞÜ]{2,})-\s*\n\s*([a-zçğıöşü]{2,})", dehyph, t)
        out_lines = []
        for line in t.split("\n"):
            s = line.strip()
            if not s:
                continue
            if JUNK_LINE.search(s) and len(WORD.findall(JUNK_LINE.sub("", s))) < 3:
                st["url_sayfa_no"] += 1
                continue
            if s in header_lines:
                st["ust_alt_bilgi"] += 1
                continue
            if re.search(r"(?:\b\w ){4,}\w\b", s):           # "E L E K T R O L İ T" → "ELEKTROLİT"
                s2 = re.sub(r"(?:\b\w ){4,}\w\b", lambda m: m.group(0).replace(" ", ""), s)
                if s2 != s:
                    st["aralikli_harf"] += 1
                    s = s2
            if self.is_junk(s):
                st["ocr_cop_satir"] += 1
                if len(removed) < 12:
                    removed.append(s[:160])
                continue
            s = re.sub(r"\s*[©®¢¥§»«]+\s*", " ", s)
            s = self.fix_words(s, st)
            s = re.sub(r"^([" + BULLETS + r"]\s*)+", "• ", s)
            s = re.sub(r"[ \t]{2,}", " ", s).strip()
            if s:
                out_lines.append(s)
        return "\n".join(out_lines), st

    def fix_words(self, s: str, st: collections.Counter) -> str:
        toks = re.split(r"(\s+)", s)
        # kopmuş kelime: "k nuşma" → "konuşma" yerine yalnız güvenli birleştirme: iki parça bilinmiyor, birleşimi çok sık
        i = 0
        while i + 2 < len(toks):
            a, b = toks[i], toks[i + 2]
            if WORD.fullmatch(a or "") and WORD.fullmatch(b or "") and not self.known(a) and not self.known(b):
                j = fold(a + b)
                if self.v.get(j, 0) >= 10:
                    toks[i:i + 3] = [a + b]
                    st["kopuk_kelime"] += 1
                    continue
            i += 1
        out = []
        for tok in toks:
            m = WORD.fullmatch(tok or "")
            if self.spell and m and len(tok) >= 5 and self.v.get(fold(tok), 0) <= 1:
                sug = self.sym.lookup(fold(tok), self.Verbosity.TOP, max_edit_distance=1)
                if sug and sug[0].distance == 1 and sug[0].count >= 20:
                    rep = self.restore_case(tok, sug[0].term)
                    if rep:
                        out.append(rep)
                        st["yazim"] += 1
                        continue
            out.append(tok)
        return "".join(out)

    @staticmethod
    def restore_case(orig: str, folded: str) -> str | None:
        """Katlanmış öneriyi özgün kelimenin Türkçe harfleriyle geri kur (yalnız uzunluk aynıysa güvenli)."""
        if len(folded) != len(orig):
            return None
        tr_map = {"c": "ç", "g": "ğ", "i": "ı", "o": "ö", "s": "ş", "u": "ü"}
        res = []
        for o, f in zip(orig, folded):
            if fold(o) == f:
                res.append(o)
            else:
                c = f
                if o.isupper():
                    c = c.upper()
                res.append(c)
        return "".join(res)


def main():
    full = "--full" in sys.argv
    t0 = time.time()
    sources = P8.load_sources()
    chunks_by_src = P8.load_chunks()
    dumps = {s for s, src in sources.items() if P8.is_exam_dump(src, chunks_by_src)}
    vocab = collections.Counter()
    for sid, cs in chunks_by_src.items():
        if sid in dumps:
            continue
        for c in cs:
            for w in WORD.findall(c.get("text") or ""):
                vocab[fold(w)] += 1
    cl = Cleaner(vocab)
    OUT.mkdir(parents=True, exist_ok=True)
    total = collections.Counter()
    examples = []
    changed = suspicious = processed = skipped = 0
    for sid, cs in chunks_by_src.items():
        if sid in dumps:
            continue
        outp = OUT / f"{sid}.jsonl"
        prev = {}
        if outp.exists() and not full:
            for r in P8.read_jsonl(outp):
                prev[r["chunk_id"]] = r
        # kaynakta tekrarlayan kısa satırlar (üst/alt bilgi): sayfaların ≥ %40'ında aynı satır
        line_pages = collections.Counter()
        for c in cs:
            for ln in {x.strip() for x in (c.get("text") or "").split("\n") if 3 <= len(x.strip()) <= 60}:
                line_pages[ln] += 1
        n_pages = max(1, len(cs))
        headers = {ln for ln, k in line_pages.items() if n_pages >= 5 and k / n_pages >= 0.4 and not ln.startswith("[")}
        rows = []
        for c in cs:
            text = c.get("text") or ""
            h = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
            p = prev.get(c.get("chunk_id"))
            if p and p.get("ozgun_hash") == h:
                rows.append(p)
                skipped += 1
                continue
            new, st = cl.clean(text, headers)
            processed += 1
            orig_letters = sum(ch.isalpha() for ch in text)
            new_letters = sum(ch.isalpha() for ch in new)
            keep_ratio = new_letters / max(1, orig_letters)
            q0, q1 = cl.word_ratio(text), cl.word_ratio(new)
            durum = "temiz"
            if keep_ratio < 0.5 and orig_letters > 80:
                durum, new = "supheli_icerik_kaybi", text
                suspicious += 1
            elif new != text:
                changed += 1
            total.update(st)
            rows.append({"chunk_id": c.get("chunk_id"), "source_id": sid, "sayfa": c.get("page"), "ozgun_hash": h,
                         "metin": new, "durum": durum, "duzeltmeler": dict(st), "silinen_satirlar": list(cl.removed), "korunan_harf": round(keep_ratio, 3),
                         "kelime_orani_once": round(q0, 3), "kelime_orani_sonra": round(q1, 3)})
            if st and len(examples) < 400 and durum == "temiz" and sum(st.values()) >= 2:
                examples.append({"kaynak": sources.get(sid, {}).get("name"), "sayfa": c.get("page"),
                                 "once": text[:500], "sonra": new[:500], "duzeltmeler": dict(st)})
        tmp = outp.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        os.replace(tmp, outp)
    # ---- Sitenin ders notu ekranı (data/lecture_notes.json): değişen sayfalar ayrı katmana yazılır, özgün dosya korunur
    ln_path = P8.ROOT / "data" / "lecture_notes.json"
    overlay, ln_stats = {}, collections.Counter()
    if ln_path.exists():
        try:
            notes = json.load(open(ln_path, encoding="utf-8"))
        except Exception:
            notes = []
        for note in notes if isinstance(notes, list) else []:
            pages = note.get("pages") or []
            lines = collections.Counter()
            for pg in pages:
                for ln in {x.strip() for x in (pg.get("content") or "").split("\n") if 3 <= len(x.strip()) <= 60}:
                    lines[ln] += 1
            headers = {ln for ln, k in lines.items() if len(pages) >= 5 and k / len(pages) >= 0.4}
            for pg in pages:
                text = pg.get("content") or ""
                if not text:
                    continue
                new, st = cl.clean(text, headers)
                keep = sum(ch.isalpha() for ch in new) / max(1, sum(ch.isalpha() for ch in text))
                if new != text and (keep >= 0.5 or sum(ch.isalpha() for ch in text) <= 80):
                    overlay.setdefault(note.get("id"), {})[str(pg.get("pageNumber"))] = new
                    ln_stats.update(st)
                    ln_stats["sayfa"] += 1
        if overlay:
            tmp = OUT / "lecture_notes_overlay.json.tmp"
            json.dump({"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "notlar": overlay}, open(tmp, "w", encoding="utf-8"),
                      ensure_ascii=False)
            os.replace(tmp, OUT / "lecture_notes_overlay.json")
    import random
    random.seed(12)
    json.dump(random.sample(examples, min(40, len(examples))), open(OUT / "ornekler.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    rep = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "islenen_chunk": processed, "degismeyen_atlandi": skipped,
           "degisen": changed, "supheli_ozgun_korundu": suspicious, "duzeltmeler": dict(total),
           "sozluk_kelime": sum(1 for c in vocab.values() if c >= 3),
           "site_ders_notu": {"not": len(overlay), **dict(ln_stats)}, "sure_sn": round(time.time() - t0, 1)}
    json.dump(rep, open(OUT / "rapor.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
