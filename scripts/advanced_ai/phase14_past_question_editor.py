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

SYSTEM = """Sen tıp fakültesi kurul ve uzmanlık sınavları (TUS/USMLE) için soru denetleyen kıdemli bir tıp eğitimcisi ve redaksiyon asistanısın.
GÖREVİN: Dizgi/OCR hatalarını, eksik kökleri ve bilimsel tutarsızlıkları düzeltmek; metni tıp literatürüne (Robbins, Guyton, ATLS vb.) uyumlu, anlam kayması içermeyen ve kolay taranabilir temiz bir formata getirmek.

I. ANLAMSAL VE BİLİMSEL KORUMA
1. ANLAM KAYMASI YASAKTIR: Soru kökündeki veya şıklardaki zaman/öncelik belirteçlerine ("ilk yapılacak", "en sık", "kesin tanı", "başlangıç tedavisi", "en spesifik") ASLA dokunma. Şıkların savunduğu temel argümanı değiştirme; yalnızca terim kaymalarını ve dizgi hatalarını düzelt (örn: "Kaşık tüp" -> "Kaflı tüp" olur; "Kaşık tüp" -> "Cerrahi trakeostomi" olmaz, bu konsept değişimidir). Soru kökü olumsuzsa ("hangisi yanlıştır/değildir?") olumluya çevirme, 4 doğru-1 yanlış dengesini bozma.
2. MİNİMAL MÜDAHALE: Şıkları baştan yazma; sorunun ölçmek istediği patofizyolojik tuzağı/klinik ayrımı ve çeldiricileri koru. Soru kökü tamamen eksikse, mevcut şıkların tıp literatüründe en sık karşılaştırıldığı ortak klinik paydaya göre kökü tamamla ve bunu review_required ile işaretle.
3. ÖNCE ANALİZ, EN SON CEVAP: Doğru cevabı ilk adımda ilan etme. Önce her şıkkın bilimsel doğruluk/yanlışlık mekanizmasını analiz et, doğru cevabı en son, bağımsız bir sonuç olarak yaz. Kaynaktaki cevapla analizin vardığı sonuç çelişirse düzeltmeyi uygulama; review_required: true döndür.
4. Tıbbi bilgi uydurma; kaynakta desteklenmeyen veya belirsiz durumlar için review_required: true döndür.

II. GÖRSEL DÜZEN
1. Soru kökünde arka arkaya verilen klinik/laboratuvar verilerini tek uzun paragraf bırakma; klinik akışa göre satır atlayarak (\\n) parçala. Hedef soru cümlesi ayrı satırda olsun.
2. Açıklamada düz metin kullanma; mekanizmayı "Olay Örgüsü", "Neden-Sonuç İlişkisi" veya "Temel Klinik Kural" başlıklı maddelerle ("- ") sun.
3. Her şık ayrı ve kısa kalsın; gereksiz boşluk/tekrar bırakma.

III. YAZIM
Fazla/eksik harfleri (örn: 'hhafif', 'tromboooz', 'patloji' -> 'patoloji', 'glomerlr' -> 'glomerüler'), harf/rakam karışıklıklarını (0->O, 1->I), birleşik/ayrık yazılan kelimeleri tespit et ve kusursuz tıbbi Türkçe/Latince imlaya göre düzelt. Düzeltilen her alanı degisen_alanlar içine ekle, degisiklik_ozeti içinde somut belirt.

Yanıtın YALNIZCA geçerli bir JSON olmalı (markdown, kod bloğu veya ek metin yok)."""


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
1. SORU KÖKÜ VE MANTIĞI KESİNLİKLE KÖKLÜ DEĞİŞTİRİLEMEZ (ZORUNLU KORUMA):
   - Akademik literatüre uygun olarak soru kökünü köklü bir biçimde ASLA değiştirme!
   - Özellikle sorunun doğru cevabını ve doğru şıkkını değiştirecek/tersine çevirecek değişiklikler KESİNLİKLE YASAKTIR.
   - ÖRNEĞİN: 'Hangisi doğrudur?' sorusunu 'Hangisi doğru değildir?' veya 'Hangisi yanlıştır?' diye değiştirmek KESİNLİKLE YASAKTIR! Sorunun yönü (olumlu/olumsuz) ve cevabı daima korunmalıdır.
2. SORU KÖKÜ VE ŞIKLARDAKİ YAZIM HATALARI, FAZLA VEYA EKSİK HARFLERİ TESPİT ET:
   - Soru kökündeki harf düşmelerini (örn: 'özellkle' -> 'özellikle', 'hastalk' -> 'hastalık', 'etkisiyle' -> 'etkisi ile') düzelt.
   - Fazladan basılmış harfleri veya OCR tekrarlarını (örn: 'aaşağıdakilerden', 'belirtidirr') temizle.
   - Rakam/harf ve OCR gürültülerini (0/O, 1/I/l, bozuk Türkçe karakterler ş, ğ, ı, ö, ü) düzelt.
   - Şıklardaki bitişik yazılmış kelimeleri ayır ('hastanıntetkikinde' -> 'hastanın tetkikinde'), imla ve Latince terminoloji hatalarını düzelt.
