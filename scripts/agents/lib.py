"""
MedSoru otomatik boru hattı — ortak kütüphane (tamamen yerel; bulut AI kullanmaz).

Süreç: PROJE_TANITIMI.md  (downloads -> temp1 -> temp2 -> temp3 -> database)
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import sys
import tempfile
import time
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # .../MedSoru Project
DOWNLOADS = Path(os.environ.get("MEDS_DOWNLOADS_DIR") or ROOT / "meds_downloads")

# Otomatik Disk Doluluk Koruma Mekanizması (%60 Eşiği):
# Ana disk (%60 veya üzeri) dolarsa veriler otomatik olarak /mnt/yedekler/meds_temp (126 GB boş) üzerine yönlendirilir.
def _resolve_temp_dir() -> Path:
    env_dir = os.environ.get("MEDS_TEMP_DIR")
    if env_dir:
        return Path(env_dir)
    try:
        import shutil
        total, used, free = shutil.disk_usage(ROOT)
        usage_pct = (used / total) * 100
        secondary_disk = Path("/mnt/yedekler/meds_temp")
        if usage_pct >= 60.0 and secondary_disk.parent.exists():
            secondary_disk.mkdir(parents=True, exist_ok=True)
            return secondary_disk
    except Exception:
        pass
    return ROOT / "meds_temp"

TEMP = _resolve_temp_dir()
DB = Path(os.environ.get("MEDS_DATABASE_DIR") or ROOT / "meds_database")
TEMP1, TEMP2, TEMP3 = TEMP / "temp1", TEMP / "temp2", TEMP / "temp3"
STATE_DIR = TEMP / "state"
REVIEW_DIR = TEMP / "review"
LOG_DIR = TEMP / "logs"
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")

# Yerel modeller (üst sınır 8B). Ortam değişkeniyle değiştirilebilir.
MODEL_TEXT = os.environ.get("MEDS_MODEL_TEXT", "gemma3:4b")        # Türkçe düzeltme / yapılandırma
MODEL_FAST = os.environ.get("MEDS_MODEL_FAST", "qwen3:1.7b-q8_0")  # ultra hızlı hafif düzeltme / birleştirme
MODEL_MED = os.environ.get("MEDS_MODEL_MED", "medgemma1.5:4b")     # tıbbi varlık / zenginleştirme
MODEL_EMBED = os.environ.get("MEDS_MODEL_EMBED", "bge-m3")         # çok dilli anlamsal arama
MODEL_VISION = os.environ.get("MEDS_VISION_MODEL", "qwen3-vl:8b")

for d in (STATE_DIR, REVIEW_DIR, LOG_DIR, TEMP2, TEMP3):
    d.mkdir(parents=True, exist_ok=True)


def is_ocr_garbage(text: str) -> bool:
    """Tıp slaytlarındaki radyoloji/grafik/mikroskop görüntülerinden çıkan OCR çöpünü tespit eder."""
    if not text or len(text.strip()) < 10:
        return True
    words = re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü]{2,}", text)
    if not words:
        return True
    meaningful = [w for w in words if len(w) >= 3]
    meaningful_ratio = len(meaningful) / max(1, len(words))
    avg_word_len = sum(len(w) for w in words) / max(1, len(words))
    noise_chars = sum(ch in '|~_—=-*#><{}[]\\/^«»`´’“”!?:;,\'\"' for ch in text)
    noise_ratio = noise_chars / max(1, len(text))
    short_words = sum(1 for w in words if len(w) <= 2)
    short_ratio = short_words / max(1, len(words))

    # Eşik kontrolleri
    if noise_ratio > 0.16:
        return True
    if avg_word_len < 3.0 and short_ratio > 0.55:
        return True
    if meaningful_ratio < 0.45:
        return True
    return False


# --------------------------------------------------------------------------- log
def get_logger(name: str) -> logging.Logger:
    lg = logging.getLogger(name)
    if not lg.handlers:
        lg.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S")
        fh = logging.FileHandler(LOG_DIR / "pipeline.log", encoding="utf-8")
        fh.setFormatter(fmt)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmt)
        lg.addHandler(fh)
        lg.addHandler(sh)
    return lg


# --------------------------------------------------------------------------- dosya yardımcıları
def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def write_json(path: Path, obj, indent: int | None = 1):
    """Atomik yazım: yarım dosya bırakmaz."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp_", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)
    os.replace(tmp, path)


def read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp_", suffix=".jsonl")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def read_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


