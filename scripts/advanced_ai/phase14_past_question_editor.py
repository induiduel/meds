#!/usr/bin/env python3
"""Faz 14 — Çıkmış soru redaksiyon önerileri.

Kaynaktaki çıkmış soruyu değiştirmez. Yerel model, yalnızca kaynak metinde
desteklenen OCR/biçim düzeltmelerini ve müfredat etiket önerilerini üretir.
Her sonuç, inceleme ve açık onay için ayrı JSONL katmanına yazılır.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / "scripts" / "agents"
sys.path.insert(0, str(AGENTS))
import lib  # noqa: E402

SOURCE = ROOT / "data" / "pastQuestions.json"
OUT = ROOT.parent / "meds_database_v2" / "phase14_past_question_editor"
REVIEWS = OUT / "reviews.jsonl"
STATE = OUT / "checkpoint.json"
REPORT = OUT / "report.json"
LOG_FILE = ROOT.parent / "meds_temp" / "logs" / "phase14.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
MODEL = lib.MODEL_TEXT

def log_msg(msg: str):
    t_str = time.strftime("%H:%M:%S")
    formatted = f"{t_str} [INFO] {msg}"
    print(formatted, flush=True)
    try:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

SYSTEM = """Sen tıp fakültesi sınav sorularını ve klinik metinleri inceleyen uzman bir redaksiyon (düzeltme) asistanısın.
GÖREVİN:
1. Soru kökünde ve şıklardaki yazım hatalarını, fazla harfleri (örn: 'hhafif', 'tromboooz'), eksik harfleri (örn: 'patloji' -> 'patoloji', 'glomerlr' -> 'glomerüler'), harf/rakam karışıklıklarını (0->O, 1->I) ve birleşik/ayrık yazılan kelimeleri tespit et ve kusursuz tıbbi Türkçe/Latince imlaya göre düzelt.
2. Tıbbi terminolojiyi (anatomi, fizyoloji, patoloji, farmakoloji, dahiliye terimleri) doğrula, yanlış yazılmış tıp terimlerini düzelt.
3. Tıbbi bilgi uydurma, klinik sorunun anlamını veya doğru şıkkını sebepsizce değiştirme.
4. Kaynakta desteklenmeyen veya belirsiz durumlar için review_required: true döndür.
5. Soru kökü veya şıklarda harf eksikliği/fazlalığı veya imla hatası düzeltildiğinde degisen_alanlar içine ekle ve degisiklik_ozeti içinde somut olarak belirt.
6. Yanıtın YALNIZCA geçerli bir JSON olmalı."""


def canonical_options(question: dict) -> dict[str, str]:
    raw = question.get("options") or (question.get("reconstruction") or {}).get("options") or {}
    if isinstance(raw, dict):
        return {str(k).upper(): str(v) for k, v in raw.items() if str(k).upper() in "ABCDE"}
    if isinstance(raw, list):
        result = {}
        for i, item in enumerate(raw[:5]):
            key = "ABCDE"[i]
            result[key] = str(item.get("text", "")) if isinstance(item, dict) else str(item)
        return result
    return {}


def source_view(question: dict) -> dict:
    rec = question.get("reconstruction") or {}
    return {
        "id": question.get("id"),
        "soru_koku": question.get("stem") or question.get("rawQuestion", {}).get("stem") or rec.get("stem") or "",
        "secenekler": canonical_options(question),
        "dogru_secenek": question.get("correctAnswer") or question.get("claimedAnswer") or rec.get("answer") or "",
        "aciklama": question.get("explanation") or rec.get("explanation") or "",
        "kurul_adi": question.get("committeeId") or "",
        "ders_adi": question.get("discipline") or "",
        "konu_adi": question.get("topic") or "",
    }


def content_hash(value: dict) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def token_set(value: str) -> set[str]:
    return set(lib.tokens(value))


def support_ratio(original: dict, proposal: dict) -> float:
    before = " ".join([original["soru_koku"], original["aciklama"], *original["secenekler"].values()])
    after = " ".join([str(proposal.get("soru_koku") or ""), str(proposal.get("aciklama") or ""),
                      *[str(v) for v in (proposal.get("secenekler") or {}).values()]])
    new_tokens = token_set(after) - token_set(before)
    return round(1 - len(new_tokens) / max(1, len(token_set(after))), 3)


CURRICULUM_FILE = ROOT / "curriculum" / "kbu_tip_donem3_curriculum.json"


def load_curriculum_summary() -> str:
    if not CURRICULUM_FILE.exists():
        return ""
    try:
        data = json.loads(CURRICULUM_FILE.read_text(encoding="utf-8"))
        comms = data.get("committees", {})
        lines = []
        for code, info in comms.items():
            name = info.get("name", "")
            deps = ", ".join(info.get("departments", [])[:5])
            lines.append(f"- {code} ({name}): Branşlar: {deps}")
        return "\n".join(lines)
    except Exception:
        return ""


def prompt(source: dict, curriculum_summary: str = "") -> str:
    curriculum_hint = f"\nRESMİ MÜFREDAT KURULLARI:\n{curriculum_summary}\n" if curriculum_summary else ""
    return f"""Aşağıdaki kaynak soruyu detaylıca incele:
