"""Soru/şık ayrıştırma — deterministik (CPU, ücretsiz). LLM yedeği ayrı ve isteğe bağlıdır.

Gerçek sınav çıktıları, amfi slayt soruları ve karışık metinlerden numaralı soruları ve A–E
şıklarını (satır içi ya da ayrı satır) ayıklar. "yanlıştır/değildir/hariç" sorularını işaretler.
"""
from __future__ import annotations

import re

from . import textnorm

__all__ = ["parse_questions", "parse_block", "parse_questions_llm"]

# Satır başındaki soru numarası: "12."  "12)"  "Soru 12)"  "97-Hangisi" (tire; yanında rakam olmasın)
_Q_START = re.compile(
    r"(?m)^[ \t]*(?:Soru[ \t]*)?(\d{1,4})[ \t]*(?:[\.\)][ \t]+|[-\u2013](?=[^\d\s])[ \t]*)"
)
# Şık işareti: harften hemen önce harf/rakam olmasın; işaretten sonra boşluk olmayabilir ("C)Fiksasyon").
_OPT = re.compile(r"(?<![\wÇĞİÖŞÜçğıöşü])([A-Ea-e])[ \t]*[\)\.][ \t]*")
_ANS = re.compile(r"(?i)(?:doğru[ \t]+cevap|cevap[ \t]+anahtar[ıi]|cevap|yanıt|answer)[ \t]*[:\-]?[ \t]*([A-E])\b")
_EXPL = re.compile(r"(?i)(?:açıklama|gerekçe|explanation)[ \t]*[:\-][ \t]*(.+)", re.S)
_NEG = re.compile(r"(?i)(yanlıştır|değildir|hariç|olmayan|hangisi\s+yanlış|yanlıştır\?)")
# Kök içinde soru kalıbı (şık listesi sondaki satırları kesmek için)
_QMARK = re.compile(r"(?i)(hangisi|hangisidir|hangileri|hangisinde|hangisine|\bnedir\b|\bnelerdir\b|\bnasıl\b|değildir|yanlıştır|doğrudur|hariç)")
_STEM_MIN = 8


def _keep_question_lines(lines: list[str]) -> str:
    """PDF satır kaydırmalarını birleştirir ama şık/cevap listesini atar.

    Soru kökü birden çok satıra sarılmış olabilir ("...sola sapmaya neden / olur?"). Cümle bitmeden
    gelen ve küçük harfle başlayan satırlar kökün devamıdır; cümle bittikten sonraki satırlar ise
    şık listesidir → kesilir."""
    lines = [ln for ln in (lines or []) if ln.strip()]
    if not lines:
        return ""
    kept = [lines[0]]
    for ln in lines[1:]:
        prev = kept[-1].rstrip()
        if prev and prev[-1] in ".?!:;":
            break
        if ln[:1].islower() or prev.endswith((",", "-", ";", ":")):
            kept.append(ln)
        else:
            break
    return "\n".join(kept)


def _option_sequence(text: str) -> list[re.Match]:
    """Metindeki şık işaretlerinden en uzun A→B→C… ardışık diziyi seçer."""
    marks = list(_OPT.finditer(text))
    best: list[re.Match] = []
    for start in marks:
        if start.group(1).upper() != "A":
            continue
        seq: list[re.Match] = []
        want = ord("A")
        for m in marks[marks.index(start):]:
            if m.group(1).upper() == chr(want):
                seq.append(m)
                want += 1
        if len(seq) > len(best):
            best = seq
    return best