class State:
    """Aşama bazlı artımlı işleme durumu: {aşama: {anahtar: {hash, ok, ts, hata}}}."""

    def __init__(self, name="pipeline_state"):
        self.path = STATE_DIR / f"{name}.json"
        self.data = read_json(self.path, {}) or {}

    def get(self, stage: str, key: str):
        return self.data.get(stage, {}).get(key)

    def done(self, stage: str, key: str, h: str, ok=True, err: str | None = None, **extra):
        self.data.setdefault(stage, {})[key] = {"hash": h, "ok": ok, "ts": time.time(), "err": err, **extra}
        self.data.pop("current_progress", None)
        write_json(self.path, self.data, indent=None)

    def set_progress(self, file_rel: str, current_step: int, total_steps: int, step_desc: str):
        pct = round((current_step / max(1, total_steps)) * 100, 1)
        self.data["current_progress"] = {
            "file": file_rel,
            "current": current_step,
            "total": total_steps,
            "percent": pct,
            "desc": step_desc,
            "ts": time.time()
        }
        write_json(self.path, self.data, indent=None)

    def add_transformation(self, file_rel: str, step_name: str, input_sample: str, output_sample: str):
        """Yapay zekanın neyi neye dönüştürdüğünü dashboard tablosunda göstermek için son 10 dönüşümü kaydeder."""
        history = self.data.setdefault("transform_history", [])
        history.append({
            "file": file_rel,
            "step": step_name,
            "input": input_sample[:300].strip(),
            "output": output_sample[:300].strip(),
            "ts": time.time()
        })
        # Son 10 dönüşümü sakla
        if len(history) > 10:
            self.data["transform_history"] = history[-10:]
        write_json(self.path, self.data, indent=None)

    def needs(self, stage: str, key: str, h: str, retry_failed_after: float = 6 * 3600) -> bool:
        e = self.get(stage, key)
        if not e or e.get("hash") != h:
            return True
        if not e.get("ok") and time.time() - e.get("ts", 0) > retry_failed_after:
            return True
        return False


# --------------------------------------------------------------------------- Ollama
def ollama_up() -> bool:
    import requests

    try:
        return requests.get(f"{OLLAMA_URL}/api/tags", timeout=5).ok
    except Exception:
        return False


def ollama_models() -> set[str]:
    import requests

    try:
        return {m["name"] for m in requests.get(f"{OLLAMA_URL}/api/tags", timeout=5).json()["models"]}
    except Exception:
        return set()


def is_gemma_running() -> bool:
    """Ollama üzerinde şu an aktif olarak çalışan modeller arasında gemma var mı kontrol eder."""
    import requests
    try:
        r = requests.get(f"{OLLAMA_URL}/api/ps", timeout=3)
        if r.ok:
            running = r.json().get("models", [])
            return any("gemma" in m.get("name", "").lower() for m in running)
    except Exception:
        pass
    return False


def chat(model: str, prompt: str, system: str | None = None, as_json: bool = False, timeout: int = 120,
         num_predict: int = 2048, retries: int = 1, num_ctx: int = 8192, num_gpu: int | None = None):
    """Yerel model çağrısı.
    Kural: Gemma aktif olarak çalışıyorsa diğer modeller %90 CPU / %10 GPU (num_gpu=3) ile çalışır.
    Gemma çalışmıyorsa diğer tüm modeller tam GPU hızında serbestçe çalışır.
    """
    import requests

    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    options = {"temperature": 0, "num_predict": num_predict, "num_ctx": num_ctx}

    # Dinamik GPU Yönetimi
    if num_gpu is not None:
        options["num_gpu"] = num_gpu
    elif "gemma" not in model.lower():
        # Model gemma harici bir model (örn: qwen, deepseek, medgemma vb.)
        if is_gemma_running():
            # Gemma çalışıyor -> VRAM çakışmasını önlemek için %90 CPU / %10 GPU
            options["num_gpu"] = 3
        else:
            # Gemma çalışmıyor -> GPU tamamen serbest, tam donanım hızlandırma!
            pass

    body = {"model": model, "messages": msgs, "stream": False, "think": False,
            "options": options}
    if as_json:
        body["format"] = "json"
    last = None
    for i in range(retries + 1):
        try:
            r = requests.post(f"{OLLAMA_URL}/api/chat", json=body, timeout=timeout)
            r.raise_for_status()
            out = r.json()["message"]["content"].strip()
            out = re.sub(r"^<unused\d+>\s*thought.*?(?=\n\n|\Z)", "", out, flags=re.S).strip() if "<unused" in out else out
            if as_json:
                try:
                    return json.loads(out)
                except Exception:
                    # JSON kısmen kesilmiş veya sonda fazladan virgül/bozukluk olabilir, kurtarmayı dene
                    cleaned = re.sub(r",\s*([\]}])", r"\1", out)
                    try:
                        return json.loads(cleaned)
                    except Exception:
                        # Kapanmamış süslü veya köşeli parantezleri kapatmayı dene
                        for suffix in ["}", "]}", '"]}', '""}', '"}]}']:
                            try:
                                return json.loads(cleaned + suffix)
                            except Exception:
                                pass
                        raise
            return out
        except Exception as e:  # noqa: BLE001
            last = e
            err_str = str(e).lower()
            if "connection" in err_str or "timed out" in err_str or "500" in err_str:
                import subprocess
                subprocess.run(["/usr/local/bin/meds-gpu-recovery"], capture_output=True)
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"Ollama çağrısı başarısız ({model}): {last}")