3. EKSİK ŞIKLARI TAMAMLAMA:
   - Soruda 5 şık (A, B, C, D, E) tam olmalıdır. Eksik şık varsa soru kökünün ölçtüğü klinik bilgiye uygun mantıklı tıp çeldiricileri üreterek 5 şıkkı tamamla.
   - Tamamlanan şıkların harflerini "yapay_zeka_tamamlanan_siklar" alanında belirt (örn: ["E"] veya ["D", "E"]).
4. Açıklama kaynakta varsa yazımını toparla ve maddeli forma getir; eksik veya anlamsızsa tıbbi gerekçesiyle düzenle.
5. Kurul/ders/konu için kaynakta mevcut etiketleri koru; emin değilsen boş bırak ve inceleme iste.
{curriculum_hint}
KAYNAK:
{json.dumps(source, ensure_ascii=False, indent=2)}

6. Çıktıdaki alan SIRASINA uy: önce tespit_raporu ve secenek_analizi, en son dogru_secenek. Doğru şıkkı analizden önce belirleme.
7. soru_koku içinde klinik/laboratuvar verilerini satır atlayarak (\\n) düzenle; aciklama maddeli (- ) ve başlıklı olsun (Olay Örgüsü / Neden-Sonuç İlişkisi / Temel Klinik Kural).

ŞU JSON ŞEMASINI DÖNDÜR (alanları bu sırayla yaz):
{{
  "tespit_raporu": {{"tespit_edilen_kusur": "dizgi hatası, eksik kök veya mantık problemi", "uygulanan_mudahale": "anlamı değiştirmeden yapılan düzeltmenin gerekçesi"}},
  "secenek_analizi": {{"A":"kısa mekanizma analizi", "B":"", "C":"", "D":"", "E":""}},
  "soru_koku": "Yazım hataları, eksik/fazla harfleri düzeltilmiş soru kökü",
  "secenekler": {{"A":"", "B":"", "C":"", "D":"", "E":""}},
  "yapay_zeka_tamamlanan_siklar": ["E"],
  "aciklama": "Maddeli (- ) açıklama: Olay Örgüsü / Neden-Sonuç İlişkisi / Temel Klinik Kural",
  "kurul_adi": "kaynak değeri veya müfredat kodu",
  "ders_adi": "kaynak değeri veya branş",
  "konu_adi": "kaynak değeri veya konu başlığı",
  "degisen_alanlar": ["soru_koku" ve/veya değişen diğer alanlar],
  "degisiklik_ozeti": "Düzeltilen harf hatası, fazla/eksik harf veya kelime düzeltmelerinin somut özeti",
  "review_required": true,
  "dogru_secenek": "A/B/C/D/E (analizden sonra, en son alan)"
}}"""


CLOUD_STATE = OUT / "checkpoint_cloud.json"


def load_done() -> set[str]:
    """İncelenen sorular (yerel + bulut). Tüm sorular bitmeden hiçbiri tekrar incelenmez."""
    done: set[str] = set()
    for path in (STATE, CLOUD_STATE):
        try:
            done |= set(json.loads(path.read_text(encoding="utf-8")).get("done_ids") or [])
        except Exception:
            pass
    return done


def save_state(done: set[str]) -> None:
    lib.write_json(STATE, {"done_ids": sorted(done), "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S")})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10, help="Bu çalıştırmada incelenecek en fazla soru")
    parser.add_argument("--full", action="store_true", help="Yalnızca tüm sorular incelenmişse yeni tur başlatır; aksi halde etkisizdir")
    args = parser.parse_args()
    if not SOURCE.exists():
        print(f"Kaynak bulunamadı: {SOURCE}", file=sys.stderr)
        return 1

    raw = json.loads(SOURCE.read_text(encoding="utf-8"))
    questions = raw if isinstance(raw, list) else raw.get("questions", [])
    OUT.mkdir(parents=True, exist_ok=True)
    done = load_done()
    eligible = set()
    for q in questions:
        v = source_view(q)
        if q.get("id") and len(v["soru_koku"].strip()) >= 15 and len(v["secenekler"]) >= 4:
            eligible.add(str(q["id"]))
    if eligible and eligible <= done:  # tüm sorular bir kez incelendi → yeni tur
        log_msg("Tüm sorular incelendi; yeni tur başlıyor")
        done = set()
        save_state(done)
        if CLOUD_STATE.exists():
            lib.write_json(CLOUD_STATE, {"done_ids": [], "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S")})
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
                proposal = lib.chat(MODEL, prompt(source, curr_summary), system=SYSTEM, as_json=True, timeout=180, num_predict=3000)
                if not isinstance(proposal, dict):
                    raise ValueError("Model geçerli JSON nesnesi döndürmedi")
                ratio = support_ratio(source, proposal)
                changed = [str(x) for x in proposal.get("degisen_alanlar") or []]
                review_required = bool(proposal.get("review_required", True)) or ratio < 0.80
                model_answer = str(proposal.get("dogru_secenek") or "").strip().upper()[:1]
                if source["dogru_secenek"] and model_answer != str(source["dogru_secenek"]).strip().upper()[:1]:
                    review_required = True  # analiz kaynaktaki cevapla çelişiyor
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