def parse_block(text: str, no: int | None = None) -> dict:
    """Tek bir soru bloğunu kök + şıklar + cevap + açıklama olarak ayrıştırır."""
    text = (text or "").strip()
    seq = _option_sequence(text)
    options: dict[str, str] = {}
    if len(seq) >= 3:
        stem = text[: seq[0].start()]
        for i, m in enumerate(seq):
            end = seq[i + 1].start() if i + 1 < len(seq) else len(text)
            options[m.group(1).upper()] = textnorm.normalize_ws(text[m.end():end])
        tail = text[seq[-1].end():]
    else:
        stem = text
        tail = ""
        # Şık işareti yok: satır kaydırmalarını birleştir, şık/cevap listesini at.
        stem = _keep_question_lines(stem.split("\n"))

    answer = None
    m = _ANS.search(tail) or _ANS.search(stem)
    if m:
        answer = m.group(1).upper()

    explanation = None
    m = _EXPL.search(tail) or _EXPL.search(stem)
    if m:
        explanation = textnorm.normalize_ws(m.group(1))

    stem = textnorm.normalize_ws(stem)
    # Kökün sonunda kalan cevap/açıklama izlerini temizle
    stem = re.split(r"(?i)(?:açıklama|gerekçe)\s*[:\-]", stem)[0].strip()
    stem = _ANS.sub("", stem).strip()
    # Cevap/çözüm işareti ve emoji gürültüsünü at; ilk soru işaretinde kes (sonrası şık/cevap listesi olabilir)
    stem = re.split(r"(?i)(?:doğru\s+cevap|cevap\s+anahtar[ıi]|açıklama|gerekçe|cevap)\s*[:\-]", stem)[0]
    stem = stem.replace("✅", " ").replace("❑", " ").strip()
    if "?" in stem:
        stem = stem[: stem.index("?") + 1].strip()
    # Baştaki soru numarasını kökten çıkar ("76)en sık..." → "en sık...")
    stem = re.sub(r"^[ \t]*\d{1,4}[ \t]*[\)\.\-][ \t]*", "", stem).strip()

    return {
        "no": no,
        "stem": stem,
        "options": options,
        "answer": answer,
        "explanation": explanation,
        "soru_tipi": "negatif" if _NEG.search(stem) else "pozitif",
    }


def parse_questions(text: str) -> list[dict]:
    """Metni numaralı sorulara böler. Numara yoksa tek blok olarak dener."""
    text = textnorm.clean_text(text)
    matches = list(_Q_START.finditer(text))
    blocks: list[tuple[str, int | None]] = []
    if not matches:
        blocks.append((text, None))
    else:
        if matches[0].start() > 0:
            head = text[: matches[0].start()].strip()
            if head:
                blocks.append((head, None))
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            blocks.append((text[m.end():end], int(m.group(1))))

    out: list[dict] = []
    for block, no in blocks:
        q = parse_block(block, no)
        if q["stem"] and len(q["stem"]) >= _STEM_MIN:
            out.append(q)
    return out


def parse_questions_llm(text: str, *, max_tokens: int = 4096) -> list[dict]:
    """Deterministik ayrıştırmanın yetmediği durumlar için LLM yedeği (ücretsiz bulut).
    JSON döndürmeyi ister; şema doğrulaması çağıran tarafta yapılır."""
    from . import llm

    prompt = (
        "Aşağıdaki metinden çıkmış sınav sorularını çıkar. Her soru için JSON üret: "
        '{"sorular": [{"no": <int|null>, "stem": "<soru kökü>", "options": {"A": "...", "B": "...", '
        '"C": "...", "D": "...", "E": "..."}, "answer": "<A-E|null>"}]}. '
        "Metinde olmayan bilgi EKLEME; okuyamadığın yeri boş bırak. Yalnızca JSON döndür.\n\n" + text[:12000]
    )
    data = llm.chat_json(prompt, max_tokens=max_tokens)
    if not isinstance(data, dict):
        return []
    out = []
    for item in data.get("sorular") or []:
        if not isinstance(item, dict):
            continue
        stem = (item.get("stem") or "").strip()
        if len(stem) < _STEM_MIN:
            continue
        out.append({
            "no": item.get("no"),
            "stem": stem,
            "options": {k: str(v) for k, v in (item.get("options") or {}).items()},
            "answer": item.get("answer"),
            "explanation": None,
            "soru_tipi": "negatif" if _NEG.search(stem) else "pozitif",
        })
    return out