def embed(texts: list[str], model: str = MODEL_EMBED, batch: int = 16):
    import numpy as np
    import requests

    out = []
    for i in range(0, len(texts), batch):
        r = requests.post(f"{OLLAMA_URL}/api/embed", json={"model": model, "input": texts[i:i + batch]}, timeout=600)
        r.raise_for_status()
        out += r.json()["embeddings"]
    a = np.array(out, dtype="float32")
    n = np.linalg.norm(a, axis=1, keepdims=True)
    return a / np.maximum(n, 1e-9)


# --------------------------------------------------------------------------- Türkçe metin
_FOLD = str.maketrans("çğıöşüâîûÇĞİÖŞÜ", "cgiosuaiucgiosu")


def fold(s: str) -> str:
    s = s.replace("İ", "i").replace("I", "ı").lower().translate(_FOLD)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", s).split())


def tokens(s: str) -> list[str]:
    return [t for t in fold(s).split() if len(t) > 2 or t.isdigit()]


WORD_RE = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşüÂâÎîÛû]+")
# Yanlış kodlama (Windows-1254/ISO-8859-9 okuma hataları)
MOJIBAKE = {"ý": "ı", "þ": "ş", "ð": "ğ", "Ý": "İ", "Þ": "Ş", "Ð": "Ğ", "\u0131\u0307": "i", "\ufffd": "",
            "Ã¼": "ü", "Ã¶": "ö", "Ã§": "ç", "Ä±": "ı", "ÅŸ": "ş", "ÄŸ": "ğ", "Ä°": "İ", "Ãœ": "Ü", "Ã–": "Ö"}

_LEX: dict[str, int] | None = None
LEX_PATH = STATE_DIR / "lexicon.json"


def build_lexicon(texts) -> dict[str, int]:
    """Temiz metinlerden (ders notları) Türkçe kelime sıklığı. '!' gibi bozuk jeton içerenler alınmaz."""
    c: Counter = Counter()
    for t in texts:
        for w in WORD_RE.findall(nfc(t)):
            if len(w) >= 3:
                c[w.lower().replace("İ", "i").replace("I", "ı")] += 1
    lex = {w: n for w, n in c.items() if n >= 2}
    write_json(LEX_PATH, lex, indent=None)
    return lex


def lexicon() -> dict[str, int]:
    global _LEX
    if _LEX is None:
        _LEX = read_json(LEX_PATH, {}) or {}
    return _LEX


def reset_lexicon():
    global _LEX
    _LEX = None


_BACK = set("aıou")


def _bang_candidates(w: str):
    """'!' içeren kelime için i/ı adayları."""
    idx = [i for i, ch in enumerate(w) if ch == "!"]
    if len(idx) > 4:
        return []
    outs = [list(w)]
    for i in idx:
        nxt = []
        for o in outs:
            for rep in ("i", "ı"):
                c = o.copy()
                c[i] = rep
                nxt.append(c)
        outs = nxt
    return ["".join(o) for o in outs]


def tr_upper(s: str) -> str:
    return s.replace("i", "İ").replace("ı", "I").upper()


_TRI: Counter | None = None


def _trigrams() -> Counter:
    """Sözlükteki kelimelerden harf üçlüsü sıklıkları (i/ı seçimi için bağlam modeli)."""
    global _TRI
    if _TRI is None:
        _TRI = Counter()
        for w, n in lexicon().items():
            ww = f"^{w}$"
            for i in range(len(ww) - 2):
                _TRI[ww[i:i + 3]] += n
    return _TRI