1. SORU KÖKÜ VE ŞIKLARDAKİ YAZIM HATALARI, FAZLA VEYA EKSİK HARFLERİ TESPİT ET:
   - Soru kökündeki harf düşmelerini (örn: 'özellkle' -> 'özellikle', 'hastalk' -> 'hastalık', 'etkisiyle' -> 'etkisi ile') düzelt.
   - Fazladan basılmış harfleri veya OCR tekrarlarını (örn: 'aaşağıdakilerden', 'belirtidirr') temizle.
   - Rakam/harf ve OCR gürültülerini (0/O, 1/I/l, bozuk Türkçe karakterler ş, ğ, ı, ö, ü) düzelt.
   - Şıklardaki bitişik yazılmış kelimeleri ayır ('hastanıntetkikinde' -> 'hastanın tetkikinde'), imla ve Latince terminoloji hatalarını düzelt.
2. EKSİK ŞIKLARI TAMAMLAMA:
   - Soruda 5 şık (A, B, C, D, E) tam olmalıdır. Eksik şık varsa soru kökünün ölçtüğü klinik bilgiye uygun mantıklı tıp çeldiricileri üreterek 5 şıkkı tamamla.
   - Tamamlanan şıkların harflerini "yapay_zeka_tamamlanan_siklar" alanında belirt (örn: ["E"] veya ["D", "E"]).
3. Tıbbi içeriğin özünü ve klinik sorunun yönünü değiştirme.
4. Açıklama kaynakta varsa yazımını toparla, eksik veya anlamsızsa tıbbi gerekçesiyle düzenle.
5. Kurul/ders/konu için kaynakta mevcut etiketleri koru; emin değilsen boş bırak ve inceleme iste.
{curriculum_hint}
KAYNAK:
{json.dumps(source, ensure_ascii=False, indent=2)}

ŞU JSON ŞEMASINI DÖNDÜR:
{{
  "soru_koku": "Yazım hataları, eksik/fazla harfleri düzeltilmiş soru kökü",
  "secenekler": {{"A":"", "B":"", "C":"", "D":"", "E":""}},
  "dogru_secenek": "A/B/C/D/E veya kaynak değer",
  "yapay_zeka_tamamlanan_siklar": ["E"],
  "aciklama": "Kaynak açıklaması ve gerekiyorsa imla/tıbbi gerekçe düzeltmesi",
  "kurul_adi": "kaynak değeri veya müfredat kodu",
  "ders_adi": "kaynak değeri veya branş",
  "konu_adi": "kaynak değeri veya konu başlığı",
  "degisen_alanlar": ["soru_koku" ve/veya değişen diğer alanlar],
  "degisiklik_ozeti": "Düzeltilen harf hatası, fazla/eksik harf veya kelime düzeltmelerinin somut özeti",
  "review_required": true
}}"""


def load_done(full: bool) -> set[str]:
    if full or not STATE.exists():
        return set()
    try:
        return set(json.loads(STATE.read_text(encoding="utf-8")).get("done_ids") or [])
    except Exception:
        return set()


def save_state(done: set[str]) -> None:
    lib.write_json(STATE, {"done_ids": sorted(done), "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S")})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10, help="Bu çalıştırmada incelenecek en fazla soru")
    parser.add_argument("--full", action="store_true", help="Daha önce incelenenleri de yeniden değerlendir")
    args = parser.parse_args()
    if not SOURCE.exists():
        print(f"Kaynak bulunamadı: {SOURCE}", file=sys.stderr)
        return 1

    raw = json.loads(SOURCE.read_text(encoding="utf-8"))
    questions = raw if isinstance(raw, list) else raw.get("questions", [])
    OUT.mkdir(parents=True, exist_ok=True)
    done = load_done(args.full)
    curr_summary = load_curriculum_summary()
    stats = {"aday": len(questions), "islenen": 0, "degisiklik_onerisi": 0, "inceleme_gerekli": 0, "hata": 0}

    with REVIEWS.open("a", encoding="utf-8") as output:
        for question in questions:
            question_id = str(question.get("id") or "")
            if not question_id or question_id in done or stats["islenen"] >= args.limit:
                continue
            source = source_view(question)
            if len(source["soru_koku"].strip()) < 15 or len(source["secenekler"]) < 4:
                continue
            try:
                proposal = lib.chat(MODEL, prompt(source, curr_summary), system=SYSTEM, as_json=True, timeout=180, num_predict=1800)
                if not isinstance(proposal, dict):
                    raise ValueError("Model geçerli JSON nesnesi döndürmedi")
                ratio = support_ratio(source, proposal)
                changed = [str(x) for x in proposal.get("degisen_alanlar") or []]
                review_required = bool(proposal.get("review_required", True)) or ratio < 0.80
                record = {
                    "question_id": question_id,
                    "source_hash": content_hash(source),
                    "processed_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "model": MODEL,
                    "source": source,
                    "proposal": proposal,
                    "support_ratio": ratio,
                    "status": "review_required" if review_required else "unchanged",
                }
                output.write(json.dumps(record, ensure_ascii=False) + "\n")
                output.flush()
                stats["islenen"] += 1
                stats["degisiklik_onerisi"] += int(bool(changed))
                stats["inceleme_gerekli"] += int(review_required)
                done.add(question_id)
                save_state(done)
                log_msg(f"✓ Soru #{question_id}: {record['status']} (kanıt: {ratio})")
            except Exception as exc:  # model ya da ağ hatası bir sonraki soruyu durdurmaz
                stats["hata"] += 1
                log_msg(f"✗ Soru #{question_id} hata: {exc}")
            time.sleep(1)

    lib.write_json(REPORT, {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), **stats,
                            "cikti": str(REVIEWS), "kaynak": str(SOURCE)})
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