def _pick_i(word_chars: list[str], pos: int) -> str:
    """pos'taki bozuk karakter için 'i' mi 'ı' mı: komşu harf üçlülerinin sözlük sıklığına göre."""
    tri = _trigrams()
    w = ["^"] + [("i" if c == "!" else c) for c in word_chars] + ["$"]
    k = pos + 1
    score = {}
    for rep in ("i", "ı"):
        w2 = w.copy()
        w2[k] = rep
        sc = 0
        for st in (k - 2, k - 1, k):
            if st >= 0 and st + 3 <= len(w2):
                sc += tri.get("".join(w2[st:st + 3]), 0)
        score[rep] = sc
    if score["i"] == score["ı"]:
        # son çare: ünlü uyumu (son ünlü art ünlüyse ı)
        prev = [c for c in word_chars[:pos] if c.lower() in "aeıioöuü"]
        return "ı" if prev and prev[-1].lower() in _BACK else "i"
    return max(score, key=score.get)


def _harmony_bang(w: str) -> str:
    chars = list(w)
    for i, c in enumerate(chars):
        if c == "!":
            chars[i] = _pick_i(chars, i)
    return "".join(chars)


_DIAC = {"c": "ç", "g": "ğ", "i": "ı", "o": "ö", "s": "ş", "u": "ü"}


def _diacritic_candidates(w: str, limit=3):
    pos = [i for i, ch in enumerate(w) if ch in _DIAC]
    if not pos or len(pos) > 8:
        return []
    outs = []
    # tek ve çift değişiklikler (üçlü patlamayı önlemek için sınırlı)
    import itertools

    for k in range(1, min(limit, len(pos)) + 1):
        for comb in itertools.combinations(pos, k):
            c = list(w)
            for p in comb:
                c[p] = _DIAC[c[p]]
            outs.append("".join(c))
        if len(outs) > 200:
            break
    return outs


def repair_text(text: str, deascii: bool = True) -> tuple[str, dict]:
    """Deterministik Türkçe onarım: mojibake, '!' (bozuk i/ı), kelime içi ASCII sadeleştirme.

    Hiçbir bilgi eklemez/çıkarmaz; yalnızca harf düzeltir. Değişiklik sayılarını döndürür.
    """
    lex = lexicon()
    stats = Counter()
    text = nfc(text)
    for k, v in MOJIBAKE.items():
        if k in text:
            stats["mojibake"] += text.count(k)
            text = text.replace(k, v)

    def bang(m):
        w = m.group(0)
        core = w.strip("!")
        if sum(ch.isalpha() for ch in core) < 2:
            return w  # "!!!" gibi gerçek noktalama
        low = w.lower()
        internal = "!" in core
        final_only = (not internal) and low.endswith("!") and not low.startswith("!")
        cands = _bang_candidates(low)
        in_lex = [c for c in cands if lex.get(c, 0) >= 2]
        if final_only and not in_lex:
            return w  # kelime sonu '!' sözlükle doğrulanamadı: gerçek ünlem olabilir
        best = max(in_lex, key=lambda c: lex[c]) if in_lex else _harmony_bang(low)
        stats["bang"] += 1
        if w.replace("!", "").isupper() and len(w) > 2:
            return tr_upper(best)
        if w[0].isupper():
            return ("İ" if best[0] == "i" else best[0].upper()) + best[1:]
        return best

    text = re.sub(r"[\wÇĞİÖŞÜçğıöşü]*![\wÇĞİÖŞÜçğıöşü!]*|[\wÇĞİÖŞÜçğıöşü]+!", bang, text)

    if deascii and lex:
        def dea(m):
            w = m.group(0)
            low = w.lower().replace("İ", "i").replace("I", "ı") if w[0] != "I" else w.lower()
            if len(low) < 4 or lex.get(low, 0) >= 2:
                return w
            # kelime tamamen ASCII ise ve sözlükte yoksa diakritikli varyantı dene
            cands = [c for c in _diacritic_candidates(low) if lex.get(c, 0) >= 3]
            if not cands:
                return w
            best = max(cands, key=lambda c: lex[c])
            if lex[best] < max(5, 5 * lex.get(low, 0)):
                return w
            stats["ascii"] += 1
            if w.isupper():
                return tr_upper(best)
            if w[0].isupper():
                return best[0].upper() + best[1:]
            return best

        text = re.sub(r"[A-Za-z]{4,}", dea, text)
    return text, dict(stats)


def clean_layout(text: str) -> str:
    """Biçim temizliği: boşluk, kesik satır sonları, sayfa numarası satırları, kontrol karakterleri."""
    t = text.replace("\r\n", "\n").replace("\x00", "")
    t = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f\u200b\u00ad\ufeff]", "", t)
    t = t.replace("\u00a0", " ")
    t = re.sub(r"(\w)-\n(\w)", r"\1\2", t)  # satır sonu tire
    lines = []
    for ln in t.split("\n"):
        ln = re.sub(r"[ \t]+", " ", ln).strip()
        if re.fullmatch(r"[-–—_=.\s]{1,}", ln) and len(ln) < 40:
            continue  # "_ _ _" gibi çöp çizgiler
        if re.fullmatch(r"(sayfa|page|slayt)?\s*\d{1,3}\s*(/\s*\d{1,3})?", ln, flags=re.I):
            continue  # yalnız sayfa numarası
        lines.append(ln)
    t = "\n".join(lines)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def quality_of(text: str) -> float:
    """0..1: harf oranı, bozuk karakter ve sözlük kapsaması."""
    if not text.strip():
        return 0.0
    n = len(text)
    letters = sum(ch.isalpha() for ch in text)
    bad = text.count("!") + text.count("\ufffd") + text.count("¿") + text.count("�")
    words = [w.lower() for w in WORD_RE.findall(text) if len(w) >= 3]
    lex = lexicon()
    cov = (sum(1 for w in words if lex.get(w, 0) >= 2) / len(words)) if (words and lex) else 0.7
    score = 0.45 * min(1.0, letters / max(1, n) / 0.6) + 0.35 * cov + 0.2 * (1 - min(1.0, bad / max(1, n) * 20))
    return round(max(0.0, min(1.0, score)), 3)


# --------------------------------------------------------------------------- kaynak meta
_MANIFEST = None


def _norm_rel(p: str) -> str:
    """İndirici her yol parçasını kırpıyor; manifest ile yerel yolu aynı biçime getir."""
    return nfc("/".join(x.strip() for x in p.split("/") if x.strip()))


def manifest_index() -> dict[str, dict]:
    """Yerel göreli yol -> manifest kaydı (drive_id, source_id...)."""
    global _MANIFEST
    if _MANIFEST is None:
        m = read_json(DOWNLOADS / "_manifest.json", {}) or {}
        idx = {}
        for it in m.get("items", []):
            if it.get("is_folder"):
                continue
            idx[_norm_rel(f"{it['root']}/{it['path']}")] = it
        _MANIFEST = idx
    return _MANIFEST


def source_id_for(rel_path: str) -> tuple[str, str | None]:
    """(source_id, drive_id). Şema: sha1(drive_id)[:12]. Manifest'te yoksa yola göre türetilir."""
    it = manifest_index().get(_norm_rel(rel_path))
    if it:
        return it.get("source_id") or hashlib.sha1(it["drive_id"].encode()).hexdigest()[:12], it["drive_id"]
    return hashlib.sha1(nfc(rel_path).encode()).hexdigest()[:12], None


def infer_meta(rel_path: str) -> dict:
    """Yoldan dönem/kurul/ders/doc_type çıkarımı (temp1 göreli yolu, uzantısız)."""
    p = nfc(rel_path)
    low = p.lower()
    meta = {"donem": 3, "kurul": None, "ders": None, "doc_type": "lecture_slide"}
    m = re.search(r"d[öo]nem\s*(\d)", low)
    if m:
        meta["donem"] = int(m.group(1))
    m = re.search(r"kurul\s*([1-6])", low)
    if m:
        meta["kurul"] = int(m.group(1))
    elif re.search(r"final|büt[üu]nleme|but[úu]nleme", low):
        meta["kurul"] = "final"
    parts = p.split("/")
    for i, part in enumerate(parts):
        if re.match(r"kurul\s*\d", part, re.I) and i + 1 < len(parts) - 1:
            meta["ders"] = parts[i + 1]
    if re.search(r"çıkmış|cikmis|sorular|kurul sınav|final|soru", low) or parts[0].startswith(("cikmis", "d3_cikmis")):
        meta["doc_type"] = "past_question"
    if "ders_programi" in low or "ders programı" in low:
        meta["doc_type"] = "schedule"
    return meta
